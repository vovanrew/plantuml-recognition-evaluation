"""Task-6 paper-ready synthesis: assemble the validated Task-1..5 artifacts into
the paper's exhibits. **Pure assembly over the emitted artifacts** -- it reads
``master_table.json`` (points + population_gap), ``ci_table.json`` (95% CIs),
``run_level.json`` (tokens + provenance) and ``crowding.json`` (per-tier image
crowding), and emits a consolidated results document as markdown plus a
Word-importable HTML rendering whose tables paste into Microsoft Word. It NEVER
re-pools a metric or computes a new one: every number is read straight from an
artifact a prior validated task produced.

Two-arms framing (plan invariant): the frontier models (GPT-5.2, Claude Opus 4.6,
Gemini 3.1 Pro) are fixed *reference points*; the Qwen open ladder (dense
2B/9B/27B) is a *scaling curve*; the 397B-A17B MoE is a capability *ceiling*
reported with BOTH total (397B) and active (~17B) parameters and kept off the
dense parameter axis. They are never merged into one ranked leaderboard.

Both reporting populations are carried side by side: ``zeros_for_failed`` (all
1000, non-compiled scored 0 -- the honest headline) and ``compiled_only`` (over
compiled cells, CSR reported separately). The ``population_gap`` (compiled - all)
is featured as the honest-vs-flattering exhibit.

Determinism: model order follows the artifact (registry) order, no timestamps, so
a re-run reproduces byte-identical files.
"""
from __future__ import annotations

import re

from analysis.aggregate import RELATIONS, TYPES
from analysis.plots import per_relation_stat_id, scaling_stat_id
from analysis.report import _chrf2, _pct1, _r3  # shared formatting (z / c notation)

POPS = ["zeros_for_failed", "compiled_only"]
TIERS = [1, 2, 3, 4]


# --------------------------------------------------------------------------- #
# arm grouping (the two-arms philosophy in code)
# --------------------------------------------------------------------------- #

def arm_groups(master: dict) -> dict[str, list[tuple[str, dict]]]:
    """Split the scored models into the three reported groups, preserving the
    artifact's (registry) order: ``frontier`` reference points, the Qwen dense
    ``ladder``, and the Qwen ``moe`` ceiling(s). A model is placed by its stored
    ``arm``/``family`` fields -- never re-derived."""
    groups: dict[str, list[tuple[str, dict]]] = {"frontier": [], "ladder": [], "moe": []}
    for mid, b in master.get("models", {}).items():
        if b.get("arm") == "frontier":
            groups["frontier"].append((mid, b))
        elif b.get("family") == "moe":
            groups["moe"].append((mid, b))
        else:
            groups["ladder"].append((mid, b))
    return groups


def param_label(block: dict) -> str:
    """Human parameter label: MoE shows total + active, a dense Qwen rung its size,
    a frontier model (undisclosed params) an em dash."""
    tot, act = block.get("params_total_b"), block.get("params_active_b")
    if tot is None:
        return "—"
    if block.get("family") == "moe":
        return f"{_bparam(tot)} total / {_bparam(act)} active"
    return _bparam(tot)


def _bparam(v) -> str:
    if v is None:
        return "—"
    return f"{int(v)}B" if float(v).is_integer() else f"{v:g}B"


# --------------------------------------------------------------------------- #
# CI read-through (never recomputed; read from ci_table.json)
# --------------------------------------------------------------------------- #

def ci_entry(ci: dict, mid: str, stat_id: str):
    """The ``{point, ci_low, ci_high, n_valid}`` record, or ``None`` if absent."""
    return ci.get("per_model", {}).get(mid, {}).get(stat_id)


def ci_md(entry, fmt, *, bracket: str = "[]") -> str:
    """``point [low, high]`` for markdown; ``point`` alone when the CI is missing
    (a point-only statistic), ``—`` when there is no point at all."""
    if entry is None:
        return "—"
    pt = entry.get("point")
    if pt is None:
        return "—"
    lo, hi = entry.get("ci_low"), entry.get("ci_high")
    if lo is None or hi is None:
        return fmt(pt)
    l, r = bracket[0], bracket[1]
    return f"{fmt(pt)} {l}{fmt(lo)}, {fmt(hi)}{r}"


