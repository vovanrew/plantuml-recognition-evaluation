"""CLI: registry -> load+gate -> paired bootstrap -> emit CI table.

Drives everything off analysis/model_registry.json (the same registry + eligibility
gate as the master table). Pending/missing runs are skipped with a logged note; a
run whose predictions leak ``<think>`` is refused. The fixed seed makes re-runs
byte-identical, so re-running after a model lands is idempotent.

    python3 analysis/build_ci_table.py                 # main panel
    python3 analysis/build_ci_table.py --include-supplementary   # + Sonnet table
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow direct execution as well as module execution: add the package root.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.bootstrap import N_RESAMPLES, SEED, bootstrap_models
from analysis.ci_report import write_ci_table
from analysis.loader import DEFAULT_DATA_ROOT
from analysis.panel import load_eligible_models
from analysis.registry import (
    DEFAULT_REGISTRY,
    ModelEntry,
    load_registry,
    panel_entries,
)

log = logging.getLogger("analysis.build_ci_table")

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "out"


def bootstrap_panel(entries: list[ModelEntry], data_root: Path, *,
                    n_resamples: int, seed: int) -> dict:
    """Load, leak-gate, and bootstrap one panel into a CI table."""
    eligible, pending, refused = load_eligible_models(entries, data_root)
    result = bootstrap_models(
        eligible, n_resamples=n_resamples, seed=seed,
        models_total=len(entries), pending_ids=pending, refused_ids=refused,
    )
    log.info("models included: %d/%d (pending: %s; refused: %s)",
             len(eligible), len(entries),
             ", ".join(pending) or "none", ", ".join(refused) or "none")
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the benchmark paired-bootstrap CI table.")
    ap.add_argument("--data-root", type=Path, default=DEFAULT_DATA_ROOT)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--basename", default="ci_table")
    ap.add_argument("--n-resamples", type=int, default=N_RESAMPLES)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--include-supplementary", action="store_true",
                    help="also emit a separate CI table for supplementary models (Sonnet)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(levelname)s %(name)s: %(message)s")

    registry = load_registry(args.registry)

    main_panel = panel_entries(registry)  # Sonnet excluded
    result = bootstrap_panel(main_panel, args.data_root,
                             n_resamples=args.n_resamples, seed=args.seed)
    paths = write_ci_table(result, args.out_dir, basename=args.basename)
    print(f"Models included: {result['meta']['models_included']}/{result['meta']['models_total']}")
    for kind, p in paths.items():
        print(f"  {kind}: {p}")

    if args.include_supplementary:
        supp = [e for e in registry if e.supplementary]
        if supp:
            sresult = bootstrap_panel(supp, args.data_root,
                                      n_resamples=args.n_resamples, seed=args.seed)
            spaths = write_ci_table(sresult, args.out_dir, basename=f"{args.basename}_supplementary")
            print(f"Supplementary included: "
                  f"{sresult['meta']['models_included']}/{sresult['meta']['models_total']}")
            for kind, p in spaths.items():
                print(f"  {kind}: {p}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
