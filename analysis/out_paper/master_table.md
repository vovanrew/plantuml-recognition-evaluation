# Master table — zero-shot image→PlantUML benchmark

**Models included: 7/7** (panel label: main)

Two populations reported side by side as `zeros_for_failed / compiled_only`: `zeros_for_failed` scores all diagrams (non-compiled = 0); `compiled_only` is over compiled cells, with CSR reported separately. chrF++ values in the headline tables are micro (corpus sacrebleu, available at the overall scope only); the macro tables and JSON carry the poolable chrF++ macro for every scope. Type accuracy is the `compiled_only` population by definition.

### Overall (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.916 / 0.958 | 0.770 / 0.812 | 60.74 / 66.01 | 0.941 |
| Claude Opus 4.6 | 94.1% | 0.934 / 0.966 | 0.700 / 0.728 | 62.36 / 66.57 | 0.951 |
| Gemini 3.1 Pro | 97.2% | 0.967 / 0.983 | 0.894 / 0.912 | 72.19 / 74.54 | 0.984 |
| Qwen3.5-2B | 19.2% | 0.239 / 0.875 | 0.110 / 0.461 | 8.79 / 61.72 | 0.757 |
| Qwen3.5-9B | 41.1% | 0.481 / 0.871 | 0.198 / 0.470 | 22.88 / 62.22 | 0.774 |
| Qwen3.5-27B | 64.6% | 0.713 / 0.946 | 0.507 / 0.730 | 40.85 / 66.32 | 0.889 |
| Qwen3.5-397B-A17B | 78.7% | 0.794 / 0.924 | 0.657 / 0.746 | 47.80 / 59.77 | 0.871 |

### Overall (macro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.908 / 0.971 | 0.817 / 0.870 | 62.73 / 67.09 | 0.941 |
| Claude Opus 4.6 | 94.1% | 0.923 / 0.981 | 0.778 / 0.826 | 65.68 / 69.80 | 0.951 |
| Gemini 3.1 Pro | 97.2% | 0.961 / 0.989 | 0.924 / 0.949 | 75.53 / 77.70 | 0.984 |
| Qwen3.5-2B | 19.2% | 0.169 / 0.880 | 0.174 / 0.491 | 11.88 / 61.87 | 0.757 |
| Qwen3.5-9B | 41.1% | 0.365 / 0.888 | 0.265 / 0.536 | 25.83 / 62.86 | 0.774 |
| Qwen3.5-27B | 64.6% | 0.619 / 0.958 | 0.533 / 0.801 | 43.97 / 68.07 | 0.889 |
| Qwen3.5-397B-A17B | 78.7% | 0.737 / 0.936 | 0.647 / 0.805 | 49.23 / 62.56 | 0.871 |

### Population gap (compiled-only − all-1000, micro)

The `compiled_only` minus `zeros_for_failed` gap per metric — the headline measure of how much a model's apparent quality rests on selective failure. A model that drops/times out on its hard diagrams is graded on an easier subset, so its `compiled_only` score runs far above its honest all-1000 score; a large gap is that fingerprint (it tracks the answer rate / CSR).

| Model | CSR | Element F1 (all → cmp, Δ) | Relationship F1 (all → cmp, Δ) | chrF++ (all → cmp, Δ) |
|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.916 → 0.958 (+0.043) | 0.770 → 0.812 (+0.042) | 60.74 → 66.01 (+5.27) |
| Claude Opus 4.6 | 94.1% | 0.934 → 0.966 (+0.032) | 0.700 → 0.728 (+0.027) | 62.36 → 66.57 (+4.21) |
| Gemini 3.1 Pro | 97.2% | 0.967 → 0.983 (+0.016) | 0.894 → 0.912 (+0.018) | 72.19 → 74.54 (+2.35) |
| Qwen3.5-2B | 19.2% | 0.239 → 0.875 (+0.636) | 0.110 → 0.461 (+0.351) | 8.79 → 61.72 (+52.93) |
| Qwen3.5-9B | 41.1% | 0.481 → 0.871 (+0.390) | 0.198 → 0.470 (+0.273) | 22.88 → 62.22 (+39.34) |
| Qwen3.5-27B | 64.6% | 0.713 → 0.946 (+0.233) | 0.507 → 0.730 (+0.223) | 40.85 → 66.32 (+25.47) |
| Qwen3.5-397B-A17B | 78.7% | 0.794 → 0.924 (+0.130) | 0.657 → 0.746 (+0.089) | 47.80 → 59.77 (+11.97) |

