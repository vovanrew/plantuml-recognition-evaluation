"""CLI: registry -> load+join -> reasoning_leak gate -> aggregate -> emit.

Drives everything off analysis/model_registry.json. Pending/missing runs are
skipped with a logged note; a run whose predictions leak ``<think>`` is refused
(never scored). Re-running after a model lands is idempotent.

    python3 analysis/build_master_table.py                 # main 7-model panel
    python3 analysis/build_master_table.py --include-supplementary   # + Sonnet table
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow direct execution (`python3 analysis/build_master_table.py`) as well as
# module execution (`python3 -m analysis.build_master_table`): when run as a
# script the package root is not on sys.path, so add it.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.aggregate import build_master_table
from analysis.loader import DEFAULT_DATA_ROOT
from analysis.panel import load_eligible_models
from analysis.registry import (
    DEFAULT_REGISTRY,
    ModelEntry,
    load_registry,
    panel_entries,
)
from analysis.report import write_table

log = logging.getLogger("analysis.build_master_table")

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "out"


def aggregate_panel(entries: list[ModelEntry], data_root: Path, label: str) -> dict:
    """Load, leak-gate, and aggregate one panel into a master table."""
    eligible, pending, refused = load_eligible_models(entries, data_root)
    table = build_master_table(
        eligible, models_total=len(entries), pending_ids=pending,
        refused_ids=refused, label=label,
    )
    log.info("[%s] models included: %d/%d (pending: %s; refused: %s)",
             label, len(eligible), len(entries),
             ", ".join(pending) or "none", ", ".join(refused) or "none")
    return table


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the benchmark master table.")
    ap.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--basename", default="master_table")
    ap.add_argument("--include-supplementary", action="store_true",
                    help="also emit a separate table for supplementary models (Sonnet)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(levelname)s %(name)s: %(message)s")

    registry = load_registry(args.registry)

    main_panel = panel_entries(registry)  # 7 models, Sonnet excluded
    table = aggregate_panel(main_panel, args.data_root, label="main")
    paths = write_table(table, args.out_dir, basename=args.basename)
    print(f"Models included: {table['meta']['models_included']}/{table['meta']['models_total']}")
    for kind, p in paths.items():
        print(f"  {kind}: {p}")

    if args.include_supplementary:
        supp = [e for e in registry if e.supplementary]
        if supp:
            stable = aggregate_panel(supp, args.data_root, label="supplementary")
            spaths = write_table(stable, args.out_dir, basename=f"{args.basename}_supplementary")
            print(f"Supplementary included: "
                  f"{stable['meta']['models_included']}/{stable['meta']['models_total']}")
            for kind, p in spaths.items():
                print(f"  {kind}: {p}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
