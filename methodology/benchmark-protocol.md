# Benchmark Protocol

Methodological record for the zero-shot benchmark runs: the inference-side
protocol applied identically to every model. Metric definitions are recorded in
`evaluation-framework.md`; test-set construction in `test-set-construction.md`.

## Model set

The benchmark has two groups of models, and both run under the same protocol below.

- **Hosted reference models.** Three are each lab's general-purpose flagship as
  of 2026-02-28, one per lab: `gpt-5.2-2025-12-11` (OpenAI), `claude-opus-4-6`
  (Anthropic) and `gemini-3.1-pro-preview` (Google). The fourth is
  Qwen3.5-397B-A17B, a mixture-of-experts model with 397B total and about 17B
  active parameters. All four are reached through provider APIs (§2).
- **Self-served open models.** These are the dense Qwen3.5 sizes 2B, 9B and 27B.
  They run on one GPU in their released bf16 weights, through a local
  OpenAI-compatible server (§2). They are also the zero-shot baseline of a
  separate fine-tuning study.

The three flagship models are reference points, not matched competitors.

## 1. Prompt

Every model receives a single zero-shot prompt, identical across models and
diagram types, frozen verbatim at `prompts/zero_shot.txt` and read from that
file by the inference harness:

> This image is a UML diagram. Reproduce it as valid PlantUML code that, when
> rendered, matches the diagram as closely as possible: capture every element
> with the UML notation shown (e.g. actor, interface, database), its contents
> and labels, and every relationship. Output only the PlantUML code starting
> with @startuml and ending with @enduml, with no explanation.

The prompt identifies the input only as "a UML diagram", without naming the
diagram type, so recognizing the diagram kind is part of the measured task.
Its instruction enumerates the dimensions the evaluation scores: element
recovery with the rendered UML notation preserved (Element F1 and its
type-accuracy companion), element contents and labels (chrF++), and
relationship recovery (Relationship F1). The output constraint — a bare
PlantUML block from `@startuml` to `@enduml` with no surrounding explanation —
matches the block-isolation step applied to every prediction before scoring.
The prompt contains no PlantUML syntax guidance, no examples, and no
model-specific phrasing.

The frozen text is pinned by `tests/test_prompt.py`, which asserts the file
content verbatim together with the properties above (single line, no diagram-
type hint, output-block constraint); any re-freeze updates the file, the test,
and this record together.

## 2. Inference protocol

Inference runs through `evaluation/infer_runner.py` (greedy decoding,
temperature 0; `max_tokens` 5376 per methodology §1 of the evaluation
framework; a per-call hard wall-clock deadline). The deadline is 90 s for the
three flagship runs. It is 600 s for the Qwen3.5-397B-A17B run and for the three
self-served runs. Each run stores one record per
test-set cell and a `run_meta.json` pinning the model identifier, endpoint,
prompt text, and decoding parameters.

Each provider is reached through the endpoint that carries its frozen
reasoning configuration (§3) and the usage fields the harness validates
(endpoint documentation verified against provider primary sources
2026-06-12):

- **OpenAI (`gpt-5.2-2025-12-11`)**: the native OpenAI chat-completions shape
  (`https://api.openai.com/v1`). GPT-5.2 takes the output cap as
  `max_completion_tokens` (`max_tokens` is rejected for this model;
  `--token-field`, recorded in `run_meta.json`). When generation reaches the
  cap, the endpoint returns HTTP 400 and no completion. Such a generation is
  therefore stored as an `http_error` failure record.
- **Qwen3.5-397B-A17B**: the same OpenAI-compatible shape, reached through
  OpenRouter (`https://openrouter.ai/api/v1`). The request pins the provider
  `alibaba` and disables fallbacks (`provider: {"only": ["alibaba"],
  "allow_fallbacks": false}`, recorded in `run_meta.json`). The run started on
  2026-06-28.
- **Anthropic (`claude-opus-4-6`)**: Anthropic's OpenAI-compatible
  endpoint (`https://api.anthropic.com/v1/chat/completions`), which
  documents passthrough of the native `thinking` request parameter and
  returns `usage.prompt_tokens`/`completion_tokens` and `image_url` content
  (the fields the ingestion check and the shared request shape require).
- **Google (`gemini-3.1-pro-preview`)**: the native REST endpoint
  (`https://generativelanguage.googleapis.com/v1beta/models/<id>:generateContent`,
  key in the `x-goog-api-key` header). The native endpoint is used because
  the per-call `thoughtsTokenCount` reported per §3 is carried only in the
  native `usageMetadata`. The harness
  (`--provider gemini`) maps the shared prompt + image content into native
  `contents`/`parts` (`inline_data` with the identical standardized PNG),
  maps temperature 0 and the token cap to `generationConfig.temperature` /
  `maxOutputTokens`, and merges the reasoning configuration into
  `generationConfig` as `{"thinkingConfig": {"thinkingLevel": "low"}}`.
  Ingestion validation reads `usageMetadata.promptTokenCount`; prediction
  text is the concatenation of non-thought candidate parts (thought
  summaries are absent without `includeThoughts`). On this endpoint
  `maxOutputTokens` covers thinking and answer tokens together. The Gemini
  run sets it to 5376, the same cap as the other runs.
