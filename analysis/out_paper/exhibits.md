# Paper exhibits — zero-shot image→PlantUML benchmark

**Models included: 7/7** (panel: main).

Assembled read-only from the validated Task-1..5 artifacts (`master_table.json`, `ci_table.json`, `run_level.json`, `crowding.json`, `failure_index.json`). No metric is re-pooled or recomputed here. Companion figures live in `plots/` beside this file; a Word-importable rendering of this document (tables paste straight into Microsoft Word) is emitted alongside it as `exhibits.html`.

## Exhibit 1 — Headline results (two arms)

Cells are `point [2.5th, 97.5th]` paired-bootstrap 95% CIs (n=1000, seed=20260614); CSR as a percentage, F1 / type accuracy on 0–1, chrF++ on its native 0–100 scale. Two populations per metric as `zeros_for_failed / compiled_only`. chrF++ is the **macro** statistic (the CI-bearing one; chrF++ micro is a corpus statistic, point-only — see Exhibit 2). Type accuracy is compiled-only by definition. **This is two arms, not one leaderboard.**

### Arm A — Hosted reference models

Each on its provider's serving (fixed comparison points).

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% [91.9%, 95.0%] | 0.916 [0.897, 0.933] / 0.958 [0.942, 0.971] | 0.770 [0.733, 0.803] / 0.812 [0.778, 0.842] | 62.73 [61.23, 64.20] / 67.09 [65.97, 68.18] | 0.941 [0.928, 0.954] |
| Claude Opus 4.6 | 94.1% [92.5%, 95.5%] | 0.934 [0.915, 0.949] / 0.966 [0.950, 0.979] | 0.700 [0.664, 0.735] / 0.728 [0.689, 0.762] | 65.68 [64.23, 67.18] / 69.80 [68.68, 70.98] | 0.951 [0.937, 0.963] |
| Gemini 3.1 Pro | 97.2% [96.2%, 98.1%] | 0.967 [0.957, 0.976] / 0.983 [0.975, 0.990] | 0.894 [0.870, 0.914] / 0.912 [0.891, 0.931] | 75.53 [74.19, 76.85] / 77.70 [76.52, 78.83] | 0.984 [0.973, 0.993] |
| Qwen3.5-397B-A17B | 78.7% [76.2%, 81.2%] | 0.794 [0.767, 0.818] / 0.924 [0.906, 0.939] | 0.657 [0.616, 0.697] / 0.746 [0.699, 0.788] | 49.23 [47.46, 51.17] / 62.56 [61.27, 64.00] | 0.871 [0.851, 0.889] |

### Arm B — Qwen open ladder (dense)

The dense 2B/9B/27B sizes, one serving, read as a scaling curve.

| Model | Params | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) | Type acc |
|---|---|---|---|---|---|---|
| Qwen3.5-2B | 2B | 19.2% [16.8%, 21.6%] | 0.239 [0.205, 0.272] / 0.875 [0.834, 0.913] | 0.110 [0.087, 0.134] / 0.461 [0.390, 0.537] | 11.88 [10.37, 13.50] / 61.87 [59.76, 64.10] | 0.757 [0.704, 0.809] |
| Qwen3.5-9B | 9B | 41.1% [38.1%, 44.4%] | 0.481 [0.445, 0.520] / 0.871 [0.840, 0.899] | 0.198 [0.169, 0.231] / 0.470 [0.415, 0.526] | 25.83 [23.73, 27.98] / 62.86 [61.15, 64.50] | 0.774 [0.731, 0.812] |
| Qwen3.5-27B | 27B | 64.6% [61.7%, 67.6%] | 0.713 [0.681, 0.743] / 0.946 [0.926, 0.961] | 0.507 [0.460, 0.552] / 0.730 [0.674, 0.782] | 43.97 [41.71, 46.22] / 68.07 [66.61, 69.64] | 0.889 [0.868, 0.910] |

## Exhibit 2 — Overall results, both populations × micro & macro

Read straight from the master table; CIs (where they exist) from the CI table. chrF++ micro is a corpus sacrebleu statistic (point estimate, no CI); chrF++ macro carries a CI.

