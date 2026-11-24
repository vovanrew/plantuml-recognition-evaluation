"""Two additions for the revised paper, from the stored per-diagram rows.

1. Stratum intervals: each main-panel model's CSR, Element F1 and Relationship F1
   per diagram type and per complexity tier, with 95% intervals, and the
   contrasts class - sequence and tier 1 - tier 4.
2. Serving robustness: each dense Qwen3.5 size, self-served run minus hosted run,
   with a paired 95% interval, and the scorer-v1 F1 beside the scorer-v2 F1.

The stratum intervals go to ``paper_extras.{md,json}``. The two checks go to
``paper_checks.{md,json}``, kept apart because they are internal checks and not
results of the paper (the release leaves them out).

One global draw serves everything: the 1,000 diagram positions are resampled
with the seed and count of ``analysis.bootstrap`` and each stratum's statistic
is computed on the resampled rows that fall in it. A contrast between two strata
is therefore the difference within one resample, and a resample in which a
statistic is undefined is left out (``n_valid`` counts the rest).

    python analysis/build_paper_extras.py --data-root data_paper \
        --registry analysis/model_registry_paper.json --out-dir analysis/out_paper
"""
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from analysis.bootstrap import (
    N_RESAMPLES, SEED, ci_from_values, diff_ci, make_resamples, model_stats,
)
from analysis.panel import load_eligible_models
from analysis.registry import load_registry

STATS = [
    ("csr|csr", "CSR"),
    ("element_f1|micro|zeros_for_failed", "Element F1, all"),
    ("element_f1|micro|compiled_only", "Element F1, compiled"),
    ("relationship_f1|micro|zeros_for_failed", "Relationship F1, all"),
    ("relationship_f1|micro|compiled_only", "Relationship F1, compiled"),
]
STRATA = [
    ("type", "class", lambda r: r["primary_type"] == "class"),
    ("type", "sequence", lambda r: r["primary_type"] == "sequence"),
    ("tier", "1", lambda r: r["tier"] == 1),
    ("tier", "2", lambda r: r["tier"] == 2),
    ("tier", "3", lambda r: r["tier"] == 3),
    ("tier", "4", lambda r: r["tier"] == 4),
]
CONTRASTS = [("class", "sequence"), ("1", "4")]
HOSTED_SUFFIX = "-hosted"


def _stats_on(rows: list[dict]) -> dict:
    return {sid: model_stats(rows)[sid] for sid, _ in STATS} if rows else {
        sid: None for sid, _ in STATS}


def _fmt(c: dict) -> str:
    if c.get("point") is None:
        return "n/a"
    if c.get("ci_low") is None:
        return f"{c['point']:.3f} (point only)"
    return f"{c['point']:.3f} [{c['ci_low']:.3f}, {c['ci_high']:.3f}]"


def _fmt_diff(d: dict) -> str:
    if d.get("diff_point") is None:
        return "n/a"
    if d.get("ci_low") is None:
        return f"{d['diff_point']:+.3f} (point only)"
    mark = "" if d.get("excludes_zero") else " (includes 0)"
    return f"{d['diff_point']:+.3f} [{d['ci_low']:+.3f}, {d['ci_high']:+.3f}]{mark}"


def stratum_table(models, resamples) -> dict:
    out = {}
    for m in models:
        rows = m.rows
        point, boot = {}, {}
        for _, name, pred in STRATA:
            keep = [pred(r) for r in rows]
            point[name] = _stats_on([r for r, k in zip(rows, keep) if k])
            boot[name] = [_stats_on([rows[i] for i in draw if keep[i]])
                          for draw in resamples]
        entry = {"display": m.entry.display, "strata": {}, "contrasts": {}}
        for _, name, _pred in STRATA:
            entry["strata"][name] = {
                sid: ci_from_values([b[sid] for b in boot[name]], point[name][sid])
                for sid, _ in STATS}
        for a, b in CONTRASTS:
            entry["contrasts"][f"{a} - {b}"] = {
                sid: diff_ci([x[sid] for x in boot[a]], [x[sid] for x in boot[b]],
                             point[a][sid], point[b][sid])
                for sid, _ in STATS}
        out[m.entry.id] = entry
    return out


def robustness_table(main, supplementary, resamples) -> dict:
    hosted = {m.entry.id: m for m in supplementary if m.entry.id.endswith(HOSTED_SUFFIX)}
    out = {}
    for m in main:
        h = hosted.get(m.entry.id + HOSTED_SUFFIX)
        if h is None:
            continue
        pa, pb = _stats_on(m.rows), _stats_on(h.rows)
        ba = [_stats_on([m.rows[i] for i in d]) for d in resamples]
        bb = [_stats_on([h.rows[i] for i in d]) for d in resamples]
        out[m.entry.id] = {
            "display": m.entry.display,
            "stats": {sid: {"self_served": pa[sid], "hosted": pb[sid],
                            **diff_ci([x[sid] for x in ba], [x[sid] for x in bb],
                                      pa[sid], pb[sid])}
                      for sid, _ in STATS}}
    return out


