"""Integration: the paired bootstrap on the real scored runs.

The bootstrap centre (point estimate, independent of the resamples) must reproduce
the Task-1 master table exactly -- same join + same pooling primitives. Skips
cleanly when run data is absent (data/* metric dirs are gitignored)."""
import pytest

from analysis.build_ci_table import bootstrap_panel
from analysis.build_master_table import aggregate_panel
from analysis.ci_report import write_ci_table
from analysis.loader import DEFAULT_DATA_ROOT
from analysis.registry import load_registry, panel_entries

DATA = DEFAULT_DATA_ROOT
SCORED = ["gpt-5.2", "claude-opus-4-6", "gemini-3.1-pro", "qwen3.5-2b", "qwen3.5-9b",
          "qwen3.5-27b", "qwen3.5-397b-a17b"]
_REG = {e.id: e for e in load_registry()}


def _have_data():
    for mid in SCORED:
        rd = _REG[mid].run_dir
        if not rd or not (DATA / "relationship_f1" / rd / "relationship_f1_results.json").exists():
            return False
    return True


pytestmark = pytest.mark.skipif(not _have_data(), reason="scored run data not on disk")

EXACT = 1e-9


def _panel():
    return panel_entries(load_registry())


def _result(n=4):
    # point estimates are independent of n_resamples -> a small n keeps it fast
    return bootstrap_panel(_panel(), DATA, n_resamples=n, seed=12345)


def test_centres_reproduce_master_table_overall():
    table = aggregate_panel(_panel(), DATA, label="main")
    res = _result()
    for mid in SCORED:
        ov = table["models"][mid]["overall"]
        pm = res["per_model"][mid]
        assert pm["csr|csr"]["point"] == pytest.approx(ov["csr"]["csr"], abs=EXACT), mid
        for pop in ("zeros_for_failed", "compiled_only"):
            assert pm[f"element_f1|micro|{pop}"]["point"] == pytest.approx(
                ov["element_f1"][pop]["micro"]["f1"], abs=EXACT), (mid, pop)
            assert pm[f"element_f1|macro|{pop}"]["point"] == pytest.approx(
                ov["element_f1"][pop]["macro"]["f1"], abs=EXACT), (mid, pop)
            assert pm[f"relationship_f1|micro|{pop}"]["point"] == pytest.approx(
                ov["relationship_f1"][pop]["micro"]["f1"], abs=EXACT), (mid, pop)
            assert pm[f"relationship_f1|macro|{pop}"]["point"] == pytest.approx(
                ov["relationship_f1"][pop]["macro"]["f1"], abs=EXACT), (mid, pop)
            assert pm[f"chrf|macro|{pop}"]["point"] == pytest.approx(
                ov["chrf"][pop]["macro"], abs=EXACT), (mid, pop)
        assert pm["type_accuracy|accuracy|compiled_only"]["point"] == pytest.approx(
            ov["type_accuracy"]["accuracy"], abs=EXACT), mid


def test_centres_reproduce_per_relation_readthrough():
    # per-relation point == master-table read-through from summary.by_relation
    # (runner gate iv: pooling the new per-diagram by_relation == summary)
    table = aggregate_panel(_panel(), DATA, label="main")
    res = _result()
    for mid in SCORED:
        pr = table["models"][mid]["per_relation"]
        pm = res["per_model"][mid]
        for pop in ("zeros_for_failed", "compiled_only"):
            for rel, v in pr[pop].items():
                got = pm[f"relationship_f1::{rel}|micro|{pop}"]["point"]
                assert got == pytest.approx(v["f1"], abs=EXACT), (mid, pop, rel)


def test_chrf_micro_point_only_matches_master_table():
    table = aggregate_panel(_panel(), DATA, label="main")
    res = _result()
    for mid in SCORED:
        ov = table["models"][mid]["overall"]
        po = res["per_model_point_only"][mid]
        for pop in ("zeros_for_failed", "compiled_only"):
            assert po[f"chrf|micro|{pop}"] == pytest.approx(ov["chrf"][pop]["micro"], abs=EXACT), (mid, pop)


def test_per_relation_cis_are_populated_on_real_data():
    # all six relations have ample support -> defined point + a real CI
    res = _result(n=200)
    for mid in SCORED:
        for rel in res["meta"]["relations"]:
            cell = res["per_model"][mid][f"relationship_f1::{rel}|micro|zeros_for_failed"]
            assert cell["point"] is not None, (mid, rel)
            assert cell["ci_low"] is not None and cell["n_valid"] > 0, (mid, rel)
            assert cell["ci_low"] <= cell["point"] <= cell["ci_high"] + 1e-9, (mid, rel)


def test_meta_counts_7_of_7_all_scored():
    meta = _result(n=2)["meta"]
    assert meta["models_included"] == 7
    assert meta["models_total"] == 7
    assert set(meta["included_ids"]) == set(SCORED)
    assert set(meta["pending_ids"]) == set()
    assert meta["refused_ids"] == []


def test_pairwise_covers_all_unordered_pairs_and_stats():
    res = _result(n=2)
    n_models = res["meta"]["models_included"]
    n_pairs = n_models * (n_models - 1) // 2
    n_stats = len(res["meta"]["ci_stats"])
    assert len(res["pairwise"]) == n_pairs * n_stats


def test_write_is_idempotent_on_real_data(tmp_path):
    res = bootstrap_panel(_panel(), DATA, n_resamples=64, seed=12345)
    a = write_ci_table(res, tmp_path)
    first = {k: a[k].read_text() for k in a}
    res2 = bootstrap_panel(_panel(), DATA, n_resamples=64, seed=12345)
    b = write_ci_table(res2, tmp_path)
    second = {k: b[k].read_text() for k in b}
    assert first == second
