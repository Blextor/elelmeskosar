# scripts

Termékadat-elemző Python szkriptek mappája.

## Szerepe

Az itt lévő szkriptek meglévő bolti snapshotokat hasonlítanak össze terméknév,
vonalkód, képlink, kategória, kiszerelés és ár alapján. A mappa célja, hogy a
letöltött adatokból ellenőrizhető riportok és később felhasználható köztes
táblák készüljenek.

## Fontos fájlok

- `analisis_term_valtozasok.py`: termékkészlet- és mezőváltozások áttekintése.
- `analizis_azonositok.py`: azonosítók megbízhatóságának vizsgálata.
- `analizis_konfliktusok.py`: részletes konfliktuslisták előállítása.
- `build_master_products.py`: SPAR, Príma és Tesco normalizált CSV-kből
  mestertermék- és bolti ajánlat táblák építése.

## Mestertermék futtatása

```powershell
python analysis\scripts\build_master_products.py
```

A kimenet az `analysis/reports/master_products_*` mappába kerül:

- `master_products.csv`
- `master_offers.csv`
- `match_edges.csv`
- `review_candidates.csv`
- `summary.md`
