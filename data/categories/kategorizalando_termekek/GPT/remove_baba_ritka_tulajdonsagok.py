#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove rarely used properties from the Baba category and Baba products."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
TREE_PATH = BASE / "kategoriak_2026-06-13.json"
PRODUCTS_PATH = BASE / "eredmeny.json"
REPORT_PATH = BASE / "baba_ritka_tulajdonsagok_torlese_2026-06-23.md"

PROP = "tulajdonságok"
ALK = "alkategóriák"
ALT = "altípusok"
EGY = "egyedi"
CSOP = "csoportos"

RARE_PROPS = {
    "alapanyag",
    "funkció",
    "szín",
    "alap",
    "por",
    "méret",
    "tartozék",
    "termékváltozat",
    "forma",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_atomic(path: Path, data: Any) -> None:
    fd, tmp_name = tempfile.mkstemp(prefix=".remove_baba_rare_", suffix=".json", dir=str(path.parent))
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        tmp.replace(path)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise


def category_hash(product: dict[str, Any]) -> str:
    props = product.get("tulajdonsagok") or {}
    key = (
        f"{product.get('fokategoria', '')}|{product.get('alkategoria', '')}|"
        f"{product.get('altipus', '')}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}"
    )
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def product_name(product: dict[str, Any]) -> str:
    termek = product.get("termek", {})
    return termek.get("product_name", "") if isinstance(termek, dict) else ""


def walk_baba_nodes(tree: dict[str, Any]) -> list[tuple[tuple[str, ...], dict[str, Any]]]:
    baba = tree.get("Baba")
    if not isinstance(baba, dict):
        return []

    rows: list[tuple[tuple[str, ...], dict[str, Any]]] = [(("Baba",), baba)]
    for ak, anode in baba.get(ALK, {}).items():
        if not isinstance(anode, dict):
            continue
        rows.append((("Baba", ak), anode))
        for at, tnode in anode.get(ALT, {}).items():
            if isinstance(tnode, dict):
                rows.append((("Baba", ak, at), tnode))
    return rows


def prop_group(node: dict[str, Any], group: str) -> dict[str, Any]:
    props = node.get(PROP, {})
    if not isinstance(props, dict):
        return {}
    values = props.get(group, {})
    return values if isinstance(values, dict) else {}


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        rows = [["-", "-"][: len(headers)]]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(item) for item in row) + " |")
    return "\n".join(lines)


def validate_absent(tree: dict[str, Any], products: list[dict[str, Any]]) -> dict[str, Any]:
    category_hits: list[list[Any]] = []
    for path, node in walk_baba_nodes(tree):
        for group in (EGY, CSOP):
            props = prop_group(node, group)
            for key in sorted(RARE_PROPS & set(props)):
                category_hits.append([" > ".join(path), group, key])

    product_hits: list[list[Any]] = []
    for idx, product in enumerate(products):
        if product.get("fokategoria") != "Baba":
            continue
        props = product.get("tulajdonsagok") or {}
        for key in sorted(RARE_PROPS & set(props)):
            product_hits.append([idx, key, product_name(product)])

    return {
        "category_hits": category_hits,
        "product_hits": product_hits,
    }


def main() -> int:
    tree = load_json(TREE_PATH)
    products = load_json(PRODUCTS_PATH)

    category_removed = Counter()
    product_removed = Counter()
    category_rows: list[list[Any]] = []
    product_rows: list[list[Any]] = []
    changed_indices: set[int] = set()

    for path, node in walk_baba_nodes(tree):
        for group in (EGY, CSOP):
            props = prop_group(node, group)
            for key in sorted(RARE_PROPS & set(props)):
                old_value = props.pop(key)
                category_removed[key] += 1
                category_rows.append([" > ".join(path), group, key, old_value])

    for idx, product in enumerate(products):
        if product.get("fokategoria") != "Baba":
            continue
        props = product.get("tulajdonsagok")
        if not isinstance(props, dict):
            continue
        removed_here: list[str] = []
        for key in sorted(RARE_PROPS & set(props)):
            old_value = props.pop(key)
            product_removed[key] += 1
            removed_here.append(key)
            product_rows.append(
                [
                    idx,
                    product.get("alkategoria", ""),
                    product.get("altipus", ""),
                    product_name(product),
                    key,
                    old_value,
                ]
            )
        if removed_here:
            product["kategoria_hash"] = category_hash(product)
            changed_indices.add(idx)

    validation = validate_absent(tree, products)

    lines = [
        "# Baba ritka tulajdonságok törlése",
        "",
        f"Dátum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "Törölt tulajdonságkulcsok:",
        "",
        ", ".join(sorted(RARE_PROPS)),
        "",
        "## Összefoglaló",
        "",
        table(
            ["Mérés", "Darab"],
            [
                ["Kategóriafából törölt definíció", sum(category_removed.values())],
                ["Termékekből törölt tulajdonság", sum(product_removed.values())],
                ["Érintett Baba-termék", len(changed_indices)],
                ["Maradt kategóriadefiníció a tiltott kulcsokra", len(validation["category_hits"])],
                ["Maradt terméktulajdonság a tiltott kulcsokra", len(validation["product_hits"])],
            ],
        ),
        "",
        "## Törlés tulajdonság szerint",
        "",
        table(
            ["Tulajdonság", "Kategóriadefiníció", "Termék"],
            [[key, category_removed[key], product_removed[key]] for key in sorted(RARE_PROPS)],
        ),
        "",
        "## Kategóriafából törölt definíciók",
        "",
        table(["Kategóriaút", "Csoport", "Tulajdonság", "Régi érték"], category_rows),
        "",
        "## Termékekből törölt tulajdonságok",
        "",
        table(["Index", "Alkategória", "Altípus", "Termék", "Tulajdonság", "Régi érték"], product_rows),
    ]

    if validation["category_hits"] or validation["product_hits"]:
        lines.extend(
            [
                "",
                "## Validációs maradványok",
                "",
                table(["Kategóriaút", "Csoport", "Tulajdonság"], validation["category_hits"]),
                "",
                table(["Index", "Tulajdonság", "Termék"], validation["product_hits"]),
            ]
        )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if validation["category_hits"] or validation["product_hits"]:
        print("Validációs hiba, JSON mentés nélkül. Riport:", REPORT_PATH)
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        return 1

    save_json_atomic(TREE_PATH, tree)
    save_json_atomic(PRODUCTS_PATH, products)

    print("Baba ritka tulajdonságok törölve:", REPORT_PATH)
    print(
        json.dumps(
            {
                "category_definitions_removed": sum(category_removed.values()),
                "product_properties_removed": sum(product_removed.values()),
                "changed_products": len(changed_indices),
                "by_property": {
                    key: {
                        "category_definitions": category_removed[key],
                        "products": product_removed[key],
                    }
                    for key in sorted(RARE_PROPS)
                },
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
