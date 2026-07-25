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

# A régi „Vegyes gyümölcs- és zöldséglé” ág 190 rekordjának kézzel
# ellenőrzött, egymást kizáró célcsoportjai. A fennmaradó 106 rekord valódi lé.
LEGACY_MIXED_JUICE_ID_SHA256 = (
    "369b35c38029ae2049ca1f1b4d3718c86edf9d9a196aa5152569ef6a6289dcbf"
)
SMOOTHIE_PUREE_IDS = frozenset(
    {
        "015757a9096c30525cd97616",
        "10003689",
        "10101629",
        "121231061",
        "440431:3977815",
        "440434:3977818",
        "4599177",
        "4599178",
        "4599179",
        "4599180",
        "4603362",
        "513662:4051052",
        "533147:4070537",
        "533153:4070543",
        "534752",
        "534753",
        "534754",
        "536931:4074321",
        "6a6c94adaf66dd29f4c5f062",
        "775977:4313367",
        "778329:4315719",
        "849917:4387307",
        "849920:4387310",
        "849923:4387313",
        "9571:9574",
        "BTY-X15551700320021",
        "BTY-X15563000320021",
        "BTY-X17539800320022",
        "BTY-X7821900320022",
        "ad9df10725f96fe1644950b6",
        "e53d95437f2838192d3d832b",
    }
)
FRUIT_DRINK_IDS = frozenset(
    {
        "10000450",
        "10000456",
        "10045431",
        "10055678",
        "1028336",
        "121229554",
        "121229709",
        "121230045",
        "121230281",
        "121230309",
        "220341206",
        "2807800",
        "2808563",
        "2dda65cc3f4c183bee87c7f2",
        "3372094",
        "3372099",
        "4604103",
        "4605175",
        "588194:4125584",
        "632549:4169939",
        "674834:4212224",
        "674840:4212230",
        "674846:4212236",
        "691970:4229360",
        "711749:4249139",
        "711755:4249145",
        "711758:4249148",
        "711761:4249151",
        "753873",
        "757841",
        "757842",
        "783350:4320740",
        "787775:4325165",
        "795707:4333097",
        "796328:4333718",
        "818540:4355930",
        "818594:4355984",
        "818600:4355990",
        "818612:4356002",
        "848948:4386338",
        "84cff7483ff5d2096fa310e6",
        "935735",
        "935736",
        "935737",
        "944844",
        "986393",
        "986394",
        "aca22233ae9019e85728e396",
        "c16cd8fee0515b8654060bd9",
        "e4443d9fe66eed9bf7d69966",
    }
)
NECTAR_IDS = frozenset({"914263", "950537:4487927", "986392"})
LEGACY_JUICE_VEGETABLE_ONLY_IDS = frozenset(
    {
        "121236845",
        "121311646",
        "470711:4008083",
        "541900",
        "688067:4225457",
        "688070:4225460",
        "720272:4257662",
        "720275:4257665",
        "825842:4363232",
        "947300:4484690",
        "950759:4488149",
        "950762:4488152",
    }
)
LEGACY_JUICE_MIXED_IDS = frozenset(
    {
        "1021641",
        "105007895",
        "121236712",
        "121236758",
        "121236862",
        "121263155",
        "15ba1924746fbabc7918d1bb",
        "2f5d164f1fc8dc1818f9f8c8",
        "44824294b396e198ef5ccced",
        "588146:4125536",
        "61850:3598934",
        "791240:4328630",
        "8152f50d112035382f9196cc",
        "848798:4386188",
        "914735",
        "BTY-X15030300320021",
        "BTY-X17540400320021",
        "BTY-X9170800320021",
    }
)

# A már eleve más léágról érkező rekordok bizonyított létípus-javításai.
EXTRA_JUICE_VEGETABLE_ONLY_IDS = frozenset(
    {"848801:4386191", "220104087"}
)
EXTRA_JUICE_MIXED_IDS = frozenset(
    {
        "121230091",
        "121230223",
        "121291035",
        "121291115",
        "121296485",
        "220104085",
        "4cd548da9047172acfece395",
        "61709:3634424",
        "693530:4230920",
        "693533:4230923",
        "783731:4321121",
        "818582:4355972",
        "818591:4355981",
    }
)
MISSING_JUICE_FRUIT_ONLY_IDS = frozenset(
    {
        "121220097",
        "3c8291fd8bb68c6030e564d0",
        "684869:4222259",
        "8362:8365",
        "BTY-X17427700320021",
    }
)
MISSING_JUICE_VEGETABLE_ONLY_IDS = frozenset({"40114:40117"})
MISSING_JUICE_MIXED_IDS = frozenset(
    {
        "121219952",
        "684953:4222343",
        "8c192683e56e4a336c1b16a6",
        "BTY-X17427600320021",
    }
)

FORCED_STILL_IDS = frozenset(
    {
        "03f69e37a32ef60be065c483",
        "40114:40117",
        "582181:4119571",
        "8362:8365",
        "8a25dbbaf94cbcf6f8de8ee5",
        "BTY-X16027500320021",
    }
)

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


def reject_nonfinite_number(value: str) -> None:
    raise ValueError(f"Nem véges JSON-szám: {value}")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite_number,
        )


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
            if re.search(r"\bipa\b", text):
                additions.append("IPA")
            if re.search(r"\bapa\b", text):
                additions.append("APA")
            if re.search(r"\bale\b", text):
                additions.append("ale")
            if additions:
                append_list(props, "sörtípus", additions)
            elif "lager" not in text:
                append_list(props, "sörtípus", ["felsőerjesztésű sör"])
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
            # Szándékosan a forrásjelölő marad meg eddig a pontig: a későbbi,
            # exact ID-készletekkel védett lé-normalizáló választ valódi célágat.
            append_list(props, "lé típusa", ["gyümölcs- és zöldséglé"])
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
    if product_id(product) == FRUIT_STEP_GINGER_ID:
        new_props["gyümölcs"] = ["citrom"]
        new_props["összetevő"] = ["gyömbér"]
    else:
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


def remove_folded_atoms(
    props: dict[str, Any],
    property_name: str,
    folded_values: set[str] | frozenset[str],
) -> None:
    if property_name not in props:
        return
    kept = [
        value
        for value in values_of(props[property_name])
        if fold_text(value) not in folded_values
    ]
    if kept:
        props[property_name] = dedupe(kept)
    else:
        props.pop(property_name, None)


