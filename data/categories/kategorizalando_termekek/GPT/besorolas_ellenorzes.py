"""Olvasási műveletek a besorolások összehasonlításához."""

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REPORTS = ROOT / "analysis/reports"
IMAGES = ROOT / "data/markets_data/product_images"
LEVELS = ("fokategoria", "alkategoria", "altipus")


def reports():
    return {p.parent.name: p for p in sorted(REPORTS.glob("*/termekenkenti_besorolas.csv"))}


def dataset(rows):
    # Review marks belong to this exact pair of snapshots.
    raw = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return {"version": hashlib.sha256(raw).hexdigest(), "rows": rows}


def report_data(path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        needed = {"bolt", "bolti_azonosito", "termeknev", "uj_tulajdonsagok"}
        needed.update(prefix + k for prefix in ("regi_", "uj_") for k in LEVELS)
        if not needed.issubset(reader.fieldnames or ()):
            raise ValueError("A jegyzékből hiányzik az azonosító, a besorolás vagy az új tulajdonságlista.")
        rows = []
        for r in reader:
            old = r.get("regi_tulajdonsagok")
            rows.append({
                "store": r["bolt"], "id": r["bolti_azonosito"], "name": r["termeknev"],
                "old": [r["regi_" + k] for k in LEVELS], "new": [r["uj_" + k] for k in LEVELS],
                "before": json.loads(old) if old else None, "after": json.loads(r["uj_tulajdonsagok"]),
                "image": r.get("kep_utvonala"), "imageSource": r.get("kep_forrasa"),
                "decision": r.get("dontes"), "reason": r.get("kivetel_indoka"),
                "brand": r.get("marka"), "size": r.get("mennyiseg"), "aisle": r.get("bolti_kategoria"),
            })
    return dataset(rows)


def compare(proposal, baseline, inventory):
    if not isinstance(proposal, list):
        raise ValueError("Termékrekordokból álló eredmény-JSON-t válassz.")
    metadata = {}
    stores = defaultdict(set)
    with inventory.open(encoding="utf-8-sig", newline="") as f:
        for item in csv.DictReader(f):
            key = (item["store_name"].strip().casefold(), item["store_product_id"])
            metadata[key] = item
            stores[key[1]].add(key[0])
    with baseline.open(encoding="utf-8-sig") as f:
        originals = json.load(f)

    def identity(record):
        product = record.get("termek") if isinstance(record, dict) else None
        if not isinstance(product, dict) or not product.get("store_product_id"):
            raise ValueError("Minden termékhez szükséges a termek.store_product_id azonosító.")
        pid = str(product["store_product_id"])
        store = str(product.get("store_name") or "").strip().casefold()
        if not store:
            candidates = stores[pid]
            if len(candidates) > 1:
                raise ValueError(f"Több bolt használja ezt az azonosítót. Add meg a boltot is: {pid}")
            store = next(iter(candidates), "")
        return store, pid

    for record in originals:
        item = record["termek"]
        if item.get("store_name"):
            stores[str(item["store_product_id"])].add(item["store_name"].strip().casefold())
    current = {}
    for record in originals:
        key = identity(record)
        if key in current:
            raise ValueError(f"Ismétlődő termék a kiinduló adatokban: {key}")
        current[key] = record
    rows, seen = [], set()
    for record in proposal:
        key = identity(record)
        if key in seen:
            raise ValueError(f"Ismétlődő termék a tervezetben: {key}")
        seen.add(key)
        if not isinstance(record.get("tulajdonsagok"), dict) or not isinstance(record.get("fokategoria"), str):
            raise ValueError(f"Hiányzó kategória vagy hibás tulajdonságlista: {key[1]}")
        existing = current.get(key)
        after = record["tulajdonsagok"]
        new = [record.get(k) or "" for k in LEVELS]
        old = [existing.get(k) or "" for k in LEVELS] if existing else None
        before = existing["tulajdonsagok"] if existing else None
        if old == new and json.dumps(before, sort_keys=True) == json.dumps(after, sort_keys=True):
            continue
        item = {**metadata.get(key, {})}
        for source in (existing, record):
            if source:
                item.update({k: v for k, v in source["termek"].items() if v})
        rows.append({
            "store": item.get("store_name") or key[0], "id": key[1], "name": item.get("product_name") or key[1],
            "old": old, "new": new, "before": before, "after": after,
            "image": (item.get("local_image_paths") or "").split(";")[0].strip(),
            "brand": item.get("brand_name"), "aisle": item.get("categories"),
            "size": " ".join(str(item[k]) for k in ("vegso_mennyiseg", "vegso_egyseg") if item.get(k)),
        })
    return {**dataset(rows), "compared": len(seen)}


def image_file(relative):
    path = (ROOT / relative).resolve()
    types = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    if path.is_relative_to(IMAGES) and path.suffix.lower() in types and path.is_file():
        return path, types[path.suffix.lower()]
    return None
