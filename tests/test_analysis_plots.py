"""Unit + smoke tests for the Task-3 plotting module (analysis/plots.py).

Two layers, matching the task's "tests where they pay":

* **Pure data-shaping helpers** — which model maps to which arm/axis (dense
  ladder vs MoE vs frontier), the (metric, level, population) -> CI stat-id join,
  extracting a point estimate from a master cell, and turning a CI entry into a
  plot-ready asymmetric error bar. Tested on a tiny synthetic fixture.
* **Figure smoke + determinism** — every figure function builds a Figure and
  writes a non-empty PNG *and* PDF; a re-render of the same figure from the same
  data is byte-identical (the determinism the acceptance criteria require).

The fixture is built by running the REAL Task-1 ``build_master_table`` and Task-2
``bootstrap_models`` over synthetic ModelData, so the master/CI dicts are
schema-identical to the on-disk artifacts the plots actually consume.
"""
from __future__ import annotations

import json

import pytest

matplotlib = pytest.importorskip("matplotlib")

from analysis.aggregate import build_master_table
from analysis.bootstrap import bootstrap_models
from analysis.loader import ModelData
from analysis.registry import ModelEntry
from tests.synth import synth_model

from analysis import plots


# --------------------------------------------------------------------------- #
# fixture: a 4-scored / 7-total panel, schema-faithful via the real builders
# --------------------------------------------------------------------------- #

PENDING = ["gemini-3.1-pro", "qwen3.5-27b", "qwen3.5-397b-a17b"]


def _md(mid, display, arm, family, pt, pa):
    base = synth_model(mid, display)
    entry = ModelEntry(id=mid, display=display, run_dir="r", status="scored",
                       lab="lab", arm=arm, family=family,
                       params_total_b=pt, params_active_b=pa, supplementary=False)
    return ModelData(entry=entry, rows=base.rows, summaries=base.summaries)


def _panel():
    return [
        _md("gpt-5.2", "GPT-5.2", "frontier", "dense", None, None),
        _md("claude-opus-4-6", "Claude Opus 4.6", "frontier", "dense", None, None),
        _md("qwen3.5-2b", "Qwen3.5-2B", "qwen", "dense", 2, 2),
        _md("qwen3.5-9b", "Qwen3.5-9B", "qwen", "dense", 9, 9),
    ]


def _roundtrip(d):
    """Mirror the on-disk artifact exactly: the plots consume json.load output, so
    dict keys (e.g. by_tier tiers) are STRINGS, not the ints build_* makes in memory."""
    return json.loads(json.dumps(d))


@pytest.fixture(scope="module")
def master():
    return _roundtrip(build_master_table(_panel(), models_total=7, pending_ids=PENDING))


@pytest.fixture(scope="module")
def ci():
    return _roundtrip(
        bootstrap_models(_panel(), n_resamples=64, models_total=7, pending_ids=PENDING))


def _entry(mid, display, arm, family, pt, pa, run="r", status="scored", supp=False):
    return ModelEntry(id=mid, display=display, run_dir=run, status=status, lab="lab",
                      arm=arm, family=family, params_total_b=pt, params_active_b=pa,
                      supplementary=supp)


def _entries():
    """Full 7-model inventory + Sonnet (supplementary), mirroring the registry."""
    return [
        _entry("gpt-5.2", "GPT-5.2", "frontier", "dense", None, None),
        _entry("claude-opus-4-6", "Claude Opus 4.6", "frontier", "dense", None, None),
        _entry("gemini-3.1-pro", "Gemini 3.1 Pro", "frontier", "dense", None, None,
               run=None, status="in_progress"),
        _entry("qwen3.5-2b", "Qwen3.5-2B", "qwen", "dense", 2, 2),
        _entry("qwen3.5-9b", "Qwen3.5-9B", "qwen", "dense", 9, 9),
        _entry("qwen3.5-27b", "Qwen3.5-27B", "qwen", "dense", 27, 27,
               run=None, status="in_progress"),
        _entry("qwen3.5-397b-a17b", "Qwen3.5-397B-A17B", "qwen", "moe", 397, 17,
               run=None, status="pending"),
        _entry("claude-sonnet-4-6", "Claude Sonnet 4.6", "frontier", "dense", None, None,
               supp=True),
    ]


