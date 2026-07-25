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
from collections import Counter, defaultdict
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
EXPECTED_PATH_COUNTS: dict[tuple[str, str], int] = {
    ("Víz és vízalapú italok", "Ízesítetlen palackozott víz"): 420,
    ("Víz és vízalapú italok", "Ízesített víz"): 93,
    (
        "Alkoholos italok és alkoholmentes alternatívák",
        "Bor és boralapú ital",
    ): 2128,
    (
        "Alkoholos italok és alkoholmentes alternatívák",
        "Pezsgő, habzóbor és gyöngyözőbor",
    ): 560,
    (
        "Alkoholos italok és alkoholmentes alternatívák",
        "Sör, radler és malátaital",
    ): 1015,
    ("Alkoholos italok és alkoholmentes alternatívák", "Cider"): 73,
    ("Alkoholos italok és alkoholmentes alternatívák", "Likőr"): 601,
    (
        "Alkoholos italok és alkoholmentes alternatívák",
        "Whisky és bourbon",
    ): 241,
    ("Alkoholos italok és alkoholmentes alternatívák", "Gin"): 135,
    ("Alkoholos italok és alkoholmentes alternatívák", "Rum"): 120,
    ("Alkoholos italok és alkoholmentes alternatívák", "Tequila"): 21,
    ("Alkoholos italok és alkoholmentes alternatívák", "Vodka"): 188,
    ("Alkoholos italok és alkoholmentes alternatívák", "Pálinka"): 133,
    ("Alkoholos italok és alkoholmentes alternatívák", "Brandy"): 41,
    (
        "Alkoholos italok és alkoholmentes alternatívák",
        "Vermut és aperitif",
    ): 33,
    (
        "Alkoholos italok és alkoholmentes alternatívák",
        "Egyéb szeszes ital",
    ): 86,
    (
        "Alkoholos italok és alkoholmentes alternatívák",
        "Koktél és előre kevert ital",
    ): 125,
    ("Üdítőitalok", "Kóla"): 349,
    ("Üdítőitalok", "Tonik"): 87,
    ("Üdítőitalok", "Jegestea"): 482,
    ("Üdítőitalok", "Limonádé"): 93,
    ("Üdítőitalok", "Aloe vera ital"): 21,
    ("Üdítőitalok", "Gyömbér- és gyökéralapú üdítőital"): 57,
    ("Üdítőitalok", "Kombucha"): 17,
    ("Üdítőitalok", "Egyéb ízesített üdítőital"): 689,
    ("Gyümölcs- és zöldségitalok", "Lé"): 379,
    ("Gyümölcs- és zöldségitalok", "Nektár"): 84,
    ("Gyümölcs- és zöldségitalok", "Gyümölcsital"): 815,
    ("Gyümölcs- és zöldségitalok", "Smoothie és püréital"): 117,
    ("Funkcionális és teljesítményitalok", "Energiaital"): 341,
    (
        "Funkcionális és teljesítményitalok",
        "Sport- és izotóniás ital",
    ): 86,
    (
        "Funkcionális és teljesítményitalok",
        "Vitamin- és wellnessital",
    ): 155,
    (
        "Funkcionális és teljesítményitalok",
        "Egyéb funkcionális ital",
    ): 147,
    ("Növényi italok", "Egynövényes ital"): 200,
    ("Növényi italok", "Kevert növényi ital"): 31,
    ("Kávé-, tea- és kakaótermékek", "Kávé"): 1301,
    ("Kávé-, tea- és kakaótermékek", "Tea"): 760,
    (
        "Kávé-, tea- és kakaótermékek",
        "Kakaó és forró csokoládé",
    ): 138,
    ("Kávé-, tea- és kakaótermékek", "Kávé- és teaadalék"): 24,
    (
        "Italkészítési alapok",
        "Italszirup és folyékony koncentrátum",
    ): 395,
    ("Italkészítési alapok", "Italpor és tabletta"): 29,
}

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
SIMPLE_QUANTITY_RE = re.compile(
    r"^\d+(?:,\d+)? (?:kg|g|ml|cl|dl|l|db)$",
    flags=re.IGNORECASE,
)
NAME_QUANTITY_RE = re.compile(
    r"(?<!\d)\d+(?:[.,]\d+)?\s*(?:kg|ml|cl|dl|l|gr|g)\b",
    flags=re.IGNORECASE,
)
CHILD_NAME_RE = re.compile(
    r"\b(?:gyerek\w*|gyermek\w*|kids?|baby|junior|babaviz|babaknak)\b"
    r"|\bbaba\s+mama\b"
)

FRUIT_BRANCH = "Gyümölcs- és zöldségitalok"
HOT_BRANCH = "Kávé-, tea- és kakaótermékek"
BASE_BRANCH = "Italkészítési alapok"
SOFT_BRANCH = "Üdítőitalok"
FRUIT_STEP_GINGER_ID = "121283822"

# A kézzel felülvizsgált célcsoportok pontos termékazonosító-hash-ei. A hash
# megakadályozza, hogy az elvárt darabszámok mellett más termékek cserélődjenek
# be ugyanabba a csoportba.
EXPECTED_FRUIT_LEAF_GROUPS: dict[str, tuple[int, str]] = {
    "Lé": (
        379,
        "dc0dc2ddf0e986eefd96680a448c81fac3278098fbf7c99bcc09358838cf6a1e",
    ),
    "Nektár": (
        84,
        "78875cd3c852a1cf845640020a403680db4e032aa4bb0f75e5d241d318231c0a",
    ),
    "Gyümölcsital": (
        815,
        "07c552b8b1236c34da546a1097bd31340bdf6acfc8d9bbd17159aa7d12b11701",
    ),
    "Smoothie és püréital": (
        117,
        "9870809283259341262061a8872102cdee210bf2ca66d880877f366311b7cc6a",
    ),
}
EXPECTED_JUICE_TYPE_GROUPS: dict[tuple[str, ...], tuple[int, str]] = {
    ("gyümölcslé",): (
        289,
        "3038c32cb8d6d664aafa8e379e70e58003d858419f7b325216c2c6e5cc65809d",
    ),
    ("zöldséglé",): (
        55,
        "68c5e4fe73698c3aeac5987e2e549be44b54e39aac3ab9061b7600537c4d90fb",
    ),
    ("gyümölcslé", "zöldséglé"): (
        35,
        "63cc74d5bf386fb5a3a7f10b4f69cd1a1feb6bcfb840237826da94f4279a8aab",
    ),
}

