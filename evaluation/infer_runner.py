#!/usr/bin/env python3
"""Inference runner (evaluation_plan.md step 1.1).

Sends standardized test-set diagram images to one hosted model with the frozen
zero-shot prompt (prompts/zero_shot.txt) and stores every raw response
untouched under the run directory. Hardened for unattended batches:

  - warmup: image-bearing throwaway calls until the endpoint ingests the image
    (Featherless drops it on cold start); aborts if it never warms.
  - per-call ingestion validation (prompt_tokens > text-only baseline) with
    bounded retry; a persistent drop is recorded, never scored.
  - transient HTTP (408/429/5xx) and network errors retried with backoff; one
    bad call never kills the batch.
  - every cell ends in a stored record: the raw response on success, else a
    failure record {"error": timeout|image_dropped|http_error|network_error}.
    No .puml is written on failure, so CSR scores the cell 0 downstream.
  - resumable: --run-dir <existing dir> skips stored successes (never
    overwritten) and re-attempts failures.
  - run_meta.json pins model, prompt, and decoding params per run.

--n defaults to 5 (smoke-test rule: pass on a handful first); a real 1k run is
--n 1000, other defaults are run-ready.

Usage (invoke from project root):
  FEATHERLESS_API_KEY=<your-key> python3 evaluation/infer_runner.py
  (per-model flags — --base-url / --key-env / --provider / --extra-body —
  are tabulated in evaluation_plan.md §3; --provider gemini speaks the native
  generateContent API, everything else OpenAI chat-completions)
"""
from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import signal
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()

# The frozen zero-shot prompt (one shared template for every model and diagram
# type; methodology/benchmark-protocol.md §1). Resolved relative to this file
# so the script works from any CWD.
_PROMPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "prompts", "zero_shot.txt")
with open(_PROMPT_PATH, encoding="utf-8") as _f:
    PROMPT = _f.read().strip()


def image_data_url(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"data:image/png;base64,{b64}"


class ApiHttpError(Exception):
    """Non-2xx API response, with the body kept for the failure record."""

    def __init__(self, code, detail):
        self.code = code
        self.detail = detail
        super().__init__(f"HTTP {code}")


def build_body(model, content, max_tokens, extra_body=None,
               token_field="max_tokens"):
    """Chat-completions request body. `extra_body` carries the per-model
    reasoning config (methodology/benchmark-protocol.md §3), e.g.
    {"chat_template_kwargs": {"enable_thinking": false}} for Qwen3.5 or
    {"reasoning_effort": "none"} for GPT-5.x, and wins over defaults.
    `token_field` names the output-cap parameter: GPT-5.x rejects
    `max_tokens` and requires `max_completion_tokens`."""
    body = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        token_field: max_tokens,
        "temperature": 0,
    }
    if extra_body:
        body.update(extra_body)
    return body


def build_gemini_body(content, max_tokens, extra_body=None):
    """Native Gemini `generateContent` body from the OpenAI-style content list.

    Gemini 3.1 Pro is run through the native REST API (not the OpenAI-compat
    layer) because methodology §3 reports per-call `thoughtsTokenCount`, which
    only the native response's `usageMetadata` carries. `extra_body` merges
    into `generationConfig` (e.g. {"thinkingConfig": {"thinkingLevel": "low"}}).
    Field names per https://ai.google.dev/api/generate-content (verified
    2026-06-12): `inline_data`/`mime_type`, `generationConfig.maxOutputTokens`.
    """
    parts = []
    for item in content:
        if item["type"] == "text":
            parts.append({"text": item["text"]})
        elif item["type"] == "image_url":
            header, b64 = item["image_url"]["url"].split(",", 1)
            mime = header.split(":", 1)[1].split(";", 1)[0]
            parts.append({"inline_data": {"mime_type": mime, "data": b64}})
    config = {"temperature": 0, "maxOutputTokens": max_tokens}
    if extra_body:
        config.update(extra_body)
    return {"contents": [{"parts": parts}], "generationConfig": config}


def prompt_tokens(response):
    """Prompt-token count from either response shape: OpenAI chat-completions
    `usage.prompt_tokens` or native Gemini `usageMetadata.promptTokenCount`."""
    if "usageMetadata" in response:
        return response["usageMetadata"].get("promptTokenCount", 0)
    return response.get("usage", {}).get("prompt_tokens", 0)


