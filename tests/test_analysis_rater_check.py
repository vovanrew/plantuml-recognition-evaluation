"""Tests for analysis/rater_check.py (human-rater check on model-against-model pairs)."""
import collections
import json

import pytest

from analysis import rater_check as R

COMP = ("m1", "m2")


def _row(compiled, ef, rf):
    return {"csr": {"compiled": compiled}, "element": {"f1": ef}, "relationship": {"f1": rf}}


def _scores(ef, rf, compiled=(True, True)):
    return {"compiled": compiled, "ef": ef, "rf": rf}


# --------------------------------------------------------------------------- #
# pool, direction, stratum
# --------------------------------------------------------------------------- #
def test_direction_uses_element_f1_first():
    assert R.direction(_scores((0.9, 0.5), (0.1, 0.8))) == 0
    assert R.direction(_scores((0.5, 0.5), (0.1, 0.8))) == 1
    assert R.direction(_scores((0.5, 0.5), (0.8, 0.8))) is None


def test_stratum():
    assert R.stratum(_scores((0.9, 0.5), (0.1, 0.1))) == "ef"
    assert R.stratum(_scores((0.5, 0.5), (0.1, 0.8))) == "rf"


def test_pool_needs_both_compiled_a_difference_and_no_exclusion():
    a = {"k1": _row(True, 1, 1), "k2": _row(False, 1, 0), "k3": _row(True, 1, 1), "k4": _row(True, 1, 0)}
    b = {"k1": _row(True, 0, 1), "k2": _row(True, 0, 1), "k3": _row(True, 1, 1), "k4": _row(True, 1, 1)}
    assert set(R.comparison_pool(a, b)) == {"k1", "k4"}
    assert set(R.comparison_pool(a, b, exclude={"k1"})) == {"k4"}


def test_split_types_even_and_short_cells():
    assert R.split_types(4, {"class": 9, "sequence": 9}) == {"class": 2, "sequence": 2}
    assert R.split_types(3, {"class": 9, "sequence": 9}) == {"class": 2, "sequence": 1}
    assert R.split_types(3, {"class": 0, "sequence": 9}) == {"class": 0, "sequence": 3}
    with pytest.raises(ValueError):
        R.split_types(3, {"class": 1, "sequence": 1})


def test_quotas():
    pool = {f"k{i}": _scores((1, 0) if i < 10 else (0, 1), (0, 0)) for i in range(13)}
    assert R.direction_quota(pool) == {0: 8, 1: 7}
    assert R.stratum_quota(8) == {"ef": 4, "rf": 4}
    assert R.stratum_quota(7) == {"ef": 3, "rf": 4}


