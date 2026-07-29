"""Unit tests for the paired percentile bootstrap (analysis/bootstrap.py).

Covers: the percentile helper on a known list; centre reproduction (model_stats
reuses the Task-1 aggregate primitives, so the un-resampled statistic equals the
master-table value); a degenerate fixture whose every diagram is identical, so
every resample yields the same statistic and the interval collapses to the point
(a fixed, seed-independent interval); self-difference = exactly [0, 0];
determinism under a fixed seed; and per-relation None handling for a relation
absent on both sides.
"""
import math

import pytest

from analysis import aggregate as agg
from analysis import bootstrap as bs
from analysis.registry import ModelEntry
from analysis.loader import ModelData
from tests.synth import make_row, synth_model


def approx(a, b):
    return math.isclose(a, b, rel_tol=0, abs_tol=1e-12)


def _model(mid, rows):
    entry = ModelEntry(id=mid, display=mid, run_dir="r", status="scored", lab="qwen",
                       arm="qwen", family="dense", params_total_b=9, params_active_b=9,
                       supplementary=False)
    summaries = {"chrf": {"zeros_for_failed": {"micro": 11.0}, "compiled_only": {"micro": 22.0}}}
    return ModelData(entry=entry, rows=rows, summaries=summaries)


# --------------------------------------------------------------------------- #
# percentile helper
# --------------------------------------------------------------------------- #

def test_percentile_linear_interpolation_known_list():
    vals = list(range(101))  # 0..100
    assert approx(bs.percentile(vals, 0.025), 2.5)
    assert approx(bs.percentile(vals, 0.975), 97.5)
    assert approx(bs.percentile(vals, 0.5), 50.0)


def test_percentile_endpoints():
    vals = [1.0, 2.0, 3.0, 4.0]
    assert approx(bs.percentile(vals, 0.0), 1.0)
    assert approx(bs.percentile(vals, 1.0), 4.0)


def test_percentile_single_value():
    assert approx(bs.percentile([7.0], 0.025), 7.0)


# --------------------------------------------------------------------------- #
# model_stats reproduces the Task-1 aggregate primitives (centre = master table)
# --------------------------------------------------------------------------- #

def test_model_stats_keys_match_stat_ids():
    md = synth_model()
    assert list(bs.model_stats(md.rows)) == bs.stat_ids()


def test_model_stats_reproduces_aggregate_primitives():
    md = synth_model()
    rows = md.rows
    s = bs.model_stats(rows)

    assert approx(s["csr|csr"], agg.csr_rate([r["csr"] for r in rows])["csr"])
    for pop in agg.POPULATIONS:
        el = [r["element"] for r in rows]
        rel = [r["relationship"] for r in rows]
        chrf = [r["chrf"] for r in rows]
        el_pop = el if pop == "zeros_for_failed" else [r for r in el if r["compiled"]]
        rel_pop = rel if pop == "zeros_for_failed" else [r for r in rel if r["compiled"]]
        assert approx(s[f"element_f1|micro|{pop}"], agg.pool_micro(el_pop)["f1"])
        assert approx(s[f"element_f1|macro|{pop}"], agg.mean_macro(el_pop)["f1"])
        assert approx(s[f"relationship_f1|micro|{pop}"], agg.pool_micro(rel_pop)["f1"])
        assert approx(s[f"relationship_f1|macro|{pop}"], agg.mean_macro(rel_pop)["f1"])
        assert approx(s[f"chrf|macro|{pop}"], agg.chrf_macro(chrf, pop))
    ta = agg.pool_type_acc([r["element"] for r in rows if r["element"]["compiled"]])
    assert approx(s["type_accuracy|accuracy|compiled_only"], ta["accuracy"])


def test_model_stats_per_relation_absent_relation_is_none():
    # synth puts all edges in inheritance/message; aggregation is absent on both
    # sides -> undefined F1 -> None (excluded from the bootstrap percentiles).
    s = bs.model_stats(synth_model().rows)
    assert s["relationship_f1::aggregation|micro|zeros_for_failed"] is None
    assert s["relationship_f1::inheritance|micro|zeros_for_failed"] is not None


# --------------------------------------------------------------------------- #
# bootstrap point estimate == un-resampled model_stats
# --------------------------------------------------------------------------- #