- **Self-served Qwen3.5 (2B, 9B, 27B)**: the same OpenAI chat-completions
  shape, sent to a local OpenAI-compatible server (`http://127.0.0.1:8000/v1`).
  The server is a thin layer over Hugging Face transformers 5.18.0 on torch
  2.14.1. It serves each model in its released bf16 weights, with no
  quantization, on one NVIDIA RTX PRO 6000 Blackwell Server Edition GPU
  (96 GB). Each model is pinned to a fixed commit of its weights, and every
  response records the commit, the precision and the GPU. The runs use the
  same prompt, the same 1,568 px images, greedy decoding at temperature 0 and
  `max_tokens` 5376 as the hosted runs, with the 600 s deadline. All three
  sizes take in the 1,568 px images without downscaling. Their stored prompt
  token counts match the expected image token count,
  `round32(W)·round32(H)/32²`, within 3 tokens. The runs started on
  2026-10-26 (2B) and on 2026-10-27 (9B and 27B).

Image ingestion is validated on every call: the response's `prompt_tokens`
must exceed a text-only baseline measured at run start, since a hosted
endpoint can accept an image-bearing request yet silently drop the image and
answer from the text alone. Before the
batch, throwaway image-bearing calls warm the endpoint until ingestion is
confirmed; the run aborts if it never is. During the batch, a call whose
image is dropped is retried a bounded number of times; a persistent drop is
recorded as an `image_dropped` failure and its blind completion is excluded
from scoring.

Transient transport failures (HTTP 408, 429, and 5xx; network-level errors)
are retried with exponential backoff. A call that exceeds the hard deadline is
recorded as a `timeout` failure without retry, because observed timeout causes
(no-EOS repetition spirals) reproduce deterministically. Every failed cell —
`timeout`, `image_dropped`, `http_error`, `network_error`, or `bad_response` — yields a stored
failure record and no prediction file, so Compilation Success Rate scores the
cell as a failure while the cause remains on disk for error analysis. Stored
successful responses are immutable: re-invoking a run directory skips them and
re-attempts only recorded failures. The three self-served runs have no failure
records: each answers all 1,000 cells.

## 3. Reasoning configuration

Every model runs at its minimum available reasoning configuration, fixed per
model from provider documentation (verified 2026-06-11) and recorded in each
run's `run_meta.json`:

| Model | Setting | Reasoning state |
|---|---|---|
| `gpt-5.2-2025-12-11` | `reasoning_effort: "none"` | off (also the model default; "does not perform reasoning") |
| `claude-opus-4-6` | `thinking: {"type": "disabled"}` | off |
| `gemini-3.1-pro-preview` | `thinking_level: "low"` | minimum available — thinking cannot be disabled on the Pro tier (`minimal` is unsupported there); `low` is the floor, below the dynamic `high` default |
| Qwen3.5-2B / 9B / 27B | `chat_template_kwargs: {"enable_thinking": false}` | off |
| Qwen3.5-397B-A17B | `reasoning: {"enabled": false}` | off |

Qwen3.5 is a hybrid thinking family whose default differs by size: 2B
defaults to non-thinking while 9B, 27B, and the 397B-A17B mixture-of-experts
default to thinking, so non-thinking is requested explicitly for every size.
The dense sizes take the official model-card form `chat_template_kwargs:
{"enable_thinking": false}` (a no-op on 2B, whose chat template enables
thinking only on an explicit `true`); the 397B-A17B, reached through
OpenRouter (§2), takes the equivalent top-level `reasoning:
{"enabled": false}`. Across all runs the stored completions carry no reasoning
content — the `reasoning_leak` tally is 0 for every model.

The Gemini setting is an asymmetry of the comparison, and it is measured:
thinking tokens generated at `thinking_level: "low"` are billed and
reported by the API in the per-response `thoughtsTokenCount` field, which is
preserved in the stored raw responses; the benchmark reports the measured
residual thinking-token volume alongside the results. The API omits the
field when the count is zero (`usageMetadata` totals confirm
`promptTokenCount + candidatesTokenCount = totalTokenCount` in such
responses), so an absent field is read as zero; the 10-sample pilot
(2026-06-12) observed zero thinking tokens on all ten calls. As of 2026-06-11
Gemini 3.1 Pro exists only as the preview id `gemini-3.1-pro-preview` with no
dated snapshot, so the literal id and the run date are recorded together.

The harness passes the per-model configuration verbatim into every request
body (`--extra-body`, stored in `run_meta.json`) and checks each completion
for inline reasoning content: a `<think>` block in a stored completion is
counted and reported as a `reasoning_leak` in the run tally, because block
isolation would otherwise strip leaked reasoning before scoring and a
wrongly-enabled thinking mode would be invisible downstream. The per-family
pilot run (10 samples) must show zero leaked completions and, for GPT-5.2,
zero `reasoning_tokens` in the reported usage before a full run is launched.
