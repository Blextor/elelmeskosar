# A mesterterméklista felépítése és napi frissítése

Az első mérföldkő a júniusi bolti adatokból felépített, kézzel ellenőrizhető mesterterméklista. Ezt az állapotot le kell zárni, másolatán pedig visszajátszani a 2026. november 18-i letöltést. Így konkrét termékeken mérhető, hogy egy árváltozás, új csomagolás vagy bolti azonosítócsere után is helyes marad-e a hozzárendelés. A napi ütemezés a sikeres visszajátszást követi.

## Kiinduló állapot

| Már rendelkezésre áll | Hátralévő feladat |
|---|---|
| Tíz bolt júniusi és novemberi normalizált fájljai, 77 148 és 80 151 bolti terméksorral. A júniusi fájlok dátuma boltonként eltér. | Két rögzített bemeneti fájllista létrehozása a bolti audit `previous_file` és `normalized_file` oszlopaiból. A régi állapot építésekor minden lépés ugyanezt a fájllistát kapja. |
| A GPT-munkapéldányban kilenc bolt 47 030 júniusi termékéhez van mentett besorolás. Az Ital ág termékenkénti felülvizsgálatáról külön napló készült. A Coopshop júniusi kínálata kívül esett ezen a munkakörön. | Rögzíteni kell a fa pontos változatát, rendezni az érvénytelen útvonalakat és a munkapéldányok eltérő döntéseit. Az `assign_categories.py` történeti kimenete külön ellenőrzendő anyag. |
| A háromboltos prototípus 30 056 sorból 22 789 mestert épített, 455 csoportot ellenőrzésre jelölt. A használt párosítási jeleket is elmenti. | Tízboltos, tartós nyilvántartás kell. A prototípus minden futásban a csoportok sorrendjéből osztja ki az `MP…` azonosítókat, és az ellentmondások egy részét csak az összevonás után jelzi. |

[Bolti fájlpárok és sorszámok](../../analysis/reports/market_refresh_20261118/store_checks.csv) · [Korábbi mesterriport](../../analysis/reports/master_products_20260608_153100/summary.md) · [Mestertermék-építő](../../analysis/scripts/build_master_products.py) · [A kategóriafa auditja](../../analysis/reports/kategoriafa_20261118/summary.md) · [A termékenkénti besorolás szabályai](../../data/categories/kategorizalando_termekek/GPT/rules.txt)

## 1. Rögzített bemenet és napi adatgyűjtés

- [ ] A júniusi és novemberi fájllistában boltonként szerepeljen a forrás, az üzlet vagy kiszolgálási terület, a lekérés ideje, a nyers és normalizált fájl, az ellenőrzőösszeg és a sorszám. A részletoldalak és a kiegészítő adatforrások kapjanak külön lefedettségi állapotot. A feldolgozók explicit fájlokat és külön kimeneti könyvtárat fogadjanak.
- [ ] Minden bolt adapteréhez készüljön kis ellenőrző lekérés. Vizsgálja a végső webcímet és az átirányítást, a válasz típusát, a szükséges mezőket, egy listaoldalt és egy ismert termék részletoldalát. A teljes futás hasonlítsa össze a kategóriafák azonosítóit, neveit és szülőit, majd ellenőrizze a lapozást, a forrás által jelzett találatszámot, a duplikációkat és a sikertelen kéréseket. Egy kategória átnevezése követhető változás. Egy megszűnt katalógusvégpont bolti hibajegy.
- [ ] Boltonként legyen mezőtérkép arról, mi jön a listából, mi igényel részletoldalt, és mit ad a forrás egyáltalán. A termékhez tartozó név, márka, azonosítók, változat, kiszerelés, összetevők, allergének, használati vagy biztonsági tudnivalók, leírás és képlink maradjon visszakereshető. Ár, egységár, akció, betétdíj és készlet a bolti ajánlathoz tartozzon. A normalizált mező mellett maradjon meg a nyers érték és a forrása.
- [ ] A Tesco több, különböző kategóriájú termékén össze kell vetni a listaválaszt a részletes válasszal. A sok terméken szó szerint ismétlődő általános tájékoztató külön tárolható, és kihagyható a név- és leíráshasonlóság számításából. Az adott termékhez tartozó figyelmeztetés vagy allergén változása önálló esemény. Egy közös szövegrész felismerése önmagában ne törölhessen tartalmat.
- [ ] A napi indító alapból csak a kép URL-jét mentse. Új vagy megváltozott terméknél kérje le a szükséges részleteket. A listában láthatatlan részletoldali változások észlelésére használjon forrásoldali módosítási időt vagy időszakos újraellenőrzést. A hiányos részletek legyenek újrapróbálhatók a teljes katalógus ismételt letöltése nélkül.

