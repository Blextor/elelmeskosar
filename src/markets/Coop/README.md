# Coop

A CoopOnline nyilvános UNAS-katalógusának letöltője a
`https://www.cooponline.hu/sct/0/` kategórialistához.

## Szerepe

Ez a mappa a CoopOnline élelmiszer jellegű kategóriáinak termékadatait tölti
le, szűri és alakítja át a többi bolt által is használt közös
`*_normalized_data_*.csv` sémára.

## Fontos eltérések

- A letöltő a kiválasztott főkategóriák alkategóriáit és a terméklisták
  következő oldalra mutató hivatkozásait járja be.
- A termékkártyáról olvassa a nevet, a cikkszámot, a vételárat, az áthúzott
  árat, a készletjelzést és a képet. Az ugyanazon cikkszámon több kategóriában
  szereplő termék egy sorba kerül, az összes megtalált kategóriaútvonallal.
- A `--product-details` kapcsolóval a letöltő az egyedi termékoldalakat is
  bejárja, ami cikkszámonként egy további lekérés. A strukturált termékadatokat a
  nyers CSV `product_schema` mezője őrzi meg. A feltüntetett visszaváltási
  díjat a `deposit_fee_huf` oszlop tartalmazza, és a normalizált CSV-ben
  külön tételként szerepel. A közölt termékleírás és márka is átkerül.
- A `store_product_id` értéke `unas:<cikkszám>`. A korábbi WooCommerce
  termékazonosítóktól eltér. A két forrás nyers fájljaiban a `sku` oszlop
  használható a közös cikkszámok azonosítására.
- A korábbi WooCommerce adatfolyam egy explicit `--api-base URL` paraméterrel
  futtatható kompatibilis forráson. A történeti CSV-k továbbra is feldolgozhatók.

## Alapértelmezett élelmiszer kategóriák

A `get_all_data_coop.py` alapból ezeket a root kategória slugokat tölti:

- `ital`
- `edesseg-nassolni-valo`
- `konzerv`
- `tartos-elelmiszer`
- `teszta`
- `sutes-fozes`
- `zoldseg-gyumolcs-tojas`
- `fuszer`
- `kenyer-peksutemeny`
- `egeszseges-eletmod`

Más kategórialista a `--root-slugs` paraméterrel adható meg vesszővel
elválasztva.

## Kiszerelés és ár

A normalizáló elsődlegesen a terméknévből nyeri ki a kiszerelést, mert a Coop
`weight` és `formatted_weight` mezője sokszor szállítási súlynak tűnik. A
terméknév parser kezeli a gramm, kilogramm, milliliter, liter, centiliter és
darab jelöléseket, valamint a `kapsz.`, `tabl.`, `tabletta` és `tasak`
darabszámokat is.

Az aktuális ár a nyers CSV `prices.price` mezőjéből jön. Ha a termék akciós,
és a `regular_price` nagyobb az aktuális árnál, akkor az eredeti ár az
`original_unit_price` mezőbe kerül.

A korábbi WooCommerce-forrásban a visszaváltási díj a `price_html` mezőben jelenik meg, például
`+ 50Ft VISSZAVÁLTÁSI DÍJ PET`. Ez a közös séma `secondary_unit_price`,
`secondary_unit_type = db`, `secondary_unit_step = 1` mezőibe kerül.

## Fájlok

- `main_coop.py`: a teljes Coop folyamat belépési pontja.
- `get_all_data_coop.py`: kategóriák és termékek letöltése a katalógusból.
- `filter_data_coop.py`: a nyers Coop CSV fontosabb oszlopainak megtartása.
- `normalize_data_coop.py`: Coop mezők átalakítása a közös 18 oszlopos
  `*_normalized_data_*.csv` sémára.
- `kategoriak.txt`: a legutóbb felfedezett és alapértelmezés szerint használt
  Coop élelmiszer kategóriafa.

## Kimenetek

A szkriptek a `data/markets_data/` mappába írnak:

- `coop_categories_*.csv`: friss Coop élelmiszer kategóriafa.
- `coop_all_data_*.csv`: nyers, deduplikált Coop termékadatok.
- `coop_failed_requests_*.csv`: sikertelen kategória- és termékoldal-lekérések.
- `coop_filtered_data_*.csv`: lényegesebb nyers oszlopokra szűkített CSV.
- `coop_normalized_data_*.csv`: a többi bolttal azonos közös kimeneti séma.

## Futtatás

```powershell
cd src\markets\Coop
python -m pip install requests pandas beautifulsoup4
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
