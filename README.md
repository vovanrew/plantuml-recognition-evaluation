# Zero-shot image-to-PlantUML: evaluation framework and benchmark

Can a multimodal language model look at a picture of a UML diagram and write back
the PlantUML source that produced it?

This repository holds the benchmark that answers that question, the evaluation
framework it is scored with, and every artifact needed to reproduce the result:
1,000 diagrams, 8 model runs, all raw predictions, all computed metrics, and the
generated exhibits.

The task is **zero-shot**: each model sees one rendered diagram image and one
frozen prompt, and must emit PlantUML source. No examples, no fine-tuning, no
diagram-type hint. Scope is **class and sequence diagrams**.

## What makes this benchmark different

A rendered UML diagram is a typed graph, but text-similarity scores treat its
source as a string and manual error counts do not scale past a few dozen cases.
This framework scores the reconstruction at several levels at once, structural
as well as surface, and reports each structural metric over **two
populations**.

That second point is the methodological core. A model that fails to produce
compilable output on hard diagrams looks deceptively strong if you only score
the diagrams it managed to compile. Reporting the compiled-only number beside
the full-set number makes that selective-failure bias visible instead of hiding
it. On this benchmark the effect is large: the smallest model scores 0.878
Element F1 on the diagrams it compiles, but 0.246 across all 1,000.

## Metrics

| Metric | What it measures |
|---|---|
| **CSR** (Compilation Success Rate) | The prediction renders to a non-empty image. A prediction that parses but renders nothing is a failure, as is a missing prediction. Precondition for everything else. |
| **Element F1** | Recovery of named entities (classes, interfaces, enums, participants, actors). Matched on normalized display name only. |
| **Relationship F1** | Recovery of typed edges as `(source, target, relation_type)` over inheritance, composition, aggregation, dependency, association, message. Reported overall and per relation type. |
| **Type accuracy** | Among name-matched entities, the share carrying the correct UML type. Companion to Element F1. |
| **chrF++** | Character and word n-gram surface similarity, covering what the structural metrics deliberately ignore: member signatures, multiplicities, message wording, control-flow framing, notes. |

Structural metrics and chrF++ are each reported two ways: **full-set** (all
1,000 diagrams, non-compiling predictions scored 0) and **compiled-only** (over
compiled predictions, with CSR reported separately). Uncertainty is a paired
bootstrap over diagrams, 1,000 resamples, fixed seed.

Full definitions, including the edge cases, are in
[`methodology/evaluation-framework.md`](methodology/evaluation-framework.md).

## Headline results

Point estimates. Structural columns are `full-set / compiled-only`. Confidence
intervals for every cell are in
[`analysis/out/exhibits.md`](analysis/out/exhibits.md), Exhibit 1.

These are **two arms, not one leaderboard**. The frontier models are fixed
reference points, one flagship per lab. The Qwen3.5 arm is an open-model family
studied as a scaling curve, and it is the fine-tuning target of later work.

**Frontier reference points**

| Model | CSR | Element F1 | Relationship F1 | chrF++ macro | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.897 / 0.939 | 0.757 / 0.799 | 62.73 / 67.09 | 0.941 |
| Claude Opus 4.6 | 94.1% | 0.909 / 0.940 | 0.693 / 0.720 | 65.68 / 69.80 | 0.950 |
| Gemini 3.1 Pro | 97.2% | 0.945 / 0.961 | 0.875 / 0.893 | 75.53 / 77.70 | 0.984 |

**Qwen3.5 open family** — dense 2B/9B/27B ladder, plus the mixture-of-experts
model as a separate capability ceiling, not a fourth dense rung.

| Model | Params | CSR | Element F1 | Relationship F1 | chrF++ macro | Type acc |
|---|---|---|---|---|---|---|
| Qwen3.5-2B | 2B | 20.1% | 0.246 / 0.878 | 0.114 / 0.481 | 12.89 / 64.14 | 0.758 |
| Qwen3.5-9B | 9B | 43.1% | 0.491 / 0.844 | 0.201 / 0.439 | 26.91 / 62.43 | 0.756 |
| Qwen3.5-27B | 27B | 60.1% | 0.676 / 0.917 | 0.485 / 0.722 | 40.91 / 68.07 | 0.886 |
| Qwen3.5-397B-A17B | 397B total, 17B active | 78.7% | 0.771 / 0.897 | 0.646 / 0.736 | 49.23 / 62.56 | 0.870 |

