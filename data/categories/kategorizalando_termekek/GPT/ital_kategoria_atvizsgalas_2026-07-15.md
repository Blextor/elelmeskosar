# Az `Ital` főkategória átvizsgálása

Audit dátuma: 2026-07-15

Vizsgált fájlok:

- `kategoriak_2026-06-13.json`
- `eredmeny.json`
- `kategorizalatlan_termekek.csv`

Az audit során a három forrásfájlt és a termékekhez elérhető helyi képeket olvasási módban vizsgáltam. A JSON- és CSV-adatokat nem módosítottam.

## Rövid összefoglaló

Az `Ital` ág szerkezetileg jó állapotban van: mind a 88 deklarált kategóriaút használatban van, nincs termékoldali, fában nem szereplő tulajdonság vagy érték, nincs üres tulajdonságérték, és mind a 12 713 Ital-termék kategória-hash-e helyes. Ez azonban csak szintaktikai konzisztencia.

A tartalmi audit több jelentős problémát talált:

1. Az `eredmeny.json` beágyazott `termek` objektumai négy különböző sémát követnek; 35 530 rekordból hiányzik a bolt neve és a legtöbb CSV-forrásmező.
2. A növényi italok két főkategória között vannak megosztva: 68 termék az `Ital`, 167 termék a `Tejtermékek és tojás` ágban található.
3. Az `alkoholmentes` érték 762 alkalommal szemantikailag rossz tulajdonságba került, például energiaitaloknál `termékcsalád`, instant kávénál `feldolgozás`, zabitalnál `minősítés` mezőbe.
4. A 12 713 termékből 9 647-ben található legalább egy `nem jelölt` érték; összesen 20 571 ilyen érték van.
5. Több konkrét félrebesorolást a terméknév, a bolti forráskategória és reprezentatív esetekben a termékkép is megerősít.
6. Azonos nevű tulajdonságok többféle típussal szerepelnek, a `kiszerelés` pedig 590 alkalommal mennyiség helyett csomagolási formát tartalmaz.

## Alapadatok

| Mutató | Aktuális érték |
| --- | ---: |
| Összes termék az `eredmeny.json` fájlban | 47 030 |
| Összes CSV-sor | 47 030 |
| `Ital` termék | 12 713 |
| `Ital` alkategória | 18 |
| Deklarált / használt `Ital` kategóriaút | 88 / 88 |
| Egyedi tulajdonságkulcs az Ital-termékekben | 67 |
| `kesz` státuszú Ital-termék | 12 713 |
| Helyes kategória-hash az Ital-termékekben | 12 713 |

### Alkategóriák mérete

| Alkategória | Altípus | Termék |
| --- | ---: | ---: |
| Ásványvíz | 3 | 420 |
| Bor | 6 | 2 058 |
| Energiaital | 1 | 341 |
| Ízesített víz | 1 | 93 |
| Kávé, tea, kakaó (száraz) | 16 | 2 234 |
| Habzó-, gyöngyözőbor, boralapú ital | 3 | 154 |
| Pezsgő | 2 | 480 |
| Alkoholok | 12 | 1 724 |
| Sör | 9 | 1 015 |
| Cider | 2 | 73 |
| Sportital | 1 | 86 |
| Citromlé | 2 | 65 |
| Szörp, üdítőitalpor | 3 | 414 |
| Üdítőital | 11 | 2 635 |
| Gyümölcslé | 5 | 534 |
| Növényi ital | 7 | 68 |
| Funkcionális ital | 3 | 302 |
| Kombucha | 1 | 17 |

## Ami jelenleg konzisztens

- Mind a 88 használt `(alkategória, altípus)` út szerepel a kategóriafában.
- Nincs nem használt deklarált altípus.
- Nincs termékben szereplő, de az adott kategóriaúton nem deklarált tulajdonság.
- Nincs termékben szereplő, de a kategóriafában nem deklarált tulajdonságérték.
- Nincs üres sztring, `null` vagy üres lista tulajdonságértékként.
- Nincs normalizálva duplikált érték egy termék listás tulajdonságán belül.
- Nincs normalizálva duplikált érték a kategóriafa deklarált értéklistáiban.
- Mind a 12 713 Ital-termék hash-e megegyezik a projekt `kategoria_hash()` képletével újraszámolt értékkel.
- A CSV-ből elérhető 12 138 Ital-termékkép mindegyike ténylegesen létezik a megadott helyi útvonalon.

