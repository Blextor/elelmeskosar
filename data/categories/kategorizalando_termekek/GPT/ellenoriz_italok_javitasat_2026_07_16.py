# -*- coding: utf-8 -*-
"""Független végellenőrzés a 2026-07-16-i Ital-javításhoz.

Nem importálja a javítószkriptet, és a javítás előtti állapotból
rögzített hash-ekkel ellenőrzi a kiszereléseket és a hatókörön kívüli
termékeket is.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


BASE = Path(__file__).resolve().parent
WORK = BASE / "italok_munkafajlok"
RESULT_PATH = BASE / "eredmeny.json"
CATEGORY_PATH = BASE / "kategoriak_2026-06-13.json"
PLANT_REVIEW = WORK / "kepellenorzes_2026_07_16" / "novenyi_italok.json"
ISSUE_REVIEW = WORK / "kepellenorzes_2026_07_16" / "konkret_hibak.json"
OUTPUT_PATH = WORK / "italok_vegellenorzes_2026-07-16.json"

EXPECTED_SIZE_SHA256 = "56b7d3b6d8421cd3aae0aee4934b5260d5e0acabad80a108d8fc755e57aebb82"
EXPECTED_UNTOUCHED_PRODUCTS = 34150
EXPECTED_UNTOUCHED_SHA256 = "26dbee646ed6d8205b250a6790a0cad9cf69e5b2b436451d9edd31118c8860d1"
EXPECTED_OUTSIDE_CATEGORY_SHA256 = "926b6b48d39f2c32b7916b94777b393bcd5721ccbb8c160d9e390218185452cc"
EXPECTED_DE_KARAVAN_SHA256 = "cdaa98681617e2e951c0674a2289d95a69f52a76a4848bfa8c5659f4ac8337a7"

SIZE_PROPS = {"kiszereles", "kiszereles csomagolas", "kiszereles rendszer"}
PLACEHOLDERS = {
    "",
    "ismeretlen",
    "n a",
    "na",
    "nem adat",
    "nem jelolt",
    "nem megadott",
    "nincs",
    "nincs adat",
}
FORBIDDEN_PROPS = {"termekcsalad", "funkcio", "minosites"}
COPIED_ALT_ALKS = {
    "Cider",
    "Citromlé",
    "Energiaital",
    "Funkcionális ital",
    "Ízesített víz",
    "Kombucha",
    "Pezsgő",
    "Sportital",
}
COOKING_IDS = {
    "c4a084a2d4aeb2442cbcba78",
    "242d8040cc313808252913f3",
    "bc09c557e3fe694d1f4dee07",
    "dde4ef9f725c9fca4d36c0c3",
}
PATH_MOVES = {
    "588146:4125536": ("Gyümölcslé", "Vegyes gyümölcs- és zöldséglé"),
    "588140:4125530": ("Gyümölcslé", "Vegyes gyümölcs- és zöldséglé"),
    "588137:4125527": ("Gyümölcslé", "Vegyes gyümölcs- és zöldséglé"),
    "533763": ("Sör", "Alkoholmentes radler"),
    "1012024:4549414": ("Sör", "Alkoholmentes sör"),
    "1032338:4569728": ("Sör", "Alkoholmentes radler"),
    "1032335:4569725": ("Sör", "Alkoholmentes radler"),
    "10101641": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X17216800320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X17216400320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X18133000320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X17216900320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X18034900320021": ("Bor", "Alkoholmentes bor"),
    "BTY-X18035000320021": ("Bor", "Alkoholmentes bor"),
    "BTY-X18035100320021": ("Bor", "Alkoholmentes bor"),
    "769656:4307046": ("Üdítőital", "Gyerekital"),
    "679217:4216607": ("Üdítőital", "Gyerekital"),
    "748902:4286292": ("Üdítőital", "Gyerekital"),
    "769659:4307049": ("Üdítőital", "Gyerekital"),
}
ALCOHOL_VALUES = {
    "566017": ["34%"],
    "1014576": ["34%"],
    "1055675": ["34%"],
    "442852:3980236": ["22%", "32%", "42%", "52%", "62%", "72%"],
    "BTY-X9705200320021": ["22%", "32%", "42%", "52%", "62%", "72%"],
    "121224421": ["13%"],
}


def fold(value: Any) -> str:
    text = unicodedata.normalize("NFKD", "" if value is None else str(value))
    text = "".join(char for char in text if not unicodedata.combining(char)).casefold()
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-z]+", " ", text)).strip()


def stable_hash(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def values(value: Any) -> list[Any]:
    if value is None or value == "" or value == [] or value == {}:
        return []
    if isinstance(value, list):
        result: list[Any] = []
        for item in value:
            result.extend(values(item))
        return result
    return [value]


def pid(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("store_product_id") or "")


def name(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("product_name") or "")


def shape(value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    return "multi" if isinstance(value, list) else "single"


def category_hash(product: dict[str, Any]) -> str:
    raw = "|".join(
        [
            str(product.get("fokategoria") or ""),
            str(product.get("alkategoria") or ""),
            str(product.get("altipus") or ""),
            json.dumps(product.get("tulajdonsagok") or {}, sort_keys=True, ensure_ascii=False),
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def prop_declarations(node: dict[str, Any]) -> tuple[dict[str, str], dict[str, list[Any]]]:
    block = node.get("tulajdonságok") or {}
    shapes: dict[str, str] = {}
    allowed: dict[str, list[Any]] = {}
    for prop, declaration in (block.get("egyedi") or {}).items():
        shapes[prop] = "flag" if isinstance(declaration, dict) else "single"
        allowed[prop] = [] if isinstance(declaration, dict) else list(declaration)
    for prop, declaration in (block.get("csoportos") or {}).items():
        shapes[prop] = "multi"
        allowed[prop] = list(declaration)
    return shapes, allowed


def combine_declarations(nodes: Iterable[dict[str, Any]]) -> tuple[dict[str, str], dict[str, list[Any]], list[str]]:
    shapes: dict[str, str] = {}
    allowed: dict[str, list[Any]] = {}
    duplicate: list[str] = []
    for node in nodes:
        node_shapes, node_allowed = prop_declarations(node)
        duplicate.extend(sorted(set(shapes) & set(node_shapes), key=fold))
        shapes.update(node_shapes)
        allowed.update(node_allowed)
    return shapes, allowed, duplicate


def main() -> int:
    products = load(RESULT_PATH)
    categories = load(CATEGORY_PATH)
    plant_review = load(PLANT_REVIEW)
    issue_review = load(ISSUE_REVIEW)
    failures: dict[str, Any] = {}

    def fail(key: str, detail: Any) -> None:
        if detail not in (None, [], {}, False, 0, ""):
            failures[key] = detail

    fail("total_products", len(products) if len(products) != 47030 else None)
    ital = [product for product in products if product.get("fokategoria") == "Ital"]
    fail("ital_products", len(ital) if len(ital) != 12876 else None)
    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        by_id[pid(product)].append(product)

    plant_ids = {str(row["store_product_id"]) for row in plant_review}
    fail("plant_review_count", len(plant_ids) if len(plant_ids) != 167 else None)
    fail("plant_review_images", sum(bool(row.get("image_path")) for row in plant_review) if sum(bool(row.get("image_path")) for row in plant_review) != 160 else None)
    fail("issue_review_count", len(issue_review) if len(issue_review) != 27 else None)
    fail("issue_review_images", sum(bool(row.get("image_path")) for row in issue_review) if sum(bool(row.get("image_path")) for row in issue_review) != 27 else None)

    plant_errors = []
    for item_id in sorted(plant_ids):
        matches = by_id.get(item_id, [])
        if len(matches) != 1:
            plant_errors.append([item_id, "darabszám", len(matches)])
            continue
        product = matches[0]
        actual = (product.get("fokategoria"), product.get("alkategoria"), product.get("altipus"))
        if item_id in COOKING_IDS:
            expected = ("Tejtermékek és tojás", "Növényi alternatíva", "Növényi főzőkrém / tejszín")
        else:
            expected = ("Ital", "Növényi ital", product.get("altipus"))
        if actual != expected:
            plant_errors.append([item_id, list(expected), list(actual)])
    fail("plant_paths", plant_errors[:30])

    base_checks = {
        "4604651": ("Zabital", ["zab"]),
        "1000957:4538347": ("Kevert növényi ital", ["kókusz", "szója"]),
        "1031498:4568888": ("Kevert növényi ital", ["kókusz", "szója"]),
        "BTY-X10253000320021": ("Kevert növényi ital", ["kókusz", "szója"]),
    }
    base_errors = []
    for item_id, (expected_alt, expected_base) in base_checks.items():
        product = by_id[item_id][0]
        actual_base = sorted(values((product.get("tulajdonsagok") or {}).get("alap")), key=fold)
        if product.get("altipus") != expected_alt or actual_base != sorted(expected_base, key=fold):
            base_errors.append([item_id, product.get("altipus"), actual_base])
    fail("image_based_plant_corrections", base_errors)

    concrete_errors = []
    for item_id, expected in PATH_MOVES.items():
        matches = by_id.get(item_id, [])
        actual = (matches[0].get("alkategoria"), matches[0].get("altipus")) if len(matches) == 1 else None
        if actual != expected:
            concrete_errors.append([item_id, list(expected), list(actual) if actual else None])
    fail("concrete_paths", concrete_errors)

    alcohol_errors = []
    for item_id, expected in ALCOHOL_VALUES.items():
        actual = values((by_id[item_id][0].get("tulajdonsagok") or {}).get("alkoholtartalom"))
        if actual != expected:
            alcohol_errors.append([item_id, expected, actual])
    fail("alcohol_values", alcohol_errors)

    copied = Counter(
        product.get("alkategoria")
        for product in ital
        if product.get("alkategoria") in COPIED_ALT_ALKS and product.get("altipus") == product.get("alkategoria")
    )
    fail("copied_same_name_altipus", dict(copied))

    root = categories.get("Ital") or {}
    root_shapes, _root_allowed = prop_declarations(root)
    fail("ital_root_properties", sorted(root_shapes, key=fold))
    alks = root.get("alkategóriák") or {}
    used_paths = {(str(product.get("alkategoria") or ""), str(product.get("altipus") or "")) for product in ital}
    declared_paths = {(alk, "") for alk in alks}
    for alk, node in alks.items():
        declared_paths.update((alk, alt) for alt in (node.get("altípusok") or {}))
    fail("missing_category_paths", sorted(used_paths - declared_paths, key=lambda row: (fold(row[0]), fold(row[1]))))
    named_used = {path for path in used_paths if path[1]}
    named_declared = {path for path in declared_paths if path[1]}
    fail("unused_named_paths", sorted(named_declared - named_used, key=lambda row: (fold(row[0]), fold(row[1]))))
    fail("ital_path_count", len(used_paths) if len(used_paths) != 89 else None)

    declarations: dict[tuple[str, str], tuple[dict[str, str], dict[str, list[Any]]]] = {}
    redefinitions = []
    for alk, node in alks.items():
        shapes, allowed, duplicate = combine_declarations([root, node])
        redefinitions.extend([[alk, "", prop] for prop in duplicate])
        declarations[(alk, "")] = (shapes, allowed)
        for alt, alt_node in (node.get("altípusok") or {}).items():
            child_shapes, child_allowed, duplicate = combine_declarations([root, node, alt_node])
            redefinitions.extend([[alk, alt, prop] for prop in duplicate])
            declarations[(alk, alt)] = (child_shapes, child_allowed)
    fail("property_redefinitions", redefinitions[:50])

    undeclared = []
    type_errors = []
    value_errors = []
    placeholders = []
    forbidden = []
    wrong_alcoholfree = []
    flag_values: dict[tuple[str, str, str], list[bool]] = defaultdict(list)
    hash_errors = []
    brand_values = Counter()
    for product in ital:
        path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        path_shapes, path_allowed = declarations.get(path, ({}, {}))
        props = product.get("tulajdonsagok") or {}
        for prop, value in props.items():
            if prop not in path_shapes:
                undeclared.append([pid(product), *path, prop])
                continue
            if fold(prop) not in SIZE_PROPS and shape(value) != path_shapes[prop]:
                type_errors.append([pid(product), *path, prop, path_shapes[prop], shape(value)])
            if path_shapes[prop] != "flag" and fold(prop) not in SIZE_PROPS:
                missing = [item for item in values(value) if item not in path_allowed[prop]]
                if missing:
                    value_errors.append([pid(product), *path, prop, missing])
            if isinstance(value, bool):
                flag_values[(*path, prop)].append(value)
            if fold(prop) not in SIZE_PROPS:
                for item in values(value):
                    if not isinstance(item, bool) and fold(item) in PLACEHOLDERS:
                        placeholders.append([pid(product), *path, prop, item])
                    if fold(item) == "alkoholmentes":
                        wrong_alcoholfree.append([pid(product), *path, prop])
            if fold(prop) in FORBIDDEN_PROPS:
                forbidden.append([pid(product), *path, prop])
        brand = props.get("márka")
        if isinstance(brand, str):
            brand_values[brand] += 1
        if product.get("kategoria_hash") != category_hash(product):
            hash_errors.append(pid(product))
    fail("undeclared_product_properties", undeclared[:50])
    fail("non_size_type_errors", type_errors[:50])
    fail("undeclared_values", value_errors[:50])
    fail("non_size_placeholders", placeholders[:50])
    fail("forbidden_5_1_properties", forbidden[:50])
    fail("wrong_alcoholfree_values", wrong_alcoholfree[:50])
    fail("all_false_path_flags", [list(key) for key, rows in flag_values.items() if rows and not any(rows)][:50])
    fail("ital_category_hashes", hash_errors[:50])

    dairy_cooking = [
        product
        for product in products
        if product.get("fokategoria") == "Tejtermékek és tojás"
        and product.get("alkategoria") == "Növényi alternatíva"
        and product.get("altipus") == "Növényi főzőkrém / tejszín"
    ]
    fail("dairy_cooking_count", len(dairy_cooking) if len(dairy_cooking) != 80 else None)
    plant_node = categories["Tejtermékek és tojás"]["alkategóriák"]["Növényi alternatíva"]
    fail("empty_dairy_plant_node", "Növényi ital" in (plant_node.get("altípusok") or {}))

    size_snapshot = []
    for index, product in enumerate(products):
        size_values = {}
        props = product.get("tulajdonsagok") or {}
        for key in props:
            if fold(key) in SIZE_PROPS:
                size_values[key] = props[key]
        size_snapshot.append([index, size_values])
    size_hash = stable_hash(size_snapshot)
    fail("size_snapshot_sha256", size_hash if size_hash != EXPECTED_SIZE_SHA256 else None)

    untouched = [
        [index, product]
        for index, product in enumerate(products)
        if product.get("fokategoria") != "Ital" and pid(product) not in plant_ids
    ]
    fail("untouched_product_count", len(untouched) if len(untouched) != EXPECTED_UNTOUCHED_PRODUCTS else None)
    fail("untouched_products_sha256", stable_hash(untouched) if stable_hash(untouched) != EXPECTED_UNTOUCHED_SHA256 else None)

    outside_categories = copy.deepcopy(categories)
    outside_categories.pop("Ital")
    fail(
        "outside_category_tree_sha256",
        stable_hash(outside_categories) if stable_hash(outside_categories) != EXPECTED_OUTSIDE_CATEGORY_SHA256 else None,
    )
    de_karavan = [product for product in products if "d e karavan" in fold(name(product))]
    fail("de_karavan_count", len(de_karavan) if len(de_karavan) != 1 else None)
    fail("de_karavan_sha256", stable_hash(de_karavan) if stable_hash(de_karavan) != EXPECTED_DE_KARAVAN_SHA256 else None)

    fake_wine_brands = {
        "Balatoni Rosé",
        "Duna-Tisza közi Muskotály",
        "Duna-Tisza közi Rosé Cuvée",
        "Dunántúli Merlot",
        "Tokaji Furmint",
        "Villányi Cabernet Sauvignon",
        "Villányi Merlot",
        "Villányi Rosé Cuvée",
        "Villányi Syrah",
    }
    bad_brands = {brand: count for brand, count in brand_values.items() if brand in fake_wine_brands or fold(brand) in PLACEHOLDERS}
    fail("bad_brand_values", bad_brands)
    fail("brand_unique_count", len(brand_values) if len(brand_values) != 1180 else None)

    semantic_errors = []
    for item_id in ("121230534", "121230615", "121230626"):
        props = by_id[item_id][0].get("tulajdonsagok") or {}
        if props.get("márka") != "Royal" or not props.get("változat"):
            semantic_errors.append(item_id)
    for item_id in ("687959:4225349", "BTY-X17303900320021", "aa93346530e07b5093a6e143", "121250274"):
        props = by_id[item_id][0].get("tulajdonsagok") or {}
        if props.get("márka") != "Red Bull" or props.get("cukormentes / zero") is not True:
            semantic_errors.append(item_id)
    mionetto = by_id["684227:4221617"][0].get("tulajdonsagok") or {}
    if mionetto.get("márka") != "Mionetto" or "Prosecco" not in values(mionetto.get("szőlőfajta / borstílus")):
        semantic_errors.append("684227:4221617")
    for item_id in ("BTY-X17350600320021", "BTY-X17352500320021"):
        props = by_id[item_id][0].get("tulajdonsagok") or {}
        if props.get("márka") != "Hohes C" or "Super Shots" not in values(props.get("változat")):
            semantic_errors.append(item_id)
    fail("brand_semantic_samples", semantic_errors)

    wrong_1664 = [
        pid(product)
        for product in ital
        if fold(name(product)).startswith("1664 blanc")
        and any(fold(item) == "alkoholmentes" for item in values((product.get("tulajdonsagok") or {}).get("sörtípus")))
    ]
    fail("wrong_1664_beer_type", wrong_1664)

    payload = {
        "status": "ok" if not failures else "hiba",
        "summary": {
            "products": len(products),
            "ital_products": len(ital),
            "ital_paths": len(used_paths),
            "plant_reviewed": len(plant_ids),
            "concrete_reviewed": len(issue_review),
            "brand_unique": len(brand_values),
            "size_snapshot_sha256": stable_hash(size_snapshot),
            "untouched_products_sha256": stable_hash(untouched),
        },
        "failures": failures,
    }
    json.encoder.c_make_encoder = None
    temp = OUTPUT_PATH.with_name(OUTPUT_PATH.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with temp.open(encoding="utf-8") as handle:
        json.load(handle)
    temp.replace(OUTPUT_PATH)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
