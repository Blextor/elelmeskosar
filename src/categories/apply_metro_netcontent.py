import csv
import glob
import os
import re
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

# Metro hiteles kiszereles-jellemzo (2026-06-13 felhasznaloi eszrevetel):
# a Metro termekoldal "Jellemzok" fule a netContentVolume / netPieceWeight
# mezonek felel meg a nyers adatban. Ez megbizhatobb, mint a nevbol valo
# parse vagy a "+" osszeadas (pl. Unicum B&N "700 ml+400 ml" valojaban 780 ml,
# St. Hubertus "500 ml + 40 ml" valojaban 540 ml).
#
# Hatokor: a "+" mintas Metro termekek (ahol a nev-alapu becsles bizonyitottan
# felrevezet). A netContentVolume (ital, ML) vagy netPieceWeight (szilard, GRAM)
# adja a helyes erteket.

REPO = Path(__file__).resolve().parents[2]
CORR = REPO / "data" / "categories" / "kiszereles_korrekciok.csv"
# A felhasznaloi dontes (2026-06-13): a Metro jellemzo (netContentVolume) csak
# ITALOKNAL hasznalando alapertelmezetten - ott a hiteles (a "+"-os palack/mini
# osszeget jol adja, a pohar/adagolo/bogre tartozekot eleve nem szamolja bele).
# Mas ter(meknel a jellemzo a brutto toltotomeg, ami a lecsopogtetett konzerveknel
# es glazuros tengeri termekeknel rosszabb -> ott marad az API.
# Ezert: barmely "+"-os ital, ahol a nevbeli kiszereles felrevezet.
PLUS = re.compile(r"\+")
ITAL = re.compile(
    r"whisk|vodka|likőr|likor|\brum\b|\bgin\b|pálinka|palinka|\bbor\b|pezsgő|pezsgo|"
    r"unicum|konyak|cognac|brandy|tequila|jäger|jager|aperol|vermut|baileys|chivas|"
    r"jim beam|jack daniel|\bsör\b|\bsor\b|whiskey|bourbon|szesz|gyógynövénylikőr|gyognovenylikor",
    re.IGNORECASE,
)
# Nem ital, meg ha az ITAL regex rallik is (pl. "pezsgotabletta" -> "pezsgo").
NEM_ITAL = re.compile(r"tabletta|étrend-kiegészítő|etrend-kiegeszito|vitamin|pezsgőtab|pezsgotab", re.IGNORECASE)


def to_float(value):
    try:
        return float(str(value).replace(",", "."))
    except (TypeError, ValueError):
        return None


def main():
    metro_file = max(glob.glob(str(REPO / "data" / "markets_data" / "metro_all_data_*.csv")), key=os.path.getmtime)

    existing = {}
    if CORR.exists():
        with open(CORR, encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("forras") == "kezi:metro_jellemzo":
                    continue
                existing[(r["store_name"], r["store_product_id"])] = r

    applied = []
    with open(metro_file, encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            name = (row.get("bundle.description") or row.get("variant.description") or "").strip()
            if not PLUS.search(name) or not ITAL.search(name) or NEM_ITAL.search(name):
                continue
            pid = (row.get("bundle_id") or row.get("bundle.bundleId.bettyBundleId")
                   or row.get("variant_id") or row.get("search_result_id") or "").strip()
            if not pid:
                continue
            vol = to_float(row.get("bundle.contentData.netContentVolume.value"))
            vol_uom = (row.get("bundle.contentData.netContentVolume.uom") or "").strip().upper()
            wgt = to_float(row.get("bundle.contentData.netPieceWeight.value"))
            wgt_uom = (row.get("bundle.contentData.netPieceWeight.uom") or "").strip().upper()
            if vol and vol_uom in ("ML", "L"):
                value = vol * (1000 if vol_uom == "L" else 1)
                unit = "ml"
            elif wgt and wgt_uom in ("GRAM", "G", "KG"):
                value = wgt * (1000 if wgt_uom == "KG" else 1)
                unit = "g"
            else:
                continue
            existing[("Metro", pid)] = {
                "store_name": "Metro", "store_product_id": pid, "product_name": name,
                "korrekcio_tipus": "kiszereles", "eredeti_mennyiseg": "", "eredeti_egyseg": unit,
                "javitott_mennyiseg": f"{value:g}", "javitott_egyseg": unit,
                "indok": f"Metro jellemzo (netContentVolume/netPieceWeight): {value:g} {unit}",
                "forras": "kezi:metro_jellemzo",
            }
            applied.append((name, value, unit))

    fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus",
              "eredeti_mennyiseg", "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg",
              "indok", "forras"]
    with open(CORR, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing.values())

    print(f"Metro jellemzo ('+' termekek) korrekciok: {len(applied)}")
    for name, value, unit in applied:
        print(f"  {name[:62]:62s} -> {value:g} {unit}")
    print(f"Korrekcios sorok osszesen: {len(existing)}")


if __name__ == "__main__":
    main()
