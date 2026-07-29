"""Task-5 run-level aggregator: unit tests on tiny synthetic source-B fixtures.

No network and no real ``data/`` reads here -- the token extractor, the
PNG-dimension reader, the reconcile/inventory logic, the provenance manifest and
the crowding descriptor are all exercised on hand-built fixtures (synth.py). A
separate smoke test drives the emitters. The real-data build + reconcile cross-check
runs in build_run_level.py against disk.
"""
import struct

import pytest

import synth
from analysis import run_level as rl


# --------------------------------------------------------------------------- #
# PNG-dimension reader (stdlib struct, no Pillow)
# --------------------------------------------------------------------------- #

def test_png_dims_reads_ihdr_width_height(tmp_path):
    p = tmp_path / "x.png"
    p.write_bytes(synth.png_header_bytes(685, 512))
    assert rl.read_png_dims(p) == (685, 512)


def test_png_dims_square_and_large(tmp_path):
    p = tmp_path / "x.png"
    p.write_bytes(synth.png_header_bytes(1568, 1568))
    assert rl.read_png_dims(p) == (1568, 1568)


def test_png_dims_rejects_non_png(tmp_path):
    p = tmp_path / "bad.png"
    p.write_bytes(b"not a png file at all............")
    with pytest.raises(ValueError):
        rl.read_png_dims(p)


def test_png_dims_rejects_truncated_header(tmp_path):
    p = tmp_path / "short.png"
    p.write_bytes(synth.png_header_bytes(100, 100)[:20])  # < 24 bytes
    with pytest.raises(ValueError):
        rl.read_png_dims(p)


# --------------------------------------------------------------------------- #
# token extractor: OpenAI vs Gemini usage shapes, error -> 0, no double count
# --------------------------------------------------------------------------- #

def test_read_cell_openai_success():
    rec = synth.srcb_openai(prompt=120, completion=340)
    out = rl.read_cell(rec)
    assert out == {"status": "ok", "input": 120, "output": 340, "reasoning": 0}


def test_read_cell_openai_reasoning_not_double_counted():
    # GPT completion_tokens ALREADY includes the reasoning subtotal -> output stays
    # completion_tokens; reasoning is reported separately, never added on top.
    rec = synth.srcb_openai(prompt=100, completion=500, reasoning=120)
    out = rl.read_cell(rec)
    assert out["output"] == 500          # NOT 500 + 120
    assert out["reasoning"] == 120
    assert out["input"] == 100


def test_read_cell_gemini_output_is_candidates_plus_thoughts():
    rec = synth.srcb_gemini(prompt=200, candidates=300, thoughts=80)
    out = rl.read_cell(rec)
    assert out == {"status": "ok", "input": 200, "output": 380, "reasoning": 80}


def test_read_cell_gemini_absent_thoughts_is_zero():
    rec = synth.srcb_gemini(prompt=200, candidates=300, thoughts=None)
    out = rl.read_cell(rec)
    assert out["reasoning"] == 0
    assert out["output"] == 300


def test_read_cell_error_record_is_zero_tokens():
    rec = synth.srcb_error(category="timeout", key="d7")
    out = rl.read_cell(rec)
    assert out == {"status": "timeout", "input": 0, "output": 0, "reasoning": 0}


def test_read_cell_http_error_category_preserved():
    out = rl.read_cell(synth.srcb_error(category="http_error"))
    assert out["status"] == "http_error"
    assert (out["input"], out["output"], out["reasoning"]) == (0, 0, 0)


def test_read_cell_image_dropped_counts_nested_usage():
    # image_dropped kept the provider response under .response -> its usage is billed
    rec = synth.srcb_image_dropped(key="d9", prompt=93, completion=5376)
    out = rl.read_cell(rec)
    assert out["status"] == "image_dropped"
    assert out["input"] == 93
    assert out["output"] == 5376


def test_read_cell_unrecognized_shape_raises():
    # a non-error record with no usage/usageMetadata is a schema surprise -> STOP
    with pytest.raises(ValueError):
        rl.read_cell({"id": "x", "object": "chat.completion"})


# --------------------------------------------------------------------------- #
# run-dir reader: sums tokens over ALL cells incl. failures; counts statuses
# --------------------------------------------------------------------------- #

