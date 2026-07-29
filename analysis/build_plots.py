"""CLI: registry + Task-1/2 artifacts -> render the benchmark figures.

Reads the two emitted JSON artifacts (``master_table.json`` for point estimates +
model metadata, ``ci_table.json`` for error bars) and the run registry (the full
model inventory incl. pending rungs + their params/arm/family), then renders the
Task-3 figures under ``<out-dir>/<plots-subdir>/`` as PNG + PDF.

The artifacts are inputs -- regenerate them first if stale::

    python3 analysis/build_master_table.py
    python3 analysis/build_ci_table.py
    python3 analysis/build_plots.py                       # main panel
    python3 analysis/build_plots.py --include-supplementary   # + Sonnet figures

Incremental: a model with no entry in the artifacts (pending/in_progress) is
skipped and the figures are annotated "N/total". Idempotent: the Agg backend plus
pinned (timestamp-free) save-metadata makes a re-render byte-identical.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Allow direct execution as well as module execution: add the package root.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis.plots import render_all
from analysis.registry import DEFAULT_REGISTRY, load_registry, panel_entries

log = logging.getLogger("analysis.build_plots")

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "out"


def load_artifacts(out_dir: str | Path, *, master_basename: str = "master_table",
                   ci_basename: str = "ci_table") -> tuple[dict, dict]:
    """Read the master-table + CI-table JSON artifacts from ``out_dir``.

    Raises ``FileNotFoundError`` naming the builder to run when an artifact is
    absent (STOP-and-report rather than render an empty figure)."""
    out_dir = Path(out_dir)
    master_path = out_dir / f"{master_basename}.json"
    ci_path = out_dir / f"{ci_basename}.json"
    for path, builder in ((master_path, "build_master_table.py"),
                          (ci_path, "build_ci_table.py")):
        if not path.exists():
            raise FileNotFoundError(
                f"missing artifact {path} -- run `python3 analysis/{builder}` first")
    with open(master_path, encoding="utf-8") as f:
        master = json.load(f)
    with open(ci_path, encoding="utf-8") as f:
        ci = json.load(f)
    return master, ci


def load_crowding(out_dir: str | Path) -> dict | None:
    """Read ``crowding.json``'s ``lines_per_mp_by_tier`` (the Task-5 per-tier
    image-crowding descriptor) for the figure annotations, or ``None`` when the
    artifact is absent (figures render without the crowding annotation)."""
    path = Path(out_dir) / "crowding.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("lines_per_mp_by_tier")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render the benchmark's Task-3 figures.")
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR,
                    help="directory holding master_table.json / ci_table.json")
    ap.add_argument("--plots-subdir", default="plots",
                    help="subdirectory of --out-dir to write figures into")
    ap.add_argument("--include-supplementary", action="store_true",
                    help="also render figures for the supplementary artifacts (Sonnet)")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(levelname)s %(name)s: %(message)s")

    registry = load_registry(args.registry)
    plots_dir = args.out_dir / args.plots_subdir

    master, ci = load_artifacts(args.out_dir)
    crowding = load_crowding(args.out_dir)
    if crowding is None:
        log.warning("crowding.json not found in %s -- figures rendered without the "
                    "crowding annotation (run build_run_level.py to produce it)", args.out_dir)
    entries = panel_entries(registry)  # full inventory minus supplementary
    produced = render_all(entries, master, ci, plots_dir, crowding=crowding)
    log.info("rendered %d figures (%d/%d models) into %s",
             len(produced), master["meta"]["models_included"],
             master["meta"]["models_total"], plots_dir)
    print(f"Models included: {master['meta']['models_included']}/{master['meta']['models_total']}")
    for name, paths in produced.items():
        print(f"  {name}: {paths['png'].name}, {paths['pdf'].name}")

    if args.include_supplementary:
        try:
            s_master, s_ci = load_artifacts(args.out_dir,
                                            master_basename="master_table_supplementary",
                                            ci_basename="ci_table_supplementary")
        except FileNotFoundError as exc:
            log.warning("supplementary artifacts not found (%s) -- skipping", exc)
        else:
            s_entries = [e for e in registry if e.supplementary]
            s_dir = plots_dir / "supplementary"
            s_produced = render_all(s_entries, s_master, s_ci, s_dir, crowding=crowding)
            print(f"Supplementary included: "
                  f"{s_master['meta']['models_included']}/{s_master['meta']['models_total']}")
            for name, paths in s_produced.items():
                print(f"  {name}: {paths['png'].name}, {paths['pdf'].name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
