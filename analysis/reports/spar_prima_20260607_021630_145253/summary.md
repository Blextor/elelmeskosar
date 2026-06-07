# SPAR vs Prima comparison

SPAR file: `data\markets_data\spar_normalized_data_20260607_021630.csv`
Prima file: `data\markets_data\prima_normalized_data_20260607_145253.csv`

## Counts
- `spar_rows`: 7822
- `prima_rows`: 4297
- `spar_rows_with_barcode`: 7277
- `prima_rows_with_barcode`: 4265
- `spar_unique_barcodes`: 7277
- `prima_unique_barcodes`: 4265
- `common_unique_barcodes`: 2178
- `spar_unique_names`: 7790
- `prima_unique_names`: 4280
- `common_unique_names`: 2042
- `spar_unique_barcode_name_pairs`: 7277
- `prima_unique_barcode_name_pairs`: 4265
- `common_barcode_name_pairs`: 2002
- `common_barcodes_without_exact_name_match`: 176

## Item price, exact same barcode and name
- `compared_pairs`: 2002
- `prima_more_expensive`: 1885
- `prima_cheaper`: 111
- `same_item_price`: 6
- `median_diff_prima_minus_spar`: 74.0
- `median_pct_prima_vs_spar`: 9.058402860548272
- `same_package_unit_and_step`: 2002

## Base price, exact same barcode and name
- `compared_pairs_same_base_unit`: 2002
- `prima_more_expensive`: 1885
- `prima_cheaper`: 111
- `same_base_price`: 6
- `median_diff_prima_minus_spar`: 433.3333333333335
- `median_pct_prima_vs_spar`: 9.058402860548265