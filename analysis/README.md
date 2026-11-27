# `analysis/`: the analysis pipeline

This folder turns the stored per-diagram scores into the tables, intervals and
figures of the benchmark. The method behind each step is in
`../methodology/analysis-protocol.md`. The metrics are defined in
`../methodology/evaluation-framework.md`, and the inference runs in
`../methodology/benchmark-protocol.md`.

The folder holds code (the `.py` files), the model registry, the generated outputs
in `out_paper/`, and a few hand-written documents.

## The panel and the registry

`model_registry_paper.json` lists the models of the benchmark. Every script below
reads it through `--registry`. The panel has two groups, and every output lists the
hosted group first.

- **Hosted reference models** (`"arm": "frontier"`): GPT-5.2, Claude Opus 4.6,
  Gemini 3.1 Pro and Qwen3.5-397B-A17B. Each one ran on its provider's serving.
- **Self-served open models** (`"arm": "qwen"`): Qwen3.5-2B, Qwen3.5-9B and
  Qwen3.5-27B. They ran on one GPU with the released bf16 weights.

Size trends use the three dense self-served models only. Qwen3.5-397B-A17B is a
mixture-of-experts model, so it is not on the size axis. Each entry also gives the
run directory, the lab, the model family and the parameter counts. Entries with
`"supplementary": true` are not part of the panel, and the scripts leave them out
unless `--include-supplementary` is given.

The scripts read the scored runs from `--data-root data_paper`. The folder
`data_paper/` is built from the released archives by `util/build_paper_root.py`
(see the run order below).

## Naming convention

- `build_X.py` is a command-line script that you run.
- `X.py` is the logic module that it imports. The modules are tested in `../tests/`.

## Code

### Shared modules

| File | Role |
|---|---|
| `registry.py` | Loads and checks the registry: unique ids and known values for status, arm and family. |
| `loader.py` | Reads the four metric files of a run and joins each diagram to its diagram type and complexity tier from the test set. |
| `panel.py` | Loads every registered run that is on disk and applies the eligibility gate. |
| `leak_gate.py` | Refuses a run whose answers contain a `<think>` block. |
| `aggregate.py` | Pools the per-diagram rows: micro and macro, both populations, type accuracy, population gap. |

### One logic module and one script per task

| Task | Logic module | Script (run this) | Output in `out_paper/` |
|---|---|---|---|
| Master table | `aggregate.py`, `report.py` | `build_master_table.py` | `master_table.*`, `master_table_per_relation.csv`, `master_table_type_accuracy.csv` |
| Bootstrap intervals | `bootstrap.py`, `ci_report.py` | `build_ci_table.py` | `ci_table.*`, `ci_table_pairwise.csv` |
| Run-level tables | `run_level.py` | `build_run_level.py` | `run_level.*`, `crowding.*` |
| Per-type and per-tier intervals | `bootstrap.py` | `build_paper_extras.py` | `paper_extras.md`, `paper_extras.json` |
| Failure index | `failure_sampler.py` | `build_failure_index.py` | `failure_index.*` |
| Figures | `plots.py` | `build_plots.py` | `plots/*` |
| Exhibits | `exhibits.py` | `build_exhibits.py` | `exhibits.md`, `exhibits.html` |
| Error-analysis sample | `failure_sampler.py` | `build_error_sample.py` | `error_sample/` |
| Human-rater check | (in the script) | `rater_check.py` | `rater_check/` |

`build_paper_extras.py` also writes `paper_checks.md` and `paper_checks.json`. They
are internal checks, not results, and the release leaves them out.

Two more scripts draw the method figures of the manuscript. They show no results.
`build_pipeline_figure.py` draws the test-set selection flow, and
`build_framework_figure.py` draws the evaluation framework. Both take `--out-dir`,
`--plots-subdir`, `--name` and `--dpi`.

## Run order

Each step reads the outputs of the steps before it, so run them in this order from
the repository root:

```bash
unzip data.zip && unzip data_v2.zip && unzip data_selfserved.zip
python3 util/build_paper_root.py --fine-tune data_selfserved     # -> data_paper/
R="--data-root data_paper --registry analysis/model_registry_paper.json --out-dir analysis/out_paper"
python3 analysis/build_master_table.py $R
python3 analysis/build_ci_table.py $R
python3 analysis/build_run_level.py $R
python3 -m analysis.build_paper_extras $R
python3 analysis/build_failure_index.py $R
python3 analysis/build_plots.py --registry analysis/model_registry_paper.json --out-dir analysis/out_paper --by-arm
python3 analysis/build_exhibits.py --out-dir analysis/out_paper
```

