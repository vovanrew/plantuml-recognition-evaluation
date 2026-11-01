#!/usr/bin/env python3
"""Pack the scorer-v2 result files of the stored runs into data_v2.zip, or check the archive.

data_v2/ holds the stored runs of data/ scored again under scorer v2 (tag `scorer-v2`):
  element_f1/<run>/element_f1_results.json, relationship_f1/<run>/relationship_f1_results.json
                         scorer v2
  _bridge/<level>/<metric>/<run>/<metric>_results.json
                         every level between scorer v1 and scorer v2, one rule at a time
  _bridge/levels.json    the switches of each level
  _bridge/spot_effect.json
                         the effect of the stereotype-spot letter alone, per run
The archive holds every .json file under data_v2/ and nothing else. The extracted blocks
(gt_extracted/, pred_extracted/) are working copies the runners write again on every run, and
they are left out.

The archive is the same bytes for the same files: entries sorted by path, every timestamp
1980-01-01 00:00, mode 0644.

Usage (from the repository root):
  python3 util/pack_data_v2.py            # writes data_v2.zip
  python3 util/pack_data_v2.py --check    # data_v2.zip against data_v2/
  unzip data_v2.zip                       # recreates data_v2/ (result files only)
"""
import argparse
import stat
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = (1980, 1, 1, 0, 0, 0)
FILE_MODE = stat.S_IFREG | 0o644


def result_files(root):
    """Paths, relative to root and sorted, of every .json file under root/data_v2."""
    top = root / "data_v2"
    if not top.is_dir():
        raise SystemExit(f"no {top}")
    return sorted(p.relative_to(root).as_posix() for p in top.rglob("*.json") if p.is_file())


def pack(root, out):
    paths = result_files(root)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in paths:
            info = zipfile.ZipInfo(rel, DATE)
            info.external_attr = FILE_MODE << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, (root / rel).read_bytes())
    return len(paths)


def check(root, archive):
    """Problems found comparing the archive with data_v2/; empty when they agree."""
    problems = []
    on_disk = result_files(root)
    with zipfile.ZipFile(archive) as z:
        names = sorted(z.namelist())
        if names != on_disk:
            missing = sorted(set(on_disk) - set(names))
            extra = sorted(set(names) - set(on_disk))
            problems += [f"not in archive: {p}" for p in missing]
            problems += [f"not in data_v2/: {p}" for p in extra]
        for rel in sorted(set(names) & set(on_disk)):
            if z.read(rel) != (root / rel).read_bytes():
                problems.append(f"differs: {rel}")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="compare data_v2.zip with data_v2/")
    ap.add_argument("--root", default=str(ROOT), help="repository root (default: this one)")
    ap.add_argument("--zip", default="", help="archive path (default: <root>/data_v2.zip)")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    archive = Path(args.zip) if args.zip else root / "data_v2.zip"
    if args.check:
        problems = check(root, archive)
        for p in problems:
            print(p)
        print(f"{archive.name}: {'OK' if not problems else f'{len(problems)} problems'}")
        return 0 if not problems else 1
    n = pack(root, archive)
    print(f"{archive}: {n} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
