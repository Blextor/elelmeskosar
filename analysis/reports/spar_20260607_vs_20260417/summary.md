# SPAR ?sszehasonl?t?s: 2026-06-07 vs 2026-04-17

- R?gi f?jl: `spar_normalized_data_20260417_021319.csv`
- ?j f?jl: `spar_normalized_data_20260607_014535.csv`

## Alapadatok

| Mutat? | 2026-04-17 | 2026-06-07 | V?ltoz?s |
|---|---:|---:|---:|
| Sorok | 4587 | 4728 | +141 |
| Egyedi nevek | 4564 | 4709 | +145 |
| Egyedi vonalk?dok | 4340 | 4336 | -4 |
| Egyedi store_product_id | 4587 | 4728 | +141 |
| Egyedi els? k?plinkek | 4587 | 4725 | +138 |
| Egyedi kateg?ri?k | 161 | 161 | +0 |
| El?rhet? term?kek | 4211 | 4354 | +143 |
| Nem el?rhet? term?kek | 376 | 374 | -2 |

## Egyedi ?rt?kek ?sszevet?se

| Azonos?t? | K?z?s | Csak r?gi | Csak ?j |
|---|---:|---:|---:|
| N?v | 3463 | 1101 | 1246 |
| Vonalk?d | 3249 | 1091 | 1087 |
| Store product ID | 3512 | 1075 | 1216 |
| Els? k?plink | 3239 | 1348 | 1486 |
| Kateg?ria | 131 | 30 | 30 |

## K?z?s vonalk?dok alapj?n

- K?z?s vonalk?d: 3249
- Ugyanaz a n?v: 3233
- Elt?r? n?v ugyanazon vonalk?dn?l: 16
- Elt?r? kateg?ria ugyanazon vonalk?dn?l: 3249
- Elt?r? els? k?plink ugyanazon vonalk?dn?l: 192
- El?rhet?s?g v?ltozott: 232
- Kiszerel?si egys?g/l?p?s v?ltozott: 7

## ?r k?z?s vonalk?dok alapj?n

- ?sszehasonl?that? ?r? term?k: 3249
- ?rv?ltoz?s: 608
- Dr?gult: 453
- Olcs?bb lett: 155
- V?ltozatlan: 2641
- Medi?n ?rk?l?nbs?g: 0.00 Ft
- Medi?n sz?zal?kos v?ltoz?s: 0.00%

## R?szletes CSV-k

- `barcode_category_changes.csv`
- `barcode_name_changes.csv`
- `barcode_price_changes.csv`
- `name_barcode_changes.csv`
- `new_internal_barcode_name_conflicts.csv`
- `new_internal_name_barcode_conflicts.csv`
- `old_internal_barcode_name_conflicts.csv`
- `old_internal_name_barcode_conflicts.csv`
- `only_new_barcodes.csv`
- `only_new_names.csv`
- `only_old_barcodes.csv`
- `only_old_names.csv`

## Kateg?ria sz?msuffix n?lk?l

A teljes `categories` mez? minden k?z?s rekordn?l elt?r, de ennek nagy r?sze a slug v?g?n l?v? sz?m v?ltoz?sa. Ha a v?gs? `-123` jelleg? sz?msuffixet lev?gjuk:

- K?z?s vonalk?dokn?l azonos kateg?rian?v-r?sz: 0
- K?z?s vonalk?dokn?l val?di kateg?rian?v-r?sz elt?r?s: 3249
- K?z?s nevekn?l azonos kateg?rian?v-r?sz: 0
- K?z?s nevekn?l val?di kateg?rian?v-r?sz elt?r?s: 3463

R?szletes f?jl: `barcode_category_base_changes.csv`.

## K?z?s store_product_id alapj?n

- K?z?s store_product_id: 3512
- Ugyanaz a n?v: 3479
- Elt?r? n?v: 33
- Ugyanaz a vonalk?d: 3249
- Elt?r? vonalk?d vagy hi?nyz?s: 263
- Ugyanaz az els? k?plink: 3239
- Elt?r? els? k?plink: 273

R?szletes f?jl: `store_product_id_changes.csv`.
