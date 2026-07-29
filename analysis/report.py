"""Emit the master table as paper-facing markdown, tidy CSV(s), and full JSON.

The JSON is the complete nested artifact. The CSVs are tidy/long for pivoting.
The markdown mirrors the protocol's anchor layout (overall micro table) so the
four scored models can be eye-checked against the validation gate, then adds the
macro, per-relation, type-accuracy, per-type and per-tier breakdowns.

Output is deterministic (registry/iteration order fixed, no timestamps) so a
re-run after a model lands reproduces byte-identical files for unchanged models.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from analysis.aggregate import POPULATIONS, RELATIONS, TYPES

# zeros first, compiled second -- matches the protocol anchor "z / c" notation
_PAIR_ORDER = ["zeros_for_failed", "compiled_only"]


# ------------------------------ formatting --------------------------------- #

def _r3(x):
    return "—" if x is None else f"{x:.3f}"


def _pct1(x):
    return "—" if x is None else f"{x * 100:.1f}%"


def _chrf2(x):
    return "—" if x is None else f"{x:.2f}"


def _pair(cell_metric: dict, stat_path, fmt) -> str:
    """Render 'zeros / compiled' for a two-population metric block."""
    def get(pop):
        node = cell_metric[pop]
        for k in stat_path:
            node = node[k]
        return node
    return f"{fmt(get('zeros_for_failed'))} / {fmt(get('compiled_only'))}"


# ------------------------------ markdown ----------------------------------- #

def _overall_row(mid: str, m: dict, cell: dict, kind: str) -> str:
    stat = ["micro", "f1"] if kind == "micro" else ["macro", "f1"]
    return "| {model} | {csr} | {el} | {rel} | {chrf} | {ta} |".format(
        model=m["display"],
        csr=_pct1(cell["csr"]["csr"]),
        el=_pair(cell["element_f1"], stat, _r3),
        rel=_pair(cell["relationship_f1"], stat, _r3),
        chrf=_pair(cell["chrf"], [("micro" if kind == "micro" else "macro")], _chrf2),
        ta=_r3(cell["type_accuracy"]["accuracy"]),
    )


def _gap_cell(triple: dict, fmt, prec: int) -> str:
    """Render 'all → compiled (Δgap)' for one population-gap triple."""
    a, c, g = triple["all"], triple["compiled"], triple["gap"]
    if g is None:
        return f"{fmt(a)} / {fmt(c)}"
    return f"{fmt(a)} → {fmt(c)} ({g:+.{prec}f})"


def _gap_table(table: dict) -> list[str]:
    lines = ["### Population gap (compiled-only − all-1000, micro)", "",
             "The `compiled_only` minus `zeros_for_failed` gap per metric — the headline "
             "measure of how much a model's apparent quality rests on selective failure. A "
             "model that drops/times out on its hard diagrams is graded on an easier subset, "
             "so its `compiled_only` score runs far above its honest all-1000 score; a large "
             "gap is that fingerprint (it tracks the answer rate / CSR).", "",
             "| Model | CSR | Element F1 (all → cmp, Δ) | Relationship F1 (all → cmp, Δ) | "
             "chrF++ (all → cmp, Δ) |",
             "|---|---|---|---|---|"]
    for mid, m in table["models"].items():
        pg = m["overall"]["population_gap"]
        lines.append("| {model} | {csr} | {el} | {rel} | {chrf} |".format(
            model=m["display"], csr=_pct1(m["overall"]["csr"]["csr"]),
            el=_gap_cell(pg["element_f1"]["micro"], _r3, 3),
            rel=_gap_cell(pg["relationship_f1"]["micro"], _r3, 3),
            chrf=_gap_cell(pg["chrf"]["micro"], _chrf2, 2)))
    lines.append("")
    return lines


def _scope_table(table: dict, get_cell, kind: str, title: str) -> list[str]:
    lines = [f"### {title} ({kind})", ""]
    lines.append("| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |")
    lines.append("|---|---|---|---|---|---|")
    for mid, m in table["models"].items():
        cell = get_cell(m)
        if cell is not None:
            lines.append(_overall_row(mid, m, cell, kind))
    lines.append("")
    return lines


def render_markdown(table: dict) -> str:
    meta = table["meta"]
    out: list[str] = []
    out.append("# Master table — zero-shot image→PlantUML benchmark")
    out.append("")
    out.append(f"**Models included: {meta['models_included']}/{meta['models_total']}** "
               f"(panel label: {meta['label']})")
    out.append("")
    if meta["pending_ids"]:
        out.append("Pending / not yet aggregated: " + ", ".join(meta["pending_ids"]))
        out.append("")
    out.append("Two populations reported side by side as `zeros_for_failed / compiled_only`: "
               "`zeros_for_failed` scores all diagrams (non-compiled = 0); `compiled_only` is "
               "over compiled cells, with CSR reported separately. chrF++ values in the headline "
               "tables are micro (corpus sacrebleu, available at the overall scope only); the "
               "macro tables and JSON carry the poolable chrF++ macro for every scope. Type "
               "accuracy is the `compiled_only` population by definition.")
    out.append("")

    # overall micro + macro
    out += _scope_table(table, lambda m: m["overall"], "micro", "Overall")
    out += _scope_table(table, lambda m: m["overall"], "macro", "Overall")

    # population gap (compiled-only - all-1000): the selective-failure fingerprint
    out += _gap_table(table)

    # per-relation (read-through, micro P/R/F1 from by_relation)
    out.append("### Relationship F1 by relation type (read-through)")
    out.append("")
    for mid, m in table["models"].items():
        out.append(f"**{m['display']}** — F1 (zeros_for_failed / compiled_only), support_gt:")
        out.append("")
        out.append("| Relation | F1 (z / c) | support_gt (z / c) |")
        out.append("|---|---|---|")
        pr = m["per_relation"]
        for rel in RELATIONS:
            z = pr["zeros_for_failed"].get(rel)
            c = pr["compiled_only"].get(rel)
            f1 = f"{_r3(z['f1']) if z else '—'} / {_r3(c['f1']) if c else '—'}"
            sup = f"{z['support_gt'] if z else '—'} / {c['support_gt'] if c else '—'}"
            out.append(f"| {rel} | {f1} | {sup} |")
        out.append("")

    # type accuracy by GT entity type (read-through, compiled_only)
    out.append("### Type accuracy by GT entity type (compiled_only, read-through)")
    out.append("")
    for mid, m in table["models"].items():
        pgt = m["type_accuracy_per_gt_type"]
        out.append(f"**{m['display']}** — pooled accuracy {_r3(pgt['accuracy'])} "
                   f"(matched {pgt['matched']}, excluded {pgt['excluded']}, "
                   f"denominator {pgt['denominator']}):")
        out.append("")
        out.append("| GT type | support | accuracy |")
        out.append("|---|---|---|")
        for gt, v in pgt["per_type"].items():
            out.append(f"| {gt} | {v['support']} | {_r3(v['accuracy'])} |")
        out.append("")

    # per-type and per-tier breakdowns (micro)
    out.append("## By diagram type")
    out.append("")
    for t in TYPES:
        out += _scope_table(table, lambda m, t=t: m["by_type"].get(t), "micro", f"Type: {t}")

    out.append("## By tier")
    out.append("")
    tiers = sorted({tier for m in table["models"].values() for tier in m["by_tier"]})
    for tier in tiers:
        out += _scope_table(table, lambda m, tier=tier: m["by_tier"].get(tier),
                            "micro", f"Tier {tier}")

    return "\n".join(out) + "\n"


# ------------------------------ CSV (tidy) --------------------------------- #

_FIELDS = ["label", "model_id", "display", "scope", "scope_value",
           "population", "metric", "stat", "value"]


def _csv_value(x):
    return "" if x is None else x


def _emit_cell_rows(label, mid, display, scope, scope_value, cell):
    rows = []

    def add(metric, stat, population, value):
        rows.append({"label": label, "model_id": mid, "display": display,
                     "scope": scope, "scope_value": scope_value, "population": population,
                     "metric": metric, "stat": stat, "value": _csv_value(value)})

    add("csr", "csr", "", cell["csr"]["csr"])
    add("csr", "compiled", "", cell["csr"]["compiled"])
    add("csr", "n", "", cell["csr"]["n"])
    for metric in ("element_f1", "relationship_f1"):
        for pop in POPULATIONS:
            blk = cell[metric][pop]
            for level in ("micro", "macro"):
                for comp in ("precision", "recall", "f1"):
                    add(metric, f"{level}_{comp}", pop, blk[level][comp])
            add(metric, "n", pop, blk["n"])
    for pop in POPULATIONS:
        add("chrf", "micro", pop, cell["chrf"][pop]["micro"])
        add("chrf", "macro", pop, cell["chrf"][pop]["macro"])
    # population gap (compiled_only - zeros_for_failed) as a third "population"
    pg = cell["population_gap"]
    for metric in ("element_f1", "relationship_f1"):
        for level in ("micro", "macro"):
            add(metric, f"{level}_f1", "gap", pg[metric][level]["gap"])
    for level in ("micro", "macro"):
        add("chrf", level, "gap", pg["chrf"][level]["gap"])
    ta = cell["type_accuracy"]
    for stat in ("accuracy", "matched", "correct", "excluded", "denominator", "n_compiled"):
        add("type_accuracy", stat, "compiled_only", ta[stat])
    return rows


def _tidy_rows(table: dict) -> list[dict]:
    label = table["meta"]["label"]
    rows = []
    for mid, m in table["models"].items():
        rows += _emit_cell_rows(label, mid, m["display"], "overall", "", m["overall"])
        for t, cell in m["by_type"].items():
            rows += _emit_cell_rows(label, mid, m["display"], "type", t, cell)
        for tier, cell in m["by_tier"].items():
            rows += _emit_cell_rows(label, mid, m["display"], "tier", str(tier), cell)
    return rows


def _per_relation_rows(table: dict) -> list[dict]:
    rows = []
    for mid, m in table["models"].items():
        for pop in POPULATIONS:
            for rel in RELATIONS:
                v = m["per_relation"][pop].get(rel)
                if v is None:
                    continue
                rows.append({"model_id": mid, "display": m["display"], "population": pop,
                             "relation": rel, "precision": v["precision"],
                             "recall": v["recall"], "f1": v["f1"],
                             "support_gt": v["support_gt"], "support_pred": v["support_pred"],
                             "n_diagrams_with_gt": v["n_diagrams_with_gt"], "n": v["n"]})
    return rows


def _type_acc_rows(table: dict) -> list[dict]:
    rows = []
    for mid, m in table["models"].items():
        pgt = m["type_accuracy_per_gt_type"]
        rows.append({"model_id": mid, "display": m["display"], "gt_type": "(all)",
                     "support": pgt["denominator"], "correct": pgt["correct"],
                     "accuracy": _csv_value(pgt["accuracy"])})
        for gt, v in pgt["per_type"].items():
            rows.append({"model_id": mid, "display": m["display"], "gt_type": gt,
                         "support": v["support"], "correct": v["correct"],
                         "accuracy": _csv_value(v["accuracy"])})
    return rows


def _write_csv(path: Path, fields: list[str], rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


# ------------------------------ entry point -------------------------------- #

def write_table(table: dict, out_dir: str | Path, basename: str = "master_table") -> dict:
    """Write JSON + markdown + CSVs under ``out_dir``; return {kind: Path}."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{basename}.json",
        "md": out_dir / f"{basename}.md",
        "csv": out_dir / f"{basename}.csv",
        "per_relation_csv": out_dir / f"{basename}_per_relation.csv",
        "type_accuracy_csv": out_dir / f"{basename}_type_accuracy.csv",
    }
    paths["json"].write_text(json.dumps(table, indent=2) + "\n", encoding="utf-8")
    paths["md"].write_text(render_markdown(table), encoding="utf-8")
    _write_csv(paths["csv"], _FIELDS, _tidy_rows(table))
    _write_csv(paths["per_relation_csv"],
               ["model_id", "display", "population", "relation", "precision", "recall",
                "f1", "support_gt", "support_pred", "n_diagrams_with_gt", "n"],
               _per_relation_rows(table))
    _write_csv(paths["type_accuracy_csv"],
               ["model_id", "display", "gt_type", "support", "correct", "accuracy"],
               _type_acc_rows(table))
    return paths