def normalize_juice_taxonomy(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    """A hibás 190-es gyűjtőágat és a bizonyított létípus-hibákat rendezi."""

    legacy_rows = []
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        juice_types = values_of((product.get("tulajdonsagok") or {}).get("lé típusa"))
        if any(fold_text(value) == "gyumolcs es zoldsegle" for value in juice_types):
            legacy_rows.append(product)

    legacy_ids = {product_id(product) for product in legacy_rows}
    if legacy_rows:
        digest = hashlib.sha256(
            "\n".join(sorted(legacy_ids)).encode("utf-8")
        ).hexdigest()
        if len(legacy_rows) != 190 or len(legacy_ids) != 190:
            raise RuntimeError(
                f"A régi vegyeslé-korpusz nem 190 egyedi rekord: "
                f"rows={len(legacy_rows)}, ids={len(legacy_ids)}"
            )
        if digest != LEGACY_MIXED_JUICE_ID_SHA256:
            raise RuntimeError(f"A régi vegyeslé-korpusz ID-hash-e eltér: {digest}")
        known_moved = SMOOTHIE_PUREE_IDS | FRUIT_DRINK_IDS | NECTAR_IDS
        if not known_moved < legacy_ids:
            raise RuntimeError(
                "Hiányzó exact vegyeslé-célrekordok: "
                f"{sorted(known_moved - legacy_ids)[:20]}"
            )

    for product in legacy_rows:
        item_id = product_id(product)
        props = product.get("tulajdonsagok") or {}
        if item_id in SMOOTHIE_PUREE_IDS:
            product["alkategoria"], product["altipus"] = (
                FRUIT_BRANCH,
                "Smoothie és püréital",
            )
            form = "smoothie" if "smoothie" in fold_text(product_name(product)) else "püré"
            append_list(props, "forma", [form])
            props.pop("lé típusa", None)
            operations["vegyeslé_smoothie_vagy_püréitalra_javítva"] += 1
        elif item_id in FRUIT_DRINK_IDS:
            product["alkategoria"], product["altipus"] = (
                FRUIT_BRANCH,
                "Gyümölcsital",
            )
            props.pop("lé típusa", None)
            operations["vegyeslé_gyümölcsitalra_javítva"] += 1
        elif item_id in NECTAR_IDS:
            product["alkategoria"], product["altipus"] = (
                FRUIT_BRANCH,
                "Nektár",
            )
            props.pop("lé típusa", None)
            operations["vegyeslé_nektárra_javítva"] += 1
        else:
            product["alkategoria"], product["altipus"] = FRUIT_BRANCH, "Lé"
            if item_id in LEGACY_JUICE_VEGETABLE_ONLY_IDS:
                props["lé típusa"] = ["zöldséglé"]
            elif item_id in LEGACY_JUICE_MIXED_IDS:
                props["lé típusa"] = ["gyümölcslé", "zöldséglé"]
            else:
                props["lé típusa"] = ["gyümölcslé"]
            operations["vegyeslé_atomi_létípusra_javítva"] += 1

    vegetable_only_ids = (
        LEGACY_JUICE_VEGETABLE_ONLY_IDS
        | EXTRA_JUICE_VEGETABLE_ONLY_IDS
        | MISSING_JUICE_VEGETABLE_ONLY_IDS
    )
    mixed_ids = (
        LEGACY_JUICE_MIXED_IDS
        | EXTRA_JUICE_MIXED_IDS
        | MISSING_JUICE_MIXED_IDS
    )
    fruit_only_ids = MISSING_JUICE_FRUIT_ONLY_IDS
    for product in products:
        if (
            product.get("fokategoria") != ITAL
            or product.get("alkategoria") != FRUIT_BRANCH
            or product.get("altipus") != "Lé"
        ):
            continue
        item_id = product_id(product)
        props = product.get("tulajdonsagok") or {}
        before = copy.deepcopy(props.get("lé típusa"))
        if item_id in vegetable_only_ids:
            props["lé típusa"] = ["zöldséglé"]
        elif item_id in mixed_ids:
            props["lé típusa"] = ["gyümölcslé", "zöldséglé"]
        elif item_id in fruit_only_ids:
            props["lé típusa"] = ["gyümölcslé"]
        if before != props.get("lé típusa"):
            operations["egyéb_bizonyított_létípus_javítva"] += 1


BRAND_MAIN_MAP = {
    "African Rock Selection": "African Rock",
    "ANGYAL": "Angyal Borászat",
    "Angyal Borászat Mosoly Tokaji Édes Cuvée": "Angyal Borászat",
    "Aperitivo Bianco": "Aperitivo",
    "Aperitivo Cherry": "Aperitivo",
    "Arran Barrel Reserve": "Arran",
    "ASAHI": "Asahi",
    "Asahi Super Dry": "Asahi",
    "AVE Aloe Vera": "AVE",
    "Bad Dogs Bulldog IPA": "Bad Dogs",
    "Bad Dogs Mopsz Meggy": "Bad Dogs",
    "Bad Dogs Puli Pils": "Bad Dogs",
    "BEERCOOL": "BE(er) Cool",
    "BOLYKI": "Bolyki",
    "Bolyki János": "Bolyki",
    "Bols Advocaat": "Bols",
    "Bols Marine": "Bols",
    "Bostavan Gold Premium": "Bostavan",
    "Bulleit Bourbon": "Bulleit",
    "Desszert Triple Sec": "Desszert",
    "Douwe Egberts Omnia": "Douwe Egberts",
    "Douwe Egberts Paloma": "Douwe Egberts",
    "Dr. Chen Patika": "Dr. Chen",
    "Dúzsi Tamás": "Dúzsi",
    "Egri Korona Borház": "Egri Korona",
    "Emese": "Theodora",
    "Fantasy Cabernet Sauvignon": "Fantasy",
    "Fantasy Chardonnay": "Fantasy",
    "Fantasy Muscat Rose": "Fantasy",
    "FEHÉRVÁRI Borbirtok": "Fehérvári",
    "Fonte Active": "Fonte",
    "Fonte Beauty": "Fonte",
    "Fonte Boost": "Fonte",
    "Fonte Natura": "Fonte",
    "Frescanti Cherry": "Frescanti",
    "Gere Tamás": "Gere Tamás & Zsolt",
    "Gedeon Birtok Brut": "Gedeon",
    "Günzer": "Günzer Tamás",
    "Haas Classic": "Haas",
    "HB": "Hofbräu München",
    "Horizont Brewing": "Horizont",
    "Ikon Pincészet": "Ikon",
    "Katona Nálad Vagy Nálam": "Katona",
    "Krušovice Černé": "Krusovice",
    "Krušovice Originál": "Krusovice",
    "La Festa Hot Chocolatta Classico": "La Festa",
    "Laposa Méthode Charmat": "Laposa",
    "Limenita Freshing Coolture": "Limenita",
    "Limenita Golden Sweet": "Limenita",
    "London Fruit & Herb Company": "London Fruit & Herb",
    "Maczkó Medve Álom": "Maczkó",
    "MATUA": "Matua",
    "Matua Valley": "Matua",
    "Mészáros": "Mészáros Pál",
    "Monkey Shoulder The Original": "Monkey Shoulder",
    "Nestlé Ricoré 3in1": "Nestlé Ricoré",
    "Nicolaus Extra Fine": "Nicolaus",
    "NIKKA": "Nikka",
    "Nikka Days": "Nikka",
    "Ostoros Hugo Spritz": "Ostorosbor",
    "Paloma Classic": "Douwe Egberts",
    "Pannonhalmi Tricollis": "Pannonhalmi Főapátság",
    "Pannonhalmi Tricollis Fehér": "Pannonhalmi Főapátság",
    "Panyolai Elixír": "Panyolai",
    "PATRON": "Patrón",
    "Patrón Silver": "Patrón",
    "Peroni Nastro Azzurro": "Peroni",
    "Piknik Selection": "Piknik",
    "Rio Cold Press": "RIO",
    "S. Pellegrino": "San Pellegrino",
    "Szent Gaál Twist": "Szent Gaál",
    "Sodastream Classics": "Sodastream",
    "Szovjetszkoje Igristoje": "Szovjetszkoje Igrisztoje",
    "Swiss": "Swiss Laboratory",
    "Takamaka Dark Spiced": "Takamaka",
    "Takamaka Koko": "Takamaka",
    "Teeling Whiskey Small Batch": "Teeling",
    "The Deli": "Rio D'Oro",
    "Three Sixty Vodka": "Three Sixty",
    "Tiffán's": "Tiffán",
    "Velkopopovický Kozel Premium Lager": "Kozel",
    "Veuve Pelletier Ponsardin": "Veuve Pelletier",
    "Vitamizu Minions": "Vitamizu",
    "Vitamizu Mizu Mate Classic": "Vitamizu",
    "Vitamizu Mizu Mate Grapefruit-Lime": "Vitamizu",
    "Vitamizu Stumble Guys": "Vitamizu",
    "Yo": "YO",
    "YO Sirup": "YO",
    "Zuegg Intenso": "Zuegg",
    "Zuegg Zero": "Zuegg",
}

BRAND_FAMILY_BY_SOURCE = {
    "African Rock Selection": "Selection",
    "Douwe Egberts Omnia": "Omnia",
    "Douwe Egberts Paloma": "Paloma",
    "Emese": "Emese",
    "La Festa Hot Chocolatta Classico": "Hot Chocolatta",
    "Nikka Days": "Days",
    "Ostoros Hugo Spritz": "Hugo Spritz",
    "Paloma Classic": "Paloma",
    "Pannonhalmi Tricollis": "Tricollis",
    "Pannonhalmi Tricollis Fehér": "Tricollis",
    "Panyolai Elixír": "Elixír",
    "Peroni Nastro Azzurro": "Nastro Azzurro",
    "Rio Cold Press": "Cold Press",
}

BRAND_VARIANT_BY_SOURCE = {
    "African Rock Selection": "Selection",
    "Aperitivo Bianco": "Bianco",
    "Aperitivo Cherry": "Cherry",
    "Bad Dogs Bulldog IPA": "Bulldog IPA",
    "Bad Dogs Mopsz Meggy": "Mopsz Meggy",
    "Bad Dogs Puli Pils": "Puli Pils",
    "Bostavan Gold Premium": "Gold Premium",
    "Fonte Active": "Active",
    "Fonte Beauty": "Beauty",
    "Fonte Boost": "Boost",
    "Fonte Natura": "Natura",
    "Krušovice Černé": "Černé",
    "Krušovice Originál": "Originál",
    "La Festa Hot Chocolatta Classico": "Classico",
    "Nicolaus Extra Fine": "Extra Fine",
    "Pannonhalmi Tricollis Fehér": "Fehér",
    "Patrón Silver": "Silver",
    "Piknik Selection": "Selection",
    "Szent Gaál Twist": "Twist",
    "Takamaka Dark Spiced": "Dark Spiced",
    "Takamaka Koko": "Koko",
    "Veuve Pelletier Ponsardin": "Ponsardin",
    "Vitamizu Minions": "Minions",
    "Vitamizu Mizu Mate Classic": "Mizu Mate Classic",
    "Vitamizu Mizu Mate Grapefruit-Lime": "Mizu Mate Grapefruit-Lime",
    "Vitamizu Stumble Guys": "Stumble Guys",
    "Zuegg Intenso": "Intenso",
    "Zuegg Zero": "Zero",
}


def normalize_brand_semantics(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    """Csak bizonyított termékcsaládokat választ le a főmárkáról."""

    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        props = product.get("tulajdonsagok") or {}
        source_brand = props.get("márka")
        if source_brand in BRAND_FAMILY_BY_SOURCE:
            append_list(
                props,
                "termékcsalád",
                [BRAND_FAMILY_BY_SOURCE[source_brand]],
            )
            operations["márkából_termékcsalád_leválasztva"] += 1
        if source_brand in BRAND_VARIANT_BY_SOURCE:
            append_list(
                props,
                "változat",
                [BRAND_VARIANT_BY_SOURCE[source_brand]],
            )
            operations["márkából_változat_leválasztva"] += 1
        if source_brand in BRAND_MAIN_MAP:
            props["márka"] = BRAND_MAIN_MAP[source_brand]
            operations["márka_főmárkára_egyszerűsítve"] += 1
        brand = props.get("márka")
        text = fold_text(product_name(product))

        if brand == "YO":
            append_list(props, "terméktípus", ["szörp"])
        if brand == "Asahi" and "super dry" in text:
            append_list(props, "változat", ["Super Dry"])
            remove_folded_atoms(props, "íz", {"super dry"})
        if brand == "Angyal Borászat" and "mosoly" in text:
            append_list(props, "változat", ["Mosoly"])
        if brand == "Teeling" and "small batch" in text:
            append_list(props, "változat", ["Small Batch"])
        if brand == "Monkey Shoulder" and "the original" in text:
            append_list(props, "változat", ["The Original"])
        if brand == "Maczkó" and "medve alom" in text:
            append_list(props, "változat", ["Medve Álom"])
        if brand == "Arran" and "barrel reserve" in text:
            append_list(props, "változat", ["Barrel Reserve"])
        if brand == "Haas" and re.search(r"\bclassic\b", text):
            append_list(props, "változat", ["Classic"])
        if brand == "Laposa" and "methode charmat" in text:
            append_list(props, "eljárás", ["Charmat"])
        if brand == "Douwe Egberts":
            if "omnia" in text:
                append_list(props, "termékcsalád", ["Omnia"])
            if "paloma" in text:
                append_list(props, "termékcsalád", ["Paloma"])
            if "paloma" in text and re.search(r"\bclassic\b", text):
                append_list(props, "változat", ["Classic"])
            elif "paloma" in text and "karavan" in text:
                append_list(props, "változat", ["Karaván"])
            elif "paloma" in text and "professional" in text:
                append_list(props, "változat", ["Professional"])
            remove_folded_atoms(props, "íz", {"classic", "paloma classic"})
        if brand == "Peroni" and "nastro azzurro" in text:
            append_list(props, "termékcsalád", ["Nastro Azzurro"])
        if brand == "Nikka" and re.search(r"\bdays\b", text):
            append_list(props, "termékcsalád", ["Days"])
        if brand == "Pannonhalmi Főapátság" and "tricollis" in text:
            append_list(props, "termékcsalád", ["Tricollis"])
        if brand == "Ostorosbor" and "hugo spritz" in text:
            append_list(props, "termékcsalád", ["Hugo Spritz"])
        if brand == "Nestlé Ricoré" and (
            "3in1" in text or "3 az 1" in text
        ):
            append_list(props, "változat", ["3in1"])
        if brand == "Desszert" and "triple sec" in text:
            append_list(props, "terméktípus", ["triple sec"])
        if brand == "Fantasy":
            if "cabernet sauvignon" in text:
                append_list(props, "szőlőfajta", ["Cabernet Sauvignon"])
            elif "chardonnay" in text:
                append_list(props, "szőlőfajta", ["Chardonnay"])
            elif "muscat" in text:
                append_list(props, "szőlőfajta", ["Muscat"])
        if brand == "Limenita":
            if "golden sweet" in text:
                append_list(props, "változat", ["Golden Sweet"])
            elif "freshing coolture" in text:
                append_list(props, "változat", ["Freshing Coolture"])
            elif re.search(r"\bblue\b", text):
                append_list(props, "változat", ["Blue"])
            # A „lime” érték mind a kilenc rekordnál kizárólag a márkanévből
            # szivárgott be, egyik termék neve/címkéje sem lime ízű.
            remove_folded_atoms(props, "íz", {"lime"})
        if brand == "Kozel" and "premium lager" in text:
            append_list(props, "változat", ["Premium"])
            append_list(props, "sörtípus", ["lager"])
            remove_folded_atoms(props, "íz", {"lager"})
        if brand == "Sodastream" and re.search(r"\bclassics\b", text):
            append_list(props, "változat", ["Classics"])
        if brand == "Bols" and "advocaat" in text:
            append_list(props, "terméktípus", ["tojáslikőr"])
            remove_folded_atoms(props, "fajta", {"tojaslikor"})
            remove_folded_atoms(props, "íz", {"tojaslikor"})
        if brand == "Bols" and re.search(r"\bmarine\b", text):
            append_list(props, "változat", ["Marine"])
        if brand == "Katona" and "nalad vagy nalam" in text:
            append_list(props, "változat", ["Nálad Vagy Nálam"])


def normalize_beer_semantics(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    pilsner_false_ipa = frozenset({"1028287", "680000:4217390"})
    apa_ids = frozenset(
        {
            "121225339",
            "53cf74709f0aed73960662e0",
            "673034:4210424",
            "678785:4216175",
            "BTY-X17303200320021",
            "dea8ebbdd70dbb5168b50674",
        }
    )
    for product in products:
        if (
            product.get("fokategoria") != ITAL
            or product.get("altipus") != "Sör, radler és malátaital"
        ):
            continue
        item_id = product_id(product)
        props = product.get("tulajdonsagok") or {}
        before = copy.deepcopy(props.get("sörtípus"))
        if item_id in pilsner_false_ipa:
            remove_folded_atoms(props, "sörtípus", {"ipa"})
        elif item_id == "678794:4216184":
            props["sörtípus"] = ["pils"]
        elif item_id == "780917:4318307":
            remove_folded_atoms(props, "sörtípus", {"felsoerjesztesu sor"})
            append_list(props, "sörtípus", ["lager"])
        elif item_id == "789926:4327316":
            remove_folded_atoms(props, "sörtípus", {"felsoerjesztesu sor"})
            append_list(props, "sörtípus", ["lager", "India Pale Lager"])
        elif item_id == "BTY-X17887400320021":
            append_list(props, "sörtípus", ["ale", "búzasör"])
        if item_id in apa_ids:
            append_list(props, "sörtípus", ["APA"])
        if "sörtípus" in props:
            canonical = {
                "apa": "APA",
                "ipa": "IPA",
                "new england ipa": "New England IPA",
                "session ipa": "Session IPA",
            }
            props["sörtípus"] = dedupe(
                canonical.get(fold_text(value), value)
                for value in values_of(props["sörtípus"])
            )
        if before != props.get("sörtípus"):
            operations["sörtípus_bizonyított_hibája_javítva"] += 1


CHILD_NAME_RE = re.compile(
    r"\b(?:gyerek\w*|gyermek\w*|kids?|baby|junior|babaviz|babaknak)\b"
    r"|\bbaba\s+mama\b"
)


def normalize_proven_product_semantics(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        props = product.get("tulajdonsagok") or {}
        item_id = product_id(product)
        if (
            product.get("alkategoria") == SOFT_BRANCH
            and product.get("altipus") == "Jegestea"
            and props.get("márka") == "Nestea"
        ) or item_id in FORCED_STILL_IDS:
            if props.get("szénsavasság") != "szénsavmentes":
                props["szénsavasság"] = "szénsavmentes"
                operations["bizonyítottan_szénsavmentes_termék_javítva"] += 1
        if CHILD_NAME_RE.search(fold_text(product_name(product))):
            before = copy.deepcopy(props.get("célcsoport"))
            append_list(props, "célcsoport", ["gyerek"])
            if before != props.get("célcsoport"):
                operations["gyerek_célcsoport_pótolva"] += 1
        if item_id == "BTY-X17833000320021":
            props["cukormentes / zero"] = True
            operations["Royal_Crown_cukormentes_javítva"] += 1


def normalize_atomic_semantics(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    """A bizonyítottan összetett értékeket és főmárkákat normalizálja."""

    normalize_juice_taxonomy(products, operations)
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        props = product.get("tulajdonsagok") or {}
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
            elif "kavefeherito" in name:
                product_type = "kávéfehérítő"
            else:
                product_type = "kávékrémpor"
            props["terméktípus"] = [product_type]
            props.pop("fajta", None)
            props.pop("típus", None)
            operations["kávéadalék_típusa_atomizálva"] += 1

    normalize_brand_semantics(products, operations)
    normalize_beer_semantics(products, operations)
    normalize_proven_product_semantics(products, operations)


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
            if props.get("gyümölcs") != ["citrom"]:
                props["gyümölcs"] = ["citrom"]
                operations["Fruit_Step_gyümölcstengelye_javítva"] += 1
            before_ingredients = copy.deepcopy(props.get("összetevő"))
            append_list(props, "összetevő", ["gyömbér"])
            if before_ingredients != props.get("összetevő"):
                operations["Fruit_Step_gyömbér_összetevője_pótolva"] += 1


ORIGIN_ALIASES = {
    "Balatonboglári": "Balatonboglár",
    "Balatonmelléke": "Balatonmellék",
    "Balatonmelléki": "Balatonmellék",
    "Duna-Tisza közi": "Duna-Tisza köze",
    "Egri": "Eger",
    "Etyek-Budai": "Etyek-Buda",
    "Felső-Magyarországi": "Felső-Magyarország",
    "Kunsági": "Kunság",
    "Mátrai": "Mátra",
    "Neszmélyi": "Neszmély",
    "Tokaji": "Tokaj",
    "Villányi": "Villány",
}

WINE_GRAPE_VALUES = frozenset(
    {
        "cabernet",
        "Cabernet Franc",
        "Cabernet Sauvignon",
        "Carmenere",
        "Chardonnay",
        "chardonnay",
        "Chenin Blanc",
        "Cirfandli",
        "Colombard",
        "Csabagyöngye",
        "Cserszegi fűszeres",
        "Ezerjó",
        "fekete leányka",
        "Furmint",
        "Garnacha",
        "Garnacha Blanca",
        "Garnacha Tinta",
        "Generosa",
        "Grillo",
        "Hárslevelű",
        "Irsai Olivér",
        "Juhfark",
        "Kadarka",
        "Királyleányka",
        "Kékfrankos",
        "Kéknyelű",
        "Macabeo",
        "Malbec",
        "Medina",
        "Menoire",
        "Merlot",
        "Moscato",
        "Muscat",
        "Muscat Blanc",
        "Muscat Lunel",
        "Muscat Ottonel",
        "muskotály",
        "Nero d'Avola",
        "olaszrizling",
        "Pinot Grigio",
        "Pinot Noir",
        "Pinotage",
        "Portugieser",
        "Primitivo",
        "Rajnai Rizling",
        "riesling",
        "rizling",
        "Sangiovese",
        "Sauvignon Blanc",
        "Shiraz",
        "syrah",
        "Szürkebarát",
        "Sárgamuskotály",
        "Tempranillo",
        "Tramini",
        "Trebbiano",
        "Turán",
        "Verdejo",
        "Viura",
        "Zenit",
        "Zeus",
        "Zinfandel",
        "Zweigelt",
        "zöld veltelini",
    }
)
WINE_GRAPE_CANONICAL = {
    "cabernet": "Cabernet",
    "chardonnay": "Chardonnay",
    "fekete leányka": "Fekete leányka",
    "muskotály": "Muskotály",
    "olaszrizling": "Olaszrizling",
    "riesling": "Riesling",
    "rizling": "Rizling",
    "Shiraz": "Syrah",
    "syrah": "Syrah",
    "zöld veltelini": "Zöld veltelini",
}
WINE_STYLE_CANONICAL = {
    "Bikavér": "bikavér",
    "Bikavér Superior": "bikavér superior",
    "cuvée": "cuvée",
    "desszertbor": "desszertbor",
    "Egri Bikavér": "bikavér",
    "Egri Csillag": "egri csillag",
    "jégbor": "jégbor",
    "késői szüret": "késői szüret",
    "Late Harvest": "késői szüret",
    "Ruby Port": "ruby port",
    "siller": "siller",
    "Szamorodni": "szamorodni",
    "tawny": "tawny port",
    "Tawny Port": "tawny port",
    "Tokaji Aszú": "aszú",
    "Tokaji Szamorodni": "szamorodni",
}
WINE_COLOR_CANONICAL = {"Rosé": "rozé", "Rozé": "rozé"}
WINE_TYPE_CANONICAL = {"prosecco": "prosecco"}

WINE_CONTEXT_FIXES_BY_ID = {
    "24418:24421": {
        "remove": ("Saint", "Émilion"),
        "eredet": ("Montagne-Saint-Émilion",),
    },
    "38053:38056": {
        "remove": ("Saint", "Émilion"),
        "eredet": ("Saint-Émilion",),
    },
    "65615:3602696": {
        "remove": ("Haut", "Médoc"),
        "eredet": ("Haut-Médoc",),
    },
    "24460:24463": {
        "remove": ("Médoc",),
        "eredet": ("Médoc",),
    },
    "24430:24433": {
        "remove": ("Pouilly", "Fuissé"),
        "eredet": ("Pouilly-Fuissé",),
    },
    "BTY-X17339500320021": {
        "remove": ("More",),
        "változat": ("Zenit & More",),
    },
    "12712:12715": {
        "remove": ("Sauvignon",),
        "szőlőfajta": ("Cabernet Sauvignon",),
    },
}

WINE_MANUAL_VALUE_MAP: dict[str, dict[str, Any]] = {
    "5 puttonyos": {"borstílus": ("aszú",), "puttonyszám": "5"},
    "Aligvárom": {"változat": ("Aligvárom",)},
    "Aszú 4 puttonyos": {"borstílus": ("aszú",), "puttonyszám": "4"},
    "Aszú 5 puttonyos": {"borstílus": ("aszú",), "puttonyszám": "5"},
    "Aszú 6 puttonyos": {"borstílus": ("aszú",), "puttonyszám": "6"},
    "Beaujolais": {"eredet": ("Beaujolais",)},
    "Big Band": {"változat": ("Big Band",)},
    "Blanc Cuvée": {"borstílus": ("cuvée",), "szín": ("fehér",)},
    "Bodorka": {"változat": ("Bodorka",)},
    "Bordeaux cuvée": {"borstílus": ("cuvée",), "eredet": ("Bordeaux",)},
    "Bordeaux Superieur": {"eredet": ("Bordeaux Supérieur",)},
    "Cabernet Rosé": {"szőlőfajta": ("Cabernet",), "szín": ("rozé",)},
    "Cabernet Sauvignon Rosé": {
        "szőlőfajta": ("Cabernet Sauvignon",),
        "szín": ("rozé",),
    },
    "cherry": {"íz": ("cseresznye",)},
    "Chianti": {"eredet": ("Chianti",)},
    "Civilis Cuvée": {"borstílus": ("cuvée",), "változat": ("Civilis",)},
    "Cuvée 11": {"borstílus": ("cuvée",), "változat": ("Cuvée 11",)},
    "Cuvée 13": {"borstílus": ("cuvée",), "változat": ("Cuvée 13",)},
    "Cuvée 7": {"borstílus": ("cuvée",), "változat": ("Cuvée 7",)},
    "Côtes du Rhône": {"eredet": ("Côtes du Rhône",)},
    "Egri Rozé": {"eredet": ("Eger",), "szín": ("rozé",)},
    "egyéb": {"discard": True},
    "erdei gyümölcs": {
        "borstílus": ("gyümölcsbor",),
        "íz": ("erdei gyümölcs",),
    },
    "Ermitage": {"borstílus": ("cuvée",), "változat": ("Ermitage",)},
    "Estve": {"változat": ("Estve",)},
    "Fajzat Cuvée": {"borstílus": ("cuvée",), "változat": ("Fajzat",)},
    "fehér cuvée": {"borstílus": ("cuvée",), "szín": ("fehér",)},
    "feketeribizlibor": {
        "alap": ("fekete ribizli",),
        "borstílus": ("gyümölcsbor",),
    },
    "Filigrán Cuvée": {"borstílus": ("cuvée",), "változat": ("Filigrán",)},
    "Franc": {"szőlőfajta": ("Cabernet Franc",)},
    "Fuissé": {"context_only": True},
    "Grand Cuvée": {
        "borstílus": ("cuvée",),
        "változat": ("Grand Cuvée",),
    },
    "Grandiózus Malbec": {
        "szőlőfajta": ("Malbec",),
        "változat": ("Grandiózus",),
    },
    "Grandiózus Syrah": {
        "szőlőfajta": ("Syrah",),
        "változat": ("Grandiózus",),
    },
    "GT Rosé": {"szín": ("rozé",), "változat": ("GT",)},
    "Halfarka": {"változat": ("Halfarka",)},
    "Haut": {"context_only": True},
    "Ihlet Cuvée": {"borstílus": ("cuvée",), "változat": ("Ihlet",)},
    "Immortal": {"változat": ("Immortal",)},
    "Indián Nyár Cuvée": {
        "borstílus": ("cuvée",),
        "változat": ("Indián Nyár",),
    },
    "K2": {"változat": ("K2",)},
    "Kopar": {"változat": ("Kopar",)},
    "Kopar Cuvée": {"borstílus": ("cuvée",), "változat": ("Kopar",)},
    "Kékfrankos Rosé": {
        "szőlőfajta": ("Kékfrankos",),
        "szín": ("rozé",),
    },
    "Lezser": {"változat": ("Lezser",)},
    "Libra Cuvée": {"borstílus": ("cuvée",), "változat": ("Libra",)},
    "Margaux": {"eredet": ("Margaux",)},
    "meggybor": {"alap": ("meggy",), "borstílus": ("gyümölcsbor",)},
    "Merlot Cuvée": {"borstílus": ("cuvée",), "szőlőfajta": ("Merlot",)},
    "Merlot Rosé": {"szőlőfajta": ("Merlot",), "szín": ("rozé",)},
    "Mirtill Cuvée": {"borstílus": ("cuvée",), "változat": ("Mirtill",)},
    "Montepulciano": {"szőlőfajta": ("Montepulciano",)},
    "Montepulciano d'Abruzzo": {
        "eredet": ("Abruzzo",),
        "szőlőfajta": ("Montepulciano",),
    },
    "More": {"context_only": True},
    "Médoc": {"context_only": True},
    "Olivér Cuvée": {"borstílus": ("cuvée",), "változat": ("Olivér",)},
    "Olívia": {"változat": ("Olívia",)},
    "Olívia Cuvée": {"borstílus": ("cuvée",), "változat": ("Olívia",)},
    "Pannon Cuvée Blanc": {
        "borstílus": ("cuvée",),
        "szín": ("fehér",),
        "változat": ("Pannon",),
    },
    "PortaGéza": {"változat": ("PortaGéza",)},
    "Pouilly": {"context_only": True},
    "Principium": {"változat": ("Principium",)},
    "Regnum Cuvée": {"borstílus": ("cuvée",), "változat": ("Regnum",)},
    "Rosso Toscana": {"eredet": ("Toscana",), "szín": ("vörös",)},
    "Rosé Cuvée": {"borstílus": ("cuvée",), "szín": ("rozé",)},
    "Royal": {"változat": ("Royal",)},
    "Royal Cuvée": {"borstílus": ("cuvée",), "változat": ("Royal",)},
    "Rozé Cuvée": {"borstílus": ("cuvée",), "szín": ("rozé",)},
    "Saint": {"context_only": True},
    "Somlói Cuvée": {"borstílus": ("cuvée",), "eredet": ("Somló",)},
    "Syrah Rosé": {"szőlőfajta": ("Syrah",), "szín": ("rozé",)},
    "Tempranillo Roble": {
        "szőlőfajta": ("Tempranillo",),
        "érlelés": ("roble",),
    },
    "Tricollis": {"változat": ("Tricollis",)},
    "Tricollis Vörös": {"szín": ("vörös",), "változat": ("Tricollis",)},
    "Trió Cuvée": {"borstílus": ("cuvée",), "változat": ("Trió",)},
    "Töpszli Cuvée": {"borstílus": ("cuvée",), "változat": ("Töpszli",)},
    "Vörös Cuvée": {"borstílus": ("cuvée",), "szín": ("vörös",)},
    "White Cuvée": {"borstílus": ("cuvée",), "szín": ("fehér",)},
    "áfonya": {"íz": ("áfonya",)},
    "Émilion": {"context_only": True},
    "muskotályos": {"discard": True},
    "Olivier": {"változat": ("Olivier",)},
    "Sauvignon": {"context_only": True},
}

FUNCTION_VALUE_MAP = {
    "antiox": "antioxidáns",
    "beauty": "szépség",
    "detox": "detox",
    "emesztes": "emésztés támogatása",
    "emesztes tamogatasa": "emésztés támogatása",
    "energie": "energia",
    "immun": "immunrendszer támogatása",
    "immunity": "immunrendszer támogatása",
    "koncentracio": "koncentráció",
    "nyugodt alvas": "nyugodt alvás",
    "regeneration": "regeneráció",
    "relax": "relaxáció",
}
ACTIVE_INGREDIENT_VALUES = frozenset(
    {"b5 vitamin", "b vitamin komplex", "c vitamin", "cink", "ginseng"}
)
INSTANT_CORRECTION_IDS = frozenset(
    {
        "100241927",
        "111274825",
        "111274827",
        "111275295",
        "70f8217f1c3b2c6ac11133f4",
    }
)


def normalize_origin_axis(
    props: dict[str, Any],
    operations: Counter[str],
) -> None:
    if "borvidék / eredet" not in props:
        return
    raw_values = values_of(props.pop("borvidék / eredet"))
    for value in raw_values:
        folded = fold_text(value)
        if folded in {"", "egyeb"}:
            continue
        if folded == "egri rose":
            append_list(props, "eredet", ["Eger"])
            append_list(props, "borstílus", ["rozé"])
            continue
        append_list(props, "eredet", [ORIGIN_ALIASES.get(str(value), value)])
    operations["borvidék_eredet_tengely_atomizálva"] += 1


def normalize_wine_descriptor_axis(
    product: dict[str, Any],
    props: dict[str, Any],
    operations: Counter[str],
) -> None:
    if "szőlőfajta / borstílus" not in props:
        return
    raw_values = values_of(props.pop("szőlőfajta / borstílus"))
    context_fix = WINE_CONTEXT_FIXES_BY_ID.get(product_id(product), {})
    removed = {
        fold_text(value)
        for value in context_fix.get("remove", ())
    }
    for property_name, additions in context_fix.items():
        if property_name == "remove":
            continue
        append_list(props, property_name, additions)

    for value in raw_values:
        if fold_text(value) in removed:
            continue
        if value in WINE_GRAPE_VALUES:
            append_list(
                props,
                "szőlőfajta",
                [WINE_GRAPE_CANONICAL.get(value, value)],
            )
            continue
        if value in WINE_STYLE_CANONICAL:
            append_list(props, "borstílus", [WINE_STYLE_CANONICAL[value]])
            if value.startswith("Egri "):
                append_list(props, "eredet", ["Eger"])
            if value.startswith("Tokaji "):
                append_list(props, "eredet", ["Tokaj"])
            continue
        if value in WINE_COLOR_CANONICAL:
            append_list(props, "szín", [WINE_COLOR_CANONICAL[value]])
            continue
        if value in WINE_TYPE_CANONICAL:
            append_list(props, "bortípus", [WINE_TYPE_CANONICAL[value]])
            continue
        mapping = WINE_MANUAL_VALUE_MAP.get(str(value))
        if mapping is None:
            raise RuntimeError(
                f"Ismeretlen szőlőfajta/borstílus érték: "
                f"{product_id(product)} / {value!r}"
            )
        if mapping.get("context_only"):
            raise RuntimeError(
                f"Kontextus nélkül maradt tört borérték: "
                f"{product_id(product)} / {value!r}"
            )
        if mapping.get("discard"):
            continue
        for property_name, additions in mapping.items():
            if isinstance(additions, tuple):
                append_list(props, property_name, additions)
            else:
                set_scalar(props, property_name, additions)

    grape_values = values_of(props.get("szőlőfajta"))
    grape_folds = {fold_text(value) for value in grape_values}
    if "cabernet" in grape_folds and {
        "cabernet franc",
        "cabernet sauvignon",
    } & grape_folds:
        remove_folded_atoms(props, "szőlőfajta", {"cabernet"})
    operations["szőlőfajta_borstílus_tengely_atomizálva"] += 1


def normalize_function_axis(
    props: dict[str, Any],
    operations: Counter[str],
) -> None:
    if "hatóanyag / cél" not in props:
        return
    raw_values = values_of(props.pop("hatóanyag / cél"))
    for value in raw_values:
        folded = fold_text(value)
        if folded in ACTIVE_INGREDIENT_VALUES:
            canonical = {
                "b5 vitamin": "B5-vitamin",
                "b vitamin komplex": "B-vitamin komplex",
                "c vitamin": "C-vitamin",
                "cink": "cink",
                "ginseng": "ginseng",
            }[folded]
            append_list(props, "hatóanyag", [canonical])
        elif folded in FUNCTION_VALUE_MAP:
            append_list(props, "funkció", [FUNCTION_VALUE_MAP[folded]])
        else:
            raise RuntimeError(f"Ismeretlen hatóanyag/cél érték: {value!r}")
    operations["hatóanyag_cél_tengely_atomizálva"] += 1


def normalize_container_axis(
    props: dict[str, Any],
    operations: Counter[str],
) -> None:
    if "palack" not in props:
        return
    raw_values = values_of(props.pop("palack"))
    for value in raw_values:
        folded = fold_text(value)
        if folded == "uveg":
            append_list(props, "csomagolás", ["palack"])
            append_list(props, "csomagolás anyaga", ["üveg"])
        elif folded == "muanyag":
            append_list(props, "csomagolás", ["palack"])
            append_list(props, "csomagolás anyaga", ["műanyag"])
        elif folded == "bag in box":
            append_list(props, "csomagolás", ["bag-in-box"])
        elif folded == "keg":
            append_list(props, "csomagolás", ["hordó"])
        elif folded == "doboz":
            append_list(props, "csomagolás", ["doboz"])
        else:
            raise RuntimeError(f"Ismeretlen régi palackérték: {value!r}")
    operations["palack_tengely_csomagolásra_bontva"] += 1


def normalize_coffee_composition(
    props: dict[str, Any],
    operations: Counter[str],
) -> None:
    if "összetétel" not in props:
        return
    raw_values = values_of(props.pop("összetétel"))
    for value in raw_values:
        text = fold_text(value)
        matches = re.findall(r"(\d+)\s*arabica|(\d+)\s*robusta", text)
        if not matches:
            raise RuntimeError(f"Ismeretlen kávéösszetétel: {value!r}")
        for arabica, robusta in matches:
            if arabica:
                append_list(props, "kávéfajta", ["arabica"])
                set_scalar(props, "arabica arány", f"{arabica}%")
            if robusta:
                append_list(props, "kávéfajta", ["robusta"])
                set_scalar(props, "robusta arány", f"{robusta}%")
    operations["kávéösszetétel_atomizálva"] += 1


def normalize_misc_property_axes(
    product: dict[str, Any],
    operations: Counter[str],
) -> None:
    props = product.get("tulajdonsagok") or {}
    if "cukormentes / zero" in props:
        props["cukormentes"] = bool(props.pop("cukormentes / zero"))
        operations["cukormentes_zero_tengely_átnevezve"] += 1

    if "püré" in props:
        if any(fold_text(value) == "igen" for value in values_of(props.pop("püré"))):
            props["pürét tartalmaz"] = True
        operations["püré_jelölés_logikaivá_alakítva"] += 1
    if "rostos" in props and not isinstance(props["rostos"], bool):
        props["rostos"] = any(
            fold_text(value) in {"igen", "true"}
            for value in values_of(props["rostos"])
        )
        operations["rostos_jelölés_logikaivá_alakítva"] += 1

    if "C-vitamin" in props:
        if props.pop("C-vitamin") is True:
            append_list(props, "tartalom", ["C-vitamin"])
        operations["C_vitamin_flag_tartalomba_vezetve"] += 1

    if product_id(product) in INSTANT_CORRECTION_IDS:
        props["instant"] = True
    if props.get("instant") is False:
        props.pop("instant")
        operations["hamis_instant_flag_törölve"] += 1

    if "zöldség" in props:
        append_list(props, "összetevő", values_of(props.pop("zöldség")))
        operations["zöldség_tengely_összetevőre_vezetve"] += 1

    if "alkohol" in props:
        raw_values = values_of(props.pop("alkohol"))
        for value in raw_values:
            folded = fold_text(value)
            if folded in {
                "aperitiv",
                "gin",
                "likor",
                "ouzo",
                "rum",
                "tequila",
                "vodka",
                "whisky",
            }:
                append_list(props, "alkoholalap", [value])
            elif folded == "tonik":
                append_list(props, "keverőanyag", ["tonik"])
            elif folded in {"alkoholos ital", "szeszesital", "anizs"}:
                continue
            else:
                raise RuntimeError(f"Ismeretlen alkoholalap-érték: {value!r}")
        name = fold_text(product_name(product))
        if "pastis" in name:
            append_list(props, "alkoholalap", ["pastis"])
        elif "abszint" in name:
            append_list(props, "alkoholalap", ["abszint"])
        operations["alkohol_tengely_alkoholalapra_bontva"] += 1

    normalize_origin_axis(props, operations)
    normalize_wine_descriptor_axis(product, props, operations)
    normalize_function_axis(props, operations)
    normalize_container_axis(props, operations)
    normalize_coffee_composition(props, operations)


def normalize_placeholder_and_text_values(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    placeholders = frozenset({"egyeb", "nem jelolt"})
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        props = product.get("tulajdonsagok") or {}
        for property_name, raw_value in list(props.items()):
            if isinstance(raw_value, bool):
                continue
            if isinstance(raw_value, list):
                cleaned = []
                for value in raw_value:
                    normalized = (
                        re.sub(r"\s+", " ", value).strip()
                        if isinstance(value, str)
                        else value
                    )
                    if isinstance(normalized, str) and fold_text(normalized) in placeholders:
                        continue
                    cleaned.append(normalized)
                cleaned = dedupe(cleaned)
                if cleaned:
                    props[property_name] = cleaned
                else:
                    props.pop(property_name, None)
            elif isinstance(raw_value, str):
                normalized = re.sub(r"\s+", " ", raw_value).strip()
                if not normalized or fold_text(normalized) in placeholders:
                    props.pop(property_name, None)
                else:
                    props[property_name] = normalized
        flavors = values_of(props.get("íz"))
        folded_flavors = {fold_text(value) for value in flavors}
        redundant_generics = set()
        if "sargarepa" in folded_flavors:
            redundant_generics.add("repa")
        if "oszibarack" in folded_flavors:
            redundant_generics.add("barack")
        if {"feketeribizli", "piros ribizli"} & folded_flavors:
            redundant_generics.add("ribizli")
        if {"kekszolo", "voros szolo"} & folded_flavors:
            redundant_generics.add("szolo")
        if redundant_generics:
            remove_folded_atoms(props, "íz", redundant_generics)
            operations["redundáns_generikus_ízérték_törölve"] += 1


HALF_PERCENT_BEER_IDS = frozenset(
    {
        "121227556",
        "3258894b9df044556713e967",
        "678971:4216361",
        "680045:4217435",
        "9fe1fad92de106673703c895",
        "a51fcde4249c0f2564c25818",
    }
)
LOOSE_TWININGS_IDS = frozenset(
    {
        "8131:8134",
        "BTY-X46022900320021",
        "bb4015d154f73a6a5332a3ef",
    }
)
WRONG_COLA_BASE_IDS = frozenset({"989120", "209543894", "220339659"})
TUTTIFRUTTI_INGREDIENT_NOISE_IDS = frozenset(
    {
        "0ab83ef40bba18b921ea51bc",
        "51789:52131",
        "583947:4121337",
    }
)
HAAS_FALSE_INSTANT_IDS = frozenset({"127538:3664736", "203228544"})


def normalize_semantic_value_axes(
    product: dict[str, Any],
    operations: Counter[str],
) -> None:
    """Bizonyított értékhibák és más tengelyre került atomok javítása."""

    props = product.get("tulajdonsagok") or {}
    item_id = product_id(product)
    name = fold_text(product_name(product))

    forms = values_of(props.get("forma"))
    if forms:
        kept_forms: list[Any] = []
        found_instant = False
        for value in forms:
            folded = fold_text(value)
            if folded == "instant":
                found_instant = True
                continue
            if folded == "instant italpor":
                found_instant = True
                kept_forms.append("italpor")
                continue
            kept_forms.append(value)
        if found_instant:
            props["instant"] = True
            if kept_forms:
                props["forma"] = dedupe(kept_forms)
            else:
                props.pop("forma", None)
            operations["instant_állapot_formából_leválasztva"] += 1
    for generic_property in ("típus", "fajta"):
        generic_values = values_of(props.get(generic_property))
        if any(fold_text(value) == "instant" for value in generic_values):
            remove_folded_atoms(props, generic_property, {"instant"})
            if item_id not in HAAS_FALSE_INSTANT_IDS:
                props["instant"] = True
            operations["instant_állapot_generikus_tengelyről_leválasztva"] += 1
    if re.search(r"\binstant\b|\bazonnal oldodo\b", name):
        if props.get("instant") is not True:
            props["instant"] = True
            operations["instant_névjelölés_pótolva"] += 1

    energy_status = props.pop("energia tartalom", None)
    if energy_status is not None:
        folded_energy = fold_text(energy_status)
        if folded_energy == "cukros":
            props["cukrozott"] = True
        elif folded_energy in {
            "energiamentes",
            "energiaszegeny",
            "csokkentett energiatartalmu",
        }:
            props["energiastátusz"] = str(energy_status)
        elif folded_energy not in {"", "egyeb", "nem jelolt"}:
            raise RuntimeError(
                f"Ismeretlen energia-/cukorstátusz: {item_id} / {energy_status!r}"
            )
        operations["energia_cukor_vegyes_tengely_szétválasztva"] += 1

    fat = props.get("zsírtartalom")
    if fat == ["1", "8%"] and "1 8" in name:
        props["zsírtartalom"] = ["1,8%"]
        operations["tört_zsírtartalom_javítva"] += 1
    elif fat == ["3", "5%"] and "3 5" in name:
        props["zsírtartalom"] = ["3,5%"]
        operations["tört_zsírtartalom_javítva"] += 1

    if item_id == "2807722":
        props["gyümölcstartalom"] = ["50,6%"]
        operations["tört_gyümölcstartalom_javítva"] += 1
    elif item_id == "BTY-X11998900320021":
        props["gyümölcstartalom"] = ["99,5%"]
        operations["tört_gyümölcstartalom_javítva"] += 1

    if item_id in HALF_PERCENT_BEER_IDS:
        props["alkoholtartalom"] = ["0,5%"]
        operations["dupla_alkoholfok_javítva"] += 1
    elif item_id == "121357396":
        # A gyártói termékoldal szerinti 12%; a forrás 53,5%-a nyilvánvaló
        # OCR/adatbeviteli hiba egy Brut Nature pezsgőnél.
        props["alkoholtartalom"] = ["12%"]
        operations["Sauska_alkoholfok_javítva"] += 1

    if item_id == "789008:4326398":
        props["kiszerelés"] = "330 ml"
        operations["Old_Jamaica_kiszerelés_javítva"] += 1
    elif item_id == "692993:4230383":
        props["csomagdarabszám"] = 6
        operations["multipack_darabszám_pótolva"] += 1
    elif item_id == "752013:4289403":
        props["csomagdarabszám"] = 4
        props["egységnyi kiszerelés"] = "330 ml"
        props["kiszerelés"] = "1320 ml"
        append_list(props, "csomagolás", ["multipack"])
        operations["multipack_darabszám_pótolva"] += 1

    content = values_of(props.get("tartalom"))
    if content:
        kept_content: list[Any] = []
        for value in content:
            folded = fold_text(value)
            if folded == "energia":
                append_list(props, "funkció", ["energia"])
            elif folded == "izotonias":
                append_list(props, "funkció", ["izotóniás"])
            elif folded == "alakreform":
                append_list(props, "funkció", ["alakreform"])
            elif folded == "rehab":
                append_list(props, "termékcsalád", ["Rehab"])
            elif folded == "koffeinmentes":
                props["koffeinmentes"] = True
            elif folded == "zold tea":
                append_list(props, "íz", ["zöld tea"])
            elif folded == "50 g protein":
                append_list(props, "fehérjetartalom", ["50 g"])
            elif folded == "hozzaadott vitaminok":
                kept_content.append("vitamin")
            else:
                kept_content.append(value)
        specific_vitamin = any(
            "vitamin" in fold_text(value) and fold_text(value) != "vitamin"
            for value in kept_content
        )
        if specific_vitamin:
            kept_content = [
                value for value in kept_content if fold_text(value) != "vitamin"
            ]
        kept_content = dedupe(kept_content)
        if kept_content:
            props["tartalom"] = kept_content
        else:
            props.pop("tartalom", None)
        if kept_content != content:
            operations["tartalom_tengely_atomizálva"] += 1

    flavors = values_of(props.get("íz"))
    if flavors:
        variant_atoms = {
            "barista": "Barista",
            "classic": "Classic",
            "classico": "Classico",
            "fusion": "Fusion",
            "gold": "Gold",
            "klasszikus": "Klasszikus",
            "premium": "Premium",
            "strong": "Strong",
            "tradicionalis": "Tradicionális",
            "yellow label": "Yellow Label",
        }
        retained_flavors: list[Any] = []
        flavor_changed = False
        for value in flavors:
            folded = fold_text(value)
            if folded in variant_atoms:
                append_list(props, "változat", [variant_atoms[folded]])
                flavor_changed = True
            elif folded == "decaffeinato":
                props["koffeinmentes"] = True
                flavor_changed = True
            elif folded in {"zero", "zero sugar", "zero cukor"}:
                props["cukormentes"] = True
                flavor_changed = True
            elif folded in {"szuretlen", "unfiltered"}:
                props["szűretlen"] = True
                flavor_changed = True
            elif folded in {"inulin", "kollagen"}:
                append_list(props, "tartalom", [value])
                flavor_changed = True
            elif folded == "immun cink":
                append_list(props, "funkció", ["immun"])
                append_list(props, "tartalom", ["cink"])
                flavor_changed = True
            else:
                retained_flavors.append(value)
        if retained_flavors:
            props["íz"] = dedupe(retained_flavors)
        else:
            props.pop("íz", None)
        if flavor_changed:
            operations["ízből_nem_íz_atom_külön_tengelyre_vezetve"] += 1

    fat_values = values_of(props.get("zsírtartalom"))
    if any(fold_text(value) == "zsirszegeny" for value in fat_values):
        props["zsírszegény"] = True
        remove_folded_atoms(props, "zsírtartalom", {"zsirszegeny"})
        operations["zsírszegény_státusz_tengelyre_vezetve"] += 1

    beer_values = values_of(props.get("sörtípus"))
    if beer_values:
        retained_beer_values: list[Any] = []
        beer_axis_changed = False
        for value in beer_values:
            folded = fold_text(value)
            if folded in {"vilagos", "barna", "dark"}:
                append_list(
                    props,
                    "szín",
                    ["barna" if folded in {"barna", "dark"} else "világos"],
                )
                beer_axis_changed = True
            elif folded == "premium":
                append_list(props, "minőség", ["prémium"])
                beer_axis_changed = True
            else:
                retained_beer_values.append(value)
        if retained_beer_values:
            props["sörtípus"] = dedupe(retained_beer_values)
        else:
            props.pop("sörtípus", None)
        if beer_axis_changed:
            operations["sörtípus_szín_minőség_atomjai_szétválasztva"] += 1

    if "puttonyszám" in props:
        raw_puttony = values_of(props["puttonyszám"])
        numeric_puttony = [
            int(value)
            for value in raw_puttony
            if isinstance(value, (int, str)) and str(value).isdigit()
        ]
        if len(numeric_puttony) != len(raw_puttony):
            raise RuntimeError(
                f"Nem numerikus puttonyszám: {item_id} / {raw_puttony!r}"
            )
        props["puttonyszám"] = numeric_puttony
        if raw_puttony != numeric_puttony:
            operations["puttonyszám_numerikussá_alakítva"] += 1

    def remove_redundant_axis_atoms(
        source_property: str,
        target_properties: tuple[str, ...],
    ) -> None:
        source_values = values_of(props.get(source_property))
        if not source_values:
            return
        dedicated = {
            fold_text(value)
            for target_property in target_properties
            for value in values_of(props.get(target_property))
        }
        redundant = {
            fold_text(value)
            for value in source_values
            if fold_text(value) in dedicated
        }
        if redundant:
            remove_folded_atoms(props, source_property, redundant)
            operations["rossz_tengelyen_duplikált_atom_törölve"] += 1

    remove_redundant_axis_atoms(
        "típus",
        (
            "édesség",
            "borstílus",
            "forma",
            "terméktípus",
            "sörtípus",
            "teatípus",
            "bortípus",
            "kávékeverék típusa",
        ),
    )
    remove_redundant_axis_atoms(
        "fajta",
        (
            "szín",
            "édesség",
            "forma",
            "szőlőfajta",
            "sörtípus",
            "terméktípus",
            "íz",
        ),
    )
    remove_redundant_axis_atoms(
        "íz",
        (
            "sörtípus",
            "eredet",
            "szőlőfajta",
            "alkoholalap",
            "kávékeverék típusa",
        ),
    )
    remove_redundant_axis_atoms("változat", ("kávékeverék típusa",))
    remove_redundant_axis_atoms("terméktípus", ("sörtípus",))

    if props.get("koffeinmentes") is True:
        remove_folded_atoms(
            props,
            "íz",
            {"koffeinmentes", "koffein mentes", "decaf"},
        )
    if props.get("cukormentes") is True:
        remove_folded_atoms(
            props,
            "íz",
            {"cukormentes", "no sugar", "sugarfree", "zero"},
        )
    if props.get("alkoholstátusz") == "alkoholmentes":
        remove_folded_atoms(props, "íz", {"alkoholmentes"})

    bases = values_of(props.get("alap"))
    if bases:
        normalized_bases = []
        for value in bases:
            folded = fold_text(value)
            if folded == "natur":
                continue
            if folded == "kola" and item_id in WRONG_COLA_BASE_IDS:
                continue
            if folded == "enyhen szensavas asvanyviz":
                normalized_bases.append("ásványvíz")
            else:
                normalized_bases.append(value)
        normalized_bases = dedupe(normalized_bases)
        if normalized_bases:
            props["alap"] = normalized_bases
        else:
            props.pop("alap", None)
        if normalized_bases != bases:
            operations["alap_tengely_zaja_javítva"] += 1
        normalized_base_folds = {
            fold_text(value) for value in values_of(props.get("alap"))
        }
        redundant_base_atoms = set()
        if "oszibarack" in normalized_base_folds:
            redundant_base_atoms.add("barack")
        if "barna rizs" in normalized_base_folds:
            redundant_base_atoms.add("rizs")
        if redundant_base_atoms:
            remove_folded_atoms(props, "alap", redundant_base_atoms)
            operations["redundáns_generikus_alapérték_törölve"] += 1

    if "csokolad" in name:
        before = copy.deepcopy(props.get("összetevő"))
        remove_folded_atoms(props, "összetevő", {"kola"})
        if before != props.get("összetevő"):
            operations["összetevő_substring_zaj_törölve"] += 1
    if item_id in TUTTIFRUTTI_INGREDIENT_NOISE_IDS:
        before = copy.deepcopy(props.get("összetevő"))
        remove_folded_atoms(props, "összetevő", {"tuttifrutti"})
        if before != props.get("összetevő"):
            operations["összetevő_substring_zaj_törölve"] += 1

    if item_id in LOOSE_TWININGS_IDS:
        before = copy.deepcopy(props.get("forma"))
        remove_folded_atoms(props, "forma", {"filteres"})
        append_list(props, "forma", ["szálas"])
        if before != props.get("forma"):
            operations["Twinings_szálas_forma_javítva"] += 1


def normalize_property_axes(
    products: list[dict[str, Any]],
    operations: Counter[str],
) -> None:
    for product in products:
        if product.get("fokategoria") == ITAL:
            normalize_misc_property_axes(product, operations)
            normalize_semantic_value_axes(product, operations)
    normalize_placeholder_and_text_values(products, operations)


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
    "bag in box": "bag-in-box",
    "pohar": "pohár",
}


QUANTITY_UNITS = frozenset({"g", "kg", "ml", "cl", "dl", "l"})


def canonical_quantity_unit(unit: str) -> str:
    folded = fold_text(unit)
    return "g" if folded == "gr" else folded


def format_quantity(number: float, unit: str) -> str:
    unit = canonical_quantity_unit(unit)
    if number.is_integer():
        text = str(int(number))
    else:
        text = f"{number:.6f}".rstrip("0").rstrip(".").replace(".", ",")
    return f"{text} {unit}"


def final_quantity_from_source(product: dict[str, Any]) -> str | None:
    item = product.get("termek") or {}
    amount = str(item.get("vegso_mennyiseg") or "").strip()
    unit = fold_text(item.get("vegso_egyseg") or "")
    if not amount or not unit:
        return None
    if unit not in QUANTITY_UNITS:
        return None
    if not re.fullmatch(r"\d+(?:[.,]\d+)?", amount):
        return None
    return format_quantity(float(amount.replace(",", ".")), unit)


def multipack_from_name(product: dict[str, Any]) -> tuple[int, float, str] | None:
    match = re.search(
        r"(?<!\d)(\d+)\s*[x×]\s*(\d+(?:[.,]\d+)?)\s*"
        r"(kg|ml|cl|dl|l|gr|g)\b",
        product_name(product),
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return (
        int(match.group(1)),
        float(match.group(2).replace(",", ".")),
        canonical_quantity_unit(match.group(3)),
    )


def quantity_from_name(product: dict[str, Any]) -> str | None:
    matches = list(
        re.finditer(
            r"(?<!\d)(\d+(?:[.,]\d+)?)\s*(kg|ml|cl|dl|l|gr|g)\b",
            product_name(product),
            flags=re.IGNORECASE,
        )
    )
    if not matches:
        return None
    match = matches[-1]
    return format_quantity(
        float(match.group(1).replace(",", ".")),
        canonical_quantity_unit(match.group(2)),
    )


def normalize_size_candidate(
    product: dict[str, Any],
    value: Any,
    props: dict[str, Any],
    packaging: list[str],
    path: tuple[str, str],
) -> str | None:
    text = re.sub(r"\s+", " ", str(value)).strip()
    number = r"(\d+(?:[.,]\d+)?)"
    unit = r"(kg|ml|cl|dl|l|gr|g|db)"

    plus_match = re.fullmatch(
        rf"{number}\s*{unit}\s*\+\s*{number}\s*{unit}",
        text,
        flags=re.IGNORECASE,
    )
    if plus_match:
        first_number = float(plus_match.group(1).replace(",", "."))
        first_unit = canonical_quantity_unit(plus_match.group(2))
        second_number = float(plus_match.group(3).replace(",", "."))
        second_unit = canonical_quantity_unit(plus_match.group(4))
        if first_unit != second_unit:
            raise RuntimeError(
                f"Eltérő egységű csomagösszetétel: {product_id(product)} / {text}"
            )
        props["csomagdarabszám"] = 2
        props["csomagegységek"] = [
            format_quantity(first_number, first_unit),
            format_quantity(second_number, second_unit),
        ]
        packaging.append("multipack")
        return format_quantity(first_number + second_number, first_unit)

    multipack_match = re.fullmatch(
        rf"(\d+)\s*[x×]\s*{number}\s*{unit}",
        text,
        flags=re.IGNORECASE,
    )
    if multipack_match:
        count = int(multipack_match.group(1))
        unit_amount = float(multipack_match.group(2).replace(",", "."))
        quantity_unit = canonical_quantity_unit(multipack_match.group(3))
        props["csomagdarabszám"] = count
        props["egységnyi kiszerelés"] = format_quantity(
            unit_amount,
            quantity_unit,
        )
        packaging.append("multipack")
        return format_quantity(count * unit_amount, quantity_unit)

    count_total_match = re.fullmatch(
        rf"(\d+)\s*(filter|teafilter|db)\s+{number}\s*{unit}",
        text,
        flags=re.IGNORECASE,
    )
    if count_total_match:
        props["csomagdarabszám"] = int(count_total_match.group(1))
        if "filter" in count_total_match.group(2).casefold() and path == (
            HOT_BRANCH,
            "Tea",
        ):
            append_list(props, "forma", ["filteres"])
        return format_quantity(
            float(count_total_match.group(3).replace(",", ".")),
            canonical_quantity_unit(count_total_match.group(4)),
        )

    count_only_match = re.fullmatch(
        r"(\d+)\s*(filter|teafilter)",
        text,
        flags=re.IGNORECASE,
    )
    if count_only_match:
        props["csomagdarabszám"] = int(count_only_match.group(1))
        if path == (HOT_BRANCH, "Tea"):
            append_list(props, "forma", ["filteres"])
        return None

    packaged_quantity_match = re.fullmatch(
        rf"{number}\s*{unit}\s*(uveg|üveg|doboz)",
        text,
        flags=re.IGNORECASE,
    )
    if packaged_quantity_match:
        package_folded = fold_text(packaged_quantity_match.group(3))
        if package_folded == "uveg":
            packaging.append("palack")
            append_list(props, "csomagolás anyaga", ["üveg"])
        else:
            packaging.append("doboz")
        return format_quantity(
            float(packaged_quantity_match.group(1).replace(",", ".")),
            canonical_quantity_unit(packaged_quantity_match.group(2)),
        )

    simple_match = re.fullmatch(
        rf"{number}\s*{unit}",
        text,
        flags=re.IGNORECASE,
    )
    if simple_match:
        return format_quantity(
            float(simple_match.group(1).replace(",", ".")),
            canonical_quantity_unit(simple_match.group(2)),
        )
    return text


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
            if folded == "uveg":
                packaging.append("palack")
                append_list(props, "csomagolás anyaga", ["üveg"])
                return
            if folded == "pet palack":
                packaging.append("palack")
                append_list(props, "csomagolás anyaga", ["PET"])
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
            selected_size = normalize_size_candidate(
                product,
                selected_size,
                props,
                packaging,
                path,
            )
        multipack = multipack_from_name(product)
        if multipack:
            count, unit_amount, unit = multipack
            source_total = final_quantity_from_source(product)
            computed_total = format_quantity(count * unit_amount, unit)
            selected_size = source_total or computed_total
            props["csomagdarabszám"] = count
            props["egységnyi kiszerelés"] = format_quantity(unit_amount, unit)
            packaging.append("multipack")
        elif "multipack" in name_folded:
            packaging.append("multipack")
        if selected_size is None:
            selected_size = final_quantity_from_source(product) or quantity_from_name(product)
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


def transaction_partial_backups() -> tuple[Path, Path]:
    _result_stage, _category_stage, result_backup, category_backup = (
        transaction_artifacts()
    )
    return (
        result_backup.with_name(result_backup.name + ".partial"),
        category_backup.with_name(category_backup.name + ".partial"),
    )


def all_transaction_artifacts() -> tuple[Path, ...]:
    return (*transaction_artifacts(), *transaction_partial_backups())


def atomic_backup_copy(source: Path, backup: Path, partial: Path) -> None:
    if backup.exists() or partial.exists():
        raise RuntimeError(f"Nem tiszta backup-cél: {backup} / {partial}")
    shutil.copy2(source, partial)
    load_json(partial)
    partial.replace(backup)


def recover_interrupted_transaction() -> bool:
    """Egy korábban félbeszakadt kétfájlos csere biztonságos helyreállítása."""

    result_stage, category_stage, result_backup, category_backup = transaction_artifacts()
    result_partial, category_partial = transaction_partial_backups()
    stages = (result_stage, category_stage)
    backups = (result_backup, category_backup)
    existing_backups = [path for path in backups if path.exists()]

    if existing_backups:
        if len(existing_backups) == 2:
            # Ha mindkét főfájl már célállapotban van, a commit lezajlott,
            # csak a takarítás szakadt félbe. Vegyes/hibás párnál visszaállunk.
            try:
                run_checker(RESULT_PATH, CATEGORY_PATH)
            except Exception:
                shutil.copy2(result_backup, RESULT_PATH)
                shutil.copy2(category_backup, CATEGORY_PATH)
        elif result_backup.exists():
            # A backup-sorrend miatt itt a commit még nem kezdődhetett el:
            # az eredményfájl biztos másolatát visszatesszük, a kategóriafájl
            # főpéldánya pedig még érintetlen.
            shutil.copy2(result_backup, RESULT_PATH)
        else:
            # Csak kategóriabackup kizárólag a sikeres commit utáni,
            # sorrendi takarítás közben maradhat vissza.
            run_checker(RESULT_PATH, CATEGORY_PATH)
        for path in all_transaction_artifacts():
            if path.exists():
                path.unlink()
        return True

    recovered = False
    for path in (*stages, result_partial, category_partial):
        if path.exists():
            path.unlink()
            recovered = True
    return recovered


def write_transactionally(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
) -> dict[str, Any]:
    result_stage, category_stage, result_backup, category_backup = transaction_artifacts()
    result_partial, category_partial = transaction_partial_backups()
    auxiliaries = all_transaction_artifacts()
    leftovers = [str(path) for path in auxiliaries if path.exists()]
    if leftovers:
        raise RuntimeError(f"Korábbi staging/backup fájl maradt vissza: {leftovers}")
    try:
        dump_json(result_stage, products)
        dump_json(category_stage, categories)
        stage_check = run_checker(result_stage, category_stage)
        atomic_backup_copy(RESULT_PATH, result_backup, result_partial)
        atomic_backup_copy(CATEGORY_PATH, category_backup, category_partial)
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
        for path in (result_stage, category_stage, result_partial, category_partial):
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
    parser.add_argument(
        "--assert-idempotent",
        action="store_true",
        help="Célfán a legkisebb eltérést is hibának tekinti",
    )
    args = parser.parse_args()

    if not CHECKER_PATH.is_file():
        raise RuntimeError(f"Hiányzó ellenőrző: {CHECKER_PATH}")
    if args.apply:
        recover_interrupted_transaction()
    else:
        leftovers = [str(path) for path in all_transaction_artifacts() if path.exists()]
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
    normalize_property_axes(products, operations)
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
    def allowed_external_product_change(
        original: dict[str, Any],
        current: dict[str, Any],
    ) -> bool:
        item_id = product_id(original)
        allowed_property_names = {
            CITRIORANGE_ID: frozenset({"terméktípus"}),
            FRUIT_STEP_GINGER_ID: frozenset(
                {"gyümölcs", "kiszerelés", "terméktípus", "összetevő"}
            ),
        }.get(item_id)
        if allowed_property_names is None:
            return False
        original_path = (
            original.get("fokategoria"),
            original.get("alkategoria"),
            original.get("altipus"),
        )
        current_path = (
            current.get("fokategoria"),
            current.get("alkategoria"),
            current.get("altipus"),
        )
        if original_path != CITRUS_TARGET or current_path != CITRUS_TARGET:
            return False
        expected = copy.deepcopy(original)
        expected_props = expected.setdefault("tulajdonsagok", {})
        current_props = current.get("tulajdonsagok") or {}
        for property_name in allowed_property_names:
            if property_name in current_props:
                expected_props[property_name] = copy.deepcopy(
                    current_props[property_name]
                )
            else:
                expected_props.pop(property_name, None)
        expected["kategoria_hash"] = current.get("kategoria_hash")
        return expected == current

    unexpected_non_ital_changes = []
    for index, original in enumerate(original_products):
        if original.get("fokategoria") == ITAL or products[index] == original:
            continue
        if allowed_external_product_change(original, products[index]):
            continue
        unexpected_non_ital_changes.append(index)
    if unexpected_non_ital_changes:
        raise RuntimeError(f"Nem-Ital termék módosult: {unexpected_non_ital_changes[:20]}")

    # A kategóriafában csak az Ital és a két explicit külső célág változhat.
    original_without_scope = copy.deepcopy(original_categories)
    current_without_scope = copy.deepcopy(categories)
    original_without_scope.pop(ITAL, None)
    current_without_scope.pop(ITAL, None)

    def remove_declared_properties(
        node: dict[str, Any],
        property_names: frozenset[str],
    ) -> None:
        prop_block = node.get(PROP_KEY) or {}
        for group_name in ("egyedi", "csoportos"):
            group = prop_block.get(group_name) or {}
            for property_name in property_names:
                group.pop(property_name, None)

    for snapshot in (original_without_scope, current_without_scope):
        root = snapshot[CITRUS_TARGET[0]]
        citrus_parent = root[ALK_KEY][CITRUS_TARGET[1]]
        remove_declared_properties(citrus_parent, frozenset({"márka"}))
        citrus_parent[ALT_KEY].pop(CITRUS_OLD_TARGET[2], None)
        citrus_parent[ALT_KEY].pop(CITRUS_TARGET[2], None)
        nesquik_parent = root[ALK_KEY][NESQUIK_TARGET[1]]
        remove_declared_properties(
            nesquik_parent,
            frozenset({"márka", "íz"}),
        )
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

    if args.assert_idempotent:
        if mode != "target-idempotency-check":
            raise RuntimeError(
                "--assert-idempotent csak a teljes célfán használható"
            )
        if changed_indices or categories != original_categories:
            raise RuntimeError(
                "Az átalakítás nem idempotens: "
                f"termékek={len(changed_indices)}, "
                f"kategóriafa_változott={categories != original_categories}"
            )

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
