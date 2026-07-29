"""Task-4 failure-case sampler: a stratified, reviewable index of failures for the
author's qualitative 30-50-case error write-up.

Pure selection + record-building (the CLI wiring lives in ``build_failure_index.py``).
Everything is read-only over ``data/`` and the Task-1/2/3 outputs; this module only
reads the joined per-diagram rows the loader produces plus the raw GT/prediction
files on disk, and emits an index under ``analysis/out/``.

Outcome classification (the failure population). Each joined per-diagram row is one
of four mutually exclusive classes, decided in this order (render success = CSR is
authoritative; all four metrics' per-diagram ``compiled`` flags agree on disk):

1. ``provider_drop``  -- no prediction reached the scorer: ``has_pred`` is False
   (equivalently csr ``error == "no prediction (missing/timeout)"``). No prediction
   puml / render file exists.
2. ``compile_fail``   -- a prediction exists but does not render: ``has_pred`` True,
   csr ``compiled`` False (csr ``error`` like ``"Error line N in file: ..."``). This
   covers the render!=parse edge: a prediction can structurally parse to a graph
   (Element matched/tp > 0) yet fail to render -- it is still a compile failure.
3. ``compiled_low_structural`` -- it rendered but is structurally wrong: ``compiled``
   True with Element OR Relationship F1 strictly below ``LOW_STRUCTURAL_F1`` (0.5).
4. ``ok``             -- compiled and both structural F1 at/above the threshold.

The sampler draws ``per_cell`` cases per (model x diagram_type x tier x outcome
class) over the three failure classes (``ok`` only when ``include_ok``), so the
review spans the whole failure spectrum rather than the most common mode. Empty
cells are skipped; cells larger than the cap are truncated and logged so a capped
sample is never mistaken for the full failure set. Selection is a per-cell seeded
shuffle over key-sorted rows: deterministic, idempotent, and per-cell independent
(adding a model never shifts another model's sample).
"""
from __future__ import annotations

import csv
import json
import logging
import random
from dataclasses import dataclass, field
from pathlib import Path

from analysis.aggregate import RELATIONS, TIERS, TYPES
from analysis.loader import ModelData

log = logging.getLogger(__name__)

SEED = 20260614                      # project convention (shared with the bootstrap)
LOW_STRUCTURAL_F1 = 0.5              # compiled but Element/Relationship F1 below this = a failure
SMALL_DIAGRAM_LINES = 40            # GT at/under this many lines is inlined regardless of class
SNIPPET_MAX_LINES = 80             # inlined GT/prediction text is truncated to this many lines

FAILURE_CLASSES = ("provider_drop", "compile_fail", "compiled_low_structural")
OUTCOME_CLASSES = FAILURE_CLASSES + ("ok",)


# --------------------------------------------------------------------------- #
# classification
# --------------------------------------------------------------------------- #

def outcome_class(row: dict, threshold: float = LOW_STRUCTURAL_F1) -> str:
    """Classify a joined per-diagram row into one of OUTCOME_CLASSES.

    Keyed on ``has_pred`` then render-``compiled`` (CSR), then structural F1 -- so a
    prediction that parses but does not render is a ``compile_fail``, never
    ``compiled_low_structural``."""
    if not row["element"]["has_pred"]:
        return "provider_drop"
    if not row["csr"]["compiled"]:
        return "compile_fail"
    if row["element"]["f1"] < threshold or row["relationship"]["f1"] < threshold:
        return "compiled_low_structural"
    return "ok"


def relation_deltas(by_relation: dict) -> tuple[list[str], list[str]]:
    """(missed, extra) relation types from a per-diagram ``by_relation`` map:
    missed = relations with fn>0 (in GT, absent/wrong in prediction), extra =
    relations with fp>0 (predicted, not in GT). Canonical RELATIONS order."""
    missed = [r for r in RELATIONS if by_relation.get(r, {}).get("fn", 0) > 0]
    extra = [r for r in RELATIONS if by_relation.get(r, {}).get("fp", 0) > 0]
    return missed, extra


# --------------------------------------------------------------------------- #
# selection (seeded, capped, deterministic, per-cell independent)
# --------------------------------------------------------------------------- #

def cell_seed_key(model_id: str, primary_type: str, tier, outcome: str) -> str:
    """Stable per-cell seed string. Depends ONLY on the cell identity, so a cell's
    sample is independent of which other cells/models are present."""
    return f"{SEED}|{model_id}|{primary_type}|{tier}|{outcome}"


