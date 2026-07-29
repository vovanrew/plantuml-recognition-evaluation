# Qualitative error analysis — zero-shot image→PlantUML benchmark

> Hand-written companion to `results_explained.md`. Where that document reports *what* the
> metrics say, this one reports *why*: a categorized review of 40 failure cases drawn from the
> stratified failure index, each citing a real `model + key`. Categories are stated in the terms
> the metrics count (`methodology/evaluation-framework.md`). This file is not machine-generated;
> the case findings behind it were produced by reading, for every case, the ground-truth `.puml`,
> the prediction, and the exact input PNG shown to the model, and were each re-checked by an
> independent second pass.

## 1. Method

### 1.1 Failure population

The review draws on the stratified failure index (`analysis/out/failure_index.{md,json}`, 233
cases, `--per-cell 2`, seed 20260614), which classifies every test diagram into one of three
mutually exclusive outcome classes (`methodology/analysis-protocol.md` §7):

- **`provider_drop`** — no prediction stored (timeout / non-response). Available counts (Exhibit 8):
  qwen3.5-2b 25, gpt-5.2 1, qwen3.5-27b 1; none elsewhere. A reliability bucket, not content error.
- **`compile_fail`** — a prediction exists but does not render. Available counts: gpt-5.2 64,
  claude-opus-4-6 59, gemini-3.1-pro 28, qwen3.5-2b 774, qwen3.5-9b 569, qwen3.5-27b 398,
  qwen3.5-397b-a17b 213. Within this class the `csr_error` is either `no PNG produced` (block
  isolation found no closing `@enduml` — runaway/truncation) or `Error line N …` (a genuine syntax
  fault). Across the 233-case index these split ≈ 25 no-`@enduml` to ≈ 82 line-errors.
- **`compiled_low_structural`** — renders, but per-diagram Element **or** Relationship F1 < 0.5.
  Available counts: gpt-5.2 94, claude-opus-4-6 120, gemini-3.1-pro 53, qwen3.5-2b 100,
  qwen3.5-9b 201, qwen3.5-27b 104, qwen3.5-397b-a17b 122. Within the index this class is driven
  overwhelmingly by **Relationship** F1 (107 of 112 indexed cases have relationship F1 < 0.5; only
  34 have element F1 < 0.5; 29 both). Its `relations_missed` (FN edge types, pooled) are dominated
  by `message` (53), then `inheritance` (27), `association` (20), `composition` (15),
  `aggregation` (13), `dependency` (9); its `relations_extra` (FP edge types) by `message` (38),
  **`dependency` (34)**, `association` (32), `inheritance` (24), `composition` (6), `aggregation`
  (5). Dependency is rarely *missed* but heavily *over-produced* — a wrong-type fingerprint
  examined in §3.5.

### 1.2 Sample (40 of 233)

Forty cases were selected deterministically (the sampler in §1.4) to span **all 7 models, both
diagram types, all 4 tiers, and all 3 outcome classes**, weighting toward failure-rich cells (the
weak Qwen rungs, tier 4) while deliberately retaining the rarer **frontier** failures, which
reveal the residual hard cases. Composition as drawn from the index:

| Model | provider_drop | compile_fail | compiled_low_structural | total |
|---|---|---|---|---|
| gpt-5.2 | 1 | 2 | 3 | 6 |
| claude-opus-4-6 | 0 | 2 | 3 | 5 |
| gemini-3.1-pro | 0 | 2 | 3 | 5 |
| qwen3.5-2b | 2 | 3 | 2 | 7 |
| qwen3.5-9b | 0 | 3 | 3 | 6 |
| qwen3.5-27b | 1 | 2 | 3 | 6 |
| qwen3.5-397b-a17b | 0 | 2 | 3 | 5 |
| **total** | **4** | **16** | **20** | **40** |

By type: 23 class / 17 sequence. By tier: 12 / 8 / 7 / 13 (T1–T4). The cell coverage is consistent
with Exhibit 8 (every model × outcome cell with available cases is represented).

### 1.3 How each case was worked, and verified

