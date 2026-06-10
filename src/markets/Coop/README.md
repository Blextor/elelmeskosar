# Coop

CoopOnline saját WooCommerce Store API alapú adatfolyam a
`cooponline.hu/termekeink/` katalógushoz.

## Szerepe

Ez a mappa a CoopOnline élelmiszer jellegű kategóriáinak termékadatait tölti
le, szűri és alakítja át a többi bolt által is használt közös
`*_normalized_data_*.csv` sémára.

## Fontos eltérések

- A CoopOnline WordPress/WooCommerce alapú oldal.
- A kategóriák a `wp-json/wc/store/v1/products/categories` végpontról jönnek.
- A termékek a `wp-json/wc/store/v1/products` végpontról kérhetők le
  `category`, `per_page` és `page` paraméterekkel.
- Nincs egyetlen közös `élelmiszer` gyökér. Az alapértelmezett letöltés több
  élelmiszer jellegű root kategóriát kér le, majd WooCommerce `id` alapján
  deduplikál.
- A termék API-ban a `sku` vegyes: néhány terméknél valódi GTIN/EAN, máshol
  Coop belső cikkszámnak tűnik. A normalizáló csak akkor tölti a `barcode`
  mezőt, ha az SKU 8, 12, 13 vagy 14 jegyű és a GTIN checksum is érvényes.

## Alapértelmezett élelmiszer kategóriák

A `get_all_data_coop.py` alapból ezeket a root kategória slugokat tölti:

- `ital`
- `edesseg-nassolni-valo`
- `konzerv`
- `tartos-elelmiszer`
- `teszta`
- `sutes-fozes`
- `sajtok-vajak-margarinok`
- `szalamik-kolbaszok`
- `zoldseg-gyumolcs-tojas`
- `fuszer`
- `kenyer-peksutemeny`
- `egeszseges-eletmod`
- `teak-es-mezek`

Más kategórialista a `--root-slugs` paraméterrel adható meg vesszővel
elválasztva.

## Kiszerelés és ár

A normalizáló elsődlegesen a terméknévből nyeri ki a kiszerelést, mert a Coop
`weight` és `formatted_weight` mezője sokszor szállítási súlynak tűnik. A
terméknév parser kezeli a gramm, kilogramm, milliliter, liter, centiliter és
darab jelöléseket, valamint a `kapsz.`, `tabl.`, `tabletta` és `tasak`
darabszámokat is.

Az aktuális ár a WooCommerce `prices.price` mezőből jön. Ha a termék akciós,
és a `regular_price` nagyobb az aktuális árnál, akkor az eredeti ár az
`original_unit_price` mezőbe kerül.

A visszaváltási díj a Coop `price_html` mezőjében jelenik meg, például
`+ 50Ft VISSZAVÁLTÁSI DÍJ PET`. Ez a közös séma `secondary_unit_price`,
`secondary_unit_type = db`, `secondary_unit_step = 1` mezőibe kerül.

## Fájlok

- `main_coop.py`: a teljes Coop folyamat belépési pontja.
- `get_all_data_coop.py`: kategóriák és termékek letöltése WooCommerce Store
  API-ból.
- `filter_data_coop.py`: a nyers Coop CSV fontosabb oszlopainak megtartása.
- `normalize_data_coop.py`: Coop mezők átalakítása a közös 18 oszlopos
  `*_normalized_data_*.csv` sémára.
- `kategoriak.txt`: a legutóbb felfedezett és alapértelmezés szerint használt
  Coop élelmiszer kategóriafa.

## Kimenetek

A szkriptek a `data/markets_data/` mappába írnak:

- `coop_categories_*.csv`: friss Coop élelmiszer kategóriafa.
- `coop_all_data_*.csv`: nyers, deduplikált Coop termékadatok.
- `coop_failed_requests_*.csv`: sikertelen kategórialekérések.
- `coop_filtered_data_*.csv`: lényegesebb nyers oszlopokra szűkített CSV.
- `coop_normalized_data_*.csv`: a többi bolttal azonos közös kimeneti séma.

## Futtatás

```powershell
cd src\markets\Coop
python main_coop.py
```

Gyors próba:

```powershell
python get_all_data_coop.py --category-limit 2 --page-limit 1 --allow-partial-download
python filter_data_coop.py
python normalize_data_coop.py
```

Teljes alapértelmezett élelmiszer letöltés:

```powershell
python get_all_data_coop.py --allow-partial-download
python filter_data_coop.py
python normalize_data_coop.py
```
