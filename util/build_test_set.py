#!/usr/bin/env python3
"""Build the curated image-to-PlantUML evaluation set.

Pipeline (per type in {class, sequence}), per methodology/test-set-construction.md:
  1. Inclusion filter (metadata only).
  2. Degeneracy exclusion (newpage multipage / renderer-clip / extreme aspect),
     using PNG dimensions read directly from the STORED image zip.
  3. Normalized-code deduplication (strip comments + collapse whitespace, hash).
  4. content_lines quartile stratification (4 tiers, computed per surviving pool).
  5. Repo-capped, fixed-seed stratified sampling (n per cell; <=5 per repository,
     cap is global across the whole test set).

The artifact is keyed by FILENAME KEY ({blob_id}.puml or {blob_id}_{NN}.puml),
never bare blob_id.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import tempfile
import time
import zipfile
from collections import defaultdict

import numpy as np

# Root of the mined 143k-pair corpus (NOT the 1000-diagram test set shipped with
# this repo). Point PLANTUML_DATASET_ROOT at it, or override each path on the CLI.
DATASET = os.environ.get("PLANTUML_DATASET_ROOT", "dataset/zenodo_content")
DEFAULT_METADATA = f"{DATASET}/uml_metadata_enriched.json"
DEFAULT_IMAGES_ZIP = f"{DATASET}/puml_images.zip"
DEFAULT_PUML_DIR = f"{DATASET}/puml_files"

# Fork structural extractor (NOT the standard renderer). Build it from
# https://github.com/vovanrew/plantuml, branch `stats-extractor-graph`:
#   ./gradlew build -x test -x javaDoc   ->  build/libs/plantuml-1.2025.9.jar
# Point PLANTUML_EXTRACTOR_JAR at that file, or pass the path on the CLI.
EXTRACTOR_JAR = os.environ.get(
    "PLANTUML_EXTRACTOR_JAR", "plantuml-stats-extractor.jar")
# Supplies the parser diagram_type used by the type-agreement filter (stage 3b).
EXTRACTOR_CLASS = "net.sourceforge.plantuml.stats.DiagramStatsExtractor"

TYPES = ("class", "sequence")
ELEMENTS_MAX = 50
CLIP_LONG_EDGE = 16384      # renderer bitmap limit
ASPECT_MAX = 8.0            # long/short edge
REPO_CAP = 5               # max diagrams per repository, global across the set

_TRAILING_PAGE = re.compile(r"_\d+$")
_BLOCK_COMMENT = re.compile(r"/'.*?'/", re.DOTALL)
_WS = re.compile(r"\s+")


# --------------------------------------------------------------------------- #
# Stage 1: inclusion filter
# --------------------------------------------------------------------------- #
def load_candidates(metadata_path):
    """Return {type: {key: record}} for records passing the inclusion filter."""
    with open(metadata_path) as f:
        records = json.load(f)["classifications"]

    out = {t: {} for t in TYPES}
    for key, rec in records.items():
        t = rec.get("primary_type")
        if t not in TYPES:
            continue
        if rec.get("secondary_types") != []:
            continue
        if rec.get("extraction_error") is not None:
            continue
        if rec.get("truncated") is True:   # field present on only 67 records
            continue
        if rec.get("elements_total", 0) > ELEMENTS_MAX:
            continue
        if not rec.get("repository"):
            continue
        out[t][key] = rec
    return out, set(records.keys())


# --------------------------------------------------------------------------- #
# Stage 2: image dimensions + degeneracy exclusion
# --------------------------------------------------------------------------- #
def png_dims(zf, info):
    """Read (width, height) from a PNG's IHDR without decoding the image."""
    with zf.open(info) as fh:
        head = fh.read(26)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def map_pages_to_bases(images_zip, all_bases):
    """Group PNG pages by the diagram base that owns them.

    A PNG stem matches its diagram base exactly (single page) or after stripping
    one trailing _NN (a newpage page). Exact match wins, so a split sibling's own
    single-page image is never mistaken for a newpage page of its parent.

    Returns {base: [(w, h), ...]} over all owned PNG pages.
    """
    zf = zipfile.ZipFile(images_zip)
    pages = defaultdict(list)
    orphans = 0
    for info in zf.infolist():
        name = info.filename
        if not name.endswith(".png"):
            continue
        stem = name[name.rfind("/") + 1 : -4]
        if stem in all_bases:
            owner = stem
        else:
            stripped = _TRAILING_PAGE.sub("", stem, count=1)
            if stripped != stem and stripped in all_bases:
                owner = stripped
            else:
                orphans += 1
                continue
        dims = png_dims(zf, info)
        if dims is not None:
            pages[owner].append(dims)
    return pages, orphans


