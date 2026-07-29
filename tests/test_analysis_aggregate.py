"""Unit tests for the pure pooling functions and the master-table builder."""
import pytest

from analysis.aggregate import (
    RELATIONS,
    build_master_table,
    chrf_macro,
    csr_rate,
    mean_macro,
    pool_micro,
    pool_type_acc,
)
from synth import synth_model


def approx(x):
    return pytest.approx(x, abs=1e-9)


# ---- pure pooling ----

def test_pool_micro_sums_tp_fp_fn():
    r = pool_micro([{"tp": 3, "fp": 1, "fn": 0}, {"tp": 0, "fp": 0, "fn": 4}])
    assert r["tp"] == 3 and r["fp"] == 1 and r["fn"] == 4
    assert r["precision"] == approx(3 / 4)
    assert r["recall"] == approx(3 / 7)
    assert r["f1"] == approx(2 * 0.75 * (3 / 7) / (0.75 + 3 / 7))


def test_pool_micro_empty_is_zero():
    r = pool_micro([])
    assert r["precision"] == 0.0 and r["recall"] == 0.0 and r["f1"] == 0.0


def test_mean_macro_averages_stored_per_diagram_scores():
    r = mean_macro([
        {"precision": 1.0, "recall": 1.0, "f1": 1.0},
        {"precision": 0.0, "recall": 0.0, "f1": 0.0},
    ])
    assert r["precision"] == approx(0.5)
    assert r["f1"] == approx(0.5)


def test_csr_rate():
    r = csr_rate([{"compiled": True}, {"compiled": False}, {"compiled": True}])
    assert r["compiled"] == 2 and r["n"] == 3 and r["csr"] == approx(2 / 3)


def test_chrf_macro_zeroes_noncompiled_only_for_zeros_population():
    rows = [
        {"score": 80.0, "compiled": True},
        {"score": 10.0, "compiled": False},  # raw score kept on disk, zeroed for zeros pop
        {"score": 60.0, "compiled": True},
    ]
    assert chrf_macro(rows, "zeros_for_failed") == approx(140.0 / 3)
    assert chrf_macro(rows, "compiled_only") == approx(70.0)


def test_pool_type_acc_denominator_excludes_excluded():
    rows = [
        {"type_accuracy": {"matched": 4, "correct": 3, "excluded": 0}},
        {"type_accuracy": {"matched": 2, "correct": 1, "excluded": 1}},
    ]
    r = pool_type_acc(rows)
    assert r["matched"] == 6 and r["correct"] == 4 and r["excluded"] == 1
    assert r["denominator"] == 5
    assert r["accuracy"] == approx(0.8)


def test_pool_type_acc_zero_denominator_is_none():
    r = pool_type_acc([{"type_accuracy": {"matched": 1, "correct": 0, "excluded": 1}}])
    assert r["denominator"] == 0
    assert r["accuracy"] is None


# ---- master-table builder ----

def test_master_table_meta_and_header_counts():
    t = build_master_table([synth_model()], models_total=7, pending_ids=["a", "b", "c"])
    assert t["meta"]["models_included"] == 1
    assert t["meta"]["models_total"] == 7
    assert t["meta"]["included_ids"] == ["m1"]
    assert t["meta"]["pending_ids"] == ["a", "b", "c"]


def test_master_table_overall_cell_reproduces_pooling():
    t = build_master_table([synth_model()], models_total=7, pending_ids=[])
    ov = t["models"]["m1"]["overall"]
    assert ov["csr"]["csr"] == approx(0.75)
    # element zeros micro over all 4: tp6 fp1 fn4
    z = ov["element_f1"]["zeros_for_failed"]["micro"]
    assert (z["tp"], z["fp"], z["fn"]) == (6, 1, 4)
    assert z["f1"] == approx(2 * (6 / 7) * 0.6 / ((6 / 7) + 0.6))
    # element compiled micro over d1,d3,d4: tp6 fp1 fn1 -> f1 6/7
    c = ov["element_f1"]["compiled_only"]["micro"]
    assert c["f1"] == approx(6 / 7)
    # chrf macro pooled, micro read-through
    assert ov["chrf"]["zeros_for_failed"]["macro"] == approx(210.0 / 4)
    assert ov["chrf"]["compiled_only"]["macro"] == approx(70.0)
    assert ov["chrf"]["zeros_for_failed"]["micro"] == approx(50.0)
    assert ov["chrf"]["compiled_only"]["micro"] == approx(70.0)