def metric_ci_pair(ci: dict, mid: str, metric: str, level: str, fmt) -> str:
    """``z [..] / c [..]`` -- the metric's CI string in both populations."""
    z = ci_md(ci_entry(ci, mid, scaling_stat_id(metric, level, "zeros_for_failed")), fmt)
    c = ci_md(ci_entry(ci, mid, scaling_stat_id(metric, level, "compiled_only")), fmt)
    return f"{z} / {c}"


# --------------------------------------------------------------------------- #
# markdown assembly -- the consolidated results document
# --------------------------------------------------------------------------- #

def _headline_table(group: list[tuple[str, dict]], ci: dict, *, with_params: bool) -> list[str]:
    """One headline block: CSR + the four metrics (micro, with CI in both
    populations) + compiled-only type accuracy, one row per model in the group."""
    head = "| Model |" + (" Params |" if with_params else "") + \
        " CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) | Type acc |"
    sep = "|---|" + ("---|" if with_params else "") + "---|---|---|---|---|"
    lines = [head, sep]
    for mid, b in group:
        csr = ci_md(ci_entry(ci, mid, "csr|csr"), _pct1)
        el = metric_ci_pair(ci, mid, "element_f1", "micro", _r3)
        rel = metric_ci_pair(ci, mid, "relationship_f1", "micro", _r3)
        chrf = metric_ci_pair(ci, mid, "chrf", "macro", _chrf2)
        ta = ci_md(ci_entry(ci, mid, scaling_stat_id("type_accuracy")), _r3)
        cells = [b["display"]]
        if with_params:
            cells.append(param_label(b))
        cells += [csr, el, rel, chrf, ta]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def exhibit_headline(master: dict, ci: dict) -> list[str]:
    g = arm_groups(master)
    out = ["## Exhibit 1 — Headline results (two arms)", "",
           "Cells are `point [2.5th, 97.5th]` paired-bootstrap 95% CIs (n="
           f"{ci['meta']['n_resamples']}, seed={ci['meta']['seed']}); CSR as a "
           "percentage, F1 / type accuracy on 0–1, chrF++ on its native 0–100 "
           "scale. Two populations per metric as `zeros_for_failed / compiled_only`. "
           "chrF++ is the **macro** statistic (the CI-bearing one; chrF++ micro is a "
           "corpus statistic, point-only — see Exhibit 2). Type accuracy is "
           "compiled-only by definition. **This is two arms, not one leaderboard.**",
           ""]
    out += ["### Arm A — Frontier reference points", "",
            "One reigning flagship per lab (fixed comparison points).", ""]
    out += _headline_table(g["frontier"], ci, with_params=False)
    out += ["",
            "### Arm B — Qwen open ladder (dense) + MoE ceiling", "",
            "The dense 2B/9B/27B ladder is a scaling curve; the 397B-A17B MoE is a "
            "capability ceiling (both total and active parameters reported), **not** a "
            "fourth dense rung.", ""]
    out += _headline_table(g["ladder"] + g["moe"], ci, with_params=True)
    out += [""]
    return out


def exhibit_populations(master: dict, ci: dict) -> list[str]:
    """Overall micro AND macro, both populations side by side, every model in one
    table per level (so the honest vs flattering columns sit together)."""
    out = ["## Exhibit 2 — Overall results, both populations × micro & macro", "",
           "Read straight from the master table; CIs (where they exist) from the CI "
           "table. chrF++ micro is a corpus sacrebleu statistic (point estimate, no "
           "CI); chrF++ macro carries a CI.", ""]
    for level in ("micro", "macro"):
        out += [f"### {level.capitalize()}", "",
                "| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | "
                "chrF++ (z / c) |", "|---|---|---|---|---|"]
        for mid, b in master["models"].items():
            csr = ci_md(ci_entry(ci, mid, "csr|csr"), _pct1) if level == "micro" \
                else _pct1(b["overall"]["csr"]["csr"])
            el = metric_ci_pair(ci, mid, "element_f1", level, _r3)
            rel = metric_ci_pair(ci, mid, "relationship_f1", level, _r3)
            if level == "macro":
                chrf = metric_ci_pair(ci, mid, "chrf", "macro", _chrf2)
            else:  # chrf micro is point-only -> read the master values directly
                ov = b["overall"]["chrf"]
                chrf = (f"{_chrf2(ov['zeros_for_failed']['micro'])} / "
                        f"{_chrf2(ov['compiled_only']['micro'])}")
            out.append(f"| {b['display']} | {csr} | {el} | {rel} | {chrf} |")
        out.append("")
    return out


