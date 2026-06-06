# Spar

SPAR termékadatok lekérésének, szűrésének és normalizálásának fő mappája.

## Szerepe

Ez a projekt jelenlegi legfontosabb adatfolyama. A `main_spar.py` sorban futtatja a három lépést:

1. `get_all_data_spar.py`: kategóriaslugok alapján letölti a termékeket a Wolt Consumer API-ból.
2. `filter_data_spar.py`: eltávolítja a nem használt oszlopokat.
3. `normalize_data_spar.py`: egységes terméksémára alakítja az adatokat.

## Fontos bemenetek és kimenetek

- `kategoriak.txt`: a lekérdezendő kategóriaslugok listája.
- `elírt termékek/`: kézi kivétellisták a kiszerelés-normalizáláshoz.
- `../../../data/markets_data/`: a generált CSV-k célmappája.

## Megjegyzés

A szkriptek relatív útvonalakat használnak, ezért ezt a mappát célszerű aktuális munkakönyvtárként használni futtatáskor.