Ezek fontos pozitívumok, de a `nem jelölt` értékek deklarálása és a hibás értékek fába történő visszaírása miatt önmagukban nem bizonyítják a szemantikai helyességet.

## 1. A CSV és az `eredmeny.json` kapcsolata

### Négy különböző `termek`-séma

Az `eredmeny.json` beágyazott `termek` objektumai négy kulcskészletet követnek:

| Séma | Rekord |
| --- | ---: |
| Teljes, 18 mezős CSV-séma | 10 700 |
| Közepes, 12 mezős séma | 800 |
| Csak `store_product_id`, `product_name`, `image_url` | 32 330 |
| Csak `store_product_id`, `product_name`, `brand_name` | 3 200 |

Következmény:

- 35 530 rekordból hiányzik a `store_name`, az ár, a mennyiség, a forráskategória és a `local_image_paths` mező;
- 32 330 rekord `local_image_paths` helyett `image_url` kulcsot használ;
- az `eredmeny.json` önmagában nem egységes forrástükör;
- az elemzéseknek jelenleg a CSV-t is be kell tölteniük.

A rekordok mindegyike visszaköthető a CSV-hez, de ehhez nem elég biztonságos mindenhol csak a `store_product_id`:

- a CSV-ben a `734295` azonosító kétszer szerepel;
- az egyik termék Aldi-, a másik Penny-forrású;
- a két rekord neve azonos: `Bravos Classic őrölt, pörkölt kávé 250 g`;
- ennél a párnál a `(store_name, store_product_id)` összetett kulcs szükséges.

Javaslat: legyen minden rekordban kötelező a `store_name`, `store_product_id`, `product_name`, `categories` és egyetlen, egységes képmező. Az összekapcsolási kulcs a `(store_name, store_product_id)` pár legyen.

### Márkamezők eltérése

A CSV és a beágyazott `termek.brand_name` nem tekinthető azonos jelentésű mezőnek:

- 20 942 rekordban a CSV-ben van márka, a beágyazott rekordban nincs;
- 1 467 rekordban a beágyazott rekordban van márka, a CSV-ben nincs;
- 165 rekordban mindkettő nem üres, de eltérő.

Ez részben lehet szándékos márkatisztítás, de a jelenlegi séma nem jelzi, hogy melyik a nyers és melyik a normalizált érték.

## 2. Képek elérhetősége

| Képállapot az Ital-termékeknél | Termék | Arány |
| --- | ---: | ---: |
| Kép elérhető az `eredmeny.json` valamely képmezőjéből | 10 955 | 86,2% |
| Kép csak a CSV-ből nyerhető vissza | 1 183 | 9,3% |
| Nincs képútvonal | 575 | 4,5% |
| CSV-ben van kép, és a fájl ténylegesen létezik | 12 138 | 95,5% |

Az `eredmeny.json` képhivatkozásai két eltérő kulcs alatt vannak:

- `local_image_paths`: 2 322 Ital-termék;
- `image_url`: 8 633 Ital-termék;
- egyik sem: 1 758 Ital-termék, közülük 1 183-nál a CSV-ben még megtalálható a kép.

Hét reprezentatív, gyanús termék képét nyitottam meg. A képek megerősítették többek között a Koch 100%-os gyümölcs-/zöldséglé, a Peroni 0,0%, a Sonic/Pink Unikornis gyerekital, a Torres Serena 0,0% és az 1664 Blanc 5% termékeknél leírt problémákat.

## 3. Kategóriahatár: a növényi italok ketté vannak osztva

Ugyanaz a termékcsalád két főkategóriában szerepel:

| Útvonal | Termék |
| --- | ---: |
| `Ital > Növényi ital > ...` | 68 |
| `Tejtermékek és tojás > Növényi alternatíva > Növényi ital` | 167 |

Példák a `Tejtermékek és tojás` ágban:

- `Alpro cukormentes zabital hozzáadott kalciummal és vitaminokkal 1 l`
- `The Bridge BIO UHT gluténmentes rizsital 1 l`
- `Joya szójaital vanília ízű UHT 1 l`
- `Alpro Barista kókuszital szójával, hozzáadott kalciummal 1 l`

Ugyanezeknek a típusoknak külön `Zabital`, `Rizsital`, `Szójaital`, `Kókuszital`, `Mandulaital` altípusuk van az `Ital` ágban.

Ez nem oldható meg pusztán értéknormalizálással: előbb tulajdonosi szabályt kell választani.

