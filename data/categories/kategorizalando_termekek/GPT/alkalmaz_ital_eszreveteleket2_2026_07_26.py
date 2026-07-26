# -*- coding: utf-8 -*-
"""Az ``ital_eszrevetelek2.txt`` szerinti, célzott második Ital-migráció.

A program alapértelmezésben csak memóriában dolgozik. A ``--prepare-only``
kapcsoló külön jelölt JSON-fájlokat ír, majd a független ellenőrzőt is lefuttatja.
A két fő JSON végleges cseréjét szándékosan a PowerShell-finalizáló végzi.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import alkalmaz_italok_eszreveteleket_2026_07_25 as round1

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


BASE = Path(__file__).resolve().parent
RESULT_PATH = BASE / "eredmeny.json"
CATEGORY_PATH = BASE / "kategoriak_2026-06-13.json"
COFFEE_MAP_PATH = BASE / "ital_eszrevetelek2_kave_mapping_2026_07_26.json"
SOFT_MAP_PATH = BASE / "ital_eszrevetelek2_udito_iz_mapping_2026_07_26.json"
CHECKER_PATH = BASE / "ellenoriz_ital_eszreveteleket2_2026_07_26.py"
AUDIT_PATH = BASE / "ital_eszrevetelek2_audit_2026-07-26.json"
CANDIDATE_PRODUCTS_PATH = BASE / ".eredmeny.ital2-20260726.candidate.json"
CANDIDATE_CATEGORIES_PATH = BASE / ".kategoriak.ital2-20260726.candidate.json"

EXPECTED_TOTAL = 47030
ITAL = "Ital"
PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"

WATER = "Ásványvíz"
FLAVORED_WATER = "Ízesített víz"
ENERGY = "Energiaital"
ALCOHOL = "Alkoholos italok és alkoholmentes alternatívák"
SOFT = "Üdítőitalok"
FRUIT = "Gyümölcs- és zöldségitalok"
FUNCTIONAL = "Funkcionális italok"
HOT = "Kávé-, tea- és forrócsokoládé-termékek"
BASES = "Italalapok"

COFFEE_LEAVES = frozenset(
    {"Instant kávé", "Őrölt kávé", "Szemes kávé", "Kapszulás kávé", "Kávé"}
)
SOFT_LEAVES = (
    "Kóla",
    "Tonik",
    "Jegestea",
    "Aloe vera ital",
    "Gyömbér- és gyökéralapú üdítőital",
    "Kombucha",
    "Kölyökpezsgő",
    "Egyéb ízesített üdítőital",
)
FRUIT_LEAVES = ("Lé", "Nektár", "Gyümölcsital", "Smoothie és püréital")
SPORT_LEAF = "Sport-, izotóniás, kollagén- és shot ital"
HOT_LEAVES = ("Kávé", "Tea", "Forró csokoládé", "Krém, tejpor és tejszín")
BASE_LEAVES = (
    "Pezsgőtabletta",
    "Szörp és koncentrátum",
    "Italpor",
    "Tejjel készítendő shake-por",
)

TARGET_HIERARCHY: tuple[tuple[str, tuple[str, ...] | None], ...] = (
    (WATER, None),
    (FLAVORED_WATER, None),
    (ENERGY, None),
    (ALCOHOL, ()),
    (SOFT, SOFT_LEAVES),
    (FRUIT, FRUIT_LEAVES),
    (FUNCTIONAL, (SPORT_LEAF,)),
    (HOT, HOT_LEAVES),
    (BASES, BASE_LEAVES),
)

HAAS_TEA_FLAVORING_IDS = frozenset({"127538:3664736", "203228544"})
SWEETENER_PATH = (
    "Alapanyag, sütés-főzés",
    "Cukor, édesítőszer",
    "Édesítőszer tabletta",
)
COCOA_PATH = (
    "Alapanyag, sütés-főzés",
    "Sütési alapanyag",
    "Kakaópor és kakaós italpor",
)

INSTANT_TEA_IDS = frozenset(
    {
        "2689:2689",
        "BTY-X12565100320021",
        "BTY-X12565300320021",
        "BTY-X12565200320021",
        "BTY-X12221200320021",
        "BTY-X16772400320021",
        "4596140",
        "1e65d083cab394912a83caad",
        "746cc10fdd8ba5107f62f114",
        "105529295",
        "105529298",
    }
)
SNACK_SHAKE_IDS = frozenset(
    {
        "340b600da09ead538e6691cc",
        "b16b51ddb1fd33c6dc930820",
        "70bea15b6e26ebe2e729e339",
        "111276034",
        "111276035",
        "111276036",
    }
)
SNACK_SHAKE_SWEETENER_IDS = frozenset(
    {"70bea15b6e26ebe2e729e339", "111276036"}
)
HELL_ICE_COOL_ID = "BTY-X17299200320021"
SIO_ZERO_APPLE_ID = "4604103"
COFFEE_DECAF_OVERRIDE_IDS = frozenset({"10107032"})

EXPECTED_COUNTS: dict[tuple[str, str, str], int] = {
    (ITAL, WATER, ""): 402,
    (ITAL, FLAVORED_WATER, ""): 262,
    (ITAL, ENERGY, ""): 346,
    (ITAL, FRUIT, "Lé"): 383,
    (ITAL, FRUIT, "Nektár"): 84,
    (ITAL, FRUIT, "Gyümölcsital"): 776,
    (ITAL, FRUIT, "Smoothie és püréital"): 117,
    (ITAL, FUNCTIONAL, SPORT_LEAF): 139,
    (ITAL, HOT, "Kávé"): 1299,
    (ITAL, HOT, "Tea"): 771,
    (ITAL, HOT, "Forró csokoládé"): 33,
    (ITAL, HOT, "Krém, tejpor és tejszín"): 24,
    (ITAL, BASES, "Pezsgőtabletta"): 8,
    (ITAL, BASES, "Szörp és koncentrátum"): 391,
    (ITAL, BASES, "Italpor"): 12,
    (ITAL, BASES, "Tejjel készítendő shake-por"): 6,
}


def load_support_maps() -> tuple[dict[str, Any], dict[str, Any]]:
    if not COFFEE_MAP_PATH.is_file():
        raise RuntimeError(f"Hiányzó kávé-mapping: {COFFEE_MAP_PATH}")
    if not SOFT_MAP_PATH.is_file():
        raise RuntimeError(f"Hiányzó üdítő-mapping: {SOFT_MAP_PATH}")
    coffee_map = round1.load_json(COFFEE_MAP_PATH)
    soft_map = round1.load_json(SOFT_MAP_PATH)
    if not isinstance(coffee_map, dict) or not isinstance(soft_map, dict):
        raise RuntimeError("A mappingfájlok gyökere nem objektum")
    return coffee_map, soft_map


def item_id(product: dict[str, Any]) -> str:
    return round1.product_id(product)


def item_name(product: dict[str, Any]) -> str:
    return round1.product_name(product)


def path_of(product: dict[str, Any]) -> tuple[str, str, str]:
    return round1.path_of(product)


def set_path(product: dict[str, Any], path: tuple[str, str, str]) -> None:
    product["fokategoria"], product["alkategoria"], product["altipus"] = path


def values_of(value: Any) -> list[Any]:
    return round1.values_of(value)


def bool_value(value: Any) -> bool:
    return round1.bool_value(value)


def fold(value: Any) -> str:
    return round1.fold_text(value)


def dedupe(values: list[Any]) -> list[Any]:
    return round1.dedupe(values)


def brand_from(props: dict[str, Any]) -> str:
    value = round1.first_value(props.get("márka"))
    return str(value or "márka nélkül")


def normalize_flavored_water(product: dict[str, Any]) -> None:
    old = product.get("tulajdonsagok") or {}
    props = dict(old)
    old_energy = fold(props.pop("energiatartalom", ""))
    label = fold(item_name(product))
    apenta_light = "apenta light" in label

    no_added = (
        bool_value(props.get("hozzáadott cukor nélkül"))
        or old_energy == "cukormentes"
        or apenta_light
        or "hozzaadott cukor nelkul" in label
        or "0 hozzaadott cukor" in label
        or re.search(r"\bzero\b", label) is not None
    )
    sweetener = (
        bool_value(props.get("édesítőszert tartalmaz"))
        or "edesitoszer" in label
        or apenta_light
    )
    energy_free = (
        bool_value(props.get("energiamentes"))
        or "energiamentes" in label
        or "energia es cukormentes" in label
        or apenta_light
        or "vitamixx zero" in label
        or "aqualife zero" in label
    )
    energy_reduced = (
        bool_value(props.get("energiacsökkentett"))
        or old_energy == "energiacsokkentett"
        or "energiaszegeny" in label
        or "csokkentett energiatartalmu" in label
    )
    vitamin = bool_value(props.pop("vitamin", False)) or bool_value(
        props.get("vitamint tartalmaz")
    )

    props["hozzáadott cukor nélkül"] = bool(no_added)
    props["édesítőszert tartalmaz"] = bool(sweetener)
    props["energiamentes"] = bool(energy_free)
    props["energiacsökkentett"] = bool(energy_reduced)
    props["vitamint tartalmaz"] = bool(vitamin)
    product["tulajdonsagok"] = props


def normalize_fruit(product: dict[str, Any], leaf: str) -> None:
    props = dict(product.get("tulajdonsagok") or {})
    if leaf == "Lé":
        props.pop("cukormentes", None)
        props.pop("édesség", None)
    elif leaf == "Gyümölcsital":
        no_added = bool_value(props.get("hozzáadott cukor nélkül")) or bool_value(
            props.pop("cukormentes", False)
        )
        if item_id(product) == SIO_ZERO_APPLE_ID:
            no_added = True
        props["hozzáadott cukor nélkül"] = bool(no_added)
    elif leaf == "Smoothie és püréital":
        props.pop("cukormentes", None)
        props.pop("rostos", None)
        props.pop("édesség", None)
    product["tulajdonsagok"] = props


def normalize_instant_tea(product: dict[str, Any]) -> None:
    old = dict(product.get("tulajdonsagok") or {})
    old["íz"] = [
        *values_of(old.get("íz")),
        *values_of(old.get("összetevő")),
        *values_of(old.get("összetevő / íz")),
    ]
    old["forma"] = "por"
    round1.normalize_tea(product, old)
    product["tulajdonsagok"]["forma"] = "por/instant"


def normalize_existing_tea(product: dict[str, Any]) -> None:
    props = dict(product.get("tulajdonsagok") or {})
    if props.get("forma") == "por":
        props["forma"] = "por/instant"
    product["tulajdonsagok"] = props


def normalize_snack_shake(product: dict[str, Any]) -> None:
    old = product.get("tulajdonsagok") or {}
    flavors = [
        str(value)
        for value in values_of(old.get("íz"))
        + values_of(old.get("összetevő / íz"))
        if fold(value) not in {"zab", "vitamin"}
    ]
    if not flavors:
        name = fold(item_name(product))
        if "csokolade" in name:
            flavors = ["csokoládé"]
        elif "vanilia" in name:
            flavors = ["vanília"]
        elif "malna" in name:
            flavors = ["málna"]
    if len(dedupe(flavors)) != 1:
        raise RuntimeError(f"Nem egyértelmű Snack&Shake íz: {item_id(product)} / {flavors}")
    sweetener = item_id(product) in SNACK_SHAKE_SWEETENER_IDS
    product["tulajdonsagok"] = {
        "márka": brand_from(old),
        "elkészítési alap": "tej",
        "zab alapú": True,
        "vitaminnal dúsított": True,
        "hozzáadott cukor nélkül": sweetener,
        "édesítőszert tartalmaz": sweetener,
        "íz": dedupe(flavors),
    }


def normalize_drink_powder(product: dict[str, Any]) -> None:
    old = product.get("tulajdonsagok") or {}
    flavors = [
        str(value)
        for value in values_of(old.get("íz")) + values_of(old.get("összetevő / íz"))
        if fold(value) not in {"tea", "zab", "vitamin"}
    ]
    if not flavors:
        raise RuntimeError(f"Íz nélküli valódi Italpor: {item_id(product)}")
    product["tulajdonsagok"] = {
        "márka": brand_from(old),
        "hozzáadott cukor nélkül": False,
        "édesítőszert tartalmaz": False,
        "íz": dedupe(flavors),
    }


def normalize_haas_tea_flavoring(product: dict[str, Any]) -> None:
    product["tulajdonsagok"] = {
        "márka": "Haas",
        "terméktípus": ["teaízesítő tabletta"],
        "forma": ["tabletta"],
        "édesítőszer típusa": ["egyéb"],
        "íz": ["citrom"],
        "C-vitaminnal": True,
    }


def coffee_form(product: dict[str, Any], old: dict[str, Any]) -> str:
    current = str(product.get("altipus") or "")
    if current == "Instant kávé":
        return "instant"
    if current == "Szemes kávé":
        return "szemes"
    if current == "Kapszulás kávé":
        return "kapszula"
    if current == "Őrölt kávé":
        return "kávépárna" if item_id(product) in round1.COFFEE_PAD_IDS else "őrölt"
    existing = str(round1.first_value(old.get("forma")) or "")
    if existing in {"instant", "őrölt", "szemes", "kapszula", "kávépárna"}:
        return existing
    raise RuntimeError(f"Ismeretlen kávéforma: {item_id(product)} / {current!r}")


def qualitative_intensity(
    product: dict[str, Any],
    old: dict[str, Any],
    overrides: dict[str, str],
    *,
    milky_or_mix: bool,
) -> str:
    if item_id(product) in overrides:
        return str(overrides[item_id(product)])
    existing = old.get("intenzitás")
    if existing in {"gyenge", "közepesen gyenge", "normál", "erős", "extra erős"}:
        return str(existing)
    text = fold(
        " ".join(
            [
                item_name(product),
                *[str(value) for value in values_of(old.get("íz / fajta"))],
            ]
        )
    )
    if any(
        token in text
        for token in ("extra strong", "extra eros", "fortissimo", "ristretto")
    ):
        return "extra erős"
    if any(
        token in text
        for token in (
            "intenso",
            "intense",
            "intenziv",
            "strong",
            "forte",
            "doppio",
            "dupla",
            "dark roast",
            "robusta",
            "walla",
        )
    ) or re.search(r"(?<!n)\bespresso\b", text):
        return "erős"
    if milky_or_mix:
        return "gyenge"
    if any(
        token in text
        for token in (
            "mild",
            "doux",
            "delicato",
            "blonde",
            "lagy",
            "silk",
            "soave",
            "fine aroma",
            "light roast",
            "calma",
        )
    ):
        return "közepesen gyenge"
    if re.search(r"\bgyenge\b|\bvery mild\b", text):
        return "gyenge"
    return "normál"


def coffee_name_flavors(product: dict[str, Any]) -> list[str]:
    text = fold(item_name(product))
    patterns: tuple[tuple[str, str], ...] = (
        ("ristretto", "ristretto"),
        ("espresso", "espresso"),
        ("lungo", "lungo"),
        ("americano", "americano"),
        ("cappuccino", "cappuccino"),
        ("cappucino", "cappuccino"),
        ("capuccino", "cappuccino"),
        ("cortado", "cortado"),
        ("flat white", "flat white"),
        ("latte macchiato", "latte macchiato"),
        ("macchiato", "macchiato"),
        ("latte", "latte"),
        ("melange", "melange"),
        ("frappe", "frappé"),
        ("mocha", "mocha"),
        ("mocca", "mocca"),
        ("crema", "crema"),
        ("cremoso", "crema"),
        ("barna cukor", "barna cukor"),
        ("ir krem", "ír krém"),
        ("csokolade", "csokoládé"),
        ("vanilia", "vanília"),
        ("vajkaramella", "vajkaramella"),
        ("karamell", "karamell"),
        ("mogyoro", "mogyoró"),
        ("mandula", "mandula"),
        ("kokusz", "kókusz"),
        ("pisztacia", "pisztácia"),
        ("marcipan", "marcipán"),
        ("malna", "málna"),
        ("eper", "eper"),
        ("gold", "gold"),
        ("klasszikus", "klasszikus"),
        ("classic", "klasszikus"),
        ("kronung", "krönung"),
        ("prodomo", "prodomo"),
        ("omnia", "omnia"),
        ("arabica", "arabica"),
        ("robusta", "robusta"),
    )
    result: list[str] = []
    for marker, value in patterns:
        if marker == "espresso":
            matched = re.search(r"\bespresso\b", text) is not None
        else:
            matched = marker in text
        if not matched:
            continue
        if marker in {"latte", "macchiato"} and "latte macchiato" in text:
            continue
        result.append(value)
    return dedupe(result)


def normalize_coffee(product: dict[str, Any], mapping: dict[str, Any]) -> None:
    old = product.get("tulajdonsagok") or {}
    form = coffee_form(product, old)
    two_ids = set(mapping.get("two_in_one_ids") or [])
    three_ids = set(mapping.get("three_in_one_ids") or [])
    mix = item_id(product) in two_ids or item_id(product) in three_ids
    raw_flavors = [
        str(value)
        for value in values_of(old.get("íz / fajta"))
        if fold(value)
        not in {
            "2in1",
            "3in1",
            "2 az 1",
            "2 az 1 ben",
            "3 az 1",
            "3 az 1 ben",
            "intenziv",
            "eros",
            "extra eros",
            "lagy",
        }
    ]
    flavors = dedupe([*raw_flavors, *coffee_name_flavors(product)])
    if len(flavors) > 1:
        flavors = [value for value in flavors if fold(value) != "natur"]
    flavors = flavors or ["natúr"]
    text = fold(item_name(product))
    decaf = (
        bool_value(old.get("koffeinmentes"))
        or item_id(product) in COFFEE_DECAF_OVERRIDE_IDS
        or "koffeinmentes" in text
        or "decaf" in text
    )
    overrides = mapping.get("intensity_override_by_id") or {}
    props: dict[str, Any] = {
        "márka": brand_from(old),
        "forma": form,
        "intenzitás": qualitative_intensity(
            product,
            old,
            overrides,
            milky_or_mix=(
                mix
                or any(
                    token in text
                    for token in (
                        "cappuccino",
                        "cappucino",
                        "capuccino",
                        "latte",
                        "macchiato",
                        "cortado",
                        "cafe au lait",
                        "flat white",
                        "tejes",
                        "tejpor",
                        "milk",
                        "mocha",
                        "frappe",
                        "melange",
                        "kaveitalpor",
                        "kakaoitalpor",
                        "milka",
                    )
                )
            ),
        ),
        "koffeinmentes": bool(decaf),
        "íz / fajta": flavors,
    }

    if item_id(product) in two_ids:
        props["hány az egyben"] = "2in1"
    elif item_id(product) in three_ids:
        props["hány az egyben"] = "3in1"

    if form == "kapszula":
        compat = (mapping.get("capsule_compatibility_by_id") or {}).get(item_id(product))
        if not compat:
            raise RuntimeError(f"Kompatibilitás nélküli kapszula: {item_id(product)}")
        props["kapszula kompatibilitás"] = str(compat)
    product["tulajdonsagok"] = props


def normalize_hot_chocolate(
    product: dict[str, Any],
    capsule_ids: set[str],
) -> None:
    old = product.get("tulajdonsagok") or {}
    text = fold(item_name(product))
    chocolate_type = str(old.get("csokoládétípus") or "")
    if not chocolate_type:
        if "feher" in text:
            chocolate_type = "fehér"
        elif "etcsokolade" in text or "dark chocolate" in text:
            chocolate_type = "ét"
        elif "tejcsokolade" in text:
            chocolate_type = "tej"
        else:
            chocolate_type = "klasszikus"
    raw_flavors = [
        *values_of(old.get("íz")),
        *values_of(old.get("íz / fajta")),
    ]
    flavors = [
        str(value)
        for value in raw_flavors
        if fold(value) not in {"kakao", "csokolade", "klasszikus"}
    ]
    if "kit kat" in text or "kitkat" in text:
        flavors = [
            value for value in flavors if fold(value) not in {"kit kat", "kitkat"}
        ]
        flavors.append("KitKat")
    product["tulajdonsagok"] = {
        "márka": brand_from(old),
        "állag": "kapszula" if item_id(product) in capsule_ids else "por",
        "csokoládétípus": chocolate_type,
        "íz": dedupe(flavors) or ["natúr"],
    }


def normalize_poloskei_zero(product: dict[str, Any]) -> None:
    props = dict(product.get("tulajdonsagok") or {})
    props["energiatartalom"] = "normál"
    props["hozzáadott cukor nélkül"] = True
    props["édesítőszert tartalmaz"] = True
    product["tulajdonsagok"] = props


def transform_product(
    product: dict[str, Any],
    coffee_map: dict[str, Any],
    soft_map: dict[str, Any],
) -> None:
    current = path_of(product)
    iid = item_id(product)
    move_hot = set(coffee_map.get("move_to_hot_chocolate_ids") or []) | set(
        coffee_map.get("kitkat_coffee_to_hot_chocolate_ids") or []
    )
    hot_capsules = set(coffee_map.get("hot_chocolate_capsule_ids") or [])

    if iid in HAAS_TEA_FLAVORING_IDS:
        set_path(product, SWEETENER_PATH)
        normalize_haas_tea_flavoring(product)
        return

    if iid in move_hot or current == (ITAL, HOT, "Forró csokoládé"):
        set_path(product, (ITAL, HOT, "Forró csokoládé"))
        normalize_hot_chocolate(product, hot_capsules)
        return

    if current[0] == ITAL and current[1] == HOT and current[2] in COFFEE_LEAVES:
        normalize_coffee(product, coffee_map)
        set_path(product, (ITAL, HOT, "Kávé"))
        return

    if iid in INSTANT_TEA_IDS:
        set_path(product, (ITAL, HOT, "Tea"))
        normalize_instant_tea(product)
        return
    if current == (ITAL, HOT, "Tea"):
        normalize_existing_tea(product)
        return

    if iid in SNACK_SHAKE_IDS or current == (
        ITAL,
        BASES,
        "Tejjel készítendő shake-por",
    ):
        set_path(product, (ITAL, BASES, "Tejjel készítendő shake-por"))
        normalize_snack_shake(product)
        return

    if current in {
        (ITAL, BASES, "Italtabletta és pezsgőkocka"),
        (ITAL, BASES, "Pezsgőtabletta"),
    }:
        set_path(product, (ITAL, BASES, "Pezsgőtabletta"))
        return

    if current == (ITAL, BASES, "Italpor"):
        normalize_drink_powder(product)
        return

    if current == (ITAL, BASES, "Szörp és koncentrátum"):
        name = fold(item_name(product))
        if "poloskei" in name and re.search(r"\bzero\b", name):
            normalize_poloskei_zero(product)
        return

    if current == (ITAL, WATER, "Ízesítetlen palackozott víz") or current == (
        ITAL,
        WATER,
        "",
    ):
        set_path(product, (ITAL, WATER, ""))
        return

    if current == (ITAL, WATER, "Ízesített víz") or current == (
        ITAL,
        FLAVORED_WATER,
        "",
    ):
        set_path(product, (ITAL, FLAVORED_WATER, ""))
        normalize_flavored_water(product)
        return

    if current == (ITAL, FUNCTIONAL, "Energiaital") or current == (
        ITAL,
        ENERGY,
        "",
    ):
        set_path(product, (ITAL, ENERGY, ""))
        if iid == HELL_ICE_COOL_ID:
            props = dict(product.get("tulajdonsagok") or {})
            props["íz"] = ["körte", "mandarin", "tuttifrutti"]
            product["tulajdonsagok"] = props
        return

    if current[0] == ITAL and current[1] == FRUIT and current[2] in FRUIT_LEAVES:
        normalize_fruit(product, current[2])
        return

    soft_by_id = soft_map.get("by_id") or {}
    if iid in soft_by_id:
        entry = soft_by_id[iid]
        leaf = str(entry["leaf"])
        flavors = [str(value) for value in entry["flavors"]]
        if leaf not in SOFT_LEAVES or not flavors:
            raise RuntimeError(f"Hibás üdítő-mapping: {iid} / {entry}")
        set_path(product, (ITAL, SOFT, leaf))
        props = dict(product.get("tulajdonsagok") or {})
        props["íz"] = dedupe(flavors)
        if leaf == "Jegestea":
            props.pop("szénsavas", None)
        product["tulajdonsagok"] = props
        return

    unresolved_by_id = {
        str(entry["id"]): entry for entry in (soft_map.get("unresolved") or [])
    }
    if iid in unresolved_by_id:
        entry = unresolved_by_id[iid]
        leaf = str(entry["leaf"])
        if leaf not in SOFT_LEAVES:
            raise RuntimeError(f"Hibás ellenőrzendő üdítőút: {iid} / {leaf}")
        set_path(product, (ITAL, SOFT, leaf))
        props = dict(product.get("tulajdonsagok") or {})
        props.pop("íz", None)
        props["íz kézi ellenőrzést igényel"] = True
        if leaf == "Jegestea":
            props.pop("szénsavas", None)
        product["tulajdonsagok"] = props


def products_at(
    products: list[dict[str, Any]],
    path: tuple[str, str, str],
) -> list[dict[str, Any]]:
    return [product for product in products if path_of(product) == path]


def rebuild_external_leaf(
    categories: dict[str, Any],
    products: list[dict[str, Any]],
    path: tuple[str, str, str],
) -> None:
    items = products_at(products, path)
    if not items:
        raise RuntimeError(f"Üres külső céllevél: {' > '.join(path)}")
    categories[path[0]][ALK_KEY][path[1]][ALT_KEY][path[2]][PROP_KEY] = (
        round1.build_prop_block(items)
    )


def rebuild_ital_tree(
    categories: dict[str, Any],
    products: list[dict[str, Any]],
    alcohol_node: dict[str, Any],
) -> None:
    by_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") == ITAL:
            by_path[
                (
                    str(product.get("alkategoria") or ""),
                    str(product.get("altipus") or ""),
                )
            ].append(product)

    parents: dict[str, Any] = {}
    expected_non_alcohol: set[tuple[str, str]] = set()
    for parent, leaves in TARGET_HIERARCHY:
        if parent == ALCOHOL:
            parents[parent] = alcohol_node
            continue
        if leaves is None:
            expected_non_alcohol.add((parent, ""))
            items = by_path.get((parent, ""), [])
            if not items:
                raise RuntimeError(f"Üres közvetlen Ital-alkategória: {parent}")
            parents[parent] = {
                PROP_KEY: round1.build_prop_block(items),
                ALT_KEY: {},
            }
            continue
        node = {PROP_KEY: {"egyedi": {}, "csoportos": {}}, ALT_KEY: {}}
        for leaf in leaves:
            expected_non_alcohol.add((parent, leaf))
            items = by_path.get((parent, leaf), [])
            if not items:
                raise RuntimeError(f"Üres Ital-levél: {parent} > {leaf}")
            node[ALT_KEY][leaf] = {PROP_KEY: round1.build_prop_block(items)}
        parents[parent] = node

    actual_non_alcohol = {
        path
        for path in by_path
        if path[0] != ALCOHOL
    }
    if actual_non_alcohol != expected_non_alcohol:
        raise RuntimeError(
            "Eltér a célfa és a termékutak halmaza: "
            f"hiány={sorted(expected_non_alcohol - actual_non_alcohol)}, "
            f"váratlan={sorted(actual_non_alcohol - expected_non_alcohol)}"
        )
    categories[ITAL] = {
        PROP_KEY: {"egyedi": {}, "csoportos": {}},
        ALK_KEY: parents,
    }
    rebuild_external_leaf(categories, products, SWEETENER_PATH)
    rebuild_external_leaf(categories, products, COCOA_PATH)


def validate_internal(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
    coffee_map: dict[str, Any],
    soft_map: dict[str, Any],
    original_alcohol_payload_hash: str,
    original_alcohol_node: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if len(products) != EXPECTED_TOTAL:
        errors.append(f"termékszám={len(products)}")

    for path, expected in EXPECTED_COUNTS.items():
        actual = len(products_at(products, path))
        if actual != expected:
            errors.append(f"{' > '.join(path)}={actual}, várt={expected}")

    alcohol_count = sum(
        1
        for product in products
        if product.get("fokategoria") == ITAL
        and product.get("alkategoria") == ALCOHOL
    )
    if alcohol_count != 5500:
        errors.append(f"alkohol={alcohol_count}, várt=5500")
    if round1.alcohol_payload_hash(products) != original_alcohol_payload_hash:
        errors.append("az alkoholos termékpayload megváltozott")
    if categories[ITAL][ALK_KEY][ALCOHOL] != original_alcohol_node:
        errors.append("az alkoholos fanód megváltozott")

    coffee = products_at(products, (ITAL, HOT, "Kávé"))
    form_counts = Counter(
        (product.get("tulajdonsagok") or {}).get("forma") for product in coffee
    )
    intensity_counts = Counter(
        (product.get("tulajdonsagok") or {}).get("intenzitás") for product in coffee
    )
    expected_forms = Counter(
        {"instant": 317, "őrölt": 256, "szemes": 235, "kapszula": 484, "kávépárna": 7}
    )
    if form_counts != expected_forms:
        errors.append(f"kávéforma={dict(form_counts)}, várt={dict(expected_forms)}")
    allowed_intensity = {"gyenge", "közepesen gyenge", "normál", "erős", "extra erős"}
    for product in coffee:
        props = product.get("tulajdonsagok") or {}
        if not values_of(props.get("íz / fajta")):
            errors.append(f"íz/fajta nélküli kávé: {item_id(product)}")
        if props.get("intenzitás") not in allowed_intensity:
            errors.append(f"hibás kávéintenzitás: {item_id(product)}")
        if props.get("forma") == "kapszula" and not props.get(
            "kapszula kompatibilitás"
        ):
            errors.append(f"kompatibilitás nélküli kapszula: {item_id(product)}")

    tea = products_at(products, (ITAL, HOT, "Tea"))
    tea_forms = Counter(
        (product.get("tulajdonsagok") or {}).get("forma") for product in tea
    )
    if tea_forms != Counter({"filteres": 713, "teafű": 32, "por/instant": 26}):
        errors.append(f"teaforma={dict(tea_forms)}")

    hot = products_at(products, (ITAL, HOT, "Forró csokoládé"))
    hot_states = Counter(
        (product.get("tulajdonsagok") or {}).get("állag") for product in hot
    )
    if hot_states != Counter({"por": 24, "kapszula": 9}):
        errors.append(f"forrócsoki-állag={dict(hot_states)}")
    if any(not values_of((product.get("tulajdonsagok") or {}).get("íz")) for product in hot):
        errors.append("íz nélküli forró csokoládé maradt")

    soft = [
        product
        for product in products
        if product.get("fokategoria") == ITAL and product.get("alkategoria") == SOFT
    ]
    if len(soft) != 1902:
        errors.append(f"üdítőszám={len(soft)}")
    missing_soft = [
        item_id(product)
        for product in soft
        if not values_of((product.get("tulajdonsagok") or {}).get("íz"))
    ]
    unresolved_ids = {
        str(entry["id"]) for entry in (soft_map.get("unresolved") or [])
    }
    if set(missing_soft) != unresolved_ids:
        errors.append(
            f"az íz nélküli és ellenőrzendő üdítők eltérnek: "
            f"ízhiány={sorted(missing_soft)}, ellenőrzendő={sorted(unresolved_ids)}"
        )
    if len(soft_map.get("by_id") or {}) != 79 or len(unresolved_ids) != 14:
        errors.append("az üdítőmapping nem 79 biztos + 14 ellenőrzendő rekord")

    fruit_drinks = products_at(products, (ITAL, FRUIT, "Gyümölcsital"))
    if any("cukormentes" in (product.get("tulajdonsagok") or {}) for product in fruit_drinks):
        errors.append("cukormentes kulcs maradt a Gyümölcsitalon")
    if any(
        "hozzáadott cukor nélkül" not in (product.get("tulajdonsagok") or {})
        for product in fruit_drinks
    ):
        errors.append("hiányos hozzáadottcukor-jelölés a Gyümölcsitalon")
    smoothies = products_at(products, (ITAL, FRUIT, "Smoothie és püréital"))
    if any(
        {"cukormentes", "rostos", "édesség"}
        & set((product.get("tulajdonsagok") or {}))
        for product in smoothies
    ):
        errors.append("tiltott smoothie-tulajdonság maradt")

    flavored_water = products_at(products, (ITAL, FLAVORED_WATER, ""))
    if any(
        "energiatartalom" in (product.get("tulajdonsagok") or {})
        for product in flavored_water
    ):
        errors.append("összevont energiatartalom maradt az Ízesített vízen")
    apenta = [
        product for product in flavored_water if "apenta light" in fold(item_name(product))
    ]
    if len(apenta) != 47 or any(
        not (product.get("tulajdonsagok") or {}).get("hozzáadott cukor nélkül")
        or not (product.get("tulajdonsagok") or {}).get("energiamentes")
        for product in apenta
    ):
        errors.append(f"hibás Apenta Light jelölés: {len(apenta)} rekord")

    poloskei = [
        product
        for product in products_at(products, (ITAL, BASES, "Szörp és koncentrátum"))
        if "poloskei" in fold(item_name(product))
        and re.search(r"\bzero\b", fold(item_name(product)))
    ]
    if len(poloskei) != 18 or any(
        (product.get("tulajdonsagok") or {}).get("energiatartalom") != "normál"
        or not (product.get("tulajdonsagok") or {}).get("hozzáadott cukor nélkül")
        or not (product.get("tulajdonsagok") or {}).get("édesítőszert tartalmaz")
        for product in poloskei
    ):
        errors.append(f"hibás Pölöskei ZERO jelölés: {len(poloskei)} rekord")

    hell = [product for product in products if item_id(product) == HELL_ICE_COOL_ID]
    if len(hell) != 1 or (hell[0].get("tulajdonsagok") or {}).get("íz") != [
        "körte",
        "mandarin",
        "tuttifrutti",
    ]:
        errors.append("a HELL Ice Cool íze hibás")

    return {
        "status": "ok" if not errors else "error",
        "errors": errors,
        "total_products": len(products),
        "ital_products": sum(1 for product in products if product.get("fokategoria") == ITAL),
        "non_alcoholic_ital_products": sum(
            1
            for product in products
            if product.get("fokategoria") == ITAL
            and product.get("alkategoria") != ALCOHOL
        ),
        "coffee_forms": dict(form_counts),
        "coffee_intensity": dict(intensity_counts),
        "tea_forms": dict(tea_forms),
        "hot_chocolate_states": dict(hot_states),
        "soft_flavor_coverage": len(soft) - len(missing_soft),
        "soft_manual_review": len(missing_soft),
        "coffee_mapping_capsules": len(
            coffee_map.get("capsule_compatibility_by_id") or {}
        ),
    }


def run_checker(products_path: Path, categories_path: Path) -> dict[str, Any]:
    failures: list[str] = []
    for attempt in range(1, 4):
        completed = subprocess.run(
            [
                sys.executable,
                str(CHECKER_PATH),
                "--products",
                str(products_path),
                "--categories",
                str(categories_path),
            ],
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=False,
            env={
                **os.environ,
                "PYTHONIOENCODING": "utf-8",
                "PYTHONMALLOC": "malloc",
            },
        )
        if completed.returncode == 0:
            return json.loads(completed.stdout)
        failures.append(
            f"{attempt}. kísérlet rc={completed.returncode}: "
            f"{completed.stdout[-1000:]} {completed.stderr[-1000:]}"
        )
    raise RuntimeError("A független ellenőrző hibás:\n" + "\n".join(failures))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--assert-idempotent", action="store_true")
    parser.add_argument("--products-source", type=Path, default=RESULT_PATH)
    parser.add_argument("--categories-source", type=Path, default=CATEGORY_PATH)
    args = parser.parse_args()

    coffee_map, soft_map = load_support_maps()
    products = round1.load_json(args.products_source)
    categories = round1.load_json(args.categories_source)
    if not isinstance(products, list) or len(products) != EXPECTED_TOTAL:
        raise RuntimeError(f"Váratlan termékállomány: {type(products).__name__}")
    if not isinstance(categories, dict) or ITAL not in categories:
        raise RuntimeError("Váratlan kategóriafa")

    before_categories_hash = round1.json_value_sha256(categories)
    alcohol_node = copy.deepcopy(categories[ITAL][ALK_KEY][ALCOHOL])
    alcohol_hash = round1.alcohol_payload_hash(products)
    changed_products = 0
    changed_paths: Counter[str] = Counter()
    changed_props: Counter[str] = Counter()
    samples: list[dict[str, Any]] = []

    for product in products:
        before_path = path_of(product)
        before_props = copy.deepcopy(product.get("tulajdonsagok") or {})
        transform_product(product, coffee_map, soft_map)
        after_path = path_of(product)
        after_props = product.get("tulajdonsagok") or {}
        if before_path != after_path or before_props != after_props:
            product["kategoria_hash"] = round1.category_hash(product)
            changed_products += 1
            changed_paths[" > ".join(before_path)] += 1
            for key in set(before_props) | set(after_props):
                if before_props.get(key) != after_props.get(key):
                    changed_props[key] += 1
            if len(samples) < 30:
                samples.append(
                    {
                        "id": item_id(product),
                        "név": item_name(product),
                        "út_előtte": list(before_path),
                        "út_utána": list(after_path),
                        "tulajdonságok_előtte": before_props,
                        "tulajdonságok_utána": after_props,
                    }
                )

    rebuild_ital_tree(categories, products, alcohol_node)
    validation = validate_internal(
        products,
        categories,
        coffee_map,
        soft_map,
        alcohol_hash,
        alcohol_node,
    )
    if validation["status"] != "ok":
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        raise RuntimeError(f"Belső validációs hibák: {validation['errors'][:20]}")

    after_categories_hash = round1.json_value_sha256(categories)
    if args.assert_idempotent and (
        changed_products != 0 or before_categories_hash != after_categories_hash
    ):
        raise RuntimeError(
            f"Nem idempotens: termék={changed_products}, "
            f"kategória={before_categories_hash != after_categories_hash}"
        )

    audit = {
        **validation,
        "changed_products": changed_products,
        "changed_paths": dict(changed_paths),
        "changed_properties": dict(changed_props),
        "samples": samples,
        "products_source": str(args.products_source),
        "categories_source": str(args.categories_source),
        "products_sha256": round1.json_value_sha256(products),
        "categories_sha256": after_categories_hash,
    }

    if args.prepare_only:
        if not CHECKER_PATH.is_file():
            raise RuntimeError(f"Hiányzó független ellenőrző: {CHECKER_PATH}")
        round1.dump_json(CANDIDATE_PRODUCTS_PATH, products)
        round1.dump_json(CANDIDATE_CATEGORIES_PATH, categories)
        audit["independent_check"] = run_checker(
            CANDIDATE_PRODUCTS_PATH,
            CANDIDATE_CATEGORIES_PATH,
        )
        round1.dump_json(AUDIT_PATH, audit)

    print(json.dumps(audit, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
