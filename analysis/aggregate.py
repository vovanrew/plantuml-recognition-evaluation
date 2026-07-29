"""Aggregation: pool joined per-diagram rows into the master table.

Pooling recipe (verified to reproduce every runner summary exactly on the four
scored models -- see the validation gate in methodology/analysis-protocol.md):

- CSR              = compiled / n over the cell's csr rows.
- Element/Rel F1   micro = pool per-diagram tp/fp/fn; macro = mean of the stored
                    per-diagram precision/recall/f1. Population is a row filter:
                    zeros_for_failed pools ALL cell rows (non-compiled rows already
                    carry tp=0,fp=0,fn=|GT| on disk); compiled_only pools the
                    ``compiled`` rows. Stored values are pooled as-is, never recomputed.
- chrF++  macro    is poolable: zeros_for_failed = mean(score if compiled else 0)
                    over all cell rows (per-diagram score is stored RAW); compiled_only
                    = mean(score) over compiled rows. chrF++ MICRO is a corpus
                    sacrebleu statistic with no per-diagram component -> read straight
                    from the summary (overall only; None for per-(type,tier) cells).
- type accuracy    pools matched/correct/excluded over COMPILED element rows;
                    denominator = matched - excluded; accuracy = correct/denominator.
- per-relation F1  has no per-diagram breakdown -> read from summary.by_relation.
- per-GT-type acc  has no per-diagram breakdown -> read from summary.type_accuracy.
"""
from __future__ import annotations

from analysis.loader import ModelData

RELATIONS = ["inheritance", "composition", "aggregation", "dependency",
             "association", "message"]
POPULATIONS = ["compiled_only", "zeros_for_failed"]
TYPES = ["class", "sequence"]
TIERS = [1, 2, 3, 4]


# --------------------------------------------------------------------------- #
# pure pooling primitives
# --------------------------------------------------------------------------- #

def pool_micro(rows: list[dict]) -> dict:
    """Micro P/R/F1 from summed tp/fp/fn (rows pre-filtered for population)."""
    tp = sum(r["tp"] for r in rows)
    fp = sum(r["fp"] for r in rows)
    fn = sum(r["fn"] for r in rows)
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return {"precision": p, "recall": r, "f1": f, "tp": tp, "fp": fp, "fn": fn}


def mean_macro(rows: list[dict]) -> dict:
    """Macro P/R/F1 = mean of the stored per-diagram precision/recall/f1."""
    n = len(rows)
    if n == 0:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    return {
        "precision": sum(r["precision"] for r in rows) / n,
        "recall": sum(r["recall"] for r in rows) / n,
        "f1": sum(r["f1"] for r in rows) / n,
    }


def csr_rate(csr_rows: list[dict]) -> dict:
    """CSR = compiled / n (population-independent; it defines the populations)."""
    n = len(csr_rows)
    compiled = sum(1 for r in csr_rows if r["compiled"])
    return {"compiled": compiled, "n": n, "csr": compiled / n if n else 0.0}


def chrf_macro(chrf_rows: list[dict], population: str) -> float:
    """Macro chrF++ for a population. zeros_for_failed forces non-compiled to 0
    (per-diagram score is stored RAW); compiled_only averages compiled scores."""
    if population == "zeros_for_failed":
        vals = [r["score"] if r["compiled"] else 0.0 for r in chrf_rows]
    elif population == "compiled_only":
        vals = [r["score"] for r in chrf_rows if r["compiled"]]
    else:  # pragma: no cover - guarded by POPULATIONS
        raise ValueError(f"unknown population {population!r}")
    return sum(vals) / len(vals) if vals else 0.0


def pool_type_acc(element_rows: list[dict]) -> dict:
    """Type accuracy over name-matched nodes (rows pre-filtered to compiled).
    accuracy = correct / (matched - excluded); None when the denominator is 0."""
    matched = sum(r["type_accuracy"]["matched"] for r in element_rows)
    correct = sum(r["type_accuracy"]["correct"] for r in element_rows)
    excluded = sum(r["type_accuracy"]["excluded"] for r in element_rows)
    denominator = matched - excluded
    accuracy = correct / denominator if denominator else None
    return {"matched": matched, "correct": correct, "excluded": excluded,
            "denominator": denominator, "accuracy": accuracy,
            "n_compiled": len(element_rows)}


# --------------------------------------------------------------------------- #
# cell + model assembly
# --------------------------------------------------------------------------- #

def _split_by_population(metric_rows: list[dict]) -> dict[str, list[dict]]:
    return {
        "zeros_for_failed": metric_rows,
        "compiled_only": [r for r in metric_rows if r["compiled"]],
    }


def _f1_block(metric_rows: list[dict]) -> dict:
    """{population: {micro, macro, n}} for an element/relationship metric."""
    out = {}
    for pop, rows in _split_by_population(metric_rows).items():
        out[pop] = {"micro": pool_micro(rows), "macro": mean_macro(rows), "n": len(rows)}
    return out


def _chrf_block(chrf_rows: list[dict], micro_readthrough: dict | None) -> dict:
    """{population: {micro, macro, n}}; micro is read-through (overall) or None (sub-cell)."""
    out = {}
    for pop in POPULATIONS:
        n = len(chrf_rows) if pop == "zeros_for_failed" else sum(1 for r in chrf_rows if r["compiled"])
        micro = micro_readthrough.get(pop) if micro_readthrough else None
        out[pop] = {"micro": micro, "macro": chrf_macro(chrf_rows, pop), "n": n}
    return out


