# Letöltési és feldolgozási futásidők

Mérés időpontja: `2026-06-08` késő este / `2026-06-09` éjfél körül.

## Mért teljes futások

| Bolt | Futtatott parancs | Normalizált sor | Idő |
| --- | --- | ---: | ---: |
| SPAR | `python main_spar.py` | 7 819 | 2:44.76 |
| Príma | `python main_prima.py` | 4 279 | 3:09.57 |
| Tesco | `python main_tesco.py` | 17 924 | 1:57.42 |
| Auchan | `python main_auchan.py` | 25 372 | 19:37.90 |

Az Auchan mért ideje a késleltetett hibásoldal-újrapróbálás beépítése előtti
teljes futás. A jelenlegi beállítással, ha ugyanaz a 6 API-oldal továbbra is
hibás, várhatóan körülbelül 3-4 perccel hosszabb lehet.

## Tesco megjegyzés

A megszakított Tesco mérés azért futott túl sokáig, mert a `main_tesco.py`
akkor még `--enrich-product-details` módban indult. Ez termékenként külön
GraphQL részletlekérést küldött volna.

Friss teljes részletes mérés:

| Tesco mód | Kimenet | Normalizált sor | Idő |
| --- | --- | ---: | ---: |
| Részletes termékgazdagítás, `--detail-progress-interval 1` | `tesco_normalized_data_20260609_011017.csv` | 17 924 | kb. 1:01:34 |

A részletes letöltés `2026-06-09 00:09:21` körül indult, a mentés
`2026-06-09 01:10:17` időbélyegű fájlba történt. A `get_all_data_tesco.py`
folyamat nagyjából 1:01:20 alatt állt le teljesen; utána a szűrés 0.85 mp, a
normalizálás 0.69 mp volt. A friss `tesco_all_data_20260609_011017.csv`
fájlban mind a 17 924 sor `details_enriched=True`.

Mért minta:

| Tesco mód | Minta | Idő |
| --- | ---: | ---: |
| Listaoldalak, részletes terméklekérés nélkül | 10 kategória első oldala, 877 termék | 4.28 mp |
| Ugyanez + 100 termék részletes gazdagítása | 100 részletes lekérés | 21.83 mp |

A 100 részletes lekérés többlete kb. 17.55 mp volt, vagyis kb. 0.175 mp/termék
`detail-delay=0` mellett. A teljes 17 924-17 937 termékes Tesco körre ez
önmagában nagyjából 52 perc extra hálózati idő lehet, és a korábbi
`detail-delay=0.05` még kb. 15 perc várakozást adna hozzá. Így a teljes,
termékenként gazdagított Tesco futás reálisan 60-70 perc körüli is lehet.

Ezért a `main_tesco.py` alapmódja vissza lett állítva terméklista-alapú
letöltésre. A Tesco lista GraphQL válasza már tartalmazza a kiszereléshez fontos
`details.packSize`, `details.netContents` és `details.drainedWeight` mezőket.

## Auchan hibás oldalak újrapróbálása

Az Auchan letöltőben maradt a gyors HTTP retry, és bekerült egy külön
hibásoldal-újrapróbálás is:

- alap: `--failed-page-retries 1`
- alap várakozás: `--failed-page-retry-delay 30`

Ez csak akkor fut, ha 1-es lapméret mellett is marad hibás oldal. Ha a hiba
átmeneti, ez vissza tudja hozni az adott oldalt; ha szerveroldali termékrekord
hiba, akkor naplózza és a többi terméket megtartja.
