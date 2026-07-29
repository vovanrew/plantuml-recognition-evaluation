# Analysis Protocol

Methodological record for the analysis layer of the zero-shot image-to-PlantUML
benchmark: the aggregation, statistical, and reporting procedures that turn the
per-diagram metric outputs into the reported results. The per-diagram metrics are
defined in `evaluation-framework.md`, the test set in `test-set-construction.md`,
and the inference protocol in `benchmark-protocol.md`. The analysis reads the
stored scorer outputs and the raw inference responses; it does not re-run inference
or re-score diagrams.

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

## 4. Per-relation reporting

Relationship F1 is reported overall and per canonical relation type (inheritance,
composition, aggregation, dependency, association, message). Because the relation
type is part of the edge match key, a diagram's edges partition cleanly across the
six relations, and the scorer emits per-diagram per-relation true/false
positive/negative counts in addition to the overall counts. Per-relation point
estimates and confidence intervals are computed by pooling and resampling these
per-diagram per-relation counts; the pooled per-relation counts reproduce the
scorer's relation-level summary in both populations. Ground-truth support per
relation is reported alongside each estimate.

## 5. Statistical uncertainty

Uncertainty is reported as 95% confidence intervals from a paired percentile
bootstrap with a fixed seed and 1000 resamples. Each resample draws diagrams with
replacement; the same draws are applied to every model, so resamples are paired by
diagram. Within each resample, micro statistics are recomputed by re-pooling the
per-diagram counts, macro statistics by re-averaging the per-diagram values, and
CSR by re-averaging the per-diagram compilation flag. The interval is the 2.5th and
97.5th percentiles of the resample distribution (linear interpolation). The
identity resample reproduces the point estimate.

Model differences are reported as the confidence interval on the paired difference
between two models for a statistic; an interval excluding zero indicates a
difference unlikely to arise from sampling variation alone.

Confidence intervals are reported for: Compilation Success Rate; Element F1 and
Relationship F1, micro and macro, in both populations; chrF++ macro in both
populations; type accuracy; and per-relation Relationship F1 micro in both
populations. chrF++ micro is reported as a point estimate without an interval,
being a corpus statistic with no per-diagram components to resample.

## 6. Selective-failure bias (population gap)

The population gap for a metric is its `compiled_only` value minus its
`zeros_for_failed` value. It quantifies how much a model's apparent quality depends
on the subset of diagrams it compiled: a model that fails selectively on its
hardest diagrams is graded, under `compiled_only`, on an easier subset, so its gap
is large; a model that compiles across the difficulty range has a gap near zero.
The gap is reported at the overall scope for Element F1, Relationship F1, and
chrF++, and tracks the inverse of CSR.

## 7. Failure-case sampling

A stratified sample of failure cases is produced for qualitative error review. Each
diagram is classified into one of four mutually exclusive outcome classes, decided
in order: **provider drop** (no prediction was produced), **compile fail** (a
prediction exists but does not render), **compiled low-structural** (renders, but
per-diagram Element or Relationship F1 is below 0.5), and **ok**. The renderer's
compilation flag is authoritative, so a non-rendering prediction is a compile fail
even when its source happens to parse structurally.

Cases are stratified by model, diagram type, tier, and outcome class, with a fixed
per-cell cap. Selection within a cell uses a seed derived from the cell identity,
so a cell's sample depends only on its own contents and adding a model does not
perturb another model's sample. Cells exceeding the cap are recorded, and the
available and sampled counts are reported per cell so a capped sample is not
mistaken for the complete failure set. Each sampled case carries the ground-truth
source, the prediction, the compilation error, and the per-diagram structural
deltas (matched, missed, and spurious entities and relations).

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
error, network error) and provider no-response from model compile failure. A
provenance manifest records, per model, the exact snapshot, endpoint, non-thinking
configuration, token ceiling, and temperature.

The reasoning-leak count is re-derived by scanning each model's predictions for a
`<think>` block; it is not persisted by the inference harness. Dollar cost is not
reported: the open-weight arm was served under flat-rate rather than per-token
billing, so a per-token price basis comparable across the panel does not exist, and
token volumes are reported instead.

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
run-level tables until rescored.

Every aggregated number reproduces the corresponding scorer summary exactly: the
per-diagram counts pooled, or the per-diagram values averaged, equal the stored
summary. The two exceptions read directly from the summary rather than recomputing
— chrF++ micro (a corpus statistic) and per-relation Relationship F1 — and are
validated by read-through.

The analysis is reproducible: fixed seeds, sorted iteration, and timestamp-free
output make every artifact byte-identical on re-run for unchanged inputs. All
analysis artifacts are regenerable from the stored runs; the raw inference
responses are the retained source of truth.

The reported panel comprises seven models in two arms — frontier reference points
and the Qwen open family (a dense parameter ladder plus a mixture-of-experts
ceiling) — and is never collapsed into a single ranked ordering. The
mixture-of-experts model is reported at both its total and active parameter counts
and is not placed on the dense parameter axis. The model set is specified in
`benchmark-protocol.md`.
