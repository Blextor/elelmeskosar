# -*- coding: utf-8 -*-
"""Független ellenőrző az ``ital_eszrevetelek2.txt`` migrációjához."""

from __future__ import annotations

import argparse
import json
import re
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
DEFAULT_PRODUCTS = BASE / ".eredmeny.ital2-20260726.candidate.json"
DEFAULT_CATEGORIES = BASE / ".kategoriak.ital2-20260726.candidate.json"
COFFEE_MAP_PATH = BASE / "ital_eszrevetelek2_kave_mapping_2026_07_26.json"
SOFT_MAP_PATH = BASE / "ital_eszrevetelek2_udito_iz_mapping_2026_07_26.json"

ITAL = "Ital"
WATER = "Ásványvíz"
FLAVORED_WATER = "Ízesített víz"
ENERGY = "Energiaital"
ALCOHOL = "Alkoholos italok és alkoholmentes alternatívák"
SOFT = "Üdítőitalok"
FRUIT = "Gyümölcs- és zöldségitalok"
FUNCTIONAL = "Funkcionális italok"
HOT = "Kávé-, tea- és forrócsokoládé-termékek"
BASES = "Italalapok"
PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"

SOFT_LEAVES = frozenset(
    {
        "Kóla",
        "Tonik",
        "Jegestea",
        "Aloe vera ital",
        "Gyömbér- és gyökéralapú üdítőital",
        "Kombucha",
        "Kölyökpezsgő",
        "Egyéb ízesített üdítőital",
    }
)
EXPECTED_NON_ALCOHOL_PATHS = {
    (WATER, ""),
    (FLAVORED_WATER, ""),
    (ENERGY, ""),
    *((SOFT, leaf) for leaf in SOFT_LEAVES),
    *((FRUIT, leaf) for leaf in ("Lé", "Nektár", "Gyümölcsital", "Smoothie és püréital")),
    (FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"),
    *((HOT, leaf) for leaf in ("Kávé", "Tea", "Forró csokoládé", "Krém, tejpor és tejszín")),
    *((BASES, leaf) for leaf in ("Pezsgőtabletta", "Szörp és koncentrátum", "Italpor", "Tejjel készítendő shake-por")),
}
EXPECTED_COUNTS = {
    (ITAL, WATER, ""): 402,
    (ITAL, FLAVORED_WATER, ""): 262,
    (ITAL, ENERGY, ""): 346,
    (ITAL, FRUIT, "Lé"): 383,
    (ITAL, FRUIT, "Nektár"): 84,
    (ITAL, FRUIT, "Gyümölcsital"): 776,
    (ITAL, FRUIT, "Smoothie és püréital"): 117,
    (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"): 139,
    (ITAL, HOT, "Kávé"): 1299,
    (ITAL, HOT, "Tea"): 771,
    (ITAL, HOT, "Forró csokoládé"): 33,
    (ITAL, HOT, "Krém, tejpor és tejszín"): 24,
    (ITAL, BASES, "Pezsgőtabletta"): 8,
    (ITAL, BASES, "Szörp és koncentrátum"): 391,
    (ITAL, BASES, "Italpor"): 12,
    (ITAL, BASES, "Tejjel készítendő shake-por"): 6,
}
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
HAAS_IDS = {"127538:3664736", "203228544"}
INSTANT_TEA_IDS = {
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
SNACK_SHAKE_IDS = {
    "340b600da09ead538e6691cc",
    "b16b51ddb1fd33c6dc930820",
    "70bea15b6e26ebe2e729e339",
    "111276034",
    "111276035",
    "111276036",
}
HELL_ID = "BTY-X17299200320021"
BANNED_BRANDS = {
    "floewater still",
    "floewater sparkling",
    "furedi ion",
    "furedi oxion",
    "omnia",
    "nestle ricore",
    "herz new york coffee",
    "vergnano",
    "bravo",
    "yippy",
    "estrella free damm",
    "dolce gusto",
    "good teahaz",
    "okf farmer s",
    "viwa vitaminwater",
    "absolute lifestyle",
    "absolute live",
    "prime hydration",
    "nutriversum flow",
    "optisana sports",
    "the gutsy captain kombucha",
    "chernel fizz water",
    "omg bubble tea",
    "bello minions party drink",
    "ice gold zero ice tea",
    "the sparkling t alba",
    "zen matcha",
    "vifon vietnamese lady",
    "canderel cankao",
    "lotte milkis",
    "dreamworks madagascar party drink",
    "jurassic world party drink",
    "yogitea",
    "sodastream pepsi",
    "sodastream mirinda",
    "sodastream 7up",
}
BANNED_ATOMS = {
    "marakuja",
    "maracuya",
    "szamoca",
    "forest fruit",
    "lemon",
    "raspberry",
    "cherry",
    "black cherry",
    "papaya",
    "repa",
    "dragon fruit",
    "red grape",
    "tropical",
    "tropical fruit",
    "tropusi gyumolcs",
    "vegyes",
    "vegyes gyumolcs",
    "vegyes gyumolcsle",
    "vegyes zoldseg",
    "zoldseges",
    "egzotikus",
    "egzotikus gyumolcs",
    "piros gyumolcs",
    "sarga gyumolcs",
    "rozsaszin gyumolcs",
    "erdei piros bogyos",
    "multifruit",
    "citrus mix",
    "dr pepper",
}
BANNED_TASTE_VALUES = {
    "revitalizalo",
    "antistressz",
    "green glory",
    "immun active",
    "immun iron",
    "jungle drink",
    "monster alarm",
    "mystic dragon",
    "pink dragon",
    "piros multi",
    "piros multivitamin",
    "tropical multivitamin",
    "kek balaton",
    "smoothie",
    "smoothie relax",
    "csontero",
    "fokusz",
    "almale suritmeny",
    "zoldalma pure",
    "repale",
    "szurt viz",
    "nata de coco",
    "spirulina alga kivonat",
    "ginger ale",
    "kofola",
    "juicy soda",
    "pink aromatic berry",
    "halloween",
    "frissito",
    "doctor",
    "extra strong",
    "full throttle",
    "lando norris",
    "loco",
    "nitro",
    "ultra",
    "ultra rosa",
    "summer ice i",
    "summer ice ii",
    "fantasy ruby red",
    "pipeline punch",
    "pacific punch",
    "rio punch",
    "ruby red",
    "barcelona edition",
    "mountain blast",
    "cool blue",
    "izotonias",
}


def item_id(product: dict[str, Any]) -> str:
    return round1.product_id(product)


def name_of(product: dict[str, Any]) -> str:
    return round1.product_name(product)


def path_of(product: dict[str, Any]) -> tuple[str, str, str]:
    return round1.path_of(product)


def values_of(value: Any) -> list[Any]:
    return round1.values_of(value)


def fold(value: Any) -> str:
    return round1.fold_text(value)


def items_at(
    products: list[dict[str, Any]],
    path: tuple[str, str, str],
) -> list[dict[str, Any]]:
    return [product for product in products if path_of(product) == path]


def declaration_for(
    categories: dict[str, Any],
    path: tuple[str, str, str],
) -> dict[str, Any]:
    parent = categories[path[0]][ALK_KEY][path[1]]
    if path[2] == "" and not parent.get(ALT_KEY):
        return parent[PROP_KEY]
    return parent[ALT_KEY][path[2]][PROP_KEY]


def validate_declared_value(
    errors: list[str],
    product: dict[str, Any],
    declaration: dict[str, Any],
) -> None:
    props = product.get("tulajdonsagok") or {}
    for key, value in props.items():
        iid = item_id(product)
        if isinstance(value, bool):
            if declaration.get("egyedi", {}).get(key, object()) != {}:
                errors.append(f"nem deklarált boolean: {iid} / {key}")
            continue
        if isinstance(value, list):
            allowed = declaration.get("csoportos", {}).get(key)
            if not isinstance(allowed, list):
                errors.append(f"nem deklarált csoportos kulcs: {iid} / {key}")
                continue
            missing = [entry for entry in value if entry not in allowed]
            if missing:
                errors.append(f"nem deklarált csoportos érték: {iid} / {key} / {missing}")
            continue
        allowed = declaration.get("egyedi", {}).get(key)
        if not isinstance(allowed, list) or value not in allowed:
            errors.append(f"nem deklarált egyedi érték: {iid} / {key} / {value!r}")


def validate_tree_and_schema(
    errors: list[str],
    products: list[dict[str, Any]],
    categories: dict[str, Any],
) -> None:
    ital_parents = categories[ITAL][ALK_KEY]
    required_parents = {
        WATER,
        FLAVORED_WATER,
        ENERGY,
        ALCOHOL,
        SOFT,
        FRUIT,
        FUNCTIONAL,
        HOT,
        BASES,
    }
    if set(ital_parents) != required_parents:
        errors.append(
            f"hibás Ital-alkategóriahalmaz: hiány={sorted(required_parents-set(ital_parents))}, "
            f"váratlan={sorted(set(ital_parents)-required_parents)}"
        )

    for direct in (WATER, FLAVORED_WATER, ENERGY):
        node = ital_parents.get(direct, {})
        if node.get(ALT_KEY) != {}:
            errors.append(f"{direct} nem közvetlen alkategória")

    product_paths = {
        (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        for product in products
        if product.get("fokategoria") == ITAL
        and product.get("alkategoria") != ALCOHOL
    }
    if product_paths != EXPECTED_NON_ALCOHOL_PATHS:
        errors.append(
            f"hibás nem alkoholos Ital-úthalmaz: "
            f"hiány={sorted(EXPECTED_NON_ALCOHOL_PATHS-product_paths)}, "
            f"váratlan={sorted(product_paths-EXPECTED_NON_ALCOHOL_PATHS)}"
        )

    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") == ITAL and product.get("alkategoria") != ALCOHOL:
            grouped[path_of(product)].append(product)
    for path, items in grouped.items():
        try:
            declaration = declaration_for(categories, path)
        except (KeyError, TypeError):
            errors.append(f"hiányzó kategóriadeklaráció: {' > '.join(path)}")
            continue
        expected = round1.build_prop_block(items)
        if declaration != expected:
            errors.append(f"nem egzakt tulajdonságséma: {' > '.join(path)}")
        for product in items:
            validate_declared_value(errors, product, declaration)
            if len(errors) > 200:
                return

    for external_path in (SWEETENER_PATH, COCOA_PATH):
        declaration = declaration_for(categories, external_path)
        items = items_at(products, external_path)
        if declaration != round1.build_prop_block(items):
            errors.append(f"nem egzakt külső séma: {' > '.join(external_path)}")


def validate_maps(
    errors: list[str],
    products: list[dict[str, Any]],
    coffee_map: dict[str, Any],
    soft_map: dict[str, Any],
) -> None:
    compat = coffee_map.get("capsule_compatibility_by_id") or {}
    two = set(coffee_map.get("two_in_one_ids") or [])
    three = set(coffee_map.get("three_in_one_ids") or [])
    hot_capsules = set(coffee_map.get("hot_chocolate_capsule_ids") or [])
    move_hot = set(coffee_map.get("move_to_hot_chocolate_ids") or [])
    kitkat = set(coffee_map.get("kitkat_coffee_to_hot_chocolate_ids") or [])
    if len(compat) != 486:
        errors.append(f"kapszulamapping={len(compat)}, várt=486")
    if len(two) != 25 or len(three) != 101 or two & three:
        errors.append(f"hibás hány-az-egyben mapping: {len(two)}/{len(three)}")
    if len(hot_capsules) != 9 or len(move_hot) != 6 or len(kitkat) != 2:
        errors.append(
            f"hibás forrócsoki-mapping: {len(hot_capsules)}/{len(move_hot)}/{len(kitkat)}"
        )
    final_capsules = {
        item_id(product)
        for product in items_at(products, (ITAL, HOT, "Kávé"))
        if (product.get("tulajdonsagok") or {}).get("forma") == "kapszula"
    }
    if final_capsules != set(compat) - kitkat:
        errors.append(
            f"kapszula-ID-paritás hibás: hiány={sorted((set(compat)-kitkat)-final_capsules)[:10]}, "
            f"váratlan={sorted(final_capsules-(set(compat)-kitkat))[:10]}"
        )

    by_id = soft_map.get("by_id") or {}
    unresolved_entries = soft_map.get("unresolved") or []
    unresolved = {str(entry["id"]) for entry in unresolved_entries}
    if (
        len(by_id) != 79
        or len(unresolved) != 14
        or set(by_id) & unresolved
        or len(set(by_id) | unresolved) != 93
    ):
        errors.append(
            f"hibás üdítőmapping: biztos={len(by_id)}, "
            f"ellenőrzendő={len(unresolved)}"
        )


def validate_semantics(
    errors: list[str],
    products: list[dict[str, Any]],
    coffee_map: dict[str, Any],
) -> dict[str, Any]:
    for path, expected in EXPECTED_COUNTS.items():
        actual = len(items_at(products, path))
        if actual != expected:
            errors.append(f"{' > '.join(path)}={actual}, várt={expected}")

    ital = [product for product in products if product.get("fokategoria") == ITAL]
    non_alcohol = [
        product for product in ital if product.get("alkategoria") != ALCOHOL
    ]
    alcohol = [product for product in ital if product.get("alkategoria") == ALCOHOL]
    if len(ital) != 12455 or len(non_alcohol) != 6955 or len(alcohol) != 5500:
        errors.append(
            f"hibás Ital darabszám: összes={len(ital)}, nemalkohol={len(non_alcohol)}, "
            f"alkohol={len(alcohol)}"
        )

    for product in non_alcohol:
        props = product.get("tulajdonsagok") or {}
        brand = props.get("márka")
        if not isinstance(brand, str) or not brand.strip():
            errors.append(f"nem skalár/üres márka: {item_id(product)} / {brand!r}")
        elif fold(brand) in BANNED_BRANDS:
            errors.append(f"nem főmárka maradt: {item_id(product)} / {brand}")
        for prop_name, value in props.items():
            if not isinstance(value, list):
                continue
            if any(
                isinstance(entry, (list, dict)) or entry in (None, "")
                for entry in value
            ):
                errors.append(f"nem elemi lista: {item_id(product)} / {prop_name}")
                continue
            markers = [fold(entry) for entry in value]
            if len(markers) != len(set(markers)):
                errors.append(f"duplikált listaérték: {item_id(product)} / {prop_name}")
            if prop_name not in {"íz", "összetevő", "összetevő / íz", "íz / fajta"}:
                continue
            for entry, marker in zip(value, markers):
                if marker in BANNED_ATOMS:
                    errors.append(
                        f"nem kanonikus atom: {item_id(product)} / {prop_name}={entry}"
                    )
                if prop_name in {"íz", "összetevő"} and marker in BANNED_TASTE_VALUES:
                    errors.append(
                        f"nem ízérték: {item_id(product)} / {prop_name}={entry}"
                    )
        if len(errors) > 200:
            break

    soft = [product for product in non_alcohol if product.get("alkategoria") == SOFT]
    soft_paths = {str(product.get("altipus") or "") for product in soft}
    missing_soft = [
        item_id(product)
        for product in soft
        if not values_of((product.get("tulajdonsagok") or {}).get("íz"))
    ]
    expected_missing = {
        str(entry["id"]) for entry in (round1.load_json(SOFT_MAP_PATH).get("unresolved") or [])
    }
    flagged_soft = {
        item_id(product)
        for product in soft
        if (product.get("tulajdonsagok") or {}).get(
            "íz kézi ellenőrzést igényel"
        )
    }
    if (
        len(soft) != 1902
        or soft_paths != SOFT_LEAVES
        or set(missing_soft) != expected_missing
        or flagged_soft != expected_missing
    ):
        errors.append(
            f"hibás üdítőaudit: count={len(soft)}, paths={sorted(soft_paths)}, "
            f"ízhiány={missing_soft[:20]}, jelölt={sorted(flagged_soft)[:20]}"
        )

    coffee = items_at(products, (ITAL, HOT, "Kávé"))
    forms = Counter((product.get("tulajdonsagok") or {}).get("forma") for product in coffee)
    intensities = Counter(
        (product.get("tulajdonsagok") or {}).get("intenzitás")
        for product in coffee
    )
    expected_forms = Counter(
        {"instant": 317, "őrölt": 256, "szemes": 235, "kapszula": 484, "kávépárna": 7}
    )
    expected_intensities = Counter(
        {
            "gyenge": 221,
            "közepesen gyenge": 40,
            "normál": 621,
            "erős": 376,
            "extra erős": 41,
        }
    )
    intensity_values = {"gyenge", "közepesen gyenge", "normál", "erős", "extra erős"}
    if forms != expected_forms:
        errors.append(f"hibás kávéforma: {dict(forms)}")
    if intensities != expected_intensities:
        errors.append(f"hibás kávéintenzitás-eloszlás: {dict(intensities)}")
    two_count = three_count = 0
    for product in coffee:
        props = product.get("tulajdonsagok") or {}
        if not values_of(props.get("íz / fajta")):
            errors.append(f"íz/fajta nélküli kávé: {item_id(product)}")
        if props.get("intenzitás") not in intensity_values:
            errors.append(f"hibás kávéintenzitás: {item_id(product)}")
        if props.get("hány az egyben") == "2in1":
            two_count += 1
        elif props.get("hány az egyben") == "3in1":
            three_count += 1
        elif "hány az egyben" in props:
            errors.append(f"hibás hány-az-egyben érték: {item_id(product)}")
        if any(
            fold(value) in {"2in1", "3in1", "2 az 1", "3 az 1"}
            for value in values_of(props.get("íz / fajta"))
        ):
            errors.append(f"hány-az-egyben maradt az ízben: {item_id(product)}")
        if props.get("forma") == "kapszula":
            expected = (coffee_map.get("capsule_compatibility_by_id") or {}).get(
                item_id(product)
            )
            if props.get("kapszula kompatibilitás") != expected:
                errors.append(f"hibás kapszulakompatibilitás: {item_id(product)}")
    if (two_count, three_count) != (25, 101):
        errors.append(f"hibás hány-az-egyben lefedettség: {two_count}/{three_count}")
    decaf = next(
        (product for product in coffee if item_id(product) == "10107032"),
        None,
    )
    if not decaf or not (decaf.get("tulajdonsagok") or {}).get("koffeinmentes"):
        errors.append("a Bellarom Viola Decaf koffeinmentessége hibás")

    tea = items_at(products, (ITAL, HOT, "Tea"))
    tea_forms = Counter((product.get("tulajdonsagok") or {}).get("forma") for product in tea)
    if tea_forms != Counter({"filteres": 713, "teafű": 32, "por/instant": 26}):
        errors.append(f"hibás teaforma: {dict(tea_forms)}")
    if {item_id(product) for product in tea} < INSTANT_TEA_IDS:
        errors.append("nem minden instant tea került a Tea levélbe")

    hot = items_at(products, (ITAL, HOT, "Forró csokoládé"))
    hot_states = Counter((product.get("tulajdonsagok") or {}).get("állag") for product in hot)
    hot_capsules = set(coffee_map.get("hot_chocolate_capsule_ids") or [])
    actual_hot_capsules = {
        item_id(product)
        for product in hot
        if (product.get("tulajdonsagok") or {}).get("állag") == "kapszula"
    }
    if hot_states != Counter({"por": 24, "kapszula": 9}):
        errors.append(f"hibás forrócsoki-állag: {dict(hot_states)}")
    if actual_hot_capsules != hot_capsules:
        errors.append("hibás forrócsoki-kapszula ID-halmaz")
    if any(not values_of((product.get("tulajdonsagok") or {}).get("íz")) for product in hot):
        errors.append("íz nélküli forró csokoládé maradt")

    juice = items_at(products, (ITAL, FRUIT, "Lé"))
    if any(
        {"cukormentes", "édesség"} & set((product.get("tulajdonsagok") or {}))
        for product in juice
    ):
        errors.append("édességi mező maradt a Lé levélen")
    fruit_drink = items_at(products, (ITAL, FRUIT, "Gyümölcsital"))
    if any(
        "cukormentes" in (product.get("tulajdonsagok") or {})
        or "hozzáadott cukor nélkül" not in (product.get("tulajdonsagok") or {})
        for product in fruit_drink
    ):
        errors.append("hibás Gyümölcsital cukormodell")
    smoothie = items_at(products, (ITAL, FRUIT, "Smoothie és püréital"))
    if any(
        {"cukormentes", "rostos", "édesség"}
        & set((product.get("tulajdonsagok") or {})
        )
        for product in smoothie
    ):
        errors.append("tiltott smoothie-tulajdonság maradt")

    flavored = items_at(products, (ITAL, FLAVORED_WATER, ""))
    required_flags = {
        "hozzáadott cukor nélkül",
        "édesítőszert tartalmaz",
        "energiamentes",
        "energiacsökkentett",
        "vitamint tartalmaz",
    }
    if any(
        "energiatartalom" in (product.get("tulajdonsagok") or {})
        or not required_flags <= set((product.get("tulajdonsagok") or {}))
        for product in flavored
    ):
        errors.append("hibás Ízesített víz cukor-/energiamodell")
    apenta = [product for product in flavored if "apenta light" in fold(name_of(product))]
    if len(apenta) != 47 or any(
        not (product.get("tulajdonsagok") or {}).get("hozzáadott cukor nélkül")
        or not (product.get("tulajdonsagok") or {}).get("energiamentes")
        for product in apenta
    ):
        errors.append(f"hibás Apenta Light audit: {len(apenta)}")

    syrups = items_at(products, (ITAL, BASES, "Szörp és koncentrátum"))
    poloskei = [
        product
        for product in syrups
        if "poloskei" in fold(name_of(product))
        and re.search(r"\bzero\b", fold(name_of(product)))
    ]
    if len(poloskei) != 18 or any(
        (product.get("tulajdonsagok") or {}).get("energiatartalom") != "normál"
        or not (product.get("tulajdonsagok") or {}).get("hozzáadott cukor nélkül")
        or not (product.get("tulajdonsagok") or {}).get("édesítőszert tartalmaz")
        for product in poloskei
    ):
        errors.append(f"hibás Pölöskei ZERO audit: {len(poloskei)}")

    hell = [product for product in products if item_id(product) == HELL_ID]
    if len(hell) != 1 or path_of(hell[0]) != (ITAL, ENERGY, "") or (
        hell[0].get("tulajdonsagok") or {}
    ).get("íz") != ["körte", "mandarin", "tuttifrutti"]:
        errors.append("hibás HELL Ice Cool rekord")

    if {item_id(product) for product in items_at(products, SWEETENER_PATH)} < HAAS_IDS:
        errors.append("a két Haas teaízesítő nincs az Édesítőszer tabletta levélen")
    if len(items_at(products, SWEETENER_PATH)) != 30:
        errors.append("hibás Édesítőszer tabletta darabszám")
    if len(items_at(products, COCOA_PATH)) != 102:
        errors.append("hibás kakaóporlevél darabszám")
    if {
        item_id(product)
        for product in items_at(products, (ITAL, BASES, "Tejjel készítendő shake-por"))
    } != SNACK_SHAKE_IDS:
        errors.append("hibás Snack&Shake ID-halmaz")

    return {
        "ital_products": len(ital),
        "non_alcoholic_ital_products": len(non_alcohol),
        "alcohol_products": len(alcohol),
        "soft_products": len(soft),
        "soft_flavor_coverage": len(soft) - len(missing_soft),
        "soft_manual_review": len(missing_soft),
        "coffee_forms": dict(forms),
        "coffee_intensity": dict(intensities),
        "tea_forms": dict(tea_forms),
        "hot_chocolate_states": dict(hot_states),
        "poloskei_zero": len(poloskei),
        "apenta_light": len(apenta),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--products", type=Path, default=DEFAULT_PRODUCTS)
    parser.add_argument("--categories", type=Path, default=DEFAULT_CATEGORIES)
    args = parser.parse_args()

    products = round1.load_json(args.products)
    categories = round1.load_json(args.categories)
    coffee_map = round1.load_json(COFFEE_MAP_PATH)
    soft_map = round1.load_json(SOFT_MAP_PATH)
    errors: list[str] = []
    if not isinstance(products, list) or len(products) != 47030:
        errors.append(f"hibás termékgyökér/darabszám: {type(products).__name__}")
    if not isinstance(categories, dict) or ITAL not in categories:
        errors.append("hibás kategóriagyökér")
    if errors:
        print(json.dumps({"status": "error", "errors": errors}, ensure_ascii=False))
        return 1

    composite_ids = [
        (
            str((product.get("termek") or {}).get("store_name") or ""),
            item_id(product),
        )
        for product in products
    ]
    duplicate_ids = [
        key for key, count in Counter(composite_ids).items() if count > 1
    ]
    if duplicate_ids:
        errors.append(f"duplikált bolt+termékazonosító: {duplicate_ids[:20]}")
    bad_hashes = [
        item_id(product)
        for product in products
        if (
            product.get("fokategoria") == ITAL
            and product.get("alkategoria") != ALCOHOL
        )
        if product.get("kategoria_hash") != round1.category_hash(product)
    ]
    if bad_hashes:
        errors.append(f"hibás kategoria_hash: {bad_hashes[:20]}")

    validate_maps(errors, products, coffee_map, soft_map)
    validate_tree_and_schema(errors, products, categories)
    summary = validate_semantics(errors, products, coffee_map)
    result = {
        "status": "ok" if not errors else "error",
        "errors": errors,
        "total_products": len(products),
        **summary,
        "products_file_sha256": round1.file_sha256(args.products),
        "categories_file_sha256": round1.file_sha256(args.categories),
        "products_value_sha256": round1.json_value_sha256(products),
        "categories_value_sha256": round1.json_value_sha256(categories),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
