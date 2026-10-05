"""Relationship F1 — pure scoring logic (metric 3).

Operates on the edges of the structural graph emitted by the
DiagramStatsExtractor fork: each edge is a directed relation
(source -> target) with a canonical relation type. The matching unit is an
edge rather than a node; otherwise this mirrors Element F1 (multiset matching,
per-diagram precision/recall/F1, micro/macro aggregation), so `prf` and
`aggregate` are reused verbatim from element_f1.

Match key = (source, target, relation), endpoints normalized as node names are.
Direction: inheritance/composition/aggregation/dependency/message are directional
(a reversed edge is a miss). An association with exactly one arrowhead is
directional too, tail -> head: a reversed or a dropped arrowhead is a miss. An
association drawn as a plain line, or with an arrowhead at both ends, carries no
direction, so its endpoints are sorted into a canonical order. The edge label is
noisy OCR-like text and is excluded from the key. Self-loops (source == target)
are kept as ordinary edges; duplicate parallel edges are handled by the multiset
semantics of `prf`.
"""
from __future__ import annotations

from element_f1 import V1, V2, normalize, prf, aggregate  # prf, aggregate reused verbatim

RELATIONS = ["inheritance", "composition", "aggregation",
             "dependency", "association", "message"]

# Relations with no inherent direction: a plain association line A-B == B-A.
UNDIRECTED = {"association"}

# Fourth key element of an association with exactly one arrowhead. It keeps a
# directed A -> B apart from the undirected A - B, whose sorted endpoints can
# coincide with it.
DIRECTED = "directed"


def edge_key(edge, rules=V2):
    """Normalized multiset match key for one edge: (source, target, relation).

    Endpoints are normalized as node names are. For undirected relations the
    endpoints are sorted so a reversed edge maps to the same key. An association
    whose `arrowhead` field (emitted by the extractor: none/source/target/both)
    names exactly one end is keyed (tail, head, relation, DIRECTED) instead.
    The label is ignored.
    """
    source = normalize(edge.get("source", ""), rules)
    target = normalize(edge.get("target", ""), rules)
    relation = edge["relation"]
    if relation in UNDIRECTED:
        arrowhead = edge.get("arrowhead") if rules.association_direction else None
        if arrowhead == "target":
            return (source, target, relation, DIRECTED)
        if arrowhead == "source":
            return (target, source, relation, DIRECTED)
        source, target = sorted((source, target))
    return (source, target, relation)


def edges_from_record(record, relation=None, rules=V2):
    """Edge match keys from one extractor record (empty if no edges).

    If `relation` is given, restrict to edges of that relation type.
    """
    keys = []
    for edge in (record.get("edges") or []):
        if relation is not None and edge["relation"] != relation:
            continue
        keys.append(edge_key(edge, rules))
    return keys


def compute(gt_by_key, pred_by_key, keys, relation=None, rules=V2):
    """Per-diagram edge scores over `keys`. Missing prediction -> empty graph.

    With `relation` set, both sides are restricted to that relation before
    scoring, yielding the per-relation stratified report.
    """
    rows = []
    for key in keys:
        gt_edges = edges_from_record(gt_by_key[key], relation, rules)
        pred_rec = pred_by_key.get(key)
        pred_edges = (edges_from_record(pred_rec, relation, rules)
                      if pred_rec is not None else [])
        row = {"key": key}
        row.update(prf(gt_edges, pred_edges))
        rows.append(row)
    return rows
