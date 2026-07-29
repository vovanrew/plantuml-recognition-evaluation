"""reasoning_leak==0 eligibility gate.

Non-thinking mode is frozen per model (methodology/benchmark-protocol.md §3); a run
that leaks chain-of-thought must not be scored. The per-run leak tally is not
persisted, so it is re-derived here by scanning the run's extracted ``.puml``
predictions for a ``<think>`` block. Any model with a non-zero count is refused
by the aggregator (with a logged note).
"""
from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)

THINK_MARKER = "<think>"


def predictions_dir(data_root: str | Path, run_dir: str) -> Path:
    """Where a run's extracted predictions live: data_root/runs/<run_dir>/."""
    return Path(data_root) / "runs" / run_dir


def count_reasoning_leaks(pred_dir: str | Path) -> int:
    """Number of ``*.puml`` predictions in ``pred_dir`` that contain a ``<think>``
    block. A missing directory counts as zero (the caller logs the skip)."""
    pred_dir = Path(pred_dir)
    if not pred_dir.is_dir():
        return 0
    leaks = 0
    for p in sorted(pred_dir.glob("*.puml")):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError as e:  # pragma: no cover - unexpected IO failure
            log.warning("could not read %s: %s", p, e)
            continue
        if THINK_MARKER in text:
            leaks += 1
    return leaks
