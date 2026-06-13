import csv
from pathlib import Path

import pandas as pd


# A 87 nagy (>50%) nev-elteres kepes/logikai atvizsgalasanak verdiktjei
# (2026-06-12, Claude kepes review + cimke-leolvasasok). A sorszamok a
# big87.csv diff szerint csokkeno sorrendjere vonatkoznak.
# Akcio: "nev" = a nev szerinti javasolt ertek; "api" = az API erteke
# megerositve; ("ertek", X) = kezi ertek (pl. mellekelt tetel nelkuli fo
# termek); "nonfood" = kiszuresre (pelenka).

VERDIKT = {
    1: ("nev", None, "safrany: a 0,12 g valos kiszereles"),
    2: ("nonfood", None, "pelenkatarolo zacsko - nem elelmiszer"),
    3: ("api", None, "kep: 60 db-os vodor, 60x18=1080 g"),
    4: ("nonfood", None, "bugyipelenka - nem elelmiszer"),
    5: ("nonfood", None, "bugyipelenka - nem elelmiszer"),
    6: ("ertek", 200, "fo termek 2x100 g camembert, +5 g fuszer mellekelt"),
    7: ("ertek", 200, "fo termek 2x100 g camembert, +5 g fuszer mellekelt"),
    8: ("ertek", 400, "fo termek 4x100 g camembert, fuszer mellekelt"),
    9: ("api", None, "Metro rekesz: 24x330 ml = 7920 ml"),
    10: ("ertek", 700, "Unicum 700 ml + 40 ml mellekelt mini"),
    11: ("api", None, "bor 750 ml; a nevbeli 50 ml eliras"),
    12: ("api", None, "500 ml fo termek + 40 ml mellekelt mini"),
    13: ("api", None, "500 ml fo termek + 40 ml mellekelt mini"),
    14: ("nev", None, "croissant 80 g; API 950 abszurd"),
    15: ("nev", None, "Auchan x10 tizedeshiba"),
    16: ("nev", None, "tasak 42 g; API x10"),
    17: ("api", None, "Metro mini ital karton: 10x20 ml"),
    18: ("nev", None, "Auchan x10 tizedeshiba"),
    19: ("api", None, "Metro mini ital karton: 10x10 ml"),
    20: ("nev", None, "tasak 21 g; API x10"),
    21: ("nev", None, "kep: egyetlen szelet, 23,5 g"),
    22: ("nev", None, "Auchan x10 tizedeshiba"),
    23: ("api", None, "Metro mini ital karton: 10x20 ml"),
    24: ("nev", None, "Auchan x10 tizedeshiba"),
    25: ("nev", None, "Auchan x10 tizedeshiba-minta"),
    26: ("api", None, "Metro mini ital karton: 10x35 ml"),
    27: ("api", None, "Metro mini ital karton: 10x20 ml"),
    28: ("api", None, "tonhalsalata 160 g; a nevbeli 16 csonka"),
    29: ("api", None, "Alpro 4-es csomag: 400 g"),
    30: ("nev", None, "chips-taller 70 g; API x10"),
    31: ("nev", None, "tasak 27 g; API x10"),
    32: ("nev", None, "16 kapszula 99,2 g; API x10"),
    33: ("nev", None, "tasak 100 g; API ar-derivalt hiba"),
    34: ("nev", None, "safrany: 0,12 g valos"),
    35: ("ertek", 400, "fo termek 4x100 g camembert, szosz mellekelt"),
    36: ("nev", None, "fuszerkeverek 100 g"),
    37: ("ertek", 200, "fo termek 2x100 g camembert, +30 g szosz mellekelt"),
    38: ("ertek", 200, "fo termek 2x100 g camembert, +30 g szosz mellekelt"),
    39: ("ertek", 200, "fo termek 2x100 g camembert, +30 g szosz mellekelt"),
    40: ("ertek", 200, "fo termek 2x100 g camembert, +30 g szosz mellekelt"),
    41: ("nev", None, "600 g; API ar-derivalt hiba"),
    42: ("nev", None, "1 kg-os desszert; API ar-derivalt hiba"),
    43: ("nev", None, "1 kg-os desszert; API ar-derivalt hiba"),
    44: ("nev", None, "1 kg-os desszert; API ar-derivalt hiba"),
    45: ("nev", None, "20x1,5 g = 30 g tea"),
    46: ("ertek", 200, "fo termek 2x100 g sajt, +50 g szosz mellekelt"),
    47: ("ertek", 700, "whisky 0,7 l + 0,2 l mellekelt mini"),
    48: ("ertek", 160, "fo termek 2x80 g sajtrud, +50 g szosz mellekelt"),
    49: ("api", None, "kep: 4x125 g = 500 g negyes csomag"),
    50: ("api", None, "4 palack x 0,33 l = 1320 ml"),
    51: ("api", None, "4x125 g = 500 g negyes csomag"),
    52: ("api", None, "4x130 g = 520 g negyes csomag"),
    53: ("api", None, "4x125 g = 500 g negyes csomag"),
    54: ("ertek", 700, "whisky 0,7 l + 0,2 l mellekelt mini"),
    55: ("api", None, "4x125 g = 500 g negyes csomag"),
    56: ("api", None, "kep: 500 g (4x125 g)"),
    57: ("nev", None, "kep cimke: 400 g (4x100 g)"),
    58: ("api", None, "4x50 g = 200 g multipack"),
    59: ("api", None, "4:1 arany, nem mennyiseg; 375 g helyes"),
    60: ("api", None, "4:1 arany, nem mennyiseg; 375 g helyes"),
    61: ("api", None, "4:1 arany, nem mennyiseg; 375 g helyes"),
    62: ("api", None, "4:1 arany, nem mennyiseg; 375 g helyes"),
    63: ("nev", None, "500 g szendvicskeksz; API ar-derivalt"),
    64: ("nev", None, "Knorr levespor tasak 51 g"),
    65: ("nev", None, "kep: 1 doboz 25 filter = 25 g; API 3 doboz"),
    66: ("api", None, "3x40 g = 120 g csomag"),
    67: ("api", None, "kep: kis pohar, 55 g; nevbeli 155 eliras"),
    68: ("api", None, "kep cimke: Netto tomeg 180 g; nevbeli 500 hibas"),
    69: ("nev", None, "safrany 0,375 g valos"),
    70: ("api", None, "kep: egesz pulykamell ~1 kg"),
    71: ("nev", None, "kep cimke: NETTO TOMEG 100 G"),
    72: ("nev", None, "ontetpor tasak 50 g"),
    73: ("nev", None, "400 ml szosz; API x2,5 hiba"),
    74: ("api", None, "mozzarella 125 g lecsopogtetett (280 g leben)"),
    75: ("nev", None, "8-as multipack jegkrem 400 ml"),
    76: ("api", None, "olajbogyo lecsopogtetett 105 g"),
    77: ("api", None, "olajbogyo lecsopogtetett 105 g"),
    78: ("nev", None, "kep: nagy tablas Roshen Wafers 216 g"),
    79: ("nev", None, "2x100 g = 200 g"),
    80: ("nev", None, "2x100 g = 200 g"),
    81: ("nev", None, "szoszos bab: a teljes 430 g eheto"),
    82: ("nev", None, "szoszos bab: a teljes 430 g eheto"),
    83: ("nev", None, "szoszos bab: a teljes 430 g eheto"),
    84: ("nev", None, "szoszos bab: a teljes 430 g eheto"),
    85: ("api", None, "olajbogyo lecsopogtetett 160 g"),
    86: ("api", None, "kep: standard 190 g-os HiPP uveg; nevbeli 90 hibas"),
    87: ("nev", None, "50x2,5 g = 125 g kapszula"),
}

