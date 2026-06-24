from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
CATEGORY_PATH = BASE_DIR / "kategoriak_2026-06-13.json"
PRODUCT_PATH = BASE_DIR / "eredmeny.json"
OUT_DIR = BASE_DIR / "tejtermekek_munkafajlok"
TARGET_CATEGORY_FOLDED = "tejtermekek es tojas"
OLD_FERMENTED_ALK_FOLDED = "ivojoghurt, kefir, iro"
NEW_FERMENTED_ALK = "Ivójoghurt, kefir, író, aludttej"

REMOVED_PROP_FOLDS = {
    "alapanyag",
    "cukormentes",
    "dieta",
    "elofloras",
    "feherje",
    "friss",
    "novenyi_alap",
    "mentes",
    "mentesseg",
    "minosites",
    "novenyi alapu",
    "sajtfajta",
    "sajt tipusa",
    "tejtipus",
    "tej tipusa",
    "turo tipusa",
    "tartasi mod",
    "hozzaadott anyag",
    "hozzaadott vitamin / asvanyi anyag",
    "kiszereles_mennyiseg",
    "iz / jelleg",
    "valtozat",
    "zsirszegeny",
    "zsirtartalom / jelleg",
}

SAJT_FORMA_DROP = {
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
    "viaszbevonatban",
}

SAJT_FORMA_MAP = {
    "cikk": ["körcikk"],
    "cikkelyes": ["körcikk"],
    "dobozos": ["doboz"],
    "gomboc": ["golyó"],
    "kenheto adag": ["kenhető"],
    "kenheto/golyo": ["kenhető", "golyó"],
    "kenheto krem": ["kenhető"],
    "kenheto sajtkrem": ["kenhető"],
    "korcikkelyes": ["körcikk"],
    "mini golyo": ["golyó", "mini"],
    "mini mozzarella": ["mini"],
    "sajttekercs": ["tekercs"],
    "stick": ["rúd"],
    "tegelyes": ["tégely"],
    "tomlos": ["tubus"],
}

FAJTA_MAP = {
    "bergkase": "bergkäse",
    "cheddar": "cheddar",
    "edam": "edami",
    "emmental": "ementáli",
    "emmentaler": "ementáli",
    "emental": "ementáli",
    "ementali tipusu": "ementáli",
    "feta jellegu": "krémfehér",
    "gouda": "gouda",
    "grana padano": "grana padano",
    "kek sajt": "kék sajt",
    "keksajt": "kék sajt",
    "kremfeher sajt": "krémfehér",
    "kremfehersajt": "krémfehér",
    "kremsajt": "krémsajt",
    "maasdammer": "maasdam",
    "maasdamer": "maasdam",
    "marvanysajt": "kék sajt",
    "parmezan": "parmigiano reggiano",
    "parmigiano reggiano": "parmigiano reggiano",
    "trappista": "trappista",
}

FAJTA_DROP = {
    "egyeb",
    "finesse original",
    "grillsajt",
    "kemeny sajt",
    "original",
    "reszelt sajt",
    "sajt",
    "sajtos szendvicskrem",
    "sajtkrem",
    "szendvicskrem",
}

