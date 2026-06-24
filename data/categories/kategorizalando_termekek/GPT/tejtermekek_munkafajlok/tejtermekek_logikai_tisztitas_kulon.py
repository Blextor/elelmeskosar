from __future__ import annotations

import copy
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


WORK_DIR = Path(__file__).resolve().parent

DATE_STAMP = "2026-06-24"
SOURCE_CATEGORY = WORK_DIR / f"tejtermekek_javitott_kategoria_{DATE_STAMP}.json"
SOURCE_PRODUCTS = WORK_DIR / f"tejtermekek_javitott_termekek_{DATE_STAMP}.json"

OUT_CATEGORY = WORK_DIR / f"tejtermekek_logikai_tisztitott_kategoria_{DATE_STAMP}.json"
OUT_PRODUCTS = WORK_DIR / f"tejtermekek_logikai_tisztitott_termekek_{DATE_STAMP}.json"
OUT_AUDIT_JSON = WORK_DIR / f"tejtermekek_logikai_tisztitott_audit_{DATE_STAMP}.json"
OUT_AUDIT_MD = WORK_DIR / f"tejtermekek_logikai_tisztitott_audit_{DATE_STAMP}.md"

FORBIDDEN_OUTPUT_NAMES = {
    "eredmeny.json",
    "kategoriak_2026-06-13.json",
}

ROOT_NAME = "Tejtermékek és tojás"
RENAMED_IVOKAT = "Ivójoghurt, kefir, író és aludttej"
RENAMED_EGYEB_TOJAS = "Egyéb tojás és tojáskészítmény"
RENAMED_KENHETO_OMLESZTETT = "Kenhető ömlesztett sajt"

BOOL_PROPS = {
    "bio",
    "bevonatos",
    "cukormentes / hozzáadott cukor nélkül",
    "cukrozott",
    "élőflórás/probiotikus",
    "érlelt",
    "extra sárga",
    "GMO-mentes",
    "gluténmentes",
    "hazai",
    "ízesített",
    "készítmény (növényi zsiradékkal)",
    "laktózmentes",
    "light / csökkentett zsír",
    "omega-3",
    "protein / magas fehérje",
    "sózott",
    "szalmonella ellen kezelt",
    "sütőmargarin",
    "vegán",
}

SCALAR_PROPS = {
    "kiszerelés",
    "márka",
    "méret",
    "tartás",
    "zsírtartalom",
}

EGYEDI_PROPS = BOOL_PROPS | SCALAR_PROPS

RARE_PRUNE_PROTECTED_PROPS = BOOL_PROPS | {
    "állat",
    "fajta",
    "forma",
    "kiszerelés",
    "márka",
    "méret",
    "tartás",
    "zsírtartalom",
}

ALWAYS_REMOVE_PROPS = {
    "alapanyag",
    "bevonat tipusa",
    "celcsoport",
    "edesitoszerrel",
    "hozzaadott anyag",
    "hozzaadott vitamin / asvanyi anyag",
    "jellemzo",
    "jellemzok",
    "kiegeszito",
    "novenyi alap",
    "novenyi_alap",
    "novenyi alapu",
    "termekcsalad",
    "termektipus",
    "toltott",
    "uht",
    "valtozat",
    "zsirtartalom_jelleg",
}

KEEP_FORMA_ALKS = {
    "sajt",
    "turo",
    "vaj",
    "novenyi alternativa",
}

KEEP_FAJTA_ALKS = {
    "sajt",
    "tojas",
}

KEEP_ALAP_ALKS = {
    "novenyi alternativa",
}

KEEP_ALLAT_ALKS = {
    "sajt",
    "tej",
    "turo",
}

KEEP_HOKEZELES_ALKS = {
    "novenyi alternativa",
    "tej",
    "tejdesszert, puding",
    "tejital, jegeskave",
    "tejszin",
    "tojas",
}

KEEP_FELHASZNALAS_ALKS = {
    "margarin",
    "novenyi alternativa",
    "tejszin",
}

DROP_PROPS_BY_ALK = {
    "novenyi alternativa": {
        "erlelt",
        "keszitmeny (novenyi zsiradekkal)",
    },
    "sajtkrem, szendvicskrem": {
        "erlelt",
    },
    "tojas": {
        "iz",
    },
    "vaj": {
        "izesitett",
        "keszitmeny (novenyi zsiradekkal)",
        "protein / magas feherje",
    },
}

BOOLS_BY_ALK = {
    "tej": {
        "bio",
        "GMO-mentes",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
    },
    "tejital, jegeskave": {
        "cukormentes / hozzáadott cukor nélkül",
        "ízesített",
        "laktózmentes",
        "protein / magas fehérje",
    },
    "joghurt": {
        "bio",
        "cukormentes / hozzáadott cukor nélkül",
        "élőflórás/probiotikus",
        "ízesített",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
    },
    "ivojoghurt, kefir, iro es aludttej": {
        "bio",
        "cukormentes / hozzáadott cukor nélkül",
        "élőflórás/probiotikus",
        "ízesített",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
    },
    "turo": {
        "bio",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
    },
    "kremturo, turodesszert": {
        "bevonatos",
        "bio",
        "cukormentes / hozzáadott cukor nélkül",
        "gluténmentes",
        "ízesített",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
    },
    "tejfol": {
        "bio",
        "élőflórás/probiotikus",
        "készítmény (növényi zsiradékkal)",
        "laktózmentes",
        "light / csökkentett zsír",
    },
    "tejszin": {
        "bio",
        "cukormentes / hozzáadott cukor nélkül",
        "cukrozott",
        "készítmény (növényi zsiradékkal)",
        "laktózmentes",
        "light / csökkentett zsír",
    },
    "vaj": {
        "bio",
        "laktózmentes",
        "light / csökkentett zsír",
        "sózott",
    },
    "margarin": {
        "bio",
        "laktózmentes",
        "light / csökkentett zsír",
        "sózott",
        "sütőmargarin",
    },
    "sajt": {
        "bio",
        "érlelt",
        "készítmény (növényi zsiradékkal)",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
    },
    "sajtkrem, szendvicskrem": {
        "bio",
        "ízesített",
        "készítmény (növényi zsiradékkal)",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
    },
    "tejdesszert, puding": {
        "bio",
        "cukormentes / hozzáadott cukor nélkül",
        "gluténmentes",
        "ízesített",
        "laktózmentes",
        "protein / magas fehérje",
    },
    "novenyi alternativa": {
        "bio",
        "cukormentes / hozzáadott cukor nélkül",
        "cukrozott",
        "gluténmentes",
        "ízesített",
        "laktózmentes",
        "light / csökkentett zsír",
        "protein / magas fehérje",
        "vegán",
    },
    "tojas": {
        "bio",
        "extra sárga",
        "GMO-mentes",
        "hazai",
        "omega-3",
        "szalmonella ellen kezelt",
    },
}

