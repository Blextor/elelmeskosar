# Kategoria-inkonzisztencia riport

Datum: 2026-06-23

Forrasok:
- `data/categories/kategorizalando_termekek/GPT/kategoriak_2026-06-13.json`
- `data/categories/kategorizalando_termekek/GPT/eredmeny.json`

Megjegyzes: ez csak audit/gyujtes. A JSON fajlok nem lettek modositva.

## Cel

A kategoriafa inkonzisztenciainak osszegyujtese egy kesobbi, hosszabb rendezesi feladathoz. A rendezesnel nem eleg a kategoriakat torolni vagy atnevezni, mert az `eredmeny.json` termekbesorolasait is utana kell majd huzni.

## Osszkep

Az audit alapjan a fobb problema nem egyszeri eliras, hanem tobb kategorizarasi kor osszecsuszasa:

- regi reszletes agak es uj osszevont agak egyszerre vannak jelen;
- nehany fokatagoria masik fokatagoria ala tartozna;
- ugyanaz az alkategoria/altipus tobb helyen szerepel;
- a tulajdonsagkulcsokban es erteklistakban sok az irasmodbeli duplikacio;
- nehany `tulajdonsagok` szerkezet elter az elvart objektumos formatol.

## Termekdarabszam fokatagoria szerint

Az `eredmeny.json` 47 030 kesz statuszu termeket tartalmaz.

| Fokategoria | Termek |
|---|---:|
| Ital | 12 673 |
| Alapanyag, sutes-fozes | 10 619 |
| Edesseg, snack, ragcsalnivalo | 6 608 |
| Tejtermekek es tojas | 5 103 |
| Hus, hal, felvagott | 4 368 |
| Fagyasztott aruk | 2 955 |
| Pekaru | 1 277 |
| Zoldseg | 742 |
| Keszetelek | 620 |
| Haztartasi termek | 613 |
| Gyumolcs | 539 |
| Baba | 518 |
| Baba-mama | 127 |
| Mentes, specialis | 124 |
| Sutemeny, desszert, torta | 79 |
| Alkoholos ital | 48 |
| Jatek | 17 |

## Legfontosabb rendezendo fokatagoriak

### Alkoholos ital

Statusz: valoszinuleg torlendo/beolvasztando fokatagoria.

Indok:
- az `Alkoholos ital` csak 48 termeket erint;
- az `Ital` alatt mar megvan a teljes alkoholos struktura: `Bor`, `Alkoholok`, `Sor`, `Pezsgo`, `Cider`, `Habzo-, gyongyozobor, boralapu ital`;
- az `Ital` alatt tobb ezer alkoholos termek van, tehat az `Alkoholos ital` kis levallt duplikatumagnak tunik.

Erintett `Alkoholos ital` termekek:

| Ag | Termek |
|---|---:|
| Alkoholos ital > Koktel, long drink | 39 |
| Alkoholos ital > Bor | 6 |
| Alkoholos ital > Sor | 3 |

Javasolt migracios irany:
- `Alkoholos ital > Bor > Feherbor/Vorosbor/Rosebor` -> `Ital > Bor > Feherbor/Vorosbor/Rozebor vagy Rosebor`
- `Alkoholos ital > Sor > Izesitett sorkulonlegesseg` -> `Ital > Sor > Izesitett sor` vagy `Ital > Sor > Sorkulonlegesseg`
- `Alkoholos ital > Koktel, long drink > ...` -> `Ital > Alkoholok > Koktel, Rogton ihato, Egyeb`, esetleg kulon `Ital > Alkoholok > Long drink / RTD koktel` altipus letrehozasa

Dontos pont:
- a koktel/long drink altipusokat erdemes-e osszevonni az aktualis `Koktel, Rogton ihato, Egyeb` altipusba, vagy legyen reszletesebb RTD koktel bontas.

### Baba es Baba-mama

Statusz: erosen atfedo fokatagoriak.

Indok:
- `Baba` alatt mar megvannak az elelmiszeres babaagak: bebietel, gyumolcspure, tejpep/gabonapep, tapszer, snack/keksz, ital/viz;
- `Baba-mama` alatt ezek ujra megjelennek mas neveken;
- `Baba-mama` csak 127 termeket erint, a `Baba` 518-at.

Erintett `Baba-mama` termekek:

