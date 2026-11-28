# Analysis Protocol

Methodological record for the analysis layer of the zero-shot image-to-PlantUML
benchmark: the aggregation, statistical, and reporting procedures that turn the
per-diagram metric outputs into the reported results. The per-diagram metrics are
defined in `evaluation-framework.md`, the test set in `test-set-construction.md`,
and the inference protocol in `benchmark-protocol.md`. The analysis reads the
stored scorer outputs and the raw inference responses; it does not re-run inference
or re-score diagrams. The panel is listed in `analysis/model_registry_paper.json`, and
the outputs are written to `analysis/out_paper/`.

## 1. Reporting populations

Every structural metric is reported in two populations, side by side:

- **`zeros_for_failed`** — computed over all test diagrams; a prediction that does
  not compile, or that is absent, scores zero on every structural metric. This is
  the primary, unbiased figure: it grades a model on the whole test set.
- **`compiled_only`** — computed over the predictions that compile, with
  Compilation Success Rate reported separately.

The two populations are reported together because they diverge for low-CSR models:
a model that fails on its hardest diagrams is, under `compiled_only`, graded on the
easier subset it managed to compile, so its `compiled_only` score overstates its
ability on the full set. Each metric uses its own per-diagram compilation flag to
determine population membership; the four scorers' per-diagram compilation flags
agree, and the renderer's flag (CSR) is authoritative.

One answer of Qwen3.5-9B stops the structure extractor. The answer also does not
render, so it is a compile fail, and the structural scorers score it as an empty
graph. Whether it gets full credit or none, no full-set figure moves by more than
0.0027.

## 2. Aggregation

Each metric is reported at two aggregation levels:

- **Micro** pools per-diagram counts before computing the statistic, so larger
  diagrams contribute proportionally more. Element F1 and Relationship F1 micro are
  computed by summing the per-diagram true positives, false positives, and false
  negatives over the population, then computing precision, recall, and F1 from the
  pooled counts.
- **Macro** averages the per-diagram statistic, so every diagram contributes
  equally. Element F1 and Relationship F1 macro are the mean of the per-diagram
  precision, recall, and F1.

Compilation Success Rate is the count of compiled predictions divided by the test
set size.

chrF++ is asymmetric between levels. Its macro is the mean of the per-diagram
scores, with non-compiled predictions forced to zero in the `zeros_for_failed`
population and excluded in `compiled_only`. Its micro is a corpus-level sacrebleu
statistic with no per-diagram decomposition; it is read from the scorer summary and
is not recomputed by pooling, because no per-diagram components exist from which to
pool it.

Type accuracy is the share of name-matched entities carrying the correct UML type,
pooled over compiled predictions. Name-matched pairs whose ground-truth type lies
outside the scored class-like and participant vocabulary are excluded from the
denominator, and the excluded count is reported alongside the accuracy.

## 3. Stratification

The stored scorer summaries are global. Per-type and per-tier cells are
reconstructed by pooling the per-diagram counts after joining each diagram to its
`primary_type` and complexity `tier` from the test set. Results are reported at
three scopes: overall, per diagram type (class, sequence), and per complexity tier
(four `content_lines` quartiles). The join is on the bare diagram identifier; the
test-set keys carry a `.puml` suffix that is stripped before joining to the
metric keys, which are bare identifiers.

At sub-scopes (per type, per tier) chrF++ is reported as macro only, since its
micro is a corpus statistic defined at the overall scope. Per-relation Relationship
F1 is reported overall.

Per-type and per-tier intervals are given for CSR, and in both populations for
Element F1 and Relationship F1 micro and for chrF++ macro, with the bootstrap of §5. One draw of the
diagrams serves all strata, and each stratum's statistic is computed on the resampled
diagrams that fall in it. Two contrasts are reported with their intervals: class
minus sequence, and tier 1 minus tier 4. A contrast is the difference between two
strata within the same resample, so it is paired. These intervals are built by
`analysis/build_paper_extras.py`.

