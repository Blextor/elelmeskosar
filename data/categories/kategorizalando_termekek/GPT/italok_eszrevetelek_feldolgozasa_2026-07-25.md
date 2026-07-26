# Az Ital kategóriára adott észrevételek feldolgozása – 2026-07-25

> Állapot: véglegesített célállapot.  
> Forráskövetelmény: `italok_észrevételek.txt`.  
> Az alkoholos ág ebben a körben szándékosan változatlan maradt.

## Összefoglaló

- A teljes állomány továbbra is **47 030 termék**.
- Az Ital ág a kiinduló **12 810** termékről **12 451** termékre változott.
- Az Ital ágban **7 második szintű kategória és 41 levél** van.
- A reprodukálható migráció **7 322 termék** útvonalát és/vagy
  tulajdonságait módosítja az eredeti forráshoz képest.
- A **5 500 alkoholos termék** és a teljes, 15 leveles alkoholos fanód
  tartalma változatlan.
- A nem alkoholos célterületen minden márka nem üres skalár; a
  többértékű tulajdonságok lapos, üres elem és normalizált duplikátum
  nélküli listák.
- A nyers CSV, a terméknév és a helyi képek keresztellenőrzése alapján
  további **51 rekord** főmárkája lett pontosítva; a bolti sajátmárkák
  megkülönböztetése megmaradt.
- A korábban bennmaradt `vegyes`, `vegyes gyümölcs`,
  `vegyes gyümölcslé`, `vegyes zöldség`, `citrus mix` és más ismert
  nem elemi vagy duplikált ízértékek száma a célterületen **0**.
- Az Ital céllevelek és a teljesen újraépített külső céllevelek közvetlen
  deklarációi pontosan egyeznek a termékértékekkel; a meglévő Drazsé levél
  deklarációja külön ellenőrzötten lefedi a hat áthelyezett terméket.
- Az idempotenciateszt eredménye: **0 változó termék, változatlan fa**.

## Végleges kategóriafa és termékszámok

| Második szint | Levél | Termék |
|---|---|---:|
| Ásványvíz | Ízesítetlen palackozott víz | 402 |
| Ásványvíz | Ízesített víz | 262 |
| Üdítőitalok | Kóla | 353 |
| Üdítőitalok | Tonik | 87 |
| Üdítőitalok | Jegestea | 487 |
| Üdítőitalok | Aloe vera ital | 21 |
| Üdítőitalok | Gyömbér- és gyökéralapú üdítőital | 57 |
| Üdítőitalok | Kombucha | 14 |
| Üdítőitalok | Kölyökpezsgő | 42 |
| Üdítőitalok | Egyéb ízesített üdítőital | 841 |
| Gyümölcs- és zöldségitalok | Lé | 383 |
| Gyümölcs- és zöldségitalok | Nektár | 84 |
| Gyümölcs- és zöldségitalok | Gyümölcsital | 776 |
| Gyümölcs- és zöldségitalok | Smoothie és püréital | 117 |
| Funkcionális italok | Energiaital | 346 |
| Funkcionális italok | Sport-, izotóniás, kollagén- és shot ital | 139 |
| Kávé-, tea- és forrócsokoládé-termékek | Instant kávé | 317 |
| Kávé-, tea- és forrócsokoládé-termékek | Őrölt kávé | 263 |
| Kávé-, tea- és forrócsokoládé-termékek | Szemes kávé | 235 |
| Kávé-, tea- és forrócsokoládé-termékek | Kapszulás kávé | 486 |
| Kávé-, tea- és forrócsokoládé-termékek | Tea | 760 |
| Kávé-, tea- és forrócsokoládé-termékek | Forró csokoládé | 25 |
| Kávé-, tea- és forrócsokoládé-termékek | Krém, tejpor és tejszín | 24 |
| Italalapok | Italtabletta és pezsgőkocka | 10 |
| Italalapok | Szörp és koncentrátum | 391 |
| Italalapok | Italpor | 29 |
| Alkoholos italok és alkoholmentes alternatívák | 15 változatlan levél | 5 500 |

Az Ital ágon kívüli, közvetlenül érintett céllevelek:

