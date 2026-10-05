"""Tests for the pure Element F1 logic (element_f1.py)."""
import math

import element_f1 as ef


def approx(a, b):
    return math.isclose(a, b, rel_tol=0, abs_tol=1e-9)


# --- normalize ---

def test_normalize_lowercases_and_strips():
    assert ef.normalize("  Order ") == "order"


def test_normalize_collapses_case_only_difference():
    assert ef.normalize("ApplicationTemplate") == ef.normalize("applicationtemplate")


# --- stereotype stripping (stereotype tokens are not part of the display-name
# match key: the extractor folds a declaration's stereotype into the node name,
# and whether a stereotype is emitted at all is model house style — pilot-10
# finding on Sonnet 837bf9cc; both source <<X>> and rendered «X» forms). ---

def test_normalize_strips_stereotype_prefix():
    assert ef.normalize("<<database>> tuple") == "tuple"


def test_normalize_strips_stereotype_suffix():
    assert ef.normalize("tuple <<database>>") == "tuple"


def test_normalize_strips_rendered_chevron_form():
    assert ef.normalize("«analysis» X") == "x"


def test_normalize_strips_stereotype_mid_name_repairs_seam():
    assert ef.normalize("w: <<analysis>> Workbook") == "w: workbook"


def test_normalize_strips_spaced_stereotype():
    # real GT shape: `<< main >> Main` (323881231c)
    assert ef.normalize("<< main >> Main") == "main"


def test_normalize_strips_multiple_stereotypes():
    assert ef.normalize("<<A>><<B>> Node") == "node"
    assert ef.normalize("«A»«B» Node") == "node"


def test_normalize_strips_stereotype_with_nested_markup():
    # real GT shape (0b04c29e): creole markup nested inside the chevrons
    assert ef.normalize(
        "<<CardResource>> <<<back:pink>PluginObserverSpi</back>>> **final** CardResourceAdapter"
    ) == "**final** cardresourceadapter"


def test_normalize_plain_name_with_single_angle_brackets_untouched():
    # generics are part of the display name, not a stereotype
    assert ef.normalize("list: List<Variable>") == "list: list<variable>"


# --- scorer v2: whitespace runs and Unicode stereotype brackets ---

def test_normalize_collapses_whitespace_runs():
    # the number of spaces between two words is not visible in the image
    assert ef.normalize("Spring  Application") == ef.normalize("Spring Application")
    assert ef.normalize("taskTypeStore  : TaskTypeStore") == "tasktypestore : tasktypestore"
    assert ef.normalize("a \t\n b") == "a b"


def test_normalize_strips_unicode_stereotype_brackets():
    # GT 532d5a1ff757 writes the stereotype as <U+226A>X<U+226B>; the extractor
    # emits the decoded characters, the prediction writes <<X>>
    gt = "≪Application≫ : OrderDeliveredController"
    pred = "<<Application>> : OrderDeliveredController"
    assert ef.normalize(gt) == ": orderdeliveredcontroller"
    assert ef.normalize(gt) == ef.normalize(pred)


def test_normalize_keeps_unpaired_unicode_bracket():
    # GT 532d5a1ff757, first participant: the opening bracket is missing in the source
    assert ef.normalize("Presentation≫ : OrderDeliveredUI") == "presentation≫ : orderdeliveredui"


def test_normalize_keeps_typed_circle_letter():
    # a letter typed into the name is indistinguishable from a real name that
    # starts with a letter and a space; it stays part of the key
    assert ef.normalize("C Producer") == "c producer"
    assert ef.normalize("C Producer") != ef.normalize("Producer")
    assert ef.normalize("I have a really long name") == "i have a really long name"


# --- scorer v1 rules: every switch off reproduces the v1 key ---

def test_v1_rules_are_all_switches_off():
    assert ef.V1 == ef.Rules(collapse_whitespace=False, unicode_brackets=False,
                             association_direction=False)
    assert ef.V2 == ef.Rules()
    assert ef.V2 == ef.Rules(collapse_whitespace=True, unicode_brackets=True,
                             association_direction=True)


