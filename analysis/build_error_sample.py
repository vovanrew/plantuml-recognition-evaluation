"""The error-analysis sample: one failure case per model x diagram type x tier x failure class.

``draw`` picks the cases with the failure sampler (``select_cell``, the project seed), gives each
a blind id in a shuffled order, and writes for every case a file the coder reads (ground truth,
answer with display-only lines removed, renderer message or structural diff) with its image. The
unblinded key goes to ``keys.json`` before any case is coded. One case per cell shows the kinds of
failure, not how often each occurs.

``report`` joins the two coders' files with the key: agreement, the cases for the author, and the
code counts per model.

    python -m analysis.build_error_sample draw   --data-root data_paper \
        --registry analysis/model_registry_paper.json --out analysis/out_paper/error_sample
    python -m analysis.build_error_sample report --out analysis/out_paper/error_sample

The design and the case format follow the fine-tuning study's error analysis.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import random
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evaluation"))

import element_f1 as ef  # noqa: E402
import relationship_f1 as rf  # noqa: E402
from csr_runner import extract_puml  # noqa: E402
from element_f1_runner import extract_graphs, write_extracted  # noqa: E402

from analysis.aggregate import TIERS, TYPES  # noqa: E402
from analysis.failure_sampler import (  # noqa: E402
    SEED, cell_seed_key, outcome_class, select_cell,
)
from analysis.loader import load_panel  # noqa: E402
from analysis.registry import load_registry  # noqa: E402

CODEBOOK = Path(__file__).with_name("error_codebook.md")
JAR = ROOT / "plantuml-stats-extractor-v2.jar"
FAILURES = ("compile_fail", "compiled_low_structural")
CODES = ["C1", "C2", "C3", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "M"]
DISPLAY_MAX_LINES = 120  # longer answers are shown as the first 90 and last 30 lines

_DISPLAY_ONLY = re.compile(
    r"^\s*(skinparam\b|title\b|hide\b|show\b|scale\b|left\s+to\s+right\s+direction\b|"
    r"top\s+to\s+bottom\s+direction\b|!|')", re.I)


def sha256(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# --------------------------------------------------------------------------- #
# the sample
# --------------------------------------------------------------------------- #
def draw_sample(models) -> list[dict]:
    """One case per model x type x tier x failure class, with blind ids."""
    cases = []
    for md in models:
        cells = collections.defaultdict(list)
        for row in md.rows:
            oc = outcome_class(row)
            if oc in FAILURES:
                cells[(row["primary_type"], row["tier"], oc)].append(row)
        for typ in TYPES:
            for tier in TIERS:
                for oc in FAILURES:
                    bucket = cells.get((typ, tier, oc), [])
                    for row in select_cell(bucket, 1, cell_seed_key(md.entry.id, typ, tier, oc)):
                        cases.append({"model_id": md.entry.id, "run_dir": md.entry.run_dir,
                                      "key": row["key"], "primary_type": typ, "tier": tier,
                                      "class": oc, "available": len(bucket)})
    order = list(range(len(cases)))
    random.Random(f"{SEED}|error-analysis|blind").shuffle(order)
    width = len(str(len(cases)))
    for n, i in enumerate(order, 1):
        cases[i]["case"] = f"E{n:0{width}d}"
    return sorted(cases, key=lambda c: c["case"])


# --------------------------------------------------------------------------- #
# what the coder sees
# --------------------------------------------------------------------------- #
def isolate(text: str) -> str:
    """The answer's PlantUML block for display: first @startuml to last @enduml, or to the end."""
    s = text.find("@startuml")
    body = text[s:] if s != -1 else text
    e = body.rfind("@enduml")
    if e != -1:
        return body[:e + len("@enduml")]
    return re.sub(r"\n?```\s*$", "", body.rstrip())


def strip_display(block: str) -> tuple[list[str], list[str]]:
    """(shown lines, stripped lines): display-only lines, skinparam blocks and block comments out."""
    shown, stripped = [], []
    depth, in_comment = 0, False
    for line in block.split("\n"):
        s = line.strip()
        if in_comment:
            stripped.append(line)
            in_comment = "'/" not in s
            continue
        if depth:
            stripped.append(line)
            depth = max(depth + s.count("{") - s.count("}"), 0)
            continue
        if s.startswith("/'"):
            stripped.append(line)
            in_comment = "'/" not in s[2:]
            continue
        if _DISPLAY_ONLY.match(line):
            stripped.append(line)
            if re.match(r"^\s*skinparam\b", line, re.I):
                depth = max(s.count("{") - s.count("}"), 0)
            continue
        shown.append(line)
    return shown, stripped


def clip(lines: list[str]) -> list[str]:
    if len(lines) <= DISPLAY_MAX_LINES:
        return lines
    return lines[:90] + [f"... {len(lines) - 120} lines omitted ..."] + lines[-30:]


