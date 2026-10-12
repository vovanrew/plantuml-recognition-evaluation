"""Extractor drawn-edge tests, scorer v2 (shell out to the fork JAR).

An edge is a link or a message PlantUML draws. PlantUML marks as not drawn the
links it adds itself to arrange three or more unconnected elements of a group,
a link the source writes as `[hidden]`, a link to an element the source hides
or removes, and a message written as `[hidden]`: none of them is an edge. The
link of a tip (a note on a class member) to its owner carries the same mark,
but the image shows the note's pointer to the member, so it stays an edge.
Elements are not touched: every node is emitted either way.

The rule holds in every diagram the extractor reads as a graph of elements and
links, not in class diagrams alone, and for a note as for any other element;
only a tip is excepted, on whichever side of its owner it stands.

With `--undrawn-edges` the extractor emits every link and every message, which
is the scorer-v1 edge list; EXPECTED_ALL pins that the switch reproduces it.
"""
import os
import subprocess

import pytest

from element_f1_runner import EXTRACTOR_CLASS, EXTRACTOR_JAR, extract_graphs

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "drawn_edge_fixtures")

pytestmark = pytest.mark.skipif(
    not os.path.exists(EXTRACTOR_JAR),
    reason="DiagramStatsExtractor JAR not built; set PLANTUML_EXTRACTOR_JAR "
           "(see README, 'The structural extractor')")

LINE = "association"

# stem -> (source, target, relation) of every emitted edge, in order
EXPECTED = {
    # three unconnected classes at the root: PlantUML links them for layout
    "standalone_root": [],
    # six unconnected interfaces in a package: 0 edges, not 5
    "standalone_package": [],
    # three packages of three unconnected classes: PlantUML also links the
    # packages' corner elements to one another
    "standalone_packages": [],
    # fewer than three unconnected elements: PlantUML adds no link
    "standalone_two": [("A", "B", LINE)],
    # real relationships beside three unconnected elements: the real ones stay
    "standalone_mixed": [("A", "B", LINE), ("B", "C", "composition")],
    # a link written as [hidden], whatever its line and arrowhead
    "hidden_link": [("A", "B", LINE)],
    # a link to an element the source hides, or removes
    "hidden_element": [("A", "B", LINE)],
    "removed_element": [("A", "B", LINE)],
    # the link of a tip to its owner stays
    "tip": [("A", "B", LINE), ("A", "A$$$RIGHT", LINE)],
    # ...on every side: PlantUML builds owner -> tip for a note on the right of
    # a member and tip -> owner for one on the left; under `left to right
    # direction` the two sides become top and bottom, both tip -> owner
    "tip_sides": [("A$$$LEFT", "A", LINE), ("A", "A$$$RIGHT", LINE)],
    "tip_sides_rotated": [("A$$$TOP", "A", LINE), ("A$$$BOTTOM", "A", LINE)],
    # a note that is not a tip follows the rule: its link to a hidden element
    # and its link written [hidden] are left out, its drawn link stays
    "note_links": [("A", "D", LINE), ("on A", "A", "dependency")],
    # not a class diagram: components, a [hidden] link and three unconnected
    # components; states and a [hidden] transition
    "component": [("A", "B", LINE)],
    "state": [("A", "B", LINE)],
    # two association classes on one pair: PlantUML ties their two points with
    # a link it does not draw
    "association_points": [("A", "apoint7", LINE), ("apoint7", "B", LINE),
                           ("A", "apoint12", LINE), ("apoint12", "B", LINE),
                           ("C", "apoint7", "dependency"), ("apoint12", "D", "dependency")],
    # a hidden message and a hidden message from outside the diagram
    "hidden_message": [("A", "B", "message"), ("B", "A", "message")],
}