def select_cell(rows: list[dict], n: int, seed_key: str, *, seed: int = SEED) -> list[dict]:
    """Deterministically pick up to ``n`` rows from one cell.

    Sorts by ``key`` then applies a seeded shuffle keyed on ``seed_key`` (so re-runs
    are byte-identical and distinct cells draw independently), and returns the first
    ``n``. Tolerates an empty cell and ``n`` larger than the cell."""
    if n <= 0 or not rows:
        return []
    ordered = sorted(rows, key=lambda r: r["key"])
    random.Random(f"{seed}|{seed_key}").shuffle(ordered)
    return ordered[:n]


@dataclass
class Selection:
    """Outcome of stratified sampling over a panel."""
    cases: list[tuple[ModelData, dict, str]]   # (model, per-diagram row, outcome_class)
    cells: list[dict] = field(default_factory=list)   # every non-empty sampled cell (+ caps)


def sample_panel(
    models: list[ModelData],
    *,
    per_cell: int,
    threshold: float = LOW_STRUCTURAL_F1,
    include_ok: bool = False,
    seed: int = SEED,
) -> Selection:
    """Stratify each model's rows by (type, tier, outcome) and pick ``per_cell`` per
    cell over the failure classes (plus ``ok`` when ``include_ok``). Cells are
    visited in a fixed order (registry model order x TYPES x TIERS x class order)
    and empty cells are skipped; a cell larger than the cap is logged."""
    classes = list(FAILURE_CLASSES) + (["ok"] if include_ok else [])
    cases: list[tuple[ModelData, dict, str]] = []
    cells: list[dict] = []

    for md in models:
        mid = md.entry.id
        # bucket this model's rows by (type, tier, outcome) once
        buckets: dict[tuple, list[dict]] = {}
        for row in md.rows:
            oc = outcome_class(row, threshold)
            buckets.setdefault((row["primary_type"], row["tier"], oc), []).append(row)

        for typ in TYPES:
            for tier in TIERS:
                for oc in classes:
                    bucket = buckets.get((typ, tier, oc), [])
                    if not bucket:
                        continue   # empty cell -> skip (logged in aggregate below)
                    picked = select_cell(bucket, per_cell,
                                         cell_seed_key(mid, typ, tier, oc), seed=seed)
                    capped = len(bucket) > len(picked)
                    cells.append({
                        "model_id": mid, "display": md.entry.display,
                        "primary_type": typ, "tier": tier, "outcome_class": oc,
                        "available": len(bucket), "sampled": len(picked), "capped": capped,
                    })
                    if capped:
                        log.info("cap: %s %s tier %s %s -> sampled %d / %d available",
                                 mid, typ, tier, oc, len(picked), len(bucket))
                    for row in picked:
                        cases.append((md, row, oc))

    n_capped = sum(1 for c in cells if c["capped"])
    log.info("sampled %d cases across %d non-empty cells (%d capped) from %d model(s)",
             len(cases), len(cells), n_capped, len(models))
    return Selection(cases=cases, cells=cells)


# --------------------------------------------------------------------------- #
# raw-file plumbing + per-case record
# --------------------------------------------------------------------------- #

def case_paths(run_dir: str, key: str) -> dict[str, str]:
    """Repo-relative paths to the four raw artifacts of one case (verified on disk
    2026-06-15). ``pred_*`` are absent for a provider drop; ``pred_render`` is absent
    whenever the prediction did not compile -- both are themselves signal."""
    return {
        "gt_puml": f"data/puml_files/{key}.puml",
        "pred_puml": f"data/runs/{run_dir}/{key}.puml",
        "input_image": f"data/puml_images_1568/{key}.png",
        "pred_render": f"data/csr/{run_dir}/png/{key}.png",
    }


def _fs_path(data_root: Path, repo_rel: str) -> Path:
    """Resolve a repo-relative ``data/...`` path against ``data_root`` (which already
    points at the ``data/`` directory) by stripping the leading ``data/`` segment."""
    return Path(data_root) / Path(repo_rel).relative_to("data")


def read_snippet(path: Path, max_lines: int = SNIPPET_MAX_LINES) -> dict | None:
    """Read a text file, truncated to ``max_lines``. Returns None if absent (a
    missing prediction is signal, not an error)."""
    if not path.exists():
        return None
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    truncated = len(lines) > max_lines
    text = "\n".join(lines[:max_lines])
    return {"text": text, "n_lines": len(lines), "truncated": truncated}


