from __future__ import annotations

import argparse
import json
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


OBSOLETE_ALKATEGORIA_FOLDS = {
    "desszert",
    "egyeb tejtermek",
    "joghurt, kefir",
    "joghurtital",
    "novenyi tejhelyettesito",
    "sajtkrem, kremsajt",
    "tejes desszert",
    "tejes ital",
    "tejpor",
    "tejszin, hab",
    "tejszin, tejfol",
    "turo, cottage cheese",
}

SAJT_ALT_REMOVALS = {
    "camembert, brie",
    "cottage cheese",
    "feta",
    "kremfeher sajt",
    "kremsajt",
    "lagy sajt",
    "novenyi sajthelyettesito",
    "novenyi szendvicskrem",
    "sajtkrem",
    "sajtkrem, szendvicskrem",
    "szendvicskrem",
    "turo, cottage cheese",
}

JOGHURT_ALT_REMOVALS = {
    "gyerek joghurt",
    "izesitett joghurt",
    "laktozmentes joghurt",
    "novenyi joghurtalternativa",
    "protein joghurt",
}

TEJ_ALT_REMOVALS = {
    "funkcionalis tejital",
    "izesitett tejital",
    "jegeskave",
    "protein ital",
    "protein tej",
    "uht tej",
}

ALWAYS_REMOVE_PRODUCT_PROPS = {
    "eredet",
    "illat / osszetevo",
    "keverek",
    "kisero",
    "koffein",
    "minoseg",
    "sajttartalom",
    "szin",
    "termekcsalad",
    "termekvonal",
    "tipus",
    "toltott",
}

MIGRATED_PRODUCT_PROP_FOLDS = {
    "allag",
    "edesitett",
    "erleles",
    "erleltseg",
    "extra_sarga",
    "magas feherjetartalmu",
    "sovany",
    "tojasfajta",
    "toltelek",
    "zsirtartalom jelleg",
}

GENERIC_MIGRATED_PROP_FOLDS = {
    "cukor",
    "etrend",
    "hozzaadott",
    "jellemzo",
    "jellemzok",
    "novenyi alap",
    "vitamin",
    "zsirossag",
}

CATEGORY_REMOVE_PROP_FOLDS = ALWAYS_REMOVE_PRODUCT_PROPS | MIGRATED_PRODUCT_PROP_FOLDS | GENERIC_MIGRATED_PROP_FOLDS


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


def folded_get(mapping: dict[str, Any], wanted_folded_key: str, default: Any = None) -> Any:
    for key, value in mapping.items():
        if fold_text(key) == wanted_folded_key:
            return value
    return default


def folded_key(mapping: dict[str, Any], wanted_folded_key: str) -> str | None:
    for key in mapping:
        if fold_text(key) == wanted_folded_key:
            return key
    return None


def require_key(mapping: dict[str, Any], wanted_folded_key: str) -> str:
    key = folded_key(mapping, wanted_folded_key)
    if key is None:
        raise KeyError(f"Missing key for folded name: {wanted_folded_key}")
    return key


def pop_by_fold(mapping: dict[str, Any], wanted_folded_key: str) -> Any:
    key = folded_key(mapping, wanted_folded_key)
    if key is None:
        return None
    return mapping.pop(key)


def values_of(value: Any) -> list[Any]:
    if value in (None, "", [], {}):
        return []
    return value if isinstance(value, list) else [value]


def add_list_value(props: dict[str, Any], key: str, value: Any) -> None:
    if value in (None, "", [], {}):
        return
    existing = props.get(key)
    if existing in (None, "", [], {}):
        props[key] = [value]
        return
    if not isinstance(existing, list):
        existing = [existing]
        props[key] = existing
    if value not in existing:
        existing.append(value)


def set_flag(props: dict[str, Any], key: str) -> None:
    props[key] = True


def product_name(product: dict[str, Any]) -> str:
    termek = product.get("termek")
    if isinstance(termek, dict):
        return str(termek.get("product_name", ""))
    return str(termek or "")


def remove_prop_by_fold(props: dict[str, Any], folded_name: str) -> Any:
    key = folded_key(props, folded_name)
    if key is None:
        return None
    return props.pop(key)


