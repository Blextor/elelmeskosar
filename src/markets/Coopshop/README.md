# Coopshop

Coopshop (`coopshop.hu`) saját WooCommerce Store API alapú adatfolyam a
webshop élelmiszer kategóriáihoz.

## Szerepe

Ez a mappa a Coopshop élelmiszer jellegű kategóriáinak termékadatait tölti
le, szűri és alakítja át a többi bolt által is használt közös
`*_normalized_data_*.csv` sémára.

## Fontos eltérések

- A coopshop.hu WordPress/WooCommerce alapú oldal, ugyanazt a Store API-t
  használja, mint a CoopOnline (`Coop/`), de **külön bolt, külön katalógussal**
  (`store_name = Coopshop`).
- A kategóriák a `wp-json/wc/store/v1/products/categories` végpontról jönnek.
  A webshopnak sok kategóriája van (>200), ezért a letöltő **lapozva** kéri le
  őket (`per_page` + `page`, az `X-WP-TotalPages` fejléc alapján).
- A termékek a `wp-json/wc/store/v1/products` végpontról kérhetők le
  `category`, `per_page` és `page` paraméterekkel. Egy gyökérkategória
  lekérése a **teljes alfáját** visszaadja (a leszármazott kategóriák
  termékeit is), ezért elég a gyökereket lekérni, majd WooCommerce `id`
  alapján deduplikálni.
- Nincs egyetlen közös `élelmiszer` gyökér. Az alapértelmezett letöltés a
  három élelmiszer jellegű root kategóriát kéri le (lásd lent).
- A termék API-ban a `sku` a Coopshopnál jellemzően valódi GTIN/EAN. A
  normalizáló csak akkor tölti a `barcode` mezőt, ha az SKU 8, 12, 13 vagy 14
  jegyű és a GTIN checksum is érvényes.
- A `brands` mező a Coopshop API-ban általában üres, ezért a `brand_name`
  jellemzően üres marad — a márka a terméknévben szerepel.

## Alapértelmezett élelmiszer kategóriák

A `get_all_data_coopshop.py` alapból ezeket a root kategória slugokat tölti:

- `elelmiszer`
- `frissaru`
- `mirelit`

Más kategórialista a `--root-slugs` paraméterrel adható meg vesszővel
elválasztva.

## Kiszerelés és ár

A normalizáló elsődlegesen a terméknévből nyeri ki a kiszerelést, mert a
Coopshop `weight` és `formatted_weight` mezője jellemzően üres. A terméknév
parser kezeli a gramm, kilogramm, milliliter, liter, centiliter és darab
jelöléseket, valamint a `kapsz.`, `tabl.`, `tabletta` és `tasak`
darabszámokat is.

Az aktuális ár a WooCommerce `prices.price` mezőből jön. Ha a termék akciós,
és a `regular_price` nagyobb az aktuális árnál, akkor az eredeti ár az
`original_unit_price` mezőbe kerül.

Esetleges visszaváltási díj a Coopshop `price_html` mezőjében jelenne meg
(`+ 50Ft VISSZAVÁLTÁSI DÍJ` minta), ez a közös séma `secondary_unit_price`,
`secondary_unit_type = db`, `secondary_unit_step = 1` mezőibe kerül.

## Fájlok

- `main_coopshop.py`: a teljes Coopshop folyamat belépési pontja.
- `get_all_data_coopshop.py`: kategóriák és termékek letöltése WooCommerce
  Store API-ból (lapozott kategórialekéréssel).
- `filter_data_coopshop.py`: a nyers Coopshop CSV fontosabb oszlopainak
  megtartása.
- `normalize_data_coopshop.py`: Coopshop mezők átalakítása a közös 18 oszlopos
  `*_normalized_data_*.csv` sémára.
- `kategoriak.txt`: a legutóbb felfedezett és alapértelmezés szerint használt
  Coopshop élelmiszer kategóriafa.

## Kimenetek

A szkriptek a `data/markets_data/` mappába írnak:

- `coopshop_categories_*.csv`: friss Coopshop élelmiszer kategóriafa.
- `coopshop_all_data_*.csv`: nyers, deduplikált Coopshop termékadatok.
- `coopshop_failed_requests_*.csv`: sikertelen kategórialekérések.
- `coopshop_filtered_data_*.csv`: lényegesebb nyers oszlopokra szűkített CSV.
- `coopshop_normalized_data_*.csv`: a többi bolttal azonos közös kimeneti séma.

## Futtatás

```powershell
cd src\markets\Coopshop
python main_coopshop.py
```

Gyors próba:

```powershell
python get_all_data_coopshop.py --category-limit 1 --page-limit 1 --allow-partial-download
python filter_data_coopshop.py
python normalize_data_coopshop.py
```

Teljes alapértelmezett élelmiszer letöltés:

```powershell
python get_all_data_coopshop.py --allow-partial-download
python filter_data_coopshop.py
python normalize_data_coopshop.py
```
