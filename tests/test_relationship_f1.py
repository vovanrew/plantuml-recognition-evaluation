"""Tests for the pure Relationship F1 logic (relationship_f1.py)."""
import math

import relationship_f1 as rf
import relationship_f1_runner as rfr


def approx(a, b):
    return math.isclose(a, b, rel_tol=0, abs_tol=1e-9)


def e(source, target, relation, label=None):
    d = {"source": source, "target": target, "relation": relation}
    if label is not None:
        d["label"] = label
    return d


# --- edge_key: normalization ---

def test_edge_key_normalizes_endpoints():
    assert rf.edge_key(e(" Order ", "Customer", "association")) == \
        rf.edge_key(e("order", " customer", "association"))


def test_edge_key_ignores_label():
    assert rf.edge_key(e("A", "B", "association", label="places")) == \
        rf.edge_key(e("A", "B", "association", label="cancels"))


def test_edge_key_collapses_stereotype_source_and_rendered_endpoints():
    # PlantUML renders <<X>> as «X»; a model that transcribes the rendered
    # chevron must produce the same edge key as a GT written in source syntax
    # (audit-50 finding on 838542d0).
    src = e("<<analysis>> EditVariablesUI", "<<analysis>> Variable", "message",
            label="setValue(newValue)")
    rendered = e("«analysis» EditVariablesUI", "«analysis» Variable", "message",
                 label="setValue(newValue)")
    assert rf.edge_key(src) == rf.edge_key(rendered)


def test_edge_key_strips_stereotypes_from_endpoints():
    # edge_key inherits stereotype stripping via element_f1.normalize: an edge
    # whose endpoints carry a one-sided stereotype (pilot-10 finding on Sonnet
    # 837bf9cc) keys identically to the plain-name edge.
    stereotyped = e("<<database>> tuple", "<<database>> ARP", "message",
                    label="lookup")
    plain = e("tuple", "ARP", "message", label="lookup")
    assert rf.edge_key(stereotyped) == rf.edge_key(plain)


# --- edge_key: direction semantics ---

def test_edge_key_inheritance_is_directional():
    assert rf.edge_key(e("Child", "Parent", "inheritance")) != \
        rf.edge_key(e("Parent", "Child", "inheritance"))


def test_edge_key_composition_is_directional():
    assert rf.edge_key(e("Whole", "Part", "composition")) != \
        rf.edge_key(e("Part", "Whole", "composition"))


def test_edge_key_aggregation_is_directional():
    assert rf.edge_key(e("Whole", "Part", "aggregation")) != \
        rf.edge_key(e("Part", "Whole", "aggregation"))


def test_edge_key_dependency_is_directional():
    assert rf.edge_key(e("A", "B", "dependency")) != \
        rf.edge_key(e("B", "A", "dependency"))


def test_edge_key_message_is_directional():
    assert rf.edge_key(e("A", "B", "message")) != \
        rf.edge_key(e("B", "A", "message"))


def test_edge_key_association_is_undirected():
    assert rf.edge_key(e("A", "B", "association")) == \
        rf.edge_key(e("B", "A", "association"))


def test_edge_key_relation_is_part_of_key():
    assert rf.edge_key(e("A", "B", "association")) != \
        rf.edge_key(e("A", "B", "dependency"))


# --- edges_from_record ---

def test_edges_from_record_extracts_keys():
    rec = {"edges": [e("Order", "Customer", "association"),
                     e("Order", "Item", "composition")]}
    keys = rf.edges_from_record(rec)
    assert len(keys) == 2
    assert rf.edge_key(e("order", "customer", "association")) in keys


def test_edges_from_record_empty_on_missing_key():
    assert rf.edges_from_record({"error": "parse_error"}) == []


def test_edges_from_record_filters_by_relation():
    rec = {"edges": [e("Order", "Customer", "association"),
                     e("Order", "Item", "composition"),
                     e("A", "B", "composition")]}
    comp = rf.edges_from_record(rec, relation="composition")
    assert len(comp) == 2
    assert all(k[2] == "composition" for k in comp)