def migrate_generic_values(props: dict[str, Any], source_folded: str, remove_unknown: bool = False) -> int:
    key = folded_key(props, source_folded)
    if key is None:
        return 0

    original_values = values_of(props.get(key))
    kept_values: list[Any] = []
    migrations = 0

    for value in original_values:
        text = str(value)
        folded = fold_text(text)
        handled = False

        if "laktozmentes" in folded:
            set_flag(props, "laktózmentes")
            handled = True
        if "glutenmentes" in folded:
            set_flag(props, "gluténmentes")
            handled = True
        if "vegan" in folded:
            set_flag(props, "vegán")
            handled = True
        if "protein" in folded or "feherje" in folded:
            set_flag(props, "protein / magas fehérje")
            handled = True
        if "uht" in folded:
            set_flag(props, "UHT")
            handled = True
        if "hozzaadott cukor nelkul" in folded or "cukormentes" in folded or "cukor nelkul" in folded:
            set_flag(props, "cukormentes / hozzáadott cukor nélkül")
            handled = True
        if "edesitoszer" in folded:
            set_flag(props, "édesítőszerrel")
            handled = True
        if "elo" in folded and "flor" in folded:
            set_flag(props, "élőflórás/probiotikus")
            handled = True
        if "probiotikus" in folded:
            set_flag(props, "élőflórás/probiotikus")
            handled = True
        if "bio" == folded or folded.startswith("bio "):
            set_flag(props, "bio")
            handled = True
        if "kalcium" in folded:
            add_list_value(props, "dúsítás", "kalcium")
            handled = True
        if "jod" in folded:
            add_list_value(props, "dúsítás", "jód")
            handled = True
        if "asvanyi anyag" in folded:
            add_list_value(props, "dúsítás", "ásványi anyag")
            handled = True
        if "vitamin" in folded or "d-vitamin" in folded or "b6" in folded:
            add_list_value(props, "dúsítás", "vitamin")
            handled = True
        if "magnezium" in folded:
            add_list_value(props, "dúsítás", "magnézium")
            handled = True
        if "folsav" in folded:
            add_list_value(props, "dúsítás", "folsav")
            handled = True
        if "kollagen" in folded:
            add_list_value(props, "dúsítás", "kollagén")
            handled = True
        if "feher nemespenesz" in folded:
            set_flag(props, "érlelt")
            add_list_value(props, "jelleg", "fehérpenészes")
            handled = True
        if "tejszines" in folded:
            add_list_value(props, "íz", "tejszínes")
            handled = True
        if "izlandi recept" in folded:
            handled = True
        if "tejfol helyettesito" in folded:
            handled = True
        if "novenyi zsir" in folded:
            add_list_value(props, "alap", "növényi zsír")
            handled = True
        if "novenyi alapu" in folded:
            add_list_value(props, "alap", "növényi")
            set_flag(props, "vegán")
            handled = True
        if folded in {"zsirszegeny", "sovany", "felzsiros", "light", "zsiros", "zsirdus", "zsirmentes"} or "sovany friss sajt" in folded:
            add_list_value(props, "zsírtartalom", text)
            handled = True

        if handled:
            migrations += 1
        elif not remove_unknown:
            kept_values.append(value)

    if kept_values:
        props[key] = kept_values
    elif migrations or remove_unknown:
        props.pop(key, None)

    return migrations


def migrate_rare_named_props(props: dict[str, Any]) -> int:
    changes = 0

    value = remove_prop_by_fold(props, "magas feherjetartalmu")
    if value is not None:
        if values_of(value):
            set_flag(props, "protein / magas fehérje")
        changes += 1

    value = remove_prop_by_fold(props, "toltelek")
    if value is not None:
        for item in values_of(value):
            add_list_value(props, "íz", item)
        changes += 1

    for folded_name in ["erleles", "erleltseg"]:
        value = remove_prop_by_fold(props, folded_name)
        if value is not None:
            if values_of(value):
                set_flag(props, "érlelt")
            changes += 1

    value = remove_prop_by_fold(props, "zsirtartalom jelleg")
    if value is not None:
        for item in values_of(value):
            add_list_value(props, "zsírtartalom_jelleg", item)
        changes += 1

    value = remove_prop_by_fold(props, "allag")
    if value is not None:
        for item in values_of(value):
            add_list_value(props, "forma", item)
        changes += 1

    value = remove_prop_by_fold(props, "sovany")
    if value is not None:
        if values_of(value):
            add_list_value(props, "zsírtartalom", "sovány")
        changes += 1

    value = remove_prop_by_fold(props, "edesitett")
    if value is not None:
        if values_of(value):
            set_flag(props, "cukrozott")
        changes += 1

    value = remove_prop_by_fold(props, "tojasfajta")
    if value is not None:
        for item in values_of(value):
            add_list_value(props, "fajta", item)
        changes += 1

    value = remove_prop_by_fold(props, "extra_sarga")
    if value is not None:
        if values_of(value):
            set_flag(props, "extra sárga")
        changes += 1

    return changes


