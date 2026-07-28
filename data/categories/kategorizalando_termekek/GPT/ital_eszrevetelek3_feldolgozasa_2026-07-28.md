# Az `ital_eszrevetelek3.txt` feldolgozása

Dátum: 2026-07-28

## Rövid eredmény

Az `Ital > Alkoholos italok és alkoholmentes alternatívák` teljes ágát
átvizsgáltam a terméknevek, a meglévő tulajdonságok, a forrásadatok és – ahol
szükséges volt – a termékképek alapján.

- 47 030 termék teljes állományparitását ellenőriztem.
- 5 493 termék maradt a 15 alkoholos céllevélben.
- 102 biztos kategóriamozgatási döntés született.
- A céllevelek tulajdonságsémája egységes és minden deklarált mező kitöltött.
- A márkaváltozatok a fő márkára kerültek, a bolti saját márkák viszont
  üzletenként külön maradtak.
- A bizonytalan számszerű adatokat nem találtam ki: ezek egységesen
  `ismeretlen` értéket kaptak.

Az eredeti észrevételfájl változatlan maradt. A reprodukálható döntések a
[`ital_eszrevetelek3_dontesek_2026_07_28.json`](ital_eszrevetelek3_dontesek_2026_07_28.json),
a migráció az
[`alkalmaz_ital_eszreveteleket3_2026_07_28.py`](alkalmaz_ital_eszreveteleket3_2026_07_28.py)
fájlban vannak.

## Értelmezési döntések

Az észrevételfájl háromszor ír `Pálinka` címet. A harmadik felsorolásban szereplő
`gyógynövényes` és `egységnyi kiszerelés` mező, valamint a projekt tényleges
kategóriái alapján ezt a sort `Likőr` sémaként értelmeztem.

Az ízt, a típust/fajtát és a színt nem vontam össze. Ezek egymástól független
tengelyek:

- a `citrom` íz;
- az `IPA`, `lager`, `prosecco` vagy `keserűlikőr` fajta/stílus;
- a `világos`, `vörös`, `fehér` vagy `rozé` szín.

Az összevonás elvesztette volna a termék jelentését. Ehelyett a korábbi
`terméktípus`, `sörtípus`, `bortípus`, `típus`, `fajta` és hasonló mezők
értékei a megfelelő, külön célmezőbe kerültek. Egy csoportos mező minden eleme
önálló, elemi érték.

## Végleges alkoholos sémák

| Céllevél | Megtartott tulajdonságok |
|---|---|
| Whisky és bourbon | alkoholstátusz, márka, kiszerelés, alkoholtartalom, típus, íz, egységnyi kiszerelés |
| Vodka | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz, egységnyi kiszerelés |
| Vermut és aperitif | alkoholstátusz, márka, kiszerelés, alkoholtartalom, édesség, szín, íz |
| Tequila | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz, egységnyi kiszerelés |
| Rum | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz, fajta |
| Pálinka | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz, fajta |
| Egyéb szeszes ital | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz, fajta |
| Likőr | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz, fajta, gyógynövényes, egységnyi kiszerelés |
| Koktél és előre kevert ital | alkoholstátusz, márka, kiszerelés, alkoholtartalom, alkoholalap, fajta, szénsavasság |
| Gin | alkoholstátusz, márka, gyümölcsös, kiszerelés, alkoholtartalom, íz, fajta, egységnyi kiszerelés |
| Cider | alkoholstátusz, csomagolás, márka, kiszerelés, alkoholtartalom, íz, egységnyi kiszerelés |
| Brandy | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz |
| Bor és boralapú ital | alkoholstátusz, márka, kiszerelés, alkoholtartalom, íz, szénsavasság, puttonyszám, csomagolás anyaga, szín, édesség, eredet, bortípus, egységnyi kiszerelés |
| Pezsgő, habzóbor és gyöngyözőbor | alkoholstátusz, márka, kiszerelés, alkoholtartalom, fajta, íz, egységnyi kiszerelés, szőlőfajta, eredet, édesség, szín |
| Sör, radler és malátaital | alkoholstátusz, márka, kiszerelés, alkoholtartalom, fajta, íz, szín, egységnyi kiszerelés, csomagdarabszám, bio, gluténmentes, kézműves, szűretlen |

