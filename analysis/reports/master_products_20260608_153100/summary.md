# Mestertermék riport

## Bemeneti fájlok

- Spar: `spar_normalized_data_20260607_021630.csv`
- Prima: `prima_normalized_data_20260607_145253.csv`
- Tesco: `tesco_normalized_data_20260607_171937.csv`

## Összkép

- Forrássorok száma: 30056
- Mestertermékek száma: 22789
- Ellenőrzést igénylő mestertermékek: 455
- Párosító élek száma: 27836

## Bolti sorok

- Prima: 4297
- Spar: 7822
- Tesco: 17937

## Párosítási módszerek

- same_barcode: 8741
- same_exact_name: 8483
- same_image_key: 1917
- same_name_core_compatible_pack: 8695

## Ellenőrzési okok

- azonos_kép_eltérő_vonalkód: 79
- eltérő_kiszerelés_db: 2
- eltérő_kiszerelés_g: 80
- eltérő_kiszerelés_ml: 6
- eltérő_kiszerelési_egység: 140
- sok_névváltozat: 10
- több_ajánlat_azonos_boltból: 142
- több_normalizált_vonalkód: 256

## Kimeneti fájlok

- `master_products.csv`
- `master_offers.csv`
- `match_edges.csv`
- `review_candidates.csv`

## Megjegyzés

Ez determinisztikus első verzió. A `review_candidates.csv` lista nem hibajegyzék, hanem azoknak a termékcsoportoknak a sora, ahol a vonalkód, név, kép vagy kiszerelés alapján további ellenőrzés indokolt.
