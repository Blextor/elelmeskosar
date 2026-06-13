# Egységes kategóriarendszer — iterációs terv és állapotkövetés

Utolsó frissítés: 2026-06-11 (a dokumentumot Claude frissíti az előrehaladással
együtt, minden érdemi lépés után)

## Cél

A 9 bolt normalizált termékkínálatát (~73 000 ajánlatsor) a saját,
boltfüggetlen kategóriafába soroljuk be, részletes tulajdonságokkal együtt.
A kiindulópont a `tools/kategorizalo/próbák/kategoriak_1005.json` fa
(13 fő kategória, 144 alkategória, fő kategória → alkategóriák → altípusok →
tulajdonságok szerkezet, öröklődő fő-szintű tulajdonságokkal).

A végeredmény a mestertermék-tervhez (`docs/plans/mestertermekek.md`)
kapcsolódik: a kategória és a tulajdonságok hosszú távon a `master_products`
tábla mezői lesznek.

## Iterációs munkafolyamat

A munka több iterációban halad. Minden iteráció ugyanazt az öt fázist követi:

1. **Fa részletezése**: a kategóriafa hiányzó ágainak kidolgozása, és a
   tulajdonságok (altípusok, egyedi/csoportos jellemzők) kigyűjtése a már
   letöltött termékadatokból (nevek, leírások, bolti kategóriautak).
2. **Besorolás**: minden termék kategóriát kap. Ami nem illik sehova, az a
   megfelelő szint `Egyéb` ágába kerül; ahol egy termékre nincs értelmes
   tulajdonságérték, azt hiányzóként jelöljük.
3. **Felhasználói átnézés**: az `Egyéb`-be került és a tulajdonság-hiányos
   termékek listáját a felhasználó átnézi, és eldönti, milyen új
   kategóriák/tulajdonságok kerüljenek a következő iterációba.
4. **Újrakategorizálás**: a kérdéses termékek besorolása az új
   kategóriákkal/tulajdonságokkal.
5. **Átszervezés**: ha a tapasztalatok alapján a fa vagy a tulajdonságok
   átrendezése indokolt, annak végrehajtása és a már besorolt termékek
   migrálása.

A 3. fázis mindig felhasználói döntés; a többi fázist Claude végzi, és az
eredményeket ebben a dokumentumban rögzíti.

## Kiinduló állapot (2026-06-11)

### Kategóriafa

| Állapot | Fő kategória |
|---|---|
| Kész / előrehaladott | Ital (14 alk.), Pékáru (14), Gyümölcs (27), Zöldség (26) |
| Részben kidolgozott | Édesség/snack (7), Fagyasztott áruk (8), Hús-hal-felvágott (12), Tejtermékek és tojás (14) |
| Csak váz | Alapanyag-sütés-főzés (8), Baba (6), Mentes/speciális (8) |
| Üres (nincs alkategória) | Sütemény-desszert-torta, Készétel |

### Korábban kategorizált termékek (SPAR-korszak, 2025 ősz)

~2510 SPAR termék négy körben: alkohol 886, ital/kávé/tea/üdítő 1127,
pékáru 285 (3 tétel eltérés az eredmeny.json és eredmeny_pekaru.json közt),
sós snack 212. Részletek: `tools/kategorizalo/próbák/KATEGORIA_ALLAPOT.md`.

### Bolti forrásadatok

9 bolt friss normalizált adata (Aldi 2925, Auchan 25 372, Coop 1915,
Lidl 1183, Metro 9962, Penny 1936, Prima 4279, Spar 7819, Tesco 17 924 sor).
A bolti kategóriautak formátuma boltonként eltér (4-féle stílus); a Spar/Prima
csak slugot ad, hierarchiát nem. Az Auchan nem-élelmiszert is tartalmaz.

## Állapotkövetés

### Előkészítés (iterációkon kívül)