CHEESE_KIND_PATTERNS = [
    ("trappista", ["trappista"]),
    ("mozzarella", ["mozzarella"]),
    ("gouda", ["gouda"]),
    ("edami", ["edam", "edami", "edámi"]),
    ("ementáli", ["emental", "emmental", "ementáli", "emmentaler"]),
    ("maasdam", ["maasdam", "maasdamer"]),
    ("cheddar", ["cheddar"]),
    ("camembert", ["camembert"]),
    ("brie", ["brie"]),
    ("kék sajt", ["kekpeneszes", "kek sajt", "blue cheese", "gorgonzola", "roquefort"]),
    ("feta", ["feta"]),
    ("krémfehér sajt", ["kremfeher"]),
    ("mascarpone", ["mascarpone"]),
    ("ricotta", ["ricotta"]),
    ("burrata", ["burrata"]),
    ("parmezán", ["parmezan", "parmesan", "parmigiano"]),
    ("grana padano", ["grana padano"]),
    ("pecorino", ["pecorino"]),
    ("parenyica", ["parenyica"]),
    ("halloumi", ["halloumi"]),
    ("raclette", ["raclette"]),
    ("scamorza", ["scamorza"]),
    ("sajtkeverék", ["sajtkeverek", "sajtok kevereke"]),
]

FLAVOR_PATTERNS = [
    ("natúr", ["natur", "natúr", "original"]),
    ("füstölt", ["fustolt", "füstölt"]),
    ("vanília", ["vanilia", "vaníli"]),
    ("csokoládé", ["csokolade", "csokoládé", "choco"]),
    ("kakaós", ["kakao", "kakaó"]),
    ("eper", ["eper", "epres"]),
    ("málna", ["malna", "málna"]),
    ("meggy", ["meggy"]),
    ("áfonya", ["afonya", "áfonya"]),
    ("őszibarack", ["oszibarack", "őszibarack", "barackos"]),
    ("sárgabarack", ["sargabarack", "sárgabarack"]),
    ("banán", ["banan", "banán"]),
    ("kókusz", ["kokusz", "kókusz"]),
    ("mangó", ["mango", "mangó"]),
    ("kávé", ["kave", "kávé", "espresso", "latte", "cappuccino"]),
    ("karamell", ["karamell"]),
    ("pisztácia", ["pisztacia", "pisztácia"]),
    ("mogyoró", ["mogyoro", "mogyoró"]),
    ("zöldfűszeres", ["zoldfuszer", "zöldfűszer"]),
    ("fokhagymás", ["fokhagyma", "fokhagymás"]),
    ("snidlinges", ["snidling", "metelohagyma", "metélőhagyma"]),
    ("sonkás", ["sonka", "sonkás"]),
    ("paprikás", ["paprika", "paprikás"]),
    ("magyaros", ["magyaros"]),
    ("sós", ["sos", "sós", "sózott", "sozott"]),
    ("cheddar", ["cheddar"]),
]

CHEESE_FORM_PATTERNS = [
    ("reszelt", ["reszelt"]),
    ("szeletelt", ["szeletelt", "szelet"]),
    ("darabolt", ["darabolt", "darab"]),
    ("tömb", ["tomb", "tömb"]),
    ("korong", ["korong"]),
    ("lapka", ["lapka", "toast"]),
    ("mini", ["mini"]),
    ("rúd", ["rud", "rúd", "rudacska"]),
    ("falat", ["falat"]),
    ("golyó", ["golyo", "golyó"]),
    ("kocka", ["kocka"]),
    ("kenhető", ["kenheto", "kenhető"]),
]


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


def dedupe_values(values: list[Any], prop_name: str) -> list[Any]:
    seen: set[str] = set()
    out: list[Any] = []
    for raw in values:
        value = normalize_value(raw, prop_name)
        if value is None or value == "":
            continue
        key = fold_text(value)
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def normalize_value(value: Any, prop_name: str) -> Any:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip()
    if not text:
        return None

    folded = fold_text(text)
    canonical_by_fold = {
        "natur": "natúr",
        "natural": "natúr",
        "original": "natúr",
        "edam": "edami",
        "edami": "edami",
        "edami": "edami",
        "emental": "ementáli",
        "emmental": "ementáli",
        "emmentaler": "ementáli",
        "maasdamer": "maasdam",
        "gouda": "gouda",
        "kekpeneszes": "kék sajt",
        "kek sajt": "kék sajt",
        "kecsketejes": "kecske",
        "juhtejes": "juh",
        "tehentej": "tehén",
        "uht": "UHT",
        "esl": "ESL",
        "pasztorozott": "pasztőrözött",
        "sozott": "sózott",
        "sos": "sós",
    }
    if folded in canonical_by_fold:
        return canonical_by_fold[folded]

    if prop_name in {"fajta", "íz", "ízesítés", "forma", "állat", "édesítés", "hőkezelés"}:
        return text[:1].lower() + text[1:]
    return text


