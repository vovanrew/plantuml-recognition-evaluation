"""Scorer-v2 switches of the two structural runners.

The defaults are scorer v2; each flag turns one rule off, and every flag
together is scorer v1. The first part checks the argument mapping alone; the
second part runs both runners end to end through the extractor JAR on five
ground-truth / prediction pairs, with the defaults, with each switch alone and
with every switch, and checks the scores, the type-accuracy counts, the
per-relation counts and the `scorer` block of the results file. The third part
does the same for the drawn-edge rule, on pairs whose links or messages
PlantUML does not draw.
"""
import argparse
import hashlib
import json
import os
import sys

import pytest

import element_f1 as ef
import element_f1_runner as efr
import relationship_f1_runner as rfr
from element_f1_runner import EXTRACTOR_JAR

ALL_OFF = ["--no-collapse-whitespace", "--no-unicode-brackets",
           "--no-association-direction", "--last-diagram",
           "--extractor-arg=--names=raw", "--extractor-arg=--no-arrowheads",
           "--extractor-arg=--undrawn-edges"]


def _parse(flags):
    ap = argparse.ArgumentParser()
    ap.add_argument("--jar", default="")
    efr.add_scorer_args(ap)
    return ap.parse_args(flags)


# --- argument mapping ---

def test_no_flags_is_scorer_v2():
    args = _parse([])
    assert efr.rules_from_args(args) == ef.V2
    assert args.last_diagram is False
    assert args.extractor_arg == []


def test_all_flags_is_scorer_v1():
    args = _parse(ALL_OFF)
    assert efr.rules_from_args(args) == ef.V1
    assert args.last_diagram is True
    assert args.extractor_arg == ["--names=raw", "--no-arrowheads", "--undrawn-edges"]


@pytest.mark.parametrize("flag,field", [
    ("--no-collapse-whitespace", "collapse_whitespace"),
    ("--no-unicode-brackets", "unicode_brackets"),
    ("--no-association-direction", "association_direction"),
])
def test_each_rule_flag_turns_off_its_rule_only(flag, field):
    args = _parse([flag])
    rules = efr.rules_from_args(args)
    for name in ("collapse_whitespace", "unicode_brackets", "association_direction"):
        assert getattr(rules, name) is (name != field)
    assert args.last_diagram is False


def test_last_diagram_flag_leaves_the_rules_alone():
    args = _parse(["--last-diagram"])
    assert args.last_diagram is True
    assert efr.rules_from_args(args) == ef.V2


def test_scorer_record_names_what_produced_the_results(tmp_path):
    jar = tmp_path / "x.jar"
    jar.write_bytes(b"not a real jar")
    args = _parse(["--jar", str(jar), "--no-unicode-brackets", "--extractor-arg=--names=markup"])
    record = efr.scorer_record(args, efr.rules_from_args(args))
    assert record == {
        "rules": {"collapse_whitespace": True, "unicode_brackets": False,
                  "association_direction": True},
        "first_diagram": True,
        "extractor_args": ["--names=markup"],
        "extractor_jar_sha256": hashlib.sha256(b"not a real jar").hexdigest(),
    }


# --- end to end through the JAR ---

jar = pytest.mark.skipif(
    not os.path.exists(EXTRACTOR_JAR),
    reason="DiagramStatsExtractor JAR not built; set PLANTUML_EXTRACTOR_JAR "
           "(see README, 'The structural extractor')")

# key -> (ground truth, prediction, relation of its one edge). Each pair has two
# nodes and one edge, and is told apart by exactly one scorer-v2 rule.
PAIRS = {
    # two spaces in the source, one in the answer
    "whitespace": ('participant "Spring  Application" as S\nparticipant B\nS -> B : go',
                   'participant "Spring Application" as S\nparticipant B\nS -> B : go',
                   "message"),
    # U+226A/U+226B brackets against a stereotype
    "brackets": ('participant "<U+226A>App<U+226B>\\n: Controller" as C\nparticipant D\nC -> D : go',
                 'participant ": Controller" as C <<App>>\nparticipant D\nC -> D : go',
                 "message"),
    # bold name above a smaller package line
    "names": ('class "<b><size:14>ConquestMapPart</b>\\n<size:10>riskgame.enums" as C\n'
              'class X\nX <|-- C',
              'class ConquestMapPart\nclass X\nX <|-- ConquestMapPart',
              "inheritance"),
    # the answer reverses the arrow: the names match, the edge matches under v1 only
    "direction": ("class A\nclass B\nA --> B", "class A\nclass B\nB --> A", "association"),
    # two diagrams, the second broken: a match on the first diagram only
    "first": ("class A\nclass B\nA *-- B",
              "class A\nclass B\nA *-- B\n@enduml\n\n@startuml\nclass Z\nnot PlantUML {{{",
              "composition"),
}

