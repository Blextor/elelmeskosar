# A fagyasztott áruk tulajdonságszótára és termékbesorolása

A 2026. november 22-én véglegesített módosítás a fagyasztott ág mind a **3 221 bolti termékrekordját** érintette. Mindegyiknél megváltoztak a tulajdonságok, **88 terméknél a kategóriaútvonal is módosult**.

[Helyi ellenőrzőoldal](http://127.0.0.1:8765/ellenorzes/) · [Termékenkénti változásjegyzék](termekenkenti_besorolas.csv) · [Aktív kategóriafa](../../../data/categories/kategorizalando_termekek/GPT/kategoriak_2026-06-13.json) · [Végleges terméklista](../../../data/categories/kategorizalando_termekek/GPT/eredmeny.json)

## Új értékek és jelentésük

Luna minden bolti rekordhoz külön választott kategóriát és tulajdonságértékeket a bolti adatlapok, az elérhető termékképek és a korábbi besorolás alapján. A szótár ezekből a döntésekből épül fel. A szótárba a kért rögzített lehetőségek is bekerültek.

- A márka nélküli vagy azonosíthatatlan márkájú termék márkamezőjében a bolt neve szerepel. A termék neve változatlanul olvasható a jegyzékben. A pizzán a márka, a termékcsalád és a változat három külön mező. A család nélküli pizzánál a termékcsalád értéke „nincs”.
- Az együtt előforduló ízek, feltétek, alapanyagok és bevonatok külön listaelemek. A saját nevű ízek, például a Rákóczi túrós, egyben kereshetők. A desszert megnevezésében már kifejezett alapíz esetén a külön íz lehet „natúr”. A töltelék nélküli desszertek tölteléklistája üres.
- A mentességi és étrendi jelölés igaz értéke az adott termékhez alátámasztott állítást jelöli. A receptből vagy a csomag elejéről hiányzó állítás önmagában nem igazolja a mentességet.
- A zöldségeknél a megnevezés alapértéke „nyers”. A felhasználási cél külön megnevezést kaphat, például leveszöldség vagy franciasaláta-alap. Az azonosított zöldségek és gombák külön szűrőértékek.
- A készételek „tésztás” jelölése a kenyeres és a péksütemény-alapú fogásokat is magában foglalja.

A fagyasztott ágban a korábbi 89 különböző tulajdonságnév helyén 51 szerepel. A szótár a tulajdonságokat az alkalmazási szintjükön tartalmazza, így a szülőn deklarált mezőre a gyerekkategóriákban is lehet szűrni.

## Kategóriánkénti mezők

Az egyedi mező egy értéket, a többválasztós mező listát tárol. A táblázat az örökölt mezőket is tartalmazza.

A 16. pont szerinti sajtséma és a 17. pont szerinti rántott zöldség/gomba sémája külön szerepel. A 23. pont a szelet és pálcikás, a 24. pont a tégelyes fagylaltokat írja le.

A három külön „Egyéb” altípus a többi megadott formába nem illő jégkrémeknek, hal- és húskészítményeknek ad helyet. Ezek jellemzői így külön megőrizhetők, és a szomszédos altípusok pontosan a kért mezőket öröklik.

A tészták és köretek formája többválasztós. A hullámos hasábburgonya két külön formaértéke a hasáb és a hullámos.

| Hely a fában | Termék | Egyedi | Igen/nem | Többválasztós |
| --- | --- | --- | --- | --- |
| Jégkrém, fagylalt → Tégelyes | 497 | márka, forma | vízalapú, vegán, multipack, több ízű, laktózmentes, gluténmentes | íz, bevonat |
| Jégkrém, fagylalt → Tölcséres | 134 | márka | vízalapú, vegán, több ízű, laktózmentes, gluténmentes | íz |
| Jégkrém, fagylalt → Szelet és pálcikás | 415 | márka | pálcikás, vízalapú, vegán, multipack | íz, bevonat |
| Jégkrém, fagylalt → Torta | 22 | márka, forma | — | íz |
| Jégkrém, fagylalt → Egyéb | 50 | márka, forma | vízalapú, vegán, multipack | íz, bevonat |
| Fagyasztott nyers zöldségek | 350 | márka, megnevezés | keverék | zöldség/gomba |
| Fagyasztott gyümölcs | 90 | márka | magozott, mix | gyümölcs |
| Fagyasztott panírozott (nem hús) → Rántott sajt | 64 | márka, megnevezés, forma | töltött, gluténmentes, laktózmentes | sajtfajta, íz |
| Fagyasztott panírozott (nem hús) → Rántott zöldség, gomba | 44 | márka, megnevezés | — | alapanyag |
| Fagyasztott panírozott (nem hús) → Rántott egyéb | 2 | márka, megnevezés | — | — |
| Fagyasztott hal, tengeri áru → Rák, garnéla | 46 | márka | héjas, panírozott | rák/garnéla fajta |
| Fagyasztott hal, tengeri áru → Tenger gyümölcsei | 29 | márka | keverék | állat |
| Fagyasztott hal, tengeri áru → Surimi | 4 | márka | panírozott | — |
| Fagyasztott hal, tengeri áru → Halászlé, lé, sűrítmény | 15 | márka, megnevezés | halszeletet tartalmaz | halfajta |
| Fagyasztott hal, tengeri áru → Panírozott hal | 87 | márka, megnevezés | filé, ízesített, gluténmentes | halfajta, íz, panír |
| Fagyasztott hal, tengeri áru → Egész / darabolt hal | 127 | márka | filé, egész hal, bőr nélkül, ízesített | ízesítés, halfajta |
| Fagyasztott hal, tengeri áru → Kagyló | 9 | márka | héjas | kagylófajta |
| Fagyasztott hal, tengeri áru → Egyéb | 9 | márka, megnevezés | — | halfajta, forma |
| Fagyasztott tészták és köretek | 216 | márka, megnevezés | köret, gluténmentes | forma, alapanyag, íz |
| Fagyasztott desszert | 171 | márka, megnevezés | gluténmentes, laktózmentes | íz, töltelék |
| Fagyasztott péksütemény | 91 | márka, megnevezés | töltött, gluténmentes, laktózmentes, tejmentes | íz |
| Jégkocka | 8 | márka | — | — |
| Fagyasztott pizza | 189 | márka, változat, termékcsalád | csípős, mini, multipack, gluténmentes | feltét, alap |
| Fagyasztott készételek és zöldséges ételek | 171 | márka, megnevezés | zöldséges, húsos, halas, tésztás, vegán, laktózmentes, gluténmentes | összetevő / íz |
| Fagyasztott hús → Darált hús, fasírt, húsgolyó | 51 | márka, megnevezés | panírozott, töltött | állat, íz / töltelék, panír |
| Fagyasztott hús → Panírozott / töltött / pácolt hús | 196 | márka, megnevezés, forma | töltött, gluténmentes, laktózmentes | állat, íz / töltelék |
| Fagyasztott hús → Egész / darabolt nyers hús | 82 | márka, megnevezés | csomagolt | állat, testrész |
| Fagyasztott hús → Húspogácsa | 24 | márka | — | állat |
| Fagyasztott hús → Egyéb | 28 | márka, megnevezés | — | állat, testrész, előkészítés |

## Példák a termékszintű változásokra

| Termék | Bolti azonosító | Mezők az új adatokban |
| --- | --- | --- |
| AMERICAN Csirkemellcsíkok, chilis - sajtos panírban, 500g | 541450 | megnevezés = csirkemellcsík; állat = csirke; íz / töltelék = chili · sajt |
| Dr. Oetker Ristorante Pizza Salame gyorsfagyasztott pizza szalámival és sajttal 320 g | 100087:3637294 | márka = Dr. Oetker; termékcsalád = Ristorante; változat = Salame; feltét = szalámi · sajt; alap = paradicsomszósz |
| ALL SEASONS Hullámos hasábburgonya, sütőben és frtiőzben is elkészíthető, 1000 g | 995302 | megnevezés = hasábburgonya; forma = hasáb · hullámos; alapanyag = burgonya; íz = üres lista |
| aro Gyorsfagyasztott, Készre Sütött Sajttorta 1,25 kg | BTY-X4367600320021 | megnevezés = sajttorta; íz = natúr; töltelék = túró |
| METRO Chef Finomfőzelék alap Zöldségkeverék 2,5 kg | BTY-X18104600320021 | megnevezés = finomfőzelék; keverék = igen; zöldség/gomba = sárgarépa · zöldborsó |
| Classic gyorsfagyasztott halászlé alap pontyszelettel 1000 g | 220229527 | megnevezés = halászlé; halszeletet tartalmaz = igen; halfajta = ponty |
| Gyorsfagyasztott húsleveszöldség 1000 g | 207963625 | márka = Tesco; megnevezés = leveszöldség; zöldség/gomba = sárgarépa · paszternák · karalábé · petrezselyem · kelbimbó |

## Ellenőrizhetőség

A változásjegyzék minden során egymás mellett szerepel a korábbi és a végleges kategóriaútvonal, valamint a két teljes tulajdonságobjektum. **69 rekordnál** külön megjegyzés segíti az ellenőrzést. Ezeket a felület **Kivételek** szűrője mutatja.

A képi források megoszlása az induló 3 221 rekordnál.

| Képforrás | Termék |
| --- | --- |
| Helyi kép | 3 215 |
| Nincs azonosítható termékfotó | 3 |
| EAN-egyezés | 2 |
| Más boltnál azonos márka, változat és méret | 1 |

A FRoSTA hal steaknél a gyártó alaszkai tőkehalat nevez meg. A Tesco a dobozon szereplő gyártási kódtól függően más lehetséges halfajokat is feltüntet. A jelölt termékhez a bolti tétel ismeretében lehet pontosítani a halfajt. [Gyártói adatlap](https://www.frosta.hu/products/halak/hal-steak/) · [Tesco](https://bevasarlas.tesco.hu/shop/hu-HU/products/2004009503027)

A végleges listában az útvonalak, a mezőtípusok, az értékszótárak, a bolti azonosítók és a kategória-hashek ellenőrzése mind a 3 221 rekordon megtörtént.

<details><summary>Az összevetés kiinduló fájljai (SHA-256)</summary>


| Fájl | SHA-256 |
| --- | --- |
| eredmeny.json | a728e5797e71b322274f94f97de1ac07a6c8072ed75b75114e602a84a8e282e4 |
| kategoriak_2026-06-13.json | 69cc2a6015ae5dc9d9358dd9347ef3d771f4d02b9189e05735cac07d72560912 |
| észrevételek.txt | 1abe135d8471ef1e2c0268248469d8582640539d4e496cc63b666cef8bcfb46f |

</details>
