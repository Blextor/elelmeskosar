import csv
import re
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

# A 2026-06-12-i felhasznaloi mintazat-dontesek alkalmazasa a kiszereles-audit
# jeloltjeire. A kimenet a kiszereles_korrekciok.csv-be kerul (merge, a kezi
# es ledig sorok erintetlenul maradnak):
#   - multipack_karton: a nev szerinti TELJES mennyiseg a kiszereles
#   - tesco lecsopogtetett (API drained): a lecsopogtetett ertek
#   - zarojeles "X g (Y g)" nevek: a zarojeles (lecsopogtetett) ertek
#   - konzerv_api_kisebb: MEGEROSITES - az API kisebb (lecsopogtetett velelmu)
#     erteke marad; a sor eldontottnek szamit
# Az egyseg_elteres es a tobbi csoport NEM kerul ide: darabonkenti review.

REPO = Path(__file__).resolve().parents[2]
AUDIT = REPO / "data" / "categories" / "kiszereles_audit.csv"
CORR = REPO / "data" / "categories" / "kiszereles_korrekciok.csv"

KONZERV = re.compile(
    r"konzerv|lében|leben|olajban|befőtt|befott|savany|uborka|olíva|oliva|bab\b|kukorica|"
    r"hal\b|tonhal|szardínia|gomba|cékla|paprika|kompót|ananász",
    re.IGNORECASE,
)

# Egyseg-elteres szabalyok (2026-06-12 felhasznaloi dontes):
# szosz/ontet/savanyusag jellegu -> GRAMM nyer; bor/olaj/ital -> ML nyer.
SZOSZ_GRAMM = re.compile(
    r"szósz|szosz|sauce|mártás|martas|öntet|ontet|majonéz|majonez|ketchup|mustár|mustar|"
    r"dresszing|tartár|tartar|remulád|remulad|pesto|savanyúság|savanyusag|uborka|"
    r"torma|habspray|krém|krem|pác\b|pac\b|lekvár|lekvar|paszta|befőtt|befott|"
    r"kompót|kompot|lében|leben|vízben|vizben|sriracha|jalapeno|gyöngyhagyma|gyongyhagyma",
    re.IGNORECASE,
)
LEVES_SKIP = re.compile(r"leves|halászlé|halaszle", re.IGNORECASE)
DUPLA_G = re.compile(r"\d[\d.,]*\s*(?:g|kg)\b", re.IGNORECASE)
DUPLA_ML = re.compile(r"\d[\d.,]*\s*(?:ml|l)\b", re.IGNORECASE)
ITAL_ML = re.compile(
    r"bor\b|vörösbor|vorosbor|fehérbor|feherbor|rozé|roze|pezsgő|pezsgo|sör|"
    r"olaj|ecet|szörp|szorp|syrup|üdítő|udito|juice|nektár|nektar|ital\b|víz\b|viz\b|"
    r"ásványvíz|asvanyviz|likőr|likor|szorbé|szorbe|jégnyalóka|jegnyaloka|jégkrém|jegkrem|"
    r"spray|aroma",
    re.IGNORECASE,
)

# Tejtermek-szabalyok (2026-06-12 felhasznaloi dontes):
# joghurt/tejfol/kefir -> GRAMM; tejszin-felek (haspray is) -> ML;
# jegeskave/tej/tejital -> ML. A sorrend szamit (a "tejfol" ne essen a
# "tej" ml-szabalya ala).
TEJTERMEK_GRAMM = re.compile(r"joghurt|tejföl|tejfol|kefir|kefír", re.IGNORECASE)
TEJSZIN_ML = re.compile(r"tejszín|tejszin", re.IGNORECASE)
TEJITAL_ML = re.compile(
    r"jegeskávé|jegeskave|kávéital|kaveital|tejital|latte|cappuccino|macchiato|tej\b",
    re.IGNORECASE,
)
ZAROJELES = re.compile(r"\(\s*\d+[.,]?\d*\s*(?:g|ml|kg|l)\s*\)", re.IGNORECASE)
MULTIPACK_X = re.compile(r"\d\s*x\s*\d", re.IGNORECASE)