| Lépés | Állapot | Megjegyzés |
|---|---|---|
| Termékképek előtöltése + helyi útvonal nyilvántartás | kész (2026-06-11) | 71 540 kép, 8,71 GB a `product_images/` alatt; 210 hibás URL (0,3%, a bolti CDN-eken ténylegesen nem létező képek, HTTP 404); a `local_image_paths` oszlop mind a 9 bolt normalizált CSV-jében kitöltve |
| Nem-élelmiszer / csomag / értelmetlen szűrőréteg | kész (2026-06-12) | 25 578 sor kiszűrve a `kiszurt_termekek.csv`-be (25 543 nem élelmiszer, 32 csomag, 3 értelmetlen); a backlog 47 084 valódi élelmiszer-sorra szűkült |
| Nagy név-eltérések képes vizsgálata (87 db) | kész (2026-06-12) | Mind a 87 eldöntve: 38 név szerinti javítás, 33 API-megerősítés, 13 kézi érték (mellékelt tételek: „2×100 g + szósz" → fő termék), 3 pelenka kiszűrve. 12 termék képi ellenőrzéssel (címke-leolvasások: Urban nápolyi 180 g, Shiitake 100 g, Danone 4×125=500 g, Milupa 400 g, HiPP 190 g). Bónusz: a pelenka név-szűrő +52 nonfood terméket fogott; védelem a szórványos regex-motorhiba ellen (safe_search) |
| Kiszerelés-audit + korrekciós réteg | mintázat-döntések alkalmazva, 336 review hátra (2026-06-12) | 2220 korrekciós sor: 1233 lédig (auto) + 987 mintázat-döntés (multipack/HoReCa: 345; konzerv lecsöpögtetett megerősítés: 358, képi szúrópróbával; szósz/lekvár/befőtt→g; tejtermék-szabályok; ital/olaj→ml; név saját egysége: 38+; plauzibilitási sáv: 17; Tesco drained: 25; zárójeles: 10). Parser-fixek: méretkód (40/60), "db x" multipack, mellékelt tételek, hamis ezres-csoport. Hátralévő review: 423 = név-eltérés 372 (87 nagy / 112 közepes / 173 kis eltérés) + Metro bruttó-gyanú 51 |

### 1. iteráció

| Fázis | Állapot | Megjegyzés |
|---|---|---|
| 1. Fa részletezése + tulajdonság-kigyűjtés | felhasználói döntéssel szűkítve | A Sütemény-desszert-torta és a Készétel ág egyelőre NEM kerül bővítésre; a termékek fő kategória szinten kerülnek be |
| 2. Termékek besorolása | első kör kész, felhasználói döntésekkel véglegesítve (2026-06-12) | Sütemény-desszert-torta: 281, Készétel: 372 (ebből Konzerv készételek alkategória: 181, friss/hűtött: 191); a szűrés után 47 084 élelmiszer-sor vár a backlog fájlban |
| 3. Egyéb/hiányos lista átnézése (felhasználó) | várakozik | A névszabályos besorolások (90 db, `besorolas_alapja=termeknev`) és az ismert határesetek átnézése javasolt |
| 4. Újrakategorizálás | — | |
| 5. Átszervezés | — | |

Ismert határesetek / következetlenségek az 1. körből (felhasználói döntésre):

- A Milka Choco Brownie és Mr. Brownie típusú csomagolt sütik a Spar/Prima/Metro/Tesco
  oldalon besorolódtak (sütemény slug/név), az Auchannál viszont a "Keksz, nápolyi,
  piskóta" út vétója miatt backlogban maradtak.
- Az Auchan "Tartós sütemény > Édes teasütemény" út (Benei isler stb.) nem került
  automatikusan besorolásra (keksz-közeli), de a névszabály a linzer/isler termékek
  egy részét behozta.
- A káposztás (sós) rétesek is a Sütemény kategóriába kerültek.
- A Spar `keszdesszertek-96` slug vegyes (Monte tejdesszert + Feketeerdő/Tiramisu);
  csak a névszabályos találatok kerültek be belőle.
- ProTeen Isler (protein süti) bent maradt a Süteményben — kérdéses, hogy
  Mentes/speciális-e inkább.

Készétel-határesetek — felhasználói döntések (2026-06-12):

- Kész hamburger (zsemlével) = készétel ✔; önmagában álló húspogácsa NEM ✘
  (Dárdás hamburgerpogácsa, Penny To Go mini húspogácsák kikerültek).
- Levesek (friss/konzerv kész levesek, gyümölcs- és krémlevesek) = készétel ✔.
- Kész desszert-jellegű főételek (aranygaluska, túrógombóc, derelye) = készétel ✔.
- Konzerv ételek megtartva, de "Konzerv készételek" alkategória-jelöléssel
  (bolti út "konzerv" tokenje vagy ismert konzervmárka — Házias Ízek, Globus,
  KAMRA, ÁSZ, Menü, PRIMANA, Rege — alapján). A kategóriafa JSON-ba vezetése
  az 5. fázis (átszervezés) feladata.

Még nyitott apróságok:

- Lecsó konzerv (Auchan/SPAR natúr lecsó) — alapanyag vs. készétel határán,
  jelenleg bent.
- Bonduelle Good Lunch hideg lunch-bowlok — jelenleg bent.
- A Lidl "Készételek" útja a szűrés után 0 terméket adott (szendvics/wrap
  jellegű volt a tartalma).

## Döntésnapló

- 2026-06-13 (kat25 + Fagyasztott ág): A kat25.py kategorizáló átállítva az új
  fára (kategoriak_2026-06-13.json előnyben, 1005 fallback; 276 altípus,
  struktúra kompatibilis). Fagyasztott stratégia (felhasználói döntés): MINDEN
  fagyasztott a Fagyasztott áruk főkategóriába kerül — a "fagyasztott" a fő
  rendezőelv, a besoroláskor a fagyasztott termék ide megy, NEM a Hús-hal/
  Zöldség/Gyümölcs ágba (azok a friss/hűtött + tartós verziókat tartják). Ág
  kidolgozva 9 alkategóriával: Jégkrém-fagylalt (legnagyobb, 7 altípus),
  Fagyasztott zöldség (+burgonyatermék), gyümölcs, hús-baromfi, hal-tenger
  gyümölcsei, készétel-pizza-egytálétel, pékáru-tészta-desszert, panírozott
  (nem hús), egyéb. Jóváhagyásra vár.
- 2026-06-13 (Alapanyag finomítás, felhasználói döntések): A konzerv/savanyúság/
  befőtt az ALAPANYAG ágba tartozik (nem a Zöldség/Gyümölcsbe) — "Konzerv,
  savanyúság, befőtt" alkategória (zöldségkonzerv, paradicsom-püré, savanyúság,
  befőtt-gyümölcskonzerv, olívabogyó, kókusztej-főzőalap). Mogyorókrém marad az
  Alapanyagban (Lekvár-méz-krém). Sütőmag tisztázva: natúr/darált mag és aszalt
  gyümölcs sütéshez-főzéshez (≠ sózott/pörkölt snack-mag, ami az Édesség ágba
  megy). Alapanyag végső: 15 alkategória.