Read the two populations together. Element F1 on the dense ladder rises steeply
on the full set (0.246 to 0.676) while the compiled-only number barely moves and
is not monotonic. Most of what scale buys on this task is the ability to emit
compilable output at all.

A plain-language walkthrough of every result is in
[`analysis/results_explained.md`](analysis/results_explained.md). A categorized
review of 40 failure cases is in
[`analysis/error_analysis.md`](analysis/error_analysis.md).

A Claude Sonnet 4.6 run is also included in `data.zip` and the registry, marked
supplementary. It is scored but excluded from the 7-model reported panel.

## The test set

1,000 diagrams: 2 types (class, sequence) x 4 complexity tiers x 125.

Diagrams come from the *UML-in-the-Wild* corpus, 143,427 PlantUML/PNG pairs
mined from open-source repositories via **World of Code**. Selection is
repository-disjoint, deduplicated on normalized source, and filtered so the
corpus type label agrees with the PlantUML parser's own reading of the file.
Complexity tiers are quartiles of `content_lines`, computed per diagram type.
Sampling is a fixed seed (42) with at most 5 diagrams per source repository.

Every model receives the identical input image, standardized to a **1,568 px
long edge**. That figure is the lowest native processing resolution across the
model panel, so it is the highest resolution every model can be given on equal
terms.

The construction pipeline, with counts at every filter stage, is in
[`methodology/test-set-construction.md`](methodology/test-set-construction.md).

## Repository layout

```
analysis/          Aggregation, bootstrap CIs, plots, exhibits. See analysis/README.md.
  out/             Generated tables, figures and exhibits (shipped, regenerable).
  model_registry.json   The 7 reported models + 1 supplementary, and their run dirs.
  results_explained.md  Plain-language walkthrough of the results.
  error_analysis.md     Qualitative review of 40 failure cases.
evaluation/        Inference runner and the four metric scorers.
util/              Test-set construction, image standardization, token measurement.
methodology/       The methodological record. The source of truth for every design decision.
prompts/           The frozen zero-shot prompt.
tests/             310 test functions across 19 modules.
data.zip           The benchmark data. Unzip at the repository root.
evaluation_plan.md How to run the benchmark end to end.
FUTURE.md          Scoped extensions that were deliberately deferred.
```

## Requirements

- **Python 3.10 or newer.** `python3 -m pip install -r requirements.txt`
- **A Java runtime**, for the PlantUML renderer. The reported runs used
  Temurin JDK 26.0.1.