| Célútvonal | Végső termék |
|---|---:|
| `Baba > Bébiital, víz > Bébivíz` | 21 |
| `Tejtermékek és tojás > Növényi alternatíva > Növényi ital` | 231 |
| `Alapanyag, sütés-főzés > Sütési alapanyag > Kakaópor és kakaós italpor` | 108 |
| `Mentes, speciális > Sport táplálékkiegészítő > Energia gél` | 5 |
| `Édesség, snack, rágcsálnivaló > Cukorka, nyalóka > Drazsé` | 151, ebből 6 most áthelyezett tejízesítő szívószál |

## Tulajdonságmodell

| Terület | Megmaradó szakmai tulajdonságok | Lényegi döntés |
|---|---|---|
| Ízesítetlen víz | márka, szénsavasság | A termékcsalád, változat, célcsoport és terméktípus megszűnt; a babavíz külön céllevélre került. |
| Ízesített víz | márka, szénsavasság, íz, energiatartalom, opcionális vitamin | Egyetlen energiaállapot van: `cukormentes`, `energiacsökkentett` vagy `normál`. |
| Üdítők | márka, íz, energiatartalom, szénsavas | A `szénsavas` boolean a jegesteán nincs jelen; Kóla és Tonik íze hiány esetén `natúr`. |
| Gyümölcs- és zöldségitalok | márka, gyümölcstartalom, íz, rostos, cukormentes | A két logikai mező minden terméken explicit; százalék csak bizonyítható forrásból van. |
| Energiaital | márka, íz, cukormentes, szénsavas, opcionális koffeinmentes | A cukormentesség valódi boolean, nem a kulcs puszta jelenlétéből következik. |
| Egyéb funkcionális ital | márka, íz, funkció | A `funkció` csak `sportital`, `izotóniás`, `kollagén` és `shot` atomokat használ. |
| Kávé | márka, koffeinmentes, íz / fajta, opcionális intenzitás | Négy fizikai céllevél; eredet és pörkölési zaj nélkül. |
| Tea | márka, forma, fajta, összetevő, teatípus | Forma: 713 filteres, 32 teafű, 15 por. A fajta és az összetevő külön tengely. |
| Forró csokoládé | márka, csokoládétípus, opcionális íz | A kakaóporok nem ezen a levélen maradtak. |
| Krém, tejpor és tejszín | márka, típus | Típusmegoszlás: 19 krémpor, 4 tejpor, 1 tejszín. |
| Italalapok | márka, összetevő / íz, energiatartalom | A tablettán opcionális vitamin, a szörpön bizonyítható hígítási arány lehet. |
| Növényi ital | márka, alap, íz, cukor-/barista-/dúsítási és releváns fizikai mezők | A `zsírszegény`, hibás fehérjetartalom, Not Milk és alapanyagot ismétlő ízek megszűntek; 46 termék `barista=true`. |
| Kakaó | márka, cukrozottság, kakaótartalom, opcionális zsírtartalom | 46 natúr, 100%-os kakaópor; 62 kakaós italpor. A zsírszázalék nem lett kakaótartalomnak átnevezve. |

A technikai csomagolási mezők csak azokon a területeken maradtak meg,
ahol a követelmény nem kérte a kizárásukat. Az Italalapok esetében a
felhasználói kérés szerint a felsorolt szakmai tulajdonságokon kívül más
nem maradt.

## Elemi értékek ellenőrzése

- Minden csoportos értéklista lapos; lista vagy objektum nem lehet listaeleme.
- Üres elem és ékezet-/kisbetű-normalizálás után ismétlődő atom nincs.
- A nem alkoholos célterület szöveges domainértékeiben nincs `/`, `+`,
  `&`, `;`, vesszővel vagy „és” szóval összeragasztott többfogalmú érték.
- A keresés egyedüli vesszős találatai tizedes százalékok:
  `50,6%`, `99,5%`, `1,8%` és `3,5%`; ezek egyetlen numerikus értékek.
- A kötőjeles találatok vitaminnevek (`C-vitamin`, `B5-vitamin`,
  `B-vitamin-komplex`) vagy egyetlen zsírtartomány
  (`10-12%`, `15-18%`, `20-22%`), nem összeragasztott ízek.
- Példák a normalizálásra:
  `marakuja`/`maracuya` → `maracuja`,
  `bergamot` → `bergamott`,
  `szamóca`/`földieper` → `eper`,
  `cherry`/`black cherry` → `cseresznye`,
  `papaya` → `papaja`,
  `répa` → `sárgarépa`,
  `dragon fruit` → `sárkánygyümölcs`,
  `red grape` → `szőlő`,
  `forest fruit` → `erdei gyümölcs`,
  `szálas` → `teafű`.
