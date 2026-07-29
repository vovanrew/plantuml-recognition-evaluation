"""Task-3 plots: the benchmark's figures, driven off the Task-1 master table and
the Task-2 CI table (read-only inputs -- never recompute a metric here).

Two-arms reporting philosophy (plan invariant): the Qwen open ladder is a scaling
*curve* (dense 2B/9B/27B on a log-parameter axis) and the frontier models are
*reference points* (a side-by-side comparison) -- never one ranked leaderboard.
The 397B-A17B MoE is a capability ceiling, NOT a 4th dense rung: it is plotted as
a distinct marker at its ~17B *active* parameters and annotated with both total
(397B) and active (~17B), never on the dense monotonic axis.

Error bars come from ``ci_table.json`` (paired bootstrap, 95%). Two facts shape
them: chrF++ **micro** is a corpus statistic with no CI (the headline chrF++ here
is **macro**), and the CI table covers OVERALL + per-relation only -- so the
per-tier / per-type breakdowns are **point estimates with no error bars** (stated
on the figure). All figures are incremental: render whatever is scored, annotate
"N/total", reserve pending positions without inventing values.

Determinism: the Agg backend plus pinned save-metadata (no embedded timestamp)
makes a re-render of unchanged data byte-identical in both PNG and PDF.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless + deterministic raster backend

import matplotlib.pyplot as plt  # noqa: E402  (must follow use())

from pathlib import Path  # noqa: E402

from analysis.aggregate import RELATIONS, TIERS, TYPES  # noqa: E402

__all__ = [
    "MODEL_COLORS", "assign_colors", "MODEL_MARKERS", "assign_markers",
    "dense_ladder", "moe_entries", "frontier_entries",
    "scaling_stat_id", "per_relation_stat_id",
    "cell_point", "per_relation_point", "ci_lookup", "yerr_about",
    "crowding_caption", "tier_crowding_label",
    "POP_LABEL", "pop_label",
    "save_figure", "render_all",
    "fig_scaling_curve", "fig_per_relation",
    "fig_breakdown_by_tier", "fig_breakdown_by_type", "fig_frontier_bars",
]

# --------------------------------------------------------------------------- #
# deterministic styling
# --------------------------------------------------------------------------- #

# Fixed per-model colors (lab-ish hues; the Qwen dense ladder is a blue ramp,
# the MoE ceiling a contrasting red). Unknown ids fall back to a fixed palette in
# call order, so colors are stable run-to-run.
MODEL_COLORS = {
    "gpt-5.2": "#1b9e77",            # OpenAI — green
    "claude-opus-4-6": "#d95f02",    # Anthropic — orange
    "claude-sonnet-4-6": "#e6a157",  # Anthropic mid-tier — light orange
    "gemini-3.1-pro": "#7570b3",     # Google — purple
    "qwen3.5-2b": "#9ecae1",         # Qwen dense ramp (light -> dark)
    "qwen3.5-9b": "#4292c6",
    "qwen3.5-27b": "#08519c",
    "qwen3.5-397b-a17b": "#e31a1c",  # MoE ceiling — red
}
QWEN_DENSE_COLOR = "#08519c"  # the dense-ladder line/markers (one series)
MOE_COLOR = "#e31a1c"
_FALLBACK = ["#66c2a5", "#fc8d62", "#8da0cb", "#e78ac3",
             "#a6d854", "#ffd92f", "#e5c494", "#b3b3b3"]


# Fixed per-model marker shapes. Colour alone does not separate seven line series
# (the frontier three overlap near the top and the Qwen ramp is one hue), and the
# journal requires figures to be clear and contrasting, which a greyscale print
# must also satisfy. Shape carries the identity when hue cannot.
MODEL_MARKERS = {
    "gpt-5.2": "o",
    "claude-opus-4-6": "s",
    "claude-sonnet-4-6": "p",
    "gemini-3.1-pro": "^",
    "qwen3.5-2b": "v",
    "qwen3.5-9b": "D",
    "qwen3.5-27b": "P",
    "qwen3.5-397b-a17b": "X",
}
_FALLBACK_MARKERS = ["o", "s", "^", "v", "D", "P", "X", "*"]


def assign_markers(ids: list[str]) -> dict[str, str]:
    """Deterministic id -> marker shape, mirroring ``assign_colors``."""
    out: dict[str, str] = {}
    fb = 0
    for mid in ids:
        if mid in MODEL_MARKERS:
            out[mid] = MODEL_MARKERS[mid]
        else:
            out[mid] = _FALLBACK_MARKERS[fb % len(_FALLBACK_MARKERS)]
            fb += 1
    return out


def assign_colors(ids: list[str]) -> dict[str, str]:
    """Deterministic id -> color. Known ids use the fixed map; unknown ids draw
    from a fixed fallback palette in call order (distinct + stable)."""
    out: dict[str, str] = {}
    fb = 0
    for mid in ids:
        if mid in MODEL_COLORS:
            out[mid] = MODEL_COLORS[mid]
        else:
            out[mid] = _FALLBACK[fb % len(_FALLBACK)]
            fb += 1
    return out


# --------------------------------------------------------------------------- #
# arm / axis splitting (the two-arms philosophy in code)
# --------------------------------------------------------------------------- #

def dense_ladder(entries):
    """Qwen DENSE rungs with disclosed params, ascending by total params.
    The MoE is excluded by construction -- it never enters the dense axis."""
    xs = [e for e in entries
          if e.arm == "qwen" and e.family == "dense" and e.params_total_b is not None]
    return sorted(xs, key=lambda e: e.params_total_b)


def moe_entries(entries):
    """Qwen MoE ceiling(s) -- plotted separately from the dense ladder."""
    return [e for e in entries if e.arm == "qwen" and e.family == "moe"]


def frontier_entries(entries):
    """Frontier reference points (one flagship per lab); Sonnet supplementary excluded."""
    return [e for e in entries if e.arm == "frontier" and not e.supplementary]


# --------------------------------------------------------------------------- #
# stat-id join: master metric naming  <->  CI-table stat ids
# --------------------------------------------------------------------------- #

def scaling_stat_id(metric: str, level: str = "micro",
                    population: str = "zeros_for_failed") -> str:
    """The ci_table stat id for an overall metric. CSR and type-accuracy have
    fixed ids (no level/population dimension on the bootstrap side)."""
    if metric == "csr":
        return "csr|csr"
    if metric == "type_accuracy":
        return "type_accuracy|accuracy|compiled_only"
    return f"{metric}|{level}|{population}"


def per_relation_stat_id(rel: str, population: str) -> str:
    return f"relationship_f1::{rel}|micro|{population}"


# --------------------------------------------------------------------------- #
# point extraction from the master table (never recomputed here)
# --------------------------------------------------------------------------- #

def _master_cell(block: dict, scope):
    """scope: ``"overall"`` | ``("type", "class")`` | ``("tier", 3)`` -> cell|None."""
    if scope == "overall":
        return block.get("overall")
    kind, val = scope
    if kind == "type":
        return block.get("by_type", {}).get(val)
    if kind == "tier":
        return block.get("by_tier", {}).get(str(val))
    raise ValueError(f"unknown scope {scope!r}")


def cell_point(master: dict, mid: str, scope, metric: str,
               level: str = "micro", population: str = "zeros_for_failed"):
    """A single point estimate from a master cell, or ``None`` if the model is
    not scored / the cell (e.g. an absent tier) is missing. Never raises on a
    pending model -- incrementality depends on it."""
    block = master.get("models", {}).get(mid)
    if block is None:
        return None
    cell = _master_cell(block, scope)
    if cell is None:
        return None
    if metric == "csr":
        return cell["csr"]["csr"]
    if metric == "type_accuracy":
        return cell["type_accuracy"]["accuracy"]
    if metric == "chrf":
        return cell["chrf"][population][level]  # micro is None in sub-cells
    return cell[metric][population][level]["f1"]  # element_f1 / relationship_f1


def per_relation_point(master: dict, mid: str, rel: str, population: str):
    """Per-relation F1 read-through from ``per_relation`` (None when absent)."""
    block = master.get("models", {}).get(mid)
    if block is None:
        return None
    rec = block.get("per_relation", {}).get(population, {}).get(rel)
    return rec.get("f1") if rec else None


def _rel_support(master: dict, rel: str, population: str):
    """GT support for a relation (model-independent under zeros_for_failed)."""
    for block in master.get("models", {}).values():
        rec = block.get("per_relation", {}).get(population, {}).get(rel)
        if rec and rec.get("support_gt") is not None:
            return rec["support_gt"]
    return None


# --------------------------------------------------------------------------- #
# error bars from the CI table
# --------------------------------------------------------------------------- #

def ci_lookup(ci: dict, mid: str, stat_id: str):
    """The {point, ci_low, ci_high, n_valid} entry, or ``None`` if absent."""
    return ci.get("per_model", {}).get(mid, {}).get(stat_id)


def yerr_about(point, ci_entry):
    """Asymmetric error-bar arms ``(point-low, high-point)`` about ``point``,
    clamped to >= 0 (a plotted point outside its CI never yields a negative arm).
    ``None`` when there is no CI (point-only statistic) or no point."""
    if ci_entry is None or point is None:
        return None
    lo, hi = ci_entry.get("ci_low"), ci_entry.get("ci_high")
    if lo is None or hi is None:
        return None
    return (max(0.0, point - lo), max(0.0, hi - point))


# --------------------------------------------------------------------------- #
# crowding descriptor (Task-5 -> Task-3 hook)
# --------------------------------------------------------------------------- #
# The per-tier image-crowding descriptor is content_lines per megapixel after the
# 1568px resize (``crowding.json``'s ``lines_per_mp_by_tier``, string tier keys).
# It rises monotonically with tier (denser images at higher complexity) and is the
# legibility context for the per-tier degradation curve.

def crowding_caption(crowding) -> str:
    """Compact one-line per-tier crowding descriptor for a figure footer, or ``""``
    when ``crowding`` is None/empty. Tiers are emitted in numeric order."""
    if not crowding:
        return ""
    parts = [f"T{t} {float(crowding[t]):.1f}" for t in sorted(crowding, key=int)]
    return ("Image crowding (content_lines/MP after 1568px resize): "
            + ", ".join(parts) + ".")


def tier_crowding_label(crowding, tier) -> str:
    """The crowding value for one tier as a short string (1 dp), or ``""`` when the
    descriptor is absent. Used as a secondary x-tick line on the per-tier figure."""
    if not crowding:
        return ""
    v = crowding.get(str(tier))
    return "" if v is None else f"{float(v):.1f}"


# --------------------------------------------------------------------------- #
# shared figure scaffolding
# --------------------------------------------------------------------------- #

# The four headline metrics carried across the multi-panel figures.
_HEADLINE = [
    ("csr", "micro", "CSR", (0.0, 1.0)),
    ("element_f1", "micro", "Element F1 (micro)", (0.0, 1.0)),
    ("relationship_f1", "micro", "Relationship F1 (micro)", (0.0, 1.0)),
    ("chrf", "macro", "chrF++ (macro)", (0.0, 100.0)),
]


# Reader-facing names for the two reporting populations. The artifact keys stay
# ``zeros_for_failed`` / ``compiled_only`` everywhere in the data; figure text uses
# the manuscript's terms, so a figure and the paper never disagree on a name.
POP_LABEL = {"zeros_for_failed": "full-set", "compiled_only": "compiled-only"}


def pop_label(population: str) -> str:
    """Manuscript term for a population key; unknown keys pass through unchanged."""
    return POP_LABEL.get(population, population)


def _scored_in_order(entries, master):
    """Inventory entries that are scored (present in master), preserving order."""
    return [e for e in entries if e.id in master.get("models", {})]


def _panel_note(master: dict) -> str:
    m = master["meta"]
    note = f"Models included: {m['models_included']}/{m['models_total']}"
    pend = m.get("pending_ids", [])
    if pend:
        note += "   (pending: " + ", ".join(pend) + ")"
    return note


def _bf(v) -> str:
    """Format a billions-of-params tick label: ``2`` -> ``2B``."""
    return f"{int(v)}B" if float(v).is_integer() else f"{v:g}B"


def _add_footer(fig, master: dict, extra: str | None = None, *, y: float = 0.004):
    """Centered italic caption: the N/total + pending annotation, plus any
    figure-specific note. ``y < 0`` hangs it BELOW an outside-lower legend (saved
    via bbox_inches="tight"); ``y >= 0`` sits it at the bottom of an axes-legend
    figure."""
    txt = _panel_note(master)
    if extra:
        txt += "    " + extra
    fig.text(0.5, y, txt, ha="center", va=("top" if y < 0 else "bottom"),
             fontsize=6.5, style="italic", color="#444444")


def _finish_multipanel(fig, axes, master: dict, *, handle_axis: int = 0,
                       extra: str | None = None, footer: bool = True,
                       top: float = 0.91, hspace: float = 0.45,
                       label_order: list[str] | None = None):
    """Manual bottom strip for a 2x2 panel figure: reserve margins, then stack a
    centered legend above a centered footer, both clear of the panels' x-labels.
    Manual margins (not constrained_layout) keep the figure-level text from
    fighting the legend/suptitle, and stay byte-deterministic. ``footer=False``
    omits the run-provenance strip (figures published in the manuscript carry that
    information in the surrounding text, not on the figure)."""
    fig.subplots_adjust(left=0.08, right=0.97, top=top, bottom=0.17,
                        hspace=hspace, wspace=0.22)
    handles, labels = axes.flat[handle_axis].get_legend_handles_labels()
    if handles and label_order:
        # matplotlib returns plain lines before error-bar containers, which is not
        # the order a reader needs; ``label_order`` pins it (unlisted labels last).
        rank = {lab: i for i, lab in enumerate(label_order)}
        pairs = sorted(zip(labels, handles),
                       key=lambda p: rank.get(p[0], len(rank)))
        labels = [p[0] for p in pairs]
        handles = [p[1] for p in pairs]
    if handles:
        fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8,
                   bbox_to_anchor=(0.5, 0.065))
    if footer:
        _add_footer(fig, master, extra, y=0.02)


# --------------------------------------------------------------------------- #
# Figure 1 — open-ladder scaling curve
# --------------------------------------------------------------------------- #

def fig_scaling_curve(entries, master, ci):
    """Qwen dense ladder (2B/9B/27B) on a log-parameter x-axis, four headline
    panels, with bootstrap error bars. The MoE ceiling is a separate marker at
    its ~17B active params (annotated 397B total / 17B active); pending rungs are
    reserved with a dotted guide, never a faked value.

    This figure is published in the manuscript, so it carries no in-image title,
    no run-provenance footer, and no per-tier crowding descriptor: the caption and
    the surrounding text carry those, and the crowding numbers belong to the
    per-tier figure and the difficulty-structure section.
    """
    ladder = dense_ladder(entries)
    moes = moe_entries(entries)

    fig, axes = plt.subplots(2, 2, figsize=(9, 8.4))

    # x positions for ticks: every disclosed rung (scored or pending) + MoE active.
    dense_x = [e.params_total_b for e in ladder]
    moe_x = [e.params_active_b for e in moes]
    all_x = sorted(set(dense_x + moe_x))

    for ax, (metric, level, title, ylim) in zip(axes.flat, _HEADLINE):
        # dense ladder, zeros_for_failed headline (error bars) ----------------
        xs, ys, elo, ehi = [], [], [], []
        for e in ladder:
            y = cell_point(master, e.id, "overall", metric, level, "zeros_for_failed")
            if y is None:
                continue
            ye = yerr_about(y, ci_lookup(ci, e.id, scaling_stat_id(metric, level,
                                                                   "zeros_for_failed")))
            xs.append(e.params_total_b)
            ys.append(y)
            elo.append(ye[0] if ye else 0.0)
            ehi.append(ye[1] if ye else 0.0)
        if xs:
            ax.errorbar(xs, ys, yerr=[elo, ehi], marker="o", ms=6, lw=1.6,
                        color=QWEN_DENSE_COLOR, capsize=3, elinewidth=1.0,
                        label=f"Qwen dense ({pop_label('zeros_for_failed')})")
        # compiled_only overlay (no error bars; CSR is population-independent) --
        if metric != "csr":
            cx, cy = [], []
            for e in ladder:
                y = cell_point(master, e.id, "overall", metric, level, "compiled_only")
                if y is not None:
                    cx.append(e.params_total_b)
                    cy.append(y)
            if cx:
                ax.plot(cx, cy, marker="s", ms=5, mfc="none", ls="--", lw=1.1,
                        color=QWEN_DENSE_COLOR, alpha=0.7,
                        label=pop_label("compiled_only"))

        # MoE ceiling — separate marker at active params, dual-param annotation -
        for e in moes:
            y = cell_point(master, e.id, "overall", metric, level, "zeros_for_failed")
            if y is not None:
                ye = yerr_about(y, ci_lookup(ci, e.id, scaling_stat_id(
                    metric, level, "zeros_for_failed")))
                ax.errorbar([e.params_active_b], [y],
                            yerr=([[ye[0]], [ye[1]]] if ye else None),
                            marker="D", ms=8, color=MOE_COLOR, capsize=3,
                            label=f"{e.display} (active)")
                ax.annotate(f"{_bf(e.params_total_b)} total /\n{_bf(e.params_active_b)} active",
                            (e.params_active_b, y), textcoords="offset points",
                            xytext=(6, -2), fontsize=6.5, color=MOE_COLOR)
            else:
                ax.axvline(e.params_active_b, color=MOE_COLOR, ls=":", lw=1.0, alpha=0.45)
        # reserve pending dense rungs with a faint guide -----------------------
        for e in ladder:
            if cell_point(master, e.id, "overall", "csr") is None:
                ax.axvline(e.params_total_b, color=QWEN_DENSE_COLOR, ls=":", lw=1.0, alpha=0.3)

        ax.set_xscale("log")
        if all_x:
            ax.set_xticks(all_x)
            ax.set_xticklabels([_bf(v) for v in all_x])
        ax.minorticks_off()
        ax.set_title(title, fontsize=10)
        ax.set_ylim(*ylim)
        ax.set_xlabel("Parameters (log scale)", fontsize=8)
        ax.grid(True, which="major", axis="y", alpha=0.25)

    order = [f"Qwen dense ({pop_label('zeros_for_failed')})", pop_label("compiled_only")]
    _finish_multipanel(fig, axes, master, handle_axis=1, footer=False, top=0.96,
                       hspace=0.32, label_order=order)
    return fig


# --------------------------------------------------------------------------- #
# Figure 2 — per-relation F1 grouped bars
# --------------------------------------------------------------------------- #

def fig_per_relation(entries, master, ci, *, population="zeros_for_failed"):
    """Grouped bars: relationship F1 (micro) per relation type × scored model,
    with per-relation bootstrap CIs as error bars. ``population`` selects the
    reporting population (the headline figure uses zeros_for_failed; the other is
    rendered separately).

    This figure is published in the manuscript, so it carries no in-image title
    and no run-provenance footer: the caption and the surrounding text carry
    those. The GT support stays in the tick labels (it is data, not provenance).
    """
    scored = _scored_in_order(entries, master)
    colors = assign_colors([e.id for e in scored])
    rels = RELATIONS
    n = max(len(scored), 1)
    width = 0.8 / n
    x = list(range(len(rels)))

    fig, ax = plt.subplots(figsize=(9, 5.4))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.98, bottom=0.22)
    for i, e in enumerate(scored):
        heights, elo, ehi = [], [], []
        for rel in rels:
            h = per_relation_point(master, e.id, rel, population)
            hv = h if h is not None else 0.0
            ye = yerr_about(hv, ci_lookup(ci, e.id, per_relation_stat_id(rel, population)))
            heights.append(hv)
            elo.append(ye[0] if ye else 0.0)
            ehi.append(ye[1] if ye else 0.0)
        offs = [xx + (i - (n - 1) / 2) * width for xx in x]
        ax.bar(offs, heights, width, color=colors[e.id], label=e.display,
               yerr=[elo, ehi], capsize=2, error_kw={"elinewidth": 0.8})

    # x labels, annotating model-independent GT support under zeros_for_failed.
    labels = []
    for rel in rels:
        if population == "zeros_for_failed":
            sup = _rel_support(master, rel, population)
            labels.append(f"{rel}\n(n={sup})" if sup is not None else rel)
        else:
            labels.append(rel)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel(f"Relationship F1 (micro), {pop_label(population)}")
    ax.grid(True, axis="y", alpha=0.25)
    if scored:
        # Legend below the axes, not inside them: the tallest error bars reach
        # ~0.95 and an in-axes legend collides with them. Bottom placement also
        # matches the multipanel figures, so the published figures agree.
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc="lower center", ncol=4, fontsize=8,
                   bbox_to_anchor=(0.5, 0.01))
    return fig


# --------------------------------------------------------------------------- #
# Figure 3a — per-tier breakdown (point estimates; no CIs)
# --------------------------------------------------------------------------- #

def fig_breakdown_by_tier(entries, master, *, population="zeros_for_failed", crowding=None):
    """Headline metrics across the 4 complexity tiers, one line per scored model.
    **Point estimates only** — the CI table bootstraps overall + per-relation, not
    per-tier cells, so the panels carry no error bars; the manuscript states that
    in the text.

    This figure is published in the manuscript, so it carries no in-image title
    and no run-provenance footer. ``crowding`` is the per-tier content-lines/MP
    image-crowding descriptor; when supplied, each tier tick gains a secondary
    line with its crowding value. ``render_all`` leaves it off: the published
    figure keeps one label line per tick and the descriptor is reported in the
    text instead.
    """
    scored = _scored_in_order(entries, master)
    colors = assign_colors([e.id for e in scored])
    markers = assign_markers([e.id for e in scored])

    # Tier tick labels gain a secondary crowding line when the descriptor is given.
    if crowding:
        xlabels = [f"{t}\n({tier_crowding_label(crowding, t)})" for t in TIERS]
        xlab = "Complexity tier (source-line quartile; lower line = lines per megapixel)"
    else:
        xlabels = [str(t) for t in TIERS]
        xlab = "Complexity tier (source-line quartile)"

    fig, axes = plt.subplots(2, 2, figsize=(9, 8.4))
    for idx, (ax, (metric, level, title, ylim)) in enumerate(zip(axes.flat, _HEADLINE)):
        for e in scored:
            xs, ys = [], []
            for t in TIERS:
                y = cell_point(master, e.id, ("tier", t), metric, level, population)
                if y is not None:
                    xs.append(t)
                    ys.append(y)
            if xs:
                ax.plot(xs, ys, marker=markers[e.id], ms=5, lw=1.5,
                        color=colors[e.id], label=e.display)
        ax.set_xticks(TIERS)
        ax.set_xticklabels(xlabels, fontsize=8)
        # The axis reading is the same in all four panels, so only the bottom row
        # is labelled; repeating it four times is clutter on a 2x2 grid.
        if idx >= 2:
            ax.set_xlabel(xlab, fontsize=8)
        # CSR has a single value in both populations; the other three do not, so
        # they name the one plotted (same terms the manuscript uses).
        ax.set_title(title if metric == "csr" else f"{title}, {pop_label(population)}",
                     fontsize=10)
        ax.set_ylim(*ylim)
        ax.grid(True, axis="y", alpha=0.25)

    _finish_multipanel(fig, axes, master, handle_axis=0, footer=False, top=0.96,
                       hspace=0.24)
    return fig


# --------------------------------------------------------------------------- #
# Figure 3b — per-type breakdown (point estimates; no CIs)
# --------------------------------------------------------------------------- #

def fig_breakdown_by_type(entries, master, *, population="zeros_for_failed"):
    """Headline metrics for the two diagram types (class / sequence), grouped bars
    per scored model. **Point estimates only** (per-type cells are not bootstrapped)."""
    scored = _scored_in_order(entries, master)
    colors = assign_colors([e.id for e in scored])
    n = max(len(scored), 1)
    width = 0.8 / n
    x = list(range(len(TYPES)))

    fig, axes = plt.subplots(2, 2, figsize=(9, 8.4))
    fig.suptitle(f"Per-type breakdown — {pop_label(population)} (point estimates)",
                 fontsize=12)
    for ax, (metric, level, title, ylim) in zip(axes.flat, _HEADLINE):
        for i, e in enumerate(scored):
            heights = []
            for t in TYPES:
                y = cell_point(master, e.id, ("type", t), metric, level, population)
                heights.append(y if y is not None else 0.0)
            offs = [xx + (i - (n - 1) / 2) * width for xx in x]
            ax.bar(offs, heights, width, color=colors[e.id], label=e.display)
        ax.set_xticks(x)
        ax.set_xticklabels(TYPES, fontsize=9)
        ax.set_title(title, fontsize=10)
        ax.set_ylim(*ylim)
        ax.grid(True, axis="y", alpha=0.25)

    _finish_multipanel(fig, axes, master, handle_axis=0,
                       extra="No error bars: per-type CIs not bootstrapped "
                             "(Task 2 = overall + per-relation).")
    return fig


# --------------------------------------------------------------------------- #
# Figure 4 — frontier comparison bars
# --------------------------------------------------------------------------- #

# Metrics on the frontier comparison: chrF++ is rescaled to /100 so it shares the
# 0–1 axis with CSR / F1 / type-accuracy (labelled and noted).
_FRONTIER_METRICS = [
    ("csr", "micro", "CSR", 1.0),
    ("element_f1", "micro", "Element F1\n(micro)", 1.0),
    ("relationship_f1", "micro", "Rel F1\n(micro)", 1.0),
    ("chrf", "macro", "chrF++\n(macro÷100)", 100.0),
    ("type_accuracy", "accuracy", "Type acc", 1.0),
]


def fig_frontier_bars(entries, master, ci, *, population="zeros_for_failed"):
    """Frontier reference points (GPT-5.2, Claude Opus 4.6, Gemini 3.1 Pro) side
    by side on the headline metrics, with bootstrap error bars. Pending frontier
    models are skipped and annotated. Type-accuracy is intrinsically compiled-only."""
    frontier = frontier_entries(entries)
    scored = [e for e in frontier if e.id in master.get("models", {})]
    pending = [e for e in frontier if e.id not in master.get("models", {})]
    colors = assign_colors([e.id for e in scored])
    n = max(len(scored), 1)
    width = 0.8 / n
    x = list(range(len(_FRONTIER_METRICS)))

    fig, ax = plt.subplots(figsize=(10, 5.6))
    fig.subplots_adjust(left=0.08, right=0.98, top=0.92, bottom=0.18)
    for i, e in enumerate(scored):
        heights, elo, ehi = [], [], []
        for metric, level, _lbl, scale in _FRONTIER_METRICS:
            pop = "compiled_only" if metric == "type_accuracy" else population
            h = cell_point(master, e.id, "overall", metric, level, pop)
            hv = (h if h is not None else 0.0) / scale
            ye = yerr_about(h, ci_lookup(ci, e.id, scaling_stat_id(metric, level, pop)))
            heights.append(hv)
            elo.append((ye[0] / scale) if ye else 0.0)
            ehi.append((ye[1] / scale) if ye else 0.0)
        offs = [xx + (i - (n - 1) / 2) * width for xx in x]
        ax.bar(offs, heights, width, color=colors[e.id], label=e.display,
               yerr=[elo, ehi], capsize=3, error_kw={"elinewidth": 0.9})

    ax.set_xticks(x)
    ax.set_xticklabels([lbl for _, _, lbl, _ in _FRONTIER_METRICS], fontsize=8)
    ax.set_ylim(0.0, 1.0)
    ax.set_ylabel("Score (chrF++ ÷100; type acc is compiled-only)")
    ax.set_title(f"Frontier reference points — {pop_label(population)}")
    ax.grid(True, axis="y", alpha=0.25)
    if scored:
        ax.legend(fontsize=8, ncol=min(len(scored), 3))
    extra = ("Pending frontier: " + ", ".join(e.display for e in pending)) if pending else None
    _add_footer(fig, master, extra, y=0.03)
    return fig


# --------------------------------------------------------------------------- #
# saving (deterministic) + orchestration
# --------------------------------------------------------------------------- #

# Pin metadata that would otherwise embed a timestamp / version, so re-renders of
# unchanged data are byte-identical (verified empirically for PNG and PDF).
_PNG_METADATA = {"Software": None}
_PDF_METADATA = {"CreationDate": None, "Producer": None, "Creator": None}


def save_figure(fig, out_dir, name: str, *, dpi: int = 150, close: bool = True) -> dict:
    """Write ``{name}.png`` and ``{name}.pdf`` under ``out_dir`` with pinned
    (timestamp-free) metadata; return ``{"png": Path, "pdf": Path}``."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / f"{name}.png"
    pdf = out_dir / f"{name}.pdf"
    # bbox_inches="tight" captures outside-axes artists (the lower legend + the
    # footer below it); verified byte-deterministic for both formats.
    fig.savefig(png, format="png", dpi=dpi, bbox_inches="tight", metadata=_PNG_METADATA)
    fig.savefig(pdf, format="pdf", bbox_inches="tight", metadata=_PDF_METADATA)
    if close:
        plt.close(fig)
    return {"png": png, "pdf": pdf}


