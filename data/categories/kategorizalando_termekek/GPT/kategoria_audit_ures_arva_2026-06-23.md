# Kategoria- es tulajdonsag-audit

Datum: 2026-06-23 08:55:16

Forrasok:
- `C:/Users/Bobo/Documents/GitHub/elelmeskosar2/data/categories/kategorizalando_termekek/GPT/kategoriak_2026-06-13.json`
- `C:/Users/Bobo/Documents/GitHub/elelmeskosar2/data/categories/kategorizalando_termekek/GPT/eredmeny.json`

Megjegyzes: a script csak olvasott; a JSON forrasfajlokat nem modositotta.

## Osszefoglalo

| Meres | Darab |
| --- | --- |
| Termekek | 47030 |
| Kategoriafa node-ok osszesen | 2151 |
| Termek nelkuli kategoria-node subtree szerint | 36 |
| Szerkezetileg ures kategoria-node | 41 |
| Tulajdonsag-deklaraciok osszesen | 13479 |
| Ures erteklistaju/skalaru tulajdonsag-deklaracio | 9 |
| Termekekben nem hasznalt tulajdonsag-deklaracio | 598 |
| Duplikalt erteket tartalmazo tulajdonsag-deklaracio | 375 |
| Kategoriat/tulajdonsagot/erteket erinto termekhibak osszesen | 19710 |
| Erintett termekek legalabb egy hibaval | 12777 |

## Kategoria-node uresseg

| Szint | Node osszesen | Subtree szerint termek nelkuli | Exact besorolas nelkuli | Szerkezetileg ures |
| --- | --- | --- | --- | --- |
| Fokategoria | 17 | 0 | 17 | 0 |
| Alkategoria | 302 | 13 | 189 | 9 |
| Altipus | 1832 | 23 | 23 | 32 |

### Termek nelkuli kategoria-node-ok mintak

| Kategoriaut | Szint | Subtree termek | Exact termek | Direkt tulajdonsag |
| --- | --- | --- | --- | --- |
| Alapanyag, sütés-főzés > Fűszer > Friss fűszernövény | 3 | 0 | 0 | 0 |
| Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Étkezési zsír (növényi) | 3 | 0 | 0 | 1 |
| Alapanyag, sütés-főzés > Rizs, köret > Galuska, nokedli (száraz) | 3 | 0 | 0 | 0 |
| Alapanyag, sütés-főzés > Rizs, köret > Burgonyaköret, hasáb | 3 | 0 | 0 | 0 |
| Baba > Tápszer > Anyatej-helyettesítő (1-es) | 3 | 0 | 0 | 0 |
| Baba > Bébi snack, keksz > Babapiskóta | 3 | 0 | 0 | 0 |
| Édesség, snack, rágcsálnivaló > Rágcsálnivaló magvak (snack) > Aszalt gyümölcs (snack) | 3 | 0 | 0 | 0 |
| Fagyasztott áruk > Jégkrém, fagylalt > Fagylalt (kimért) | 3 | 0 | 0 | 0 |
| Fagyasztott áruk > Fagyasztott zöldség > Zöldségfasírt, -pogácsa | 3 | 0 | 0 | 0 |
| Gyümölcs > Mix, vegyes | 2 | 0 | 0 | 0 |
| Gyümölcs > Egzotikus | 2 | 0 | 0 | 0 |
| Hús, hal, felvágott > Pulyka > Egész pulyka | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Pulyka > Pulyka aprólék | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Sertés > Sertésmáj | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Marha, borjú > Leveshús | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Nyúl, egyéb > Egész nyúl | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Vad > Egyéb vadhús | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Darált hús, fasírt > Gyros, csíkozott pecsenye | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Hal (friss, fagyasztott) > Panírozott hal, halrudacska | 3 | 0 | 0 | 0 |
| Hús, hal, felvágott > Egyéb hús, hal | 2 | 0 | 0 | 0 |
| Készétel > Kész köret | 2 | 0 | 0 | 0 |
| Mentes, speciális > Egyéb | 2 | 0 | 0 | 0 |
| Mentes, speciális > Paleo | 2 | 0 | 0 | 0 |
| Mentes, speciális > Paleo > Paleo liszt, sütőkeverék | 3 | 0 | 0 | 0 |
| Mentes, speciális > Paleo > Paleo édesség | 3 | 0 | 0 | 0 |
| Mentes, speciális > Paleo > Paleo tészta | 3 | 0 | 0 | 0 |
| Mentes, speciális > Paleo > Paleo snack | 3 | 0 | 0 | 0 |
| Pékáru > Zsemle > Hamburgerzsemle | 3 | 0 | 0 | 6 |
| Sütemény, desszert, torta > Rétes, pite, lepény | 2 | 0 | 0 | 1 |
| Tejtermékek és tojás > Tojás > Főtt / füstölt tojás | 3 | 0 | 0 | 0 |
| Zöldség > Borsófélék | 2 | 0 | 0 | 1 |
| Zöldség > Kelbimbó | 2 | 0 | 0 | 0 |
| Zöldség > Lencse | 2 | 0 | 0 | 1 |
| Zöldség > Sóska, spenót | 2 | 0 | 0 | 0 |
| Zöldség > Avokádó | 2 | 0 | 0 | 0 |
| Alkoholos ital > Égetett szesz | 2 | 0 | 0 | 0 |

### Hibas tulajdonsag-csoport szerkezetu node-ok

| Kategoriaut | Hiba |
| --- | --- |
| Gyümölcs > Áfonya > Áfonya | egyedi_not_dict |
| Gyümölcs > Alma > Red Jonaprince alma | egyedi_not_dict |
| Gyümölcs > Alma > Jonagored alma | egyedi_not_dict |
| Gyümölcs > Ananász > Ananász | egyedi_not_dict |
| Gyümölcs > Görögdinnye > Görögdinnye | egyedi_not_dict |
| Gyümölcs > Grapefruit > Grapefruit | egyedi_not_dict |
| Gyümölcs > Körte > Vilmos körte | egyedi_not_dict |
| Gyümölcs > Körte > Packhams körte | egyedi_not_dict |
| Gyümölcs > Lime > Lime | egyedi_not_dict |
| Gyümölcs > Kókuszdió > Kókuszdió | egyedi_not_dict |
| Zöldség > Káposzta > Kelkáposzta | egyedi_not_dict |
| Zöldség > Retekfélék > Jégcsapretek | egyedi_not_dict |
| Zöldség > Retekfélék > Vajretek | egyedi_not_dict |
| Háztartási termék > Takarítóeszköz > Felmosófej | egyedi_not_dict |
| Háztartási termék > Takarítóeszköz > Súroló | egyedi_not_dict |