def add_values(props: dict[str, Any], prop_name: str, new_values: list[Any], audit: Counter[str]) -> None:
    values = values_of(props.get(prop_name)) + new_values
    values = dedupe_values(values, prop_name)
    if not values:
        return
    if prop_name in SCALAR_PROPS and len(values) == 1:
        new_value: Any = values[0]
    else:
        new_value = values
    if props.get(prop_name) != new_value:
        props[prop_name] = new_value
        audit[prop_name] += 1


def set_bool(props: dict[str, Any], prop_name: str, value: bool, audit: Counter[str]) -> None:
    old = props.get(prop_name)
    if isinstance(old, str):
        folded = fold_text(old)
        if folded in {"true", "igen", "yes", "laktózmentes", "laktozmentes", "bio", "vegán", "vegan"}:
            old = True
        elif folded in {"false", "nem", "no"}:
            old = False
    if old is not value:
        props[prop_name] = value
        audit[prop_name] += 1


def remove_prop(props: dict[str, Any], prop_name: str, audit: Counter[str]) -> None:
    if prop_name in props:
        props.pop(prop_name, None)
        audit[prop_name] += 1


def product_text(product: dict[str, Any]) -> str:
    termek = product.get("termek") or {}
    parts = [
        termek.get("product_name", ""),
        termek.get("brand_name", ""),
        termek.get("categories", ""),
        product.get("alkategoria", ""),
        product.get("altipus", ""),
    ]
    return " ".join(str(part) for part in parts if part)


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(fold_text(pattern) in text for pattern in patterns)


def kategoriak_hash(fok: str, alk: str, alt: str, props: dict[str, Any]) -> str:
    key = f"{fok}|{alk}|{alt}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def classify_milk_alt(text_folded: str, old_alt: str) -> str:
    old_folded = fold_text(old_alt)
    if "tejpor" in text_folded:
        return "Tejpor"
    if "suritett" in text_folded:
        return "Sűrített tej"
    if "kavefeherito" in text_folded or "completa" in text_folded:
        return "Kávéfehérítő, tejkészítmény"
    if "esl" in text_folded:
        return "ESL tej"
    if "uht" in text_folded or "tartos" in text_folded or "ultramagas" in text_folded:
        return "UHT tartós tej"
    if old_folded in {"tej", "kecsketej", "laktozmentes tej"}:
        return "Friss tej"
    return old_alt


def classify_spread_alt(text_folded: str, old_alt: str) -> tuple[str, str]:
    old_folded = fold_text(old_alt)
    if "vajkrem" in old_folded or "vajkrem" in text_folded:
        return "Vaj", "Vajkrém"
    if "omlesztett" in old_folded or "omlesztett" in text_folded:
        return "Sajtkrém, szendvicskrém", RENAMED_KENHETO_OMLESZTETT
    if "szendvicskrem" in old_folded or "szendvicskrem" in text_folded:
        return "Sajtkrém, szendvicskrém", "Szendvicskrém"
    return "Sajtkrém, szendvicskrém", "Sajtkrém"


def add_cheese_kind_from_alt(props: dict[str, Any], old_alt: str, text_folded: str, audit: Counter[str]) -> None:
    old_folded = fold_text(old_alt)
    alt_kind = {
        "mozzarella": "mozzarella",
        "trappista sajt": "trappista",
        "cheddar": "cheddar",
        "parenyica": "parenyica",
        "mascarpone": "mascarpone",
        "ricotta": "ricotta",
        "burrata": "burrata",
        "raclette": "raclette",
        "scamorza": "scamorza",
    }.get(old_folded)
    if alt_kind:
        add_values(props, "fajta", [alt_kind], audit)
    if old_folded == "feta / kremfeher sajt":
        add_values(props, "fajta", ["feta" if "feta" in text_folded else "krémfehér sajt"], audit)
    if old_folded == "camembert / brie":
        add_values(props, "fajta", ["brie" if "brie" in text_folded else "camembert"], audit)
    if old_folded == "kek sajt":
        add_values(props, "fajta", ["kék sajt"], audit)


def classify_cheese_alt(product: dict[str, Any], props: dict[str, Any], text_folded: str) -> tuple[str, str]:
    old_alt = product.get("altipus", "")
    old_folded = fold_text(old_alt)

    if old_folded == "kremsajt / kenheto sajt":
        return classify_spread_alt(text_folded, old_alt)

    if old_folded in {"lapka sajt"} or "lapka" in text_folded or "omlesztett" in text_folded:
        return "Sajt", "Ömlesztett sajt"
    if old_folded in {"grillsajt / halloumi / sutnivalo"}:
        return "Sajt", old_alt
    if old_folded in {"camembert / brie", "kek sajt"}:
        return "Sajt", "Penészes sajt"
    if old_folded in {"mozzarella", "burrata", "feta / kremfeher sajt", "mascarpone", "ricotta"}:
        return "Sajt", "Friss / lágy sajt"

    if old_folded in {
        "cheddar",
        "darabolt sajt",
        "juhsajt",
        "kecskesajt",
        "marinalt sajt",
        "parenyica",
        "raclette",
        "reszelt sajt",
        "sajtsnack",
        "sajtspecialitas",
        "scamorza",
        "szeletelt sajt",
        "trappista sajt",
    }:
        if contains_any(text_folded, ["félkemény", "felkemeny"]):
            return "Sajt", "Félkemény sajt"
        if contains_any(text_folded, ["camembert", "brie", "kékpenészes", "kekpeneszes", "gorgonzola", "roquefort"]):
            return "Sajt", "Penészes sajt"
        if contains_any(text_folded, ["mozzarella", "burrata", "feta", "krémfehér", "kremfeher", "mascarpone", "ricotta", "friss", "lágy", "lagy"]):
            return "Sajt", "Friss / lágy sajt"
        if contains_any(text_folded, ["grill", "halloumi", "sütnivaló", "sutnivalo"]):
            return "Sajt", "Grillsajt / halloumi / sütnivaló"
        if contains_any(text_folded, ["parmezán", "parmezan", "parmigiano", "grana padano", "pecorino", "extra kemény", "extra kemeny", "kemény", "kemeny"]):
            return "Sajt", "Kemény sajt"
        return "Sajt", "Félkemény sajt"

    return "Sajt", old_alt


