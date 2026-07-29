"""Tests for the master-table emitters (markdown / CSV / JSON)."""
import csv
import json

from analysis.aggregate import build_master_table
from analysis.report import render_markdown, write_table
from synth import synth_model


def _table():
    return build_master_table([synth_model()], models_total=7, pending_ids=["x", "y", "z"])


def test_markdown_shows_n_of_total_header_and_pending():
    md = render_markdown(_table())
    assert "Models included: 1/7" in md
    assert "M1" in md            # display name present
    assert "Pending" in md or "pending" in md


def test_markdown_has_metric_sections():
    md = render_markdown(_table())
    for token in ["CSR", "Element F1", "Relationship F1", "chrF", "Type accuracy"]:
        assert token in md


def test_write_table_emits_md_csv_json(tmp_path):
    paths = write_table(_table(), tmp_path)
    for name in ("json", "md", "csv"):
        assert paths[name].exists()
    # JSON is the full artifact and is valid + structured
    obj = json.loads(paths["json"].read_text())
    assert obj["meta"]["models_total"] == 7
    assert "m1" in obj["models"]


def test_csv_is_tidy_long_with_overall_element_micro(tmp_path):
    paths = write_table(_table(), tmp_path)
    with open(paths["csv"], newline="") as f:
        rows = list(csv.DictReader(f))
    # an overall element_f1 micro f1 row exists for the model
    hit = [r for r in rows if r["model_id"] == "m1" and r["scope"] == "overall"
           and r["metric"] == "element_f1" and r["population"] == "zeros_for_failed"
           and r["stat"] == "micro_f1"]
    assert len(hit) == 1
    assert abs(float(hit[0]["value"]) - (2 * (6 / 7) * 0.6 / ((6 / 7) + 0.6))) < 1e-9


def test_write_table_is_idempotent(tmp_path):
    p1 = write_table(_table(), tmp_path)
    first = {k: p1[k].read_text() for k in ("json", "md", "csv")}
    p2 = write_table(_table(), tmp_path)
    second = {k: p2[k].read_text() for k in ("json", "md", "csv")}
    assert first == second


def test_csv_has_population_gap_rows(tmp_path):
    paths = write_table(_table(), tmp_path)
    with open(paths["csv"], newline="") as f:
        rows = list(csv.DictReader(f))

    def cell(pop, stat="micro_f1", metric="element_f1"):
        return next(r for r in rows if r["model_id"] == "m1" and r["scope"] == "overall"
                    and r["metric"] == metric and r["population"] == pop and r["stat"] == stat)

    gap = cell("gap")
    z, c = cell("zeros_for_failed"), cell("compiled_only")
    assert abs(float(gap["value"]) - (float(c["value"]) - float(z["value"]))) < 1e-9


def test_markdown_has_population_gap_section(tmp_path):
    md = render_markdown(_table())
    assert "Population gap" in md