def test_v1_rules_keep_internal_whitespace():
    # whitespace fidelity is part of the v1 key for stereotype-free names
    assert ef.normalize("Upper  layer", ef.V1) == "upper  layer"
    # ...while the seam left by a stereotype removal is collapsed, as in v1
    assert ef.normalize("w: <<analysis>> Workbook", ef.V1) == "w: workbook"


def test_v1_rules_keep_unicode_stereotype_brackets():
    assert ef.normalize("≪Application≫ : X", ef.V1) == "≪application≫ : x"


def test_rule_switches_are_independent():
    only_ws = ef.Rules(collapse_whitespace=True, unicode_brackets=False)
    only_brackets = ef.Rules(collapse_whitespace=False, unicode_brackets=True)
    assert ef.normalize("≪A≫  B  C", only_ws) == "≪a≫ b c"
    assert ef.normalize("≪A≫ B  C", only_brackets) == "b c"
    assert ef.normalize("B  C", only_brackets) == "b  c"


def test_compute_passes_rules_to_names():
    gt = {"k": {"nodes": [{"name": "Upper  layer", "type": "class"}]}}
    pred = {"k": {"nodes": [{"name": "Upper layer", "type": "class"}]}}
    assert ef.compute(gt, pred, ["k"])[0]["tp"] == 1
    assert ef.compute(gt, pred, ["k"], ef.V1)[0]["tp"] == 0
    assert ef.compute_type_accuracy(gt, pred, ["k"])[0]["matched"] == 1
    assert ef.compute_type_accuracy(gt, pred, ["k"], ef.V1)[0]["matched"] == 0


def test_prf_matches_source_vs_rendered_stereotype():
    # both-sides symmetric: same stereotype in source vs rendered form
    gt = ["<<analysis>> EditVariablesUI", "<<analysis>> Variable"]
    pred = ["«analysis» EditVariablesUI", "«analysis» Variable"]
    r = ef.prf([ef.normalize(x) for x in gt], [ef.normalize(x) for x in pred])
    assert r["tp"] == 2 and r["fp"] == 0 and r["fn"] == 0
    assert approx(r["f1"], 1.0)


def test_prf_matches_one_sided_stereotype():
    # the 837bf9cc artifact: GT plain names, pred adds <<database>> house-style
    gt = ["tuple", "IPv4 layer", "Routing table"]
    pred = ["<<database>> tuple", "<<database>> IPv4 layer", "<<database>> Routing table"]
    r = ef.prf([ef.normalize(x) for x in gt], [ef.normalize(x) for x in pred])
    assert r["tp"] == 3 and r["fp"] == 0 and r["fn"] == 0
    assert approx(r["f1"], 1.0)


# --- prf: exact / partial ---

def test_prf_perfect_match():
    r = ef.prf(["a", "b", "c"], ["a", "b", "c"])
    assert r["tp"] == 3 and r["fp"] == 0 and r["fn"] == 0
    assert approx(r["precision"], 1.0) and approx(r["recall"], 1.0) and approx(r["f1"], 1.0)


def test_prf_partial_overlap():
    r = ef.prf(["a", "b", "c"], ["a", "b", "d"])
    assert r["tp"] == 2 and r["fp"] == 1 and r["fn"] == 1
    assert approx(r["precision"], 2 / 3)
    assert approx(r["recall"], 2 / 3)
    assert approx(r["f1"], 2 / 3)


def test_prf_precision_recall_differ():
    # gt has 2, pred has 3, 2 correct -> recall 1.0, precision 2/3
    r = ef.prf(["a", "b"], ["a", "b", "c"])
    assert r["tp"] == 2 and r["fp"] == 1 and r["fn"] == 0
    assert approx(r["precision"], 2 / 3)
    assert approx(r["recall"], 1.0)
    assert approx(r["f1"], 2 * (2 / 3) * 1.0 / (2 / 3 + 1.0))


# --- prf: empty edge cases ---