def exhibit_population_gap(master: dict) -> list[str]:
    """The compiled-only − all-1000 gap (overall micro): the selective-failure
    fingerprint. Largest for weak models, ~0 for the frontier."""
    out = ["## Exhibit 3 — Population gap (selective-failure bias)", "",
           "`compiled_only − zeros_for_failed` (overall micro). A low-CSR model that "
           "drops/times out on its hardest diagrams is graded on an easier subset, so "
           "its compiled-only score runs far above its honest all-1000 score; the gap "
           "is that fingerprint and tracks CSR (near-zero for the frontier, large for "
           "the weak rungs).", "",
           "| Model | CSR | ΔElement F1 | ΔRelationship F1 | ΔchrF++ |",
           "|---|---|---|---|---|"]
    for mid, b in master["models"].items():
        pg = b["overall"]["population_gap"]
        out.append("| {m} | {csr} | {el:+.3f} | {rel:+.3f} | {chrf:+.2f} |".format(
            m=b["display"], csr=_pct1(b["overall"]["csr"]["csr"]),
            el=pg["element_f1"]["micro"]["gap"],
            rel=pg["relationship_f1"]["micro"]["gap"],
            chrf=pg["chrf"]["micro"]["gap"]))
    out.append("")
    return out


def exhibit_per_relation(master: dict, ci: dict) -> list[str]:
    """Relationship F1 per relation type (6 relations) with CIs, both populations.
    Point estimates from the master read-through; CIs from the bootstrap."""
    out = ["## Exhibit 4 — Relationship F1 by relation type (with CIs)", "",
           "Per-relation F1 (micro), `zeros_for_failed [CI] / compiled_only [CI]`. "
           "GT support (model-independent) annotates each relation.", ""]
    # model-independent GT support per relation (read from any model's read-through)
    support = {}
    for rel in RELATIONS:
        for b in master["models"].values():
            rec = b["per_relation"]["zeros_for_failed"].get(rel)
            if rec and rec.get("support_gt") is not None:
                support[rel] = rec["support_gt"]
                break
    header = "| Model | " + " | ".join(
        f"{rel}<br>(n={support.get(rel, '—')})" for rel in RELATIONS) + " |"
    out += [header, "|---|" + "---|" * len(RELATIONS)]
    for mid, b in master["models"].items():
        cells = [b["display"]]
        for rel in RELATIONS:
            z = ci_md(ci_entry(ci, mid, per_relation_stat_id(rel, "zeros_for_failed")), _r3)
            c = ci_md(ci_entry(ci, mid, per_relation_stat_id(rel, "compiled_only")), _r3)
            cells.append(f"{z} / {c}")
        out.append("| " + " | ".join(cells) + " |")
    out.append("")
    return out


def _breakdown_block(master: dict, scope_keys, get_cell, label_fmt, title: str,
                     note: str) -> list[str]:
    """A per-scope point-estimate table (micro), one row per model per scope value
    -- no CIs (the bootstrap covers overall + per-relation only)."""
    out = [f"## {title}", "", note, ""]
    for sv in scope_keys:
        out += [f"### {label_fmt(sv)} (micro, point estimates)", "",
                "| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | "
                "chrF++ macro (z / c) |", "|---|---|---|---|---|"]
        for mid, b in master["models"].items():
            cell = get_cell(b, sv)
            if cell is None:
                continue
            el = _pair_micro(cell["element_f1"], "micro", _r3)
            rel = _pair_micro(cell["relationship_f1"], "micro", _r3)
            chrf = _pair_chrf(cell["chrf"], "macro")
            out.append(f"| {b['display']} | {_pct1(cell['csr']['csr'])} | {el} | "
                       f"{rel} | {chrf} |")
        out.append("")
    return out


def _pair_micro(metric_block: dict, level: str, fmt) -> str:
    z = metric_block["zeros_for_failed"][level]["f1"]
    c = metric_block["compiled_only"][level]["f1"]
    return f"{fmt(z)} / {fmt(c)}"


def _pair_chrf(chrf_block: dict, level: str) -> str:
    return f"{_chrf2(chrf_block['zeros_for_failed'][level])} / " \
           f"{_chrf2(chrf_block['compiled_only'][level])}"


def exhibit_by_type(master: dict) -> list[str]:
    return _breakdown_block(
        master, TYPES, lambda b, t: b["by_type"].get(t), lambda t: f"Type: {t}",
        "Exhibit 5 — Per-type breakdown (class / sequence)",
        "Point estimates (per-type cells are not bootstrapped). chrF++ is macro "
        "(poolable at sub-scopes).")