SAJT_JELLEG_DROP = {
    "afonyaszosszal",
    "bazsalikomos",
    "classic",
    "dan",
    "erdei gombas",
    "fokhagymas",
    "francia sajtkulonlegesseg",
    "fuszerkeverekkel",
    "fuszerekkel",
    "fuszernovenyekkel",
    "ir",
    "klasszikus",
    "kremsajtos",
    "laktozmentes",
    "light",
    "mango chutney szosszal",
    "mini",
    "napraforgo olajban",
    "nincs kep",
    "olaszfuszeres",
    "piccante",
    "provanszi",
    "sajthelyettesito",
    "snidlinges",
    "vaghato",
    "viaszbevonatban",
    "zoldborsos",
    "zoldfuszeres",
    "zsirdus",
    "zsiros",
    "zsirszegeny",
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
    tmp_path = path.with_name(f"{path.name}.tmp")
    with tmp_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    with tmp_path.open("r", encoding="utf-8") as handle:
        json.load(handle)
    tmp_path.replace(path)


def folded_key(mapping: dict[str, Any], folded_name: str) -> str | None:
    for key in mapping:
        if fold_text(key) == folded_name:
            return key
    return None


def require_key(mapping: dict[str, Any], folded_name: str) -> str:
    key = folded_key(mapping, folded_name)
    if key is None:
        raise KeyError(f"Missing key: {folded_name}")
    return key


def folded_get(mapping: dict[str, Any], folded_name: str, default: Any = None) -> Any:
    key = folded_key(mapping, folded_name)
    if key is None:
        return default
    return mapping[key]


def pop_by_fold(mapping: dict[str, Any], folded_name: str) -> Any:
    key = folded_key(mapping, folded_name)
    if key is None:
        return None
    return mapping.pop(key)


def values_of(value: Any) -> list[Any]:
    if value in (None, "", [], {}):
        return []
    return value if isinstance(value, list) else [value]


def unique_values(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value in (None, "", [], {}):
            continue
        folded = fold_text(value)
        if folded not in seen:
            result.append(value)
            seen.add(folded)
    return result


def set_values(props: dict[str, Any], key: str, values: list[Any]) -> None:
    clean_values = unique_values(values)
    if clean_values:
        props[key] = clean_values
    else:
        props.pop(key, None)


def add_value(props: dict[str, Any], key: str, value: Any) -> None:
    if value in (None, "", [], {}):
        return
    current = values_of(props.get(key))
    current.append(value)
    set_values(props, key, current)


def set_flag(props: dict[str, Any], key: str) -> None:
    props[key] = True


def remove_prop_by_fold(props: dict[str, Any], folded_name: str) -> Any:
    key = folded_key(props, folded_name)
    if key is None:
        return None
    return props.pop(key)


def product_name(product: dict[str, Any]) -> str:
    termek = product.get("termek")
    if isinstance(termek, dict):
        return str(termek.get("product_name", ""))
    return str(termek or "")


def split_base_values(value: Any) -> list[str]:
    text = str(value)
    parts = re.split(r"\s+(?:és|&)\s+", text)
    return [part.strip() for part in parts if part.strip()]


def normalize_dusitas(value: Any) -> str:
    folded = fold_text(value)
    if "jod" in folded:
        return "jód"
    if "asvanyi" in folded:
        return "ásványi anyag"
    if "b12" in folded:
        return "B12-vitamin"
    if "b6" in folded:
        return "B6-vitamin"
    if "d2" in folded:
        return "D2-vitamin"
    if "d3" in folded:
        return "D3-vitamin"
    if folded in {"d-vitamin", "d vitamin"}:
        return "D-vitamin"
    if "e-vitamin" in folded or folded == "e vitamin":
        return "E-vitamin"
    if "c-vitamin" in folded or folded == "c vitamin":
        return "C-vitamin"
    if "vitamin" in folded:
        return "vitamin"
    return str(value)


def normalize_animal(value: Any) -> str | None:
    folded = fold_text(value)
    if "bivaly" in folded:
        return "bivaly"
    if "juh" in folded:
        return "juh"
    if "kecske" in folded:
        return "kecske"
    if "tehen" in folded:
        return "tehén"
    return None


def migrate_named_props(product: dict[str, Any]) -> int:
    props = product.get("tulajdonsagok")
    if not isinstance(props, dict):
        return 0

    changes = 0

    for source in ["alapanyag", "novenyi_alap"]:
        value = remove_prop_by_fold(props, source)
        if value is not None:
            for item in values_of(value):
                for part in split_base_values(item):
                    add_value(props, "alap", part)
            changes += 1

    for source in ["sajtfajta", "sajt tipusa"]:
        value = remove_prop_by_fold(props, source)
        if value is not None:
            for item in values_of(value):
                add_value(props, "fajta", normalize_fajta_value(item))
            changes += 1

    value = remove_prop_by_fold(props, "tejtipus")
    if value is not None:
        for item in values_of(value):
            animal = normalize_animal(item)
            if animal:
                add_value(props, "állat", animal)
        changes += 1

    value = remove_prop_by_fold(props, "turo tipusa")
    if value is not None:
        for item in values_of(value):
            animal = normalize_animal(item)
            if animal:
                add_value(props, "állat", animal)
        changes += 1

    value = remove_prop_by_fold(props, "tartasi mod")
    if value is not None:
        for item in values_of(value):
            add_value(props, "tartás", item)
        changes += 1

    for source in ["hozzaadott anyag", "hozzaadott vitamin / asvanyi anyag"]:
        value = remove_prop_by_fold(props, source)
        if value is not None:
            for item in values_of(value):
                add_value(props, "dúsítás", normalize_dusitas(item))
            changes += 1

    value = remove_prop_by_fold(props, "kiszereles_mennyiseg")
    if value is not None:
        for item in values_of(value):
            add_value(props, "kiszerelés", item)
        changes += 1

    for source in ["iz / jelleg", "valtozat"]:
        value = remove_prop_by_fold(props, source)
        if value is not None:
            for item in values_of(value):
                folded = fold_text(item)
                if "light" in folded:
                    set_flag(props, "light / csökkentett zsír")
                elif "suto" in folded and "margarin" in folded:
                    set_flag(props, "sütőmargarin")
                elif "omega" in folded:
                    add_value(props, "dúsítás", "omega-3")
                elif "vitamin" in folded or "multivitamin" in folded:
                    add_value(props, "dúsítás", "vitamin")
                elif "sos" in folded:
                    set_flag(props, "sózott")
                elif "novenyi" in folded:
                    add_value(props, "alap", "növényi")
                elif folded not in {"classic", "original", "gold", "sandwich"}:
                    add_value(props, "íz", item)
            changes += 1

    value = remove_prop_by_fold(props, "cukormentes")
    if value is not None:
        if values_of(value):
            set_flag(props, "cukormentes / hozzáadott cukor nélkül")
        changes += 1

    value = remove_prop_by_fold(props, "elofloras")
    if value is not None:
        if values_of(value):
            set_flag(props, "élőflórás/probiotikus")
        changes += 1

    value = remove_prop_by_fold(props, "feherje")
    if value is not None:
        if values_of(value):
            set_flag(props, "protein / magas fehérje")
        changes += 1

    value = remove_prop_by_fold(props, "zsirszegeny")
    if value is not None:
        if values_of(value):
            add_value(props, "zsírtartalom", "zsírszegény")
        changes += 1

    value = remove_prop_by_fold(props, "novenyi alapu")
    if value is not None:
        if values_of(value):
            add_value(props, "alap", "növényi")
        changes += 1

    value = remove_prop_by_fold(props, "minosites")
    if value is not None:
        for item in values_of(value):
            if fold_text(item) == "bio":
                set_flag(props, "bio")
        changes += 1

    for source in ["dieta", "mentes", "mentesseg"]:
        value = remove_prop_by_fold(props, source)
        if value is not None:
            for item in values_of(value):
                folded = fold_text(item)
                if "vegan" in folded:
                    set_flag(props, "vegán")
                if "laktozmentes" in folded:
                    set_flag(props, "laktózmentes")
                if "glutenmentes" in folded:
                    set_flag(props, "gluténmentes")
            changes += 1

    value = remove_prop_by_fold(props, "friss")
    if value is not None:
        changes += 1

    value = remove_prop_by_fold(props, "tej tipusa")
    if value is not None:
        for item in values_of(value):
            folded = fold_text(item)
            if "uht" in folded:
                set_flag(props, "UHT")
            elif "esl" in folded:
                add_value(props, "hőkezelés", "ESL")
        changes += 1

    value = remove_prop_by_fold(props, "zsirtartalom / jelleg")
    if value is not None:
        for item in values_of(value):
            folded = fold_text(item)
            if folded in {"egyeb"}:
                continue
            if re.fullmatch(r"\d+(?:,\d+)?%", str(item).strip()) or folded in {"zsirszegeny", "felzsiros", "teljes", "sovany"}:
                add_value(props, "zsírtartalom_jelleg", item)
            elif folded in {"barista", "habkesziteshez", "sutes-fozeshez", "habalap es fozokrem"}:
                add_value(props, "felhasználás", item)
        changes += 1

    value = remove_prop_by_fold(props, "jeloles")
    if value is not None:
        for item in values_of(value):
            folded = fold_text(item)
            if "glutenmentes" in folded:
                set_flag(props, "gluténmentes")
            elif "laktozmentes" in folded:
                set_flag(props, "laktózmentes")
        changes += 1

    return changes


def normalize_fajta_value(value: Any) -> str:
    folded = fold_text(value)
    return FAJTA_MAP.get(folded, str(value))


def clean_sajt_forma(props: dict[str, Any]) -> int:
    key = folded_key(props, "forma")
    if key is None:
        return 0

    old_values = values_of(props.get(key))
    new_values: list[Any] = []
    changed = False
    for value in old_values:
        folded = fold_text(value)
        if folded in SAJT_FORMA_DROP:
            changed = True
            continue
        mapped = SAJT_FORMA_MAP.get(folded)
        if mapped is not None:
            new_values.extend(mapped)
            changed = True
        else:
            new_values.append(value)

    set_values(props, key, new_values)
    return int(changed)


def clean_fajta(props: dict[str, Any], altipus: str = "") -> int:
    key = folded_key(props, "fajta")
    if key is None:
        return 0

    old_values = values_of(props.get(key))
    new_values: list[Any] = []
    changed = False
    alt_folded = fold_text(altipus)

    for value in old_values:
        folded = fold_text(value)
        if folded in FAJTA_DROP:
            changed = True
            continue

        normalized = normalize_fajta_value(value)
        normalized_folded = fold_text(normalized)
        if normalized_folded != folded:
            changed = True

        if (
            alt_folded
            and normalized_folded
            and normalized_folded in alt_folded
            and alt_folded
            in {
                "mozzarella",
                "mascarpone",
                "trappista sajt",
                "cheddar",
                "parenyica",
                "ricotta",
                "kecskesajt",
                "juhsajt",
                "burrata",
                "raclette",
                "scamorza",
            }
        ):
            changed = True
            continue

        if alt_folded == "omlesztett sajt" and normalized_folded in {
            "omlesztett",
            "omlesztett sajt",
            "omlesztett sajtszelet",
            "omlesztett cheddar sajtos szelet",
            "lapka sajt",
            "toast szelet",
        }:
            changed = True
            continue

        new_values.append(normalized)

    set_values(props, key, new_values)
    return int(changed)


def has_prop_value(props: dict[str, Any], prop_folded: str, candidates: set[str]) -> bool:
    key = folded_key(props, prop_folded)
    if key is None:
        return False
    return any(fold_text(value) in candidates for value in values_of(props.get(key)))


def clean_sajt_jelleg(props: dict[str, Any], altipus: str) -> int:
    key = folded_key(props, "jelleg")
    if key is None:
        return 0

    old_values = values_of(props.get(key))
    new_values: list[Any] = []
    changed = False
    alt_folded = fold_text(altipus)

    for value in old_values:
        text = str(value)
        folded = fold_text(text)

        if folded in {"nincs kep", "classic", "klasszikus", "mini", "dan", "ir"}:
            changed = True
            continue
        if "laktozmentes" in folded:
            set_flag(props, "laktózmentes")
            changed = True
            continue
        if "protein" in folded:
            set_flag(props, "protein / magas fehérje")
            changed = True
            continue
        if folded in {"light", "zsirszegeny", "felzsiros", "zsiros", "zsirdus", "sovany"}:
            if folded == "light":
                set_flag(props, "light / csökkentett zsír")
            else:
                add_value(props, "zsírtartalom", text)
            changed = True
            continue
        if re.fullmatch(r"(?:min\.\s*)?\d+(?:,\d+)?%", text.strip()):
            add_value(props, "zsírtartalom", text)
            changed = True
            continue
        if folded == "kenheto":
            add_value(props, "forma", "kenhető")
            changed = True
            continue
        if folded == "vaghato":
            changed = True
            continue
        if folded in {"lagy", "felkemeny", "friss"} and folded in alt_folded:
            changed = True
            continue
        if folded in {"fokhagymas", "snidlinges", "provanszi", "olaszfuszeres", "zoldfuszeres", "erdei gombas", "zoldborsos", "afonyaszosszal", "mango chutney szosszal", "bazsalikomos"}:
            add_value(props, "ízesítés", text)
            changed = True
            continue

        new_values.append(value)

    set_values(props, key, new_values)
    return int(changed)


def clean_nonsajt_values(product: dict[str, Any]) -> int:
    props = product.get("tulajdonsagok")
    if not isinstance(props, dict):
        return 0

    changes = 0
    for prop_folded in ["zsirtartalom", "zsirtartalom / jelleg", "zsirtartalom_jelleg"]:
        key = folded_key(props, prop_folded)
        if key is None:
            continue
        values = values_of(props.get(key))
        new_values: list[Any] = []
        for value in values:
            folded = fold_text(value)
            if folded in {"bio", "glutenmentes", "cukormentes", "edesitett", "spray"}:
                if folded == "bio":
                    set_flag(props, "bio")
                elif folded == "glutenmentes":
                    set_flag(props, "gluténmentes")
                elif folded == "cukormentes":
                    set_flag(props, "cukormentes / hozzáadott cukor nélkül")
                elif folded == "edesitett":
                    set_flag(props, "cukrozott")
                elif folded == "spray":
                    add_value(props, "forma", "spray")
                changes += 1
            elif re.fullmatch(r"\d+(?:,\d+)?%", str(value).strip()):
                add_value(props, "zsírtartalom", value)
                changes += 1
            elif folded in {"barista", "habkesziteshez", "sutes-fozeshez", "habalap es fozokrem"}:
                add_value(props, "felhasználás", value)
                changes += 1
            elif folded in {"aludttej", "kecsketej"}:
                if folded == "kecsketej":
                    add_value(props, "állat", "kecske")
                changes += 1
            else:
                new_values.append(value)
        if len(new_values) != len(values):
            set_values(props, key, new_values)
    return changes


def ensure_alt_type(alkategoriak: dict[str, Any], alk_folded: str, alt_name: str) -> None:
    alk_key = require_key(alkategoriak, alk_folded)
    alk_node = alkategoriak[alk_key]
    altipusok = folded_get(alk_node, "altipusok", {}) or {}
    if folded_key(altipusok, fold_text(alt_name)) is None:
        altipusok[alt_name] = {
            "tulajdonságok": {"egyedi": {}, "csoportos": {}},
            "altípusok": {},
        }


def canonical_alt(alkategoriak: dict[str, Any], alk_folded: str, alt_folded: str) -> str:
    alk_key = require_key(alkategoriak, alk_folded)
    altipusok = folded_get(alkategoriak[alk_key], "altipusok", {}) or {}
    alt_key = folded_key(altipusok, alt_folded)
    if alt_key is None:
        raise KeyError(f"Missing alt type {alt_folded} under {alk_key}")
    return alt_key


def assign_product(
    product: dict[str, Any],
    index: int,
    alkategoriak: dict[str, Any],
    alk_folded: str,
    alt_folded: str,
    reason: str,
    moves: list[dict[str, Any]],
) -> None:
    new_alk = require_key(alkategoriak, alk_folded)
    new_alt = canonical_alt(alkategoriak, alk_folded, alt_folded)
    old_alk = product.get("alkategoria", "")
    old_alt = product.get("altipus", "")
    if old_alk == new_alk and old_alt == new_alt:
        return
    product["alkategoria"] = new_alk
    product["altipus"] = new_alt
    moves.append(
        {
            "index": index,
            "termek": product_name(product),
            "regi_alkategoria": old_alk,
            "regi_altipus": old_alt,
            "uj_alkategoria": new_alk,
            "uj_altipus": new_alt,
            "ok": reason,
        }
    )


def rename_fermented_category(category_node: dict[str, Any], products: list[dict[str, Any]]) -> int:
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    old_key = folded_key(alkategoriak, OLD_FERMENTED_ALK_FOLDED)
    new_key = folded_key(alkategoriak, fold_text(NEW_FERMENTED_ALK))
    renamed = 0

    if old_key is not None and new_key is None:
        items = list(alkategoriak.items())
        rebuilt = {}
        for key, value in items:
            if key == old_key:
                rebuilt[NEW_FERMENTED_ALK] = value
                renamed += 1
            else:
                rebuilt[key] = value
        alkategoriak.clear()
        alkategoriak.update(rebuilt)
    elif new_key is not None:
        renamed += 0

    for product in products:
        if (
            fold_text(product.get("fokategoria", "")) == TARGET_CATEGORY_FOLDED
            and fold_text(product.get("alkategoria", "")) == OLD_FERMENTED_ALK_FOLDED
        ):
            product["alkategoria"] = NEW_FERMENTED_ALK
            renamed += 1

    return renamed


def clean_category_tree(category_node: dict[str, Any]) -> Counter[str]:
    counters: Counter[str] = Counter()

    def clean_prop_block(block: Any) -> None:
        if not isinstance(block, dict):
            return
        for group in block.values():
            if not isinstance(group, dict):
                continue
            for prop_folded in REMOVED_PROP_FOLDS | {"jeloles"}:
                if pop_by_fold(group, prop_folded) is not None:
                    counters["removed_declared_property"] += 1
            forma_key = folded_key(group, "forma")
            if forma_key and isinstance(group.get(forma_key), list):
                values = []
                for value in group[forma_key]:
                    folded = fold_text(value)
                    if folded in SAJT_FORMA_DROP:
                        counters["removed_forma_value"] += 1
                        continue
                    mapped = SAJT_FORMA_MAP.get(folded)
                    if mapped:
                        values.extend(mapped)
                        counters["mapped_forma_value"] += 1
                    else:
                        values.append(value)
                group[forma_key] = unique_values(values)
            fajta_key = folded_key(group, "fajta")
            if fajta_key and isinstance(group.get(fajta_key), list):
                values = []
                for value in group[fajta_key]:
                    folded = fold_text(value)
                    if folded in FAJTA_DROP:
                        counters["removed_fajta_value"] += 1
                        continue
                    normalized = normalize_fajta_value(value)
                    if fold_text(normalized) != folded:
                        counters["mapped_fajta_value"] += 1
                    values.append(normalized)
                group[fajta_key] = unique_values(values)
            jelleg_key = folded_key(group, "jelleg")
            if jelleg_key and isinstance(group.get(jelleg_key), list):
                values = []
                for value in group[jelleg_key]:
                    folded = fold_text(value)
                    if (
                        folded in SAJT_JELLEG_DROP
                        or re.fullmatch(r"(?:min\.\s*)?\d+(?:,\d+)?%", str(value).strip())
                    ):
                        counters["removed_jelleg_value"] += 1
                        continue
                    values.append(value)
                group[jelleg_key] = unique_values(values)
            fat_kind_key = folded_key(group, "zsirtartalom_jelleg")
            if fat_kind_key and isinstance(group.get(fat_kind_key), list):
                values = []
                for value in group[fat_kind_key]:
                    folded = fold_text(value)
                    if re.fullmatch(r"\d+(?:,\d+)?%", str(value).strip()) or folded in {
                        "barista",
                        "habkesziteshez",
                        "sutes-fozeshez",
                        "habalap es fozokrem",
                        "edesitett",
                        "spray",
                    }:
                        counters["removed_zsirtartalom_jelleg_value"] += 1
                        continue
                    values.append(value)
                group[fat_kind_key] = unique_values(values)

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            props = folded_get(node, "tulajdonsagok")
            clean_prop_block(props)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(category_node)
    return counters


def declared_paths(category_node: dict[str, Any]) -> set[tuple[str, str]]:
    paths = set()
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    for alkategoria, alk_node in alkategoriak.items():
        paths.add((alkategoria, ""))
        altipusok = folded_get(alk_node, "altipusok", {}) or {}
        for altipus in altipusok:
            paths.add((alkategoria, altipus))
    return paths


def validate(products: list[dict[str, Any]], category_node: dict[str, Any]) -> dict[str, Any]:
    paths = declared_paths(category_node)
    missing_paths = Counter()
    removed_prop_count = Counter()
    bad_sajt_forma = Counter()
    milk_count = 0
    empty_alt = 0

    for product in products:
        if fold_text(product.get("fokategoria", "")) != TARGET_CATEGORY_FOLDED:
            continue
        milk_count += 1
        alk = product.get("alkategoria", "")
        alt = product.get("altipus", "")
        if not alt:
            empty_alt += 1
        if (alk, alt) not in paths:
            missing_paths[(alk, alt)] += 1
        props = product.get("tulajdonsagok") or {}
        for prop_name, value in props.items():
            if fold_text(prop_name) in REMOVED_PROP_FOLDS:
                removed_prop_count[prop_name] += 1
            if fold_text(alk) == "sajt" and fold_text(prop_name) == "forma":
                for item in values_of(value):
                    if fold_text(item) in SAJT_FORMA_DROP:
                        bad_sajt_forma[str(item)] += 1

    return {
        "milk_products": milk_count,
        "empty_alt": empty_alt,
        "missing_paths": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in missing_paths.most_common()
        ],
        "removed_prop_count": dict(removed_prop_count),
        "bad_sajt_forma": dict(bad_sajt_forma),
    }


def write_report(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Tejtermékek második javítási iteráció",
        "",
        f"- Generálva: {payload['meta']['generated_at']}",
        f"- Mód: {payload['meta']['mode']}",
        f"- Kategória/termék átnevezések: {payload['renamed_fermented']}",
        f"- Termékmozgatások: {len(payload['product_moves'])}",
        f"- Tulajdonság-módosítások: {payload['property_changes']}",
        "",
        "## Kategóriafa módosítások",
    ]
    for key, value in payload["category_changes"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Validálás"])
    validation = payload["validation"]
    lines.extend(
        [
            f"- Tejtermékes termékek: {validation['milk_products']}",
            f"- Üres altípus: {validation['empty_alt']}",
            f"- Hiányzó kategóriaútvonal: {len(validation['missing_paths'])}",
            f"- Régi mezők maradtak: {validation['removed_prop_count']}",
            f"- Tiltott sajt forma érték maradt: {validation['bad_sajt_forma']}",
        ]
    )

    lines.extend(["", "## Termékmozgatások"])
    for move in payload["product_moves"]:
        lines.append(
            f"- #{move['index']} {move['regi_alkategoria']} / {move['regi_altipus']} -> "
            f"{move['uj_alkategoria']} / {move['uj_altipus']}: {move['termek']}"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write changes to the main JSON files.")
    args = parser.parse_args()

    generated_at = datetime.now().isoformat(timespec="seconds")
    date_stamp = generated_at[:10]
    categories = load_json(CATEGORY_PATH)
    products = load_json(PRODUCT_PATH)
    category_key = require_key(categories, TARGET_CATEGORY_FOLDED)
    category_node = categories[category_key]
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}

    renamed_fermented = rename_fermented_category(category_node, products)
    ensure_alt_type(alkategoriak, "novenyi alternativa", "Növényi sajt")
    ensure_alt_type(alkategoriak, "turo", "Cottage cheese")
    ensure_alt_type(alkategoriak, "sajtkrem, szendvicskrem", "Sajtkrém")

    product_moves: list[dict[str, Any]] = []
    property_changes = 0
    for index, product in enumerate(products):
        if fold_text(product.get("fokategoria", "")) != TARGET_CATEGORY_FOLDED:
            continue

        props = product.get("tulajdonsagok")
        if not isinstance(props, dict):
            continue

        property_changes += migrate_named_props(product)
        if fold_text(product.get("alkategoria", "")) == "sajt":
            if has_prop_value(props, "fajta", {"cottage cheese"}) or "cottage cheese" in fold_text(product_name(product)):
                assign_product(
                    product,
                    index,
                    alkategoriak,
                    "turo",
                    "cottage cheese",
                    "Cottage cheese atvezetese Turo ala",
                    product_moves,
                )
            elif has_prop_value(props, "fajta", {"szendvicskrem", "sajtos szendvicskrem"}):
                assign_product(
                    product,
                    index,
                    alkategoriak,
                    "sajtkrem, szendvicskrem",
                    "szendvicskrem",
                    "Szendvicskrem atvezetese Sajtkrém alkategoria ala",
                    product_moves,
                )
            elif has_prop_value(props, "fajta", {"sajtkrem", "kremsajt", "friss sajtkrem"}):
                assign_product(
                    product,
                    index,
                    alkategoriak,
                    "sajtkrem, szendvicskrem",
                    "sajtkrem",
                    "Sajtkrem atvezetese Sajtkrém alkategoria ala",
                    product_moves,
                )

            property_changes += clean_sajt_forma(props)
            property_changes += clean_sajt_jelleg(props, product.get("altipus", ""))
            if props.get("készítmény (növényi zsiradékkal)") is True and (
                "sajthelyettesito" in fold_text(str(props)) or "novenyi zsir" in fold_text(product_name(product))
            ):
                assign_product(
                    product,
                    index,
                    alkategoriak,
                    "novenyi alternativa",
                    "novenyi sajt",
                    "Sajthelyettesito atvezetese novenyi alternativa ala",
                    product_moves,
                )
        else:
            property_changes += clean_nonsajt_values(product)

        property_changes += clean_fajta(props, product.get("altipus", ""))

    category_changes = clean_category_tree(category_node)
    validation = validate(products, category_node)

    payload = {
        "meta": {
            "generated_at": generated_at,
            "mode": "apply" if args.apply else "dry-run",
            "category_source": CATEGORY_PATH.name,
            "product_source": PRODUCT_PATH.name,
            "fokategoria": category_key,
        },
        "renamed_fermented": renamed_fermented,
        "product_moves": product_moves,
        "property_changes": property_changes,
        "category_changes": dict(category_changes),
        "validation": validation,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report_json = OUT_DIR / f"tejtermekek_masodik_iteracio_{date_stamp}.json"
    report_md = OUT_DIR / f"tejtermekek_masodik_iteracio_{date_stamp}.md"
    dump_json(report_json, payload)
    write_report(report_md, payload)

    failed = bool(
        validation["empty_alt"]
        or validation["missing_paths"]
        or validation["removed_prop_count"]
        or validation["bad_sajt_forma"]
    )
    if args.apply:
        if failed:
            raise SystemExit("Validation failed; main files were not written.")
        dump_json(CATEGORY_PATH, categories)
        dump_json(PRODUCT_PATH, products)

    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"renamed_fermented={renamed_fermented}")
    print(f"product_moves={len(product_moves)}")
    print(f"property_changes={property_changes}")
    print(f"category_changes={dict(category_changes)}")
    print(f"empty_alt={validation['empty_alt']}")
    print(f"missing_paths={len(validation['missing_paths'])}")
    print(f"removed_prop_count={validation['removed_prop_count']}")
    print(f"bad_sajt_forma={validation['bad_sajt_forma']}")
    print(f"report_json={report_json}")
    print(f"report_md={report_md}")


if __name__ == "__main__":
    main()