def build_case_record(
    md: ModelData,
    row: dict,
    outcome: str,
    data_root: str | Path,
    *,
    small_lines: int = SMALL_DIAGRAM_LINES,
    snippet_lines: int = SNIPPET_MAX_LINES,
) -> dict:
    """Assemble one triage record: identity + structural deltas + raw-file paths
    (with existence) + inlined GT/prediction text where it pays."""
    data_root = Path(data_root)
    key = row["key"]
    run_dir = md.entry.run_dir
    paths = case_paths(run_dir, key)
    exists = {name: _fs_path(data_root, rel).exists() for name, rel in paths.items()}

    el = row["element"]
    rel = row["relationship"]
    missed, extra = relation_deltas(rel.get("by_relation", {}))

    # inline GT + prediction text for compile failures (read the syntax error in
    # place) and for small diagrams (cheap, and the whole case fits on screen)
    gt_path = _fs_path(data_root, paths["gt_puml"])
    gt_lines = 0
    if gt_path.exists():
        gt_lines = len(gt_path.read_text(encoding="utf-8", errors="replace").splitlines())
    inline = outcome == "compile_fail" or (0 < gt_lines <= small_lines)
    inlined = {"gt": None, "pred": None}
    if inline:
        inlined["gt"] = read_snippet(gt_path, snippet_lines)
        inlined["pred"] = read_snippet(_fs_path(data_root, paths["pred_puml"]), snippet_lines)

    return {
        "model_id": md.entry.id,
        "display": md.entry.display,
        "run_dir": run_dir,
        "key": key,
        "primary_type": row["primary_type"],
        "tier": row["tier"],
        "outcome_class": outcome,
        "compiled": row["csr"]["compiled"],
        "has_pred": el["has_pred"],
        "csr_error": row["csr"].get("error"),
        "element": {
            "tp": el["tp"], "fp": el["fp"], "fn": el["fn"], "f1": el["f1"],
            "type_accuracy": {
                "matched": el["type_accuracy"]["matched"],
                "correct": el["type_accuracy"]["correct"],
                "excluded": el["type_accuracy"]["excluded"],
            },
        },
        "relationship": {
            "tp": rel["tp"], "fp": rel["fp"], "fn": rel["fn"], "f1": rel["f1"],
            "relations_missed": missed,
            "relations_extra": extra,
            "by_relation": rel.get("by_relation", {}),
        },
        "chrf": row["chrf"]["score"],
        "paths": paths,
        "paths_exist": exists,
        "gt_n_lines": gt_lines,
        "inlined": inlined,
    }


# --------------------------------------------------------------------------- #
# index assembly (records + meta)
# --------------------------------------------------------------------------- #

def build_index(
    models: list[ModelData],
    *,
    models_total: int,
    pending_ids: list[str],
    refused_ids: list[str] | None = None,
    data_root: str | Path,
    per_cell: int,
    threshold: float = LOW_STRUCTURAL_F1,
    include_ok: bool = False,
    seed: int = SEED,
    small_lines: int = SMALL_DIAGRAM_LINES,
    snippet_lines: int = SNIPPET_MAX_LINES,
    label: str = "main",
) -> tuple[list[dict], dict]:
    """Sample the panel and build (records, meta). ``records`` are key-sorted within
    each (model, outcome) for a stable, idempotent index."""
    selection = sample_panel(models, per_cell=per_cell, threshold=threshold,
                             include_ok=include_ok, seed=seed)
    records = [build_case_record(md, row, oc, data_root,
                                 small_lines=small_lines, snippet_lines=snippet_lines)
               for md, row, oc in selection.cases]
    # stable order: model (registry order) -> outcome (class order) -> key
    model_order = {m.entry.id: i for i, m in enumerate(models)}
    class_order = {c: i for i, c in enumerate(OUTCOME_CLASSES)}
    records.sort(key=lambda r: (model_order[r["model_id"]],
                                class_order[r["outcome_class"]], r["key"]))

    classes_sampled = list(FAILURE_CLASSES) + (["ok"] if include_ok else [])
    # per (model, outcome) availability vs sampled, for the summary table
    summary: dict[str, dict[str, dict[str, int]]] = {}
    for c in selection.cells:
        slot = summary.setdefault(c["model_id"], {})
        agg = slot.setdefault(c["outcome_class"], {"available": 0, "sampled": 0})
        agg["available"] += c["available"]
        agg["sampled"] += c["sampled"]

    meta = {
        "label": label,
        "seed": seed,
        "per_cell": per_cell,
        "low_structural_threshold": threshold,
        "small_diagram_lines": small_lines,
        "snippet_max_lines": snippet_lines,
        "include_ok": include_ok,
        "outcome_classes_sampled": classes_sampled,
        "stratification": "model x primary_type x tier x outcome_class",
        "models_included": len(models),
        "models_total": models_total,
        "included_ids": [m.entry.id for m in models],
        "pending_ids": list(pending_ids),
        "refused_ids": list(refused_ids or []),
        "total_cases": len(records),
        "cell_summary": summary,
        "capped_cells": [c for c in selection.cells if c["capped"]],
    }
    return records, meta


