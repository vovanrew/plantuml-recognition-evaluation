"""Extractor orientation tests (shell out to the DiagramStatsExtractor fork JAR).

Class-diagram directional relations must be canonicalized by their link
decoration, not source token order: rendering `A *-- B` and `B --* A` produces
the identical relationship (composition diamond on A in both), so both must emit
the same (source, target, relation) edge. The canonical orientations follow
evaluation-framework.md §2.2/§4: inheritance child->parent, composition and
aggregation whole->part, dependency dependent->dependency (arrow tail->head).
"""
import os

import pytest

from element_f1_runner import EXTRACTOR_JAR, extract_graphs

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "direction_fixtures")

pytestmark = pytest.mark.skipif(
    not os.path.exists(EXTRACTOR_JAR),
    reason="DiagramStatsExtractor JAR not built; set PLANTUML_EXTRACTOR_JAR "
           "(see README, 'The structural extractor')")

# Each pair renders one identical relationship written in opposite token order;
# both stems must emit this single canonical (source, target, relation) edge.
EXPECTED = {
    ("comp_A", "comp_B"): ("A", "B", "composition"),   # whole(A) -> part(B)
    ("inh_A", "inh_B"): ("B", "A", "inheritance"),     # child(B) -> parent(A)
    ("agg_A", "agg_B"): ("A", "B", "aggregation"),     # whole(A) -> part(B)
    ("dep_A", "dep_B"): ("A", "B", "dependency"),      # tail(A) -> head(B)
}


@pytest.fixture(scope="module")
def graphs():
    return extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR)


def _only_edge(record):
    edges = record["edges"]
    assert len(edges) == 1, f"expected exactly one edge, got {edges}"
    e = edges[0]
    return (e["source"], e["target"], e["relation"])


@pytest.mark.parametrize("pair,expected", list(EXPECTED.items()),
                         ids=[p[0].rsplit("_", 1)[0] for p in EXPECTED])
def test_pair_canonical_orientation(graphs, pair, expected):
    a_stem, b_stem = pair
    a = _only_edge(graphs[a_stem])
    b = _only_edge(graphs[b_stem])
    assert a == expected, f"{a_stem}: {a} != {expected}"
    assert b == expected, f"{b_stem}: {b} != {expected}"
