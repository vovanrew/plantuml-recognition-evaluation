#!/usr/bin/env python3
"""Element F1 runner (metric 2).

Extracts the structural graph from ground-truth and predicted PlantUML with the
DiagramStatsExtractor fork JAR, matches node names (normalized, multiset),
and reports precision/recall/F1 per diagram plus micro/macro over the set.

Two reporting modes (methodology/evaluation-framework.md, "reported two ways"):
  - zeros_for_failed: every test-set key scored; a missing/non-parsing
    prediction yields an empty graph -> F1 0.
  - compiled_only:   only keys whose prediction compiled (per csr_results.json).

Also reports type accuracy (companion metric, methodology §3): over the
name-matched pairs, the share whose extractor `type` agrees, with
container/internal GT types excluded from the denominator.

The PlantUML block is isolated symmetrically on both sides with
csr_runner.extract_puml, so a WoC header before @startuml is dropped the same way
for GT and predictions. An answer holding several @startuml...@enduml diagrams is
scored on its first diagram.

The defaults are scorer v2. Each v2 rule has a switch (--no-collapse-whitespace,
--no-unicode-brackets, --last-diagram, --extractor-arg=--names=raw); with every
switch off the runner reproduces scorer v1.

Usage (invoke from project root):
  python evaluation/element_f1_runner.py --pred-dir data/csr/<run>/extracted \
      --test-set data/test_set.json --csr data/csr/<run>/csr_results.json \
      --out data/element_f1/<run>
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import re
import subprocess
from glob import glob

import element_f1 as ef
from csr_runner import extract_puml

# Fork structural extractor (NOT the standard renderer). Build it from
# https://github.com/vovanrew/plantuml, branch `stats-extractor-graph`:
#   ./gradlew build -x test -x javaDoc   ->  build/libs/plantuml-1.2025.9.jar
# Point PLANTUML_EXTRACTOR_JAR at that file, or pass the path on the CLI.
EXTRACTOR_JAR = os.environ.get(
    "PLANTUML_EXTRACTOR_JAR", "plantuml-stats-extractor.jar")
EXTRACTOR_CLASS = "net.sourceforge.plantuml.stats.DiagramStatsExtractor"


def _stem(path):
    return os.path.splitext(os.path.basename(path))[0]


def write_extracted(src_files, dst_dir):
    """Isolate the PlantUML block of each source file into dst_dir/<stem>.puml."""
    os.makedirs(dst_dir, exist_ok=True)
    stems = []
    for sf in src_files:
        stem = _stem(sf)
        with open(sf, encoding="utf-8") as f:
            block = extract_puml(f.read())
        with open(os.path.join(dst_dir, stem + ".puml"), "w", encoding="utf-8") as f:
            f.write(block)
        stems.append(stem)
    return stems


# The extractor emits one record per diagram of a file: `<stem>.puml` for the
# first, `<stem>.puml_1`, `<stem>.puml_2`, ... for the following ones.
_LATER_DIAGRAM = re.compile(r"\.[A-Za-z]+_\d+$")


def graphs_from_output(stdout, first_diagram=True):
    """{stem: record} from the extractor's output, one JSON record per '\\n'.

    strict=False tolerates raw control chars the JAR leaves unescaped inside
    label/name strings (split on '\\n' rather than splitlines so a vertical-tab /
    form-feed in a label cannot wrongly break a record).

    A file with several diagrams yields several records. The first diagram is
    the one kept: it is the diagram PlantUML displays. With first_diagram=False
    each record overwrites the previous one, so the last diagram is kept (the
    scorer-v1 behaviour)."""
    graphs = {}
    for line in stdout.split("\n"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line, strict=False)
        if first_diagram and _LATER_DIAGRAM.search(rec["file"]):
            continue
        graphs[_stem(rec["file"])] = rec
    return graphs


def extract_graphs(puml_dir, jar, first_diagram=True, extractor_args=()):
    """Run the extractor JAR over a directory; return {stem: record}."""
    proc = subprocess.run(
        ["java", "-cp", jar, EXTRACTOR_CLASS, *extractor_args,
         "--dir", os.path.abspath(puml_dir)],
        capture_output=True, text=True, check=True)
    return graphs_from_output(proc.stdout, first_diagram)


def add_scorer_args(ap):
    """Scorer-v2 rule switches shared by the structural runners."""
    ap.add_argument("--no-collapse-whitespace", action="store_true",
                    help="v1: keep whitespace runs inside names")
    ap.add_argument("--no-unicode-brackets", action="store_true",
                    help="v1: do not strip U+226A/U+226B stereotype tokens")
    ap.add_argument("--no-association-direction", action="store_true",
                    help="v1: every association is undirected")
    ap.add_argument("--last-diagram", action="store_true",
                    help="v1: score the last diagram of a multi-diagram answer")
    ap.add_argument("--extractor-arg", action="append", default=[],
                    help="option passed to the extractor JAR, repeatable "
                         "(e.g. --extractor-arg=--names=raw)")


def rules_from_args(args):
    return ef.Rules(collapse_whitespace=not args.no_collapse_whitespace,
                    unicode_brackets=not args.no_unicode_brackets,
                    association_direction=not args.no_association_direction)


def scorer_record(args, rules):
    """What produced a results file: rule switches, extractor options, JAR hash."""
    with open(args.jar, "rb") as f:
        jar_sha256 = hashlib.sha256(f.read()).hexdigest()
    return {"rules": dataclasses.asdict(rules),
            "first_diagram": not args.last_diagram,
            "extractor_args": list(args.extractor_arg),
            "extractor_jar_sha256": jar_sha256}


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

    # Keys to score: test-set key list if given, else the predictions present.
    pred_files = sorted(glob(os.path.join(args.pred_dir, "*.puml"))
                        + glob(os.path.join(args.pred_dir, "*.txt")))
    have_pred = {_stem(p) for p in pred_files}
    if args.test_set:
        keys = [d["key"][:-5] for d in json.load(open(args.test_set))["diagrams"]]
    else:
        keys = sorted(have_pred)

    # Isolate PlantUML blocks symmetrically, then extract graphs from both sides.
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

    # zeros_for_failed: all keys; missing/non-parsing prediction -> empty -> F1 0.
    rows = ef.compute(gt_by_key, pred_by_key, keys, rules)
    summary = {"zeros_for_failed": ef.aggregate(rows)}
    by_key = {r["key"]: r for r in rows}

    # compiled_only: restrict to predictions that compiled (per CSR).
    compiled_keys = None
    if args.csr:
        csr = json.load(open(args.csr))
        compiled_keys = [d["key"] for d in csr["diagrams"]
                         if d.get("compiled") and d["key"] in by_key]
        summary["compiled_only"] = ef.aggregate([by_key[k] for k in compiled_keys])

    # Type accuracy (companion metric): conditional on name matches, reported
    # for the compiled population when CSR is available (pooled counts are
    # identical under zeros_for_failed — failed predictions contribute no pairs).
    ta_rows = ef.compute_type_accuracy(gt_by_key, pred_by_key, keys, rules)
    ta_by_key = {r["key"]: r for r in ta_rows}
    ta_population = compiled_keys if compiled_keys is not None else keys
    summary["type_accuracy"] = ef.aggregate_type_accuracy(
        [ta_by_key[k] for k in ta_population])
    summary["type_accuracy"]["population"] = (
        "compiled_only" if compiled_keys is not None else "all")

    compiled_set = set(compiled_keys) if compiled_keys is not None else None
    diagrams = []
    for r in rows:
        d = dict(r)
        d["has_pred"] = r["key"] in have_pred
        if compiled_set is not None:
            d["compiled"] = r["key"] in compiled_set
        ta = ta_by_key[r["key"]]
        d["type_accuracy"] = {k: ta[k] for k in ("matched", "correct", "excluded")}
        diagrams.append(d)

    out_path = os.path.join(args.out, "element_f1_results.json")
    with open(out_path, "w") as f:
        json.dump({"scorer": scorer_record(args, rules),
                   "summary": summary, "diagrams": diagrams}, f, indent=2)

    def show(label, agg):
        m, M = agg["micro"], agg["macro"]
        print(f"{label:<16} n={agg['n']:<5} "
              f"micro F1={m['f1']:.3f} (P={m['precision']:.3f} R={m['recall']:.3f})  "
              f"macro F1={M['f1']:.3f}")

    print("Element F1")
    show("zeros_for_failed", summary["zeros_for_failed"])
    if "compiled_only" in summary:
        show("compiled_only", summary["compiled_only"])
    ta = summary["type_accuracy"]
    acc = "n/a" if ta["accuracy"] is None else f"{ta['accuracy']:.3f}"
    print(f"type_accuracy    {ta['correct']}/{ta['denominator']} = {acc} "
          f"(excluded={ta['excluded']}, population={ta['population']})")
    print(f"results -> {out_path}")


if __name__ == "__main__":
    main()