def renderer_note(csr_row: dict, text: str) -> str:
    err = csr_row.get("error") or ""
    parts = []
    if "@enduml" not in text:
        parts.append("The answer has no `@enduml`.")
    m = re.match(r"Error line (\d+)", err)
    if m:
        lines = extract_puml(text).split("\n")
        n = int(m.group(1))
        src = lines[n - 1] if 0 < n <= len(lines) else "(line not in the block)"
        parts.append(f"Renderer: error at line {n} of the answer block: `{src.strip()}`")
    elif err:
        parts.append(f"Renderer: {err.split(' in file:')[0]}")
    return " ".join(parts)


def _counter_lines(c) -> str:
    return ", ".join(f"`{k}`" + (f" ×{v}" if v > 1 else "") for k, v in sorted(c.items())) or "none"


def _edge_text(k) -> str:
    return f"{k[0]} -> {k[1]} : {k[2]}" + (" (one arrowhead)" if len(k) > 3 else "")


def structural_diff(gt_rec, pred_rec) -> dict:
    gn = collections.Counter(ef.names_from_record(gt_rec or {}))
    pn = collections.Counter(ef.names_from_record(pred_rec or {}))
    ge = collections.Counter(_edge_text(k) for k in rf.edges_from_record(gt_rec or {}))
    pe = collections.Counter(_edge_text(k) for k in rf.edges_from_record(pred_rec or {}))
    return {"nodes": {"matched": gn & pn, "missed": gn - pn, "spurious": pn - gn},
            "edges": {"matched": ge & pe, "missed": ge - pe, "spurious": pe - ge}}


def case_markdown(case, gt_text, shown, n_stripped, note, diff, el_f1, rel_f1) -> str:
    cid = case["case"]
    out = [f"# Case {cid}", "",
           f"Diagram type: {case['primary_type']} · tier {case['tier']} · outcome: "
           f"{'compile fail' if case['class'] == 'compile_fail' else 'compiled low-structural'}",
           f"Image: `{cid}.png`", "", "## Ground truth", "", "```plantuml", gt_text.rstrip(), "```",
           "", f"## Answer ({n_stripped} display-only lines removed; they are in "
           f"`{cid}.stripped.txt`)", "", "```plantuml", *clip(shown), "```", ""]
    if case["class"] == "compile_fail":
        out += ["## Renderer", "", note or "Renderer: no PNG produced.", ""]
    else:
        out += ["## Structural diff", "",
                f"Element F1 {el_f1:.3f} · Relationship F1 {rel_f1:.3f}", ""]
        for part in ("nodes", "edges"):
            for kind in ("matched", "missed", "spurious"):
                c = diff[part][kind]
                out.append(f"- {part} {kind} ({sum(c.values())}): {_counter_lines(c)}")
        out.append("")
    return "\n".join(out)


def extract_cases(cases, data_root: Path) -> tuple[dict, dict]:
    """Re-extract the graphs of the sampled diagrams only: ({key: gt}, {(run, key): answer}).
    An answer whose element row says ``has_pred`` False gets no graph (it was held back)."""
    with tempfile.TemporaryDirectory() as tmp:
        keys = sorted({c["key"] for c in cases})
        write_extracted([str(data_root / "puml_files" / f"{k}.puml") for k in keys],
                        str(Path(tmp) / "gt"))
        gt = extract_graphs(str(Path(tmp) / "gt"), str(JAR))
        pred = {}
        by_run = collections.defaultdict(list)
        for c in cases:
            if c["class"] == "compiled_low_structural":
                by_run[c["run_dir"]].append(c["key"])
        for run, ks in by_run.items():
            d = Path(tmp) / "runs" / run
            write_extracted([str(data_root / "runs" / run / f"{k}.puml") for k in ks], str(d))
            for k, rec in extract_graphs(str(d), str(JAR)).items():
                pred[(run, k)] = rec
    return gt, pred


def check_case(row, gt_rec, pred_rec, case) -> None:
    """The re-extracted graphs must reproduce the stored per-diagram counts."""
    g = ef.prf(ef.names_from_record(gt_rec), ef.names_from_record(pred_rec or {}))
    s = row["element"]
    if (g["tp"], g["fp"], g["fn"]) != (s["tp"], s["fp"], s["fn"]):
        raise SystemExit(f"{case['case']}: re-extracted element counts differ from the stored row")
    g = ef.prf(rf.edges_from_record(gt_rec), rf.edges_from_record(pred_rec or {}))
    s = row["relationship"]
    if (g["tp"], g["fp"], g["fn"]) != (s["tp"], s["fp"], s["fn"]):
        raise SystemExit(f"{case['case']}: re-extracted edge counts differ from the stored row")


