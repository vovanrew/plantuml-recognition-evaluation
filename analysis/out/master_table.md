# Master table — zero-shot image→PlantUML benchmark

**Models included: 7/7** (panel label: main)

Two populations reported side by side as `zeros_for_failed / compiled_only`: `zeros_for_failed` scores all diagrams (non-compiled = 0); `compiled_only` is over compiled cells, with CSR reported separately. chrF++ values in the headline tables are micro (corpus sacrebleu, available at the overall scope only); the macro tables and JSON carry the poolable chrF++ macro for every scope. Type accuracy is the `compiled_only` population by definition.

### Overall (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.897 / 0.939 | 0.757 / 0.799 | 60.74 / 66.01 | 0.941 |
| Claude Opus 4.6 | 94.1% | 0.909 / 0.940 | 0.693 / 0.720 | 62.36 / 66.57 | 0.950 |
| Gemini 3.1 Pro | 97.2% | 0.945 / 0.961 | 0.875 / 0.893 | 72.19 / 74.54 | 0.984 |
| Qwen3.5-2B | 20.1% | 0.246 / 0.878 | 0.114 / 0.481 | 8.96 / 65.12 | 0.758 |
| Qwen3.5-9B | 43.1% | 0.491 / 0.844 | 0.201 / 0.439 | 24.40 / 61.17 | 0.756 |
| Qwen3.5-27B | 60.1% | 0.676 / 0.917 | 0.485 / 0.722 | 38.41 / 65.65 | 0.886 |
| Qwen3.5-397B-A17B | 78.7% | 0.771 / 0.897 | 0.646 / 0.736 | 47.80 / 59.77 | 0.870 |

### Overall (macro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.891 / 0.953 | 0.807 / 0.860 | 62.73 / 67.09 | 0.941 |
| Claude Opus 4.6 | 94.1% | 0.901 / 0.958 | 0.776 / 0.823 | 65.68 / 69.80 | 0.950 |
| Gemini 3.1 Pro | 97.2% | 0.940 / 0.967 | 0.906 / 0.931 | 75.53 / 77.70 | 0.984 |
| Qwen3.5-2B | 20.1% | 0.175 / 0.865 | 0.166 / 0.495 | 12.89 / 64.14 | 0.758 |
| Qwen3.5-9B | 43.1% | 0.371 / 0.861 | 0.260 / 0.519 | 26.91 / 62.43 | 0.756 |
| Qwen3.5-27B | 60.1% | 0.562 / 0.925 | 0.505 / 0.803 | 40.91 / 68.07 | 0.886 |
| Qwen3.5-397B-A17B | 78.7% | 0.716 / 0.909 | 0.639 / 0.797 | 49.23 / 62.56 | 0.870 |

### Population gap (compiled-only − all-1000, micro)

The `compiled_only` minus `zeros_for_failed` gap per metric — the headline measure of how much a model's apparent quality rests on selective failure. A model that drops/times out on its hard diagrams is graded on an easier subset, so its `compiled_only` score runs far above its honest all-1000 score; a large gap is that fingerprint (it tracks the answer rate / CSR).

| Model | CSR | Element F1 (all → cmp, Δ) | Relationship F1 (all → cmp, Δ) | chrF++ (all → cmp, Δ) |
|---|---|---|---|---|
| GPT-5.2 | 93.5% | 0.897 → 0.939 (+0.042) | 0.757 → 0.799 (+0.042) | 60.74 → 66.01 (+5.27) |
| Claude Opus 4.6 | 94.1% | 0.909 → 0.940 (+0.031) | 0.693 → 0.720 (+0.027) | 62.36 → 66.57 (+4.21) |
| Gemini 3.1 Pro | 97.2% | 0.945 → 0.961 (+0.016) | 0.875 → 0.893 (+0.018) | 72.19 → 74.54 (+2.35) |
| Qwen3.5-2B | 20.1% | 0.246 → 0.878 (+0.632) | 0.114 → 0.481 (+0.367) | 8.96 → 65.12 (+56.16) |
| Qwen3.5-9B | 43.1% | 0.491 → 0.844 (+0.354) | 0.201 → 0.439 (+0.238) | 24.40 → 61.17 (+36.77) |
| Qwen3.5-27B | 60.1% | 0.676 → 0.917 (+0.241) | 0.485 → 0.722 (+0.237) | 38.41 → 65.65 (+27.23) |
| Qwen3.5-397B-A17B | 78.7% | 0.771 → 0.897 (+0.127) | 0.646 → 0.736 (+0.090) | 47.80 → 59.77 (+11.97) |