## Tulajdonsagok uressege

| Meres | Darab |
| --- | --- |
| Osszes tulajdonsag-deklaracio | 13479 |
| Egyedi deklaracio | 4913 |
| Csoportos deklaracio | 8566 |
| Flag jellegu deklaracio | 2046 |
| Ures erteklistaju/skalaru deklaracio | 9 |
| Termekekben nem hasznalt deklaracio | 598 |
| Duplikalt ertekeket tartalmaz | 375 |

### Ures erteklistaju tulajdonsag-deklaraciok mintak

| Kategoriaut | Csoport | Tulajdonsag | Tipus | Termekhasznalat |
| --- | --- | --- | --- | --- |
| Ital > Bor > Fehérbor | egyedi | alkoholmentes | single | 0 |
| Ital > Bor > Vörösbor | egyedi | alkoholmentes | single | 0 |
| Ital > Alkoholok > Vermuth | egyedi | alkoholmentes | single | 0 |
| Pékáru > Kenyér > Kovászos kenyér | csoportos | szeletelt | multi | 1 |
| Pékáru > Kenyér > Toast kenyér | csoportos | szeletelt | multi | 7 |
| Pékáru > Kenyér > Szendvicskenyér | csoportos | szeletelt | multi | 1 |
| Pékáru > Kenyér > Gluténmentes kenyér | csoportos | szeletelt | multi | 4 |
| Pékáru > Kenyér > Gluténmentes kenyér | csoportos | gluténmentes | multi | 14 |
| Pékáru > Croissant > Croissant | csoportos | töltött | multi | 52 |

### Nem hasznalt tulajdonsag-deklaraciok mintak

| Kategoriaut | Csoport | Tulajdonsag | Tipus | Ertekek |
| --- | --- | --- | --- | --- |
| Alapanyag, sütés-főzés > Cukor, édesítőszer | egyedi | márka | single | 35 |
| Alapanyag, sütés-főzés > Cukor, édesítőszer | csoportos | terméktípus | multi | 15 |
| Alapanyag, sütés-főzés > Étkezési só, ételízesítő | egyedi | márka | single | 23 |
| Alapanyag, sütés-főzés > Fűszer | egyedi | márka | single | 38 |
| Alapanyag, sütés-főzés > Olaj, ecet, zsiradék | egyedi | márka | single | 61 |
| Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Étkezési zsír (növényi) | csoportos | zsiradék típusa | multi | 4 |
| Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Állati zsiradék | csoportos | zsiradék típusa | multi | 4 |
| Alapanyag, sütés-főzés > Hüvelyesek | egyedi | márka | single | 16 |
| Alapanyag, sütés-főzés > Hüvelyesek > Csicseriborsó | csoportos | forma | multi | 1 |
| Alapanyag, sütés-főzés > Sütési alapanyag | egyedi | hűtött | flag | 0 |
| Alapanyag, sütés-főzés > Sütési alapanyag | csoportos | jelleg | multi | 6 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | egyedi | márka | single | 94 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | alapanyag | multi | 79 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | terméktípus | multi | 5 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | forma | multi | 20 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | csomagolás | multi | 8 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | kiszerelés | multi | 2 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | jelleg | multi | 11 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | ízesítés | multi | 22 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | fajta | multi | 14 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt | csoportos | töltelék | multi | 6 |
| Alapanyag, sütés-főzés > Olajos magvak, aszalt gyümölcs (natúr, sütéshez-főzéshez) | egyedi | bio | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | hozzáadott cukor nélkül | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | protein / magas fehérje | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | instant | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | bio | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | gluténmentes | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | édesítőszerrel | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | csökkentett cukortartalmú | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | egyedi | márka | single | 34 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | csoportos | alap | multi | 19 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | csoportos | íz / hozzáadott | multi | 68 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli | csoportos | forma | multi | 16 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Kukoricapehely (cornflakes) | csoportos | alapanyag | multi | 7 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Müzli, granola | csoportos | alapanyag | multi | 7 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Müzli, granola | csoportos | jellemzők | multi | 7 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | egyedi | cukormentes / hozzáadott cukor nélkül | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | egyedi | laktózmentes | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | egyedi | teljes kiőrlésű | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | egyedi | rostban gazdag | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | egyedi | töltött | flag | 0 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | csoportos | jellemző | multi | 8 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | csoportos | jellemzők | multi | 7 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Instant kása | egyedi | hozzáadott cukor nélkül | flag | 0 |
| Baba | egyedi | bio | flag | 0 |
| Baba | egyedi | hozzáadott cukor nélkül | flag | 0 |
| Baba | egyedi | márka | single | 2 |
| Baba | csoportos | életkor | multi | 10 |
| Baba > Bébiétel, bébimenü (sós) | egyedi | hűtött | flag | 0 |
| Baba > Bébiétel, bébimenü (sós) | egyedi | bio | flag | 0 |
| Baba > Bébiétel, bébimenü (sós) | egyedi | márka | single | 1 |
| Baba > Bébiétel, bébimenü (sós) | csoportos | fő alapanyag | multi | 16 |
| Baba > Bébiétel, bébimenü (sós) | csoportos | hús / fehérje | multi | 8 |
| Baba > Bébiétel, bébimenü (sós) | csoportos | állag | multi | 4 |
| Baba > Gyümölcspüré, bébidesszert | egyedi | tejalapú | flag | 0 |
| Baba > Gyümölcspüré, bébidesszert | egyedi | hűtött | flag | 0 |
| Baba > Gyümölcspüré, bébidesszert | egyedi | bio | flag | 0 |
| Baba > Gyümölcspüré, bébidesszert | egyedi | márka | single | 2 |
| Baba > Gyümölcspüré, bébidesszert | csoportos | fő alapanyag | multi | 19 |
| Baba > Gyümölcspüré, bébidesszert | csoportos | állag | multi | 5 |
| Baba > Tejpép, gabonapép, kása | egyedi | tejmentes | flag | 0 |
| Baba > Tejpép, gabonapép, kása | egyedi | tejalapú | flag | 0 |
| Baba > Tejpép, gabonapép, kása | csoportos | gabona | multi | 7 |
| Baba > Tejpép, gabonapép, kása | csoportos | íz | multi | 7 |
| Baba > Tejpép, gabonapép, kása | csoportos | állag | multi | 4 |
| Baba > Tápszer | egyedi | tejalapú | flag | 0 |
| Baba > Tápszer | csoportos | fokozat | multi | 6 |
| Baba > Tápszer | csoportos | speciális jelleg | multi | 6 |
| Baba > Tápszer | csoportos | állag | multi | 3 |
| Baba > Bébi snack, keksz | csoportos | íz | multi | 8 |
| Baba > Bébiital, víz | csoportos | íz | multi | 8 |
| Baba > Bébiital, víz | csoportos | állag | multi | 3 |
| Édesség, snack, rágcsálnivaló > Csokoládé | egyedi | márka | single | 88 |
| Édesség, snack, rágcsálnivaló > Csokoládé | csoportos | típus | multi | 5 |
| Édesség, snack, rágcsálnivaló > Csokoládé | csoportos | töltelék / íz | multi | 125 |
| Édesség, snack, rágcsálnivaló > Csokoládé > Csokoládé szelet | egyedi | édesítőszeres | flag | 0 |
| Édesség, snack, rágcsálnivaló > Keksz, nápolyi, ostya | egyedi | teljes kiőrlésű | flag | 0 |
| Édesség, snack, rágcsálnivaló > Keksz, nápolyi, ostya | egyedi | rostban gazdag | flag | 0 |
| Édesség, snack, rágcsálnivaló > Keksz, nápolyi, ostya | egyedi | cukormentes / hozzáadott cukor nélkül | flag | 0 |
| Édesség, snack, rágcsálnivaló > Keksz, nápolyi, ostya | egyedi | gluténmentes | flag | 0 |

