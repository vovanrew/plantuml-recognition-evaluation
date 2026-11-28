# Evaluation Plan

How to run the zero-shot image-to-PlantUML benchmark from start to end on the
1,000-diagram test set. Section 1 is the pipeline for one model. Section 3 gives
the command that ran each of the seven panel models. Section 4 builds the tables,
figures and checks of the paper.

Run every command from the repository root. The default paths of `--gt-dir`,
`--test-set` and `--images` are relative to the current folder.

## 0. Prerequisites

The test-set construction pipeline produces these files
(`methodology/test-set-construction.md`).

- `data/test_set.json`: the 1,000 test keys, one record per diagram.
- `data/puml_files/<key>.puml`: the 1,000 ground-truth PlantUML sources.
- `data/puml_images/<key>.png`: the 1,000 full-resolution renders (`util/populate_test_set.py`).
- `data/puml_images_1568/<key>.png`: the 1,000 images scaled to a 1,568 px long
  edge (`util/standardize_images.py`). Every model receives these images.
- `plantuml-1.2025.9.jar` in the root: the official renderer, used by
  `evaluation/csr_runner.py`.
- `plantuml-stats-extractor-v2.jar` in the root: the `DiagramStatsExtractor` JAR
  that the structural scorers use. Its SHA-256 is in the README table
  ("The structural extractor"). Use this file, not a build of your own.

The structural scorers read the extractor path from `PLANTUML_EXTRACTOR_JAR`, or
from `--jar`. Set it once per shell:

```bash
export PLANTUML_EXTRACTOR_JAR=$PWD/plantuml-stats-extractor-v2.jar
```

## 1. Per-model pipeline

One model run is stored in `data/runs/<run>/`. The runner names a new run
`<model id with / replaced by _>_<UTC timestamp>`. A run has five steps. Steps
1.3 to 1.5 are independent of each other once step 1.2 is done.

```
INFERENCE ──► CSR ──► ELEMENT F1
                 ├──► RELATIONSHIP F1
                 └──► chrF++
```

### 1.1 Inference

The runner sends all 1,000 standardized images to the model and stores the raw
responses. It reads the prompt from `prompts/zero_shot.txt`, which is the same for
every model and both diagram types (`methodology/benchmark-protocol.md` §1). The
endpoints are described in §2 of that file, and the reasoning settings in §3.
The reasoning setting of a model goes into `--extra-body '<json>'`, and the runner
records it in `run_meta.json`.

```bash
python3 evaluation/infer_runner.py \
  --model <id> --base-url <api> --key-env <ENV_VAR_WITH_KEY> \
  --test-set data/test_set.json --images data/puml_images_1568 \
  --n 1000 --max-tokens 5376 --timeout <seconds> \
  --extra-body '<reasoning json>' \
  --out data/runs
```

Output: `data/runs/<run>/<key>.puml` (the raw text) and `<key>.json` (the
response and its metadata), with `run_meta.json`. The section 3 commands give
`--base-url`, `--key-env`, `--timeout` and `--extra-body` for each model. Always
set `--n 1000`, because the default runs only 5 diagrams. `--base-url`,
`--model` and `--key-env` have no default and must be given.

The runner checks every call. Before the batch it warms the endpoint until an
image is taken in. On each call it checks that `prompt_tokens` is above the
text-only baseline, and it retries a dropped image a few times. It retries
HTTP 408, 429 and 5xx errors and network errors with backoff. Every cell gets a
stored record: the raw response on success, or a failure record with no `.puml`.
A failure record names its cause: `timeout`, `image_dropped`, `http_error`,
`network_error` or `bad_response`. CSR then scores that cell 0, and the cause
stays on disk.

The runner also counts every completion that holds a `<think>` block as a
`reasoning_leak`. A count above zero means thinking mode is on, and the run must
not be scored (`methodology/benchmark-protocol.md` §3).

To resume a run that stopped or has failed cells, add `--run-dir data/runs/<run>`.
Stored successes are final and are never overwritten. Failure records are tried
again.

### 1.2 Compilation Success Rate (CSR)

This step compiles every raw output and scores it pass or fail. It also writes
the isolated PlantUML block and the rendered PNG, which later steps reuse.

```bash
python3 evaluation/csr_runner.py \
  --pred-dir data/runs/<run> \
  --test-set data/test_set.json \
  --out data/csr/<run>
```

