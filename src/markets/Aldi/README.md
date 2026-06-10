# Aldi

Roksh alapú Aldi adatfolyam a `https://www.roksh.com/aldi/kezdooldal`
oldalhoz.

## Szerepe

Ez a mappa az Aldi kategóriáit és termékeit tölti le a Roksh `shopservice`
API-jából, majd a többi bolttal azonos, 18 oszlopos
`*_normalized_data_*.csv` sémára alakítja. A folyamat a Penny adatfolyammal
azonos felépítésű, mert mindkét bolt a Roksh platformon fut.

## Fontos eltérések

- A publikus oldal Angular alkalmazás, a termékek nem a HTML-ben vannak.
- A kategóriák a `category/GetFullCategoryList` végpontról jönnek.
- Az Aldi provider azonosítóit a `session/configure` hívás adja vissza:
  `provider_code = ALDI`, `provider_id = 13`.
- A termékek a `productlist/GetProductList` végpontról kérhetők le
  kategória `ProgID`, oldal és oldalméret alapján.
- A Roksh válaszban a terméklista már sok részletes adatot tartalmaz
  (összetevők, tápérték, képek, betétdíj), ezért külön termékadatlap-hívásra
  alapértelmezés szerint nincs szükség.
- A próbák alapján nincs publikus EAN/GTIN/vonalkód mező. A normalizáló csak
  akkor tölti a `barcode` mezőt, ha később mégis talál érvényes GTIN mezőt.

## Kategóriák

Az alapértelmezett letöltés a Roksh által visszaadott teljes Aldi kategóriafát
frissíti, majd a fő kategóriákon keresztül tölti le a termékeket
`ChildrenCategoryProductsNeeded=true` paraméterrel. Ez sokkal kevesebb API-hívás,
mint az összes levélkategória külön lekérése, de a terméksorokban továbbra is a
válaszban szereplő tényleges levélkategória kerül mentésre. A `kategoriak.txt`
minden futáskor újraírásra kerül, és a `data/markets_data/` mappába külön
`aldi_categories_*.csv` pillanatkép is készül.

Gyors próba egy-két kategóriával:

```powershell
python get_all_data_aldi.py --category-prog-ids tejtermek-tojas,pekaru --allow-partial-download --verbose
```

Ha valamiért levélkategóriánként kell végigmenni:

```powershell
python get_all_data_aldi.py --fetch-mode leaf --allow-partial-download --verbose
```

## Kiszerelés és ár

A normalizáló elsődlegesen nem a terméknévből dolgozik. A csomagméretet először
a Roksh által küldött termékárból és kg/l/db egységárból számolja vissza:

```text
unit_step = price / unitPrice * kg_vagy_liter_alap
```

Így például egy 200 g-os sajt vagy egy 1,5 l-es ital esetében a kilós/literes
összehasonlítás nem a névben szereplő szövegre támaszkodik. Ha az egységárból
nem számolható ki a kiszerelés, akkor a `productProvider.packageQuantity` és
végül a terméknév a fallback.

A betétdíj a Roksh `depositFee` mezőjéből kerül a közös séma
`secondary_unit_price`, `secondary_unit_type = db`, `secondary_unit_step = 1`
mezőibe.

## Fájlok

- `main_aldi.py`: a teljes Aldi folyamat belépési pontja.
- `get_all_data_aldi.py`: session, kategóriafa és termékek letöltése a Roksh
  API-ból.
- `filter_data_aldi.py`: a nyers Aldi CSV fontosabb oszlopainak megtartása.
- `normalize_data_aldi.py`: Aldi/Roksh mezők átalakítása a közös 18 oszlopos
  sémára.
- `validate_data_aldi.py`: kiszerelési ellentmondások keresése az Aldi
  `filtered_data` fájlban.
- `kategoriak.txt`: a legutóbb felfedezett Aldi kategóriafa.

## Kimenetek

A szkriptek a `data/markets_data/` mappába írnak:

- `aldi_categories_*.csv`: friss Aldi kategóriafa.
- `aldi_all_data_*.csv`: nyers, deduplikált Aldi termékadatok.
- `aldi_failed_requests_*.csv`: sikertelen kategórialekérdezések, ha voltak.
- `aldi_filtered_data_*.csv`: lényegesebb nyers oszlopokra szűkített CSV.
- `aldi_normalized_data_*.csv`: a többi bolttal azonos közös kimeneti séma.
- `aldi_package_anomalies_*.csv`: kiszerelési ellenőrző riport.

## Futtatás

```powershell
cd src\markets\Aldi
python main_aldi.py
```

Részletesebb futtatás:

```powershell
python get_all_data_aldi.py --allow-partial-download --verbose
python filter_data_aldi.py
python normalize_data_aldi.py
python validate_data_aldi.py
```
