# markets_data

Időbélyeggel ellátott piaci termékadatok tárolója.

## Szerepe

Itt találhatók a SPAR adatfolyam különböző feldolgozási állapotai:

- `spar_all_data_*.csv`: nyers, API-ból összegyűjtött adatok.
- `spar_filtered_data_*.csv`: a kevésbé fontos oszlopoktól megtisztított adatok.
- `spar_normalized_data_*.csv`: egységes mezősémára alakított termékadatok.
- `prima_all_data_*.csv`: Prima nyers, API-ból összegyűjtött adatok.
- `prima_filtered_data_*.csv`: Prima szűrt adatok.
- `prima_normalized_data_*.csv`: Prima egységes mezősémára alakított termékadatok.

## Megjegyzés

A fájlnevekben lévő dátum/idő a futtatás időpontját jelöli, ezért ezek snapshotként kezelendők.
