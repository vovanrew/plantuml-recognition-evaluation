# Results, explained: zero-shot image-to-PlantUML benchmark

This file explains the benchmark results in plain words. It is written by hand. Every
number is copied from a file in `analysis/out_paper/`, and each section names the file
it draws on. The generated tables with all values are in `out_paper/exhibits.md`.

## 1. What was measured

Seven multimodal models received a rendered UML diagram image, a class diagram or a
sequence diagram. They were asked, with no examples, to write the PlantUML source of
the diagram. Each model answered all 1,000 diagrams of the test set. Five metrics
score each answer. Their full definitions are in `methodology/evaluation-framework.md`.

- **CSR (Compilation Success Rate)** is the share of answers that PlantUML renders
  into a diagram. An answer that does not render fails, whatever its text says.
- **Element F1** measures how well the answer recovers the named entities, such as
  classes, interfaces, actors and participants. Entities are matched by their visible
  name. The scale is 0 to 1.
- **Relationship F1** measures how well the answer recovers the typed edges. An edge
  is matched by its source, its target and its relation type. There are six relation
  types: inheritance, composition, aggregation, dependency, association and message.
- **Type accuracy** is the share of name-matched entities that also have the correct
  UML type. It uses compiled answers only.
- **chrF++** is a character-level text similarity score on a 0 to 100 scale. It
  covers the text that the structural metrics ignore, such as attributes and message
  labels.

### Two populations

Each structural metric is reported in two ways, written `all / compiled`:

- **all** (`zeros_for_failed`) uses all 1,000 diagrams. An answer that does not
  compile scores 0. This is the main figure.
- **compiled** (`compiled_only`) uses only the answers that compiled.

A weak model often compiles only its easier diagrams. The `compiled` figure then
grades it on an easy subset, so the `all` figure is the fair one. Section 5 measures
this effect.

**Micro and macro.** Micro adds up the matches over all diagrams first, so large
diagrams count more. Macro averages the per-diagram scores, so every diagram counts
the same. Unless a section says otherwise, the numbers below are micro.

**Intervals.** A range `[low, high]` is a 95% paired bootstrap interval with 1,000
resamples (`out_paper/ci_table.md`, line 5). To compare two models, we use the
interval of their difference. A difference counts only when that interval excludes
zero.

### The panel

The panel has two groups, and they are not one ranking.

- **Hosted reference models:** GPT-5.2, Claude Opus 4.6, Gemini 3.1 Pro and
  Qwen3.5-397B-A17B. Each model ran on its provider's serving.
- **Self-served open models:** Qwen3.5-2B, Qwen3.5-9B and Qwen3.5-27B. They ran on
  one GPU with the released bf16 weights.

Size trends use the three dense self-served models only. Qwen3.5-397B-A17B is a
mixture-of-experts model, so it is not on the size axis.

---

## 2. Main results

Source: `out_paper/exhibits.md`, Exhibit 1 (lines 17 to 20 and 28 to 30), for the
table, and `out_paper/ci_table.md` (pairwise tables) for the comparisons.

All values use the `all` population. chrF++ is macro here, because only the macro
value has an interval.

| Model | CSR | Element F1 | Relationship F1 | chrF++ macro | Type acc |
|---|---|---|---|---|---|
| GPT-5.2 | 93.5% [91.9%, 95.0%] | 0.916 [0.897, 0.933] | 0.770 [0.733, 0.803] | 62.73 [61.23, 64.20] | 0.941 [0.928, 0.954] |
| Claude Opus 4.6 | 94.1% [92.5%, 95.5%] | 0.934 [0.915, 0.949] | 0.700 [0.664, 0.735] | 65.68 [64.23, 67.18] | 0.951 [0.937, 0.963] |
| Gemini 3.1 Pro | 97.2% [96.2%, 98.1%] | 0.967 [0.957, 0.976] | 0.894 [0.870, 0.914] | 75.53 [74.19, 76.85] | 0.984 [0.973, 0.993] |
| Qwen3.5-397B-A17B | 78.7% [76.2%, 81.2%] | 0.794 [0.767, 0.818] | 0.657 [0.616, 0.697] | 49.23 [47.46, 51.17] | 0.871 [0.851, 0.889] |
| Qwen3.5-2B | 19.1% [16.7%, 21.5%] | 0.239 [0.205, 0.272] | 0.110 [0.087, 0.134] | 11.82 [10.31, 13.45] | 0.755 [0.702, 0.807] |
| Qwen3.5-9B | 41.1% [38.1%, 44.4%] | 0.481 [0.445, 0.520] | 0.198 [0.169, 0.231] | 25.83 [23.73, 27.98] | 0.774 [0.731, 0.812] |
| Qwen3.5-27B | 64.4% [61.5%, 67.3%] | 0.713 [0.681, 0.743] | 0.507 [0.460, 0.552] | 43.87 [41.65, 46.10] | 0.889 [0.867, 0.909] |

