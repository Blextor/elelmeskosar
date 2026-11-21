# A fagyasztott termékek végleges besorolása

A jóváhagyott, 2026. november 21-én véglegesített állapot **3 221 fagyasztott bolti termékrekordot** tartalmaz. Közülük **1 642 termék besorolása vagy tulajdonsága változott**. 1 540 rekordnak módosult a kategóriaútvonala, ezen belül 343 másik ágba került az átnevezések és a szendvicság beolvasztásán felül. 1 091 rekordnál változtak a tulajdonságértékek. A két szám között van átfedés.

A kézi felülvizsgálat 3 124 bolti rekordra terjedt ki. A fagyasztott gyümölcsök és a jégkockák korábbi termékbesorolásait átvettük.

A kiindulópont minden sornál az észrevételek feldolgozásakor használt besorolás. A változásjegyzékben az átvezetés előtti és a végleges állapot hasonlítható össze. Luna termékenként, a bolti adatokkal és az elérhető képekkel vizsgálta a besorolási döntéseket. A fájlkezelés a képek és rekordok összeillesztését, a kézi döntések mentését és az eredmény ellenőrzését szolgálta.

[Megnyitás a helyi ellenőrzőoldalon](http://127.0.0.1:8765/ellenorzes/) · [Tételes összehasonlítás](termekenkenti_besorolas.csv) · [Aktív kategóriafa](../../../data/categories/kategorizalando_termekek/GPT/kategoriak_2026-06-13.json) · [Végleges terméklista](../../../data/categories/kategorizalando_termekek/GPT/eredmeny.json)

## A szűrők és a kategóriák változásai

- **Pizzák (1., 10. pont).** A 189 pizzarekord feltétei egyetlen többválasztós `feltét` mezőben kereshetők. A recept nevét a `pizzaváltozat` tárolhatja. A D’oro dupla paradicsomos pizzaalap a pizzák ágába kerül.
- **Nyers zöldségek (2., 8., 12. pont).** A 350 rekordra hat mező vonatkozik. A `bio` és a `mix/keverék` igen/nem jelölés, a `márka` és a `megnevezés` egyedi érték, a `zöldség/gomba` és a `forma` többválasztós. A bio jelölés a forrásokban azonosítható bio megjelölést követi. A leveszöldség vagy a finomfőzelék megnevezés mellett az azonosított zöldségek külön választhatók. A korábbi `zöldségcsoport` megszűnik. A főzéshez árult natúr, akár blansírozott zöldségek alapanyagként szerepelnek. A külön kért Fevita rizses zöldségkeverék is ide kerül.
- **Jégkrémek (3–7. pont).** A pálcikás és a szendvics altípus közös neve **Szelet és pálcikás**. Az ide sorolt 415 rekordon a `pálcikás` mező mindenhol kitöltött: 387 igen és 28 nem. A név szerint ellenőrzött Kaktus 110 ml és a SPAR citromos–epres szorbés termék a tölcséresek közé kerül.
- **Tészták, köretek és zöldséges ételek (9., 13. pont).** A natúr tészta, nokedli és a töltetlen krokett a tészták és köretek között található. Az édes töltött tészták, gombócok, derelyék és édes palacsinták desszertek. A sós töltött ételek, például a húsos gyoza és a hortobágyi palacsinta a készételek és zöldséges ételek közé tartoznak.
- **Halak és tengeri termékek (11., 14., 18. pont).** A halászlé a halas ág megfelelő altípusába kerül. Az Iglo Fish’n’Rösti burgonyás bundában lévő halfilé, így a panírozott halak közé tartozik. A panírozott rák, garnéla, surimi és a többi tengeri termék saját termékcsoportjában marad kereshető. A panír ezeknél tulajdonság.
- **Húsok (15–17. pont).** A fasírtok és húsgolyók a darált húsokhoz tartoznak, a panír vagy a töltelék tulajdonságként megőrizhető. A pácolt húsok az új **Panírozott / töltött / pácolt hús** altípusba illenek. Az aro baromfis pogácsa a panírozott húsokhoz kerül.

## Név szerint ellenőrzött példák

| Termék / fotó | Bolt és azonosító | Korábban | Végleges besorolás | Döntés alapja |
| --- | --- | --- | --- | --- |
| [Rios Bourbon vanília ízű jégkrém kakaós rétegekkel 650 ml](../../../data/markets_data/product_images/penny/3d7556996d80cecb.jpg) | Penny · 992056 | Jégkrém, fagylalt → Tégelyes | Jégkrém, fagylalt → Torta | Réteges jégkrémtorta |
| [BALLINO Csokoládés-vaníliás jégkrém](../../../data/markets_data/product_images/lidl/ef8bfb4f8ab8f27e.png) | Lidl · 10107453 | Jégkrém, fagylalt → Tégelyes | Jégkrém, fagylalt → Szelet és pálcikás | Csokoládébevonatos, pálcikás termék |
| [Kaktus citromos jégkrém és epres gyümölcsjégkrém zöld bevonattal 110 ml](../../../data/markets_data/product_images/coopshop/9862150b9e4776aa.jpg) | Coopshop · 186814 | Jégkrém, fagylalt → Pálcikás | Jégkrém, fagylalt → Tölcséres | A 110 ml-es változat tölcséres |
| [SPAR Citrom ízű jégkrém (40%) és epres szorbé (19%) epres szósszal, belül kakaós](../../../data/markets_data/product_images/spar/e2f224263f47d61e.png) | Spar · 6a2fa2e791f9d325482e7fcc | Jégkrém, fagylalt → Pálcikás | Jégkrém, fagylalt → Tölcséres | Tölcséres, epres szorbés termék |
| [Fevita gyorsfagyasztott rizses zöldségkeverék 450 g](../../../data/markets_data/product_images/coopshop/16718a7e538deeeb.jpg) | Coopshop · 41677 | Fagyasztott készétel | Fagyasztott nyers zöldségek | A megnevezés és a zöldségösszetevők külön mezőkben szerepelnek |
| [D'oro Dupla Paradicsomos Pizzaalap 560 g](../../../data/markets_data/product_images/metro/7d9bae9459cc36d8.png) | Metro · BTY-X12205600320021 | Fagyasztott tészta | Fagyasztott pizza | Paradicsomos pizzaalap |
| [Classic gyorsfagyasztott halászlé alap pontyszelettel 1000 g](../../../data/markets_data/product_images/tesco/a3b3f5c464409b3f.jpg) | Tesco · 220229527 | Fagyasztott készétel | Fagyasztott hal, tengeri áru → Halászlé, lé, sűrítmény | Halászléalap pontyszelettel |
| [Iglo Fish'n'Rösti gyorsfagyasztott halfilé ropogós burgonyás tésztában 5 db 250 g](../../../data/markets_data/product_images/auchan/8284029dd263dcd6.png) | Auchan · 32296:32299 | Fagyasztott készétel | Fagyasztott hal, tengeri áru → Panírozott hal | A burgonya a hal bundájában van |
| [aro gyorsfagyasztott baromfis pogácsa 1 kg](../../../data/markets_data/product_images/metro/b4d315241fb61583.png) | Metro · BTY-X494400320021 | Fagyasztott hús → Húspogácsa | Fagyasztott hús → Panírozott / töltött / pácolt hús | Panírozott termék |
| [Tesco gyorsfagyasztott enyhén csípős csirkeszárny édes-csilis marinádban 500 g](../../../data/markets_data/product_images/tesco/f289870ea16e23bf.jpg) | Tesco · 100888599 | Fagyasztott hús | Fagyasztott hús → Panírozott / töltött / pácolt hús | Édes-csilis marinádban |

## Az új alkategóriák mérete

| Alkategória | Közvetlenül besorolva | Altípuson | Összesen |
| --- | --- | --- | --- |
| Jégkrém, fagylalt | 38 | 1080 | 1118 |
| Fagyasztott nyers zöldségek | 350 | 0 | 350 |
| Fagyasztott gyümölcs | 90 | 0 | 90 |
| Fagyasztott panírozott (nem hús) | 0 | 110 | 110 |
| Fagyasztott hal, tengeri áru | 9 | 317 | 326 |
| Fagyasztott tészták és köretek | 216 | 0 | 216 |
| Fagyasztott desszert | 171 | 0 | 171 |
| Fagyasztott péksütemény | 91 | 0 | 91 |
| Jégkocka | 8 | 0 | 8 |
| Fagyasztott pizza | 189 | 0 | 189 |
| Fagyasztott készételek és zöldséges ételek | 171 | 0 | 171 |
| Fagyasztott hús | 26 | 355 | 381 |

A szelet alakú jégkrémeknél a pálcikát külön ellenőriztük. A 90 ml-es Milka Caramel Crunch például a gyártó szerint pálcikás, míg a pálcika nélküli szendvicseken a jelölés hamis. [Milka termékadatlap](https://www.milkaicecream.com/hu-HU/products-hu/caramel-crunch-stick-hu/)

A Tesco 1 kg-os húsleveszöldségénél az összetevőket a megfelelő bolti azonosítóhoz tartozó adatlap alapján lehet kiválasztani. A francia keverék külön termék, saját recepttel. [Húsleveszöldség](https://bevasarlas.tesco.hu/shop/hu-HU/products/207963625) · [Francia zöldségkeverék](https://bevasarlas.tesco.hu/shop/hu-HU/products/208856629)

A METRO Chef ratatouille-keverék receptjét a magyar termékadatlap és az azonos, 4337182142607 vonalkódú termék összetevőlistája kapcsolja ugyanahhoz a kiszereléshez. [Magyar adatlap](https://cdn.metro-group.com/hu/hu_fir_166350001001_hu.pdf) · [Összetevőlista](https://metro.zakaz.ua/en/products/ratatui-metro-shef-2500g--04337182142607/)

A 750 g-os SPAR Wok Gemüse keveréknél a csomag alapján azonosítható SPAR-termékadatlap adja meg a zöldségeket és a fafülgombát. [SPAR termékadatlap](https://www.spar.at/produktwelt/spar-qualitaetsmarke-wokgemuese-p2902135)

## Külön ellenőrizhető zöldségkeverékek

Ezeknél hiányos az összetevőlista, vagy a terméknév, a kép és az adatlap eltér egymástól. A végleges besorolás az igazolható összetevőket tartalmazza. Az ellenőrzőoldal **Kivételek** szűrőjével együtt is megnyithatók.

| Termék | Bolt és azonosító | Megjegyzés |
| --- | --- | --- |
| [Erdei gombakeverék 500 g](../../../data/markets_data/product_images/auchan/734f0812461df87f.png) | Auchan · 11428:11431 | Az erdei gombakeverék fajai nincsenek felsorolva; a csomag csak gombakeverékként azonosítja. |
| [Auchan Kedvenc zöldségkeverék franciasalátához gyorsfagyasztott 450 g](../../../data/markets_data/product_images/auchan/63abf7c0c8c6b223.png) | Auchan · 632438:4169828 | Franciasaláta-alap: a képen répa, borsó és burgonya látszik, de teljes összetételt igazoló lista nem található. |
| [Auchan Kedvenc gyorsfagyasztott zöldségkeverék franciasalátához 1000 g](../../../data/markets_data/product_images/auchan/e0d27ae0a308cee8.png) | Auchan · 987125:4524515 | Franciasaláta-alap: a képen répa, borsó és burgonya látszik, de teljes összetételt igazoló lista nem található. |
| [Bonduelle gyorsfagyasztott 4 évszak zöldségkeverék 400 g](../../../data/markets_data/product_images/auchan/0c4b2fede994f4b1.png) | Auchan · 102821:3640019 | 4 évszak keverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [FRoSTA gyorsfagyasztott serpenyős zöldségek ázsiai stílusban 400 g](../../../data/markets_data/product_images/auchan/9526e45cb73f353c.png) | Auchan · 765624:4303014 | Ázsiai zöldségkeverék: a leírás mungóbabcsírát és bambuszrügyet említ, de nem sorolja fel a teljes összetételt. |
| [Bonduelle gyorsfagyasztott sütőtökös krémleves zöldségkeverék 400 g](../../../data/markets_data/product_images/auchan/1153039eebb8921c.png) | Auchan · 102594:3639795 | Sütőtökös krémleves-keverék: a név és a kép csak a sütőtököt támasztja alá; további összetevők nem igazoltak. |
| [Mirsa Morzsolt Csemege Kukorica 10 kg](../../../data/markets_data/product_images/metro/e953810daad1a207.png) | Metro · BTY-X16882800320021 | A terméknév/kép csemegekukoricát jelez, a társított Metro-adatlap viszont többféle zöldségkeveréket sorol; forrásellentmondás. |
| [aro Gyorsfagyasztott Leveszöldség Alap 10 kg](../../../data/markets_data/product_images/metro/4575653cbfed194e.png) | Metro · BTY-X18301900320021 | A METRO-adat csak „tartalmazhat zellert” állít; ez nem bizonyít zöldségösszetevőt, így az összetétel nincs azonosítva. |
| [Zöldségeskert gyorsfagyasztott mexikói zöldségkeverék 1000 g](../../../data/markets_data/product_images/penny/a57502aa94223cc8.jpg) | Penny · 821414 | Mexikói keverék: a csomagképen látszó összetevők nem igazolják a teljes összetétellistát. |
| [CBA PIROS gyorsfagyasztott franciasaláta 1kg](../../../data/markets_data/product_images/prima/e0a84e6b9073a385.jpg) | Prima · 29b8469995b8e484c1e738c9 | Franciasaláta-keverék: a képen répa, borsó és burgonya látszik, de teljes összetételt igazoló lista nem található. |
| [CBA PIROS gyorsfagyasztott mexikói keverék 1kg](../../../data/markets_data/product_images/prima/60e4afc620eba8e2.jpg) | Prima · e83fa2642ba9079e57b93324 | Mexikói keverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [Bonduelle gyorsfagyasztott 4 évszak zöldségkeverék 400 g](../../../data/markets_data/product_images/prima/f1fc2a91434bcaae.jpg) | Prima · bc3c06764e2421d8eff0b893 | 4 évszak keverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [FRoSTA gyorsfagyasztott kedvenc serpenyős zöldségek 400 g](../../../data/markets_data/product_images/spar/0fc6c452a879a8b4.jpg) | Spar · 08b2a008745d2e4511c2ba4d | Kedvenc serpenyős mix: a leírás karfiolt és zöldbabot említ, de nem közli a teljes összetételt. |
| [FRoSTA gyorsfagyasztott tavaszi zöldségkeverék 400 g](../../../data/markets_data/product_images/spar/3f1492082f514da5.jpg) | Spar · cf6821195c9dff1cb77e5232 | Tavaszi zöldségkeverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [FRoSTA gyorsfagyasztott zöldségleves mix sárga színű répával 400 g](../../../data/markets_data/product_images/spar/d34f72e3a9fd3d21.jpg) | Spar · 024cd8737a1b0cf0379ede9b | Sárgarépás leveszöldség-keverék: a leírás csak a répát nevezi meg, a további összetevőket nem. |
| [S-Budget gyorsfagyasztott franciasaláta zöldségkeverék 1000 g](../../../data/markets_data/product_images/spar/fdde5f768c72bf68.jpg) | Spar · f60b92185a9e71485f21edcb | Franciasaláta-keverék: a képen répa, borsó és burgonya látszik, de teljes összetételt igazoló lista nem található. |
| [S-Budget gyorsfagyasztott zöldségkeverék 600 g](../../../data/markets_data/product_images/spar/3fa95cfbbb5ad159.jpg) | Spar · 8a8ad7e860b9b51b88e2e264 | Általános zöldségkeverék: a csomagkép mutat összetevőket, de teljes összetétellista nincs. |
| [S-Budget gyorsfagyasztott tavaszi zöldségkeverék 1 kg](../../../data/markets_data/product_images/spar/6e03c7d3d67ae56b.jpg) | Spar · f5122d6273e6e72429de44af | Tavaszi zöldségkeverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [S-Budget gyorsfagyasztott mexikói mix 1000 g](../../../data/markets_data/product_images/spar/5a4670922af3b0e3.jpg) | Spar · 5a2d299876391926d2f88d55 | Mexikói keverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [Tesco gyorsfagyasztott, keleties stílusú zöldségkeverék 450 g](../../../data/markets_data/product_images/tesco/9f5cfc398c9e18a5.jpg) | Tesco · 100579716 | Keleties zöldségkeverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [Tesco gyorsfagyasztott zöldségleves keverék 450 g](../../../data/markets_data/product_images/tesco/d15f4d99464772f1.jpg) | Tesco · 100579701 | Zöldségleves-keverék: a csomagkép nem ad teljes, ellenőrizhető összetevőlistát. |
| [Bonduelle gyorsfagyasztott sütőtökös krémleves zöldségkeverék 400 g](../../../data/markets_data/product_images/tesco/7c70eb99f4de9c82.jpg) | Tesco · 220166941 | Sütőtökös krémleves-keverék: a név és a kép csak a sütőtököt támasztja alá; további összetevők nem igazoltak. |
| [Tesco BIO gyorsfagyasztott zöldségkeverék 300 g](../../../data/markets_data/product_images/tesco/3dbfbf23ac43d525.jpg) | Tesco · 100623693 | Bio zöldségkeverék: a csomagképen látható összetevők nem igazolják a teljes összetételt. |
| [FRoSTA gyorsfagyasztott serpenyős zöldségek ázsiai stílusban 400 g](../../../data/markets_data/product_images/tesco/c5097870e257ab13.jpg) | Tesco · 105026043 | Ázsiai zöldségkeverék: a leírás mungóbabcsírát és bambuszrügyet említ, de nem sorolja fel a teljes összetételt. |
| [FRoSTA gyorsfagyasztott kedvenc serpenyős zöldségek 400 g](../../../data/markets_data/product_images/tesco/7a5d0521e4078505.jpg) | Tesco · 105029100 | Kedvenc serpenyős mix: a leírás karfiolt és zöldbabot említ, de nem közli a teljes összetételt. |
| [FeVita gyorsfagyasztott nyári zöldségkeverék 450 g](../../../data/markets_data/product_images/tesco/cc68423e5bb826f1.jpg) | Tesco · 120271884 | Nyári zöldségkeverék: a teljes összetételhez nincs gyártói lista; a csomagképen látható összetevők nem igazolják a teljes receptet. |
| [Mirelite gyorsfagyasztott dolina zöldségkeverék 400 g](../../../data/markets_data/product_images/coopshop/166fa652e8d0c051.jpg) | Coopshop · 182941 | Dolina zöldségkeverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [Coop Gyorsan Kész gyorsfagyasztott mexikói zöldségkeverék 450 g](../../../data/markets_data/product_images/coopshop/4ec7ee9fe2e05a91.jpg) | Coopshop · 186229 | Mexikói keverék: csak a csomagképen azonosítható összetevők állnak rendelkezésre; teljes összetétellista nincs. |
| [Coop Gyorsan Kész gyorsfagyasztott franciasaláta zöldségkeverék 450 g](../../../data/markets_data/product_images/coopshop/c7bc0d37c6d3719a.jpg) | Coopshop · 186231 | Franciasaláta-keverék: a képen répa, borsó és burgonya látszik, de teljes összetételt igazoló lista nem található. |

A jóváhagyott változásjegyzék az ellenőrzőoldalon a **fagyasztott aruk luna 20261121 eszrevetelek** jegyzéknél található.