def exhibit_by_tier(master: dict, crowding: dict | None) -> list[str]:
    out = _breakdown_block(
        master, [str(t) for t in TIERS], lambda b, t: b["by_tier"].get(t),
        lambda t: f"Tier {t}",
        "Exhibit 6 — Per-tier breakdown (complexity quartiles)",
        "Point estimates (per-tier cells are not bootstrapped). chrF++ is macro.")
    if crowding:
        out += ["### Per-tier image crowding (degradation context)", "",
                "Content_lines per megapixel after the 1568px resize (pooled), the "
                "legibility descriptor accompanying the degradation curve — it rises "
                "monotonically with tier (harder diagrams are denser).", "",
                "| Tier | content_lines / MP |", "|---|---|"]
        for t in TIERS:
            v = crowding.get(str(t))
            out.append(f"| {t} | {v:.2f} |" if v is not None else f"| {t} | — |")
        out.append("")
    return out


def exhibit_run_level(run_level: dict) -> list[str]:
    """Token footprint + reproducibility provenance, straight from run_level.json."""
    out = ["## Exhibit 7 — Run-level: token footprint & provenance", "",
           run_level["meta"].get("token_note", ""), "",
           "### Token totals (all 1000 cells incl. failures)", "",
           "| Model | input (M) | output (M) | reasoning (M) | total (M) |",
           "|---|---|---|---|---|"]
    for m in run_level["models"]:
        t = m["tokens"]
        out.append("| {d} | {i:.3f} | {o:.3f} | {r:.3f} | {tot:.3f} |".format(
            d=m["display"], i=t["input"] / 1e6, o=t["output"] / 1e6,
            r=t["reasoning"] / 1e6, tot=t["total"] / 1e6))
    out += ["", "### Reproducibility provenance", "",
            "| Model | snapshot | provider | non-thinking config | max_tokens | "
            "leak |", "|---|---|---|---|---|---|"]
    for m in run_level["models"]:
        p = m["provenance"]
        eb = "; ".join(f"{k}={v}" for k, v in (p.get("extra_body") or {}).items()) or "—"
        out.append("| {d} | `{snap}` | {prov} | {eb} | {mt} | {leak} |".format(
            d=m["display"], snap=p["model"], prov=p["provider"], eb=eb,
            mt=p["max_tokens"], leak=p["reasoning_leak"]))
    out.append("")
    return out


def _best(master: dict, group: list[tuple[str, dict]], metric: str, level: str,
          population: str):
    """The (display, value) with the highest overall metric in a group (read-only)."""
    best = None
    for _mid, b in group:
        if metric == "csr":
            v = b["overall"]["csr"]["csr"]
        else:
            v = b["overall"][metric][population][level]["f1"]
        if best is None or v > best[1]:
            best = (b["display"], v)
    return best