**Gemini 3.1 Pro scores highest on every metric in the table.** Its difference from
each other model excludes zero on every metric of the CI table, in both populations.

**GPT-5.2 and Claude Opus 4.6 are close.** Their CSR difference is -0.006
[-0.028, 0.015], and their Element F1 difference is -0.019 [-0.039, 0.002]. Both
intervals include zero, so neither model is ahead on these metrics. Type accuracy
also shows no difference. GPT-5.2 is ahead on Relationship F1, by 0.070
[0.042, 0.097]. Claude Opus 4.6 is ahead on chrF++ macro: GPT-5.2 minus Claude Opus 4.6 is -2.95 [-4.50, -1.42].

**Qwen3.5-397B-A17B is below the other three hosted models.** Its CSR is lower than
that of GPT-5.2 by 0.148 [0.118, 0.176], and lower than that of Gemini 3.1 Pro by
0.185 [0.158, 0.211]. On Relationship F1 it is closest to Claude Opus 4.6. Their
difference is 0.043 [0.015, 0.073], which still excludes zero.

---

## 3. The dense sizes: what size changes

Source: `out_paper/master_table.md`, lines 14 to 17, and `out_paper/ci_table.md`
(pairwise tables, lines 52 to 57, 78 to 83, 104 to 109 and 130 to 161).

On the `all` population, every metric rises with size, from 2B to 9B to 27B:

- CSR: 19.1%, 41.1%, 64.4%.
- Element F1: 0.239, 0.481, 0.713.
- Relationship F1: 0.110, 0.198, 0.507.

Each step is a real difference. For example, the CSR difference is -0.220
[-0.258, -0.183] from 2B to 9B, and -0.233 [-0.271, -0.197] from 9B to 27B.

The `compiled` population tells a different story. Element F1 on compiled answers is
0.874 for 2B, 0.871 for 9B and 0.945 for 27B. The 2B and 9B values do not differ:
the interval is [-0.042, 0.054]. Relationship F1 on compiled answers is 0.463 for 2B
and 0.470 for 9B, and these do not differ either. So the step from 2B to 9B mainly
adds answers that compile. The step from 9B to 27B adds both: more answers compile,
and the compiled answers are better. On compiled answers, 9B minus 27B is -0.074
[-0.106, -0.042] for Element F1 and -0.258 [-0.326, -0.182] for Relationship F1.

**Qwen3.5-397B-A17B against Qwen3.5-27B.** On the `all` population, the 397B model
is ahead. For CSR, 27B minus 397B is -0.143 [-0.181, -0.109]. For Relationship F1 it
is -0.150 [-0.190, -0.114]. On compiled answers the picture changes. Their Relationship F1
difference is -0.017 [-0.062, 0.026], so there is no difference. On compiled Element
F1, 27B is ahead by 0.022 [0.000, 0.040].

---

## 4. Selective failure: the population gap

Source: `out_paper/master_table.md`, lines 37 to 43.

The population gap is the `compiled` value minus the `all` value. A large gap means
that the `compiled` figure looks much better than the model's real result.

| Model | CSR | Element F1 gap | Relationship F1 gap | chrF++ gap |
|---|---|---|---|---|
| GPT-5.2 | 93.5% | +0.043 | +0.042 | +5.27 |
| Claude Opus 4.6 | 94.1% | +0.032 | +0.027 | +4.21 |
| Gemini 3.1 Pro | 97.2% | +0.016 | +0.018 | +2.35 |
| Qwen3.5-397B-A17B | 78.7% | +0.130 | +0.089 | +11.97 |
| Qwen3.5-2B | 19.1% | +0.635 | +0.353 | +53.00 |
| Qwen3.5-9B | 41.1% | +0.390 | +0.273 | +39.34 |
| Qwen3.5-27B | 64.4% | +0.232 | +0.221 | +25.62 |

