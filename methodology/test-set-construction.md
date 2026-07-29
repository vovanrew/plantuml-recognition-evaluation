# Test Set Construction

Methodological record for the curated evaluation set used in the zero-shot
image-to-PlantUML benchmark. Scope: class and sequence diagrams. Decisions
recorded 2026-06-07.

## 1. Objective

Construct a reproducible, repository-disjoint evaluation set of UML diagrams,
balanced across diagram type and complexity, drawn from the *UML-in-the-Wild*
corpus (143,427 PlantUML/PNG pairs mined from open-source repositories via World
of Code). The set must (i) support stable per-stratum comparison of multimodal
models, (ii) enable a complexity-degradation analysis, and (iii) reserve all
selected repositories from future fine-tuning training data.

Size: 1,000 diagrams (2 types x 4 complexity tiers x 125). The full set is the
benchmark population for every model run.

## 2. Unit of analysis and identifier

Each per-diagram metadata record is keyed by its source filename
(`{blob_id}.puml`, or `{blob_id}_{NN}.puml` for files split from a multi-block
source). The `blob_id` field is **not** a unique diagram identifier: 5,360
records (1,465 distinct `blob_id` values) are split siblings that share the
parent file's content hash. The unique identifier is therefore the **filename
key**. The published reproducibility artifact is the list of filename keys (not
bare `blob_id`s).

## 3. Inclusion criteria

A diagram is eligible if all of the following hold in the corpus metadata:

| Criterion | Condition |
|---|---|
| Diagram type | `primary_type in {class, sequence}` |
| No hybrid labels | `secondary_types == []` |
| Structural extraction succeeded | `extraction_error == null` |
| Source not truncated | `truncated != true` |
| Bounded structural size | `elements_total <= 50` |
| Source repository known | `repository != null` |

`repository != null` is required because the repository-disjoint constraint
(Section 6) cannot be enforced without a repository identifier; 1,125 otherwise
eligible diagrams lack a mapped repository and are excluded.

Applying these criteria yields a candidate pool of **106,348 diagrams**
(class 71,323; sequence 35,025).

## 4. Exclusion of degenerate renders

Diagrams whose rendered image cannot serve as a faithful single-image input are
removed. This is a *degeneracy* filter, not a resolution cap (cf. Section 7):

1. **Multi-page (`newpage`)** — a source that renders to more than one PNG page
   has no single canonical image and violates the one-image-per-diagram
   contract. Identified by mapping each diagram's filename key to its PNG page
   set. **309** candidates excluded. (Split multi-block siblings, each a
   distinct single-image diagram, are retained and must not be conflated with
   `newpage` pages; both use a `_{NN}` suffix.)
2. **Renderer-clipped** — image long edge >= 16,384 px (the renderer's bitmap
   limit), at which the diagram is truncated and no longer matches its source.
   **595** candidates excluded.
3. **Extreme aspect ratio** — long/short edge > 8:1, which no model's
   tiling/resize pipeline ingests without severe distortion. **326** candidates
   excluded.

Surviving pool after degeneracy exclusion: **105,118 diagrams**
(class 70,477; sequence 34,641). Total degeneracy loss ~1.2%.

## 5. Stratification variable

Complexity is stratified into four tiers per type by **quartiles of
`content_lines`** (non-blank, non-comment line count), computed independently
within each type.

### 5.1 Rejection of `elements_total`

`elements_total` was rejected as the stratification variable for sequence
diagrams. The parser counts only *participants* as elements of a sequence
diagram, a quantity that is small and concentrated: its quartiles on the
sequence pool are Q1=3, Q2=4, Q3=6, producing three near-degenerate integer
tiers (<=3, =4, 5-6 participants) and one wide top tier (7-50).

### 5.2 Rejection of a multi-metric composite index

A composite complexity index over graph, text, and visual metrics was
considered and rejected as disproportionate to its benefit. Within each type,
the candidate size metrics are strongly collinear (Spearman rho):

| Pair | class | sequence |
|---|---|---|
| `elements_total` ~ `connections_total` | 0.90 | 0.65 |
| `elements_total` ~ `content_lines` | 0.78 | 0.58 |
| `content_lines` ~ `connections_total` | 0.75 | 0.82 |

A composite would reproduce a single well-chosen axis at high agreement while
requiring additional parsing/rendering passes and a sensitivity analysis to
defend. `connections_total` was additionally disfavoured because class-diagram
connection counts are the least reliable corpus annotation (~73% exact match in
manual validation).

### 5.3 Selection of `content_lines`

`content_lines` provides well-spread, continuous tiers for both types
(class quartiles 11/24/49; sequence 12/22/39), requires no additional
extraction, and is robust. Critically, because the task is image-to-code, the
tiers were verified to be **monotonic in visual complexity**: median rendered
image area (megapixels) increases across tiers for both types.

| Tier | class median MP | sequence median MP |
|---|---|---|
| Q1 | 0.65 | 1.36 |
| Q2 | 1.46 | 2.89 |
| Q3 | 3.17 | 5.38 |
| Q4 | 10.86 | 14.75 |

`elements_total` and `connections_total` are retained as reported descriptors of
each selected diagram but are not the binning variable.

## 6. Repository-disjoint sampling

Selected repositories are reserved from any future fine-tuning training set.
Within the test set, at most 5 diagrams are drawn per repository, to prevent a
single large project's stylistic conventions from dominating a stratum.

### 6.1 Feasibility