**Elkészült**, ha ugyanaz a mentett válasz ugyanazt a normalizált eredményt adja, a mezőváltozás visszavezethető a nyers sorra, és egy félbeszakadt bolti futás megőrzi az utolsó teljes állapotot. A novemberi 55 hiányzó vagy nulla ár és a CoopOnline részletoldalainak időtúllépése kézzelfogható próbák erre.

## 2. A júniusi termékek besorolása és a csomagolás leírása

- [ ] Elsőként egyeztessük a kategóriafa munkapéldányait és a meglévő termékszintű döntéseket. A javítás nélküli átvételhez legyen azonosítható az eredeti termék, a döntés forrása és a ma is érvényes kategóriaút. A kétes vagy csak szkripttel címkézett sorokat adjuk termékenként a modellnek. A korábbi automatikus kizárás szintén felülvizsgálható. Minden forrássort számoljunk el.
- [ ] A csomagolásnál külön mező legyen a darabszám, a darabonkénti mennyiség és egység, az összmennyiség, valamint ahol elérhető, a nettó és lecsöpögtetett tömeg. A lédig terméknél az értékesítési egységet és a rendelési lépést külön kezeljük. A `4 × 125 g` és az `1 × 500 g` két mestertermék. Az eltérő íz, változat vagy tényleges kiszerelés szintén megkülönböztető tulajdonság.
- [ ] **Tilos szkripttel terméket kategorizálni.** Az új vagy felülvizsgálandó termék kategóriájáról, altípusáról és szemantikai tulajdonságairól a modell egyenként, szaktudással döntsön. Vesse össze a nevet, képet vagy képlinket, kiszerelést, leírást és a bolt saját kategóriáját. A bolti mező téves is lehet. A kód feladata az adatok előkészítése, a kép megjelenítése, a döntés mentése és a formai ellenőrzés. Ellentmondás, bizonytalanság vagy hiányzó faág esetén konkrét kérdés kerüljön a kézi sorba. Az új faág javaslata külön döntés.

**Elkészült**, ha a 77 148 bemeneti sor mindegyike elszámolható, a tíz bolt lefedettsége külön látszik, és egy kézi korrekció megismételt futás után is érvényben marad. [Korábbi kategória- és kiszerelési döntések](kategoria_iteracios_terv.md)

## 3. A júniusi mesterlista felépítése

Egy mester egy meghatározott termékváltozatot és fogyasztói kiszerelést jelöl. Egy mester alatt több bolt több listázása és azok korábbi azonosítói is szerepelhetnek. A változó árakat és készletet dátumozott bolti megfigyelésben őrizzük.

- [ ] Hozzunk létre tartós mesterazonosítót, belső bolti listázásazonosítót és időbeli hozzárendelést. Tároljuk a bolti ID-k és cikkszámok előzményeit, a kapcsolat érvényességét, a döntés okát és forrását. A kézi összevonás vagy szétválasztás legyen visszafejthető. Egy listázásnak egy időpontban legfeljebb egy elfogadott mestere lehet.
- [ ] Minden sorhoz rövid jelöltlistát építsünk. Először az érvényes GTIN és a jóváhagyott azonosítókapcsolatok, majd a közös vagy szomszédos kategória, márka, névrészlet, változat és kiszerelés adjon jelölteket. Az erős azonosító kategóriák között is találjon. Hiányzó vagy hibás kategóriánál legyen második keresés a márka, név és csomagolás alapján. A képlink egyezése támogató jel, a sablonkép és az URL méretparamétere kiszűrendő.
- [ ] Az összevonási döntés előtt ellenőrizzük a jelölt teljes csoportját. Ha A hasonlít B-re és B hasonlít C-re, de A és C kiszerelése ütközik, a három rekord együtt kézi eset. Egyedi, egymást megerősítő bizonyíték és csomagolási ellentmondás hiánya engedjen automatikus kapcsolatot. Önálló új mestert akkor hozzunk létre, ha a keresés lefutott és az új termék kellően azonosítható. Két életszerű jelöltnél vagy hiányos termékleírásnál maradjon függőben a kapcsolat.

