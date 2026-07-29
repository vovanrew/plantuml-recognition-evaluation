"""Task-5 run-level aggregator: read source B (``data/runs/<run>/``) -- the raw
per-cell API responses + ``run_meta.json`` -- and emit, per reported model, the
run-level tables the metric JSONs (source A) do not carry:

(a) token totals -- input / output / reasoning(-or-thoughts) summed over ALL 1000
    cells incl. failures (the basis for the run's cost/deployment argument; dollar
    pricing is intentionally out of scope -- token volumes only);
(b) Gemini per-call ``thoughtsTokenCount`` (methodology-mandated; surfaced as the
    reasoning column for the native ``generateContent`` shape);
(c) a failure/outcome inventory separating PROVIDER/harness failure (timeout /
    image_dropped / http_error / network_error, from source B) from MODEL failure
    (compile-fail, derived from the CSR summary in source A);
(d) a provenance manifest from each ``run_meta.json`` (+ the re-derived
    reasoning_leak count) for the reproducibility table;
(e) a per-tier crowding descriptor -- ``content_lines`` per megapixel after the
    1568px resize, MP read from the real PNG IHDR dims -- model-independent, emitted
    once and consumed by the Task-3 plots.

Everything is read-only over ``data/`` and the Task-1..4 outputs; stdlib only.

Token-field convention (mirrors ``util/project_run_cost.usage_totals``):
- ``input``  = prompt tokens.
- ``output`` = tokens billed at the output rate -- OpenAI/Claude/Qwen
  ``completion_tokens`` AS-IS (it already includes any reasoning, so reasoning is
  NEVER added on top -- that would double-count); Gemini ``candidatesTokenCount +
  thoughtsTokenCount`` (thoughts are a separate component of Gemini output).
- ``reasoning`` = the reasoning/thinking subtotal, surfaced for transparency and for
  the Gemini-thoughts requirement -- OpenAI
  ``completion_tokens_details.reasoning_tokens`` (a subset of ``output``); Gemini
  ``thoughtsTokenCount`` (already inside ``output``). Absent ⇒ 0.

Polymorphic per-key record (inspect the shape, never assume): a SUCCESS carries
top-level ``usage`` (OpenAI-like) or ``usageMetadata`` (Gemini). A FAILURE is a
harness error record ``{error, key, attempts, detail?}`` with no usage -- EXCEPT
``image_dropped``, which keeps the provider response (with usage) under
``response``; those billed tokens are counted while the cell still counts as a
provider failure. A non-error record lacking usage is a schema surprise -> raise.
"""
from __future__ import annotations

import csv
import json
import logging
import struct
from pathlib import Path

log = logging.getLogger(__name__)

_PNG_SIGNATURE = bytes.fromhex("89504e470d0a1a0a")

# harness error categories (evaluation/infer_runner.py)
ERROR_CATEGORIES = ("timeout", "image_dropped", "http_error", "network_error")
# image_dropped is a provider failure whose stored record may still carry usage
PROVIDER_FAILURE_CATEGORIES = ERROR_CATEGORIES


# --------------------------------------------------------------------------- #
# PNG dimensions (stdlib struct, no Pillow) -- crowding descriptor input
# --------------------------------------------------------------------------- #

def read_png_dims(path) -> tuple[int, int]:
    """``(width, height)`` from a PNG's IHDR chunk: the 8-byte signature is followed
    by the IHDR length+type, then width,height as two big-endian uint32 at bytes
    16:24. Raises on a non-PNG / truncated header (STOP-and-report)."""
    with open(path, "rb") as f:
        header = f.read(24)
    if len(header) < 24 or header[:8] != _PNG_SIGNATURE:
        raise ValueError(f"{path}: not a PNG (bad signature or truncated header)")
    width, height = struct.unpack(">II", header[16:24])
    return width, height


# --------------------------------------------------------------------------- #
# token extraction from one raw per-cell record
# --------------------------------------------------------------------------- #

