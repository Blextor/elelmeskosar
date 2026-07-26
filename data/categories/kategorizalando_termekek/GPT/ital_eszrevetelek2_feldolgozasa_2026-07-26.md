# Az `ital_eszrevetelek2.txt` feldolgozása

Dátum: 2026-07-26

## Eredmény

Az `ital_eszrevetelek2.txt` minden pontját tételesen összevetettem a
kategóriafával, a 47 030 termékkel, a rendelkezésre álló helyi képekkel és a
bolti forrásadatokkal. A javítás a kategóriafát és a termékpayloadot együtt
módosítja.

A második migráció célállapota:

- összes termék: **47 030**;
- Ital-termék: **12 455**;
- ebből alkoholos ág: **5 500**, változatlan;
- nem alkoholos Ital-termék: **6 955**;
- érintett termékrekord: **3 783**;
- nem alkoholos Ital-útvonal: **24**, az alkoholos ág 15 levelével együtt
  összesen **39 Ital-útvonal**.

Az Ital-termékszám azért nő néggyel, mert hat valódi forrócsokoládé-kapszula
került át a külső kakaópor-ágból, miközben két Haas teaízesítő tabletta kikerült
az Ital ágból. A további mozgások az Ital ágon belül történtek.

## Kategóriafa

| Célútvonal | Termék |
|---|---:|
| `Ital > Ásványvíz` | 402 |
| `Ital > Ízesített víz` | 262 |
| `Ital > Energiaital` | 346 |
| `Ital > Üdítőitalok` | 1 902 |
| `Ital > Gyümölcs- és zöldségitalok` | 1 360 |
| `Ital > Funkcionális italok` | 139 |
| `Ital > Kávé-, tea- és forrócsokoládé-termékek` | 2 127 |
| `Ital > Italalapok` | 417 |

Az `Ásványvíz`, az `Ízesített víz` és az `Energiaital` közvetlen
alkategóriák lettek. Termékeiknél a projekt domináns konvenciójának megfelelően
`altipus=""`, a kategóriafában pedig üres az `altípusok` objektum.

A `Funkcionális italok` alatt csak a
`Sport-, izotóniás, kollagén- és shot ital` levél maradt.

## Cukor- és energiajelölések

### Ízesített víz

Az összevont, félreérthető `energiatartalom` mezőt öt elemi boolean váltotta:

- `hozzáadott cukor nélkül`;
- `édesítőszert tartalmaz`;
- `energiamentes`;
- `energiacsökkentett`;
- `vitamint tartalmaz`.

A 262 termékből 143 hozzáadott cukor nélküli, 79 bizonyíthatóan energiamentes,
17 energiacsökkentett. A **47 Apenta Light** rekord mindegyike
`hozzáadott cukor nélkül=true` és `energiamentes=true`; egyik sem kapott
`cukormentes` állítást pusztán a „Light” vagy a „0% hozzáadott cukor” felirat
alapján.

### Pölöskei ZERO

Mind a **18 Pölöskei ZERO** szörp természetes gyümölcscukrot tartalmaz. A
helyes modell:

- `energiatartalom="normál"`;
- `hozzáadott cukor nélkül=true`;
- `édesítőszert tartalmaz=true`.

Így a ZERO megnevezés többé nem jelent téves cukor- vagy energiamentességet.

### Gyümölcsitalok

- `Lé` (383): a haszontalan, mindenhol hamis `cukormentes`/édességi mező
  törölve, a `rostos` megmaradt.
- `Nektár` (84): a kérés nem érintette, a meglévő séma megmaradt.
- `Gyümölcsital` (776): a `cukormentes` kulcs helyett minden terméken
  `hozzáadott cukor nélkül` boolean szerepel; 54 igaz és 722 hamis érték.
- `Smoothie és püréital` (117): a `cukormentes`, `rostos` és `édesség`
  mezők törölve.

A külön képpel ellenőrzött `4604103` Sió Zero alma rekord is
`hozzáadott cukor nélkül=true`; ez nem állítja, hogy a gyümölcs természetes
cukrától is mentes.

## Kávé

A négy korábbi kávélevél egyetlen `Kávé` levélbe olvadt. A két KitKat
csokoládéital-kapszula eltávolítása után **1 299 valódi kávé** maradt.

### Forma

| Forma | Termék |
|---|---:|
| instant | 317 |
| őrölt | 256 |
| szemes | 235 |
| kapszula | 484 |
| kávépárna | 7 |

A hét Senseo párna külön `kávépárna` formát kapott, mert az „őrölt” önmagában
nem írja le a termék tényleges kiszerelését.

### Intenzitás

Minden kávé azonos szöveges skálát használ:

| Intenzitás | Termék |
|---|---:|
| gyenge | 221 |
| közepesen gyenge | 40 |
| normál | 621 |
| erős | 376 |
| extra erős | 41 |