def _write_mixed_run(tmp_path):
    records = {
        "d1": synth.srcb_openai(prompt=100, completion=200),
        "d2": synth.srcb_gemini(prompt=50, candidates=60, thoughts=10),
        "d3": synth.srcb_error(category="timeout", key="d3"),
        "d4": synth.srcb_image_dropped(key="d4", prompt=93, completion=5376),
    }
    return synth.write_run_dir(tmp_path, "run_x", records, synth.run_meta())


def test_read_run_usage_sums_over_all_cells_incl_failures(tmp_path):
    run_dir = _write_mixed_run(tmp_path)
    u = rl.read_run_usage(run_dir)
    assert u["n_cells"] == 4
    assert u["n_ok"] == 2
    assert u["n_error"] == 2
    assert u["input"] == 100 + 50 + 0 + 93                # error -> 0; image_dropped counts
    assert u["output"] == 200 + (60 + 10) + 0 + 5376      # gemini = candidates + thoughts
    assert u["reasoning"] == 0 + 10 + 0 + 0


def test_read_run_usage_status_counts(tmp_path):
    run_dir = _write_mixed_run(tmp_path)
    u = rl.read_run_usage(run_dir)
    assert u["status_counts"] == {"ok": 2, "timeout": 1, "image_dropped": 1}


def test_read_run_usage_ignores_run_meta(tmp_path):
    run_dir = synth.write_run_dir(
        tmp_path, "run_y", {"d1": synth.srcb_openai()}, synth.run_meta())
    u = rl.read_run_usage(run_dir)
    assert u["n_cells"] == 1               # run_meta.json not counted as a cell


# --------------------------------------------------------------------------- #
# reconcile: source-B no-response must equal source-A has_pred==false
# --------------------------------------------------------------------------- #

def _md_with_drops(n_drops):
    """A 4-row model with ``n_drops`` provider-drop rows (has_pred False)."""
    rows = []
    for i in range(4):
        drop = i < n_drops
        rows.append(synth.make_row(
            f"d{i}", "class", 1, compiled=not drop, el=(1, 0, 0), rel=(1, 0, 0),
            chrf=10.0, ta=(1, 1, 0), has_pred=not drop,
            csr_error="no prediction (missing/timeout)" if drop else None))
    from analysis.loader import ModelData
    from analysis.registry import ModelEntry
    entry = ModelEntry(id="m", display="M", run_dir="r", status="scored", lab="qwen",
                       arm="qwen", family="dense", params_total_b=9, params_active_b=9,
                       supplementary=False)
    summaries = {"csr": {"n": 4, "compiled": 4 - n_drops, "csr": (4 - n_drops) / 4}}
    return ModelData(entry=entry, rows=rows, summaries=summaries)


def test_reconcile_ok_when_counts_match():
    md = _md_with_drops(2)
    rec = rl.reconcile(md, {"n_error": 2})
    assert rec["ok"] is True
    assert rec["source_a_has_pred_false"] == 2
    assert rec["source_b_no_response"] == 2


def test_reconcile_flags_desync():
    md = _md_with_drops(2)                  # source A says 2 drops
    rec = rl.reconcile(md, {"n_error": 1})  # source B has only 1 (resumed one)
    assert rec["ok"] is False
    assert rec["source_a_has_pred_false"] == 2
    assert rec["source_b_no_response"] == 1


# --------------------------------------------------------------------------- #
# failure inventory: provider (source B) vs model compile-fail (source A CSR)
# --------------------------------------------------------------------------- #

def test_failure_inventory_splits_provider_and_compile_fail():
    # 10 cells: 6 compiled, 2 provider drops (timeout), 2 compile-fail.
    md = _md_with_drops(0)
    md.summaries["csr"] = {"n": 10, "compiled": 6, "csr": 0.6}
    # patch rows: 2 provider drops
    for i in range(2):
        md.rows[i]["element"]["has_pred"] = False
    run_usage = {"n_error": 2, "status_counts": {"ok": 8, "timeout": 2}}
    inv = rl.failure_inventory(md, run_usage)
    assert inv["no_response"] == 2
    assert inv["compile_fail"] == (10 - 6) - 2          # non-compiled minus drops
    assert inv["compiled"] == 6
    assert inv["provider_failures"]["timeout"] == 2
    assert inv["provider_failures"]["http_error"] == 0  # category always present, zero
    assert inv["partition_ok"] is True                  # compiled + compile_fail + no_response == n
    assert inv["reconcile"]["ok"] is True