Javasolt döntés: a fogyasztásra kész növényi italok kerüljenek egységesen az `Ital > Növényi ital` alá; a növényi joghurt, desszert, főzőkrém és hasonló termékek maradjanak a tejtermék-alternatívák között.

## 4. Biztos vagy erősen alátámasztott félrebesorolások

### 4.1. 100%-os levek szénsavas üdítőként

Három Koch-termék került ide:

`Ital > Üdítőital > Szénsavas üdítő`

- `Koch frissen préselt BIO kékszőlőlé céklával 3 l`
- `Koch frissen préselt kékszőlőlé almával és erdei gyümölccsel 3 l`
- `Koch frissen préselt rosé szőlőlé almával és málnával 3 l`

Mindháromnál a `szénsavasság = ["szénsavas"]` érték is hibás. A forráskategória `Gyümölcs és zöldséglevek > Mixek`; az első termék képe 100%-os gyümölcs-/zöldséglevet mutat.

### 4.2. Alkoholmentes termékek alkoholos altípusban

A kategóriafában vannak külön alkoholmentes altípusok, ennek ellenére legalább 12, név alapján egyértelmű termék normál alkoholos altípusban maradt:

- `Peroni Nastro Azzurro 0,0% 0,5L` → `Sör > Világos sör`
- `Peroni 0,0% Vérnarancs 0,5L` → `Sör > Világos sör`
- `KARLSKRONE Radler citromos, 0,0%...` → `Sör > Ízesített sör`
- `Peroni 0,0% Citrom 0,5L` → `Sör > Ízesített sör`
- öt alkoholmentes pezsgő → `Pezsgő > Pezsgő`
- `Torres Serena Alkoholmentes Sauvignon Blanc 0,0%` → `Bor > Fehérbor`
- `NATUREO Natureo Muscat Alkoholmentes Fehérbor 0,0%` → `Bor > Fehérbor`
- `NATUREO Garnacha - Syrah Alkoholmentes Vörösbor 0,0%` → `Bor > Vörösbor`

Az alkoholmentes bor altípusban jelenleg mindössze egy termék van, miközben a fenti három termék a szín szerinti ágakban maradt.

### 4.3. Gyerek-/üdítőital pezsgőként

Négy, alkoholmentes szénsavas üdítő vagy gyümölcsital szerepel `Pezsgő > Pezsgő` alatt:

- `Celebration party szénsavas alma-eper ízű gyümölcsital...`
- `Süsü vadmálna ízű szénsavas üdítőital...`
- `Smurfy erdei gyümölcs ízű szénsavas üdítőital...`
- `Sonic Prime alma-citrom ízű szénsavas gyümölcsital...`

A Sonic képén gyermekfigurás, `Sparkling Drink` feliratú termék látható. A Pink Unikornis/Celebration Party képe ugyancsak alkoholmentes party italt mutat. Ezekhez az `Üdítőital > Gyerekital` vagy egy egységesen meghatározott alkoholmentes partyital-altípus illeszkedne jobban.

### 4.4. Italból sajt lett

A `D.E.KARAVÁN VAC. 225G` termék a következő helyen van:

`Tejtermékek és tojás > Sajt > Félkemény sajt`

Tulajdonságai között `füstölt`, `tömb`, `állat` és más sajttulajdonságok szerepelnek. A CSV forráskategóriája viszont `Ital > Kávé, Tea, Kakaó`, a termékazonosító `2756249`, a márka Karaván. Kép nincs, de a forráskategória, a 225 g-os vákuumcsomagolás és a márka alapján ezt kézi ellenőrzés után nagy valószínűséggel őrölt kávéhoz kell visszatenni.

### 4.5. Helyes kategória, hibás tulajdonság

Az `1664 Blanc búzasör 5,0% 0,5 l` helyesen `Sör > Búzasör`, de `sörtípus = ["alkoholmentes"]`, miközben az `alkoholtartalom = ["5%"]`, és a kép is 5,0%-os sört mutat.

További erős ellentmondások:

- `Homola 100% Balaton száraz fehérbor 13% 0,75 l` → `alkoholtartalom = ["0,0%"]`;
- `Tatratea Mini Set ...` és `Tatratea tea likőr válogatás ...` → `alkoholtartalom = ["0,0%"]`;
- több `Mini szeszek ...` termék → `alkoholtartalom = ["0,0%"]`.

## 5. Tömeges szemantikai tulajdonsághibák