def test_master_table_subcells_repool_and_chrf_micro_is_none():
    t = build_master_table([synth_model()], models_total=7, pending_ids=[])
    m = t["models"]["m1"]
    assert set(m["by_type"]) == {"class", "sequence"}
    assert set(m["by_tier"]) == {1, 2, 3}  # only tiers present (d1/d3=1, d2=2, d4=3)
    cls = m["by_type"]["class"]
    # class zeros micro over d1,d2: tp2 fp0 fn3
    z = cls["element_f1"]["zeros_for_failed"]["micro"]
    assert (z["tp"], z["fp"], z["fn"]) == (2, 0, 3)
    # chrf micro not available per-cell (corpus stat)
    assert cls["chrf"]["zeros_for_failed"]["micro"] is None
    assert cls["chrf"]["compiled_only"]["micro"] is None
    # chrf macro IS poolable per-cell: class zeros = (80 + 0)/2 = 40
    assert cls["chrf"]["zeros_for_failed"]["macro"] == approx(40.0)


def test_master_table_readthrough_per_relation_and_type_per_gt():
    t = build_master_table([synth_model()], models_total=7, pending_ids=[])
    m = t["models"]["m1"]
    assert set(m["per_relation"]) == {"zeros_for_failed", "compiled_only"}
    assert set(m["per_relation"]["zeros_for_failed"]) == set(RELATIONS)
    assert m["per_relation"]["zeros_for_failed"]["message"]["f1"] == approx(0.5)
    pgt = m["type_accuracy_per_gt_type"]
    assert pgt["population"] == "compiled_only"
    assert pgt["per_type"]["class"]["accuracy"] == approx(1.0)
    assert pgt["excluded"] == 0


def test_master_table_overall_type_acc_pooled_matches_expected():
    t = build_master_table([synth_model()], models_total=7, pending_ids=[])
    ov = t["models"]["m1"]["overall"]
    # type acc pooled over compiled element rows d1(2,2,0),d3(1,0,0),d4(3,3,0)
    ta = ov["type_accuracy"]
    assert ta["matched"] == 6 and ta["correct"] == 5 and ta["excluded"] == 0
    assert ta["accuracy"] == approx(5 / 6)


def test_population_gap_is_compiled_minus_all():
    # the headline "selective-failure" fingerprint: compiled_only - zeros_for_failed.
    ov = build_master_table([synth_model()], models_total=7, pending_ids=[])["models"]["m1"]["overall"]
    pg = ov["population_gap"]
    for metric in ("element_f1", "relationship_f1"):
        for level in ("micro", "macro"):
            z = ov[metric]["zeros_for_failed"][level]["f1"]
            c = ov[metric]["compiled_only"][level]["f1"]
            g = pg[metric][level]
            assert g["all"] == approx(z)
            assert g["compiled"] == approx(c)
            assert g["gap"] == approx(c - z)
    for level in ("micro", "macro"):           # chrf carries a scalar per population
        z = ov["chrf"]["zeros_for_failed"][level]
        c = ov["chrf"]["compiled_only"][level]
        g = pg["chrf"][level]
        assert g["all"] == approx(z) and g["compiled"] == approx(c) and g["gap"] == approx(c - z)


def test_population_gap_chrf_micro_none_in_subcells():
    # chrf micro is a corpus stat (None outside overall) -> its gap is None there,
    # but the poolable chrf macro gap is still defined.
    bt = build_master_table([synth_model()], models_total=7, pending_ids=[])["models"]["m1"]["by_tier"]
    for cell in bt.values():
        assert cell["population_gap"]["chrf"]["micro"]["gap"] is None
        assert cell["population_gap"]["chrf"]["macro"]["gap"] is not None
        assert cell["population_gap"]["element_f1"]["micro"]["gap"] is not None
