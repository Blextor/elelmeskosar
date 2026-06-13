import csv
import glob
import re
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

# A 13 hal/tengeri termek kepes review verdiktjei (2026-06-13).
# kulcs: nev-reszlet; ertek: (javitott_mennyiseg_g, indok)
# A glazurozott (20% glazur/GL) termekeknel a netto (glazur nelkuli) tomeg a
# helyes, amit az API mar kiszamolt; toltotomeg-konzervnel a toltotomeg;
# sos leben/olajban tonhalnal a lecsopogtetett (nevbeli) ertek.

VERDIKT = [
    ("cápaharcsafilé 20% glazúr", 800, "glazúr levonva, nettó haltartalom (kép)"),
    ("Viking alaszkai tőkehalfilé", 85, "címke: töltőtömeg 85 g"),
    ("Riga Gold halgombóc paradicsom", 240, "paradicsomszósz fogyasztható, teljes nettó"),
    ("halkidiki olajbogyó", 180, "olajbogyó lében, lecsöpögtetett (kép)"),
    ("Pangasius Filé 20% Glazúr", 4000, "glazúr levonva, nettó (kép)"),
    ("METRO Chef Garnélarák 1,7", 1700, "címke: töltőtömeg 1,7 kg"),
    ("Garnélafarok 41/50 20%", 800, "glazúr levonva, nettó"),
    ("Seacon Gyorsfagyasztott Óriás Garnélarák 16/20 20%", 800, "glazúr levonva, nettó"),
    ("METRO Chef Tonhal Darabok Sós Lében", 1300, "kép: 1705 g bruttó, 1,3 kg lecsöpögtetett"),
    ("METRO Chef Tonhal Darabok Napraforgó Olajban", 1260, "lecsöpögtetett 1,26 kg, 1705 g bruttó"),
    ("Rozmár gyorsfagyasztott glazúrozott tilápia", 800, "kép: 800 g csomagtömeg"),
    ("SeaFood Hungary fűszervajas sous vide lazac", 150, "deklarált 150 g"),
    ("SeaFood Hungary fokhagymás-zöldfűszeres sous vide lazac", 150, "deklarált 150 g"),
]

REPO = Path(__file__).resolve().parents[2]
CORR = REPO / "data" / "categories" / "kiszereles_korrekciok.csv"


def latest_normalized():
    result = {}
    rx = re.compile(r"(.+)_normalized_data_(\d{8}_\d{6})\.csv$")
    for fn in glob.glob(str(REPO / "data" / "markets_data" / "*_normalized_data_*.csv")):
        p = Path(fn)
        m = rx.match(p.name)
        if m and (m.group(1) not in result or p.stat().st_mtime > result[m.group(1)].stat().st_mtime):
            result[m.group(1)] = p
    return result


def main():
    # Termekek beolvasasa (store_product_id + step a kulcshoz)
    products = []
    for path in latest_normalized().values():
        with open(path, encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                products.append((r.get("store_name", ""), r.get("store_product_id", ""),
                                 r.get("product_name", ""), r.get("unit_step", ""), r.get("unit_type", "")))

    existing = {}
    if CORR.exists():
        with open(CORR, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("forras") == "kezi:hal_review":
                    continue
                existing[(r["store_name"], r["store_product_id"])] = r

    applied = 0
    for frag, value, indok in VERDIKT:
        for store, pid, name, step, unit in products:
            if frag.lower() in name.lower():
                existing[(store, pid)] = {
                    "store_name": store, "store_product_id": pid, "product_name": name,
                    "korrekcio_tipus": "kiszereles", "eredeti_mennyiseg": step, "eredeti_egyseg": unit,
                    "javitott_mennyiseg": str(value), "javitott_egyseg": "g",
                    "indok": f"hal kepes review: {indok}", "forras": "kezi:hal_review",
                }
                applied += 1

    fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus",
              "eredeti_mennyiseg", "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg",
              "indok", "forras"]
    with open(CORR, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing.values())
    print(f"Hal review korrekciok: {applied} | korrekcios sorok: {len(existing)}")


if __name__ == "__main__":
    main()
