"""Tests for the per-model loader: strip-.puml join + clean skip of pending runs."""
import json
from pathlib import Path

import pytest

from analysis.loader import load_model, load_panel, load_test_set_index, strip_puml
from analysis.registry import ModelEntry


def _entry(run_dir, status="scored", supplementary=False, mid="m"):
    return ModelEntry(
        id=mid, display=mid, run_dir=run_dir, status=status, lab="qwen",
        arm="qwen", family="dense", params_total_b=1, params_active_b=1,
        supplementary=supplementary,
    )


def _f1(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return p, r, f


def write_run(data_root: Path, run_dir: str, diagrams: list[dict]):
    """Write test_set.json (once) + the 4 metric JSONs for one run under data_root.

    Each diagram spec: {key, type, tier, compiled, el:(tp,fp,fn), rel:(tp,fp,fn),
    chrf, ta:(matched,correct,excluded), has_pred}.  test_set keys get a .puml
    suffix; metric keys stay bare (mirrors the real layout).
    """
    data_root = Path(data_root)
    # test_set.json (shared; write if absent)
    ts_path = data_root / "test_set.json"
    if not ts_path.exists():
        ts = {"count": len(diagrams), "diagrams": [
            {"key": d["key"] + ".puml", "blob_id": d["key"].split("_")[0],
             "primary_type": d["type"], "tier": d["tier"], "content_lines": 5}
            for d in diagrams
        ]}
        ts_path.parent.mkdir(parents=True, exist_ok=True)
        ts_path.write_text(json.dumps(ts))

    def per_diag_f1(spec, which):
        tp, fp, fn = spec[which]
        p, r, f = _f1(tp, fp, fn)
        row = {"key": spec["key"], "tp": tp, "fp": fp, "fn": fn,
               "precision": p, "recall": r, "f1": f,
               "has_pred": spec.get("has_pred", True), "compiled": spec["compiled"]}
        return row

    # csr
    csr_rows = [{"key": d["key"], "compiled": d["compiled"], "n_png": 1 if d["compiled"] else 0,
                 "png_bytes": 999 if d["compiled"] else 0,
                 "error": None if d["compiled"] else "no PNG produced"} for d in diagrams]
    n = len(diagrams)
    ncomp = sum(1 for d in diagrams if d["compiled"])
    _dump(data_root / "csr" / run_dir / "csr_results.json",
          {"summary": {"pred_dir": f"data/runs/{run_dir}", "n": n, "compiled": ncomp,
                       "csr": ncomp / n, "min_png_bytes": 256}, "diagrams": csr_rows})

    # element_f1 (+ type_accuracy on per-diagram)
    el_rows = []
    for d in diagrams:
        row = per_diag_f1(d, "el")
        m, c, x = d.get("ta", (0, 0, 0))
        row["type_accuracy"] = {"matched": m, "correct": c, "excluded": x}
        el_rows.append(row)
    _dump(data_root / "element_f1" / run_dir / "element_f1_results.json",
          {"summary": {"zeros_for_failed": {}, "compiled_only": {}, "type_accuracy": {}},
           "diagrams": el_rows})

    # relationship_f1
    rel_rows = [per_diag_f1(d, "rel") for d in diagrams]
    _dump(data_root / "relationship_f1" / run_dir / "relationship_f1_results.json",
          {"summary": {"zeros_for_failed": {}, "compiled_only": {}}, "diagrams": rel_rows})

    # chrf
    chrf_rows = [{"key": d["key"], "has_pred": d.get("has_pred", True),
                  "compiled": d["compiled"], "score": d.get("chrf", 0.0)} for d in diagrams]
    _dump(data_root / "chrf" / run_dir / "chrf_results.json",
          {"summary": {"scale": "0-100", "params": {}, "zeros_for_failed": {}, "compiled_only": {}},
           "diagrams": chrf_rows})


def _dump(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj))


