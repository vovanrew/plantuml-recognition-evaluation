"""Unit + smoke tests for the Task-4 failure-case sampler (analysis/failure_sampler.py).

"Tests where they pay" (per the task acceptance):

* **outcome_class(row)** — the four-class classifier, including the render≠parse
  edge (a prediction that structurally parses yet does not render is still a
  ``compile_fail``, not ``compiled_low_structural``) and the threshold boundary.
* **select_cell(...)** — the seeded, stratified selector: deterministic subset,
  respects the per-cell cap, tolerates an empty cell, draws a subset of its input,
  and is per-cell independent (incrementality: a new model never shifts another
  model's sample).
* **relation_deltas / case_paths / build_case_record** — the structural-delta and
  raw-file plumbing each sampled case must carry.
* **emitter smoke** — write_index writes non-empty md + csv + json with an N/total
  header.

Pure helpers run on tiny synthetic rows (tests/synth.make_row); the record/emitter
tests stage a couple of files under a tmp data root.
"""
from __future__ import annotations

import json

import pytest

from analysis.loader import ModelData
from analysis.registry import ModelEntry
from tests.synth import make_row, synth_model

from analysis import failure_sampler as fs


# --------------------------------------------------------------------------- #
# outcome_class — the four classes + the two edges
# --------------------------------------------------------------------------- #

def test_outcome_class_provider_drop():
    row = make_row("d", "class", 1, compiled=False, el=(0, 0, 2), rel=(0, 0, 0),
                   chrf=0.0, ta=(0, 0, 0), has_pred=False,
                   csr_error="no prediction (missing/timeout)")
    assert fs.outcome_class(row) == "provider_drop"


def test_outcome_class_compile_fail():
    row = make_row("d", "class", 1, compiled=False, el=(0, 0, 2), rel=(0, 0, 1),
                   chrf=5.0, ta=(0, 0, 0), has_pred=True,
                   csr_error="Error line 19 in file: x.puml")
    assert fs.outcome_class(row) == "compile_fail"


def test_outcome_class_compile_fail_render_not_parse_edge():
    """A prediction that structurally parses (matched/tp > 0) yet fails to render
    (compiled=False) is a compile_fail, NOT compiled_low_structural — the Qwen-2B
    edge the plan flags. Classification keys on has_pred then compiled (render)."""
    row = make_row("d", "class", 1, compiled=False, el=(7, 0, 0), rel=(0, 0, 0),
                   chrf=40.0, ta=(7, 7, 0), has_pred=True,
                   csr_error="Error line 3 in file: x.puml")
    # element f1 is high (perfect) AND it parsed, but it never rendered:
    assert row["element"]["f1"] == pytest.approx(1.0)
    assert fs.outcome_class(row) == "compile_fail"


def test_outcome_class_low_via_element():
    row = make_row("d", "class", 1, compiled=True, el=(0, 3, 3), rel=(0, 0, 0),
                   chrf=50.0, ta=(0, 0, 0))
    assert row["element"]["f1"] < 0.5
    assert fs.outcome_class(row) == "compiled_low_structural"


def test_outcome_class_low_via_relationship_only():
    row = make_row("d", "class", 1, compiled=True, el=(5, 0, 0), rel=(0, 2, 2),
                   chrf=50.0, ta=(5, 5, 0))
    assert row["element"]["f1"] == pytest.approx(1.0)
    assert row["relationship"]["f1"] < 0.5
    assert fs.outcome_class(row) == "compiled_low_structural"


def test_outcome_class_ok():
    row = make_row("d", "class", 1, compiled=True, el=(5, 0, 0), rel=(3, 0, 0),
                   chrf=80.0, ta=(5, 5, 0))
    assert fs.outcome_class(row) == "ok"


def test_outcome_class_threshold_boundary_is_ok():
    """f1 exactly at the threshold is NOT a failure (the cut is strictly below)."""
    row = make_row("d", "class", 1, compiled=True, el=(1, 1, 1), rel=(1, 1, 1),
                   chrf=50.0, ta=(1, 1, 0))
    assert row["element"]["f1"] == pytest.approx(0.5)
    assert fs.outcome_class(row, threshold=0.5) == "ok"


def test_outcome_class_threshold_is_parameterised():
    row = make_row("d", "class", 1, compiled=True, el=(3, 1, 1), rel=(3, 0, 0),
                   chrf=70.0, ta=(3, 3, 0))
    assert 0.5 < row["element"]["f1"] < 0.9
    assert fs.outcome_class(row, threshold=0.5) == "ok"
    assert fs.outcome_class(row, threshold=0.9) == "compiled_low_structural"


# --------------------------------------------------------------------------- #
# relation_deltas — which relations were missed (fn>0) / extra (fp>0)
# --------------------------------------------------------------------------- #

def test_relation_deltas_missed_and_extra():
    by_rel = {r: {"tp": 0, "fp": 0, "fn": 0} for r in fs.RELATIONS}
    by_rel["message"] = {"tp": 1, "fp": 0, "fn": 2}      # missed messages
    by_rel["inheritance"] = {"tp": 0, "fp": 3, "fn": 0}  # spurious inheritance
    missed, extra = fs.relation_deltas(by_rel)
    assert missed == ["message"]
    assert extra == ["inheritance"]