**A júniusi átadás** tartalmazza a mestertáblát, a bolti hozzárendeléseket, a döntési előzményeket és a felülvizsgálandó eseteket. Az elfogadott mesterek közé csak eldöntött azonosság kerüljön. A nyitott esetek lezárása vagy kifejezett halasztása után fagyasszuk be az alapállapotot. A novemberi adatokból származó döntéseket csak a visszajátszás során használjuk fel.

## 4. AI-promptok és egyenkénti kézi döntés

A kategória és kiszerelés meghatározása, a termékazonosság eldöntése és az adatminőségi kivételek kezelése kapjon külön verziózott promptot. A meglévő AI-folyamatból a mentés és a kimenetellenőrzés újrahasználható. A modell számára a teljes fa többi ága is választható legyen, különösen téves bolti kategória esetén. A másik két prompthoz külön mintakészlet és döntésellenőrzés szükséges. A technikai letöltési hibák a bolti futási naplóba kerüljenek.

**A termékazonossági prompt kiinduló szövege**

> Egy bolti rekordot hasonlítasz a megadott mesterjelöltekhez. Vizsgáld külön a márkát, változatot, darabszámot, darabonkénti kiszerelést, GTIN-t, bolti azonosítók előzményeit és a kategóriát. Minden állításod mellé add meg a forrásmezőt és az értékét. Ha egyezést javasolsz, nevezd meg a jelöltet és azt is, mi különbözteti meg a következő jelölttől. Ha több jelölt is lehetséges, a csomagolás ütközik, vagy a döntő adat hiányzik, kérj emberi döntést egy konkrét kérdéssel. Képlinkből önmagában ne következtess a címke tartalmára.

| Prompt | Bemenet | Ellenőrizhető kimenet |
|---|---|---|
| Kategória és kiszerelés | Nyers név, bolti kategóriaút, forrásmezők, megengedett kategóriaág és meglévő korrekció | Kategóriaút, változat, csomagdarabszám, mennyiség, egység, idézett mezők vagy konkrét kérdés |
| Termékazonosság | Régi és új bolti rekord, mesterjelöltek, korábbi döntések, egyező és ütköző adatok | `egyezik`, `új_mester` vagy `kézi_ellenőrzés`, jelöltazonosító, bizonyítékok, ellentmondások és kérdés |
| Adatminőségi kivétel | Érintett mező, nyers és normalizált érték, alkalmazott szabály, régi érték | Forrással igazolt korrekció vagy nyitott ügy. Ár, GTIN, allergén és figyelmeztetés csak tényleges forrásértékkel pótolható. |

A program ellenőrizze a válasz sémáját, az idézett értékeket, az engedélyezett jelöltazonosítókat és a csomagolási feltételeket. Automatikus alkalmazás csak kézzel címkézett példákon bevált döntési szabállyal történjen. A modell saját magabiztossága önmagában kevés. Hibás válasz, sikertelen AI-hívás vagy bizonytalan eredmény esetén maradjon meg az eredeti adat és nyíljon újrapróbálható ügy.

**A kézi sorban** egy ügy mutassa egymás mellett a régi és az új rekordot, a legjobb jelölteket, a kiemelt eltéréseket, a forrás- és képlinkeket, valamint egy eldönthető kérdést. Választható művelet legyen a hozzárendelés, új mester létrehozása, téves jelölt kizárása, mezőjavítás és halasztás. A döntés a bizonyítékokkal együtt maradjon meg. Ugyanaz az eset változatlan adatokkal ne jelenjen meg másnap újra. Érdemi új bizonyíték újranyithatja.

## 5. A novemberi frissítés visszajátszása

