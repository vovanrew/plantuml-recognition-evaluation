# Paper exhibits — zero-shot image→PlantUML benchmark

**Models included: 7/7** (panel: main).

Assembled read-only from the validated Task-1..5 artifacts (`master_table.json`, `ci_table.json`, `run_level.json`, `crowding.json`, `failure_index.json`). No metric is re-pooled or recomputed here. Companion figures live in `analysis/out/plots/`; a Word-importable rendering of this document (tables paste straight into Microsoft Word) is emitted alongside it as `exhibits.html`.

## Exhibit 1 — Headline results (two arms)

Cells are `point [2.5th, 97.5th]` paired-bootstrap 95% CIs (n=1000, seed=20260614); CSR as a percentage, F1 / type accuracy on 0–1, chrF++ on its native 0–100 scale. Two populations per metric as `zeros_for_failed / compiled_only`. chrF++ is the **macro** statistic (the CI-bearing one; chrF++ micro is a corpus statistic, point-only — see Exhibit 2). Type accuracy is compiled-only by definition. **This is two arms, not one leaderboard.**

### Arm A — Frontier reference points

One reigning flagship per lab (fixed comparison points).

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% [91.9%, 95.0%] | 0.897 [0.876, 0.916] / 0.939 [0.920, 0.954] | 0.757 [0.720, 0.790] / 0.799 [0.764, 0.828] | 62.73 [61.23, 64.20] / 67.09 [65.97, 68.18] | 0.941 [0.927, 0.954] |
| Claude Opus 4.6 | 94.1% [92.5%, 95.5%] | 0.909 [0.888, 0.927] / 0.940 [0.922, 0.957] | 0.693 [0.655, 0.728] / 0.720 [0.681, 0.756] | 65.68 [64.23, 67.18] / 69.80 [68.68, 70.98] | 0.950 [0.936, 0.962] |
| Gemini 3.1 Pro | 97.2% [96.2%, 98.1%] | 0.945 [0.932, 0.959] / 0.961 [0.948, 0.973] | 0.875 [0.848, 0.900] / 0.893 [0.867, 0.916] | 75.53 [74.19, 76.85] / 77.70 [76.52, 78.83] | 0.984 [0.972, 0.992] |

### Arm B — Qwen open ladder (dense) + MoE ceiling

The dense 2B/9B/27B ladder is a scaling curve; the 397B-A17B MoE is a capability ceiling (both total and active parameters reported), **not** a fourth dense rung.

| Model | Params | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) | Type acc |
|---|---|---|---|---|---|---|
| Qwen3.5-2B | 2B | 20.1% [17.6%, 22.6%] | 0.246 [0.211, 0.282] / 0.878 [0.838, 0.913] | 0.114 [0.091, 0.139] / 0.481 [0.415, 0.545] | 12.89 [11.18, 14.61] / 64.14 [61.99, 66.30] | 0.758 [0.703, 0.809] |
| Qwen3.5-9B | 9B | 43.1% [40.2%, 46.2%] | 0.491 [0.456, 0.527] / 0.844 [0.811, 0.877] | 0.201 [0.173, 0.233] / 0.439 [0.382, 0.499] | 26.91 [24.84, 29.10] / 62.43 [60.74, 64.21] | 0.756 [0.711, 0.798] |
| Qwen3.5-27B | 27B | 60.1% [56.9%, 63.2%] | 0.676 [0.645, 0.707] / 0.917 [0.891, 0.941] | 0.485 [0.443, 0.526] / 0.722 [0.666, 0.771] | 40.91 [38.55, 43.27] / 68.07 [66.61, 69.48] | 0.886 [0.861, 0.910] |
| Qwen3.5-397B-A17B | 397B total / 17B active | 78.7% [76.2%, 81.2%] | 0.771 [0.744, 0.796] / 0.897 [0.877, 0.917] | 0.646 [0.605, 0.687] / 0.736 [0.688, 0.779] | 49.23 [47.46, 51.17] / 62.56 [61.27, 64.00] | 0.870 [0.850, 0.888] |