- A `barack` csak akkor marad, ha a forrásból nem dönthető el a konkrét
  fajta; `őszibarack` vagy `sárgabarack` mellett a generikus duplikátum
  törlődik.
- Ismeretlen összetételnél nem találtunk ki konkrét atomokat. A
  `vegyes*` gyűjtőértékek helyett ilyenkor az ízmező marad el, amíg
  kép vagy összetevőlista alapján nem bizonyítható konkrét érték.

## Márkák

A márka minden ellenőrzött célterméken egyetlen, nem üres szövegérték.
A termékcsaládokat nem használtuk külön márkaként; a fogyasztó által
azonosítható főmárka maradt. Példák:

- `Omnia` → `Douwe Egberts`
- `BRAVO`, `YIPPY` → `Rauch`
- `Dolce Gusto` → `Nescafé`
- `Vergnano` → `Caffè Vergnano`
- `Nestlé Ricoré` → `Ricoré`
- `Viwa Vitaminwater` → `Viwa`
- `Absolute LifeStyle`, `Absolute Live` → `Absolute`
- `Prime Hydration` → `Prime`
- `The Gutsy Captain Kombucha` → `The Gutsy Captain`
- `Floewater Still`, `Floewater Sparkling` → `Floewater`
- `Füredi ION`, `Füredi OXION` → `Füredi`
- `Sodastream` → `SodaStream`
- 18 tévesen `Douwe Egberts` értékű Paloma-termék → `Paloma`
- `Glacéau Smartwater` → `Smartwater`
- `Aloe Vera Original` → `Aloe Vera`
- `Guarana No Sleep` → `Guarana`
- `Bobble Bobble` → `BOB`
- `Biancaffé` → `Biancaffè`, `Caffé Perté` → `Caffè Pertè`
- `Degli Angeli` → `Caffè Degli Angeli`
- `Panna Coctail` → `Panna Cocktail`
- a három tejízesítő szívószálon `Milky` → `Milky Sip`

Az azonos vállalati tulajdonos önmagában nem összevonási ok:
például az Eduscho nem lett Tchibo, a New Gen nem lett HELL, a Fanta és
a Sprite nem lett Coca-Cola. A bolti sajátmárkák külön maradtak:
például `SPAR`/`S-Budget`, `Tesco`/`Stockwell & Co.`,
`ARO`/`RIOBA`/`METRO Chef`, `Auchan Tipp Pannon-Aqua` és
`CBA Pannon-Aqua`. A hat valódi COOP CÍVIS csomag `Coop Cívis`; két,
Coop-jelölés nélküli csomag `Cívis`.

## Kiemelt kategorizálási javítások

- Az Apenta Vitamixx, Apenta Light, Active O2, Kubu Waterrr és a
  bizonyítható Vitamin Water termékek az ízesített vizekhez kerültek.
- Az ízesített víznél 60 név szerinti vitaminos/Vitamixx/Multivitamin
  termék és három további, forrásból igazolt rekord kapott
  `vitamin=true` értéket; a `vitamin` nem íz.
- Az energiaital ág 346 termék; az öt New Gen termék ide került.
- A másik funkcionális levélen 139 igazolt sport-, izotóniás,
  kollagén- vagy shot-termék maradt.
- Három energiazselé az Energia gél levélre került.
- Hat Dr. Oetker Snack&Shake termék az `Italpor` levélre került.
  Az elemi összetevő-/ízatomok ízenként
  `csokoládé|vanília|málna`, `zab`, `vitamin`; a két málnás termék
  energiaállapota `édesítőszeres`.
- A 33 Bubble12 szörpnél a képről bizonyítható hígítási arány
  `1:23`; más terméknél nem találtunk ki arányt.
- Hat, korábban kakaóitalpornak jelölt tejízesítő cukordrazsés szívószál
  a Drazsé levélre került, a már meglévő Quick Milk és SPAR referenciákkal
  azonos sémában.
- A kakaó céllevélen 108 termék maradt: 46 natúr kakaópor és
  62 kakaós italpor. A 25 forró csokoládé az Ital ágban maradt.
- A forró csokoládé bizonyított típuseloszlása javítás után:
  15 klasszikus, 4 ét, 4 fehér és 2 tej.