def normalize_product_props(product: dict[str, Any]) -> int:
    props = product.setdefault("tulajdonsagok", {})
    if not isinstance(props, dict):
        product["tulajdonsagok"] = {}
        return 0

    changes = migrate_rare_named_props(props)
    for folded_name in ALWAYS_REMOVE_PRODUCT_PROPS:
        if remove_prop_by_fold(props, folded_name) is not None:
            changes += 1

    for source in ["jellemzok", "etrend", "jellemzo", "hozzaadott", "cukor", "zsirossag", "vitamin"]:
        changes += migrate_generic_values(props, source, remove_unknown=True)

    novenyi_alap = remove_prop_by_fold(props, "novenyi alap")
    if novenyi_alap is not None:
        for value in values_of(novenyi_alap):
            add_list_value(props, "alap", value)
        changes += 1

    if product.get("alkategoria") == "Ivójoghurt, kefir, író":
        jelleg = remove_prop_by_fold(props, "jelleg")
        if jelleg is not None:
            for value in values_of(jelleg):
                text = str(value)
                folded = fold_text(text)
                if "elo" in folded and "flor" in folded or "probiotikus" in folded:
                    set_flag(props, "élőflórás/probiotikus")
                elif "sos" in folded:
                    add_list_value(props, "íz", "sós")
                elif "vitamin" in folded:
                    add_list_value(props, "dúsítás", "vitamin")
                elif "edesitoszer" in folded:
                    set_flag(props, "édesítőszerrel")
                elif "laktozmentes" in folded:
                    set_flag(props, "laktózmentes")
                elif "%" in text or "zsir" in folded:
                    add_list_value(props, "zsírtartalom", text)
            changes += 1

    return changes


def ensure_alt_type(alkategoriak: dict[str, Any], alk_folded: str, alt_name: str) -> None:
    alk_key = require_key(alkategoriak, alk_folded)
    alk_node = alkategoriak[alk_key]
    altipusok = folded_get(alk_node, "altipusok")
    if not isinstance(altipusok, dict):
        altipusok = {}
        alk_node["altípusok"] = altipusok
    if folded_key(altipusok, fold_text(alt_name)) is None:
        altipusok[alt_name] = {
            "tulajdonságok": {
                "egyedi": {},
                "csoportos": {},
            },
            "altípusok": {},
        }


def canonical_alt(alkategoriak: dict[str, Any], alk_folded: str, alt_folded: str, fallback: str | None = None) -> str:
    alk_key = require_key(alkategoriak, alk_folded)
    altipusok = folded_get(alkategoriak[alk_key], "altipusok", {}) or {}
    key = folded_key(altipusok, alt_folded)
    if key is not None:
        return key
    if fallback is None:
        raise KeyError(f"Missing alt type {alt_folded} under {alk_key}")
    ensure_alt_type(alkategoriak, alk_folded, fallback)
    return fallback