Az exact képes/skálás kivételek megelőzik a névszabályokat. Ezért például:

- `10055660`: 5/12 → `közepesen gyenge`;
- `10107032`: 9/12 → `erős`, továbbá `koffeinmentes=true`;
- a 6/11 érték normál, míg a 6/6 érték extra erős lehet.

Skála nélkül az explicit `ristretto`, `extra strong`, `intenso`, `forte`,
`robusta`, `mild`, `delicato`, illetve a tejes/2in1/3in1 jelleg dönt; ha nincs
bizonyíték, `normál` az alapérték.

### Íz/fajta és kapszula

- `íz / fajta`: **1 299/1 299**;
- bizonyítható külön változat nélkül `natúr`: 145;
- `hány az egyben=2in1`: 25;
- `hány az egyben=3in1`: 101;
- kapszulakompatibilitás: **484/484**.

A kompatibilitási mapping az eredeti 486 kapszulát teljesen lefedi. A két
Dolce Gusto rendszerű KitKat eltávolítása után a kávék között
290 Nespresso-kompatibilis, 137 Dolce Gusto, 53 Tchibo Cafissimo,
3 Nespresso Professional és 1 Illy Iperespresso rendszerű kapszula marad.

A `2in1`, `3in1`, `intenzív`, `erős` és `lágy` értékek nem maradtak
íz/fajtaként; saját tulajdonságukba kerültek.

## Tea, forró csokoládé és italalapok

### Tea

Az Italporból 11 instant tea került át. A Tea levél így 771 termék:

- filteres: 713;
- teafű: 32;
- `por/instant`: 26.

Az utolsó értéket a felhasználói kérés szerinti pontos formában tartottam meg.

### Forró csokoládé

A levél 25-ről **33 termékre** nőtt:

- por: 24;
- kapszula: 9.

A kilenc kapszula egy már helyesen itt lévő Tesco kapszula, hat korábban a
kakaópor-ágban lévő Nesquik/Chococino/KitKat rekord, valamint két korábban
kávénak tekintett KitKat rekord. Minden terméknek van `íz`; az alapváltozatok
`natúr`, a KitKat külön elemi érték.

### Italalapok

| Levél | Termék |
|---|---:|
| Pezsgőtabletta | 8 |
| Szörp és koncentrátum | 391 |
| Italpor | 12 |
| Tejjel készítendő shake-por | 6 |

A két Haas teaízesítő az azonos bolti duplikátumokkal egyező
`Alapanyag, sütés-főzés > Cukor, édesítőszer > Édesítőszer tabletta`
útvonalra került.

Az Italporban csak nyolc Szobi és négy Frutti Kendy, vízben oldandó
üdítőitalpor maradt. Az `összetevő / íz` mezőt elemi `íz`, valamint két külön
boolean váltotta.

A hat Dr. Oetker Snack&Shake külön
`Tejjel készítendő shake-por` levelet kapott. Az elemi séma rögzíti a tejes
elkészítést, a zabalapot, a vitamindúsítást, az ízt, a hozzáadottcukor- és
édesítőszer-jelölést.

## Energiaital és üdítők

A `BTY-X17299200320021` HELL Ice Cool rekord helyes íze:

```json
["körte", "mandarin", "tuttifrutti"]
```

A hibás `karamell` és `sós` érték törölve.

Az 1 902 üdítőből korábban 1 809-nek volt íze. A hiányzó 93 rekordot egyenként
átvizsgáltam:

- 79 termékhez bizonyítható elemi íz került;
- 14 terméknél nincs elég adat biztonságos íz megadásához;
- a biztos lefedettség így **1 888/1 902**;
- a 14 fennmaradó rekord `íz kézi ellenőrzést igényel=true` jelölést kapott.

Két kategóriahiba is javult:

- `10044814` → Tonik;
- `10107811` Dr. Pepper → Kóla, `íz=["natúr"]`.

### Kézi ellenőrzést igénylő 14 üdítő

| ID | Termék | Ok |
|---|---|---|
| `121226765` | Sconto trópusi vegyesgyümölcs | A címke nem bontja elemi ízekre. |
| `121313650` | Sapinca bio vegyes gyökér ital | Sokkomponensű elixír, deklarált ízlista nélkül. |
| `121313667` | Sapinca bio gyökér- és gyümölcsital | Sokkomponensű elixír, deklarált ízlista nélkül. |
| `121328327` | Fanta Exotic 330 ml | A magyar receptúra csak trópusi aromát nevez meg. |
| `121328333` | Fanta Exotic 500 ml | A magyar receptúra csak trópusi aromát nevez meg. |
| `121328345` | Fanta Exotic 1,75 l | A magyar receptúra csak trópusi aromát nevez meg. |
| `2806122` | TESZTCIKK DOB.DRS 0.5L | Nincs értelmezhető név, kép vagy ízadat. |
| `397bc6e37dc220ca837a45d2` | Fanta Exotic 1,75 l | A magyar receptúra csak trópusi aromát nevez meg. |
| `686126:4223516` | Sweet&Fruit Multivitamin | Csak gyűjtőíz látható. |
| `838caaa45a79fdcc97eb0cbf` | Fanta Exotic 330 ml | A magyar receptúra csak trópusi aromát nevez meg. |
| `BTY-X18589600320021` | Fanta Exotic 500 ml | A magyar receptúra csak trópusi aromát nevez meg. |
| `BTY-X18589700320021` | Fanta Halloween Zero | A név és a helyi Fanta Exotic kép ütközik. |
| `d34b1319426056f2e3568e9c` | Fanta Exotic 1,75 l | A magyar receptúra csak trópusi aromát nevez meg. |
| `ec88235f1ced056dd93b44c8` | Fanta Exotic 500 ml | A magyar receptúra csak trópusi aromát nevez meg. |

