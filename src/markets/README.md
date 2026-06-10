# markets

Boltonként rendezett adatgyűjtő és feldolgozó kódok mappája.

## Szerepe

Az itt lévő almappák egy-egy kereskedőhöz tartozó lekérő, szűrő és normalizáló
logikát tartalmaznak. A cél, hogy a boltok eltérő API-válaszai végül azonos
felépítésű `*_normalized_data_*.csv` fájlokba kerüljenek.

## Almappák

- `Spar/`: SPAR/Wolt API alapú adatfolyam.
- `Prima/`: Príma/Wolt API alapú adatfolyam.
- `Tesco/`: Tesco saját GraphQL/API alapú adatfolyam.
- `Auchan/`: Auchan saját Nuxt/REST API alapú adatfolyam.
- `Metro/`: Metro saját search/evaluate API alapú, élelmiszerre szűrt
  adatfolyam.
- `Coop/`: CoopOnline WooCommerce Store API alapú, élelmiszerre szűrt
  adatfolyam.
- `Lidl/`: Lidl saját search API alapú, `Étel & ital` kategóriából induló
  adatfolyam.
- `Penny/`: Penny/Roksh shopservice API alapú adatfolyam.
- `Aldi/`: Aldi/Roksh shopservice API alapú adatfolyam.

## Közös feldolgozók

- `build_promotions.py`: a legfrissebb bolti normalizált és promóciós forrás
  CSV-kből közös `promotions_*.csv` táblát és promócióhivatkozással bővített
  `offers_with_promotions_*.csv` ajánlattáblát épít.

## Közös kimeneti séma

A normalizált bolti CSV-k 18 oszlopos közös sémát használnak:

`store_name`, `store_product_id`, `product_name`, `brand_name`, `available`,
`expected_restock`, `barcode`, `unit_price`, `unit_type`, `unit_step`,
`is_discounted`, `original_unit_price`, `secondary_unit_price`,
`secondary_unit_type`, `secondary_unit_step`, `image_urls`, `description`,
`categories`.

Az akciók részletesebb kezeléséhez a normalizált sorokban lévő
`is_discounted` és `original_unit_price` csak alap jelzés. A többféle
kedvezménytípus, hűségprogram és mennyiségi ársáv a külön `promotions_*.csv`
táblába kerül:

```powershell
python src\markets\build_promotions.py
```