def assign_product(
    product: dict[str, Any],
    index: int,
    alkategoriak: dict[str, Any],
    target_alk_folded: str,
    target_alt_folded: str,
    reason: str,
    changes: list[dict[str, Any]],
    fallback_alt: str | None = None,
) -> None:
    old_alk = product.get("alkategoria", "")
    old_alt = product.get("altipus", "")
    new_alk = require_key(alkategoriak, target_alk_folded)
    new_alt = canonical_alt(alkategoriak, target_alk_folded, target_alt_folded, fallback_alt)

    if old_alk == new_alk and old_alt == new_alt:
        return

    product["alkategoria"] = new_alk
    product["altipus"] = new_alt
    changes.append(
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


def kremturo_alt(product: dict[str, Any]) -> tuple[str, str]:
    name = fold_text(product_name(product))
    props = product.get("tulajdonsagok") or {}
    iz_values = [fold_text(value) for value in values_of(props.get("íz"))]
    if "natúr" in product_name(product).casefold() or iz_values == ["natur"]:
        return "natur kremturo", "Natúr krémtúró"
    return "gyumolcsos kremturo", "Gyümölcsös krémtúró"


def tejital_alt(product: dict[str, Any]) -> tuple[str, str]:
    name = fold_text(product_name(product))
    if "kakao" in name:
        return "kakaos tej", "Kakaós tej"
    if "jegeskave" in name or "ice coffee" in name:
        return "jegeskave", "Jegeskávé"
    if "latte" in name or "cappuccino" in name or "kave" in name or "espresso" in name:
        return "kaveital / latte / cappuccino", "Kávéital / latte / cappuccino"
    if "protein" in name or "feherje" in name:
        return "protein tejital", "Protein tejital"
    return "egyeb izesitett tejital", "Egyéb ízesített tejital"


def route_products(products: list[dict[str, Any]], alkategoriak: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    changes: list[dict[str, Any]] = []
    prop_changes = 0

    ensure_alt_type(alkategoriak, "tej", "Tejpor")
    ensure_alt_type(alkategoriak, "turo", "Cottage cheese")
    ensure_alt_type(alkategoriak, "sajtkrem, szendvicskrem", "Sajtkrém")

    for index, product in enumerate(products):
        if fold_text(product.get("fokategoria", "")) != TARGET_CATEGORY_FOLDED:
            continue

        alk = fold_text(product.get("alkategoria", ""))
        alt = fold_text(product.get("altipus", ""))
        name = fold_text(product_name(product))

        if alk == "egyeb tejtermek":
            assign_product(product, index, alkategoriak, "tej", "suritett tej", "Egyeb tejtermek/Sűrített tej atvezetese Tej ala", changes)

        elif alk == "tejpor":
            assign_product(product, index, alkategoriak, "tej", "tejpor", "Tejpor kulon alkategoria megszuntetese", changes, "Tejpor")

        elif alk == "turo, cottage cheese":
            assign_product(product, index, alkategoriak, "turo", "cottage cheese", "Turo, cottage cheese kulon alkategoria megszuntetese", changes, "Cottage cheese")

        elif alk == "novenyi tejhelyettesito":
            assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi tejfol", "Novenyi tejhelyettesito beolvasztasa Novenyi alternativa ala", changes)

        elif alk == "sajtkrem, kremsajt":
            assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi szendvicskrem", "Vegan kremkeszitmeny atvezetese novenyi szendvicskrem ala", changes)

        elif alk == "tejes ital":
            assign_product(product, index, alkategoriak, "tejital, jegeskave", "protein tejital", "Tejes ital beolvasztasa Tejital, jegeskave ala", changes)

        elif alk == "joghurtital":
            assign_product(product, index, alkategoriak, "ivojoghurt, kefir, iro", "ivojoghurt", "Joghurtital beolvasztasa ivójoghurt ala", changes)

        elif alk == "joghurt, kefir":
            if alt in {"joghurtital", "ivojoghurt", "savanyu tejkeszitmeny", "fermentalt tejtermek", "ayran"}:
                assign_product(product, index, alkategoriak, "ivojoghurt, kefir, iro", "ivojoghurt", "Joghurt, kefir szetszedese ivójoghurt iranyba", changes)
            elif alt == "kefir":
                assign_product(product, index, alkategoriak, "ivojoghurt, kefir, iro", "kefir", "Joghurt, kefir szetszedese kefir iranyba", changes)
            elif alt == "novenyi fermentalt keszitmeny":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi joghurt / fermentalt keszitmeny", "Novenyi fermentalt keszitmeny atvezetese novenyi alternativa ala", changes)
            elif alt in {"gyumolcsjoghurt", "izesitett joghurt"}:
                assign_product(product, index, alkategoriak, "joghurt", "gyumolcsos/izesitett joghurt", "Joghurt, kefir szetszedese izesitett joghurt iranyba", changes)
            elif alt == "kremjoghurt":
                assign_product(product, index, alkategoriak, "joghurt", "kremjoghurt", "Joghurt, kefir szetszedese kremjoghurt iranyba", changes)
            elif alt == "natur joghurt":
                assign_product(product, index, alkategoriak, "joghurt", "natur joghurt", "Joghurt, kefir szetszedese natur joghurt iranyba", changes)
            elif alt == "protein joghurt":
                assign_product(product, index, alkategoriak, "joghurt", "skyr / proteinjoghurt", "Joghurt, kefir szetszedese protein joghurt iranyba", changes)

        elif alk == "tejes desszert":
            if alt in {"turodesszert", "turos desszert"}:
                target = "turo rudi jellegu turodesszert" if "rudi" in name else "turodesszert"
                assign_product(product, index, alkategoriak, "kremturo, turodesszert", target, "Tejes desszert turodesszert atvezetese", changes)
            elif alt == "kremturo":
                target_fold, fallback = kremturo_alt(product)
                assign_product(product, index, alkategoriak, "kremturo, turodesszert", target_fold, "Tejes desszert kremturo atvezetese", changes, fallback)
            elif alt == "novenyi desszert":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi desszert", "Novenyi desszert atvezetese novenyi alternativa ala", changes)
            elif alt == "puding":
                assign_product(product, index, alkategoriak, "tejdesszert, puding", "puding", "Tejes desszert puding atvezetese", changes)
            elif alt == "tejberizs":
                assign_product(product, index, alkategoriak, "tejdesszert, puding", "tejberizs", "Tejes desszert tejberizs atvezetese", changes)
            elif alt == "habdesszert":
                assign_product(product, index, alkategoriak, "tejdesszert, puding", "habdesszert", "Tejes desszert habdesszert atvezetese", changes)
            elif alt == "grizpuding":
                assign_product(product, index, alkategoriak, "tejdesszert, puding", "puding", "Grizpuding beolvasztasa puding ala", changes)
            else:
                assign_product(product, index, alkategoriak, "tejdesszert, puding", "egyeb tejdesszert", "Tejes desszert altalanos atvezetese", changes)

        elif alk == "desszert":
            if alt in {"protein turodesszert", "laktozmentes turodesszert", "protein ricotta desszert"}:
                assign_product(product, index, alkategoriak, "kremturo, turodesszert", "turodesszert", "Desszert turodesszert atvezetese", changes)
            elif alt == "kremturo":
                target_fold, fallback = kremturo_alt(product)
                assign_product(product, index, alkategoriak, "kremturo, turodesszert", target_fold, "Desszert kremturo atvezetese", changes, fallback)
            elif alt in {"novenyi desszert", "novenyi rizsdesszert"}:
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi desszert", "Desszert novenyi atvezetese", changes)
            elif alt == "rizsdesszert":
                assign_product(product, index, alkategoriak, "tejdesszert, puding", "tejberizs", "Rizsdesszert atvezetese tejberizs ala", changes)
            else:
                assign_product(product, index, alkategoriak, "tejdesszert, puding", "egyeb tejdesszert", "Desszert altalanos atvezetese", changes)

        elif alk == "tejszin, hab":
            if "vegan" in name or "novenyi" in name:
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi fozokrem / tejszin", "Vegan habspray atvezetese novenyi alternativa ala", changes)
            else:
                assign_product(product, index, alkategoriak, "tejszin", "tejszinhab spray", "Tejszin, hab atvezetese tejszin ala", changes)

        elif alk == "tejszin, tejfol":
            if alt in {"fozotejszin", "habtejszin", "tejszinhab spray", "kavetejszin"}:
                assign_product(product, index, alkategoriak, "tejszin", alt, "Tejszin, tejfol szetszedese tejszin iranyba", changes)
            elif alt in {"habkeszitmeny", "novenyi fozokrem", "fozokrem", "novenyi habkrem"}:
                if "novenyi" in name or "hulala" in name or "rama crema" in name or "napraforgo" in name:
                    assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi fozokrem / tejszin", "Novenyi tejszinjellegu termek atvezetese", changes)
                else:
                    assign_product(product, index, alkategoriak, "tejszin", "cukraszhab", "Habkeszitmeny atvezetese cukraszhab ala", changes)
            elif alt == "tejfol":
                target = "laktozmentes tejfol" if "laktozmentes" in name else "tejfol"
                assign_product(product, index, alkategoriak, "tejfol", target, "Tejfol atvezetese sajat alkategoria ala", changes)
            elif alt == "novenyi tejfolhelyettesito":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi tejfol", "Novenyi tejfolhelyettesito atvezetese", changes)
            elif alt == "vajkrem":
                assign_product(product, index, alkategoriak, "sajtkrem, szendvicskrem", "vajkrem", "Vajkrem atvezetese sajtkrem/szendvicskrem ala", changes)
            elif alt == "szendvicskrem":
                assign_product(product, index, alkategoriak, "sajtkrem, szendvicskrem", "szendvicskrem", "Szendvicskrem atvezetese sajtkrem/szendvicskrem ala", changes)
            elif alt == "novenyi kenheto keszitmeny":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi vaj / margarin", "Novenyi kenheto keszitmeny atvezetese", changes)
            elif alt == "novenyi mascarpone":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi sajt", "Novenyi mascarpone atvezetese novenyi sajt ala", changes)
            elif alt == "vaj, margarin, kenheto zsiradek":
                if "margarin" in name or "flora" in name:
                    assign_product(product, index, alkategoriak, "margarin", "margarin", "Margarin atvezetese sajat alkategoria ala", changes)
                elif "kenheto" in name or "keverek" in name:
                    assign_product(product, index, alkategoriak, "vaj", "kenheto vajkeverek", "Kenheto vajkeverek atvezetese vaj ala", changes)
                else:
                    assign_product(product, index, alkategoriak, "vaj", "vaj", "Vaj atvezetese sajat alkategoria ala", changes)

        elif alk == "sajt":
            if alt == "camembert, brie":
                assign_product(product, index, alkategoriak, "sajt", "camembert / brie", "Camembert/brie duplikalt altipus osszevonasa", changes)
            elif alt in {"feta", "kremfeher sajt"}:
                assign_product(product, index, alkategoriak, "sajt", "feta / kremfeher sajt", "Feta/kremfeher duplikalt altipus osszevonasa", changes)
            elif alt == "kremsajt":
                assign_product(product, index, alkategoriak, "sajt", "kremsajt / kenheto sajt", "Kremsajt duplikalt altipus osszevonasa", changes)
            elif alt == "lagy sajt":
                assign_product(product, index, alkategoriak, "sajt", "friss / lagy sajt", "Lagy sajt beolvasztasa friss/lagy sajt ala", changes)
            elif alt in {"sajtkrem, szendvicskrem", "szendvicskrem"}:
                assign_product(product, index, alkategoriak, "sajtkrem, szendvicskrem", "szendvicskrem", "Sajt alatti szendvicskrem atvezetese sajtkrem alkategoria ala", changes)
            elif alt == "novenyi szendvicskrem":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi szendvicskrem", "Novenyi szendvicskrem atvezetese novenyi alternativa ala", changes)
            elif alt == "novenyi sajthelyettesito":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi sajt", "Novenyi sajthelyettesito atvezetese novenyi alternativa ala", changes)
            elif alt == "turo, cottage cheese":
                if "juhturo" in name:
                    assign_product(product, index, alkategoriak, "turo", "juhturo", "Juhturo atvezetese turo alkategoria ala", changes)
                elif "cottage" in name:
                    assign_product(product, index, alkategoriak, "turo", "cottage cheese", "Cottage cheese atvezetese turo alkategoria ala", changes, "Cottage cheese")
                else:
                    assign_product(product, index, alkategoriak, "sajt", "friss / lagy sajt", "Friss sajt atvezetese friss/lagy sajt ala", changes)
            elif alt == "cottage cheese":
                assign_product(product, index, alkategoriak, "turo", "cottage cheese", "Cottage cheese atvezetese turo alkategoria ala", changes, "Cottage cheese")

        elif alk == "joghurt":
            if alt == "izesitett joghurt":
                assign_product(product, index, alkategoriak, "joghurt", "gyumolcsos/izesitett joghurt", "Izestett joghurt beolvasztasa gyumolcsos/izesitett joghurt ala", changes)
            elif alt == "protein joghurt":
                assign_product(product, index, alkategoriak, "joghurt", "skyr / proteinjoghurt", "Protein joghurt beolvasztasa skyr/proteinjoghurt ala", changes)
            elif alt == "gyerek joghurt":
                assign_product(product, index, alkategoriak, "joghurt", "gyumolcsos/izesitett joghurt", "Gyerek joghurt beolvasztasa izesitett joghurt ala", changes)
            elif alt == "novenyi joghurtalternativa":
                assign_product(product, index, alkategoriak, "novenyi alternativa", "novenyi joghurt", "Novenyi joghurtalternativa atvezetese", changes)
            elif alt == "laktozmentes joghurt":
                if "natur" in name:
                    assign_product(product, index, alkategoriak, "joghurt", "natur joghurt", "Laktozmentes natur joghurt atvezetese natur joghurt ala", changes)
                elif "protein" in name:
                    assign_product(product, index, alkategoriak, "joghurt", "skyr / proteinjoghurt", "Laktozmentes protein joghurt atvezetese protein joghurt ala", changes)
                else:
                    assign_product(product, index, alkategoriak, "joghurt", "gyumolcsos/izesitett joghurt", "Laktozmentes izesitett joghurt atvezetese", changes)

        elif alk == "tej":
            if alt == "uht tej":
                assign_product(product, index, alkategoriak, "tej", "uht tartos tej", "UHT tej beolvasztasa UHT tartos tej ala", changes)
            elif alt in {"jegeskave", "izesitett tejital", "protein ital", "funkcionalis tejital"}:
                target_fold, fallback = tejital_alt(product)
                assign_product(product, index, alkategoriak, "tejital, jegeskave", target_fold, "Tej alatti ital jellegu altipus atvezetese Tejital ala", changes, fallback)
            elif alt == "protein tej":
                assign_product(product, index, alkategoriak, "tej", "uht tartos tej", "Protein tej ritka altipus beolvasztasa UHT tej ala", changes)

        if not product.get("altipus"):
            current_alk = fold_text(product.get("alkategoria", ""))
            current_name = fold_text(product_name(product))
            props = product.get("tulajdonsagok") or {}

            if current_alk == "tejfol":
                target = "laktozmentes tejfol" if props.get("laktózmentes") is True or "laktozmentes" in current_name else "tejfol"
                assign_product(product, index, alkategoriak, "tejfol", target, "Ures tejfol altipus potlasa", changes)
            elif current_alk == "margarin":
                assign_product(product, index, alkategoriak, "margarin", "margarin", "Ures margarin altipus potlasa", changes)
            elif current_alk == "tojas":
                if "furj" in current_name:
                    target = "furjtojas"
                elif "fott" in current_name or "fustolt" in current_name:
                    target = "fott / fustolt tojas"
                else:
                    target = "tyuktojas"
                assign_product(product, index, alkategoriak, "tojas", target, "Ures tojas altipus potlasa", changes)
            elif current_alk == "tejital, jegeskave":
                target_fold, fallback = tejital_alt(product)
                assign_product(product, index, alkategoriak, "tejital, jegeskave", target_fold, "Ures tejital altipus potlasa", changes, fallback)
            elif current_alk == "sajtkrem, szendvicskrem":
                if "vajkrem" in current_name:
                    target = "vajkrem"
                    fallback = "Vajkrém"
                elif "szendvicskrem" in current_name:
                    target = "szendvicskrem"
                    fallback = "Szendvicskrém"
                elif "omlesztett" in current_name:
                    target = "omlesztett sajt"
                    fallback = "Ömlesztett sajt"
                else:
                    target = "sajtkrem"
                    fallback = "Sajtkrém"
                assign_product(product, index, alkategoriak, "sajtkrem, szendvicskrem", target, "Ures sajtkrem/szendvicskrem altipus potlasa", changes, fallback)

        prop_changes += normalize_product_props(product)

    return changes, prop_changes


def cleanup_category_tree(category_node: dict[str, Any]) -> dict[str, int]:
    alkategoriak = folded_get(category_node, "alkategoriak", {}) or {}
    counters: Counter[str] = Counter()

    ivo_key = require_key(alkategoriak, "ivojoghurt, kefir, iro")
    ivo_props = folded_get(alkategoriak[ivo_key], "tulajdonsagok", {}) or {}
    csoportos = ivo_props.get("csoportos")
    if isinstance(csoportos, dict) and pop_by_fold(csoportos, "jelleg") is not None:
        counters["ivojoghurt_jelleg_torles"] += 1

    for folded_name in OBSOLETE_ALKATEGORIA_FOLDS:
        if pop_by_fold(alkategoriak, folded_name) is not None:
            counters["torolt_alkategoria"] += 1

    for alk_folded, removals in [
        ("sajt", SAJT_ALT_REMOVALS),
        ("joghurt", JOGHURT_ALT_REMOVALS),
        ("tej", TEJ_ALT_REMOVALS),
    ]:
        alk_key = folded_key(alkategoriak, alk_folded)
        if alk_key is None:
            continue
        altipusok = folded_get(alkategoriak[alk_key], "altipusok", {}) or {}
        for alt_folded in removals:
            if pop_by_fold(altipusok, alt_folded) is not None:
                counters[f"{alk_folded}_torolt_altipus"] += 1

    def remove_props_recursive(node: Any) -> None:
        if isinstance(node, dict):
            props = folded_get(node, "tulajdonsagok")
            if isinstance(props, dict):
                for group in props.values():
                    if isinstance(group, dict):
                        for folded_name in CATEGORY_REMOVE_PROP_FOLDS:
                            if pop_by_fold(group, folded_name) is not None:
                                counters["torolt_kategoria_tulajdonsag"] += 1
            for value in node.values():
                remove_props_recursive(value)
        elif isinstance(node, list):
            for value in node:
                remove_props_recursive(value)

    remove_props_recursive(category_node)
    return dict(counters)


def declared_paths(category_node: dict[str, Any]) -> set[tuple[str, str]]:
    paths: set[tuple[str, str]] = set()
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
    obsolete_alk_products = Counter()
    removed_alt_products = Counter()
    prop_counts = Counter()

    for product in products:
        if fold_text(product.get("fokategoria", "")) != TARGET_CATEGORY_FOLDED:
            continue
        alk = product.get("alkategoria", "")
        alt = product.get("altipus", "")
        if (alk, alt) not in paths:
            missing_paths[(alk, alt)] += 1
        if fold_text(alk) in OBSOLETE_ALKATEGORIA_FOLDS:
            obsolete_alk_products[alk] += 1
        if fold_text(alk) == "sajt" and fold_text(alt) in SAJT_ALT_REMOVALS:
            removed_alt_products[(alk, alt)] += 1
        if fold_text(alk) == "joghurt" and fold_text(alt) in JOGHURT_ALT_REMOVALS:
            removed_alt_products[(alk, alt)] += 1
        if fold_text(alk) == "tej" and fold_text(alt) in TEJ_ALT_REMOVALS:
            removed_alt_products[(alk, alt)] += 1
        for prop_name in (product.get("tulajdonsagok") or {}):
            prop_counts[prop_name] += 1

    return {
        "missing_paths": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in missing_paths.most_common()
        ],
        "obsolete_alkategoria_products": [
            {"alkategoria": alk, "termek_db": count}
            for alk, count in obsolete_alk_products.most_common()
        ],
        "removed_alt_products": [
            {"alkategoria": alk, "altipus": alt, "termek_db": count}
            for (alk, alt), count in removed_alt_products.most_common()
        ],
        "termekcsalad_db": prop_counts.get("termékcsalád", 0),
        "toltott_db": prop_counts.get("töltött", 0),
        "milk_products": sum(1 for product in products if fold_text(product.get("fokategoria", "")) == TARGET_CATEGORY_FOLDED),
    }


def write_report(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# Tejtermékek első javítási iteráció",
        "",
        f"- Generálva: {payload['meta']['generated_at']}",
        f"- Mód: {payload['meta']['mode']}",
        f"- Termékmozgatások: {len(payload['product_moves'])}",
        f"- Tulajdonság-normalizálási lépések: {payload['property_changes']}",
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
            f"- Hiányzó kategóriaútvonalak: {len(validation['missing_paths'])}",
            f"- Törölt alkategória alatt maradt termékek: {len(validation['obsolete_alkategoria_products'])}",
            f"- Törölt altípus alatt maradt termékek: {len(validation['removed_alt_products'])}",
            f"- termékcsalád tulajdonság maradt: {validation['termekcsalad_db']}",
            f"- töltött tulajdonság maradt: {validation['toltott_db']}",
        ]
    )

    by_reason = Counter(move["ok"] for move in payload["product_moves"])
    lines.extend(["", "## Termékmozgatások ok szerint"])
    for reason, count in by_reason.most_common():
        lines.append(f"- {reason}: {count}")

    lines.extend(["", "## Termékmozgatások mintája"])
    for move in payload["product_moves"][:100]:
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

    product_moves, property_changes = route_products(products, alkategoriak)
    category_changes = cleanup_category_tree(category_node)
    validation = validate(products, category_node)

    payload = {
        "meta": {
            "generated_at": generated_at,
            "mode": "apply" if args.apply else "dry-run",
            "category_source": CATEGORY_PATH.name,
            "product_source": PRODUCT_PATH.name,
            "fokategoria": category_key,
        },
        "product_moves": product_moves,
        "property_changes": property_changes,
        "category_changes": category_changes,
        "validation": validation,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report_json = OUT_DIR / f"tejtermekek_elso_iteracio_{date_stamp}.json"
    report_md = OUT_DIR / f"tejtermekek_elso_iteracio_{date_stamp}.md"
    dump_json(report_json, payload)
    write_report(report_md, payload)

    failed = bool(
        validation["missing_paths"]
        or validation["obsolete_alkategoria_products"]
        or validation["removed_alt_products"]
        or validation["termekcsalad_db"]
        or validation["toltott_db"]
    )

    if args.apply:
        if failed:
            raise SystemExit("Validation failed; main files were not written.")
        dump_json(CATEGORY_PATH, categories)
        dump_json(PRODUCT_PATH, products)

    print(f"mode={'apply' if args.apply else 'dry-run'}")
    print(f"product_moves={len(product_moves)}")
    print(f"property_changes={property_changes}")
    print(f"category_changes={category_changes}")
    print(f"missing_paths={len(validation['missing_paths'])}")
    print(f"obsolete_alk_products={len(validation['obsolete_alkategoria_products'])}")
    print(f"removed_alt_products={len(validation['removed_alt_products'])}")
    print(f"termekcsalad_db={validation['termekcsalad_db']}")
    print(f"toltott_db={validation['toltott_db']}")
    print(f"report_json={report_json}")
    print(f"report_md={report_md}")


if __name__ == "__main__":
    main()
