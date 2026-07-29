"""Element F1 — pure scoring logic (metric 2).

Operates on the structural graph emitted by the DiagramStatsExtractor fork:
nodes are class-like leaves (class diagrams) or participants (sequence). An
element is matched iff its node name matches after lowercasing, trimming, and
stereotype-token stripping; matching is multiset (a name repeated k times must
appear k times on both sides).

Empty/empty -> perfect (F1 1.0); a non-parsing prediction (empty graph) against
a non-empty ground truth scores F1 0.0, which realizes the zeros-for-failed mode.
"""
from __future__ import annotations

import re
from collections import Counter

# Stereotype tokens are not part of the display-name match key: the extractor
# folds a declaration's stereotype into the node name, and whether a model
# emits a stereotype at all is house style (pilot-10 finding on Sonnet
# 837bf9cc). Both the source syntax `<<X>>` and the rendered chevron form `«X»`
# are removed wherever they occur in the name; `>>+` absorbs the extra closer
# left by creole markup nested inside the chevrons (`<<<back:pink>X</back>>>`,
# GT 0b04c29e). Single angle brackets (generics like `List<Variable>`) are
# untouched. The whitespace seam left by a removal is collapsed; names without
# stereotype tokens keep their internal whitespace verbatim.
_STEREOTYPE_TOKEN = re.compile(r"<<.*?>>+|«[^«»]*»", re.S)
_WHITESPACE_RUN = re.compile(r"\s+")


def normalize(name):
    stripped = _STEREOTYPE_TOKEN.sub(" ", name)
    if stripped != name:
        stripped = _WHITESPACE_RUN.sub(" ", stripped)
    return stripped.strip().lower()


def prf(gt_names, pred_names):
    """Precision/recall/F1 for one diagram, multiset matching on names."""
    gt = Counter(gt_names)
    pred = Counter(pred_names)
    tp = sum((gt & pred).values())
    n_gt = sum(gt.values())
    n_pred = sum(pred.values())
    fp = n_pred - tp
    fn = n_gt - tp

    precision = tp / n_pred if n_pred else (1.0 if n_gt == 0 else 0.0)
    recall = tp / n_gt if n_gt else (1.0 if n_pred == 0 else 0.0)
    f1 = 0.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)

    return {"tp": tp, "fp": fp, "fn": fn,
            "precision": precision, "recall": recall, "f1": f1}


def names_from_record(record):
    """Normalized node names from one extractor JSONL record (empty if no nodes)."""
    return [normalize(n["name"]) for n in (record.get("nodes") or [])]


def _f1(precision, recall):
    return 0.0 if (precision + recall) == 0 else 2 * precision * recall / (precision + recall)


def aggregate(per_diagram):
    """Micro (pooled counts) and macro (mean of per-diagram scores) over rows."""
    n = len(per_diagram)
    if n == 0:
        zero = {"precision": 0.0, "recall": 0.0, "f1": 0.0}
        return {"micro": dict(zero), "macro": dict(zero), "n": 0}

    tp = sum(r["tp"] for r in per_diagram)
    fp = sum(r["fp"] for r in per_diagram)
    fn = sum(r["fn"] for r in per_diagram)
    micro_p = tp / (tp + fp) if (tp + fp) else 1.0
    micro_r = tp / (tp + fn) if (tp + fn) else 1.0
    micro = {"precision": micro_p, "recall": micro_r, "f1": _f1(micro_p, micro_r)}

    macro = {k: sum(r[k] for r in per_diagram) / n
             for k in ("precision", "recall", "f1")}

    return {"micro": micro, "macro": macro, "n": n}


def compute(gt_by_key, pred_by_key, keys):
    """Per-diagram scores over `keys`. Missing prediction -> empty graph -> scored."""
    rows = []
    for key in keys:
        gt_names = names_from_record(gt_by_key[key])
        pred_rec = pred_by_key.get(key)
        pred_names = names_from_record(pred_rec) if pred_rec is not None else []
        row = {"key": key}
        row.update(prf(gt_names, pred_names))
        rows.append(row)
    return rows


