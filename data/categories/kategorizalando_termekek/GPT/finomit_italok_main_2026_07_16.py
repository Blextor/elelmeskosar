# -*- coding: utf-8 -*-
"""Bizonyítékalapú Ital-javítás a 2026-07-15-i audit után.

Alapértelmezésben száraz futás. A két fő adatfájlt csak a ``--apply`` kapcsoló
írja vissza. A kiszerelés nevű terméktulajdonságokat a program nem módosítja.
"""

from __future__ import annotations

import argparse
import builtins
import copy
import hashlib
import json
import re
import shutil
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

# Ezen a gépen a CPython JSON C-encodere nagy, ékezetes adathalmazon
# korábban hibázott, ezért a kiírást a standard library tiszta Python
# útjára tereljük. A dekódert nem cseréljük le: mindkét megvalósítást
# külön kipróbálva azonos, környezeti folyamat-instabilitás jelentkezett.
json.encoder.c_make_encoder = None


BASE = Path(__file__).resolve().parent
WORK = BASE / "italok_munkafajlok"
RESULT_PATH = BASE / "eredmeny.json"
CATEGORY_PATH = BASE / "kategoriak_2026-06-13.json"
REVIEW_DIR = WORK / "kepellenorzes_2026_07_16"
PLANT_REVIEW = REVIEW_DIR / "novenyi_italok.json"
ISSUE_REVIEW = REVIEW_DIR / "konkret_hibak.json"
BRAND_ROUND5 = WORK / "italok_brand_cleanup_round5_2026-06-30.json"
BRAND_ROUND12 = WORK / "italok_brand_cleanup_round12_2026-06-30.json"
AUDIT_PATH = WORK / "italok_finomitas_2026-07-16.json"
DRY_AUDIT_PATH = WORK / "italok_finomitas_2026-07-16_dry_run.json"
REPORT_PATH = WORK / "italok_finomitas_2026-07-16.md"
FINAL_CHECK_PATH = WORK / "italok_vegellenorzes_2026-07-16.json"

# Az eredeti állapotról induló teljes javítás összesített számai.
# Az idempotens utóellenőrzések Countere csak az adott futás deltája.
FULL_OPERATION_SUMMARY = {
    "Növényi ital az Ital ágba mozgatva": 163,
    "Főzési kókusztermék a tejágban megtartva": 4,
    "Konkrét, képpel igazolt kategóriamozgatás": 19,
    "Az alkategóriával azonos altípus törölve": 1210,
    "Nem méretjellegű placeholder érték törölve": 20385,
    "Minden terméknél hamis útvonaljelző törölve": 480,
    "Márkaérték elemivé téve": 553,
    "Márka-utótag jelentése külön tulajdonságban megőrizve": 551,
    "Borrégió/fajta téves márkamezőből áthelyezve": 17,
    "Atomi érték írásmódja kanonizálva": 22,
}

ITAL = "Ital"
DAIRY = "Tejtermékek és tojás"
PLANT_ALK = "Növényi alternatíva"
PLANT_DAIRY_ALT = "Növényi ital"
PLANT_COOKING_ALT = "Növényi főzőkrém / tejszín"

PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"

PLACEHOLDER_FOLDS = {
    "",
    "ismeretlen",
    "n a",
    "na",
    "nem adat",
    "nem jelolt",
    "nem megadott",
    "nincs",
    "nincs adat",
}

BOOL_PROPS = {
    "bio",
    "cukormentes / zero",
    "DRS",
    "édesítőszerrel",
    "gluténmentes",
    "gyógynövényes",
    "gyümölcsös",
    "ízesített",
    "kézműves",
    "koffeinmentes",
    "laktózmentes",
    "pürét tartalmaz",
    "szűretlen",
    "vegán",
}

SIZE_PROP_FOLDS = {
    "kiszereles",
    "kiszereles csomagolas",
    "kiszereles rendszer",
}

COPIED_ALT_ALKS = {
    "Energiaital",
    "Ízesített víz",
    "Pezsgő",
    "Cider",
    "Sportital",
    "Citromlé",
    "Funkcionális ital",
    "Kombucha",
}

COCONUT_COOKING_IDS = {
    "c4a084a2d4aeb2442cbcba78",
    "242d8040cc313808252913f3",
    "bc09c557e3fe694d1f4dee07",
    "dde4ef9f725c9fca4d36c0c3",
}

PLANT_BASE_CORRECTIONS = {
    "4604651": ["zab"],
    "1000957:4538347": ["kókusz", "szója"],
    "1031498:4568888": ["kókusz", "szója"],
    "BTY-X10253000320021": ["kókusz", "szója"],
}

PATH_MOVES = {
    # 4.1 – képpel igazolt, 100%-os frissen préselt levek.
    "588146:4125536": ("Gyümölcslé", "Vegyes gyümölcs- és zöldséglé"),
    "588140:4125530": ("Gyümölcslé", "Vegyes gyümölcs- és zöldséglé"),
    "588137:4125527": ("Gyümölcslé", "Vegyes gyümölcs- és zöldséglé"),
    # 4.2 – alkoholmentes sör/radler.
    "533763": ("Sör", "Alkoholmentes radler"),
    "1012024:4549414": ("Sör", "Alkoholmentes sör"),
    "1032338:4569728": ("Sör", "Alkoholmentes radler"),
    "1032335:4569725": ("Sör", "Alkoholmentes radler"),
    # 4.2 – alkoholmentes habzó italok.
    "10101641": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X17216800320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X17216400320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X18133000320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    "BTY-X17216900320021": ("Habzó-, gyöngyözőbor, boralapú ital", "Alkoholmentes habzó ital"),
    # 4.2 – alkoholmentes borok.
    "BTY-X18034900320021": ("Bor", "Alkoholmentes bor"),
    "BTY-X18035000320021": ("Bor", "Alkoholmentes bor"),
    "BTY-X18035100320021": ("Bor", "Alkoholmentes bor"),
    # 4.3 – gyerek-/partyitalok.
    "769656:4307046": ("Üdítőital", "Gyerekital"),
    "679217:4216607": ("Üdítőital", "Gyerekital"),
    "748902:4286292": ("Üdítőital", "Gyerekital"),
    "769659:4307049": ("Üdítőital", "Gyerekital"),
}

MINI_SPIRIT_IDS = {"566017", "1014576", "1055675"}
TATRATEA_SET_IDS = {"442852:3980236", "BTY-X9705200320021"}
HOMOLA_ID = "121224421"

BRAND_MANUAL_MAP = {
    "1664 Blanc": "1664",
    "1664 Lager": "1664",
    "1664 Rosé": "1664",
    "Homola 100% Balaton": "Homola",
    "Joya Barista": "Joya",
    "Joya Protein": "Joya",
    "Joya PUR": "Joya",
    "Joya Rizs": "Joya",
    "Joya Voll": "Joya",
    "Koch Frissen Préselt": "Koch",
    "Kopparberg Strawberry & Lime": "Kopparberg",
    "Mionetto Prosecco DOC Treviso Brut": "Mionetto",
    "Moët & Chandon Brut Impérial": "Moët & Chandon",
    "NATUREO": "Natureo",
    "Peroni Nastro Azzurro Arancia Rossa": "Peroni Nastro Azzurro",
    "Peroni Nastro Azzurro Limone di Sicilia": "Peroni Nastro Azzurro",
    "Riso Scotti Barista": "Riso Scotti",
    "Somersby Strawberry & Lime": "Somersby",
    "Appelle Moi Bitter & Orange": "Appelle Moi",
    "Cinzano Prosecco D.O.C.": "Cinzano",
    "Friss 0,0%": "Friss",
    "Royal Boldog Névnapot!": "Royal",
    "Royal Boldog Születésnapot!": "Royal",
    "Royal Hugo": "Royal",
    "Royal Hugo A/ Spritz": "Royal",
    "Royal Original": "Royal",
    "Torres Serena": "Torres",
    "Prime Ice Hydration Blue Chill": "Prime Hydration",
    "Prime Ice Hydration Orange": "Prime Hydration",
    "Prime Ice Hydration Red Chill": "Prime Hydration",
    "Sodastream 7Up Zero": "Sodastream 7Up",
    "Sodastream Mirinda Zero": "Sodastream Mirinda",
    "Sodastream Pepsi Zero": "Sodastream Pepsi",
}

BRAND_FAMILY_PREFIXES = {
    "Almdudler",
    "Aqvital",
    "Arizona",
    "Auchan",
    "Basilur",
    "Bella Cucina",
    "Bodri",
    "Borsodi",
    "Budweiser Budvar",
    "Bumbu",
    "Caffè Borbone",
    "Capri-Sun",
    "Coop",
    "Corona",
    "Davidoff",
    "Edelweiss",
    "Gösser",
    "Grey Goose",
    "Happy",
    "Hoegaarden",
    "Hohes C",
    "Inka",
    "Jana",
    "Joe Rebel",
    "Kopparberg",
    "L'OR",
    "LAFI",
    "Lipton",
    "Mészáros Pál",
    "Miller",
    "Mokate",
    "Mort Subite",
    "Night Orient",
    "Penny",
    "Portorico",
    "Prime Hydration",
    "Pure Star",
    "Pécsi Sör",
    "Pécsi",
    "Royal",
    "Sió",
    "Smirnoff",
    "Sodastream 7Up",
    "Sodastream Mirinda",
    "Sodastream Pepsi",
    "Soproni",
    "SPAR",
    "Strongbow",
    "Süsü",
    "Sweetab",
    "Swiss Laboratory",
    "Szentkirályi",
    "Tesco",
    "Tetley",
    "Tokajicum",
    "Tropical",
    "Tubi 60",
    "Vida Péter",
    "Vitalade",
    "Vöslauer",
}

BRAND_FAMILY_EXCLUSIONS = {
    "ROYAL PORT",
    "Royal Crown",
    "Royal Oporto",
    "Royal Tokaji",
}

