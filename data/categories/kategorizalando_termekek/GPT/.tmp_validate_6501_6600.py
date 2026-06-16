# -*- coding: utf-8 -*-
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
TREE = BASE / "kategoriak_2026-06-13.json"
CSV = BASE / "kategorizalatlan_termekek.csv"
ERED = BASE / "eredmeny.json"


def norm(block):
    out = {}
    if not isinstance(block, dict):
        return out
    for name, value in block.get("egyedi", {}).items():
        if isinstance(value, list):
            out[name] = {"kind": "single", "values": value}
        elif isinstance(value, str):
            out[name] = {"kind": "single", "values": [value]}
        else:
            out[name] = {"kind": "bool", "values": None}
    for name, values in block.get("csoportos", {}).items():
        out[name] = {"kind": "multi", "values": values if isinstance(values, list) else []}
    return out


def schema(tree, fok, alk, alt):
    res = {}
    root = tree[fok]
    res.update(norm(root.get("tulajdonságok", {})))
    cat = root["alkategóriák"][alk]
    res.update(norm(cat.get("tulajdonságok", {})))
    if alt:
        res.update(norm(cat["altípusok"][alt].get("tulajdonságok", {})))
    return res


def main():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
    expected = [(r["store_name"], r["store_product_id"]) for r in rows[6500:6600]]
    ered = json.loads(ERED.read_text(encoding="utf-8"))
    by_key = {}
    duplicates = []
    for item in ered:
        key = (item.get("termek", {}).get("store_name"), item.get("termek", {}).get("store_product_id"))
        if key in by_key:
            duplicates.append(key)
        by_key[key] = item

    errors = []
    missing = [key for key in expected if key not in by_key]
    if missing:
        errors.append(f"hiányzó kulcsok: {missing[:10]}")
    if duplicates:
        errors.append(f"duplikált kulcsok: {duplicates[:10]}")

    for key in expected:
        if key not in by_key:
            continue
        item = by_key[key]
        pid = item["termek"]["store_product_id"]
        fok, alk, alt = item["fokategoria"], item["alkategoria"], item["altipus"]
        if fok not in tree:
            errors.append(f"{pid}: ismeretlen főkategória {fok}")
            continue
        if alk not in tree[fok]["alkategóriák"]:
            errors.append(f"{pid}: ismeretlen alkategória {alk}")
            continue
        if alt and alt not in tree[fok]["alkategóriák"][alk]["altípusok"]:
            errors.append(f"{pid}: ismeretlen altípus {alt}")
            continue
        sch = schema(tree, fok, alk, alt)
        props = item["tulajdonsagok"]
        extra = sorted(set(props) - set(sch))
        missing_props = sorted(set(sch) - set(props))
        if extra:
            errors.append(f"{pid}: ismeretlen tulajdonság {extra}")
        if missing_props:
            errors.append(f"{pid}: hiányzó tulajdonság {missing_props}")
        for name, actual in props.items():
            if name not in sch:
                continue
            spec = sch[name]
            if spec["kind"] == "bool":
                if not isinstance(actual, bool):
                    errors.append(f"{pid}: {name} nem bool")
            elif spec["kind"] == "single":
                if isinstance(actual, list):
                    errors.append(f"{pid}: {name} single, de lista")
                elif actual not in spec["values"]:
                    errors.append(f"{pid}: {name} ismeretlen érték {actual!r}")
            else:
                if not isinstance(actual, list):
                    errors.append(f"{pid}: {name} multi, de nem lista")
                else:
                    bad = [v for v in actual if v not in spec["values"]]
                    if bad:
                        errors.append(f"{pid}: {name} ismeretlen érték {bad}")

    if errors:
        print("ERRORS")
        for error in errors[:100]:
            print(error)
        raise SystemExit(1)
    print("OK 6501-6600; records=100; eredmeny length=", len(ered))


if __name__ == "__main__":
    main()
