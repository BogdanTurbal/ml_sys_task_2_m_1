#!/usr/bin/env python3
"""Full analysis: separate throughput and index-size bar plots
for mixed workloads × fb dataset × 3 indexes (DynamicPGM, LIPP, HybridPGMLIPP).
BTree is excluded. Index-size plots include a zoomed inset comparing LIPP vs
HybridPGMLIPP with enough precision to show the ~1.7 MB PGM buffer overhead."""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DATASETS = {
    "fb": "fb_100M_public_uint64",
}
INDEXES = ["DynamicPGM", "LIPP", "HybridPGMLIPP"]
COLORS = {
    "DynamicPGM":     "tab:blue",
    "LIPP":           "tab:orange",
    "HybridPGMLIPP":  "tab:green",
}
OUT_DIR = "m2_results"


def best_row(df, index_name, throughput_cols):
    if "index_name" not in df.columns:
        return 0.0, 0
    rows = df[df["index_name"] == index_name]
    if rows.empty:
        return 0.0, 0
    existing_cols = [c for c in throughput_cols if c in df.columns]
    if not existing_cols:
        return 0.0, 0
    means = rows[existing_cols].mean(axis=1)
    best_idx = means.idxmax()
    return float(means.loc[best_idx]), int(rows.loc[best_idx, "index_size_bytes"])


def load_csv(dataset_full, pattern):
    path = f"results/{dataset_full}_{pattern}_results_table.csv"
    if not os.path.exists(path):
        print(f"  WARNING: missing {path}")
        return pd.DataFrame()
    # Read with extended column names to handle indexes with multiple variant
    # fields (e.g. HybridPGMLIPP has 3 variant columns but the header has 2).
    with open(path) as f:
        header_cols = f.readline().strip().split(",")
    max_extra = 3
    extended_cols = header_cols + [f"variant{i}" for i in range(1, max_extra + 1)]
    return pd.read_csv(path, names=extended_cols, skiprows=1, engine="python")


def make_grouped_bar(title, datasets_short, indexes, values_by_ds, ylabel, filename):
    """Throughput bar chart: one group per index, one bar per dataset."""
    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(indexes))
    n_ds = len(datasets_short)
    width = 0.8 / n_ds
    ds_colors = {"fb": "tab:blue", "books": "tab:red", "osmc": "tab:green"}

    for i, ds in enumerate(datasets_short):
        vals = [values_by_ds[ds][idx] for idx in indexes]
        offset = (i - (n_ds - 1) / 2) * width
        bars = ax.bar(x + offset, vals, width, label=ds, color=ds_colors[ds])
        for bar, val in zip(bars, vals):
            if val > 0:
                label = f"{val:.2f}" if val < 100 else f"{val:.1f}"
                ax.text(bar.get_x() + bar.get_width() / 2, val, label,
                        ha="center", va="bottom", fontsize=14)

    ax.set_ylabel(ylabel, fontsize=18)
    ax.set_title(title, fontsize=20)
    ax.set_xticks(x)
    ax.set_xticklabels(indexes, fontsize=18)
    ax.tick_params(axis="y", labelsize=18)
    ax.legend(fontsize=18)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, filename), dpi=300)
    plt.close(fig)
    print(f"  Saved {OUT_DIR}/{filename}")


