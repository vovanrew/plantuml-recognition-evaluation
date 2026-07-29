"""Paired percentile bootstrap for 95% CIs on pairwise model differences.

Design (methodology/analysis-protocol.md, Statistical uncertainty):
  * Resample *diagrams*, not metrics. ``make_resamples`` draws ``n`` index samples
    of the 1000 diagram positions with replacement from one fixed ``random.Random``
    seed. The SAME index sample is applied to every model; because the loader sorts
    each model's rows by key into the identical order, positional resampling is
    automatically *paired by diagram*.
  * Per resample, per model, every metric is recomputed by re-running the Task-1
    pooling on the resampled rows -- ``model_stats`` calls the ``analysis.aggregate``
    primitives verbatim, so the statistic on the un-resampled (identity) sample
    equals the master-table value (centre reproduction).
  * Metrics with per-diagram components get CIs: CSR, Element/Relationship F1
    micro (re-pooled tp/fp/fn) and macro (re-averaged per-diagram p/r/f1), chrF++
    macro (per-diagram score, non-compiled -> 0 under zeros_for_failed), type
    accuracy (re-pooled matched/correct/excluded over compiled), and per-relation
    F1 (re-pooled from the runner's additive per-diagram ``by_relation``).
  * chrF++ MICRO is a corpus sacrebleu statistic with no per-diagram component:
    reported as a point estimate from the model summary, flagged "no CI".

Pairwise difference CI = percentile (2.5 / 97.5) of the ``n`` resampled
differences ``stat_A - stat_B``; ``excludes_zero`` marks a CI off zero. Per-model
metric CIs are emitted too (Task 3 needs them for error bars).
"""
from __future__ import annotations

import math
import random

from analysis.aggregate import (
    POPULATIONS, RELATIONS,
    chrf_macro, csr_rate, mean_macro, pool_micro, pool_type_acc,
)
from analysis.loader import ModelData

SEED = 20260614          # fixed bootstrap seed (recorded; re-runs are byte-identical)
N_RESAMPLES = 1000       # paired bootstrap resamples (evaluation_plan.md)
CI_Q = (0.025, 0.975)    # 95% percentile interval


# --------------------------------------------------------------------------- #
# statistic identifiers
# --------------------------------------------------------------------------- #

def stat_ids() -> list[str]:
    """The CI-eligible statistic ids, in a fixed order (matches ``model_stats``).

    Id grammar (``|``-separated): ``csr|csr``; ``<metric>|<level>|<population>``
    for element/relationship F1 (level micro|macro) and chrF++ macro;
    ``type_accuracy|accuracy|compiled_only``; and per-relation
    ``relationship_f1::<rel>|micro|<population>``.
    """
    ids = ["csr|csr"]
    for pop in POPULATIONS:
        ids += [f"element_f1|micro|{pop}", f"element_f1|macro|{pop}",
                f"relationship_f1|micro|{pop}", f"relationship_f1|macro|{pop}",
                f"chrf|macro|{pop}"]
    ids.append("type_accuracy|accuracy|compiled_only")
    for pop in POPULATIONS:
        for rel in RELATIONS:
            ids.append(f"relationship_f1::{rel}|micro|{pop}")
    return ids


def point_only_ids() -> list[str]:
    """chrF++ micro ids -- reported as point estimates with no CI."""
    return [f"chrf|micro|{pop}" for pop in POPULATIONS]


def parse_stat_id(sid: str) -> dict:
    """Decompose a stat id into {metric, level, population, relation} for display."""
    relation = None
    head, *rest = sid.split("|")
    if head.startswith("relationship_f1::"):
        metric, relation = "relationship_f1", head.split("::", 1)[1]
    else:
        metric = head
    level = rest[0] if rest else ""
    population = rest[1] if len(rest) > 1 else ""
    return {"metric": metric, "level": level, "population": population, "relation": relation}


