"""An answer with several @startuml...@enduml diagrams is scored on its first.

The first diagram is the one PlantUML displays. The extractor emits one record
per diagram (`<stem>.puml`, `<stem>.puml_1`, ...); scorer v1 kept whichever
record came last. The fixture holds a valid first diagram and a broken second.
"""
import json
import os

import pytest

from element_f1_runner import EXTRACTOR_JAR, extract_graphs, graphs_from_output

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "multi_diagram_fixtures")


def _rec(file, names, error=None):
    return json.dumps({"file": file, "nodes": [{"name": n, "type": "class"} for n in names],
                       "edges": [], "error": error})


OUTPUT = "\n".join([
    _rec("k1.puml", ["A", "B"]),
    _rec("k1.puml_1", [], "parse_error"),
    _rec("k1.puml_2", ["Z"]),
    _rec("k2_1.puml", ["C"]),       # a stem that itself ends in _<digits>
    "",
])


def test_first_diagram_is_kept():
    g = graphs_from_output(OUTPUT)
    assert set(g) == {"k1", "k2_1"}
    assert g["k1"]["file"] == "k1.puml"
    assert [n["name"] for n in g["k1"]["nodes"]] == ["A", "B"]
    assert [n["name"] for n in g["k2_1"]["nodes"]] == ["C"]


def test_last_diagram_is_kept_under_v1():
    g = graphs_from_output(OUTPUT, first_diagram=False)
    assert set(g) == {"k1", "k2_1"}
    assert g["k1"]["file"] == "k1.puml_2"
    assert [n["name"] for n in g["k1"]["nodes"]] == ["Z"]


jar = pytest.mark.skipif(
    not os.path.exists(EXTRACTOR_JAR),
    reason="DiagramStatsExtractor JAR not built; set PLANTUML_EXTRACTOR_JAR "
           "(see README, 'The structural extractor')")


@jar
def test_extractor_first_diagram_scored():
    rec = extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR)["two_diagrams"]
    assert rec["error"] is None
    assert [n["name"] for n in rec["nodes"]] == ["A", "B"]
    assert len(rec["edges"]) == 1


@jar
def test_extractor_last_diagram_scored_under_v1():
    rec = extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR, first_diagram=False)["two_diagrams"]
    assert rec["error"] == "parse_error"
    assert rec["nodes"] == []