- Mind a nyolc Dr Pepper rekord a Kóla levélen van, főmárkája
  `Dr. Pepper`, íze az extra ízesítés hiánya miatt egységesen `natúr`.
- A 42 kölyökpezsgő exact termékhalmazának SHA-256 azonosítója:
  `8002ecafc6cce94539965ea8f3daff1ec19091ab900f7ac7dc38940c17df5c6d`.

## Energia- és cukorállapot

Az ellenőrzés közben kiderült, hogy egy korábbi normalizáló a
tulajdonságkulcs nevét is termékszövegként vizsgálta. Így például a
`cukormentes: false` mező puszta jelenléte is cukormentes találatot
okozhatott volna. A hibás köztes állapot nem maradt meg: az eredeti,
hash-ellenőrzött backupból újragenerált végleges állapot **2 697 rekord**
jelzőit korrigálta.

Végső, függetlenül kapuzott megoszlások:

| Terület | Megoszlás |
|---|---|
| Ízesített víz | 143 cukormentes, 16 energiacsökkentett, 103 normál |
| Üdítőital | 512 cukormentes, 78 energiacsökkentett, 1 312 normál |
| Gyümölcs-/zöldségital | 53 `cukormentes=true`, 1 307 `false` |
| Energiaital | 56 `cukormentes=true`, 290 `false` |
| Italalap | 187 édesítőszeres, 16 csökkentett, 227 normál |

A független ellenőrző szándékosan elutasítja azokat az állományokat,
amelyekben ezek a bizonyított megoszlások a korábbi kulcsnév-hiba miatt
összecsúsznának.

## Megőrzött alkoholos ág

- Termékpayload SHA-256:
  `7dac6e408bcbcf4bdfe959ed4c71b1c45b81fcc54c536c28dda6ea5e58a4bc7c`
- Fanód SHA-256:
  `dec48a3fe112273431b2c31055728990431b5b7b0cb99cd48e4b132f0afd0c33`
- Termékszám: **5 500**

## Ismert forrásadat-korlátok és tudatosan nyitva hagyott pontok

- `2806122`, `TESZTCIKK DOB.DRS 0.5L` tesztrekord. Nincs bizonyítható
  fogyasztói márkája, ezért a kitalálás helyett `márka=egyéb` maradt;
  később karanténba helyezhető.
- Hat valódi teaválogatásnál nem lett egyetlen teatípus kitalálva,
  mert a doboz több típust tartalmaz; a pontos készlethez kézi
  címkeellenőrzés kell. A `220320804` instant mézes-gyömbéres porból
  sem bizonyítható tea-alap, ezért teatípust nem kapott.
- A célterületen kívül ugyanannak a három Apenta-gélnek a duplikátuma
  (`105568150`, `105568151`, `105567923`) még
  `Apenta+ Powergel` márkával szerepel. Javasolt főmárkájuk `Apenta`,
  de a jelen kör nem terjesztette ki a módosítást erre a másik ágra.
- Kilenc, képpel ellenőrzött rekordnál az `eredmeny.json` termékblokkjából
  hiányzik néhány nyers bolt-/ár-/forrás-/képmező, miközben a CSV-ben
  megvan: a három Milky Sip és a hat Dr. Oetker Snack&Shake rekord.
  A kategorizálást a CSV-s képek alapján ellenőriztük, de a nyers
  termékmeta visszatöltése nem része ennek a tulajdonságmigrációnak.
- Az Andros Memory+ 55 ml shotként maradt; az Apenta Energy Water
  ízesített víz; a Vitamizu Yerba Mate jegestea.
- Huszonegy BCAA/L-karnitin/Amino Mix jellegű, de nem konkrétan
  sport-/izotóniás/shot néven árult termék az egyéb üdítőkhöz került.
- Következő, külön kategorizálási felülvizsgálatra jelölt csoportok:
  a smoothie/püré levél tasakos gyümölcspüréi; hat kapszulás
  forrócsokoládé-jelölt a kakaós italporok között; egy Fever-Tree
  Ginger Beer a Tonik levélen; valamint a Vegabond kókusztejpor a
  kávé-/teaadalékok között. Ezeket ez az atomossági és márkakör nem
  mozgatta át bizonytalan tömegszabállyal.