def infer_alt_and_path(product: dict[str, Any], props: dict[str, Any], audit: dict[str, Any]) -> tuple[str, str]:
    alk = product.get("alkategoria", "")
    alt = product.get("altipus", "")
    old_path = (alk, alt)
    text = product_text(product)
    text_folded = fold_text(text)
    alk_folded = fold_text(alk)
    alt_folded = fold_text(alt)

    if alk_folded == "ivojoghurt, kefir, iro, aludttej":
        alk = RENAMED_IVOKAT

    if alk_folded == "tej":
        new_alt = classify_milk_alt(text_folded, alt)
        if new_alt != alt:
            alt = new_alt

    elif alk_folded == "tejital, jegeskave" and alt_folded == "tejalapu ital":
        alt = "Egyéb ízesített tejital"

    elif alk_folded == "turo" and alt_folded in {"cottage cheese", "rogos turo"}:
        add_values(props, "forma", ["szemcsés" if alt_folded == "cottage cheese" else "rögös"], audit["props_added"])
        alt = "Tehéntúró"

    elif alk_folded == "tejfol" and alt_folded in {"laktozmentes tejfol", "izesitett tejfol"}:
        alt = "Tejföl"

    elif alk_folded == "tejszin" and alt_folded == "hab- es fozotejszin":
        alt = "Habtejszín" if "hab" in text_folded else "Főzőtejszín"

    elif alk_folded == "vaj":
        if alt_folded == "vaj":
            alt = "Teavaj, márkázott vaj"
        elif alt_folded == "fuszervaj":
            alt = "Vajkrém" if contains_any(text_folded, ["krém", "krem", "kenhető", "kenheto"]) else "Teavaj, márkázott vaj"

    elif alk_folded == "sajt":
        add_cheese_kind_from_alt(props, alt, text_folded, audit["props_added"])
        new_alk, new_alt = classify_cheese_alt(product, props, text_folded)
        alk, alt = new_alk, new_alt

    elif alk_folded == "sajtkrem, szendvicskrem":
        new_alk, new_alt = classify_spread_alt(text_folded, alt)
        alk, alt = new_alk, new_alt

    elif alk_folded == "tejdesszert, puding" and alt_folded in {"desszertalap", "pohardesszert, kremdesszert"}:
        alt = "Egyéb tejdesszert"

    elif alk_folded == "novenyi alternativa":
        if alt_folded == "novenyi fozokrem":
            alt = "Növényi főzőkrém / tejszín"
        elif alt_folded == "novenyi joghurt / fermentalt keszitmeny":
            alt = "Növényi joghurt"

    elif alk_folded == "tojas":
        if alt_folded in {"furjtojas", "egyeb tojas (furj, stb.)"}:
            alt = RENAMED_EGYEB_TOJAS
        elif alt_folded == "fott / fustolt tojas":
            alt = RENAMED_EGYEB_TOJAS

    if old_path != (alk, alt):
        audit["moves"].append(
            {
                "index": product.get("_forras_index"),
                "termek": (product.get("termek") or {}).get("product_name", ""),
                "from": f"{old_path[0]} / {old_path[1]}",
                "to": f"{alk} / {alt}",
            }
        )
        audit["move_reasons"][f"{old_path[0]} / {old_path[1]} -> {alk} / {alt}"] += 1

    return alk, alt