# --------------------------------------------------------------------------- #
# provenance manifest from run_meta.json (+ re-derived reasoning_leak count)
# --------------------------------------------------------------------------- #

def test_provenance_record_picks_reproducibility_fields():
    meta = synth.run_meta(model="gpt-5.2-2025-12-11", provider="openai",
                          extra_body={"reasoning_effort": "none"}, started="20260613T154248Z")
    prov = rl.provenance_record(meta, leak_count=0)
    assert prov["model"] == "gpt-5.2-2025-12-11"
    assert prov["provider"] == "openai"
    assert prov["extra_body"] == {"reasoning_effort": "none"}
    assert prov["max_tokens"] == 5376
    assert prov["temperature"] == 0
    assert prov["started"] == "20260613T154248Z"
    assert prov["reasoning_leak"] == 0


def test_provenance_record_keeps_gemini_thinking_config():
    meta = synth.run_meta(model="gemini-3.1-pro-preview", provider="gemini",
                          extra_body={"thinkingConfig": {"thinkingLevel": "low"}})
    prov = rl.provenance_record(meta, leak_count=0)
    assert prov["extra_body"] == {"thinkingConfig": {"thinkingLevel": "low"}}
    assert prov["provider"] == "gemini"


# --------------------------------------------------------------------------- #
# crowding descriptor: content_lines per MP after the 1568px resize (PNG dims)
# --------------------------------------------------------------------------- #

_CROWD_DIAGRAMS = [
    {"key": "a.puml", "primary_type": "class", "tier": 1, "content_lines": 10},
    {"key": "b.puml", "primary_type": "class", "tier": 1, "content_lines": 20},
    {"key": "c.puml", "primary_type": "sequence", "tier": 2, "content_lines": 30},
]
_CROWD_DIMS = {"a": (1000, 1000), "b": (1000, 2000), "c": (500, 1000)}  # MP 1.0, 2.0, 0.5


def test_crowding_pooled_lines_per_mp_per_tier():
    cr = rl.crowding_descriptor(_CROWD_DIAGRAMS, _CROWD_DIMS)
    # tier 1: lines 30 / mp 3.0 = 10.0 ; tier 2: lines 30 / mp 0.5 = 60.0
    assert cr["by_tier"][1]["lines_per_mp"] == pytest.approx(10.0)
    assert cr["by_tier"][2]["lines_per_mp"] == pytest.approx(60.0)
    assert cr["by_tier"][1]["n"] == 2
    assert cr["by_tier"][1]["mp"] == pytest.approx(3.0)


def test_crowding_task3_consumable_shape_string_tier_keys():
    cr = rl.crowding_descriptor(_CROWD_DIAGRAMS, _CROWD_DIMS)
    # Task-3 fig_*(crowding={tier: lines_per_mp}) expects string tier keys.
    assert cr["lines_per_mp_by_tier"] == {"1": pytest.approx(10.0), "2": pytest.approx(60.0)}


def test_crowding_per_type_tier():
    cr = rl.crowding_descriptor(_CROWD_DIAGRAMS, _CROWD_DIMS)
    assert cr["by_type_tier"]["class"][1]["lines_per_mp"] == pytest.approx(10.0)
    assert cr["by_type_tier"]["sequence"][2]["lines_per_mp"] == pytest.approx(60.0)


def test_crowding_missing_dim_raises():
    # a test-set key with no PNG on disk is a schema surprise -> STOP
    with pytest.raises(KeyError):
        rl.crowding_descriptor(_CROWD_DIAGRAMS, {"a": (1, 1), "b": (1, 1)})  # 'c' missing


def test_load_crowding_reads_pngs_from_disk(tmp_path):
    images = tmp_path / "puml_images_1568"
    images.mkdir()
    for key, (w, h) in _CROWD_DIMS.items():
        (images / f"{key}.png").write_bytes(synth.png_header_bytes(w, h))
    ts = tmp_path / "test_set.json"
    import json
    ts.write_text(json.dumps({"diagrams": _CROWD_DIAGRAMS}), encoding="utf-8")
    cr = rl.load_crowding(ts, images)
    assert cr["by_tier"][1]["lines_per_mp"] == pytest.approx(10.0)
    assert cr["lines_per_mp_by_tier"]["2"] == pytest.approx(60.0)


