"""Assemble data_paper/: the data root the revised paper's tables are built from.

It holds every stored run under scorer v2, and adds the three self-served
Qwen3.5 zero-shot runs (one card, bf16) made in the fine-tuning study:

- test_set.json, gt_token_stats.json, puml_files/, puml_images_1568/  <- data/
- csr/, chrf/, runs/ of the hosted runs                              <- data/
  (CSR and chrF++ do not depend on the scorer version)
- element_f1/, relationship_f1/ of the hosted runs                   <- data_v2/
- the four metrics and the answers of the self-served runs           <- <fine-tune>/runs/test/<run>/

Nothing is scored here: every file is copied as stored. Run it from the
repository root after unpacking data.zip and data_v2.zip:

    python util/build_paper_root.py --fine-tune ../fine-tune
"""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# fine-tune run name -> run directory name in data_paper/
SELF_SERVED = {
    "2B_zero_shot": "Qwen3.5-2B_self-served",
    "9B_zero_shot": "Qwen3.5-9B_self-served",
    "27B_zero_shot": "Qwen3.5-27B_self-served",
}
METRIC_FILES = {
    "csr": "csr_results.json",
    "chrf": "chrf_results.json",
    "element_f1": "element_f1_results.json",
    "relationship_f1": "relationship_f1_results.json",
}
SHARED = ("test_set.json", "gt_token_stats.json", "puml_files", "puml_images_1568")


def _copy(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    if src.is_dir():
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def build(data: Path, data_v2: Path, fine_tune: Path, out: Path,
          scorer: str = "v2") -> list[str]:
    """Copy everything into ``out``; return the run directory names it holds.

    ``scorer`` picks the F1 result files: "v2" (data_v2/ and scores/v2) or "v1"
    (data/ and scores/v1). CSR and chrF++ are the same files for both."""
    f1_root = data_v2 if scorer == "v2" else data
    for name in SHARED:
        _copy(data / name, out / name)

    hosted = sorted(p.name for p in (data / "runs").iterdir() if p.is_dir())
    for run in hosted:
        _copy(data / "runs" / run, out / "runs" / run)
        for metric in ("csr", "chrf"):
            _copy(data / metric / run, out / metric / run)
        for metric in ("element_f1", "relationship_f1"):
            _copy(f1_root / metric / run, out / metric / run)

    for src_name, run in SELF_SERVED.items():
        src = fine_tune / "runs" / "test" / src_name
        _copy(src / "answers", out / "runs" / run)
        for metric, fname in METRIC_FILES.items():
            version = scorer if metric in ("element_f1", "relationship_f1") else "v2"
            _copy(src / "scores" / version / metric / src_name / fname,
                  out / metric / run / fname)

    return hosted + list(SELF_SERVED.values())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data", type=Path, default=ROOT / "data")
    ap.add_argument("--data-v2", type=Path, default=ROOT / "data_v2")
    ap.add_argument("--fine-tune", type=Path, default=ROOT.parent / "fine-tune")
    ap.add_argument("--scorer", choices=("v1", "v2"), default="v2")
    ap.add_argument("--out", type=Path, default=None,
                    help="default: data_paper/ for v2, data_paper_v1/ for v1")
    args = ap.parse_args()
    if args.out is None:
        args.out = ROOT / ("data_paper" if args.scorer == "v2" else "data_paper_v1")
    runs = build(args.data, args.data_v2, args.fine_tune, args.out, args.scorer)
    for run in runs:
        print(run)
    print(f"{len(runs)} runs in {args.out}")


if __name__ == "__main__":
    main()