def test_prf_both_empty_is_perfect():
    r = ef.prf([], [])
    assert approx(r["precision"], 1.0) and approx(r["recall"], 1.0) and approx(r["f1"], 1.0)


def test_prf_empty_prediction_against_nonempty_gt_is_zero():
    r = ef.prf(["a", "b"], [])
    assert r["tp"] == 0 and r["fn"] == 2
    assert approx(r["f1"], 0.0)


def test_prf_hallucination_against_empty_gt_is_zero():
    r = ef.prf([], ["a"])
    assert r["tp"] == 0 and r["fp"] == 1
    assert approx(r["f1"], 0.0)


# --- prf: duplicate names (multiset semantics) ---

def test_prf_duplicates_counted_as_multiset():
    r = ef.prf(["a", "a", "b"], ["a", "b"])
    assert r["tp"] == 2 and r["fp"] == 0 and r["fn"] == 1
    assert approx(r["precision"], 1.0)
    assert approx(r["recall"], 2 / 3)


# --- names_from_record ---

def test_names_from_record_extracts_and_normalizes():
    rec = {"nodes": [{"name": "Order", "type": "class"},
                     {"name": " Customer ", "type": "class"}]}
    assert ef.names_from_record(rec) == ["order", "customer"]


def test_names_from_record_empty_on_error():
    rec = {"nodes": [], "error": "no_block"}
    assert ef.names_from_record(rec) == []


def test_names_from_record_handles_missing_nodes_key():
    assert ef.names_from_record({"error": "parse_error"}) == []


# --- aggregate: micro + macro ---

def test_aggregate_micro_pools_counts():
    per = [
        ef.prf(["a", "b"], ["a", "b"]),       # tp2 fp0 fn0
        ef.prf(["c", "d"], ["c", "x"]),       # tp1 fp1 fn1
    ]
    agg = ef.aggregate(per)
    # micro: TP=3, FP=1, FN=1 -> p=3/4, r=3/4
    assert approx(agg["micro"]["precision"], 3 / 4)
    assert approx(agg["micro"]["recall"], 3 / 4)
    assert approx(agg["micro"]["f1"], 3 / 4)
    assert agg["n"] == 2


def test_aggregate_macro_means_per_diagram():
    per = [
        ef.prf(["a", "b"], ["a", "b"]),       # f1 1.0
        ef.prf(["c", "d"], ["c", "x"]),       # f1 0.5
    ]
    agg = ef.aggregate(per)
    assert approx(agg["macro"]["f1"], 0.75)


def test_aggregate_empty_list():
    agg = ef.aggregate([])
    assert agg["n"] == 0


# --- compute over keys with missing predictions ---

def test_compute_missing_prediction_scores_zero():
    gt = {
        "k1": {"nodes": [{"name": "A"}, {"name": "B"}]},
        "k2": {"nodes": [{"name": "C"}]},
    }
    pred = {"k1": {"nodes": [{"name": "A"}, {"name": "B"}]}}  # k2 missing
    rows = ef.compute(gt, pred, ["k1", "k2"])
    by_key = {r["key"]: r for r in rows}
    assert approx(by_key["k1"]["f1"], 1.0)
    assert approx(by_key["k2"]["f1"], 0.0)  # missing pred -> empty -> 0 vs nonempty gt


def test_compute_normalizes_case_across_sides():
    gt = {"k": {"nodes": [{"name": "Order"}]}}
    pred = {"k": {"nodes": [{"name": "order"}]}}
    rows = ef.compute(gt, pred, ["k"])
    assert approx(rows[0]["f1"], 1.0)


# --- type accuracy (companion metric over name-matched pairs) ---

def test_typed_pairs_from_record_normalizes_names_and_keeps_type():
    rec = {"nodes": [{"name": " Order ", "type": "class"},
                     {"name": "Bob", "type": "actor"}]}
    assert ef.typed_pairs_from_record(rec) == [("order", "class"), ("bob", "actor")]