def _usage_tokens(obj: dict) -> dict:
    """Pull (input, output, reasoning) from a response object carrying either a
    Gemini ``usageMetadata`` or an OpenAI-like ``usage``."""
    if "usageMetadata" in obj:                     # Gemini native generateContent
        u = obj["usageMetadata"]
        thoughts = u.get("thoughtsTokenCount", 0)  # absent ⇒ 0
        return {"input": u.get("promptTokenCount", 0),
                "output": u.get("candidatesTokenCount", 0) + thoughts,
                "reasoning": thoughts}
    u = obj["usage"]                               # OpenAI / Claude / Qwen
    details = u.get("completion_tokens_details") or {}
    return {"input": u.get("prompt_tokens", 0),
            "output": u.get("completion_tokens", 0),          # already includes reasoning
            "reasoning": details.get("reasoning_tokens", 0)}  # subset of output (GPT only)


def read_cell(record: dict) -> dict:
    """Classify + extract one raw per-cell record.

    Returns ``{status, input, output, reasoning}`` where ``status`` is ``"ok"`` for a
    success or the harness error category for a failure. A pure error record yields 0
    tokens; an ``image_dropped`` record counts the usage of its retained ``response``.
    A non-error record without ``usage``/``usageMetadata`` is unrecognized -> raise.
    """
    if "error" in record:
        resp = record.get("response")
        if isinstance(resp, dict) and ("usage" in resp or "usageMetadata" in resp):
            toks = _usage_tokens(resp)
        else:
            toks = {"input": 0, "output": 0, "reasoning": 0}
        return {"status": record["error"], **toks}
    if "usage" in record or "usageMetadata" in record:
        return {"status": "ok", **_usage_tokens(record)}
    raise ValueError(f"unrecognized cell record shape: keys={sorted(record.keys())}")


# --------------------------------------------------------------------------- #
# per-run source-B aggregation (tokens + status counts over all cells)
# --------------------------------------------------------------------------- #

def read_run_usage(run_dir) -> dict:
    """Sum tokens + count statuses over every ``<key>.json`` cell in a source-B run
    dir (``run_meta.json`` excluded). Failures contribute 0 tokens unless they kept a
    usage-bearing response (image_dropped). Deterministic (sorted file iteration).

    Returns ``{n_cells, n_ok, n_error, input, output, reasoning, status_counts}``.
    """
    run_dir = Path(run_dir)
    totals = {"input": 0, "output": 0, "reasoning": 0}
    status_counts: dict[str, int] = {}
    n_cells = 0
    for path in sorted(run_dir.glob("*.json")):
        if path.name == "run_meta.json":
            continue
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
        cell = read_cell(record)
        n_cells += 1
        for k in totals:
            totals[k] += cell[k]
        status_counts[cell["status"]] = status_counts.get(cell["status"], 0) + 1
    n_ok = status_counts.get("ok", 0)
    n_error = n_cells - n_ok
    return {"n_cells": n_cells, "n_ok": n_ok, "n_error": n_error,
            "status_counts": status_counts, **totals}


def token_record(run_usage: dict) -> dict:
    """The per-model token table row: totals over all cells (no dollar pricing)."""
    return {
        "n_cells": run_usage["n_cells"],
        "n_ok": run_usage["n_ok"],
        "input": run_usage["input"],
        "output": run_usage["output"],
        "reasoning": run_usage["reasoning"],
        "total": run_usage["input"] + run_usage["output"],
    }


# --------------------------------------------------------------------------- #
# run_meta provenance manifest
# --------------------------------------------------------------------------- #

