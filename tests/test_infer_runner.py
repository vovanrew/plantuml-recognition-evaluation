"""Tests for the inference-harness hardening logic (infer_runner.py).

Covers the pure decision layer — transient-HTTP retry, per-cell outcome
classification (ok / image_dropped / timeout / http_error / network_error /
bad_response), and endpoint warmup — with injected fake call thunks; no
network involved.
"""
import http.client
import json
import urllib.error

import pytest

import infer_runner as ir


def ok_response(prompt_tokens=500):
    return ({"usage": {"prompt_tokens": prompt_tokens, "completion_tokens": 7},
             "choices": [{"message": {"content": "@startuml\nA -> B\n@enduml"}}]},
            1.0)


def seq(*outcomes):
    """A no-arg call thunk that replays outcomes; exceptions are raised."""
    it = iter(outcomes)
    calls = []

    def thunk():
        calls.append(1)
        out = next(it)
        if isinstance(out, BaseException):
            raise out
        return out
    thunk.calls = calls
    return thunk


# --- call_with_retry: transient HTTP/network errors ---

def test_retry_recovers_from_429():
    thunk = seq(ir.ApiHttpError(429, "rate limited"), ok_response())
    naps = []
    resp, _ = ir.call_with_retry(thunk, sleep=naps.append, log=lambda *_: None)
    assert resp["usage"]["prompt_tokens"] == 500
    assert len(thunk.calls) == 2 and len(naps) == 1


def test_retry_gives_up_after_exhausting_attempts():
    thunk = seq(*[ir.ApiHttpError(503, "down")] * 4)
    with pytest.raises(ir.ApiHttpError):
        ir.call_with_retry(thunk, retries=3, sleep=lambda _: None, log=lambda *_: None)
    assert len(thunk.calls) == 4  # initial + 3 retries


def test_retry_does_not_retry_client_errors():
    thunk = seq(ir.ApiHttpError(400, "bad request"), ok_response())
    with pytest.raises(ir.ApiHttpError):
        ir.call_with_retry(thunk, sleep=lambda _: None, log=lambda *_: None)
    assert len(thunk.calls) == 1


def test_retry_recovers_from_network_error():
    thunk = seq(urllib.error.URLError("connection reset"), ok_response())
    resp, _ = ir.call_with_retry(thunk, sleep=lambda _: None, log=lambda *_: None)
    assert resp["usage"]["prompt_tokens"] == 500
    assert len(thunk.calls) == 2


def test_retry_does_not_retry_timeouts():
    # a timeout is a per-cell verdict (deterministic no-EOS spirals), not transient
    thunk = seq(TimeoutError("hard deadline 90s"), ok_response())
    with pytest.raises(TimeoutError):
        ir.call_with_retry(thunk, sleep=lambda _: None, log=lambda *_: None)
    assert len(thunk.calls) == 1


def test_retry_recovers_from_connection_reset():
    # a reset during resp.read() surfaces as a raw ConnectionError, not a URLError
    thunk = seq(ConnectionResetError(54, "Connection reset by peer"), ok_response())
    resp, _ = ir.call_with_retry(thunk, sleep=lambda _: None, log=lambda *_: None)
    assert resp["usage"]["prompt_tokens"] == 500
    assert len(thunk.calls) == 2


def test_retry_gives_up_on_persistent_connection_reset():
    thunk = seq(*[ConnectionResetError("reset")] * 4)
    with pytest.raises(ConnectionError):
        ir.call_with_retry(thunk, retries=3, sleep=lambda _: None, log=lambda *_: None)
    assert len(thunk.calls) == 4


def _bad_json():
    # a truncated/garbled response body: resp.read() returned partial bytes and
    # json.loads choked mid-structure (clean early close, not a raised socket error)
    return json.JSONDecodeError("Expecting ',' delimiter", "{...", 3425)


def test_retry_recovers_from_bad_json():
    thunk = seq(_bad_json(), ok_response())
    resp, _ = ir.call_with_retry(thunk, sleep=lambda _: None, log=lambda *_: None)
    assert resp["usage"]["prompt_tokens"] == 500
    assert len(thunk.calls) == 2


