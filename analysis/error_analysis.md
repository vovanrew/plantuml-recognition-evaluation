# Error analysis: zero-shot image-to-PlantUML benchmark

This file reports what kinds of failure the seven models make. The method is in
`methodology/analysis-protocol.md` §7. The numbers come from
`analysis/out_paper/failure_index.md` (outcome counts) and from the coded sample in
`analysis/out_paper/error_sample/` (`keys.json`, `cases/`, `codes_a/`, `codes_b/`, `votes/`,
`codes_final.json`, `report.md`, `final_table.json`). Every case below is cited by its blind
identifier and the first eight characters of its diagram key.

## 1. Method

### 1.1 Outcome counts

Each of the 1,000 answers of a run gets one outcome class. The counts say how often each class
occurs.

| Model | Compiled, ok | Compiled, low-structural | Compile fail | Provider drop |
|---|---|---|---|---|
| GPT-5.2 | 852 | 83 | 64 | 1 |
| Claude Opus 4.6 | 824 | 117 | 59 | 0 |
| Gemini 3.1 Pro | 941 | 31 | 28 | 0 |
| Qwen3.5-2B | 96 | 96 | 808 | 0 |
| Qwen3.5-9B | 223 | 188 | 589 | 0 |
| Qwen3.5-27B | 532 | 114 | 354 | 0 |
| Qwen3.5-397B-A17B | 676 | 111 | 213 | 0 |

A compiled low-structural answer renders, but its Element F1 or Relationship F1 is below 0.5.
The one provider drop is a timeout. No run contains a refusal.

### 1.2 The sample

The strata are model × diagram type × tier × failure class (compile fail or compiled
low-structural). That is 16 cells per model, and each non-empty cell gives one case. Four cells
are empty, three of Gemini 3.1 Pro and one of Claude Opus 4.6, so the sample holds 108 cases:
54 compile fails and 54 compiled low-structural answers.

One case per cell shows which kinds of failure occur. It does not show how often they occur. A
count in this file is a count of sampled cases, never a rate.

The sample was drawn when three answers that name their diagram after `@startuml` were still
counted as compile fails: one of Qwen3.5-2B and two of Qwen3.5-27B. The table in §1.1 gives the
corrected counts. None of the three answers is in the sample. The sample is kept as drawn and
coded. A draw from the corrected counts would replace 3 of the 108 cases.

### 1.3 Coding

Each case was coded from its ground truth, its answer and the image the model was shown. The
coder did not know which model wrote the answer. The codebook (`analysis/error_codebook.md`) was
fixed before the first case was coded. Every case has one primary code and any secondary codes.

- Each case was coded twice, independently. The two codings give the same primary code in 105
  of the 108 cases.
- 21 cases went to review: the three disagreements and 18 cases that a coder flagged.
- Each review case was coded five more times, so it has seven codings. The primary code with
  the most votes was taken. Fifteen of the 21 cases are unanimous, and none is tied.
- Two review cases (E025, E038) ended on the codebook's placeholder for a possible measurement
  artifact. The author set both to a misread name.

The coder is an AI model (Claude Fable 5.2, Anthropic), run as separate instances that could not
see each other's codes. All codings therefore come from one model with one codebook. The
agreement shows that the codes are stable under the codebook. It is not the agreement of
independent human raters.

## 2. Codes

| Code | Name | Meaning |
|---|---|---|
| C1 | Syntax error | the answer does not render because of invalid syntax |
| C2 | Runaway | the answer never reaches its closing marker |
| C3 | Wrong diagram family | the answer is written in another diagram family |
| S1 | Wrong relation type | the endpoints are right, the decoration or direction is wrong |
| S2 | Missed relations | an edge of the image is absent, or sits between other endpoints |
| S3 | Invented elements | nodes or edges that the image does not show |
| S4 | Misread name | a name is transcribed so that it no longer matches |
| S5 | Wrong element kind | for example an enum written as a class |
| S6 | Lost control flow | `alt`, `opt`, `loop` or a group is lost |
| S7 | Missed elements | a node of the image is absent |
| M | Measurement artifact | the answer is right and the score is wrong |

## 3. Results

### 3.1 Primary codes per model