### Micro

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 93.5% [91.9%, 95.0%] | 0.916 [0.897, 0.933] / 0.958 [0.942, 0.971] | 0.770 [0.733, 0.803] / 0.812 [0.778, 0.842] | 60.74 / 66.01 |
| Claude Opus 4.6 | 94.1% [92.5%, 95.5%] | 0.934 [0.915, 0.949] / 0.966 [0.950, 0.979] | 0.700 [0.664, 0.735] / 0.728 [0.689, 0.762] | 62.36 / 66.57 |
| Gemini 3.1 Pro | 97.2% [96.2%, 98.1%] | 0.967 [0.957, 0.976] / 0.983 [0.975, 0.990] | 0.894 [0.870, 0.914] / 0.912 [0.891, 0.931] | 72.19 / 74.54 |
| Qwen3.5-2B | 19.2% [16.8%, 21.6%] | 0.239 [0.205, 0.272] / 0.875 [0.834, 0.913] | 0.110 [0.087, 0.134] / 0.461 [0.390, 0.537] | 8.79 / 61.72 |
| Qwen3.5-9B | 41.1% [38.1%, 44.4%] | 0.481 [0.445, 0.520] / 0.871 [0.840, 0.899] | 0.198 [0.169, 0.231] / 0.470 [0.415, 0.526] | 22.88 / 62.22 |
| Qwen3.5-27B | 64.6% [61.7%, 67.6%] | 0.713 [0.681, 0.743] / 0.946 [0.926, 0.961] | 0.507 [0.460, 0.552] / 0.730 [0.674, 0.782] | 40.85 / 66.32 |
| Qwen3.5-397B-A17B | 78.7% [76.2%, 81.2%] | 0.794 [0.767, 0.818] / 0.924 [0.906, 0.939] | 0.657 [0.616, 0.697] / 0.746 [0.699, 0.788] | 47.80 / 59.77 |

### Macro

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.908 [0.890, 0.924] / 0.971 [0.962, 0.978] | 0.817 [0.795, 0.837] / 0.870 [0.853, 0.887] | 62.73 [61.23, 64.20] / 67.09 [65.97, 68.18] |
| Claude Opus 4.6 | 94.1% | 0.923 [0.907, 0.938] / 0.981 [0.975, 0.987] | 0.778 [0.758, 0.797] / 0.826 [0.808, 0.842] | 65.68 [64.23, 67.18] / 69.80 [68.68, 70.98] |
| Gemini 3.1 Pro | 97.2% | 0.961 [0.950, 0.971] / 0.989 [0.984, 0.993] | 0.924 [0.910, 0.936] / 0.949 [0.939, 0.959] | 75.53 [74.19, 76.85] / 77.70 [76.52, 78.83] |
| Qwen3.5-2B | 19.2% | 0.169 [0.147, 0.191] / 0.880 [0.845, 0.912] | 0.174 [0.154, 0.197] / 0.491 [0.430, 0.552] | 11.88 [10.37, 13.50] / 61.87 [59.76, 64.10] |
| Qwen3.5-9B | 41.1% | 0.365 [0.336, 0.395] / 0.888 [0.864, 0.909] | 0.265 [0.242, 0.290] / 0.536 [0.495, 0.577] | 25.83 [23.73, 27.98] / 62.86 [61.15, 64.50] |
| Qwen3.5-27B | 64.6% | 0.619 [0.590, 0.647] / 0.958 [0.946, 0.969] | 0.533 [0.504, 0.561] / 0.801 [0.775, 0.825] | 43.97 [41.71, 46.22] / 68.07 [66.61, 69.64] |
| Qwen3.5-397B-A17B | 78.7% | 0.737 [0.712, 0.763] / 0.936 [0.925, 0.947] | 0.647 [0.620, 0.675] / 0.805 [0.783, 0.826] | 49.23 [47.46, 51.17] / 62.56 [61.27, 64.00] |

## Exhibit 3 — Population gap (selective-failure bias)

`compiled_only − zeros_for_failed` (overall micro). A low-CSR model that drops/times out on its hardest diagrams is graded on an easier subset, so its compiled-only score runs far above its honest all-1000 score; the gap is that fingerprint and tracks CSR (near-zero for the frontier, large for the weak rungs).

