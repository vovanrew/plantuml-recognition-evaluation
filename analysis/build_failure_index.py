"""CLI: registry -> load+join -> reasoning_leak gate -> stratified failure sample -> emit.

Builds a reviewable failure-case index (markdown + CSV + JSON) under ``analysis/out/``
for the author's qualitative 30-50-case error write-up. Drives everything off
analysis/model_registry.json; pending/missing runs are skipped with a logged note and
a leaking run is refused, so a partial index is labelled "N/total". Read-only over
``data/``. Idempotent (fixed seed, sorted iteration).

    python3 analysis/build_failure_index.py                    # main 4/7 panel
    python3 analysis/build_failure_index.py --per-cell 2       # cap per cell (default 2)
    python3 analysis/build_failure_index.py --include-ok       # also sample compiled-ok cases
    python3 analysis/build_failure_index.py --include-supplementary   # + Sonnet index
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow direct execution as well as module execution: add the package root.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis import failure_sampler as fs
from analysis.loader import DEFAULT_DATA_ROOT
from analysis.panel import load_eligible_models
from analysis.registry import (
    DEFAULT_REGISTRY,
    ModelEntry,
    load_registry,
    panel_entries,
)

log = logging.getLogger("analysis.build_failure_index")

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "out"


def build_panel_index(
    entries: list[ModelEntry],
    data_root: Path,
    *,
    label: str,
    per_cell: int,
    threshold: float,
    include_ok: bool,
    seed: int,
    small_lines: int,
    snippet_lines: int,
) -> tuple[list[dict], dict]:
    """Load, leak-gate, and sample one panel into (records, meta)."""
    eligible, pending, refused = load_eligible_models(entries, data_root)
    records, meta = fs.build_index(
        eligible, models_total=len(entries), pending_ids=pending, refused_ids=refused,
        data_root=data_root, per_cell=per_cell, threshold=threshold,
        include_ok=include_ok, seed=seed, small_lines=small_lines,
        snippet_lines=snippet_lines, label=label)
    log.info("[%s] models included: %d/%d (pending: %s; refused: %s); %d cases, %d capped cell(s)",
             label, len(eligible), len(entries), ", ".join(pending) or "none",
             ", ".join(refused) or "none", meta["total_cases"], len(meta["capped_cells"]))
    return records, meta


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the benchmark failure-case index.")
    ap.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--basename", default="failure_index")
    ap.add_argument("--per-cell", type=int, default=2,
                    help="max cases per (model x type x tier x outcome class) cell")
    ap.add_argument("--low-structural-threshold", type=float, default=fs.LOW_STRUCTURAL_F1,
                    help="compiled rows with Element OR Relationship F1 below this are failures")
    ap.add_argument("--include-ok", action="store_true",
                    help="also sample compiled-ok cases (contrast cases; off by default)")
    ap.add_argument("--seed", type=int, default=fs.SEED)
    ap.add_argument("--small-diagram-lines", type=int, default=fs.SMALL_DIAGRAM_LINES,
                    help="inline GT+prediction text for GT at/under this many lines")
    ap.add_argument("--snippet-max-lines", type=int, default=fs.SNIPPET_MAX_LINES,
                    help="truncate inlined GT/prediction text to this many lines")
    ap.add_argument("--include-supplementary", action="store_true",
                    help="also emit a separate index for supplementary models (Sonnet)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(levelname)s %(name)s: %(message)s")

    registry = load_registry(args.registry)

    def _run(entries, label, basename):
        records, meta = build_panel_index(
            entries, args.data_root, label=label, per_cell=args.per_cell,
            threshold=args.low_structural_threshold, include_ok=args.include_ok,
            seed=args.seed, small_lines=args.small_diagram_lines,
            snippet_lines=args.snippet_max_lines)
        paths = fs.write_index(records, meta, args.out_dir, basename=basename)
        print(f"[{label}] models included: {meta['models_included']}/{meta['models_total']}; "
              f"{meta['total_cases']} cases")
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
