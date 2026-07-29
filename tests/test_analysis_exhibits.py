"""Unit + smoke tests for the Task-6 exhibit assembly (analysis/exhibits.py) and
the Task-3 crowding-annotation wiring (analysis/plots.py).

Three layers:
  * **Pure helpers** — arm grouping, parameter labels, CI read-through formatting,
    LaTeX escaping/cells, and the crowding caption/tick helpers.
  * **Document assembly** — render the consolidated markdown over a schema-faithful
    synthetic master/CI (built by the real Task-1/2 builders) and assert the
    two-arms structure, MoE dual-param reporting, population-gap and per-relation
    exhibits are present; optional artifacts (run_level/failure) omit cleanly.
  * **LaTeX + determinism** — the .tex assemblers emit booktabs scaffolding and a
    re-render is byte-identical.
"""
from __future__ import annotations

import json

import pytest

from analysis.aggregate import build_master_table
from analysis.bootstrap import bootstrap_models
from analysis.loader import ModelData
from analysis.registry import ModelEntry
from tests.synth import synth_model

from analysis import exhibits, plots


# --------------------------------------------------------------------------- #
# schema-faithful synthetic panel (frontier + dense ladder + MoE)
# --------------------------------------------------------------------------- #

def _md(mid, display, arm, family, pt, pa):
    base = synth_model(mid, display)
    entry = ModelEntry(id=mid, display=display, run_dir="r", status="scored",
                       lab="lab", arm=arm, family=family,
                       params_total_b=pt, params_active_b=pa, supplementary=False)
    return ModelData(entry=entry, rows=base.rows, summaries=base.summaries)


def _panel():
    return [
        _md("gpt-5.2", "GPT-5.2", "frontier", "dense", None, None),
        _md("qwen3.5-2b", "Qwen3.5-2B", "qwen", "dense", 2, 2),
        _md("qwen3.5-27b", "Qwen3.5-27B", "qwen", "dense", 27, 27),
        _md("qwen3.5-397b-a17b", "Qwen3.5-397B-A17B", "qwen", "moe", 397, 17),
    ]


def _roundtrip(d):
    """The exhibits consume json.load output, so dict keys (tiers) are strings."""
    return json.loads(json.dumps(d))


@pytest.fixture(scope="module")
def master():
    return _roundtrip(build_master_table(_panel(), models_total=7,
                                         pending_ids=["a", "b", "c"]))


@pytest.fixture(scope="module")
def ci():
    return _roundtrip(bootstrap_models(_panel(), n_resamples=48, models_total=7,
                                       pending_ids=["a", "b", "c"]))


@pytest.fixture
def run_level():
    return {
        "meta": {"label": "main", "token_note": "token totals over all cells."},
        "models": [
            {"model_id": "gpt-5.2", "display": "GPT-5.2",
             "tokens": {"input": 1_000_000, "output": 200_000, "reasoning": 0,
                        "total": 1_200_000, "n_cells": 1000, "n_ok": 999},
             "provenance": {"model": "gpt-5.2-2025-12-11", "provider": "openai",
                            "extra_body": {"reasoning_effort": "none"},
                            "max_tokens": 5376, "reasoning_leak": 0}},
        ],
    }


@pytest.fixture
def failure():
    return {
        "meta": {"total_cases": 40, "per_cell": 2, "seed": 20260614,
                 "outcome_classes_sampled": ["compile_fail", "compiled_low_structural"],
                 "included_ids": ["gpt-5.2"],
                 "cell_summary": {"gpt-5.2": {
                     "compile_fail": {"available": 64, "sampled": 16},
                     "compiled_low_structural": {"available": 94, "sampled": 16}}}},
    }


# --------------------------------------------------------------------------- #
# pure helpers — arm grouping / param labels
# --------------------------------------------------------------------------- #

def test_arm_groups_partition(master):
    g = exhibits.arm_groups(master)
    assert [mid for mid, _ in g["frontier"]] == ["gpt-5.2"]
    assert [mid for mid, _ in g["ladder"]] == ["qwen3.5-2b", "qwen3.5-27b"]
    assert [mid for mid, _ in g["moe"]] == ["qwen3.5-397b-a17b"]
    # the MoE never appears on the dense ladder (a plan invariant)
    assert "qwen3.5-397b-a17b" not in {mid for mid, _ in g["ladder"]}


def test_param_label_variants(master):
    b = master["models"]
    assert exhibits.param_label(b["gpt-5.2"]) == "—"           # undisclosed frontier
    assert exhibits.param_label(b["qwen3.5-27b"]) == "27B"      # dense rung
    assert exhibits.param_label(b["qwen3.5-397b-a17b"]) == "397B total / 17B active"


# --------------------------------------------------------------------------- #
# pure helpers — CI read-through formatting
# --------------------------------------------------------------------------- #

def test_ci_md_formats():
    assert exhibits.ci_md(None, exhibits._r3) == "—"
    assert exhibits.ci_md({"point": None}, exhibits._r3) == "—"
    # point only (no CI bounds)
    assert exhibits.ci_md({"point": 0.5}, exhibits._r3) == "0.500"
    # full CI
    got = exhibits.ci_md({"point": 0.5, "ci_low": 0.4, "ci_high": 0.6}, exhibits._r3)
    assert got == "0.500 [0.400, 0.600]"


def test_metric_ci_pair_uses_both_populations(master, ci):
    s = exhibits.metric_ci_pair(ci, "gpt-5.2", "element_f1", "micro", exhibits._r3)
    assert " / " in s and s.count("[") == 2  # a CI for each population


