# Evaluation Plan

How to run the zero-shot image→PlantUML benchmark end-to-end against a frozen
1000-key test set. Per-model pipeline first, then loop over the model list, then
aggregate.

Invoke every command from the project root. Paths in `--gt-dir`, `--test-set`,
`--csr` defaults are CWD-relative.

## 0. Prerequisites

All produced by the test-set construction pipeline; assumed already in place.

- `data/test_set.json` — 1000 keys frozen (the ordered list of `<key>.puml` filenames).
- `data/puml_files/<key>.puml` — 1000 ground-truth PlantUML sources.
- `data/puml_images/<key>.png` — 1000 full-resolution renders (built by `util/populate_test_set.py`).
- `data/puml_images_1568/<key>.png` — 1000 standardized 1568-px-long-edge inputs (built by `util/standardize_images.py`), the image fed to every model.
- `plantuml-1.2025.9.jar` — official renderer, at the project root (used by `evaluation/csr_runner.py`).
- `$PLANTUML_EXTRACTOR_JAR` — `DiagramStatsExtractor` fork JAR with the named-graph emitter (used by the structural runners). Build it from https://github.com/vovanrew/plantuml, branch `stats-extractor-graph` (not the default branch), with `./gradlew build -x test -x javaDoc`; the JAR lands at `build/libs/plantuml-1.2025.9.jar`. The runners also accept `--jar <path>`.

## 1. Per-model pipeline

One model run = `<run> = <model_id_sanitized>_<timestamp>`. Five sequential
steps; steps 3–5 are independent of each other once step 2 is done.

```
INFERENCE ──► CSR ──► ELEMENT F1
                 ├──► RELATIONSHIP F1
                 └──► chrF++
```

### 1.1 Inference

Call the model on all 1000 standardized images, store raw responses. The
prompt is read verbatim from `prompts/zero_shot.txt` (frozen; one shared
template for all models and both diagram types — see
`methodology/benchmark-protocol.md` §1). The per-model reasoning config
(methodology §3) is passed as `--extra-body '<json>'` and recorded in
`run_meta.json`; the runner counts any `<think>` block in a completion as a
`reasoning_leak` in the outcome tally — a non-zero count means thinking mode
is on and the run must not be scored. `--key-env` names the env var holding
the API key (default `FEATHERLESS_API_KEY`); `--provider gemini` switches the
request/response shape to native `generateContent` (see §3 for the per-model
flag table).

```bash
python evaluation/infer_runner.py \
  --model <id> --base-url <api> \
  --test-set data/test_set.json --images data/puml_images_1568 \
  --n 1000 --max-tokens 5376 --timeout 90 \
  --out data/runs
```

Output: `data/runs/<run>/<key>.puml` (raw text) + `<key>.json` (response metadata).

Only `--n` defaults to a smoke value (5); a real run is `--n 1000`, all other
defaults are run-ready (`--max-tokens 5376`, `--timeout 90` — sized to the
worst legitimate generation). The harness is hardened for
unattended batches: endpoint warmup before the batch, per-call image-ingestion
validation (`prompt_tokens` > text-only baseline) with bounded retry,
backoff-retry on transient HTTP (408/429/5xx) and network errors, and a stored
record for every cell — the raw response on success, else
`{"error": timeout|image_dropped|http_error|network_error, ...}` with no
`.puml`, so CSR scores the cell 0 while the cause stays on disk. `run_meta.json`
in the run dir pins model, prompt, and decoding params. A crashed or partially
failed run is resumed with `--run-dir data/runs/<run>`: stored successes are
final (never overwritten), failure records are re-attempted.

### 1.2 Compilation Success Rate (CSR)

Compile every raw output; score pass/fail; produce the block-isolated PlantUML
and rendered PNG reused by downstream steps.

```bash
python evaluation/csr_runner.py \
  --pred-dir data/runs/<run> \
  --test-set data/test_set.json \
  --out data/csr/<run>
```

Output: `data/csr/<run>/csr_results.json`, `extracted/<key>.puml`, `png/<key>.png`.

A missing prediction (e.g. inference timeout) counts as a failure when
`--test-set` is given, so CSR is over the full denominator.

### 1.3 Element F1

Node-level structural match (classes / participants) after normalization
(lowercase + trim; stereotype tokens `<<X>>` / `«X»` stripped from the name,
methodology §2.1). Multiset matching. Also computes type accuracy
(companion metric, methodology §3): share of name-matched pairs whose
extractor entity type agrees, container/internal GT types excluded from
the denominator.

```bash
python evaluation/element_f1_runner.py \
  --pred-dir data/csr/<run>/extracted \
  --test-set data/test_set.json \
  --csr      data/csr/<run>/csr_results.json \
  --out data/element_f1/<run>
```

Output: `element_f1_results.json` with `{summary: {zeros_for_failed, compiled_only, type_accuracy}, diagrams: [...]}` (per-diagram rows carry `type_accuracy: {matched, correct, excluded}`; the summary block adds the pooled accuracy and per-GT-type table).

### 1.4 Relationship F1

Edge-level structural match: key `(source, target, relation)` with endpoints
normalized, association undirected, label excluded. Reports overall + per
relation type (inheritance, composition, aggregation, dependency, association,
message).

