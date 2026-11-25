# Evaluation Framework

Methodological record for the metrics used in the zero-shot image-to-PlantUML
benchmark. Scope: class and sequence diagrams.

## 1. Compilation Success Rate

Compilation Success Rate (CSR) is the fraction of predictions that constitute
valid, renderable PlantUML. Each prediction's PlantUML block is isolated — the
span from the first `@startuml` to the last `@enduml` — and submitted to the
official PlantUML renderer. A prediction succeeds when the renderer produces a
non-empty diagram image and fails otherwise; syntactic acceptance alone is
insufficient, so a prediction that parses but renders nothing counts as a
failure. A prediction whose generation runs into the API's `max_tokens` ceiling
is returned truncated, lacking the closing `@enduml`; block isolation then fails
on the incomplete output and the renderer produces no image, so a runaway
no-EOS generation counts as a failure rather than masking as a successful
compile. The ceiling is set to 5376 tokens, approximately 1.5 × the longest
test-set ground-truth length (3546 tokens, measured with the Qwen3.5-2B
tokenizer via `transformers` 5.10.2), so a legitimate complex diagram is not
curtailed. CSR is computed over the full set of test-set keys, so a prediction
that is absent — for example an inference timeout that produced no output —
counts as a failure rather than being excluded.

## 2. Structural extraction (typed graph)

Structural metrics operate on a typed graph extracted from PlantUML source by a
custom tool (`DiagramStatsExtractor`), a fork of the official PlantUML renderer
that reuses its internal parser. The same extractor is applied to both
ground-truth and predicted code, so the two are compared on identical terms. For
each diagram the extractor emits one JSON record containing `nodes` and `edges`
alongside the diagram type.

### 2.1 Nodes

A node is a first-class diagram entity: a class-like leaf (class, interface,
enum, abstract, ...) for class diagrams, or a participant (participant, actor,
boundary, ...) for sequence diagrams. Each node carries its entity type and a
name. A grouping container that holds at least one child entity (a package or
namespace wrapping classes) is not a node; its children are the nodes.

Notes are handled differently by diagram type. In class diagrams every note is
emitted as a node of type `note`, named by its text, and a note attached to a
node, or a floating note linked to one, additionally yields an edge typed
`dependency` between them; an unlinked floating note yields a node and no edge.
In sequence diagrams notes are not emitted at all, neither as nodes nor as
edges. Notes therefore enter the Element F1 and Relationship F1 counts on class
diagrams, while `note`-typed pairs are excluded from the type-accuracy
denominator (§3). Measured over the 1,000-diagram test set, notes are 71 of the
5,742 ground-truth nodes (2.3% of the 3,125 class-diagram nodes) and 66 of the
9,265 ground-truth edges, occurring in 39 diagrams.

A childless grouping container — a box written with empty braces, such as
`rectangle "Application" {}`, an empty `package`, or a `database X {}` — is a
node. PlantUML models any braced box as a group, so a box with no contents would
otherwise be dropped from the graph even though it is a single visible element
that a model reproduces as a class. Counting it as a node keeps the graph
consistent with the image: a prediction that renders the box matches it instead
of scoring a false positive (e.g. an empty-box endpoint that would otherwise
leave its incident edge pointing at a non-existent node).

Node identity is the entity's **visible display name** — the label rendered in
the image — rather than any source-level alias or code identifier. Because the
task is image-to-code, a model can reproduce only what is visible; an entity
declared `class "ApplicationTemplate" as Model` is identified as
`ApplicationTemplate`.

The display name is the text that PlantUML draws for the label. The extractor
reads the label with PlantUML's own markup parser and keeps the text of the
drawn lines. Formatting tags, icons, sprites and emoji are markup, so they are
not part of the name. An actor drawn as the sprite `<$actor>` above `Payer` is
named `Payer`. The parser decides what is markup, so a generic such as
`List<Pharmacy>` stays text. Unicode escapes such as `<U+226A>` are read as the
characters they stand for. A label with no drawn text is named by its alias, as
an empty label is. Every rule of this section applies in the same way to the
ground truth and to a prediction.

PlantUML draws a label on one of three paths, by kind of element, and the name
is read on the same path.

