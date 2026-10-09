"""Extractor name tests, scorer v2 (shell out to the DiagramStatsExtractor fork JAR).

A node name is the text PlantUML draws for the label, read through PlantUML's own
markup parser: formatting markup, icons and the letter of a stereotype spot are
not part of it; generics and other single-angle text are. When the lines of a
label differ in font size, the line(s) at the largest size are the name. The
label lines of the fixtures are taken from the ground-truth sources named below.

The label is read on the path PlantUML draws that kind of element with: a class
header has no `__underline__` and no list items; the label of a note, a use case
or a rectangle-like element is cut at separator lines first; every other label
goes through the parser whole, with every markup on.

With `--names=raw` the extractor joins the label lines as typed, which is the
scorer-v1 name; EXPECTED_RAW pins that the switch reproduces it.
"""
import os

import pytest

import element_f1 as ef
from element_f1_runner import EXTRACTOR_JAR, extract_graphs

FIXTURE_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "name_fixtures")

pytestmark = pytest.mark.skipif(
    not os.path.exists(EXTRACTOR_JAR),
    reason="DiagramStatsExtractor JAR not built; set PLANTUML_EXTRACTOR_JAR "
           "(see README, 'The structural extractor')")

# stem -> node names, in declaration order
EXPECTED = {
    # bold name above a smaller package line (GT 0bffda3c5610)
    "size_bold_package": ["ConquestMapPart"],
    # the same pattern without <b> (GT 32dd5e5f68d0)
    "size_package": ["ViewFactory"],
    # one explicit size: the unsized line is drawn at the element's own font
    # size, which is larger (GT 461bf802c53c)
    "size_one_explicit": ["DimensionComponent"],
    # lines of one size are all kept (GT 0bbd74f73c7b)
    "multiline_plain": ["Operation Queue"],
    # the size of a line is the largest among its text atoms: a line that
    # reaches the largest size through one word is kept whole
    "size_within_line": ["A b C", "D"],
    # a generic inside markup survives the markup removal (GT ab45a1d1120a)
    "generic_in_markup": ["InMemoryRepository<T, I>"],
    # single-angle text is not markup (GT 3000289f, 838542d0); <I> is: PlantUML
    # reads it as the italic tag, on both sides alike
    "angle_text": ["<FHIR API> HPI", "«analysis» list: List<Variable>", "Foo Bar"],
    # underline, icon, bold (GT 6744cc18cdc7, c5bb38162326); a URL keeps its
    # single //, a pair of // is PlantUML's italic markup
    "inline_markup": ["api / Handler", "Representation", "Bold name",
                      "see http://example.org/a", "see http:example.org/ab"],
    "emoji": ["Classification"],                       # GT 49f7f03b47c0
    # a label with no drawn text falls back to the alias, as an empty label does
    "icon_only": ["IconOnly", "Named"],
    # stereotype spot: the label stays, the circle letter does not (GT 32b85a4b,
    # 2830a2eabd8a)
    "spot_label": ["«@Controller» SubscriptionController"],
    "spot_empty": ["Producer", "Tansport"],
    # a one-letter participant keeps its letter; a letter typed into the name
    # stays; a one-letter stereotype typed into the name stays a stereotype
    "letter_names": ["«x» A", "C Producer", "«S» Tansport"],
    "italic_stereotype": ["«presentation» DefineNewCategoryUI"],   # GT 6c7324c7
    # <U+XXXX> escapes are decoded (GT 532d5a1ff757, 938e9cc0e6b8)
    "unicode_brackets": ["≪Application≫ : OrderDeliveredController", "«Boundary» MakerUI"],
    "unicode_brackets_pred": ["«Application» : OrderDeliveredController", "«Boundary» MakerUI"],
    # the title of a rule is drawn text and is kept (GT df9a59b4a945)
    "note_rule_title": ["A", "Your are analyzing: AnalyzeAST detailed  Filter "
                             "You can click the names. Home:    index.html"],
    # a creole heading is drawn larger than the other lines of the note, so it
    # alone is the name
    "note_heading": ["A", "Filter"],
    # a class header is drawn without `__underline__` and without list items:
    # double underscores, a leading asterisk and a leading hash are text, a
    # `**…**` pair is bold (corpus 98ecad690094, 19cd18cb54e1, 095002d9b1a8)
    "class_header": ["__main__", "client_new_connection_SYNC__NO_MSG__AT_MOST", "Transaction",
                     "*mongo.Client", "# Numbered"],
    # an object, a map and a childless package are read whole, with every
    # markup on: a `__…__` pair is an underline, and a lone `==` line is drawn
    # as a heading `=`, the largest line
    "plain_label": ["obj", "=", "map", "=", "pkg", "="],
    # in a use case, a rectangle, a note and a childless rectangle a separator
    # line is a drawn rule, not text; its title is text (corpus 50d94af635a4)
    "separator_lines": ["Dummy", "Delete Reminder Actor:User Some more text Conclusion last",
                        "API Gateway /api/v2/petstore", "first second third",
                        "Group title group second"],
    # a participant label is not cut at separators: PlantUML draws the lone
    # `==` as a heading `=`, the largest line
    "separator_participant": ["="],
    # a circle and a business use case are cut at separators too; a lone `..`
    # is a separator; a separator title of `-`, `.` or `_` alone is part of the
    # rule; an embedded diagram stays whole inside its block and is not text
    "body_path_kinds": ["Dummy", "Top Bottom", "Plan Actors", "alpha beta gamma delta epsilon",
                        "before after"],
}

