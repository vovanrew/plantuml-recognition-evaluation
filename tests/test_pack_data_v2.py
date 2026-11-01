"""util/pack_data_v2.py: what goes into data_v2.zip, that it is the same bytes twice, and the check."""
import importlib.util
import zipfile
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "pack_data_v2", Path(__file__).resolve().parent.parent / "util" / "pack_data_v2.py")
pack_data_v2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pack_data_v2)


@pytest.fixture
def root(tmp_path):
    files = {
        "data_v2/element_f1/run_a/element_f1_results.json": '{"summary": 1}',
        "data_v2/relationship_f1/run_a/relationship_f1_results.json": '{"summary": 2}',
        "data_v2/_bridge/levels.json": '{"L0_v1": []}',
        "data_v2/_bridge/L0_v1/element_f1/run_a/element_f1_results.json": '{"summary": 3}',
        "data_v2/element_f1/run_a/gt_extracted/k1.puml": "@startuml\nA\n@enduml\n",
        "data_v2/element_f1/run_a/pred_extracted/k1.puml": "@startuml\nB\n@enduml\n",
    }
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return tmp_path


def test_archive_holds_the_json_files_only(root):
    pack_data_v2.pack(root, root / "data_v2.zip")
    names = zipfile.ZipFile(root / "data_v2.zip").namelist()
    assert names == sorted(names)
    assert names == [
        "data_v2/_bridge/L0_v1/element_f1/run_a/element_f1_results.json",
        "data_v2/_bridge/levels.json",
        "data_v2/element_f1/run_a/element_f1_results.json",
        "data_v2/relationship_f1/run_a/relationship_f1_results.json",
    ]


def test_same_files_give_the_same_bytes(root):
    pack_data_v2.pack(root, root / "a.zip")
    for p in (root / "data_v2").rglob("*.json"):
        p.touch()
    pack_data_v2.pack(root, root / "b.zip")
    assert (root / "a.zip").read_bytes() == (root / "b.zip").read_bytes()


def test_check_passes_on_a_fresh_archive(root):
    pack_data_v2.pack(root, root / "data_v2.zip")
    assert pack_data_v2.check(root, root / "data_v2.zip") == []


def test_check_reports_a_changed_file(root):
    pack_data_v2.pack(root, root / "data_v2.zip")
    (root / "data_v2/_bridge/levels.json").write_text('{"changed": true}')
    assert pack_data_v2.check(root, root / "data_v2.zip") == ["differs: data_v2/_bridge/levels.json"]


def test_check_reports_a_missing_and_an_extra_file(root):
    pack_data_v2.pack(root, root / "data_v2.zip")
    (root / "data_v2/_bridge/levels.json").unlink()
    (root / "data_v2/_bridge/new.json").write_text("{}")
    assert pack_data_v2.check(root, root / "data_v2.zip") == [
        "not in archive: data_v2/_bridge/new.json",
        "not in data_v2/: data_v2/_bridge/levels.json",
    ]
