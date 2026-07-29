"""Guards the frozen zero-shot prompt (prompts/zero_shot.txt).

The prompt is a reproducibility artifact: one shared template for every model
and diagram type. These tests pin its load path and the properties the
benchmark design relies on; a wording re-freeze must update the expected text
here and in methodology/benchmark-protocol.md together.
"""
import os

PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "zero_shot.txt")

FROZEN = (
    "This image is a UML diagram. Reproduce it as valid PlantUML code that, "
    "when rendered, matches the diagram as closely as possible: capture every "
    "element with the UML notation shown (e.g. actor, interface, database), "
    "its contents and labels, and every relationship. Output only the PlantUML "
    "code starting with @startuml and ending with @enduml, with no explanation."
)


def load():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return f.read().strip()


def test_prompt_file_is_frozen_verbatim():
    assert load() == FROZEN


def test_prompt_is_single_line_plain_ascii():
    # one paragraph, no template placeholders, nothing model- or type-specific
    text = load()
    assert "\n" not in text
    assert "{" not in text and "}" not in text
    assert text.isascii()


def test_prompt_does_not_hint_diagram_type():
    # zero-shot: type identification is part of the task; the only "diagram"
    # mentions must be generic ("a UML diagram", "the diagram")
    text = load().lower()
    assert "class diagram" not in text
    assert "sequence diagram" not in text


def test_prompt_constrains_output_block():
    text = load()
    assert "@startuml" in text and "@enduml" in text
