"""Relationship F1 — pure scoring logic (metric 3).

Operates on the edges of the structural graph emitted by the
DiagramStatsExtractor fork: each edge is a directed relation
(source -> target) with a canonical relation type. The matching unit is an
edge rather than a node; otherwise this mirrors Element F1 (multiset matching,
per-diagram precision/recall/F1, micro/macro aggregation), so `prf` and
`aggregate` are reused verbatim from element_f1.

Match key = (source, target, relation), endpoints normalized by lowercase+strip.
Direction: inheritance/composition/aggregation/dependency/message are directional
(a reversed edge is a miss); association is undirected (a plain line A-B carries
no inherent direction), so its endpoints are sorted into a canonical order. The
edge label is noisy OCR-like text and is excluded from the key. Self-loops
(source == target) are kept as ordinary edges; duplicate parallel edges are
handled by the multiset semantics of `prf`.
"""
from __future__ import annotations

from element_f1 import normalize, prf, aggregate  # reused verbatim

RELATIONS = ["inheritance", "composition", "aggregation",
             "dependency", "association", "message"]

# Relations with no inherent direction: a plain association line A-B == B-A.
UNDIRECTED = {"association"}


def edge_key(edge):
    """Normalized multiset match key for one edge: (source, target, relation).

    Endpoints are lowercased+stripped. For undirected relations the endpoints
    are sorted so a reversed edge maps to the same key. The label is ignored.
    """
    source = normalize(edge.get("source", ""))
    target = normalize(edge.get("target", ""))
    relation = edge["relation"]
    if relation in UNDIRECTED:
        source, target = sorted((source, target))
    return (source, target, relation)


def edges_from_record(record, relation=None):
    """Edge match keys from one extractor record (empty if no edges).

    If `relation` is given, restrict to edges of that relation type.
    """
    keys = []
    for edge in (record.get("edges") or []):
        if relation is not None and edge["relation"] != relation:
            continue
        keys.append(edge_key(edge))
    return keys


def compute(gt_by_key, pred_by_key, keys, relation=None):
    """Per-diagram edge scores over `keys`. Missing prediction -> empty graph.

    With `relation` set, both sides are restricted to that relation before
    scoring, yielding the per-relation stratified report.
    """
    rows = []
    for key in keys:
        gt_edges = edges_from_record(gt_by_key[key], relation)
        pred_rec = pred_by_key.get(key)
        pred_edges = edges_from_record(pred_rec, relation) if pred_rec is not None else []
        row = {"key": key}
        row.update(prf(gt_edges, pred_edges))
        rows.append(row)
    return rows
