#!/usr/bin/env python3
"""Standardize test-set images for inference (methodology/test-set-construction.md §7).

Produces the single canonical image sent identically to every model:
  - long edge capped at 1568 px (Claude Sonnet 4.6 native processing resolution),
    aspect preserved, DOWNSCALE ONLY (never upscale),
  - transparency flattened onto white (avoids black-composite text loss),
  - lossless PNG output.

Also reports the per-tier legibility/crowding descriptor (content_lines per MP
after resize).
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None   # trusted corpus; some Q4 renders exceed the bomb threshold

LONG_EDGE = 1568


def standardize(src_path, dst_path, long_edge):
    im = Image.open(src_path)
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        rgba = im.convert("RGBA")
        bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
        im = Image.alpha_composite(bg, rgba).convert("RGB")
    else:
        im = im.convert("RGB")

    w, h = im.size
    scale = long_edge / max(w, h)
    if scale < 1.0:                       # downscale only
        new = (max(1, round(w * scale)), max(1, round(h * scale)))
        im = im.resize(new, Image.LANCZOS)
    im.save(dst_path, "PNG")
    return (w, h), im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-set", default="data/test_set.json")
    ap.add_argument("--src", default="data/puml_images")
    ap.add_argument("--out", default="data/puml_images_1568")
    ap.add_argument("--long-edge", type=int, default=LONG_EDGE)
    ap.add_argument("--limit", type=int, default=0, help="smoke: only N images")
    args = ap.parse_args()

    import os
    os.makedirs(args.out, exist_ok=True)
    diagrams = json.load(open(args.test_set))["diagrams"]
    if args.limit:
        diagrams = diagrams[: args.limit]

    resized = 0
    crowding = defaultdict(list)   # (type, tier) -> content_lines per MP after resize
    for r in diagrams:
        base = r["key"][:-5]
        (ow, oh), (nw, nh) = standardize(
            f"{args.src}/{base}.png", f"{args.out}/{base}.png", args.long_edge)
        if (nw, nh) != (ow, oh):
            resized += 1
        mp_after = nw * nh / 1e6
        crowding[(r["primary_type"], r["tier"])].append(r["content_lines"] / mp_after)

    print(f"standardized {len(diagrams)} images -> {args.out} "
          f"(long edge {args.long_edge}; {resized} downscaled, "
          f"{len(diagrams)-resized} kept native)")
    print("\n  crowding descriptor: median content_lines per MP (after resize)")
    print("  type      T1     T2     T3     T4")
    for t in ("class", "sequence"):
        cells = [f"{np.median(crowding[(t, tier)]):>6.1f}"
                 if crowding[(t, tier)] else "   -  " for tier in (1, 2, 3, 4)]
        print(f"  {t:<8}  " + " ".join(cells))


if __name__ == "__main__":
    main()
