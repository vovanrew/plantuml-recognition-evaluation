"""Tests for the Phase-3 run-registry config (analysis/model_registry.json)."""
import json

import pytest

from analysis import registry
from analysis.registry import DEFAULT_REGISTRY, ModelEntry, load_registry, panel_entries


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


# --------------------------------------------------------------------------- #
# condition (zero_shot | fine_tuned)
# --------------------------------------------------------------------------- #

DENSE_LADDER = ["qwen3.5-2b", "qwen3.5-9b", "qwen3.5-27b"]


def _ladder_both_conditions() -> list[dict]:
    """The three dense rungs, each as a zero-shot and a fine-tuned entry. The
    fine-tuned stand-in copies the published entry and changes id, display and
    condition only."""
    with open(DEFAULT_REGISTRY, encoding="utf-8") as f:
        by_id = {m["id"]: m for m in json.load(f)["models"]}
    models = []
    for mid in DENSE_LADDER:
        models.append({**by_id[mid], "condition": "zero_shot"})
        models.append({**by_id[mid], "id": mid + "-ft",
                       "display": by_id[mid]["display"] + " (fine-tuned)",
                       "condition": "fine_tuned"})
    return models


def _write_registry(tmp_path, models: list[dict]):
    path = tmp_path / "registry.json"
    path.write_text(json.dumps({"models": models}), encoding="utf-8")
    return path


def test_published_entries_are_zero_shot_without_a_condition_key():
    with open(DEFAULT_REGISTRY, encoding="utf-8") as f:
        raw = json.load(f)["models"]
    assert all("condition" not in m for m in raw)  # the published entries are not edited
    assert [e.condition for e in load_registry()] == ["zero_shot"] * 8


def test_model_entry_built_without_condition_is_zero_shot():
    entry = ModelEntry(id="m", display="M", run_dir="r", status="scored", lab="qwen",
                       arm="qwen", family="dense", params_total_b=9, params_active_b=9,
                       supplementary=False)
    assert entry.condition == "zero_shot"


def test_ladder_registers_in_both_conditions(tmp_path):
    reg = load_registry(_write_registry(tmp_path, _ladder_both_conditions()))
    assert [e.id for e in reg] == [
        "qwen3.5-2b", "qwen3.5-2b-ft",
        "qwen3.5-9b", "qwen3.5-9b-ft",
        "qwen3.5-27b", "qwen3.5-27b-ft",
    ]
    assert [e.condition for e in reg] == ["zero_shot", "fine_tuned"] * 3
    # a fine-tuned run stays in its model's arm and family
    assert {e.arm for e in reg} == {"qwen"}
    assert {e.family for e in reg} == {"dense"}
    assert [e.params_total_b for e in reg] == [2, 2, 9, 9, 27, 27]


def test_condition_has_exactly_two_values():
    # the checks below reject by example; this pins the whole set
    assert registry._VALID_CONDITION == {"zero_shot", "fine_tuned"}
    assert registry.DEFAULT_CONDITION == "zero_shot"


@pytest.mark.parametrize("bad", ["finetuned", "fine-tuned", "Zero_Shot", "", None])
def test_unknown_condition_is_rejected(tmp_path, bad):
    models = _ladder_both_conditions()
    models[1]["condition"] = bad
    with pytest.raises(ValueError, match="qwen3.5-2b-ft: bad condition"):
        load_registry(_write_registry(tmp_path, models))


def test_condition_is_not_carried_by_arm(tmp_path):
    models = _ladder_both_conditions()
    models[1]["arm"] = "finetuned"
    with pytest.raises(ValueError, match="qwen3.5-2b-ft: bad arm"):
        load_registry(_write_registry(tmp_path, models))


def test_two_conditions_need_two_ids(tmp_path):
    models = _ladder_both_conditions()
    models[1]["id"] = models[0]["id"]
    with pytest.raises(ValueError, match="duplicate model id in registry: qwen3.5-2b"):
        load_registry(_write_registry(tmp_path, models))