A Pezsgő és a Sör külön `fajta` mezője szándékos. Ebbe került az összeolvasztott
termékcsalád/stílus, miközben az íz és a szín külön maradt. Példák:
`["pezsgő", "prosecco"]`, illetve `["sör", "IPA"]`.

## Kategóriamozgatások

| Forrás | Cél | Darab |
|---|---|---:|
| Brandy | Egyéb szeszes ital | 2 |
| Egyéb szeszes ital | Bor és boralapú ital | 1 |
| Koktél és előre kevert ital | Bor és boralapú ital | 4 |
| Koktél és előre kevert ital | Egyéb szeszes ital | 7 |
| Koktél és előre kevert ital | Vermut és aperitif | 2 |
| Likőr | Egyéb szeszes ital | 4 |
| Likőr | Vermut és aperitif | 18 |
| Pezsgő | Bor és boralapú ital | 1 |
| Pezsgő | Kölyökpezsgő | 5 |
| Pálinka | Egyéb szeszes ital | 2 |
| Rum | Egyéb szeszes ital | 33 |
| Rum | Likőr | 1 |
| Sör | Funkcionális italok | 2 |
| Vodka | Egyéb szeszes ital | 3 |
| Whisky és bourbon | Egyéb szeszes ital | 14 |
| Whisky és bourbon | Likőr | 3 |
| **Összesen** |  | **102** |

Fontosabb döntések:

- a rum-, whisky-, brandy- vagy vodkaízű „spirit drink” nem lett automatikusan
  valódi rum, whisky, brandy vagy vodka;
- a mézes/fahéjas whisky alapú likőrök Likőrbe kerültek;
- az Aperol-, Campari-, Mionetto- és RIOBA aperitifek a Vermut és aperitif
  levélbe kerültek;
- a pastis, ouzo, abszint, soju és hasonló önálló párlatok az Egyéb szeszes
  ital levélbe kerültek;