| Ag | Termek |
|---|---:|
| Baba-mama > Babaetel | 35 |
| Baba-mama > Baba italpor | 30 |
| Baba-mama > Babaapolasi eszkoz | 24 |
| Baba-mama > Tapszer | 22 |
| Baba-mama > Baba snack | 11 |
| Baba-mama > Baba keksz | 3 |
| Baba-mama > Baba ital | 2 |

Javasolt migracios irany:
- `Baba-mama > Tapszer` -> `Baba > Tapszer`
- `Baba-mama > Babaetel` -> `Baba > Bebietel, bebimenu (sos)` vagy `Baba > Tejpep, gabonapep, kasa` vagy `Baba > Gyumolcspure, bebidesszert`
- `Baba-mama > Baba snack` es `Baba-mama > Baba keksz` -> `Baba > Bebi snack, keksz`
- `Baba-mama > Baba ital` -> `Baba > Bebiital, viz`
- `Baba-mama > Baba italpor` -> valoszinuleg `Baba > Tapszer > Gyermek italpor`, de egyedi ellenorzes kell

Dontos pont:
- `Babaapolasi eszkoz` nem elelmiszer. Vagy a `Baba` alatt kell nem-elelmiszer alkategoria, vagy `Haztartasi termek > Szepsegapolas, higienia`/kulon babaapolas ag ala kell mozgatni.

### Mentes, specialis

Statusz: meta-/eletmod jellegu fokatagoria, nem tiszta termekfokatagoria.

Erintett termekek:

| Ag | Termek |
|---|---:|
| Mentes, specialis > Protein termek | 61 |
| Mentes, specialis > Etrend-kiegeszito, vitamin | 60 |
| Mentes, specialis > Sport taplalekkiegeszito | 2 |
| Mentes, specialis > Etrendkiegeszito | 1 |

Problemak:
- `Etrend-kiegeszito, vitamin` es `Etrendkiegeszito` duplikalt;
- `Protein termek` lehet snack, italpor, szelet, csokolade, keksz, tehat sokszor mas termekfokatagoria ala illik;
- a "mentes" tulajdonsag inkabb tulajdonsagkent jo: glutenmentes, laktozmentes, cukormentes, vegan, protein/magas feherje.

Dontos pont:
- maradjon-e kulon `Etrend-kiegeszito, vitamin` fokatagoria/alkategoria, vagy menjen `Haztartasi termek` ala;
- a protein termekek termektipus szerint szetszedendok-e (`Edesseg/snack`, `Ital`, stb.).

### Sutemeny, desszert, torta

Statusz: kicsi, tobb mas kategoriaval atfedo fokatagoria.

Erintett termekek: 79.

Atfedesek:
- `Fank` van `Pekaru` alatt is;
- `Edes sutemeny, desszert` atfed `Edesseg, snack, ragcsalnivalo` alatt levo sutemeny/desszert agakkal;
- `Pohardesszert, kremdesszert` es `Kesz sutemeny, desszert` atfedhet `Tejtermekek es tojas > Tejdesszert, puding`/`Tejes desszert` agakkal;
- `Tortalap, piskota` inkabb `Alapanyag, sutes-fozes > Sutesi alapanyag` vagy `Edesseg > Keksz, napolyi, ostya` jellegu lehet.

Dontos pont:
- legyen-e kulon cukraszati/desszert fokatagoria, vagy ezeket a termekeket a `Pekaru`, `Edesseg`, `Tejtermekek` es `Alapanyag` agakba kell szetosztani.

### Jatek

Statusz: nem elelmiszer, kis fokatagoria.

Erintett termekek:
- `Jatek > Epitojatek, konstrukcios jatek > LEGO keszlet`: 17 termek.

Dontos pont:
- maradjon-e kulon nem-elelmiszer fokatagoria, vagy menjen `Haztartasi termek`/egyeb nem-elelmiszer gyujto ala.

## Erős alkategoria-duplikaciok

### Edesseg, snack, ragcsalnivalo

Jelleg: regi reszletes es uj egyszerusitett snack/edesseg agak egyszerre vannak jelen.

Fo problemak:
- `Keksz, napolyi, ostya` mellett van kulon `Keksz`, `Ostya`, `Napolyi, ostya`, `Edes keksz, ostya, sutemeny`;
- `Snack` mellett van `Sos snack`, `Sos snack, ropi, perec`, `Edes snack`, `Gyumolcssnack`;
- `Csokolade` mellett van `Csokolades snack`, `Csokolade, csokolades edesseg`;
- `Cukorka, nyaloka` mellett van `Cukorka`;
- `Gumicukor, zsele, pillecukor` mellett van `Gumicukor`;
- `Muzliszelet, gabonaszelet` mellett van `Muzliszelet`.

