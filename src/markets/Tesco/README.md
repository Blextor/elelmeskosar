# Tesco

Tesco sajat webes adatfolyam a `bevasarlas.tesco.hu` / `xapi.tesco.com`
GraphQL vegpontjaihoz.

## Szerepe

Ez a mappa a Tesco termekadatok letolteset, szureset es az egységes piaci
CSV semara normalizalasat tartalmazza. A Tesco nem Wolt-alapu bolt, ezert a
SPAR/Prima letoltoktol elteroen mukodik:

- a fo kategoriak a Tesco landing oldal aktualis `browse/.../all` linkjeibol
  frissulnek;
- a termeklista GraphQL `category` lekerdezesen keresztul jon;
- a `facet` ertek az ekezetes kategoriautvonal URL-encode + base64 alakja;
- a reszletes kategoriafa a termekekben levo
  `superDepartmentName / departmentName / aisleName / shelfName` mezokbol epul;
- az arak mar forintban erkeznek, nem filleres/centes formatumban;
- a lédig es catch-weight termekeknel a kosarba teheto alaplepes sokszor az
  aranybol szamolhato: `price.actual / price.unitPrice`.

## Fajlok

- `main_tesco.py`: a teljes Tesco folyamat belepesi pontja.
- `get_all_data_tesco.py`: aktualis kategoriak es termekek letoltese.
- `filter_data_tesco.py`: a nyers Tesco CSV fontosabb oszlopainak megtartasa.
- `normalize_data_tesco.py`: Tesco mezok atalakítása a kozos 18 oszlopos
  `*_normalized_data_*.csv` semara.
- `kategoriak.txt`: a legutobb felfedezett Tesco fo fetch-kategoriak.

## Kimenetek

A szkriptek a `data/markets_data/` mappaba irnak:

- `tesco_fetch_categories_*.csv`: a landing oldalrol felfedezett fo
  fetch-kategoriak.
- `tesco_categories_*.csv`: a letoltott termekekbol ujraepitett reszletes
  kategoriafa.
- `tesco_all_data_*.csv`: nyers, lapozott GraphQL termekadatok.
- `tesco_filtered_data_*.csv`: lenyegesebb nyers oszlopokra szukitett CSV.
- `tesco_normalized_data_*.csv`: SPAR/Prima-val azonos kimeneti sema.

## Futtatas

```powershell
cd src\markets\Tesco
python main_tesco.py
```

Gyors proba egy-ket kategoriaval:

```powershell
python get_all_data_tesco.py --category-limit 2 --page-limit 1
python normalize_data_tesco.py
```