EXPECTED_RAW = {
    "size_bold_package": ["<b><size:14>ConquestMapPart</b> <size:10>soen6441riskgame.enums"],
    "size_package": ["<size:14>ViewFactory <size:10>it.tidalwave.northernwind.frontend.ui"],
    "size_one_explicit": ["<size:10>Components:: <color:black>DimensionComponent"],
    "multiline_plain": ["Operation Queue"],
    "size_within_line": ["<size:20>A</size> <size:11>b <size:20>C</size>",
                         "<size:20>D</size> <size:11>e f"],
    "icon_only": ["<:file_folder:>", "Named"],
    "generic_in_markup": ["<b><size:14>InMemoryRepository<T, I></b> "
                          "<size:10>eapli.framework.infrastructure.repositories.impl.inmemory"],
    "angle_text": ["<FHIR API> HPI", "<<analysis>> list: List<Variable>", "Foo<I> Bar"],
    "inline_markup": ["__api__ / Handler", "<&transfer> Representation", "**Bold** name",
                      "see http://example.org/a", "see http://example.org/a//b"],
    "emoji": ["<:file_folder:> Classification"],
    "spot_label": ["C << @Controller >> SubscriptionController"],
    "spot_empty": ["C  Producer", "S  Tansport"],
    "letter_names": ["<<x>> A", "C Producer", "<<S>> Tansport"],
    "italic_stereotype": ["//<<presentation>>// DefineNewCategoryUI"],
    "unicode_brackets": ["<U+226A>Application<U+226B> : OrderDeliveredController",
                         "<U+00ab>Boundary<U+00bb> MakerUI"],
    "unicode_brackets_pred": ["<<Application>> : OrderDeliveredController", "<<Boundary>> MakerUI"],
    "note_rule_title": ["A", "Your are analyzing: AnalyzeAST **detailed**   ==Filter== "
                             "You can click the names. * Home:    [[index.html]]"],
    "note_heading": ["A", "Your are analyzing: AnalyzeAST **detailed** ---- =Filter "
                          "You can click the names."],
    "class_header": ["__main__", "client_new_connection_SYNC__NO_MSG__AT_MOST",
                     "**     Transaction     **", "*mongo.Client", "# Numbered"],
    "plain_label": ["__obj__", "ObjTop == ObjBottom", "__map__", "MapTop == MapBottom",
                    "__pkg__", "PkgTop == PkgBottom"],
    "body_path_kinds": ["Dummy", "Top == Bottom", "Plan == Actors",
                        "alpha .. beta ----- gamma ..... delta _____ epsilon",
                        "before {{ class Inner note as M in == side end note }} after"],
    "separator_lines": ["Dummy", "Delete Reminder -- Actor:User == Some more text ..Conclusion.. last",
                        "<b>API Gateway</b> === /api/v2/petstore", "first ===== second __ third",
                        "Group title === group second"],
    "separator_participant": ["Top == Bottom"],
}

# stem -> match keys after normalize(): what the scorer compares
EXPECTED_KEYS = {
    "spot_label": ["subscriptioncontroller"],
    "spot_empty": ["producer", "tansport"],
    "letter_names": ["a", "c producer", "tansport"],
    "italic_stereotype": ["definenewcategoryui"],
    "angle_text": ["<fhir api> hpi", "list: list<variable>", "foo bar"],
    "unicode_brackets": [": orderdeliveredcontroller", "makerui"],
    "unicode_brackets_pred": [": orderdeliveredcontroller", "makerui"],
    "class_header": ["__main__", "client_new_connection_sync__no_msg__at_most", "transaction",
                     "*mongo.client", "# numbered"],
    "separator_lines": ["dummy", "delete reminder actor:user some more text conclusion last",
                        "api gateway /api/v2/petstore", "first second third",
                        "group title group second"],
}


def _names(record):
    return [n["name"] for n in record["nodes"]]


@pytest.fixture(scope="module")
def graphs():
    return extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR)


@pytest.fixture(scope="module")
def raw_graphs():
    return extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR, extractor_args=["--names=raw"])


def test_every_fixture_is_covered(graphs):
    assert set(graphs) == set(EXPECTED) == set(EXPECTED_RAW)
    assert all(rec["error"] is None for rec in graphs.values())