- 2026-06-13 (Hús-hal fedettség + Alapanyag ág): Hús-hal "biztos ami biztos"
  fedettség-ellenőrzés: 4849-ből 4112 tisztán besorolható, a maradék zöme
  teszt-kulcsszó hiány (létező alkategóriák); egy valódi hiány pótolva: Húsos
  snack/szárított (kabanos, baromfirúd) altípus. Alapanyag ág kidolgozva 15
  alkategóriával (korábbi 8 → 15). Új alkategóriák a szélső esetekből: Szószok/
  öntetek/dresszingek (ketchup/majonéz/mustár/BBQ — több száz db!), Cukor/
  édesítőszer, Hüvelyesek, Konzerv/főzőalap (paradicsompüré/kókusztej),
  Instant ételek/alapok, Olajos magvak/aszalt gyümölcs. Öröklődő flagek: bio,
  gluténmentes, cukormentes, instant/por. Nyitott határesetek: (a) savanyúság/
  befőtt/zöldségkonzerv → a Zöldség/Gyümölcs ágba kerül a besoroláskor, nem ide;
  (b) snack-mag (sózott mogyoró) → Édesség/snack, csak a sütőmag van itt;
  (c) mogyorókrém/Nutella itt a Lekvár-méz alatt, de lehetne az Édességben is.
  Jóváhagyásra vár.