def exhibit_narrative_skeleton(master: dict, ci: dict, run_level: dict | None,
                               crowding: dict | None) -> list[str]:
    """A results-section SKELETON (headed bullets with the key numbers filled),
    NOT prose -- the author writes the paper prose (the qualitative error write-up is in `analysis/error_analysis.md`)."""
    g = arm_groups(master)
    out = ["## Results-narrative skeleton (author expands into prose)", "",
           "_Headed bullets with the artifact numbers pre-filled; this is scaffolding, "
           "not paper prose. The qualitative error write-up is in `analysis/error_analysis.md` "
           "(40 cases from `failure_index`)._", ""]

    fb = _best(master, g["frontier"], "csr", "micro", "zeros_for_failed")
    out += ["**R1 — Frontier reference points.** Compilation is near-saturated across "
            f"the three flagships; {fb[0]} leads on CSR ({_pct1(fb[1])}). They anchor "
            "the upper bound; report them as fixed points, not as a ranked contest "
            "(Exhibit 1A, Fig. frontier_bars).", ""]

    ladder = g["ladder"]
    if ladder:
        lo, hi = ladder[0][1], ladder[-1][1]
        out += ["**R2 — Open-ladder scaling (dense).** CSR rises monotonically with "
                f"dense scale: {lo['display']} {_pct1(lo['overall']['csr']['csr'])} → "
                f"{hi['display']} {_pct1(hi['overall']['csr']['csr'])}; Element/Relationship "
                "F1 track it (Exhibit 1B, Fig. scaling_curve). The compiled-only overlay "
                "stays high throughout — the gain is in *compiling at all*, not in the "
                "quality of what compiles.", ""]
    if g["moe"]:
        moe = g["moe"][0][1]
        out += ["**R3 — MoE capability ceiling.** The 397B-A17B mixture "
                f"({param_label(moe)}) reaches CSR {_pct1(moe['overall']['csr']['csr'])}, "
                "above the dense ladder and approaching the frontier band, at ~17B active "
                "parameters — a capability ceiling for the open arm, plotted off the dense "
                "axis as a separate marker (Fig. scaling_curve).", ""]

    # population gap extremes
    gaps = [(b["display"], b["overall"]["population_gap"]["element_f1"]["micro"]["gap"],
             b["overall"]["csr"]["csr"]) for b in master["models"].values()]
    gmax = max(gaps, key=lambda x: x[1])
    gmin = min(gaps, key=lambda x: x[1])
    out += ["**R4 — Selective-failure bias (population gap).** The compiled-only − "
            f"all-1000 Element-F1 gap is largest for the weakest rung ({gmax[0]}, "
            f"{gmax[1]:+.3f} at CSR {_pct1(gmax[2])}) and negligible at the frontier "
            f"({gmin[0]}, {gmin[1]:+.3f}). Report the honest all-1000 column as the "
            "headline (Exhibit 3).", ""]

    out += ["**R5 — Structural failure modes (per-relation).** Per-relation F1 separates "
            "easy from hard edges; read the per-relation table for which relations each "
            "arm misses, with CIs (Exhibit 4, Fig. per_relation_f1). The qualitative "
            "error categories draw on `failure_index`.", ""]

    deg = ""
    if crowding:
        deg = (f" Image crowding rises in lockstep (content_lines/MP: T1 "
               f"{crowding.get('1', 0):.1f} → T4 {crowding.get('4', 0):.1f}), the "
               "legibility context for the drop.")
    out += ["**R6 — Complexity degradation (per-tier).** Every metric declines from tier "
            "1 to tier 4 across the panel; the weak rungs fall fastest (Exhibit 6, Fig. "
            f"breakdown_by_tier).{deg}", ""]

    if run_level:
        out += ["**R7 — Token footprint.** Per-model input/output token totals over all "
                "1000 cells back the deployment/fine-tuning cost argument (Exhibit 7); "
                "the open arm ran under flat-rate billing, so dollar figures are omitted "
                "by design (token volumes stand).", ""]
    return out


def render_exhibits_md(master: dict, ci: dict, run_level: dict | None,
                       crowding: dict | None, failure: dict | None) -> str:
    meta = master["meta"]
    out = ["# Paper exhibits — zero-shot image→PlantUML benchmark", "",
           f"**Models included: {meta['models_included']}/{meta['models_total']}** "
           f"(panel: {meta['label']}).", ""]
    if meta.get("pending_ids"):
        out += ["Pending: " + ", ".join(meta["pending_ids"]), ""]
    out += ["Assembled read-only from the validated Task-1..5 artifacts "
            "(`master_table.json`, `ci_table.json`, `run_level.json`, `crowding.json`"
            + (", `failure_index.json`" if failure else "") +
            "). No metric is re-pooled or recomputed here. Companion figures live in "
            "`analysis/out/plots/`; a Word-importable rendering of this document (tables "
            "paste straight into Microsoft Word) is emitted alongside it as "
            "`exhibits.html`.", ""]
    out += exhibit_headline(master, ci)
    out += exhibit_populations(master, ci)
    out += exhibit_population_gap(master)
    out += exhibit_per_relation(master, ci)
    out += exhibit_by_type(master)
    out += exhibit_by_tier(master, crowding)
    if run_level:
        out += exhibit_run_level(run_level)
    if failure:
        out += _failure_coverage(failure)
    out += exhibit_narrative_skeleton(master, ci, run_level, crowding)
    return "\n".join(out) + "\n"


