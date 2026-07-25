# Ital kategóriafa átalakítása – 2026-07-23

## Eredmény

- Ital-termékek: **12876 → 12810**
- Használt Ital-útvonalak: **89 → 41**
- Második szintű Ital-kategóriák: **18 → 8**
- Minden Ital-termék név szerinti harmadik szintű levélen van.
- A szénsavasság, alkoholstátusz, sör-/bor-/teatípus, célcsoport és növényi alap tulajdonságként marad meg.
- A kategóriafa, a termékutak, az értékalakok, az engedélyezett értékek és a termékhash-ek paritása ellenőrzött.

## Új kategóriafa

- **Víz és vízalapú italok**
  - Ízesítetlen palackozott víz: 420
  - Ízesített víz: 93
- **Alkoholos italok és alkoholmentes alternatívák**
  - Bor és boralapú ital: 2128
  - Pezsgő, habzóbor és gyöngyözőbor: 560
  - Sör, radler és malátaital: 1015
  - Cider: 73
  - Likőr: 601
  - Whisky és bourbon: 241
  - Gin: 135
  - Rum: 120
  - Tequila: 21
  - Vodka: 188
  - Pálinka: 133
  - Brandy: 41
  - Vermut és aperitif: 33
  - Egyéb szeszes ital: 86
  - Koktél és előre kevert ital: 125
- **Üdítőitalok**
  - Kóla: 349
  - Tonik: 87
  - Jegestea: 482
  - Limonádé: 93
  - Aloe vera ital: 21
  - Gyömbér- és gyökéralapú üdítőital: 57
  - Kombucha: 17
  - Egyéb ízesített üdítőital: 689
- **Gyümölcs- és zöldségitalok**
  - Lé: 379
  - Nektár: 84
  - Gyümölcsital: 815
  - Smoothie és püréital: 117
- **Funkcionális és teljesítményitalok**
  - Energiaital: 341
  - Sport- és izotóniás ital: 86
  - Vitamin- és wellnessital: 155
  - Egyéb funkcionális ital: 147
- **Növényi italok**
  - Egynövényes ital: 200
  - Kevert növényi ital: 31
- **Kávé-, tea- és kakaótermékek**
  - Kávé: 1301
  - Tea: 760
  - Kakaó és forró csokoládé: 138
  - Kávé- és teaadalék: 24
- **Italkészítési alapok**
  - Italszirup és folyékony koncentrátum: 395
  - Italpor és tabletta: 29

## Kikerült hibás vagy nem italjellegű termékek

- 65 citruslé/citrusízesítő → `Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Citruslé és citrusízesítő`
- Nesquik kakaós szirup (`209545089`) → `Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Desszertszósz, topping`

## Ellenőrzés

- Belső candidate-validáció: `ok`
- Független ellenőrző: `ok`
- Forrásút-lefedés: `89/89`
- Futtatás módja: `source-migration`
- Utólagos idempotenciakorrekció: 37, név szerint „enyhén szénsavas” Apenta-termék
  szénsavassága `szénsavas` helyett `enyhén szénsavas`; ismételt száraz futásban
  elvárt változás: **0 termék**.

## Automatikusan feloldott ellentmondások

Összesen 175 eset. A teljes lista a gépi audit JSON-ban található.

## Tulajdonság- és márkanormalizálás – 2026-07-24

- A végleges tulajdonságfutás **9707 terméket** módosított, majd az ismételt
  idempotenciateszt **0 módosítandó terméket** talált.
- **12720** Ital-termék rendelkezik márkával; **1105** különböző főmárka maradt.
  A betűméret- és ékezetfüggetlen márkaütközések száma **0**.
- A közvetlen Git-összehasonlítás szerint ebben a végső futásban már
  **0 márkaértéket** kellett átírni: a korábbi normalizálás eredménye a
  kiinduló fájlban is jelen volt. Az ellenőrzött 90 ismert termékvonal-,
  termékváltozat- és írásmód-alias egyike sem maradt aktív márkaértékként.
  A termékcsalád jelentése külön `termékcsalád` vagy `változat`
  tulajdonságban maradt meg.