| Element | How the label is read | Example |
|---|---|---|
| Class-like element | With the setting of PlantUML's class header: a pair of double underscores is text, and a leading `*`, `**` or `#` starts no list item | `client_new_connection_SYNC__NO_MSG__AT_MOST` keeps its underscores |
| Note, use case, rectangle-like element, circle, childless group that has a symbol | The label is cut at separator lines first. A separator line is a horizontal line that PlantUML draws, not text. Its title is text, unless it holds only separator characters | The lines `API Gateway`, `===`, `/api/v2/petstore` give `API Gateway /api/v2/petstore` |
| Every other label: sequence participant, object, map, childless package without a symbol | Whole, with every kind of markup on. A lone `==` line is the heading `=` that PlantUML draws | The lines `PkgTop`, `==`, `PkgBottom` of a childless package give `=`: the heading is the largest line |

When the lines of a label differ in font size, the line or lines at the largest
size are the name. The size of a line is the largest size of any text in it.
Sources generated from code often write the class name at one size and its
package under it at a smaller one. `<b><size:14>ConquestMapPart</b>` above
`<size:10>soen6441riskgame.enums` is named `ConquestMapPart`. Text without a
size of its own has the base size of the diagram's own style for that element.
That is PlantUML's default (14 pt for a class name or a participant, 13 pt for a
note), unless the source changes it with `skinparam` or `<style>`. So
`<size:10>Components::` above the unsized `DimensionComponent` is named
`DimensionComponent`.

The letter of a stereotype spot is not part of the name. A spot such as
`<< (C,#ADD1B2) >>` sets the letter and the colour of the circle drawn beside the
name, so the letter belongs to an icon. The declaration
`participant "Producer" as UpstreamProducer << (C,#ADD1B2) >>` is named
`Producer`. A tip, a note on a class member, is named by its owner and its side,
as in `NumbersStack$$$LEFT`.

Names are compared after lowercasing, trimming, and collapsing every run of
whitespace to one space. The number of spaces between two words cannot be read
from an image, so `Spring  Application`, typed with two spaces, equals
`Spring Application`.

Stereotype tokens are not part of the display-name match key on any node, in
either diagram type, on both the ground-truth and prediction sides. The
extractor folds a declaration's stereotype into the emitted node name
(`participant "tuple" <<database>>` yields the name `«database» tuple`), and
whether a stereotype is written at all varies by model house style; keying the
name on the stereotype would score a stylistic difference as a structural
mismatch. Name comparison therefore removes every stereotype token wherever it
occurs in the name. This covers the source syntax `<<X>>`, the chevron forms
`«X»` and `≪X≫` (U+226A and U+226B), and the source form with creole markup
nested inside the chevrons (`<<<back:pink>X</back>>>`).
Single angle brackets remain part of the name (`List<Variable>` is a generic,
not a stereotype): `<<database>> tuple`, `tuple <<database>>`, `«database»
tuple`, `≪database≫ tuple`, and `tuple` all key as `tuple`. Stereotype-driven entity-kind
distinctions are scored by the type-accuracy companion metric (§3); stereotype
tags as surface text are assessed by chrF++ (§5).

### 2.2 Edges

An edge is a directed relation between two entities, identified by their display
names, with a canonical relation type and an optional label. Relation types are
canonicalized from PlantUML link decorations and line style to a fixed
vocabulary:

| Relation | Source construct |
|---|---|
| inheritance | generalization or realization (triangle head; solid or dashed) |
| composition | filled-diamond decoration |
| aggregation | hollow-diamond decoration |
| dependency | dashed line carrying an arrow head |
| association | any other plain line (solid, with or without a plain arrow) |
| message | any sequence-diagram message |

The orientation of a directional edge is fixed by the link decoration — the
triangle, diamond, or arrow head — rather than the order in which its two
entities are written, so a relation drawn in either token order yields a single
canonical edge. For an association, the extractor also records which end
carries an arrowhead: neither end, the source, the target, or both. Relationship
F1 uses this to decide whether an association is directed (§4).

An edge is counted only when PlantUML draws it. The extractor leaves out every
link and every message that PlantUML marks as not drawn:

- a link that PlantUML adds itself to arrange three or more elements of a group
  that have no relationship;
- the link that PlantUML adds between the points of two association classes on
  the same pair of classes;
- a link or a message that the source writes as `[hidden]`, and a link to an
  element that the source hides or removes.

The image shows no line for these, so a model cannot read them. For example, six
unconnected interfaces in one package give no edges. The link of a tip to its
owner stays an edge, because the image shows the note's pointer to the class
member. The rule holds in every diagram that the extractor reads as elements and
links, and for the messages of a sequence diagram. It removes no node, so
Element F1 and type accuracy do not depend on it.

