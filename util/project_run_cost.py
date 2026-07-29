#!/usr/bin/env python3
"""Project a 1000-cell run's API cost from a pilot run directory.

Sums prompt/completion (and Gemini thoughts) tokens over the stored raw
responses, then linearly extrapolates per-cell averages to the full test set
at the given per-1M-token prices. The pilot's deterministic stride spread
covers both types and all four tiers, so the per-cell average is taken as
representative of the full set.

Usage:
  python3 util/project_run_cost.py data/runs/<run_dir> \
      --in-price 1.75 --out-price 14.00 [--n 1000]
"""
from __future__ import annotations

import argparse
import glob
import json
import os


def usage_totals(run_dir):
    """(cells, prompt_tokens, completion_tokens, thoughts_tokens) summed over
    stored successful responses (failure records are skipped)."""
    cells = ptok = ctok = ttok = 0
    for path in glob.glob(os.path.join(run_dir, "*.json")):
        if os.path.basename(path) == "run_meta.json":
            continue
        with open(path) as f:
            r = json.load(f)
        if "error" in r:
            continue
        cells += 1
        if "usageMetadata" in r:
            u = r["usageMetadata"]
            ptok += u.get("promptTokenCount", 0)
            ctok += u.get("candidatesTokenCount", 0)
            ttok += u.get("thoughtsTokenCount", 0)
        else:
            u = r.get("usage", {})
            ptok += u.get("prompt_tokens", 0)
            ctok += u.get("completion_tokens", 0)
    return cells, ptok, ctok, ttok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir")
    ap.add_argument("--in-price", type=float, required=True,
                    help="USD per 1M input tokens")
    ap.add_argument("--out-price", type=float, required=True,
                    help="USD per 1M output tokens (incl. thinking)")
    ap.add_argument("--n", type=int, default=1000)
    args = ap.parse_args()

    cells, ptok, ctok, ttok = usage_totals(args.run_dir)
    if not cells:
        raise SystemExit(f"no successful responses in {args.run_dir}")
    scale = args.n / cells
    cost = (ptok * args.in_price + (ctok + ttok) * args.out_price) / 1e6
    print(f"{args.run_dir}: {cells} cells | "
          f"ptok {ptok} ctok {ctok} ttok {ttok} | pilot cost ${cost:.3f}")
    print(f"projected to n={args.n}: in {ptok*scale/1e6:.2f}M out "
          f"{(ctok+ttok)*scale/1e6:.2f}M -> ${cost*scale:.2f}")


if __name__ == "__main__":
    main()
