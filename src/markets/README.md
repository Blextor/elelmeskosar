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
- `Coopshop/`: Coopshop (coopshop.hu) WooCommerce Store API alapú,
  élelmiszerre szűrt adatfolyam.
- `Lidl/`: Lidl saját search API alapú, `Étel & ital` kategóriából induló
  adatfolyam.
- `Penny/`: Penny/Roksh shopservice API alapú adatfolyam.
- `Aldi/`: Aldi/Roksh shopservice API alapú adatfolyam.

## Közös feldolgozók

- `build_promotions.py`: a legfrissebb bolti normalizált és promóciós forrás
  CSV-kből közös `promotions_*.csv` táblát és promócióhivatkozással bővített
  `offers_with_promotions_*.csv` ajánlattáblát épít.
- `download_product_images.py`: a normalizált CSV-k `image_urls` mezője
  alapján inkrementálisan letölti a termékképeket a
  `data/markets_data/product_images/<bolt>/` mappába. A fájlnév az URL
  SHA1-kivonata, így változatlan URL-t soha nem tölt le újra, képcsere
  (új URL) esetén viszont automatikusan frissül. Futás után a legfrissebb
  normalizált CSV-be `local_image_paths` oszlopot ír a helyi útvonalakkal,
  és `<bolt>_image_index_*.csv` nyilvántartást készít. Minden bolti
  `main_*.py` lánc utolsó lépésként meghívja a saját boltjára, így a képek a
  termékadat-frissítéssel együtt frissülnek. Alapból termékenként az első
  (elsődleges) képet tölti; `--max-per-product 0` esetén az összeset.

## Közös kimeneti séma

A normalizált bolti CSV-k 18 oszlopos közös sémát használnak:

`store_name`, `store_product_id`, `product_name`, `brand_name`, `available`,
`expected_restock`, `barcode`, `unit_price`, `unit_type`, `unit_step`,
`is_discounted`, `original_unit_price`, `secondary_unit_price`,
`secondary_unit_type`, `secondary_unit_step`, `image_urls`, `description`,
`categories`.

A `download_product_images.py` futása után a legfrissebb normalizált CSV-k
egy opcionális 19. oszlopot is kapnak: `local_image_paths` — a letöltött
termékképek repo-relatív helyi útvonalai `;`-vel elválasztva.

Az akciók részletesebb kezeléséhez a normalizált sorokban lévő
`is_discounted` és `original_unit_price` csak alap jelzés. A többféle
kedvezménytípus, hűségprogram és mennyiségi ársáv a külön `promotions_*.csv`
táblába kerül:

```powershell
python src\markets\build_promotions.py
```
