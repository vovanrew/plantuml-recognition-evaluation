#!/usr/bin/env python3
"""Select stratified audit-50 keys for the manual label-validation pass.

Loads the frozen test set, excludes keys and repositories already covered by the
audit-10 first pass, then draws --per-cell keys from each (primary_type, tier)
cell with a fixed seed. The repo-disjoint guarantee is global: no two selected
keys share a repository, so each diagram is an independent draw from a distinct
project. The selected key list is written as the reproducibility artifact.

Smoke run (per project convention):
    python3 util/select_audit50.py --per-cell 1 --dry-run

Real run:
    python3 util/select_audit50.py --per-cell 5
"""
from __future__ import annotations

import argparse
import json
import os
import random
from collections import defaultdict

# Audit-10 keys from the first validation pass, locked here so this file is the
# self-contained selection record.
AUDIT10_KEYS = [
    "000133b38e70cfb70834681221553363e9f37714.puml",
    "008c6a6b50e161de77bd77f0e2ec740338e46f6d.puml",
    "00b4fb3b3308858bd81708f49aa4137d440dc178.puml",
    "01325068fa93284336d6055e819ad4dd59251533.puml",
    "013f262fafb9cce412d05966af0aca59982ed3f2.puml",
    "01dc8e46963f6e5d63634cf04af97c014aa5d965.puml",
    "031323e4864971cf223ecb69cb6a9c3c5c4fd0e1.puml",
    "0348c6cacb29ed7cc29bb3d32701aaa613959137.puml",
    "077e15622b3991ab16cb96332f12a384c534bb6d.puml",
    "09bc09780e50abf92d747f85119ea9ce3da32472.puml",
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test-set", default="data/test_set.json")
    ap.add_argument("--per-cell", type=int, default=5,
                    help="keys to draw from each of the 8 (type, tier) cells")
    ap.add_argument("--seed", type=int, default=50,
                    help="random.Random seed; recorded with the selection")
    ap.add_argument("--out", default="audit50_keys.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the selection but do not write the artifact")
    args = ap.parse_args()

    diagrams = json.load(open(args.test_set))["diagrams"]
    by_key = {d["key"]: d for d in diagrams}

    audit10_set = set(AUDIT10_KEYS)
    audit10_repos = {by_key[k]["repository"] for k in AUDIT10_KEYS if k in by_key}

    # Bucket the candidate pool by (primary_type, tier).
    cells = defaultdict(list)
    for d in diagrams:
        if d["key"] in audit10_set:
            continue
        if d["repository"] in audit10_repos:
            continue
        cells[(d["primary_type"], d["tier"])].append(d)

    rng = random.Random(args.seed)
    selected = []
    used_repos = set()

    # Walk cells in a fixed order so the seed is reproducible.
    for cell_key in sorted(cells):
        pool = list(cells[cell_key])
        rng.shuffle(pool)
        picked = 0
        for d in pool:
            if picked == args.per_cell:
                break
            if d["repository"] in used_repos:
                continue
            selected.append(d)
            used_repos.add(d["repository"])
            picked += 1
        if picked < args.per_cell:
            raise SystemExit(
                f"cell {cell_key}: only {picked} repo-disjoint candidates after "
                f"excluding audit-10; need {args.per_cell}")

    # Summary for the operator.
    print(f"seed={args.seed} per_cell={args.per_cell} total={len(selected)}")
    print(f"audit10 excluded: {len(audit10_set)} keys / {len(audit10_repos)} repos")
    by_cell = defaultdict(list)
    for d in selected:
        by_cell[(d["primary_type"], d["tier"])].append(d)
    for cell_key in sorted(by_cell):
        ds = by_cell[cell_key]
        print(f"  {cell_key[0]} T{cell_key[1]}: {len(ds)} keys")
        for d in ds:
            print(f"    {d['key']}  {d['repository']}")
    repo_overlap = used_repos & audit10_repos
    assert not repo_overlap, f"repo overlap with audit-10: {repo_overlap}"
    assert len(used_repos) == len(selected), "repo-disjoint within selection violated"

    keys = [d["key"] for d in selected]
    if args.dry_run:
        print("\n--dry-run: not writing artifact")
        return
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(keys, f, indent=2)
    print(f"\nwrote {len(keys)} keys to {args.out}")


if __name__ == "__main__":
    main()