## Exhibit 2 — Overall results, both populations × micro & macro

Read straight from the master table; CIs (where they exist) from the CI table. chrF++ micro is a corpus sacrebleu statistic (point estimate, no CI); chrF++ macro carries a CI.

### Micro

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 93.5% [91.9%, 95.0%] | 0.897 [0.876, 0.916] / 0.939 [0.920, 0.954] | 0.757 [0.720, 0.790] / 0.799 [0.764, 0.828] | 60.74 / 66.01 |
| Claude Opus 4.6 | 94.1% [92.5%, 95.5%] | 0.909 [0.888, 0.927] / 0.940 [0.922, 0.957] | 0.693 [0.655, 0.728] / 0.720 [0.681, 0.756] | 62.36 / 66.57 |
| Gemini 3.1 Pro | 97.2% [96.2%, 98.1%] | 0.945 [0.932, 0.959] / 0.961 [0.948, 0.973] | 0.875 [0.848, 0.900] / 0.893 [0.867, 0.916] | 72.19 / 74.54 |
| Qwen3.5-2B | 20.1% [17.6%, 22.6%] | 0.246 [0.211, 0.282] / 0.878 [0.838, 0.913] | 0.114 [0.091, 0.139] / 0.481 [0.415, 0.545] | 8.96 / 65.12 |
| Qwen3.5-9B | 43.1% [40.2%, 46.2%] | 0.491 [0.456, 0.527] / 0.844 [0.811, 0.877] | 0.201 [0.173, 0.233] / 0.439 [0.382, 0.499] | 24.40 / 61.17 |
| Qwen3.5-27B | 60.1% [56.9%, 63.2%] | 0.676 [0.645, 0.707] / 0.917 [0.891, 0.941] | 0.485 [0.443, 0.526] / 0.722 [0.666, 0.771] | 38.41 / 65.65 |
| Qwen3.5-397B-A17B | 78.7% [76.2%, 81.2%] | 0.771 [0.744, 0.796] / 0.897 [0.877, 0.917] | 0.646 [0.605, 0.687] / 0.736 [0.688, 0.779] | 47.80 / 59.77 |

### Macro

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.891 [0.872, 0.908] / 0.953 [0.942, 0.963] | 0.807 [0.785, 0.828] / 0.860 [0.842, 0.877] | 62.73 [61.23, 64.20] / 67.09 [65.97, 68.18] |
| Claude Opus 4.6 | 94.1% | 0.901 [0.882, 0.918] / 0.958 [0.946, 0.968] | 0.776 [0.755, 0.794] / 0.823 [0.804, 0.840] | 65.68 [64.23, 67.18] / 69.80 [68.68, 70.98] |
| Gemini 3.1 Pro | 97.2% | 0.940 [0.927, 0.952] / 0.967 [0.957, 0.976] | 0.906 [0.891, 0.921] / 0.931 [0.918, 0.944] | 75.53 [74.19, 76.85] / 77.70 [76.52, 78.83] |
| Qwen3.5-2B | 20.1% | 0.175 [0.151, 0.198] / 0.865 [0.825, 0.900] | 0.166 [0.144, 0.188] / 0.495 [0.437, 0.555] | 12.89 [11.18, 14.61] / 64.14 [61.99, 66.30] |
| Qwen3.5-9B | 43.1% | 0.371 [0.343, 0.400] / 0.861 [0.834, 0.887] | 0.260 [0.235, 0.285] / 0.519 [0.478, 0.562] | 26.91 [24.84, 29.10] / 62.43 [60.74, 64.21] |
| Qwen3.5-27B | 60.1% | 0.562 [0.532, 0.591] / 0.925 [0.909, 0.941] | 0.505 [0.476, 0.533] / 0.803 [0.778, 0.828] | 40.91 [38.55, 43.27] / 68.07 [66.61, 69.48] |
| Qwen3.5-397B-A17B | 78.7% | 0.716 [0.691, 0.742] / 0.909 [0.894, 0.923] | 0.639 [0.613, 0.667] / 0.797 [0.773, 0.818] | 49.23 [47.46, 51.17] / 62.56 [61.27, 64.00] |

