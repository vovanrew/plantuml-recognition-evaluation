#!/usr/bin/env python3
"""Measure the ground-truth PlantUML token-length distribution over the test set.

Sizes the inference `--max-tokens` ceiling: the cap must exceed every legitimate
GT (so no real diagram is silently truncated) while still bounding runaway
no-EOS repetition loops. Reports min / mean / p50 / p75 / p90 / p95 / p99 / max
of completion-token counts for the 1000 frozen test-set GTs.

Tokenizer: Qwen3.5-2B (via transformers AutoTokenizer; family currently
benchmarked). Qwen tokenizes code less efficiently than frontier model
tokenizers, so a Qwen-sized cap is conservative for every model in the suite.

Usage (invoke from project root):
  python util/measure_gt_tokens.py                 # full 1000-file run
  python util/measure_gt_tokens.py --smoke 10      # 10-file smoke before scale
  python util/measure_gt_tokens.py --tokenizer Qwen/Qwen3.5-2B
"""
from __future__ import annotations

import argparse
import json
import math
import os
import statistics


def percentile(sorted_xs, p):
    """Linear-interpolation percentile (p in [0, 100]) over a sorted sequence."""
    if not sorted_xs:
        return 0
    if len(sorted_xs) == 1:
        return sorted_xs[0]
    rank = (p / 100.0) * (len(sorted_xs) - 1)
    lo = int(math.floor(rank))
    hi = int(math.ceil(rank))
    if lo == hi:
        return sorted_xs[lo]
    return sorted_xs[lo] + (sorted_xs[hi] - sorted_xs[lo]) * (rank - lo)


def round_up_to(n, step):
    return int(math.ceil(n / step) * step)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-set", default="data/test_set.json")
    ap.add_argument("--puml-dir", default="data/puml_files")
    ap.add_argument("--tokenizer", default="Qwen/Qwen3.5-2B")
    ap.add_argument("--out", default="data/gt_token_stats.json")
    ap.add_argument("--smoke", type=int, default=0,
                    help="if > 0, run on only the first N files (per project smoke-test rule)")
    args = ap.parse_args()

    from transformers import AutoTokenizer  # heavy: import after argparse
    import transformers

    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    tok_class = type(tok).__name__

    diagrams = json.load(open(args.test_set))["diagrams"]
    if args.smoke > 0:
        diagrams = diagrams[: args.smoke]

    counts = []  # list of (key, primary_type, tier, n_tokens, n_chars)
    for r in diagrams:
        path = os.path.join(args.puml_dir, r["key"])
        with open(path, encoding="utf-8") as f:
            text = f.read()
        n = len(tok.encode(text, add_special_tokens=False))
        counts.append({
            "key": r["key"],
            "primary_type": r["primary_type"],
            "tier": r["tier"],
            "n_tokens": n,
            "n_chars": len(text),
        })

    ns = sorted(c["n_tokens"] for c in counts)
    stats = {
        "n_files": len(ns),
        "min": ns[0],
        "mean": round(statistics.fmean(ns), 2),
        "p50": int(percentile(ns, 50)),
        "p75": int(percentile(ns, 75)),
        "p90": int(percentile(ns, 90)),
        "p95": int(percentile(ns, 95)),
        "p99": int(percentile(ns, 99)),
        "max": ns[-1],
    }

    # Sizing heuristic: ceil(max * 1.5) rounded up to the nearest 256.
    cap_raw = int(math.ceil(stats["max"] * 1.5))
    cap_rounded = round_up_to(cap_raw, 256)

    out = {
        "tokenizer": {
            "package": "transformers",
            "package_version": transformers.__version__,
            "model": args.tokenizer,
            "tokenizer_class": tok_class,
            "add_special_tokens": False,
        },
        "test_set": args.test_set,
        "puml_dir": args.puml_dir,
        "stats": stats,
        "recommended_max_tokens": {
            "raw_ceil_1_5x_max": cap_raw,
            "rounded_to_256": cap_rounded,
            "heuristic": "ceil(max * 1.5) rounded up to nearest 256",
        },
        "per_file": counts,
    }

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out, f, indent=2)

    print(f"tokenizer: {args.tokenizer} ({tok_class}), transformers {transformers.__version__}")
    print(f"n_files: {stats['n_files']}")
    print(f"  min  = {stats['min']}")
    print(f"  mean = {stats['mean']}")
    print(f"  p50  = {stats['p50']}")
    print(f"  p75  = {stats['p75']}")
    print(f"  p90  = {stats['p90']}")
    print(f"  p95  = {stats['p95']}")
    print(f"  p99  = {stats['p99']}")
    print(f"  max  = {stats['max']}")
    print(f"recommended --max-tokens: {cap_rounded} (raw 1.5x = {cap_raw})")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