@pytest.mark.parametrize("stem", sorted(EXPECTED))
def test_drawn_name(graphs, stem):
    assert _names(graphs[stem]) == EXPECTED[stem]


@pytest.mark.parametrize("stem", sorted(EXPECTED_KEYS))
def test_match_key(graphs, stem):
    assert ef.names_from_record(graphs[stem]) == EXPECTED_KEYS[stem]


@pytest.mark.parametrize("stem", sorted(EXPECTED_RAW))
def test_raw_names_reproduce_v1(raw_graphs, stem):
    assert _names(raw_graphs[stem]) == EXPECTED_RAW[stem]


def test_markup_mode_keeps_every_drawn_line():
    g = extract_graphs(FIXTURE_DIR, EXTRACTOR_JAR, extractor_args=["--names=markup"])
    assert _names(g["size_bold_package"]) == ["ConquestMapPart soen6441riskgame.enums"]
    assert _names(g["size_one_explicit"]) == ["Components:: DimensionComponent"]
    assert _names(g["spot_empty"]) == ["Producer", "Tansport"]
    assert _names(g["size_within_line"]) == ["A b C", "D e f"]
    assert _names(g["separator_participant"]) == ["Top = Bottom"]
    assert _names(g["plain_label"]) == ["obj", "ObjTop = ObjBottom", "map", "MapTop = MapBottom",
                                        "pkg", "PkgTop = PkgBottom"]


def test_unsized_text_starts_from_the_diagram_style(tmp_path):
    # the element's own font size decides which line of size_one_explicit is
    # the larger one; a skinparam in the source moves it
    src = open(os.path.join(FIXTURE_DIR, "size_one_explicit.puml"), encoding="utf-8").read()
    (tmp_path / "small.puml").write_text(
        src.replace("@startuml\n", "@startuml\nskinparam classFontSize 8\n"), encoding="utf-8")
    (tmp_path / "equal.puml").write_text(
        src.replace("@startuml\n", "@startuml\nskinparam classFontSize 10\n"), encoding="utf-8")
    g = extract_graphs(str(tmp_path), EXTRACTOR_JAR)
    assert _names(g["small"]) == ["Components::"]
    assert _names(g["equal"]) == ["Components:: DimensionComponent"]
    forced = extract_graphs(str(tmp_path), EXTRACTOR_JAR, extractor_args=["--name-font-size=12"])
    assert _names(forced["small"]) == ["DimensionComponent"]


# --- the size unsized text starts from, per element kind ---
#
# A label `<size:N>sized\nplain` has one sized line and one line drawn at the
# element's own font size. The plain line is the name when N is below that
# size, both lines when N equals it, the sized line when N is above it. The
# own size is PlantUML's skin default (class name 14 pt, participant 14 pt,
# note 13 pt, childless group 14 pt) unless the diagram's source sets another.

# kind -> (diagram body, skin default in pt, skinparam that sets the size)
BASE_SIZE_CASES = {
    "class": ('class C as "%s"', 14, "skinparam classFontSize %d"),
    "participant": ('participant "%s" as P', 14, "skinparam participantFontSize %d"),
    "note": ('class A\nnote "%s" as N', 13, "skinparam noteFontSize %d"),
    "childless_group": ('package "%s" as G {\n}', 14, None),
}


def _bracket(tmp_path, kind, base, header=""):
    """Names read for N = base - 1, base, base + 1."""
    body = BASE_SIZE_CASES[kind][0]
    for n in (base - 1, base, base + 1):
        label = "<size:%d>sized\\nplain" % n
        (tmp_path / ("n%d.puml" % n)).write_text(
            "@startuml\n%s%s\n@enduml\n" % (header, body % label), encoding="utf-8")
    g = extract_graphs(str(tmp_path), EXTRACTOR_JAR)
    return [_names(g["n%d" % n])[-1] for n in (base - 1, base, base + 1)]


@pytest.mark.parametrize("kind", sorted(BASE_SIZE_CASES))
def test_base_size_is_the_skin_default(tmp_path, kind):
    base = BASE_SIZE_CASES[kind][1]
    assert _bracket(tmp_path, kind, base) == ["plain", "sized plain", "sized"]


@pytest.mark.parametrize("kind", ["class", "participant", "note"])
def test_base_size_follows_the_diagram_source(tmp_path, kind):
    skinparam = BASE_SIZE_CASES[kind][2] % 20 + "\n"
    assert _bracket(tmp_path, kind, 20, header=skinparam) == ["plain", "sized plain", "sized"]


@pytest.mark.parametrize("kind", ["class", "participant", "note"])
def test_base_size_follows_a_style_block(tmp_path, kind):
    element = {"class": "class", "participant": "participant", "note": "note"}[kind]
    style = "<style>\n%s {\n  FontSize 20\n}\n</style>\n" % element
    assert _bracket(tmp_path, kind, 20, header=style) == ["plain", "sized plain", "sized"]