A júniusi alap másolatára vigyük fel a tíz novemberi fájlt. Először a **bolton belüli folytonosságot** vizsgáljuk, majd az érintett listázás **mesterkapcsolatát**. Így egy átnevezett termék ártörténete és egy valóban új kiszerelés is helyesen kezelhető.

| Mi változott? | Várt kezelés |
|---|---|
| Csak az ár, akció, készlet, leírás vagy képlink | Mezőnként régi és új érték, dátumozott ajánlat vagy tulajdonság. Az igazolt azonosság megmarad. A pusztán formázási URL- vagy szövegváltozás külön jelölhető. |
| Azonos bolti ID, új név | A GTIN, márka, változat és csomagolás igazolhatja az átnevezést. Lényegi ütközésnél számoljunk a bolti ID újrafelhasználásával. |
| Új bolti ID, azonos vagy hasonló név | Egyező bolti cikkszám vagy GTIN és kompatibilis kiszerelés alapján kapcsolható a régi listázáshoz. A CoopOnline platformváltása külön teszteset. |
| A név és az ID is megváltozott | Keresés a bolt korábbi, akár inaktív listázásaiban és a releváns mesterek között. Több valószínű jelölt vagy kevés bizonyíték esetén egyedi kérdés a kézi sorban. |
| Eltérő csomagolás, új, eltűnt vagy visszatérő tétel | Az eltérő csomagolás külön mester lehet. A hiányzást csak igazoltan teljes, azonos bolti körű letöltés után rögzítsük. Visszatéréskor a korábbi kapcsolat is legyen jelölt. |

**Átvételi próba.** Készüljön kézzel ellenőrzött minta mind a tíz boltból, könnyű egyezésekkel, megtévesztően hasonló külön termékekkel és valódi ID-cserékkel. Mérjük az automatikusan elfogadott egyezések helyességét, a kimaradt valós egyezéseket, a jelöltlista találati arányát és a napi kézi esetszámot. A hibás összevonásokat külön mutassuk ki. A mintán beállított szabályokat félretett eseteken is ellenőrizzük, mielőtt napi használatba kerülnek.

**A novemberi próba eredménye** boltonkénti változáslista a 80 151 sor elszámolásával, stabil mesterazonosítókkal, indokolt új kapcsolatokkal és áttekinthető kézi sorral. Ugyanazt a novemberi bemenetet kétszer feldolgozva ugyanazok a mesterek, érvényes kapcsolatok és nyitott ügyek maradjanak. Egy szándékosan csonka bolti bemenetből ne keletkezzen tömeges eltűnés.

## 6. Napi üzem

- [ ] Egyetlen napi indító végezze a bolti ellenőrzést, letöltést, normalizálást, változáskeresést, kategorizálást, mesterhez rendelést és riportolást. Az AI csak az új, érdemben változott vagy korábban eldöntetlen eseteket kapja.
- [ ] Boltonként külön legyen futásazonosító, készültségi állapot és újraindítási pont. Az elfogadott eredmény egyben váljon aktuálissá. Egy hibás bolt mellett a többi frissülhessen. Párhuzamos indítás vagy újrapróbálás ne hozhasson létre kettős ajánlatot, mestert vagy kérdést.
- [ ] A napi összesítő mutassa a boltok frissességét, a technikai hibákat, új vagy eltűnt kategóriákat, mezőváltozásokat, új mestereket, automatikus döntéseket és a megnyitható kézi eseteket. Legyen visszaállítható az előző elfogadott állapot.
- [ ] A visszajátszás és a hibából helyreállás próbája után kerüljön a parancs napi ütemezésbe, budapesti idő szerint. Az első napi futásokon a kézi döntések és a téves párosítások alapján finomítsuk a szabályokat.

**A következő mérföldkő az egyeztetett kategóriafa és a kategóriadöntések ellenőrzött listája.** A modell először a már azonosított eltérő vagy hiányzó utakhoz tartozó konkrét termékeket vizsgálja meg. A jóváhagyott és a nyitott döntéseket külön őrizzük meg a júniusi forrásfájlok és a fa verziójával együtt. Ezekre épülhet a régi mesterlista, majd a novemberi visszajátszás.
