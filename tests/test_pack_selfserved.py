"""util/pack_selfserved.py: what goes into data_selfserved.zip, links, same bytes twice, the check."""
import importlib.util
import stat
import zipfile
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "pack_selfserved", Path(__file__).resolve().parent.parent / "util" / "pack_selfserved.py")
pack_selfserved = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pack_selfserved)


@pytest.fixture
def fine_tune(tmp_path):
    for run in pack_selfserved.RUNS:
        files = {
            f"answers/k1.json": '{"choices": []}',
            f"answers/k1.puml": "@startuml\nA\n@enduml\n",
            f"scores/v2/csr/{run}/csr_results.json": '{"csr": 1}',
            f"scores/v1/element_f1/{run}/element_f1_results.json": '{"f1": 1}',
            "scores/v1/csr": "../v2/csr",  # a link checked out as a text file
            "answer_manifest.json": '{"diagrams": 1}',
        }
        for rel, text in files.items():
            p = tmp_path / "runs" / "test" / run / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
    return tmp_path


def test_archive_layout(fine_tune, tmp_path):
    pack_selfserved.pack(fine_tune, tmp_path / "s.zip")
    names = zipfile.ZipFile(tmp_path / "s.zip").namelist()
    assert names == sorted(names)
    assert len(names) == 6 * 3
    assert "data_selfserved/runs/test/9B_zero_shot/scores/v2/csr/9B_zero_shot/csr_results.json" in names


def test_link_stub_is_stored_as_a_link(fine_tune, tmp_path):
    pack_selfserved.pack(fine_tune, tmp_path / "s.zip")
    z = zipfile.ZipFile(tmp_path / "s.zip")
    info = z.getinfo("data_selfserved/runs/test/2B_zero_shot/scores/v1/csr")
    assert stat.S_ISLNK(info.external_attr >> 16)
    assert z.read(info) == b"../v2/csr"
    other = z.getinfo("data_selfserved/runs/test/2B_zero_shot/answer_manifest.json")
    assert stat.S_ISREG(other.external_attr >> 16)


def test_same_files_give_the_same_bytes(fine_tune, tmp_path):
    pack_selfserved.pack(fine_tune, tmp_path / "a.zip")
    for p in (fine_tune / "runs").rglob("*.json"):
        p.touch()
    pack_selfserved.pack(fine_tune, tmp_path / "b.zip")
    assert (tmp_path / "a.zip").read_bytes() == (tmp_path / "b.zip").read_bytes()


def test_check_passes_then_reports_a_change(fine_tune, tmp_path):
    pack_selfserved.pack(fine_tune, tmp_path / "s.zip")
    assert pack_selfserved.check(fine_tune, tmp_path / "s.zip") == []
    (fine_tune / "runs/test/27B_zero_shot/answer_manifest.json").write_text("{}")
    assert pack_selfserved.check(fine_tune, tmp_path / "s.zip") == [
        "differs: data_selfserved/runs/test/27B_zero_shot/answer_manifest.json"]