def test_edges_from_record_keeps_self_loops():
    rec = {"edges": [e("Node", "Node", "message")]}
    keys = rf.edges_from_record(rec)
    assert len(keys) == 1


# --- compute: matching behavior via prf ---

def test_compute_perfect_match():
    gt = {"k": {"edges": [e("A", "B", "inheritance")]}}
    pred = {"k": {"edges": [e("A", "B", "inheritance")]}}
    rows = rf.compute(gt, pred, ["k"])
    assert approx(rows[0]["f1"], 1.0)


def test_compute_reversed_inheritance_is_miss():
    gt = {"k": {"edges": [e("Child", "Parent", "inheritance")]}}
    pred = {"k": {"edges": [e("Parent", "Child", "inheritance")]}}
    rows = rf.compute(gt, pred, ["k"])
    assert rows[0]["tp"] == 0
    assert approx(rows[0]["f1"], 0.0)


def test_compute_reversed_association_still_matches():
    gt = {"k": {"edges": [e("A", "B", "association")]}}
    pred = {"k": {"edges": [e("B", "A", "association")]}}
    rows = rf.compute(gt, pred, ["k"])
    assert approx(rows[0]["f1"], 1.0)


def test_compute_relation_mismatch_is_miss():
    gt = {"k": {"edges": [e("A", "B", "aggregation")]}}
    pred = {"k": {"edges": [e("A", "B", "dependency")]}}
    rows = rf.compute(gt, pred, ["k"])
    assert rows[0]["tp"] == 0
    assert approx(rows[0]["f1"], 0.0)


def test_compute_both_empty_is_perfect():
    gt = {"k": {"edges": []}}
    pred = {"k": {"edges": []}}
    rows = rf.compute(gt, pred, ["k"])
    assert approx(rows[0]["f1"], 1.0)


def test_compute_empty_prediction_against_nonempty_gt_is_zero():
    gt = {"k": {"edges": [e("A", "B", "association")]}}
    pred = {"k": {"edges": []}}
    rows = rf.compute(gt, pred, ["k"])
    assert approx(rows[0]["f1"], 0.0)


def test_compute_missing_prediction_scores_zero():
    gt = {"k1": {"edges": [e("A", "B", "association")]},
          "k2": {"edges": [e("C", "D", "composition")]}}
    pred = {"k1": {"edges": [e("A", "B", "association")]}}  # k2 missing
    rows = rf.compute(gt, pred, ["k1", "k2"])
    by_key = {r["key"]: r for r in rows}
    assert approx(by_key["k1"]["f1"], 1.0)
    assert approx(by_key["k2"]["f1"], 0.0)


def test_compute_duplicate_parallel_edges_are_multiset():
    gt = {"k": {"edges": [e("A", "B", "message"),
                          e("A", "B", "message")]}}
    pred = {"k": {"edges": [e("A", "B", "message")]}}
    rows = rf.compute(gt, pred, ["k"])
    assert rows[0]["tp"] == 1 and rows[0]["fn"] == 1
    assert approx(rows[0]["recall"], 0.5)
    assert approx(rows[0]["precision"], 1.0)


def test_compute_with_relation_filter_restricts_both_sides():
    gt = {"k": {"edges": [e("A", "B", "association"),
                          e("A", "C", "composition")]}}
    pred = {"k": {"edges": [e("A", "B", "association")]}}
    rows = rf.compute(gt, pred, ["k"], relation="composition")
    # Only the composition edge is scored; pred has none -> recall 0.
    assert rows[0]["tp"] == 0 and rows[0]["fn"] == 1
    assert approx(rows[0]["f1"], 0.0)


def test_compute_relation_filter_empty_both_sides_is_perfect():
    gt = {"k": {"edges": [e("A", "B", "association")]}}
    pred = {"k": {"edges": [e("A", "B", "association")]}}
    rows = rf.compute(gt, pred, ["k"], relation="inheritance")
    assert approx(rows[0]["f1"], 1.0)


# --- aggregate is reused from element_f1; smoke its presence ---

