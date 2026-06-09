# Adatminőségi audit - SPAR, Príma, Tesco

## Vizsgált fájlok

- Spar: `spar_normalized_data_20260607_021630.csv`
- Prima: `prima_normalized_data_20260607_145253.csv`
- Tesco: `tesco_normalized_data_20260607_171937.csv`

## Gyors összkép

- Spar: 7822 sor; hiányzó vonalkód 545; hard error sor 1; duplikált név kulcs
  28; duplikált vonalkód kulcs 0.
- Prima: 4297 sor; hiányzó vonalkód 32; hard error sor 0; duplikált név kulcs
  13; duplikált vonalkód kulcs 0.
- Tesco: 17937 sor; hiányzó vonalkód 0; hard error sor 0; duplikált név kulcs
  117; duplikált vonalkód kulcs 0.

## Fő megállapítások

- Hard error sor: 1. Ezek hiányzó vagy érvénytelen ár, kiszerelés vagy
  egységtípus jellegű hibák.
- Multipack/kiszerelés név alapján gyanús sor: 35. Ebből SPAR 26, Príma 6,
  Tesco 3.
- Tesco `unitPrice` alapján számolt kiszerelés és normalizált kiszerelés között
  2x feletti konfliktus: 345 sor. Ezek nem mind biztos hibák, mert van
  drained-weight és pultos/catch-weight logika, de a lista több egyértelmű
  címhibát tartalmaz.
- Vonalkód+név alapján 200% feletti boltközi alapár-spread: 8 sor. Ezek között
  sok valós outlier helyett kiszerelési vagy parsing hiba van.

## Kiemelt konkrét hibagyanúk

- SPAR: `Zewa Softis Original ... 10 x 9 db` 10 db-ra normalizálódott, Tesco
  ugyanazt 90 db-ra hozza. Ez SPAR kiszerelés-parser hiba.
- SPAR/Príma: `Pöttyös Óriás Túró Rudi ... 6 x 51 g (306 g)` 51 g-ra
  normalizálódott. Csomagként 306 g lenne, így az alapár hatszorosára torzul.
- Tesco: több címben hiányzik tizedes vagy nulla: `BB ... 75 l`,
  `Alpro ... 40 g`, `Old Spice ... 2 ml`, `Pedigree ... 1440 kg`. A részletes
  Tesco API ezeknél sokszor reálisabb kiszerelést ad.
- Tesco/SPAR: `Old Spice Tomorrowland ... 2 ml` mindkét boltban gyanús címadat;
  valószínűleg 200 ml vagy más nagyobb kiszerelés.
- SPAR/Príma: több tonhal/konzerv terméknél a név szerinti nettó tömeg és a
  normalizált vagy drained tömeg eltér. Ez lehet szándékos egységár-logika, de
  összehasonlításnál jelölni kell.

## Mentett részletes listák

- `hard_errors.csv`
- `duplicates_summary.csv`
- `multipack_mismatches.csv`
- `base_price_outliers.csv`
- `tesco_unitprice_step_conflicts.csv`
- `cross_store_extreme_spreads_barcode_name.csv`
- `summary.json`
