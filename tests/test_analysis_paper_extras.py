"""Stratum intervals (analysis.build_paper_extras): the statistics and their values."""
import math

from analysis.bootstrap import make_resamples
from analysis.build_paper_extras import STATS, stratum_table
from tests.synth import synth_model

CHRF_ALL = "chrf|macro|zeros_for_failed"
CHRF_COMPILED = "chrf|macro|compiled_only"


def _table():
    m = synth_model()
    return stratum_table([m], make_resamples(len(m.rows), 50, 7))["m1"]


def test_stats_cover_csr_f1_and_chrf_in_both_populations():
    ids = [sid for sid, _ in STATS]
    assert ids == [
        "csr|csr",
        "element_f1|micro|zeros_for_failed", "element_f1|micro|compiled_only",
        "relationship_f1|micro|zeros_for_failed", "relationship_f1|micro|compiled_only",
        CHRF_ALL, CHRF_COMPILED,
    ]


def test_chrf_point_values_per_stratum():
    # synth rows: d1 class t1 compiled 80; d2 class t2 failed 5; d3 sequence t1 compiled 60;
    # d4 sequence t3 compiled 70. A failed answer scores 0 in the full set.
    t = _table()
    assert math.isclose(t["strata"]["1"][CHRF_ALL]["point"], 70.0)
    assert math.isclose(t["strata"]["1"][CHRF_COMPILED]["point"], 70.0)
    assert math.isclose(t["strata"]["2"][CHRF_ALL]["point"], 0.0)
    assert math.isclose(t["strata"]["class"][CHRF_ALL]["point"], 40.0)
    assert math.isclose(t["strata"]["class"][CHRF_COMPILED]["point"], 80.0)


def test_chrf_contrasts_are_reported():
    t = _table()
    for contrast in ("class - sequence", "1 - 4"):
        assert CHRF_ALL in t["contrasts"][contrast]
        assert CHRF_COMPILED in t["contrasts"][contrast]
    d = t["contrasts"]["class - sequence"][CHRF_COMPILED]
    assert math.isclose(d["diff_point"], 80.0 - 65.0)
