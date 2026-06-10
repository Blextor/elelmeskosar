# Lidl

## Szerepe

Ez a mappa a Lidl magyar `Étel & ital` oldalának termékletöltését és közös
bolti CSV-sémára normalizálását tartalmazza.

## Adatforrás

- Kiinduló oldal: `https://www.lidl.hu/c/etel-ital/s10068374`
- Termékkereső API: `https://www.lidl.de/q/api/search`
- Fő kategóriaazonosító: `10068374`

A magyar Lidl oldal Nuxt konfigurációja a német Lidl search backendet használja
HU paraméterekkel (`locale=hu_HU`, `assortment=HU`). A közvetlen
`www.lidl.hu/q/api/search` hívás 401-et ad, ezért a script a konfigurációban
talált backend URL-t használja.

## Fájlok

- `get_all_data_lidl.py`: lapozva lekéri az összes terméket, deduplikálja őket
  Lidl termékkód alapján, majd frissíti a `kategoriak.txt` fájlt a termékek
  saját kategóriaútvonalaiból.
- `filter_data_lidl.py`: az all_data CSV-ből kiválogatja a normalizáláshoz
  szükséges mezőket.
- `normalize_data_lidl.py`: a Lidl mezőit a közös 18 oszlopos bolti sémára
  alakítja.
- `main_lidl.py`: egymás után futtatja a letöltést, szűrést és normalizálást.
- `kategoriak.txt`: futásonként frissülő kategóriafájl.

## Sajátosságok

- A Lidl API a nagy `fetchsize` értéket jelenleg 108-ra vágja vissza, ezért a
  letöltő a válaszban kapott tényleges `fetchsize` alapján lapoz.
- A publikus terméklistában nincs megbízható GTIN/EAN vonalkód. Az `ians` mező
  Lidl cikkszám jellegű adat, ezért nem kerül a `barcode` oszlopba.
- A kiszereléshez elsődlegesen a `price.basePrice.text` mezőt használjuk, nem a
  terméknevet.
- Néhány terméknél a Lidl kártya csak egy darab/egység mennyiségét írja ki,
  miközben az ár a teljes multipackra vonatkozik. Ilyenkor a normalizáló a
  termékár és a Lidl által megadott kg/l egységár alapján visszaszámolja a
  teljes kiszerelést.
- A Lidl Plus árak külön mezőben érkeznek. Ha a fő ármező üres, de Lidl Plus ár
  van, a normalizált árként ez kerül be, az eredeti ár pedig
  `original_unit_price` lesz.
- A betétdíj sok terméknél csak a HTML leírásban szerepel (`+50 Ft betétdíj`);
  ezt a normalizáló `secondary_unit_price` mezőként próbálja kinyerni.
- A Lidl saját `Étel & ital` oldala tartalmaz néhány nem szigorúan élelmiszer
  jellegű sort is, például virágot, állateledelt vagy baba kategóriás terméket.
  Ezeket a letöltő jelenleg nem szűri ki automatikusan, mert a forrásoldal részei.
- Maradhat néhány forrásoldali egységár-ellentmondás. Például előfordul, hogy a
  kiszerelés és a `1 kg = ... Ft` szöveg nem adja ki a termékárat. Ezeknél a
  normalizáló a stabilabb kiszerelési részre támaszkodik, nem írja át vakon
  irreális értékre.

## Futtatás

```powershell
cd src\markets\Lidl
python main_lidl.py
```
