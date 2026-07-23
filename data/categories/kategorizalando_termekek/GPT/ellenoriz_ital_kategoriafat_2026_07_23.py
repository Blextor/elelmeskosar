# -*- coding: utf-8 -*-
"""Az Ital 2026-07-23-i kategóriafa-migrációjának csak olvasó ellenőrzője.

Az ellenőrző nem importálja a migrációs scriptet, és nem ír fájlt. A termék-
és kategóriafájl útvonala felülírható a ``--products`` és ``--categories``
kapcsolókkal. A standard kimenetre egy JSON-összegzést ír, majd siker esetén
0, hiba esetén 1 kilépési kóddal fejeződik be.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


BASE = Path(__file__).resolve().parent
DEFAULT_PRODUCTS = BASE / "eredmeny.json"
DEFAULT_CATEGORIES = BASE / "kategoriak_2026-06-13.json"

ITAL = "Ital"
PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"

EXPECTED_TOTAL_PRODUCTS = 47030
EXPECTED_ITAL_PRODUCTS = 12810

EXPECTED_HIERARCHY: dict[str, tuple[str, ...]] = {
    "Víz és vízalapú italok": (
        "Ízesítetlen palackozott víz",
        "Ízesített víz",
    ),
    "Alkoholos italok és alkoholmentes alternatívák": (
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
    "Üdítőitalok": (
        "Kóla",
        "Tonik",
        "Jegestea",
        "Limonádé",
        "Aloe vera ital",
        "Gyömbér- és gyökéralapú üdítőital",
        "Kombucha",
        "Egyéb ízesített üdítőital",
    ),
    "Gyümölcs- és zöldségitalok": (
        "Lé",
        "Nektár",
        "Gyümölcsital",
        "Smoothie és püréital",
    ),
    "Funkcionális és teljesítményitalok": (
        "Energiaital",
        "Sport- és izotóniás ital",
        "Vitamin- és wellnessital",
        "Egyéb funkcionális ital",
    ),
    "Növényi italok": (
        "Egynövényes ital",
        "Kevert növényi ital",
    ),
    "Kávé-, tea- és kakaótermékek": (
        "Kávé",
        "Tea",
        "Kakaó és forró csokoládé",
        "Kávé- és teaadalék",
    ),
    "Italkészítési alapok": (
        "Italszirup és folyékony koncentrátum",
        "Italpor és tabletta",
    ),
}

EXPECTED_ITAL_LEAVES = frozenset(
    (alkategoria, altipus)
    for alkategoria, altipusok in EXPECTED_HIERARCHY.items()
    for altipus in altipusok
)

ALCOHOL_BRANCH = "Alkoholos italok és alkoholmentes alternatívák"
ALCOHOL_STATUSES = frozenset({"alkoholos", "alkoholmentes"})
WATER_BRANCH = "Víz és vízalapú italok"
CARBONATED_SOFT_DRINK_LEAVES = frozenset({"Kóla", "Tonik"})

NESQUIK_ID = "209545089"
CITRIORANGE_ID = "440767:3978151"
NESQUIK_TARGET = (
    "Alapanyag, sütés-főzés",
    "Szószok, öntetek, dresszingek",
    "Desszertszósz, topping",
)

CITRUS_TARGET = (
    "Alapanyag, sütés-főzés",
    "Olaj, ecet, zsiradék",
    "Citruslé és citrusízesítő",
)

# A migráció előtti ``Ital > Citromlé`` ág 65, egyedi azonosítójú rekordja.
CITRUS_PRODUCT_IDS = frozenset(
    {
        "10003679",
        "1010432",
        "1010441",
        "1058935",
        "121219318",
        "121219399",
        "121219508",
        "121219543",
        "121229767",
        "121230033",
        "121237665",
        "121283816",
        "121283822",
        "121289107",
        "121289113",
        "121338102",
        "209793268",
        "27b5bd0f8e935d1b860a7305",
        "2807088",
        "2807365",
        "2807796",
        "2807797",
        "2808508",
        "2808606",
        "285cd4a524cadba65471edb6",
        "3375575",
        "440767:3978151",
        "440770:3978154",
        "440773:3978157",
        "4886a2e48ee9872b04d561ed",
        "5162c1810e532869e97adf43",
        "581176:4118566",
        "581179:4118569",
        "648e9895345ef1e9fa3edd2d",
        "674825:4212215",
        "674828:4212218",
        "679094:4216484",
        "684140:4221530",
        "684293:4221683",
        "684971:4222361",
        "684974:4222364",
        "684977:4222367",
        "684980:4222370",
        "712622:4250012",
        "8ea9f0066c4b0b7572cf6f92",
        "950864:4488254",
        "969257",
        "9beb5f18ac67b48a7776f87a",
        "BTY-X14844700320021",
        "BTY-X17193200320021",
        "BTY-X17193300320021",
        "BTY-X17426100320021",
        "BTY-X17426200320021",
        "BTY-X17426300320021",
        "BTY-X17426400320021",
        "BTY-X17476800320021",
        "BTY-X17540500320021",
        "BTY-X17540700320021",
        "BTY-X17939100320021",
        "BTY-X17945700320021",
        "a6dae5b7901b0117574e0290",
        "aeccbc873aa7effe517c9bcf",
        "b7d8eeee0b1d6c11b70e030f",
        "d2118e088e54e90b075cc940",
        "e806055a2c6933e690c217aa",
    }
)

NUMERIC_ALCOHOL_RE = re.compile(r"^\d+(?:[,.]\d+)?%$")
MAX_SAMPLES_PER_FAILURE = 20


class DuplicateJsonKeyError(ValueError):
    """A bemeneti JSON egy objektuma ugyanazt a kulcsot többször tartalmazza."""


@dataclass(frozen=True)
class Declaration:
    shape: str
    allowed_values: tuple[Any, ...] | None


class FailureCollector:
    """Darabszámot és korlátozott mintát gyűjt hibatípusonként."""

    def __init__(self) -> None:
        self._rows: dict[str, dict[str, Any]] = {}
        self._seen: dict[str, set[str]] = defaultdict(set)

    def add(self, key: str, detail: Any) -> None:
        identity = json.dumps(detail, ensure_ascii=False, sort_keys=True, default=str)
        if identity in self._seen[key]:
            return
        self._seen[key].add(identity)
        row = self._rows.setdefault(key, {"count": 0, "samples": []})
        row["count"] += 1
        if len(row["samples"]) < MAX_SAMPLES_PER_FAILURE:
            row["samples"].append(detail)

    def add_mismatch(self, key: str, expected: Any, actual: Any) -> None:
        if actual != expected:
            self.add(key, {"expected": expected, "actual": actual})

    def as_dict(self) -> dict[str, dict[str, Any]]:
        return dict(sorted(self._rows.items()))

    def __bool__(self) -> bool:
        return bool(self._rows)


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateJsonKeyError(f"Duplikált JSON-kulcs: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=reject_duplicate_keys)


def fold(value: Any) -> str:
    text = unicodedata.normalize("NFKD", "" if value is None else str(value))
    text = "".join(char for char in text if not unicodedata.combining(char)).casefold()
    text = "".join(char if char.isalnum() else " " for char in text)
    return " ".join(text.split())


def product_id(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("store_product_id") or "")


def product_name(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("product_name") or "")


def product_path(product: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(product.get("fokategoria") or ""),
        str(product.get("alkategoria") or ""),
        str(product.get("altipus") or ""),
    )


def product_context(index: int, product: dict[str, Any]) -> dict[str, Any]:
    return {
        "index": index,
        "product_id": product_id(product),
        "name": product_name(product),
        "path": list(product_path(product)),
    }


def value_shape(value: Any) -> str:
    if isinstance(value, bool):
        return "flag"
    if isinstance(value, list):
        return "multi"
    if isinstance(value, dict):
        return "object"
    return "single"


def category_hash(product: dict[str, Any]) -> str:
    key = "|".join(
        [
            str(product.get("fokategoria") or ""),
            str(product.get("alkategoria") or ""),
            str(product.get("altipus") or ""),
            json.dumps(
                product.get("tulajdonsagok") or {},
                sort_keys=True,
                ensure_ascii=False,
            ),
        ]
    )
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def get_node(tree: dict[str, Any], path: tuple[str, ...]) -> dict[str, Any] | None:
    if not path:
        return None
    node = tree.get(path[0])
    if not isinstance(node, dict):
        return None
    if len(path) >= 2:
        children = node.get(ALK_KEY) or {}
        if not isinstance(children, dict):
            return None
        node = children.get(path[1])
        if not isinstance(node, dict):
            return None
    if len(path) >= 3:
        children = node.get(ALT_KEY) or {}
        if not isinstance(children, dict):
            return None
        node = children.get(path[2])
        if not isinstance(node, dict):
            return None
    return node


def allowed_value_key(value: Any) -> tuple[str, str]:
    if isinstance(value, str):
        return ("str", fold(value))
    return (type(value).__name__, repr(value))


def parse_local_declarations(
    node: dict[str, Any],
    path: tuple[str, ...],
    failures: FailureCollector,
    cache: dict[tuple[str, ...], dict[str, Declaration]],
) -> dict[str, Declaration]:
    if path in cache:
        return cache[path]

    result: dict[str, Declaration] = {}
    seen_property_names: dict[str, tuple[str, str]] = {}
    block = node.get(PROP_KEY, {})
    if not isinstance(block, dict):
        failures.add(
            "tree_invalid_property_block",
            {"path": list(path), "actual_type": type(block).__name__},
        )
        cache[path] = result
        return result

    for group_name in ("egyedi", "csoportos"):
        group = block.get(group_name, {})
        if not isinstance(group, dict):
            failures.add(
                "tree_invalid_property_group",
                {
                    "path": list(path),
                    "group": group_name,
                    "actual_type": type(group).__name__,
                },
            )
            continue
        for property_name, raw_declaration in group.items():
            if not isinstance(property_name, str) or not property_name.strip():
                failures.add(
                    "tree_invalid_property_name",
                    {"path": list(path), "group": group_name, "property": property_name},
                )
                continue
            folded_name = fold(property_name)
            if folded_name in seen_property_names:
                previous_name, previous_group = seen_property_names[folded_name]
                failures.add(
                    "tree_duplicate_local_property",
                    {
                        "path": list(path),
                        "property": property_name,
                        "group": group_name,
                        "previous_property": previous_name,
                        "previous_group": previous_group,
                    },
                )
                continue
            seen_property_names[folded_name] = (property_name, group_name)

            if group_name == "egyedi" and isinstance(raw_declaration, dict):
                if raw_declaration:
                    failures.add(
                        "tree_nonempty_flag_declaration",
                        {
                            "path": list(path),
                            "property": property_name,
                            "value": raw_declaration,
                        },
                    )
                result[property_name] = Declaration("flag", None)
                continue

            if not isinstance(raw_declaration, list):
                failures.add(
                    "tree_invalid_property_declaration",
                    {
                        "path": list(path),
                        "property": property_name,
                        "group": group_name,
                        "actual_type": type(raw_declaration).__name__,
                    },
                )
                continue

            shape = "single" if group_name == "egyedi" else "multi"
            if not raw_declaration:
                failures.add(
                    "tree_empty_allowed_values",
                    {"path": list(path), "property": property_name, "shape": shape},
                )

            seen_values: dict[tuple[str, str], Any] = {}
            for allowed_value in raw_declaration:
                if (
                    allowed_value is None
                    or isinstance(allowed_value, (bool, dict, list))
                    or (isinstance(allowed_value, str) and not allowed_value.strip())
                ):
                    failures.add(
                        "tree_invalid_allowed_value",
                        {
                            "path": list(path),
                            "property": property_name,
                            "value": allowed_value,
                        },
                    )
                    continue
                key = allowed_value_key(allowed_value)
                # A feladat szigorú értékatomicitási hatóköre az Ital fa.
                # A két külső célág örökölt, korábban is meglévő listáiban
                # előforduló alakváltozatokat nem tekintjük új Ital-hibának.
                if key in seen_values and path[0] == ITAL:
                    failures.add(
                        "tree_duplicate_allowed_value",
                        {
                            "path": list(path),
                            "property": property_name,
                            "value": allowed_value,
                            "previous_value": seen_values[key],
                        },
                    )
                else:
                    seen_values[key] = allowed_value

            result[property_name] = Declaration(shape, tuple(raw_declaration))

    cache[path] = result
    return result


def effective_declarations(
    tree: dict[str, Any],
    path: tuple[str, str, str],
    failures: FailureCollector,
    cache: dict[tuple[str, ...], dict[str, Declaration]],
    *,
    scope: str,
) -> dict[str, Declaration]:
    levels = (
        (path[0],),
        (path[0], path[1]),
        path,
    )
    result: dict[str, Declaration] = {}
    seen_folded: dict[str, tuple[str, tuple[str, ...]]] = {}

    for level_path in levels:
        node = get_node(tree, level_path)
        if node is None:
            failures.add(
                f"{scope}_missing_tree_node",
                {"path": list(level_path), "product_path": list(path)},
            )
            return {}
        local = parse_local_declarations(node, level_path, failures, cache)
        for property_name, declaration in local.items():
            folded_name = fold(property_name)
            if folded_name in seen_folded:
                previous_name, previous_path = seen_folded[folded_name]
                failures.add(
                    f"{scope}_property_redefinitions",
                    {
                        "product_path": list(path),
                        "property": property_name,
                        "declared_at": list(level_path),
                        "previous_property": previous_name,
                        "previous_declared_at": list(previous_path),
                    },
                )
                continue
            seen_folded[folded_name] = (property_name, level_path)
            result[property_name] = declaration
    return result


def validate_product_properties(
    index: int,
    product: dict[str, Any],
    declarations: dict[str, Declaration],
    failures: FailureCollector,
    *,
    scope: str,
) -> None:
    context = product_context(index, product)
    properties = product.get("tulajdonsagok")
    if not isinstance(properties, dict):
        failures.add(
            f"{scope}_invalid_property_object",
            {**context, "actual_type": type(properties).__name__},
        )
        return

    declared_by_fold = {fold(name): name for name in declarations}
    seen_product_names: dict[str, str] = {}
    for property_name, raw_value in properties.items():
        folded_name = fold(property_name)
        if folded_name in seen_product_names:
            failures.add(
                f"{scope}_duplicate_folded_product_property",
                {
                    **context,
                    "property": property_name,
                    "previous_property": seen_product_names[folded_name],
                },
            )
        else:
            seen_product_names[folded_name] = property_name

        declaration = declarations.get(property_name)
        if declaration is None:
            failures.add(
                f"{scope}_undeclared_product_property",
                {
                    **context,
                    "property": property_name,
                    "folded_match": declared_by_fold.get(folded_name),
                },
            )
            continue

        actual_shape = value_shape(raw_value)
        if actual_shape != declaration.shape:
            failures.add(
                f"{scope}_property_shape_mismatch",
                {
                    **context,
                    "property": property_name,
                    "expected": declaration.shape,
                    "actual": actual_shape,
                    "value": raw_value,
                },
            )
            continue

        if declaration.shape == "flag":
            continue

        values: Iterable[Any]
        if declaration.shape == "multi":
            values = raw_value
            if not raw_value:
                failures.add(
                    f"{scope}_empty_product_property",
                    {**context, "property": property_name, "value": raw_value},
                )
        else:
            values = (raw_value,)

        allowed_values = declaration.allowed_values or ()
        for value in values:
            if (
                value is None
                or isinstance(value, (bool, dict, list))
                or (isinstance(value, str) and not value.strip())
            ):
                failures.add(
                    f"{scope}_invalid_product_property_value",
                    {
                        **context,
                        "property": property_name,
                        "value": value,
                    },
                )
                continue
            if value not in allowed_values:
                failures.add(
                    f"{scope}_undeclared_property_value",
                    {
                        **context,
                        "property": property_name,
                        "value": value,
                    },
                )


def collect_declared_ital_leaves(
    categories: dict[str, Any],
    failures: FailureCollector,
) -> set[tuple[str, str]]:
    root = categories.get(ITAL)
    if not isinstance(root, dict):
        failures.add("missing_ital_root", {"root": ITAL})
        return set()

    raw_alkategoriak = root.get(ALK_KEY)
    if not isinstance(raw_alkategoriak, dict):
        failures.add(
            "invalid_ital_subcategory_container",
            {"actual_type": type(raw_alkategoriak).__name__},
        )
        return set()

    expected_parents = set(EXPECTED_HIERARCHY)
    actual_parents = set(raw_alkategoriak)
    for name in sorted(expected_parents - actual_parents, key=fold):
        failures.add("missing_ital_subcategory", {"alkategoria": name})
    for name in sorted(actual_parents - expected_parents, key=fold):
        failures.add("unexpected_ital_subcategory", {"alkategoria": name})

    declared: set[tuple[str, str]] = set()
    for alkategoria, node in raw_alkategoriak.items():
        if not isinstance(node, dict):
            failures.add(
                "invalid_ital_subcategory_node",
                {"alkategoria": alkategoria, "actual_type": type(node).__name__},
            )
            continue
        raw_altipusok = node.get(ALT_KEY)
        if not isinstance(raw_altipusok, dict):
            failures.add(
                "invalid_ital_leaf_container",
                {
                    "alkategoria": alkategoria,
                    "actual_type": type(raw_altipusok).__name__,
                },
            )
            continue
        expected_altipusok = set(EXPECTED_HIERARCHY.get(alkategoria, ()))
        actual_altipusok = set(raw_altipusok)
        for name in sorted(expected_altipusok - actual_altipusok, key=fold):
            failures.add(
                "missing_ital_leaf",
                {"alkategoria": alkategoria, "altipus": name},
            )
        for name in sorted(actual_altipusok - expected_altipusok, key=fold):
            failures.add(
                "unexpected_ital_leaf",
                {"alkategoria": alkategoria, "altipus": name},
            )
        declared.update((alkategoria, altipus) for altipus in actual_altipusok)
    return declared


def validate_hash(
    index: int,
    product: dict[str, Any],
    failures: FailureCollector,
    *,
    scope: str,
) -> None:
    expected = category_hash(product)
    actual = product.get("kategoria_hash")
    if actual != expected:
        failures.add(
            f"{scope}_category_hash",
            {
                **product_context(index, product),
                "expected": expected,
                "actual": actual,
            },
        )


def validate_special_ital_semantics(
    index: int,
    product: dict[str, Any],
    failures: FailureCollector,
) -> None:
    _fokategoria, alkategoria, altipus = product_path(product)
    properties = product.get("tulajdonsagok") or {}
    if not isinstance(properties, dict):
        return
    context = product_context(index, product)

    if alkategoria == ALCOHOL_BRANCH:
        status = properties.get("alkoholstátusz")
        if not isinstance(status, str) or status not in ALCOHOL_STATUSES:
            failures.add(
                "alcohol_status",
                {
                    **context,
                    "expected": sorted(ALCOHOL_STATUSES),
                    "actual": status,
                    "actual_shape": value_shape(status),
                },
            )

    numeric_alcohol_values: list[float] = []
    if "alkoholtartalom" in properties:
        raw_alcohol = properties["alkoholtartalom"]
        alcohol_values = raw_alcohol if isinstance(raw_alcohol, list) else [raw_alcohol]
        for value in alcohol_values:
            if not isinstance(value, str) or not NUMERIC_ALCOHOL_RE.fullmatch(value.strip()):
                failures.add(
                    "categorical_or_invalid_alcohol_content",
                    {**context, "value": value},
                )
            else:
                numeric_alcohol_values.append(
                    float(value.strip().removesuffix("%").replace(",", "."))
                )

    if alkategoria == ALCOHOL_BRANCH:
        status = properties.get("alkoholstátusz")
        if status == "alkoholmentes":
            if not numeric_alcohol_values or max(numeric_alcohol_values) > 0.5:
                failures.add(
                    "alcohol_status_content_mismatch",
                    {
                        **context,
                        "status": status,
                        "alcohol_values": numeric_alcohol_values,
                        "expected": "legalább egy numerikus, legfeljebb 0,5%-os érték",
                    },
                )
        elif (
            status == "alkoholos"
            and numeric_alcohol_values
            and max(numeric_alcohol_values) <= 0.5
        ):
            failures.add(
                "alcohol_status_content_mismatch",
                {
                    **context,
                    "status": status,
                    "alcohol_values": numeric_alcohol_values,
                    "expected": "0,5%-nál nagyobb érték vagy hiányzó alkoholfok",
                },
            )

    for property_name, raw_value in properties.items():
        atoms = raw_value if isinstance(raw_value, list) else [raw_value]
        for value in atoms:
            if not isinstance(value, str):
                continue
            folded_value = fold(value)
            if folded_value in {
                "gyumolcs es zoldsegle",
                "kavefeherito vagy tejpor",
            }:
                failures.add(
                    "compound_non_atomic_property_value",
                    {
                        **context,
                        "property": property_name,
                        "value": value,
                    },
                )
            if property_name == "márka" and value == "Katona Nálad Vagy Nálam":
                failures.add(
                    "brand_contains_product_variant",
                    {
                        **context,
                        "value": value,
                        "expected_brand": "Katona",
                    },
                )

    if alkategoria == "Üdítőitalok" and altipus in CARBONATED_SOFT_DRINK_LEAVES:
        carbonation = properties.get("szénsavasság")
        if not isinstance(carbonation, str) or fold(carbonation) != fold("szénsavas"):
            failures.add(
                "cola_or_tonic_not_carbonated",
                {**context, "actual": carbonation},
            )

    if alkategoria == WATER_BRANCH:
        carbonation = properties.get("szénsavasság")
        if not isinstance(carbonation, str) or not carbonation.strip():
            failures.add(
                "water_carbonation_not_scalar",
                {
                    **context,
                    "actual": carbonation,
                    "actual_shape": value_shape(carbonation),
                },
            )


def validate_moved_products(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
    by_id: dict[str, list[tuple[int, dict[str, Any]]]],
    failures: FailureCollector,
    declaration_cache: dict[tuple[str, ...], dict[str, Declaration]],
) -> dict[str, int]:
    target_declaration_cache: dict[tuple[str, str, str], dict[str, Declaration]] = {}

    def declarations_for(path: tuple[str, str, str]) -> dict[str, Declaration]:
        if path not in target_declaration_cache:
            target_declaration_cache[path] = effective_declarations(
                categories,
                path,
                failures,
                declaration_cache,
                scope="moved_target",
            )
        return target_declaration_cache[path]

    nesquik_matches = by_id.get(NESQUIK_ID, [])
    if len(nesquik_matches) != 1:
        failures.add(
            "nesquik_record_count",
            {"product_id": NESQUIK_ID, "expected": 1, "actual": len(nesquik_matches)},
        )
    else:
        index, product = nesquik_matches[0]
        actual_path = product_path(product)
        if actual_path != NESQUIK_TARGET:
            failures.add(
                "nesquik_target_path",
                {
                    **product_context(index, product),
                    "expected": list(NESQUIK_TARGET),
                },
            )
        else:
            validate_product_properties(
                index,
                product,
                declarations_for(NESQUIK_TARGET),
                failures,
                scope="nesquik_target",
            )
        validate_hash(index, product, failures, scope="nesquik")

    citrus_target_rows = [
        (index, product)
        for index, product in enumerate(products)
        if product_path(product) == CITRUS_TARGET
    ]
    citrus_target_ids = {product_id(product) for _index, product in citrus_target_rows}
    failures.add_mismatch(
        "citrus_target_product_count",
        len(CITRUS_PRODUCT_IDS),
        len(citrus_target_rows),
    )
    for missing_id in sorted(CITRUS_PRODUCT_IDS - citrus_target_ids):
        failures.add("citrus_target_missing_id", {"product_id": missing_id})
    for unexpected_id in sorted(citrus_target_ids - CITRUS_PRODUCT_IDS):
        failures.add("citrus_target_unexpected_id", {"product_id": unexpected_id})

    citrus_declarations = declarations_for(CITRUS_TARGET)
    checked_citrus = 0
    for item_id in sorted(CITRUS_PRODUCT_IDS):
        matches = by_id.get(item_id, [])
        if len(matches) != 1:
            failures.add(
                "citrus_record_count",
                {"product_id": item_id, "expected": 1, "actual": len(matches)},
            )
            continue
        index, product = matches[0]
        actual_path = product_path(product)
        if actual_path != CITRUS_TARGET:
            failures.add(
                "citrus_target_path",
                {
                    **product_context(index, product),
                    "expected": list(CITRUS_TARGET),
                },
            )
        else:
            validate_product_properties(
                index,
                product,
                citrus_declarations,
                failures,
                scope="citrus_target",
            )
            if (
                item_id == CITRIORANGE_ID
                and (product.get("tulajdonsagok") or {}).get("terméktípus")
                != ["narancslé-koncentrátum"]
            ):
                failures.add(
                    "citriorange_wrong_product_type",
                    {
                        **product_context(index, product),
                        "actual": (product.get("tulajdonsagok") or {}).get(
                            "terméktípus"
                        ),
                        "expected": ["narancslé-koncentrátum"],
                    },
                )
            checked_citrus += 1
        validate_hash(index, product, failures, scope="citrus")

    return {
        "nesquik_records": len(nesquik_matches),
        "citrus_ids_expected": len(CITRUS_PRODUCT_IDS),
        "citrus_records_on_target": len(citrus_target_rows),
        "citrus_records_fully_checked": checked_citrus,
    }


def run_checks(
    products: Any,
    categories: Any,
    products_path: Path,
    categories_path: Path,
) -> tuple[dict[str, Any], bool]:
    failures = FailureCollector()
    if not isinstance(products, list):
        failures.add(
            "invalid_product_collection",
            {"actual_type": type(products).__name__},
        )
        product_rows: list[dict[str, Any]] = []
    else:
        product_rows = []
        for index, product in enumerate(products):
            if isinstance(product, dict):
                product_rows.append(product)
            else:
                failures.add(
                    "invalid_product_record",
                    {"index": index, "actual_type": type(product).__name__},
                )

    if not isinstance(categories, dict):
        failures.add(
            "invalid_category_tree",
            {"actual_type": type(categories).__name__},
        )
        category_tree: dict[str, Any] = {}
    else:
        category_tree = categories

    failures.add_mismatch(
        "total_product_count",
        EXPECTED_TOTAL_PRODUCTS,
        len(products) if isinstance(products, list) else None,
    )
    ital_rows = [
        (index, product)
        for index, product in enumerate(product_rows)
        if product.get("fokategoria") == ITAL
    ]
    failures.add_mismatch(
        "ital_product_count",
        EXPECTED_ITAL_PRODUCTS,
        len(ital_rows),
    )

    declared_leaves = collect_declared_ital_leaves(category_tree, failures)
    used_leaves: set[tuple[str, str]] = set()
    empty_altipus_count = 0
    for index, product in ital_rows:
        raw_alkategoria = product.get("alkategoria")
        raw_altipus = product.get("altipus")
        if not isinstance(raw_alkategoria, str) or not isinstance(raw_altipus, str):
            failures.add(
                "invalid_ital_path_value_type",
                {
                    **product_context(index, product),
                    "alkategoria_type": type(raw_alkategoria).__name__,
                    "altipus_type": type(raw_altipus).__name__,
                },
            )
        alkategoria = str(raw_alkategoria or "")
        altipus = str(raw_altipus or "")
        used_leaves.add((alkategoria, altipus))
        if not altipus:
            empty_altipus_count += 1
            failures.add("empty_ital_altipus", product_context(index, product))

    for path in sorted(EXPECTED_ITAL_LEAVES - declared_leaves, key=lambda row: (fold(row[0]), fold(row[1]))):
        failures.add("expected_leaf_not_declared", {"path": list(path)})
    for path in sorted(declared_leaves - EXPECTED_ITAL_LEAVES, key=lambda row: (fold(row[0]), fold(row[1]))):
        failures.add("unexpected_declared_leaf", {"path": list(path)})
    for path in sorted(EXPECTED_ITAL_LEAVES - used_leaves, key=lambda row: (fold(row[0]), fold(row[1]))):
        failures.add("expected_leaf_not_used", {"path": list(path)})
    for path in sorted(used_leaves - EXPECTED_ITAL_LEAVES, key=lambda row: (fold(row[0]), fold(row[1]))):
        failures.add("unexpected_used_leaf", {"path": list(path)})
    for path in sorted(declared_leaves - used_leaves, key=lambda row: (fold(row[0]), fold(row[1]))):
        failures.add("declared_leaf_not_used", {"path": list(path)})
    for path in sorted(used_leaves - declared_leaves, key=lambda row: (fold(row[0]), fold(row[1]))):
        failures.add("used_leaf_not_declared", {"path": list(path)})

    declaration_cache: dict[tuple[str, ...], dict[str, Declaration]] = {}
    effective_by_leaf: dict[tuple[str, str], dict[str, Declaration]] = {}
    for alkategoria, altipus in sorted(
        EXPECTED_ITAL_LEAVES | used_leaves,
        key=lambda row: (fold(row[0]), fold(row[1])),
    ):
        effective_by_leaf[(alkategoria, altipus)] = effective_declarations(
            category_tree,
            (ITAL, alkategoria, altipus),
            failures,
            declaration_cache,
            scope="ital",
        )

    alcohol_products = 0
    water_products = 0
    cola_tonic_products = 0
    for index, product in ital_rows:
        path = (
            str(product.get("alkategoria") or ""),
            str(product.get("altipus") or ""),
        )
        declarations = effective_by_leaf.get(path, {})
        validate_product_properties(
            index,
            product,
            declarations,
            failures,
            scope="ital",
        )
        validate_hash(index, product, failures, scope="ital")
        validate_special_ital_semantics(index, product, failures)
        if path[0] == ALCOHOL_BRANCH:
            alcohol_products += 1
        if path[0] == WATER_BRANCH:
            water_products += 1
        if path[0] == "Üdítőitalok" and path[1] in CARBONATED_SOFT_DRINK_LEAVES:
            cola_tonic_products += 1

    by_id: dict[str, list[tuple[int, dict[str, Any]]]] = defaultdict(list)
    for index, product in enumerate(product_rows):
        by_id[product_id(product)].append((index, product))

    moved_summary = validate_moved_products(
        product_rows,
        category_tree,
        by_id,
        failures,
        declaration_cache,
    )

    payload = {
        "status": "hiba" if failures else "ok",
        "inputs": {
            "products": str(products_path.resolve()),
            "categories": str(categories_path.resolve()),
        },
        "summary": {
            "products": len(products) if isinstance(products, list) else None,
            "ital_products": len(ital_rows),
            "expected_ital_subcategories": len(EXPECTED_HIERARCHY),
            "expected_ital_leaves": len(EXPECTED_ITAL_LEAVES),
            "declared_ital_leaves": len(declared_leaves),
            "used_ital_leaves": len(used_leaves),
            "empty_ital_altipus_products": empty_altipus_count,
            "alcohol_branch_products": alcohol_products,
            "water_branch_products": water_products,
            "cola_and_tonic_products": cola_tonic_products,
            **moved_summary,
        },
        "failures": failures.as_dict(),
    }
    return payload, not failures


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValueError(message)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = JsonArgumentParser(description=__doc__)
    parser.add_argument(
        "--products",
        type=Path,
        default=DEFAULT_PRODUCTS,
        help="Az ellenőrizendő eredmeny.json útvonala",
    )
    parser.add_argument(
        "--categories",
        type=Path,
        default=DEFAULT_CATEGORIES,
        help="Az ellenőrizendő kategóriafa JSON útvonala",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    products = load_json(args.products)
    categories = load_json(args.categories)
    payload, success = run_checks(
        products,
        categories,
        args.products,
        args.categories,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if success else 1


def cli() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    json.encoder.c_make_encoder = None
    try:
        return main()
    except Exception as exc:
        payload = {
            "status": "hiba",
            "summary": {},
            "failures": {
                "runtime_error": {
                    "count": 1,
                    "samples": [
                        {
                            "type": type(exc).__name__,
                            "message": str(exc),
                        }
                    ],
                }
            },
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    sys.exit(cli())