### Relationship F1 by relation type (read-through)

**GPT-5.2** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.820 / 0.851 | 940 / 875 |
| composition | 0.634 / 0.658 | 300 / 282 |
| aggregation | 0.618 / 0.625 | 244 / 239 |
| dependency | 0.618 / 0.630 | 375 / 358 |
| association | 0.549 / 0.594 | 862 / 739 |
| message | 0.814 / 0.862 | 6544 / 5866 |

**Claude Opus 4.6** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.870 / 0.886 | 940 / 906 |
| composition | 0.467 / 0.492 | 300 / 276 |
| aggregation | 0.508 / 0.520 | 244 / 235 |
| dependency | 0.581 / 0.592 | 375 / 360 |
| association | 0.461 / 0.476 | 862 / 805 |
| message | 0.732 / 0.765 | 6544 / 6009 |

**Gemini 3.1 Pro** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.931 / 0.947 | 940 / 909 |
| composition | 0.820 / 0.828 | 300 / 295 |
| aggregation | 0.800 / 0.820 | 244 / 233 |
| dependency | 0.843 / 0.850 | 375 / 369 |
| association | 0.770 / 0.777 | 862 / 847 |
| message | 0.914 / 0.935 | 6544 / 6253 |

**Qwen3.5-2B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.076 / 0.388 | 940 / 119 |
| composition | 0.000 / 0.000 | 300 / 31 |
| aggregation | 0.008 / 0.125 | 244 / 15 |
| dependency | 0.013 / 0.029 | 375 / 55 |
| association | 0.036 / 0.134 | 862 / 99 |
| message | 0.141 / 0.605 | 6544 / 874 |

**Qwen3.5-9B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.381 / 0.526 | 940 / 541 |
| composition | 0.159 / 0.271 | 300 / 150 |
| aggregation | 0.160 / 0.253 | 244 / 134 |
| dependency | 0.223 / 0.283 | 375 / 175 |
| association | 0.223 / 0.299 | 862 / 440 |
| message | 0.155 / 0.707 | 6544 / 906 |

**Qwen3.5-27B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.665 / 0.790 | 940 / 682 |
| composition | 0.340 / 0.563 | 300 / 134 |
| aggregation | 0.470 / 0.578 | 244 / 172 |
| dependency | 0.535 / 0.647 | 375 / 255 |
| association | 0.372 / 0.464 | 862 / 557 |
| message | 0.509 / 0.792 | 6544 / 3114 |

**Qwen3.5-397B-A17B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.621 / 0.777 | 940 / 617 |
| composition | 0.463 / 0.598 | 300 / 199 |
| aggregation | 0.443 / 0.556 | 244 / 173 |
| dependency | 0.360 / 0.422 | 375 / 249 |
| association | 0.421 / 0.514 | 862 / 581 |
| message | 0.727 / 0.801 | 6544 / 5436 |

### Type accuracy by GT entity type (compiled_only, read-through)

**GPT-5.2** — pooled accuracy 0.941 (matched 5055, excluded 62, denominator 4993):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 138 | 0.841 |
| actor | 259 | 0.996 |
| annotation | 1 | 1.000 |
| boundary | 65 | 0.677 |
| class | 2246 | 0.975 |
| collections | 24 | 0.125 |
| control | 77 | 0.688 |
| database | 102 | 0.980 |
| entity | 82 | 0.280 |
| enum | 60 | 0.817 |
| interface | 230 | 0.965 |
| object | 1 | 0.000 |
| participant | 1704 | 0.963 |
| queue | 4 | 0.000 |

**Claude Opus 4.6** — pooled accuracy 0.951 (matched 5197, excluded 73, denominator 5124):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 143 | 0.979 |
| actor | 253 | 0.984 |
| annotation | 1 | 1.000 |
| boundary | 65 | 0.600 |
| class | 2325 | 0.989 |
| collections | 29 | 0.241 |
| control | 79 | 0.405 |
| database | 92 | 0.957 |
| entity | 89 | 0.494 |
| enum | 65 | 0.985 |
| interface | 239 | 0.900 |
| object | 7 | 0.000 |
| participant | 1730 | 0.979 |
| queue | 7 | 0.000 |

