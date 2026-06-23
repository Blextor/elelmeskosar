#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply targeted fixes to the Baba main category."""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import tempfile
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
TREE_PATH = BASE / "kategoriak_2026-06-13.json"
PRODUCTS_PATH = BASE / "eredmeny.json"
REPORT_PATH = BASE / "baba_kategoria_javitas_2026-06-23.md"

PROP = "tulajdons\u00e1gok"
ALK = "alkateg\u00f3ri\u00e1k"
ALT = "alt\u00edpusok"
EGY = "egyedi"
CSOP = "csoportos"

FOK = "fokategoria"
AK = "alkategoria"
AT = "altipus"
PROPS = "tulajdonsagok"

BABY = "Baba"
BABY_FOOD_OTHER = "Egy\u00e9b baba\u00e9lelmiszer"
BABY_CARE = "Baba\u00e1pol\u00e1si eszk\u00f6z"
CHANGING_PAD = "Pelenk\u00e1z\u00f3 al\u00e1t\u00e9t"
FRUIT_DESSERT = "Gy\u00fcm\u00f6lcsp\u00fcr\u00e9, b\u00e9bidesszert"
FRUIT_GRAIN = "Gy\u00fcm\u00f6lcs-gabona k\u00e9sz\u00edtm\u00e9ny"
FRUIT_GRAIN_PUREE = "Gy\u00fcm\u00f6lcs-gabona p\u00fcr\u00e9"
FRUIT_PUREE_WITH_GRAIN = "Gy\u00fcm\u00f6lcsp\u00fcr\u00e9 gabon\u00e1val"
BABY_SNACK = "B\u00e9bi snack, keksz"
SPONGE_CAKE = "Babapisk\u00f3ta"
MILK_CEREAL = "Tejp\u00e9p, gabonap\u00e9p, k\u00e1sa"
FORMULA = "T\u00e1pszer"
CHILD_DRINK_POWDER = "Gyermek italpor"

AGE = "\u00e9letkor"
OLD_AGE = "koroszt\u00e1ly"
FEATURE = "jellemz\u0151"
OLD_FEATURES = "jellemz\u0151k"
INGREDIENT = "alapanyag"
GRAIN = "gabona"
PACKAGING = "csomagol\u00e1s"
PACKAGE_SIZE = "kiszerel\u00e9s"

PACKAGING_VALUES = {
    "\u00fcveg",
    "tasak / pouch",
    "doboz",
    "poh\u00e1r",
    "flakon",
    "tubus",
    "egy\u00e9b",
}