## 4. Per-relation reporting

Relationship F1 is reported overall and per canonical relation type (inheritance,
composition, aggregation, dependency, association, message). Because the relation
type is part of the edge match key, a diagram's edges partition cleanly across the
six relations, and the scorer emits per-diagram per-relation true/false
positive/negative counts in addition to the overall counts. Per-relation point
estimates and confidence intervals are computed by pooling and resampling these
per-diagram per-relation counts; the pooled per-relation counts reproduce the
scorer's relation-level summary in both populations. The master table reads its
per-relation point estimates from that summary. Ground-truth support per
relation is reported alongside each estimate.

## 5. Statistical uncertainty

Uncertainty is reported as 95% confidence intervals from a paired percentile
bootstrap with the fixed seed 20260614 and 1,000 resamples. Each resample draws diagrams with
replacement; the same draws are applied to every model, so resamples are paired by
diagram. Within each resample, micro statistics are recomputed by re-pooling the
per-diagram counts, macro statistics by re-averaging the per-diagram values, and
CSR by re-averaging the per-diagram compilation flag. The interval is the 2.5th and
97.5th percentiles of the resample distribution (linear interpolation). The
identity resample reproduces the point estimate. A resample in which a statistic is
undefined is left out of that statistic's percentiles. This happens, for example, to a
per-relation F1 when the relation is absent from both the ground truth and the
predictions of the resampled set. A paired difference uses the resamples in which both statistics are
defined.

Model differences are reported as the confidence interval on the paired difference
between two models for a statistic; an interval excluding zero indicates a
difference unlikely to arise from sampling variation alone.

Confidence intervals are reported for: Compilation Success Rate; Element F1 and
Relationship F1, micro and macro, in both populations; chrF++ macro in both
populations; type accuracy; and per-relation Relationship F1 micro in both
populations. chrF++ micro is reported as a point estimate without an interval,
being a corpus statistic with no per-diagram components to resample.

## 6. Population gap

The population gap for a metric is its `compiled_only` value minus its
`zeros_for_failed` value. It has two parts.

**The part built into the populations.** A failed answer scores zero in
`zeros_for_failed` and is left out of `compiled_only`. The gap is therefore positive
whenever CSR is below 100%, even when failures fall at random over the test set.

**Selective failure.** Failures are not spread evenly: the compile rate falls as
complexity rises (§3). So `compiled_only` grades each model on a subset that holds
more simple diagrams than the test set, a subset the model selected itself. This part
raises the gap only where the compiled answers also score differently across tiers.

The two parts are not separated. The gap is reported at the overall scope for Element
F1, Relationship F1 and chrF++, and tracks the inverse of CSR.

## 7. Error analysis

The error analysis says what kinds of failure the models make. It has two parts: outcome
counts over all 1,000 diagrams of every run, and a coded sample of failure cases.

**Outcome classes.** Each diagram of a run gets one of four classes, decided in order. A
**provider drop** has no answer. A **compile fail** has an answer that does not render. A
**compiled low-structural** answer renders, but its per-diagram Element F1 or Relationship F1
is below 0.5. Every other answer is **ok**. The class comes from the renderer's result first,
so an answer that does not render is a compile fail even when its source can be parsed. An
answer that stops the structure extractor is also a compile fail: the model answered, and the
answer does not render. The counts of the four classes are reported per run, and they give
how often each class occurs. The counts are written by `analysis/build_failure_index.py`.

**The sample.** The strata are model × diagram type × tier × failure class (compile fail or
compiled low-structural), which is 16 cells per model. Each non-empty cell gives one case, and
the seven models give 108 cases. The
case is drawn by a seeded rule whose seed depends only on the cell, so one model's sample does
not change when another model is added. One case per cell shows the kinds of failure, not how
often each occurs. Provider drops are counted from the runs and are not sampled.