DIAGS = [
    {"key": "aaa", "type": "class", "tier": 1, "compiled": True,
     "el": (3, 1, 0), "rel": (2, 0, 1), "chrf": 70.0, "ta": (3, 3, 0)},
    {"key": "bbb_01", "type": "sequence", "tier": 2, "compiled": False,
     "el": (0, 0, 4), "rel": (0, 0, 2), "chrf": 0.0, "ta": (0, 0, 0)},
]


def test_strip_puml():
    assert strip_puml("abc.puml") == "abc"
    assert strip_puml("abc_01.puml") == "abc_01"  # split-file suffix preserved
    assert strip_puml("abc") == "abc"


def test_join_attaches_type_and_tier_including_split_key(tmp_path):
    write_run(tmp_path, "run1", DIAGS)
    md = load_model(_entry("run1"), data_root=tmp_path)
    assert md is not None
    rows = {r["key"]: r for r in md.rows}
    assert set(rows) == {"aaa", "bbb_01"}
    assert rows["aaa"]["primary_type"] == "class" and rows["aaa"]["tier"] == 1
    # the split-file key only joins because .puml was stripped from the test_set key
    assert rows["bbb_01"]["primary_type"] == "sequence" and rows["bbb_01"]["tier"] == 2
    # metric sub-blocks present and carry tp/fp/fn
    assert rows["aaa"]["element"]["tp"] == 3
    assert rows["bbb_01"]["relationship"]["fn"] == 2
    assert rows["aaa"]["chrf"]["score"] == 70.0
    assert rows["bbb_01"]["csr"]["compiled"] is False


def test_summaries_loaded_for_readthrough(tmp_path):
    write_run(tmp_path, "run1", DIAGS)
    md = load_model(_entry("run1"), data_root=tmp_path)
    assert set(md.summaries) == {"csr", "element_f1", "relationship_f1", "chrf"}
    assert md.summaries["csr"]["n"] == 2


def test_pending_entry_skipped_returns_none(tmp_path):
    write_run(tmp_path, "run1", DIAGS)  # test_set exists, but entry has no run_dir
    assert load_model(_entry(None, status="pending"), data_root=tmp_path) is None


def test_missing_metric_dir_skipped_returns_none(tmp_path):
    write_run(tmp_path, "run1", DIAGS)
    assert load_model(_entry("does-not-exist"), data_root=tmp_path) is None


def test_partial_run_missing_one_metric_skipped(tmp_path):
    write_run(tmp_path, "run1", DIAGS)
    # delete one of the four metric files -> incomplete -> skip, not crash
    (tmp_path / "chrf" / "run1" / "chrf_results.json").unlink()
    assert load_model(_entry("run1"), data_root=tmp_path) is None


def test_key_mismatch_raises(tmp_path):
    write_run(tmp_path, "run1", DIAGS)
    # corrupt the element metric to drop a key -> schema surprise -> STOP (raise)
    p = tmp_path / "element_f1" / "run1" / "element_f1_results.json"
    obj = json.loads(p.read_text())
    obj["diagrams"] = obj["diagrams"][:1]
    p.write_text(json.dumps(obj))
    with pytest.raises(ValueError):
        load_model(_entry("run1"), data_root=tmp_path)


def test_load_panel_skips_pending_keeps_scored(tmp_path):
    write_run(tmp_path, "run1", DIAGS)
    reg = [_entry("run1", mid="scored1"),
           _entry(None, status="pending", mid="pend1"),
           _entry("missing", mid="miss1")]
    loaded = load_panel(reg, data_root=tmp_path)
    assert [md.entry.id for md in loaded] == ["scored1"]


def test_load_test_set_index_strips_puml(tmp_path):
    write_run(tmp_path, "run1", DIAGS)
    idx = load_test_set_index(tmp_path / "test_set.json")
    assert set(idx) == {"aaa", "bbb_01"}
    assert idx["aaa"]["primary_type"] == "class"
    assert idx["bbb_01"]["tier"] == 2
