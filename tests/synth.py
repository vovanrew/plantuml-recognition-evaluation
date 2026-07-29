"""Shared synthetic ModelData builder for the analysis unit tests.

Not collected by pytest (no ``test_`` prefix). Mirrors the joined-row shape the
loader produces and the summary blocks the aggregator reads through.

Also carries source-B fixtures (Task 5): the polymorphic per-key API-response
records (OpenAI/Claude/Qwen ``usage`` shape, Gemini ``usageMetadata`` shape, the
harness error record, and the ``image_dropped`` record that nests a provider
response with usage) plus a minimal PNG IHDR header builder and a tiny run-dir
writer, so the run-level aggregator's pure helpers can be tested on disk-free
fixtures.
"""
import json
import struct
from pathlib import Path

from analysis.aggregate import RELATIONS
from analysis.loader import ModelData
from analysis.registry import ModelEntry


def make_row(key, typ, tier, compiled, el, rel, chrf, ta, rel_type="message",
             has_pred=True, csr_error=None):
    """A joined per-diagram row, mirroring the loader's shape.

    ``has_pred`` / ``csr_error`` default to the original behaviour (a model that
    produced a prediction; null CSR error). Set ``has_pred=False`` with
    ``csr_error="no prediction (missing/timeout)"`` to synthesize a provider/harness
    drop row (the Task-4 sampler's ``provider_drop`` outcome); pass a
    ``csr_error="Error line N..."`` string for a model compile-fail row.
    """
    def f1(tp, fp, fn):
        p = tp / (tp + fp) if tp + fp else 0.0
        r = tp / (tp + fn) if tp + fn else 0.0
        return p, r, (2 * p * r / (p + r) if p + r else 0.0)
    elp = dict(zip(("precision", "recall", "f1"), f1(*el)))
    relp = dict(zip(("precision", "recall", "f1"), f1(*rel)))
    # Per-diagram per-relation tp/fp/fn (the runner's additive emission): the whole
    # edge count sits in one relation so sum_rel == overall (the partition invariant).
    by_relation = {r: {"tp": 0, "fp": 0, "fn": 0} for r in RELATIONS}
    by_relation[rel_type] = {"tp": rel[0], "fp": rel[1], "fn": rel[2]}
    return {
        "key": key, "primary_type": typ, "tier": tier,
        "csr": {"key": key, "compiled": compiled, "error": csr_error},
        "element": {"key": key, "tp": el[0], "fp": el[1], "fn": el[2], **elp,
                    "has_pred": has_pred, "compiled": compiled,
                    "type_accuracy": {"matched": ta[0], "correct": ta[1], "excluded": ta[2]}},
        "relationship": {"key": key, "tp": rel[0], "fp": rel[1], "fn": rel[2], **relp,
                         "has_pred": has_pred, "compiled": compiled, "by_relation": by_relation},
        "chrf": {"key": key, "has_pred": has_pred, "compiled": compiled, "score": chrf},
    }


def synth_model(mid="m1", display="M1"):
    rows = [
        make_row("d1", "class", 1, True, (2, 0, 0), (1, 0, 0), 80.0, (2, 2, 0), rel_type="inheritance"),
        make_row("d2", "class", 2, False, (0, 0, 3), (0, 0, 1), 5.0, (0, 0, 0), rel_type="message"),
        make_row("d3", "sequence", 1, True, (1, 1, 0), (2, 0, 1), 60.0, (1, 0, 0), rel_type="message"),
        make_row("d4", "sequence", 3, True, (3, 0, 1), (1, 1, 0), 70.0, (3, 3, 0), rel_type="inheritance"),
    ]
    by_rel = {r: {"precision": 0.5, "recall": 0.5, "f1": 0.5, "support_gt": 10,
                  "support_pred": 8, "n_diagrams_with_gt": 3, "n": 4} for r in RELATIONS}
    summaries = {
        "csr": {"n": 4, "compiled": 3, "csr": 0.75},
        "element_f1": {"type_accuracy": {
            "matched": 6, "correct": 5, "excluded": 0, "denominator": 6,
            "accuracy": 5 / 6, "population": "compiled_only",
            "per_type": {"class": {"support": 4, "correct": 4, "accuracy": 1.0},
                         "participant": {"support": 2, "correct": 1, "accuracy": 0.5}}}},
        "relationship_f1": {"zeros_for_failed": {"by_relation": by_rel},
                            "compiled_only": {"by_relation": by_rel}},
        "chrf": {"zeros_for_failed": {"micro": 50.0}, "compiled_only": {"micro": 70.0}},
    }
    entry = ModelEntry(id=mid, display=display, run_dir="r", status="scored", lab="qwen",
                       arm="qwen", family="dense", params_total_b=9, params_active_b=9,
                       supplementary=False)
    return ModelData(entry=entry, rows=rows, summaries=summaries)