- 2026-06-13 (Hús, hal, felvágott ág): Tejtermék ág jóváhagyva. Hús-hal ág
  kidolgozva 18 alkategóriával. A szélső eset-vizsgálat öt új alkategóriát
  hozott a korábbi 12-höz: Darált hús/fasírt (159 db), Belsőség (74),
  Szalonna/tepertő/zsiradék (183), Panírozott/elősütött (89), Növényi húspótló
  (45, MYVAY). A friss hús állatfaj szerint (Csirke/Sertés/Marha/...) testrész-
  altípusokkal; a hal 521 termék faj szerint (lazac/tőkehal/pangasius/tonhal/
  rák); felvágottak 10 altípus. Öröklődő flagek: füstölt, csípős, fagyasztott,
  ízesített/pácolt, készítmény(növényi/kevert). Nyitott kérdés: a Növényi
  húspótló itt vagy a Mentes/speciális ágban legyen. Jóváhagyásra vár.
- 2026-06-13 (fa-kidolgozás indul): A kiszerelés kész, kezdődik a kategóriafa
  befejezése. Felhasználói döntés: RÉSZLETES kidolgozás (minden alkategória
  altípusokra bontva, sok tulajdonsággal), ÁGANKÉNTI jóváhagyással, új fájlba
  (kategoriak_2026-06-13.json, az 1005 érintetlen). Minta/konvenció: márka =
  egyedi tulajdonság; íz/fajta = csoportos; a flag-jellegű tulajdonság értéke
  {}, a választható listáé []. Sorrend volumen szerint: Tejtermék (~8900) →
  Hús-hal (~5700) → Alapanyag (~4900) → Édesség (~3700) → Fagyasztott → Mentes
  → Baba. Az első ág (Tejtermékek és tojás) kidolgozva, jóváhagyásra vár.
- 2026-06-13 (Tejtermék ág — szélső esetek felülvizsgálata, felhasználói
  kérésre): A backlog alapos átnézése valós hiányokat tárt fel az első
  javaslatban, pótolva: (1) "készítmény (növényi zsiradékkal)" öröklődő flag a
  Délibáb-szerű műtermékekre (157 db: sajtkészítmény, tejkészítmény); (2)
  kimaradt "Tejital, jegeskávé" alkategória visszatéve (101+ db, tévesen
  összevontam a joghurtitallal); (3) Sajt → Grillsajt/halloumi + Sajtkészítmény
  altípus; (4) Ivójoghurt-kefir → Író; (5) Vaj → Vajkrém + kenhető vajkeverék;
  (6) öröklődő flagek: protein/magas fehérje, light, cukormentes, ízesített;
  (7) Növényi alternatíva altípus-bővítés. Végső: 16 alkategória. Tanulság a
  többi ágra: minden főkategóriánál keresni kell a "készítmény/ízű/jellegű/
  helyettesítő" műtermékeket és a protein/light/mentes/növényi variánsokat.
- 2026-06-13 (kiszerelés-review LEZÁRVA): A maradék 303 review-jelölt (252
  név-eltérés + 51 Metro bruttó) konszenzus-logikával eldöntve (API + név +
  Metro jellemző hármas jel): 204 első körben, majd LECSO-bővítésekkel a
  konzervek, végül a maradék a "név = deklarált csomagméret" elvvel (az API
  >12% eltérése ár-derivált pontatlanság). 3 esetnél kép döntött (Penny
  gyümölcssaláta szirupban → lecsöpögtetett 480; ALL SEASONS mangó fagyasztott
  → név 750; Auchan csirke levestál → név 700). 1 szett (Martini+Kinley → API
  összeg). Eszköz: apply_maradek_kiszereles.py. Teljes kiszerelés-korrekció:
  2629 (1223 lédig auto + 980 mintázat + 426 kézi/képes), 0 nyitott review.
  A kiszerelés-réteg ezzel kész; a jövőbeli letöltéseknél a scriptek
  (audit → mintazat → plus → metro_netcontent → xy → hal → maradek → assign)
  újrafuttathatók.
