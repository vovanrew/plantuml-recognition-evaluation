"""Integration: the master table must reproduce the four scored runner summaries
exactly (the analysis-protocol validation gate). Skips cleanly when run data is absent
(data/csr, data/element_f1, data/relationship_f1 are gitignored)."""
import json

import pytest

from analysis.build_master_table import aggregate_panel
from analysis.loader import DEFAULT_DATA_ROOT
from analysis.registry import load_registry, panel_entries
from analysis.report import write_table

DATA = DEFAULT_DATA_ROOT
SCORED = ["gpt-5.2", "claude-opus-4-6", "gemini-3.1-pro", "qwen3.5-2b", "qwen3.5-9b",
          "qwen3.5-27b", "qwen3.5-397b-a17b"]

# Human-readable anchor table from the analysis protocol (micro; zeros / compiled).
ANCHORS = {
    "gpt-5.2":           {"csr": 0.935, "el": (0.897, 0.939), "rel": (0.757, 0.799), "chrf": (60.74, 66.01), "ta": 0.941},
    "claude-opus-4-6":   {"csr": 0.941, "el": (0.909, 0.940), "rel": (0.693, 0.720), "chrf": (62.36, 66.57), "ta": 0.950},
    "gemini-3.1-pro":    {"csr": 0.972, "el": (0.945, 0.961), "rel": (0.875, 0.893), "chrf": (72.19, 74.54), "ta": 0.984},
    "qwen3.5-2b":        {"csr": 0.201, "el": (0.246, 0.878), "rel": (0.114, 0.481), "chrf": (8.96, 65.12),  "ta": 0.758},
    "qwen3.5-9b":        {"csr": 0.431, "el": (0.491, 0.844), "rel": (0.201, 0.439), "chrf": (24.40, 61.17), "ta": 0.756},
    "qwen3.5-27b":       {"csr": 0.601, "el": (0.676, 0.917), "rel": (0.485, 0.722), "chrf": (38.41, 65.65), "ta": 0.886},
    "qwen3.5-397b-a17b": {"csr": 0.787, "el": (0.771, 0.897), "rel": (0.646, 0.736), "chrf": (47.80, 59.77), "ta": 0.870},
}

_REG = {e.id: e for e in load_registry()}


def _have_data():
    for mid in SCORED:
        rd = _REG[mid].run_dir
        if not rd or not (DATA / "element_f1" / rd / "element_f1_results.json").exists():
            return False
    return True


pytestmark = pytest.mark.skipif(not _have_data(), reason="scored run data not on disk")


def _summary(metric, mid):
    rd = _REG[mid].run_dir
    p = DATA / metric / rd / f"{metric}_results.json"
    return json.loads(p.read_text())["summary"]


def _main_table():
    return aggregate_panel(panel_entries(load_registry()), DATA, label="main")


def test_reproduces_stored_summaries_exactly():
    table = _main_table()
    EXACT = 1e-9
    for mid in SCORED:
        ov = table["models"][mid]["overall"]
        el_s = _summary("element_f1", mid)
        rel_s = _summary("relationship_f1", mid)
        chrf_s = _summary("chrf", mid)
        csr_s = _summary("csr", mid)

        assert ov["csr"]["csr"] == pytest.approx(csr_s["csr"], abs=EXACT), mid
        for pop in ("zeros_for_failed", "compiled_only"):
            for level in ("micro", "macro"):
                for comp in ("precision", "recall", "f1"):
                    assert ov["element_f1"][pop][level][comp] == pytest.approx(
                        el_s[pop][level][comp], abs=EXACT), (mid, "element", pop, level, comp)
                    assert ov["relationship_f1"][pop][level][comp] == pytest.approx(
                        rel_s[pop]["all"][level][comp], abs=EXACT), (mid, "rel", pop, level, comp)
            # chrf macro is pooled (must reproduce); micro is read-through (equal by construction)
            assert ov["chrf"][pop]["macro"] == pytest.approx(chrf_s[pop]["macro"], abs=EXACT), (mid, pop)
            assert ov["chrf"][pop]["micro"] == pytest.approx(chrf_s[pop]["micro"], abs=EXACT), (mid, pop)
        # type accuracy
        assert ov["type_accuracy"]["accuracy"] == pytest.approx(
            el_s["type_accuracy"]["accuracy"], abs=EXACT), mid


