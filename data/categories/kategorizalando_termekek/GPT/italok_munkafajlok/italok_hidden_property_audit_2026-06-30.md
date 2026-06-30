# Ital rejtett tulajdonság audit

- Ital termékek: 12713
- Használt Ital altípus utak: 129
- `terméktípus` mezős utak: 0
- `jellemzők` mezős utak: 7
- Boolean gyanúk: 9
- Ritka érték gyanúk: 3364

## Legnagyobb `terméktípus` használatok

## `jellemzők` problémás értékei
- Növényi ital > Zabital (23): problémás=[], ritka=[('D2-vitaminnal', 2), ('hozzáadott kalciummal', 1), ('D-vitaminnal', 1), ('B12-vitaminnal', 1), ('gluténmentes', 1)]
- Funkcionális ital > Fit ital (11): problémás=[], ritka=[('energiamentes', 2), ('szénsavmentes', 2), ('vitaminos', 1), ('kollagénnel', 1)]
- Növényi ital > Szójaital (9): problémás=[], ritka=[('hozzáadott kalciummal', 2), ('édesített', 1), ('jóddal', 1)]
- Növényi ital > Rizsital (8): problémás=[], ritka=[('cukormentes', 1), ('kalciummal', 1), ('vitaminos', 1), ('barista', 1)]
- Növényi ital > Kevert növényi ital (7): problémás=[], ritka=[('bio', 2), ('UHT', 2), ('gluténmentes', 1)]
- Üdítőital > Gyökér alapú üdítőital (3): problémás=[], ritka=[('szénsavas', 1)]
- Növényi ital > Egyéb növényi ital (1): problémás=[], ritka=[('kalciummal', 1), ('vitaminos', 1)]

## Boolean gyanúk
- Üdítőital > Szénsavas üdítő | bio: true=2, false=754
- Üdítőital > Szénsavas üdítő | koffeinmentes: true=12, false=744
- Üdítőital > Jegestea | bio: true=6, false=475
- Sör > Világos sör | gluténmentes: true=8, false=467
- Sör > Világos sör | kézműves: true=9, false=466
- Szörp, üdítőitalpor > Szörp | cukormentes / diabetikus: true=7, false=360
- Kávé, tea, kakaó (száraz) > Őrölt kávé | bio: true=3, false=252
- Kávé, tea, kakaó (száraz) > Szemes kávé | bio: true=3, false=233
- Kávé, tea, kakaó (száraz) > Teafű, filteres tea, instant tea | bio: true=2, false=207