## Teljes nem alkoholos audit

A 6 955 nem alkoholos Ital-termékre lefutott:

- útvonal–kategóriafa paritás;
- terméktulajdonság–deklaráció paritás;
- tulajdonságtípus-paritás (`egyedi`/`csoportos`/boolean);
- skalár, nem üres főmárka-ellenőrzés;
- ismert almárka- és alias-tiltólista;
- lapos, nem üres, foldolt duplikáció nélküli listák;
- nem kanonikus és gyűjtőíz-tiltólista;
- minden módosított `kategoria_hash` újraszámítása;
- 47 030-as össztermékszám és a változatlan 5 500-as alkoholos ág ellenőrzése.

A kategóriafa deklarációi minden érintett levélen pontosan a tényleges
termékértékekből épültek újra.

## Reprodukálhatóság és ellenőrzés

Létrehozott segédállományok:

- `alkalmaz_ital_eszreveteleket2_2026_07_26.py`;
- `ellenoriz_ital_eszreveteleket2_2026_07_26.py`;
- `ital_eszrevetelek2_kave_mapping_2026_07_26.json`;
- `ital_eszrevetelek2_udito_iz_mapping_2026_07_26.json`;
- `veglegesit_ital2_jelolteket_2026_07_26.ps1`;
- `ital_eszrevetelek2_audit_2026-07-26.json`.

Sikeres ellenőrzések:

1. Python szintaktikai fordítás mindkét scriptre.
2. Szigorú JSON-beolvasás duplikált objektumkulcs tiltásával.
3. Független Python-ellenőrző: `status=ok`, nulla hiba.
4. Node.js JSON-parse és külön darabszám/lefedettség-audit.
5. Idempotenciateszt: második futásnál `changed_products=0`, a kategóriafa
   értékhash-e változatlan.
6. Végleges termékfájl SHA-256:
   `EC3E11AB19116FC0147091857FE3FF61D28A3A31DA076E2AD15E28F9B51844E8`.
7. Végleges kategóriafa SHA-256:
   `1B0A1C30A3D95197EBDE279ABAEFB2E7D127FD72DDDD09B455C91861AFC54E5F`.
8. Hatókör-diff:
   - a 47 030 termék `termek` törzsadata és `statusz` mezője változatlan;
   - az 5 500 alkoholos termék kategóriaadata változatlan;
   - az Ital ágon kívülről pontosan hat kakaókapszula került át a megfelelő
     forrócsokoládé-levélre:
     `1005700:4543090`, `68069:3605150`, `BTY-X17735300320021`,
     `BTY-X84838600320021`, `BTY-X18992800320021`, `220010422`.

Az értéktartalom determinisztikus SHA-256 értékei:

- termékek:
  `ED93EC3FEA4D0C541E8307FEB8991BF8810F05B61C607BCF7781D6811DFCBFF8`;
- kategóriafa:
  `68B9BB36FAA83FBD1111B9FB6E2B28EC24BD58A1B069F9D92C92EA6AEF2830DF`.

## Végleges alkalmazás

A validált jelöltek tranzakciós cseréje `status=ok` eredménnyel lefutott. A
független ellenőrző ezután a tényleges főfájlokon is `status=ok`, nulla hibát
adott. A megismételt transzformáció `changed_products=0` eredménnyel igazolta az
idempotenciát.

A második javítási kör előtti állapot tartós mentései:

- `eredmeny.before-ital2-20260726.json`;
- `kategoriak_2026-06-13.before-ital2-20260726.json`.

A jelölt és az atomikus cseréhez használt ideiglenes fájlok nem maradtak vissza.

## Ismert, szándékosan nyitva hagyott pont

Csak a fenti 14 üdítő íze maradt nyitott. Ezeknél az elemi érték megadása
olvasható hátcímke, helyes termékkép vagy gyártói receptúra nélkül találgatás
lenne. A rekordok nem vesztek el és nem kaptak gyűjtőízt; géppel szűrhető
kézi-ellenőrzési jelölésük van.