## Termekek nem illeszkedo adatai

| Hibatipus | Elofordulas | Erintett termek |
| --- | --- | --- |
| property_value_not_allowed | 10222 | 6447 |
| property_shape_mismatch | 9327 | 8432 |
| property_has_no_allowed_values | 79 | 75 |
| missing_altipus | 76 | 76 |
| missing_alkategoria | 4 | 4 |
| property_not_declared_for_category | 2 | 2 |

### Hianyzo kategoriautak

| Hiba | Termek kategoriaut | Darab |
| --- | --- | --- |
| missing_altipus | Készétel > Saláta, hidegtál > Saláta, hidegtál | 31 |
| missing_altipus | Készétel > Friss töltött tészta, gnocchi > Friss töltött tészta, gnocchi | 20 |
| missing_altipus | Készétel > Szendvicskrém, hummusz, pástétom > Szendvicskrém, hummusz, pástétom | 15 |
| missing_altipus | Készétel > Kész szendvics > Kész szendvics | 7 |
| missing_alkategoria | Alapanyag, sütés-főzés > Szendvicskrém, hummusz, kenőkrém | 4 |
| missing_altipus | Készétel > Egyéb főétel, melegétel > Egyéb főétel, melegétel | 2 |
| missing_altipus | Alapanyag, sütés-főzés > Sütési alapanyag > Vaníliás cukor, sütőcukor | 1 |

### Kategoriaban nem deklaralt termek-tulajdonsagok

| Kategoriaut | Tulajdonsag | Darab |
| --- | --- | --- |
| Hús, hal, felvágott > Vad > Vaddisznó | pácolt / fűszerezett | 1 |
| Hús, hal, felvágott > Halkészítmény > Füstölt hal | bőrös | 1 |

### Nem engedelyezett vagy erteklista nelkuli termek-tulajdonsagertekek