def test_retry_gives_up_on_persistent_bad_json():
    thunk = seq(*[_bad_json() for _ in range(4)])
    with pytest.raises(json.JSONDecodeError):
        ir.call_with_retry(thunk, retries=3, sleep=lambda _: None, log=lambda *_: None)
    assert len(thunk.calls) == 4


def _incomplete_read():
    # a cut chunked stream: resp.read() raises before any parsing (the next
    # chunk-size line came back empty). IncompleteRead subclasses HTTPException.
    return http.client.IncompleteRead(b"1298 partial bytes")


def test_retry_recovers_from_incomplete_read():
    thunk = seq(_incomplete_read(), ok_response())
    resp, _ = ir.call_with_retry(thunk, sleep=lambda _: None, log=lambda *_: None)
    assert resp["usage"]["prompt_tokens"] == 500
    assert len(thunk.calls) == 2


def test_retry_gives_up_on_persistent_incomplete_read():
    thunk = seq(*[_incomplete_read() for _ in range(4)])
    with pytest.raises(http.client.HTTPException):
        ir.call_with_retry(thunk, retries=3, sleep=lambda _: None, log=lambda *_: None)
    assert len(thunk.calls) == 4


# --- infer_cell: per-diagram outcome classification ---

def test_cell_ok_first_attempt():
    out = ir.infer_cell(seq(ok_response()), baseline=100, log=lambda *_: None)
    assert out["status"] == "ok" and out["attempts"] == 1
    assert out["response"]["usage"]["prompt_tokens"] == 500


def test_cell_image_drop_then_ok_is_ok():
    # cold-start drop: prompt_tokens at the text-only baseline -> retry recovers
    thunk = seq(ok_response(prompt_tokens=100), ok_response(prompt_tokens=500))
    out = ir.infer_cell(thunk, baseline=100, log=lambda *_: None)
    assert out["status"] == "ok" and out["attempts"] == 2


def test_cell_persistent_drop_is_image_dropped():
    thunk = seq(*[ok_response(prompt_tokens=100)] * 3)
    out = ir.infer_cell(thunk, baseline=100, drop_retries=2, log=lambda *_: None)
    assert out["status"] == "image_dropped" and out["attempts"] == 3
    assert "response" in out  # the blind completion is kept for the record


def test_cell_missing_usage_counts_as_drop():
    resp = ({"choices": [{"message": {"content": "x"}}]}, 1.0)
    out = ir.infer_cell(seq(resp, resp, resp), baseline=100, drop_retries=2,
                        log=lambda *_: None)
    assert out["status"] == "image_dropped"


def test_cell_timeout_recorded_not_retried():
    thunk = seq(TimeoutError("hard deadline 90s"), ok_response())
    out = ir.infer_cell(thunk, baseline=100, log=lambda *_: None)
    assert out["status"] == "timeout" and out["attempts"] == 1
    assert len(thunk.calls) == 1


def test_cell_http_error_recorded():
    out = ir.infer_cell(seq(ir.ApiHttpError(401, "bad key")), baseline=100,
                        log=lambda *_: None)
    assert out["status"] == "http_error"
    assert "401" in out["detail"]


def test_cell_network_error_recorded():
    out = ir.infer_cell(seq(urllib.error.URLError("dns")), baseline=100,
                        log=lambda *_: None)
    assert out["status"] == "network_error"


def test_cell_connection_reset_recorded_as_network_error():
    # a persistent reset (re-raised by call_with_retry) becomes a failure cell,
    # never an uncaught crash of the batch
    out = ir.infer_cell(seq(ConnectionResetError(54, "Connection reset by peer")),
                        baseline=100, log=lambda *_: None)
    assert out["status"] == "network_error"


def test_cell_bad_json_recorded_as_bad_response():
    # a persistent truncated/garbled body (re-raised by call_with_retry) becomes a
    # recoverable failure cell, never an uncaught JSONDecodeError that kills the batch
    out = ir.infer_cell(seq(_bad_json()), baseline=100, log=lambda *_: None)
    assert out["status"] == "bad_response"


