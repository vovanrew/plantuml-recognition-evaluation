"""Human-rater check of the metrics on model-against-model pairs.

For one test diagram and two models, a rater sees the test image and the renders of the two
models' answers, unlabelled and in random order as A and B, and answers: A, B, or about the same.
The report says how often each rater picks the answer the metric scores higher, and how far the
two raters agree.

Comparisons (COMPARISONS): Gemini 3.1 Pro vs Claude Opus 4.6, GPT-5.2 vs Claude Opus 4.6,
Qwen3.5-397B-A17B vs Qwen3.5-27B, Qwen3.5-9B vs Qwen3.5-27B.

Pool, per comparison: the test diagrams whose two answers both compiled (CSR row) and whose
Element F1 or Relationship F1 differ, minus the excluded diagrams (``--exclude``: a keys file of an
earlier rater round, whose diagrams the raters may have seen). A pair's direction is the model the
metric prefers: by Element F1 when it differs, otherwise by Relationship F1. A pair's stratum is
"ef" when Element F1 differs, "rf" when only Relationship F1 does.

Sample: 15 pairs per comparison, 60 in all. The direction the pool prefers more often takes 8
pairs, the other 7. Within a direction, half (rounded down) are "ef" pairs and the rest "rf"
pairs, so that Element F1 agreement rests on enough pairs; within a direction x stratum cell,
class and sequence are split as evenly as the cell allows (class takes the odd one). Each cell
is drawn with random.Random(f"{SEED}|rater-models|<comparison>|<direction>|<stratum>|<type>")
.sample over the sorted keys. Comparisons are drawn in COMPARISONS order, and a diagram drawn
for one comparison leaves the later pools, so each test diagram appears once. Pair ids P01..P60
come from one seeded shuffle; which answer is A comes from a second seeded stream; each rater
sees the pairs in a seeded order of their own.

Pictures: the answer's PlantUML block (the scorer's extract_puml) rendered by the render pipeline
that made the test images (``--render-py``: render.py of the fine-tuning study, which pins the
renderer, Graphviz guard and image stages); the test image itself as the original. A sample
answer that does not render to exactly one picture stops the build.

Numbers (all descriptive, no pass mark): per rater and metric, the share of A/B picks that chose
the answer with the higher score, on the pairs where that metric differs, with a Wilson 95%
interval, and the count of "same"; counts per comparison and per type; Cohen's kappa and raw
agreement between the raters on A / B / same; the pairs where both raters chose against the
pair's direction, for the author to describe (``differences.csv``: pair, differs, kind).

    python -m analysis.rater_check draw   --data-root data_paper \\
        --registry analysis/model_registry_paper.json --exclude <earlier keys.json>
    python -m analysis.rater_check render --data-root data_paper --render-py ../fine-tune/build/render.py
    python -m analysis.rater_check sheets --data-root data_paper
    python -m analysis.rater_check report

Output folder: analysis/out_paper/rater_check/ (keys, ratings, report; renders under render/,
not tracked). The rating pages are copies of the pictures for the raters and go to rater_sheets/,
which is not tracked.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import importlib.util
import json
import math
import random
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evaluation"))

from csr_runner import extract_puml  # noqa: E402

from analysis.failure_sampler import SEED  # noqa: E402
from analysis.loader import load_panel  # noqa: E402
from analysis.registry import load_registry  # noqa: E402

OUT = ROOT / "analysis" / "out_paper" / "rater_check"
SHEETS = ROOT / "rater_sheets"
COMPARISONS = (
    ("gemini-3.1-pro", "claude-opus-4-6"),
    ("gpt-5.2", "claude-opus-4-6"),
    ("qwen3.5-397b-a17b", "qwen3.5-27b"),
    ("qwen3.5-9b", "qwen3.5-27b"),
)
PER_COMPARISON = 15
TYPES = ("class", "sequence")
STRATA = ("ef", "rf")
METRICS = {"ef": "element", "rf": "relationship"}
RATERS = ("R1", "R2")                             # R1 the author, R2 the second rater
CHOICES = ("A", "B", "same")
DIFFERENCES = "differences.csv"
Z95 = 1.959963984540054

# The raters are Ukrainian, so the page is in Ukrainian. The English meaning:
#   "Which drawing shows the original diagram more faithfully: A, B, or about the same?"
#   "Judge the content: which boxes there are, their names and members, the messages and their text,
#    and what is connected to what, with which kind of arrow. Ignore layout, position and colour."
QUESTION = "Який малюнок точніше відтворює оригінальну діаграму: A, B чи приблизно однаково?"
GUIDANCE = ("Оцінюйте зміст: які є блоки, їхні назви та члени (атрибути й методи), повідомлення та "
            "їхній текст, а також що з чим з'єднано і яким видом стрілки. Не зважайте на "
            "розташування, положення та колір.")


def comparison_id(comp) -> str:
    return f"{comp[0]}__{comp[1]}"


# --------------------------------------------------------------------------- #
# the pool
# --------------------------------------------------------------------------- #
def pair_scores(rows_a: dict, rows_b: dict, key: str) -> dict:
    """{"compiled": (a, b), "ef": (a, b), "rf": (a, b)} for one diagram."""
    ra, rb = rows_a[key], rows_b[key]
    out = {"compiled": (bool(ra["csr"]["compiled"]), bool(rb["csr"]["compiled"]))}
    for m, col in METRICS.items():
        out[m] = (ra[col]["f1"], rb[col]["f1"])
    return out


def direction(s: dict):
    """0 or 1, the side the metric prefers (Element F1 first); None when both metrics tie."""
    for m in ("ef", "rf"):
        a, b = s[m]
        if a != b:
            return 0 if a > b else 1
    return None


def stratum(s: dict) -> str:
    return "ef" if s["ef"][0] != s["ef"][1] else "rf"


def in_pool(s: dict) -> bool:
    return all(s["compiled"]) and direction(s) is not None


def comparison_pool(rows_a: dict, rows_b: dict, exclude=frozenset()) -> dict:
    out = {}
    for k in sorted(rows_a):
        if k in exclude:
            continue
        s = pair_scores(rows_a, rows_b, k)
        if in_pool(s):
            out[k] = s
    return out


# --------------------------------------------------------------------------- #
# the draw
# --------------------------------------------------------------------------- #
def split_types(n: int, avail: dict) -> dict:
    """How many class and sequence pairs a cell of n takes: as even as availability allows."""
    c = min(avail.get("class", 0), (n + 1) // 2)
    s = min(avail.get("sequence", 0), n - c)
    c = min(avail.get("class", 0), n - s)
    if c + s != n:
        raise ValueError(f"cell needs {n} pairs, has {avail}")
    return {"class": c, "sequence": s}


def direction_quota(pool: dict, n: int = PER_COMPARISON) -> dict:
    """{0: k, 1: n-k}: the side the pool prefers more often takes the larger half."""
    count = collections.Counter(direction(s) for s in pool.values())
    major = 0 if count[0] >= count[1] else 1
    return {major: (n + 1) // 2, 1 - major: n // 2}


def stratum_quota(n: int) -> dict:
    return {"ef": n // 2, "rf": n - n // 2}


def draw(pools: dict, meta: dict, seed: int = SEED) -> list[dict]:
    """pools: {comparison: {key: scores}}, in COMPARISONS order. Returns the pair records,
    sorted by pair id. A key drawn for one comparison is not drawn again."""
    pairs, used = [], set()
    for comp, pool in pools.items():
        pool = {k: s for k, s in pool.items() if k not in used}
        cid = comparison_id(comp)
        for d, n_d in sorted(direction_quota(pool).items()):
            for st, n_s in stratum_quota(n_d).items():
                cell = collections.defaultdict(list)
                for k, s in pool.items():
                    if direction(s) == d and stratum(s) == st:
                        cell[meta[k]["primary_type"]].append(k)
                take = split_types(n_s, {t: len(v) for t, v in cell.items()})
                for t in TYPES:
                    rng = random.Random(f"{seed}|rater-models|{cid}|{comp[d]}|{st}|{t}")
                    for k in rng.sample(sorted(cell[t]), take[t]):
                        s = pool[k]
                        used.add(k)
                        pairs.append({"comparison": cid, "models": list(comp), "key": k,
                                      "primary_type": t, "tier": meta[k]["tier"],
                                      "direction": comp[d], "stratum": st,
                                      "scores": {m: {comp[0]: s[m][0], comp[1]: s[m][1]}
                                                 for m in METRICS}})
    order = list(range(len(pairs)))
    random.Random(f"{seed}|rater-models|ids").shuffle(order)
    width = len(str(len(pairs)))
    for n, i in enumerate(order, 1):
        pairs[i]["pair"] = f"P{n:0{width}d}"
    pairs.sort(key=lambda p: p["pair"])
    ab = random.Random(f"{seed}|rater-models|ab")
    for p in pairs:
        first = ab.random() < 0.5
        p["A"], p["B"] = (p["models"][0], p["models"][1]) if first else (p["models"][1], p["models"][0])
    return pairs


def rater_order(pairs: list[dict], rater: str, seed: int = SEED) -> list[str]:
    ids = [p["pair"] for p in pairs]
    random.Random(f"{seed}|rater-models|order|{rater}").shuffle(ids)
    return ids


def sha256(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_keys(out: Path) -> dict:
    return json.load(open(out / "keys.json", encoding="utf-8"))


def read_exclude(path) -> set:
    """Diagram keys of an earlier rater round's keys file."""
    if not path:
        return set()
    return {p["key"] for p in json.load(open(path, encoding="utf-8"))["pairs"]}


