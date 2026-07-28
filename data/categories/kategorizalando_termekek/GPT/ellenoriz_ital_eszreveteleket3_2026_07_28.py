# -*- coding: utf-8 -*-
"""Független, csak olvasó validátor az Ital 3. tisztítás jelöltfájljaihoz.

A program szándékosan nem importálja a migrációs modult. A forrás- és a
jelöltállományt szigorú JSON-olvasással tölti be, majd a termékadatokat, a
kategóriafát és a kézzel rögzített döntések alkalmazását is összeveti.
Az eredmény egyetlen JSON-objektum a standard kimeneten; hiba esetén a
kilépési kód nem nulla.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


EXPECTED_TOTAL = 47030
MAX_REPORTED_ERRORS = 250

ITAL = "Ital"
ALCOHOL = "Alkoholos italok és alkoholmentes alternatívák"
SOFT = "Üdítőitalok"
KIDS = "Kölyökpezsgő"
FUNCTIONAL = "Funkcionális italok"
SPORT = "Sport-, izotóniás, kollagén- és shot ital"
PRODUCT_PROP_KEY = "tulajdonsagok"
TREE_PROP_KEY = "tulajdonságok"
SUBCATEGORY_KEY = "alkategóriák"
LEAF_KEY = "altípusok"

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

# A shape értéke single/group/flag. A sorrend is szerződés: a migráció
# determinisztikusan ebben a sorrendben írja a terméktulajdonságokat.
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

KIDS_SCHEMA = (
    ("márka", "single"),
    ("íz", "group"),
    ("szénsavas", "flag"),
    ("energiatartalom", "single"),
)
FUNCTIONAL_SCHEMA = (
    ("márka", "single"),
    ("íz", "group"),
    ("funkció", "group"),
)

SIZE_RE = re.compile(r"^(?:[1-9]\d*)(?:,\d*[1-9])? ml$")
ABV_RE = re.compile(r"^(?:0|[1-9]\d*)(?:,\d*[1-9])?%$")
NUMERIC_FALLBACK = "ismeretlen"
BEER_BASES = {"sor", "radler", "malataital"}

BEER_STYLE_OR_COLOR_ATOMS = {
    "sor",
    "radler",
    "malataital",
    "buzasor",
    "ipa",
    "apa",
    "lager",
    "pils",
    "pilsner",
    "ale",
    "lambic",
    "new england ipa",
    "session ipa",
    "india pale lager",
    "sorkulonlegesseg",
    "pale ale",
    "west coast ipa",
    "double ipa",
    "black ipa",
    "sour ipa",
    "porter",
    "stout",
    "bak",
    "helles",
    "dunkel",
    "kellerbier",
    "belga blond",
    "dubbel",
    "tripel",
    "quadrupel",
    "feher",
    "vilagos",
    "barna",
    "sotet",
    "voros",
    "fekete",
    "zold",
    "borostyan",
    "roze",
    "amber",
    "ruby",
    "green",
    "dark",
    "brune",
}

ENGLISH_FLAVOR_ALIASES = {
    "apple",
    "sour cherry",
    "cherry",
    "orange",
    "blood orange",
    "red berry",
    "mixed fruit",
    "berry",
    "berry kiss",
    "pink strawberry",
    "purple hibiscus",
    "bison grass",
    "pear",
    "smoky",
    "japanese blossom",
    "honey",
    "wild cherry",
    "watermelon",
    "spiced",
    "spiced gold",
    "black spiced",
    "caribbean spiced",
    "brown cacao",
    "cioccolato",
    "sweet honey",
    "lemon mint",
    "sauer apfel",
    "tropical chilli",
    "tropical flirt",
    "pink grapefruit",
    "passion fruit",
    "pineapple",
    "apricot",
    "peach",
}

ATOMIC_PROPERTIES = {
    "íz",
    "fajta",
    "típus",
    "szín",
    "édesség",
    "szőlőfajta",
    "eredet",
    "bortípus",
    "alkoholalap",
    "csomagolás anyaga",
}
FORBIDDEN_ATOM_MARKERS = (";", "|", "/", "\n", "\r", "[", "]", "{", "}")


class ErrorReport:
    def __init__(self) -> None:
        self.count = 0
        self.errors: list[str] = []

    def add(self, message: str) -> None:
        self.count += 1
        if len(self.errors) < MAX_REPORTED_ERRORS:
            self.errors.append(message)


def strict_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplikált JSON-kulcs: {key!r}")
        result[key] = value
    return result


def reject_nonfinite(value: str) -> None:
    raise ValueError(f"nem véges JSON-szám: {value}")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(
            handle,
            object_pairs_hook=strict_object,
            parse_constant=reject_nonfinite,
        )


def fold(value: Any) -> str:
    text = unicodedata.normalize("NFKD", "" if value is None else str(value))
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.casefold()
    text = re.sub(r"[^0-9a-z]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def values_of(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    return list(value) if isinstance(value, list) else [value]


def first_value(value: Any) -> Any:
    values = values_of(value)
    return values[0] if values else None


def item_id(product: dict[str, Any]) -> str:
    termek = product.get("termek")
    if not isinstance(termek, dict):
        return ""
    return str(termek.get("store_product_id") or "")


def record_key(product: dict[str, Any]) -> tuple[str, str]:
    """A bolti termék ténylegesen egyedi kulcsa.

    A nyers ``store_product_id`` boltok között ütközhet (a jelenlegi forrásban
    például az Aldi és a Penny is használja a 734295 értéket), ezért az
    egyediséget a bolt és a bolti azonosító párjára kell vizsgálni.
    """

    termek = product.get("termek")
    if not isinstance(termek, dict):
        return ("", "")
    return (
        str(termek.get("store_name") or ""),
        str(termek.get("store_product_id") or ""),
    )


def path_of(product: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(product.get("fokategoria") or ""),
        str(product.get("alkategoria") or ""),
        str(product.get("altipus") or ""),
    )


def json_value_sha256(payload: Any) -> str:
    digest = hashlib.sha256()
    encoder = json.JSONEncoder(
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    for piece in encoder.iterencode(payload):
        digest.update(piece.encode("utf-8"))
    return digest.hexdigest()


def category_hash(product: dict[str, Any]) -> str:
    key = "|".join(
        [
            str(product.get("fokategoria") or ""),
            str(product.get("alkategoria") or ""),
            str(product.get("altipus") or ""),
            json.dumps(
                product.get(PRODUCT_PROP_KEY) or {},
                sort_keys=True,
                ensure_ascii=False,
            ),
        ]
    )
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def shape_of(value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    if isinstance(value, list):
        return "group"
    return "single"


def dedupe(values: Iterable[Any]) -> list[Any]:
    result: list[Any] = []
    seen: set[str] = set()
    for value in values:
        if value is None or value == "":
            continue
        marker = f"{type(value).__name__}:{fold(value)}"
        if marker in seen:
            continue
        seen.add(marker)
        result.append(value)
    return result


def build_prop_block(products: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    raw: dict[str, list[Any]] = defaultdict(list)
    values: dict[str, list[Any]] = defaultdict(list)
    for product in products:
        props = product.get(PRODUCT_PROP_KEY)
        if not isinstance(props, dict):
            raise ValueError(f"nem objektum tulajdonságok: {item_id(product)}")
        for name, value in props.items():
            raw[name].append(value)
            values[name].extend(values_of(value))
    block: dict[str, dict[str, Any]] = {"egyedi": {}, "csoportos": {}}
    for name in sorted(raw, key=fold):
        shapes = {shape_of(value) for value in raw[name]}
        if len(shapes) != 1:
            raise ValueError(f"kevert tulajdonságalak: {name!r}: {shapes}")
        shape = next(iter(shapes))
        allowed = sorted(dedupe(values[name]), key=fold)
        if shape == "flag":
            block["egyedi"][name] = {}
        elif shape == "single":
            block["egyedi"][name] = allowed
        else:
            block["csoportos"][name] = allowed
    return block


def nested(root: Any, *keys: str) -> Any:
    current = root
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            raise KeyError(" > ".join(keys))
        current = current[key]
    return current


def masked_tree(categories: dict[str, Any]) -> dict[str, Any]:
    clone = copy.deepcopy(categories)
    nested(clone, ITAL, SUBCATEGORY_KEY)[ALCOHOL] = "<alkoholos ág>"
    nested(
        clone,
        ITAL,
        SUBCATEGORY_KEY,
        SOFT,
        LEAF_KEY,
    )[KIDS] = "<kölyökpezsgő levél>"
    nested(
        clone,
        ITAL,
        SUBCATEGORY_KEY,
        FUNCTIONAL,
        LEAF_KEY,
    )[SPORT] = "<funkcionálisital-levél>"
    return clone


def merge_assignment(
    target: dict[str, dict[str, Any]],
    iid: str,
    name: str,
    value: Any,
    report: ErrorReport,
    origin: str,
) -> None:
    current = target.setdefault(iid, {})
    if name in current and current[name] != value:
        report.add(
            f"ütköző döntés: {iid}/{name}: {current[name]!r} != "
            f"{value!r} ({origin})"
        )
        return
    current[name] = copy.deepcopy(value)


def expand_decisions(
    decisions: Any,
    report: ErrorReport,
) -> tuple[
    dict[str, list[str]],
    dict[str, str],
    dict[str, dict[str, Any]],
    dict[str, str],
]:
    if not isinstance(decisions, dict):
        report.add("a döntésfájl gyökere nem objektum")
        return {}, {}, {}, {}

    required = {
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
    missing = required - set(decisions)
    if missing:
        report.add(f"hiányos döntésfájl: {sorted(missing)}")

    moves: dict[str, list[str]] = {}
    raw_moves = decisions.get("move_path_by_id") or {}
    if not isinstance(raw_moves, dict):
        report.add("a move_path_by_id nem objektum")
    else:
        for raw_iid, raw_path in raw_moves.items():
            iid = str(raw_iid)
            if (
                not isinstance(raw_path, list)
                or len(raw_path) != 3
                or not all(isinstance(value, str) and value for value in raw_path)
            ):
                report.add(f"hibás mozgatási út: {iid}: {raw_path!r}")
                continue
            moves[iid] = list(raw_path)

    brands: dict[str, str] = {}
    raw_brands = decisions.get("brand_by_id") or {}
    if not isinstance(raw_brands, dict):
        report.add("a brand_by_id nem objektum")
    else:
        for raw_iid, raw_brand in raw_brands.items():
            iid = str(raw_iid)
            if not isinstance(raw_brand, str) or not raw_brand.strip():
                report.add(f"hibás egyedi márkadöntés: {iid}: {raw_brand!r}")
                continue
            brands[iid] = raw_brand
    raw_brand_groups = decisions.get("brand_groups") or []
    if not isinstance(raw_brand_groups, list):
        report.add("a brand_groups nem lista")
    else:
        for index, group in enumerate(raw_brand_groups):
            if not isinstance(group, dict):
                report.add(f"hibás brand_groups[{index}]")
                continue
            brand = group.get("brand")
            ids = group.get("ids")
            if (
                not isinstance(brand, str)
                or not brand.strip()
                or not isinstance(ids, list)
                or not ids
            ):
                report.add(f"hiányos brand_groups[{index}]")
                continue
            for raw_iid in ids:
                iid = str(raw_iid)
                if iid in brands and brands[iid] != brand:
                    report.add(
                        f"ütköző csoportos márka: {iid}: "
                        f"{brands[iid]!r} != {brand!r}"
                    )
                    continue
                brands[iid] = brand

    properties: dict[str, dict[str, Any]] = {}
    raw_properties = decisions.get("property_overrides_by_id") or {}
    if not isinstance(raw_properties, dict):
        report.add("a property_overrides_by_id nem objektum")
    else:
        for raw_iid, assignments in raw_properties.items():
            iid = str(raw_iid)
            if not isinstance(assignments, dict) or not assignments:
                report.add(f"hibás egyedi tulajdonságdöntés: {iid}")
                continue
            for name, value in assignments.items():
                if not isinstance(name, str) or not name:
                    report.add(f"üres tulajdonságnév a döntésben: {iid}")
                    continue
                merge_assignment(
                    properties,
                    iid,
                    name,
                    value,
                    report,
                    "property_overrides_by_id",
                )

    raw_property_groups = decisions.get("property_groups") or []
    if not isinstance(raw_property_groups, list):
        report.add("a property_groups nem lista")
    else:
        for index, group in enumerate(raw_property_groups):
            if not isinstance(group, dict):
                report.add(f"hibás property_groups[{index}]")
                continue
            ids = group.get("ids")
            assignments = group.get("set")
            if assignments is None:
                name = group.get("property")
                assignments = {name: group.get("value")} if name else {}
            if (
                not isinstance(ids, list)
                or not ids
                or not isinstance(assignments, dict)
                or not assignments
            ):
                report.add(f"hiányos property_groups[{index}]")
                continue
            for raw_iid in ids:
                iid = str(raw_iid)
                for name, value in assignments.items():
                    if not isinstance(name, str) or not name:
                        report.add(f"üres tulajdonságnév: property_groups[{index}]")
                        continue
                    merge_assignment(
                        properties,
                        iid,
                        name,
                        value,
                        report,
                        f"property_groups[{index}]",
                    )

    fajta_leaf_by_id: dict[str, str] = {}
    raw_fajta_groups = decisions.get("fajta_groups") or {}
    if not isinstance(raw_fajta_groups, dict):
        report.add("a fajta_groups nem objektum")
    else:
        for leaf, value_groups in raw_fajta_groups.items():
            if leaf not in {LIQUEUR, OTHER} or not isinstance(value_groups, dict):
                report.add(f"hibás fajta_groups ág: {leaf!r}")
                continue
            for value, ids in value_groups.items():
                if (
                    not isinstance(value, str)
                    or not value
                    or not isinstance(ids, list)
                    or not ids
                ):
                    report.add(f"hibás fajta_groups csoport: {leaf}/{value!r}")
                    continue
                for raw_iid in ids:
                    iid = str(raw_iid)
                    if iid in fajta_leaf_by_id and fajta_leaf_by_id[iid] != leaf:
                        report.add(
                            f"több levélhez rendelt fajta_groups ID: {iid}"
                        )
                    fajta_leaf_by_id[iid] = leaf
                    merge_assignment(
                        properties,
                        iid,
                        "fajta",
                        value,
                        report,
                        f"fajta_groups/{leaf}",
                    )
    return moves, brands, properties, fajta_leaf_by_id


def check_shape(
    iid: str,
    leaf: str,
    props: Any,
    schema: tuple[tuple[str, str], ...],
    report: ErrorReport,
) -> bool:
    if not isinstance(props, dict):
        report.add(f"nem objektum tulajdonságok: {iid}/{leaf}")
        return False
    expected_names = [name for name, _ in schema]
    actual_names = list(props)
    if actual_names != expected_names:
        report.add(
            f"hibás vagy rossz sorrendű séma: {iid}/{leaf}: "
            f"{actual_names!r} != {expected_names!r}"
        )
        return False

    valid = True
    for name, shape in schema:
        value = props[name]
        if shape == "flag":
            if not isinstance(value, bool):
                report.add(f"nem bool érték: {iid}/{leaf}/{name}: {value!r}")
                valid = False
        elif shape == "group":
            if not isinstance(value, list) or not value:
                report.add(
                    f"nem kitöltött csoportos érték: "
                    f"{iid}/{leaf}/{name}: {value!r}"
                )
                valid = False
                continue
            seen: set[str] = set()
            for atom in value:
                if not isinstance(atom, str) or not atom.strip():
                    report.add(
                        f"nem elemi szöveg a csoportban: "
                        f"{iid}/{leaf}/{name}: {atom!r}"
                    )
                    valid = False
                    continue
                marker = fold(atom)
                if marker in seen:
                    report.add(
                        f"duplikált csoportérték: "
                        f"{iid}/{leaf}/{name}: {atom!r}"
                    )
                    valid = False
                seen.add(marker)
        else:
            if (
                value is None
                or isinstance(value, (list, dict, bool))
                or (isinstance(value, str) and not value.strip())
                or (
                    isinstance(value, float)
                    and (math.isnan(value) or math.isinf(value))
                )
            ):
                report.add(
                    f"nem kitöltött egyedi érték: "
                    f"{iid}/{leaf}/{name}: {value!r}"
                )
                valid = False
    return valid


def check_atomic_values(
    iid: str,
    leaf: str,
    props: dict[str, Any],
    report: ErrorReport,
) -> None:
    for name in ATOMIC_PROPERTIES & set(props):
        for atom in values_of(props[name]):
            if not isinstance(atom, str):
                continue
            if any(marker in atom for marker in FORBIDDEN_ATOM_MARKERS):
                report.add(
                    f"összetett/nem elemi érték: {iid}/{leaf}/{name}: {atom!r}"
                )
            if name == "íz" and re.search(
                r"\s+(?:és|vagy)\s+",
                atom,
                flags=re.IGNORECASE,
            ):
                report.add(
                    f"összekapcsolt ízérték: {iid}/{leaf}/{name}: {atom!r}"
                )
            if name == "íz" and fold(atom) in ENGLISH_FLAVOR_ALIASES:
                report.add(
                    f"nem honosított ízérték: {iid}/{leaf}/{name}: {atom!r}"
                )


def check_numeric_formats(
    iid: str,
    leaf: str,
    props: dict[str, Any],
    report: ErrorReport,
) -> None:
    for value in values_of(props.get("alkoholtartalom")):
        if value == NUMERIC_FALLBACK:
            continue
        if value == "egyéb":
            report.add(
                f"nem egységes alkoholtartalom-fallback: "
                f"{iid}/{leaf}: {value!r}"
            )
            continue
        if not isinstance(value, str) or not ABV_RE.fullmatch(value):
            report.add(
                f"nem kanonikus alkoholtartalom: {iid}/{leaf}: {value!r}"
            )
            continue
        number = float(value[:-1].replace(",", "."))
        if number < 0 or number > 100:
            report.add(
                f"tartományon kívüli alkoholtartalom: "
                f"{iid}/{leaf}: {value!r}"
            )

    for name in ("kiszerelés", "egységnyi kiszerelés"):
        if name not in props:
            continue
        for value in values_of(props[name]):
            if value == NUMERIC_FALLBACK:
                continue
            if value == "egyéb":
                report.add(
                    f"nem egységes kiszerelés-fallback: "
                    f"{iid}/{leaf}/{name}: {value!r}"
                )
                continue
            if not isinstance(value, str) or not SIZE_RE.fullmatch(value):
                report.add(
                    f"nem kanonikus ml-érték: "
                    f"{iid}/{leaf}/{name}: {value!r}"
                )


def check_product_semantics(
    product: dict[str, Any],
    report: ErrorReport,
) -> None:
    iid = item_id(product)
    leaf = str(product.get("altipus") or "")
    props = product.get(PRODUCT_PROP_KEY)
    if leaf not in SCHEMAS or not isinstance(props, dict):
        return

    if props["alkoholstátusz"] not in {"alkoholos", "alkoholmentes"}:
        report.add(
            f"hibás alkoholstátusz: {iid}/{leaf}: "
            f"{props['alkoholstátusz']!r}"
        )
    if not isinstance(props["márka"], str) or not props["márka"].strip():
        report.add(f"üres márka: {iid}/{leaf}")
    check_numeric_formats(iid, leaf, props, report)
    check_atomic_values(iid, leaf, props, report)

    if leaf == CIDER and props["csomagolás"] not in {"doboz", "palack"}:
        report.add(
            f"hibás cider-csomagolás: {iid}: {props['csomagolás']!r}"
        )
    if leaf == BEER:
        tags = props["fajta"]
        folded_tags = [fold(value) for value in tags]
        bases = [value for value in folded_tags if value in BEER_BASES]
        if len(bases) != 1 or not folded_tags or folded_tags[0] not in BEER_BASES:
            report.add(f"hibás sör-alaptípus: {iid}: {tags!r}")
        if folded_tags and folded_tags[0] in {"radler", "malataital"} and len(tags) != 1:
            report.add(f"radler/malátaital mellett stíluscímke maradt: {iid}: {tags!r}")
        flavors = [fold(value) for value in props["íz"]]
        polluted = sorted(set(flavors) & BEER_STYLE_OR_COLOR_ATOMS)
        if polluted:
            report.add(f"sörízben stílus/szín maradt: {iid}: {polluted!r}")
        if any(value == "roze" for value in (fold(item) for item in props["szín"])):
            report.add(f"rozé maradt sörszínként: {iid}: {props['szín']!r}")
        count = props["csomagdarabszám"]
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            report.add(f"hibás sörcsomag-darabszám: {iid}: {count!r}")


def check_tree_parity(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
    report: ErrorReport,
) -> tuple[dict[str, int], int, int]:
    leaf_counts: Counter[str] = Counter()
    for product in products:
        if (
            product.get("fokategoria") == ITAL
            and product.get("alkategoria") == ALCOHOL
        ):
            leaf_counts[str(product.get("altipus") or "")] += 1

    try:
        alcohol_node = nested(
            categories,
            ITAL,
            SUBCATEGORY_KEY,
            ALCOHOL,
        )
        alcohol_tree = nested(
            categories,
            ITAL,
            SUBCATEGORY_KEY,
            ALCOHOL,
            LEAF_KEY,
        )
    except KeyError as exc:
        report.add(f"hiányzó alkoholos faág: {exc}")
        return dict(leaf_counts), 0, 0

    if not isinstance(alcohol_node, dict):
        report.add("az alkoholos fanód nem objektum")
        return dict(leaf_counts), 0, 0
    if alcohol_node.get(TREE_PROP_KEY) != {"egyedi": {}, "csoportos": {}}:
        report.add("az alkoholos köztes fanód tulajdonságblokkja nem üres")
    if not isinstance(alcohol_tree, dict):
        report.add("az alkoholos altípusfa nem objektum")
        return dict(leaf_counts), 0, 0
    if set(alcohol_tree) != set(ALCOHOL_LEAVES):
        report.add(
            "eltérő alkoholos fanód-levélhalmaz: "
            f"{sorted(alcohol_tree)!r}"
        )

    for leaf in ALCOHOL_LEAVES:
        items = [
            product
            for product in products
            if path_of(product) == (ITAL, ALCOHOL, leaf)
        ]
        if not items:
            report.add(f"üres alkoholos céllevél: {leaf}")
            continue
        node = alcohol_tree.get(leaf)
        if not isinstance(node, dict):
            report.add(f"hiányzó/nem objektum alkoholos levél: {leaf}")
            continue
        if set(node) != {TREE_PROP_KEY}:
            report.add(f"váratlan mező az alkoholos fanódon: {leaf}: {list(node)!r}")
        try:
            expected = build_prop_block(items)
        except (TypeError, ValueError) as exc:
            report.add(f"nem építhető tulajdonságblokk: {leaf}: {exc}")
            continue
        if node.get(TREE_PROP_KEY) != expected:
            report.add(f"fa/termék tulajdonságérték-paritási hiba: {leaf}")
        declared = node.get(TREE_PROP_KEY)
        if isinstance(declared, dict):
            singles = declared.get("egyedi")
            groups = declared.get("csoportos")
            if isinstance(singles, dict) and isinstance(groups, dict):
                expected_single = {
                    name for name, shape in SCHEMAS[leaf] if shape != "group"
                }
                expected_group = {
                    name for name, shape in SCHEMAS[leaf] if shape == "group"
                }
                if set(singles) != expected_single or set(groups) != expected_group:
                    report.add(f"hibás deklarált tulajdonságséma a fában: {leaf}")

    kids_items = [
        product
        for product in products
        if path_of(product) == (ITAL, SOFT, KIDS)
    ]
    functional_items = [
        product
        for product in products
        if path_of(product) == (ITAL, FUNCTIONAL, SPORT)
    ]
    try:
        kids_block = nested(
            categories,
            ITAL,
            SUBCATEGORY_KEY,
            SOFT,
            LEAF_KEY,
            KIDS,
            TREE_PROP_KEY,
        )
        if kids_block != build_prop_block(kids_items):
            report.add("fa/termék értékparitási hiba: Kölyökpezsgő")
    except (KeyError, TypeError, ValueError) as exc:
        report.add(f"hibás Kölyökpezsgő célág: {exc}")
    try:
        functional_block = nested(
            categories,
            ITAL,
            SUBCATEGORY_KEY,
            FUNCTIONAL,
            LEAF_KEY,
            SPORT,
            TREE_PROP_KEY,
        )
        if functional_block != build_prop_block(functional_items):
            report.add("fa/termék értékparitási hiba: funkcionális ital")
    except (KeyError, TypeError, ValueError) as exc:
        report.add(f"hibás funkcionálisital-célág: {exc}")
    return dict(leaf_counts), len(kids_items), len(functional_items)


def validate(
    products: Any,
    categories: Any,
    source_products: Any,
    source_categories: Any,
    decisions: Any,
) -> dict[str, Any]:
    report = ErrorReport()
    moves, explicit_brands, property_overrides, fajta_leaf_by_id = (
        expand_decisions(decisions, report)
    )

    if not isinstance(products, list):
        report.add("a jelölt termékállomány gyökere nem lista")
        products = []
    if not isinstance(source_products, list):
        report.add("a forrás termékállomány gyökere nem lista")
        source_products = []
    if not isinstance(categories, dict):
        report.add("a jelölt kategóriafa gyökere nem objektum")
        categories = {}
    if not isinstance(source_categories, dict):
        report.add("a forrás kategóriafa gyökere nem objektum")
        source_categories = {}

    if len(products) != EXPECTED_TOTAL:
        report.add(
            f"jelölt termékszám={len(products)}, várt={EXPECTED_TOTAL}"
        )
    if len(source_products) != EXPECTED_TOTAL:
        report.add(
            f"forrás termékszám={len(source_products)}, várt={EXPECTED_TOTAL}"
        )

    candidate_ids = [item_id(product) for product in products if isinstance(product, dict)]
    source_ids = [
        item_id(product)
        for product in source_products
        if isinstance(product, dict)
    ]
    if len(candidate_ids) != len(products):
        report.add("nem objektum elem van a jelölt terméklistában")
    if len(source_ids) != len(source_products):
        report.add("nem objektum elem van a forrás terméklistában")
    if any(not iid for iid in candidate_ids):
        report.add("üres termékazonosító van a jelöltben")
    if any(not iid for iid in source_ids):
        report.add("üres termékazonosító van a forrásban")

    candidate_counts = Counter(candidate_ids)
    source_counts = Counter(source_ids)
    candidate_record_counts = Counter(
        record_key(product)
        for product in products
        if isinstance(product, dict)
    )
    source_record_counts = Counter(
        record_key(product)
        for product in source_products
        if isinstance(product, dict)
    )
    candidate_duplicate_records = {
        key: count
        for key, count in candidate_record_counts.items()
        if count != 1
    }
    source_duplicate_records = {
        key: count
        for key, count in source_record_counts.items()
        if count != 1
    }
    if candidate_duplicate_records:
        report.add(
            f"nem egyedi jelölt (bolt, termékazonosító) kulcsok: "
            f"{dict(list(candidate_duplicate_records.items())[:20])!r}"
        )
    if source_duplicate_records:
        report.add(
            f"nem egyedi forrás (bolt, termékazonosító) kulcsok: "
            f"{dict(list(source_duplicate_records.items())[:20])!r}"
        )
    if candidate_counts != source_counts:
        report.add("megváltozott a termékazonosítók multihalmaza")
    if candidate_record_counts != source_record_counts:
        report.add("megváltozott a (bolt, termékazonosító) kulcsok multihalmaza")

    source_terms = [
        product.get("termek") if isinstance(product, dict) else None
        for product in source_products
    ]
    candidate_terms = [
        product.get("termek") if isinstance(product, dict) else None
        for product in products
    ]
    source_terms_hash = json_value_sha256(source_terms)
    candidate_terms_hash = json_value_sha256(candidate_terms)
    if source_terms_hash != candidate_terms_hash:
        report.add(
            "megváltozott a termek payloadok kanonikus szerkezete vagy sorrendje"
        )

    source_index = {
        item_id(product): product
        for product in source_products
        if isinstance(product, dict) and item_id(product)
    }
    candidate_index = {
        item_id(product): product
        for product in products
        if isinstance(product, dict) and item_id(product)
    }
    for iid in source_counts.keys() & candidate_counts.keys():
        if source_index[iid].get("termek") != candidate_index[iid].get("termek"):
            report.add(f"megváltozott termek payload: {iid}")

    all_decision_ids = (
        set(moves)
        | set(explicit_brands)
        | set(property_overrides)
        | set(fajta_leaf_by_id)
    )
    for iid in sorted(all_decision_ids):
        if source_counts[iid] != 1:
            report.add(
                f"hiányzó/nem egyedi döntési ID a forrásban: "
                f"{iid} ({source_counts[iid]})"
            )
        if candidate_counts[iid] != 1:
            report.add(
                f"hiányzó/nem egyedi döntési ID a jelöltben: "
                f"{iid} ({candidate_counts[iid]})"
            )

    source_alcohol_ids = {
        item_id(product)
        for product in source_products
        if isinstance(product, dict)
        and path_of(product)[:2] == (ITAL, ALCOHOL)
    }
    target_ids = source_alcohol_ids | set(moves)
    source_outside = [
        product
        for product in source_products
        if isinstance(product, dict) and item_id(product) not in target_ids
    ]
    candidate_outside = [
        product
        for product in products
        if isinstance(product, dict) and item_id(product) not in target_ids
    ]
    source_outside_hash = json_value_sha256(source_outside)
    candidate_outside_hash = json_value_sha256(candidate_outside)
    if source_outside_hash != candidate_outside_hash:
        report.add("célon kívüli termék vagy terméksorrend megváltozott")
        for source_product in source_outside:
            iid = item_id(source_product)
            candidate = candidate_index.get(iid)
            if candidate != source_product:
                report.add(f"célon kívüli termék változott: {iid}")

    try:
        source_tree_outside_hash = json_value_sha256(masked_tree(source_categories))
        candidate_tree_outside_hash = json_value_sha256(masked_tree(categories))
        if source_tree_outside_hash != candidate_tree_outside_hash:
            report.add("célon kívüli kategóriafaág változott")
    except KeyError as exc:
        source_tree_outside_hash = ""
        candidate_tree_outside_hash = ""
        report.add(f"nem maszkolható kategóriafa: {exc}")

    for iid, expected_path in moves.items():
        product = candidate_index.get(iid)
        if product is not None and list(path_of(product)) != expected_path:
            report.add(
                f"hibás célút: {iid}: {list(path_of(product))!r} "
                f"!= {expected_path!r}"
            )

    for iid, expected_leaf in fajta_leaf_by_id.items():
        product = candidate_index.get(iid)
        if product is not None and product.get("altipus") != expected_leaf:
            report.add(
                f"hibás fajta_groups céllevél: {iid}: "
                f"{product.get('altipus')!r} != {expected_leaf!r}"
            )

    for iid, assignments in property_overrides.items():
        product = candidate_index.get(iid)
        if product is None:
            continue
        props = product.get(PRODUCT_PROP_KEY)
        if not isinstance(props, dict):
            report.add(f"nincs tulajdonságobjektum a döntési ID-n: {iid}")
            continue
        for name, expected in assignments.items():
            if name not in props:
                report.add(f"nem alkalmazott tulajdonságdöntés: {iid}/{name}")
            elif props[name] != expected:
                report.add(
                    f"eltérő tulajdonságdöntés: {iid}/{name}: "
                    f"{props[name]!r} != {expected!r}"
                )

    aliases = decisions.get("brand_aliases") if isinstance(decisions, dict) else {}
    if not isinstance(aliases, dict):
        report.add("a brand_aliases nem objektum")
        aliases = {}
    folded_brand_aliases = {fold(key): value for key, value in aliases.items()}
    for iid in target_ids & source_counts.keys() & candidate_counts.keys():
        source = source_index[iid]
        candidate = candidate_index[iid]
        props = candidate.get(PRODUCT_PROP_KEY)
        if not isinstance(props, dict) or "márka" not in props:
            report.add(f"hiányzó jelölt márka: {iid}")
            continue
        override_props = property_overrides.get(iid) or {}
        if "márka" in override_props:
            expected_brand = override_props["márka"]
        elif iid in explicit_brands:
            expected_brand = explicit_brands[iid]
        else:
            source_props = source.get(PRODUCT_PROP_KEY)
            raw_brand = (
                first_value(source_props.get("márka"))
                if isinstance(source_props, dict)
                else None
            )
            if not raw_brand and isinstance(source.get("termek"), dict):
                raw_brand = source["termek"].get("brand_name")
            text = str(raw_brand or "").strip()
            expected_brand = folded_brand_aliases.get(
                fold(text),
                text or "márka nélkül",
            )
        if props["márka"] != expected_brand:
            report.add(
                f"nem alkalmazott márkadöntés/alias: {iid}: "
                f"{props['márka']!r} != {expected_brand!r}"
            )

    value_aliases = (
        decisions.get("value_aliases") if isinstance(decisions, dict) else {}
    )
    flavor_aliases = (
        value_aliases.get("íz")
        if isinstance(value_aliases, dict)
        and isinstance(value_aliases.get("íz"), dict)
        else {}
    )
    folded_flavor_aliases = {fold(key) for key in flavor_aliases}
    flavor_drops = (
        decisions.get("flavor_drop_by_leaf")
        if isinstance(decisions, dict)
        else {}
    )
    if not isinstance(flavor_drops, dict):
        report.add("a flavor_drop_by_leaf nem objektum")
        flavor_drops = {}

    leaf_counts: Counter[str] = Counter()
    fallback_counts: Counter[str] = Counter()
    for product in products:
        if not isinstance(product, dict):
            continue
        if path_of(product)[:2] != (ITAL, ALCOHOL):
            continue
        iid = item_id(product)
        leaf = str(product.get("altipus") or "")
        leaf_counts[leaf] += 1
        schema = SCHEMAS.get(leaf)
        if schema is None:
            report.add(f"ismeretlen alkoholos levél: {iid}/{leaf}")
            continue
        props = product.get(PRODUCT_PROP_KEY)
        if not check_shape(iid, leaf, props, schema, report):
            continue
        assert isinstance(props, dict)
        check_product_semantics(product, report)
        for name, value in props.items():
            for atom in values_of(value):
                if fold(atom) in {
                    "egyeb",
                    "ismeretlen",
                    "marka nelkul",
                    "nem alkalmazhato",
                }:
                    fallback_counts[f"{leaf} / {name} / {atom}"] += 1

        candidate_flavors = {
            fold(value)
            for value in values_of(props.get("íz"))
            if isinstance(value, str)
        }
        unresolved_aliases = candidate_flavors & folded_flavor_aliases
        for alias in sorted(unresolved_aliases):
            mapped = flavor_aliases.get(alias)
            if fold(mapped) != alias:
                report.add(
                    f"nem alkalmazott íz-alias: {iid}/{leaf}: {alias!r}"
                )
        drops = {
            fold(value)
            for value in (
                flavor_drops.get(leaf)
                if isinstance(flavor_drops.get(leaf), list)
                else []
            )
        }
        remaining_drops = candidate_flavors & drops
        if remaining_drops:
            report.add(
                f"eltávolítandó ízérték maradt: "
                f"{iid}/{leaf}: {sorted(remaining_drops)!r}"
            )

    if set(leaf_counts) != set(ALCOHOL_LEAVES):
        report.add(
            f"eltérő alkoholos terméklevél-halmaz: {sorted(leaf_counts)!r}"
        )

    # A külső célleveleken csak az oda mozgatott rekordok kapnak új sémát;
    # a már ott lévő termékek korábbi, eltérő sémáját nem írjuk át.
    for iid, expected_path in moves.items():
        product = candidate_index.get(iid)
        if product is None:
            continue
        if tuple(expected_path) == (ITAL, SOFT, KIDS):
            check_shape(
                iid,
                KIDS,
                product.get(PRODUCT_PROP_KEY),
                KIDS_SCHEMA,
                report,
            )
        elif tuple(expected_path) == (ITAL, FUNCTIONAL, SPORT):
            check_shape(
                iid,
                SPORT,
                product.get(PRODUCT_PROP_KEY),
                FUNCTIONAL_SCHEMA,
                report,
            )

    for iid in target_ids & candidate_counts.keys():
        product = candidate_index[iid]
        actual_hash = category_hash(product)
        if product.get("kategoria_hash") != actual_hash:
            report.add(
                f"hibás kategoria_hash: {iid}: "
                f"{product.get('kategoria_hash')!r} != {actual_hash!r}"
            )

    tree_leaf_counts, kids_count, functional_count = check_tree_parity(
        products,
        categories,
        report,
    )

    return {
        "status": "ok" if report.count == 0 else "error",
        "error_count": report.count,
        "errors": report.errors,
        "errors_truncated": report.count > len(report.errors),
        "total_products": len(products),
        "source_total_products": len(source_products),
        "unique_plain_product_ids": len(candidate_counts),
        "unique_record_keys": len(candidate_record_counts),
        "plain_id_collisions": {
            iid: count
            for iid, count in candidate_counts.items()
            if iid and count > 1
        },
        "alcohol_products": sum(leaf_counts.values()),
        "alcohol_leaf_counts": tree_leaf_counts,
        "kids_sparkling_products": kids_count,
        "functional_products": functional_count,
        "moves": len(moves),
        "brand_decisions": len(explicit_brands),
        "property_decision_products": len(property_overrides),
        "fallback_counts": dict(fallback_counts),
        "hashes": {
            "source_termek_payloads": source_terms_hash,
            "candidate_termek_payloads": candidate_terms_hash,
            "source_outside_products": source_outside_hash,
            "candidate_outside_products": candidate_outside_hash,
            "source_outside_tree": source_tree_outside_hash,
            "candidate_outside_tree": candidate_tree_outside_hash,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--products", type=Path, required=True)
    parser.add_argument("--categories", type=Path, required=True)
    parser.add_argument("--source-products", type=Path, required=True)
    parser.add_argument("--source-categories", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    args = parser.parse_args()

    try:
        products = load_json(args.products)
        categories = load_json(args.categories)
        source_products = load_json(args.source_products)
        source_categories = load_json(args.source_categories)
        decisions = load_json(args.decisions)
        result = validate(
            products,
            categories,
            source_products,
            source_categories,
            decisions,
        )
    except Exception as exc:
        result = {
            "status": "error",
            "error_count": 1,
            "errors": [f"{type(exc).__name__}: {exc}"],
            "errors_truncated": False,
        }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
