#!/usr/bin/env python3
"""Relationship F1 runner (metric 3).

Extracts the structural graph from ground-truth and predicted PlantUML with the
DiagramStatsExtractor fork JAR, matches edges by (source, target, relation)
(endpoints normalized as node names; an association is directional when exactly
one end carries an arrowhead and undirected otherwise, all other relations
directional; label ignored; multiset), and reports precision/recall/F1 per
diagram plus micro/macro over the set.

Two reporting modes (methodology/evaluation-framework.md, "reported two ways"):
  - zeros_for_failed: every test-set key scored; a missing/non-parsing
    prediction yields an empty graph -> F1 0.
  - compiled_only:   only keys whose prediction compiled (per csr_results.json).

Per-relation stratification (inheritance/composition/aggregation/dependency/
association/message) is reported as micro P/R/F1 over all scored keys plus
support counts; empty-on-both-sides diagrams contribute zero pooled counts, so a
relation absent from a diagram does not inflate its stratum.

The PlantUML block is isolated symmetrically on both sides with
csr_runner.extract_puml (reused via element_f1_runner.write_extracted), so a WoC
header before @startuml is dropped the same way for GT and predictions. An answer
holding several @startuml...@enduml diagrams is scored on its first diagram.

The defaults are scorer v2; the rule switches are those of element_f1_runner
(plus --no-association-direction and --extractor-arg=--no-arrowheads), and with
every switch off the runner reproduces scorer v1.

Usage (invoke from project root):
  python evaluation/relationship_f1_runner.py --pred-dir data/csr/<run>/extracted \
      --test-set data/test_set.json --csr data/csr/<run>/csr_results.json \
      --out data/relationship_f1/<run>
"""
from __future__ import annotations

import argparse
import json
import os
from glob import glob

import relationship_f1 as rf
from element_f1_runner import (
    EXTRACTOR_JAR, _stem, add_scorer_args, extract_graphs, rules_from_args,
    scorer_record, write_extracted,
)


def _f1(p, r):
    return 0.0 if (p + r) == 0 else 2 * p * r / (p + r)


def micro_with_support(rows):
    """Pooled micro P/R/F1 plus support counts for a set of per-diagram rows."""
    tp = sum(r["tp"] for r in rows)
    fp = sum(r["fp"] for r in rows)
    fn = sum(r["fn"] for r in rows)
    p = tp / (tp + fp) if (tp + fp) else 1.0
    r = tp / (tp + fn) if (tp + fn) else 1.0
    return {
        "precision": p, "recall": r, "f1": _f1(p, r),
        "support_gt": tp + fn,        # GT edges of this relation
        "support_pred": tp + fp,      # predicted edges of this relation
        "n_diagrams_with_gt": sum(1 for x in rows if (x["tp"] + x["fn"]) > 0),
        "n": len(rows),
    }


def per_relation_counts(gt_by_key, pred_by_key, keys, rules=rf.V2):
    """Per-diagram per-relation tp/fp/fn over the canonical RELATIONS.

    Returns ``{key: {rel: {"tp", "fp", "fn"}}}``. Built from the same
    ``rf.compute(relation=rel)`` scoring that ``summarize`` pools into
    ``summary.by_relation``, so two structural invariants hold by construction:
      * pooling these counts across any key subset reproduces
        ``summary[pop]["by_relation"]`` (both populations); and
      * the edge match key carries the relation type, so edges partition by
        relation -- summing a diagram's six relations reproduces its overall
        tp/fp/fn.
    This is purely additive: it is attached to each per-diagram row and does not
    touch the overall scores or the summary.
    """
    per_key = {k: {} for k in keys}
    for rel in rf.RELATIONS:
        for row in rf.compute(gt_by_key, pred_by_key, keys, relation=rel, rules=rules):
            per_key[row["key"]][rel] = {"tp": row["tp"], "fp": row["fp"], "fn": row["fn"]}
    return per_key