**What a coder sees.** Each case is a file with the ground-truth source, the model's answer
and the image the model was shown. Display-only lines are removed from the shown answer and
kept in a side file. A compile fail also shows the renderer's message and the line it names. A
compiled low-structural case also shows the structural difference as the scorer keys it:
matched, missed and spurious elements and relations. These are extracted again for the sampled
cases, and the build stops if they do not reproduce the stored per-diagram counts. The case
carries a blind identifier in a shuffled order. The coder is not told which model produced the
answer. The key that links identifiers to models is written before any case is coded.

**Coding.** The codes and their rules are fixed in a codebook before the first case is coded,
and the key records the codebook's hash. Every case gets one primary code, the defect that
would recover most of the loss if fixed alone, and any secondary codes. The compile-failure
codes are a syntax error, an answer that never ends, and the wrong diagram family. The
structural codes are a wrong relation type, missed relations, invented elements, a misread
name, a wrong element kind, lost control flow, and missed elements. One more code marks a
measurement artifact.
The measurement artifact is limited to two stated causes, and any other candidate goes to the
author. The coder is an AI model, run as separate instances that cannot see each other's codes.
Each case is coded twice, independently. A case goes to review when the two codings differ on
the primary code or a coder flags it (`ask_author`, or `M?` as the primary code). Each review
case is coded five more times, so it has seven codings, and the primary code with the most votes
is taken. The author decides a review case whose vote ends on `M?`.

**Reported.** The report gives the agreement of the two codings on the primary code, the review
cases with their votes, the cases the author decided, and the primary codes per model. The votes
are in `analysis/out_paper/error_sample/votes/`.

The sample is drawn by `analysis/build_error_sample.py draw` and reported by its `report`
command. The codebook is `analysis/error_codebook.md`.

## 8. Run-level accounting

Token totals are computed from the raw inference responses, summed over all cells
including failures. Input is the prompt token count. Output is the completion token
count as returned by the provider, which already includes any reasoning tokens, so
reasoning is never added on top; for the native Gemini responses, output is the sum
of the candidate and thought token counts. Reasoning (or thought) tokens are
reported as a separate component of output. A record that signals a dropped image
but carries a complete billed response has its tokens counted while the cell is
still classified as a provider failure.

A failure inventory separates provider failures (timeout, dropped image, HTTP
error, network error) and provider no-response from model compile failure. The
finish reasons of the returned answers are counted per model in three classes: the
answer ended on its own, it reached the output limit, or the provider stopped it as
recitation of existing text. A provider that stops an answer as recitation returns
no text, and the answer counts as a compile fail. A
provenance manifest records, per model, the exact snapshot, provider, endpoint,
reasoning configuration, token ceiling, timeout, temperature, and run start time.

The reasoning-leak count is re-derived by scanning each model's predictions for a
`<think>` block; it is not persisted by the inference harness. Dollar cost is not
reported. The three dense Qwen3.5 models are self-served and have no per-token price,
so no price basis is comparable across the panel. Token volumes are reported instead.

## 9. Image crowding descriptor

Per-tier image crowding is reported as `content_lines` per megapixel after the
1568px standardization, pooled within each tier, with megapixels read from the
dimensions of the standardized images. It rises monotonically with tier and is
reported as the legibility context accompanying the per-tier degradation of the
metrics.

## 10. Eligibility, validation, and reproducibility

A model is reported only when its four metric outputs are present and its
reasoning-leak count is zero. Run-level reporting additionally requires that the
raw-response and scorer views of the run agree on the no-response count; a
mismatch indicates a run resumed after scoring and the model is held out of the
run-level tables until rescored. On the scorer side, a diagram counts as no-response
only when neither the structural scorers nor chrF++ saw an answer. An answer held
back from the structure extractor (§1) is therefore not a no-response.

Every aggregated number reproduces the corresponding scorer summary exactly: the
per-diagram counts pooled, or the per-diagram values averaged, equal the stored
summary. The two exceptions read directly from the summary rather than recomputing
— chrF++ micro (a corpus statistic) and per-relation Relationship F1 — and are
validated by read-through.