def _panel(args) -> dict:
    """{model id: (run_dir, {key: row})} for the models of COMPARISONS."""
    want = {m for c in COMPARISONS for m in c}
    entries = [e for e in load_registry(args.registry) if e.id in want]
    models = load_panel(entries, Path(args.data_root))
    got = {md.entry.id: (md.entry.run_dir, {r["key"]: r for r in md.rows}) for md in models}
    if set(got) != want:
        raise SystemExit(f"models not loaded: {sorted(want - set(got))}")
    return got


def cmd_draw(args) -> None:
    out = Path(args.out)
    if (out / "keys.json").exists():
        raise SystemExit(f"{out / 'keys.json'} exists; the sample is drawn once")
    panel = _panel(args)
    exclude = read_exclude(args.exclude)
    meta = {k: {"primary_type": r["primary_type"], "tier": r["tier"]}
            for k, r in next(iter(panel.values()))[1].items()}
    pools = {c: comparison_pool(panel[c[0]][1], panel[c[1]][1], exclude) for c in COMPARISONS}
    pairs = draw(pools, meta)
    pool_counts = {comparison_id(c): {
        "pairs": len(p),
        "prefers": {c[d]: n for d, n in sorted(collections.Counter(direction(s) for s in p.values()).items())},
        "ef_differs": sum(stratum(s) == "ef" for s in p.values())} for c, p in pools.items()}
    out.mkdir(parents=True, exist_ok=True)
    keys = {"_doc": "The unblinded key of the rater-check sample. Raters never read this file.",
            "seed": SEED, "rater_check_sha256": sha256(__file__),
            "registry": str(args.registry), "per_comparison": PER_COMPARISON,
            "run_dirs": {m: panel[m][0] for m in sorted(panel)},
            "excluded_keys": sorted(exclude),
            "excluded_from": (sha256(args.exclude) if args.exclude else None),
            "pool": pool_counts, "n_pairs": len(pairs), "pairs": pairs}
    (out / "keys.json").write_text(json.dumps(keys, indent=1) + "\n", encoding="utf-8")
    print(f"drawn: {len(pairs)} pairs; key {out / 'keys.json'}")
    for cid, c in pool_counts.items():
        print(f"  pool {cid}: {c}")


