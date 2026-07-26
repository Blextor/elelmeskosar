# -*- coding: utf-8 -*-
"""Független, csak olvasó ellenőrző a 2026-07-25-i Ital-migrációhoz."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

# A gépen tapasztalt szórványos CPython C-extension access violation miatt
# az ellenőrző tudatosan a stabilabb, tiszta Python JSON-útvonalat használja.
json.decoder.scanstring = json.decoder.py_scanstring
json.scanner.make_scanner = json.scanner.py_make_scanner

ITAL = "Ital"
PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"
EXPECTED_TOTAL = 47030
EXPECTED_ITAL = 12451

WATER = "Ásványvíz"
ALCOHOL = "Alkoholos italok és alkoholmentes alternatívák"
SOFT = "Üdítőitalok"
FRUIT = "Gyümölcs- és zöldségitalok"
FUNCTIONAL = "Funkcionális italok"
HOT = "Kávé-, tea- és forrócsokoládé-termékek"
BASES = "Italalapok"

BABY_WATER_PATH = ("Baba", "Bébiital, víz", "Bébivíz")
PLANT_PATH = ("Tejtermékek és tojás", "Növényi alternatíva", "Növényi ital")
COCOA_PATH = (
    "Alapanyag, sütés-főzés",
    "Sütési alapanyag",
    "Kakaópor és kakaós italpor",
)
GEL_PATH = ("Mentes, speciális", "Sport táplálékkiegészítő", "Energia gél")
DRAGEE_PATH = ("Édesség, snack, rágcsálnivaló", "Cukorka, nyalóka", "Drazsé")

TARGET_HIERARCHY: dict[str, tuple[str, ...]] = {
    WATER: ("Ízesítetlen palackozott víz", "Ízesített víz"),
    ALCOHOL: (
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
    SOFT: (
        "Kóla",
        "Tonik",
        "Jegestea",
        "Aloe vera ital",
        "Gyömbér- és gyökéralapú üdítőital",
        "Kombucha",
        "Kölyökpezsgő",
        "Egyéb ízesített üdítőital",
    ),
    FRUIT: ("Lé", "Nektár", "Gyümölcsital", "Smoothie és püréital"),
    FUNCTIONAL: ("Energiaital", "Sport-, izotóniás, kollagén- és shot ital"),
    HOT: (
        "Instant kávé",
        "Őrölt kávé",
        "Szemes kávé",
        "Kapszulás kávé",
        "Tea",
        "Forró csokoládé",
        "Krém, tejpor és tejszín",
    ),
    BASES: ("Italtabletta és pezsgőkocka", "Szörp és koncentrátum", "Italpor"),
}
TARGET_PATHS = frozenset(
    (parent, leaf)
    for parent, leaves in TARGET_HIERARCHY.items()
    for leaf in leaves
)

EXPECTED_COUNTS = {
    (ITAL, WATER, "Ízesítetlen palackozott víz"): 402,
    (ITAL, WATER, "Ízesített víz"): 262,
    (ITAL, ALCOHOL, None): 5500,
    (ITAL, FUNCTIONAL, "Energiaital"): 346,
    (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"): 139,
    (ITAL, SOFT, "Kóla"): 353,
    (ITAL, SOFT, "Egyéb ízesített üdítőital"): 841,
    (ITAL, HOT, "Szemes kávé"): 235,
    (ITAL, HOT, "Őrölt kávé"): 263,
    (ITAL, HOT, "Kapszulás kávé"): 486,
    (ITAL, HOT, "Instant kávé"): 317,
    (ITAL, HOT, "Tea"): 760,
    (ITAL, HOT, "Forró csokoládé"): 25,
    (ITAL, HOT, "Krém, tejpor és tejszín"): 24,
    (ITAL, BASES, "Italtabletta és pezsgőkocka"): 10,
    (ITAL, BASES, "Szörp és koncentrátum"): 391,
    (ITAL, BASES, "Italpor"): 29,
    BABY_WATER_PATH: 21,
    PLANT_PATH: 231,
    COCOA_PATH: 108,
    GEL_PATH: 5,
    DRAGEE_PATH: 151,
}

ALCOHOL_PAYLOAD_SHA256 = "7dac6e408bcbcf4bdfe959ed4c71b1c45b81fcc54c536c28dda6ea5e58a4bc7c"
ALCOHOL_TREE_SHA256 = "dec48a3fe112273431b2c31055728990431b5b7b0cb99cd48e4b132f0afd0c33"

STRAW_IDS = frozenset(
    {
        "748932",
        "748933",
        "748934",
        "148552:3685798",
        "438439:3975826",
        "148549:3685795",
    }
)
MILKSHAKE_POWDER_IDS = frozenset(
    {
        "340b600da09ead538e6691cc",
        "b16b51ddb1fd33c6dc930820",
        "70bea15b6e26ebe2e729e339",
        "111276034",
        "111276035",
        "111276036",
    }
)
MILKSHAKE_EXPECTED = {
    "340b600da09ead538e6691cc": (["csokoládé", "zab", "vitamin"], "normál"),
    "111276034": (["csokoládé", "zab", "vitamin"], "normál"),
    "b16b51ddb1fd33c6dc930820": (["vanília", "zab", "vitamin"], "normál"),
    "111276035": (["vanília", "zab", "vitamin"], "normál"),
    "70bea15b6e26ebe2e729e339": (["málna", "zab", "vitamin"], "édesítőszeres"),
    "111276036": (["málna", "zab", "vitamin"], "édesítőszeres"),
}
MILKY_SIP_IDS = frozenset(
    {"148552:3685798", "438439:3975826", "148549:3685795"}
)
DR_PEPPER_IDS = frozenset(
    {
        "675212:4212602",
        "10107947",
        "BTY-X17344700320021",
        "BTY-X17346100320021",
        "a0aaeb4a487a012f13eeedce",
        "7c872344a9aa65115cf75272",
        "121255136",
        "121223566",
    }
)
EXPECTED_BRANDS_BY_ID = {
    "34996:34999": "Paloma",
    "23425:23428": "Paloma",
    "150346:3687592": "Paloma",
    "23428:23431": "Paloma",
    "2753812": "Paloma",
    "BTY-X15982200320021": "Paloma",
    "BTY-X16195500320021": "Paloma",
    "BTY-X16043900320021": "Paloma",
    "179158": "Paloma",
    "179159": "Paloma",
    "779987": "Paloma",
    "777478": "Paloma",
    "28a30a8f1308ab0bc1ff116a": "Paloma",
    "1e98093134a9bb274a761a1c": "Paloma",
    "120010543": "Paloma",
    "120010520": "Paloma",
    "220330050": "Paloma",
    "120014735": "Paloma",
    "678470:4215860": "Smartwater",
    "f4699baa15c1da274ae18505": "Smartwater",
    "121217862": "Smartwater",
    "121217879": "Smartwater",
    "677855:4215245": "Auchan Tipp Pannon-Aqua",
    "677858:4215248": "Auchan Tipp Pannon-Aqua",
    "677861:4215251": "Auchan Tipp Pannon-Aqua",
    "677864:4215254": "Auchan Tipp Pannon-Aqua",
    "677867:4215257": "Auchan Tipp Pannon-Aqua",
    "677870:4215260": "Auchan Tipp Pannon-Aqua",
    "a96d2f36b5cecee09c11afa6": "CBA Pannon-Aqua",
    "913a824486991a0c73e0f077": "CBA Pannon-Aqua",
    "BTY-X2905900320021": "Cívis",
    "BTY-X17520500320021": "Cívis",
    "632288:4169678": "Biancaffè",
    "632291:4169681": "Biancaffè",
    "828302:4365692": "Biancaffè",
    "828305:4365695": "Biancaffè",
    "875360:4412750": "Caffè Pertè",
    "942494:4479884": "Caffè Pertè",
    "BTY-X1231600320021": "Caffè Pertè",
    "BTY-X1850500320021": "Caffè Pertè",
    "BTY-X2967100320021": "Caffè Pertè",
    "BTY-X7769200320021": "Caffè Pertè",
    "425482:3962863": "Caffè Degli Angeli",
    "BTY-X4333100320021": "Panna Cocktail",
    "998015": "Aloe Vera",
    "1031577": "Aloe Vera",
    "BTY-X17348600320021": "Guarana",
    "105516728": "BOB",
    "105516793": "BOB",
    "105516794": "BOB",
    "105516798": "BOB",
}
EXPECTED_HOT_CHOCOLATE_TYPES = {
    "51513:51855": "ét",
    "1714e29f26da732910f8a20f": "ét",
    "220339680": "ét",
    "127517:3664715": "fehér",
}
EXPECTED_TEA_TYPES = {
    "566752": "gyümölcstea",
    "828557": "zöld tea",
    "891126": "gyümölcstea",
    "926142": "gyümölcstea",
    "4597571": "gyógytea",
    "152525:3689765": "gyógytea",
    "1031021:4568411": "gyümölcstea",
    "1031393:4568783": "gyümölcstea",
    "BTY-X16752700320021": "gyógytea",
}

BABY_WATER_IDS = frozenset(
    {
        "10000512",
        "121229957",
        "121234432",
        "3375509",
        "36b671f13e2ca444e8ab2bcf",
        "5439b7feb63ede5ff2f61620",
        "55c59aca7f3e353c69166e53",
        "675029:4212419",
        "678479:4215869",
        "679580:4216970",
        "7eddc33e6c21dd83b533cd35",
        "8835ab20e432a58a25a562ed",
        "986082",
        "BTY-X17289100320021",
        "BTY-X17476700320021",
        "BTY-X18736300320021",
        "b2a4fca5951a6d0e4801b224",
        "ba079de4b9bfc8a5a0b1858e",
    }
)
GEL_IDS = frozenset({"946424:4483814", "824738:4362128", "824741:4362131"})
SHOT_IDS = frozenset(
    {
        "818540:4355930",
        "787775:4325165",
        "796328:4333718",
        "830327:4367717",
        "10000450",
        "10000456",
        "10055678",
        "BTY-X18623300320021",
        "84cff7483ff5d2096fa310e6",
        "279787f97383b762332eac0c",
        "8c4b16713a2ebd9260920dd1",
        "5ade240c14c1d7b9429f21c0",
        "105010609",
        "105010606",
        "BTY-X17350600320021",
        "BTY-X17352500320021",
        "121328166",
        "121232152",
        "121233306",
        "121254022",
        "111273604",
    }
)
KIDS_IDS = frozenset(
    {
        "661461:4198851",
        "684401:4221791",
        "684398:4221788",
        "684404:4221794",
        "661464:4198854",
        "BTY-X17219500320021",
        "BTY-X17219400320021",
        "BTY-X17176700320021",
        "BTY-X17219600320021",
        "e862a3fb03f89070e8287dfd",
        "771ad0bb0d16c25230148ca0",
        "00e3b97b38a1b130cd4b6346",
        "15942758f1b8f8a9c5e7c4b5",
        "6630a3a361fd4620dc766e31",
        "d57e4f193b2e90d7a3e2a4c5",
        "20a51071d1312d8fc2fd96fc",
        "08dafa3801f11c81cbf42f91",
        "bc071862dcc530d36c4cbe6a",
        "6bfceb8948f178cbc2e86c5f",
        "121221995",
        "121222020",
        "121222360",
        "121222037",
        "121222072",
        "679211:4216601",
        "679214:4216604",
        "679217:4216607",
        "BTY-X17810400320021",
        "BTY-X17810500320021",
        "121265441",
        "121265458",
        "121316641",
        "769656:4307046",
        "748902:4286292",
        "769659:4307049",
        "18554ba03d7aec0b25f5e7a1",
        "bc364d912b026a9e40149485",
        "7fac53361c94bb6fefb8927f",
        "121230505",
        "121230511",
        "121230528",
        "121340559",
    }
)

ALLOWED_SCHEMAS = {
    (WATER, "Ízesítetlen palackozott víz"): {
        "márka",
        "szénsavasság",
        "kiszerelés",
        "DRS",
        "csomagdarabszám",
        "egységnyi kiszerelés",
        "csomagolás",
    },
    (WATER, "Ízesített víz"): {
        "márka",
        "szénsavasság",
        "íz",
        "energiatartalom",
        "vitamin",
        "kiszerelés",
        "DRS",
        "csomagdarabszám",
        "egységnyi kiszerelés",
        "csomagolás",
    },
    (FUNCTIONAL, "Energiaital"): {
        "márka",
        "íz",
        "cukormentes",
        "szénsavas",
        "koffeinmentes",
    },
    (FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"): {
        "márka",
        "íz",
        "funkció",
    },
    (HOT, "Instant kávé"): {"márka", "koffeinmentes", "íz / fajta", "intenzitás"},
    (HOT, "Őrölt kávé"): {"márka", "koffeinmentes", "íz / fajta", "intenzitás"},
    (HOT, "Szemes kávé"): {"márka", "koffeinmentes", "íz / fajta", "intenzitás"},
    (HOT, "Kapszulás kávé"): {"márka", "koffeinmentes", "íz / fajta", "intenzitás"},
    (HOT, "Tea"): {"márka", "forma", "fajta", "összetevő", "teatípus"},
    (HOT, "Forró csokoládé"): {"márka", "csokoládétípus", "íz"},
    (HOT, "Krém, tejpor és tejszín"): {"márka", "típus"},
    (BASES, "Italtabletta és pezsgőkocka"): {
        "márka",
        "összetevő / íz",
        "energiatartalom",
        "vitamint tartalmaz",
        "vitamin",
    },
    (BASES, "Szörp és koncentrátum"): {
        "márka",
        "összetevő / íz",
        "energiatartalom",
        "hígítási arány",
    },
    (BASES, "Italpor"): {"márka", "összetevő / íz", "energiatartalom"},
}


def fold_text(value: Any) -> str:
    text = unicodedata.normalize("NFKD", "" if value is None else str(value))
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.casefold()
    text = re.sub(r"[^0-9a-z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplikált JSON-kulcs: {key!r}")
        result[key] = value
    return result


def reject_nonfinite(value: str) -> None:
    raise ValueError(f"Nem véges JSON-szám: {value}")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(
            handle,
            object_pairs_hook=strict_object,
            parse_constant=reject_nonfinite,
        )


def values_of(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    return list(value) if isinstance(value, list) else [value]


def dedupe(values: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        marker = f"{type(value).__name__}:{fold_text(value)}"
        if marker in seen:
            continue
        seen.add(marker)
        result.append(value)
    return result


def product_id(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("store_product_id") or "")


def product_name(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("product_name") or "")


def path_of(product: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(product.get("fokategoria") or ""),
        str(product.get("alkategoria") or ""),
        str(product.get("altipus") or ""),
    )


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


def id_hash(ids: Iterable[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def canonical_hash(payload: Any) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def alcohol_payload_hash(products: list[dict[str, Any]]) -> str:
    states = [
        {
            "id": product_id(product),
            "név": product_name(product),
            "út": list(path_of(product)),
            "tulajdonságok": product.get("tulajdonsagok") or {},
        }
        for product in products
        if product.get("fokategoria") == ITAL and product.get("alkategoria") == ALCOHOL
    ]
    states.sort(key=lambda item: item["id"])
    return canonical_hash(states)


def shape_of(value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    if isinstance(value, list):
        return "group"
    return "single"


def build_prop_block(products: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    raw: dict[str, list[Any]] = defaultdict(list)
    values: dict[str, list[Any]] = defaultdict(list)
    for product in products:
        for name, value in (product.get("tulajdonsagok") or {}).items():
            raw[name].append(value)
            values[name].extend(values_of(value))
    block: dict[str, dict[str, Any]] = {"egyedi": {}, "csoportos": {}}
    for name in sorted(raw, key=fold_text):
        shapes = {shape_of(value) for value in raw[name]}
        if len(shapes) != 1:
            raise ValueError(f"Kevert alak: {name}: {shapes}")
        shape = next(iter(shapes))
        allowed = sorted(dedupe(values[name]), key=fold_text)
        if shape == "flag":
            block["egyedi"][name] = {}
        elif shape == "single":
            block["egyedi"][name] = allowed
        else:
            block["csoportos"][name] = allowed
    return block


def products_at(
    products: list[dict[str, Any]],
    path: tuple[str, str, str],
) -> list[dict[str, Any]]:
    return [product for product in products if path_of(product) == path]


def declared_leaf(
    categories: dict[str, Any],
    path: tuple[str, str, str],
) -> dict[str, Any]:
    return (
        categories[path[0]][ALK_KEY][path[1]][ALT_KEY][path[2]][PROP_KEY]
    )


def declaration_accepts(
    block: dict[str, Any],
    name: str,
    value: Any,
) -> bool:
    section = "csoportos" if isinstance(value, list) else "egyedi"
    declared = (block.get(section) or {}).get(name)
    if isinstance(value, bool):
        return declared == {}
    if not isinstance(declared, list):
        return False
    actual_values = values_of(value)
    return all(item in declared for item in actual_values)


def add_error(errors: list[str], message: str, *, limit: int = 200) -> None:
    if len(errors) < limit:
        errors.append(message)


def validate(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    by_path: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        by_path[path_of(product)].append(product)
    if not isinstance(products, list) or len(products) != EXPECTED_TOTAL:
        add_error(errors, f"termékszám={len(products) if isinstance(products, list) else type(products)}")
    ids = [product_id(product) for product in products]
    if any(not item_id for item_id in ids):
        add_error(errors, "üres termékazonosító")
    # Azonos bolti azonosító külön láncoknál előfordulhat (például 734295
    # Aldi/Penny), ezért a valódi kulcs a bolt és az azonosító együtt.
    composite_ids = [
        (str((product.get("termek") or {}).get("store_name") or ""), product_id(product))
        for product in products
    ]
    duplicate_ids = [item for item, count in Counter(composite_ids).items() if count > 1]
    if duplicate_ids:
        add_error(errors, f"duplikált bolt+termékazonosító: {duplicate_ids[:20]}")

    ital = [product for product in products if product.get("fokategoria") == ITAL]
    if len(ital) != EXPECTED_ITAL:
        add_error(errors, f"Ital termékszám={len(ital)}, várt={EXPECTED_ITAL}")
    observed_paths = {
        (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        for product in ital
    }
    if observed_paths != set(TARGET_PATHS):
        add_error(
            errors,
            f"célút-paritás: hiány={sorted(TARGET_PATHS-observed_paths)}, "
            f"váratlan={sorted(observed_paths-TARGET_PATHS)}",
        )
    tree_parents = categories[ITAL][ALK_KEY]
    if tuple(tree_parents) != tuple(TARGET_HIERARCHY):
        add_error(errors, f"Ital szülőfa eltér: {list(tree_parents)}")
    for parent, leaves in TARGET_HIERARCHY.items():
        actual = tuple(tree_parents[parent][ALT_KEY])
        if actual != leaves:
            add_error(errors, f"{parent} levelei eltérnek: {actual}")

    for path, expected in EXPECTED_COUNTS.items():
        if path[2] is None:
            actual = sum(
                1
                for product in products
                if product.get("fokategoria") == path[0]
                and product.get("alkategoria") == path[1]
            )
        else:
            actual = len(by_path.get(path, ()))
        if actual != expected:
            add_error(errors, f"{' > '.join(value or '' for value in path)}={actual}, várt={expected}")

    alcohol_items = [
        product
        for product in products
        if product.get("fokategoria") == ITAL and product.get("alkategoria") == ALCOHOL
    ]
    alcohol_hash = alcohol_payload_hash(products)
    if alcohol_hash != ALCOHOL_PAYLOAD_SHA256:
        add_error(errors, f"alkohol-payload hash={alcohol_hash}")
    alcohol_tree_hash = canonical_hash(categories[ITAL][ALK_KEY][ALCOHOL])
    if alcohol_tree_hash != ALCOHOL_TREE_SHA256:
        add_error(errors, f"alkohol-fanód hash={alcohol_tree_hash}")

    # A közvetlen levéldeklaráció pontosan a termékekből épüljön fel.
    parity_paths = [
        (ITAL, parent, leaf)
        for parent, leaves in TARGET_HIERARCHY.items()
        if parent != ALCOHOL
        for leaf in leaves
    ] + [BABY_WATER_PATH, PLANT_PATH, COCOA_PATH, GEL_PATH]
    for path in parity_paths:
        items = by_path.get(path, [])
        try:
            expected_block = build_prop_block(items)
            actual_block = declared_leaf(categories, path)
        except (KeyError, TypeError, ValueError) as exc:
            add_error(errors, f"fa/paritás kivétel {' > '.join(path)}: {exc}")
            continue
        if actual_block != expected_block:
            add_error(errors, f"fa/termék értékparitás eltér: {' > '.join(path)}")

    # A migráció teljes célterületén minden kategória-hash friss legyen.
    hash_scope = {
        (ITAL, parent, leaf)
        for parent, leaves in TARGET_HIERARCHY.items()
        if parent != ALCOHOL
        for leaf in leaves
    } | {BABY_WATER_PATH, PLANT_PATH, COCOA_PATH, GEL_PATH}
    bad_hashes = [
        product_id(product)
        for product in products
        if (path_of(product) in hash_scope or product_id(product) in STRAW_IDS)
        and product.get("kategoria_hash") != category_hash(product)
    ]
    if bad_hashes:
        add_error(errors, f"elavult kategoria_hash: {bad_hashes[:20]} ({len(bad_hashes)})")

    # Márka minden célterméken skalár és nem üres.
    brand_scope = [
        product
        for product in products
        if path_of(product) in hash_scope or product_id(product) in STRAW_IDS
    ]
    banned_brands = {
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
    for product in brand_scope:
        brand = (product.get("tulajdonsagok") or {}).get("márka")
        if not isinstance(brand, str) or not brand.strip():
            add_error(errors, f"nem skalár/üres márka: {product_id(product)} / {brand!r}")
        elif fold_text(brand) in banned_brands:
            add_error(errors, f"nem főmárka maradt: {product_id(product)} / {brand}")

    # Listák: laposak, üresek és foldolt duplikátumok nélkül.
    for product in brand_scope:
        for name, value in (product.get("tulajdonsagok") or {}).items():
            if not isinstance(value, list):
                continue
            if any(isinstance(item, (list, dict)) or item in (None, "") for item in value):
                add_error(errors, f"nem elemi lista: {product_id(product)} / {name}")
            markers = [fold_text(item) for item in value]
            if len(markers) != len(set(markers)):
                add_error(errors, f"duplikált listaérték: {product_id(product)} / {name}")

    # Útvonalankénti szigorú sémák.
    for product in ital:
        parent, leaf = str(product.get("alkategoria")), str(product.get("altipus"))
        props = product.get("tulajdonsagok") or {}
        allowed: set[str] | None = ALLOWED_SCHEMAS.get((parent, leaf))
        if parent == SOFT:
            allowed = {"márka", "íz", "energiatartalom"}
            if leaf != "Jegestea":
                allowed.add("szénsavas")
        elif parent == FRUIT:
            allowed = {"márka", "gyümölcstartalom", "íz", "rostos", "cukormentes"}
        if allowed is not None and not set(props) <= allowed:
            add_error(
                errors,
                f"tiltott tulajdonság: {product_id(product)} / "
                f"{sorted(set(props)-allowed)}",
            )

    waters = [
        product
        for product in ital
        if product.get("alkategoria") == WATER
    ]
    allowed_carbonation = {
        "szénsavmentes",
        "enyhén szénsavas",
        "szénsavas",
        "extra szénsavas",
    }
    for product in waters:
        props = product.get("tulajdonsagok") or {}
        if props.get("szénsavasság") not in allowed_carbonation:
            add_error(errors, f"hibás szénsavasság: {product_id(product)}")
        if {"termékcsalád", "változat", "terméktípus", "célcsoport"} & set(props):
            add_error(errors, f"régi víztulajdonság: {product_id(product)}")
    flavored_water = by_path.get((ITAL, WATER, "Ízesített víz"), [])
    for product in flavored_water:
        state = (product.get("tulajdonsagok") or {}).get("energiatartalom")
        if state not in {"cukormentes", "energiacsökkentett", "normál"}:
            add_error(errors, f"hibás víz-energiatartalom: {product_id(product)} / {state}")
    water_energy = Counter(
        (product.get("tulajdonsagok") or {}).get("energiatartalom")
        for product in flavored_water
    )
    if water_energy != Counter(
        {"cukormentes": 143, "normál": 103, "energiacsökkentett": 16}
    ):
        add_error(errors, f"ízesítettvíz-energia megoszlás={dict(water_energy)}")

    soft = [product for product in ital if product.get("alkategoria") == SOFT]
    for product in soft:
        props = product.get("tulajdonsagok") or {}
        if props.get("energiatartalom") not in {"cukormentes", "energiacsökkentett", "normál"}:
            add_error(errors, f"hibás üdítő-energiatartalom: {product_id(product)}")
        leaf = product.get("altipus")
        if leaf == "Jegestea" and "szénsavas" in props:
            add_error(errors, f"jegesteán szénsavasság: {product_id(product)}")
        if leaf != "Jegestea" and not isinstance(props.get("szénsavas"), bool):
            add_error(errors, f"üdítőn hiányzó szénsavas bool: {product_id(product)}")
        if leaf in {"Kóla", "Tonik"} and not values_of(props.get("íz")):
            add_error(errors, f"kóla/tonik íz nélkül: {product_id(product)}")
    soft_energy = Counter(
        (product.get("tulajdonsagok") or {}).get("energiatartalom")
        for product in soft
    )
    if soft_energy != Counter(
        {"normál": 1312, "cukormentes": 512, "energiacsökkentett": 78}
    ):
        add_error(errors, f"üdítő-energia megoszlás={dict(soft_energy)}")
    soft_carbonation = Counter(
        (product.get("tulajdonsagok") or {}).get("szénsavas")
        for product in soft
    )
    if soft_carbonation != Counter({True: 1117, None: 487, False: 298}):
        add_error(errors, f"üdítő-szénsav megoszlás={dict(soft_carbonation)}")

    fruit = [product for product in ital if product.get("alkategoria") == FRUIT]
    for product in fruit:
        props = product.get("tulajdonsagok") or {}
        if not isinstance(props.get("rostos"), bool) or not isinstance(props.get("cukormentes"), bool):
            add_error(errors, f"gyümölcsital bool hiány: {product_id(product)}")
        percent = props.get("gyümölcstartalom")
        if percent is not None and not re.fullmatch(r"\d+(?:,\d+)?%", str(percent)):
            add_error(errors, f"hibás gyümölcstartalom: {product_id(product)} / {percent}")
    fruit_fiber = Counter(
        (product.get("tulajdonsagok") or {}).get("rostos")
        for product in fruit
    )
    fruit_sugar_free = Counter(
        (product.get("tulajdonsagok") or {}).get("cukormentes")
        for product in fruit
    )
    if fruit_fiber != Counter({False: 1267, True: 93}):
        add_error(errors, f"gyümölcsital-rostos megoszlás={dict(fruit_fiber)}")
    if fruit_sugar_free != Counter({False: 1307, True: 53}):
        add_error(
            errors,
            f"gyümölcsital-cukormentes megoszlás={dict(fruit_sugar_free)}",
        )

    energy_drinks = by_path.get((ITAL, FUNCTIONAL, "Energiaital"), [])
    energy_sugar_free = Counter(
        (product.get("tulajdonsagok") or {}).get("cukormentes")
        for product in energy_drinks
    )
    if energy_sugar_free != Counter({False: 290, True: 56}):
        add_error(
            errors,
            f"energiaital-cukormentes megoszlás={dict(energy_sugar_free)}",
        )

    func = by_path.get(
        (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"),
        [],
    )
    allowed_functions = {"sportital", "izotóniás", "kollagén", "shot"}
    for product in func:
        functions = set(values_of((product.get("tulajdonsagok") or {}).get("funkció")))
        if not functions or not functions <= allowed_functions:
            add_error(errors, f"hibás funkció: {product_id(product)} / {sorted(functions)}")

    coffee = [
        product
        for product in ital
        if product.get("alkategoria") == HOT and "kávé" in str(product.get("altipus")).casefold()
    ]
    decaf_count = 0
    intensity_ids: set[str] = set()
    for product in coffee:
        props = product.get("tulajdonsagok") or {}
        if not isinstance(props.get("koffeinmentes"), bool):
            add_error(errors, f"kávé koffein-bool nélkül: {product_id(product)}")
        decaf_count += props.get("koffeinmentes") is True
        if "intenzitás" in props:
            intensity_ids.add(product_id(product))
            if not isinstance(props["intenzitás"], int):
                add_error(errors, f"nem numerikus intenzitás: {product_id(product)}")
    if decaf_count != 73:
        add_error(errors, f"koffeinmentes kávé={decaf_count}, várt=73")
    if len(intensity_ids) != 15:
        add_error(errors, f"explicit intenzitás={len(intensity_ids)}, várt=15")

    tea = by_path.get((ITAL, HOT, "Tea"), [])
    tea_forms = Counter((product.get("tulajdonsagok") or {}).get("forma") for product in tea)
    if tea_forms != Counter({"filteres": 713, "teafű": 32, "por": 15}):
        add_error(errors, f"teaforma={dict(tea_forms)}")
    bad_tea_varieties = {
        "teavalogatas",
        "gyerektea",
        "fruit infusion",
        "herbal infusion",
        "multivitamin",
        "defense",
        "immune",
        "digestion super tea",
        "reflux",
        "boost super tea",
        "yellow label",
        "classic",
        "classic label",
        "garzon",
        "natur pur",
        "vilag teai",
        "classic matcha latte",
        "mango matcha latte",
        "strawberry matcha latte",
    }
    for product in tea:
        varieties = {
            fold_text(value)
            for value in values_of((product.get("tulajdonsagok") or {}).get("fajta"))
        }
        if varieties & bad_tea_varieties:
            add_error(
                errors,
                f"nem elemi teafajta: {product_id(product)} / "
                f"{sorted(varieties & bad_tea_varieties)}",
            )

    flavored_water = by_path.get((ITAL, WATER, "Ízesített víz"), [])
    for product in flavored_water:
        label = fold_text(product_name(product))
        if any(marker in label for marker in ("vitamin", "vitamixx", "multivitamin")):
            if (product.get("tulajdonsagok") or {}).get("vitamin") is not True:
                add_error(errors, f"explicit vitaminjelölés flag nélkül: {product_id(product)}")

    additive = by_path.get((ITAL, HOT, "Krém, tejpor és tejszín"), [])
    additive_types = Counter((product.get("tulajdonsagok") or {}).get("típus") for product in additive)
    if additive_types != Counter({"krémpor": 19, "tejpor": 4, "tejszín": 1}):
        add_error(errors, f"adaléktípus={dict(additive_types)}")

    plant = by_path.get(PLANT_PATH, [])
    barista_count = sum(
        (product.get("tulajdonsagok") or {}).get("barista") is True
        for product in plant
    )
    if barista_count != 46:
        add_error(errors, f"barista={barista_count}, várt=46")
    for product in plant:
        props = product.get("tulajdonsagok") or {}
        if {"zsírszegény", "fehérjetartalom", "változat", "felhasználás"} & set(props):
            add_error(errors, f"régi növényi tulajdonság: {product_id(product)}")
        flavors = {fold_text(value) for value in values_of(props.get("íz"))}
        if flavors & {"tea", "not milk", "not milk semi", "not milk whole", "szoja"}:
            add_error(errors, f"hibás növényi íz: {product_id(product)} / {sorted(flavors)}")
        bases = {fold_text(value) for value in values_of(props.get("alap"))}
        if flavors & bases:
            add_error(errors, f"alap ízként ismétlődik: {product_id(product)} / {sorted(flavors & bases)}")

    cocoa = by_path.get(COCOA_PATH, [])
    cocoa_sweetness = Counter(
        (product.get("tulajdonsagok") or {}).get("cukrozottság")
        for product in cocoa
    )
    if cocoa_sweetness.get("natúr") != 46 or sum(cocoa_sweetness.values()) != 108:
        add_error(errors, f"kakaó cukrozottság={dict(cocoa_sweetness)}")
    pure = [
        product
        for product in cocoa
        if (product.get("tulajdonsagok") or {}).get("cukrozottság") == "natúr"
    ]
    if any((product.get("tulajdonsagok") or {}).get("kakaótartalom") != "100%" for product in pure):
        add_error(errors, "natúr kakaó nem 100%-os")

    tablets = by_path.get((ITAL, BASES, "Italtabletta és pezsgőkocka"), [])
    if any((product.get("tulajdonsagok") or {}).get("vitamint tartalmaz") is not True for product in tablets):
        add_error(errors, "nem minden italtabletta vitaminos bool")
    syrups = by_path.get((ITAL, BASES, "Szörp és koncentrátum"), [])
    dilution = [
        product for product in syrups
        if (product.get("tulajdonsagok") or {}).get("hígítási arány") == "1:23"
    ]
    if len(dilution) != 33:
        add_error(errors, f"1:23 hígítás={len(dilution)}, várt=33")
    powders = by_path.get((ITAL, BASES, "Italpor"), [])
    for product in powders:
        props = product.get("tulajdonsagok") or {}
        if not values_of(props.get("összetevő / íz")):
            add_error(errors, f"italpor összetevő/íz nélkül: {product_id(product)}")
        if props.get("energiatartalom") not in {
            "normál",
            "csökkentett",
            "édesítőszeres",
        }:
            add_error(
                errors,
                f"italpor hibás energiatartalom: "
                f"{product_id(product)} / {props.get('energiatartalom')}",
            )
    all_bases = [
        product
        for path, items in by_path.items()
        if path[0] == ITAL and path[1] == BASES
        for product in items
    ]
    base_energy = Counter(
        (product.get("tulajdonsagok") or {}).get("energiatartalom")
        for product in all_bases
    )
    if base_energy != Counter(
        {"normál": 227, "édesítőszeres": 187, "csökkentett": 16}
    ):
        add_error(errors, f"italalap-energia megoszlás={dict(base_energy)}")

    # Exact mozgatási halmazok.
    by_id = {product_id(product): product for product in products}
    for item_id, expected_brand in EXPECTED_BRANDS_BY_ID.items():
        product = by_id.get(item_id)
        actual_brand = (
            (product.get("tulajdonsagok") or {}).get("márka")
            if product is not None
            else None
        )
        if actual_brand != expected_brand:
            add_error(
                errors,
                f"exact főmárka eltér: {item_id} / {actual_brand!r}, várt={expected_brand!r}",
            )
    test_product = by_id.get("2806122")
    if test_product is None or (test_product.get("tulajdonsagok") or {}).get("márka") != "egyéb":
        add_error(errors, "TESZTCIKK forráskivétel megváltozott vagy eltűnt: 2806122")
    for item_id in DR_PEPPER_IDS:
        product = by_id.get(item_id)
        props = (product or {}).get("tulajdonsagok") or {}
        if (
            product is None
            or path_of(product) != (ITAL, SOFT, "Kóla")
            or props.get("íz") != ["natúr"]
        ):
            add_error(
                errors,
                f"Dr Pepper nincs egységes Kóla/natúr állapotban: "
                f"{item_id} / {path_of(product) if product else None} / {props.get('íz')}",
            )
    for item_id, expected_type in EXPECTED_HOT_CHOCOLATE_TYPES.items():
        product = by_id.get(item_id)
        actual_type = (
            (product.get("tulajdonsagok") or {}).get("csokoládétípus")
            if product is not None
            else None
        )
        if actual_type != expected_type:
            add_error(
                errors,
                f"forrócsokoládé-típus eltér: {item_id} / "
                f"{actual_type!r}, várt={expected_type!r}",
            )
    for item_id, expected_type in EXPECTED_TEA_TYPES.items():
        product = by_id.get(item_id)
        actual_types = set(
            values_of((product or {}).get("tulajdonsagok", {}).get("teatípus"))
        )
        if expected_type not in actual_types:
            add_error(
                errors,
                f"bizonyított teatípus hiányzik: {item_id} / "
                f"{sorted(actual_types)}, várt={expected_type!r}",
            )
    for item_id in BABY_WATER_IDS:
        if path_of(by_id[item_id]) != BABY_WATER_PATH:
            add_error(errors, f"babavíz rossz úton: {item_id}")
    for item_id in GEL_IDS:
        if path_of(by_id[item_id]) != GEL_PATH:
            add_error(errors, f"energiazselé rossz úton: {item_id}")
    shot_path = (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital")
    for item_id in SHOT_IDS:
        if path_of(by_id[item_id]) != shot_path:
            add_error(errors, f"shot rossz úton: {item_id}")
    powder_path = (ITAL, BASES, "Italpor")
    for item_id in MILKSHAKE_POWDER_IDS:
        product = by_id[item_id]
        props = product.get("tulajdonsagok") or {}
        if path_of(product) != powder_path:
            add_error(errors, f"milkshake-por rossz úton: {item_id}")
        expected_flavors, expected_energy = MILKSHAKE_EXPECTED[item_id]
        if props.get("márka") != "Dr. Oetker":
            add_error(errors, f"milkshake-por márkája hibás: {item_id}")
        if props.get("összetevő / íz") != expected_flavors:
            add_error(
                errors,
                f"milkshake-por atomjai hibásak: "
                f"{item_id} / {props.get('összetevő / íz')}",
            )
        if props.get("energiatartalom") != expected_energy:
            add_error(
                errors,
                f"milkshake-por energiatartalma hibás: "
                f"{item_id} / {props.get('energiatartalom')}",
            )
    try:
        dragee_block = declared_leaf(categories, DRAGEE_PATH)
    except (KeyError, TypeError, ValueError) as exc:
        dragee_block = {}
        add_error(errors, f"Drazsé-deklaráció nem olvasható: {exc}")
    straw_schema = {
        "márka",
        "íz",
        "forma",
        "cukormentes / hozzáadott cukor nélkül",
        "mentolos",
        "savanyú",
        "alkoholos",
    }
    for item_id in STRAW_IDS:
        product = by_id[item_id]
        props = product.get("tulajdonsagok") or {}
        if path_of(product) != DRAGEE_PATH:
            add_error(errors, f"ízesítő szívószál rossz úton: {item_id}")
        expected_brand = "Milky Sip" if item_id in MILKY_SIP_IDS else "Good Choice"
        if props.get("márka") != expected_brand:
            add_error(
                errors,
                f"ízesítő szívószál márkája hibás: "
                f"{item_id} / {props.get('márka')}",
            )
        if set(props) != straw_schema:
            add_error(errors, f"ízesítő szívószál sémája hibás: {item_id} / {sorted(props)}")
        if props.get("forma") != ["szívószál"] or len(values_of(props.get("íz"))) != 1:
            add_error(errors, f"ízesítő szívószál nem elemi: {item_id}")
        if any(
            props.get(flag) is not False
            for flag in (
                "cukormentes / hozzáadott cukor nélkül",
                "mentolos",
                "savanyú",
                "alkoholos",
            )
        ):
            add_error(errors, f"ízesítő szívószál booleanje hibás: {item_id}")
        for name, value in props.items():
            if not declaration_accepts(dragee_block, name, value):
                add_error(errors, f"Drazsé-deklaráció nem fedi: {item_id} / {name}={value!r}")
    kids_path = (ITAL, SOFT, "Kölyökpezsgő")
    actual_kids = {product_id(product) for product in by_path.get(kids_path, [])}
    if actual_kids != KIDS_IDS:
        add_error(
            errors,
            f"kölyökpezsgő-halmaz eltér: count={len(actual_kids)}, hash={id_hash(actual_kids)}",
        )
    for product in products:
        folded_name = fold_text(product_name(product))
        if "kubu waterr" in folded_name and path_of(product) != (ITAL, WATER, "Ízesített víz"):
            add_error(errors, f"Kubu Waterr nem víz: {product_id(product)}")
        if "cappy ice fruit" in folded_name and path_of(product) != (
            ITAL,
            SOFT,
            "Egyéb ízesített üdítőital",
        ):
            add_error(errors, f"Cappy Ice Fruit rossz út: {product_id(product)}")

    # Ismert aliasok és értelmetlen értékek ne maradjanak a nem alkoholos célban.
    banned_atoms = {
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
    banned_taste_values = {
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
    for product in brand_scope:
        props = product.get("tulajdonsagok") or {}
        for prop_name in ("íz", "összetevő", "összetevő / íz", "íz / fajta"):
            for value in values_of(props.get(prop_name)):
                if fold_text(value) in banned_atoms:
                    add_error(errors, f"nem kanonikus atom: {product_id(product)} / {prop_name}={value}")
                if prop_name in {"íz", "összetevő"} and fold_text(value) in banned_taste_values:
                    add_error(
                        errors,
                        f"nem íz/összetevő érték: "
                        f"{product_id(product)} / {prop_name}={value}",
                    )
        for prop_name in ("íz", "összetevő", "összetevő / íz", "íz / fajta"):
            markers = {
                fold_text(value)
                for value in values_of(props.get(prop_name))
            }
            if "barack" in markers and markers & {"oszibarack", "sargabarack"}:
                add_error(
                    errors,
                    f"redundáns barackatom: {product_id(product)} / {prop_name}",
                )
            if "tea" in markers and any(
                marker.endswith(" tea") and marker != "tea" for marker in markers
            ):
                add_error(
                    errors,
                    f"redundáns teaatom: {product_id(product)} / {prop_name}",
                )
        if any(
            fold_text(value) == "multivitamin"
            for value in values_of(props.get("íz"))
        ):
            add_error(errors, f"multivitamin ízként: {product_id(product)}")

    return {
        "status": "ok" if not errors else "error",
        "errors": errors,
        "counts": {
            "products": len(products),
            "ital": len(ital),
            "ital_paths": len(observed_paths),
            "alcohol": len(alcohol_items),
            "water": sum(product.get("alkategoria") == WATER for product in ital),
            "functional": sum(product.get("alkategoria") == FUNCTIONAL for product in ital),
        },
        "hashes": {
            "alcohol_payload": alcohol_hash,
            "alcohol_tree": alcohol_tree_hash,
            "kids": id_hash(
                product_id(product)
                for product in by_path.get((ITAL, SOFT, "Kölyökpezsgő"), [])
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--products", type=Path, required=True)
    parser.add_argument("--categories", type=Path, required=True)
    args = parser.parse_args()
    try:
        products = load_json(args.products)
        categories = load_json(args.categories)
        payload = validate(products, categories)
    except BaseException as exc:
        payload = {
            "status": "error",
            "errors": [f"{type(exc).__name__}: {exc}"],
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