# --------------------------------------------------------------------------- #
# one model's full statistic bundle for a (possibly resampled) row list
# --------------------------------------------------------------------------- #

def model_stats(rows: list[dict]) -> dict[str, float | None]:
    """Every CI-eligible statistic for ``rows`` via the Task-1 aggregate primitives.

    Population is a row filter (each metric uses its own per-diagram ``compiled``
    flag): zeros_for_failed pools all rows, compiled_only pools compiled rows.
    A per-relation statistic is ``None`` when the relation is absent on both sides
    of the (resampled) set -- F1 is then undefined and excluded from percentiles.
    """
    el = [r["element"] for r in rows]
    rel = [r["relationship"] for r in rows]
    chrf = [r["chrf"] for r in rows]
    csr = [r["csr"] for r in rows]

    out: dict[str, float | None] = {"csr|csr": csr_rate(csr)["csr"]}
    for pop in POPULATIONS:
        el_pop = el if pop == "zeros_for_failed" else [r for r in el if r["compiled"]]
        rel_pop = rel if pop == "zeros_for_failed" else [r for r in rel if r["compiled"]]
        out[f"element_f1|micro|{pop}"] = pool_micro(el_pop)["f1"]
        out[f"element_f1|macro|{pop}"] = mean_macro(el_pop)["f1"]
        out[f"relationship_f1|micro|{pop}"] = pool_micro(rel_pop)["f1"]
        out[f"relationship_f1|macro|{pop}"] = mean_macro(rel_pop)["f1"]
        out[f"chrf|macro|{pop}"] = chrf_macro(chrf, pop)
    out["type_accuracy|accuracy|compiled_only"] = pool_type_acc(
        [r for r in el if r["compiled"]])["accuracy"]
    for pop in POPULATIONS:
        rel_pop = rel if pop == "zeros_for_failed" else [r for r in rel if r["compiled"]]
        for rl in RELATIONS:
            m = pool_micro([rr["by_relation"][rl] for rr in rel_pop])
            total = m["tp"] + m["fp"] + m["fn"]
            out[f"relationship_f1::{rl}|micro|{pop}"] = m["f1"] if total > 0 else None
    return out


def chrf_micro_points(md: ModelData) -> dict[str, float | None]:
    """Point-only chrF++ micro per population, read straight from the summary."""
    chrf_summary = md.summaries.get("chrf", {})
    return {f"chrf|micro|{pop}": chrf_summary.get(pop, {}).get("micro")
            for pop in POPULATIONS}


# --------------------------------------------------------------------------- #
# percentile + interval helpers
# --------------------------------------------------------------------------- #

def percentile(sorted_vals: list[float], q: float) -> float:
    """Type-7 (linear-interpolation) percentile of an ALREADY-SORTED list."""
    n = len(sorted_vals)
    if n == 0:
        return float("nan")
    if n == 1:
        return float(sorted_vals[0])
    pos = q * (n - 1)
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return float(sorted_vals[lo])
    frac = pos - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def ci_from_values(values: list[float | None], point: float | None) -> dict:
    """Per-model 95% percentile CI from the resampled statistic values.

    ``None`` resamples (an undefined per-relation/type-accuracy statistic) are
    dropped; the point estimate is carried through verbatim (it may be None)."""
    valid = sorted(v for v in values if v is not None)
    if not valid:
        return {"point": point, "ci_low": None, "ci_high": None, "n_valid": 0}
    return {"point": point,
            "ci_low": percentile(valid, CI_Q[0]),
            "ci_high": percentile(valid, CI_Q[1]),
            "n_valid": len(valid)}