def infer_common_values(product: dict[str, Any], props: dict[str, Any], audit: dict[str, Any]) -> None:
    text = product_text(product)
    folded = fold_text(text)
    alk_folded = fold_text(product.get("alkategoria", ""))

    if not props.get("márka"):
        brand = (product.get("termek") or {}).get("brand_name") or ""
        if brand.strip():
            props["márka"] = brand.strip()
            audit["props_added"]["márka"] += 1
        else:
            props["márka"] = "márka nélkül"
            audit["props_added"]["márka"] += 1

    for prop_name, patterns in [
        ("hőkezelés", ["UHT", "ESL", "pasztőrözött"]),
        ("állat", ["kecske", "juh", "bivaly"]),
    ]:
        values: list[str] = []
        for pattern in patterns:
            if fold_text(pattern) in folded:
                values.append(pattern)
        if prop_name == "állat" and values:
            if "kecske" in values:
                add_values(props, prop_name, ["kecske"], audit["props_added"])
            if "juh" in values:
                add_values(props, prop_name, ["juh"], audit["props_added"])
            if "bivaly" in values:
                add_values(props, prop_name, ["bivaly"], audit["props_added"])
        elif prop_name == "hőkezelés" and values:
            add_values(props, prop_name, values, audit["props_added"])

    if "allat" not in {fold_text(k) for k in props} and alk_folded in {"tej", "turo"}:
        if not contains_any(folded, ["kecske", "juh", "bivaly"]):
            add_values(props, "állat", ["tehén"], audit["props_added"])

    if not props.get("zsírtartalom"):
        percent_match = re.search(r"(?<!\d)(\d{1,2}(?:[,.]\d)?)\s*%", text)
        if percent_match:
            percent = percent_match.group(1).replace(".", ",") + "%"
            add_values(props, "zsírtartalom", [percent], audit["props_added"])
        elif "zsirszegeny" in folded:
            add_values(props, "zsírtartalom", ["zsírszegény"], audit["props_added"])
        elif "sovany" in folded:
            add_values(props, "zsírtartalom", ["sovány"], audit["props_added"])
        elif "felzsiros" in folded:
            add_values(props, "zsírtartalom", ["félzsíros"], audit["props_added"])
        elif "zsirdus" in folded:
            add_values(props, "zsírtartalom", ["zsírdús"], audit["props_added"])
        elif "zsiros" in folded:
            add_values(props, "zsírtartalom", ["zsíros"], audit["props_added"])

    if not props.get("íz"):
        inferred_flavors = [flavor for flavor, patterns in FLAVOR_PATTERNS if contains_any(folded, patterns)]
        if inferred_flavors:
            add_values(props, "íz", inferred_flavors, audit["props_added"])

    if alk_folded == "sajt":
        kinds = [kind for kind, patterns in CHEESE_KIND_PATTERNS if contains_any(folded, patterns)]
        if kinds:
            add_values(props, "fajta", kinds, audit["props_added"])
        forms = [form for form, patterns in CHEESE_FORM_PATTERNS if contains_any(folded, patterns)]
        if forms:
            add_values(props, "forma", forms, audit["props_added"])

    if alk_folded == "turo":
        forms: list[str] = []
        if contains_any(folded, ["cottage", "szemcsés", "szemcses"]):
            forms.append("szemcsés")
        if contains_any(folded, ["rögös", "rogos"]):
            forms.append("rögös")
        if contains_any(folded, ["krémes", "kremes"]):
            forms.append("krémes")
        if forms:
            add_values(props, "forma", forms, audit["props_added"])

    if alk_folded == "tojas":
        if contains_any(folded, ["fürj", "furj"]):
            add_values(props, "fajta", ["fürjtojás"], audit["props_added"])
        elif contains_any(folded, ["tojásfehérje", "tojasfeherje"]):
            add_values(props, "fajta", ["tojásfehérje"], audit["props_added"])
        elif contains_any(folded, ["tojássárgája", "tojassargaja"]):
            add_values(props, "fajta", ["tojássárgája"], audit["props_added"])
        elif contains_any(folded, ["tojáslé", "tojasle", "teljes tojás", "teljes tojas"]):
            add_values(props, "fajta", ["teljes tojáslé"], audit["props_added"])
        else:
            add_values(props, "fajta", ["tyúktojás"], audit["props_added"])

        size_match = re.search(r"\b(L-XL|M-L|XL|L|M|S)\b", text.upper())
        if size_match and not props.get("méret"):
            props["méret"] = size_match.group(1)
            audit["props_added"]["méret"] += 1
        if "melyalmos" in folded:
            props["tartás"] = "mélyalmos"
            audit["props_added"]["tartás"] += 1
        elif "szabadtart" in folded or "szabad tart" in folded:
            props["tartás"] = "szabadtartású"
            audit["props_added"]["tartás"] += 1
        elif "ketreces" in folded:
            props["tartás"] = "ketreces"
            audit["props_added"]["tartás"] += 1


def infer_booleans(product: dict[str, Any], props: dict[str, Any], audit: dict[str, Any]) -> None:
    text_folded = fold_text(product_text(product))
    alk_folded = fold_text(product.get("alkategoria", ""))
    wanted = BOOLS_BY_ALK.get(alk_folded, set())

    true_patterns = {
        "bio": ["bio ", " bio", "organic", "natur*pur"],
        "bevonatos": ["bevonat", "csokoladebevon", "kakaos bevon"],
        "cukormentes / hozzáadott cukor nélkül": ["cukormentes", "hozzaadott cukor nelkul", "zero"],
        "cukrozott": ["cukrozott", "edesitett"],
        "élőflórás/probiotikus": ["elofloras", "probiotikus", "kulturaval", "kulturas"],
        "érlelt": ["erlelt"],
        "extra sárga": ["extra sarga"],
        "GMO-mentes": ["gmo-mentes", "gmo mentes"],
        "gluténmentes": ["glutenmentes", "gluten free"],
        "hazai": ["hazai", "magyar"],
        "készítmény (növényi zsiradékkal)": ["novenyi zsiradek", "novenyi olaj"],
        "laktózmentes": ["laktozmentes", "lactose free", "free from"],
        "light / csökkentett zsír": ["light", "csokkentett zsirtartalm", "felzsiros vaj"],
        "omega-3": ["omega-3", "omega 3"],
        "protein / magas fehérje": ["protein", "magas feherje"],
        "sózott": ["sozott", "sos", "enyhen sozott"],
        "szalmonella ellen kezelt": ["szalmonella ellen kezelt"],
        "sütőmargarin": ["sutomargarin", "sutőmargarin", "sütőmargarin", "suteshez"],
        "vegán": ["vegan", "vegán", "plant", "novenyi"],
    }

    for prop_name in sorted(wanted, key=fold_text):
        prop_folded = fold_text(prop_name)
        existing_keys = {fold_text(k): k for k in props}
        existing_key = existing_keys.get(prop_folded, prop_name)
        current_value = props.get(existing_key)

        if prop_name == "ízesített":
            flavor_values = [fold_text(v) for v in values_of(props.get("íz"))]
            is_true = any(v not in {"natur", "natúr", "original"} for v in flavor_values)
            is_true = is_true or contains_any(text_folded, ["ízű", "izu", "ízesítésű", "izesitesu", "gyümölcsös", "gyumolcsos"])
        elif prop_name == "cukrozott" and contains_any(text_folded, ["cukormentes", "hozzaadott cukor nelkul"]):
            is_true = False
        elif prop_name == "sózott" and contains_any(text_folded, ["sózatlan", "sozatlan"]):
            is_true = False
        elif prop_name == "vegán" and alk_folded == "novenyi alternativa":
            is_true = not contains_any(text_folded, ["állati és növényi", "allati es novenyi"])
        else:
            is_true = contains_any(text_folded, true_patterns.get(prop_name, []))

        if isinstance(current_value, bool) and current_value is True:
            is_true = True
        set_bool(props, prop_name, is_true, audit["bool_filled"])


