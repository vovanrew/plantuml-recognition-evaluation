"""Tests for the Phase-3 run-registry config (analysis/model_registry.json)."""
from analysis.registry import load_registry, panel_entries


PANEL_ORDER = [
    "gpt-5.2",
    "claude-opus-4-6",
    "gemini-3.1-pro",
    "qwen3.5-2b",
    "qwen3.5-9b",
    "qwen3.5-27b",
    "qwen3.5-397b-a17b",
]


def test_registry_has_seven_panel_models_plus_sonnet():
    reg = load_registry()
    assert len(reg) == 8  # 7 panel + 1 supplementary (Sonnet)
    panel = panel_entries(reg)  # default: supplementary excluded
    assert len(panel) == 7
    assert all(not e.supplementary for e in panel)


def test_panel_order_is_frontier_then_qwen_ladder():
    panel = panel_entries(load_registry())
    assert [e.id for e in panel] == PANEL_ORDER
    assert [e.arm for e in panel] == ["frontier"] * 3 + ["qwen"] * 4


def test_sonnet_supplementary_off_by_default_on_when_flagged():
    reg = load_registry()
    sonnet = next(e for e in reg if "sonnet" in e.id)
    assert sonnet.supplementary is True
    assert sonnet.id not in {e.id for e in panel_entries(reg)}
    assert sonnet.id in {e.id for e in panel_entries(reg, include_supplementary=True)}


def test_scored_models_have_run_dirs():
    by_id = {e.id: e for e in load_registry()}
    assert by_id["gpt-5.2"].run_dir == "gpt-5.2-2025-12-11_20260613T154248Z"
    assert by_id["gpt-5.2"].status == "scored"
    assert by_id["claude-opus-4-6"].run_dir == "claude-opus-4-6_20260614T081502Z"
    assert by_id["qwen3.5-2b"].run_dir == "Qwen_Qwen3.5-2B_20260613T153655Z"
    assert by_id["qwen3.5-9b"].run_dir == "Qwen_Qwen3.5-9B_20260613T202001Z"
    assert by_id["qwen3.5-27b"].run_dir == "Qwen_Qwen3.5-27B_20260613T202731Z"
    assert by_id["qwen3.5-27b"].status == "scored"
    assert by_id["gemini-3.1-pro"].status == "scored"


def test_moe_scored_on_first_party_serving():
    by_id = {e.id: e for e in load_registry()}
    # 397B-A17B: measured on first-party serving (OpenRouter pinned to the Alibaba backend)
    # rather than the shared host used for the dense sizes; registered and included.
    moe = by_id["qwen3.5-397b-a17b"]
    assert moe.status == "scored"
    assert moe.run_dir == "qwen3.5-397b-a17b-openrouter-alibaba_20260628T095506Z"


def test_moe_entry_carries_total_and_active_params():
    by_id = {e.id: e for e in load_registry()}
    moe = by_id["qwen3.5-397b-a17b"]
    assert moe.family == "moe"
    assert moe.params_total_b == 397
    assert moe.params_active_b == 17
    # dense rungs: active == total
    dense9 = by_id["qwen3.5-9b"]
    assert dense9.family == "dense"
    assert dense9.params_total_b == 9
    assert dense9.params_active_b == 9