Termekdarabszamok:

| Alkategoria | Termek |
|---|---:|
| Keksz, napolyi, ostya | 1 716 |
| Csokolade | 1 558 |
| Snack | 1 362 |
| Cukorka, nyaloka | 439 |
| Muzliszelet, gabonaszelet | 393 |
| Ragcsalnivalo magvak (snack) | 368 |
| Gumicukor, zsele, pillecukor | 331 |
| Ragagumi | 226 |
| Sos snack | 52 |
| Edes sutemeny, desszert | 40 |
| Keksz | 26 |
| Csokolades snack | 23 |
| Muzliszelet | 22 |

Javaslat:
- megtartani a nagy, reszletesebb agakat kanonikusnak;
- a kis uj agak termekeit visszamap-elni a kanonikus agakba.

### Fagyasztott aruk

Fo problemak:
- `Jegkrem, fagylalt` mellett kulon `Jegkrem`, `Fagylalt`;
- `Fagyasztott hal, tengeri aru` mellett `Fagyasztott hal, tenger gyumolcsei`;
- `Fagyasztott keszetel, pizza, egytaletel` mellett `Fagyasztott keszetel`, `Pizza`, `Keszetel`;
- `Fagyasztott zoldseg`, `Fagyasztott gyumolcs`, `Fagyasztott hus, baromfi` jol indokolhato, mert allapot szerinti fagyasztott ag.

Termekdarabszamok:

| Alkategoria | Termek |
|---|---:|
| Jegkrem, fagylalt | 1 033 |
| Fagyasztott zoldseg | 536 |
| Fagyasztott hus, baromfi | 349 |
| Fagyasztott hal, tengeri aru | 303 |
| Fagyasztott keszetel, pizza, egytaletel | 299 |
| Fagyasztott teszta, desszert | 218 |
| Fagyasztott panirozott (nem hus) | 95 |
| Fagyasztott gyumolcs | 90 |
| Fagyasztott hal, tenger gyumolcsei | 11 |
| Fagyasztott keszetel | 8 |
| Pizza | 4 |

### Tejtermekek es tojas

Fo problemak:
- `Joghurt`, `Joghurt, kefir`, `Joghurtital`;
- `Tejszin`, `Tejszin, tejfol`, `Tejszin, hab`;
- `Tejdesszert, puding`, `Tejes desszert`, `Desszert`;
- `Sajtkrem, szendvicskrem`, `Sajtkrem, kremsajt`;
- `Novenyi alternativa` es `Novenyi tejhelyettesito` atfed, illetve `Ital > Novenyi ital` aggal is utkozik.

Termekdarabszamok:

| Alkategoria | Termek |
|---|---:|
| Sajt | 1 441 |
| Joghurt | 499 |
| Novenyi alternativa | 404 |
| Tejdesszert, puding | 340 |
| Tejital, jegeskave | 308 |
| Kremturo, turodesszert | 290 |
| Tej | 281 |
| Ivojoghurt, kefir, iro | 209 |
| Margarin | 188 |
| Vaj | 162 |
| Tejfol | 156 |
| Tejszin | 155 |
| Tejes desszert | 153 |
| Joghurt, kefir | 103 |
| Sajtkrem, szendvicskrem | 99 |
| Tejszin, tejfol | 77 |

### Pekaru

Fo problemak:
- `Kifli`, `Zsemle`, `Kifli, zsemle`, `Zsemle, buci`;
- `Tortilla lap` es `Tortilla, wrap`;
- `Ketszersult, extrudalt kenyer` es `Extrudalt, ropogos kenyer`;
- `Kalacs` es `Kalacs, edes peksutemeny`;
- `Fank` atfed a `Sutemeny, desszert, torta > Fank` aggal.

Termekdarabszamok:

| Alkategoria | Termek |
|---|---:|
| Kenyer | 322 |
| Croissant | 159 |
| Egyeb edes pekaru | 108 |
| Ketszersult, extrudalt kenyer | 103 |
| Egyeb sos pekaru | 91 |
| Bagett | 82 |
| Tortilla lap | 79 |
| Hotdog buci es hamburger zsemle | 58 |
| Zsemle | 52 |
| Kalacs | 50 |
| Fank | 37 |
| Kifli | 22 |
| Extrudalt, ropogos kenyer | 16 |
| Kifli, zsemle | 13 |
| Kalacs, edes peksutemeny | 10 |
| Tortilla, wrap | 3 |
| Zsemle, buci | 2 |