### 5.1. Az `alkoholmentes` rossz mezőkbe került

Az `alkoholmentes` pontos érték 762 alkalommal olyan mezőben szerepel, amely nem ezt a jelentést hordozza:

| Tulajdonság | Előfordulás | Jellemző érintett ág |
| --- | ---: | --- |
| `termékcsalád` | 418 | 341 energiaital, 77 kakaó italpor |
| `feldolgozás` | 235 | 180 instant kávé, 40 gyümölcslé, 15 kombucha |
| `funkció` | 64 | funkcionális ital, vitaminital |
| `minősítés` | 35 | zabital, kombucha |
| `íz` | 9 | alkoholmentes habzó ital |
| `sörtípus` | 1 | 1664 Blanc 5%-os búzasör |

Példák:

- `FLYING POWER Energiaital...` → `termékcsalád = ["alkoholmentes"]`;
- `NESCAFÉ Instant kávé classic...` → `feldolgozás = ["alkoholmentes"]`;
- `Nesquik kakaóitalpor...` → `termékcsalád = ["alkoholmentes"]`;
- `Alpro zabital...` → `minősítés = ["alkoholmentes"]`.

Ez tömeges mezőkiosztási hiba, nem ritka kivétel. Az értéket nem másik szinonimára kell cserélni, hanem az érintett tulajdonságok jelentését és kitöltési szabályát kell javítani.

### 5.2. `nem jelölt` értékek

- 9 647 termék, vagyis az Ital-ág 75,9%-a tartalmaz legalább egy `nem jelölt` értéket.
- Összesen 20 571 `nem jelölt` érték van.
- 33 terméknél maga a `márka` is `nem jelölt`.

Kiemelt ágak:

| Útvonal | `nem jelölt`-et tartalmazó termék / összes termék |
| --- | ---: |
| Bor / Fehérbor | 931 / 936 |
| Üdítőital / Szénsavas üdítő | 668 / 668 |
| Bor / Vörösbor | 648 / 674 |
| Alkoholok / Likőr | 596 / 601 |
| Üdítőital / Gyümölcsital | 594 / 594 |
| Üdítőital / Jegestea | 482 / 482 |
| Pezsgő / Pezsgő | 423 / 423 |
| Kávé... / Őrölt kávé | 252 / 256 |

Az ismeretlen adat nem ugyanaz, mint egy valós tulajdonságérték. Érdemes eldönteni, hogy az ismeretlen mező hiányozzon, `null` legyen, vagy külön adatminőségi státuszt kapjon. A `nem jelölt` ne kerüljön automatikusan a kategóriafa értéklistájába.

### 5.3. A `kiszerelés` több fogalmat kever

Az Ital-termékekben 252 különböző `kiszerelés` érték szerepel. A mező 19 terméknél hiányzik, miközben a forrásadatban általában van mennyiség.

966 `kiszerelés` érték nem tartalmaz számot:

- 522 `palack`;
- 57 `doboz`;
- 7 `multipack`;
- 3 `tasak`;
- 1 `adagcsomagolt`;
- 376 `nem jelölt`.

A `palack`, `doboz`, `tasak` csomagolási forma, nem kiszerelési mennyiség. A fában külön `palack`, `csomagolás` és `kiszerelés / rendszer` mező is van, ezért a fogalmak jelenleg átfednek.

Javasolt szétválasztás:

- `kiszerelés_mennyiség`: például `500 ml`, `1 l`, `200 g`;
- `csomagolás`: például `palack`, `doboz`, `tasak`, `üveg`;
- `multipack`: külön strukturált darabszám és egységméret.

## 6. Tulajdonságtípusok és deklarációk

### 6.1. Közvetlen típushibák

244 termék értéktípusa nem felel meg a kategóriafában deklarált típusnak:

- 219 `Üdítőital > Gyerekital` terméknél az `energia tartalom` sztring, miközben a fában `{}` alakú, logikai mezőként van deklarálva;
- 25 `Üdítőital > Limonádé` terméknél ugyanez a hiba.

Ezen kívül négy kategóriaút tartalmaz deklarált, de egyetlen termékben sem használt tulajdonságot:

- `Alkoholmentes habzó ital`: `palack`;
- `Aloe vera ital`: `energia tartalom`;
- `Smoothie`: `energia tartalom`;
- `Gyökér alapú üdítőital`: `energia tartalom`.

137 deklarált érték nincs használatban; ezek jelentős része korábbi márka- vagy választékmaradvány.