def test_typed_pairs_from_record_empty_on_missing_nodes():
    assert ef.typed_pairs_from_record({"error": "parse_error"}) == []


def test_type_counts_all_types_correct():
    gt = [("a", "class"), ("b", "interface")]
    pred = [("a", "class"), ("b", "interface")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 2 and r["correct"] == 2 and r["excluded"] == 0


def test_type_counts_wrong_type_in_denominator_not_correct():
    gt = [("a", "actor"), ("b", "participant")]
    pred = [("a", "participant"), ("b", "participant")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 2 and r["correct"] == 1 and r["excluded"] == 0


def test_type_counts_unmatched_names_contribute_nothing():
    gt = [("a", "class"), ("b", "class")]
    pred = [("a", "class"), ("x", "class")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 1 and r["correct"] == 1 and r["excluded"] == 0


def test_type_counts_duplicate_names_mixed_types_multiset():
    # gt: a as class + a as interface; pred: a twice as class.
    # name-matched = 2; (name,type) intersection = 1 correct.
    gt = [("a", "class"), ("a", "interface")]
    pred = [("a", "class"), ("a", "class")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 2 and r["correct"] == 1 and r["excluded"] == 0


def test_type_counts_package_gt_excluded_and_reported():
    gt = [("p", "package"), ("b", "class")]
    pred = [("p", "package"), ("b", "class")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 2
    assert r["excluded"] == 1          # the package pair, even though types agree
    assert r["correct"] == 1           # only the scored class pair counts


def test_type_counts_note_gt_excluded_regardless_of_pred_type():
    gt = [("n", "note")]
    pred = [("n", "class")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 1 and r["excluded"] == 1 and r["correct"] == 0


def test_type_counts_unscored_pred_type_against_scored_gt_is_wrong():
    # exclusion keys on the GT type only; an off-vocabulary pred type is just wrong
    gt = [("a", "actor")]
    pred = [("a", "package")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 1 and r["excluded"] == 0 and r["correct"] == 0


def test_type_counts_duplicate_name_scored_and_unscored_gt_prefers_scored():
    # gt: x as class + x as note; pred: one x as class. The single matched slot
    # is attributed to the scored (and type-correct) GT instance, not excluded.
    gt = [("x", "class"), ("x", "note")]
    pred = [("x", "class")]
    r = ef.type_counts(gt, pred)
    assert r["matched"] == 1 and r["correct"] == 1 and r["excluded"] == 0


def test_type_counts_per_type_breakdown():
    gt = [("a", "actor"), ("b", "actor"), ("c", "class")]
    pred = [("a", "participant"), ("b", "actor"), ("c", "class")]
    r = ef.type_counts(gt, pred)
    assert r["per_type"]["actor"] == {"support": 2, "correct": 1}
    assert r["per_type"]["class"] == {"support": 1, "correct": 1}


def test_type_counts_empty_prediction():
    r = ef.type_counts([("a", "class")], [])
    assert r == {"matched": 0, "correct": 0, "excluded": 0, "per_type": {}}


def test_aggregate_type_accuracy_pools_counts():
    rows = [
        ef.type_counts([("a", "actor")], [("a", "participant")]),   # wrong
        ef.type_counts([("b", "class"), ("p", "package")],
                       [("b", "class"), ("p", "package")]),         # 1 correct + 1 excluded
    ]
    agg = ef.aggregate_type_accuracy(rows)
    assert agg["matched"] == 3 and agg["excluded"] == 1
    assert agg["denominator"] == 2 and agg["correct"] == 1
    assert approx(agg["accuracy"], 0.5)
    assert agg["per_type"]["actor"] == {"support": 1, "correct": 0, "accuracy": 0.0}
    assert agg["per_type"]["class"] == {"support": 1, "correct": 1, "accuracy": 1.0}


def test_aggregate_type_accuracy_zero_denominator():
    agg = ef.aggregate_type_accuracy([])
    assert agg["matched"] == 0 and agg["denominator"] == 0
    assert agg["accuracy"] is None