# --- Type accuracy: companion metric over name-matched pairs ---------------
#
# The Element F1 match key stays name-only; entity-type recovery is reported
# separately. A name-matched GT<->pred pair counts as type-correct iff the
# extractor `type` strings agree ((name, type) multiset intersection). Pairs
# whose GT type is outside the scored vocabulary are excluded from the
# denominator and reported as an excluded count: `package` is the extractor's
# emission for every childless `{}` container regardless of rendered shape
# (the visible skin is unrecoverable downstream), and types like `note` /
# `tips` / `point_for_association` are renderer-internal artifacts, not
# entities a model is asked to type.

CLASS_TYPES = frozenset({
    "class", "abstract_class", "interface", "enum", "entity", "object",
    "annotation", "protocol", "struct", "exception", "metaclass",
    "dataclass", "record", "map", "json",
})
PARTICIPANT_TYPES = frozenset({
    "participant", "actor", "boundary", "control", "entity", "queue",
    "database", "collections",
})
SCORED_TYPES = CLASS_TYPES | PARTICIPANT_TYPES


def typed_pairs_from_record(record):
    """(normalized name, extractor type) per node of one JSONL record."""
    return [(normalize(n["name"]), n.get("type", ""))
            for n in (record.get("nodes") or [])]


def type_counts(gt_pairs, pred_pairs):
    """Type-accuracy counts over the name-matched pairs of one diagram.

    Per name, matched = min(gt count, pred count); correct = (name, type)
    multiset intersection restricted to scored GT types. Matched slots not
    type-correct are attributed to leftover GT instances, scored types first,
    so an unscored GT instance is excluded only when no scored instance can
    absorb the slot (keeps correct <= denominator under duplicate names).
    """
    gt_by_name, pred_by_name = {}, {}
    for n, t in gt_pairs:
        gt_by_name.setdefault(n, Counter())[t] += 1
    for n, t in pred_pairs:
        pred_by_name.setdefault(n, Counter())[t] += 1

    matched = correct = excluded = 0
    per_type = {}
    for name, gtc in gt_by_name.items():
        predc = pred_by_name.get(name)
        if not predc:
            continue
        m = min(sum(gtc.values()), sum(predc.values()))
        matched += m

        correct_by_type = {t: min(c, predc[t]) for t, c in gtc.items()}
        attributed = dict(correct_by_type)
        slots = m - sum(correct_by_type.values())
        for t in sorted(gtc, key=lambda t: (t not in SCORED_TYPES, t)):
            if slots == 0:
                break
            take = min(slots, gtc[t] - correct_by_type[t])
            attributed[t] += take
            slots -= take

        for t, a in attributed.items():
            if a == 0:
                continue
            if t in SCORED_TYPES:
                correct += correct_by_type[t]
                row = per_type.setdefault(t, {"support": 0, "correct": 0})
                row["support"] += a
                row["correct"] += correct_by_type[t]
            else:
                excluded += a

    return {"matched": matched, "correct": correct, "excluded": excluded,
            "per_type": per_type}


def compute_type_accuracy(gt_by_key, pred_by_key, keys):
    """Per-diagram type counts over `keys`. Missing prediction -> no pairs."""
    rows = []
    for key in keys:
        gt_pairs = typed_pairs_from_record(gt_by_key[key])
        pred_rec = pred_by_key.get(key)
        pred_pairs = typed_pairs_from_record(pred_rec) if pred_rec is not None else []
        row = {"key": key}
        row.update(type_counts(gt_pairs, pred_pairs))
        rows.append(row)
    return rows


def aggregate_type_accuracy(rows):
    """Pooled (micro) type accuracy plus a per-GT-type table with support."""
    matched = sum(r["matched"] for r in rows)
    correct = sum(r["correct"] for r in rows)
    excluded = sum(r["excluded"] for r in rows)
    denominator = matched - excluded

    per_type = {}
    for r in rows:
        for t, c in r["per_type"].items():
            row = per_type.setdefault(t, {"support": 0, "correct": 0})
            row["support"] += c["support"]
            row["correct"] += c["correct"]
    for t, c in per_type.items():
        c["accuracy"] = c["correct"] / c["support"] if c["support"] else None

    return {"matched": matched, "correct": correct, "excluded": excluded,
            "denominator": denominator,
            "accuracy": correct / denominator if denominator else None,
            "per_type": dict(sorted(per_type.items()))}
