#!/usr/bin/env python3
"""
Extract report-ready Milestone 1 tables from benchmark CSV files.

The script:
1) reads all *_results_table.csv files in results/
2) computes averages across the 3 repeated runs
3) picks the best row per dataset/workload/index
4) writes compact CSVs for direct reporting
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List

import pandas as pd


RESULT_FILE_RE = re.compile(
    r"^(?P<dataset>[a-z]+)_100M_public_uint64_(?P<workload>.+)_results_table\.csv$"
)

INDEX_ORDER = ["BTree", "DynamicPGM", "LIPP"]


def detect_workload_type(df: pd.DataFrame) -> str:
    cols = set(df.columns)
    if {
        "lookup_throughput_mops1",
        "lookup_throughput_mops2",
        "lookup_throughput_mops3",
    }.issubset(cols):
        if {
            "insert_throughput_mops1",
            "insert_throughput_mops2",
            "insert_throughput_mops3",
        }.issubset(cols):
            return "insert_lookup"
        return "lookup_only"
    if {
        "mixed_throughput_mops1",
        "mixed_throughput_mops2",
        "mixed_throughput_mops3",
    }.issubset(cols):
        return "mixed"
    raise ValueError("Unknown workload type from columns")


def with_means(df: pd.DataFrame, workload_type: str) -> pd.DataFrame:
    out = df.copy()
    if workload_type in {"lookup_only", "insert_lookup"}:
        out["lookup_mean_mops"] = out[
            ["lookup_throughput_mops1", "lookup_throughput_mops2", "lookup_throughput_mops3"]
        ].mean(axis=1)
    if workload_type == "insert_lookup":
        out["insert_mean_mops"] = out[
            ["insert_throughput_mops1", "insert_throughput_mops2", "insert_throughput_mops3"]
        ].mean(axis=1)
        out["balanced_mean_mops"] = (out["lookup_mean_mops"] + out["insert_mean_mops"]) / 2.0
    if workload_type == "mixed":
        out["mixed_mean_mops"] = out[
            ["mixed_throughput_mops1", "mixed_throughput_mops2", "mixed_throughput_mops3"]
        ].mean(axis=1)

    if {"build_time_ns1", "build_time_ns2", "build_time_ns3"}.issubset(out.columns):
        out["build_time_mean_ns"] = out[
            ["build_time_ns1", "build_time_ns2", "build_time_ns3"]
        ].mean(axis=1)
    return out


def choose_best_rows(
    df: pd.DataFrame, dataset: str, workload_file_stem: str, workload_type: str
) -> List[Dict]:
    rows: List[Dict] = []
    for index_name in INDEX_ORDER:
        cand = df[df["index_name"] == index_name]
        if cand.empty:
            continue

        # Keep output stable for ties.
        sort_cols = ["index_name", "search_method", "value"]
        present_sort_cols = [c for c in sort_cols if c in cand.columns]
        if present_sort_cols:
            cand = cand.sort_values(present_sort_cols, kind="stable")

        if workload_type == "lookup_only":
            best = cand.loc[cand["lookup_mean_mops"].idxmax()]
            rows.append(
                make_record(
                    dataset, workload_file_stem, workload_type, index_name, "lookup", best
                )
            )
        elif workload_type == "mixed":
            best = cand.loc[cand["mixed_mean_mops"].idxmax()]
            rows.append(
                make_record(
                    dataset, workload_file_stem, workload_type, index_name, "mixed", best
                )
            )
        else:
            # Insert+lookup file: select best for each report metric.
            best_lookup = cand.loc[cand["lookup_mean_mops"].idxmax()]
            best_insert = cand.loc[cand["insert_mean_mops"].idxmax()]
            best_balanced = cand.loc[cand["balanced_mean_mops"].idxmax()]

            rows.append(
                make_record(
                    dataset,
                    workload_file_stem,
                    workload_type,
                    index_name,
                    "lookup",
                    best_lookup,
                )
            )
            rows.append(
                make_record(
                    dataset,
                    workload_file_stem,
                    workload_type,
                    index_name,
                    "insert",
                    best_insert,
                )
            )
            rows.append(
                make_record(
                    dataset,
                    workload_file_stem,
                    workload_type,
                    index_name,
                    "balanced",
                    best_balanced,
                )
            )
    return rows


def make_record(
    dataset: str,
    workload_file_stem: str,
    workload_type: str,
    index_name: str,
    metric: str,
    row: pd.Series,
) -> Dict:
    record = {
        "dataset": dataset,
        "workload_file_stem": workload_file_stem,
        "workload_type": workload_type,
        "index_name": index_name,
        "metric": metric,
        "search_method": row.get("search_method", ""),
        "value": row.get("value", ""),
        "index_size_bytes": row.get("index_size_bytes", None),
        "build_time_mean_ns": row.get("build_time_mean_ns", None),
        "lookup_mean_mops": row.get("lookup_mean_mops", None),
        "insert_mean_mops": row.get("insert_mean_mops", None),
        "mixed_mean_mops": row.get("mixed_mean_mops", None),
    }
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results-dir",
        default="results",
        help="Directory containing *_results_table.csv files",
    )
    parser.add_argument(
        "--output-dir",
        default="analysis_results",
        help="Directory where report-ready CSVs are written",
    )
    args = parser.parse_args()

    results_dir = Path(args.results_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = sorted(results_dir.glob("*_results_table.csv"))
    if not files:
        raise SystemExit(f"No results files found in: {results_dir}")

    all_best_rows: List[Dict] = []

    for fpath in files:
        m = RESULT_FILE_RE.match(fpath.name)
        if not m:
            # Skip non-standard files.
            continue
        dataset = m.group("dataset")
        workload_file_stem = m.group("workload")

        df = pd.read_csv(fpath)
        workload_type = detect_workload_type(df)
        df = with_means(df, workload_type)
        all_best_rows.extend(
            choose_best_rows(df, dataset, workload_file_stem, workload_type)
        )

    best_df = pd.DataFrame(all_best_rows)
    best_df = best_df.sort_values(
        ["dataset", "workload_type", "workload_file_stem", "index_name", "metric"],
        kind="stable",
    )

    # Main long-form table for report generation.
    best_df.to_csv(output_dir / "m1_best_rows_long.csv", index=False)

    # Compact tables commonly needed in Milestone 1 writeups.
    lookup_summary = (
        best_df[
            (best_df["workload_type"] == "lookup_only") & (best_df["metric"] == "lookup")
        ][["dataset", "index_name", "lookup_mean_mops", "search_method", "value"]]
        .sort_values(["dataset", "index_name"], kind="stable")
        .reset_index(drop=True)
    )
    lookup_summary.to_csv(output_dir / "m1_lookup_summary.csv", index=False)

    insert_lookup_summary = (
        best_df[
            (best_df["workload_type"] == "insert_lookup")
            & (best_df["metric"].isin(["lookup", "insert"]))
        ][
            [
                "dataset",
                "index_name",
                "metric",
                "lookup_mean_mops",
                "insert_mean_mops",
                "search_method",
                "value",
            ]
        ]
        .sort_values(["dataset", "index_name", "metric"], kind="stable")
        .reset_index(drop=True)
    )
    insert_lookup_summary.to_csv(output_dir / "m1_insert_lookup_summary.csv", index=False)

    print(f"Wrote: {output_dir / 'm1_best_rows_long.csv'}")
    print(f"Wrote: {output_dir / 'm1_lookup_summary.csv'}")
    print(f"Wrote: {output_dir / 'm1_insert_lookup_summary.csv'}")


if __name__ == "__main__":
    main()
