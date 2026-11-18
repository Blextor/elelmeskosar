# A kategóriafa és a mentett termékbesorolások állapota

2026. november 18-án a GPT-munkapéldányban **47 030 egyedi bolti termékrekord** szerepel `kesz` állapottal. A forrásuk **kilenc bolt 2026. június 8–10-i letöltése**. Ebből **46 950** rekord mentett kategóriaútvonala megtalálható a hozzá tartozó GPT-fában. A mentés állapota, az útvonal létezése és a termék szaktudással végzett ellenőrzése a készültség három különböző szintje. A tízboltos novemberi frissítésre ezek a számok közvetlenül nem vihetők át.

## Mely termékekről van döntés

A termékjegyzékben egy sor egy bolt és bolti azonosító párosa. Tartalmazza a nevet, a dátumozott forrásfájlt, a mentett fő- és alkategóriát, az altípust, az útvonal ellenőrzését és az esetleges Claude-útvonalat. Ugyanaz az árucikk több boltnál külön sor. [A 47 030 termék szűrhető jegyzéke](mentett_besorolasok.csv)

| Bolt | Júniusi forrásnap | Forrássor | Mentett GPT-besorolás |
|---|---|---:|---:|
| ALDI | június 10. | 2 925 | 2 321 |
| Auchan | június 8. | 25 372 | 10 120 |
| CoopOnline | június 10. | 1 915 | 1 887 |
| Coopshop | június 23. | 3 833 | 0 |
| Lidl | június 10. | 1 183 | 1 178 |
| METRO | június 10. | 9 962 | 9 836 |
| PENNY | június 10. | 1 936 | 1 609 |
| Príma | június 8. | 4 279 | 3 896 |
| SPAR | június 8. | 7 819 | 6 740 |
| Tesco | június 9. | 17 924 | 9 443 |
| **Összesen** | | **77 148** | **47 030** |

**A forrásdátum ellenőrzése.** A 47 030 mentést egyenként egyeztettem az eredeti munkalista sorával. 35 530 mentésben hiányzik a bolt neve. Az eredeti listában az ID és, ahol szükséges, a mentett boltnév minden esetben egyetlen sort azonosít. Két mentett terméknévnél javított karakter szerepel, ezekhez mindkét nevet megőriztem a jegyzékben. A munkalista mind a 47 030 soránál a bolti kulcs, név, márka, ár, egység, lépésköz, bolti kategória és helyi képútvonal egyezik a táblázat szerinti júniusi fájllal. A fa fájlnevében lévő június 13. a fa változatjelölése. A GPT eredményfájljának utolsó gitben rögzített módosítása augusztus 3. [Bemeneti munkalista](../../../data/categories/kategorizalando_termekek/GPT/kategorizalatlan_termekek.csv) · [Bolti fájlpárok](../market_refresh_20261118/store_checks.csv)

A kilenc bolt 73 315 forrássora maradéktalanul elszámolható. A 47 030 GPT-rekordon kívül **655** sor a korábbi szabályalapú besorolásban, **25 630** a korábbi kizárási listában van. A három halmaz bolti kulcsonként diszjunkt. A 655-ből 563-nál a bolti kategóriaút, 92-nél a terméknév a rögzített besorolási alap. A kategória- és kizárási döntések átvételéhez termékenkénti szakmai ellenőrzés szükséges. A Coopshop további 3 833 sora későbbi letöltésből származik. [Szabályalapú címkék](../../../data/categories/kategorizalt_termekek.csv) · [Korábbi kizárások](../../../data/categories/kiszurt_termekek.csv)

## Mennyire kész a fa

A GPT-eredményt a vele egy mappában lévő fához mértem. Ebben **15 főkategória, 265 alkategória és 1 340 altípus** van. Mindegyik főágban van termék. Az alkategóriák közül 12-höz egyetlen rekord sem tartozik közvetlenül vagy altípuson keresztül, 20 definiált altípushoz sincs mentett termék. Egy üres ág önmagában nem bizonyít hibát. [A vizsgált fa](../../../data/categories/kategorizalando_termekek/GPT/kategoriak_2026-06-13.json) · [Mind a 15 ág darabszámai és eltérései](agankenti_allapot.csv)

