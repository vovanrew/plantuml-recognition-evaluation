# Zero-shot image-to-PlantUML: evaluation framework and benchmark

Can a multimodal language model look at a picture of a UML diagram and write back
the PlantUML source that produced it?

This repository holds the benchmark that answers that question and the
evaluation framework it is scored with. It also holds every file needed to
reproduce the results: 1,000 diagrams, 7 model runs, all raw answers, all
computed metrics, and the tables, figures and exhibits.

The task is **zero-shot**: each model sees one rendered diagram image and one
frozen prompt, and must write PlantUML source. There are no examples, no
fine-tuning and no hint about the diagram type. The scope is **class and
sequence diagrams**.

## What makes this benchmark different

A rendered UML diagram is a typed graph. Text-similarity scores treat its source
as a string, and manual error counts do not scale past a few dozen cases. This
framework scores the answer at several levels at once, structural as well as
surface. It reports each structural metric over **two populations**.

The second point is the methodological core. A model that fails to compile its
answer on hard diagrams looks strong if you score only the diagrams it compiled.
Reporting the compiled-only number beside the full-set number makes this
selective-failure bias visible. On this benchmark the effect is large: Qwen3.5-2B
scores 0.874 Element F1 on the diagrams it compiles, but 0.239 across all 1,000.

## Metrics

| Metric | What it measures |
|---|---|
| **CSR** (Compilation Success Rate) | The answer renders to a non-empty image. An answer that parses but renders nothing is a failure, and so is a missing answer. Precondition for everything else. |
| **Element F1** | Recovery of named entities (classes, interfaces, enums, participants, actors). Matched on the normalized display name only. |
| **Relationship F1** | Recovery of typed edges as `(source, target, relation_type)` over inheritance, composition, aggregation, dependency, association and message. Reported overall and per relation type. |
| **Type accuracy** | Among name-matched entities, the share with the correct UML type. Companion to Element F1. |
| **chrF++** | Character and word n-gram surface similarity. It covers what the structural metrics ignore: member signatures, multiplicities, message wording, control-flow framing, notes. |

The structural metrics and chrF++ are each reported two ways. **Full-set** covers
all 1,000 diagrams, and an answer that does not compile scores 0.
**Compiled-only** covers the compiled answers, with CSR reported beside it.
Uncertainty is a paired bootstrap over diagrams, with 1,000 resamples and a fixed
seed.

The full definitions, with the edge cases, are in
[`methodology/evaluation-framework.md`](methodology/evaluation-framework.md).

## Headline results

Point estimates. Structural columns and chrF++ are `full-set / compiled-only`.
The 95% intervals for every cell are in
[`analysis/out_paper/exhibits.md`](analysis/out_paper/exhibits.md), Exhibit 1.

The panel has **two groups, not one leaderboard**, and it is listed in
[`analysis/model_registry_paper.json`](analysis/model_registry_paper.json).

**Hosted reference models**, each on its provider's serving. Qwen3.5-397B-A17B
is reached through OpenRouter, pinned to the provider Alibaba.

| Model | CSR | Element F1 | Relationship F1 | chrF++ macro | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.916 / 0.958 | 0.770 / 0.812 | 62.73 / 67.09 | 0.941 |
| Claude Opus 4.6 | 94.1% | 0.934 / 0.966 | 0.700 / 0.728 | 65.68 / 69.80 | 0.951 |
| Gemini 3.1 Pro | 97.2% | 0.967 / 0.983 | 0.894 / 0.912 | 75.53 / 77.70 | 0.984 |
| Qwen3.5-397B-A17B | 78.7% | 0.794 / 0.924 | 0.657 / 0.746 | 49.23 / 62.56 | 0.871 |

**Self-served open models**, the dense Qwen3.5 sizes. They run on one GPU in
their released bf16 weights, through a local OpenAI-compatible server.