# --------------------------------------------------------------------------- #
# arm / axis splitting
# --------------------------------------------------------------------------- #

def test_dense_ladder_filters_and_sorts():
    ladder = plots.dense_ladder(_entries())
    assert [e.id for e in ladder] == ["qwen3.5-2b", "qwen3.5-9b", "qwen3.5-27b"]
    # sorted ascending by total params; frontier + MoE excluded
    assert [e.params_total_b for e in ladder] == [2, 9, 27]


def test_moe_entries_only_moe():
    moe = plots.moe_entries(_entries())
    assert [e.id for e in moe] == ["qwen3.5-397b-a17b"]
    assert moe[0].params_total_b == 397 and moe[0].params_active_b == 17


def test_frontier_entries_excludes_supplementary():
    fr = plots.frontier_entries(_entries())
    assert [e.id for e in fr] == ["gpt-5.2", "claude-opus-4-6", "gemini-3.1-pro"]
    assert all(not e.supplementary for e in fr)


def test_moe_never_on_dense_axis():
    """The MoE id must not appear in the dense ladder (a plan invariant)."""
    ladder_ids = {e.id for e in plots.dense_ladder(_entries())}
    assert "qwen3.5-397b-a17b" not in ladder_ids


def test_scaling_curve_with_scored_moe(tmp_path):
    """When the MoE lands it renders as a SEPARATE marker (the diamond + dual-param
    annotation branch), still excluded from the dense ladder."""
    panel = _panel() + [_md("qwen3.5-397b-a17b", "Qwen3.5-397B-A17B", "qwen", "moe", 397, 17)]
    pend = ["gemini-3.1-pro", "qwen3.5-27b"]
    m = _roundtrip(build_master_table(panel, models_total=7, pending_ids=pend))
    c = _roundtrip(bootstrap_models(panel, n_resamples=32, models_total=7, pending_ids=pend))
    assert "qwen3.5-397b-a17b" in m["models"]                                # scored
    assert "qwen3.5-397b-a17b" not in {e.id for e in plots.dense_ladder(_entries())}
    paths = plots.save_figure(plots.fig_scaling_curve(_entries(), m, c), tmp_path, "scaling_moe")
    assert paths["png"].stat().st_size > 0 and paths["pdf"].stat().st_size > 0


# --------------------------------------------------------------------------- #
# colors
# --------------------------------------------------------------------------- #

def test_assign_colors_known_ids_are_fixed():
    ids = ["gpt-5.2", "claude-opus-4-6", "qwen3.5-2b"]
    c = plots.assign_colors(ids)
    assert c["gpt-5.2"] == plots.MODEL_COLORS["gpt-5.2"]
    assert c["claude-opus-4-6"] == plots.MODEL_COLORS["claude-opus-4-6"]


def test_assign_colors_unknown_ids_distinct_and_stable():
    c1 = plots.assign_colors(["mystery-a", "mystery-b"])
    c2 = plots.assign_colors(["mystery-a", "mystery-b"])
    assert c1 == c2                              # deterministic
    assert c1["mystery-a"] != c1["mystery-b"]    # distinct


# --------------------------------------------------------------------------- #
# stat-id join (master metric naming -> CI table stat ids)
# --------------------------------------------------------------------------- #

def test_scaling_stat_id_mapping():
    assert plots.scaling_stat_id("csr") == "csr|csr"
    assert plots.scaling_stat_id("element_f1", "micro", "zeros_for_failed") == \
        "element_f1|micro|zeros_for_failed"
    assert plots.scaling_stat_id("chrf", "macro", "compiled_only") == \
        "chrf|macro|compiled_only"
    assert plots.scaling_stat_id("type_accuracy") == "type_accuracy|accuracy|compiled_only"


def test_per_relation_stat_id():
    assert plots.per_relation_stat_id("inheritance", "zeros_for_failed") == \
        "relationship_f1::inheritance|micro|zeros_for_failed"