| Kategoriaut | Tulajdonsag | Ertek | Darab |
| --- | --- | --- | --- |
| Ital > Pezsgő > Pezsgő | alkoholtartalom | alkoholos | 145 |
| Fagyasztott áruk > Jégkrém, fagylalt > Dobozos, családi jégkrém | kiszerelés | tégely | 92 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Virsli, debreceni | forma | pár | 88 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Főző-, grillkolbász | forma | pár | 88 |
| Ital > Ásványvíz > Szénsavmentes ásványvíz | szénsavasság | mentes | 74 |
| Fagyasztott áruk > Jégkrém, fagylalt > Pálcikás, tölcséres jégkrém | kiszerelés | zacskó | 68 |
| Fagyasztott áruk > Jégkrém, fagylalt > Tégelyes prémium jégkrém | kiszerelés | tégely | 65 |
| Pékáru > Croissant > Croissant | töltött | True | 51 |
| Alapanyag, sütés-főzés > Instant ételek, alapok > Ételalap, fix por | kiszerelés | tasak | 45 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Puffasztott gabona | kiszerelés | doboz | 42 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Majonéz | csípősség | csemege | 38 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | kiszerelés | üveg | 37 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Párizsi, felvágott | csomagolás | rúd / darabos | 35 |
| Tejtermékek és tojás > Sajt > Félkemény sajt | márka | Milsani | 33 |
| Hús, hal, felvágott > Pástétom, húskrém > Húskrém, kenhető | csomagolás | konzerv | 32 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt > Olívabogyó, kapribogyó, eltett zöldség | kiszerelés | üveg | 30 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | kiszerelés | flakon | 29 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Egyéb hideg szósz, dip | alap | chili | 28 |
| Alapanyag, sütés-főzés > Fűszer > Fűszersó, pác | kiszerelés | tasak | 28 |
| Alapanyag, sütés-főzés > Lekvár, méz, édes krém > Mogyorókrém, csokikrém (Nutella jellegű) | édesítés | cukorral | 27 |
| Zöldség > Csomagolt saláta, salátatál | kiszerelés | csomagolt | 27 |
| Ital > Kávé, tea, kakaó (száraz) > Kapszulás kávé | kiszerelés | 10 db | 27 |
| Édesség, snack, rágcsálnivaló > Rágógumi > Szálas rágógumi | forma | lap / szálas | 26 |
| Tejtermékek és tojás > Sajt > Kemény sajt | kiszerelés | tasak | 26 |
| Hús, hal, felvágott > Pástétom, húskrém > Májpástétom | kiszerelés | tégely | 26 |
| Ital > Kávé, tea, kakaó (száraz) > Őrölt kávé | kiszerelés | 250 g | 26 |
| Fagyasztott áruk > Jégkrém, fagylalt > Jégkrém multipack, válogatás | márka | Auchan Kedvenc | 25 |
| Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | kiszerelés | tasak | 25 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Müzli, granola | kiszerelés | tasak | 25 |
| Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | csípősség | nem csípős | 24 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Majonéz | kiszerelés | flakon | 24 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Húsos snack, szárított (kabanos, baromfirúd) | csomagolás | zacskó | 24 |
| Hús, hal, felvágott > Pástétom, húskrém > Húskrém, kenhető | kiszerelés | konzerv | 24 |
| Zöldség > Csomagolt saláta, salátatál | feldolgozottság | mosott | 22 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Szalámi | csomagolás | rúd / darabos | 22 |
| Készétel > Kész saláta > Majonézes / joghurtos kész saláta | márka | márka nélkül | 22 |
| Alapanyag, sütés-főzés > Fűszer > Bors, chili | kiszerelés | tasak | 21 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Torma | kiszerelés | üveg | 21 |
| Fagyasztott áruk > Fagyasztott zöldség > Hasábburgonya, burgonyatermék | ízesítés | natúr | 21 |
| Tejtermékek és tojás > Sajt > Grillsajt / halloumi / sütnivaló | forma | tömb | 21 |
| Tejtermékek és tojás > Sajt > Grillsajt / halloumi / sütnivaló | kiszerelés | vákuumcsomagolt | 21 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Grill / BBQ szósz | konyha / stílus | BBQ | 21 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt > Savanyúság (uborka, csalamádé, vegyes) | márka | Auchan | 21 |
| Alapanyag, sütés-főzés > Étkezési só, ételízesítő > Só | kiszerelés | zacskó | 20 |
| Tejtermékek és tojás > Joghurt > Gyümölcsös/ízesített joghurt | márka | Milsani | 20 |
| Tejtermékek és tojás > Sajt > Ömlesztett sajt | kiszerelés | tálca | 20 |
| Alapanyag, sütés-főzés > Fűszer > Fűszerkeverék | kiszerelés | tasak | 19 |
| Fagyasztott áruk > Fagyasztott zöldség > Zöldségkeverék | zöldség | zöldségmix | 19 |
| Tejtermékek és tojás > Tojás > Tyúktojás | tartás | egyéb | 19 |
| Tejtermékek és tojás > Sajt > Grillsajt / halloumi / sütnivaló | fajta | egyéb | 19 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Paprikakrém, darált paprika | márka | Univer | 19 |
| Készétel > Kész saláta > Majonézes / joghurtos kész saláta | márka | SPAR Enjoy | 19 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Pesto | kiszerelés | üveg | 18 |
| Hús, hal, felvágott > Csirke > Csirkemell | GMO-mentes | False | 18 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Sonka | ízesítés | füstölt | 18 |
| Tejtermékek és tojás > Joghurt > Krémjoghurt | kiszerelés | pohár | 18 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | íz | klasszikus | 18 |
| Alapanyag, sütés-főzés > Sütési alapanyag > Aroma, kivonat, vaníliarúd | kiszerelés | üveg | 17 |
| Alapanyag, sütés-főzés > Sütési alapanyag > Zselatin, habfixáló, tortazselé | kiszerelés | tasak | 17 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Húsos snack, szárított (kabanos, baromfirúd) | forma | snack rúd | 17 |
| Tejtermékek és tojás > Tojás > Tyúktojás | kiszerelés | doboz | 17 |
| Tejtermékek és tojás > Tejdesszert, puding > Tejberizs | márka | Müller | 17 |
| Hús, hal, felvágott > Növényi húspótló > Tofu, seitan, tempeh | forma | egyéb | 17 |
| Fagyasztott áruk > Jégkrém, fagylalt > Dobozos, családi jégkrém | márka | Auchan Kedvenc | 17 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Sonka | kiszerelés | 90 g | 17 |
| Fagyasztott áruk > Jégkrém, fagylalt > Pálcikás, tölcséres jégkrém | kiszerelés | 120 ml | 17 |
| Fagyasztott áruk > Jégkrém, fagylalt > Dobozos, családi jégkrém | kiszerelés | 825 ml | 17 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | kiszerelés | üveg | 16 |
| Hús, hal, felvágott > Pástétom, húskrém > Májpástétom | csomagolás | konzerv | 16 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Száraz kolbász | forma | pár | 16 |
| Fagyasztott áruk > Fagyasztott hal, tengeri áru > Halrudacska | ízesítés | natúr | 16 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Mustár | kiszerelés | üveg | 15 |
| Fagyasztott áruk > Jégkrém, fagylalt > Jégkrém multipack, válogatás | márka | Mucci | 15 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Grill / BBQ szósz | íz | BBQ | 15 |
| Alapanyag, sütés-főzés > Fűszer > Fűszersó, pác | márka | SunCity Spices | 15 |
| Alapanyag, sütés-főzés > Instant ételek, alapok > Instant tészta, burgonyapüré | márka | Vifon | 15 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt > Savanyúság (uborka, csalamádé, vegyes) | kiszerelés | vödör | 15 |
| Hús, hal, felvágott > Pástétom, húskrém > Húskrém, kenhető | alap | zöldség | 15 |
| Fagyasztott áruk > Jégkrém, fagylalt > Dobozos, családi jégkrém | kiszerelés | 900 ml | 15 |
| Fagyasztott áruk > Jégkrém, fagylalt > Tégelyes prémium jégkrém | kiszerelés | 500 ml | 15 |
| Tejtermékek és tojás > Sajt > Kemény sajt | forma | gerezd | 14 |
| Tejtermékek és tojás > Sajt > Kemény sajt | kiszerelés | tálca | 14 |
| Gyümölcs > Alma | kiszerelés | lédig | 14 |
| Alapanyag, sütés-főzés > Fűszer > Salátaöntet-por | forma | por | 14 |
| Tejtermékek és tojás > Tojás > Tyúktojás | GMO-mentes | False | 14 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Száraz kolbász | ízesítés | vastagkolbász | 14 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Száraz kolbász | csomagolás | rúd / darabos | 14 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Sonka | forma | tömb | 14 |
| Alapanyag, sütés-főzés > Fűszer > Nemzetközi fűszerkeverék | kiszerelés | tasak | 14 |
| Pékáru > Kenyér > Gluténmentes kenyér | gluténmentes | True | 14 |
| Ital > Szörp, italkoncentrátum > Italkoncentrátum | kiszerelés | 440 ml | 14 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Mustár | kiszerelés | flakon | 13 |
| Alapanyag, sütés-főzés > Instant ételek, alapok > Instant leves | márka | Le Gusto | 13 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Müzli, granola | kiszerelés | doboz | 13 |
| Fagyasztott áruk > Fagyasztott zöldség > Hasábburgonya, burgonyatermék | kiszerelés | zacskó | 13 |
| Fagyasztott áruk > Jégkrém, fagylalt > Pálcikás, tölcséres jégkrém | kiszerelés | egyéb | 13 |
| Hús, hal, felvágott > Növényi húspótló > Tofu, seitan, tempeh | csomagolás | vákuumcsomagolt | 13 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Egyéb hideg szósz, dip | alap | fokhagyma | 13 |
| Tejtermékek és tojás > Sajt > Félkemény sajt | márka | Auchan Kedvenc | 13 |
| Fagyasztott áruk > Fagyasztott hal, tengeri áru > Halrudacska | halfajta | tőkehal | 13 |
| Alapanyag, sütés-főzés > Sütési alapanyag > Friss leveles, rétes- és linzertészta | kiszerelés | tasak | 13 |
| Ital > Ásványvíz > Enyhén szénsavas ásványvíz | szénsavasság | enyhén szénsavas | 13 |
| Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | 12 |
| Fagyasztott áruk > Fagyasztott panírozott (nem hús) > Rántott sajt | ízesítés | natúr | 12 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Sonka | ízesítés | kemencés sült | 12 |
| Tejtermékek és tojás > Joghurt > Skyr / proteinjoghurt | kiszerelés | pohár | 12 |
| Tejtermékek és tojás > Joghurt > Natúr joghurt | zsírtartalom | teljes | 12 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Főző-, grillkolbász | ízesítés | egyéb | 12 |
| Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Egyéb hideg szósz, dip | kiszerelés | üveg | 12 |
| Fagyasztott áruk > Fagyasztott zöldség > Zöldségkeverék | ízesítés | natúr | 12 |
| Fagyasztott áruk > Jégkrém, fagylalt > Dobozos, családi jégkrém | márka | Gelatiamo | 12 |
| Alapanyag, sütés-főzés > Instant ételek, alapok > Instant tészta, burgonyapüré | márka | Knorr | 12 |
| Hús, hal, felvágott > Pástétom, húskrém > Májpástétom | kiszerelés | konzerv | 12 |
| Hús, hal, felvágott > Felvágottak, húskészítmény > Virsli, debreceni | kiszerelés | 140 g | 12 |
| Fagyasztott áruk > Jégkrém, fagylalt > Tégelyes prémium jégkrém | kiszerelés | 460 ml | 12 |
| Ital > Kávé, tea, kakaó (száraz) > Kakaó / Vanília / Egyéb | típus | édesített kakaópor | 11 |
| Alapanyag, sütés-főzés > Instant ételek, alapok > Instant tészta, burgonyapüré | kiszerelés | tasakos | 11 |
| Alapanyag, sütés-főzés > Konzerv, savanyúság, befőtt > Savanyúság (uborka, csalamádé, vegyes) | márka | King's Crown | 11 |
| Alapanyag, sütés-főzés > Lekvár, méz, édes krém > Lekvár, dzsem | márka | Grandessa | 11 |
| Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Müzliszelet, gyümölcsszelet | márka | Golden Bridge | 11 |

