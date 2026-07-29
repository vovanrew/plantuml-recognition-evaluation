"""Per-model loader: read the four metric JSONs + test_set.json for a registered
run and join them by diagram key.

Join detail that matters: test_set.json keys carry a ``.puml`` suffix (37 are
split-file ``_NN.puml``) while the metric JSONs key on the bare blob_id (with the
``_NN`` kept). Stripping ``.puml`` from the test_set key gives a clean 1:1 join;
a raw equality join matches zero rows.

A pending/missing/incomplete run is skipped (returns ``None``) with a logged
note -- never an error. A present run whose metric key sets disagree with the
test set is a schema surprise and raises (STOP-and-report).
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from analysis.registry import ModelEntry

log = logging.getLogger(__name__)

DEFAULT_DATA_ROOT = Path(__file__).resolve().parent.parent / "data"

# metric name -> (subdir under data_root, results filename)
_METRIC_FILES = {
    "csr": ("csr", "csr_results.json"),
    "element_f1": ("element_f1", "element_f1_results.json"),
    "relationship_f1": ("relationship_f1", "relationship_f1_results.json"),
    "chrf": ("chrf", "chrf_results.json"),
}


@dataclass
class ModelData:
    """A registered model's joined per-diagram rows plus its raw metric summaries."""

    entry: ModelEntry
    rows: list[dict]          # joined per-diagram rows (key, primary_type, tier, + 4 metrics)
    summaries: dict           # {"csr","element_f1","relationship_f1","chrf"} -> summary block

    @property
    def run_dir(self) -> str:
        return self.entry.run_dir


def strip_puml(key: str) -> str:
    """test_set key -> metric key. Drops the ``.puml`` suffix, keeps any ``_NN``."""
    return key[:-5] if key.endswith(".puml") else key


def load_test_set_index(path: str | Path) -> dict[str, dict]:
    """Map stripped key -> per-diagram metadata (primary_type, tier, ...)."""
    with open(path, encoding="utf-8") as f:
        ts = json.load(f)
    index: dict[str, dict] = {}
    for d in ts["diagrams"]:
        index[strip_puml(d["key"])] = d
    return index


def _metric_path(data_root: Path, metric: str, run_dir: str) -> Path:
    subdir, fname = _METRIC_FILES[metric]
    return data_root / subdir / run_dir / fname


def load_model(
    entry: ModelEntry,
    data_root: str | Path = DEFAULT_DATA_ROOT,
    test_set_index: dict[str, dict] | None = None,
) -> ModelData | None:
    """Load + join one registered model. Returns ``None`` (with a logged note) for
    a pending/missing/incomplete run; raises on a present-but-inconsistent run."""
    data_root = Path(data_root)

    if entry.is_pending:
        log.info("skip %s: pending (no run_dir recorded)", entry.id)
        return None

    paths = {m: _metric_path(data_root, m, entry.run_dir) for m in _METRIC_FILES}
    missing = [str(p) for p in paths.values() if not p.exists()]
    if missing:
        log.info("skip %s (%s): metrics not on disk (%d/%d missing)",
                 entry.id, entry.run_dir, len(missing), len(paths))
        return None

    metrics = {}
    for m, p in paths.items():
        with open(p, encoding="utf-8") as f:
            metrics[m] = json.load(f)

    if test_set_index is None:
        test_set_index = load_test_set_index(data_root / "test_set.json")

    # index each metric's per-diagram rows by key
    by_key = {m: {row["key"]: row for row in metrics[m]["diagrams"]} for m in metrics}

    # every metric must cover exactly the test set's keys (schema surprise -> STOP)
    ts_keys = set(test_set_index)
    for m in metrics:
        mkeys = set(by_key[m])
        if mkeys != ts_keys:
            raise ValueError(
                f"{entry.id}: {m} keys do not match test set "
                f"(metric only: {len(mkeys - ts_keys)}, test only: {len(ts_keys - mkeys)})"
            )

    rows = []
    for key in sorted(ts_keys):  # deterministic order
        meta = test_set_index[key]
        rows.append({
            "key": key,
            "primary_type": meta["primary_type"],
            "tier": meta["tier"],
            "csr": by_key["csr"][key],
            "element": by_key["element_f1"][key],
            "relationship": by_key["relationship_f1"][key],
            "chrf": by_key["chrf"][key],
        })

    summaries = {m: metrics[m]["summary"] for m in metrics}
    log.info("loaded %s (%s): %d diagrams joined", entry.id, entry.run_dir, len(rows))
    return ModelData(entry=entry, rows=rows, summaries=summaries)


def load_panel(
    registry: list[ModelEntry],
    data_root: str | Path = DEFAULT_DATA_ROOT,
) -> list[ModelData]:
    """Load every entry whose run is on disk, in registry order. Pending/missing
    entries are skipped (logged), never an error."""
    data_root = Path(data_root)
    ts_index = load_test_set_index(data_root / "test_set.json")
    out = []
    for entry in registry:
        md = load_model(entry, data_root=data_root, test_set_index=ts_index)
        if md is not None:
            out.append(md)
    return out