def test_cell_incomplete_read_recorded_as_bad_response():
    # a persistent cut chunked stream (HTTPException) is the same transport
    # failure as a truncated body — recorded, never an uncaught crash
    out = ir.infer_cell(seq(_incomplete_read()), baseline=100, log=lambda *_: None)
    assert out["status"] == "bad_response"


# --- warmup ---

def test_warmup_returns_tries_once_ingesting():
    thunk = seq(ok_response(prompt_tokens=100), ok_response(prompt_tokens=500))
    assert ir.warmup(thunk, baseline=100, log=lambda *_: None) == 2


def test_warmup_tolerates_errors_between_tries():
    thunk = seq(ir.ApiHttpError(503, "cold"), ok_response(prompt_tokens=500))
    assert ir.warmup(thunk, baseline=100, log=lambda *_: None) == 2


def test_warmup_aborts_when_endpoint_never_ingests():
    thunk = seq(*[ok_response(prompt_tokens=100)] * 5)
    with pytest.raises(SystemExit):
        ir.warmup(thunk, baseline=100, max_tries=5, log=lambda *_: None)


# --- build_body: per-model reasoning config passthrough ---

def test_build_body_core_fields():
    body = ir.build_body("m", [{"type": "text", "text": "hi"}], 5376)
    assert body["model"] == "m" and body["max_tokens"] == 5376
    assert body["temperature"] == 0
    assert body["messages"][0]["role"] == "user"


def test_build_body_merges_extra_body():
    extra = {"chat_template_kwargs": {"enable_thinking": False}}
    body = ir.build_body("Qwen/Qwen3.5-9B", [], 5376, extra_body=extra)
    assert body["chat_template_kwargs"] == {"enable_thinking": False}
    assert body["temperature"] == 0  # defaults untouched


def test_build_body_extra_body_overrides_defaults():
    # explicit per-run config wins over harness defaults
    body = ir.build_body("m", [], 5376, extra_body={"temperature": 1})
    assert body["temperature"] == 1


def test_build_body_none_extra_body():
    assert "chat_template_kwargs" not in ir.build_body("m", [], 64)


def test_build_body_max_completion_tokens_field():
    # GPT-5.x rejects max_tokens ("use 'max_completion_tokens' instead")
    body = ir.build_body("gpt-5.2-2025-12-11", [], 5376,
                         token_field="max_completion_tokens")
    assert body["max_completion_tokens"] == 5376
    assert "max_tokens" not in body


# --- Gemini native adapter: generateContent body + response accessors ---

def test_build_gemini_body_text_and_image():
    content = [{"type": "text", "text": "prompt"},
               {"type": "image_url", "image_url": {"url": "data:image/png;base64,QUJD"}}]
    body = ir.build_gemini_body(content, 5376,
                                extra_body={"thinkingConfig": {"thinkingLevel": "low"}})
    parts = body["contents"][0]["parts"]
    assert parts[0] == {"text": "prompt"}
    assert parts[1] == {"inline_data": {"mime_type": "image/png", "data": "QUJD"}}
    cfg = body["generationConfig"]
    assert cfg["temperature"] == 0 and cfg["maxOutputTokens"] == 5376
    assert cfg["thinkingConfig"] == {"thinkingLevel": "low"}


def test_build_gemini_body_without_extra_body():
    body = ir.build_gemini_body([{"type": "text", "text": "hi"}], 64)
    assert body["generationConfig"] == {"temperature": 0, "maxOutputTokens": 64}


def test_prompt_tokens_openai_shape():
    assert ir.prompt_tokens({"usage": {"prompt_tokens": 432}}) == 432


def test_prompt_tokens_gemini_shape():
    assert ir.prompt_tokens({"usageMetadata": {"promptTokenCount": 1900}}) == 1900


def test_prompt_tokens_missing_usage_is_zero():
    assert ir.prompt_tokens({"choices": []}) == 0


def test_completion_text_openai_shape():
    resp = {"choices": [{"message": {"content": "@startuml\n@enduml"}}]}
    assert ir.completion_text(resp) == "@startuml\n@enduml"