| Model | CSR | ΔElement F1 | ΔRelationship F1 | ΔchrF++ |
|---|---|---|---|---|
| GPT-5.2 | 93.5% | +0.043 | +0.042 | +5.27 |
| Claude Opus 4.6 | 94.1% | +0.032 | +0.027 | +4.21 |
| Gemini 3.1 Pro | 97.2% | +0.016 | +0.018 | +2.35 |
| Qwen3.5-2B | 19.2% | +0.636 | +0.351 | +52.93 |
| Qwen3.5-9B | 41.1% | +0.390 | +0.273 | +39.34 |
| Qwen3.5-27B | 64.6% | +0.233 | +0.223 | +25.47 |
| Qwen3.5-397B-A17B | 78.7% | +0.130 | +0.089 | +11.97 |

## Exhibit 4 — Relationship F1 by relation type (with CIs)

Per-relation F1 (micro), `zeros_for_failed [CI] / compiled_only [CI]`. GT support (model-independent) annotates each relation.

| Model | inheritance<br>(n=940) | composition<br>(n=300) | aggregation<br>(n=244) | dependency<br>(n=375) | association<br>(n=862) | message<br>(n=6544) |
|---|---|---|---|---|---|---|
| GPT-5.2 | 0.820 [0.771, 0.865] / 0.851 [0.806, 0.896] | 0.634 [0.501, 0.756] / 0.658 [0.521, 0.782] | 0.618 [0.514, 0.714] / 0.625 [0.521, 0.722] | 0.618 [0.537, 0.689] / 0.630 [0.550, 0.703] | 0.549 [0.477, 0.624] / 0.594 [0.517, 0.671] | 0.814 [0.771, 0.855] / 0.862 [0.818, 0.901] |
| Claude Opus 4.6 | 0.870 [0.831, 0.901] / 0.886 [0.851, 0.917] | 0.467 [0.353, 0.588] / 0.492 [0.375, 0.617] | 0.508 [0.412, 0.606] / 0.520 [0.422, 0.621] | 0.581 [0.498, 0.665] / 0.592 [0.506, 0.677] | 0.461 [0.394, 0.529] / 0.476 [0.409, 0.542] | 0.732 [0.683, 0.779] / 0.765 [0.711, 0.811] |
| Gemini 3.1 Pro | 0.931 [0.906, 0.953] / 0.947 [0.925, 0.967] | 0.820 [0.728, 0.894] / 0.828 [0.736, 0.899] | 0.800 [0.719, 0.875] / 0.820 [0.746, 0.890] | 0.843 [0.785, 0.899] / 0.850 [0.792, 0.907] | 0.770 [0.701, 0.841] / 0.777 [0.709, 0.847] | 0.914 [0.886, 0.941] / 0.935 [0.908, 0.960] |
| Qwen3.5-2B | 0.076 [0.042, 0.117] / 0.388 [0.229, 0.564] | 0.000 [0.000, 0.000] / 0.000 [0.000, 0.000] | 0.008 [0.000, 0.027] / 0.125 [0.000, 0.308] | 0.013 [0.000, 0.034] / 0.029 [0.000, 0.070] | 0.036 [0.014, 0.062] / 0.134 [0.054, 0.231] | 0.141 [0.108, 0.173] / 0.605 [0.498, 0.716] |
| Qwen3.5-9B | 0.381 [0.317, 0.446] / 0.526 [0.448, 0.604] | 0.159 [0.076, 0.255] / 0.271 [0.147, 0.420] | 0.160 [0.079, 0.264] / 0.253 [0.127, 0.390] | 0.223 [0.153, 0.297] / 0.283 [0.199, 0.370] | 0.223 [0.174, 0.281] / 0.299 [0.234, 0.380] | 0.155 [0.114, 0.205] / 0.707 [0.625, 0.786] |
| Qwen3.5-27B | 0.665 [0.589, 0.739] / 0.790 [0.706, 0.854] | 0.340 [0.225, 0.466] / 0.563 [0.426, 0.686] | 0.470 [0.355, 0.589] / 0.578 [0.447, 0.700] | 0.535 [0.435, 0.619] / 0.647 [0.551, 0.737] | 0.372 [0.304, 0.444] / 0.464 [0.382, 0.548] | 0.509 [0.443, 0.566] / 0.792 [0.700, 0.868] |
| Qwen3.5-397B-A17B | 0.621 [0.543, 0.690] / 0.777 [0.717, 0.833] | 0.463 [0.339, 0.601] / 0.598 [0.451, 0.748] | 0.443 [0.321, 0.563] / 0.556 [0.425, 0.685] | 0.360 [0.274, 0.439] / 0.422 [0.326, 0.511] | 0.421 [0.340, 0.509] / 0.514 [0.417, 0.617] | 0.727 [0.674, 0.777] / 0.801 [0.740, 0.857] |