# stem -> every link and message: the scorer-v1 edge list
EXPECTED_ALL = {
    "standalone_root": [("A", "B", LINE), ("A", "C", LINE)],
    "standalone_package": [("Reader", "Writer", LINE), ("Writer", "Parser", LINE),
                           ("Reader", "Mapper", LINE), ("Mapper", "Loader", LINE),
                           ("Loader", "Closer", LINE)],
    "standalone_packages": [("A1", "A2", LINE), ("A1", "A3", LINE), ("B1", "B2", LINE),
                            ("B1", "B3", LINE), ("C1", "C2", LINE), ("C1", "C3", LINE),
                            ("A2", "B1", LINE), ("A3", "C1", LINE)],
    "standalone_two": EXPECTED["standalone_two"],
    "standalone_mixed": EXPECTED["standalone_mixed"] + [("D", "E", LINE), ("D", "F", LINE)],
    "hidden_link": [("A", "B", LINE), ("A", "C", LINE), ("C", "D", "dependency"),
                    ("B", "D", LINE)],
    "hidden_element": [("A", "B", LINE), ("B", "C", LINE)],
    "removed_element": [("A", "B", LINE), ("B", "C", LINE)],
    "tip": EXPECTED["tip"],
    "tip_sides": EXPECTED["tip_sides"],
    "tip_sides_rotated": EXPECTED["tip_sides_rotated"],
    "note_links": EXPECTED["note_links"] + [("on B", "B", "dependency"),
                                            ("on C", "C", "dependency")],
    "component": [("A", "B", LINE), ("A", "C", LINE), ("D", "E", LINE), ("D", "F", LINE)],
    "state": [("A", "B", LINE), ("A", "C", LINE)],
    "association_points": EXPECTED["association_points"] + [("apoint7", "apoint12", LINE)],
    "hidden_message": [("A", "B", "message"), ("A", "B", "message"), ("", "A", "message"),
                       ("B", "A", "message")],
}

# stem -> node names: the same with and without the switch
NODES = {
    "standalone_root": ["A", "B", "C"],
    "standalone_package": ["Reader", "Writer", "Parser", "Mapper", "Loader", "Closer"],
    "standalone_packages": ["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"],
    "standalone_two": ["A", "B", "C", "D"],
    "standalone_mixed": ["A", "B", "C", "D", "E", "F"],
    "hidden_link": ["A", "B", "C", "D"],
    "hidden_element": ["A", "B", "C"],      # the hidden element is still a node
    "removed_element": ["A", "B", "C"],     # and so is the removed one
    "tip": ["A", "B", "A$$$RIGHT"],
    "tip_sides": ["A", "A$$$LEFT", "A$$$RIGHT"],
    "tip_sides_rotated": ["A", "A$$$TOP", "A$$$BOTTOM"],
    "note_links": ["A", "B", "C", "D", "on A", "on B", "on C"],   # hidden B and its note stay
    "component": ["A", "B", "C", "D", "E", "F"],
    "state": ["A", "B", "C"],
    "association_points": ["A", "B", "C", "D", "apoint7", "apoint12"],
    "hidden_message": ["A", "B"],
}

# stem -> the `elements` counter: the same with and without the switch, and
# what scorer v1 counts (a hidden or removed element is counted)
ELEMENTS = {
    "standalone_root": {"class": 3},
    "standalone_package": {"interface": 6, "package": 1},
    "standalone_packages": {"class": 9, "package": 3},
    "standalone_two": {"class": 4},
    "standalone_mixed": {"class": 6},
    "hidden_link": {"class": 4},
    "hidden_element": {"class": 3},
    "removed_element": {"class": 3},
    "tip": {"class": 2, "tips": 1},
    "tip_sides": {"class": 1, "tips": 2},
    "tip_sides_rotated": {"class": 1, "tips": 2},
    "note_links": {"class": 4, "note": 3},
    "component": {"description": 6},
    "state": {"state": 3},
    "association_points": {"class": 4, "point_for_association": 2},
    "hidden_message": {"participant": 2},
}


@pytest.fixture(scope="module")
def graphs():
    return extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR)


@pytest.fixture(scope="module")
def all_graphs():
    return extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR, extractor_args=["--undrawn-edges"])


def _edges(record):
    return [(e["source"], e["target"], e["relation"]) for e in record["edges"]]


def test_every_fixture_is_covered(graphs, all_graphs):
    assert set(graphs) == set(all_graphs) == set(EXPECTED) == set(EXPECTED_ALL) == set(NODES)
    assert set(graphs) == set(ELEMENTS)
    assert all(rec["error"] is None for rec in graphs.values())
    assert all(rec["error"] is None for rec in all_graphs.values())


@pytest.mark.parametrize("stem", sorted(EXPECTED))
def test_drawn_edges(graphs, stem):
    assert _edges(graphs[stem]) == EXPECTED[stem]


@pytest.mark.parametrize("stem", sorted(EXPECTED_ALL))
def test_undrawn_edges_switch_emits_every_link(all_graphs, stem):
    assert _edges(all_graphs[stem]) == EXPECTED_ALL[stem]