Realization is folded into inheritance. Every sequence message is typed
`message`; a message whose counterpart lies outside the diagram is recorded with
an empty external endpoint on the side the external participant occupies: the
source is empty for an inbound message, whose external participant is the sender,
and the target is empty for an outbound message, whose external participant is
the receiver. Sequence control-flow constructs — `alt`, `else`, `opt`, `par`,
`loop`, `group` — are not edges; the messages they contain are emitted unchanged.

### 2.3 Accounting for unparseable predictions

Every input file yields exactly one record. A prediction that does not parse to a
complete diagram — for example a truncated model output lacking `@enduml` — is
recorded as an error with an empty graph (zero nodes, zero edges), so that such
cases are counted rather than silently dropped.

### 2.4 Answers with several diagrams

A prediction can hold several `@startuml` ... `@enduml` diagrams. The structural
metrics read only the first diagram of such a prediction, because PlantUML
displays only the first diagram of a file. The extractor emits one record for
each diagram, and the records of the later diagrams are not scored. The same
rule applies to the ground truth.

## 3. Element F1

Element F1 measures recovery of the diagram's first-class entities — the nodes of
the typed graph (classes for class diagrams, participants for sequence diagrams).
A predicted node matches a ground-truth node when their display names are equal
after the normalization of §2.1: lowercasing, trimming, collapsing whitespace
runs, and removing stereotype tokens. Matching is multiset: a name occurring k times in
the ground truth is credited at most k times. For one diagram, true positives are
the matched names, precision is true positives over the predicted node count, and
recall is true positives over the ground-truth node count; F1 is their harmonic
mean. A diagram with no nodes on either side scores 1; a prediction whose graph is
empty against a non-empty ground truth scores 0.

Scores are aggregated over the set in two ways. The micro average pools true
positives, false positives, and false negatives across diagrams before forming
precision, recall, and F1, weighting each diagram by its node count. The macro
average is the mean of the per-diagram scores, weighting each diagram equally.

Element F1 is reported under two diagram populations. The compiled-only
population restricts scoring to predictions that pass Compilation Success Rate.
The zeros-for-failed population spans every test-set key, with a missing or
non-compiling prediction contributing an empty graph and therefore F1 zero. Both
sides of every comparison have their PlantUML block isolated identically (the
span from the first `@startuml` to the last `@enduml`), so any repository header
preceding the diagram is removed symmetrically before extraction. Within that
span, the scorer reads the first diagram (§2.4).

Entity-type recovery is reported by a companion metric, **type accuracy**,
computed over the name-matched node pairs; the Element F1 match key itself is
the display name alone. The type-correct count is the multiset intersection of
(name, type) pairs between the two sides, where the type is the extractor's
entity type string; this count is at most the name-matched count, so the metric
is well-defined under duplicate names without per-pair assignment. The
denominator is the name-matched count minus the excluded pairs, and the
excluded count is reported alongside the score. A pair is excluded when its
ground-truth node type lies outside the scored vocabulary: the class-like types
`class`, `abstract_class`, `interface`, `enum`, `entity`, `object`,
`annotation`, `protocol`, `struct`, `exception`, `metaclass`, `dataclass`,
`record`, `map`, `json`, and the participant types `participant`, `actor`,
`boundary`, `control`, `entity`, `queue`, `database`, `collections`. Types
outside this vocabulary do not denote a recoverable entity type: `package` is
the extractor's emission for every childless braced container (§2.1)
irrespective of the rendered shape, and the remaining ground-truth occurrences
(`note`, `tips`, `point_for_association`, `description`, `lollipop_full`) are
renderer-internal artifacts. Type accuracy is aggregated as the pooled ratio of
type-correct pairs to the denominator over the diagram set, together with a
per-ground-truth-type table reporting support and accuracy for each scored
type, analogous to the per-relation stratification of Relationship F1. The
metric is conditional on name matches, so a missing or non-compiling prediction
contributes no pairs; it is reported for the compiled-only population, under
which the pooled counts equal those of the zeros-for-failed population.

## 4. Relationship F1

Relationship F1 measures recovery of the diagram's typed relations — the edges of
the typed graph. The matching unit is an edge; the construction otherwise follows
Element F1. A predicted edge matches a ground-truth edge when their match keys are
equal, where the match key is the triple of source endpoint, target endpoint, and
canonical relation type. Endpoints are display names, compared after the same
normalization as node names (§2.1). Matching is multiset, so an
edge occurring k times — including parallel edges between the same pair — is
credited at most k times. The edge label is excluded from the key: it is
transcribed surface text rather than structure, so a relation is identified by
its endpoints and canonical type alone, and the fidelity of message wording is
assessed separately by the surface metric (chrF++).