def test_relation_deltas_orders_by_relation_vocab():
    by_rel = {r: {"tp": 0, "fp": 1, "fn": 1} for r in fs.RELATIONS}
    missed, extra = fs.relation_deltas(by_rel)
    assert missed == fs.RELATIONS         # all six, in canonical order
    assert extra == fs.RELATIONS


def test_relation_deltas_empty():
    by_rel = {r: {"tp": 0, "fp": 0, "fn": 0} for r in fs.RELATIONS}
    assert fs.relation_deltas(by_rel) == ([], [])


# --------------------------------------------------------------------------- #
# select_cell — seeded, capped, deterministic, per-cell independent
# --------------------------------------------------------------------------- #

def _rows(n):
    return [make_row(f"k{i:02d}", "class", 1, True, (1, 0, 0), (1, 0, 0), 50.0, (1, 1, 0))
            for i in range(n)]


def test_select_cell_deterministic():
    rows = _rows(10)
    a = fs.select_cell(rows, 3, "gpt|class|1|compile_fail")
    b = fs.select_cell(rows, 3, "gpt|class|1|compile_fail")
    assert [r["key"] for r in a] == [r["key"] for r in b]


def test_select_cell_respects_cap():
    rows = _rows(10)
    assert len(fs.select_cell(rows, 3, "k")) == 3
    assert len(fs.select_cell(rows, 99, "k")) == 10   # n > available -> all
    assert fs.select_cell(rows, 0, "k") == []


def test_select_cell_empty_cell():
    assert fs.select_cell([], 3, "k") == []


def test_select_cell_returns_subset_of_input():
    rows = _rows(10)
    picked = fs.select_cell(rows, 4, "k")
    keys = {r["key"] for r in rows}
    assert all(r["key"] in keys for r in picked)
    assert len({r["key"] for r in picked}) == 4   # no duplicates


def test_select_cell_per_cell_independent():
    """Different seed keys draw independently (so distinct cells don't correlate)."""
    rows = _rows(10)
    a = [r["key"] for r in fs.select_cell(rows, 10, "cellA")]
    b = [r["key"] for r in fs.select_cell(rows, 10, "cellB")]
    assert a != b   # 1/10! chance of collision -> effectively never


# --------------------------------------------------------------------------- #
# sample_panel — stratify by (model x type x tier x outcome), cap, skip empty
# --------------------------------------------------------------------------- #

def test_sample_panel_only_failure_classes_by_default():
    sel = fs.sample_panel([synth_model("m1")], per_cell=5)
    outcomes = {o for _, _, o in sel.cases}
    assert "ok" not in outcomes
    assert outcomes <= set(fs.FAILURE_CLASSES)


def test_sample_panel_include_ok():
    sel = fs.sample_panel([synth_model("m1")], per_cell=5, include_ok=True)
    outcomes = {o for _, _, o in sel.cases}
    assert "ok" in outcomes


def test_sample_panel_caps_and_logs():
    # one model, many compile-fail rows in a single (type,tier) cell -> capped
    rows = [make_row(f"k{i:02d}", "class", 1, False, (0, 0, 1), (0, 0, 0), 0.0, (0, 0, 0),
                     has_pred=True, csr_error="Error line 1 in file: x")
            for i in range(8)]
    md = ModelData(entry=synth_model("m1").entry, rows=rows, summaries=synth_model("m1").summaries)
    sel = fs.sample_panel([md], per_cell=3)
    assert len([c for c in sel.cases if c[2] == "compile_fail"]) == 3
    capped = [c for c in sel.cells if c["capped"]]
    assert capped and capped[0]["available"] == 8 and capped[0]["sampled"] == 3


def test_sample_panel_incremental_stable_when_model_added():
    """Adding a second model must not change the first model's selected cases
    (per-cell independent seeding -> idempotent incremental re-runs)."""
    a = synth_model("m1")
    b = synth_model("m2", "M2")
    only_a = fs.sample_panel([a], per_cell=1)
    a_with_b = fs.sample_panel([a, b], per_cell=1)
    ka = [(m.entry.id, r["key"], o) for m, r, o in only_a.cases]
    kab = [(m.entry.id, r["key"], o) for m, r, o in a_with_b.cases if m.entry.id == "m1"]
    assert ka == kab


# --------------------------------------------------------------------------- #
# case_paths + build_case_record — raw-file plumbing & structural deltas
# --------------------------------------------------------------------------- #

def test_case_paths_repo_relative():
    p = fs.case_paths("run-x", "abc")
    assert p["gt_puml"] == "data/puml_files/abc.puml"
    assert p["pred_puml"] == "data/runs/run-x/abc.puml"
    assert p["input_image"] == "data/puml_images_1568/abc.png"
    assert p["pred_render"] == "data/csr/run-x/png/abc.png"