def diff_ci(values_a: list[float | None], values_b: list[float | None],
            point_a: float | None, point_b: float | None) -> dict:
    """Paired difference CI: percentile of ``a - b`` over resamples where BOTH
    are defined. ``excludes_zero`` is True iff the whole CI is on one side of 0."""
    diffs = sorted(a - b for a, b in zip(values_a, values_b)
                   if a is not None and b is not None)
    diff_point = (point_a - point_b) if (point_a is not None and point_b is not None) else None
    if not diffs:
        return {"diff_point": diff_point, "ci_low": None, "ci_high": None,
                "excludes_zero": False, "n_valid": 0}
    lo, hi = percentile(diffs, CI_Q[0]), percentile(diffs, CI_Q[1])
    return {"diff_point": diff_point, "ci_low": lo, "ci_high": hi,
            "excludes_zero": bool(lo > 0.0 or hi < 0.0), "n_valid": len(diffs)}


# --------------------------------------------------------------------------- #
# resampling + panel bootstrap
# --------------------------------------------------------------------------- #

def make_resamples(n_rows: int, n_resamples: int = N_RESAMPLES, seed: int = SEED) -> list[list[int]]:
    """``n_resamples`` index draws of ``n_rows`` positions with replacement, from a
    single fixed-seed RNG. Pure in (n_rows, n_resamples, seed) -> the same draws are
    reused for every model, which is what makes the bootstrap paired by diagram."""
    rng = random.Random(seed)
    pop = range(n_rows)
    return [rng.choices(pop, k=n_rows) for _ in range(n_resamples)]


def bootstrap_models(
    models: list[ModelData],
    n_resamples: int = N_RESAMPLES,
    seed: int = SEED,
    *,
    models_total: int | None = None,
    pending_ids: list[str] | None = None,
    refused_ids: list[str] | None = None,
) -> dict:
    """Paired bootstrap over ``models`` -> per-model CIs + pairwise difference CIs.

    All models must share row count (the loader guarantees a key-paired 1000-row
    panel). ``models_total`` / ``pending_ids`` / ``refused_ids`` are registry-derived
    and recorded in meta so a partial table ("models included: N/total") is never
    mistaken for final.
    """
    ids = stat_ids()
    if models:
        n_rows = len(models[0].rows)
        for m in models:
            if len(m.rows) != n_rows:
                raise ValueError(
                    f"row-count mismatch: {models[0].entry.id}={n_rows} vs "
                    f"{m.entry.id}={len(m.rows)} -- pairing requires equal row sets")
    else:
        n_rows = 0

    resamples = make_resamples(n_rows, n_resamples, seed)
    point = {m.entry.id: model_stats(m.rows) for m in models}
    boot = {m.entry.id: [model_stats([m.rows[i] for i in draw]) for draw in resamples]
            for m in models}

    per_model = {}
    for m in models:
        mid = m.entry.id
        per_model[mid] = {
            sid: ci_from_values([b[sid] for b in boot[mid]], point[mid][sid])
            for sid in ids
        }
    per_model_point_only = {m.entry.id: chrf_micro_points(m) for m in models}

    pairwise = []
    mids = [m.entry.id for m in models]
    for i in range(len(mids)):
        for j in range(i + 1, len(mids)):
            a, b = mids[i], mids[j]
            for sid in ids:
                d = diff_ci([x[sid] for x in boot[a]], [x[sid] for x in boot[b]],
                            point[a][sid], point[b][sid])
                pairwise.append({"model_a": a, "model_b": b, "stat": sid, **d})

    meta = {
        "seed": seed,
        "n_resamples": n_resamples,
        "method": "paired percentile bootstrap (2.5/97.5), resample diagrams, "
                  "shared draws across models",
        "models_included": len(models),
        "models_total": models_total if models_total is not None else len(models),
        "included_ids": list(mids),
        "displays": {m.entry.id: m.entry.display for m in models},
        "pending_ids": list(pending_ids or []),
        "refused_ids": list(refused_ids or []),
        "ci_stats": ids,
        "point_only_stats": point_only_ids(),
        "populations": POPULATIONS,
        "relations": RELATIONS,
    }
    return {"meta": meta, "per_model": per_model,
            "per_model_point_only": per_model_point_only, "pairwise": pairwise}