# --------------------------------------------------------------------------- #
# pictures
# --------------------------------------------------------------------------- #
def source_name(run_dir: str, key: str) -> str:
    return f"{run_dir}__{key}.puml"


def write_sources(pairs, run_dirs: dict, data_root: Path, src: Path) -> list[str]:
    """Each sample answer's PlantUML block (the scorer's extract_puml) as <run>__<key>.puml."""
    src.mkdir(parents=True, exist_ok=True)
    names = []
    for p in pairs:
        for m in p["models"]:
            run = run_dirs[m]
            text = (data_root / "runs" / run / f"{p['key']}.puml").read_text(encoding="utf-8",
                                                                         errors="replace")
            name = source_name(run, p["key"])
            (src / name).write_text(extract_puml(text) + "\n", encoding="utf-8")
            names.append(name)
    return names


def render_check(names, rows: dict) -> dict:
    """Counts of render status over the sample answers. Any answer that is not one picture
    stops the build: the raters see one picture per answer."""
    status = collections.Counter(rows.get(n, {}).get("status", "missing") for n in names)
    check = {"answers": len(names), "ok": status["ok"], "multi_page": status["multi_page"],
             "other": {k: v for k, v in status.items() if k not in ("ok", "multi_page")}}
    if check["ok"] != len(names):
        raise SystemExit(f"sample answers that are not one picture: {check}")
    return check


