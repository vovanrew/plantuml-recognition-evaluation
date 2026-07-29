# FUTURE.md

Deferred work registry: extensions that were considered, scoped, and cut for time.
All of it is out of scope for the zero-shot benchmark reported in this repository.

## Extractor: emit visible skin for childless containers

The `DiagramStatsExtractor` fork emits `type: "package"` for every childless
braced container regardless of rendered shape — verified that `rectangle {}`,
`package {}`, `database {}`, `frame {}`, `cloud {}`, `folder {}`, `node {}`
all produce the same type string, because the visible skin lives in the
group's `USymbol`, which the extractor does not read. Consequence: the type
accuracy companion metric cannot grade empty-box node types
and excludes them from its denominator (the "Python exclusion" rule, decided
2026-06-11).

Patch sketch: in the childless-group emission loop of
`DiagramStatsExtractor.java`, emit the skin name via
`group.getUSymbol().getSNames()` (fall back to `groupType.name()` when the
symbol is null), rebuild the JAR, re-extract. No effect on Element F1
(name-only), Relationship F1 (name endpoints), or CSR. Exposure if done:
~15 `package`-typed + ~8 `description`-typed GT nodes (~0.7% of class
nodes, 0 sequence) become gradeable. Recomputable post-hoc from stored
predictions at any time, including after paper submission. Trigger to
reconsider: Phase 3 error analysis surfaces empty-box type confusion as a
real failure mode.

## Thinking-mode comparison

The benchmark runs every model at its minimum reasoning configuration
(methodology/benchmark-protocol.md §3). Two deferred extensions:

1. **Both modes per model**: re-run the six models with thinking/reasoning enabled and
   compare. Diagram-to-code is plausibly reasoning-sensitive for relationship
   recovery, so the delta is a genuinely interesting result — but it doubles
   run count and thinking inflates completion tokens severalfold, which the
   project's cost and time budget could not carry. Re-running requires
   re-deriving `max_tokens` (5376 was sized to non-thinking GT lengths; in-band
   reasoning tokens would consume it) and the 90s timeout.
2. **Gemini 3.5 Flash @ `thinking_level: "minimal"` supplementary row**:
   Gemini 3.1 Pro cannot disable thinking (floor `low`); a Flash run at
   `minimal` would bound how much the residual thinking helps Pro without
   contaminating the main same-tier comparison. Cheap (one extra model run);
   add only if budget remains after the six main runs.

## Explicitly out of scope

LLM-as-judge, visual similarity (SSIM/CLIP), graph edit distance, LLaVA
baselines, fine-tuning (next work), 7 remaining diagram types.
