"""Run-registry: the single committed mapping of reported model -> run directory.

Every analysis task drives off this file. The author maintains it as runs finish
(see analysis/model_registry.json). Loading validates the minimal invariants the
pipeline relies on (unique ids, known status/arm/family values) and returns the
entries in reporting order.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

DEFAULT_REGISTRY = Path(__file__).with_name("model_registry.json")

_VALID_STATUS = {"scored", "in_progress", "pending"}
_VALID_ARM = {"frontier", "qwen"}
_VALID_FAMILY = {"dense", "moe"}


@dataclass(frozen=True)
class ModelEntry:
    """One reported (or pending) model and where its scored artifacts live."""

    id: str
    display: str
    run_dir: str | None
    status: str
    lab: str
    arm: str
    family: str
    params_total_b: float | None
    params_active_b: float | None
    supplementary: bool

    @property
    def is_pending(self) -> bool:
        """No run directory recorded yet -> nothing to load."""
        return not self.run_dir


def _parse_entry(d: dict) -> ModelEntry:
    return ModelEntry(
        id=d["id"],
        display=d["display"],
        run_dir=d.get("run_dir") or None,
        status=d["status"],
        lab=d["lab"],
        arm=d["arm"],
        family=d["family"],
        params_total_b=d.get("params_total_b"),
        params_active_b=d.get("params_active_b"),
        supplementary=bool(d.get("supplementary", False)),
    )


def load_registry(path: str | Path = DEFAULT_REGISTRY) -> list[ModelEntry]:
    """Load and validate the registry, preserving file (reporting) order."""
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    entries = [_parse_entry(d) for d in raw["models"]]

    seen: set[str] = set()
    for e in entries:
        if e.id in seen:
            raise ValueError(f"duplicate model id in registry: {e.id}")
        seen.add(e.id)
        if e.status not in _VALID_STATUS:
            raise ValueError(f"{e.id}: bad status {e.status!r} (want {_VALID_STATUS})")
        if e.arm not in _VALID_ARM:
            raise ValueError(f"{e.id}: bad arm {e.arm!r} (want {_VALID_ARM})")
        if e.family not in _VALID_FAMILY:
            raise ValueError(f"{e.id}: bad family {e.family!r} (want {_VALID_FAMILY})")
    return entries


def panel_entries(
    registry: list[ModelEntry], include_supplementary: bool = False
) -> list[ModelEntry]:
    """The reported panel in order. Supplementary models (Sonnet) are excluded
    unless explicitly requested."""
    if include_supplementary:
        return list(registry)
    return [e for e in registry if not e.supplementary]