**Gemini 3.1 Pro** — pooled accuracy 0.984 (matched 5462, excluded 87, denominator 5375):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 141 | 0.972 |
| actor | 274 | 0.996 |
| annotation | 1 | 1.000 |
| boundary | 69 | 1.000 |
| class | 2393 | 0.986 |
| collections | 31 | 0.839 |
| control | 78 | 1.000 |
| database | 113 | 1.000 |
| entity | 111 | 0.775 |
| enum | 61 | 0.984 |
| interface | 224 | 0.982 |
| object | 9 | 0.000 |
| participant | 1862 | 0.999 |
| queue | 8 | 0.750 |

**Qwen3.5-2B** — pooled accuracy 0.757 (matched 806, excluded 0, denominator 806):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 20 | 0.000 |
| actor | 48 | 0.146 |
| boundary | 13 | 0.000 |
| class | 333 | 0.940 |
| collections | 1 | 0.000 |
| control | 13 | 0.000 |
| database | 15 | 0.000 |
| entity | 9 | 0.000 |
| enum | 11 | 0.000 |
| interface | 32 | 0.188 |
| participant | 309 | 0.919 |
| queue | 2 | 0.000 |

**Qwen3.5-9B** — pooled accuracy 0.774 (matched 1959, excluded 29, denominator 1930):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 89 | 0.022 |
| actor | 72 | 0.486 |
| annotation | 1 | 0.000 |
| boundary | 11 | 0.000 |
| class | 1265 | 0.953 |
| collections | 5 | 0.000 |
| control | 15 | 0.000 |
| database | 20 | 0.400 |
| entity | 27 | 0.037 |
| enum | 28 | 0.071 |
| interface | 149 | 0.557 |
| participant | 248 | 0.629 |

**Qwen3.5-27B** — pooled accuracy 0.889 (matched 3308, excluded 42, denominator 3266):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 123 | 0.480 |
| actor | 115 | 0.826 |
| annotation | 1 | 0.000 |
| boundary | 44 | 0.227 |
| class | 1679 | 0.985 |
| collections | 13 | 0.000 |
| control | 36 | 0.139 |
| database | 29 | 0.759 |
| entity | 62 | 0.339 |
| enum | 31 | 0.387 |
| interface | 168 | 0.857 |
| participant | 961 | 0.917 |
| queue | 4 | 0.250 |

**Qwen3.5-397B-A17B** — pooled accuracy 0.871 (matched 4092, excluded 51, denominator 4041):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 106 | 0.104 |
| actor | 238 | 0.983 |
| boundary | 60 | 0.233 |
| class | 1631 | 0.967 |
| collections | 25 | 0.040 |
| control | 62 | 0.500 |
| database | 75 | 0.813 |
| entity | 73 | 0.301 |
| enum | 35 | 0.257 |
| interface | 173 | 0.717 |
| object | 7 | 0.000 |
| participant | 1550 | 0.926 |
| queue | 6 | 0.167 |

## By diagram type

### Type: class (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 94.4% | 0.916 / 0.957 | 0.667 / 0.697 | — / — | 0.954 |
| Claude Opus 4.6 | 97.4% | 0.945 / 0.967 | 0.627 / 0.644 | — / — | 0.973 |
| Gemini 3.1 Pro | 97.6% | 0.962 / 0.978 | 0.845 / 0.856 | — / — | 0.974 |
| Qwen3.5-2B | 20.0% | 0.220 / 0.889 | 0.040 / 0.172 | — / — | 0.806 |
| Qwen3.5-9B | 62.8% | 0.627 / 0.877 | 0.284 / 0.402 | — / — | 0.834 |
| Qwen3.5-27B | 78.2% | 0.777 / 0.949 | 0.522 / 0.657 | — / — | 0.928 |
| Qwen3.5-397B-A17B | 73.4% | 0.735 / 0.901 | 0.484 / 0.595 | — / — | 0.875 |

