"""CLI: assemble the validated Task-1..5 artifacts into the paper's exhibits.

Reads (read-only) the artifacts in ``analysis/out/`` and emits a consolidated
paper-facing results document in two formats::

    python3 analysis/build_master_table.py
    python3 analysis/build_ci_table.py
    python3 analysis/build_run_level.py     # also produces crowding.json
    python3 analysis/build_failure_index.py # optional (Exhibit 8 coverage)
    python3 analysis/build_exhibits.py      # this step

Outputs under ``--out-dir`` (default ``analysis/out/``):
  * ``exhibits.md``   -- the consolidated results document + narrative skeleton
  * ``exhibits.html`` -- the same document, Word-importable (its tables paste
    straight into Microsoft Word as editable tables)

master_table.json and ci_table.json are required (STOP-and-report if absent);
run_level.json / crowding.json / failure_index.json are optional enrichments — a
missing one is logged and the corresponding exhibit is omitted, never faked.
Idempotent: no timestamps, artifact (registry) iteration order, byte-identical
re-runs for unchanged inputs.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from analysis import exhibits

log = logging.getLogger("analysis.build_exhibits")

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "out"


def _load_required(out_dir: Path, basename: str, builder: str) -> dict:
    path = out_dir / f"{basename}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"missing artifact {path} -- run `python3 analysis/{builder}` first")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_optional(out_dir: Path, basename: str):
    path = out_dir / f"{basename}.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Assemble paper-ready exhibits.")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR,
                    help="directory holding the input artifacts and receiving the exhibits")
    ap.add_argument("--master-basename", default="master_table")
    ap.add_argument("--ci-basename", default="ci_table")
    ap.add_argument("--run-level-basename", default="run_level")
    ap.add_argument("--failure-basename", default="failure_index")
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args(argv)

    logging.basicConfig(level=args.log_level, format="%(levelname)s %(name)s: %(message)s")
    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    master = _load_required(out_dir, args.master_basename, "build_master_table.py")
    ci = _load_required(out_dir, args.ci_basename, "build_ci_table.py")
    run_level = _load_optional(out_dir, args.run_level_basename)
    failure = _load_optional(out_dir, args.failure_basename)
    crowding_raw = _load_optional(out_dir, "crowding")
    crowding = crowding_raw.get("lines_per_mp_by_tier") if crowding_raw else None

    for name, obj in (("run_level", run_level), ("crowding", crowding_raw),
                      ("failure_index", failure)):
        if obj is None:
            log.warning("optional artifact %s.json absent -- its exhibit is omitted", name)

    # consistency note: the CI and master panels should agree (both 7/7).
    if master["meta"]["models_included"] != ci["meta"]["models_included"]:
        log.warning("master panel (%d) != CI panel (%d) -- exhibits mix populations",
                    master["meta"]["models_included"], ci["meta"]["models_included"])

    md = exhibits.render_exhibits_md(master, ci, run_level, crowding, failure)
    md_path = out_dir / "exhibits.md"
    md_path.write_text(md, encoding="utf-8")

    html_path = out_dir / "exhibits.html"
    html_path.write_text(exhibits.md_to_html(md), encoding="utf-8")

    written = [md_path, html_path]
    meta = master["meta"]
    print(f"Models included: {meta['models_included']}/{meta['models_total']}")
    for p in written:
        print(f"  {p.name}")
    log.info("assembled %d exhibit files into %s", len(written), out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