FAKE_WINE_BRAND_ROUTES = {
    "Balatoni Friss": (["Balaton"], [], ["Friss"]),
    "Balatoni Rosé": (["Balaton"], ["rosé"], []),
    "Balatonmelléki Rosé": (["Balatonmelléke"], ["rosé"], []),
    "Duna-Tisza közi Muskotály": (["Duna-Tisza köze"], ["muskotály"], []),
    "Duna-Tisza közi Rosé Cuvée": (["Duna-Tisza köze"], ["rosé", "cuvée"], []),
    "Dunántúli Merlot": (["Dunántúl"], ["Merlot"], []),
    "Superior Egri Bikavér": (["Eger"], ["Egri Bikavér"], ["Superior"]),
    "Tokaji Furmint": (["Tokaj"], ["Furmint"], []),
    "Tokaji Késői Szüret": (["Tokaj"], ["késői szüret"], []),
    "Villányi": (["Villány"], [], []),
    "Villányi Cabernet Sauvignon": (["Villány"], ["Cabernet Sauvignon"], []),
    "Villányi Merlot": (["Villány"], ["Merlot"], []),
    "Villányi Rosé Cuvée": (["Villány"], ["rosé", "cuvée"], []),
    "Villányi Syrah": (["Villány"], ["Syrah"], []),
}

BRAND_VARIANT_FEATURES = {
    "1664 Blanc": ("változat", "Blanc"),
    "1664 Lager": ("változat", "Lager"),
    "1664 Rosé": ("változat", "Rosé"),
    "Joya Barista": ("felhasználás", "barista"),
    "Joya Protein": ("tartalom", "protein"),
    "Riso Scotti Barista": ("felhasználás", "barista"),
    "Royal Boldog Névnapot!": ("változat", "Boldog névnapot"),
    "Royal Boldog Születésnapot!": ("változat", "Boldog születésnapot"),
    "Royal Hugo": ("változat", "Hugo"),
    "Royal Hugo A/ Spritz": ("változat", "Hugo Spritz"),
}

BRAND_VARIANT_ROUTES = {
    "Appelle Moi Bitter & Orange": {"íz": ["keserű", "narancs"]},
    "Cinzano Prosecco D.O.C.": {
        "szőlőfajta / borstílus": ["Prosecco"],
        "eredetvédelem": ["DOC"],
    },
    "Kopparberg Strawberry & Lime": {"íz": ["eper", "lime"]},
    "Mionetto Prosecco DOC Treviso Brut": {
        "szőlőfajta / borstílus": ["Prosecco"],
        "borvidék / eredet": ["Treviso"],
        "édesség": ["brut"],
        "eredetvédelem": ["DOC"],
    },
    "Moët & Chandon Brut Impérial": {
        "édesség": ["brut"],
        "változat": ["Impérial"],
    },
    "Peroni Nastro Azzurro Arancia Rossa": {"íz": ["vérnarancs"]},
    "Peroni Nastro Azzurro Limone di Sicilia": {"íz": ["citrom"]},
    "Prime Ice Hydration Blue Chill": {"változat": ["Blue Chill"]},
    "Prime Ice Hydration Orange": {"íz": ["narancs"]},
    "Prime Ice Hydration Red Chill": {"változat": ["Red Chill"]},
    "Somersby Strawberry & Lime": {"íz": ["eper", "lime"]},
}

ATOMIC_VALUE_CANONICAL = {
    ("marka", "moet chandon"): "Moët & Chandon",
    ("marka", "oatly"): "Oatly!",
    ("szolofajta borstilus", "rose"): "Rosé",
    ("valtozat", "hugo"): "Hugo",
}

FLAVOR_ATOMS = [
    ("gránátalma", ["granatalma", "granatalmas"]),
    ("feketeribizli", ["feketeribizli", "fekete ribizli"]),
    ("őszibarack", ["oszibarack", "oszibarackos"]),
    ("sárgabarack", ["sargabarack", "sargabarackos", "kajszibarack"]),
    ("kékszőlő", ["kekszolo", "kek szolo"]),
    ("erdei gyümölcs", ["erdei gyumolcs"]),
    ("piros gyümölcs", ["piros gyumolcs"]),
    ("bogyós gyümölcs", ["bogyos gyumolcs"]),
    ("aloe vera", ["aloe vera"]),
    ("citromfű", ["citromfu", "citromfuves"]),
    ("homoktövis", ["homoktovis"]),
    ("csipkebogyó", ["csipkebogyo"]),
    ("vörös tea", ["voros tea"]),
    ("alma", ["alma", "almas"]),
    ("körte", ["korte", "kortes"]),
    ("eper", ["eper", "epres"]),
    ("málna", ["malna", "malnas"]),
    ("áfonya", ["afonya", "afonyas"]),
    ("szeder", ["szeder", "szedres", "feketeszeder"]),
    ("ribizli", ["ribizli", "ribizlis"]),
    ("meggy", ["meggy", "meggyes"]),
    ("cseresznye", ["cseresznye", "cseresznyes"]),
    ("szilva", ["szilva", "szilvas"]),
    ("barack", ["barack", "barackos"]),
    ("narancs", ["narancs", "narancsos"]),
    ("vérnarancs", ["vernarancs"]),
    ("citrom", ["citrom", "citromos"]),
    ("lime", ["lime", "limett"]),
    ("grapefruit", ["grapefruit"]),
    ("kivi", ["kivi", "kiwi"]),
    ("banán", ["banan", "bananos"]),
    ("ananász", ["ananasz", "ananaszos"]),
    ("mangó", ["mango", "mangos"]),
    ("maracuja", ["maracuja", "passio", "passion fruit"]),
    ("görögdinnye", ["gorogdinnye", "dinnye"]),
    ("szőlő", ["szolo", "szolos"]),
    ("kaktusz", ["kaktusz", "kaktuszos"]),
    ("pomelo", ["pomelo"]),
    ("bodza", ["bodza", "bodzas"]),
    ("gyömbér", ["gyomber", "gyomberes"]),
    ("menta", ["menta", "mentas"]),
    ("levendula", ["levendula"]),
    ("ginzeng", ["ginzeng", "ginseng"]),
    ("hibiszkusz", ["hibiszkusz"]),
    ("uborka", ["uborka", "uborkas"]),
    ("paradicsom", ["paradicsom", "paradicsomos"]),
    ("cékla", ["cekla", "ceklas"]),
    ("sárgarépa", ["sargarepa"]),
    ("chili", ["chili", "chilis"]),
    ("kóla", ["kola", "cola"]),
    ("tonik", ["tonik", "tonic"]),
    ("tuttifrutti", ["tuttifrutti", "tutti frutti"]),
    ("kávé", ["kave", "kaves", "coffee"]),
    ("matcha", ["matcha"]),
    ("tea", ["tea"]),
    ("kakaó", ["kakao", "kakaos"]),
    ("csokoládé", ["csokolade", "csokolades", "csokis", "csoki", "chocolate"]),
    ("mogyoró", ["mogyoro", "mogyoros", "hazelnut"]),
    ("mandula", ["mandula", "mandulas"]),
    ("kókusz", ["kokusz", "kokuszos", "coconut"]),
    ("pisztácia", ["pisztacia", "pisztacias"]),
    ("dió", ["dio", "dios"]),
    ("karamell", ["karamell", "karamellas", "caramel"]),
    ("vanília", ["vanilia", "vanilias"]),
    ("fahéj", ["fahej", "fahejas", "cinnamon"]),
    ("méz", ["mez", "mezes"]),
    ("sós", ["sos", "sozott"]),
    ("édes", ["edes"]),
    ("savanyú", ["savanyu"]),
    ("natúr", ["natur", "natural", "original", "sima"]),
]

SIMPLE_ATOMIC_MAP = {
    "citromlime": ["citrom", "lime"],
    "citrom lime": ["citrom", "lime"],
    "csoko nut": ["csokoládé", "mogyoró"],
    "edes savanyu": ["édes", "savanyú"],
    "kola": ["kóla"],
    "cola": ["kóla"],
    "sima": ["natúr"],
    "natur": ["natúr"],
    "original": ["natúr"],
    "gyumolcsos": ["gyümölcs"],
    "gyumolcs": ["gyümölcs"],
    "vegyes gyumolcsos": ["vegyes gyümölcs"],
    "vegyes gyumolcs": ["vegyes gyümölcs"],
    "piros gyumolcs": ["piros gyümölcs"],
    "bogyos gyumolcs": ["bogyós gyümölcs"],
    "erdei gyumolcs": ["erdei gyümölcs"],
}

CONTENT_MAP = {
    "5 vitamin": "vitamin",
    "6 vitamin": "vitamin",
    "8 vitamin": "vitamin",
    "asvanyi anyagokkal": "ásványi anyag",
    "b12 vitaminnal": "B12-vitamin",
    "b2 vitaminnal": "B2-vitamin",
    "b5 vitamin": "B5-vitamin",
    "b6 vitamin": "B6-vitamin",
    "c vitamin": "C-vitamin",
    "d vitaminnal": "D-vitamin",
    "d2 vitaminnal": "D2-vitamin",
    "feherjeben gazdag": "protein",
    "hozzaadott kalciummal": "kalcium",
    "joddal": "jód",
    "kalciummal": "kalcium",
    "vitaminok": "vitamin",
    "vitaminos": "vitamin",
}


def fold_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.casefold()
    text = re.sub(r"[^0-9a-z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def folded_get(mapping: dict[str, Any], name: str, default: Any = None) -> Any:
    target = fold_text(name)
    for key, value in mapping.items():
        if fold_text(key) == target:
            return value
    return default


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: Any) -> None:
    # A gyors C encoder ezen a gépen nagy, ékezetes objektumnál korábban hibázott.
    json.encoder.c_make_encoder = None
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with temp.open(encoding="utf-8") as handle:
        json.load(handle)
    temp.replace(path)


def write_main_files_transactionally(products: list[dict[str, Any]], categories: dict[str, Any]) -> None:
    result_stage = RESULT_PATH.with_name(RESULT_PATH.name + ".ital-stage")
    category_stage = CATEGORY_PATH.with_name(CATEGORY_PATH.name + ".ital-stage")
    result_backup = RESULT_PATH.with_name(RESULT_PATH.name + ".pre-ital-fix.bak")
    category_backup = CATEGORY_PATH.with_name(CATEGORY_PATH.name + ".pre-ital-fix.bak")
    auxiliaries = (result_stage, category_stage, result_backup, category_backup)
    existing = [str(path) for path in auxiliaries if path.exists()]
    if existing:
        raise RuntimeError(f"Korábbi staging/backup fájl maradt vissza: {existing}")

    dump_json(result_stage, products)
    dump_json(category_stage, categories)
    shutil.copy2(RESULT_PATH, result_backup)
    shutil.copy2(CATEGORY_PATH, category_backup)
    try:
        result_stage.replace(RESULT_PATH)
        category_stage.replace(CATEGORY_PATH)
        if len(load_json(RESULT_PATH)) != 47030:
            raise RuntimeError("Written result file failed read-back validation")
        if ITAL not in load_json(CATEGORY_PATH):
            raise RuntimeError("Written category file failed read-back validation")
    except BaseException:
        shutil.copy2(result_backup, RESULT_PATH)
        shutil.copy2(category_backup, CATEGORY_PATH)
        raise
    else:
        result_backup.unlink()
        category_backup.unlink()
    finally:
        for path in (result_stage, category_stage):
            if path.exists():
                path.unlink()