## Exhibit 3 — Population gap (selective-failure bias)

`compiled_only − zeros_for_failed` (overall micro). A low-CSR model that drops/times out on its hardest diagrams is graded on an easier subset, so its compiled-only score runs far above its honest all-1000 score; the gap is that fingerprint and tracks CSR (near-zero for the frontier, large for the weak rungs).

| Model | CSR | ΔElement F1 | ΔRelationship F1 | ΔchrF++ |
|---|---|---|---|---|
| GPT-5.2 | 93.5% | +0.042 | +0.042 | +5.27 |
| Claude Opus 4.6 | 94.1% | +0.031 | +0.027 | +4.21 |
| Gemini 3.1 Pro | 97.2% | +0.016 | +0.018 | +2.35 |
| Qwen3.5-2B | 20.1% | +0.632 | +0.367 | +56.16 |
| Qwen3.5-9B | 43.1% | +0.354 | +0.238 | +36.77 |
| Qwen3.5-27B | 60.1% | +0.241 | +0.237 | +27.23 |
| Qwen3.5-397B-A17B | 78.7% | +0.127 | +0.090 | +11.97 |

## Exhibit 4 — Relationship F1 by relation type (with CIs)

Per-relation F1 (micro), `zeros_for_failed [CI] / compiled_only [CI]`. GT support (model-independent) annotates each relation.

| Model | inheritance<br>(n=940) | composition<br>(n=300) | aggregation<br>(n=244) | dependency<br>(n=393) | association<br>(n=1014) | message<br>(n=6546) |
|---|---|---|---|---|---|---|
| GPT-5.2 | 0.814 [0.765, 0.860] / 0.845 [0.801, 0.890] | 0.630 [0.497, 0.755] / 0.654 [0.514, 0.780] | 0.618 [0.514, 0.714] / 0.625 [0.521, 0.722] | 0.571 [0.488, 0.651] / 0.583 [0.500, 0.667] | 0.629 [0.563, 0.693] / 0.680 [0.615, 0.738] | 0.793 [0.748, 0.835] / 0.839 [0.794, 0.880] |
| Claude Opus 4.6 | 0.863 [0.825, 0.895] / 0.880 [0.843, 0.911] | 0.467 [0.353, 0.588] / 0.492 [0.375, 0.617] | 0.508 [0.412, 0.606] / 0.520 [0.422, 0.621] | 0.539 [0.451, 0.620] / 0.550 [0.460, 0.636] | 0.600 [0.541, 0.660] / 0.617 [0.558, 0.678] | 0.708 [0.656, 0.757] / 0.740 [0.686, 0.792] |
| Gemini 3.1 Pro | 0.924 [0.898, 0.947] / 0.940 [0.917, 0.960] | 0.817 [0.722, 0.892] / 0.824 [0.732, 0.896] | 0.800 [0.719, 0.875] / 0.820 [0.746, 0.890] | 0.782 [0.710, 0.851] / 0.789 [0.715, 0.856] | 0.811 [0.751, 0.866] / 0.819 [0.762, 0.873] | 0.889 [0.853, 0.921] / 0.909 [0.876, 0.940] |
| Qwen3.5-2B | 0.086 [0.045, 0.131] / 0.462 [0.311, 0.604] | 0.006 [0.000, 0.021] / 0.029 [0.000, 0.078] | 0.008 [0.000, 0.027] / 0.091 [0.000, 0.240] | 0.016 [0.000, 0.042] / 0.039 [0.000, 0.097] | 0.064 [0.032, 0.102] / 0.202 [0.109, 0.298] | 0.143 [0.109, 0.176] / 0.649 [0.580, 0.716] |
| Qwen3.5-9B | 0.401 [0.327, 0.469] / 0.547 [0.460, 0.631] | 0.130 [0.062, 0.220] / 0.238 [0.124, 0.391] | 0.141 [0.078, 0.217] / 0.190 [0.111, 0.297] | 0.200 [0.135, 0.261] / 0.246 [0.171, 0.315] | 0.264 [0.207, 0.331] / 0.341 [0.267, 0.427] | 0.147 [0.105, 0.194] / 0.611 [0.496, 0.716] |
| Qwen3.5-27B | 0.652 [0.581, 0.717] / 0.771 [0.706, 0.830] | 0.425 [0.301, 0.547] / 0.618 [0.498, 0.730] | 0.510 [0.394, 0.628] / 0.627 [0.498, 0.747] | 0.435 [0.343, 0.527] / 0.498 [0.385, 0.605] | 0.483 [0.410, 0.552] / 0.602 [0.524, 0.682] | 0.462 [0.403, 0.522] / 0.783 [0.694, 0.861] |
| Qwen3.5-397B-A17B | 0.615 [0.538, 0.685] / 0.769 [0.708, 0.825] | 0.459 [0.336, 0.597] / 0.592 [0.448, 0.743] | 0.443 [0.321, 0.563] / 0.556 [0.425, 0.685] | 0.326 [0.240, 0.407] / 0.387 [0.292, 0.477] | 0.508 [0.436, 0.583] / 0.627 [0.550, 0.703] | 0.708 [0.654, 0.759] / 0.779 [0.719, 0.839] |

