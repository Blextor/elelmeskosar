# Auchan

Auchan saját webes adatfolyam az `auchan.hu/shop` Nuxt oldalához és az
`auchan.hu/api/v2` REST API-hoz.

## Szerepe

Ez a mappa az Auchan termékadatok letöltését, szűrését és az egységes piaci CSV
sémára normalizálását tartalmazza. Az Auchan nem Wolt-alapú és nem Tesco
GraphQL-alapú bolt, hanem saját REST API-t használ.

## Fontos eltérések

- A termékekhez anon token kell, amelyet a frontend a `/fe-api/get-token`
  végponton kér le.
- A kínálat kiszolgálási területhez kötött. A letöltő alapból az Auchan Soroksár
  áruházi átvételi pontot állítja be: `type=department_store`, `areaId=47`.
- A kategóriafa a `/api/v2/tree/0` végpontról jön.
- A terméklista a `/api/v2/products` végpontról jön, `categoryId`,
  `itemsPerPage` és `page` paraméterekkel.
- Az alapletöltés csak a valódi, `level > 0` levélkategóriákat kéri le. A
  `level = 0` promóciós gyűjtők, például a Bizalomkártyás és Kifutó termékek
  listái duplikáló gyűjtemények, és a terméklista végponton 404-et adnak.
- A letöltő termék+variáns alapján deduplikál.

## Hibakezelés

Az Auchan API néhány kategóriánál 100-as lapméretre 500-at ad, ezért a letöltő
kategóriánként kisebb lapméretekre vált vissza: `100`, `50`, `20`, `10`, `5`,
`1`. Ha 1-es lapméretnél is csak egy konkrét oldal hibázik, a többi terméket
megtartja, és a hibás oldalt `auchan_failed_categories_*.csv` fájlba írja.
Hibás levélkategóriánál megpróbálja a szülőkategóriát is lekérni, majd a
termékválasz `categoryId` mezője alapján visszaírja a valódi levélkategória
útvonalát.

A `main_auchan.py` emiatt alapból engedi a részleges mentést. A jelenlegi API
állapotban ez szükséges ahhoz, hogy a letölthető termékek ne vesszenek el egy
hibás Auchan oldal miatt.

## Kiszerelés és egységár

Az Auchan strukturált mezőket küld, ezért a normalizáló nem a terméknévre
támaszkodik elsődlegesen:

1. `selectedVariant.packageInfo.packageSize` és `packageUnit`.
2. Lédig terméknél `selectedVariant.loose.weightPerPiece`.
3. Kosár lépésköz: `selectedVariant.cartInfo.quantityStepSize`.
4. Terméknév parser csak végső tartalék.

Az `unit_price` mezőbe a termék bruttó aktuális ára kerül. A visszaváltási díj,
ha van, a közös séma `secondary_unit_price` mezőjébe kerül, hogy ne torzítsa az
alapár-összehasonlítást.

## Fájlok

- `main_auchan.py`: a teljes Auchan folyamat belépési pontja.
- `get_all_data_auchan.py`: anon token, delivery-area beállítás, kategóriák és
  termékek letöltése.
- `filter_data_auchan.py`: a nyers Auchan CSV fontosabb oszlopainak megtartása.
- `normalize_data_auchan.py`: Auchan mezők átalakítása a közös 18 oszlopos
  `*_normalized_data_*.csv` sémára.
- `kategoriak.txt`: a legutóbb felfedezett Auchan kategóriafa.

## Kimenetek

A szkriptek a `data/markets_data/` mappába írnak:

- `auchan_department_stores_*.csv`: áruházi átvételi pontok.
- `auchan_categories_*.csv`: friss Auchan kategóriafa.
- `auchan_all_data_*.csv`: nyers, lapozott REST termékadatok.
- `auchan_failed_categories_*.csv`: hibás vagy részlegesen hibás kategóriák.
- `auchan_filtered_data_*.csv`: lényegesebb nyers oszlopokra szűkített CSV.
- `auchan_normalized_data_*.csv`: SPAR/Príma/Tesco-val azonos kimeneti séma.

## Futtatás

```powershell
cd src\markets\Auchan
python main_auchan.py
```

Célzott kategória-újrapróbálás:

```powershell
python get_all_data_auchan.py --category-ids 6243,7269 --allow-partial-download
python filter_data_auchan.py
python normalize_data_auchan.py
```

Gyors próba:

```powershell
python get_all_data_auchan.py --category-limit 3 --page-limit 1 --page-delay 0 --category-delay 0 --allow-partial-download
python filter_data_auchan.py
python normalize_data_auchan.py
```