Output: `data/csr/<run>/csr_results.json`, `extracted/<key>.puml`,
`render_src/<key>.puml` (the copy that is rendered, without a diagram name) and
`png/<key>.png`. With `--test-set`, a missing prediction counts as a failure, so
CSR is computed over all 1,000 keys.

### 1.3 Element F1

Element F1 matches the nodes of the two graphs by display name. The names are
normalized as in `methodology/evaluation-framework.md` §2.1, and the metric is
defined in §3. Only the first diagram of an answer is scored (§2.4). The runner
also reports type accuracy, the companion metric of §3.

```bash
python3 evaluation/element_f1_runner.py \
  --pred-dir data/csr/<run>/extracted \
  --test-set data/test_set.json \
  --csr      data/csr/<run>/csr_results.json \
  --out data_v2/element_f1/<run>
```

Output: `element_f1_results.json`. Its `summary` holds the `zeros_for_failed`
and `compiled_only` populations and `type_accuracy`. Each row of `diagrams`
holds the scores of one diagram.

### 1.4 Relationship F1

Relationship F1 matches the edges of the two graphs by source, target and
relation type. The label is not part of the key. Association direction comes
from the arrowheads, as `methodology/evaluation-framework.md` §4 describes. The
edges are defined in §2.2. The runner reports the overall score and one score
per relation type.

```bash
python3 evaluation/relationship_f1_runner.py \
  --pred-dir data/csr/<run>/extracted \
  --test-set data/test_set.json \
  --csr      data/csr/<run>/csr_results.json \
  --out data_v2/relationship_f1/<run>
```

Output: `relationship_f1_results.json`.

### 1.5 chrF++

chrF++ measures how close the predicted text is to the ground-truth text
(`methodology/evaluation-framework.md` §5). `--csr` is required here. chrF++ does
not parse the code, so it needs the CSR file to know which answers compiled.

```bash
python3 evaluation/chrf_runner.py \
  --pred-dir data/runs/<run> \
  --test-set data/test_set.json \
  --csr      data/csr/<run>/csr_results.json \
  --out data/chrf/<run>
```

Output: `chrf_results.json`.

## 2. Order of the steps

- **CSR (1.2) must finish first.** Element F1, Relationship F1 and chrF++ all read
  `csr_results.json`. It decides which answers belong to the `zeros_for_failed`
  and `compiled_only` populations.
- **Steps 1.3, 1.4 and 1.5 are independent** and can run in parallel.
- **The `--pred-dir` choice.** The structural runners read
  `data/csr/<run>/extracted/`, so they reuse the blocks that CSR has already
  isolated. chrF++ reads the raw `data/runs/<run>/`, because it isolates the block
  itself on both sides. Isolating a block twice gives the same block, so either
  input works for all three runners.
- **Output folders.** CSR and chrF++ write under `data/`, and the structural
  runners write under `data_v2/`. `util/build_paper_root.py` reads the result
  files from these folders (section 4).

## 3. The seven panel models

The panel is listed in `analysis/model_registry_paper.json`. Each command below
is the section 1.1 command with these flags. All runs use temperature 0 and
`--max-tokens 5376`. The flags match the `run_meta.json` of each stored run.

### 3.1 Hosted reference models

The four hosted models are reached through provider APIs
(`methodology/benchmark-protocol.md` §2).

| Model | Flags |
|---|---|
| GPT-5.2 | `--model gpt-5.2-2025-12-11 --base-url https://api.openai.com/v1 --key-env OPENAI_API_KEY --token-field max_completion_tokens --timeout 90 --extra-body '{"reasoning_effort": "none"}'` |
| Claude Opus 4.6 | `--model claude-opus-4-6 --base-url https://api.anthropic.com/v1 --key-env ANTHROPIC_API_KEY --timeout 90 --extra-body '{"thinking": {"type": "disabled"}}'` |
| Gemini 3.1 Pro | `--model gemini-3.1-pro-preview --provider gemini --base-url https://generativelanguage.googleapis.com/v1beta --key-env GEMINI_API_KEY --timeout 90 --extra-body '{"thinkingConfig": {"thinkingLevel": "low"}}'` |
| Qwen3.5-397B-A17B | `--model qwen/qwen3.5-397b-a17b --base-url https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --timeout 600 --extra-body '{"provider": {"only": ["alibaba"], "allow_fallbacks": false}, "reasoning": {"enabled": false}}'` |

Notes on these flags:

- GPT-5.2 takes the output cap as `max_completion_tokens`. When the output
  reaches the cap, the API returns HTTP 400, which is stored as an `http_error`
  cell (`methodology/benchmark-protocol.md` §2).