In this panel, the gap grows as CSR falls, for all three metrics. Qwen3.5-2B shows it
most clearly. Its Element F1 is 0.239 on all diagrams but 0.874 on compiled answers,
a gap of +0.635. It compiles only 19.1% of the diagrams. The hosted models compile
most diagrams, so their gaps are small. **The practical rule: report the `all`
figure as the main result, and always read a `compiled` figure next to CSR.**

---

## 5. Relationship F1 by relation type

Source: `out_paper/ci_table.md`, lines 247 to 253 (`all` population), and
`out_paper/exhibits.md`, line 78 (ground-truth counts).

The six relation types are very uneven in the test set. There are 6544 message
edges, 940 inheritance edges and 862 association edges. Dependency has 375,
composition 300 and aggregation 244. The rare types have wide intervals, so only
large differences are clear. The intervals compared below are each model's own
intervals, and they do not overlap.

- **GPT-5.2 and Claude Opus 4.6** recover inheritance and message best. For GPT-5.2,
  inheritance is 0.820 [0.771, 0.865] and message is 0.814 [0.771, 0.855]. Its other
  four types are all at or below 0.634. Claude Opus 4.6 has 0.870 for inheritance and
  0.732 for message. Its other four types range from 0.461 to 0.581.
- **Gemini 3.1 Pro** is highest on inheritance, 0.931 [0.906, 0.953], and message,
  0.914 [0.886, 0.941]. Its lowest type is association, 0.770 [0.701, 0.841].
- **Qwen3.5-2B** recovers almost no edges of any type. Composition is 0.000, and its
  best type is message at 0.141.
- **Qwen3.5-9B** is weak on messages: 0.155 [0.114, 0.205], against 0.381
  [0.317, 0.446] for inheritance. This matches its low CSR on sequence diagrams
  (Section 6).
- **Qwen3.5-397B-A17B** is best on message, 0.727 [0.674, 0.777], and lowest on
  dependency, 0.360 [0.274, 0.439].

---

## 6. Class diagrams and sequence diagrams

Source: `out_paper/paper_extras.md`, lines 9 to 63 (column "class - sequence").

**CSR.** Four models compile class diagrams and sequence diagrams at different rates.
Claude Opus 4.6 (+0.066 [+0.038, +0.096]), Qwen3.5-9B (+0.434 [+0.381, +0.489]) and
Qwen3.5-27B (+0.276 [+0.219, +0.334]) compile more class diagrams. Qwen3.5-9B shows
the largest gap: 0.628 on class diagrams and 0.194 on sequence diagrams.
Qwen3.5-397B-A17B compiles more sequence diagrams (-0.106 [-0.156, -0.054]). For
GPT-5.2, Gemini 3.1 Pro and Qwen3.5-2B, the interval includes zero, so there is no
difference.

**Element F1 on compiled answers.** Once an answer compiles, entity recovery is about
the same on both types. Only Qwen3.5-397B-A17B differs: it is better on sequence
diagrams: class minus sequence is -0.046 [-0.076, -0.012].

**Relationship F1 on all diagrams.** Five models recover edges better on sequence
diagrams: GPT-5.2 (-0.147), Claude Opus 4.6 (-0.104), Gemini 3.1 Pro (-0.069),
Qwen3.5-2B (-0.100) and Qwen3.5-397B-A17B (-0.243). The intervals of all five exclude
zero. Qwen3.5-9B is the exception: it is better on class diagrams, by +0.136
[+0.075, +0.196]. For Qwen3.5-27B the interval includes zero.

---

## 7. Complexity tiers

Source: `out_paper/paper_extras.md`, lines 69 to 123 (column "1 - 4"), and
`out_paper/run_level.md`, lines 51 to 54 (crowding).

The test diagrams are split into four tiers of 250 diagrams by their number of source
lines. Tier 1 holds the simplest diagrams and tier 4 the most complex. The contrast
below is tier 1 minus tier 4, so a positive value means a drop at tier 4.