def render_all(entries, master, ci, out_dir, *, crowding=None) -> dict:
    """Render the full Task-3 inventory into ``out_dir``; return {name: paths}.
    Both reporting populations are emitted where they matter (per-relation,
    frontier); the scaling curve overlays them in one figure. ``crowding`` is the
    per-tier content-lines/MP descriptor; it is accepted for callers that still
    pass it, but no rendered figure is annotated with it any more (both published
    figures carry that context in the manuscript text)."""
    out: dict[str, dict] = {}
    out["scaling_curve"] = save_figure(
        fig_scaling_curve(entries, master, ci),
        out_dir, "scaling_curve")
    for pop, suf in (("zeros_for_failed", "zeros"), ("compiled_only", "compiled")):
        out[f"per_relation_{suf}"] = save_figure(
            fig_per_relation(entries, master, ci, population=pop),
            out_dir, f"per_relation_f1_{suf}")
    out["breakdown_by_tier"] = save_figure(
        fig_breakdown_by_tier(entries, master),
        out_dir, "breakdown_by_tier")
    out["breakdown_by_type"] = save_figure(
        fig_breakdown_by_type(entries, master), out_dir, "breakdown_by_type")
    for pop, suf in (("zeros_for_failed", "zeros"), ("compiled_only", "compiled")):
        out[f"frontier_{suf}"] = save_figure(
            fig_frontier_bars(entries, master, ci, population=pop),
            out_dir, f"frontier_bars_{suf}")
    return out