For every case the ground-truth `.puml`, the prediction (`compile_fail`/`low_structural` only), and
the **input PNG actually shown to the model** were read; for `compile_fail` cases the renderer error
line was mapped against the *extracted* `@startuml…@enduml` block (line numbers refer to that block,
not the raw output), and several were re-rendered with `plantuml-1.2025.9.jar` to confirm the
offending token. Each classification was then **independently re-derived** by a second pass that
re-read the same files and the recorded `tp/fp/fn` deltas and checked for any case that contradicts
its own metrics (the analysis-protocol STOP condition). Outcome: **38/40 independently verified
(37 with evidence confirmed exact; 1 corrected — `0b04c29e`, see §3.6; 38/38 category agreement;
0 metric-contradictions).** Two cases (the shared key `013f262f` on qwen-27b and qwen-397b) did not receive the
independent second pass, but each carries extractor-reproduced deltas and the two
corroborate one another (§3.5). Every claim below cites a real `model + key`; no example is
invented.

### 1.4 Reproducibility

Selection is deterministic from the committed index: for each (model × outcome) quota the sampler
greedily maximizes diversity of (type, tier) and of the per-case signal (for `compile_fail`,
no-`@enduml` vs line-error; for `low_structural`, element-miss / wrong-type / missed-edges /
type-confusion), iterating the index in its stored seeded order. Re-running
`python3 analysis/build_failure_index.py` regenerates the 233-case pool byte-identically; no CLI
flags were changed for this review.

## 2. Taxonomy

Each case is assigned **one primary category** (its dominant defect); co-occurring defects are
recorded as secondary. Categories are grouped by the kind of failure: **reliability** (no usable
output), **generation/compilation** (output does not render), **structural/semantic** (renders but
the graph is wrong), and **measurement** (the metric, not the model, produced the low score). The
sample is stratified, so the primary-count column is **not** a population frequency — population
context is the "Concentrates in" column (from Exhibit 8 / §1.1).

| # | Category | Primary (n=40) | As secondary | Metric(s) hit | Concentrates in |
|---|---|---|---|---|---|
| R | **Provider drop / non-response** | 5 | — | all (absence → 0) | qwen-2b (25 avail.); trace on gpt-5.2, qwen-27b; one gemini safety-filter case |
| C1 | **Syntax / compile error** | 9 | 1 | CSR | every model; near-misses on frontier, gross on weak Qwen |
| C2 | **Runaway / truncation** (no `@enduml`) | 5 | — | CSR | qwen-2b/9b; also qwen-27b and 397B at tier 4 |
| C3 | **Diagram-type / family confusion** | 4 | 3 | CSR + Relationship F1 + type acc | qwen-2b/9b on **sequence** (lifelines→rectangles) |
| S1 | **Wrong relation type** | 4 | 5 | Relationship F1 | all models; the composition/aggregation/dependency tail |
| S2 | **Missed relations** (incl. messages-as-notes) | 3 | 12 | Relationship F1 | tier-4 class (frontier) + Qwen note-substitution |
| S3 | **Hallucinated elements** | 3 | 7 | Element F1 | Qwen (enum-literal / note explosion); gpt-5.2 stereotype→interface |
| S4 | **OCR / text / name misread** | 2 | 8 | Element F1 + chrF++ (cascades to Rel. F1) | sequence endpoint names (`:Instance`, accents) |
| S5 | **Type / stereotype confusion** | 0 | 11 | type accuracy | always co-occurs with C3/S1 |
| S6 | **Control-flow loss** (alt/opt/loop) | 0 | 3 | chrF++ | sequence tier 4 |
| S7 | **Missed elements** (pure) | 0 | 14 | Element F1 | none pure — always cascade or naming (§4.5) |
| M | **Measurement / normalization artifact** | 5 | 5 | Element / Relationship F1 | **frontier residual `low_structural`** + Qwen notes-as-nodes |

Two categories from the starting scheme have **zero primary cases** in this sample, which is itself
a finding: pure **missed-element** failures (S7) and standalone **type-confusion** (S5) never
*dominate* a case — they appear only as consequences of a compile-cascade, a name-key break, or a
diagram-family swap. **Refusals / non-attempts** did not occur at all (the one zero-output safety
event, §3.1, is a filter block, not a refusal in the prediction text).

## 3. Per category, with representative cases

### 3.1 Provider drop / non-response (R) — reliability, not content

No prediction was stored, so every metric scores by absence. Two mechanisms, both confirmed from the
raw response records:

- **Runaway-to-deadline on the smallest rung.** `qwen3.5-2b 09bde3e2f993` (sequence, T4): raw record
  `{"error":"timeout", "detail":"hard deadline 600s"}` — the 2B model ran the full 600 s deadline on
  a CJK-heavy tier-4 image and stored nothing; the 5 participants and 11 messages all score FN. This
  is the §8 "runaway no-stop generation" mechanism reaching the wall-clock cap instead of the token
  cap.