- **80 termék hét hiányzó útvonalon van.** A Készétel ágban 75 ilyen tétel található, köztük 31 a `Saláta, hidegtál → Saláta, hidegtál` útvonalon. Az Alapanyag, sütés-főzés ágban további öt van. A jegyzékben az `utvonal_a_faban = 0` szűrő adja a konkrét tételeket.
- **1 343 termék egy létező szülőkategórián áll**, miközben van választható altípus. A Pékáru ágban 473, az Alapanyag, sütés-főzés ágban 435 ilyen rekord van. A pontosabb besorolásról a termék bizonyítékai alapján lehet dönteni.
- **9 180 rekordnál eltér a mentett kategória-hash** a szerkesztőben használt képlettel újraszámolt értéktől. Az Ital ágban az eltérés nulla. A hash az útvonal és a tulajdonságok technikai egyezését vizsgálja. Az eltérés oka ebből nem állapítható meg.
- **37 107 létező útvonalú rekordban** hiányzik legalább egy, a saját vagy felmenő csomópontokon definiált tulajdonságkulcs. Ez egyszerű kulcsjelenléti mérés. Egyes tulajdonságok csak bizonyos termékekre alkalmazhatók. A szám szakmai hibaarányként nem értelmezhető. A hiányzó kulcsok termékenként szűrhetők a jegyzékben.

**Az Ital ág felülvizsgálata dokumentált a legrészletesebben.** A július 29-i keltezésű, később folytatott napló 12 455 egyedileg ellenőrzött célrekordot számol el. Egy termék a Baba → Bébiital, víz → Bébivíz ágra került, ezért ma 12 454 az Ital főág darabszáma. A napló három faépítési javaslatot is nyitva hagyott az ízesítetlen vizekhez. A vizsgált Ital-fában külön Gyógyvíz, Egyéb ivóvíz és Szódavíz és szikvíz levél továbbra sem szerepel. A többi ág szakmai ellenőrzésének teljességére a `kesz` jelzőből nem következik darabszám. [Termékszintű felülvizsgálati napló](../../../data/categories/kategorizalando_termekek/GPT/ital_termekek_kezi_felulvizsgalata_2026-07-29.md)

## Párhuzamos és történeti munkák

- **Claude Opus.** A külön munkapéldány fájában 13 főkategória, 189 alkategória és 406 altípus van. Mind a 3 077 mentett termék benne van a GPT-jegyzékben is, közülük 2 321 ALDI- és 756 Auchan-termék. A mentett kategóriaút 2 412 esetben egyezik, 665-ben eltér. Az eltérés oka lehet eltérő faverzió vagy eltérő termékértelmezés. [Claude-eredmények](../../../data/categories/kategorizalando_termekek/Claude_Opus/eredmeny.json)
- **Korábbi SPAR-munka.** Az archivált JSON-mentésekben 2 484 egyedi, késznek jelölt SPAR-rekord van. Mind a 2 484 forrásadata egyezik a 2025. augusztus 2-i 20:46:54-es SPAR-pillanatképpel. Ezek régi bolti azonosítók. A történeti és a júniusi rekordok közötti termékazonosság külön döntést igényel. A korábbi pékségi munkában további 26 rekord állapota `folyamatban`. [Archív termékjegyzék](archiv_spar.csv) · [Korábbi állapotjegyzet](../../../tools/kategorizalo/próbák/KATEGORIA_ALLAPOT.md)

**A mesterlista előtti következő feladat** a 80 hiányzó útvonalú termék, majd a két munkapéldány 665 eltérésének termékenkénti szakmai egyeztetése. A modell a nevet, képet, kiszerelést, leírást és a bolti kategória megbízhatóságát együtt mérlegelje. A technikai audit a mentett döntések számlálására, visszakeresésére és formai ellenőrzésére szolgál. [Kategorizálási munkaszabályok](../../../data/categories/kategorizalando_termekek/GPT/rules.txt)
