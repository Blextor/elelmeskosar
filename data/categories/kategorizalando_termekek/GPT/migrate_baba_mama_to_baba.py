#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Move the Baba-mama main category into Baba.

The script is intentionally narrow: it only touches products whose current
`fokategoria` is `Baba-mama`, removes that top-level category from the tree,
and writes a Markdown migration report.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
TREE_PATH = BASE / "kategoriak_2026-06-13.json"
PRODUCTS_PATH = BASE / "eredmeny.json"
REPORT_PATH = BASE / "baba_mama_migracio_2026-06-23.md"

PROP = "tulajdons\u00e1gok"
ALK = "alkateg\u00f3ri\u00e1k"
ALT = "alt\u00edpusok"
EGY = "egyedi"
CSOP = "csoportos"
LEVEL_FIELDS = ("fokategoria", "alkategoria", "altipus")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_atomic(path: Path, data: Any) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=".baba_mama_", suffix=".json", dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def norm(text: Any) -> str:
    text = str(text).replace("õ", "ő").replace("û", "ű").replace("Õ", "Ő").replace("Û", "Ű")
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def value_key(value: Any) -> str:
    if isinstance(value, bool):
        return "bool:" + str(value).lower()
    return norm(value)


def flatten(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]


def clean_scalar(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


def dedupe_values(values: list[Any]) -> list[Any]:
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
    val = props.get(group, {})
    return val if isinstance(val, dict) else {}


def find_key(container: dict[str, Any], wanted_norm: str) -> str | None:
    for key in container:
        if norm(key) == wanted_norm:
            return key
    return None


def empty_node(level: int) -> dict[str, Any]:
    node: dict[str, Any] = {PROP: {EGY: {}, CSOP: {}}}
    if level == 1:
        node[ALK] = {}
    elif level == 2:
        node[ALT] = {}
    return node


def get_node(tree: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any] | None:
    node = tree.get(path[0]) if path else None
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


def resolve_path(tree: dict[str, Any], path_norms: tuple[str, ...], labels: tuple[str, ...] | None = None, create: bool = False) -> tuple[str, ...] | None:
    labels = labels or path_norms
    container = tree
    actual: list[str] = []
    for level, wanted in enumerate(path_norms, start=1):
        key = find_key(container, wanted)
        if key is None:
            if not create:
                return None
            key = labels[level - 1]
            container[key] = empty_node(level)
        actual.append(key)
        node = container[key]
        ensure_props(node)
        if level < len(path_norms):
            child_key = ALK if level == 1 else ALT
            if not isinstance(node.get(child_key), dict):
                node[child_key] = {}
            container = node[child_key]
    return tuple(actual)


def category_exists(tree: dict[str, Any], path: tuple[str, str, str]) -> bool:
    f, a, t = path
    node = tree.get(f)
    if not isinstance(node, dict):
        return False
    if a:
        node = node.get(ALK, {}).get(a)
        if not isinstance(node, dict):
            return False
    if t:
        node = node.get(ALT, {}).get(t)
        if not isinstance(node, dict):
            return False
    return True


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
            props[CSOP][prop] = dedupe_values(flatten(props[CSOP].get(prop, [])) + [value])
        else:
            props[EGY][prop] = {}
        return

    group = existing_group or preferred_group or (CSOP if isinstance(value, list) else EGY)
    incoming = dedupe_values(flatten(value))
    if group == EGY:
        current = props[EGY].get(prop)
        if isinstance(current, list):
            props[EGY][prop] = dedupe_values(current + incoming)
        elif isinstance(current, dict):
            props[EGY][prop] = current
        else:
            props[EGY][prop] = dedupe_values(([current] if current not in (None, "") else []) + incoming)
    else:
        current = props[CSOP].get(prop)
        if isinstance(current, list):
            props[CSOP][prop] = dedupe_values(current + incoming)
        else:
            props[CSOP][prop] = dedupe_values(([current] if current not in (None, "") and not isinstance(current, dict) else []) + incoming)


def direct_prop_defs(node: dict[str, Any]) -> dict[str, tuple[str, str, list[Any]]]:
    out: dict[str, tuple[str, str, list[Any]]] = {}
    for name, value in prop_group(node, EGY).items():
        if isinstance(value, dict):
            out[name] = (EGY, "flag", [])
        else:
            out[name] = (EGY, "single", dedupe_values(flatten(value)))
    for name, value in prop_group(node, CSOP).items():
        values = dedupe_values(flatten(value))
        if name in out and out[name][1] != "flag":
            values = dedupe_values(out[name][2] + values)
        out[name] = (CSOP, "multi", values)
    return out


def effective_defs(tree: dict[str, Any], path: tuple[str, str, str]) -> dict[str, tuple[str, str, list[Any]]]:
    out: dict[str, tuple[str, str, list[Any]]] = {}
    f, a, t = path
    fnode = tree.get(f)
    if isinstance(fnode, dict):
        out.update(direct_prop_defs(fnode))
        anode = fnode.get(ALK, {}).get(a) if a else None
        if isinstance(anode, dict):
            out.update(direct_prop_defs(anode))
            tnode = anode.get(ALT, {}).get(t) if t else None
            if isinstance(tnode, dict):
                out.update(direct_prop_defs(tnode))
    return out


def merge_node_props(dst: dict[str, Any], src: dict[str, Any]) -> None:
    for group in (EGY, CSOP):
        for prop, value in prop_group(src, group).items():
            merge_prop_definition(dst, prop, value, preferred_group=group)


def category_hash(fok: str, alk: str, alt: str, props: dict[str, Any]) -> str:
    key = f"{fok}|{alk}|{alt}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def source_category_structure(tree: dict[str, Any], fk: str) -> list[dict[str, Any]]:
    rows = []
    node = tree.get(fk, {})
    for ak, anode in node.get(ALK, {}).items():
        rows.append(
            {
                "path": (fk, ak),
                "egyedi": list(prop_group(anode, EGY).keys()),
                "csoportos": list(prop_group(anode, CSOP).keys()),
            }
        )
        for at, tnode in anode.get(ALT, {}).items():
            rows.append(
                {
                    "path": (fk, ak, at),
                    "egyedi": list(prop_group(tnode, EGY).keys()),
                    "csoportos": list(prop_group(tnode, CSOP).keys()),
                }
            )
    return rows


def target_for_product(product: dict[str, Any]) -> tuple[str, str, str]:
    ak = norm(product.get("alkategoria", ""))
    at = norm(product.get("altipus", ""))
    props = product.get("tulajdonsagok") or {}

    if ak == "baba snack":
        return ("Baba", "Bébi snack, keksz", "Puffasztott snack, ropi")
    if ak == "baba keksz":
        return ("Baba", "Bébi snack, keksz", "Bébikeksz")
    if ak == "baba ital":
        return ("Baba", "Bébiital, víz", "Gyümölcslé, gyerekital")
    if ak == "baba italpor":
        return ("Baba", "Tápszer", "Gyermek italpor")

    if ak == "babaetel":
        if at == "bio gyumolcspure":
            return ("Baba", "Gyümölcspüré, bébidesszert", "Gyümölcspüré")
        if at == "baba zabkasa":
            return ("Baba", "Tejpép, gabonapép, kása", "Zabkása, instant kása")
        if at in {"baba gabonakasa", "baba gabonapep", "baba rizskasa", "folyekony gabonas bebietel"}:
            return ("Baba", "Tejpép, gabonapép, kása", "Gabonapép")
        if at in {"baba tejpep", "baba tejberizs", "baba tejbegriz", "baba tejberizspep"}:
            return ("Baba", "Tejpép, gabonapép, kása", "Tejpép")

    if ak == "tapszer":
        if at == "junior tapszer":
            return ("Baba", "Tápszer", "Junior tápszer (1-3 év)")
        if at in {"ha junior tapszer", "ha tapszer", "specialis tapszer"}:
            return ("Baba", "Tápszer", "Speciális tápszer")
        if at == "anyatej helyettesito tapszer":
            return ("Baba", "Tápszer", "Anyatej-helyettesítő (1-es)")
        if at == "anyatej kiegeszito tapszer":
            fokozat_values = [norm(v) for v in flatten(props.get("fokozat", []))]
            term_type = " ".join(norm(v) for v in flatten(props.get("terméktípus", [])))
            name = norm(product.get("termek", {}).get("product_name", ""))
            if "junior" in term_type or "junior" in name:
                return ("Baba", "Tápszer", "Junior tápszer (1-3 év)")
            if any(v == "3" for v in fokozat_values):
                return ("Baba", "Tápszer", "Követő tápszer (3-as)")
            return ("Baba", "Tápszer", "Követő tápszer (2-es)")

    if ak == "babaapolasi eszkoz":
        # Not food, but the main category must disappear. Keep the original
        # specific subtype under a new Baba subcategory.
        return ("Baba", "Babaápolási eszköz", product.get("altipus", "") or "Egyéb babaápolási eszköz")

    raise ValueError(f"Nincs migracios cel: {product.get('alkategoria')} > {product.get('altipus')}")


def rename_and_coerce_props(tree: dict[str, Any], target: tuple[str, str, str], props: dict[str, Any]) -> dict[str, Any]:
    renamed: dict[str, Any] = {}
    for key, value in props.items():
        new_key = key
        if key == "korosztály":
            new_key = "életkor"
        elif key == "jellemzők":
            new_key = "jellemző"
        elif key == "alapanyag" and target[1] == "Tejpép, gabonapép, kása":
            new_key = "gabona"

        if new_key in renamed:
            old = renamed[new_key]
            renamed[new_key] = dedupe_values(flatten(old) + flatten(value))
        else:
            renamed[new_key] = copy.deepcopy(value)

    defs = effective_defs(tree, target)
    coerced: dict[str, Any] = {}
    for key, value in renamed.items():
        pdef = defs.get(key)
        if pdef:
            group, kind, _values = pdef
            if kind == "flag":
                if isinstance(value, bool):
                    coerced[key] = value
                elif isinstance(value, list):
                    coerced[key] = bool(value)
                else:
                    coerced[key] = str(value).strip().lower() not in {"", "nem", "false", "0"}
            elif group == EGY:
                vals = dedupe_values(flatten(value))
                coerced[key] = vals[0] if len(vals) == 1 else vals
            else:
                coerced[key] = dedupe_values(flatten(value))
        else:
            if isinstance(value, list):
                coerced[key] = dedupe_values(value)
            else:
                coerced[key] = clean_scalar(value)
    return coerced


def sync_product_props_to_target(tree: dict[str, Any], target: tuple[str, str, str], props: dict[str, Any]) -> None:
    node = get_node(tree, target)
    if node is None:
        raise RuntimeError("Missing target node: " + " > ".join(target))
    defs = effective_defs(tree, target)
    for key, value in props.items():
        pdef = defs.get(key)
        preferred_group = pdef[0] if pdef else (CSOP if isinstance(value, list) else EGY)
        merge_prop_definition(node, key, value, preferred_group=preferred_group)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(md_escape(v) for v in row) + " |")
    return "\n".join(out)