Per-cell capacity (distinct diagrams available after the 5-per-repository cap)
exceeds the 125-per-cell target by more than fortyfold in every cell, confirming
the 1,000-diagram target is unconstrained by pool size:

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| class (cap@5) | 6,840 | 10,273 | 11,507 | 12,439 |
| sequence (cap@5) | 6,844 | 6,665 | 6,727 | 5,461 |

## 7. Image standardization for inference

Every test image is pre-resized to a single standard prior to
inference (aspect ratio preserved), and the identical image is sent to all
models (controlled comparison). The standard is set at the lowest common
*effective processing* resolution across the model set. A distinction is drawn
between a provider's maximum *accepted* dimensions (an upload gate that rejects
larger files) and its *native processing* resolution (the size at which the
image is actually encoded; larger inputs are silently downscaled to it):

| Model | Native processing resolution | Max accepted |
|---|---|---|
| GPT-5.x (high detail) | ~2,048 px long edge (tiled) | — |
| Gemini 3.1 Pro (media_resolution HIGH) | ~1,536 px long edge | — |
| Claude Opus 4.6 | **1,568 px long edge (~1,568 tokens, ~1.19 MP)** | 8,000 x 8,000 px |
| Qwen3.5 / Qwen3-VL (hosted) | configurable, ceiling ~16 MP (16,384 tokens) | ~16 MP |

The binding floor is **Claude Opus 4.6 at a 1,568 px long edge (~1.19 MP)**.
Per the Claude vision documentation, high-resolution support (2,576 px long
edge) exists only on Claude Opus 4.7/4.8; Opus 4.6 falls under "other models"
and downscales any larger input to a 1,568 px long edge / ~1,568 image tokens
(`width x height / 750`), confirmed by the documented cost table (1,092 x 1,092
through 2,000 x 1,500 px all map to the ~1,568-token ceiling).

Working standard: **long edge 1,568 px (~1.19 MP)**, Lanczos downscaling, PNG
(lossless, preserving text legibility). This is the lowest native processing
resolution among the four models and therefore the highest resolution every
model can receive identically under the controlled-comparison constraint. The
future fine-tuned Qwen will be run at this same resolution to preserve
baseline-to-fine-tuned comparability.

The hosted Qwen path (Featherless, all three sizes Qwen3.5-2B/9B/27B) encodes
this standard without downscaling: black-box probes via
`util/probe_image_tokens.py` (2B/9B 2026-06-11; 27B 2026-06-12) show the
returned image-token count growing linearly with pixel count and matching the
Qwen3.5 expectation `round32(W)·round32(H)/32²` through the 1,568 px standard
(27B: 2,404 observed vs 2,401 expected at 1,568²) and beyond (full-size
encoding observed at 4,000², ~16 MP).

Legibility is reported, not filtered: a per-tier crowding descriptor (e.g.
`content_lines` per megapixel after resize to the 1,568 px standard) quantifies
how far the dense Q4 diagrams are downscaled below their native resolution,
supporting interpretation of the degradation curve.

## 8. Deduplication

The corpus is deduplicated by exact SHA-1 content hash only; near-duplicates
differing in whitespace or comments persist. A normalized-code deduplication
(remove block `/' '/` and full-line `'` comments, collapse all whitespace, then
SHA-1 hash; keep the first occurrence in corpus order) is applied during
selection. On the post-degeneracy pool it removes **2,018** class and **1,452**
sequence near-duplicates, leaving **68,459** class and **33,189** sequence
diagrams. As anticipated, the step is not capacity-binding (per-cell pool still
exceeds the 125 target by >60x).

## 9. Type-agreement filter

A diagram enters the set only if its corpus `primary_type` label (LLM-assigned)
agrees with the diagram type independently determined by the PlantUML parser. The
parser (the DiagramStatsExtractor fork at https://github.com/vovanrew/plantuml,
branch `stats-extractor-graph`) reports a
`diagram_type` per source; a diagram is retained iff
`parser.diagram_type == primary_type`. The filter is applied after deduplication,
on the per-type pools.

On the post-dedup pool it removes **128** class diagrams (parser-labeled
component 105, sequence 17, state 4, activity 2) and **309** sequence diagrams
(activity 192, component 93, class 20, state 4), leaving **68,331** class and
**32,880** sequence. The step is not capacity-binding (per-cell pool still
exceeds the 125 target by >60x). Every ground-truth diagram in the set therefore
parses to the structural-graph type the benchmark scores, and structural-metric
extraction is defined on all ground truth.

## 10. Sampling protocol

For each type t in {class, sequence}:
1. Apply inclusion criteria (Section 3) and degeneracy exclusions (Section 4).
2. Apply normalized-code deduplication (Section 8).
3. Apply the type-agreement filter (Section 9).
4. Compute `content_lines` quartile thresholds on the resulting pool.
5. Within each quartile tier, draw a stratified random sample of n=125 under a
   fixed seed, subject to the <=5-per-repository constraint.

The final artifact is the committed list of filename keys, with fixed random
seed and the per-type quartile thresholds recorded for reproducibility.

## 11. Open items

- Normalized-code deduplication: implemented in `build_test_set.py` (see Section 8).
- Image standard pixel budget on Qwen3.5-27B: confirmed 2026-06-12 (see §7).
- Qwen hosting availability: confirmed (all three sizes live on Featherless).
  Gemini GA snapshot: none exists as of 2026-06-11; the preview id and run
  date are recorded together (benchmark-protocol.md §3).
