# Spar

SPAR termékadatok lekérésének, szűrésének és normalizálásának fő mappája.

## Szerepe

Ez a projekt jelenlegi legfontosabb adatfolyama. A `main_spar.py` sorban futtatja a három lépést:

1. `get_all_data_spar.py`: induláskor frissíti a Wolt aktuális kategóriafáját, majd kategóriaslugok alapján letölti a termékeket a Wolt Consumer API-ból.
2. `filter_data_spar.py`: eltávolítja a nem használt oszlopokat.
3. `normalize_data_spar.py`: egységes terméksémára alakítja az adatokat.

## Fontos bemenetek és kimenetek

- `kategoriak.txt`: a lekérdezendő kategóriaslugok listája; a letöltő alapértelmezetten automatikusan frissíti az aktuális Wolt `assortment` alapján.
- `elírt termékek/`: kézi kivétellisták a kiszerelés-normalizáláshoz.
- `../../../data/markets_data/`: a generált CSV-k célmappája.

## Megjegyzés

A szkriptek relatív útvonalakat használnak, ezért ezt a mappát célszerű aktuális munkakönyvtárként használni futtatáskor.

## Hasznos opciók

- `python get_all_data_spar.py --refresh-categories-only`: csak a kategóriákat frissíti.
- `python get_all_data_spar.py --no-category-refresh`: explicit módon a meglévő `kategoriak.txt` alapján tölt le.
- `python get_all_data_spar.py --allow-stale-categories`: ha a kategóriafrissítés hibázik, engedi a helyi kategóriafájl használatát.
- `python get_all_data_spar.py --allow-partial-download`: engedi, hogy néhány sikertelen kategória mellett is all_data CSV készüljön.
- `python get_all_data_spar.py --venue-slug interspar-szentendre`: másik SPAR/Wolt venue lekérdezése.

Alapértelmezett teljes futásnál friss kategóriafa szükséges, és sikertelen kategórialekérés esetén a script nem ír hiányos `all_data` fájlt.
