from __future__ import annotations

import json
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
WORK_DIR = BASE_DIR / "tejtermekek_munkafajlok"

CATEGORY_SOURCE = WORK_DIR / "tejtermekek_kategoria_2026-06-24.json"
PRODUCT_SOURCE = WORK_DIR / "tejtermekek_termekek_2026-06-24.json"

DATE_STAMP = "2026-06-24"
CATEGORY_OUT = WORK_DIR / f"tejtermekek_javitott_kategoria_{DATE_STAMP}.json"
PRODUCT_OUT = WORK_DIR / f"tejtermekek_javitott_termekek_{DATE_STAMP}.json"
AUDIT_JSON_OUT = WORK_DIR / f"tejtermekek_javitott_audit_{DATE_STAMP}.json"
AUDIT_MD_OUT = WORK_DIR / f"tejtermekek_javitott_audit_{DATE_STAMP}.md"

FORBIDDEN_OUTPUT_NAMES = {
    "eredmeny.json",
    "kategoriak_2026-06-13.json",
}

NOISY_OR_MERGED_PROPS = {
    "alapanyag",
    "cukormentes",
    "dieta",
    "elofloras",
    "feherje",
    "friss",
    "hozzaadott anyag",
    "hozzaadott vitamin / asvanyi anyag",
    "iz / jelleg",
    "jellemzo",
    "jellemzok",
    "kiszereles_mennyiseg",
    "mentes",
    "mentesseg",
    "minosites",
    "novenyi alap",
    "novenyi_alap",
    "novenyi alapu",
    "sajt tipusa",
    "sajtfajta",
    "tartasi mod",
    "tej tipusa",
    "tejtipus",
    "termekcsalad",
    "toltott",
    "turo tipusa",
    "valtozat",
    "zsirszegeny",
    "zsirtartalom / jelleg",
}

SAJT_BAD_FORMA_VALUES = {
    "friss sajt",
    "grillsajt",
    "lagy sajt",
    "nagylyuku",
    "sajt",
    "sajtkeszitmeny",
    "sajtkrem",
    "soleben erlelt",
    "szemcses friss sajt",
    "szendvicskrem",
    "tejszinsajt",
    "vaghato",
    "valogatas",
}


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
    if path.name in FORBIDDEN_OUTPUT_NAMES:
        raise RuntimeError(f"Forbidden output target: {path}")
    if not path.resolve().is_relative_to(WORK_DIR.resolve()):
        raise RuntimeError(f"Output must stay under {WORK_DIR}: {path}")

    tmp_path = path.with_name(f"{path.name}.tmp")
    with tmp_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with tmp_path.open("r", encoding="utf-8") as handle:
        json.load(handle)
    tmp_path.replace(path)


def values_of(value: Any) -> list[Any]:
    if value in (None, "", [], {}):
        return []
    return value if isinstance(value, list) else [value]


def folded_get(mapping: dict[str, Any], folded_name: str, default: Any = None) -> Any:
    for key, value in mapping.items():
        if fold_text(key) == folded_name:
            return value
    return default


def property_names_from_block(block: Any) -> set[str]:
    names: set[str] = set()
    if not isinstance(block, dict):
        return names
    for group in block.values():
        if isinstance(group, dict):
            names.update(str(name) for name in group)
    return names


def collect_declared_paths(category_node: dict[str, Any]) -> set[tuple[str, str]]:
    paths: set[tuple[str, str]] = set()
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    for alkategoria, alk_node in alkategoriak.items():
        paths.add((alkategoria, ""))
        altipusok = folded_get(alk_node, "altipusok", {}) or {}
        for altipus in altipusok:
            paths.add((alkategoria, altipus))
    return paths