def read_run_meta(run_dir) -> dict:
    """Load a run's ``run_meta.json`` (raises if absent -- STOP-and-report)."""
    path = Path(run_dir) / "run_meta.json"
    if not path.exists():
        raise FileNotFoundError(f"run_meta.json missing: {path}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


_PROVENANCE_FIELDS = ("model", "base_url", "provider", "token_field", "max_tokens",
                      "timeout", "temperature", "extra_body", "started")


def provenance_record(run_meta: dict, leak_count: int) -> dict:
    """The reproducibility row: the reasoning-relevant ``run_meta`` fields verbatim
    plus the re-derived ``reasoning_leak`` count (the run-meta tally is not
    persisted)."""
    missing = [k for k in _PROVENANCE_FIELDS if k not in run_meta]
    if missing:
        raise KeyError(f"run_meta missing field(s) {missing}")
    rec = {k: run_meta[k] for k in _PROVENANCE_FIELDS}
    rec["reasoning_leak"] = leak_count
    return rec


# --------------------------------------------------------------------------- #
# reconcile (inclusion gate) + failure/outcome inventory
# --------------------------------------------------------------------------- #

def source_a_no_response(md) -> int:
    """Source-A no-prediction count: per-diagram element rows with ``has_pred`` False."""
    return sum(1 for r in md.rows if not r["element"]["has_pred"])


def reconcile(md, run_usage: dict) -> dict:
    """Cross-check that source B (raw responses) and source A (scored metrics)
    describe the same run: the source-B no-response count (error records) must equal
    source A's ``has_pred==false`` count. A mismatch means the run dir was resumed
    after scoring (source B ahead) -> the model is excluded until re-scored."""
    b = run_usage["n_error"]
    a = source_a_no_response(md)
    return {"source_b_no_response": b, "source_a_has_pred_false": a, "ok": a == b}


def failure_inventory(md, run_usage: dict) -> dict:
    """Separate PROVIDER/harness failure (source B error categories) from MODEL
    failure (compile-fail, from the CSR summary). compile_fail = non-compiled minus
    no-response; the three classes partition the n cells."""
    csr = md.summaries["csr"]
    n, compiled = csr["n"], csr["compiled"]
    no_response = run_usage["n_error"]
    compile_fail = (n - compiled) - no_response
    counts = run_usage.get("status_counts", {})
    provider = {cat: counts.get(cat, 0) for cat in PROVIDER_FAILURE_CATEGORIES}
    return {
        "n": n,
        "compiled": compiled,
        "compile_fail": compile_fail,
        "no_response": no_response,
        "provider_failures": provider,
        "partition_ok": compiled + compile_fail + no_response == n,
        "reconcile": reconcile(md, run_usage),
    }


# --------------------------------------------------------------------------- #
# per-tier crowding descriptor (model-independent; consumed by Task-3 plots)
# --------------------------------------------------------------------------- #

def _pooled_cell(items: list[dict]) -> dict:
    """Pool a group of ``{content_lines, mp}`` diagrams into a crowding cell.
    ``lines_per_mp`` is the pooled ratio total_lines / total_mp (the tier's text
    density per megapixel); ``mean_lines_per_mp`` weights each diagram equally."""
    n = len(items)
    total_lines = sum(it["content_lines"] for it in items)
    total_mp = sum(it["mp"] for it in items)
    per = [it["content_lines"] / it["mp"] for it in items if it["mp"] > 0]
    return {
        "n": n,
        "content_lines": total_lines,
        "mp": total_mp,
        "lines_per_mp": total_lines / total_mp if total_mp else None,
        "mean_mp": total_mp / n if n else None,
        "mean_lines_per_mp": sum(per) / len(per) if per else None,
    }


def crowding_descriptor(diagrams: list[dict], dims_by_key: dict[str, tuple]) -> dict:
    """Per-tier (and per-type x tier) crowding = ``content_lines`` per megapixel after
    the 1568px resize. ``diagrams`` are test_set items (``.puml`` keys); ``dims_by_key``
    maps the STRIPPED key to its real ``(width, height)`` PNG dims. A diagram with no
    dims is a schema surprise -> raise (STOP-and-report)."""
    from analysis.aggregate import TIERS, TYPES
    from analysis.loader import strip_puml

    items = []
    for d in diagrams:
        sk = strip_puml(d["key"])
        if sk not in dims_by_key:
            raise KeyError(f"no PNG dims for test-set key {d['key']!r} (stripped {sk!r})")
        w, h = dims_by_key[sk]
        items.append({"primary_type": d["primary_type"], "tier": d["tier"],
                      "content_lines": d["content_lines"], "mp": w * h / 1e6})

    by_tier = {}
    for tier in TIERS:
        group = [it for it in items if it["tier"] == tier]
        if group:
            by_tier[tier] = _pooled_cell(group)

    by_type_tier = {}
    for typ in TYPES:
        per_tier = {}
        for tier in TIERS:
            group = [it for it in items if it["primary_type"] == typ and it["tier"] == tier]
            if group:
                per_tier[tier] = _pooled_cell(group)
        if per_tier:
            by_type_tier[typ] = per_tier

    by_type = {}
    for typ in TYPES:
        group = [it for it in items if it["primary_type"] == typ]
        if group:
            by_type[typ] = _pooled_cell(group)

    # Task-3 consumable: {str(tier): lines_per_mp} (string keys, plots index by str)
    lines_per_mp_by_tier = {str(tier): cell["lines_per_mp"] for tier, cell in by_tier.items()}

    return {
        "n": len(items),
        "metric": "content_lines per megapixel after 1568px resize (pooled total/total)",
        "by_tier": by_tier,
        "by_type_tier": by_type_tier,
        "by_type": by_type,
        "lines_per_mp_by_tier": lines_per_mp_by_tier,
    }


def load_crowding(test_set_path, images_dir) -> dict:
    """Build the crowding descriptor from disk: test_set diagrams + the real
    ``data/puml_images_1568/<stripped_key>.png`` IHDR dims. Model-independent."""
    from analysis.loader import strip_puml

    test_set_path, images_dir = Path(test_set_path), Path(images_dir)
    with open(test_set_path, encoding="utf-8") as f:
        diagrams = json.load(f)["diagrams"]
    dims_by_key = {}
    for d in diagrams:
        sk = strip_puml(d["key"])
        png = images_dir / f"{sk}.png"
        if not png.exists():
            raise FileNotFoundError(f"missing standardized image for {d['key']!r}: {png}")
        dims_by_key[sk] = read_png_dims(png)
    return crowding_descriptor(diagrams, dims_by_key)


# --------------------------------------------------------------------------- #
# per-model record + disk-driven build (reconcile is the inclusion gate)
# --------------------------------------------------------------------------- #

def model_run_record(md, run_usage: dict, run_meta: dict, leak_count: int) -> dict:
    """Assemble one included model's run-level record from already-read inputs."""
    e = md.entry
    return {
        "model_id": e.id,
        "display": e.display,
        "arm": e.arm,
        "lab": e.lab,
        "family": e.family,
        "params_total_b": e.params_total_b,
        "params_active_b": e.params_active_b,
        "run_dir": e.run_dir,
        "tokens": token_record(run_usage),
        "failures": failure_inventory(md, run_usage),
        "provenance": provenance_record(run_meta, leak_count),
    }


def build_run_level(
    models,
    *,
    models_total: int,
    pending_ids: list[str],
    refused_ids: list[str] | None,
    data_root,
    label: str = "main",
) -> tuple[list[dict], dict]:
    """Read source B for each (eligible, leak-clean) model, apply the reconcile
    inclusion gate, and assemble (records, meta).

    A model whose source-B no-response count does not equal source A's
    ``has_pred==false`` (the run dir was resumed after scoring) is DESYNCED -> dropped
    with a logged note and listed in ``meta.desynced``. The gate is self-correcting:
    once the run is re-scored the counts agree and the model is included on the next
    run. ``records`` preserve the input (registry) order of included models.
    """
    from analysis.leak_gate import count_reasoning_leaks, predictions_dir

    data_root = Path(data_root)
    records: list[dict] = []
    desynced: list[dict] = []

    for md in models:
        run_path = predictions_dir(data_root, md.entry.run_dir)
        run_usage = read_run_usage(run_path)
        rec = reconcile(md, run_usage)
        if not rec["ok"]:
            log.warning(
                "DESYNCED %s: source-B no-response=%d != source-A has_pred==false=%d "
                "(run dir resumed after scoring) -- excluded until re-scored",
                md.entry.id, rec["source_b_no_response"], rec["source_a_has_pred_false"])
            desynced.append({"model_id": md.entry.id, "display": md.entry.display, **rec})
            continue
        run_meta = read_run_meta(run_path)
        leaks = count_reasoning_leaks(run_path)
        records.append(model_run_record(md, run_usage, run_meta, leaks))

    desynced_ids = [d["model_id"] for d in desynced]
    meta = {
        "label": label,
        "models_included": len(records),
        "models_total": models_total,
        "included_ids": [r["model_id"] for r in records],
        "pending_ids": list(pending_ids),
        "refused_ids": list(refused_ids or []),
        "desynced_ids": desynced_ids,
        "desynced": desynced,
        "provider_failure_categories": list(PROVIDER_FAILURE_CATEGORIES),
        "token_note": ("token totals over all cells incl. failures; output already "
                       "includes reasoning (no double count); Gemini output = "
                       "candidates + thoughts. Dollar pricing out of scope."),
    }
    log.info("[%s] run-level: %d/%d included (pending: %s; desynced: %s; refused: %s)",
             label, len(records), models_total, ", ".join(pending_ids) or "none",
             ", ".join(desynced_ids) or "none", ", ".join(refused_ids or []) or "none")
    return records, meta


# --------------------------------------------------------------------------- #
# emitters: markdown (human) + CSV (flat) + JSON (machine); crowding artifact
# --------------------------------------------------------------------------- #

CSV_FIELDS = [
    "model_id", "display", "arm", "family", "run_dir",
    "n_cells", "input_tokens", "output_tokens", "reasoning_tokens", "total_tokens",
    "compiled", "compile_fail", "no_response",
    "timeout", "image_dropped", "http_error", "network_error",
    "provider", "max_tokens", "temperature", "reasoning_leak",
    "source_a_has_pred_false", "source_b_no_response", "reconcile_ok",
]


def run_level_csv_rows(records: list[dict]) -> list[dict]:
    rows = []
    for r in records:
        tok, fail, prov = r["tokens"], r["failures"], r["provenance"]
        pf = fail["provider_failures"]
        rows.append({
            "model_id": r["model_id"], "display": r["display"], "arm": r["arm"],
            "family": r["family"], "run_dir": r["run_dir"],
            "n_cells": tok["n_cells"], "input_tokens": tok["input"],
            "output_tokens": tok["output"], "reasoning_tokens": tok["reasoning"],
            "total_tokens": tok["total"],
            "compiled": fail["compiled"], "compile_fail": fail["compile_fail"],
            "no_response": fail["no_response"],
            "timeout": pf["timeout"], "image_dropped": pf["image_dropped"],
            "http_error": pf["http_error"], "network_error": pf["network_error"],
            "provider": prov["provider"], "max_tokens": prov["max_tokens"],
            "temperature": prov["temperature"], "reasoning_leak": prov["reasoning_leak"],
            "source_a_has_pred_false": fail["reconcile"]["source_a_has_pred_false"],
            "source_b_no_response": fail["reconcile"]["source_b_no_response"],
            "reconcile_ok": fail["reconcile"]["ok"],
        })
    return rows


def _fmt_m(n: int) -> str:
    """Token count as millions, 3 dp (the table reads in M for 1000-cell runs)."""
    return f"{n / 1e6:.3f}M"


def render_markdown(records: list[dict], meta: dict, crowding: dict | None = None) -> str:
    out: list[str] = []
    out.append("# Run-level aggregator — zero-shot image→PlantUML benchmark")
    out.append("")
    out.append(f"**Models included: {meta['models_included']}/{meta['models_total']}** "
               f"(panel: {meta['label']}).")
    out.append("")
    if meta["pending_ids"]:
        out.append("Pending / not yet scored: " + ", ".join(meta["pending_ids"]))
        out.append("")
    if meta["desynced"]:
        out.append("**Excluded — source A/B desync** (run dir resumed after scoring; "
                   "re-score to include):")
        for d in meta["desynced"]:
            out.append(f"- {d['display']} (`{d['model_id']}`): source-A "
                       f"has_pred==false = {d['source_a_has_pred_false']}, source-B "
                       f"no-response = {d['source_b_no_response']}")
        out.append("")
    if meta["refused_ids"]:
        out.append("Refused (reasoning leak): " + ", ".join(meta["refused_ids"]))
        out.append("")

    # (a) token table
    out.append("## Token totals (all 1000 cells incl. failures)")
    out.append("")
    out.append("Output already includes reasoning (no double count); Gemini output = "
               "candidates + thoughts. No dollar pricing (out of scope).")
    out.append("")
    out.append("| Model | cells | input | output | reasoning | total |")
    out.append("|---|--:|--:|--:|--:|--:|")
    for r in records:
        t = r["tokens"]
        out.append(f"| {r['display']} | {t['n_cells']} | {_fmt_m(t['input'])} | "
                   f"{_fmt_m(t['output'])} | {_fmt_m(t['reasoning'])} | {_fmt_m(t['total'])} |")
    out.append("")

    # (c) failure/outcome inventory
    out.append("## Failure / outcome inventory")
    out.append("")
    out.append("Provider/harness failure (source B) vs model compile-fail (source A "
               "CSR). `no_response` reconciles with source-A `has_pred==false`.")
    out.append("")
    out.append("| Model | compiled | compile-fail | no-response | timeout | "
               "image_dropped | http_error | network_error | reconcile |")
    out.append("|---|--:|--:|--:|--:|--:|--:|--:|:--:|")
    for r in records:
        f = r["failures"]
        pf = f["provider_failures"]
        rc = "✓" if f["reconcile"]["ok"] else "✗"
        out.append(f"| {r['display']} | {f['compiled']} | {f['compile_fail']} | "
                   f"{f['no_response']} | {pf['timeout']} | {pf['image_dropped']} | "
                   f"{pf['http_error']} | {pf['network_error']} | {rc} |")
    out.append("")

    # (d) provenance manifest
    out.append("## Provenance manifest")
    out.append("")
    out.append("| Model | snapshot | provider | base_url | reasoning config | "
               "max_tokens | temp | started | leak |")
    out.append("|---|---|---|---|---|--:|--:|---|--:|")
    for r in records:
        p = r["provenance"]
        out.append(f"| {r['display']} | `{p['model']}` | {p['provider']} | "
                   f"{p['base_url']} | `{json.dumps(p['extra_body'])}` | "
                   f"{p['max_tokens']} | {p['temperature']} | {p['started']} | "
                   f"{p['reasoning_leak']} |")
    out.append("")

    # (e) crowding descriptor (model-independent; full artifact in crowding.json)
    if crowding is not None:
        out.append("## Per-tier crowding descriptor (model-independent)")
        out.append("")
        out.append(f"{crowding['metric']}; from the real `data/puml_images_1568/` PNG "
                   f"dimensions ({crowding['n']} diagrams). Machine artifact: "
                   "`crowding.json` (Task-3 `crowding=` hook).")
        out.append("")
        out.append("| Tier | n | content_lines | MP | lines/MP |")
        out.append("|---|--:|--:|--:|--:|")
        for tier in sorted(crowding["by_tier"]):
            c = crowding["by_tier"][tier]
            out.append(f"| {tier} | {c['n']} | {c['content_lines']} | {c['mp']:.2f} | "
                       f"{c['lines_per_mp']:.2f} |")
        out.append("")
    return "\n".join(out) + "\n"


def write_run_level(records: list[dict], meta: dict, out_dir,
                    basename: str = "run_level", crowding: dict | None = None) -> dict:
    """Write JSON + markdown + CSV under ``out_dir``; return {kind: Path}.
    Deterministic (sorted iteration, no timestamps)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": out_dir / f"{basename}.json",
        "md": out_dir / f"{basename}.md",
        "csv": out_dir / f"{basename}.csv",
    }
    paths["json"].write_text(
        json.dumps({"meta": meta, "models": records}, indent=2) + "\n", encoding="utf-8")
    paths["md"].write_text(render_markdown(records, meta, crowding), encoding="utf-8")
    with open(paths["csv"], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(run_level_csv_rows(records))
    return paths


CROWDING_CSV_FIELDS = ["scope", "tier", "n", "content_lines", "mp", "lines_per_mp",
                       "mean_mp", "mean_lines_per_mp"]


def crowding_csv_rows(crowding: dict) -> list[dict]:
    rows = []
    for tier in sorted(crowding["by_tier"]):
        c = crowding["by_tier"][tier]
        rows.append({"scope": "all", "tier": tier, **{k: c[k] for k in
                     ("n", "content_lines", "mp", "lines_per_mp", "mean_mp", "mean_lines_per_mp")}})
    for typ in sorted(crowding["by_type_tier"]):
        for tier in sorted(crowding["by_type_tier"][typ]):
            c = crowding["by_type_tier"][typ][tier]
            rows.append({"scope": typ, "tier": tier, **{k: c[k] for k in
                         ("n", "content_lines", "mp", "lines_per_mp", "mean_mp", "mean_lines_per_mp")}})
    return rows


def write_crowding(crowding: dict, out_dir, basename: str = "crowding") -> dict:
    """Write the model-independent crowding descriptor: JSON (Task-3 consumable) + CSV
    (flat per-tier). Emitted once per build (not per panel)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {"json": out_dir / f"{basename}.json", "csv": out_dir / f"{basename}.csv"}
    paths["json"].write_text(json.dumps(crowding, indent=2) + "\n", encoding="utf-8")
    with open(paths["csv"], "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CROWDING_CSV_FIELDS)
        w.writeheader()
        w.writerows(crowding_csv_rows(crowding))
    return paths