### Termekhiba mintak

| Hiba | Index | Kategoriaut | Tulajdonsag | Ertek | Termek |
| --- | --- | --- | --- | --- | --- |
| property_value_not_allowed | 0 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | kiszerelés | üveg | BEN'S ORIGINAL Édes savanyú mártás ananásszal, 400g |
| property_value_not_allowed | 0 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | íz | egyéb | BEN'S ORIGINAL Édes savanyú mártás ananásszal, 400g |
| property_value_not_allowed | 0 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | alap | gyümölcs | BEN'S ORIGINAL Édes savanyú mártás ananásszal, 400g |
| property_value_not_allowed | 1 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | kiszerelés | üveg | BEN'S ORIGINAL Édes-savanyú mártás, 400 g |
| property_value_not_allowed | 1 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | íz | egyéb | BEN'S ORIGINAL Édes-savanyú mártás, 400 g |
| property_value_not_allowed | 1 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | alap | gyümölcs | BEN'S ORIGINAL Édes-savanyú mártás, 400 g |
| property_value_not_allowed | 2 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ázsiai / wok szósz | kiszerelés | üveg | BEN'S ORIGINAL Csípős szecsuáni mártás, 400 g |
| property_shape_mismatch | 4 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | kiszerelés | üveg | LYTTOS Görög olívaolaj, extraszűz, 500 ml |
| property_value_not_allowed | 4 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | kiszerelés | üveg | LYTTOS Görög olívaolaj, extraszűz, 500 ml |
| property_value_not_allowed | 4 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | márka | Lyttos | LYTTOS Görög olívaolaj, extraszűz, 500 ml |
| property_shape_mismatch | 5 | Ital > Kávé, tea, kakaó (száraz) > Kakaó / Vanília / Egyéb | típus | édesített kakaópor | NESQUIK Kakaóitalpor, 800 g |
| property_value_not_allowed | 5 | Ital > Kávé, tea, kakaó (száraz) > Kakaó / Vanília / Egyéb | típus | édesített kakaópor | NESQUIK Kakaóitalpor, 800 g |
| property_value_not_allowed | 6 | Alapanyag, sütés-főzés > Fűszer > Őrölt / egész fűszer | márka | Le Gusto | LE GUSTO Fokhagyma granulátum, 30 g |
| property_value_not_allowed | 7 | Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | márka | Enjoy Free! | ENJOY FREE! Vörösáfonyás - meggyes zabkása, hozzáadott cukor nélkül, vegán, 65 g |
| property_value_not_allowed | 7 | Alapanyag, sütés-főzés > Gabonapehely, reggeli müzli > Zabkása, zabpehely | íz / hozzáadott | vörös áfonya | ENJOY FREE! Vörösáfonyás - meggyes zabkása, hozzáadott cukor nélkül, vegán, 65 g |
| property_value_not_allowed | 8 | Alapanyag, sütés-főzés > Liszt, dara, morzsa > Kenyérliszt (BL80/BL112) | márka | Happy Harvest | HAPPY HARVEST Kenyérliszt keverék fehér kenyér, 1kg |
| property_value_not_allowed | 9 | Alapanyag, sütés-főzés > Liszt, dara, morzsa > Teljes kiőrlésű liszt | márka | Happy Harvest | HAPPY HARVEST Kenyérliszt keverék, 1 kg |
| property_shape_mismatch | 10 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | kiszerelés | zacskó | LE GUSTO Fűszerpaprika, édesnemes, 100 g |
| property_value_not_allowed | 10 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | kiszerelés | zacskó | LE GUSTO Fűszerpaprika, édesnemes, 100 g |
| property_value_not_allowed | 10 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | márka | Le Gusto | LE GUSTO Fűszerpaprika, édesnemes, 100 g |
| property_value_not_allowed | 10 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | csípősség | nem csípős | LE GUSTO Fűszerpaprika, édesnemes, 100 g |
| property_shape_mismatch | 12 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | kiszerelés | flakon | LE GUSTO Ketchup hozzáadott cukor nélkül, 615 g |
| property_value_not_allowed | 12 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | kiszerelés | flakon | LE GUSTO Ketchup hozzáadott cukor nélkül, 615 g |
| property_value_not_allowed | 12 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | márka | Le Gusto | LE GUSTO Ketchup hozzáadott cukor nélkül, 615 g |
| property_value_not_allowed | 12 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | íz | natúr | LE GUSTO Ketchup hozzáadott cukor nélkül, 615 g |
| property_shape_mismatch | 13 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | kiszerelés | üveg | CUCINA NOBILE Olívaolaj extraszűz, 750 ml |
| property_value_not_allowed | 13 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | kiszerelés | üveg | CUCINA NOBILE Olívaolaj extraszűz, 750 ml |
| property_value_not_allowed | 13 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | márka | Cucina Nobile | CUCINA NOBILE Olívaolaj extraszűz, 750 ml |
| property_shape_mismatch | 16 | Alapanyag, sütés-főzés > Étkezési só, ételízesítő > Só | kiszerelés | zacskó | LE GUSTO Jódozott vákumsó 1 kg |
| property_value_not_allowed | 16 | Alapanyag, sütés-főzés > Étkezési só, ételízesítő > Só | kiszerelés | zacskó | LE GUSTO Jódozott vákumsó 1 kg |
| property_value_not_allowed | 16 | Alapanyag, sütés-főzés > Étkezési só, ételízesítő > Só | márka | Le Gusto | LE GUSTO Jódozott vákumsó 1 kg |
| property_shape_mismatch | 18 | Alapanyag, sütés-főzés > Rizs, köret > Rizs | kiszerelés | doboz | ASIA Jázmin rizs főzőtasakban, 250 g |
| property_value_not_allowed | 18 | Alapanyag, sütés-főzés > Rizs, köret > Rizs | kiszerelés | doboz | ASIA Jázmin rizs főzőtasakban, 250 g |
| property_value_not_allowed | 18 | Alapanyag, sütés-főzés > Rizs, köret > Rizs | márka | Asia | ASIA Jázmin rizs főzőtasakban, 250 g |
| property_value_not_allowed | 22 | Alapanyag, sütés-főzés > Liszt, dara, morzsa > Dara, gríz | márka | Happy Harvest | HAPPY HARVEST Búzadara, 1 kg |
| property_value_not_allowed | 23 | Alapanyag, sütés-főzés > Liszt, dara, morzsa > Teljes kiőrlésű liszt | márka | Happy Harvest | HAPPY HARVEST Teljes kiőrlésű búzaliszt, 1 kg |
| property_shape_mismatch | 25 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Ecet | kiszerelés | flakon | LE GUSTO Ételecet 20%-os savtartalommal, 1 liter |
| property_value_not_allowed | 25 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Ecet | kiszerelés | flakon | LE GUSTO Ételecet 20%-os savtartalommal, 1 liter |
| property_value_not_allowed | 25 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Ecet | márka | Le Gusto | LE GUSTO Ételecet 20%-os savtartalommal, 1 liter |
| property_value_not_allowed | 26 | Alapanyag, sütés-főzés > Liszt, dara, morzsa > Kenyérliszt (BL80/BL112) | márka | Happy Harvest | HAPPY HARVEST Kenyérlisztkeverék, vital, 1kg |
| property_value_not_allowed | 27 | Alapanyag, sütés-főzés > Liszt, dara, morzsa > Kenyérliszt (BL80/BL112) | márka | Happy Harvest | HAPPY HARVEST Kenyérlisztkeverék, napraforgómagos, 1kg |
| property_value_not_allowed | 28 | Alapanyag, sütés-főzés > Liszt, dara, morzsa > Kenyérliszt (BL80/BL112) | márka | Happy Harvest | HAPPY HARVEST Kenyérlisztkeverék, parasztkenyér, 1kg |
| property_shape_mismatch | 29 | Alapanyag, sütés-főzés > Cukor, édesítőszer > Folyékony édesítő | kiszerelés | flakon | SÜSSLI Folyékony édesítőszer, 300 ml |
| property_value_not_allowed | 29 | Alapanyag, sütés-főzés > Cukor, édesítőszer > Folyékony édesítő | kiszerelés | flakon | SÜSSLI Folyékony édesítőszer, 300 ml |
| property_value_not_allowed | 29 | Alapanyag, sütés-főzés > Cukor, édesítőszer > Folyékony édesítő | márka | Süssli | SÜSSLI Folyékony édesítőszer, 300 ml |
| property_value_not_allowed | 29 | Alapanyag, sütés-főzés > Cukor, édesítőszer > Folyékony édesítő | szín | egyéb | SÜSSLI Folyékony édesítőszer, 300 ml |
| property_shape_mismatch | 30 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | kiszerelés | zacskó | LE GUSTO Fűszerpaprika, csemege, 100 g |
| property_value_not_allowed | 30 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | kiszerelés | zacskó | LE GUSTO Fűszerpaprika, csemege, 100 g |
| property_value_not_allowed | 30 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | márka | Le Gusto | LE GUSTO Fűszerpaprika, csemege, 100 g |
| property_value_not_allowed | 30 | Alapanyag, sütés-főzés > Fűszer > Őrölt paprika | csípősség | nem csípős | LE GUSTO Fűszerpaprika, csemege, 100 g |
| property_value_not_allowed | 33 | Alapanyag, sütés-főzés > Instant ételek, alapok > Pürépor, krumplipehely | kiszerelés | tasakos | LE GUSTO Burgonyapüré alappor, 345 g |
| property_value_not_allowed | 33 | Alapanyag, sütés-főzés > Instant ételek, alapok > Pürépor, krumplipehely | márka | Le Gusto | LE GUSTO Burgonyapüré alappor, 345 g |
| property_value_not_allowed | 34 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Paprikakrém, darált paprika | márka | Le Gusto | LE GUSTO Darált paprika csípős, 200 g |
| property_value_not_allowed | 35 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Paprikakrém, darált paprika | márka | Le Gusto | LE GUSTO Darált paprika csemege, 200 g |
| property_shape_mismatch | 36 | Alapanyag, sütés-főzés > Étkezési só, ételízesítő > Só | kiszerelés | doboz | LE GUSTO jódozott tengeri só finom szemű, 1 kg |
| property_value_not_allowed | 36 | Alapanyag, sütés-főzés > Étkezési só, ételízesítő > Só | kiszerelés | doboz | LE GUSTO jódozott tengeri só finom szemű, 1 kg |
| property_value_not_allowed | 36 | Alapanyag, sütés-főzés > Étkezési só, ételízesítő > Só | márka | Le Gusto | LE GUSTO jódozott tengeri só finom szemű, 1 kg |
| property_shape_mismatch | 38 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | kiszerelés | flakon | LE GUSTO Ketchup csípős, 1 kg |
| property_value_not_allowed | 38 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | kiszerelés | flakon | LE GUSTO Ketchup csípős, 1 kg |
| property_value_not_allowed | 38 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | márka | Le Gusto | LE GUSTO Ketchup csípős, 1 kg |
| property_shape_mismatch | 39 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | kiszerelés | flakon | LE GUSTO Ketchup enyhe, 1 kg |
| property_value_not_allowed | 39 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | kiszerelés | flakon | LE GUSTO Ketchup enyhe, 1 kg |
| property_value_not_allowed | 39 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | márka | Le Gusto | LE GUSTO Ketchup enyhe, 1 kg |
| property_value_not_allowed | 39 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Ketchup | íz | natúr | LE GUSTO Ketchup enyhe, 1 kg |
| property_shape_mismatch | 40 | Alapanyag, sütés-főzés > Cukor, édesítőszer > Barnacukor, nádcukor | kiszerelés | doboz | HAPPY HARVEST Nádcukor, 1kg |
| property_value_not_allowed | 40 | Alapanyag, sütés-főzés > Cukor, édesítőszer > Barnacukor, nádcukor | kiszerelés | doboz | HAPPY HARVEST Nádcukor, 1kg |
| property_value_not_allowed | 40 | Alapanyag, sütés-főzés > Cukor, édesítőszer > Barnacukor, nádcukor | márka | Happy Harvest | HAPPY HARVEST Nádcukor, 1kg |
| property_value_not_allowed | 41 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | kiszerelés | üveg | LE GUSTO Tésztaszósz arrabbiata, 500 g |
| property_value_not_allowed | 41 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | márka | Le Gusto | LE GUSTO Tésztaszósz arrabbiata, 500 g |
| property_value_not_allowed | 41 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | íz | csípős | LE GUSTO Tésztaszósz arrabbiata, 500 g |
| property_value_not_allowed | 42 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | kiszerelés | üveg | LE GUSTO Tésztaszósz bazsalikomos, 500 g |
| property_value_not_allowed | 42 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | márka | Le Gusto | LE GUSTO Tésztaszósz bazsalikomos, 500 g |
| property_value_not_allowed | 42 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | íz | egyéb | LE GUSTO Tésztaszósz bazsalikomos, 500 g |
| property_value_not_allowed | 43 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | kiszerelés | üveg | LE GUSTO Tésztaszósz bolognai, 500 g |
| property_value_not_allowed | 43 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | márka | Le Gusto | LE GUSTO Tésztaszósz bolognai, 500 g |
| property_value_not_allowed | 43 | Alapanyag, sütés-főzés > Szószok, öntetek, dresszingek > Tésztaszósz | íz | egyéb | LE GUSTO Tésztaszósz bolognai, 500 g |
| property_value_not_allowed | 49 | Alapanyag, sütés-főzés > Sütési alapanyag > Kakaópor, csokicsepp, tortabevonó | kiszerelés | zacskó | BACK FAMILY Mártócsokoládé tejcsokoládé, 200 g |
| property_value_not_allowed | 49 | Alapanyag, sütés-főzés > Sütési alapanyag > Kakaópor, csokicsepp, tortabevonó | márka | Back Family | BACK FAMILY Mártócsokoládé tejcsokoládé, 200 g |
| property_value_not_allowed | 50 | Alapanyag, sütés-főzés > Sütési alapanyag > Kakaópor, csokicsepp, tortabevonó | kiszerelés | zacskó | BACK FAMILY Mártócsokoládé fehércsokoládé, 200 g |
| property_value_not_allowed | 50 | Alapanyag, sütés-főzés > Sütési alapanyag > Kakaópor, csokicsepp, tortabevonó | márka | Back Family | BACK FAMILY Mártócsokoládé fehércsokoládé, 200 g |
| property_value_not_allowed | 51 | Alapanyag, sütés-főzés > Sütési alapanyag > Kakaópor, csokicsepp, tortabevonó | kiszerelés | zacskó | BACK FAMILY Mártócsokoládé étcsokoládé, 200 g |
| property_value_not_allowed | 51 | Alapanyag, sütés-főzés > Sütési alapanyag > Kakaópor, csokicsepp, tortabevonó | márka | Back Family | BACK FAMILY Mártócsokoládé étcsokoládé, 200 g |
| property_shape_mismatch | 52 | Alapanyag, sütés-főzés > Lekvár, méz, édes krém > Mogyorókrém, csokikrém (Nutella jellegű) | kiszerelés | üveg | FERRERO Nutella mogyorókrém 400 g |
| property_value_not_allowed | 52 | Alapanyag, sütés-főzés > Lekvár, méz, édes krém > Mogyorókrém, csokikrém (Nutella jellegű) | márka | Ferrero | FERRERO Nutella mogyorókrém 400 g |
| property_value_not_allowed | 52 | Alapanyag, sütés-főzés > Lekvár, méz, édes krém > Mogyorókrém, csokikrém (Nutella jellegű) | édesítés | cukorral | FERRERO Nutella mogyorókrém 400 g |
| property_shape_mismatch | 53 | Alapanyag, sütés-főzés > Lekvár, méz, édes krém > Méz | kiszerelés | üveg | GRANDESSA virágméz 900g |
| property_value_not_allowed | 53 | Alapanyag, sütés-főzés > Lekvár, méz, édes krém > Méz | márka | Grandessa | GRANDESSA virágméz 900g |
| property_shape_mismatch | 54 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | kiszerelés | flakon | FONTOLIVA Olívapogácsa olaj, 1 liter |
| property_value_not_allowed | 54 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | kiszerelés | flakon | FONTOLIVA Olívapogácsa olaj, 1 liter |
| property_value_not_allowed | 54 | Alapanyag, sütés-főzés > Olaj, ecet, zsiradék > Olívaolaj | márka | Fontoliva | FONTOLIVA Olívapogácsa olaj, 1 liter |
| property_value_not_allowed | 58 | Alapanyag, sütés-főzés > Sütési alapanyag > Sütőpor, szódabikarbóna, élesztő | kiszerelés | egyéb | Élesztő, 42 g |
| property_value_not_allowed | 58 | Alapanyag, sütés-főzés > Sütési alapanyag > Sütőpor, szódabikarbóna, élesztő | márka | egyéb | Élesztő, 42 g |
| property_value_not_allowed | 58 | Alapanyag, sütés-főzés > Sütési alapanyag > Sütőpor, szódabikarbóna, élesztő | forma | egyéb | Élesztő, 42 g |
| property_value_not_allowed | 59 | Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | LE GUSTO majoranna, 8 g |
| property_value_not_allowed | 60 | Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | LE GUSTO Kakukkfű, 10 g |
| property_value_not_allowed | 61 | Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | LE GUSTO Rozmaring, 15 g |
| property_value_not_allowed | 62 | Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | LE GUSTO Bazsalikom, 10 g |
| property_value_not_allowed | 63 | Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | LE GUSTO Kapor, 10 g |
| property_value_not_allowed | 64 | Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | LE GUSTO Oregánó, 10 g |
| property_value_not_allowed | 65 | Alapanyag, sütés-főzés > Fűszer > Szárított fűszernövény | márka | Le Gusto | LE GUSTO Petrezselyem, 10 g |
| property_value_not_allowed | 66 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | márka | Enjoy Free! | ENJOY FREE! Kókuszos müzliszelet kakaós tejbevonó talppal 30 g |
| property_value_not_allowed | 66 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | alap | egyéb | ENJOY FREE! Kókuszos müzliszelet kakaós tejbevonó talppal 30 g |
| property_value_not_allowed | 67 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | márka | Enjoy Free! | ENJOY FREE! Epres müzliszelet hozzáadott cukor nélkül, 30 g |
| property_value_not_allowed | 67 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | alap | egyéb | ENJOY FREE! Epres müzliszelet hozzáadott cukor nélkül, 30 g |
| property_value_not_allowed | 67 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | íz | egyéb | ENJOY FREE! Epres müzliszelet hozzáadott cukor nélkül, 30 g |
| property_value_not_allowed | 68 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | márka | Golden Bridge | GOLDEN BRIDGE Sárgabarackos müzliszelet joghurtos bevonótalppal, 30 g |
| property_value_not_allowed | 68 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | alap | gyümölcs | GOLDEN BRIDGE Sárgabarackos müzliszelet joghurtos bevonótalppal, 30 g |
| property_value_not_allowed | 68 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | íz | egyéb | GOLDEN BRIDGE Sárgabarackos müzliszelet joghurtos bevonótalppal, 30 g |
| property_value_not_allowed | 69 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | márka | Golden Bridge | GOLDEN BRIDGE Áfonyás müzliszelet joghurtos bevonóval, 30 g |
| property_value_not_allowed | 69 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | alap | gyümölcs | GOLDEN BRIDGE Áfonyás müzliszelet joghurtos bevonóval, 30 g |
| property_value_not_allowed | 70 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | márka | Golden Bridge | GOLDEN BRIDGE Csokoládés müzliszelet, 30 g |
| property_value_not_allowed | 70 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | alap | egyéb | GOLDEN BRIDGE Csokoládés müzliszelet, 30 g |
| property_value_not_allowed | 71 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | márka | Golden Bridge | GOLDEN BRIDGE Gyümölcsös müzliszelet, 30 g |
| property_value_not_allowed | 71 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | alap | gyümölcs | GOLDEN BRIDGE Gyümölcsös müzliszelet, 30 g |
| property_value_not_allowed | 71 | Édesség, snack, rágcsálnivaló > Müzliszelet, gabonaszelet > Müzliszelet | íz | egyéb | GOLDEN BRIDGE Gyümölcsös müzliszelet, 30 g |
| property_value_not_allowed | 72 | Alapanyag, sütés-főzés > Fűszer > Őrölt / egész fűszer | márka | Le Gusto | LE GUSTO Őrölt kömény, 25 g |
| property_value_not_allowed | 73 | Alapanyag, sütés-főzés > Fűszer > Őrölt / egész fűszer | márka | Le Gusto | LE GUSTO Őrölt gyömbér, 20 g |
| property_value_not_allowed | 74 | Hús, hal, felvágott > Pástétom, húskrém > Májpástétom | márka | Primana | PRIMANA Májas sertés, 100 g |
| property_value_not_allowed | 74 | Hús, hal, felvágott > Pástétom, húskrém > Májpástétom | csomagolás | konzerv | PRIMANA Májas sertés, 100 g |
| property_value_not_allowed | 75 | Hús, hal, felvágott > Pástétom, húskrém > Májpástétom | márka | Primana | PRIMANA Májas csirke, 100 g |

## Ertelmezes

- `subtree szerint termek nelkuli`: az adott node ala egyetlen termek sem esik, leszarmozott altipussal sem.
- `exact besorolas nelkuli`: pont arra a node-ra nincs termek; ettol meg lehetnek alatta termekek.
- `property_not_declared_for_category`: a termek tulajdonsaga nincs deklaralva a fokategoria/alkategoria/altipus effektiven orokolt tulajdonsagai kozott.
- `property_value_not_allowed`: a tulajdonsag letezik, de a termeken szereplo ertek nincs a kategoriafaban felsorolt engedelyezett ertekek kozott.
- `property_has_no_allowed_values`: a tulajdonsag letezik, de ures erteklistaval, mikozben a termeken van nem ures ertek.
- A flag tulajdonsagok `{} ` alaku deklaracioi nem szamitanak ures erteklistanak; ezek bool erteket varnak.