def render(strata: dict) -> str:
    L = ["# Stratum intervals", "",
         f"Paired percentile bootstrap, seed {SEED}, {N_RESAMPLES} resamples, 95% interval; "
         "one global draw, each stratum computed on the resampled rows that fall in it. "
         "\"all\" is all diagrams of the stratum (a non-compiled answer scores 0); "
         "\"compiled\" is the run's own compiled answers. F1 is micro.", ""]
    for kind, names in (("type", ["class", "sequence"]), ("tier", ["1", "2", "3", "4"])):
        contrast = "class - sequence" if kind == "type" else "1 - 4"
        for sid, label in STATS:
            L += [f"### {label} by {kind}", "",
                  "| Model | " + " | ".join(f"{kind} {n}" for n in names) + f" | {contrast} |",
                  "|---|" + "---|" * (len(names) + 1)]
            for e in strata.values():
                cells = [_fmt(e["strata"][n][sid]) for n in names]
                L.append(f"| {e['display']} | " + " | ".join(cells)
                         + f" | {_fmt_diff(e['contrasts'][contrast][sid])} |")
            L.append("")
    return "\n".join(L) + "\n"


def render_checks(robust: dict) -> str:
    L = ["# Internal checks (not results of the paper)", "",
         "## Serving robustness: self-served minus hosted", "",
          "The same model and prompt on two servings: the self-served run (one card, bf16) "
          "and the hosted run. Paired over the 1,000 diagrams.", "",
          "| Model | Statistic | self-served | hosted | difference |", "|---|---|---|---|---|"]
    for e in robust.values():
        for sid, label in STATS:
            s = e["stats"][sid]
            L.append(f"| {e['display']} | {label} | {s['self_served']:.3f} | "
                     f"{s['hosted']:.3f} | {_fmt_diff(s)} |")
    return "\n".join(L) + "\n"


def render_sensitivity(v2: dict, v1: dict) -> str:
    """Scorer v1 beside scorer v2: overall micro F1 of every main-panel model."""
    L = ["", "## Scorer sensitivity: v1 beside v2", "",
         "Overall micro F1 as `all / compiled`. CSR and chrF++ do not depend on the "
         "scorer version.", "",
         "| Model | Element F1, v1 | Element F1, v2 | Relationship F1, v1 | Relationship F1, v2 |",
         "|---|---|---|---|---|"]

    def pair(block: dict, metric: str) -> str:
        m = block["overall"][metric]
        return (f"{m['zeros_for_failed']['micro']['f1']:.3f} / "
                f"{m['compiled_only']['micro']['f1']:.3f}")

    for mid, b2 in v2["models"].items():
        b1 = v1["models"].get(mid)
        if b1 is None:
            continue
        L.append(f"| {b2['display']} | {pair(b1, 'element_f1')} | {pair(b2, 'element_f1')} | "
                 f"{pair(b1, 'relationship_f1')} | {pair(b2, 'relationship_f1')} |")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--data-root", type=Path, required=True)
    ap.add_argument("--registry", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--basename", default="paper_extras")
    ap.add_argument("--log-level", default="WARNING")
    args = ap.parse_args()
    logging.basicConfig(level=args.log_level)

    registry = load_registry(args.registry)
    main_models, _, _ = load_eligible_models(
        [e for e in registry if not e.supplementary], args.data_root)
    supp, _, _ = load_eligible_models(
        [e for e in registry if e.supplementary], args.data_root)

    resamples = make_resamples(len(main_models[0].rows), N_RESAMPLES, SEED)
    strata = stratum_table(main_models, resamples)
    robust = robustness_table(main_models, supp, resamples)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"seed": SEED, "n_resamples": N_RESAMPLES}
    (args.out_dir / f"{args.basename}.json").write_text(
        json.dumps({"meta": meta, "strata": strata}, indent=1) + "\n", encoding="utf-8")
    (args.out_dir / f"{args.basename}.md").write_text(render(strata), encoding="utf-8")
    print(args.out_dir / f"{args.basename}.md")

    checks = render_checks(robust)
    v2_path = args.out_dir / "master_table.json"
    v1_path = args.out_dir / "master_table_v1.json"
    if v2_path.exists() and v1_path.exists():
        checks += render_sensitivity(json.loads(v2_path.read_text(encoding="utf-8")),
                                     json.loads(v1_path.read_text(encoding="utf-8")))
    (args.out_dir / "paper_checks.json").write_text(
        json.dumps({"meta": meta, "robustness": robust}, indent=1) + "\n", encoding="utf-8")
    (args.out_dir / "paper_checks.md").write_text(checks, encoding="utf-8")
    print(args.out_dir / "paper_checks.md")


if __name__ == "__main__":
    main()