# --------------------------------------------------------------------------- #
# per-model record assembly + the disk-driven build (reconcile inclusion gate)
# --------------------------------------------------------------------------- #

def _make_md(mid, run_dir, n_drops, n, compiled):
    from analysis.loader import ModelData
    from analysis.registry import ModelEntry
    rows = []
    for i in range(n):
        drop = i < n_drops
        rows.append(synth.make_row(
            f"d{i}", "class", 1, compiled=(i < compiled), el=(1, 0, 0), rel=(1, 0, 0),
            chrf=10.0, ta=(1, 1, 0), has_pred=not drop,
            csr_error="no prediction (missing/timeout)" if drop else None))
    entry = ModelEntry(id=mid, display=mid.upper(), run_dir=run_dir, status="scored",
                       lab="qwen", arm="qwen", family="dense", params_total_b=9,
                       params_active_b=9, supplementary=False)
    return ModelData(entry=entry, rows=rows,
                     summaries={"csr": {"n": n, "compiled": compiled, "csr": compiled / n}})


def test_model_run_record_assembles_tokens_failures_provenance():
    md = synth.synth_model(mid="m1", display="M1")
    run_usage = {"n_cells": 4, "n_ok": 4, "n_error": 0, "status_counts": {"ok": 4},
                 "input": 1000, "output": 2000, "reasoning": 0}
    rec = rl.model_run_record(md, run_usage, synth.run_meta(model="m1"), leak_count=0)
    assert rec["model_id"] == "m1"
    assert rec["tokens"]["input"] == 1000
    assert rec["tokens"]["total"] == 3000
    assert rec["failures"]["compiled"] == 3
    assert rec["failures"]["compile_fail"] == 1          # (4-3) non-compiled, 0 drops
    assert rec["provenance"]["model"] == "m1"
    assert rec["provenance"]["reasoning_leak"] == 0


def test_build_run_level_excludes_desynced_model(tmp_path):
    data_root = tmp_path
    # good: source A 0 drops, source B 0 errors -> reconciles
    good = _make_md("good", "good_run", n_drops=0, n=2, compiled=2)
    synth.write_run_dir(data_root, "good_run",
                        {"d0": synth.srcb_openai(), "d1": synth.srcb_openai()},
                        synth.run_meta(model="good"))
    # bad: source A 1 drop, but source B has 0 errors (resumed) -> desync, excluded
    bad = _make_md("bad", "bad_run", n_drops=1, n=2, compiled=1)
    synth.write_run_dir(data_root, "bad_run",
                        {"d0": synth.srcb_openai(), "d1": synth.srcb_openai()},
                        synth.run_meta(model="bad"))

    records, meta = rl.build_run_level(
        [good, bad], models_total=3, pending_ids=["pend"], refused_ids=[],
        data_root=data_root, label="main")

    assert meta["models_included"] == 1
    assert meta["included_ids"] == ["good"]
    assert meta["desynced_ids"] == ["bad"]
    assert meta["pending_ids"] == ["pend"]
    assert [r["model_id"] for r in records] == ["good"]
    # the desync detail is carried for the report
    assert meta["desynced"][0]["model_id"] == "bad"
    assert meta["desynced"][0]["source_a_has_pred_false"] == 1
    assert meta["desynced"][0]["source_b_no_response"] == 0


# --------------------------------------------------------------------------- #
# emitters: non-empty md/csv/json + crowding artifact, byte-identical on re-run
# --------------------------------------------------------------------------- #

def _tiny_panel(tmp_path):
    data_root = tmp_path
    good = _make_md("good", "good_run", n_drops=0, n=2, compiled=2)
    synth.write_run_dir(data_root, "good_run",
                        {"d0": synth.srcb_openai(), "d1": synth.srcb_openai()},
                        synth.run_meta(model="good"))
    records, meta = rl.build_run_level(
        [good], models_total=2, pending_ids=["pend"], refused_ids=[],
        data_root=data_root, label="main")
    crowding = rl.crowding_descriptor(_CROWD_DIAGRAMS, _CROWD_DIMS)
    return records, meta, crowding


