from __future__ import annotations

import json
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
WORK_DIR = BASE_DIR / "tejtermekek_munkafajlok"

MAIN_PRODUCTS = BASE_DIR / "eredmeny.json"
MAIN_CATEGORIES = BASE_DIR / "kategoriak_2026-06-13.json"

SOURCE_PRODUCTS = WORK_DIR / "tejtermekek_logikai_tisztitott_termekek_2026-06-24.json"
SOURCE_CATEGORIES = WORK_DIR / "tejtermekek_logikai_tisztitott_kategoria_2026-06-24.json"

REPORT_OUT = WORK_DIR / "tejtermekek_logikai_tisztitott_fo_fajl_integracio_2026-06-25.md"

ROOT_NAME = "Tejtermékek és tojás"


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
    tmp_path = path.with_name(path.name + ".tmp")
    with tmp_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with tmp_path.open("r", encoding="utf-8") as handle:
        json.load(handle)
    tmp_path.replace(path)


def values_of(value: Any) -> list[Any]:
    if value is None or value == "" or value == [] or value == {}:
        return []
    if isinstance(value, list):
        return value
    return [value]


def product_identity(product: dict[str, Any]) -> tuple[Any, Any, Any]:
    termek = product.get("termek") or {}
    return (
        termek.get("store_name"),
        termek.get("store_product_id"),
        termek.get("product_name"),
    )


def folded_get(mapping: dict[str, Any], folded_name: str, default: Any = None) -> Any:
    target = fold_text(folded_name)
    for key, value in mapping.items():
        if fold_text(key) == target:
            return value
    return default


def collect_declared_paths(category_node: dict[str, Any]) -> set[tuple[str, str]]:
    paths: set[tuple[str, str]] = set()
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    for alkategoria, alk_node in alkategoriak.items():
        altipusok = folded_get(alk_node, "altipusok", {}) or {}
        for altipus in altipusok:
            paths.add((alkategoria, altipus))
    return paths


def collect_declared_props(category_node: dict[str, Any]) -> set[str]:
    props: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            prop_block = folded_get(node, "tulajdonsagok")
            if isinstance(prop_block, dict):
                for group in prop_block.values():
                    if isinstance(group, dict):
                        props.update(group)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(category_node)
    return props


