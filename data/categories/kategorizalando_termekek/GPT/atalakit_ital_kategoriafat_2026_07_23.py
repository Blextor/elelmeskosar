# -*- coding: utf-8 -*-
"""Az Ital kategóriafa 2026-07-23-i, megismételhető átalakítása.

Alapértelmezésben csak memóriában dolgozik és nem ír fájlt. A ``--apply``
kapcsoló a két fő JSON-fájlt tranzakciósan cseréli, de csak a külön, csak olvasó
ellenőrző sikeres candidate- és visszaolvasási futása után.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

# A gépen korábban a nagy, ékezetes adathalmaz C-encoderes kiírása instabil volt.
json.encoder.c_make_encoder = None

BASE = Path(__file__).resolve().parent
RESULT_PATH = BASE / "eredmeny.json"
CATEGORY_PATH = BASE / "kategoriak_2026-06-13.json"
CHECKER_PATH = BASE / "ellenoriz_ital_kategoriafat_2026_07_23.py"
AUDIT_PATH = BASE / "ital_kategoriafa_atstrukturazas_2026-07-23.json"
REPORT_PATH = BASE / "ital_kategoriafa_atstrukturazas_2026-07-23.md"

ITAL = "Ital"
PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"

EXPECTED_TOTAL_PRODUCTS = 47030
EXPECTED_SOURCE_ITAL_PRODUCTS = 12876
EXPECTED_TARGET_ITAL_PRODUCTS = 12810
NESQUIK_ID = "209545089"
CITRIORANGE_ID = "440767:3978151"
FRUIT_STEP_GINGER_ID = "121283822"

ALCOHOL_BRANCH = "Alkoholos italok és alkoholmentes alternatívák"
WATER_BRANCH = "Víz és vízalapú italok"
SOFT_BRANCH = "Üdítőitalok"
FRUIT_BRANCH = "Gyümölcs- és zöldségitalok"
FUNCTIONAL_BRANCH = "Funkcionális és teljesítményitalok"
PLANT_BRANCH = "Növényi italok"
HOT_BRANCH = "Kávé-, tea- és kakaótermékek"
BASE_BRANCH = "Italkészítési alapok"

NESQUIK_TARGET = (
    "Alapanyag, sütés-főzés",
    "Szószok, öntetek, dresszingek",
    "Desszertszósz, topping",
)
CITRUS_OLD_TARGET = (
    "Alapanyag, sütés-főzés",
    "Olaj, ecet, zsiradék",
    "Citromlé, limelé",
)
CITRUS_TARGET = (
    "Alapanyag, sütés-főzés",
    "Olaj, ecet, zsiradék",
    "Citruslé és citrusízesítő",
)

TARGET_HIERARCHY: dict[str, tuple[str, ...]] = {
    WATER_BRANCH: (
        "Ízesítetlen palackozott víz",
        "Ízesített víz",
    ),
    ALCOHOL_BRANCH: (
        "Bor és boralapú ital",
        "Pezsgő, habzóbor és gyöngyözőbor",
        "Sör, radler és malátaital",
        "Cider",
        "Likőr",
        "Whisky és bourbon",
        "Gin",
        "Rum",
        "Tequila",
        "Vodka",
        "Pálinka",
        "Brandy",
        "Vermut és aperitif",
        "Egyéb szeszes ital",
        "Koktél és előre kevert ital",
    ),
    SOFT_BRANCH: (
        "Kóla",
        "Tonik",
        "Jegestea",
        "Limonádé",
        "Aloe vera ital",
        "Gyömbér- és gyökéralapú üdítőital",
        "Kombucha",
        "Egyéb ízesített üdítőital",
    ),
    FRUIT_BRANCH: (
        "Lé",
        "Nektár",
        "Gyümölcsital",
        "Smoothie és püréital",
    ),
    FUNCTIONAL_BRANCH: (
        "Energiaital",
        "Sport- és izotóniás ital",
        "Vitamin- és wellnessital",
        "Egyéb funkcionális ital",
    ),
    PLANT_BRANCH: (
        "Egynövényes ital",
        "Kevert növényi ital",
    ),
    HOT_BRANCH: (
        "Kávé",
        "Tea",
        "Kakaó és forró csokoládé",
        "Kávé- és teaadalék",
    ),
    BASE_BRANCH: (
        "Italszirup és folyékony koncentrátum",
        "Italpor és tabletta",
    ),
}
TARGET_PATHS = frozenset(
    (alkategoria, altipus)
    for alkategoria, altipusok in TARGET_HIERARCHY.items()
    for altipus in altipusok
)


def build_source_routes() -> dict[tuple[str, str], tuple[str, str] | tuple[str, str, str]]:
    routes: dict[tuple[str, str], tuple[str, str] | tuple[str, str, str]] = {}

    def add(
        alkategoria: str,
        target: tuple[str, str] | tuple[str, str, str],
        *altipusok: str,
    ) -> None:
        for altipus in altipusok:
            key = (alkategoria, altipus)
            if key in routes:
                raise RuntimeError(f"Duplikált forrásút: {key}")
            routes[key] = target

    add(
        "Ásványvíz",
        (WATER_BRANCH, "Ízesítetlen palackozott víz"),
        "Szénsavmentes ásványvíz",
        "Szénsavas ásványvíz",
        "Enyhén szénsavas ásványvíz",
    )
    add("Ízesített víz", (WATER_BRANCH, "Ízesített víz"), "")

    add(
        "Bor",
        (ALCOHOL_BRANCH, "Bor és boralapú ital"),
        "Fehérbor",
        "Rozébor",
        "Vörösbor",
        "Boralapú ital",
        "Tokaji borkülönlegesség",
        "Alkoholmentes bor",
    )
    add(
        "Habzó-, gyöngyözőbor, boralapú ital",
        (ALCOHOL_BRANCH, "Pezsgő, habzóbor és gyöngyözőbor"),
        "Gyöngyözőbor",
        "Alkoholmentes habzó ital",
    )
    add(
        "Habzó-, gyöngyözőbor, boralapú ital",
        (ALCOHOL_BRANCH, "Bor és boralapú ital"),
        "Ízesített boralapú ital",
    )
    add(
        "Pezsgő",
        (ALCOHOL_BRANCH, "Pezsgő, habzóbor és gyöngyözőbor"),
        "",
        "Prosecco",
    )

    spirit_routes = {
        "Likőr": "Likőr",
        "Whisky & Bourbon": "Whisky és bourbon",
        "Gin": "Gin",
        "Rum": "Rum",
        "Tequila": "Tequila",
        "Vodka": "Vodka",
        "Pálinka": "Pálinka",
        "Brandy": "Brandy",
        "Koktél, Rögtön iható, Egyéb": "Koktél és előre kevert ital",
        "Vermut": "Vermut és aperitif",
        "Szeszesital": "Egyéb szeszes ital",
        "Alkoholmentes szeszesital, koktél": "Egyéb szeszes ital",
    }
    for source_alt, target_alt in spirit_routes.items():
        add("Alkoholok", (ALCOHOL_BRANCH, target_alt), source_alt)

    add(
        "Sör",
        (ALCOHOL_BRANCH, "Sör, radler és malátaital"),
        "Ízesített sör",
        "Világos sör",
        "Alkoholmentes sör",
        "Malátaital",
        "Búzasör",
        "Alkoholmentes radler",
        "Barna sör",
        "IPA / Ale",
        "Sörválogatás",
    )
    add(
        "Cider",
        (ALCOHOL_BRANCH, "Cider"),
        "",
        "Alkoholmentes cider",
    )

    add("Energiaital", (FUNCTIONAL_BRANCH, "Energiaital"), "")
    add("Sportital", (FUNCTIONAL_BRANCH, "Sport- és izotóniás ital"), "")
    add(
        "Funkcionális ital",
        (FUNCTIONAL_BRANCH, "Egyéb funkcionális ital"),
        "",
        "Shot ital",
    )
    add(
        "Funkcionális ital",
        (FUNCTIONAL_BRANCH, "Vitamin- és wellnessital"),
        "Vitaminital",
    )

    add("Kombucha", (SOFT_BRANCH, "Kombucha"), "")

    add(
        "Üdítőital",
        (SOFT_BRANCH, "Jegestea"),
        "Jegestea",
    )
    add("Üdítőital", (SOFT_BRANCH, "Limonádé"), "Limonádé")
    add("Üdítőital", (FRUIT_BRANCH, "Gyümölcsital"), "Gyümölcsital", "Gyerekital")
    add("Üdítőital", (SOFT_BRANCH, "Kóla"), "Cola")
    add("Üdítőital", (SOFT_BRANCH, "Aloe vera ital"), "Aloe vera ital")
    add("Üdítőital", (SOFT_BRANCH, "Tonik"), "Tonic")
    add(
        "Üdítőital",
        (SOFT_BRANCH, "Egyéb ízesített üdítőital"),
        "Szénsavas üdítő",
        "Szénsavmentes üdítő",
    )
    add("Üdítőital", (FRUIT_BRANCH, "Smoothie és püréital"), "Smoothie")
    add(
        "Üdítőital",
        (SOFT_BRANCH, "Gyömbér- és gyökéralapú üdítőital"),
        "Gyökér alapú üdítőital",
    )

    add("Gyümölcslé", (FRUIT_BRANCH, "Lé"), "100% gyümölcslé")
    add("Gyümölcslé", (FRUIT_BRANCH, "Lé"), "Vegyes gyümölcs- és zöldséglé")
    add("Gyümölcslé", (FRUIT_BRANCH, "Lé"), "Zöldséglé")
    add("Gyümölcslé", (FRUIT_BRANCH, "Nektár"), "Nektár")
    add("Gyümölcslé", (FRUIT_BRANCH, "Smoothie és püréital"), "Gyümölcspüré")

    plant_routes = {
        "Zabital": "zab",
        "Kókuszital": "kókusz",
        "Szójaital": "szója",
        "Mandulaital": "mandula",
        "Rizsital": "rizs",
        "Mogyoróital": "mogyoró",
        "Egyéb növényi ital": "mogyoró",
    }
    for source_alt in plant_routes:
        add("Növényi ital", (PLANT_BRANCH, "Egynövényes ital"), source_alt)
    add("Növényi ital", (PLANT_BRANCH, "Kevert növényi ital"), "Kevert növényi ital")

    coffee_alts = (
        "Cappuccino italpor",
        "Őrölt kávé",
        "Szemes kávé",
        "Instant kávé",
        "Kávékapszula",
        "2in1, 3in1 instant kávé",
    )
    add("Kávé, tea, kakaó (száraz)", (HOT_BRANCH, "Kávé"), *coffee_alts)
    tea_alts = (
        "Teafű, filteres tea, instant tea",
        "Gyümölcstea",
        "Rooibos tea",
        "Gyógytea",
        "Fekete tea",
        "Zöld tea",
    )
    add("Kávé, tea, kakaó (száraz)", (HOT_BRANCH, "Tea"), *tea_alts)
    add(
        "Kávé, tea, kakaó (száraz)",
        (HOT_BRANCH, "Kakaó és forró csokoládé"),
        "Kakaó italpor",
        "Kakaópor",
        "Forró csokoládé italpor",
    )
    add(
        "Kávé, tea, kakaó (száraz)",
        (HOT_BRANCH, "Kávé- és teaadalék"),
        "Kávé ízesítők / tejek / tejporok",
    )

    add("Citromlé", CITRUS_TARGET, "", "Citromízesítő")
    add(
        "Szörp, üdítőitalpor",
        (BASE_BRANCH, "Italszirup és folyékony koncentrátum"),
        "Szörp",
        "Koktélszirup, italkoncentrátum",
    )
    add(
        "Szörp, üdítőitalpor",
        (BASE_BRANCH, "Italpor és tabletta"),
        "Üdítőitalpor, italtabletta",
    )

    if len(routes) != 89:
        raise RuntimeError(f"A forrásút-térkép nem 89 elemű: {len(routes)}")
    return routes


SOURCE_ROUTES = build_source_routes()
SOURCE_PATHS = frozenset(SOURCE_ROUTES)
NONALCOHOLIC_SOURCE_PATHS = frozenset(
    {
        ("Bor", "Alkoholmentes bor"),
        ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
        ("Alkoholok", "Alkoholmentes szeszesital, koktél"),
        ("Sör", "Alkoholmentes sör"),
        ("Sör", "Alkoholmentes radler"),
        ("Sör", "Malátaital"),
        ("Cider", "Alkoholmentes cider"),
    }
)
PLANT_BASE_BY_ALT = {
    "Zabital": "zab",
    "Kókuszital": "kókusz",
    "Szójaital": "szója",
    "Mandulaital": "mandula",
    "Rizsital": "rizs",
    "Mogyoróital": "mogyoró",
    "Egyéb növényi ital": "mogyoró",
}


def fold_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^0-9a-z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplikált JSON-kulcs: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def dump_json(path: Path, payload: Any) -> None:
    json.encoder.c_make_encoder = None
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    load_json(path)


def values_of(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    return list(value) if isinstance(value, list) else [value]


def dedupe(values: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value is None or value == "":
            continue
        marker = f"{type(value).__name__}:{fold_text(value)}"
        if marker in seen:
            continue
        seen.add(marker)
        result.append(value)
    return result


def append_list(props: dict[str, Any], name: str, additions: Iterable[Any]) -> None:
    merged = dedupe([*values_of(props.get(name)), *additions])
    if merged:
        props[name] = merged
    else:
        props.pop(name, None)


def set_scalar(props: dict[str, Any], name: str, value: Any) -> None:
    if value is None or value == "":
        props.pop(name, None)
    else:
        props[name] = value


def product_id(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("store_product_id") or "")


def product_name(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("product_name") or "")


def product_text(product: dict[str, Any]) -> str:
    termek = product.get("termek") or {}
    return fold_text(
        " ".join(
            [
                str(termek.get("product_name") or ""),
                str(termek.get("brand_name") or ""),
                str(termek.get("categories") or ""),
                json.dumps(product.get("tulajdonsagok") or {}, ensure_ascii=False),
            ]
        )
    )


def product_state(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "fokategoria": product.get("fokategoria"),
        "alkategoria": product.get("alkategoria"),
        "altipus": product.get("altipus"),
        "tulajdonsagok": copy.deepcopy(product.get("tulajdonsagok") or {}),
    }


def category_hash(product: dict[str, Any]) -> str:
    key = "|".join(
        [
            str(product.get("fokategoria") or ""),
            str(product.get("alkategoria") or ""),
            str(product.get("altipus") or ""),
            json.dumps(product.get("tulajdonsagok") or {}, sort_keys=True, ensure_ascii=False),
        ]
    )
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def normalize_percent_value(value: Any) -> str | None:
    text = str(value).strip()
    folded = fold_text(text)
    if folded in {"alkoholos", "egyeb", "nem jelolt", ""}:
        return None
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*%", text)
    if not match:
        return text
    number = match.group(1).replace(".", ",")
    if number.endswith(",0"):
        number = number[:-2]
    return f"{number}%"


def percent_number(value: Any) -> float | None:
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*%", str(value))
    return float(match.group(1).replace(",", ".")) if match else None


def normalize_alcohol(
    props: dict[str, Any],
    status: str,
    operations: Counter[str],
    conflicts: list[dict[str, Any]],
    item_id: str,
) -> None:
    set_scalar(props, "alkoholstátusz", status)
    raw_values = values_of(props.get("alkoholtartalom"))
    normalized = dedupe(
        value
        for raw in raw_values
        if (value := normalize_percent_value(raw)) is not None
    )
    numeric = [(value, percent_number(value)) for value in normalized]
    if status == "alkoholmentes":
        incompatible = [value for value, number in numeric if number is not None and number > 0.5]
        if incompatible:
            conflicts.append(
                {
                    "id": item_id,
                    "property": "alkoholtartalom",
                    "before": raw_values,
                    "resolution": ["0,0%"],
                    "reason": "explicit alkoholmentes forrásút",
                }
            )
            normalized = ["0,0%"]
        else:
            normalized = [
                value
                for value, number in numeric
                if number is None or number <= 0.5
            ]
            if not normalized:
                normalized = ["0,0%"]
        props["alkoholtartalom"] = dedupe(normalized)
    else:
        low_only = bool(numeric) and not any(
            number is None or number > 0.5 for _value, number in numeric
        )
        if low_only:
            conflicts.append(
                {
                    "id": item_id,
                    "property": "alkoholtartalom",
                    "before": raw_values,
                    "resolution": None,
                    "reason": "alkoholos termékút mellett csak 0-0,5% szerepelt",
                }
            )
            normalized = []
        else:
            normalized = [
                value
                for value, number in numeric
                if number is None or number > 0.5
            ]
        if normalized:
            props["alkoholtartalom"] = dedupe(normalized)
        else:
            props.pop("alkoholtartalom", None)
    if raw_values != values_of(props.get("alkoholtartalom")):
        operations["alkoholtartalom_normalizálva"] += 1


def normalize_energy(props: dict[str, Any], operations: Counter[str]) -> None:
    energy = props.get("energia tartalom")
    redundant = props.get("energiamentes")
    if energy is None and redundant is True:
        props["energia tartalom"] = "energiamentes"
        operations["energia_tartalom_flagből_pótolva"] += 1
    if "energiamentes" in props:
        del props["energiamentes"]
        operations["redundáns_energiamentes_flag_törölve"] += 1


def normalize_caffeine(props: dict[str, Any], operations: Counter[str]) -> None:
    if "koffeinmentes" not in props:
        return
    value = props["koffeinmentes"]
    if isinstance(value, bool):
        return
    atoms = values_of(value)
    folded = {fold_text(atom) for atom in atoms}
    props["koffeinmentes"] = bool(
        True in atoms or "true" in folded or "igen" in folded or "koffeinmentes" in folded
    )
    operations["koffeinmentes_flag_alakja_javítva"] += 1


def split_coffee_system(
    product: dict[str, Any],
    props: dict[str, Any],
    operations: Counter[str],
) -> None:
    if "kiszerelés / rendszer" not in props:
        return
    raw = props.pop("kiszerelés / rendszer")
    for atom in values_of(raw):
        folded = fold_text(atom)
        if folded in {"", "nem jelolt", "egyeb"}:
            continue
        if "nespresso" in folded:
            append_list(props, "kávérendszer", ["Nespresso-kompatibilis"])
        elif "dolce gusto" in folded:
            append_list(props, "kávérendszer", ["Dolce Gusto"])
        elif "cafissimo" in folded:
            append_list(props, "kávérendszer", ["Tchibo Cafissimo"])
        elif "iperespresso" in folded:
            append_list(props, "kávérendszer", ["Illy Iperespresso"])
        elif "vacuum" in folded or "vakuum" in folded:
            append_list(props, "csomagolás", ["vákuumcsomagolás"])
        elif "coffee pod" in folded or "parnas" in folded or "párnás" in str(atom).casefold():
            if "parna" in fold_text(product_name(product)) or "pad" in fold_text(product_name(product)):
                append_list(props, "csomagolás", ["kávépárna"])
            else:
                append_list(props, "csomagolás", ["tasak"])
        elif "kapszula" in folded:
            append_list(props, "csomagolás", ["kapszula"])
        elif "utantolto" in folded or "refill" in folded:
            append_list(props, "csomagolás", ["utántöltő tasak"])
        elif "tasak" in folded:
            append_list(props, "csomagolás", ["tasak"])
        else:
            append_list(props, "csomagolás", [str(atom)])
    operations["kiszerelés_rendszer_szétválasztva"] += 1


CARBONATION_MAP = {
    "szensavmentes": "szénsavmentes",
    "szensavas": "szénsavas",
    "enyhen szensavas": "enyhén szénsavas",
    "extra szensavas": "extra szénsavas",
}


def carbonation_from_name(product: dict[str, Any]) -> str | None:
    text = fold_text(product_name(product))
    if "szensavmentes" in text or re.search(r"\bstill\b", text):
        return "szénsavmentes"
    if "enyhen szensavas" in text or "mild" in text:
        return "enyhén szénsavas"
    if "extra szensavas" in text or "extra dus" in text:
        return "extra szénsavas"
    if "szensavas" in text or "sparkling" in text:
        return "szénsavas"
    return None


def normalize_carbonation(
    product: dict[str, Any],
    old_path: tuple[str, str] | None,
    operations: Counter[str],
    conflicts: list[dict[str, Any]],
) -> None:
    props = product.get("tulajdonsagok") or {}
    target_path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
    existing = dedupe(
        CARBONATION_MAP[folded]
        for atom in values_of(props.get("szénsavasság"))
        if (folded := fold_text(atom)) in CARBONATION_MAP
    )
    name_value = carbonation_from_name(product)
    forced: str | None = None
    if old_path:
        if old_path == ("Ásványvíz", "Enyhén szénsavas ásványvíz"):
            forced = name_value or (existing[0] if len(existing) == 1 else None) or "enyhén szénsavas"
        elif old_path == ("Ásványvíz", "Szénsavas ásványvíz"):
            forced = name_value or (existing[0] if len(existing) == 1 else None) or "szénsavas"
        elif old_path == ("Ásványvíz", "Szénsavmentes ásványvíz"):
            forced = name_value or (existing[0] if len(existing) == 1 else None) or "szénsavmentes"
        elif old_path == ("Üdítőital", "Szénsavas üdítő"):
            forced = name_value or "szénsavas"
        elif old_path == ("Üdítőital", "Szénsavmentes üdítő"):
            forced = name_value or "szénsavmentes"
    if target_path in {
        (SOFT_BRANCH, "Kóla"),
        (SOFT_BRANCH, "Tonik"),
    }:
        forced = "szénsavas"
    elif target_path[0] == WATER_BRANCH:
        forced = forced or name_value or (existing[0] if len(existing) == 1 else None)
    elif forced is None:
        forced = name_value or (existing[0] if len(existing) == 1 else None)

    before = copy.deepcopy(props.get("szénsavasság"))
    if forced:
        props["szénsavasság"] = forced
    else:
        props.pop("szénsavasság", None)
    if before != props.get("szénsavasság"):
        operations["szénsavasság_egyértékűsítve"] += 1
        if len(existing) > 1:
            conflicts.append(
                {
                    "id": product_id(product),
                    "property": "szénsavasság",
                    "before": before,
                    "resolution": forced,
                    "reason": "ellentmondó többértékű adat",
                }
            )


def special_spirit_target(product: dict[str, Any]) -> tuple[str, str]:
    text = product_text(product)
    brand = fold_text((product.get("tulajdonsagok") or {}).get("márka"))
    if "gin" in text or brand == "tanqueray":
        return ALCOHOL_BRANCH, "Gin"
    if "rum" in text:
        return ALCOHOL_BRANCH, "Rum"
    if "whisky" in text or "whiskey" in text or "bourbon" in text:
        return ALCOHOL_BRANCH, "Whisky és bourbon"
    if "vodka" in text:
        return ALCOHOL_BRANCH, "Vodka"
    if (
        "vermut" in text
        or "aperitif" in text
        or brand in {"martini", "mionetto"}
    ):
        return ALCOHOL_BRANCH, "Vermut és aperitif"
    if any(
        marker in text
        for marker in ("koktel", "mojito", "pina colada", "margarita", "spritz")
    ):
        return ALCOHOL_BRANCH, "Koktél és előre kevert ital"
    return ALCOHOL_BRANCH, "Egyéb szeszes ital"


def special_generic_drink_target(
    product: dict[str, Any],
    old_path: tuple[str, str],
    default_target: tuple[str, str],
) -> tuple[str, str] | tuple[str, str, str]:
    text = product_text(product)
    item_id = product_id(product)
    if old_path == ("Szörp, üdítőitalpor", "Koktélszirup, italkoncentrátum"):
        if item_id == NESQUIK_ID:
            return NESQUIK_TARGET
        if "pezsgokocka" in text or "italtabletta" in text:
            return BASE_BRANCH, "Italpor és tabletta"
    if old_path == ("Kávé, tea, kakaó (száraz)", "Teafű, filteres tea, instant tea"):
        if "instant" in text and ("italpor" in text or "granulatum" in text or "tabletta" in text):
            return BASE_BRANCH, "Italpor és tabletta"
    if old_path == ("Üdítőital", "Gyerekital"):
        if "pure" in text or "smoothie" in text or "püré" in product_name(product).casefold():
            return FRUIT_BRANCH, "Smoothie és püréital"
        fruit_content = {
            fold_text(value)
            for value in values_of((product.get("tulajdonsagok") or {}).get("gyümölcstartalom"))
        }
        if "100" in fruit_content or "100%" in product_name(product):
            return FRUIT_BRANCH, "Lé"
        if "nektar" in text:
            return FRUIT_BRANCH, "Nektár"
        return FRUIT_BRANCH, "Gyümölcsital"
    if old_path[0] == "Növényi ital":
        bases = {
            fold_text(value)
            for value in values_of((product.get("tulajdonsagok") or {}).get("alap"))
            if fold_text(value)
        }
        source_base = PLANT_BASE_BY_ALT.get(old_path[1])
        if source_base:
            bases.add(fold_text(source_base))
        if old_path[1] == "Kevert növényi ital" or len(bases) > 1:
            return PLANT_BRANCH, "Kevert növényi ital"
        return PLANT_BRANCH, "Egynövényes ital"
    if old_path in {
        ("Üdítőital", "Szénsavas üdítő"),
        ("Üdítőital", "Szénsavmentes üdítő"),
    }:
        if "kombucha" in text:
            return SOFT_BRANCH, "Kombucha"
        if "cola" in text or "kola" in text:
            return SOFT_BRANCH, "Kóla"
        if "tonic" in text or "tonik" in text:
            return SOFT_BRANCH, "Tonik"
        if "limonade" in text:
            return SOFT_BRANCH, "Limonádé"
        if "ice tea" in text or "jegestea" in text or "jeges tea" in text:
            return SOFT_BRANCH, "Jegestea"
        if "izesitett viz" in text or "flavoured water" in text:
            return WATER_BRANCH, "Ízesített víz"
        if "energiaital" in text or "energy drink" in text:
            return FUNCTIONAL_BRANCH, "Energiaital"
        if "smoothie" in text or "pure" in text:
            return FRUIT_BRANCH, "Smoothie és püréital"
        if "100" in text and ("gyumolcsle" in text or "zoldsegle" in text):
            return FRUIT_BRANCH, "Lé"
        if "gyumolcsital" in text:
            return FRUIT_BRANCH, "Gyümölcsital"
        if "gyomber" in text or "ginger" in text or "root beer" in text:
            return SOFT_BRANCH, "Gyömbér- és gyökéralapú üdítőital"
    return default_target


def add_source_semantics(
    product: dict[str, Any],
    old_path: tuple[str, str],
    operations: Counter[str],
) -> None:
    props = product.setdefault("tulajdonsagok", {})
    old_alk, old_alt = old_path

    if old_alk == "Bor":
        append_list(props, "bortípus", ["boralapú ital" if old_alt == "Boralapú ital" else "bor"])
        color = {
            "Fehérbor": "fehér",
            "Rozébor": "rozé",
            "Vörösbor": "vörös",
        }.get(old_alt)
        if color:
            append_list(props, "szín", [color])
        if old_alt == "Tokaji borkülönlegesség":
            append_list(props, "borstílus", ["tokaji borkülönlegesség"])
    elif old_alk == "Habzó-, gyöngyözőbor, boralapú ital":
        if old_alt == "Ízesített boralapú ital":
            append_list(props, "bortípus", ["boralapú ital"])
            props["ízesített"] = True
        elif old_alt == "Gyöngyözőbor":
            append_list(props, "bortípus", ["gyöngyözőbor"])
        else:
            append_list(props, "bortípus", ["alkoholmentes habzó ital"])
    elif old_alk == "Pezsgő":
        append_list(props, "bortípus", ["prosecco" if old_alt == "Prosecco" else "pezsgő"])

    if old_alk == "Sör":
        beer_type = "sör"
        if old_alt == "Malátaital":
            beer_type = "malátaital"
        elif old_alt == "Alkoholmentes radler" or "radler" in product_text(product):
            beer_type = "radler"
        elif old_alt == "Sörválogatás":
            beer_type = "sörválogatás"
        append_list(props, "terméktípus", [beer_type])
        if old_alt == "Ízesített sör":
            props["ízesített"] = True
        elif old_alt == "Világos sör":
            append_list(props, "szín", ["világos"])
        elif old_alt == "Barna sör":
            append_list(props, "szín", ["barna"])
        elif old_alt == "Búzasör":
            append_list(props, "sörtípus", ["búzasör"])
        elif old_alt == "IPA / Ale":
            text = product_text(product)
            additions: list[str] = []
            if "ipa" in text:
                additions.append("IPA")
            if re.search(r"\bale\b", text):
                additions.append("ale")
            append_list(props, "sörtípus", additions or ["felsőerjesztésű sör"])
        if "sörtípus" in props:
            props["sörtípus"] = [
                value
                for value in dedupe(values_of(props["sörtípus"]))
                if fold_text(value) not in {"szuretlen", "izesitett sor"}
            ]
            if not props["sörtípus"]:
                del props["sörtípus"]
    elif old_alk == "Cider":
        append_list(props, "terméktípus", ["cider"])

    if old_alk == "Gyümölcslé":
        if old_alt == "100% gyümölcslé":
            append_list(props, "lé típusa", ["gyümölcslé"])
            append_list(props, "gyümölcstartalom", ["100%"])
        elif old_alt == "Vegyes gyümölcs- és zöldséglé":
            append_list(props, "lé típusa", ["gyümölcslé", "zöldséglé"])
        elif old_alt == "Zöldséglé":
            append_list(props, "lé típusa", ["zöldséglé"])
        elif old_alt == "Gyümölcspüré":
            append_list(props, "forma", ["püré"])
    elif old_path == ("Üdítőital", "Smoothie"):
        append_list(props, "forma", ["smoothie"])
    elif old_path == ("Üdítőital", "Gyerekital"):
        append_list(props, "célcsoport", ["gyerek"])

    if old_path == ("Funkcionális ital", "Shot ital"):
        append_list(props, "forma", ["shot"])

    if old_alk == "Növényi ital":
        source_base = PLANT_BASE_BY_ALT.get(old_alt)
        if source_base:
            append_list(props, "alap", [source_base])

    coffee_form = {
        "Őrölt kávé": "őrölt",
        "Szemes kávé": "szemes",
        "Instant kávé": "instant",
        "Kávékapszula": "kapszula",
        "Cappuccino italpor": "instant italpor",
        "2in1, 3in1 instant kávé": "instant italpor",
    }.get(old_alt)
    if old_alk == "Kávé, tea, kakaó (száraz)" and coffee_form:
        append_list(props, "forma", [coffee_form])
        if old_alt == "Cappuccino italpor":
            append_list(props, "kávékeverék típusa", ["cappuccino"])
        elif old_alt == "2in1, 3in1 instant kávé":
            text = product_text(product)
            kind = "2in1" if "2in1" in text or "2 az 1" in text else "3in1" if "3in1" in text or "3 az 1" in text else "instant kávékeverék"
            append_list(props, "kávékeverék típusa", [kind])

    tea_type = {
        "Gyümölcstea": "gyümölcstea",
        "Rooibos tea": "rooibos tea",
        "Gyógytea": "gyógytea",
        "Fekete tea": "fekete tea",
        "Zöld tea": "zöld tea",
    }.get(old_alt)
    if old_alk == "Kávé, tea, kakaó (száraz)" and tea_type:
        append_list(props, "teatípus", [tea_type])
    if "teatípus" in props:
        normalized_tea = [
            "rooibos tea" if fold_text(value) == "rooibos" else value
            for value in values_of(props["teatípus"])
        ]
        specific = [value for value in dedupe(normalized_tea) if fold_text(value) != "tea"]
        props["teatípus"] = specific or ["tea"]

    if old_alk == "Kávé, tea, kakaó (száraz)":
        if old_alt == "Kakaó italpor":
            append_list(props, "terméktípus", ["kakaóitalpor"])
            append_list(props, "forma", ["italpor"])
        elif old_alt == "Forró csokoládé italpor":
            append_list(props, "terméktípus", ["forró csokoládé"])
            append_list(props, "forma", ["italpor"])
        elif old_alt == "Kakaópor":
            append_list(props, "terméktípus", ["kakaópor"])
            append_list(props, "forma", ["por"])
        elif old_alt == "Kávé ízesítők / tejek / tejporok":
            append_list(props, "terméktípus", ["kávéfehérítő vagy tejpor"])


def transform_citrus_product(product: dict[str, Any], old_path: tuple[str, str]) -> None:
    old_props = product.get("tulajdonsagok") or {}
    name_folded = fold_text(product_name(product))
    flavors = [
        str(value)
        for value in values_of(old_props.get("íz"))
        if fold_text(value) in {"citrom", "lime", "narancs", "gyomber", "menta"}
    ]
    if product_id(product) == FRUIT_STEP_GINGER_ID:
        product_type = "citrusízesítő"
    elif old_path[1] == "Citromízesítő" or "izesito" in name_folded:
        product_type = "citrusízesítő"
    elif (
        "narancs" in name_folded
        or "naracs" in name_folded
        or any(fold_text(value) == "narancs" for value in flavors)
    ):
        product_type = "narancslé-koncentrátum"
    elif "limele" in name_folded or ("lime" in name_folded and "citrom" not in name_folded):
        product_type = "limelé"
    elif "gyomberle" in name_folded:
        product_type = "gyömbér-citromlé"
    else:
        product_type = "citromlé"
    content = [
        normalized
        for value in values_of(old_props.get("gyümölcstartalom"))
        if (normalized := normalize_percent_value(value)) is not None
        and percent_number(normalized) is not None
    ]
    new_props: dict[str, Any] = {}
    brand = old_props.get("márka")
    if isinstance(brand, str) and brand.strip():
        new_props["márka"] = brand
    new_props["terméktípus"] = [product_type]
    new_props["gyümölcs"] = dedupe(flavors or ["citrom"])
    if content:
        new_props["citruslé-tartalom"] = dedupe(content)
    # A célfőkategóriában a kiszerelés a csomagolás alakja, nem a méret.
    # A mennyiség az eredeti termékmezőkben változatlanul megmarad.
    new_props["kiszerelés"] = (
        "tasak" if product_id(product) == FRUIT_STEP_GINGER_ID else "flakon"
    )
    new_props["forma"] = ["folyadék"]
    product["fokategoria"], product["alkategoria"], product["altipus"] = CITRUS_TARGET
    product["tulajdonsagok"] = new_props


def transform_nesquik(product: dict[str, Any]) -> None:
    product["fokategoria"], product["alkategoria"], product["altipus"] = NESQUIK_TARGET
    product["tulajdonsagok"] = {
        "márka": "Nesquik",
        "terméktípus": ["szirup"],
        "íz": ["kakaó"],
    }


def normalize_atomic_semantics(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    """A migráció által érintett, még összetett értékeket elemi értékekre bontja."""

    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        props = product.get("tulajdonsagok") or {}

        juice_types = values_of(props.get("lé típusa"))
        if any(fold_text(value) == "gyumolcs es zoldsegle" for value in juice_types):
            props["lé típusa"] = dedupe(
                [
                    atom
                    for value in juice_types
                    for atom in (
                        ["gyümölcslé", "zöldséglé"]
                        if fold_text(value) == "gyumolcs es zoldsegle"
                        else [value]
                    )
                ]
            )
            operations["összetett_létípus_atomokra_bontva"] += 1

        product_types = values_of(props.get("terméktípus"))
        if any(
            fold_text(value) == "kavefeherito vagy tejpor"
            for value in product_types
        ):
            name = fold_text(product_name(product))
            if "kavetejszin" in name:
                product_type = "kávétejszín"
            elif "tejpor" in name:
                product_type = "tejpor"
            else:
                product_type = "kávéfehérítő"
            props["terméktípus"] = [product_type]
            # A régi gyűjtőkategória minden termékre rámásolt, emiatt
            # félrevezető és a fenti atomi típussal redundáns tengelyei.
            props.pop("fajta", None)
            props.pop("típus", None)
            operations["kávéadalék_típusa_atomizálva"] += 1

        if props.get("márka") == "Katona Nálad Vagy Nálam":
            props["márka"] = "Katona"
            append_list(props, "változat", ["Nálad Vagy Nálam"])
            operations["márka_főmárkára_egyszerűsítve"] += 1


def normalize_external_targets(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    """A két Italból kimozgatott célág bizonyított szemantikai javításai."""

    for product in products:
        if (
            product_id(product) == CITRIORANGE_ID
            and (
                product.get("fokategoria"),
                product.get("alkategoria"),
                product.get("altipus"),
            )
            == CITRUS_TARGET
        ):
            props = product.get("tulajdonsagok") or {}
            expected = ["narancslé-koncentrátum"]
            if props.get("terméktípus") != expected:
                props["terméktípus"] = expected
                operations["Citriorange_narancslé_típusa_javítva"] += 1
        if (
            product_id(product) == FRUIT_STEP_GINGER_ID
            and (
                product.get("fokategoria"),
                product.get("alkategoria"),
                product.get("altipus"),
            )
            == CITRUS_TARGET
        ):
            props = product.get("tulajdonsagok") or {}
            if props.get("terméktípus") != ["citrusízesítő"]:
                props["terméktípus"] = ["citrusízesítő"]
                operations["Fruit_Step_összetett_típusa_atomizálva"] += 1
            if props.get("kiszerelés") != "tasak":
                props["kiszerelés"] = "tasak"
                operations["Fruit_Step_csomagolása_javítva"] += 1


PACKAGING_CANONICAL = {
    "palack": "palack",
    "pet palack": "PET-palack",
    "doboz": "doboz",
    "uveg": "üveg",
    "tasak": "tasak",
    "zacsko": "zacskó",
    "flakon": "flakon",
    "tubus": "tubus",
    "adagcsomagolt": "adagcsomagolt",
    "csomag": "csomag",
    "karton": "karton",
    "rekesz": "rekesz",
    "hordo": "hordó",
    "kanna": "kanna",
    "kapszula": "kapszula",
    "kaveparna": "kávépárna",
    "utantolto tasak": "utántöltő tasak",
    "vakuumcsomagolas": "vákuumcsomagolás",
    "aromazaro csomagolas": "aromazáró csomagolás",
    "multipack": "multipack",
}


def final_quantity_from_source(product: dict[str, Any]) -> str | None:
    item = product.get("termek") or {}
    amount = str(item.get("vegso_mennyiseg") or "").strip()
    unit = str(item.get("vegso_egyseg") or "").strip()
    if not amount or not unit:
        return None
    if not re.fullmatch(r"\d+(?:[.,]\d+)?", amount):
        return None
    number = amount.replace(".", ",")
    if number.endswith(",0"):
        number = number[:-2]
    return f"{number} {unit}"


def normalize_size_and_packaging(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    """A mennyiséget és a fizikai csomagolást külön, elemi tengelyre teszi."""

    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        props = product.get("tulajdonsagok") or {}
        path = (
            str(product.get("alkategoria") or ""),
            str(product.get("altipus") or ""),
        )
        name_folded = fold_text(product_name(product))
        before_size = copy.deepcopy(props.get("kiszerelés"))
        before_packaging = copy.deepcopy(props.get("csomagolás"))
        size_candidates: list[Any] = []
        packaging: list[str] = []

        def accept_packaging(value: Any) -> None:
            folded = fold_text(value)
            if folded in {"", "nem jelolt", "egyeb"}:
                return
            if folded == "filter":
                if path == (HOT_BRANCH, "Tea"):
                    append_list(props, "forma", ["filteres"])
                return
            if folded == "szalas":
                if path == (HOT_BRANCH, "Tea"):
                    append_list(props, "forma", ["szálas"])
                return
            if any(char.isdigit() for char in str(value)):
                return
            canonical = PACKAGING_CANONICAL.get(folded, str(value))
            if (
                canonical == "palack"
                and (
                    path[0] == HOT_BRANCH
                    or path == (BASE_BRANCH, "Italpor és tabletta")
                )
            ):
                return
            packaging.append(canonical)

        for value in values_of(props.get("kiszerelés")):
            folded = fold_text(value)
            if (
                folded in PACKAGING_CANONICAL
                or folded in {"filter", "szalas", "nem jelolt", "egyeb"}
            ):
                accept_packaging(value)
            else:
                size_candidates.append(value)
        for value in values_of(props.get("csomagolás")):
            accept_packaging(value)

        size_candidates = dedupe(size_candidates)
        selected_size: Any | None = None
        if size_candidates:
            multipack_sizes = [
                value
                for value in size_candidates
                if re.search(r"\b\d+\s*x\s*\d+", fold_text(value))
            ]
            selected_size = multipack_sizes[-1] if multipack_sizes else size_candidates[0]
            if re.search(r"\b\d+\s*x\s*\d+", name_folded):
                selected_size = final_quantity_from_source(product) or selected_size
        if selected_size is None:
            props.pop("kiszerelés", None)
        else:
            props["kiszerelés"] = selected_size

        packaging = dedupe(packaging)
        if packaging:
            props["csomagolás"] = packaging
        else:
            props.pop("csomagolás", None)

        if before_size != props.get("kiszerelés"):
            operations["kiszerelés_egyértékű_mennyiséggé_tisztítva"] += 1
        if before_packaging != props.get("csomagolás"):
            operations["csomagolás_elemi_értékekre_tisztítva"] += 1


def shape_of(value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    if isinstance(value, list):
        return "multi"
    return "single"


def align_shapes_within_paths(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    ital_products = [product for product in products if product.get("fokategoria") == ITAL]
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in ital_products:
        grouped[(str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))].append(product)
    force_single = {
        "márka",
        "energia tartalom",
        "szénsavasság",
        "alkoholstátusz",
        "kiszerelés",
    }
    for path_products in grouped.values():
        raw_by_prop: dict[str, list[Any]] = defaultdict(list)
        for product in path_products:
            for prop_name, value in (product.get("tulajdonsagok") or {}).items():
                raw_by_prop[prop_name].append(value)
        target_shapes: dict[str, str] = {}
        for prop_name, raw_values in raw_by_prop.items():
            shapes = {shape_of(value) for value in raw_values}
            if shapes == {"flag"}:
                target_shapes[prop_name] = "flag"
            elif prop_name in force_single:
                target_shapes[prop_name] = "single"
            elif "multi" in shapes:
                target_shapes[prop_name] = "multi"
            else:
                target_shapes[prop_name] = "single"
        for product in path_products:
            props = product.get("tulajdonsagok") or {}
            for prop_name, value in list(props.items()):
                target = target_shapes[prop_name]
                actual = shape_of(value)
                if actual == target:
                    continue
                if target == "multi":
                    props[prop_name] = dedupe(values_of(value))
                elif target == "single":
                    atoms = dedupe(values_of(value))
                    if len(atoms) != 1:
                        raise RuntimeError(
                            f"Nem tehető skalárrá: {product_id(product)} / {prop_name} / {atoms}"
                        )
                    props[prop_name] = atoms[0]
                else:
                    raise RuntimeError(
                        f"Nem logikai alakú érték: {product_id(product)} / {prop_name} / {value!r}"
                    )
                operations["útvonalon_belüli_típus_egységesítve"] += 1


def canonicalize_equivalent_values_within_paths(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    """Azonos jelentésű írásmódokhoz útvonalanként egyetlen pontos értéket választ."""

    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") == ITAL:
            grouped[
                (
                    str(product.get("alkategoria") or ""),
                    str(product.get("altipus") or ""),
                )
            ].append(product)

    for path_products in grouped.values():
        representatives: dict[str, dict[str, Any]] = defaultdict(dict)
        for product in path_products:
            for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
                if isinstance(raw_value, bool):
                    continue
                for value in values_of(raw_value):
                    marker = f"{type(value).__name__}:{fold_text(value)}"
                    representatives[prop_name].setdefault(marker, value)

        for product in path_products:
            props = product.get("tulajdonsagok") or {}
            for prop_name, raw_value in list(props.items()):
                if isinstance(raw_value, bool):
                    continue
                if isinstance(raw_value, list):
                    normalized: list[Any] = []
                    seen: set[str] = set()
                    for value in raw_value:
                        marker = f"{type(value).__name__}:{fold_text(value)}"
                        if marker in seen:
                            continue
                        seen.add(marker)
                        normalized.append(representatives[prop_name][marker])
                    if normalized != raw_value:
                        props[prop_name] = normalized
                        operations["útvonalon_belüli_értékírásmód_egységesítve"] += 1
                else:
                    marker = f"{type(raw_value).__name__}:{fold_text(raw_value)}"
                    normalized = representatives[prop_name][marker]
                    if normalized != raw_value:
                        props[prop_name] = normalized
                        operations["útvonalon_belüli_értékírásmód_egységesítve"] += 1


def build_prop_block(
    products: list[dict[str, Any]],
    *,
    exclude: frozenset[str] = frozenset(),
) -> dict[str, dict[str, Any]]:
    raw_by_prop: dict[str, list[Any]] = defaultdict(list)
    values_by_prop: dict[str, list[Any]] = defaultdict(list)
    for product in products:
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            if prop_name in exclude:
                continue
            raw_by_prop[prop_name].append(raw_value)
            values_by_prop[prop_name].extend(values_of(raw_value))
    block: dict[str, dict[str, Any]] = {"egyedi": {}, "csoportos": {}}
    for prop_name in sorted(raw_by_prop, key=fold_text):
        shapes = {shape_of(value) for value in raw_by_prop[prop_name]}
        if len(shapes) != 1:
            raise RuntimeError(f"Kevert alak a faépítésnél: {prop_name} / {shapes}")
        shape = next(iter(shapes))
        allowed = sorted(dedupe(values_by_prop[prop_name]), key=fold_text)
        if shape == "flag":
            block["egyedi"][prop_name] = {}
        elif shape == "single":
            block["egyedi"][prop_name] = allowed
        else:
            block["csoportos"][prop_name] = allowed
    return block


def rebuild_ital_tree(categories: dict[str, Any], products: list[dict[str, Any]]) -> None:
    by_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        by_path[path].append(product)
    if set(by_path) != set(TARGET_PATHS):
        missing = sorted(TARGET_PATHS - set(by_path))
        unexpected = sorted(set(by_path) - TARGET_PATHS)
        raise RuntimeError(f"Célút-paritási hiba: missing={missing}, unexpected={unexpected}")
    alks: dict[str, Any] = {}
    for alkategoria, altipusok in TARGET_HIERARCHY.items():
        node = {
            PROP_KEY: {"egyedi": {}, "csoportos": {}},
            ALT_KEY: {},
        }
        for altipus in altipusok:
            node[ALT_KEY][altipus] = {
                PROP_KEY: build_prop_block(by_path[(alkategoria, altipus)])
            }
        alks[alkategoria] = node
    categories[ITAL] = {
        PROP_KEY: {"egyedi": {}, "csoportos": {}},
        ALK_KEY: alks,
    }


def hoist_leaf_properties(
    parent_node: dict[str, Any],
    leaf_name: str,
    property_names: frozenset[str],
) -> None:
    """A levél ismételt deklarációit a szülőbe emeli, értékvesztés nélkül."""

    leaf_node = parent_node[ALT_KEY][leaf_name]
    parent_props = parent_node.setdefault(PROP_KEY, {"egyedi": {}, "csoportos": {}})
    leaf_props = leaf_node.setdefault(PROP_KEY, {"egyedi": {}, "csoportos": {}})

    for prop_name in property_names:
        parent_group = next(
            (
                group_name
                for group_name in ("egyedi", "csoportos")
                if prop_name in (parent_props.get(group_name) or {})
            ),
            None,
        )
        leaf_group = next(
            (
                group_name
                for group_name in ("egyedi", "csoportos")
                if prop_name in (leaf_props.get(group_name) or {})
            ),
            None,
        )
        if leaf_group is None:
            continue
        if parent_group is None:
            parent_props.setdefault(leaf_group, {})[prop_name] = copy.deepcopy(
                leaf_props[leaf_group][prop_name]
            )
        else:
            if parent_group != leaf_group:
                raise RuntimeError(
                    f"Eltérő örökölt alak: {leaf_name} / {prop_name} / "
                    f"{parent_group} != {leaf_group}"
                )
            parent_declaration = parent_props[parent_group][prop_name]
            leaf_declaration = leaf_props[leaf_group][prop_name]
            if isinstance(parent_declaration, dict) or isinstance(leaf_declaration, dict):
                if parent_declaration != {} or leaf_declaration != {}:
                    raise RuntimeError(
                        f"Hibás logikai deklaráció: {leaf_name} / {prop_name}"
                    )
            else:
                # Pontos érték szerint egyesítünk: ezzel a meglévő, nem Ital
                # termékek deklarált értékei is változatlanul érvényesek maradnak.
                for value in leaf_declaration:
                    if value not in parent_declaration:
                        parent_declaration.append(value)
        del leaf_props[leaf_group][prop_name]


def rebuild_nesquik_target(categories: dict[str, Any]) -> None:
    root = categories[NESQUIK_TARGET[0]]
    parent_node = root[ALK_KEY][NESQUIK_TARGET[1]]
    hoist_leaf_properties(
        parent_node,
        NESQUIK_TARGET[2],
        frozenset({"márka", "íz"}),
    )


def rebuild_citrus_target(categories: dict[str, Any], products: list[dict[str, Any]]) -> None:
    root = categories[CITRUS_TARGET[0]]
    alk_node = root[ALK_KEY][CITRUS_TARGET[1]]
    alts = alk_node[ALT_KEY]
    if CITRUS_OLD_TARGET[2] in alts and CITRUS_TARGET[2] not in alts:
        old_order = list(alts)
        renamed: dict[str, Any] = {}
        for name in old_order:
            renamed[CITRUS_TARGET[2] if name == CITRUS_OLD_TARGET[2] else name] = alts[name]
        alk_node[ALT_KEY] = alts = renamed
    citrus_products = [
        product
        for product in products
        if (
            product.get("fokategoria"),
            product.get("alkategoria"),
            product.get("altipus"),
        )
        == CITRUS_TARGET
    ]
    if len(citrus_products) != 65:
        raise RuntimeError(f"Nem 65 citrusrekord került célra: {len(citrus_products)}")
    alts[CITRUS_TARGET[2]] = {
        PROP_KEY: build_prop_block(
            citrus_products,
            exclude=frozenset({"márka", "kiszerelés"}),
        )
    }
    leaf_props = alts[CITRUS_TARGET[2]][PROP_KEY]
    leaf_props["egyedi"]["márka"] = sorted(
        {
            product["tulajdonsagok"]["márka"]
            for product in citrus_products
            if isinstance((product.get("tulajdonsagok") or {}).get("márka"), str)
        },
        key=fold_text,
    )
    hoist_leaf_properties(
        alk_node,
        CITRUS_TARGET[2],
        frozenset({"márka"}),
    )


def effective_declarations(
    categories: dict[str, Any],
    path: tuple[str, str, str],
) -> tuple[dict[str, str], dict[str, list[Any]], list[str]]:
    fokategoria, alkategoria, altipus = path
    root = categories.get(fokategoria)
    if not isinstance(root, dict):
        return {}, {}, [f"hiányzó főkategória: {fokategoria}"]
    alk_node = (root.get(ALK_KEY) or {}).get(alkategoria)
    if not isinstance(alk_node, dict):
        return {}, {}, [f"hiányzó alkategória: {path}"]
    alt_node = (alk_node.get(ALT_KEY) or {}).get(altipus)
    if not isinstance(alt_node, dict):
        return {}, {}, [f"hiányzó altípus: {path}"]
    shapes: dict[str, str] = {}
    allowed: dict[str, list[Any]] = {}
    errors: list[str] = []
    for node in (root, alk_node, alt_node):
        props = node.get(PROP_KEY) or {}
        local: dict[str, tuple[str, list[Any]]] = {}
        for name, declaration in (props.get("egyedi") or {}).items():
            local[name] = ("flag" if isinstance(declaration, dict) else "single", [] if isinstance(declaration, dict) else declaration)
        for name, declaration in (props.get("csoportos") or {}).items():
            local[name] = ("multi", declaration)
        for name, (shape, values) in local.items():
            if name in shapes:
                errors.append(f"újradefiniált tulajdonság: {path} / {name}")
            shapes[name] = shape
            allowed[name] = values
    return shapes, allowed, errors


def validate_candidate(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if len(products) != EXPECTED_TOTAL_PRODUCTS:
        errors.append(f"termékszám={len(products)}")
    ital_products = [product for product in products if product.get("fokategoria") == ITAL]
    if len(ital_products) != EXPECTED_TARGET_ITAL_PRODUCTS:
        errors.append(f"Ital-termékszám={len(ital_products)}")
    used_paths = {
        (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        for product in ital_products
    }
    if used_paths != set(TARGET_PATHS):
        errors.append("Ital-útvonalparitás")
    if any(not product.get("altipus") for product in ital_products):
        errors.append("üres Ital-altípus")

    declaration_cache: dict[tuple[str, str], tuple[dict[str, str], dict[str, list[Any]]]] = {}
    type_errors: list[Any] = []
    value_errors: list[Any] = []
    declaration_errors: list[Any] = []
    hash_errors: list[str] = []
    for product in ital_products:
        path2 = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        if path2 not in declaration_cache:
            shapes, allowed, local_errors = effective_declarations(
                categories, (ITAL, path2[0], path2[1])
            )
            declaration_cache[path2] = (shapes, allowed)
            declaration_errors.extend(local_errors)
        shapes, allowed = declaration_cache[path2]
        for prop_name, value in (product.get("tulajdonsagok") or {}).items():
            if prop_name not in shapes:
                value_errors.append([product_id(product), path2, prop_name, "nincs deklarálva"])
                continue
            if shape_of(value) != shapes[prop_name]:
                type_errors.append(
                    [product_id(product), path2, prop_name, shapes[prop_name], shape_of(value)]
                )
            declared_values = allowed.get(prop_name) or []
            if declared_values:
                permitted = {fold_text(item) for item in declared_values}
                missing = [
                    item
                    for item in values_of(value)
                    if fold_text(item) not in permitted
                ]
                if missing:
                    value_errors.append([product_id(product), path2, prop_name, missing])
        if product.get("kategoria_hash") != category_hash(product):
            hash_errors.append(product_id(product))

    alcohol_errors: list[Any] = []
    for product in ital_products:
        if product.get("alkategoria") != ALCOHOL_BRANCH:
            continue
        props = product.get("tulajdonsagok") or {}
        status = props.get("alkoholstátusz")
        if status not in {"alkoholos", "alkoholmentes"}:
            alcohol_errors.append([product_id(product), "status", status])
            continue
        numbers = [
            number
            for value in values_of(props.get("alkoholtartalom"))
            if (number := percent_number(value)) is not None
        ]
        categorical = [
            value
            for value in values_of(props.get("alkoholtartalom"))
            if fold_text(value) in {"alkoholos", "egyeb"}
        ]
        if categorical:
            alcohol_errors.append([product_id(product), "kategorikus", categorical])
        if status == "alkoholmentes" and any(number > 0.5 for number in numbers):
            alcohol_errors.append([product_id(product), "alkoholmentes_abv", numbers])
        if status == "alkoholos" and numbers and not any(number > 0.5 for number in numbers):
            alcohol_errors.append([product_id(product), "alkoholos_abv", numbers])

    carbonation_errors: list[Any] = []
    for product in ital_products:
        path2 = (product.get("alkategoria"), product.get("altipus"))
        value = (product.get("tulajdonsagok") or {}).get("szénsavasság")
        if path2 in {(SOFT_BRANCH, "Kóla"), (SOFT_BRANCH, "Tonik")} and value != "szénsavas":
            carbonation_errors.append([product_id(product), path2, value])
        if product.get("alkategoria") == WATER_BRANCH and (
            not isinstance(value, str)
            or value not in {
                "szénsavmentes",
                "szénsavas",
                "enyhén szénsavas",
                "extra szénsavas",
            }
        ):
            carbonation_errors.append([product_id(product), path2, value])

    nesquik = [product for product in products if product_id(product) == NESQUIK_ID]
    if len(nesquik) != 1 or (
        nesquik[0].get("fokategoria"),
        nesquik[0].get("alkategoria"),
        nesquik[0].get("altipus"),
    ) != NESQUIK_TARGET:
        errors.append("Nesquik-célút")
    elif nesquik[0].get("kategoria_hash") != category_hash(nesquik[0]):
        errors.append("Nesquik-hash")

    citrus = [
        product
        for product in products
        if (
            product.get("fokategoria"),
            product.get("alkategoria"),
            product.get("altipus"),
        )
        == CITRUS_TARGET
    ]
    if len(citrus) != 65:
        errors.append(f"citrus-célszám={len(citrus)}")
    citrus_hash_errors = [
        product_id(product)
        for product in citrus
        if product.get("kategoria_hash") != category_hash(product)
    ]

    if declaration_errors:
        errors.append("deklarációs hiba")
    if type_errors:
        errors.append("tulajdonságtípus-hiba")
    if value_errors:
        errors.append("megengedettérték-hiba")
    if hash_errors:
        errors.append("Ital-hash-hiba")
    if alcohol_errors:
        errors.append("alkoholstátusz-hiba")
    if carbonation_errors:
        errors.append("szénsavasság-hiba")
    if citrus_hash_errors:
        errors.append("citrus-hash-hiba")
    return {
        "status": "ok" if not errors else "hiba",
        "errors": errors,
        "counts": {
            "total_products": len(products),
            "ital_products": len(ital_products),
            "ital_paths": len(used_paths),
            "ital_parent_categories": len(TARGET_HIERARCHY),
            "citrus_moved": len(citrus),
        },
        "details": {
            "declaration_errors": declaration_errors[:50],
            "type_errors": type_errors[:50],
            "value_errors": value_errors[:50],
            "hash_errors": hash_errors[:50],
            "alcohol_errors": alcohol_errors[:50],
            "carbonation_errors": carbonation_errors[:50],
            "citrus_hash_errors": citrus_hash_errors[:50],
        },
    }


def run_checker(products_path: Path, categories_path: Path) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(CHECKER_PATH),
            "--products",
            str(products_path),
            "--categories",
            str(categories_path),
        ],
        cwd=str(BASE),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Az ellenőrző nem JSON-kimenetet adott (exit={completed.returncode}): "
            f"{completed.stdout[-2000:]} {completed.stderr[-2000:]}"
        ) from exc
    if completed.returncode != 0 or payload.get("status") != "ok":
        raise RuntimeError(
            f"A külön ellenőrző hibát jelzett (exit={completed.returncode}): "
            f"{json.dumps(payload, ensure_ascii=False)}"
        )
    return payload


def transaction_artifacts() -> tuple[Path, Path, Path, Path]:
    return (
        RESULT_PATH.with_name(RESULT_PATH.name + ".ital-tree-stage"),
        CATEGORY_PATH.with_name(CATEGORY_PATH.name + ".ital-tree-stage"),
        RESULT_PATH.with_name(RESULT_PATH.name + ".pre-ital-tree.bak"),
        CATEGORY_PATH.with_name(CATEGORY_PATH.name + ".pre-ital-tree.bak"),
    )


def recover_interrupted_transaction() -> bool:
    """Egy korábban félbeszakadt kétfájlos csere biztonságos helyreállítása."""

    result_stage, category_stage, result_backup, category_backup = transaction_artifacts()
    stages = (result_stage, category_stage)
    backups = (result_backup, category_backup)
    existing_backups = [path for path in backups if path.exists()]

    if existing_backups:
        if len(existing_backups) == 2:
            shutil.copy2(result_backup, RESULT_PATH)
            shutil.copy2(category_backup, CATEGORY_PATH)
        else:
            # Ez tipikusan a már sikeresen ellenőrzött csere utáni
            # backup-takarítás megszakadását jelenti. Csak a teljes jelenlegi
            # fájlpár sikeres ellenőrzése esetén fogadjuk el.
            run_checker(RESULT_PATH, CATEGORY_PATH)
        for path in (*stages, *backups):
            if path.exists():
                path.unlink()
        return True

    recovered = False
    for path in stages:
        if path.exists():
            path.unlink()
            recovered = True
    return recovered


def write_transactionally(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
) -> dict[str, Any]:
    result_stage, category_stage, result_backup, category_backup = transaction_artifacts()
    auxiliaries = (result_stage, category_stage, result_backup, category_backup)
    leftovers = [str(path) for path in auxiliaries if path.exists()]
    if leftovers:
        raise RuntimeError(f"Korábbi staging/backup fájl maradt vissza: {leftovers}")
    try:
        dump_json(result_stage, products)
        dump_json(category_stage, categories)
        stage_check = run_checker(result_stage, category_stage)
        shutil.copy2(RESULT_PATH, result_backup)
        shutil.copy2(CATEGORY_PATH, category_backup)
        try:
            result_stage.replace(RESULT_PATH)
            category_stage.replace(CATEGORY_PATH)
            final_check = run_checker(RESULT_PATH, CATEGORY_PATH)
        except BaseException:
            if result_backup.exists():
                shutil.copy2(result_backup, RESULT_PATH)
            if category_backup.exists():
                shutil.copy2(category_backup, CATEGORY_PATH)
            raise
        else:
            result_backup.unlink()
            category_backup.unlink()
            return {"stage": stage_check, "final": final_check}
    finally:
        for path in (result_stage, category_stage):
            if path.exists():
                path.unlink()


def markdown_report(payload: dict[str, Any]) -> str:
    before = payload["before"]
    after = payload["after"]
    lines = [
        "# Ital kategóriafa átalakítása – 2026-07-23",
        "",
        "## Eredmény",
        "",
        f"- Ital-termékek: **{before['ital_products']} → {after['ital_products']}**",
        f"- Használt Ital-útvonalak: **{before['paths']} → {after['paths']}**",
        f"- Második szintű Ital-kategóriák: **{before['parent_categories']} → {after['parent_categories']}**",
        "- Minden Ital-termék név szerinti harmadik szintű levélen van.",
        "- A szénsavasság, alkoholstátusz, sör-/bor-/teatípus, célcsoport és növényi alap tulajdonságként marad meg.",
        "- A kategóriafa, a termékutak, az értékalakok, az engedélyezett értékek és a termékhash-ek paritása ellenőrzött.",
        "",
        "## Új kategóriafa",
        "",
    ]
    for alkategoria, altipusok in TARGET_HIERARCHY.items():
        lines.append(f"- **{alkategoria}**")
        for altipus in altipusok:
            count = payload["after"]["path_counts"].get(f"{alkategoria} > {altipus}", 0)
            lines.append(f"  - {altipus}: {count}")
    lines.extend(
        [
            "",
            "## Kikerült hibás vagy nem italjellegű termékek",
            "",
            f"- 65 citruslé/citrusízesítő → `{CITRUS_TARGET[0]} > {CITRUS_TARGET[1]} > {CITRUS_TARGET[2]}`",
            f"- Nesquik kakaós szirup (`{NESQUIK_ID}`) → `{NESQUIK_TARGET[0]} > {NESQUIK_TARGET[1]} > {NESQUIK_TARGET[2]}`",
            "",
            "## Ellenőrzés",
            "",
            f"- Belső candidate-validáció: `{payload['validation']['status']}`",
            f"- Független ellenőrző: `{payload['checker']['final']['status']}`",
            f"- Forrásút-lefedés: `{payload['source_route_coverage']}/89`",
            f"- Futtatás módja: `{payload['mode']}`",
            "",
        ]
    )
    if payload["conflicts"]:
        lines.extend(
            [
                "## Automatikusan feloldott ellentmondások",
                "",
                f"Összesen {len(payload['conflicts'])} eset. A teljes lista a gépi audit JSON-ban található.",
                "",
            ]
        )
    return "\n".join(lines)


def path_counts(products: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(
        f"{product.get('alkategoria') or ''} > {product.get('altipus') or '(nincs altípus)'}"
        for product in products
        if product.get("fokategoria") == ITAL
    )
    return dict(sorted(counts.items(), key=lambda row: fold_text(row[0])))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="A két fő JSON-fájl tranzakciós visszaírása")
    args = parser.parse_args()

    if not CHECKER_PATH.is_file():
        raise RuntimeError(f"Hiányzó ellenőrző: {CHECKER_PATH}")
    if args.apply:
        recover_interrupted_transaction()
    else:
        leftovers = [str(path) for path in transaction_artifacts() if path.exists()]
        if leftovers:
            raise RuntimeError(
                "Félbeszakadt tranzakció nyoma maradt; a helyreállításhoz "
                f"futtasd --apply kapcsolóval: {leftovers}"
            )
    products = load_json(RESULT_PATH)
    categories = load_json(CATEGORY_PATH)
    if not isinstance(products, list) or len(products) != EXPECTED_TOTAL_PRODUCTS:
        raise RuntimeError(f"Váratlan termékgyűjtemény: {type(products).__name__}, {len(products)}")
    if ITAL not in categories:
        raise RuntimeError("Hiányzik az Ital főkategória")

    original_products = copy.deepcopy(products)
    original_categories = copy.deepcopy(categories)
    original_ital = [product for product in products if product.get("fokategoria") == ITAL]
    observed_paths = frozenset(
        (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        for product in original_ital
    )
    if observed_paths == SOURCE_PATHS and len(original_ital) == EXPECTED_SOURCE_ITAL_PRODUCTS:
        mode = "source-migration"
    elif observed_paths == TARGET_PATHS and len(original_ital) == EXPECTED_TARGET_ITAL_PRODUCTS:
        mode = "target-idempotency-check"
    else:
        raise RuntimeError(
            "Sem a teljes 89 utas forrásfa, sem a teljes 41 utas célfa nem egyezik. "
            f"Ital={len(original_ital)}, utak={len(observed_paths)}, "
            f"forrásból hiányzik={sorted(SOURCE_PATHS - observed_paths)[:20]}, "
            f"váratlan={sorted(observed_paths - SOURCE_PATHS - TARGET_PATHS)[:20]}"
        )

    operations: Counter[str] = Counter()
    conflicts: list[dict[str, Any]] = []
    source_route_transitions: Counter[str] = Counter()
    changed_indices: set[int] = set()

    if mode == "source-migration":
        for index, product in enumerate(products):
            if product.get("fokategoria") != ITAL:
                continue
            before = product_state(product)
            old_path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
            base_target = SOURCE_ROUTES[old_path]
            if len(base_target) == 3:
                transform_citrus_product(product, old_path)
                operations["citrus_alapanyag_ágba_mozgatva"] += 1
                target_label = " > ".join(CITRUS_TARGET)
            else:
                target = special_generic_drink_target(product, old_path, base_target)
                if len(target) == 3:
                    if product_id(product) != NESQUIK_ID:
                        raise RuntimeError(f"Nem várt Italból kimozgatás: {product_id(product)} / {target}")
                    transform_nesquik(product)
                    operations["Nesquik_desszertszósz_ágba_mozgatva"] += 1
                    target_label = " > ".join(NESQUIK_TARGET)
                else:
                    if old_path == ("Alkoholok", "Alkoholmentes szeszesital, koktél"):
                        target = special_spirit_target(product)
                    product["alkategoria"], product["altipus"] = target
                    props = product.setdefault("tulajdonsagok", {})
                    if target[0] == ALCOHOL_BRANCH:
                        status = "alkoholmentes" if old_path in NONALCOHOLIC_SOURCE_PATHS else "alkoholos"
                        normalize_alcohol(
                            props,
                            status,
                            operations,
                            conflicts,
                            product_id(product),
                        )
                    add_source_semantics(product, old_path, operations)
                    normalize_carbonation(product, old_path, operations, conflicts)
                    normalize_energy(props, operations)
                    normalize_caffeine(props, operations)
                    split_coffee_system(product, props, operations)
                    if old_path[0] == "Ásványvíz":
                        props.pop("cukormentes / zero", None)
                    target_label = f"{ITAL} > {target[0]} > {target[1]}"
            source_route_transitions[
                f"{ITAL} > {old_path[0]} > {old_path[1] or '(nincs altípus)'} -> {target_label}"
            ] += 1
            if product_state(product) != before:
                changed_indices.add(index)
    else:
        for index, product in enumerate(products):
            if product.get("fokategoria") != ITAL:
                continue
            before = product_state(product)
            props = product.setdefault("tulajdonsagok", {})
            normalize_carbonation(product, None, operations, conflicts)
            normalize_energy(props, operations)
            normalize_caffeine(props, operations)
            split_coffee_system(product, props, operations)
            if product_state(product) != before:
                changed_indices.add(index)

    normalize_atomic_semantics(products, operations)
    normalize_external_targets(products, operations)
    normalize_size_and_packaging(products, operations)
    align_shapes_within_paths(products, operations)
    canonicalize_equivalent_values_within_paths(products, operations)
    rebuild_ital_tree(categories, products)
    rebuild_nesquik_target(categories)
    rebuild_citrus_target(categories, products)

    for index, product in enumerate(products):
        if product_state(product) != product_state(original_products[index]):
            product["kategoria_hash"] = category_hash(product)
            changed_indices.add(index)

    # Minden eredetileg nem Ital-termék változatlan marad.
    unexpected_non_ital_changes = []
    for index, original in enumerate(original_products):
        if original.get("fokategoria") == ITAL or products[index] == original:
            continue
        original_path = (
            original.get("fokategoria"),
            original.get("alkategoria"),
            original.get("altipus"),
        )
        if product_id(original) == CITRIORANGE_ID and original_path == CITRUS_TARGET:
            continue
        unexpected_non_ital_changes.append(index)
    if unexpected_non_ital_changes:
        raise RuntimeError(f"Nem-Ital termék módosult: {unexpected_non_ital_changes[:20]}")

    # A kategóriafában csak az Ital és a két explicit külső célág változhat.
    original_without_scope = copy.deepcopy(original_categories)
    current_without_scope = copy.deepcopy(categories)
    original_without_scope.pop(ITAL, None)
    current_without_scope.pop(ITAL, None)
    for snapshot in (original_without_scope, current_without_scope):
        root = snapshot[CITRUS_TARGET[0]]
        citrus_parent = root[ALK_KEY][CITRUS_TARGET[1]]
        citrus_parent.pop(PROP_KEY, None)
        citrus_parent[ALT_KEY].pop(CITRUS_OLD_TARGET[2], None)
        citrus_parent[ALT_KEY].pop(CITRUS_TARGET[2], None)
        nesquik_parent = root[ALK_KEY][NESQUIK_TARGET[1]]
        nesquik_parent.pop(PROP_KEY, None)
        nesquik_parent[ALT_KEY].pop(NESQUIK_TARGET[2], None)
    if original_without_scope != current_without_scope:
        raise RuntimeError("A kategóriafa az Ital és a két külső célágon kívül is módosult")

    validation = validate_candidate(products, categories)
    if validation["status"] != "ok":
        print(json.dumps(validation, ensure_ascii=True, indent=2))
        raise RuntimeError(f"A belső validáció hibás: {validation['errors']}")

    before_summary = {
        "ital_products": len(original_ital),
        "paths": len(observed_paths),
        "parent_categories": len((original_categories[ITAL].get(ALK_KEY) or {})),
        "path_counts": path_counts(original_products),
    }
    after_ital = [product for product in products if product.get("fokategoria") == ITAL]
    after_summary = {
        "ital_products": len(after_ital),
        "paths": len(TARGET_PATHS),
        "parent_categories": len(TARGET_HIERARCHY),
        "path_counts": path_counts(products),
    }
    payload: dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "mode": mode,
        "apply": bool(args.apply),
        "source_route_coverage": len(SOURCE_PATHS) if mode == "source-migration" else 89,
        "before": before_summary,
        "after": after_summary,
        "operations": dict(operations),
        "changed_products": len(changed_indices),
        "source_route_transitions": dict(source_route_transitions),
        "conflicts": conflicts,
        "validation": validation,
    }

    if not args.apply:
        print(
            json.dumps(
                {
                    "status": "ok",
                    "mode": mode,
                    "would_change_products": len(changed_indices),
                    "before": {
                        "ital_products": before_summary["ital_products"],
                        "paths": before_summary["paths"],
                        "parent_categories": before_summary["parent_categories"],
                    },
                    "after": {
                        "ital_products": after_summary["ital_products"],
                        "paths": after_summary["paths"],
                        "parent_categories": after_summary["parent_categories"],
                    },
                    "operations": dict(operations),
                    "resolved_conflicts": len(conflicts),
                },
                ensure_ascii=True,
                indent=2,
            )
        )
        return 0

    checker = write_transactionally(products, categories)
    payload["checker"] = checker
    # Az első migráció részletes auditját az idempotenciapróba ne írja felül.
    if mode == "source-migration" or not (AUDIT_PATH.exists() and REPORT_PATH.exists()):
        dump_json(AUDIT_PATH, payload)
        REPORT_PATH.write_text(markdown_report(payload), encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "status": "ok",
                "mode": mode,
                "changed_products": len(changed_indices),
                "ital_products": after_summary["ital_products"],
                "ital_paths": after_summary["paths"],
                "parent_categories": after_summary["parent_categories"],
                "resolved_conflicts": len(conflicts),
                "checker": checker["final"].get("status"),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