def test_write_run_level_emits_nonempty_md_csv_json(tmp_path):
    records, meta, crowding = _tiny_panel(tmp_path)
    out = tmp_path / "out"
    paths = rl.write_run_level(records, meta, out, basename="run_level")
    for kind in ("md", "csv", "json"):
        assert paths[kind].exists() and paths[kind].stat().st_size > 0
    import json
    blob = json.loads(paths["json"].read_text())
    assert blob["meta"]["models_included"] == 1
    assert blob["models"][0]["model_id"] == "good"


def test_write_crowding_emits_artifact(tmp_path):
    _, _, crowding = _tiny_panel(tmp_path)
    out = tmp_path / "out"
    paths = rl.write_crowding(crowding, out)
    assert paths["json"].exists() and paths["json"].stat().st_size > 0
    assert paths["csv"].exists() and paths["csv"].stat().st_size > 0


def test_emitters_byte_identical_on_rerun(tmp_path):
    records, meta, crowding = _tiny_panel(tmp_path)
    out = tmp_path / "out"
    p1 = rl.write_run_level(records, meta, out)
    first = {k: v.read_bytes() for k, v in p1.items()}
    pc1 = rl.write_crowding(crowding, out)
    first_c = {k: v.read_bytes() for k, v in pc1.items()}
    # re-run
    p2 = rl.write_run_level(records, meta, out)
    pc2 = rl.write_crowding(crowding, out)
    assert all(p2[k].read_bytes() == first[k] for k in first)
    assert all(pc2[k].read_bytes() == first_c[k] for k in first_c)


# --------------------------------------------------------------------------- #
# integration on real source B (skips when run data is absent). Asserts the
# reconcile cross-check + partition INVARIANTS for whatever panel is on disk --
# robust to the live qwen-9b resume (it verifies the gate, not a pinned roster).
# --------------------------------------------------------------------------- #

from analysis.loader import DEFAULT_DATA_ROOT  # noqa: E402
from analysis.panel import load_eligible_models  # noqa: E402
from analysis.registry import load_registry, panel_entries  # noqa: E402

_DATA = DEFAULT_DATA_ROOT
_REG = {e.id: e for e in load_registry()}


def _have_run_data():
    for mid in ("gpt-5.2", "claude-opus-4-6", "qwen3.5-2b"):
        rd = _REG[mid].run_dir
        if not rd or not (_DATA / "runs" / rd / "run_meta.json").exists():
            return False
        if not (_DATA / "element_f1" / rd / "element_f1_results.json").exists():
            return False
    return True


@pytest.mark.skipif(not _have_run_data(), reason="scored run data not on disk")
def test_real_panel_reconcile_and_partition_invariants():
    entries = panel_entries(load_registry())
    eligible, pending, refused = load_eligible_models(entries, _DATA)
    records, meta = rl.build_run_level(
        eligible, models_total=len(entries), pending_ids=pending,
        refused_ids=refused, data_root=_DATA, label="main")

    by_id = {md.entry.id: md for md in eligible}
    for r in records:
        f = r["failures"]
        # every INCLUDED model reconciles and its three outcome classes partition n
        assert f["reconcile"]["ok"], f"{r['model_id']} included but reconcile failed"
        assert f["partition_ok"], f"{r['model_id']} partition broken"
        # no_response equals this model's own source-A has_pred==false (self-consistent)
        src_a = sum(1 for row in by_id[r["model_id"]].rows if not row["element"]["has_pred"])
        assert f["no_response"] == src_a == f["reconcile"]["source_a_has_pred_false"]
        assert f["compiled"] + f["compile_fail"] + f["no_response"] == f["n"]

    # the two final frontier runs are always present (not subject to resume)
    assert "gpt-5.2" in meta["included_ids"]
    assert "claude-opus-4-6" in meta["included_ids"]


@pytest.mark.skipif(not _have_run_data(), reason="standardized images not on disk")
def test_real_crowding_monotonic_across_tiers():
    cr = rl.load_crowding(_DATA / "test_set.json", _DATA / "puml_images_1568")
    tiers = sorted(cr["by_tier"])
    assert tiers == [1, 2, 3, 4]
    lpm = [cr["by_tier"][t]["lines_per_mp"] for t in tiers]
    # crowding (content_lines per MP) increases with tier -- the degradation story
    assert all(a < b for a, b in zip(lpm, lpm[1:])), lpm