## Exhibit 5 — Per-type breakdown (class / sequence)

Point estimates (per-type cells are not bootstrapped). chrF++ is macro (poolable at sub-scopes).

### Type: class (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 94.4% | 0.916 / 0.957 | 0.667 / 0.697 | 65.74 / 69.64 |
| Claude Opus 4.6 | 97.4% | 0.945 / 0.967 | 0.627 / 0.644 | 71.77 / 73.68 |
| Gemini 3.1 Pro | 97.6% | 0.962 / 0.978 | 0.845 / 0.856 | 79.07 / 81.01 |
| Qwen3.5-2B | 20.0% | 0.220 / 0.889 | 0.040 / 0.172 | 12.69 / 63.46 |
| Qwen3.5-9B | 62.8% | 0.627 / 0.877 | 0.284 / 0.402 | 40.33 / 64.22 |
| Qwen3.5-27B | 78.2% | 0.777 / 0.949 | 0.522 / 0.657 | 54.78 / 70.05 |
| Qwen3.5-397B-A17B | 73.4% | 0.735 / 0.901 | 0.484 / 0.595 | 44.94 / 61.23 |

### Type: sequence (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 92.6% | 0.915 / 0.959 | 0.814 / 0.861 | 59.72 / 64.50 |
| Claude Opus 4.6 | 90.8% | 0.920 / 0.965 | 0.731 / 0.764 | 59.60 / 65.64 |
| Gemini 3.1 Pro | 96.8% | 0.972 / 0.989 | 0.914 / 0.935 | 71.99 / 74.37 |
| Qwen3.5-2B | 18.4% | 0.262 / 0.862 | 0.140 / 0.579 | 11.07 / 60.15 |
| Qwen3.5-9B | 19.4% | 0.244 / 0.848 | 0.148 / 0.580 | 11.34 / 58.46 |
| Qwen3.5-27B | 51.0% | 0.626 / 0.940 | 0.501 / 0.772 | 33.16 / 65.03 |
| Qwen3.5-397B-A17B | 84.0% | 0.861 / 0.947 | 0.726 / 0.800 | 53.52 / 63.71 |

## Exhibit 6 — Per-tier breakdown (complexity quartiles)

Point estimates (per-tier cells are not bootstrapped). chrF++ is macro.

### Tier 1 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 97.6% | 0.961 / 0.972 | 0.945 / 0.952 | 64.05 / 65.62 |
| Claude Opus 4.6 | 98.4% | 0.972 / 0.985 | 0.929 / 0.948 | 70.13 / 71.27 |
| Gemini 3.1 Pro | 98.4% | 0.989 / 0.996 | 0.990 / 0.994 | 76.83 / 78.08 |
| Qwen3.5-2B | 32.0% | 0.456 / 0.853 | 0.350 / 0.635 | 19.73 / 61.67 |
| Qwen3.5-9B | 48.8% | 0.554 / 0.851 | 0.228 / 0.403 | 30.32 / 62.14 |
| Qwen3.5-27B | 74.0% | 0.806 / 0.957 | 0.697 / 0.841 | 49.39 / 66.75 |
| Qwen3.5-397B-A17B | 87.2% | 0.845 / 0.900 | 0.842 / 0.882 | 54.41 / 62.40 |