- Gemini uses the native `generateContent` API (`--provider gemini`), because only
  that API reports `thoughtsTokenCount`. On this API `--extra-body` goes into
  `generationConfig`, and the cap of 5376 covers thinking and answer together.
- The Qwen3.5-397B-A17B request pins OpenRouter to the Alibaba backend, with no
  fallback.

### 3.2 Self-served Qwen3.5 models

The dense Qwen3.5-2B, 9B and 27B run on one GPU in their released bf16 weights.
A local OpenAI-compatible server answers at `http://127.0.0.1:8000/v1`
(`methodology/benchmark-protocol.md` §2). The server is `infer/server.py` of the
fine-tuning study. It is started with `--model Qwen/Qwen3.5-<size> --revision
<commit> --port 8000`. The commit of each model is recorded in the run's
`answer_manifest.json`.

The runner needs a key variable, but the local server does not check it.

```bash
LOCAL_KEY=local python3 evaluation/infer_runner.py \
  --model Qwen/Qwen3.5-2B --base-url http://127.0.0.1:8000/v1 --key-env LOCAL_KEY \
  --test-set data/test_set.json --images data/puml_images_1568 \
  --n 1000 --max-tokens 5376 --timeout 600 \
  --extra-body '{"chat_template_kwargs": {"enable_thinking": false}}'
```

For the other two sizes, change `--model` to `Qwen/Qwen3.5-9B` or
`Qwen/Qwen3.5-27B`. The three stored runs, with their answers, scores and logs,
are in `data_selfserved.zip`. Unzipping it at the root creates
`data_selfserved/runs/test/<size>_zero_shot/`.

### 3.3 Before a full run

Each model family first runs a 10-sample pilot (`--n 10`). A full run starts only
when the pilot shows `reasoning_leak` 0 in the tally, and, for GPT-5.2, zero
`usage.completion_tokens_details.reasoning_tokens` in every response
(`methodology/benchmark-protocol.md` §3).

Each model then has one run folder under `data/runs/` and four result files, one
in each metric folder. The seven models give 28 result files.

## 4. Analysis

The analysis reads the stored result files and the raw responses. It does not
call a model or score a diagram again (`methodology/analysis-protocol.md`). All
outputs go to `analysis/out_paper/`.

First, unpack the release archives and assemble the data root `data_paper/`:

```bash
unzip data.zip && unzip data_v2.zip && unzip data_selfserved.zip
python3 util/build_paper_root.py --fine-tune data_selfserved     # -> data_paper/
```

Then build the tables, intervals and figures:

```bash
R="--data-root data_paper --registry analysis/model_registry_paper.json --out-dir analysis/out_paper"
python3 analysis/build_master_table.py $R     # master_table.*
python3 analysis/build_ci_table.py $R         # ci_table.*, paired intervals (§5)
python3 analysis/build_run_level.py $R        # run_level.*, crowding.* (§8, §9)
python3 -m analysis.build_paper_extras $R     # paper_extras.*, stratum intervals (§3)
python3 analysis/build_failure_index.py $R    # failure_index.*, outcome classes (§7)
python3 analysis/build_plots.py --registry analysis/model_registry_paper.json \
  --out-dir analysis/out_paper --by-arm       # plots/
python3 analysis/build_exhibits.py --out-dir analysis/out_paper   # exhibits.*
```

The section numbers in the comments are those of `methodology/analysis-protocol.md`.
`build_exhibits.py` reads the outputs of the earlier steps, so it runs last.

The error-analysis sample (§7) is drawn and then reported after two coders have
coded it:

```bash
python3 -m analysis.build_error_sample draw --data-root data_paper \
  --registry analysis/model_registry_paper.json --out analysis/out_paper/error_sample
python3 -m analysis.build_error_sample report --out analysis/out_paper/error_sample
```

The human-rater check (§11) has four steps. `draw` picks the 60 pairs and leaves
out the diagrams listed in the `--exclude` keys file. `render` draws the answers
with the render pipeline of the fine-tuning study. `sheets` builds the rating
pages. `report` reads the two raters' files from `ratings/`.

```bash
python3 -m analysis.rater_check draw --data-root data_paper \
  --registry analysis/model_registry_paper.json --exclude <keys file>
python3 -m analysis.rater_check render --data-root data_paper --render-py ../fine-tune/build/render.py
python3 -m analysis.rater_check sheets --data-root data_paper
python3 -m analysis.rater_check report
```

Its outputs go to `analysis/out_paper/rater_check/`.