def _failure_coverage(failure: dict) -> list[str]:
    """A pointer table: the failure-case index feeds the author's qualitative review;
    here we only surface its coverage (available → sampled per model × outcome)."""
    m = failure["meta"]
    out = ["## Exhibit 8 — Failure-case coverage (feeds the qualitative review)", "",
           f"The stratified failure index holds **{m['total_cases']}** cases "
           f"(`--per-cell {m['per_cell']}`, seed {m['seed']}) across outcome classes "
           f"{', '.join(m['outcome_classes_sampled'])}. Full records — GT, prediction, "
           "CSR error, structural deltas — are in `failure_index.{md,json,csv}`; the "
           "40-case write-up is in `analysis/error_analysis.md`. Coverage (available → sampled):", "",
           "| Model | " + " | ".join(m["outcome_classes_sampled"]) + " |",
           "|---|" + "---|" * len(m["outcome_classes_sampled"])]
    for mid in m["included_ids"]:
        cs = m["cell_summary"].get(mid, {})
        cells = [mid]
        for oc in m["outcome_classes_sampled"]:
            rec = cs.get(oc)
            cells.append(f"{rec['available']}→{rec['sampled']}" if rec else "—")
        out.append("| " + " | ".join(cells) + " |")
    out.append("")
    return out


# --------------------------------------------------------------------------- #
# HTML rendering -- Word-importable (open in Word, or copy a table in)
# --------------------------------------------------------------------------- #
# Microsoft Word reads HTML <table> markup natively: opening the emitted
# exhibits.html in Word, or copy-pasting a table from a browser, yields a real,
# editable Word table with the header styling preserved. This is the Word analog
# of an \input-able LaTeX table. The renderer handles only the markdown THIS
# module emits (#/##/### headings, pipe tables, **bold**, _italic_, `code`); it is
# not a general markdown parser.

_HTML_STYLE = (
    "body{font-family:Calibri,Arial,sans-serif;font-size:11pt;line-height:1.4;}"
    "table{border-collapse:collapse;margin:8px 0;}"
    "th,td{border:1px solid #999;padding:3px 8px;text-align:left;vertical-align:top;}"
    "th{background:#eee;}"
    "code{font-family:Consolas,monospace;}"
)


def _html_inline(text: str) -> str:
    """Escape one line and apply inline markdown (**bold**, `code`, _italic_),
    preserving an intentional literal ``<br>`` (used in table headers)."""
    text = text.replace("<br>", "\x00BR\x00")
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = text.replace("\x00BR\x00", "<br/>")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    # underscores only count as italic at word boundaries, so identifiers like
    # zeros_for_failed (always inside backticks anyway) are never touched.
    text = re.sub(r"(?<![\w*])_(.+?)_(?![\w*])", r"<em>\1</em>", text)
    return text


def _split_row(row: str) -> list[str]:
    """``| a | b |`` -> ``["a", "b"]``."""
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _is_separator(row: str) -> bool:
    cells = _split_row(row)
    return bool(cells) and all(set(c) <= set("-: ") and "-" in c for c in cells)


def _html_table(block: list[str]) -> str:
    """A markdown pipe-table block (header, separator, rows) -> an HTML table."""
    if not block:
        return ""
    header = _split_row(block[0])
    body = block[1:]
    if body and _is_separator(body[0]):
        body = body[1:]
    out = ["<table>",
           "<thead><tr>" + "".join(f"<th>{_html_inline(c)}</th>" for c in header)
           + "</tr></thead>", "<tbody>"]
    for r in body:
        cells = _split_row(r)
        out.append("<tr>" + "".join(f"<td>{_html_inline(c)}</td>" for c in cells)
                   + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def md_to_html(md_text: str, *, title: str = "Paper exhibits") -> str:
    """Render the generated exhibits markdown as a standalone HTML document whose
    tables paste cleanly into Microsoft Word. Deterministic (no timestamps)."""
    lines = md_text.split("\n")
    out = ["<!DOCTYPE html>", "<html><head><meta charset=\"utf-8\">",
           f"<title>{_html_inline(title)}</title>",
           f"<style>{_HTML_STYLE}</style></head><body>"]
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("### "):
            out.append(f"<h3>{_html_inline(line[4:])}</h3>"); i += 1; continue
        if line.startswith("## "):
            out.append(f"<h2>{_html_inline(line[3:])}</h2>"); i += 1; continue
        if line.startswith("# "):
            out.append(f"<h1>{_html_inline(line[2:])}</h1>"); i += 1; continue
        if line.startswith("|"):
            block = []
            while i < n and lines[i].startswith("|"):
                block.append(lines[i]); i += 1
            out.append(_html_table(block)); continue
        if line.strip() == "":
            i += 1; continue
        out.append(f"<p>{_html_inline(line)}</p>"); i += 1
    out.append("</body></html>")
    return "\n".join(out) + "\n"
