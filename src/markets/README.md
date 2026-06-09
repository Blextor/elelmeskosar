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

## Közös kimeneti séma

A normalizált bolti CSV-k 18 oszlopos közös sémát használnak:

`store_name`, `store_product_id`, `product_name`, `brand_name`, `available`,
`expected_restock`, `barcode`, `unit_price`, `unit_type`, `unit_step`,
`is_discounted`, `original_unit_price`, `secondary_unit_price`,
`secondary_unit_type`, `secondary_unit_step`, `image_urls`, `description`,
`categories`.