# --------------------------------------------------------------------------- #
# source-B fixtures (Task 5): raw per-key API responses + run_meta + PNG headers
# --------------------------------------------------------------------------- #

def srcb_openai(prompt=100, completion=200, reasoning=None):
    """A successful OpenAI/Claude/Qwen response: top-level ``usage``. ``completion``
    already INCLUDES any reasoning (do not re-add). ``reasoning`` (GPT only) is the
    reasoning subtotal, surfaced under ``completion_tokens_details``; omit for the
    Claude/Qwen shape that carries no details sub-object."""
    usage = {"prompt_tokens": prompt, "completion_tokens": completion,
             "total_tokens": prompt + completion}
    if reasoning is not None:
        usage["completion_tokens_details"] = {"reasoning_tokens": reasoning}
        usage["prompt_tokens_details"] = {"cached_tokens": 0}
    return {"id": "cmpl-x", "object": "chat.completion", "usage": usage}


def srcb_gemini(prompt=100, candidates=200, thoughts=None):
    """A successful Gemini native ``generateContent`` response: ``usageMetadata``.
    ``thoughtsTokenCount`` is ABSENT when zero (pass ``thoughts=None``)."""
    um = {"promptTokenCount": prompt, "candidatesTokenCount": candidates,
          "totalTokenCount": prompt + candidates,
          "promptTokensDetails": [{"modality": "TEXT", "tokenCount": prompt}]}
    if thoughts is not None:
        um["thoughtsTokenCount"] = thoughts
        um["totalTokenCount"] += thoughts
    return {"usageMetadata": um}


def srcb_error(category="timeout", key="d1", attempts=3, detail="..."):
    """A pure harness error record (no usage): timeout/http_error/network_error."""
    return {"error": category, "key": key, "attempts": attempts, "detail": detail}


def srcb_image_dropped(key="d1", prompt=93, completion=5376, attempts=3):
    """An ``image_dropped`` record: a harness failure that KEPT the provider response
    (with usage) under ``response`` -- the billed tokens must still be counted."""
    return {"error": "image_dropped", "key": key, "attempts": attempts,
            "response": srcb_openai(prompt=prompt, completion=completion)}


def png_header_bytes(width, height):
    """Minimal valid PNG header: 8-byte signature + IHDR length/type + width/height.
    The dimension reader only needs the first 24 bytes (bytes 16:24 = w,h)."""
    sig = bytes.fromhex("89504e470d0a1a0a")
    return sig + struct.pack(">I", 13) + b"IHDR" + struct.pack(">II", width, height)


def write_run_dir(base, run_dir, records, meta):
    """Write a tiny source-B run dir: ``<key>.json`` per record + ``run_meta.json``.
    ``records`` maps key -> response dict. Returns the run-dir Path."""
    d = Path(base) / "runs" / run_dir
    d.mkdir(parents=True, exist_ok=True)
    for key, rec in records.items():
        (d / f"{key}.json").write_text(json.dumps(rec), encoding="utf-8")
    (d / "run_meta.json").write_text(json.dumps(meta), encoding="utf-8")
    return d


def run_meta(model="m1", provider="openai", base_url="https://api.x/v1",
             extra_body=None, max_tokens=5376, temperature=0, started="20260613T000000Z"):
    """A run_meta.json provenance dict (Task-5 provenance manifest source)."""
    return {"model": model, "base_url": base_url, "provider": provider,
            "token_field": "max_completion_tokens", "prompt": "p", "max_tokens": max_tokens,
            "timeout": 90, "temperature": temperature,
            "extra_body": extra_body if extra_body is not None else {"reasoning_effort": "none"},
            "test_set": "data/test_set.json", "images": "data/puml_images_1568",
            "n_cells": 1000, "baseline_prompt_tokens": 85, "warmup_calls": 1, "started": started}