### Relationship F1 by relation type (read-through)

**GPT-5.2** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.814 / 0.845 | 940 / 875 |
| composition | 0.630 / 0.654 | 300 / 282 |
| aggregation | 0.618 / 0.625 | 244 / 239 |
| dependency | 0.571 / 0.583 | 393 / 374 |
| association | 0.629 / 0.680 | 1014 / 869 |
| message | 0.793 / 0.839 | 6546 / 5868 |

**Claude Opus 4.6** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.863 / 0.880 | 940 / 906 |
| composition | 0.467 / 0.492 | 300 / 276 |
| aggregation | 0.508 / 0.520 | 244 / 235 |
| dependency | 0.539 / 0.550 | 393 / 376 |
| association | 0.600 / 0.617 | 1014 / 956 |
| message | 0.708 / 0.740 | 6546 / 6010 |

**Gemini 3.1 Pro** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.924 / 0.940 | 940 / 909 |
| composition | 0.817 / 0.824 | 300 / 295 |
| aggregation | 0.800 / 0.820 | 244 / 233 |
| dependency | 0.782 / 0.789 | 393 / 387 |
| association | 0.811 / 0.819 | 1014 / 993 |
| message | 0.889 / 0.909 | 6546 / 6255 |

**Qwen3.5-2B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.086 / 0.462 | 940 / 128 |
| composition | 0.006 / 0.029 | 300 / 52 |
| aggregation | 0.008 / 0.091 | 244 / 21 |
| dependency | 0.016 / 0.039 | 393 / 42 |
| association | 0.064 / 0.202 | 1014 / 123 |
| message | 0.143 / 0.649 | 6546 / 828 |

**Qwen3.5-9B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.401 / 0.547 | 940 / 557 |
| composition | 0.130 / 0.238 | 300 / 139 |
| aggregation | 0.141 / 0.190 | 244 / 163 |
| dependency | 0.200 / 0.246 | 393 / 218 |
| association | 0.264 / 0.341 | 1014 / 505 |
| message | 0.147 / 0.611 | 6546 / 1078 |

**Qwen3.5-27B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.652 / 0.771 | 940 / 685 |
| composition | 0.425 / 0.618 | 300 / 162 |
| aggregation | 0.510 / 0.627 | 244 / 172 |
| dependency | 0.435 / 0.498 | 393 / 289 |
| association | 0.483 / 0.602 | 1014 / 680 |
| message | 0.462 / 0.783 | 6546 / 2730 |

**Qwen3.5-397B-A17B** — F1 (zeros_for_failed / compiled_only), support_gt:

| Relation | F1 (z / c) | support_gt (z / c) |
|---|---|---|
| inheritance | 0.615 / 0.769 | 940 / 617 |
| composition | 0.459 / 0.592 | 300 / 199 |
| aggregation | 0.443 / 0.556 | 244 / 173 |
| dependency | 0.326 / 0.387 | 393 / 253 |
| association | 0.508 / 0.627 | 1014 / 665 |
| message | 0.708 / 0.779 | 6546 / 5437 |

### Type accuracy by GT entity type (compiled_only, read-through)

**GPT-5.2** — pooled accuracy 0.941 (matched 4955, excluded 56, denominator 4899):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 137 | 0.847 |
| actor | 259 | 0.996 |
| annotation | 1 | 1.000 |
| boundary | 65 | 0.677 |
| class | 2210 | 0.975 |
| collections | 23 | 0.130 |
| control | 77 | 0.688 |
| database | 101 | 0.980 |
| entity | 82 | 0.280 |
| enum | 60 | 0.817 |
| interface | 224 | 0.964 |
| object | 1 | 0.000 |
| participant | 1655 | 0.964 |
| queue | 4 | 0.000 |

**Claude Opus 4.6** — pooled accuracy 0.950 (matched 5064, excluded 64, denominator 5000):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 142 | 0.979 |
| actor | 253 | 0.984 |
| annotation | 1 | 1.000 |
| boundary | 65 | 0.600 |
| class | 2293 | 0.989 |
| collections | 29 | 0.241 |
| control | 79 | 0.405 |
| database | 90 | 0.967 |
| entity | 93 | 0.473 |
| enum | 64 | 0.984 |
| interface | 232 | 0.897 |
| object | 7 | 0.000 |
| participant | 1645 | 0.980 |
| queue | 7 | 0.000 |