### Gyumolcs es Zoldseg

Fo problema:
- az egyedi termeny-alkategoriak mellett letezik `Friss gyumolcs` es `Friss zoldseg`, amelyek ugyanazokat altipuskent is tartalmazzak.

Peldak:
- `Gyumolcs > Alma > Alma` es `Gyumolcs > Friss gyumolcs > Alma`;
- `Gyumolcs > Banán > Banán` es `Gyumolcs > Friss gyumolcs > Banan`;
- `Zoldseg > Gomba > Gomba` es `Zoldseg > Friss zoldseg > Gomba`;
- `Zoldseg > Paprika > Paprika` es `Zoldseg > Friss zoldseg > Paprika`;
- `Zoldseg > Avokado` es `Gyumolcs > Avokado`.

Dontos pont:
- legyen sok egyedi alkategoria, vagy egy `Friss gyumolcs`/`Friss zoldseg` alkategoria sok altipussal. A ket modell egyszerre duplikaciot okoz.

### Alapanyag, sutes-fozes

Fo problemak:
- `Fuszer` es `Fuszerek, etelizesitok`;
- `Rizs, koret` es `Rizs, gabona, mag`;
- `Cukor, edesitoszer` es `Cukor, edesitoszer, sutesi alapanyag`;
- `Szendvicskrem, pastetom` atfed `Keszetel > Szendvicskrem, hummusz, pastetom` aggal;
- `Sutesi alapanyag` sok altipusa atfedhet szosz/desszert/gyumolcs agakkal.

Kisebb uj agak:

| Alkategoria | Termek |
|---|---:|
| Fuszerek, etelizesitok | 39 |
| Szendvicskrem, pastetom | 14 |
| Cukor, edesitoszer, sutesi alapanyag | 3 |
| Fasirtpor | 3 |
| Kokosztej, kokoszkrem | 1 |

### Hus, hal, felvagott

Fo problemak:
- `Halkeszitmeny`, `Halkonzerv`, `Hal, halkonzerv` atfed;
- `Husos snack, szaritott` egyszerre lehet sajat alkategoria es `Felvagottak, huskeszitmeny` altipus;
- `Baromfi` kis uj ag, mikozben `Csirke`, `Pulyka`, `Kacsa, liba` mar letezik;
- `Grill husok` allapot/felhasznalas szerinti ag, utkozhat husfaj szerinti kategoriakkal.

## Normalizalt alkategoria-nev duplikaciok

Pontosan egyezo normalizalt alkategoria-nevek:

| Nev | Elofordulasok |
|---|---|
| Avokado | `Gyumolcs > Avokado`, `Zoldseg > Avokado` |
| Bor | `Ital > Bor`, `Alkoholos ital > Bor` |
| Fank | `Pekaru > Fank`, `Sutemeny, desszert, torta > Fank` |
| Mix, vegyes | `Gyumolcs > Mix, vegyes`, `Zoldseg > Mix, vegyes` |
| Sor | `Ital > Sor`, `Alkoholos ital > Sor` |
| Tapszer | `Baba > Tapszer`, `Baba-mama > Tapszer` |

## Normalizalt altipus-nev duplikaciok

Osszesen 170 normalizalt altipus-nev duplikacio csoport van:
- 151 csoport ket helyen fordul elo;
- 17 csoport harom helyen fordul elo;
- 2 csoport negy helyen fordul elo.

Fontosabb csoportok:

| Altipus | Elofordulasok |
|---|---|
| Gyumolcspure | `Alapanyag > Sutesi alapanyag`, `Baba > Gyumolcspure, bebidesszert`, `Gyumolcs > Gyumolcskeszitmeny, pure`, `Ital > Gyumolcsle` |
| Szendvicskrem | `Alapanyag > Szendvicskrem, pastetom`, `Tejtermekek > Sajt`, `Tejtermekek > Sajtkrem, szendvicskrem`, `Tejtermekek > Tejszin, tejfol` |
| Aszalt gyumolcs | `Alapanyag > Olajos magvak, aszalt gyumolcs`, `Edesseg > Ragcsalnivalo magvak`, `Gyumolcs > Aszalt gyumolcs` |
| Bogyos gyumolcs | `Fagyasztott aruk > Fagyasztott gyumolcs`, `Gyumolcs > Bogyos gyumolcs`, `Gyumolcs > Friss gyumolcs` |
| Fuszerso | `Alapanyag > Etkezesi so, etelizesito`, `Alapanyag > Fuszer`, `Alapanyag > Fuszerek, etelizesitok` |
| Gomba | `Fagyasztott aruk > Fagyasztott zoldseg`, `Zoldseg > Gomba`, `Zoldseg > Friss zoldseg` |
| Jegkocka | `Fagyasztott aruk > Fagyasztott teszta, desszert`, `Fagyasztott aruk > Egyeb fagyasztott`, `Fagyasztott aruk > Jeg` |
| Kombucha | `Ital > Uditoital`, `Ital > Funkcionalis ital`, `Ital > Kombucha` |
| Novenyi fozokrem | `Ital > Novenyi ital`, `Tejtermekek > Novenyi alternativa`, `Tejtermekek > Tejszin, tejfol` |
| Paprika | `Alapanyag > Fuszer`, `Zoldseg > Paprika`, `Zoldseg > Friss zoldseg` |
| Tofu | `Alapanyag > Huvelyesek`, `Hus, hal, felvagott > Novenyi huspotlo`, `Keszetel > Vegetarianus, vegan keszetel` |
| Vajkrem | `Tejtermekek > Vaj`, `Tejtermekek > Sajtkrem, szendvicskrem`, `Tejtermekek > Tejszin, tejfol` |
| Voroshagyma | `Alapanyag > Fuszer`, `Fagyasztott aruk > Fagyasztott zoldseg`, `Zoldseg > Hagymafelek` |
| Zoldsegkrem | `Alapanyag > Szoszok, ontetek, dresszingek`, `Alapanyag > Szendvicskrem, pastetom`, `Keszetel > Szendvicskrem, hummusz, pastetom` |
| Befott | `Alapanyag > Konzerv, savanyusag, befott`, `Gyumolcs > Gyumolcskonzerv / befott` |
| Fank | `Pekaru > Fank`, `Sutemeny, desszert, torta > Fank` |
| Feherbor | `Ital > Bor`, `Alkoholos ital > Bor` |
| Gnocchi | `Alapanyag > Teszta`, `Keszetel > Friss toltott teszta, gnocchi` |
| Hummusz | `Alapanyag > Szendvicskrem, pastetom`, `Keszetel > Szendvicskrem, hummusz, pastetom` |
| Jegeskave | `Tejtermekek > Tej`, `Tejtermekek > Tejital, jegeskave` |

Megjegyzes: nem minden altipus-nev duplikacio hiba. Peldaul `Comb` sertesen/marhan/baranyon belul jogos lehet. A fenti lista a leginkabb rendezendo, strukturat erinto eseteket emeli ki.

## Tulajdonsag-szerkezeti problemak

15 helyen a `tulajdonsagok.egyedi` nem objektum, hanem lista. Ezek szerkezeti inkonzisztenciak:

- `Gyumolcs > Afonya > Afonya`
- `Gyumolcs > Alma > Red Jonaprince alma`
- `Gyumolcs > Alma > Jonagored alma`
- `Gyumolcs > Ananasz > Ananasz`
- `Gyumolcs > Gorogdinnye > Gorogdinnye`
- `Gyumolcs > Grapefruit > Grapefruit`
- `Gyumolcs > Korte > Vilmos korte`
- `Gyumolcs > Korte > Packhams korte`
- `Gyumolcs > Lime > Lime`
- `Gyumolcs > Kokoszdio > Kokoszdio`
- `Zoldseg > Kaposzta > Kelkaposzta`
- `Zoldseg > Retekfelek > Jegcsapretek`
- `Zoldseg > Retekfelek > Vajretek`
- `Haztartasi termek > Takaritoeszkoz > Felmosofej`
- `Haztartasi termek > Takaritoeszkoz > Surolo`

Ezeket javitas elott egyseges formatumra kell hozni:

```json
"tulajdonsagok": {
  "egyedi": {},
  "csoportos": {}
}
```

## Tulajdonsagkulcs-duplikaciok

Ugyanaz a tulajdonsagkulcs tobb irasmoddal is szerepel.

Peldak:

| Normalizalt kulcs | Irasmodok |
|---|---|
| csipos | `csipos`, `csípõs`, `csípős` |
| csiposseg | `csípõsség`, `csípősség` |
| edesitoszer tipusa | `édesítõszer típusa`, `édesítőszer típusa` |
| extra sarga | `extra sárga`, `extra_sárga` |
| furt hotdog kifli | `fúrt hotdog kifli`, `fürt hotdog kifli` |
| fuszer iz | `fûszer / íz`, `fűszer / íz` |
| kiszereles mennyiseg | `kiszerelés / mennyiség`, `kiszerelés_mennyiség` |
| novenyi alap | `növényi alap`, `növényi_alap` |
| tea tipusa | `tea típusa`, `tea_típusa` |
| teljes kiorlesu | `teljes kiõrlésû`, `teljes kiőrlésű` |
| zsirtartalom jelleg | `zsírtartalom / jelleg`, `zsírtartalom jelleg`, `zsírtartalom_jelleg` |