| Model | C1 | C2 | C3 | S1 | S2 | S3 | S4 | M | Cases |
|---|---|---|---|---|---|---|---|---|---|
| GPT-5.2 | 8 | 0 | 0 | 1 | 0 | 4 | 3 | 0 | 16 |
| Claude Opus 4.6 | 7 | 0 | 0 | 1 | 5 | 2 | 0 | 0 | 15 |
| Gemini 3.1 Pro | 5 | 2 | 0 | 2 | 1 | 0 | 3 | 0 | 13 |
| Qwen3.5-2B | 3 | 4 | 2 | 4 | 2 | 1 | 0 | 0 | 16 |
| Qwen3.5-9B | 5 | 3 | 4 | 2 | 0 | 2 | 0 | 0 | 16 |
| Qwen3.5-27B | 3 | 3 | 4 | 4 | 0 | 0 | 2 | 0 | 16 |
| Qwen3.5-397B-A17B | 5 | 3 | 0 | 2 | 0 | 2 | 3 | 1 | 16 |
| All | 36 | 15 | 10 | 16 | 8 | 11 | 11 | 1 | 108 |

S5, S6 and S7 are the primary code of no case.

### 3.2 Primary codes by failure class, diagram type and tier

| Stratum | C1 | C2 | C3 | S1 | S2 | S3 | S4 | M |
|---|---|---|---|---|---|---|---|---|
| Compile fail | 36 | 15 | 3 | 0 | 0 | 0 | 0 | 0 |
| Compiled low-structural | 0 | 0 | 7 | 16 | 8 | 11 | 11 | 1 |
| Class diagrams | 15 | 11 | 0 | 16 | 1 | 8 | 3 | 0 |
| Sequence diagrams | 21 | 4 | 10 | 0 | 7 | 3 | 8 | 1 |
| Tier 1 | 9 | 4 | 2 | 3 | 1 | 6 | 1 | 0 |
| Tier 2 | 9 | 3 | 3 | 3 | 2 | 3 | 4 | 0 |
| Tier 3 | 8 | 5 | 3 | 6 | 2 | 1 | 1 | 1 |
| Tier 4 | 10 | 3 | 2 | 4 | 3 | 1 | 5 | 0 |

### 3.3 Secondary codes

A case can carry several secondary codes. Over the 108 cases the secondary codes are: S3 in 41
cases, S2 in 30, the `note` tag in 16, S5 in 15, S1 in 15, S6 in 12, S4 in 6, C3 in 2, S7 in 1
and M in 1.

## 4. The codes in the cases

### 4.1 Syntax error (C1), 36 cases

Every model has C1 cases. In the three commercial models the usual case is one invalid token on
content that otherwise matches the image.

- **A class-diagram arrow in a sequence diagram.** The dotted arrow `..>` or `<..` stops the
  renderer: E014 `6084305e`, E021 `5ff302fd` and E057 `75d17323` (Claude Opus 4.6), E013
  `a4ace769`, E064 `4aad3806` and E073 `880c4bc5` (GPT-5.2). E058 `685ed638` has the invalid
  token `-..>`.
- **A name declared twice.** A class is declared again under an alias, or after a note has
  already created it: E050 `836fc1be` and E086 `bd045dcd` (Claude Opus 4.6), E090 `09ba2de0`
  (Gemini 3.1 Pro), E059 `2fc02b63` and E076 `784e17a8` (GPT-5.2).
- **An empty label.** A relation ends in a colon with nothing after it: E093 `50efbc2a`
  (Claude Opus 4.6), E088 `960d086e` and E098 `3742b108` (Qwen3.5-27B).
- **Unquoted or invalid names.** E037 `e9a06725` has unquoted Thai participant names (Gemini
  3.1 Pro), and E008 `b21a6faa` has an unquoted name with a backtick (Qwen3.5-397B-A17B).
- **Grouping written with the wrong construct.** Sequence groups or boxes are written as
  `frame`, `package` or a participant with a body: E002 `e74eafa3` and E015 `7e0e0e33`
  (Qwen3.5-397B-A17B), E046 `a6c835a4` (Qwen3.5-9B).
- **A directive that the diagram type rejects.** E023 `04642e29` and E081 `562c9533`
  (Qwen3.5-9B) fail on `left to right direction` in a sequence diagram. E006 `93d6d005` and
  E060 `cff9c8f0` (Qwen3.5-2B) fail after an incomplete `skinparam` line.

### 4.2 Runaway (C2), 15 cases