EXPECTED_MAIN_BRAND_GROUPS: dict[str, tuple[int, str]] = {
    "Douwe Egberts": (
        93,
        "6f536ee6a62051078bb0de5fc3be0bb574a114740ab0ae0c4c4a071508d458b5",
    ),
    "Peroni": (
        34,
        "5a206256809cab91c399ff0a0f990af1e1e9c6052f900cfb598ce60773bbabcb",
    ),
    "RIO": (
        31,
        "74fc7b2ac8f01b026ed68337a9e6a99c9cfec37cb20531aa75df2b9eb1d0315d",
    ),
    "Rio D'Oro": (
        29,
        "fb444143fa5630b48fd2a1f306a2882786072b6da033190ae6f48117bbbea224",
    ),
    "Swiss Laboratory": (
        19,
        "ae2f88b2eabee58343470925217537dc6b19ec3670219909307bb4d0f3582d34",
    ),
    "Theodora": (
        77,
        "1577278b7b34f5c68f3e5f01e5c189450d2a47f1adec84a8def20bc79b127338",
    ),
    "Panyolai": (
        22,
        "3390781439179f967df2168ce9e9e63f8aeb78ccb93066e06abcb2b5a0117820",
    ),
    "Günzer Tamás": (
        33,
        "aac6db593d01ec2a7fb5fe5c5788be79f18086e4d4d9027717d522bb51674f2b",
    ),
    "YO": (
        19,
        "1962a7bac78ae038c1f31f4e17c40d1ca1d7d7cacd66deb9c3d1208a8a3276ba",
    ),
    "Asahi": (
        8,
        "a39e805383b19fcf69653b2be8bd0e7fc4eec89d871ce5de7cac4bea54922e84",
    ),
    "Angyal Borászat": (
        8,
        "5562fec62aa40ef94caeed7a514c1594d69be6db294f8fab00d6d0e22949b6f1",
    ),
    "Limenita": (
        9,
        "fb5cc2037f30c03badc49275bbe8ca6d917c160ca1593a5dccc6517c1d799f69",
    ),
    "Kozel": (
        9,
        "0975954388b219cfcd5e63a3101f0597ad14c49321d0d480cef58d0be9d08e60",
    ),
    "Sodastream": (
        8,
        "dcc11f8334de93cfce9fbce5236f3fd5e31fb920d49b6bc2a5d885f059f75289",
    ),
    "Bols": (
        8,
        "42e113d4c6b60465bc0cc988e2ed457fb05c02022f0fa1dcd689d36a5d2df69e",
    ),
    "BE(er) Cool": (
        7,
        "b3fb50e94724c524f132a50ce39e5643aeba0973562337ab7cdfcfd4b79f2653",
    ),
}
EXPECTED_BRAND_RECORDS = 12720
EXPECTED_UNIQUE_BRANDS = 1105
EXPECTED_BRAND_ASSIGNMENT_SHA256 = (
    "eb26ce417916b1272a850d5f8eda32fc6359f623ca7d41f47f5d8e043c05cfca"
)
FORBIDDEN_BRAND_VALUES = frozenset(
    {
        "African Rock Selection",
        "ANGYAL",
        "Angyal Borászat Mosoly Tokaji Édes Cuvée",
        "Aperitivo Bianco",
        "Aperitivo Cherry",
        "Arran Barrel Reserve",
        "ASAHI",
        "Asahi Super Dry",
        "AVE Aloe Vera",
        "Bad Dogs Bulldog IPA",
        "Bad Dogs Mopsz Meggy",
        "Bad Dogs Puli Pils",
        "BEERCOOL",
        "BOLYKI",
        "Bolyki János",
        "Bols Advocaat",
        "Bols Marine",
        "Bostavan Gold Premium",
        "Bulleit Bourbon",
        "Desszert Triple Sec",
        "Douwe Egberts Omnia",
        "Douwe Egberts Paloma",
        "Dr. Chen Patika",
        "Dúzsi Tamás",
        "Egri Korona Borház",
        "Emese",
        "egyéb",
        "Fantasy Cabernet Sauvignon",
        "Fantasy Chardonnay",
        "Fantasy Muscat Rose",
        "FEHÉRVÁRI Borbirtok",
        "Fonte Active",
        "Fonte Beauty",
        "Fonte Boost",
        "Fonte Natura",
        "Frescanti Cherry",
        "Gere Tamás",
        "Gedeon Birtok Brut",
        "Günzer",
        "Haas Classic",
        "HB",
        "Horizont Brewing",
        "Ikon Pincészet",
        "Katona Nálad Vagy Nálam",
        "Krušovice Černé",
        "Krušovice Originál",
        "La Festa Hot Chocolatta Classico",
        "Laposa Méthode Charmat",
        "Limenita Freshing Coolture",
        "Limenita Golden Sweet",
        "London Fruit & Herb Company",
        "Maczkó Medve Álom",
        "MATUA",
        "Matua Valley",
        "Mészáros",
        "Monkey Shoulder The Original",
        "Nestlé Ricoré 3in1",
        "Nicolaus Extra Fine",
        "NIKKA",
        "Nikka Days",
        "Ostoros Hugo Spritz",
        "Paloma Classic",
        "Pannonhalmi Tricollis",
        "Pannonhalmi Tricollis Fehér",
        "Panyolai Elixír",
        "PATRON",
        "Patrón Silver",
        "Peroni Nastro Azzurro",
        "Piknik Selection",
        "Rio Cold Press",
        "S. Pellegrino",
        "Sodastream Classics",
        "Szent Gaál Twist",
        "Szovjetszkoje Igristoje",
        "Swiss",
        "Takamaka Dark Spiced",
        "Takamaka Koko",
        "Teeling Whiskey Small Batch",
        "The Deli",
        "Three Sixty Vodka",
        "Tiffán's",
        "Velkopopovický Kozel Premium Lager",
        "Veuve Pelletier Ponsardin",
        "Vitamizu Minions",
        "Vitamizu Mizu Mate Classic",
        "Vitamizu Mizu Mate Grapefruit-Lime",
        "Vitamizu Stumble Guys",
        "Yo",
        "YO Sirup",
        "Zuegg Intenso",
        "Zuegg Zero",
    }
)

