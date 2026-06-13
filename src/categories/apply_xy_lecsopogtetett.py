import csv
import re
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

# "X egyseg / Y egyseg" vagy "X egyseg (Y egyseg)" ket-erteku nev: a nagyobb a
# brutto toltotomeg, a kisebb a lecsopogtetett -> a KISEBB a kiszereles
# (2026-06-13 felhasznaloi dontes). Csak azonos egysegu parokat kezelunk, es
# csak ha a ket ertek tenyleg ket kulonbozo tomeg (nem meretkod, mint 100/200).

REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "data" / "categories" / "kiszereles_audit.csv"
CORR = REPO / "data" / "categories" / "kiszereles_korrekciok.csv"

PAIR = re.compile(
    r"(\d+(?:[.,]\d+)?)\s*(g|kg|ml|l|dl|cl)\s*[/(]\s*(\d+(?:[.,]\d+)?)\s*(g|kg|ml|l|dl|cl)\s*\)?",
    re.IGNORECASE,
)


def to_base(value, unit):
    value = float(value.replace(",", "."))
    unit = unit.lower()
    if unit in ("kg", "l"):
        return value * 1000
    if unit == "dl":
        return value * 100
    if unit == "cl":
        return value * 10
    return value


MULTIPACK = re.compile(r"\d+\s*x\s*\d", re.IGNORECASE)


def xy_value(name):
    m = PAIR.search(name)
    if not m:
        return None
    a = to_base(m.group(1), m.group(2))
    b = to_base(m.group(3), m.group(4))
    if a <= 0 or b <= 0:
        return None
    smaller, larger = min(a, b), max(a, b)
    if (larger - smaller) / larger < 0.05:
        return None
    # "N x M (osszeg)" multipack -> a TELJES csomag (nagyobb). Egyebkent a par
    # brutto/lecsopogtetett -> a kisebb (lecsopogtetett) ertek.
    is_multipack = bool(MULTIPACK.search(name))
    target = larger if is_multipack else smaller
    if target == a:
        unit = m.group(2).lower()
    else:
        unit = m.group(4).lower()
    base_unit = "ml" if unit in ("ml", "l", "dl", "cl") else "g"
    indok = ("N x M multipack: a teljes csomag" if is_multipack
             else "X/Y ketertekes nev: a kisebb (lecsopogtetett) ertek")
    return round(target, 3), base_unit, indok


def main():
    existing = {}
    if CORR.exists():
        with open(CORR, mode="r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                if row.get("forras") == "kezi:xy_lecsopogtetett":
                    continue
                existing[(row["store_name"], row["store_product_id"])] = row

    applied = []
    with open(AUDIT, mode="r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            if row["tipus"] != "nev_elteres":
                continue
            result = xy_value(row["product_name"])
            if result is None:
                continue
            value, unit, indok = result
            key = (row["store_name"], row["store_product_id"])
            if key in existing and existing[key].get("forras", "").startswith("kezi:") and existing[key]["forras"] != "kezi:xy_lecsopogtetett":
                continue
            existing[key] = {
                "store_name": row["store_name"], "store_product_id": row["store_product_id"],
                "product_name": row["product_name"], "korrekcio_tipus": "kiszereles",
                "eredeti_mennyiseg": row["unit_step"], "eredeti_egyseg": row["unit_type"],
                "javitott_mennyiseg": f"{value:g}", "javitott_egyseg": unit,
                "indok": indok,
                "forras": "kezi:xy_lecsopogtetett",
            }
            applied.append((row["store_name"], row["product_name"], value, unit, indok))

    fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus",
              "eredeti_mennyiseg", "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg",
              "indok", "forras"]
    with open(CORR, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing.values())

    print(f"X/Y + multipack korrekciok: {len(applied)}")
    for store, name, value, unit, indok in applied:
        tag = "MP" if "multipack" in indok else "lecs"
        print(f"  [{store:6s}][{tag}] {name[:58]} -> {value:g} {unit}")


if __name__ == "__main__":
    main()
