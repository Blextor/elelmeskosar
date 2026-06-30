# Ital kategória - rejtett tulajdonság és értéknormalizálás

## Elvégzett tisztítás

- Eltávolítottam az Ital alól a redundáns `terméktípus` mezőt.
- A `jellemzők` mezőt csak ott hagytam meg, ahol ténylegesen hasznos, objektív címkéket tartalmaz; kikerültek többek közt az `alkoholmentes`, `prémium`, `nem jelölt`, `classic`, `light`, `balanced & fruity` értékek.
- Kikerültek az általánosan redundáns vagy hibás boolean mezők: például `szénsavas`, `alkoholmentes`, `alkoholos`, több konstans igaz/hamis út-specifikus boolean, illetve az alkoholos utakból a `cukormentes / zero`.
- Normalizáltam több márkacsoportot: `UNICUM` és Unicum-változatok -> `Zwack Unicum`, Coca-Cola variánsok -> `Coca-Cola`, `Natur Aqua`/`NaturAqua Emotion` -> `NaturAqua`, továbbá több ital- és kávémárka termékváltozata főmárkára került.
- A kávékapszuláknál külön tisztítást végeztem: a termékváltozat-szintű márkákat alapszintre húztam, a `kiszerelés / rendszer` mezőt gramm/db értékek helyett kapszularendszerre javítottam, és levettem a tartalmatlan/duplikáló `csomagolás`, `feldolgozás`, `ízesítés`, `koffeintartalom`, `változat`, `eredet`, `intenzitás` mezőket.
- A mélyaudit által jelzett márkaírásmód-eltéréseket is egységesítettem, például `7UP` -> `7Up`, `DISARONNO` -> `Disaronno`, `SPAR/Spar` -> `SPAR`, `OMG Bubble tea` -> `OMG Bubble Tea`.

## Mennyiségi hatás

- 1. tisztítás által érintett termékek: 12669
- 2. tisztítás által érintett termékek: 2285
- 3. tisztítás által érintett termékek: 3170
- 4. tisztítás által érintett termékek: 5071
- 5. márkatisztítás által érintett termékek: 513
- 6. generikus mező/márka tisztítás által érintett termékek: 1372
- 7. kávékapszula tisztítás: 124 márkajavítás, 190 kapszularendszer-javítás, törölt mezők: {'csomagolás': 478, 'feldolgozás': 478, 'ízesítés': 478, 'koffeintartalom': 478, 'változat': 478}
- 8. kávékapszula részlegesen kitöltött mezők eltávolítása: {'intenzitás': 60, 'eredet': 2}
- 10. márkaírásmód-normalizálás: 27 termék
- 11. végső márkaduplikáció-normalizálás: 3 termék, 4 kategóriafa-lista
- 12. explicit termékváltozat-márka normalizálás: 359 termék, 55 kategóriafa-lista

## Aktuális audit állapot

- Ital termékek: 12713
- Deklarált/használt Ital utak: 129 / 129
- Hiányzó útvonal: 0
- Termékben lévő, de fában nem deklarált tulajdonság: 0
- Fában deklarált, de termékből hiányzó tulajdonság: 0
- Üres tulajdonságérték: 0
- Duplikált altípusnév: 0
- Mélyaudit hiányzó kötelező tulajdonság: 0
- Mélyaudit extra tulajdonság: 0
- Mélyaudit nem deklarált érték: 0
- Mélyaudit típusgyanú: 0
- Szemantikai audit Italban gyanús érték: 0
- Szemantikai audit Italból hiányzó gyanús érték: 0
- Szinonima audit tulajdonságnév-variáns: 0
- Szinonima audit foldolt értékduplikáció: 0
- Rejtett audit `terméktípus` utak: 0
- Rejtett audit `jellemzők` utak: 7
- Rejtett audit boolean gyanúk: 9
- Generikus property audit sorok: 51

## Tudatosan meghagyott maradékok

- A maradék boolean gyanúk ritka, de objektív jelölések: `bio`, `koffeinmentes`, `gluténmentes`, `kézműves`, `cukormentes / diabetikus`. Példákkal ellenőrizve valódi termékjelölések, ezért nem töröltem őket csak ritkaság alapján.
- A maradék generikus sorok többsége olyan széles altípusban maradt, ahol a mező ténylegesen segít: például tea forma/típus, pálinka/gin/IPA fajta, kakaó italpor típus.
- A ritka érték gyanúk száma magas maradt, mert az audit minden egyszer előforduló ízt, borvidéket, szőlőfajtát és termékspecifikus értéket listáz. Ezek nem automatikusan hibák.