The analysis is reproducible: fixed seeds, sorted iteration, and timestamp-free
output make every artifact byte-identical on re-run for unchanged inputs. All
analysis artifacts are regenerable from the stored runs; the raw inference
responses are the retained source of truth.

The reported panel has seven models in two groups, and it is never collapsed into a
single ranked order. The hosted reference models come first: GPT-5.2, Claude Opus
4.6, Gemini 3.1 Pro and Qwen3.5-397B-A17B, each on its provider's serving. The
self-served open models follow: the dense Qwen3.5-2B, 9B and 27B. Statements about a
trend with model size use these three dense models only. Qwen3.5-397B-A17B is a
mixture-of-experts model, named by its total and active parameter counts, and it is
not placed on the size axis. The figures show the models in the same two groups
(`analysis/build_plots.py --by-arm`). The panel is listed in
`analysis/model_registry_paper.json`, and the models are specified in
`benchmark-protocol.md`.

## 11. Human-rater check

The human-rater check asks one question. When two models answer the same test diagram, does a
person pick the drawing that the metrics score higher? All its numbers are descriptive, and no
pass mark is set.

**What a rater sees.** For one test diagram, the rater sees three pictures: the test image, and
the two models' answers rendered as drawings A and B. The order of A and B is random, and
nothing names a model. Each answer's PlantUML block is rendered by the same pipeline that made
the test images. A sample answer that does not render to exactly one picture stops the build.
The rater answers: A is closer, B is closer, or about the same. The rater judges the content:
the boxes, their names and members, the messages and their text, and what is connected to what
with which kind of arrow. Layout, position and colour are ignored. An optional comment follows.
The raters are Ukrainian, so the page is in Ukrainian.

**Comparisons.** Four comparisons: Gemini 3.1 Pro against Claude Opus 4.6, GPT-5.2 against
Claude Opus 4.6, Qwen3.5-397B-A17B against Qwen3.5-27B, and Qwen3.5-9B against Qwen3.5-27B.

**Pool.** A diagram enters a comparison's pool when both answers compiled and their Element F1
or Relationship F1 differ. A pair's direction is the model the metric prefers: by Element F1
when it differs, otherwise by Relationship F1. Test diagrams that the raters may already have
seen are left out.

**The sample.** Each comparison gives 15 pairs, 60 in all. The direction the pool prefers more
often gets 8 pairs and the other gets 7. Without this balance, a rater who always picked one
model could agree with the metric without judging content. In each direction, half the pairs
(rounded down) have different Element F1, and the rest differ only in Relationship F1. Class
and sequence diagrams are split as evenly as each cell allows. Each cell is drawn by a seeded
rule, and a diagram appears in one pair only. The key that links pairs to models is written
before anything is rendered.

**Raters.** Two raters rate the 60 pairs alone, each in their own random order: the author (R1
in the report) and a second person (R2), a software engineer who uses UML diagrams in his work.
They do not discuss pairs before both have finished.

**Reported.** For each rater and each metric, the report takes the pairs where the metric
differs and the rater picked A or B. It gives the share where the rater picked the answer with
the higher score, with a Wilson 95% interval, and the count of "about the same". Beside this:
the agreement with the pair's direction, the same numbers on the pairs where the two metrics
prefer different answers, and counts per comparison and per diagram type. The agreement with the
pair's direction is also given by the size of the gap in the metric that sets the direction. The
gap falls in four bins: below 0.05, 0.05 to 0.15, 0.15 to 0.35, and 0.35 or more. These numbers
are given per rater and over both raters' picks. The bins are set after the ratings are seen, so
they describe and do not test. Between the raters: the share of pairs with the same answer and
Cohen's kappa. The author describes what differs in each pair where both raters
chose against the metric.

The sample is drawn by `analysis/rater_check.py draw`, rendered by its `render` command, put on
rating pages by `sheets`, and reported by `report`.