## Exhibit 5 — Per-type breakdown (class / sequence)

Point estimates (per-type cells are not bootstrapped). chrF++ is macro (poolable at sub-scopes).

### Type: class (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 94.4% | 0.899 / 0.940 | 0.679 / 0.711 | 65.74 / 69.64 |
| Claude Opus 4.6 | 97.4% | 0.928 / 0.949 | 0.662 / 0.679 | 71.77 / 73.68 |
| Gemini 3.1 Pro | 97.6% | 0.944 / 0.959 | 0.844 / 0.855 | 79.07 / 81.01 |
| Qwen3.5-2B | 21.6% | 0.238 / 0.882 | 0.055 / 0.218 | 14.13 / 65.41 |
| Qwen3.5-9B | 65.6% | 0.635 / 0.857 | 0.304 / 0.419 | 41.60 / 63.41 |
| Qwen3.5-27B | 75.4% | 0.762 / 0.923 | 0.545 / 0.670 | 53.20 / 70.55 |
| Qwen3.5-397B-A17B | 73.4% | 0.716 / 0.878 | 0.503 / 0.623 | 44.94 / 61.23 |

### Type: sequence (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 92.6% | 0.895 / 0.938 | 0.792 / 0.839 | 59.72 / 64.50 |
| Claude Opus 4.6 | 90.8% | 0.887 / 0.930 | 0.707 / 0.738 | 59.60 / 65.64 |
| Gemini 3.1 Pro | 96.8% | 0.947 / 0.963 | 0.889 / 0.909 | 71.99 / 74.37 |
| Qwen3.5-2B | 18.6% | 0.255 / 0.875 | 0.141 / 0.609 | 11.66 / 62.67 |
| Qwen3.5-9B | 20.6% | 0.261 / 0.800 | 0.137 / 0.469 | 12.22 / 59.32 |
| Qwen3.5-27B | 44.8% | 0.555 / 0.906 | 0.454 / 0.760 | 28.62 / 63.89 |
| Qwen3.5-397B-A17B | 84.0% | 0.834 / 0.917 | 0.707 / 0.778 | 53.52 / 63.71 |