```bash
python evaluation/relationship_f1_runner.py \
  --pred-dir data/csr/<run>/extracted \
  --test-set data/test_set.json \
  --csr      data/csr/<run>/csr_results.json \
  --out data/relationship_f1/<run>
```

Output: `relationship_f1_results.json`.

### 1.5 chrF++

Surface text fidelity sanity metric: sacrebleu `sentence_chrf` with
`char_order=6, word_order=2, beta=2`; raw 0–100 scale; macro = mean of
per-diagram scores, micro = `corpus_chrf` pooled. `--csr` is REQUIRED here:
chrF++ is parse-independent, so the compile gate must be supplied explicitly
for the `zeros_for_failed` population.

```bash
python evaluation/chrf_runner.py \
  --pred-dir data/runs/<run> \
  --test-set data/test_set.json \
  --csr      data/csr/<run>/csr_results.json \
  --out data/chrf/<run>
```

Output: `chrf_results.json`.

## 2. Ordering & dependency notes

- **CSR (1.2) must finish before Element F1, Relationship F1, and chrF++** —
  all three consume `csr_results.json` for the compile gate that defines the
  `zeros_for_failed` and `compiled_only` populations.
- **Steps 1.3, 1.4, 1.5 are independent** and can run in parallel.
- **`--pred-dir` choice**: the structural F1 runners point at
  `data/csr/<run>/extracted/` to reuse CSR's already-isolated PlantUML and skip
  a re-extraction pass; chrF++ points at the raw `data/runs/<run>/` because it
  does its own `extract_puml` on both sides. Either input works for any of the
  three (block isolation is idempotent) — the docstring convention reflects
  what saves the extractor JAR a pass.

## 3. Loop over all six models

Per-model wiring (endpoints settled 2026-06-12 against provider primary docs;
record in `methodology/benchmark-protocol.md` §2–§3). The runner speaks OpenAI
chat-completions by default; Claude goes through Anthropic's documented
OpenAI-compatibility endpoint (native `thinking` param passes through the
body); Gemini goes through the **native** `generateContent` API
(`--provider gemini`) because only the native `usageMetadata` carries the
`thoughtsTokenCount` that methodology §3 reports — its `--extra-body` merges
into `generationConfig`.

| Model | flags |
|---|---|
| `gpt-5.2-2025-12-11` | `--base-url https://api.openai.com/v1 --key-env OPENAI_API_KEY --token-field max_completion_tokens --extra-body '{"reasoning_effort": "none"}'` (GPT-5.x rejects `max_tokens`; it also returns HTTP 400 — not a truncated 200 — when output hits the cap, which surfaces as `http_error` cells) |
| `claude-opus-4-6` | `--base-url https://api.anthropic.com/v1 --key-env ANTHROPIC_API_KEY --extra-body '{"thinking": {"type": "disabled"}}'` (Anthropic flagship) |
| `gemini-3.1-pro-preview` | `--provider gemini --base-url https://generativelanguage.googleapis.com/v1beta --key-env GEMINI_API_KEY --extra-body '{"thinkingConfig": {"thinkingLevel": "low"}}'` (thinking not disableable on Pro tier; per-call `thoughtsTokenCount` preserved in the stored raw responses; `maxOutputTokens` covers thinking + answer jointly — size the run's `--max-tokens` from pilot-observed thinking volume on top of 5376) |
| Qwen3.5-2B / 9B / 27B | `--base-url https://api.featherless.ai/v1 --key-env FEATHERLESS_API_KEY --extra-body '{"chat_template_kwargs": {"enable_thinking": false}}'` (dense sizes; size `--timeout` from pilot throughput) |
| Qwen3.5-397B-A17B | `--base-url https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --extra-body '{"provider": {"only": ["alibaba"], "allow_fallbacks": false}, "reasoning": {"enabled": false}}'` (measured on first-party serving, reached through OpenRouter pinned to the Alibaba backend) |

```bash
# per model: 1.1 infer → data/runs/<run>; 1.2 CSR → data/csr/<run>;
# 1.3 Element F1, 1.4 Relationship F1, 1.5 chrF++ (parallel after CSR)
```

Gate before any 1k launch (per-family 10-sample pilot): `reasoning_leak: 0`
in the tally; for GPT-5.2, `usage.completion_tokens_details.reasoning_tokens
== 0`; for Gemini, `thoughtsTokenCount` present in stored raw responses;
ingestion validated on every call; observed per-call cost extrapolated to
1000 and checked against the <$150 total budget before frontier launches.

Per-model footprint: one inference dir under `data/runs/<run>/`, four metric
JSONs under `data/{csr,element_f1,relationship_f1,chrf}/<run>/`. Seven models =
28 metric JSONs total.

## 4. After all six models — analysis (Phase 3, not yet built)

The analysis stage covers what comes after the metric JSONs:

- Aggregate into a master `model × {metric, complexity tier, type}` results table.
- Paired bootstrap (n=1000) 95% CIs on the model-vs-model differences that matter.
- Plots: metric vs complexity tier per type; CSR comparison across models.
- Error analysis: 30–50 failure cases categorized (missed relations, wrong
  relation type, OCR/text drift, syntax breaks, refusals).