def test_bootstrap_point_equals_full_sample_stat():
    md = synth_model("m1")
    res = bs.bootstrap_models([md], n_resamples=64, seed=bs.SEED)
    full = bs.model_stats(md.rows)
    pm = res["per_model"]["m1"]
    for sid in bs.stat_ids():
        if full[sid] is None:
            assert pm[sid]["point"] is None
        else:
            assert approx(pm[sid]["point"], full[sid])


def test_bootstrap_reports_chrf_micro_point_only():
    md = _model("m1", synth_model().rows)
    res = bs.bootstrap_models([md], n_resamples=16, seed=bs.SEED)
    po = res["per_model_point_only"]["m1"]
    assert approx(po["chrf|micro|zeros_for_failed"], 11.0)
    assert approx(po["chrf|micro|compiled_only"], 22.0)
    # chrf micro is NOT among the CI stats
    assert not any(sid.startswith("chrf|micro") for sid in bs.stat_ids())


# --------------------------------------------------------------------------- #
# deterministic interval (degenerate fixture) + determinism under fixed seed
# --------------------------------------------------------------------------- #

def _constant_model(mid="c1", n=8):
    # every diagram identical -> any resample yields the same statistic
    rows = [make_row(f"d{i}", "class", 1, True, (2, 0, 0), (1, 0, 0), 50.0, (2, 2, 0),
                     rel_type="inheritance") for i in range(n)]
    return _model(mid, rows)


def test_constant_metric_collapses_ci_to_point():
    md = _constant_model()
    res = bs.bootstrap_models([md], n_resamples=50, seed=bs.SEED)
    pm = res["per_model"]["c1"]
    for sid in ("element_f1|micro|zeros_for_failed",
                "relationship_f1|micro|compiled_only",
                "csr|csr", "chrf|macro|zeros_for_failed"):
        cell = pm[sid]
        assert approx(cell["ci_low"], cell["point"])
        assert approx(cell["ci_high"], cell["point"])


def test_bootstrap_is_deterministic_under_fixed_seed():
    a = bs.bootstrap_models([synth_model("m1"), synth_model("m2")], n_resamples=128, seed=bs.SEED)
    b = bs.bootstrap_models([synth_model("m1"), synth_model("m2")], n_resamples=128, seed=bs.SEED)
    assert a == b


def test_resamples_are_shared_across_models_paired():
    # make_resamples is a pure function of (n_rows, n_resamples, seed): the SAME
    # index draws are applied to every model -> pairing by position.
    r1 = bs.make_resamples(4, n_resamples=20, seed=bs.SEED)
    r2 = bs.make_resamples(4, n_resamples=20, seed=bs.SEED)
    assert r1 == r2
    assert all(0 <= i < 4 for draw in r1 for i in draw)
    assert all(len(draw) == 4 for draw in r1)


# --------------------------------------------------------------------------- #
# pairwise difference CIs
# --------------------------------------------------------------------------- #

def test_self_difference_is_exactly_zero_interval():
    vals = [0.1, 0.4, 0.55, 0.6, 0.9]
    d = bs.diff_ci(vals, vals, 0.5, 0.5)
    assert d["diff_point"] == 0.0
    assert d["ci_low"] == 0.0 and d["ci_high"] == 0.0
    assert d["excludes_zero"] is False


def test_pairwise_self_pair_excluded_but_distinct_pairs_present():
    res = bs.bootstrap_models([synth_model("m1"), synth_model("m2"), synth_model("m3")],
                              n_resamples=32, seed=bs.SEED)
    pairs = {(p["model_a"], p["model_b"]) for p in res["pairwise"]}
    assert ("m1", "m1") not in pairs
    assert ("m1", "m2") in pairs
    assert ("m2", "m1") not in pairs  # unordered: only one orientation
    assert len(pairs) == 3  # C(3,2)


def test_diff_ci_excludes_zero_flag():
    # all differences strictly positive -> CI excludes 0
    pos = [0.2, 0.3, 0.25, 0.4, 0.35]
    d = bs.diff_ci(pos, [0.0] * 5, 0.3, 0.0)
    assert d["ci_low"] > 0 and d["excludes_zero"] is True


def test_diff_ci_drops_none_resamples():
    # None on either side (e.g. an absent relation in that resample) is skipped
    a = [0.5, None, 0.7, 0.6]
    b = [0.1, 0.2, None, 0.3]
    d = bs.diff_ci(a, b, 0.5, 0.2)
    assert d["n_valid"] == 2  # only indices 0 and 3 are usable