def _load_render(path: Path):
    """render.py as the module ``render`` (registered in sys.modules, so its worker processes can
    pickle its functions)."""
    spec = importlib.util.spec_from_file_location("render", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    sys.modules["render"] = mod
    spec.loader.exec_module(mod)
    return mod


def cmd_render(args) -> None:
    R = _load_render(Path(args.render_py))
    out = Path(args.out)
    keys = load_keys(out)
    names = write_sources(keys["pairs"], keys["run_dirs"], Path(args.data_root), out / "render" / "src")
    R.render(names, out / "render" / "src", out / "render", threads=args.threads, heap_mb=args.heap_mb)
    rows = {r["key"]: r for r in R.read_manifest(out / "render" / "manifest.jsonl")}
    check = render_check(names, rows)
    (out / "render" / "check.json").write_text(json.dumps(check, indent=1) + "\n", encoding="utf-8")
    print(f"rendered {len(names)} answers: {check}")


# --------------------------------------------------------------------------- #
# rating sheets
# --------------------------------------------------------------------------- #
PAGE = """<!doctype html>
<html lang="uk"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Оцінювання діаграм</title>
<style>
:root { --bg:#fff; --fg:#1d1d1f; --muted:#666; --line:#d0d0d0; --accent:#1f5fbf; --sel:#e6eefc; }
@media (prefers-color-scheme: dark) { :root { --bg:#1b1b1d; --fg:#ececec; --muted:#a0a0a0;
  --line:#3a3a3d; --accent:#7aa7ff; --sel:#25324a; } }
body { margin:0; background:var(--bg); color:var(--fg); font:15px/1.45 system-ui, sans-serif; }
header, main, footer { max-width:1400px; margin:0 auto; padding:10px 16px; }
h1 { font-size:18px; margin:4px 0; } .muted { color:var(--muted); }
.q { font-weight:600; }
.pics { display:grid; grid-template-columns:repeat(3, minmax(0, 1fr)); gap:12px; align-items:start; }
body.stacked .pics { grid-template-columns:1fr; }
@media (max-width:700px) { .pics { grid-template-columns:1fr; } }
figure { margin:0; border:1px solid var(--line); border-radius:6px; padding:6px; background:#fff; }
figcaption { color:#333; font-weight:600; margin-bottom:4px; }
figure img { display:block; max-width:100%; margin:0 auto; cursor:zoom-in; }
.choices { display:flex; gap:10px; margin:10px 0; flex-wrap:wrap; }
button { font:inherit; padding:8px 16px; border:1px solid var(--line); border-radius:6px;
  background:var(--bg); color:var(--fg); cursor:pointer; }
button.on { background:var(--sel); border-color:var(--accent); font-weight:600; }
textarea { width:100%; box-sizing:border-box; min-height:44px; font:inherit; background:var(--bg);
  color:var(--fg); border:1px solid var(--line); border-radius:6px; padding:6px; }
nav { display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-top:8px; }
</style></head><body>
<header>
<h1>Оцінювання діаграм, оцінювач __RATER__</h1>
<p class="q">__QUESTION__</p>
<p class="muted">__GUIDANCE__ Натисніть на малюнок, щоб відкрити його в повному розмірі;
кнопка «Малюнки один під одним» показує їх на всю ширину. Клавіші: A, B, S (приблизно однаково),
стрілки — перехід між парами (працюють і в українській розкладці). Відповіді зберігаються в цьому
браузері, поки ви працюєте; наприкінці натисніть <b>Зберегти відповіді</b> й надішліть файл автору.</p>
</header>
<main>
<p><b id="pos"></b> <span class="muted" id="done"></span></p>
<div class="choices">
<button data-c="A">A ближче</button><button data-c="B">B ближче</button>
<button data-c="same">Приблизно однаково</button></div>
<textarea id="note" placeholder="Коментар (необов'язково)"></textarea>
<nav><button id="prev">Назад</button><button id="next">Далі</button>
<button id="save">Зберегти відповіді</button><button id="layout">Малюнки один під одним</button>
<span class="muted" id="msg"></span></nav>
<div class="pics" style="margin-top:12px">
<figure><figcaption>Оригінал</figcaption><img id="o" alt="оригінал"></figure>
<figure><figcaption>A</figcaption><img id="a" alt="малюнок A"></figure>
<figure><figcaption>B</figcaption><img id="b" alt="малюнок B"></figure>
</div>
</main>
<script>
const RATER = "__RATER__";
const IDS = __IDS__;
const STORE = "rating-models-" + RATER;
let ans = {}; try { ans = JSON.parse(localStorage.getItem(STORE) || "{}"); } catch (e) { ans = {}; }
let i = 0;
function keep() { try { localStorage.setItem(STORE, JSON.stringify(ans)); } catch (e) {} }
function show() {
  const id = IDS[i];
  for (const s of ["o", "a", "b"]) { const el = document.getElementById(s);
    el.src = "img/" + id + "_" + s + ".png"; el.onclick = () => window.open(el.src, "_blank"); }
  document.getElementById("pos").textContent = "Пара " + (i + 1) + " з " + IDS.length;
  const n = IDS.filter(x => ans[x] && ans[x].choice).length;
  document.getElementById("done").textContent = "(відповідей: " + n + ")";
  const a = ans[id] || {};
  document.querySelectorAll(".choices button").forEach(b => b.classList.toggle("on", b.dataset.c === a.choice));
  document.getElementById("note").value = a.comment || "";
}
function pick(c) { const id = IDS[i]; ans[id] = Object.assign(ans[id] || {}, {choice: c}); keep(); show(); }
function move(d) { i = Math.max(0, Math.min(IDS.length - 1, i + d)); show(); window.scrollTo(0, 0); }
document.querySelectorAll(".choices button").forEach(b => b.onclick = () => pick(b.dataset.c));
document.getElementById("note").oninput = e => { const id = IDS[i];
  ans[id] = Object.assign(ans[id] || {}, {comment: e.target.value}); keep(); };
function layout(stacked) { document.body.classList.toggle("stacked", stacked);
  document.getElementById("layout").textContent = stacked ? "Малюнки поруч" : "Малюнки один під одним";
  try { localStorage.setItem(STORE + "-stacked", stacked ? "1" : ""); } catch (e) {} }
let stacked = false; try { stacked = !!localStorage.getItem(STORE + "-stacked"); } catch (e) {}
layout(stacked);
document.getElementById("layout").onclick = () => layout(!document.body.classList.contains("stacked"));
document.getElementById("prev").onclick = () => move(-1);
document.getElementById("next").onclick = () => move(1);
document.addEventListener("keydown", e => { if (e.target.tagName === "TEXTAREA" || e.metaKey || e.ctrlKey || e.altKey) return;
  // e.code is the physical key, so A / B / S work in the Ukrainian layout too
  if (e.code === "KeyA") pick("A"); else if (e.code === "KeyB") pick("B"); else if (e.code === "KeyS") pick("same");
  else if (e.key === "ArrowRight") move(1); else if (e.key === "ArrowLeft") move(-1); });
function toCSV(ids, ans) {
  const q = s => '"' + String(s || "").replace(/"/g, '""') + '"';
  return ["pair,choice,comment"].concat(ids.map(x => [x, (ans[x] || {}).choice || "",
    q((ans[x] || {}).comment)].join(","))).join("\\n") + "\\n";
}
document.getElementById("save").onclick = () => {
  const missing = IDS.filter(x => !(ans[x] && ans[x].choice));
  const url = URL.createObjectURL(new Blob([toCSV(IDS, ans)], {type: "text/csv"}));
  const link = document.createElement("a"); link.href = url; link.download = RATER + ".csv"; link.click();
  document.getElementById("msg").textContent = missing.length ?
    "Збережено; пар без відповіді: " + missing.length + "." : "Збережено всі " + IDS.length + " відповідей.";
};
show();
</script></body></html>
"""


def sheet_html(rater: str, ids: list[str]) -> str:
    return (PAGE.replace("__RATER__", rater).replace("__IDS__", json.dumps(ids))
            .replace("__QUESTION__", QUESTION).replace("__GUIDANCE__", GUIDANCE))


def build_sheet(pairs, run_dirs: dict, rater: str, sheet_dir: Path, render_dir: Path,
                images: Path) -> None:
    """One rater's folder: index.html and img/<pair>_{o,a,b}.png. Nothing in it names a model,
    a run or a test key."""
    img = sheet_dir / "img"
    img.mkdir(parents=True, exist_ok=True)
    for p in pairs:
        shutil.copyfile(images / f"{p['key']}.png", img / f"{p['pair']}_o.png")
        for side in ("A", "B"):
            name = source_name(run_dirs[p[side]], p["key"])[:-5] + ".png"
            shutil.copyfile(render_dir / name, img / f"{p['pair']}_{side.lower()}.png")
    (sheet_dir / "index.html").write_text(sheet_html(rater, rater_order(pairs, rater)), encoding="utf-8")


def cmd_sheets(args) -> None:
    out, sheets = Path(args.out), Path(args.sheets)
    keys = load_keys(out)
    for rater in RATERS:
        d = sheets / rater
        if d.exists():
            shutil.rmtree(d)
        build_sheet(keys["pairs"], keys["run_dirs"], rater, d, out / "render" / "puml_images_1568",
                    Path(args.data_root) / "puml_images_1568")
        shutil.make_archive(str(sheets / f"rating_{rater}"), "zip", root_dir=sheets, base_dir=rater)
        print(f"sheet {rater}: {d / 'index.html'} and {sheets / f'rating_{rater}.zip'}")


# --------------------------------------------------------------------------- #
# the report
# --------------------------------------------------------------------------- #
def read_ratings(path, pairs) -> dict:
    """{pair: {"choice", "comment"}}; every sample pair answered once with A, B or same."""
    ids = {p["pair"] for p in pairs}
    out = {}
    with open(path, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            pid, choice = row["pair"].strip(), row["choice"].strip()
            if pid not in ids:
                raise ValueError(f"{path}: unknown pair {pid}")
            if pid in out:
                raise ValueError(f"{path}: pair {pid} twice")
            if choice not in CHOICES:
                raise ValueError(f"{path}: pair {pid} has choice {choice!r}")
            out[pid] = {"choice": choice, "comment": (row.get("comment") or "").strip()}
    missing = sorted(ids - set(out))
    if missing:
        raise ValueError(f"{path}: {len(missing)} pairs without an answer, e.g. {missing[:3]}")
    return out


def picked(pair: dict, choice: str) -> str:
    """The model a choice names, or "same"."""
    return "same" if choice == "same" else pair[choice]


def higher(pair: dict, metric: str):
    s = pair["scores"][metric]
    a, b = pair["models"]
    if s[a] == s[b]:
        return None
    return a if s[a] > s[b] else b


def wilson(k: int, n: int, z: float = Z95):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def kappa(a: list, b: list) -> dict:
    """Raw agreement and Cohen's kappa of two label lists."""
    n = len(a)
    if not n:
        return {"n": 0, "agree": 0, "raw": None, "kappa": None}
    agree = sum(x == y for x, y in zip(a, b))
    po = agree / n
    ca, cb = collections.Counter(a), collections.Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return {"n": n, "agree": agree, "raw": po, "kappa": (po - pe) / (1 - pe) if pe < 1 else None}


def agreement(pairs, ratings, prefer, select=None) -> dict:
    """On the pairs where ``prefer(pair)`` names a model (and ``select`` holds): A/B picks of that
    model, their share among A/B picks with a Wilson interval, and the count of "same"."""
    n_pairs = agree = against = same = 0
    for p in pairs:
        h = prefer(p)
        if h is None or (select and not select(p)):
            continue
        n_pairs += 1
        c = picked(p, ratings[p["pair"]]["choice"])
        if c == "same":
            same += 1
        elif c == h:
            agree += 1
        else:
            against += 1
    n = agree + against
    ci = wilson(agree, n)
    return {"pairs": n_pairs, "picks": n, "agree": agree, "against": against, "same": same,
            "share": agree / n if n else None, "ci95": list(ci) if ci else None}


def by_metric(metric: str):
    return lambda p: higher(p, metric)


def opposite(p: dict) -> bool:
    """Both metrics differ and prefer different models."""
    e, r = higher(p, "ef"), higher(p, "rf")
    return e is not None and r is not None and e != r


GAP_EDGES = (0.05, 0.15, 0.35)   # bins of the deciding metric's gap: [0, .05), [.05, .15), [.15, .35), [.35, 1]


def gap(p: dict) -> float:
    """The score gap that sets the pair's direction: Element F1 when it differs, else Relationship F1."""
    s = p["scores"]["ef" if p["stratum"] == "ef" else "rf"]
    return abs(s[p["models"][0]] - s[p["models"][1]])


def gap_bins(edges=GAP_EDGES) -> list[tuple]:
    lows = (0.0,) + tuple(edges)
    return [(lo, hi) for lo, hi in zip(lows, tuple(edges) + (None,))]


def in_bin(p: dict, lo: float, hi) -> bool:
    g = gap(p)
    return g >= lo and (hi is None or g < hi)


def by_gap(pairs, ratings) -> list[dict]:
    """Agreement with the pair's direction per gap bin, per rater and over both raters' picks."""
    rows = []
    for lo, hi in gap_bins():
        sel = lambda p, lo=lo, hi=hi: in_bin(p, lo, hi)
        per = {r: agreement(pairs, rt, lambda p: p["direction"], sel) for r, rt in ratings.items()}
        k = sum(a["agree"] for a in per.values())
        n = sum(a["picks"] for a in per.values())
        ci = wilson(k, n)
        rows.append({"lo": lo, "hi": hi, "pairs": sum(1 for p in pairs if sel(p)), "raters": per,
                     "pooled": {"agree": k, "picks": n, "share": k / n if n else None,
                                "ci95": list(ci) if ci else None}})
    return rows


def report(pairs, ratings) -> dict:
    comps = list(dict.fromkeys(p["comparison"] for p in sorted(pairs, key=lambda p: p["comparison"])))
    rep = {"n_pairs": len(pairs), "raters": sorted(ratings), "agreement": {}, "by_direction": {},
           "by_comparison": {}, "by_type": {}, "opposite": {}}
    for r, rt in ratings.items():
        rep["agreement"][r] = {m: agreement(pairs, rt, by_metric(m)) for m in METRICS}
        rep["by_direction"][r] = agreement(pairs, rt, lambda p: p["direction"])
        rep["by_comparison"][r] = {c: {m: agreement(pairs, rt, by_metric(m), lambda p, c=c: p["comparison"] == c)
                                       for m in METRICS} for c in comps}
        rep["by_type"][r] = {t: {m: agreement(pairs, rt, by_metric(m), lambda p, t=t: p["primary_type"] == t)
                                 for m in METRICS} for t in TYPES}
        rep["opposite"][r] = {m: agreement(pairs, rt, by_metric(m), opposite) for m in METRICS}
    rep["by_gap"] = by_gap(pairs, ratings)
    if len(ratings) == 2:
        a, b = (ratings[r] for r in sorted(ratings))
        rep["between_raters"] = kappa([a[p["pair"]]["choice"] for p in pairs],
                                      [b[p["pair"]]["choice"] for p in pairs])
    rep["both_against_direction"] = [
        {"pair": p["pair"], "comparison": p["comparison"], "key": p["key"],
         "primary_type": p["primary_type"], "direction": p["direction"], "scores": p["scores"],
         "comments": {r: ratings[r][p["pair"]]["comment"] for r in sorted(ratings)}}
        for p in pairs
        if len(ratings) == 2 and all(picked(p, ratings[r][p["pair"]]["choice"]) not in (p["direction"], "same")
                                     for r in ratings)]
    return rep


def read_differences(path, against) -> dict:
    """The author's lines, one per pair both raters chose against the metric: pair -> (differs, kind).
    Refuses a file whose pairs are not exactly the report's list, or a row without a description."""
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or set(rows[0]) != {"pair", "differs", "kind"}:
        raise SystemExit(f"{path}: expected columns pair, differs, kind")
    got = [r["pair"] for r in rows]
    want = [p["pair"] for p in against]
    if sorted(got) != sorted(want) or len(set(got)) != len(got):
        raise SystemExit(f"{path}: pairs {sorted(got)} are not the report's list {sorted(want)}")
    for r in rows:
        if not r["differs"].strip():
            raise SystemExit(f"{path}: {r['pair']} has no description")
    return {r["pair"]: (r["differs"].strip(), r["kind"].strip()) for r in rows}


def add_differences(rep: dict, diffs: dict) -> dict:
    for p in rep["both_against_direction"]:
        p["differs"], p["kind"] = diffs[p["pair"]]
    return rep


def _fmt(a: dict) -> str:
    if not a["picks"]:
        return f"– (pairs {a['pairs']}, same {a['same']})"
    lo, hi = a["ci95"]
    return (f"{a['agree']}/{a['picks']} = {a['share']:.3f} [{lo:.3f}, {hi:.3f}]; same {a['same']} "
            f"(pairs {a['pairs']})")


def _counts(a: dict) -> str:
    return f"{a['agree']} / {a['against']} / {a['same']}"


def report_md(rep: dict) -> str:
    L = ["# Human-rater check on model-against-model pairs: report", "",
         "All numbers descriptive. Agreement: of the pairs where the metric differs and the rater "
         "picked A or B, those where the pick is the answer the metric scores higher; Wilson 95% "
         "interval.", ""]
    L += ["## Agreement with the metric", "", "| Rater | Element F1 | Relationship F1 |", "|---|---|---|"]
    for r in rep["raters"]:
        a = rep["agreement"][r]
        L.append(f"| {r} | {_fmt(a['ef'])} | {_fmt(a['rf'])} |")
    L += ["", "## With the pair's direction", "",
          "The answer the metric prefers: Element F1 when it differs, otherwise Relationship F1.", "",
          "| Rater | Agreement |", "|---|---|"]
    for r in rep["raters"]:
        L.append(f"| {r} | {_fmt(rep['by_direction'][r])} |")
    L += ["", "## By the size of the score gap", "",
          "Agreement with the pair's direction, by the gap in the metric that sets it. The pooled "
          "column adds both raters' picks; a pair counts once per rater, so its interval is "
          "descriptive only.", "",
          "| Gap | Pairs | " + " | ".join(rep["raters"]) + " | Pooled picks |",
          "|---|---|" + "---|" * len(rep["raters"]) + "---|"]
    for b in rep["by_gap"]:
        rng = f"[{b['lo']:.2f}, {b['hi']:.2f})" if b["hi"] is not None else f"[{b['lo']:.2f}, 1.00]"
        po = b["pooled"]
        pooled = (f"{po['agree']}/{po['picks']} = {po['share']:.3f} [{po['ci95'][0]:.3f}, {po['ci95'][1]:.3f}]"
                  if po["picks"] else "–")
        L.append(f"| {rng} | {b['pairs']} | " + " | ".join(_fmt(b["raters"][r]) for r in rep["raters"])
                 + f" | {pooled} |")
    L += ["", "## Pairs where the two metrics prefer different answers", "",
          "| Rater | Element F1 | Relationship F1 |", "|---|---|---|"]
    for r in rep["raters"]:
        a = rep["opposite"][r]
        L.append(f"| {r} | {_fmt(a['ef'])} | {_fmt(a['rf'])} |")
    if "between_raters" in rep:
        k = rep["between_raters"]
        kap = "–" if k["kappa"] is None else f"{k['kappa']:.3f}"
        L += ["", "## Between the raters", "",
              f"Same answer on {k['agree']} of {k['n']} pairs ({k['raw']:.3f}); Cohen's kappa {kap} "
              "(A / B / about the same)."]
    L += ["", "## Counts by comparison and by type (agree / against / same)", "",
          "| Rater | Group | Element F1 | Relationship F1 |", "|---|---|---|---|"]
    for r in rep["raters"]:
        for c, a in rep["by_comparison"][r].items():
            L.append(f"| {r} | {c.replace('__', ' vs ')} | {_counts(a['ef'])} | {_counts(a['rf'])} |")
        for t, a in rep["by_type"][r].items():
            L.append(f"| {r} | {t} | {_counts(a['ef'])} | {_counts(a['rf'])} |")
    L += ["", "## Pairs where both raters chose against the metric", "",
          "| Pair | Comparison | Type | Metric prefers | What differs (written by the author) | Kind |",
          "|---|---|---|---|---|---|"]
    for p in rep["both_against_direction"]:
        L.append(f"| {p['pair']} | {p['comparison'].replace('__', ' vs ')} | {p['primary_type']} "
                 f"| {p['direction']} | {p.get('differs', '')} | {p.get('kind', '')} |")
    return "\n".join(L) + "\n"


def cmd_report(args) -> None:
    out = Path(args.out)
    pairs = load_keys(out)["pairs"]
    ratings = {}
    for r in RATERS:
        p = out / "ratings" / f"{r}.csv"
        if p.exists():
            ratings[r] = read_ratings(p, pairs)
    if not ratings:
        raise SystemExit(f"no ratings in {out / 'ratings'}")
    rep = report(pairs, ratings)
    if (out / DIFFERENCES).exists():
        add_differences(rep, read_differences(out / DIFFERENCES, rep["both_against_direction"]))
    rep["rater_check_sha256"] = sha256(__file__)
    (out / "report.json").write_text(json.dumps(rep, indent=1) + "\n", encoding="utf-8")
    (out / "report.md").write_text(report_md(rep), encoding="utf-8")
    print(f"report: {out / 'report.md'} (raters {sorted(ratings)})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("draw", "render", "sheets", "report"):
        sp = sub.add_parser(name)
        sp.add_argument("--out", default=str(OUT))
        if name in ("draw", "render", "sheets"):
            sp.add_argument("--data-root", default="data_paper")
        if name == "draw":
            sp.add_argument("--registry", default="analysis/model_registry_paper.json")
            sp.add_argument("--exclude", default=None,
                            help="keys.json of an earlier rater round; its diagrams are left out")
        if name == "sheets":
            sp.add_argument("--sheets", default=str(SHEETS))
        if name == "render":
            sp.add_argument("--render-py", default=str(ROOT.parent / "fine-tune" / "build" / "render.py"))
            sp.add_argument("--threads", type=int, default=3)
            sp.add_argument("--heap-mb", type=int, default=8192)
    args = ap.parse_args()
    {"draw": cmd_draw, "render": cmd_render, "sheets": cmd_sheets, "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    main()