| Model | Params | CSR | Element F1 | Relationship F1 | chrF++ macro | Type acc |
|---|---|---|---|---|---|---|
| Qwen3.5-2B | 2B | 19.1% | 0.239 / 0.874 | 0.110 / 0.463 | 11.82 / 61.90 | 0.755 |
| Qwen3.5-9B | 9B | 41.1% | 0.481 / 0.871 | 0.198 / 0.470 | 25.83 / 62.86 | 0.774 |
| Qwen3.5-27B | 27B | 64.4% | 0.713 / 0.945 | 0.507 / 0.729 | 43.87 / 68.12 | 0.889 |

Statements about model size use the three dense models only.
Qwen3.5-397B-A17B is a mixture-of-experts model, so it is not placed on the size
axis. Read the two populations together. Across the dense models, CSR rises from
19.1% to 64.4%, while compiled-only Element F1 stays between 0.871 and 0.945.
Most of what size buys on this task is the ability to write compilable output at
all.

[`analysis/error_analysis.md`](analysis/error_analysis.md) reviews 108 sampled
failure cases, coded with the codebook in
[`analysis/error_codebook.md`](analysis/error_codebook.md).

### Human-rater check

Two raters compared the answers of two models on the same test diagram, 60 pairs
in four comparisons. They did not know which model wrote which answer. On the
pairs where the metric differs, the raters chose the answer with the higher
Relationship F1 in 40 of 53 and 38 of 51 picks. They chose the answer with the
higher Element F1 in 18 of 28 and 17 of 27 picks. The two raters gave the same
answer on 56 of 60 pairs (Cohen's kappa 0.877). The report is
[`analysis/out_paper/rater_check/report.md`](analysis/out_paper/rater_check/report.md),
and the method is in
[`methodology/analysis-protocol.md`](methodology/analysis-protocol.md) §11.

## The test set

1,000 diagrams: 2 types (class, sequence) x 4 complexity tiers x 125.

The diagrams come from the *UML-in-the-Wild* corpus, 143,427 PlantUML/PNG pairs
mined from open-source repositories via **World of Code**. The selection is
repository-disjoint and deduplicated on normalized source. It is filtered so that
the corpus type label agrees with the PlantUML parser's own reading of the file.
Complexity tiers are quartiles of `content_lines`, computed per diagram type.
Sampling uses a fixed seed (42), with at most 5 diagrams per source repository.

Every model receives the same input image, scaled down to a **1,568 px long
edge**. That is the lowest native processing resolution in the model panel, so
it is the highest resolution every model can be given on equal terms.

The construction pipeline, with counts at every filter stage, is in
[`methodology/test-set-construction.md`](methodology/test-set-construction.md).
The inference protocol, with the serving of each model, is in
[`methodology/benchmark-protocol.md`](methodology/benchmark-protocol.md).

## Repository layout

```
analysis/          Aggregation, bootstrap intervals, plots, exhibits. See analysis/README.md.
  out_paper/       The results: tables, intervals, run level, failure index, stratum
                   intervals (paper_extras.*), figures (plots/), exhibits.
    error_sample/  The 108 coded failure cases.
    rater_check/   The human-rater check: pairs (keys.json), ratings, report.
  model_registry_paper.json  The 7 models of the panel and their run directories.
  error_analysis.md     Review of the 108 coded failure cases.
  error_codebook.md     The codebook the cases were coded with.
  rater_check.py        The human-rater check: draw, render, rating pages, report.
  out/             Outputs of the default registry (model_registry.json), not the results above.
evaluation/        Inference runner and the four metric scorers.
util/              Test-set construction, image standardization, archive packing.
methodology/       The methodological record. The source of truth for every design decision.
prompts/           The frozen zero-shot prompt.
tests/             413 test functions across 27 modules.
data.zip           Test set, ground truth and the hosted runs. Unzip at the repository root.
data_v2.zip        Structural result files of the hosted runs. Unzip at the repository root.
data_selfserved.zip
                   The self-served Qwen3.5-2B, 9B and 27B runs. Unzip at the repository root.
plantuml-stats-extractor-v1.jar, -v2.jar
                   The extractor JARs (GPL-3.0). See "The structural extractor".
evaluation_plan.md How to run the benchmark end to end.
FUTURE.md          Scoped extensions that were deliberately deferred.
```

## Requirements

- **Python 3.9 or newer** (the scorers were run under 3.9.6). `python3 -m pip install -r requirements.txt`
- **A Java runtime**, for the PlantUML renderer. The reported runs used
  Temurin JDK 26.0.1.
- **PlantUML `1.2025.9`**, as `plantuml-1.2025.9.jar` in the repository root.
  The JAR is not included here. Download that exact version from the
  [PlantUML releases page](https://github.com/plantuml/plantuml/releases).
  The version matters: CSR measures how the renderer handles bad input, so
  another version can move the numbers.
- **The extractor JAR** `plantuml-stats-extractor-v2.jar`, in the repository
  root, only if you want to re-run the structural scorers. See below.

You need neither Java nor the JARs to rebuild the results from the archives.

### The structural extractor

Element F1 and Relationship F1 do not parse PlantUML text directly. They are
computed over a typed graph written by `DiagramStatsExtractor`. It is a fork of
PlantUML that reuses the renderer's own parser, so the ground truth and the
answer are read on the same terms.

The fork is published at **https://github.com/vovanrew/plantuml**, branch
`stats-extractor-graph`. Both JARs are in the root of this repository:

| File | Use | Fork commit | SHA-256 |
|---|---|---|---|
| `plantuml-stats-extractor-v2.jar` | The extractor of the scorer on `main` | `549fe8ec08` | `2747a72aec9206e424ddf9ed659f9eceb96730444a68b1fe99094317400f555b` |
| `plantuml-stats-extractor-v1.jar` | The extractor behind the older score files in `data.zip` | `7d2292dab1` | `f6e76d4973ce12c23cb15dff6420726f7d2203a80c1761d1454b5a2c5a91777b` |

```bash
export PLANTUML_EXTRACTOR_JAR=$PWD/plantuml-stats-extractor-v2.jar
```

The scorers read the JAR path from `PLANTUML_EXTRACTOR_JAR`, or take it as
`--jar`. Use this file rather than a build of your own. Each structural result
file records the SHA-256 of the JAR it was scored with. A JAR built from the
commit will in general have another hash.

The JARs are PlantUML and are licensed under the GNU General Public License,
version 3 or later ([`LICENSE-GPL-3.0`](LICENSE-GPL-3.0)), not under this
repository's MIT or CC BY 4.0 licences. Their source is the fork at the commits
above.

The stock renderer JAR, `plantuml-1.2025.9.jar`, is a different file. The two
are not interchangeable.

## Reproducing the results

This rebuilds every table, figure and exhibit in `analysis/out_paper/` from the
shipped archives. It needs no API keys, no Java and no network access.

```bash
unzip data.zip && unzip data_v2.zip && unzip data_selfserved.zip
python3 -m pip install -r requirements.txt
python3 util/build_paper_root.py --fine-tune data_selfserved     # -> data_paper/
R="--data-root data_paper --registry analysis/model_registry_paper.json --out-dir analysis/out_paper"
python3 analysis/build_master_table.py $R    # -> master_table.*
python3 analysis/build_ci_table.py $R        # -> ci_table.*
python3 analysis/build_run_level.py $R       # -> run_level.*, crowding.*
python3 -m analysis.build_paper_extras $R    # -> paper_extras.*
python3 analysis/build_failure_index.py $R   # -> failure_index.*
python3 analysis/build_plots.py --registry analysis/model_registry_paper.json --out-dir analysis/out_paper --by-arm
python3 analysis/build_exhibits.py --out-dir analysis/out_paper   # -> exhibits.md, exhibits.html
python3 -m analysis.build_error_sample report --out analysis/out_paper/error_sample
python3 -m analysis.rater_check report       # -> rater_check/report.*
```

`util/build_paper_root.py` copies the stored result files into one data root,
`data_paper/`, and scores nothing. Run the analysis steps in the order shown,
because each step reads the output of the steps before it. `build_paper_extras`
also writes `paper_checks.*`, internal checks that are not shipped.

The last two commands rebuild the reports from the stored codes and ratings. The
error sample is drawn by `python3 -m analysis.build_error_sample draw`, and
`methodology/analysis-protocol.md` §7 describes it. The rater pairs are drawn,
rendered and put on rating pages by the `draw`, `render` and `sheets` commands of
`analysis/rater_check.py`. Its `render` step needs a render script outside this
repository (`--render-py`).

The pipeline is deterministic: fixed seeds, sorted iteration, no timestamps.
The rounded Markdown tables regenerate byte for byte. Full-precision values in
the `.json` and `.csv` outputs can differ in the last floating-point digit,
because the order of summation depends on the platform. No reported figure is
affected.

`analysis/README.md` describes what each script and each output file holds.

## Re-running the benchmark itself

You need this only to add a model or to score raw answers again. Full
instructions are in [`evaluation_plan.md`](evaluation_plan.md). The short
version:

```bash
# 1. Inference: 1000 images -> 1000 raw responses. Needs an endpoint, an API key and the images.
python3 evaluation/infer_runner.py --base-url <endpoint> --model <model id> --key-env <ENV_VAR> --n 1000 --out data/runs

# 2. Compilation success. Needs Java + plantuml-1.2025.9.jar.
python3 evaluation/csr_runner.py --pred-dir data/runs/<run> --out data/csr/<run>

# 3. Structural + surface metrics. Steps 3a-3c are independent of each other.
python3 evaluation/element_f1_runner.py      --pred-dir data/runs/<run> --out data/element_f1/<run>
python3 evaluation/relationship_f1_runner.py --pred-dir data/runs/<run> --out data/relationship_f1/<run>
python3 evaluation/chrf_runner.py            --pred-dir data/runs/<run> --out data/chrf/<run>
```

Then add the run to a registry and run the analysis steps again. Steps 3a and 3b
need the extractor JAR. Step 1 needs the standardized input images, which are in
`data/puml_images_1568/`, outside `data.zip` (see below).

API keys are read from the environment. No key is stored in this repository.

## The data archives

### `data.zip`

`data.zip` is 14 MB and holds 17,023 files. Unzipping it at the repository root
recreates `data/` where every script expects it.

```
data/
├── test_set.json                     The frozen 1000-diagram benchmark definition.
├── gt_token_stats.json               Ground-truth length statistics.
├── puml_files/                       1000 ground-truth .puml sources.
│   └── <key>.puml
├── runs/                             Raw model output, one directory per run.
│   └── <run>/
│       ├── run_meta.json             Model id, endpoint, prompt, decoding params.
│       ├── <key>.json                The raw API response, stored untouched.
│       └── <key>.puml                The PlantUML block isolated from that response.
├── csr/<run>/csr_results.json        Compilation success.
├── csr/<run>/errors.log              Renderer stderr for failed compiles.
├── element_f1/<run>/element_f1_results.json
├── relationship_f1/<run>/relationship_f1_results.json
└── chrf/<run>/chrf_results.json
```

The run directories are named `<model_id>_<timestampZ>`. The four hosted runs of
the panel are the `run_dir` values in `analysis/model_registry_paper.json`. The
archive also holds runs that the panel does not use. Its `element_f1/` and
`relationship_f1/` files are the older score files; the results take these two
metrics from `data_v2.zip`.

### `data_v2.zip` and `data_selfserved.zip`

`data_v2.zip` holds the Element F1 and Relationship F1 result files of the hosted
runs, scored by the scorer on `main`. Unzipping it at the root recreates
`data_v2/`, with `element_f1/<run>/` and `relationship_f1/<run>/`. It holds the
result files only: the extracted graphs are left out, and re-running the
scorers writes them again. `python3 util/pack_data_v2.py --check` compares the
archive with an unpacked `data_v2/`.

`data_selfserved.zip` holds the three self-served runs. Unzipping it at the root
recreates `data_selfserved/runs/test/<size>_zero_shot/`. Each run holds the 1,000
answers (`answers/`), the four result files (`scores/`, with the SHA-256 of each
in `scores/manifest.json`) and the provenance of the run (`answer_manifest.json`,
logs). `python3 util/pack_selfserved.py --fine-tune <dir> --check` compares the
archive with a directory that holds `runs/test/`.

### `test_set.json`

The benchmark definition, and the file to cite when you refer to "the test set".
It has four metadata blocks and the diagram list:

| Field | Content |
|---|---|
| `config` | Sampling parameters: `seed` 42, `n_per_cell` 125, `repo_cap` 5, `elements_max` 50, and the degeneracy filter settings. |
| `quartile_thresholds` | The `content_lines` tier boundaries, per diagram type. |
| `cell_stats` | Per `(type, tier)` cell: how many diagrams were available, how many selected. |
| `count` | 1000. |
| `diagrams` | The 1000 records. |

```json
{
  "key": "000133b38e70cfb70834681221553363e9f37714.puml",
  "blob_id": "000133b38e70cfb70834681221553363e9f37714",
  "primary_type": "class",
  "tier": 1,
  "content_lines": 3,
  "elements_total": 1,
  "connections_total": 0,
  "repository": "H4rmey_PotionPalooza",
  "image_width": 685,
  "image_height": 512
}
```

**The identifier is `key`, the filename, not `blob_id`.** A source file with
several `@startuml` blocks is split into siblings that share a `blob_id`. A
`_NN` suffix tells them apart. There are 37 such split files in the test set, so
joining on `blob_id` silently merges them.

One more join detail: `test_set.json` keys carry the `.puml` suffix, and the
metric files key on the bare stem. `analysis/loader.py` strips the suffix. A raw
equality join matches zero rows.

### Answer records: `runs/<run>/<key>.json`

The provider's response, stored as received, so its shape follows the API that
produced it. Most runs are OpenAI-compatible chat completions: the generated text
is at `choices[0].message.content`, and token counts are under `usage`. The
Gemini run is the provider's native format, with the text at
`candidates[0].content.parts[0].text` and the counts under `usageMetadata`.

A failed cell still gets a record, so a failure stays countable and does not
become a missing row:

```json
{"error": "timeout", "key": "938e9cc0...bd_02", "attempts": 1, "detail": "hard deadline 600s"}
```

`error` is one of `timeout`, `image_dropped`, `http_error`, `network_error` and
`bad_response`. No `.puml` is written for a failed cell, so CSR scores it 0.

The sibling `<key>.puml` is the PlantUML block isolated from the response: the
span from the first `@startuml` to the last `@enduml`. This is the exact text
that was scored.

`run_meta.json` records `n_cells` for the **final** batch of a run. Runs can be
resumed, so a small `n_cells` means that a resume completed the run. Every run
covers all 1,000 keys.

### Metric records

All four files share a `{"summary": ..., "diagrams": [...]}` shape, with one
entry per test-set key in `diagrams`.

**`csr_results.json`**

```json
"summary":  {"pred_dir": "data/runs/<run>", "n": 1000, "compiled": 935,
             "csr": 0.935, "min_png_bytes": 256}
"diagrams": {"key": "000133b3...", "compiled": true, "n_png": 1,
             "png_bytes": 2555, "error": null}
```

**`element_f1_results.json`**: `summary` is keyed by population
(`zeros_for_failed`, `compiled_only`), and each holds `micro`, `macro` and `n`.

```json
"diagrams": {"key": "000133b3...", "tp": 1, "fp": 0, "fn": 0,
             "precision": 1.0, "recall": 1.0, "f1": 1.0,
             "has_pred": true, "compiled": true,
             "type_accuracy": {"matched": 1, "correct": 1, "excluded": 0}}
```

`type_accuracy.excluded` counts name-matched entities whose UML type cannot be
graded. They are removed from the denominator, not counted as wrong.

**`relationship_f1_results.json`**: the same populations, and each has an `all`
block and a `by_relation` block for the six relation types. Per diagram, it has
the same counts and a `by_relation` breakdown.

The structural files in `data_v2.zip` and `data_selfserved.zip` start with a
`scorer` block. It records the rules that were on, the options passed to the
extractor and the SHA-256 of the extractor JAR.

**`chrf_results.json`**: `summary` records the scoring parameters
(`char_order` 6, `word_order` 2, `beta` 2). Per population, it has `micro`
(corpus chrF++) and `macro` (mean of the per-diagram scores).

```json
"diagrams": {"key": "000133b3...", "has_pred": true, "compiled": true,
             "score": 69.04552345548973}
```

Scores are on sacrebleu's native 0-100 scale, stored unrescaled.

### What is not in the archives, and why

**The diagram images.** Two sets exist: `puml_images/` (the original renders,
242 MB) and `puml_images_1568/` (the standardized model inputs, 187 MB). PNG is
already compressed, so zipping them saves almost nothing. Either set alone, as a
single file, would exceed GitHub's file size limit.

The standardized model inputs are therefore tracked as plain files in
`data/puml_images_1568/`, next to `data.zip`: 1,000 PNG files, one per diagram,
named by key. A clone has them, and unzipping `data.zip` fills in the rest of
`data/` around them. The Zenodo record of release v1.0.0 does not hold them.

The original renders are not in the repository. You need them only to rebuild the
standardized set from the corpus:

```bash
python3 util/populate_test_set.py --test-set data/test_set.json --prune  # needs the corpus
python3 util/standardize_images.py                                       # -> puml_images_1568/
```

Rendering uses PlantUML `1.2025.9`. `util/populate_test_set.py` reads the corpus
location from the `PLANTUML_DATASET_ROOT` environment variable.

**Metric intermediates.** The scorers also write rendered PNGs and extracted
graph JSON under each metric directory, about 390 MB in total. Nothing reads
them: `analysis/loader.py` reads only the four `*_results.json` files per run.
They help with inspection, and re-running the scorers writes them again.

## Tests

```bash
python3 -m pytest tests/
```

413 test functions across 27 modules. They cover the scoring logic, the
aggregation math, the bootstrap, the registry and loader, the plot builders, the
human-rater check and the frozen prompt. A test skips, and does not fail, when
what it needs is absent: benchmark data that is not unpacked, the standardized
images, or the extractor JAR.

The extractor tests run only when `PLANTUML_EXTRACTOR_JAR` points at
`plantuml-stats-extractor-v2.jar`.

## Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21670236.svg)](https://doi.org/10.5281/zenodo.21670236)

If you use this benchmark, its data, or its evaluation framework, please cite it:

> Polishchuk, V. (2026). *Zero-shot image-to-PlantUML: a multi-level structural
> evaluation framework and benchmark* (v1.0.0) [Software]. Zenodo.
> https://doi.org/10.5281/zenodo.21670236

```bibtex
@software{polishchuk2026plantuml,
  author    = {Polishchuk, Volodymyr},
  title     = {Zero-shot image-to-{PlantUML}: a multi-level structural
               evaluation framework and benchmark},
  year      = {2026},
  publisher = {Zenodo},
  version   = {v1.0.0},
  doi       = {10.5281/zenodo.21670236},
  url       = {https://doi.org/10.5281/zenodo.21670236}
}
```

`10.5281/zenodo.21670236` is the concept DOI: it always resolves to the newest
version, so it stays correct as this work is updated. To cite this exact
release instead, use `10.5281/zenodo.21670237`.

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff).

## Licence

Code is MIT. Data and documentation are CC BY 4.0, **except** the ground-truth
`.puml` sources and any image rendered from them. Those were mined from
open-source repositories, and each remains under the licence of the repository
it came from.

The two extractor JARs are PlantUML, under the GNU GPL v3 or later
([`LICENSE-GPL-3.0`](LICENSE-GPL-3.0)). Their source is the fork at the commits
in [The structural extractor](#the-structural-extractor).

See [`LICENSE`](LICENSE) and [`LICENSE-DATA`](LICENSE-DATA). The second file
matters if you plan to redistribute the diagram sources or the images.

## Scope and limitations

These limits bound what the numbers support.

- Two of nine diagram types in the corpus: class and sequence only.
- Zero-shot only. Fine-tuning is not evaluated here.
- One frozen prompt, with no prompt ablation.
- Minimum-reasoning configuration only. Gemini 3.1 Pro cannot fully disable
  thinking, but it used zero thinking tokens across the run.
- Structural metrics plus chrF++. No visual similarity, no graph edit distance,
  no model-as-judge.
- The panel is reported in two groups, hosted and self-served, and never as one
  ranked order.

Deferred extensions, each scoped and costed, are in
[`FUTURE.md`](FUTURE.md).