- **Transient drop on a trivial diagram.** `gpt-5.2 b3d43297c56f` (class, T1): raw record
  `{"error":"timeout", "detail":"hard deadline 90s"}` on a **13-line, single-class** Cyrillic diagram
  (`«Отчеты» Анализ причин проигрыша сделок`). The input PNG is the easiest possible case (one box,
  fully legible), so this is a provider-side reliability event, **not** a capability failure — yet it
  contributes element FN=1 to the honest all-1000 aggregate.
- **Safety-filter zero-output, mis-binned as compile_fail.** `gemini-3.1-pro 1067b9cef0f7` (class,
  T3) is recorded in the index as `compile_fail / "no PNG produced"`, but the raw Gemini response is
  `finishReason="RECITATION"`, empty content, `totalTokenCount == promptTokenCount` (zero completion
  tokens). A 0-byte prediction file was written (rather than left null), so it escaped the
  `provider_drop` bucket although it is functionally one. It is a Gemini-specific copyright-filter
  drop and should be tallied with the reliability events, not with syntax failures.

Other drops reviewed: `qwen3.5-2b 2ba4e7f17f9f` (same key Opus *compile-fails* on, §3.2) and
`qwen3.5-27b 938e9cc0e6b8` (a 5-participant, 20-message diagram with full alt/else/loop scaffolding
lost wholesale). The qwen drops match the documented Featherless image-bearing-concurrency drop
behaviour and are expected to clear on resume passes; they carry no signal about model capability.

### 3.2 Syntax / compile error (C1) — on the frontier, one bad token on correct content

This is the dominant frontier `compile_fail` mode, and its signature is striking: **a structurally
and textually correct answer reduced to all-zero by a single illegal token.** All four frontier
syntax cases were re-rendered to confirm a one-edit fix:

- `gpt-5.2 05af3d5892f5` (sequence, T2): the prediction declares all **11 participants** and
  reproduces all **14 messages** (chrF++ 81.2), but prepends `left to right direction` (line 2) — a
  layout directive invalid in sequence diagrams. Deleting that one line renders cleanly; with it, the
  parser rejects the participant block and Element/Relationship F1 are both 0.
- `claude-opus-4-6 2ba4e7f17f9f` (sequence, T2): uses `spm <.. EventBus : …`, the class-diagram
  dotted-dependency arrow, where a sequence message arrow is required. `<..` → `<--` (one character)
  renders; as written, fail-fast halts at line 15.
- `claude-opus-4-6 50efbc2a904f` (class, T3): `Amount ..> User :` — a dependency edge with a dangling
  colon and **empty label**. `Amount ..> User` renders; the trailing `:` alone yields
  "Syntax Error? (Assumed diagram type: class)".
- `gemini-3.1-pro 09ba2de07109` (class, T1): `class ClassDefinition as c1` — an **unquoted** display
  name combined with the `as` alias keyword. `class "ClassDefinition" as c1` renders; the model had
  both nodes, both edges, and both directions correct (`c1 --> c2`, `c2 -up-|> c1`).

On the weak Qwen rungs the same category is **gross**, not near-miss: `qwen3.5-2b 1067b9cef0f7`
splits `class Character` / `as Character` across two lines (orphan `as Character` at line 3) while
also mixing sequence constructs (`participant`, `<<interface>>`, `include "Character.h"`) into a
class diagram; `qwen3.5-2b 187969222acb` fuses keyword and arrow as `class User <|-- Teacher`; the
397B's `474f51755545` invents a brace-delimited `frame "Virologist wear gloves" { … }` grouping that
does not exist in sequence PlantUML, preceded by ~80 lines of invented skinparams
(`skinparam noteSynergy true`, …). The contrast is the point: **frontier CSR loss is formatting
slips on otherwise-correct content; Qwen CSR loss is malformed generation.**

### 3.3 Runaway / truncation (C2) — degenerate loops to the token cap

The `no PNG produced` cases are dominated by non-terminating repetition that never emits `@enduml`:

- `qwen3.5-2b 4dc97fd76002` (sequence, T1): emits `@startuml` then
  `skinparam UMLActor labelStyle "bold"` ~480 times, truncating mid-token at the cap (`skinparam U`).
  chrF++ 1.36 — no diagram content at all.
- `qwen3.5-9b 01325068fa93` (class, T4): the only non-`skinparam` lines are `@startuml` and
  `left to right direction`; lines 9–458 are one 5-line `classIcon*` skinparam cycle repeated to the
  cap; `@enduml` count = 0.