def _stage(data_root, run_dir, key, *, gt=None, pred=None, render=False):
    (data_root / "puml_files").mkdir(parents=True, exist_ok=True)
    if gt is not None:
        (data_root / "puml_files" / f"{key}.puml").write_text(gt, encoding="utf-8")
    if pred is not None:
        (data_root / "runs" / run_dir).mkdir(parents=True, exist_ok=True)
        (data_root / "runs" / run_dir / f"{key}.puml").write_text(pred, encoding="utf-8")
    if render:
        (data_root / "csr" / run_dir / "png").mkdir(parents=True, exist_ok=True)
        (data_root / "csr" / run_dir / "png" / f"{key}.png").write_bytes(b"\x89PNG")


def test_build_case_record_compile_fail(tmp_path):
    key = "d2"
    row = make_row(key, "class", 2, compiled=False, el=(0, 1, 3), rel=(0, 0, 1),
                   chrf=5.0, ta=(0, 0, 0), rel_type="message", has_pred=True,
                   csr_error="Error line 7 in file: d2.puml")
    md = ModelData(entry=synth_model("m1").entry, rows=[row],
                   summaries=synth_model("m1").summaries)
    _stage(tmp_path, "r", key, gt="@startuml\nclass A\n@enduml",
           pred="@startuml\nclas A\n@enduml")   # typo -> compile fail, no render

    rec = fs.build_case_record(md, row, "compile_fail", tmp_path)
    assert rec["key"] == key and rec["outcome_class"] == "compile_fail"
    assert rec["csr_error"] == "Error line 7 in file: d2.puml"
    assert rec["element"] == {"tp": 0, "fp": 1, "fn": 3, "f1": pytest.approx(0.0),
                              "type_accuracy": {"matched": 0, "correct": 0, "excluded": 0}}
    assert rec["relationship"]["relations_missed"] == ["message"]   # fn=1 on message
    assert rec["relationship"]["relations_extra"] == []
    # paths recorded + existence: gt & pred present, render absent (didn't render)
    assert rec["paths"]["gt_puml"] == "data/puml_files/d2.puml"
    assert rec["paths_exist"]["gt_puml"] is True
    assert rec["paths_exist"]["pred_puml"] is True
    assert rec["paths_exist"]["pred_render"] is False
    # compile_fail inlines GT + prediction text so the syntax error is readable in place
    assert "class A" in rec["inlined"]["gt"]["text"]
    assert "clas A" in rec["inlined"]["pred"]["text"]


def test_build_case_record_provider_drop_has_no_pred_file(tmp_path):
    key = "d9"
    row = make_row(key, "sequence", 1, compiled=False, el=(0, 0, 1), rel=(0, 0, 0),
                   chrf=0.0, ta=(0, 0, 0), has_pred=False,
                   csr_error="no prediction (missing/timeout)")
    md = ModelData(entry=synth_model("m1").entry, rows=[row],
                   summaries=synth_model("m1").summaries)
    _stage(tmp_path, "r", key, gt="@startuml\nAlice -> Bob\n@enduml")  # GT only, no pred

    rec = fs.build_case_record(md, row, "provider_drop", tmp_path)
    assert rec["has_pred"] is False
    assert rec["paths_exist"]["pred_puml"] is False
    assert rec["paths_exist"]["pred_render"] is False
    assert rec["inlined"]["pred"] is None   # nothing to inline


# --------------------------------------------------------------------------- #
# emitter smoke — non-empty md + csv + json with an N/total header
# --------------------------------------------------------------------------- #

def test_build_index_and_write(tmp_path):
    models = [synth_model("m1"), synth_model("m2", "M2")]
    records, meta = fs.build_index(
        models, models_total=7, pending_ids=["gemini-3.1-pro"], refused_ids=[],
        data_root=tmp_path, per_cell=2)
    assert meta["models_included"] == 2 and meta["models_total"] == 7
    assert meta["seed"] == fs.SEED
    assert records  # some failure cases sampled from the synth rows

    paths = fs.write_index(records, meta, tmp_path)
    for kind in ("md", "csv", "json"):
        assert paths[kind].exists() and paths[kind].stat().st_size > 0
    doc = json.loads(paths["json"].read_text())
    assert doc["meta"]["models_included"] == 2
    assert len(doc["cases"]) == len(records)
    md = paths["md"].read_text()
    assert "2/7" in md   # N/total header so a partial index is never mistaken for final
    # CSV has a header + one row per case
    csv_lines = paths["csv"].read_text().strip().splitlines()
    assert len(csv_lines) == 1 + len(records)


def test_write_index_idempotent(tmp_path):
    models = [synth_model("m1")]
    records, meta = fs.build_index(models, models_total=7, pending_ids=[], refused_ids=[],
                                   data_root=tmp_path, per_cell=2)
    p1 = fs.write_index(records, meta, tmp_path / "a")
    p2 = fs.write_index(records, meta, tmp_path / "b")
    for kind in ("md", "csv", "json"):
        assert p1[kind].read_bytes() == p2[kind].read_bytes()