def make_size_bar(title, datasets_short, indexes, values_by_ds, ylabel, filename):
    """Index-size bar chart (left) + zoomed inset for LIPP vs HybridPGMLIPP (right)."""
    zoom_indexes = [idx for idx in ["LIPP", "HybridPGMLIPP"] if idx in indexes]
    fig, (ax, ax_zoom) = plt.subplots(1, 2, figsize=(18, 7),
                                       gridspec_kw={"width_ratios": [2, 1]})
    x = np.arange(len(indexes))
    n_ds = len(datasets_short)
    width = 0.8 / n_ds
    ds_colors = {"fb": "tab:blue", "books": "tab:red", "osmc": "tab:green"}

    # --- Left panel: all indexes ---
    for i, ds in enumerate(datasets_short):
        vals = [values_by_ds[ds][idx] for idx in indexes]
        offset = (i - (n_ds - 1) / 2) * width
        bars = ax.bar(x + offset, vals, width, label=ds, color=ds_colors[ds])
        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, val,
                        f"{val:.4f}", ha="center", va="bottom",
                        fontsize=11, rotation=30)

    ax.set_ylabel(ylabel, fontsize=18)
    ax.set_title(title, fontsize=18)
    ax.set_xticks(x)
    ax.set_xticklabels(indexes, fontsize=16)
    ax.tick_params(axis="y", labelsize=16)
    ax.legend(fontsize=16)
    ax.grid(axis="y", alpha=0.3)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.18)

    # --- Right panel: zoom on LIPP vs HybridPGMLIPP ---
    x_zoom = np.arange(len(zoom_indexes))
    for i, ds in enumerate(datasets_short):
        vals_zoom = [values_by_ds[ds].get(idx, 0) for idx in zoom_indexes]
        offset = (i - (n_ds - 1) / 2) * width
        bars = ax_zoom.bar(x_zoom + offset, vals_zoom, width,
                           label=ds, color=ds_colors[ds])
        for bar, val in zip(bars, vals_zoom):
            if val > 0:
                ax_zoom.text(bar.get_x() + bar.get_width() / 2, val,
                             f"{val:.6f}", ha="center", va="bottom",
                             fontsize=11, rotation=30)

    # Zoom y-axis to show the tiny PGM buffer difference
    all_zoom_vals = [values_by_ds[ds].get(idx, 0)
                     for ds in datasets_short for idx in zoom_indexes
                     if values_by_ds[ds].get(idx, 0) > 0]
    if all_zoom_vals:
        lo = min(all_zoom_vals)
        hi = max(all_zoom_vals)
        margin = max((hi - lo) * 10, 0.002)  # at least 2 MB range visible
        ax_zoom.set_ylim(lo - margin, hi + margin * 4)

    ax_zoom.set_ylabel(ylabel, fontsize=18)
    ax_zoom.set_title("LIPP vs HybridPGMLIPP\n(zoomed)", fontsize=16)
    ax_zoom.set_xticks(x_zoom)
    ax_zoom.set_xticklabels(zoom_indexes, fontsize=16)
    ax_zoom.tick_params(axis="y", labelsize=14)
    ax_zoom.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, filename), dpi=300)
    plt.close(fig)
    print(f"  Saved {OUT_DIR}/{filename}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    mixed_cols = ["mixed_throughput_mops1", "mixed_throughput_mops2", "mixed_throughput_mops3"]
    summary_rows = []
    ds_list = list(DATASETS.keys())

    # --- Mixed 10% insert ---
    tp_by_ds, sz_by_ds = {}, {}
    for ds_short, ds_full in DATASETS.items():
        df = load_csv(ds_full, "ops_2M_0.000000rq_0.500000nl_0.100000i_0m_mix")
        tp_by_ds[ds_short] = {}
        sz_by_ds[ds_short] = {}
        for idx in INDEXES:
            tp, sz = best_row(df, idx, mixed_cols)
            tp_by_ds[ds_short][idx] = tp
            sz_by_ds[ds_short][idx] = sz / 1e9
            summary_rows.append({"workload": "Mixed (10% Insert)", "dataset": ds_short,
                                 "index": idx, "throughput_mops": round(tp, 6),
                                 "index_size_gb": round(sz / 1e9, 6)})

    make_grouped_bar("Mixed (90% Lookup, 10% Insert) — Throughput", ds_list, INDEXES,
                     tp_by_ds, "Throughput (Mops/s)", "mixed_10insert_throughput.png")
    make_size_bar("Mixed (90% Lookup, 10% Insert) — Index Size", ds_list, INDEXES,
                  sz_by_ds, "Index Size (GB)", "mixed_10insert_index_size.png")

    # --- Mixed 90% insert ---
    tp_by_ds, sz_by_ds = {}, {}
    for ds_short, ds_full in DATASETS.items():
        df = load_csv(ds_full, "ops_2M_0.000000rq_0.500000nl_0.900000i_0m_mix")
        tp_by_ds[ds_short] = {}
        sz_by_ds[ds_short] = {}
        for idx in INDEXES:
            tp, sz = best_row(df, idx, mixed_cols)
            tp_by_ds[ds_short][idx] = tp
            sz_by_ds[ds_short][idx] = sz / 1e9
            summary_rows.append({"workload": "Mixed (90% Insert)", "dataset": ds_short,
                                 "index": idx, "throughput_mops": round(tp, 6),
                                 "index_size_gb": round(sz / 1e9, 6)})

    make_grouped_bar("Mixed (10% Lookup, 90% Insert) — Throughput", ds_list, INDEXES,
                     tp_by_ds, "Throughput (Mops/s)", "mixed_90insert_throughput.png")
    make_size_bar("Mixed (10% Lookup, 90% Insert) — Index Size", ds_list, INDEXES,
                  sz_by_ds, "Index Size (GB)", "mixed_90insert_index_size.png")

    # --- Summary CSV ---
    pd.DataFrame(summary_rows).to_csv(os.path.join(OUT_DIR, "m2_summary.csv"), index=False)
    print(f"\nSaved {OUT_DIR}/m2_summary.csv")


if __name__ == "__main__":
    main()