def _gap_triple(all_v, compiled_v) -> dict:
    """``{all, compiled, gap}`` for one scalar, gap = compiled_only - zeros_for_failed.
    gap is None when either side is None (e.g. chrf micro outside the overall scope)."""
    gap = compiled_v - all_v if all_v is not None and compiled_v is not None else None
    return {"all": all_v, "compiled": compiled_v, "gap": gap}


def population_gap(element_block: dict, relationship_block: dict, chrf_block: dict) -> dict:
    """The compiled_only - zeros_for_failed gap per metric -- the headline measure of
    how much a model's apparent quality is propped up by selective failure (a model
    that drops its hard cases scores far higher on compiled_only than on all-1000).
    Reported on f1 for the structural metrics and on the score for chrF++."""
    def f1_gap(blk, level):
        return _gap_triple(blk["zeros_for_failed"][level]["f1"],
                           blk["compiled_only"][level]["f1"])

    def chrf_gap(level):
        return _gap_triple(chrf_block["zeros_for_failed"][level],
                           chrf_block["compiled_only"][level])

    return {
        "element_f1": {"micro": f1_gap(element_block, "micro"),
                       "macro": f1_gap(element_block, "macro")},
        "relationship_f1": {"micro": f1_gap(relationship_block, "micro"),
                            "macro": f1_gap(relationship_block, "macro")},
        "chrf": {"micro": chrf_gap("micro"), "macro": chrf_gap("macro")},
    }


def _cell(rows: list[dict], chrf_micro: dict | None = None) -> dict:
    """One scope's aggregated metrics. ``chrf_micro`` is supplied (read-through)
    only for the overall scope; sub-cells get None (corpus stat not poolable)."""
    element = _f1_block([r["element"] for r in rows])
    relationship = _f1_block([r["relationship"] for r in rows])
    chrf = _chrf_block([r["chrf"] for r in rows], chrf_micro)
    return {
        "n": len(rows),
        "csr": csr_rate([r["csr"] for r in rows]),
        "element_f1": element,
        "relationship_f1": relationship,
        "chrf": chrf,
        "type_accuracy": pool_type_acc([r["element"] for r in rows if r["element"]["compiled"]]),
        "population_gap": population_gap(element, relationship, chrf),
    }


def _per_relation(rel_summary: dict) -> dict:
    """Read-through per-relation F1 for both populations from summary.by_relation."""
    out = {}
    for pop in POPULATIONS:
        by_rel = rel_summary.get(pop, {}).get("by_relation", {})
        out[pop] = {rel: by_rel[rel] for rel in RELATIONS if rel in by_rel}
    return out


def _type_acc_per_gt(element_summary: dict) -> dict:
    """Read-through per-GT-type support/accuracy table (+ excluded) from summary."""
    ta = element_summary.get("type_accuracy", {})
    return {
        "population": ta.get("population", "compiled_only"),
        "matched": ta.get("matched"),
        "correct": ta.get("correct"),
        "excluded": ta.get("excluded"),
        "denominator": ta.get("denominator"),
        "accuracy": ta.get("accuracy"),
        "per_type": ta.get("per_type", {}),
    }


def _model_block(md: ModelData) -> dict:
    rows = md.rows
    e = md.entry
    chrf_micro = {pop: md.summaries["chrf"].get(pop, {}).get("micro") for pop in POPULATIONS}

    by_type = {t: _cell([r for r in rows if r["primary_type"] == t])
               for t in TYPES if any(r["primary_type"] == t for r in rows)}
    tiers_present = sorted({r["tier"] for r in rows})
    by_tier = {tier: _cell([r for r in rows if r["tier"] == tier]) for tier in tiers_present}

    return {
        "display": e.display,
        "arm": e.arm,
        "lab": e.lab,
        "family": e.family,
        "params_total_b": e.params_total_b,
        "params_active_b": e.params_active_b,
        "status": e.status,
        "run_dir": e.run_dir,
        "overall": _cell(rows, chrf_micro=chrf_micro),
        "by_type": by_type,
        "by_tier": by_tier,
        "per_relation": _per_relation(md.summaries["relationship_f1"]),
        "type_accuracy_per_gt_type": _type_acc_per_gt(md.summaries["element_f1"]),
    }


def build_master_table(
    models: list[ModelData],
    *,
    models_total: int,
    pending_ids: list[str],
    refused_ids: list[str] | None = None,
    label: str = "main",
) -> dict:
    """Assemble the master table for the given (eligible) models.

    ``models_total`` / ``pending_ids`` / ``refused_ids`` are registry-derived and
    recorded in meta so a partial table ("models included: N/total") is never
    mistaken for final. ``pending_ids`` = runs not yet on disk; ``refused_ids`` =
    runs present but excluded by the reasoning_leak gate.
    """
    return {
        "meta": {
            "label": label,
            "models_included": len(models),
            "models_total": models_total,
            "included_ids": [m.entry.id for m in models],
            "pending_ids": list(pending_ids),
            "refused_ids": list(refused_ids or []),
            "populations": POPULATIONS,
            "relations": RELATIONS,
            "types": TYPES,
            "tiers": TIERS,
        },
        "models": {m.entry.id: _model_block(m) for m in models},
    }
