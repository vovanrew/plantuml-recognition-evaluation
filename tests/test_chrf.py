"""Tests for chrF++ scorer (chrf.py)."""
import math

import sacrebleu

import chrf


def approx(a, b, tol=1e-6):
    return math.isclose(a, b, rel_tol=0, abs_tol=tol)


# --- sentence_score ---

def test_identical_strings_score_100():
    assert approx(chrf.sentence_score("hello world", "hello world"), 100.0)


def test_empty_hypothesis_scores_zero():
    assert approx(chrf.sentence_score("", "hello world"), 0.0)


def test_closer_hypothesis_scores_strictly_higher_than_farther():
    ref = "the quick brown fox jumps over the lazy dog"
    near = "the quick brown fox jumps over a lazy dog"
    far = "completely unrelated nonsense xyz"
    assert chrf.sentence_score(near, ref) > chrf.sentence_score(far, ref)


def test_sentence_score_matches_sacrebleu_chrf_plus_plus_kwargs():
    # The wrapper must pass char_order=6, word_order=2, beta=2 to sacrebleu.
    hyp = "@startuml\nclass Order\n@enduml"
    ref = "@startuml\nclass Customer\n@enduml"
    expected = sacrebleu.sentence_chrf(
        hyp, [ref], char_order=6, word_order=2, beta=2).score
    assert approx(chrf.sentence_score(hyp, ref), expected)


def test_word_order_2_engaged_not_plain_chrf():
    # A pair where char-level and word-level overlap differ in ratio:
    # plain chrF (chars only) and chrF++ (chars + word 1,2-grams) must disagree,
    # proving the wrapper actually engages word_order=2.
    hyp = "alpha beta gamma"
    ref = "alpha beta delta"
    plus = chrf.sentence_score(hyp, ref)
    plain = sacrebleu.sentence_chrf(
        hyp, [ref], char_order=6, word_order=0, beta=2).score
    assert plus != plain


# --- aggregate ---

def _row(key, hyp, ref):
    return {"key": key, "hyp": hyp, "ref": ref,
            "score": chrf.sentence_score(hyp, ref)}


def test_aggregate_macro_is_mean_of_per_diagram_scores():
    per = [_row("a", "hello world", "hello world"),
           _row("b", "foo bar",     "foo baz")]
    agg = chrf.aggregate(per)
    expected_macro = (per[0]["score"] + per[1]["score"]) / 2
    assert approx(agg["macro"], expected_macro)
    assert agg["n"] == 2


def test_aggregate_micro_is_corpus_chrf_pooled():
    per = [_row("a", "hello world", "hello world"),
           _row("b", "foo bar",     "foo baz")]
    agg = chrf.aggregate(per)
    hyps = [r["hyp"] for r in per]
    refs = [r["ref"] for r in per]
    expected_micro = sacrebleu.corpus_chrf(
        hyps, [refs], char_order=6, word_order=2, beta=2).score
    assert approx(agg["micro"], expected_micro)


def test_aggregate_micro_differs_from_macro_when_lengths_differ():
    # Macro is unweighted across diagrams; micro pools n-grams so a long, low-
    # scoring diagram drags the corpus number more than a short one.
    per = [
        _row("short_match", "a", "a"),                    # short, score 100
        _row("long_miss",
             "lorem ipsum dolor sit amet consectetur",
             "completely different text here"),           # long, low score
    ]
    agg = chrf.aggregate(per)
    assert agg["micro"] != agg["macro"]


def test_aggregate_empty_list_returns_zeros():
    agg = chrf.aggregate([])
    assert agg == {"micro": 0.0, "macro": 0.0, "n": 0}