MERGE_ALT_TYPES = {
    (FRUIT_DESSERT, FRUIT_GRAIN_PUREE): (FRUIT_DESSERT, FRUIT_GRAIN),
    (FRUIT_DESSERT, FRUIT_PUREE_WITH_GRAIN): (FRUIT_DESSERT, FRUIT_GRAIN),
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_atomic(path: Path, data: Any) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=".fix_baba_", suffix=".json", dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def flatten(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]


def clean_scalar(value: Any) -> Any:
    return value.strip() if isinstance(value, str) else value


def value_key(value: Any) -> str:
    if isinstance(value, bool):
        return "bool:" + str(value).lower()
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def dedupe(values: list[Any]) -> list[Any]:
    out: list[Any] = []
    seen: set[str] = set()
    for value in values:
        value = clean_scalar(value)
        if value in ("", None):
            continue
        key = value_key(value)
        if key not in seen:
            seen.add(key)
            out.append(value)
    return out


def ensure_props(node: dict[str, Any]) -> dict[str, dict[str, Any]]:
    props = node.setdefault(PROP, {})
    if not isinstance(props, dict):
        props = {}
        node[PROP] = props
    for group in (EGY, CSOP):
        if not isinstance(props.get(group), dict):
            props[group] = {}
    return props


def prop_group(node: dict[str, Any], group: str) -> dict[str, Any]:
    props = node.get(PROP, {})
    if not isinstance(props, dict):
        return {}
    values = props.get(group, {})
    return values if isinstance(values, dict) else {}


def empty_node(level: int) -> dict[str, Any]:
    node: dict[str, Any] = {PROP: {EGY: {}, CSOP: {}}}
    if level == 1:
        node[ALK] = {}
    if level == 2:
        node[ALT] = {}
    return node


def get_node(tree: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any] | None:
    if not path:
        return None
    node = tree.get(path[0])
    if not isinstance(node, dict):
        return None
    if len(path) >= 2:
        node = node.get(ALK, {}).get(path[1])
        if not isinstance(node, dict):
            return None
    if len(path) >= 3:
        node = node.get(ALT, {}).get(path[2])
        if not isinstance(node, dict):
            return None
    return node


def ensure_path(tree: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any]:
    container = tree
    node: dict[str, Any] | None = None
    for level, label in enumerate(path, start=1):
        if label not in container:
            container[label] = empty_node(level)
        node = container[label]
        ensure_props(node)
        if level < len(path):
            child_key = ALK if level == 1 else ALT
            if not isinstance(node.get(child_key), dict):
                node[child_key] = {}
            container = node[child_key]
    if node is None:
        raise RuntimeError("Empty path")
    return node


def direct_defs(node: dict[str, Any]) -> dict[str, tuple[str, str, list[Any]]]:
    out: dict[str, tuple[str, str, list[Any]]] = {}
    for name, value in prop_group(node, EGY).items():
        if isinstance(value, dict):
            out[name] = (EGY, "flag", [])
        else:
            out[name] = (EGY, "single", dedupe(flatten(value)))
    for name, value in prop_group(node, CSOP).items():
        values = dedupe(flatten(value))
        if name in out and out[name][1] != "flag":
            values = dedupe(out[name][2] + values)
        out[name] = (CSOP, "multi", values)
    return out


def effective_defs(tree: dict[str, Any], path: tuple[str, str, str]) -> dict[str, tuple[str, str, list[Any]]]:
    out: dict[str, tuple[str, str, list[Any]]] = {}
    for level in range(1, len(path) + 1):
        node = get_node(tree, path[:level])
        if isinstance(node, dict):
            out.update(direct_defs(node))
    return out


def merge_prop_definition(target_node: dict[str, Any], prop: str, value: Any, preferred_group: str | None = None) -> None:
    props = ensure_props(target_node)
    existing_group = None
    if preferred_group in (EGY, CSOP) and prop in props[preferred_group]:
        existing_group = preferred_group
    for group in (EGY, CSOP):
        if existing_group is None and prop in props[group]:
            existing_group = group
            break

    if isinstance(value, bool):
        group = existing_group or EGY
        if group == CSOP:
            props[CSOP][prop] = dedupe(flatten(props[CSOP].get(prop, [])) + [value])
        else:
            props[EGY][prop] = {}
        return

    group = existing_group or preferred_group or (CSOP if isinstance(value, list) else EGY)
    incoming = dedupe(flatten(value))
    current = props[group].get(prop)
    if group == EGY:
        if isinstance(current, dict):
            props[EGY][prop] = current
        else:
            props[EGY][prop] = dedupe((flatten(current) if current not in (None, "") else []) + incoming)
    else:
        if isinstance(current, dict):
            props[CSOP][prop] = incoming
        else:
            props[CSOP][prop] = dedupe((flatten(current) if current not in (None, "") else []) + incoming)


def merge_node_props(dst: dict[str, Any], src: dict[str, Any]) -> None:
    for group in (EGY, CSOP):
        for prop, value in prop_group(src, group).items():
            merge_prop_definition(dst, prop, value, preferred_group=group)


def remove_prop(node: dict[str, Any], prop: str) -> list[tuple[str, Any]]:
    removed: list[tuple[str, Any]] = []
    for group in (EGY, CSOP):
        props = prop_group(node, group)
        if prop in props:
            removed.append((group, props.pop(prop)))
    return removed


def walk_baba(tree: dict[str, Any]) -> list[tuple[tuple[str, ...], dict[str, Any]]]:
    rows: list[tuple[tuple[str, ...], dict[str, Any]]] = []
    baba = tree.get(BABY, {})
    if not isinstance(baba, dict):
        return rows
    rows.append(((BABY,), baba))
    for ak, anode in baba.get(ALK, {}).items():
        rows.append(((BABY, ak), anode))
        for at, tnode in anode.get(ALT, {}).items():
            rows.append(((BABY, ak, at), tnode))
    return rows


def category_hash(fok: str, alk: str, alt: str, props: dict[str, Any]) -> str:
    key = f"{fok}|{alk}|{alt}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def product_name(product: dict[str, Any]) -> str:
    termek = product.get("termek", {})
    return termek.get("product_name", "") if isinstance(termek, dict) else ""


def path_of(product: dict[str, Any]) -> tuple[str, str, str]:
    return (product.get(FOK, "") or "", product.get(AK, "") or "", product.get(AT, "") or "")


def set_product_path(product: dict[str, Any], path: tuple[str, str, str]) -> None:
    product[FOK], product[AK], product[AT] = path


def normalize_age_value(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    raw = value.strip()
    key = value_key(raw)
    if key in {"egyeb", "gyermekeknek"}:
        return raw
    if "ujszulott" in key:
        return "0 h\u00f3+"

    match = re.search(r"(\d+)\s*[-]\s*(\d+)\s*(?:h[oó]|honap)", key)
    if match:
        return f"{match.group(1)}-{match.group(2)} h\u00f3"
    match = re.search(r"(\d+)\s*/\s*(\d+)\s*(?:h[oó]|honap)", key)
    if match:
        return f"{match.group(1)}/{match.group(2)} h\u00f3+"
    match = re.search(r"(\d+)\s*[-]\s*(\d+)\s*(?:ev|eves)", key)
    if match:
        return f"{match.group(1)}-{match.group(2)} \u00e9v"
    match = re.search(r"(\d+)\s*(?:\+)?\s*(?:h[oó]|honap|honapos)", key)
    if match:
        return f"{match.group(1)} h\u00f3+"
    match = re.search(r"(\d+)\s*(?:ev|eves)", key)
    if match:
        years = int(match.group(1))
        if years == 1:
            return "12 h\u00f3+"
        return f"{years} \u00e9v+"
    return raw


def normalize_age(value: Any) -> Any:
    values = dedupe([normalize_age_value(item) for item in flatten(value)])
    if isinstance(value, list):
        return values
    return values[0] if values else value


def extract_amount(name: str) -> str | None:
    pattern = re.compile(r"(?i)(\d+(?:[,.]\d+)?\s*(?:x\s*\d+(?:[,.]\d+)?\s*)?(?:kg|g|ml|l|db))")
    matches = pattern.findall(name.replace("\u00a0", " "))
    if not matches:
        return None
    return re.sub(r"\s+", " ", matches[-1].replace(",", ",")).strip()


def is_packaging(value: Any) -> bool:
    return value_key(value) in {value_key(item) for item in PACKAGING_VALUES}


def scalar_if_single(value: Any) -> Any:
    if isinstance(value, list):
        values = dedupe(value)
        if len(values) == 1:
            return values[0]
        return values
    return clean_scalar(value)


def coerce_product_props(tree: dict[str, Any], product: dict[str, Any]) -> dict[str, Any]:
    path = path_of(product)
    defs = effective_defs(tree, path)
    out: dict[str, Any] = {}
    for prop, value in (product.get(PROPS) or {}).items():
        pdef = defs.get(prop)
        if pdef:
            group, kind, _values = pdef
            if kind == "flag":
                out[prop] = bool(value) if not isinstance(value, bool) else value
            elif group == EGY:
                out[prop] = scalar_if_single(value)
            else:
                out[prop] = dedupe(flatten(value))
        else:
            out[prop] = copy.deepcopy(value)
    return out


def sync_product_values_to_leaf(tree: dict[str, Any], product: dict[str, Any]) -> None:
    path = path_of(product)
    node = ensure_path(tree, path)
    defs = effective_defs(tree, path)
    for prop, value in (product.get(PROPS) or {}).items():
        pdef = defs.get(prop)
        if pdef:
            group, kind, _values = pdef
            if kind == "flag":
                continue
            preferred = group
        else:
            preferred = CSOP if isinstance(value, list) and len(value) > 1 else EGY
        merge_prop_definition(node, prop, value, preferred_group=preferred)


def write_report(rows: list[list[Any]], counters: Counter[str], duplicate_summary: tuple[int, int]) -> None:
    def md(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ")

    def table(headers: list[str], data: list[list[Any]]) -> str:
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for row in data:
            lines.append("| " + " | ".join(md(item) for item in row) + " |")
        return "\n".join(lines)

    lines = [
        "# Baba kategoria javitas",
        "",
        f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Osszefoglalo",
        "",
        table(
            ["Muvelet", "Darab"],
            [
                ["Csomagolasra szetvalasztott kiszereles", counters["packaging_split"]],
                ["Termeknevbol visszatoltott mennyiseg", counters["amount_parsed"]],
                ["Normalizalt eletkor ertek", counters["age_normalized_values"]],
                ["Atmozgatott termek kategoriak kozott", counters["products_moved"]],
                ["Osszevont/torolt altipus", counters["alt_removed"]],
                ["Torolt ures alkategoria", counters["alk_removed"]],
                ["Torolt vagy osszevezetett regi tulajdonsagdefinicio", counters["old_prop_defs_removed"]],
                ["Termekhez szinkronizalt erteklista", counters["value_syncs"]],
                ["Ujraszamolt kategoria hash", counters["hash_recomputed"]],
                ["Erintett termek", counters["changed_products"]],
                ["Pontos duplikalt termeknevcsoport tovabbra is kulon kor", duplicate_summary[0]],
                ["Pontos duplikalt termeksor tovabbra is kulon kor", duplicate_summary[1]],
            ],
        ),
        "",
        "## Termek- es kategoria-szintu valtozasok",
        "",
        table(["Tipus", "Index", "Termek", "Regi", "Uj"], rows),
        "",
        "Megjegyzes: a pontos termeknev-duplikatumokat ez a kor nem torolte, mert ott forras/bolt es tulajdonsag-osszevezetes nelkul adatvesztes lehet.",
    ]
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    tree = load_json(TREE_PATH)
    products = load_json(PRODUCTS_PATH)
    ensure_path(tree, (BABY,))

    counters: Counter[str] = Counter()
    rows: list[list[Any]] = []
    changed_indices: set[int] = set()

    # Move the lone non-food item out of "Egyeb babaelelmiszer".
    old_pad_path = (BABY, BABY_FOOD_OTHER, CHANGING_PAD)
    new_pad_path = (BABY, BABY_CARE, CHANGING_PAD)
    old_pad_node = get_node(tree, old_pad_path)
    if old_pad_node is not None:
        new_pad_node = ensure_path(tree, new_pad_path)
        merge_node_props(new_pad_node, old_pad_node)
    for idx, product in enumerate(products):
        if path_of(product) == old_pad_path:
            set_product_path(product, new_pad_path)
            changed_indices.add(idx)
            counters["products_moved"] += 1
            rows.append(["pelenkazo_atsorolas", idx, product_name(product), " > ".join(old_pad_path), " > ".join(new_pad_path)])

    # Merge tiny fruit+grain subtype variants into the main fruit+grain subtype.
    for (src_ak, src_at), (dst_ak, dst_at) in MERGE_ALT_TYPES.items():
        src_path = (BABY, src_ak, src_at)
        dst_path = (BABY, dst_ak, dst_at)
        src_node = get_node(tree, src_path)
        if src_node is not None:
            dst_node = ensure_path(tree, dst_path)
            merge_node_props(dst_node, src_node)
        moved_here = 0
        for idx, product in enumerate(products):
            if path_of(product) == src_path:
                set_product_path(product, dst_path)
                changed_indices.add(idx)
                moved_here += 1
                rows.append(["altipus_osszevonas", idx, product_name(product), " > ".join(src_path), " > ".join(dst_path)])
        counters["products_moved"] += moved_here

    # Product property cleanup.
    for idx, product in enumerate(products):
        if product.get(FOK) != BABY:
            continue
        props = product.setdefault(PROPS, {})
        if not isinstance(props, dict):
            continue

        before_props = copy.deepcopy(props)

        if OLD_AGE in props:
            existing = flatten(props.get(AGE, [])) if AGE in props else []
            props[AGE] = dedupe(existing + flatten(props.pop(OLD_AGE)))

        if OLD_FEATURES in props:
            existing = flatten(props.get(FEATURE, [])) if FEATURE in props else []
            props[FEATURE] = dedupe(existing + flatten(props.pop(OLD_FEATURES)))

        if product.get(AK) == MILK_CEREAL and INGREDIENT in props:
            existing = flatten(props.get(GRAIN, [])) if GRAIN in props else []
            props[GRAIN] = dedupe(existing + flatten(props.pop(INGREDIENT)))

        if (product.get(AK), product.get(AT)) == (FORMULA, CHILD_DRINK_POWDER) and INGREDIENT in props:
            existing = flatten(props.get(GRAIN, [])) if GRAIN in props else []
            props[GRAIN] = dedupe(existing + flatten(props.pop(INGREDIENT)))

        if AGE in props:
            old_age = copy.deepcopy(props[AGE])
            props[AGE] = normalize_age(props[AGE])
            if props[AGE] != old_age:
                counters["age_normalized_values"] += len(flatten(old_age))

        if PACKAGE_SIZE in props:
            size_values = flatten(props[PACKAGE_SIZE])
            packaging_values = [item for item in size_values if is_packaging(item)]
            non_packaging_values = [item for item in size_values if not is_packaging(item)]
            if packaging_values:
                old_packaging = flatten(props.get(PACKAGING, [])) if PACKAGING in props else []
                props[PACKAGING] = scalar_if_single(dedupe(old_packaging + packaging_values))
                counters["packaging_split"] += 1

                amount = extract_amount(product_name(product))
                if amount:
                    non_packaging_values.append(amount)
                    counters["amount_parsed"] += 1
                if non_packaging_values:
                    props[PACKAGE_SIZE] = scalar_if_single(dedupe(non_packaging_values))
                else:
                    props.pop(PACKAGE_SIZE, None)

        if props != before_props:
            changed_indices.add(idx)
            rows.append(["tulajdonsag_javitas", idx, product_name(product), before_props, props])

    # Category tree cleanup and old definition merges.
    for path, node in walk_baba(tree):
        for prop, target in ((OLD_AGE, AGE), (OLD_FEATURES, FEATURE)):
            removed = remove_prop(node, prop)
            for group, value in removed:
                merge_prop_definition(node, target, normalize_age(value) if prop == OLD_AGE else value, preferred_group=group)
                counters["old_prop_defs_removed"] += 1
                rows.append(["regi_definicio_osszevezetes", "", "", " > ".join(path) + f" :: {prop}", target])

        if len(path) == 3 and path[1] in {MILK_CEREAL, FORMULA}:
            removed = remove_prop(node, INGREDIENT)
            for group, value in removed:
                merge_prop_definition(node, GRAIN, value, preferred_group=group)
                counters["old_prop_defs_removed"] += 1
                rows.append(["regi_definicio_osszevezetes", "", "", " > ".join(path) + f" :: {INGREDIENT}", GRAIN])

        # kiszereles is a single concrete amount; keep it out of csoportos.
        csop_props = prop_group(node, CSOP)
        if PACKAGE_SIZE in csop_props:
            value = csop_props.pop(PACKAGE_SIZE)
            merge_prop_definition(node, PACKAGE_SIZE, value, preferred_group=EGY)
            rows.append(["kiszereles_definicio_egyedi", "", "", " > ".join(path), PACKAGE_SIZE])

    # Remove source/empty alt types after product moves.
    baba = tree[BABY]
    for src_ak, src_at in MERGE_ALT_TYPES:
        alts = baba.get(ALK, {}).get(src_ak, {}).get(ALT, {})
        if src_at in alts:
            alts.pop(src_at)
            counters["alt_removed"] += 1
            rows.append(["altipus_torles", "", "", f"{BABY} > {src_ak} > {src_at}", "osszevonva"])

    snack_alts = baba.get(ALK, {}).get(BABY_SNACK, {}).get(ALT, {})
    if SPONGE_CAKE in snack_alts and not any(path_of(p) == (BABY, BABY_SNACK, SPONGE_CAKE) for p in products):
        snack_alts.pop(SPONGE_CAKE)
        counters["alt_removed"] += 1
        rows.append(["ures_altipus_torles", "", "", f"{BABY} > {BABY_SNACK} > {SPONGE_CAKE}", "torolve"])

    other_node = baba.get(ALK, {}).get(BABY_FOOD_OTHER)
    if isinstance(other_node, dict):
        other_alts = other_node.get(ALT, {})
        if isinstance(other_alts, dict) and CHANGING_PAD in other_alts and not any(path_of(p) == old_pad_path for p in products):
            other_alts.pop(CHANGING_PAD)
            counters["alt_removed"] += 1
            rows.append(["ures_altipus_torles", "", "", f"{BABY} > {BABY_FOOD_OTHER} > {CHANGING_PAD}", "atsorolva"])

    if isinstance(other_node, dict) and not other_node.get(ALT):
        baba[ALK].pop(BABY_FOOD_OTHER)
        counters["alk_removed"] += 1
        rows.append(["ures_alkategoria_torles", "", "", f"{BABY} > {BABY_FOOD_OTHER}", "torolve"])

    # Normalize age values inside remaining category definitions.
    for path, node in walk_baba(tree):
        for group in (EGY, CSOP):
            props = prop_group(node, group)
            if AGE in props and not isinstance(props[AGE], dict):
                old = copy.deepcopy(props[AGE])
                props[AGE] = dedupe([normalize_age_value(item) for item in flatten(props[AGE])])
                if props[AGE] != old:
                    rows.append(["eletkor_definicio_normalizalas", "", "", " > ".join(path), props[AGE]])

    # Re-sync every Baba product's used property values into its leaf category.
    before_sync_defs: dict[tuple[tuple[str, str, str], str], set[str]] = defaultdict(set)
    for idx, product in enumerate(products):
        if product.get(FOK) != BABY:
            continue
        product[PROPS] = coerce_product_props(tree, product)
        sync_product_values_to_leaf(tree, product)
        path = path_of(product)
        for prop, value in (product.get(PROPS) or {}).items():
            before_sync_defs[(path, prop)].update(value_key(item) for item in flatten(value))

    # Count value syncs from final direct leaf definitions by checking changed/added product values.
    # The exact changed definition count is less useful than the number of product values now represented.
    counters["value_syncs"] = sum(len(values) for values in before_sync_defs.values())

    for idx in sorted(changed_indices):
        product = products[idx]
        product["kategoria_hash"] = category_hash(product.get(FOK, ""), product.get(AK, ""), product.get(AT, ""), product.get(PROPS) or {})
        counters["hash_recomputed"] += 1
    counters["changed_products"] = len(changed_indices)

    # Duplicate products are intentionally left for a separate merge policy.
    by_name: dict[str, list[int]] = defaultdict(list)
    for idx, product in enumerate(products):
        if product.get(FOK) == BABY:
            by_name[product_name(product)].append(idx)
    duplicate_groups = {name: indices for name, indices in by_name.items() if name and len(indices) > 1}
    duplicate_summary = (len(duplicate_groups), sum(len(indices) for indices in duplicate_groups.values()))

    write_report(rows, counters, duplicate_summary)
    save_json_atomic(TREE_PATH, tree)
    save_json_atomic(PRODUCTS_PATH, products)

    print("Baba javitas kesz:", REPORT_PATH)
    print(json.dumps(dict(counters), ensure_ascii=False, indent=2))
    print(json.dumps({"duplicate_groups_left_for_next_round": duplicate_summary[0], "duplicate_rows_left_for_next_round": duplicate_summary[1]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