# --------------------------------------------------------------------------- #
# the draw
# --------------------------------------------------------------------------- #
def _synthetic(n=200, seed_offset=0):
    """Two comparisons sharing keys; every direction x stratum x type cell well filled."""
    meta, pools = {}, {}
    for i in range(n):
        meta[f"k{i:03d}"] = {"primary_type": R.TYPES[i % 2], "tier": f"T{1 + i % 4}"}
    for c, comp in enumerate((("m1", "m2"), ("m3", "m2"))):
        pool = {}
        for i in range(n):
            d = (i // 2 + c) % 2
            st = (i // 4) % 2
            ef = (0.9, 0.4) if d == 0 else (0.4, 0.9)
            rf = (0.8, 0.3) if d == 0 else (0.3, 0.8)
            pool[f"k{i:03d}"] = _scores(ef if st == 0 else (0.5, 0.5), rf)
        pools[comp] = pool
    return pools, meta


def test_draw_sizes_strata_and_unique_keys():
    pools, meta = _synthetic()
    pairs = R.draw(pools, meta)
    assert len(pairs) == 30
    assert len({p["key"] for p in pairs}) == 30
    assert [p["pair"] for p in pairs] == [f"P{i:02d}" for i in range(1, 31)]
    by = collections.Counter((p["comparison"], p["stratum"]) for p in pairs)
    for comp in pools:
        cid = R.comparison_id(comp)
        assert by[(cid, "ef")] == 7 and by[(cid, "rf")] == 8
    for p in pairs:
        assert {p["A"], p["B"]} == set(p["models"])
        s = {m: (p["scores"]["ef"][m], p["scores"]["rf"][m]) for m in p["models"]}
        assert p["direction"] == p["models"][R.direction(
            {"ef": (s[p["models"][0]][0], s[p["models"][1]][0]),
             "rf": (s[p["models"][0]][1], s[p["models"][1]][1])})]


def test_draw_is_deterministic():
    pools, meta = _synthetic()
    assert R.draw(pools, meta) == R.draw(pools, meta)


def test_rater_orders_differ_and_cover_all():
    pools, meta = _synthetic()
    pairs = R.draw(pools, meta)
    o1, o2 = R.rater_order(pairs, "R1"), R.rater_order(pairs, "R2")
    assert sorted(o1) == sorted(o2) == [p["pair"] for p in pairs]
    assert o1 != o2


def test_sheet_names_no_model():
    html = R.sheet_html("R2", ["P01", "P02"])
    assert "R2" in html and '["P01", "P02"]' in html and R.QUESTION in html
    for word in ("gemini", "claude", "gpt", "qwen", "m1", "m2"):
        assert word not in html.lower()


# --------------------------------------------------------------------------- #
# the report
# --------------------------------------------------------------------------- #
def _pair(pid, ef, rf, comp="m1__m2", a="m1"):
    s = {"ef": {"m1": ef[0], "m2": ef[1]}, "rf": {"m1": rf[0], "m2": rf[1]}}
    d = R.direction({"ef": ef, "rf": rf})
    return {"pair": pid, "comparison": comp, "models": ["m1", "m2"], "key": pid.lower(),
            "primary_type": "class", "direction": ["m1", "m2"][d], "scores": s,
            "stratum": R.stratum({"ef": ef, "rf": rf}), "A": a, "B": "m2" if a == "m1" else "m1"}


def test_agreement_counts_and_same():
    pairs = [_pair("P1", (1, 0), (1, 0)), _pair("P2", (1, 0), (0, 1), a="m2"),
             _pair("P3", (0.5, 0.5), (0, 1)), _pair("P4", (0, 1), (0, 1))]
    rt = {"P1": {"choice": "A"}, "P2": {"choice": "B"}, "P3": {"choice": "same"}, "P4": {"choice": "A"}}
    ef = R.agreement(pairs, rt, R.by_metric("ef"))
    assert (ef["pairs"], ef["agree"], ef["against"], ef["same"]) == (3, 2, 1, 0)
    rf = R.agreement(pairs, rt, R.by_metric("rf"))
    assert (rf["pairs"], rf["agree"], rf["against"], rf["same"]) == (4, 1, 2, 1)
    opp = R.agreement(pairs, rt, R.by_metric("ef"), R.opposite)
    assert opp["pairs"] == 1


def test_gap_uses_the_deciding_metric_and_bins():
    p_ef = _pair("P1", (0.9, 1.0), (0.0, 1.0))      # Element F1 differs: gap 0.1, not 1.0
    p_rf = _pair("P2", (1, 1), (0.6, 0.2))          # only Relationship F1 differs: gap 0.4
    assert p_ef["stratum"] == "ef" and abs(R.gap(p_ef) - 0.1) < 1e-9
    assert p_rf["stratum"] == "rf" and abs(R.gap(p_rf) - 0.4) < 1e-9
    assert R.gap_bins() == [(0.0, 0.05), (0.05, 0.15), (0.15, 0.35), (0.35, None)]
    assert R.in_bin(_pair("P3", (0.95, 1.0), (1, 1)), 0.05, 0.15)   # lower edge included
    pairs = [p_ef, p_rf]
    ratings = {"R1": {"P1": {"choice": "B"}, "P2": {"choice": "A"}},
               "R2": {"P1": {"choice": "A"}, "P2": {"choice": "same"}}}
    rows = R.by_gap(pairs, ratings)
    assert [r["pairs"] for r in rows] == [0, 1, 0, 1]
    assert (rows[1]["pooled"]["agree"], rows[1]["pooled"]["picks"]) == (1, 2)   # P1 prefers m2 = B
    assert (rows[3]["pooled"]["agree"], rows[3]["pooled"]["picks"]) == (1, 1)
    assert rows[0]["pooled"]["share"] is None


def test_wilson_known_value():
    lo, hi = R.wilson(45, 48)
    assert round(lo, 2) == 0.83 and round(hi, 2) == 0.98
    assert R.wilson(0, 0) is None


def test_kappa():
    k = R.kappa(["A", "B", "A", "same"], ["A", "B", "B", "same"])
    assert k["agree"] == 3 and k["raw"] == 0.75
    assert 0 < k["kappa"] < 1


def test_report_both_against(tmp_path):
    pairs = [_pair("P1", (1, 0), (1, 0)), _pair("P2", (1, 0), (1, 0))]
    ratings = {"R1": {"P1": {"choice": "B", "comment": ""}, "P2": {"choice": "A", "comment": ""}},
               "R2": {"P1": {"choice": "B", "comment": "x"}, "P2": {"choice": "B", "comment": ""}}}
    rep = R.report(pairs, ratings)
    assert [p["pair"] for p in rep["both_against_direction"]] == ["P1"]
    assert rep["between_raters"]["agree"] == 1
    f = tmp_path / "d.csv"
    f.write_text("pair,differs,kind\nP1,one arrow,arrows\n", encoding="utf-8")
    R.add_differences(rep, R.read_differences(f, rep["both_against_direction"]))
    md = R.report_md(rep)
    assert "one arrow" in md and "m1 vs m2" in md
    f.write_text("pair,differs,kind\nP2,x,y\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        R.read_differences(f, rep["both_against_direction"])


def test_read_ratings_validates(tmp_path):
    pairs = [{"pair": "P1"}, {"pair": "P2"}]
    f = tmp_path / "R1.csv"
    f.write_text('pair,choice,comment\nP1,A,""\nP2,same,"ok"\n', encoding="utf-8")
    assert R.read_ratings(f, pairs)["P2"] == {"choice": "same", "comment": "ok"}
    for bad in ('pair,choice,comment\nP1,A,\n',
                'pair,choice,comment\nP1,A,\nP2,C,\n',
                'pair,choice,comment\nP1,A,\nP1,B,\nP2,A,\n',
                'pair,choice,comment\nP1,A,\nP2,A,\nP9,A,\n'):
        f.write_text(bad, encoding="utf-8")
        with pytest.raises(ValueError):
            R.read_ratings(f, pairs)


def test_build_sheet_copies_pictures(tmp_path):
    pairs = [_pair("P1", (1, 0), (1, 0))]
    run_dirs = {"m1": "run1", "m2": "run2"}
    images, render = tmp_path / "img", tmp_path / "render"
    images.mkdir()
    render.mkdir()
    (images / "p1.png").write_bytes(b"o")
    (render / "run1__p1.png").write_bytes(b"1")
    (render / "run2__p1.png").write_bytes(b"2")
    R.build_sheet(pairs, run_dirs, "R1", tmp_path / "R1", render, images)
    out = tmp_path / "R1" / "img"
    assert (out / "P1_o.png").read_bytes() == b"o"
    assert (out / "P1_a.png").read_bytes() == b"1" and (out / "P1_b.png").read_bytes() == b"2"
    names = json.dumps(sorted(p.name for p in out.iterdir()))
    assert "run" not in names and "p1." not in names
