#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit the Baba main category without modifying source JSON files."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE = Path(__file__).resolve().parent
TREE_PATH = BASE / "kategoriak_2026-06-13.json"
PRODUCTS_PATH = BASE / "eredmeny.json"
REPORT_PATH = BASE / "baba_kategoria_audit_2026-06-23.md"

ALK = "alkategóriák"
ALT = "altípusok"
PROP = "tulajdonságok"
EGY = "egyedi"
CSOP = "csoportos"
LEVEL_FIELDS = ("fokategoria", "alkategoria", "altipus")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def flatten(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]


def dedupe(values: list[Any]) -> list[Any]:
    out: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value in ("", None):
            continue
        key = value_key(value)
        if key not in seen:
            seen.add(key)
            out.append(value)
    return out


def value_key(value: Any) -> str:
    if isinstance(value, bool):
        return "bool:" + str(value).lower()
    text = str(value).strip().lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def name_key(value: Any) -> str:
    text = str(value).replace("\u00a0", " ").lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-z0-9+%]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def prop_group(node: dict[str, Any], group: str) -> dict[str, Any]:
    props = node.get(PROP, {})
    if not isinstance(props, dict):
        return {}
    values = props.get(group, {})
    return values if isinstance(values, dict) else {}


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


def category_exists(tree: dict[str, Any], path: tuple[str, str, str]) -> bool:
    return get_node(tree, path) is not None


def effective_defs(tree: dict[str, Any], path: tuple[str, str, str]) -> dict[str, tuple[str, str, list[Any]]]:
    out: dict[str, tuple[str, str, list[Any]]] = {}
    for level in range(1, len(path) + 1):
        node = get_node(tree, path[:level])
        if isinstance(node, dict):
            out.update(direct_defs(node))
    return out


def walk_baba(tree: dict[str, Any]) -> list[tuple[tuple[str, ...], dict[str, Any]]]:
    rows: list[tuple[tuple[str, ...], dict[str, Any]]] = []
    baba = tree.get("Baba", {})
    if not isinstance(baba, dict):
        return rows
    rows.append((("Baba",), baba))
    for ak, anode in baba.get(ALK, {}).items():
        rows.append((("Baba", ak), anode))
        for at, tnode in anode.get(ALT, {}).items():
            rows.append((("Baba", ak, at), tnode))
    return rows


def product_name(product: dict[str, Any]) -> str:
    termek = product.get("termek", {})
    return termek.get("product_name", "") if isinstance(termek, dict) else ""


def path_of(product: dict[str, Any]) -> tuple[str, str, str]:
    return tuple(product.get(field, "") or "" for field in LEVEL_FIELDS)  # type: ignore[return-value]


def md_escape(value: Any) -> str:
    text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        rows = [["-", "-"][: len(headers)]]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(item) for item in row) + " |")
    return "\n".join(lines)


def bool_text(value: bool) -> str:
    return "igen" if value else "nem"


def is_packaging_value(value: Any) -> bool:
    return value_key(value) in {
        "uveg",
        "tasak pouch",
        "doboz",
        "pohar",
        "flakon",
        "tubus",
        "egyeb",
    }


def is_amount_value(value: Any) -> bool:
    return bool(re.search(r"\d", str(value))) and bool(re.search(r"\b(g|kg|ml|l|db)\b", str(value).lower()))