def summarize(gt_by_key, pred_by_key, keys, compiled_keys, rules=rf.V2):
    """Build the summary for both reporting populations.

    Each population carries an overall ('all', micro+macro) score and a
    per-relation breakdown ('by_relation', micro+support).
    """
    overall_rows = rf.compute(gt_by_key, pred_by_key, keys, rules=rules)
    overall_by_key = {r["key"]: r for r in overall_rows}

    def population(row_subset_keys):
        all_rows = ([overall_by_key[k] for k in row_subset_keys]
                    if row_subset_keys is not None else overall_rows)
        by_relation = {}
        for rel in rf.RELATIONS:
            rel_rows = rf.compute(gt_by_key, pred_by_key,
                                  row_subset_keys if row_subset_keys is not None else keys,
                                  relation=rel, rules=rules)
            by_relation[rel] = micro_with_support(rel_rows)
        return {"all": rf.aggregate(all_rows), "by_relation": by_relation}

    summary = {"zeros_for_failed": population(None)}
    if compiled_keys is not None:
        summary["compiled_only"] = population(compiled_keys)
    return summary, overall_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred-dir", required=True,
                    help="dir of predicted code files (*.puml/*.txt), stem = diagram key")
    ap.add_argument("--gt-dir", default="data/puml_files",
                    help="dir of ground-truth .puml files")
    ap.add_argument("--out", required=True, help="results dir")
    ap.add_argument("--test-set", default="",
                    help="test_set.json: score over its full key set "
                         "(missing predictions count as F1 0)")
    ap.add_argument("--csr", default="",
                    help="csr_results.json: enables the compiled_only reporting mode")
    ap.add_argument("--jar", default=EXTRACTOR_JAR,
                    help="DiagramStatsExtractor fork JAR (NOT the standard renderer)")
    add_scorer_args(ap)
    args = ap.parse_args()
    rules = rules_from_args(args)

    os.makedirs(args.out, exist_ok=True)

    pred_files = sorted(glob(os.path.join(args.pred_dir, "*.puml"))
                        + glob(os.path.join(args.pred_dir, "*.txt")))
    have_pred = {_stem(p) for p in pred_files}
    if args.test_set:
        keys = [d["key"][:-5] for d in json.load(open(args.test_set))["diagrams"]]
    else:
        keys = sorted(have_pred)

    gt_files = [os.path.join(args.gt_dir, k + ".puml") for k in keys]
    missing_gt = [k for k, p in zip(keys, gt_files) if not os.path.exists(p)]
    if missing_gt:
        raise SystemExit(f"missing {len(missing_gt)} GT files, e.g. {missing_gt[:3]}")

    write_extracted(gt_files, os.path.join(args.out, "gt_extracted"))
    write_extracted(pred_files, os.path.join(args.out, "pred_extracted"))

    gt_by_key = extract_graphs(os.path.join(args.out, "gt_extracted"), args.jar,
                               not args.last_diagram, args.extractor_arg)
    pred_by_key = extract_graphs(os.path.join(args.out, "pred_extracted"), args.jar,
                                 not args.last_diagram, args.extractor_arg)

    compiled_keys = None
    if args.csr:
        csr = json.load(open(args.csr))
        compiled_keys = [d["key"] for d in csr["diagrams"]
                         if d.get("compiled") and d["key"] in keys]

    summary, overall_rows = summarize(gt_by_key, pred_by_key, keys, compiled_keys, rules)

    # Additive per-diagram per-relation tp/fp/fn (enables per-relation CIs);
    # overall scores and the summary above are untouched.
    by_rel = per_relation_counts(gt_by_key, pred_by_key, keys, rules)

    compiled_set = set(compiled_keys) if compiled_keys is not None else None
    diagrams = []
    for r in overall_rows:
        d = dict(r)
        d["has_pred"] = r["key"] in have_pred
        if compiled_set is not None:
            d["compiled"] = r["key"] in compiled_set
        d["by_relation"] = by_rel[r["key"]]
        diagrams.append(d)

    out_path = os.path.join(args.out, "relationship_f1_results.json")
    with open(out_path, "w") as f:
        json.dump({"scorer": scorer_record(args, rules),
                   "summary": summary, "diagrams": diagrams}, f, indent=2)

    def show_all(label, agg):
        m, M = agg["micro"], agg["macro"]
        print(f"{label:<16} n={agg['n']:<5} "
              f"micro F1={m['f1']:.3f} (P={m['precision']:.3f} R={m['recall']:.3f})  "
              f"macro F1={M['f1']:.3f}")

    def show_relations(by_relation):
        for rel in rf.RELATIONS:
            s = by_relation[rel]
            if s["support_gt"] == 0 and s["support_pred"] == 0:
                continue
            print(f"  {rel:<13} micro F1={s['f1']:.3f} "
                  f"(P={s['precision']:.3f} R={s['recall']:.3f})  "
                  f"gt={s['support_gt']} pred={s['support_pred']}")

    print("Relationship F1")
    show_all("zeros_for_failed", summary["zeros_for_failed"]["all"])
    show_relations(summary["zeros_for_failed"]["by_relation"])
    if "compiled_only" in summary:
        show_all("compiled_only", summary["compiled_only"]["all"])
        show_relations(summary["compiled_only"]["by_relation"])
    print(f"results -> {out_path}")


if __name__ == "__main__":
    main()