# switches -> pairs whose names stop matching / whose edge stops matching
NAME_CASES = [
    ([], set()),
    (["--no-collapse-whitespace"], {"whitespace"}),
    (["--no-unicode-brackets"], {"brackets"}),
    # typed names keep <U+226A> undecoded, so the bracket rule has nothing to strip
    (["--extractor-arg=--names=raw"], {"names", "brackets"}),
    (["--last-diagram"], {"first"}),
    (["--no-association-direction"], set()),
    # every link of these pairs is drawn, and nodes are never touched
    (["--extractor-arg=--undrawn-edges"], set()),
    (ALL_OFF, {"whitespace", "brackets", "names", "first"}),
]
EDGE_CASES = [
    ([], {"direction"}),
    (["--no-collapse-whitespace"], {"direction", "whitespace"}),
    (["--no-unicode-brackets"], {"direction", "brackets"}),
    (["--extractor-arg=--names=raw"], {"direction", "names", "brackets"}),
    (["--last-diagram"], {"direction", "first"}),
    (["--no-association-direction"], set()),
    (["--extractor-arg=--no-arrowheads"], set()),
    (["--extractor-arg=--undrawn-edges"], {"direction"}),
    (ALL_OFF, {"whitespace", "brackets", "names", "first"}),
]
_IDS = lambda case: " ".join(f.replace("--extractor-arg=", "") for f in case) or "defaults"


def _run(runner, tmp_path, flags, monkeypatch, pairs=None):
    gt, pred, out = tmp_path / "gt", tmp_path / "pred", tmp_path / "out"
    for d in (gt, pred):
        d.mkdir()
    for key, pair in (PAIRS if pairs is None else pairs).items():
        g, p = pair[0], pair[1]
        (gt / (key + ".puml")).write_text("@startuml\n%s\n@enduml\n" % g, encoding="utf-8")
        (pred / (key + ".puml")).write_text("@startuml\n%s\n@enduml\n" % p, encoding="utf-8")
    monkeypatch.setattr(sys, "argv", [
        "runner", "--pred-dir", str(pred), "--gt-dir", str(gt), "--out", str(out),
        "--jar", EXTRACTOR_JAR] + flags)
    runner.main()
    stem = "element_f1" if runner is efr else "relationship_f1"
    res = json.load(open(out / (stem + "_results.json")))
    return res, {d["key"]: d for d in res["diagrams"]}


@jar
@pytest.mark.parametrize("flags,missed", NAME_CASES, ids=[_IDS(c[0]) for c in NAME_CASES])
def test_element_runner(tmp_path, monkeypatch, flags, missed):
    res, rows = _run(efr, tmp_path, flags, monkeypatch)

    assert res["scorer"]["rules"] == {
        "collapse_whitespace": "--no-collapse-whitespace" not in flags,
        "unicode_brackets": "--no-unicode-brackets" not in flags,
        "association_direction": "--no-association-direction" not in flags}
    assert res["scorer"]["first_diagram"] is ("--last-diagram" not in flags)
    assert res["scorer"]["extractor_args"] == [
        f[len("--extractor-arg="):] for f in flags if f.startswith("--extractor-arg=")]

    # names: both nodes match, or one does not (none when the scored diagram is broken)
    matched = {k: (2 if k not in missed else 0 if k == "first" else 1) for k in PAIRS}
    assert {k: r["tp"] for k, r in rows.items()} == matched
    assert {k: r["f1"] == 1.0 for k, r in rows.items()} == {k: k not in missed for k in PAIRS}
    # type accuracy is counted over the same name matches
    assert {k: r["type_accuracy"]["matched"] for k, r in rows.items()} == matched
    assert res["summary"]["type_accuracy"]["matched"] == sum(matched.values())