Edge direction enters the match key by relation type. Inheritance, composition,
aggregation, dependency, and message are directional: their endpoints carry an
inherent orientation (child to parent, whole to part, sender to receiver), so a
reversed edge is a mismatch. An association with exactly one arrowhead is also
directional, and the edge runs from the tail to the head. The image shows an
arrowhead as it shows a diamond, so a reversed, dropped, or added arrowhead is a
mismatch. For the ground truth `Order --> Customer`, the predictions
`Customer --> Order` and `Order -- Customer` are mismatches, and
`Customer <-- Order` is a match. A plain line, or a line with an arrowhead at
both ends, has no orientation. Its two endpoints are placed in a canonical order
before forming the key, so such an association matches when written in either
direction. A directed association never matches an undirected one between the
same two entities. Self-loops, whose source and target coincide, are scored as
ordinary edges.

For one diagram, true positives are the matched edges, precision is true positives
over the predicted edge count, and recall is true positives over the ground-truth
edge count; F1 is their harmonic mean. A diagram with no edges on either side
scores 1; a prediction whose edge set is empty against a non-empty ground truth
scores 0. The overall score, computed over all relation types jointly, is
aggregated over the set as a micro average that pools true positives, false
positives, and false negatives across diagrams, and a macro average that means the
per-diagram scores.

The score is additionally stratified by relation type. For each relation, both the
ground-truth and predicted edge sets are restricted to that relation and scored,
yielding a per-relation micro precision, recall, and F1 together with the
ground-truth and predicted edge counts that form its support. Because a diagram
that does not use a relation contributes no pooled counts to that relation's
stratum, a relation absent from a diagram neither helps nor harms its
per-relation score. This stratification reports which relation kinds models
recover well — for example inheritance versus dependency in class diagrams, and
messages in sequence diagrams.

Relationship F1 is reported under the same two diagram populations as Element F1,
the compiled-only and zeros-for-failed populations, and both sides of every
comparison have their PlantUML block isolated identically before extraction.

## 5. chrF++

chrF++ measures surface text fidelity between the predicted and ground-truth
PlantUML code as a single character-and-word n-gram F-score. It covers the
descriptive dimensions the structural metrics deliberately exclude — message
wording, member signatures, multiplicities, role labels, stereotype tags,
sequence control-flow framing (`alt` / `else` / `opt` / `par` / `loop` /
`group` brackets), and notes — and so complements Element F1 and Relationship
F1 with a graded partial-credit signal on near-miss text. The score is a single
aggregate over all surface text and does not by itself isolate any one of these
dimensions: a given chrF++ value reflects the joint fidelity of every surface
layer, so the metric reports overall surface similarity rather than per-layer
accuracy.

The score is sacrebleu's chrF with character n-grams up to order 6 and word
n-grams up to order 2 (the `++` extension), weighted equally and combined with
β = 2 (recall weighted twice precision), implemented via sacrebleu 2.6.0
(`char_order=6, word_order=2, beta=2`). Per-diagram scores are computed with
`sentence_chrf`; values lie on sacrebleu's native 0–100 range and are stored
unrescaled. Both sides of every comparison have their PlantUML block isolated
identically — the span from the first `@startuml` to the last `@enduml`, the
same procedure applied for the structural metrics — so any repository header,
markdown fence, or surrounding prose is removed symmetrically before scoring.

Scores are aggregated over the set in two ways. The macro average is the
unweighted mean of the per-diagram sentence scores, weighting each diagram
equally. The micro average is the corpus chrF++ computed over all
(hypothesis, reference) pairs jointly, pooling n-gram counts across the set and
therefore weighting each diagram by its n-gram volume — long, low-scoring
predictions move the corpus number more than short ones.

chrF++ is reported under two diagram populations defined to be comparable with
Element F1 and Relationship F1. The compiled-only population restricts scoring
to predictions that pass Compilation Success Rate. The zeros-for-failed
population spans every test-set key, with any missing or non-compiling
prediction forced to score zero and contributing an empty hypothesis to the
corpus-level pool. The compile gate is supplied explicitly from the CSR result
file: unlike the structural metrics, where a non-parsing prediction yields an
empty graph and therefore F1 zero by construction, chrF++ is parse-independent
and a syntactically broken prediction can still have a non-zero surface
similarity to the ground truth.