**Gemini 3.1 Pro** — pooled accuracy 0.984 (matched 5340, excluded 74, denominator 5266):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 140 | 0.971 |
| actor | 274 | 0.996 |
| annotation | 1 | 1.000 |
| boundary | 69 | 1.000 |
| class | 2358 | 0.986 |
| collections | 31 | 0.839 |
| control | 78 | 1.000 |
| database | 111 | 1.000 |
| entity | 111 | 0.775 |
| enum | 60 | 0.983 |
| interface | 218 | 0.982 |
| object | 9 | 0.000 |
| participant | 1798 | 0.999 |
| queue | 8 | 0.750 |

**Qwen3.5-2B** — pooled accuracy 0.758 (matched 824, excluded 0, denominator 824):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 21 | 0.000 |
| actor | 48 | 0.104 |
| boundary | 13 | 0.000 |
| class | 372 | 0.957 |
| collections | 4 | 0.000 |
| control | 8 | 0.000 |
| database | 14 | 0.071 |
| entity | 9 | 0.000 |
| enum | 5 | 0.000 |
| interface | 24 | 0.083 |
| object | 6 | 0.000 |
| participant | 297 | 0.879 |
| queue | 3 | 0.000 |

**Qwen3.5-9B** — pooled accuracy 0.756 (matched 2030, excluded 29, denominator 2001):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 86 | 0.012 |
| actor | 73 | 0.466 |
| annotation | 1 | 0.000 |
| boundary | 14 | 0.000 |
| class | 1298 | 0.943 |
| collections | 7 | 0.000 |
| control | 17 | 0.000 |
| database | 18 | 0.444 |
| entity | 30 | 0.033 |
| enum | 26 | 0.077 |
| interface | 155 | 0.529 |
| participant | 274 | 0.588 |
| queue | 2 | 0.000 |

**Qwen3.5-27B** — pooled accuracy 0.886 (matched 3077, excluded 42, denominator 3035):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 109 | 0.550 |
| actor | 94 | 0.862 |
| annotation | 1 | 0.000 |
| boundary | 35 | 0.229 |
| class | 1645 | 0.962 |
| collections | 8 | 0.000 |
| control | 37 | 0.135 |
| database | 21 | 0.762 |
| entity | 61 | 0.344 |
| enum | 39 | 0.487 |
| interface | 162 | 0.864 |
| object | 1 | 0.000 |
| participant | 821 | 0.923 |
| queue | 1 | 0.000 |

**Qwen3.5-397B-A17B** — pooled accuracy 0.870 (matched 3975, excluded 41, denominator 3934):

| GT type | support | accuracy |
|---|---|---|
| abstract_class | 105 | 0.105 |
| actor | 238 | 0.983 |
| boundary | 60 | 0.233 |
| class | 1597 | 0.966 |
| collections | 25 | 0.040 |
| control | 62 | 0.500 |
| database | 73 | 0.836 |
| entity | 73 | 0.301 |
| enum | 34 | 0.265 |
| interface | 167 | 0.731 |
| object | 7 | 0.000 |
| participant | 1487 | 0.924 |
| queue | 6 | 0.167 |

## By diagram type

### Type: class (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 94.4% | 0.899 / 0.940 | 0.679 / 0.711 | — / — | 0.953 |
| Claude Opus 4.6 | 97.4% | 0.928 / 0.949 | 0.662 / 0.679 | — / — | 0.971 |
| Gemini 3.1 Pro | 97.6% | 0.944 / 0.959 | 0.844 / 0.855 | — / — | 0.973 |
| Qwen3.5-2B | 21.6% | 0.238 / 0.882 | 0.055 / 0.218 | — / — | 0.836 |
| Qwen3.5-9B | 65.6% | 0.635 / 0.857 | 0.304 / 0.419 | — / — | 0.825 |
| Qwen3.5-27B | 75.4% | 0.762 / 0.923 | 0.545 / 0.670 | — / — | 0.913 |
| Qwen3.5-397B-A17B | 73.4% | 0.716 / 0.878 | 0.503 / 0.623 | — / — | 0.875 |