- 2026-06-13 (Metro API vs jellemző elemzés): A teljes Metro készleten (9962)
  összevetve a normalizált API-t (basePriceContent-alapú unit_step) és a
  netContentVolume/netPieceWeight "jellemzőt": egyezik 8976 (90%), db-eltérés
  767, különbözik 217, hiányzó ~0. A 217 eltérőnél a jellemző NEM univerzálisan
  jobb: italoknál + abszurd API-hibáknál (méz 900000 g) igen, de a
  lecsöpögtetett konzerveknél/glazúros tengeri termékeknél a jellemző a BRUTTÓ
  töltőtömeg → ott az API (lecsöpögtetett) a jó; db-terméknél a darab. Felhasználói
  döntés: a jellemző PLUSZ vizsgálódási jel, nem felülíró alap. Alkalmazva csak
  a "+"-os italokra (12, apply_metro_netcontent.py). A teljes 217-es lista:
  data/categories/metro_api_vs_jellemzo_elteresek.csv.
- 2026-06-13 (név-eltérés review, 1. adag): Felhasználói döntések a kisebb
  (<50%) név-eltérésekre: X/Y kétértékes név ("820 g/470 g") → a kisebb
  (lecsöpögtetett); "N×M (összeg)" → a teljes csomag; kis eltérés (≤12%),
  konzerv-API-kisebb és glazúros hal → egyenként. Alkalmazva: 17 X/Y +
  multipack (apply_xy_lecsopogtetett.py), 15 hal/tengeri termék képes
  review-val (apply_hal_review.py): glazúrnál nettó haltartalom, tonhal sós
  lében a lecsöpögtetett (1705 g bruttó → 1,3 kg), Viking töltőtömeg 85 g.
  Hátralévő: 252 név-eltérés (főleg ≤12% kis eltérés + konzerv) következő
  adagokban, egyenként/képpel.
- 2026-06-13 ("+"-os termékek): A 87-es képes review egy hibáját javítottuk:
  a Johnnie Walker "0,7 l + 0,2 l" nem fő termék + tartozék, hanem két önálló
  ital → 900 ml (összeadás). Általános elv (felhasználó): ital + "+" második
  kiszerelés ÖSSZEADÓDIK; étel + "+" tartozék (szósz/fűszer) esetén csak a fő
  termék. A "pohár NN cl" a tárgy űrtartalma, nem ital (Bacardi + Mojito
  pohár → 700 ml rum). Az egész adatbázisban 10 ital "+" termék érintett
  (JW ×2 → 900, Unicum B&N → 740, Unicum Szilva/Bitter/Narancs → 1100,
  Coop Unicum szettek → 780, St. Hubertus ×2 → 540). Eszköz:
  apply_plus_osszeg.py (idempotens, a jövőbeli letöltésekre is). A 6 camembert
  "+szósz/fűszer" helyesen fő termék maradt.

- 2026-06-12 (levesek): A kész levesek (friss, hűtött, konzerv — pl.
  Hmmmaster, halászlé konzerv, gulyásleves) a Készétel kategóriába
  tartoznak (felhasználói döntés); a leves-nevű termékek mentesülnek a
  készétel név-kizárások alól, ha tényleg kész levesek (nem por, kocka,
  sűrítmény, levestészta, fagyasztott alap). A fagyasztott levesek a
  mirelit-szabály alá esnek (backlogban maradnak). A levesek kiszerelési
  egysége az általános szabály szerint a név saját egysége. Készétel így
  374 termék, ebből 24 leves.
- 2026-06-12 (tejtermék- és általános egység-szabályok, felhasználóval
  közösen): joghurt/tejföl/kefir → GRAMM; jegeskávé/tej/tejital → ML;
  tejszín, habtejszín, tejszínhab (spray is) → ML. Általános szabályok:
  dupla deklarációnál ("330g/370 ml") a gramm a tömeg-deklaráció; egyébként
  a név saját egysége a gyártói konvenció (szilárd termék nem ml, folyadék
  nem gramm). A levesek (5 db) konvenciója még nyitott felhasználói döntés.
