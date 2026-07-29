"""Shared panel loading + eligibility gate.

Every aggregator (master table, bootstrap CIs, future run-level tables) needs the
same front matter: load each registered run that is on disk, drop any model whose
predictions leak ``<think>`` (the reasoning_leak==0 gate), and report which
registered models are still pending vs refused so a partial result is labelled
"N/total". This factors that flow out so the loaders agree by construction.
"""
from __future__ import annotations

import logging
from pathlib import Path

from analysis.leak_gate import count_reasoning_leaks, predictions_dir
from analysis.loader import ModelData, load_panel
from analysis.registry import ModelEntry

log = logging.getLogger(__name__)


def load_eligible_models(
    entries: list[ModelEntry], data_root: str | Path
) -> tuple[list[ModelData], list[str], list[str]]:
    """Load + leak-gate ``entries``. Returns ``(eligible, pending_ids, refused_ids)``.

    ``eligible``  -- loaded models with zero reasoning leaks (reporting order).
    ``pending_ids`` -- registered runs not (yet) on disk (skipped, not an error).
    ``refused_ids`` -- runs present on disk but excluded by the leak gate.
    """
    data_root = Path(data_root)
    loaded = load_panel(entries, data_root)

    eligible: list[ModelData] = []
    refused: list[str] = []
    for md in loaded:
        leaks = count_reasoning_leaks(predictions_dir(data_root, md.entry.run_dir))
        if leaks:
            log.warning("REFUSED %s: %d prediction(s) contain <think> (reasoning_leak) "
                        "-- not scored", md.entry.id, leaks)
            refused.append(md.entry.id)
        else:
            eligible.append(md)

    included = {md.entry.id for md in eligible}
    refused_set = set(refused)
    pending = [e.id for e in entries if e.id not in included and e.id not in refused_set]
    return eligible, pending, refused
