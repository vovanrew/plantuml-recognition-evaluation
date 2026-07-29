"""chrF++ — pure surface-similarity scoring (metric 4).

Thin wrapper over sacrebleu's chrF with word n-grams engaged (char_order=6,
word_order=2, beta=2 — the standard chrF++ parameters). Scores are sacrebleu's
native 0-100 range.

chrF++ is the surface sanity metric: it gives graded partial credit for
near-miss text (wording, signatures, multiplicities, role labels) that the
structural F1s deliberately ignore.

Aggregation:
  macro = unweighted mean of per-diagram sentence_chrf scores;
  micro = corpus_chrf over all (hyp, ref) pairs, which pools n-gram counts and
          is therefore length-weighted.
"""
from __future__ import annotations

import sacrebleu

CHAR_ORDER = 6
WORD_ORDER = 2
BETA = 2


def sentence_score(hyp, ref):
    """chrF++ between one hypothesis and one reference, on the 0-100 scale."""
    return sacrebleu.sentence_chrf(
        hyp, [ref],
        char_order=CHAR_ORDER, word_order=WORD_ORDER, beta=BETA).score


def aggregate(per_diagram):
    """Micro (pooled n-gram counts) and macro (mean of per-diagram scores).

    Each row in `per_diagram` must carry `hyp`, `ref`, and `score`."""
    n = len(per_diagram)
    if n == 0:
        return {"micro": 0.0, "macro": 0.0, "n": 0}
    macro = sum(r["score"] for r in per_diagram) / n
    micro = sacrebleu.corpus_chrf(
        [r["hyp"] for r in per_diagram],
        [[r["ref"] for r in per_diagram]],
        char_order=CHAR_ORDER, word_order=WORD_ORDER, beta=BETA).score
    return {"micro": micro, "macro": macro, "n": n}
