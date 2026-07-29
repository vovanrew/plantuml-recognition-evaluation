"""CLI: registry -> load+join -> reasoning_leak gate -> reconcile gate -> run-level tables.

Drives the Task-5 run-level aggregator off ``analysis/model_registry.json`` and
reads SOURCE B (``data/runs/<run>/`` raw API responses + ``run_meta.json``), not the
metric JSONs. Emits, under ``analysis/out/``:

  - ``run_level.{json,md,csv}``      -- per-model token totals (all cells incl.
                                        failures), failure/outcome inventory
                                        (provider vs compile-fail), provenance manifest.
  - ``crowding.{json,csv}``          -- the model-independent per-tier crowding
                                        descriptor (content_lines per MP after 1568px
                                        resize), the Task-3 ``crowding=`` hook.

A model present on disk but whose source-B no-response count does not reconcile with
source A's ``has_pred==false`` (the run dir was resumed after scoring) is excluded
with a logged note and listed in the report -- the gate is self-correcting (re-score
to include). Pending/missing runs are skipped; a leaking run is refused. Read-only
over ``data/``; idempotent (sorted iteration, no timestamps); no new dependency.

    python3 analysis/build_run_level.py
    python3 analysis/build_run_level.py --include-supplementary   # + Sonnet table
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow direct execution as well as module execution: add the package root.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis import run_level as rl
from analysis.loader import DEFAULT_DATA_ROOT
from analysis.panel import load_eligible_models
from analysis.registry import (
    DEFAULT_REGISTRY,
    ModelEntry,
    load_registry,
    panel_entries,
)

log = logging.getLogger("analysis.build_run_level")

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "out"


def build_panel(entries: list[ModelEntry], data_root: Path, *, label: str):
    """Load, leak-gate, reconcile-gate, and assemble one panel into (records, meta)."""
    eligible, pending, refused = load_eligible_models(entries, data_root)
    records, meta = rl.build_run_level(
        eligible, models_total=len(entries), pending_ids=pending,
        refused_ids=refused, data_root=data_root, label=label)
    return records, meta


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the run-level aggregator tables.")
    ap.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--basename", default="run_level")
    ap.add_argument("--include-supplementary", action="store_true",
                    help="also emit a separate run-level table for supplementary models (Sonnet)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(levelname)s %(name)s: %(message)s")

    registry = load_registry(args.registry)

    # crowding descriptor is model-independent -> build + write once
    crowding = rl.load_crowding(args.data_root / "test_set.json",
                                args.data_root / "puml_images_1568")
    cpaths = rl.write_crowding(crowding, args.out_dir)
    print(f"[crowding] {crowding['n']} diagrams; lines/MP by tier "
          f"{ {t: round(v, 2) for t, v in crowding['lines_per_mp_by_tier'].items()} }")
    for kind, p in cpaths.items():
        print(f"  {kind}: {p}")

    def _run(entries, label, basename):
        records, meta = build_panel(entries, args.data_root, label=label)
        paths = rl.write_run_level(records, meta, args.out_dir,
                                   basename=basename, crowding=crowding)
        print(f"[{label}] models included: {meta['models_included']}/{meta['models_total']}"
              f" (pending: {', '.join(meta['pending_ids']) or 'none'}; "
              f"desynced: {', '.join(meta['desynced_ids']) or 'none'})")
        for kind, p in paths.items():
            print(f"  {kind}: {p}")

    _run(panel_entries(registry), "main", args.basename)   # 7-model panel, Sonnet excluded

    if args.include_supplementary:
        supp = [e for e in registry if e.supplementary]
        if supp:
            _run(supp, "supplementary", f"{args.basename}_supplementary")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