def write_report(
    report_rows: list[dict[str, Any]],
    before_baba: list[dict[str, Any]],
    before_baba_mama: list[dict[str, Any]],
    validation: dict[str, Any],
) -> None:
    lines = []
    lines.append("# Baba-mama migracio Baba ala")
    lines.append("")
    lines.append(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("Forrasok:")
    lines.append(f"- `{TREE_PATH.as_posix()}`")
    lines.append(f"- `{PRODUCTS_PATH.as_posix()}`")
    lines.append("")
    lines.append("## Osszefoglalo")
    lines.append("")
    by_target = Counter(row["new_path"] for row in report_rows)
    lines.append(
        table(
            ["Meres", "Darab"],
            [
                ["Erintett Baba-mama termek", len(report_rows)],
                ["Baba-mama főkategoria maradt a kategoriakban", validation["baba_mama_in_tree"]],
                ["Baba-mama termek maradt", validation["baba_mama_products_left"]],
                ["Erintett termekek hianyzo celkategoriaval", validation["missing_target_for_moved"]],
                ["Erintett termekek nem deklaralt tulajdonsaggal/ertekkel", validation["moved_property_issues"]],
            ],
        )
    )
    lines.append("")
    lines.append("### Uj celkategoriak darabszam szerint")
    lines.append("")
    lines.append(table(["Cel kategoriaut", "Termek"], [[path, count] for path, count in by_target.most_common()]))
    lines.append("")

    lines.append("## Kiindulo Baba szerkezet")
    lines.append("")
    lines.append(
        table(
            ["Kategoriaut", "Egyedi tulajdonsagok", "Csoportos tulajdonsagok"],
            [[ " > ".join(row["path"]), ", ".join(row["egyedi"]), ", ".join(row["csoportos"]) ] for row in before_baba],
        )
    )
    lines.append("")
    lines.append("## Kiindulo Baba-mama szerkezet")
    lines.append("")
    lines.append(
        table(
            ["Kategoriaut", "Egyedi tulajdonsagok", "Csoportos tulajdonsagok"],
            [[ " > ".join(row["path"]), ", ".join(row["egyedi"]), ", ".join(row["csoportos"]) ] for row in before_baba_mama],
        )
    )
    lines.append("")

    lines.append("## Erintett termekek es besorolasuk")
    lines.append("")
    lines.append(
        table(
            ["Index", "Termek", "Regi kategoriaut", "Uj kategoriaut", "Tulajdonsag-kulcs modositas"],
            [
                [
                    row["index"],
                    row["product_name"],
                    row["old_path"],
                    row["new_path"],
                    ", ".join(row["property_changes"]) if row["property_changes"] else "",
                ]
                for row in report_rows
            ],
        )
    )
    lines.append("")
    if validation["property_issue_samples"]:
        lines.append("## Validacios mintak")
        lines.append("")
        lines.append(
            table(
                ["Hiba", "Index", "Kategoriaut", "Tulajdonsag", "Ertek"],
                validation["property_issue_samples"],
            )
        )
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def validate_moved(tree: dict[str, Any], products: list[dict[str, Any]], moved_indices: set[int]) -> dict[str, Any]:
    issues = []
    for idx in moved_indices:
        product = products[idx]
        target = tuple(product.get(field, "") or "" for field in LEVEL_FIELDS)
        if not category_exists(tree, target):
            issues.append(["missing_target", idx, " > ".join(target), "", ""])
            continue
        defs = effective_defs(tree, target)
        for key, value in (product.get("tulajdonsagok") or {}).items():
            pdef = defs.get(key)
            if not pdef:
                issues.append(["missing_property", idx, " > ".join(target), key, value])
                continue
            _group, kind, values = pdef
            if kind == "flag":
                continue
            if values:
                allowed = {value_key(v) for v in values}
                for item in flatten(value):
                    if item in ("", None):
                        continue
                    if value_key(item) not in allowed:
                        issues.append(["missing_value", idx, " > ".join(target), key, item])
    return {
        "baba_mama_in_tree": "Baba-mama" in tree,
        "baba_mama_products_left": sum(1 for p in products if p.get("fokategoria") == "Baba-mama"),
        "missing_target_for_moved": sum(1 for issue in issues if issue[0] == "missing_target"),
        "moved_property_issues": sum(1 for issue in issues if issue[0] != "missing_target"),
        "property_issue_samples": issues[:50],
    }


def main() -> int:
    tree = load_json(TREE_PATH)
    products = load_json(PRODUCTS_PATH)

    if "Baba-mama" not in tree:
        print("Nincs Baba-mama főkategória; nincs teendő.")
        return 0

    before_baba = source_category_structure(tree, "Baba")
    before_baba_mama = source_category_structure(tree, "Baba-mama")
    affected = [idx for idx, product in enumerate(products) if product.get("fokategoria") == "Baba-mama"]

    baba = tree.setdefault("Baba", {PROP: {EGY: {}, CSOP: {}}, ALK: {}})
    baba.setdefault(ALK, {})
    baba_mama = tree["Baba-mama"]

    # Preserve the non-food baby-care branch under Baba, because the main
    # Baba-mama category must disappear and no existing Baba branch fits it.
    apol_source = baba_mama.get(ALK, {}).get("Babaápolási eszköz")
    if isinstance(apol_source, dict):
        if "Babaápolási eszköz" not in baba[ALK]:
            baba[ALK]["Babaápolási eszköz"] = copy.deepcopy(apol_source)
        else:
            merge_node_props(baba[ALK]["Babaápolási eszköz"], apol_source)
            for at, node in apol_source.get(ALT, {}).items():
                baba[ALK]["Babaápolási eszköz"].setdefault(ALT, {}).setdefault(at, copy.deepcopy(node))

    report_rows: list[dict[str, Any]] = []
    moved_indices: set[int] = set()

    for idx in affected:
        product = products[idx]
        old_path = tuple(product.get(field, "") or "" for field in LEVEL_FIELDS)
        target = target_for_product(product)
        resolve_path(tree, tuple(norm(x) for x in target), labels=target, create=True)

        # Merge the source subtype definition into the chosen target subtype.
        source_path = resolve_path(tree, tuple(norm(x) for x in old_path), create=False)
        if source_path:
            source_node = get_node(tree, source_path)
            target_node = get_node(tree, target)
            if source_node and target_node:
                merge_node_props(target_node, source_node)

        old_props = product.get("tulajdonsagok") or {}
        new_props = rename_and_coerce_props(tree, target, old_props)
        property_changes = []
        if "korosztály" in old_props:
            property_changes.append("korosztály -> életkor")
        if "jellemzők" in old_props:
            property_changes.append("jellemzők -> jellemző")
        if "alapanyag" in old_props and target[1] == "Tejpép, gabonapép, kása":
            property_changes.append("alapanyag -> gabona")

        product["fokategoria"], product["alkategoria"], product["altipus"] = target
        product["tulajdonsagok"] = new_props
        sync_product_props_to_target(tree, target, new_props)
        product["kategoria_hash"] = category_hash(target[0], target[1], target[2], new_props)

        moved_indices.add(idx)
        report_rows.append(
            {
                "index": idx,
                "product_name": product.get("termek", {}).get("product_name", ""),
                "old_path": " > ".join(old_path),
                "new_path": " > ".join(target),
                "property_changes": property_changes,
            }
        )

    tree.pop("Baba-mama", None)

    validation = validate_moved(tree, products, moved_indices)
    write_report(report_rows, before_baba, before_baba_mama, validation)

    if validation["baba_mama_in_tree"] or validation["baba_mama_products_left"] or validation["missing_target_for_moved"] or validation["moved_property_issues"]:
        print("Validációs hiba, nem mentek JSON-t. Riport:", REPORT_PATH)
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        return 1

    save_json_atomic(TREE_PATH, tree)
    save_json_atomic(PRODUCTS_PATH, products)

    print("Baba-mama termékek átsorolva:", len(report_rows))
    print("Riport:", REPORT_PATH)
    print("Mentve:", TREE_PATH)
    print("Mentve:", PRODUCTS_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
