from __future__ import annotations

import json
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
CATEGORY_PATH = BASE_DIR / "kategoriak_2026-06-13.json"
PRODUCT_PATH = BASE_DIR / "eredmeny.json"
OUT_DIR = BASE_DIR / "tejtermekek_munkafajlok"
TARGET_CATEGORY_FOLDED = "tejtermekek es tojas"


def fold_text(value: Any) -> str:
    text = "" if value is None else str(value)
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
        .casefold()
        .strip()
    )


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def folded_get(mapping: dict[str, Any], folded_key: str, default: Any = None) -> Any:
    for key, value in mapping.items():
        if fold_text(key) == folded_key:
            return value
    return default


def find_key_by_fold(mapping: dict[str, Any], folded_key: str) -> str:
    matches = [key for key in mapping if fold_text(key) == folded_key]
    if not matches:
        raise KeyError(f"No key found for folded name: {folded_key}")
    if len(matches) > 1:
        raise KeyError(f"Multiple keys found for folded name {folded_key}: {matches}")
    return matches[0]


def property_names_from_block(block: Any) -> list[str]:
    if not isinstance(block, dict):
        return []

    names: list[str] = []
    for group_value in block.values():
        if isinstance(group_value, dict):
            names.extend(str(name) for name in group_value)
    return sorted(set(names), key=fold_text)


def property_details_from_block(block: Any) -> list[dict[str, Any]]:
    if not isinstance(block, dict):
        return []

    details: list[dict[str, Any]] = []
    for group_name, group_value in block.items():
        if not isinstance(group_value, dict):
            continue

        for prop_name, raw_values in group_value.items():
            if isinstance(raw_values, list):
                values = raw_values
                value_count = len(raw_values)
                kind = "values"
            elif isinstance(raw_values, dict):
                values = []
                value_count = 0
                kind = "flag" if not raw_values else "object"
            else:
                values = raw_values
                value_count = 1 if raw_values not in (None, "") else 0
                kind = type(raw_values).__name__

            details.append(
                {
                    "csoport": group_name,
                    "tulajdonsag": prop_name,
                    "tipus": kind,
                    "ertek_db": value_count,
                    "ertekek": values,
                }
            )

    return sorted(details, key=lambda item: (fold_text(item["csoport"]), fold_text(item["tulajdonsag"])))