@jar
@pytest.mark.parametrize("flags,missed", EDGE_CASES, ids=[_IDS(c[0]) for c in EDGE_CASES])
def test_relationship_runner(tmp_path, monkeypatch, flags, missed):
    res, rows = _run(rfr, tmp_path, flags, monkeypatch)

    assert res["scorer"]["rules"]["association_direction"] is (
        "--no-association-direction" not in flags)
    assert res["scorer"]["first_diagram"] is ("--last-diagram" not in flags)

    assert {k: r["tp"] for k, r in rows.items()} == {k: int(k not in missed) for k in PAIRS}
    # per-diagram per-relation counts follow the same rules
    for key, (_, _, relation) in PAIRS.items():
        assert rows[key]["by_relation"][relation]["tp"] == int(key not in missed)
        assert rows[key]["by_relation"][relation]["fn"] == int(key in missed)
    # ...and so does the per-relation summary
    by_relation = res["summary"]["zeros_for_failed"]["by_relation"]
    for relation in {r for _, _, r in PAIRS.values()}:
        keys = [k for k, (_, _, r) in PAIRS.items() if r == relation]
        assert by_relation[relation]["support_gt"] == len(keys)
        assert by_relation[relation]["recall"] == sum(k not in missed for k in keys) / len(keys)


# --- the drawn-edge rule, end to end through the JAR ---

_SIX = ["Reader", "Writer", "Parser", "Mapper", "Loader", "Closer"]
_TIP = "class A {\n+foo()\n}\nclass B\nA --> B\nnote right of A::foo\nabout foo\nend note"
_COMPONENTS = "\n".join("component " + n for n in "ABCDEF")


def _package(names):
    return "package api {\n%s\n}" % "\n".join("interface " + n for n in names)


# key -> (ground truth, prediction). The links and messages PlantUML does not
# draw are on the ground-truth side, on the prediction side, or on both.
DRAWN_PAIRS = {
    # six unconnected interfaces in a package; the answer lists them in the
    # order of the source: under v1 the five layout links match for nothing
    "package": (_package(_SIX), _package(_SIX)),
    # the same picture, the answer in the reverse order: under v1 it is charged
    # a wrong and a missed relationship
    "package_reordered": (_package(_SIX), _package(_SIX[::-1])),
    # three unconnected classes at the root
    "root": ("class A\nclass B\nclass C", "class A\nclass B\nclass C"),
    # two real relationships beside three unconnected classes
    "mixed": ("class A\nclass B\nclass C\nclass D\nclass E\nclass F\nA --> B\nB *-- C",
              "class A\nclass B\nclass C\nclass D\nclass E\nclass F\nA --> B\nB *-- C"),
    # fewer than three unconnected classes: PlantUML adds no link
    "two": ("class A\nclass B\nclass C\nclass D\nA --> B",
            "class A\nclass B\nclass C\nclass D\nA --> B"),
    # the answer leaves unconnected what the source connects with plain lines:
    # under v1 its layout links match the two real relationships
    "answer_unconnected": ("class A\nclass B\nclass C\nA -- B\nA -- C",
                           "class A\nclass B\nclass C"),
    # a link the source hides; the answer holds what the image shows
    "hidden_link": ("class A\nclass B\nclass C\nA --> B\nA -[hidden]-> C",
                    "class A\nclass B\nclass C\nA --> B"),
    # a link to an element the source hides: the edge goes, the node stays
    "hidden_element": ("class A\nclass B\nclass C\nA --> B\nB --> C\nhide C",
                       "class A\nclass B\nA --> B"),
    # a tip keeps the link to its owner; the answer has the tip as well
    "tip": (_TIP, _TIP),
    # ...or leaves it out
    "tip_missed": (_TIP, "class A {\n+foo()\n}\nclass B\nA --> B"),
    # a hidden message
    "hidden_message": ("participant A\nparticipant B\nA -> B : one\nA -[hidden]-> B : two\n"
                       "B --> A : three",
                       "participant A\nparticipant B\nA -> B : one\nB --> A : three"),
    # not a class diagram: a component diagram with a hidden link and three
    # unconnected components; the answer holds what the image shows
    "component": (_COMPONENTS + "\nA --> B\nA -[hidden]- C", _COMPONENTS + "\nA --> B"),
    # ...and a state diagram with a hidden transition
    "state": ("state A\nstate B\nstate C\nA --> B\nA -[hidden]-> C",
              "state A\nstate B\nstate C\nA --> B"),
}

