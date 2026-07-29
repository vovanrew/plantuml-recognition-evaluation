"""Emit the paired-bootstrap result as paper-facing markdown, tidy CSV(s), full JSON.

The JSON is the complete artifact (per-model CIs, point-only chrF++ micro, and the
pairwise difference CIs) consumed downstream (Task 3 error bars). The CSVs are
tidy/long for pivoting. The markdown surfaces the headline per-model CIs, the
pairwise model-difference CIs with an ``excludes 0`` significance flag, and the
per-relation F1 CIs.

Output is deterministic (registry/iteration order fixed, no timestamps), so a
re-run after a model lands reproduces byte-identical files for unchanged models.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from analysis.bootstrap import parse_stat_id

# Headline statistics carried in the markdown (full set lives in CSV/JSON).
_HEADLINE = [
    ("csr|csr", "CSR"),
    ("element_f1|micro|zeros_for_failed", "Element F1 micro (zeros)"),
    ("element_f1|micro|compiled_only", "Element F1 micro (compiled)"),
    ("relationship_f1|micro|zeros_for_failed", "Rel F1 micro (zeros)"),
    ("relationship_f1|micro|compiled_only", "Rel F1 micro (compiled)"),
    ("chrf|macro|zeros_for_failed", "chrF++ macro (zeros)"),
    ("chrf|macro|compiled_only", "chrF++ macro (compiled)"),
    ("type_accuracy|accuracy|compiled_only", "Type acc"),
]


# ------------------------------ formatting --------------------------------- #

def _fmt(sid: str, x: float | None) -> str:
    if x is None:
        return "—"
    decimals = 2 if parse_stat_id(sid)["metric"] == "chrf" else 3
    return f"{x:.{decimals}f}"


def _cell(sid: str, c: dict) -> str:
    """'point [lo, hi]' for a per-model CI cell ('point' alone when no CI)."""
    pt = _fmt(sid, c["point"])
    if c["ci_low"] is None:
        return pt
    return f"{pt} [{_fmt(sid, c['ci_low'])}, {_fmt(sid, c['ci_high'])}]"


def _diff_cell(sid: str, d: dict) -> tuple[str, str, str]:
    pt = _fmt(sid, d["diff_point"])
    if d["ci_low"] is None:
        return pt, "—", ""
    ci = f"[{_fmt(sid, d['ci_low'])}, {_fmt(sid, d['ci_high'])}]"
    return pt, ci, ("**yes**" if d["excludes_zero"] else "no")


# ------------------------------ markdown ----------------------------------- #

def render_markdown(result: dict) -> str:
    meta = result["meta"]
    displays = meta["displays"]
    pm = result["per_model"]
    po = result["per_model_point_only"]
    ids = meta["included_ids"]
    out: list[str] = []

    out.append("# Paired bootstrap CIs — zero-shot image→PlantUML benchmark")
    out.append("")
    out.append(f"**Models included: {meta['models_included']}/{meta['models_total']}**")
    out.append("")
    if meta["pending_ids"]:
        out.append("Pending / not yet aggregated: " + ", ".join(meta["pending_ids"]))
        out.append("")
    if meta["refused_ids"]:
        out.append("Refused (reasoning_leak): " + ", ".join(meta["refused_ids"]))
        out.append("")
    out.append(f"Method: {meta['method']}; n={meta['n_resamples']} resamples, seed={meta['seed']}. "
               "Cells are `point [2.5th, 97.5th]`. CSR / F1 / type-accuracy on the 0–1 scale "
               "(3 dp); chrF++ on its native scale (2 dp). chrF++ **micro** is a corpus statistic "
               "with no per-diagram component — reported as a point estimate, no CI.")
    out.append("")

    # --- per-model headline CIs ---
    out.append("## Per-model 95% CIs (headline metrics)")
    out.append("")
    header = "| Model | " + " | ".join(lbl for _, lbl in _HEADLINE) + " |"
    out.append(header)
    out.append("|" + "---|" * (len(_HEADLINE) + 1))
    for mid in ids:
        cells = " | ".join(_cell(sid, pm[mid][sid]) for sid, _ in _HEADLINE)
        out.append(f"| {displays[mid]} | {cells} |")
    out.append("")
    out.append("chrF++ micro (point estimate, no CI), zeros / compiled:")
    out.append("")
    for mid in ids:
        z = po[mid]["chrf|micro|zeros_for_failed"]
        c = po[mid]["chrf|micro|compiled_only"]
        out.append(f"- **{displays[mid]}**: {_fmt('chrf', z)} / {_fmt('chrf', c)}")
    out.append("")

    # --- pairwise differences for each headline metric ---
    out.append("## Pairwise model-difference CIs")
    out.append("")
    out.append("Δ = row model − column model (positive ⇒ the first model scores higher). "
               "`excludes 0` flags a CI that does not contain zero (significant at 95%).")
    out.append("")
    by_stat: dict[str, list[dict]] = {}
    for d in result["pairwise"]:
        by_stat.setdefault(d["stat"], []).append(d)
    for sid, lbl in _HEADLINE:
        out.append(f"### {lbl}")
        out.append("")
        out.append("| Pair (A − B) | Δ | 95% CI | excludes 0 |")
        out.append("|---|---|---|---|")
        for d in by_stat.get(sid, []):
            pt, ci, sig = _diff_cell(sid, d)
            pair = f"{displays[d['model_a']]} − {displays[d['model_b']]}"
            out.append(f"| {pair} | {pt} | {ci} | {sig} |")
        out.append("")

    # --- per-relation F1 CIs (per model) ---
    out.append("## Relationship F1 by relation type — per-model 95% CIs")
    out.append("")
    relations = meta["relations"]
    for pop, plbl in (("zeros_for_failed", "zeros_for_failed"), ("compiled_only", "compiled_only")):
        out.append(f"### Population: {plbl} (micro F1)")
        out.append("")
        out.append("| Model | " + " | ".join(relations) + " |")
        out.append("|" + "---|" * (len(relations) + 1))
        for mid in ids:
            cells = " | ".join(_cell(f"relationship_f1::{rel}|micro|{pop}",
                                     pm[mid][f"relationship_f1::{rel}|micro|{pop}"])
                                for rel in relations)
            out.append(f"| {displays[mid]} | {cells} |")
        out.append("")

    return "\n".join(out) + "\n"


# ------------------------------ CSV (tidy) --------------------------------- #

_PER_MODEL_FIELDS = ["model_id", "display", "stat", "metric", "level", "population",
                     "relation", "point", "ci_low", "ci_high", "n_valid", "has_ci"]
_PAIRWISE_FIELDS = ["model_a", "display_a", "model_b", "display_b", "stat", "metric",
                    "level", "population", "relation", "diff_point", "ci_low", "ci_high",
                    "excludes_zero", "n_valid"]


def _v(x):
    return "" if x is None else x


def _per_model_rows(result: dict) -> list[dict]:
    meta = result["meta"]
    displays = meta["displays"]
    rows = []
    for mid in meta["included_ids"]:
        for sid in meta["ci_stats"]:
            c = result["per_model"][mid][sid]
            p = parse_stat_id(sid)
            rows.append({"model_id": mid, "display": displays[mid], "stat": sid,
                         "metric": p["metric"], "level": p["level"], "population": p["population"],
                         "relation": _v(p["relation"]), "point": _v(c["point"]),
                         "ci_low": _v(c["ci_low"]), "ci_high": _v(c["ci_high"]),
                         "n_valid": c["n_valid"], "has_ci": c["ci_low"] is not None})
        # point-only chrF++ micro
        for sid, val in result["per_model_point_only"][mid].items():
            p = parse_stat_id(sid)
            rows.append({"model_id": mid, "display": displays[mid], "stat": sid,
                         "metric": p["metric"], "level": p["level"], "population": p["population"],
                         "relation": _v(p["relation"]), "point": _v(val),
                         "ci_low": "", "ci_high": "", "n_valid": 0, "has_ci": False})
    return rows


def _pairwise_rows(result: dict) -> list[dict]:
    displays = result["meta"]["displays"]
    rows = []
    for d in result["pairwise"]:
        p = parse_stat_id(d["stat"])
        rows.append({"model_a": d["model_a"], "display_a": displays[d["model_a"]],
                     "model_b": d["model_b"], "display_b": displays[d["model_b"]],
                     "stat": d["stat"], "metric": p["metric"], "level": p["level"],
                     "population": p["population"], "relation": _v(p["relation"]),
                     "diff_point": _v(d["diff_point"]), "ci_low": _v(d["ci_low"]),
                     "ci_high": _v(d["ci_high"]), "excludes_zero": d["excludes_zero"],
                     "n_valid": d["n_valid"]})
    return rows


def _write_csv(path: Path, fields: list[str], rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


# ------------------------------ entry point -------------------------------- #

def write_ci_table(result: dict, out_dir: str | Path, basename: str = "ci_table") -> dict:
    """Write JSON + markdown + CSVs under ``out_dir``; return {kind: Path}."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{basename}.json",
        "md": out_dir / f"{basename}.md",
        "csv": out_dir / f"{basename}.csv",
        "pairwise_csv": out_dir / f"{basename}_pairwise.csv",
    }
    paths["json"].write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    paths["md"].write_text(render_markdown(result), encoding="utf-8")
    _write_csv(paths["csv"], _PER_MODEL_FIELDS, _per_model_rows(result))
    _write_csv(paths["pairwise_csv"], _PAIRWISE_FIELDS, _pairwise_rows(result))
    return paths