A C2 answer has no closing marker. In ten of the 15 cases the answer holds nothing but
display-only lines after its opening marker, between 110 and 823 of them: E009 `a87c8d58`,
E061 `246df95c` and E104 `e9a06725` (Qwen3.5-27B), E039 `59a417a8` and E074 `7bd2076a`
(Qwen3.5-2B), E026 `922bf6a5`, E051 `b8328a27` and E083 `3b84f043` (Qwen3.5-397B-A17B), E030
`7193e55a` and E097 `f18f0fa4` (Qwen3.5-9B). Three cases loop on diagram content: E084
`03144dcd` and E103 `bf4d1059` (Qwen3.5-2B), E063 `77b140eb` (Qwen3.5-9B).

The two Gemini 3.1 Pro cases are different. In E005 `1067b9ce` and E011 `dd18a88b` the answer
block is empty. GPT-5.2 and Claude Opus 4.6 have no C2 case in the sample.

### 4.3 Wrong diagram family (C3), 10 cases

All ten cases are sequence diagrams, and all are answers of the three dense Qwen3.5 sizes. The
lifelines are written as `rectangle`, `component`, `package` or `class` elements, so every
message is scored as an association or a dependency: E007 `21b4a540`, E017 `8bc750aa`, E024
`4d55d9c1` and E102 `7409cf40` (Qwen3.5-27B), E018 `7560f1b6` and E105 `defb5523`
(Qwen3.5-2B), E003 `e613eefd`, E031 `f8e33eb7`, E035 `7560f1b6` and E094 `9f8b8b5e`
(Qwen3.5-9B). Seven of the ten answers still render, so the failure shows in Relationship F1
and not in the compilation rate.

### 4.4 Wrong relation type (S1), 16 cases

All 16 cases are class diagrams, and every model has at least one. The endpoints are right, and
the decoration or the direction is wrong.

- **Another relation's mark.** Association is drawn as inheritance in E091 `d6312a93` and E101
  `836fc1be` (Gemini 3.1 Pro) and E033 `8acb8a80` (Qwen3.5-27B). Inheritance is drawn as
  dependency in E001 `86c771a5` (Qwen3.5-27B) and as a plain arrow in E036 `6510a08c`
  (Qwen3.5-397B-A17B). Composition is drawn as inheritance in E066 `f60a13a2` (Qwen3.5-9B) and,
  with the direction reversed, in E106 `f2502053` (Qwen3.5-2B). Three interface links are drawn
  as inheritance in E096 `9d3da061` (Qwen3.5-27B).
- **One mark for every relation.** The whole diagram is written with one arrow type: plain
  `-->` in E085 `83e0fd9a` (Claude Opus 4.6), dependency in E047 `ed0383f2`, inheritance in
  E070 `73140d95` and an undirected line in E087 `ad3ea3fc` (all Qwen3.5-2B). E044 `8bd6ca50`
  (Qwen3.5-27B) draws every aggregation as an association.
- **The mark at the wrong end.** All edges are reversed in E048 `1619bfd0` (GPT-5.2) and E027
  `fff389a2` (Qwen3.5-397B-A17B). The diamonds sit at the wrong class in E032 `82fd0908`
  (Qwen3.5-9B).

### 4.5 Missed relations (S2), 8 cases

In these cases the edge is usually not absent. It is drawn between other endpoints, most often
a message placed on another lifeline. The true edge is then missed and an edge the image does
not show appears, so S3 is a secondary code of all eight cases. Five of the eight cases are
Claude Opus 4.6: E019 `f611824f`, E042 `f3df7314`, E049 `10c4e675`, E056 `e613eefd` and E068
`549be1e0`. The others are E075 `a3dcb61f` (Gemini 3.1 Pro), E016 `8ff4bbff` and E077
`bc5d8adf` (Qwen3.5-2B). The codebook has no code of its own for a wrong endpoint. Seven of the
eight cases were reviewed for that reason, and in each of them all seven codings give S2.

### 4.6 Invented elements (S3), 11 cases

- **Notes.** The answer attaches a note to a class, or moves text into a note, and the note
  becomes a node with an edge: E010 `d3736e83` and E107 `f4b04251` (Claude Opus 4.6), E099
  `42fc85c2` (GPT-5.2), E108 `42fc85c2` (Qwen3.5-397B-A17B), E089 `a5898ca0` (Qwen3.5-9B).
- **Parts of an element read as elements.** Enum members become nodes in E092 `0806d963`
  (Qwen3.5-9B). A package frame becomes a class in E062 `7cbb0b64` (GPT-5.2). The head and foot
  boxes of one lifeline become two elements in E069 `c22af72a` (GPT-5.2) and E065 `c22af72a`
  (Qwen3.5-2B).