- **PlantUML `1.2025.9`**, as `plantuml-1.2025.9.jar` in the repository root.
  The JAR is not vendored here. Download that exact version from the
  [PlantUML releases page](https://github.com/plantuml/plantuml/releases).
  The version matters: renderer behaviour on malformed input is what CSR
  measures, so a different version can move the numbers.
- **The `DiagramStatsExtractor` fork**, only if you want to re-run the
  structural scorers. Build instructions below.

### The structural extractor

Element F1 and Relationship F1 do not parse PlantUML text directly. They are
computed over a typed graph emitted by `DiagramStatsExtractor`, a fork of
PlantUML that reuses the renderer's own parser, so ground truth and prediction
are read on identical terms.

The fork is published separately, at
**https://github.com/vovanrew/plantuml**. Build it like this:

```bash
git clone -b stats-extractor-graph https://github.com/vovanrew/plantuml.git
cd plantuml
./gradlew build -x test -x javaDoc        # -> build/libs/plantuml-1.2025.9.jar
export PLANTUML_EXTRACTOR_JAR=$PWD/build/libs/plantuml-1.2025.9.jar
```

**Check out `stats-extractor-graph` explicitly.** It is not the fork's default
branch, and it is the branch that emits the named graph these metrics are scored
on. The scorers read the JAR path from `PLANTUML_EXTRACTOR_JAR`, or take it as
`--jar`.

Mind the filename: the fork builds to `plantuml-1.2025.9.jar`, the same name as
the stock renderer JAR, but the two are not interchangeable. Keep them apart, or
rename one.

You do not need any of this to reproduce a reported number. The extracted graphs
are already reflected in the shipped `*_results.json` files, so the whole
analysis pipeline runs from `data.zip` alone. The extractor is needed only to
**re-score** raw predictions from scratch, or to score a new model.

## Reproducing the analysis

This reproduces every table, figure and exhibit in the paper from the shipped
data. It needs no API keys, no Java, and no network access.

```bash
unzip data.zip                                # recreates data/
python3 -m pip install -r requirements.txt

python3 analysis/build_master_table.py        # -> analysis/out/master_table.*
python3 analysis/build_ci_table.py            # -> ci_table.*
python3 analysis/build_run_level.py           # -> run_level.*, crowding.*
python3 analysis/build_plots.py               # -> plots/*
python3 analysis/build_failure_index.py       # -> failure_index.*
python3 analysis/build_exhibits.py            # -> exhibits.md, exhibits.html
```

Run them in that order; each step reads the previous steps' output. The pipeline
is deterministic: fixed seeds, sorted iteration, no timestamps. Re-running
overwrites `analysis/out/` in place.

One caveat on exact reproduction. The rounded Markdown tables regenerate
byte-for-byte. Full-precision values in the `.json` and `.csv` outputs can differ
from the committed ones in the final floating-point digit, because summation
order in the accumulators is sensitive to the platform's floating-point
behaviour. No reported figure is affected.

`analysis/README.md` documents what each script and each output file holds.

## Re-running the benchmark itself

Only needed to add a model or re-score raw predictions. Full instructions are in
[`evaluation_plan.md`](evaluation_plan.md); the short version:

```bash
# 1. Inference: 1000 images -> 1000 raw responses. Needs an API key and the images.
python3 evaluation/infer_runner.py --n 1000 --out data/runs

# 2. Compilation success. Needs Java + plantuml-1.2025.9.jar.
python3 evaluation/csr_runner.py --pred-dir data/runs/<run> --out data/csr/<run>

# 3. Structural + surface metrics. Steps 3a-3c are independent of each other.
python3 evaluation/element_f1_runner.py      --pred-dir data/runs/<run> --out data/element_f1/<run>
python3 evaluation/relationship_f1_runner.py --pred-dir data/runs/<run> --out data/relationship_f1/<run>
python3 evaluation/chrf_runner.py            --pred-dir data/runs/<run> --out data/chrf/<run>
```

Then add the run to `analysis/model_registry.json` and re-run the analysis
pipeline. Steps 3a and 3b require the extractor fork. Step 1 requires the
standardized input images, which are not in `data.zip` (see below).

API keys are read from the environment; no key is stored in this repository.

## The data archive

`data.zip` is 14 MB and holds 17,023 files. Unzipping at the repository root
recreates `data/` exactly where every script expects it.

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

Eight run directories, named `<model_id>_<timestampZ>`. They match the `run_dir`
values in `analysis/model_registry.json`, which is how the analysis pipeline
finds them.

### `test_set.json`

The benchmark definition and the artifact to cite when referring to "the test
set". Four metadata blocks plus the diagram list:

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

**The identifier is `key`, the filename, not `blob_id`.** A single source file
containing several `@startuml` blocks is split into siblings that share a
`blob_id` and are distinguished by a `_NN` suffix. There are 37 such split files
in the test set. Joining on `blob_id` silently merges them.

One more join detail: `test_set.json` keys carry the `.puml` suffix and the
metric files key on the bare stem. `analysis/loader.py` strips the suffix. A raw
equality join matches zero rows.

### Prediction records: `runs/<run>/<key>.json`

The provider's response, stored verbatim and unnormalized, so the shape follows
whichever API produced it. Most runs are OpenAI-compatible chat completions,
where the generated text is at `choices[0].message.content` and token counts are
under `usage`. The Gemini run is the provider's native format, with text at
`candidates[0].content.parts[0].text` and counts under `usageMetadata`.

A failed cell still gets a record, which is how a failure stays countable rather
than becoming a silently missing row:

```json
{"error": "timeout", "key": "938e9cc0...bd_02", "attempts": 1, "detail": "hard deadline 600s"}
```

`error` is one of `timeout`, `image_dropped`, `http_error`, `network_error`. No
`.puml` is written for a failed cell, so CSR scores it 0.

The sibling `<key>.puml` is the PlantUML block isolated from the response: the
span from the first `@startuml` to the last `@enduml`. This is the exact text
that was scored.

Note that `run_meta.json` records `n_cells` for the **final** batch of a run.
Runs were resumable, so a small `n_cells` means the run was completed by a
resume, not that it covered few diagrams. Every run covers all 1,000 keys.

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

**`element_f1_results.json`** — `summary` is keyed by population
(`zeros_for_failed`, `compiled_only`), each holding `micro`, `macro` and `n`.

```json
"diagrams": {"key": "000133b3...", "tp": 1, "fp": 0, "fn": 0,
             "precision": 1.0, "recall": 1.0, "f1": 1.0,
             "has_pred": true, "compiled": true,
             "type_accuracy": {"matched": 1, "correct": 1, "excluded": 0}}
```

`type_accuracy.excluded` counts name-matched entities whose UML type cannot be
graded, and they are removed from the denominator rather than counted wrong.

**`relationship_f1_results.json`** — same populations, and each carries both an
`all` block and a `by_relation` block covering the six relation types. Per
diagram, the same counts plus a `by_relation` breakdown.

**`chrf_results.json`** — `summary` records the scoring parameters
(`char_order` 6, `word_order` 2, `beta` 2) and, per population, `micro` (corpus
chrF++) and `macro` (mean of per-diagram scores).

```json
"diagrams": {"key": "000133b3...", "has_pred": true, "compiled": true,
             "score": 69.04552345548973}
```

Scores are on sacrebleu's native 0-100 scale, stored unrescaled.

### What is not in the archive, and why

**The diagram images.** Two sets exist: `puml_images/` (the original renders,
242 MB) and `puml_images_1568/` (the standardized model inputs, 187 MB). PNG is
already compressed, so zipping them saves essentially nothing, and either one
alone would exceed GitHub's file size limit.

<!-- TODO(author): once the image archives are uploaded to Zenodo as their own
     record, replace this paragraph with the link and its DOI. -->

They are not in the Zenodo record above either, which holds the repository
archive only. Regenerate them from the ground-truth sources, which is the fully
reproducible route in any case:

```bash
python3 util/populate_test_set.py --test-set data/test_set.json --prune  # needs the corpus
python3 util/standardize_images.py                                       # -> puml_images_1568/
```

Rendering uses PlantUML `1.2025.9`. `util/populate_test_set.py` reads the corpus
location from the `PLANTUML_DATASET_ROOT` environment variable.

**Metric intermediates.** The scorers also write rendered PNGs and extracted
graph JSON under each metric directory, roughly 390 MB in total. Nothing reads
them: `analysis/loader.py` consumes only the four `*_results.json` files per run.
They are inspection aids, and they are regenerable by re-running the scorers.

## Tests

```bash
python3 -m pytest tests/
```

310 test functions across 19 modules, covering the scoring logic, the
aggregation math, the bootstrap, the registry and loader, the plot builders, and
the frozen prompt. Tests skip cleanly rather than fail when what they need is
absent: benchmark data that has not been unpacked, or the extractor JAR.

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
`.puml` sources and any image rendered from them: those were mined from
open-source repositories and each remains under the licence of the repository it
came from.

See [`LICENSE`](LICENSE) and [`LICENSE-DATA`](LICENSE-DATA). The second file
matters if you plan to redistribute the diagram sources or the images.

## Scope and limitations

Stated plainly, because they bound what the numbers support.

- Two of nine diagram types in the corpus: class and sequence only.
- Zero-shot only. Fine-tuning is later work, not evaluated here.
- One frozen prompt, no prompt ablation.
- Minimum-reasoning configuration only. Gemini 3.1 Pro cannot fully disable
  thinking, but emitted zero thinking tokens across the run, so the frontier
  comparison is clean on this axis.
- Structural metrics plus chrF++. No visual similarity, no graph edit distance,
  no model-as-judge.
- The mixture-of-experts model was served differently from the dense ladder, so
  it is a capability ceiling rather than a backend-matched fourth rung.

Deferred extensions, each scoped and costed, are in
[`FUTURE.md`](FUTURE.md).