def cmd_draw(args) -> None:
    out = Path(args.out)
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out}: exists and is not empty; the sample is drawn once")
    data_root = Path(args.data_root)
    registry = [e for e in load_registry(args.registry) if not e.supplementary]
    models = load_panel(registry, data_root)
    rows = {m.entry.id: {r["key"]: r for r in m.rows} for m in models}
    cases = draw_sample(models)
    gt, pred = extract_cases(cases, data_root)

    cdir = out / "cases"
    cdir.mkdir(parents=True)
    for c in cases:
        k, run = c["key"], c["run_dir"]
        row = rows[c["model_id"]][k]
        text = (data_root / "runs" / run / f"{k}.puml").read_text(encoding="utf-8",
                                                                   errors="replace")
        shown, stripped = strip_display(isolate(text))
        diff = None
        if c["class"] == "compiled_low_structural":
            check_case(row, gt[k], pred.get((run, k)), c)
            diff = structural_diff(gt[k], pred.get((run, k)))
        gt_text = (data_root / "puml_files" / f"{k}.puml").read_text(encoding="utf-8",
                                                                      errors="replace")
        (cdir / f"{c['case']}.md").write_text(
            case_markdown(c, gt_text, shown, len(stripped), renderer_note(row["csr"], text),
                          diff, row["element"]["f1"], row["relationship"]["f1"]),
            encoding="utf-8")
        (cdir / f"{c['case']}.stripped.txt").write_text("\n".join(stripped) + "\n",
                                                        encoding="utf-8")
        shutil.copyfile(data_root / "puml_images_1568" / f"{k}.png", cdir / f"{c['case']}.png")
    shutil.copyfile(CODEBOOK, out / "error_codebook.md")
    keys = {"_doc": "The unblinded key of the error-analysis sample. Coders never read this file.",
            "seed": SEED, "codebook_sha256": sha256(CODEBOOK),
            "build_error_sample_sha256": sha256(__file__), "jar_sha256": sha256(JAR),
            "registry": str(args.registry), "n_cases": len(cases), "cases": cases}
    (out / "keys.json").write_text(json.dumps(keys, indent=1) + "\n", encoding="utf-8")
    print(f"drawn: {len(cases)} cases into {cdir}; key {out / 'keys.json'}")


# --------------------------------------------------------------------------- #
# report
# --------------------------------------------------------------------------- #
def load_codes(path: Path) -> dict:
    codes = {}
    for f in sorted(path.glob("*.json")):
        codes.update(json.loads(f.read_text(encoding="utf-8")))
    return codes


def cmd_report(args) -> None:
    out = Path(args.out)
    keys = json.loads((out / "keys.json").read_text(encoding="utf-8"))
    if sha256(out / "error_codebook.md") != keys["codebook_sha256"]:
        raise SystemExit("the codebook differs from the one the sample was drawn with")
    a, b = load_codes(out / "codes_a"), load_codes(out / "codes_b")
    final_path = out / "codes_final.json"
    final = json.loads(final_path.read_text(encoding="utf-8")) if final_path.exists() else {}
    cases = keys["cases"]
    missing = [c["case"] for c in cases if c["case"] not in a or c["case"] not in b]
    if missing:
        raise SystemExit(f"{len(missing)} cases lack a code from one coder, e.g. {missing[:5]}")

    agree = [c for c in cases if a[c["case"]]["primary"] == b[c["case"]]["primary"]]
    review = [c for c in cases
              if a[c["case"]]["primary"] != b[c["case"]]["primary"]
              or a[c["case"]].get("ask_author") or b[c["case"]].get("ask_author")
              or "?" in a[c["case"]]["primary"] + b[c["case"]]["primary"]]

    L = ["# Error-analysis sample: coding report", "",
         f"{len(cases)} cases, one per model × diagram type × tier × failure class. "
         f"Two coders agree on the primary code in {len(agree)} of {len(cases)} cases. "
         f"{len(review)} cases go to the author (a disagreement, an `ask_author` flag or `M?`).",
         "", "## Cases for the author", "",
         "| Case | Model | Type | Tier | Class | Coder A | Coder B | Final |", "|---|---|---|---|---|---|---|---|"]
    for c in review:
        ca, cb = a[c["case"]], b[c["case"]]
        L.append(f"| {c['case']} | {c['model_id']} | {c['primary_type']} | {c['tier']} | "
                 f"{c['class']} | {ca['primary']}: {ca['reason']} | {cb['primary']}: {cb['reason']} | "
                 f"{final.get(c['case'], {}).get('primary', '')} |")

    def settled(c):
        """The author's code where given; else the agreed code of a case not sent to the author."""
        if c["case"] in final:
            return final[c["case"]]["primary"]
        return a[c["case"]]["primary"] if c not in review else None

    L += ["", "## Primary codes per model (settled cases)", "",
          "| Model | " + " | ".join(CODES) + " | open |", "|---|" + "---|" * (len(CODES) + 1)]
    for mid in dict.fromkeys(c["model_id"] for c in cases):
        mine = [c for c in cases if c["model_id"] == mid]
        cnt = collections.Counter(settled(c) for c in mine)
        L.append(f"| {mid} | " + " | ".join(str(cnt.get(code, 0)) for code in CODES)
                 + f" | {cnt.get(None, 0)} |")
    (out / "report.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(out / "report.md")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draw")
    d.add_argument("--data-root", type=Path, required=True)
    d.add_argument("--registry", type=Path, required=True)
    d.add_argument("--out", type=Path, required=True)
    d.set_defaults(func=cmd_draw)
    r = sub.add_parser("report")
    r.add_argument("--out", type=Path, required=True)
    r.set_defaults(func=cmd_report)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
