# Élelmes Kosár

Ez a repository az Élelmes Kosár adatgyűjtő, adattisztító, kategorizáló és elemző kódjait tartalmazza.

## Fő részek

- `src/`: a főbb, élesebb forráskódok helye.
- `data/`: a letöltött és feldolgozott piaci adatok tárolója.
- `analysis/`: elemző szkriptek, riportok és adatütközési eredmények.
- `docs/`: tervek, működési jegyzetek és koncepcionális dokumentáció.
- `experiments/`: WIP prototípusok, térképes próbák és bolti API-kísérletek.
- `tools/`: fejlesztést segítő eszközök, például a kategorizáló próbák.

## Megjegyzés

A projekt jelenleg szkript- és adatközpontú felépítésű. A Wolt alapú adatfolyamok
fő belépési pontjai:

- `src/markets/Spar/main_spar.py`
- `src/markets/Prima/main_prima.py`