def validate_tejtermekek(main_products: list[dict[str, Any]], category_node: dict[str, Any]) -> dict[str, Any]:
    products = [product for product in main_products if product.get("fokategoria") == ROOT_NAME]
    declared_paths = collect_declared_paths(category_node)
    product_paths = Counter((product.get("alkategoria", ""), product.get("altipus", "")) for product in products)
    product_props: set[str] = set()
    forbidden_props = Counter()
    forbidden_folded = {
        "jelleg",
        "termekcsalad",
        "termektipus",
        "toltott",
        "uht",
        "zsirtartalom_jelleg",
    }

    for product in products:
        for prop_name in product.get("tulajdonsagok", {}):
            product_props.add(prop_name)
            if fold_text(prop_name) in forbidden_folded:
                forbidden_props[prop_name] += 1

    declared_props = collect_declared_props(category_node)
    return {
        "products": len(products),
        "declared_paths": len(declared_paths),
        "used_paths": len(product_paths),
        "missing_paths": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in product_paths.items()
            if (alk, alt) not in declared_paths
        ],
        "empty_altipus_products": sum(count for (_alk, alt), count in product_paths.items() if not alt),
        "product_only_props": sorted(product_props - declared_props, key=fold_text),
        "category_only_props": sorted(declared_props - product_props, key=fold_text),
        "forbidden_props_left": dict(forbidden_props),
        "path_counts": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in product_paths.most_common()
        ],
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")

    main_products = load_json(MAIN_PRODUCTS)
    main_categories = load_json(MAIN_CATEGORIES)
    source_products_payload = load_json(SOURCE_PRODUCTS)
    source_categories_payload = load_json(SOURCE_CATEGORIES)

    if not isinstance(main_products, list):
        raise RuntimeError(f"{MAIN_PRODUCTS} expected to be a list")
    if ROOT_NAME not in main_categories:
        raise RuntimeError(f"{ROOT_NAME!r} not found in {MAIN_CATEGORIES}")
    if set(source_categories_payload.get("kategoria", {})) != {ROOT_NAME}:
        raise RuntimeError(f"Source category file must contain only {ROOT_NAME!r}")

    source_products = source_products_payload["termekek"]
    source_category_node = source_categories_payload["kategoria"][ROOT_NAME]

    seen_indexes: set[int] = set()
    identity_mismatches: list[dict[str, Any]] = []
    bad_indexes: list[Any] = []
    replacement_indexes: list[int] = []

    for product in source_products:
        index = product.get("_forras_index")
        if not isinstance(index, int) or index < 0 or index >= len(main_products):
            bad_indexes.append(index)
            continue
        if index in seen_indexes:
            raise RuntimeError(f"Duplicate _forras_index in source products: {index}")
        seen_indexes.add(index)
        replacement_indexes.append(index)

        main_identity = product_identity(main_products[index])
        source_identity = product_identity(product)
        if main_identity != source_identity:
            identity_mismatches.append(
                {
                    "index": index,
                    "main": main_identity,
                    "source": source_identity,
                }
            )

    if bad_indexes:
        raise RuntimeError(f"Invalid _forras_index values: {bad_indexes[:20]}")
    if identity_mismatches:
        raise RuntimeError(f"Product identity mismatch at source indexes: {identity_mismatches[:5]}")

    before_tej_count = sum(1 for product in main_products if product.get("fokategoria") == ROOT_NAME)
    before_category_roots = list(main_categories)

    for product in source_products:
        index = product["_forras_index"]
        replacement = {key: value for key, value in product.items() if key != "_forras_index"}
        main_products[index] = replacement

    main_categories[ROOT_NAME] = source_category_node

    validation = validate_tejtermekek(main_products, main_categories[ROOT_NAME])
    if validation["products"] != len(source_products):
        raise RuntimeError(f"Unexpected tejtermek product count after merge: {validation['products']}")
    if validation["missing_paths"]:
        raise RuntimeError(f"Missing category paths after merge: {validation['missing_paths'][:10]}")
    if validation["empty_altipus_products"]:
        raise RuntimeError(f"Empty altipus products after merge: {validation['empty_altipus_products']}")
    if validation["product_only_props"]:
        raise RuntimeError(f"Product-only props after merge: {validation['product_only_props'][:20]}")
    if validation["category_only_props"]:
        raise RuntimeError(f"Category-only props after merge: {validation['category_only_props'][:20]}")
    if validation["forbidden_props_left"]:
        raise RuntimeError(f"Forbidden props left after merge: {validation['forbidden_props_left']}")

    dump_json(MAIN_PRODUCTS, main_products)
    dump_json(MAIN_CATEGORIES, main_categories)

    lines = [
        "# Tejtermékek logikai tisztítás átemelése fő fájlokba",
        "",
        f"- Generálva: {generated_at}",
        f"- Termék forrás: `{SOURCE_PRODUCTS.name}`",
        f"- Kategória forrás: `{SOURCE_CATEGORIES.name}`",
        f"- Módosított fő termékfájl: `{MAIN_PRODUCTS.name}`",
        f"- Módosított fő kategóriafájl: `{MAIN_CATEGORIES.name}`",
        "",
        "## Összesítés",
        f"- Forrás tejtermékes termékek: {len(source_products)}",
        f"- Fő fájlbeli tejtermékes termékek előtte: {before_tej_count}",
        f"- Lecserélt termékrekordok: {len(replacement_indexes)}",
        f"- Kategória gyökerek száma: {len(before_category_roots)}",
        f"- Validált kategóriaútvonalak: {validation['declared_paths']}",
        f"- Használt kategóriaútvonalak: {validation['used_paths']}",
        "",
        "## Validáció",
        f"- Hiányzó kategóriaút: {validation['missing_paths']}",
        f"- Üres altípusú termék: {validation['empty_altipus_products']}",
        f"- Termékben szereplő, de kategóriafából hiányzó tulajdonság: {validation['product_only_props']}",
        f"- Kategóriafában szereplő, de termékben nem használt tulajdonság: {validation['category_only_props']}",
        f"- Tiltott/zajos tulajdonság maradt: {validation['forbidden_props_left']}",
        "",
        "## Tejtermékes útvonalak a fő fájlban",
    ]
    lines.extend(
        markdown_table(
            ["Alkategória", "Altípus", "Termék"],
            [[row["alkategoria"], row["altipus"], row["termek_db"]] for row in validation["path_counts"]],
        )
    )
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"source_products={len(source_products)}")
    print(f"replaced_products={len(replacement_indexes)}")
    print(f"before_tej_count={before_tej_count}")
    print(f"after_tej_count={validation['products']}")
    print(f"declared_paths={validation['declared_paths']}")
    print(f"used_paths={validation['used_paths']}")
    print(f"missing_paths={len(validation['missing_paths'])}")
    print(f"product_only_props={len(validation['product_only_props'])}")
    print(f"category_only_props={len(validation['category_only_props'])}")
    print(f"forbidden_props_left={sum(validation['forbidden_props_left'].values())}")
    print(f"report={REPORT_OUT}")


if __name__ == "__main__":
    main()
