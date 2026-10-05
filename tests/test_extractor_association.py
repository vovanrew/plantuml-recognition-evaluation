"""Extractor association-arrowhead tests, scorer v2 (shell out to the fork JAR).

An association edge carries `arrowhead`: which end of the emitted
(source, target) holds an arrowhead -- none, source, target or both. With
exactly one arrowhead the edge is directed tail -> head; a reversed or a dropped
arrowhead is then a miss, as a dropped diamond already is. A plain line and a
line with an arrowhead at both ends stay undirected.
"""
import os

import pytest

import relationship_f1 as rf
from element_f1_runner import EXTRACTOR_JAR, extract_graphs

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "association_fixtures")

pytestmark = pytest.mark.skipif(
    not os.path.exists(EXTRACTOR_JAR),
    reason="DiagramStatsExtractor JAR not built; set PLANTUML_EXTRACTOR_JAR "
           "(see README, 'The structural extractor')")

# stem -> (source, target, relation, arrowhead) of the single emitted edge
EXPECTED = {
    "arrow_AB": ("A", "B", "association", "target"),                 # A --> B
    "arrow_AB_written_from_B": ("B", "A", "association", "source"),  # B <-- A
    "arrow_BA": ("B", "A", "association", "target"),                 # B --> A
    "plain_AB": ("A", "B", "association", "none"),                   # A -- B
    "plain_BA": ("B", "A", "association", "none"),                   # B -- A
    "both_AB": ("A", "B", "association", "both"),                    # A <--> B
    "both_BA": ("B", "A", "association", "both"),                    # B <--> A
    "dependency_AB": ("A", "B", "dependency", None),                 # A ..> B
}

AB_DIRECTED = ("a", "b", "association", rf.DIRECTED)
AB_UNDIRECTED = ("a", "b", "association")


@pytest.fixture(scope="module")
def graphs():
    return extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR)


def _only_edge(record):
    edges = record["edges"]
    assert len(edges) == 1, f"expected exactly one edge, got {edges}"
    return edges[0]


def _key(graphs, stem, rules=rf.V2):
    return rf.edge_key(_only_edge(graphs[stem]), rules)


@pytest.mark.parametrize("stem,expected", list(EXPECTED.items()))
def test_arrowhead_end(graphs, stem, expected):
    e = _only_edge(graphs[stem])
    assert (e["source"], e["target"], e["relation"], e.get("arrowhead")) == expected


def test_arrowhead_is_emitted_for_associations_only(graphs):
    assert "arrowhead" not in _only_edge(graphs["dependency_AB"])


def test_same_arrow_written_either_way_matches(graphs):
    assert _key(graphs, "arrow_AB") == AB_DIRECTED
    assert _key(graphs, "arrow_AB_written_from_B") == AB_DIRECTED


def test_reversed_arrow_is_a_miss(graphs):
    assert _key(graphs, "arrow_BA") == ("b", "a", "association", rf.DIRECTED)
    assert _key(graphs, "arrow_BA") != _key(graphs, "arrow_AB")


def test_dropped_arrowhead_is_a_miss(graphs):
    assert _key(graphs, "plain_AB") != _key(graphs, "arrow_AB")


def test_plain_line_written_either_way_matches(graphs):
    assert _key(graphs, "plain_AB") == _key(graphs, "plain_BA") == AB_UNDIRECTED


def test_two_arrowheads_are_undirected(graphs):
    assert _key(graphs, "both_AB") == _key(graphs, "both_BA") == AB_UNDIRECTED


def test_v1_rules_make_every_association_undirected(graphs):
    for stem in ("arrow_AB", "arrow_AB_written_from_B", "arrow_BA",
                 "plain_AB", "plain_BA", "both_AB", "both_BA"):
        assert _key(graphs, stem, rf.V1) == AB_UNDIRECTED


def test_no_arrowheads_switch_reproduces_v1_records():
    g = extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR, extractor_args=["--no-arrowheads"])
    for stem, (source, target, relation, _) in EXPECTED.items():
        e = _only_edge(g[stem])
        assert set(e) == {"source", "target", "relation", "label"}
        assert (e["source"], e["target"], e["relation"]) == (source, target, relation)