def main() -> int:
    tree = load_json(TREE_PATH)
    products = load_json(PRODUCTS_PATH)
    baba = tree.get("Baba", {})
    if not isinstance(baba, dict):
        raise SystemExit("Nincs Baba főkategória.")

    baba_products = [(idx, product) for idx, product in enumerate(products) if product.get("fokategoria") == "Baba"]
    category_counts = Counter((p.get("alkategoria") or "", p.get("altipus") or "") for _, p in baba_products)

    alt_rows: list[list[Any]] = []
    empty_alt_categories: list[tuple[str, str, str]] = []
    for ak, anode in baba.get(ALK, {}).items():
        for at in anode.get(ALT, {}):
            count = category_counts[(ak, at)]
            alt_rows.append([f"Baba > {ak} > {at}", count])
            if count == 0:
                empty_alt_categories.append(("Baba", ak, at))
    alt_rows.sort(key=lambda row: (-int(row[1]), str(row[0])))

    missing_paths: list[tuple[int, tuple[str, str, str], str]] = []
    missing_props: list[tuple[int, tuple[str, str, str], str, Any, str]] = []
    missing_values: list[tuple[int, tuple[str, str, str], str, Any, str]] = []
    cardinality_issues: list[tuple[int, tuple[str, str, str], str, str, Any, str]] = []
    used_props_by_path: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    used_values_by_path_prop: dict[tuple[tuple[str, str, str], str], set[str]] = defaultdict(set)
    packaging_amount_mix: Counter[str] = Counter()

    for idx, product in baba_products:
        path = path_of(product)
        name = product_name(product)
        if not category_exists(tree, path):
            missing_paths.append((idx, path, name))
            continue
        defs = effective_defs(tree, path)
        for prop, value in (product.get("tulajdonsagok") or {}).items():
            used_props_by_path[path].add(prop)
            for item in flatten(value):
                used_values_by_path_prop[(path, prop)].add(value_key(item))
                if prop == "kiszerelés":
                    if is_packaging_value(item):
                        packaging_amount_mix["packaging"] += 1
                    elif is_amount_value(item):
                        packaging_amount_mix["amount"] += 1
                    else:
                        packaging_amount_mix["other"] += 1

            pdef = defs.get(prop)
            if not pdef:
                missing_props.append((idx, path, prop, value, name))
                continue

            group, kind, values = pdef
            if kind == "flag":
                if not isinstance(value, bool):
                    cardinality_issues.append((idx, path, prop, "logikai mező nem bool", value, name))
                continue

            if group == EGY and isinstance(value, list) and len(value) > 1:
                cardinality_issues.append((idx, path, prop, "egyedi mezőben több érték", value, name))
            if group == CSOP and not isinstance(value, list):
                cardinality_issues.append((idx, path, prop, "csoportos mező skalár értékkel", value, name))

            if values:
                allowed = {value_key(v) for v in values}
                for item in flatten(value):
                    if item in ("", None):
                        continue
                    if value_key(item) not in allowed:
                        missing_values.append((idx, path, prop, item, name))

    direct_duplicate_props: list[tuple[tuple[str, ...], str]] = []
    unused_direct_props: list[tuple[tuple[str, ...], str]] = []
    for path, node in walk_baba(tree):
        direct_duplicate_props.extend((path, prop) for prop in set(prop_group(node, EGY)) & set(prop_group(node, CSOP)))
        if len(path) == 2:
            product_paths = [path_of(p) for _, p in baba_products if p.get("alkategoria") == path[1]]
        elif len(path) == 3:
            product_paths = [path_of(p) for _, p in baba_products if (p.get("alkategoria"), p.get("altipus")) == (path[1], path[2])]
        else:
            product_paths = [path_of(p) for _, p in baba_products]
        used = set().union(*(used_props_by_path[p] for p in product_paths)) if product_paths else set()
        for prop in direct_defs(node):
            if prop not in used:
                unused_direct_props.append((path, prop))

    missing_by_prop = Counter(prop for _, _, prop, _, _ in missing_values)
    missing_by_path_prop = Counter((path, prop) for _, path, prop, _, _ in missing_values)
    missing_unique_by_prop: dict[str, Counter[str]] = defaultdict(Counter)
    for _, _, prop, value, _ in missing_values:
        missing_unique_by_prop[prop][str(value)] += 1

    by_exact_name: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    by_norm_name: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for idx, product in baba_products:
        name = product_name(product)
        by_exact_name[name].append((idx, product))
        by_norm_name[name_key(name)].append((idx, product))
    exact_dups = {name: rows for name, rows in by_exact_name.items() if name and len(rows) > 1}
    norm_dups = {key: rows for key, rows in by_norm_name.items() if key and len(rows) > 1}
    cross_category_dup_groups = [
        (name, rows)
        for name, rows in exact_dups.items()
        if len({(p.get("alkategoria"), p.get("altipus")) for _, p in rows}) > 1
    ]

    non_food_products = [
        (idx, product)
        for idx, product in baba_products
        if product.get("alkategoria") == "Babaápolási eszköz"
        or (product.get("alkategoria"), product.get("altipus")) == ("Egyéb babaélelmiszer", "Pelenkázó alátét")
    ]
    baby_care_products = [product for _, product in non_food_products if product.get("alkategoria") == "Babaápolási eszköz"]
    misplaced_non_food = [product for _, product in non_food_products if product.get("alkategoria") != "Babaápolási eszköz"]

    age_values = Counter()
    for _, product in baba_products:
        value = (product.get("tulajdonsagok") or {}).get("életkor")
        if value is None:
            continue
        for item in flatten(value):
            age_values[str(item)] += 1

    special_prop_usage = Counter()
    for _, product in baba_products:
        for prop in (product.get("tulajdonsagok") or {}):
            if prop in {"hús", "hús / fehérje", "fő alapanyag", "alapanyag", "gabona", "összetevő", "jellemző", "jellemzők", "korosztály", "életkor", "kiszerelés"}:
                special_prop_usage[prop] += 1

    findings = [
        [
            "Duplikált Baba-terméknevek",
            len(exact_dups),
            f"{sum(len(rows) for rows in exact_dups.values())} terméksor érintett; {len(cross_category_dup_groups)} névcsoport több kategória/altípus között is szóródik.",
            "Dedublikáció vagy egy forrásonkénti merge szabály kell, mert eltérő tulajdonságsémák is vannak ugyanarra a terméknévre.",
        ],
        [
            "Nem élelmiszer jellegű Baba-termékek",
            len(non_food_products),
            f"{len(baby_care_products)} Babaápolási eszköz; rossz élelmiszer-ágon maradt: {len(misplaced_non_food)}.",
            "Ha a Baba főkategória vegyes baba-termék kategória marad, ez így konzisztens. Ha csak élelmiszer legyen, ezt az egész ágat külön főkategóriába kellene vinni.",
        ],
        [
            "Hiányzó értéklistás deklarációk",
            len(missing_values),
            ", ".join(f"{prop}: {count}" for prop, count in missing_by_prop.most_common()),
            "A használt értékeket fel kell venni, vagy lazítani kell az adott tulajdonság értéklistáját.",
        ],
        [
            "Kiszerelés jelentése keveredik",
            sum(packaging_amount_mix.values()),
            f"csomagolástípus: {packaging_amount_mix['packaging']}, mennyiség: {packaging_amount_mix['amount']}, egyéb: {packaging_amount_mix['other']}",
            "Érdemes szétválasztani `csomagolás` és `kiszerelés`/`nettó mennyiség` mezőkre.",
        ],
        [
            "Nem használt közvetlen tulajdonságdefiníciók",
            len(unused_direct_props),
            "Főleg régi `korosztály`, `jellemzők`, `alapanyag` maradványok.",
            "A régi kulcsokat össze kell vezetni az aktuális `életkor`, `jellemző`, `gabona` kulcsokkal, majd törölni a maradék deklarációkat.",
        ],
        [
            "Üres altípusok",
            len(empty_alt_categories),
            "; ".join(" > ".join(path) for path in empty_alt_categories),
            "Ha nincs tervezett termékfeltöltés, törölhető.",
        ],
        [
            "Közvetlen duplikált tulajdonságdefiníció",
            len(direct_duplicate_props),
            "; ".join(f"{' > '.join(path)} :: {prop}" for path, prop in direct_duplicate_props),
            "Egy mező csak `egyedi` vagy `csoportos` legyen ugyanazon a szinten.",
        ],
        [
            "Életkor értékformátum szóródik",
            len(age_values),
            f"{len(age_values)} különböző életkorérték.",
            "Egységes formátum javasolt, például `4 hó+`, `6 hó+`, `12 hó+`, `1-3 év`.",
        ],
    ]

    lines: list[str] = []
    lines.append("# Baba főkategória audit")
    lines.append("")
    lines.append(f"Dátum: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("Források:")
    lines.append(f"- `{TREE_PATH.as_posix()}`")
    lines.append(f"- `{PRODUCTS_PATH.as_posix()}`")
    lines.append("")
    lines.append("## Összefoglaló")
    lines.append("")
    lines.append(
        table(
            ["Mérés", "Darab"],
            [
                ["Baba termék", len(baba_products)],
                ["Baba alkategória", len(baba.get(ALK, {}))],
                ["Baba altípus", sum(len(anode.get(ALT, {})) for anode in baba.get(ALK, {}).values())],
                ["Termékkel használt kategóriaút", len(category_counts)],
                ["Üres altípus", len(empty_alt_categories)],
                ["Hiányzó kategóriaút", len(missing_paths)],
                ["Hiányzó tulajdonságdefiníció", len(missing_props)],
                ["Hiányzó értéklistás deklaráció", len(missing_values)],
                ["Kardinalitási gond", len(cardinality_issues)],
                ["Nem használt közvetlen tulajdonságdefiníció", len(unused_direct_props)],
                ["Pontos duplikált terméknévcsoport", len(exact_dups)],
                ["Pontos duplikált terméksor", sum(len(rows) for rows in exact_dups.values())],
            ],
        )
    )
    lines.append("")
    lines.append("## Javítási jelöltek")
    lines.append("")
    lines.append(table(["Téma", "Darab", "Megjegyzés", "Javaslat"], findings))
    lines.append("")
    lines.append("## Kategóriaeloszlás")
    lines.append("")
    lines.append(table(["Kategóriaút", "Termék"], alt_rows))
    lines.append("")
    lines.append("## Hiányzó értéklistás deklarációk")
    lines.append("")
    lines.append("### Tulajdonság szerint")
    lines.append("")
    lines.append(table(["Tulajdonság", "Darab"], [[prop, count] for prop, count in missing_by_prop.most_common()]))
    lines.append("")
    lines.append("### Kategóriaút és tulajdonság szerint")
    lines.append("")
    lines.append(
        table(
            ["Kategóriaút", "Tulajdonság", "Darab"],
            [[" > ".join(path), prop, count] for (path, prop), count in missing_by_path_prop.most_common()],
        )
    )
    lines.append("")
    lines.append("### Konkrét hiányzó értékek")
    lines.append("")
    lines.append(
        table(
            ["Tulajdonság", "Érték", "Darab"],
            [[prop, value, count] for prop, values in sorted(missing_unique_by_prop.items()) for value, count in values.most_common()],
        )
    )
    lines.append("")
    lines.append("## Kardinalitási gondok")
    lines.append("")
    lines.append(
        table(
            ["Index", "Kategóriaút", "Tulajdonság", "Gond", "Érték", "Termék"],
            [[idx, " > ".join(path), prop, issue, value, name] for idx, path, prop, issue, value, name in cardinality_issues],
        )
    )
    lines.append("")
    lines.append("## Nem használt közvetlen tulajdonságdefiníciók")
    lines.append("")
    lines.append(table(["Kategóriaút", "Tulajdonság"], [[" > ".join(path), prop] for path, prop in unused_direct_props]))
    lines.append("")
    lines.append("## Speciális tulajdonságkulcsok használata")
    lines.append("")
    lines.append(table(["Tulajdonság", "Termékdarab"], [[prop, count] for prop, count in special_prop_usage.most_common()]))
    lines.append("")
    lines.append("## Életkor értékek")
    lines.append("")
    lines.append(table(["Érték", "Darab"], [[value, count] for value, count in age_values.most_common()]))
    lines.append("")
    lines.append("## Nem élelmiszer jellegű Baba-termékek")
    lines.append("")
    lines.append(
        table(
            ["Index", "Kategóriaút", "Termék"],
            [
                [idx, " > ".join(path_of(product)), product_name(product)]
                for idx, product in non_food_products
            ],
        )
    )
    lines.append("")
    lines.append("## Duplikált terméknevek")
    lines.append("")
    lines.append("### Több kategória/altípus között is szóródó pontos egyezések")
    lines.append("")
    cross_rows: list[list[Any]] = []
    for name, rows in cross_category_dup_groups:
        indices = ", ".join(str(idx) for idx, _ in rows)
        paths = "; ".join(sorted({" > ".join(path_of(product)) for _, product in rows}))
        cross_rows.append([len(rows), indices, name, paths])
    cross_rows.sort(key=lambda row: (-int(row[0]), str(row[2])))
    lines.append(table(["Darab", "Indexek", "Termék", "Kategóriautak"], cross_rows))
    lines.append("")
    lines.append("### Összes pontos duplikált terméknévcsoport")
    lines.append("")
    all_dup_rows: list[list[Any]] = []
    for name, rows in exact_dups.items():
        indices = ", ".join(str(idx) for idx, _ in rows)
        paths = "; ".join(sorted({" > ".join(path_of(product)) for _, product in rows}))
        all_dup_rows.append([len(rows), indices, name, paths])
    all_dup_rows.sort(key=lambda row: (-int(row[0]), str(row[2])))
    lines.append(table(["Darab", "Indexek", "Termék", "Kategóriautak"], all_dup_rows))
    lines.append("")
    lines.append("## Kategória-összevonási jelöltek")
    lines.append("")
    lines.append(
        table(
            ["Jelölt", "Darab", "Javasolt cél"],
            [
                ["Baba > Gyümölcspüré, bébidesszert > Gyümölcs-gabona püré", category_counts[("Gyümölcspüré, bébidesszert", "Gyümölcs-gabona püré")], "Baba > Gyümölcspüré, bébidesszert > Gyümölcs-gabona készítmény"],
                ["Baba > Gyümölcspüré, bébidesszert > Gyümölcspüré gabonával", category_counts[("Gyümölcspüré, bébidesszert", "Gyümölcspüré gabonával")], "Baba > Gyümölcspüré, bébidesszert > Gyümölcs-gabona készítmény"],
                ["Baba > Bébi snack, keksz > Babapiskóta", category_counts[("Bébi snack, keksz", "Babapiskóta")], "törlés, ha nincs tervezett termék"],
                ["Baba > Egyéb babaélelmiszer > Pelenkázó alátét", category_counts[("Egyéb babaélelmiszer", "Pelenkázó alátét")], "Baba > Babaápolási eszköz > Pelenkázó alátét, ha Baba vegyes baba-termék kategória marad"],
            ],
        )
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Baba audit kész: {REPORT_PATH}")
    print(json.dumps({
        "baba_products": len(baba_products),
        "empty_alt_categories": len(empty_alt_categories),
        "missing_paths": len(missing_paths),
        "missing_props": len(missing_props),
        "missing_values": len(missing_values),
        "cardinality_issues": len(cardinality_issues),
        "unused_direct_props": len(unused_direct_props),
        "exact_duplicate_name_groups": len(exact_dups),
        "exact_duplicate_product_rows": sum(len(rows) for rows in exact_dups.values()),
        "non_food_products": len(non_food_products),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