def test_per_relation_readthrough_matches_summary():
    table = _main_table()
    for mid in SCORED:
        pr = table["models"][mid]["per_relation"]
        rel_s = _summary("relationship_f1", mid)
        for pop in ("zeros_for_failed", "compiled_only"):
            for rel, v in rel_s[pop]["by_relation"].items():
                assert pr[pop][rel]["f1"] == pytest.approx(v["f1"], abs=1e-9), (mid, pop, rel)
                assert pr[pop][rel]["support_gt"] == v["support_gt"]


def test_matches_human_anchor_table():
    table = _main_table()
    for mid, a in ANCHORS.items():
        ov = table["models"][mid]["overall"]
        assert ov["csr"]["csr"] == pytest.approx(a["csr"], abs=1e-3), mid
        assert ov["element_f1"]["zeros_for_failed"]["micro"]["f1"] == pytest.approx(a["el"][0], abs=1e-3), mid
        assert ov["element_f1"]["compiled_only"]["micro"]["f1"] == pytest.approx(a["el"][1], abs=1e-3), mid
        assert ov["relationship_f1"]["zeros_for_failed"]["micro"]["f1"] == pytest.approx(a["rel"][0], abs=1e-3), mid
        assert ov["relationship_f1"]["compiled_only"]["micro"]["f1"] == pytest.approx(a["rel"][1], abs=1e-3), mid
        assert ov["chrf"]["zeros_for_failed"]["micro"] == pytest.approx(a["chrf"][0], abs=1e-2), mid
        assert ov["chrf"]["compiled_only"]["micro"] == pytest.approx(a["chrf"][1], abs=1e-2), mid
        assert ov["type_accuracy"]["accuracy"] == pytest.approx(a["ta"], abs=1e-3), mid


def test_meta_counts_7_of_7_all_scored():
    meta = _main_table()["meta"]
    assert meta["models_included"] == 7
    assert meta["models_total"] == 7
    assert set(meta["included_ids"]) == set(SCORED)
    assert meta["pending_ids"] == []
    assert meta["refused_ids"] == []
    # 397B-A17B measured on first-party serving (OpenRouter->Alibaba) rather than the
    # shared host used for the dense sizes; scored and included.
    assert set(meta["pending_ids"]) == set()
    assert meta["refused_ids"] == []  # no model leaks <think>


def test_write_is_idempotent_on_real_data(tmp_path):
    table = _main_table()
    a = write_table(table, tmp_path)
    first = {k: a[k].read_text() for k in a}
    b = write_table(_main_table(), tmp_path)
    second = {k: b[k].read_text() for k in b}
    assert first == second


def test_sonnet_excluded_by_default_supplementary_on():
    main = _main_table()
    assert "claude-sonnet-4-6" not in main["models"]
    supp_entries = [e for e in load_registry() if e.supplementary]
    supp = aggregate_panel(supp_entries, DATA, label="supplementary")
    assert "claude-sonnet-4-6" in supp["models"]
    assert supp["meta"]["label"] == "supplementary"


def test_per_type_and_per_tier_present_and_repool():
    table = _main_table()
    for mid in SCORED:
        m = table["models"][mid]
        assert set(m["by_type"]) == {"class", "sequence"}
        assert set(m["by_tier"]) == {1, 2, 3, 4}
        # re-pooling invariant: summing type micro tp/fp/fn == overall micro tp/fp/fn
        for pop in ("zeros_for_failed", "compiled_only"):
            ov = m["overall"]["element_f1"][pop]["micro"]
            tp = sum(m["by_type"][t]["element_f1"][pop]["micro"]["tp"] for t in ("class", "sequence"))
            assert tp == ov["tp"], (mid, pop)