def completion_tokens(response):
    if "usageMetadata" in response:
        return response["usageMetadata"].get("candidatesTokenCount", 0)
    return response.get("usage", {}).get("completion_tokens", 0)


def thoughts_tokens(response):
    """Gemini-only thinking-token count (reported per methodology §3 because
    thinking cannot be disabled on the Pro tier); None for chat-completions."""
    if "usageMetadata" in response:
        return response["usageMetadata"].get("thoughtsTokenCount", 0)
    return None


def completion_text(response):
    """The model's text from either response shape. Gemini: thought parts
    (present only with includeThoughts) are skipped; a candidate that spent
    its whole maxOutputTokens on thinking has no parts -> empty string."""
    if "candidates" in response:
        parts = response["candidates"][0].get("content", {}).get("parts", [])
        return "".join(p.get("text", "") for p in parts if not p.get("thought"))
    return response["choices"][0]["message"]["content"] or ""


def resolve_api_key(env_name, environ=os.environ):
    """API key from the env var named by --key-env (provider-agnostic:
    FEATHERLESS_API_KEY / OPENAI_API_KEY / ANTHROPIC_API_KEY / GEMINI_API_KEY)."""
    key = environ.get(env_name, "")
    if not key:
        raise SystemExit(f"set {env_name} (e.g. {env_name}=$(cat <key-file>))")
    return key


def reasoning_leak(text):
    """True iff the completion carries an inline reasoning block. A leaked
    <think> block before @startuml would be silently stripped by block
    isolation, so thinking mode would corrupt the run invisibly downstream —
    it must be caught here."""
    return "<think" in text.lower()


def call(base_url, key, model, content, max_tokens, timeout, extra_body=None,
         provider="openai", token_field="max_tokens"):
    """One API call. provider="openai": chat-completions (OpenAI, Featherless,
    Anthropic's OpenAI-compat layer). provider="gemini": native generateContent
    (URL pattern + x-goog-api-key header per ai.google.dev REST docs)."""
    if provider == "gemini":
        url = base_url.rstrip("/") + f"/models/{model}:generateContent"
        body = json.dumps(build_gemini_body(content, max_tokens, extra_body)).encode()
        auth = {"x-goog-api-key": key}
    else:
        url = base_url.rstrip("/") + "/chat/completions"
        body = json.dumps(build_body(model, content, max_tokens, extra_body,
                                     token_field)).encode()
        auth = {"Authorization": f"Bearer {key}"}
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            **auth,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0 Safari/537.36",
        },
    )
    # Hard wall-clock deadline: urllib's socket timeout only trips on byte-level
    # inactivity, so a server that trickles bytes can hang forever. SIGALRM fires
    # regardless. (Main thread only; fine for this single-threaded smoke.)
    def _on_alarm(signum, frame):
        raise TimeoutError(f"hard deadline {timeout}s")
    old = signal.signal(signal.SIGALRM, _on_alarm)
    signal.alarm(timeout)
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CTX) as resp:
            return json.loads(resp.read()), time.time() - t0
    except urllib.error.HTTPError as e:
        raise ApiHttpError(e.code, e.read().decode("utf-8", "replace")) from e
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


RETRIABLE_HTTP = {408, 429, 500, 502, 503, 504}


def call_with_retry(call_fn, retries=3, base_delay=5.0, sleep=time.sleep, log=print):
    """Run a no-arg call thunk, retrying transient failures with backoff.

    Retriable: HTTP {408, 429, 5xx}, network-level URLError, and a raw
    ConnectionError (reset/abort during the response read — not wrapped in
    URLError). NOT retriable: other HTTP codes (a 400/401 will not heal) and
    TimeoutError — a timeout is a per-cell verdict (no-EOS spirals reproduce
    deterministically; retrying burns the full deadline again for the same
    outcome). TimeoutError is a sibling OSError of ConnectionError, so catching
    ConnectionError (not OSError) keeps that verdict intact.
    """
    for attempt in range(retries + 1):
        try:
            return call_fn()
        except ApiHttpError as e:
            if e.code not in RETRIABLE_HTTP or attempt == retries:
                raise
            reason = f"HTTP {e.code}"
        except urllib.error.URLError as e:
            if attempt == retries:
                raise
            reason = f"network: {e.reason}"
        except ConnectionError as e:
            # reset/abort mid-read surfaces as a raw socket error, not a URLError
            if attempt == retries:
                raise
            reason = f"connection: {e}"
        except json.JSONDecodeError as e:
            # truncated/garbled body: resp.read() returned partial bytes on a
            # clean early close, so json.loads parses bad (no socket exception
            # raised). Transient — a fresh request usually returns whole.
            if attempt == retries:
                raise
            reason = f"bad json: {e}"
        except http.client.HTTPException as e:
            # malformed/cut HTTP response — e.g. IncompleteRead when a chunked
            # stream is severed mid-transfer (resp.read() fails before parsing),
            # or BadStatusLine. Transient — a fresh request usually completes.
            if attempt == retries:
                raise
            reason = f"http read: {type(e).__name__}: {e}"
        delay = base_delay * (2 ** attempt)
        log(f"   transient ({reason}), retry {attempt + 1}/{retries} in {delay:.0f}s")
        sleep(delay)


