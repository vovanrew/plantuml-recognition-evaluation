"""Scorer-v2 switches of the two structural runners.

The defaults are scorer v2; each flag turns one rule off, and every flag
together is scorer v1. The first half checks the argument mapping alone; the
second half runs both runners end to end through the extractor JAR on five
ground-truth / prediction pairs, with the defaults, with each switch alone and
with every switch, and checks the scores, the type-accuracy counts, the
per-relation counts and the `scorer` block of the results file.
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
           "--extractor-arg=--names=raw", "--extractor-arg=--no-arrowheads"]


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
    assert args.extractor_arg == ["--names=raw", "--no-arrowheads"]


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
    (ALL_OFF, {"whitespace", "brackets", "names", "first"}),
]
_IDS = lambda case: " ".join(f.replace("--extractor-arg=", "") for f in case) or "defaults"


def _run(runner, tmp_path, flags, monkeypatch):
    gt, pred, out = tmp_path / "gt", tmp_path / "pred", tmp_path / "out"
    for d in (gt, pred):
        d.mkdir()
    for key, (g, p, _) in PAIRS.items():
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