def test_completion_text_openai_null_content():
    assert ir.completion_text({"choices": [{"message": {"content": None}}]}) == ""


def test_completion_text_gemini_shape():
    resp = {"candidates": [{"content": {"parts": [{"text": "@startuml\n"},
                                                  {"text": "@enduml"}]}}]}
    assert ir.completion_text(resp) == "@startuml\n@enduml"


def test_completion_text_gemini_skips_thought_parts():
    resp = {"candidates": [{"content": {"parts": [
        {"text": "internal plan", "thought": True}, {"text": "@startuml"}]}}]}
    assert ir.completion_text(resp) == "@startuml"


def test_completion_text_gemini_empty_candidate():
    # thinking can consume the whole maxOutputTokens -> candidate without parts
    assert ir.completion_text({"candidates": [{"finishReason": "MAX_TOKENS"}]}) == ""


def test_thoughts_tokens_gemini():
    resp = {"usageMetadata": {"promptTokenCount": 5, "thoughtsTokenCount": 712}}
    assert ir.thoughts_tokens(resp) == 712


def test_thoughts_tokens_none_for_chat_completions():
    assert ir.thoughts_tokens({"usage": {"prompt_tokens": 5}}) is None


def test_ingested_works_on_gemini_shape():
    assert ir.ingested({"usageMetadata": {"promptTokenCount": 1900}}, baseline=93)
    assert not ir.ingested({"usageMetadata": {"promptTokenCount": 93}}, baseline=93)


# --- resolve_api_key: provider-agnostic key lookup (--key-env) ---

def test_resolve_api_key_reads_named_env_var():
    assert ir.resolve_api_key("OPENAI_API_KEY",
                              {"OPENAI_API_KEY": "sk-test"}) == "sk-test"


def test_resolve_api_key_missing_aborts_with_var_name():
    with pytest.raises(SystemExit) as exc:
        ir.resolve_api_key("ANTHROPIC_API_KEY", {})
    assert "ANTHROPIC_API_KEY" in str(exc.value)


def test_resolve_api_key_empty_value_aborts():
    with pytest.raises(SystemExit):
        ir.resolve_api_key("GEMINI_API_KEY", {"GEMINI_API_KEY": ""})


# --- reasoning_leak: thinking content must never reach scoring silently ---

def test_reasoning_leak_detects_think_block():
    assert ir.reasoning_leak("<think>\nLet me look at the image\n</think>\n@startuml\n@enduml")


def test_reasoning_leak_case_insensitive():
    assert ir.reasoning_leak("<THINK>x</THINK>")


def test_reasoning_leak_false_on_clean_output():
    assert not ir.reasoning_leak("@startuml\nclass Thinker\nA -> B: rethink()\n@enduml")


# --- format_progress: operator-facing rolling status line (stdout only) ---

def test_format_progress_basic_no_eta():
    line = ir.format_progress(123, 1000, {"ok": 110, "timeout": 11, "skipped": 2})
    assert line == "[123/1000] ok=110 timeout=11 skipped=2"


def test_format_progress_renders_tally_in_insertion_order():
    # tally dict order is preserved (insertion order = order outcomes first seen)
    assert ir.format_progress(3, 10, {"timeout": 1, "ok": 2}) == "[3/10] timeout=1 ok=2"


def test_format_progress_empty_tally_has_no_trailing_space():
    assert ir.format_progress(1, 1000, {}) == "[1/1000]"


def test_format_progress_appends_eta_minutes():
    # rate 6s/cell over 100 done -> 900 remaining -> 5400s -> ~90m
    assert ir.format_progress(100, 1000, {"ok": 100}, elapsed=600.0) == "[100/1000] ok=100 ~90m"


def test_format_progress_eta_zero_at_completion():
    # last cell: no work remains -> ~0m (no division surprises)
    assert ir.format_progress(10, 10, {"ok": 10}, elapsed=120.0) == "[10/10] ok=10 ~0m"


def test_format_progress_no_eta_when_elapsed_omitted():
    assert ir.format_progress(5, 10, {"ok": 5}) == "[5/10] ok=5"
