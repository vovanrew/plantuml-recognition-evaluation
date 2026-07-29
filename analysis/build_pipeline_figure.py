"""CLI: render the test-set selection-pipeline flow diagram (manuscript figure).

A PRISMA-style flow: the main spine tracks the pool from the mined corpus down
to the 1,000-diagram benchmark test set; side boxes carry each exclusion step
with its counts. Every number is a frozen fact from
``methodology/test-set-construction.md`` (sections 3, 4, 8, 9, 10) -- update
there first, then mirror here. No metric or result appears in this figure.

Usage::

    python3 analysis/build_pipeline_figure.py                 # 1000-dpi PNG + vector PDF
    python3 analysis/build_pipeline_figure.py --dpi 120       # quick preview

Writes ``<out-dir>/<plots-subdir>/dataset_pipeline.{png,pdf}``. Deterministic:
Agg backend + pinned save-metadata (via ``analysis.plots.save_figure``) makes a
re-render byte-identical. Monochrome by design so the figure survives grayscale
print; the caption is supplied by the publication (the figure bakes in no title).
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow direct execution as well as module execution: add the package root.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib  # noqa: E402

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from analysis.plots import save_figure  # noqa: E402  (pinned-metadata writer)

DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "out"

# --------------------------------------------------------------------------- #
# Frozen pipeline facts (source of truth: methodology/test-set-construction.md)
# --------------------------------------------------------------------------- #

# Main spine, top to bottom: (text, n_lines is derived from the text).
SPINE = [
    "Published input dataset: 143,427 PlantUML diagrams\nmined from open-source repositories (World of Code)",
    "Candidate pool: 106,348 diagrams\n(class 71,323 / sequence 35,025)",
    "After degenerate-render exclusion: 105,118\n(class 70,477 / sequence 34,641)",
    "After normalized-code deduplication: 101,648\n(class 68,459 / sequence 33,189)",
    "Sampling pool after type-agreement filter: 101,211\n(class 68,331 / sequence 32,880)",
    "Benchmark test set: 1,000 diagrams\n"
    "2 diagram types × 4 complexity tiers × 125 per cell\n"
    "tiers by source-line quartiles within each type\n"
    "stratified random draw, fixed seed, ≤ 5 per repository",
]

# Side boxes: index of the spine gap they branch from (0 = between spine[0]
# and spine[1]) -> text. The final gap (sampling) has no exclusion branch.
SIDE = {
    0: "Excluded 37,079 by the inclusion criteria:\n"
       "other or hybrid type; failed structural\n"
       "extraction; truncated source;\n"
       "> 50 elements; repository unknown",
    1: "Excluded 1,230 degenerate renders:\n"
       "multi-page source (309);\n"
       "renderer-clipped image (595);\n"
       "extreme aspect ratio (326)",
    2: "Removed 3,470 near-duplicates by\n"
       "normalized-code hash\n(class 2,018 / sequence 1,452)",
    3: "Removed 437: dataset type label vs\n"
       "parser type disagreement\n(class 128 / sequence 309)",
}

# --------------------------------------------------------------------------- #
# Layout (canvas coordinates 0..100 x 0..100)
# --------------------------------------------------------------------------- #

SPINE_CX, SPINE_W = 30.0, 58.0        # spine box center x / width
SIDE_X0, SIDE_W = 61.5, 37.0          # side box left edge / width
TOP_Y, GAP_H = 97.0, 6.5              # top edge of first box / inter-box gap
LINE_H, BOX_PAD = 2.6, 2.6            # per-text-line height / vertical padding

INK, BORDER = "#111111", "#333333"
SIDE_FILL, FINAL_FILL = "#f5f5f5", "#e8e8e8"


def _box(ax, x0, y0, w, h, *, fill="white", lw=0.9):
    ax.add_patch(FancyBboxPatch(
        (x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.8",
        facecolor=fill, edgecolor=BORDER, linewidth=lw))


def _arrow(ax, x0, y0, x1, y1):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=0.9, color=INK,
                                shrinkA=0, shrinkB=0))


def build_figure():
    fig, ax = plt.subplots(figsize=(7.2, 8.4))
    ax.set_xlim(0, 100)
    ax.set_aspect("auto")
    ax.axis("off")

    # Lay the spine out top-down; remember each box's top/bottom edge.
    edges = []
    y_top = TOP_Y
    for i, text in enumerate(SPINE):
        n_lines = text.count("\n") + 1
        h = n_lines * LINE_H + BOX_PAD
        last = i == len(SPINE) - 1
        _box(ax, SPINE_CX - SPINE_W / 2, y_top - h, SPINE_W, h,
             fill=FINAL_FILL if last else "white", lw=1.6 if last else 0.9)
        ax.text(SPINE_CX, y_top - h / 2, text, ha="center", va="center",
                fontsize=8, color=INK, linespacing=1.35)
        edges.append((y_top, y_top - h))
        y_top -= h + GAP_H

    # Clamp the canvas to the content (no dead band under the final box).
    ax.set_ylim(edges[-1][1] - 1.5, TOP_Y + 1.5)

    # Spine arrows + side branches at each gap midpoint.
    for i in range(len(SPINE) - 1):
        gap_top, gap_bot = edges[i][1], edges[i + 1][0]
        _arrow(ax, SPINE_CX, gap_top, SPINE_CX, gap_bot)
        if i in SIDE:
            text = SIDE[i]
            n_lines = text.count("\n") + 1
            h = n_lines * (LINE_H * 0.88) + BOX_PAD * 0.8
            mid = (gap_top + gap_bot) / 2
            _arrow(ax, SPINE_CX, mid, SIDE_X0, mid)
            _box(ax, SIDE_X0, mid - h / 2, SIDE_W, h, fill=SIDE_FILL, lw=0.7)
            ax.text(SIDE_X0 + SIDE_W / 2, mid, text, ha="center", va="center",
                    fontsize=7, color=INK, linespacing=1.3)

    return fig


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Render the selection-pipeline flow diagram (PNG + PDF).")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--plots-subdir", default="plots")
    ap.add_argument("--name", default="dataset_pipeline")
    ap.add_argument("--dpi", type=int, default=1000,
                    help="PNG raster resolution (PDF is vector regardless)")
    args = ap.parse_args(argv)

    fig = build_figure()
    paths = save_figure(fig, args.out_dir / args.plots_subdir, args.name, dpi=args.dpi)
    for kind, path in paths.items():
        print(f"{kind}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
