"""CLI: render the evaluation-framework overview diagram (manuscript figure).

A left-to-right schematic of the evaluation framework: ground-truth and predicted PlantUML
source pass through identical diagram-code isolation; the prediction is gated by the
renderer (CSR), both sides are turned into typed graphs by the shared
structural extractor, and the metric suite hangs off the pipeline at its three
levels (compilation / structure / surface). A non-rendering prediction drops to
an empty graph and scores zero, feeding the full-set population. No counts,
metrics results, or tool internals appear; wording mirrors
``methodology/evaluation-framework.md`` -- update there first, then mirror here.

Usage::

    python3 analysis/build_framework_figure.py                 # 1000-dpi PNG + vector PDF
    python3 analysis/build_framework_figure.py --dpi 120       # quick preview

Writes ``<out-dir>/<plots-subdir>/evaluation_framework.{png,pdf}``.
Deterministic: Agg backend + pinned save-metadata (via
``analysis.plots.save_figure``) makes a re-render byte-identical. Monochrome by
design so the figure survives grayscale print; the caption is supplied by the
publication (the figure bakes in no title).
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

INK, BORDER, MUTED = "#111111", "#333333", "#555555"
STAGE_FILL, CHIP_FILL = "#f2f2f2", "#e2e2e2"

SZ_TAG, SZ_NAME, SZ_SUB, SZ_TITLE, SZ_DETAIL, SZ_EDGE = 5.8, 8.0, 6.2, 7.5, 6.2, 6.2


def _box(ax, x0, y0, w, h, *, fill="white", lw=0.9, dashed=False):
    ax.add_patch(FancyBboxPatch(
        (x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.8",
        facecolor=fill, edgecolor=BORDER, linewidth=lw,
        linestyle=(0, (3.2, 2.2)) if dashed else "solid"))


def _arrow(ax, x0, y0, x1, y1, *, color=INK, lw=0.9, dashed=False):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", lw=lw, color=color,
                                shrinkA=0, shrinkB=0,
                                linestyle=(0, (3.2, 2.2)) if dashed else "solid"))


def _line(ax, pts, *, color=INK, lw=0.9, dashed=False):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round",
            linestyle=(0, (3.2, 2.2)) if dashed else "solid", zorder=1)


def _chip(ax, x0, y0, w, h, tag, name, sub):
    _box(ax, x0, y0, w, h, fill=CHIP_FILL, lw=1.1)
    cx = x0 + w / 2
    ax.text(cx, y0 + h - 1.6, tag, ha="center", va="center",
            fontsize=SZ_TAG, color=MUTED)
    ax.text(cx, y0 + h - 3.5, name, ha="center", va="center",
            fontsize=SZ_NAME, color=INK, fontweight="bold")
    ax.text(cx, y0 + 2.5, sub, ha="center", va="center",
            fontsize=SZ_SUB, color=INK, linespacing=1.25)


def build_figure():
    fig, ax = plt.subplots(figsize=(6.9, 3.73))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 54)
    ax.set_aspect("auto")
    ax.axis("off")

    y_gt, y_pr = 42.0, 22.0  # ground-truth / prediction track centerlines

    # --- Inputs -------------------------------------------------------------
    _box(ax, 1, y_gt - 4.5, 14.5, 9)
    ax.text(8.25, y_gt, "Ground-truth\nPlantUML source", ha="center",
            va="center", fontsize=SZ_DETAIL, color=INK, linespacing=1.3)
    _box(ax, 1, y_pr - 4.5, 14.5, 9)
    ax.text(8.25, y_pr, "Predicted\nPlantUML source\n(model output)", ha="center",
            va="center", fontsize=SZ_DETAIL, color=INK, linespacing=1.3)

    # --- Diagram code isolation (one shared stage; both tracks pass through) -
    _box(ax, 17.5, 13, 16, 35, fill=STAGE_FILL)
    ax.text(25.5, 43.0, "Diagram code\nisolation", ha="center", va="center",
            fontsize=SZ_TITLE, color=INK, fontweight="bold", linespacing=1.25)
    ax.text(25.5, 32.5, "the code between\n@startuml and\n@enduml is kept;\n"
            "everything around\nit is discarded", ha="center", va="center",
            fontsize=SZ_DETAIL, color=INK, linespacing=1.35)
    _arrow(ax, 15.5, y_gt, 17.5, y_gt)
    _arrow(ax, 15.5, y_pr, 17.5, y_pr)

    # --- Compile gate (prediction track only) --------------------------------
    _arrow(ax, 33.5, y_pr, 36.5, y_pr)
    _box(ax, 36.5, y_pr - 4.5, 13, 9)
    ax.text(43, y_pr, "PlantUML\nrenderer:\nnon-empty\nimage?", ha="center",
            va="center", fontsize=SZ_DETAIL, color=INK, linespacing=1.25)
    _arrow(ax, 49.5, y_pr, 54, y_pr)
    ax.text(51.7, y_pr + 1.4, "yes", ha="center", va="center",
            fontsize=SZ_EDGE, color=MUTED, style="italic")
    # CSR measures the gate outcome.
    _arrow(ax, 39.5, y_pr - 4.5, 39.5, 12.1, color=MUTED, lw=0.8)
    _chip(ax, 30, 2.8, 19, 9.3, "level 1 · compilation", "CSR",
          "fraction of predictions\nthat render")
    # Failed compile: empty graph, zero scores (kept, not dropped).
    _line(ax, [(51.5, 19.5), (52.6, 19.5), (52.6, 9), (54.5, 9)],
          color=MUTED, lw=0.8, dashed=True)
    _arrow(ax, 53.7, 9, 54.5, 9, color=MUTED, lw=0.8)
    ax.text(51.4, 15.0, "no", ha="center", va="center",
            fontsize=SZ_EDGE, color=MUTED, style="italic")
    _box(ax, 54.5, 4, 19, 10, dashed=True)
    ax.text(64, 9, "no image rendered:\nempty graph,\nstructural scores zero\n"
            "(kept in the full set)", ha="center",
            va="center", fontsize=SZ_EDGE, color=INK, linespacing=1.25)

    # --- Structural extraction (one shared stage) ----------------------------
    _arrow(ax, 33.5, y_gt, 54, y_gt)
    _box(ax, 54, 17, 15, 30, fill=STAGE_FILL)
    ax.text(61.5, 42.5, "Structural\nextraction", ha="center", va="center",
            fontsize=SZ_TITLE, color=INK, fontweight="bold", linespacing=1.25)
    ax.text(61.5, 37.7, "(PlantUML parser)", ha="center", va="center",
            fontsize=SZ_DETAIL, color=MUTED)
    ax.text(61.5, 27.5, "node:\ndisplay name\n+ UML type\n\nedge:\n"
            "(source, target,\nrelation type)", ha="center", va="center",
            fontsize=SZ_DETAIL, color=INK, linespacing=1.3)

    # --- Typed graphs -> metric chips ---------------------------------------
    _line(ax, [(69, y_gt), (71.5, y_gt)])
    _line(ax, [(69, y_pr), (71.5, y_pr)])
    _line(ax, [(71.5, y_pr), (71.5, 48.5)])  # bus joining the two graphs
    ax.text(71.75, 19.5, "typed\ngraphs", ha="center", va="center",
            fontsize=5.8, color=MUTED, style="italic", linespacing=1.2)
    _arrow(ax, 71.5, 48.5, 74, 48.5)
    _arrow(ax, 71.5, 26, 74, 26)

    _chip(ax, 74, 44, 22, 9, "level 2 · structure", "Element F1",
          "nodes, matched by\nnormalized display name")
    _chip(ax, 74, 32.75, 22, 9, "level 2 · structure",
          "Type accuracy", "UML type agreement\non name-matched pairs")
    _arrow(ax, 85, 44, 85, 41.75)
    _chip(ax, 74, 21.5, 22, 9, "level 2 · structure", "Relationship F1",
          "edges, matched by\n(source, target, type)")

    # --- Surface metric (bypasses the graph) ---------------------------------
    _line(ax, [(25.5, 13), (25.5, 1.5), (85, 1.5)], color=MUTED, lw=0.8)
    _arrow(ax, 85, 1.5, 85, 8.5, color=MUTED, lw=0.8)
    ax.text(77, 2.9, "source text", ha="center", va="center",
            fontsize=SZ_EDGE, color=MUTED, style="italic")
    _chip(ax, 74, 8.5, 22, 9, "level 3 · surface", "chrF++",
          "text similarity of\nthe full source")

    return fig


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="Render the evaluation-framework overview diagram (PNG + PDF).")
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--plots-subdir", default="plots")
    ap.add_argument("--name", default="evaluation_framework")
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
