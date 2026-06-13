import csv
import glob
import os
import re
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

# "+" osszeadas szabaly (2026-06-13 felhasznaloi dontes):
# Ha egy termek nevben ket kiszereles van "+"-szal osszekotve, ES mindketto
# onallo, teljes erteku fogyaszthato termek (jellemzoen ital: nagy palack +
# mini ugyanabbol/hasonlobol), akkor a ket mennyiseg OSSZEADODIK.
# Ez ELTER a tartozek-esettol (camembert + fuszer/szosz), ahol a "+" utani
# tetel csak kiegeszito -> csak a fo termek szamit (azt az apply_kep_review
# kezeli).
#
# A megkulonbozteto jel: a termek ITAL. Italnal a "+ X ml/l" masodik palack;
# etelnel a "+ X g szosz/fuszer" tartozek.

ITAL = re.compile(
    r"whisk|vodka|likőr|likor|\brum\b|\bgin\b|pálinka|palinka|\bbor\b|pezsgő|pezsgo|"
    r"unicum|konyak|cognac|brandy|tequila|jäger|jager|aperol|vermut|"
    r"\bsör\b|\bsor\b|whiskey|bourbon|szesz|gyógynövénylikőr|gyognovenylikor",
    re.IGNORECASE,
)
# Tartozek/ajandek a "+" utan, amit NEM adunk hozza (meg ital eseten sem).
PLUS_TARTOZEK = re.compile(r"pohár|pohar|díszdoboz|diszdoboz|ajándék(?! mini)|ajandek(?! mini)", re.IGNORECASE)

VOLUME = re.compile(r"(\d+(?:[.,]\d+)?)\s*(l|ml|cl|dl)\b", re.IGNORECASE)
PLUS = re.compile(r"\+")
# Pohar/tárgy + terfogata: ez NEM ital-mennyiseg, eltavolitando a szamolas elott.
POHAR_VOLUME = re.compile(
    r"(?:pohár|pohar|kulacs|bögre|bogre)\s*\d+(?:[.,]\d+)?\s*(?:l|ml|cl|dl)\b"
    r"|\d+(?:[.,]\d+)?\s*(?:l|ml|cl|dl)(?:-es|-os|-ös)?\s*(?:pohár|pohar|kulacs|bögre|bogre)",
    re.IGNORECASE,
)


def to_ml(value, unit):
    value = float(value.replace(",", "."))
    unit = unit.lower()
    return value * {"l": 1000, "dl": 100, "cl": 10, "ml": 1}[unit]


def repo_root():
    return Path(__file__).resolve().parents[2]


def latest_normalized_files():
    result = {}
    rx = re.compile(r"(.+)_normalized_data_(\d{8}_\d{6})\.csv$")
    for file_name in glob.glob(str(repo_root() / "data" / "markets_data" / "*_normalized_data_*.csv")):
        path = Path(file_name)
        match = rx.match(path.name)
        if not match:
            continue
        key = match.group(1)
        if key not in result or path.stat().st_mtime > result[key].stat().st_mtime:
            result[key] = path
    return result


def plus_sum(name):
    # Csak akkor, ha van "+" ES a termek ital.
    if not PLUS.search(name) or not ITAL.search(name):
        return None
    # A pohar/targy + terfogata NEM ital-mennyiseg -> eltavolitjuk a szamolas elott.
    clean = POHAR_VOLUME.sub(" ", name)
    volumes = VOLUME.findall(clean)
    if len(volumes) < 2:
        return None
    parts = [to_ml(v, u) for v, u in volumes]
    return round(sum(parts), 3), parts


def main():
    corr_path = repo_root() / "data" / "categories" / "kiszereles_korrekciok.csv"
    existing = {}
    if corr_path.exists():
        with open(corr_path, mode="r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                # A sajat korabbi "+" sorainkat eldobjuk -> idempotens ujraszamolas.
                if row.get("forras") == "kezi:plus_osszeg":
                    continue
                existing[(row["store_name"], row["store_product_id"])] = row

    applied = []
    for store_key, path in sorted(latest_normalized_files().items()):
        # A Metro-nal a strukturalt netContentVolume jellemzo a hiteles
        # (apply_metro_netcontent.py kezeli), a nevbol valo osszeadas felrevezet
        # (pl. Unicum B&N "700 ml+400 ml" valojaban 780 ml).
        if store_key == "metro":
            continue
        with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                name = (row.get("product_name") or "").strip()
                unit = (row.get("unit_type") or "").strip().lower()
                if unit not in ("ml", "l"):
                    continue
                result = plus_sum(name)
                if result is None:
                    continue
                total, parts = result
                key = ((row.get("store_name") or "").strip(), (row.get("store_product_id") or "").strip())
                step = row.get("unit_step", "")
                existing[key] = {
                    "store_name": key[0], "store_product_id": key[1], "product_name": name,
                    "korrekcio_tipus": "kiszereles", "eredeti_mennyiseg": step, "eredeti_egyseg": unit,
                    "javitott_mennyiseg": f"{total:g}", "javitott_egyseg": "ml",
                    "indok": f"'+' osszeadas: ket onallo ital-kiszereles ({'+'.join(f'{p:g}' for p in parts)} ml)",
                    "forras": "kezi:plus_osszeg",
                }
                applied.append((key[0], name, total))

    fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus",
              "eredeti_mennyiseg", "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg",
              "indok", "forras"]
    with open(corr_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing.values())

    print(f"'+' osszeadas korrekciok: {len(applied)}")
    for store, name, total in applied:
        print(f"  [{store}] {name[:66]} -> {total:g} ml")
    print(f"Korrekcios sorok osszesen: {len(existing)}")


if __name__ == "__main__":
    main()