FORBIDDEN_LEGACY_PROPERTIES = frozenset(
    {
        "energia tartalom",
        "energiamentes",
        "kiszerelés / rendszer",
        "borvidék / eredet",
        "szőlőfajta / borstílus",
        "hatóanyag / cél",
        "cukormentes / zero",
        "palack",
        "alkohol",
        "C-vitamin",
        "püré",
        "összetétel",
        "zöldség",
    }
)
PLACEHOLDER_ATOMS = frozenset({"egyeb", "nem jelolt"})
ALLOWED_PACKAGING = frozenset(
    {
        "palack",
        "doboz",
        "multipack",
        "tasak",
        "vákuumcsomagolás",
        "kapszula",
        "bag-in-box",
        "kávépárna",
        "hordó",
        "utántöltő tasak",
        "aromazáró csomagolás",
        "pohár",
        "adagcsomagolt",
    }
)
ALLOWED_PACKAGING_MATERIALS = frozenset({"üveg", "műanyag", "PET"})
EXPECTED_PROPERTY_COUNTS = {
    "eredet": 1787,
    "szőlőfajta": 1238,
    "borstílus": 657,
    "hatóanyag": 6,
    "funkció": 372,
    "cukormentes": 3821,
    "csomagolás anyaga": 2220,
    "alkoholalap": 87,
    "keverőanyag": 7,
    "kávéfajta": 11,
    "pürét tartalmaz": 7,
    "rostos": 3,
    "instant": 421,
    "termékcsalád": 176,
    "fehérjetartalom": 1,
    "energiastátusz": 910,
    "cukrozott": 585,
    "minőség": 7,
    "puttonyszám": 27,
    "csomagdarabszám": 630,
    "egységnyi kiszerelés": 609,
    "csomagegységek": 1,
}
EXPECTED_PRODUCT_FAMILY_COUNTS = {
    "Omnia": 75,
    "Nastro Azzurro": 29,
    "Paloma": 18,
    "Elixír": 13,
    "Tricollis": 10,
    "Hugo Spritz": 10,
    "Emese": 8,
    "Cold Press": 6,
    "Days": 3,
    "Rehab": 2,
    "Selection": 1,
    "Hot Chocolatta": 1,
}