- Az alkoholos ág szemantikai tisztítása a felhasználói kérés szerint
  egy későbbi kör feladata.
- Hátoldali összetevőlista nélkül nem találtunk ki kakaó-, vitamin- vagy
  gyümölcsszázalékot.

## Fájlbiztonság és a Python-processzhibák kezelése

A gépen a futás közben ismét jelentkezett a korábban megfigyelt,
nem determinisztikus Python-folyamathiba. A Windows eseménynaplóban:

- `python312.dll`, `0xc0000005`
- `python312.dll`, `0xc0000409`
- egy további heap-hiba: `0xc0000374`

Ez nem JSON-szintaktikai kivétel volt: ugyanaz a változatlan fájl egyik
futásban strict módon betöltődött, másikban a Python-folyamat natív
memóriahibával leállt. Újraindítás és BIOS-módosítás nélkül az alábbi
védelmekkel készült el a módosítás:

- tiszta Python JSON-szkenner és -encoder;
- streamelt, SHA-256-tal visszaolvasott JSON-írás;
- `PYTHONMALLOC=malloc` futtatás és processzszintű újrapróbálás;
- a jelölt fájlok és a főfájlcsere szétválasztása;
- kétszeri jelöltellenőrzés a főfájlok módosítása előtt;
- PowerShell/.NET atomikus fájlcsere;
- hash-ellenőrzött, tartós visszaállítási másolat.

## Ellenőrzések

Sikeresen lefutott:

1. mindkét Python-script szintaktikai fordítása;
2. strict Python JSON-betöltés duplikált kulcs és nem véges szám tiltásával,
   továbbá külön Node.js `JSON.parse` mindkét főfájlon;
3. 47 030 termék és 41 Ital-levél paritása;
4. minden új Ital- és újraépített külső céllevél fa–termék
   tulajdonság- és értékparitása, továbbá a hat Drazsé-rekord
   deklarációlefedettsége;
5. márka skalár/nem üres ellenőrzés és ismert aliasok tiltása;
6. 51 exact főmárka és a sajátmárkás kivételek ellenőrzése;
7. lapos, elemi, duplikátummentes értéklisták, tiltott gyűjtőértékek
   és szemantikai aliaspárok ellenőrzése;
8. exact termékhalmazok és termékszámok ellenőrzése;
9. energia-/cukorállapot megoszlások független ellenőrzése;
10. alkoholos termékpayload- és fanódhash változatlansága;
11. független ellenőrző a jelölteken és a tényleges főfájlokon;
12. negatív kontroll: a régi fa és a hibás energiajelzőjű köztes állapot
    elutasítása;
13. külön Node.js-audit: 0 hiányzó nem alkoholos márka, 0 beágyazott
    listaelem, 0 normalizált listaduplikátum, 0 tiltott atom;
14. idempotenciateszt: `changed_products=0`,
    `category_tree_changed=false`.

Végleges főfájl-hash:

- `eredmeny.json`:
  `804B248BC371D54D01EB9D37F2D83EBC7843E5B3A067A44556B6325BB0B0FBB3`
- `kategoriak_2026-06-13.json`:
  `6D12CC9A454CFF05F8839278123CB4453255D1B58D3E5E888757D25EB9EE150F`

Eredeti, visszaállítható backup-hash:

- `eredmeny.before-italok-20260725.json`:
  `426F79FD4698CA596916484A4AEB322C50724A729992CA2262DC1C3ADF5C2E8E`
- `kategoriak_2026-06-13.before-italok-20260725.json`:
  `DD37310ACFD88DC5DE37DCEE6C031B92F1E8F9D358676D394D07ABE96FDD75D5`

## Kapcsolódó fájlok

- `eredmeny.json` – végleges termékbesorolás és tulajdonságok
- `kategoriak_2026-06-13.json` – végleges kategóriafa
- `alkalmaz_italok_eszreveteleket_2026_07_25.py` – reprodukálható,
  alapértelmezésben csak szárazon futó migráció
- `ellenoriz_italok_eszreveteleket_2026_07_25.py` – független,
  csak olvasó validátor
- `veglegesit_italok_jelolteket_2026_07_25.ps1` – hash-ellenőrzött
  Windows-tranzakciós véglegesítő
- `eredmeny.before-italok-20260725.json` és
  `kategoriak_2026-06-13.before-italok-20260725.json` – eredeti backupok
