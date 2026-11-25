# FUTURE.md

Open extensions that were considered and left out. None of them is part of the
zero-shot benchmark reported in this repository.

## Extractor: emit the visible shape of childless containers

The `DiagramStatsExtractor` fork gives the type `package` to every childless
braced container, whatever shape is drawn. `rectangle {}`, `package {}`,
`database {}`, `frame {}`, `cloud {}`, `folder {}` and `node {}` all get the same
type. The drawn shape is held in the group's `USymbol`, which the extractor does
not read for the type. For this reason type accuracy cannot grade these nodes and
leaves them out of its denominator (`methodology/evaluation-framework.md` §3).

Patch sketch: where `DiagramStatsExtractor.java` emits childless groups, emit the
shape name from `group.getUSymbol().getSNames()`, and fall back to
`groupType.name()` when the symbol is null. Then rebuild the JAR and extract
again. Element F1, Relationship F1 and CSR do not change, because they do not use
the node type. The change can be computed later from the stored predictions. It is
worth doing if the type of empty boxes turns out to matter as a failure mode.

## Thinking-mode comparison

The benchmark runs every model at its minimum reasoning setting
(`methodology/benchmark-protocol.md` §3). Two extensions remain open.

1. **Both modes per model.** Run the seven models again with thinking or reasoning
   turned on, and compare. Relationship recovery may depend on reasoning, so the
   difference would be a useful result. It doubles the number of runs, and
   thinking makes the outputs several times longer. A new run must size
   `max_tokens` and the deadline again, because 5376 tokens was sized to answers
   without reasoning.
2. **A Gemini Flash row at thinking level `minimal`.** Thinking cannot be turned
   off on Gemini 3.1 Pro, whose lowest level is `low`. A Flash model at `minimal`
   would show how much the remaining thinking helps, without changing the main
   comparison. It costs one extra model run.

## Out of scope

LLM-as-judge, visual similarity (SSIM, CLIP), graph edit distance, LLaVA
baselines, and the other diagram types of the corpus.