### Type: sequence (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 92.6% | 0.895 / 0.938 | 0.792 / 0.839 | — / — | 0.927 |
| Claude Opus 4.6 | 90.8% | 0.887 / 0.930 | 0.707 / 0.738 | — / — | 0.923 |
| Gemini 3.1 Pro | 96.8% | 0.947 / 0.963 | 0.889 / 0.909 | — / — | 0.996 |
| Qwen3.5-2B | 18.6% | 0.255 / 0.875 | 0.141 / 0.609 | — / — | 0.674 |
| Qwen3.5-9B | 20.6% | 0.261 / 0.800 | 0.137 / 0.469 | — / — | 0.493 |
| Qwen3.5-27B | 44.8% | 0.555 / 0.906 | 0.454 / 0.760 | — / — | 0.836 |
| Qwen3.5-397B-A17B | 84.0% | 0.834 / 0.917 | 0.707 / 0.778 | — / — | 0.865 |

## By tier

### Tier 1 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 97.6% | 0.952 / 0.964 | 0.929 / 0.936 | — / — | 0.936 |
| Claude Opus 4.6 | 98.4% | 0.957 / 0.969 | 0.916 / 0.935 | — / — | 0.974 |
| Gemini 3.1 Pro | 98.4% | 0.972 / 0.978 | 0.975 / 0.979 | — / — | 0.997 |
| Qwen3.5-2B | 32.8% | 0.451 / 0.833 | 0.353 / 0.634 | — / — | 0.702 |
| Qwen3.5-9B | 52.0% | 0.569 / 0.847 | 0.235 / 0.420 | — / — | 0.727 |
| Qwen3.5-27B | 72.0% | 0.763 / 0.924 | 0.656 / 0.821 | — / — | 0.864 |
| Qwen3.5-397B-A17B | 87.2% | 0.829 / 0.884 | 0.829 / 0.868 | — / — | 0.860 |

### Tier 2 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 94.8% | 0.945 / 0.975 | 0.902 / 0.927 | — / — | 0.959 |
| Claude Opus 4.6 | 94.0% | 0.953 / 0.982 | 0.831 / 0.865 | — / — | 0.966 |
| Gemini 3.1 Pro | 98.0% | 0.987 / 0.994 | 0.969 / 0.979 | — / — | 0.994 |
| Qwen3.5-2B | 22.0% | 0.313 / 0.824 | 0.176 / 0.466 | — / — | 0.793 |
| Qwen3.5-9B | 43.2% | 0.517 / 0.841 | 0.265 / 0.501 | — / — | 0.755 |
| Qwen3.5-27B | 62.0% | 0.760 / 0.962 | 0.625 / 0.848 | — / — | 0.891 |
| Qwen3.5-397B-A17B | 81.6% | 0.826 / 0.919 | 0.788 / 0.859 | — / — | 0.866 |

### Tier 3 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.2% | 0.911 / 0.943 | 0.840 / 0.868 | — / — | 0.927 |
| Claude Opus 4.6 | 90.8% | 0.915 / 0.956 | 0.734 / 0.767 | — / — | 0.942 |
| Gemini 3.1 Pro | 96.4% | 0.948 / 0.961 | 0.920 / 0.935 | — / — | 0.974 |
| Qwen3.5-2B | 19.6% | 0.304 / 0.941 | 0.141 / 0.452 | — / — | 0.736 |
| Qwen3.5-9B | 44.0% | 0.527 / 0.840 | 0.264 / 0.514 | — / — | 0.755 |
| Qwen3.5-27B | 58.0% | 0.709 / 0.931 | 0.567 / 0.821 | — / — | 0.872 |
| Qwen3.5-397B-A17B | 74.8% | 0.800 / 0.925 | 0.718 / 0.823 | — / — | 0.835 |

### Tier 4 (micro)

| Model | CSR | Element F1 | Relationship F1 | chrF++ | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 88.4% | 0.851 / 0.913 | 0.643 / 0.697 | — / — | 0.943 |
| Claude Opus 4.6 | 93.2% | 0.873 / 0.905 | 0.599 / 0.622 | — / — | 0.939 |
| Gemini 3.1 Pro | 96.0% | 0.918 / 0.941 | 0.810 / 0.832 | — / — | 0.981 |
| Qwen3.5-2B | 6.0% | 0.095 / 0.947 | 0.028 / 0.350 | — / — | 0.848 |
| Qwen3.5-9B | 33.2% | 0.430 / 0.849 | 0.141 / 0.363 | — / — | 0.770 |
| Qwen3.5-27B | 48.4% | 0.587 / 0.878 | 0.368 / 0.592 | — / — | 0.904 |
| Qwen3.5-397B-A17B | 71.2% | 0.707 / 0.873 | 0.535 / 0.625 | — / — | 0.901 |

