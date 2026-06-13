import csv
import glob
import os
import re
from collections import Counter
from pathlib import Path

csv.field_size_limit(1024 * 1024 * 1024)
REPO = Path(__file__).resolve().parents[2]
CATDIR = REPO / "data" / "categories"
AUDIT = CATDIR / "kiszereles_audit.csv"
CORR = CATDIR / "kiszereles_korrekciok.csv"
KETES = CATDIR / "kiszereles_review_ketes.csv"


def tof(v):
    try:
        return float(str(v).replace(",", "."))
    except (TypeError, ValueError):
        return None


def pid_of(r):
    return (r.get("bundle_id") or r.get("bundle.bundleId.bettyBundleId") or r.get("variant_id") or r.get("search_result_id") or "").strip()


# Metro jellemzo
jell = {}
mall = max(glob.glob(str(REPO / "data" / "markets_data" / "metro_all_data_*.csv")), key=os.path.getmtime)
with open(mall, encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        p = pid_of(r)
        vol = tof(r.get("bundle.contentData.netContentVolume.value")); vu = (r.get("bundle.contentData.netContentVolume.uom") or "").upper()
        wgt = tof(r.get("bundle.contentData.netPieceWeight.value")); wu = (r.get("bundle.contentData.netPieceWeight.uom") or "").upper()
        if vol and vu in ("ML", "L"): jell[p] = (vol * (1000 if vu == "L" else 1), "ml")
        elif wgt and wu in ("GRAM", "G", "KG"): jell[p] = (wgt * (1000 if wu == "KG" else 1), "g")

done = set()
existing = {}
with open(CORR, encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        existing[(r["store_name"], r["store_product_id"])] = r
        if r["forras"].startswith(("kezi:", "mintazat:")):
            done.add((r["store_name"], r["store_product_id"]))

NUM = r"(?<![\d,./])(?:\d{1,3}(?:[ \xa0]\d{3})+|\d+)(?:[.,]\d+)?"
UNIT = r"kg|g|ml|liter(?:es)?|l|cl|db|darab|pcs|pc"
MULTI = re.compile(rf"({NUM})\s*(?:db|darab)?\s*x\s*({NUM})\s*({UNIT})", re.IGNORECASE)
def name_last(name):
    name = name.lower().replace("×", "x"); last = None
    for m in re.finditer(rf"({NUM})\s*({UNIT})\b", name):
        v = tof(m.group(1)); u = m.group(2)
        if v is None: continue
        if u in ("kg", "l"): v, u = v * 1000, ("g" if u == "kg" else "ml")
        elif u == "cl": v, u = v * 10, "ml"
        elif u in ("liter", "literes"): v, u = v * 1000, "ml"
        elif u in ("darab", "pcs", "pc"): u = "db"
        last = (v, u)
    return last

def multipack_total(name):
    name = name.lower().replace("×", "x")
    best = None
    for m in re.finditer(MULTI, name):
        a = tof(m.group(1)); b = tof(m.group(2)); u = m.group(3)
        if not a or not b: continue
        tot = a * b
        if u in ("kg", "l"): tot, u = tot * 1000, ("g" if u == "kg" else "ml")
        elif u == "cl": tot, u = tot * 10, "ml"
        elif u in ("liter", "literes"): tot, u = tot * 1000, "ml"
        elif u in ("darab", "pcs", "pc"): u = "db"
        best = (tot, u)
    return best

LECSO = re.compile(r"lében|leben|olajban|szószban|szoszban|konzerv|befőtt|befott|savany|"
                   r"olajbogy|olívabogy|olivabogy|uborka|\bbab\b|csicseri|lencse|kukorica|"
                   r"paradicsom|káposzta|kaposzta|kapri|felezett|hámozott|hamozott|párolt|parolt|"
                   r"gőzben|gozben|kompót|kompot|escabeche|gari|gyömbér|"
                   r"borsó|borso|gomba|csiperke|kagyló|kagylo|csemegekukorica|"
                   r"bébirépa|bebirepa|cékla|cekla|gyöngyhagyma|gyongyhagyma|articsóka|articsoka|"
                   r"cseresznye|jalapeno|jalapeño|csalamádé|csalamade|hering|ruszli|pácolt|pacolt|"
                   r"bambusz|sombrero|zöldbors|zoldbors|zöldségkeverék|zoldsegkeverek|"
                   r"krémfehér|kremfeher|feta|antipasti|chili paprika|padlizsán", re.IGNORECASE)
GLAZUR = re.compile(r"glaz|glazing|\bgl\b|jegelt", re.IGNORECASE)
TOJAS = re.compile(r"tojás|tojas", re.IGNORECASE)


def decide(r):
    name = r["product_name"]
    step = tof(r["unit_step"]); unit = r["unit_type"]
    nl = name_last(name); nv = nl[0] if nl and nl[1] == unit else None
    nl_db = nl[0] if nl and nl[1] == "db" else None
    j = jell.get(r["store_product_id"]) if r["store_name"] == "Metro" else None
    jv = j[0] if (j and j[1] == unit) else None
    mp = multipack_total(name)

    # 1) tojas/db-termek: a darabszam a kiszereles
    if TOJAS.search(name) and nl_db:
        return nl_db, "db", "tojás: darabszám"
    # 2) multipack N x M: a teljes csomag
    if mp and mp[1] == unit and step and abs(mp[0] - step) / max(mp[0], step) > 0.02:
        return mp[0], unit, f"multipack összeg ({mp[0]:g})"
    # 3) glazuros tengeri (Metro): a netto (jellemzo, ha kisebb mint step)
    if GLAZUR.search(name) and jv and step:
        return min(jv, step), unit, "glazúr: nettó (kisebb)"
    # 4) lecsopogtetett: leben/befott/parolt + step kisebb mint nev
    if LECSO.search(name) and nv and step and step < nv * 0.98:
        return step, unit, "lecsöpögtetett (API kisebb)"
    # 5) Metro netto_api (nem tojas): a kisebb ertek
    if r["tipus"] == "netto_api":
        jav = tof(r["javasolt_mennyiseg"])
        if jav:
            return jav, unit, "Metro nettó tömeg"
    # 6) nev + jellemzo konszenzus
    if nv and jv and abs(nv - jv) / max(nv, jv) <= 0.02 and step and abs(nv - step) / max(nv, step) > 0.02:
        return nv, unit, "név+jellemző konszenzus"
    # 7) kis elteres: nev (deklaralt)
    if nv and step and abs(nv - step) / max(nv, step) <= 0.12:
        return nv, unit, "kis eltérés: név (deklarált)"
    # 8) celzott kivetelek (kepes/logikai dontes)
    if "gyümölcssaláta" in name.lower() and r["store_name"] == "Penny":
        return 480, unit, "kép: gyümölcskonzerv szirupban, lecsöpögtetett"
    if "és kinley" in name.lower() or ("martini" in name.lower() and "kinley" in name.lower()):
        return step, unit, "szett (Martini + Kinley): a teljes API-érték"
    # 9) maradek: a nev a gyartoi deklaralt csomagmeret (az API ar-derivalt
    # pontatlansaga miatt ter el >12%-kal); a kep nem segit a kerekitesnel
    if nv and step:
        return nv, unit, "név (deklarált csomagméret, API ár-derivált)"
    return None, None, None


applied = []
ketes = []
with open(AUDIT, encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        if r["bizonyossag"] != "review":
            continue
        key = (r["store_name"], r["store_product_id"])
        if key in done:
            continue
        val, unit, indok = decide(r)
        if val is None:
            ketes.append(r)
            continue
        existing[key] = {
            "store_name": r["store_name"], "store_product_id": r["store_product_id"], "product_name": r["product_name"],
            "korrekcio_tipus": "kiszereles", "eredeti_mennyiseg": r["unit_step"], "eredeti_egyseg": r["unit_type"],
            "javitott_mennyiseg": f"{val:g}", "javitott_egyseg": unit,
            "indok": f"maradék review: {indok}", "forras": "kezi:maradek_review",
        }
        applied.append((r["store_name"], r["product_name"], val, unit, indok))

fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus", "eredeti_mennyiseg",
          "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg", "indok", "forras"]
with open(CORR, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(existing.values())
with open(KETES, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(ketes[0].keys()) if ketes else ["store_name"]); w.writeheader(); w.writerows(ketes)

ic = Counter(a[4] for a in applied)
print(f"Alkalmazott korrekciok: {len(applied)} | kétes (kép kell): {len(ketes)}")
for k, v in ic.most_common():
    print(f"  {k}: {v}")
