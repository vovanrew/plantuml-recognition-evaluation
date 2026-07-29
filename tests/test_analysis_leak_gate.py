"""Tests for the reasoning_leak==0 eligibility gate."""
from pathlib import Path

from analysis.leak_gate import count_reasoning_leaks, predictions_dir


def _write(p: Path, text: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_predictions_dir_path():
    assert predictions_dir("data", "run1") == Path("data") / "runs" / "run1"


def test_counts_only_files_with_think_block(tmp_path):
    _write(tmp_path / "a.puml", "@startuml\nclass A\n@enduml\n")
    _write(tmp_path / "b.puml", "<think>let me reason</think>\n@startuml\nclass B\n@enduml\n")
    _write(tmp_path / "c.puml", "@startuml\nclass C\n@enduml\n")
    assert count_reasoning_leaks(tmp_path) == 1


def test_clean_run_is_zero(tmp_path):
    _write(tmp_path / "a.puml", "@startuml\nclass A\n@enduml\n")
    _write(tmp_path / "b.puml", "@startuml\nclass B\n@enduml\n")
    assert count_reasoning_leaks(tmp_path) == 0


def test_non_puml_files_ignored(tmp_path):
    _write(tmp_path / "resp.json", '{"x": "<think>not a prediction</think>"}')
    _write(tmp_path / "run_meta.json", '{"<think>": 1}')
    _write(tmp_path / "a.puml", "@startuml\nclass A\n@enduml\n")
    assert count_reasoning_leaks(tmp_path) == 0


def test_missing_dir_is_zero(tmp_path):
    assert count_reasoning_leaks(tmp_path / "nope") == 0
