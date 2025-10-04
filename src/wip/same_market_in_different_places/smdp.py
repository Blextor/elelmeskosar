# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compare_csvs.py

Usage:
  python smdp.py szeged.csv szentendre.csv --barcode-col barcode --name-col product_name --out-dir results

What it does:
- Checks that the same barcode maps to the same name across files (cross-file consistency by barcode).
- Checks that the same name maps to the same barcode across files (cross-file consistency by name).
- Detects internal conflicts within each file (same barcode -> multiple names, or same name -> multiple barcodes).
- Writes separate CSVs for matches and conflicts, plus a summary.txt.
"""

import argparse
import os
import sys
import pandas as pd


def load_csv(path):
    # Try common encodings, prefer utf-8-sig to handle BOM
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
    # Strip surrounding whitespace; if case-insensitive, lower-case
    # Preserve NaNs
    s = s.astype(str).str.strip()
    s = s.where(~s.str.lower().isin(["nan", "none"]), other=pd.NA)
    if case_insensitive:
        s = s.str.lower()
    return s


def ensure_columns(df, barcode_col, name_col, label):
    missing = [c for c in [barcode_col, name_col] if c not in df.columns]
    if missing:
        raise ValueError(f"{label}: Missing columns: {missing}. Available columns: {list(df.columns)}")
    return df[[barcode_col, name_col]].copy()


def detect_internal_conflicts(df, key_col, val_col):
    # For each key, count distinct non-null values of val_col
    # Conflicts: keys mapping to more than one distinct value
    tmp = df.dropna(subset=[key_col]).copy()
    tmp[val_col] = tmp[val_col].fillna(pd.NA)
    groups = tmp.groupby(key_col, dropna=False)[val_col].nunique(dropna=True).reset_index(name="distinct_values")
    conflict_keys = groups.loc[groups["distinct_values"] > 1, key_col]
    conflicts = tmp[tmp[key_col].isin(conflict_keys)].sort_values([key_col, val_col])
    return conflicts


def unique_mapping(df, key_col, val_col):
    # Reduce to one row per key, but keep a marker if that key had conflicts internally
    # (choose the first non-null pairing as representative)
    tmp = df.copy()
    tmp = tmp.dropna(subset=[key_col])
    # Choose the first occurrence as representative
    reps = tmp.drop_duplicates(subset=[key_col], keep="first")[[key_col, val_col]].copy()
    # Mark keys that had multiple different vals
    conflict_tbl = detect_internal_conflicts(df, key_col, val_col)
    conflict_keys = set(conflict_tbl[key_col].unique().tolist())
    reps["internal_conflict"] = reps[key_col].apply(lambda k: k in conflict_keys)
    return reps, conflict_tbl


def main():
    ap = argparse.ArgumentParser(description="Compare two CSVs by barcode and name.")
    ap.add_argument("file1", help="First CSV file")
    ap.add_argument("file2", help="Second CSV file")
    ap.add_argument("--barcode-col", default="barcode", help="Column name for barcode (default: barcode)")
    ap.add_argument("--name-col", default="name", help="Column name for name (default: name)")
    ap.add_argument("--out-dir", default="comparison_results", help="Output directory")
    ap.add_argument("--case-insensitive", action="store_true", help="Compare names case-insensitively")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # Load
    df1 = load_csv(args.file1)
    df2 = load_csv(args.file2)

    # Validate and select cols
    df1 = ensure_columns(df1, args.barcode_col, args.name_col, "file1")
    df2 = ensure_columns(df2, args.barcode_col, args.name_col, "file2")

    # Rename to common names
    df1 = df1.rename(columns={args.barcode_col: "barcode", args.name_col: "name"})
    df2 = df2.rename(columns={args.barcode_col: "barcode", args.name_col: "name"})

    # Normalize
    df1["barcode"] = normalize_series(df1["barcode"], case_insensitive=False)
    df2["barcode"] = normalize_series(df2["barcode"], case_insensitive=False)
    df1["name"] = normalize_series(df1["name"], case_insensitive=args.case_insensitive)
    df2["name"] = normalize_series(df2["name"], case_insensitive=args.case_insensitive)

    # INTERNAL conflicts (within each file)
    f1_barcode_conflicts = detect_internal_conflicts(df1, "barcode", "name")
    f2_barcode_conflicts = detect_internal_conflicts(df2, "barcode", "name")
    f1_name_conflicts = detect_internal_conflicts(df1, "name", "barcode")
    f2_name_conflicts = detect_internal_conflicts(df2, "name", "barcode")

    # Reduce to representative unique mappings for cross-file comparisons
    f1_barcode_map, f1_barcode_conflict_tbl = unique_mapping(df1, "barcode", "name")
    f2_barcode_map, f2_barcode_conflict_tbl = unique_mapping(df2, "barcode", "name")
    f1_name_map, f1_name_conflict_tbl = unique_mapping(df1, "name", "barcode")
    f2_name_map, f2_name_conflict_tbl = unique_mapping(df2, "name", "barcode")

    # CROSS-FILE: by BARCODE (does same barcode map to same name?)
    bc_merge = f1_barcode_map.merge(
        f2_barcode_map,
        on="barcode",
        how="outer",
        suffixes=("_file1", "_file2")
    )

    # Determine matches and conflicts
    bc_merge["status"] = bc_merge.apply(
        lambda r: (
            "match" if pd.notna(r["name_file1"]) and pd.notna(r["name_file2"]) and r["name_file1"] == r["name_file2"]
            else ("only_in_file1" if pd.notna(r["name_file1"]) and pd.isna(r["name_file2"])
                  else ("only_in_file2" if pd.isna(r["name_file1"]) and pd.notna(r["name_file2"])
                        else (
                "conflict" if pd.notna(r["name_file1"]) and pd.notna(r["name_file2"]) and r["name_file1"] != r[
                    "name_file2"]
                else "missing")))
        ),
        axis=1
    )

    barcode_matches = bc_merge[bc_merge["status"] == "match"].copy()
    barcode_conflicts = bc_merge[bc_merge["status"] == "conflict"].copy()
    barcode_only_f1 = bc_merge[bc_merge["status"] == "only_in_file1"].copy()
    barcode_only_f2 = bc_merge[bc_merge["status"] == "only_in_file2"].copy()

    # CROSS-FILE: by NAME (does same name map to same barcode?)
    name_merge = f1_name_map.merge(
        f2_name_map,
        on="name",
        how="outer",
        suffixes=("_file1", "_file2")
    )

    name_merge["status"] = name_merge.apply(
        lambda r: (
            "match" if pd.notna(r["barcode_file1"]) and pd.notna(r["barcode_file2"]) and r["barcode_file1"] == r[
                "barcode_file2"]
            else ("only_in_file1" if pd.notna(r["barcode_file1"]) and pd.isna(r["barcode_file2"])
                  else ("only_in_file2" if pd.isna(r["barcode_file1"]) and pd.notna(r["barcode_file2"])
                        else (
                "conflict" if pd.notna(r["barcode_file1"]) and pd.notna(r["barcode_file2"]) and r["barcode_file1"] != r[
                    "barcode_file2"]
                else "missing")))
        ),
        axis=1
    )

    name_matches = name_merge[name_merge["status"] == "match"].copy()
    name_conflicts = name_merge[name_merge["status"] == "conflict"].copy()
    name_only_f1 = name_merge[name_merge["status"] == "only_in_file1"].copy()
    name_only_f2 = name_merge[name_merge["status"] == "only_in_file2"].copy()

    # Write outputs
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

    # Summary
    summary_path = os.path.join(args.out_dir, "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("=== Summary ===\n")
        f.write(f"File1: {args.file1}\n")
        f.write(f"File2: {args.file2}\n")
        f.write(f"Columns: barcode='{args.barcode_col}', name='{args.name_col}'\n")
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
        f.write(
            f"File1: barcode->name conflicts: {len(f1_barcode_conflicts.drop_duplicates(subset=['barcode', 'name']))}\n")
        f.write(
            f"File1: name->barcode conflicts: {len(f1_name_conflicts.drop_duplicates(subset=['name', 'barcode']))}\n")
        f.write(
            f"File2: barcode->name conflicts: {len(f2_barcode_conflicts.drop_duplicates(subset=['barcode', 'name']))}\n")
        f.write(
            f"File2: name->barcode conflicts: {len(f2_name_conflicts.drop_duplicates(subset=['name', 'barcode']))}\n\n")

        f.write("Output files:\n")
        for p in outputs:
            f.write(f"- {p}\n")
    print(f"Done. Results in: {os.path.abspath(args.out_dir)}")


if __name__ == "__main__":
    # Make pandas display consistent if ever printed
    pd.set_option("display.max_rows", 200)
    pd.set_option("display.max_columns", 50)
    pd.set_option("display.width", 120)
    main()