def category_paths(category_node: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    root_props = folded_get(category_node, "tulajdonsagok", {}) or {}
    rows.append(
        {
            "szint": "fokategoria",
            "alkategoria": "",
            "altipus": "",
            "tulajdonsagok": property_details_from_block(root_props),
        }
    )

    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    for alkategoria, alk_node in alkategoriak.items():
        alk_props = folded_get(alk_node, "tulajdonsagok", {}) or {}
        rows.append(
            {
                "szint": "alkategoria",
                "alkategoria": alkategoria,
                "altipus": "",
                "tulajdonsagok": property_details_from_block(alk_props),
            }
        )

        altipusok = folded_get(alk_node, "altipusok", {}) or {}
        for altipus, alt_node in altipusok.items():
            alt_props = folded_get(alt_node, "tulajdonsagok", {}) or {}
            rows.append(
                {
                    "szint": "altipus",
                    "alkategoria": alkategoria,
                    "altipus": altipus,
                    "tulajdonsagok": property_details_from_block(alt_props),
                }
            )

    return rows


def empty_value(value: Any) -> bool:
    return value in (None, "", [], {})


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell).replace("\n", " ") for cell in row) + " |")
    return lines


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")
    date_stamp = generated_at[:10]

    categories = load_json(CATEGORY_PATH)
    products = load_json(PRODUCT_PATH)

    category_key = find_key_by_fold(categories, TARGET_CATEGORY_FOLDED)
    category_node = categories[category_key]

    exported_products = []
    for index, product in enumerate(products):
        if fold_text(product.get("fokategoria", "")) == TARGET_CATEGORY_FOLDED:
            exported = {"_forras_index": index}
            exported.update(product)
            exported_products.append(exported)

    paths = category_paths(category_node)
    declared_pairs = {
        (row["alkategoria"], row["altipus"])
        for row in paths
        if row["szint"] in {"alkategoria", "altipus"}
    }

    product_pair_counts = Counter(
        (product.get("alkategoria", ""), product.get("altipus", "")) for product in exported_products
    )
    product_alk_counts = Counter(product.get("alkategoria", "") for product in exported_products)
    product_prop_counts: Counter[str] = Counter()
    empty_product_prop_counts: Counter[str] = Counter()
    product_value_counts: dict[str, Counter[str]] = defaultdict(Counter)

    for product in exported_products:
        props = product.get("tulajdonsagok") or {}
        for prop_name, value in props.items():
            product_prop_counts[prop_name] += 1
            if empty_value(value):
                empty_product_prop_counts[prop_name] += 1
                continue

            values = value if isinstance(value, list) else [value]
            for item in values:
                if not empty_value(item):
                    product_value_counts[prop_name][str(item)] += 1

    missing_pairs = sorted(
        set(product_pair_counts) - declared_pairs,
        key=lambda pair: (fold_text(pair[0]), fold_text(pair[1])),
    )
    unused_pairs = sorted(
        declared_pairs - set(product_pair_counts),
        key=lambda pair: (fold_text(pair[0]), fold_text(pair[1])),
    )

    alk_rows = []
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    for alkategoria, alk_node in sorted(alkategoriak.items(), key=lambda item: fold_text(item[0])):
        altipusok = folded_get(alk_node, "altipusok", {}) or {}
        props = folded_get(alk_node, "tulajdonsagok", {}) or {}
        alk_rows.append(
            {
                "alkategoria": alkategoria,
                "termek_db": product_alk_counts[alkategoria],
                "altipus_db": len(altipusok),
                "ures_altipus_termek_db": product_pair_counts[(alkategoria, "")],
                "tulajdonsagok": property_names_from_block(props),
            }
        )

    alt_rows = []
    for (alkategoria, altipus), count in sorted(
        product_pair_counts.items(), key=lambda item: (-item[1], fold_text(item[0][0]), fold_text(item[0][1]))
    ):
        alt_rows.append(
            {
                "alkategoria": alkategoria,
                "altipus": altipus,
                "termek_db": count,
                "szerepel_a_kategoriafaban": (alkategoria, altipus) in declared_pairs,
            }
        )

    property_rows = []
    for prop_name, count in product_prop_counts.most_common():
        top_values = ", ".join(
            f"{value} ({value_count})"
            for value, value_count in product_value_counts[prop_name].most_common(8)
        )
        property_rows.append(
            {
                "tulajdonsag": prop_name,
                "termek_db": count,
                "ures_db": empty_product_prop_counts[prop_name],
                "gyakori_ertekek": top_values,
            }
        )

    meta = {
        "generated_at": generated_at,
        "category_source": CATEGORY_PATH.name,
        "product_source": PRODUCT_PATH.name,
        "fokategoria": category_key,
        "total_products_in_source": len(products),
        "matching_products": len(exported_products),
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    category_export_path = OUT_DIR / f"tejtermekek_kategoria_{date_stamp}.json"
    products_export_path = OUT_DIR / f"tejtermekek_termekek_{date_stamp}.json"
    structure_export_path = OUT_DIR / f"tejtermekek_struktura_{date_stamp}.json"
    report_path = OUT_DIR / f"tejtermekek_attekintes_{date_stamp}.md"

    dump_json(
        category_export_path,
        {
            "meta": meta,
            "kategoria": {category_key: category_node},
        },
    )
    dump_json(
        products_export_path,
        {
            "meta": meta,
            "termekek": exported_products,
        },
    )
    dump_json(
        structure_export_path,
        {
            "meta": meta,
            "kategoriak": alk_rows,
            "utvonalak": alt_rows,
            "tulajdonsagok_termekek_alapjan": property_rows,
            "kategoriafa_utvonalak": paths,
            "termekekben_hasznalt_de_hianyzo_utvonalak": [
                {"alkategoria": alkategoria, "altipus": altipus, "termek_db": product_pair_counts[(alkategoria, altipus)]}
                for alkategoria, altipus in missing_pairs
            ],
            "kategoriafaban_szereplo_de_nem_hasznalt_utvonalak": [
                {"alkategoria": alkategoria, "altipus": altipus}
                for alkategoria, altipus in unused_pairs
            ],
        },
    )

    lines: list[str] = [
        f"# {category_key} munkakivonat",
        "",
        "## Fajlok",
        f"- Kategoriafa: `{category_export_path.name}`",
        f"- Termekek: `{products_export_path.name}`",
        f"- Struktura es szamolt adatok: `{structure_export_path.name}`",
        "",
        "## Osszesites",
        f"- Generalva: {generated_at}",
        f"- Forras kategoriafa: `{CATEGORY_PATH.name}`",
        f"- Forras termeklista: `{PRODUCT_PATH.name}`",
        f"- Fokategoria: {category_key}",
        f"- Alkategoriak szama: {len(alkategoriak)}",
        f"- Kategoriafaban szereplo alkategoria/altipus utak: {len(declared_pairs)}",
        f"- Termekek szama: {len(exported_products)}",
        f"- Termekekben hasznalt alkategoria/altipus utak: {len(product_pair_counts)}",
        f"- Ures altipusu termekek: {sum(count for (alkategoria, altipus), count in product_pair_counts.items() if not altipus)}",
        f"- Termekekben hasznalt, de kategoriafaban nem szereplo utak: {len(missing_pairs)}",
        f"- Kategoriafaban szereplo, de termeknel nem hasznalt utak: {len(unused_pairs)}",
        "",
        "## Alkategoriak",
    ]

    lines.extend(
        markdown_table(
            ["Alkategoria", "Termek", "Altipus", "Ures altipus", "Tulajdonsagok"],
            [
                [
                    row["alkategoria"],
                    row["termek_db"],
                    row["altipus_db"],
                    row["ures_altipus_termek_db"],
                    ", ".join(row["tulajdonsagok"][:12]) + (" ..." if len(row["tulajdonsagok"]) > 12 else ""),
                ]
                for row in alk_rows
            ],
        )
    )

    lines.extend(["", "## Termekutak termekszam szerint"])
    lines.extend(
        markdown_table(
            ["Alkategoria", "Altipus", "Termek", "Kategoriafaban"],
            [
                [
                    row["alkategoria"],
                    row["altipus"] or "(ures)",
                    row["termek_db"],
                    "igen" if row["szerepel_a_kategoriafaban"] else "nem",
                ]
                for row in alt_rows
            ],
        )
    )

    if missing_pairs:
        lines.extend(["", "## Termekekben hasznalt, de a kategoriafaban nem szereplo utak"])
        lines.extend(
            markdown_table(
                ["Alkategoria", "Altipus", "Termek"],
                [
                    [alkategoria, altipus or "(ures)", product_pair_counts[(alkategoria, altipus)]]
                    for alkategoria, altipus in missing_pairs
                ],
            )
        )

    if unused_pairs:
        lines.extend(["", "## Kategoriafaban szereplo, de termeknel nem hasznalt utak"])
        lines.extend(
            markdown_table(
                ["Alkategoria", "Altipus"],
                [[alkategoria, altipus or "(ures)"] for alkategoria, altipus in unused_pairs],
            )
        )

    lines.extend(["", "## Termektulajdonsagok gyakorisaga"])
    lines.extend(
        markdown_table(
            ["Tulajdonsag", "Termek", "Ures", "Gyakori ertekek"],
            [
                [
                    row["tulajdonsag"],
                    row["termek_db"],
                    row["ures_db"],
                    row["gyakori_ertekek"],
                ]
                for row in property_rows
            ],
        )
    )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"category={category_key}")
    print(f"products={len(exported_products)}")
    print(f"alkategoriak={len(alkategoriak)}")
    print(f"declared_paths={len(declared_pairs)}")
    print(f"used_paths={len(product_pair_counts)}")
    print(f"missing_paths={len(missing_pairs)}")
    print(f"unused_paths={len(unused_pairs)}")
    print(f"out_dir={OUT_DIR}")


if __name__ == "__main__":
    main()