# --------------------------------------------------------------------------- #
# emitters: markdown (human triage) + CSV (flat) + JSON (machine)
# --------------------------------------------------------------------------- #

CSV_FIELDS = [
    "model_id", "display", "key", "primary_type", "tier", "outcome_class",
    "compiled", "has_pred", "csr_error",
    "el_tp", "el_fp", "el_fn", "el_f1", "ta_matched", "ta_correct", "ta_excluded",
    "rel_tp", "rel_fp", "rel_fn", "rel_f1", "relations_missed", "relations_extra",
    "chrf", "gt_puml", "pred_puml", "pred_puml_exists",
    "input_image", "pred_render", "pred_render_exists",
]


def case_csv_rows(records: list[dict]) -> list[dict]:
    rows = []
    for r in records:
        el, rel = r["element"], r["relationship"]
        rows.append({
            "model_id": r["model_id"], "display": r["display"], "key": r["key"],
            "primary_type": r["primary_type"], "tier": r["tier"],
            "outcome_class": r["outcome_class"], "compiled": r["compiled"],
            "has_pred": r["has_pred"], "csr_error": r["csr_error"] or "",
            "el_tp": el["tp"], "el_fp": el["fp"], "el_fn": el["fn"],
            "el_f1": f"{el['f1']:.4f}",
            "ta_matched": el["type_accuracy"]["matched"],
            "ta_correct": el["type_accuracy"]["correct"],
            "ta_excluded": el["type_accuracy"]["excluded"],
            "rel_tp": rel["tp"], "rel_fp": rel["fp"], "rel_fn": rel["fn"],
            "rel_f1": f"{rel['f1']:.4f}",
            "relations_missed": ";".join(rel["relations_missed"]),
            "relations_extra": ";".join(rel["relations_extra"]),
            "chrf": "" if r["chrf"] is None else f"{r['chrf']:.2f}",
            "gt_puml": r["paths"]["gt_puml"],
            "pred_puml": r["paths"]["pred_puml"],
            "pred_puml_exists": r["paths_exist"]["pred_puml"],
            "input_image": r["paths"]["input_image"],
            "pred_render": r["paths"]["pred_render"],
            "pred_render_exists": r["paths_exist"]["pred_render"],
        })
    return rows


def _exist_mark(ok: bool) -> str:
    return "yes" if ok else "MISSING"


def _case_md(r: dict) -> list[str]:
    el, rel = r["element"], r["relationship"]
    out = [f"#### `{r['key']}` — {r['outcome_class']} ({r['primary_type']}, tier {r['tier']})", ""]
    if r["csr_error"]:
        out.append(f"- CSR: `{r['csr_error']}`")
    out.append(f"- Element: tp={el['tp']} fp={el['fp']} fn={el['fn']} F1={el['f1']:.3f}; "
               f"type-acc matched={el['type_accuracy']['matched']} "
               f"correct={el['type_accuracy']['correct']} "
               f"excluded={el['type_accuracy']['excluded']}")
    rel_line = (f"- Relationship: tp={rel['tp']} fp={rel['fp']} fn={rel['fn']} "
                f"F1={rel['f1']:.3f}")
    if rel["relations_missed"]:
        rel_line += f"; missed: {', '.join(rel['relations_missed'])}"
    if rel["relations_extra"]:
        rel_line += f"; extra: {', '.join(rel['relations_extra'])}"
    out.append(rel_line)
    chrf_txt = "—" if r["chrf"] is None else f"{r['chrf']:.2f}"
    out.append(f"- chrF++: {chrf_txt}")
    out.append(f"- Files: GT `{r['paths']['gt_puml']}` ({_exist_mark(r['paths_exist']['gt_puml'])}) "
               f"· pred `{r['paths']['pred_puml']}` ({_exist_mark(r['paths_exist']['pred_puml'])}) "
               f"· input `{r['paths']['input_image']}` ({_exist_mark(r['paths_exist']['input_image'])}) "
               f"· render `{r['paths']['pred_render']}` ({_exist_mark(r['paths_exist']['pred_render'])})")
    out.append("")
    gt, pred = r["inlined"]["gt"], r["inlined"]["pred"]
    if gt is not None:
        out.append(f"GT PlantUML{' (truncated)' if gt['truncated'] else ''}:")
        out.append("```plantuml")
        out.append(gt["text"])
        out.append("```")
        out.append("")
        if pred is not None:
            out.append(f"Prediction PlantUML{' (truncated)' if pred['truncated'] else ''}:")
            out.append("```plantuml")
            out.append(pred["text"])
            out.append("```")
        else:
            out.append("_Prediction: no file on disk (provider/harness drop)._")
        out.append("")
    return out


