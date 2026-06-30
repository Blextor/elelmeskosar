# Ital ritka altípus iteráció - 2026-06-30

## Fókusz

- Magányos vagy kevés terméket tartalmazó Ital altípusok ellenőrzése.
- Túl specifikus, íz/funkció/alapanyag-keverék alapján létrejött altípusok összevonása.
- Valódi ritka terméktípusok megtartása.

## Eredmény

- Alacsony elemszámú útvonalak száma: 83 -> 22
- Singleton útvonalak száma: 42 -> 7
- Ital útvonalak száma: 187 -> 129
- Ital termékek száma: 12716 -> 12713

## Fő összevonások

- Funkcionális italok:
  - Antioxidáns, Body, Boost, Immun, Stresszoldó, Relax, Funkcionális víz, Mate, Oxigénes, Kollagén/Kollagénes altípusok -> Funkcionális ital
  - Gyömbér shot -> Shot ital
- Gyümölcslevek:
  - kevés elemszámú gyümölcsital/nektár altípusok -> Gyümölcsital / nektár
  - Zöldség-gyümölcs ital / Vegyes zöldség- és gyümölcslé / Zöldséges-gyümölcsös üdítő -> Vegyes gyümölcs- és zöldséglé
  - Multivitamin ital -> Multivitamin gyümölcslé
  - Ananászlé termékek termékszinten szétválasztva 100% gyümölcslé vagy Gyümölcsital / nektár útvonalra
- Növényi italok:
  - kevert alapú növényi italok -> Kevert növényi ital
  - Protein szójaital -> Szójaital
  - Mogyoróital -> Egyéb növényi ital
  - Kávés zabital -> Zabital
  - 3 növényi főzőkrém kikerült az Ital fából a Tejtermékek és tojás > Növényi alternatíva > Növényi főzőkrém / tejszín alá
- Kávé/tea/kakaó:
  - Forró csokoládé kapszula -> Kakaó kapszula
  - Gyerektea -> Rooibos tea
  - Instant gyömbér ital -> Teafű, filteres tea, instant tea
  - Kávékrémpor -> Kávé ízesítők / tejek / tejporok
  - Pótkávé -> Gabonakávé
- Sör/cider/pezsgő:
  - APA -> IPA / Ale
  - Bock sör és Pils típusú sör -> Lager sör
  - Félbarna sör és Vörös sör -> Barna sör
  - Sörkülönlegesség -> Ízesített sör
  - Alma cider -> Cider
  - Alkoholmentes cider jellegű ital -> Alkoholmentes cider
  - Pezsgőkoktél -> Habzó-, gyöngyözőbor, boralapú ital > Ízesített boralapú ital
- Víz/üdítő:
  - Szénsavmentes vízalapú ital és Szénsavas ivóvíz -> Ivóvíz / vízalapú ital
  - Gyökér- és gyümölcsital -> Gyökér alapú üdítőital
- Alkohol:
  - Rum alapú likőr -> Likőr

## Megtartott ritka altípusok

Megmaradt néhány 1-2 termékes altípus, mert önálló, nem csak íz vagy funkció szerinti bontás:

- Sake
- Alkoholmentes bor
- Likőrbor
- Siller bor
- Oolong tea
- Sörválogatás
- Abszint
- Ouzo

## Ellenőrzési eredmények

- Hiányzó kategóriaút: 0
- Nem használt kategóriaút: 0
- Duplikált altípusnév: 0
- Ugyanazon altípuson belüli duplikált tulajdonság: 0
- Termékben szereplő, de kategóriafából hiányzó tulajdonság: 0
- Kategóriafában szereplő, de termékből hiányzó tulajdonság: 0
- Üres tulajdonságérték: 0
- Kategóriafából hiányzó tulajdonságérték: 0
- Típusgyanús tulajdonságérték: 0
- Finomított szemantikai audit szerinti áthelyezendő ital/nem ital maradék: 0
- A növényi főzőkrém áthelyezések után a tejtermék tulajdonság- és logikai audit is 0 hibát jelez.

## Képes ellenőrzés

- `italok_munkafajlok/kontaktlapok_2026_06_30/ital_low_count_candidates_1.jpg`
- `italok_munkafajlok/kontaktlapok_2026_06_30/ital_low_count_candidates_2.jpg`