def degeneracy_label(dims_list):
    """Return None if the diagram is a usable single image, else a reason."""
    if len(dims_list) == 0:
        return "no_image"
    if len(dims_list) > 1:
        return "multipage"
    w, h = dims_list[0]
    long_edge, short_edge = max(w, h), min(w, h)
    if long_edge >= CLIP_LONG_EDGE:
        return "clipped"
    if short_edge == 0 or long_edge / short_edge > ASPECT_MAX:
        return "aspect"
    return None


# --------------------------------------------------------------------------- #
# Stage 3: normalized-code dedup
# --------------------------------------------------------------------------- #
def normalized_code(path):
    """Strip PlantUML comments and collapse whitespace for dedup hashing."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    text = _BLOCK_COMMENT.sub(" ", text)
    kept = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("'"):   # blank or full-line comment
            continue
        kept.append(s)
    return _WS.sub(" ", " ".join(kept)).strip()


# --------------------------------------------------------------------------- #
# Stage 3b: type-agreement filter (parser diagram_type == metadata primary_type)
# --------------------------------------------------------------------------- #
def parser_diagram_types(keys, puml_dir, jar):
    """Batch-parse the given filename keys with the fork extractor.

    Returns {key: diagram_type}; a key that fails to parse maps to "" (and so
    never agrees with any metadata type). Files are symlinked into a temp dir so
    one JVM run handles the whole pool via --dir."""
    types = {}
    with tempfile.TemporaryDirectory() as tmp:
        for key in keys:
            src = os.path.abspath(os.path.join(puml_dir, key))
            if os.path.exists(src):
                os.symlink(src, os.path.join(tmp, key))
        proc = subprocess.run(
            ["java", "-cp", jar, EXTRACTOR_CLASS, "--dir", tmp],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
        # One record per '\n'. strict=False tolerates raw control chars the JAR
        # leaves unescaped inside label/name strings; a record that still fails to
        # parse is skipped (its key gets no type -> treated as a disagreement).
        unparsed = 0
        for line in proc.stdout.split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line, strict=False)
            except json.JSONDecodeError:
                unparsed += 1
                continue
            types[rec["file"]] = rec.get("diagram_type") or ""
        if unparsed:
            print(f"    (note: {unparsed} extractor lines unparseable, treated as disagreements)")
    return types


# --------------------------------------------------------------------------- #
# Stage 4 + 5: stratify and sample
# --------------------------------------------------------------------------- #
def quartile_thresholds(values):
    q1, q2, q3 = (float(np.percentile(values, p)) for p in (25, 50, 75))
    return q1, q2, q3


def assign_tier(content_lines, thr):
    q1, q2, q3 = thr
    if content_lines <= q1:
        return 1
    if content_lines <= q2:
        return 2
    if content_lines <= q3:
        return 3
    return 4


def sample_cells(by_cell, n_per_cell, seed):
    """Seeded, repo-capped selection. Returns (selected_keys, per_cell_stats)."""
    rng = np.random.default_rng(seed)
    repo_count = defaultdict(int)
    selected = []
    stats = {}
    # Fixed cell order for reproducibility: class T1..T4, then sequence T1..T4.
    for t in TYPES:
        for tier in (1, 2, 3, 4):
            keys = list(by_cell[(t, tier)])
            order = rng.permutation(len(keys))
            picked = []
            for idx in order:
                key, rec = keys[idx]
                repo = rec["repository"]
                if repo_count[repo] >= REPO_CAP:
                    continue
                picked.append((key, rec))
                repo_count[repo] += 1
                if len(picked) >= n_per_cell:
                    break
            selected.extend(picked)
            stats[(t, tier)] = {"available": len(keys), "selected": len(picked)}
    return selected, stats


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #
def build(args):
    t0 = time.time()
    print("[1] inclusion filter ...", flush=True)
    candidates, all_keys = load_candidates(args.metadata)
    all_bases = {k[:-5] for k in all_keys}
    for t in TYPES:
        print(f"    {t}: {len(candidates[t]):,} candidates")

    if args.smoke:
        for t in TYPES:
            keys = sorted(candidates[t])[: args.smoke]
            candidates[t] = {k: candidates[t][k] for k in keys}
        print(f"    SMOKE: capped to {args.smoke}/type "
              f"({sum(len(candidates[t]) for t in TYPES)} total)")

    print(f"[2] image dims + degeneracy ... ({time.time()-t0:.0f}s)", flush=True)
    pages, orphans = map_pages_to_bases(args.images_zip, all_bases)
    print(f"    mapped PNG owners; {orphans:,} orphan pages ignored")

    survivors = {t: {} for t in TYPES}
    drops = {t: defaultdict(int) for t in TYPES}
    for t in TYPES:
        for key, rec in candidates[t].items():
            base = key[:-5]
            reason = degeneracy_label(pages.get(base, []))
            if reason is None:
                w, h = pages[base][0]
                rec = dict(rec, _w=w, _h=h)
                survivors[t][key] = rec
            else:
                drops[t][reason] += 1
    for t in TYPES:
        d = drops[t]
        print(f"    {t}: {len(survivors[t]):,} survive "
              f"(drops: { {k: v for k, v in d.items()} })")

    print(f"[3] normalized-code dedup ... ({time.time()-t0:.0f}s)", flush=True)
    deduped = {t: {} for t in TYPES}
    for t in TYPES:
        seen = set()
        dups = 0
        for key, rec in survivors[t].items():
            norm = normalized_code(f"{args.puml_dir}/{key}")
            h = hashlib.sha1(norm.encode("utf-8")).hexdigest()
            if h in seen:
                dups += 1
                continue
            seen.add(h)
            deduped[t][key] = rec
        print(f"    {t}: {len(deduped[t]):,} unique ({dups:,} dropped)")

    print(f"[3b] type-agreement filter (parser diagram_type == primary_type) ... "
          f"({time.time()-t0:.0f}s)", flush=True)
    ptypes = parser_diagram_types(
        [k for t in TYPES for k in deduped[t]], args.puml_dir, args.extractor_jar)
    agreed = {t: {} for t in TYPES}
    for t in TYPES:
        disagree = defaultdict(int)
        for key, rec in deduped[t].items():
            pt = ptypes.get(key, "")
            if pt == t:
                agreed[t][key] = rec
            else:
                disagree[pt or "<unparsed>"] += 1
        print(f"    {t}: {len(agreed[t]):,} agree "
              f"(dropped { {k: v for k, v in disagree.items()} })")
    deduped = agreed

    print(f"[4] stratify (content_lines quartiles) ... ({time.time()-t0:.0f}s)",
          flush=True)
    thresholds = {}
    by_cell = defaultdict(list)
    for t in TYPES:
        cl = np.array([r["content_lines"] for r in deduped[t].values()])
        thr = quartile_thresholds(cl)
        thresholds[t] = thr
        print(f"    {t}: Q1/Q2/Q3 = {thr[0]:.0f}/{thr[1]:.0f}/{thr[2]:.0f}")
        for key, rec in deduped[t].items():
            tier = assign_tier(rec["content_lines"], thr)
            by_cell[(t, tier)].append((key, rec))

    print(f"[5] repo-capped seeded sample (n={args.n_per_cell}/cell, "
          f"seed={args.seed}) ... ({time.time()-t0:.0f}s)", flush=True)
    selected, cell_stats = sample_cells(by_cell, args.n_per_cell, args.seed)

    write_artifact(args, selected, thresholds, cell_stats)
    print_summary(selected, thresholds, cell_stats)
    print(f"\ndone in {time.time()-t0:.0f}s -> {args.out}")
    return selected


def write_artifact(args, selected, thresholds, cell_stats):
    records = []
    for key, rec in selected:
        tier = assign_tier(rec["content_lines"], thresholds[rec["primary_type"]])
        records.append({
            "key": key,
            "blob_id": rec["blob_id"],
            "primary_type": rec["primary_type"],
            "tier": tier,
            "content_lines": rec["content_lines"],
            "elements_total": rec["elements_total"],
            "connections_total": rec["connections_total"],
            "repository": rec["repository"],
            "image_width": rec["_w"],
            "image_height": rec["_h"],
        })
    records.sort(key=lambda r: (r["primary_type"], r["tier"], r["key"]))
    artifact = {
        "config": {
            "seed": args.seed,
            "n_per_cell": args.n_per_cell,
            "repo_cap": REPO_CAP,
            "elements_max": ELEMENTS_MAX,
            "clip_long_edge": CLIP_LONG_EDGE,
            "aspect_max": ASPECT_MAX,
            "type_agreement_filter": True,
            "smoke": args.smoke,
        },
        "quartile_thresholds": {
            t: {"q1": thresholds[t][0], "q2": thresholds[t][1],
                "q3": thresholds[t][2]} for t in TYPES
        },
        "cell_stats": {f"{t}_T{tier}": cell_stats[(t, tier)]
                       for t in TYPES for tier in (1, 2, 3, 4)},
        "count": len(records),
        "diagrams": records,
    }
    with open(args.out, "w") as f:
        json.dump(artifact, f, indent=2)


def print_summary(selected, thresholds, cell_stats):
    mp = defaultdict(list)
    for _, rec in selected:
        tier = assign_tier(rec["content_lines"], thresholds[rec["primary_type"]])
        mp[(rec["primary_type"], tier)].append(rec["_w"] * rec["_h"] / 1e6)
    print("\n  per-stratum summary (selected / available, median MP):")
    print("  type      T1            T2            T3            T4")
    for t in TYPES:
        cells = []
        for tier in (1, 2, 3, 4):
            s = cell_stats[(t, tier)]
            med = float(np.median(mp[(t, tier)])) if mp[(t, tier)] else 0.0
            cells.append(f"{s['selected']:>3}/{s['available']:<5} {med:>5.2f}MP")
        print(f"  {t:<8}  " + "  ".join(cells))
    # monotonicity check
    for t in TYPES:
        meds = [np.median(mp[(t, tier)]) if mp[(t, tier)] else 0
                for tier in (1, 2, 3, 4)]
        ok = all(meds[i] < meds[i + 1] for i in range(3))
        print(f"  {t}: median MP monotonic across tiers? {ok}  ({[round(m,2) for m in meds]})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default=DEFAULT_METADATA)
    ap.add_argument("--images-zip", default=DEFAULT_IMAGES_ZIP)
    ap.add_argument("--puml-dir", default=DEFAULT_PUML_DIR)
    ap.add_argument("--extractor-jar", default=EXTRACTOR_JAR,
                    help="fork DiagramStatsExtractor JAR for the type-agreement filter")
    ap.add_argument("--n-per-cell", type=int, default=125)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--smoke", type=int, default=0,
                    help="cap candidate pool to N/type for a fast plumbing test")
    ap.add_argument("--out", default="test_set.json")
    build(ap.parse_args())


if __name__ == "__main__":
    main()