EXPECTED_SIZE_RECORDS = 12531
EXPECTED_SIZE_MISSING = 279
EXPECTED_PACKAGING_RECORDS = 4879
EXPECTED_MULTIPACK_RECORDS = 611
EXPECTED_CHILD_ID_SHA256 = (
    "1d9532d473faffdd9a355946eda05eebdd00554d798c22a9309587c8cbfaf6d0"
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
PILSNER_FALSE_IPA_IDS = frozenset({"1028287", "680000:4217390"})
APA_IDS = frozenset(
    {
        "121225339",
        "53cf74709f0aed73960662e0",
        "673034:4210424",
        "678785:4216175",
        "BTY-X17303200320021",
        "dea8ebbdd70dbb5168b50674",
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
COLA_INGREDIENT_NOISE_IDS = frozenset(
    {
        "121328172",
        "36127:36130",
        "4598457",
        "507766:4045153",
        "535021",
        "765738:4303128",
    }
)
HAAS_FALSE_INSTANT_IDS = frozenset({"127538:3664736", "203228544"})
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


def reject_nonfinite_number(value: str) -> None:
    raise ValueError(f"Nem véges JSON-szám: {value}")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return json.load(
            handle,
            object_pairs_hook=reject_duplicate_keys,
            parse_constant=reject_nonfinite_number,
        )


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


def identifier_set_hash(rows: Iterable[dict[str, Any]]) -> str:
    """Stabil hash egy ellenőrzött termékcsoport azonosítóhalmazáról."""

    identifiers = sorted(product_id(product) for product in rows)
    return hashlib.sha256("\n".join(identifiers).encode("utf-8")).hexdigest()


def check_expected_identifier_group(
    failures: FailureCollector,
    failure_prefix: str,
    label: str,
    rows: list[dict[str, Any]],
    expected: tuple[int, str],
) -> None:
    expected_count, expected_hash = expected
    actual_hash = identifier_set_hash(rows)
    if len(rows) != expected_count or actual_hash != expected_hash:
        failures.add(
            failure_prefix,
            {
                "group": label,
                "expected_count": expected_count,
                "actual_count": len(rows),
                "expected_id_sha256": expected_hash,
                "actual_id_sha256": actual_hash,
            },
        )


def has_parseable_source_quantity(product: dict[str, Any]) -> bool:
    item = product.get("termek") or {}
    amount = str(item.get("vegso_mennyiseg") or "").strip()
    unit = fold(item.get("vegso_egyseg") or "")
    return bool(
        re.fullmatch(r"\d+(?:[.,]\d+)?", amount)
        and unit in {"g", "kg", "ml", "cl", "dl", "l"}
    )


def has_parseable_name_quantity(product: dict[str, Any]) -> bool:
    return NAME_QUANTITY_RE.search(product_name(product)) is not None


def quantity_in_base_unit(value: Any) -> tuple[str, float] | None:
    if not isinstance(value, str) or SIMPLE_QUANTITY_RE.fullmatch(value) is None:
        return None
    number_text, unit = value.split()
    number = float(number_text.replace(",", "."))
    factors = {
        "kg": ("mass", 1000.0),
        "g": ("mass", 1.0),
        "l": ("volume", 1000.0),
        "dl": ("volume", 100.0),
        "cl": ("volume", 10.0),
        "ml": ("volume", 1.0),
        "db": ("count", 1.0),
    }
    dimension, factor = factors[unit.casefold()]
    return dimension, number * factor


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
            if property_name != property_name.strip():
                failures.add(
                    "tree_untrimmed_property_name",
                    {"path": list(path), "group": group_name, "property": property_name},
                )
            if path[0] == ITAL and property_name in FORBIDDEN_LEGACY_PROPERTIES:
                failures.add(
                    "tree_forbidden_legacy_property",
                    {"path": list(path), "group": group_name, "property": property_name},
                )
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
                if isinstance(allowed_value, str):
                    if allowed_value != re.sub(r"\s+", " ", allowed_value).strip():
                        failures.add(
                            "tree_noncanonical_whitespace",
                            {
                                "path": list(path),
                                "property": property_name,
                                "value": allowed_value,
                            },
                        )
                    if path[0] == ITAL and fold(allowed_value) in PLACEHOLDER_ATOMS:
                        failures.add(
                            "tree_placeholder_allowed_value",
                            {
                                "path": list(path),
                                "property": property_name,
                                "value": allowed_value,
                            },
                        )
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
        if not isinstance(property_name, str) or not property_name.strip():
            failures.add(
                f"{scope}_invalid_product_property_name",
                {**context, "property": property_name},
            )
            continue
        if property_name != property_name.strip():
            failures.add(
                f"{scope}_untrimmed_product_property_name",
                {**context, "property": property_name},
            )
        if (
            product.get("fokategoria") == ITAL
            and property_name in FORBIDDEN_LEGACY_PROPERTIES
        ):
            failures.add(
                "forbidden_legacy_product_property",
                {**context, "property": property_name},
            )
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
            folded_atoms = [
                allowed_value_key(value)
                for value in raw_value
                if not isinstance(value, (dict, list))
            ]
            if len(folded_atoms) != len(set(folded_atoms)):
                failures.add(
                    f"{scope}_duplicate_product_property_value",
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
            if isinstance(value, str):
                if value != re.sub(r"\s+", " ", value).strip():
                    failures.add(
                        f"{scope}_noncanonical_whitespace",
                        {
                            **context,
                            "property": property_name,
                            "value": value,
                        },
                    )
                if (
                    product.get("fokategoria") == ITAL
                    and fold(value) in PLACEHOLDER_ATOMS
                ):
                    failures.add(
                        "placeholder_product_property_value",
                        {
                            **context,
                            "property": property_name,
                            "value": value,
                        },
                    )
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


def validate_local_tree_values_are_used(
    categories: dict[str, Any],
    ital_rows: list[tuple[int, dict[str, Any]]],
    failures: FailureCollector,
    declaration_cache: dict[tuple[str, ...], dict[str, Declaration]],
) -> int:
    """Minden helyi Ital-deklarációhoz leszármazotti termékbizonyítékot kér."""

    levels: list[tuple[tuple[str, ...], list[dict[str, Any]]]] = [
        ((ITAL,), [product for _index, product in ital_rows])
    ]
    for alkategoria, altipusok in EXPECTED_HIERARCHY.items():
        parent_products = [
            product
            for _index, product in ital_rows
            if product.get("alkategoria") == alkategoria
        ]
        levels.append(((ITAL, alkategoria), parent_products))
        for altipus in altipusok:
            leaf_products = [
                product
                for product in parent_products
                if product.get("altipus") == altipus
            ]
            levels.append(((ITAL, alkategoria, altipus), leaf_products))

    checked_values = 0
    for path, descendants in levels:
        node = get_node(categories, path)
        if node is None:
            continue
        declarations = parse_local_declarations(
            node,
            path,
            failures,
            declaration_cache,
        )
        for property_name, declaration in declarations.items():
            used_values = {
                allowed_value_key(atom)
                for product in descendants
                for atom in (
                    (product.get("tulajdonsagok") or {}).get(property_name)
                    if isinstance(
                        (product.get("tulajdonsagok") or {}).get(property_name),
                        list,
                    )
                    else [
                        (product.get("tulajdonsagok") or {}).get(property_name)
                    ]
                )
                if atom is not None
            }
            if declaration.shape == "flag":
                if not used_values:
                    failures.add(
                        "unused_tree_flag_declaration",
                        {"path": list(path), "property": property_name},
                    )
                continue
            for allowed_value in declaration.allowed_values or ():
                checked_values += 1
                if allowed_value_key(allowed_value) not in used_values:
                    failures.add(
                        "unused_tree_allowed_value",
                        {
                            "path": list(path),
                            "property": property_name,
                            "value": allowed_value,
                        },
                    )
    return checked_values


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


def validate_ital_dataset_semantics(
    ital_rows: list[tuple[int, dict[str, Any]]],
    by_id: dict[str, list[tuple[int, dict[str, Any]]]],
    failures: FailureCollector,
) -> dict[str, int]:
    """A termékenkénti deklarációparitáson túli, korpuszszintű invariánsok."""

    ital_products = [product for _index, product in ital_rows]
    property_counts: dict[str, int] = defaultdict(int)
    brand_rows: list[tuple[str, str]] = []
    brands_by_fold: dict[str, set[str]] = defaultdict(set)
    size_records = 0
    size_missing = 0
    packaging_records = 0
    multipack_records = 0
    instant_name_candidates = 0

    for index, product in ital_rows:
        context = product_context(index, product)
        properties = product.get("tulajdonsagok") or {}
        if not isinstance(properties, dict):
            continue
        for property_name in properties:
            property_counts[property_name] += 1

        brand = properties.get("márka")
        if brand is not None:
            if not isinstance(brand, str) or not brand.strip():
                failures.add(
                    "brand_not_nonempty_scalar",
                    {**context, "value": brand, "shape": value_shape(brand)},
                )
            else:
                brand_rows.append((product_id(product), brand))
                brands_by_fold[fold(brand)].add(brand)
                if brand in FORBIDDEN_BRAND_VALUES:
                    failures.add(
                        "forbidden_legacy_brand_value",
                        {**context, "value": brand},
                    )

        size = properties.get("kiszerelés")
        if size is None:
            size_missing += 1
            if has_parseable_source_quantity(product) or has_parseable_name_quantity(
                product
            ):
                failures.add(
                    "missing_parseable_size",
                    {
                        **context,
                        "source_amount": (product.get("termek") or {}).get(
                            "vegso_mennyiseg"
                        ),
                        "source_unit": (product.get("termek") or {}).get(
                            "vegso_egyseg"
                        ),
                    },
                )
        else:
            size_records += 1
            parsed_size = quantity_in_base_unit(size)
            if parsed_size is None or parsed_size[1] <= 0:
                failures.add(
                    "non_atomic_size",
                    {**context, "value": size, "shape": value_shape(size)},
                )

        package_count = properties.get("csomagdarabszám")
        if package_count is not None and (
            not isinstance(package_count, int)
            or isinstance(package_count, bool)
            or package_count <= 0
        ):
            failures.add(
                "invalid_package_count",
                {**context, "value": package_count},
            )

        unit_size = properties.get("egységnyi kiszerelés")
        if unit_size is not None and (
            not isinstance(unit_size, str)
            or SIMPLE_QUANTITY_RE.fullmatch(unit_size) is None
        ):
            failures.add(
                "invalid_unit_size",
                {**context, "value": unit_size},
            )

        package_units = properties.get("csomagegységek")
        if package_units is not None:
            if not isinstance(package_units, list) or not package_units:
                failures.add(
                    "invalid_package_units",
                    {**context, "value": package_units},
                )
            else:
                for package_unit in package_units:
                    if (
                        not isinstance(package_unit, str)
                        or SIMPLE_QUANTITY_RE.fullmatch(package_unit) is None
                    ):
                        failures.add(
                            "invalid_package_unit",
                            {**context, "value": package_unit},
                        )

        packaging = properties.get("csomagolás")
        packaging_atoms = packaging if isinstance(packaging, list) else []
        if packaging is not None:
            packaging_records += 1
            if not isinstance(packaging, list) or not packaging:
                failures.add(
                    "invalid_packaging_shape",
                    {**context, "value": packaging, "shape": value_shape(packaging)},
                )
            for atom in packaging_atoms:
                if (
                    not isinstance(atom, str)
                    or atom not in ALLOWED_PACKAGING
                    or any(char.isdigit() for char in atom)
                ):
                    failures.add(
                        "invalid_packaging_atom",
                        {**context, "value": atom},
                    )
                if isinstance(atom, str) and fold(atom) in {"filter", "szalas"}:
                    failures.add(
                        "product_form_in_packaging",
                        {**context, "value": atom},
                    )
            if "multipack" in packaging_atoms:
                multipack_records += 1
                if (
                    not isinstance(package_count, int)
                    or isinstance(package_count, bool)
                    or package_count <= 0
                ):
                    failures.add(
                        "multipack_missing_package_count",
                        {**context, "value": package_count},
                    )
            path = (product.get("alkategoria"), product.get("altipus"))
            if (
                product.get("alkategoria") == HOT_BRANCH
                or path == (BASE_BRANCH, "Italpor és tabletta")
            ) and "palack" in packaging_atoms:
                failures.add("dry_product_marked_as_bottle", context)

        materials = properties.get("csomagolás anyaga")
        if materials is not None:
            material_atoms = materials if isinstance(materials, list) else [materials]
            for atom in material_atoms:
                if atom not in ALLOWED_PACKAGING_MATERIALS:
                    failures.add(
                        "invalid_packaging_material",
                        {**context, "value": atom},
                    )
            if "palack" not in packaging_atoms:
                failures.add(
                    "packaging_material_without_bottle",
                    {**context, "materials": materials, "packaging": packaging},
                )

        parsed_total = quantity_in_base_unit(size)
        parsed_unit = quantity_in_base_unit(unit_size)
        if (
            parsed_total is not None
            and parsed_unit is not None
            and isinstance(package_count, int)
            and not isinstance(package_count, bool)
            and package_count > 0
        ):
            expected_dimension, expected_amount = parsed_unit
            actual_dimension, actual_amount = parsed_total
            if (
                actual_dimension != expected_dimension
                or abs(actual_amount - package_count * expected_amount) > 0.01
            ):
                failures.add(
                    "multipack_total_mismatch",
                    {
                        **context,
                        "count": package_count,
                        "unit_size": unit_size,
                        "total_size": size,
                    },
                )
        if isinstance(package_units, list) and package_units and parsed_total is not None:
            parsed_parts = [quantity_in_base_unit(value) for value in package_units]
            if all(part is not None for part in parsed_parts):
                dimensions = {part[0] for part in parsed_parts if part is not None}
                expected_amount = sum(
                    part[1] for part in parsed_parts if part is not None
                )
                if (
                    dimensions != {parsed_total[0]}
                    or abs(expected_amount - parsed_total[1]) > 0.01
                ):
                    failures.add(
                        "package_units_total_mismatch",
                        {
                            **context,
                            "parts": package_units,
                            "total_size": size,
                        },
                    )

        for true_only_property in (
            "pürét tartalmaz",
            "rostos",
            "instant",
            "cukrozott",
        ):
            if (
                true_only_property in properties
                and properties[true_only_property] is not True
            ):
                failures.add(
                    "non_true_presence_flag",
                    {
                        **context,
                        "property": true_only_property,
                        "value": properties[true_only_property],
                    },
                )

        form_atoms = properties.get("forma")
        for atom in form_atoms if isinstance(form_atoms, list) else [form_atoms]:
            if isinstance(atom, str) and fold(atom) in {"instant", "instant italpor"}:
                failures.add(
                    "instant_state_left_in_form",
                    {**context, "value": atom},
                )
        for generic_property in ("típus", "fajta"):
            raw_generic = properties.get(generic_property)
            generic_values = (
                raw_generic if isinstance(raw_generic, list) else [raw_generic]
            )
            if any(
                isinstance(atom, str) and fold(atom) == "instant"
                for atom in generic_values
            ):
                failures.add(
                    "instant_state_left_on_generic_axis",
                    {
                        **context,
                        "property": generic_property,
                        "value": raw_generic,
                    },
                )
        if re.search(
            r"\binstant\b|\bazonnal oldodo\b",
            fold(product_name(product)),
        ):
            instant_name_candidates += 1
            if properties.get("instant") is not True:
                failures.add("instant_name_without_flag", context)

        energy_status = properties.get("energiastátusz")
        if energy_status is not None and energy_status not in {
            "energiamentes",
            "energiaszegény",
            "csökkentett energiatartalmú",
        }:
            failures.add(
                "invalid_energy_status",
                {**context, "value": energy_status},
            )

        flavor = properties.get("íz")
        flavor_values = flavor if isinstance(flavor, list) else [flavor]
        forbidden_flavor_atoms = {
            "barista",
            "classic",
            "classico",
            "decaffeinato",
            "fusion",
            "gold",
            "immun cink",
            "inulin",
            "klasszikus",
            "kollagen",
            "premium",
            "strong",
            "szuretlen",
            "tradicionalis",
            "unfiltered",
            "yellow label",
            "zero",
            "zero cukor",
            "zero sugar",
        }
        for atom in flavor_values:
            if isinstance(atom, str) and fold(atom) in forbidden_flavor_atoms:
                failures.add(
                    "non_flavor_atom_in_flavor",
                    {**context, "value": atom},
                )

        beer_type = properties.get("sörtípus")
        beer_type_values = (
            beer_type if isinstance(beer_type, list) else [beer_type]
        )
        for atom in beer_type_values:
            if isinstance(atom, str) and fold(atom) in {
                "barna",
                "dark",
                "premium",
                "vilagos",
            }:
                failures.add(
                    "color_or_quality_in_beer_type",
                    {**context, "value": atom},
                )

        puttony = properties.get("puttonyszám")
        if puttony is not None:
            puttony_values = puttony if isinstance(puttony, list) else [puttony]
            if (
                not puttony_values
                or any(
                    not isinstance(atom, int)
                    or isinstance(atom, bool)
                    or atom not in {4, 5, 6}
                    for atom in puttony_values
                )
            ):
                failures.add(
                    "invalid_numeric_puttony_count",
                    {**context, "value": puttony},
                )

        if properties.get("zsírtartalom") in (["1", "8%"], ["3", "5%"]):
            failures.add(
                "split_decimal_fat_content",
                {**context, "value": properties.get("zsírtartalom")},
            )

        content_atoms = properties.get("tartalom")
        content_values = (
            content_atoms if isinstance(content_atoms, list) else [content_atoms]
        )
        forbidden_content = {
            "energia",
            "izotonias",
            "rehab",
            "alakreform",
            "koffeinmentes",
            "50 g protein",
            "hozzaadott vitaminok",
            "zold tea",
        }
        for atom in content_values:
            if isinstance(atom, str) and fold(atom) in forbidden_content:
                failures.add(
                    "non_content_atom_in_content",
                    {**context, "value": atom},
                )
        folded_content = {
            fold(atom) for atom in content_values if isinstance(atom, str)
        }
        if "vitamin" in folded_content and any(
            "vitamin" in atom and atom != "vitamin" for atom in folded_content
        ):
            failures.add(
                "generic_vitamin_with_specific_vitamin",
                {**context, "value": content_atoms},
            )

        base = properties.get("alap")
        base_values = base if isinstance(base, list) else [base]
        for atom in base_values:
            if isinstance(atom, str) and (
                fold(atom) in {"natur", "enyhen szensavas asvanyviz"}
                or (
                    fold(atom) == "kola"
                    and product_id(product) in WRONG_COLA_BASE_IDS
                )
            ):
                failures.add(
                    "invalid_base_atom",
                    {**context, "value": atom},
                )

        if product_id(product) in (
            TUTTIFRUTTI_INGREDIENT_NOISE_IDS | COLA_INGREDIENT_NOISE_IDS
        ):
            ingredients = properties.get("összetevő")
            ingredient_values = (
                ingredients if isinstance(ingredients, list) else [ingredients]
            )
            forbidden_ingredients = (
                {"tuttifrutti"}
                if product_id(product) in TUTTIFRUTTI_INGREDIENT_NOISE_IDS
                else {"kola"}
            )
            if any(
                isinstance(atom, str) and fold(atom) in forbidden_ingredients
                for atom in ingredient_values
            ):
                failures.add(
                    "brand_substring_left_as_ingredient",
                    {**context, "value": ingredients},
                )

        overlap_rules = {
            "típus": (
                "édesség",
                "borstílus",
                "forma",
                "terméktípus",
                "sörtípus",
                "teatípus",
                "bortípus",
                "kávékeverék típusa",
            ),
            "fajta": (
                "szín",
                "édesség",
                "forma",
                "szőlőfajta",
                "sörtípus",
                "terméktípus",
            ),
            "íz": (
                "sörtípus",
                "eredet",
                "szőlőfajta",
                "alkoholalap",
                "kávékeverék típusa",
            ),
            "változat": ("kávékeverék típusa",),
        }
        for source_property, target_properties in overlap_rules.items():
            source = properties.get(source_property)
            source_values = source if isinstance(source, list) else [source]
            source_folded = {
                fold(atom) for atom in source_values if isinstance(atom, str)
            }
            target_folded = {
                fold(atom)
                for target_property in target_properties
                for atom in (
                    properties.get(target_property)
                    if isinstance(properties.get(target_property), list)
                    else [properties.get(target_property)]
                )
                if isinstance(atom, str)
            }
            overlap = sorted(source_folded & target_folded)
            if overlap:
                failures.add(
                    "same_atom_on_generic_and_dedicated_axis",
                    {
                        **context,
                        "source_property": source_property,
                        "overlap": overlap,
                    },
                )

    for folded_brand, spellings in sorted(brands_by_fold.items()):
        if len(spellings) > 1:
            failures.add(
                "fold_equivalent_brand_spellings",
                {"folded": folded_brand, "values": sorted(spellings)},
            )
    if len(brands_by_fold) != EXPECTED_UNIQUE_BRANDS:
        failures.add(
            "unique_brand_count",
            {
                "expected": EXPECTED_UNIQUE_BRANDS,
                "actual": len(brands_by_fold),
            },
        )

    assignment_payload = "\n".join(
        sorted(f"{item_id}\t{brand}" for item_id, brand in brand_rows)
    )
    assignment_hash = hashlib.sha256(assignment_payload.encode("utf-8")).hexdigest()
    if (
        len(brand_rows) != EXPECTED_BRAND_RECORDS
        or assignment_hash != EXPECTED_BRAND_ASSIGNMENT_SHA256
    ):
        failures.add(
            "brand_assignment_parity",
            {
                "expected_records": EXPECTED_BRAND_RECORDS,
                "actual_records": len(brand_rows),
                "expected_sha256": EXPECTED_BRAND_ASSIGNMENT_SHA256,
                "actual_sha256": assignment_hash,
            },
        )

    for label, expected, actual in (
        ("size_records", EXPECTED_SIZE_RECORDS, size_records),
        ("size_missing", EXPECTED_SIZE_MISSING, size_missing),
        ("packaging_records", EXPECTED_PACKAGING_RECORDS, packaging_records),
        ("multipack_records", EXPECTED_MULTIPACK_RECORDS, multipack_records),
        ("instant_name_candidates", 339, instant_name_candidates),
    ):
        if actual != expected:
            failures.add(
                "dataset_count_parity",
                {"metric": label, "expected": expected, "actual": actual},
            )

    for brand, expectation in EXPECTED_MAIN_BRAND_GROUPS.items():
        brand_products = [
            product
            for product in ital_products
            if (product.get("tulajdonsagok") or {}).get("márka") == brand
        ]
        check_expected_identifier_group(
            failures,
            "main_brand_group_parity",
            brand,
            brand_products,
            expectation,
        )

    for property_name, expected_count in EXPECTED_PROPERTY_COUNTS.items():
        actual_count = property_counts.get(property_name, 0)
        if actual_count != expected_count:
            failures.add(
                "normalized_property_count",
                {
                    "property": property_name,
                    "expected": expected_count,
                    "actual": actual_count,
                },
            )

    product_family_counts = Counter(
        atom
        for product in ital_products
        for atom in (
            (product.get("tulajdonsagok") or {}).get("termékcsalád")
            if isinstance(
                (product.get("tulajdonsagok") or {}).get("termékcsalád"),
                list,
            )
            else [(product.get("tulajdonsagok") or {}).get("termékcsalád")]
        )
        if isinstance(atom, str)
    )
    if dict(product_family_counts) != EXPECTED_PRODUCT_FAMILY_COUNTS:
        failures.add(
            "product_family_distribution",
            {
                "expected": EXPECTED_PRODUCT_FAMILY_COUNTS,
                "actual": dict(product_family_counts),
            },
        )

    for leaf, expectation in EXPECTED_FRUIT_LEAF_GROUPS.items():
        rows = [
            product
            for product in ital_products
            if product.get("alkategoria") == FRUIT_BRANCH
            and product.get("altipus") == leaf
        ]
        check_expected_identifier_group(
            failures,
            "fruit_leaf_group_parity",
            leaf,
            rows,
            expectation,
        )

    juice_type_rows: dict[tuple[str, ...], list[dict[str, Any]]] = defaultdict(list)
    for product in ital_products:
        if (
            product.get("alkategoria") != FRUIT_BRANCH
            or product.get("altipus") != "Lé"
        ):
            continue
        raw_type = (product.get("tulajdonsagok") or {}).get("lé típusa")
        juice_type = tuple(raw_type) if isinstance(raw_type, list) else ()
        if juice_type not in EXPECTED_JUICE_TYPE_GROUPS:
            failures.add(
                "invalid_atomic_juice_type",
                {
                    "product_id": product_id(product),
                    "name": product_name(product),
                    "value": raw_type,
                },
            )
            continue
        juice_type_rows[juice_type].append(product)
    for juice_type, expectation in EXPECTED_JUICE_TYPE_GROUPS.items():
        check_expected_identifier_group(
            failures,
            "juice_type_group_parity",
            " + ".join(juice_type),
            juice_type_rows.get(juice_type, []),
            expectation,
        )

    nestea_rows = [
        product
        for product in ital_products
        if product.get("alkategoria") == SOFT_BRANCH
        and product.get("altipus") == "Jegestea"
        and (product.get("tulajdonsagok") or {}).get("márka") == "Nestea"
    ]
    if len(nestea_rows) != 60:
        failures.add(
            "nestea_iced_tea_count",
            {"expected": 60, "actual": len(nestea_rows)},
        )
    for product in nestea_rows:
        if (product.get("tulajdonsagok") or {}).get("szénsavasság") != "szénsavmentes":
            failures.add(
                "nestea_not_still",
                {
                    "product_id": product_id(product),
                    "name": product_name(product),
                    "value": (product.get("tulajdonsagok") or {}).get(
                        "szénsavasság"
                    ),
                },
            )

    def unique_ital_product(item_id: str, failure_key: str) -> dict[str, Any] | None:
        matches = [
            product
            for _index, product in by_id.get(item_id, [])
            if product.get("fokategoria") == ITAL
        ]
        if len(matches) != 1:
            failures.add(
                failure_key,
                {"product_id": item_id, "expected": 1, "actual": len(matches)},
            )
            return None
        return matches[0]

    for item_id in sorted(FORCED_STILL_IDS):
        product = unique_ital_product(item_id, "forced_still_record_count")
        if product is not None and (
            product.get("tulajdonsagok") or {}
        ).get("szénsavasság") != "szénsavmentes":
            failures.add(
                "forced_still_value",
                {
                    "product_id": item_id,
                    "value": (product.get("tulajdonsagok") or {}).get(
                        "szénsavasság"
                    ),
                },
            )

    exact_property_expectations: dict[str, dict[str, Any]] = {
        "2807722": {"gyümölcstartalom": ["50,6%"]},
        "BTY-X11998900320021": {"gyümölcstartalom": ["99,5%"]},
        "121357396": {"alkoholtartalom": ["12%"]},
        "789008:4326398": {"kiszerelés": "330 ml"},
        "692993:4230383": {"csomagdarabszám": 6},
        "752013:4289403": {
            "csomagdarabszám": 4,
            "egységnyi kiszerelés": "330 ml",
            "kiszerelés": "1320 ml",
        },
    }
    for item_id, expected_properties in exact_property_expectations.items():
        product = unique_ital_product(item_id, "exact_fix_record_count")
        if product is None:
            continue
        properties = product.get("tulajdonsagok") or {}
        for property_name, expected_value in expected_properties.items():
            if properties.get(property_name) != expected_value:
                failures.add(
                    "exact_semantic_fix",
                    {
                        "product_id": item_id,
                        "property": property_name,
                        "expected": expected_value,
                        "actual": properties.get(property_name),
                    },
                )
    for item_id in sorted(HAAS_FALSE_INSTANT_IDS):
        product = unique_ital_product(item_id, "haas_record_count")
        if product is not None and (
            product.get("tulajdonsagok") or {}
        ).get("instant") is not None:
            failures.add(
                "haas_false_instant",
                {
                    "product_id": item_id,
                    "actual": (product.get("tulajdonsagok") or {}).get(
                        "instant"
                    ),
                },
            )
    for item_id in (
        "121227556",
        "3258894b9df044556713e967",
        "678971:4216361",
        "680045:4217435",
        "9fe1fad92de106673703c895",
        "a51fcde4249c0f2564c25818",
    ):
        product = unique_ital_product(item_id, "half_percent_beer_record_count")
        if product is not None and (
            product.get("tulajdonsagok") or {}
        ).get("alkoholtartalom") != ["0,5%"]:
            failures.add(
                "half_percent_beer_alcohol",
                {
                    "product_id": item_id,
                    "actual": (product.get("tulajdonsagok") or {}).get(
                        "alkoholtartalom"
                    ),
                },
            )

    coffee_additive_types: dict[str, int] = defaultdict(int)
    for product in ital_products:
        if (
            product.get("alkategoria") != HOT_BRANCH
            or product.get("altipus") != "Kávé- és teaadalék"
        ):
            continue
        raw_types = (product.get("tulajdonsagok") or {}).get("terméktípus")
        for atom in raw_types if isinstance(raw_types, list) else [raw_types]:
            if isinstance(atom, str):
                coffee_additive_types[atom] += 1
    expected_coffee_additive_types = {
        "kávékrémpor": 17,
        "tejpor": 4,
        "kávéfehérítő": 2,
        "kávétejszín": 1,
    }
    if dict(coffee_additive_types) != expected_coffee_additive_types:
        failures.add(
            "coffee_additive_type_distribution",
            {
                "expected": expected_coffee_additive_types,
                "actual": dict(coffee_additive_types),
            },
        )

    child_candidates = [
        product
        for product in ital_products
        if CHILD_NAME_RE.search(fold(product_name(product)))
    ]
    if len(child_candidates) != 43:
        failures.add(
            "child_name_candidate_count",
            {"expected": 43, "actual": len(child_candidates)},
        )
    child_hash = identifier_set_hash(child_candidates)
    if child_hash != EXPECTED_CHILD_ID_SHA256:
        failures.add(
            "child_name_candidate_id_parity",
            {
                "expected_sha256": EXPECTED_CHILD_ID_SHA256,
                "actual_sha256": child_hash,
            },
        )
    for product in child_candidates:
        audience = (product.get("tulajdonsagok") or {}).get("célcsoport")
        audience_atoms = audience if isinstance(audience, list) else [audience]
        if "gyerek" not in audience_atoms:
            failures.add(
                "child_audience_missing",
                {
                    "product_id": product_id(product),
                    "name": product_name(product),
                    "value": audience,
                },
            )

    def beer_types(item_id: str) -> tuple[dict[str, Any] | None, set[str]]:
        product = unique_ital_product(item_id, "beer_record_count")
        if product is None:
            return None, set()
        raw = (product.get("tulajdonsagok") or {}).get("sörtípus")
        atoms = raw if isinstance(raw, list) else [raw]
        return product, {fold(value) for value in atoms if isinstance(value, str)}

    for item_id in sorted(PILSNER_FALSE_IPA_IDS):
        _product, types = beer_types(item_id)
        if "ipa" in types:
            failures.add(
                "pilsner_false_ipa",
                {"product_id": item_id, "types": sorted(types)},
            )

    beer_expectations = {
        "678794:4216184": ({"pils"}, {"ale"}),
        "780917:4318307": ({"lager"}, {"felsoerjesztesu sor"}),
        "789926:4327316": (
            {"lager", "india pale lager"},
            {"felsoerjesztesu sor"},
        ),
        "BTY-X17887400320021": ({"ale", "buzasor"}, set()),
    }
    for item_id, (required, forbidden) in beer_expectations.items():
        _product, types = beer_types(item_id)
        if not required.issubset(types) or types.intersection(forbidden):
            failures.add(
                "beer_type_semantics",
                {
                    "product_id": item_id,
                    "required": sorted(required),
                    "forbidden": sorted(forbidden),
                    "actual": sorted(types),
                },
            )
    for item_id in sorted(APA_IDS):
        _product, types = beer_types(item_id)
        if "apa" not in types:
            failures.add(
                "apa_type_missing",
                {"product_id": item_id, "types": sorted(types)},
            )
    for product in ital_products:
        if product.get("altipus") != "Sör, radler és malátaital":
            continue
        raw = (product.get("tulajdonsagok") or {}).get("sörtípus")
        for atom in raw if isinstance(raw, list) else [raw]:
            if isinstance(atom, str) and (
                (fold(atom) == "ipa" and atom != "IPA")
                or (fold(atom) == "apa" and atom != "APA")
            ):
                failures.add(
                    "beer_abbreviation_not_canonical",
                    {
                        "product_id": product_id(product),
                        "value": atom,
                    },
                )

    royal_crown = unique_ital_product(
        "BTY-X17833000320021",
        "royal_crown_record_count",
    )
    if royal_crown is not None and (
        royal_crown.get("tulajdonsagok") or {}
    ).get("cukormentes") is not True:
        failures.add(
            "royal_crown_sugarfree",
            {
                "product_id": "BTY-X17833000320021",
                "value": (royal_crown.get("tulajdonsagok") or {}).get(
                    "cukormentes"
                ),
            },
        )

    return {
        "size_records": size_records,
        "size_missing_unparseable": size_missing,
        "packaging_records": packaging_records,
        "multipack_records": multipack_records,
        "brand_records": len(brand_rows),
        "unique_brands": len(brands_by_fold),
        "instant_name_candidates": instant_name_candidates,
        "child_name_candidates": len(child_candidates),
        "nestea_iced_teas": len(nestea_rows),
    }


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
            expected_nesquik_properties = {
                "márka": "Nesquik",
                "terméktípus": ["szirup"],
                "íz": ["kakaó"],
            }
            if product.get("tulajdonsagok") != expected_nesquik_properties:
                failures.add(
                    "nesquik_exact_properties",
                    {
                        **product_context(index, product),
                        "expected": expected_nesquik_properties,
                        "actual": product.get("tulajdonsagok"),
                    },
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
            if item_id == FRUIT_STEP_GINGER_ID:
                properties = product.get("tulajdonsagok") or {}
                expected_values = {
                    "terméktípus": ["citrusízesítő"],
                    "kiszerelés": "tasak",
                    "gyümölcs": ["citrom"],
                }
                for property_name, expected_value in expected_values.items():
                    if properties.get(property_name) != expected_value:
                        failures.add(
                            "fruit_step_wrong_property",
                            {
                                **product_context(index, product),
                                "property": property_name,
                                "actual": properties.get(property_name),
                                "expected": expected_value,
                            },
                        )
                ingredients = properties.get("összetevő")
                ingredient_atoms = (
                    ingredients if isinstance(ingredients, list) else [ingredients]
                )
                if "gyömbér" not in ingredient_atoms:
                    failures.add(
                        "fruit_step_missing_ginger",
                        {
                            **product_context(index, product),
                            "actual": ingredients,
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
    path_counts = Counter(
        (
            str(product.get("alkategoria") or ""),
            str(product.get("altipus") or ""),
        )
        for _index, product in ital_rows
    )
    for path, expected_count in EXPECTED_PATH_COUNTS.items():
        actual_count = path_counts.get(path, 0)
        if actual_count != expected_count:
            failures.add(
                "ital_path_product_count",
                {
                    "path": list(path),
                    "expected": expected_count,
                    "actual": actual_count,
                },
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

    checked_local_tree_values = validate_local_tree_values_are_used(
        category_tree,
        ital_rows,
        failures,
        declaration_cache,
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

    dataset_summary = validate_ital_dataset_semantics(
        ital_rows,
        by_id,
        failures,
    )
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
            "checked_local_tree_values": checked_local_tree_values,
            "empty_ital_altipus_products": empty_altipus_count,
            "alcohol_branch_products": alcohol_products,
            "water_branch_products": water_products,
            "cola_and_tonic_products": cola_tonic_products,
            **dataset_summary,
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
