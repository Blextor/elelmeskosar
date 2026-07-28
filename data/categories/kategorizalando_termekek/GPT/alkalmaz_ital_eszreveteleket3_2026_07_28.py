# -*- coding: utf-8 -*-
"""Az ``ital_eszrevetelek3.txt`` ellenőrzött alkoholosital-migrációja.

A program alapértelmezésben csak memóriában dolgozik. A ``--prepare-only``
kapcsoló külön jelölt JSON-fájlokat ír; a két fő JSON végleges cseréjét egy
külön PowerShell-finalizáló végzi.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable

import alkalmaz_italok_eszreveteleket_2026_07_25 as round1


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# A korábbi géphibánál a natív JSON-kódoló instabil volt. Az indentált,
# tisztán Pythonos út determinisztikus, és a round1 írója SHA-256-tal ellenőriz.
json.encoder.c_make_encoder = None


BASE = Path(__file__).resolve().parent
RESULT_PATH = BASE / "eredmeny.json"
CATEGORY_PATH = BASE / "kategoriak_2026-06-13.json"
DECISIONS_PATH = BASE / "ital_eszrevetelek3_dontesek_2026_07_28.json"
CHECKER_PATH = BASE / "ellenoriz_ital_eszreveteleket3_2026_07_28.py"
AUDIT_PATH = BASE / "ital_eszrevetelek3_audit_2026-07-28.json"
CANDIDATE_PRODUCTS_PATH = BASE / ".eredmeny.ital3-20260728.candidate.json"
CANDIDATE_CATEGORIES_PATH = BASE / ".kategoriak.ital3-20260728.candidate.json"

EXPECTED_TOTAL = 47030
ITAL = "Ital"
ALCOHOL = "Alkoholos italok és alkoholmentes alternatívák"
SOFT = "Üdítőitalok"
KIDS = "Kölyökpezsgő"
FUNCTIONAL = "Funkcionális italok"
SPORT = "Sport-, izotóniás, kollagén- és shot ital"
PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"

WINE = "Bor és boralapú ital"
SPARKLING = "Pezsgő, habzóbor és gyöngyözőbor"
BEER = "Sör, radler és malátaital"
CIDER = "Cider"
LIQUEUR = "Likőr"
WHISKY = "Whisky és bourbon"
GIN = "Gin"
RUM = "Rum"
TEQUILA = "Tequila"
VODKA = "Vodka"
PALINKA = "Pálinka"
BRANDY = "Brandy"
VERMOUTH = "Vermut és aperitif"
OTHER = "Egyéb szeszes ital"
COCKTAIL = "Koktél és előre kevert ital"

ALCOHOL_LEAVES = (
    WINE,
    SPARKLING,
    BEER,
    CIDER,
    LIQUEUR,
    WHISKY,
    GIN,
    RUM,
    TEQUILA,
    VODKA,
    PALINKA,
    BRANDY,
    VERMOUTH,
    OTHER,
    COCKTAIL,
)

# A ``shape`` értéke single/group/flag. A Sör és a Pezsgő ``fajta`` mezője
# szándékosan csoportos: a termékcsalád és a stílus külön, elemi címkék maradnak
# (például ["sör", "IPA"] vagy ["pezsgő", "prosecco"]).
SCHEMAS: dict[str, tuple[tuple[str, str], ...]] = {
    WHISKY: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("típus", "single"),
        ("íz", "group"),
        ("egységnyi kiszerelés", "group"),
    ),
    VODKA: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("egységnyi kiszerelés", "group"),
    ),
    VERMOUTH: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("édesség", "group"),
        ("szín", "group"),
        ("íz", "group"),
    ),
    TEQUILA: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("egységnyi kiszerelés", "group"),
    ),
    RUM: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("fajta", "group"),
    ),
    PALINKA: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("fajta", "group"),
    ),
    OTHER: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("fajta", "single"),
    ),
    LIQUEUR: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("fajta", "single"),
        ("gyógynövényes", "flag"),
        ("egységnyi kiszerelés", "group"),
    ),
    COCKTAIL: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("alkoholalap", "group"),
        ("fajta", "single"),
        ("szénsavasság", "single"),
    ),
    GIN: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("gyümölcsös", "flag"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("fajta", "single"),
        ("egységnyi kiszerelés", "group"),
    ),
    CIDER: (
        ("alkoholstátusz", "single"),
        ("csomagolás", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("egységnyi kiszerelés", "single"),
    ),
    BRANDY: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
    ),
    WINE: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("íz", "group"),
        ("szénsavasság", "single"),
        ("puttonyszám", "single"),
        ("csomagolás anyaga", "group"),
        ("szín", "group"),
        ("édesség", "group"),
        ("eredet", "group"),
        ("bortípus", "single"),
        ("egységnyi kiszerelés", "single"),
    ),
    SPARKLING: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("fajta", "group"),
        ("íz", "group"),
        ("egységnyi kiszerelés", "single"),
        ("szőlőfajta", "group"),
        ("eredet", "group"),
        ("édesség", "group"),
        ("szín", "group"),
    ),
    BEER: (
        ("alkoholstátusz", "single"),
        ("márka", "single"),
        ("kiszerelés", "single"),
        ("alkoholtartalom", "group"),
        ("fajta", "group"),
        ("íz", "group"),
        ("szín", "group"),
        ("egységnyi kiszerelés", "single"),
        ("csomagdarabszám", "single"),
        ("bio", "flag"),
        ("gluténmentes", "flag"),
        ("kézműves", "flag"),
        ("szűretlen", "flag"),
    ),
}


WHISKY_TYPE_ALIASES = {
    "skot whisky": "skót whisky",
    "scotch whisky": "skót whisky",
    "ir whiskey": "ír whisky",
    "irish whiskey": "ír whisky",
    "ir whisky": "ír whisky",
    "blended scotch whisky": "kevert skót whisky",
    "kevert skot whisky": "kevert skót whisky",
    "kevert skot whiskey": "kevert skót whisky",
    "tennessee whiskey": "Tennessee whisky",
    "tennessee whisky": "Tennessee whisky",
    "bourbon whiskey": "bourbon",
    "bourbon": "bourbon",
    "single malt scotch whisky": "single malt skót whisky",
    "islay single malt scotch whisky": "single malt skót whisky",
    "skot maltawhisky": "malátawhisky",
    "single malt skot whisky": "single malt skót whisky",
    "maltawhisky": "malátawhisky",
    "single malt whisky": "single malt whisky",
    "japan whisky": "japán whisky",
    "blended japan whisky": "kevert japán whisky",
    "kevert japan whisky": "kevert japán whisky",
    "kanadai whisky": "kanadai whisky",
    "blended whisky": "kevert whisky",
    "kevert whisky": "kevert whisky",
    "whisky": "egyéb whisky",
    "egyeb whisky": "egyéb whisky",
    "alkoholmentes whisky jellegu ital": "alkoholmentes whiskyjellegű ital",
    "alkoholmentes whiskyjellegu ital": "alkoholmentes whiskyjellegű ital",
}

GIN_TYPE_ALIASES = {
    "london dry gin": "London dry gin",
    "dry gin": "dry gin",
    "desztillalt gin": "desztillált gin",
    "izesitett gin": "ízesített gin",
    "pink gin": "ízesített gin",
    "alkoholmentes gin": "alkoholmentes ginjellegű ital",
    "alkoholmentes szeszesital": "alkoholmentes ginjellegű ital",
    "alkoholmentes ginjellegu ital": "alkoholmentes ginjellegű ital",
    "japan gin": "egyéb gin",
    "skot gin": "egyéb gin",
    "francia gin": "egyéb gin",
    "egyeb gin": "egyéb gin",
}

RUM_TYPE_ALIASES = {
    "barna": "barna",
    "sotet": "sötét",
    "gold": "arany",
    "arany": "arany",
    "feher": "fehér",
    "fuszeres": "fűszeres",
    "gyumolcsos": "ízesített",
    "izesitett": "ízesített",
    "rumalapu szeszesital": "rumalapú szeszesital",
    "alkoholmentes rum jellegu ital": "alkoholmentes rumjellegű ital",
    "sotet rum": "sötét",
    "arany rum": "arany",
    "feher rum": "fehér",
    "fuszeres rum": "fűszeres",
    "gyumolcsos rum": "ízesített",
    "alkoholmentes rumjellegu ital": "alkoholmentes rumjellegű ital",
    "rum": "egyéb rum",
    "egyeb rum": "egyéb rum",
}

PALINKA_TYPE_ALIASES = {
    "agyas palinka": "ágyas pálinka",
    "gyumolcspalinka": "gyümölcspálinka",
    "torkolypalinka": "törkölypálinka",
    "erlelt palinka": "érlelt pálinka",
    "palinka": "gyümölcspálinka",
}

LIQUEUR_TYPE_ALIASES = {
    "gyogynovenylikor": "keserűlikőr",
    "kremlikor": "krémlikőr",
    "gyumolcslikor": "gyümölcslikőr",
    "keserulikor": "keserűlikőr",
    "tea likor": "tealikőr",
    "tealikor": "tealikőr",
    "whiskey likor": "whiskyalapú likőr",
    "whisky likor": "whiskyalapú likőr",
    "whiskylikor": "whiskyalapú likőr",
    "whiskyalapu likor": "whiskyalapú likőr",
    "gyomorkeseru": "keserűlikőr",
    "csokolade likor": "csokoládélikőr",
    "csokoladelikor": "csokoládélikőr",
    "maklikor": "máklikőr",
    "rumalapu likor": "rumalapú likőr",
    "rumlikor": "rumalapú likőr",
    "karamellalikor": "egyéb likőr",
    "karamelllikor": "egyéb likőr",
    "tojaslikor": "tojáslikőr",
    "gin likor": "ginalapú likőr",
    "ginlikor": "ginalapú likőr",
    "ginalapu likor": "ginalapú likőr",
    "diolikor": "diólikőr",
    "kavelikor": "kávélikőr",
    "amaretto": "amaretto",
    "triple sec": "triple sec",
    "narancslikor": "triple sec",
    "sambuca": "sambuca",
    "limoncello": "limoncello",
    "curacao": "curaçao",
    "tequilaalapu likor": "tequilaalapú likőr",
    "likor": "egyéb likőr",
    "egyeb likor": "egyéb likőr",
}

OTHER_TYPE_ALIASES = {
    "abszint": "abszint",
    "ouzo": "ouzo",
    "pastis": "pastis",
    "soju": "soju",
    "grappa": "grappa",
    "torkolypalinka": "grappa",
    "torkolylat": "grappa",
    "cachaca": "cachaça",
    "gyumolcsparlat": "gyümölcspárlat",
    "gyumolcsos": "gyümölcsízű szeszesital",
    "gyumolcslikor": "gyümölcsízű szeszesital",
    "izesitett whisky alapu szeszesital": "whiskyalapú szeszesital",
    "whisky alapu szeszesital": "whiskyalapú szeszesital",
    "whiskyalapu szeszesital": "whiskyalapú szeszesital",
    "rumalapu szeszesital": "rumalapú szeszesital",
    "rumizu szeszesital": "rumízű szeszesital",
    "brandyjellegu szeszesital": "brandyízű szeszesital",
    "brandyizu szeszesital": "brandyízű szeszesital",
    "vodkaalapu szeszesital": "vodkaízű szeszesital",
    "vodkaizu szeszesital": "vodkaízű szeszesital",
    "palinkaizu szeszesital": "pálinkaízű szeszesital",
    "aromasitott": "egyéb ízesített szeszesital",
    "fuszeres": "rumalapú szeszesital",
    "egyeb szeszes ital": "egyéb szeszesital",
    "egyeb szeszesital": "egyéb szeszesital",
}

SWEETNESS_ALIASES = {
    "extra dry": "különlegesen száraz",
    "extra szaraz": "különlegesen száraz",
    "kulonleges szaraz": "különlegesen száraz",
    "secco": "száraz",
    "dry": "száraz",
    "doux": "édes",
    "sweet": "édes",
    "semi dry": "félszáraz",
}

VERMOUTH_SWEETNESS_ALIASES = {
    **SWEETNESS_ALIASES,
    "extra dry": "extra száraz",
    "extra szaraz": "extra száraz",
}

COLOR_ALIASES = {
    "rose": "rozé",
    "roze": "rozé",
    "rosato": "rozé",
    "bianco": "fehér",
    "white": "fehér",
    "rouge": "vörös",
    "red": "vörös",
}

FLAVOR_ALIASES = {
    "apple": "alma",
    "sour cherry": "meggy",
    "cherry": "cseresznye",
    "orange": "narancs",
    "blood orange": "vérnarancs",
    "red berry": "vörös bogyós gyümölcs",
    "mixed fruit": "vegyes gyümölcs",
    "berry": "erdei gyümölcs",
    "berry kiss": "erdei gyümölcs",
    "pink strawberry": "eper",
    "purple hibiscus": "hibiszkusz",
    "bison grass": "bölényfű",
    "pear": "körte",
    "smoky": "füstös",
    "mogyoro": "földimogyoró",
    "birsalma": "birs",
    "kajszi": "sárgabarack",
    "torkoly": "szőlő",
    "vegyes": "vegyes gyümölcs",
    "eperizu": "eper",
    "feketeribizli": "fekete ribizli",
    "granat": "gránátalma",
    "tropusi": "trópusi gyümölcs",
    "japanese blossom": "cseresznyevirág",
    "sakura": "cseresznyevirág",
    "harsfavirag": "hárs",
    "honey": "méz",
    "ir krem": "tejszín",
    "tejkrem": "tejszín",
    "jack apple": "alma",
    "jack fire": "fahéj",
    "jack honey": "méz",
    "amaretto": "mandula",
    "blue curacao": "narancs",
    "brown cacao": "csokoládé",
    "cherry brandy": "cseresznye",
    "cioccolato": "csokoládé",
    "limoncello": "citrom",
    "sambuca": "ánizs",
    "tojasos": "tojás",
    "mojito": ["lime", "menta"],
    "orange bitter": "keserűnarancs",
    "orange dark": ["narancs", "csokoládé"],
    "sauer apfel": "alma",
    "triple sec": "narancs",
    "tropical chilli": ["trópusi gyümölcs", "chili"],
    "tropical flirt": "trópusi gyümölcs",
    "tuttifrutti": "tutti-frutti",
    "tutti frutti": "tutti-frutti",
    "tropusi gyumolcs": "trópusi gyümölcs",
    "vegyes gyumolcs": "vegyes gyümölcs",
    "citrus dry": "citrus",
    "lemon mint": ["citrom", "menta"],
    "sweet honey": "méz",
    "watermelon": "görögdinnye",
    "wild cherry": "cseresznye",
    "spiced": "fűszer",
    "spiced gold": "fűszer",
    "black spiced": "fűszer",
    "caribbean spiced": "fűszer",
    "fuszeres": "fűszer",
    "ouzo": "ánizs",
}


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


def fold(value: Any) -> str:
    return round1.fold_text(value)


def dedupe(values: Iterable[Any]) -> list[Any]:
    return round1.dedupe(values)


def first(value: Any) -> Any:
    vals = values_of(value)
    return vals[0] if vals else None


def load_decisions(path: Path) -> dict[str, Any]:
    decisions = round1.load_json(path)
    if not isinstance(decisions, dict):
        raise RuntimeError("A döntésfájl gyökere nem objektum")
    expected = {
        "move_path_by_id",
        "brand_by_id",
        "brand_groups",
        "property_overrides_by_id",
        "property_groups",
        "fajta_groups",
        "brand_aliases",
        "value_aliases",
        "flavor_drop_by_leaf",
    }
    missing = expected - set(decisions)
    if missing:
        raise RuntimeError(f"Hiányos döntésfájl: {sorted(missing)}")
    expanded_props = copy.deepcopy(decisions.get("property_overrides_by_id") or {})
    for group_index, group in enumerate(decisions.get("property_groups") or []):
        if not isinstance(group, dict):
            raise RuntimeError(f"Hibás property_groups[{group_index}]")
        ids = group.get("ids") or []
        assignments = group.get("set")
        if assignments is None:
            name = str(group.get("property") or "")
            assignments = {name: group.get("value")} if name else {}
        if (
            not isinstance(assignments, dict)
            or not assignments
            or not isinstance(ids, list)
            or not ids
        ):
            raise RuntimeError(f"Hiányos property_groups[{group_index}]")
        for iid in ids:
            target = expanded_props.setdefault(str(iid), {})
            for name, value in assignments.items():
                if name in target and target[name] != value:
                    raise RuntimeError(
                        f"Ütköző csoportos felülírás: {iid}/{name}: "
                        f"{target[name]!r} != {value!r}"
                    )
                target[name] = copy.deepcopy(value)
    for leaf, value_groups in (decisions.get("fajta_groups") or {}).items():
        if leaf not in {LIQUEUR, OTHER} or not isinstance(value_groups, dict):
            raise RuntimeError(f"Hibás fajta_groups ág: {leaf!r}")
        for value, ids in value_groups.items():
            if not isinstance(value, str) or not value or not isinstance(ids, list) or not ids:
                raise RuntimeError(f"Hibás fajta_groups csoport: {leaf!r}/{value!r}")
            for iid in ids:
                iid = str(iid)
                target = expanded_props.setdefault(iid, {})
                if "fajta" in target and target["fajta"] != value:
                    raise RuntimeError(
                        f"Ütköző fajta_groups felülírás: {iid}: "
                        f"{target['fajta']!r} != {value!r}"
                    )
                target["fajta"] = value
    decisions["_expanded_property_overrides"] = expanded_props

    expanded_brands = dict(decisions.get("brand_by_id") or {})
    for group_index, group in enumerate(decisions.get("brand_groups") or []):
        if not isinstance(group, dict) or not group.get("brand") or not group.get("ids"):
            raise RuntimeError(f"Hibás brand_groups[{group_index}]")
        for iid in group["ids"]:
            iid = str(iid)
            brand = str(group["brand"])
            if iid in expanded_brands and expanded_brands[iid] != brand:
                raise RuntimeError(
                    f"Ütköző csoportos márka: {iid}: "
                    f"{expanded_brands[iid]!r} != {brand!r}"
                )
            expanded_brands[iid] = brand
    decisions["_expanded_brand_by_id"] = expanded_brands
    decisions["_folded_brand_aliases"] = {
        fold(key): value
        for key, value in (decisions.get("brand_aliases") or {}).items()
    }
    decisions["_folded_flavor_aliases"] = {
        **FLAVOR_ALIASES,
        **{
            fold(key): value
            for key, value in (
                decisions.get("value_aliases", {}).get("íz", {}) or {}
            ).items()
        },
    }
    decisions["_folded_flavor_drop_by_leaf"] = {
        leaf: {fold(value) for value in values}
        for leaf, values in (decisions.get("flavor_drop_by_leaf") or {}).items()
    }
    return decisions


def decimal_text(value: Decimal) -> str:
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text.replace(".", ",")


def canonical_size(value: Any) -> str:
    raw = str(first(value) or "").strip()
    if not raw or fold(raw) in {"egyeb", "ismeretlen", "nem azonosithato"}:
        return "ismeretlen"
    compact = re.sub(r"\s+", "", raw.casefold()).replace(",", ".")
    match = re.fullmatch(r"(\d+(?:\.\d+)?)(ml|cl|dl|l)", compact)
    if not match:
        return "ismeretlen"
    number = Decimal(match.group(1))
    factor = {"ml": Decimal(1), "cl": Decimal(10), "dl": Decimal(100), "l": Decimal(1000)}
    milliliters = number * factor[match.group(2)]
    return f"{decimal_text(milliliters)} ml"


def canonical_size_group(value: Any, fallback: str) -> list[str]:
    sizes = [
        canonical_size(raw)
        for raw in values_of(value)
        if raw not in (None, "")
    ]
    sizes = [size for size in sizes if size != "ismeretlen"]
    return dedupe(sizes) or [fallback]


def canonical_abv(value: Any) -> list[str]:
    result: list[str] = []
    for raw in values_of(value):
        text = str(raw).strip()
        if fold(text) in {"egyeb", "ismeretlen", "nem azonosithato"}:
            result.append("ismeretlen")
            continue
        match = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*%\s*", text)
        if not match:
            result.append("ismeretlen")
            continue
        try:
            number = Decimal(match.group(1).replace(",", "."))
        except InvalidOperation:
            result.append("ismeretlen")
            continue
        result.append(f"{decimal_text(number)}%")
    return dedupe(result) or ["ismeretlen"]


def canonical_scalar(
    value: Any,
    *,
    aliases: dict[str, str] | None = None,
    default: str = "egyéb",
) -> str:
    raw = str(first(value) or "").strip()
    if not raw:
        return default
    return (aliases or {}).get(fold(raw), raw)


def canonical_group(
    value: Any,
    *,
    aliases: dict[str, str | list[str]] | None = None,
    default: str = "egyéb",
) -> list[str]:
    result: list[str] = []
    for raw in values_of(value):
        text = str(raw).strip()
        if not text:
            continue
        mapped = (aliases or {}).get(fold(text), text)
        result.extend(str(item).strip() for item in values_of(mapped) if str(item).strip())
    return dedupe(result) or [default]


def canonical_flavors(
    old: dict[str, Any],
    leaf: str,
    decisions: dict[str, Any],
) -> list[str]:
    drop = decisions.get("_folded_flavor_drop_by_leaf", {}).get(leaf, set())
    result: list[str] = []
    aliases = decisions.get("_folded_flavor_aliases") or FLAVOR_ALIASES
    for raw in values_of(old.get("íz")):
        raw_text = str(raw).strip()
        raw_key = fold(raw_text)
        if not raw_text or raw_key in drop:
            continue
        if raw_key in aliases:
            mapped = aliases[raw_key]
            result.extend(str(value) for value in values_of(mapped))
            continue
        for atom in round1.flavor_atoms([raw_text]):
            if fold(atom) in drop:
                continue
            mapped = aliases.get(fold(atom), str(atom).casefold())
            result.extend(str(value) for value in values_of(mapped))
    result = dedupe(result)

    # Ezek terméktípus-/marketingjelzők, nem önálló ízek. A célágankénti
    # eltávolítás megakadályozza, hogy például a ``bitter`` vagy a
    # ``hidegkomlós`` az ízértékek közé szivárogjon.
    leaf_specific_non_flavors = {
        LIQUEUR: {
            "bitter",
            "elixir",
            "keserű",
            "macaron",
            "velvet",
        },
        VERMOUTH: {"aperitivo", "bitter", "keserű", "keserűlikőr"},
        OTHER: {"cachaça"},
        BEER: {"hidegkomlós"},
    }
    forbidden = {
        fold(value) for value in leaf_specific_non_flavors.get(leaf, set())
    }
    result = [value for value in result if fold(value) not in forbidden]
    if leaf == LIQUEUR:
        result = [
            "gyógynövény" if fold(value) == "erdei gyogynoveny" else value
            for value in result
        ]
        if {"sós", "karamell"}.issubset(set(result)):
            result = [
                value for value in result if value not in {"sós", "karamell"}
            ]
            result.append("sós karamell")
    return dedupe(result) or ["natúr"]


def canonical_brand(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> str:
    iid = item_id(product)
    override = decisions.get("_expanded_brand_by_id", {}).get(iid)
    if override:
        return str(override)
    raw = first(old.get("márka"))
    if not raw:
        raw = (product.get("termek") or {}).get("brand_name")
    text = str(raw or "").strip()
    aliases = decisions.get("_folded_brand_aliases") or {}
    return str(aliases.get(fold(text), text or "márka nélkül"))


def canonical_status(old: dict[str, Any]) -> str:
    raw = fold(first(old.get("alkoholstátusz")))
    if raw == "alkoholmentes":
        return "alkoholmentes"
    return "alkoholos"


def base_common(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    size = canonical_size(old.get("kiszerelés"))
    unit = canonical_size(old.get("egységnyi kiszerelés"))
    if unit in {"egyéb", "ismeretlen"}:
        unit = size
    unit_group = canonical_size_group(old.get("egységnyi kiszerelés"), size)
    return {
        "alkoholstátusz": canonical_status(old),
        "márka": canonical_brand(product, old, decisions),
        "kiszerelés": size,
        "alkoholtartalom": canonical_abv(old.get("alkoholtartalom")),
        "egységnyi kiszerelés": unit,
        "egységnyi kiszerelések": unit_group,
    }


def first_mapped(
    old: dict[str, Any],
    fields: Iterable[str],
    aliases: dict[str, str],
    default: str,
) -> str:
    for field in fields:
        for value in values_of(old.get(field)):
            mapped = aliases.get(fold(value))
            if mapped:
                return mapped
    return default


def all_mapped(
    old: dict[str, Any],
    fields: Iterable[str],
    aliases: dict[str, str | list[str]],
    default: str,
) -> list[str]:
    result: list[str] = []
    for field in fields:
        for value in values_of(old.get(field)):
            mapped = aliases.get(fold(value))
            if mapped is not None:
                result.extend(str(item) for item in values_of(mapped))
    return dedupe(result) or [default]


def apply_overrides(
    product: dict[str, Any],
    props: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    override = (decisions.get("_expanded_property_overrides") or {}).get(item_id(product)) or {}
    result = dict(props)
    for key, value in override.items():
        result[key] = copy.deepcopy(value)
    return result


def ordered_props(leaf: str, props: dict[str, Any]) -> dict[str, Any]:
    expected = SCHEMAS[leaf]
    expected_keys = {name for name, _ in expected}
    unknown = set(props) - expected_keys
    missing = expected_keys - set(props)
    if unknown or missing:
        raise RuntimeError(
            f"Sémahiba ({leaf}): hiány={sorted(missing)}, váratlan={sorted(unknown)}"
        )
    result: dict[str, Any] = {}
    for name, shape in expected:
        value = props[name]
        if shape == "flag" and not isinstance(value, bool):
            raise RuntimeError(f"Nem logikai {leaf}/{name}: {value!r}")
        if shape == "group" and (not isinstance(value, list) or not value):
            raise RuntimeError(f"Nem kitöltött csoportos {leaf}/{name}: {value!r}")
        if shape == "single" and (
            isinstance(value, (list, dict, bool)) or value is None or value == ""
        ):
            raise RuntimeError(f"Nem kitöltött egyedi {leaf}/{name}: {value!r}")
        result[name] = value
    return result


def normalize_whisky(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "típus": first_mapped(
            old,
            ("típus",),
            WHISKY_TYPE_ALIASES,
            "egyéb whisky",
        ),
        "íz": canonical_flavors(old, WHISKY, decisions),
        "egységnyi kiszerelés": common["egységnyi kiszerelések"],
    }
    return ordered_props(WHISKY, apply_overrides(product, props, decisions))


def normalize_vodka(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, VODKA, decisions),
        "egységnyi kiszerelés": common["egységnyi kiszerelések"],
    }
    return ordered_props(VODKA, apply_overrides(product, props, decisions))


def normalize_vermouth(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    sweetness = canonical_group(
        old.get("édesség"),
        aliases=VERMOUTH_SWEETNESS_ALIASES,
    )
    if "extra száraz" in sweetness:
        sweetness = [value for value in sweetness if value != "száraz"]
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "édesség": sweetness,
        "szín": canonical_group(old.get("szín"), aliases=COLOR_ALIASES),
        "íz": canonical_flavors(old, VERMOUTH, decisions),
    }
    return ordered_props(VERMOUTH, apply_overrides(product, props, decisions))


def normalize_tequila(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, TEQUILA, decisions),
        "egységnyi kiszerelés": common["egységnyi kiszerelések"],
    }
    return ordered_props(TEQUILA, apply_overrides(product, props, decisions))


def normalize_rum(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    rum_type = all_mapped(
        old,
        ("fajta", "típus"),
        RUM_TYPE_ALIASES,
        "egyéb rum",
    )
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, RUM, decisions),
        "fajta": rum_type,
    }
    return ordered_props(RUM, apply_overrides(product, props, decisions))


def normalize_palinka(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    palinka_type = all_mapped(
        old,
        ("fajta",),
        PALINKA_TYPE_ALIASES,
        "gyümölcspálinka",
    )
    if (
        "ágyas pálinka" in palinka_type
        and "gyümölcspálinka" not in palinka_type
    ):
        palinka_type.append("gyümölcspálinka")
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, PALINKA, decisions),
        "fajta": palinka_type,
    }
    return ordered_props(PALINKA, apply_overrides(product, props, decisions))


def normalize_other(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
    source_leaf: str,
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    source_default = {
        RUM: "rumalapú szeszesital",
        WHISKY: "whiskyalapú szeszesital",
        VODKA: "vodkaízű szeszesital",
        BRANDY: "brandyízű szeszesital",
        PALINKA: "pálinkaízű szeszesital",
    }.get(source_leaf)
    if source_default is not None:
        current_type = source_default
    else:
        current_type = first_mapped(
            old,
            ("fajta", "terméktípus", "típus", "alkoholalap"),
            OTHER_TYPE_ALIASES,
            "egyéb szeszesital",
        )
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, OTHER, decisions),
        "fajta": current_type,
    }
    return ordered_props(OTHER, apply_overrides(product, props, decisions))


def normalize_liqueur(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
    source_leaf: str,
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    liqueur_type = first_mapped(
        old,
        ("fajta", "terméktípus"),
        LIQUEUR_TYPE_ALIASES,
        "whiskyalapú likőr" if source_leaf == WHISKY else "egyéb likőr",
    )
    herbal_types = {"keserűlikőr"}
    herbal = round1.bool_value(old.get("gyógynövényes")) or liqueur_type in herbal_types
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, LIQUEUR, decisions),
        "fajta": liqueur_type,
        "gyógynövényes": herbal,
        "egységnyi kiszerelés": common["egységnyi kiszerelések"],
    }
    props = apply_overrides(product, props, decisions)
    explicit = decisions.get("_expanded_property_overrides", {}).get(
        item_id(product),
        {},
    )
    if "gyógynövényes" not in explicit and props["fajta"] in herbal_types:
        props["gyógynövényes"] = True
    return ordered_props(LIQUEUR, props)


COCKTAIL_TYPE_ALIASES = {
    "ready to drink": "előre kevert ital",
    "gin tonic": "gin-tonik",
    "moscow mule": "Moscow Mule",
    "koktel": "egyéb koktél",
    "tequila sunrise cocktail": "Tequila Sunrise",
    "mojito cocktail": "Mojito",
    "sex on the beach cocktail": "Sex on the Beach",
    "pina colada cocktail": "Piña Colada",
}

ALCOHOL_BASE_ALIASES = {
    "whiskey": "whisky",
    "aperitiv": "aperitív",
}


def normalize_cocktail(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    cocktail_type = canonical_scalar(
        old.get("fajta"),
        aliases=COCKTAIL_TYPE_ALIASES,
        default="egyéb koktél",
    )
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "alkoholalap": canonical_group(
            old.get("alkoholalap"),
            aliases=ALCOHOL_BASE_ALIASES,
        ),
        "fajta": cocktail_type,
        "szénsavasság": canonical_scalar(
            old.get("szénsavasság"),
            default="szénsavas",
        ),
    }
    return ordered_props(COCKTAIL, apply_overrides(product, props, decisions))


def normalize_gin(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    gin_type = first_mapped(old, ("fajta", "típus"), GIN_TYPE_ALIASES, "egyéb gin")
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "gyümölcsös": round1.bool_value(old.get("gyümölcsös")),
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, GIN, decisions),
        "fajta": gin_type,
        "egységnyi kiszerelés": common["egységnyi kiszerelések"],
    }
    return ordered_props(GIN, apply_overrides(product, props, decisions))


def normalize_cider(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    packaging_values = {fold(value) for value in values_of(old.get("csomagolás"))}
    packaging = "doboz" if "doboz" in packaging_values else "palack"
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "csomagolás": packaging,
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, CIDER, decisions),
        "egységnyi kiszerelés": common["egységnyi kiszerelés"],
    }
    return ordered_props(CIDER, apply_overrides(product, props, decisions))


def normalize_brandy(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, BRANDY, decisions),
    }
    return ordered_props(BRANDY, apply_overrides(product, props, decisions))


def wine_type(old: dict[str, Any]) -> str:
    values = [
        fold(value)
        for field in ("bortípus", "típus", "fajta", "borstílus")
        for value in values_of(old.get(field))
    ]
    joined = " | ".join(values)
    priorities = (
        ("hugo", "hugo"),
        ("forralt bor", "forralt bor"),
        ("sangria", "sangria"),
        ("gyumolcsbor", "gyümölcsbor"),
        ("likorbor", "likőrbor"),
        ("portoi", "likőrbor"),
        ("sherry", "likőrbor"),
        ("izesitett boralapu ital", "ízesített boralapú ital"),
        ("izesitett bor", "ízesített bor"),
        ("boralapu koktel", "boralapú koktél"),
        ("pezsgokoktel", "boralapú koktél"),
        ("borkoktel", "boralapú koktél"),
        ("spritz", "boralapú koktél"),
        ("koktel", "boralapú koktél"),
        ("boralapu ital", "boralapú ital"),
    )
    for marker, target in priorities:
        if marker in joined:
            return target
    if canonical_status(old) == "alkoholmentes":
        return "alkoholmentes bor"
    return "bor"


def normalize_wine(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    raw_puttony = first(old.get("puttonyszám"))
    puttony = "nem alkalmazható"
    if raw_puttony not in (None, ""):
        number = re.sub(r"\D+", "", str(raw_puttony))
        puttony = f"{number} puttonyos" if number else "nem alkalmazható"
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "íz": canonical_flavors(old, WINE, decisions),
        "szénsavasság": canonical_scalar(
            old.get("szénsavasság"),
            default="szénsavmentes",
        ),
        "puttonyszám": puttony,
        "csomagolás anyaga": canonical_group(old.get("csomagolás anyaga")),
        "szín": canonical_group(old.get("szín"), aliases=COLOR_ALIASES),
        "édesség": canonical_group(
            old.get("édesség"),
            aliases=SWEETNESS_ALIASES,
        ),
        "eredet": canonical_group(old.get("eredet")),
        "bortípus": wine_type(old),
        "egységnyi kiszerelés": common["egységnyi kiszerelés"],
    }
    return ordered_props(WINE, apply_overrides(product, props, decisions))


SPARKLING_STYLE_ALIASES = {
    "champagne": "champagne",
    "cremant": "crémant",
    "prosecco": "prosecco",
    "spumante": "spumante",
}

GRAPE_ALIASES = {
    "moscato": "Muskotály",
    "muscateller": "Muskotály",
    "muscat": "Muskotály",
    "muskotaly": "Muskotály",
    "irsai": "Irsai Olivér",
    "irsai oliver": "Irsai Olivér",
    "chardonnay": "Chardonnay",
}


def sparkling_tags(old: dict[str, Any]) -> list[str]:
    existing = [
        str(value)
        for value in values_of(old.get("fajta"))
        if fold(value)
        in {
            "pezsgo",
            "habzobor",
            "gyongyozobor",
            "alkoholmentes habzo ital",
            "champagne",
            "cremant",
            "prosecco",
            "spumante",
        }
    ]
    if existing and "bortípus" not in old and "típus" not in old:
        return dedupe(existing)
    raw_type = [fold(value) for value in values_of(old.get("bortípus"))]
    raw_other = [
        fold(value)
        for field in ("típus", "fajta")
        for value in values_of(old.get(field))
    ]
    all_values = raw_type + raw_other
    if any(value in {"gyongyozobor", "gyongybor", "frizzante"} for value in all_values):
        base = "gyöngyözőbor"
    elif any(
        value in {"habzobor", "borbol keszult habzo ital"}
        for value in all_values
    ):
        base = "habzóbor"
    elif any(
        value in {"alkoholmentes habzo ital", "alkoholmentes pezsgo"}
        for value in all_values
    ):
        base = "alkoholmentes habzó ital"
    else:
        base = "pezsgő"
    styles = [
        SPARKLING_STYLE_ALIASES[value]
        for value in all_values
        if value in SPARKLING_STYLE_ALIASES
    ]
    return dedupe([base, *styles])


def sparkling_grapes(old: dict[str, Any]) -> list[str]:
    grapes = canonical_group(old.get("szőlőfajta"), aliases=GRAPE_ALIASES, default="")
    if grapes == [""]:
        grapes = []
    for field in ("típus", "fajta", "íz"):
        for value in values_of(old.get(field)):
            mapped = GRAPE_ALIASES.get(fold(value))
            if mapped:
                grapes.append(mapped)
    return dedupe(grapes) or ["egyéb"]


def sparkling_sweetness(old: dict[str, Any]) -> list[str]:
    raw = list(values_of(old.get("édesség")))
    sweetness_markers = {
        "brut",
        "brut nature",
        "extra brut",
        "extra dry",
        "extra szaraz",
        "kulonleges szaraz",
        "szaraz",
        "felszaraz",
        "feledes",
        "edes",
        "doux",
        "secco",
        "dry",
    }
    for field in ("típus", "fajta", "íz"):
        raw.extend(
            value
            for value in values_of(old.get(field))
            if fold(value) in sweetness_markers
        )
    result = canonical_group(raw, aliases=SWEETNESS_ALIASES)
    # A pezsgőknél ezek külön jogi maradékcukor-kategóriák. Ha a régi
    # mezőkben az általánosabb és a pontosabb címke is szerepelt, csak a
    # pontosabbat tartjuk meg.
    if "brut nature" in result:
        result = [
            value for value in result if value not in {"brut", "extra brut"}
        ]
    elif "extra brut" in result:
        result = [value for value in result if value != "brut"]
    if "különlegesen száraz" in result:
        result = [value for value in result if value != "száraz"]
    return dedupe(result)


def sparkling_color(old: dict[str, Any]) -> list[str]:
    raw = list(values_of(old.get("szín")))
    for field in ("típus", "fajta"):
        raw.extend(
            value
            for value in values_of(old.get(field))
            if fold(value) in COLOR_ALIASES
        )
    return canonical_group(raw, aliases=COLOR_ALIASES)


def normalize_sparkling(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "fajta": sparkling_tags(old),
        "íz": canonical_flavors(old, SPARKLING, decisions),
        "egységnyi kiszerelés": common["egységnyi kiszerelés"],
        "szőlőfajta": sparkling_grapes(old),
        "eredet": canonical_group(old.get("eredet")),
        "édesség": sparkling_sweetness(old),
        "szín": sparkling_color(old),
    }
    return ordered_props(SPARKLING, apply_overrides(product, props, decisions))


BEER_STYLE_ALIASES = {
    "sor": "sör",
    "sorvalogatas": "sör",
    "radler": "radler",
    "malataital": "malátaital",
    "buzasor": "búzasör",
    "ipa": "IPA",
    "apa": "APA",
    "lager": "lager",
    "premium lager": "lager",
    "pils": "pilsner",
    "pilsner": "pilsner",
    "ale": "ale",
    "lambic": "lambic",
    "new england ipa": "New England IPA",
    "session ipa": "Session IPA",
    "india pale lager": "India pale lager",
    "sorkulonlegesseg": "sörkülönlegesség",
    "felsoerjesztesu sor": "ale",
    "tropical ale": "ale",
    "golden ale": "ale",
    "buza": "búzasör",
    "blanc": "búzasör",
    "weissbier": "búzasör",
    "white": "búzasör",
    "wit beer": "búzasör",
    "witbier": "búzasör",
    "hefe trub": "búzasör",
    "double west coast ipa": "double IPA",
    "dupla ipa": "double IPA",
    "india pale ale": "IPA",
    "punk ipa": "IPA",
    "dark lager": "lager",
    "cerne": "lager",
    "cerny": "lager",
    "genuine draft": "lager",
    "pilsener": "pilsner",
    "pilseni": "pilsner",
    "premium pils": "pilsner",
    "majdnem pilsner": "pilsner",
    "draught stout": "stout",
    "oatmeal stout": "stout",
    "kriek": "lambic",
    "west coast ipa": "West Coast IPA",
    "double ipa": "double IPA",
    "black ipa": "black IPA",
    "sour ipa": "sour IPA",
    "porter": "porter",
    "stout": "stout",
    "bak": "bak",
    "helles": "helles",
    "dunkel": "dunkel",
    "kellerbier": "kellerbier",
    "blond": "belga blond",
    "blonde": "belga blond",
    "dubbel": "dubbel",
    "tripel": "tripel",
    "quadrupel": "quadrupel",
}


def beer_tags(old: dict[str, Any]) -> list[str]:
    existing = [str(value) for value in values_of(old.get("fajta"))]
    if existing and "terméktípus" not in old and "sörtípus" not in old:
        return dedupe(existing)
    raw_product = [fold(value) for value in values_of(old.get("terméktípus"))]
    raw_style = [
        fold(value)
        for field in ("sörtípus", "íz")
        for value in values_of(old.get(field))
    ]
    if "radler" in raw_product or "radler" in raw_style:
        base = "radler"
    elif "malataital" in raw_product or "malataital" in raw_style:
        base = "malátaital"
    else:
        base = "sör"
    styles = [
        BEER_STYLE_ALIASES[value]
        for value in raw_style
        if value in BEER_STYLE_ALIASES
        and BEER_STYLE_ALIASES[value] not in {"sör", "radler", "malátaital"}
    ]
    if base in {"radler", "malátaital"}:
        return [base]
    # A ``sör`` a termékcsalád, a további elemek stílusok. Így a generikus
    # sör sem kényszerül ``egyéb`` értékre, és az IPA/lager jelző sem kerül
    # az íz mezőbe.
    return dedupe(["sör", *styles])


def normalize_beer(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    common = base_common(product, old, decisions)
    colors = canonical_group(old.get("szín"), aliases=COLOR_ALIASES)
    colors = ["világos" if fold(value) == "feher" else value for value in colors]
    colors = ["világos" if fold(value) == "roze" else value for value in colors]
    color_from_style = {
        "amber": "borostyán",
        "felbarna ipa": "borostyán",
        "ruby": "vörös",
        "green": "zöld",
        "dark": "barna",
        "dark lager": "barna",
        "brune": "barna",
        "cerne": "barna",
        "cerny": "barna",
        "dunkel": "barna",
        "black ipa": "fekete",
        "stout": "fekete",
        "draught stout": "fekete",
        "oatmeal stout": "fekete",
    }
    raw_flavor_tokens = [fold(value) for value in values_of(old.get("íz"))]
    inferred_colors = [
        color_from_style[value]
        for value in raw_flavor_tokens
        if value in color_from_style
    ]
    if colors == ["egyéb"] and inferred_colors:
        colors = inferred_colors
    raw_count = first(old.get("csomagdarabszám"))
    try:
        package_count = int(raw_count) if raw_count not in (None, "") else 1
    except (TypeError, ValueError):
        package_count = 1
    props = {
        "alkoholstátusz": common["alkoholstátusz"],
        "márka": common["márka"],
        "kiszerelés": common["kiszerelés"],
        "alkoholtartalom": common["alkoholtartalom"],
        "fajta": beer_tags(old),
        "íz": canonical_flavors(old, BEER, decisions),
        "szín": dedupe(colors) or ["egyéb"],
        "egységnyi kiszerelés": common["egységnyi kiszerelés"],
        "csomagdarabszám": max(package_count, 1),
        "bio": round1.bool_value(old.get("bio")),
        "gluténmentes": round1.bool_value(old.get("gluténmentes")),
        "kézműves": round1.bool_value(old.get("kézműves")),
        "szűretlen": round1.bool_value(old.get("szűretlen")),
    }
    return ordered_props(BEER, apply_overrides(product, props, decisions))


NORMALIZERS = {
    WHISKY: normalize_whisky,
    VODKA: normalize_vodka,
    VERMOUTH: normalize_vermouth,
    TEQUILA: normalize_tequila,
    RUM: normalize_rum,
    PALINKA: normalize_palinka,
    COCKTAIL: normalize_cocktail,
    GIN: normalize_gin,
    CIDER: normalize_cider,
    BRANDY: normalize_brandy,
    WINE: normalize_wine,
    SPARKLING: normalize_sparkling,
    BEER: normalize_beer,
}


def normalize_kids_drink(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    props = {
        "márka": canonical_brand(product, old, decisions),
        "íz": canonical_flavors(old, KIDS, decisions),
        "szénsavas": True,
        "energiatartalom": "normál",
    }
    override = (decisions.get("_expanded_property_overrides") or {}).get(item_id(product)) or {}
    for key, value in override.items():
        props[key] = copy.deepcopy(value)
    expected = {"márka", "íz", "szénsavas", "energiatartalom"}
    if set(props) != expected or not props["íz"]:
        raise RuntimeError(f"Hibás Kölyökpezsgő-séma: {item_id(product)}")
    return props


def normalize_functional_drink(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
) -> dict[str, Any]:
    props = {
        "márka": canonical_brand(product, old, decisions),
        "íz": canonical_flavors(old, SPORT, decisions),
        "funkció": ["funkcionális ital"],
    }
    override = (decisions.get("_expanded_property_overrides") or {}).get(item_id(product)) or {}
    for key, value in override.items():
        props[key] = copy.deepcopy(value)
    expected = {"márka", "íz", "funkció"}
    if set(props) != expected or not props["íz"] or not props["funkció"]:
        raise RuntimeError(f"Hibás funkcionálisital-séma: {item_id(product)}")
    return props


def normalize_alcohol_product(
    product: dict[str, Any],
    old: dict[str, Any],
    decisions: dict[str, Any],
    source_leaf: str,
) -> dict[str, Any]:
    leaf = str(product.get("altipus") or "")
    if leaf == OTHER:
        return normalize_other(product, old, decisions, source_leaf)
    if leaf == LIQUEUR:
        return normalize_liqueur(product, old, decisions, source_leaf)
    normalizer = NORMALIZERS.get(leaf)
    if normalizer is None:
        raise RuntimeError(f"Ismeretlen alkoholos céllevél: {leaf}")
    return normalizer(product, old, decisions)


def transform_product(product: dict[str, Any], decisions: dict[str, Any]) -> None:
    iid = item_id(product)
    move = (decisions.get("move_path_by_id") or {}).get(iid)
    current_path = path_of(product)
    source_leaf = str(product.get("altipus") or "")
    is_alcohol = current_path[0] == ITAL and current_path[1] == ALCOHOL
    if not is_alcohol and not move:
        return

    old = copy.deepcopy(product.get("tulajdonsagok") or {})
    if move:
        if not isinstance(move, list) or len(move) != 3:
            raise RuntimeError(f"Hibás célút ({iid}): {move!r}")
        set_path(product, tuple(str(value) for value in move))

    target = path_of(product)
    if target == (ITAL, SOFT, KIDS):
        product["tulajdonsagok"] = normalize_kids_drink(product, old, decisions)
    elif target == (ITAL, FUNCTIONAL, SPORT):
        product["tulajdonsagok"] = normalize_functional_drink(
            product,
            old,
            decisions,
        )
    elif target[0] == ITAL and target[1] == ALCOHOL:
        product["tulajdonsagok"] = normalize_alcohol_product(
            product,
            old,
            decisions,
            source_leaf,
        )
    else:
        raise RuntimeError(f"Nem támogatott alkoholos célút ({iid}): {target}")


def alcohol_products(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        product
        for product in products
        if product.get("fokategoria") == ITAL
        and product.get("alkategoria") == ALCOHOL
    ]


def rebuild_trees(
    categories: dict[str, Any],
    products: list[dict[str, Any]],
) -> None:
    alcohol_node = categories[ITAL][ALK_KEY][ALCOHOL]
    rebuilt_leaves: dict[str, Any] = {}
    for leaf in ALCOHOL_LEAVES:
        items = [
            product
            for product in products
            if path_of(product) == (ITAL, ALCOHOL, leaf)
        ]
        if not items:
            raise RuntimeError(f"Üres alkoholos céllevél: {leaf}")
        rebuilt_leaves[leaf] = {PROP_KEY: round1.build_prop_block(items)}
    alcohol_node[PROP_KEY] = {"egyedi": {}, "csoportos": {}}
    alcohol_node[ALT_KEY] = rebuilt_leaves

    kids = [
        product
        for product in products
        if path_of(product) == (ITAL, SOFT, KIDS)
    ]
    if not kids:
        raise RuntimeError("Üres Kölyökpezsgő céllevél")
    categories[ITAL][ALK_KEY][SOFT][ALT_KEY][KIDS][PROP_KEY] = (
        round1.build_prop_block(kids)
    )

    functional = [
        product
        for product in products
        if path_of(product) == (ITAL, FUNCTIONAL, SPORT)
    ]
    if not functional:
        raise RuntimeError("Üres funkcionálisital-céllevél")
    categories[ITAL][ALK_KEY][FUNCTIONAL][ALT_KEY][SPORT][PROP_KEY] = (
        round1.build_prop_block(functional)
    )


def tree_outside_targets(categories: dict[str, Any]) -> dict[str, Any]:
    clone = copy.deepcopy(categories)
    clone[ITAL][ALK_KEY][ALCOHOL] = "<alkoholos ág>"
    clone[ITAL][ALK_KEY][SOFT][ALT_KEY][KIDS] = "<kölyökpezsgő levél>"
    clone[ITAL][ALK_KEY][FUNCTIONAL][ALT_KEY][SPORT] = "<funkcionálisital-levél>"
    return clone


def products_outside_targets(
    products: list[dict[str, Any]],
    moved_ids: set[str],
) -> list[dict[str, Any]]:
    return [
        product
        for product in products
        if not (
            product.get("fokategoria") == ITAL
            and product.get("alkategoria") == ALCOHOL
        )
        and item_id(product) not in moved_ids
    ]


def validate_internal(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
    decisions: dict[str, Any],
    *,
    original_product_ids: Counter[str],
    original_terms_hash: str,
    original_outside_hash: str,
    original_tree_outside_hash: str,
) -> dict[str, Any]:
    errors: list[str] = []
    if len(products) != EXPECTED_TOTAL:
        errors.append(f"termékszám={len(products)}, várt={EXPECTED_TOTAL}")
    if Counter(item_id(product) for product in products) != original_product_ids:
        errors.append("megváltozott a termékazonosítók multihalmaza")
    term_payloads = [product.get("termek") for product in products]
    if round1.json_value_sha256(term_payloads) != original_terms_hash:
        errors.append("megváltozott legalább egy termek payload")

    moved_ids = set((decisions.get("move_path_by_id") or {}).keys())
    if round1.json_value_sha256(
        products_outside_targets(products, moved_ids)
    ) != original_outside_hash:
        errors.append("célon kívüli termék változott")
    if round1.json_value_sha256(
        tree_outside_targets(categories)
    ) != original_tree_outside_hash:
        errors.append("célon kívüli kategóriafanód változott")

    matches = Counter(
        item_id(product)
        for product in products
        if item_id(product) in moved_ids
    )
    for iid, expected_path in (decisions.get("move_path_by_id") or {}).items():
        if matches[iid] != 1:
            errors.append(f"nem egyedi mozgatási ID: {iid} ({matches[iid]})")
            continue
        product = next(product for product in products if item_id(product) == iid)
        if list(path_of(product)) != expected_path:
            errors.append(f"hibás célút: {iid}: {path_of(product)}")

    leaf_counts: Counter[str] = Counter()
    fallback_counts: Counter[str] = Counter()
    for product in alcohol_products(products):
        leaf = str(product.get("altipus") or "")
        leaf_counts[leaf] += 1
        if leaf not in SCHEMAS:
            errors.append(f"ismeretlen alkoholos levél: {leaf}")
            continue
        props = product.get("tulajdonsagok") or {}
        expected = dict(SCHEMAS[leaf])
        if set(props) != set(expected):
            errors.append(f"hibás mezők: {item_id(product)} / {leaf}")
            continue
        for name, shape in expected.items():
            value = props[name]
            if shape == "flag" and not isinstance(value, bool):
                errors.append(f"nem bool: {item_id(product)} / {name}")
            elif shape == "group" and (not isinstance(value, list) or not value):
                errors.append(f"üres/nem lista: {item_id(product)} / {name}")
            elif shape == "single" and (
                isinstance(value, (list, dict, bool)) or value in (None, "")
            ):
                errors.append(f"üres/nem egyedi: {item_id(product)} / {name}")
            for atom in values_of(value):
                if fold(atom) in {
                    "egyeb",
                    "ismeretlen",
                    "marka nelkul",
                    "nem alkalmazhato",
                }:
                    fallback_counts[f"{leaf} / {name} / {atom}"] += 1

    if set(leaf_counts) != set(ALCOHOL_LEAVES):
        errors.append(
            f"eltérő alkoholos levélhalmaz: {sorted(leaf_counts)}"
        )

    alcohol_tree = categories[ITAL][ALK_KEY][ALCOHOL][ALT_KEY]
    if set(alcohol_tree) != set(ALCOHOL_LEAVES):
        errors.append("eltérő alkoholos fanód-levélhalmaz")
    else:
        for leaf in ALCOHOL_LEAVES:
            items = [
                product
                for product in products
                if path_of(product) == (ITAL, ALCOHOL, leaf)
            ]
            expected_block = round1.build_prop_block(items)
            if alcohol_tree[leaf][PROP_KEY] != expected_block:
                errors.append(f"fa/termék értékparitási hiba: {leaf}")

    kids = [
        product
        for product in products
        if path_of(product) == (ITAL, SOFT, KIDS)
    ]
    kids_block = categories[ITAL][ALK_KEY][SOFT][ALT_KEY][KIDS][PROP_KEY]
    if kids_block != round1.build_prop_block(kids):
        errors.append("fa/termék értékparitási hiba: Kölyökpezsgő")

    functional = [
        product
        for product in products
        if path_of(product) == (ITAL, FUNCTIONAL, SPORT)
    ]
    functional_block = categories[ITAL][ALK_KEY][FUNCTIONAL][ALT_KEY][SPORT][PROP_KEY]
    if functional_block != round1.build_prop_block(functional):
        errors.append("fa/termék értékparitási hiba: funkcionális ital")

    return {
        "status": "ok" if not errors else "error",
        "errors": errors,
        "total_products": len(products),
        "alcohol_products": sum(leaf_counts.values()),
        "alcohol_leaf_counts": dict(leaf_counts),
        "fallback_counts": dict(fallback_counts),
        "kids_sparkling_products": len(kids),
        "functional_products": len(functional),
        "moves": len(moved_ids),
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
                "--source-products",
                str(RESULT_PATH),
                "--source-categories",
                str(CATEGORY_PATH),
                "--decisions",
                str(DECISIONS_PATH),
            ],
            cwd=BASE,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
            check=False,
        )
        if completed.returncode == 0:
            return json.loads(completed.stdout)
        failures.append(
            f"{attempt}. kísérlet rc={completed.returncode}: "
            f"{completed.stdout[-1200:]} {completed.stderr[-1200:]}"
        )
    raise RuntimeError("A független ellenőrző hibás:\n" + "\n".join(failures))


def ensure_decision_ids(
    products: list[dict[str, Any]],
    decisions: dict[str, Any],
) -> None:
    counts = Counter(item_id(product) for product in products)
    referenced = (
        set((decisions.get("move_path_by_id") or {}).keys())
        | set((decisions.get("_expanded_brand_by_id") or {}).keys())
        | set((decisions.get("_expanded_property_overrides") or {}).keys())
    )
    invalid = {iid: counts[iid] for iid in referenced if counts[iid] != 1}
    if invalid:
        raise RuntimeError(f"Nem egyedi vagy hiányzó döntési ID-k: {invalid}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--assert-idempotent", action="store_true")
    parser.add_argument("--products-source", type=Path, default=RESULT_PATH)
    parser.add_argument("--categories-source", type=Path, default=CATEGORY_PATH)
    parser.add_argument("--decisions", type=Path, default=DECISIONS_PATH)
    args = parser.parse_args()

    decisions = load_decisions(args.decisions)
    products = round1.load_json(args.products_source)
    categories = round1.load_json(args.categories_source)
    if not isinstance(products, list) or len(products) != EXPECTED_TOTAL:
        raise RuntimeError(f"Váratlan termékállomány: {type(products).__name__}")
    if not isinstance(categories, dict) or ITAL not in categories:
        raise RuntimeError("Váratlan kategóriafa")
    ensure_decision_ids(products, decisions)

    original_product_ids = Counter(item_id(product) for product in products)
    original_terms_hash = round1.json_value_sha256(
        [product.get("termek") for product in products]
    )
    moved_ids = set((decisions.get("move_path_by_id") or {}).keys())
    original_outside_hash = round1.json_value_sha256(
        products_outside_targets(products, moved_ids)
    )
    original_tree_outside_hash = round1.json_value_sha256(
        tree_outside_targets(categories)
    )
    before_categories_hash = round1.json_value_sha256(categories)

    changed_products = 0
    changed_paths: Counter[str] = Counter()
    changed_properties: Counter[str] = Counter()
    samples: list[dict[str, Any]] = []
    for product in products:
        before_path = path_of(product)
        before_props = copy.deepcopy(product.get("tulajdonsagok") or {})
        transform_product(product, decisions)
        after_path = path_of(product)
        after_props = product.get("tulajdonsagok") or {}
        if before_path == after_path and before_props == after_props:
            continue
        product["kategoria_hash"] = round1.category_hash(product)
        changed_products += 1
        changed_paths[f"{' > '.join(before_path)} -> {' > '.join(after_path)}"] += 1
        for key in set(before_props) | set(after_props):
            if before_props.get(key) != after_props.get(key):
                changed_properties[key] += 1
        if len(samples) < 40:
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

    rebuild_trees(categories, products)
    validation = validate_internal(
        products,
        categories,
        decisions,
        original_product_ids=original_product_ids,
        original_terms_hash=original_terms_hash,
        original_outside_hash=original_outside_hash,
        original_tree_outside_hash=original_tree_outside_hash,
    )
    if validation["status"] != "ok":
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        raise RuntimeError(f"Belső validációs hibák: {validation['errors'][:30]}")

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
        "changed_properties": dict(changed_properties),
        "samples": samples,
        "products_source": str(args.products_source),
        "categories_source": str(args.categories_source),
        "decisions_source": str(args.decisions),
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
