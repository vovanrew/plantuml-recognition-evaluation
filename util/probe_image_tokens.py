#!/usr/bin/env python3
"""Probe a hosted endpoint's applied image pixel budget via returned token counts.

Black-box test for whether the provider downscales images below our 1568 px
standard (methodology §7). Sends a fixed text prompt with synthetic images of
increasing size and reads `usage.prompt_tokens`; the image-token count is the
difference from a text-only baseline.

For Qwen3.5 the expected relation is tokens ~= round32(W)*round32(H) / (32*32).
A LINEAR curve through 1568^2 means no compression at/below the standard; a
PLATEAU reveals the provider's max_pixels cap (the knee = its applied budget).

Usage (invoke from project root):
  FEATHERLESS_API_KEY=... python util/probe_image_tokens.py
  (override --base-url / --model for other OpenAI-compatible providers)
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import os
import ssl
import urllib.error
import urllib.request

from PIL import Image

# macOS python.org builds lack a system CA bundle; use certifi's if present.
try:
    import certifi
    _SSL_CTX = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL_CTX = ssl.create_default_context()


def data_url(px):
    """A px-by-px solid-gray PNG as a base64 data URL (exact pixel dims)."""
    buf = io.BytesIO()
    Image.new("RGB", (px, px), (128, 128, 128)).save(buf, "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"


def call(base_url, key, model, content):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 1,
    }).encode()
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            # Cloudflare (error 1010) blocks the default Python-urllib UA.
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0 Safari/537.36",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120, context=_SSL_CTX) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {e.code} {e.reason}\nresponse body:\n{detail}")


def round32(n):
    return max(32, round(n / 32) * 32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="https://api.featherless.ai/v1")
    ap.add_argument("--model", default="Qwen/Qwen3.5-2B")
    ap.add_argument("--sizes", default="512,1024,1568,2048,3000,4000")
    args = ap.parse_args()

    key = os.environ.get("FEATHERLESS_API_KEY")
    if not key:
        raise SystemExit("set FEATHERLESS_API_KEY")

    text = "Describe the image in one word."
    base = call(args.base_url, key, args.model, [{"type": "text", "text": text}])
    usage = base.get("usage")
    if not usage:
        print("NO usage field returned. Full response:")
        print(json.dumps(base, indent=2)[:2000])
        return
    baseline = usage["prompt_tokens"]
    print(f"model={args.model}")
    print(f"text-only baseline prompt_tokens = {baseline}\n")
    print(f"{'size':>10} {'MP':>6} {'prompt_tok':>11} {'image_tok':>10} {'expected':>9}")
    for px in (int(s) for s in args.sizes.split(",")):
        r = call(args.base_url, key, args.model,
                 [{"type": "text", "text": text},
                  {"type": "image_url", "image_url": {"url": data_url(px)}}])
        pt = r["usage"]["prompt_tokens"]
        img_tok = pt - baseline
        expected = round32(px) * round32(px) // (32 * 32)
        print(f"{px:>7}^2 {px*px/1e6:>6.2f} {pt:>11} {img_tok:>10} {expected:>9}")
    print("\nlinear & matching 'expected' through 1568^2 -> no compression at the "
          "standard.\nplateau below expected -> provider caps max_pixels at the knee.")


if __name__ == "__main__":
    main()