| Model | CSR, tier 1 | CSR, tier 4 | CSR, tier 1 - 4 |
|---|---|---|---|
| GPT-5.2 | 0.976 | 0.884 | +0.092 [+0.048, +0.138] |
| Claude Opus 4.6 | 0.984 | 0.932 | +0.052 [+0.019, +0.088] |
| Gemini 3.1 Pro | 0.984 | 0.960 | +0.024 [-0.002, +0.054] (includes 0) |
| Qwen3.5-397B-A17B | 0.872 | 0.712 | +0.160 [+0.088, +0.227] |
| Qwen3.5-2B | 0.320 | 0.060 | +0.260 [+0.197, +0.321] |
| Qwen3.5-9B | 0.488 | 0.312 | +0.176 [+0.091, +0.257] |
| Qwen3.5-27B | 0.740 | 0.540 | +0.200 [+0.118, +0.282] |

- **CSR** drops from tier 1 to tier 4 for six models. For Gemini 3.1 Pro the
  interval includes zero, so its drop is not clear.
- **Element F1 on all diagrams** drops for all seven models. The smallest drop is
  Gemini 3.1 Pro's, +0.042 [+0.021, +0.067].
- **Relationship F1 on all diagrams** drops for six models, by between +0.159
  (Gemini 3.1 Pro) and +0.327 (Claude Opus 4.6). For Qwen3.5-9B the interval,
  [-0.000, +0.169], includes zero.
- **Element F1 on compiled answers** drops for GPT-5.2, Claude Opus 4.6, Gemini 3.1
  Pro and Qwen3.5-27B. For Qwen3.5-2B, Qwen3.5-9B and Qwen3.5-397B-A17B the interval
  includes zero.

The images also become more crowded from tier to tier. The source has 8.74 lines per
megapixel at tier 1, then 13.25, 21.12 and 50.09 at tier 4. So the most complex
diagrams are also the densest images.

---

## 8. Tokens, failures and run settings

Source: `out_paper/run_level.md`, lines 11 to 17 (tokens), 25 to 31 (failures) and
37 to 43 (provenance).

Token totals over all 1,000 diagrams, in millions:

| Model | Input | Output | Total |
|---|---|---|---|
| GPT-5.2 | 1.631 | 0.331 | 1.962 |
| Claude Opus 4.6 | 1.415 | 0.339 | 1.754 |
| Gemini 3.1 Pro | 1.165 | 0.297 | 1.462 |
| Qwen3.5-397B-A17B | 1.386 | 0.679 | 2.066 |
| Qwen3.5-2B | 1.387 | 2.078 | 3.465 |
| Qwen3.5-9B | 1.387 | 1.204 | 2.591 |
| Qwen3.5-27B | 1.387 | 0.783 | 2.170 |

Input is similar for all models, because every model gets the same images and prompt.
Output differs much more. Among the dense sizes, the smallest model writes the most:
2.078 million output tokens for 2B, 1.204 for 9B and 0.783 for 27B. The hosted models
write between 0.297 and 0.679 million. No dollar prices are given.

**Failures.** Almost every failure is an answer that does not compile. The counts of
such answers are 64 for GPT-5.2, 59 for Claude Opus 4.6, 28 for Gemini 3.1 Pro and
213 for Qwen3.5-397B-A17B. For the dense sizes they are 809 for 2B, 589 for 9B and
356 for 27B. Only one answer in the whole panel is missing: GPT-5.2 gave no response
to one diagram, after a timeout.

**Run settings.** All runs used temperature 0 and the same output limit of 5376
tokens. Thinking was turned off, except for Gemini 3.1 Pro, where it was set to low. No
run leaked reasoning text into its answers: the leak count is 0 for every model.

---

## 9. Related documents

- `analysis/error_analysis.md` describes the kinds of failure, from a coded sample of
  108 failure cases in `out_paper/error_sample/`. The codes are defined in
  `analysis/error_codebook.md`.
- `out_paper/failure_index.md` gives the outcome counts and the failure cases that
  the sample draws from.
- `out_paper/rater_check/report.md` reports the human-rater check. It asks whether
  people prefer the answer that the metrics score higher. The method is in
  `methodology/analysis-protocol.md` §11.
- `methodology/analysis-protocol.md` describes the full analysis method.
