#!/usr/bin/env python3
"""Pack the self-served Qwen3.5 zero-shot runs into data_selfserved.zip, or check the archive.

The three dense sizes (2B, 9B, 27B) were answered on one card in bf16 in the fine-tuning
study (../fine-tune, runs/test/<size>_zero_shot) and are the main Qwen rows of the revised
paper. The archive holds, for each run, under data_selfserved/runs/test/<run>/:

  answers/<key>.json, <key>.puml, manifest.json, run_meta.json
                         the 1,000 raw responses and the extracted PlantUML answers
  scores/v2/<metric>/<run>/<metric>_results.json
                         CSR, chrF++, Element F1 and Relationship F1 under scorer v2
  scores/v1/<metric>/<run>/<metric>_results.json
                         Element F1 and Relationship F1 under scorer v1; scores/v1/csr and
                         scores/v1/chrf are links to ../v2/csr and ../v2/chrf, since those two
                         metrics do not depend on the scorer version
  scores/manifest.json   the sha256 of every result file
  answer_manifest.json, queue_commit.txt, manifest.log, runner.log, server.log
                         provenance: model revision, settings, test-set sha256, dates, logs

Unzipping at the repository root recreates data_selfserved/, and
`python util/build_paper_root.py --fine-tune data_selfserved` then reads the runs from it.

The archive is the same bytes for the same files: entries sorted by path, every timestamp
1980-01-01 00:00, mode 0644 (links 0777).

Usage (from the repository root):
  python3 util/pack_selfserved.py --fine-tune ../fine-tune           # writes data_selfserved.zip
  python3 util/pack_selfserved.py --fine-tune ../fine-tune --check   # archive against the runs
  unzip data_selfserved.zip                                          # recreates data_selfserved/
"""
import argparse
import stat
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = (1980, 1, 1, 0, 0, 0)
FILE_MODE = stat.S_IFREG | 0o644
LINK_MODE = stat.S_IFLNK | 0o777
RUNS = ("2B_zero_shot", "9B_zero_shot", "27B_zero_shot")
PREFIX = "data_selfserved/runs/test"


def is_link_stub(path):
    """True for a link stored as a small text file (a symlink checked out on Windows):
    its whole content is a relative path to a directory beside it."""
    if path.is_symlink():
        return True
    if path.stat().st_size > 256:
        return False
    try:
        target = path.read_text(encoding="utf-8").strip()
    except UnicodeDecodeError:
        return False
    return target.startswith("..") and (path.parent / target).is_dir()


def link_target(path):
    return str(path.readlink()) if path.is_symlink() else path.read_text(encoding="utf-8").strip()


def run_files(fine_tune):
    """{archive path: source path} for every file of the three runs, sorted by archive path."""
    out = {}
    for run in RUNS:
        top = Path(fine_tune) / "runs" / "test" / run
        if not top.is_dir():
            raise SystemExit(f"no {top}")
        for p in top.rglob("*"):
            if p.is_file() or p.is_symlink():
                out[f"{PREFIX}/{run}/{p.relative_to(top).as_posix()}"] = p
    return dict(sorted(out.items()))


def entry_bytes(src):
    """(bytes, is_link) of one archive entry."""
    if is_link_stub(src):
        return link_target(src).encode("utf-8"), True
    return src.read_bytes(), False


def pack(fine_tune, out):
    files = run_files(fine_tune)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel, src in files.items():
            data, link = entry_bytes(src)
            info = zipfile.ZipInfo(rel, DATE)
            info.external_attr = (LINK_MODE if link else FILE_MODE) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, data)
    return len(files)


def check(fine_tune, archive):
    """Problems found comparing the archive with the runs; empty when they agree."""
    problems = []
    files = run_files(fine_tune)
    with zipfile.ZipFile(archive) as z:
        names = sorted(z.namelist())
        if names != list(files):
            problems += [f"not in archive: {p}" for p in sorted(set(files) - set(names))]
            problems += [f"not in the runs: {p}" for p in sorted(set(names) - set(files))]
        for rel in sorted(set(names) & set(files)):
            if z.read(rel) != entry_bytes(files[rel])[0]:
                problems.append(f"differs: {rel}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--fine-tune", default=str(ROOT.parent / "fine-tune"),
                    help="the fine-tuning study's repository (default: ../fine-tune)")
    ap.add_argument("--check", action="store_true", help="compare the archive with the runs")
    ap.add_argument("--zip", default="", help="archive path (default: <repo>/data_selfserved.zip)")
    args = ap.parse_args(argv)
    archive = Path(args.zip) if args.zip else ROOT / "data_selfserved.zip"
    if args.check:
        problems = check(args.fine_tune, archive)
        for p in problems:
            print(p)
        print(f"{archive.name}: {'OK' if not problems else f'{len(problems)} problems'}")
        return 0 if not problems else 1
    n = pack(args.fine_tune, archive)
    print(f"{archive}: {n} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
