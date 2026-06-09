# Tesco-SPAR-Príma összehasonlítás

## Bemeneti fájlok

- Spar: `spar_normalized_data_20260607_021630.csv`
- Prima: `prima_normalized_data_20260607_145253.csv`
- Tesco: `tesco_normalized_data_20260607_171937.csv`

## Alap statisztika

- Spar: 7822 sor, 7277 egyedi vonalkód, 7790 egyedi név, 7277 egyedi
  vonalkód+név pár.
- Prima: 4297 sor, 4265 egyedi vonalkód, 4280 egyedi név, 4265 egyedi
  vonalkód+név pár.
- Tesco: 17937 sor, 17937 egyedi vonalkód, 17812 egyedi név, 17937 egyedi
  vonalkód+név pár.

## Egyezések

- Vonalkód: SPAR-Príma 2178, SPAR-Tesco 3894, Príma-Tesco 2669, mindhárom 1834.
- Név: SPAR-Príma 2042, SPAR-Tesco 3767, Príma-Tesco 2422, mindhárom 1641.
- Vonalkód+név: SPAR-Príma 2002, SPAR-Tesco 3711, Príma-Tesco 2380, mindhárom
  1604.

## Páronkénti alapár-összehasonlítás vonalkód+név alapján

- Spar_vs_Prima: 2002 közös kulcs, 2002 összevethető; Spar olcsóbb 1885
  esetben, Prima olcsóbb 111 esetben, azonos 6; medián eltérés 9.058%
  (Prima - Spar).
- Spar_vs_Tesco: 3711 közös kulcs, 3638 összevethető; Spar olcsóbb 603 esetben,
  Tesco olcsóbb 2959 esetben, azonos 76; medián eltérés -6.903%
  (Tesco - Spar).
- Prima_vs_Tesco: 2380 közös kulcs, 2323 összevethető; Prima olcsóbb 87 esetben,
  Tesco olcsóbb 2221 esetben, azonos 15; medián eltérés -16.258%
  (Tesco - Prima).

## Kimeneti fájlok

- `summary.json`
- `overlap_summary.csv`
- `pairwise_base_price_summary.csv`
- `price_spread_by_barcode_name.csv`
- `price_spread_by_barcode.csv`
- `price_spread_by_name.csv`
- `all_three_barcode_name_base_price_comparison.csv`
- `all_three_barcode_base_price_comparison.csv`
- `all_three_name_base_price_comparison.csv`

## Megjegyzések

- A névegyezés exact normalizált név: kisbetűsítés és whitespace rendezés, nem
  fuzzy matching.
- A vonalkód egyezésnél a vezető nullákat levágtam a kulcsból, mert egyes
  források 14 jegyű GTIN-ként írják ugyanazt a kódot.
- Az árösszevetés alapáron történik: `g -> Ft/kg`, `ml -> Ft/l`, `db -> Ft/db`.
- Név-only egyezésnél nem kell a vonalkódnak egyeznie; ha bolton belül több
  azonos név van, a legalacsonyabb összevethető alapárú sor lett a reprezentáns.
