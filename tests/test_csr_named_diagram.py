"""The compile check finds the image of an answer that names its diagram.

PlantUML names the image after the text that follows ``@startuml`` on its line,
not after the source file. The check looks for an image named after the diagram
key, so the batch is rendered from copies without that name.
"""
import os

from csr_runner import extract_puml, matched_pngs, without_diagram_name


def test_name_after_startuml_is_dropped():
    assert without_diagram_name("@startuml Orders\nA -> B\n@enduml") == "@startuml\nA -> B\n@enduml"


def test_name_with_spaces_or_extension_is_dropped():
    assert without_diagram_name("@startuml My diagram v2\n@enduml") == "@startuml\n@enduml"
    assert without_diagram_name("@startuml ttr.uml\r\n@enduml") == "@startuml\r\n@enduml"


def test_plain_startuml_is_unchanged():
    code = "@startuml\nclass A\n@enduml"
    assert without_diagram_name(code) == code
    assert without_diagram_name("@startuml   \nclass A\n@enduml") == "@startuml   \nclass A\n@enduml"


def test_every_diagram_of_an_answer_loses_its_name():
    code = "@startuml one\nA -> B\n@enduml\n@startuml two\nC -> D\n@enduml"
    assert without_diagram_name(code) == "@startuml\nA -> B\n@enduml\n@startuml\nC -> D\n@enduml"


def test_only_the_startuml_line_changes():
    code = "@startuml Shop\ntitle @startuml Shop\nnote right: see @startuml x\n@enduml"
    assert without_diagram_name(code) == (
        "@startuml\ntitle @startuml Shop\nnote right: see @startuml x\n@enduml")


def test_extracted_text_keeps_the_name():
    """The other metrics read the extracted answer, which is not changed."""
    raw = "```plantuml\n@startuml Orders\nA -> B\n@enduml\n```"
    assert extract_puml(raw) == "@startuml Orders\nA -> B\n@enduml"


def test_image_is_matched_by_key_not_by_diagram_name(tmp_path):
    (tmp_path / "Orders.png").write_bytes(b"x" * 300)
    assert matched_pngs("abc123", str(tmp_path)) == []
    (tmp_path / "abc123.png").write_bytes(b"x" * 300)
    assert matched_pngs("abc123", str(tmp_path)) == [os.path.join(str(tmp_path), "abc123.png")]