- 2026-06-12 (egység-szabályok, felhasználóval közösen): szósz/öntet/
  majonéz/savanyúság jellegű termék GRAMMBAN, bor/olaj/üdítő/ital ML-ben
  mérendő — amelyik forrás (név vagy API) a helyes egységet adja, az nyer.
  Összetett termékeknél („müncheni kolbász + mustárral") a FŐ termék
  kiszerelése számít, a mellékelt extra megjelölendő és figyelmen kívül
  hagyandó; a név-parser pozíció szerint az utolsó mennyiséget veszi.
- 2026-06-12 (kiszerelés mintázat-döntések, felhasználóval közösen): (1) a
  LECSÖPÖGTETETT tömeg a preferált kiszerelés (többet mond), nem a nettó —
  a korábbi nettó-preferencia megfordítva; cél a hasonló termékek
  konvenciójához igazodni. (2) Multipack/karton: a név szerinti teljes
  mennyiség a kiszerelés (10 db tojás, 24×330 ml karton). (3) Konzerveknél
  az API kisebb (lecsöpögtetett vélelmű) értéke marad — képi szúrópróbával
  igazolva (Happy Frucht 400/240 g a címkén). (4) Tesco drained mező és a
  "X g (Y g)" zárójeles nevek lecsöpögtetett értéke automatikusan átvéve.
  (5) Az egység-eltérések (g↔ml, 219 db) darabonkénti átnézésre maradnak.
  A mintázat-döntéseket az `apply_mintazat_dontesek.py` alkalmazza; kézi
  korrekciót sosem ír felül.
- 2026-06-12 (kiszerelés-réteg): Felhasználói elvek rögzítve: (1) a lédig
  termékeknél a bolti lépésköz NEM kiszerelés — ott csak az egységár
  használandó; (2) név-vs-API eltérésnél és nettó/bruttó töltőtömeg esetén a
  valós, lehetőleg NETTÓ kiszerelést kell megtalálni; (3) a korrekciók külön
  fájlban élnek, az eredeti adat nem íródik felül. Lédig-felismerés: Metro
  `isWeightArticle=WEIGHT`, Tesco `catchWeightList`, Spar/Prima
  `sell_by_weight_config`, Roksh `isBulk`, plusz a névbeli "lédig" szó
  (Auchan így jelöl). Az Auchan `loose.weightPerPiece` mező NEM lédig-jel
  (logisztikai darabtömeg, pólókon is ki van töltve).
- 2026-06-12 (szűrőréteg): Bevezetve a nem élelmiszer / csomag / értelmetlen
  előszűrés (felhasználói kérésre). Nem élelmiszer: bolti nonfood ágak
  (Auchan Elektronika/Otthon/Kert/Játék/Fanshop, Tesco Otthon-hobbi/Drogéria/
  Háztartás/Kisállat, Roksh Háztartás/Szépség-egészség/Állateledel/Középső
  sor, Spar-Prima drogéria- és állateledel-slugok) + a vegyes Baba-ágakból a
  nem-étel részek (a bébiétel marad). Vitamin/étrend-kiegészítő nonfoodnak
  minősítve; a protein termékek NEM kerültek szűrésre (a fa Mentes ága fedi).
  Csomag: ajándékkosár/-csomag/-szett, mikuláscsomag, adventi kalendárium —
  az egy-termékes díszdobozos italok (pl. whisky díszdobozban) megmaradtak.
  Értelmetlen: üres nevű vagy ár nélküli sorok (pl. Spar "ÁRrésSTOP").
- 2026-06-12 (2. kör): Felhasználói döntések a határesetekről: kész hamburger
  készétel, önálló húspogácsa nem; levesek és kész desszert-főételek
  (aranygaluska, túrógombóc, derelye) készételek; a konzerv ételek "Konzerv
  készételek" alkategóriát kapnak. Bevezetve az alkategória-jelölés a
  kategorizalt_termekek.csv-ben (181 konzerv / 191 friss-hűtött).
- 2026-06-12: Készétel-definíció pontosítva (felhasználó): csak az számít
  készételnek, ami készen van és legfeljebb mikrózni kell, főétel-jellegű.
  NEM készétel: mirelit/fagyasztott (pl. mirelit pizza, fagyasztott rántott
  sajt), snack, popcorn, bögrés/instant leves. A fagyasztott "készételek"
  (372 sor) visszakerültek a backlogba. Módszertani elv (felhasználó): a bolti
  kategóriaút csak kiindulási alap — a terméknév, a kép és a kiszerelés
  együttes mérlegelése szükséges; a besoroló ennek megfelelően név-alapú
  kizárásokkal és feltételes szabályokkal (szósz/rántott csak körettel) szűri
  a bolti készétel-utak jelöltjeit.

- 2026-06-11: A terv rögzítve. Az iterációk a fenti ötfázisú kör szerint
  haladnak; a fa kiindulópontja a `kategoriak_1005.json`.
- 2026-06-11: Termékkép-előtöltés külön, közös szkriptként megvalósítva
  (`download_product_images.py`), nem a kat25.py kategorizáló részeként.
  Célja, hogy a Claude-os kategorizálás során a képek helyben, azonnal
  megnézhetők legyenek. Inkrementális: a fájlnév az URL SHA1-kivonata,
  így csak új/megváltozott képek töltődnek le; a frissítés a bolti
  `main_*.py` láncok végén automatikus. A helyi útvonalak a normalizált
  CSV-k `local_image_paths` oszlopában és a `<bolt>_image_index_*.csv`
  fájlokban vannak nyilvántartva. Alapértelmezés: termékenként az
  elsődleges (első) kép.

## Kapcsolódó fájlok

- `tools/kategorizalo/próbák/kategoriak_1005.json` — kiinduló kategóriafa.
- `tools/kategorizalo/próbák/KATEGORIA_ALLAPOT.md` — a SPAR-korszakos
  kategorizálási munka állapotjegyzete.
- `tools/kategorizalo/próbák/eredmeny_alkohol.json`, `ktest/ital_spar/`,
  `kategorizalt_termekek/` — korábbi kézi kategorizálások eredményei.
- `docs/plans/mestertermekek.md` — mestertermék terv, a kategóriarendszer
  célállomása.
- `data/markets_data/*_normalized_data_*.csv` — a besorolandó termékek
  forrása (boltonként a legfrissebb).
- `src/categories/assign_categories.py` — szabályalapú besoroló (bolti
  kategóriaút- és terméknév-szabályok, vétólistákkal).
- `data/categories/kategorizalt_termekek.csv` — a már besorolt termékek
  (fő kategória, alkategória, altípus, tulajdonságok, besorolás alapja).
- `data/categories/kategorizalatlan_termekek.csv` — a feldolgozásra váró
  backlog; ahogy a termékek besorolódnak, innen fogynak.
- `data/categories/kiszurt_termekek.csv` — nem élelmiszer, csomag (ajándék-,
  mikuláscsomag, adventi kalendárium) és értelmetlen (üres nevű/ár nélküli)
  sorok, `kiszures_oka` oszloppal; nem részei a kategorizálásnak.
- `src/categories/audit_kiszereles.py` — kiszerelés-audit: lédig-felismerés
  (bolti jelek + névbeli "lédig"), név-vs-API eltérések, nettó/töltőtömeg
  jelek; kimenete a `kiszereles_audit.csv` jelölt-lista.
- `data/categories/kiszereles_korrekciok.csv` — a karbantartható korrekciós
  réteg: a lédig sorok automatikusan, a review-ból megerősített javítások
  kézzel kerülnek ide; az eredeti normalizált adat sosem íródik felül. Az
  `assign_categories.py` ebből tölti a `vegso_mennyiseg`/`vegso_egyseg`/
  `ledig` oszlopokat.