def to_float(value):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def classify(row):
    tipus = row["tipus"]
    name = row["product_name"]
    step = to_float(row["unit_step"])
    suggested = to_float(row["javasolt_mennyiseg"])
    if tipus == "ledig":
        return None
    if tipus == "lecsopogtetett_api":
        return "tesco_drained"
    if tipus == "egyseg_elteres":
        # A gramm/ml szabalyok; amelyik oldal a megfelelo egyseget adja, az
        # nyer. Ha egyik token sem illik, marad darabonkenti review.
        if SZOSZ_GRAMM.search(name):
            if row["javasolt_egyseg"] == "g":
                return "szosz_gramm_nev"
            if row["unit_type"] == "g":
                return "szosz_gramm_api"
        if TEJTERMEK_GRAMM.search(name):
            if row["javasolt_egyseg"] == "g":
                return "tejtermek_gramm_nev"
            if row["unit_type"] == "g":
                return "tejtermek_gramm_api"
        if TEJSZIN_ML.search(name):
            if row["javasolt_egyseg"] == "ml":
                return "tejszin_ml_nev"
            if row["unit_type"] == "ml":
                return "tejszin_ml_api"
        if TEJITAL_ML.search(name):
            if row["javasolt_egyseg"] == "ml":
                return "tejital_ml_nev"
            if row["unit_type"] == "ml":
                return "tejital_ml_api"
        if ITAL_ML.search(name):
            if row["javasolt_egyseg"] == "ml":
                return "ital_ml_nev"
            if row["unit_type"] == "ml":
                return "ital_ml_api"
        # Dupla deklaracio a nevben (g ES ml is): a gramm a tomeg-deklaracio.
        if DUPLA_G.search(name) and DUPLA_ML.search(name):
            if row["javasolt_egyseg"] == "g":
                return "dupla_gramm_nev"
            if row["unit_type"] == "g":
                return "dupla_gramm_api"
        # Egyebkent a nev sajat egysege a gyartoi konvencio (a szilard termek
        # nem ml, a folyadek nem gramm).
        if row["javasolt_egyseg"] in ("g", "ml"):
            return "nev_egyseg_nyer"
        return None
    if suggested and step and step > 0:
        ratio = suggested / step
        # Ha a nevben explicit "N x M" minta van (HoReCa kiszerelesek is, pl.
        # 150 x 35 g), nincs szorzo-plafon; anelkul max 40x.
        max_ratio = 1000 if MULTIPACK_X.search(name) else 40
        if ratio > 1.5 and abs(ratio - round(ratio)) / ratio < 0.03 and 2 <= round(ratio) <= max_ratio:
            return "multipack_karton"
        # Plauzibilitas: ha az egyik ertek elelmiszer-kiszereleskent abszurd
        # (pl. 470 000 g ketchup, 75 l pezsgo, 0,33 ml sor), a masik nyer.
        unit = row["unit_type"]
        if unit in ("g", "ml"):
            low, high = (0.1, 30000) if unit == "g" else (10, 12000)
            step_ok = low <= step <= high
            sugg_ok = low <= suggested <= high
            if step_ok and not sugg_ok:
                return "plauzibilis_api"
            if sugg_ok and not step_ok:
                return "plauzibilis_nev"
    if ZAROJELES.search(name) and not MULTIPACK_X.search(name) and suggested and step and suggested < step:
        return "zarojeles_lecsopogtetett"
    if suggested and step and suggested > step and KONZERV.search(name):
        return "konzerv_megerosites"
    return None


def main():
    existing = {}
    if CORR.exists():
        with open(CORR, mode="r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                existing[(row["store_name"], row["store_product_id"])] = row

    applied = {"multipack_karton": 0, "tesco_drained": 0, "zarojeles_lecsopogtetett": 0,
               "konzerv_megerosites": 0, "szosz_gramm_nev": 0, "szosz_gramm_api": 0,
               "ital_ml_nev": 0, "ital_ml_api": 0, "tejtermek_gramm_nev": 0,
               "tejtermek_gramm_api": 0, "tejszin_ml_nev": 0, "tejszin_ml_api": 0,
               "tejital_ml_nev": 0, "tejital_ml_api": 0, "dupla_gramm_nev": 0,
               "dupla_gramm_api": 0, "nev_egyseg_nyer": 0, "plauzibilis_api": 0,
               "plauzibilis_nev": 0}
    with open(AUDIT, mode="r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            decision = classify(row)
            if decision is None:
                continue
            key = (row["store_name"], row["store_product_id"])
            if key in existing and existing[key].get("forras", "").startswith("kezi"):
                continue  # kezi bejegyzest sosem irunk felul
            if decision.endswith("_api"):
                correction = {
                    "store_name": row["store_name"], "store_product_id": row["store_product_id"],
                    "product_name": row["product_name"], "korrekcio_tipus": "megerosites",
                    "eredeti_mennyiseg": row["unit_step"], "eredeti_egyseg": row["unit_type"],
                    "javitott_mennyiseg": row["unit_step"], "javitott_egyseg": row["unit_type"],
                    "indok": "egyseg-szabaly: az API egysege a helyes (szosz=g, ital/olaj=ml)",
                    "forras": f"mintazat:{decision}",
                }
            elif decision == "konzerv_megerosites":
                correction = {
                    "store_name": row["store_name"], "store_product_id": row["store_product_id"],
                    "product_name": row["product_name"], "korrekcio_tipus": "megerosites",
                    "eredeti_mennyiseg": row["unit_step"], "eredeti_egyseg": row["unit_type"],
                    "javitott_mennyiseg": row["unit_step"], "javitott_egyseg": row["unit_type"],
                    "indok": "API kisebb erteke lecsopogtetett velelmu - megerositve (mintazat-dontes)",
                    "forras": "mintazat:konzerv_megerosites",
                }
            else:
                correction = {
                    "store_name": row["store_name"], "store_product_id": row["store_product_id"],
                    "product_name": row["product_name"], "korrekcio_tipus": "kiszereles",
                    "eredeti_mennyiseg": row["unit_step"], "eredeti_egyseg": row["unit_type"],
                    "javitott_mennyiseg": row["javasolt_mennyiseg"], "javitott_egyseg": row["javasolt_egyseg"],
                    "indok": row["indok"],
                    "forras": f"mintazat:{decision}",
                }
            existing[key] = correction
            applied[decision] += 1

    fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus",
              "eredeti_mennyiseg", "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg",
              "indok", "forras"]
    with open(CORR, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing.values())

    print(f"Korrekcios sorok osszesen: {len(existing)} -> {CORR}")
    for decision, count in applied.items():
        print(f"  {decision}: {count}")


if __name__ == "__main__":
    main()