REPO = Path(__file__).resolve().parents[2]
big = pd.read_csv(r"c:\Users\Bobo\AppData\Local\Temp\big87.csv", dtype=str, keep_default_na=False)
corr_path = REPO / "data" / "categories" / "kiszereles_korrekciok.csv"

existing = {}
with open(corr_path, mode="r", encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file):
        existing[(row["store_name"], row["store_product_id"])] = row

applied = {"nev": 0, "api": 0, "ertek": 0, "nonfood_skip": 0}
for index, (_, row) in enumerate(big.iterrows(), start=1):
    action, value, indok = VERDIKT[index]
    key = (row["store_name"], row["store_product_id"])
    if action == "nonfood":
        applied["nonfood_skip"] += 1
        continue  # a nonfood szures kezeli (nev-token: pelenka)
    if action == "nev":
        javitott, tipus = row["javasolt_mennyiseg"], "kiszereles"
    elif action == "api":
        javitott, tipus = row["unit_step"], "megerosites"
    else:
        javitott, tipus = str(value), "kiszereles"
    existing[key] = {
        "store_name": row["store_name"], "store_product_id": row["store_product_id"],
        "product_name": row["product_name"], "korrekcio_tipus": tipus,
        "eredeti_mennyiseg": row["unit_step"], "eredeti_egyseg": row["unit_type"],
        "javitott_mennyiseg": javitott, "javitott_egyseg": row["unit_type"],
        "indok": f"kepes review: {indok}", "forras": "kezi:kep_review",
    }
    applied[action] += 1

fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus",
          "eredeti_mennyiseg", "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg",
          "indok", "forras"]
with open(corr_path, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(existing.values())

print(f"Korrekcios sorok: {len(existing)}")
print("alkalmazva:", applied)
