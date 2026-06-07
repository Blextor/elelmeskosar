# Tesco adatstrukt?ra riport - 20260607_171937

## Snapshotok

- `tesco_fetch_categories_20260607_171936.csv`: 15 sor, 11 oszlop
- `tesco_categories_20260607_171937.csv`: 1717 sor, 8 oszlop
- `tesco_all_data_20260607_171937.csv`: 17937 sor, 37 oszlop
- `tesco_filtered_data_20260607_171937.csv`: 17937 sor, 34 oszlop
- `tesco_normalized_data_20260607_171937.csv`: 17937 sor, 18 oszlop

## ?sszevet?s SPAR/Pr?ma adatokkal

- `spar_all_data_20260607_021630.csv`: 7822 sor, 69 oszlop
- `prima_all_data_20260607_145253.csv`: 4297 sor, 69 oszlop
- `tesco_all_data_20260607_171937.csv`: 17937 sor, 37 oszlop
- `spar_normalized_data_20260607_021630.csv`: 7822 sor, 18 oszlop
- `prima_normalized_data_20260607_145253.csv`: 4297 sor, 18 oszlop
- `tesco_normalized_data_20260607_171937.csv`: 17937 sor, 18 oszlop

## Tesco normaliz?lt min?s?gellen?rz?s

- Vonalk?dos sorok: 17937 / 17937
- N?vvel rendelkez? sorok: 17937 / 17937
- Hi?nyz? `unit_price`: 0
- Hi?nyz? `unit_step`: 0
- Akci?sk?nt normaliz?lt sorok: 84
- `unit_type` eloszl?s: {'g': 7853, 'db': 4546, 'ml': 5538}

## Tesco nyers mez?szerkezet

- `price.unitOfMeasure` eloszl?s: {'kg': 7505, 'each': 5178, 'litre': 5192, 'metre': 62}
- `catchWeightList` sorok: 216
- `details.packSize.value` sorok: 0
- `details.netContents` sorok: 0
- Prom?ci?s objektummal rendelkez? sorok: 3205

## Kateg?riafa

- R?szletes Tesco kateg?ri?k sz?ma: 1717
- M?lys?g szerinti eloszl?s: {'0': 15, '1': 127, '2': 530, '3': 1045}
- A fetch-kateg?ri?k sz?ma 15; ezek a landing oldal egy szint? `browse/.../all` linkjei.

## Fontos elt?r?sek

- SPAR/Pr?ma Wolt-on j?n: `assortment/categories/slug/...`; Tesco saj?t GraphQL `category` queryt haszn?l.
- Wolt kateg?ri?kn?l a `slug` a let?lt?si kulcs; Tesco-n?l az ?kezetes kateg?ria?tvonal URL-encode + base64 alakja a `facet`.
- Wolt ?rak fill?r/cent jelleg? integer mez?k, a normaliz?l? /100-at haszn?l; Tesco `price.actual` ?s `price.unitPrice` m?r forintban van.
- Wolt `unit_info` sokszor k?zvetlen kiszerel?st ad; Tesco-n?l ez gyakran hi?nyzik, ez?rt `catchWeightList`, c?m/parsing ?s `actual/unitPrice` ar?ny kell.
- Tesco kateg?ria?tvonal 4 n?vmez?b?l ?ll, nem egyetlen slugb?l: `superDepartmentName|departmentName|aisleName|shelfName`.