`build_plots.py` reads `master_table.json`, `ci_table.json` and `crowding.json` from
`--out-dir`. With `--by-arm`, the multi-model figures show the hosted models first and
the self-served models second, with one legend row for each group.
`build_exhibits.py` reads the master table, the CI table, the run-level tables,
the crowding file and the failure index from `--out-dir`.

The error-analysis sample is drawn once and then coded by two coders. The `report`
command joins their codes with the key:

```bash
python -m analysis.build_error_sample draw   --data-root data_paper --registry analysis/model_registry_paper.json --out analysis/out_paper/error_sample
python -m analysis.build_error_sample report --out analysis/out_paper/error_sample
```

The human-rater check has four commands. Their defaults are `--data-root data_paper`,
`--registry analysis/model_registry_paper.json` and `--out analysis/out_paper/rater_check`:

```bash
python -m analysis.rater_check draw   --exclude <keys.json of an earlier rater round>
python -m analysis.rater_check render --render-py ../fine-tune/build/render.py
python -m analysis.rater_check sheets
python -m analysis.rater_check report
```

`render` also takes `--threads` and `--heap-mb`, and `sheets` takes `--sheets`. The
rendered pictures (`rater_check/render/`) and the rating pages (`rater_sheets/`) are
not tracked. The method is in `../methodology/analysis-protocol.md` §11.

Other flags: `build_master_table.py`, `build_ci_table.py`, `build_run_level.py` and
`build_failure_index.py` take `--basename`, `--include-supplementary` and
`--log-level`. `build_ci_table.py` also takes `--n-resamples` and `--seed`.
`build_failure_index.py` also takes `--per-cell`, `--low-structural-threshold`,
`--include-ok`, `--seed`, `--small-diagram-lines` and `--snippet-max-lines`.
`build_plots.py` also takes `--plots-subdir`, and `build_exhibits.py` takes one
`--*-basename` flag for each of its four inputs.

Re-running gives the same files for the same inputs: the seeds are fixed, the order
is sorted, and no output carries a timestamp. Full-precision `.json` and `.csv`
values can differ in the last digit across platforms, while the rounded `.md` tables
stay the same.

## `out_paper/`: the results

Do not edit these files by hand. Most tables come in three formats of the same data:
`.md` to read, `.json` for the next step, `.csv` for spreadsheets.

| Output | What it holds |
|---|---|
| `master_table.*` | Each model's CSR, Element F1, Relationship F1, chrF++ and type accuracy: micro and macro, both populations, overall, per diagram type and per tier. Also the population gap, Relationship F1 per relation type, and type accuracy per entity type. |
| `ci_table.*` | Paired bootstrap 95% intervals for each model, intervals on the difference between each pair of models, and per-relation intervals. |
| `run_level.*` | Token totals over all 1,000 diagrams, the failure inventory, and the provenance of each run. |
| `crowding.*` | Image crowding per tier: source lines per megapixel of the resized test images. |
| `paper_extras.*` | 95% intervals for CSR, Element F1, Relationship F1 and chrF++ per diagram type and per tier, with the contrasts class minus sequence and tier 1 minus tier 4. |
| `failure_index.*` | The outcome counts and a stratified index of failure cases. |
| `plots/` | Figures as `.png` and `.pdf`: `scaling_curve` (the three dense sizes), `frontier_bars_*` (the hosted models), `per_relation_f1_*`, `breakdown_by_tier`, `breakdown_by_type`. |
| `exhibits.md`, `exhibits.html` | The results tables in one document. The `.html` file opens in Word with editable tables. |
| `error_sample/` | The 108-case error-analysis sample: cases, the two coders' codes, votes, final codes and report. |
| `rater_check/` | The human-rater check: the key, the two raters' ratings and the report. |

## Hand-written documents

These files sit beside the code and are edited by hand:

- `README.md`: this file.
- `results_explained.md`: the results in plain words, with the source file of each
  number.
- `error_analysis.md`: the kinds of failure, from the 108-case sample in
  `out_paper/error_sample/`.
- `error_codebook.md`: the codes used to classify the failure cases.

## Reporting rules (short)

- **Two populations**, always side by side. `zeros_for_failed` scores all 1,000
  diagrams, and an answer that does not compile scores 0; this is the main figure.
  `compiled_only` scores the compiled answers only, and CSR is given beside it.
- **Two groups of models**, not one ranking: the hosted reference models and the
  self-served dense sizes.
- Metrics: CSR, Element F1 with type accuracy, Relationship F1 (overall and for six
  relation types), and chrF++. Micro and macro are both reported.
- A difference between two models or two strata counts only when its 95% interval
  excludes zero.

The folder `out/` and the file `model_registry.json` are the default output folder and
registry of the scripts; they are not the benchmark's results.
