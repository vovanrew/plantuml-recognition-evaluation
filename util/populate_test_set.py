#!/usr/bin/env python3
"""Populate data/ from a test_set.json key list.

Copies each selected diagram's PlantUML source from the corpus and extracts its
rendered PNG from the corpus image zip into the local data/ dirs, then prunes any
files that are no longer in the set so data/ matches the artifact exactly.

  data/puml_files/<key>.puml          (corpus source)
  data/puml_images/<base>.png         (original render, from the zip)

The 1568 px model inputs are produced separately by standardize_images.py.

Usage (invoke from project root):
  export PLANTUML_DATASET_ROOT=/path/to/zenodo_content
  python3 util/populate_test_set.py --test-set data/test_set.json --prune

The corpus location comes from PLANTUML_DATASET_ROOT; --puml-src and --images-zip
override it per path.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import zipfile

# Root of the mined 143k-pair corpus (NOT the 1000-diagram test set shipped with
# this repo). Point PLANTUML_DATASET_ROOT at it, or override each path on the CLI.
DATASET = os.environ.get("PLANTUML_DATASET_ROOT", "dataset/zenodo_content")
DEFAULT_PUML_SRC = f"{DATASET}/puml_files"
DEFAULT_IMAGES_ZIP = f"{DATASET}/puml_images.zip"


def prune_dir(directory, keep_names):
    """Delete files in `directory` whose basename is not in keep_names."""
    if not os.path.isdir(directory):
        return 0
    removed = 0
    for name in os.listdir(directory):
        if name not in keep_names and os.path.isfile(os.path.join(directory, name)):
            os.remove(os.path.join(directory, name))
            removed += 1
    return removed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-set", default="data/test_set.json")
    ap.add_argument("--puml-src", default=DEFAULT_PUML_SRC)
    ap.add_argument("--images-zip", default=DEFAULT_IMAGES_ZIP)
    ap.add_argument("--puml-out", default="data/puml_files")
    ap.add_argument("--img-out", default="data/puml_images")
    ap.add_argument("--img-1568", default="data/puml_images_1568",
                    help="standardized-image dir to prune (regenerated separately)")
    ap.add_argument("--prune", action="store_true",
                    help="remove data/ files not in the current set")
    args = ap.parse_args()

    os.makedirs(args.puml_out, exist_ok=True)
    os.makedirs(args.img_out, exist_ok=True)

    keys = [d["key"] for d in json.load(open(args.test_set))["diagrams"]]
    bases = [k[:-5] for k in keys]

    # 1. copy PlantUML source
    missing_puml = []
    for key in keys:
        src = os.path.join(args.puml_src, key)
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(args.puml_out, key))
        else:
            missing_puml.append(key)

    # 2. extract original PNGs from the zip (single-page; stem == base)
    zf = zipfile.ZipFile(args.images_zip)
    by_stem = {}
    for n in zf.namelist():
        if n.endswith(".png"):
            by_stem[n.rsplit("/", 1)[-1][:-4]] = n
    missing_img = []
    for base in bases:
        entry = by_stem.get(base)
        if entry is None:
            missing_img.append(base)
            continue
        with zf.open(entry) as fh, open(os.path.join(args.img_out, base + ".png"), "wb") as out:
            shutil.copyfileobj(fh, out)

    print(f"copied {len(keys) - len(missing_puml)}/{len(keys)} puml -> {args.puml_out}")
    print(f"extracted {len(bases) - len(missing_img)}/{len(bases)} png -> {args.img_out}")
    if missing_puml:
        print(f"  WARNING: {len(missing_puml)} puml missing, e.g. {missing_puml[:3]}")
    if missing_img:
        print(f"  WARNING: {len(missing_img)} png missing, e.g. {missing_img[:3]}")

    if args.prune:
        r1 = prune_dir(args.puml_out, set(keys))
        r2 = prune_dir(args.img_out, {b + ".png" for b in bases})
        r3 = prune_dir(args.img_1568, {b + ".png" for b in bases})
        print(f"pruned stale files: {r1} puml, {r2} img, {r3} img_1568")


if __name__ == "__main__":
    main()