def collect_category_props(category_node: dict[str, Any]) -> set[str]:
    props: set[str] = set()

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            prop_block = folded_get(node, "tulajdonsagok")
            props.update(property_names_from_block(prop_block))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(category_node)
    return props


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe_row = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(safe_row) + " |")
    return lines


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")
    category_payload = load_json(CATEGORY_SOURCE)
    product_payload = load_json(PRODUCT_SOURCE)

    category_map = category_payload["kategoria"]
    if len(category_map) != 1:
        raise RuntimeError(f"Expected exactly one category root, got {list(category_map)}")

    category_name, category_node = next(iter(category_map.items()))
    products = product_payload["termekek"]

    declared_paths = collect_declared_paths(category_node)
    declared_props = collect_category_props(category_node)

    path_counts = Counter((p.get("alkategoria", ""), p.get("altipus", "")) for p in products)
    alk_counts = Counter(p.get("alkategoria", "") for p in products)
    prop_counts: Counter[str] = Counter()
    prop_value_counts: dict[str, Counter[str]] = defaultdict(Counter)
    noisy_props = Counter()
    bad_sajt_forma = Counter()
    missing_paths = Counter()

    for product in products:
        path = (product.get("alkategoria", ""), product.get("altipus", ""))
        if path not in declared_paths:
            missing_paths[path] += 1

        props = product.get("tulajdonsagok") or {}
        for prop_name, raw_value in props.items():
            prop_counts[prop_name] += 1
            if fold_text(prop_name) in NOISY_OR_MERGED_PROPS:
                noisy_props[prop_name] += 1
            for value in values_of(raw_value):
                prop_value_counts[prop_name][str(value)] += 1
                if (
                    fold_text(product.get("alkategoria", "")) == "sajt"
                    and fold_text(prop_name) == "forma"
                    and fold_text(value) in SAJT_BAD_FORMA_VALUES
                ):
                    bad_sajt_forma[str(value)] += 1

    product_props = set(prop_counts)
    rare_props = {
        prop_name: count
        for prop_name, count in prop_counts.items()
        if count <= 5 and prop_name not in {"márka"}
    }

    audit = {
        "meta": {
            "generated_at": generated_at,
            "input_category_file": CATEGORY_SOURCE.name,
            "input_product_file": PRODUCT_SOURCE.name,
            "output_category_file": CATEGORY_OUT.name,
            "output_product_file": PRODUCT_OUT.name,
            "fokategoria": category_name,
            "note": "Csak kulon tejtermekes munkafajlokbol dolgozik; fo JSON fajlokat nem ir.",
        },
        "counts": {
            "products": len(products),
            "alkategoriak": len(folded_get(category_node, "alkategoriak", {}) or {}),
            "declared_paths": len(declared_paths),
            "used_paths": len(path_counts),
            "empty_altipus_products": sum(count for (alk, alt), count in path_counts.items() if not alt),
            "missing_paths": len(missing_paths),
            "product_only_props": len(product_props - declared_props),
            "category_only_props": len(declared_props - product_props),
            "rare_props_max_5": len(rare_props),
            "noisy_or_merged_props_left": sum(noisy_props.values()),
            "bad_sajt_forma_values_left": sum(bad_sajt_forma.values()),
        },
        "alkategoriak": [
            {"alkategoria": alkategoria, "termek_db": count}
            for alkategoria, count in alk_counts.most_common()
        ],
        "termekutak": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in path_counts.most_common()
        ],
        "missing_paths": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in missing_paths.most_common()
        ],
        "product_only_props": sorted(product_props - declared_props, key=fold_text),
        "category_only_props": sorted(declared_props - product_props, key=fold_text),
        "rare_props_max_5": [
            {
                "tulajdonsag": prop_name,
                "termek_db": count,
                "gyakori_ertekek": prop_value_counts[prop_name].most_common(10),
            }
            for prop_name, count in sorted(rare_props.items(), key=lambda item: (item[1], fold_text(item[0])))
        ],
        "noisy_or_merged_props_left": dict(noisy_props),
        "bad_sajt_forma_values_left": dict(bad_sajt_forma),
    }

    output_category_payload = {
        **category_payload,
        "meta": {
            **category_payload.get("meta", {}),
            "separate_working_copy": True,
            "generated_from": CATEGORY_SOURCE.name,
            "generated_at": generated_at,
        },
    }
    output_product_payload = {
        **product_payload,
        "meta": {
            **product_payload.get("meta", {}),
            "separate_working_copy": True,
            "generated_from": PRODUCT_SOURCE.name,
            "generated_at": generated_at,
        },
    }

    dump_json(CATEGORY_OUT, output_category_payload)
    dump_json(PRODUCT_OUT, output_product_payload)
    dump_json(AUDIT_JSON_OUT, audit)

    lines = [
        "# Tejtermékek külön munkafájl audit",
        "",
        f"- Generálva: {generated_at}",
        f"- Bemeneti kategória: `{CATEGORY_SOURCE.name}`",
        f"- Bemeneti termékek: `{PRODUCT_SOURCE.name}`",
        f"- Kimeneti kategória: `{CATEGORY_OUT.name}`",
        f"- Kimeneti termékek: `{PRODUCT_OUT.name}`",
        "- A fő JSON fájlok nem célfájlok, ez a script nem írja őket.",
        "",
        "## Összesítés",
    ]
    lines.extend(f"- {key}: {value}" for key, value in audit["counts"].items())
    lines.extend(["", "## Alkategóriák"])
    lines.extend(
        markdown_table(
            ["Alkategória", "Termék"],
            [[row["alkategoria"], row["termek_db"]] for row in audit["alkategoriak"]],
        )
    )
    lines.extend(["", "## Ellenőrzési maradékok"])
    lines.append(f"- Hiányzó útvonalak: {audit['missing_paths']}")
    lines.append(f"- Termékben van, kategóriafában nincs tulajdonság: {audit['product_only_props']}")
    lines.append(f"- Kategóriafában van, termékben nincs tulajdonság: {audit['category_only_props']}")
    lines.append(f"- Ritka tulajdonságok max. 5 termékkel: {audit['rare_props_max_5']}")
    lines.append(f"- Régi/összevont mezők maradtak: {audit['noisy_or_merged_props_left']}")
    lines.append(f"- Rossz sajt forma értékek maradtak: {audit['bad_sajt_forma_values_left']}")

    AUDIT_MD_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"products={len(products)}")
    print(f"alkategoriak={audit['counts']['alkategoriak']}")
    print(f"missing_paths={audit['counts']['missing_paths']}")
    print(f"product_only_props={audit['counts']['product_only_props']}")
    print(f"category_only_props={audit['counts']['category_only_props']}")
    print(f"rare_props_max_5={audit['counts']['rare_props_max_5']}")
    print(f"noisy_or_merged_props_left={audit['counts']['noisy_or_merged_props_left']}")
    print(f"bad_sajt_forma_values_left={audit['counts']['bad_sajt_forma_values_left']}")
    print(f"audit={AUDIT_MD_OUT}")


if __name__ == "__main__":
    main()