- A bolti saját márkák továbbra is külön márkák. Példák:
  `S-Budget`, `SPAR`, `CBA Piros`, `CBA Minera`, `Barissimo`, `Solevita`,
  `Freeway` és `Bellarom`.
- Nem történt bizonytalan vállalati vagy társmárka-összevonás. Többek között
  külön maradtak a Nestlé-, Zwack-, Bacardi/Breezer-, Budweiser/Budvar-,
  Kronenbourg/1664- és SodaStream-licencmárkák.

### Elemi tulajdonságok

- A 190 korábbi vegyes gyümölcsital-rekordot tartalom alapján szétválasztottuk:
  106 lé, 50 gyümölcsital, 31 smoothie/püréital és 3 nektár.
- A `kávéfehérítő vagy tejpor` 24 összetett értéke elemi értékekre vált:
  17 kávékrémpor, 4 tejpor, 2 kávéfehérítő és 1 kávétejszín.
- Megszűntek az összetett tengelyek, például:
  `borvidék / eredet`, `szőlőfajta / borstílus`, `hatóanyag / cél`,
  `cukormentes / zero` és `kiszerelés / rendszer`.
- A korábbi összevont értékek külön elemi tengelyekre kerültek, többek között:
  `eredet`, `szőlőfajta`, `borstílus`, `hatóanyag`, `funkció`,
  `cukormentes`, `energiastátusz`, `cukrozott`, `alkoholalap`,
  `keverőanyag`, `csomagolás` és `csomagolás anyaga`.
- Az `instant` nem formaérték, hanem logikai tulajdonság. Összesen
  **421 terméknél** szerepel.
- A `kiszerelés` elemi skalár: **12531** értelmezett méret és **279**
  valóban hiányzó vagy nem biztonságosan értelmezhető adat maradt.
- **611 többdarabos csomag** mindegyikénél pozitív darabszám van; a teljes
  kiszerelés, az egységnyi kiszerelés és a darabszám számtanilag is ellenőrzött.

### Bizonyított adatjavítások

- Helyreálltak a hibás tizedes értékek, köztük az Alpro 1,8% és 3,5%
  zsírtartalmai, a Cappy 50,6% és a Rauch 99,5% gyümölcstartalma.
- A Sauska Brut Nature alkoholtartalma 12%-ra javult az
  [Sauska hivatalos termékoldala](https://shop.sauska.hu/pezsgok-27/sauska-brut-nature-nv-3117)
  alapján.
- Javítva lett az Old Jamaica 330 ml-es mérete, két többdarabos csomag
  darabszáma, valamint hat alkoholmentes sör téves 0%-os duplikátuma.

### Végső validáció

- Szigorú JSON-beolvasás: duplikált kulcs és nem véges szám nélkül.
- Független ellenőrző: `ok` – **47030 termék**, **12810 Ital-termék**,
  **41/41 deklarált és használt levél**, **5288 ellenőrzött faérték**.
- Márkakiosztás, levélkategóriák, tulajdonságszámok és kijelölt termékcsoportok
  teljes azonosító-hash alapján rögzítve.
- Hat szándékosan elrontott mintát az ellenőrző mind elutasított:
  régi márkaalias, rossz lé-kategória, helykitöltő érték, duplikált listaelem,
  összetett kiszerelés és használaton kívüli faérték.
- Végleges idempotenciateszt: `ok`, várható további változás:
  **0 termék**, kategóriafa-változás nélkül.

A korábbi gépi audit JSON az első, kategóriafa-szintű migráció részleteit
tartalmazza; ez a kiegészítő fejezet dokumentálja a későbbi tulajdonság- és
márkanormalizálást.