def render_markdown(records: list[dict], meta: dict) -> str:
    out: list[str] = []
    out.append("# Failure-case index — zero-shot image→PlantUML benchmark")
    out.append("")
    out.append(f"**Models included: {meta['models_included']}/{meta['models_total']}** "
               f"(panel label: {meta['label']}) — {meta['total_cases']} sampled cases.")
    out.append("")
    if meta["pending_ids"]:
        out.append("Pending / not yet scored: " + ", ".join(meta["pending_ids"]))
        out.append("")
    if meta["refused_ids"]:
        out.append("Refused (reasoning leak): " + ", ".join(meta["refused_ids"]))
        out.append("")
    out.append(
        f"Stratified sample of failures: up to **{meta['per_cell']} case(s) per "
        f"(model × diagram type × tier × outcome class)** over the failure classes "
        f"{', '.join(f'`{c}`' for c in meta['outcome_classes_sampled'])}. "
        f"`compiled_low_structural` = rendered but Element or Relationship F1 < "
        f"{meta['low_structural_threshold']}. Selection is a seeded shuffle "
        f"(seed={meta['seed']}) over key-sorted rows — deterministic and per-cell "
        f"independent. A missing prediction/render file is itself signal (a provider "
        f"drop or a non-rendering prediction).")
    out.append("")

    # per-(model, outcome) availability vs sampled
    out.append("## Coverage (available → sampled)")
    out.append("")
    out.append("| Model | " + " | ".join(meta["outcome_classes_sampled"]) + " |")
    out.append("|---|" + "---|" * len(meta["outcome_classes_sampled"]))
    for mid in meta["included_ids"]:
        slot = meta["cell_summary"].get(mid, {})
        cells = []
        for oc in meta["outcome_classes_sampled"]:
            v = slot.get(oc)
            cells.append(f"{v['available']}→{v['sampled']}" if v else "—")
        disp = next((r["display"] for r in records if r["model_id"] == mid), mid)
        out.append(f"| {disp} | " + " | ".join(cells) + " |")
    out.append("")
    if meta["capped_cells"]:
        out.append(f"_{len(meta['capped_cells'])} cell(s) capped at {meta['per_cell']} "
                   f"(full list in the JSON `capped_cells`) — the sample is a subset of "
                   f"those cells, not the complete failure set._")
        out.append("")

    # detail, grouped by model then outcome class (records are pre-sorted)
    out.append("## Cases")
    out.append("")
    cur_model = cur_outcome = None
    for r in records:
        if r["model_id"] != cur_model:
            cur_model, cur_outcome = r["model_id"], None
            out.append(f"### {r['display']}")
            out.append("")
        if r["outcome_class"] != cur_outcome:
            cur_outcome = r["outcome_class"]
            out.append(f"#### outcome: {cur_outcome}")
            out.append("")
        out += _case_md(r)
    return "\n".join(out) + "\n"


def write_index(records: list[dict], meta: dict, out_dir: str | Path,
                basename: str = "failure_index") -> dict:
    """Write JSON + markdown + CSV under ``out_dir``; return {kind: Path}.
    Deterministic (sorted records, no timestamps)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{basename}.json",
        "md": out_dir / f"{basename}.md",
        "csv": out_dir / f"{basename}.csv",
    }
    paths["json"].write_text(
        json.dumps({"meta": meta, "cases": records}, indent=2) + "\n", encoding="utf-8")
    paths["md"].write_text(render_markdown(records, meta), encoding="utf-8")
    with open(paths["csv"], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(case_csv_rows(records))
    return paths
