#!/usr/bin/env python3
"""Compilation Success Rate (CSR) runner (metric 1).

Given a directory of raw model outputs (one file per diagram, stem = diagram
key), extracts the PlantUML block from each, compiles the whole batch with
plantuml.jar, and scores each diagram as compiled iff PlantUML produced a
non-empty PNG (byte-size floor). A failed compile yields no PNG (`--no-error-image`).

CSR is computed over the full expected key set when `--test-set` is given, so a
missing prediction (e.g. an inference timeout) correctly counts as a failure.

Outputs <out>/csr_results.json (summary + per-diagram) plus the extracted .puml
and rendered PNGs for inspection / downstream metrics.

Usage (invoke from project root):
  python3 evaluation/csr_runner.py --pred-dir data/runs/<run> --out data/csr/<run>
  python3 evaluation/csr_runner.py --pred-dir <dir> --test-set data/test_set.json --out <dir>
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from glob import glob

JAR = "plantuml-1.2025.9.jar"


def extract_puml(text):
    """Isolate the PlantUML block from a raw model response.

    Takes the span from the first @startuml to the last @enduml (drops markdown
    fences / prose around it). Falls back to the fence-stripped text so a missing
    @enduml still gets a compile attempt (and an honest failure)."""
    s = text.find("@startuml")
    e = text.rfind("@enduml")
    if s != -1 and e != -1 and e > s:
        return text[s:e + len("@enduml")]
    return text.strip().strip("`").strip()


def matched_pngs(stem, png_dir):
    """PNGs belonging to a diagram: exact stem, plus PlantUML @newpage pages
    stem_001.png, stem_002.png, ... (3-digit suffix, per the renderer)."""
    out = []
    exact = os.path.join(png_dir, stem + ".png")
    if os.path.exists(exact):
        out.append(exact)
    for p in glob(os.path.join(png_dir, stem + "_*.png")):
        suffix = os.path.basename(p)[len(stem) + 1:-4]
        if suffix.isdigit() and len(suffix) == 3:
            out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pred-dir", required=True,
                    help="dir of raw model outputs (*.puml / *.txt), stem = diagram key")
    ap.add_argument("--out", required=True, help="results dir")
    ap.add_argument("--test-set", default="",
                    help="optional test_set.json: score over its full key set "
                         "(missing predictions count as failures)")
    ap.add_argument("--min-png-bytes", type=int, default=256,
                    help="a PNG below this is treated as an empty/degenerate render")
    ap.add_argument("--jar", default=JAR)
    args = ap.parse_args()

    extracted_dir = os.path.join(args.out, "extracted")
    png_dir = os.path.join(args.out, "png")
    os.makedirs(extracted_dir, exist_ok=True)
    os.makedirs(png_dir, exist_ok=True)

    # 1. Extract the PlantUML block from each prediction file.
    pred_files = sorted(glob(os.path.join(args.pred_dir, "*.puml"))
                        + glob(os.path.join(args.pred_dir, "*.txt")))
    have_pred = set()
    for pf in pred_files:
        stem = os.path.splitext(os.path.basename(pf))[0]
        with open(pf, encoding="utf-8") as f:
            code = extract_puml(f.read())
        with open(os.path.join(extracted_dir, stem + ".puml"), "w", encoding="utf-8") as f:
            f.write(code)
        have_pred.add(stem)

    # 2. Compile the whole batch in one JVM (proven command from the corpus
    #    pipeline). --no-error-image => a failed compile produces no PNG.
    errors_log = os.path.join(args.out, "errors.log")
    with open(errors_log, "w") as elog:
        subprocess.run(
            ["java", "-jar", args.jar, "--threads", "auto",
             "--output-dir", os.path.abspath(png_dir), "-tpng", "-stdrpt",
             "--no-error-image", os.path.join(extracted_dir, "*.puml")],
            stdout=subprocess.DEVNULL, stderr=elog, check=False)

    # 3. Map each failed file to its first error line, for analysis.
    err_by_stem = {}
    with open(errors_log, encoding="utf-8", errors="replace") as f:
        for line in f:
            if " in file: " in line:
                path = line.rsplit(" in file: ", 1)[1].strip()
                stem = os.path.splitext(os.path.basename(path))[0]
                err_by_stem.setdefault(stem, line.strip())

    # 4. Score. Denominator = test-set keys if given, else the predictions found.
    if args.test_set:
        keys = [d["key"][:-5] for d in json.load(open(args.test_set))["diagrams"]]
    else:
        keys = sorted(have_pred)

    results, compiled = [], 0
    for stem in keys:
        if stem not in have_pred:
            results.append({"key": stem, "compiled": False, "n_png": 0,
                            "png_bytes": 0, "error": "no prediction (missing/timeout)"})
            continue
        pngs = matched_pngs(stem, png_dir)
        total_bytes = sum(os.path.getsize(p) for p in pngs)
        ok = bool(pngs) and total_bytes >= args.min_png_bytes
        compiled += ok
        results.append({
            "key": stem, "compiled": ok, "n_png": len(pngs),
            "png_bytes": total_bytes,
            "error": None if ok else err_by_stem.get(stem,
                     "empty/degenerate render" if pngs else "no PNG produced"),
        })

    n = len(keys)
    summary = {"pred_dir": args.pred_dir, "n": n, "compiled": compiled,
               "csr": round(compiled / n, 4) if n else 0.0,
               "min_png_bytes": args.min_png_bytes}
    with open(os.path.join(args.out, "csr_results.json"), "w") as f:
        json.dump({"summary": summary, "diagrams": results}, f, indent=2)

    print(f"CSR = {compiled}/{n} = {summary['csr']:.1%}")
    print(f"results -> {os.path.join(args.out, 'csr_results.json')}")
    fails = [r for r in results if not r["compiled"]]
    if fails:
        print(f"\n{len(fails)} failed:")
        for r in fails:
            print(f"  {r['key'][:24]:<26} {r['error']}")


if __name__ == "__main__":
    main()