# --------------------------------------------------------------------------- #
# point extraction + error bars
# --------------------------------------------------------------------------- #

def test_cell_point_reads_master(master):
    csr = plots.cell_point(master, "qwen3.5-2b", "overall", "csr")
    assert csr == pytest.approx(0.75)  # synth: 3/4 compiled
    el = plots.cell_point(master, "qwen3.5-2b", "overall", "element_f1", "micro",
                          "zeros_for_failed")
    assert 0.0 <= el <= 1.0
    # chrf micro is null in sub-cells (corpus stat) but present overall
    assert plots.cell_point(master, "qwen3.5-2b", "overall", "chrf", "micro",
                            "zeros_for_failed") is not None
    # absent (pending) model -> None, never raises
    assert plots.cell_point(master, "gemini-3.1-pro", "overall", "csr") is None


def test_cell_point_scopes(master):
    # by_type and by_tier scopes resolve; a missing tier (synth has no tier 4) -> None
    assert plots.cell_point(master, "qwen3.5-2b", ("type", "class"), "csr") is not None
    assert plots.cell_point(master, "qwen3.5-2b", ("tier", 1), "csr") is not None
    assert plots.cell_point(master, "qwen3.5-2b", ("tier", 4), "csr") is None


def test_per_relation_point(master):
    v = plots.per_relation_point(master, "qwen3.5-2b", "message", "zeros_for_failed")
    assert v is not None and 0.0 <= v <= 1.0
    assert plots.per_relation_point(master, "absent", "message", "zeros_for_failed") is None


def test_ci_lookup(ci):
    e = plots.ci_lookup(ci, "qwen3.5-2b", "csr|csr")
    assert set(e) == {"point", "ci_low", "ci_high", "n_valid"}
    assert plots.ci_lookup(ci, "absent", "csr|csr") is None


def test_yerr_about_symmetric_and_clamped():
    entry = {"point": 0.8, "ci_low": 0.7, "ci_high": 0.9, "n_valid": 100}
    lo, hi = plots.yerr_about(0.8, entry)
    assert lo == pytest.approx(0.1) and hi == pytest.approx(0.1)
    # plotted point above the CI -> lower arm clamps to 0 (never negative)
    lo2, hi2 = plots.yerr_about(0.95, entry)
    assert lo2 == pytest.approx(0.25) and hi2 == 0.0
    # no CI -> None
    assert plots.yerr_about(0.5, {"point": 0.5, "ci_low": None, "ci_high": None,
                                  "n_valid": 0}) is None
    assert plots.yerr_about(0.5, None) is None


# --------------------------------------------------------------------------- #
# the plotting-join guard: master point == CI point for the same statistic
# --------------------------------------------------------------------------- #

def test_overall_cell_point_matches_ci_point(master, ci):
    for mid in master["models"]:
        for metric, level in [("element_f1", "micro"), ("relationship_f1", "micro"),
                              ("chrf", "macro")]:
            for pop in ["zeros_for_failed", "compiled_only"]:
                mp = plots.cell_point(master, mid, "overall", metric, level, pop)
                cp = plots.ci_lookup(ci, mid, plots.scaling_stat_id(metric, level, pop))["point"]
                assert mp == pytest.approx(cp, abs=1e-9), (mid, metric, level, pop)
        csr_mp = plots.cell_point(master, mid, "overall", "csr")
        assert csr_mp == pytest.approx(plots.ci_lookup(ci, mid, "csr|csr")["point"], abs=1e-9)


# --------------------------------------------------------------------------- #
# figure smoke tests: each writes a non-empty PNG + PDF
# --------------------------------------------------------------------------- #

def _assert_nonempty(paths):
    assert paths["png"].exists() and paths["png"].stat().st_size > 0
    assert paths["pdf"].exists() and paths["pdf"].stat().st_size > 0


def test_fig_scaling_curve(master, ci, tmp_path):
    fig = plots.fig_scaling_curve(_entries(), master, ci)
    _assert_nonempty(plots.save_figure(fig, tmp_path, "scaling_curve"))