# key -> (tp, fp, fn) of Relationship F1 with the defaults, and with every
# link and message an edge (the switch alone, and every switch off: scorer v1)
DRAWN_EDGE_ROWS = {
    "package": ((0, 0, 0), (5, 0, 0)),
    "package_reordered": ((0, 0, 0), (4, 1, 1)),
    "root": ((0, 0, 0), (2, 0, 0)),
    "mixed": ((2, 0, 0), (4, 0, 0)),
    "two": ((1, 0, 0), (1, 0, 0)),
    "answer_unconnected": ((0, 0, 2), (2, 0, 0)),
    "hidden_link": ((1, 0, 0), (1, 0, 1)),
    "hidden_element": ((1, 0, 0), (1, 0, 1)),
    "tip": ((2, 0, 0), (2, 0, 0)),
    "tip_missed": ((1, 0, 1), (1, 0, 1)),
    "hidden_message": ((2, 0, 0), (2, 0, 1)),
    "component": ((1, 0, 0), (1, 3, 3)),
    "state": ((1, 0, 0), (1, 0, 1)),
}
# key -> (tp, fp, fn) of Element F1: the same whatever the switch
DRAWN_NODE_ROWS = {
    "package": (6, 0, 0), "package_reordered": (6, 0, 0), "root": (3, 0, 0),
    "mixed": (6, 0, 0), "two": (4, 0, 0), "answer_unconnected": (3, 0, 0),
    "hidden_link": (3, 0, 0), "hidden_element": (2, 0, 1), "tip": (3, 0, 0),
    "tip_missed": (2, 0, 1), "hidden_message": (2, 0, 0), "component": (6, 0, 0),
    "state": (3, 0, 0),
}
DRAWN_CASES = [([], 0), (["--extractor-arg=--undrawn-edges"], 1), (ALL_OFF, 1)]


def _counts(rows):
    return {k: (r["tp"], r["fp"], r["fn"]) for k, r in rows.items()}


@jar
@pytest.mark.parametrize("flags,column", DRAWN_CASES, ids=[_IDS(c[0]) for c in DRAWN_CASES])
def test_relationship_runner_drawn_edges(tmp_path, monkeypatch, flags, column):
    res, rows = _run(rfr, tmp_path, flags, monkeypatch, DRAWN_PAIRS)

    assert res["scorer"]["extractor_args"] == [
        f[len("--extractor-arg="):] for f in flags if f.startswith("--extractor-arg=")]
    assert _counts(rows) == {k: v[column] for k, v in DRAWN_EDGE_ROWS.items()}
    # a diagram without a drawn relationship on either side has no edge at all
    for key in ("package", "package_reordered", "root"):
        assert (rows[key]["f1"] == 1.0) is (column == 0 or key != "package_reordered")
    # the per-relation summary pools the same counts
    by_relation = res["summary"]["zeros_for_failed"]["by_relation"]
    pooled = [sum(r["by_relation"][rel][c] for r in rows.values() for rel in by_relation)
              for c in ("tp", "fp", "fn")]
    assert pooled == [sum(v[column][i] for v in DRAWN_EDGE_ROWS.values()) for i in range(3)]
    assert by_relation["message"]["support_gt"] == 2 + column


@jar
@pytest.mark.parametrize("flags", [[], ["--extractor-arg=--undrawn-edges"]],
                         ids=["defaults", "--undrawn-edges"])
def test_element_runner_is_untouched_by_the_drawn_edge_rule(tmp_path, monkeypatch, flags):
    res, rows = _run(efr, tmp_path, flags, monkeypatch, DRAWN_PAIRS)
    assert _counts(rows) == DRAWN_NODE_ROWS
    assert res["summary"]["type_accuracy"]["matched"] == sum(v[0] for v in DRAWN_NODE_ROWS.values())
