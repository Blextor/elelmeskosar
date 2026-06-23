#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit empty category/property definitions and orphan product classifications.

Reads:
  - kategoriak_2026-06-13.json
  - eredmeny.json

Writes a Markdown report. The script does not modify the source JSON files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
DEFAULT_TREE = BASE / "kategoriak_2026-06-13.json"
DEFAULT_PRODUCTS = BASE / "eredmeny.json"
DEFAULT_REPORT = BASE / "kategoria_audit_ures_arva_2026-06-23.md"

PROP = "tulajdons\u00e1gok"
ALK = "alkateg\u00f3ri\u00e1k"
ALT = "alt\u00edpusok"
EGY = "egyedi"
CSOP = "csoportos"
LEVEL_FIELDS = ("fokategoria", "alkategoria", "altipus")


@dataclass(frozen=True)
class PropDef:
    group: str
    kind: str  # flag, single, multi
    values: tuple[Any, ...]
    declared_at: tuple[str, ...]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fix_letters(text: str) -> str:
    return (
        text.replace("\u00f5", "\u0151")
        .replace("\u00fb", "\u0171")
        .replace("\u00d5", "\u0150")
        .replace("\u00db", "\u0170")
    )


def norm(text: Any) -> str:
    text = fix_letters(str(text))
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def value_key(value: Any) -> str:
    if isinstance(value, bool):
        return "bool:" + str(value).lower()
    return norm(value)


def fmt_path(parts: tuple[str, ...] | list[str]) -> str:
    return " > ".join([p for p in parts if p])


def prop_group(props: Any, group: str) -> dict[str, Any]:
    if not isinstance(props, dict):
        return {}
    val = props.get(group, {})
    return val if isinstance(val, dict) else {}


def walk_nodes(tree: dict[str, Any]):
    for fk, fnode in tree.items():
        yield (fk,), fnode
        for ak, anode in fnode.get(ALK, {}).items():
            yield (fk, ak), anode
            for at, tnode in anode.get(ALT, {}).items():
                yield (fk, ak, at), tnode


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


def direct_prop_defs(node: dict[str, Any], path: tuple[str, ...]) -> dict[str, PropDef]:
    out: dict[str, PropDef] = {}
    props = node.get(PROP, {})
    for name, value in prop_group(props, EGY).items():
        if isinstance(value, dict):
            out[name] = PropDef(EGY, "flag", tuple(), path)
        elif isinstance(value, list):
            out[name] = PropDef(EGY, "single", tuple(value), path)
        else:
            out[name] = PropDef(EGY, "single", (value,), path)
    for name, value in prop_group(props, CSOP).items():
        if isinstance(value, list):
            out[name] = PropDef(CSOP, "multi", tuple(value), path)
        elif isinstance(value, dict):
            out[name] = PropDef(CSOP, "multi", tuple(), path)
        else:
            out[name] = PropDef(CSOP, "multi", (value,), path)
    return out


def effective_prop_defs(tree: dict[str, Any], fk: str, ak: str, at: str) -> dict[str, PropDef]:
    """Effective inherited property definitions for a product path.

    Mirrors the editor behavior: main category props are inherited, then
    subcategory props override same-name props, then subtype props override them.
    """
    out: dict[str, PropDef] = {}
    fnode = tree.get(fk)
    if not isinstance(fnode, dict):
        return out
    out.update(direct_prop_defs(fnode, (fk,)))
    if ak:
        anode = fnode.get(ALK, {}).get(ak)
        if isinstance(anode, dict):
            out.update(direct_prop_defs(anode, (fk, ak)))
            if at:
                tnode = anode.get(ALT, {}).get(at)
                if isinstance(tnode, dict):
                    out.update(direct_prop_defs(tnode, (fk, ak, at)))
    return out


def category_issue(tree: dict[str, Any], fk: str, ak: str, at: str) -> str | None:
    fnode = tree.get(fk)
    if not isinstance(fnode, dict):
        return "missing_fokategoria"
    if not ak:
        return None
    anode = fnode.get(ALK, {}).get(ak)
    if not isinstance(anode, dict):
        return "missing_alkategoria"
    if not at:
        return None
    tnode = anode.get(ALT, {}).get(at)
    if not isinstance(tnode, dict):
        return "missing_altipus"
    return None


