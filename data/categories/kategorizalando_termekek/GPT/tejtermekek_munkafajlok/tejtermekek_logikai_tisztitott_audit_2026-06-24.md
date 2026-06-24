# Tejtermékek logikai tisztítás - külön munkafájl

- Generálva: 2026-06-24T19:23:45
- Bemeneti kategória: `tejtermekek_javitott_kategoria_2026-06-24.json`
- Bemeneti termékek: `tejtermekek_javitott_termekek_2026-06-24.json`
- Kimeneti kategória: `tejtermekek_logikai_tisztitott_kategoria_2026-06-24.json`
- Kimeneti termékek: `tejtermekek_logikai_tisztitott_termekek_2026-06-24.json`
- A fő `eredmeny.json` és `kategoriak_2026-06-13.json` fájlokat ez a script nem írja.

## Összesítés
- products: 5103
- paths_before: 102
- paths_after: 62
- product_moves: 875
- properties_added_or_inferred: 2978
- properties_removed: 4331
- properties_merged: 718
- rare_properties_pruned: 15
- booleans_filled: 22017

## Fő logikai döntések
- A `terméktípus`, `jelleg`, `termékcsalád`, `töltött`, `UHT`, `zsírtartalom_jelleg` jellegű ismétlő vagy kevert mezők törlésre/összevonásra kerültek.
- A `ízesítés` értékei az egységes `íz` tulajdonságba kerültek.
- A sajtnál az altípus a fő sajttípus lett; a konkrét sajtnevek és feldolgozási formák `fajta`/`forma` tulajdonságként maradtak.
- A túró `Cottage cheese` és `Rögös túró` altípusai `Tehéntúró` alá kerültek, a szemcsés/rögös információ `forma` lett.
- A `Vajkrém` termékek a sajtkrém/szendvicskrém alól a `Vaj / Vajkrém` útvonalra kerültek.
- A növényi joghurt/fermentált készítmény és a külön növényi főzőkrém altípusok beolvadtak a meglévő növényi gyűjtő altípusokba.
- A tojásnál a fürjtojás és tojáskészítmény jellegű termékek közös, tisztábban nevezett altípusba kerültek.

## Validáció
- products: 5103
- declared_paths: 62
- used_paths: 62
- missing_paths: []
- empty_altipus_products: 0
- product_only_props: []
- category_only_props: []
- forbidden_props_left: {}
- rare_props_by_alk_max_3: {}

## Altípusok tisztítás után
| Alkategória | Altípus | Termék |
| --- | --- | --- |
| Sajt | Félkemény sajt | 471 |
| Joghurt | Gyümölcsös/ízesített joghurt | 284 |
| Sajt | Ömlesztett sajt | 264 |
| Krémtúró, túródesszert | Túró Rudi jellegű túródesszert | 240 |
| Sajt | Friss / lágy sajt | 229 |
| Margarin | Margarin | 189 |
| Ivójoghurt, kefir, író és aludttej | Ivójoghurt | 180 |
| Növényi alternatíva | Növényi ital | 167 |
| Tejföl | Tejföl | 165 |
| Sajt | Penészes sajt | 134 |
| Tejital, jegeskávé | Kávéital / latte / cappuccino | 132 |
| Tejdesszert, puding | Puding | 122 |
| Tej | UHT tartós tej | 121 |
| Sajt | Kemény sajt | 119 |
| Tejdesszert, puding | Egyéb tejdesszert | 108 |
| Túró | Tehéntúró | 97 |
| Sajtkrém, szendvicskrém | Szendvicskrém | 95 |
| Vaj | Teavaj, márkázott vaj | 93 |
| Joghurt | Natúr joghurt | 92 |
| Tejital, jegeskávé | Egyéb ízesített tejital | 92 |
| Sajt | Grillsajt / halloumi / sütnivaló | 91 |
| Ivójoghurt, kefir, író és aludttej | Kefir | 89 |
| Tejdesszert, puding | Tejberizs | 88 |
| Tojás | Tyúktojás | 87 |
| Növényi alternatíva | Növényi joghurt | 78 |
| Tejital, jegeskávé | Jegeskávé | 76 |
| Növényi alternatíva | Növényi főzőkrém / tejszín | 73 |
| Vaj | Vajkrém | 72 |
| Tejszín | Főzőtejszín | 68 |
| Tej | ESL tej | 67 |
| Tejital, jegeskávé | Kakaós tej | 67 |
| Joghurt | Görög joghurt | 63 |
| Sajtkrém, szendvicskrém | Kenhető ömlesztett sajt | 62 |
| Joghurt | Krémjoghurt | 59 |
| Növényi alternatíva | Növényi sajt | 55 |
| Tejdesszert, puding | Tejszelet | 54 |
| Krémtúró, túródesszert | Gyümölcsös krémtúró | 53 |
| Krémtúró, túródesszert | Natúr krémtúró | 50 |
| Tejszín | Tejszínhab spray | 47 |
| Sajtkrém, szendvicskrém | Sajtkrém | 40 |
| Növényi alternatíva | Növényi desszert | 38 |
| Tejszín | Habtejszín | 36 |
| Növényi alternatíva | Növényi szendvicskrém | 33 |
| Tejszín | Kávétejszín | 31 |
| Tejdesszert, puding | Habdesszert | 24 |
| Tejdesszert, puding | Hűtött snack | 24 |
| Vaj | Kenhető vajkeverék | 23 |
| Joghurt | Skyr / proteinjoghurt | 23 |
| Krémtúró, túródesszert | Túródesszert | 23 |
| Túró | Körözött | 19 |
| Tejital, jegeskávé | Protein tejital | 18 |
| Túró | Juhtúró | 15 |
| Tojás | Egyéb tojás és tojáskészítmény | 10 |
| Növényi alternatíva | Növényi vaj / margarin | 10 |
| Tej | Friss tej | 9 |
| Tej | Sűrített tej | 8 |
| Növényi alternatíva | Növényi tejföl | 8 |
| Tejszín | Cukrászhab | 8 |
| Ivójoghurt, kefir, író és aludttej | Író | 5 |
| Ivójoghurt, kefir, író és aludttej | Aludttej | 2 |
| Tej | Kávéfehérítő, tejkészítmény | 2 |
| Tej | Tejpor | 1 |