def test_fig_per_relation(master, ci, tmp_path):
    fig = plots.fig_per_relation(_entries(), master, ci, population="zeros_for_failed")
    _assert_nonempty(plots.save_figure(fig, tmp_path, "per_relation"))


def test_fig_breakdown_by_tier(master, tmp_path):
    fig = plots.fig_breakdown_by_tier(_entries(), master)
    _assert_nonempty(plots.save_figure(fig, tmp_path, "by_tier"))


def test_fig_breakdown_by_type(master, tmp_path):
    fig = plots.fig_breakdown_by_type(_entries(), master)
    _assert_nonempty(plots.save_figure(fig, tmp_path, "by_type"))


def test_fig_frontier_bars(master, ci, tmp_path):
    fig = plots.fig_frontier_bars(_entries(), master, ci, population="zeros_for_failed")
    _assert_nonempty(plots.save_figure(fig, tmp_path, "frontier"))


def test_render_all_writes_inventory(master, ci, tmp_path):
    produced = plots.render_all(_entries(), master, ci, tmp_path)
    assert produced  # non-empty mapping
    for name, paths in produced.items():
        _assert_nonempty(paths)


def test_pending_models_do_not_break_figures(master, ci, tmp_path):
    """Pending gemini / 27B / MoE are in the inventory but absent from master/CI;
    figures must render anyway (incremental: render what's scored, mark pending)."""
    produced = plots.render_all(_entries(), master, ci, tmp_path)
    assert len(produced) >= 5


# --------------------------------------------------------------------------- #
# determinism: re-rendering the same figure from the same data is byte-identical
# --------------------------------------------------------------------------- #

def test_figure_bytes_deterministic(master, ci, tmp_path):
    p1 = plots.save_figure(plots.fig_per_relation(_entries(), master, ci),
                           tmp_path / "a", "fig")
    p2 = plots.save_figure(plots.fig_per_relation(_entries(), master, ci),
                           tmp_path / "b", "fig")
    assert p1["png"].read_bytes() == p2["png"].read_bytes(), "PNG not byte-identical"
    assert p1["pdf"].read_bytes() == p2["pdf"].read_bytes(), "PDF not byte-identical"


# --------------------------------------------------------------------------- #
# CLI (analysis/build_plots.py)
# --------------------------------------------------------------------------- #

def _registry_dict(entries):
    return {"models": [{"id": e.id, "display": e.display, "run_dir": e.run_dir,
                        "status": e.status, "lab": e.lab, "arm": e.arm,
                        "family": e.family, "params_total_b": e.params_total_b,
                        "params_active_b": e.params_active_b,
                        "supplementary": e.supplementary} for e in entries]}


def test_load_artifacts_missing_raises(tmp_path):
    from analysis import build_plots
    with pytest.raises(FileNotFoundError) as ei:
        build_plots.load_artifacts(tmp_path)
    # error must point the user at the builder to run (STOP-and-report friendly)
    assert "master_table" in str(ei.value)


def test_load_artifacts_reads(tmp_path, master, ci):
    from analysis import build_plots
    (tmp_path / "master_table.json").write_text(json.dumps(master))
    (tmp_path / "ci_table.json").write_text(json.dumps(ci))
    m, c = build_plots.load_artifacts(tmp_path)
    assert m["meta"]["models_total"] == 7 and "per_model" in c


def test_main_renders_into_out_dir(tmp_path, master, ci):
    from analysis import build_plots
    (tmp_path / "master_table.json").write_text(json.dumps(master))
    (tmp_path / "ci_table.json").write_text(json.dumps(ci))
    regp = tmp_path / "registry.json"
    regp.write_text(json.dumps(_registry_dict(_entries())))

    rc = build_plots.main(["--registry", str(regp), "--out-dir", str(tmp_path)])
    assert rc == 0
    plots_dir = tmp_path / "plots"
    pngs = sorted(plots_dir.glob("*.png"))
    pdfs = sorted(plots_dir.glob("*.pdf"))
    assert len(pngs) >= 5 and len(pdfs) == len(pngs)
    assert all(p.stat().st_size > 0 for p in pngs + pdfs)
