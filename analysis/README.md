# `analysis/` — the analysis pipeline

Turns the per-model metric JSONs under `data/` into the paper's exhibits:
**aggregate → master table → bootstrap CIs → plots → failure cases → run-level →
paper exhibits**. The scientific rationale for each step is recorded in
`../methodology/analysis-protocol.md`.

The folder has two parts: **code** (the `.py` files + one config) and **`out/`**
(everything the code generates — the files you *read*). You only ever *run* the
`build_*.py` scripts and *read* the files in `out/`.

## Naming convention

> **`build_X.py`** = a runnable CLI (an entry point).
> **`X.py`** = the importable logic it uses (pure functions, unit-tested in `../tests/`).

Every `build_*.py` has one sibling logic module.

## Code

### Shared foundation (used by every task)

| File | Role |
|---|---|
| `model_registry.json` | **Config** — the 7 reported models, their run-dir names, arm/family/params. *The one file the author edits as runs land.* |
| `registry.py` | Loads & validates the registry. |
| `loader.py` | Reads the four metric JSONs from `data/` and joins each diagram to its `primary_type` + complexity `tier`. |
| `panel.py` | Eligibility gate — which models are scored, leak-clean, and ready to report. |
| `leak_gate.py` | Confirms no `<think>` reasoning leaked into a scored prediction. |
| `aggregate.py` | The pooling math (micro/macro, both populations, type accuracy, population gap). |

### One logic module + one driver per task

| Task | Logic module(s) | Driver (run this) | Outputs in `out/` |
|---|---|---|---|
| 1 — master table | `aggregate.py`, `report.py` | `build_master_table.py` | `master_table.*` |
| 2 — bootstrap CIs | `bootstrap.py`, `ci_report.py` | `build_ci_table.py` | `ci_table.*` |
| 3 — plots | `plots.py` | `build_plots.py` | `plots/*` |
| 4 — failure sampler | `failure_sampler.py` | `build_failure_index.py` | `failure_index.*` |
| 5 — run-level | `run_level.py` | `build_run_level.py` | `run_level.*`, `crowding.*` |
| 6 — paper exhibits | `exhibits.py` | `build_exhibits.py` | `exhibits.md`, `exhibits.html` |

## Run order

Each step reads the previous steps' outputs, so run them in this order:

```
python3 analysis/build_master_table.py        # → master_table.*
python3 analysis/build_ci_table.py            # → ci_table.*
python3 analysis/build_run_level.py           # → run_level.*, crowding.*
python3 analysis/build_plots.py               # reads master + ci + crowding → plots/*
python3 analysis/build_failure_index.py       # → failure_index.*
python3 analysis/build_exhibits.py            # reads everything → exhibits.md + exhibits.html
```

Re-running is idempotent: fixed seeds, sorted iteration, no timestamps → byte-identical
output for unchanged inputs. A model that is pending/missing in the registry is skipped
with a logged note (outputs are headed "N/7"), never an error.

## `out/` — generated artifacts (read these; do not hand-edit)

Each artifact is emitted in **three formats of the same data**:

- **`.md`** — human-readable (open these).
- **`.json`** — full nested data (what the next stage consumes).
- **`.csv`** — flat tables (for spreadsheets / pivoting).

So `master_table.{md,json,csv}` is one result, three ways. Same for `ci_table`,
`run_level`, `failure_index`, `crowding`.

| Artifact | What it holds |
|---|---|
| `master_table.*` | Per-model × metric × {micro,macro} × {honest, compiled-only} × overall/type/tier, plus per-relation read-through, type accuracy, and the population gap. |
| `ci_table.*` | Paired-bootstrap 95% CIs (overall + per-relation); the error bars for the figures. |
| `run_level.*` | Token totals, failure inventory (provider vs compile-fail), reproducibility provenance. |
| `crowding.*` | Per-tier image crowding (content_lines per megapixel after the 1568px resize). |
| `failure_index.*` | The stratified failure cases that feed the qualitative error write-up. |
| `plots/` | Figures as `.png` (viewing) + `.pdf` (paper): `scaling_curve`, `frontier_bars_*`, `per_relation_f1_*`, `breakdown_by_tier`, `breakdown_by_type`. |
| `exhibits.md` + `exhibits.html` | The paper-ready synthesis (two-arms layout). The `.html` is Word-importable — open it in Word, or copy a table in, to get editable Word tables. |

`out/` ships with this repository so the reported numbers can be read without running
anything. Everything in it is regenerable: unpack `data.zip` and follow the run order
above. Re-running overwrites these files in place; full-precision `.json`/`.csv` values
can differ from the committed ones in the last floating-point digit across platforms,
while the rounded `.md` tables reproduce byte-for-byte.

## Hand-written docs (in `analysis/`, tracked, safe to edit)

These live beside the code (NOT in the generated `out/`), so they are version-controlled:

- `README.md` — this file.
- `results_explained.md` — a plain-language companion to `exhibits.md`.
- `error_analysis.md` — the qualitative review of 40 failure cases drawn from
  `out/failure_index.md`.

## Reporting conventions (quick reference)

- **Two populations**, always side by side: `zeros_for_failed` (all 1000, non-compiled
  scored 0 — the honest headline) and `compiled_only` (over compiled cells, CSR
  reported separately).
- **Two arms**, never one leaderboard: frontier reference points (GPT-5.2, Opus 4.6,
  Gemini 3.1 Pro) vs the Qwen open ladder (dense 2B/9B/27B) plus the 397B-A17B MoE
  ceiling (reported at both total and active params, off the dense axis).
- Metrics, in priority order: CSR, Element F1 (+ type accuracy), Relationship F1
  (overall + 6 relation types), chrF++. Micro and macro both reported.

See `../methodology/analysis-protocol.md` for the full invariants and the
validation-gate anchor table.