### Tier 2 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 94.8% | 0.955 / 0.985 | 0.918 / 0.943 | 64.79 / 68.34 |
| Claude Opus 4.6 | 94.0% | 0.960 / 0.990 | 0.838 / 0.873 | 66.99 / 71.26 |
| Gemini 3.1 Pro | 98.0% | 0.991 / 0.998 | 0.974 / 0.985 | 78.24 / 79.84 |
| Qwen3.5-2B | 21.2% | 0.312 / 0.876 | 0.186 / 0.525 | 13.20 / 62.28 |
| Qwen3.5-9B | 42.4% | 0.524 / 0.856 | 0.269 / 0.522 | 26.86 / 63.36 |
| Qwen3.5-27B | 70.4% | 0.800 / 0.977 | 0.661 / 0.819 | 47.60 / 67.62 |
| Qwen3.5-397B-A17B | 81.6% | 0.839 / 0.933 | 0.805 / 0.877 | 50.78 / 62.23 |

### Tier 3 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 93.2% | 0.936 / 0.968 | 0.859 / 0.889 | 62.80 / 67.38 |
| Claude Opus 4.6 | 90.8% | 0.943 / 0.984 | 0.746 / 0.780 | 63.31 / 69.73 |
| Gemini 3.1 Pro | 96.4% | 0.973 / 0.987 | 0.944 / 0.959 | 74.36 / 77.14 |
| Qwen3.5-2B | 17.6% | 0.284 / 0.922 | 0.131 / 0.440 | 10.96 / 62.28 |
| Qwen3.5-9B | 42.0% | 0.516 / 0.861 | 0.245 / 0.520 | 26.84 / 63.91 |
| Qwen3.5-27B | 59.6% | 0.733 / 0.964 | 0.546 / 0.800 | 41.74 / 70.04 |
| Qwen3.5-397B-A17B | 74.8% | 0.825 / 0.954 | 0.729 / 0.835 | 45.94 / 61.42 |

### Tier 4 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 88.4% | 0.872 / 0.935 | 0.650 / 0.703 | 59.29 / 67.07 |
| Claude Opus 4.6 | 93.2% | 0.907 / 0.939 | 0.602 / 0.625 | 62.31 / 66.85 |
| Gemini 3.1 Pro | 96.0% | 0.947 / 0.971 | 0.830 / 0.853 | 72.67 / 75.69 |
| Qwen3.5-2B | 6.0% | 0.095 / 0.830 | 0.024 / 0.231 | 3.62 / 60.37 |
| Qwen3.5-9B | 31.2% | 0.412 / 0.898 | 0.143 / 0.427 | 19.31 / 61.89 |
| Qwen3.5-27B | 54.4% | 0.630 / 0.911 | 0.404 / 0.631 | 37.14 / 68.28 |
| Qwen3.5-397B-A17B | 71.2% | 0.735 / 0.908 | 0.543 / 0.631 | 45.79 / 64.31 |

### Per-tier image crowding (degradation context)

Content_lines per megapixel after the 1568px resize (pooled), the legibility descriptor accompanying the degradation curve — it rises monotonically with tier (harder diagrams are denser).

| Tier | content_lines / MP |
|---|---|
| 1 | 8.74 |
| 2 | 13.25 |
| 3 | 21.12 |
| 4 | 50.09 |

## Exhibit 7 — Run-level: token footprint & provenance

token totals over all cells incl. failures; output already includes reasoning (no double count); Gemini output = candidates + thoughts. Dollar pricing out of scope.

### Token totals (all 1000 cells incl. failures)

| Model | input (M) | output (M) | reasoning (M) | total (M) |
|---|---|---|---|---|
| GPT-5.2 | 1.631 | 0.331 | 0.000 | 1.962 |
| Claude Opus 4.6 | 1.415 | 0.339 | 0.000 | 1.754 |
| Gemini 3.1 Pro | 1.165 | 0.297 | 0.000 | 1.462 |
| Qwen3.5-2B | 1.387 | 2.078 | 0.000 | 3.465 |
| Qwen3.5-9B | 1.387 | 1.204 | 0.000 | 2.591 |
| Qwen3.5-27B | 1.387 | 0.783 | 0.000 | 2.170 |
| Qwen3.5-397B-A17B | 1.386 | 0.679 | 0.000 | 2.066 |

### Reproducibility provenance