- öt gyermekpezsgő az alkoholos Pezsgő levélből a Kölyökpezsgőbe került;
- két Friss+ 0,0% malátás-vitaminos ital a funkcionális italok közé került. A
  termékleírás szerint ezek üdítőital és alkoholmentes malátaital keverékei,
  hozzáadott vitaminokkal: [Tesco termékadatlap](https://bevasarlas.tesco.hu/shop/hu-HU/products/121355749).

## Típusok, fajták és ízek

### Whisky

A `whiskey`, `whisky`, `scotch`, `skót whisky`, `bourbon whisky` és hasonló
alakokat nem hagytam párhuzamos szinonimaként. A `whisky` önmagában nem
ismétlődik minden típusban; a ténylegesen bizonyítható típus – például bourbon,
skót blended vagy single malt – maradt meg. A hiányzó ízek képellenőrzés után
`natúr`, bizonytalan esetben `ismeretlen` értéket kaptak.

### Likőr és egyéb szeszes ital

A hiányzó Likőr-fajták közül 258 kapott biztos, specifikus értéket, 14 termék
más kategóriába került, 20 valódi fallback maradt. A hiányzó Egyéb
szeszesital-fajták közül 65 kapott specifikus értéket, 5 maradt fallback.

Külön marad:

- `rumalapú szeszesital`: a felhasznált alkoholalap rum;
- `rumízű szeszesital`: rumjellegű íz, de nem igazolt rumalap;
- `rumalapú likőr`: likőr, amelynek alkoholalapja rum.

A `curaçao` önálló Likőr-fajta lett; nem lett automatikusan `triple sec`.

### Koktél

A `fajta` a tényleges italt írja le, például `gin-tonik`, `rum-kóla`,
`whisky-kóla`, `Mojito`, `Piña Colada` vagy `espresso martini`. Az
`alkoholalap` külön, csoportos mező maradt. Három terméknél a szénsavasság a
névből és a képből sem volt bizonyítható; ezek `ismeretlen` értéket kaptak.

### Bor, Cherry és erősített borok

A `Cherry` szó önmagában nem kategória:

- a Frescanti és Angelli Cherry ízesített bor/boralapú ital maradt;
- a Garrone Cherry vermut/aperitif maradt;
- a cherry brandy és a meggylikőr Likőr maradt;
- a cseresznyés sör, cider és alkoholmentes ital a saját termékcsaládjában
  maradt.

A sherry és a portói erősített bor, nem vermut. A Choya sake/rizsbor a
borjellegű italokhoz került. A Garrone saját termékcsaládját a gyártó is
vermutként kezeli: [Garrone vermouth](https://www.garroneitaly.com/vermouth/).

### Pezsgő édesség

Az angol és magyar duplumokat egységesítettem, de a jogilag és technológiailag
eltérő pezsgőkategóriákat nem mostam össze. A `brut nature`, `extra brut`,
`brut` és `különlegesen száraz` megmaradt külön értéknek; az `extra dry`
magyar megfelelője `különlegesen száraz`. Az uniós kategóriák külön
cukortartományokat jelölnek:
[EU 2019/33 felhatalmazáson alapuló rendelet](https://eur-lex.europa.eu/eli/reg_del/2019/33/oj?locale=hu).

### Sör és malátaital

A `rozé` kikerült a sör színei közül. A stílusok – például `lager`,
`búzasör`, `IPA`, `stout` – a `fajta` mezőbe, a tényleges hozzáadott ízek az
`íz` mezőbe kerültek.

Az észrevételben szereplő általános „malátaital legyen radler” szabályt csak
akkor alkalmaztam, amikor a termék ténylegesen sör és üdítő keveréke. Huszonkét
képpel ellenőrzött termék valódi malátaital, ezért ezeknél a `malátaital`
megmaradt. A radler és a malátaital nem szinonima.

## Márkák

A márka fő márkát jelent, nem termékváltozatot. Példák:

- `Gentleman Jack` → `Jack Daniel's`;
- `The Singleton of Dufftown` → `The Singleton`;
- `Famous Grouse` → `The Famous Grouse`;
- `Glenlivet` → `The Glenlivet`;
- `Zwack Fütyülős` → `Fütyülős`;
- `Gilvesy Bohém Cuvée` → `Gilvesy`;
- `Gere Frici` → `Gere Attila`;
- `MALFY`, `MONKEY 47`, `CAMPARI`, `MOLINARI` → egységes hivatalos írásmód.

A `Gere Attila`, `Gere Tamás & Zsolt` és `Gere-Schubert` nem lett egyetlen
`Gere` értékre összemosva, mert külön termelői márkák. A Gere Attila saját
Frici termékcsaládja viszont `Gere Attila` lett.

A bolti saját márkák kivételként elkülönülnek, például `Aldi saját márka` és
`Auchan Kedvenc`. Márkajelzés nélküli termék `márka nélkül` értéket kapott.

## Képes és adatalapú ellenőrzés

Az audit nem névalapú tömeges találgatás volt:

- 1 226 Sör + Koktél + Egyéb szeszesital-terméket ellenőriztem 50
  képrácson;
- 1 599 töményital-terméket ellenőriztem 69 képrácson; 28 kép hiányzott;
- 2 761 Bor + Pezsgő + Cider termék márka- és képi ellenőrzése megtörtént;
- a Bor/Pezsgő hiányzó alkoholtartalom- és kiszerelésmezőinek 636 elemű
  ellenőrzése külön készült el;
- a biztos döntések és a további vizsgálatot igénylő tételek külön blokkokban
  maradtak.

A képrácsokat a
[`elokeszit_ital3_kepellenorzest_2026_07_28.py`](elokeszit_ital3_kepellenorzest_2026_07_28.py)
csak olvasó segéd készíti a rendszer ideiglenes könyvtárába.

## Fallbackek és adatkorlátok

Az ismeretlen adat nem lett kitalálva:

- Bor + Pezsgő: 520 nem bizonyítható alkoholtartalom;
- az összes alkoholos levélben együtt 601 nem bizonyítható alkoholtartalom;
- 23 nem bizonyítható teljes kiszerelés;
- három nem bizonyítható koktél-szénsavasság;
- 20 Likőr- és 5 Egyéb szeszesital-fajta, amelynél a kép és a név alapján sem
  volt igazolható specifikusabb típus.

Ezekben a numerikus/állapotmezőkben az egységes fallback `ismeretlen`.
Általános taxonómiai mezőben az `egyéb likőr`, `egyéb szeszesital`, illetve
`egyéb` továbbra is valódi gyűjtőérték lehet.

## Ellenőrzési lánc

A véglegesítés csak az alábbi ellenőrzések együttes sikere után történhet:

1. Python szintaktikai ellenőrzés és mindkét JSON külön parse-olása.
2. A 47 030 termékrekord, az összetett `(áruház, store_product_id)` kulcsok
   és a puszta azonosítók multihalmazának változatlansága.
3. A teljes `termek` forráspayload strukturális hash-paritása.
4. A célon kívüli termékek és kategóriafanódok változatlansága.
5. Mind a 102 ID pontos célútjának ellenőrzése.
6. A 15 levél pontos mezőhalmaza és single/group/bool típusa.
7. A kategóriafa deklarált értékeinek és a termékértékeknek a paritása.
8. Minden `kategoria_hash` újraszámítása és ellenőrzése.
9. Független checker, majd a migráció idempotenciatesztje.
10. Hash-ellenőrzött backup, tranzakciós csere, végül ismételt post-check.

A független ellenőrző:
[`ellenoriz_ital_eszreveteleket3_2026_07_28.py`](ellenoriz_ital_eszreveteleket3_2026_07_28.py).
A tranzakciós finalizáló:
[`veglegesit_ital3_jelolteket_2026_07_28.ps1`](veglegesit_ital3_jelolteket_2026_07_28.ps1).

## Végleges ellenőrzési eredmények

A tranzakciós véglegesítés 2026. július 28-án `ok` állapottal befejeződött.
A független ellenőrző a jelölt és a végleges fájlokon is `error_count = 0`
eredményt adott. Az ismételt migráció `changed_products = 0`, tehát a
művelet idempotens.

Összesítés:

- 47 030 termékrekord, és mind a 47 030 összetett
  `(áruház, store_product_id)` kulcs egyedi;
- 47 029 egyedi puszta `store_product_id`: a kiinduló adatban is meglévő
  `734295` azonosító egy Aldi- és egy Penny-rekordhoz tartozik;
- 5 493 alkoholos termék;
- 102 ellenőrzött kategóriamozgatás;
- 117 explicit márkadöntés;
- 1 059 explicit tulajdonságdöntéssel érintett termék;
- az első migrációban 5 487 módosult termék, a másodikban nulla;
- mind a 15 alkoholos levél illeszkedik a fa és a termékadat között;
- 116 deklarált mező és 1 889 deklarált megengedett érték esetén nulla
  hiányzó, extra vagy használatlan elem;
- 25 789 csoportos mezőben nulla üres, beágyazott, nem atomi vagy duplikált
  érték;
- 4 770 bool cellában minden érték valódi JSON `true` vagy `false`.

A forrástartalom és a célon kívüli adatok strukturális SHA-256 paritása:

- teljes `termek` forráspayload:
  `e69a45334887fee89b81fe03a99ca62569859ece24575198585da58d9da59639`;
- Ital célágon kívüli termékadat:
  `0dadb7a182e0461f36f37a7e9c05428ab766d650fc50ee362eb1ed5965ad43cd`;
- Ital célágon kívüli kategóriafa:
  `f234b770e16d1942058be9243f3b3ff48af5427d699dbf65d248d37fb4553a75`.

A végleges fájlok SHA-256 értékei:

- `eredmeny.json`:
  `88D0D1E08606B50308394FCF611B1C72B494E76437E55A0326914DAC89125705`;
- `kategoriak_2026-06-13.json`:
  `BB6B2D436A79686D473C320DC43BF45151A8B9160AC594A5C6AA2248CEBE5612`.

A tranzakció előtt készült tartós mentések:

- [`eredmeny.before-ital3-20260728.json`](eredmeny.before-ital3-20260728.json),
  SHA-256:
  `EC3E11AB19116FC0147091857FE3FF61D28A3A31DA076E2AD15E28F9B51844E8`;
- [`kategoriak_2026-06-13.before-ital3-20260728.json`](kategoriak_2026-06-13.before-ital3-20260728.json),
  SHA-256:
  `1B0A1C30A3D95197EBDE279ABAEFB2E7D127FD72DDDD09B455C91861AFC54E5F`.
