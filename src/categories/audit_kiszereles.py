import csv
import glob
import os
import re
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

# Kiszereles-audit: a normalizalt unit_step/unit_type ellenorzese a termeknev,
# a bolti nyers ledig/netto jelek alapjan. NEM ir felul semmit: az eredmeny a
# data/categories/kiszereles_audit.csv jelolt-lista, amibol a megerositett
# sorok a kiszereles_korrekciok.csv-be kerulnek (a ledig jeloles automatikus).


def repo_root():
    return Path(__file__).resolve().parents[2]


def markets_dir():
    return repo_root() / "data" / "markets_data"


def latest_file(pattern):
    candidates = glob.glob(str(markets_dir() / pattern))
    return Path(max(candidates, key=os.path.getmtime)) if candidates else None


def latest_normalized_files():
    result = {}
    rx = re.compile(r"(.+)_normalized_data_(\d{8}_\d{6})\.csv$")
    for file_name in glob.glob(str(markets_dir() / "*_normalized_data_*.csv")):
        path = Path(file_name)
        match = rx.match(path.name)
        if not match:
            continue
        key = match.group(1)
        if key not in result or path.stat().st_mtime > result[key].stat().st_mtime:
            result[key] = path
    return result


def clean(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def to_float(value):
    value = clean(value).replace("\xa0", "").replace(" ", "").replace(",", ".")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def normalize_unit(value, unit):
    unit = clean(unit).lower()
    if value is None or not unit:
        return None, None
    if unit in {"kg", "kilogram", "kilogramm"}:
        return value * 1000, "g"
    if unit in {"g", "gr", "gram", "gramm"}:
        return value, "g"
    if unit in {"l", "liter", "litre", "literes"}:
        return value * 1000, "ml"
    if unit in {"ml"}:
        return value, "ml"
    if unit == "cl":
        return value * 10, "ml"
    if unit in {"db", "darab", "pc", "pcs"}:
        return value, "db"
    return value, unit


# A (?<![\d,./]) lookbehind megakadalyozza, hogy a "4,5 400 ml" tizedesresze
# vagy a "40/60 500 g" meretkodja hamis ezres-csoportkent olvasodjon.
NUM = r"(?<![\d,./])(?:\d{1,3}(?:[\s\xa0]\d{3})+|\d+)(?:[\.,]\d+)?"
UNITS = r"kg|g|ml|liter(?:es)?|l|cl|db|darab|pcs|pc"


def parse_pack_from_name(text):
    # A nev szerinti kiszereles a POZICIO szerint utolso mennyiseg: a
    # "kolbász 3 x 15 ml mustárral, 300 g" eseteben a 300 g nyer, nem a
    # mellekelt mustar multipack-mintaja.
    text = clean(text).lower().replace("×", "x")
    if not text:
        return None, None
    candidates = []
    multi_spans = []
    for match in re.finditer(rf"(?<![a-záéíóöőúüű])({NUM})\s*(?:db|darab)?\s*x\s*({NUM})\s*({UNITS})\b", text, flags=re.IGNORECASE):
        total = (to_float(match.group(1)) or 0) * (to_float(match.group(2)) or 0)
        if total > 0:
            candidates.append((match.start(), total, match.group(3)))
            multi_spans.append((match.start(), match.end()))
    for match in re.finditer(rf"(?<![a-záéíóöőúüű])({NUM})\s*({UNITS})\b", text, flags=re.IGNORECASE):
        if any(start <= match.start() < end for start, end in multi_spans):
            continue
        numeric = to_float(match.group(1))
        if numeric and numeric > 0:
            candidates.append((match.start(), numeric, match.group(2)))
    if not candidates:
        return None, None
    candidates.sort(key=lambda item: item[0])
    _, value, unit = candidates[-1]
    return normalize_unit(value, unit)


NETTO_NAME = re.compile(r"(töltőtömeg|lecsöpögtetett tömeg|lecsepegtetett tömeg)\s*:?\s*(" + NUM + r")\s*(kg|g|ml|l)", re.IGNORECASE)


def read_columns(path, id_field, columns):
    result = {}
    if path is None or not path.exists():
        return result
    with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fields = set(reader.fieldnames or [])
        use = [c for c in columns if c in fields]
        if id_field not in fields:
            return result
        for row in reader:
            key = clean(row.get(id_field))
            if key:
                result[key] = {c: clean(row.get(c)) for c in use}
    return result


def metro_product_id(row):
    return clean(row.get("bundle_id") or row.get("bundle.bundleId.bettyBundleId") or row.get("variant_id") or row.get("search_result_id"))


def load_store_signals(store):
    if store in ("aldi", "penny"):
        raw = read_columns(latest_file(f"{store}_filtered_data_*.csv"), "productID",
                           ["isBulk", "selectedShopIsBulk", "minWeightStep", "maxWeightStep"])
        return {k: {"ledig": v.get("isBulk", "").lower() == "true" or v.get("selectedShopIsBulk", "").lower() == "true"}
                for k, v in raw.items()}
    if store in ("spar", "prima"):
        raw = read_columns(latest_file(f"{store}_all_data_*.csv"), "id",
                           ["sell_by_weight_config.input_type", "sell_by_weight_config.grams_per_step"])
        return {k: {"ledig": bool(clean(v.get("sell_by_weight_config.input_type")))} for k, v in raw.items()}
    if store == "auchan":
        # Az Auchan kimert arui a nevukben hordozzak a "ledig" jelzest; a
        # loose.weightPerPiece logisztikai darabtomeg, nem ledig-jel.
        return {}
    if store == "metro":
        result = {}
        path = latest_file("metro_filtered_data_*.csv")
        if path is None:
            return result
        with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                key = metro_product_id(row)
                if not key:
                    continue
                net_val, net_unit = normalize_unit(
                    to_float(row.get("bundle.contentData.netPieceWeight.value")),
                    row.get("bundle.contentData.netPieceWeight.uom"),
                )
                gross = to_float(row.get("bundle.grossWeight"))
                result[key] = {
                    "ledig": clean(row.get("bundle.isWeightArticle")).upper() == "WEIGHT",
                    "net_g": net_val if net_unit == "g" else None,
                    "gross_g": gross * 1000 if gross and gross < 100 else gross,
                }
        return result
    if store == "tesco":
        raw = read_columns(latest_file("tesco_filtered_data_*.csv"), "id",
                           ["catchWeightList", "details.netContents", "details.drainedWeight", "price.unitOfMeasure"])
        out = {}
        for k, v in raw.items():
            net_v, net_u = parse_pack_from_name(v.get("details.netContents", ""))
            drained_v, drained_u = parse_pack_from_name(v.get("details.drainedWeight", ""))
            out[k] = {
                "ledig": len(v.get("catchWeightList", "")) > 4,
                "net": (net_v, net_u),
                "drained": (drained_v, drained_u),
            }
        return out
    return {}


def main():
    categories_dir = repo_root() / "data" / "categories"
    kiszurt_ids = set()
    kiszurt_path = categories_dir / "kiszurt_termekek.csv"
    if kiszurt_path.exists():
        with open(kiszurt_path, mode="r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                kiszurt_ids.add((row["store_name"], row["store_product_id"]))

    decided = {}
    corr_path = categories_dir / "kiszereles_korrekciok.csv"
    if corr_path.exists():
        with open(corr_path, mode="r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                decided[(row["store_name"], row["store_product_id"])] = row.get("forras", "")

    audit_rows = []
    auto_corrections = []
    stats = {}

    for store, normalized_path in sorted(latest_normalized_files().items()):
        signals = load_store_signals(store)
        with open(normalized_path, mode="r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                store_name = clean(row.get("store_name"))
                product_id = clean(row.get("store_product_id"))
                if (store_name, product_id) in kiszurt_ids:
                    continue
                # Mar eldontott sor (mintazat-dontes vagy kezi korrekcio) nem
                # kerul ujra a jeloltek koze; a ledig (bolti_api) ujraertekelo.
                decided_source = decided.get((store_name, product_id), "")
                if decided_source and decided_source != "bolti_api":
                    continue
                name = clean(row.get("product_name"))
                step = to_float(row.get("unit_step"))
                unit = clean(row.get("unit_type")).lower()
                signal = signals.get(product_id, {})

                base = {
                    "store_name": store_name,
                    "store_product_id": product_id,
                    "product_name": name,
                    "unit_step": row.get("unit_step", ""),
                    "unit_type": unit,
                    "local_image_paths": row.get("local_image_paths", ""),
                }

                # 1) Ledig: a lepeskoz nem kiszereles -> egysegar hasznalando.
                # Bolti jel VAGY a termeknevben szereplo "ledig" szo.
                if signal.get("ledig") or "lédig" in name.lower():
                    stats[(store_name, "ledig")] = stats.get((store_name, "ledig"), 0) + 1
                    audit_rows.append({**base, "tipus": "ledig", "javasolt_mennyiseg": "", "javasolt_egyseg": unit,
                                       "bizonyossag": "auto", "indok": f"bolti ledig jelzes; lepeskoz volt: {row.get('unit_step','')} {unit}"})
                    auto_corrections.append({
                        "store_name": store_name, "store_product_id": product_id, "product_name": name,
                        "korrekcio_tipus": "ledig", "eredeti_mennyiseg": row.get("unit_step", ""),
                        "eredeti_egyseg": unit, "javitott_mennyiseg": "", "javitott_egyseg": unit,
                        "indok": "bolti ledig/sulyra mert jelzes - egysegar hasznalando", "forras": "bolti_api",
                    })
                    continue

                # 2) Lecsopogtetett/toltotomeg preferencia: ha elerheto, a
                # lecsopogtetett tomeg a hasznalando kiszereles, mert az mond
                # tobbet a tenyleges tartalomrol.
                drained = signal.get("drained", (None, None))
                step_is_drained = bool(
                    drained[0] and step and drained[1] == unit
                    and abs(drained[0] - step) / max(drained[0], step) <= 0.05
                )

                name_lecso = NETTO_NAME.search(name)
                if name_lecso:
                    lecso_v, lecso_u = normalize_unit(to_float(name_lecso.group(2)), name_lecso.group(3))
                    if lecso_v and step and lecso_u == unit and abs(lecso_v - step) / max(lecso_v, step) > 0.02:
                        stats[(store_name, "lecsopogtetett_nev")] = stats.get((store_name, "lecsopogtetett_nev"), 0) + 1
                        audit_rows.append({**base, "tipus": "lecsopogtetett_nev", "javasolt_mennyiseg": lecso_v,
                                           "javasolt_egyseg": lecso_u, "bizonyossag": "review",
                                           "indok": f"nevben {name_lecso.group(1)}: {lecso_v:g} {lecso_u} - a lecsopogtetett a preferalt"})
                        continue

                if (
                    drained[0] and step and drained[1] == unit and not step_is_drained
                    and abs(drained[0] - step) / max(drained[0], step) > 0.02
                ):
                    stats[(store_name, "lecsopogtetett_api")] = stats.get((store_name, "lecsopogtetett_api"), 0) + 1
                    audit_rows.append({**base, "tipus": "lecsopogtetett_api", "javasolt_mennyiseg": drained[0],
                                       "javasolt_egyseg": drained[1], "bizonyossag": "review",
                                       "indok": f"API lecsopogtetett: {drained[0]:g} {drained[1]} - ez hasznalando a netto {row.get('unit_step','')} {unit} helyett"})
                    continue

                # Csak brutto-gyanu eseten javasolunk nettora valtast (lepes >
                # netto). Ha a lepes KISEBB a nettonal es a termek leben/olajban
                # van, az velhetoen a lecsopogtetett ertek - az marad.
                net_g = signal.get("net_g")
                if net_g and unit == "g" and step and step > net_g and (step - net_g) / step > 0.05:
                    stats[(store_name, "netto_api")] = stats.get((store_name, "netto_api"), 0) + 1
                    audit_rows.append({**base, "tipus": "netto_api", "javasolt_mennyiseg": net_g,
                                       "javasolt_egyseg": "g", "bizonyossag": "review",
                                       "indok": f"API netto tomeg: {net_g:g} g (bruttoval szamolhatott)"})
                    continue

                # 3) Nev vs API kiszereles elteres. Ha a lepes mar a
                # lecsopogtetett ertéken all, az helyes - a nev szerinti
                # (netto) ertek NEM javitando ra.
                name_v, name_u = parse_pack_from_name(name)
                if step_is_drained:
                    stats[(store_name, "lecsopogtetett_ok")] = stats.get((store_name, "lecsopogtetett_ok"), 0) + 1
                elif name_v and step and name_u == unit:
                    diff = abs(name_v - step) / max(name_v, step)
                    if diff > 0.05:
                        stats[(store_name, "nev_elteres")] = stats.get((store_name, "nev_elteres"), 0) + 1
                        audit_rows.append({**base, "tipus": "nev_elteres", "javasolt_mennyiseg": name_v,
                                           "javasolt_egyseg": name_u, "bizonyossag": "review",
                                           "indok": f"nev szerint {name_v:g} {name_u}, API szerint {row.get('unit_step','')} {unit} (elteres {diff*100:.0f}%)"})
                elif name_v and step and name_u and unit and name_u != unit and "db" not in (name_u, unit):
                    stats[(store_name, "egyseg_elteres")] = stats.get((store_name, "egyseg_elteres"), 0) + 1
                    audit_rows.append({**base, "tipus": "egyseg_elteres", "javasolt_mennyiseg": name_v,
                                       "javasolt_egyseg": name_u, "bizonyossag": "review",
                                       "indok": f"nev szerint {name_v:g} {name_u}, API szerint {row.get('unit_step','')} {unit}"})

    audit_fields = ["store_name", "store_product_id", "product_name", "unit_step", "unit_type",
                    "tipus", "javasolt_mennyiseg", "javasolt_egyseg", "bizonyossag", "indok", "local_image_paths"]
    audit_path = categories_dir / "kiszereles_audit.csv"
    with open(audit_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=audit_fields)
        writer.writeheader()
        writer.writerows(audit_rows)

    corr_fields = ["store_name", "store_product_id", "product_name", "korrekcio_tipus",
                   "eredeti_mennyiseg", "eredeti_egyseg", "javitott_mennyiseg", "javitott_egyseg",
                   "indok", "forras"]
    corr_path = categories_dir / "kiszereles_korrekciok.csv"
    existing = {}
    if corr_path.exists():
        with open(corr_path, mode="r", encoding="utf-8", newline="") as file:
            for row in csv.DictReader(file):
                existing[(row["store_name"], row["store_product_id"])] = row
    # Az automatikus ledig sorok frissulnek, a kezzel felvett sorok megmaradnak.
    for correction in auto_corrections:
        key = (correction["store_name"], correction["store_product_id"])
        if key not in existing or existing[key].get("forras") == "bolti_api":
            existing[key] = correction
    with open(corr_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=corr_fields)
        writer.writeheader()
        writer.writerows(existing.values())

    print(f"Audit jeloltek: {len(audit_rows)} -> {audit_path}")
    print(f"Korrekcios sorok (ledig auto + kezi): {len(existing)} -> {corr_path}")
    print()
    for (store, tipus), count in sorted(stats.items()):
        print(f"  {store:8s} | {tipus:15s} | {count}")


if __name__ == "__main__":
    main()
