# Ital termékek kézi felülvizsgálata

Dátum: 2026-07-29

Állapot: folyamatban

## Hatókör és szabályok

- Kiinduló `Ital` termékszám: **12 455**.
- Minden terméket egyenként kell ellenőrizni a terméknév, a teljes forrásadat,
  a jelenlegi besorolás és tulajdonságok, valamint a termékkép alapján.
- A felülvizsgálat nem használ automatikus, névrészlet-alapú kategorizálást.
- Új kategória és új tulajdonság nem vehető fel.
- Tulajdonságérték csak akkor vehető fel, ha elemi, bizonyítható és szorosan az
  adott tulajdonsághoz tartozik.
- A repóban csak az `eredmeny.json`, a `kategoriak_2026-06-13.json` és ez az
  összegző fájl módosítható.
- Helyben elérhető termékkép: **11 895**. Helyi kép nélkül: **560**. A kép
  nélküli rekordoknál ezt külön jelezni kell, és csak a névvel vagy más
  bizonyítható forrásadattal alátámasztott érték módosítható.

## Előrehaladás

| Ellenőrzött | Összes | Készültség |
|---:|---:|---:|
| 5533 | 12 455 | 44,42% |

Az előrehaladás egyedi termékazonosítók alapján számol. A korábbi 2 734-es
érték 45 olyan Bikavér-rekord második ellenőrzését is új termékként számolta,
amely az első tételcsalád után a sorszámos borkötegekben ismét szerepelt.

## Kategóriafa-értékek változásai

Ez a rész tartalmazza az összes felvett és törölt megengedett értéket
kategóriánként és tulajdonságonként.

| Kategóriaút | Tulajdonság | Felvett értékek | Törölt értékek | Indok |
|---|---|---|---|---|
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | íz | `keserűnarancs`, `sárgadinnye`, `fekete ribizli` | `kávé` | A három új értéket konkrét terméknév és kép igazolja. A `kávé` mind a 35 használata Bikavér-rekordból, hibás részszóillesztésből származott. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | csomagolás anyaga | `fém` | – | Két Lafi Hugo Frizzante termék alumíniumdobozos; a korábbi `egyéb` nem volt kellően pontos. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | szín | `kék` | – | A Lafi Hugo Blue Lagoon folyadéka a képen egyértelműen kék. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Gazdától az asztalig` | – | A Gris Sable de Camargue rekord teljes forrásadata ezt a márkanevet adja; a korábbi `Pillangósvirágú` egy másik termékcsaládból került rá. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Görögország` | – | A Mavrodaphne görög eredetű, édes, erősített vörösbor; az országérték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | – | `Voilá` | Mind a tizenegy Voilá rekordot kézzel a pezsgőkoktélok közé soroltuk; a borágban nem maradt ilyen márkájú termék. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | – | `Primitivo Puglia`, `Tolnai Chardonnay` | A kézi ellenőrzés igazolta, hogy ezek szőlőfajta- és eredetleírások, nem márkák; a javított rekordok után egyik értéket sem használja más borrekord. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | – | `Badacsonyi Olaszrizling` | Mindkét ilyen nevű rekordnál a név a borvidéket és a szőlőfajtát írta le, nem márkát; a kézi javítás után az érték használatlan lett. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Cape Bridge` | `Green Cape` | A 2024-es Sauvignon Blanc közvetlen termékképe és specifikációja `Cape Bridge` márkát és dél-afrikai eredetet igazol; a téves `Green Cape` érték más borrekordon nem szerepelt. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Domaine de la Chézatte` | – | A Sancerre Blanc közvetlen termékképén olvasható birtoknév és a termelő hivatalos oldala egyaránt ezt igazolja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Weinhaus` | – | A két Egri Bikavér pontos termékneve, címkéje és a gyártó termékkínálata egyaránt Weinhaus márkát igazol; a korábbi `márka nélkül` érték pontatlan volt. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `André Vonnier` | `BELLUSSI ANDRE VONNIER` | A közvetlen címke és a METRO saját Beaujolais Nouveau termékének hivatalos megnevezése egyaránt André Vonnier márkát igazol. A törölt érték két külön nevet fűzött össze, és más borrekord nem használta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | csomagolás anyaga | `papír` | – | A Sol Montis 5 literes Sárgamuskotály közvetlen termékképe kartondobozos kiszerelést mutat, a pincészet pedig az 5 literes termékeit Bag-in-Boxként jelöli. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Zala` | – | A Dóka Éva Riesling közvetlen termékképe a tételt, a pincészet hivatalos termék- és borvidékoldala pedig a zalai eredetet igazolja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Castilla` | – | A Batuta Tempranillo 12,5%-os pontos termékforrása a Vino de la Tierra de Castilla eredetjelölést adja meg; az érték önálló, elemi boreredet. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Bősz Adrián` | – | Az Odonata közvetlen címkéjén és palackzáró fóliáján is kizárólag a Bősz Adrián név szerepel; a pontos termékforrás gyártóként is a Bősz Borászati Kft.-t adja meg. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Németország` | – | A Hüttenglut 9%-os, 10 literes forralt bor pontos METRO-termékadata és a csomagolás címkéje német gyártást igazol. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | íz | `fűszeres` | – | A Hüttenglut pontos termékadata szegfűszeg-, fahéj-, narancshéj- és citromhéjkivonatot sorol fel; a gyűjtőérték elemi ízjelző és közvetlenül az íz tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Ostoros` | – | Az Ostoros Birtok Egri Bikavér és Merlot Édes közvetlen címkéje, termékneve és a pincészet hivatalos márkaszűrője az `Ostoros` márkaformát igazolja. Az `Ostorosbor` érték megmarad, mert további 110, még felül nem vizsgált rekord használja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Románia` | – | Az Angelli Bianco gyártói termékadata és román termékforrása egyaránt román eredetet igazol; az országérték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Füred` | – | A Zelna közvetlen palackcímkéje `FÜRED` eredetmegjelölést és a Balatonfüred–Csopaki borvidéket is közli. Az uniós termékleírás a `Füred` OEM-et önálló eredetmegjelölésként különíti el a `Balatonfüred-Csopak` OEM-től, ezért nem olvasztottuk be a `Balatonfüred` értékbe. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Mosel` | – | A Tesco Finest Riesling Mosel Steillage közvetlen termékadata és a pontos brit termékoldal egyaránt Mosel eredetet igazol; az érték önálló, elemi borvidék. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Ribera del Duero` | – | A Tesco Finest Ebeia pontos termékneve, közvetlen termékadata és szakmai terméklapja egyaránt Ribera del Duero eredetet igazol; az érték önálló, elemi eredetmegjelölés. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Saint-Chinian` | – | A Tesco Finest Saint-Chinian közvetlen termékadata a francia Saint-Chinian eredetmegjelölést igazolja; az érték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Swartland` | – | A Tesco Finest Swartland Shiraz pontos termékneve és termékadata, valamint a dél-afrikai eredetvédelmi nyilvántartás Swartlandot önálló termőterületként igazolja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Vigneti delle Dolomiti` | – | A Tesco Finest Pinot Grigio Blush pontos termékneve és közvetlen termékadata a Vigneti delle Dolomiti földrajzi eredetjelölést igazolja; az érték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Moldova` | – | A Fantasy Cabernet Sauvignon pontos Tesco-termékadata „Bor Moldovából” származást és Moldova országot közöl; az országérték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Valdepeñas` | – | A Viña Albali Rosado Tempranillo pontos gyártói terméklapja a bort a D.O. Valdepeñas eredetmegjelöléshez köti; az érték önálló, elemi boreredet. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Belgium` | – | A Night Orient Rosé Tempranillo pontos Tesco-termékadata Belgiumot adja meg származási helyként és országként; az országérték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | eredet | `Szlovákia` | – | Az Aperitivo Bianco pontos Tesco-termékadata Szlovákiát adja meg származási országként; az országérték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Günzer` | – | A Günzer Rosé pontos termékneve és közvetlen palackcímkéje a `Günzer` márkaformát igazolja. A `Günzer Tamás` érték megmarad a név szerint Günzer Tamás-termékekhez. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Wairau Cove` | – | A pontos Tesco-termékoldal és a bor független szakmai adatlapja egyaránt `Wairau Cove` márkanéven azonosítja a Marlborough Sauvignon Blanc-t; az érték elemi és közvetlenül a márka tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | íz | `mojito` | – | A Royal Hugo Mojito neve, közvetlen címkéje és pontos Tesco-termékleírása szó szerint mojito ízű boralapú koktélt igazol; az érték elemi és közvetlenül az íz tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | `Gere & Schubert` | – | A két közvetlen palackcímke és a pincészet hivatalos neve egyaránt az ampersandos márkaformát igazolja. A `Gere - Schubert` érték megmarad, mert további 19, még felül nem vizsgált borrekord használja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Bor és boralapú ital | márka | – | `HHattyús` | Az egyetlen ilyen rekord forrásnevében kettőzött kezdőbetű szerepelt, a közvetlen címke és a termelő hivatalos terméklapja egyaránt `Hattyús` márkát igazol. A javítás után a hibás érték használatlan lett. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | márka | `Voilá` | – | Tizenegy Voilá pezsgőkoktél kézi átsorolásával került a pezsgőágba. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | fajta | `pezsgőkoktél` | – | A terméknév és a pezsgős csomagolás alapján pontos, elemi termékfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | íz | `áfonya` | – | A Voilá áfonya pezsgőkoktélok igazolják. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Németország`, `Somló` | – | A Stolzenfels pontos ALDI-termékadata német eredetet, a Kreinbacher Extra Dry pontos Tesco-termékadata Somlói borvidéket közöl. Mindkét érték elemi és közvetlenül az eredet tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | fajta | `részben erjedt szőlőmust` | – | A Natara Quattrosé pontos termékneve ezt a termékfajtát közli; nem gyöngyözőbor. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Furmint`, `Pinot Blanc`, `Pinot Noir` | – | A Kreinbacher Extra Dry pontos termékadata a már meglévő Chardonnay mellett ezt a három szőlőfajtát is tételesen megadja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Champagne` | – | A Laurent-Perrier hivatalos termékoldala a La Cuvée-t Champagne-ként azonosítja; az érték önálló, elemi eredetmegjelölés. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Hárslevelű`, `Kékfrankos`, `Meunier` | – | A Château Dereszla Vintage pontos termékadata Hárslevelűt, a Kreinbacher Rosé Brut hivatalos összetétele Kékfrankost, a Laurent-Perrier hivatalos La Cuvée-oldala pedig Meunier-t közöl. Mindhárom érték elemi szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Kunság` | – | A felülvizsgált, 12%-os Gedeon Birtok Brut pontos szakmai termékadata a tételt a Kunsági borvidékhez köti; az érték önálló, elemi boreredet. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Generosa`, `Rizlingszilváni`, `Zenit`, `Zöld veltelini` | – | A Gedeon Birtok Brut pontos adata Generosa és Zöld veltelini, a Juhász Eufória hivatalos termékoldala Chardonnay mellett Rizlingszilváni és Zenit szőlőfajtát közöl. Mind a négy érték elemi szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | márka | `Louis François & Co.` | `Treviso` | A Louis François & Co. Brut Nature közvetlen függőcímkéje és pontos termékforrása az önálló márkanevet igazolja. A `Treviso` az egyetlen ilyen márkaértékű rekordnál eredetmegjelölés volt; márka nem olvasható a közvetlen palackképen, ezért a rekord `márka nélkül` értéket kapott, a hibás márkaérték pedig használatlanná vált. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Glera`, `Moscato Bianco` | – | A Prosecco DOC-termékeket a közvetlen terméknevek és képek, valamint a termékleírások Glera-alapúként igazolják. A Martini Asti gyártói oldala és az Asti DOCG termékleírása Moscato Bianco szőlőfajtát közöl. Mindkét érték elemi szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Asti` | – | A Martini, Gancia és Cinzano Asti közvetlen neve, palackképe és DOCG-termékadata az Asti eredetmegjelölést igazolja; az érték önálló, elemi boreredet. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | márka | `Pata Negra`, `Juvé & Camps` | `J. Garcia`, `Juve & Camps` | A két Cava közvetlen palackcímkéje a Pata Negra, illetve az ékezetes Juvé & Camps márkaformát mutatja. A két korábbi érték csak ezen az egy-egy rekordon szerepelt, és a javítás után használatlanná vált. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | fajta | `cava` | – | Négy közvetlenül Cava néven forgalmazott, spanyol eredetű terméknél ez a pontos, elemi termékfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Valdobbiadene`, `Spanyolország`, `Emilia-Romagna` | – | A Mionetto DOCG neve és gyártói lapja Valdobbiadenét, a négy Cava termékadata Spanyolországot, a Chiarli műszaki lapja pedig Emilia-Romagnát igazolja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Macabeo`, `Xarel-lo`, `Parellada`, `Sauvignon Blanc`, `Királyleányka`, `Lambrusco` | – | A Cava műszaki lapok az első három fajtát, a Comedy Wine közvetlen dobozcímkéje a Sauvignon Blanc-t, az Etyeki Kúria terméklapja a Királyleánykát, a Chiarli műszaki lapja pedig a Lambruscót igazolja. Mindegyik önálló szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Magyarország`, `Veneto` | – | A magyar országértéket a konkrét Törley, Hungaria, Szovjetszkoje Igrisztoje és BB termékadatok, a Venetót pedig a Pra’della Luna Prosecco DOC Millesimato Brut pontos műszaki adata igazolja. Mindkettő elemi eredetérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Menoir`, `Muscat Ottonel` | – | A Gere Rosé Frici hivatalos termékleírása Menoir és Kékfrankos, a fehér Fricié Királyleányka, Sauvignon Blanc és Muscat Ottonel házasítást közöl. A két új érték önálló szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | íz | `narancs` | – | Az Allini Bitterol Sprizz pontos termékadata aromatizált gyümölcsborkoktélt és narancsaromát közöl. A `narancs` önálló, elemi ízérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Bianca` | – | Az Arvenus száraz fehér pezsgő szakmai versenyadata Bianca és egyéb szőlőfajták házasítását közli. A Bianca önálló szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | márka | – | `Arnevus` | Az egyetlen `Arnevus` értékű rekordnál a termékkép felirata és a szakmai versenyadat egyaránt az `Arvenus` márkaalakot igazolja. A javítás után a hibás érték használatlanná vált. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | márka | `ANDRÉ GALLOIS` | – | A pontos francia METRO-katalógus és a termék GTIN-hez kötött adata egyaránt André Gallois néven azonosítja a 10,5%-os Vin Mousseux Brut terméket. Az `ADRIEN ROMET` név egy szomszédos Blanc de Blancs tételből fűződött a forrásnév elé. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Burgundia`, `Franciaország`, `Mór` | – | A Valentin Vignot Crémant de Bourgogne pontos termékadata Burgundiát, az André Gallois és Adrien Romet tételek Franciaországot, a két Paulus termék pontos adata pedig Mórt igazolja. Mindhárom önálló, elemi eredetérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Tramini` | – | A 12%-os Babarczi Buborczi pontos termékadata Tramini, Cserszegi fűszeres és Irsai Olivér házasítást közöl. A Tramini önálló szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Muscat Lunel` | – | A Törley Fortuna Doux pontos termékadata Irsai Olivér, Muscat Lunel, Muscat Ottonel és Rizlingszilváni házasítást közöl. A Muscat Lunel önálló szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Badacsony`, `Balatonfüred-Csopak` | – | A Laposa Méthode Charmat Balatoni Extra Dry pontos termékadata Badacsony borvidéket, a Feind Coupé Extra Dry pontos termékadata és a pincészet termőhelyadata Balatonfüred-Csopak borvidéket igazol. Mindkettő önálló, elemi boreredet. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Asolo` | – | A La Gioiosa Asolo Prosecco Superiore DOCG közvetlen palackcímkéje és hivatalos termékadata az Asolo eredetmegjelölést igazolja; az érték önálló, elemi boreredet. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | eredet | `Mendoza` | – | A CHANDON Brut pontos hivatalos termékadata Argentínát és Mendozát, valamint Chardonnay–Pinot Noir házasítást igazol. A Mendoza önálló, elemi boreredet. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Garganega` | – | A Cinzano To-Spritz közvetlen címkéje és a pontos termékadat Glera–Garganega házasítású, Veneto eredetű Vino Spumantét igazol. A Garganega önálló szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Pinot Grigio` | – | A Tesco Finest Prosecco DOC 0,75 és 0,375 literes pontos gyártói termékadata Glera, Chardonnay, Pinot Blanc és Pinot Grigio házasítást közöl. A 0,2 literes lap az azonos fajtát `Pinot Gris` szinonimával nevezi meg; ezt az egységes `Pinot Grigio` értékre normalizáltuk. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | szőlőfajta | `Riesling` | – | A Natara Extra Dry 11%-os pontos szakmai terméklapja Riesling, Cserszegi fűszeres és Bianca házasítást közöl. A Riesling önálló, elemi szőlőfajta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pezsgő, habzóbor és gyöngyözőbor | márka | `The Sparkling T` | – | A The Sparkling T Alba közvetlen palackcímkéje és pontos termékforrásai egyaránt ezt a márkanevet használják. A név önálló, elemi márkaérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `märzen` | – | A Zipfer Märzen termékneve és közvetlen dobozcímkéje egyaránt ezt a pontos, önálló sörstílust igazolja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `dortmunder` | – | A DAB Export és DAB Lager közvetlen címkéje `Dortmunder Export`, illetve `Dortmunder Lager` megjelölést tartalmaz. A Dortmunder önálló, elemi sörstílus. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `Cold IPA` | – | A Hübris Hüpped gyártói termékoldala `DDH Cold IPA` stílust közöl. A Cold IPA önálló, elemi sörstílus. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `braggot` | – | A Mad Scientist Matrix Red Pill pontos termékadata eperrel és lime-mal készített, alacsony alkoholtartalmú gyümölcsös braggotként azonosítja a tételt. A braggot önálló sör–mézsör hibrid stílus. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `sour ale` | – | A Horizont Rebel Berry gyártói termékadata málnás Sour Ale stílust közöl. A sour ale önálló, elemi sörstílus. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `imperial pilsner` | – | A Szent András Monarchista közvetlen címkéje, teljes termékneve és a főzde saját termékoldala egyaránt `imperial pilsner` stílust közöl. Ez önálló, elemi sörstílus. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `witbier` | – | A Szent András Hegemónt a főzde saját oldala dubbelwitként, a Hübris Büza gyártói oldala Belgian Wit Beerként azonosítja. A közös, elemi stílusérték a `witbier`. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | fajta | `schwarzbier` | – | Az Adelskronen 5%-os barna sör közvetlen dobozfelirata `Schwarzbier`; a BJCP stílusleírása ezt önálló sötét német lagerként határozza meg. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | íz | `fűszeres` | – | A Hegemón gyártói leírása koriandermagot, a Hübris Büza gyártói leírása thai citromfüvet, zöld kardamomot és koriandermagot közöl; utóbbi közvetlen termékneve és címkéje is fűszeres búzasörként nevezi meg. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | csomagdarabszám | `11` | – | Az Erdinger Weissbräu pontos forrásneve szó szerint `0,5 l x 11` csomagot közöl; a darabszám önálló, elemi csomagadat. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Sör, radler és malátaital | kiszerelés | `5500 ml` | – | Az Erdinger Weissbräu igazolt 11 × 500 ml-es csomagjának teljes kiszerelése 5500 ml; az érték elemi mennyiségadat. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Vermut és aperitif | márka | – | `RIOBA` | A két `RIOBA Madruzzo` nevű aperitif közvetlen címkéje és forrásbeli márkamezője egyaránt `Madruzzo` márkát igazol. A kézi javítások után a `RIOBA` értéket a levél egyetlen terméke sem használta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Rum | márka | `The Demon's Share` | `The Demons Share` | Mind a négy érintett terméknév, forrásbeli márkamező és közvetlen palackcímke az aposztrófos alakot igazolja. A négy rekord egységesítése után a hibás érték használata megszűnt. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Gin | íz | `borsmenta`, `csonthéjas gyümölcs`, `mandarin`, `piros ribizli`, `szeder` | – | A The Foxtale Pink gyártói leírása borsmentát, a Hendrick's Grand Cabaret csonthéjasgyümölcs-profilt, a Bombay Sapphire Sunset spanyol mandarint, a Gordon's Premium Pink piros ribizlit, a Brockmans gyártói oldala pedig áfonya mellett szedret igazol. Mind az öt önálló, közvetlenül bizonyított ízérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Pálinka | íz | `fűszeres` | – | A Bolyhos Ágyas Fűszeres Cseresznye teljes termékneve közvetlenül igazolja a cseresznye melletti fűszeres ízjelleget; az érték önálló és közvetlenül az íz tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Whisky és bourbon | íz | `IPA` | – | A Jameson Caskmates IPA teljes neve és közvetlen címkéje az IPA-hordós finist egyértelműen azonosítja. Az érték önálló és közvetlenül az íz tulajdonsághoz tartozik. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Whisky és bourbon | típus | `single malt ír whisky` | – | A Connemara közvetlen dobozfelirata szó szerint `Peated Single Malt Irish Whiskey`; az új érték önálló és pontos whisky-típus. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Whisky és bourbon | típus | `kevert kanadai whisky` | – | A Black Velvet két közvetlen palackcímkéjén a `Blended Canadian Whisky` megjelölés olvasható. Az új érték önálló és pontos whisky-típus. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Vodka | íz | `ismeretlen` | – | A Várda Sósborszesz neve és az Auchan összetevőadata ízesített vodkát, illetve mesterséges ízesítőszereket igazol, de a konkrét ízt nem nevezi meg. A biztonságos visszaeső érték megakadályozza a téves `natúr` besorolást és a találgatást. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Vodka | íz | `gyógynövény` | – | A Kaiser Herbal pontos termékneve közvetlenül gyógynövényes változatot igazol; az érték elemi, és kizárja a téves `natúr` besorolást. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Vodka | kiszerelés | – | `20 ml`, `35 ml` | A két érték egy-egy terméknévből kihagyott nullából keletkezett. A teljes forrásmennyiségek 200 és 350 ml-t igazoltak; a javítás után egyik hibás értéket sem használja termék. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Vodka | egységnyi kiszerelés | – | `20 ml`, `35 ml` | A két érték ugyanazon hibásan rövidített Royal-rekordokból származott; a forrásrekordok és a 0,35 literes címke 200, illetve 350 ml-t igazoltak. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `mogyoró` | – | A Bottega Gianduia gyártói terméklapja valódi mogyorópasztát és csokoládé–mogyoró ízt igazol. A korábbi `földimogyoró` eltérő alapanyagot jelentett; a `mogyoró` önálló, elemi ízérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `kannabisz` | – | A Cannabis Spirit Classic48 teljes termékneve és közvetlen palackcímkéje szó szerint kannabisz–tea likőrt igazol. A `kannabisz` önálló, elemi ízérték; pontosabb a korábbi gyűjtő `gyógynövény` értéknél. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | márka | `Ramazzotti` | `Ramazotti` | A Limoncello közvetlen palackcímkéje és a gyártó hivatalos termékoldala egyaránt a két `z` betűs `Ramazzotti` márkaalakot igazolja. A hibás értéket csak ez az egy rekord használta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `fekete cseresznye` | – | A Fütyülős pontos termékneve, a gyártó termékoldala és termékkatalógusa egyaránt fekete cseresznyét igazol. Az érték önálló, elemi íz, ezért pontosabb a korábbi általános `cseresznye` értéknél. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | márka | `Kunság-Szesz` | `Kunság` | A teljes forrásnév és a közvetlen palackcímke is `KUNSÁG-SZESZ` márkát mutat. A rövidített `Kunság` értéket a javítás után más likőrrekord nem használja. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `fűszeres`, `mézeskalács`, `vörös áfonya` | – | A két gömb alakú ginlikőr eredeti csomagolásán szó szerint `Orange & Gingerbread`, illetve `Spiced Orange & Cranberry` olvasható. A három magyar érték önálló, elemi íz, és pontosabb a korábbi `gyömbér`, illetve `áfonya` besorolásnál. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `bodzavirág` | – | A Tatratea Flower közvetlen palackcímkéje és gyártói terméklapja a bodzavirágot nevezi meg a változat meghatározó ízeként. A `bodzavirág` önálló, elemi és közvetlenül bizonyított ízérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | kiszerelés | `540 ml` | – | A két St. Hubertus ajándékcsomag teljes neve, forrásmennyisége és közvetlen csomagképe egyaránt egy 500 ml-es palackot és egy 40 ml-es minit igazol; az elemi összkiszerelés ezért 540 ml. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `kakaó` | – | A Monin Brown Cacao közvetlen címkéje szó szerint kakaót nevez meg, a pontos termékforrás pedig kakaóbabból készült likőrt igazol. A `kakaó` önálló, elemi íz, és nem azonos a korábbi általános `csokoládé` értékkel. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `mazsola` | – | A Legendario Elixir de Cuba gyártói termékleírása szerint az érlelt rumkeveréket 40–50 napig mazsolán áztatják, és ez adja a jellegzetes aromát, állagot és ízt. A `mazsola` önálló, elemi és közvetlenül bizonyított ízérték. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `bodza`, `boróka`, `narancsvirág`, `turbolya`, `zsálya` | – | A Zwack hivatalos St. Hubertus portfólióoldala az Erdei változatnál bodzát, szedret, borókát, erdélyi zsályát és zamatos turbolyát, a St. Hubertus 33 változatnál pedig ánizs mellett narancsvirágot nevez meg. Az öt új érték önálló, elemi és közvetlenül gyártói forrással bizonyított ízösszetevő. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | márka | `Di Vasco` | `Vascó` | Az Amaretto közvetlen palackcímkéje, teljes termékneve és pontos termékforrásai egyaránt az ékezet nélküli, két szóból álló `Di Vasco` márkaalakot igazolják. A hibás `Vascó` értéket csak ez az egy rekord használta. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Likőr | íz | `kékáfonya` | – | A Fütyülős teljes termékneve és közvetlen palackcímkéje szó szerint kékáfonya ízt igazol. Az érték önálló és elemi, ezért pontosabb az általános `áfonya` értéknél; utóbbi más likőrökhöz megmaradt. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Egyéb szeszes ital | márka | `Kunság-Szesz`, `márka nélkül` | – | A Kunság Szilva közvetlen címkéje a `Kunság-Szesz` márkaalakot igazolja. A Mini Szilva címkéjén nem szerepel `Mini` márkanév, ezért a biztonságos `márka nélkül` értéket kapta. A régi értékeket más, még felül nem vizsgált rekordok miatt egyelőre megtartottuk. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Egyéb szeszes ital | íz | `brandy`, `chili`, `fahéj`, `kókusz`, `mandula`, `rum`, `szegfűszeg`, `szerecsendió` | – | A konkrét terméknevek, címkék és pontos gyártói termékadatok közvetlenül igazolják ezeket az önálló ízelemeket a brandy- és rumízű termékeknél, valamint a Ballantine's, Stroh, Bacardi, Kraken és Don Papa változatoknál. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Egyéb szeszes ital | íz | `fekete cseresznye`, `kannabisz` | – | A Fütyülős teljes neve és közvetlen címkéje fekete cseresznyét, az Euphoria Cannabis Absinthe neve, címkéje és gyártói termékadata pedig kannabiszt igazol. Mindkettő önálló, elemi és pontosabb a korábbi általános ízértéknél. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Egyéb szeszes ital | íz | `zöld szőlő` | – | A Jinro Green Grape teljes neve és közvetlen címkéje a zöldszőlő-változatot igazolja; a pontos érték önálló és szűkebb a korábbi általános `szőlő` értéknél. |
| Ital → Alkoholos italok és alkoholmentes alternatívák → Egyéb szeszes ital | íz | – | `fekete cseresznye` | Az értéket igazoló egyetlen rekordot a teljes Fütyülős termékcsalád összevetése után kézzel a `Likőr` levélbe soroltuk át, ahol a `fekete cseresznye` már megengedett. Az Egyéb szeszes ital levélben az érték használatlan lett. |

## Termékszintű módosítások

### 001. tételcsalád – Bikavér

- Ellenőrzött rekord: **61**.
- Elérhető és megvizsgált helyi kép: **59**.
- Helyi kép nélkül: **2**.
- Módosított rekord: **37**.
- Módosított tulajdonságcella: **42**.
- Változatlanul helyes rekord: **24**.

#### Bor és boralapú ital → íz: `kávé` → `natúr`

Az alábbi 35 rekord mind Bikavér bor. A név, a forráskategória és az elérhető
termékképek egyike sem igazol kávéízesítést:

`1005711`, `712385:4249775`, `27130:27133`, `679892:4217282`,
`693014:4230404`, `679427:4216817`, `680093:4217483`,
`680090:4217480`, `144862:3682108`, `678317:4215707`, `8116:8119`,
`40972:40975`, `963251:4500641`, `10000107`, `10002301`, `10099678`,
`BTY-X17337900320021`, `BTY-X17365300320021`,
`BTY-X12330900320021`, `4605507`, `19baf5e1dfef560d0c569169`,
`5fd510be028afef75491efbe`, `825e077066f8f5a6cf796a45`,
`e6c3fce9b2d3fc506764d8ed`, `2ee9e7891bdb7247c3c05727`,
`b87881edc115df36ceec2fb5`, `120170721`, `121235788`, `121236891`,
`121236096`, `121234841`, `121237055`, `121288005`, `121310405`,
`121363371`.

#### Bor és boralapú ital → édesség: `egyéb` → `száraz`

A Bikavér száraz vörösbor. Öt rekordnál a hiányos rövid név miatt maradt
`egyéb`, miközben a termékcsalád és a képek alapján a `száraz` érték
bizonyítható:

`679427:4216817`, `144862:3682108`, `10000107`, `10002301`, `10099678`.

#### Bor és boralapú ital → eredet: `egyéb` → `Eger`

- `2807808` – `OSTOROS TRAD.EG.BIKAVÉR.SZ.V.Ü.DRS 0.75L`.
  A rövidítés és az Ostoros Egri Bikavér termékcsalád egyértelműen Egert
  jelöli. Ehhez a rekordhoz nem állt rendelkezésre helyi kép.

#### Pálinka → fajta: `gyümölcspálinka` → `törkölypálinka`

- `121230407` – `Grape-Vine Egri Bikavér törkölypálinka 40% 500 ml`.
  A terméknév kifejezetten törkölypálinkát jelöl; az Egri Bikavér itt a
  felhasznált szőlőtörköly eredetére utal. Ehhez a rekordhoz nem állt
  rendelkezésre helyi kép.

### 002. köteg – Borok és boralapú italok, nem natúr ízek 1–25.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **22**.
- Módosított tulajdonságcella: **48**.
- Változatlanul helyes rekord: **3** (`691157:4228547`,
  `827504:4364894`, `691145:4228535`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `540822` | szénsavasság `szénsavmentes` → `szénsavas`; csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér`; bortípus `boralapú koktél` → `hugo` |
| `677999:4215389` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `683963:4221353` | íz `szőlő` → `natúr`; a „töppedt szőlőből” alapanyag, nem hozzáadott íz |
| `678332:4215722` | íz `szőlő` → `natúr`; a „Balatonszőlősi” eredetmegjelölés, nem íz |
| `827501:4364891` | íz `bodza, lime, trópusi gyümölcs` → `mangó, maracuja`; szénsavasság `szénsavmentes` → `szénsavas`; csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér`; bortípus `boralapú koktél` → `hugo` |
| `712802:4250192` | csomagolás anyaga `egyéb` → `fém`; bortípus `boralapú ital` → `hugo` |
| `712805:4250195` | csomagolás anyaga `egyéb` → `fém` |
| `691163:4228553` | szín `fehér` → `rozé` |
| `712349:4249739` | íz `narancs` → `keserűnarancs`; szín `fehér` → `borostyán` |
| `691151:4228541` | szín `fehér` → `rozé` |
| `690770:4228160` | íz `narancs` → `keserűnarancs`; szín `fehér` → `borostyán`; bortípus `hugo` → `boralapú koktél` |
| `690773:4228163` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `vörös` |
| `691154:4228544` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `vörös` |
| `691148:4228538` | íz `görögdinnye` → `görögdinnye, sárgadinnye`; csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `rozé` |
| `796232:4333622` | szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `796229:4333619` | szín `fehér` → `rozé` |
| `796226:4333616` | szín `egyéb` → `fehér`; bortípus `boralapú koktél` → `hugo` |
| `690764:4228154` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `690776:4228166` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér` |
| `683897:4221287` | íz `bodza` → `alma, bodza`; szénsavasság `szénsavas` → `szénsavmentes`; szín `egyéb` → `borostyán` |
| `683900:4221290` | szín `fehér` → `vörös`; bortípus `bor` → `gyümölcsbor` |
| `683903:4221293` | íz `ribizli` → `fekete ribizli`; szín `fehér` → `vörös` |

### 003. köteg – Borok és boralapú italok, nem natúr ízek 26–50.

- Ellenőrzött új rekord: **25**.
- Elérhető és megvizsgált helyi kép: **23**.
- Helyi kép nélkül: **2**.
- Módosított rekord: **24**.
- Kategóriamozgatás: **4**.
- Módosított kategória- vagy tulajdonságmező: **56**.
- Változatlanul helyes rekord: **1** (`942008:4479398`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `683906:4221296` | szín `fehér` → `vörös` |
| `754428:4291818` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `rozé` |
| `691142:4228532` | íz `alma, meggy, narancs` → `lime, narancs`; csak a képen igazolható gyümölcsök maradtak |
| `685154:4222544` | szín `egyéb` → `vörös` |
| `684473:4221863` | szín `fehér` → `vörös` |
| `684470:4221860` | szín `egyéb` → `vörös` |
| `712826:4250216` | íz `narancs` → `citrom, narancs`; csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `vörös`; bortípus `boralapú ital` → `sangria` |
| `684233:4221623` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `áfonya`; szín `vörös` |
| `684236:4221626` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `eper`; szín `rozé` |
| `674483:4211873` | szín `egyéb` → `vörös` |
| `686681:4224071` | íz `áfonya, szőlő` → `áfonya`; a szőlőlé alapanyag, nem ízesítés; szín `fehér, vörös` → `vörös` |
| `827498:4364888` | szín `fehér` → `kék` |
| `2813338` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `áfonya`; szín `vörös` |
| `2813336` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `eper`; szín `rozé` |
| `2808517` | szín `egyéb` → `vörös`; bortípus `boralapú ital` → `ízesített bor` |
| `2807695` | szín `egyéb` → `vörös`; bortípus `boralapú ital` → `ízesített bor` |
| `10076525` | szín `egyéb` → `rozé` |
| `10076526` | szín `egyéb` → `vörös` |
| `BTY-X17467700320021` | szín `egyéb` → `fehér`; bortípus `boralapú koktél` → `hugo` |
| `BTY-X17210400320021` | szín `egyéb` → `fehér` |
| `BTY-X17339400320021` | íz `szőlő` → `natúr`; a „Balatonszőlősi” eredetmegjelölés, nem íz |
| `BTY-X17552800320021` | íz `szőlő` → `natúr`; a „szőlőből készült” alapanyag-leírás, nem íz |
| `BTY-X17440100320021` | íz `alma, meggy, narancs` → `lime, narancs`; csak a képen igazolható gyümölcsök maradtak |
| `BTY-X17210500320021` | szín `egyéb` → `rozé` |

### 004. köteg – Borok és boralapú italok, nem natúr ízek 51–75.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **25**.
- Kategóriamozgatás: **2**.
- Módosított kategória- vagy tulajdonságmező: **49**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17467900320021` | szín `egyéb` → `rozé`; bortípus `boralapú koktél` → `hugo` |
| `BTY-X18364200320021` | csomagolás anyaga `üveg` → `fém` |
| `BTY-X18364300320021` | csomagolás anyaga `üveg` → `fém` |
| `BTY-X18364600320021` | csomagolás anyaga `üveg` → `fém` |
| `BTY-X17440000320021` | szín `egyéb` → `rozé`; bortípus `boralapú ital` → `boralapú koktél` |
| `BTY-X17456300320021` | szín `egyéb` → `fehér`; bortípus `boralapú koktél` → `hugo` |
| `BTY-X17219100320021` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `áfonya`; szín `vörös` |
| `BTY-X17219200320021` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `eper`; szín `rozé` |
| `BTY-X17304500320021` | szín `fehér` → `borostyán`; bortípus `boralapú koktél` → `hugo` |
| `BTY-X17439700320021` | szín `egyéb` → `fehér` |
| `BTY-X17440300320021` | szín `fehér` → `vörös` |
| `BTY-X17440600320021` | szín `egyéb` → `vörös`; bortípus `boralapú ital` → `boralapú koktél` |
| `BTY-X17456400320021` | szín `egyéb` → `rozé`; bortípus `boralapú koktél` → `hugo` |
| `BTY-X18028400320021` | szénsavasság `szénsavmentes` → `szénsavas`; csomagolás anyaga `üveg` → `fém` |
| `BTY-X18028600320021` | szénsavasság `szénsavmentes` → `szénsavas`; csomagolás anyaga `üveg` → `fém`; szín `egyéb` → `rozé` |
| `BTY-X18144500320021` | íz `narancs` → `keserűnarancs`; szín `fehér` → `borostyán`; bortípus `hugo` → `boralapú koktél` |
| `BTY-X18184500320021` | szín `egyéb` → `fehér` |
| `BTY-X18184800320021` | szín `egyéb` → `rozé` |
| `BTY-X18184900320021` | szín `egyéb` → `fehér` |
| `BTY-X17580800320021` | szín `egyéb` → `vörös` |
| `BTY-X17580700320021` | íz `áfonya, szőlő` → `áfonya`; szín `fehér, vörös` → `vörös` |
| `1001790` | íz `alma, meggy, narancs` → `lime, narancs`; csak a képen igazolható gyümölcsök maradtak |
| `995754` | szín `egyéb` → `fehér` |
| `1000388` | szín `egyéb` → `vörös` |
| `1000389` | szín `egyéb` → `rozé` |

### 005. köteg – Borok és boralapú italok, nem natúr ízek 76–100.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **20**.
- Kategóriamozgatás: **3**.
- Módosított kategória- vagy tulajdonságmező: **47**.
- Változatlanul helyes rekord: **5** (`f3d6c0a3cb1aa83f3381de53`,
  `5d5e836494e804d2cce154b3`, `b119f43e1f42d270f70ace19`,
  `3f799b5ae1cc0b13c8bbc1c2`, `fff6dd1c86f7b903f62b5ebe`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `4603298` | íz `alma, meggy` → `meggy`; szín `egyéb` → `vörös` |
| `4603299` | szín `egyéb` → `rozé` |
| `0e347f2fca390c62e117c325` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `eper`; szín `rozé` |
| `1320a95c07a2451ba8b0ba02` | szín `fehér` → `rozé` |
| `ae39b63a5b793425e1abdb36` | íz `narancs` → `keserűnarancs`; szín `fehér` → `borostyán` |
| `148d02e96266ead39e789921` | íz `áfonya, szőlő` → `áfonya`; szín `fehér, vörös` → `vörös` |
| `cd9454952aee216e2916816f` | íz `alma, meggy, narancs` → `lime, narancs`; csomagolás anyaga `üveg` → `műanyag` |
| `b5808c95b1025510881ff12f` | szín `fehér` → `rozé`; bortípus `ízesített boralapú ital` → `boralapú koktél` |
| `b1308215df1f6d72e589687e` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `eper`; szín `rozé` |
| `08236700e19e620091cb016a` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `áfonya`; szín `vörös` |
| `12d7d639acdff6e35c5690e0` | szín `fehér` → `vörös` |
| `16b5b92cf96e741fd9c34604` | szín `egyéb` → `rozé` |
| `dbe7d8b6bcfe5103936f13fb` | szín `egyéb` → `vörös` |
| `6f777169342931feafc3dfb1` | szín `egyéb` → `rozé` |
| `d7b1901b8f340b49b91a5b75` | szín `fehér` → `rozé` |
| `582a40210c0faeb93dd8f16b` | szín `egyéb` → `vörös` |
| `fe385e2d76dc18cd719b596d` | csomagolás anyaga `üveg` → `fém`; szín `fehér` → `rozé` |
| `b36fc39053996d1eeb7bc50d` | csomagolás anyaga `egyéb` → `fém` |
| `75c2962d2bb33a12efdf400b` | szénsavasság `szénsavmentes` → `szénsavas`; szín `egyéb` → `vörös` |
| `1b8c60de413d3737df9edda6` | íz `narancs` → `keserűnarancs`; szín `fehér` → `borostyán`; bortípus `hugo` → `boralapú koktél` |

### 006. köteg – Borok és boralapú italok, nem natúr ízek 101–125.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **22**.
- Kategóriamozgatás: **2**.
- Módosított kategória- vagy tulajdonságmező: **52**.
- Változatlanul helyes rekord: **3** (`121230966`, `121222855`,
  `121230897`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `f44d4bcf8f91576d530e75c5` | szín `fehér` → `borostyán`; bortípus `boralapú koktél` → `hugo` |
| `9bb7629b8eac1f12659cb059` | szín `fehér` → `rozé`; bortípus `boralapú koktél` → `hugo` |
| `e501d8bd68ec6867fe1d5073` | szín `fehér` → `kék`; bortípus `boralapú koktél` → `hugo` |
| `121257376` | csomagolás anyaga `egyéb` → `fém` |
| `121360777` | csomagolás anyaga `egyéb` → `fém`; bortípus `boralapú ital` → `boralapú koktél` |
| `121230684` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `121260976` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `rozé`; bortípus `boralapú koktél` → `hugo` |
| `121230955` | szín `fehér` → `rozé` |
| `121230868` | szín `fehér` → `rozé`; bortípus `ízesített boralapú ital` → `boralapú koktél` |
| `121222291` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `áfonya`; szín `vörös` |
| `121230649` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `rozé`; bortípus `boralapú ital` → `hugo` |
| `121231308` | íz `szőlő` → `natúr`; a „töppedt szőlőből készült” alapanyag-leírás, nem hozzáadott íz |
| `121260982` | szín `fehér` → `borostyán`; bortípus `boralapú koktél` → `hugo` |
| `121260999` | íz `narancs` → `keserűnarancs`; szín `fehér` → `borostyán`; bortípus `hugo` → `boralapú koktél` |
| `121230747` | íz `alma, meggy, narancs` → `lime, narancs`; csak a képen igazolható gyümölcsök maradtak |
| `121257687` | szín `egyéb` → `vörös` |
| `121266912` | szín `fehér` → `rozé` |
| `121266929` | szín `egyéb` → `vörös` |
| `121222573` | íz `áfonya, szőlő` → `áfonya`; a szőlőlé alapanyag, nem ízesítés; szín `fehér, vörös` → `vörös` |
| `121266935` | szín `egyéb` → `vörös` |
| `121222965` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; fajta `pezsgőkoktél`; íz `eper`; szín `rozé` |
| `121289465` | íz `narancs` → `keserűnarancs`; szín `fehér` → `borostyán` |

### 007. köteg – Borok és boralapú italok, nem natúr ízek 126–140.

- Ellenőrzött rekord: **15**.
- Elérhető és megvizsgált helyi kép: **15**.
- Módosított rekord: **14**.
- Módosított tulajdonságmező: **29**.
- Változatlanul helyes rekord: **1** (`121318610`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121303754` | szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `121303760` | szín `fehér` → `rozé` |
| `121303800` | szín `egyéb` → `borostyán`; bortípus `boralapú koktél` → `hugo` |
| `121306682` | szín `fehér` → `rozé`; bortípus `boralapú koktél` → `hugo` |
| `121306855` | szín `egyéb` → `vörös`; bortípus `boralapú ital` → `ízesített boralapú ital` |
| `121311859` | szín `egyéb` → `borostyán`; bortípus `boralapú koktél` → `hugo` |
| `121311865` | szín `fehér` → `kék`; bortípus `boralapú koktél` → `hugo` |
| `121311911` | szín `egyéb` → `rozé`; bortípus `boralapú ital` → `boralapú koktél` |
| `121315538` | szénsavasság `szénsavmentes` → `szénsavas`; szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `121318633` | szín `egyéb` → `fehér` |
| `121328172` | márka `Lafi` → `La Fiesta`; szín `egyéb` → `vörös`; bortípus `boralapú ital` → `hugo` |
| `121328195` | márka `Lafi` → `La Fiesta`; szín `egyéb` → `rozé`; bortípus `boralapú ital` → `hugo` |
| `121339527` | szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `121363273` | szín `egyéb` → `rozé`; bortípus `boralapú ital` → `hugo` |

### 008. köteg – Borok és boralapú italok, natúr ízek 1–25.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **11**.
- Változatlanul helyes rekord: **20** (`1005710`, `533720`, `885296`,
  `1014272`, `997145`, `940621`, `540869`, `986458`, `997446`, `1005738`,
  `1005739`, `997447`, `997086`, `997173`, `1005712`, `1014273`, `1018156`,
  `979341`, `533721`, `533751`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1018151` | édesség `egyéb` → `száraz` |
| `1018152` | édesség `egyéb` → `száraz` |
| `1018153` | édesség `egyéb` → `száraz` |
| `538682` | szénsavasság `szénsavmentes` → `szénsavas`; csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér`; bortípus `boralapú ital` → `hugo` |
| `891114` | szénsavasság `szénsavmentes` → `szénsavas`; csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `kék`; bortípus `boralapú ital` → `hugo` |

### 009. köteg – Borok és boralapú italok, natúr ízek 26–50.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **23**.
- Helyi kép nélkül: **2** (`4606152`, `4607051`).
- Módosított rekord: **0**.
- Változatlanul helyes rekord: **25** (`533752`, `891128`, `533761`,
  `986389`, `1013066`, `533770`, `4606152`, `989192`, `1017871`, `1058174`,
  `1005743`, `1017873`, `997445`, `1017861`, `533760`, `1054635`, `885288`,
  `1054931`, `926349`, `885295`, `4607051`, `1018159`, `1006648`, `541793`,
  `757818`).

### 010. köteg – Borok és boralapú italok, natúr ízek 51–75.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **23**.
- Helyi kép nélkül: **2** (`4606901`, `4606131`).
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **5**.
- Változatlanul helyes rekord: **21** (`1017872`, `926101`, `1005703`,
  `4598605`, `1028288`, `4606901`, `1018139`, `549599`, `4606131`,
  `4595325`, `954176:4491566`, `712394:4249784`, `712403:4249793`,
  `712793:4250183`, `712799:4250189`, `712397:4249787`,
  `712412:4249802`, `678398:4215788`, `678008:4215398`, `27109:27112`,
  `27091:27094`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `4604731` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `4600057` | csomagolás anyaga `egyéb` → `műanyag` |
| `4600058` | csomagolás anyaga `egyéb` → `műanyag` |
| `4600222` | csomagolás anyaga `egyéb` → `műanyag` |

### 011. köteg – Borok és boralapú italok, natúr ízek 76–100.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **2**.
- Változatlanul helyes rekord: **24** (`712421:4249811`, `28015:28018`,
  `678434:4215824`, `712415:4249805`, `712430:4249820`,
  `712436:4249826`, `712457:4249847`, `712439:4249829`,
  `712424:4249814`, `27100:27103`, `27094:27097`, `27097:27100`,
  `27103:27106`, `27106:27109`, `679229:4216619`, `679232:4216622`,
  `679235:4216625`, `679226:4216616`, `894554:4431944`,
  `679325:4216715`, `795170:4332560`, `679331:4216721`,
  `679334:4216724`, `679328:4216718`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `797567:4334957` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |

### 012. köteg – Borok és boralapú italok, natúr ízek 101–125.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **6**.
- Változatlanul helyes rekord: **19** (`679337:4216727`, `27136:27139`,
  `771258:4308648`, `680108:4217498`, `680081:4217471`,
  `680078:4217468`, `680075:4217465`, `680084:4217474`,
  `680087:4217477`, `826802:4364192`, `683930:4221320`,
  `683936:4221326`, `679436:4216826`, `713276:4250666`,
  `674429:4211819`, `713090:4250480`, `713093:4250483`,
  `679901:4217291`, `693062:4230452`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `795185:4332575` | eredet `Eger` → `Debrő, Eger` |
| `683933:4221323` | eredet `Duna-Tisza köze, Mór` → `Mór` |
| `946277:4483667` | eredet `Duna-Tisza köze, Mór` → `Mór` |
| `826805:4364195` | eredet `Duna-Tisza köze, Mór` → `Mór` |
| `677693:4215083` | szín `egyéb` → `fehér` |
| `46121:46193` | édesség `egyéb` → `száraz` |

### 013. köteg – Borok és boralapú italok, natúr ízek 126–150.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- A forrásnévvel nem egyező helyi kép: **1** (`1007251:4544641`); a
  Szőllősi Királyleányka rekord képe Fodorvin Cserszegi Fűszerest ábrázol,
  ezért a képből nem került át adat.
- Módosított rekord: **0**.
- Változatlanul helyes rekord: **25** (`693065:4230455`, `678416:4215806`,
  `679304:4216694`, `679307:4216697`, `679313:4216703`,
  `771246:4308636`, `679031:4216421`, `679028:4216418`,
  `679034:4216424`, `678413:4215803`, `678419:4215809`,
  `588314:4125704`, `99588:3636792`, `685121:4222511`,
  `684257:4221647`, `426130:3963511`, `679550:4216940`,
  `674435:4211825`, `680132:4217522`, `680135:4217525`,
  `747446:4284836`, `1007251:4544641`, `679439:4216829`,
  `683954:4221344`, `683960:4221350`).

### 014. köteg – Borok és boralapú italok, natúr ízek 151–175.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **2**.
- Módosított tulajdonságmező: **3**.
- Változatlanul helyes rekord: **23** (`769437:4306827`, `691133:4228523`,
  `789806:4327196`, `680129:4217519`, `679397:4216787`,
  `678401:4215791`, `683912:4221302`, `679499:4216889`,
  `684302:4221692`, `678320:4215710`, `946478:4483868`,
  `827339:4364729`, `847922:4385312`, `793076:4330466`,
  `683948:4221338`, `747359:4284749`, `747365:4284755`,
  `827525:4364915`, `771255:4308645`, `678455:4215845`,
  `678458:4215848`, `678464:4215854`, `678461:4215851`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `693005:4230395` | eredet `Szekszárd` → `Pannon, Szekszárd` |
| `679898:4217288` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |

### 015. köteg – Borok és boralapú italok, natúr ízek 176–200.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **12**.
- Változatlanul helyes rekord: **18** (`747371:4284761`, `793961:4331351`,
  `680054:4217444`, `764175:4301565`, `678308:4215698`,
  `678311:4215701`, `683561:4220951`, `660555:4197945`,
  `751959:4289349`, `675110:4212500`, `674417:4211807`,
  `678323:4215713`, `684299:4221689`, `680138:4217528`,
  `680141:4217531`, `827147:4364537`, `685133:4222523`,
  `678341:4215731`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `773100:4310490` | édesség `egyéb` → `édes` |
| `793967:4331357` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `680180:4217570` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `684506:4221896` | eredet `Balaton` → `Badacsony, Balaton` |
| `693212:4230602` | édesség `egyéb` → `száraz` |
| `773115:4310505` | szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `828701:4366091` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |

### 016. köteg – Borok és boralapú italok, natúr ízek 201–225.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **4**.
- Változatlanul helyes rekord: **21** (`683558:4220948`, `680144:4217534`,
  `14734:14737`, `793079:4330469`, `793028:4330418`,
  `747374:4284764`, `793979:4331369`, `784616:4322006`,
  `678335:4215725`, `963521:4500911`,
  `685142:4222532`, `678347:4215737`, `512571:4049961`,
  `394237:3931537`, `463921:4001311`, `796781:4334171`,
  `793052:4330442`, `483482:4020872`, `58692:59031`,
  `122893:3660088`, `37441:37444`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `679559:4216949` | édesség `egyéb` → `száraz` |
| `747377:4284767` | szín `egyéb` → `fehér` |
| `198326:3735566` | csomagolás anyaga `egyéb` → `üveg` |
| `684635:4222025` | eredet `Nagy-Somló`, `Somló` → `Nagy-Somló` |

### 017. köteg – Borok és boralapú italok, natúr ízek 226–250.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **19**.
- Változatlanul helyes rekord: **17** (`824684:4362074`, `68750:3605831`,
  `658866:4196256`, `502070:4039466`, `37444:37447`,
  `685130:4222520`, `101269:3638476`, `775764:4313154`,
  `775761:4313151`, `38266:38269`, `38269:38272`,
  `411334:3948700`, `672962:4210352`, `102738:3639939`,
  `30823:30826`, `547626:4085016`, `21883:21886`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `680177:4217567` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `771252:4308642` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `680183:4217573` | szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `747356:4284746` | szín `egyéb` → `fehér` |
| `680186:4217576` | szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `764427:4301817` | márka `Evinor` → `Babits`; szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `45668:45740` | szín `egyéb` → `fehér` |
| `828704:4366094` | szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |

### 018. köteg – Borok és boralapú italok, natúr ízek 251–275.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **6**.
- Változatlanul helyes rekord: **21** (`28012:28015`, `679316:4216706`,
  `679310:4216700`, `680777:4218167`, `712823:4250213`,
  `712406:4249796`, `713078:4250468`, `712451:4249841`,
  `684275:4221665`, `35500:35503`, `27133:27136`,
  `679244:4216634`, `677432:4214822`, `773382:4310772`,
  `677438:4214828`, `674420:4211810`, `713105:4250495`,
  `826562:4363952`, `692921:4230311`, `679322:4216712`,
  `679529:4216919`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `747350:4284740` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `57195:57534` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `31927:31930` | szénsavasság `szénsavmentes` → `szénsavas` |
| `828689:4366079` | eredet `egyéb` → `Mór` |

### 019. köteg – Borok és boralapú italok, natúr ízek 276–300.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul helyes rekord: **25** (`677435:4214825`, `588311:4125701`,
  `407913:3945264`, `426133:3963514`, `677384:4214774`,
  `458148:3995538`, `411061:3948427`, `769440:4306830`,
  `693020:4230410`, `679523:4216913`, `677417:4214807`,
  `677441:4214831`, `674402:4211792`, `752163:4289553`,
  `677414:4214804`, `683576:4220966`, `684254:4221644`,
  `847928:4385318`, `675122:4212512`, `685139:4222529`,
  `677420:4214810`, `683573:4220963`, `693227:4230617`,
  `677429:4214819`, `677378:4214768`).

### 020. köteg – Borok és boralapú italok, natúr ízek 301–325.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul helyes rekord: **24** (`675098:4212488`, `771186:4308576`,
  `677423:4214813`, `677426:4214816`, `764976:4302366`,
  `685148:4222538`, `512574:4049964`, `783092:4320482`,
  `394240:3931540`, `58689:59028`, `41473:41476`,
  `68753:3605834`, `38272:38275`, `102741:3639942`,
  `30826:30829`, `102750:3639951`, `1038641:4576031`,
  `101263:3638470`, `1000912:4538302`, `1000915:4538305`,
  `954185:4491575`, `988880:4526270`, `712814:4250204`,
  `712391:4249781`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `502073:4039469` | szín `fehér, rozé` → `rozé` |

### 021. köteg – Borok és boralapú italok, natúr ízek 326–350.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul helyes rekord: **24** (`712817:4250207`, `988241:4525631`,
  `712751:4250141`, `712757:4250147`, `712442:4249832`,
  `712427:4249817`, `712448:4249838`, `684272:4221662`,
  `684269:4221659`, `684266:4221656`, `684278:4221668`,
  `684281:4221671`, `27121:27124`, `27124:27127`,
  `27118:27121`, `679238:4216628`, `679367:4216757`,
  `684290:4221680`, `712745:4250135`, `680102:4217492`,
  `679445:4216835`, `679451:4216841`, `679448:4216838`,
  `679442:4216832`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `894575:4431965` | édesség `egyéb` → `édes` |

### 022. köteg – Borok és boralapú italok, natúr ízek 351–375.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **2**.
- Módosított tulajdonságmező: **2**.
- Változatlanul helyes rekord: **23** (`633476:4170866`, `692918:4230308`,
  `678425:4215815`, `132677:3669884`, `678428:4215818`,
  `687776:4225166`, `679895:4217285`, `679457:4216847`,
  `679454:4216844`, `458154:3995544`, `693017:4230407`,
  `693008:4230398`, `679421:4216811`, `712655:4250045`,
  `712658:4250048`, `7870:7873`, `713102:4250492`,
  `674405:4211795`, `674408:4211798`, `756162:4293552`,
  `763455:4300845`, `14071:14074`, `955118:4492508`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `679424:4216814` | szín `fehér` → `vörös` |
| `693215:4230605` | szín `fehér` → `vörös` |

### 023. köteg – Borok és boralapú italok, natúr ízek 376–400.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul helyes rekord: **24** (`680105:4217495`, `680099:4217489`,
  `679430:4216820`, `10441:10444`, `552435:4089825`,
  `847925:4385315`, `675119:4212509`, `762369:4299759`,
  `683570:4220960`, `693011:4230401`, `713777:4251167`,
  `679418:4216808`, `693224:4230614`, `679511:4216901`,
  `794021:4331411`, `675116:4212506`, `678314:4215704`,
  `827081:4364471`, `7801:7804`, `969449:4506839`,
  `990725:4528115`, `675113:4212503`, `754947:4292337`,
  `827702:4365092`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `946304:4483694` | szín `fehér` → `vörös` |

### 024. köteg – Borok és boralapú italok, natúr ízek 401–425.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **5**.
- Változatlanul helyes rekord: **20** (`752160:4289550`, `685145:4222535`,
  `776079:4313469`, `783089:4320479`, `37591:37594`,
  `827705:4365095`, `827708:4365098`, `679409:4216799`,
  `818993:4356383`, `101266:3638473`, `58578:58917`,
  `38275:38278`, `795188:4332578`, `7156:7159`,
  `102744:3639945`, `764973:4302363`, `30829:30832`,
  `678986:4216376`, `975290:4512680`, `102747:3639948`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `797561:4334951` | szín `fehér` → `vörös` |
| `502076:4039472` | szín `fehér, vörös` → `vörös` |
| `679412:4216802` | szín `fehér` → `vörös` |
| `198323:3735563` | csomagolás anyaga `egyéb` → `üveg` |
| `675092:4212482` | szín `fehér` → `vörös` |

### 025. köteg – Borok és boralapú italok, natúr ízek 426–450.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **25**.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **4**.
- Változatlanul helyes rekord: **21** (`34237:34240`, `988199:4525589`,
  `954269:4491659`, `764526:4301916`, `712433:4249823`,
  `12712:12715`, `679517:4216907`, `1010941:4548331`,
  `1000909:4538299`, `366770:3904049`, `759462:4296852`,
  `683894:4221284`, `718607:4255997`, `759027:4296417`,
  `24430:24433`, `988238:4525628`, `828614:4366004`,
  `1000918:4538308`, `988265:4525655`, `23821:23824`,
  `771123:4308513`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `545827:4083217` | szín `fehér` → `vörös` |
| `547007:4084397` | márka `Pillangósvirágú` → `Gazdától az asztalig` |
| `827648:4365038` | szín `fehér` → `vörös` |
| `849527:4386917` | szín `fehér` → `vörös` |

### 026. köteg – Borok és boralapú italok, natúr ízek 451–475.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **18**.
- Helyi kép nélkül ellenőrzött rekord: **7** (`3376042`, `3376038`,
  `3375580`, `3375544`, `3375523`, `3304171`, `3304169`).
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **15**.
- Változatlanul helyes rekord: **15** (`1000885:4538275`,
  `777645:4315035`, `759006:4296396`, `796682:4334072`,
  `683882:4221272`, `683879:4221269`, `24460:24463`,
  `439834:3977218`, `24418:24421`, `65615:3602696`,
  `38053:38056`, `38074:38077`, `3376038`, `3375580`,
  `3304169`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `849524:4386914` | édesség `egyéb` → `félédes` |
| `826811:4364201` | szín `fehér` → `vörös` |
| `849515:4386905` | szín `fehér` → `vörös` |
| `759024:4296414` | szín `fehér` → `vörös` |
| `849530:4386920` | szín `fehér` → `borostyán` |
| `674486:4211876` | csomagolás anyaga `egyéb` → `üveg`; szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; bortípus `boralapú ital` → `ízesített boralapú ital` |
| `3376042` | csomagolás anyaga `üveg` → `egyéb` |
| `3375544` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Kunság` |
| `3375523` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Felső-Magyarország` |
| `3304171` | eredet `egyéb` → `Duna-Tisza köze` |

### 027. köteg – Borok és boralapú italok, natúr ízek 476–500.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **0**.
- Helyi kép nélkül ellenőrzött rekord: **25** (`2817962`, `2817545`,
  `2817128`, `2812867`, `2809889`, `2808655`, `2808654`, `2808653`,
  `2808652`, `2808651`, `2808639`, `2808629`, `2808544`, `2808243`,
  `2807684`, `2807423`, `2807422`, `2807071`, `2756805`, `2755374`,
  `2755057`, `2754501`, `2754366`, `2753426`, `11352`).
- Módosított rekord: **13**.
- Módosított tulajdonságmező: **15**.
- Változatlanul helyes rekord: **12** (`2817545`, `2812867`, `2809889`,
  `2808639`, `2808544`, `2808243`, `2807684`, `2756805`, `2755374`,
  `2754501`, `2753426`, `11352`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `2817962` | édesség `egyéb` → `száraz` |
| `2817128` | édesség `egyéb` → `száraz` |
| `2808655` | csomagolás anyaga `üveg` → `műanyag` |
| `2808654` | csomagolás anyaga `üveg` → `műanyag` |
| `2808653` | eredet `egyéb` → `Duna-Tisza köze` |
| `2808652` | eredet `egyéb` → `Duna-Tisza köze` |
| `2808651` | eredet `egyéb` → `Duna-Tisza köze` |
| `2808629` | eredet `egyéb` → `Eger` |
| `2807423` | eredet `egyéb` → `Eger` |
| `2807422` | eredet `egyéb` → `Eger` |
| `2807071` | szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `2755057` | édesség `egyéb` → `száraz` |
| `2754366` | édesség `egyéb` → `száraz` |

### 028. köteg – Borok és boralapú italok, natúr ízek 501–525.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **0**.
- Helyi kép nélkül ellenőrzött rekord: **25** (`11215`, `11063`,
  `10000046`, `10000047`, `10000048`, `10000049`, `10000050`,
  `10000051`, `10000052`, `10000054`, `10000056`, `10000057`,
  `10000059`, `10000081`, `10000104`, `10000105`, `10000106`,
  `10000110`, `10000111`, `10000112`, `10000208`, `10000209`,
  `10000232`, `10000235`, `10000239`).
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul helyes rekord: **24** (`11063`, `10000046`, `10000047`,
  `10000048`, `10000049`, `10000050`, `10000051`, `10000052`,
  `10000054`, `10000056`, `10000057`, `10000059`, `10000081`,
  `10000104`, `10000105`, `10000106`, `10000110`, `10000111`,
  `10000112`, `10000208`, `10000209`, `10000232`, `10000235`,
  `10000239`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `11215` | édesség `egyéb` → `száraz` |

### 029. köteg – Borok és boralapú italok, natúr ízek 526–550.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált helyi kép: **0**.
- Helyi kép nélkül ellenőrzött rekord: **25** (`10000243`, `10000244`,
  `10000295`, `10000299`, `10000312`, `10000313`, `10000438`,
  `10000439`, `10000440`, `10000485`, `10000495`, `10000496`,
  `10000497`, `10000501`, `10000502`, `10000531`, `10000565`,
  `10000669`, `10002093`, `10002482`, `10003421`, `10005857`,
  `10005906`, `10005907`, `10006064`).
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **15**.
- Változatlanul helyes rekord: **19** (`10000243`, `10000244`,
  `10000312`, `10000313`, `10000438`, `10000439`, `10000440`,
  `10000485`, `10000495`, `10000496`, `10000497`, `10000501`,
  `10000502`, `10000531`, `10002482`, `10003421`, `10005857`,
  `10005906`, `10005907`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `10000295` | eredet `egyéb` → `Villány` |
| `10000299` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `10000565` | szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `10000669` | édesség `egyéb` → `édes`; eredet `egyéb` → `Görögország`; bortípus `bor` → `likőrbor` |
| `10002093` | alkoholtartalom `ismeretlen` → `14,5%`; édesség `egyéb` → `száraz`; eredet `egyéb` → `Villány` |
| `10006064` | alkoholtartalom `ismeretlen` → `14%`; édesség `egyéb` → `száraz`; eredet `egyéb` → `Szekszárd` |

### 030. köteg – Borok és boralapú italok, natúr ízek 551–575.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **0**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **25** (`10006445`,
  `10009073`, `10009074`, `10009077`, `10011282`, `10011299`,
  `10016761`, `10022997`, `10025139`, `10031974`, `10034548`,
  `10050023`, `10056197`, `10064012`, `10067012`, `10074785`,
  `10076174`, `10076520`, `10076522`, `10076523`, `10099671`,
  `10099674`, `10099675`, `10099676`, `10099677`).
- Bizonyítékként külön megvizsgált, azonos termékhez tartozó helyi
  összehasonlító kép: **8** (Bock Cultus rozé, Hilltop Chardonnay, három
  Grand Tokaj 5 puttonyos Aszú-változat, Grand Tokaj Szamorodni, Koch
  Sauvignon Blanc és Sauska Villányi Cuvée).
- Módosított rekord: **24**.
- Módosított tulajdonságmező: **49**.
- Változatlanul helyes rekord: **1** (`10076520`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `10006445` | márka `Tolnai Chardonnay` → `márka nélkül`; édesség `egyéb` → `száraz` |
| `10009073` | alkoholtartalom `ismeretlen` → `10,5%`; édesség `egyéb` → `száraz` |
| `10009074` | alkoholtartalom `ismeretlen` → `12%`; édesség `egyéb` → `száraz`; eredet `egyéb` → `Eger` |
| `10009077` | édesség `egyéb` → `félédes` |
| `10011282` | alkoholtartalom `ismeretlen` → `13%`; édesség `egyéb` → `száraz` |
| `10011299` | alkoholtartalom `ismeretlen` → `19%`; szín `egyéb` → `vörös`; édesség `egyéb` → `édes`; eredet `egyéb` → `Portugália` |
| `10016761` | édesség `egyéb` → `száraz` |
| `10022997` | márka `Primitivo Puglia` → `márka nélkül`; alkoholtartalom `ismeretlen` → `13,5%`; édesség `egyéb` → `száraz` |
| `10025139` | édesség `egyéb` → `száraz` |
| `10031974` | édesség `egyéb` → `száraz` |
| `10034548` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Villány` |
| `10050023` | alkoholtartalom `ismeretlen` → `10,5%`; édesség `egyéb` → `száraz` |
| `10056197` | eredet `egyéb` → `Spanyolország` |
| `10064012` | édesség `egyéb` → `száraz` |
| `10067012` | márka `Badacsonyi Olaszrizling` → `márka nélkül`; alkoholtartalom `ismeretlen` → `11,5%`; édesség `egyéb` → `száraz` |
| `10074785` | alkoholtartalom `ismeretlen` → `14%`; édesség `egyéb` → `száraz` |
| `10076174` | alkoholtartalom `ismeretlen` → `11%`; édesség `egyéb` → `száraz`; eredet `egyéb` → `Hajós-Baja` |
| `10076522` | alkoholtartalom `ismeretlen` → `11,5%`; édesség `egyéb` → `száraz` |
| `10076523` | alkoholtartalom `ismeretlen` → `12%`; édesség `egyéb` → `száraz`; eredet `Veneto` → `Delle Venezie` |
| `10099671` | édesség `egyéb` → `száraz` |
| `10099674` | édesség `egyéb` → `száraz` |
| `10099675` | szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `10099676` | alkoholtartalom `ismeretlen` → `10,5%`; szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `10099677` | édesség `egyéb` → `száraz` |

### 031. köteg – Borok és boralapú italok, natúr ízek 576–600.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `10099679`, `10099680`, `10099681`,
  `10101527`, `10101615`, `10101651`, `10106400`, `10107291`,
  `6404425`, `BTY-X8472500320021`, `BTY-X18068300320021`,
  `BTY-X17187200320021`, `BTY-X17209000320021`,
  `BTY-X17187500320021`, `BTY-X17224600320021`,
  `BTY-X17176300320021`, `BTY-X17211100320021`,
  `BTY-X17447700320021`, `BTY-X17209100320021`,
  `BTY-X17186200320021`, `BTY-X17208900320021`,
  `BTY-X17187700320021`, `BTY-X17358800320021`,
  `BTY-X17187000320021`, `BTY-X17358900320021`.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **22**.
- Változatlanul helyes rekord: **9** (`10101615`,
  `BTY-X18068300320021`, `BTY-X17187200320021`,
  `BTY-X17187500320021`, `BTY-X17186200320021`,
  `BTY-X17187700320021`, `BTY-X17358800320021`,
  `BTY-X17187000320021`, `BTY-X17358900320021`).
- Az évjárattal változó, a konkrét címkén nem olvasható alkoholfokokat
  bizonyíték hiányában `ismeretlen` értéken hagytuk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `10099679` | édesség `egyéb` → `száraz` |
| `10099680` | édesség `egyéb` → `száraz` |
| `10099681` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Ménes` |
| `10101527` | édesség `egyéb` → `száraz`; eredet `Balatonfüred` → `Balatonfüred-Csopak` |
| `10101651` | csomagolás anyaga `üveg` → `műanyag`; édesség `egyéb` → `száraz` |
| `10106400` | márka `Badacsonyi Olaszrizling` → `márka nélkül`; alkoholtartalom `ismeretlen` → `11,5%`; édesség `egyéb` → `száraz` |
| `10107291` | édesség `egyéb` → `száraz` |
| `6404425` | édesség `egyéb` → `száraz` |
| `BTY-X8472500320021` | márka `Le Colline Dei Filari` → `FONTE FRONTINI`; csomagolás anyaga `egyéb` → `papír` |
| `BTY-X17209000320021` | eredet `egyéb` → `Mór` |
| `BTY-X17224600320021` | eredet `egyéb` → `Mór` |
| `BTY-X17176300320021` | márka `Hilltop` → `KAMOCSAY` |
| `BTY-X17211100320021` | eredet `egyéb` → `Mór` |
| `BTY-X17447700320021` | eredet `egyéb` → `Pécs` |
| `BTY-X17209100320021` | eredet `egyéb` → `Mór` |
| `BTY-X17208900320021` | eredet `egyéb` → `Mór` |

### 032. köteg – Borok és boralapú italok, natúr ízek 601–625.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17188000320021`,
  `BTY-X17188300320021`, `BTY-X17188400320021`,
  `BTY-X17222900320021`, `BTY-X17275800320021`,
  `BTY-X17928000320021`, `BTY-X17940200320021`,
  `BTY-X18003600320021`, `BTY-X18322900320021`,
  `BTY-X17751900320021`, `BTY-X17751700320021`,
  `BTY-X10762300320021`, `BTY-X17375100320021`,
  `BTY-X17375800320021`, `BTY-X17493300320021`,
  `BTY-X17494500320021`, `BTY-X17495600320021`,
  `BTY-X17534400320021`, `BTY-X17534900320021`,
  `BTY-X17920600320021`, `BTY-X18076700320021`,
  `BTY-X18130800320021`, `BTY-X18131000320021`,
  `BTY-X18283800320021`, `BTY-X17458300320021`.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **16**.
- Változatlanul helyes rekord: **13** (`BTY-X17275800320021`,
  `BTY-X17940200320021`, `BTY-X18322900320021`,
  `BTY-X17751900320021`, `BTY-X17751700320021`,
  `BTY-X17375100320021`, `BTY-X17375800320021`,
  `BTY-X17493300320021`, `BTY-X17494500320021`,
  `BTY-X17495600320021`, `BTY-X17534400320021`,
  `BTY-X17920600320021`, `BTY-X17458300320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17188000320021` | márka `Hilltop` → `KAMOCSAY` |
| `BTY-X17188300320021` | márka `Hilltop` → `KAMOCSAY` |
| `BTY-X17188400320021` | márka `Hilltop` → `KAMOCSAY` |
| `BTY-X17222900320021` | eredet `egyéb` → `Mór` |
| `BTY-X17928000320021` | eredet `egyéb` → `Kunság` |
| `BTY-X18003600320021` | eredet `egyéb` → `Pécs` |
| `BTY-X10762300320021` | eredet `Veneto` → `Delle Venezie` |
| `BTY-X17534900320021` | eredet `egyéb` → `Ausztrália` |
| `BTY-X18076700320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X18130800320021` | márka `Green Cape` → `Cape Bridge`; alkoholtartalom `ismeretlen` → `12,5%`; eredet `Új-Zéland` → `Dél-Afrika` |
| `BTY-X18131000320021` | márka `Font` → `FONTBREUIL` |
| `BTY-X18283800320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |

### 033. köteg – Borok és boralapú italok, natúr ízek 626–650.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17458800320021`,
  `BTY-X78333500320022`, `BTY-X6692800320021`,
  `BTY-X17434300320021`, `BTY-X87566500320022`,
  `BTY-X17961200320021`, `BTY-X17522000320021`,
  `BTY-X17434100320021`, `BTY-X2776300320021`,
  `BTY-X2776100320021`, `BTY-X17515300320021`,
  `BTY-X17522200320021`, `BTY-X17392300320021`,
  `BTY-X17910500320021`, `BTY-X17475000320021`,
  `BTY-X17332500320021`, `BTY-X18287100320021`,
  `BTY-X17212700320021`, `BTY-X5983900320021`,
  `BTY-X18007400320021`, `BTY-X17912700320021`,
  `BTY-X87046400320022`, `BTY-X17863000320021`,
  `BTY-X17583400320021`, `BTY-X18002800320021`.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **17** (`BTY-X17458800320021`,
  `BTY-X78333500320022`, `BTY-X6692800320021`,
  `BTY-X17434300320021`, `BTY-X87566500320022`,
  `BTY-X17522000320021`, `BTY-X17434100320021`,
  `BTY-X2776300320021`, `BTY-X2776100320021`,
  `BTY-X17515300320021`, `BTY-X17522200320021`,
  `BTY-X17910500320021`, `BTY-X17475000320021`,
  `BTY-X17212700320021`, `BTY-X87046400320022`,
  `BTY-X17863000320021`, `BTY-X17583400320021`).
- Az évjáratonként eltérő, a konkrét rekord nevében vagy címkéjén nem szereplő
  alkoholfokokat nem módosítottuk külső évjárat adata alapján.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17961200320021` | eredet `egyéb` → `Felső-Magyarország` |
| `BTY-X17392300320021` | eredet `egyéb` → `Villány` |
| `BTY-X17332500320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X18287100320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X5983900320021` | csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X18007400320021` | eredet `egyéb` → `Mátra` |
| `BTY-X17912700320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X18002800320021` | eredet `egyéb` → `Mátra` |

### 034. köteg – Borok és boralapú italok, natúr ízek 651–675.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17673900320021`,
  `BTY-X17890100320021`, `BTY-X17940500320021`,
  `BTY-X17365900320021`, `BTY-X17772700320021`,
  `BTY-X17259600320021`, `BTY-X18007200320021`,
  `BTY-X17403500320021`, `BTY-X17332600320021`,
  `BTY-X6756100320021`, `BTY-X17521200320021`,
  `BTY-X17338000320021`, `BTY-X17475100320021`,
  `BTY-X11275800320021`, `BTY-X17212800320021`,
  `BTY-X17332300320021`, `BTY-X17921800320021`,
  `BTY-X17367800320021`, `BTY-X17921700320021`,
  `BTY-X5215100320021`, `BTY-X4452400320021`,
  `BTY-X17463800320021`, `BTY-X17459000320021`,
  `BTY-X17364800320021`, `BTY-X17201300320021`.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **13**.
- Változatlanul helyes rekord: **17** (`BTY-X17673900320021`,
  `BTY-X17940500320021`, `BTY-X17365900320021`,
  `BTY-X17259600320021`, `BTY-X17403500320021`,
  `BTY-X6756100320021`, `BTY-X17521200320021`,
  `BTY-X17338000320021`, `BTY-X17475100320021`,
  `BTY-X17212800320021`, `BTY-X17921800320021`,
  `BTY-X17921700320021`, `BTY-X5215100320021`,
  `BTY-X4452400320021`, `BTY-X17463800320021`,
  `BTY-X17364800320021`, `BTY-X17201300320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17890100320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X17772700320021` | eredet `Új-Zéland` → `Marlborough`, `Új-Zéland` |
| `BTY-X18007200320021` | eredet `egyéb` → `Mátra` |
| `BTY-X17332600320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X11275800320021` | eredet `Dunántúl` → `Felső-Magyarország` |
| `BTY-X17332300320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X17367800320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X17459000320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |

### 035. köteg – Borok és boralapú italok, natúr ízek 676–700.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X13626800320021`,
  `BTY-X17515500320021`, `BTY-X17228200320021`,
  `BTY-X17365000320021`, `BTY-X12219500320021`,
  `BTY-X17331800320021`, `BTY-X17363200320021`,
  `BTY-X17363200320022`, `BTY-X9393600320021`,
  `BTY-X17363000320021`, `BTY-X17363000320022`,
  `BTY-X6503300320021`, `BTY-X17272400320021`,
  `BTY-X17392800320021`, `BTY-X17364700320021`,
  `BTY-X16698200320021`, `BTY-X17332100320021`,
  `BTY-X17276300320021`, `BTY-X10023000320021`,
  `BTY-X12022200320021`, `BTY-X12538600320021`,
  `BTY-X12648800320021`, `BTY-X1287800320021`,
  `BTY-X1287800320022`, `BTY-X12957600320021`.
- A `BTY-X12219500320021` helyi képe a név szerinti Mátra-Bacchus
  Olaszrizling helyett Merlot-dobozt mutat. A téves képből nem vezettünk le
  tulajdonságmódosítást; a rekordot a terméknév és a teljes forrásadat alapján
  ellenőriztük.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **17** (`BTY-X17515500320021`,
  `BTY-X17228200320021`, `BTY-X17365000320021`,
  `BTY-X12219500320021`, `BTY-X17331800320021`,
  `BTY-X17363200320021`, `BTY-X9393600320021`,
  `BTY-X17392800320021`, `BTY-X17364700320021`,
  `BTY-X16698200320021`, `BTY-X17332100320021`,
  `BTY-X12022200320021`, `BTY-X12538600320021`,
  `BTY-X12648800320021`, `BTY-X1287800320021`,
  `BTY-X1287800320022`, `BTY-X12957600320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X13626800320021` | csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X17363200320022` | kiszerelés `2000 ml` → `12000 ml` |
| `BTY-X17363000320021` | alkoholtartalom `ismeretlen` → `11%` |
| `BTY-X17363000320022` | alkoholtartalom `ismeretlen` → `11%` |
| `BTY-X6503300320021` | csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X17272400320021` | eredet `Pannonhalma` → `Pannon` |
| `BTY-X17276300320021` | eredet `Dunántúl` → `Balatonfüred-Csopak` |
| `BTY-X10023000320021` | alkoholtartalom `ismeretlen` → `10%`; eredet `Dunántúl` → `Badacsony` |

### 036. köteg – Borok és boralapú italok, natúr ízek 701–725.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **24**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **1**
  (`BTY-X15688300320021`).
- Képpel ellenőrzött rekordok: `BTY-X13251500320021`,
  `BTY-X13750900320021`, `BTY-X14709200320021`,
  `BTY-X14861300320021`, `BTY-X14934600320021`,
  `BTY-X14934800320021`, `BTY-X15608800320021`,
  `BTY-X15778100320021`, `BTY-X15779100320021`,
  `BTY-X16026400320021`, `BTY-X16026400320022`,
  `BTY-X17079800320021`, `BTY-X17212400320021`,
  `BTY-X17212500320021`, `BTY-X17212600320021`,
  `BTY-X17225000320021`, `BTY-X17252800320021`,
  `BTY-X17253000320021`, `BTY-X17257900320021`,
  `BTY-X17258000320021`, `BTY-X17259400320021`,
  `BTY-X17259500320021`, `BTY-X17268400320021`,
  `BTY-X17275200320021`.
- Módosított rekord: **3**.
- Módosított tulajdonságmező: **3**.
- Változatlanul helyes rekord: **22** (`BTY-X13251500320021`,
  `BTY-X13750900320021`, `BTY-X14709200320021`,
  `BTY-X14934600320021`, `BTY-X14934800320021`,
  `BTY-X15608800320021`, `BTY-X15688300320021`,
  `BTY-X15778100320021`, `BTY-X15779100320021`,
  `BTY-X16026400320021`, `BTY-X16026400320022`,
  `BTY-X17212400320021`, `BTY-X17212500320021`,
  `BTY-X17212600320021`, `BTY-X17252800320021`,
  `BTY-X17253000320021`, `BTY-X17257900320021`,
  `BTY-X17258000320021`, `BTY-X17259400320021`,
  `BTY-X17259500320021`, `BTY-X17268400320021`,
  `BTY-X17275200320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X14861300320021` | csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X17079800320021` | alkoholtartalom `ismeretlen` → `14,5%` |
| `BTY-X17225000320021` | eredet `egyéb` → `Mór` |

### 037. köteg – Borok és boralapú italok, natúr ízek 726–750.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **24**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **1**
  (`BTY-X17339600320021`).
- Képpel ellenőrzött rekordok: `BTY-X17276200320021`,
  `BTY-X17276600320021`, `BTY-X17276900320021`,
  `BTY-X17290100320021`, `BTY-X17290200320021`,
  `BTY-X17293900320021`, `BTY-X17294100320021`,
  `BTY-X17296900320021`, `BTY-X17303100320021`,
  `BTY-X17329800320021`, `BTY-X17333100320021`,
  `BTY-X17338900320021`, `BTY-X17339100320021`,
  `BTY-X17339300320021`, `BTY-X17339500320021`,
  `BTY-X17353800320021`, `BTY-X17354200320021`,
  `BTY-X17359100320021`, `BTY-X17359400320021`,
  `BTY-X17359600320021`, `BTY-X17359800320021`,
  `BTY-X17359900320021`, `BTY-X17360100320021`,
  `BTY-X17360300320021`.
- A `BTY-X17329800320021` Mészáros Chardonnay alkoholtartalmát nem
  pontosítottuk: a különböző évjáratokra talált termékadatok eltérnek, a helyi
  rekord pedig nem azonosít évjáratot.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **7**.
- Változatlanul helyes rekord: **19** (`BTY-X17276200320021`,
  `BTY-X17276600320021`, `BTY-X17276900320021`,
  `BTY-X17290100320021`, `BTY-X17290200320021`,
  `BTY-X17293900320021`, `BTY-X17294100320021`,
  `BTY-X17329800320021`, `BTY-X17333100320021`,
  `BTY-X17338900320021`, `BTY-X17339600320021`,
  `BTY-X17353800320021`, `BTY-X17354200320021`,
  `BTY-X17359100320021`, `BTY-X17359400320021`,
  `BTY-X17359600320021`, `BTY-X17359800320021`,
  `BTY-X17359900320021`, `BTY-X17360100320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17296900320021` | édesség `száraz` → `édes` |
| `BTY-X17303100320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X17339100320021` | eredet `Balatonfüred` → `Balatonfüred-Csopak` |
| `BTY-X17339300320021` | eredet `Balatonfüred` → `Balatonfüred-Csopak` |
| `BTY-X17339500320021` | eredet `Balatonfüred` → `Balatonfüred-Csopak` |
| `BTY-X17360300320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |

### 038. köteg – Borok és boralapú italok, natúr ízek 751–775.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17360800320021`,
  `BTY-X17360900320021`, `BTY-X17363800320021`,
  `BTY-X17364300320021`, `BTY-X17364500320021`,
  `BTY-X17365800320021`, `BTY-X17367900320021`,
  `BTY-X17368000320021`, `BTY-X17368600320021`,
  `BTY-X17368700320021`, `BTY-X17372100320021`,
  `BTY-X17392100320021`, `BTY-X17392500320021`,
  `BTY-X17403800320021`, `BTY-X17405300320021`,
  `BTY-X17434400320021`, `BTY-X17434500320021`,
  `BTY-X17447800320021`, `BTY-X17457900320021`,
  `BTY-X17458200320021`, `BTY-X17458900320021`,
  `BTY-X17459200320021`, `BTY-X17459500320021`,
  `BTY-X17475200320021`, `BTY-X17475300320021`.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **8**.
- Változatlanul helyes rekord: **19** (`BTY-X17360800320021`,
  `BTY-X17364300320021`, `BTY-X17364500320021`,
  `BTY-X17365800320021`, `BTY-X17368700320021`,
  `BTY-X17372100320021`, `BTY-X17392100320021`,
  `BTY-X17392500320021`, `BTY-X17405300320021`,
  `BTY-X17434400320021`, `BTY-X17434500320021`,
  `BTY-X17447800320021`, `BTY-X17457900320021`,
  `BTY-X17458200320021`, `BTY-X17458900320021`,
  `BTY-X17459200320021`, `BTY-X17459500320021`,
  `BTY-X17475200320021`, `BTY-X17475300320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17360900320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X17363800320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X17367900320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X17368000320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X17368600320021` | eredet `Szekszárd` → `Pannon`, `Szekszárd` |
| `BTY-X17403800320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |

### 039. köteg – Borok és boralapú italok, natúr ízek 776–800.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **23**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **2**
  (`BTY-X17515600320021`, `BTY-X17552600320021`).
- Képpel ellenőrzött rekordok: `BTY-X17475600320021`,
  `BTY-X17494000320021`, `BTY-X17496300320021`,
  `BTY-X17500600320021`, `BTY-X17500800320021`,
  `BTY-X17501000320021`, `BTY-X17501100320021`,
  `BTY-X17509500320021`, `BTY-X17510800320021`,
  `BTY-X17510900320021`, `BTY-X17511000320021`,
  `BTY-X17521300320021`, `BTY-X17521500320021`,
  `BTY-X17533900320021`, `BTY-X17552100320021`,
  `BTY-X17552200320021`, `BTY-X17552300320021`,
  `BTY-X17552700320021`, `BTY-X17573900320021`,
  `BTY-X17574000320021`, `BTY-X17583200320021`,
  `BTY-X17583800320021`, `BTY-X17583900320021`.
- A `BTY-X17509500320021` Jásdi Csopaki Rizling alkoholtartalmát nem
  pontosítottuk: az évjárat nélküli rekordhoz talált évjáratos források 12%,
  12,5% és 13% értéket is közölnek.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **5**.
- Változatlanul helyes rekord: **20** (`BTY-X17475600320021`,
  `BTY-X17494000320021`, `BTY-X17501100320021`,
  `BTY-X17509500320021`, `BTY-X17510800320021`,
  `BTY-X17510900320021`, `BTY-X17511000320021`,
  `BTY-X17515600320021`, `BTY-X17521300320021`,
  `BTY-X17521500320021`, `BTY-X17552100320021`,
  `BTY-X17552200320021`, `BTY-X17552300320021`,
  `BTY-X17552600320021`, `BTY-X17552700320021`,
  `BTY-X17573900320021`, `BTY-X17574000320021`,
  `BTY-X17583200320021`, `BTY-X17583800320021`,
  `BTY-X17583900320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17496300320021` | márka `márka nélkül` → `Domaine de la Chézatte` |
| `BTY-X17500600320021` | eredet `Nagy-Somló`, `Somló` → `Nagy-Somló` |
| `BTY-X17500800320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X17501000320021` | eredet `Villány` → `Tokaj` |
| `BTY-X17533900320021` | eredet `Új-Zéland` → `Marlborough`, `Új-Zéland` |

### 040. köteg – Borok és boralapú italok, natúr ízek 801–825.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **22**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **3**
  (`BTY-X17943600320021`, `BTY-X17943700320021`,
  `BTY-X18036600320021`).
- Képpel ellenőrzött rekordok: `BTY-X17723600320021`,
  `BTY-X17724100320021`, `BTY-X17724200320021`,
  `BTY-X17755800320021`, `BTY-X17862200320021`,
  `BTY-X17880900320021`, `BTY-X17890000320021`,
  `BTY-X17994800320021`, `BTY-X17995100320021`,
  `BTY-X18002500320021`, `BTY-X18003700320021`,
  `BTY-X18003800320021`, `BTY-X18007000320021`,
  `BTY-X18007100320021`, `BTY-X18007300320021`,
  `BTY-X18010400320021`, `BTY-X18012100320021`,
  `BTY-X18012300320021`, `BTY-X18032900320021`,
  `BTY-X18037000320021`, `BTY-X18072400320021`,
  `BTY-X18075900320021`.
- A `BTY-X17862200320021` Gedeon Zöld Veltelini és a
  `BTY-X17994800320021` Varga Muskotály eredetét nem pontosítottuk: az
  évjárat nélküli rekordokhoz talált, eltérő évjáratú vagy termékváltozatú
  források egymásnak ellentmondó borvidéket közölnek.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **8**.
- Változatlanul helyes rekord: **17** (`BTY-X17724200320021`,
  `BTY-X17755800320021`, `BTY-X17862200320021`,
  `BTY-X17880900320021`, `BTY-X17890000320021`,
  `BTY-X17943700320021`, `BTY-X17994800320021`,
  `BTY-X17995100320021`, `BTY-X18003700320021`,
  `BTY-X18003800320021`, `BTY-X18007000320021`,
  `BTY-X18007100320021`, `BTY-X18012100320021`,
  `BTY-X18012300320021`, `BTY-X18032900320021`,
  `BTY-X18072400320021`, `BTY-X18075900320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17723600320021` | eredet `Új-Zéland` → `Marlborough`, `Új-Zéland` |
| `BTY-X17724100320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X17943600320021` | eredet `Tokaj` → `Nagy-Somló` |
| `BTY-X18002500320021` | eredet `egyéb` → `Mátra` |
| `BTY-X18007300320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X18010400320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X18036600320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X18037000320021` | eredet `Somló` → `Nagy-Somló` |

### 041. köteg – Borok és boralapú italok, natúr ízek 826–850.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **22**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **3**
  (`BTY-X18117000320021`, `BTY-X18697300320021`,
  `BTY-X18697400320021`).
- Képpel ellenőrzött rekordok: `BTY-X18116800320021`,
  `BTY-X18159800320021`, `BTY-X18165500320021`,
  `BTY-X18212500320021`, `BTY-X18216200320021`,
  `BTY-X18216200320022`, `BTY-X18216300320021`,
  `BTY-X18216300320022`, `BTY-X18286700320021`,
  `BTY-X18287000320021`, `BTY-X18287600320021`,
  `BTY-X18287700320021`, `BTY-X18287800320021`,
  `BTY-X18288100320021`, `BTY-X18288300320021`,
  `BTY-X18288400320021`, `BTY-X18468700320021`,
  `BTY-X18531700320021`, `BTY-X18673300320021`,
  `BTY-X18697400320022`, `BTY-X18697800320021`,
  `BTY-X18697800320022`.
- A régebbi, a közvetlen képen csak magyar borként jelölt La Fiesta tételek,
  valamint az eltérő alkoholtartalmú vagy termékvonalú BB-változatok eredetét
  nem pontosítottuk, ha a talált források nem azonosították egyértelműen
  ugyanazt a termékváltozatot.
- Módosított rekord: **14**.
- Módosított tulajdonságmező: **17**.
- Változatlanul helyes rekord: **11** (`BTY-X18165500320021`,
  `BTY-X18216300320021`, `BTY-X18216300320022`,
  `BTY-X18287800320021`, `BTY-X18288100320021`,
  `BTY-X18468700320021`, `BTY-X18697300320021`,
  `BTY-X18697400320021`, `BTY-X18697400320022`,
  `BTY-X18697800320021`, `BTY-X18697800320022`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18116800320021` | eredet `Balaton` → `Balaton`, `Balatonfüred-Csopak` |
| `BTY-X18117000320021` | eredet `Balaton` → `Balaton`, `Balatonfüred` |
| `BTY-X18159800320021` | szín `egyéb` → `borostyán`; eredet `egyéb` → `Tokaj` |
| `BTY-X18212500320021` | puttonyszám `nem alkalmazható` → `5 puttonyos`; szín `egyéb` → `borostyán`; eredet `egyéb` → `Tokaj` |
| `BTY-X18216200320021` | eredet `egyéb` → `Duna-Tisza köze` |
| `BTY-X18216200320022` | eredet `egyéb` → `Duna-Tisza köze` |
| `BTY-X18286700320021` | alkoholtartalom `ismeretlen` → `12%` |
| `BTY-X18287000320021` | eredet `egyéb` → `Dunántúl` |
| `BTY-X18287600320021` | eredet `egyéb` → `Dunántúl` |
| `BTY-X18287700320021` | eredet `egyéb` → `Balaton`, `Balatonboglár` |
| `BTY-X18288300320021` | eredet `egyéb` → `Balaton`, `Balatonboglár` |
| `BTY-X18288400320021` | eredet `egyéb` → `Balaton`, `Balatonboglár` |
| `BTY-X18531700320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X18673300320021` | eredet `egyéb` → `Zala` |

### 042. köteg – Borok és boralapú italok, natúr ízek 851–875.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X18698000320021`,
  `BTY-X18710400320021`, `BTY-X18710500320021`,
  `BTY-X18799100320021`, `BTY-X18880100320021`,
  `BTY-X18887200320021`, `BTY-X18965500320021`,
  `BTY-X18966700320021`, `BTY-X18966800320021`,
  `BTY-X19628000320022`, `BTY-X2383700320021`,
  `BTY-X2383700320022`, `BTY-X8005500320021`,
  `BTY-X8007900320021`, `BTY-X85794800320022`,
  `BTY-X9400700320021`, `BTY-X9800200320021`,
  `BTY-X15688200320021`, `BTY-X14090400320021`,
  `BTY-X15226500320021`, `BTY-X15685100320021`,
  `BTY-X15983000320021`, `BTY-X1682400320021`,
  `BTY-X17175300320021`, `BTY-X17213500320021`.
- A `BTY-X85794800320022` Varga Jégbor és a
  `BTY-X9800200320021` Varga Aranymetszés Olaszrizling alkoholtartalmát nem
  pontosítottuk: az elérhető források eltérő évjáratokhoz eltérő értékeket
  közölnek.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **11**.
- Változatlanul helyes rekord: **17** (`BTY-X18710400320021`,
  `BTY-X18710500320021`, `BTY-X18880100320021`,
  `BTY-X18887200320021`, `BTY-X18965500320021`,
  `BTY-X18966700320021`, `BTY-X18966800320021`,
  `BTY-X19628000320022`, `BTY-X2383700320021`,
  `BTY-X2383700320022`, `BTY-X8005500320021`,
  `BTY-X8007900320021`, `BTY-X14090400320021`,
  `BTY-X15226500320021`, `BTY-X1682400320021`,
  `BTY-X17175300320021`, `BTY-X17213500320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18698000320021` | eredet `Villány` → `Tokaj` |
| `BTY-X18799100320021` | eredet `egyéb` → `Mór`; a közvetlen kép a névben szereplő általános „fehér cuvée” helyett Paulus Gold Olaszrizling palackot mutat |
| `BTY-X85794800320022` | eredet `egyéb` → `Felső-Magyarország` |
| `BTY-X9400700320021` | alkoholtartalom `ismeretlen` → `10,5%`; csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X9800200320021` | eredet `Balaton` → `Badacsony`, `Balaton` |
| `BTY-X15688200320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X15685100320021` | eredet `egyéb` → `Zala` |
| `BTY-X15983000320021` | alkoholtartalom `ismeretlen` → `11%`; szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |

### 043. köteg – Borok és boralapú italok, natúr ízek 876–900.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **12**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **13**.
- Képpel ellenőrzött rekordok: `BTY-X17272600320021`,
  `BTY-X17293800320021`, `BTY-X17294000320021`,
  `BTY-X17331700320021`, `BTY-X17403900320021`,
  `BTY-X17456800320021`, `BTY-X17896400320021`,
  `BTY-X17896700320021`, `BTY-X18067200320021`,
  `BTY-X18362700320021`, `BTY-X18989800320021`,
  `BTY-X10762200320021`.
- Közvetlen helyi kép nélkül ellenőrzött rekordok:
  `BTY-X17332200320021`, `BTY-X17551900320021`,
  `BTY-X17552000320021`, `BTY-X17553100320021`,
  `BTY-X17574300320021`, `BTY-X17723100320021`,
  `BTY-X17918300320021`, `BTY-X17943900320021`,
  `BTY-X17944000320021`, `BTY-X17944100320021`,
  `BTY-X18037300320021`, `BTY-X18049100320021`,
  `BTY-X18106800320021`.
- A `BTY-X17551900320021` általános nevű, kép nélküli Varga Jégbor
  eredetét és alkoholtartalmát nem pontosítottuk, mert nem azonosítható
  biztonsággal a források eltérő évjáratú termékeivel.
- A Grand Tokaj édes Szamorodni fehér színét és tokaji eredetét a pontos
  0,25 literes termékadat és a termelő hivatalos leírása igazolja.
- A Garamvári Prémium Sauvignon Blanc balatoni-balatonboglári, a Matua
  Lands & Legends Sauvignon Blanc marlborough-i és új-zélandi, a Bujdosó
  Olaszrizling Válogatás balatoni-balatonboglári eredetét közvetlen
  termelői vagy pontos termékforrás igazolja.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **12**.
- Változatlanul helyes rekord: **14** (`BTY-X17272600320021`,
  `BTY-X17293800320021`, `BTY-X17294000320021`,
  `BTY-X17331700320021`, `BTY-X17456800320021`,
  `BTY-X17551900320021`, `BTY-X17552000320021`,
  `BTY-X17553100320021`, `BTY-X17574300320021`,
  `BTY-X17918300320021`, `BTY-X18037300320021`,
  `BTY-X18067200320021`, `BTY-X18362700320021`,
  `BTY-X18989800320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17332200320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `BTY-X17403900320021` | eredet `egyéb` → `Balaton`, `Balatonboglár` |
| `BTY-X17723100320021` | eredet `Új-Zéland` → `Marlborough`, `Új-Zéland` |
| `BTY-X17896400320021` | csomagolás anyaga `egyéb` → `fém` |
| `BTY-X17896700320021` | csomagolás anyaga `egyéb` → `fém` |
| `BTY-X17943900320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X17944000320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X17944100320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X18049100320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X18106800320021` | eredet `Somló` → `Nagy-Somló` |
| `BTY-X10762200320021` | csomagolás anyaga `egyéb` → `papír` |

### 044. köteg – Borok és boralapú italok, natúr ízek 901–925.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17375600320021`,
  `BTY-X8472300320021`, `BTY-X17187300320021`,
  `BTY-X17498500320021`, `BTY-X17496100320021`,
  `BTY-X17501500320021`, `BTY-X13901100320021`,
  `BTY-X13813600320021`, `BTY-X17375200320021`,
  `BTY-X17376000320021`, `BTY-X17376400320021`,
  `BTY-X17494600320021`, `BTY-X17495900320021`,
  `BTY-X17496000320021`, `BTY-X17534100320021`,
  `BTY-X17534200320021`, `BTY-X17534500320021`,
  `BTY-X17867800320021`, `BTY-X18119300320021`,
  `BTY-X18125700320021`, `BTY-X18130900320021`,
  `BTY-X78334200320022`, `BTY-X3718200320021`,
  `BTY-X17374900320021`, `BTY-X14659500320021`.
- A `BTY-X18130900320021` rekordhoz kötött helyi kép Green Cape Chenin
  Blanc palackot mutat, tehát nem egyezik a Los Pagos Cabernet Sauvignon
  névvel és teljes forrásadattal. A besorolást nem a hibás képkapcsolat
  szerint írtuk át; több pontos Los Pagos termékforrás alapján csak a hibás
  spanyol eredetet javítottuk chilere.
- A Hüttenglut Glühwein alkoholtartalmát nem pontosítottuk, mert az azonos
  nevű 1 literes források 8,6% és 8,8% értéket is közölnek. Az édes jelleget
  a pontos termékleírásokban szereplő cukrozás igazolja.
- A `BTY-X18125700320021` Sóvárgó régi, 14,5%-os változatának eredetét nem
  pontosítottuk: a jelenlegi, 12%-os termékváltozat nem azonos ezzel a
  rekorddal, a talált borvidékadatok pedig egymásnak ellentmondanak.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **17** (`BTY-X17375600320021`,
  `BTY-X17187300320021`, `BTY-X17496100320021`,
  `BTY-X13813600320021`, `BTY-X17375200320021`,
  `BTY-X17376000320021`, `BTY-X17376400320021`,
  `BTY-X17494600320021`, `BTY-X17495900320021`,
  `BTY-X17496000320021`, `BTY-X17534100320021`,
  `BTY-X17534200320021`, `BTY-X18119300320021`,
  `BTY-X18125700320021`, `BTY-X78334200320022`,
  `BTY-X3718200320021`, `BTY-X17374900320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X8472300320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X17498500320021` | eredet `Argentína` → `Argentína`, `Mendoza` |
| `BTY-X17501500320021` | édesség `egyéb` → `édes` |
| `BTY-X13901100320021` | csomagolás anyaga `egyéb` → `papír`; eredet `Spanyolország` → `Chile` |
| `BTY-X17534500320021` | eredet `Spanyolország` → `Castilla`, `Spanyolország` |
| `BTY-X17867800320021` | eredet `egyéb` → `Franciaország`, `Pays d'Oc` |
| `BTY-X18130900320021` | eredet `Spanyolország` → `Chile` |
| `BTY-X14659500320021` | csomagolás anyaga `egyéb` → `műanyag` |

### 045. köteg – Borok és boralapú italok, natúr ízek 926–950.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17959400320021`,
  `BTY-X17365400320021`, `BTY-X12978400320021`,
  `BTY-X17330200320021`, `BTY-X18005800320021`,
  `BTY-X17763800320021`, `BTY-X17393200320021`,
  `BTY-X17841100320021`, `BTY-X4452500320021`,
  `BTY-X17921200320021`, `BTY-X17359700320021`,
  `BTY-X1567200320021`, `BTY-X8707400320021`,
  `BTY-X17330500320021`, `BTY-X17457700320021`,
  `BTY-X11148300320021`, `BTY-X9400900320021`,
  `BTY-X17354100320021`, `BTY-X17203000320021`,
  `BTY-X3247600320021`, `BTY-X17515800320021`,
  `BTY-X87052700320022`, `BTY-X16361900320021`,
  `BTY-X17951300320021`, `BTY-X17329700320021`.
- A Konyári Loliense vörösbor balatonboglári eredetét a pontos,
  14,5%-os vörös termékváltozat és több közvetlen termékforrás igazolja.
- A Varga 3 literes Zweigelt–Cabernet Sauvignon közvetlen képe és pontos
  termékleírása műanyag borzsákot, a Mátra-Bacchus 5 literes Cabernet
  Sauvignon képe pedig papír külső csomagolást igazol.
- Módosított rekord: **3**.
- Módosított tulajdonságmező: **3**.
- Változatlanul helyes rekord: **22** (`BTY-X17959400320021`,
  `BTY-X17365400320021`, `BTY-X12978400320021`,
  `BTY-X17330200320021`, `BTY-X18005800320021`,
  `BTY-X17763800320021`, `BTY-X17393200320021`,
  `BTY-X17841100320021`, `BTY-X4452500320021`,
  `BTY-X17921200320021`, `BTY-X17359700320021`,
  `BTY-X1567200320021`, `BTY-X8707400320021`,
  `BTY-X17330500320021`, `BTY-X17457700320021`,
  `BTY-X17354100320021`, `BTY-X17203000320021`,
  `BTY-X17515800320021`, `BTY-X87052700320022`,
  `BTY-X16361900320021`, `BTY-X17951300320021`,
  `BTY-X17329700320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X11148300320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X9400900320021` | csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X3247600320021` | csomagolás anyaga `egyéb` → `papír` |

### 046. köteg – Borok és boralapú italok, natúr ízek 951–975.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17510300320021`,
  `BTY-X17370400320021`, `BTY-X95904200320021`,
  `BTY-X95904200320022`, `BTY-X17363300320021`,
  `BTY-X17363300320022`, `BTY-X18007700320021`,
  `BTY-X17862700320021`, `BTY-X2776400320021`,
  `BTY-X12219700320021`, `BTY-X12219600320021`,
  `BTY-X5215300320021`, `BTY-X17363400320021`,
  `BTY-X17363400320022`, `BTY-X78334900320022`,
  `BTY-X2485500320021`, `BTY-X17365200320021`,
  `BTY-X17230600320021`, `BTY-X17511400320021`,
  `BTY-X79560600320022`, `BTY-X17380400320021`,
  `BTY-X5984100320021`, `BTY-X15241300320021`,
  `BTY-X17272800320021`, `BTY-X17228600320021`.
- A Varga Merlot és a 750 ml-es Zweigelt–Cabernet Sauvignon eredetét nem
  pontosítottuk: a közvetlen előlapi képek és a pontos terméknevek nem
  tartalmaznak borvidéket, eltérő Varga-termékváltozatból pedig nem
  következtettünk.
- A két Weinhaus Egri Bikavér márkáját a pontos név, a címke és a gyártó
  terméklistája együtt igazolja.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **7**.
- Változatlanul helyes rekord: **18** (`BTY-X17510300320021`,
  `BTY-X17370400320021`, `BTY-X17363300320021`,
  `BTY-X17363300320022`, `BTY-X17862700320021`,
  `BTY-X2776400320021`, `BTY-X17363400320021`,
  `BTY-X17363400320022`, `BTY-X78334900320022`,
  `BTY-X2485500320021`, `BTY-X17365200320021`,
  `BTY-X17230600320021`, `BTY-X17511400320021`,
  `BTY-X79560600320022`, `BTY-X17380400320021`,
  `BTY-X15241300320021`, `BTY-X17272800320021`,
  `BTY-X17228600320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X95904200320021` | márka `márka nélkül` → `Weinhaus` |
| `BTY-X95904200320022` | márka `márka nélkül` → `Weinhaus` |
| `BTY-X18007700320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X12219700320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X12219600320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X5215300320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X5984100320021` | csomagolás anyaga `egyéb` → `műanyag` |

### 047. köteg – Borok és boralapú italok, natúr ízek 976–1000.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X12538900320021`,
  `BTY-X15226900320021`, `BTY-X15266700320021`,
  `BTY-X15266900320021`, `BTY-X15482100320021`,
  `BTY-X15689900320021`, `BTY-X15690100320021`,
  `BTY-X15850300320021`, `BTY-X16026300320021`,
  `BTY-X16026300320022`, `BTY-X17188100320021`,
  `BTY-X17212900320021`, `BTY-X17213300320021`,
  `BTY-X17332100320021`, `BTY-X17332200320021`,
  `BTY-X17332300320021`, `BTY-X17332400320021`,
  `BTY-X17332500320021`, `BTY-X17332600320021`,
  `BTY-X17332700320021`, `BTY-X17332800320021`,
  `BTY-X17332900320021`, `BTY-X17333000320021`,
  `BTY-X17333100320021`, `BTY-X17333200320021`.
- A Koch 3 literes és a Feind 10 literes közvetlen termékképe
  kartondobozos Bag-in-Box kiszerelést mutat, ezért a külső csomagolás
  anyaga `papír`.
- A KAMOCSAY Prémium Merlot terméknevét és címkéjét együtt értelmezve a
  márka `KAMOCSAY`; a Hilltop a pincészethez kapcsolódó jelölés.
- A Szent István Korona forrásneve és forráskategóriája vörösbort ír, de a
  közvetlen termékkép a Cabernet Sauvignon Rosé palackját mutatja. A pontos
  termékoldal 12%-os, száraz, dunántúli rozébort igazol, ezért a
  tulajdonságok a tényleges képi termékváltozatot követik; a forrásnevet nem
  módosítottuk.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **5**.
- Változatlanul helyes rekord: **21** (`BTY-X15226900320021`,
  `BTY-X15266700320021`, `BTY-X15266900320021`,
  `BTY-X15482100320021`, `BTY-X15689900320021`,
  `BTY-X15850300320021`, `BTY-X16026300320021`,
  `BTY-X16026300320022`, `BTY-X17213300320021`,
  `BTY-X17332100320021`, `BTY-X17332200320021`,
  `BTY-X17332300320021`, `BTY-X17332400320021`,
  `BTY-X17332500320021`, `BTY-X17332600320021`,
  `BTY-X17332700320021`, `BTY-X17332800320021`,
  `BTY-X17332900320021`, `BTY-X17333000320021`,
  `BTY-X17333100320021`, `BTY-X17333200320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X12538900320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X15690100320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X17188100320021` | márka `Hilltop` → `KAMOCSAY` |
| `BTY-X17212900320021` | alkoholtartalom `ismeretlen` → `12%`; szín `vörös` → `rozé` |

### 048. köteg – Borok és boralapú italok, natúr ízek 1001–1025.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **24**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **1**
  (`BTY-X17338700320021`).
- Képpel ellenőrzött rekordok: `BTY-X17236000320021`,
  `BTY-X17236300320021`, `BTY-X17236500320021`,
  `BTY-X17257300320021`, `BTY-X17257500320021`,
  `BTY-X17257600320021`, `BTY-X17257700320021`,
  `BTY-X17258100320021`, `BTY-X17258200320021`,
  `BTY-X17258300320021`, `BTY-X17258400320021`,
  `BTY-X17258700320021`, `BTY-X17259700320021`,
  `BTY-X17272200320021`, `BTY-X17272300320021`,
  `BTY-X17297500320021`, `BTY-X17329600320021`,
  `BTY-X17330400320021`, `BTY-X17338100320021`,
  `BTY-X17339800320021`, `BTY-X17354500320021`,
  `BTY-X17354600320021`, `BTY-X17355000320021`,
  `BTY-X17355200320021`.
- Az Etyeki Kúria Red helyi képe hiányzik, ezért csak az azonos 750 ml-es
  termék pontos kereskedelmi leírásával és a pincészet hivatalos
  termékoldalával alátámasztott adatokat módosítottuk: 13% alkoholtartalom,
  száraz vörösbor, soproni termőterületről.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **2**.
- Változatlanul helyes rekord: **24** (`BTY-X17236000320021`,
  `BTY-X17236300320021`, `BTY-X17236500320021`,
  `BTY-X17257300320021`, `BTY-X17257500320021`,
  `BTY-X17257600320021`, `BTY-X17257700320021`,
  `BTY-X17258100320021`, `BTY-X17258200320021`,
  `BTY-X17258300320021`, `BTY-X17258400320021`,
  `BTY-X17258700320021`, `BTY-X17259700320021`,
  `BTY-X17272200320021`, `BTY-X17272300320021`,
  `BTY-X17297500320021`, `BTY-X17329600320021`,
  `BTY-X17330400320021`, `BTY-X17338100320021`,
  `BTY-X17339800320021`, `BTY-X17354500320021`,
  `BTY-X17354600320021`, `BTY-X17355000320021`,
  `BTY-X17355200320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17338700320021` | alkoholtartalom `ismeretlen` → `13%`; eredet `Etyek-Buda` → `Sopron` |

### 049. köteg – Borok és boralapú italok, natúr ízek 1026–1050.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17365500320021`,
  `BTY-X17369000320021`, `BTY-X17369200320021`,
  `BTY-X17369300320021`, `BTY-X17369400320021`,
  `BTY-X17369500320021`, `BTY-X17371700320021`,
  `BTY-X17372000320021`, `BTY-X17392600320021`,
  `BTY-X17392700320021`, `BTY-X17435000320021`,
  `BTY-X17457800320021`, `BTY-X17458100320021`,
  `BTY-X17458400320021`, `BTY-X17493400320021`,
  `BTY-X17515900320021`, `BTY-X17516000320021`,
  `BTY-X17516200320021`, `BTY-X17516300320021`,
  `BTY-X17563100320021`, `BTY-X17563400320021`,
  `BTY-X17600200320021`, `BTY-X17662000320021`,
  `BTY-X17706100320021`, `BTY-X17823800320021`.
- A Beaujolais Nouveau palackján az `André Vonnier` név olvasható, és a
  METRO termékforrása is ezen a néven azonosítja saját márkás borát. A
  forrásrekord `BELLUSSI` brandmezője és a címkén szereplő név nem egy
  összetett márka, ezért a korábbi összefűzött értéket megszüntettük.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul helyes rekord: **24** (`BTY-X17365500320021`,
  `BTY-X17369000320021`, `BTY-X17369200320021`,
  `BTY-X17369300320021`, `BTY-X17369400320021`,
  `BTY-X17369500320021`, `BTY-X17371700320021`,
  `BTY-X17372000320021`, `BTY-X17392600320021`,
  `BTY-X17392700320021`, `BTY-X17435000320021`,
  `BTY-X17457800320021`, `BTY-X17458100320021`,
  `BTY-X17458400320021`, `BTY-X17493400320021`,
  `BTY-X17515900320021`, `BTY-X17516000320021`,
  `BTY-X17516200320021`, `BTY-X17516300320021`,
  `BTY-X17563100320021`, `BTY-X17563400320021`,
  `BTY-X17662000320021`, `BTY-X17706100320021`,
  `BTY-X17823800320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17600200320021` | márka `BELLUSSI ANDRE VONNIER` → `André Vonnier` |

### 050. köteg – Borok és boralapú italok, natúr ízek 1051–1076.

- Ellenőrzött rekord: **26**.
- Elérhető és megvizsgált közvetlen helyi kép: **26**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17841400320021`,
  `BTY-X17862900320021`, `BTY-X17870900320021`,
  `BTY-X17883500320021`, `BTY-X17883700320021`,
  `BTY-X17928200320021`, `BTY-X17928500320021`,
  `BTY-X17942200320021`, `BTY-X17998100320021`,
  `BTY-X18002200320021`, `BTY-X18002300320021`,
  `BTY-X18010200320021`, `BTY-X18014200320021`,
  `BTY-X18015300320021`, `BTY-X18023300320021`,
  `BTY-X18025600320021`, `BTY-X18028100320021`,
  `BTY-X18028300320021`, `BTY-X18033000320021`,
  `BTY-X18034500320021`, `BTY-X18034600320021`,
  `BTY-X18034700320021`, `BTY-X18036700320021`,
  `BTY-X18081500320021`, `121319528`, `BTY-X18098600320021`.
- A Balla Kolna Feketeleányka pontos termékváltozata a Ménesi borvidékről
  származik. Az Ikon Evangelista Balatonboglárhoz, a Konyári Fecske és a
  Bujdosó Kalóz pedig a Balatonon belül a Balatonboglári borvidékhez
  köthető.
- A Gere Tamás Tripla Cuvée közvetlen képe a régebbi, `Gere Tamás`
  címkeváltozatot mutatja; az azonos METRO-termék korabeli katalógusa ehhez
  a változathoz 13%-os alkoholtartalmat ad meg.
- A Varga Piroschka neve, képe és termékleírása egyaránt az `Extra Bubis`
  változatot azonosítja; a leírás kifejezetten magas szénsavtartalmat ad
  meg, ezért a `szénsavmentes` érték téves volt.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **7**.
- Változatlanul helyes rekord: **19** (`BTY-X17870900320021`,
  `BTY-X17928200320021`, `BTY-X17928500320021`,
  `BTY-X17942200320021`, `BTY-X17998100320021`,
  `BTY-X18002200320021`, `BTY-X18002300320021`,
  `BTY-X18010200320021`, `BTY-X18014200320021`,
  `BTY-X18015300320021`, `BTY-X18023300320021`,
  `BTY-X18025600320021`, `BTY-X18028100320021`,
  `BTY-X18028300320021`, `BTY-X18033000320021`,
  `BTY-X18034500320021`, `BTY-X18034600320021`,
  `BTY-X18034700320021`, `BTY-X18098600320021`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17841400320021` | eredet `egyéb` → `Ménes` |
| `BTY-X17862900320021` | alkoholtartalom `ismeretlen` → `13%` |
| `BTY-X17883500320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X17883700320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X18036700320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X18081500320021` | szénsavasság `szénsavmentes` → `szénsavas` |
| `121319528` | szénsavasság `szénsavmentes` → `szénsavas` |

### 051. köteg – Borok és boralapú italok, natúr ízek 1077–1102.

- Ellenőrzött rekord: **26**.
- Elérhető és megvizsgált közvetlen helyi kép: **26**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X18116900320021`,
  `BTY-X18215800320021`, `BTY-X18215800320022`,
  `BTY-X18216400320021`, `BTY-X18216400320022`,
  `BTY-X18231600320021`, `BTY-X18285700320021`,
  `BTY-X18286600320021`, `BTY-X18286900320021`,
  `BTY-X18287900320021`, `BTY-X18315900320021`,
  `BTY-X18468900320021`, `BTY-X18542400320021`,
  `BTY-X18542500320021`, `BTY-X18567400320021`,
  `BTY-X18605600320021`, `BTY-X18607600320021`,
  `BTY-X18653500320021`, `BTY-X18664300320021`,
  `BTY-X18666400320021`, `BTY-X18697600320021`,
  `BTY-X18697600320022`, `BTY-X18710700320021`,
  `BTY-X18710800320021`, `BTY-X18714700320021`, `121322921`.
- A La Fiesta Édes Élmény vörösbor mindkét METRO-kiszerelésének és az azonos
  Tesco-terméknek a pontos termékforrása `Felső-Magyarország` eredetet igazol.
- A Gere Tamás Cabernet Sauvignon pontos változata 13,5%-os, a Schieber Patina
  Cabernet Sauvignon díszdobozos változata 14,5%-os.
- A BB Kékfrankos és BB Merlot vizsgált címke- és alkoholtartalom-változatai
  dunántúli borok. Az Ikon Shiraz 2024 Balatonboglárról származik.
- A Bock Syrah helyi képe a 2022-es évjáratot mutatja; a pincészet ehhez 14%
  alkoholtartalmat és papírdobozos üvegpalack-csomagolást ad meg.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **10**.
- Változatlanul helyes rekord: **17** (`BTY-X18116900320021`,
  `BTY-X18216400320021`, `BTY-X18216400320022`,
  `BTY-X18285700320021`, `BTY-X18287900320021`,
  `BTY-X18315900320021`, `BTY-X18468900320021`,
  `BTY-X18542500320021`, `BTY-X18567400320021`,
  `BTY-X18605600320021`, `BTY-X18653500320021`,
  `BTY-X18664300320021`, `BTY-X18697600320021`,
  `BTY-X18697600320022`, `BTY-X18710700320021`,
  `BTY-X18710800320021`, `BTY-X18714700320021`).
- Ebben a kötegben nem került be új megengedett tulajdonságérték, és meglévő
  megengedett értéket sem töröltünk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18215800320021` | eredet `egyéb` → `Felső-Magyarország` |
| `BTY-X18215800320022` | eredet `egyéb` → `Felső-Magyarország` |
| `121322921` | eredet `egyéb` → `Felső-Magyarország` |
| `BTY-X18231600320021` | alkoholtartalom `ismeretlen` → `13,5%` |
| `BTY-X18286600320021` | eredet `egyéb` → `Dunántúl` |
| `BTY-X18286900320021` | eredet `egyéb` → `Dunántúl` |
| `BTY-X18542400320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X18607600320021` | alkoholtartalom `ismeretlen` → `14,5%` |
| `BTY-X18666400320021` | alkoholtartalom `ismeretlen` → `14%`; csomagolás anyaga `üveg` → `üveg`, `papír` |

### 052. köteg – Borok és boralapú italok, natúr ízek 1103–1127.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **23**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **2**
  (`BTY-X17236200320021`, `BTY-X17236400320021`).
- Képpel ellenőrzött rekordok: `BTY-X18799400320021`,
  `BTY-X18887300320021`, `BTY-X18887700320021`,
  `BTY-X18888300320021`, `BTY-X2390000320021`,
  `BTY-X2390000320022`, `BTY-X2390100320021`,
  `BTY-X46128200320021`, `BTY-X46128200320022`,
  `BTY-X5100800320021`, `BTY-X5950600320021`,
  `BTY-X74529000320022`, `BTY-X77634200320022`,
  `BTY-X8089400320021`, `BTY-X8485500320021`,
  `BTY-X14134900320021`, `BTY-X13988200320021`,
  `BTY-X14741700320021`, `BTY-X15266800320021`,
  `BTY-X15628800320021`, `BTY-X15690800320021`,
  `BTY-X15690900320021`, `BTY-X16549900320021`.
- A Dankó Kékfrankos pontos termékváltozata 10,5%-os. A többi Dankó és Borbár
  rekordnál a név, címke és pontos termékforrás a jelenlegi édességet és
  Duna–Tisza közi vagy felső-magyarországi eredetet igazolja.
- A Teleki 3 literes közvetlen képe kartondobozos Bag-in-Box kiszerelést mutat;
  az alkoholtartalom a képen jól olvasható 14,5%, ezért csak a csomagolást
  javítottuk.
- A Hüttenglut 10 literes terméke német, félédes, fűszerezett forralt bor
  kartondobozban. A pontos termékadat szegfűszeg-, fahéj-, narancshéj- és
  citromhéjkivonatot sorol fel.
- Az Odonata közvetlen termékképén a Bősz Adrián név kétszer is szerepel; a
  pontos termékforrás szintén a szekszárdi Bősz Borászati Kft.-t igazolja. A
  forrásnév elején álló `Gere Tamás` nem a képen látható termék márkája.
- A Bock Ermitage 1,5 literes képe az üvegpalack mellett a papírdobozt is
  mutatja. Az Ikon Evangelista Balatonboglárról, a Dóka Éva Sató St. Gróth
  pedig a Zalai borvidékről származik.
- A két kép nélküli Eszterbauer terméknél a teljes forrásnév és a pontos
  termékváltozatok forrásai igazolják a jelenlegi márkát, kiszerelést,
  alkoholtartalmat, száraz vörös jelleget és szekszárdi eredetet.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **10**.
- Változatlanul helyes rekord: **18** (`BTY-X18799400320021`,
  `BTY-X18887700320021`, `BTY-X18888300320021`,
  `BTY-X2390000320021`, `BTY-X2390000320022`,
  `BTY-X2390100320021`, `BTY-X46128200320021`,
  `BTY-X46128200320022`, `BTY-X5100800320021`,
  `BTY-X5950600320021`, `BTY-X74529000320022`,
  `BTY-X77634200320022`, `BTY-X8089400320021`,
  `BTY-X13988200320021`, `BTY-X15266800320021`,
  `BTY-X15690900320021`, `BTY-X17236200320021`,
  `BTY-X17236400320021`).
- Új megengedett érték: **3** (`márka: Bősz Adrián`,
  `eredet: Németország`, `íz: fűszeres`). Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18887300320021` | alkoholtartalom `ismeretlen` → `10,5%` |
| `BTY-X8485500320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X14134900320021` | íz `natúr` → `fűszeres`; csomagolás anyaga `egyéb` → `papír`; édesség `egyéb` → `félédes`; eredet `egyéb` → `Németország` |
| `BTY-X14741700320021` | márka `Gere Tamás & Zsolt` → `Bősz Adrián` |
| `BTY-X15628800320021` | csomagolás anyaga `üveg` → `üveg`, `papír` |
| `BTY-X15690800320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X16549900320021` | eredet `egyéb` → `Zala` |

### 053. köteg – Borok és boralapú italok, natúr ízek 1128–1152.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **23**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **2**
  (`BTY-X17447300320021`, `BTY-X18005900320021`).
- Képpel ellenőrzött rekordok: `BTY-X17272900320021`,
  `BTY-X17297400320021`, `BTY-X17297600320021`,
  `BTY-X17330100320021`, `BTY-X17404000320021`,
  `BTY-X17447900320021`, `BTY-X17510600320021`,
  `BTY-X17511500320021`, `BTY-X17573300320021`,
  `BTY-X17573400320021`, `BTY-X17674100320021`,
  `BTY-X17883400320021`, `BTY-X17896600320021`,
  `BTY-X18884300320021`, `BTY-X18884400320021`,
  `BTY-X74515700320022`, `BTY-X8158700320021`,
  `BTY-X86592800320022`, `BTY-X8712500320021`,
  `BTY-X88652900320022`, `BTY-X9049200320021`,
  `BTY-X9092400320021`, `BTY-X9363800320021`.
- A Garamvári Premium Syrah közvetlen képe és a pincészet pontos
  termékoldala Balatonboglárt igazol. A Sol Montis 19 literes KEG közvetlen
  képén a fémhordó egyértelműen látható.
- A kép nélküli Balla Géza Kolna Kadarka teljes forrásneve a Balla Géza
  terméket azonosítja, a pontos borforrások pedig a Ménesi borvidéket
  igazolják. A forrásnév elején álló `Takler` és a korábbi `Szekszárd`
  érték nem ehhez a termékhez tartozott.
- A két Ostoros Birtok termék közvetlen címkéje, teljes neve és a pincészet
  hivatalos márkaszűrője az `Ostoros` márkaformát igazolja. Az
  `Ostorosbor` megengedett értéket nem töröltük, mert további 110, még felül
  nem vizsgált rekord használja.
- A Varga Aranymetszés Cabernet Sauvignon képe DHC Eger eredetjelölést
  mutat, pontos termékforrása pedig 13,5%-os alkoholtartalmat ad meg.
- A Bősz Adrián Adriano közvetlen címkéjén és palackzáró fóliáján a Bősz
  Adrián név olvasható; a forrásnévben szereplő `Gere Tamás` nem a képen
  látható termék márkája.
- A Thummerer Cabernet Sauvignon Superior és Vili Papa Cuvée
  alkoholtartalmát `ismeretlen` értéken hagytuk: a források évjáratonként
  eltérő értékeket adnak meg, a helyi képek és rekordok pedig nem
  azonosítják az évjáratot.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **18** (`BTY-X17272900320021`,
  `BTY-X17297400320021`, `BTY-X17297600320021`,
  `BTY-X17330100320021`, `BTY-X17447300320021`,
  `BTY-X17447900320021`, `BTY-X17510600320021`,
  `BTY-X17511500320021`, `BTY-X17573300320021`,
  `BTY-X17573400320021`, `BTY-X17674100320021`,
  `BTY-X17883400320021`, `BTY-X74515700320022`,
  `BTY-X8158700320021`, `BTY-X8712500320021`,
  `BTY-X88652900320022`, `BTY-X9049200320021`,
  `BTY-X9092400320021`).
- Új megengedett érték: **1** (`márka: Ostoros`). Törölt megengedett
  érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17404000320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X17896600320021` | csomagolás anyaga `egyéb` → `fém` |
| `BTY-X18005900320021` | márka `Takler` → `Balla Géza`; eredet `Szekszárd` → `Ménes` |
| `BTY-X18884300320021` | márka `Ostorosbor` → `Ostoros` |
| `BTY-X18884400320021` | márka `Ostorosbor` → `Ostoros` |
| `BTY-X86592800320022` | alkoholtartalom `ismeretlen` → `13,5%`; eredet `egyéb` → `Eger` |
| `BTY-X9363800320021` | márka `Gere Tamás & Zsolt` → `Bősz Adrián` |

### 054. köteg – Borok és boralapú italok, natúr ízek 1153–1177.

- Ellenőrzött rekord: **25**.
- Elérhető és megvizsgált közvetlen helyi kép: **25**.
- Közvetlen helyi kép nélkül ellenőrzött rekord: **0**.
- Képpel ellenőrzött rekordok: `BTY-X17187400320021`,
  `BTY-X17235900320021`, `BTY-X17338200320021`,
  `BTY-X17359000320021`, `BTY-X17447400320021`,
  `BTY-X17494700320021`, `BTY-X17495000320021`,
  `BTY-X18125900320021`, `BTY-X8438700320021`,
  `BTY-X17434800320021`, `BTY-X17338800320021`,
  `BTY-X17393100320021`, `BTY-X17339200320021`,
  `BTY-X87054100320022`, `BTY-X13627000320021`,
  `BTY-X17527000320021`, `BTY-X7388600320021`,
  `BTY-X17257400320021`, `BTY-X5215200320021`,
  `BTY-X17522100320021`, `BTY-X17468800320021`,
  `BTY-X17368800320021`, `BTY-X17365100320021`,
  `BTY-X3718500320021`, `BTY-X17392000320021`.
- A Michel Laurent Rosé d'Anjou 10,5%-os pontos METRO-termékadata félszáraz
  bort igazol, ezért a korábbi `száraz` érték téves volt.
- A Vallefiore és a Feind 5 literes termékképe kartondobozos Bag-in-Box
  kiszerelést mutat. A Hilltop Bortarisznya közvetlen képe ezzel szemben
  csappal ellátott, hajlékony műanyag tasakot ábrázol.
- A Figula Rosé Cuvée pontos 13,5%-os változata Balatonfüred-Csopakhoz, az
  Ikon Rosé pedig Balatonboglárhoz tartozik. A Feind 5 literes címkéje és
  pontos termékadata kizárólag `Balaton` eredetet, a Varga 750 ml-es
  félszáraz rozé pontos termékadata pedig `Balatonmellék` eredetet igazol.
- A két Varga Ház Bora nevében szereplő `Bubis`, a pontos termékadatok és
  a termékváltozatok leírása szénsavas bort igazol; a `szénsavmentes` érték
  mindkét rekordnál téves volt.
- A Taschner 187 ml-es képén a `Hungary • Sopron` eredetjelölés olvasható.
  A METRO azonos kis kiszerelésű Taschner Rosé termékadata 12,5%-os
  alkoholtartalmat ad meg.
- A Juhász termék helyi képe azonos a repóban szereplő, másik áruházból
  származó Juhász Felső-Magyarországi Rosé Gyöngyözőbor képével. Annak
  teljes rekordja, a pincészet termékadata és a pontos kereskedelmi forrás
  egyaránt 12%-os, száraz rosé gyöngyözőbort igazol, ezért a rekordot a
  meglévő pezsgő-, habzóbor- és gyöngyözőbor-ág sémájára soroltuk át.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **20**.
- Változatlanul helyes rekord: **14** (`BTY-X17187400320021`,
  `BTY-X17235900320021`, `BTY-X17338200320021`,
  `BTY-X17359000320021`, `BTY-X17447400320021`,
  `BTY-X17494700320021`, `BTY-X18125900320021`,
  `BTY-X17434800320021`, `BTY-X17338800320021`,
  `BTY-X17393100320021`, `BTY-X17527000320021`,
  `BTY-X17257400320021`, `BTY-X17368800320021`,
  `BTY-X17392000320021`).
- Ebben a kötegben nem került be új megengedett tulajdonságérték, és meglévő
  megengedett értéket sem töröltünk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17495000320021` | édesség `száraz` → `félszáraz` |
| `BTY-X8438700320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X17339200320021` | eredet `Balaton` → `Balatonfüred-Csopak` |
| `BTY-X87054100320022` | szénsavasság `szénsavmentes` → `szénsavas` |
| `BTY-X13627000320021` | csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X7388600320021` | szénsavasság `szénsavmentes` → `szénsavas` |
| `BTY-X5215200320021` | csomagolás anyaga `egyéb` → `papír`; eredet `Balaton`, `Balatonmellék` → `Balaton` |
| `BTY-X17522100320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X17468800320021` | alkoholtartalom `ismeretlen` → `12,5%`; eredet `egyéb` → `Sopron` |
| `BTY-X17365100320021` | Bor és boralapú ital → Pezsgő, habzóbor és gyöngyözőbor; alkoholtartalom `ismeretlen` → `12%`; fajta `gyöngyözőbor`; szőlőfajta `egyéb`; eredet `Eger` → `Felső-Magyarország`; a borág négy, célágban nem használt mezője kikerült |
| `BTY-X3718500320021` | eredet `Dunántúl` → `Balatonmellék` |

### 055. köteg – Borok és boralapú italok, natúr ízek 1178–1202.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **23**.
- Más terméket ábrázoló, ezért bizonyítékként nem használt helyi kép: **2**
  (`BTY-X12538700320021`, `BTY-X17562900320021`).
- A forrásnév szerinti termékkép alapján is ellenőrzött rekordok:
  `BTY-X17562800320021`, `BTY-X17515700320021`,
  `BTY-X6693000320021`, `BTY-X17228900320021`,
  `BTY-X6693300320021`, `BTY-X17510700320021`,
  `BTY-X17272700320021`, `BTY-X17354300320021`,
  `BTY-X17392400320021`, `BTY-X15778900320021`,
  `BTY-X16698300320021`, `BTY-X17174800320021`,
  `BTY-X17206900320021`, `BTY-X17276100320021`,
  `BTY-X17330300320021`, `BTY-X17353900320021`,
  `BTY-X17359500320021`, `BTY-X17360200320021`,
  `BTY-X17361900320021`, `BTY-X17366000320021`,
  `BTY-X17403700320021`, `BTY-X17458600320021`,
  `BTY-X17552400320021`.
- A Varga 750 ml-es `Bubis` rozé pontos termékadata szénsavas, balatoni
  száraz rozébort igazol; a korábbi `szénsavmentes`, `Dunántúl` páros
  téves volt.
- A Koch 3 literes rekord helyi képe egy palackos Koch-terméket mutat, ezért
  a képet nem használtuk bizonyítékként. A teljes forrásnév és több pontos
  termékforrás ugyanakkor azonos 3 literes Bag-in-Box Kékfrankos Rosét
  igazol, ezért a csomagolás anyaga `papír`.
- Az Ostoros 3 literes közvetlen képén az `Ostoros`, `Egri Rozé`,
  `száraz rozébor` és `3 L` jelölések egyaránt olvashatók. A 12%-os pontos
  termékváltozat száraz, míg a félszáraz Ostoros BIB külön, 12,5%-os
  változat. A kartondobozos kép a `papír` csomagolást is igazolja.
- A Frittmann 3 literes közvetlen képe kartondobozos Bag-in-Box kiszerelést
  mutat. A Nyakas Rosé az Etyek–Budai borvidékről származik, nem
  Neszmélyről.
- A Bujdosó Mentőöv Balatonboglárhoz és a Balatonhoz, a Garamvári Rosé Gold
  Balatonboglárhoz tartozik. Az Ostoros Egri Rozé palackján és teljes
  forrásnevében az `Ostoros` márkaforma szerepel.
- A Varga Aranymetszés Friss Egri Kékfrankos Rozé pontos
  termékváltozata 12,5%-os.
- A `BTY-X17562900320021` helyi képe tévesen Dúzsi Lányvár 246 vörösbort
  mutat. A teljes METRO-forrásnév és a pontos Dúzsi Cabernet
  Sauvignon–Kékfrankos Rozé termékforrás igazolja a jelenlegi 13%-os,
  száraz szekszárdi rozébesorolást, ezért a rekordot nem módosítottuk.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **12**.
- Változatlanul helyes rekord: **16** (`BTY-X17562800320021`,
  `BTY-X17515700320021`, `BTY-X6693000320021`,
  `BTY-X17228900320021`, `BTY-X17510700320021`,
  `BTY-X17272700320021`, `BTY-X17354300320021`,
  `BTY-X17392400320021`, `BTY-X17174800320021`,
  `BTY-X17276100320021`, `BTY-X17330300320021`,
  `BTY-X17353900320021`, `BTY-X17359500320021`,
  `BTY-X17361900320021`, `BTY-X17366000320021`,
  `BTY-X17562900320021`).
- Ebben a kötegben nem került be új megengedett tulajdonságérték, és meglévő
  megengedett értéket sem töröltünk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X6693300320021` | szénsavasság `szénsavmentes` → `szénsavas`; eredet `Dunántúl` → `Balaton` |
| `BTY-X12538700320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X15778900320021` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `egyéb` → `papír`; édesség `félszáraz` → `száraz` |
| `BTY-X16698300320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X17206900320021` | eredet `Neszmély` → `Etyek-Buda` |
| `BTY-X17360200320021` | eredet `Balaton` → `Balaton`, `Balatonboglár` |
| `BTY-X17403700320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X17458600320021` | márka `Ostorosbor` → `Ostoros` |
| `BTY-X17552400320021` | alkoholtartalom `ismeretlen` → `12,5%` |

### 056. köteg – Borok és boralapú italok, natúr ízek 1203–1227.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A SOL MONTIS és a Mátra-Bacchus 5 literes termékének közvetlen képe
  kartondobozos Bag-in-Box kiszerelést mutat, ezért a csomagolás anyaga
  mindkét rekordnál `papír`.
- A Bárdos Cabernet Sauvignon Rosé a Mátrához, a Konyári Rosé és mindkét
  BB Rosé Cuvée a Balatonboglári borvidékhez tartozik; az általános vagy
  pontatlan eredetértékeket ezekre a bizonyított borvidékekre pontosítottuk.
- A Lafi Hugo Sex on the Beach teljes forrásneve és palackcímkéje egyaránt
  `barack-áfonya-narancs` ízű, szénsavas boralapú koktélt igazol, ezért a
  téves `natúr` ízt a három elemi ízérték váltotta fel.
- Az Ostoros Birtok Egri Rosé palackján és forrásnevében is az `Ostoros`
  márkaforma szerepel, ezért az `Ostorosbor` értéket egységesítettük.
- A Mateus Rosé portugál bor, és a pontos termékleírások enyhén szénsavas
  rozéként írják le; ennek megfelelően az eredete `Portugália`, a
  szénsavassága pedig `szénsavas`.
- A Lelovits Rosé Cuvée alkoholtartalma évjáratonként eltérő forrásadatokkal
  szerepel, a helyi képen pedig sem évjárat, sem alkoholfok nem olvasható.
  Emiatt a bizonyítatlan találgatás helyett az `ismeretlen` értéket
  megőriztük.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **10**.
- Változatlanul helyes rekord: **16** (`BTY-X17575500320021`,
  `BTY-X17662900320021`, `BTY-X17871100320021`,
  `BTY-X17884900320021`, `BTY-X18012200320021`,
  `BTY-X18014100320021`, `BTY-X18028200320021`,
  `BTY-X18165800320021`, `BTY-X18216000320021`,
  `BTY-X18216000320022`, `BTY-X18697500320021`,
  `BTY-X18697500320022`, `BTY-X2389900320021`,
  `BTY-X2389900320022`, `BTY-X2909800320021`,
  `BTY-X2909800320022`).
- Ebben a kötegben nem került be új megengedett tulajdonságérték, és meglévő
  megengedett értéket sem töröltünk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18002900320021` | eredet `egyéb` → `Mátra` |
| `BTY-X18007600320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X18015100320021` | eredet `Balaton` → `Balatonboglár` |
| `BTY-X18182700320021` | íz `natúr` → `barack`, `áfonya`, `narancs` |
| `BTY-X18287200320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X18287300320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X18710600320021` | márka `Ostorosbor` → `Ostoros` |
| `BTY-X3247500320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X3729900320021` | eredet `egyéb` → `Portugália`; szénsavasság `szénsavmentes` → `szénsavas` |

### 057. köteg – Borok és boralapú italok, natúr ízek 1228–1252.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **23**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **22**.
- Helyi kép nélkül: **2** (`BTY-X17435100320021`,
  `BTY-X18024700320021`).
- Más terméket ábrázoló, ezért bizonyítékként nem használt helyi kép: **1**
  (`BTY-X15688500320021`). A Feind Birtok Rosé 10 literes rekordhoz rendelt
  kép Feind Sauvignon Blanc tasakot mutat; ezért a rosé rekord
  csomagolóanyagát bizonyíték hiányában `egyéb` értéken hagytuk.
- A Varga Édes Bubis azonos termékének másik áruházi rekordja és a Bubis
  termékcsalád pontos adatai szénsavas balatoni rozébort igazolnak. A Varga
  Csendes Rozé pontos termékadata balatoni bort, a közvetlen kép pedig
  műanyag borzsákot mutat.
- A Feind Cabernet Rosé és a Varga Csendes Rozé közvetlen képe műanyag
  borzsákot, a Szent István Korona és a Dubicz 3 literes rozé képe
  kartondobozos Bag-in-Boxot, a SOL MONTIS 19 literes KEG képe pedig
  fémhordót igazol.
- A három Don Pablo tétel közül a Ruby és a Tawny édes portugál portói, a
  White pedig portugál portói. A White édességére egymásnak ellentmondó
  pontos források találhatók, ezért ott az `egyéb` értéket megőriztük.
  A Don Pablo Fino spanyol sherry, a kép nélküli Royal Oporto Ruby pedig
  portugál portói.
- A Zonin Limoneto címkéje és gyártói terméklapja citromlével készült,
  szénsavas olasz ízesített boralapú italt igazol üvegpalackban. A Sol de
  España Sangria pontos összetevői fűszer- és citrusaromát, közvetlen
  címkéje narancsot és vörös italt, termékadata pedig spanyol eredetet
  igazol.
- A Torres Serena Mode fehér, chilei Valle Central-i alkoholmentes
  Sauvignon Blanc. A két Natureo alkoholmentes bor közül a Muscat fehér, a
  Garnacha–Syrah vörös; mindkettő spanyol eredetű.
- A Choya Sake pontos termékadata száraz japán rizsbort és üvegpalackot
  igazol. Az Angelli Bianco gyártói adata édes, gyógynövényekkel és
  fűszerekkel ízesített román aperitifet igazol.
- A BB Rosé Cuvée a Balatonboglári borvidékhez tartozik. Az Ostoros Egri
  Bikavér közvetlen címkéjén és palackzáró fóliáján az `Ostoros` márkanév
  olvasható.
- A Paulus Gold Ezerjó alkoholfoka évjáratonként 12%, 12,5% és 13% is lehet,
  a rekord nem tartalmaz évjáratot, a helyi előlapi képen pedig nem
  olvasható alkoholfok. Emiatt az `ismeretlen` értéket megőriztük.
- Módosított rekord: **20**.
- Módosított tulajdonságmező: **36**.
- Változatlanul helyes rekord: **5** (`BTY-X15688500320021`,
  `BTY-X17435100320021`, `BTY-X18077100320021`, `1027183`, `1044093`).
- Új megengedett érték: **1** (`eredet: Románia`). Törölt megengedett
  érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X4452300320021` | szénsavasság `szénsavmentes` → `szénsavas`; eredet `Dunántúl` → `Balaton` |
| `BTY-X5984000320021` | csomagolás anyaga `egyéb` → `műanyag` |
| `BTY-X9393700320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X9400800320021` | csomagolás anyaga `egyéb` → `műanyag`; eredet `Balaton`, `Dunántúl` → `Balaton` |
| `BTY-X12022300320021` | csomagolás anyaga `egyéb` → `papír` |
| `BTY-X17896500320021` | csomagolás anyaga `egyéb` → `fém` |
| `BTY-X17533300320021` | édesség `egyéb` → `édes`; eredet `egyéb` → `Portugália` |
| `BTY-X17533500320021` | édesség `egyéb` → `édes`; eredet `egyéb` → `Portugália` |
| `BTY-X17705500320021` | eredet `egyéb` → `Portugália` |
| `BTY-X17705600320021` | eredet `egyéb` → `Spanyolország` |
| `BTY-X18024700320021` | eredet `egyéb` → `Portugália` |
| `BTY-X18233700320021` | íz `natúr` → `citrom`; szénsavasság `szénsavmentes` → `szénsavas`; csomagolás anyaga `egyéb` → `üveg`; eredet `egyéb` → `Olaszország`; bortípus `boralapú koktél` → `ízesített boralapú ital` |
| `BTY-X17467400320021` | íz `natúr` → `fűszeres`, `narancs`; szín `egyéb` → `vörös`; eredet `egyéb` → `Spanyolország` |
| `BTY-X18034900320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Valle Central` |
| `BTY-X18035000320021` | szín `egyéb` → `fehér`; eredet `egyéb` → `Spanyolország` |
| `BTY-X18035100320021` | szín `egyéb` → `vörös`; eredet `egyéb` → `Spanyolország` |
| `BTY-X17772800320021` | csomagolás anyaga `egyéb` → `üveg`; édesség `egyéb` → `száraz` |
| `BTY-X17580400320021` | íz `natúr` → `fűszeres`; édesség `egyéb` → `édes`; eredet `egyéb` → `Románia` |
| `2248826` | eredet `Balaton`, `Dunántúl` → `Balatonboglár` |
| `988122` | márka `Ostorosbor` → `Ostoros` |

### 058. köteg – Borok és boralapú italok, natúr ízek 1253–1277.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Paulus Rosé és Irsai Olivér palackzáró fóliáján egyaránt a
  `Paulus Mór` felirat olvasható. Az Irsai Olivér pontos termékadata is a
  Móri borvidéket igazolja, ezért a rosé bizonytalan, illetve az Irsai
  téves Duna–Tisza közi eredetét `Mór` értékre javítottuk.
- Az öt Ostoros-termék közvetlen címkéjén egységesen az `Ostoros` márkanév
  szerepel. Az előlapi képek ezen kívül az Olaszrizling, Irsai Olivér,
  Egri Rozé, Medina és Debrői Hárslevelű jelenlegi szín-, édesség- és
  eredetbesorolását is megerősítik.
- A két Tokaji félédes bor `Ungvár Pince` márkáját a pontos
  termékinformációk igazolják; a márkanév hiánya az előlapi címkén ezért
  nem indokolta a bizonyított érték törlését.
- A három Arany Koma közvetlen képe műanyag PET-palackot mutat, ami
  megerősíti a jelenlegi `műanyag` csomagolásértéket.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **7**.
- Változatlanul helyes rekord: **18** (`1001785`, `1001786`, `1001791`,
  `1001792`, `1001793`, `1002874`, `1002399`, `1015939`, `1000656`,
  `1000666`, `1010380`, `1050149`, `1050150`, `1054712`, `1048028`,
  `1048030`, `1048034`, `987794`).
- Ebben a kötegben nem került be új megengedett tulajdonságérték, és meglévő
  megengedett értéket sem töröltünk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1044097` | eredet `egyéb` → `Mór` |
| `1044098` | eredet `Duna-Tisza köze` → `Mór` |
| `988118` | márka `Ostorosbor` → `Ostoros` |
| `988119` | márka `Ostorosbor` → `Ostoros` |
| `988121` | márka `Ostorosbor` → `Ostoros` |
| `988123` | márka `Ostorosbor` → `Ostoros` |
| `988127` | márka `Ostorosbor` → `Ostoros` |

### 059. köteg – Borok és boralapú italok, natúr ízek 1278–1302.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Bordeaux vörösbor címkéjén a `Bordeaux` eredetmegjelölésként, nem
  elkülönülő márkanévként szerepel. A Tokaji Édes Szamorodni címkéjén a
  `Tokaji` szintén az eredetet és a bortípust jelöli; külön márka nem
  azonosítható. Mindkét téves márkaértéket `márka nélkül` értékre
  javítottuk, a Szamorodni fehér színét és tokaji eredetét pedig a pontos
  terméknév és a közvetlen kép igazolja.
- A két 3 literes Ostorosbor BIB közvetlen képe kartondobozt és `Ostoros`
  márkafeliratot mutat, ezért a márkát `Ostoros`, a csomagolás anyagát
  `papír` értékre pontosítottuk.
- A Sauska hivatalos Siller terméklapja a 12,5%-os bort villányi
  termőhelyűként írja le. A termelő és a pontos kiskereskedelmi
  termékleírás is a rozé és a könnyű vörösbor közötti sillerként, illetve
  rozétermékként kezeli, ezért a jelenlegi `rozé` színt megőriztük, és
  csak az eredetet javítottuk `Villány` értékre.
- A négy Feind-bor helyi előlapi képén nem olvasható alkoholfok. A
  Cabernet Rosé és a Syrah–Merlot pontos, de eltérő évjáratú forrásai
  különböző alkoholfokokat közölnek, ezért a Királyleányka, Chardonnay,
  Syrah–Merlot és Cabernet Rosé `ismeretlen` alkoholtartalmát nem
  helyettesítettük találgatással.
- A Frittmann Rajnai Rizling terméknevében szereplő `50 ml` ellentmond a
  teljes forrásadat 750 ml-es mennyiségének és a közvetlen 0,75 literes
  palackképnek. A jelenlegi 750 ml-es kiszerelés ezért helyes maradt.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **20** (`996268`, `999975`, `2235927`,
  `2242755`, `2243514`, `4250059`, `4250143`, `1024047`, `1040543`,
  `990814`, `1008177`, `1008187`, `1018827`, `1040538`, `1040541`,
  `1040712`, `4604453`, `995066`, `996304`, `1052340`).
- Ebben a kötegben nem került be új megengedett tulajdonságérték, és meglévő
  megengedett értéket sem töröltünk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `4603304` | márka `Bordeaux` → `márka nélkül` |
| `1050148` | márka `Tokaji` → `márka nélkül`; szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `1047926` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `egyéb` → `papír` |
| `1047923` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `egyéb` → `papír` |
| `1058782` | eredet `egyéb` → `Villány` |

### 060. köteg – Borok és boralapú italok, natúr ízek 1303–1327.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Nyakas Aligvárom és Irsai Olivér két-két áruházi rekordja ugyanazokat
  a közvetlen termékképeket és termékváltozatokat tartalmazza, mégis három
  eltérő eredetkombinációval szerepelt. A pincészet hivatalos termékadatai,
  valamint az Aligvárom 2024 és az Irsai Olivér 2021 és 2024 pontos
  évjáratadatai egyaránt az `Etyek-Buda` borvidéket igazolják. Mind a négy
  rekord eredetét erre az egy bizonyított értékre egységesítettük.
- A Tokajicum 5 puttonyos Tokaji Aszú pontos termékneve és közvetlen
  palackképe fehér borkülönlegességet igazol, ezért a bizonytalan `egyéb`
  színt `fehér` értékre javítottuk.
- A két Gere–Schubert termék palackcímkéjén `GERE & SCHUBERT` szerepel, és
  a pincészet hivatalos neve is `Gere & Schubert`. Az új, pontos
  márkaértéket felvettük és a két rekordot erre javítottuk. A korábbi
  `Gere - Schubert` értéket nem töröltük, mert még 19, felül nem vizsgált
  borrekord használja.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **7**.
- Változatlanul helyes rekord: **18** (`1023348`, `1052433`,
  `7d79937879669ddc5e8b28d5`, `55d581bb6c384bf5675a9111`,
  `0fdb704e94005369ac3859ae`, `ec9be80e5f2e72984ca3e5dd`,
  `a289fbeb4f5b30c8e1a73f2b`, `5b9352cb0e84606bfce6f09a`,
  `010cdb1ec15e209df702209e`, `5d0f364c56560514055b2323`,
  `551fc2c36f4caa59afc407d0`, `ae7b413eda882292be064eaa`,
  `b8a7c936b4aa5a50c0b0b097`, `d45b6b70e0a07f3cc39030b6`,
  `95d8a74bd303b3eea8b3d38f`, `467db6c5a528c2533da7749c`,
  `c3e225fb0b5e9b0cfea0a295`, `3ed718425ae5946134a16f1d`).
- Új megengedett érték: **1** (`márka: Gere & Schubert`). Törölt
  megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `985116` | eredet `Budai`, `Neszmély` → `Etyek-Buda` |
| `997500` | eredet `Neszmély` → `Etyek-Buda` |
| `990817` | szín `egyéb` → `fehér` |
| `7e2eaf40a7d50a6441a0b18a` | márka `Gere - Schubert` → `Gere & Schubert` |
| `d3d83c5479f2c9e4cf804fbd` | márka `Gere - Schubert` → `Gere & Schubert` |
| `1015b41b56f8fc46227ca3d9` | eredet `Budai`, `Neszmély` → `Etyek-Buda` |
| `38e7824c5fc7abd3dd374662` | eredet `Budai`, `Etyek-Buda` → `Etyek-Buda` |

### 061. köteg – Borok és boralapú italok, natúr ízek 1328–1352.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Varga Irsai Olivér Bubis pontos, 10,5%-os termékváltozata balatoni
  szénsavas száraz fehérbor, ezért az `egyéb` eredetet `Balaton` értékre
  javítottuk.
- A Varga Bubis Rozé pontos termékadata balatoni, szénsavas száraz rozé
  tájbort igazol. Az eredetet, a szénsavasságot és az édességet ennek
  megfelelően pontosítottuk. Az alkoholtartalom `ismeretlen` maradt, mert a
  rekord neve és helyi előlapi képe nem közli, a kereskedő pedig
  évjáratváltáskor eltérést jelez.
- A Nyakas Rosé pontos 13%-os termékadata OEM Etyek-Buda eredetet igazol,
  ezért a pontatlan `Budai` értéket `Etyek-Buda` értékre javítottuk.
- A Gere–Schubert Rosé Cuvée közvetlen címkéjén is `GERE & SCHUBERT`
  szerepel, ezért a márkát az előző kötegben felvett pontos értékre
  egységesítettük.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **6**.
- Változatlanul helyes rekord: **21**
  (`e8d75c2be38a3d257346802e`, `32c2852c673df871f6f5b5f0`,
  `28dcaf4e3e95f380581d328f`, `56a3882a8b1cc6ad33d11a39`,
  `0a58844ad76c6d0bbd333ea4`, `c02f5053f42e26e3abcbeb97`,
  `e71551bc073a7ae335a2e5be`, `60ec99d676455ca468a02a63`,
  `f5a31c70e18b565c97fbff6a`, `e85f36886c8d6404d931e82e`,
  `a16cc41b71295e0ba18058ab`, `96fe961215a6d67da2478557`,
  `04674d356589392d2f946dd9`, `57f60440ce94a5e19f11dbd0`,
  `ded403d332b6d19ccdbcd0c4`, `a29c2274a2e7b547e1f60f74`,
  `d33d5dc197ee3de1ee444aaf`, `ceee16fde2ffa039e2f32672`,
  `661d1440fbf3ca2605c997f3`, `574c7771fcd038443e7beb2f`,
  `052ff348dee9109a470f4901`).
- Ebben a kötegben nem került be új megengedett tulajdonságérték, és meglévő
  megengedett értéket sem töröltünk.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `fb697895153397f4e27d5e53` | eredet `egyéb` → `Balaton` |
| `75bb8b799bde5e0007df2171` | márka `Gere - Schubert` → `Gere & Schubert` |
| `65b215e5ab19645e2914c388` | szénsavasság `szénsavmentes` → `szénsavas`; édesség `egyéb` → `száraz`; eredet `egyéb` → `Balaton` |
| `9471a61c7cc55345c80b93b9` | eredet `Budai` → `Etyek-Buda` |

### 062. köteg – Borok és boralapú italok, natúr ízek 1353–1377.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Bodri QV Civilis Cuvée pontos termékadata száraz szekszárdi vörösbort
  igazol, ezért a bizonytalan `egyéb` édességet `száraz` értékre
  javítottuk.
- A Varga Merlot pontos termékadata és kiskereskedelmi kategóriája balatoni
  édes vörösbort igazol, ezért az `egyéb` eredetet `Balaton` értékre
  javítottuk. Az alkoholtartalom `ismeretlen` maradt, mert a rekord nem
  tartalmaz évjáratot, a közvetlen előlapi kép pedig nem közli az
  alkoholfokot.
- A `HHattyús` forrásnév elgépelés: a közvetlen címkén és a Disznókő
  hivatalos terméklapján is `Hattyús Tokaji Aszú 5 Puttonyos` szerepel.
  A márkát, puttonyszámot, fehér színt, édes jelleget és tokaji eredetet
  egyszerre javítottuk. A hibás `HHattyús` megengedett márkaértéket
  töröltük, mert a javítás után más borrekord nem használta.
- A Royal Tokaji 5 puttonyos Aszú pontos neve és közvetlen képe fehérbort
  igazol, ezért a színt `fehér` értékre javítottuk.
- A Royal Hugo Mojito címkéjén külön olvasható a `menta` és `lime`;
  a téves `natúr` ízt erre a két meglévő, elemi ízértékre cseréltük.
- Az Ostoros 3 literes Olaszrizling képe `Ostoros` márkafeliratú
  kartondobozos Bag-in-Boxot mutat, ezért a márkát és a csomagolás anyagát
  is pontosítottuk.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **11**.
- Változatlanul helyes rekord: **19**
  (`5708047833b06bfbc76cbfc4`, `23bcec3ab64dd9af69d71513`,
  `49fb016dc812c713d75ed4b6`, `cbe1214363317a52b002d7f4`,
  `b8e07a00fb139433831e5c2f`, `44e2d678308c26eccb4e7f50`,
  `2bd7abba0ff9c54c3eae06e2`, `4d7be59b7035d77caecb7f34`,
  `c8ac2fdd06eeef33cb77f289`, `1ead191d14e6eda0e4be0436`,
  `b5c5206f372c34a52aeea2df`, `859965b8d2c5d9b81f898151`,
  `474ff7197fe98413a310a7d9`, `720b97588c0dea8c01cf9461`,
  `06eeceebe76129c31602a045`, `e29e14b6eae36fe5c6e86669`,
  `3137dcf2b78c43560ddf0bea`, `fd612253bea20c0cc4f699c8`,
  `e99492d63a3ba9e5895467e5`).
- Új megengedett érték: **0**. Törölt megengedett érték: **1**
  (`márka: HHattyús`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `9d608976117f8655000fa67f` | édesség `egyéb` → `száraz` |
| `b46cb4d88069fc2f5c5669f3` | eredet `egyéb` → `Balaton` |
| `80c88310dba11d0461473079` | márka `HHattyús` → `Hattyús`; puttonyszám `nem alkalmazható` → `5 puttonyos`; szín `egyéb` → `fehér`; édesség `egyéb` → `édes`; eredet `egyéb` → `Tokaj` |
| `d2aacd508876de8b07421ec0` | szín `egyéb` → `fehér` |
| `068e4ac4bdac8260053b9321` | íz `natúr` → `menta`, `lime` |
| `6a7c5db571a2b4b9b461031f` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `egyéb` → `papír` |

### 063. köteg – Borok és boralapú italok, natúr ízek 1378–1402.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Frittmann 3 literes Olivér Cuvée képe kartondobozos Bag-in-Boxot mutat,
  ezért a csomagolás anyagát `egyéb` értékről `papír` értékre
  pontosítottuk.
- A Grand Tokaj Aszú és Szamorodni pontos neve egyaránt édes fehérbort
  igazol, ezért a bizonytalan `egyéb` színt mindkét rekordnál `fehér`
  értékre javítottuk.
- A Királyleányka és Chardonnay közvetlen címkéjén `OSTOROS` olvasható,
  ezért az `Ostorosbor` márkaértéket mindkét rekordnál `Ostoros` értékre
  egységesítettük.
- A Paulus Gold Chardonnay és Generosa közvetlen palackcímkéjén `MÓR`
  szerepel. A Chardonnay téves `Duna-Tisza köze` eredetét, illetve a
  Generosa téves `Duna-Tisza köze, Mór` kettős értékét ezért `Mór`
  értékre javítottuk. Az alkoholtartalom `ismeretlen` maradt, mert a
  rekordnév és az előlapi kép nem ad meg alkoholfokot vagy évjáratot.
- A Gere & Schubert Irsai Olivér közvetlen címkéje `GERE & SCHUBERT`
  márkanevet mutat, ezért a korábbi `Gere - Schubert` alakot a már
  meglévő `Gere & Schubert` értékre javítottuk.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **8**.
- Változatlanul helyes rekord: **17**
  (`e6b070626886fa89b4014c18`, `cc38d8e204ae62f9f6b4dc2e`,
  `0a2572c6f18c0ee0ac4fcb9c`, `c1e9e7b863e2a2f11526a1bb`,
  `83a31444e304efce6f55a557`, `b4b0dfbb31ed5f5d316e036d`,
  `17b22ecad0c9d55a6d3a4d4d`, `4d141c4faed8abf331dc1d80`,
  `ff3f226c5296325da99d92b4`, `f916e1747e5e4ca138238371`,
  `7092471adf09d13e0938d3b8`, `fbd9893db6181bdd8814bc9a`,
  `c93e7669ae258bd124002afb`, `35c5e63cbcb7e47a4f0a115a`,
  `6679143b7c1c9cd5ba35fad3`, `d571ae9f442d7c7b1af979d5`,
  `cca7554b5a42a0febe940d86`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `f1e55a9cf96c600930b7064d` | csomagolás anyaga `egyéb` → `papír` |
| `1960d1668b9219af7a15fd09` | szín `egyéb` → `fehér` |
| `9e71610057f5868e786c0f49` | szín `egyéb` → `fehér` |
| `821786a83b1f6fc5467f82c8` | márka `Ostorosbor` → `Ostoros` |
| `4345fe47d72cf23773360c34` | eredet `Duna-Tisza köze` → `Mór` |
| `b649e24f2d9c2ff3ae8e2a21` | eredet `Duna-Tisza köze, Mór` → `Mór` |
| `38c7832495e0a73f090978cc` | márka `Ostorosbor` → `Ostoros` |
| `f80f1b1317bf4eed3bf43a6e` | márka `Gere - Schubert` → `Gere & Schubert` |

### 064. köteg – Borok és boralapú italok, natúr ízek 1403–1427.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Kreinbacher Birtok hivatalos kínálata a cuvée-t `Nagy-Somlói`
  eredetmegjelöléssel közli, és a közvetlen címke is ezt a tételt ábrázolja;
  ezért a rövidített `Somló` eredetet `Nagy-Somló` értékre pontosítottuk.
- Az Ostoros Muskotály közvetlen címkéjén `OSTOROS` olvasható, ezért az
  `Ostorosbor` márkaértéket `Ostoros` értékre javítottuk.
- A generic Tokaji Sárgamuskotály közvetlen képe ugyanazt a címkecsaládot
  mutatja, mint az Ungvár Pince Hárslevelű és Furmint tételei; a pontos
  kiskereskedelmi termékadat az Ungvár-Pince Kft.-t nevezi meg gyártóként.
  Ezért a `márka nélkül` értéket `Ungvár Pince` értékre javítottuk.
- A Nyakas Pince hivatalos terméklapja a Budai Sauvignon Blanc kategóriáját
  `OEM Etyek-Buda` alakban adja meg. A `Budai` itt a terméknév része, ezért a
  redundáns `Budai, Etyek-Buda` eredetet `Etyek-Buda` értékre
  egyszerűsítettük.
- A Bodri Blanka Sauvignon Blanc neve `Pannon` és `Szekszárd` eredetet is
  közöl; ugyanennek a terméknek a korábban kézzel ellenőrzött
  `693005:4230395` rekordja is ezt a két értéket igazolja. Ezért a hiányzó
  `Pannon` eredetértéket felvettük a termékhez.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **5**.
- Változatlanul helyes rekord: **20**
  (`874ff7dba2aa8b2321aea63f`, `e0210f60f5932f7524a50c37`,
  `b8348004016b71b29a3b8ab3`, `e6ad8ac335ecebcf79c32d7c`,
  `f3caedc63cef58b76aca0d71`, `81440df4eed22fc6be3335dd`,
  `0ef6cbea57eba79a0c224c04`, `d4cacbb512770810987cc174`,
  `f5618beffbc9000ae58c2aee`, `59eddd70754fb46a9681be4f`,
  `6060d0997b5c8493f44657ef`, `11c6e7cb962158fcb430a70f`,
  `6916fe8c121c9cbaff6e8d32`, `3e06009abef3551ba8862945`,
  `97460cfa5cb8ca633814561b`, `db0731a657c55736e5ed81c3`,
  `7f7575100c9b9a8fcffa36f0`, `aac634de1a0bf572b558a9d0`,
  `c6b05214ae389251c0b03a35`, `c56eec075f875bae02511456`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `4a48adcef86ef717e6690269` | eredet `Somló` → `Nagy-Somló` |
| `4098e822c94fe846396e7f04` | márka `Ostorosbor` → `Ostoros` |
| `2dfa24b863563faa8696075f` | márka `márka nélkül` → `Ungvár Pince` |
| `d616f3b87a5fa9faeaeb2ed2` | eredet `Budai, Etyek-Buda` → `Etyek-Buda` |
| `2bd80d9bc844aa11002609a4` | eredet `Szekszárd` → `Pannon`, `Szekszárd` |

### 065. köteg – Borok és boralapú italok, natúr ízek 1428–1452.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Figula Balatonszőlősi Sóskút Olaszrizling pontos, korábban kézzel
  ellenőrzött párrekordjai a `Balaton`, `Balatonfüred-Csopak` és
  `Balatonszőlős` eredethármast igazolják; a hiányzó
  `Balatonfüred-Csopak` értéket pótoltuk.
- A Tokajicum 5 puttonyos Aszú és a Tokaji Szamorodni pontos termékneve
  édes fehérbort közöl, ezért a bizonytalan `egyéb` színt mindkét
  rekordnál `fehér` értékre javítottuk. A Szamorodni közvetlen címkéje és
  pontos termékforrása az `Ungvár Pince` márkát is igazolja.
- A Gere–Schubert Cserszegi Fűszeres közvetlen címkéjén
  `GERE & SCHUBERT` olvasható, ezért a márka írásmódját a már meglévő,
  bizonyított értékre egységesítettük.
- A Paulus Gold Olaszrizling és Sauvignon Blanc közvetlen palackcímkéjén
  `MÓR` szerepel, ezért a téves `Duna-Tisza köze` eredetet mindkét
  rekordból eltávolítottuk. Az alkoholtartalom `ismeretlen` maradt, mert a
  rekordnév és az előlapi kép nem közöl alkoholfokot vagy évjáratot.
- A Zelna Füredi Olaszrizling közvetlen palackcímkéje a `FÜRED`
  eredetmegjelölést és a Balatonfüred–Csopaki borvidéket is feltünteti. A
  Zelna hivatalos oldala a Balatonfüred–Csopaki borvidéket, az uniós
  termékleírás pedig a `Füred` OEM önálló eredetmegjelölését igazolja.
  Ezért a termék eredetét `Balaton`, `Balatonfüred-Csopak`, `Füred`
  értékhármasra pontosítottuk, és felvettük az elemi `Füred` értéket.
- A Soltész Debrői Hárslevelű az Egri borvidék Debrői körzetének
  eredetvédett bora, ezért a meglévő `Debrő` mellé az `Eger` értéket is
  felvettük.
- A Nyakas Aligvárom, Budai Chardonnay és Irsai Olivér hivatalos
  terméklapja `OEM Etyek-Buda` eredetet közöl. A `Budai` a terméknév
  része, a Neszmély pedig az Aligvárom rekordján téves volt, ezért mindhárom
  eredetet `Etyek-Buda` értékre egységesítettük.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **12**.
- Változatlanul helyes rekord: **14**
  (`ffb029d3a9948fe6537f7d83`, `dba139fce625c7eaf71edbe6`,
  `4df284ddaaa282e140e00f8b`, `ef3b93f7a026beb2c9234330`,
  `b8e6b0c07fba11c4bdf6d223`, `e9ca9ab4aa1433d689912d78`,
  `f93be3ff363f3a0f49454910`, `07827e128c26b48ca7c182c9`,
  `cf1d950cbe78a7097f858657`, `d59641a09b3567e8af02b1f2`,
  `1bd33127869b326a6c8f7bfa`, `ad9050300d365a6998fb7e36`,
  `4961c4927d48deb1157eb478`, `a5021453a3830e72e592766e`).
- Új megengedett érték: **1** (`eredet: Füred`). Törölt megengedett
  érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `6411a7a086f8e56ba2aa53b0` | eredet `Balaton, Balatonszőlős` → `Balaton`, `Balatonfüred-Csopak`, `Balatonszőlős` |
| `e44f19c296490191488d8b94` | szín `egyéb` → `fehér` |
| `f7506653bd419ad8fd403992` | márka `márka nélkül` → `Ungvár Pince`; szín `egyéb` → `fehér` |
| `f2ac870783fcd1a2249528d3` | márka `Gere - Schubert` → `Gere & Schubert` |
| `a9aca7f406252ad90d77625b` | eredet `Duna-Tisza köze, Mór` → `Mór` |
| `acb95b250941d4c5bed47448` | eredet `Duna-Tisza köze, Mór` → `Mór` |
| `486aee3eaf3c97edd37934e2` | eredet `Balatonfüred` → `Balaton`, `Balatonfüred-Csopak`, `Füred` |
| `893a4ac2a14dc42cca5f8a57` | eredet `Debrő` → `Debrő`, `Eger` |
| `b9892f48c55403dbfa3ba192` | eredet `Budai, Neszmély` → `Etyek-Buda` |
| `4c126ebad119c258d1b3abf9` | eredet `Budai, Etyek-Buda` → `Etyek-Buda` |
| `226e58c872a446101069902f` | eredet `Budai, Etyek-Buda` → `Etyek-Buda` |

### 066. köteg – Borok és boralapú italok, natúr ízek 1453–1477.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- Az Egri Csillag, az Irsai Olivér, a Sauvignon Blanc, az Olaszrizling és
  a Debrői Hárslevelű közvetlen palackcímkéjén egyaránt `OSTOROS`
  olvasható. A pincészet hivatalos kínálata ugyanezeket a tételeket az
  Ostoros családi márka alatt közli, ezért az `Ostorosbor` értéket az öt
  rekordnál a már meglévő `Ostoros` értékre egységesítettük.
- A Debrői Hárslevelű az Egri borvidék Debrői körzetének önálló
  eredetmegjelölése; az Egri Borvidék Hegyközségi Tanácsának dokumentumai
  mindkét szintet igazolják. Ezért a meglévő `Debrő` mellé az `Eger`
  eredetértéket is felvettük.
- A 3 literes Irsai Olivér közvetlen képe `OSTOROS` feliratú,
  kartondobozos Bag-in-Boxot mutat. A márkát `Ostoros`, a csomagolás
  anyagát `papír` értékre pontosítottuk.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **8**.
- Változatlanul helyes rekord: **19**
  (`6d25f657402282e25ee150e3`, `4744074705d07cac6adf0c76`,
  `f9fa69e50af020f0a4b3d084`, `f7db23e036a3098b1ced57a0`,
  `854c880df1c8c380493509cc`, `9c66e9e2cb1dc05c37bfd736`,
  `8a039a55918141d7f5cb0b4c`, `2ae22bd59ac4cb69a1f32877`,
  `b8eded717532446626045ae9`, `1d2e82bd8c913b27bbf7f4bf`,
  `a368ccf6908ad8ca8e04886f`, `3fd8f8e5ff829175eb31ea8a`,
  `0cf04ad58819ab3bea985dc1`, `2090c892ae2c99dd46606ccd`,
  `fe41ba6054f8b641c0780704`, `fdcc3c9c88b406d77dcce774`,
  `2b9328f0a7ce4559c828be97`, `05e3f760027eed54889e17c0`,
  `13b7a514253ab73276f3027e`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `686230a6b73fbfd0e315e143` | márka `Ostorosbor` → `Ostoros` |
| `4bc3ee4c817545923f2c7e26` | márka `Ostorosbor` → `Ostoros` |
| `f29dfafe1ee4e4b33da4cd3d` | márka `Ostorosbor` → `Ostoros` |
| `9908a50cf2684727acee0b75` | márka `Ostorosbor` → `Ostoros` |
| `d96fbab529f94f4334ba4702` | márka `Ostorosbor` → `Ostoros`; eredet `Debrő` → `Debrő`, `Eger` |
| `d8b8a069c216ab68c5d978f7` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `egyéb` → `papír` |

### 067. köteg – Borok és boralapú italok, natúr ízek 1478–1502.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A BB Tramini pontos, 11%-os termékadatának regionális információja
  `Balatonboglári`. Ugyanennek a BB termékcsaládnak a közvetlen képei és
  szomszédos rekordjai is ezt a borvidéki kötődést igazolják, ezért a
  pontatlan `Dunántúl` eredetet `Balaton`, `Balatonboglár` értékekre
  javítottuk.
- A Várhegyi pontos 750 ml-es termékváltozatát több aktuális termékforrás
  Duna–Tisza közi félédes fehérborként, 11%-os alkoholtartalommal közli.
  Ezért az eredetet `Magyarország` helyett `Duna-Tisza köze`, az
  alkoholtartalmat `ismeretlen` helyett `11%` értékre pontosítottuk.
- A Gere–Schubert Sauvignon Blanc közvetlen palackcímkéjén az ampersand
  külön is jól olvasható, ezért a `Gere - Schubert` márkaalakot a már
  meglévő `Gere & Schubert` értékre egységesítettük.
- Módosított rekord: **3**.
- Módosított tulajdonságmező: **4**.
- Változatlanul helyes rekord: **22**
  (`d206efdb723e81d47f5cc34e`, `90fdc0f560d4c9ff4e594548`,
  `6452ef83e57e74f859a51462`, `f6a7f9e244d3649f86833fa9`,
  `2a7947ffaf536c721643c1c1`, `832e331c70508dacb900a1c3`,
  `6ed6697c1c249cf490a01da5`, `b6a1e9c676d14a66c5842b8d`,
  `85cba2dfd043745f270ca525`, `9d006364eeb6970195e23e1c`,
  `23355830c47f9b6278e16179`, `b5742fde1c84cb7142eb528d`,
  `9080dfa30035bdefa7a538e1`, `141bed4d271689e9084b9571`,
  `6e9b5654dffcda4f2515cfdc`, `eed0475edc36b1ff6efe076d`,
  `b2fda5080638d753b6a9035c`, `4df27bbc0ef6a25afbc6c85c`,
  `1f87b5c3ce2c147db900757d`, `1e19646cb1a6ab8f4093fe15`,
  `d6e724bdbf8fd778b4af16de`, `03a194ea821c7cbab7dda8e6`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `d1a6034ecdc6c35af4015314` | eredet `Dunántúl` → `Balaton`, `Balatonboglár` |
| `766bbc6529d91e8887da13a1` | alkoholtartalom `ismeretlen` → `11%`; eredet `Magyarország` → `Duna-Tisza köze` |
| `411fbd196554d375d6265d2d` | márka `Gere - Schubert` → `Gere & Schubert` |

### 068. köteg – Borok és boralapú italok, natúr ízek 1503–1527.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- Az El Circo Volatinero Tempranillo hivatalos termelői lapja a bort
  `Cariñena D.O.P.` eredetű, 13,5%-os spanyol vörösborként közli. A
  meglévő `Spanyolország` mellé ezért felvettük a már engedélyezett
  `Carinena` borvidékértéket.
- A Felső-Magyarországi Kékfrankos és az Egri Merlot közvetlen címkéjén
  `OSTOROS` olvasható, ezért mindkét `Ostorosbor` márkaértéket a már
  meglévő `Ostoros` értékre egységesítettük.
- A Bodri Bodrikutya termékneve `Szekszárd Pannon Cuvée`, a közvetlen kép
  pedig a név szerinti fehérbort mutatja. A meglévő `Szekszárd` mellé
  ezért a hiányzó `Pannon` eredetértéket is felvettük.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **4**.
- Változatlanul helyes rekord: **21**
  (`0ccd22ba56d025ebf88b781c`, `dbd253fd15313e1bed1a0b1e`,
  `727bc17ed78bd78febf17b19`, `af2976c3dad3df9a228ecf0a`,
  `ef6a59638e43e36e511ff0d7`, `a71a93043f26a39c86cf2538`,
  `d5d34ecad530b5db99b9de92`, `f0b6af285b236bf3bb58c9f9`,
  `f307f17d5ad2af6e9065f7ef`, `90625f6f73dbe764c16338f9`,
  `7a16c385aab2ee138baa3390`, `124774b26583295aeafe9587`,
  `1e6b922e721dff9c0fa820a0`, `eacc31a50673c91b316ab27f`,
  `1873b20c4aa4879cfc7e9a7f`, `693861565c6feaffd02cbc85`,
  `73c61c3e5e557422d2632b8c`, `783dff8cfa10b67bdfc02b1c`,
  `05e993acb6687477add18195`, `6c2e5f58f225f824951a230d`,
  `a214600d6e2345dd687439cb`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `76f063676161cca20f8cc702` | eredet `Spanyolország` → `Carinena`, `Spanyolország` |
| `0dd2d579e4c2bd203bc932a5` | márka `Ostorosbor` → `Ostoros` |
| `5e1378ea1eb520d9ad3cf6b2` | márka `Ostorosbor` → `Ostoros` |
| `55f04536b0d3994b05e273b2` | eredet `Szekszárd` → `Pannon`, `Szekszárd` |

### 069. köteg – Borok és boralapú italok, natúr ízek 1528–1552.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Silk & Spice Red Blend gyártói adatlapja 15 g/l összcukrot közöl, a
  magyar Príma-borkatalógus pedig ugyanezt a terméket kifejezetten
  félszáraz vörösborként jelöli. Ezért a téves `száraz` édességértéket
  `félszáraz` értékre javítottuk.
- Az Ostoros Cabernet Sauvignon közvetlen palackcímkéjén `OSTOROS`
  olvasható, ezért az `Ostorosbor` márkaértéket a már meglévő és
  bizonyított `Ostoros` értékre egységesítettük.
- Módosított rekord: **2**.
- Módosított tulajdonságmező: **2**.
- Változatlanul helyes rekord: **23**
  (`a153fb4f6f86b789c993f451`, `3ecf6d60b8fe0ee133c1cfc1`,
  `3e3cb79c2f21a3170b1b33ea`, `add2da8e8d3f9932d714301e`,
  `1ff9aefa7bc9ac192c55c7c8`, `94f304b12cac501e65952e32`,
  `cb4320a850966296f376ebe8`, `a49ea6cf4fceeb933688da05`,
  `1e8673b054fc9af93b554f3d`, `92c53e5046e4810950c07628`,
  `ecbaf811204c0a3d54a08717`, `2878d977532b52d1a606aba2`,
  `58c118d706c649c550284ee1`, `e496a921cd5578aab532600f`,
  `5da75218ea99fce09bc8d0ca`, `b09748e271aaed5f9a9a228b`,
  `fcf6ab8848ef822fe9fff673`, `bdd0372d5336ea0b5c52dec4`,
  `139a420677f7f56d600ee477`, `362de302158da1332f5c636b`,
  `6c5caf625287d4a2fa1fcd2d`, `bda029ec175304b251845b60`,
  `fb713590e4484613e3ca04cd`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `6ed8ca64adb736a2f860757d` | édesség `száraz` → `félszáraz` |
| `ed238f59db2922407056e730` | márka `Ostorosbor` → `Ostoros` |

### 070. köteg – Borok és boralapú italok, natúr ízek 1553–1577.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- Az Ostoros 3 literes Egri Rozé közvetlen dobozképén `OSTOROS` és
  `SZÁRAZ ROZÉBOR` olvasható. A pontos, jelenlegi 12%-os SPAR-termékadat
  szintén szárazként közli; a félszáraz 12,5%-os tétel külön
  termékváltozat. Ezért a márkát `Ostoros`, az édességet `száraz`, a
  látható kartondoboz alapján pedig a csomagolás anyagát `papír` értékre
  pontosítottuk.
- A Frittmann 3 literes Rosé Cuvée közvetlen képe szintén kartondobozos
  Bag-in-Box kiszerelést mutat, ezért az `egyéb` csomagolóanyagot
  `papír` értékre javítottuk.
- A Feind Cabernet Rosé pontos 750 ml-es termékadata 13%-os
  alkoholtartalmat közöl, ezért az `ismeretlen` értéket `13%` értékre
  pontosítottuk. A Balaton eredetet több pontos termékforrás is
  megerősíti.
- A Sauska Cabernet Franc 14,5%-os tételének villányi eredetét a
  pincészet hivatalos termékadata igazolja; a rekord változatlanul helyes.
- Módosított rekord: **3**.
- Módosított tulajdonságmező: **5**.
- Változatlanul helyes rekord: **22**
  (`2a7c01e5fb66458c18e2dafd`, `6b1082894c1192407bd08e45`,
  `e41de2b32d7e4fd160187c94`, `2bb517d07670564cebb5a661`,
  `720887c99a7c8b13990ccc4e`, `e73a49bd6ecd2a75cc7e390f`,
  `3a88ed034b1720d33f4bc4c7`, `92375a4ec33cf5cc43d9f3a7`,
  `3460e6e52729131ccc97ad5a`, `8f37360b00ab2d5e88531bf0`,
  `45220ab11dd2816c31736055`, `f9533ec0dc80ba79d7f9c81d`,
  `cba1580a8c7a103e93ccbb45`, `2914c0081fca0c90b84e5abf`,
  `faee259fddb31ceb2796b90e`, `0f6e99e55bfe3f8c7af25ed7`,
  `e98859a978108957a3dca56b`, `fc9163932fe55ddc8900607e`,
  `f7798e009e92a8defdafb9dd`, `2334093d27c949718d532e74`,
  `6a367001d89e01a85dda3c37`, `d618f1821f95c418685868b1`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `6de20cc605461f876cc842b6` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `egyéb` → `papír`; édesség `félszáraz` → `száraz` |
| `47cf35e4c917cdbd0546e384` | csomagolás anyaga `egyéb` → `papír` |
| `ce8db3f9c685fc9a5693b748` | alkoholtartalom `ismeretlen` → `13%` |

### 071. köteg – Borok és boralapú italok, natúr ízek 1578–1602.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A két Ostoros rozé közvetlen palackcímkéjén `OSTOROS` olvasható,
  ezért az `Ostorosbor` márkaértéket mindkét rekordnál a már meglévő
  `Ostoros` értékre egységesítettük.
- A Gere–Schubert Rosé Cuvée palackcímkéje és a pincészet korábban
  ellenőrzött hivatalos neve az ampersandos `Gere & Schubert`
  márkaformát igazolja.
- A Nyakas Rosé hivatalos terméklapja `OEM Etyek-Buda` kategóriát közöl,
  ezért a pontatlan `Budai` eredetet `Etyek-Buda` értékre javítottuk.
- A BB félédes Rosé Cuvée pontos termékadata `Balatonboglár` regionális
  információt közöl, ezért a tág `Dunántúl` helyett a `Balaton`,
  `Balatonboglár` eredetpárt rögzítettük.
- A három Várhegyi vörösbor pontos jelenlegi termékadata külön
  változatokat igazol: a száraz bor 11%-os Felső-Magyarországi Cuvée, a
  félédes 10,5%-os Duna–Tisza közi Kékfrankos, az édes pedig 10%-os
  Duna–Tisza közi Cuvée. Az alkoholtartalmat és az eredetet mindhárom
  rekordnál ennek megfelelően pontosítottuk.
- Az Eszterbauer Fuxli termékneve és képe sillerbort igazol. A jelenlegi
  `rozé` színértéket megtartottuk, mert a projekt öt sillerrekordjából
  négy ezt a meglévő színértéket használja; új megengedett értéket nem
  vezettünk be.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **11**.
- Változatlanul helyes rekord: **17**
  (`f9599f1013ce7c9680c56bce`, `a84f8391f8e23073bce03ab5`,
  `5368952a12da443ce70ef69d`, `31673360bb31fff8a4efe19e`,
  `ec96eb16192313adb0744512`, `3ffd7ca634bdb8cdfb3d08e1`,
  `e349ccb888854b8ac88023a7`, `7be04da03353c9a0963cd4ec`,
  `66fed9cd3a117ad90a2e7649`, `dbe281795b7f3208f940ecd8`,
  `5417fc51e1fcd0d2b19708e9`, `346ef4cb8c9e1c8dd28bd4b3`,
  `379f64814b63f55635683ec8`, `c97fdd0dd684815e77f87882`,
  `c0d512213b2075fc68c0ce36`, `5b1cf4a1d96151d98303370c`,
  `f8a6da66c777313a1d3ec16a`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `0470c685428d2680c7d9e19b` | márka `Ostorosbor` → `Ostoros` |
| `62ac613436c649b3e6f6fc47` | eredet `Budai` → `Etyek-Buda` |
| `2edac87a08a91a0da55c709d` | márka `Ostorosbor` → `Ostoros` |
| `20b0707d8912329725683c9b` | márka `Gere - Schubert` → `Gere & Schubert` |
| `48bf51952a340add6a7fd43a` | eredet `Balaton, Dunántúl` → `Balaton`, `Balatonboglár` |
| `f59d5ffda0fb3b319f49620b` | alkoholtartalom `ismeretlen` → `11%`; eredet `Magyarország` → `Felső-Magyarország` |
| `240d2c2df8736b69915570e6` | alkoholtartalom `ismeretlen` → `10,5%`; eredet `Magyarország` → `Duna-Tisza köze` |
| `0125d8abd642b67b3d233b9a` | alkoholtartalom `ismeretlen` → `10%`; eredet `Magyarország` → `Duna-Tisza köze` |

### 072. köteg – Borok és boralapú italok, natúr ízek 1603–1627.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A három Pincemester pontos jelenlegi termékadata a Cabernet Sauvignont
  11,5%-os felső-magyarországi, a félédes Kékfrankost 10,5%-os
  Duna–Tisza közi, az édes Merlot-t pedig 10,5%-os dunántúli borként
  azonosítja.
- A Várhegyi félédes rozé pontos jelenlegi termékadata 10,5%-os
  Duna–Tisza közi Cuvée változatot igazol.
- Az Angelli gyártói oldala a Bianco 14,5%-os változatát, a gyártó
  bemutatkozása pedig a márka román eredetét igazolja. Az édesség
  `egyéb` maradt, mert a pontos termékadat nem ad egyértelmű
  édességi osztályt.
- A Tesco közvetlen termékoldalai alapján pontosítottuk az Abruzzo,
  Campo de Borja, Chianti, Côtes du Rhône, Dél-Afrika,
  Montagne-Saint-Émilion, Rioja, Saint-Chinian és Tokaj eredeteket.
  A Primitivo száraz besorolását a pontos IWSC-terméklap, a Mosel
  Rieslingét a pontos brit Tesco-termékoldal, az Ebeia Ribera del
  Duero és a Rioja Reserva besorolását pedig pontos szakmai
  terméklap is megerősíti.
- A Tesco Finest Tokaji Aszú pontos neve 5 puttonyos édes fehérbort
  közöl, ezért a puttonyszámot, a színt és az eredetet is
  egyértelműsítettük.
- A `Mosel`, `Ribera del Duero`, `Saint-Chinian` és `Swartland`
  önálló, közvetlenül bizonyított boreredetek; mind a négy elemi
  értéket felvettük az eredet engedélyezett értékei közé.
- Módosított rekord: **21**.
- Módosított tulajdonságmező: **41**.
- Változatlanul helyes rekord: **4**
  (`5c5e2a5cbf99130d5a634651`, `121234743`, `121234870`,
  `121236355`).
- Új megengedett érték: **4** (`eredet: Mosel`,
  `eredet: Ribera del Duero`, `eredet: Saint-Chinian`,
  `eredet: Swartland`). Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `e8f173cacc0fefc47fd17f6f` | alkoholtartalom `ismeretlen` → `11,5%`; eredet `Magyarország` → `Felső-Magyarország` |
| `c30b85f17aaab6bd396f57bc` | alkoholtartalom `ismeretlen` → `10,5%`; eredet `Magyarország` → `Duna-Tisza köze` |
| `881b2f9bd229ccc2b2da7bcd` | alkoholtartalom `ismeretlen` → `10,5%`; eredet `Magyarország` → `Dunántúl` |
| `b2f748f50f460a45a9b39626` | alkoholtartalom `ismeretlen` → `10,5%`; eredet `Magyarország` → `Duna-Tisza köze` |
| `95d8e54da047f4bd7584d151` | eredet `egyéb` → `Románia` |
| `121234674` | eredet `egyéb` → `Campo de Borja` |
| `121279407` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Abruzzo` |
| `121279459` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Abruzzo` |
| `121236729` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Dél-Afrika` |
| `121286139` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Montagne-Saint-Émilion` |
| `121257175` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Chianti` |
| `121286145` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Saint-Chinian` |
| `121279413` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Abruzzo` |
| `121286082` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Côtes du Rhône` |
| `121286122` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Mosel` |
| `121286076` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Ribera del Duero` |
| `121234979` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Rioja` |
| `121279436` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Abruzzo` |
| `121223071` | puttonyszám `nem alkalmazható` → `5 puttonyos`; szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `121236695` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Dél-Afrika` |
| `121236706` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Swartland` |

### 073. köteg – Borok és boralapú italok, natúr ízek 1628–1652.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A három Tesco Finest bor közvetlen termékadata pontosította az
  édességet és az eredetet: a Pinot Grigio Blush száraz
  Vigneti delle Dolomiti, a Floreal száraz francia, a Bio Verdejo pedig
  száraz Rueda bor. A `Vigneti delle Dolomiti` önálló, közvetlenül
  bizonyított földrajzi eredet, ezért elemi értékként felvettük az
  eredet engedélyezett értékei közé.
- Az Ostoros Irsai Olivér és Cabernet Sauvignon közvetlen címkéjén
  `OSTOROS` olvasható; a pontos termékadat mindkettőt
  Felső-Magyarországhoz köti. Az Egri Rozé címkéje ugyanezt a
  márkaformát igazolja.
- A Feind három 5 literes borának képe csappal ellátott kartondobozt
  mutat, ezért a csomagolás anyagát `papír` értékre javítottuk. A pontos
  termékadat a Fehér Cuvée 12%-os, a Vörös Cuvée 14%-os, a Rosé Cuvée
  12,5%-os változatát igazolja; a forráskategória a fehér és a rozé
  Balaton eredetét is közli. A Feind Olaszrizlingnél csak a Balaton
  eredetet pontosítottuk, mert az alkoholtartalom nem volt egyértelműen
  bizonyítható.
- A Nyakas Irsai Olivér pontos OEM-megjelölése `Etyek-Buda`, a
  Gere–Schubert Irsai Olivér pedig villányi. A két Gere–Schubert
  közvetlen címkéje az ampersandos `Gere & Schubert` márkaformát
  igazolja.
- A Varga Zweigelt–Cabernet Sauvignon és Muskotály pontos
  termékváltozata 11%-os; a Zweigelt–Cabernet Sauvignon és a Merlot
  eredete Balaton. A Merlot, a Royal és a Tokaji Hárslevelű egymással
  ütköző évjárat- vagy változatadatainál az alkoholtartalom
  `ismeretlen` maradt.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **27**.
- Változatlanul helyes rekord: **9**
  (`121235166`, `202931070`, `121235051`, `121235949`, `120268353`,
  `121232653`, `121233560`, `120340814`, `121224295`).
- Új megengedett érték: **1**
  (`eredet: Vigneti delle Dolomiti`). Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121237279` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Vigneti delle Dolomiti` |
| `121311738` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Franciaország` |
| `121314810` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Rueda` |
| `121226528` | márka `Ostorosbor` → `Ostoros`; eredet `egyéb` → `Felső-Magyarország` |
| `120196247` | alkoholtartalom `ismeretlen` → `12%`; csomagolás anyaga `üveg` → `papír`; eredet `egyéb` → `Balaton` |
| `121235932` | eredet `Budai, Etyek-Buda` → `Etyek-Buda` |
| `121224041` | márka `Gere - Schubert` → `Gere & Schubert`; eredet `egyéb` → `Villány` |
| `121231723` | eredet `egyéb` → `Balaton` |
| `121226615` | márka `Ostorosbor` → `Ostoros` |
| `120252020` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Balaton` |
| `120170681` | eredet `egyéb` → `Balaton` |
| `121224058` | márka `Gere - Schubert` → `Gere & Schubert` |
| `120496791` | alkoholtartalom `ismeretlen` → `11%` |
| `121226275` | márka `Ostorosbor` → `Ostoros` |
| `120196230` | alkoholtartalom `ismeretlen` → `14%`; csomagolás anyaga `üveg` → `papír` |
| `120196224` | alkoholtartalom `ismeretlen` → `12,5%`; csomagolás anyaga `üveg` → `papír`; eredet `egyéb` → `Balaton` |

### 074. köteg – Borok és boralapú italok, natúr ízek 1653–1677.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Frittmann Classic Irsai Olivér pontos termékadata földrajzi jelzés
  nélküli magyar bort közöl. Ezért a termelő telephelyéből tévesen
  származtatott `Kunság` eredetet a bizonyítható `Magyarország` értékre
  javítottuk.
- A Gere–Schubert Sauvignon Blanc közvetlen címkéje a korábban is
  igazolt `Gere & Schubert` márkaformát, a Nyakas Rosé pontos
  termékadata pedig az `OEM Etyek-Buda` eredetet igazolja.
- Az Ostoros 3 literes Irsai Olivér dobozképén `OSTOROS` olvasható, a
  kiszerelés pedig csappal ellátott Bag-in-Box kartondoboz. A
  Portugieser palackcímkéje szintén az `Ostoros` márkaformát mutatja. A
  Szent István Korona 3 literes Irsai Olivér pontos termékadata és képe
  ugyancsak kartondobozos Bag-in-Box kiszerelést igazol.
- A két Hilltop Bortarisznya közvetlen képe nem kartondobozt, hanem
  fogantyús, csappal ellátott hordtasakot mutat. Három azonos
  projektbeli termékrekord is `műanyag` csomagolóanyagot használ, ezért
  mindkét téves `üveg` értéket `műanyag` értékre javítottuk.
- A Varga Szürkebarát pontos jelenlegi termékforrásai 11,5%-os
  változatot igazolnak. A Tokaji Furmint alkoholtartalma `ismeretlen`
  maradt, mert a pontos terméknévhez eltérő évjáratoknál 10,5% és 11%
  is előfordul. A Varga Óvörös Barrique pontos EAN-azonos termékadata
  12,5%-os balatoni bort igazol.
- A Feind Irsai Olivér több pontos jelenlegi termékforrásban 11%-os, a
  Feind Cabernet Rosé pedig 13%-os. A Grand Tokaj Szamorodni neve és
  pontos termékadata egyaránt fehér bort közöl.
- A Laposa Friss pontos termékadata `Badacsony`, a Tornai Somló Irsai
  Olivér pontos termékadata pedig – a terméknév ellenére – `Balaton Bor
  régió` eredetet közöl. A Petite Ville származási régiója `Bordeaux`.
  A Schieber Sauvignon Blanc `Dunántúli` földrajzi jelzésű bor; a
  palackozó szekszárdi címe nem boreredet, ezért a `Szekszárd`
  értéket eltávolítottuk a rekordból.
- Módosított rekord: **17**.
- Módosított tulajdonságmező: **19**.
- Változatlanul helyes rekord: **8**
  (`121236977`, `121236902`, `121264586`, `207661026`, `121256435`,
  `121233785`, `120340808`, `209392690`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121249599` | eredet `Kunság` → `Magyarország` |
| `121224191` | márka `Gere - Schubert` → `Gere & Schubert` |
| `121235828` | eredet `Budai` → `Etyek-Buda` |
| `220262182` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `üveg` → `papír` |
| `220157083` | csomagolás anyaga `üveg` → `papír` |
| `121226799` | márka `Ostorosbor` → `Ostoros` |
| `120496785` | alkoholtartalom `ismeretlen` → `11,5%` |
| `120194998` | csomagolás anyaga `üveg` → `műanyag` |
| `121231717` | alkoholtartalom `ismeretlen` → `11%` |
| `121235886` | szín `egyéb` → `fehér` |
| `120031086` | csomagolás anyaga `üveg` → `műanyag` |
| `121237089` | eredet `Balaton` → `Badacsony` |
| `121256319` | eredet `egyéb` → `Balaton` |
| `121232325` | alkoholtartalom `ismeretlen` → `13%` |
| `121237193` | eredet `egyéb` → `Bordeaux` |
| `120268324` | alkoholtartalom `ismeretlen` → `12,5%`; eredet `egyéb` → `Balaton` |
| `121259351` | eredet `Dunántúl, Szekszárd` → `Dunántúl` |

### 075. köteg – Borok és boralapú italok, natúr ízek 1678–1702.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Nyakas Budai Sauvignon Blanc közvetlen termékadata `OEM Etyek-Buda`
  eredetet közöl. A `Budai` terméknévelem nem külön eredet, ezért a rekordból
  eltávolítottuk a redundáns `Budai` értéket.
- Az öt Ostoros-bor közvetlen címkéjén `OSTOROS` olvasható, ezért a
  terméknévből átvett `Ostorosbor` cégnevet az igazolt `Ostoros`
  márkaformára javítottuk. A Medina pontos termékadata
  `Felső-Magyarországi` eredetet közöl. A 3 literes Olaszrizling képe és
  közvetlen termékadata Bag-in-Box kartondobozos kiszerelést igazol, ezért
  a téves `üveg` csomagolóanyagot `papír` értékre javítottuk.
- A Fantasy Cabernet Sauvignon pontos termékadata „Bor Moldovából”
  származást és Moldova országot közöl. A `Moldova` önálló, elemi
  országértéket felvettük az eredet megengedett értékei közé.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **18**
  (`210886782`, `121249605`, `121237509`, `207256499`, `210527968`,
  `120815806`, `121124188`, `121257226`, `121224087`, `121235955`,
  `121285250`, `121249616`, `121233531`, `121232682`, `121260965`,
  `120684729`, `121235546`, `121235581`).
- Új megengedett érték: **1** (`eredet: Moldova`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121235961` | eredet `Budai, Etyek-Buda` → `Etyek-Buda` |
| `121226678` | márka `Ostorosbor` → `Ostoros` |
| `121226540` | márka `Ostorosbor` → `Ostoros` |
| `121226534` | márka `Ostorosbor` → `Ostoros` |
| `121236960` | eredet `egyéb` → `Moldova` |
| `121226563` | márka `Ostorosbor` → `Ostoros`; eredet `egyéb` → `Felső-Magyarország` |
| `220221735` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `üveg` → `papír` |

### 076. köteg – Borok és boralapú italok, natúr ízek 1703–1727.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Font Irsai Olivér és az Ostoros Egri Rozé közvetlen képe, valamint
  pontos termékadata Bag-in-Box kartondobozos kiszerelést igazol. Az
  Ostoros dobozán az `OSTOROS` márkaforma olvasható. A Varga 3 literes
  Zweigelt–Cabernet Sauvignon képe ezzel szemben merev műanyag kannát
  mutat.
- A Fantasy Chardonnay pontos termékadata félédes, 12,5%-os moldovai
  fehérbort igazol. A `Moldova` értéket az előző kötegben már felvettük,
  ezért itt újabb értékmódosításra nem volt szükség.
- A Varga Édes Bubis a termelő nyilatkozata szerint 3 g/l
  szén-dioxidot tartalmaz, ugyanakkor hivatalosan csendes bor
  kategóriájú. Emiatt nem soroltuk át gyöngyözőbornak, hanem a borágban
  maradt, és a téves `szénsavmentes` értéket `szénsavas` értékre
  javítottuk. Az alkoholtartalom továbbra is `ismeretlen`, mert a pontos
  jelenlegi termékadat nem közöl százalékot.
- A Tokaji Szamorodni pontos termékadata édes fehérbort, a Tokajicum
  Sárgamuskotály pedig édes fehér, tokaji bort igazol. A Sauska Cuvée 13
  pontos származási régiója `Villány`.
- A Viña Albali Rosado Tempranillo pontos gyártói terméklapja D.O.
  Valdepeñas eredetet, az EAN-azonos pontos termékforrások pedig száraz
  stílust igazolnak. A `Valdepeñas` önálló, elemi eredetértéket felvettük
  a megengedett értékek közé.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **13**.
- Változatlanul helyes rekord: **16**
  (`121233583`, `121236833`, `121235425`, `120816005`, `121236085`,
  `121236009`, `121222233`, `121285313`, `121235673`, `121236954`,
  `121235172`, `220324563`, `121255401`, `121235454`, `121224335`,
  `121224686`).
- Új megengedett érték: **1** (`eredet: Valdepeñas`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `120495072` | csomagolás anyaga `üveg` → `papír` |
| `220009024` | márka `Ostorosbor` → `Ostoros`; csomagolás anyaga `üveg` → `papír` |
| `121236983` | édesség `egyéb` → `félédes`; eredet `egyéb` → `Moldova` |
| `120304461` | szénsavasság `szénsavmentes` → `szénsavas` |
| `220162008` | csomagolás anyaga `üveg` → `műanyag` |
| `121236465` | szín `egyéb` → `fehér` |
| `121224185` | eredet `egyéb` → `Villány` |
| `121235696` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `121235137` | édesség `egyéb` → `száraz`; eredet `egyéb` → `Valdepeñas` |

### 077. köteg – Borok és boralapú italok, natúr ízek 1728–1752.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Bostavan Gold Premium Merlot és a Fantasy Muscat Rose pontos Tesco-
  termékadata egyaránt moldovai származást közöl. A `Moldova` értéket a
  075. kötegben már felvettük, ezért itt nem kellett új megengedett értéket
  hozzáadni.
- A három Ostoros-bor közvetlen címkéje és termékadata az `Ostoros`
  márkaformát igazolja. A Dankó Rozé Cuvée termékneve és pontos termékadata
  egyaránt `Felső-Magyarországi` eredetet közöl.
- A Royal Tokaji Furmint a Tesco száraz fehérbor-kategóriájában szerepel, és
  a termelő pontos 13%-os Furmint-tételei is száraz borok. A Tokajicum 5
  puttonyos Aszú pontos termékadata a bor színét `Fehér` értékkel közli.
- A BB és a Teleki 3 literes termékképe kartondobozos Bag-in-Box
  kiszerelést mutat. A Teleki termelői terméklapja a 3 literes változatra is
  14,5%-os alkoholtartalmat közöl. A Feind és a Varga közvetlen képe ezzel
  szemben fogantyús, csappal ellátott borzsákot mutat; a Varga leírása
  kifejezetten zsákként nevezi meg a belső csomagolást.
- A Feind 3 literes Cabernet Rosé eredetét a projekt forráskategóriája és a
  pontos termékforrások balatoni/balatonmelléki borként igazolják. Az
  alkoholtartalma `ismeretlen` maradt, mert a jelenlegi pontos források 13%
  és 13,5% értéket is közölnek. A Varga Csendes Rozé pontos Tesco-
  termékadata `Balatoni` regionális információt ad, ezért a redundáns
  `Dunántúl` értéket eltávolítottuk.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **15**.
- Változatlanul helyes rekord: **13**
  (`121235045`, `121235483`, `121224110`, `121260953`, `121236885`,
  `121232722`, `208817194`, `121266503`, `121249858`, `121233105`,
  `121236038`, `121237008`, `121256141`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121237383` | eredet `egyéb` → `Moldova` |
| `121226632` | márka `Ostorosbor` → `Ostoros` |
| `121236931` | eredet `egyéb` → `Moldova` |
| `121227182` | márka `Ostorosbor` → `Ostoros` |
| `120148265` | eredet `egyéb` → `Felső-Magyarország` |
| `220321102` | édesség `egyéb` → `száraz` |
| `220262409` | csomagolás anyaga `üveg` → `papír` |
| `120675873` | csomagolás anyaga `üveg` → `műanyag`; eredet `egyéb` → `Balaton` |
| `220021204` | alkoholtartalom `ismeretlen` → `14,5%`; csomagolás anyaga `üveg` → `papír` |
| `121226684` | márka `Ostorosbor` → `Ostoros` |
| `220162007` | csomagolás anyaga `üveg` → `műanyag`; eredet `Balaton, Dunántúl` → `Balaton` |
| `121235765` | szín `egyéb` → `fehér` |

### 078. köteg – Borok és boralapú italok, natúr ízek 1753–1777.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Feind Cabernet Sauvignon pontos, azonos FHA-kódú termékadata 13,5%-os
  dunántúli bort igazol. A Varga Aranymetszés Friss Irsai Olivér pontos
  jelenlegi termékforrásai és a 2026-os balatoni borverseny eredménylistája
  egyaránt száraz borként közlik a tételt.
- A Royal Tokaji 5 puttonyos Aszú neve és pontos Tesco-termékadata fehér bort
  közöl. Az Etyeki Kúria White pontos termékadata kizárólag `Etyek-Buda`
  regionális információt ad, ezért a redundáns `Etyek` értéket
  eltávolítottuk.
- A Szent István Korona 3 literes Rosé Cuvée közvetlen képe kartondobozos
  Bag-in-Box kiszerelést mutat. A Feind 3 literes Olaszrizling képe ezzel
  szemben fogantyús, csappal ellátott borzsák; a pontos termékforrás
  kifejezetten borzsákként nevezi meg, és 13%-os alkoholtartalmat közöl. A
  projekt forráskategóriája és a pontos termelői információk balatoni
  eredetet támasztanak alá.
- A Night Orient Rosé Tempranillo közvetlen képe üvegpalackot mutat, a pontos
  Tesco-termékadata pedig Belgiumot adja meg származási helyként és
  országként. A `Belgium` elemi országértéket felvettük az eredet
  megengedett értékei közé. Az édesség `egyéb` maradt, mert a pontos
  források nem adnak egyértelmű szárazsági fokot.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **11**.
- Változatlanul helyes rekord: **18**
  (`121233393`, `121265781`, `121223134`, `121249945`, `121236891`,
  `121235915`, `121235431`, `121231406`, `121236401`, `121265821`,
  `121269402`, `121235794`, `121222227`, `121236948`, `121259282`,
  `220332190`, `121278466`, `121235108`).
- Új megengedett érték: **1** (`eredet: Belgium`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121232296` | alkoholtartalom `ismeretlen` → `13,5%`; eredet `egyéb` → `Dunántúl` |
| `121231389` | édesség `egyéb` → `száraz` |
| `206281539` | szín `egyéb` → `fehér` |
| `220157084` | csomagolás anyaga `üveg` → `papír` |
| `121253829` | eredet `Etyek, Etyek-Buda` → `Etyek-Buda` |
| `121277070` | csomagolás anyaga `egyéb` → `üveg`; eredet `egyéb` → `Belgium` |
| `120675850` | alkoholtartalom `ismeretlen` → `13%`; csomagolás anyaga `üveg` → `műanyag`; eredet `egyéb` → `Balaton` |

### 079. köteg – Borok és boralapú italok, natúr ízek 1778–1802.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Bostavan Gold Premium Cabernet Sauvignon pontos Tesco-termékadata
  moldovai származást közöl. A Tokajicum 6 puttonyos Aszú neve, pontos
  termékadata és közvetlen címkéje együttesen a `6 puttonyos`, `fehér` és
  `Tokaj` értékeket igazolja. A Grand Tokaj 5 puttonyos Aszú pontos
  termékadata szintén fehér bort közöl.
- Az Ikon Cabernet Sauvignon pontos Tesco-termékadata `Balatonboglár`, a
  Figula Rosé pontos termékadata pedig `Balatonfüred-Csopak` regionális
  információt ad. Ezeket a korábbi pontatlan `egyéb` eredetek helyett
  rögzítettük.
- Az Ostoros Muskotály közvetlen címkéje az `Ostoros` márkaformát mutatja.
  A Günzer Rosé termékneve és címkéje `Günzer`, nem `Günzer Tamás`
  márkanevet közöl. A `Günzer` értéket külön felvettük; a `Günzer Tamás`
  megmaradt a név szerint Günzer Tamás-termékekhez.
- Az Aperitivo Bianco neve ízesített boralapú italt közöl, pontos
  Tesco-termékadatában pedig 86% almabor, gyógynövénykivonat és aroma
  szerepel. Ez igazolja a `fűszeres` ízt és az `ízesített boralapú ital`
  bortípust. Ugyanez a forrás Szlovákiát adja meg származási országként,
  ezért a `Szlovákia` elemi országértéket felvettük az eredet megengedett
  értékei közé. A szín és az édesség bizonyíték hiányában `egyéb` maradt.
- A Bodri QV Szekszárdi Civilis Cuvée projektbeli forráskategóriája és a
  pontos termékforrások egyaránt száraz vörösborként közlik a tételt.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **13**.
- Változatlanul helyes rekord: **16**
  (`121255995`, `121237072`, `121235926`, `121222953`, `121235448`,
  `121235609`, `121233595`, `121255983`, `121236349`, `121224277`,
  `121224421`, `121257290`, `121236925`, `121236096`, `121255948`,
  `121222688`).
- Új megengedett érték: **2** (`eredet: Szlovákia`; `márka: Günzer`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121237395` | eredet `egyéb` → `Moldova` |
| `121235725` | puttonyszám `nem alkalmazható` → `6 puttonyos`; szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `121224352` | eredet `egyéb` → `Balatonboglár` |
| `121226937` | márka `Ostorosbor` → `Ostoros` |
| `121235644` | szín `egyéb` → `fehér` |
| `121224628` | eredet `egyéb` → `Balatonfüred-Csopak` |
| `121224248` | márka `Günzer Tamás` → `Günzer` |
| `121257042` | íz `natúr` → `fűszeres`; eredet `egyéb` → `Szlovákia`; bortípus `boralapú ital` → `ízesített boralapú ital` |
| `121249933` | édesség `egyéb` → `száraz` |

### 080. köteg – Borok és boralapú italok, natúr ízek 1803–1827.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Szent Gaál Twist Irsai Olivér pontos Tesco-termékadata `Pannon`
  regionális információt ad. Az Ostoros Csipke közvetlen címkéje az
  `Ostoros` márkaformát igazolja. A kislaki és a Katona termékének pontos
  neve egyaránt `Balatonboglár` eredetet közöl, ezért a mellette szereplő
  tágabb, redundáns `Balaton` értéket eltávolítottuk.
- A Teleki, a két Chill és a Font 3 literes termék közvetlen képe
  kartondobozos Bag-in-Box kiszerelést mutat; a pontos termékadatok is
  dobozként, csappal használható Bag-in-Boxként írják le őket. A Teleki
  termelői terméklapja ugyanazon termék 0,375, 0,75 és 3 literes
  kiszerelése mellett 11,5%-os alkoholtartalmat közöl.
- A Sauska Rosé és Cabernet Sauvignon pontos Tesco-termékadata egyaránt
  `Villány` regionális információt ad. A Sauska Siller közvetlen képe
  üvegpalackot, pontos termékadata pedig villányi eredetet igazol. A Siller
  alkoholtartalmát nem módosítottuk: ugyanazon Tesco-oldal címe 12,5%-ot,
  részletes adatmezője 12%-ot közöl.
- A Gere–Schubert két közvetlen címkéje és a korábban ellenőrzött hivatalos
  márkanév a `Gere & Schubert` alakot igazolja. A Syrah-Merlot pontos
  Tesco-termékadata `Villány` regionális információt ad.
- A St. Andrea Áldás pontos termékleírása Egri Bikavérként nevezi meg a
  bort, és `Eger` régiót közöl. A Takler Merlot pontos termékadata
  `Szekszárd`, a Figula Zenit and More pontos termékadata pedig
  `Balatonfüred-Csopak` regionális információt ad.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **19**.
- Változatlanul helyes rekord: **9**
  (`121235650`, `120968815`, `121235713`, `121268081`, `121230615`,
  `121224145`, `121224225`, `121224283`, `121224317`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121256170` | eredet `egyéb` → `Pannon` |
| `121226655` | márka `Ostorosbor` → `Ostoros` |
| `121220495` | eredet `Balaton, Balatonboglár` → `Balatonboglár` |
| `105111370` | alkoholtartalom `ismeretlen` → `11,5%`; csomagolás anyaga `üveg` → `papír` |
| `105540993` | csomagolás anyaga `üveg` → `papír` |
| `105541000` | csomagolás anyaga `üveg` → `papír` |
| `120495089` | csomagolás anyaga `üveg` → `papír` |
| `121224070` | eredet `egyéb` → `Villány` |
| `121224254` | eredet `egyéb` → `Villány` |
| `121224323` | csomagolás anyaga `egyéb` → `üveg`; eredet `egyéb` → `Villány` |
| `121224375` | márka `Gere - Schubert` → `Gere & Schubert`; eredet `egyéb` → `Villány` |
| `121224398` | eredet `Balaton, Balatonboglár` → `Balatonboglár` |
| `121224409` | eredet `egyéb` → `Eger` |
| `121224415` | eredet `egyéb` → `Szekszárd` |
| `121224485` | márka `Gere - Schubert` → `Gere & Schubert` |
| `121224525` | eredet `egyéb` → `Balatonfüred-Csopak` |

### 081. köteg – Borok és boralapú italok, natúr ízek 1828–1852.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **24**.
- A Wairau Cove helyi képfájl csak „Image unavailable” helyőrzőt
  tartalmazott; ennél a rekordnál a pontos Tesco-termékoldal adatait
  használtuk.
- A Sauska Cuvée 11 pontos Tesco-termékadata `Villány`, a Gilvesy Bohém
  Cuvée pontos termékadata pedig `Badacsonyi borvidék` regionális
  információt közöl. A Gilvesy alkoholtartalmát nem módosítottuk: a
  felülvizsgált forrásrekord és név 12,5%-ot, a jelenlegi termékoldal 12%-ot
  ad meg.
- Az Ostoros Debrői Hárslevelű közvetlen címkéje az `Ostoros` márkaformát
  mutatja. A Duna-Tisza közi Muskotály közvetlen képe csavarzáras,
  áttetsző PET-palackot igazol, ezért a csomagolás anyaga `műanyag`.
- A Feind Zenit pontos termelői terméklapja 12%-os félédes fehérbort
  közöl. A projekt forráskategóriája, a termelő balatoni megjelölése és a
  balatonfőkajári termelői cím együttesen `Balaton` eredetet támaszt alá.
- A Wairau Cove pontos Tesco-oldala Marlborough Sauvignon
  Blanc-ként azonosítja a terméket; a független boradatlap ugyanezt a
  márkát és száraz stílust igazolja. A `Wairau Cove` elemi márkaértéket
  felvettük. Az alkoholtartalom 12,5% maradt: ez egyezik a felülvizsgált
  forrásrekorddal és a hozzá illő korábbi évjárat szakmai adatával, míg a
  jelenlegi Tesco-oldal már egy 12%-os évjáratot mutat.
- A Bock Cserszegi Fűszeres eredete `egyéb` maradt: a pontos termékadat
  kifejezetten földrajzi jelzés nélküli borként közli, ezért a villányi
  termelői cím nem használható a bor eredeteként.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **8**.
- Változatlanul helyes rekord: **19**
  (`121228273`, `121228307`, `121228457`, `121230626`, `121233364`,
  `121233410`, `121233456`, `121233738`, `121234680`, `121234697`,
  `121234841`, `121234904`, `121234933`, `121234985`, `121235068`,
  `121235080`, `121235120`, `121235552`, `121235569`).
- Új megengedett érték: **1** (`márka: Wairau Cove`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121224675` | eredet `egyéb` → `Villány` |
| `121224732` | eredet `egyéb` → `Badacsony` |
| `121226753` | márka `Ostorosbor` → `Ostoros` |
| `121228169` | csomagolás anyaga `üveg` → `műanyag` |
| `121232123` | alkoholtartalom `ismeretlen` → `12%`; eredet `egyéb` → `Balaton` |
| `121234668` | márka `márka nélkül` → `Wairau Cove`; édesség `egyéb` → `száraz` |

### 082. köteg – Borok és boralapú italok, natúr ízek 1853–1877.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **24**.
- A Firemark Malbec helyi képfájlja csak „Image unavailable” helyőrzőt
  tartalmazott; ennél a rekordnál a pontos Tesco-termékoldal képeit és
  termékadatait használtuk.
- A négy Gere Tamás & Zsolt tétel projektbeli forráskategóriája száraz bort
  közöl. A Hárslevelű, a Kékfrankos és a Cabernet Sauvignon pontos
  termékforrásai, valamint a Páratlan hivatalos termelői terméklapja ezt
  külön is megerősíti, ezért a korábbi `egyéb` édességet `száraz` értékre
  javítottuk.
- A Hattyús pontos forrásrekordja az édes fehérborok közé sorolja a terméket,
  a Tesco-termékoldal pedig tokaji késői szüretelésű Furmintként azonosítja;
  az édesség ezért `édes`.
- A Ruby Port forrásrekordja `TESCO` márkát és portugál kategóriát közöl. A
  pontos Tesco-termékoldal Portugáliát, 10,3 g/100 ml cukrot és 18%-os
  likőrbort ad meg, a közvetlen kép és a szakmai terméklap pedig
  üvegpalackos Tesco Ruby Portként azonosítja. Ez a `Tesco`, `üveg`, `édes`
  és `Portugália` értékeket igazolja.
- A Firemark Malbec édessége `egyéb` maradt. A pontos termékoldal 0,5 g/100
  ml cukrot közöl, de savadatot és kifejezett szárazsági fokot nem; ezért a
  száraz és félszáraz jogi határ találgatás nélkül nem dönthető el.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **19**
  (`121235598`, `121235685`, `121235707`, `121235736`, `121237055`,
  `121249622`, `121249639`, `121249645`, `121249841`, `121249893`,
  `121255574`, `121256129`, `121256164`, `121257111`, `121257186`,
  `121259299`, `121259316`, `121265798`, `121265815`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121235667` | édesség `egyéb` → `száraz` |
| `121235742` | édesség `egyéb` → `száraz` |
| `121235759` | édesség `egyéb` → `száraz` |
| `121235771` | édesség `egyéb` → `száraz` |
| `121236787` | édesség `egyéb` → `édes` |
| `121237596` | márka `márka nélkül` → `Tesco`; csomagolás anyaga `egyéb` → `üveg`; édesség `egyéb` → `édes`; eredet `egyéb` → `Portugália` |

### 083. köteg – Borok és boralapú italok, natúr ízek 1878–1902.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen kép: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Szepsy Furmint pontos Tesco-termékadata Mád, Tállya és Tarcal szőlőiből
  készült birtokborként írja le a terméket, regionális információként pedig
  Tokaj-Hegyalját közöl; ezt a kategóriafa meglévő `Tokaj` értékével
  rögzítettük.
- A Gere Merlot pontos Tesco-termékadata `Villány` regionális információt
  ad. A Piknik Chardonnay pontos termékleírása `DTK` oltalom alatt álló
  földrajzi jelzést közöl; a hivatalos termékleírás ezt Duna-Tisza közi
  OFJ-ként azonosítja, ezért az eredet a meglévő `Duna-Tisza köze` érték.
- A Várszegi Rosé pontos neve és termékadata kizárólag a balatonboglári
  eredetmegjelölést közli, ezért a mellette szereplő tágabb, redundáns
  `Balaton` értéket eltávolítottuk.
- A márkanév nélkül forgalmazott Tokaji Szamorodni pontos termékoldala
  fehér színt és `Tokaj` régiót közöl. A termelői adat az Ungvár-Pincét
  gyártóként, nem külön termékmárkaként adja meg, ezért a `márka nélkül`
  értéket megtartottuk.
- A Royal Hugo neve, közvetlen címkéje és pontos termékleírása egyaránt
  mojito ízű, szénsavas, ízesített boralapú koktélt igazol; ugyanaz a
  termékoldal magyar származást közöl. A `mojito` elemi ízértéket
  felvettük.
- A Haraszthy Pinot Noir Rosé alkoholtartalma `ismeretlen` maradt: sem a
  felülvizsgált terméknév és címke, sem a pontos termékoldal nem közöl
  alkoholszázalékot.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **8**.
- Változatlanul helyes rekord: **19**
  (`121265873`, `121265885`, `121266325`, `121266388`, `121266561`,
  `121267001`, `121267018`, `121268121`, `121287524`, `121287576`,
  `121287599`, `121287956`, `121287962`, `121287979`, `121288005`,
  `121289390`, `121303748`, `121306083`, `121306095`).
- Új megengedett érték: **1** (`íz: mojito`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121266244` | eredet `egyéb` → `Tokaj` |
| `121266267` | eredet `egyéb` → `Villány` |
| `121287565` | eredet `egyéb` → `Duna-Tisza köze` |
| `121300377` | eredet `Balaton, Balatonboglár` → `Balatonboglár` |
| `121306457` | szín `egyéb` → `fehér`; eredet `egyéb` → `Tokaj` |
| `121306722` | íz `natúr` → `mojito`; eredet `egyéb` → `Magyarország` |

### 084. köteg – Borok és boralapú italok, natúr ízek 1903–1927.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **23**.
- A két Taparoo Valley helyi képfájlja csak „Image unavailable” helyőrzőt
  tartalmazott; ezeknél a pontos Tesco-termékoldalak képeit és termékadatait
  használtuk. Mindkét oldal ausztrál eredetű borként azonosítja a terméket.
  Az édességük `egyéb` maradt: a Chardonnay 0,5 g/100 ml cukoradata savadat
  nélkül nem dönti el a száraz és félszáraz jogi határt, a Shiraz oldala
  pedig nem közöl szárazsági fokot.
- A Nyakas Don Olivér pontos Tesco-termékadata `OEM Etyek-Buda` regionális
  információt ad, ezért az eredet a kategóriafa meglévő `Etyek-Buda`
  értéke.
- A Spritzi pontos termékleírása vörös narancs ízű, szénsavas, ízesített
  boralapú italt, az adatlap pedig 8,4%-os alkoholtartalmat közöl. Az ízt a
  meglévő elemi `narancs` értékkel rögzítettük; a bortípust
  `ízesített boralapú ital` értékre pontosítottuk. A szín és az édesség
  `egyéb` maradt, mert a termékoldal egyiket sem nevezi meg.
- A La Fiesta vörösbor pontos termékadata megerősíti a már rögzített
  `Felső-Magyarország` eredetet. A rosé pontos leírása és regionális
  információja viszont `Duna-Tisza közi`, ezért annak korábbi `egyéb`
  eredetét `Duna-Tisza köze` értékre javítottuk.
- A BB Muskotály, Rosé Cuvée, Olaszrizling és Irsai Olivér pontos
  termékadata egyaránt Balatonboglár/Balatonboglári régiót közöl. Az egzakt
  `Balatonboglár` értéket tartottuk meg, a mellette szereplő tágabb vagy
  téves `Balaton`, illetve `Dunántúl` értéket eltávolítottuk.
- A Konyári Sauvignon Blanc pontos Tesco-termékadata `Balatonboglár`
  regionális információt közöl.
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **13**.
- Változatlanul helyes rekord: **15**
  (`121307491`, `121310405`, `121316629`, `121316635`, `121319528`,
  `121319586`, `121320376`, `121320405`, `121322921`, `121322973`,
  `121322985`, `121324055`, `121324101`, `121324153`, `121324631`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121309229` | eredet `egyéb` → `Ausztrália` |
| `121309264` | eredet `egyéb` → `Ausztrália` |
| `121315982` | eredet `egyéb` → `Etyek-Buda` |
| `121318627` | alkoholtartalom `ismeretlen` → `8,4%`; íz `natúr` → `narancs`; szénsavasság `szénsavmentes` → `szénsavas`; bortípus `boralapú ital` → `ízesített boralapú ital` |
| `121322967` | eredet `egyéb` → `Duna-Tisza köze` |
| `121324090` | eredet `Balaton, Balatonboglár` → `Balatonboglár` |
| `121324147` | eredet `Balaton, Dunántúl` → `Balatonboglár` |
| `121324165` | eredet `Balaton, Balatonboglár` → `Balatonboglár` |
| `121324176` | eredet `Balaton, Balatonboglár` → `Balatonboglár` |
| `121326807` | eredet `egyéb` → `Balatonboglár` |

### 085. köteg – Borok és boralapú italok, natúr ízek 1928–1952.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **23**.
- A két Sauska Tokaj rekord helyi képfájlja tévesen egy-egy Balassa
  Sárgamuskotályt, illetve Chardonnay-t ábrázol. A teljes forrásrekord és a
  két pontos Tesco-termékoldal egyaránt a Sauska terméknevet, a megfelelő
  szőlőfajtát, alkoholtartalmat és Tokaj-Hegyalja régiót közli, ezért a
  besorolást a hibás helyi kép alapján nem módosítottuk.
- A BB Chardonnay és Tramini pontos Tesco-termékadata Balatonboglár,
  illetve Balatonboglári borvidék regionális információt ad. A Chardonnay
  redundáns `Balaton` értékét eltávolítottuk, a Tramini tágabb `Dunántúl`
  eredetét pedig `Balatonboglár` értékre pontosítottuk.
- A Tornai Orange Zeus neve és közvetlen képe narancsbor-jelleget és
  borostyánszínű bort mutat; ezt a fa meglévő `borostyán` színértékével
  rögzítettük. A pontos Tesco szárazfehérbor-polc és a felülvizsgált
  forráskategória egyaránt szárazként sorolja, ezért az édesség `száraz`.
- Az öt Casa Maña pontos Tesco-termékoldala egyaránt
  `Spanyolországból származó bor` megjelölést és Spanyolország országot
  közöl.
- A Vineyards Sangria pontos termékadata spanyol, vörösboralapú sangriát
  igazol. Az összetevők citrusfélék és fahéj aromáját, a tápértékadat
  8,5 g/100 ml cukrot közöl; ezért az íz `fűszeres`, a szín `vörös`, az
  édesség `édes`, az eredet `Spanyolország`, a bortípus pedig `sangria`.
  Nem vettünk fel általános citrus ízértéket, mert a forrás nem nevez meg
  egyetlen konkrét citrusfélét sem.
- A Dino Primitivo pontos termékadata `Puglia` regionális információt ad.
  A Dino Trebbiano Pinot Grigio `Abruzzo` eredete változatlanul helyes. Az
  édessége `egyéb` maradt: a 0,4 g/100 ml cukoradat savadat és kifejezett
  szárazsági fok nélkül nem dönti el a száraz és félszáraz jogi határt.
- A Vineyards 2 literes fehér Cuvée pontos neve és termékadata
  Duna-Tisza közi eredetet igazol, a közvetlen képen pedig egyértelműen
  műanyag palack látható.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **16**.
- Változatlanul helyes rekord: **14**
  (`121328189`, `121328212`, `121328517`, `121328552`, `121328569`,
  `121328609`, `121330859`, `121330865`, `121330871`, `121330888`,
  `121330894`, `121333545`, `121339487`, `121339493`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121328535` | eredet `Balaton, Balatonboglár` → `Balatonboglár` |
| `121328546` | eredet `Dunántúl` → `Balatonboglár` |
| `121329349` | szín `fehér` → `borostyán`; édesség `egyéb` → `száraz` |
| `121333292` | eredet `egyéb` → `Spanyolország` |
| `121333355` | eredet `egyéb` → `Spanyolország` |
| `121333476` | íz `natúr` → `fűszeres`; szín `egyéb` → `vörös`; édesség `egyéb` → `édes`; eredet `egyéb` → `Spanyolország`; bortípus `boralapú ital` → `sangria` |
| `121333482` | eredet `egyéb` → `Spanyolország` |
| `121333499` | eredet `egyéb` → `Spanyolország` |
| `121333539` | eredet `egyéb` → `Puglia` |
| `121333580` | eredet `egyéb` → `Spanyolország` |
| `121341103` | csomagolás anyaga `üveg` → `műanyag` |

### 086. köteg – Borok és boralapú italok, natúr ízek 1953–1971.

- Ellenőrzött rekord: **19**.
- Helyben elérhető és megvizsgált képfájl: **19**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **19**.
- A két Vineyards 2 literes palack közvetlen képe egyértelműen műanyag
  csomagolást mutat. A Rosado jelenlegi Tesco-oldala már `Dunántúli`
  termékváltozatot ír le, miközben a felülvizsgált forrásrekord neve és
  teljes adata `Duna-Tisza közi`; ezt termékadat-változásnak tekintettük,
  ezért az eredetet nem írtuk át. A Tinto pontos oldala továbbra is
  Duna-Tisza közi eredetet közöl.
- A Figula Sauvignon Blanc pontos Tesco-termékadata
  `Balatonfüred-Csopak`, a Sauska Syrah oldala `Villány`, a Vida Péter
  Tündérrózsa oldala pedig `Szekszárd` regionális információt ad.
- A Royal Tokaji Sárga Muskotály pontos termelői adatlapja 7,5 g/l
  maradékcukrot és 7,8 g/l savtartalmat közöl; a termelő ugyanazt a
  12,5%-os tételt száraz Sárgamuskotályként azonosítja. Ezért az édesség
  `száraz`.
- Az Ostorosbor, a Teleki és a Frittmann 3 literes termékeinek közvetlen
  képe kartondobozos Bag-in-Box kiszerelést mutat, ezért a csomagolás
  anyaga a meglévő `papír` érték. Az Ostorosbor jelenlegi termékoldala
  13%-ot közöl, de a felülvizsgált forrásrekord neve 12,5%-os terméket
  azonosít; a forrásrekord szerinti 12,5%-ot megtartottuk.
- A Teleki gyártói termékoldala a 3 literes kiszerelést és 12,5%-os
  alkoholtartalmat ugyanazon Villányi Rosé Cuvée termékhez közli, ezért az
  `ismeretlen` értéket `12,5%`-ra javítottuk. A pontos Tesco-oldal a száraz
  rosébort, a 3 literes kiszerelést és a villányi eredetet is megerősíti.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **10**.
- Változatlanul helyes rekord: **10**
  (`121356558`, `121357649`, `121360299`, `121361972`, `121363371`,
  `121249910`, `121316802`, `121356645`, `121357684`, `121359486`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121341115` | csomagolás anyaga `üveg` → `műanyag` |
| `121341132` | csomagolás anyaga `üveg` → `műanyag` |
| `121348378` | eredet `egyéb` → `Balatonfüred-Csopak` |
| `121349210` | édesség `egyéb` → `száraz` |
| `121356512` | eredet `egyéb` → `Villány` |
| `121361753` | eredet `egyéb` → `Szekszárd` |
| `220001469` | csomagolás anyaga `üveg` → `papír` |
| `220266310` | alkoholtartalom `ismeretlen` → `12,5%`; csomagolás anyaga `üveg` → `papír` |
| `120676820` | csomagolás anyaga `üveg` → `papír` |

### 087. köteg – Bor és boralapú ital, azonosítólistából hiányzó Bikavérek.

- Ellenőrzött rekord: **5**.
- Helyben elérhető és megvizsgált képfájl: **5**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **5**.
- Az öt rekord az eddigi tételes azonosítólistákból hiányzott, ezért külön
  kézi ellenőrzést kapott. Az Ostorosbor, a Schieber Trilógia, a Grand
  Nobilia Superior, a Thummerer Classicus és a Pincemester palackképe,
  forrásneve és teljes jelenlegi besorolása egymással összhangban van.
- Mind az öt termék hagyományos, száraz vörös Bikavér; a leírásokban
  szereplő gyümölcsös és fűszeres kóstolójegyek nem termékízesítések, ezért
  az íz helyesen `natúr`.
- A Pincemester alkoholtartalma `ismeretlen` maradt: a forrásnév, a
  közvetlen palackkép és a pontos SPAR-termékanyag sem közöl
  alkoholszázalékot. A forrásban szereplő rosé-polc téves, de a terméknév
  és a kép egyértelműen Egri Bikavér száraz vörösbort igazol; a jelenlegi
  besorolás ezt már helyesen tartalmazza.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul helyes rekord: **5**
  (`b99bf52636b6ddea5c1360be`, `0391157dbd5fbd9ae76f7fb2`,
  `fa875b03c2ad42c769816251`, `7f83b16b275fbc8d7f55f8be`,
  `46a2affb1de28ff60a645daa`).
- Új megengedett érték: **0**. Törölt megengedett érték: **0**.

### 088. köteg – Pezsgő, habzóbor és gyöngyözőbor 1–25.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **24**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **24**.
- Helyi kép nélkül: **1** (`4604640`). A Balaton Bollicine Olivier
  rekordnál csak a névvel és a teljes forrásadattal bizonyítható értékeket
  tartottuk meg; az alkoholtartalom és a szín ezért `ismeretlen`, illetve
  `egyéb` maradt.
- A Vino Frizzante Secco közvetlen címkéje az olasz terméket mutatja, a
  pontos ALDI-termékadat pedig 10,5%-os alkoholtartalmat, olasz eredetet,
  fehér szőlőt és szalmasárga bort közöl. A szín ezért a meglévő `fehér`
  érték.
- A Stolzenfels pontos ALDI-termékadata 11%-os, Németországból származó
  száraz fehér pezsgőt igazol.
- A Kreinbacher Extra Dry pontos Tesco-termékadata 12,5%-os
  alkoholtartalmat, Somlói borvidéket, valamint Pinot Noir, Chardonnay,
  Furmint és Pinot Blanc szőlőfajtát közöl. A kóstolójegyzet gyümölcsnevei
  nem ízesítések, ezért az íz változatlanul `natúr`.
- A Varga Bubis 1,5 literes rekord neve kifejezetten Irsai Olivér
  szőlőfajtát ad. Az alkoholtartalma `ismeretlen` maradt, mert a pontos
  1,5 literes termékforrás nem közöl százalékot; a 0,75 literes változat
  10%-os adatát nem másoltuk át másik kiszerelésre.
- A Natara Quattrosé pontos neve `részben erjedt édes rosé szőlőmust`;
  ezért a fajta korábbi `gyöngyözőbor` értékét erre a pontos, elemi
  terméktípusra javítottuk.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **10**.
- Változatlanul helyes rekord: **20**
  (`981413`, `1012920`, `4604640`, `33892:33895`, `33895:33898`,
  `677381:4214771`, `684191:4221581`, `674480:4211870`,
  `684200:4221590`, `677825:4215215`, `679190:4216580`,
  `679205:4216595`, `679187:4216577`, `683513:4220903`,
  `683516:4220906`, `683525:4220915`, `679175:4216565`,
  `683510:4220900`, `674924:4212314`, `683522:4220912`).
- Új megengedett érték: **6** (`eredet: Németország, Somló`;
  `fajta: részben erjedt szőlőmust`;
  `szőlőfajta: Furmint, Pinot Blanc, Pinot Noir`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `541486` | alkoholtartalom `ismeretlen` → `10,5%`; eredet `egyéb` → `Olaszország`; szín `egyéb` → `fehér` |
| `902348` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Németország` |
| `4600140` | alkoholtartalom `ismeretlen` → `12,5%`; szőlőfajta `egyéb` → `Pinot Noir, Chardonnay, Furmint, Pinot Blanc`; eredet `egyéb` → `Somló` |
| `458151:3995541` | szőlőfajta `egyéb` → `Irsai Olivér` |
| `690761:4228151` | fajta `gyöngyözőbor` → `részben erjedt szőlőmust` |

### 089. köteg – Pezsgő, habzóbor és gyöngyözőbor 26–50.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Château Dereszla Brut pontos termékforrásai Tokaj eredetet, Furmint
  szőlőfajtát és 11%-os alkoholtartalmat igazolnak. A Vintage tétel pontos
  termékadata Furmint és Hárslevelű házasítást közöl. A Prestige Réserve
  szőlőfajtája `egyéb` maradt, mert az eltérő évjáratokhoz tartozó pontos
  források nem egyeznek a Furmint és a Furmint–Hárslevelű összetételben.
- A François President Brut gyártói termékanyaga Etyek-Budát, pontos szakmai
  termékadata pedig Chardonnay és Pinot Noir szőlőfajtát közöl. A Fehérvári
  Reserve pontos termékforrása és közvetlen csomagolása Somlót igazol.
- A Törley Chardonnay Brut és Chardonnay Brut Nature pontos termékadata
  egyaránt 12%-os alkoholtartalmat és Chardonnay szőlőfajtát ad; a Brut Nature
  Etyek-Buda eredete is igazolt. A Teleki Tradíció teljes termékneve
  Villányi Chardonnay pezsgőként azonosítja a tételt.
- A Sauska Brut és Rosé Brut pontos termelői, illetve szakmai termékadata Tokaj
  eredetet, valamint Furmint, Chardonnay és Pinot Noir házasítást közöl. A
  felsorolt gyümölcsös kóstolójegyek nem ízesítések, ezért az íz mindkét
  rekordnál változatlanul `natúr`.
- A Kreinbacher hivatalos termékoldalai szerint a Rosé Brut Furmint,
  Chardonnay, Pinot Blanc, Pinot Noir és Kékfrankos, a Brut Classic pedig
  Furmint, Chardonnay, Pinot Blanc és Pinot Noir házasítása. A pontos
  termékadat a Rosé Brutnál 12%-os alkoholtartalmat, mindkét tételnél Somló
  eredetet igazol.
- A Babits pontos termékanyaga Tokaji Furmint Brutként azonosítja a tételt. A
  Törley Tokaji Brut 1,5 literes pontos termékoldala 13%-os alkoholtartalmat
  közöl; más kiszerelés adatait nem másoltuk át.
- A Laurent-Perrier hivatalos La Cuvée-oldala Champagne eredetet és
  Chardonnay, Pinot Noir, Meunier házasítást igazol, ezért a fajta is
  `champagne`. A BB termék teljes neve közvetlenül `Spumante` fajtát ad.
- A Mészáros Pannon Bianco Secco, a három Hungaria, a Törley Tokaji Brut
  0,75 és 3 literes tétele, a Château Dereszla Prestige Réserve, a két
  0,2 literes Törley Charmant és a Rex Danubius nem bizonyítható hiányzó
  mezőit nem következtettük ki; ezek jelenlegi, igazolható értékei helyesek.
- Módosított rekord: **15**.
- Módosított tulajdonságmező: **28**.
- Változatlanul helyes rekord: **10**
  (`679400:4216790`, `683546:4220936`, `764970:4302360`,
  `683519:4220909`, `684194:4221584`, `963254:4500644`,
  `532943:4070333`, `684215:4221605`, `684224:4221614`,
  `674477:4211867`).
- Új megengedett érték: **4** (`eredet: Champagne`;
  `szőlőfajta: Hárslevelű, Kékfrankos, Meunier`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `796676:4334066` | alkoholtartalom `ismeretlen` → `11%`; szőlőfajta `egyéb` → `Furmint`; eredet `egyéb` → `Tokaj` |
| `954362:4491752` | szőlőfajta `egyéb` → `Furmint, Hárslevelű` |
| `763485:4300875` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `765759:4303149` | eredet `egyéb` → `Somló` |
| `684188:4221578` | alkoholtartalom `ismeretlen` → `12%`; szőlőfajta `egyéb` → `Chardonnay` |
| `684185:4221575` | alkoholtartalom `ismeretlen` → `12%`; szőlőfajta `egyéb` → `Chardonnay`; eredet `egyéb` → `Etyek-Buda` |
| `684632:4222022` | szőlőfajta `egyéb` → `Chardonnay` |
| `694247:4231637` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj` |
| `777630:4315020` | szőlőfajta `egyéb` → `Furmint, Pinot Noir, Chardonnay`; eredet `egyéb` → `Tokaj` |
| `678362:4215752` | alkoholtartalom `ismeretlen` → `12%`; szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Blanc, Pinot Noir, Kékfrankos`; eredet `egyéb` → `Somló` |
| `678356:4215746` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Blanc, Pinot Noir`; eredet `egyéb` → `Somló` |
| `764424:4301814` | szőlőfajta `egyéb` → `Furmint` |
| `532937:4070327` | alkoholtartalom `ismeretlen` → `13%` |
| `946343:4483733` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir, Meunier`; eredet `egyéb` → `Champagne` |
| `684209:4221599` | fajta `pezsgő` → `spumante` |

### 090. köteg – Pezsgő, habzóbor és gyöngyözőbor, következő 25 új rekord.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- Az ág 51–77. pozíciójából a 61–62. pozíción álló két Voilá-rekord már a
  003. kötegben teljes kézi ellenőrzést kapott. Ezeket nem számoltuk el újra;
  helyettük a 76–77. pozíció két még ellenőrizetlen Hungaria-terméke került
  ebbe a 25 új rekordba.
- A BB Spumante teljes neve és közvetlen címkéje `Spumante` terméket
  azonosít, a BB és a Törley hivatalos termékleírása pedig muskotályos szőlő
  mustját közli. A BB Arany Cuvée hivatalos BB-termékleírása szintén
  muskotályos szőlőt igazol. A kóstolójegyekben felsorolt gyümölcsök nem
  ízesítések, ezért az íz változatlanul `natúr`.
- A Boldog Születésnapot pezsgő közvetlen, nagy felbontású címkéjének alsó
  sorában a 750 ml-es kiszerelés mellett 11,5%-os alkoholtartalom olvasható.
  A márka és a szőlőfajta nem bizonyítható a címkéről, ezért ezeknél nem
  következtettünk.
- A Juhász Eufória hivatalos termékoldala ugyanahhoz a 12%-os Extra Dry
  fehér pezsgőhöz Chardonnay, Rizlingszilváni és Zenit szőlőfajtát közöl.
  A gyümölcsös kóstolójegyek itt sem termékízesítések.
- A felülvizsgált Gedeon Birtok Brut 12%-os tételének pontos szakmai
  termékadata 50% Generosa és 50% Zöld veltelini házasítást, valamint
  Kunsági borvidéket ad. A termelő jelenlegi 12,5%-os változatának adatát nem
  másoltuk a névvel és képpel egyértelműen 12%-os forrásrekordra.
- A Hungaria CityPack közvetlen képe és pontos hivatalos csomagadata egyaránt
  két fehér Extra Dry és két Rosé Extra Dry 0,2 literes palackot mutat. A
  csomag pontos termékadata 12%-os alkoholtartalmat közöl, ezért a szín
  `fehér, rozé`, az alkoholtartalom pedig `12%`.
- A Törley, Hungaria, Szovjetszkoje Igrisztoje és Natara egyes jelenlegi
  termékoldalain az azonos nevű, de átdolgozott változatok alkoholfoka eltér
  a felülvizsgált rekord teljes nevében és képén szereplő értéktől. Ezeknél a
  rekordhoz tartozó, közvetlenül bizonyítható értéket tartottuk meg.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **9**.
- Változatlanul helyes rekord: **19**
  (`684206:4221596`, `684221:4221611`, `762012:4299402`,
  `679196:4216586`, `683531:4220921`, `683549:4220939`,
  `683534:4220924`, `683540:4220930`, `683543:4220933`,
  `679193:4216583`, `683537:4220927`, `683528:4220918`,
  `684218:4221608`, `684179:4221569`, `674492:4211882`,
  `679184:4216574`, `679178:4216568`, `683507:4220897`,
  `819437:4356827`).
- Új megengedett érték: **5** (`eredet: Kunság`;
  `szőlőfajta: Generosa, Rizlingszilváni, Zenit, Zöld veltelini`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `684212:4221602` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Muskotály` |
| `694262:4231652` | alkoholtartalom `ismeretlen` → `11,5%` |
| `684203:4221593` | szőlőfajta `egyéb` → `Muskotály` |
| `680072:4217462` | szőlőfajta `egyéb` → `Chardonnay, Rizlingszilváni, Zenit` |
| `965054:4502444` | szőlőfajta `egyéb` → `Generosa, Zöld veltelini`; eredet `egyéb` → `Kunság` |
| `684176:4221566` | alkoholtartalom `ismeretlen` → `12%`; szín `egyéb` → `fehér, rozé` |

### 091. köteg – Pezsgő, habzóbor és gyöngyözőbor 78–102.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Garamvári Classic Extra Dry hivatalos termékoldala Balatonboglár
  eredetet, valamint Chardonnay és Pinot Blanc szőlőfajtát igazol. A
  François President és a Louis François & Co. pontos termékadata egyaránt
  Chardonnay és Pinot Noir házasítást közöl; utóbbi közvetlen függőcímkéje a
  korábbi összefűzött márkanév helyett `Louis François & Co.` márkát mutat.
- A Sauska Extra Dry pontos termelői anyaga Tokaj eredetet, Furmint,
  Chardonnay és Pinot Noir szőlőfajtát közöl. A Kreinbacher Extra Dry
  hivatalos termékoldala Somlót, valamint Furmint, Chardonnay, Pinot Noir és
  Pinot Blanc házasítást igazol.
- A Veuve Émille, Vollereaux, Mumm, Moët & Chandon és Veuve Clicquot
  termékeket a közvetlen palackképek és a pontos gyártói termékadatok
  Champagne-ként azonosítják. A Veuve Émille 12,5%-os; a többi
  alkoholtartalma már helyes volt. A termékenként igazolt Chardonnay, Pinot
  Noir és Meunier összetételt rögzítettük; a Vollereaux Brut Nature Blanc de
  Noirs 100% Pinot Noir.
- Az I Heart Vino Frizzante, a csavarzáras Treviso és a Gancia Prosecco
  közvetlen képe fehér bort mutat, ezért a korábbi rosé értékeket töröltük.
  A Treviso-rekord palackján nem látható márka; a `Treviso` földrajzi
  megjelölés, ezért a márka `márka nélkül`, az eredet pedig `Treviso`.
- A Martini, Gancia és Cinzano Asti Moscato Bianco szőlőből készült Asti
  spumante. A Prosecco DOC-tételeknél a Glera szőlőfajtát, a Treviso nevű
  tételeknél a Treviso eredetet rögzítettük. A palackzár és a termékjelölés
  alapján az I Heart és a csavarzáras Treviso `gyöngyözőbor, prosecco`
  maradt, a Gancia, Menolia, Cinzano és Mionetto tételek fajtája
  `spumante, prosecco`.
- A két Henkell pontos e-címkéje a németországi Wiesbadenben működő gyártót
  és a terméket azonosítja, de szőlőfajtát nem közöl; ezért csak az eredetet
  javítottuk `Németország` értékre, a szőlőfajta `egyéb` maradt.
- A Bottega Fragolino Rosso gyártói adatlapja 10%-os, élénk vörös, édes,
  eperízű, olasz szőlőfajtákból készült boralapú italt igazol. A szőlőfajta
  ezért nem lett találgatással pontosítva.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **67**.
- Változatlanul helyes rekord: **0**.
- Új megengedett érték: **4** (`márka: Louis François & Co.`;
  `szőlőfajta: Glera, Moscato Bianco`; `eredet: Asti`).
  Törölt megengedett érték: **1** (`márka: Treviso`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `674678:4212068` | szőlőfajta `egyéb` → `Chardonnay, Pinot Blanc`; eredet `egyéb` → `Balatonboglár` |
| `965102:4502492` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir` |
| `684164:4221554` | márka `Francois Louis François & Co.` → `Louis François & Co.`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir` |
| `796385:4333775` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj` |
| `678359:4215749` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir, Pinot Blanc`; eredet `egyéb` → `Somló` |
| `557292:4094682` | alkoholtartalom `ismeretlen` → `12,5%`; fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne` |
| `764190:4301580` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir, Meunier`; eredet `egyéb` → `Champagne` |
| `751923:4289313` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir`; eredet `egyéb` → `Champagne` |
| `688085:4225475` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Chardonnay, Meunier`; eredet `egyéb` → `Champagne` |
| `694232:4231622` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne` |
| `694235:4231625` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne` |
| `694226:4231616` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne` |
| `684182:4221572` | szőlőfajta `egyéb` → `Glera`; szín `fehér, rozé` → `fehér` |
| `694277:4231667` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `684326:4221716` | márka `Treviso` → `márka nélkül`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso`; szín `rozé` → `fehér` |
| `684173:4221563` | eredet `egyéb` → `Németország` |
| `782171:4319561` | alkoholtartalom `ismeretlen` → `10%`; eredet `egyéb` → `Olaszország`; szín `egyéb` → `vörös` |
| `694292:4231682` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; szín `rozé` → `fehér` |
| `674585:4211975` | eredet `egyéb` → `Németország` |
| `825626:4363016` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso` |
| `946397:4483787` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso`; édesség `brut` → `extra brut` |
| `694295:4231685` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `694205:4231595` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `687956:4225346` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `684227:4221617` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera` |

### 092. köteg – Pezsgő, habzóbor és gyöngyözőbor 103–127.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **25**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **25**.
- A Mionetto, Martini és Gancia pontos gyártói termékadatai alapján a
  palackban erjesztett Prosecco- és Asti-tételek `spumante` fajtát kaptak.
  A Prosecco-termékeknél a Glera, a rozéknál a Pinot Noir, az Astiknál a
  Moscato Bianco szőlőfajta igazolt. A Valdobbiadene és Treviso
  eredetmegjelöléseket a teljes terméknévvel egyezően, országérték
  megkettőzése nélkül rögzítettük.
- A Pata Negra, Freixenet, Pere Ventura és Juvé & Camps termékek közvetlen
  palackképe, teljes neve és műszaki lapja Cava terméket, spanyol eredetet,
  valamint Macabeo, Xarel-lo és Parellada szőlőfajtát igazol. A `J. Garcia`
  és `Juve & Camps` hibás márkaérték csak egy-egy ilyen rekordon szerepelt;
  a címke szerinti `Pata Negra` és `Juvé & Camps` javítás után mindkettő
  használatlanná vált.
- A két azonos nevű 0,75 literes Törley alkoholmentes tételt a saját
  közvetlen palackkép különbözteti meg: az egyik rozé, a másik fehér. Ezek
  és a Mionetto 0.0 nem borfajták, hanem `alkoholmentes habzó ital`
  besorolást kaptak. A Mionetto gyártói adata 100% Glerát, olasz szőlőt és
  20 g/l cukrot közöl; a Hungaria termékadata 30 g/l cukrot ad. Az ág
  édességi skáláján ezért mindkettő `száraz`, nem `édes`.
- A Comedy Wine közvetlen dobozcímkéje és pontos termékleírása Sauvignon
  Blanc száraz fehér gyöngyözőbort igazol. Alkoholfokot és eredetet nem
  következtettünk hozzá. A BB Spumante neve és gyártói leírása spumante
  fajtát és muskotályos szőlőt igazol. A Teleki és Frittmann teljes neve
  közvetlenül Villány, illetve Kunság eredetet, utóbbi Irsai Olivér
  szőlőfajtát is közöl.
- A Giorgio pontos termékadata Sárgamuskotály–Furmint házasítást, Tokaj
  eredetet és fehér színt igazol. Az alkoholfoka évjáratonként eltér, a
  forrásrekord pedig nem közöl évjáratot, ezért `ismeretlen` maradt. Az
  Etyeki Kúria terméklapja Királyleányka–Zenit házasítást igazol; a rekord
  nevében szereplő 11,5%-ot nem írtuk felül a jelenlegi, 12%-os évjárat
  adatával. A Chiarli közvetlen címkéje és műszaki lapja vörös, édes,
  Emilia-Romagna eredetű Lambruscót igazol.
- A 0,2 literes Törley és a BB alkoholmentes ital minden meglévő mezője
  közvetlenül igazolható volt; bizonytalan szőlőfajtát vagy eredetet nem
  következtettünk hozzájuk.
- Módosított rekord: **23**.
- Módosított tulajdonságmező: **66**.
- Változatlanul helyes rekord: **2**
  (`684407:4221797`, `684395:4221785`).
- Új megengedett érték: **12** (`márka: Pata Negra, Juvé & Camps`;
  `fajta: cava`; `eredet: Valdobbiadene, Spanyolország, Emilia-Romagna`;
  `szőlőfajta: Macabeo, Xarel-lo, Parellada, Sauvignon Blanc,
  Királyleányka, Lambrusco`).
  Törölt megengedett érték: **2** (`márka: J. Garcia, Juve & Camps`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `684230:4221620` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `755643:4293033` | alkoholtartalom `ismeretlen` → `11%`; fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Valdobbiadene` |
| `661347:4198737` | szőlőfajta `egyéb` → `Glera`; eredet `Olaszország, Treviso` → `Treviso` |
| `694280:4231670` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `848207:4385597` | alkoholtartalom `ismeretlen` → `11,5%`; fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; édesség `egyéb` → `száraz` |
| `694274:4231664` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Chardonnay, Glera`; eredet `egyéb` → `Olaszország` |
| `694289:4231679` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `54585:54924` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `849422:4386812` | márka `J. Garcia` → `Pata Negra`; alkoholtartalom `ismeretlen` → `11,5%`; fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Macabeo, Xarel-lo, Parellada`; eredet `egyéb` → `Spanyolország` |
| `684167:4221557` | fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Parellada, Macabeo, Xarel-lo`; eredet `egyéb` → `Spanyolország` |
| `849512:4386902` | alkoholtartalom `ismeretlen` → `11,5%`; fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Macabeo, Parellada, Xarel-lo`; eredet `egyéb` → `Spanyolország` |
| `849509:4386899` | márka `Juve & Camps` → `Juvé & Camps`; alkoholtartalom `ismeretlen` → `12%`; fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Xarel-lo, Macabeo, Parellada`; eredet `egyéb` → `Spanyolország` |
| `683552:4220942` | fajta `habzóbor` → `alkoholmentes habzó ital`; szín `fehér, rozé` → `rozé` |
| `683555:4220945` | fajta `habzóbor` → `alkoholmentes habzó ital`; szín `fehér, rozé` → `fehér` |
| `789563:4326953` | édesség `édes` → `száraz` |
| `777618:4315008` | fajta `habzóbor` → `alkoholmentes habzó ital`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; édesség `édes` → `száraz` |
| `712796:4250186` | szőlőfajta `egyéb` → `Sauvignon Blanc`; szín `egyéb` → `fehér` |
| `674489:4211879` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Muskotály` |
| `679460:4216850` | eredet `egyéb` → `Villány` |
| `679301:4216691` | szőlőfajta `egyéb` → `Irsai Olivér`; eredet `egyéb` → `Kunság` |
| `679469:4216859` | szőlőfajta `egyéb` → `Sárgamuskotály, Furmint`; eredet `egyéb` → `Tokaj`; szín `egyéb` → `fehér` |
| `678326:4215716` | szőlőfajta `egyéb` → `Királyleányka, Zenit` |
| `761097:4298487` | szőlőfajta `egyéb` → `Lambrusco`; eredet `egyéb` → `Emilia-Romagna`; szín `egyéb` → `vörös` |

### 093. köteg – Pezsgő, habzóbor és gyöngyözőbor 128–152.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **3**.
- A forrásnév szerinti terméket ábrázoló közvetlen kép: **3**.
- Helyi kép nélkül, teljes név és pontos külső termékadat alapján ellenőrzött
  rekord: **22**.
- A Gere fehér és rosé Frici közvetlen palackképe 11%-os, száraz fehér,
  illetve rosé gyöngyözőbort mutat. A pincészet hivatalos leírása mindkettőt
  Villányhoz köti; a fehér változat Királyleányka, Sauvignon Blanc és Muscat
  Ottonel, a rosé Menoir és Kékfrankos házasítás.
- A Cinzano To Spritz közvetlen palackképe és pontos termékadata 11,5%-os,
  száraz fehér olasz spumantét igazol. Az eltérő piacokon közölt
  szőlőösszetétel nem egységes, ezért a szőlőfajta `egyéb` maradt.
- A két Pra’della Luna Prosecco DOC Millesimato Brut pontos termékadata
  11%-os, fehér, Veneto eredetű, 100% Glera spumantét igazol. A korábbi
  `rozé` szín és az általános `pezsgő` fajta ezért hibás volt.
- A Törley ICE, Hungaria Rosé Extra Dry és Hungaria Irsai Olivér azonos nevű
  forrásain több alkoholfokú receptúra fordul elő, helyi palackkép pedig
  nincs. Az alkoholtartalmuk ezért `ismeretlen` maradt; csak a névvel és
  pontos termékadattal bizonyított édességet, színt és magyar eredetet
  rögzítettük. Ugyanezen okból a Törley Excellence Sárgamuskotály 10%,
  10,5% és 11% forrásváltozatai közül sem választottunk alkoholfokot.
- A Henkell Trocken pontos gyártói adata 11,5%-os, száraz fehér német
  pezsgőt; a két Voilá termék pontos adata 6,5%-os édes áfonya-, illetve
  szamócaízű pezsgőkoktélt igazol. A Törley Talisman pontos, DRS-es
  termékadata 11%-os félszáraz fehér pezsgő.
- A két Martini Asti 7,5%-os, édes fehér, Moscato Bianco szőlőből készült
  Asti spumante. A Törley Excellence Chardonnay pontos termékadata
  12,5%-os, különlegesen száraz fehér, Etyek–Buda eredetű Chardonnay
  pezsgőt igazol.
- A Szovjetszkoje Igrisztoje pontos tételei 11%-os magyar száraz fehér,
  illetve félszáraz rosé pezsgők. A rosé rekord korábbi `száraz,
  félszáraz` kettős értéke hibás volt. A BB Spumante fehér változata
  muskotályos, Balatonboglár eredetű spumante; a rosé rekord nevében
  szereplő 10%-ot nem írtuk felül a jelenlegi, eltérő receptúra adatával.
- A csomagolási változattal egyező termékadat alapján a Törley Charmant
  Doux 1,5 literes, a Charmant Rouge egyutas, valamint a BB Doux egyutas
  tétele 11%-os. A jelenlegi DRS-változatok eltérő alkoholfokát nem
  másoltuk a régebbi, egyutas vagy magnum rekordokra.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **70**.
- Változatlanul helyes rekord: **0**.
- Új megengedett érték: **4** (`eredet: Magyarország, Veneto`;
  `szőlőfajta: Menoir, Muscat Ottonel`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `685118:4222508` | szőlőfajta `egyéb` → `Királyleányka, Sauvignon Blanc, Muscat Ottonel`; eredet `egyéb` → `Villány` |
| `685115:4222505` | szőlőfajta `egyéb` → `Menoir, Kékfrankos`; eredet `egyéb` → `Villány` |
| `751953:4289343` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Olaszország` |
| `3375587` | alkoholtartalom `ismeretlen` → `11%`; fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto`; szín `rozé` → `fehér` |
| `3375491` | eredet `egyéb` → `Magyarország`; édesség `egyéb` → `félszáraz`; szín `egyéb` → `rozé` |
| `3372542` | eredet `egyéb` → `Magyarország`; édesség `egyéb` → `félszáraz`; szín `egyéb` → `fehér` |
| `2817938` | eredet `egyéb` → `Magyarország` |
| `2817599` | alkoholtartalom `ismeretlen` → `11%`; fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto`; szín `rozé` → `fehér` |
| `2813886` | eredet `egyéb` → `Magyarország`; szín `egyéb` → `fehér` |
| `2813846` | alkoholtartalom `ismeretlen` → `11,5%`; eredet `egyéb` → `Németország`; szín `egyéb` → `fehér` |
| `2813338` | alkoholtartalom `ismeretlen` → `6,5%`; édesség `egyéb` → `édes` |
| `2813336` | alkoholtartalom `ismeretlen` → `6,5%`; édesség `egyéb` → `édes` |
| `2812864` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Magyarország`; szín `egyéb` → `fehér` |
| `2810944` | alkoholtartalom `ismeretlen` → `7,5%`; fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `2810943` | alkoholtartalom `ismeretlen` → `7,5%`; fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti`; édesség `egyéb` → `édes`; szín `egyéb` → `fehér` |
| `2808522` | alkoholtartalom `ismeretlen` → `12,5%`; eredet `egyéb` → `Etyek-Buda`; édesség `száraz` → `különlegesen száraz`; szín `egyéb` → `fehér` |
| `2808494` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Magyarország`; szín `egyéb` → `fehér` |
| `2807701` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár`; szín `egyéb` → `fehér` |
| `2805001` | eredet `egyéb` → `Magyarország` |
| `2799409` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Magyarország`; édesség `száraz, félszáraz` → `félszáraz` |
| `2754514` | szőlőfajta `egyéb` → `Sárgamuskotály`; eredet `egyéb` → `Etyek-Buda` |
| `2754149` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Balatonboglár` |
| `2753649` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Magyarország` |
| `2752930` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Magyarország` |
| `2752928` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Magyarország` |

### 094. köteg – Pezsgő, habzóbor és gyöngyözőbor 153–177.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **0**.
- Helyi kép nélkül, teljes név és pontos külső termékadat alapján ellenőrzött
  rekord: **25**.
- A Törley Charmant Doux és Fortuna egyutas tételeknél több, egymástól eltérő
  alkoholfokú receptúra található, a rekordokhoz pedig nincs helyi palackkép.
  Az alkoholtartalmuk ezért `ismeretlen` maradt. A BB Demi Sec és a Törley
  Charmant Rosé pontos egyutas termékadata ezzel szemben 11,5%-ot igazol.
  A négy magyar tételnél a magyar eredetet rögzítettük.
- Az Allini Secco Rosato és Bianco, valamint a közös Rosato / Bianco rekord
  pontos Lidl-termékadata 10%-os, száraz olasz gyöngyözőbort igazol. Az Allini
  Prosecco frizzante 10,5%-os, fehér, Glera szőlőből készült Treviso eredetű
  gyöngyözőbor; a két spumante Prosecco teljesen habzó, fehér Glera-tétel.
  A Conegliano Valdobbiadene Superiore 11%-os Extra Dry, a DOC Brut pontos
  termékadata 10,5%-os.
- Az Allini Fragolino Frizzante pontos termékadata 7,5%-os, édes vörös,
  eperízesítésű olasz gyöngyözőbort igazol. A Bitterol Sprizz 10,5%-os,
  narancsaromás gyümölcsborkoktél, ezért `pezsgőkoktél` fajtát és az új,
  elemi `narancs` ízértéket kapta. Nem következtettünk hozzá bizonytalan
  eredetet, édességet vagy színt.
- A két Pannon Imperial Extra Dry pontos termékadata 12,5%-os,
  Balatonboglárról származó Chardonnay fehér pezsgőt igazol. Az Arestel
  11,5%-os spanyol Cava, Macabeo, Xarel-lo és Parellada házasítás. A két
  Château Dereszla Brut Tokajból származó, Furmint és Hárslevelű házasítású
  fehér pezsgő; évjárat nélküli alkoholfokot nem következtettünk hozzájuk.
- Az Arvenus szakmai versenyadata száraz fehér, Kunság eredetű, Bianca és
  egyéb szőlőfajtákból készült pezsgőt igazol. A termékképen és a szakmai
  adatban szereplő `Arvenus` alakra javítottuk az egyetlen `Arnevus`
  márkaértéket, majd a használatlanná vált hibás alakot töröltük.
- A Feind Irsai Olivér pontos termékadata 11%-os száraz fehér gyöngyözőbort
  igazol. A Burg Schöneck 0%-os, száraz fehér német alkoholmentes habzó ital.
  A Lelovits Gyöngybor száraz fehér, Villány eredetű, Muscat Ottonel
  gyöngyözőbor; alkoholfoka évjáratonként 9%, 10% és 11% is lehet, ezért az
  évjárat nélküli rekordban `ismeretlen` maradt.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **73**.
- Változatlanul helyes rekord: **0**.
- Új megengedett érték: **2** (`íz: narancs`; `szőlőfajta: Bianca`).
  Törölt megengedett érték: **1** (`márka: Arnevus`).

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `2752927` | eredet `egyéb` → `Magyarország` |
| `2752926` | alkoholtartalom `ismeretlen` → `11,5%`; eredet `egyéb` → `Magyarország` |
| `2752925` | eredet `egyéb` → `Magyarország` |
| `2752923` | alkoholtartalom `ismeretlen` → `11,5%`; eredet `egyéb` → `Magyarország` |
| `10000055` | eredet `egyéb` → `Magyarország`; édesség `egyéb` → `édes` |
| `10000060` | eredet `egyéb` → `Magyarország`; szín `egyéb` → `fehér` |
| `10000102` | alkoholtartalom `ismeretlen` → `10%`; eredet `egyéb` → `Olaszország`; édesség `egyéb` → `száraz` |
| `10000103` | alkoholtartalom `ismeretlen` → `10%`; eredet `egyéb` → `Olaszország`; édesség `egyéb` → `száraz` |
| `10000218` | alkoholtartalom `ismeretlen` → `12,5%`; szőlőfajta `egyéb` → `Chardonnay`; eredet `egyéb` → `Balatonboglár`; szín `egyéb` → `fehér` |
| `10000275` | alkoholtartalom `ismeretlen` → `10,5%`; fajta `pezsgő, prosecco` → `gyöngyözőbor, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso`; szín `rozé` → `fehér` |
| `10000296` | alkoholtartalom `ismeretlen` → `7,5%`; íz `natúr` → `eper`; eredet `egyéb` → `Olaszország` |
| `10000500` | alkoholtartalom `ismeretlen` → `10,5%`; fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto`; szín `rozé` → `fehér` |
| `10003027` | szőlőfajta `egyéb` → `Furmint, Hárslevelű`; eredet `egyéb` → `Tokaj`; szín `egyéb` → `fehér` |
| `10003226` | eredet `egyéb` → `Magyarország`; szín `egyéb` → `fehér` |
| `10009076` | alkoholtartalom `ismeretlen` → `10,5%`; édesség `egyéb` → `száraz` |
| `10022962` | alkoholtartalom `ismeretlen` → `11,5%`; fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Macabeo, Xarel-lo, Parellada`; eredet `egyéb` → `Spanyolország`; szín `egyéb` → `fehér` |
| `10064615` | márka `Arnevus` → `Arvenus`; szőlőfajta `egyéb` → `Bianca, egyéb`; eredet `egyéb` → `Kunság`; édesség `egyéb` → `száraz`; szín `egyéb` → `fehér` |
| `10076524` | alkoholtartalom `ismeretlen` → `11%`; fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Valdobbiadene`; édesség `egyéb` → `különlegesen száraz`; szín `rozé` → `fehér` |
| `10099670` | alkoholtartalom `ismeretlen` → `11%`; édesség `egyéb` → `száraz`; szín `egyéb` → `fehér` |
| `10099672` | alkoholtartalom `ismeretlen` → `12,5%`; szőlőfajta `egyéb` → `Chardonnay`; eredet `egyéb` → `Balatonboglár`; szín `egyéb` → `fehér` |
| `10099673` | szőlőfajta `egyéb` → `Furmint, Hárslevelű` |
| `10101641` | eredet `egyéb` → `Németország`; édesség `egyéb` → `száraz` |
| `10107419` | alkoholtartalom `ismeretlen` → `10,5%`; fajta `gyöngyözőbor` → `pezsgőkoktél`; íz `natúr` → `narancs` |
| `10107421` | alkoholtartalom `ismeretlen` → `10%`; eredet `egyéb` → `Olaszország` |
| `BTY-X17072400320021` | szőlőfajta `egyéb` → `Muscat Ottonel`; szín `egyéb` → `fehér` |

### 095. köteg – Pezsgő, habzóbor és gyöngyözőbor 178–202.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált képfájl: **0**.
- Helyi kép nélkül, teljes név és pontos külső termékadat alapján ellenőrzött
  rekord: **25**.
- Az Etyeki Kúria Pláne rekord nevével és alkoholfokával egyező közvetlen
  termékadat Királyleányka és Zenit házasítást igazol. A korábbi, harmadik
  szőlőfajtát is tartalmazó receptúrákat nem másoltuk át. A Garamvári Zsongás
  Chardonnay és Zenit házasítású, Balatonboglár eredetű fehér gyöngyözőbor.
- A 12%-os Babarczi Buborczi pontos termékadata Tramini, Cserszegi fűszeres
  és Irsai Olivér házasítást közöl. A Grand Tokaj 11,5%-os Pillanat Cuvée
  2020 pontos adata száraz fehér magyar gyöngyözőbort igazol; az évjáratonként
  eltérő házasítás miatt a szőlőfajta `egyéb` maradt.
- A Feind Bollicine Olivier nevéből és pontos termékadatából az Irsai Olivér,
  fehér gyöngyözőbor-jelleg bizonyítható. A név szerint fehér Feind Bollicine
  rekord, valamint a Haraszthy Sir Irsai minden jelenlegi tulajdonsága helyes
  volt, ezért ez a két rekord változatlan maradt.
- A Valmarone Fragolino Rosso 10%-os, eperízesítésű, félédes vörös Veneto
  gyöngyözőbor. A Juhász neve közvetlenül Kékfrankos rosét, a Teleki pontos
  termékadata 12%-os Villányi rosé gyöngyözőbort igazol. A Teleki házasítása
  évjáratonként változik, ezért szőlőfajtája `egyéb` maradt.
- A Valmarone Prosecco DOC teljesen habzó, Extra Dry spumante, az I Am és az
  Alberto Torresi Prosecco pedig frizzante, ezért gyöngyözőbor. Mindhárom
  fehér Glera-tétel. A Corner Valdobbiadene DOCG fehér Glera spumante; a
  rekord nevében szereplő 11,5%-ot nem írtuk felül a jelenlegi 11%-os
  változat adatával.
- A Visiega 11,5%-os spanyol Cava Macabeo, Xarel-lo és Parellada házasítás.
  A Ca' Ernesto Millesimato nem Prosecco, hanem 11,5%-os fehér Veneto
  spumante. A Ca' Ernesto Valdobbiadene DOCG ezzel szemben Glera-alapú,
  Extra Dry fehér Prosecco spumante.
- A Paulus Extra Dry pontos, 12%-os tételadata Királyleányka szőlőt és Mór
  eredetet igazol. A Paulus Honey részben erjedt szőlőmust Cserszegi fűszeres
  és Királyleányka házasításból; a rekord nevében szereplő 10%-ot nem
  cseréltük le a jelenlegi receptúra eltérő alkoholfokára.
- A Valmarone Brut olasz spumante, és kizárólag `brut` édességű. A
  Veuve Pelletier–Ponsardin forrásnév két champagne-nevet fűz össze; a márka
  bizonytalansága miatt a jelenlegi márkát megtartottuk, de a Champagne
  eredet, a `champagne` fajta és a kizárólagos `brut` érték mindkét lehetséges
  névhez közvetlenül igazolt.
- Az André Gallois 10,5%-os francia Vin Mousseux Brut; az `ADRIEN ROMET`
  előtag egy másik katalógustételből került a nevébe. Az Adrien Romet Blanc
  de Blancs ezzel szemben francia, Chardonnay-alapú, hagyományos módszerrel
  készült pezsgő. A Valentin Vignot 12%-os Chardonnay Crémant de Bourgogne,
  ezért fajtája kizárólag `crémant`, eredete pedig `Burgundia`.
- A Bosco dei Cirmioli gyártói terméklapja 11%-os, fehér Glera Prosecco
  frizzantét igazol; ezért a korábbi általános pezsgőfajtát
  `gyöngyözőbor, prosecco` érték váltotta fel.
- Módosított rekord: **23**.
- Módosított tulajdonságmező: **65**.
- Változatlanul helyes rekord: **2** (`BTY-X17366100320021`,
  `BTY-X18881300320021`).
- Új megengedett érték: **5** (`márka: ANDRÉ GALLOIS`;
  `eredet: Burgundia, Franciaország, Mór`; `szőlőfajta: Tramini`).
  Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17338600320021` | szőlőfajta `egyéb` → `Királyleányka, Zenit` |
| `BTY-X17404200320021` | szőlőfajta `egyéb` → `Chardonnay, Zenit`; eredet `egyéb` → `Balatonboglár`; szín `egyéb` → `fehér` |
| `BTY-X17583600320021` | szőlőfajta `egyéb` → `Tramini, Cserszegi fűszeres, Irsai Olivér` |
| `BTY-X18025900320021` | eredet `Tokaj` → `Magyarország`; szín `vörös` → `fehér` |
| `BTY-X18881200320022` | szőlőfajta `egyéb` → `Irsai Olivér`; szín `egyéb` → `fehér` |
| `BTY-X17496700320021` | fajta `pezsgő` → `gyöngyözőbor`; íz `natúr` → `eper`; eredet `egyéb` → `Veneto`; édesség `édes` → `félédes` |
| `BTY-X17365100320021` | szőlőfajta `egyéb` → `Kékfrankos` |
| `BTY-X19000700320021` | alkoholtartalom `ismeretlen` → `12%` |
| `BTY-X17496800320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto`; édesség `száraz` → `különlegesen száraz`; szín `rozé` → `fehér` |
| `BTY-X17375700320021` | fajta `pezsgő, prosecco` → `gyöngyözőbor, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; szín `rozé` → `fehér` |
| `BTY-X17492500320021` | fajta `pezsgő, prosecco` → `gyöngyözőbor, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto`; szín `rozé` → `fehér` |
| `BTY-X17493900320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Valdobbiadene`; szín `rozé` → `fehér` |
| `BTY-X17497500320021` | fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Macabeo, Xarel-lo, Parellada`; eredet `egyéb` → `Spanyolország` |
| `BTY-X17375900320021` | fajta `pezsgő, prosecco` → `spumante`; eredet `egyéb` → `Veneto`; szín `egyéb` → `fehér` |
| `BTY-X17195800320021` | szőlőfajta `egyéb` → `Királyleányka`; eredet `egyéb` → `Mór` |
| `BTY-X17199100320021` | fajta `pezsgő` → `részben erjedt szőlőmust`; szőlőfajta `egyéb` → `Cserszegi fűszeres, Királyleányka`; eredet `egyéb` → `Mór` |
| `BTY-X17496900320021` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Olaszország`; édesség `brut, száraz` → `brut` |
| `BTY-X13897900320021` | fajta `pezsgő` → `champagne`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `BTY-X17375500320021` | márka `ADRIEN ROMET` → `ANDRÉ GALLOIS`; eredet `egyéb` → `Franciaország` |
| `BTY-X17376200320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Valdobbiadene`; édesség `száraz` → `különlegesen száraz`; szín `rozé` → `fehér` |
| `BTY-X17376300320021` | szőlőfajta `egyéb` → `Chardonnay`; eredet `egyéb` → `Franciaország` |
| `BTY-X17494100320021` | fajta `pezsgő, crémant` → `crémant`; szőlőfajta `egyéb` → `Chardonnay`; eredet `egyéb` → `Burgundia` |
| `BTY-X17723000320021` | alkoholtartalom `ismeretlen` → `11%`; fajta `pezsgő, prosecco` → `gyöngyözőbor, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto` |

### 096. köteg – Pezsgő, habzóbor és gyöngyözőbor 203–227.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Törley-termékek közvetlen címkéit és pontos termékadatait együtt
  vizsgáltuk. A Gála, Charmant és Talisman Etyek-Buda eredetű; a Fortuna
  Irsai Olivér, Muscat Lunel, Muscat Ottonel és Rizlingszilváni házasítás;
  az Excellence tételek Sárgamuskotály, illetve Chardonnay fajtájúak; a
  Muscosecco Cserszegi fűszeres és Irsai Olivér házasítása.
- A Hungaria Extra Dry Etyek-Buda eredetű Chardonnay, Királyleányka és
  Pinot Noir házasítás. A két Kreinbacher tétel pontos termékadata Somlót
  és az eltérő Furmint-, Chardonnay-, Pinot Blanc- és Pinot Noir-arányokat
  igazolja.
- A Codorníu Selección Familia Raventós címkéje és pontos termékadata
  spanyol, brut Cava-besorolást, valamint Chardonnay, Macabeo és Xarel-lo
  szőlőfajtákat igazol. A Louis François címkéjén a helyes márkanév
  `Louis François & Co.`, a termék Brut Nature, Chardonnay és Pinot Noir
  házasítás.
- A Cinzano, Gancia és Mionetto teljesen habzó olasz tételeinél a meglévő
  `spumante` értéket használtuk; a Prosecco tételek Glera szőlőfajtájúak.
  A Gancia Prosecco fehér, nem rozé. A Cinzano To Spritz szőlőfajtája
  `egyéb` maradt, mert a különböző piacokon közölt összetételek eltérnek,
  ezért nem rögzítettünk bizonytalan fajtát.
- A BB, Szovjetszkoje és Catherina tételek pontos magyar termék- és
  gyártói adatai alapján az eddigi `egyéb` eredetet `Magyarország`
  értékre pontosítottuk.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **44**.
- Változatlanul hagyott rekord: **0**.
- Új megengedett érték: **1** (`szőlőfajta: Muscat Lunel`).
- Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17215300320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17215500320021` | szőlőfajta `egyéb` → `Irsai Olivér, Muscat Lunel, Muscat Ottonel, Rizlingszilváni`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17216700320021` | szőlőfajta `egyéb` → `Sárgamuskotály`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17214100320021` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17912100320021` | fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Chardonnay, Macabeo, Xarel-lo`; eredet `egyéb` → `Spanyolország`; édesség `száraz` → `brut` |
| `BTY-X17216300320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17921500320021` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Blanc, Pinot Noir`; eredet `egyéb` → `Somló` |
| `BTY-X17218500320021` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17673500320021` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir, Pinot Blanc`; eredet `egyéb` → `Somló` |
| `BTY-X17412700320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17218300320021` | márka `Francois Louis François & Co.` → `Louis François & Co.`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; édesség `brut` → `brut nature` |
| `BTY-X17428000320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `BTY-X17216600320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17584600320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; szín `rozé` → `fehér` |
| `BTY-X17216100320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17218100320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17218200320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17215600320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17215200320021` | szőlőfajta `egyéb` → `Cserszegi fűszeres, Irsai Olivér`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17215400320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17415000320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17219700320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera` |
| `BTY-X17278900320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17278900320022` | eredet `egyéb` → `Magyarország` |
| `BTY-X17427800320021` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Olaszország` |

### 097. köteg – Pezsgő, habzóbor és gyöngyözőbor 228–252.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Mionetto hivatalos termékadata a Treviso DOC Brut tételt Glera szőlőből
  készült `spumante, prosecco` termékként igazolja. A BB és Catherina
  termékeknél a közvetlen címkéket, a teljes forrásnevet és a gyártói
  adatokat együtt vizsgáltuk; a BB Spumante muskotályos, Balatonboglár
  eredetű spumante, a két Catherina tétel magyar pezsgő.
- A Hungaria Irsai Olivér Doux Irsai Olivér szőlőből készült, az Irsai
  Olivér Extra Dry ugyanezt a fajtát, a Grande Cuvée és az Extra Dry pedig
  Chardonnay, Királyleányka és Pinot Noir házasítást igazol. Mind a négy
  pontosított Hungaria-tétel Etyek-Buda eredetű. A forrásnévben szereplő
  alkoholfokokat megtartottuk ott is, ahol a jelenlegi receptúra adata már
  eltér.
- A Martini Asti címkéje és gyártói lapja Moscato Bianco szőlőből készült
  Asti spumantét igazol. A Törley Muscateller Etyek-Buda, a Henkell Trocken
  Németország, a Szovjetszkoje Igrisztoje pedig Magyarország eredetet
  kapott; bizonytalan szőlőfajtát ezekhez nem következtettünk.
- A Dom Pérignon rekord neve 2008-as évjáratot azonosít, miközben a helyi
  illusztráció egy 2010-es palackot mutat. Emiatt a képről nem vittünk át
  évjáratspecifikus adatot; a pontos 2008-as terméklap alapján a rekord
  Chardonnay–Pinot Noir házasítású, brut Champagne. A Natara pontos adata
  Kunság eredetet, a Paulus Generosa közvetlen címkéje és gyártói lapja
  Generosa szőlőt, Mór eredetet és Extra Dry édességi szintet igazol.
- A François President Brut Chardonnay és Pinot Noir házasítású,
  Etyek-Buda eredetű. A Törley Tokaji Brut Furmint–Hárslevelű házasítás;
  a `brut` mellett szereplő redundáns `száraz` értéket eltávolítottuk. A
  Törley Chardonnay Nyerspezsgő címkéje és pontos gyártói lapja 12%-os,
  Etyek-Buda eredetű Chardonnay Brut Nature tételt igazol.
- A Freixenet Cordon Negro palackcímkéje és hivatalos termékadata alapján
  Parellada, Macabeo és Xarel-lo szőlőből készült spanyol brut Cava; a
  hibás `félszáraz` értéket eltávolítottuk.
- Módosított rekord: **21**.
- Módosított tulajdonságmező: **44**.
- Változatlanul hagyott rekord: **4**
  (`BTY-X17216000320021`, `BTY-X17215000320021`,
  `BTY-X17217000320021`, `BTY-X17217400320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17221700320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera` |
| `BTY-X17279000320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17279000320022` | eredet `egyéb` → `Magyarország` |
| `BTY-X17214500320021` | szőlőfajta `egyéb` → `Irsai Olivér`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17214300320021` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17175800320021` | fajta `pezsgő, spumante` → `spumante`; szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `BTY-X17473500320021` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `BTY-X17215700320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17220300320021` | eredet `egyéb` → `Németország` |
| `BTY-X17412100320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X10459100320021` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X12755700320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Champagne`; édesség `száraz` → `brut` |
| `BTY-X16687600320021` | eredet `egyéb` → `Kunság` |
| `BTY-X17175600320021` | szőlőfajta `egyéb` → `Irsai Olivér`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17199900320021` | szőlőfajta `egyéb` → `Generosa`; eredet `egyéb` → `Mór`; édesség `száraz` → `különlegesen száraz` |
| `BTY-X17214700320021` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17217100320021` | szőlőfajta `egyéb` → `Furmint, Hárslevelű`; édesség `brut, száraz` → `brut` |
| `BTY-X17217600320021` | szőlőfajta `egyéb` → `Muskotály` |
| `BTY-X17217700320021` | fajta `pezsgő, spumante` → `spumante`; szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `BTY-X17219000320021` | alkoholtartalom `ismeretlen` → `12%`; eredet `egyéb` → `Etyek-Buda`; édesség `száraz` → `brut nature` |
| `BTY-X17219900320021` | fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Parellada, Macabeo, Xarel-lo`; eredet `egyéb` → `Spanyolország`; édesség `brut, félszáraz` → `brut` |

### 098. köteg – Pezsgő, habzóbor és gyöngyözőbor 253–277.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Henkell Blanc de Blancs pontos gyártói e-címkéje német eredetet igazol,
  de a felülvizsgált, 12%-os forrásváltozathoz nem közöl egyértelmű
  szőlőfajtákat, ezért azok `egyéb` értéken maradtak. A Laurent-Perrier La
  Cuvée Chardonnay, Pinot Noir és Meunier házasítású brut Champagne.
- A Feind Coupé Extra Dry különböző időpontú termékadatai Zenit, illetve
  Sauvignon Blanc szőlőfajtát közölnek. A 12%-os forrásrekordhoz ezért nem
  választottunk bizonytalan receptúrát; csak a mindkét forrásban igazolt
  Balatonfüred-Csopak eredetet rögzítettük. Az Etyeki Kúria felülvizsgált,
  12,5%-os tétele Sauvignon Blancból készült brut pezsgő, Etyek-Buda
  eredete már helyes volt.
- A két Fehérvári Reserve tétel Somló eredetű. A Garamvári Brut Nature
  Chardonnay és Pinot Noir házasítás, a Classic Brut Chardonnay, Furmint és
  Pinot Blanc házasítás; mindkettő Balatonboglár eredetű.
- A Szovjetszkoje Igrisztoje két pontos termékadata magyar eredetet, a
  Natara édes, száraz és Cuvée Extra Dry termékanyagai Kunság eredetet
  igazolnak. A forrásnevekben szereplő alkoholfokokat változatlanul
  megtartottuk.
- A Cinzano, Martini és Gancia Asti tételek Moscato Bianco szőlőből készült
  Asti spumanték. A Martini Prosecco Glera szőlőből készült olasz
  `spumante, prosecco`; a Martini Brut Chardonnay és Glera házasítású olasz
  spumante. A Gancia Brut gyártói lapja csak nem részletezett alkalmas
  szőlőket közöl, ezért szőlőfajtája `egyéb` maradt.
- A Mumm Grand Cordon, a Moët & Chandon Brut Impérial és a Veuve Clicquot
  Yellow Label Champagne eredetét, valamint Pinot Noir, Chardonnay és
  Meunier házasítását a közvetlen palackképek és a gyártói termékadatok
  igazolják. A `brut` mellett szereplő redundáns `száraz` értékeket
  eltávolítottuk.
- A Sauska Brut Tokaj eredetű Furmint, Chardonnay és Pinot Noir házasítás.
  A Laposa Méthode Charmat Extra Dry pontos termékadata Furmint szőlőt és
  Badacsony borvidéket közöl. A La Gioiosa palackcímkéje és gyártói lapja
  Glera szőlőből készült, Treviso eredetű brut `spumante, prosecco`
  terméket igazol.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **58**.
- Változatlanul hagyott rekord: **0**.
- Új megengedett érték: **2** (`eredet: Badacsony,
  Balatonfüred-Csopak`).
- Törölt megengedett érték: **0**.
- Az első Fehérvári Brut Reserve írási próbát a PowerShell beépített
  `h` aliasával ütköző rövid ellenőrzőfüggvény-név megszakította. A
  rekordot a teljes validátor még a hiba után visszaállította; az
  egyértelműen átnevezett függvénnyel megismételt írás és az azt követő
  összes ellenőrzés sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17220500320021` | eredet `egyéb` → `Németország` |
| `BTY-X17220800320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir, Meunier`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `BTY-X17276800320021` | eredet `egyéb` → `Balatonfüred-Csopak` |
| `BTY-X17338500320021` | szőlőfajta `egyéb` → `Sauvignon Blanc`; édesség `száraz` → `brut` |
| `BTY-X17364000320021` | eredet `egyéb` → `Somló` |
| `BTY-X17364100320021` | eredet `egyéb` → `Somló` |
| `BTY-X17380100320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17389600320021` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `BTY-X17404300320021` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Balatonboglár` |
| `BTY-X17405000320021` | szőlőfajta `egyéb` → `Chardonnay, Furmint, Pinot Blanc`; eredet `egyéb` → `Balatonboglár` |
| `BTY-X17415400320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17455300320021` | eredet `egyéb` → `Kunság` |
| `BTY-X17455600320021` | eredet `egyéb` → `Kunság` |
| `BTY-X17455700320021` | eredet `egyéb` → `Kunság` |
| `BTY-X17473300320021` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `BTY-X17473700320021` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Chardonnay, Glera`; eredet `egyéb` → `Olaszország`; édesség `brut, száraz` → `brut` |
| `BTY-X17473800320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `BTY-X17475700320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Chardonnay, Meunier`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `BTY-X17584300320021` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `BTY-X17584400320021` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Olaszország`; édesség `brut, száraz` → `brut` |
| `BTY-X17656300320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne` |
| `BTY-X17656400320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `BTY-X17673400320021` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj`; édesség `brut, száraz` → `brut` |
| `BTY-X17684900320021` | szőlőfajta `egyéb` → `Furmint`; eredet `Balaton` → `Badacsony` |
| `BTY-X17821000320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso`; édesség `különlegesen száraz` → `brut` |

### 099. köteg – Pezsgő, habzóbor és gyöngyözőbor 278–302.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Pol Roger Brut Réserve hivatalos termékadata azonos arányú Pinot Noir,
  Meunier és Chardonnay házasítást, valamint Champagne eredetet igazol. A
  pontos alkoholtartalom forrásonként 12% és 12,5% között eltért, a
  forrásrekord pedig nem tartalmazott alkoholfokot, ezért azt nem egészítettük
  ki bizonytalan értékkel.
- A Zonin 1821 hivatalos termékadata Glera szőlőből készült, venetói Prosecco
  DOC Spumantét igazol. A Sauska Extra Dry Tokaj eredetű Furmint, Chardonnay
  és Pinot Noir házasítás. A Natara Moscato pontos termékadata a már helyesen
  rögzített Muskotály mellett Kunság eredetet igazol.
- A három Menolia Prosecco közvetlen címkéje és a repó pontos
  termékpárhuzamai Glera szőlőből készült, Treviso DOC eredetű
  `spumante, prosecco` terméket igazolnak.
- A Törley Selection Brut és Extra Sec pontos termékadata 12,5%-os,
  Etyek-Buda eredetű pezsgőt igazol. Biztos szőlőfajta-adat hiányában a
  szőlőfajtát nem egészítettük ki.
- A Feind Méthode Traditionnelle 100% Chardonnay, Balatonfüred-Csopak eredetű
  brut pezsgő. A Garamvári Blanc Fleur Pinot Blanc szőlőből készült,
  Balatonboglár eredetű tétel.
- A Villa Vincento 24K Gold közvetlen címkéje és a hivatalos forgalmazói adat
  11%-os, magyar eredetű, édes pezsgőt igazol. A La Gioiosa Asolo hivatalos
  termékadata Glera szőlőből készült Asolo Prosecco Superiore DOCG Spumantét
  igazol; az `Asolo` elemi eredetértéket ezért felvettük.
- A Paulus Secco jelenlegi hivatalos termékadata Királyleányka szőlőt és Mór
  eredetet igazol. A mai alkoholfok eltér a felülvizsgált régebbi, 12%-os
  forrásváltozattól, ezért a forrásrekord alkoholfokát megtartottuk.
- A BB Ezüst Cuvée helyi képe egy korábbi Extra Dry változatot mutat, míg a
  jelenlegi hivatalos termékoldal félszáraz tételt közöl. Emiatt az
  édességet nem írtuk felül; csak a mindkét termékkörnyezetben igazolt
  Balatonboglár eredetet rögzítettük.
- A két Charmant Doux pontos termékadata Etyek-Buda eredetet, a két Törley
  Tokaji Brut Furmint és Hárslevelű házasítást igazol. A Törley Chardonnay
  Brut Chardonnay szőlőből készült, Etyek-Buda eredetű brut pezsgő.
- A Mionetto Treviso Frizzante hivatalos termékadata Glera szőlőt és Treviso
  eredetet, a Garamvári Lellei Furmint hivatalos adata Furmint szőlőt és
  Balatonboglár eredetet, a Gancia Asti pontos termékpárhuzama pedig Moscato
  Bianco szőlőből készült Asti spumantét igazol.
- A Varga Extra Száraz Pezsgőnél nem találtunk a pontos forrásváltozathoz
  megbízható szőlőfajta- és eredetadatot. A BB Frizzante félédes fehér
  gyöngyözőbor minden jelenlegi értékét a név, a kép és a termékadat
  alátámasztotta; ezt a két rekordot változatlanul hagytuk.
- Módosított rekord: **23**.
- Módosított tulajdonságmező: **52**.
- Változatlanul hagyott rekord: **2** (`BTY-X18337300320021`,
  `BTY-X17214000320021`).
- Új megengedett érték: **1** (`eredet: Asolo`).
- Törölt megengedett érték: **0**.
- A Pol Roger első írási próbája után a PowerShell natív argumentumkezelése
  elvette a `python -c` ellenőrző f-stringjének idézőjeleit. A sikertelen
  ellenőrzés az aktuális rekordot automatikusan visszaállította; a bemeneten
  átadott ellenőrzőforrással megismételt írás sikeres volt.
- A következő ötrekordos szerkesztési csoport első indítása a kötelező
  PowerShell-szóközök nélkül összetömörített `foreach` kifejezésnél még
  beolvasás vagy írás előtt szintaktikai hibával leállt. A kibontott,
  ellenőrizhető változat mind az öt rekordot sikeresen írta.
- A záró három rekord első próbáját egy új ellenőrző túl szigorú
  értékvizsgálata állította meg: a kategóriafában üres objektummal jelölt
  logikai tulajdonságokat tévesen értéklistaként kezelte. Az aktuális rekord
  automatikusan visszaállt; a logikai ágat külön kezelő javított ellenőrzővel
  mindhárom írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17884700320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `BTY-X17912400320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto` |
| `BTY-X17951200320021` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj` |
| `BTY-X18144800320021` | eredet `egyéb` → `Kunság` |
| `BTY-X18184200320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso` |
| `BTY-X18184300320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso` |
| `BTY-X18415100320021` | alkoholtartalom `ismeretlen` → `12,5%`; eredet `egyéb` → `Etyek-Buda`; édesség `brut, száraz` → `brut` |
| `BTY-X18415200320021` | alkoholtartalom `ismeretlen` → `12,5%`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X18483300320021` | szőlőfajta `egyéb` → `Chardonnay`; eredet `Balaton` → `Balatonfüred-Csopak`; édesség `brut, száraz` → `brut` |
| `BTY-X18483600320021` | szőlőfajta `egyéb` → `Pinot Blanc`; eredet `egyéb` → `Balatonboglár` |
| `BTY-X18496000320021` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Magyarország`; édesség `száraz` → `édes` |
| `BTY-X18701100320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Asolo` |
| `BTY-X18799300320021` | szőlőfajta `egyéb` → `Királyleányka`; eredet `egyéb` → `Mór` |
| `BTY-X18879600320021` | eredet `egyéb` → `Balatonboglár` |
| `BTY-X18184100320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso` |
| `BTY-X34782300320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X80329900320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X15539800320021` | szőlőfajta `egyéb` → `Furmint, Hárslevelű` |
| `BTY-X15542900320021` | szőlőfajta `egyéb` → `Furmint, Hárslevelű` |
| `BTY-X17218700320021` | szőlőfajta `egyéb` → `Chardonnay`; eredet `egyéb` → `Etyek-Buda`; édesség `brut, száraz` → `brut` |
| `BTY-X17221500320021` | szőlőfajta `egyéb` → `Glera`; eredet `Olaszország, Treviso` → `Treviso` |
| `BTY-X17404900320021` | szőlőfajta `egyéb` → `Furmint`; eredet `egyéb` → `Balatonboglár` |
| `BTY-X17584200320021` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |

### 100. köteg – Pezsgő, habzóbor és gyöngyözőbor 303–327.

- Ellenőrzött rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **24**.
- Helyi kép nélkül ellenőrzött rekord: **1** (`BTY-X18132900320021`).
- A Gancia Prosecco 0,2 literes pontos gyártói termékadata Glera szőlőből
  készült, olasz Prosecco DOC Brut Spumantét igazol. A Piper-Heidsieck Cuvée
  Brut hivatalos összetétele Pinot Noir, Meunier és Chardonnay házasítást, a
  termék neve és palackja Champagne eredetet és brut édességet igazol.
- A CHANDON Brut hivatalos termékadata Mendoza eredetet, valamint Chardonnay és
  Pinot Noir házasítást igazol; ezért a `Mendoza` elemi eredetértéket felvettük.
- A Szovjetszkoje Igrisztoje, Törley, Hungaria, BB és Natara tételeknél a pontos
  termékadatok és gyártói oldalak igazolták a magyar, Etyek-Buda,
  Balatonboglár, illetve Kunság eredetet. A Hungaria Rosé helyi címkéjén Extra
  Dry szerepel, ezért a tág `száraz` értéket `különlegesen száraz` értékre
  pontosítottuk.
- A Veuve Pelletier közvetlen palackcímkéje Champagne Brut Rosé besorolást
  igazol. Az alkoholtartalomra és a szőlőházasításra talált források nem
  egyeztek kellő bizonyossággal a pontos forrásváltozattal, ezért ezek
  `ismeretlen`, illetve `egyéb` értékét megtartottuk.
- A CA' ERNESTO közvetlen címkéje és pontos termékadata Veneto eredetű, Glera és
  Pinot Noir szőlőből készült Prosecco DOC Rosé Extra Dry Spumantét igazol. A
  BB Spumante Rosé gyártói termékoldala a spumante termékfajtát és
  Balatonboglár eredetet igazolja; bizonytalan szőlőfajta-adatot nem vettünk fel.
- A Martini és Gancia Prosecco Rosé pontos termékköre Glera–Pinot Noir
  házasítású olasz Prosecco DOC Spumante. A Gancia Rosé pontos gyártói oldala
  és a közvetlen első címke nem igazolt egyértelműen Brut vagy Extra Dry
  édességet, ezért a forrás szerinti `száraz` értéket nem írtuk felül.
- A Veuve Clicquot Rosé, Moët & Chandon Rosé Impérial és Mumm Grand Cordon
  Rosé hivatalos termékadatai Champagne eredetet, brut édességet, valamint
  Pinot Noir, Meunier és Chardonnay házasítást igazolnak. A Mumm rekord
  `brut` édessége már helyes volt, ezért az változatlan maradt.
- A Sauska Rosé Extra Brut hivatalos terméklapja Tokaj eredetet, Furmint,
  Hárslevelű és Pinot Noir házasítást; a Kreinbacher Rosé Brut hivatalos
  termékadata Somló eredetet, Furmint, Chardonnay, Pinot Blanc, Pinot Noir és
  Kékfrankos házasítást igazol.
- A Hungaria Rosé és a Sauska Rosé Extra Brut jelenlegi gyártói alkoholfoka
  eltér a felülvizsgált forrásrekord korábbi változatától. A változatkeverés
  elkerülésére mindkét rekord forrás szerinti alkoholfokát megtartottuk.
- A Törley Selection Rosé pontos termékadata 12,5%-os, Etyek-Buda eredetű
  pezsgőt igazol. A helyi kép nélküli Mionetto Prosecco Rosé pontos neve és
  hivatalos termékoldala 11%-os, Glera–Pinot Noir házasítású, olasz Prosecco
  DOC Millesimato Extra Dry Spumantét igazol; csak a közvetlenül bizonyított
  tulajdonságokat pontosítottuk.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **57**.
- Változatlanul hagyott rekord: **0**.
- Új megengedett érték: **1** (`eredet: Mendoza`).
- Törölt megengedett érték: **0**.
- Az 57 tervezett mezőmódosítást írás előtt összevetettük a teljes jelenlegi
  rekorddal. Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és a
  kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 25 írás sikeres volt,
  visszaállításra nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17584500320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; édesség `száraz` → `brut` |
| `BTY-X18117500320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `BTY-X18991800320021` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Mendoza` |
| `BTY-X2137200320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17175700320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17214600320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X13898000320021` | fajta `pezsgő` → `champagne`; eredet `egyéb` → `Champagne`; édesség `félszáraz` → `brut` |
| `BTY-X17600400320021` | fajta `pezsgő, spumante` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Veneto`; édesség `száraz` → `különlegesen száraz` |
| `BTY-X17412600320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X17217300320021` | fajta `pezsgő, spumante` → `spumante`; eredet `egyéb` → `Balatonboglár` |
| `BTY-X17214200320021` | eredet `egyéb` → `Etyek-Buda`; édesség `száraz` → `különlegesen száraz` |
| `BTY-X32355400320022` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17215900320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17218400320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17270700320021` | eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17455500320021` | eredet `egyéb` → `Kunság` |
| `BTY-X17474000320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `BTY-X17584800320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `BTY-X17656500320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `száraz` → `brut` |
| `BTY-X17862800320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `BTY-X17959300320021` | szőlőfajta `egyéb` → `Furmint, Hárslevelű, Pinot Noir`; eredet `egyéb` → `Tokaj` |
| `BTY-X18285900320021` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Blanc, Pinot Noir, Kékfrankos`; eredet `egyéb` → `Somló` |
| `BTY-X18415300320021` | alkoholtartalom `ismeretlen` → `12,5%`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X18132900320021` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `BTY-X17475800320021` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Chardonnay, Meunier`; eredet `egyéb` → `Champagne` |

### 101. köteg – Pezsgő, habzóbor és gyöngyözőbor 328–354., a már ellenőrzött 331–332. rekord nélkül.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A 331–332. pozíció két Voilá pezsgőkoktélját
  (`BTY-X17219100320021`, `BTY-X17219200320021`) egy korábbi kötegben már
  teljes rekorddal és képpel ellenőriztük. Ezeket nem számoltuk kétszer; a
  köteget a 353–354. pozíció két még nem vizsgált rekordjával egészítettük ki.
- A Sauska Rosé Brut hivatalos termékadata Tokaj eredetet, valamint Furmint,
  Pinot Noir és Chardonnay házasítást igazol. A Varga Rosé Édes pontos
  forrásváltozatához nem találtunk kellően biztos eredet- vagy
  szőlőfajta-adatot, ezért a jelenlegi értékeit megtartottuk.
- A Törley és BB alkoholmentes tételek közvetlen címkéi, gyártói oldalai és
  pontos termékadatai alkoholmentes habzó italt, magyar eredetet, a két fehér
  és rosé Törley terméknél pedig édes jelleget igazolnak. A 200 ml-es Törley
  címkéje külön az `ALKOHOLMENTES`, `ÉDES-SWEET` és fehér jelleget is
  közvetlenül mutatja.
- A Hungaria 0,0% közvetlen címkéje és pontos termékadata fehér, magyar
  alkoholmentes habzó italt igazol. Az Extra Dry megjelölést a kategóriafa
  következetes megfeleltetése szerint `különlegesen száraz` értékre
  pontosítottuk.
- A Mionetto 0,0% hivatalos termékadata Glera szőlőt, olasz eredetet és fehér
  alkoholmentes habzó italt igazol. A pontos La Gioiosa Et Amorosa 0,0%
  gyártói és termékadata Glera szőlőt, Veneto eredetet és fehér
  alkoholmentes habzó italt igazol; az édességi megnevezés nem volt elég
  egyértelmű, ezért ott az `egyéb` értéket megtartottuk.
- A Natara pontos termékadata Kunság eredetet, a Szovjetszkoje Igrisztoje
  tételek pontos termékköre és korábban ellenőrzött párhuzamai magyar
  eredetet igazolnak. A két Mon Amour tételnél nem egészítettünk ki bizonytalan
  szőlőfajta- vagy eredetadatot.
- A BB Spumante gyártói oldala a spumante termékfajtát, muskotályos jelleget
  és Balatonboglár eredetet igazol. A Feind Play pontos termékadata Cserszegi
  fűszeres szőlőből készült dunántúli száraz fehér gyöngyözőbort igazol.
- A Törley Charmant Rosé, Gála Sec, Charmant Doux és Muscateller pontos
  termékadatai, valamint a korábban kézzel ellenőrzött azonos termékpárhuzamok
  Etyek-Buda eredetet igazolnak. A 0,2 literes Charmant Rosé címkéje az
  alkoholfokot is igazolja.
- A Cinzano To-Spritz közvetlen címkéje `VINO SPUMANTE` megjelölést mutat, a
  pontos termékadat pedig Glera és Garganega szőlőt, valamint Veneto eredetet
  igazol. A `Garganega` elemi szőlőfajtaértéket ezért felvettük.
- Módosított rekord: **22**.
- Módosított tulajdonságmező: **40**.
- Változatlanul hagyott rekord: **3** (`BTY-X18337100320021`, `1012971`,
  `1012972`).
- Új megengedett érték: **1** (`szőlőfajta: Garganega`).
- Törölt megengedett érték: **0**.
- A 40 egyedi mezőmódosítást írás előtt összevetettük a teljes jelenlegi
  rekorddal. Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és a
  kategóriahash-eket vizsgáló teljes ellenőrzés; minden írás sikeres volt,
  visszaállításra nem volt szükség. A Hungaria édességét a záró
  forrás-újraellenőrzés az általános `száraz` helyett a pontos
  `különlegesen száraz` értékre finomította.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17921300320021` | szőlőfajta `egyéb` → `Furmint, Pinot Noir, Chardonnay`; eredet `egyéb` → `Tokaj` |
| `BTY-X8944700320021` | alkoholtartalom `ismeretlen` → `11%`; eredet `egyéb` → `Etyek-Buda` |
| `BTY-X17216800320021` | édesség `egyéb` → `édes`; eredet `egyéb` → `Magyarország` |
| `BTY-X17216400320021` | eredet `egyéb` → `Magyarország` |
| `BTY-X18133000320021` | édesség `egyéb` → `különlegesen száraz`; eredet `egyéb` → `Magyarország` |
| `BTY-X17216900320021` | édesség `egyéb` → `édes`; eredet `egyéb` → `Magyarország` |
| `BTY-X17217800320021` | fajta `habzóbor` → `alkoholmentes habzó ital`; édesség `egyéb` → `édes`; eredet `egyéb` → `Magyarország`; szín `egyéb` → `fehér` |
| `BTY-X17685400320021` | fajta `habzóbor` → `alkoholmentes habzó ital`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; édesség `édes` → `száraz` |
| `BTY-X17685600320021` | fajta `habzóbor` → `alkoholmentes habzó ital`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto`; szín `egyéb` → `fehér` |
| `1023399` | eredet `egyéb` → `Kunság` |
| `995744` | eredet `egyéb` → `Magyarország` |
| `1001762` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `995749` | eredet `egyéb` → `Magyarország` |
| `995767` | eredet `egyéb` → `Magyarország` |
| `1023400` | eredet `egyéb` → `Magyarország` |
| `1023401` | eredet `egyéb` → `Magyarország` |
| `1040546` | szőlőfajta `egyéb` → `Cserszegi fűszeres` |
| `1000667` | eredet `egyéb` → `Etyek-Buda` |
| `1000669` | eredet `egyéb` → `Etyek-Buda` |
| `1010096` | eredet `egyéb` → `Etyek-Buda` |
| `1010097` | eredet `egyéb` → `Etyek-Buda` |
| `997270` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Glera, Garganega`; eredet `egyéb` → `Veneto` |

### 102. köteg – Pezsgő, habzóbor és gyöngyözőbor 355–380., a már ellenőrzött 374. rekord nélkül.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A 374. pozíció `0e347f2fca390c62e117c325` azonosítójú rekordját egy
  korábbi kötegben már teljes rekorddal és képpel ellenőriztük. Ezt nem
  számoltuk kétszer; a köteget a 380. pozíció még nem vizsgált rekordjával
  egészítettük ki.
- A Hungaria Extra Dry 0,75 és 0,2 literes változatának pontos termékadata
  Chardonnay, Királyleányka és Pinot Noir házasítást, valamint Etyek-Buda
  eredetet igazol. A Grande Cuvée ugyanezt a házasítást és eredetet, az Irsai
  Olivér Doux pedig Irsai Olivér szőlőt és Etyek-Buda eredetet igazol.
- A Gancia Prosecco pontos bolti párhuzamai és termékadata Glera szőlőből
  készült olasz Prosecco Spumantét igazol. A Martini Asti közvetlen címkéje és
  hivatalos termékadata Moscato Bianco szőlőből készült Asti Spumantét igazol.
- A Törley Gála, Charmant Rouge, Talisman és Muscateller pontos
  termékpárhuzamai Etyek-Buda eredetet igazolnak. A Fortuna hivatalos
  termékadata Irsai Olivér, Muscat Lunel, Muscat Ottonel és Rizlingszilváni
  házasítást, valamint Etyek-Buda eredetet igazol.
- A Tokaji Doux jelenlegi termékfajtája, Tokaj eredete, édessége, színe és
  alkoholfoka helyes. A pontos változathoz nem találtunk kellően biztos
  szőlőházasítási adatot, ezért a rekordot változatlanul hagytuk.
- A Mionetto Treviso Frizzante pontos termékadata Glera szőlőt és az egyetlen,
  elemi Treviso eredetet igazol. A Treviso Brut Glera szőlőből készült
  Prosecco Spumante; a már helyes brut, fehér és Treviso értékeket
  megtartottuk.
- A BB Spumante fehér termék neve, címkéje és pontos termékadata spumante
  termékfajtát, Muskotály szőlőt és Balatonboglár eredetet igazol. A Spumante
  Rosé pontos termékadata a spumante fajtát és Balatonboglár eredetet
  igazolja; bizonytalan szőlőfajtát nem rögzítettünk.
- A BB édes, félszáraz fehér, félszáraz rosé, száraz, Arany Cuvée és Ezüst
  Cuvée pontos termékadatai Balatonboglár eredetet igazolnak. Az Arany Cuvée
  gyártói leírása emellett Muskotály szőlőt igazol; a kóstolási jegyeket egyik
  BB tételnél sem kezeltük hozzáadott ízként.
- A Törley alkoholmentes 0,75 literes rekord közvetlen képe kizárólag a rosé
  változatot mutatja. Ezért a kettős fehér–rosé színt `rozé` értékre
  szűkítettük, a fajtát `alkoholmentes habzó ital` értékre pontosítottuk, és a
  magyar eredetet rögzítettük.
- A François President Brut pontos szakmai termékadata Chardonnay és Pinot
  Noir házasítást, valamint Etyek-Buda eredetet igazol.
- Módosított rekord: **24**.
- Módosított tulajdonságmező: **41**.
- Változatlanul hagyott rekord: **1** (`4ad63fd42f375dbea627a67c`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 41 tervezett mezőmódosítást írás előtt összevetettük a teljes jelenlegi
  rekorddal. Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és a
  kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 24 írás sikeres volt,
  visszaállításra nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1019793` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `72442c0cd26f9b61b372c134` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `a082eae27fce8661afbba3ff` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `636bd40de828a77c13cf0cdd` | eredet `egyéb` → `Etyek-Buda` |
| `5f2e67c346cd44c46f1d6a81` | eredet `egyéb` → `Etyek-Buda` |
| `7d8f4000727b8deb7081121e` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `3fdb8ba6e044c863f57b36e8` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `da72e49a8edd49e16f71d693` | szőlőfajta `egyéb` → `Glera`; eredet `Olaszország, Treviso` → `Treviso` |
| `cdf1af0769cb1cadfcfd4312` | eredet `egyéb` → `Etyek-Buda` |
| `2c818427e99447549bc7f958` | eredet `egyéb` → `Balatonboglár` |
| `b10819a1b4367dd28c95e1ed` | eredet `egyéb` → `Etyek-Buda` |
| `73d1846b8404221910280bc7` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `dae0643910a95be92bc9ce42` | szőlőfajta `egyéb` → `Irsai Olivér, Muscat Lunel, Muscat Ottonel, Rizlingszilváni`; eredet `egyéb` → `Etyek-Buda` |
| `99cc8cb3d448a0e1fba57be6` | eredet `egyéb` → `Etyek-Buda` |
| `3c0af3dd2de97fcc0e8deea4` | eredet `egyéb` → `Balatonboglár` |
| `d8e98259322f184a40a3c30a` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera` |
| `f8b4b4d17d222efb02331140` | eredet `egyéb` → `Balatonboglár` |
| `5ef2807c8213be52072313e1` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Balatonboglár` |
| `346e0aa856d5cb89c3cc4e62` | eredet `egyéb` → `Etyek-Buda` |
| `a3065f9c797840403d6a020c` | szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `c533dd613097cd88f4def65c` | eredet `egyéb` → `Balatonboglár` |
| `259c89ac2315d57c4691b09d` | eredet `egyéb` → `Balatonboglár` |
| `b72446833006b099998578f3` | fajta `habzóbor` → `alkoholmentes habzó ital`; eredet `egyéb` → `Magyarország`; szín `fehér, rozé` → `rozé` |
| `864af3276912a410c3c67eb1` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |

### 103. köteg – Pezsgő, habzóbor és gyöngyözőbor 381–405.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Henkell Blanc de Blancs pontos gyártói e-címkéje, a Henkell Trocken
  gyártói termékadata és az azonos, korábban kézzel ellenőrzött
  termékpárhuzamok mindhárom rekordnál Németország eredetet igazolnak. A Blanc
  de Blancs pontos forrásváltozatához nem közöltek egyértelmű szőlőfajtát,
  ezért az `egyéb` értéket megtartottuk.
- A két Hungaria Extra Dry és a Grande Cuvée pontos termékadata Chardonnay,
  Királyleányka és Pinot Noir házasítást, valamint Etyek-Buda eredetet igazol.
  A Rouge Demi Sec és a Hungaria Rosé pontos párhuzamai Etyek-Buda eredetet
  igazolnak; bizonytalan szőlőházasítást nem rögzítettünk.
- A Törley Charmant Doux, Charmant Rosé, Excellence Sárgamuskotály,
  Excellence Chardonnay és a két Ice Pink pontos termékadata Etyek-Buda
  eredetet igazol. A Muscosecco Cserszegi fűszeres és Irsai Olivér
  házasítású, Etyek-Buda eredetű tétel.
- A két Ice White Edition neve, közvetlen képe, alkoholfoka, édessége és színe
  összhangban van. A pontos forrásváltozathoz nem találtunk kellően biztos
  eredet- vagy szőlőfajta-adatot, ezért mindkét rekordot változatlanul
  hagytuk.
- A Gancia Asti közvetlen címkéje és pontos termékadata Moscato Bianco
  szőlőből készült Asti Spumantét igazol. A Gancia Brut gyártói lapja olasz
  Spumantét, valamint a `brut` édességet igazol; a redundáns `száraz` értéket
  eltávolítottuk. A gyártói lap nem részletezi a felhasznált alkalmas
  szőlőfajtákat, ezért a szőlőfajta `egyéb` maradt.
- A BB alkoholmentes ital neve, közvetlen címkéje és pontos termékadata
  alkoholmentes, édes, fehér habzó italt és magyar eredetet igazol. A
  kóstolási leírást nem kezeltük hozzáadott ízként.
- Az Etyeki Kúria Pláne Frizzante White pontos termékadata Királyleányka és
  Zenit házasítást igazol. A két Bubik rekord neve és közvetlen címkéje a
  jelenlegi gyöngyözőbor-fajtát, édességet, színt és a Felső-Magyarország,
  illetve Dunántúl eredetet közvetlenül alátámasztja; bizonytalan
  szőlőfajtát nem következtettünk hozzájuk, így változatlanok maradtak.
- A Natara száraz fehér és rosé pontos termékpárhuzamai Kunság eredetet
  igazolnak.
- Módosított rekord: **21**.
- Módosított tulajdonságmező: **29**.
- Változatlanul hagyott rekord: **4** (`4a33c89eed3d0166141b2ac2`,
  `788833363e96f8ac3f4846af`, `72037c80c47ef790ffb5f267`,
  `7cc5b6193f916fe7b61d3731`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Az első száraz tervellenőrzés egy összetömörített PowerShell `foreach`
  kifejezés kötelező szóközének hiánya miatt még adatolvasás vagy írás előtt
  leállt. Az ugyanazt a tervet vizsgáló olvasásos ellenőrzés ezután 21
  rekordot és 29 mezőt igazolt.
- Mind a 29 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 21 írás sikeres volt, visszaállításra nem
  volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `241f351348de9cd9d787d158` | eredet `egyéb` → `Németország` |
| `fb7a8b41ed135feb2e7eaa4b` | eredet `egyéb` → `Németország` |
| `362cd2f0b6bcd4de3549a68a` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `4893d34bc8b528256a193634` | eredet `egyéb` → `Etyek-Buda` |
| `31de7b700c4365fbaa849d52` | eredet `egyéb` → `Etyek-Buda` |
| `bc8b0af8c0649cd7fde2f70c` | eredet `egyéb` → `Etyek-Buda` |
| `5ae9cc5057ba88157adc7120` | eredet `egyéb` → `Etyek-Buda` |
| `1bc6054dbe35efb238a35be5` | eredet `egyéb` → `Etyek-Buda` |
| `551c5a4e4c6f15f05c6cb4a4` | eredet `egyéb` → `Etyek-Buda` |
| `99ebfd1029cd828e06451210` | szőlőfajta `egyéb` → `Cserszegi fűszeres, Irsai Olivér`; eredet `egyéb` → `Etyek-Buda` |
| `8f0b8e33a928afaa285461a2` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `9631eae850744264da386cc4` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Olaszország`; édesség `brut, száraz` → `brut` |
| `3da49df048784b8aafdd62d7` | eredet `egyéb` → `Magyarország` |
| `06ca90beed99c3bfddb99aae` | eredet `egyéb` → `Etyek-Buda` |
| `a0114c5013a72a5921e566ce` | szőlőfajta `egyéb` → `Királyleányka, Zenit` |
| `4a7b82ef712374aff7195421` | eredet `egyéb` → `Etyek-Buda` |
| `745e841458ea826ebe4809fd` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `1e55c770542d7babb87761f4` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `b4e39de98ec3b1a044c7d685` | eredet `egyéb` → `Németország` |
| `2ff222020db9846faf4e5aae` | eredet `egyéb` → `Kunság` |
| `c0d091d7b7fe25668f901cc1` | eredet `egyéb` → `Kunság` |

### 104. köteg – Pezsgő, habzóbor és gyöngyözőbor 406–430.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Mionetto Prosecco Rosé DOC Millesimato Extra Dry közvetlen címkéje és
  pontos termékadata Glera–Pinot Noir házasítású, olasz Prosecco DOC
  Spumantét igazol. A Mionetto Prosecco DOC Treviso Brut és a Cinzano
  Prosecco DOC pontos, korábban kézzel ellenőrzött termékpárhuzama Glera
  szőlőből készült `spumante, prosecco` besorolást, valamint Treviso, illetve
  Olaszország eredetet igazol.
- A Cinzano To-Spritz közvetlen címkéje `VINO SPUMANTE` megjelölést mutat; a
  pontos termékadat Glera és Garganega szőlőt, valamint Veneto eredetet
  igazol.
- A Kreinbacher Extra Dry pontos termékadata és gyártói oldala Furmint,
  Chardonnay, Pinot Noir és Pinot Blanc házasítást, valamint Somló eredetet
  igazol. A Sauska Brut pontos termelői és szakmai adata Furmint,
  Chardonnay és Pinot Noir házasítást, Tokaj eredetet és brut édességet
  közöl; a `brut` mellett redundáns `száraz` értéket eltávolítottuk.
- A Louis François & Co. Brut Nature közvetlen függőcímkéje a
  `Louis François & Co.` márkanevet mutatja, pontos termékadata pedig
  Chardonnay–Pinot Noir házasítást igazol. A névben szereplő és már helyesen
  rögzített Etyek-Buda eredetet megtartottuk.
- A Törley Gála, Excellence Sárgamuskotály, Excellence Chardonnay,
  Talisman, Muscateller, Gála Sec, Charmant Rouge, Charmant Rosé és Charmant
  Doux pontos termékadatai és a korábban kézzel ellenőrzött azonos
  termékpárhuzamok Etyek-Buda eredetet igazolnak. A Fortuna hivatalos
  termékadata Irsai Olivér, Muscat Lunel, Muscat Ottonel és Rizlingszilváni
  házasítást, valamint Etyek-Buda eredetet közöl.
- A BB Spumante Rosé pontos termékadata a spumante fajtát és Balatonboglár
  eredetet igazolja; bizonytalan szőlőfajtát nem rögzítettünk. A BB Spumante
  fehér termék neve, címkéje és pontos termékadata a spumante fajtát,
  Muskotály szőlőt és Balatonboglár eredetet igazol. A BB száraz fehér,
  félszáraz fehér, félszáraz rosé és édes fehér pezsgők pontos
  termékadatai szintén Balatonboglár eredetet igazolnak.
- A Hungaria Rosé pontos termékpárhuzama Etyek-Buda eredetet igazol. A
  0,2 literes Hungaria Extra Dry az azonos 0,75 literes termékkel egyezően
  Chardonnay, Királyleányka és Pinot Noir házasítású, Etyek-Buda eredetű
  pezsgő.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **41**.
- Változatlanul hagyott rekord: **0**.
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Az első alkalmazási kísérlet a Windows CRLF sorvég miatt a hash-sor
  illesztésénél még az első tartalmi írás előtt leállt; az eredeti fájl
  változatlan tartalommal került vissza. A javított futás első 10 rekordja
  sikeresen átment a teljes köztes validáción, majd a 11. rekord skalár
  márkamezőjénél a sorvégi vessző megőrzését vizsgáló JSON-ellenőrzés
  megállította az írást. A 11. rekord visszaállt, az első 10 validált
  módosítás megmaradt. Az idempotens, vesszőt megőrző folytatás ezután mind
  a 25 rekordot újra ellenőrizte és sikeresen lezárta.
- Mind a 41 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; a végállapotban minden tervezett érték pontosan
  visszaolvasható.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `783575ae51a77565e7d9322d` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `fccbe9b52eca104f9cc94dae` | eredet `egyéb` → `Etyek-Buda` |
| `2d677e4dd3e970bc258a9252` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir, Pinot Blanc`; eredet `egyéb` → `Somló` |
| `3a816aa63f8ed1132fef588e` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Glera, Garganega`; eredet `egyéb` → `Veneto` |
| `7b868fee5a2845821831b382` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj`; édesség `brut, száraz` → `brut` |
| `06dd52310517785ea5b460a5` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `df12c553b47e1c075ad79b06` | eredet `egyéb` → `Etyek-Buda` |
| `4e35e1271259d8a44c58eb72` | eredet `egyéb` → `Etyek-Buda` |
| `5c8eeb4996bc848e3eb4e870` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Balatonboglár` |
| `c2d6c37666ade8b99686db76` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera` |
| `1a0dec4f0624bbeb102477c6` | márka `Francois Louis François & Co.` → `Louis François & Co.`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir` |
| `39f5b42211b4b14e368ffdf5` | eredet `egyéb` → `Balatonboglár` |
| `9bbc2a77b4afcdb4b92f50e3` | eredet `egyéb` → `Etyek-Buda` |
| `37105fb2167a4195ea5a577d` | eredet `egyéb` → `Etyek-Buda` |
| `b865f54cabdb91ffd9a03b8f` | eredet `egyéb` → `Etyek-Buda` |
| `7e07bf7e1638d5a66ae8d1a3` | szőlőfajta `egyéb` → `Irsai Olivér, Muscat Lunel, Muscat Ottonel, Rizlingszilváni`; eredet `egyéb` → `Etyek-Buda` |
| `9ba768fed4cb6301e5cc8f22` | eredet `egyéb` → `Etyek-Buda` |
| `e930775beb6cac26b79e30fb` | eredet `egyéb` → `Etyek-Buda` |
| `457538a96c43912b10e7f23d` | eredet `egyéb` → `Etyek-Buda` |
| `e0c3a05d473dbe63409936d8` | eredet `egyéb` → `Balatonboglár` |
| `2f29eba7916eb99fd6644782` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `38906a93282190ae8908f602` | eredet `egyéb` → `Balatonboglár` |
| `d7a387ff0f3a96891208f849` | eredet `egyéb` → `Balatonboglár` |
| `799d87bf6a415bef96c96ab9` | eredet `egyéb` → `Etyek-Buda` |
| `81f7b6aa334f677a05bbddd7` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |

### 105. köteg – Pezsgő, habzóbor és gyöngyözőbor 431–455.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Cinzano Asti és a Martini Asti közvetlen címkéje, valamint pontos
  termékadata Moscato Bianco szőlőből készült Asti Spumantét igazol.
- A Juhász Eufória pontos termékadata Chardonnay, Rizlingszilváni és Zenit
  házasítást közöl. Egyértelmű, pontos eredetadatot nem találtunk, ezért az
  eredet `egyéb` maradt.
- A Zonin Prosecco 1821 pontos termékadata Glera szőlőből készült, venetói
  Prosecco DOC Spumantét igazol. Az I Heart Prosecco neve, közvetlen címkéje
  és pontos termékadata Glera szőlőből készült, fehér gyöngyözőbor–prosecco
  besorolást igazol.
- A Garamvári Classic Brut pontos termékadata Chardonnay, Furmint és Pinot
  Blanc házasítást, valamint Balatonboglár eredetet közöl. A Sauska Rosé
  Brut pontos termelői és szakmai adata Furmint, Pinot Noir és Chardonnay
  házasítást, Tokaj eredetet és brut édességet igazol; a `brut` mellett
  redundáns `száraz` értéket eltávolítottuk.
- A Martini Prosecco pontos termékadata Glera szőlőből készült, olasz,
  fehér Prosecco DOC Spumantét igazol. A Martini Brut pontos termékadata
  Chardonnay–Glera házasítású, olasz Spumantét és brut édességet közöl; a
  redundáns `száraz` értéket eltávolítottuk.
- A Codorníu Raventós Cuvée pontos termékadata Chardonnay, Macabeo és
  Xarel-lo szőlőből készült spanyol cavát, a Freixenet Cordon Negro pedig
  Parellada, Macabeo és Xarel-lo szőlőből készült spanyol cavát igazol.
- A Moët & Chandon Brut Impérial pontos gyártói termékadata Pinot Noir,
  Meunier és Chardonnay házasítású Champagne-t és brut édességet igazol. A
  redundáns `pezsgő` fajtát és `száraz` édességet eltávolítottuk.
- A Natara édes fehér pontos termékpárhuzama Kunság eredetet igazol. A
  Hungaria Irsai Olivér pontos termékadata Etyek-Buda eredetet, a Törley
  Muscosecco pedig Cserszegi fűszeres–Irsai Olivér házasítást és Etyek-Buda
  eredetet közöl.
- A négy Bohém-változat közvetlen címkéje és pontos SPAR-termékadata magyar
  pezsgőt igazol. Ennél pontosabb borvidéket nem következtettünk, ezért az
  eredet `Magyarország` lett.
- A Törley Charmant Doux, Selection Rosé Sec és Selection Brut pontos
  termékadata Etyek-Buda eredetet igazol. A Rosé Sec és Brut pontos
  szőlőházasítása nem volt kellően bizonyítható, ezért a szőlőfajta `egyéb`
  maradt.
- A Juhász Cserszegi fűszeres és rosé gyöngyözőbor, valamint a BB Frizzante
  neve, közvetlen képe és pontos termékadata összhangban van a jelenlegi
  kategóriával és tulajdonságokkal; mindhárom rekord változatlan maradt.
- Módosított rekord: **22**.
- Módosított tulajdonságmező: **46**.
- Változatlanul hagyott rekord: **3** (`04e78b6fb493dfb49a9ece13`,
  `0542051b527f68f253efce66`, `0dc123af3808da4e3388b326`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 46 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 22 írás sikeres volt, visszaállításra
  nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `f0de77264dfe00646293b756` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `d0e28548b8c39b8626e4f7b4` | szőlőfajta `egyéb` → `Chardonnay, Rizlingszilváni, Zenit` |
| `e611a5541c7b761589e4b922` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Veneto` |
| `1c20ef526df4c6516f8a004b` | szőlőfajta `egyéb` → `Chardonnay, Furmint, Pinot Blanc`; eredet `egyéb` → `Balatonboglár` |
| `4a98fb5447daa558c40020e6` | szőlőfajta `egyéb` → `Glera`; szín `fehér, rozé` → `fehér` |
| `42f5346f93a4474d43bae86c` | szőlőfajta `egyéb` → `Furmint, Pinot Noir, Chardonnay`; eredet `egyéb` → `Tokaj`; édesség `brut, száraz` → `brut` |
| `0eddd7826faca2b6c1a0ce87` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; szín `fehér, rozé` → `fehér` |
| `8aa8fef23f1a15ac663aa3f4` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Chardonnay, Glera`; eredet `egyéb` → `Olaszország`; édesség `brut, száraz` → `brut` |
| `4a619931a1a81189f054326b` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `bf95f13ce7af4a768622ee43` | fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Chardonnay, Macabeo, Xarel-lo`; eredet `egyéb` → `Spanyolország` |
| `8c5b21d6badfa2a609ff48c6` | eredet `egyéb` → `Kunság` |
| `a2a05ada2f0406264a800f33` | fajta `pezsgő` → `cava`; szőlőfajta `egyéb` → `Parellada, Macabeo, Xarel-lo`; eredet `egyéb` → `Spanyolország` |
| `34818377b3df3c643741b96b` | fajta `pezsgő, champagne` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `40c0d5fa6141be1171dd1a81` | eredet `egyéb` → `Etyek-Buda` |
| `ef6acf9d129d0a3a70c38330` | szőlőfajta `egyéb` → `Cserszegi fűszeres, Irsai Olivér`; eredet `egyéb` → `Etyek-Buda` |
| `79a4b7c8ed6ad86eac0e8ce1` | eredet `egyéb` → `Magyarország` |
| `08ca955e800e945ca34103d0` | eredet `egyéb` → `Magyarország` |
| `88a80032b807975dfe008a34` | eredet `egyéb` → `Magyarország` |
| `cf7501423704d6bebb2f26ef` | eredet `egyéb` → `Magyarország` |
| `fe015d4a3073e69766a4943f` | eredet `egyéb` → `Etyek-Buda` |
| `af641904ab32bcd2362a3e9a` | eredet `egyéb` → `Etyek-Buda` |
| `b4bb03b24ed0901f02afe02c` | eredet `egyéb` → `Etyek-Buda` |

### 106. köteg – Pezsgő, habzóbor és gyöngyözőbor 456–482.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A 459. és 460. pozíció `b1308215df1f6d72e589687e`, illetve
  `08236700e19e620091cb016a` azonosítójú Voilá rekordját korábbi kötegben már
  teljes rekorddal és képpel ellenőriztük. Ezeket nem számoltuk kétszer; a
  köteget a 481. és 482. pozíció még nem vizsgált rekordjaival egészítettük
  ki.
- A Törley Extra Sec pontos termékpárhuzama Etyek-Buda eredetet igazol. A
  Gancia Prosecco hivatalos termékadata Glera szőlőből készült, olasz
  Prosecco DOC Spumantét, a Gancia Astié Moscato Bianco szőlőből készült Asti
  Spumantét igazol.
- A három Tesco Finest fehér Prosecco DOC pontos gyártói termékadata Glera,
  Chardonnay, Pinot Blanc és Pinot Grigio házasítást, olasz eredetet és fehér
  színt közöl. A 0,2 literes adatlap a Pinot Grigio szinonimáját, a `Pinot
  Gris` alakot használja; ezt az egységes, újonnan engedélyezett `Pinot
  Grigio` értékre normalizáltuk. A rosé változat pontos adata Glera–Pinot Noir
  házasítást és olasz eredetet igazol. Mind a négy termék Prosecco DOC
  Spumante.
- A Tesco Finest Premier Cru Brut pontos gyártói termékadata Chardonnay és
  Pinot Noir szőlőből készült, fehér Champagne-t igazol. A Tesco Finest
  Valdobbiadene Prosecco Superiore DOCG pontos termékadata Glera–Chardonnay
  házasítást, Valdobbiadene eredetet, fehér színt és Spumante–Prosecco
  besorolást igazol.
- A Martini Asti pontos termékadata Moscato Bianco szőlőből készült Asti
  Spumantét igazol. A Hungaria Extra Dry Chardonnay, Királyleányka és Pinot
  Noir házasítású, Etyek-Buda eredetű pezsgő.
- A Törley Fortuna pontos termékadata Irsai Olivér, Muscat Lunel, Muscat
  Ottonel és Rizlingszilváni házasítást, valamint Etyek-Buda eredetet közöl.
  A Gála Sec, Charmant Doux, Muscateller, Talisman és Ice Pink pontos
  termékpárhuzamai szintén Etyek-Buda eredetet igazolnak.
- A BB Spumante közvetlen címkéje és pontos termékadata Muskotály szőlőből
  készült, balatonboglári Spumantét igazol. A BB alkoholmentes fehér
  szénsavas ital pontos termékpárhuzama magyar eredetet igazol; az
  ízesítést a forrás nem részletezi, ezért bizonytalan ízértéket nem
  rögzítettünk.
- A négy Törley alkoholmentes rekord közvetlen képei két fehér és két rosé,
  édes, alkoholmentes habzó italt mutatnak. A fajtát pontosítottuk, a színt
  képenként rögzítettük, és a magyar eredetet az azonos pontos
  termékpárhuzamok alapján adtuk meg.
- A Szovjetszkoje Igrisztoje száraz fehér és Muskotály édes fehér pontos
  termékadata magyar eredetet igazol. A Muskotály szőlőfajta már helyesen
  szerepelt; a száraz változatnál bizonytalan szőlőfajtát nem
  következtettünk.
- Módosított rekord: **25**.
- Módosított tulajdonságmező: **60**.
- Változatlanul hagyott új rekord: **0**.
- Új megengedett érték: **1** (`szőlőfajta: Pinot Grigio`).
- Törölt megengedett érték: **0**.
- A 60 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 25 írás sikeres volt, visszaállításra
  nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `978765ffa4c06b7254130475` | eredet `egyéb` → `Etyek-Buda` |
| `a6b9cca67dfff7f6b563f09c` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `06262b6b62aeb8cbdc128054` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `06d8d0a0aa0ea9d14c074152` | fajta `habzóbor` → `alkoholmentes habzó ital`; eredet `egyéb` → `Magyarország`; szín `fehér, rozé` → `rozé` |
| `25cc4f8417c231a63615a2d2` | fajta `habzóbor` → `alkoholmentes habzó ital`; eredet `egyéb` → `Magyarország`; édesség `egyéb` → `édes`; szín `egyéb` → `fehér` |
| `121237129` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Chardonnay, Pinot Blanc, Pinot Grigio`; eredet `egyéb` → `Olaszország` |
| `121279471` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Chardonnay, Pinot Blanc, Pinot Grigio`; eredet `egyéb` → `Olaszország`; szín `rozé` → `fehér` |
| `121237135` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `121279488` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Chardonnay, Pinot Blanc, Pinot Grigio`; eredet `egyéb` → `Olaszország`; szín `rozé` → `fehér` |
| `121286116` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Champagne`; szín `egyéb` → `fehér` |
| `121237141` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Chardonnay`; eredet `egyéb` → `Valdobbiadene`; szín `rozé` → `fehér` |
| `121218302` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `121222066` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `121222055` | fajta `habzóbor` → `alkoholmentes habzó ital`; eredet `egyéb` → `Magyarország`; szín `fehér, rozé` → `fehér` |
| `121221960` | szőlőfajta `egyéb` → `Irsai Olivér, Muscat Lunel, Muscat Ottonel, Rizlingszilváni`; eredet `egyéb` → `Etyek-Buda` |
| `121221983` | eredet `egyéb` → `Etyek-Buda` |
| `121221977` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `121221948` | eredet `egyéb` → `Etyek-Buda` |
| `121222141` | fajta `habzóbor` → `alkoholmentes habzó ital`; eredet `egyéb` → `Magyarország`; szín `fehér, rozé` → `rozé` |
| `121222204` | eredet `egyéb` → `Magyarország` |
| `121221954` | eredet `egyéb` → `Etyek-Buda` |
| `121230321` | eredet `egyéb` → `Magyarország` |
| `121230315` | eredet `egyéb` → `Magyarország` |
| `121222008` | eredet `egyéb` → `Etyek-Buda` |
| `121259305` | eredet `egyéb` → `Etyek-Buda` |

### 107. köteg – Pezsgő, habzóbor és gyöngyözőbor 483–508.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A 499. pozíció `121222291` azonosítójú Voilá áfonya rekordját korábbi
  kötegben már teljes rekorddal és képpel ellenőriztük. Ezt nem számoltuk
  kétszer; a köteget az 508. pozíció még nem vizsgált rekordjával
  egészítettük ki.
- A Szovjetszkoje Igrisztoje édes fehér, Extra Dry fehér és félszáraz rosé
  pontos termékadata magyar eredetet igazol. Bizonytalan szőlőfajtát egyik
  változathoz sem következtettünk.
- A Törley Muscosecco pontos termékadata Cserszegi fűszeres és Irsai Olivér
  házasítást, valamint Etyek-Buda eredetet közöl. A Charmant Rosé, Charmant
  Doux, Charmant Rouge, Excellence Sárgamuskotály és Excellence Chardonnay
  pontos termékpárhuzamai szintén Etyek-Buda eredetet igazolnak.
- A BB száraz fehér, félszáraz fehér, édes fehér és félszáraz rosé pontos
  termékadata Balatonboglár eredetet igazol. A BB Spumante Rosé pontos
  termékadata a spumante fajtát és Balatonboglár eredetet közöl; bizonytalan
  szőlőfajtát nem rögzítettünk.
- A Juhász Felső-Magyarországi rosé gyöngyözőbor teljes rekordja és közvetlen
  képe megegyezik a korábban kézzel ellenőrzött azonos termékpárhuzamokkal;
  változtatás nem indokolt.
- A Törley Ice White Edition pontos forrásváltozatához továbbra sem találtunk
  kellően biztos szőlőfajta- vagy eredetadatot, ezért a névvel, képpel,
  alkoholfokkal, édességgel és színnel összhangban lévő rekordot
  változatlanul hagytuk. A Törley Tokaji Doux jelenlegi Tokaj eredete és
  többi bizonyítható tulajdonsága szintén helyes.
- A Varga Irsai Olivér Bubis neve, közvetlen címkéje és teljes forrásadata
  összhangban van a jelenlegi gyöngyözőbor-fajtával, Irsai Olivér
  szőlőfajtával, Balaton eredettel, száraz édességgel és fehér színnel;
  változatlan maradt.
- A Martini Brut pontos termékadata Chardonnay–Glera házasítású, olasz
  Spumantét és brut édességet igazol; a redundáns `száraz` értéket
  eltávolítottuk.
- A Hungaria Rosé pontos termékpárhuzama Etyek-Buda eredetet igazol. A
  Hungaria Grande Cuvée Brut pontos termékadata Chardonnay, Királyleányka és
  Pinot Noir házasítást, valamint Etyek-Buda eredetet közöl.
- A Cinzano Asti pontos termékadata Moscato Bianco szőlőből készült Asti
  Spumantét igazol. A Cinzano To Spritz közvetlen címkéje és pontos
  termékadata Glera–Garganega házasítású, venetói Spumantét igazol.
- A Bella Cucina Demi-Sec pontos Tesco-termékadata olasz eredetű, fehér,
  félszáraz gyöngyözőbort igazol. A termékhez nem közöl egyértelmű
  szőlőfajtát, ezért a szőlőfajta `egyéb` maradt.
- A Mionetto Prosecco DOC Treviso Brut pontos termékadata Glera szőlőből
  készült Prosecco Spumantét igazol; a már helyes Treviso eredetet, brut
  édességet és fehér színt megtartottuk.
- Módosított rekord: **21**.
- Módosított tulajdonságmező: **32**.
- Változatlanul hagyott rekord: **4** (`121236015`, `121222884`,
  `120476890`, `121222976`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 32 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 21 írás sikeres volt, visszaállításra
  nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121230177` | eredet `egyéb` → `Magyarország` |
| `121222112` | szőlőfajta `egyéb` → `Cserszegi fűszeres, Irsai Olivér`; eredet `egyéb` → `Etyek-Buda` |
| `121222918` | eredet `egyéb` → `Balatonboglár` |
| `121222014` | eredet `egyéb` → `Etyek-Buda` |
| `121222383` | eredet `egyéb` → `Balatonboglár` |
| `121222354` | eredet `egyéb` → `Balatonboglár` |
| `121230373` | eredet `egyéb` → `Magyarország` |
| `121222095` | eredet `egyéb` → `Etyek-Buda` |
| `121222129` | eredet `egyéb` → `Etyek-Buda` |
| `121218360` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Chardonnay, Glera`; eredet `egyéb` → `Olaszország`; édesség `brut, száraz` → `brut` |
| `121222763` | eredet `egyéb` → `Etyek-Buda` |
| `121222849` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `121230338` | eredet `egyéb` → `Magyarország` |
| `121222348` | eredet `egyéb` → `Etyek-Buda` |
| `121234069` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `121222982` | eredet `egyéb` → `Balatonboglár` |
| `121257451` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Balatonboglár` |
| `121234075` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Glera, Garganega`; eredet `egyéb` → `Veneto` |
| `121222210` | eredet `egyéb` → `Etyek-Buda` |
| `121237170` | eredet `egyéb` → `Olaszország` |
| `121222613` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera` |

### 108. köteg – Pezsgő, habzóbor és gyöngyözőbor 509–533.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Cinzano Prosecco és a két Mionetto Prosecco Brut pontos termékneve,
  közvetlen címkéje és termékadata Glera szőlőből készült Prosecco DOC
  Spumantét igazol. A Mionetto 750 ml-es palackján a Treviso eredetjelölés
  is szerepel.
- A Mionetto Prosecco Rosé pontos termékadata Glera–Pinot Noir házasítású,
  olasz Prosecco DOC Spumantét igazol. A Bella Cucina Prosecco DOC két
  kiszerelése Glera-alapú, olasz, félszáraz gyöngyözőbor, ezért a meglévő
  `gyöngyözőbor` értéket megtartva a `prosecco` fajtát is rögzítettük.
- A Hungaria Extra Dry 0,2 literes pontos termékpárhuzama Chardonnay,
  Királyleányka és Pinot Noir házasítást, valamint Etyek-Buda eredetet
  igazol. A Hungaria Irsai Olivér Doux és a Hungaria Extra Dry Rosé
  termékpárhuzama szintén Etyek-Buda eredetet közöl.
- A Sauska Brut pontos termékadata Furmint, Chardonnay és Pinot Noir
  házasítást, Tokaj eredetet és brut édességet igazol. A Kreinbacher Extra
  Dry pontos termékadata Furmint, Chardonnay, Pinot Noir és Pinot Blanc
  házasítást, Somló eredetet, a közvetlen kép pedig fehér színt igazol.
- A két Tesco Cava pontos áruházi termékadata és forrásmárkája Tesco márkájú,
  spanyol Cava besorolást igazol. Egyértelmű szőlőfajta-adat hiányában a
  `szőlőfajta: egyéb` értéket nem találgattuk.
- A Bella Cucina Demi-Sec rosé pontos Tesco-termékadata 10,5%-os, olasz,
  félszáraz rosé gyöngyözőbort igazol. A Bella Cucina Proseccóktól eltérően
  ennél a rekordnál a forrás nem közöl szőlőfajtát, ezért az `egyéb` érték
  maradt.
- A Mionetto 0.0 pontos termékadata alkoholmentes borból készült szénsavas
  italt igazol, ezért a `habzóbor` fajtát `alkoholmentes habzó ital`
  értékre pontosítottuk. A forrás nem ad édességi osztályt vagy pontos
  eredetet, ezért ezeket nem következtettük.
- A Varga Bubis Rosé pontos Tesco-termékadata szénsavas, száraz balatoni rosé
  tájbort igazol, de alkoholfokot nem közöl. A jelenlegi rekord többi
  bizonyítható értéke helyes, ezért változatlan maradt.
- A Laposa Méthode Charmat Balatoni Brut pontos termékadata Furmint-alapú
  balatoni pezsgőt, a közvetlen címke pedig fehér színt igazol. A BB Arany
  Cuvée pontos termékpárhuzama Muskotály szőlőfajtát és Balatonboglár
  eredetet közöl.
- A Louis François & Co. Brut Nature közvetlen függőcímkéje és pontos
  termékadata a `Louis François & Co.` márkaformát, valamint Chardonnay és
  Pinot Noir házasítást igazol. A korábbi összefűzött márkanév hibás volt.
- A Szovjetszkoje Igrisztoje félszáraz fehér, a Törley alkoholmentes fehér
  és a két König pezsgő pontos termékadata magyar eredetet igazol. A Törley
  Charmant Rosé pontos termékpárhuzama Etyek-Buda, a Natara száraz fehéré
  Kunság eredetet közöl.
- Módosított rekord: **24**.
- Módosított tulajdonságmező: **48**.
- Változatlanul hagyott rekord: **1** (`120476279`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 48 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 24 írás sikeres volt, visszaállításra
  nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121230592` | eredet `egyéb` → `Magyarország` |
| `121234098` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `121266371` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Treviso` |
| `121222193` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `121222245` | eredet `egyéb` → `Etyek-Buda` |
| `121257422` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera` |
| `121274021` | alkoholtartalom `ismeretlen` → `10,5%`; eredet `egyéb` → `Olaszország` |
| `121222550` | eredet `egyéb` → `Magyarország` |
| `121224346` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj`; édesség `brut, száraz` → `brut` |
| `121222665` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `121224496` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir, Pinot Blanc`; eredet `egyéb` → `Somló`; szín `egyéb` → `fehér` |
| `121222395` | eredet `egyéb` → `Etyek-Buda` |
| `121282633` | márka `márka nélkül` → `Tesco`; fajta `pezsgő` → `cava`; eredet `egyéb` → `Spanyolország` |
| `121230874` | eredet `egyéb` → `Kunság` |
| `121266365` | fajta `habzóbor` → `alkoholmentes habzó ital` |
| `121222377` | eredet `egyéb` → `Etyek-Buda` |
| `121237158` | fajta `gyöngyözőbor` → `gyöngyözőbor, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `121230494` | eredet `egyéb` → `Magyarország` |
| `121257480` | szőlőfajta `egyéb` → `Furmint`; szín `egyéb` → `fehér` |
| `121222106` | szőlőfajta `egyéb` → `Muskotály`; eredet `egyéb` → `Balatonboglár` |
| `121279782` | fajta `gyöngyözőbor` → `gyöngyözőbor, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `121222694` | márka `Francois Louis François & Co.` → `Louis François & Co.`; szőlőfajta `egyéb` → `Chardonnay, Pinot Noir` |
| `121230488` | eredet `egyéb` → `Magyarország` |
| `121282627` | márka `márka nélkül` → `Tesco`; fajta `pezsgő` → `cava`; eredet `egyéb` → `Spanyolország` |

### 109. köteg – Pezsgő, habzóbor és gyöngyözőbor 534–559.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **24**.
- Közvetlen termékkép nélkül ellenőrzött rekord: **1** (`121315521`); a
  helyi fájl csak `image unavailable` helyőrzőt tartalmaz.
- Az 537. pozíció `121222965` azonosítójú Voilá szamóca rekordját korábbi
  kötegben már teljes rekorddal és képpel ellenőriztük. Ezt nem számoltuk
  kétszer; a köteget az 559. pozíció még nem vizsgált rekordjával
  egészítettük ki.
- A Hungaria 1,5 literes különlegesen száraz tétel pontos
  termékpárhuzama Chardonnay, Királyleányka és Pinot Noir házasítást,
  valamint Etyek-Buda eredetet igazol. A Hungaria Irsai Olivér pontos
  párhuzama szintén Etyek-Buda eredetet közöl.
- A Natara száraz rosé, édes fehér és Moscato pontos termékpárhuzamai
  Kunság eredetet igazolnak. A Natara Extra Dry 11%-os pontos szakmai
  terméklapja Kunság eredetet, valamint Riesling, Cserszegi fűszeres és
  Bianca házasítást közöl.
- A Royal születésnapi Muskotály és a márka nélküli Muskotály pontos
  termékadata magyar terméket igazol. Egyikhez sem következtettünk a
  bizonyítható országadatnál szűkebb eredetet.
- A François President Brut és Extra Dry pontos termékadata Chardonnay és
  Pinot Noir házasítást igazol. A Brut Etyek-Buda eredetét is pótoltuk; az
  Extra Dry jelenlegi Etyek-Buda eredete már helyes volt.
- A Veuve Clicquot Yellow Label és a Moët & Chandon Brut Impérial pontos
  gyártói termékadata Pinot Noir, Meunier és Chardonnay házasítású
  Champagne-t és brut édességet igazol. A redundáns általános `pezsgő`
  fajtát és `száraz` édességet eltávolítottuk.
- A BB 0,2 literes Spumante pontos termékpárhuzama Muskotály szőlőből
  készült balatonboglári Spumantét igazol. A Sauska Extra Dry Furmint,
  Chardonnay és Pinot Noir házasítású, Tokaj eredetű pezsgő.
- A Gedeon Birtok Brut pontos szakmai termékadata Generosa és Zöld
  veltelini házasítást, valamint Kunság eredetet közöl. A Törley Brut,
  Extra Sec és Rosé Sec pontos termékpárhuzamai Etyek-Buda eredetet
  igazolnak.
- A Hungaria alkoholmentesített borból készült habzó ital pontos
  termékadata 30 g/l cukrot közöl; az ág egységes édességi skáláján ez
  `száraz`, nem `édes`. Bizonytalan szőlőfajtát és eredetet nem
  következtettünk.
- A Louis Couturier Crémant jelenlegi Crémant de Bordeaux besorolása,
  Bordeaux eredete és brut édessége helyes. Az elérhető források nem
  egyeznek teljesen a pontos alkoholfokú változat szőlőösszetételében és
  színében, ezért a két `egyéb` értéket változatlanul hagytuk.
- A Bella Cucina Asti neve és pontos termékadata Moscato Bianco szőlőből
  készült Asti Spumantét, a Bella Cucina Prosecco pedig Glera szőlőből
  készült olasz Prosecco DOC Spumantét igazol.
- A Barigny pontos szakmai termékadata francia fehér brut habzóbort
  igazol. Egyértelmű, a pontos forrásváltozathoz kötött szőlőösszetétel
  hiányában a szőlőfajta `egyéb` maradt.
- A Kislaki Chardonnay neve és pontos termékadata a jelenlegi
  Chardonnay–Balatonboglár–brut értékeket igazolja. A helyi kép csak
  helyőrző, a pontos termékoldal pedig nem közöl külön színmezőt, ezért a
  színt nem találgattuk.
- A Mionetto Treviso Frizzante pontos termékadata Glera szőlőből készült,
  Treviso eredetű gyöngyözőbor–Proseccót igazol; a tágabb, redundáns
  `Olaszország` eredetértéket eltávolítottuk.
- Módosított rekord: **23**.
- Módosított tulajdonságmező: **40**.
- Változatlanul hagyott új rekord: **2** (`121311635`, `121315521`).
- Új megengedett érték: **1** (`szőlőfajta: Riesling`).
- Törölt megengedett érték: **0**.
- A 40 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 23 írás sikeres volt, visszaállításra
  nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `220305116` | szőlőfajta `egyéb` → `Chardonnay, Királyleányka, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `121230908` | eredet `egyéb` → `Kunság` |
| `121230534` | eredet `egyéb` → `Magyarország` |
| `121223036` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir`; eredet `egyéb` → `Etyek-Buda` |
| `121224260` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `121224513` | fajta `pezsgő` → `champagne`; szőlőfajta `egyéb` → `Pinot Noir, Meunier, Chardonnay`; eredet `egyéb` → `Champagne`; édesség `brut, száraz` → `brut` |
| `121230816` | eredet `egyéb` → `Magyarország` |
| `121230851` | eredet `egyéb` → `Kunság` |
| `121257445` | szőlőfajta `egyéb` → `Riesling, Cserszegi fűszeres, Bianca`; eredet `egyéb` → `Kunság` |
| `121257468` | fajta `pezsgő` → `spumante`; eredet `egyéb` → `Balatonboglár` |
| `121257474` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj` |
| `121257497` | szőlőfajta `egyéb` → `Generosa, Zöld veltelini`; eredet `egyéb` → `Kunság` |
| `121269419` | eredet `egyéb` → `Etyek-Buda` |
| `121278368` | eredet `egyéb` → `Etyek-Buda` |
| `121278374` | eredet `egyéb` → `Etyek-Buda` |
| `121278380` | eredet `egyéb` → `Etyek-Buda` |
| `121278397` | szőlőfajta `egyéb` → `Chardonnay, Pinot Noir` |
| `121285336` | eredet `egyéb` → `Kunság` |
| `121306313` | édesség `édes` → `száraz` |
| `121314672` | fajta `pezsgő` → `spumante`; szőlőfajta `egyéb` → `Moscato Bianco`; eredet `egyéb` → `Asti` |
| `121314695` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország` |
| `121314845` | eredet `egyéb` → `Franciaország` |
| `121315573` | szőlőfajta `egyéb` → `Glera`; eredet `Olaszország, Treviso` → `Treviso` |

### 110. köteg – Pezsgő, habzóbor és gyöngyözőbor 560–566.

- Ellenőrzött új rekord: **7**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **7**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- Ezzel a köteggel a **566** rekordos pezsgő-, habzóbor- és
  gyöngyözőborág valamennyi termékének egyenkénti felülvizsgálata elkészült.
- A Kreinbacher Brut Classic hivatalos terméklapja Furmint, Chardonnay,
  Pinot Blanc és Pinot Noir házasítást, Somló eredetet, brut édességet és
  fehér színt igazol. A redundáns `száraz` édességértéket eltávolítottuk.
- A Martini Prosecco pontos termékadata Glera szőlőből készült olasz,
  fehér Prosecco DOC Spumantét, a Martini Prosecco Rosé pedig Glera és
  Pinot Noir házasítású olasz rosé Prosecco DOC Spumantét igazol.
- A Natara alkoholmentes, édes, fehér habzóital-rekordjának minden
  bizonyítható tulajdonsága összhangban van a névvel, a képpel és a pontos
  termékadattal. A forrás nem közöl egyértelmű szőlőfajtát vagy eredetet,
  ezért változatlan maradt.
- A Villa Vincento közvetlen palackcímkéje és pontos termékpárhuzama 11%-os,
  magyar eredetű, édes fehér pezsgőt igazol. Bizonytalan szőlőfajtát nem
  rögzítettünk.
- A Sauska Brut Nature hivatalos műszaki lapja 12%-os, Furmint,
  Chardonnay és Pinot Noir házasítású, fehér tokaji Brut Nature pezsgőt
  igazol. A forrásnévben szereplő `53,5%` nyilvánvaló forráshiba; a
  terméktulajdonságban már helyesen szereplő 12%-ot megtartottuk, a
  redundáns `száraz` édességértéket eltávolítottuk.
- A The Sparkling T Alba nem bor, hanem alkoholmentes, fehér, száraz,
  pezsgőalternatívaként csomagolt szénsavas teaital. A jelenlegi
  `alkoholmentes habzó ital` fajta megfelelő; a közvetlen címke alapján a
  `The Sparkling T` márkát, a pontos termékleírások alapján a fehér színt
  rögzítettük. Bizonytalan boreredetet vagy szőlőfajtát nem
  következtettünk.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **18**.
- Változatlanul hagyott rekord: **1** (`121333597`).
- Új megengedett érték: **1** (`márka: The Sparkling T`).
- Törölt megengedett érték: **0**.
- A 18 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 6 írás sikeres volt, visszaállításra
  nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121321594` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Blanc, Pinot Noir`; eredet `egyéb` → `Somló`; édesség `brut, száraz` → `brut`; szín `egyéb` → `fehér` |
| `121323085` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera`; eredet `egyéb` → `Olaszország`; szín `fehér, rozé` → `fehér` |
| `121323091` | fajta `pezsgő, prosecco` → `spumante, prosecco`; szőlőfajta `egyéb` → `Glera, Pinot Noir`; eredet `egyéb` → `Olaszország` |
| `121333712` | eredet `egyéb` → `Magyarország` |
| `121357396` | szőlőfajta `egyéb` → `Furmint, Chardonnay, Pinot Noir`; eredet `egyéb` → `Tokaj`; édesség `brut nature, száraz` → `brut nature`; szín `egyéb` → `fehér` |
| `121361937` | márka `márka nélkül` → `The Sparkling T`; szín `egyéb` → `fehér` |

### 111. köteg – Sör, radler és malátaital 1–25.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **24**.
- Helyi kép nélkül ellenőrzött rekord: **1** (`873849`).
- A Karlskrone 4,5%-os, a Bergkönig Premium 0,33 literes és a Löwenbräu
  közvetlen címkéje lager sört jelöl. A Karlskrone búzasör címkéje
  szűretlen, világos búzasört, az IPA címkéje pedig világos sört igazol.
- A Soproni világos sör címkéjén `lager`, az Óvatos Duhaj Meggy címkéjén
  `ale`, a Heineken címkéjén `pure malt lager` szerepel; ezeket a meglévő
  fajtaértékekkel pontosítottuk.
- A Sixtusbräu 1,5 literes pontos ALDI-termékadata 4,2%-os világos sört,
  az azonos termék palackadata pedig lager stílust igazol.
- A Karlskrone alkoholmentes sör pontos ALDI-termékadata 0,5%-os névleges
  alkoholtartalmat közöl; a korábbi `0%` értéket ezért `0,5%`-ra
  javítottuk.
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **12**.
- Változatlanul hagyott rekord: **15** (`989118`, `541393`, `873849`,
  `749188`, `541087`, `992576`, `4604641`, `913908`, `539287`, `4606192`,
  `996225`, `566880`, `992577`, `997467`, `1028287`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 12 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 10 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1027165` | fajta `sör` → `sör, lager` |
| `533682` | szín `egyéb` → `világos`; szűretlen `hamis` → `igaz` |
| `4598565` | fajta `sör` → `sör, lager` |
| `1059546` | szín `egyéb` → `világos` |
| `541746` | fajta `sör` → `sör, lager` |
| `4605610` | fajta `sör` → `sör, lager` |
| `997189` | fajta `sör` → `sör, ale` |
| `997187` | fajta `sör` → `sör, lager` |
| `1026722` | alkoholtartalom `ismeretlen` → `4,2%`; fajta `sör` → `sör, lager` |
| `533754` | alkoholtartalom `0%` → `0,5%` |

### 112. köteg – Sör, radler és malátaital 26–50.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A két Friss 0,0%-os termék neve, közvetlen dobozcímkéje és forrásadata
  üdítőital és malátaital keverékét igazolja. A téves `alkoholos`
  státuszt `alkoholmentes` értékre, a `radler` fajtát `malátaital`
  értékre javítottuk.
- A Carlsberg 0,33 és 0,5 literes termékek közvetlen címkéje `Danish
  Pilsner`, az Auchan-forráskategóriájuk pedig `Pilsner`. A Berliner Kindl
  címkéje szintén Pilsener; ezért az általános `sör` mellé felvettük a
  meglévő `pilsner` fajtaértéket.
- A Welsenburg, Kőbányai, Soproni, Arany Ászok, Arany Szarvas,
  Staropramen, Dreher Gold, Gösser Premium és Heineken forráskategóriája
  `Lager`; a Soproni és a Heineken közvetlen címkéje ezt külön is
  megerősíti. Ezeknél az általános `sör` mellé felvettük a meglévő
  `lager` értéket.
- Módosított rekord: **15**.
- Módosított tulajdonságmező: **17**.
- Változatlanul hagyott rekord: **10** (`533763`, `972079`, `1059392`,
  `1059393`, `1059394`, `992563`, `678956:4216346`, `684596:4221986`,
  `795203:4332593`, `719261:4256651`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 17 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 15 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `907853` | alkoholstátusz `alkoholos` → `alkoholmentes`; fajta `radler` → `malátaital` |
| `4606125` | alkoholstátusz `alkoholos` → `alkoholmentes`; fajta `radler` → `malátaital` |
| `679910:4217300` | fajta `sör` → `sör, pilsner` |
| `679925:4217315` | fajta `sör` → `sör, pilsner` |
| `679913:4217303` | fajta `sör` → `sör, pilsner` |
| `682310:4219700` | fajta `sör` → `sör, pilsner` |
| `678284:4215674` | fajta `sör` → `sör, lager` |
| `677810:4215200` | fajta `sör` → `sör, lager` |
| `674633:4212023` | fajta `sör` → `sör, lager` |
| `677804:4215194` | fajta `sör` → `sör, lager` |
| `679298:4216688` | fajta `sör` → `sör, lager` |
| `678197:4215587` | fajta `sör` → `sör, lager` |
| `677807:4215197` | fajta `sör` → `sör, lager` |
| `661500:4198890` | fajta `sör` → `sör, lager` |
| `661494:4198884` | fajta `sör` → `sör, lager` |

### 113. köteg – Sör, radler és malátaital 51–75.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- Húsz rekord Auchan-forráskategóriája `Lager`; ezt a Löwenbräu,
  Hofbräu, Soproni, Holsten, Pécsi Sör és Kozel közvetlen címkéi külön is
  megerősítik. A jelenleg csak `sör` fajtájú rekordoknál felvettük a
  meglévő `lager` értéket.
- A Szalon közvetlen dobozcímkéje a `Szalon` márkát és lager típust
  igazolja. A korábbi `Pécsi` a gyártóra utalt, ezért a márkaértéket
  `Szalon` értékre javítottuk.
- A Zipfer termék neve és közvetlen címkéje egyaránt `Märzen` sört
  igazol. A pontos, elemi sörstílust új `märzen` fajtaértékként felvettük,
  a forráskategória alapján a `lager` értéket is rögzítettük.
- Módosított rekord: **20**.
- Módosított tulajdonságmező: **21**.
- Változatlanul hagyott rekord: **5** (`677801:4215191`,
  `679985:4217375`, `674630:4212020`, `678959:4216349`,
  `679994:4217384`).
- Új megengedett érték: **1** (`fajta: märzen`).
- Törölt megengedett érték: **0**.
- A 21 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 20 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `674627:4212017` | fajta `sör` → `sör, lager` |
| `679991:4217381` | fajta `sör` → `sör, lager` |
| `678962:4216352` | márka `Pécsi` → `Szalon`; fajta `sör` → `sör, lager` |
| `679295:4216685` | fajta `sör` → `sör, lager` |
| `679934:4217324` | fajta `sör` → `sör, lager` |
| `679970:4217360` | fajta `sör` → `sör, lager` |
| `661:661` | fajta `sör` → `sör, lager` |
| `678194:4215584` | fajta `sör` → `sör, lager` |
| `679916:4217306` | fajta `sör` → `sör, lager` |
| `898:898` | fajta `sör` → `sör, lager` |
| `679922:4217312` | fajta `sör` → `sör, lager` |
| `752007:4289397` | fajta `sör` → `sör, lager, märzen` |
| `661497:4198887` | fajta `sör` → `sör, lager` |
| `500699:4038095` | fajta `sör` → `sör, lager` |
| `661503:4198893` | fajta `sör` → `sör, lager` |
| `678185:4215575` | fajta `sör` → `sör, lager` |
| `679979:4217369` | fajta `sör` → `sör, lager` |
| `678191:4215581` | fajta `sör` → `sör, lager` |
| `680009:4217399` | fajta `sör` → `sör, lager` |
| `760797:4298187` | fajta `sör` → `sör, lager` |

### 114. köteg – Sör, radler és malátaital 76–100.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- Tizenkilenc rekord Auchan-forráskategóriája `Lager`. A Heineken,
  Zlaty Bazant, Karlovačko és Daura Damm közvetlen címkéje ezt szó szerint
  megerősíti; a Primator `ležák` megnevezése szintén lager sört jelent.
- Az Amstel közvetlen dobozcímkéje a lager besorolás mellett `Pilsener`
  megjelölést is tartalmaz, ezért ennél a rekordnál a meglévő `pilsner`
  értéket is rögzítettük.
- A Platan címkéjén a `10°` a sörlé extrakttartalmának jelölése, míg az
  alkoholtartalom külön 4,0%-ként szerepel. A jelenlegi 4%-os értéket
  ezért változatlanul hagytuk.
- Módosított rekord: **19**.
- Módosított tulajdonságmező: **19**.
- Változatlanul hagyott rekord: **6** (`791252:4328642`,
  `789929:4327319`, `795200:4332590`, `793091:4330481`,
  `678968:4216358`, `787886:4325276`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 19 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 19 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `661491:4198881` | fajta `sör` → `sör, lager` |
| `185918:3723158` | fajta `sör` → `sör, lager` |
| `678203:4215593` | fajta `sör` → `sör, lager` |
| `761994:4299384` | fajta `sör` → `sör, lager` |
| `795194:4332584` | fajta `sör` → `sör, lager` |
| `819563:4356953` | fajta `sör` → `sör, lager, pilsner` |
| `752001:4289391` | fajta `sör` → `sör, lager` |
| `31795:31798` | fajta `sör` → `sör, lager` |
| `680015:4217405` | fajta `sör` → `sör, lager` |
| `793022:4330412` | fajta `sör` → `sör, lager` |
| `52872:53211` | fajta `sör` → `sör, lager` |
| `186730:3723973` | fajta `sör` → `sör, lager` |
| `679973:4217363` | fajta `sör` → `sör, lager` |
| `679988:4217378` | fajta `sör` → `sör, lager` |
| `661479:4198869` | fajta `sör` → `sör, lager` |
| `678188:4215578` | fajta `sör` → `sör, lager` |
| `672995:4210385` | fajta `sör` → `sör, lager` |
| `661488:4198878` | fajta `sör` → `sör, lager` |
| `1032530:4569920` | fajta `sör` → `sör, lager` |

### 115. köteg – Sör, radler és malátaital 101–125.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A két Staropramen Dark címkéje szó szerint `full-bodied dark lager`
  megjelölést tartalmaz; ezért az általános `sör` mellé felvettük a
  meglévő `lager` értéket.
- A Paulaner Salvator címkéje `Doppelbock`, vagyis bak sört igazol. A
  Leffe Brune belga, felső erjesztésű barna apátsági sör, ezért a meglévő
  `ale` értékkel pontosítottuk.
- A Soproni Démon címkéje `barna sör karamellmalátával` megnevezést
  tartalmaz. A karamell itt malátatípus, nem hozzáadott ízesítés, ezért a
  hibás `karamell` ízt `natúr` értékre javítottuk.
- A Paulaner Münchner Hell termékeknél a név és a címke együtt igazolja a
  `lager` és `helles` típust. A Paulaner Weissbier világos változatánál a
  színt, az Erdinger Weissbräu és a `Naturtrüb` feliratú Kaiserdom
  Hefe-Weißbiernél pedig a szűretlenséget pontosítottuk.
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **10**.
- Változatlanul hagyott rekord: **15** (`793097:4330487`,
  `679958:4217348`, `661470:4198860`, `747278:4284668`,
  `680042:4217432`, `692957:4230347`, `775776:4313166`,
  `679931:4217321`, `680039:4217429`, `1012231:4549621`,
  `795197:4332587`, `679889:4217279`, `674690:4212080`,
  `677741:4215131`, `53727:54066`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 10 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 10 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `4348:4348` | fajta `sör` → `sör, lager` |
| `678260:4215650` | fajta `sör` → `sör, lager` |
| `790052:4327442` | fajta `sör` → `sör, bak` |
| `713813:4251203` | fajta `sör` → `sör, ale` |
| `661473:4198863` | íz `karamell` → `natúr` |
| `677747:4215137` | fajta `sör, lager` → `sör, lager, helles` |
| `677738:4215128` | szín `egyéb` → `világos` |
| `7609:7612` | szűretlen `hamis` → `igaz` |
| `677744:4215134` | fajta `sör, helles` → `sör, lager, helles` |
| `684629:4222019` | szűretlen `hamis` → `igaz` |

### 116. köteg – Sör, radler és malátaital 126–150.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Paulaner 5 literes Hefe-Weißbier neve és `Naturtrüb` címkéje a
  szűretlenség mellett a világos búzasörváltozatot igazolja; a hiányzó
  színt `világos` értékre pontosítottuk.
- A Szalon alkoholmentes sör közvetlen dobozcímkéjén a `Szalon` név
  szerepel. A `Pécsi` a gyártóra utalt, ezért a márkaértéket `Szalon`
  értékre javítottuk.
- A Heineken 0.0 dobozcímkéje `pure malt lager`, a Staropramené `premium
  lager`, a DAB Zero dobozcímkéje pedig `non-alcoholic lager beer`
  megjelölést tartalmaz. Ezeknél felvettük a meglévő `lager` értéket.
- A Peroni gyártói termékadata a Nastro Azzurro 0.0-t alkoholmentes
  lagerként, a Corona gyártói oldala a Cero változatot `pale lager`
  típusként azonosítja. A két Peroni-rekordnál a `lager` mellett az 500
  ml-es tétel hiányzó világos színét is javítottuk.
- A Stella Artois alkoholmentes változata ugyanannak a belga lagernek a
  0,0%-os tétele, ezért ennél is felvettük a meglévő `lager` értéket.
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **15** (`692954:4230344`,
  `692987:4230377`, `680045:4217435`, `673016:4210406`,
  `821780:4359170`, `678977:4216367`, `678980:4216370`,
  `678983:4216373`, `688061:4225451`, `680117:4217507`,
  `796646:4334036`, `796649:4334039`, `680126:4217516`,
  `686096:4223486`, `793838:4331228`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 11 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 10 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `97303:3634337` | szín `egyéb` → `világos` |
| `678971:4216361` | márka `Pécsi` → `Szalon` |
| `673025:4210415` | fajta `sör` → `sör, lager` |
| `875006:4412396` | fajta `sör` → `sör, lager` |
| `674684:4212074` | fajta `sör` → `sör, lager` |
| `678269:4215659` | fajta `sör` → `sör, lager` |
| `1012024:4549414` | fajta `sör` → `sör, lager`; szín `egyéb` → `világos` |
| `680123:4217513` | fajta `sör` → `sör, lager` |
| `785903:4323293` | fajta `sör` → `sör, lager` |
| `963515:4500905` | fajta `sör` → `sör, lager` |

### 117. köteg – Sör, radler és malátaital 151–175.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Dreher 24 Citrom négyes csomag közvetlen képe minden dobozon 0,0%-ot
  mutat, az egyedi 500 ml-es, azonos termék rekordja pedig már helyesen
  alkoholmentes és világos. A csomag rekordjának téves `alkoholos`
  státuszát és hiányzó színét ennek megfelelően javítottuk.
- A két Paulaner alkoholmentes Weissbier a világos búzasörváltozat; a
  330 ml-es palacknál a szűretlenség már helyesen szerepelt, mindkét
  rekord hiányzó színét `világos` értékre pontosítottuk.
- A Guinness 0.0 dobozcímkéje közvetlenül `alcohol free stout`, a
  terméknév pedig fekete színt közöl. Ezért a `stout` típust felvettük,
  a téves `barna` színt pedig `fekete` értékre javítottuk.
- A Primátor Free Mother in Law gyártói termékadata a normál India Pale
  Lager alkoholmentes változatát, szűretlenséget és arany-réz színt
  igazol. A meglévő `lager`, `India pale lager` és `borostyán`
  értékekkel, valamint a szűretlen jelzővel pontosítottuk.
- A Heineken Silver Auchan-forráskategóriája `Lager, Pilsner`; a termék a
  Heineken világos lager könnyebb változata, ezért az általános `sör`
  mellé felvettük a meglévő `lager` értéket.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **10**.
- Változatlanul hagyott rekord: **19** (`793832:4331222`,
  `793829:4331219`, `793826:4331216`, `673019:4210409`,
  `673013:4210403`, `673010:4210400`, `673007:4210397`,
  `674681:4212071`, `673022:4210412`, `673028:4210418`,
  `674687:4212077`, `673004:4210394`, `673031:4210421`,
  `1032338:4569728`, `1032335:4569725`, `760794:4298184`,
  `692990:4230380`, `692960:4230350`, `847979:4385369`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 10 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 6 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1017781:4555171` | alkoholstátusz `alkoholos` → `alkoholmentes`; szín `egyéb` → `világos` |
| `97309:3634343` | szín `egyéb` → `világos` |
| `677750:4215140` | szín `egyéb` → `világos` |
| `791255:4328645` | fajta `sör` → `sör, stout`; szín `barna` → `fekete` |
| `946502:4483892` | fajta `sör` → `sör, lager, India pale lager`; szín `egyéb` → `borostyán`; szűretlen `hamis` → `igaz` |
| `674618:4212008` | fajta `sör` → `sör, lager` |

### 118. köteg – Sör, radler és malátaital 176–200.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Birra Moretti, Coors, Peroni Nastro Azzurro, Asahi Super Dry,
  Estrella Damm és Borsodi Hoppy forráskategóriája `Lager, Pilsner`; a
  Konrad címkéje külön `Czech lager beer` és `světlý ležák` megjelölést
  is tartalmaz. Ezeknél az általános `sör` mellé felvettük a meglévő
  `lager` értéket.
- A Peroni Stile Capri gyártói termékadata alsó erjesztésű, citromhéj- és
  olívalevél-jegyekkel készített sört igazol. A meglévő `citrom` íz
  helyes volt, a hiányzó `lager` típust pótoltuk.
- A Bitburger közvetlen dobozcímkéjén `Premium Pils` olvasható, ezért a
  meglévő `pilsner` típust rögzítettük.
- Az O'Hara's Nitro Irish Red közvetlen dobozcímkéje Irish Red Ale-t, az
  Irish Stout címkéje stoutot igazol. Mindkét dobozon szó szerint `craft
  brewed in Ireland` áll, ezért a `kézműves` jelzőt igazra állítottuk; a
  stout téves `barna` színét `fekete` értékre javítottuk.
- Módosított rekord: **15**.
- Módosított tulajdonságmező: **17**.
- Változatlanul hagyott rekord: **10** (`678248:4215638`,
  `751965:4289355`, `679919:4217309`, `747389:4284779`,
  `693026:4230416`, `679961:4217351`, `793088:4330478`,
  `795149:4332539`, `678218:4215608`, `1032329:4569719`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 17 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 15 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `674621:4212011` | fajta `sör` → `sör, lager` |
| `789413:4326803` | fajta `sör` → `sör, lager` |
| `678230:4215620` | fajta `sör` → `sör, lager` |
| `678221:4215611` | fajta `sör` → `sör, lager` |
| `678227:4215617` | fajta `sör` → `sör, lager` |
| `680036:4217426` | fajta `sör` → `sör, lager` |
| `679997:4217387` | fajta `sör` → `sör, lager` |
| `680051:4217441` | fajta `sör` → `sör, lager` |
| `680021:4217411` | fajta `sör` → `sör, lager` |
| `680024:4217414` | fajta `sör` → `sör, lager` |
| `693485:4230875` | fajta `sör` → `sör, pilsner` |
| `682307:4219697` | fajta `sör` → `sör, lager` |
| `678215:4215605` | fajta `sör` → `sör, lager` |
| `747260:4284650` | fajta `sör` → `sör, ale`; kézműves `hamis` → `igaz` |
| `747263:4284653` | szín `barna` → `fekete`; kézműves `hamis` → `igaz` |

### 119. köteg – Sör, radler és malátaital 201–225.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Borsodi Tropical Ale neve és címkéje nem gyümölcsös ízesítést, hanem
  ale sört közöl; a `Tropical` a komlós aromajelleg neve. A hibás
  `trópusi gyümölcs` ízt `natúr` értékre javítottuk.
- A Bohemia Regent Premium Pale Lager pontos termékadata 5,0%-os
  alkoholtartalmat igazol, ezért az `ismeretlen` értéket `5%`-ra
  pontosítottuk.
- A Dreher Hidegkomlós alsó erjesztésű lager, a Desperados Original és a
  Corona Extra pedig ízesített, illetve natúr pale lager; mindháromnál
  felvettük a meglévő `lager` értéket.
- A Primátor Mother in Law közvetlen címkéje és gyártói termékadata India
  Pale Lagert, szűretlenséget és arany-réz színt igazol. A meglévő
  `lager`, `India pale lager`, `borostyán` értékekkel és a szűretlen
  jelzővel pontosítottuk.
- A Belgium büszkesége csomag közvetlen képe 2 Stella Artois, 2
  Hoegaarden, 1 Leffe Blonde és 1 Leffe Dark palackot mutat. Ez nem
  gyümölcsös válogatás: a fajtákat `lager`, `búzasör` és `ale`
  értékekkel, az ízt `natúr`, a színeket `világos, barna` értékkel
  javítottuk.
- A DAB Export és DAB Lager címkéjén közvetlenül `Dortmunder Export`,
  illetve `Dortmunder Lager` olvasható. Az önálló, elemi `dortmunder`
  fajtaértéket felvettük, és a `lager` mellett mindkét rekordhoz
  hozzárendeltük.
- A Schöfferhofer Hefeweizen dobozcímkéje `Naturtrüb`, ezért a
  szűretlenséget igazra állítottuk.
- A Lázadó Láma és Léhűtő Lajhár forráskategóriája `Magyar kisüzemi`,
  közvetlen címkéjük IPA-, illetve APA-sört igazol; ezért a `kézműves`
  jelzőt igazra állítottuk.
- A Cecei Fresh IPA-nál ugyancsak a kisüzemi, natúrsör-jelleg alapján
  javítottuk a `kézműves` mezőt. A bizonyíték a 191. sorszámú, előző
  kötegben már ellenőrzött Cecei Lagernél is igazolta a kézműves és
  szűretlen jelleget, ezért azt követő korrekcióként módosítottuk. A
  korábban ellenőrzött DAB Zero címkéje szintén közvetlen
  `Dortmunder Zero` megjelölést tartalmazott, ezért az új stílusértéket
  azon is rögzítettük. Ezeket az előrehaladásban nem számoltuk újra.
- Módosított új rekord: **13**.
- Módosított tulajdonságmező az új rekordokon: **17**.
- Korábbi kötegből követően pontosított rekord: **2**, tulajdonságmező:
  **3** (`785903:4323293`, `693026:4230416`).
- Változatlanul hagyott új rekord: **12** (`661476:4198866`,
  `673034:4210424`, `678236:4215626`, `678212:4215602`,
  `674693:4212083`, `680033:4217423`, `747380:4284770`,
  `678257:4215647`, `770952:4308342`, `747254:4284644`,
  `790184:4327574`, `677735:4215125`).
- Új megengedett érték: **1** (`fajta: dortmunder`).
- Törölt megengedett érték: **0**.
- A 20 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 15 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `693023:4230413` | kézműves `hamis` → `igaz` |
| `678224:4215614` | íz `trópusi gyümölcs` → `natúr` |
| `780917:4318307` | alkoholtartalom `ismeretlen` → `5%` |
| `680030:4217420` | fajta `sör` → `sör, lager` |
| `672992:4210382` | fajta `sör` → `sör, lager` |
| `789926:4327316` | fajta `sör, India pale lager` → `sör, lager, India pale lager`; szín `világos` → `borostyán`; szűretlen `hamis` → `igaz` |
| `678233:4215623` | fajta `sör` → `sör, lager` |
| `678209:4215599` | fajta `sör` → `sör, lager, búzasör, ale`; íz `vegyes gyümölcs` → `natúr`; szín `világos` → `világos, barna` |
| `747248:4284638` | fajta `sör` → `sör, lager, dortmunder` |
| `682304:4219694` | fajta `sör` → `sör, lager, dortmunder` |
| `784556:4321946` | szűretlen `hamis` → `igaz` |
| `678788:4216178` | kézműves `hamis` → `igaz` |
| `678785:4216175` | kézműves `hamis` → `igaz` |
| `785903:4323293` | korábbi köteg követő javítása: fajta `sör, lager` → `sör, lager, dortmunder` |
| `693026:4230416` | korábbi köteg követő javítása: kézműves `hamis` → `igaz`; szűretlen `hamis` → `igaz` |

### 120. köteg – Sör, radler és malátaital 226–250.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Hoegaarden White címkéje `naturally cloudy`, ezért a szűretlenséget
  igazra állítottuk. A Leffe Blonde belga apátsági ale; a meglévő `belga
  blond` mellé felvettük az `ale` értéket.
- A Hacker-Pschorr Weissbier címkéje `classic wheat beer unfiltered`, a
  termék a világos változat, ezért a hiányzó színt `világos` értékre
  javítottuk. A másik Hacker-Pschorr dobozon `Kellerbier`, `authentic
  lager` és `unfiltered` olvasható; a szűretlenség már helyes volt, a
  `lager` és `kellerbier` típust pótoltuk.
- A Szent András Magyar Vándor közvetlen címkéje szó szerint `lager–ale
  hibrid`, ezért mindkét meglévő fajtaértéket rögzítettük.
- A St-Louis Kriek Lambic pontos gyártói termékadata 4,0%-os,
  élénk vörösesbarna lambicot igazol. Az `ismeretlen` alkoholtartalmat
  `4%`-ra, a téves `világos` színt `vörös, barna` értékre javítottuk.
- A Hobgoblin Gold és Ruby a gyártó sörkínálatának angol ale tételei;
  mindkettőnél felvettük a meglévő `ale` értéket. Az íz továbbra is
  `natúr`, mert a gyártó által leírt citrusos, karamelles és gyümölcsös
  jegyek nem hozzáadott ízesítések.
- A Szent András Málnás Búza gyártói leírása kifejezetten szűretlen,
  málnával érlelt búzasört igazol; a hiányzó szűretlen jelzőt pótoltuk.
- A Duvel közvetlen címkéje `Belgian Strong Blond`; a meglévő `ale` és
  `belga blond` értékekkel pontosítottuk. A Pannonhalmi Főapátság
  Quadrupel forráskategóriája `Magyar kisüzemi`, ezért a `kézműves`
  jelzőt igazra állítottuk.
- A Staropramen Premium cseh világos lager, ezért a négyes csomag
  rekordján az általános `sör` mellé felvettük a `lager` értéket.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **13**.
- Változatlanul hagyott rekord: **13** (`678797:4216187`,
  `678794:4216184`, `673037:4210427`, `760800:4298190`,
  `712613:4250003`, `684476:4221866`, `684485:4221875`,
  `712607:4249997`, `684680:4222070`, `747305:4284695`,
  `747395:4284785`, `684605:4221995`, `684608:4221998`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 13 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 12 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `678239:4215629` | szűretlen `hamis` → `igaz` |
| `678245:4215635` | fajta `sör, belga blond` → `sör, ale, belga blond` |
| `677732:4215122` | szín `egyéb` → `világos` |
| `677729:4215119` | fajta `sör` → `sör, lager, kellerbier` |
| `712610:4250000` | fajta `sör` → `sör, lager, ale` |
| `684620:4222010` | alkoholtartalom `ismeretlen` → `4%`; szín `világos` → `vörös, barna` |
| `679463:4216853` | fajta `sör` → `sör, ale` |
| `712715:4250105` | fajta `sör` → `sör, ale` |
| `689840:4227230` | szűretlen `hamis` → `igaz` |
| `693182:4230572` | fajta `sör` → `sör, ale, belga blond` |
| `747392:4284782` | kézműves `hamis` → `igaz` |
| `678251:4215641` | fajta `sör` → `sör, lager` |

### 121. köteg – Sör, radler és malátaital 251–275.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **25**.
- Helyi kép nélkül ellenőrzött rekord: **0**.
- A Balatonszentgyörgyi hatos válogatás közvetlen képén Pils, Málnás Búza,
  IPA, Mangó IPA és APA feliratú dobozok láthatók. Ezek alapján a meglévő
  `sör` mellé felvettük a `pilsner`, `búzasör`, `IPA` és `APA` értékeket,
  az ízeket `natúr, málna, mangó` értékre egészítettük ki, és a magyar
  kisüzemi forráskategóriával összhangban a `kézműves` jelzőt igazra
  állítottuk.
- Az Auchan Kedvenc Vidám Vadkan dobozán közvetlenül `Imperial Stout`
  olvasható. A fajtát `stout` értékkel egészítettük ki, a téves `világos`
  színt pedig `fekete` értékre javítottuk.
- A Welsenburg 5% pontos Auchan-termékadata lagerként nevezi meg a sört. A
  Budweiser Budvar Original dobozain `Czech Lager` olvasható; a
  Staropramen Premium és a Krušovice Original ugyancsak cseh világos
  lagerek. A hat érintett rekordnál az általános `sör` mellé felvettük a
  meglévő `lager` értéket.
- A Craft Boys Pack ablakában `Premium IPA` doboz látható, miközben a
  korabeli termékfelsorolás a gyümölcsös csomagot a Boys Packtől külön
  változatként kezeli. Ezért felvettük az `IPA` fajtát, a téves `vegyes
  gyümölcs` ízt pedig `natúr` értékre javítottuk. A Craft Fruit Pack és a
  Craft Girls Pack meglévő `vegyes gyümölcs` ízét a közvetlen csomagképek
  igazolták, ezért azok változatlanok maradtak.
- A Pannonhalmi Apátsági Sörválogatás pontos termékadata szerint a csomag
  Blonde 5%, Dubbel 6,5%, Tripel 8% és Quadrupel 10% tételeket tartalmaz.
  Az alkoholtartalmakat mind a négy értékkel rögzítettük, a fajtákat
  `ale`, `belga blond`, `dubbel`, `tripel` és `quadrupel` értékkel
  egészítettük ki, a téves gyümölcsízt `natúr` értékre, a csomag
  színkészletét pedig `világos, barna` értékre javítottuk.
- A Dreher gyártói oldala a Dreher 24 Epret 0,0%-os ízesített
  alkoholmentes sörként sorolja fel. Az alkoholtartalom és az eperíz már
  helyes volt; az alkoholstátuszt `alkoholos` értékről `alkoholmentes`
  értékre javítottuk.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **18**.
- Változatlanul hagyott rekord: **14** (`444394:3981778`,
  `761676:4299066`, `747251:4284641`, `680003:4217393`,
  `680018:4217408`, `680006:4217396`, `827516:4364906`,
  `827522:4364912`, `827519:4364909`, `824723:4362113`,
  `680000:4217390`, `712787:4250177`, `979535:4516925`,
  `678965:4216355`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 18 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 11 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `692993:4230383` | fajta `sör` → `sör, pilsner, búzasör, IPA, APA`; íz `natúr` → `natúr, málna, mangó`; kézműves `hamis` → `igaz` |
| `678791:4216181` | fajta `sör` → `sör, stout`; szín `világos` → `fekete` |
| `678287:4215677` | fajta `sör` → `sör, lager` |
| `679904:4217294` | fajta `sör` → `sör, lager` |
| `678200:4215590` | fajta `sör` → `sör, lager` |
| `679907:4217297` | fajta `sör` → `sör, lager` |
| `4735:4735` | fajta `sör` → `sör, lager` |
| `661485:4198875` | fajta `sör` → `sör, lager` |
| `979532:4516922` | fajta `sör` → `sör, IPA`; íz `vegyes gyümölcs` → `natúr` |
| `752013:4289403` | alkoholtartalom `ismeretlen` → `5%, 6,5%, 8%, 10%`; fajta `sör` → `sör, ale, belga blond, dubbel, tripel, quadrupel`; íz `vegyes gyümölcs` → `natúr`; szín `világos` → `világos, barna` |
| `1032332:4569722` | alkoholstátusz `alkoholos` → `alkoholmentes` |

### 122. köteg – Sör, radler és malátaital 276–300.

- Ellenőrzött új rekord: **25**.
- Helyben elérhető és megvizsgált közvetlen termékkép: **12**.
- Helyi kép nélkül ellenőrzött rekord: **13**.
- A Dreher gyártói oldala a Dreher Citrust 4%-os lagerként, citrom- és
  lime-ízzel írja le. Mindkét érintett rekordnál felvettük a `lager`
  fajtát; a kép nélküli Coop-rekord általános `citrus` ízét a két pontos
  gyümölcsértékre, ismeretlen színét `világos` értékre javítottuk.
- A Soproni Citrus közvetlen dobozcímkéjén `szűretlen lager` olvasható;
  a szűretlen jelző már helyes volt, a `lager` típust és a `világos`
  színt pótoltuk. A Soproni gyártói termékoldala a Klasszikus és a 0,0%-os
  változatot egyaránt lagerként nevezi meg; a két Klasszikus rekord
  fajtáját, valamint az alkoholmentes rekord fajtáját és világos színét
  ennek megfelelően javítottuk.
- A Staropramen Unfiltered gyártói adata 5%-os szűretlen világos lagerként
  azonosítja a terméket. A szűretlenség és a szín már helyes volt, a
  `lager` típust pótoltuk. A Staropramen Premium kép nélküli rekordjánál
  ugyanezt a típust a gyártó zászlóshajó-termékének `premium lager`
  besorolása igazolta.
- A Gösser Premium, Peroni, Coors, Birra Moretti, Stella Artois és Steffl
  pontos termékváltozatai világos lagerek; ezeknél az általános `sör`
  mellé felvettük a `lager` értéket. A képes Birra Moretti címkéjén
  közvetlenül `Premium Lager` olvasható.
- A Van Pur Non-alco gyártói oldala a pontos 500 ml-es terméket 0,5%-os,
  könnyű, világos alkoholmentes sörként írja le; a gyártói kínálat ezt
  alkoholmentes lagerként sorolja. Az alkoholtartalmat `0%` értékről
  `0,5%` értékre, a fajtát `sör, lager`, a színt `világos` értékre
  javítottuk.
- A Tuborg Green gyártói termékadata a 4,6%-os változat típusát
  kifejezetten `Pilsner` értékkel adja meg, ezért a meglévő `sör` mellé a
  `pilsner` fajtát vettük fel.
- A 1664 Blanc gyártói adata búzasört, citrusos ízt, narancshéjat és
  koriandert, valamint ködös megjelenést igazol. A `búzasör` fajta és a
  világos szín már helyes volt; a téves `natúr` ízt a fában már
  engedélyezett `citrus` értékre, a szűretlen jelzőt igazra javítottuk. A
  külön `narancs` és `koriander` értéket nem vettük fel, mert ebben az
  ágban nem voltak engedélyezettek, a meglévő `citrus` pedig pontosan
  lefedi az igazolt termékízt.
- Módosított rekord: **17**.
- Módosított tulajdonságmező: **24**.
- Változatlanul hagyott rekord: **8** (`788933:4326323`,
  `780734:4318124`, `2818050`, `2818048`, `2810971`, `2810970`,
  `2808669`, `2808559`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 24 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 17 végleges írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1032326:4569716` | fajta `sör` → `sör, lager` |
| `3380715` | fajta `sör` → `sör, lager`; íz `citrus` → `citrom, lime`; szín `egyéb` → `világos` |
| `3380678` | fajta `sör` → `sör, lager` |
| `3379590` | fajta `sör` → `sör, lager`; szín `egyéb` → `világos` |
| `3373918` | fajta `sör` → `sör, lager` |
| `3140087` | fajta `sör` → `sör, lager` |
| `3091148` | alkoholtartalom `0%` → `0,5%`; fajta `sör` → `sör, lager`; szín `egyéb` → `világos` |
| `3090985` | fajta `sör` → `sör, lager` |
| `3090979` | fajta `sör` → `sör, lager` |
| `2905337` | fajta `sör` → `sör, pilsner` |
| `2817537` | fajta `sör` → `sör, lager` |
| `2817126` | fajta `sör` → `sör, lager` |
| `2812861` | fajta `sör` → `sör, lager` |
| `2810969` | fajta `sör` → `sör, lager` |
| `2810173` | fajta `sör` → `sör, lager`; szín `egyéb` → `világos` |
| `2809945` | fajta `sör` → `sör, lager` |
| `2808668` | íz `natúr` → `citrus`; szűretlen `hamis` → `igaz` |

### Sör kézi felülvizsgálat, 301–325. tétel

- A 25 teljes termékrekordot, a hozzájuk tartozó forrássorokat, neveket,
  jelenlegi kategóriákat és tulajdonságokat egyenként ellenőriztük. Az 5
  elérhető helyi termékképet közvetlenül, eredeti vagy részletes
  felbontásban is megvizsgáltuk; 20 rekordhoz nem volt helyi kép.
- A Dreher Gold, Borsodi, Arany Ászok, Heineken, Gösser Premium, Arany
  Fácán, Kőbányai és Krušovice Světlé pontos változatai világos lagerek.
  A színük már helyes volt, az általános `sör` mellé a `lager` fajtát
  pótoltuk. A Heineken második kiszerelésén ugyanezt a javítást végeztük.
- A Gösser NaturZitrone 0,0%-os és 2%-os gyártói termékadata mindkét
  változatot citromos NaturRadlerként azonosítja, és a valódi citromlé
  okozta természetes fátyolosságot is leírja. A már helyes citromíz
  mellett a fajtát `radler`, a színt `világos`, a szűretlen jelzőt igaz
  értékre javítottuk.
- A Mort Subite Kriek gyártói leírása vörös színt ad meg; a már helyes
  `lambic` fajta és meggyíz mellett az ismeretlen színt `vörös` értékre
  pontosítottuk.
- A Heineken 0.0 pontos terméke alkoholmentes világos lager; a
  `lager` fajtát és a `világos` színt pótoltuk.
- Az Argus El Bravos közvetlen palackcímkéjén `5,9%` olvasható, a
  folyadék világos aranyszínű. Az alkoholtartalmat `5%` értékről
  `5,9%` értékre, a színt `egyéb` értékről `világos` értékre
  javítottuk. Mindkét célérték már engedélyezett volt a fában.
- A Beck's pontos termékváltozata pilsner; a meglévő `sör` mellé a
  `pilsner` fajtát pótoltuk.
- A generikus nevű Soproni 0% rekord közvetlen termékképe a
  `Citrom 0.0` Radler változatot mutatja. A fajtát `sör` értékről
  `radler`, az ízt `natúr` értékről `citrom` értékre javítottuk.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **23**.
- Változatlanul hagyott rekord: **9** (`2808554`, `2808493`, `2807651`,
  `2807640`, `2807639`, `2807638`, `2807542`, `2807539`, `2806930`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 23 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; mind a 16 végleges írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `2808558` | fajta `sör` → `sör, lager` |
| `2808550` | fajta `sör` → `sör, lager` |
| `2808547` | fajta `sör` → `sör, lager` |
| `2808476` | fajta `sör` → `sör, lager` |
| `2808475` | fajta `sör` → `sör, lager` |
| `2808474` | fajta `sör` → `sör, lager` |
| `2808472` | fajta `sör` → `radler`; szín `egyéb` → `világos`; szűretlen `hamis` → `igaz` |
| `2807772` | fajta `sör` → `sör, lager` |
| `2807649` | szín `egyéb` → `vörös` |
| `2807648` | fajta `sör` → `sör, lager` |
| `2807647` | fajta `sör` → `sör, lager` |
| `2807636` | fajta `sör` → `radler`; szín `egyéb` → `világos`; szűretlen `hamis` → `igaz` |
| `2807525` | fajta `sör` → `sör, lager`; szín `egyéb` → `világos` |
| `10101675` | alkoholtartalom `5%` → `5,9%`; szín `egyéb` → `világos` |
| `10101681` | fajta `sör` → `sör, pilsner` |
| `10104535` | fajta `sör` → `radler`; íz `natúr` → `citrom` |

### Sör kézi felülvizsgálat, 326–350. tétel

- A 25 teljes termékrekordot, a forrássorokat, neveket, jelenlegi
  kategóriákat és tulajdonságokat egyenként ellenőriztük. Mind a 25
  rekordhoz volt helyi termékkép; ezeket közvetlenül, részletes
  felbontásban is megvizsgáltuk.
- A Holsten és a Budweiser közvetlen címkéjén `Lager Beer`, illetve
  `Czech Lager` olvasható. A The Crafty Brewing Co. címkéje `Lager`
  stílust, a pontos termékadat 5%-os alkoholtartalmat igazol; mindhárom
  rekordnál pótoltuk a `lager` fajtát, a Crafty rekordnál az
  alkoholtartalmat is.
- A Leute közvetlen csomagképe belga barna bokbiert mutat, a pontos
  termékadat pedig 7,5%-os, felsőerjesztésű erős ale-ként írja le. A már
  helyes alkoholtartalom mellett a fajtát `sör, ale, bak`, a téves
  világos színt `barna` értékre javítottuk.
- A Perlenbacher 5 literes party hordó pontos Lidl-termékadata 4,9%-os
  Pilst igazol; az ismeretlen alkoholtartalmat és az általános fajtát
  ennek megfelelően pontosítottuk.
- A Hübris többváltozatos rekordjánál a Lidl-ajánlat a Müggy, Rüdler és
  Hüpped alkoholtartalmát 4,2%, 3,2% és 6% értékkel közli. A gyártói
  oldalak a Müggyt meggyes pale ale-ként, a Rüdlert citromos-grapefruitos
  radlerként, a Hüppedet citrusos-trópusi, ködös DDH Cold IPA-ként
  azonosítják. A három változat összes igazolt értékét felvettük, a színt
  `világos, vörös`, a kézműves és szűretlen jelzőt igaz értékre
  javítottuk.
- A Mad Scientist rekord három külön változatot fog össze. A Liquid
  Cocaine közvetlen dobozcímkéje és gyártói adatlapja 9%-os Double IPA-t,
  a Matrix Blue Pill pontos adata 7%-os West Coast IPA-t, a Matrix Red
  Pill pontos adata 3,5%-os, eperrel és lime-mal készített braggotot
  igazol. Az alkoholtartalom-, fajta- és ízlistát mindhárom változatra
  kiegészítettük, a félrevezetően egyetlen `vörös` színt a vegyes
  kínálatot jelző `egyéb` értékre, a kézműves jelzőt igazra javítottuk.
- A Horizont rekordnál a Rebel Berry 4,5%-os málnás Sour Ale, a Hazy
  Queen 6%-os New England IPA, a Gentle Bastard 6,5%-os West Coast IPA.
  A három alkoholtartalmat, stílust és az igazolt málna-, citrus- és
  trópusigyümölcs-jegyeket felvettük, a kézműves jelzőt igazra
  javítottuk.
- A Gösser Natur Zitrone 0,0%-os változatánál a már helyes radler- és
  citromérték mellett a gyártói leírásból igazolt `világos` színt és
  szűretlenséget pótoltuk.
- A Borsodi két kiszerelésén, a Heineken csomagon, az Argus 2 literes,
  a Gösser Premium és a Kőbányai 2 literes rekordján a közvetlen
  címkék és a pontos terméktípus alapján a `lager` fajtát pótoltuk.
  A Krombacher csomag pontos Pils-terméke `pilsner` fajtát kapott.
- Az Argus Panaché közvetlen képe és Lidl-termékadata sörrel kevert
  citromos limonádét igazol. A fajta `radler`, az íz `citrom`, a szín
  `világos` lett. A címke csak 1% alatti tartományt közöl, ezért az
  alkoholtartalmat nem becsültük meg, az `ismeretlen` értéket
  megtartottuk.
- A Miller többváltozatos rekordja egy natúr 4,7%-os világos lagert és
  egy 4%-os lime-os változatot fog össze; a már helyes két
  alkoholtartalom mellett a `lager` fajtát és a hiányzó `natúr` ízt
  pótoltuk. A Duff pontos Lidl-ajánlata 4,9%-os világos lagert igazol;
  az alkoholtartalmat és a fajtát ennek megfelelően javítottuk.
- Módosított rekord: **19**.
- Módosított tulajdonságmező: **39**.
- Változatlanul hagyott rekord: **6** (`10106276`, `10107367`,
  `10107383`, `BTY-X17457400320021`, `BTY-X17337000320021`,
  `BTY-X17577400320021`).
- Új megengedett érték: **3** (`fajta: Cold IPA, braggot, sour ale`).
- Törölt megengedett érték: **0**.
- A 39 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 19 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `10106402` | fajta `sör` → `sör, lager` |
| `10106408` | fajta `sör` → `sör, lager` |
| `10107315` | alkoholtartalom `ismeretlen` → `5%`; fajta `sör` → `sör, lager` |
| `10107329` | fajta `sör` → `sör, ale, bak`; szín `világos` → `barna` |
| `10107333` | alkoholtartalom `ismeretlen` → `4,9%`; fajta `sör` → `sör, pilsner` |
| `10107369` | alkoholtartalom `ismeretlen` → `3,2%, 4,2%, 6%`; fajta `sör` → `sör, pale ale, radler, Cold IPA`; íz `citrom, meggy` → `citrom, citrus, grapefruit, meggy, trópusi gyümölcs`; szín `egyéb` → `világos, vörös`; kézműves `hamis` → `igaz`; szűretlen `hamis` → `igaz` |
| `10107371` | alkoholtartalom `ismeretlen` → `3,5%, 7%, 9%`; fajta `sör` → `sör, braggot, double IPA, West Coast IPA`; íz `vegyes gyümölcs` → `citrus, eper, lime, vegyes gyümölcs`; szín `vörös` → `egyéb`; kézműves `hamis` → `igaz` |
| `10107373` | alkoholtartalom `ismeretlen` → `4,5%, 6%, 6,5%`; fajta `sör, IPA` → `sör, sour ale, New England IPA, West Coast IPA`; íz `erdei gyümölcs` → `citrus, málna, trópusi gyümölcs`; kézműves `hamis` → `igaz` |
| `10107375` | szín `egyéb` → `világos`; szűretlen `hamis` → `igaz` |
| `10107377` | fajta `sör` → `sör, lager` |
| `10107379` | fajta `sör` → `sör, pilsner` |
| `10107381` | fajta `sör` → `sör, lager` |
| `10107425` | fajta `sör` → `radler`; íz `natúr` → `citrom`; szín `egyéb` → `világos` |
| `10107429` | fajta `sör` → `sör, lager` |
| `10107949` | fajta `sör` → `sör, lager`; íz `lime` → `natúr, lime` |
| `10107951` | alkoholtartalom `ismeretlen` → `4,9%`; fajta `sör` → `sör, lager` |
| `BTY-X17569000320021` | fajta `sör` → `sör, lager` |
| `BTY-X17482800320021` | fajta `sör` → `sör, lager` |
| `BTY-X17336100320021` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 351–375. tétel

- A 25 teljes termékrekordot, forrássort, nevet, jelenlegi kategóriát és
  tulajdonságkészletet egyenként ellenőriztük. Mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban is megvizsgáltuk.
- A Dreher Gold négy kiszerelésén, a Heineken Silver és Heineken Original
  négy kiszerelésén, a Borsodi Bivaly és Mester, a Peroni Nastro Azzurro,
  a Stella Artois két kiszerelése, a Soproni Klasszikus két kiszerelése,
  a Hofbräu München Premium, a Gösser Premium és a Kőbányai pontos
  termékeinél a közvetlen címke, a terméknév és a forrás `Lager/Pils`
  besorolása lagert igazol. Az általános `sör` mellé a `lager` fajtát
  pótoltuk.
- A Tuborg Green közvetlen termékképe és már ellenőrzött pontos gyártói
  termékadata pilsnert igazol; a meglévő `sör` mellé a `pilsner` fajtát
  pótoltuk.
- A Löwenbräu Lager, Carlsberg Danish Pilsner, Pécsi Prémium Lager,
  Pécsi Prémium Pils Szűretlen, Zipfer Pils és Miller Lime rekordja
  minden vizsgált mezőben már helyes volt, ezért változatlan maradt.
- Módosított rekord: **19**.
- Módosított tulajdonságmező: **19**.
- Változatlanul hagyott rekord: **6** (`BTY-X17568900320021`,
  `BTY-X17472400320021`, `BTY-X17499500320021`,
  `BTY-X17499700320021`, `BTY-X17528900320021`,
  `BTY-X17447200320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 19 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 19 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17427300320021` | fajta `sör` → `sör, lager` |
| `BTY-X17307900320021` | fajta `sör` → `sör, lager` |
| `BTY-X17568200320021` | fajta `sör` → `sör, lager` |
| `BTY-X17629100320021` | fajta `sör` → `sör, lager` |
| `BTY-X18445400320021` | fajta `sör` → `sör, lager` |
| `BTY-X17482900320021` | fajta `sör` → `sör, lager` |
| `BTY-X8951600320021` | fajta `sör` → `sör, lager` |
| `BTY-X98599200320021` | fajta `sör` → `sör, lager` |
| `BTY-X1677800320021` | fajta `sör` → `sör, lager` |
| `BTY-X17483000320021` | fajta `sör` → `sör, lager` |
| `BTY-X17568400320021` | fajta `sör` → `sör, lager` |
| `BTY-X17336500320021` | fajta `sör` → `sör, lager` |
| `BTY-X96759600320021` | fajta `sör` → `sör, lager` |
| `BTY-X68475200320021` | fajta `sör` → `sör, lager` |
| `BTY-X17472800320021` | fajta `sör` → `sör, pilsner` |
| `BTY-X47033000320021` | fajta `sör` → `sör, lager` |
| `BTY-X15304900320021` | fajta `sör` → `sör, lager` |
| `BTY-X17308100320021` | fajta `sör` → `sör, lager` |
| `BTY-X17337200320021` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 376–400. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Heineken két normál kiszerelése, a Kőbányai, Steffl, Borsodi,
  Staropramen szűretlen és Premium, Arany Ászok, Arany Fácán, Gösser
  Premium, Soproni 1895, Szalon és Coors két kiszerelése pontos világos
  lager. Az általános `sör` mellé a `lager` fajtát pótoltuk.
- A Heineken 6×250 ml-es csomag közvetlen csomagképén `Premium
  Pilsener`, a Beck's pontos termékváltozatánál pilsner stílus igazolt;
  ezeknél a `pilsner` fajtát pótoltuk.
- A Pilsner Urquell három kiszerelése, a Kozel Premium Lager, Carlsberg
  Pilsner, BE(er) Cool Lager, Laško Zlatorog Lager és Zlaty Bazant Lager
  rekordja már minden vizsgált mezőben pontos volt.
- Módosított rekord: **17**.
- Módosított tulajdonságmező: **17**.
- Változatlanul hagyott rekord: **8** (`BTY-X65077000320021`,
  `BTY-X17336000320021`, `BTY-X17384300320021`,
  `BTY-X17470300320022`, `BTY-X17500300320021`,
  `BTY-X1752200320021`, `BTY-X17528500320021`,
  `BTY-X17594400320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 17 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 17 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X8946700320021` | fajta `sör` → `sör, lager` |
| `BTY-X75824100320021` | fajta `sör` → `sör, lager` |
| `BTY-X17483300320021` | fajta `sör` → `sör, lager` |
| `BTY-X72221800320021` | fajta `sör` → `sör, lager` |
| `BTY-X17567800320021` | fajta `sör` → `sör, lager` |
| `BTY-X17335000320021` | fajta `sör` → `sör, lager` |
| `BTY-X28470400320021` | fajta `sör` → `sör, lager` |
| `BTY-X17308400320021` | fajta `sör` → `sör, lager` |
| `BTY-X14705500320021` | fajta `sör` → `sör, lager` |
| `BTY-X15303800320021` | fajta `sör` → `sör, lager` |
| `BTY-X17307800320021` | fajta `sör` → `sör, pilsner` |
| `BTY-X17308000320021` | fajta `sör` → `sör, lager` |
| `BTY-X17308300320021` | fajta `sör` → `sör, lager` |
| `BTY-X17499400320021` | fajta `sör` → `sör, lager` |
| `BTY-X17568300320021` | fajta `sör` → `sör, lager` |
| `BTY-X17568700320021` | fajta `sör` → `sör, pilsner` |
| `BTY-X17568800320021` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 401–425. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Amstel pontos dobozcímkéje pilsnert, a Borsodi, Singha, Staropramen
  Unfiltered és Dark, Arany Ászok pedig lagert igazol; a Tuborg pontos
  változata pilsner. A hiányzó fajtákat pótoltuk.
- A Szent András Monarchista teljes neve, közvetlen címkéje és gyártói
  oldala `imperial pilsner` stílust igazol. A Magyar Vándor
  lager–ale hibrid besorolása helyes volt; mindkét Szent András tételnél,
  valamint a Fehér Nyúl Hellesnél a kézműves jelzőt javítottuk.
- A Miller vegyes válogatás négy 330 ml-es, natúr és lime-os
  változatokat tartalmazó csomag. A Staropramen 24×330 ml-es termék teljes
  neve 7 920 ml-es összkiszerelést és 24 darabot bizonyít; mindkét
  csomagadatot javítottuk.
- A Szent András Hegemón gyártói oldala szűretlen, sevillai
  narancshéjjal és korianderrel készülő dubbelwitet, a Hübris saját oldala
  ködös, citrusos-fűszeres Belgian Wit Beert ír le. Mindkettőnél pótoltuk
  a `witbier`, `citrus`, `fűszeres`, `kézműves` és `szűretlen`
  információk közül a hiányzókat. A Schöfferhofer közvetlen címkéjén a
  `Naturtrüb` jelölés igazolta a szűretlenséget.
- Az Estrella Galicia gyártói oldala a pontos 5,5%-os terméket Helles
  Exportbierként és lagerként azonosítja, ezért a `lager` és `helles`
  fajtát pótoltuk.
- A Pécsi Premium Wheat, Szent András 1993, Paulaner Weissbier,
  Krušovice Černé, Primátor Double 24 és a három Soproni Óvatos Duhaj
  rekordja már minden vizsgált mezőben pontos volt. A Primátornál a
  gyártói forrás különleges barna sört közöl, ezért nem vezettünk le
  bizonyítatlan porter- vagy stout-stílust.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **27**.
- Változatlanul hagyott rekord: **9** (`BTY-X18380800320021`,
  `BTY-X17600500320021`, `BTY-X17499200320021`,
  `BTY-X18686400320021`, `BTY-X17362600320021`,
  `BTY-X18905900320021`, `BTY-X17303200320021`,
  `BTY-X17483100320021`, `BTY-X17202900320021`).
- Új megengedett érték: **3** (`fajta: imperial pilsner, witbier`;
  `íz: fűszeres`).
- Törölt megengedett érték: **0**.
- Az első alkalmazási futás a Hegemón rekordnál jelezte, hogy a
  `fűszeres` a teljes kategóriafában már létezett, de a sörlevél
  ízértékei között még nem volt engedélyezve. Az érintett rekord
  automatikusan visszaállt; a közvetlen termék- és gyártói bizonyíték
  alapján az elemi értéket felvettük a sörlevélre, majd a teljes futást
  sikeresen megismételtük.
- A 27 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 16 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17627800320021` | fajta `sör` → `sör, pilsner` |
| `BTY-X17690300320021` | fajta `sör` → `sör, lager` |
| `BTY-X17887600320021` | fajta `sör, pilsner` → `sör, pilsner, imperial pilsner`; kézműves `false` → `true` |
| `BTY-X17887700320021` | kézműves `false` → `true` |
| `BTY-X18308100320021` | fajta `sör` → `sör, lager` |
| `BTY-X18344000320021` | kézműves `false` → `true` |
| `BTY-X18360900320021` | fajta `sör` → `sör, pilsner` |
| `BTY-X18547800320021` | alkoholtartalom `4,7%` → `4%, 4,7%`; fajta `sör` → `sör, lager`; íz `natúr` → `natúr, lime` |
| `BTY-X4674500320021` | kiszerelés `330 ml` → `7920 ml`; fajta `sör` → `sör, lager`; csomagdarabszám `1` → `24` |
| `BTY-X66353600320021` | fajta `sör` → `sör, lager` |
| `BTY-X17567700320021` | fajta `sör` → `sör, lager` |
| `BTY-X17887400320021` | fajta `sör, búzasör, ale` → `sör, búzasör, witbier, ale`; íz `natúr` → `citrus, fűszeres`; kézműves `false` → `true`; szűretlen `false` → `true` |
| `BTY-X17890500320021` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres`; kézműves `false` → `true`; szűretlen `false` → `true` |
| `BTY-X18315200320021` | szűretlen `false` → `true` |
| `BTY-X17567600320021` | fajta `sör` → `sör, lager` |
| `BTY-X17824700320021` | fajta `sör` → `sör, lager, helles` |

### Sör kézi felülvizsgálat, 426–436. tétel

- A sörág utolsó 11 teljes rekordját és forrássorát egyenként,
  mind a 11 helyi termékképet közvetlenül, részletes felbontásban
  ellenőriztük.
- A Krušovice Originál egyedi és 20×500 ml-es kiszerelésének közvetlen
  címkéje, valamint a gyártó alsóerjesztésű `Světlé` termékadata
  világos lagert igazol; a `lager` fajtát pótoltuk.
- A Szent András Laza Morál gyártói oldala Session IPA-ként,
  kézművesként és szeparált, de szűretlen sörként írja le a pontos
  terméket. A fajta már helyes volt, a két logikai jelzőt javítottuk.
- A Bernard Bohemian Ale közvetlen címkéje és gyártói oldala 8,2%-os,
  korianderrel készülő felsőerjesztésű sört igazol; a `fűszeres` ízt
  pótoltuk. A Bernard IPA rekordja már pontos volt.
- A 1664 Rosé gyártói összetevőlistája málna- és bodzalevet,
  narancshéjat és koriandert közöl, hivatalos megjelenésadata pedig
  rosépiros, más gyártói oldalon élénk rubinvörös színt. A hiányzó
  `bodza`, `citrus`, `fűszeres` ízeket és a `vörös` színt pótoltuk.
- A Gösser Natur Zitrone 2%-os változatát a már korábban ellenőrzött
  gyártói termékadat citromos NaturRadlerként, természetesen fátyolos
  italként azonosítja; a fajtát `radler`, a szűretlen jelzőt igaz
  értékre javítottuk.
- Az Almás Rétes gyártói oldala almával, vaníliával és fahéjjal készülő
  pastry ale-t igazol, ezért az `ale` fajtát és a fahéjat lefedő
  `fűszeres` ízt pótoltuk. A Málnás Búza gyártói adata 25% málnával és
  5% almával készülő, vöröses színű szűretlen bajor búzasört közöl;
  pótoltuk az `ale`, `alma`, `vörös` és `kézműves` adatokat.
- A két Garage ízesített malátasör azonos termékváltozatait korábbi
  bolti duplikátumaiknál már közvetlen képpel, változatlanul helyesnek
  minősítettük; a jelenlegi két rekord ugyanazokat a pontos értékeket
  tartalmazta.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **15**.
- Változatlanul hagyott rekord: **3** (`BTY-X18315100320021`,
  `BTY-X17473000320021`, `BTY-X17473100320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 15 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 8 végleges
  írás sikeres volt.
- Ezzel a `Sör, radler és malátaital` altípus első **436** rekordjának
  kézi ellenőrzése elkészült; az altípus jelenlegi teljes mérete
  **1 013** rekord.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17358400320021` | fajta `sör` → `sör, lager` |
| `BTY-X17600600320021` | kézműves `false` → `true`; szűretlen `false` → `true` |
| `BTY-X18315000320021` | íz `natúr` → `fűszeres` |
| `BTY-X7725700320021` | fajta `sör` → `sör, lager` |
| `BTY-X18076500320021` | íz `málna` → `bodza, citrus, fűszeres, málna`; szín `világos` → `vörös` |
| `BTY-X17176800320021` | fajta `sör` → `radler`; szűretlen `false` → `true` |
| `BTY-X17600900320021` | fajta `sör` → `sör, ale`; íz `alma` → `alma, fűszeres` |
| `BTY-X17601100320021` | fajta `sör, búzasör` → `sör, búzasör, ale`; íz `málna` → `alma, málna`; szín `világos` → `vörös`; kézműves `false` → `true` |

### Sör kézi felülvizsgálat, 437–461. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Hübris Rüdler közvetlen dobozcímkéje és gyártói oldala grapefruitos
  radlert igazol; a gyártói összetevőlista valódi citromlevet is közöl,
  a főzde pedig kézműves radlerként írja le. A `citrom` ízt és a
  kézműves jelzőt pótoltuk.
- A 1664 Rosé 330 ml-es változatánál ugyanaz a gyártói összetevő- és
  megjelenésadat érvényes, mint az előző köteg 500 ml-es tételénél:
  bodza, málna, narancshéj, koriander és rosépiros szín. A hiányzó
  `citrus`, `fűszeres` és `vörös` értékeket pótoltuk.
- A Free Damm Limón címkéje 0,0%-os citromos alkoholmentes sört, a
  világos termékkép világos színt igazol; csak a hibás `egyéb` színt
  javítottuk.
- A 1664 Blanc mindkét kiszerelésének magyar gyártói oldala
  narancshéjat és koriandert tartalmazó, ködös búzasört közöl. A
  `citrus`, `fűszeres` és szűretlen adatok közül a hiányzókat pótoltuk.
- A Peroni Stile Capri gyártói sajtóanyaga 4,2%-os, könnyű, citromos
  lagert igazol. A Birra Moretti közvetlen címkéje `Premium Lager`;
  mindkettőnél pótoltuk a hiányzó fajtát, a Stile Caprinál a
  `citrom` ízt is.
- A Lindemans Kriek közvetlen palackja meggyes lambicot és vörös
  folyadékot igazol; a színt javítottuk. A DAB két közvetlen dobozcímkéje
  `Dortmunder Export`, illetve `Dortmunder Dark`; mindkettőhöz a
  `lager` és `dortmunder` fajtát pótoltuk.
- Az Inedit rekord bolti neve keverte az Estrella Galicia és az Inedit
  Damm neveket, miközben a közvetlen palack és a Damm saját
  összetevőadata egyértelműen Inedit Damm terméket igazol. A márkát
  `Estrella Damm` értékre javítottuk; a gyártói és pontos termékadatok
  alapján a lager–búzasör/witbier keveréket, a narancshéj és koriander
  ízét, valamint a ködös megjelenést is pótoltuk.
- A Miller 500 ml-es kiszerelésén, a Peroni Nastro Azzurro, Corona,
  Mythos és Primátor Premium rekordján a közvetlen címke pontos lagert
  igazol; a hiányzó `lager` fajtát pótoltuk.
- A Primátor Tchyně gyártói oldala szűretlen, arany-réz/borostyán színű
  India Pale Lagert ír le; a fajtát, színt és szűretlen jelzőt ennek
  megfelelően javítottuk.
- A Primátor Chipper, Guinness Draught Stout, Miller 330 ml, Edelweiss
  Hefetrüb, Budvar Premium és Dark Lager, Primátor Weizen, valamint
  Pécsi gluténmentes bio lager rekordja már pontos volt.
- Módosított rekord: **17**.
- Módosított tulajdonságmező: **27**.
- Változatlanul hagyott rekord: **8** (`BTY-X18705900320022`,
  `BTY-X17715900320021`, `BTY-X17569500320021`,
  `BTY-X17464900320021`, `BTY-X17471600320021`,
  `BTY-X17471700320021`, `BTY-X15306800320021`,
  `BTY-X17499800320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 27 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 17 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17890700320021` | íz `grapefruit` → `citrom, grapefruit`; kézműves `false` → `true` |
| `BTY-X18076300320021` | íz `bodza, málna` → `bodza, citrus, fűszeres, málna`; szín `világos` → `vörös` |
| `BTY-X18344300320021` | szín `egyéb` → `világos` |
| `BTY-X17470400320021` | íz `natúr` → `citrus, fűszeres`; szűretlen `false` → `true` |
| `BTY-X17472500320021` | íz `natúr` → `citrus, fűszeres`; szűretlen `false` → `true` |
| `BTY-X17337300320021` | fajta `sör` → `sör, lager`; íz `natúr` → `citrom` |
| `BTY-X17481700320021` | fajta `sör` → `sör, lager` |
| `BTY-X17573800320021` | szín `világos` → `vörös` |
| `BTY-X17577900320021` | fajta `sör` → `sör, lager, dortmunder` |
| `BTY-X17578300320021` | márka `Estrella Galicia` → `Estrella Damm`; fajta `sör` → `sör, lager, búzasör, witbier`; íz `natúr` → `citrus, fűszeres`; szűretlen `false` → `true` |
| `BTY-X17581000320021` | fajta `sör` → `sör, lager, dortmunder` |
| `BTY-X17569400320021` | fajta `sör` → `sör, lager` |
| `BTY-X17336400320021` | fajta `sör` → `sör, lager` |
| `BTY-X17715700320021` | fajta `sör` → `sör, lager` |
| `BTY-X17472200320021` | fajta `sör` → `sör, lager` |
| `BTY-X15306700320021` | fajta `sör` → `sör, lager` |
| `BTY-X15307100320021` | fajta `sör` → `sör, lager, India pale lager`; szín `világos` → `borostyán`; szűretlen `false` → `true` |

### Sör kézi felülvizsgálat, 462–486. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Estrella Damm közvetlen palackcímkéje feloldja a bolti név
  Estrella Galicia–Estrella Damm keverését; a márkát `Estrella Damm`
  értékre, a fajtát lagerre javítottuk. Az Asahi Super Dry két
  kiszerelésének gyártói adata `Premium Lager`, a Karlovačko közvetlen
  címkéje `Lager`, a Desperados gyártói oldala pedig agávés lagert
  igazol; mindegyiknél pótoltuk a hiányzó `lager` fajtát.
- A Duvel közvetlen címkéje erős belga blond ale-t igazol, ezért a már
  helyes `ale` mellé felvettük a `belga blond` fajtát.
- Az Az Én Söröm Meggyes közvetlen címkéje kézműves sört jelöl. A
  Hübris Üpa, Müggy és Sür a főzde saját termékei; mindháromnál
  javítottuk a kézműves jelzőt, az Üpa gyártói megjelenésadata alapján
  pedig a színt borostyánra. Az Üpa citrusos komlójegye nem hozzáadott
  ízesítés, ezért az `íz: natúr` értéket változatlanul hagytuk.
- A Horizont Gentle Bastard közvetlen címkéje és gyártói oldala West
  Coast IPA-t, a terméknév szűretlen sört igazol. A részletes fajtát és
  a kézműves jelzőt pótoltuk; a citrusos kóstolási jegyet itt sem
  kezeltük hozzáadott termékízként.
- A Hoegaarden közvetlen címkéje természetesen ködös fehér búzasört, a
  pontos termékadat narancshéjat és koriandert igazol. A `witbier`
  fajtát, a `citrus, fűszeres` ízeket és a szűretlen jelzőt pótoltuk.
  A Fehér Nyúl RAFA kézműves jelzőjét a közvetlen márka- és termékadat
  alapján javítottuk.
- A Hobgoblin Stout közvetlen címkéje fekete stoutot, a Hobgoblin Ruby
  vörös ale-t igazol. A DAB címkéje `Dortmunder Export`, ezért a
  `lager, dortmunder` fajtákat pótoltuk. Az Erdinger Dunkel gyártói
  anyaga élesztős-fátyolos búzasört közöl, így a szűretlen jelzőt igaz
  értékre javítottuk. A Köstritzer címkéje fekete lagerként azonosítja
  a terméket; a fajtát és a színt ennek megfelelően pontosítottuk.
- A Primátor IPA, Mort Subite Kriek, Apostel Weissbier, Az Én Söröm
  Prémium IPA, Krombacher Pils, Leffe Blonde és Erdinger Weißbier
  rekordja már pontos volt.
- Módosított rekord: **18**.
- Módosított tulajdonságmező: **24**.
- Változatlanul hagyott rekord: **7** (`BTY-X15307000320021`,
  `BTY-X17362700320021`, `BTY-X15315800320021`,
  `BTY-X17281000320021`, `BTY-X17528400320021`,
  `BTY-X17569100320021`, `BTY-X17578600320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 24 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 18 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17524200320021` | márka `Estrella Galicia` → `Estrella Damm`; fajta `sör` → `sör, lager` |
| `BTY-X17335100320021` | fajta `sör` → `sör, lager` |
| `BTY-X17587900320021` | fajta `sör, ale` → `sör, ale, belga blond` |
| `BTY-X17175000320021` | fajta `sör` → `sör, lager` |
| `BTY-X17280700320021` | kézműves `false` → `true` |
| `BTY-X17335200320021` | fajta `sör` → `sör, lager` |
| `BTY-X17361000320021` | szín `világos` → `borostyán`; kézműves `false` → `true` |
| `BTY-X17361100320021` | kézműves `false` → `true` |
| `BTY-X17361200320021` | kézműves `false` → `true` |
| `BTY-X17527700320021` | fajta `sör, IPA` → `sör, IPA, West Coast IPA`; kézműves `false` → `true` |
| `BTY-X17528300320021` | fajta `sör` → `sör, lager` |
| `BTY-X17569200320021` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres`; szűretlen `false` → `true` |
| `BTY-X17572000320021` | kézműves `false` → `true` |
| `BTY-X17573600320021` | szín `barna` → `fekete` |
| `BTY-X17577800320021` | fajta `sör` → `sör, lager, dortmunder` |
| `BTY-X17578700320021` | szűretlen `false` → `true` |
| `BTY-X17579000320021` | fajta `sör` → `sör, lager`; szín `barna` → `fekete` |
| `BTY-X17579300320021` | fajta `sör` → `sör, ale` |

### Sör kézi felülvizsgálat, 487–511. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Kaiserdom Kellerbier neve és címkéje szűretlen lagert, a Kirin
  Ichiban, a Flensburger Gold és a Pražačka közvetlen címkéje lagert
  igazol; a hiányzó `lager` fajtákat pótoltuk. A Bitburger 500 ml-es
  doboza `Premium Pils`, ezért a hiányzó `pilsner` fajtát felvettük.
- A Daura palackja szó szerint `Daura Damm Gluten-Free Lager Beer`;
  ezért a bolti névben kevert Estrella Galicia márkát a kategóriafában
  már létező `Daura Damm` értékre javítottuk, és a `lager` fajtát is
  pótoltuk.
- Az Apostel Weissbier Hell pontos termékadata Hefeweizent, a
  termékmegjelenés fátyolos sört igazol; a hiányzó szűretlen jelzőt
  pótoltuk. Az Apostel Weissbier Dunkel közvetlen címkéje alapján a már
  helyes `dunkel` mellé a hiányzó `búzasör` fajtát is felvettük.
- A Horizont Hop Session IPA közvetlen címkéje és márkaadata alapján a
  kézműves jelzőt igaz értékre javítottuk; a fajta és szűretlenség már
  pontos volt.
- A Bernard gluténmentes termékének közvetlen palackcímkéje
  `Gluten Free Lager`, ezért a hiányzó `lager` fajtát pótoltuk. A
  Celebration, Dark és Amber Lager rekordjai már pontosak voltak.
- A Hobgoblin Gold gyártói és márkatulajdonosi oldala `Golden Ale`
  stílust igazol; a kategóriafa meglévő `ale` értékével pontosítottuk.
  A Chimay saját anyaga a Blue 9%-os változatát erős, sötétbarna
  trappista sörként, a szakmai stílusadat belga erős barna ale-ként
  azonosítja; az `ale` fajtát pótoltuk. A Delirium Tremens gyártói
  oldala 8,5%-os, halvány blond sört, a gyártó történeti adata erős
  ale-t igazol; az `ale, belga blond` fajtákat felvettük.
- Az Erdinger Weissbräu forrásneve `0,5 l x 11`, ára is többdarabos
  csomagot igazol. A teljes kiszerelést 5500 ml-re, a darabszámot
  11-re javítottuk. A két közvetlenül bizonyított, elemi értéket a
  sörlevél engedélyezett készletébe is felvettük.
- A Lindemans Framboise, St. Pierre Blond, Flensburger Pilsener és
  Weizen, Bavaria gluténmentes Pilsner, három Bernard lager, Free Damm,
  Radeberger Pilsner és Bitburger ötliteres Premium Pils rekordja már
  pontos volt.
- Módosított rekord: **14**.
- Módosított tulajdonságmező: **16**.
- Változatlanul hagyott rekord: **11** (`BTY-X17579500320021`,
  `BTY-X17586400320021`, `BTY-X17722700320021`,
  `BTY-X17722900320021`, `BTY-X17752600320021`,
  `BTY-X18222900320021`, `BTY-X18223000320021`,
  `BTY-X18223200320021`, `BTY-X18516900320021`,
  `BTY-X17577500320021`, `BTY-X12451100320021`).
- Új megengedett érték: **2** (`csomagdarabszám: 11`;
  `kiszerelés: 5500 ml`).
- Törölt megengedett érték: **0**.
- Az első alkalmazási futás az Erdinger csomagnál jelezte, hogy az
  igazolt `11` és `5500 ml` még nem szerepelt a sörlevél engedélyezett
  értékei között. Az érintett rekord automatikusan visszaállt; a két
  elemi értéket felvettük és naplóztuk, majd a teljes futást sikeresen
  megismételtük.
- A 16 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 14 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17586900320021` | fajta `sör, kellerbier` → `sör, lager, kellerbier` |
| `BTY-X17615700320021` | fajta `sör` → `sör, lager` |
| `BTY-X17629000320021` | márka `Estrella Galicia` → `Daura Damm`; fajta `sör` → `sör, lager` |
| `BTY-X17722800320021` | fajta `sör` → `sör, lager` |
| `BTY-X17840700320021` | szűretlen `false` → `true` |
| `BTY-X18089200320021` | kézműves `false` → `true` |
| `BTY-X18223300320021` | fajta `sör` → `sör, lager` |
| `BTY-X18957600320021` | fajta `sör` → `sör, ale` |
| `BTY-X6276600320021` | fajta `sör` → `sör, ale` |
| `BTY-X7176700320021` | fajta `sör` → `sör, ale, belga blond` |
| `BTY-X98284900320021` | kiszerelés `500 ml` → `5500 ml`; csomagdarabszám `1` → `11` |
| `BTY-X17840800320021` | fajta `sör, dunkel` → `sör, búzasör, dunkel` |
| `BTY-X11321200320021` | fajta `sör` → `sör, lager` |
| `BTY-X17578500320021` | fajta `sör` → `sör, pilsner` |

### Sör kézi felülvizsgálat, 512–536. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Corona Extra korábban ellenőrzött pontos változata világos lager.
  A Heineken 0.0 mindkét kiszerelését a gyártó alkoholmentes lagerként
  azonosítja, a Peroni Nastro Azzurro 0.0 pedig a normál Peroni
  alkoholmentes lagerváltozata. Mind a négy rekordnál pótoltuk a
  hiányzó `lager` fajtát.
- A Guinness saját termékoldala a Guinness 0.0-t stoutként és sötét
  rubinvörös, gyakorlatilag fekete megjelenésű italként írja le; a
  közvetlen doboz és az azonos termék korábban felülvizsgált rekordja
  alapján a fajtát `stout`, a színt `fekete` értékre javítottuk.
- A Gösser NaturZitrone 0,0%-os gyártói termékadata valódi citromlével
  készülő, természetesen fátyolos NaturRadlert igazol. Az alap citromos
  rekord színét világosra, szűretlen jelzőjét igazra javítottuk; az
  áfonya–citrom és mangó–citrom változatnál a már helyes világos szín
  mellett a szűretlenséget pótoltuk.
- A Soproni hat és a Borsodi öt ízesített alkoholmentes radlerének
  közvetlen dobozfelirata minden esetben egyezett a jelenlegi fajtával
  és ízlistával. A négy Dreher 24 ízesített keverék szintén pontos
  volt. A natúr Dreher 24 és Szalon alkoholmentes sörét nem
  pontosítottuk lagerre közvetlen stílusbizonyíték nélkül.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **10**.
- Változatlanul hagyott rekord: **17** (`BTY-X17181600320021`,
  `BTY-X18202400320021`, `BTY-X17181400320021`,
  `BTY-X17185800320021`, `BTY-X17274400320021`,
  `BTY-X17274500320021`, `BTY-X17274800320021`,
  `BTY-X18202200320021`, `BTY-X18202300320021`,
  `BTY-X18202500320021`, `BTY-X18202600320021`,
  `BTY-X17336600320021`, `BTY-X17336800320021`,
  `BTY-X17335600320021`, `BTY-X17335700320021`,
  `BTY-X17335900320021`, `BTY-X17499900320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 10 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az
  azonosító-paritást, az alkoholos sémákat, az engedélyezett értékeket és
  a kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 8 végleges
  írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18997400320021` | fajta `sör` → `sör, lager` |
| `BTY-X18314900320021` | fajta `sör` → `sör, stout`; szín `egyéb` → `fekete` |
| `BTY-X17362500320021` | fajta `sör` → `sör, lager` |
| `BTY-X17362900320021` | fajta `sör` → `sör, lager` |
| `BTY-X17336300320021` | fajta `sör` → `sör, lager` |
| `BTY-X17482600320021` | szín `egyéb` → `világos`; szűretlen `false` → `true` |
| `BTY-X17205000320021` | szűretlen `false` → `true` |
| `BTY-X17358500320021` | szűretlen `false` → `true` |

### Sör kézi felülvizsgálat, 537–561. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Clausthaler gyártói termékoldala az Original változatot
  alkoholmentes lagerként azonosítja. A Stella Artois 0.0 pontos
  termékadata ugyancsak alkoholmentes lagert igazol; mindkét rekordnál
  pótoltuk a hiányzó `lager` fajtát.
- A Szent András saját termékoldala a Majdnem Pilsnert alkoholmentes
  pilsnerként, alsóerjesztésű lagerként és kisüzemi sörként írja le. A
  fajta már pontos volt, a hiányzó kézműves jelzőt igazra javítottuk.
- Az Adelskronen világos dobozán `Premium Pils`, a Königsbrau dobozán
  `Lager Beer` olvasható; ezért a hiányzó `pilsner`, illetve `lager`
  fajtát pótoltuk.
- Az Adelskronen 5%-os barna sör közvetlen dobozfelirata
  `Schwarzbier`. A BJCP ezt önálló sötét német lagerként határozza meg,
  ezért a fajtát `sör, lager, schwarzbier`, a színt `fekete` értékre
  javítottuk. A közvetlenül bizonyított, elemi `schwarzbier` értéket a
  sörlevél engedélyezett fajtái közé is felvettük.
- Az O'Stout Extra Stout közvetlen doboza és a pontos stílus fekete
  stoutot igazol; a már helyes fajta mellett csak a színt javítottuk.
- Az Arany Ászok tradicionális és a Dreher Gold azonos termékeinek
  korábban ellenőrzött pontos változatai világos lagerek, a Beck's
  pontos változata pilsner. A hiányzó fajtákat ezekkel egyezően
  pótoltuk.
- A két BE(er) Cool keverék, az Erdinger alkoholmentes búzasör, a
  Bavaria 0.0 IPA, a két Karamalz malátaital, a három Dreher 24
  ízesített keverék, a Dresdner Felsenkeller, az Arany Korsó három
  változata, a Löwenbräu, az Adelskronen Hefe-Weissbier és a Holsten
  rekordja már pontos volt. A névben és képen pontos sörstílust nem
  közlő általános termékeket nem egészítettük ki feltételezett
  fajtával.
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **15** (`BTY-X17500100320021`,
  `BTY-X17500200320021`, `BTY-X17580000320021`,
  `BTY-X17585100320021`, `BTY-X17748900320021`,
  `BTY-X18086200320021`, `BTY-X18118500320021`,
  `BTY-X18686700320021`, `BTY-X17669200320021`, `1012311`,
  `1021728`, `1012312`, `1019808`, `1048033`, `1000966`).
- Új megengedett érték: **1** (`fajta: schwarzbier`).
- Törölt megengedett érték: **0**.
- A 11 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a
  kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 10 írás
  sikeres volt, visszaállításra nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17578800320021` | fajta `sör` → `sör, lager` |
| `BTY-X17715500320021` | fajta `sör` → `sör, lager` |
| `BTY-X17601200320021` | kézműves `false` → `true` |
| `1048038` | fajta `sör` → `sör, pilsner` |
| `1014066` | fajta `sör` → `sör, lager` |
| `1048039` | fajta `sör` → `sör, lager, schwarzbier`; szín `barna` → `fekete` |
| `4250235` | szín `barna` → `fekete` |
| `991939` | fajta `sör` → `sör, lager` |
| `991942` | fajta `sör` → `sör, lager` |
| `1019810` | fajta `sör` → `sör, pilsner` |

### Sör kézi felülvizsgálat, 562–586. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Staropramen gyártói oldala az 5%-os Premium változatot világos
  lagerként, a 4,4%-os Dark változatot sötét lagerként azonosítja. A
  Dark közvetlen dobozfelirata is szó szerint `dark lager`; mindkét
  rekordnál pótoltuk a hiányzó `lager` fajtát.
- A Stella Artois gyártói/márkatulajdonosi termékadata a pontos 5%-os
  változatot alsóerjesztésű szőke pilsnerként és nemzetközi lagerként
  írja le; ezért a fajtát `sör, lager, pilsner` értékre pontosítottuk.
- A Peroni Nastro Azzurro gyártói termékoldala az 5%-os, 0,33 literes
  palackot Premium Lagerként azonosítja. Mind a Penny-, mind a
  Prima-rekordnál pótoltuk a `lager` fajtát.
- A két Kőbányai azonos, 4,3%-os termékváltozatának pontos
  termékadata lagerbesorolást igazol; a két kiszerelésnél pótoltuk a
  hiányzó fajtát. A Gösser Premium pontos 5%-os magyar változatát a
  termékadatok lagerként azonosítják, ezért ennél is felvettük a
  hiányzó `lager` értéket.
- A Dreher Gold az előző tételben ellenőrzött, azonos 5%-os termék
  Prima-rekordja, ezért ugyanúgy világos lagerre pontosítottuk. A
  Heineken gyártói oldala az Original 5%-os változatát lagerként
  azonosítja; mindkét Prima-kiszerelésnél pótoltuk ezt a fajtát.
- A Miller Genuine Draft, a két Pilsner Urquell és a Kozel Premium
  Lager fajtája már pontos volt. Az ízesített Dreher 24 és Arany Korsó
  radlerek, valamint a két Friss malátaital ízei és fajtái egyeztek a
  teljes terméknévvel és a közvetlen dobozfelirattal. Az Adelskronen
  alkoholmentes sört nem pontosítottuk feltételezett stílussal.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **14** (`1017347`, `1004149`,
  `4603962`, `1048043`, `999346`, `999347`, `1012313`, `990850`,
  `1054660`, `1057856`, `1057694`, `1054659`,
  `83e5d6cbe83b1693c0079c63`, `0ca9bf7221fa2da2b4a9a0fc`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 11 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a
  kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 11 írás
  sikeres volt, visszaállításra nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1019799` | fajta `sör` → `sör, lager` |
| `1018804` | fajta `sör` → `sör, lager, pilsner` |
| `1019804` | fajta `sör` → `sör, lager` |
| `990856` | fajta `sör` → `sör, lager` |
| `991943` | fajta `sör` → `sör, lager` |
| `13e84857c86572015e1cefb8` | fajta `sör` → `sör, lager` |
| `3468f6a878582f972d660cd4` | fajta `sör` → `sör, lager` |
| `16f7c6c31d299df98512fa7c` | fajta `sör` → `sör, lager` |
| `cbb62faf6ca216c0ae3fe032` | fajta `sör` → `sör, lager` |
| `afb1109691315b7e427d4f5f` | fajta `sör` → `sör, lager` |
| `f71f566c267bec5793ae2b71` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 587–611. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Heineken gyártói oldala a 4%-os Silver változatot prémium
  lagerként azonosítja. A Soproni 1895 pontos 5%-os termékadata
  lagert, a Soproni 4,5%-os hatos csomagja pedig a gyártó jelenlegi
  Lager termékével azonos kiszerelést igazol; mindháromnál pótoltuk a
  hiányzó `lager` fajtát.
- Az Arany Ászok és a Dreher Gold az előző tételekben ellenőrzött
  pontos termékek újabb Prima-rekordjai; mindkettőt azonos módon
  lagerre pontosítottuk. A Dreher saját oldala a Hidegkomlóst a
  `Kraft Söreink` termékcsaládban közli, ezért a kézműves jelzőt igazra
  javítottuk, de ennél pontosabb fajtát a forrás nem bizonyított.
- A Tuborg Green márkatulajdonosi oldala a pontos 4,6%-os változatot
  alsóerjesztésű lagerként és pilsnerként azonosítja; a fajtát
  `sör, lager, pilsner` értékre javítottuk. A Corona gyártói oldala a
  4,5%-os, 355 ml-es Extra változatot pale lagerként közli, ezért a
  hiányzó `lager` fajtát pótoltuk.
- A Horizont Hop Session IPA az előzőleg ellenőrzött azonos termék
  Prima-rekordja, ezért a kézműves jelzőt igazra javítottuk. A Gentle
  Bastard azonos termékváltozatánál a hiányzó `IPA` fölérendelt
  stílust és a kézműves jelzőt is pótoltuk; a Hazy Queen már pontos
  volt.
- A Beck's az előzőleg ellenőrzött pontos 5%-os termékkel azonos
  pilsner. A Coors gyártói termékadata lagert igazol; mindkét rekord
  hiányzó fajtáját pótoltuk.
- A BJCP Belgian Blond Ale stílusleírása a Leffe Blondot kereskedelmi
  példaként nevezi meg, a gyártói oldal pedig a pontos 6,6%-os blond
  apátsági sört igazolja. A már helyes `belga blond` mellé ezért
  felvettük az `ale` fajtát.
- A Soproni Lager, APA és IPA, a Hofbräu Lager, a Pilsner Urquell és a
  Pécsi Prémium Pils rekordja már pontos volt. A Borsodi Bivaly,
  Világos és Mester, valamint a Steffl és Riesenbrau rekordját nem
  egészítettük ki feltételezett stílussal, mert a teljes név, a
  közvetlen kép és a gyártói adat csak általános világos sört
  bizonyított.
- Módosított rekord: **13**.
- Módosított tulajdonságmező: **14**.
- Változatlanul hagyott rekord: **12** (`de551d883538c4ecd4355d95`,
  `dea8ebbdd70dbb5168b50674`, `e2a739c1fd25c8ae0d0d7091`,
  `951aecc7e33119ccca045f21`, `5d062dfa3c829d53d7b7d120`,
  `311f26df1632a12a7cd5cf54`, `729d357b0ca4b07de13b8c00`,
  `6a5dcea72138c2ade216a9bd`, `e5955b8299002afec1c4fa05`,
  `35b69cd66f01eca48418ba6a`, `6b02be5a3d8c7a23a1d06053`,
  `8955f9d727a632adab0084f6`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 14 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal.
  Minden rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az
  alkoholos sémákat, az engedélyezett értékeket és a
  kategóriahash-eket vizsgáló teljes ellenőrzés; mind a 13 írás
  sikeres volt, visszaállításra nem volt szükség.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `86d64e89c4ea371ee93ddb0a` | fajta `sör` → `sör, lager` |
| `98e37fc09ee1ea46192f9e70` | fajta `sör` → `sör, lager` |
| `d1e530729ebf4ead9fb13e9a` | fajta `sör` → `sör, lager` |
| `1cc55c0f8cb2d0028cd6dd70` | fajta `sör` → `sör, lager` |
| `ebe581ab657891860ae6818d` | kézműves `false` → `true` |
| `6abbca9ef713e4003e6a1b24` | fajta `sör` → `sör, lager, pilsner` |
| `11c06efb88ff7f522b01564e` | fajta `sör` → `sör, lager` |
| `c2fe2ebfa721dceca85cb94d` | kézműves `false` → `true` |
| `8b1a7d3ee56c9678eb00e22e` | fajta `sör, West Coast IPA` → `sör, IPA, West Coast IPA`; kézműves `false` → `true` |
| `9ee81ee2784331f8cdc79c9c` | fajta `sör` → `sör, pilsner` |
| `01f65b805ef8d91354468631` | fajta `sör` → `sör, lager` |
| `98f650d9c392ea62dd00a79b` | fajta `sör` → `sör, lager` |
| `9c5568b6ab11c38a9db77f45` | fajta `sör, belga blond` → `sör, ale, belga blond` |

### Sör kézi felülvizsgálat, 612–636. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Staropramen Unfiltered gyártói leírása lager- és búzasörjelleget,
  valamint koriandert igazol; a Premium, Dark és Granát változatok
  lagerbesorolását is a gyártói termékadat alapján pontosítottuk. A Granát
  nevében szereplő szó nem gránátalma-ízesítés, hanem vörös lagerstílus,
  ezért az ízt `natúr`, a színt `vörös` értékre javítottuk.
- A 1664 Blanc és Hoegaarden White bizonyított witbier, citrusos-fűszeres
  jelleggel; a Hoegaarden szűretlen. A 1664 Rosé málnás-fűszeres vörös
  búzasör. A Dreher Bak képe és termékadata karamelles ízt, a Dreher saját
  Kraft termékcsaládja pedig kézműves besorolást igazol.
- Módosított rekord: **14**.
- Módosított tulajdonságmező: **22**.
- Változatlanul hagyott rekord: **11** (`21c04cd47294621fa0b10c00`,
  `4f05a1f42ff4dd2873183db5`, `575888a136522902aa6ce733`,
  `6e5fabd3673c35f9ba2d0f23`, `97d7a23241176c159d09c863`,
  `a1ba0873b26175f90d9b3261`, `c1b768be470178f07fe203c5`,
  `d00c0d88d78bfdfef967bd75`, `e3a822770af8234bb375021a`,
  `e7513d22bdb0e832cf0d3c43`, `ec2a128fb94998fc8c64db0e`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 22 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 14 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `84fab7168f8fe9dab352e8b1` | fajta `sör` → `sör, lager, búzasör`; íz `natúr` → `fűszeres` |
| `cf32b1afbc94b19b0c5385b9` | fajta `sör` → `sör, lager` |
| `fb5aedded5bf64022970b775` | fajta `sör` → `sör, lager, pilsner` |
| `d13a17e275e7cc4fa0244344` | fajta `sör` → `sör, lager` |
| `2cc9a1d75fef1df042835c83` | fajta `sör` → `sör, lager` |
| `18862ca85a6f54edfa129889` | fajta `sör` → `sör, lager` |
| `a56588df3b7add649108b77a` | fajta `sör` → `sör, lager` |
| `2e587d5d8c13eeabf41a69e9` | fajta `sör` → `sör, lager` |
| `c3589c6faecb2f0a77e0f0b5` | íz `natúr` → `karamell`; kézműves `false` → `true` |
| `6a46a947e00ea1a1f78fb4a5` | fajta `sör` → `sör, lager` |
| `9252aba656ee36bc95b3e7bd` | fajta `sör` → `sör, lager`; íz `gránátalma` → `natúr`; szín `barna` → `vörös` |
| `d59205d3062598603a835c67` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `c7d3f98598acaf194a5d67af` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres`; szűretlen `false` → `true` |
| `292a9cba7bce7e3d1f181f0f` | íz `málna` → `málna, fűszeres`; szín `világos` → `vörös` |

### Sör kézi felülvizsgálat, 637–661. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A 1664 Rosé másik kiszerelésénél ugyanaz a málnás-fűszeres vörös jelleg,
  a 1664 Blancnál ugyanaz a citrusos-fűszeres witbier besorolás bizonyítható.
  A Peroni 0.0 gyártói termékadata alkoholmentes lagerként azonosítja a
  terméket.
- A többi radler, alkoholmentes ízesített sörkeverék és malátaital fajtája,
  íze és alkoholtartalma már megfelelt a teljes rekordnak és a közvetlen
  csomagolási képnek.
- Módosított rekord: **3**.
- Módosított tulajdonságmező: **5**.
- Változatlanul hagyott rekord: **22** (`03da3507c0ca7ffdeaceb7e2`,
  `107922f3b26ccc5aab9cad5f`, `15cbccbfd4480db5475a8ba2`,
  `390bb9255db8f69ce11902b0`, `398de80ef7d949d8c6668e81`,
  `3e28d7c7463f2a8545c2f77f`, `4258da35c35f34c364d16fb2`,
  `470dd85a41cbc7bbc7f720ef`, `4e8b0a41230f991f2c913582`,
  `5d51b26703ff8491944dbd8f`, `6b4badb4cf58881bdf056343`,
  `6c1bbcdfe4bb9d83f1ecab83`, `6ea7ca2655dcdcefe690f990`,
  `817e77bc0a624cbe2bbc2c9e`, `89f89ea1382b91b6ba601f33`,
  `8a2fc13df69ad1bc28c051d7`, `98732791b29de32594cb6ec1`,
  `b2ce688034bc93294f2d89ca`, `c354151d791c4b19ff47dfae`,
  `c648e7393775fc8cf44ac0e3`, `e05e7f227e0e87f602b8e793`,
  `ea6c7148697fc5bd0d766d88`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Az 5 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a teljes validáció; mind a 3 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `31612fae288230974ed5c88b` | íz `málna` → `málna, fűszeres`; szín `világos` → `vörös` |
| `7a90df3db43ed9b76e1352cf` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `f25bd5e08baf79c4f15f70e8` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 662–686. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Stella Artois 0.0 gyártói adatából a lager és pilsner, a Heineken 0.0 és
  a Free Damm termékadatából a lager besorolás következik. A Pannonhalmi
  Blonde, Tripel, Dubbel és Quadrupel felsőerjesztésű ale; a közvetlen
  termékadatok alapján a citrusos-fűszeres, illetve karamelles ízeket is
  pontosítottuk.
- A Horizont, Fehér Nyúl és MONYO termékeknél pótoltuk a hiányzó `IPA`
  fölérendelt stílust és a közvetlenül bizonyított kézműves jelzőt. A
  Dead Rabbit pontos terméke double IPA és West Coast IPA is.
- Módosított rekord: **15**.
- Módosított tulajdonságmező: **28**.
- Változatlanul hagyott rekord: **10** (`22598cd603618cf48d96f527`,
  `2e2abac944ac172b45447a42`, `590ca717382931898390903a`,
  `5ad6f40a5b995535231321d6`, `64b43a11009f0e03139cb611`,
  `8484933dd0721a4570c9b649`, `9fe1fad92de106673703c895`,
  `abc0e869f6238391546bc15c`, `dde4a4f9c3f673825a671cde`,
  `f15bea483e59a689fdbb750e`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 28 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a teljes validáció; mind a 15 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `88d3e468869921461c511ac8` | fajta `sör` → `sör, lager, pilsner` |
| `3552c3d747c34b232041efad` | fajta `sör` → `sör, lager` |
| `69085f2c969079f388fb8181` | fajta `sör` → `sör, lager` |
| `e76ed79549c55385fdb8a7f5` | fajta `sör, belga blond` → `sör, ale, belga blond`; íz `natúr` → `citrus, fűszeres`; kézműves `false` → `true` |
| `b339f7189ce81e1564527e94` | fajta `sör, tripel` → `sör, ale, tripel`; íz `natúr` → `citrus, fűszeres` |
| `2ae3391d13f3c20e15899eb3` | fajta `sör, dubbel` → `sör, ale, dubbel`; íz `natúr` → `karamell`; kézműves `false` → `true` |
| `9f9900f3cb186d5363a50c76` | fajta `sör, quadrupel` → `sör, ale, quadrupel`; íz `natúr` → `karamell`; kézműves `false` → `true` |
| `8f6f67fce821eba28ba551d4` | fajta `sör, New England IPA` → `sör, IPA, New England IPA` |
| `86e1c2e2da4f90dac8c0e240` | fajta `sör, West Coast IPA` → `sör, IPA, West Coast IPA`; kézműves `false` → `true` |
| `e790b5c30e01b1f95f1ad8f1` | fajta `sör, Session IPA` → `sör, IPA, Session IPA`; kézműves `false` → `true` |
| `005f6fbdac28b55f31c2fe90` | kézműves `false` → `true` |
| `ccb5ef12f0538adc036dae2b` | fajta `sör, sour IPA` → `sör, IPA, sour IPA`; kézműves `false` → `true` |
| `461e253d564021255c6a68e4` | fajta `sör, New England IPA` → `sör, IPA, New England IPA`; kézműves `false` → `true` |
| `a9f993d2e3e238132aa5143b` | fajta `sör, double IPA` → `sör, IPA, double IPA, West Coast IPA`; kézműves `false` → `true` |
| `ff95b32d5573544d342b4baa` | fajta `sör, New England IPA` → `sör, IPA, New England IPA`; kézműves `false` → `true` |

### Sör kézi felülvizsgálat, 687–711. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A BrewDog Hazy Jane gyártói oldala New England IPA-ként és szűretlenként
  azonosítja a terméket; ezért pótoltuk az `IPA` fölérendelt stílust, a
  kézműves és a szűretlen jelzőt. A többi BrewDog-, First-, Aha!-,
  Mad Scientist- és MONYO-terméknél a teljes név, a forráskategória és a
  közvetlen csomagolási kép alapján javítottuk a bizonyított kézműves
  besorolást és a hiányzó stílushierarchiát.
- A BE(er) Cool Premium Lagernél nem vettük át automatikusan a forrás
  kézműves kategóriáját, mert sem a teljes terméknév, sem a kép nem
  bizonyította ezt. A Peroni, Arany Ászok, Dreher Gold, Kőbányai és
  Heineken már korábban ellenőrzött azonos termékváltozatainál a hiányzó
  lagerbesorolást pótoltuk.
- Módosított rekord: **20**.
- Módosított tulajdonságmező: **27**.
- Változatlanul hagyott rekord: **5** (`21ea6b240edf3b56abb214c4`,
  `4d470dda9b14466c976eda09`, `937241ba2a677dcd4a564ad8`,
  `cc0e97c04e106f00b0d561ba`, `e3e6f23fd2f2e37ce2ee9af0`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 27 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 20 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `458bc2eb717b2eaf83ec52b1` | kézműves `false` → `true` |
| `a0ce6d9598bad9e100dc02af` | kézműves `false` → `true` |
| `6101d8a6fedf301b461e3400` | fajta `sör, New England IPA` → `sör, IPA, New England IPA`; kézműves `false` → `true`; szűretlen `false` → `true` |
| `31b72d0f85d9f45b10aa46ac` | kézműves `false` → `true` |
| `dc44f37998d709e67481419c` | kézműves `false` → `true` |
| `dc8a4e63fb3173977edbc446` | kézműves `false` → `true` |
| `df2bb00f7605f17d34b095e3` | fajta `sör, búzasör` → `sör, búzasör, witbier`; kézműves `false` → `true` |
| `77549d501adeeeb32ad048f1` | fajta `sör, black IPA` → `sör, IPA, black IPA`; kézműves `false` → `true` |
| `9d9c36ef03422dc0fafc0173` | fajta `sör, ale` → `sör, ale, sour ale`; kézműves `false` → `true` |
| `0fc19ea928074cb2a30f2152` | fajta `sör, pale ale` → `sör, ale, pale ale`; kézműves `false` → `true` |
| `e2743def1fd7bc771f161ff8` | kézműves `false` → `true` |
| `966482f51a5903afee15ce74` | fajta `sör, double IPA` → `sör, IPA, double IPA`; kézműves `false` → `true` |
| `b10848b0a127478b3d5dcd6b` | fajta `sör` → `sör, lager` |
| `8b6cf0386c1a7d2709379d59` | fajta `sör` → `sör, lager` |
| `892fb2ea70d971a05306b3d1` | fajta `sör` → `sör, lager` |
| `a88f8292238f4d0f0cc4f0ad` | fajta `sör` → `sör, lager` |
| `b65197f4fba93621394374fc` | fajta `sör` → `sör, lager` |
| `9f9ef6b34f143b1e8de8ee3f` | fajta `sör` → `sör, lager` |
| `5744c86698c65c15630fa0d3` | fajta `sör` → `sör, lager` |
| `4d16433e3c41df3c0eeb1fd2` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 712–736. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Asahi gyártói sörismertetője a Super Dry terméket pilseni típusú
  sörként, a gyártó 2023-as versenyeredménye pedig International Style
  Pilsner lagerként azonosítja. Mindkét kiszerelésnél pótoltuk a `lager`
  és `pilsner` fajtát.
- Az Asahi Group gyártói közleménye a Peroni Stile Capri 4,2%-os terméket
  mediterrán lagerként írja le, olasz citromkivonattal és citrusjegyekkel;
  ezért a fajtát `sör, lager`, az ízt `citrom, citrus` értékre javítottuk.
  A Damm gyártói oldala az Estrella Dammot mediterrán lagerként, a
  Molson Coors termékadata a Coorst lagerként igazolja.
- Az Arany Ászok, Kőbányai, Gösser Premium, Soproni Klasszikus, Soproni
  hatos csomag és Heineken Silver a korábban ellenőrzött pontos
  termékváltozatok újabb rekordjai; a hiányzó lagerbesorolást pótoltuk.
  A Dreher Hidegkomlósnál a gyártó Kraft termékcsaládja alapján a kézműves
  jelzőt javítottuk.
- A Dreher Meggy, Soproni Lager, Soproni IPA és APA, Miller Genuine Draft,
  Borsodi IPA, Mester, Világos és Bivaly rekordok már pontosak voltak. A
  kizárólag általános világos sört bizonyító Borsodi-rekordokat nem
  egészítettük ki feltételezett stílussal.
- Módosított rekord: **14**.
- Módosított tulajdonságmező: **15**.
- Változatlanul hagyott rekord: **11** (`4c7cc88eda8847c54bad90f7`,
  `8e090fd2c9728b85bf52e1c3`, `773386a65674e591e90bd11a`,
  `53cf74709f0aed73960662e0`, `f929800adf44cff3057e37e1`,
  `ee975ece26be2e504e48032d`, `91528115670644bed964112c`,
  `a522b22d3b3329f00f0b20d2`, `2387ed18f3355a642b35a094`,
  `bed737fcc882f7267ae01a90`, `3773f02c4c331ef0dbde5e39`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 15 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 14 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `746243e9fee52f1c99d0e152` | fajta `sör` → `sör, lager` |
| `c3cd1af7eb00b3a48dfea3d7` | fajta `sör` → `sör, lager` |
| `d11a45864e6babad4dd4ca46` | fajta `sör` → `sör, lager` |
| `5c20060f453be427502f63e9` | kézműves `false` → `true` |
| `8bbc79c2e24f2d1d51d5dcae` | fajta `sör` → `sör, lager` |
| `baf82f406839dd11b23ea951` | fajta `sör` → `sör, lager` |
| `099523c91df1601605ba6bec` | fajta `sör` → `sör, lager` |
| `66c635705195cb57eb84e726` | fajta `sör` → `sör, lager, pilsner` |
| `45a88806dc23545decb4e71e` | fajta `sör` → `sör, lager, pilsner` |
| `e75f2dea36f4de7595658778` | fajta `sör` → `sör, lager`; íz `natúr` → `citrom, citrus` |
| `ef9e8e831994c32c9e699405` | fajta `sör` → `sör, lager` |
| `cf049d4281d2eae71dcd6edf` | fajta `sör` → `sör, lager` |
| `e029b1de617fa68f8e78e951` | fajta `sör` → `sör, lager` |
| `ff9a38ad893be29c5d2fd14e` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 737–761. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A 1664 Blanc két kiszerelése a már ellenőrzött, citrusos-fűszeres
  witbier; a Heineken hatos csomag címkéje `Premium Pilsener`, az Original
  dobozé `premium malt lager`. A Gösser Premium, Birra Moretti és Arany
  Ászok az előző kötegekben ellenőrzött lagertermékek újabb rekordjai.
- A DAB közvetlen dobozcímkéje `Dortmunder Export`, ezért a fajtát
  `sör, lager, dortmunder` értékre javítottuk. A Staropramen Unfiltered
  gyártói adata lager- és búzasörjelleget, valamint koriandert igazol.
- A Budweiser Budvar gyártói oldala az 5%-os Original változatot világos
  lagerként, a Corona pontos termékadata pale lagerként, a Tuborg gyártói
  oldala lagerként és pilsnerként, a Carlsberg magyar termékoldala az 5%-os
  változatot lagerként és dán pilsnerként azonosítja. A Beck's gyártói
  oldala a klasszikus terméket pilsnerként közli.
- A Hoegaarden White az előző kötegekben igazolt citrusos-fűszeres,
  szűretlen witbier. A Pilsner Urquell három kiszerelése, a Pécsi Prémium
  Pils és Lager, az Edelweiss Hefetrüb és a Löwenbräu Lager már pontos
  volt. A Szalon, Krušovice Originál és Arany Fácán általános világos
  söröket nem egészítettük ki feltételezett stílussal.
- Módosított rekord: **15**.
- Módosított tulajdonságmező: **20**.
- Változatlanul hagyott rekord: **10** (`5b3e7cf5baab30a57fb51ff0`,
  `8fe6d575618c3be214bccf73`, `23fe2bd829eef84eb1ec139e`,
  `6bf910bb1f724440ebd764c1`, `09ce6c31bc58dabeb4e0a3b2`,
  `1598c37cede00087e86cb198`, `950c7269436526701e305a78`,
  `3815560ecb3c6b378afdcb2e`, `032788997dc70e43c99b3893`,
  `039f7da3ea82ba1cba29b6d1`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 20 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 15 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `c55d3953af4abd224ed5d274` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `fe6f2e95a419e6a179aa0dae` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `b990ed46dba3921330d40eb1` | fajta `sör` → `sör, lager, pilsner` |
| `967417cac34cc37f742c4602` | fajta `sör` → `sör, lager` |
| `31dd68800337d1ae78b45ce2` | fajta `sör` → `sör, lager` |
| `c1bd96ebf3f8cd934c3ba834` | fajta `sör` → `sör, lager, dortmunder` |
| `7224c382866dcbed17f79e09` | fajta `sör` → `sör, lager, búzasör`; íz `natúr` → `fűszeres` |
| `ead89765bd148ed9415b2718` | fajta `sör` → `sör, lager` |
| `892f2cadc14f86b83a06e001` | fajta `sör` → `sör, lager` |
| `e1d1f346630957cca817947e` | fajta `sör` → `sör, lager` |
| `8eb90601bad98b1455ac581e` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres`; szűretlen `false` → `true` |
| `a8e8603819c921f860068c90` | fajta `sör` → `sör, lager` |
| `a9e34e6e09f3239d7540509f` | fajta `sör` → `sör, lager, pilsner` |
| `d16511eb79706c61b9c5c649` | fajta `sör` → `sör, lager, pilsner` |
| `6d0d5b5b4ae9e4786f49ffc0` | fajta `sör` → `sör, pilsner` |

### Sör kézi felülvizsgálat, 762–786. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Leffe Blonde az előző kötegekben igazolt belga blond ale. A Staropramen
  Premium két kiszerelése lager, a Stella Artois három kiszerelése lager és
  pilsner. A Tsingtao címkéjén `Premium Lager`, a Paulaner Münchner Hell
  teljes terméknevében és címkéjén lager, a Löwenbräu csomagolásán
  közvetlenül `Lager` olvasható.
- A Szent András Monarchista teljes neve és főzdei termékadata
  `imperial pilsner`, a Magyar Vándor pontos főzdei besorolása lager–ale
  hibrid; a kézműves jelzők közül a Monarchistáét is javítottuk. A Dreher
  Session IPA-nál pótoltuk az `IPA` fölérendelt stílust és a Dreher Kraft
  termékcsalád által igazolt kézműves jelzőt.
- A Coors, Beck's, 1664 Blanc, Estrella Damm 0.0, Peroni Nastro Azzurro és
  Heineken az előző kötegekben ellenőrzött pontos termékváltozatok újabb
  rekordjai; ezeknél az ott már bizonyított fajtákat és ízeket vittük át.
- A Steffl és a 4,2%-os BE(er) Cool általános világos söröknél nem
  feltételeztünk stílust. A Paulaner Weissbier, a másik BE(er) Cool Lager,
  Radeberger Pilsner, Guinness IPA és Dreher Citrus már pontos volt.
- Módosított rekord: **18**.
- Módosított tulajdonságmező: **21**.
- Változatlanul hagyott rekord: **7** (`f56786479038a886f3ccdebc`,
  `a33179a903dc0ccbd9e4daae`, `7089cd47da2715ef7174cf66`,
  `ed39728cf0a001c07fdedbd6`, `d405d114fe8d75c6e689f43f`,
  `fa1e5d8282c355bc8ff29c13`, `ae535afae918a846b8bcb11e`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 21 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 18 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `c8848a2c2435b3941ab536dc` | fajta `sör, belga blond` → `sör, ale, belga blond` |
| `62c5ac9f404553224a76390b` | fajta `sör` → `sör, lager` |
| `a924fb93ac8dcb2e81a27c13` | fajta `sör` → `sör, lager, pilsner` |
| `20e4af776e5eac7e5ab491dc` | fajta `sör` → `sör, lager` |
| `1f01fe7109d9eaa9c4a6d99e` | fajta `sör` → `sör, lager, pilsner` |
| `72561b7e3b178d536d967015` | fajta `sör, pilsner` → `sör, pilsner, imperial pilsner`; kézműves `false` → `true` |
| `b91a21e81d6bf82e52cf9ec9` | fajta `sör` → `sör, lager, ale` |
| `989e0c767c4155437bd6244a` | fajta `sör` → `sör, lager` |
| `baaf0828cd4f1508af949fc2` | fajta `sör, helles` → `sör, lager, helles` |
| `b8ac504361b7accdc6261e14` | fajta `sör` → `sör, lager` |
| `2ef36f07a40d77464f03a601` | fajta `sör` → `sör, lager` |
| `d74ee73dd03acce51f09cad9` | fajta `sör` → `sör, pilsner` |
| `bb010aacb78c6a166074d1a3` | fajta `sör` → `sör, lager, pilsner` |
| `79e54337ddf4e0756102a5c1` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `5cee1b15211520f380cfed5c` | fajta `sör` → `sör, lager` |
| `af65f9bf75be2200792ac548` | fajta `sör, Session IPA` → `sör, IPA, Session IPA`; kézműves `false` → `true` |
| `0689393fbe74e13b91faf62d` | fajta `sör` → `sör, lager` |
| `14c2cd0d987eba573204f562` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 787–811. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Carlsberg csomagolása `Danish Pilsner`, a gyártói termékoldal pedig
  lagerként is azonosítja a pontos 5%-os változatot. A Staropramen Premium
  és Dark az előző kötegekben ellenőrzött lagertermékek újabb rekordjai.
- A Leffe Brune belga, felső erjesztésű barna apátsági ale. A Soproni Démon
  `karamellmaláta` felirata malátatípust, nem hozzáadott karamellízesítést
  jelent, ezért az ízt `natúr` értékre javítottuk.
- A Pannonhalmi Főapátság Sörfőzde Meggy Ale és a Horizont Morning Joe
  kisüzemi, kézműves főzdék termékei. A Morning Joe közvetlen dobozcímkéje
  `coffee & chocolate stout`, ezért a hiányzó stout stílust is pótoltuk.
- A Riesenbrau általános világos sörnél nem feltételeztünk lagerstílust.
  A Dreher Bak, Guinness, Kozel Černý, radlerek, lambicok, ízesített ale-ek,
  búzasörök és a Soproni Citrus meglévő besorolása a teljes rekorddal és a
  képpel együtt már pontos volt.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **8**.
- Változatlanul hagyott rekord: **18** (`6497597f4a362ced34dfe8af`,
  `c6e8832f319acc5b17281230`, `70ce11d87f5ee58501de876e`,
  `6d45abc2556ac641499ca2d7`, `fdc221bef7d72d8cb45021d4`,
  `4689c57a4c9c2a0678aff318`, `c9f353d6a42ba408e9709b31`,
  `015d20c4eea8f344b7e7e235`, `77d632e9bb93c5751a1179f3`,
  `6bac1ed645efc7c92a9245ea`, `8878886a90d58b4c5585162c`,
  `e2f4de1cfcd23adc8f5ee98b`, `9be26a591f3e29e25e81e974`,
  `34fd626cbc85f65b15eec4b2`, `2f1511ea7d3d83303964383a`,
  `a4a7f7509ab5b2335e022504`, `08a44c8de3559ee0cf569c7e`,
  `85c577646b6ea06d5819e91f`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 8 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 7 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1269906a2a2169b744bf1160` | fajta `sör` → `sör, lager, pilsner` |
| `ea8b0f7ba24a194ee4c2c40a` | fajta `sör` → `sör, lager` |
| `efab4337dc834fdf33ce4354` | íz `karamell` → `natúr` |
| `73e19e910a577eec7068f832` | fajta `sör` → `sör, ale` |
| `9b01c951c368a05bee4404c6` | fajta `sör` → `sör, lager` |
| `94a28482e9940af7f2b7cbf4` | kézműves `false` → `true` |
| `f44bf27c5454e02cfadba230` | fajta `sör` → `sör, stout`; kézműves `false` → `true` |

### Sör kézi felülvizsgálat, 812–836. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Heineken 0.0 két kiszerelését a közvetlen `pure malt lager` felirat és a
  gyártói termékadat is alkoholmentes lagerként igazolja. A Staropramen 0.0
  dobozán `Premium Lager`, a DAB Zero dobozán `Dortmunder` és
  `non-alcoholic lager` olvasható.
- A Peroni Nastro Azzurro 0.0 a gyártó szerint az eredeti Peroni azonos
  lager-alapreceptjéből készül, az alkohol utólagos eltávolításával. A Stella
  Artois 0.0 az előző kötegben ellenőrzött lager/pilsner újabb kiszerelése, a
  Corona Cero pedig a gyártó klasszikus mexikói lagerének alkoholmentes
  változata.
- A Dreher, Soproni és Gösser ízesített söritalok radlerbesorolása, összetett
  ízei és 0%-os alkoholadatai pontosak voltak. A Friss két termékét a név és
  a doboz egyaránt alkoholmentes malátaitalként igazolja.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **7**.
- Változatlanul hagyott rekord: **18** (`1ff590f5ffb641f7e5084f5c`,
  `a51fcde4249c0f2564c25818`, `dd11b3d7bf0e29fff31b4b8b`,
  `a04096cdeb0f72748244ffc4`, `b2a150ceae2644344f5af34a`,
  `9f03841d625de8106e651734`, `2765f69d6cc21e6fd7eabaf1`,
  `5a9d9e4e60b48b1e01ffffad`, `38d43c38acb7d6850b80fc5b`,
  `02421ac7580b0f892315665e`, `44d3edc8543c98242e03921d`,
  `25aaea0b9cdaa84e99266e2a`, `3258894b9df044556713e967`,
  `31f27c97d1b45ab1b25b1d09`, `93142e971a5ee2da2b34d0f5`,
  `c46191771542fa34bbef9ca4`, `8f5972ecfad56429615a8b95`,
  `c06ef381184fa026ef380c2a`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 7 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 7 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `6f05ff1ac6e4347f970958df` | fajta `sör` → `sör, lager` |
| `830118604ce994eaad81d7b7` | fajta `sör` → `sör, lager` |
| `1cdbac17af99c1c583a4b92b` | fajta `sör` → `sör, lager, pilsner` |
| `72162f5381fa77fa1f4d55d9` | fajta `sör` → `sör, lager` |
| `367458cc32163e9452940a22` | fajta `sör` → `sör, lager` |
| `b04838aadfddcf0d79e4eefa` | fajta `sör` → `sör, lager, dortmunder` |
| `b7e0dae26997f012ccc80324` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 837–861. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Guinness 0.0 dobozcímkéje `alcohol free stout`, a teljes terméknév
  pedig fekete színt közöl; ezért a stout típust pótoltuk, a téves barna
  színt feketére javítottuk. A Stella Artois 0.0 és a Peroni Nastro Azzurro
  0.0 az előző kötegben ellenőrzött lager-, illetve lager/pilsner termékek
  újabb kiszerelései.
- A Mad Scientist Jam32 pontos neve és képe Session IPA-t igazol. Az `IPA`
  fölérendelt stílust és a főzde alapján bizonyított kézműves jelzőt
  pótoltuk; a szűretlenség már helyes volt.
- A Dreher Gold két kiszerelése, a Heineken és a Gösser Premium korábban
  ellenőrzött lagertermékek újabb rekordjai. A Pilsner Urquell és a Soproni
  Lager már pontos volt; a Rastinger és a Borsodi általános világos sörnél
  nem feltételeztünk további stílust.
- Az alkoholmentes Friss, Gösser, Soproni, Peroni és Dreher ízesített
  tételek fajtája, íze, alkoholtartalma és csomagadata pontos volt. A két
  Gösser Spritz, a Desperados és a két Garage terméknél sem találtunk
  bizonyítható mezőhibát.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **10**.
- Változatlanul hagyott rekord: **17** (`fb7817582ea8a1b3e7eb9c8e`,
  `c2368c0478f161d88c3d528a`, `94ae6c6ee2f84615a07b568c`,
  `bdc78ef13adf20b3e9739b3a`, `9ef4bb3e2d0447cd24b12cc8`,
  `85a6d0ec9d1376256d217a08`, `3f4c943a8a998e9cf6bfdd47`,
  `13293249d335b2d77ca72965`, `523e0c3cfd6fd53f9e5acc9a`,
  `121262732`, `121224824`, `121231695`, `121231746`, `121225063`,
  `121248295`, `121227850`, `121226033`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 10 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 8 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `390286a1536d636b862d5dea` | fajta `sör` → `sör, stout`; szín `barna` → `fekete` |
| `02e99bb70fa990b7dd083c17` | fajta `sör` → `sör, lager, pilsner` |
| `06cc726fc1306628b642d23c` | fajta `sör` → `sör, lager` |
| `d058d63ce5bb1ac065c788f9` | fajta `sör, Session IPA` → `sör, IPA, Session IPA`; kézműves `false` → `true` |
| `121227723` | fajta `sör` → `sör, lager` |
| `121227873` | fajta `sör` → `sör, lager` |
| `121225190` | fajta `sör` → `sör, lager` |
| `121225201` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 862–886. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Budweiser Budvar közvetlen dobozcímkéje `Czech Lager`. A Tuborg,
  Staropramen, Heineken, Kőbányai, Soproni, Peroni és Carlsberg az előző
  kötegekben már ellenőrzött lager-, illetve pilsnertermékek más
  kiszerelései; a hiányzó stílusértékeket ezeknél pótoltuk.
- A 1664 Blanc az előző kötegekben igazolt citrusos-fűszeres witbier. A
  Tesco-rekord általános búzasör- és natúr besorolását ennek megfelelően
  pontosítottuk.
- A Soproni Démon `karamellmaláta` felirata itt is malátatípust, nem
  hozzáadott karamellízesítést jelent, ezért az ízt `natúr` értékre
  javítottuk.
- A Löwenbräu Lager, Soproni Meggy Ale és IPA, Pécsi Radler, Miller
  Genuine Draft, valamint az alkoholmentes Dreher, Gösser és Soproni
  rekordok már pontosak voltak. A Steffl általános világos sörnél nem
  feltételeztünk további stílust.
- Módosított rekord: **15**.
- Módosított tulajdonságmező: **16**.
- Változatlanul hagyott rekord: **10** (`121224801`, `121226004`,
  `121225011`, `121224847`, `121234236`, `121227556`, `121225316`,
  `121224916`, `121226062`, `121224980`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 16 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 15 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121232526` | fajta `sör` → `sör, lager` |
| `121227585` | fajta `sör` → `sör, lager` |
| `121232463` | fajta `sör` → `sör, lager, pilsner` |
| `121226091` | fajta `sör` → `sör, lager` |
| `121225149` | fajta `sör` → `sör, lager` |
| `121227896` | fajta `sör` → `sör, lager` |
| `121227885` | fajta `sör` → `sör, lager` |
| `121225253` | fajta `sör` → `sör, lager` |
| `121225161` | fajta `sör` → `sör, lager` |
| `121231435` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `121227809` | fajta `sör` → `sör, lager` |
| `121227660` | fajta `sör` → `sör, lager` |
| `121232492` | fajta `sör` → `sör, lager, pilsner` |
| `121225299` | íz `karamell` → `natúr` |
| `121227545` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 887–911. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Gösser Premium, Heineken Original és Arany Ászok az előző kötegekben
  már ellenőrzött lagertermékek további kiszerelései. A két Heineken 0.0
  ugyanennek az igazolt alkoholmentes lagernek a 330 és 500 ml-es változata.
- A Stella Artois az előző kötegben ellenőrzött lager/pilsner, a Staropramen
  Dark pedig a korábban igazolt lager sötét változata; a hiányzó
  stílusértékeket pótoltuk.
- A Soproni, Dreher, Gösser, Pécsi és Rastinger ízesített söritalok
  radlerbesorolása, ízei és alkoholadatai pontosak voltak. A Dreher Bak és a
  Pécsi Prémium Lager stílusa már helyesen szerepelt. A Rastinger és Arany
  Fácán általános világos söröknél nem feltételeztünk nem bizonyított
  részletesebb stílust.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **8**.
- Változatlanul hagyott rekord: **17** (`121224997`, `121225005`,
  `121227510`, `121227959`, `121224882`, `121248289`, `121224853`,
  `121234213`, `121224974`, `121258202`, `121234265`, `121249432`,
  `121225028`, `121224865`, `121261365`, `121224818`, `121227527`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 8 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 8 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121225155` | fajta `sör` → `sör, lager` |
| `121224922` | fajta `sör` → `sör, lager` |
| `121226027` | fajta `sör` → `sör, lager, pilsner` |
| `121224905` | fajta `sör` → `sör, lager` |
| `121274292` | fajta `sör` → `sör, lager` |
| `121226125` | fajta `sör` → `sör, lager` |
| `121227769` | fajta `sör` → `sör, lager` |
| `120998491` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 912–936. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Dreher Hidegkomlós közvetlen dobozcímkéje a Kraft termékcsaládot
  igazolja, ezért a korábban ellenőrzött azonos változattal egyezően a
  kézműves jelzőt igazra állítottuk.
- A Heineken, Coors és Corona korábban igazolt lagerek más kiszerelései. A
  Stella Artois 0.0 az ellenőrzött lager/pilsner alkoholmentes változata.
- A Staropramen Granát gyártói termékadata vörös lagert igazol; a félbarna
  bolti megnevezésből származó `barna` színt ezért `vörös` értékre
  javítottuk. A 1664 Blanc az előző kötegekben igazolt citrusos-fűszeres
  witbier.
- A Rastinger 7 közvetlen dobozán `Lager Style`, a Soproni Klasszikusén
  `Lager` olvasható. A Peroni Stile Capri korábban igazolt citromos-citrusos
  mediterrán lager; ezek hiányzó értékeit pótoltuk.
- A Pilsner Urquell `sör, pilsner` besorolását a húsz azonos
  testvérrekorddal egyezően változatlanul hagytuk. A Kozel Premium Lager,
  Miller Genuine Draft, Mort Subite Kriek, Soproni APA, Edelweiss Hefetrüb
  és az ízesített alkoholmentes radlerek már pontosak voltak. A Krušovice,
  Borsodi és általános Rastinger világos söröknél nem feltételeztünk
  további stílust.
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **13**.
- Változatlanul hagyott rekord: **15** (`121227867`, `121227994`,
  `121249979`, `121226045`, `121225374`, `121225339`, `121224899`,
  `121226396`, `121227579`, `206700788`, `121264321`, `121249484`,
  `121226119`, `121225282`, `121225132`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 13 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 10 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121227988` | kézműves `false` → `true` |
| `120998433` | fajta `sör` → `sör, lager` |
| `121264269` | fajta `sör` → `sör, lager` |
| `121226085` | fajta `sör` → `sör, lager` |
| `121225938` | fajta `sör` → `sör, lager, pilsner` |
| `121226102` | fajta `sör` → `sör, lager`; szín `barna` → `vörös` |
| `121231510` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `121249357` | fajta `sör` → `sör, lager` |
| `121257566` | fajta `sör` → `sör, lager` |
| `121227781` | fajta `sör` → `sör, lager`; íz `citrom` → `citrom, citrus` |

### Sör kézi felülvizsgálat, 937–961. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Soproni Klasszikus, Dreher Gold, Birra Moretti, Staropramen Premium és
  Dark, Arany Ászok, Gösser Premium és Heineken Silver korábban igazolt
  lagerek más kiszerelései. A Stella Artois az ellenőrzött lager/pilsner
  termék újabb rekordja.
- A Heineken 6 × 250 ml-es csomag közvetlen változata `Premium Pilsener`,
  a Beck's gyártói stílusa pilsner. A két Asahi Super Dry az előző
  kötegekben igazolt lager/pilsner.
- A Staropramen Unfiltered gyártói termékadata lager- és búzasörjelleget,
  valamint koriandert igazol; ezért a hiányzó `lager`, `búzasör` és
  `fűszeres` értékeket pótoltuk.
- A Borsodi Tropical Ale neve és címkéje itt sem hozzáadott gyümölcsöt,
  hanem komlós aromajelleget közöl; a téves `trópusi gyümölcs` ízt
  `natúr` értékre javítottuk.
- A Pilsner Urquell két rekordja, Krušovice Černé, Pécsi Prémium Búza,
  Tiltott Csíki bock és Edelweiss Hefetrüb már pontos volt. A két Bad Dogs
  terméknél a teljes rekord, a közvetlen csomagolás és a Tesco-adatlap nem
  igazolta a kézműves jelzőt; egy nem elsődleges adatbázis `contract
  brewery` megjelölését nem tekintettük elégnek a módosításhoz.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **17**.
- Változatlanul hagyott rekord: **9** (`121228048`, `121225305`,
  `121234328`, `120931207`, `202649098`, `121249565`, `203223525`,
  `121249553`, `121228031`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 17 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 16 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `202645564` | fajta `sör` → `sör, lager` |
| `121227913` | fajta `sör` → `sör, lager` |
| `121225126` | fajta `sör` → `sör, lager` |
| `121225086` | fajta `sör` → `sör, pilsner` |
| `121226160` | fajta `sör` → `sör, lager` |
| `121228077` | fajta `sör` → `sör, lager` |
| `210302909` | fajta `sör` → `sör, lager` |
| `121226079` | fajta `sör` → `sör, lager, búzasör`; íz `natúr` → `fűszeres` |
| `121227936` | fajta `sör` → `sör, lager, pilsner` |
| `121227815` | fajta `sör` → `sör, lager, pilsner` |
| `121226338` | fajta `sör` → `sör, pilsner` |
| `121225265` | fajta `sör` → `sör, lager` |
| `202780791` | fajta `sör` → `sör, lager, pilsner` |
| `121225247` | fajta `sör` → `sör, lager` |
| `120998525` | fajta `sör` → `sör, lager` |
| `121225875` | íz `trópusi gyümölcs` → `natúr` |

### Sör kézi felülvizsgálat, 962–986. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Hoegaarden White az előző kötegekben igazolt citrusos-fűszeres,
  szűretlen witbier; a hiányzó három mezőértéket pótoltuk.
- A Staropramen Premium, Kőbányai és Coors korábban igazolt lagerek. A
  Staropramen Unfiltered újabb rekordjánál ugyanaz a lager–búzasör jelleg
  és korianderből származó fűszeresség bizonyítható. A Beck's és az Amstel
  pontos változata pilsner.
- A Guinness 0.0 közvetlen dobozcímkéje `Draught Stout`, a terméknév
  fekete színt közöl; ezért a stout típust pótoltuk, a téves barna színt
  feketére javítottuk. A Stella Artois az ellenőrzött lager/pilsner újabb
  kiszerelése.
- A 1664 Rosé két kiszerelése az előző kötegekben igazolt
  málnás-fűszeres vörös búzasör. A közvetlen Tesco-névben bizonyított
  `bodza` és `málna` ízek megőrzése mellett pótoltuk a `fűszeres` értéket,
  a színt pedig vörösre javítottuk.
- A Pécsi Meggy, Bad Dogs Mopsz Meggy, Zipfer Pils, Friss malátaitalok,
  Dreher Hydrate radlerek és Estrella Galicia már pontosak voltak. A
  Borsodi Mester, Wundertal és Rákóczi Extra általános világos söröknél
  nem feltételeztünk további stílust.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **18**.
- Változatlanul hagyott rekord: **13** (`121226056`, `121234207`,
  `121249576`, `121234599`, `121289165`, `121289171`, `121300596`,
  `121300613`, `121300642`, `121300688`, `121302778`, `121302784`,
  `121305579`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 18 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 12 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121226269` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres`; szűretlen `false` → `true` |
| `203108198` | fajta `sör` → `sör, lager` |
| `203215971` | fajta `sör` → `sör, lager` |
| `120517883` | fajta `sör` → `sör, lager, búzasör`; íz `natúr` → `fűszeres` |
| `207970166` | fajta `sör` → `sör, pilsner` |
| `121226350` | fajta `sör` → `sör, lager` |
| `121264315` | fajta `sör` → `sör, lager` |
| `121300607` | fajta `sör` → `sör, stout`; szín `barna` → `fekete` |
| `121300636` | fajta `sör` → `sör, lager, pilsner` |
| `121305683` | fajta `sör` → `sör, pilsner` |
| `121307082` | íz `bodza, málna` → `bodza, málna, fűszeres`; szín `világos` → `vörös` |
| `121307099` | íz `bodza, málna` → `bodza, málna, fűszeres`; szín `világos` → `vörös` |

### Sör kézi felülvizsgálat, 987–1011. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Corona Cero, Staropramen 0.0, Budweiser Budvar, Tuborg, Carlsberg,
  Peroni Nastro Azzurro, Stella Artois és alkoholmentes Peroni korábban
  igazolt lager-, illetve ahol indokolt, pilsnertípusának hiányzó értékeit
  pótoltuk.
- A Mythos 5%-os sörnél a közvetlen címke önmagában nem nevezte meg a
  típust, ezért a gyártó Olympic Brewery hivatalos termékoldalával is
  ellenőriztük; az oldal egyértelműen lagerként azonosítja.
- A 1664 Blanc négyes csomagja a korábban igazolt citrusos-fűszeres
  witbier újabb kiszerelése. A Dreher Session IPA rekordján a konkrét
  `Session IPA` mellől hiányzó általános `IPA` típust pótoltuk.
- A Bitburger Pils, Gösser Natur Zitrone, Borsodi, belga sörcsomag,
  1664 Lager, Peroni radlerek, Dreher és Soproni radlerek, Soproni Citrus
  és a bio, gluténmentes Pécsi Prémium Lager már pontosak voltak. A vegyes
  belga csomagnál nem állítottunk be egyetlen közös sörstílust vagy
  kézműves jelzőt, mert az öt különböző termékből álló válogatásra ezek
  nem lennének egységesen igazak.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **12**.
- Változatlanul hagyott rekord: **14** (`121308415`, `121308576`,
  `121314689`, `121339222`, `121343556`, `121355145`, `121355191`,
  `121355202`, `121355219`, `121355254`, `121355295`, `121355300`,
  `121355317`, `121234144`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 12 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal. Minden
  rekord után lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos
  sémákat, az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; mind a 11 írás sikeres volt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121314453` | fajta `sör` → `sör, lager` |
| `121328385` | fajta `sör` → `sör, lager` |
| `121339441` | fajta `sör` → `sör, lager` |
| `121343562` | fajta `sör` → `sör, lager` |
| `121343579` | fajta `sör` → `sör, lager, pilsner` |
| `121354641` | fajta `sör` → `sör, lager, pilsner` |
| `121354658` | fajta `sör, búzasör` → `sör, búzasör, witbier`; íz `natúr` → `citrus, fűszeres` |
| `121355133` | fajta `sör` → `sör, lager` |
| `121355156` | fajta `sör, Session IPA` → `sör, IPA, Session IPA` |
| `121355755` | fajta `sör` → `sör, lager, pilsner` |
| `121359722` | fajta `sör` → `sör, lager` |

### Sör kézi felülvizsgálat, 1012–1013. tétel

- A sörlevél utolsó két teljes rekordját és forrássorát egyenként, mindkét
  helyi termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Pécsi Prémium Lager rekordja pontos volt: a név és a címke is igazolja
  a lager típust és a gluténmentességet.
- A Daura Damm 5,4%-os termékénél a Damm hivatalos termékoldala igazolja a
  lager típust, ezért a hiányzó `lager` értéket pótoltuk.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **1** (`121251117`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Az egy mezőt írás előtt összevetettük a teljes jelenlegi rekorddal, majd
  lefutott a 47 030 rekordot, az azonosító-paritást, az alkoholos sémákat,
  az engedélyezett értékeket és a kategóriahash-eket vizsgáló teljes
  ellenőrzés; az írás sikeres volt.
- Ezzel a `Sör, radler és malátaital` levél mind az **1 013** jelenlegi
  termékének kézi felülvizsgálata elkészült.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121249115` | fajta `sör` → `sör, lager` |

### Cider kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Ravini alma-, szeder- és spritzváltozata, a Somersby alma-, áfonya-,
  bodza–lime-, körte-, málna–lime-, eper–lime- és meggyváltozatai, valamint
  a Woodgate és Strongbow almás ciderek alkoholstátusza, csomagolása,
  márkája, kiszerelése, alkoholtartalma és íze egyezett a bizonyítékokkal.
- A 24 × 330 ml-es Somersby teljes kiszerelése `7920 ml`, egységnyi
  kiszerelése `330 ml`, mindkettő helyes. A cider meglévő sémájában nincs
  csomagdarabszám, ezért új tulajdonságot nem hoztunk létre.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **25** (`1059047`, `1059048`, `1059049`,
  `539156`, `833223`, `679940:4217330`, `679937:4217327`,
  `679943:4217333`, `795191:4332581`, `789410:4326800`,
  `679967:4217357`, `680114:4217504`, `679946:4217336`, `10104531`,
  `10106434`, `BTY-X17471800320021`, `BTY-X17470500320021`,
  `BTY-X17470700320021`, `BTY-X17471400320021`,
  `BTY-X17471900320021`, `BTY-X18076200320021`,
  `BTY-X18076400320021`, `BTY-X18716900320021`,
  `BTY-X18716900320022`, `BTY-X18717600320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Adatírás nem történt. Lefutott a 47 030 rekordot, az azonosító-paritást,
  az alkoholos sémákat, az engedélyezett értékeket és a kategóriahash-eket
  vizsgáló teljes ellenőrzés; eltérés nem maradt.

### Cider kézi felülvizsgálat, 26–50. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Somersby meggy-, narancs-, görögdinnye-, málna–lime-, eper–lime-,
  körte-, alma-, áfonya- és bodza–lime-változatainak alkoholstátusza,
  csomagolása, márkája, kiszerelése, alkoholtartalma és íze minden áruházi
  rekordban egyezett a névvel, a forrással és a képpel.
- A 24 × 500 ml-es meggyes csomag teljes kiszerelése `12000 ml`,
  egységnyi kiszerelése `500 ml`; ezek helyesek.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **25** (`BTY-X18717600320022`,
  `BTY-X18948000320021`, `BTY-X17470800320021`,
  `BTY-X17472100320021`, `BTY-X17471100320021`, `4601662`, `1052125`,
  `999922`, `999923`, `999924`, `c9dd304b2ecc68122bba3048`,
  `773eb8c226d13e495e5ff7c4`, `c59ae62ee5d9287e22104da4`,
  `a2fa5c78b79db81072fa237b`, `4cce93fc315c103331c1ffcb`,
  `fbc594be69b13b444549e56c`, `6399194b39ea54e68ec10ddb`,
  `5f65757a56caf3ed58bf7a87`, `17a84c5946d5c6dce6aa4233`,
  `1f2e5fb5a0368bde90552d85`, `30d5e95d8fbea3054d6eb85a`,
  `fd8baee06b0c22452dc7c9eb`, `283d9e4038fba54f03e73489`,
  `1e3007bd0ddbda845b9787f5`, `70a0c83b6ff4a41c807e30d4`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Adatírás nem történt. A teljes validáció 47 030 rekordot, azonosító-
  paritást, alkoholos sémákat, engedélyezett értékeket és kategóriahash-eket
  ellenőrzött; eltérés nem maradt.

### Cider kézi felülvizsgálat, 51–73. tétel

- A ciderlevél utolsó 23 teljes rekordját és forrássorát egyenként, mind a
  23 helyi termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Strongbow Red Berries és Gold Apple, a Somersby meggy-, narancs-,
  eper–lime-, bodza–lime-, alma-, áfonya-, málna–lime- és körteváltozatai,
  továbbá a Kopparberg eper–lime, Mixed Fruit és Passionfruit ciderek
  minden meglévő tulajdonsága egyezett a bizonyítékokkal.
- A Kopparberg Mixed Fruit `fekete ribizli, málna`, a Passionfruit
  `maracuja`, a Strongbow Red Berries `erdei gyümölcs` ízértéke helyes.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **23** (`a81338addf6d9266d4c5511d`,
  `233e6421d42b39ecead3e011`, `ff5e50fcb167629f5dc8f7e4`,
  `cde3723205cff701d1d04410`, `27d4b245a65df2a0714ee6a2`,
  `0c45473d6827d85e176236ca`, `121231648`, `121231355`, `121264246`,
  `121231660`, `121231412`, `121232388`, `121304661`, `121304678`,
  `121304684`, `121307001`, `121320860`, `121320877`, `121349832`,
  `121349930`, `121354664`, `121354704`, `121358769`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Adatírás nem történt. A teljes validáció 47 030 rekordot, azonosító-
  paritást, alkoholos sémákat, engedélyezett értékeket és kategóriahash-eket
  ellenőrzött; eltérés nem maradt.
- Ezzel a `Cider` levél mind a **73** jelenlegi termékének kézi
  felülvizsgálata elkészült.

### Brandy kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az ARARAT, Pâpidoux Calvados, Hennessy, METAXA, Cortel, St. Rémy, Győri
  és Martell termékek márkája, kiszerelése és alkoholtartalma minden
  rekordban egyezett a névvel, forrással és csomagolással.
- A Pâpidoux Calvados bizonyított almaíze helyes; a cognacok, hagyományos
  brandyk és METAXA-változatok hozzáadott ízesítés nélküli `natúr`
  értéke szintén helyes.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **25** (`772035:4309425`,
  `683867:4221257`, `712670:4250060`, `712637:4250027`,
  `946265:4483655`, `954830:4492220`, `152705:3689945`,
  `979547:4516937`, `10080982`, `BTY-X18363700320021`,
  `BTY-X17692100320021`, `BTY-X17638400320021`,
  `BTY-X17692800320021`, `BTY-X7381300320021`,
  `BTY-X17721300320021`, `BTY-X10396300320021`,
  `BTY-X11144600320021`, `BTY-X11885400320021`,
  `BTY-X17592100320021`, `BTY-X17592200320021`,
  `BTY-X17592500320021`, `BTY-X17602500320021`,
  `BTY-X17638500320021`, `BTY-X17691900320021`,
  `BTY-X17692200320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Adatírás nem történt. A teljes validáció 47 030 rekordot, azonosító-
  paritást, alkoholos sémákat, engedélyezett értékeket és kategóriahash-eket
  ellenőrzött; eltérés nem maradt.

### Brandy kézi felülvizsgálat, 26–39. tétel

- A brandylevél utolsó 14 teljes rekordját és forrássorát egyenként, mind a
  14 helyi termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A St. Rémy, Rémy Martin, Bardinet, Janneau, Lánchíd, Pâpidoux, Martell,
  Courvoisier, Hennessy, Napoleon, METAXA és ARARAT termékek márkája,
  kiszerelése, alkoholtartalma és íze egyezett a bizonyítékokkal.
- A Bardinet forrásneve pontatlanul konyakot ír, miközben a közvetlen
  csomagolás `Finest Brandy`; ezért a jelenlegi `Brandy` besorolást
  megtartottuk. Az Armagnac, Calvados és Cognac termékek is helyesen a
  közös brandylevélben szerepelnek.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **14** (`BTY-X17692900320021`,
  `BTY-X17906100320021`, `BTY-X18414400320021`,
  `BTY-X5452400320021`, `BTY-X17396300320021`,
  `BTY-X17642300320021`, `BTY-X20271300320021`,
  `BTY-X7164900320021`, `BTY-X17639800320021`,
  `8f389f45f4df8b8acc426e60`, `e8695885be44babcf7bd9a78`,
  `37d2a55e6326e7799e16d148`, `6f46834a7b8d82380f80b88d`, `121228872`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Adatírás nem történt. A teljes validáció 47 030 rekordot, azonosító-
  paritást, alkoholos sémákat, engedélyezett értékeket és kategóriahash-eket
  ellenőrzött; eltérés nem maradt.
- Ezzel a `Brandy` levél mind a **39** jelenlegi termékének kézi
  felülvizsgálata elkészült.

### Tequila kézi felülvizsgálat, 1–21. tétel

- A tequila-levél mind a 21 teljes rekordját és forrássorát egyenként,
  mind a 21 helyi termékképet közvetlenül, részletes felbontásban
  ellenőriztük.
- A Jose Cuervo, Don Diego, Sierra, El Jimador, Olmeca, Don Julio és
  Patrón termékek márkája, teljes és egységnyi kiszerelése,
  alkoholtartalma és natúr ízértéke egyezett a névvel, forrásadattal és
  csomagolással.
- A Blanco/Silver és Reposado megjelölések minden esetben egyeztek a
  közvetlen termékképpel. Ezekhez a meglévő tequila-sémában nincs külön
  tulajdonság, ezért új tulajdonságot nem hoztunk létre.
- A 12 × 50 ml-es Sierra Blanco teljes kiszerelése helyesen `600 ml`,
  egységnyi kiszerelése `50 ml`.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **21** (`693095:4230485`,
  `693098:4230488`, `BTY-X18115400320021`, `BTY-X17641200320021`,
  `BTY-X17490800320021`, `BTY-X17491000320021`,
  `BTY-X17641100320021`, `BTY-X17691400320021`,
  `BTY-X17691500320021`, `BTY-X17922300320021`,
  `BTY-X18115200320021`, `BTY-X16779200320021`,
  `BTY-X18823900320021`, `BTY-X8891100320021`,
  `927a5507dfef87690eacddda`, `fbb771f3903e9b1caa055ab7`, `121271744`,
  `120255587`, `121352378`, `121352418`, `121356299`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Adatírás nem történt. A teljes validáció 47 030 rekordot, azonosító-
  paritást, alkoholos sémákat, engedélyezett értékeket és
  kategóriahash-eket ellenőrzött; eltérés nem maradt.
- Ezzel a `Tequila` levél mind a **21** jelenlegi termékének kézi
  felülvizsgálata elkészült.

### Vermut és aperitif kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük. A 24
  elérhető helyi termékképet közvetlenül, részletes felbontásban
  megvizsgáltuk; a `3375566` azonosítójú Aperolhoz nincs helyi kép, ezért
  annál kizárólag a név és a forrásadat alapján ellenőriztünk.
- A Ravini, Aperini, Mionetto, Aperol, Garrone, Martini, Campari és
  Madruzzo termékek kategóriája, alkoholtartalma, édessége, színe és íze
  három kivétellel egyezett a bizonyítékokkal.
- A Mionetto alkoholos aperitif hivatalos termékleírása a névben szereplő
  keserűnarancs mellett citrusos és gyógynövényes ízjegyeket is igazol;
  ezeket a későbbi, azonos Mionetto-tétellel végzett összevetés során
  pótoltuk.
- A Lidl `10101673` Aperol-rekordján a forrás `700 ml` mennyisége és az
  azonos közvetlen 700 ml-es Aperol-csomagolás igazolja a kiszerelést és
  a 11%-os alkoholtartalmat; a két `ismeretlen` értéket pontosítottuk.
- A `BTY-X17941100320021` címkéjén és a forrás márkamezőjében is
  `Madruzzo` szerepel, ezért a hibás `RIOBA` márkát javítottuk.
- A Martini Fiero + Kinley Tonic csomag teljes kiszerelése helyesen
  `2500 ml`: 1000 ml vermut és 1500 ml tonik.
- Módosított rekord: **3**.
- Módosított tulajdonságmező: **4**.
- Változatlanul hagyott rekord: **22** (`982243`, `982244`, `4597572`,
  `713144:4250534`, `713141:4250531`,
  `751971:4289361`, `751974:4289364`, `751977:4289367`,
  `712961:4250351`, `712964:4250354`, `712982:4250372`,
  `712973:4250363`, `748872:4286262`, `3375566`, `2857575`, `2808667`,
  `10104537`, `BTY-X18326300320021`, `BTY-X17574700320021`,
  `BTY-X17575100320021`, `BTY-X17574800320021`,
  `BTY-X17575200320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A négy mezőt írás előtt összevetettük a teljes jelenlegi rekorddal,
  majd mindkét célzott rekordcsere után és a végén is lefutott a 47 030
  rekordot, azonosító-paritást, alkoholos sémákat, engedélyezett
  értékeket és kategóriahash-eket vizsgáló teljes ellenőrzés; eltérés
  nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `678179:4215569` | íz `keserűnarancs` → `citrus, gyógynövény, keserűnarancs` |
| `10101673` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `11%` |
| `BTY-X17941100320021` | márka `RIOBA` → `Madruzzo` |

### Vermut és aperitif kézi felülvizsgálat, 26–50. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Martini Extra Dry, Fiero, Rosso, Bianco, Rosato, Floreale és
  Vibrante, továbbá a Garrone, Aperol, Campari, Cinzano és Turchetto
  termékek meglévő adatai két rekord kivételével egyeztek a
  bizonyítékokkal.
- A `BTY-X18264500320021` alkoholmentes aperitif címkéje és forrásbeli
  márkamezője egyaránt `Madruzzo`; a hibás `RIOBA` értéket javítottuk.
- A `BTY-X18225800320021` Mionetto Alkohol Free közvetlen címkéje és a
  Mionetto hivatalos termékleírása 0,5% alatti alkoholtartalmat,
  vöröses-narancs színt, keserédes profilt, valamint citrusos,
  gyógynövényes és keserűnarancsos ízjegyeket igazol. A levél már meglévő
  elemi értékeivel pontosítottuk a négy mezőt.
- Módosított rekord: **2**.
- Módosított tulajdonságmező: **5**.
- Változatlanul hagyott rekord: **23** (`BTY-X17598800320021`,
  `BTY-X17598900320021`, `BTY-X17599000320021`,
  `BTY-X17599200320021`, `BTY-X17599100320021`,
  `BTY-X17599800320021`, `BTY-X17616300320021`, `1008048`, `1008049`,
  `1007135`, `704414d96969b9900bc88be9`, `6efd4becd0ba22f4ea7470cf`,
  `8a1f69c3423e498eca18934d`, `b0a9f75b44c03153ef907e10`,
  `b7379a5cc20532bb2aea8a01`, `d2570463a203fd4a2468b537`,
  `4d588b0ce5a9bb5bcb80cd31`, `38a682a29f63d2756ea77c37`,
  `29711436c2aa64cfb3a6028c`, `121234052`, `121257923`, `121234000`,
  `121256982`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A változtatások előtt ellenőriztük a pontos előértékeket, majd
  mindkét rekordcsere után és a végén is lefutott a teljes validáció;
  eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18264500320021` | márka `RIOBA` → `Madruzzo` |
| `BTY-X18225800320021` | alkoholtartalom `0%` → `0,5%`; édesség `egyéb` → `keserédes`; szín `egyéb` → `narancs`; íz `natúr` → `citrus, gyógynövény, keserűnarancs` |

### Vermut és aperitif kézi felülvizsgálat, 51–53. tétel

- A levél utolsó három teljes rekordját és forrássorát egyenként, mind a
  három helyi termékképet közvetlenül, részletes felbontásban
  ellenőriztük.
- A Martini Floreale alkoholmentes státusza, 0,5% alatti
  alkoholtartalma, fehér színe és virágos íze minden bizonyítékkal
  egyezett.
- A Mionetto alkoholos aperitif hivatalos ízprofilja a keserűnarancs
  mellett citrusos és gyógynövényes jegyeket is igazol; ezeket ezen és a
  korábban ellenőrzött, azonos 500 ml-es Mionetto-rekordon is pótoltuk.
- Az Appelle Moi Bitter & Orange közvetlen képe narancsszínű italt
  igazol, ezért az `egyéb` színt `narancs` értékre pontosítottuk.
- Módosított rekord az 51–53. tételben: **2**.
- Módosított tulajdonságmező az 51–53. tételben: **2**.
- Változatlanul hagyott rekord: **1** (`121273742`).
- Korábbi, azonos termékváltozaton szinkronizált rekord: **1**
  (`678179:4215569`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **1** (`márka: RIOBA`).
- A `RIOBA` eltávolítása előtt célzottan igazoltuk, hogy a levél egyetlen
  termékrekordja sem használja. A rekordjavítások és a fa-patch után
  lefutott a teljes validáció, továbbá a levélbeli `RIOBA`-használat és
  faérték hiányát vizsgáló külön ellenőrzés; eltérés nem maradt.
- Ezzel a `Vermut és aperitif` levél mind az **53** jelenlegi termékének
  kézi felülvizsgálata elkészült.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121257036` | íz `keserűnarancs` → `citrus, gyógynövény, keserűnarancs` |
| `121237498` | szín `egyéb` → `narancs` |

### Rum kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Old Hopking fehér rum közvetlen palackcímkéjén a `37,5% vol`
  felirat olvasható, ezért az ismeretlen alkoholtartalmat pontosítottuk.
- A két Bacardi Carta Blanca és két további kiszerelésük közül kizárólag
  a 700 ml-es rekord, valamint a Captain Morgan White rekord fajtaértéke
  volt hibás. A nevük és címkéjük alapján az `egyéb rum` értéket mindkét
  esetben `fehér` értékre javítottuk.
- A The Demon's Share 3 éves és 6 éves rum pontos termékadatai, valamint
  a Bumbu XO gyártói termékleírása egyaránt `40%` alkoholtartalmat
  igazol; a három `ismeretlen` értéket ennek megfelelően javítottuk.
- A Bumbu Original gyártói leírása természetes ízesítésű, válogatott
  fűszerekkel készülő rumként határozza meg a terméket. A Rum-levél
  meglévő fajtaértékei közül ezért a `barna` helyett a `fűszeres` a
  bizonyított besorolás.
- A Bacardi, Havana Club, Dictador, Diplomático, Don Papa, El Nino,
  Silverstone, St Simon és Plantation többi vizsgált rekordjának
  kategóriája, kiszerelése, alkoholtartalma és fajtaértéke egyezett a
  teljes forrásadattal és a csomagolással.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **7**.
- Változatlanul hagyott rekord: **18** (`997155`,
  `684002:4221392`, `712889:4250279`, `712892:4250282`,
  `774333:4311723`, `712904:4250294`, `712907:4250297`,
  `712886:4250276`, `760827:4298217`, `409394:3946751`,
  `712511:4249901`, `712520:4249910`, `827153:4364543`,
  `712898:4250288`, `684338:4221728`, `713738:4251128`,
  `874958:4412348`, `761403:4298793`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A hét mezőt írás előtt összevetettük a teljes jelenlegi rekorddal,
  majd minden célzott rekordcsere után és a végén is lefutott a 47 030
  rekordot, azonosító-paritást, alkoholos sémákat, engedélyezett
  értékeket és kategóriahash-eket vizsgáló teljes ellenőrzés; eltérés
  nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `539237` | alkoholtartalom `ismeretlen` → `37,5%` |
| `712883:4250273` | fajta `egyéb rum` → `fehér` |
| `674984:4212374` | fajta `egyéb rum` → `fehér` |
| `963527:4500917` | alkoholtartalom `ismeretlen` → `40%` |
| `748851:4286241` | fajta `barna` → `fűszeres` |
| `963524:4500914` | alkoholtartalom `ismeretlen` → `40%` |
| `751935:4289325` | alkoholtartalom `ismeretlen` → `40%` |

### Rum kézi felülvizsgálat, 26–50. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük. A 24
  elérhető helyi termékképet közvetlenül, részletes felbontásban
  megvizsgáltuk; a `3376037` azonosítójú Bumbu Original rekordhoz nincs
  helyi kép, ezért annál a pontos név, a forrásadat és a gyártói
  termékleírás szolgált bizonyítékul.
- A Bumbu Original három előfordulását és a Kraken Black Spiced két
  előfordulását a nevük, csomagolásuk és gyártói leírásuk alapján az
  általános `egyéb rum` helyett `fűszeres` fajtára javítottuk.
- A Bacardi Carta Blanca két rekordja, a Captain Morgan White és a
  Havana Club 3 éves Fehér Rum közvetlenül `fehér` megjelölésű. A
  Papa’s Pilar Blonde terméket a gyártó light rumként határozza meg,
  ezért ez is a meglévő `fehér` értéket kapta.
- A Dictador 10YO, Diplomatico Mantuano, Diplomatico Reserva Exclusiva,
  Bumbu XO, Don Papa, Don Papa Baroko, Matusalem 15 éves és Brugal 1888
  érlelt, barna változatai a képek és az azonos termékváltozatok
  összevetése alapján `barna` fajtát kaptak.
- A Captain Morgan Dark és a dokumentáltan dark rum típusú Portorico 60
  esetében az `egyéb rum` értéket `sötét` értékre pontosítottuk.
- A négy Lidl-rekord hiányzó kiszerelését a teljes forrássor igazolja. A
  Diplomatico Mantuano és Bumbu Original azonos, pontos másik
  termékváltozatai, a Professorado gyártói oldala, valamint a The
  Demon's Share pontos palackváltozata igazolta a hiányzó
  alkoholtartalmakat és fajtaértékeket.
- Az Eminente Reserva és a Bacardi Carta Oro minden vizsgált mezője
  egyezett a névvel, forrásadattal és csomagolással.
- Módosított rekord: **23**.
- Módosított tulajdonságmező: **31**.
- Változatlanul hagyott rekord: **2** (`712631:4250021`,
  `BTY-X17490000320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 31 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal, majd
  minden célzott rekordcsere után és a végén is lefutott a 47 030
  rekordos teljes validáció; séma-, érték-, hash- vagy
  azonosító-paritási eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `3376037` | fajta `egyéb rum` → `fűszeres` |
| `3134742` | fajta `egyéb rum` → `barna` |
| `2817613` | fajta `egyéb rum` → `fehér` |
| `2817553` | fajta `egyéb rum` → `fűszeres` |
| `10038374` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `40%`; fajta `egyéb rum` → `barna` |
| `10041708` | kiszerelés `ismeretlen` → `500 ml`; alkoholtartalom `ismeretlen` → `38%`; fajta `egyéb rum` → `arany` |
| `10041709` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `40%`; fajta `egyéb rum` → `fűszeres` |
| `10107319` | kiszerelés `ismeretlen` → `500 ml`; alkoholtartalom `ismeretlen` → `40%`; fajta `egyéb rum` → `arany` |
| `BTY-X17620200320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17489800320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X17592900320021` | fajta `egyéb rum` → `fűszeres` |
| `BTY-X17620800320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17401800320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X17593000320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17949100320021` | fajta `egyéb rum` → `barna` |
| `BTY-X18358300320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17620300320021` | fajta `egyéb rum` → `fűszeres` |
| `BTY-X17579600320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17490300320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17670200320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X17489900320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X17396700320021` | fajta `egyéb rum` → `sötét` |
| `BTY-X17397500320021` | fajta `egyéb rum` → `sötét` |

### Rum kézi felülvizsgálat, 51–75. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Old Pascas Fehér, Diplomático Planas, Royal Port White, Santa Lucia
  fehér, Bacardi Carta Blanca és Captain Morgan White rekordjain, továbbá
  a gyártó által light rumként meghatározott Papa’s Pilar Blonde
  változaton az `egyéb rum` fajtát `fehér` értékre javítottuk.
- A Royal Port Brown, Zacapa 23, The Demon's Share 6 éves, Bacardi Gran
  Reserva Diez, Santa Lucia barna, Diplomático Exclusiva és Mantuano
  érlelt, barna termékei `barna` fajtaértéket kaptak.
- A CANEROCK gyártói termékazonosítása jamaicai spiced rumot igazol. A
  Takamaka Dark Spiced és a Bumbu Original termékekkel együtt ezért a
  meglévő `fűszeres` fajtaértéket kapták.
- A negyedik és egyben utolsó `The Demons Share` márkaértékű rekord
  ellenőrzése után mind a négy közvetlen palackcímkén és forrásnévben
  szereplő helyes `The Demon's Share` alakot egységesen átvezettük. A
  helyes értéket felvettük, a használat nélkül maradt hibás értéket
  töröltük a Rum-levélből.
- A Bacardi Reserva Ocho, Old Pascas Dark, Sober Spirits alkoholmentes
  rumjellegű ital, Bacardi Carta Negra és Bacardi Carta Oro rekordjának
  minden vizsgált mezője változatlanul helyes.
- Módosított rekord az 51–75. tételben: **20**.
- Módosított tulajdonságmező az 51–75. tételben: **21**.
- Változatlanul hagyott rekord: **5** (`BTY-X17490100320021`,
  `BTY-X17642500320021`, `BTY-X18490000320021`,
  `227caff943f7fe8317db732b`, `0b05f3c48d1c2a32f5d69675`).
- Korábban ellenőrzött, azonos márkanévvel szinkronizált rekord: **3**
  (`963527:4500917`, `963524:4500914`, `10107319`).
- Új megengedett érték: **1** (`márka: The Demon's Share`).
- Törölt megengedett érték: **1** (`márka: The Demons Share`).
- A teljes művelet 23 rekord 24 mezőjét érintette. A rekordcserék előtt,
  minden csere után, majd a régi faérték törlése után is lefutott a
  47 030 rekordos teljes validáció; külön ellenőrzés igazolta, hogy a
  helyes márkaérték jelen van, a régi érték és annak termékoldali
  használata pedig hiányzik.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17642900320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X17620100320021` | fajta `egyéb rum` → `fűszeres` |
| `BTY-X14581500320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X17310700320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X17310800320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17402300320021` | fajta `egyéb rum` → `barna` |
| `BTY-X17621000320021` | márka `The Demons Share` → `The Demon's Share`; fajta `egyéb rum` → `barna` |
| `BTY-X17856200320021` | fajta `egyéb rum` → `fűszeres` |
| `BTY-X18304200320021` | fajta `egyéb rum` → `fehér` |
| `BTY-X18551500320021` | fajta `egyéb rum` → `barna` |
| `1012969` | fajta `egyéb rum` → `fehér` |
| `1032367` | fajta `egyéb rum` → `barna` |
| `c2f94ab7b2fa55d04874d83e` | fajta `egyéb rum` → `fehér` |
| `354ea2c4adad2eccc5ec0af8` | fajta `egyéb rum` → `fűszeres` |
| `9f51e71b9470cf5c8854c998` | fajta `egyéb rum` → `fehér` |
| `ca72f89770cedb13a2ed882c` | fajta `egyéb rum` → `fehér` |
| `3e904f1b94b92192ea040c31` | fajta `egyéb rum` → `barna` |
| `121218423` | fajta `egyéb rum` → `fehér` |
| `121248370` | fajta `egyéb rum` → `barna` |
| `121256037` | fajta `egyéb rum` → `fűszeres` |
| `963527:4500917` | márka `The Demons Share` → `The Demon's Share` |
| `963524:4500914` | márka `The Demons Share` → `The Demon's Share` |
| `10107319` | márka `The Demons Share` → `The Demon's Share` |

### Rum kézi felülvizsgálat, 76–86. tétel

- A Rum-levél utolsó 11 teljes rekordját és forrássorát egyenként, mind
  a 11 helyi termékképet közvetlenül, részletes felbontásban
  ellenőriztük.
- A Captain Morgan White és República de Caña White rekordjain az
  `egyéb rum` fajtát `fehér` értékre javítottuk.
- A Takamaka Dark Spiced közvetlen termékneve és címkéje `fűszeres`, a
  República de Caña Black pedig `sötét` fajtát igazol.
- A Diplomático Exclusiva és Zacapa Solera érlelt, barna változatai
  `barna` fajtaértéket kaptak. A Planteray Barbados 5 Years gyártói
  leírása az ötéves érlelt változatot, a közvetlen palackkép pedig
  aranyszínű italt igazol, ezért az `arany` értéket alkalmaztuk.
- A Bacardi Carta Negra, Havana Club Añejo Especial, Sailor Jerry és Don
  Papa rekordjának minden vizsgált mezője változatlanul helyes.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **7**.
- Változatlanul hagyott rekord: **4** (`121273903`, `121228895`,
  `121255810`, `121327207`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A hét mezőt írás előtt összevetettük a teljes jelenlegi rekorddal,
  majd minden célzott rekordcsere után és a végén is lefutott a 47 030
  rekordos teljes validáció; eltérés nem maradt.
- Ezzel a `Rum` levél mind a **86** jelenlegi termékének kézi
  felülvizsgálata elkészült.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121221516` | fajta `egyéb rum` → `fehér` |
| `121248358` | fajta `egyéb rum` → `barna` |
| `121255827` | fajta `egyéb rum` → `fűszeres` |
| `111237209` | fajta `egyéb rum` → `arany` |
| `121221891` | fajta `egyéb rum` → `barna` |
| `121228359` | fajta `egyéb rum` → `sötét` |
| `121228405` | fajta `egyéb rum` → `fehér` |

### Gin kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Johnsen Pink közvetlen címkéje `Wild Berry Flavoured Distilled Gin`
  megjelölést és 37,5%-os alkoholtartalmat mutat. Az ízesített gin
  gyümölcsösségét `true`, ismeretlen ízét `erdei gyümölcs` értékre
  javítottuk.
- A Johnsen Club palackcímkéje, az Old Inn pontos termékadata, valamint a
  Beefeater azonos 700 ml-es változata igazolta a három hiányzó
  alkoholtartalmat.
- Az Agárdi Chameleon címkéjén `Distilled Gin`, az Opera hivatalos
  terméknevében `Budapest Dry Gin` szerepel; ezért az `egyéb gin`
  értéket rendre `desztillált gin`, illetve `dry gin` értékre
  pontosítottuk.
- A Mandaley, Coventry, Finsbury, Kalumba, Beefeater, Gordon’s, Bombay
  Sapphire, Tanqueray és Bulldog többi vizsgált rekordjának márkája,
  gyümölcsössége, kiszerelése, alkoholtartalma, íze és gin-típusa
  egyezett a névvel, forrásadattal és csomagolással.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **7**.
- Változatlanul hagyott rekord: **19** (`1018160`,
  `784562:4321952`, `683810:4221200`, `683813:4221203`,
  `674543:4211933`, `674546:4211936`, `658827:4196217`,
  `674549:4211939`, `751926:4289316`, `751929:4289319`,
  `751932:4289322`, `674540:4211930`, `674537:4211927`,
  `691487:4228877`, `674531:4211921`, `674981:4212371`,
  `712880:4250270`, `770331:4307721`, `691490:4228880`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A hét mezőt írás előtt összevetettük a teljes jelenlegi rekorddal,
  majd minden célzott rekordcsere után és a végén is lefutott a 47 030
  rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `911141` | gyümölcsös `false` → `true`; íz `ismeretlen` → `erdei gyümölcs` |
| `533680` | alkoholtartalom `ismeretlen` → `37,5%` |
| `680210:4217600` | alkoholtartalom `ismeretlen` → `37,5%` |
| `677756:4215146` | fajta `egyéb gin` → `desztillált gin` |
| `797189:4334579` | alkoholtartalom `ismeretlen` → `40%` |
| `713771:4251161` | fajta `egyéb gin` → `dry gin` |

### Gin kézi felülvizsgálat, 26–50. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük. A 23
  elérhető helyi termékképet közvetlenül, részletes felbontásban
  megvizsgáltuk; a `3376039` és `2807380` rekordhoz nem volt helyi kép.
- A Búzavirág közvetlen címkéje `Dry Gin` megjelölést mutat, a gyártói
  leírás pedig a már rögzített virágos ízprofilt igazolja. A fajta ezért
  `dry gin` értékre pontosult.
- A Drumshanbo címkéjén 43%-os alkoholtartalom olvasható. A helyi kép
  nélküli Bombay Sapphire pontos termékneve és az azonos, képpel
  ellenőrzött változat `London dry gin` típust igazol.
- A Hendrick's és Roku Lidl-rekordjain a teljes forrássor 700 ml-es
  kiszerelést mutat; a közvetlen termékkép és az azonos termékváltozat
  rendre 41,4%, illetve 43% alkoholtartalmat igazol.
- A Hampstead Pink Gin 500 ml-es, 40%-os, piros bogyós gyümölcsökkel
  ízesített változat. A görögdinnyés Hampstead 700 ml-es, 37,5%-os
  ízesített gin.
- A két változatot felsoroló Tanqueray-forrásnévvel szemben a közvetlen
  termékkép egyértelműen a 700 ml-es, 41,3%-os Blackcurrant Royale
  palackot mutatja. Ezért a hibás narancs ízt eltávolítottuk, és a fajtát
  `ízesített gin` értékre javítottuk.
- A Malfy Rosa, Balaton, Hendrick's, Roku, Never Never, valamint a
  Kalumba, Beefeater, Bombay Sapphire, Gordon's és Tanqueray Metro-tételek
  többi vizsgált tulajdonsága egyezett a teljes névvel, forrássorral és
  csomagolással.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **23**.
- Változatlanul hagyott rekord: **17** (`795164:4332554`,
  `764673:4302063`, `684728:4222118`, `683825:4221215`,
  `990878:4528268`, `3376039`, `BTY-X17594200320021`,
  `BTY-X17192300320021`, `BTY-X17401500320021`,
  `BTY-X17591500320021`, `BTY-X17591400320021`,
  `BTY-X17639500320021`, `BTY-X17397700320021`,
  `BTY-X17489400320021`, `BTY-X17400900320021`,
  `BTY-X17401200320021`, `BTY-X17397900320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 23 mezőt írás előtt összevetettük a teljes jelenlegi rekorddal, majd
  minden célzott rekordcsere után és a végén is lefutott a 47 030
  rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `677996:4215386` | fajta `egyéb gin` → `dry gin` |
| `980096:4517486` | alkoholtartalom `ismeretlen` → `43%` |
| `2807380` | fajta `egyéb gin` → `London dry gin` |
| `10038362` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `41,4%`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10038370` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `43%`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10106410` | gyümölcsös `false` → `true`; kiszerelés `ismeretlen` → `500 ml`; alkoholtartalom `ismeretlen` → `40%`; íz `ismeretlen` → `erdei gyümölcs`; egységnyi kiszerelés `ismeretlen` → `500 ml` |
| `10107317` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `37,5%`; fajta `egyéb gin` → `ízesített gin`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10107431` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `41,3%`; íz `fekete ribizli, narancs` → `fekete ribizli`; fajta `egyéb gin` → `ízesített gin`; egységnyi kiszerelés `ismeretlen` → `700 ml` |

### Gin kézi felülvizsgálat, 51–75. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Gordon's Premium Pink hivatalos leírása eper, málna és piros ribizli
  ízt közöl; a korábbi `fekete ribizli` ezért pontosítva lett.
- A Tanqueray No. TEN gyártói oldala egész citrusgyümölcsökből, kis
  adagokban végzett lepárlást, valamint citrusos ízprofilt igazol. A
  rekord gyümölcsössége, íze és fajtája ennek megfelelően változott.
- A Bombay Sapphire Sunset hivatalos termékadata szerint az ízprofil
  spanyol mandarinból, kardamomból és kurkumából áll. A pontatlan
  `narancs` ízt ezért `mandarin` értékre javítottuk.
- A Hendrick's Grand Cabaret gyártói leírása határozott
  csonthéjasgyümölcs-profilt és édes fűszernövényeket közöl. A korábbi
  `natúr` helyett ezt az ízt, `true` gyümölcsösséget és `ízesített gin`
  fajtát rögzítettünk.
- A Monkey 47 közvetlen címkéjén `Schwarzwald Dry Gin` szerepel. A
  Drumshanbo címkéje és gyártói oldala Gunpowder teát, valamint kézi,
  rézüstös lepárlást igazol; emiatt a jelenlegi tétel és a korábban
  ellenőrzött azonos rekord is `desztillált gin` fajtát kapott.
- A többi Kalumba, Tanqueray, Malfy, Roku, Hendrick's, Beefeater,
  Bobby's, Bombay Sapphire, Finsbury, Balaton, ETSU és The Botanist
  rekord minden vizsgált mezője egyezett a névvel, forrássorral és
  csomagolással.
- Módosított rekord az 51–75. tételben: **6**.
- Módosított tulajdonságmező az 51–75. tételben: **11**.
- Változatlanul hagyott rekord: **19** (`BTY-X17398000320021`,
  `BTY-X17401400320021`, `BTY-X17401600320021`,
  `BTY-X17591800320021`, `BTY-X17592000320021`,
  `BTY-X18227100320021`, `BTY-X18889900320021`,
  `BTY-X18906500320021`, `BTY-X18936300320021`,
  `BTY-X17591600320021`, `BTY-X17618700320021`,
  `BTY-X17489600320021`, `BTY-X17564100320021`,
  `BTY-X17643200320021`, `BTY-X17593600320021`,
  `BTY-X17619400320021`, `BTY-X17627300320021`,
  `BTY-X17636300320021`, `BTY-X17683300320021`).
- Korábban ellenőrzött, azonos Drumshanbo-termékkel szinkronizált
  rekord: **1** (`980096:4517486`).
- Új megengedett érték: **3** (`íz: csonthéjas gyümölcs`,
  `íz: mandarin`, `íz: piros ribizli`).
- Törölt megengedett érték: **0**.
- A teljes művelet 7 rekord 12 mezőjét érintette. A három faérték
  felvétele után, minden rekordcsere után és a végén is lefutott a
  47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17401000320021` | íz `eper, málna, fekete ribizli` → `eper, málna, piros ribizli` |
| `BTY-X17401100320021` | gyümölcsös `false` → `true`; íz `natúr` → `citrus`; fajta `egyéb gin` → `desztillált gin` |
| `BTY-X17489700320021` | íz `narancs` → `mandarin` |
| `BTY-X17555000320021` | gyümölcsös `false` → `true`; íz `natúr` → `csonthéjas gyümölcs`; fajta `egyéb gin` → `ízesített gin` |
| `BTY-X17594300320021` | fajta `egyéb gin` → `dry gin` |
| `BTY-X17619500320021` | íz `natúr` → `tea`; fajta `egyéb gin` → `desztillált gin` |
| `980096:4517486` | fajta `egyéb gin` → `desztillált gin` |

### Gin kézi felülvizsgálat, 76–100. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük. A 24
  elérhető helyi termékképet közvetlenül, részletes felbontásban
  megvizsgáltuk; a `BTY-X18709500320022` rekordhoz nem volt helyi kép.
- Az Opera gyártói leírása szerint a termék teljesíti a London Dry
  követelményeit; a meglévő besorolási rendszerben ezért a már használt
  `dry gin` értékre pontosult. A két Agárdi Chameleon közvetlen címkéjén
  `Distilled Gin` olvasható.
- A Brockmans gyártói oldala az áfonya mellett szedret is tételesen
  megnevez, ezért ezt a második ízt is rögzítettük.
- A Hendrick's Oasium gyártói leírása aromás fűszernövényekkel és élénk,
  citrusos gyümölcsprofillal készült különkiadást igazol. A rekord
  gyümölcsössége `true`, íze `citrus`, fajtája `ízesített gin` lett.
- A második Gordon's Premium Pink rekordon is `piros ribizli` váltotta a
  téves `fekete ribizli` értéket.
- A közvetlen Hendrick's-palackokon szereplő lepárlási jelölést az
  aktuális és három korábban kézzel ellenőrzött, azonos jellegű rekordon
  egységesen `desztillált gin` fajtával rögzítettük.
- Az Oyster Fine de Claire Wild Citrus és kép nélküli gyűjtőkarton,
  Tanqueray 0.0, PY'S, Bombay Sapphire, Roku, Beefeater, Tanqueray,
  Kalumba, Bulldog, Finsbury és Gordon's többi vizsgált tulajdonsága
  egyezett a teljes névvel, forrássorral és — ahol volt — a
  csomagolással.
- Módosított rekord a 76–100. tételben: **7**.
- Módosított tulajdonságmező a 76–100. tételben: **9**.
- Változatlanul hagyott rekord: **18** (`BTY-X17700300320021`,
  `BTY-X18709400320021`, `BTY-X18709500320022`,
  `BTY-X18203000320021`, `1012967`, `1012968`,
  `e2050249aee8cc376422e9fc`, `6262a17b057e3ae43d691841`,
  `68fc6afdf8147df2bb70ebbe`, `5736adc796c3c9a2e0b330ca`,
  `3d989a510d64ba8805d10df8`, `ced267db55df9bffb647fb01`,
  `d6f680e61d9c08fc02273ddb`, `51d251f277bc4a25f927adc1`,
  `9346b027667ecad3bf1bb909`, `ce8e7e92c87ee197b4c6d241`,
  `f7411e769590bb48481e4b93`, `e7b9a10667e2510499246a93`).
- Korábban ellenőrzött, azonos Hendrick's-termékkel szinkronizált rekord:
  **3** (`684728:4222118`, `10038362`, `BTY-X18889900320021`).
- Új megengedett érték: **1** (`íz: szeder`).
- Törölt megengedett érték: **0**.
- A teljes művelet 10 rekord 12 mezőjét érintette. A faérték felvétele
  után, minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17696400320021` | fajta `egyéb gin` → `dry gin` |
| `BTY-X17697900320021` | fajta `egyéb gin` → `desztillált gin` |
| `BTY-X17830200320021` | íz `áfonya` → `áfonya, szeder` |
| `BTY-X18230600320021` | gyümölcsös `false` → `true`; íz `natúr` → `citrus`; fajta `egyéb gin` → `ízesített gin` |
| `80ba61a199117ca3bfa77303` | fajta `egyéb gin` → `desztillált gin` |
| `aec8d45e6ab03ad4568853ef` | íz `eper, málna, fekete ribizli` → `eper, málna, piros ribizli` |
| `e8822a67bb6f46d91a22034d` | fajta `egyéb gin` → `desztillált gin` |
| `684728:4222118` | fajta `egyéb gin` → `desztillált gin` |
| `10038362` | fajta `egyéb gin` → `desztillált gin` |
| `BTY-X18889900320021` | fajta `egyéb gin` → `desztillált gin` |

### Gin kézi felülvizsgálat, 101–125. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Bombay Sapphire Sunset gyártói ízleírásának megfelelően a pontatlan
  `narancs` helyett `mandarin` ízt rögzítettünk.
- A Gordon's Premium Pink ízét a gyártó által megnevezett eper, málna és
  piros ribizli összetételre pontosítottuk.
- A Hendrick's eredeti változatának palackjelölése alapján a fajtát
  `desztillált gin` értékre javítottuk.
- A Citadelle Original gyártói leírása száraz karaktert közöl. Emiatt az
  aktuális rekord és a korábban átnézett, azonos termék fajtáját is
  egységesen `dry gin` értékre állítottuk.
- A Tanqueray Blackcurrant Royale és Flor de Sevilla egyértelműen
  ízesített változat, ezért mindkét rekord `ízesített gin` lett.
- Az Ironcides teljes termékneve és közvetlen címkéje is `London Dry
  Gin` megjelölést mutat; a fajta ennek megfelelően pontosult.
- Az Oxford, Bombay Sapphire, Beefeater, Finsbury, Kalumba, Tanqueray,
  Malfy, Bulldog, Harahorn, Old Tower és a többi vizsgált gin minden
  ellenőrizhető mezője egyezett a teljes névvel, forrássorral és
  csomagolással.
- Módosított rekord a 101–125. tételben: **7**.
- Módosított tulajdonságmező a 101–125. tételben: **7**.
- Változatlanul hagyott rekord: **18**
  (`10bf2a94a9ced21d8a128df7`, `ab15a5abcd09145e03fd6925`,
  `e858a26a5b927bb584950035`, `8f70863ff4715ac9e096bd0f`,
  `121218775`, `121229462`, `121228624`, `121229485`, `121221401`,
  `121221240`, `121221332`, `121229491`, `121221418`, `121256642`,
  `121234017`, `121256596`, `121228630`, `121231153`).
- Korábban ellenőrzött, azonos Citadelle Original termékkel
  szinkronizált rekord: **1** (`BTY-X17700300320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A teljes művelet 8 rekord 8 mezőjét érintette. Minden rekordcsere után
  és a végén is lefutott a 47 030 rekordos teljes validáció; eltérés nem
  maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121219042` | íz `narancs` → `mandarin` |
| `121221793` | íz `eper, málna, fekete ribizli` → `eper, málna, piros ribizli` |
| `121220788` | fajta `egyéb gin` → `desztillált gin` |
| `121257727` | fajta `egyéb gin` → `dry gin` |
| `121256538` | fajta `egyéb gin` → `ízesített gin` |
| `121221424` | fajta `egyéb gin` → `ízesített gin` |
| `121227735` | fajta `egyéb gin` → `London dry gin` |
| `BTY-X17700300320021` | fajta `desztillált gin` → `dry gin` |

### Gin kézi felülvizsgálat, 126–135. tétel

- A gin ág utolsó 10 teljes rekordját és forrássorát egyenként, mind a 10
  helyi termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Old Tower teljes termékneve és közvetlen palackcímkéje `London Dry
  Gin` megjelölést mutat.
- A The Foxtale gyártói oldala a Very Berry változatot áfonyásként, a
  Pink változatot eperrel és borsmentával készülő ízesített ginként írja
  le. A Pineapple név és palack az ananászos változatot azonosítja.
- Az Ukiyo gyártói oldala szerint a Japanese Blossom gint
  cseresznyevirágot is tartalmazó botanikákkal együtt desztillálják,
  ezért a fajtája `desztillált gin` lett.
- A Roku Sakura teljes neve kifejezetten ízesített gint közöl. A Tarsier
  Lychee & Raspberry és a Kalumba Purple Hibiscus egyértelmű
  ízváltozatait szintén `ízesített gin` fajtával rögzítettük; ez az
  azonos, korábban ellenőrzött Roku- és Kalumba-rekordokkal is egyezik.
- A Balaton Gin és a Tanqueray 0.0 minden ellenőrizhető mezője egyezett
  a névvel, forrássorral és csomagolással.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **2** (`121298586`, `121273990`).
- Új megengedett érték: **1** (`íz: borsmenta`).
- Törölt megengedett érték: **0**.
- Az új faérték felvétele után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121231205` | fajta `egyéb gin` → `London dry gin` |
| `121305873` | íz `erdei gyümölcs` → `áfonya`; fajta `egyéb gin` → `ízesített gin` |
| `121305913` | fajta `egyéb gin` → `ízesített gin` |
| `121305925` | gyümölcsös `false` → `true`; íz `ismeretlen` → `eper, borsmenta`; fajta `egyéb gin` → `ízesített gin` |
| `121305936` | fajta `egyéb gin` → `desztillált gin` |
| `121338177` | fajta `egyéb gin` → `ízesített gin` |
| `121345387` | fajta `egyéb gin` → `ízesített gin` |
| `121357972` | fajta `egyéb gin` → `ízesített gin` |

### Pálinka kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Aldi saját márkás, a Villányi, Bolyhos, Óbester, Magna, Rézangyal,
  Zwack Kosher, Márkházi és Panyolai termékek márkája, gyümölcse,
  pálinkafajtája, kiszerelése és — ahol a név nem közölte — a közvetlen
  címkéről leolvasható alkoholtartalma egyezett a rekorddal.
- A Rézangyal Barrique szilvapálinka közvetlen neve és címkéje mellett a
  gyártói leírás is hordós érlelést igazol. A meglévő
  `gyümölcspálinka` fajta ezért az `érlelt pálinka` értékkel egészült ki.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **24** (`823314`, `828946`, `4599216`,
  `4599217`, `62966:3600047`, `21958:21961`, `29674:29677`,
  `29677:29680`, `59454:59793`, `29680:29683`, `29686:29689`,
  `29689:29692`, `674597:4211987`, `661353:4198743`,
  `444049:3981433`, `15361:15364`, `15352:15355`,
  `674600:4211990`, `265436:3802718`, `59421:59760`,
  `64859:3601940`, `135398:3672614`, `135359:3672575`,
  `135392:3672608`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A rekordcsere után és a végén is lefutott a 47 030 rekordos teljes
  validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `15355:15358` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |

### Pálinka kézi felülvizsgálat, 26–50. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Magna, Panyolai, Nobilis, Árpád, Bolyhos, Rónasági, Magyar és Zwack
  Kosher termékek márkája, gyümölcse, pálinkafajtája, kiszerelése és
  alkoholtartalma egyezett a teljes névvel, forrássorral és címkével.
- A Panyolai Elixír szatmári szilvapálinka neve és közvetlen címkéje is
  egyértelműen érlelt terméket azonosít. A meglévő
  `gyümölcspálinka` fajta ezért az `érlelt pálinka` értékkel egészült ki.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **24** (`444583:3981967`,
  `59442:59781`, `685103:4222493`, `946247:4483637`,
  `59439:59778`, `BTY-X16498500320021`, `BTY-X13415200320021`,
  `BTY-X5584800320021`, `BTY-X7382000320021`,
  `BTY-X80485300320022`, `BTY-X59200400320022`,
  `BTY-X5585000320021`, `BTY-X59201800320022`,
  `BTY-X5599900320021`, `BTY-X59203200320022`,
  `BTY-X9482600320021`, `BTY-X6929500320021`,
  `BTY-X7382300320021`, `BTY-X95852400320022`,
  `BTY-X74078900320021`, `BTY-X17397200320021`,
  `BTY-X5584900320021`, `BTY-X10062000320021`,
  `BTY-X10062100320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A rekordcsere után és a végén is lefutott a 47 030 rekordos teljes
  validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `54492:54831` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |

### Pálinka kézi felülvizsgálat, 51–75. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Magna, Rézangyal, Favágó, Rónasági, Bolyhos, Óbester, Mátyás,
  Hortobágyi Betyár, Agárdi, Márkházi és Magyar termékek márkája,
  gyümölcse, pálinkafajtája, kiszerelése és alkoholtartalma egyezett a
  teljes névvel, forrássorral és címkével.
- A Bolyhos Ágyas Fűszeres Cseresznye teljes neve a cseresznye mellett
  kifejezetten fűszeres ízjelleget közöl. A rekord íze ezzel a közvetlenül
  bizonyított, új megengedett értékkel egészült ki.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **24** (`BTY-X10062200320021`,
  `BTY-X13174600320021`, `BTY-X13174800320021`,
  `BTY-X13174900320021`, `BTY-X13414200320021`,
  `BTY-X13414400320021`, `BTY-X13414600320021`,
  `BTY-X13414700320021`, `BTY-X13414900320021`,
  `BTY-X13415300320021`, `BTY-X13415400320021`,
  `BTY-X17398100320021`, `BTY-X17398300320021`,
  `BTY-X17610300320021`, `BTY-X17610400320021`,
  `BTY-X17610500320021`, `BTY-X17610900320021`,
  `BTY-X17646200320021`, `BTY-X18180900320021`,
  `BTY-X18181000320021`, `BTY-X18248500320021`,
  `BTY-X18248600320021`, `BTY-X18495800320021`,
  `BTY-X18495900320021`).
- Új megengedett érték: **1** (`íz: fűszeres`).
- Törölt megengedett érték: **0**.
- Az új faérték felvétele után, a rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X16498700320021` | íz `cseresznye` → `cseresznye, fűszeres` |

### Pálinka kézi felülvizsgálat, 76–100. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Panyolai, Bolyhos, Rézangyal, Magyar, Agárdi, Zwack Kosher,
  Szépvölgyi és Éden termékek márkája, gyümölcse, kiszerelése és
  alkoholtartalma egyezett a teljes névvel, forrássorral és címkével.
- Két Panyolai érlelt szatmári szilva, két Rézangyal Barrique szilva és
  a Rézangyal érlelt alma rekordja a név és a címke alapján az
  `érlelt pálinka` fajtával egészült ki.
- A Vilmos Körte ágyon érlelt vegyes gyümölcspálinka teljes neve
  egyszerre igazolja a körte és vegyes gyümölcs ízt, valamint az ágyas
  és érlelt készítési módot. Mindkét mezőt ennek megfelelően
  pontosítottuk.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **7**.
- Változatlanul hagyott rekord: **19** (`BTY-X5869900320021`,
  `BTY-X59202500320022`, `BTY-X6354900320021`,
  `BTY-X7381900320021`, `BTY-X7382100320021`,
  `BTY-X8751300320021`, `BTY-X88415600320022`,
  `BTY-X156700320022`, `BTY-X155700320022`,
  `BTY-X13174400320021`, `BTY-X18180600320021`,
  `cd3ac179873f08080e6753e6`, `28038ff3fb0549a01860a92c`,
  `c638298021c974fe0a0d4a93`, `bb86045616e946c89f27fc79`,
  `f92e27cf275efc258571a009`, `ab4756cdd09449e16b73f61e`,
  `b183c84682d8d6128bd96a37`, `599b29d2227f958eeb9f4bac`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X5585500320021` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |
| `BTY-X6234000320021` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |
| `BTY-X13174300320021` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |
| `BTY-X17395300320021` | íz `körte` → `körte, vegyes gyümölcs`; fajta `gyümölcspálinka` → `ágyas pálinka, érlelt pálinka, gyümölcspálinka` |
| `d3cfccd4d505b649850d0890` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |
| `6ed34f00ffaecaa431ae8ea7` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |

### Pálinka kézi felülvizsgálat, 101–125. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- Az Óbester, Éden, Agárdi, Panyolai, Zwack Kosher, Pannonhalmi
  Pálinkárium, Kulacs és Mátyás termékek márkája, gyümölcse,
  kiszerelése és alkoholtartalma egyezett a teljes névvel,
  forrássorral és címkével.
- Az Alföldünk Aranya három ágyas termékénél, továbbá a Puszta Kincse
  és Rézangyal ágyas termékénél a teljes név közvetlenül igazolta a
  hiányzó `ágyas pálinka` fajtát.
- A Panyolai Elixír érlelt szatmári szilvapálinka rekordja az
  `érlelt pálinka` fajtával egészült ki.
- A Vilmos körte ágyon érlelt vegyes gyümölcspálinka teljes neve
  egyszerre igazolta a körte és vegyes gyümölcs ízt, valamint az ágyas
  és érlelt készítési módot. Mindkét mezőt ennek megfelelően
  pontosítottuk.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **8**.
- Változatlanul hagyott rekord: **18**
  (`36b7f72959b4f1899eb74f85`, `9089b0f63bad6e53dae5fec7`,
  `be53f1f815edcb54ee5f3c8b`, `8dfe8c3e536485f2d7a6a605`,
  `121221568`, `121220949`, `209683699`, `210901225`, `120183545`,
  `121221764`, `121236240`, `120183556`, `105015670`, `105015671`,
  `105027676`, `105027687`, `105027689`, `105027693`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121248393` | fajta `gyümölcspálinka` → `ágyas pálinka, gyümölcspálinka` |
| `209683682` | fajta `gyümölcspálinka` → `érlelt pálinka, gyümölcspálinka` |
| `121221770` | íz `körte` → `körte, vegyes gyümölcs`; fajta `gyümölcspálinka` → `ágyas pálinka, érlelt pálinka, gyümölcspálinka` |
| `121248485` | fajta `gyümölcspálinka` → `ágyas pálinka, gyümölcspálinka` |
| `121248410` | fajta `gyümölcspálinka` → `ágyas pálinka, gyümölcspálinka` |
| `121248462` | fajta `gyümölcspálinka` → `ágyas pálinka, gyümölcspálinka` |
| `220222243` | fajta `gyümölcspálinka` → `ágyas pálinka, gyümölcspálinka` |

### Pálinka kézi felülvizsgálat, 126–131. tétel

- A 6 teljes rekordot és forrássort egyenként, mind a 6 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Grape-Vine Egri Bikavér törkölypálinka, valamint az öt Mátyás
  gyümölcspálinka márkája, gyümölcse, fajtája, kiszerelése és
  alkoholtartalma egyezett a teljes névvel, forrássorral és címkével.
- A `121230407` azonosítójú Grape-Vine rekord a korábbi kézi
  felülvizsgálatban már szerepelt, ezért az előrehaladásban nem
  számoltuk újra; a másik öt rekord új egyedi ellenőrzés.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **6** (`121230407`, `121271001`,
  `121271018`, `121271030`, `121271047`, `121271082`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A köteg után lefutott a 47 030 rekordos teljes validáció; eltérés
  nem maradt.

### Whisky és bourbon kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük; 23
  termékhez volt helyi kép, ezeket közvetlenül, részletes felbontásban
  is megvizsgáltuk. A `4606403` és `4599886` rekordhoz nem volt helyi
  kép, ezért ezeknél kizárólag a teljes név és a forrássor bizonyítható
  adatait tartottuk meg.
- A helyi címkék alapján a Johnnie Walker Red Label, Hankey Bannister
  Original és Chivas Regal 12 termékek típusa pontosabban
  `kevert skót whisky`.
- A Jack Daniel's Old No. 7 helyi címkéje közvetlenül 40%-ot mutatott.
  A Ballantine's Finest 0,2 l az azonos címkéjű, más kiszerelésű
  termékekkel és a gyártói termékadattal egyezően 40%-os.
- A Hankey Bannister 1 l helyi címkéje 40%-ot és `blended Scotch
  whisky` típust igazolt.
- Az Isle of Skye 8 éves címkéje és gyártói termékadata egyaránt
  kevert whiskyt és 40%-os alkoholtartalmat igazolt.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **10**.
- Változatlanul hagyott rekord: **17** (`4606403`, `533759`,
  `4599886`, `59301:59640`, `712832:4250222`, `684446:4221836`,
  `674573:4211963`, `684413:4221803`, `684425:4221815`,
  `712829:4250219`, `684716:4222106`, `683792:4221182`,
  `712865:4250255`, `684419:4221809`, `684701:4222091`,
  `684428:4221818`, `685175:4222565`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `4603342` | alkoholtartalom `ismeretlen` → `40%` |
| `684440:4221830` | alkoholtartalom `ismeretlen` → `40%` |
| `760782:4298172` | típus `skót whisky` → `kevert skót whisky` |
| `713075:4250465` | típus `skót whisky` → `kevert skót whisky` |
| `674966:4212356` | típus `skót whisky` → `kevert skót whisky` |
| `693164:4230554` | alkoholtartalom `ismeretlen` → `40%`; típus `skót whisky` → `kevert skót whisky` |
| `684452:4221842` | típus `skót whisky` → `kevert skót whisky` |
| `712370:4249760` | alkoholtartalom `ismeretlen` → `40%`; típus `skót whisky` → `kevert skót whisky` |

### Whisky és bourbon kézi felülvizsgálat, 26–50. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük; 24
  termékhez volt helyi kép, ezeket közvetlenül, részletes felbontásban
  is megvizsgáltuk. A `3376041` rekordhoz nem volt helyi kép; ennél az
  azonos Johnnie Walker Red Label termék más kiszereléseivel egyező,
  bizonyított típust alkalmaztuk.
- Az Arran Barrel Reserve címkéje közvetlenül `Single Malt Scotch
  Whisky` megjelölést tartalmazott, ezért a típus
  `single malt skót whisky` lett.
- A Johnnie Walker Red, Black és Gold Label, a Chivas Regal 12 és 18,
  a Hunting Lodge, valamint a Grant's címkéje kevert skót whiskyt
  igazolt.
- A Jameson 1 l helyi címkéje és az azonos Jameson termék más
  kiszerelései 40%-ot igazoltak. A Ballantine's Finest 1,5 l címkéje
  és gyártói termékadata szintén 40%-ot igazolt.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **14** (`683795:4221185`,
  `712862:4250252`, `712352:4249742`, `14458:14461`,
  `684719:4222109`, `627037:4164427`, `771303:4308693`,
  `444475:3981859`, `712835:4250225`, `443698:3981082`,
  `764442:4301832`, `684710:4222100`, `674975:4212365`,
  `712871:4250261`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `674969:4212359` | típus `skót whisky` → `kevert skót whisky` |
| `712364:4249754` | típus `skót whisky` → `single malt skót whisky` |
| `685178:4222568` | típus `skót whisky` → `kevert skót whisky` |
| `684416:4221806` | alkoholtartalom `ismeretlen` → `40%` |
| `674972:4212362` | típus `skót whisky` → `kevert skót whisky` |
| `440113:3977497` | alkoholtartalom `ismeretlen` → `40%` |
| `674579:4211969` | típus `skót whisky` → `kevert skót whisky` |
| `54504:54843` | típus `skót whisky` → `kevert skót whisky` |
| `797552:4334942` | típus `skót whisky` → `kevert skót whisky` |
| `684713:4222103` | típus `skót whisky` → `kevert skót whisky` |
| `3376041` | típus `skót whisky` → `kevert skót whisky` |

### Whisky és bourbon kézi felülvizsgálat, 51–75. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük; 23
  termékhez volt helyi kép, ezeket közvetlenül, részletes felbontásban
  is megvizsgáltuk. A `3376036` és `2807815` rekordhoz nem volt helyi
  kép; teljes nevük és forrássoruk minden meglévő mezőt igazolt.
- A Lidl négy rekordjánál a forrás `unit_step` mezője 500 vagy 700
  ml-t adott, miközben a két kiszerelésmező `ismeretlen` volt. Ezeket
  a közvetlen forrásadat alapján pótoltuk.
- A Grant's, Teeling Small Batch, Chivas Regal 12, Queen Margot 3 éves
  és Jack Daniel's helyi címkéje, azonos termékváltozata és gyártói
  adata igazolta a hiányzó alkoholfokot. A Queen Margot 3 évesnél a
  Lidl termékadata külön is 700 ml-t, 40%-ot és kevert skót típust
  igazolt.
- A Chivas Regal, Ballantine's, Johnnie Walker Red és Black Label,
  The Famous Grouse, Grant's, valamint Queen Margot címkéje
  `kevert skót whisky` típust igazolt.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **25**.
- Változatlanul hagyott rekord: **13** (`3376036`, `3040622`,
  `2817551`, `2808664`, `2807815`, `BTY-X17639100320021`,
  `BTY-X17504100320021`, `BTY-X17593700320021`,
  `BTY-X17486800320021`, `BTY-X17397300320021`,
  `BTY-X17593900320021`, `BTY-X17637700320021`,
  `BTY-X17589200320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `2813848` | típus `skót whisky` → `kevert skót whisky` |
| `2813743` | típus `skót whisky` → `kevert skót whisky` |
| `10035104` | kiszerelés `ismeretlen` → `500 ml`; alkoholtartalom `ismeretlen` → `40%`; típus `skót whisky` → `kevert skót whisky`; egységnyi kiszerelés `ismeretlen` → `500 ml` |
| `10038378` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `46%`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10041711` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `40%`; típus `skót whisky` → `kevert skót whisky`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10107631` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `40%`; típus `skót whisky` → `kevert skót whisky`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10107953` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `40%`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `BTY-X17402500320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17402400320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17403000320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17487600320021` | típus `kevert whisky` → `kevert skót whisky` |
| `BTY-X17561900320021` | típus `skót whisky` → `kevert skót whisky` |

### Whisky és bourbon kézi felülvizsgálat, 76–100. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Nikka Days teljes neve és díszdoboza japán `Blended Whisky`
  megjelölést tartalmazott, ezért a típusa `kevert japán whisky` lett.
- A Ballantine's 1,5 l és 17 éves, a Chivas Regal 12 éves, valamint a
  Johnnie Walker Red és Gold Label címkéje és teljes neve kevert skót
  whiskyt igazolt.
- A Jameson, Jim Beam, Maker's Mark, Glen Broch, O'LIAM, Jack Daniel's,
  Woodford Reserve, Tamnavulin, The Irishman, Talisker és The Singleton
  rekordok minden tulajdonsága egyezett a névvel, forrássorral és
  címkével.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **6**.
- Változatlanul hagyott rekord: **19**
  (`BTY-X17590500320021`, `BTY-X17590800320021`,
  `BTY-X17628600320021`, `BTY-X17639000320021`,
  `BTY-X18938800320021`, `BTY-X91714700320022`,
  `BTY-X9603100320021`, `BTY-X10454200320021`,
  `BTY-X18485200320021`, `BTY-X18485300320021`,
  `BTY-X17486500320021`, `BTY-X16629300320021`,
  `BTY-X63256900320021`, `BTY-X15974400320021`,
  `BTY-X16168300320021`, `BTY-X16659100320021`,
  `BTY-X17261500320021`, `BTY-X17400000320021`,
  `BTY-X17400200320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17621600320021` | típus `japán whisky` → `kevert japán whisky` |
| `BTY-X27693400320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17589700320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17402600320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X16168100320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17400500320021` | típus `skót whisky` → `kevert skót whisky` |

### Whisky és bourbon kézi felülvizsgálat, 101–125. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Johnnie Walker Black és Red Label, Famous Grouse Smoky Black,
  Naked Grouse, Chivas Regal, Hankey Bannister és Ballantine's
  címkéje kevert skót whiskyt igazolt.
- A FUYU és Hatozaki teljes neve és címkéje egyaránt `Blended Japán
  Whisky` megjelölést tartalmazott, ezért típusuk
  `kevert japán whisky` lett.
- A Jameson Caskmates IPA neve és közvetlen címkéje az IPA-hordós
  finist egyértelműen azonosította. A whisky `íz` értékei közé ezért
  felvettük az atomikus `IPA` értéket, és a rekord `natúr` ízét erre
  pontosítottuk.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **14**
  (`BTY-X17400700320021`, `BTY-X17503700320021`,
  `BTY-X17555400320021`, `BTY-X17561800320021`,
  `BTY-X17562100320021`, `BTY-X17562200320021`,
  `BTY-X17590100320021`, `BTY-X17590200320021`,
  `BTY-X17621300320021`, `BTY-X17638900320021`,
  `BTY-X17641500320021`, `BTY-X17670000320021`,
  `BTY-X17697100320021`, `BTY-X17765900320021`).
- Új megengedett érték: **1** (`íz: IPA`).
- Törölt megengedett érték: **0**.
- Az új faérték felvétele után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17402900320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17487200320021` | típus `kevert whisky` → `kevert skót whisky` |
| `BTY-X17487300320021` | típus `egyéb whisky` → `kevert skót whisky` |
| `BTY-X17589800320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17590700320021` | íz `natúr` → `IPA` |
| `BTY-X17621200320021` | típus `egyéb whisky` → `kevert skót whisky` |
| `BTY-X17628500320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17636200320021` | típus `japán whisky` → `kevert japán whisky` |
| `BTY-X17642000320021` | típus `japán whisky` → `kevert japán whisky` |
| `BTY-X17775500320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17831400320021` | típus `skót whisky` → `kevert skót whisky` |

### Whisky és bourbon kézi felülvizsgálat, 126–150. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Johnnie Walker, Chivas Regal, Ballantine's és Golden Shoe
  címkéje kevert skót whiskyt, a Tottori címkéje kevert japán
  whiskyt igazolt.
- A Joe Rebel címkéjén szereplő `Master Blend` megjelölés alapján a
  korábbi `egyéb whisky` típust `kevert whisky` értékre pontosítottuk.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **9**.
- Változatlanul hagyott rekord: **16**
  (`BTY-X17834200320021`, `BTY-X17835800320021`,
  `BTY-X17894500320021`, `BTY-X18410100320021`,
  `BTY-X18590400320021`, `BTY-X18709200320021`,
  `BTY-X18709300320021`, `BTY-X63252000320021`,
  `BTY-X75303200320022`, `BTY-X16978900320021`,
  `BTY-X17894400320021`, `BTY-X18308300320021`,
  `BTY-X8146200320021`, `BTY-X18490100320021`, `1006039`,
  `1019822`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18050700320021` | típus `japán whisky` → `kevert japán whisky` |
| `BTY-X18543800320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X18965300320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X59228400320022` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X17400100320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X1999000320021` | típus `skót whisky` → `kevert skót whisky` |
| `BTY-X66567900320022` | típus `skót whisky` → `kevert skót whisky` |
| `1056782` | típus `egyéb whisky` → `kevert whisky` |
| `998982` | típus `skót whisky` → `kevert skót whisky` |

### Whisky és bourbon kézi felülvizsgálat, 151–175. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Johnnie Walker Red Label, a két Chivas Regal és a Hankey
  Bannister címkéje kevert skót whiskyt, a Hatozaki címkéje kevert
  japán whiskyt, a Joe Black címkéje kevert whiskyt igazolt.
- A Connemara közvetlen dobozfelirata szó szerint `Peated Single
  Malt Irish Whiskey`. A típust ezért `single malt ír whisky`
  értékre, az ízt pedig `füstös` értékre pontosítottuk.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **8**.
- Változatlanul hagyott rekord: **18**
  (`1006047`, `c8421612d8060ad7dc029730`,
  `3b36614a8597d87ec26f0d01`, `26ba2c4db1565c54f66415c0`,
  `f95c25ac093841482df92de4`, `76383eabcf9f38509ed14f4f`,
  `bdb20ad96392696692317d86`, `a0742b1044ab1dcb34e1256e`,
  `11345c66b86171513d562bd6`, `cdc20b6b29e01eb7110fb2e7`,
  `3e4b7e7b1471adef0b2e7482`, `a8e7efb7643dfa4a0ac9c3a5`,
  `bfa75cb1ad49466fe85b9591`, `878d7ddd6308ebc6832d8213`,
  `b22743d83d5827188d8d47cd`, `e84ae88064f3e5e25e89cc18`,
  `1a85069ceaa0dcc1f6843596`, `04c093314e864389e54d7f73`).
- Új megengedett érték: **1** (`típus: single malt ír whisky`).
- Törölt megengedett érték: **0**.
- Az új faérték felvétele után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `83ba388daf0df37afa6a27ff` | típus `skót whisky` → `kevert skót whisky` |
| `46e79df6aa06c035b3ef52bd` | típus `skót whisky` → `kevert skót whisky` |
| `cde5ad42f01bd367cb717376` | típus `skót whisky` → `kevert skót whisky` |
| `fe78c38f4fe5f3fcc8d7e06b` | típus `ír whisky` → `single malt ír whisky`; íz `natúr` → `füstös` |
| `98c836cea537606db465d5c2` | típus `skót whisky` → `kevert skót whisky` |
| `423a3f005e803cfeb6347a29` | típus `japán whisky` → `kevert japán whisky` |
| `e7d3c896f7392096e3362cd4` | típus `egyéb whisky` → `kevert whisky` |

### Whisky és bourbon kézi felülvizsgálat, 176–200. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Chivas Regal és Johnnie Walker címkéi kevert skót whiskyt, a
  Nikka Days doboza kevert japán whiskyt igazolt.
- A két Black Velvet palackcímkéjén a `Blended Canadian Whisky`
  megjelölés közvetlenül olvasható, ezért típusuk
  `kevert kanadai whisky` lett.
- Módosított rekord: **11**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **14**
  (`b76131fc5052f609f5b3807c`, `c5bf99298cc910b700dfc7c4`,
  `635905caffd3a6f3574cb432`, `7749d3333308f2dce2540b60`,
  `097db342a11020d1eb682a3e`, `5d10f4f8ed3d391d0dbc9435`,
  `121237481`, `121218383`, `121227619`, `121228814`,
  `121218446`, `121228739`, `121220517`, `121228722`).
- Új megengedett érték: **1** (`típus: kevert kanadai whisky`).
- Törölt megengedett érték: **0**.
- Az új faérték felvétele után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1f7297392f815c990afdd4e2` | típus `skót whisky` → `kevert skót whisky` |
| `18c80b4c38ed0c4b595f0786` | típus `kanadai whisky` → `kevert kanadai whisky` |
| `4cf40af0fe93b17fffc22ce5` | típus `skót whisky` → `kevert skót whisky` |
| `be3c8f859c753d5a6c2e9f65` | típus `skót whisky` → `kevert skót whisky` |
| `2e95e9abf22960bdafb19732` | típus `japán whisky` → `kevert japán whisky` |
| `121220834` | típus `skót whisky` → `kevert skót whisky` |
| `121277922` | típus `skót whisky` → `kevert skót whisky` |
| `121220857` | típus `kanadai whisky` → `kevert kanadai whisky` |
| `121228745` | típus `skót whisky` → `kevert skót whisky` |
| `121221194` | típus `skót whisky` → `kevert skót whisky` |
| `121221712` | típus `skót whisky` → `kevert skót whisky` |

### Whisky és bourbon kézi felülvizsgálat, 201–224. tétel

- A 24 teljes rekordot és forrássort egyenként ellenőriztük.
  Mind a 24 helyi képfájlt közvetlenül megvizsgáltuk; a Maker's Mark
  képe csak `image unavailable` helyőrzőt tartalmazott, a másik 23
  kép érdemi termékábrát adott.
- A Johnnie Walker Gold és Red Label kevert skót, a Nikka Days
  kevert japán, a Laphroaig, Arran és Glen Turner single malt skót
  típusát a címke, a teljes név és a gyártói termékadat igazolta.
- A Joe Rebel az előző kötegben ellenőrzött, azonos nevű és
  kiszerelésű `Master Blend` termék újabb rekordja.
- A Laphroaig Oak Select és a Scarabus gyártói leírása is közvetlenül
  füstös, tőzegfüstös karaktert közöl, ezért ízüket `füstös`
  értékre pontosítottuk.
- A 350 ml-es Tesco Special Reserve az ellenőrzött 700 és 1000 ml-es
  változatokkal azonos, 3 éves, 40%-os kevert skót whisky; a hiányzó
  alkoholtartalmat pótoltuk.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **10**.
- Változatlanul hagyott rekord: **15**
  (`121228250`, `121218585`, `121220742`, `121228837`,
  `121228808`, `121248312`, `121270935`, `121257641`,
  `121257664`, `121220552`, `120255719`, `121220794`,
  `121228855`, `121248335`, `121273569`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.
- A Whisky és bourbon levél mind a **224 / 224** aktuális rekordjának
  kézi felülvizsgálata befejeződött.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121221188` | típus `skót whisky` → `kevert skót whisky` |
| `121221211` | típus `skót whisky` → `kevert skót whisky` |
| `121248341` | típus `japán whisky` → `kevert japán whisky` |
| `121228095` | típus `egyéb whisky` → `single malt skót whisky`; íz `natúr` → `füstös` |
| `121248306` | típus `skót whisky` → `single malt skót whisky` |
| `121255672` | típus `egyéb whisky` → `kevert whisky` |
| `121255712` | típus `skót whisky` → `single malt skót whisky` |
| `121255758` | íz `natúr` → `füstös` |
| `121257670` | alkoholtartalom `ismeretlen` → `40%` |

### Vodka kézi felülvizsgálat, 1–25. tétel

- A 25 teljes rekordot és forrássort egyenként, mind a 25 helyi
  termékképet közvetlenül, részletes felbontásban ellenőriztük.
- A Spacerowa Czysta pontos, 0,7 literes termékváltozata 37,5%-os,
  ezért a hiányzó alkoholtartalmat pótoltuk.
- A Várda Sósborszesz közvetlen címkéje és pontos termékadata
  ízesített vodkát igazol, de a konkrét ízt nem nevezi meg; a téves
  `natúr` helyett `ismeretlen` értéket kapott.
- A Nicolaus Extra Fine képe natúr vodkát és poharas díszcsomagot
  mutat; a `kóla` ízt sem a név, sem a címke, sem a forrásadat nem
  igazolta.
- Módosított rekord: **3**.
- Módosított tulajdonságmező: **3**.
- Változatlanul hagyott rekord: **22**
  (`4596780`, `533764`, `444472:3981856`, `693101:4230491`,
  `682532:4219922`, `674567:4211957`, `37030:37033`,
  `684386:4221776`, `684737:4222127`, `684743:4222133`,
  `684746:4222136`, `674564:4211954`, `751938:4289328`,
  `693104:4230494`, `684758:4222148`, `684749:4222139`,
  `693107:4230497`, `712940:4250330`, `712919:4250309`,
  `674561:4211951`, `684389:4221779`, `684767:4222157`).
- Új megengedett érték: **1** (`íz: ismeretlen`).
- Törölt megengedett érték: **0**.
- Az új faérték felvétele után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1056405` | alkoholtartalom `ismeretlen` → `37,5%` |
| `444640:3982024` | íz `natúr` → `ismeretlen` |
| `754923:4292313` | íz `kóla, natúr` → `natúr` |

### Vodka kézi felülvizsgálat, 26–50. tétel

- A 25 teljes rekordot és forrássort egyenként ellenőriztük. A 21
  elérhető helyi termékképet közvetlenül, részletes felbontásban
  megvizsgáltuk; négy Coop-rekordhoz nem tartozott helyi kép.
- A Wyborowa palackcímkéje közvetlenül 40%-os alkoholtartalmat mutat.
- A Żubrówka Bison Grass neve és címkéje a natúr íz helyett a már
  deklarált `bölényfű` értéket igazolja.
- A Tattoo Company gyártói termékoldala a Criminal Vodka pontos
  0,7 literes változatát 40%-osként adja meg.
- A rövid nevű Lidl Finlandia rekord teljes forrássora 700 ml-es
  mennyiséget közöl, helyi képe pedig az ellenőrzött natúr Finlandia
  palackot mutatja; a hiányzó kiszerelést, egységnyi kiszerelést és
  40%-os alkoholtartalmat pótoltuk.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **6**.
- Változatlanul hagyott rekord: **21**
  (`684764:4222154`, `674558:4211948`, `693110:4230500`,
  `693113:4230503`, `712943:4250333`, `712922:4250312`,
  `684752:4222142`, `747332:4284722`, `712931:4250321`,
  `693116:4230506`, `751947:4289337`, `3380293`, `3375666`,
  `3352074`, `2807817`, `BTY-X16657100320021`,
  `BTY-X17772900320021`, `BTY-X17488500320021`,
  `BTY-X18339800320021`, `BTY-X7921800320021`,
  `BTY-X17591300320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `751941:4289331` | alkoholtartalom `ismeretlen` → `40%` |
| `684770:4222160` | íz `natúr` → `bölényfű` |
| `714125:4251515` | alkoholtartalom `ismeretlen` → `40%` |
| `10107433` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `40%`; egységnyi kiszerelés `ismeretlen` → `700 ml` |

### Vodka kézi felülvizsgálat, 51–75. tétel

- Mind a 25 teljes rekordot és forrássort, továbbá mind a 25 helyi
  termékképet egyenként, közvetlenül és részletes felbontásban
  ellenőriztük.
- A natúr vodkák és az ízesített Finlandia, Ciroc és Absolut
  változatok íze, alkoholtartalma, márkája és kiszerelése minden
  esetben egyezett a névvel, a forrásadattal és a címkével.
- A Koronás 24 × 40 ml-es gyűjtőcsomag 960 ml-es teljes
  kiszerelése és 40 ml-es egységnyi kiszerelése is helyes.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **25**
  (`BTY-X17655100320021`, `BTY-X16651200320021`,
  `BTY-X17282400320021`, `BTY-X17395400320021`,
  `BTY-X17399800320021`, `BTY-X17402800320021`,
  `BTY-X17488200320021`, `BTY-X17489300320021`,
  `BTY-X17503600320021`, `BTY-X17561000320021`,
  `BTY-X17573000320021`, `BTY-X18220200320021`,
  `BTY-X18339600320021`, `BTY-X18339700320021`,
  `BTY-X18339900320021`, `BTY-X18414600320021`,
  `BTY-X7070100320021`, `BTY-X17395500320021`,
  `BTY-X17561500320021`, `BTY-X17572700320021`,
  `BTY-X17638300320021`, `BTY-X17488400320021`,
  `BTY-X17488700320021`, `BTY-X17561200320021`,
  `BTY-X17396000320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentesen lefutott.

### Vodka kézi felülvizsgálat, 76–100. tétel

- Mind a 25 teljes rekordot és forrássort, valamint mind a 25
  elérhető helyi termékképet egyenként, közvetlenül és részletes
  felbontásban ellenőriztük.
- A Royal 35 ml-ként rövidített nevével szemben a forrásrekord
  `unit_step` és végső mennyiség mezője egyaránt 350 ml-t közöl, a
  palackcímke pedig 0,35 litert mutat; ezért mindkét
  kiszerelésmezőt 350 ml-re javítottuk.
- A NEFT forrásrekordja és neve 700 ml-es terméket ír le. A hozzá
  társított kép más piaci, 750 ml-es stockfotó, ezért az ellenőrzött
  rekord mennyiségét nem írtuk felül a képpel.
- A Żubrówka Bison Grass két rekordja már helyesen `bölényfű`, a
  Biała változatok helyesen `natúr` ízzel szerepeltek.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **2**.
- Változatlanul hagyott rekord: **24**
  (`BTY-X16651500320021`, `BTY-X16714200320021`,
  `BTY-X16979000320021`, `BTY-X17010900320021`,
  `BTY-X17192200320021`, `BTY-X17395900320021`,
  `BTY-X17397400320021`, `BTY-X17488900320021`,
  `BTY-X17503300320021`, `BTY-X17503400320021`,
  `BTY-X17561100320021`, `BTY-X17561300320021`,
  `BTY-X17561400320021`, `BTY-X17561700320021`,
  `BTY-X17566700320021`, `BTY-X17572900320021`,
  `BTY-X17581800320021`, `BTY-X17640400320021`,
  `BTY-X17643100320021`, `BTY-X17647500320021`,
  `BTY-X17696500320021`, `BTY-X17823200320021`,
  `BTY-X17846200320021`, `BTY-X18071800320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17560800320021` | kiszerelés `35 ml` → `350 ml`; egységnyi kiszerelés `35 ml` → `350 ml` |

### Vodka kézi felülvizsgálat, 101–125. tétel

- Mind a 25 teljes rekordot és forrássort egyenként ellenőriztük.
  Huszonnégy helyi termékképet közvetlenül, részletes felbontásban
  megvizsgáltunk; a 90 ml-es Royal rekordhoz nem tartozott kép.
- A Royal `20 ml` névhibájával szemben a forrásrekord 200 ml-es
  `unit_step` és végső mennyiség mezője igazolja a 200 ml-es
  kiszerelést, ezért mindkét kiszerelésmezőt javítottuk.
- A kép nélküli Royal rekord neve, `unit_step` és végső mennyisége
  egyaránt 90 ml, ezért azt bizonyíték nélkül nem változtattuk meg.
- A Nicolaus Extra Fine neve és címkéje natúr vodkát igazol; a
  korábbi `kóla` íznek nem volt termékoldali alapja.
- Módosított rekord: **2**.
- Módosított tulajdonságmező: **3**.
- Változatlanul hagyott rekord: **23**
  (`BTY-X18149800320021`, `BTY-X18291900320021`,
  `BTY-X17646700320021`, `BTY-X18506100320021`, `1021730`,
  `999980`, `1012104`, `1012103`, `1012105`, `1012100`,
  `1004359`, `1021726`, `b99245ffb43d08464d959c5e`,
  `c4d0316f288667e33b4c1a7f`, `bf221f1f81dbeed0ab61c6d4`,
  `c69ac267eaf2529fb82759ca`, `482c906153fa0b485f81e508`,
  `122a82418704003b0ccfeb84`, `392b89221993723bf05677a1`,
  `f64671f67884f61d322ca6f7`, `93824340aa7be3721b484ed1`,
  `eb8126359d76d1482cfa97f5`, `079f17ad3e35c82db2031671`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X9529900320021` | kiszerelés `20 ml` → `200 ml`; egységnyi kiszerelés `20 ml` → `200 ml` |
| `1048626` | íz `kóla, natúr` → `natúr` |

### Vodka kézi felülvizsgálat, 126–150. tétel

- Mind a 25 teljes rekordot és forrássort, valamint mind a 25 helyi
  termékképet egyenként, közvetlenül és részletes felbontásban
  ellenőriztük.
- A Kaiser Herbal pontos neve gyógynövényes változatot igazol, ezért
  a téves `natúr` ízt az új, elemi `gyógynövény` értékre
  pontosítottuk.
- Az előző két kötegben igazolt 200 és 350 ml-es Royal-javítás után a
  `20 ml` és `35 ml` értéket már egyetlen Vodka-rekord sem használta.
  A hibás maradványértékeket a teljes és az egységnyi kiszerelés
  listájából is töröltük.
- A Żubrówka Bison Grass rekordok helyesen `bölényfű`, a Biała
  rekordok helyesen `natúr` ízzel szerepeltek.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **24**
  (`1a36348db643e3e6f95f673b`, `d9165b2446f8eb3ba9593eab`,
  `df9e56e3160513b3dd906c58`, `8e517285704b23d7ff1f31f7`,
  `6b5399b547ad0a214c9567fa`, `30ff9cdcaac8cab5923d3cfd`,
  `d9fd30243876104f7a849222`, `25e7b5e328cf9d29412ac01a`,
  `f440901cb7566784c8b4c5a2`, `b6c739c71ca28ce8ba4ae8d0`,
  `4a14bfde1c6e884f84075320`, `4c8819c567fd666494d055b0`,
  `1b34e0e4fa628de3bb0360dd`, `64c3d5e6a1f61d4bbe42301f`,
  `cf8d15d49de9a05d8309623c`, `68a4aa6da2fb57a8f34d7088`,
  `1346163d0acc8034c7555a54`, `41587e0bd56c05f5e8e8c6d1`,
  `58204035201b88642e71a155`, `5c7705c725e38010c6c6989c`,
  `117577fcf355a81471c208d5`, `6bd0ac3f050a94c12293852d`,
  `9acfa1b369729e0f95862df5`, `e24cf4e777d237d7d3163cd5`).
- Új megengedett érték: **1** (`íz: gyógynövény`).
- Törölt megengedett érték: **4** (`kiszerelés: 20 ml, 35 ml`;
  `egységnyi kiszerelés: 20 ml, 35 ml`).
- A fa módosítása után, a rekordcsere után és a végén is lefutott a
  47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `8910e3b15a125437d4446c52` | íz `natúr` → `gyógynövény` |

### Vodka kézi felülvizsgálat, 151–175. tétel

- Mind a 25 teljes rekordot és forrássort, valamint mind a 25 helyi
  termékképet egyenként, közvetlenül és részletes felbontásban
  ellenőriztük.
- A Nicolaus Extra Fine neve és címkéje natúr vodkát igazol; a
  rekordba került `kóla` íznek nem volt termékoldali alapja.
- A Ciroc Red Berry `vörös bogyós gyümölcs`, a Finlandia Redberry
  pedig `áfonya` ízzel helyesen szerepelt.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **24**
  (`b1b4dc4f680595ea3c370000`, `525cb9ad7a977913356ba5a7`,
  `2447de6b54cb60ca36da1794`, `86f818cb56a5f0be0d2c7148`,
  `121236205`, `121218400`, `121221384`, `121220811`, `121220581`,
  `121273984`, `121236228`, `121228912`, `121218567`, `121220621`,
  `121256106`, `121256055`, `121221931`, `121228964`, `220335911`,
  `121256135`, `121273961`, `121219013`, `121264425`, `121302058`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121231124` | íz `kóla, natúr` → `natúr` |

### Vodka kézi felülvizsgálat, 176–185. tétel

- Mind a 10 teljes rekordot és forrássort, valamint mind a 10 helyi
  termékképet egyenként, közvetlenül és részletes felbontásban
  ellenőriztük.
- A natúr és ízesített változatok márkája, kiszerelése,
  alkoholtartalma és íze minden esetben megfelelt a névnek,
  forrásadatnak és címkének.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **10**
  (`121309270`, `121309287`, `121319575`, `121321732`, `121324769`,
  `121337909`, `121345393`, `121345404`, `121352355`, `121356161`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció lefutott; eltérés nem maradt.

### Likőr kézi felülvizsgálat, 1–25. tétel

- Mind a 25 teljes rekordot és forrássort, valamint mind a 25 helyi
  termékképet egyenként, közvetlenül és részletes felbontásban
  ellenőriztük.
- A gyártói termékleírás az Unicum Orange Bitter 34,5%-os
  alkoholtartalmát igazolta.
- Az eredeti Unicum, Jägermeister és Tatratea kisüveges rekordjaiba
  öröklött `narancs` ízt a címke szerinti `gyógynövény`, illetve
  `tea` értékre javítottuk. Az eredeti St. Hubertus-változatokból
  eltávolítottuk a téves másodlagos `narancs` értéket.
- A márkajelzés nélküli, generikus „Mini szeszek” terméknél a
  `Mini` ál-márkát `márka nélkül` értékre javítottuk.
- A St. Almtaler és a 40 ml-es Szent Márk alkoholfokára egymásnak
  ellentmondó külső adatok voltak, a helyi képen pedig nem volt
  egyértelműen olvasható érték; ezért az `ismeretlen` értéket
  bizonyíték nélkül nem írtuk át.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **9**.
- Változatlanul hagyott rekord: **16**
  (`533777`, `533765`, `533779`, `997440`, `1005709`, `4606124`,
  `998432`, `683771:4221161`, `683768:4221158`, `712847:4250237`,
  `712856:4250246`, `712859:4250249`, `683789:4221179`,
  `683783:4221173`, `712838:4250228`, `712841:4250231`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1057405` | alkoholtartalom `ismeretlen` → `34,5%` |
| `1014576` | márka `Mini` → `márka nélkül` |
| `73165:3610253` | íz `narancs` → `gyógynövény` |
| `67421:3604502` | íz `gyógynövény, narancs` → `gyógynövény` |
| `444562:3981946` | íz `narancs` → `gyógynövény` |
| `463915:4001305` | íz `narancs` → `gyógynövény` |
| `144925:3682171` | íz `narancs` → `gyógynövény` |
| `627049:4164439` | íz `narancs` → `tea` |
| `675107:4212497` | íz `gyógynövény, narancs` → `gyógynövény` |

### Likőr kézi felülvizsgálat, 26–50. tétel

- Mind a 25 teljes rekordot és forrássort egyenként ellenőriztük.
  Huszonnégy helyi termékképet közvetlenül és részletes felbontásban
  megvizsgáltunk; a Mátyás Classic rekordhoz nem tartozott helyi kép.
- Az eredeti Unicum-, Jägermeister-, St. Hubertus-, Becherovka- és
  Szent Márk-változatok téves `narancs` értékeit a termékazonosság
  szerinti `gyógynövény` értékre javítottuk.
- A kép nélküli Mátyás Classic terméknél a pontos kereskedői leírás
  reneszánsz fűszereket és keserédes botanikus profilt igazolt; konkrét
  narancsízesítést nem, ezért az ízt `gyógynövény` értékre javítottuk.
- A St. Hubertus Erdei pontos termékleírása erdei bogyókat és
  gyógynövényeket igazolt, ezért az örökölt `narancs` helyett
  `erdei gyümölcs, gyógynövény` értéket kapott.
- A Bottega gyártói terméklapjai a Fior di Latte és Nero 15%-os, a
  Gianduia és Pistacchio 17%-os alkoholtartalmát igazolták. A Gianduia
  valódi mogyoróízét elkülönítettük a földimogyorótól; a Fior di Latte
  címkéjén szereplő fehér csokoládét is rögzítettük.
- A Szent Márk Szilva pontos termékadata 24%-os alkoholtartalmat, az
  Opyyum Orange közvetlen címkéje 30%-ot igazolt.
- Módosított rekord: **18**.
- Módosított tulajdonságmező: **20**.
- Változatlanul hagyott rekord: **7**
  (`827432:4364822`, `658836:4196226`, `860348:4397738`,
  `35713:35716`, `3175:3175`, `678974:4216364`, `35719:35722`).
- Új megengedett érték: **1** (`íz: mogyoró`).
- Törölt megengedett érték: **0**.
- A fa módosítása után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `675011:4212401` | íz `narancs` → `gyógynövény` |
| `674654:4212044` | íz `gyógynövény, narancs` → `gyógynövény` |
| `712322:4249712` | íz `narancs` → `gyógynövény` |
| `674903:4212293` | íz `gyógynövény, narancs` → `gyógynövény` |
| `674900:4212290` | íz `gyógynövény, narancs` → `erdei gyümölcs, gyógynövény` |
| `674909:4212299` | íz `gyógynövény, narancs` → `gyógynövény` |
| `764466:4301856` | íz `gyógynövény, narancs` → `gyógynövény` |
| `775293:4312683` | alkoholtartalom `ismeretlen` → `24%` |
| `693143:4230533` | íz `gyógynövény, narancs` → `gyógynövény` |
| `775296:4312686` | íz `narancs` → `gyógynövény` |
| `674906:4212296` | íz `narancs` → `gyógynövény` |
| `693149:4230539` | íz `gyógynövény, narancs` → `gyógynövény` |
| `674651:4212041` | íz `gyógynövény, narancs` → `gyógynövény` |
| `660540:4197930` | alkoholtartalom `ismeretlen` → `15%`; íz `tejszín` → `csokoládé, tejszín` |
| `660543:4197933` | alkoholtartalom `ismeretlen` → `17%`; íz `csokoládé, földimogyoró` → `csokoládé, mogyoró` |
| `979544:4516934` | alkoholtartalom `ismeretlen` → `15%` |
| `631439:4168829` | alkoholtartalom `ismeretlen` → `17%` |
| `954254:4491644` | alkoholtartalom `ismeretlen` → `30%` |

### Likőr kézi felülvizsgálat, 51–75. tétel

- Mind a 25 teljes rekordot és forrássort, valamint mind a 25 helyi
  termékképet egyenként, közvetlenül és részletes felbontásban
  ellenőriztük.
- Az Opyyum Cream Poppy Seed pontos, 0,75 literes krémváltozatának
  termékadata 17%-os alkoholtartalmat igazolt.
- A Cannabis Spirit Classic48 neve és közvetlen címkéje kannabisz–tea
  likőrt igazolt; ezért a gyűjtő `gyógynövény` ízt a pontosabb
  `kannabisz` értékre cseréltük, a `tea` érték megtartásával.
- Az eredeti Unicum és Unicum Riserva téves `natúr` ízét
  `gyógynövény` értékre javítottuk.
- A két Sütő likőr pontos termékadata és címkéje rum ízesítést igazolt,
  ezért az íz `natúr` → `rum` lett. A fajtát nem módosítottuk
  `rumalapú likőr` értékre, mert a bizonyíték rumos ízesítést, nem
  rumalapot igazolt.
- A Rézangyal teljes neve a meggy mellett mézes ágyazást is közöl,
  ezért az ízhez a `méz` értéket is felvettük.
- Hat Auchan Kedvenc krémlikőr közvetlen címkéjén olvasható 15%-os
  alkoholtartalmat rögzítettük. A mogyoró–csokoládé változatnál a
  téves `földimogyoró` értéket `mogyoró` értékre javítottuk.
- A csokoládés Auchan Kedvenc alkoholfoka a helyi képen és a pontos
  termékoldalon sem volt egyértelműen olvasható; az azonos család
  alapján nem következtettünk, ezért az `ismeretlen` érték megmaradt.
- Módosított rekord: **13**.
- Módosított tulajdonságmező: **14**.
- Változatlanul hagyott rekord: **12**
  (`681977:4219367`, `681998:4219388`, `693152:4230542`,
  `685097:4222487`, `682001:4219391`, `681995:4219385`,
  `681989:4219379`, `681992:4219382`, `524386:4061776`,
  `476119:4013500`, `476122:4013503`, `776427:4313817`).
- Új megengedett érték: **1** (`íz: kannabisz`).
- Törölt megengedett érték: **0**.
- A fa módosítása után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `954869:4492259` | alkoholtartalom `ismeretlen` → `17%` |
| `627169:4164559` | íz `gyógynövény, tea` → `kannabisz, tea` |
| `3160:3160` | íz `natúr` → `gyógynövény` |
| `100528:3637735` | íz `natúr` → `gyógynövény` |
| `674513:4211903` | íz `natúr` → `rum` |
| `674510:4211900` | íz `natúr` → `rum` |
| `15349:15352` | íz `meggy` → `meggy, méz` |
| `524392:4061782` | alkoholtartalom `ismeretlen` → `15%` |
| `524395:4061785` | alkoholtartalom `ismeretlen` → `15%` |
| `524389:4061779` | alkoholtartalom `ismeretlen` → `15%` |
| `780944:4318334` | alkoholtartalom `ismeretlen` → `15%`; íz `csokoládé, földimogyoró` → `csokoládé, mogyoró` |
| `685151:4222541` | alkoholtartalom `ismeretlen` → `15%` |
| `685061:4222451` | alkoholtartalom `ismeretlen` → `15%` |

### Likőr kézi felülvizsgálat, 76–100. tétel

- Mind a 25 teljes rekordot és forrássort, valamint mind a 25 helyi
  termékképet egyenként, közvetlenül és részletes felbontásban
  ellenőriztük.
- Az Angelli gyártói termékoldala a Toffee változatot 15%-os
  krémlikőrként azonosította; a korábbi általános `egyéb likőr`
  fajtát pontosítottuk.
- A Garrone és Ramazzotti termékneve, címkéje és pontos termékadata
  Limoncellót igazolt. A Ramazzotti gyártói lapja 18%-os
  alkoholtartalmat és a két `z` betűs márkaalakot is közölte.
- A Distillati Group gyártói katalógusa az Oscar Bombardinót
  whiskyvel és rummal készülő tojáslikőrként írja le; ennek megfelelően
  a téves `natúr` ízt és `krémlikőr` fajtát javítottuk.
- A két azonos Baileys Original közül az 0,5 literes rekordnál pótoltuk
  a gyártó által is igazolt whisky-összetevőt, így az ízmező
  megegyezik a 0,7 literes változatéval.
- A Baileys Toffee Popcorn közvetlen címkéje és gyártói oldala a
  popcorn mellett a toffee ízt is igazolta.
- A Tatratea első sorozatú hatos miniszett címkéje és pontos
  készletleírása a 22%-os kókuszos, 32%-os citrusos, 42%-os
  őszibarackos, 52%-os eredeti, 62%-os erdei gyümölcsös és 72%-os
  Outlaw változatot igazolta. A már helyesen felsorolt hat alkoholfok
  mellé a négy hiányzó elemi ízt is rögzítettük.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **10**.
- Változatlanul hagyott rekord: **18**
  (`819551:4356941`, `819542:4356932`, `39394:39397`,
  `35905:35908`, `35716:35719`, `764463:4301853`,
  `796337:4333727`, `684809:4222199`, `627253:4164643`,
  `11233:11236`, `791762:4329152`, `764484:4301874`,
  `387761:3925034`, `3049:3049`, `265460:3802742`,
  `658824:4196214`, `11773:11776`, `36382:36385`).
- Új megengedett érték: **1** (`márka: Ramazzotti`).
- Törölt megengedett érték: **1** (`márka: Ramazotti`).
- A márkacsere átmeneti előállapotát külön ellenőriztük; az első
  rekordcsere után minden további lépés és a végső 47 030 rekordos
  validáció már az új fával futott. Eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `793106:4330496` | márka `Ramazotti` → `Ramazzotti`; alkoholtartalom `ismeretlen` → `18%`; fajta `gyümölcslikőr` → `limoncello` |
| `35119:35122` | fajta `egyéb likőr` → `krémlikőr` |
| `751968:4289358` | fajta `gyümölcslikőr` → `limoncello` |
| `3070:3070` | íz `tejszín` → `tejszín, whisky` |
| `684341:4221731` | íz `natúr` → `rum, tojás, whisky`; fajta `krémlikőr` → `tojáslikőr` |
| `894569:4431959` | íz `popcorn` → `popcorn, toffee` |
| `442852:3980236` | íz `tea` → `citrus, erdei gyümölcs, kókusz, őszibarack, tea` |

### Likőr kézi felülvizsgálat, 101–125. tétel

- Mind a 25 teljes rekordot és forrássort egyenként ellenőriztük.
  Huszonkét helyi termékképet közvetlenül és részletes felbontásban
  megvizsgáltunk; a két Tatratea Coop-rekordhoz és az 0,5 literes
  Unicum Szilvához nem tartozott helyi kép.
- A Baileys 1 literes Original változatánál pótoltuk a gyártó által
  igazolt whisky-elemet; így az azonos 0,5 és 0,7 literes rekordokkal
  egységes lett.
- A Beluga hivatalos oldala a két Botanicals változatot
  vodkaalapú, cukormentes botanikus italként, nem bitterként
  azonosítja. A forrás `növényi kivonatos likőr` megnevezését és a
  jelenlegi levél hatókörét megtartva a téves `keserűlikőr` fajtát a
  meglévő `egyéb likőr` értékre javítottuk.
- A két Jägermeister díszdoboz közül az egyik téves `natúr` ízét az
  azonos termék és a közvetlen címke szerinti `gyógynövény` értékre
  javítottuk.
- A Tullamore D.E.W. Honey közvetlen címkéje ír whiskyt és mézet
  igazolt; a már helyes `whiskyalapú likőr` fajta mellett az ízmezőbe
  is bekerült a hiányzó `whisky`.
- Az Unicum Orange esetében a `Bitter` a keserűlikőr fajtát jelöli,
  nem keserűnarancs-alapanyagot. A név és címke narancspárlatot
  igazol, ezért a redundáns, téves `keserűnarancs` értéket
  eltávolítottuk.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **6**.
- Változatlanul hagyott rekord: **19**
  (`829094:4366484`, `793766:4331156`, `793049:4330439`,
  `3376040`, `3375556`, `2857587`, `2857583`, `2857581`,
  `2857579`, `2857569`, `2857567`, `2817861`, `2817615`,
  `2817541`, `2814335`, `2813570`, `2813566`, `2810430`,
  `2808484`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `408015:3945366` | íz `tejszín` → `tejszín, whisky` |
| `770958:4308348` | fajta `keserűlikőr` → `egyéb likőr` |
| `771747:4309137` | fajta `keserűlikőr` → `egyéb likőr` |
| `3373920` | íz `natúr` → `gyógynövény` |
| `2817559` | íz `méz` → `méz, whisky` |
| `2817557` | íz `narancs, keserűnarancs` → `narancs` |

### Likőr kézi felülvizsgálat, 126–150. tétel

- Mind a 25 teljes rekordot és forrássort egyenként ellenőriztük.
  Tizenhat helyi termékképet közvetlenül és részletes felbontásban
  megvizsgáltunk; kilenc rekordhoz nem tartozott helyi kép.
- A Fütyülős hivatalos termékoldala és webshopja a rövidített
  Coop-nevek mögött a Feketecseresznye Mézzel, illetve a Csokis
  Mogyoró változatot igazolta. Emiatt a gyűjtő `cseresznye` értéket
  `fekete cseresznye`, a téves `földimogyoró` értéket pedig
  `mogyoró` értékre pontosítottuk.
- A Mozart Chocolate Cream poharas ajándékcsomag pontos termékadata
  0,5 literes palackot és 17%-os alkoholtartalmat, a Tatratea Peach
  neve és pontos termékadata pedig 0,7 literes, 42%-os őszibarackos
  tealikőrt igazolt. Csak a két hiányzó kiszerelésmezőt pótoltuk.
- A Jägermeister gyártói termékoldala a Manifest díszdobozt
  0,5 literes, 38%-os gyógynövénylikőrként azonosította; mindhárom
  hiányzó mennyiségi és alkoholfokmezőt rögzítettük.
- A Baileys Original és Jim Beam Honey azonos, már ellenőrzött
  termékcsaládja, teljes neve és címkéje igazolta a hiányzó
  `whisky` ízelemet.
- A magyar hatósági likőrvizsgálat a Gold Advocaat 0,7 literes
  tojáslikőrt 14%-osként azonosította; a közvetlen kép ugyanazt a
  magyar változatot mutatja, ezért nem a jelenlegi német 20%-os
  változat adatát vettük át.
- A Lidl-forrás három 0,7 literes rekordja és a közvetlen címkék
  Tatratea Original 52%, Unicum 40%, illetve Jägermeister 35%
  terméket igazoltak; a hiányzó kiszereléseket és két alkoholfokot
  pótoltuk.
- A három Koronás és az egy St. Hubertus keserűlikőr közvetlen
  címkéje, valamint a már helyes `gyógynövényes: true` jelölés
  gyógynövényes profilt igazolt. A téves `natúr` ízt mind a négy
  rekordnál `gyógynövény` értékre javítottuk.
- A KUNSÁG-SZESZ Mézes barack teljes forrásneve és palackcímkéje
  igazolta a teljes márkaalakot. A likőrlevél egyetlen `Kunság`
  márkájú rekordjának javítása után a rövidített faértéket töröltük.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **25**.
- Változatlanul hagyott rekord: **9**
  (`2808481`, `2806835`, `2806932`, `2797374`, `2752580`,
  `BTY-X10061600320021`, `BTY-X10061700320021`,
  `BTY-X11899600320021`, `BTY-X16739700320021`).
- Új megengedett érték: **2** (`íz: fekete cseresznye`,
  `márka: Kunság-Szesz`).
- Törölt megengedett érték: **1** (`márka: Kunság`).
- A márkacsere átmeneti előállapotát külön ellenőriztük; az első
  rekordcsere után minden további lépés és a végső 47 030 rekordos
  validáció már az új fával futott. Eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18292000320021` | márka `Kunság` → `Kunság-Szesz` |
| `2808480` | íz `cseresznye, méz` → `fekete cseresznye, méz` |
| `2808479` | íz `csokoládé, földimogyoró` → `csokoládé, mogyoró` |
| `2757431` | kiszerelés `ismeretlen` → `500 ml`; egységnyi kiszerelés `ismeretlen` → `500 ml` |
| `2757310` | kiszerelés `ismeretlen` → `700 ml`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `2756786` | kiszerelés `ismeretlen` → `500 ml`; alkoholtartalom `ismeretlen` → `38%`; egységnyi kiszerelés `ismeretlen` → `500 ml` |
| `2752587` | íz `tejszín` → `tejszín, whisky` |
| `10539` | íz `méz` → `méz, whisky` |
| `10000146` | alkoholtartalom `ismeretlen` → `14%` |
| `10041720` | kiszerelés `ismeretlen` → `700 ml`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10106438` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `40%`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `10107389` | kiszerelés `ismeretlen` → `700 ml`; alkoholtartalom `ismeretlen` → `35%`; egységnyi kiszerelés `ismeretlen` → `700 ml` |
| `BTY-X16650500320021` | íz `natúr` → `gyógynövény` |
| `BTY-X16658300320021` | íz `natúr` → `gyógynövény` |
| `BTY-X17581700320021` | íz `natúr` → `gyógynövény` |
| `BTY-X17582100320021` | íz `natúr` → `gyógynövény` |

### Likőr kézi felülvizsgálat, 151–175. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Snow Globe eredeti csomagolása `Orange & Gingerbread` ízt
  közöl. A `gingerbread` teljes íznév, nem pusztán gyömbér, ezért a
  téves `gyömbér` értéket `mézeskalács` értékre pontosítottuk.
- A Christmas Globe eredeti csomagolása szó szerint
  `Spiced Orange & Cranberry`. Az `áfonya` gyűjtőérték helyett a
  pontos `vörös áfonya` került be, és rögzítettük a közvetlenül
  feliratozott `fűszeres` ízjelleget is.
- A Baileys Original 0,7 literes rekordjánál pótoltuk az azonos,
  korábban ellenőrzött Original változatok és a gyártói termékadat
  által igazolt `whisky` ízelemet.
- A Mercy’s közvetlen címkéje és teljes forrásneve `Whisky Cream`,
  illetve `Krémlikőr Whiskyvel` megjelölést tartalmaz. A téves
  `natúr` ízt ezért `tejszín, whisky` értékre javítottuk.
- Az Unicum 0,5 literes eredeti változatának teljes neve
  gyógynövénylikőrt, a rekord pedig már helyesen
  `gyógynövényes: true` értéket közölt; a téves `natúr` ízt
  `gyógynövény` értékre javítottuk.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **5**.
- Változatlanul hagyott rekord: **20**
  (`BTY-X18326600320021`, `BTY-X17572600320021`,
  `BTY-X17572500320021`, `BTY-X18414700320021`,
  `BTY-X16636600320021`, `BTY-X18104300320021`,
  `BTY-X17532000320021`, `BTY-X14787300320021`,
  `BTY-X16265400320021`, `BTY-X16599700320021`,
  `BTY-X17179300320021`, `BTY-X17179900320021`,
  `BTY-X17250200320021`, `BTY-X17370000320021`,
  `BTY-X17394200320021`, `BTY-X17394400320021`,
  `BTY-X17394700320021`, `BTY-X17394800320021`,
  `BTY-X17531800320021`, `BTY-X17531900320021`).
- Új megengedett érték: **3** (`íz: fűszeres`,
  `íz: mézeskalács`, `íz: vörös áfonya`).
- Törölt megengedett érték: **0**.
- A fa módosítása után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X16915700320021` | íz `gyömbér, narancs` → `mézeskalács, narancs` |
| `BTY-X16915800320021` | íz `áfonya, narancs` → `fűszeres, narancs, vörös áfonya` |
| `BTY-X10280700320021` | íz `tejszín` → `tejszín, whisky` |
| `BTY-X16636700320021` | íz `natúr` → `tejszín, whisky` |
| `BTY-X17394600320021` | íz `natúr` → `gyógynövény` |

### Likőr kézi felülvizsgálat, 176–200. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- Külön ellenőriztük az Unicum Orange Bitter kiszerelésenként eltérő
  alkoholfokát. A gyártói webshop a 0,2 literes változatot 32%-osként,
  a felülvizsgált 0,5 és 1 literes változatokat 34,5%-osként adja meg,
  ezért mindhárom rekord meglévő értéke változatlanul helyes.
- A Baileys Original 0,5 literes rekordjánál pótoltuk az azonos,
  korábban ellenőrzött Original változatok és a gyártói termékadat
  által igazolt `whisky` ízelemet.
- A 12 × 40 ml-es Unicum csomag az eredeti Unicum minipalackjait
  tartalmazza. A gyártói termékadat a 40 ml-es változatot is
  40%-osként igazolja, ezért az `ismeretlen` alkoholfokot
  pontosítottuk.
- A Fütyülős Csokis Mogyoró neve, közvetlen címkéje és gyártói
  termékoldala valódi mogyoróízt igazolt; a téves `földimogyoró`
  értéket `mogyoró` értékre javítottuk.
- A Drinks Ireland gyártói tagsági terméklapja a Carolans Original
  összetevőjeként friss ír tejszínt, ír whiskyt és mézet sorol fel;
  a két hiányzó ízelemet rögzítettük.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **4**.
- Változatlanul hagyott rekord: **21**
  (`BTY-X17532300320021`, `BTY-X18090200320021`,
  `BTY-X18104200320021`, `BTY-X18193600320021`,
  `BTY-X18415000320021`, `BTY-X18906100320021`,
  `BTY-X18969500320021`, `BTY-X17418600320021`,
  `BTY-X17418500320021`, `BTY-X17416800320021`,
  `BTY-X7427800320021`, `BTY-X17416600320021`,
  `BTY-X17395200320021`, `BTY-X18326500320021`,
  `BTY-X18326800320021`, `BTY-X1261300320022`,
  `BTY-X17310000320021`, `BTY-X14365600320021`,
  `BTY-X17873700320021`, `BTY-X17686000320021`,
  `BTY-X17309900320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X3766700320021` | íz `tejszín` → `tejszín, whisky` |
| `BTY-X16658400320021` | alkoholtartalom `ismeretlen` → `40%` |
| `BTY-X17399300320021` | íz `csokoládé, földimogyoró` → `csokoládé, mogyoró` |
| `BTY-X12267800320021` | íz `tejszín` → `méz, tejszín, whisky` |

### Likőr kézi felülvizsgálat, 201–225. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Becherovka gyártói termékleírása az Original változatot
  gyógynövények és fűszerek kiegyensúlyozott keverékéből készült
  cseh bitterként azonosítja. A már helyes `gyógynövény` íz és
  `gyógynövényes: true` jelölés mellett a pontatlan `egyéb likőr`
  fajtát ezért `keserűlikőr` értékre javítottuk.
- A Baileys Original 1 literes rekordjánál pótoltuk az azonos,
  korábban ellenőrzött Original változatok és a gyártói termékadat
  által igazolt `whisky` ízelemet.
- A Baileys Chocolat Luxe gyártói leírása ír tejszínt, ír whiskyt
  és belga csokoládét nevez meg. A már rögzített csokoládé mellé
  bekerült a két hiányzó, közvetlenül igazolt ízelem.
- Az Angelli Toffee az azonos, korábban ellenőrzött változat
  gyártói termékadata szerint krémlikőr; a pontatlan `egyéb likőr`
  fajtát ennek megfelelően javítottuk.
- A Mátyás Keserű Classic termékleírása gazdag gyógynövényes
  karaktert közöl, a 24%-os Mátyás Keserű pontos összetevőlistája
  pedig gyógynövénykivonatokat nevez meg. A négy érintett rekord
  téves `natúr` ízét `gyógynövény` értékre javítottuk.
- A Mozart Dark Chocolate gyártói oldala egyértelműen tejszín
  nélküli, vegán csokoládélikőrként írja le a terméket, és
  csokoládé-, vanília-, karamell- és toffee-jegyeket közöl. A téves
  `krémlikőr` fajtát és a hiányos ízlistát ennek megfelelően
  pontosítottuk.
- A Bumbu Crème gyártói leírása rumot, fűszereket és valódi
  tejszínt nevez meg; a téves `natúr` íz helyére ez a három
  közvetlenül igazolt elem került.
- Módosított rekord: **10**.
- Módosított tulajdonságmező: **11**.
- Változatlanul hagyott rekord: **15**
  (`BTY-X13013300320021`, `BTY-X17508600320021`,
  `BTY-X17691600320021`, `BTY-X17592800320021`,
  `BTY-X10414300320021`, `BTY-X10206900320021`,
  `BTY-X12146700320021`, `BTY-X12353200320021`,
  `BTY-X14787600320021`, `BTY-X14787700320021`,
  `BTY-X15329100320021`, `BTY-X16295900320021`,
  `BTY-X16590300320021`, `BTY-X16630200320021`,
  `BTY-X16658800320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17807800320021` | fajta `egyéb likőr` → `keserűlikőr` |
| `BTY-X12963200320021` | íz `tejszín` → `tejszín, whisky` |
| `BTY-X10628500320021` | íz `csokoládé` → `csokoládé, tejszín, whisky` |
| `BTY-X11899700320021` | fajta `egyéb likőr` → `krémlikőr` |
| `BTY-X13390800320021` | íz `natúr` → `gyógynövény` |
| `BTY-X15363500320021` | íz `csokoládé` → `csokoládé, karamell, toffee, vanília`; fajta `krémlikőr` → `csokoládélikőr` |
| `BTY-X16293800320021` | íz `natúr` → `fűszeres, rum, tejszín` |
| `BTY-X16453700320021` | íz `natúr` → `gyógynövény` |
| `BTY-X16453800320021` | íz `natúr` → `gyógynövény` |
| `BTY-X16453900320021` | íz `natúr` → `gyógynövény` |

### Likőr kézi felülvizsgálat, 226–250. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A két Feketecseresznye Mézzel változat teljes neve és közvetlen
  címkéje a pontos `fekete cseresznye` értéket és a mézet is
  igazolta. A Mézes Barack 0,5 literes változatnál szintén pótoltuk
  a névben és címkén szereplő, de a rekordból hiányzó `méz` értéket.
- A Royal Bitter gyártói oldala fahéjat, vaníliát, citromhéjat és
  gyógynövényeket nevez meg a likőr jellegzetes aromájának
  forrásaként. A téves `natúr` ízt ezért a meglévő elemi
  `citrom, fahéj, gyógynövény, vanília` értékekre javítottuk.
- A Ferencz Keserű pontos termékleírása gyógynövénykivonatot és
  gyógynövénypárlatot igazol; a téves `natúr` ízt
  `gyógynövény` értékre javítottuk.
- Az eredeti Jägermeister 0,5 literes változatánál a közvetlen
  címke, a termékazonosság és a már ellenőrzött azonos kiszerelések
  csak a gyógynövényes profilt igazolják. A korábbról örökölt,
  termékváltozatot tévesen jelölő `narancs` értéket eltávolítottuk.
- Módosított rekord: **6**.
- Módosított tulajdonságmező: **6**.
- Változatlanul hagyott rekord: **19**
  (`BTY-X16740900320021`, `BTY-X16780800320021`,
  `BTY-X17179500320021`, `BTY-X17179600320021`,
  `BTY-X17179700320021`, `BTY-X17180200320021`,
  `BTY-X17180300320021`, `BTY-X17192400320021`,
  `BTY-X17310900320021`, `BTY-X17393900320021`,
  `BTY-X17394000320021`, `BTY-X17394100320021`,
  `BTY-X17398600320021`, `BTY-X17503900320021`,
  `BTY-X17530500320021`, `BTY-X17531700320021`,
  `BTY-X17532400320021`, `BTY-X17532600320021`,
  `BTY-X17532700320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17398400320021` | íz `cseresznye` → `fekete cseresznye, méz` |
| `BTY-X17399000320021` | íz `cseresznye, méz` → `fekete cseresznye, méz` |
| `BTY-X17399100320021` | íz `barack` → `barack, méz` |
| `BTY-X17503200320021` | íz `natúr` → `citrom, fahéj, gyógynövény, vanília` |
| `BTY-X17550600320021` | íz `natúr` → `gyógynövény` |
| `BTY-X17572300320021` | íz `gyógynövény, narancs` → `gyógynövény` |

### Likőr kézi felülvizsgálat, 251–275. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Sierra gyártói termékoldala és a közvetlen címke a Tropical
  Chilli változatot mangó-, maracuja- és chiliízűként azonosítja.
  A pontatlan `trópusi gyümölcs` gyűjtőértéket a két konkrét
  gyümölcsre bontottuk.
- Egy további eredeti Jägermeister-változatból eltávolítottuk a
  termékazonosságot tévesen módosító `narancs` ízt.
- A Royal Bitter 10 és 20 ml-ként rövidített két forrásneve
  valójában 0,1 és 0,2 literes palackot jelöl: ezt a forrás
  100/200 ml-es numerikus mennyisége és a pontos termékoldalak is
  igazolják. Mindkét mennyiségmezőt javítottuk, a téves `natúr`
  ízt pedig az azonos 0,5 literes változat gyártói adata szerinti
  `citrom, fahéj, gyógynövény, vanília` értékekre cseréltük.
- A Fireball teljes neve, fajtája és címkéje fahéjas whiskylikőrt
  igazol; a hiányzó `whisky` ízelemet pótoltuk.
- A Casali közvetlen címkéje és az alapjául szolgáló gyártói
  termékadat banánt és csokoládét, a Manner gyártói webshopja pedig
  csokoládés-mogyorós krémlikőrt igazol. A két ízlistát, valamint a
  Manner téves fajtáját ennek megfelelően javítottuk.
- A Cream Heroes gyártói oldalai mindkét tételnél tejkrém-alapot,
  tequilát és a címke szerinti epret, illetve kávét neveznek meg.
  A hiányzó `tejszín` értéket mindkét rekordban pótoltuk.
- A Baileys Toffee Popcorn gyártói oldala a változatot az Original
  Irish Cream tejszínes-whiskys alapjával kapcsolja össze; a
  popcorn és karamell mellé bekerült a hiányzó `tejszín` és
  `whisky`.
- A két Unicum Orange és az Unicum B&N ajándékcsomag
  `keserűnarancs` értékét a név, címke és korábban ellenőrzött
  azonos termékek szerinti `narancs` értékre javítottuk. A `Bitter`
  ezeknél a keserűlikőr fajtát, nem az alapanyagot jelöli.
- A 24 × 40 ml-es Mátyás Keserű közvetlen címkéje fűszer- és
  gyógynövénykivonatokat sorol fel; az azonos változatokkal
  egységesen a téves `natúr` ízt `gyógynövény` értékre javítottuk.
- Módosított rekord: **14**.
- Módosított tulajdonságmező: **19**.
- Változatlanul hagyott rekord: **11**
  (`BTY-X17641600320021`, `BTY-X17641700320021`,
  `BTY-X17646900320021`, `BTY-X17686300320021`,
  `BTY-X17692600320021`, `BTY-X17807900320021`,
  `BTY-X18280200320021`, `BTY-X18303800320021`,
  `BTY-X18303900320021`, `BTY-X18304000320021`,
  `BTY-X18413400320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17641000320021` | íz `trópusi gyümölcs, chili` → `chili, mangó, maracuja` |
| `BTY-X17691000320021` | íz `gyógynövény, narancs` → `gyógynövény` |
| `BTY-X17698000320021` | kiszerelés `10 ml` → `100 ml`; íz `natúr` → `citrom, fahéj, gyógynövény, vanília`; egységnyi kiszerelés `10 ml` → `100 ml` |
| `BTY-X17698200320021` | kiszerelés `20 ml` → `200 ml`; íz `natúr` → `citrom, fahéj, gyógynövény, vanília`; egységnyi kiszerelés `20 ml` → `200 ml` |
| `BTY-X17700400320021` | íz `fahéj` → `fahéj, whisky` |
| `BTY-X17838000320021` | íz `banán` → `banán, csokoládé` |
| `BTY-X17854600320021` | íz `földimogyoró` → `csokoládé, mogyoró, tejszín`; fajta `egyéb likőr` → `krémlikőr` |
| `BTY-X18345800320021` | íz `eper` → `eper, tejszín` |
| `BTY-X18346000320021` | íz `kávé` → `kávé, tejszín` |
| `BTY-X18358100320021` | íz `karamell, popcorn` → `karamell, popcorn, tejszín, whisky` |
| `BTY-X18412900320021` | íz `keserűnarancs` → `narancs` |
| `BTY-X18413300320021` | íz `keserűnarancs` → `narancs` |
| `BTY-X18506000320021` | íz `natúr` → `gyógynövény` |
| `BTY-X18542900320021` | íz `gyógynövény, keserűnarancs, kávé` → `gyógynövény, kávé, narancs` |

### Likőr kézi felülvizsgálat, 276–300. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A három Unicum ajándékcsomag közvetlen képe az Orange változatot
  igazolja. A `Bitter` a keserűlikőr fajtát jelöli, ezért a pontatlan
  `keserűnarancs` ízt az azonos, már ellenőrzött termékekkel egységesen
  `narancs` értékre javítottuk.
- A Várda eredeti, Szilva, Coffee és Orange Dark pontos gyártói, illetve
  termékforrásai gyógynövény- és fűszerkivonatokra épülő keserűlikőröket
  igazolnak. A Szilva aszalt szilva kivonatot, a Coffee kávékivonatot,
  az Orange Dark narancskoncentrátumot és kakaókivonatot is tartalmaz;
  a fajtát, az ízlistát és a gyógynövényes jelzőt ennek megfelelően
  pontosítottuk.
- A két St. Hubertus díszdoboz közvetlen csomagképe egy 500 ml-es
  palackot és egy 40 ml-es minit mutat. Az összkiszerelést 540 ml-re,
  az egységnyi kiszereléseket 500 és 40 ml-re javítottuk; az Original
  csomagnál a vérnarancs mini 32%-os alkoholfokát és ízét is pótoltuk.
- Az Angelli Cioccolato gyártói leírása csokoládét, mogyorót és
  tejjel készült krémes karaktert, a Tiramisu pedig krémlikőr-alapot
  igazol. A hiányzó `mogyoró`, illetve `tejszín` ízelemeket pótoltuk.
- A Mozart Gold, White és Strawberry gyártói terméklapjai tejszínt és
  vaníliát, a White karamellt, a Strawberry pedig epret és fehér
  csokoládét is igazol. A három ízlistát csak ezekkel a közvetlenül
  bizonyított elemekkel egészítettük ki.
- A Baileys Original ajándékcsomagnál pótoltuk az ír krémlikőr
  whisky-elemét. A Tatratea hatrészes mini csomag gyártói termékadata
  a kókusz, citrus, őszibarack, eredeti tea, erdei gyümölcs és Outlaw
  változatokat igazolja; az ízlistát a bizonyítható elemi ízekre
  bontottuk.
- A Ferencz 30 × 40 ml-es keserűlikőr pontos összetevőadata
  gyógynövénykivonatot igazol. A Tatratea Flower gyártói leírása
  bodzavirágot, akácmézet és teát nevez meg; a hiányzó elemi
  `bodzavirág` értéket felvettük a Likőr ízlistájába.
- Módosított rekord: **18**.
- Módosított tulajdonságmező: **28**.
- Változatlanul hagyott rekord: **7**
  (`BTY-X18958000320021`, `BTY-X43396900320022`,
  `BTY-X6974300320021`, `BTY-X16658700320021`,
  `BTY-X16756700320021`, `BTY-X17709000320021`,
  `BTY-X83484800320022`).
- Új megengedett érték: **2** (`íz: bodzavirág`;
  `kiszerelés: 540 ml`).
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18543100320021` | íz `szilva, keserűnarancs, kávé` → `kávé, narancs, szilva` |
| `BTY-X18543200320021` | íz `kávé, keserűnarancs` → `kávé, narancs` |
| `BTY-X18543300320021` | íz `kávé, keserűnarancs` → `kávé, narancs` |
| `BTY-X18615700320021` | íz `natúr` → `gyógynövény` |
| `BTY-X18615900320021` | íz `szilva` → `gyógynövény, szilva`; fajta `gyümölcslikőr` → `keserűlikőr`; gyógynövényes `false` → `true` |
| `BTY-X18616000320021` | íz `kávé` → `gyógynövény, kávé`; fajta `kávélikőr` → `keserűlikőr`; gyógynövényes `false` → `true` |
| `BTY-X18616100320021` | íz `narancs, csokoládé` → `csokoládé, gyógynövény, narancs`; fajta `egyéb likőr` → `keserűlikőr`; gyógynövényes `false` → `true` |
| `BTY-X18824100320021` | kiszerelés `40 ml` → `540 ml`; alkoholtartalom `33%` → `33%, 32%`; íz `gyógynövény` → `gyógynövény, vérnarancs`; egységnyi kiszerelés `40 ml` → `500 ml, 40 ml` |
| `BTY-X18824500320021` | kiszerelés `40 ml` → `540 ml`; egységnyi kiszerelés `40 ml` → `500 ml, 40 ml` |
| `BTY-X3566900320021` | íz `csokoládé` → `csokoládé, mogyoró, tejszín` |
| `BTY-X3567000320021` | íz `tiramisu` → `tejszín, tiramisu` |
| `BTY-X87615500320022` | íz `csokoládé` → `csokoládé, tejszín, vanília` |
| `BTY-X87616200320022` | íz `csokoládé` → `csokoládé, karamell, tejszín, vanília` |
| `BTY-X93291100320022` | íz `tejszín` → `tejszín, whisky` |
| `BTY-X9705200320021` | íz `tea` → `citrus, erdei gyümölcs, kókusz, őszibarack, tea` |
| `BTY-X10376300320021` | íz `csokoládé, eper` → `csokoládé, eper, tejszín, vanília` |
| `BTY-X16739600320021` | íz `natúr` → `gyógynövény` |
| `BTY-X17532500320021` | íz `tea` → `bodzavirág, méz, tea` |

### Likőr kézi felülvizsgálat, 301–325. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Monin Brown Cacao közvetlen címkéje és pontos termékforrása
  kakaóbabból készült, barna kakaólikőrt igazol. A pontatlan
  `csokoládé` ízt ezért az új, elemi `kakaó` értékre javítottuk;
  a meglévő `csokoládélikőr` fajta maradt a legpontosabb elérhető
  likőrfajta.
- A Monin hivatalos, 700 ml-es Litchi terméklapja 17%-os
  alkoholtartalmat közöl. A korábbi `ismeretlen` értéket erre
  javítottuk; az íz, fajta és minden mennyiségmező változatlanul
  helyes maradt.
- A Royal Kaktusz közvetlen címkéje kaktuszgyümölcsöt ábrázol, a
  pontos termékforrások pedig kaktuszgyümölcsös likőrként írják le.
  A pontatlan `egyéb likőr` fajtát `gyümölcslikőr` értékre
  javítottuk.
- A 100 és 500 ml-es Royal Mogyoró közvetlen palackcímkéjén
  mogyoró látható és a terméknév is ezt nevezi meg. A növénytanilag
  és ízében is eltérő `földimogyoró` értéket mindkét rekordnál
  `mogyoró` értékre cseréltük.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **5**.
- Változatlanul hagyott rekord: **20**
  (`BTY-X16132600320021`, `BTY-X16132800320021`,
  `BTY-X6022300320021`, `BTY-X6022700320021`,
  `BTY-X18150100320021`, `BTY-X18150500320021`,
  `BTY-X18150800320021`, `BTY-X18151300320021`,
  `BTY-X18152000320021`, `BTY-X18152800320021`,
  `BTY-X18474000320021`, `BTY-X18889600320021`,
  `BTY-X14949800320021`, `BTY-X17502400320021`,
  `BTY-X17636900320021`, `BTY-X17637000320021`,
  `BTY-X17637100320021`, `BTY-X18150000320021`,
  `BTY-X18150200320021`, `BTY-X18150400320021`).
- Új megengedett érték: **1** (`íz: kakaó`).
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X5998200320021` | íz `csokoládé` → `kakaó` |
| `BTY-X6023000320021` | alkoholtartalom `ismeretlen` → `17%` |
| `BTY-X18473600320021` | fajta `egyéb likőr` → `gyümölcslikőr` |
| `BTY-X14949400320021` | íz `földimogyoró` → `mogyoró` |
| `BTY-X17502900320021` | íz `földimogyoró` → `mogyoró` |

### Likőr kézi felülvizsgálat, 326–350. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A 200 ml-es Royal Mogyoró címkéje és termékneve az előző
  kötegben ellenőrzött 100 és 500 ml-es változatokkal azonos
  mogyorót igazol. A téves `földimogyoró` ízt `mogyoró`
  értékre javítottuk.
- A 200 ml-es Royal Kaktusz azonos termékcsaládhoz és recepthez
  tartozik, mint az előző kötegben ellenőrzött 500 ml-es
  kaktuszgyümölcsös változat. A pontatlan `egyéb likőr` fajtát
  `gyümölcslikőr` értékre javítottuk.
- A tizenegy Jack Daniel's és Jim Beam tétel teljes neve,
  közvetlen címkéje és meglévő `whiskyalapú likőr` fajtája
  egyaránt Tennessee whiskey-, illetve bourbonwhiskey-alapot
  igazol. Az alma, méz, fahéj, őszibarack és ananász mellől
  hiányzó `whisky` ízelemet minden érintett rekordnál pótoltuk.
- A Jim Beam Black Cherry neve és címkéje kifejezetten fekete
  cseresznyét igazol. Az általános `cseresznye` értéket a már
  engedélyezett `fekete cseresznye` értékre pontosítottuk, és
  ennél a whiskyalapot is rögzítettük.
- Módosított rekord: **13**.
- Módosított tulajdonságmező: **13**.
- Változatlanul hagyott rekord: **12**
  (`BTY-X18150600320021`, `BTY-X18150700320021`,
  `BTY-X18151100320021`, `BTY-X18151200320021`,
  `BTY-X18151800320021`, `BTY-X18151900320021`,
  `BTY-X18152300320021`, `BTY-X18152600320021`,
  `BTY-X18473800320021`, `BTY-X18473900320021`,
  `BTY-X18889700320021`, `BTY-X18889800320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18151500320021` | íz `földimogyoró` → `mogyoró` |
| `BTY-X18473500320021` | fajta `egyéb likőr` → `gyümölcslikőr` |
| `BTY-X17485700320021` | íz `fahéj` → `fahéj, whisky` |
| `BTY-X17486100320021` | íz `alma` → `alma, whisky` |
| `BTY-X17486400320021` | íz `méz` → `méz, whisky` |
| `BTY-X17637800320021` | íz `alma` → `alma, whisky` |
| `BTY-X17638000320021` | íz `cseresznye` → `fekete cseresznye, whisky` |
| `BTY-X17638100320021` | íz `méz` → `méz, whisky` |
| `BTY-X17639200320021` | íz `őszibarack` → `őszibarack, whisky` |
| `BTY-X18936500320021` | íz `ananász` → `ananász, whisky` |
| `BTY-X17485600320021` | íz `méz` → `méz, whisky` |
| `BTY-X17485800320021` | íz `fahéj` → `fahéj, whisky` |
| `BTY-X17485900320021` | íz `alma` → `alma, whisky` |

### Likőr kézi felülvizsgálat, 351–375. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A két Malibu teljes neve és közvetlen címkéje egyaránt karibi
  rumot és kókuszt nevez meg. A `rumalapú likőr` fajtával
  összhangban mindkét ízlistához pótoltuk a `rum` értéket.
- A Monkai Belgian Rum Liqueur pontos termékleírásai karibi rumot,
  karamellizált banánt, karamellt, mézet, toffee-t, trópusi
  gyümölcsöt, vaníliát és fűszeres jegyeket igazolnak. A téves
  `natúr` értéket csak ezekre a közvetlenül közölt elemekre
  bontottuk; a „krémes” itt állag, nem bizonyított tejtermék.
- A Legendario Elixir de Cuba gyártói leírása szerint érlelt
  rumok keverékét 40–50 napig mazsolán áztatják. Az ízt
  `mazsola, rum` értékre, a pontatlan `egyéb likőr` fajtát
  `rumalapú likőr` értékre javítottuk.
- A Baileys Original és az O'Caroll közvetlen neve, címkéje és
  krémlikőr fajtája tejszínes-whiskys alapot igazol; a hiányzó
  `whisky`, illetve `tejszín, whisky` elemeket pótoltuk.
- Az Unicum Orange Bitter esetében a `Bitter` a keserűlikőr
  fajtát jelöli, a név és a címke pedig narancspárlatot. A
  redundáns, termékváltozatot tévesen kettőző `keserűnarancs`
  értéket eltávolítottuk.
- A Sunburst Cherry magyar termékneve és palackcímkéje egyaránt
  meggyet nevez meg; a téves `cseresznye` értéket `meggy`
  értékre javítottuk.
- A Jägermeister, a három eredeti St. Hubertus és az eredeti
  Unicum képe, neve és az azonos korábban ellenőrzött változatok
  csak a gyógynövényes profilt igazolják. A más ízesített
  változatból örökölt `narancs` értéket mind a hat rekordból
  eltávolítottuk.
- A Jack Daniel's Tennessee Fire teljes neve és címkéje fahéjas,
  Tennessee whiskeyvel készült likőrt igazol; a hiányzó
  `whisky` ízelemet pótoltuk.
- Módosított rekord: **15**.
- Módosított tulajdonságmező: **16**.
- Változatlanul hagyott rekord: **10**
  (`BTY-X18548400320021`, `1012973`, `1012101`, `1012102`,
  `1012970`, `999979`, `1009910`,
  `e21b7894c69ed353fab3076f`, `9423baf9153730c4d9850106`,
  `db64f0b1de32440fabd7625c`).
- Új megengedett érték: **1** (`íz: mazsola`).
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17592700320021` | íz `kókusz` → `kókusz, rum` |
| `BTY-X18548500320021` | íz `natúr` → `banán, fűszeres, karamell, méz, rum, toffee, trópusi gyümölcs, vanília` |
| `BTY-X17579700320021` | íz `natúr` → `mazsola, rum`; fajta `egyéb likőr` → `rumalapú likőr` |
| `732232` | íz `tejszín` → `tejszín, whisky` |
| `1054317` | íz `narancs, keserűnarancs` → `narancs` |
| `1021725` | íz `cseresznye` → `meggy` |
| `914673` | íz `natúr` → `tejszín, whisky` |
| `985632` | íz `gyógynövény, narancs` → `gyógynövény` |
| `1006051` | íz `kókusz` → `kókusz, rum` |
| `998001` | íz `gyógynövény, narancs` → `gyógynövény` |
| `b9b54b306a5fc7c0e3b05401` | íz `fahéj` → `fahéj, whisky` |
| `82c85696b5ce3759841cb416` | íz `gyógynövény, narancs` → `gyógynövény` |
| `8675b412840ae31faa847b42` | íz `gyógynövény, narancs` → `gyógynövény` |
| `9a0559f0a8784f3e14f34d5c` | íz `gyógynövény, narancs` → `gyógynövény` |
| `24bd57ea790c3e2c760020d6` | íz `gyógynövény, narancs` → `gyógynövény` |

### Likőr kézi felülvizsgálat, 376–400. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A két eredeti Jägermeister és a két eredeti Unicum neve,
  címkéje és a korábban ellenőrzött azonos változatok csak a
  gyógynövényes profilt igazolják. A három tévesen örökölt
  `narancs` elemet eltávolítottuk, az 1 literes Unicum pontatlan
  `natúr` ízét pedig `gyógynövény` értékre javítottuk.
- A Jägermeister Orange neve és címkéje az eredeti gyógynövényes
  alap narancsos változatát igazolja, ezért a hiányzó
  `gyógynövény` ízelemet pótoltuk. Az Unicum Orange Bitter
  rekordjánál a `Bitter` a keserűlikőr fajtát jelöli, ezért a
  redundáns `keserűnarancs` értéket eltávolítottuk.
- A négy Baileys Original az azonos, korábban ellenőrzött
  változatok és a gyártói termékadat alapján tejszínt és ír
  whiskyt tartalmaz; mind a négy ízlistához pótoltuk a hiányzó
  `whisky` elemet.
- A Saint's whiskyvel készült krémlikőr termékleírása holland
  tejszínt és több mint tíz évig érlelt whiskyt nevez meg. A
  téves `natúr` értéket a két bizonyított ízelemre javítottuk.
  A tojásos és csokoládés Saint's változatot nem egészítettük ki
  nem bizonyított tejszínnel.
- A Mozart Gold, az Angelli Cioccolato és az Angelli Tiramisu
  azonos változatait korábban gyártói termékadat alapján már
  ellenőriztük. A hiányzó `tejszín`, `vanília` és `mogyoró`
  elemeket ugyanazon bizonyíték szerint pótoltuk. Az Angelli
  Toffee gyártói oldala krémlikőrként azonosítja a terméket, ezért
  csak a pontatlan `egyéb likőr` fajtát javítottuk.
- A Tokaj Spirit Zserbó termékleírása dió ízű csokoládé
  krémlikőrt és barackpálinkát nevez meg. A `zserbó` változatjelölés
  megtartása mellett pótoltuk a három közvetlenül bizonyított
  ízelemet.
- A Carolans Original gyártói tagsági terméklapja friss ír
  tejszínt, ír whiskyt és mézet sorol fel; a két hiányzó
  ízelemet rögzítettük.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **16**.
- Változatlanul hagyott rekord: **9**
  (`a3512e5432a419980c2a494a`, `0501d42c4750c57e3204f1e6`,
  `c06b349d41f8cba7bb38ecc9`, `56d7fd1f43f186684b863cae`,
  `a3cb731669b365cd6276916a`, `7c128c37b2a60e5ed644804a`,
  `49e1364237c29495809c90d1`, `f335f6e560bbf8767497d94d`,
  `bf7fbb5eaf2b555cdced8dc4`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `0647f45caeb7a30972dff54e` | íz `gyógynövény, narancs` → `gyógynövény` |
| `3b29031e9ce8cc3784a136c2` | íz `gyógynövény, narancs` → `gyógynövény` |
| `0c7febd62cc0204de2f1af0e` | íz `narancs, keserűnarancs` → `narancs` |
| `5d7c0fbc5e2c3986ef3188dd` | íz `narancs` → `gyógynövény, narancs` |
| `fd5a2c8bfc50fa05a0d96fe9` | íz `tejszín` → `tejszín, whisky` |
| `8559b3c0599b6599f3c2ff15` | íz `tejszín` → `tejszín, whisky` |
| `6f3efcc39cec43f1b3e205c1` | íz `tejszín` → `tejszín, whisky` |
| `cc34d43e649a5cc28c876b33` | íz `tejszín` → `tejszín, whisky` |
| `278c4bb346e2ab152281bc31` | íz `natúr` → `tejszín, whisky` |
| `4bc01cb1c7c333afaaccf791` | íz `csokoládé` → `csokoládé, tejszín, vanília` |
| `d6e3c1cb8b6abe75d8405b02` | íz `csokoládé` → `csokoládé, mogyoró, tejszín` |
| `34becb95f3773c832dab9e16` | íz `tiramisu` → `tejszín, tiramisu` |
| `8e51bedd28904bbab0197b9b` | fajta `egyéb likőr` → `krémlikőr` |
| `a2f7bd11034f3fda7f2f0b4c` | íz `zserbó` → `barack, csokoládé, dió, zserbó` |
| `1858be8cea2d9512f8ab3c35` | íz `natúr` → `gyógynövény` |
| `e6f3c677e12f269df31af18a` | íz `tejszín` → `méz, tejszín, whisky` |

### Likőr kézi felülvizsgálat, 401–425. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Tokaj Spirit Eper termékleírása holland tejszínalapot és epret
  nevez meg; a hiányzó `tejszín` ízelemet pótoltuk.
- A Tatratea 62% Forest Fruit teljes neve, palackcímkéje és gyártói
  portfóliója erdei gyümölcsös tealikőrt igazol. A már helyes
  `erdei gyümölcs` mellé bekerült a hiányzó `tea`.
- A Zwack hivatalos St. Hubertus portfólióoldala a korábbi
  értelmezésnél pontosabb, elsődleges bizonyítékot adott. Az
  Eredeti változat narancsos és gyógynövényes, a St. Hubertus 33
  ánizst és narancsvirágot, az Erdei bodzát, szedret, borókát,
  zsályát és turbolyát, a Vérnarancs pedig vérnarancsot és
  gyógy-/fűszernövényes alapot tartalmaz.
- Az új gyártói bizonyíték miatt a korábbi, narancs nélküli
  St. Hubertus-megállapításokat kifejezetten helyesbítettük:
  a mostani tétel három érintett rekordja mellett **28 korábban
  ellenőrzött rekordot** is visszajavítottunk. Ez nem új
  termékellenőrzés, ezért az összesített előrehaladást nem növeli.
- Az eredeti Unicum 200 ml-es változatából eltávolítottuk a más
  változatból örökölt `narancs` értéket. Az Unicum Riserva
  termékneve és az azonos, korábban ellenőrzött változat a téves
  `natúr` helyett gyógynövényes profilt igazol.
- A Walden két méretének pontos termékadata legalább 5% növényi
  kivonatot közöl, ezért a téves `natúr` ízt `gyógynövény`
  értékre javítottuk.
- A két Sütő likőr azonos, korábban ellenőrzött változatának
  termékadata és címkéje rumos ízesítést igazol; mindkét
  `natúr` értéket `rum` értékre javítottuk.
- A Fütyülős teljes neve és közvetlen címkéje fekete cseresznyét
  és mézet nevez meg. A gyűjtő `cseresznye` helyére a két
  közvetlenül bizonyított ízelem került.
- A 401–425. tételben módosított rekord: **12**.
- A 401–425. tételben módosított tulajdonságmező: **12**.
- A 401–425. tételben változatlanul hagyott rekord: **13**
  (`ddee2d38ed6a6e0f6b74be74`, `b4a8d23b2e400f274bfe1f0c`,
  `66d7d75a37150b7208db9f58`, `1ea99fba0a682746896ef86c`,
  `62e285856baa75125b2f7f62`, `2180d6c6cdf225c64dd871f8`,
  `f40d476d5c353247faabaacb`, `629bc2c827dfe2ecb1d0b4ff`,
  `0c5ea715f4d4bf57a364df65`, `77e1e3f66288fde8b5511fbe`,
  `38358b7e7d44636d43e6fb18`, `1adef53e5a42f5f2199d50f0`,
  `6c4356de3cd54b7502f960a2`).
- Korábbi St. Hubertus-rekord helyesbítése: **28** rekord,
  **28** tulajdonságmező.
- Új megengedett érték: **5** (`íz: bodza`, `íz: boróka`,
  `íz: narancsvirág`, `íz: turbolya`, `íz: zsálya`).
- Törölt megengedett érték: **0**.
- A fa módosítása után, minden rekordcsere után és a végén is
  lefutott a 47 030 rekordos teljes validáció; eltérés nem maradt.

| Termékazonosító | A 401–425. tétel kézzel ellenőrzött módosításai |
|---|---|
| `6f17ed182b5a985c412ead3a` | íz `eper` → `eper, tejszín` |
| `fb1e9e73d0b4ba5a8cad82fb` | íz `erdei gyümölcs` → `erdei gyümölcs, tea` |
| `de2a699ad0b03a2138c39f4c` | íz `gyógynövény, narancs` → `gyógynövény` |
| `72aa6bd35e4aeed887f561c6` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `61470b917422987322738c76` | íz `gyógynövény` → `gyógynövény, narancs` |
| `41a8fef1c98a4afa9db69345` | íz `gyógynövény, narancs` → `bodza, boróka, gyógynövény, szeder, turbolya, zsálya` |
| `617686dea4a40da4d3dca4d4` | íz `natúr` → `gyógynövény` |
| `f2534aadd354787091ac39bb` | íz `natúr` → `gyógynövény` |
| `a7628169e9d758546bd5a8ef` | íz `natúr` → `gyógynövény` |
| `d2d060f23c269a1ed119abe6` | íz `natúr` → `rum` |
| `bea4e738bc904b3b3ed33946` | íz `natúr` → `rum` |
| `f98617323ab3a29786a7a540` | íz `cseresznye` → `fekete cseresznye, méz` |

| Termékazonosító | Új gyártói bizonyíték alapján helyesbített korábbi St. Hubertus-rekord |
|---|---|
| `67421:3604502` | íz `gyógynövény` → `gyógynövény, narancs` |
| `675107:4212497` | íz `gyógynövény` → `gyógynövény, narancs` |
| `674903:4212293` | íz `gyógynövény` → `ánizs, gyógynövény, narancsvirág` |
| `674900:4212290` | íz `erdei gyümölcs, gyógynövény` → `bodza, boróka, gyógynövény, szeder, turbolya, zsálya` |
| `674909:4212299` | íz `gyógynövény` → `gyógynövény, narancs` |
| `658836:4196226` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `674906:4212296` | íz `gyógynövény` → `gyógynövény, narancs` |
| `2813570` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `2806835` | íz `gyógynövény` → `gyógynövény, narancs` |
| `2806932` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `BTY-X16658300320021` | íz `gyógynövény` → `gyógynövény, narancs` |
| `BTY-X18414700320021` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `BTY-X17179300320021` | íz `gyógynövény` → `gyógynövény, narancs` |
| `BTY-X17179900320021` | íz `gyógynövény` → `gyógynövény, narancs` |
| `BTY-X18906100320021` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `BTY-X16295900320021` | íz `gyógynövény` → `gyógynövény, narancs` |
| `BTY-X17179500320021` | íz `gyógynövény` → `gyógynövény, narancs` |
| `BTY-X17179600320021` | íz `gyógynövény` → `ánizs, gyógynövény, narancsvirág` |
| `BTY-X17179700320021` | íz `gyógynövény` → `bodza, boróka, gyógynövény, szeder, turbolya, zsálya` |
| `BTY-X17180200320021` | íz `gyógynövény` → `gyógynövény, narancs` |
| `BTY-X17180300320021` | íz `gyógynövény` → `bodza, boróka, gyógynövény, szeder, turbolya, zsálya` |
| `BTY-X17192400320021` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `BTY-X18824100320021` | íz `gyógynövény, vérnarancs` → `gyógynövény, narancs, vérnarancs` |
| `BTY-X18824500320021` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `985632` | íz `gyógynövény` → `gyógynövény, narancs` |
| `82c85696b5ce3759841cb416` | íz `gyógynövény` → `ánizs, gyógynövény, narancsvirág` |
| `8675b412840ae31faa847b42` | íz `gyógynövény` → `gyógynövény, narancs` |
| `9a0559f0a8784f3e14f34d5c` | íz `gyógynövény` → `gyógynövény, narancs` |

### Likőr kézi felülvizsgálat, 426–450. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A három eredeti Jägermeister/Unicum rekord neve, címkéje és a
  korábban ellenőrzött azonos változatok csak a gyógynövényes
  profilt igazolják; a tévesen örökölt `narancs` elemet
  eltávolítottuk.
- A két Unicum Orange rekordnál a `keserűnarancs` nem külön
  bizonyított ízösszetevő, ezért az egyértelmű `narancs` maradt.
  A Jägermeister Orange az eredeti gyógynövényes likőr narancsos
  változata, így a hiányzó `gyógynövény` elemet pótoltuk.
- A Kick the Rules közvetlen címkéje és a pontos termékleírás
  eperrel, friss tejszínnel és tequilával készült krémlikőrt
  igazol. Az ízlistát mindhárom elemmel pontosítottuk, a fajtát
  pedig `gyümölcslikőr` helyett `krémlikőr` értékre javítottuk.
- A Lloyd Bitter és a két Bellora krémlikőr esetében nem találtunk
  olyan közvetlen, termékspecifikus összetevőbizonyítékot, amely a
  meglévő tulajdonságok bővítését indokolná; ezeket találgatás
  nélkül változatlanul hagytuk.
- Módosított rekord: **7**.
- Módosított tulajdonságmező: **8**.
- Változatlanul hagyott rekord: **18**
  (`32e1dea99d0df69343a0306b`, `fd7ab05328f8ffe512030e0f`,
  `f86e47fc7776c96b38b4d97b`, `639480c4ea87a82608969fe8`,
  `513755413490f44463da1f44`, `23598b819d0d9930cca69762`,
  `d4365c4fc4c6b47ca2b8b22b`, `128142d2f70f5dde49454cba`,
  `31db1c6618bcf30487799554`, `5e040c74a3acca428d771d97`,
  `e5167f8d3c59d62934223342`, `14cb02d5fdb9fa3ff4d5958d`,
  `1c84bb30a9385f6df91ea674`, `3becad9da8a23518c44fc431`,
  `15e4676f33f5e20a160ae906`, `c013007449d0d62e2a5e2ade`,
  `64e7caad5c424bb452344f98`, `26737e1c172280c2ca00bb9a`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `7127020b4e6375ab43235593` | íz `gyógynövény, narancs` → `gyógynövény` |
| `ca9a77669c18888c6e897b55` | íz `gyógynövény, narancs` → `gyógynövény` |
| `5b80820528fc07e613e032f7` | íz `gyógynövény, narancs` → `gyógynövény` |
| `aac31385e60aaf82d4d6288b` | íz `narancs, keserűnarancs` → `narancs` |
| `246348b24d6b8fd3e0d326d7` | íz `narancs` → `gyógynövény, narancs` |
| `826d5feb5f12b3757ca5f3f1` | íz `eper` → `eper, tejszín, tequila`; fajta `gyümölcslikőr` → `krémlikőr` |
| `4f64ec9d443778f6debc4874` | íz `narancs, keserűnarancs` → `narancs` |

### Likőr kézi felülvizsgálat, 451–475. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- Hat Jack Daniel's/Jim Beam rekord teljes neve, közvetlen címkéje
  és meglévő `whiskyalapú likőr` fajtája Tennessee whiskey-,
  illetve bourbonwhiskey-alapot igazol. A fahéj, méz és alma mellől
  hiányzó `whisky` ízelemet pótoltuk. A Jim Beam Black Cherry
  általános `cseresznye` értékét `fekete cseresznye` értékre is
  pontosítottuk.
- A Rézangyal teljes neve és címkéje mézes ágyas meggylikőrt, a
  Malibu teljes neve és címkéje kókuszos, fehér rum alapú likőrt
  igazol. A hiányzó `méz`, illetve `rum` ízelemet pótoltuk.
- A Baileys Original 500 ml-es változatánál az azonos, már
  ellenőrzött változatok és a gyártói termékadat alapján a tejszín
  mellé bekerült a hiányzó `whisky`.
- Az eredeti Unicum- és Jägermeister-változatoknál a más
  változatokból örökölt `narancs` elemeket eltávolítottuk, két
  pontatlan `natúr` értéket pedig `gyógynövény` értékre
  javítottunk. A St. Hubertus Eredeti ízlistáját a hivatalos
  portfólióadat szerinti `gyógynövény, narancs` értékre
  egészítettük ki.
- A Mátyás Classic azonos, korábban ellenőrzött változatának
  termékleírása gyógynövényes karaktert igazol, konkrét narancsot
  nem; az ízt ennek megfelelően `gyógynövény` értékre javítottuk.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **16**.
- Változatlanul hagyott rekord: **9**
  (`34fd927df5f074d177f6aeb6`, `203199219`, `203219276`,
  `220252723`, `220252724`, `220314998`, `121236257`,
  `121231994`, `121231683`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `77f82a633b7a5b6bdea6d93b` | íz `fahéj` → `fahéj, whisky` |
| `6152953b4749f22c0d00e249` | íz `méz` → `méz, whisky` |
| `57b1926260433002431e52d1` | íz `alma` → `alma, whisky` |
| `ab8555945a299030de8b32c2` | íz `méz` → `méz, whisky` |
| `e1d4f9fddb00fd450da4ab26` | íz `cseresznye` → `fekete cseresznye, whisky` |
| `70626ead82ce5e791c15be8c` | íz `alma` → `alma, whisky` |
| `eb53de17f62c62033ee29b0d` | íz `meggy` → `meggy, méz` |
| `db1cc03870ac0b141651f252` | íz `kókusz` → `kókusz, rum` |
| `203218620` | íz `natúr` → `gyógynövény` |
| `203218880` | íz `tejszín` → `tejszín, whisky` |
| `121220609` | íz `narancs` → `gyógynövény, narancs` |
| `121231735` | íz `gyógynövény, narancs` → `gyógynövény` |
| `121220535` | íz `gyógynövény, narancs` → `gyógynövény` |
| `121236672` | íz `narancs` → `gyógynövény` |
| `220145649` | íz `natúr` → `gyógynövény` |
| `121220828` | íz `gyógynövény, narancs` → `gyógynövény` |

### Likőr kézi felülvizsgálat, 476–500. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Mátyás gyártói webáruháza a Szilva, Meggy és Strong Coffee
  alapanyagaként fűszer- és gyógynövényeket is megnevez. A
  gyümölcs-, illetve kávéíz megtartása mellett mindhárom
  ízlistához pótoltuk a `gyógynövény` elemet.
- A Baileys hivatalos termékoldalai szerint a Tiramisu és a Salted
  Caramel az Original Irish Cream tejszínes-whiskys alapjával
  készül. A Tiramisu mascarponét, eszpresszót és csokoládés
  jegyeket is közöl; az ízlistákat csak ezekkel a közvetlenül
  igazolt elemekkel egészítettük ki.
- Az Angelli Cioccolato, Angelli Tiramisu és Mozart Gold azonos,
  korábban gyártói adatokkal ellenőrzött változatai alapján
  pótoltuk a hiányzó `mogyoró`, `tejszín` és `vanília`
  ízelemeket. Az Angelli Toffee fajtáját `krémlikőr` értékre
  javítottuk.
- A Tokaj Spirit Tiramisu pontos termékoldala és gyártói
  katalógusa holland tejszínt nevez meg, ezért a hiányzó
  `tejszín` bekerült. A Tokaj Spirit Csokoládé pontos oldala csak
  tojásallergént közöl, tejet nem; azt nem egészítettük ki
  feltételezett tejszínnel.
- A Jim Beam Black Cherry és Apple, valamint a Jack Daniel's Fire
  címkéje és fajtája a korábban ellenőrzött azonos változatokkal
  egyezően whiskyalapot igazol; pótoltuk a `whisky` elemet, a
  Black Cherry ízét pedig `fekete cseresznye` értékre
  pontosítottuk.
- A St. Hubertus Vérnarancs ízlistájához a hivatalos portfólióadat
  alapján bekerült a `gyógynövény`; az eredeti Jägermeister mini
  téves `narancs` értékét `gyógynövény` értékre javítottuk. A
  Malibu fajtája és címkéje szerint hiányzó `rum` elemet is
  pótoltuk.
- Módosított rekord: **16**.
- Módosított tulajdonságmező: **16**.
- Változatlanul hagyott rekord: **9**
  (`121220598`, `220043836`, `121220569`, `120056005`,
  `121220805`, `121220673`, `220314997`, `121228618`,
  `121221361`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121257860` | íz `szilva` → `gyógynövény, szilva` |
| `105012511` | íz `tiramisu` → `csokoládé, kávé, tejszín, tiramisu, whisky` |
| `121256481` | íz `kávé` → `gyógynövény, kávé` |
| `220311557` | íz `sós karamell` → `sós karamell, tejszín, whisky` |
| `121257877` | íz `meggy` → `gyógynövény, meggy` |
| `120184463` | íz `tiramisu` → `tejszín, tiramisu` |
| `120184475` | íz `csokoládé` → `csokoládé, mogyoró, tejszín` |
| `121227775` | íz `cseresznye` → `fekete cseresznye, whisky` |
| `210435652` | íz `csokoládé` → `csokoládé, tejszín, vanília` |
| `220222242` | íz `tiramisu` → `tejszín, tiramisu` |
| `121256498` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `121227695` | íz `alma` → `alma, whisky` |
| `121218475` | íz `fahéj` → `fahéj, whisky` |
| `220320737` | íz `narancs` → `gyógynövény` |
| `120184486` | fajta `egyéb likőr` → `krémlikőr` |
| `121228889` | íz `kókusz` → `kókusz, rum` |

### Likőr kézi felülvizsgálat, 501–525. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Jim Beam Honey és Peach, valamint a Jack Daniel's Apple teljes
  neve, címkéje és `whiskyalapú likőr` fajtája közvetlenül igazolja
  a hiányzó `whisky` elemet. A Fütyülős teljes neve és címkéje
  szerint az általános `cseresznye` értéket `fekete cseresznye`
  értékre pontosítottuk.
- A Baileys Chocolat Luxe gyártói adata ír tejszínt, ír whiskyt és
  belga csokoládét nevez meg; a csokoládé mellé pótoltuk a két
  hiányzó elemet. A Carolans gyártói tagsági terméklapja friss ír
  tejszínt, ír whiskyt és mézet igazol, ezért ott is kiegészült az
  ízlista.
- A St. Hubertus Erdei és 33 változatot a hivatalos
  portfólióleírás szerint javítottuk: az Erdei bodzát, szedret,
  borókát, zsályát, turbolyát és gyógynövényes alapot, a 33 pedig
  ánizst, narancsvirágot és gyógynövényes alapot kapott.
- Az eredeti Unicum 40 ml-es változatának más változatból örökölt
  `narancs` értékét `gyógynövény` értékre javítottuk.
- Módosított rekord: **9**.
- Módosított tulajdonságmező: **9**.
- Változatlanul hagyott rekord: **16**
  (`121221165`, `121220875`, `220335880`, `121257704`,
  `121231700`, `121228601`, `121256417`, `121220650`,
  `220335890`, `121221522`, `121221574`, `105001669`,
  `121221257`, `121271767`, `220336061`, `105001671`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121228221` | íz `méz` → `méz, whisky` |
| `121255787` | íz `őszibarack` → `őszibarack, whisky` |
| `121221234` | íz `cseresznye, méz` → `fekete cseresznye, méz` |
| `121218763` | íz `alma` → `alma, whisky` |
| `120404665` | íz `csokoládé` → `csokoládé, tejszín, whisky` |
| `121221551` | íz `gyógynövény, narancs` → `bodza, boróka, gyógynövény, szeder, turbolya, zsálya` |
| `121221655` | íz `gyógynövény, narancs` → `ánizs, gyógynövény, narancsvirág` |
| `220306686` | íz `narancs` → `gyógynövény` |
| `220335933` | íz `tejszín` → `méz, tejszín, whisky` |

### Likőr kézi felülvizsgálat, 526–550. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Jack Daniel's Tennessee Honey neve, címkéje és
  `whiskyalapú likőr` fajtája közvetlenül igazolja a hiányzó
  `whisky` elemet.
- A Cream Heroes Lily Cafetón pontos összetevőadata tejszínt,
  tequilát és kávéaromát közöl; a két utóbbi mellett pótoltuk a
  `tejszín` elemet. A Tokaj Spirit pisztáciás változatánál a pontos
  termékadat holland tejszínt, a Dubai változatnál csokoládét,
  pisztáciát és tejet igazol.
- A Baileys Toffee Popcorn pontos neve és gyártói termékadata a
  karamell mellett popcornt, ír tejszínt és ír whisky-alapot
  igazol. A Feeney's Dubai Chocolate Style pontos gyártói és
  összetevőadata friss ír tejszínt, ír malt whiskyt, csokoládés és
  pisztáciás karaktert közöl; mindkét ízlistát ennek megfelelően
  egészítettük ki.
- Az Unicum Orange Bitter neve és közvetlen címkéje narancspárlatot
  igazol, de külön `keserűnarancs` ízt nem; a redundáns, nem
  bizonyított elemet eltávolítottuk.
- A Di Vasco Amaretto közvetlen címkéje és termékforrása alapján a
  `Vascó` márkanevet `Di Vasco` értékre javítottuk. A régi értéket
  más likőrrekord nem használta, ezért a megengedett
  értékkészletből is töröltük.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **8**.
- Változatlanul hagyott rekord: **17**
  (`121228590`, `121256999`, `121228584`, `121255793`,
  `121232002`, `121229018`, `121221804`, `121221482`,
  `120661077`, `111221030`, `113130173`, `113130174`,
  `113130176`, `113130177`, `121229445`, `121231147`,
  `121231165`).
- Új megengedett érték: **1** (`Di Vasco` márka).
- Törölt megengedett érték: **1** (`Vascó` márka).
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121218550` | íz `méz` → `méz, whisky` |
| `121288074` | márka `Vascó` → `Di Vasco` |
| `105504686` | íz `kávé, tequila` → `kávé, tejszín, tequila` |
| `111221033` | íz `pisztácia` → `pisztácia, tejszín` |
| `111268297` | íz `csokoládé` → `csokoládé, pisztácia, tejszín` |
| `111269583` | íz `karamell` → `karamell, popcorn, tejszín, whisky` |
| `111270710` | íz `narancs, keserűnarancs` → `narancs` |
| `111275544` | íz `csokoládé` → `csokoládé, pisztácia, tejszín, whisky` |

### Likőr kézi felülvizsgálat, 551–575. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- Az Unicum Orange Bitter 500 ml-es változatánál a `Bitter` a
  keserűlikőr fajtát jelöli, ezért a külön nem igazolt,
  redundáns `keserűnarancs` ízelemet eltávolítottuk.
- A Jägermeister Orange 700 és 500 ml-es változata az eredeti
  gyógynövényes likőr narancsos kiadása; mindkettőnél pótoltuk a
  hiányzó `gyógynövény` elemet. A St. Hubertus Vérnarancs 700 és
  200 ml-es változatánál a teljes név és a gyártói portfólióadat
  ugyancsak gyógynövényes alapot igazol.
- A Tubi 60 gyártói ismertetője citrusféléket, gyógynövényeket,
  fűszereket, virág- és fakivonatokat nevez meg; a téves `natúr`
  értéket `citrus, fűszeres, gyógynövény` listára javítottuk.
- A Takamaka Koko gyártói termékoldala fehér rumot, tiszta
  kókuszkivonatot és vaníliás jegyeket igazol. A terméket
  `rumalapú likőr` fajtára pontosítottuk, ízlistáját pedig a
  hiányzó `rum` és `vanília` elemekkel egészítettük ki. A Malibu
  teljes neve és fajtája alapján szintén pótoltuk a hiányzó
  `rum` elemet.
- Módosított rekord: **8**.
- Módosított tulajdonságmező: **9**.
- Változatlanul hagyott rekord: **17**
  (`121256354`, `121270958`, `121276203`, `121301923`,
  `121306895`, `121315383`, `121315395`, `121315400`,
  `121315417`, `121315435`, `121315446`, `121315452`,
  `121355853`, `121357989`, `121358429`, `121358435`,
  `121358470`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121305781` | íz `narancs, keserűnarancs` → `narancs` |
| `121307681` | íz `narancs` → `gyógynövény, narancs` |
| `121321749` | íz `vérnarancs` → `gyógynövény, vérnarancs` |
| `121323908` | íz `natúr` → `citrus, fűszeres, gyógynövény` |
| `121324775` | íz `narancs` → `gyógynövény, narancs` |
| `121336369` | íz `kókusz` → `kókusz, rum, vanília`; fajta `egyéb likőr` → `rumalapú likőr` |
| `121341731` | íz `kókusz` → `kókusz, rum` |
| `121357845` | íz `vérnarancs` → `gyógynövény, vérnarancs` |

### Likőr kézi felülvizsgálat, 576–583. zárótétel

- Mind a 8 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Fütyülős fekete cseresznye teljes neve és címkéje alapján az
  általános `cseresznye` értéket `fekete cseresznye` értékre
  pontosítottuk; a méz igazolt elemként megmaradt.
- A Fütyülős kékáfonya neve és címkéje szó szerint a pontosabb
  `kékáfonya` értéket igazolja. Ezt új megengedett ízértékként
  felvettük, az általános `áfonya` értéket pedig más termékekhez
  megtartottuk.
- A csokis mogyoró közvetlen címkéje és pontos termékleírása
  pirított mogyorót, nem földimogyorót igazol; az ízlistát ennek
  megfelelően javítottuk.
- A Jim Beam Pineapple teljes neve, címkéje és gyártói termékadata
  Kentucky straight bourbon whiskeyvel készült ananászlikőrt
  igazol, ezért pótoltuk a hiányzó `whisky` elemet.
- Módosított rekord: **4**.
- Módosított tulajdonságmező: **4**.
- Változatlanul hagyott rekord: **4**
  (`121358510`, `121358556`, `121358585`, `121358625`).
- Új megengedett érték: **1** (`kékáfonya` íz).
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.
- Az akkori Likőr levél **583/583** rekordjának kézi felülvizsgálata
  lezárult. A később kézzel átsorolt hat rekorddal a jelenlegi
  állomány **589/589** ellenőrzött likőrrekordot tartalmaz.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121358591` | íz `cseresznye, méz` → `fekete cseresznye, méz` |
| `121358602` | íz `áfonya, méz` → `kékáfonya, méz` |
| `121358619` | íz `csokoládé, földimogyoró` → `csokoládé, mogyoró` |
| `121361004` | íz `ananász` → `ananász, whisky` |

### Egyéb szeszes ital kézi felülvizsgálat, 1–25. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- Az ouzo-, vodkaízű, whiskyalapú, rumalapú és brandyalapú
  szeszesitaloknál ellenőriztük, hogy az `Egyéb szeszes ital`
  besorolás a termék megnevezésének és alkoholtartalmának megfelel;
  egyik rekord sem indokolt átsorolást a tiszta párlatok közé.
- A brandy- és rumízű termékek `natúr` ízét a teljes névben
  szereplő, közvetlenül igazolt ízre javítottuk. A Mini Szilva
  címkéjén nem szerepel `Mini` márka, ezért `márka nélkül`
  értéket kapott; a Kunság Szilva címkéje pedig a
  `Kunság-Szesz` márkaalakot igazolja.
- A Ballantine's Brasil és Wild Cherry, Grant's Summer Orange,
  Stroh Jagertee, Captain Morgan Spiced Gold, Bacardi Caribbean
  Spiced, Kraken Black Spiced, Don Papa Baroko és Masskara
  pontos gyártói termékadatai alapján csak a közvetlenül
  bizonyított, elemi ízeket pótoltuk. A Jameson Orange gyártói
  adata a korábban ismeretlen alkoholtartalmat 30%-ként igazolja.
- Módosított rekord: **14**.
- Módosított tulajdonságmező: **14**.
- Változatlanul hagyott rekord: **11**
  (`533703`, `1055675`, `963083:4500473`, `963512:4500902`,
  `674519:4211909`, `674522:4211912`, `674990:4212380`,
  `674528:4211918`, `674525:4211915`, `712325:4249715`,
  `674594:4211984`).
- Új megengedett érték: **10** (`Kunság-Szesz`, `márka nélkül`
  márka; `brandy`, `chili`, `fahéj`, `kókusz`, `mandula`, `rum`,
  `szegfűszeg`, `szerecsendió` íz).
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `533696` | íz `natúr` → `brandy` |
| `566017` | márka `Mini` → `márka nélkül` |
| `684437:4221827` | íz `lime` → `lime, vanília` |
| `684449:4221839` | íz `cseresznye` → `cseresznye, mandula` |
| `785522:4322912` | íz `narancs` → `lime, narancs` |
| `748896:4286286` | alkoholtartalom `ismeretlen` → `30%` |
| `674516:4211906` | íz `natúr` → `rum` |
| `683834:4221224` | íz `tea` → `citrom, fahéj, narancs, szegfűszeg, tea, vanília` |
| `674987:4212377` | íz `fűszer` → `fűszer, vanília` |
| `712901:4250291` | íz `natúr` → `ananász, fahéj, kókusz, vanília` |
| `712517:4249907` | íz `fűszer` → `fahéj, fűszer, szerecsendió, vanília` |
| `874961:4412351` | íz `natúr` → `citrus, méz, vanília` |
| `849443:4386833` | íz `natúr` → `chili, citrus, lime` |
| `684368:4221758` | márka `Kunság` → `Kunság-Szesz` |

### Egyéb szeszes ital kézi felülvizsgálat, 26–50. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- Az Euphoria Cannabis Absinthe teljes neve és címkéje, valamint
  a gyártó 70%-os termékadata kannabiszos abszintot igazol; az
  ánizs mellé ezért pótoltuk a `kannabisz` elemet.
- A második Pilavas Ouzo rekord téves `natúr` ízét a termékfajta
  és az azonos, közvetlenül ellenőrzött termék alapján `ánizs`
  értékre javítottuk.
- A Jinro képe egyértelműen a 350 ml-es Strawberry változatot
  mutatja, a gyártói termékoldal pedig az eperízt és a 13%-os
  alkoholtartalmat is megerősíti; a téves `natúr` ízt `eper`
  értékre javítottuk.
- A két 22,5%-os Fütyülős teljes neve és címkéje mézzel készült
  barack-, illetve feketecseresznye-változatot igazol. Pótoltuk a
  `méz` elemet, az általános `cseresznye` értéket pedig
  `fekete cseresznye` értékre pontosítottuk.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **5**.
- Változatlanul hagyott rekord: **20**
  (`674591:4211981`, `1000888:4538278`, `684329:4221719`,
  `752214:4289604`, `674603:4211993`, `2813568`,
  `BTY-X17395100320021`, `BTY-X18326900320021`,
  `BTY-X17396200320021`, `BTY-X16652200320021`,
  `BTY-X17582000320021`, `BTY-X16650600320021`,
  `BTY-X16650800320021`, `BTY-X17394900320021`,
  `BTY-X17396100320021`, `BTY-X17582300320021`,
  `BTY-X16651100320021`, `BTY-X17542900320021`,
  `BTY-X17582200320021`, `BTY-X17399700320021`).
- Új megengedett érték: **2** (`fekete cseresznye`,
  `kannabisz` íz).
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `752217:4289607` | íz `ánizs` → `ánizs, kannabisz` |
| `3040626` | íz `natúr` → `ánizs` |
| `10106990` | íz `natúr` → `eper` |
| `BTY-X18891000320021` | íz `barack` → `barack, méz` |
| `BTY-X18891100320021` | íz `cseresznye` → `fekete cseresznye, méz` |

### Egyéb szeszes ital kézi felülvizsgálat, 51–75. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A teljes Fütyülős termékcsalád összevetése kimutatta, hogy öt
  22,5%-os Metro-rekord ugyanazon likőrök áruházfüggően eltérő
  besorolású másolata volt. A három mostani és a két előző tételbeli
  rekordot `Likőr` alá soroltuk, fajtájukat a már helyesen besorolt
  párjukkal egységesítettük, továbbá felvettük a kötelező
  `gyógynövényes: false` és megfelelő `egységnyi kiszerelés` mezőt.
- A Kalinka Barack 26%-os terméket a Kalinka Meggy azonos
  termékcsaládja és a gyártói webshop `likőr` alkohol típusa alapján
  szintén `Likőr` alá soroltuk. A Kalinka Ice gyártói összetevőadata
  csak vizet és gabonából készült finomszeszt közöl, ezért a `natúr`
  ízt megtartottuk, a téves `egyéb ízesített szeszesital` fajtát
  `vodkaízű szeszesital` értékre javítottuk.
- A Fütyülős Kékáfonya Mézzel ízét `kékáfonya, méz`, a Csokis
  Mogyoró földimogyoróját a közvetlen címke és az azonos termék
  alapján `mogyoró` értékre javítottuk. A Jinro Green Grape ízét
  `zöld szőlő` értékre pontosítottuk.
- Az Antonio Nadal gyártói termékoldala a Black Absinthe enyhe
  ánizsízét igazolja. A Ballantine's és Grant's gyártói termékadatai
  alapján pótoltuk a Brasil vaníliáját, a Wild manduláját és a
  Summer Orange lime-ját; a Captain Morgan Spiced Goldnál a
  fűszer mellé a vaníliát.
- A 25 most ellenőrzött rekordból módosított rekord: **11**.
- A 25 most ellenőrzött rekordban módosított tulajdonságmező:
  **21**; kézi kategória-átsorolás: **4**.
- Változatlanul hagyott rekord: **14**
  (`BTY-X2900700320021`, `BTY-X17636400320021`,
  `BTY-X17642400320021`, `BTY-X18044700320021`,
  `BTY-X18044800320021`, `BTY-X18044900320021`,
  `BTY-X18045000320021`, `BTY-X18970100320021`,
  `BTY-X18970200320021`, `BTY-X17395800320021`,
  `BTY-X17489000320021`, `BTY-X18317400320021`,
  `BTY-X18551000320021`, `BTY-X18423200320021`).
- Az előző tételből utólag egységesített rekord: **2**; ezeken
  módosított tulajdonságmező: **6**; kézi kategória-átsorolás:
  **2**.
- Új megengedett érték: **1** (`zöld szőlő` íz).
- Törölt megengedett érték: **1** (`fekete cseresznye` az
  Egyéb szeszes ital levélből; a Likőr levélben megmaradt).
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18891000320021` | kategória `Egyéb szeszes ital` → `Likőr`; fajta `gyümölcspárlat` → `gyümölcslikőr`; `gyógynövényes: false`; egységnyi kiszerelés `500 ml` |
| `BTY-X18891100320021` | kategória `Egyéb szeszes ital` → `Likőr`; fajta `gyümölcspárlat` → `gyümölcslikőr`; `gyógynövényes: false`; egységnyi kiszerelés `500 ml` |
| `BTY-X18891200320021` | kategória `Egyéb szeszes ital` → `Likőr`; íz `áfonya` → `kékáfonya, méz`; fajta `gyümölcspárlat` → `gyümölcslikőr`; `gyógynövényes: false`; egységnyi kiszerelés `500 ml` |
| `BTY-X18909900320021` | kategória `Egyéb szeszes ital` → `Likőr`; íz `csokoládé, földimogyoró` → `csokoládé, mogyoró`; fajta `gyümölcspárlat` → `csokoládélikőr`; `gyógynövényes: false`; egységnyi kiszerelés `500 ml` |
| `BTY-X18957100320021` | kategória `Egyéb szeszes ital` → `Likőr`; fajta `gyümölcspárlat` → `gyümölcslikőr`; `gyógynövényes: false`; egységnyi kiszerelés `500 ml` |
| `BTY-X18379800320021` | kategória `Egyéb szeszes ital` → `Likőr`; fajta `gyümölcsízű szeszesital` → `gyümölcslikőr`; `gyógynövényes: false`; egységnyi kiszerelés `200 ml` |
| `BTY-X17611100320021` | íz `szőlő` → `zöld szőlő` |
| `BTY-X17773100320021` | íz `natúr` → `ánizs` |
| `BTY-X18380000320021` | fajta `egyéb ízesített szeszesital` → `vodkaízű szeszesital` |
| `BTY-X17589400320021` | íz `lime` → `lime, vanília` |
| `BTY-X17628400320021` | íz `cseresznye` → `cseresznye, mandula` |
| `BTY-X18230500320021` | íz `narancs` → `lime, narancs` |
| `BTY-X17401700320021` | íz `fűszer` → `fűszer, vanília` |

### Egyéb szeszes ital kézi felülvizsgálat, 76–100. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
  A korábbi hat kézi Likőr-átsorolás miatt ezek a jelenlegi
  Egyéb szeszes ital levél 70–94. pozíciói, de az eredeti kézi
  ellenőrzési sorozat 76–100. tételei.
- A Bacardi Spiced gyártói ízprofilja a vanília, mandula, fahéj,
  szerecsendió és méz elemeket közvetlenül igazolja; ezt mind a
  négy azonos termékváltozaton egységesen rögzítettük.
- A Stroh gyártói termékadata a 80%-os változatnál a vanília,
  fahéj és mandula ízjegyeket igazolja. A Don Papa Masskara,
  Bacardi Caribbean Spiced és Captain Morgan Spiced Gold
  rekordokat az azonos, korábban már ellenőrzött termékcsalád
  bizonyítékaival egységesítettük.
- A két Casino teljes termékneve közvetlenül `Rum Ízesítésű`
  szeszesitalt jelöl, ezért a téves `natúr` ízt `rum` értékre
  javítottuk. A Koronás Tengerész termékeknél nem találtunk
  elég erős, termékspecifikus ízbizonyítékot, ezért azokat nem
  módosítottuk találgatással.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **12**.
- Változatlanul hagyott rekord: **13**
  (`BTY-X17401900320021`, `BTY-X7381600320021`,
  `BTY-X7381400320021`, `BTY-X16651000320021`,
  `BTY-X17508500320021`, `BTY-X17582400320021`,
  `BTY-X18551600320021`, `BTY-X9666000320021`,
  `02c2bfc4bcf0a97dd2da371c`, `e92e96bfe24251bff1a7c0cc`,
  `a845a2093ebb6e0ea558c03b`, `d5c1741ede2083f64593e66d`,
  `462ded626ed6c696de7ea349`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X17490400320021` | íz `fűszer` → `fahéj, mandula, méz, szerecsendió, vanília` |
| `BTY-X17490600320021` | íz `natúr` → `fahéj, mandula, méz, szerecsendió, vanília` |
| `BTY-X18358400320021` | íz `natúr` → `chili, citrus, lime` |
| `BTY-X17402200320021` | íz `fűszer` → `fűszer, vanília` |
| `BTY-X17396600320021` | íz `natúr` → `rum` |
| `BTY-X17396500320021` | íz `natúr` → `rum` |
| `BTY-X13160300320021` | íz `natúr` → `fahéj, mandula, vanília` |
| `BTY-X17616400320021` | íz `fűszer` → `ananász, fahéj, kókusz, vanília` |
| `BTY-X17640100320021` | íz `natúr` → `fahéj, mandula, vanília` |
| `BTY-X18559600320021` | íz `fűszer` → `fahéj, mandula, méz, szerecsendió, vanília` |
| `bc33fe46df68c712c4e39056` | íz `fűszer` → `fahéj, mandula, méz, szerecsendió, vanília` |
| `14420ca2d94bbf55d04a3e64` | íz `fűszer` → `fűszer, vanília` |

### Egyéb szeszes ital kézi felülvizsgálat, 101–125. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
  A korábbi hat Likőr-átsorolás miatt ezek a jelenlegi Egyéb
  szeszes ital levél 95–119. pozíciói.
- A Ballantine's Wild, Bacardi Spiced, Kraken Black Spiced és
  Captain Morgan Spiced Gold rekordokat az azonos, korábban már
  ellenőrzött termékcsaládok gyártói ízadataival egységesítettük.
- A Napoleon, Trois Tours, Portorico és Mariner termékek neve és
  olvasható címkéje nem bizonyít külön ízt. Ezeket az azonos,
  korábban már ellenőrzött rekordokkal összhangban változatlanul
  hagytuk; forráskategóriából vagy márkanévből nem következtettünk
  ízre.
- Módosított rekord: **5**.
- Módosított tulajdonságmező: **5**.
- Változatlanul hagyott rekord: **20**
  (`b3ffc00817fd94ce2745d669`, `183b12d4dba1ec22da362553`,
  `f283358aa4f080866831ef42`, `a8185b189d25d97adcd3451b`,
  `ae67d10626d0e574fe08bbde`, `397240c2d4339d0b386e2966`,
  `f0aec8f6122c4c0071e6be85`, `60f0eb5949aaff48dc29256d`,
  `8397a47fc6e30f9d77e351ba`, `6f6103751b846b19259d92a8`,
  `adebb7341f23ec7c6f39c14e`, `f53b4d99f41d6ebe3a0d6e29`,
  `03e62912d33eb387d0350e61`, `6628d412bf1e3acdaa7251cf`,
  `0b6b75392f8aa62d0794b7ba`, `e0807df15b65538b8a421362`,
  `d2b47f42c2826f609d787361`, `0c3ff9cc37168de80726ce7c`,
  `121236125`, `121221355`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `87befefbc64289083972194f` | íz `cseresznye` → `cseresznye, mandula` |
| `f7c3ad3fd08f465d4180355d` | íz `fűszer` → `fahéj, mandula, méz, szerecsendió, vanília` |
| `91fae1266c2d4e2cb8343a89` | íz `fűszer` → `fahéj, fűszer, szerecsendió, vanília` |
| `aa46b1d4e88f38c5ed5ecbe9` | íz `fűszer` → `fűszer, vanília` |
| `121220892` | íz `fűszer` → `fűszer, vanília` |

### Egyéb szeszes ital kézi felülvizsgálat, 126–150. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
  A korábbi hat Likőr-átsorolás miatt ezek a jelenlegi Egyéb
  szeszes ital levél 120–144. pozíciói.
- A Captain Morgan Spiced Gold, Bacardi Spiced, Stroh 80,
  Ballantine's Wild és Brasil, Grant's Summer Orange, valamint
  Don Papa Baroko és Masskara rekordokat az azonos, korábban már
  ellenőrzött termékcsaládok gyártói ízadataival egységesítettük.
- A két Kunság termék címkéjén közvetlenül a `Kunság-Szesz`
  márkaalak olvasható, ezért a márkát erre a már meglévő
  faértékre javítottuk.
- A Joe Rebel Wild Cherry és Sweet Honey forráskategóriája,
  címkéje és kereskedelmi termékcsaládja whiskyalapú italt
  bizonyít; mindkét téves fajtaértéket
  `whiskyalapú szeszesital` értékre javítottuk. Az ízeket a
  közvetlen Cherry és Honey jelölés alapján változatlanul hagytuk.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **12**.
- Változatlanul hagyott rekord: **13**
  (`121221205`, `121221787`, `121221499`, `220335882`,
  `121221286`, `220335885`, `121221827`, `121221620`,
  `121221171`, `220335881`, `220335884`, `121315918`,
  `121329735`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030 rekordos
  teljes validáció; eltérés nem maradt.
- Az eredeti Egyéb szeszes ital lista **150/150** rekordjának
  kézi felülvizsgálata lezárult. A Likőr alá kézzel átsorolt hat
  termék után a jelenlegi levél **144/144** ellenőrzött rekordot
  tartalmaz.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121220955` | íz `fűszer` → `fűszer, vanília` |
| `121218930` | íz `fűszer` → `fahéj, mandula, méz, szerecsendió, vanília` |
| `121228394` | íz `natúr` → `fahéj, mandula, vanília` |
| `121255689` | íz `cseresznye` → `cseresznye, mandula` |
| `121228751` | íz `lime` → `lime, vanília` |
| `121270964` | márka `Kunság` → `Kunság-Szesz` |
| `121270970` | márka `Kunság` → `Kunság-Szesz` |
| `121271410` | fajta `gyümölcsízű szeszesital` → `whiskyalapú szeszesital` |
| `121271427` | fajta `egyéb ízesített szeszesital` → `whiskyalapú szeszesital` |
| `121301917` | íz `narancs` → `lime, narancs` |
| `121327213` | íz `natúr` → `citrus, méz, vanília` |
| `121327225` | íz `natúr` → `chili, citrus, lime` |

### Koktél és előre kevert ital kézi felülvizsgálat, 1–25. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- Ellenőriztük az alkoholstátuszt, márkát, kiszerelést,
  alkoholtartalmat, alkoholalapot, koktélfajtát és
  szénsavasságot. A gin-tonikok, whisky-kólák, Breezer-változatok,
  Tropical palackos koktélok és MIX termékek mezői a névvel és
  címkével egyeznek.
- A Malibu Piña Colada 250 ml-es termékadata kifejezetten
  szénsavmentes, előre kevert koktélként azonosítja a terméket,
  ezért a `szénsavmentes` érték helyes. A Solevita alkoholmentes
  mojitónál a kép nem bizonyítja a szénsavasságot, ezért az
  `ismeretlen` értéket megtartottuk.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **25**
  (`748899:4286289`, `747410:4284800`, `751995:4289385`,
  `691136:4228526`, `691130:4228520`, `691139:4228529`,
  `684644:4222034`, `712958:4250348`, `672755:4210145`,
  `793109:4330499`, `712946:4250336`, `712952:4250342`,
  `712955:4250345`, `712949:4250339`, `677696:4215086`,
  `680189:4217579`, `680204:4217594`, `680192:4217582`,
  `64625:3601706`, `10101653`, `10107409`, `10107417`,
  `BTY-X17281900320021`, `BTY-X17284800320021`,
  `BTY-X17284900320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentes; az ellenőrzött
  25 azonosító mind a céllevélen maradt.

### Koktél és előre kevert ital kézi felülvizsgálat, 26–50. tétel

- Mind a 25 teljes rekordot és forrássort egyenként, közvetlenül
  ellenőriztük. Huszonkét termékhez helyi kép is tartozott, ezeket
  részletes felbontásban vizsgáltuk meg; három Le Coq rekordnál a
  teljes név, a forrássor és az azonos termékcsalád adta a
  közvetlen bizonyítékot.
- A MIX, Jack Daniel's, Jim Beam, Tatratea, Kalumba, Tanqueray,
  Le Coq, Tropical, Breezer, Old Tower és Professorado termékek
  alkoholstátusza, márkája, kiszerelése, alkoholtartalma,
  alkoholalapja, koktélfajtája és szénsavassága helyes.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **25**
  (`BTY-X17285000320021`, `BTY-X17486300320021`,
  `BTY-X17638800320021`, `BTY-X18304100320021`,
  `BTY-X18932700320021`, `BTY-X18932800320021`,
  `BTY-X18933000320021`, `BTY-X18957900320021`,
  `BTY-X17416300320021`, `BTY-X17415700320021`,
  `BTY-X17416200320021`, `BTY-X12145800320021`,
  `BTY-X17309300320021`, `BTY-X17415800320021`,
  `BTY-X17415900320021`, `BTY-X17416100320021`,
  `BTY-X17491100320021`, `BTY-X17491200320021`,
  `BTY-X17491300320021`, `BTY-X17529000320021`,
  `BTY-X17576500320021`, `BTY-X17598600320021`,
  `BTY-X18978500320021`, `BTY-X18978600320021`,
  `BTY-X18978700320021`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentes; az ellenőrzött
  25 azonosító mind a céllevélen maradt.

### Koktél és előre kevert ital kézi felülvizsgálat, 51–75. tétel

- Mind a 25 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A BITTER, Jack Daniel's, MIX, Jim Beam, Breezer,
  Chill&cheers, Le Coq és Lafi termékek alkoholstátusza, márkája,
  kiszerelése, alkoholtartalma, alkoholalapja, koktélfajtája és
  szénsavassága a terméknévvel és címkével egyezik.
- A Bubble Banks Alma-citrus-gyömbér pontos termékadata
  vodkaalapot, az összetevőlista pedig hozzáadott szén-dioxidot
  közöl, ezért az `alkoholalap` értéket `egyéb` helyett
  `vodka`, a `szénsavasság` értéket `ismeretlen` helyett
  `szénsavas` értékre javítottuk.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **2**.
- Változatlanul hagyott rekord: **24**
  (`BTY-X18978800320021`, `BTY-X17599900320021`, `1007129`,
  `1007132`, `1007140`, `33655165e905515e46bfc995`,
  `3c16bfd6dd2954ce5f67940b`, `436d5443e2d8b605c543079c`,
  `fd1a7c4caa171cc6da45a3e0`, `72e3f891ca0169bfd8508627`,
  `0bddefa57e1f92c276c327ae`, `3568e2139c7d464146a1ad04`,
  `2580f96fcf0217162a1bbbf3`, `4e59642eb0be1580f73de013`,
  `dbb94408a73134324e43129d`, `694e865348161b7f1c594649`,
  `121234576`, `121257508`, `121219854`, `121233975`,
  `121219059`, `121257405`, `121234582`, `121219071`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentes; az ellenőrzött
  25 azonosító mind a céllevélen maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `BTY-X18333200320021` | alkoholalap `egyéb` → `vodka`; szénsavasság `ismeretlen` → `szénsavas` |

### Koktél és előre kevert ital kézi felülvizsgálat, 76–100. tétel

- Mind a 25 teljes rekordot és forrássort egyenként,
  közvetlenül ellenőriztük. Huszonhárom használható helyi
  termékképet részletes felbontásban vizsgáltunk meg; a Three
  Sixty Vodka Lemon és Espresso Martini rekordhoz ugyanaz a
  „kép nem érhető el” helykitöltő volt bekötve, ezért ott a pontos
  termékadat szolgált közvetlen bizonyítékként.
- A Breezer, Jim Beam, MIX, Jack Daniel's, Le Coq, Beefeater,
  Jameson, Malibu, Kalumba, Tatratea, Three Sixty és Smirnoff
  termékek alkoholstátusza, márkája, kiszerelése,
  alkoholtartalma, alkoholalapja és koktélfajtája helyes.
- A Three Sixty Vodka Espresso Martini pontos összetevőlistája
  vizet, vodkát, kávélikőrt, cukrot és kávékivonatot sorol fel,
  szén-dioxidot nem. A gyártói klasszikus recept sem tartalmaz
  szénsavas összetevőt, ezért a `szénsavasság` értéket
  `ismeretlen` helyett `szénsavmentes` értékre javítottuk.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **24**
  (`121219088`, `121219128`, `121228325`, `121264436`,
  `121264442`, `121264459`, `121264465`, `121268375`,
  `121305591`, `121305602`, `121305619`, `121309495`,
  `121309517`, `121309523`, `121319511`, `121360132`,
  `121360149`, `121360184`, `121361010`, `121361027`,
  `121361177`, `121361183`, `121361505`, `121361575`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentes; az ellenőrzött
  25 azonosító mind a céllevélen maradt.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `121361195` | szénsavasság `ismeretlen` → `szénsavmentes` |

### Koktél és előre kevert ital kézi felülvizsgálat, 101–112. tétel

- Mind a 12 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A Captain Morgan, Tanqueray és MIX dobozos premixek mezői a
  közvetlen terméknévvel és címkével egyeznek. A Tropical
  palackos koktélok szénsavmentesek; a Night Orient Mojito és
  Spritz pezsgős zárású, szénsavas termék, míg a Piña Colada és
  Strawberry Margarita szénsavmentes.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **12**
  (`121361586`, `121361592`, `121361839`, `121361845`,
  `120183654`, `121235523`, `121235500`, `121235517`,
  `121276981`, `121277225`, `121276969`, `121277191`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentes; az ellenőrzött
  12 azonosító mind a céllevélen maradt.
- A Koktél és előre kevert ital levél **112/112** rekordjának
  kézi felülvizsgálata lezárult.

Az Alkoholos italok és alkoholmentes alternatívák ág valamennyi
jelenlegi levele és összesen **5 493/5 493** egyedi terméke kézzel
felülvizsgált.

### Pezsgőtabletta kézi felülvizsgálat, 1–8. tétel

- Mind a nyolc teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- Az Aqua Drop MIX, Forest Fruit, Raspberry és Lemon, valamint a
  három Waterdrop pezsgőkocka márkája, íze és vitaminjelölése a
  névvel és csomagolással egyezik. A „zero sugar” jelölésből nem
  következtettünk energiamentességre.
- Az `SPAR Aquadrop Ice Tea Peach` közvetlen neve és csomagolása
  az őszibarackízt is bizonyítja, ezért az `összetevő / íz`
  értéket `tea` helyett `tea, őszibarack` értékre javítottuk.
- Módosított rekord: **1**.
- Módosított tulajdonságmező: **1**.
- Változatlanul hagyott rekord: **7**
  (`d9772d1f89be796fb34ec9d0`, `e5b810005409b5c600008e20`,
  `763c43451b13eb805b5de259`, `aa8717e4a5f51bf5371c10de`,
  `105027674`, `111274365`, `111274368`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentes.
- A Pezsgőtabletta levél **8/8** rekordjának kézi
  felülvizsgálata lezárult.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `3435092401126e1473cb7b3c` | összetevő / íz `tea` → `tea, őszibarack` |

### Tejjel készítendő shake-por kézi felülvizsgálat, 1–6. tétel

- Mind a hat teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A két áruházban szereplő három azonos Dr. Oetker
  Snack&Shake-változatnál a csokoládé-, vanília- és málnaíz, a
  tejjel való elkészítés, a zab- és vitaminjelölés, valamint a
  málnás változat hozzáadottcukor-mentessége és
  édesítőszer-jelölése a közvetlen csomagolással egyezik.
- Módosított rekord: **0**.
- Módosított tulajdonságmező: **0**.
- Változatlanul hagyott rekord: **6**
  (`340b600da09ead538e6691cc`, `b16b51ddb1fd33c6dc930820`,
  `70bea15b6e26ebe2e729e339`, `111276034`, `111276035`,
  `111276036`).
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- A 47 030 rekordos teljes validáció hibamentes.
- A Tejjel készítendő shake-por levél **6/6** rekordjának kézi
  felülvizsgálata lezárult.

### Italpor kézi felülvizsgálat, 1–12. tétel

- Mind a 12 teljes rekordot és forrássort egyenként,
  közvetlenül ellenőriztük. Nyolc rekordhoz használható helyi
  kép is tartozott, ezeket részletes felbontásban vizsgáltuk meg;
  a négy Frutti Kendy Coop-rekordnál a pontos terméknév és
  termék-összetevőlista szolgált bizonyítékként.
- A Szobi termékek pontos leírása és összetevőlistája
  kristálycukrot, valamint aszpartámot, aceszulfám-K-t,
  nátrium-ciklamátot és nátrium-szacharinátot is közöl. Emiatt
  mind a nyolc Szobi rekordnál az `édesítőszert tartalmaz`
  mezőt `false` helyett `true` értékre javítottuk; a
  `hozzáadott cukor nélkül: false` érték helyes maradt.
- A Frutti Kendy termékcsalád összetevőlistája maltodextrint és
  több édesítőszert sorol fel, a tápérték 0 g cukrot, a
  termékleírás pedig cukormentességet közöl. Mind a négy
  rekordnál az `édesítőszert tartalmaz` és a `hozzáadott cukor
  nélkül` mezőt `false` helyett `true` értékre javítottuk.
- A `szamóca` ízű Szobi termékeket a meglévő `eper`
  szinonimaértéken tartottuk; nem vettünk fel párhuzamos,
  azonos jelentésű értéket.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **16**.
- Változatlanul hagyott rekord: **0**.
- Új megengedett érték: **0**.
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030
  rekordos teljes validáció; eltérés nem maradt.
- Az Italpor levél **12/12** rekordjának kézi felülvizsgálata
  lezárult.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `660585:4197975` | édesítőszert tartalmaz `false` → `true` |
| `660588:4197978` | édesítőszert tartalmaz `false` → `true` |
| `660591:4197981` | édesítőszert tartalmaz `false` → `true` |
| `660582:4197972` | édesítőszert tartalmaz `false` → `true` |
| `2799425` | hozzáadott cukor nélkül `false` → `true`; édesítőszert tartalmaz `false` → `true` |
| `2799424` | hozzáadott cukor nélkül `false` → `true`; édesítőszert tartalmaz `false` → `true` |
| `2799423` | hozzáadott cukor nélkül `false` → `true`; édesítőszert tartalmaz `false` → `true` |
| `2799422` | hozzáadott cukor nélkül `false` → `true`; édesítőszert tartalmaz `false` → `true` |
| `105013549` | édesítőszert tartalmaz `false` → `true` |
| `105013552` | édesítőszert tartalmaz `false` → `true` |
| `105013548` | édesítőszert tartalmaz `false` → `true` |
| `105013598` | édesítőszert tartalmaz `false` → `true` |

### Kombucha kézi felülvizsgálat, 1–14. tétel

- Mind a 14 teljes rekordot, forrássort és helyi termékképet
  egyenként, közvetlenül és részletes felbontásban ellenőriztük.
- A VIGO barack–citromfű termékénél a `citrom` érték egy hibás
  részszóegyezésből származott: a pontos gyártói terméknév és
  összetevőlista őszibarackot és citromfüvet, külön citromot nem
  igazol. Az `íz` listából ezért a `citrom` értéket eltávolítottuk.
- A Komvida Superglow rekord téves `menta` ízét a pontos Tesco-
  összetevőlista és a gyártói termékadat alapján `aloe vera`,
  `citrom`, `eper`, `goji`, `hibiszkusz`, `lime` értékekre
  javítottuk. A meglévő `íz` tulajdonsághoz a négy eddig hiányzó,
  közvetlenül igazolt atomi értéket (`aloe vera`, `eper`, `goji`,
  `lime`) felvettük.
- A VIGO pontos termékváltozatainak gyártói összetevőlistája
  szén-dioxidot közöl. A Komvida gyártói termékadat természetes
  szénsavat ír a palackos termékcsaládra. A Gutsy Captain pontos
  Tesco-termékoldalai a ZERO gyömbér–citrom, ZERO málna és
  őszibarack változatokat enyhén szénsavasnak nevezik és
  szén-dioxidot sorolnak fel; a limonádé gyártói oldala ugyanezt
  közli. A hiányzó `szénsavas` jelölést ennek megfelelően 12
  rekordnál `false` helyett `true` értékre javítottuk.
- A Carpe Diem Classic és a Gutsy Captain Original rekord
  szénsavassági jelölése már helyes volt.
- Módosított rekord: **12**.
- Módosított tulajdonságmező: **14**.
- Változatlanul hagyott rekord: **2**
  (`121362746`, `121311698`).
- Új megengedett érték: **4**
  (`íz`: `aloe vera`, `eper`, `goji`, `lime`).
- Törölt megengedett érték: **0**.
- Minden rekordcsere után és a végén is lefutott a 47 030
  rekordos teljes validáció; eltérés nem maradt.
- A Kombucha levél **14/14** rekordjának kézi felülvizsgálata
  lezárult.

| Termékazonosító | Kézzel ellenőrzött módosítások |
|---|---|
| `1011367:4548757` | íz `barack, citrom, citromfű` → `barack, citromfű`; szénsavas `false` → `true` |
| `1031633:4569023` | szénsavas `false` → `true` |
| `121313068` | íz `menta` → `aloe vera, citrom, eper, goji, hibiszkusz, lime`; szénsavas `false` → `true` |
| `121313108` | szénsavas `false` → `true` |
| `121313114` | szénsavas `false` → `true` |
| `121311715` | szénsavas `false` → `true` |
| `121311721` | szénsavas `false` → `true` |
| `121311681` | szénsavas `false` → `true` |
| `121311709` | szénsavas `false` → `true` |
| `121315642` | szénsavas `false` → `true` |
| `121315659` | szénsavas `false` → `true` |
| `121315665` | szénsavas `false` → `true` |

## Új kategória- vagy tulajdonságjavaslatok

Eddig nincs olyan javaslat, amely új kategóriát vagy új tulajdonságot
indokolna.

## Ellenőrzések

- Mindkét JSON újra beolvasható.
- Termékrekordok: **47 030**, összetett áruház–termékazonosító: **47 030
  egyedi**.
- `Ital` termékek: **12 455**.
- Alkoholos célág: **5 493** termék.
- Likőr: **589**; Egyéb szeszes ital: **144**; Koktél és előre
  kevert ital: **112**.
- Termékoldali, fában nem deklarált tulajdonság vagy érték: **0**.
- Alkoholos levelek pontos sémaeltérése: **0**.
- Hibás `kategoria_hash`: **0**.
- Bor-terméken maradt `kávé` íz: **0**.
- Validációs hibák: **0**.
