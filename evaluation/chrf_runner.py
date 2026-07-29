#!/usr/bin/env python3
"""chrF++ runner (metric 4).

Computes sacrebleu chrF++ (char_order=6, word_order=2, beta=2; raw 0-100 scale)
between each predicted PlantUML block and its ground-truth, then aggregates over
the set with macro = mean of per-diagram scores and micro = corpus_chrf pooled
over all (hyp, ref) pairs.

The PlantUML block is isolated symmetrically on both sides with
csr_runner.extract_puml so a WoC header or markdown fence around the model
output is dropped the same way for GT and predictions.

Two reporting modes (mirroring the structural metrics):
  - zeros_for_failed: every test-set key scored; missing OR non-compiling
    predictions forced to score 0 (consulted from --csr).
  - compiled_only:    chrF++ over CSR-passing predictions only.

Unlike the structural runners, --csr is REQUIRED here: chrF++ is parse-
independent, so a broken-but-textually-close prediction still has a real,
non-zero surface score; the compile gate must be supplied explicitly.

Usage (invoke from project root):
  python evaluation/chrf_runner.py --pred-dir <run-dir> \
      --csr data/csr/<run>/csr_results.json --out data/chrf/<run>
  python evaluation/chrf_runner.py --pred-dir <run-dir> --test-set data/test_set.json \
      --csr <csr.json> --out <out>
"""
from __future__ import annotations

import argparse
import json
import os
from glob import glob

import chrf
from csr_runner import extract_puml


def _stem(path):
    return os.path.splitext(os.path.basename(path))[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred-dir", required=True,
                    help="dir of predicted code files (*.puml/*.txt), stem = diagram key")
    ap.add_argument("--gt-dir", default="data/puml_files",
                    help="dir of ground-truth .puml files")
    ap.add_argument("--out", required=True, help="results dir")
    ap.add_argument("--test-set", default="",
                    help="test_set.json: score over its full key set "
                         "(missing predictions count as score 0)")
    ap.add_argument("--csr", required=True,
                    help="csr_results.json: REQUIRED. Defines the compile gate "
                         "for zeros_for_failed and the membership of compiled_only")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    # Index the predictions on disk by their stem (= diagram key).
    pred_files = sorted(glob(os.path.join(args.pred_dir, "*.puml"))
                        + glob(os.path.join(args.pred_dir, "*.txt")))
    pred_path = {_stem(p): p for p in pred_files}
    have_pred = set(pred_path)

    # Keys to score: test-set key list if given, else the predictions present.
    if args.test_set:
        keys = [d["key"][:-5] for d in json.load(open(args.test_set))["diagrams"]]
    else:
        keys = sorted(have_pred)

    # Load compile status from CSR.
    csr = json.load(open(args.csr))
    compiled_set = {d["key"] for d in csr["diagrams"] if d.get("compiled")}

    # Load and isolate the PlantUML block from each GT file.
    gt_block = {}
    missing_gt = []
    for k in keys:
        gt_path = os.path.join(args.gt_dir, k + ".puml")
        if not os.path.exists(gt_path):
            missing_gt.append(k)
            continue
        with open(gt_path, encoding="utf-8") as f:
            gt_block[k] = extract_puml(f.read())
    if missing_gt:
        raise SystemExit(f"missing {len(missing_gt)} GT files, e.g. {missing_gt[:3]}")

    # Score every key on its actual text (score = 0 only when no prediction file
    # exists; the compile gate is applied later, in the zeros_for_failed view).
    rows = []
    for k in keys:
        ref = gt_block[k]
        if k in have_pred:
            with open(pred_path[k], encoding="utf-8") as f:
                hyp = extract_puml(f.read())
            score = chrf.sentence_score(hyp, ref)
        else:
            hyp, score = "", 0.0
        rows.append({"key": k, "has_pred": k in have_pred,
                     "compiled": k in compiled_set, "score": score,
                     "hyp": hyp, "ref": ref})

    # zeros_for_failed: missing OR non-compiling -> score 0, hyp "" (so the
    # corpus_chrf micro pool gets zero contribution from those keys).
    zfr_rows = [r if (r["has_pred"] and r["compiled"])
                else {**r, "score": 0.0, "hyp": ""}
                for r in rows]
    # compiled_only: actual scores over CSR-passing predictions.
    co_rows = [r for r in rows if r["compiled"]]

    summary = {
        "scale": "0-100 (sacrebleu native)",
        "params": {"char_order": chrf.CHAR_ORDER,
                   "word_order": chrf.WORD_ORDER, "beta": chrf.BETA},
        "zeros_for_failed": chrf.aggregate(zfr_rows),
        "compiled_only": chrf.aggregate(co_rows),
    }

    # Public per-diagram rows: actual score, gating flags; hyp/ref omitted (bulky).
    diagrams = [{k: v for k, v in r.items() if k not in ("hyp", "ref")}
                for r in rows]

    out_path = os.path.join(args.out, "chrf_results.json")
    with open(out_path, "w") as f:
        json.dump({"summary": summary, "diagrams": diagrams}, f, indent=2)

    def show(label, agg):
        print(f"{label:<16} n={agg['n']:<5} "
              f"micro={agg['micro']:6.2f}  macro={agg['macro']:6.2f}")

    print("chrF++  (0-100 scale; char_order=6 word_order=2 beta=2)")
    show("zeros_for_failed", summary["zeros_for_failed"])
    show("compiled_only", summary["compiled_only"])
    print(f"results -> {out_path}")


if __name__ == "__main__":
    main()