def ingested(response, baseline):
    """True iff the image reached the model: prompt_tokens above the text-only
    baseline. A response without usage cannot be verified -> treated as a drop."""
    return prompt_tokens(response) > baseline


def infer_cell(call_fn, baseline, drop_retries=2, log=print):
    """One benchmark cell -> outcome record {status, attempts, ...}.

    status "ok": image-validated response in "response". "image_dropped": every
    attempt returned a text-only prompt_token count (the last blind completion
    is kept in "response" for the record, never scored). "timeout" /
    "http_error" / "network_error" / "bad_response": the exception detail in
    "detail". "bad_response" (a persistent truncated/garbled JSON body) is a
    transport failure like "network_error" — recoverable on a targeted resume,
    never scored — kept as a distinct status so it is visible in the tally.
    """
    attempts = 0
    last = None
    while attempts <= drop_retries:
        attempts += 1
        try:
            response, secs = call_fn()
        except TimeoutError as e:
            return {"status": "timeout", "attempts": attempts, "detail": str(e)}
        except ApiHttpError as e:
            return {"status": "http_error", "attempts": attempts,
                    "detail": f"HTTP {e.code}: {e.detail[:2000]}"}
        except (urllib.error.URLError, ConnectionError) as e:
            return {"status": "network_error", "attempts": attempts,
                    "detail": str(e)}
        except (json.JSONDecodeError, http.client.HTTPException) as e:
            return {"status": "bad_response", "attempts": attempts,
                    "detail": f"{type(e).__name__}: {e}"}
        if ingested(response, baseline):
            return {"status": "ok", "attempts": attempts,
                    "response": response, "secs": secs}
        last = response
        log(f"   image DROPPED (attempt {attempts}/{drop_retries + 1})")
    return {"status": "image_dropped", "attempts": attempts, "response": last}


def warmup(call_fn, baseline, max_tries=5, log=print):
    """Throwaway image-bearing calls until the endpoint ingests the image
    (Featherless drops it on cold start). Returns the number of calls used;
    aborts the run if the endpoint never warms — launching the batch would
    silently score blind completions."""
    for i in range(1, max_tries + 1):
        try:
            response, _ = call_fn()
        except (TimeoutError, ApiHttpError, urllib.error.URLError) as e:
            log(f"   warmup call {i}/{max_tries} failed: {e}")
            continue
        if ingested(response, baseline):
            return i
        log(f"   warmup call {i}/{max_tries}: image still dropped")
    raise SystemExit(f"endpoint did not ingest the image in {max_tries} warmup calls")