- **Edges the image does not draw.** Ten dependencies in E028 `4b0486c0` (GPT-5.2) and four
  messages on a diagram without messages in E053 `13535b2c` (Qwen3.5-397B-A17B).

### 4.7 Misread name (S4), 11 cases

A name that fails to match takes its edges with it, so one misread name can remove most of a
diagram's score.

- **The leading colon of an instance name.** It is dropped or respaced in E080 `d88ff3fb` and
  E100 `69166c59` (Qwen3.5-27B), E052 `d88ff3fb` (Qwen3.5-397B-A17B) and E079 `de951dfb`
  (GPT-5.2).
- **Part of a displayed name.** A line of a two-line name is dropped in E054 `c2056417`
  (GPT-5.2). A line break is dropped in E025 `56b1f581` (Qwen3.5-397B-A17B). Display names are
  rewritten as identifiers in E040 `1348037e` (Gemini 3.1 Pro). Box titles are taken as
  participants in E012 `b0d04738` (Qwen3.5-397B-A17B).
- **An icon written as a character.** E004 `c5bb3816` (GPT-5.2) and E038 `c5bb3816` (Gemini
  3.1 Pro) are the same diagram. Both answers write the icon before a name as a glyph.
- **A single character.** E055 `0ffb6611` (Gemini 3.1 Pro) reads a lower-case `l` as a capital
  `I` in the only class name.

E025, E038 and E004 are close to a measurement artifact, because the model reads the name and
the name match fails. They are coded S4 by the codebook's rule: a name change that the image
does not show is a misread name.

### 4.8 Measurement artifact (M), 1 case

E020 `de434622` (Qwen3.5-397B-A17B) is the only case with M as its primary code. Its test image
is rendered on a black background, so the actor's name and every arrow and label are invisible.
The answer cannot be right, and the fault is in the test image.

Two more cases have a test image with the same defect, E043 `73ece5e0` and E067 `de434622`
(both Gemini 3.1 Pro). Both answers also fail to compile on an empty actor name, so their
primary code is C1. The sample thus touches two test diagrams whose image hides content
(`de434622`, `73ece5e0`).

### 4.9 Codes that are never primary

S5 (wrong element kind), S6 (lost control flow) and S7 (missed elements) are the primary code
of no case. They occur beside another failure: S5 in 15 cases, S6 in 12 and S7 in 1. Lost
control flow is most often a result of a wrong diagram family or of a syntax error in a group.

## 5. Observations

- **Commercial models: small faults on correct content.** Their compile fails are C1 in 20 of
  22 sampled cases, and most are one invalid token. The two others are the empty Gemini
  answers.
- **Dense Qwen3.5 sizes: runaways and the wrong diagram family.** Ten of the 15 runaways and
  all ten family swaps are theirs. Both failures remove the whole answer, not a part of it.
- **Diagram type decides the structural failure.** All 16 wrong relation types are class
  diagrams. All ten family swaps and seven of the eight missed relations are sequence diagrams.
- **Relations fail by substitution.** In the class diagrams the edge is present with the wrong
  mark or at the wrong end. In the sequence diagrams the message is present on the wrong
  lifeline. A relation that is simply left out is rare in the sample.
- **Names cascade.** A misread name is the primary code of 11 cases, in four of the seven
  models, and each one also loses the edges of that name.
- **The instrument is seldom the cause.** One case of 108 has a measurement artifact as its
  primary code, and it comes from a defective test image.

## 6. Limits

- One case per cell shows kinds of failure, not their frequency. Section 1.1 gives the
  frequencies of the outcome classes, not of the codes.
- All codings come from one AI model with one codebook (Section 1.3).
- A primary code names the largest defect of a case. Most cases have more than one defect.
- Two test diagrams in the sample have an image that hides content (Section 4.8). The check
  that found them covers the sampled cases only.

## 7. Reproducibility

```
python -m analysis.build_error_sample draw   --data-root data_paper --registry analysis/model_registry_paper.json --out analysis/out_paper/error_sample
python -m analysis.build_error_sample report --out analysis/out_paper/error_sample
```

`draw` refuses a folder that is not empty, so the sample is drawn once. `keys.json` records the
seed and the hashes of the codebook, the script and the extractor. `report` refuses a codebook
that differs from the recorded one.