# --------------------------------------------------------------------------- #
# pure helpers — crowding annotation (plots.py)
# --------------------------------------------------------------------------- #

def test_crowding_caption():
    c = {"1": 8.74, "2": 13.25, "3": 21.12, "4": 50.09}
    cap = plots.crowding_caption(c)
    assert cap.startswith("Image crowding")
    assert "T1 8.7" in cap and "T4 50.1" in cap
    assert plots.crowding_caption(None) == ""
    assert plots.crowding_caption({}) == ""


def test_tier_crowding_label():
    c = {"1": 8.74, "4": 50.09}
    assert plots.tier_crowding_label(c, 1) == "8.7"
    assert plots.tier_crowding_label(c, 4) == "50.1"
    assert plots.tier_crowding_label(c, 2) == ""   # absent tier
    assert plots.tier_crowding_label(None, 1) == ""


def test_crowding_annotation_changes_tier_figure(master, tmp_path):
    """Passing crowding alters the per-tier figure (the wiring is live, not ignored)."""
    crowd = {"1": 8.7, "2": 13.2, "3": 21.1, "4": 50.1}
    entries = [_e(m) for m in _panel()]
    plain = plots.save_figure(plots.fig_breakdown_by_tier(entries, master),
                              tmp_path, "tier_plain")
    withc = plots.save_figure(
        plots.fig_breakdown_by_tier(entries, master, crowding=crowd),
        tmp_path, "tier_crowd")
    assert plain["png"].read_bytes() != withc["png"].read_bytes()


def _e(md):
    return md.entry


# --------------------------------------------------------------------------- #
# document assembly
# --------------------------------------------------------------------------- #

def test_render_md_two_arms_and_moe(master, ci):
    md = exhibits.render_exhibits_md(master, ci, None, None, None)
    # two arms, never one leaderboard
    assert "Arm A — Frontier reference points" in md
    assert "Arm B — Qwen open ladder" in md
    assert "not one leaderboard" in md.lower() or "not a fourth dense rung" in md.lower()
    # MoE reports both total and active params
    assert "397B total / 17B active" in md
    # population gap exhibit present with the +signed deltas
    assert "Population gap" in md
    # per-relation exhibit lists all six relations
    for rel in ("inheritance", "composition", "aggregation", "dependency",
                "association", "message"):
        assert rel in md
    # narrative skeleton present
    assert "Results-narrative skeleton" in md


def test_render_md_includes_optional_exhibits(master, ci, run_level, failure):
    md = exhibits.render_exhibits_md(master, ci, run_level, None, failure)
    assert "Token totals" in md and "Reproducibility provenance" in md
    assert "Failure-case coverage" in md and "64→16" in md


def test_render_md_omits_absent_optionals(master, ci):
    md = exhibits.render_exhibits_md(master, ci, None, None, None)
    assert "Token totals" not in md
    assert "Failure-case coverage" not in md


def test_render_md_crowding_section(master, ci):
    crowd = {"1": 8.74, "2": 13.25, "3": 21.12, "4": 50.09}
    md = exhibits.render_exhibits_md(master, ci, None, crowd, None)
    assert "Per-tier image crowding" in md
    assert "50.09" in md


def test_anchor_values_flow_through(master, ci):
    """A headline number must equal the master/CI artifact value (no recompute)."""
    md = exhibits.render_exhibits_md(master, ci, None, None, None)
    pt = ci["per_model"]["gpt-5.2"]["element_f1|micro|zeros_for_failed"]["point"]
    assert f"{pt:.3f}" in md


# --------------------------------------------------------------------------- #
# HTML rendering (Word-importable) + determinism
# --------------------------------------------------------------------------- #

def test_md_to_html_table_structure():
    md = ("## Heading\n\n"
          "| Model | CSR |\n|---|---|\n| GPT-5.2 | 93.5% |\n| Qwen3.5-2B | 20.1% |\n")
    html = exhibits.md_to_html(md)
    assert "<h2>Heading</h2>" in html
    assert "<table>" in html and "</table>" in html
    assert "<th>Model</th>" in html and "<td>GPT-5.2</td>" in html
    # the markdown separator row must NOT become a body row
    assert "---" not in html


def test_md_to_html_inline_and_escaping():
    md = "**bold** and `code` and a < b\n\n| H<br>(n=5) |\n|---|\n| x |\n"
    html = exhibits.md_to_html(md)
    assert "<strong>bold</strong>" in html and "<code>code</code>" in html
    assert "a &lt; b" in html          # a real '<' is escaped
    assert "H<br/>(n=5)" in html       # an intentional <br> is preserved


def test_render_html_has_all_tables_and_two_arms(master, ci, run_level, failure):
    crowd = {"1": 8.74, "2": 13.25, "3": 21.12, "4": 50.09}
    md = exhibits.render_exhibits_md(master, ci, run_level, crowd, failure)
    html = exhibits.md_to_html(md)
    assert html.startswith("<!DOCTYPE html>")
    assert "Arm A" in html and "Arm B" in html
    assert "397B total / 17B active" in html
    # one HTML table per markdown pipe-table in the document
    assert html.count("<table>") == md.count("\n|---")


def test_exhibits_deterministic(master, ci, run_level, failure):
    crowd = {"1": 8.74, "2": 13.25, "3": 21.12, "4": 50.09}
    a = exhibits.render_exhibits_md(master, ci, run_level, crowd, failure)
    b = exhibits.render_exhibits_md(master, ci, run_level, crowd, failure)
    assert a == b
    assert exhibits.md_to_html(a) == exhibits.md_to_html(b)