@pytest.mark.parametrize("stem", sorted(NODES))
def test_nodes_are_not_touched(graphs, all_graphs, stem):
    assert [n["name"] for n in graphs[stem]["nodes"]] == NODES[stem]
    assert graphs[stem]["nodes"] == all_graphs[stem]["nodes"]
    assert graphs[stem]["elements"] == all_graphs[stem]["elements"]
    assert graphs[stem]["elements_total"] == all_graphs[stem]["elements_total"]


@pytest.mark.parametrize("stem", sorted(ELEMENTS))
def test_element_counters_are_those_of_v1(graphs, all_graphs, stem):
    for rec in (graphs[stem], all_graphs[stem]):
        assert rec["elements"] == ELEMENTS[stem]
        assert rec["elements_total"] == sum(ELEMENTS[stem].values())


def test_six_unconnected_interfaces_give_no_edge(graphs, all_graphs):
    assert graphs["standalone_package"]["edges"] == []
    assert len(all_graphs["standalone_package"]["edges"]) == 5


def test_fewer_than_three_unconnected_elements_get_no_layout_link(graphs, all_graphs):
    assert graphs["standalone_two"] == all_graphs["standalone_two"]


def test_tip_keeps_its_link(graphs, all_graphs):
    assert ("A", "A$$$RIGHT", LINE) in _edges(graphs["tip"])
    assert graphs["tip"] == all_graphs["tip"]


def test_tip_keeps_its_link_on_every_side(graphs, all_graphs):
    # the tip is the second end of the link of a note on the right of a member
    # and the first end of one on the left, at the top or at the bottom
    assert _edges(graphs["tip_sides"]) == [("A$$$LEFT", "A", LINE), ("A", "A$$$RIGHT", LINE)]
    assert _edges(graphs["tip_sides_rotated"]) == [("A$$$TOP", "A", LINE), ("A$$$BOTTOM", "A", LINE)]
    for stem in ("tip_sides", "tip_sides_rotated"):
        assert graphs[stem] == all_graphs[stem]


def test_note_follows_the_rule_only_a_tip_is_excepted(graphs, all_graphs):
    kept, every = _edges(graphs["note_links"]), _edges(all_graphs["note_links"])
    assert ("on A", "A", "dependency") in kept           # a drawn link of a note
    assert ("on B", "B", "dependency") in every          # a note's link to a hidden element
    assert ("on B", "B", "dependency") not in kept
    assert ("on C", "C", "dependency") in every          # a note's link written [hidden]
    assert ("on C", "C", "dependency") not in kept
    assert [n["type"] for n in graphs["note_links"]["nodes"]][4:] == ["note"] * 3


@pytest.mark.parametrize("stem,diagram_type,every", [("component", "component", 4),
                                                     ("state", "state", 2)])
def test_rule_holds_outside_class_diagrams(graphs, all_graphs, stem, diagram_type, every):
    assert graphs[stem]["diagram_type"] == all_graphs[stem]["diagram_type"] == diagram_type
    assert _edges(graphs[stem]) == [("A", "B", LINE)]
    assert len(all_graphs[stem]["edges"]) == every


def test_hidden_link_is_left_out_whatever_its_relation(all_graphs):
    # the three hidden links are an association with an arrowhead, a
    # dependency and a plain line
    hidden = all_graphs["hidden_link"]["edges"][1:]
    assert [(e["relation"], e.get("arrowhead")) for e in hidden] == [
        (LINE, "target"), ("dependency", None), (LINE, "none")]


@pytest.mark.parametrize("stem", sorted(EXPECTED))
def test_connection_counters_count_the_emitted_edges(graphs, all_graphs, stem):
    for rec in (graphs[stem], all_graphs[stem]):
        assert rec["connections_total"] == len(rec["edges"])
        assert sum(rec["connections"].values()) == rec["connections_total"]


def test_usage_text_names_the_switch():
    # scripts tell an extractor JAR that has the drawn-edge rule from an earlier
    # one by the option in its usage text
    proc = subprocess.run(["java", "-cp", EXTRACTOR_JAR, EXTRACTOR_CLASS],
                          capture_output=True, text=True)
    assert "--undrawn-edges" in proc.stderr


def test_every_switch_off_reproduces_v1_records():
    g = extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR,
                       extractor_args=["--names=raw", "--no-arrowheads", "--undrawn-edges"])
    for stem, expected in EXPECTED_ALL.items():
        assert _edges(g[stem]) == expected
        assert all(set(e) == {"source", "target", "relation", "label"} for e in g[stem]["edges"])
        assert [n["name"] for n in g[stem]["nodes"]] == NODES[stem]
        assert g[stem]["elements"] == ELEMENTS[stem]
