# Run-level aggregator — zero-shot image→PlantUML benchmark

**Models included: 7/7** (panel: main).

## Token totals (all 1000 cells incl. failures)

Output already includes reasoning (no double count); Gemini output = candidates + thoughts. No dollar pricing (out of scope).

| Model | cells | input | output | reasoning | total |
|---|--:|--:|--:|--:|--:|
| GPT-5.2 | 1000 | 1.631M | 0.331M | 0.000M | 1.962M |
| Claude Opus 4.6 | 1000 | 1.415M | 0.339M | 0.000M | 1.754M |
| Gemini 3.1 Pro | 1000 | 1.165M | 0.297M | 0.000M | 1.462M |
| Qwen3.5-2B | 1000 | 1.387M | 2.078M | 0.000M | 3.465M |
| Qwen3.5-9B | 1000 | 1.387M | 1.204M | 0.000M | 2.591M |
| Qwen3.5-27B | 1000 | 1.387M | 0.783M | 0.000M | 2.170M |
| Qwen3.5-397B-A17B | 1000 | 1.386M | 0.679M | 0.000M | 2.066M |

## Failure / outcome inventory

Provider/harness failure (source B) vs model compile-fail (source A CSR). `no_response` reconciles with source-A `has_pred==false`.

| Model | compiled | compile-fail | no-response | timeout | image_dropped | http_error | network_error | reconcile |
|---|--:|--:|--:|--:|--:|--:|--:|:--:|
| GPT-5.2 | 935 | 64 | 1 | 1 | 0 | 0 | 0 | ✓ |
| Claude Opus 4.6 | 941 | 59 | 0 | 0 | 0 | 0 | 0 | ✓ |
| Gemini 3.1 Pro | 972 | 28 | 0 | 0 | 0 | 0 | 0 | ✓ |
| Qwen3.5-2B | 191 | 809 | 0 | 0 | 0 | 0 | 0 | ✓ |
| Qwen3.5-9B | 411 | 589 | 0 | 0 | 0 | 0 | 0 | ✓ |
| Qwen3.5-27B | 644 | 356 | 0 | 0 | 0 | 0 | 0 | ✓ |
| Qwen3.5-397B-A17B | 787 | 213 | 0 | 0 | 0 | 0 | 0 | ✓ |

## Provenance manifest

| Model | snapshot | provider | base_url | reasoning config | max_tokens | temp | started | leak |
|---|---|---|---|---|--:|--:|---|--:|
| GPT-5.2 | `gpt-5.2-2025-12-11` | openai | https://api.openai.com/v1 | `{"reasoning_effort": "none"}` | 5376 | 0 | 20260613T154248Z | 0 |
| Claude Opus 4.6 | `claude-opus-4-6` | openai | https://api.anthropic.com/v1 | `{"thinking": {"type": "disabled"}}` | 5376 | 0 | 20260614T081502Z | 0 |
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | gemini | https://generativelanguage.googleapis.com/v1beta | `{"thinkingConfig": {"thinkingLevel": "low"}}` | 5376 | 0 | 20260617T081808Z | 0 |
| Qwen3.5-2B | `Qwen/Qwen3.5-2B` | openai | http://127.0.0.1:8000/v1 | `{"chat_template_kwargs": {"enable_thinking": false}}` | 5376 | 0 | 20261026T170812Z | 0 |
| Qwen3.5-9B | `Qwen/Qwen3.5-9B` | openai | http://127.0.0.1:8000/v1 | `{"chat_template_kwargs": {"enable_thinking": false}}` | 5376 | 0 | 20261027T051557Z | 0 |
| Qwen3.5-27B | `Qwen/Qwen3.5-27B` | openai | http://127.0.0.1:8000/v1 | `{"chat_template_kwargs": {"enable_thinking": false}}` | 5376 | 0 | 20261027T190103Z | 0 |
| Qwen3.5-397B-A17B | `qwen/qwen3.5-397b-a17b` | openai | https://openrouter.ai/api/v1 | `{"provider": {"only": ["alibaba"], "allow_fallbacks": false}, "reasoning": {"enabled": false}}` | 5376 | 0 | 20260628T171705Z | 0 |

## Per-tier crowding descriptor (model-independent)

content_lines per megapixel after 1568px resize (pooled total/total); from the real `data/puml_images_1568/` PNG dimensions (1000 diagrams). Machine artifact: `crowding.json` (Task-3 `crowding=` hook).

| Tier | n | content_lines | MP | lines/MP |
|---|--:|--:|--:|--:|
| 1 | 250 | 1864 | 213.15 | 8.74 |
| 2 | 250 | 4268 | 322.15 | 13.25 |
| 3 | 250 | 8331 | 394.50 | 21.12 |
| 4 | 250 | 19668 | 392.64 | 50.09 |