### Type: sequence (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 92.6% | 0.915 / 0.959 | 0.814 / 0.861 | — / — | 0.927 |
| Claude Opus 4.6 | 90.8% | 0.920 / 0.965 | 0.731 / 0.764 | — / — | 0.924 |
| Gemini 3.1 Pro | 96.8% | 0.972 / 0.989 | 0.914 / 0.935 | — / — | 0.996 |
| Qwen3.5-2B | 18.4% | 0.262 / 0.862 | 0.140 / 0.579 | — / — | 0.710 |
| Qwen3.5-9B | 19.4% | 0.244 / 0.848 | 0.148 / 0.580 | — / — | 0.528 |
| Qwen3.5-27B | 51.0% | 0.626 / 0.940 | 0.501 / 0.772 | — / — | 0.825 |
| Qwen3.5-397B-A17B | 84.0% | 0.861 / 0.947 | 0.726 / 0.800 | — / — | 0.867 |

## By tier

### Tier 1 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 97.6% | 0.961 / 0.972 | 0.945 / 0.952 | — / — | 0.935 |
| Claude Opus 4.6 | 98.4% | 0.972 / 0.985 | 0.929 / 0.948 | — / — | 0.975 |
| Gemini 3.1 Pro | 98.4% | 0.989 / 0.996 | 0.990 / 0.994 | — / — | 0.997 |
| Qwen3.5-2B | 32.0% | 0.456 / 0.853 | 0.350 / 0.635 | — / — | 0.789 |
| Qwen3.5-9B | 48.8% | 0.554 / 0.851 | 0.228 / 0.403 | — / — | 0.691 |
| Qwen3.5-27B | 74.0% | 0.806 / 0.957 | 0.697 / 0.841 | — / — | 0.875 |
| Qwen3.5-397B-A17B | 87.2% | 0.845 / 0.900 | 0.842 / 0.882 | — / — | 0.856 |

### Tier 2 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 94.8% | 0.955 / 0.985 | 0.918 / 0.943 | — / — | 0.959 |
| Claude Opus 4.6 | 94.0% | 0.960 / 0.990 | 0.838 / 0.873 | — / — | 0.966 |
| Gemini 3.1 Pro | 98.0% | 0.991 / 0.998 | 0.974 / 0.985 | — / — | 0.994 |
| Qwen3.5-2B | 21.2% | 0.312 / 0.876 | 0.186 / 0.525 | — / — | 0.769 |
| Qwen3.5-9B | 42.4% | 0.524 / 0.856 | 0.269 / 0.522 | — / — | 0.759 |
| Qwen3.5-27B | 70.4% | 0.800 / 0.977 | 0.661 / 0.819 | — / — | 0.861 |
| Qwen3.5-397B-A17B | 81.6% | 0.839 / 0.933 | 0.805 / 0.877 | — / — | 0.868 |

### Tier 3 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.2% | 0.936 / 0.968 | 0.859 / 0.889 | — / — | 0.929 |
| Claude Opus 4.6 | 90.8% | 0.943 / 0.984 | 0.746 / 0.780 | — / — | 0.943 |
| Gemini 3.1 Pro | 96.4% | 0.973 / 0.987 | 0.944 / 0.959 | — / — | 0.975 |
| Qwen3.5-2B | 17.6% | 0.284 / 0.922 | 0.131 / 0.440 | — / — | 0.681 |
| Qwen3.5-9B | 42.0% | 0.516 / 0.861 | 0.245 / 0.520 | — / — | 0.789 |
| Qwen3.5-27B | 59.6% | 0.733 / 0.964 | 0.546 / 0.800 | — / — | 0.890 |
| Qwen3.5-397B-A17B | 74.8% | 0.825 / 0.954 | 0.729 / 0.835 | — / — | 0.835 |

### Tier 4 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 88.4% | 0.872 / 0.935 | 0.650 / 0.703 | — / — | 0.943 |
| Claude Opus 4.6 | 93.2% | 0.907 / 0.939 | 0.602 / 0.625 | — / — | 0.940 |
| Gemini 3.1 Pro | 96.0% | 0.947 / 0.971 | 0.830 / 0.853 | — / — | 0.981 |
| Qwen3.5-2B | 6.0% | 0.095 / 0.830 | 0.024 / 0.231 | — / — | 0.827 |
| Qwen3.5-9B | 31.2% | 0.412 / 0.898 | 0.143 / 0.427 | — / — | 0.807 |
| Qwen3.5-27B | 54.4% | 0.630 / 0.911 | 0.404 / 0.631 | — / — | 0.911 |
| Qwen3.5-397B-A17B | 71.2% | 0.735 / 0.908 | 0.543 / 0.631 | — / — | 0.904 |