def values_of(value: Any) -> list[Any]:
    if value is None or value == "" or value == [] or value == {}:
        return []
    if isinstance(value, list):
        out: list[Any] = []
        for item in value:
            out.extend(values_of(item))
        return out
    return [value]


def dedupe(values: Iterable[Any]) -> list[Any]:
    out: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value is None or value == "":
            continue
        key = fold_text(value)
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def clean_text(value: Any) -> str:
    text = re.sub(r"\s+", " ", str(value)).strip()
    text = text.replace("ízü", "ízű")
    return text


def is_placeholder(value: Any) -> bool:
    return not isinstance(value, bool) and fold_text(value) in PLACEHOLDER_FOLDS


def is_size_prop(prop_name: str) -> bool:
    return fold_text(prop_name) in SIZE_PROP_FOLDS


def shape_of(value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    if isinstance(value, list):
        return "multi"
    return "single"


def normalize_alcohol_atom(value: Any) -> str | None:
    text = clean_text(value)
    folded = fold_text(text)
    if folded in PLACEHOLDER_FOLDS:
        return None
    if "alkoholmentes" in folded or folded in {"0", "0 0", "0 0%"}:
        return "0,0%"
    if folded == "alkoholos":
        return "alkoholos"
    match = re.search(r"(\d+(?:[,.]\d+)?)\s*%?", text)
    if not match:
        return text
    number = match.group(1).replace(".", ",")
    if "," in number:
        number = number.rstrip("0").rstrip(",")
    if number == "0":
        number = "0,0"
    return f"{number}%"


def pattern_matches(folded: str, pattern: str) -> bool:
    if len(pattern) <= 4 and " " not in pattern:
        return bool(re.search(rf"(^|\s){re.escape(pattern)}($|\s)", folded))
    return pattern in folded


def flavor_matches(folded: str) -> list[str]:
    matches: list[str] = []
    for canonical, patterns in FLAVOR_ATOMS:
        if builtins.any(pattern_matches(folded, pattern) for pattern in patterns):
            matches.append(canonical)
    suppressions = {
        "gránátalma": {"alma"},
        "feketeribizli": {"ribizli"},
        "őszibarack": {"barack"},
        "sárgabarack": {"barack"},
        "kékszőlő": {"szőlő"},
        "vérnarancs": {"narancs"},
        "vörös tea": {"tea"},
        "matcha": {"tea"},
    }
    for specific, generics in suppressions.items():
        if specific in matches:
            matches = [value for value in matches if value not in generics]
    return dedupe(matches)


def atomize_flavor(value: Any) -> list[str]:
    text = clean_text(value)
    folded = fold_text(text)
    if folded in PLACEHOLDER_FOLDS:
        return []
    if folded in SIMPLE_ATOMIC_MAP:
        return SIMPLE_ATOMIC_MAP[folded]
    matches = flavor_matches(folded)
    has_separator = bool(re.search(r"[/,+&]|\bés\b|(?<=\w)-(?=\w)", text, flags=re.IGNORECASE))
    if len(matches) >= 2:
        return matches
    if has_separator and not matches:
        parts = [clean_text(part) for part in re.split(r"\s*(?:/|,|\+|&|\bés\b|-)\s*", text, flags=re.IGNORECASE)]
        return [part for part in parts if part]
    if len(matches) == 1:
        return matches
    return [text]


def atomize_general_list_value(prop_name: str, value: Any) -> list[str]:
    text = clean_text(value)
    folded = fold_text(text)
    if folded in PLACEHOLDER_FOLDS:
        return []
    if fold_text(prop_name) in {"szolofajta borstilus"} and "-" in text:
        parts = [part.strip() for part in text.split("-") if part.strip()]
        if len(parts) > 1:
            return parts
    if re.search(r"[/,+&]|\bés\b", text, flags=re.IGNORECASE):
        parts = [
            clean_text(part)
            for part in re.split(r"\s*(?:/|,|\+|&|\bés\b)\s*", text, flags=re.IGNORECASE)
            if clean_text(part)
        ]
        if len(parts) > 1:
            return parts
    return [text]


def normalize_content(value: Any) -> list[str]:
    text = clean_text(value)
    folded = fold_text(text)
    if folded in PLACEHOLDER_FOLDS:
        return []
    if folded in CONTENT_MAP:
        return [CONTENT_MAP[folded]]
    parts = re.split(r"\s*(?:/|,|\+|&|\bés\b)\s*", text, flags=re.IGNORECASE)
    if len(parts) > 1:
        return dedupe(CONTENT_MAP.get(fold_text(part), clean_text(part)) for part in parts if clean_text(part))
    return [text]


def load_brand_map() -> dict[str, str]:
    mapping = dict(BRAND_MANUAL_MAP)
    round5 = load_json(BRAND_ROUND5)
    for label, _count in round5.get("product_changes", []):
        if " -> " in label:
            old, new = label.split(" -> ", 1)
            mapping[old] = new
    round12 = load_json(BRAND_ROUND12)
    for row in round12.get("product_changes_first", []):
        if len(row) >= 3:
            mapping[str(row[1])] = str(row[2])
    mapping.update(BRAND_MANUAL_MAP)
    return mapping


def extend_brand_map_from_products(mapping: dict[str, str], products: list[dict[str, Any]]) -> None:
    families = sorted(BRAND_FAMILY_PREFIXES, key=lambda value: (-len(value), value.casefold()))
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        brand = folded_get(product.get("tulajdonsagok") or {}, "marka")
        if not isinstance(brand, str) or brand in BRAND_FAMILY_EXCLUSIONS:
            continue
        for family in families:
            if brand.casefold().startswith(family.casefold() + " "):
                mapping.setdefault(brand, family)
                break


def load_review() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    def index(path: Path) -> dict[str, dict[str, Any]]:
        return {str(row["store_product_id"]): row for row in load_json(path)}

    return index(PLANT_REVIEW), index(ISSUE_REVIEW)


def product_id(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("store_product_id") or "")


def product_name(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("product_name") or "")


def is_de_karavan(product: dict[str, Any]) -> bool:
    return "d e karavan" in fold_text(product_name(product))


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


def append_list(props: dict[str, Any], prop_name: str, values: Iterable[Any]) -> None:
    clean_values = [value for value in values if value is not None and value != ""]
    if not clean_values:
        return
    existing = values_of(props.get(prop_name))
    props[prop_name] = dedupe([*existing, *clean_values])


def preserve_size_snapshot(products: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    snapshot: dict[int, dict[str, Any]] = {}
    for index, product in enumerate(products):
        snapshot[index] = {
            key: copy.deepcopy(value)
            for key, value in (product.get("tulajdonsagok") or {}).items()
            if is_size_prop(key)
        }
    return snapshot


def preserve_category_state(products: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    return {
        index: {
            "fokategoria": product.get("fokategoria"),
            "alkategoria": product.get("alkategoria"),
            "altipus": product.get("altipus"),
            "tulajdonsagok": copy.deepcopy(product.get("tulajdonsagok") or {}),
        }
        for index, product in enumerate(products)
    }


def merge_prop(props: dict[str, Any], prop_name: str, value: Any) -> None:
    if value is None or value == "" or value == []:
        return
    if prop_name not in props:
        props[prop_name] = copy.deepcopy(value)
        return
    existing = props[prop_name]
    if isinstance(existing, bool) and isinstance(value, bool):
        props[prop_name] = existing or value
        return
    merged = dedupe([*values_of(existing), *values_of(value)])
    if isinstance(existing, list) or isinstance(value, list) or len(merged) > 1:
        props[prop_name] = merged
    elif merged:
        props[prop_name] = merged[0]


def plant_alt_for_base(raw_base: Any) -> str:
    atoms = {fold_text(value) for value in values_of(raw_base) if not is_placeholder(value)}
    if len(atoms) > 1:
        return "Kevert növényi ital"
    base = next(iter(atoms), "")
    return {
        "zab": "Zabital",
        "mandula": "Mandulaital",
        "kokusz": "Kókuszital",
        "rizs": "Rizsital",
        "szoja": "Szójaital",
        "mogyoro": "Mogyoróital",
    }.get(base, "Egyéb növényi ital")


def normalize_plant_properties(
    product: dict[str, Any],
    corrected_base: list[str] | None,
    audit: Counter[str],
) -> dict[str, Any]:
    source = product.get("tulajdonsagok") or {}
    out: dict[str, Any] = {}
    for prop_name, raw_value in source.items():
        folded = fold_text(prop_name)
        if is_size_prop(prop_name):
            out[prop_name] = copy.deepcopy(raw_value)
            continue
        if folded == "marka":
            out["márka"] = raw_value
        elif folded == "bio" and raw_value is True:
            out["bio"] = True
        elif folded in {"cukormentes hozzaadott cukor nelkul", "cukormentes zero"} and raw_value is True:
            out["cukormentes / zero"] = True
        elif folded == "glutenmentes" and raw_value is True:
            out["gluténmentes"] = True
        elif folded == "protein magas feherje" and raw_value is True:
            append_list(out, "tartalom", ["protein"])
        elif folded == "light csokkentett zsir" and raw_value is True:
            append_list(out, "zsírtartalom", ["zsírszegény"])
        elif folded == "alap":
            append_list(out, "alap", corrected_base or values_of(raw_value))
        elif folded == "dusitas":
            for value in values_of(raw_value):
                append_list(out, "tartalom", normalize_content(value))
        elif folded == "felhasznalas":
            for value in values_of(raw_value):
                if fold_text(value) not in PLACEHOLDER_FOLDS | {"altalanos"}:
                    append_list(out, "felhasználás", [clean_text(value)])
        elif folded == "hokezeles":
            for value in values_of(raw_value):
                if not is_placeholder(value):
                    append_list(out, "feldolgozás", [clean_text(value)])
        elif folded == "iz":
            for value in values_of(raw_value):
                append_list(out, "íz", atomize_flavor(value))
        elif folded == "zsirtartalom":
            kept = [clean_text(value) for value in values_of(raw_value) if not is_placeholder(value)]
            if kept:
                out["zsírtartalom"] = kept
        elif folded in {"cukrozott", "izesitett", "laktozmentes", "vegan"}:
            # A növényi ital kategóriában ezek vagy a kategóriából következnek,
            # vagy a tényleges íz/cukor tulajdonság hordozza az információt.
            continue
        else:
            kept = [copy.deepcopy(value) for value in values_of(raw_value) if not is_placeholder(value)]
            if kept:
                out[prop_name] = kept if isinstance(raw_value, list) else kept[0]
    if corrected_base:
        out["alap"] = dedupe(corrected_base)
        audit["plant_base_corrected_from_image"] += 1
    return out


def route_semantic_value(
    out: dict[str, Any],
    source_prop: str,
    value: Any,
    audit: Counter[str],
) -> None:
    folded = fold_text(value)
    if folded in PLACEHOLDER_FOLDS:
        audit["placeholder_values_removed"] += 1
        return
    if folded == "alkoholmentes":
        audit[f"irrelevant_alcoholfree_removed_from_{fold_text(source_prop)}"] += 1
    elif folded in {"zero", "sugarfree", "cukormentes"}:
        merge_prop(out, "cukormentes / zero", True)
        audit["zero_routed"] += 1
    elif folded in {"vitamin", "vitaminos"}:
        append_list(out, "tartalom", ["vitamin"])
        audit["vitamin_routed"] += 1
    elif folded == "bio":
        merge_prop(out, "bio", True)
        audit["bio_routed"] += 1
    elif fold_text(source_prop) == "funkcio":
        append_list(out, "hatóanyag / cél", [clean_text(value)])
        audit["function_routed"] += 1
    else:
        append_list(out, "változat", [clean_text(value)])
        audit["variant_routed"] += 1


def route_processing_value(
    out: dict[str, Any],
    value: Any,
    audit: Counter[str],
) -> None:
    folded = fold_text(value)
    if folded in PLACEHOLDER_FOLDS:
        audit["placeholder_values_removed"] += 1
    elif folded == "alkoholmentes":
        audit["irrelevant_alcoholfree_removed_from_feldolgozas"] += 1
    elif folded in {"zero", "sugarfree", "cukormentes"}:
        merge_prop(out, "cukormentes / zero", True)
        audit["zero_routed"] += 1
    elif folded in {"vitamin", "vitaminos"}:
        append_list(out, "tartalom", ["vitamin"])
        audit["vitamin_routed"] += 1
    elif folded == "bio":
        merge_prop(out, "bio", True)
        audit["bio_routed"] += 1
    elif folded in {"pure", "purevel", "pure tartalmu"}:
        merge_prop(out, "pürét tartalmaz", True)
        audit["puree_routed"] += 1
    else:
        mapping = {
            "kozvetlenul preselt": "közvetlenül préselt",
            "hidegen preselt": "hidegen préselt",
            "preselt": "préselt",
            "fagyasztva szaritott": "fagyasztva szárított",
            "fermentalt": "fermentált",
            "frissen preselt": "frissen préselt",
        }
        append_list(out, "feldolgozás", [mapping.get(folded, clean_text(value))])


def canonical_prop_name(prop_name: str) -> str:
    return {
        "alapanyag": "alap",
        "asvanyi anyag": "tartalom",
        "borvidek": "borvidék / eredet",
        "citrom tartalom": "gyümölcstartalom",
        "cukormentes diabetikus": "cukormentes / zero",
        "dusitas": "tartalom",
        "hozzaadott vitamin asvanyi anyag": "tartalom",
        "novenyi alap": "alap",
        "protein": "tartalom",
        "szolofajta": "szőlőfajta / borstílus",
    }.get(fold_text(prop_name), prop_name)


def route_brand_variant(
    out: dict[str, Any],
    old_brand: str,
    new_brand: str,
    audit: Counter[str],
) -> None:
    explicit = BRAND_VARIANT_ROUTES.get(old_brand)
    if explicit:
        for prop_name, values in explicit.items():
            append_list(out, prop_name, values)
        audit["brand_variant_explicitly_routed"] += 1
        return

    feature = BRAND_VARIANT_FEATURES.get(old_brand)
    if feature:
        append_list(out, feature[0], [feature[1]])
        audit["brand_variant_explicitly_routed"] += 1
        return

    suffix = ""
    if old_brand.casefold().startswith(new_brand.casefold() + " "):
        suffix = old_brand[len(new_brand) :].strip(" -_/")
    if not suffix:
        return

    folded_suffix = fold_text(suffix)
    semantic_only = False
    if re.search(r"(^| )(zero|sugarfree|cukormentes|cero)( |$)", folded_suffix):
        merge_prop(out, "cukormentes / zero", True)
        semantic_only = folded_suffix in {"zero", "sugarfree", "cukormentes", "cero"}
    if "0 0" in folded_suffix:
        append_list(out, "alkoholtartalom", ["0,0%"])
        semantic_only = folded_suffix == "0 0"
    if "multivitamin" in folded_suffix or "vitamin" in folded_suffix:
        append_list(out, "tartalom", ["vitamin"])
        semantic_only = folded_suffix in {"multivitamin", "vitamin"}
    if "barista" in folded_suffix:
        append_list(out, "felhasználás", ["barista"])
        semantic_only = folded_suffix == "barista"
    if "protein" in folded_suffix:
        append_list(out, "tartalom", ["protein"])
        semantic_only = folded_suffix == "protein"
    if "collagen" in folded_suffix or "kollagen" in folded_suffix:
        append_list(out, "tartalom", ["kollagén"])
        semantic_only = folded_suffix in {"collagen", "kollagen"}

    if folded_suffix.startswith("super shots "):
        append_list(out, "változat", ["Super Shots"])
        append_list(out, "hatóanyag / cél", [suffix.split()[-1]])
        audit["brand_variant_semantics_routed"] += 1
        return

    if not semantic_only:
        append_list(out, "változat", atomize_general_list_value("változat", suffix))
    audit["brand_variant_semantics_routed"] += 1


def normalize_ital_properties(
    product: dict[str, Any],
    brand_map: dict[str, str],
    audit: Counter[str],
) -> dict[str, Any]:
    original = product.get("tulajdonsagok") or {}
    out: dict[str, Any] = {}
    for raw_prop_name, raw_value in original.items():
        raw_folded = fold_text(raw_prop_name)
        if is_size_prop(raw_prop_name):
            out[raw_prop_name] = copy.deepcopy(raw_value)
            continue
        if raw_folded in {"termekcsalad", "funkcio", "minosites"}:
            for value in values_of(raw_value):
                route_semantic_value(out, raw_prop_name, value, audit)
            continue
        if raw_folded == "feldolgozas":
            for value in values_of(raw_value):
                route_processing_value(out, value, audit)
            continue
        if raw_folded == "jellemzok":
            for value in values_of(raw_value):
                folded = fold_text(value)
                if folded in PLACEHOLDER_FOLDS | {"nincs"}:
                    audit["placeholder_or_empty_feature_removed"] += 1
                elif folded == "bio":
                    merge_prop(out, "bio", True)
                elif folded == "glutenmentes":
                    merge_prop(out, "gluténmentes", True)
                elif folded in {"cukormentes", "zero", "sugarfree"}:
                    merge_prop(out, "cukormentes / zero", True)
                elif folded in {
                    "vitaminos",
                    "asvanyi anyagokkal",
                    "kalciummal",
                    "hozzaadott kalciummal",
                    "d2 vitaminnal",
                    "b12 vitaminnal",
                    "d vitaminnal",
                    "joddal",
                    "feherjeben gazdag",
                }:
                    append_list(out, "tartalom", normalize_content(value))
                elif folded == "barista":
                    append_list(out, "felhasználás", ["barista"])
                elif folded == "uht":
                    append_list(out, "feldolgozás", ["UHT"])
                elif folded == "szensavas":
                    append_list(out, "szénsavasság", ["szénsavas"])
                elif folded == "edesitett":
                    append_list(out, "édesség", ["édesített"])
                else:
                    append_list(out, "változat", [clean_text(value)])
            audit["feature_property_routed"] += 1
            continue

        prop_name = canonical_prop_name(raw_prop_name)
        prop_folded = fold_text(prop_name)
        values = values_of(raw_value)
        if not values:
            audit["empty_properties_removed"] += 1
            continue

        if prop_folded == "marka":
            old_brand = clean_text(values[0])
            if is_placeholder(old_brand) or fold_text(old_brand) in {"marka nelkul", "nincs marka"}:
                audit["placeholder_values_removed"] += 1
                continue
            fake_route = FAKE_WINE_BRAND_ROUTES.get(old_brand)
            if fake_route:
                append_list(out, "borvidék / eredet", fake_route[0])
                append_list(out, "szőlőfajta / borstílus", fake_route[1])
                append_list(out, "változat", fake_route[2])
                audit["fake_wine_brand_values_routed"] += 1
                continue
            new_brand = brand_map.get(old_brand, old_brand)
            out["márka"] = new_brand
            if new_brand != old_brand:
                audit["brand_values_atomicized"] += 1
                route_brand_variant(out, old_brand, new_brand, audit)
            continue

        kept_values = [value for value in values if not is_placeholder(value)]
        audit["placeholder_values_removed"] += len(values) - len(kept_values)
        if not kept_values:
            continue

        if prop_folded in {"iz", "alap", "osszetevo"}:
            atomic: list[str] = []
            for value in kept_values:
                if prop_folded == "iz" and fold_text(value) == "alkoholmentes":
                    audit["irrelevant_alcoholfree_removed_from_iz"] += 1
                    continue
                atomic.extend(atomize_flavor(value))
            merge_prop(out, prop_name, dedupe(atomic))
        elif prop_folded == "tartalom":
            atomic = []
            for value in kept_values:
                atomic.extend(normalize_content(value))
            merge_prop(out, prop_name, dedupe(atomic))
        elif prop_folded == "alkoholtartalom":
            normalized = [normalize_alcohol_atom(value) for value in kept_values]
            normalized = [value for value in normalized if value]
            if isinstance(raw_value, list):
                merge_prop(out, prop_name, dedupe(normalized))
            elif normalized:
                merge_prop(out, prop_name, normalized[0])
        elif isinstance(raw_value, list):
            atomic: list[str] = []
            for value in kept_values:
                atomic.extend(atomize_general_list_value(prop_name, value))
            merge_prop(out, prop_name, dedupe(atomic))
        elif isinstance(raw_value, bool):
            merge_prop(out, prop_name, raw_value)
        else:
            scalar = clean_text(kept_values[0])
            if prop_folded in {"fajta", "tipus", "forma", "alkohol"}:
                atomic = atomize_general_list_value(prop_name, scalar)
                merge_prop(out, prop_name, atomic if len(atomic) > 1 else atomic[0])
            else:
                merge_prop(out, prop_name, scalar)

    for prop_name, value in list(out.items()):
        if isinstance(value, list):
            value = sorted(dedupe(value), key=fold_text)
            if value:
                out[prop_name] = value
            else:
                del out[prop_name]
    return out


def convert_koch(product: dict[str, Any], audit: Counter[str]) -> None:
    old = product.get("tulajdonsagok") or {}
    pid = product_id(product)
    props: dict[str, Any] = {}
    if any(is_size_prop(key) for key in old):
        for key, value in old.items():
            if is_size_prop(key):
                props[key] = copy.deepcopy(value)
    props["márka"] = "Koch"
    props["feldolgozás"] = ["frissen préselt"]
    if pid == "588146:4125536":
        props["bio"] = True
    for prop_name in ("íz", "alap", "alapanyag"):
        if prop_name in old:
            target = "alap" if prop_name == "alapanyag" else prop_name
            for value in values_of(old[prop_name]):
                append_list(props, target, atomize_flavor(value))
    product["tulajdonsagok"] = props
    audit["koch_juice_properties_rebuilt"] += 1


def convert_child_party_drink(product: dict[str, Any], audit: Counter[str]) -> None:
    old = product.get("tulajdonsagok") or {}
    props: dict[str, Any] = {
        "márka": old.get("márka"),
        "szénsavasság": ["szénsavas"],
    }
    for key, value in old.items():
        if is_size_prop(key):
            props[key] = copy.deepcopy(value)
    flavors = values_of(old.get("íz"))
    if product_id(product) == "748902:4286292":
        flavors = ["erdei gyümölcs"]
    for flavor in flavors:
        append_list(props, "íz", atomize_flavor(flavor))
    name_fold = fold_text(product_name(product))
    if "cukorral es edesitoszerrel" in name_fold:
        props["édesítőszerrel"] = True
    product["tulajdonsagok"] = {key: value for key, value in props.items() if value is not None}
    audit["child_party_properties_rebuilt"] += 1


def convert_alcoholfree_sparkling(product: dict[str, Any], audit: Counter[str]) -> None:
    old = product.get("tulajdonsagok") or {}
    props: dict[str, Any] = {
        "márka": old.get("márka"),
        "alkoholtartalom": ["0,0%"],
        "típus": ["alkoholmentes habzó ital"],
    }
    for key in ("szín", "édesség", "íz"):
        kept = [value for value in values_of(old.get(key)) if not is_placeholder(value) and fold_text(value) != "alkoholmentes"]
        if kept:
            props[key] = kept
    for key, value in old.items():
        if is_size_prop(key):
            props[key] = copy.deepcopy(value)
    product["tulajdonsagok"] = {key: value for key, value in props.items() if value is not None}
    audit["alcoholfree_sparkling_properties_rebuilt"] += 1


def convert_alcoholfree_wine(product: dict[str, Any], audit: Counter[str]) -> None:
    props = product.get("tulajdonsagok") or {}
    props["alkoholtartalom"] = ["0,0%"]
    if fold_text(props.get("típus", "")) == "alkoholmentes bor" or builtins.any(
        fold_text(value) == "alkoholmentes bor" for value in values_of(props.get("típus"))
    ):
        props.pop("típus", None)
    product["tulajdonsagok"] = props
    audit["alcoholfree_wine_properties_fixed"] += 1


def apply_evidence_based_moves(
    products: list[dict[str, Any]],
    plant_review: dict[str, dict[str, Any]],
    issue_review: dict[str, dict[str, Any]],
    audit: Counter[str],
) -> None:
    by_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        by_id[product_id(product)].append(product)

    plant_candidates = [
        product
        for product in products
        if product.get("fokategoria") == DAIRY
        and product.get("alkategoria") == PLANT_ALK
        and product.get("altipus") == PLANT_DAIRY_ALT
    ]
    if len(plant_candidates) == 167:
        if set(product_id(product) for product in plant_candidates) != set(plant_review):
            raise RuntimeError("Plant review manifest does not match current candidates")
        for product in plant_candidates:
            pid = product_id(product)
            review = plant_review[pid]
            if pid in COCONUT_COOKING_IDS:
                if not review.get("image_path"):
                    raise RuntimeError(f"Cooking coconut product lacks image evidence: {pid}")
                product["altipus"] = PLANT_COOKING_ALT
                audit["plant_cooking_products_kept_in_dairy"] += 1
                continue
            correction = PLANT_BASE_CORRECTIONS.get(pid)
            if correction and not review.get("image_path"):
                raise RuntimeError(f"Image-based plant correction lacks image: {pid}")
            product["fokategoria"] = ITAL
            product["alkategoria"] = "Növényi ital"
            product["tulajdonsagok"] = normalize_plant_properties(product, correction, audit)
            product["altipus"] = plant_alt_for_base(product["tulajdonsagok"].get("alap"))
            audit["plant_drinks_moved_to_ital"] += 1
    elif len(plant_candidates) == 0:
        for pid in plant_review:
            matches = by_id.get(pid, [])
            if len(matches) != 1:
                raise RuntimeError(f"Already-applied plant product count mismatch: {pid}")
            product = matches[0]
            if pid in COCONUT_COOKING_IDS:
                expected = (DAIRY, PLANT_ALK, PLANT_COOKING_ALT)
                audit["plant_cooking_products_kept_in_dairy"] += 1
            else:
                expected = (ITAL, "Növényi ital", product.get("altipus"))
                audit["plant_drinks_moved_to_ital"] += 1
            actual = (product.get("fokategoria"), product.get("alkategoria"), product.get("altipus"))
            if actual != expected:
                raise RuntimeError(f"Already-applied plant path mismatch: {pid}: {actual}")
        audit["plant_migration_already_applied"] += 1
    else:
        raise RuntimeError(f"Expected 167 or 0 dairy plant candidates, got {len(plant_candidates)}")

    if audit["plant_drinks_moved_to_ital"] != 163:
        raise RuntimeError("Plant migration count differs from the image-reviewed decision")

    if not set(PATH_MOVES).issubset(issue_review):
        missing = sorted(set(PATH_MOVES) - set(issue_review))
        raise RuntimeError(f"Concrete issue review manifest missing IDs: {missing}")
    for pid, (alk, alt) in PATH_MOVES.items():
        matches = by_id.get(pid, [])
        if len(matches) != 1:
            raise RuntimeError(f"Expected one product for path move {pid}, got {len(matches)}")
        if not issue_review[pid].get("image_path"):
            raise RuntimeError(f"Path move lacks image evidence: {pid}")
        product = matches[0]
        if (product.get("fokategoria"), product.get("alkategoria"), product.get("altipus")) != (ITAL, alk, alt):
            product["fokategoria"] = ITAL
            product["alkategoria"] = alk
            product["altipus"] = alt
            if pid.startswith("5881"):
                convert_koch(product, audit)
            elif alt == "Gyerekital":
                convert_child_party_drink(product, audit)
            elif alt == "Alkoholmentes habzó ital":
                convert_alcoholfree_sparkling(product, audit)
            elif alt == "Alkoholmentes bor":
                convert_alcoholfree_wine(product, audit)
        audit["concrete_path_moves"] += 1

    wrong_1664 = [
        product
        for product in products
        if product.get("fokategoria") == ITAL
        and product_name(product).casefold().startswith("1664 blanc")
        and builtins.any(fold_text(value) == "alkoholmentes" for value in values_of((product.get("tulajdonsagok") or {}).get("sörtípus")))
    ]
    if len(wrong_1664) == 1:
        wrong_1664[0]["tulajdonsagok"].pop("sörtípus", None)
        audit["wrong_1664_beer_type_removed"] += 1
    elif wrong_1664:
        raise RuntimeError(f"Expected at most one wrong 1664 sörtípus, got {len(wrong_1664)}")

    for pid in MINI_SPIRIT_IDS:
        matches = by_id.get(pid, [])
        if len(matches) != 1 or not issue_review.get(pid, {}).get("image_path"):
            raise RuntimeError(f"Mini spirit evidence mismatch: {pid}")
        matches[0]["tulajdonsagok"]["alkoholtartalom"] = ["34%"]
        audit["mini_spirit_alcohol_fixed"] += 1

    for pid in TATRATEA_SET_IDS:
        matches = by_id.get(pid, [])
        if len(matches) != 1 or not issue_review.get(pid, {}).get("image_path"):
            raise RuntimeError(f"Tatratea set evidence mismatch: {pid}")
        matches[0]["tulajdonsagok"]["alkoholtartalom"] = ["22%", "32%", "42%", "52%", "62%", "72%"]
        audit["tatratea_set_alcohol_fixed"] += 1

    homola = by_id.get(HOMOLA_ID, [])
    if len(homola) != 1 or not issue_review.get(HOMOLA_ID, {}).get("image_path"):
        raise RuntimeError("Homola evidence mismatch")
    homola[0]["tulajdonsagok"]["alkoholtartalom"] = ["13%"]
    audit["homola_alcohol_fixed"] += 1


def remove_copied_altipus_values(products: list[dict[str, Any]], audit: Counter[str]) -> None:
    for product in products:
        if (
            product.get("fokategoria") == ITAL
            and product.get("alkategoria") in COPIED_ALT_ALKS
            and product.get("altipus") == product.get("alkategoria")
        ):
            product["altipus"] = ""
            audit["copied_altipus_removed"] += 1


def normalize_all_ital_products(
    products: list[dict[str, Any]],
    brand_map: dict[str, str],
    audit: Counter[str],
) -> None:
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        before = product.get("tulajdonsagok") or {}
        after = normalize_ital_properties(product, brand_map, audit)
        if before != after:
            audit["ital_products_normalized"] += 1
        product["tulajdonsagok"] = after


def canonicalize_atomic_values(products: list[dict[str, Any]], audit: Counter[str]) -> None:
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        props = product.get("tulajdonsagok") or {}
        for prop_name, raw_value in list(props.items()):
            if is_size_prop(prop_name):
                continue
            prop_folded = fold_text(prop_name)
            if isinstance(raw_value, list):
                normalized = [
                    ATOMIC_VALUE_CANONICAL.get((prop_folded, fold_text(value)), value)
                    for value in raw_value
                ]
                normalized = dedupe(normalized)
                if normalized != raw_value:
                    props[prop_name] = normalized
                    audit["atomic_value_spellings_canonicalized"] += 1
            elif not isinstance(raw_value, bool):
                normalized = ATOMIC_VALUE_CANONICAL.get((prop_folded, fold_text(raw_value)), raw_value)
                if normalized != raw_value:
                    props[prop_name] = normalized
                    audit["atomic_value_spellings_canonicalized"] += 1


def remove_all_false_path_flags(products: list[dict[str, Any]], audit: Counter[str]) -> None:
    values: dict[tuple[str, str, str], list[bool]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        for prop_name, value in (product.get("tulajdonsagok") or {}).items():
            if isinstance(value, bool):
                values[(path[0], path[1], prop_name)].append(value)
    removable = {key for key, flags in values.items() if flags and not builtins.any(flags)}
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        props = product.get("tulajdonsagok") or {}
        for prop_name in list(props):
            if (path[0], path[1], prop_name) in removable:
                del props[prop_name]
                audit["all_false_values_removed"] += 1
    audit["all_false_path_properties_removed"] = len(removable)


def convert_value_shape(value: Any, target: str) -> Any:
    if target == "flag":
        if isinstance(value, bool):
            return value
        return builtins.any(bool(item) for item in values_of(value))
    if target == "multi":
        return dedupe(values_of(value))
    if isinstance(value, list):
        if len(value) > 1:
            raise ValueError("Cannot losslessly convert a multi-value list to scalar")
        return value[0] if value else ""
    return value


def choose_shape(entries: list[Any], prop_name: str) -> str:
    shapes = Counter(shape_of(value) for value in entries)
    if len(shapes) == 1:
        return next(iter(shapes))
    if prop_name in BOOL_PROPS and set(shapes) <= {"flag", "single", "multi"}:
        return "flag"
    has_real_multi = builtins.any(isinstance(value, list) and len(value) > 1 for value in entries)
    if has_real_multi:
        return "multi"
    return "single" if shapes["single"] >= shapes["multi"] else "multi"


def align_shapes_within_paths(products: list[dict[str, Any]], audit: Counter[str]) -> None:
    groups: dict[tuple[str, str, str], list[tuple[dict[str, Any], Any]]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        for prop_name, value in (product.get("tulajdonsagok") or {}).items():
            groups[(path[0], path[1], prop_name)].append((product, value))
    for (_alk, _alt, prop_name), entries in groups.items():
        shapes = {shape_of(value) for _product, value in entries}
        if len(shapes) <= 1:
            continue
        if is_size_prop(prop_name):
            audit["size_shape_mismatches_intentionally_skipped"] += 1
            continue
        target = choose_shape([value for _product, value in entries], prop_name)
        for product, value in entries:
            if shape_of(value) != target:
                product["tulajdonsagok"][prop_name] = convert_value_shape(value, target)
                audit["product_shapes_aligned_within_path"] += 1


def align_child_shapes_with_direct_parent(products: list[dict[str, Any]], audit: Counter[str]) -> None:
    by_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") == ITAL:
            by_path[(str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))].append(product)
    for (alk, alt), child_products in list(by_path.items()):
        if not alt or (alk, "") not in by_path:
            continue
        direct_products = by_path[(alk, "")]
        parent_values: dict[str, list[Any]] = defaultdict(list)
        for product in direct_products:
            for prop_name, value in product["tulajdonsagok"].items():
                parent_values[prop_name].append(value)
        parent_shapes = {prop: choose_shape(values, prop) for prop, values in parent_values.items()}
        for product in child_products:
            for prop_name, value in list(product["tulajdonsagok"].items()):
                target = parent_shapes.get(prop_name)
                if not target or shape_of(value) == target:
                    continue
                if is_size_prop(prop_name):
                    audit["size_parent_child_shape_mismatches_intentionally_skipped"] += 1
                    continue
                product["tulajdonsagok"][prop_name] = convert_value_shape(value, target)
                audit["child_shapes_aligned_with_parent"] += 1


def build_prop_block(
    products: list[dict[str, Any]],
    excluded_props: set[str] | None = None,
    allowed_value_products: list[dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    excluded_props = excluded_props or set()
    values_by_prop: dict[str, list[Any]] = defaultdict(list)
    raw_by_prop: dict[str, list[Any]] = defaultdict(list)
    for product in products:
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            if prop_name in excluded_props:
                continue
            raw_by_prop[prop_name].append(raw_value)
    allowed_names = set(raw_by_prop)
    for product in allowed_value_products or products:
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            if prop_name in allowed_names:
                values_by_prop[prop_name].extend(values_of(raw_value))
    block: dict[str, dict[str, Any]] = {"egyedi": {}, "csoportos": {}}
    for prop_name in sorted(raw_by_prop, key=fold_text):
        target_shape = choose_shape(raw_by_prop[prop_name], prop_name)
        allowed = sorted(dedupe(values_by_prop[prop_name]), key=fold_text)
        if target_shape == "flag":
            block["egyedi"][prop_name] = {}
        elif target_shape == "single":
            block["egyedi"][prop_name] = allowed
        else:
            block["csoportos"][prop_name] = allowed
    return block


def rebuild_ital_category(categories: dict[str, Any], products: list[dict[str, Any]]) -> None:
    old_ital = categories[ITAL]
    old_alks = folded_get(old_ital, "alkategoriak", {}) or {}
    old_alk_order = list(old_alks)
    ital_products = [product for product in products if product.get("fokategoria") == ITAL]
    by_alk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in ital_products:
        alk = str(product.get("alkategoria") or "")
        alt = str(product.get("altipus") or "")
        by_alk[alk].append(product)
        by_path[(alk, alt)].append(product)

    alk_order = [alk for alk in old_alk_order if alk in by_alk]
    alk_order.extend(sorted((alk for alk in by_alk if alk not in alk_order), key=fold_text))
    new_alks: dict[str, Any] = {}
    for alk in alk_order:
        old_node = old_alks.get(alk, {})
        old_alts = folded_get(old_node, "altipusok", {}) or {}
        named_alts = {alt for (path_alk, alt) in by_path if path_alk == alk and alt}
        alt_order = [alt for alt in old_alts if alt in named_alts]
        alt_order.extend(sorted((alt for alt in named_alts if alt not in alt_order), key=fold_text))
        direct_products = by_path.get((alk, ""), [])
        parent_block = build_prop_block(direct_products, allowed_value_products=by_alk[alk])
        parent_props = set(parent_block["egyedi"]) | set(parent_block["csoportos"])
        node: dict[str, Any] = {
            PROP_KEY: parent_block,
            ALT_KEY: {},
        }
        for alt in alt_order:
            node[ALT_KEY][alt] = {
                PROP_KEY: build_prop_block(by_path[(alk, alt)], excluded_props=parent_props)
            }
        new_alks[alk] = node
    categories[ITAL] = {
        PROP_KEY: {"egyedi": {}, "csoportos": {}},
        ALK_KEY: new_alks,
    }


def prune_empty_dairy_plant_alt(categories: dict[str, Any], products: list[dict[str, Any]], audit: Counter[str]) -> None:
    remaining = [
        product
        for product in products
        if product.get("fokategoria") == DAIRY
        and product.get("alkategoria") == PLANT_ALK
        and product.get("altipus") == PLANT_DAIRY_ALT
    ]
    if remaining:
        raise RuntimeError(f"Dairy plant drink path still has {len(remaining)} products")
    dairy = categories[DAIRY]
    plant_node = folded_get(folded_get(dairy, "alkategoriak", {}), PLANT_ALK)
    alts = folded_get(plant_node, "altipusok", {})
    if PLANT_DAIRY_ALT in alts:
        del alts[PLANT_DAIRY_ALT]
        audit["empty_dairy_plant_alt_removed"] += 1
    else:
        audit["empty_dairy_plant_alt_already_removed"] += 1


def refresh_hashes(
    products: list[dict[str, Any]],
    original_state: dict[int, dict[str, Any]],
    audit: Counter[str],
) -> None:
    for index, product in enumerate(products):
        if is_de_karavan(product):
            audit["de_karavan_hash_refresh_skipped"] += 1
            continue
        current_state = {
            "fokategoria": product.get("fokategoria"),
            "alkategoria": product.get("alkategoria"),
            "altipus": product.get("altipus"),
            "tulajdonsagok": product.get("tulajdonsagok") or {},
        }
        if current_state == original_state[index]:
            continue
        new_hash = category_hash(product)
        if product.get("kategoria_hash") != new_hash:
            product["kategoria_hash"] = new_hash
            audit["category_hashes_refreshed"] += 1


def node_prop_shapes(node: dict[str, Any]) -> dict[str, str]:
    props = folded_get(node, "tulajdonsagok", {}) or {}
    result: dict[str, str] = {}
    for prop_name, declaration in (folded_get(props, "egyedi", {}) or {}).items():
        result[prop_name] = "flag" if isinstance(declaration, dict) else "single"
    for prop_name in (folded_get(props, "csoportos", {}) or {}):
        result[prop_name] = "multi"
    return result


def effective_declarations(
    categories: dict[str, Any],
    alk: str,
    alt: str,
) -> tuple[dict[str, str], dict[str, Any], list[str]]:
    root = categories[ITAL]
    alks = folded_get(root, "alkategoriak", {}) or {}
    alk_node = alks.get(alk)
    if not isinstance(alk_node, dict):
        return {}, {}, [f"missing alkategoria: {alk}"]
    nodes = [root, alk_node]
    errors: list[str] = []
    if alt:
        alt_node = (folded_get(alk_node, "altipusok", {}) or {}).get(alt)
        if not isinstance(alt_node, dict):
            return {}, {}, [f"missing altipus: {alk} > {alt}"]
        nodes.append(alt_node)
    shapes: dict[str, str] = {}
    declarations: dict[str, Any] = {}
    seen: Counter[str] = Counter()
    for node in nodes:
        local_shapes = node_prop_shapes(node)
        props = folded_get(node, "tulajdonsagok", {}) or {}
        for prop_name, shape in local_shapes.items():
            seen[prop_name] += 1
            shapes[prop_name] = shape
            group = "csoportos" if shape == "multi" else "egyedi"
            declarations[prop_name] = (folded_get(props, group, {}) or {}).get(prop_name)
    for prop_name, count in seen.items():
        if count > 1:
            errors.append(f"redefined: {alk} > {alt} :: {prop_name}")
    return shapes, declarations, errors


def list_compound_suspects(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    suspects: Counter[tuple[str, str]] = Counter()
    excluded = {"alkoholtartalom", "borvidék / eredet", "márka"}
    exact_allowlist = {"Snack&Shake"}
    for product in products:
        if product.get("fokategoria") != ITAL:
            continue
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            if prop_name in excluded or is_size_prop(prop_name):
                continue
            for value in values_of(raw_value):
                text = str(value)
                if text in exact_allowlist:
                    continue
                if re.search(r"[/,+&]|\bés\b", text, flags=re.IGNORECASE):
                    suspects[(prop_name, text)] += 1
                elif fold_text(prop_name) in {"iz", "alap", "osszetevo", "szolofajta borstilus"} and "-" in text:
                    suspects[(prop_name, text)] += 1
    return [
        {"property": prop, "value": value, "count": count}
        for (prop, value), count in suspects.most_common(200)
    ]


def validate(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
    size_snapshot: dict[int, dict[str, Any]],
    de_karavan_snapshot: list[dict[str, Any]],
    plant_review: dict[str, dict[str, Any]],
    issue_review: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    ital_products = [product for product in products if product.get("fokategoria") == ITAL]
    path_counts = Counter((str(p.get("alkategoria") or ""), str(p.get("altipus") or "")) for p in ital_products)
    missing_paths: list[str] = []
    redefinitions: set[str] = set()
    product_only: Counter[str] = Counter()
    type_mismatches: list[dict[str, Any]] = []
    skipped_size_type_mismatches: list[dict[str, Any]] = []
    missing_allowed_values: list[dict[str, Any]] = []
    placeholder_non_size: Counter[str] = Counter()
    placeholder_size: Counter[str] = Counter()
    five_one_props: Counter[str] = Counter()
    wrong_alcoholfree_placements: Counter[str] = Counter()
    brand_values: Counter[str] = Counter()
    declaration_cache: dict[tuple[str, str], tuple[dict[str, str], dict[str, Any]]] = {}

    for product in ital_products:
        path = (str(product.get("alkategoria") or ""), str(product.get("altipus") or ""))
        if path not in declaration_cache:
            shapes, declarations, errors = effective_declarations(categories, *path)
            if errors and builtins.any(error.startswith("missing") for error in errors):
                missing_paths.extend(errors)
            redefinitions.update(error for error in errors if error.startswith("redefined"))
            declaration_cache[path] = (shapes, declarations)
        shapes, declarations = declaration_cache[path]
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            folded_prop = fold_text(prop_name)
            if folded_prop in {"termekcsalad", "funkcio", "minosites"}:
                five_one_props[prop_name] += 1
            if folded_prop in {"termekcsalad", "feldolgozas", "funkcio", "minosites", "iz", "sortipus"}:
                for value in values_of(raw_value):
                    if fold_text(value) == "alkoholmentes":
                        wrong_alcoholfree_placements[prop_name] += 1
            for value in values_of(raw_value):
                if is_placeholder(value):
                    (placeholder_size if is_size_prop(prop_name) else placeholder_non_size)[prop_name] += 1
            expected = shapes.get(prop_name)
            if not expected:
                product_only[prop_name] += 1
                continue
            actual = shape_of(raw_value)
            if actual != expected:
                row = {
                    "path": [*path],
                    "property": prop_name,
                    "expected": expected,
                    "actual": actual,
                    "product_id": product_id(product),
                }
                if is_size_prop(prop_name):
                    skipped_size_type_mismatches.append(row)
                else:
                    type_mismatches.append(row)
            declaration = declarations.get(prop_name)
            if isinstance(declaration, list):
                allowed = {fold_text(value) for value in declaration}
                for value in values_of(raw_value):
                    if fold_text(value) not in allowed:
                        missing_allowed_values.append(
                            {"path": [*path], "property": prop_name, "value": value, "product_id": product_id(product)}
                        )
            if folded_prop == "marka":
                brand_values[str(raw_value)] += 1

    size_changes = []
    for index, product in enumerate(products):
        current = {
            key: value
            for key, value in (product.get("tulajdonsagok") or {}).items()
            if is_size_prop(key)
        }
        if current != size_snapshot[index]:
            size_changes.append({"index": index, "id": product_id(product), "before": size_snapshot[index], "after": current})

    current_de_karavan = [
        copy.deepcopy(product)
        for product in products
        if is_de_karavan(product)
    ]
    energy_shapes = {}
    for alt in ("Gyerekital", "Limonádé"):
        shapes, _decl, errors = effective_declarations(categories, "Üdítőital", alt)
        energy_shapes[alt] = {"shape": shapes.get("energia tartalom"), "errors": errors}

    copied_alt_counts = {
        alk: path_counts.get((alk, alk), 0)
        for alk in sorted(COPIED_ALT_ALKS, key=fold_text)
    }
    dairy_plant = sum(
        1
        for product in products
        if product.get("fokategoria") == DAIRY
        and product.get("alkategoria") == PLANT_ALK
        and product.get("altipus") == PLANT_DAIRY_ALT
    )
    dairy_cooking = sum(
        1
        for product in products
        if product.get("fokategoria") == DAIRY
        and product.get("alkategoria") == PLANT_ALK
        and product.get("altipus") == PLANT_COOKING_ALT
    )
    declared_named_paths: set[tuple[str, str]] = set()
    ital_alks = folded_get(categories[ITAL], "alkategoriak", {}) or {}
    for alk, alk_node in ital_alks.items():
        for alt in (folded_get(alk_node, "altipusok", {}) or {}):
            declared_named_paths.add((alk, alt))
    used_named_paths = {path for path in path_counts if path[1]}
    concrete_paths = {
        pid: [matches[0].get("alkategoria"), matches[0].get("altipus")]
        for pid in PATH_MOVES
        if len(matches := [p for p in products if product_id(p) == pid]) == 1
    }
    wrong_1664_left = sum(
        1
        for product in ital_products
        if product_name(product).casefold().startswith("1664 blanc")
        and builtins.any(fold_text(value) == "alkoholmentes" for value in values_of((product.get("tulajdonsagok") or {}).get("sörtípus")))
    )
    alcohol_checks = {
        pid: (next((p for p in products if product_id(p) == pid), {}).get("tulajdonsagok") or {}).get("alkoholtartalom")
        for pid in sorted(MINI_SPIRIT_IDS | TATRATEA_SET_IDS | {HOMOLA_ID})
    }
    family_variants: dict[str, int] = {}
    family_exact = {value.casefold() for value in BRAND_FAMILY_PREFIXES}
    for brand, count in brand_values.items():
        if brand in BRAND_FAMILY_EXCLUSIONS or brand.casefold() in family_exact:
            continue
        if builtins.any(brand.casefold().startswith(family.casefold() + " ") for family in BRAND_FAMILY_PREFIXES):
            family_variants[brand] = count
    fake_wine_brands_left = {
        brand: count for brand, count in brand_values.items() if brand in FAKE_WINE_BRAND_ROUTES
    }
    brand_placeholders_left = {
        brand: count
        for brand, count in brand_values.items()
        if fold_text(brand) in {"marka nelkul", "nincs marka"}
    }
    return {
        "total_products": len(products),
        "ital_products": len(ital_products),
        "ital_paths": len(path_counts),
        "dairy_plant_drinks_left": dairy_plant,
        "dairy_plant_cooking_products": dairy_cooking,
        "missing_paths": sorted(set(missing_paths)),
        "declared_unused_paths": [
            [alk, alt]
            for alk, alt in sorted(declared_named_paths - used_named_paths, key=lambda row: (fold_text(row[0]), fold_text(row[1])))
        ],
        "property_redefinitions": sorted(redefinitions),
        "product_only_properties": dict(product_only),
        "type_mismatches_non_size": type_mismatches,
        "type_mismatches_size_skipped": skipped_size_type_mismatches,
        "missing_allowed_values": missing_allowed_values,
        "placeholder_non_size": dict(placeholder_non_size),
        "placeholder_size_skipped": dict(placeholder_size),
        "five_one_properties_left": dict(five_one_props),
        "wrong_alcoholfree_placements": dict(wrong_alcoholfree_placements),
        "energy_content_shapes": energy_shapes,
        "copied_altipus_counts": copied_alt_counts,
        "concrete_paths": concrete_paths,
        "wrong_1664_left": wrong_1664_left,
        "alcohol_property_checks": alcohol_checks,
        "size_property_changes": size_changes,
        "de_karavan_records": len(current_de_karavan),
        "de_karavan_unchanged": current_de_karavan == de_karavan_snapshot,
        "compound_value_suspects": list_compound_suspects(products),
        "brand_unique": len(brand_values),
        "brand_user_examples_left": {
            brand: count
            for brand, count in brand_values.items()
            if brand in {"Royal Boldog Névnapot!", "Royal Boldog Születésnapot!"}
        },
        "brand_family_variants_left": family_variants,
        "fake_wine_brands_left": fake_wine_brands_left,
        "brand_placeholders_left": brand_placeholders_left,
        "review_evidence": {
            "plant_products": len(plant_review),
            "plant_with_image": sum(bool(row.get("image_path")) for row in plant_review.values()),
            "concrete_products": len(issue_review),
            "concrete_with_image": sum(bool(row.get("image_path")) for row in issue_review.values()),
        },
    }


def validation_errors(validation: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    exact_empty_keys = [
        "missing_paths",
        "declared_unused_paths",
        "property_redefinitions",
        "product_only_properties",
        "type_mismatches_non_size",
        "missing_allowed_values",
        "placeholder_non_size",
        "five_one_properties_left",
        "wrong_alcoholfree_placements",
        "size_property_changes",
        "compound_value_suspects",
        "brand_user_examples_left",
        "brand_family_variants_left",
        "fake_wine_brands_left",
        "brand_placeholders_left",
    ]
    for key in exact_empty_keys:
        if validation.get(key):
            errors.append(key)
    if validation["total_products"] != 47030:
        errors.append("total_product_count")
    if validation["ital_products"] != 12876:
        errors.append("ital_product_count")
    if validation["dairy_plant_drinks_left"] != 0:
        errors.append("dairy_plant_drinks_left")
    if validation["dairy_plant_cooking_products"] != 80:
        errors.append("dairy_plant_cooking_count")
    if validation["de_karavan_records"] != 1:
        errors.append("de_karavan_record_count")
    if not validation["de_karavan_unchanged"]:
        errors.append("de_karavan_changed")
    if validation["wrong_1664_left"]:
        errors.append("wrong_1664_left")
    if builtins.any(validation["copied_altipus_counts"].values()):
        errors.append("copied_altipus_counts")
    for alt, row in validation["energy_content_shapes"].items():
        if row.get("shape") not in {None, "single"} or row.get("errors"):
            errors.append(f"energy_shape::{alt}")
    expected_alcohol = {
        "566017": ["34%"],
        "1014576": ["34%"],
        "1055675": ["34%"],
        "442852:3980236": ["22%", "32%", "42%", "52%", "62%", "72%"],
        "BTY-X9705200320021": ["22%", "32%", "42%", "52%", "62%", "72%"],
        HOMOLA_ID: ["13%"],
    }
    if validation["alcohol_property_checks"] != expected_alcohol:
        errors.append("alcohol_property_checks")
    expected_paths = {pid: [alk, alt] for pid, (alk, alt) in PATH_MOVES.items()}
    if validation["concrete_paths"] != expected_paths:
        errors.append("concrete_paths")
    evidence = validation["review_evidence"]
    if evidence != {
        "plant_products": 167,
        "plant_with_image": 160,
        "concrete_products": 27,
        "concrete_with_image": 27,
    }:
        errors.append("review_evidence")
    return errors


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [str(value).replace("\n", " ").replace("|", "\\|") for value in row]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def write_report(payload: dict[str, Any]) -> None:
    operations = payload["operations"]
    validation = payload["validation"]
    final_check = load_json(FINAL_CHECK_PATH) if FINAL_CHECK_PATH.is_file() else {}
    lines = [
        "# Ital kategória javítása – 2026-07-16",
        "",
        f"- Futás: {payload['meta']['generated_at']}",
        f"- Termékek összesen: {validation['total_products']}",
        f"- Ital termékek javítás után: {validation['ital_products']}",
        f"- Használt Ital útvonalak: {validation['ital_paths']}",
        "- A kiszerelés nevű terméktulajdonságok értéke és alakja változatlan maradt.",
        "",
        "## Bizonyíték és kategóriamozgatások",
        "",
        f"- A tejág 167 `Növényi ital` termékéből 160-hoz volt helyi kép. 163 valódi ital az Ital ágba került.",
        "- A kép nélküli hét terméknél csak a bolti strukturált adatot használtuk; képből származó tulajdonság-korrekció nem történt.",
        f"- Négy, képen is főzési alapanyagnak látszó kókusztej a tejág `Növényi főzőkrém / tejszín` altípusába került.",
        f"- A 27 konkrét 4.x jelölt mindegyikéhez sikerült helyi képet visszakeresni.",
        f"- Konkrét kategóriamozgatások: {operations.get('concrete_path_moves', 0)}.",
        "- A forrásban `D.E.KARAVÁN VAC. 225G` néven szereplő rekordot a program teljesen változatlanul hagyta.",
        "",
        "## 5.1 és 5.2 felülvizsgálata",
        "",
        "- A `termékcsalád`, `funkció` és `minősítés` mezők jelentést hordozó értékei célzott tulajdonságba kerültek; a mezők nem maradtak meg zajos gyűjtőként.",
        "- A `feldolgozás` megmaradt, ahol valódi eljárást jelöl (például frissen/hidegen préselt, fermentált, fagyasztva szárított).",
        "- A nem méretjellegű `nem jelölt` és más technikai placeholder értékek törlődtek. Ez nem állít új termékadatot: az ismeretlen érték helyén egyszerűen nincs termékérték.",
        "- A 100%-ban hamis logikai tulajdonságok útvonalanként törlődtek; a ritka, de legalább egy igaz értékkel rendelkező jelzők megmaradtak.",
        "",
        "## Szerkezet és elemi értékek",
        "",
        f"- Elemivé tett márkaértékek: {FULL_OPERATION_SUMMARY['Márkaérték elemivé téve']} termékérték-előfordulás.",
        f"- Eltávolított, az alkategóriával azonos altípus: {FULL_OPERATION_SUMMARY['Az alkategóriával azonos altípus törölve']} termék.",
        "- A fa az aktuális termékértékekből épült újra; az öröklési útvonalakon nincs tulajdonság-felüldefiniálás.",
        "- A `Gyerekital` és `Limonádé` `energia tartalom` mezője egyértékű felsorolás, nem logikai flag.",
        "- Az íz-, alap-, összetevő- és más csoportos összetett értékek elemi listává váltak; a `Royal Boldog Névnapot!` márka például `Royal`, a névnapi jelleg pedig `változat`.",
        "",
        "## Fő műveleti számlálók",
        "",
    ]
    operation_rows = [[key, value] for key, value in FULL_OPERATION_SUMMARY.items()]
    lines.extend(markdown_table(["Művelet", "Darab"], operation_rows))
    lines.extend(
        [
            "",
            "## Végellenőrzés",
            "",
            f"- Hiányzó útvonal: {len(validation['missing_paths'])}",
            f"- Nem használt deklarált útvonal: {len(validation['declared_unused_paths'])}",
            f"- Tulajdonság-felüldefiniálás: {len(validation['property_redefinitions'])}",
            f"- Termékben van, fában nincs tulajdonság: {sum(validation['product_only_properties'].values())}",
            f"- Nem méretjellegű típushiba: {len(validation['type_mismatches_non_size'])}",
            f"- Nem deklarált érték: {len(validation['missing_allowed_values'])}",
            f"- Nem méretjellegű placeholder: {sum(validation['placeholder_non_size'].values())}",
            f"- Maradék összetettérték-gyanú: {len(validation['compound_value_suspects'])}",
            f"- Módosult kiszerelés-tulajdonság: {len(validation['size_property_changes'])}",
            f"- Tudatosan kihagyott, már korábban is létező vagy a mozgatásból adódó kiszerelés-alak eltérés: {len(validation['type_mismatches_size_skipped'])}",
            f"- Független ellenőrző állapota: `{final_check.get('status', 'még nem futott')}`; hibák: {len(final_check.get('failures', {}))}",
            "",
            "## Képi munkafájlok",
            "",
            f"- Növényi ital jegyzék: `{PLANT_REVIEW.relative_to(BASE)}`",
            f"- Konkrét hibák jegyzéke: `{ISSUE_REVIEW.relative_to(BASE)}`",
            f"- Kontaktlapok: `{REVIEW_DIR.relative_to(BASE)}`",
            "",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="A két fő JSON-fájl visszaírása")
    args = parser.parse_args()

    required = [
        RESULT_PATH,
        CATEGORY_PATH,
        PLANT_REVIEW,
        ISSUE_REVIEW,
        BRAND_ROUND5,
        BRAND_ROUND12,
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise RuntimeError(f"Missing required files: {missing}")

    generated_at = datetime.now().isoformat(timespec="seconds")
    products = load_json(RESULT_PATH)
    categories = load_json(CATEGORY_PATH)
    if not isinstance(products, list) or len(products) != 47030:
        raise RuntimeError("Unexpected eredmeny.json product collection")
    if ITAL not in categories or DAIRY not in categories:
        raise RuntimeError("Required category roots are missing")

    size_snapshot = preserve_size_snapshot(products)
    category_state_snapshot = preserve_category_state(products)
    de_karavan_snapshot = [
        copy.deepcopy(product)
        for product in products
        if is_de_karavan(product)
    ]
    plant_review, issue_review = load_review()
    brand_map = load_brand_map()
    operations: Counter[str] = Counter()

    apply_evidence_based_moves(products, plant_review, issue_review, operations)
    extend_brand_map_from_products(brand_map, products)
    remove_copied_altipus_values(products, operations)
    normalize_all_ital_products(products, brand_map, operations)
    canonicalize_atomic_values(products, operations)
    remove_all_false_path_flags(products, operations)
    align_shapes_within_paths(products, operations)
    align_child_shapes_with_direct_parent(products, operations)
    rebuild_ital_category(categories, products)
    prune_empty_dairy_plant_alt(categories, products, operations)
    refresh_hashes(products, category_state_snapshot, operations)

    validation = validate(
        products,
        categories,
        size_snapshot,
        de_karavan_snapshot,
        plant_review,
        issue_review,
    )
    errors = validation_errors(validation)
    payload = {
        "meta": {
            "generated_at": generated_at,
            "mode": "apply" if args.apply else "dry-run",
            "products_file": RESULT_PATH.name,
            "categories_file": CATEGORY_PATH.name,
            "report_file": REPORT_PATH.name,
        },
        "operations": dict(operations),
        "validation": validation,
        "hard_errors": errors,
    }
    dump_json(DRY_AUDIT_PATH if not args.apply else AUDIT_PATH, payload)
    if errors:
        print(json.dumps({"mode": payload["meta"]["mode"], "hard_errors": errors}, ensure_ascii=False, indent=2))
        raise RuntimeError(f"Validation failed: {errors}")

    if args.apply:
        write_main_files_transactionally(products, categories)
        write_report(payload)

    print(
        json.dumps(
            {
                "mode": payload["meta"]["mode"],
                "hard_errors": [],
                "ital_products": validation["ital_products"],
                "plant_moved": operations["plant_drinks_moved_to_ital"],
                "concrete_path_moves": operations["concrete_path_moves"],
                "normalized_products": operations["ital_products_normalized"],
                "report": str(REPORT_PATH) if args.apply else None,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