Javaslat:
- a tulajdonsagkulcsokra kulon kanonikus nevlista kell;
- az `õ/ő`, `û/ű`, underscore, perjel es szokoz variaciokat normalizalni kell;
- a termekek `tulajdonsagok` mezoihez is ugyanazt a kulcsmigraciot kell alkalmazni.

## Tulajdonsag-erteklista duplikaciok

Osszesen 377 tulajdonsag-erteklistaban van normalizalt duplikacio. Tipikus okok:

- kisbetu/nagybetu: `Caputo` / `CAPUTO`, `Kotanyi` / `KOTANYI`;
- ekezetes kompatibilitasi gond: `orolt` / `õrölt` / `őrölt`;
- markanev irasmod: `Nagyi Titka` / `Nagyi titka`;
- kotojel/szokoz: `edes chili` / `edes-chili`;
- felesleges zarojeles meretvaltozat: `4 x 28 g` / `4 x 28 g (112 g)`;
- eliras: `sajtos-baconos` / `sajtos-baconös`.

Peldak:

| Hely | Tulajdonsag | Duplikacio |
|---|---|---|
| `Alapanyag > Liszt, dara, morzsa` | marka | `Caputo` / `CAPUTO` |
| `Alapanyag > Liszt, dara, morzsa > Kenyerliszt` | marka | `Nagyi Titka` / `Nagyi titka`, `Caputo` / `CAPUTO` |
| `Alapanyag > Fuszer` | marka | `Kotanyi` / `KOTANYI`, `Izmester` / `IZMESTER`, `Thymos` / `THYMOS` |
| `Alapanyag > Fuszer > Bors` | forma | `őrölt` / `õrölt` |
| `Alapanyag > Szoszok > Ketchup` | marka | `Globus` / `GLOBUS`, `Heinz` / `HEINZ`, `Hellmann's` / `HELLMANN'S` |
| `Alapanyag > Teszta` | marka | `Gyermelyi` / `GYERMELYI`, `Barilla` / `BARILLA`, `It's Us` / `It's us` |
| `Ital`, tobb ag | ital/kategoria ertekek | `Rosebor` / `Rozebor`, `Vermuth` / `Vermut` jellegu variaciok |

Javaslat:
- markakra erdemes case-insensitive deduplikaciot futtatni, de megtartott kanonikus megjelenesi formaval;
- nem marka ertekeknel ovatosabb kezi ellenorzes kell, mert neha valodi jelenteskulonbseg lehet.

## Javasolt kesobbi munkamenet

1. Kanonikus fokatagoria- es alkategoria-dontesek rogzitese.
2. Migracios tabla keszitese: regi `fokategoria/alkategoria/altipus` -> uj `fokategoria/alkategoria/altipus`.
3. `kategoriak_2026-06-13.json` rendezese a migracios tabla szerint.
4. `eredmeny.json` termekbesorolasainak atvezetese ugyanazzal a tablaval.
5. Tulajdonsagkulcsok kanonizalasa.
6. Tulajdonsagertek-listak deduplikalasa.
7. Validacio:
   - nincs arva termekbesorolas;
   - nincs ures vagy megszunt kategoriara mutato termek;
   - minden hasznalt termek-kategoria letezik a kategoriafaban;
   - nincs duplikalt normalizalt alkategoria ugyanazon dontesi szinten;
   - nincs lista-formatumu `tulajdonsagok.egyedi`.

## Prioritas-javaslat

1. `Alkoholos ital` beolvasztasa `Ital` ala.
2. `Baba-mama` beolvasztasa/rendezese.
3. `Edesseg, snack, ragcsalnivalo` duplikalt kisebb againak osszevonasa.
4. `Fagyasztott aruk`, `Tejtermekek es tojas`, `Pekaru` belso duplikacioinak tisztitasa.
5. `Gyumolcs`/`Zoldseg` modell-dontes: egyedi alkategoria vs. `Friss ...` gyujto.
6. Tulajdonsagkulcsok es erteklistak normalizalasa.