- `gpt-5.2 5922ccf81ce2` (class, T1): a frontier exception — having correctly transcribed the one
  class (`«РегистрыСведений» Взаимозависимые лица`) and its member, it then loops the escaped-space
  token `\ ` thousands of times trying to reproduce a right-aligned wrapped label, consuming context
  before `@enduml`. A rendering-cosmetic trigger, not a content failure.
- `qwen3.5-27b b2fe8e9f55ef` (class, T4) and `qwen3.5-397b-a17b 2830a2eabd8a` (sequence, T4): both
  collapse into repetition (a hex string and an alphabet-cycling `skinparam participant<<X>>` block,
  respectively) with no body. These are the same no-`@enduml` runaway failure the small rungs
  show, surfacing here at tier 4 on the larger Qwen sizes.

This category is the case-level face of the §8 token-footprint result (the 2B/9B emit 3–5× the
frontier's output): the excess output *is* these loops, and they are the proximate cause of the weak
rungs' compile failures and timeouts.

### 3.4 Diagram-type / family confusion (C3) — sequences reparsed as component/class diagrams

A distinctly Qwen failure, and the case-level mechanism behind the §7 **sequence asymmetry** (9B CSR
20.6% on sequence vs 65.6% on class). The model emits the right names and arrows but in the wrong
diagram *family*, so participants become rectangles and messages become associations:

- `qwen3.5-9b 21b4a540ef03` (sequence, T3): GT declares `participant`/`queue` lifelines inside a
  `box DomainModel`; the prediction replaces them with `rectangle "UIBFF" as UIBFF` … nested in
  `rectangle "DomainModel" { }` plus `left to right direction`. With no participants, all 16 messages
  reclassify message→association: `relations_missed=[message]` (16 FN), `relations_extra=[association]`
  (16 FP), Relationship F1 = 0, type accuracy 0/9 — while Element F1 stays 1.0 and chrF++ 81.3. High
  surface fidelity **masks a total topology failure.**
- `qwen3.5-2b 04a41abf900a` (sequence, T3): same swap (`interface "Kjedesystem"`, `rectangle` group
  boxes, undirected `--` associations); 14 messages all missed, 12 spurious associations, plus two
  hallucinated group-label nodes from the rectangle captions.
- `qwen3.5-27b 2b81c26799a6` (sequence, T4) shows the *compile-failing* variant: `left to right
  direction` (line 2) and `rectangle "…" as admProcess` (line 17) flip the parser into component-mode
  so the first `participant` (line 12) is rejected — a family confusion that manifests as a syntax
  error rather than a mis-typed graph.
- `gpt-5.2 13535b2cbd8a` (sequence, T1): even a frontier model is not immune — on a *degenerate*
  sequence (5 lifelines, **zero messages**) it switches to a component layout and emits each
  participant **twice** (`A1/W1/D1` then `A2/W2/D3/D4`), the doubling induced by the top-and-bottom
  lifeline rendering. Element F1 0.667 (5 TP + 5 FP duplicates), type accuracy 0/5.

### 3.5 Wrong relation type (S1) — the composition/aggregation/dependency collapse

This is the category that explains the §6 quantitative finding (composition, aggregation, dependency
are the hardest relations for every model). The endpoints and often the direction are right, but the
**decoration is wrong**, so the `(source, target, type)` key fails:

- `qwen3.5-9b 2399ddf66f2d` (class, T1): both GT edges are composition (`Fruta *-- Tallo`,
  `Fruta *-- Piel`, filled diamonds clearly visible in the PNG); the prediction draws them as
  inheritance (`Fruta --|> Tallo`, triangle heads). `relations_missed=[composition]`,
  `relations_extra=[inheritance]`, Relationship F1 = 0 — the canonical type-substitution signature.
- `qwen3.5-2b 289412e14085` (class, T1): GT association `ParameterAnnotation --> Attribute` rendered
  as dependency `ParameterAnnotation ..> Attribute` (solid → dashed). Identical endpoints/direction;
  the dashed-line substitution is exactly why **`dependency` is the most over-produced edge type**
  (34 FP across the index, §1.1).
- `qwen3.5-27b 013f262fafb9` and `qwen3.5-397b-a17b 013f262fafb9` (class, T4 — **same diagram, both
  large Qwen**): the most severe form. The 397B renders **all 18 GT relations as a generic `-->`** —
  7 compositions, the aggregations, and even an inheritance (`TDelClignotteTemp <|-- TDel` →
  reversed association) flattened to plain association; the 27B emits **23 `..>` dependency arrows
  where GT has zero**, and not a single composition or aggregation marker despite 8 in GT. Total
  relation-type-vocabulary collapse (Relationship F1 0.17 and 0.0). Both also misread hub-class names
  (`TGestionnaireDels`→`TCaptionnaireDels`, accents inserted: `TEtatDel`→`TÉtatDel`) and externalize
  legends as `note` blocks (see M, §3.10). The two runs independently reproduce each other's failure
  mode on the same image.

### 3.6 Hallucinated elements (S3) — stereotype tags and enum members promoted to nodes

The model invents nodes (and the edges that wire them), inflating Element FP:

- `qwen3.5-9b 0806d963c5e7` (class, T2) — **enum-literal explosion**: a single GT enum's members each
  became a standalone class wired by a spurious association (`A18 --> UKPT`, `A18 --> E3DC`, …) — 19
  invented nodes, 19 FP association edges, Element F1 0.1. The one extra node `E` is the encircled
  enum-type icon misread as a literal.
- `gpt-5.2 0b04c29eb903` (class, T4) — **stereotype-text→interface**: the GT writes 16 step-interface
  names only as `<<…>>` stereotype tags on its class boxes; GPT-5.2 promotes all 16 to standalone
  `interface` nodes (`IAllocationStrategyStep`, `IPluginStep`, …) wired by 16 spurious `..|>`
  inheritance edges. *(The second-pass verifier corrected the FP arithmetic here: of the 22 element
  FP, 16 are these interfaces and the remaining 6 are the model's real `final X` classes failing the
  name key against GT's markdown-bold `**final** X` — a measurement artifact, M/§3.10 — so the
  genuine hallucination is the 16 interfaces, and the case also downgrades 5 GT compositions to
  aggregation, an S1 component.)*
- `qwen3.5-397b-a17b 119e0cad229d` (class, T1): on a single-class diagram the 397B hallucinates a
  `note` node containing `<b>С</b>` (the green circled-"C" class icon misread) plus a spurious
  `dependency` edge from it — and since GT has **zero** edges, that one phantom edge drives
  Relationship F1 to 0 (see §4.4 on brittleness).

### 3.7 Missed relations (S2) — including the "messages-as-notes" representation choice

Edges present in GT are simply absent as edges in the prediction:

- `qwen3.5-27b 0b185a3b2c5e` (sequence, T4): the model **understood every message but rendered all 34
  as notes** (`note right of NS1: 1 启动 NameServer 服务器`, …) with no arrow tokens anywhere.
  `relations_missed=[message]` with `relations_extra=[]` — the empty *extra* list rules out a
  name-cascade or reversal (those put `message` in both lists) and confirms a clean wholesale drop.
  Relationship F1 = 0 while Element F1 = 1.0: a representation choice, not a comprehension failure.
- `qwen3.5-397b-a17b 0c347826efa0` (class, T2): both substantive class relationships (one inheritance,
  one realization) are recovered perfectly; Relationship F1 0.4 collapses entirely on the **four
  note-attachment dependency edges** — GT wires each `note` to two classes, the model attaches each to
  one and reverses direction, so `relations_missed=[dependency]` and `relations_extra=[dependency]`.
- `claude-opus-4-6 145fbd18e198` (class, T4) is the frontier's genuine tier-4 structural difficulty:
  **0 of 8** inheritance+composition edges recovered (no `<|--`/`*--` emitted at all), 11 invented
  associations, interfaces declared as `class <<I>>` — Relationship F1 0.15 even though Element F1 0.9
  and chrF++ 75. Names and member text survive; typed structure does not.

### 3.8 OCR / text / name misread (S4) — and the sequence endpoint-name cascade

Mis-transcribed names break the name-key directly, and on sequence diagrams the break **cascades**
through every incident message:

- `qwen3.5-27b 18a145261879` (sequence, T3): the model drops the leading `:` from four `:Instance`
  lifeline names (`:Main UI` → `Main UI`, etc.). Those four nodes split into 4 FN + 4 FP (Element F1
  cascades), and because every one of the 10 GT messages touches a renamed participant, **all 10
  message keys fail** → Relationship F1 = 0 with `message` in both missed and extra. One stylistic
  transcription choice zeroes the relationship metric.
- `gemini-3.1-pro 1348037e5ef8` (class, T4): the model emits valid code *identifiers*
  (`equalwidth`, `td4c_kullback_leibler`) for GT's quoted multi-word *display strings*
  (`"Equal Width"`, `"TD4C Kullback-Leibler"`); lowercase+trim does not collapse spaces/hyphens, so 7
  entities split into 7 FN + 7 FP and 6 inheritance edges cascade. Structurally faithful; penalized on
  name normalization (this case sits on the S4 / M boundary — the misread is the model's, the
  non-collapse is the metric's).

### 3.9 Type/stereotype confusion (S5) and control-flow loss (S6) — secondary, never dominant

Neither category is the *primary* defect in any sampled case, but both recur as secondary:

- **Type/stereotype confusion** (11× secondary) is always downstream of C3 or S1: when sequences
  reparse as components every lifeline flattens to `description`/`rectangle` (type accuracy 0/9 in
  `qwen3.5-9b 21b4a540ef03`); when relations are mis-typed the endpoint kinds drift too
  (`interface`→`class <<I>>`, `enum`→`class <<C>>` in `claude-opus-4-6 145fbd18e198`, type accuracy
  5/18). The frontier's strong type-accuracy headline (Gemini 0.984) reflects that, *when names match
  and the family is right*, UML kind is usually right too.
- **Control-flow loss** (3× secondary) — `alt`/`else`/`loop`/`ref` scaffolding — appears where the
  whole prediction is lost (`qwen3.5-27b 938e9cc0e6b8`, R) or where messages are dropped
  (`qwen3.5-27b 0b185a3b2c5e`, S2). It is invisible to the structural metrics (which emit the
  contained messages unchanged) and surfaces only in chrF++, exactly as the framework intends.

### 3.10 Measurement / normalization artifact (M) — the frontier's residual "failures"

A distinct and important class: the prediction is visually and semantically correct, but the
*scoring* produces a low structural F1. These dominate the **frontier** `low_structural` cases and
were each verified on the exact GT (and several cross-model):

- **Unstripped creole/markup in GT node names.** Key `0bffda3c5610` (one Java enum
  `ConquestMapPart`) appears as a `low_structural` failure for **all three frontier models**
  (`gpt-5.2`, `claude-opus-4-6`, `gemini-3.1-pro`). The GT node name is
  `<b><size:14>ConquestMapPart</b> <size:10>soen6441riskgame.enums`. The name normalizer strips
  `<<…>>`/`«…»` stereotypes but **not** single-angle creole tags (`<b>`, `<size:…>`) or the package
  subtitle (per framework §2.1, single brackets are kept). Opus and Gemini both emit the clean
  `enum ConquestMapPart`; their correct output therefore cannot match the marked-up GT key →
  Element F1 = 0. A shared-frontier scoring artifact, not three independent comprehension failures.
- **Spot-stereotype letter prefix.** `gemini-3.1-pro 32b85a4b1e1c` (sequence, T3): GT uses the
  `<< (C,#ADD1B2) @Controller >>` spot form, which the extractor folds to a node name beginning with
  a bare `C` *outside* the `<<…>>` token. The normalizer removes `<<@Controller>>` but the leftover
  `c` survives, so all 4 stereotyped participants are unmatchable for the whole panel; their 10
  messages then cascade to Relationship F1 = 0 (chrF++ 84 confirms the content is right).
- **Notes counted as nodes/edges.** The extractor counts a `note` block as a node (type `note`) and a
  note attachment as a `dependency` edge. Qwen models that externalize legends/members as notes are
  charged FP on both metrics: in `qwen3.5-397b-a17b 013f262fafb9`, **13 of 16 element FP and 13 of 25
  relationship FP** are externalized notes, overstating genuine hallucination; `0c347826efa0` (§3.7)
  and `119e0cad229d` (§3.6) are smaller instances.
- **Dotted-FQN / namespace separator.** `gpt-5.2 0bffda3c5610` — the same enum diagram as above, but
  GPT-5.2's *own* output triggers a different break: it omits `set namespaceSeparator none`, so the
  `.` in its display name `soen6441riskgame.enums` is read as a namespace separator and the leaf node
  becomes `enums` (nested under a grouping container, which is not a node). The transcription was
  faithful (chrF++ 54.5); the name-key failed on a formatting omission. (So this one key fails on
  *all three* frontier models — Opus/Gemini on the GT-side creole markup, GPT on its own dotted-name
  nesting.)
- **Degenerate GT.** `claude-opus-4-6 1010a06e412b` (sequence): GT routes all 5 messages to `:Board`
  while declaring `pawn`/`draught` lifelines that are never messaged; Opus reroutes 4 messages to the
  more sensible `Pawn`/`Draught` targets and is scored 4 FN + 4 FP (Relationship F1 0.20) for a
  defensible reading of an oddly-authored GT.

These artifacts matter for interpretation (§4.3): they are concentrated in precisely the frontier's
*residual* structural gap, so a meaningful share of the frontier's distance from a perfect score is
measurement, not model error. They are candidates for a normalization refinement before final
scoring (strip creole/`<size>`/`**bold**` and the spot-letter prefix from node names; optionally
exclude `note` nodes from the structural denominators) — a decision for the author, recorded here as
an observation, not a change.

## 4. Cross-cutting observations

### 4.1 Frontier vs Qwen — the failures are categorically different

The two arms fail in different *kinds*, which is why §1–§5 of `results_explained` treat them as two
arms rather than one ranking:

- **Frontier** failures are (a) **rare**, (b) **near-misses** — a single illegal token on otherwise
  correct content (C1: `05af3d58`, `2ba4e7f1`, `50efbc2a`, `09ba2de0`), and (c) when structural,
  **largely measurement artifacts** (M: `0bffda3c`, `32b85a4b`, `1348037e`). The genuine residual
  frontier difficulty is narrow: dense **tier-4 class** topology (`claude-opus-4-6 145fbd18e198`, 0/8
  typed edges recovered) and a degenerate-sequence doubling reflex (`gpt-5.2 13535b2c`). This is the
  case-level explanation of the near-zero population gap (Exhibit 3: Gemini +0.016 / Opus +0.031 /
  GPT +0.042): there is no easy subset to hide in because the failures are not capability cliffs.
- **Qwen** failures are **gross and generative**: runaway loops (C2), wrong-family reparses (C3),
  malformed syntax (C1), and wholesale relation-type collapse (S1). These *are* difficulty-correlated,
  which is why the weak rungs show the large population gap (Exhibit 3: 2B +0.632, 9B +0.354) — they
  compile only the easy diagrams and fail the hard ones outright.

### 4.2 Why composition / aggregation / dependency score low (§6), case by case

The §6 per-relation result — inheritance and messages easy, composition/aggregation/dependency hard —
is explained almost entirely by **S1 (wrong relation type)**, not by missed edges. Models keep the
topology but substitute the decoration: filled-diamond composition → triangle inheritance
(`qwen3.5-9b 2399ddf6`) or plain association (`qwen3.5-397b 013f262f`); solid association → dashed
dependency (`qwen3.5-2b 289412e1`); and dependency is *over*-produced (34 FP vs 9 FN across the index)
because models default rare relations to `..>` and because note-attachments are scored as dependency
edges (M). The visual cues that distinguish these — filled vs hollow diamond, dashed vs solid line,
triangle head — are exactly the fine decorations a model must read off a crowded render, so they fail
where the bulk relations (inheritance triangles, sequence arrows) succeed.

### 4.3 What "compiled but low-structural" really is

The index's own composition (107/112 relationship-driven, only 34 element-driven) is borne out:
**Relationship F1 is the binding structural metric.** And among the relationship collapses, a large
fraction are not "the model missed the structure" but one of: the diagram family was wrong (C3), the
relation type was substituted (S1), a single name misread cascaded through every message (S4), or the
extractor scored notes/markup against the model (M). Genuine *missed* structure that a human reader
would also call missing is the minority (`145fbd18`, `0b185a3b`). Element-F1 loss is even more often
non-substantive: **no sampled case is a pure missed-element failure (S7 = 0 primary)** — element FN is
always a compile/drop cascade or a name-key break.

### 4.4 A metric brittleness worth flagging: zero-edge ground truths

When a GT has **no edges**, Relationship F1 is 1.0 if the prediction also has none, but collapses to
**0.0 on a single spurious edge** regardless of magnitude. `gpt-5.2 13535b2c` (9 FP associations from
a component reparse) and `qwen3.5-397b 119e0cad` (one phantom note→class dependency) both score
Relationship F1 = 0 on diagrams that genuinely contain zero relations. This inflates the count of
"relationship failures" on simple diagrams; the honest reading is that these are element/family
errors, not relation errors.

### 4.5 By tier — the collapse is loops and crowding

The §7 per-tier degradation (steep for weak rungs, near-flat for frontier) shows in the cases as: at
tier 4 the weak/mid Qwen rungs fall into runaway loops (`qwen3.5-9b 01325068`, `qwen3.5-27b b2fe8e9f`,
`qwen3.5-397b 2830a2ea` — all C2) and compound structural failures on the densest renders
(`013f262f` at 50 lines/MP crowding, where hub-class names are misread *and* every relation is
mis-typed *and* legends become notes — three categories at once). The frontier degrades gently and
mostly via M-artifacts and the one genuine dense-class case. Tier 4 is where reliability (C2) and
structure (S1+S4+M) failures stack.

### 4.6 Sequence vs class

Consistent with Exhibit 5: the **diagram-family confusion (C3)** is the sequence-specific killer for
small/mid Qwen and is the mechanism behind the 9B sequence collapse (20.6% CSR). Class diagrams fail
more through relation-type substitution (S1) and hallucinated elements (S3). The 397B's relative
*strength* on sequence (Exhibit 5: 84.0% vs 73.4% class) is visible too — its sequence failures here
are non-termination runaways (`2830a2ea`) rather than comprehension errors, whereas its class
failures are genuine relation-type collapses (`013f262f`).

## 5. Implications for fine-tuning (Qwen target)

The benchmark's purpose is to motivate fine-tuning the Qwen arm; the failure modes above map directly
to a training-data mix and objectives. In rough priority order:

1. **Termination / well-formedness first.** The single largest source of weak-rung failure is
   degenerate non-termination (C2: skinparam/escaped-space/hex loops to the cap) and the drops they
   cause (R). The §3 result that "scale buys *compiling at all*, not per-diagram polish" says the
   binding constraint is reliability. SFT on complete, well-formed PlantUML (every example ending in
   `@enduml`, no skinparam padding) and an explicit penalty on non-termination targets this directly,
   and should also shrink the population gap.
2. **Diagram-family discipline (sequence).** The C3 reparse (lifelines→`rectangle`, messages→
   association, stray `left to right direction`/`frame "X" {`) is the sequence-specific collapse. The
   training mix must over-represent **sequence** diagrams with correct `participant`/`actor`/`->`
   syntax and teach that class/component layout directives are not sequence constructs. This is the
   highest-leverage fix for the 9B sequence asymmetry.
3. **Relation-type vocabulary — the largest structural headroom.** S1 (composition/aggregation/
   dependency → generic association or `..>`) is *the* reason the rare relations score low (§6, §4.2).
   Training should over-sample the diamond/dashed/triangle decorations and pair them with their
   visual cue, so the model learns the (rendered-decoration → relation-type) mapping rather than
   defaulting to association. Expect the biggest Relationship-F1 gains here.
4. **In-class members over externalized notes.** Qwen's habit of exporting members/legends as `note`
   blocks and rendering messages as notes (S2/M: `0b185a3b`, `0c347826`, `013f262f`) both loses
   structure and is charged as FP. Prefer in-class member compartments and real message arrows.
5. **Icon and stereotype reading.** Enum-literal explosion (`0806d963`) and class-icon "C" misreads
   (`289412e1`, `119e0cad`, `013f262f`) show the model mis-parsing the encircled type-icon and
   stereotype semantics. Include examples that pair the icon/stereotype with the correct entity kind
   and members so literals are not promoted to nodes.
6. **Name fidelity on UML notation.** The `:Instance` colon-prefix drop (`18a145261879`) and
   multi-word display names should be in the data so endpoint names survive — on sequence diagrams a
   single endpoint misread zeroes Relationship F1 (S4 cascade).

The frontier arm needs no such work; its rare failures are formatting slips and measurement
artifacts. Two **benchmark-side** items the cases surfaced (for the author to weigh before final
scoring, not training): the name-normalization gap on creole/`**bold**`/spot-stereotype markup and
the notes-as-nodes/edges counting (M, §3.10) systematically depress structural F1 for *correct*
predictions across the panel — most visibly for the frontier, whose true comprehension is right.

## 6. Coverage cross-check

The 40 cases are drawn from the 233-case index whose per-model availability is Exhibit 8; the sample
touches every model × outcome cell that has available cases, both diagram types, and all four tiers
(§1.2). Category assignments are consistent with the index aggregates: provider drops concentrate in
qwen-2b; `no PNG produced` (C2) concentrates in the small/mid rungs and the larger rungs at
tier 4; and the `low_structural` class is relationship-driven (107/112 in the index), which the
per-category review attributes to S1 (wrong type), C3 (family confusion), S4 (name cascade), S2
(missed/notes), and M (measurement) rather than to pure missed structure.