### 6.2. Azonos név, eltérő típus

Azonos tulajdonságnév többféle adattípussal szerepel:

| Tulajdonság | Típusmegoszlás a termékekben |
| --- | --- |
| `kiszerelés` | 10 137 sztring, 2 557 lista |
| `alkoholtartalom` | 5 022 lista, 480 sztring |
| `koffeinmentes` | 1 417 logikai, 482 lista |
| `típus` | 2 253 lista, 492 sztring |
| `fajta` | 1 443 lista, 334 sztring |
| `palack` | 2 001 sztring, 184 lista |
| `forma` | 795 lista, 15 sztring |

A kategóriafában 22 örökölt tulajdonság-újradefiniálás van. Ebből 14 esetben az `egyedi`/`csoportos` típus is megváltozik. Leginkább a `Kávé, tea, kakaó (száraz)` ág `kiszerelés` mezője, illetve az `Üdítőital` ág `energia tartalom` mezője érintett.

Javaslat: egy tulajdonságnévnek globálisan legyen egy kanonikus típusa. Ha két jelentés szükséges, két külön, egyértelmű nevet kell használni.

## 7. Név alapján közvetlenül ellenőrizhető logikai mezők

Az alábbi összevetés csak akkor tekintett találatnak egy terméket, ha a terméknévben kifejezetten szerepelt az állítás.

| Állítás a névben | Találat | Helyes `true` | Hibás `false` | Hiányzó / más típus |
| --- | ---: | ---: | ---: | ---: |
| DRS / 50 Ft visszaváltási díj | 684 | 44 | 2 | 638 |
| Cukormentes / zero | 501 | 481 | 1 | 19 |
| Koffeinmentes | 94 | 86 | 0 | 8 |
| Bio / organikus | 104 | 64 | 0 | 40 |
| Energiamentes | 432 | 298 | 0 | 134 |
| Édesítőszerrel | 1 082 | 931 | 9 | 142 |
| Gluténmentes | 23 | 15 | 0 | 8 |
| Szűretlen | 109 | 103 | 0 | 6 |

Konkrét ellentmondások:

- `JANA BABY ... DRS` → `DRS = false`;
- `COOP LÚGOS VÍZ ... DRS` → `DRS = false`;
- `Royal Crown no sugar 1.33L` → `cukormentes / zero = false`;
- kilenc, név szerint édesítőszeres szénsavmentes üdítőnél `édesítőszerrel = false`.

A DRS mező jelenleg főként ásványvizes utakra korlátozódik, miközben legalább 638 név szerint DRS-es sör, üdítő és más ital útvonalán egyáltalán nincs deklarálva. Ez közös, csomagolt italokra alkalmazható tulajdonságot indokol.

## 8. Márka- és ízértékek

| Tulajdonság | Egyedi érték | Egyszer előforduló érték |
| --- | ---: | ---: |
| `márka` | 1 322 | 494 |
| `íz` | 911 | 290 |

Az egyedi értékek nagy száma önmagában nem hiba, de a ritka értékeket felülvizsgálati listaként érdemes kezelni. A ritkaság nem törlési szabály.

Márkának tűnő, de valószínűleg termékcsaládot, változatot vagy teljes terméknevet is tartalmazó példák:

- `Royal Boldog Névnapot!`
- `Royal Boldog Születésnapot!`
- `Angyal Borászat Mosoly Tokaji Édes Cuvée`
- `Mionetto Prosecco DOC Treviso Brut`
- `Duna-Tisza közi Muskotály`
- `Badacsonyi Olaszrizling`

A megnyitott `Royal Boldog Névnapot!` kép alapján a köszöntő a címke változata, nem önálló gyártói márka. A márkát és a termékcsaládot/változatot külön mezőben célszerű tárolni.

Az `íz` mezőben is vannak nem ízjellegű értékek, például `1895`, `10 éves`, `100% arabica espresso`, `100% robusta`, illetve kapszulaváltozatok (`n°42 tradizionale`, `n°82 vivace`). Ezeket `változat`, `összetétel`, `érlelés` vagy kávéprofil mezőbe érdemes áthelyezni.

## 9. Kategóriafa-topológiai észrevételek

Nyolc útvonalon az alkategória és az altípus neve azonos:

- `Energiaital > Energiaital`
- `Ízesített víz > Ízesített víz`
- `Pezsgő > Pezsgő`
- `Cider > Cider`
- `Sportital > Sportital`
- `Citromlé > Citromlé`
- `Funkcionális ital > Funkcionális ital`
- `Kombucha > Kombucha`