def normalize_props(product: dict[str, Any], props: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in props.items():
        folded = fold_text(key)
        canonical_key = {
            "marka": "márka",
            "kiszereles": "kiszerelés",
            "meret": "méret",
            "tartas": "tartás",
            "zsirtartalom": "zsírtartalom",
            "izesites": "ízesítés",
            "iz": "íz",
            "edesites": "édesítés",
            "elo floras/probiotikus": "élőflórás/probiotikus",
            "elofloras/probiotikus": "élőflórás/probiotikus",
            "erlelt": "érlelt",
        }.get(folded, key)
        normalized[canonical_key] = value

    if "ízesítés" in normalized:
        add_values(normalized, "íz", values_of(normalized["ízesítés"]), audit["props_merged"])
        remove_prop(normalized, "ízesítés", audit["props_removed"])

    if "bevonat típusa" in normalized:
        if "bevonat" not in normalized:
            add_values(normalized, "bevonat", values_of(normalized["bevonat típusa"]), audit["props_merged"])
        remove_prop(normalized, "bevonat típusa", audit["props_removed"])

    if normalized.get("UHT") is True:
        add_values(normalized, "hőkezelés", ["UHT"], audit["props_merged"])
    remove_prop(normalized, "UHT", audit["props_removed"])

    infer_common_values(product, normalized, audit)

    alk_folded = fold_text(product.get("alkategoria", ""))
    for key in list(normalized):
        folded = fold_text(key)
        if folded in ALWAYS_REMOVE_PROPS:
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded == "jelleg":
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded == "forma" and alk_folded not in KEEP_FORMA_ALKS:
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded == "fajta" and alk_folded not in KEEP_FAJTA_ALKS:
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded == "alap" and alk_folded not in KEEP_ALAP_ALKS:
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded == "allat" and alk_folded not in KEEP_ALLAT_ALKS:
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded == "hokezeles" and alk_folded not in KEEP_HOKEZELES_ALKS:
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded == "felhasznalas" and alk_folded not in KEEP_FELHASZNALAS_ALKS:
            remove_prop(normalized, key, audit["props_removed"])
            continue
        if folded in DROP_PROPS_BY_ALK.get(alk_folded, set()):
            remove_prop(normalized, key, audit["props_removed"])
            continue

    infer_booleans(product, normalized, audit)

    compacted: dict[str, Any] = {}
    for key in sorted(normalized, key=fold_text):
        values = values_of(normalized[key])
        if key in BOOL_PROPS:
            raw = normalized[key]
            compacted[key] = bool(raw)
        elif not values:
            continue
        else:
            values = dedupe_values(values, key)
            if key in SCALAR_PROPS and len(values) == 1:
                compacted[key] = values[0]
            else:
                compacted[key] = values
    return compacted


def rebuild_category_tree(category_payload: dict[str, Any], products: list[dict[str, Any]], generated_at: str) -> dict[str, Any]:
    root_props: dict[str, dict[str, Any]] = {"egyedi": {}, "csoportos": {}}
    alk_products: dict[str, list[dict[str, Any]]] = defaultdict(list)
    alt_products: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        alk_products[product["alkategoria"]].append(product)
        alt_products[(product["alkategoria"], product["altipus"])].append(product)

    original_root = next(iter(category_payload["kategoria"].values()))
    original_order = list((folded_get(original_root, "alkategoriak", {}) or {}).keys())
    desired_order = [
        "Tej",
        "Tejital, jegeskávé",
        "Joghurt",
        RENAMED_IVOKAT,
        "Túró",
        "Krémtúró, túródesszert",
        "Tejföl",
        "Tejszín",
        "Vaj",
        "Margarin",
        "Sajt",
        "Sajtkrém, szendvicskrém",
        "Tejdesszert, puding",
        "Növényi alternatíva",
        "Tojás",
    ]
    ordered_alks = [alk for alk in desired_order if alk in alk_products]
    ordered_alks += [alk for alk in original_order if alk in alk_products and alk not in ordered_alks]
    ordered_alks += sorted([alk for alk in alk_products if alk not in ordered_alks], key=fold_text)

    new_alks: dict[str, Any] = {}
    for alk in ordered_alks:
        products_for_alk = alk_products[alk]
        alt_counts = Counter(product["altipus"] for product in products_for_alk)
        ordered_alts = [alt for alt, _count in alt_counts.most_common()]
        alk_node = {
            "tulajdonságok": build_prop_block(products_for_alk),
            "altípusok": {},
        }
        for alt in ordered_alts:
            alk_node["altípusok"][alt] = {
                "tulajdonságok": build_prop_block(alt_products[(alk, alt)])
            }
        new_alks[alk] = alk_node

    all_prop_block = build_prop_block(products)
    root_props["egyedi"].update(all_prop_block.get("egyedi", {}))
    root_props["csoportos"].update(all_prop_block.get("csoportos", {}))

    return {
        **category_payload,
        "meta": {
            **category_payload.get("meta", {}),
            "separate_working_copy": True,
            "generated_from": SOURCE_CATEGORY.name,
            "generated_at": generated_at,
            "logic_cleanup": True,
            "note": "Csak külön tejtermékes munkafájlokból készült; fő JSON fájlokat nem ír.",
        },
        "kategoria": {
            ROOT_NAME: {
                "tulajdonságok": root_props,
                "alkategóriák": new_alks,
            }
        },
    }


def folded_get(mapping: dict[str, Any], folded_name: str, default: Any = None) -> Any:
    if not isinstance(mapping, dict):
        return default
    target = fold_text(folded_name)
    for key, value in mapping.items():
        if fold_text(key) == target:
            return value
    return default


def build_prop_block(products: list[dict[str, Any]]) -> dict[str, Any]:
    values_by_prop: dict[str, list[Any]] = defaultdict(list)
    for product in products:
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            values_by_prop[prop_name].extend(values_of(raw_value))

    block = {"egyedi": {}, "csoportos": {}}
    for prop_name in sorted(values_by_prop, key=fold_text):
        if prop_name in BOOL_PROPS:
            target = block["egyedi"]
            target[prop_name] = {}
            continue

        values = dedupe_values(values_by_prop[prop_name], prop_name)
        if not values:
            continue
        target = block["egyedi"] if prop_name in EGYEDI_PROPS else block["csoportos"]
        target[prop_name] = sorted(values, key=fold_text)

    return block


def prune_rare_props_by_alk(products: list[dict[str, Any]], audit: dict[str, Any], max_count: int = 3) -> None:
    prop_counts_by_alk: dict[str, Counter[str]] = defaultdict(Counter)
    for product in products:
        for prop_name in product.get("tulajdonsagok", {}):
            prop_counts_by_alk[product["alkategoria"]][prop_name] += 1

    rare_by_alk: dict[str, set[str]] = {}
    for alk, counter in prop_counts_by_alk.items():
        rare_by_alk[alk] = {
            prop_name
            for prop_name, count in counter.items()
            if count <= max_count and prop_name not in RARE_PRUNE_PROTECTED_PROPS
        }

    for product in products:
        props = product.get("tulajdonsagok") or {}
        for prop_name in list(rare_by_alk.get(product["alkategoria"], set())):
            if prop_name in props:
                props.pop(prop_name, None)
                audit["props_removed"][prop_name] += 1
                audit["rare_props_pruned"][f"{product['alkategoria']} / {prop_name}"] += 1


def collect_declared_paths(category_payload: dict[str, Any]) -> set[tuple[str, str]]:
    root = next(iter(category_payload["kategoria"].values()))
    alks = folded_get(root, "alkategoriak", {}) or {}
    paths: set[tuple[str, str]] = set()
    for alk, alk_node in alks.items():
        altipusok = folded_get(alk_node, "altipusok", {}) or {}
        for alt in altipusok:
            paths.add((alk, alt))
    return paths


def collect_declared_props(category_payload: dict[str, Any]) -> set[str]:
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

    walk(category_payload)
    return props


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def validate(category_payload: dict[str, Any], products: list[dict[str, Any]]) -> dict[str, Any]:
    declared_paths = collect_declared_paths(category_payload)
    product_paths = Counter((product.get("alkategoria", ""), product.get("altipus", "")) for product in products)
    product_props = set()
    forbidden_props = Counter()
    prop_counts = Counter()
    prop_counts_by_alk: dict[str, Counter[str]] = defaultdict(Counter)
    for product in products:
        for prop_name in (product.get("tulajdonsagok") or {}):
            product_props.add(prop_name)
            prop_counts[prop_name] += 1
            prop_counts_by_alk[product.get("alkategoria", "")][prop_name] += 1
            folded = fold_text(prop_name)
            if (
                folded in ALWAYS_REMOVE_PROPS
                or folded == "jelleg"
                or (folded == "forma" and fold_text(product.get("alkategoria", "")) not in KEEP_FORMA_ALKS)
                or (folded == "fajta" and fold_text(product.get("alkategoria", "")) not in KEEP_FAJTA_ALKS)
                or (folded == "alap" and fold_text(product.get("alkategoria", "")) not in KEEP_ALAP_ALKS)
            ):
                forbidden_props[prop_name] += 1

    declared_props = collect_declared_props(category_payload)
    rare_props = {name: count for name, count in prop_counts.items() if count <= 3}
    rare_props_by_alk = {
        alk: {name: count for name, count in counter.items() if count <= 3 and name not in RARE_PRUNE_PROTECTED_PROPS}
        for alk, counter in prop_counts_by_alk.items()
    }
    rare_props_by_alk = {alk: props for alk, props in rare_props_by_alk.items() if props}
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
        "rare_props_max_3": rare_props,
        "rare_props_by_alk_max_3": rare_props_by_alk,
    }


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")
    category_payload = load_json(SOURCE_CATEGORY)
    product_payload = load_json(SOURCE_PRODUCTS)

    products_in = product_payload["termekek"]
    before_paths = Counter((product.get("alkategoria", ""), product.get("altipus", "")) for product in products_in)

    audit: dict[str, Any] = {
        "meta": {
            "generated_at": generated_at,
            "input_category_file": SOURCE_CATEGORY.name,
            "input_product_file": SOURCE_PRODUCTS.name,
            "output_category_file": OUT_CATEGORY.name,
            "output_product_file": OUT_PRODUCTS.name,
            "note": "Csak külön tejtermékes munkafájlokat olvas és ír.",
        },
        "moves": [],
        "move_reasons": Counter(),
        "props_added": Counter(),
        "props_removed": Counter(),
        "props_merged": Counter(),
        "rare_props_pruned": Counter(),
        "bool_filled": Counter(),
    }

    products_out: list[dict[str, Any]] = []
    for original in products_in:
        product = copy.deepcopy(original)
        props = copy.deepcopy(product.get("tulajdonsagok") or {})

        new_alk, new_alt = infer_alt_and_path(product, props, audit)
        product["fokategoria"] = ROOT_NAME
        product["alkategoria"] = new_alk
        product["altipus"] = new_alt

        props = normalize_props(product, props, audit)
        product["tulajdonsagok"] = props
        products_out.append(product)

    prune_rare_props_by_alk(products_out, audit)
    for product in products_out:
        product["kategoria_hash"] = kategoriak_hash(
            ROOT_NAME,
            product["alkategoria"],
            product["altipus"],
            product["tulajdonsagok"],
        )

    category_out = rebuild_category_tree(category_payload, products_out, generated_at)
    product_out = {
        **product_payload,
        "meta": {
            **product_payload.get("meta", {}),
            "separate_working_copy": True,
            "generated_from": SOURCE_PRODUCTS.name,
            "generated_at": generated_at,
            "logic_cleanup": True,
            "note": "Csak külön tejtermékes munkafájlokból készült; fő JSON fájlokat nem ír.",
        },
        "termekek": products_out,
    }

    after_paths = Counter((product.get("alkategoria", ""), product.get("altipus", "")) for product in products_out)
    validation = validate(category_out, products_out)

    audit_json = {
        **audit,
        "move_reasons": dict(audit["move_reasons"]),
        "props_added": dict(audit["props_added"]),
        "props_removed": dict(audit["props_removed"]),
        "props_merged": dict(audit["props_merged"]),
        "rare_props_pruned": dict(audit["rare_props_pruned"]),
        "bool_filled": dict(audit["bool_filled"]),
        "counts": {
            "products": len(products_out),
            "paths_before": len(before_paths),
            "paths_after": len(after_paths),
            "product_moves": len(audit["moves"]),
            "properties_added_or_inferred": sum(audit["props_added"].values()),
            "properties_removed": sum(audit["props_removed"].values()),
            "properties_merged": sum(audit["props_merged"].values()),
            "rare_properties_pruned": sum(audit["rare_props_pruned"].values()),
            "booleans_filled": sum(audit["bool_filled"].values()),
        },
        "before_paths": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in before_paths.most_common()
        ],
        "after_paths": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in after_paths.most_common()
        ],
        "validation": validation,
    }

    dump_json(OUT_CATEGORY, category_out)
    dump_json(OUT_PRODUCTS, product_out)
    dump_json(OUT_AUDIT_JSON, audit_json)

    lines = [
        "# Tejtermékek logikai tisztítás - külön munkafájl",
        "",
        f"- Generálva: {generated_at}",
        f"- Bemeneti kategória: `{SOURCE_CATEGORY.name}`",
        f"- Bemeneti termékek: `{SOURCE_PRODUCTS.name}`",
        f"- Kimeneti kategória: `{OUT_CATEGORY.name}`",
        f"- Kimeneti termékek: `{OUT_PRODUCTS.name}`",
        "- A fő `eredmeny.json` és `kategoriak_2026-06-13.json` fájlokat ez a script nem írja.",
        "",
        "## Összesítés",
    ]
    lines.extend(f"- {key}: {value}" for key, value in audit_json["counts"].items())
    lines.extend(
        [
            "",
            "## Fő logikai döntések",
            "- A `terméktípus`, `jelleg`, `termékcsalád`, `töltött`, `UHT`, `zsírtartalom_jelleg` jellegű ismétlő vagy kevert mezők törlésre/összevonásra kerültek.",
            "- A `ízesítés` értékei az egységes `íz` tulajdonságba kerültek.",
            "- A sajtnál az altípus a fő sajttípus lett; a konkrét sajtnevek és feldolgozási formák `fajta`/`forma` tulajdonságként maradtak.",
            "- A túró `Cottage cheese` és `Rögös túró` altípusai `Tehéntúró` alá kerültek, a szemcsés/rögös információ `forma` lett.",
            "- A `Vajkrém` termékek a sajtkrém/szendvicskrém alól a `Vaj / Vajkrém` útvonalra kerültek.",
            "- A növényi joghurt/fermentált készítmény és a külön növényi főzőkrém altípusok beolvadtak a meglévő növényi gyűjtő altípusokba.",
            "- A tojásnál a fürjtojás és tojáskészítmény jellegű termékek közös, tisztábban nevezett altípusba kerültek.",
            "",
            "## Validáció",
        ]
    )
    for key, value in validation.items():
        if key in {"missing_paths", "product_only_props", "category_only_props", "forbidden_props_left"}:
            lines.append(f"- {key}: {value}")
        elif key != "rare_props_max_3":
            lines.append(f"- {key}: {value}")

    lines.extend(["", "## Altípusok tisztítás után"])
    lines.extend(
        markdown_table(
            ["Alkategória", "Altípus", "Termék"],
            [[row["alkategoria"], row["altipus"], row["termek_db"]] for row in audit_json["after_paths"]],
        )
    )

    lines.extend(["", "## Legnagyobb mozgatási szabályok"])
    lines.extend(
        markdown_table(
            ["Mozgatás", "Termék"],
            [[reason, count] for reason, count in Counter(audit_json["move_reasons"]).most_common(30)],
        )
    )

    lines.extend(["", "## Törölt tulajdonságok"])
    lines.extend(
        markdown_table(
            ["Tulajdonság", "Törlés"],
            [[prop, count] for prop, count in Counter(audit_json["props_removed"]).most_common()],
        )
    )

    lines.extend(["", "## Ritka tulajdonságok max. 3 termékkel"])
    lines.extend(
        markdown_table(
            ["Tulajdonság", "Termék"],
            [[prop, count] for prop, count in sorted(validation["rare_props_max_3"].items(), key=lambda item: (item[1], fold_text(item[0])))],
        )
    )

    lines.extend(["", "## Alkategóriánként törölt ritka tulajdonságok"])
    lines.extend(
        markdown_table(
            ["Alkategória / tulajdonság", "Törlés"],
            [[prop, count] for prop, count in Counter(audit_json["rare_props_pruned"]).most_common()],
        )
    )

    OUT_AUDIT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"products={len(products_out)}")
    print(f"paths_before={len(before_paths)}")
    print(f"paths_after={len(after_paths)}")
    print(f"product_moves={len(audit['moves'])}")
    print(f"properties_removed={sum(audit['props_removed'].values())}")
    print(f"properties_added_or_inferred={sum(audit['props_added'].values())}")
    print(f"booleans_filled={sum(audit['bool_filled'].values())}")
    print(f"missing_paths={len(validation['missing_paths'])}")
    print(f"product_only_props={len(validation['product_only_props'])}")
    print(f"category_only_props={len(validation['category_only_props'])}")
    print(f"forbidden_props_left={sum(validation['forbidden_props_left'].values())}")
    print(f"audit={OUT_AUDIT_MD}")


if __name__ == "__main__":
    main()