| Model | snapshot | provider | non-thinking config | max_tokens | leak |
|---|---|---|---|---|---|
| GPT-5.2 | `gpt-5.2-2025-12-11` | openai | reasoning_effort=none | 5376 | 0 |
| Claude Opus 4.6 | `claude-opus-4-6` | openai | thinking={'type': 'disabled'} | 5376 | 0 |
| Gemini 3.1 Pro | `gemini-3.1-pro-preview` | gemini | thinkingConfig={'thinkingLevel': 'low'} | 5376 | 0 |
| Qwen3.5-2B | `Qwen/Qwen3.5-2B` | openai | chat_template_kwargs={'enable_thinking': False} | 5376 | 0 |
| Qwen3.5-9B | `Qwen/Qwen3.5-9B` | openai | chat_template_kwargs={'enable_thinking': False} | 5376 | 0 |
| Qwen3.5-27B | `Qwen/Qwen3.5-27B` | openai | chat_template_kwargs={'enable_thinking': False} | 5376 | 0 |
| Qwen3.5-397B-A17B | `qwen/qwen3.5-397b-a17b` | openai | provider={'only': ['alibaba'], 'allow_fallbacks': False}; reasoning={'enabled': False} | 5376 | 0 |

## Exhibit 8 — Failure-case coverage (feeds the qualitative review)

The stratified failure index holds **213** cases (`--per-cell 2`, seed 20260614) across outcome classes provider_drop, compile_fail, compiled_low_structural. Full records — GT, prediction, CSR error, structural deltas — are in `failure_index.{md,json,csv}`; the coded error sample is written up in `analysis/error_analysis.md`. Coverage (available → sampled):

| Model | provider_drop | compile_fail | compiled_low_structural |
|---|---|---|---|
| gpt-5.2 | 1→1 | 64→16 | 83→15 |
| claude-opus-4-6 | — | 59→14 | 117→16 |
| gemini-3.1-pro | — | 28→13 | 31→10 |
| qwen3.5-2b | — | 808→16 | 96→16 |
| qwen3.5-9b | — | 589→16 | 188→16 |
| qwen3.5-27b | — | 354→16 | 114→16 |
| qwen3.5-397b-a17b | — | 213→16 | 111→16 |

## Results-narrative skeleton (author expands into prose)

_Headed bullets with the artifact numbers pre-filled; this is scaffolding, not paper prose. The qualitative error write-up is in `analysis/error_analysis.md` (the coded error sample)._

**R1 — Frontier reference points.** Compilation is near-saturated across the three flagships; Gemini 3.1 Pro leads on CSR (97.2%). They anchor the upper bound; report them as fixed points, not as a ranked contest (Exhibit 1A, Fig. frontier_bars).

**R2 — Open-ladder scaling (dense).** CSR rises monotonically with dense scale: Qwen3.5-2B 19.2% → Qwen3.5-27B 64.6%; Element/Relationship F1 track it (Exhibit 1B, Fig. scaling_curve). The compiled-only overlay stays high throughout — the gain is in *compiling at all*, not in the quality of what compiles.

**R4 — Selective-failure bias (population gap).** The compiled-only − all-1000 Element-F1 gap is largest for the weakest rung (Qwen3.5-2B, +0.636 at CSR 19.2%) and negligible at the frontier (Gemini 3.1 Pro, +0.016). Report the honest all-1000 column as the headline (Exhibit 3).

**R5 — Structural failure modes (per-relation).** Per-relation F1 separates easy from hard edges; read the per-relation table for which relations each arm misses, with CIs (Exhibit 4, Fig. per_relation_f1). The qualitative error categories draw on `failure_index`.

**R6 — Complexity degradation (per-tier).** Every metric declines from tier 1 to tier 4 across the panel; the weak rungs fall fastest (Exhibit 6, Fig. breakdown_by_tier). Image crowding rises in lockstep (content_lines/MP: T1 8.7 → T4 50.1), the legibility context for the drop.

**R7 — Token footprint.** Per-model input/output token totals over all 1000 cells back the deployment/fine-tuning cost argument (Exhibit 7); the open arm ran under flat-rate billing, so dollar figures are omitted by design (token volumes stand).

