# Kategorizalas allapotjegyzet

Utolso frissites: 2026-06-07

Ez a jegyzet azt rogziti, hogy meddig jutott a `tools/kategorizalo/probak`
termekkategorizalasi munka, es hogyan erdemes innen folytatni. A mappa neve a
fajlrendszeren ekezetesen `próbák`.

## Aktiv fajlok

- `kat25.py`: jelenleg hasznalt Tkinter alapu termekkategorizalo.
- `kategoriak_1005.json`: legfrissebb fo kategoriafa.
- `pekaru_sutemeny.csv`: a top-level `kat25.py` jelenlegi bemeneti CSV-je.
- `eredmeny_pekaru.json`: a top-level `kat25.py` ezt olvassa be indulasnal.
- `eredmeny.json`: a top-level `kat25.py` ide ment.
- `eredmeny_alkohol.json`: alkoholos termekek kesz kategorizalasa.
- `ktest/ital_spar/ital_eredmeny.json`: ital/kave/tea/udito tesztkor teljes eredmenye.
- `kategorizalt_termekek/sós_snack/eredmeny.json`: sos snack termekkor eredmenye.

Fontos mukodesi megjegyzes: `kat25.py` indulasnal `eredmeny_pekaru.json`-t olvas,
de menteskor `eredmeny.json`-t ir. A ket fajl 285 termekbol 3 termeknel ter el:
harom pogacsa jellegu termek `eredmeny.json` szerint `Pogácsa`, mig
`eredmeny_pekaru.json` szerint `Egyéb sós pékáru`.

## Kategoriafa ertelmezese

A kategoriafa szerkezete:

- fo kategoria
- `alkategóriák`
- `altípusok`
- `tulajdonságok`

A kidolgozottsag ertekelesenel nem eleg csak az alkategoria sajat
tulajdonsagait nezni. A fo kategoria szintu tulajdonsagok oroklodonek
tekintendok az alkategoriakra. Emiatt egy alkategoria akkor sem "ures", ha csak
a fo kategoria kozos tulajdonsagai vonatkoznak ra.

Kulcsfontossagu korrekcio:

- `Gyümölcs`: kesznek tekintendo. Fo kategoria szinten rogzitve van:
  `bio`, `hazai`, `kiszerelés`.
- `Zöldség`: a felhasznaloi pontositas alapjan kesznek tekintendo, mert erre is
  ervenyes a `bio`, `hazai`, `kiszerelés` tulajdonsaglogika. A jelenlegi
  `kategoriak_1005.json` fajlban viszont a `Zöldség` fo kategorianal ezek a
  kozos tulajdonsagok nem latszanak eltárolva, ezert a gepi ellenorzes tevesen
  hianyosnak jelolhette.

## Kesz vagy elorehaladott agak

- `Ital`: nagyon elorehaladott. Az alkohol, kave/tea/kakao, udito, asvanyviz,
  energiaital, szorp es kapcsolodo agai hasznalhatok.
- `Alkohol`: 886/886 termek kesz az `eredmeny_alkohol.json` alapjan.
- `Ital/kave/tea/udito`: 1127/1127 termek kesz a `ktest/ital_spar` eredmenyekben.
- `Pékáru`: kesz kozeli; minden alkategoria kapott tulajdonsagot.
- `Gyümölcs`: kesznek tekintendo.
- `Zöldség`: kesznek tekintendo a felhasznaloi pontositas alapjan.
- `Sós snack`: kulon csomagban jol feldolgozott; 212 kesz tetel latszik.

## Reszben kidolgozott agak

- `Édesség, snack, rágcsálnivaló`: a `Snack` ag jol kidolgozott, de a
  csokolade/edesseg/keksz/muzli irany meg hianyosabb.
- `Fagyasztott áruk`: tobb altipus-vaz megvan, de kevesebb a reszletes
  tulajdonsag.
- `Hús, hal, felvágott`: hus/hal altipus-vaz megvan, de sok tulajdonsag meg
  hianyzik.
- `Tejtermékek és tojás`: reszben kidolgozott. Fo vazak: `Joghurt`, `Sajt`,
  `Tejital`, de sok alkategoria meg tovabbi bontast vagy tulajdonsagot igenyel.

## Fo hianyok

Ezeket erdemes kovetkezokent folytatni:

1. `Sütemény, desszert, torta`
   - Fo kategoria szintu tulajdonsagok vannak: `fagyasztott`, `csomagolt`,
     `édes`, `sós`, `fajta`.
   - Alkategoriafa meg nincs kidolgozva.
   - A peksutemenyes munkaban 23 tetel emiatt maradt `folyamatban`.

2. `Készétel`
   - Nincs meg alkategoriafa.
   - A peksutemenyes munkaban 3 tetel emiatt maradt `folyamatban`.

3. `Alapanyag, sütés-főzés`
   - Alkategoria-vaz van, de reszletes tulajdonsag/altipus kidolgozas nincs.
   - Alkategoriak: `Étkezési só, ételízesítő`, `Fűszer`,
     `Lekvár, méz, mogyorókrém`, `Liszt, dara, morzsa`, `Olaj, zsiradék`,
     `Rizs, köret`, `Sütőpor, szódabikarbóna, élesztő`, `Tészta`.

4. `Baba`
   - Alkategoria-vaz van, de reszletes kidolgozas nincs.
   - Alkategoriak: `Bébiétel`, `Bébiital`, `Egyéb`, `Snack, keksz`,
     `Tejpép, gabonapép`, `Víz`.

5. `Mentes, speciális`
   - Alkategoria-vaz van, de reszletes kidolgozas nincs.
   - Alkategoriak: `Bio`, `Diétás, diabetikus`, `Egyéb`,
     `Gluténmentes termék`, `Laktózmentes termék`, `Paleo`,
     `Protein termék`, `Vegán`.

## Javasolt kovetkezo lepes

Elsokent a `Sütemény, desszert, torta` es a `Készétel` alkategoriafajat erdemes
felvenni, mert ezek konkretan blokkoljak a mar megkezdett peksutemenyes
kategorizalast. Ezutan jo kovetkezo blokk az `Alapanyag, sütés-főzés`, majd a
`Baba` es a `Mentes, speciális`.

Ha a `Zöldség` tenyleg ugyanazokat a kozos tulajdonsagokat orokli, mint a
`Gyümölcs`, akkor erdemes ezt a `kategoriak_1005.json` fajlban is explicit
rogziteni: `bio`, `hazai`, `kiszerelés`.