Négy alkategóriának pontosan egy, vele azonos nevű altípusa van. Ez nem adatvesztési hiba, de felesleges hierarchiaszint lehet, ha az alkalmazás nem követel minden termékhez altípust.

Tizenegy altípusban legfeljebb tíz termék van:

- 1 termék: `Alkoholmentes bor`, `Egyéb növényi ital`, `Sörválogatás`;
- 3 termék: `Gyümölcspüré`, `Gyökér alapú üdítőital`;
- 5 termék: `Citromízesítő`;
- 6 termék: `Kókuszital`;
- 7 termék: `Kevert növényi ital`;
- 8 termék: `Shot ital`, `Rizsital`;
- 9 termék: `Szójaital`.

Ezeket nem szabad pusztán alacsony darabszám miatt összevonni. Előbb azt kell vizsgálni, hogy az alacsony szám valós választékméret, más főkategóriába szétszórt termékek következménye, vagy besorolási hiány. A növényi italoknál például egyértelműen a második eset is fennáll.

## 10. Javasolt javítási sorrend

1. **Forrásrekord-séma egységesítése.** Kötelező összetett termékkulcs, egységes képmező, a nyers és normalizált márka különválasztása.
2. **Kategóriatulajdonosi döntések.** Elsőként a növényi italok 68/167-es megosztását kell rendezni; ezután a kávékrémpor/tejpor, gyümölcspüré és gyerek-partyital határokat.
3. **Biztos félrebesorolások javítása.** Koch levek, Peroni/KarlsKrone 0,0%, alkoholmentes borok és pezsgők, gyerekitalok, D.E. Karaván.
4. **Tömeges szemantikai hiba megszüntetése.** A 762 rossz helyen lévő `alkoholmentes` értéket szabályalapon, termékpéldákkal ellenőrizve kell javítani.
5. **Tulajdonságséma kanonizálása.** Azonos tulajdonságnév csak egy típussal; `kiszerelés` és `csomagolás` szétválasztása; DRS közös tulajdonsággá tétele.
6. **Ismeretlen értékek új modellje.** A `nem jelölt` ne legyen automatikusan deklarált normál érték.
7. **Névvel közvetlenül bizonyítható logikai hibák javítása.** DRS, cukormentes, édesítőszeres, bio, energiamentes, gluténmentes, szűretlen.
8. **Márka- és ízfelülvizsgálati lista.** Csak nagy biztonságú összevonások; a ritka vagy hosszú értékeket nem szabad automatikusan törölni.
9. **Minden javítási adag után független validáció.** Útvonalparitás, tulajdonságparitás, értéktípus, tiltott maradványok, hash, CSV-kapcsolat és képfájl-elérhetőség.

## 11. Javasolt automatikus ellenőrzések

A későbbi regressziók ellen érdemes a következőket külön ellenőrző parancsba vagy tesztbe tenni:

- minden eredményrekord feloldható egyetlen CSV-sorra az összetett kulccsal;
- minden `termek` objektum azonos sémát követ;
- pontosan egy képmező van, és a nem üres helyi útvonal létező fájlra mutat;
- a deklarált és használt kategóriautak megegyeznek;
- nincs termékoldali vagy kategóriaoldali árva tulajdonság;
- nincs nem deklarált érték;
- minden tulajdonságnévhez egyetlen engedélyezett típus tartozik;
- a `kiszerelés` mennyiségformátumot tartalmaz, nem csomagolási szót;
- nincs `alkoholmentes` a `termékcsalád`, `feldolgozás`, `funkció`, `minősítés` vagy `íz` mezőben;
- a névben explicit `0,0%`, DRS, cukormentes, bio stb. állítás nem mond ellent a tulajdonságoknak;
- a kategória-hash minden módosított terméknél újraszámolt és helyes;
- azonos termékcsalád ne legyen döntés nélkül több főkategória között megosztva.

## Záró megállapítás

Az Ital-ág jelenleg jó szerkezeti alapot ad, de a fa és a termékek szinkronja részben azért hibamentes, mert a hibás és ismeretlen értékek is következetesen visszakerültek a kategóriadeklarációkba. A következő körben nem újabb általános normalizálásra, hanem kategóriatulajdonosi döntésekre, célzott termékjavításokra és tulajdonságonként rögzített jelentésre/típusra van szükség.
