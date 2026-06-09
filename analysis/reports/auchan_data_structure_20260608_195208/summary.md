# Auchan adatstruktúra és letöltési riport

Futtatás időpontja: `2026-06-08 19:52:08`

## Kimeneti fájlok

- `data/markets_data/auchan_department_stores_20260608_193238.csv`
- `data/markets_data/auchan_categories_20260608_193239.csv`
- `data/markets_data/auchan_all_data_20260608_195208.csv`
- `data/markets_data/auchan_failed_categories_20260608_195208.csv`
- `data/markets_data/auchan_filtered_data_20260608_195208.csv`
- `data/markets_data/auchan_normalized_data_20260608_195208.csv`

## Felfedezett Auchan API

- Shop oldal: `https://auchan.hu/shop`
- Anon token: `POST https://auchan.hu/fe-api/get-token`, payload:
  `{"grant_type":"anonymous"}`
- Kiszolgálási terület: `POST https://auchan.hu/api/v2/delivery-area`, alap:
  `{"type":"department_store","areaId":47}`
- Átvételi pontok: `GET https://auchan.hu/api/v2/department_stores`
- Kategóriafa: `GET https://auchan.hu/api/v2/tree/0`
- Terméklista: `GET https://auchan.hu/api/v2/products?categoryId=...&itemsPerPage=...&page=...`

## Kategóriafa

| Mutató | Érték |
| --- | ---: |
| Összes kategória sor | 1 775 |
| Gyökér `productCount` | 36 811 |
| Terméket tartalmazó levélkategória | 1 384 |
| Valódi, `level > 0` levélkategória | 1 379 |
| `level = 0` promóciós gyűjtő | 5 |
| Valódi levélkategóriák `product_count` összege | 26 050 |

A `level = 0` promóciós gyűjtők nem kerülnek az alapletöltésbe:
`OkAuchan ajánlatok`, `Bizalomkártyás ajánlatok`, `Kiemelt ajánlatok`,
`Új a kínálatunkban`, `Kifutó termékek`. Ezek duplikáló listák, és a
terméklista végponton `categoryId` alapján 404-et adnak.

## Letöltési eredmény

| Mutató | Érték |
| --- | ---: |
| Lekért valódi levélkategória | 1 379 |
| Nyers termék/variáns sor | 25 372 |
| Szűrt sor | 25 372 |
| Normalizált sor | 25 372 |
| Hiányzó terméknév | 0 |
| Hiányzó vonalkód | 1 |
| Hiányzó ár | 0 |
| Hiányzó kiszerelés | 0 |
| Hiányzó kép | 13 |

A szülőkategória fallback két terméket visszanyert a hibás
`Zsírszegény, sovány túró` levélkategóriából:

- `5998202942967`: Nádudvari Fitness sovány túró 250 g
- `5998202940277`: Nádudvari zsírszegény túró 250 g

## Megmaradt API-hibák

| Kategória | Státusz | Megjegyzés |
| --- | --- | --- |
| `6243` Natúr és görög joghurt | részleges | 1-es lapméretnél a 16. oldal 500-at ad |
| `5669` Joghurtok fallback | részleges | 1-es lapméretnél az 52. oldal 500-at ad |
| `6551` Zsírszegény, sovány túró | sikertelen | 1-es lapméretnél az első oldal 500-at ad |
| `5677` Túró, tejszín fallback | részleges | 1-es lapméretnél a 9. oldal 500-at ad |
| `7269` Hűtött tejtermékek- joghurt, kefir, vaj | részleges | 1-es lapméretnél a 40. oldal 500-at ad |
| `5595` Laktózmentes termékek fallback | részleges | 1-es lapméretnél a 70. oldal 500-at ad |

Ezek az Auchan API oldalhibái. A letöltő a többi oldalt megtartja, a hibás
oldalakat `auchan_failed_categories_*.csv` fájlban naplózza.

## Normalizált sémák összevetése

Mind a négy bolt ugyanazt a 18 oszlopos normalizált sémát használja.

| Bolt | Sor | Hiányzó vonalkód | Hiányzó kép | Fő egységtípusok |
| --- | ---: | ---: | ---: | --- |
| SPAR | 7 822 | 545 | 8 | `g`, `ml`, `db` |
| Príma | 4 297 | 32 | 4 | `g`, `ml`, `db` |
| Tesco | 17 937 | 0 | 0 | `g`, `ml`, `db` |
| Auchan | 25 372 | 1 | 13 | `db`, `g`, `ml`, `m`, `m2` |

Auchan egységtípus eloszlás:

- `db`: 11 917
- `g`: 8 363
- `ml`: 5 007
- `m`: 76
- `m2`: 9

## Adatszerkezeti eltérések

- SPAR és Príma Wolt-alapú. A kategória és termékadatok Wolt venue/catalog
  válaszokból jönnek, a két bolt szerkezete nagyon hasonló.
- Tesco saját GraphQL/API folyamat. A kategóriafa és a termék részletei külön
  lekérdezésekből állnak össze, a vonalkód kitöltöttsége jelenleg teljes.
- Auchan saját Nuxt/REST folyamat. A termék a `selectedVariant` alatt hordozza a
  legtöbb árat, képet, kiszerelést és kosárinformációt.
- Auchannál a kínálat területfüggő, ezért a `delivery-area` beállítás kötelező.
- Auchannál több nem élelmiszer egység is van (`m`, `m2`), ezt a későbbi master
  termék párosításban kezelni kell.

## Kiszerelés és ár

Auchannál a kiszerelés elsődleges forrása strukturált:
`selectedVariant.packageInfo.packageSize` és `packageUnit`. A friss auditban ez
minden sorban kitöltött volt. Emiatt az Auchan normalizálás nem támaszkodik
elsődlegesen a névre.

A normalizált `unit_price` mező a termék aktuális bruttó ára, a `unit_step` és
`unit_type` mezők pedig a kiszerelést írják le. Az összehasonlítható kg/l/db ár
ebből számítható. Az Auchan nyers válaszában külön szerepel a bolti
`selectedVariant.packageInfo.unitPrice.grossDiscounted` is, ezt auditálási
referenciaként érdemes megtartani.

A visszaváltási díj az Auchan válaszában `selectedVariant.roll` alatt jön. Ez a
normalizált CSV-ben a `secondary_unit_price`, `secondary_unit_type` és
`secondary_unit_step` mezőkbe kerül. A 25 372 sorból 1 803 sorban volt ilyen
másodlagos díj.