def test_aggregate_micro_and_macro_available():
    per = [rf.prf([("a", "b", "x")], [("a", "b", "x")]),
           rf.prf([("c", "d", "y")], [("c", "z", "y")])]
    agg = rf.aggregate(per)
    assert agg["n"] == 2
    assert approx(agg["macro"]["f1"], 0.5)


# --- per_relation_counts: the new additive per-diagram per-relation emission ---
#
# The runner additionally writes, per diagram, a `by_relation` map of
# {rel: {tp, fp, fn}} over the canonical RELATIONS. These pins guard the two
# structural invariants the per-relation bootstrap relies on (the runner re-score
# gates iii/iv in miniature): edges partition by relation type, and pooling the
# per-relation counts reproduces summary.by_relation.

def test_per_relation_counts_has_all_canonical_relations():
    gt = {"k": {"edges": [e("A", "B", "inheritance")]}}
    pred = {"k": {"edges": [e("A", "B", "inheritance")]}}
    per = rfr.per_relation_counts(gt, pred, ["k"])
    assert set(per) == {"k"}
    assert list(per["k"]) == rf.RELATIONS  # all six, in canonical order
    assert per["k"]["inheritance"] == {"tp": 1, "fp": 0, "fn": 0}
    assert per["k"]["association"] == {"tp": 0, "fp": 0, "fn": 0}


def test_per_relation_counts_partition_reproduces_overall():
    # The match key carries the relation, so a diagram's edges partition by type:
    # summing tp/fp/fn across the six relations must equal the overall counts.
    gt = {"k": {"edges": [e("A", "B", "inheritance"),
                          e("A", "C", "association"),
                          e("X", "Y", "message"),
                          e("P", "Q", "composition")]}}
    pred = {"k": {"edges": [e("A", "B", "inheritance"),   # hit
                            e("C", "A", "association"),    # undirected -> hit
                            e("X", "Z", "message"),        # wrong endpoint -> miss (fp+fn)
                            e("P", "Q", "aggregation")]}}  # wrong relation -> miss (fp+fn)
    per = rfr.per_relation_counts(gt, pred, ["k"])
    overall = rf.compute(gt, pred, ["k"])[0]
    for field in ("tp", "fp", "fn"):
        assert sum(per["k"][rel][field] for rel in rf.RELATIONS) == overall[field], field


def test_per_relation_counts_pooling_reproduces_micro_with_support():
    # Pooling the per-diagram per-relation counts across keys must reproduce the
    # summary's by_relation micro P/R/F1 + support (runner gate iv in miniature).
    gt = {"k1": {"edges": [e("A", "B", "inheritance"), e("C", "D", "message")]},
          "k2": {"edges": [e("E", "F", "inheritance")]}}
    pred = {"k1": {"edges": [e("A", "B", "inheritance")]},          # message missing
            "k2": {"edges": [e("F", "E", "inheritance")]}}          # reversed -> miss
    keys = ["k1", "k2"]
    per = rfr.per_relation_counts(gt, pred, keys)
    for rel in rf.RELATIONS:
        tp = sum(per[k][rel]["tp"] for k in keys)
        fp = sum(per[k][rel]["fp"] for k in keys)
        fn = sum(per[k][rel]["fn"] for k in keys)
        ref = rfr.micro_with_support(rf.compute(gt, pred, keys, relation=rel))
        p = tp / (tp + fp) if (tp + fp) else 1.0
        r = tp / (tp + fn) if (tp + fn) else 1.0
        assert approx(p, ref["precision"]) and approx(r, ref["recall"]), rel
        assert tp + fn == ref["support_gt"] and tp + fp == ref["support_pred"], rel


def test_per_relation_counts_missing_prediction_is_all_fn():
    gt = {"k": {"edges": [e("A", "B", "inheritance"), e("C", "D", "message")]}}
    pred = {}  # missing prediction -> empty graph
    per = rfr.per_relation_counts(gt, pred, ["k"])
    assert per["k"]["inheritance"] == {"tp": 0, "fp": 0, "fn": 1}
    assert per["k"]["message"] == {"tp": 0, "fp": 0, "fn": 1}
    assert per["k"]["association"] == {"tp": 0, "fp": 0, "fn": 0}