def pick(diagrams, n):
    """Deterministic spread across types/tiers: stride through the frozen list."""
    step = max(1, len(diagrams) // n)
    return [diagrams[i * step] for i in range(n)]


def format_progress(done, total, tally, elapsed=None):
    """One-line operator-facing rolling status: batch position, live tally, and
    an optional rough ETA. Pure stdout decoration — never touches the on-disk
    reproducibility artifact. `done` is the 1-based count of cells reached
    (resume-skips included); `tally` the running {status: count} dict; `elapsed`
    wall-clock seconds since the loop started (omit -> no ETA). ETA is the naive
    (elapsed/done)*(total-done) projection, rounded to whole minutes."""
    parts = [f"[{done}/{total}]"]
    parts += [f"{k}={v}" for k, v in tally.items()]
    if elapsed is not None and done:
        eta = (elapsed / done) * (total - done)
        parts.append(f"~{round(eta / 60)}m")
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="https://api.featherless.ai/v1")
    ap.add_argument("--model", default="Qwen/Qwen3.5-2B")
    ap.add_argument("--test-set", default="data/test_set.json")
    ap.add_argument("--images", default="data/puml_images_1568")
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--keys", default="", help="comma-separated blob_id prefixes to target instead of the spread; repeats each --repeat times")
    ap.add_argument("--repeat", type=int, default=1, help="send each selected diagram this many times (cold-start/stall test)")
    # Sized ~1.5x the longest test-set GT (3546 Qwen3.5-2B tokens, see
    # data/gt_token_stats.json), rounded up to the nearest 256: large enough that
    # a legitimate long diagram is never silently truncated, small enough that a
    # no-EOS repetition loop is cut off and cascades to CSR=0 (methodology §1).
    ap.add_argument("--max-tokens", type=int, default=5376)
    # Sized to the worst LEGITIMATE generation (~max_tokens / observed 40-52
    # tok/s + prefill margin). A timeout is recorded as a failure
    # (no .puml -> CSR 0); do NOT set it tight: that kills slow-but-valid long
    # outputs and biases against complex tiers.
    ap.add_argument("--timeout", type=int, default=90, help="per-call hard deadline, seconds")
    ap.add_argument("--out", default="data/runs")
    ap.add_argument("--run-dir", default="",
                    help="resume into this existing run dir: cells with a stored "
                         "successful response are skipped, failed cells re-attempted")
    ap.add_argument("--token-field", default="max_tokens",
                    choices=["max_tokens", "max_completion_tokens"],
                    help="output-cap parameter name; GPT-5.x requires "
                         "max_completion_tokens")
    ap.add_argument("--provider", default="openai", choices=["openai", "gemini"],
                    help="API shape: openai = chat-completions (OpenAI, "
                         "Featherless, Anthropic OpenAI-compat); gemini = "
                         "native generateContent (preserves thoughtsTokenCount; "
                         "--extra-body merges into generationConfig)")
    ap.add_argument("--key-env", default="FEATHERLESS_API_KEY",
                    help="env var holding the API key for --base-url "
                         "(e.g. OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY)")
    ap.add_argument("--extra-body", default="",
                    help="JSON merged into every request body — the per-model "
                         "reasoning config (methodology §3), e.g. "
                         '\'{"chat_template_kwargs": {"enable_thinking": false}}\'')
    args = ap.parse_args()
    extra_body = json.loads(args.extra_body) if args.extra_body else None

    key = resolve_api_key(args.key_env)

    all_diagrams = json.load(open(args.test_set))["diagrams"]
    if args.keys:
        wanted = [k.strip() for k in args.keys.split(",") if k.strip()]
        selected = [r for r in all_diagrams
                    if any(r["blob_id"].startswith(w) for w in wanted)]
    else:
        selected = pick(all_diagrams, args.n)
    diagrams = [r for r in selected for _ in range(args.repeat)]

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.run_dir:
        run_dir = args.run_dir
        if not os.path.isdir(run_dir):
            raise SystemExit(f"--run-dir {run_dir} does not exist")
    else:
        run_dir = os.path.join(args.out, f"{args.model.replace('/', '_')}_{stamp}")
    os.makedirs(run_dir, exist_ok=True)

    def api_call(content, max_tokens):
        return call_with_retry(lambda: call(args.base_url, key, args.model,
                                            content, max_tokens, args.timeout,
                                            extra_body, provider=args.provider,
                                            token_field=args.token_field))

    # Text-only baseline: prompt_tokens for an image-bearing call must exceed
    # this. Cap 16, not 1: GPT-5.2 returns HTTP 400 (not a truncated 200) when
    # generation hits the output cap, so a 1-token throwaway call always fails.
    base_resp, _ = api_call([{"type": "text", "text": PROMPT}], max_tokens=16)
    baseline = prompt_tokens(base_resp)
    print(f"model={args.model}")
    print(f"text-only baseline prompt_tokens = {baseline}")
    print(f"run dir = {run_dir}", flush=True)

    # Warm the endpoint until it ingests an image (cold-start drop defense);
    # throwaway calls on the first diagram's image, never scored.
    first_img = image_data_url(
        os.path.join(args.images, diagrams[0]["key"][:-5] + ".png"))
    warm_content = [{"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": first_img}}]
    warm_calls = warmup(lambda: api_call(warm_content, max_tokens=16), baseline)
    print(f"endpoint warm after {warm_calls} call(s)", flush=True)

    with open(os.path.join(run_dir, "run_meta.json"), "w") as f:
        json.dump({"model": args.model, "base_url": args.base_url,
                   "provider": args.provider, "token_field": args.token_field,
                   "prompt": PROMPT, "max_tokens": args.max_tokens,
                   "timeout": args.timeout, "temperature": 0,
                   "extra_body": extra_body,
                   "test_set": args.test_set, "images": args.images,
                   "n_cells": len(diagrams), "baseline_prompt_tokens": baseline,
                   "warmup_calls": warm_calls, "started": stamp}, f, indent=2)

    tally = {}
    total = len(diagrams)
    loop_start = time.time()
    for attempt, r in enumerate(diagrams):
        base = r["key"][:-5]
        stem = f"{base}_a{attempt}" if args.repeat > 1 else base
        json_path = os.path.join(run_dir, stem + ".json")

        # Resume: a stored successful response is final (never overwritten);
        # a stored failure record is re-attempted.
        if os.path.exists(json_path):
            with open(json_path) as f:
                prev = json.load(f)
            if "error" not in prev:
                tally["skipped"] = tally.get("skipped", 0) + 1
                print(f"[{attempt + 1}/{total}] -> {base[:18]} already done, "
                      f"skipping", flush=True)
                print(format_progress(attempt + 1, total, tally,
                                      time.time() - loop_start), flush=True)
                continue

        print(f"\n[{attempt + 1}/{total}] -> {base[:18]} ({r['primary_type']} "
              f"T{r['tier']}, {r['image_width']}x{r['image_height']}) sending...",
              flush=True)
        img = image_data_url(os.path.join(args.images, base + ".png"))
        content = [{"type": "text", "text": PROMPT},
                   {"type": "image_url", "image_url": {"url": img}}]
        out = infer_cell(lambda: api_call(content, args.max_tokens), baseline)
        tally[out["status"]] = tally.get(out["status"], 0) + 1

        if out["status"] != "ok":
            # Failure record instead of a poisoned/absent cell; no .puml, so
            # downstream CSR scores the cell 0 while the cause stays on disk.
            record = {"error": out["status"], "key": base,
                      "attempts": out["attempts"]}
            if "detail" in out:
                record["detail"] = out["detail"]
            if "response" in out:  # the blind completion of an image_dropped cell
                record["response"] = out["response"]
            with open(json_path, "w") as f:
                json.dump(record, f, indent=2)
            print(f"   FAIL {out['status']} (attempts={out['attempts']})", flush=True)
            print(format_progress(attempt + 1, total, tally,
                                  time.time() - loop_start), flush=True)
            continue

        # Persist the raw response verbatim before touching it.
        resp = out["response"]
        with open(json_path, "w") as f:
            json.dump(resp, f, indent=2)
        code = completion_text(resp)
        with open(os.path.join(run_dir, stem + ".puml"), "w") as f:
            f.write(code)
        leak = reasoning_leak(code)
        if leak:
            tally["reasoning_leak"] = tally.get("reasoning_leak", 0) + 1
        thoughts = thoughts_tokens(resp)
        print(f"   ptok={prompt_tokens(resp)} "
              f"ctok={completion_tokens(resp)} "
              f"{f'ttok={thoughts} ' if thoughts is not None else ''}"
              f"{out['secs']:.1f}s "
              f"attempts={out['attempts']} "
              f"@startuml={'@startuml' in code} @enduml={'@enduml' in code}"
              f"{'  REASONING LEAK!' if leak else ''}",
              flush=True)
        print(format_progress(attempt + 1, total, tally,
                              time.time() - loop_start), flush=True)

    print(f"\nraw responses + extracted .puml in {run_dir}")
    print("outcome tally:", json.dumps(tally))
    if tally.get("reasoning_leak"):
        print(f"WARNING: {tally['reasoning_leak']} completion(s) contain a "
              f"<think> block — thinking mode is ON for this model/config; "
              f"fix --extra-body before scoring (methodology §3).")
    failed = sum(v for k, v in tally.items()
                 if k not in ("ok", "skipped", "reasoning_leak"))
    if failed:
        print(f"{failed} cell(s) failed — re-run with --run-dir {run_dir} "
              f"to retry just those.")


if __name__ == "__main__":
    main()