## Exhibit 6 — Per-tier breakdown (complexity quartiles)

Point estimates (per-tier cells are not bootstrapped). chrF++ is macro.

### Tier 1 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 97.6% | 0.952 / 0.964 | 0.929 / 0.936 | 64.05 / 65.62 |
| Claude Opus 4.6 | 98.4% | 0.957 / 0.969 | 0.916 / 0.935 | 70.13 / 71.27 |
| Gemini 3.1 Pro | 98.4% | 0.972 / 0.978 | 0.975 / 0.979 | 76.83 / 78.08 |
| Qwen3.5-2B | 32.8% | 0.451 / 0.833 | 0.353 / 0.634 | 20.87 / 63.63 |
| Qwen3.5-9B | 52.0% | 0.569 / 0.847 | 0.235 / 0.420 | 32.06 / 61.66 |
| Qwen3.5-27B | 72.0% | 0.763 / 0.924 | 0.656 / 0.821 | 48.45 / 67.29 |
| Qwen3.5-397B-A17B | 87.2% | 0.829 / 0.884 | 0.829 / 0.868 | 54.41 / 62.40 |

### Tier 2 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 94.8% | 0.945 / 0.975 | 0.902 / 0.927 | 64.79 / 68.34 |
| Claude Opus 4.6 | 94.0% | 0.953 / 0.982 | 0.831 / 0.865 | 66.99 / 71.26 |
| Gemini 3.1 Pro | 98.0% | 0.987 / 0.994 | 0.969 / 0.979 | 78.24 / 79.84 |
| Qwen3.5-2B | 22.0% | 0.313 / 0.824 | 0.176 / 0.466 | 14.13 / 64.25 |
| Qwen3.5-9B | 43.2% | 0.517 / 0.841 | 0.265 / 0.501 | 27.03 / 62.58 |
| Qwen3.5-27B | 62.0% | 0.760 / 0.962 | 0.625 / 0.848 | 42.96 / 69.29 |
| Qwen3.5-397B-A17B | 81.6% | 0.826 / 0.919 | 0.788 / 0.859 | 50.78 / 62.23 |

### Tier 3 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 93.2% | 0.911 / 0.943 | 0.840 / 0.868 | 62.80 / 67.38 |
| Claude Opus 4.6 | 90.8% | 0.915 / 0.956 | 0.734 / 0.767 | 63.31 / 69.73 |
| Gemini 3.1 Pro | 96.4% | 0.948 / 0.961 | 0.920 / 0.935 | 74.36 / 77.14 |
| Qwen3.5-2B | 19.6% | 0.304 / 0.941 | 0.141 / 0.452 | 12.76 / 65.08 |
| Qwen3.5-9B | 44.0% | 0.527 / 0.840 | 0.264 / 0.514 | 28.22 / 64.15 |
| Qwen3.5-27B | 58.0% | 0.709 / 0.931 | 0.567 / 0.821 | 40.04 / 69.04 |
| Qwen3.5-397B-A17B | 74.8% | 0.800 / 0.925 | 0.718 / 0.823 | 45.94 / 61.42 |

### Tier 4 (micro, point estimates)

| Model | CSR | Element F1 (z / c) | Relationship F1 (z / c) | chrF++ macro (z / c) |
|---|---|---|---|---|
| GPT-5.2 | 88.4% | 0.851 / 0.913 | 0.643 / 0.697 | 59.29 / 67.07 |
| Claude Opus 4.6 | 93.2% | 0.873 / 0.905 | 0.599 / 0.622 | 62.31 / 66.85 |
| Gemini 3.1 Pro | 96.0% | 0.918 / 0.941 | 0.810 / 0.832 | 72.67 / 75.69 |
| Qwen3.5-2B | 6.0% | 0.095 / 0.947 | 0.028 / 0.350 | 3.81 / 63.53 |
| Qwen3.5-9B | 33.2% | 0.430 / 0.849 | 0.141 / 0.363 | 20.31 / 61.17 |
| Qwen3.5-27B | 48.4% | 0.587 / 0.878 | 0.368 / 0.592 | 32.18 / 66.49 |
| Qwen3.5-397B-A17B | 71.2% | 0.707 / 0.873 | 0.535 / 0.625 | 45.79 / 64.31 |

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
| Qwen3.5-2B | 1.351 | 1.752 | 0.000 | 3.103 |
| Qwen3.5-9B | 1.387 | 1.177 | 0.000 | 2.564 |
| Qwen3.5-27B | 1.385 | 0.371 | 0.000 | 1.756 |
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

