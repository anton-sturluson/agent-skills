#!/usr/bin/env python3
"""Plot ETF category mix, concentration, and optional pair-miss heatmaps."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

META = {
    "fund",
    "direct_theme_ex_adjacent",
    "direct_theme_ex_adjacent_pct",
    "operating_weight_covered_pct",
    "excluded_weight_pct",
    "top10_concentration",
    "top10_concentration_pct",
    "holdings_count",
    "operating_holdings_count",
    "as_of_date",
    "raw_total_weight_pct",
}

DEFAULT_COLORS = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#E45756", "#72B7B2", "#EECA3B", "#B0B0B0"]


def read_summary(path: Path) -> tuple[list[str], list[str], dict[str, dict[str, float]], dict[str, float]]:
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames or []
        categories = [c for c in fields if c not in META]
        funds: list[str] = []
        data: dict[str, dict[str, float]] = {}
        top10: dict[str, float] = {}
        for row in reader:
            fund = row["fund"]
            funds.append(fund)
            data[fund] = {c: float(row.get(c) or 0) for c in categories}
            top10[fund] = float(row.get("top10_concentration_pct") or row.get("top10_concentration") or 0)
    return funds, categories, data, top10


def save_jpg_from_png(png_path: Path, max_size=(1800, 1400)) -> None:
    try:
        from PIL import Image
    except Exception:
        return
    im = Image.open(png_path).convert("RGB")
    im.thumbnail(max_size)
    im.save(png_path.with_suffix(".jpg"), quality=90, optimize=True)


def plot_category_and_concentration(summary_csv: Path, out_dir: Path) -> list[Path]:
    funds, categories, data, top10 = read_summary(summary_csv)
    colors = {cat: DEFAULT_COLORS[i % len(DEFAULT_COLORS)] for i, cat in enumerate(categories)}
    outputs: list[Path] = []

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(13, 10), gridspec_kw={"height_ratios": [3.2, 1.2]})
    bottom = np.zeros(len(funds))
    for cat in categories:
        vals = [data[f][cat] for f in funds]
        ax.bar(funds, vals, bottom=bottom, label=cat, color=colors[cat])
        for i, v in enumerate(vals):
            if v >= 8:
                ax.text(i, bottom[i] + v / 2, f"{v:.0f}%", ha="center", va="center", fontsize=8)
        bottom += np.array(vals)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Operating-company weight (%)")
    ax.set_title("ETF Category Distribution\n(classified holdings; non-operating rows excluded)")
    ax.legend(ncol=2, loc="upper center", bbox_to_anchor=(0.5, -0.08), frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=0.2)

    vals = [top10[f] for f in funds]
    ax2.bar(funds, vals, color="#4C78A8")
    for i, v in enumerate(vals):
        ax2.text(i, v + 1, f"{v:.0f}%", ha="center", fontsize=8)
    ax2.set_ylabel("Top-10 weight (%)")
    ax2.set_title("Concentration rate: lower is more diversified")
    ax2.set_ylim(0, max(vals + [1]) + 10)
    ax2.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    png = out_dir / "category-distribution-and-concentration.png"
    fig.savefig(png, dpi=200, bbox_inches="tight")
    plt.close(fig)
    save_jpg_from_png(png)
    outputs.extend([png, png.with_suffix(".jpg")])

    cols = min(4, max(1, len(funds)))
    rows = int(np.ceil(len(funds) / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 4 * rows))
    axes_arr = np.array(axes).reshape(-1) if isinstance(axes, np.ndarray) else np.array([axes])
    for idx, fund in enumerate(funds):
        vals = [data[fund][cat] for cat in categories]
        axes_arr[idx].pie(vals, colors=[colors[c] for c in categories], startangle=90, counterclock=False, wedgeprops=dict(width=0.42, edgecolor="white"))
        axes_arr[idx].text(0, 0, f"{fund}\nTop10 {top10[fund]:.0f}%", ha="center", va="center", fontsize=10, fontweight="bold")
        axes_arr[idx].set_title(fund)
    for ax in axes_arr[len(funds):]:
        ax.axis("off")
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=colors[c], markersize=9) for c in categories]
    fig.legend(handles, categories, loc="lower center", ncol=2, frameon=False, fontsize=8)
    fig.suptitle("ETF Category Mix — Donut Small Multiples", fontsize=14, y=0.98)
    fig.tight_layout(rect=[0, 0.08, 1, 0.95])
    donut = out_dir / "category-mix-donut-small-multiples.png"
    fig.savefig(donut, dpi=200, bbox_inches="tight")
    plt.close(fig)
    save_jpg_from_png(donut)
    outputs.extend([donut, donut.with_suffix(".jpg")])
    return outputs


def plot_pair_heatmap(pair_miss_csv: Path, out_dir: Path) -> Path | None:
    if not pair_miss_csv.exists():
        return None
    pairs: list[str] = []
    cats: list[str] = []
    vals: dict[tuple[str, str], float] = {}
    with pair_miss_csv.open(newline="") as f:
        for row in csv.DictReader(f):
            pair = row["pair"]
            cat = row["miss_category"]
            if pair not in pairs:
                pairs.append(pair)
            if cat not in cats:
                cats.append(cat)
            vals[(pair, cat)] = float(row.get("missed_weight_in_excluded_funds") or 0)
    if not pairs or not cats:
        return None
    matrix = np.array([[vals.get((p, c), 0.0) for c in cats] for p in pairs])
    fig, ax = plt.subplots(figsize=(max(8, len(cats) * 1.6), max(4, len(pairs) * 0.7)))
    im = ax.imshow(matrix, cmap="Blues")
    ax.set_xticks(range(len(cats)), labels=cats, rotation=35, ha="right")
    ax.set_yticks(range(len(pairs)), labels=pairs)
    for i in range(len(pairs)):
        for j in range(len(cats)):
            ax.text(j, i, f"{matrix[i, j]:.0f}", ha="center", va="center", fontsize=8)
    ax.set_title("Pair-miss heatmap: missed excluded-fund weight by category")
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    out = out_dir / "pair-miss-heatmap.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    plt.close(fig)
    save_jpg_from_png(out)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("summary_csv", type=Path)
    ap.add_argument("-o", "--out-dir", type=Path, required=True)
    ap.add_argument("--pair-miss-by-category", type=Path)
    args = ap.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    outputs = plot_category_and_concentration(args.summary_csv, args.out_dir)
    heatmap = plot_pair_heatmap(args.pair_miss_by_category, args.out_dir) if args.pair_miss_by_category else None
    if heatmap:
        outputs.append(heatmap)
    for path in outputs:
        if path.exists():
            print(path)


if __name__ == "__main__":
    main()
