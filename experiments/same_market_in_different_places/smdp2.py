
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_csvs.py

Usage:
    python smdp2.py szeged2.csv szentendre2.csv --barcode-col barcode --name-col product_name --price-col unit_price --out-dir results4
  python compare_csvs.py file1.csv file2.csv \
      --barcode-col barcode --name-col name [--price-col price] \
      --out-dir results \
      [--case-insensitive]

What it does:
- Checks that the same barcode maps to the same name across files (cross-file consistency by barcode).
- Checks that the same name maps to the same barcode across files (cross-file consistency by name).
- Detects internal conflicts within each file (same barcode -> multiple names, or same name -> multiple barcodes).
- If a price column is provided (default: 'price' when present), compares prices for items that match by BOTH barcode and name.
  * Computes absolute difference and two percentage metrics:
      - pct_vs_file1 = (file2 - file1) / file1 * 100
      - pct_symmetric = |file2 - file1| / ((file1 + file2)/2) * 100   (when both prices > 0)
- Writes separate CSVs for matches and conflicts, plus a summary.txt and price_summary.txt (if price compared).
"""

import argparse
import os
import sys
import re
import math
import pandas as pd
import numpy as np

def load_csv(path):
    encodings = ["utf-8-sig", "utf-8", "cp1250", "latin-1"]
    last_err = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception as e:
            last_err = e
            continue
    raise last_err

def normalize_series(s, case_insensitive=False):
    s = s.astype(str).str.strip()
    s = s.where(~s.str.lower().isin(["nan", "none"]), other=pd.NA)
    if case_insensitive:
        s = s.str.lower()
    return s

def ensure_columns(df, barcode_col, name_col, label):
    missing = [c for c in [barcode_col, name_col] if c not in df.columns]
    if missing:
        raise ValueError(f"{label}: Missing columns: {missing}. Available columns: {list(df.columns)}")
    return df

def detect_internal_conflicts(df, key_col, val_col):
    tmp = df.dropna(subset=[key_col]).copy()
    tmp[val_col] = tmp[val_col].fillna(pd.NA)
    groups = tmp.groupby(key_col, dropna=False)[val_col].nunique(dropna=True).reset_index(name="distinct_values")
    conflict_keys = groups.loc[groups["distinct_values"] > 1, key_col]
    conflicts = tmp[tmp[key_col].isin(conflict_keys)].sort_values([key_col, val_col])
    return conflicts

def unique_mapping(df, key_col, val_col):
    tmp = df.copy()
    tmp = tmp.dropna(subset=[key_col])
    reps = tmp.drop_duplicates(subset=[key_col], keep="first")[[key_col, val_col]].copy()
    conflict_tbl = detect_internal_conflicts(df, key_col, val_col)
    conflict_keys = set(conflict_tbl[key_col].unique().tolist())
    reps["internal_conflict"] = reps[key_col].apply(lambda k: k in conflict_keys)
    return reps, conflict_tbl

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

PRICE_PATTERN = re.compile(r"[-+]?\d[\d\s\.,]*")

def parse_price_value(x):
    """Parse various price formats to float. Returns NaN if not parseable."""
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if not s:
        return np.nan
    m = PRICE_PATTERN.search(s)
    if not m:
        return np.nan
    token = m.group(0)
    token = token.replace(" ", "")
    token = token.replace(",", ".")
    if token.count(".") > 1:
        parts = token.split(".")
        token = "".join(parts[:-1]) + "." + parts[-1]
    try:
        return float(token)
    except Exception:
        return np.nan

def parse_price_column(s):
    return s.apply(parse_price_value)

def main():
    ap = argparse.ArgumentParser(description="Compare two CSVs by barcode, name, and (optionally) price.")
    ap.add_argument("file1", help="First CSV file")
    ap.add_argument("file2", help="Second CSV file")
    ap.add_argument("--barcode-col", default="barcode", help="Column name for barcode (default: barcode)")
    ap.add_argument("--name-col", default="name", help="Column name for name (default: name)")
    ap.add_argument("--price-col", default="price", help="Column name for price (default: price; if missing in either file, price comparison is skipped)")
    ap.add_argument("--out-dir", default="comparison_results", help="Output directory")
    ap.add_argument("--case-insensitive", action="store_true", help="Compare names case-insensitively")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    df1 = load_csv(args.file1)
    df2 = load_csv(args.file2)

    df1 = ensure_columns(df1, args.barcode_col, args.name_col, "file1")
    df2 = ensure_columns(df2, args.barcode_col, args.name_col, "file2")

    rename1 = {args.barcode_col: "barcode", args.name_col: "name"}
    rename2 = {args.barcode_col: "barcode", args.name_col: "name"}
    if args.price_col in df1.columns: rename1[args.price_col] = "price"
    if args.price_col in df2.columns: rename2[args.price_col] = "price"
    df1 = df1.rename(columns=rename1)
    df2 = df2.rename(columns=rename2)

    df1["barcode"] = normalize_series(df1["barcode"], case_insensitive=False)
    df2["barcode"] = normalize_series(df2["barcode"], case_insensitive=False)
    df1["name"] = normalize_series(df1["name"], case_insensitive=args.case_insensitive)
    df2["name"] = normalize_series(df2["name"], case_insensitive=args.case_insensitive)

    f1_barcode_conflicts = detect_internal_conflicts(df1, "barcode", "name")
    f2_barcode_conflicts = detect_internal_conflicts(df2, "barcode", "name")
    f1_name_conflicts = detect_internal_conflicts(df1, "name", "barcode")
    f2_name_conflicts = detect_internal_conflicts(df2, "name", "barcode")

    f1_barcode_map, _ = unique_mapping(df1, "barcode", "name")
    f2_barcode_map, _ = unique_mapping(df2, "barcode", "name")
    f1_name_map, _ = unique_mapping(df1, "name", "barcode")
    f2_name_map, _ = unique_mapping(df2, "name", "barcode")

    bc_merge = f1_barcode_map.merge(
        f2_barcode_map,
        on="barcode",
        how="outer",
        suffixes=("_file1", "_file2")
    )
    bc_merge["status"] = bc_merge.apply(
        lambda r: (
            "match" if pd.notna(r["name_file1"]) and pd.notna(r["name_file2"]) and r["name_file1"] == r["name_file2"]
            else ("only_in_file1" if pd.notna(r["name_file1"]) and pd.isna(r["name_file2"])
            else ("only_in_file2" if pd.isna(r["name_file1"]) and pd.notna(r["name_file2"])
            else ("conflict" if pd.notna(r["name_file1"]) and pd.notna(r["name_file2"]) and r["name_file1"] != r["name_file2"]
            else "missing")))
        ),
        axis=1
    )

    barcode_matches = bc_merge[bc_merge["status"] == "match"].copy()
    barcode_conflicts = bc_merge[bc_merge["status"] == "conflict"].copy()
    barcode_only_f1 = bc_merge[bc_merge["status"] == "only_in_file1"].copy()
    barcode_only_f2 = bc_merge[bc_merge["status"] == "only_in_file2"].copy()

    name_merge = f1_name_map.merge(
        f2_name_map,
        on="name",
        how="outer",
        suffixes=("_file1", "_file2")
    )
    name_merge["status"] = name_merge.apply(
        lambda r: (
            "match" if pd.notna(r["barcode_file1"]) and pd.notna(r["barcode_file2"]) and r["barcode_file1"] == r["barcode_file2"]
            else ("only_in_file1" if pd.notna(r["barcode_file1"]) and pd.isna(r["barcode_file2"])
            else ("only_in_file2" if pd.isna(r["barcode_file1"]) and pd.notna(r["barcode_file2"])
            else ("conflict" if pd.notna(r["barcode_file1"]) and pd.notna(r["barcode_file2"]) and r["barcode_file1"] != r["barcode_file2"]
            else "missing")))
        ),
        axis=1
    )

    name_matches = name_merge[name_merge["status"] == "match"].copy()
    name_conflicts = name_merge[name_merge["status"] == "conflict"].copy()
    name_only_f1 = name_merge[name_merge["status"] == "only_in_file1"].copy()
    name_only_f2 = name_merge[name_merge["status"] == "only_in_file2"].copy()

    def save(df, filename):
        out = os.path.join(args.out_dir, filename)
        df.to_csv(out, index=False, encoding="utf-8-sig")
        return out

    outputs = []
    outputs.append(save(barcode_matches, "barcode_matches.csv"))
    outputs.append(save(barcode_conflicts, "barcode_conflicts.csv"))
    outputs.append(save(barcode_only_f1, "barcode_only_in_file1.csv"))
    outputs.append(save(barcode_only_f2, "barcode_only_in_file2.csv"))
    outputs.append(save(name_matches, "name_matches.csv"))
    outputs.append(save(name_conflicts, "name_conflicts.csv"))
    outputs.append(save(name_only_f1, "name_only_in_file1.csv"))
    outputs.append(save(name_only_f2, "name_only_in_file2.csv"))
    outputs.append(save(f1_barcode_conflicts, "internal_file1_barcode_conflicts.csv"))
    outputs.append(save(f2_barcode_conflicts, "internal_file2_barcode_conflicts.csv"))
    outputs.append(save(f1_name_conflicts, "internal_file1_name_conflicts.csv"))
    outputs.append(save(f2_name_conflicts, "internal_file2_name_conflicts.csv"))

    # PRICE comparison (barcode + name matches)
    can_compare_price = ("price" in df1.columns) and ("price" in df2.columns)
    price_outputs = []
    if can_compare_price:
        f1_prices = df1.dropna(subset=["barcode", "name"]).drop_duplicates(subset=["barcode", "name"], keep="first")[["barcode","name","price"]].copy()
        f2_prices = df2.dropna(subset=["barcode", "name"]).drop_duplicates(subset=["barcode", "name"], keep="first")[["barcode","name","price"]].copy()

        keys = barcode_matches[["barcode","name_file1"]].rename(columns={"name_file1":"name"}).copy()

        pm = keys.merge(f1_prices, on=["barcode","name"], how="left") \
                 .merge(f2_prices, on=["barcode","name"], how="left", suffixes=("_file1","_file2"))

        pm["price_file1_parsed"] = parse_price_column(pm["price_file1"]) if "price_file1" in pm.columns else np.nan
        pm["price_file2_parsed"] = parse_price_column(pm["price_file2"]) if "price_file2" in pm.columns else np.nan

        pm["abs_diff"] = pm["price_file2_parsed"] - pm["price_file1_parsed"]
        pm["pct_vs_file1"] = np.where(
            pm["price_file1_parsed"].abs() > 0,
            (pm["abs_diff"] / pm["price_file1_parsed"]) * 100.0,
            np.nan
        )
        mean_prices = (pm["price_file1_parsed"] + pm["price_file2_parsed"]) / 2.0
        pm["pct_symmetric"] = np.where(
            (mean_prices > 0) & pm["price_file1_parsed"].notna() & pm["price_file2_parsed"].notna(),
            (pm["abs_diff"].abs() / mean_prices) * 100.0,
            np.nan
        )

        ordered_cols = [
            "barcode","name",
            "price_file1","price_file1_parsed",
            "price_file2","price_file2_parsed",
            "abs_diff","pct_vs_file1","pct_symmetric"
        ]
        pm = pm[ordered_cols]

        price_outputs.append(save(pm, "price_differences.csv"))
        top = pm.dropna(subset=["pct_symmetric"]).copy()
        top = top.reindex(top["pct_symmetric"].abs().sort_values(ascending=False).index)
        price_outputs.append(save(top, "top_price_differences.csv"))

        # Summary stats
        valid = pm.dropna(subset=["price_file1_parsed","price_file2_parsed"]).copy()
        n_all = len(pm); n_valid = len(valid); n_missing = n_all - n_valid
        def s(x): return "nan" if pd.isna(x) else f"{x:.2f}"
        if n_valid > 0:
            mean_abs = valid["abs_diff"].mean(); median_abs = valid["abs_diff"].median()
            mean_pct1 = valid["pct_vs_file1"].mean(); median_pct1 = valid["pct_vs_file1"].median()
            mean_pct_sym = valid["pct_symmetric"].mean(); median_pct_sym = valid["pct_symmetric"].median()
        else:
            mean_abs=median_abs=mean_pct1=median_pct1=mean_pct_sym=median_pct_sym=np.nan
        with open(os.path.join(args.out_dir, "price_summary.txt"), "w", encoding="utf-8") as f:
            f.write("=== Price Comparison Summary ===\n")
            f.write(f"Comparable (barcode+name matches) rows: {n_all}\n")
            f.write(f"Rows with parseable prices in both files: {n_valid}\n")
            f.write(f"Rows with missing/unparseable price(s): {n_missing}\n\n")
            f.write("--- Absolute difference (file2 - file1) ---\n")
            f.write(f"Mean: {s(mean_abs)} | Median: {s(median_abs)}\n\n")
            f.write("--- % difference vs file1 ---\n")
            f.write(f"Mean: {s(mean_pct1)}% | Median: {s(median_pct1)}%\n\n")
            f.write("--- Symmetric % difference ---\n")
            f.write(f"Mean: {s(mean_pct_sym)}% | Median: {s(median_pct_sym)}%\n")

    # Main summary
    with open(os.path.join(args.out_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("=== Summary ===\n")
        f.write(f"File1: {args.file1}\n")
        f.write(f"File2: {args.file2}\n")
        f.write(f"Columns: barcode='{args.barcode_col}', name='{args.name_col}', price='{args.price_col}'\n")
        f.write(f"Case-insensitive name compare: {args.case_insensitive}\n\n")
        f.write("--- Cross-file by BARCODE ---\n")
        f.write(f"Matches: {len(barcode_matches)}\n")
        f.write(f"Conflicts: {len(barcode_conflicts)}\n")
        f.write(f"Only in file1: {len(barcode_only_f1)}\n")
        f.write(f"Only in file2: {len(barcode_only_f2)}\n\n")
        f.write("--- Cross-file by NAME ---\n")
        f.write(f"Matches: {len(name_matches)}\n")
        f.write(f"Conflicts: {len(name_conflicts)}\n")
        f.write(f"Only in file1: {len(name_only_f1)}\n")
        f.write(f"Only in file2: {len(name_only_f2)}\n\n")
        f.write("--- Internal conflicts (within files) ---\n")
        f.write(f"File1: barcode->name conflicts: {len(f1_barcode_conflicts.drop_duplicates(subset=['barcode','name']))}\n")
        f.write(f"File1: name->barcode conflicts: {len(f1_name_conflicts.drop_duplicates(subset=['name','barcode']))}\n")
        f.write(f"File2: barcode->name conflicts: {len(f2_barcode_conflicts.drop_duplicates(subset=['barcode','name']))}\n")
        f.write(f"File2: name->barcode conflicts: {len(f2_name_conflicts.drop_duplicates(subset=['name','barcode']))}\n\n")
        if can_compare_price:
            f.write("--- Price comparison outputs ---\n")
            f.write("price_differences.csv, top_price_differences.csv, price_summary.txt\n")
        else:
            f.write("--- Price comparison skipped ---\n")
            f.write(f"Reason: price column '{args.price_col}' not present in both files.\n")

    print("Updated script written.")
if __name__ == "__main__":
    pd.set_option("display.max_rows", 200)
    pd.set_option("display.max_columns", 50)
    pd.set_option("display.width", 120)
    main()