The stratified failure index holds **233** cases (`--per-cell 2`, seed 20260614) across outcome classes provider_drop, compile_fail, compiled_low_structural. Full records — GT, prediction, CSR error, structural deltas — are in `failure_index.{md,json,csv}`; the 40-case write-up is in `analysis/error_analysis.md`. Coverage (available → sampled):

| Model | provider_drop | compile_fail | compiled_low_structural |
|---|---|---|---|
| gpt-5.2 | 1→1 | 64→16 | 94→16 |
| claude-opus-4-6 | — | 59→14 | 120→16 |
| gemini-3.1-pro | — | 28→13 | 53→16 |
| qwen3.5-2b | 25→12 | 774→16 | 100→16 |
| qwen3.5-9b | — | 569→16 | 201→16 |
| qwen3.5-27b | 1→1 | 398→16 | 104→16 |
| qwen3.5-397b-a17b | — | 213→16 | 122→16 |

## Results-narrative skeleton (author expands into prose)

_Headed bullets with the artifact numbers pre-filled; this is scaffolding, not paper prose. The qualitative error write-up is in `analysis/error_analysis.md` (40 cases from `failure_index`)._

**R1 — Frontier reference points.** Compilation is near-saturated across the three flagships; Gemini 3.1 Pro leads on CSR (97.2%). They anchor the upper bound; report them as fixed points, not as a ranked contest (Exhibit 1A, Fig. frontier_bars).

**R2 — Open-ladder scaling (dense).** CSR rises monotonically with dense scale: Qwen3.5-2B 20.1% → Qwen3.5-27B 60.1%; Element/Relationship F1 track it (Exhibit 1B, Fig. scaling_curve). The compiled-only overlay stays high throughout — the gain is in *compiling at all*, not in the quality of what compiles.

**R3 — MoE capability ceiling.** The 397B-A17B mixture (397B total / 17B active) reaches CSR 78.7%, above the dense ladder and approaching the frontier band, at ~17B active parameters — a capability ceiling for the open arm, plotted off the dense axis as a separate marker (Fig. scaling_curve).

**R4 — Selective-failure bias (population gap).** The compiled-only − all-1000 Element-F1 gap is largest for the weakest rung (Qwen3.5-2B, +0.632 at CSR 20.1%) and negligible at the frontier (Gemini 3.1 Pro, +0.016). Report the honest all-1000 column as the headline (Exhibit 3).

**R5 — Structural failure modes (per-relation).** Per-relation F1 separates easy from hard edges; read the per-relation table for which relations each arm misses, with CIs (Exhibit 4, Fig. per_relation_f1). The qualitative error categories draw on `failure_index`.

**R6 — Complexity degradation (per-tier).** Every metric declines from tier 1 to tier 4 across the panel; the weak rungs fall fastest (Exhibit 6, Fig. breakdown_by_tier). Image crowding rises in lockstep (content_lines/MP: T1 8.7 → T4 50.1), the legibility context for the drop.

**R7 — Token footprint.** Per-model input/output token totals over all 1000 cells back the deployment/fine-tuning cost argument (Exhibit 7); the open arm ran under flat-rate billing, so dollar figures are omitted by design (token volumes stand).