## Legnagyobb mozgatási szabályok
| Mozgatás | Termék |
| --- | --- |
| Ivójoghurt, kefir, író, aludttej / Ivójoghurt -> Ivójoghurt, kefir, író és aludttej / Ivójoghurt | 180 |
| Ivójoghurt, kefir, író, aludttej / Kefir -> Ivójoghurt, kefir, író és aludttej / Kefir | 89 |
| Sajt / Krémsajt / kenhető sajt -> Sajtkrém, szendvicskrém / Sajtkrém | 40 |
| Sajt / Friss / lágy sajt -> Sajt / Ömlesztett sajt | 40 |
| Sajtkrém, szendvicskrém / Ömlesztett sajt -> Sajtkrém, szendvicskrém / Kenhető ömlesztett sajt | 36 |
| Sajt / Mozzarella -> Sajt / Friss / lágy sajt | 35 |
| Sajt / Darabolt sajt -> Sajt / Félkemény sajt | 33 |
| Sajt / Félkemény sajt -> Sajt / Ömlesztett sajt | 31 |
| Sajt / Camembert / Brie -> Sajt / Penészes sajt | 31 |
| Sajt / Szeletelt sajt -> Sajt / Félkemény sajt | 31 |
| Sajt / Krémsajt / kenhető sajt -> Sajtkrém, szendvicskrém / Szendvicskrém | 26 |
| Növényi alternatíva / Növényi joghurt / fermentált készítmény -> Növényi alternatíva / Növényi joghurt | 23 |
| Sajtkrém, szendvicskrém / Sajtkrém -> Sajtkrém, szendvicskrém / Szendvicskrém | 21 |
| Sajt / Feta / krémfehér sajt -> Sajt / Friss / lágy sajt | 20 |
| Sajtkrém, szendvicskrém / Sajtkrém -> Sajtkrém, szendvicskrém / Kenhető ömlesztett sajt | 19 |
| Sajtkrém, szendvicskrém / Vajkrém -> Vaj / Vajkrém | 16 |
| Sajt / Reszelt sajt -> Sajt / Félkemény sajt | 16 |
| Vaj / Vaj -> Vaj / Teavaj, márkázott vaj | 16 |
| Sajt / Mascarpone -> Sajt / Friss / lágy sajt | 13 |
| Tejföl / Laktózmentes tejföl -> Tejföl / Tejföl | 12 |
| Sajt / Trappista sajt -> Sajt / Félkemény sajt | 12 |
| Túró / Cottage cheese -> Túró / Tehéntúró | 10 |
| Tojás / Egyéb tojás (fürj, stb.) -> Tojás / Egyéb tojás és tojáskészítmény | 8 |
| Sajt / Parenyica -> Sajt / Félkemény sajt | 8 |
| Sajt / Lapka sajt -> Sajt / Ömlesztett sajt | 8 |
| Tej / Tej -> Tej / UHT tartós tej | 7 |
| Sajt / Kék sajt -> Sajt / Penészes sajt | 7 |
| Sajt / Kemény sajt -> Sajt / Ömlesztett sajt | 6 |
| Sajtkrém, szendvicskrém / Szendvicskrém -> Sajtkrém, szendvicskrém / Kenhető ömlesztett sajt | 6 |
| Ivójoghurt, kefir, író, aludttej / Író -> Ivójoghurt, kefir, író és aludttej / Író | 5 |

## Törölt tulajdonságok
| Tulajdonság | Törlés |
| --- | --- |
| terméktípus | 2513 |
| jelleg | 587 |
| ízesítés | 547 |
| forma | 255 |
| UHT | 100 |
| bevonat típusa | 80 |
| zsírtartalom_jelleg | 65 |
| fajta | 49 |
| hőkezelés | 28 |
| édesítőszerrel | 24 |
| alap | 16 |
| érlelt | 10 |
| célcsoport | 9 |
| kiegészítő | 9 |
| készítmény (növényi zsiradékkal) | 7 |
| íz | 6 |
| ízesített | 5 |
| protein / magas fehérje | 5 |
| állat | 4 |
| felhasználás | 4 |
| édesítés | 3 |
| bevonat | 2 |
| dúsítás | 2 |
| darabos / feltét | 1 |

## Ritka tulajdonságok max. 3 termékkel
| Tulajdonság | Termék |
| --- | --- |

## Alkategóriánként törölt ritka tulajdonságok
| Alkategória / tulajdonság | Törlés |
| --- | --- |
| Tejföl / íz | 3 |
| Tejszín / édesítés | 3 |
| Tojás / hőkezelés | 2 |
| Tejdesszert, puding / bevonat | 2 |
| Tejszín / felhasználás | 2 |
| Tejital, jegeskávé / dúsítás | 2 |
| Krémtúró, túródesszert / darabos / feltét | 1 |
