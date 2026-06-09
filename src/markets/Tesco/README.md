# Tesco

Tesco saját webes adatfolyam a `bevasarlas.tesco.hu` és `xapi.tesco.com`
GraphQL végpontjaihoz.

## Szerepe

Ez a mappa a Tesco termékadatok letöltését, szűrését és az egységes piaci CSV
sémára normalizálását tartalmazza. A Tesco nem Wolt-alapú bolt, ezért a
SPAR/Príma letöltőktől eltérően működik:

- a fő kategóriák a Tesco landing oldal aktuális `browse/.../all` linkjeiből
  frissülnek;
- a terméklista GraphQL `category` lekérdezésen keresztül jön;
- a `facet` érték az ékezetes kategóriaútvonal URL-encode + base64 alakja;
- a részletes kategóriafa a termékekben lévő
  `superDepartmentName / departmentName / aisleName / shelfName` mezőkből épül;
- az árak már forintban érkeznek, nem filléres vagy centes formátumban;
- a lédig és catch-weight termékeknél a kosárba tehető alaplépés gyakran a
  `catchWeightList` mezőből vagy az `price.actual / price.unitPrice` arányból
  számolható.

## Kiszerelés normalizálása

A Tesco esetén nem szabad csak a terméknévre támaszkodni, mert a címben néha
hibás vagy félrevezető kiszerelés jelenik meg. A normalizáló sorrendje:

1. `catchWeightList`: változó súlyú vagy lédig termékek.
2. `details.packSize`: a terméklista GraphQL válasz strukturált kiszerelése.
3. `details.netContents`, `details.drainedWeight`, `details.boxContents`:
   részletes termékadatból származó mennyiségek, ha vannak.
4. `price.actual / price.unitPrice`: egységárból visszaszámolt kiszerelés.
5. Terméknév parser: csak végső tartalék.

A terméklista alap GraphQL válasza már tartalmazza a fontosabb `details.*`
mezőket, ezért a `main_tesco.py` alapból nem indít külön részletes lekérést
minden termékre. A teljes termékoldali gazdagítás opcionális, és sokkal lassabb,
mert termékenként külön GraphQL kérést küld.

## Fájlok

- `main_tesco.py`: a teljes Tesco folyamat belépési pontja.
- `get_all_data_tesco.py`: aktuális kategóriák és termékek letöltése, opcionális
  részletes termékadat-gazdagítással.
- `filter_data_tesco.py`: a nyers Tesco CSV fontosabb oszlopainak megtartása.
- `normalize_data_tesco.py`: Tesco mezők átalakítása a közös 18 oszlopos
  `*_normalized_data_*.csv` sémára.
- `kategoriak.txt`: a legutóbb felfedezett Tesco fő fetch-kategóriák.

## Kimenetek

A szkriptek a `data/markets_data/` mappába írnak:

- `tesco_fetch_categories_*.csv`: a landing oldalról felfedezett fő
  fetch-kategóriák.
- `tesco_categories_*.csv`: a letöltött termékekből újraépített részletes
  kategóriafa.
- `tesco_all_data_*.csv`: nyers, lapozott GraphQL termékadatok.
- `tesco_filtered_data_*.csv`: lényegesebb nyers oszlopokra szűkített CSV.
- `tesco_normalized_data_*.csv`: SPAR/Príma/Auchan boltokkal azonos kimeneti
  séma.

## Futtatás

Alap, gyorsabb teljes futás:

```powershell
cd src\markets\Tesco
python main_tesco.py
```

Opcionális, részletes termékoldali gazdagítás:

```powershell
python get_all_data_tesco.py --enrich-product-details --allow-partial-download
python filter_data_tesco.py
python normalize_data_tesco.py
```

Gyors próba egy-két kategóriával:

```powershell
python get_all_data_tesco.py --category-limit 2 --page-limit 1
python filter_data_tesco.py
python normalize_data_tesco.py
```
