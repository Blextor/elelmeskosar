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


def find_key(mapping: dict[str, Any], folded_key: str) -> str:
    for key in mapping:
        if fold_text(key) == folded_key:
            return key
    raise KeyError(f"Missing key: {folded_key}")


def is_empty(value: Any) -> bool:
    return value in (None, "", [], {})


def values_of(value: Any) -> list[Any]:
    if is_empty(value):
        return []
    return value if isinstance(value, list) else [value]


def property_names(block: Any) -> list[str]:
    if not isinstance(block, dict):
        return []
    names: list[str] = []
    for group in block.values():
        if isinstance(group, dict):
            names.extend(str(name) for name in group)
    return sorted(set(names), key=fold_text)


def path_key(product: dict[str, Any]) -> tuple[str, str]:
    return product.get("alkategoria", ""), product.get("altipus", "")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe_row = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(safe_row) + " |")
    return lines


def collect_category_properties(category_node: dict[str, Any]) -> dict[tuple[str, str, str], list[str]]:
    rows: dict[tuple[str, str, str], list[str]] = {}
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    for alkategoria, alk_node in alkategoriak.items():
        props = folded_get(alk_node, "tulajdonsagok", {}) or {}
        rows[(alkategoria, "", "alkategoria")] = property_names(props)

        altipusok = folded_get(alk_node, "altipusok", {}) or {}
        for altipus, alt_node in altipusok.items():
            props = folded_get(alt_node, "tulajdonsagok", {}) or {}
            rows[(alkategoria, altipus, "altipus")] = property_names(props)
    return rows


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")
    date_stamp = generated_at[:10]
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    categories = load_json(CATEGORY_PATH)
    products = load_json(PRODUCT_PATH)
    category_key = find_key(categories, TARGET_CATEGORY_FOLDED)
    category_node = categories[category_key]
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    milk_products = [
        {"_forras_index": index, **product}
        for index, product in enumerate(products)
        if fold_text(product.get("fokategoria", "")) == TARGET_CATEGORY_FOLDED
    ]

    by_alk = Counter(product.get("alkategoria", "") for product in milk_products)
    by_path = Counter(path_key(product) for product in milk_products)

    prop_counts: Counter[str] = Counter()
    prop_empty_counts: Counter[str] = Counter()
    prop_values: dict[str, Counter[str]] = defaultdict(Counter)
    prop_by_alk: dict[str, Counter[str]] = defaultdict(Counter)
    prop_by_path: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    for product in milk_products:
        props = product.get("tulajdonsagok") or {}
        for prop_name, value in props.items():
            prop_counts[prop_name] += 1
            prop_by_alk[prop_name][product.get("alkategoria", "")] += 1
            prop_by_path[prop_name][path_key(product)] += 1
            if is_empty(value):
                prop_empty_counts[prop_name] += 1
            for item in values_of(value):
                prop_values[prop_name][str(item)] += 1

    category_props = collect_category_properties(category_node)
    category_prop_names = {
        prop_name
        for names in category_props.values()
        for prop_name in names
    }

    product_prop_names = set(prop_counts)
    product_only_props = sorted(product_prop_names - category_prop_names, key=fold_text)
    category_only_props = sorted(category_prop_names - product_prop_names, key=fold_text)
    rare_props = sorted(
        [name for name, count in prop_counts.items() if count <= 5],
        key=lambda name: (prop_counts[name], fold_text(name)),
    )

    duplicate_like_alks = []
    for alkategoria, count in sorted(by_alk.items(), key=lambda item: (item[1], fold_text(item[0]))):
        folded = fold_text(alkategoria)
        if count <= 5 or any(
            token in folded
            for token in [
                "joghurt, kefir",
                "joghurtital",
                "tejes desszert",
                "desszert",
                "tejszin, tejfol",
                "tejszin, hab",
                "tejes ital",
                "tejpor",
                "novenyi tejhelyettesito",
                "sajtkrem, kremsajt",
                "turo, cottage cheese",
            ]
        ):
            duplicate_like_alks.append(
                {
                    "alkategoria": alkategoria,
                    "termek_db": count,
                    "altipusok": [
                        {"altipus": altipus, "termek_db": alt_count}
                        for (path_alk, altipus), alt_count in by_path.most_common()
                        if path_alk == alkategoria
                    ],
                }
            )

    sajt_rows = []
    for (alkategoria, altipus), count in sorted(by_path.items(), key=lambda item: (-item[1], fold_text(item[0][1]))):
        if fold_text(alkategoria) == "sajt":
            sajt_rows.append({"altipus": altipus, "termek_db": count})

    explicit_findings = [
        {
            "tipus": "alkategoria_osszevonas",
            "megallapitas": "A Joghurt, kefir alkategoria vegyesen tartalmaz joghurtot, kefirt, joghurtitalt es novenyi fermentalt keszitmenyt.",
            "javaslat": "Szetszedes Joghurt, Ivojoghurt/kefir/iro es Novenyi alternativa ala.",
        },
        {
            "tipus": "alkategoria_osszevonas",
            "megallapitas": "A Tejes desszert es Desszert alkategoriak atfednek a Tejdesszert, puding es Kremturo, turodesszert alkategoriakkal.",
            "javaslat": "Puding/tejberizs/tejdeszert a Tejdesszert, puding ala; turodesszert/kremturo a Kremturo, turodesszert ala; novenyi desszertek a Novenyi alternativa ala.",
        },
        {
            "tipus": "altipus_osszevonas",
            "megallapitas": "A Sajt alatt tobb altipus par duplikalt vagy egymast szukiti: Camembert, brie vs Camembert / Brie; Feta vs Feta / kremfeher sajt; Kremsajt vs Kremsajt / kenheto sajt; Lagy sajt vs Friss / lagy sajt.",
            "javaslat": "Az alacsonyabb hasznalatu valtozatokat a stabilabb, nagyobb gyujto altipusba kell atvezetni.",
        },
        {
            "tipus": "tulajdonsag_torles",
            "megallapitas": "A termekcsalad es toltott tulajdonsag ritka es nem kategoriateremto informacio.",
            "javaslat": "Torles a tejtermekes termekekbol es a kategoriafabol, ha szerepel.",
        },
        {
            "tipus": "tulajdonsag_tisztitas",
            "megallapitas": "Az Ivojoghurt, kefir, iro alatt a jelleg tulajdonsag vegyesen altipus-, iz-, es jeloles-jellegu ertekeket hordoz.",
            "javaslat": "A jelleg torlese innen; a valodi informaciok kulon tulajdonsagokban mar megvannak vagy nevbol potolhatok.",
        },
        {
            "tipus": "sajt_tulajdonsag",
            "megallapitas": "A Sajt forma es fajta tulajdonsagai tobb helyen altipus-informaciot ismetelnek.",
            "javaslat": "Elso lepesben az altipus-duplikaciokat kell osszevonni; utana lehet a forma/fajta erteklistat szukiteni.",
        },
    ]

    audit = {
        "meta": {
            "generated_at": generated_at,
            "category_source": CATEGORY_PATH.name,
            "product_source": PRODUCT_PATH.name,
            "fokategoria": category_key,
            "termek_db": len(milk_products),
            "alkategoria_db": len(alkategoriak),
        },
        "alkategoriak_termekszammal": [
            {"alkategoria": alkategoria, "termek_db": count}
            for alkategoria, count in by_alk.most_common()
        ],
        "gyanus_alkategoriak": duplicate_like_alks,
        "sajt_altipusok": sajt_rows,
        "ritka_tulajdonsagok_max_5": [
            {
                "tulajdonsag": name,
                "termek_db": prop_counts[name],
                "ures_db": prop_empty_counts[name],
                "fo_alkategoriak": [
                    {"alkategoria": alkategoria, "termek_db": count}
                    for alkategoria, count in prop_by_alk[name].most_common(5)
                ],
                "gyakori_ertekek": [
                    {"ertek": value, "db": count}
                    for value, count in prop_values[name].most_common(10)
                ],
            }
            for name in rare_props
        ],
        "termekekben_van_de_kategoriafaban_nincs_tulajdonsag": [
            {
                "tulajdonsag": name,
                "termek_db": prop_counts[name],
                "gyakori_ertekek": [
                    {"ertek": value, "db": count}
                    for value, count in prop_values[name].most_common(10)
                ],
            }
            for name in product_only_props
        ],
        "kategoriafaban_van_de_termekekben_nincs_tulajdonsag": category_only_props,
        "fo_megallapitasok": explicit_findings,
    }

    json_path = OUT_DIR / f"tejtermekek_logikai_audit_{date_stamp}.json"
    md_path = OUT_DIR / f"tejtermekek_logikai_audit_{date_stamp}.md"
    dump_json(json_path, audit)

    lines: list[str] = [
        "# Tejtermékek logikai audit",
        "",
        f"- Generálva: {generated_at}",
        f"- Főkategória: {category_key}",
        f"- Termékek: {len(milk_products)}",
        f"- Alkategóriák: {len(alkategoriak)}",
        "",
        "## Fő megállapítások",
    ]
    for finding in explicit_findings:
        lines.append(f"- **{finding['tipus']}**: {finding['megallapitas']} Javaslat: {finding['javaslat']}")

    lines.extend(["", "## Alkategóriák termékszámmal"])
    lines.extend(
        markdown_table(
            ["Alkategória", "Termék"],
            [[alkategoria, count] for alkategoria, count in by_alk.most_common()],
        )
    )

    lines.extend(["", "## Gyanús alkategóriák és altípus-megoszlás"])
    for row in duplicate_like_alks:
        alt_text = ", ".join(f"{item['altipus'] or '(üres)'} ({item['termek_db']})" for item in row["altipusok"])
        lines.append(f"- **{row['alkategoria']}**: {row['termek_db']} termék. Altípusok: {alt_text}")

    lines.extend(["", "## Sajt altípusok"])
    lines.extend(
        markdown_table(
            ["Altípus", "Termék"],
            [[row["altipus"] or "(üres)", row["termek_db"]] for row in sajt_rows],
        )
    )

    lines.extend(["", "## Ritka tulajdonságok legfeljebb 5 termékkel"])
    lines.extend(
        markdown_table(
            ["Tulajdonság", "Termék", "Üres", "Fő alkategóriák", "Gyakori értékek"],
            [
                [
                    row["tulajdonsag"],
                    row["termek_db"],
                    row["ures_db"],
                    ", ".join(f"{item['alkategoria']} ({item['termek_db']})" for item in row["fo_alkategoriak"]),
                    ", ".join(f"{item['ertek']} ({item['db']})" for item in row["gyakori_ertekek"]),
                ]
                for row in audit["ritka_tulajdonsagok_max_5"]
            ],
        )
    )

    lines.extend(["", "## Termékekben használt, de kategóriafában nem deklarált tulajdonságok"])
    lines.extend(
        markdown_table(
            ["Tulajdonság", "Termék", "Gyakori értékek"],
            [
                [
                    row["tulajdonsag"],
                    row["termek_db"],
                    ", ".join(f"{item['ertek']} ({item['db']})" for item in row["gyakori_ertekek"]),
                ]
                for row in audit["termekekben_van_de_kategoriafaban_nincs_tulajdonsag"]
            ],
        )
    )

    lines.extend(["", "## Kategóriafában deklarált, de termékekben nem használt tulajdonságok"])
    lines.extend(f"- {name}" for name in category_only_props)

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"audit_json={json_path}")
    print(f"audit_md={md_path}")
    print(f"milk_products={len(milk_products)}")
    print(f"rare_props={len(rare_props)}")
    print(f"product_only_props={len(product_only_props)}")


if __name__ == "__main__":
    main()