def product_path(product: dict[str, Any]) -> tuple[str, str, str]:
    return tuple(product.get(field, "") or "" for field in LEVEL_FIELDS)  # type: ignore[return-value]


def path_prefix_matches(path: tuple[str, ...], triple: tuple[str, str, str]) -> bool:
    return all(triple[i] == path[i] for i in range(len(path)))


def exact_path_matches(path: tuple[str, ...], triple: tuple[str, str, str]) -> bool:
    if not path_prefix_matches(path, triple):
        return False
    return all(not triple[i] for i in range(len(path), 3))


def flatten_value(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return [value]


def is_empty_scalar(value: Any) -> bool:
    return value is None or value == ""


def audit(tree: dict[str, Any], products: list[dict[str, Any]]) -> dict[str, Any]:
    triples = [product_path(p) for p in products if isinstance(p, dict)]
    subtree_counts: Counter[tuple[str, ...]] = Counter()
    exact_counts: Counter[tuple[str, ...]] = Counter()
    for triple in triples:
        exact_len = 1
        if triple[1]:
            exact_len = 2
        if triple[2]:
            exact_len = 3
        exact_counts[triple[:exact_len]] += 1
        for length in (1, 2, 3):
            if triple[length - 1]:
                subtree_counts[triple[:length]] += 1

    category_rows = []
    category_totals = Counter()
    direct_prop_usage: Counter[tuple[tuple[str, ...], str]] = Counter()
    effective_prop_usage: Counter[tuple[str, str, str, str]] = Counter()

    for path, node in walk_nodes(tree):
        props = node.get(PROP, {})
        direct_defs = direct_prop_defs(node, path)
        has_children = bool(node.get(ALK) or node.get(ALT))
        has_direct_props = bool(direct_defs)
        row = {
            "path": path,
            "level": len(path),
            "subtree_products": subtree_counts[path],
            "exact_products": exact_counts[path],
            "has_children": has_children,
            "direct_property_count": len(direct_defs),
            "structurally_empty": (not has_children and not has_direct_props),
            "subtree_empty": subtree_counts[path] == 0,
            "exact_empty": exact_counts[path] == 0,
            "prop_group_shape_errors": [],
        }
        if not isinstance(props, dict):
            row["prop_group_shape_errors"].append("tulajdonsagok_not_dict")
        else:
            for group in (EGY, CSOP):
                if not isinstance(props.get(group, {}), dict):
                    row["prop_group_shape_errors"].append(f"{group}_not_dict")
        category_rows.append(row)
        category_totals[f"level_{len(path)}"] += 1
        if row["subtree_empty"]:
            category_totals[f"level_{len(path)}_subtree_empty"] += 1
        if row["exact_empty"]:
            category_totals[f"level_{len(path)}_exact_empty"] += 1
        if row["structurally_empty"]:
            category_totals[f"level_{len(path)}_structurally_empty"] += 1

    product_issues = []
    product_issue_counts = Counter()
    product_issue_products: dict[str, set[int]] = defaultdict(set)
    prop_value_issue_counter: Counter[tuple[str, str, Any]] = Counter()
    prop_key_issue_counter: Counter[tuple[str, str]] = Counter()
    category_issue_counter: Counter[tuple[str, str]] = Counter()

    for idx, product in enumerate(products):
        if not isinstance(product, dict):
            continue
        fk, ak, at = product_path(product)
        issue = category_issue(tree, fk, ak, at)
        path_text = fmt_path([fk, ak, at])
        if issue:
            product_issue_counts[issue] += 1
            product_issue_products[issue].add(idx)
            category_issue_counter[(issue, path_text)] += 1
            product_issues.append(
                {
                    "type": issue,
                    "index": idx,
                    "path": path_text,
                    "product_name": product.get("termek", {}).get("product_name", ""),
                }
            )
            continue

        defs = effective_prop_defs(tree, fk, ak, at)
        props = product.get("tulajdonsagok", {})
        if not isinstance(props, dict):
            product_issue_counts["product_props_not_dict"] += 1
            product_issue_products["product_props_not_dict"].add(idx)
            product_issues.append(
                {
                    "type": "product_props_not_dict",
                    "index": idx,
                    "path": path_text,
                    "product_name": product.get("termek", {}).get("product_name", ""),
                }
            )
            continue

        for prop_name, value in props.items():
            pdef = defs.get(prop_name)
            if pdef is None:
                product_issue_counts["property_not_declared_for_category"] += 1
                product_issue_products["property_not_declared_for_category"].add(idx)
                prop_key_issue_counter[(path_text, prop_name)] += 1
                product_issues.append(
                    {
                        "type": "property_not_declared_for_category",
                        "index": idx,
                        "path": path_text,
                        "property": prop_name,
                        "value": value,
                        "product_name": product.get("termek", {}).get("product_name", ""),
                    }
                )
                continue

            direct_prop_usage[(pdef.declared_at, prop_name)] += 1
            effective_prop_usage[(fk, ak, at, prop_name)] += 1

            if pdef.kind == "flag":
                if not isinstance(value, bool):
                    product_issue_counts["property_shape_mismatch"] += 1
                    product_issue_products["property_shape_mismatch"].add(idx)
                    product_issues.append(
                        {
                            "type": "property_shape_mismatch",
                            "index": idx,
                            "path": path_text,
                            "property": prop_name,
                            "expected": "bool flag",
                            "actual": type(value).__name__,
                            "value": value,
                            "product_name": product.get("termek", {}).get("product_name", ""),
                        }
                    )
                continue

            if pdef.kind == "multi":
                if not isinstance(value, list):
                    product_issue_counts["property_shape_mismatch"] += 1
                    product_issue_products["property_shape_mismatch"].add(idx)
                    product_issues.append(
                        {
                            "type": "property_shape_mismatch",
                            "index": idx,
                            "path": path_text,
                            "property": prop_name,
                            "expected": "list/csoportos",
                            "actual": type(value).__name__,
                            "value": value,
                            "product_name": product.get("termek", {}).get("product_name", ""),
                        }
                    )
                    values = flatten_value(value)
                else:
                    values = value
            else:
                if isinstance(value, list):
                    product_issue_counts["property_shape_mismatch"] += 1
                    product_issue_products["property_shape_mismatch"].add(idx)
                    product_issues.append(
                        {
                            "type": "property_shape_mismatch",
                            "index": idx,
                            "path": path_text,
                            "property": prop_name,
                            "expected": "scalar/egyedi",
                            "actual": "list",
                            "value": value,
                            "product_name": product.get("termek", {}).get("product_name", ""),
                        }
                    )
                    values = value
                else:
                    values = [value]

            if pdef.values:
                allowed = {value_key(v) for v in pdef.values}
                for item in values:
                    if is_empty_scalar(item):
                        continue
                    if value_key(item) not in allowed:
                        product_issue_counts["property_value_not_allowed"] += 1
                        product_issue_products["property_value_not_allowed"].add(idx)
                        prop_value_issue_counter[(path_text, prop_name, item)] += 1
                        product_issues.append(
                            {
                                "type": "property_value_not_allowed",
                                "index": idx,
                                "path": path_text,
                                "property": prop_name,
                                "value": item,
                                "product_name": product.get("termek", {}).get("product_name", ""),
                            }
                        )
            else:
                # Non-flag list properties with no allowed values are suspicious
                # when products contain a non-empty value.
                for item in values:
                    if not is_empty_scalar(item):
                        product_issue_counts["property_has_no_allowed_values"] += 1
                        product_issue_products["property_has_no_allowed_values"].add(idx)
                        prop_value_issue_counter[(path_text, prop_name, item)] += 1
                        product_issues.append(
                            {
                                "type": "property_has_no_allowed_values",
                                "index": idx,
                                "path": path_text,
                                "property": prop_name,
                                "value": item,
                                "product_name": product.get("termek", {}).get("product_name", ""),
                            }
                        )

    property_rows = []
    property_totals = Counter()
    duplicate_value_rows = []
    for path, node in walk_nodes(tree):
        props = node.get(PROP, {})
        for group in (EGY, CSOP):
            for prop_name, raw_value in prop_group(props, group).items():
                if isinstance(raw_value, dict):
                    kind = "flag"
                    value_count = 0
                    empty_values = False
                    duplicate_values = []
                elif isinstance(raw_value, list):
                    kind = "single" if group == EGY else "multi"
                    value_count = len(raw_value)
                    empty_values = len(raw_value) == 0
                    seen = {}
                    duplicate_values = []
                    for item in raw_value:
                        key = value_key(item)
                        if key in seen:
                            duplicate_values.append((seen[key], item))
                        else:
                            seen[key] = item
                else:
                    kind = "scalar_definition"
                    value_count = 1
                    empty_values = is_empty_scalar(raw_value)
                    duplicate_values = []
                usage = direct_prop_usage[(path, prop_name)]
                row = {
                    "path": path,
                    "group": group,
                    "property": prop_name,
                    "kind": kind,
                    "value_count": value_count,
                    "empty_values": empty_values,
                    "usage": usage,
                    "unused": usage == 0,
                    "duplicate_values": duplicate_values,
                }
                property_rows.append(row)
                property_totals["total"] += 1
                property_totals[f"group_{group}"] += 1
                property_totals[f"kind_{kind}"] += 1
                if empty_values:
                    property_totals["empty_value_list_or_scalar"] += 1
                if usage == 0:
                    property_totals["unused"] += 1
                if duplicate_values:
                    property_totals["with_duplicate_values"] += 1
                    duplicate_value_rows.append(row)

    return {
        "category_rows": category_rows,
        "category_totals": category_totals,
        "property_rows": property_rows,
        "property_totals": property_totals,
        "duplicate_value_rows": duplicate_value_rows,
        "product_issue_counts": product_issue_counts,
        "product_issue_products": {k: len(v) for k, v in product_issue_products.items()},
        "product_issues": product_issues,
        "prop_value_issue_counter": prop_value_issue_counter,
        "prop_key_issue_counter": prop_key_issue_counter,
        "category_issue_counter": category_issue_counter,
        "products_count": len(products),
        "tree_node_count": len(category_rows),
    }


def md_escape(value: Any) -> str:
    text = str(value)
    text = text.replace("|", "\\|").replace("\n", " ")
    return text


def table(headers: list[str], rows: list[list[Any]]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        out.append("| " + " | ".join(md_escape(v) for v in row) + " |")
    return "\n".join(out)


def top_rows(counter: Counter, limit: int = 30):
    return counter.most_common(limit)


def write_report(report: Path, tree_path: Path, products_path: Path, data: dict[str, Any]) -> None:
    category_rows = data["category_rows"]
    property_rows = data["property_rows"]
    category_totals = data["category_totals"]
    property_totals = data["property_totals"]
    product_issue_counts = data["product_issue_counts"]
    product_issue_products = data["product_issue_products"]

    empty_subtree = [r for r in category_rows if r["subtree_empty"]]
    structurally_empty = [r for r in category_rows if r["structurally_empty"]]
    empty_value_props = [r for r in property_rows if r["empty_values"]]
    unused_props = [r for r in property_rows if r["unused"]]
    shape_error_nodes = [r for r in category_rows if r["prop_group_shape_errors"]]

    lines = []
    lines.append("# Kategoria- es tulajdonsag-audit")
    lines.append("")
    lines.append(f"Datum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("Forrasok:")
    lines.append(f"- `{tree_path.as_posix()}`")
    lines.append(f"- `{products_path.as_posix()}`")
    lines.append("")
    lines.append("Megjegyzes: a script csak olvasott; a JSON forrasfajlokat nem modositotta.")
    lines.append("")

    lines.append("## Osszefoglalo")
    lines.append("")
    lines.append(
        table(
            ["Meres", "Darab"],
            [
                ["Termekek", data["products_count"]],
                ["Kategoriafa node-ok osszesen", data["tree_node_count"]],
                ["Termek nelkuli kategoria-node subtree szerint", len(empty_subtree)],
                ["Szerkezetileg ures kategoria-node", len(structurally_empty)],
                ["Tulajdonsag-deklaraciok osszesen", property_totals["total"]],
                ["Ures erteklistaju/skalaru tulajdonsag-deklaracio", len(empty_value_props)],
                ["Termekekben nem hasznalt tulajdonsag-deklaracio", len(unused_props)],
                ["Duplikalt erteket tartalmazo tulajdonsag-deklaracio", property_totals["with_duplicate_values"]],
                ["Kategoriat/tulajdonsagot/erteket erinto termekhibak osszesen", sum(product_issue_counts.values())],
                ["Erintett termekek legalabb egy hibaval", len({i["index"] for i in data["product_issues"]})],
            ],
        )
    )
    lines.append("")

    lines.append("## Kategoria-node uresseg")
    lines.append("")
    lines.append(
        table(
            ["Szint", "Node osszesen", "Subtree szerint termek nelkuli", "Exact besorolas nelkuli", "Szerkezetileg ures"],
            [
                [
                    "Fokategoria",
                    category_totals["level_1"],
                    category_totals["level_1_subtree_empty"],
                    category_totals["level_1_exact_empty"],
                    category_totals["level_1_structurally_empty"],
                ],
                [
                    "Alkategoria",
                    category_totals["level_2"],
                    category_totals["level_2_subtree_empty"],
                    category_totals["level_2_exact_empty"],
                    category_totals["level_2_structurally_empty"],
                ],
                [
                    "Altipus",
                    category_totals["level_3"],
                    category_totals["level_3_subtree_empty"],
                    category_totals["level_3_exact_empty"],
                    category_totals["level_3_structurally_empty"],
                ],
            ],
        )
    )
    lines.append("")
    lines.append("### Termek nelkuli kategoria-node-ok mintak")
    lines.append("")
    rows = [
        [fmt_path(r["path"]), r["level"], r["subtree_products"], r["exact_products"], r["direct_property_count"]]
        for r in empty_subtree[:80]
    ]
    lines.append(table(["Kategoriaut", "Szint", "Subtree termek", "Exact termek", "Direkt tulajdonsag"], rows) if rows else "Nincs ilyen.")
    lines.append("")

    if shape_error_nodes:
        lines.append("### Hibas tulajdonsag-csoport szerkezetu node-ok")
        lines.append("")
        lines.append(
            table(
                ["Kategoriaut", "Hiba"],
                [[fmt_path(r["path"]), ", ".join(r["prop_group_shape_errors"])] for r in shape_error_nodes],
            )
        )
        lines.append("")

    lines.append("## Tulajdonsagok uressege")
    lines.append("")
    lines.append(
        table(
            ["Meres", "Darab"],
            [
                ["Osszes tulajdonsag-deklaracio", property_totals["total"]],
                ["Egyedi deklaracio", property_totals["group_egyedi"]],
                ["Csoportos deklaracio", property_totals["group_csoportos"]],
                ["Flag jellegu deklaracio", property_totals["kind_flag"]],
                ["Ures erteklistaju/skalaru deklaracio", property_totals["empty_value_list_or_scalar"]],
                ["Termekekben nem hasznalt deklaracio", property_totals["unused"]],
                ["Duplikalt ertekeket tartalmaz", property_totals["with_duplicate_values"]],
            ],
        )
    )
    lines.append("")

    lines.append("### Ures erteklistaju tulajdonsag-deklaraciok mintak")
    lines.append("")
    rows = [
        [fmt_path(r["path"]), r["group"], r["property"], r["kind"], r["usage"]]
        for r in empty_value_props[:80]
    ]
    lines.append(table(["Kategoriaut", "Csoport", "Tulajdonsag", "Tipus", "Termekhasznalat"], rows) if rows else "Nincs ilyen.")
    lines.append("")

    lines.append("### Nem hasznalt tulajdonsag-deklaraciok mintak")
    lines.append("")
    rows = [
        [fmt_path(r["path"]), r["group"], r["property"], r["kind"], r["value_count"]]
        for r in unused_props[:80]
    ]
    lines.append(table(["Kategoriaut", "Csoport", "Tulajdonsag", "Tipus", "Ertekek"], rows) if rows else "Nincs ilyen.")
    lines.append("")

    lines.append("## Termekek nem illeszkedo adatai")
    lines.append("")
    issue_rows = []
    for issue_type, count in sorted(product_issue_counts.items(), key=lambda item: (-item[1], item[0])):
        issue_rows.append([issue_type, count, product_issue_products.get(issue_type, 0)])
    lines.append(table(["Hibatipus", "Elofordulas", "Erintett termek"], issue_rows) if issue_rows else "Nincs termekhiba.")
    lines.append("")

    if data["category_issue_counter"]:
        lines.append("### Hianyzo kategoriautak")
        lines.append("")
        rows = [[issue, path, count] for (issue, path), count in top_rows(data["category_issue_counter"], 50)]
        lines.append(table(["Hiba", "Termek kategoriaut", "Darab"], rows))
        lines.append("")

    if data["prop_key_issue_counter"]:
        lines.append("### Kategoriaban nem deklaralt termek-tulajdonsagok")
        lines.append("")
        rows = [[path, prop, count] for (path, prop), count in top_rows(data["prop_key_issue_counter"], 80)]
        lines.append(table(["Kategoriaut", "Tulajdonsag", "Darab"], rows))
        lines.append("")

    if data["prop_value_issue_counter"]:
        lines.append("### Nem engedelyezett vagy erteklista nelkuli termek-tulajdonsagertekek")
        lines.append("")
        rows = [
            [path, prop, value, count]
            for (path, prop, value), count in top_rows(data["prop_value_issue_counter"], 120)
        ]
        lines.append(table(["Kategoriaut", "Tulajdonsag", "Ertek", "Darab"], rows))
        lines.append("")

    lines.append("### Termekhiba mintak")
    lines.append("")
    sample_rows = []
    for issue in data["product_issues"][:120]:
        sample_rows.append(
            [
                issue.get("type", ""),
                issue.get("index", ""),
                issue.get("path", ""),
                issue.get("property", ""),
                issue.get("value", ""),
                issue.get("product_name", ""),
            ]
        )
    lines.append(table(["Hiba", "Index", "Kategoriaut", "Tulajdonsag", "Ertek", "Termek"], sample_rows) if sample_rows else "Nincs minta, mert nincs termekhiba.")
    lines.append("")

    lines.append("## Ertelmezes")
    lines.append("")
    lines.append("- `subtree szerint termek nelkuli`: az adott node ala egyetlen termek sem esik, leszarmozott altipussal sem.")
    lines.append("- `exact besorolas nelkuli`: pont arra a node-ra nincs termek; ettol meg lehetnek alatta termekek.")
    lines.append("- `property_not_declared_for_category`: a termek tulajdonsaga nincs deklaralva a fokategoria/alkategoria/altipus effektiven orokolt tulajdonsagai kozott.")
    lines.append("- `property_value_not_allowed`: a tulajdonsag letezik, de a termeken szereplo ertek nincs a kategoriafaban felsorolt engedelyezett ertekek kozott.")
    lines.append("- `property_has_no_allowed_values`: a tulajdonsag letezik, de ures erteklistaval, mikozben a termeken van nem ures ertek.")
    lines.append("- A flag tulajdonsagok `{} ` alaku deklaracioi nem szamitanak ures erteklistanak; ezek bool erteket varnak.")
    lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, default=DEFAULT_TREE)
    parser.add_argument("--products", type=Path, default=DEFAULT_PRODUCTS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    tree = load_json(args.tree)
    products = load_json(args.products)
    result = audit(tree, products)
    write_report(args.report, args.tree, args.products, result)
    print(f"report: {args.report}")
    print(f"products: {result['products_count']}")
    print(f"tree_nodes: {result['tree_node_count']}")
    print(f"product_issues: {sum(result['product_issue_counts'].values())}")
    print(f"affected_products: {len({i['index'] for i in result['product_issues']})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

