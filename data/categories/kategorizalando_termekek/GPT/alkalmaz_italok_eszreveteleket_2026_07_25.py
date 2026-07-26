# -*- coding: utf-8 -*-
"""Az ``italok_észrevételek.txt`` szerinti, megismételhető Ital-migráció.

Alapértelmezésben csak memóriában dolgozik. A ``--apply`` kapcsoló kizárólag
akkor cseréli le a két fő JSON-fájlt, ha a külön ellenőrző a jelölt fájlokat
hibátlannak találta. Az alkoholos ág termékei és fanódja változatlan marad.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

# A nagy, ékezetes állomány C-encoderes kiírása ezen a gépen korábban
# instabil volt. A tiszta Python encoder lassabb, de determinisztikus.
json.encoder.c_make_encoder = None
json.decoder.scanstring = json.decoder.py_scanstring
json.scanner.make_scanner = json.scanner.py_make_scanner

BASE = Path(__file__).resolve().parent
RESULT_PATH = BASE / "eredmeny.json"
CATEGORY_PATH = BASE / "kategoriak_2026-06-13.json"
CHECKER_PATH = BASE / "ellenoriz_italok_eszreveteleket_2026_07_25.py"
AUDIT_PATH = BASE / "italok_eszrevetelek_audit_2026-07-25.json"
CANDIDATE_PRODUCTS_PATH = BASE / ".eredmeny.italok-20260725.candidate.json"
CANDIDATE_CATEGORIES_PATH = BASE / ".kategoriak.italok-20260725.candidate.json"

ITAL = "Ital"
PROP_KEY = "tulajdonságok"
ALK_KEY = "alkategóriák"
ALT_KEY = "altípusok"
EXPECTED_TOTAL = 47030

OLD_WATER = "Víz és vízalapú italok"
WATER = "Ásványvíz"
ALCOHOL = "Alkoholos italok és alkoholmentes alternatívák"
SOFT = "Üdítőitalok"
FRUIT = "Gyümölcs- és zöldségitalok"
OLD_FUNCTIONAL = "Funkcionális és teljesítményitalok"
FUNCTIONAL = "Funkcionális italok"
OLD_PLANT = "Növényi italok"
OLD_HOT = "Kávé-, tea- és kakaótermékek"
HOT = "Kávé-, tea- és forrócsokoládé-termékek"
OLD_BASE = "Italkészítési alapok"
BASES = "Italalapok"

BABY_WATER_PATH = ("Baba", "Bébiital, víz", "Bébivíz")
PLANT_PATH = ("Tejtermékek és tojás", "Növényi alternatíva", "Növényi ital")
COCOA_PATH = (
    "Alapanyag, sütés-főzés",
    "Sütési alapanyag",
    "Kakaópor és kakaós italpor",
)
COCOA_OLD_LEAF = "Kakaópor"
COCOA_MIXED_LEAF = "Kakaópor, csokicsepp, tortabevonó"
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
        # A korábbi exact lista hét, forrásmezővel/képpel igazolt shotot
        # kihagyott. A felhasználói szabály szerint ezek is itt maradnak.
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
YIPPY_COLA_IDS = frozenset({"121252986", "121252975"})
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
LEMONADE_TEA_IDS = frozenset(
    {"684101:4221491", "684104:4221494", "675134:4212524"}
)

COCOA_PURE_OVERRIDE_IDS = frozenset(
    {"1020872", "638030:4175420", "550386", "550385"}
)
COCOA_MIXED_SOURCE_IDS = frozenset(
    {"2754415", "2754314", "105041965", "220339855"}
)
COCOA_FRAPPE_ID = "70f8217f1c3b2c6ac11133f4"
COCOA_SWEETENER_IDS = frozenset({"36373:36376", "209732687"})
COCOA_KNOWN_PERCENT = {"BTY-X16203300320021": "16%"}
HOT_CHOCOLATE_TYPE_BY_ID = {
    "51513:51855": "ét",
    "1714e29f26da732910f8a20f": "ét",
    "220339680": "ét",
    "127517:3664715": "fehér",
}
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

COFFEE_PAD_IDS = frozenset(
    {
        "399920:3937247",
        "399926:3937253",
        "550023:4087413",
        "32404:32407",
        "768867:4306257",
        "BTY-X15951800320021",
        "c4867f36aa4d5afcd94901c0",
    }
)
COFFEE_CAPSULE_IDS = frozenset(
    {
        "942488:4479878",
        "942509:4479899",
        "766908:4304298",
        "942494:4479884",
        "875360:4412750",
        "829358:4366748",
        "798236:4335626",
        "100579761",
        "100579760",
    }
)
COFFEE_INTENSITY = {
    "500765:4038161": 8,
    "500768:4038164": 10,
    "500774:4038170": 8,
    "500771:4038167": 6,
    "500780:4038176": 11,
    "500792:4038188": 8,
    "512984:4050374": 7,
    "500786:4038182": 7,
    "536730:4074120": 9,
    "536733:4074123": 3,
    "399926:3937253": 5,
    "399950:3937277": 4,
    "399953:3937280": 6,
    "399932:3937259": 8,
    "547647:4085037": 5,
}
COFFEE_NATURAL_DECAF_IDS = frozenset(
    {
        "689726:4227116",
        "507775:4045162",
        "51789:52131",
        "11746:11749",
        "5d6d8112007e26612f20e16a",
        "210214547",
        "671228:4208618",
        "2752408",
        "9408196442eaaea6c024b524",
    }
)

TEA_LOOSE_OVERRIDE_IDS = frozenset(
    {
        "f1cb8319ce58a43f13b3a771",
        "35387bbc739170a6c8b56b8b",
        "3956ec638ab3f5998e5b737b",
        "b03ea02b2ea204f0678d4080",
        "d84f478bccb150c92963dc4f",
        "220314020",
        "220336058",
        "220314021",
        "220336057",
        "220314022",
        "152525:3689765",
        "40918:40921",
        "73057:3610145",
        "54588:54927",
        "209730492",
    }
)
TEA_POWDER_OVERRIDE_IDS = frozenset({"989129", "989130", "989131", "220320804"})

TABLET_IDS = frozenset(
    {
        "d9772d1f89be796fb34ec9d0",
        "3435092401126e1473cb7b3c",
        "e5b810005409b5c600008e20",
        "763c43451b13eb805b5de259",
        "aa8717e4a5f51bf5371c10de",
        "127538:3664736",
        "203228544",
        "105027674",
        "111274365",
        "111274368",
    }
)
BASE_POWDER_FROM_LIQUID_IDS = frozenset({"2799425", "2799424", "2799423", "2799422"})
HAAS_VITAMIN_IDS = frozenset({"127538:3664736", "203228544"})
FALSE_CARROT_FLAVOR_IDS = frozenset(
    {
        "674447:4211837",
        "674444:4211834",
        "BTY-X17445600320021",
        "BTY-X17445700320021",
        "121253415",
        "121253933",
    }
)
BASE_FLAVORS_BY_ID: dict[str, tuple[str, ...]] = {
    # A helyi termékképeken közvetlenül látható gyümölcsök/variánsok.
    "1059558": ("ananász", "alma", "narancs", "maracuja"),
    "670551:4207941": ("szőlő",),
    "BTY-X1348800320021": ("citrom", "lime"),
    "4596140": ("citrom", "őszibarack", "erdei gyümölcs"),
    # A Snack&Shake csomagolások zabbal készült, vitaminnal dúsított
    # italport mutatnak. A három komponens külön atom marad.
    "340b600da09ead538e6691cc": ("csokoládé", "zab", "vitamin"),
    "111276034": ("csokoládé", "zab", "vitamin"),
    "b16b51ddb1fd33c6dc930820": ("vanília", "zab", "vitamin"),
    "111276035": ("vanília", "zab", "vitamin"),
    "70bea15b6e26ebe2e729e339": ("málna", "zab", "vitamin"),
    "111276036": ("málna", "zab", "vitamin"),
}
BASE_ENERGY_BY_ID = {
    "70bea15b6e26ebe2e729e339": "édesítőszeres",
    "111276036": "édesítőszeres",
}

BRAND_BY_ID = {
    "121266135": "Floewater",
    "121266152": "Floewater",
    "121312000": "Füredi",
    "121312017": "Füredi",
    "970480": "Nestlé Aquarel",
    "820625:4358015": "Aqua Minera",
    "821276:4358666": "Aqua Minera",
    "679112:4216502": "Aqua Minera",
    "BTY-X17305200320021": "Aqua Minera",
    "BTY-X17305200320022": "Aqua Minera",
    "ec8e2d7a45292dc0e511481a": "CBA Minera",
    "ed294413f3a82fc28b9a8197": "CBA Minera",
    "875dbbb95244f97305b4d317": "CBA Minera",
    "8608:8611": "Davidoff",
    "220335763": "Davidoff",
    "209701478": "Davidoff",
    "209701461": "Davidoff",
    "2787444": "Bon Aroma",
    "151345:3688591": "Nesquik",
    "BTY-X17636600320022": "RIOBA",
    "BTY-X17645300320022": "RIOBA",
    "BTY-X17636700320022": "RIOBA",
    "BTY-X17601600320021": "Herbária",
    "BTY-X1875900320021": "Herbária",
    "BTY-X1876300320021": "Herbária",
    "BTY-X9432700320021": "Eduscho",
    "3375563": "New Gen",
    "3372161": "New Gen",
    "BTY-X18284100320021": "New Gen",
    "BTY-X18283900320021": "New Gen",
    "BTY-X18284300320021": "New Gen",
    "BTY-X18824000320021": "New Gen",
    "BTY-X18947900320021": "New Gen",
    "769656:4307046": "Celebration Party",
    "992580": "Aldi",
    "992582": "Aldi",
    "4602869": "Aldi",
    "1059531": "Aldi",
    "533978": "Aldi",
    "748850": "Aldi",
    "997182": "Aldi",
    "997183": "Aldi",
    "997184": "Aldi",
    "6407588": "Lidl",
    "6407589": "Lidl",
    "6407591": "Lidl",
    "6409645": "Lidl",
    "6412334": "Lidl",
    "6412603": "Lidl",
    "6407590": "Solevita",
    "935735": "Aldi",
    "935736": "Aldi",
    "935737": "Aldi",
    "6410784": "Solevita",
    "984933": "Penny",
    "2808492": "Coop Cívis",
    "2808491": "Coop Cívis",
    "BTY-X2905900320021": "Cívis",
    "BTY-X17520500320021": "Cívis",
    "3375493": "Coop Cívis",
    "2809133": "Coop Cívis",
    "2807526": "Coop Cívis",
    "2807087": "Coop Cívis",
    "148552:3685798": "Milky Sip",
    "438439:3975826": "Milky Sip",
    "148549:3685795": "Milky Sip",
    # CSV-, terméknév- és képalapú, rekordazonosítóra kötött főmárkák.
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
BRAND_ALIASES = {
    "floewater still": "Floewater",
    "floewater sparkling": "Floewater",
    "furedi ion": "Füredi",
    "furedi oxion": "Füredi",
    "omnia": "Douwe Egberts",
    "nestle ricore": "Ricoré",
    "herz new york coffee": "Herz Coffee",
    "vergnano": "Caffè Vergnano",
    "bravo": "Rauch",
    "yippy": "Rauch",
    "friss": "Borsodi",
    "estrella free damm": "Free Damm",
    "dolce gusto": "Nescafé",
    "good teahaz": "Gárdonyi Teaház",
    "okf farmer s": "OKF",
    "viwa vitaminwater": "Viwa",
    "absolute lifestyle": "Absolute",
    "absolute live": "Absolute",
    "prime hydration": "Prime",
    "nutriversum flow": "Nutriversum",
    "optisana sports": "Optisana",
    "the gutsy captain kombucha": "The Gutsy Captain",
    "chernel fizz water": "Chernel",
    "omg bubble tea": "OMG",
    "bello minions party drink": "Bello!",
    "ice gold zero ice tea": "Ice Gold",
    "the sparkling t alba": "The Sparkling T",
    "zen matcha": "ZEN",
    "vifon vietnamese lady": "Vifon",
    "canderel cankao": "Canderel",
    "lotte milkis": "Milkis",
    "dreamworks madagascar party drink": "DreamWorks Madagascar",
    "jurassic world party drink": "Jurassic World",
    "yogitea": "Yogi Tea",
    "caffe cagliari": "Caffè Cagliari",
    "caffe diemme": "Caffè Diemme",
    "sodastream": "SodaStream",
    "sodastream pepsi": "Pepsi",
    "sodastream mirinda": "Mirinda",
    "sodastream 7up": "7Up",
}

FLAVOR_ALIASES = {
    "marakuja": "maracuja",
    "maracuya": "maracuja",
    "passion fruit": "maracuja",
    "passionfruit": "maracuja",
    "szamoca": "eper",
    "foldieper": "eper",
    "strawberry": "eper",
    "forest fruit": "erdei gyümölcs",
    "erdei vegyes gyumolcs": "erdei gyümölcs",
    "erdei vegyesgyumolcs": "erdei gyümölcs",
    "erdeigyumolcs darabok": "erdei gyümölcs",
    "mixed berries": "erdei gyümölcs",
    "vegyes bogyos": "erdei gyümölcs",
    "lemon": "citrom",
    "raspberry": "málna",
    "cherry": "cseresznye",
    "black cherry": "cseresznye",
    "papaya": "papaja",
    "repa": "sárgarépa",
    "dragon fruit": "sárkánygyümölcs",
    "red grape": "szőlő",
    "bad apple": "alma",
    "strong apple": "alma",
    "valentino rossi citrus": "citrus",
    "viking berry": "erdei gyümölcs",
    "aranciata": "narancs",
    "bitter lemon": "citrom",
    "jaffa": "narancs",
    "tropical": "trópusi",
    "tropical fruit": "trópusi",
    "tropusi gyumolcs": "trópusi",
    "alpesi gyogynoveny": "gyógynövény",
    "kiwi": "kivi",
    "grenadine": "grenadin",
    "bergamot": "bergamott",
    "kamillavirag": "kamilla",
    "csalanlevel": "csalán",
    "echinacea": "kasvirág",
    "hars": "hársfavirág",
    "harsfa": "hársfavirág",
    "harsfavirag": "hársfavirág",
    "harsfaviragzat": "hársfavirág",
    "vegyesgyumolcs": "vegyes gyümölcs",
    "fekete ribizli": "feketeribizli",
    "bogyos gyumolcs": "erdei gyümölcs",
    "piros bogyos": "erdei gyümölcs",
    "acai bogyo": "acai",
    "b5": "B5-vitamin",
    "c vitamin": "C-vitamin",
    "b vitamin komplex": "B-vitamin-komplex",
    "nadcukor": "nádcukor",
    "cukornad": "nádcukor",
    "citrus mix": "citrus",
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


def clone_json_value(value: Any) -> Any:
    """Memoizálás nélkül másolja a JSON-ban megengedett értékeket."""

    if isinstance(value, dict):
        return {key: clone_json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [clone_json_value(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"Nem JSON-érték másolása: {type(value).__name__}")


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_name(f".{path.name}.writing")
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            digest = hashlib.sha256()
            encoder = json.JSONEncoder(ensure_ascii=False, indent=2)
            with partial.open("wb", buffering=0) as handle:
                buffer = bytearray()
                for piece in encoder.iterencode(payload):
                    buffer.extend(piece.encode("utf-8"))
                    if len(buffer) < 1024 * 1024:
                        continue
                    chunk = bytes(buffer)
                    written = handle.write(chunk)
                    if written != len(chunk):
                        raise OSError(f"Rövid fájlírás: {written}/{len(chunk)} bájt")
                    digest.update(chunk)
                    buffer.clear()
                buffer.extend(b"\n")
                if buffer:
                    chunk = bytes(buffer)
                    written = handle.write(chunk)
                    if written != len(chunk):
                        raise OSError(f"Rövid fájlírás: {written}/{len(chunk)} bájt")
                    digest.update(chunk)
                handle.flush()
                os.fsync(handle.fileno())
            expected_hash = digest.hexdigest()
            actual_hash = file_sha256(partial)
            if actual_hash != expected_hash:
                raise OSError(
                    f"Írás utáni SHA-256 eltérés ({attempt}/3): "
                    f"{actual_hash} != {expected_hash}"
                )
            os.replace(partial, path)
            if file_sha256(path) != expected_hash:
                raise OSError("Az atomikus átnevezés után megváltozott a fájl")
            return
        except (OSError, UnicodeError) as exc:
            last_error = exc
    raise RuntimeError(f"A JSON három ellenőrzött írásból sem lett ép: {path}") from last_error


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb", buffering=0) as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


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


def verified_copy(source: Path, target: Path) -> None:
    expected = file_sha256(source)
    last_actual = ""
    for _ in range(3):
        shutil.copy2(source, target)
        last_actual = file_sha256(target)
        if last_actual == expected:
            return
    raise RuntimeError(
        f"Három másolásból sem egyezik az SHA-256: {source} -> {target}; "
        f"{expected} != {last_actual}"
    )


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


def product_id(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("store_product_id") or "")


def product_name(product: dict[str, Any]) -> str:
    return str((product.get("termek") or {}).get("product_name") or "")


def product_text(product: dict[str, Any], props: dict[str, Any] | None = None) -> str:
    termek = product.get("termek") or {}
    return fold_text(
        " ".join(
            [
                str(termek.get("product_name") or ""),
                str(termek.get("brand_name") or ""),
                str(termek.get("categories") or ""),
                json.dumps(
                    product.get("tulajdonsagok") if props is None else props,
                    ensure_ascii=False,
                ),
            ]
        )
    )


def product_label_text(product: dict[str, Any]) -> str:
    """Csak a forrás termékmezők szövege, tulajdonságkulcsok nélkül."""

    termek = product.get("termek") or {}
    return fold_text(
        " ".join(
            [
                str(termek.get("product_name") or ""),
                str(termek.get("brand_name") or ""),
                str(termek.get("categories") or ""),
            ]
        )
    )


def path_of(product: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(product.get("fokategoria") or ""),
        str(product.get("alkategoria") or ""),
        str(product.get("altipus") or ""),
    )


def set_path(product: dict[str, Any], path: tuple[str, str, str]) -> None:
    product["fokategoria"], product["alkategoria"], product["altipus"] = path


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


def first_value(value: Any) -> Any:
    vals = values_of(value)
    return vals[0] if vals else None


def bool_value(value: Any) -> bool:
    return any(item is True or fold_text(item) in {"true", "igen", "1"} for item in values_of(value))


def canonical_brand(product: dict[str, Any], props: dict[str, Any]) -> str:
    item_id = product_id(product)
    if item_id in BRAND_BY_ID:
        return BRAND_BY_ID[item_id]
    raw = first_value(props.get("márka"))
    if not raw:
        raw = (product.get("termek") or {}).get("brand_name") or ""
    text = str(raw).strip()
    return BRAND_ALIASES.get(fold_text(text), text)


def canonical_flavor(raw: Any) -> str | None:
    text = str(raw).strip()
    folded = fold_text(text)
    if not folded:
        return None
    if folded in {"mix", "vegyes"}:
        return "vegyes"
    return FLAVOR_ALIASES.get(folded, text.casefold())


PROTECTED_FLAVORS = frozenset(
    {
        "erdei gyumolcs",
        "egzotikus gyumolcs",
        "piros gyumolcs",
        "sarkanygyumolcs",
        "zold alma",
        "fekete ribizli",
        "barna cukor",
        "c vitamin",
        "b vitamin komplex",
    }
)

NON_ATOMIC_FLAVOR_VALUES = frozenset(
    {
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
        "tropusi",
        "multifruit",
        "dr pepper",
    }
)


def drop_redundant_flavors(values: Iterable[str]) -> list[str]:
    result = dedupe(values)
    markers = {fold_text(value) for value in result}
    if "barack" in markers and markers & {"oszibarack", "sargabarack"}:
        result = [value for value in result if fold_text(value) != "barack"]
    markers = {fold_text(value) for value in result}
    if "tea" in markers and any(
        marker.endswith(" tea") and marker != "tea" for marker in markers
    ):
        result = [value for value in result if fold_text(value) != "tea"]
    return dedupe(result)


def flavor_atoms(values: Iterable[Any], *, remove: frozenset[str] = frozenset()) -> list[str]:
    atoms: list[str] = []
    for raw in values:
        if raw is None or raw == "":
            continue
        raw_text = str(raw).strip()
        folded_whole = fold_text(raw_text)
        canonical_whole = canonical_flavor(raw_text)
        if folded_whole in PROTECTED_FLAVORS or folded_whole in FLAVOR_ALIASES:
            parts = [canonical_whole]
        else:
            parts_raw = re.split(r"\s*(?:/|\+|&|;|,|\s+-\s+|\s+és\s+)\s*", raw_text)
            if len(parts_raw) == 1 and "-" in raw_text and not re.search(r"\d-\d", raw_text):
                parts_raw = re.split(r"\s*-\s*", raw_text)
            parts = [canonical_flavor(part) for part in parts_raw]
        for atom in parts:
            if not atom:
                continue
            marker = fold_text(atom)
            if marker in remove or marker in NON_ATOMIC_FLAVOR_VALUES:
                continue
            atoms.append(atom)
    return drop_redundant_flavors(atoms)


def physical_properties(props: dict[str, Any]) -> dict[str, Any]:
    kept: dict[str, Any] = {}
    for name in (
        "kiszerelés",
        "DRS",
        "csomagdarabszám",
        "egységnyi kiszerelés",
        "csomagolás",
    ):
        if name in props:
            kept[name] = clone_json_value(props[name])
    return kept


def carbonation_value(product: dict[str, Any], props: dict[str, Any]) -> str:
    if isinstance(props.get("szénsavas"), bool):
        return "szénsavas" if props["szénsavas"] else "szénsavmentes"
    values = [fold_text(value) for value in values_of(props.get("szénsavasság"))]
    if "extra szensavas" in values:
        return "extra szénsavas"
    if "enyhen szensavas" in values:
        return "enyhén szénsavas"
    if "szensavas" in values:
        return "szénsavas"
    if "szensavmentes" in values:
        return "szénsavmentes"
    text = product_label_text(product)
    if "szensavmentes" in text:
        return "szénsavmentes"
    if "enyhen szensavas" in text or "szendioxiddal enyhen" in text:
        return "enyhén szénsavas"
    if "szensavas" in text or "pezsgo" in text or "party drink" in text:
        return "szénsavas"
    return "szénsavmentes"


def carbonated_bool(product: dict[str, Any], props: dict[str, Any], leaf: str) -> bool:
    value = carbonation_value(product, props)
    if value != "szénsavmentes":
        return True
    if leaf in {"Kóla", "Tonik", "Kölyökpezsgő"}:
        return True
    return False


def energy_state(product: dict[str, Any], props: dict[str, Any], *, syrup: bool = False) -> str:
    existing = first_value(props.get("energiatartalom"))
    allowed = (
        {"édesítőszeres", "csökkentett", "normál"}
        if syrup
        else {"cukormentes", "energiacsökkentett", "normál"}
    )
    if existing in allowed:
        return str(existing)
    text = product_label_text(product)
    raw_status = " ".join(fold_text(value) for value in values_of(props.get("energiastátusz")))
    sugar_free = bool_value(props.get("cukormentes"))
    sweetener = bool_value(props.get("édesítőszerrel"))
    if (
        sugar_free
        or "cukormentes" in text
        or "zero sugar" in text
        or re.search(r"\bzero\b|\bzero\b", text)
        or "energiamentes" in raw_status
    ):
        return "édesítőszeres" if syrup else "cukormentes"
    if (
        "csokkentett" in raw_status
        or "energiaszegeny" in raw_status
        or "csokkentett energiatartalmu" in text
        or (" light " in f" {text} " and "delight" not in text)
    ):
        return "csökkentett" if syrup else "energiacsökkentett"
    if syrup and sweetener:
        return "édesítőszeres"
    return "normál"


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
            raise RuntimeError(f"Kevert tulajdonságalak: {name!r}: {shapes}")
        shape = next(iter(shapes))
        allowed = sorted(dedupe(values[name]), key=lambda value: fold_text(value))
        if shape == "flag":
            block["egyedi"][name] = {}
        elif shape == "single":
            block["egyedi"][name] = allowed
        else:
            block["csoportos"][name] = allowed
    return block


def normalize_water(product: dict[str, Any], old_props: dict[str, Any], *, flavored: bool) -> None:
    props = physical_properties(old_props)
    props["márka"] = canonical_brand(product, old_props)
    props["szénsavasság"] = carbonation_value(product, old_props)
    if flavored:
        raw_flavors = [
            *values_of(old_props.get("íz")),
            *values_of(old_props.get("összetevő")),
        ]
        flavors = flavor_atoms(
            raw_flavors,
            remove=frozenset(
                {
                    "vitamin",
                    "oxigen",
                    "multivitamin",
                    "revitalizalo",
                    "antistressz",
                    "limonade",
                    "tea",
                }
            ),
        )
        # Két Lemon Lime rekordban a generikus angol lemon a konkrét citrom
        # és lime mellett szerepelt; a canonicalizálás eleve összevonja.
        if flavors:
            props["íz"] = flavors
        props["energiatartalom"] = energy_state(product, old_props)
        label_text = product_label_text(product)
        if (
            product_id(product) in {"4606916", "4606917", "4606918"}
            or "vitamin" in label_text
            or "vitamixx" in label_text
            or "multivitamin" in label_text
        ):
            props["vitamin"] = True
    product["tulajdonsagok"] = props


def normalize_baby_water(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    props = physical_properties(old_props)
    props["márka"] = canonical_brand(product, old_props)
    props["szénsavasság"] = carbonation_value(product, old_props)
    product["tulajdonsagok"] = props


PLANT_BASE_ATOMS = frozenset(
    {
        "zab",
        "mandula",
        "rizs",
        "kokusz",
        "szoja",
        "mogyoro",
        "kesudio",
        "borso",
        "hajdina",
        "kender",
        "quinoa",
        "tonkoly",
    }
)


def normalize_plant(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    props = physical_properties(old_props)
    props["márka"] = canonical_brand(product, old_props)

    bases: list[str] = []
    for raw in values_of(old_props.get("alap")):
        folded = fold_text(raw)
        if folded in PLANT_BASE_ATOMS:
            bases.append(str(raw).casefold())
    bases = dedupe(bases)
    if bases:
        props["alap"] = bases

    raw_flavors = values_of(old_props.get("íz"))
    flavors: list[str] = []
    base_markers = {fold_text(value) for value in bases}
    for raw in raw_flavors:
        folded = fold_text(raw)
        if folded in {"not milk", "not milk semi", "not milk whole", "szoja"}:
            continue
        if folded == "tea":
            raw = "matcha"
            folded = "matcha"
        if folded in base_markers:
            continue
        flavors.extend(flavor_atoms([raw]))
    flavors = dedupe(
        value
        for value in flavors
        if fold_text(value) not in base_markers
    )
    if flavors:
        props["íz"] = flavors

    if "zsírtartalom" in old_props:
        raw_fat = first_value(old_props["zsírtartalom"])
        if raw_fat not in (None, ""):
            props["zsírtartalom"] = raw_fat
    if bool_value(old_props.get("cukormentes")):
        props["cukormentes"] = True

    text = product_text(product, old_props)
    sweetness = first_value(old_props.get("édesség"))
    if sweetness:
        props["édesség"] = str(sweetness).casefold()
    elif "nem edesitett" in text or "unsweetened" in text:
        props["édesség"] = "nem édesített"
    elif re.search(r"\bedesitett\b|\bsweetened\b", text):
        props["édesség"] = "édesített"

    item_id = product_id(product)
    barista = (
        "barista" in fold_text(product_name(product))
        or any(fold_text(value) == "barista" for value in values_of(old_props.get("felhasználás")))
        or any(fold_text(value) == "barista" for value in values_of(old_props.get("változat")))
    )
    if item_id in {"116836844", "116836845"}:
        barista = False
    if item_id in {"105006980", "220206696"}:
        barista = True
    if barista:
        props["barista"] = True

    enrichments = flavor_atoms(
        [
            *values_of(old_props.get("tartalom")),
            *values_of(old_props.get("dúsítás")),
        ],
        remove=frozenset({"protein"}),
    )
    if enrichments:
        props["dúsítás"] = enrichments
    heat = first_value(old_props.get("hőkezelés")) or first_value(old_props.get("feldolgozás"))
    if heat:
        props["hőkezelés"] = str(heat)
    product["tulajdonsagok"] = props


def cocoa_kind(product: dict[str, Any], old_props: dict[str, Any]) -> str:
    item_id = product_id(product)
    current_path = path_of(product)
    termek_tipus = fold_text(first_value(old_props.get("terméktípus")))
    old_sweetness = fold_text(first_value(old_props.get("cukrozottság")))
    if current_path == COCOA_PATH:
        return "pure" if old_sweetness == "natur" else "drink"
    if item_id in COCOA_PURE_OVERRIDE_IDS:
        return "pure"
    if termek_tipus == "kakaopor":
        return "pure"
    if (
        current_path[0] == COCOA_PATH[0]
        and current_path[1] == COCOA_PATH[1]
        and current_path[2] in {COCOA_OLD_LEAF, COCOA_MIXED_LEAF}
    ):
        return "pure"
    return "drink"


def normalize_cocoa(
    product: dict[str, Any],
    old_props: dict[str, Any],
    *,
    kind: str,
) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    item_id = product_id(product)
    if kind == "pure":
        props["cukrozottság"] = "natúr"
        props["kakaótartalom"] = "100%"
        raw_fat = first_value(old_props.get("zsírtartalom"))
        if raw_fat:
            props["zsírtartalom"] = str(raw_fat)
    else:
        props["cukrozottság"] = (
            "édesítőszeres" if item_id in COCOA_SWEETENER_IDS else "cukrozott"
        )
        if item_id in COCOA_KNOWN_PERCENT:
            props["kakaótartalom"] = COCOA_KNOWN_PERCENT[item_id]
    product["tulajdonsagok"] = props


def normalize_hot_chocolate(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    text = product_text(product, old_props)
    old_flavors = [*values_of(old_props.get("íz")), *values_of(old_props.get("összetevő"))]
    existing_type = first_value(old_props.get("csokoládétípus"))
    if product_id(product) in HOT_CHOCOLATE_TYPE_BY_ID:
        chocolate_type = HOT_CHOCOLATE_TYPE_BY_ID[product_id(product)]
    elif existing_type in {"klasszikus", "ét", "fehér", "tej"}:
        chocolate_type = str(existing_type)
    elif re.search(r"\bfeher\b|\bwhite\b", text):
        chocolate_type = "fehér"
    elif re.search(r"\betcsokolade\b|\bdark chocolate\b|\bet\b", text):
        chocolate_type = "ét"
    elif "tejcsokolade" in text or any(fold_text(value) == "tejes" for value in old_flavors):
        chocolate_type = "tej"
    else:
        chocolate_type = "klasszikus"
    props["csokoládétípus"] = chocolate_type
    flavors = flavor_atoms(
        old_flavors,
        remove=frozenset({"kakao", "csokolade", "natur", "kola", "tejes"}),
    )
    if flavors:
        props["íz"] = flavors
    product["tulajdonsagok"] = props


def normalize_additive(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    raw_type = fold_text(first_value(old_props.get("típus")) or first_value(old_props.get("terméktípus")))
    if "tejszin" in raw_type:
        kind = "tejszín"
    elif "tejpor" in raw_type and "kavefeherito" not in raw_type:
        kind = "tejpor"
    else:
        kind = "krémpor"
    product["tulajdonsagok"] = {
        "márka": canonical_brand(product, old_props),
        "típus": kind,
    }


TEA_VARIETY_MAP = {
    "earl grey": "Earl Grey",
    "english breakfast": "English Breakfast",
    "lady grey": "Lady Grey",
    "ceylon supreme": "Ceylon Supreme",
    "sencha": "Sencha",
    "matcha": "Matcha",
    "zserbo": "Zserbó",
    "premium assam": "Assam",
}
TEA_NON_VARIETY_VALUES = frozenset(
    {
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
    }
)
TEA_TYPE_BY_ID = {
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


def tea_form(product: dict[str, Any], old_props: dict[str, Any]) -> str:
    item_id = product_id(product)
    if item_id in TEA_LOOSE_OVERRIDE_IDS:
        return "teafű"
    if item_id in TEA_POWDER_OVERRIDE_IDS:
        return "por"
    forms = {fold_text(value) for value in values_of(old_props.get("forma"))}
    if forms & {"szalas", "teafu"}:
        return "teafű"
    if "por" in forms:
        return "por"
    return "filteres"


def normalize_tea(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    props: dict[str, Any] = {
        "márka": canonical_brand(product, old_props),
        "forma": tea_form(product, old_props),
    }
    varieties: list[str] = []
    ingredients_raw: list[Any] = [
        *values_of(old_props.get("íz")),
        *values_of(old_props.get("összetevő")),
        *values_of(old_props.get("hatóanyag")),
    ]

    for raw in [
        *values_of(old_props.get("fajta")),
        *values_of(old_props.get("változat")),
    ]:
        folded = fold_text(raw)
        if folded == "feher":
            continue
        if folded == "oolong":
            varieties.append("Oolong")
            continue
        if folded == "premium":
            continue
        if folded in {
            "classic matcha latte",
            "mango matcha latte",
            "strawberry matcha latte",
        }:
            varieties.append("Matcha")
            if folded == "mango matcha latte":
                ingredients_raw.append("mangó")
            elif folded == "strawberry matcha latte":
                ingredients_raw.append("eper")
            continue
        if folded in TEA_NON_VARIETY_VALUES:
            continue
        varieties.append(TEA_VARIETY_MAP.get(folded, str(raw)))

    remaining_ingredients: list[Any] = []
    for raw in ingredients_raw:
        folded = fold_text(raw)
        if folded == "earl grey lemon":
            varieties.append("Earl Grey")
            remaining_ingredients.append("citrom")
            continue
        if folded in TEA_VARIETY_MAP:
            varieties.append(TEA_VARIETY_MAP[folded])
            continue
        remaining_ingredients.append(raw)
    if varieties:
        props["fajta"] = dedupe(varieties)

    ingredients = flavor_atoms(
        remaining_ingredients,
        remove=frozenset(
            {
                "natur",
                "tea",
                "gyogynoveny",
                "gyumolcs",
                "fantazia",
                "fuszeres",
                "gyumolcs variaciok",
                "vegyes",
                "szuperbogyo",
                "vitamin",
                "mate",
                "b vitamin komplex",
            }
        ),
    )
    if ingredients:
        props["összetevő"] = ingredients

    tea_types = [
        str(value).casefold()
        for value in values_of(old_props.get("teatípus"))
        if value not in (None, "")
    ]
    if product_id(product) in TEA_TYPE_BY_ID:
        tea_types.append(TEA_TYPE_BY_ID[product_id(product)])
    text = product_text(product, old_props)
    raw_varieties = {fold_text(value) for value in values_of(old_props.get("fajta"))}
    if "feher" in raw_varieties or "feher tea" in text:
        tea_types.append("fehér tea")
    if "oolong" in raw_varieties or "oolong" in text:
        tea_types.append("oolong tea")
    if re.search(r"\bmate\b", text):
        tea_types.append("maté tea")
    if "matcha" in text and not any(fold_text(value) == "zold tea" for value in tea_types):
        tea_types.append("zöld tea")
    if not tea_types:
        if "rooibos" in text:
            tea_types.append("rooibos tea")
        elif "zold tea" in text:
            tea_types.append("zöld tea")
        elif "fekete tea" in text:
            tea_types.append("fekete tea")
        elif "gyumolcstea" in text:
            tea_types.append("gyümölcstea")
        elif any(word in text for word in ("gyogytea", "kamilla", "csalan", "harsfavirag")):
            tea_types.append("gyógytea")
    if tea_types:
        props["teatípus"] = dedupe(tea_types)
    product["tulajdonsagok"] = props


COFFEE_ORIGIN_ATOMS = frozenset(
    {
        "brazil",
        "brasil",
        "uganda",
        "kenya",
        "colombia",
        "kolumbia",
        "peru",
        "chiapas",
        "costa rica",
        "india",
        "mexico",
        "guatemala",
        "costa ricai coco",
    }
)

COFFEE_EXACT_VALUE_MAP: dict[str, tuple[str, ...]] = {
    "2 az 1": ("2in1",),
    "2 az 1 ben": ("2in1",),
    "2in1": ("2in1",),
    "3 az 1": ("3in1",),
    "3 az 1 ben": ("3in1",),
    "3in1": ("3in1",),
    "3in1 cappuccino": ("3in1", "cappuccino"),
    "barna cukros": ("barna cukor",),
    "brown sugar": ("barna cukor",),
    "cafe": (),
    "cikoria kave": ("cikória",),
    "creamy latte": ("latte", "krémes"),
    "cappuccino zero": ("cappuccino",),
    "gold decaf": ("gold",),
    "gold selection": ("gold",),
    "granulalt": (),
    "ir krem": ("ír krém",),
    "irish": ("ír krém",),
    "irish cream": ("ír krém",),
    "irish cream likor": ("ír krém",),
    "irish cappuccino": ("ír krém", "cappuccino"),
    "vanilla cappuccino": ("vanília", "cappuccino"),
    "unsweetened": (),
    "zero": (),
    "100 robusta": ("robusta",),
    "selezione arabica": ("arabica",),
    "bon": (),
    "bon aroma": (),
    "fine aroma": ("aromás",),
    "rich": ("aromás",),
    "rich aroma": ("aromás",),
    "gazdag aroma": ("aromás",),
    "telt aromaju": ("aromás",),
    "ahora gold roast": ("ahora", "gold"),
    "calma fine roast": ("calma",),
    "walla dark roast": ("walla",),
    "blonde roast": ("blonde",),
    "italian style roast": ("olasz stílus",),
    "pike place roast": ("pike place",),
    "creamy vanilla": ("vanília", "krémes"),
    "buttertoffee": ("vajkaramella",),
    "double choc": ("csokoládé",),
    "white mocha": ("mocha", "fehér csokoládé"),
    "toasted nut": ("diós",),
    "nut": ("diós",),
    "vanille": ("vanília",),
    "kola": (),
    "extra bar": (),
    "top": (),
}


def coffee_leaf(product: dict[str, Any], old_props: dict[str, Any]) -> str:
    item_id = product_id(product)
    forms = {fold_text(value) for value in values_of(old_props.get("forma"))}
    current_leaf = str(product.get("altipus") or "")
    if item_id in COFFEE_CAPSULE_IDS or "kapszula" in forms or current_leaf == "Kapszulás kávé":
        return "Kapszulás kávé"
    if "szemes" in forms or current_leaf == "Szemes kávé":
        return "Szemes kávé"
    if item_id in COFFEE_PAD_IDS or "orolt" in forms or current_leaf == "Őrölt kávé":
        return "Őrölt kávé"
    return "Instant kávé"


def coffee_flavor_variety(old_props: dict[str, Any], old_brand: str) -> list[str]:
    raw_values = [
        *values_of(old_props.get("íz / fajta")),
        *values_of(old_props.get("íz")),
        *values_of(old_props.get("fajta")),
        *values_of(old_props.get("változat")),
        *values_of(old_props.get("kávékeverék típusa")),
        *values_of(old_props.get("kávéfajta")),
        *values_of(old_props.get("összetevő")),
    ]
    result: list[str] = []
    if fold_text(old_brand) == "omnia":
        result.append("omnia")
    for raw in raw_values:
        folded = fold_text(raw)
        if not folded or folded in {"kave", "natur", "bio"} or folded in COFFEE_ORIGIN_ATOMS:
            continue
        if folded in COFFEE_EXACT_VALUE_MAP:
            result.extend(COFFEE_EXACT_VALUE_MAP[folded])
            continue
        if "espresso" in folded:
            result.append("espresso")
        if "ristretto" in folded:
            result.append("ristretto")
        if "lungo" in folded:
            result.append("lungo")
        if "crema" in folded or "cremoso" in folded:
            result.append("crema")
        if any(token in folded for token in ("intenso", "intense", "intensive", "intenziv", "strong", "forte")):
            result.append("intenzív")
        if any(token in folded for token in ("classic", "classico", "klasszikus")):
            result.append("klasszikus")
        handled = any(
            token in folded
            for token in (
                "espresso",
                "ristretto",
                "lungo",
                "crema",
                "cremoso",
                "intenso",
                "intense",
                "intensive",
                "intenziv",
                "strong",
                "forte",
                "classic",
                "classico",
                "klasszikus",
            )
        )
        if handled:
            continue
        result.extend(
            flavor_atoms(
                [raw],
                remove=COFFEE_ORIGIN_ATOMS | frozenset({"kave", "natur", "bio"}),
            )
        )
    return dedupe(result)


def normalize_coffee(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    old_brand = str(first_value(old_props.get("márka")) or "")
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    text = fold_text(product_name(product))
    decaf = (
        bool_value(old_props.get("koffeinmentes"))
        or product_id(product) in COFFEE_NATURAL_DECAF_IDS
        or any(token in text for token in ("koffeinmentes", "decaf", "deca ", " cikoria", "gabonakave"))
    )
    # A Ricoré valódi kávét is tartalmaz, ezért a cikóriatartalma önmagában
    # nem teszi koffeinmentessé.
    if "ricore" in text and "koffeinmentes" not in text:
        decaf = False
    props["koffeinmentes"] = bool(decaf)
    combined = coffee_flavor_variety(old_props, old_brand)
    if combined:
        props["íz / fajta"] = combined
    if product_id(product) in COFFEE_INTENSITY:
        props["intenzitás"] = COFFEE_INTENSITY[product_id(product)]
    product["tulajdonsagok"] = props


def normalize_base(product: dict[str, Any], old_props: dict[str, Any], leaf: str) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    raw = [
        *values_of(old_props.get("összetevő / íz")),
        *values_of(old_props.get("íz")),
        *values_of(old_props.get("összetevő")),
        *values_of(old_props.get("fajta")),
    ]
    remove = (
        {"repa", "sargarepa"}
        if product_id(product) in FALSE_CARROT_FLAVOR_IDS
        else set()
    )
    remove.update(
        {
            "multivitamin",
            "gyumolcs",
            "vegyes",
            "edes",
            "savanyu",
            "sos",
        }
    )
    flavors = flavor_atoms(raw, remove=frozenset(remove))
    if product_id(product) in {
        "d9772d1f89be796fb34ec9d0",
        "3435092401126e1473cb7b3c",
        "e5b810005409b5c600008e20",
        "763c43451b13eb805b5de259",
        "aa8717e4a5f51bf5371c10de",
    } and "mix" in {fold_text(value) for value in raw}:
        flavors = ["málna", "erdei gyümölcs", "citrom", "tea", "őszibarack"]
    if product_id(product) in BASE_FLAVORS_BY_ID:
        flavors = list(BASE_FLAVORS_BY_ID[product_id(product)])
    concrete_citrus = {
        "citrom",
        "lime",
        "narancs",
        "grapefruit",
        "mandarin",
        "pomelo",
    }
    flavor_markers = {fold_text(value) for value in flavors}
    if flavor_markers & concrete_citrus:
        flavors = [
            value
            for value in flavors
            if fold_text(value) not in {"citrus mix", "citrus"}
        ]
    else:
        flavors = [
            "citrus" if fold_text(value) == "citrus mix" else value
            for value in flavors
        ]
    if fold_text(props["márka"]) == "pepsi":
        flavors = ["kóla" if fold_text(value) == "pepsi" else value for value in flavors]
    flavors = dedupe(flavors)
    if flavors:
        props["összetevő / íz"] = flavors
    props["energiatartalom"] = BASE_ENERGY_BY_ID.get(
        product_id(product),
        energy_state(product, old_props, syrup=True),
    )
    if leaf == "Italtabletta és pezsgőkocka":
        props["vitamint tartalmaz"] = True
        if product_id(product) in HAAS_VITAMIN_IDS:
            props["vitamin"] = ["C-vitamin"]
    if leaf == "Szörp és koncentrátum" and "bubble12" in product_text(product, old_props):
        props["hígítási arány"] = "1:23"
    product["tulajdonsagok"] = props


def normalize_fruit(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    raw_percent = first_value(old_props.get("gyümölcstartalom"))
    percent_source = str(raw_percent) if raw_percent not in (None, "") else product_name(product)
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*%", percent_source)
    if match:
        number = match.group(1).replace(".", ",")
        if number.endswith(",0"):
            number = number[:-2]
        props["gyümölcstartalom"] = f"{number}%"
    raw_flavors = [
        *values_of(old_props.get("íz")),
        *values_of(old_props.get("gyümölcs")),
        *values_of(old_props.get("zöldség")),
        *values_of(old_props.get("összetevő")),
    ]
    flavors = flavor_atoms(
        raw_flavors,
        remove=frozenset(
            {
                "multivitamin",
                "vitamin",
                "gyumolcs",
                "zoldseg",
                "gyumolcsle",
                "vegyes",
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
                "natur",
                "almale suritmeny",
                "zoldalma pure",
                "repale",
                "szurt viz",
                "nata de coco",
                "spirulina",
                "spirulina alga kivonat",
                "rizs",
                "griz",
                "boba",
            }
        ),
    )
    if flavors:
        props["íz"] = flavors
    text = product_label_text(product)
    props["rostos"] = bool(bool_value(old_props.get("rostos")) or "rostos" in text)
    props["cukormentes"] = bool(
        bool_value(old_props.get("cukormentes"))
        or "cukormentes" in text
        or "zero sugar" in text
    )
    product["tulajdonsagok"] = props


def normalize_soft(product: dict[str, Any], old_props: dict[str, Any], leaf: str) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    raw_flavors = [
        *values_of(old_props.get("íz")),
        *values_of(old_props.get("összetevő")),
        *values_of(old_props.get("gyümölcs")),
    ]
    remove = {
        "multivitamin",
        "vitamin",
        "ginger ale",
        "kofola",
        "juicy soda",
        "pink aromatic berry",
        "halloween",
        "frissito",
        "tejes",
    }
    item_id = product_id(product)
    name_folded = fold_text(product_name(product))
    flavors = flavor_atoms(raw_flavors, remove=frozenset(remove))

    if leaf == "Kóla":
        flavors = [
            value
            for value in flavors
            if fold_text(value) not in {"kola", "cola", "dr pepper"}
        ]
    elif leaf == "Tonik":
        flavors = [
            value for value in flavors if fold_text(value) not in {"tonik", "tonic"}
        ]
    elif leaf == "Jegestea":
        flavors = [value for value in flavors if fold_text(value) != "tea"]

    if "cappy ice fruit" in name_folded:
        if "mangosztan" in name_folded:
            flavors = [
                value for value in flavors if fold_text(value) not in {"mango", "multivitamin"}
            ]
            flavors.append("mangosztán")
        if "sargadinnye" in name_folded:
            flavors = [
                value for value in flavors if fold_text(value) not in {"gorogdinnye", "citrom"}
            ]
            flavors.append("sárgadinnye")
        if "citromfu" in name_folded:
            flavors = [value for value in flavors if fold_text(value) != "citrom"]
            flavors.append("citromfű")
        if "bogyo" in name_folded:
            flavors = [
                value
                for value in flavors
                if fold_text(value) not in {"vegyes bogyos", "bogyos gyumolcs"}
            ]
            flavors.append("erdei gyümölcs")

    if leaf in {"Kóla", "Tonik"} and not flavors:
        flavors = ["natúr"]
    if flavors:
        props["íz"] = dedupe(flavors)
    if leaf != "Jegestea":
        props["szénsavas"] = carbonated_bool(product, old_props, leaf)
    props["energiatartalom"] = energy_state(product, old_props)
    product["tulajdonsagok"] = props


def normalize_energy_drink(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    flavors = flavor_atoms(
        [
            *values_of(old_props.get("íz")),
            *values_of(old_props.get("összetevő")),
        ],
        remove=frozenset(
            {
                "energia",
                "koffein",
                "vitamin",
                "natur",
                "doctor",
                "extra strong",
                "focus",
                "fokusz",
                "full throttle",
                "green",
                "feher",
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
            }
        ),
    )
    if flavors:
        props["íz"] = flavors
    props["cukormentes"] = bool(
        bool_value(old_props.get("cukormentes"))
        or "cukormentes" in product_label_text(product)
        or re.search(r"\bzero\b", product_label_text(product))
    )
    props["szénsavas"] = carbonated_bool(product, old_props, "Energiaital")
    if bool_value(old_props.get("koffeinmentes")):
        props["koffeinmentes"] = True
    product["tulajdonsagok"] = props


def normalize_functional(
    product: dict[str, Any],
    old_props: dict[str, Any],
    *,
    source_sport: bool = False,
) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    flavors = flavor_atoms(
        [
            *values_of(old_props.get("íz")),
            *values_of(old_props.get("összetevő")),
            *values_of(old_props.get("gyümölcs")),
        ],
        remove=frozenset(
            {
                "sportital",
                "izotonias ital",
                "kollagen",
                "shot",
                "vitamin",
                "energia",
                "mountain blast",
                "cool blue",
                "izotonias",
                "barcelona edition",
            }
        ),
    )
    if flavors:
        props["íz"] = flavors
    text = product_text(product, old_props)
    functions: list[str] = []
    old_function = " ".join(
        fold_text(value)
        for name in ("funkció", "funkcionális jelleg", "funkció / jelleg")
        for value in values_of(old_props.get(name))
    )
    if source_sport or "sportital" in text or "sport ital" in text or "sport" in old_function:
        functions.append("sportital")
    if "izoton" in text or "izoton" in old_function:
        functions.append("izotóniás")
    if "kollagen" in text:
        functions.append("kollagén")
    if product_id(product) in SHOT_IDS or "shot" in old_function:
        functions.append("shot")
    functions = dedupe(functions)
    if not functions:
        raise RuntimeError(
            f"Funkcionális jelleg nélkül maradt: {product_id(product)} / {product_name(product)}"
        )
    props["funkció"] = functions
    product["tulajdonsagok"] = props


def normalize_gel(product: dict[str, Any], old_props: dict[str, Any]) -> None:
    props: dict[str, Any] = {"márka": canonical_brand(product, old_props)}
    flavors = flavor_atoms(
        [*values_of(old_props.get("íz")), *values_of(old_props.get("összetevő"))]
    )
    if flavors:
        props["íz"] = flavors
    props["állag"] = "gél"
    size = first_value(old_props.get("kiszerelés"))
    if size:
        props["kiszerelés"] = size
    product["tulajdonsagok"] = props


def normalize_flavoring_straw(
    product: dict[str, Any],
    old_props: dict[str, Any],
) -> None:
    """A tejízesítő cukordrazsés szívószálak Drazsé-sémája.

    Ugyanezt az elemi tulajdonságkészletet használják a már helyesen ezen a
    levélen lévő Quick Milk szívószálak is.
    """

    flavors = flavor_atoms(values_of(old_props.get("íz")))
    if len(flavors) != 1:
        raise RuntimeError(
            f"A szívószál íze nem egyetlen atom: {product_id(product)} / {flavors}"
        )
    product["tulajdonsagok"] = {
        "márka": canonical_brand(product, old_props),
        "íz": flavors,
        "forma": ["szívószál"],
        "cukormentes / hozzáadott cukor nélkül": False,
        "mentolos": False,
        "savanyú": False,
        "alkoholos": False,
    }


def is_current_alcohol(product: dict[str, Any]) -> bool:
    return product.get("fokategoria") == ITAL and product.get("alkategoria") == ALCOHOL


def is_cocoa_external_source(product: dict[str, Any]) -> bool:
    path = path_of(product)
    if path == COCOA_PATH:
        return True
    if path[:2] != COCOA_PATH[:2]:
        return False
    if path[2] == COCOA_OLD_LEAF:
        return True
    return path[2] == COCOA_MIXED_LEAF and product_id(product) in COCOA_MIXED_SOURCE_IDS


def is_cocoa_source(product: dict[str, Any], old_props: dict[str, Any]) -> bool:
    path = path_of(product)
    if is_cocoa_external_source(product):
        return True
    return (
        path[0] == ITAL
        and path[1] in {OLD_HOT, HOT}
        and path[2] in {"Kakaó és forró csokoládé", "Forró csokoládé"}
        and path[2] != "Forró csokoládé"
    )


def is_hot_chocolate(product: dict[str, Any], old_props: dict[str, Any]) -> bool:
    if path_of(product) == (ITAL, HOT, "Forró csokoládé"):
        return True
    if product_id(product) == COCOA_FRAPPE_ID:
        return False
    return fold_text(first_value(old_props.get("terméktípus"))) == "forro csokolade"


def is_plant_product(product: dict[str, Any]) -> bool:
    path = path_of(product)
    return (
        path[0] == ITAL and path[1] == OLD_PLANT
    ) or path == PLANT_PATH


def functional_source_target(
    product: dict[str, Any],
    old_props: dict[str, Any],
) -> tuple[str, str, str] | None:
    path = path_of(product)
    if path == (ITAL, FUNCTIONAL, "Energiaital"):
        return path
    if path == (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"):
        return path
    if path[0] != ITAL or path[1] != OLD_FUNCTIONAL:
        return None

    item_id = product_id(product)
    old_leaf = path[2]
    text = product_text(product, old_props)
    brand = fold_text(canonical_brand(product, old_props))

    if old_leaf == "Energiaital":
        return (ITAL, FUNCTIONAL, "Energiaital")
    if item_id in GEL_IDS or "energiazsele" in text:
        return GEL_PATH
    if (
        item_id in SHOT_IDS
        or any(fold_text(value) == "shot" for value in values_of(old_props.get("forma")))
        or old_leaf == "Sport- és izotóniás ital"
        or "kollagen" in text
    ):
        return (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital")
    if brand == "new gen":
        return (ITAL, FUNCTIONAL, "Energiaital")
    if re.search(r"100\s*%", product_name(product)) or (
        brand == "hohes c" and "classic multivitamin" in text and "gyumolcsle" in text
    ):
        return (ITAL, FRUIT, "Lé")
    if brand in {"kubu", "topjoy", "rauch", "hey ho"}:
        return (ITAL, FRUIT, "Gyümölcsital")
    if brand == "vitamizu":
        return (ITAL, SOFT, "Jegestea")

    water_brands = {
        "active o2",
        "viwa",
        "aqvital",
        "fonte",
        "kekforras",
        "szentkiralyi",
        "theodora",
    }
    is_apenta_water = brand == "apenta" and (
        "vitamixx" in text
        or "energy water" in text
        or item_id in {"2808597", "2807793", "3380683"}
    )
    is_hohes_water = brand == "hohes c" and (
        "vitamin water" in text or "vitaminviz" in text
    )
    if brand in water_brands or is_apenta_water or is_hohes_water:
        return (ITAL, WATER, "Ízesített víz")
    return (ITAL, SOFT, "Egyéb ízesített üdítőital")


def is_named_flavored_water(product: dict[str, Any]) -> bool:
    text = fold_text(product_name(product))
    return any(
        marker in text
        for marker in (
            "apenta vitamixx",
            "apenta light",
            "active o2",
            "kubu waterr",
        )
    ) or product_id(product) in {"2808597", "2807793", "3380683"}


def current_base_leaf(product: dict[str, Any], old_props: dict[str, Any]) -> str | None:
    path = path_of(product)
    if path[0] != ITAL or path[1] not in {OLD_BASE, BASES}:
        return None
    item_id = product_id(product)
    if path[1] == BASES and path[2] in TARGET_HIERARCHY[BASES]:
        return path[2]
    if item_id in TABLET_IDS:
        return "Italtabletta és pezsgőkocka"
    if item_id in BASE_POWDER_FROM_LIQUID_IDS:
        return "Italpor"
    if path[2] == "Italpor és tabletta":
        return "Italpor"
    return "Szörp és koncentrátum"


def current_hot_kind(product: dict[str, Any], old_props: dict[str, Any]) -> str | None:
    path = path_of(product)
    if path[0] != ITAL or path[1] not in {OLD_HOT, HOT}:
        return None
    if path[2] in {"Kávé", "Instant kávé", "Őrölt kávé", "Szemes kávé", "Kapszulás kávé"}:
        return "coffee"
    if path[2] == "Tea":
        return "tea"
    if path[2] in {"Kávé- és teaadalék", "Krém, tejpor és tejszín"}:
        return "additive"
    if path[2] == "Forró csokoládé":
        return "hot"
    if path[2] == "Kakaó és forró csokoládé":
        return "hot" if is_hot_chocolate(product, old_props) else "cocoa"
    return None


def transform_product(product: dict[str, Any]) -> None:
    # A normalizálók csak olvassák a forrást, majd új dictet rendelnek a
    # termékhez; ezért nincs szükség termékenkénti általános deepcopy-ra.
    old_props = product.get("tulajdonsagok") or {}
    original_path = path_of(product)
    item_id = product_id(product)

    if is_current_alcohol(product):
        return

    if item_id in STRAW_IDS:
        set_path(product, DRAGEE_PATH)
        normalize_flavoring_straw(product, old_props)
        return

    if item_id in MILKSHAKE_POWDER_IDS:
        set_path(product, (ITAL, BASES, "Italpor"))
        normalize_base(product, old_props, "Italpor")
        return

    if original_path == GEL_PATH:
        normalize_gel(product, old_props)
        return

    if item_id in BABY_WATER_IDS or original_path == BABY_WATER_PATH:
        set_path(product, BABY_WATER_PATH)
        normalize_baby_water(product, old_props)
        return

    if is_plant_product(product):
        set_path(product, PLANT_PATH)
        normalize_plant(product, old_props)
        return

    if is_cocoa_external_source(product):
        kind = cocoa_kind(product, old_props)
        set_path(product, COCOA_PATH)
        normalize_cocoa(product, old_props, kind=kind)
        return

    hot_kind = current_hot_kind(product, old_props)
    if hot_kind == "cocoa":
        kind = cocoa_kind(product, old_props)
        set_path(product, COCOA_PATH)
        normalize_cocoa(product, old_props, kind=kind)
        return
    if hot_kind == "hot":
        set_path(product, (ITAL, HOT, "Forró csokoládé"))
        normalize_hot_chocolate(product, old_props)
        return
    if hot_kind == "additive":
        set_path(product, (ITAL, HOT, "Krém, tejpor és tejszín"))
        normalize_additive(product, old_props)
        return
    if hot_kind == "tea":
        set_path(product, (ITAL, HOT, "Tea"))
        normalize_tea(product, old_props)
        return
    if hot_kind == "coffee":
        leaf = coffee_leaf(product, old_props)
        set_path(product, (ITAL, HOT, leaf))
        normalize_coffee(product, old_props)
        return

    base_leaf = current_base_leaf(product, old_props)
    if base_leaf is not None:
        set_path(product, (ITAL, BASES, base_leaf))
        normalize_base(product, old_props, base_leaf)
        return

    if item_id in GEL_IDS:
        set_path(product, GEL_PATH)
        normalize_gel(product, old_props)
        return
    if item_id in SHOT_IDS:
        set_path(product, (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"))
        normalize_functional(product, old_props)
        return
    if item_id in DR_PEPPER_IDS:
        set_path(product, (ITAL, SOFT, "Kóla"))
        normalize_soft(product, old_props, "Kóla")
        return
    if item_id in KIDS_IDS:
        set_path(product, (ITAL, SOFT, "Kölyökpezsgő"))
        normalize_soft(product, old_props, "Kölyökpezsgő")
        return
    if item_id in YIPPY_COLA_IDS:
        set_path(product, (ITAL, SOFT, "Kóla"))
        normalize_soft(product, old_props, "Kóla")
        return
    if "cappy ice fruit" in fold_text(product_name(product)):
        set_path(product, (ITAL, SOFT, "Egyéb ízesített üdítőital"))
        normalize_soft(product, old_props, "Egyéb ízesített üdítőital")
        return
    if is_named_flavored_water(product):
        set_path(product, (ITAL, WATER, "Ízesített víz"))
        normalize_water(product, old_props, flavored=True)
        return

    functional_target = functional_source_target(product, old_props)
    if functional_target is not None:
        set_path(product, functional_target)
        if functional_target == GEL_PATH:
            normalize_gel(product, old_props)
            return
        if functional_target[1] == FUNCTIONAL:
            if functional_target[2] == "Energiaital":
                normalize_energy_drink(product, old_props)
            else:
                normalize_functional(
                    product,
                    old_props,
                    source_sport=original_path[2] == "Sport- és izotóniás ital",
                )
        elif functional_target[1] == WATER:
            normalize_water(product, old_props, flavored=True)
        elif functional_target[1] == FRUIT:
            normalize_fruit(product, old_props)
        else:
            normalize_soft(product, old_props, functional_target[2])
        return

    if original_path[0] != ITAL:
        return

    parent, leaf = original_path[1], original_path[2]
    if parent in {OLD_WATER, WATER}:
        flavored = leaf == "Ízesített víz"
        set_path(
            product,
            (ITAL, WATER, "Ízesített víz" if flavored else "Ízesítetlen palackozott víz"),
        )
        normalize_water(product, old_props, flavored=flavored)
        return
    if parent == SOFT:
        if leaf == "Limonádé":
            leaf = "Jegestea" if item_id in LEMONADE_TEA_IDS else "Egyéb ízesített üdítőital"
        set_path(product, (ITAL, SOFT, leaf))
        normalize_soft(product, old_props, leaf)
        return
    if parent == FRUIT:
        set_path(product, (ITAL, FRUIT, leaf))
        normalize_fruit(product, old_props)
        return
    if parent == FUNCTIONAL:
        if leaf == "Energiaital":
            normalize_energy_drink(product, old_props)
        else:
            normalize_functional(product, old_props)
        return
    raise RuntimeError(
        f"Kezeletlen nem alkoholos Ital-termék: {item_id} / {original_path} / {product_name(product)}"
    )


def products_at(
    products: list[dict[str, Any]],
    path: tuple[str, str, str],
) -> list[dict[str, Any]]:
    return [product for product in products if path_of(product) == path]


def category_parent(
    categories: dict[str, Any],
    path: tuple[str, str, str],
) -> dict[str, Any]:
    return categories[path[0]][ALK_KEY][path[1]]


def set_leaf_from_products(
    categories: dict[str, Any],
    products: list[dict[str, Any]],
    path: tuple[str, str, str],
) -> None:
    items = products_at(products, path)
    if not items:
        raise RuntimeError(f"Üres külső céllevél: {' > '.join(path)}")
    parent = category_parent(categories, path)
    parent.setdefault(ALT_KEY, {})[path[2]] = {PROP_KEY: build_prop_block(items)}


def extend_leaf_declarations(
    categories: dict[str, Any],
    products: list[dict[str, Any]],
    path: tuple[str, str, str],
    item_ids: frozenset[str],
) -> None:
    """Csak az újonnan mozgatott termékek értékeivel bővít egy külső levelet."""

    items = [
        product
        for product in products
        if product_id(product) in item_ids and path_of(product) == path
    ]
    if {product_id(product) for product in items} != set(item_ids):
        raise RuntimeError(f"Hiányos külső mozgatási halmaz: {' > '.join(path)}")
    additions = build_prop_block(items)
    leaf = category_parent(categories, path)[ALT_KEY][path[2]]
    declared = leaf[PROP_KEY]
    for section in ("egyedi", "csoportos"):
        opposite = "csoportos" if section == "egyedi" else "egyedi"
        target = declared.setdefault(section, {})
        for name, allowed in additions[section].items():
            if name in declared.setdefault(opposite, {}):
                raise RuntimeError(
                    f"Eltérő tulajdonságalak a külső levélen: {name!r}"
                )
            if name not in target:
                target[name] = clone_json_value(allowed)
                continue
            if isinstance(allowed, dict):
                if target[name] != {}:
                    raise RuntimeError(
                        f"Nem boolean deklaráció a külső levélen: {name!r}"
                    )
                continue
            if not isinstance(target[name], list):
                raise RuntimeError(
                    f"Nem értéklista a külső levélen: {name!r}"
                )
            target[name] = dedupe([*target[name], *allowed])


def rebuild_categories(
    categories: dict[str, Any],
    products: list[dict[str, Any]],
    alcohol_node: dict[str, Any],
) -> None:
    by_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        if product.get("fokategoria") == ITAL:
            by_path[
                (
                    str(product.get("alkategoria") or ""),
                    str(product.get("altipus") or ""),
                )
            ].append(product)
    if set(by_path) != set(TARGET_PATHS):
        raise RuntimeError(
            "A célfa és a termékutak eltérnek: "
            f"hiány={sorted(TARGET_PATHS - set(by_path))}, "
            f"váratlan={sorted(set(by_path) - TARGET_PATHS)}"
        )

    parents: dict[str, Any] = {}
    for parent_name, leaves in TARGET_HIERARCHY.items():
        if parent_name == ALCOHOL:
            # A régi fanódot sem itt, sem később nem módosítjuk; az eredeti
            # objektum átemelése byte-szinten is ugyanazt a tartalmat őrzi meg.
            parents[parent_name] = alcohol_node
            continue
        node = {PROP_KEY: {"egyedi": {}, "csoportos": {}}, ALT_KEY: {}}
        for leaf_name in leaves:
            node[ALT_KEY][leaf_name] = {
                PROP_KEY: build_prop_block(by_path[(parent_name, leaf_name)])
            }
        parents[parent_name] = node
    categories[ITAL] = {
        PROP_KEY: {"egyedi": {}, "csoportos": {}},
        ALK_KEY: parents,
    }

    set_leaf_from_products(categories, products, BABY_WATER_PATH)
    set_leaf_from_products(categories, products, PLANT_PATH)

    cocoa_parent = category_parent(categories, COCOA_PATH)
    cocoa_leaves = cocoa_parent[ALT_KEY]
    cocoa_leaves.pop(COCOA_OLD_LEAF, None)
    set_leaf_from_products(categories, products, COCOA_PATH)

    set_leaf_from_products(categories, products, GEL_PATH)
    extend_leaf_declarations(
        categories,
        products,
        DRAGEE_PATH,
        STRAW_IDS,
    )


def alcohol_payload_hash(products: list[dict[str, Any]]) -> str:
    states = [
        {
            "id": product_id(product),
            "név": product_name(product),
            "út": list(path_of(product)),
            "tulajdonságok": product.get("tulajdonsagok") or {},
        }
        for product in products
        if is_current_alcohol(product)
    ]
    states.sort(key=lambda item: item["id"])
    encoded = json.dumps(states, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def path_counts(products: list[dict[str, Any]]) -> dict[str, int]:
    counts = Counter(
        " > ".join(path_of(product))
        for product in products
        if product.get("fokategoria") == ITAL
    )
    return dict(sorted(counts.items(), key=lambda item: fold_text(item[0])))


def validate_internal(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
    *,
    original_paths: list[tuple[str, str, str]],
    original_alcohol_hash: str,
    original_alcohol_node: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    if len(products) != EXPECTED_TOTAL:
        errors.append(f"termékszám={len(products)}")

    ital_items = [product for product in products if product.get("fokategoria") == ITAL]
    paths = {(product.get("alkategoria"), product.get("altipus")) for product in ital_items}
    if paths != set(TARGET_PATHS):
        errors.append("Ital célút-paritás hibás")

    expected_counts = {
        (ITAL, ALCOHOL, None): 5500,
        PLANT_PATH: 231,
        BABY_WATER_PATH: 21,
        COCOA_PATH: 108,
        DRAGEE_PATH: 151,
        GEL_PATH: 5,
        (ITAL, HOT, "Tea"): 760,
        (ITAL, HOT, "Forró csokoládé"): 25,
        (ITAL, HOT, "Krém, tejpor és tejszín"): 24,
        (ITAL, HOT, "Szemes kávé"): 235,
        (ITAL, HOT, "Őrölt kávé"): 263,
        (ITAL, HOT, "Kapszulás kávé"): 486,
        (ITAL, HOT, "Instant kávé"): 317,
        (ITAL, BASES, "Italtabletta és pezsgőkocka"): 10,
        (ITAL, BASES, "Szörp és koncentrátum"): 391,
        (ITAL, BASES, "Italpor"): 29,
        (ITAL, FUNCTIONAL, "Energiaital"): 346,
        (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"): 139,
    }
    for path, expected in expected_counts.items():
        if path[2] is None:
            actual = sum(
                1
                for product in products
                if product.get("fokategoria") == path[0]
                and product.get("alkategoria") == path[1]
            )
        else:
            actual = len(products_at(products, path))
        if actual != expected:
            errors.append(f"{' > '.join(value or '' for value in path)}={actual}, várt={expected}")

    tea = products_at(products, (ITAL, HOT, "Tea"))
    tea_forms = Counter((product.get("tulajdonsagok") or {}).get("forma") for product in tea)
    if tea_forms != Counter({"filteres": 713, "teafű": 32, "por": 15}):
        errors.append(f"teaforma={dict(tea_forms)}")

    alias_scope = {
        (ITAL, parent, leaf)
        for parent, leaves in TARGET_HIERARCHY.items()
        if parent != ALCOHOL
        for leaf in leaves
    } | {BABY_WATER_PATH, PLANT_PATH, COCOA_PATH, GEL_PATH}
    if any(
        fold_text(value) == "marakuja"
        for product in products
        if path_of(product) in alias_scope
        for value in values_of((product.get("tulajdonsagok") or {}).get("íz"))
    ):
        errors.append("marakuja alias maradt")

    for product in products_at(
        products,
        (ITAL, FUNCTIONAL, "Sport-, izotóniás, kollagén- és shot ital"),
    ):
        functions = {
            fold_text(value)
            for value in values_of((product.get("tulajdonsagok") or {}).get("funkció"))
        }
        if not functions or not functions <= {"sportital", "izotonias", "kollagen", "shot"}:
            errors.append(f"hibás funkció: {product_id(product)} / {sorted(functions)}")

    current_alcohol_products = [p for p in products if is_current_alcohol(p)]
    if alcohol_payload_hash(products) != original_alcohol_hash:
        errors.append("az alkoholos termékpayload módosult")
    current_alcohol_node = categories[ITAL][ALK_KEY][ALCOHOL]
    if current_alcohol_node != original_alcohol_node:
        errors.append("az alkoholos fanód módosult")

    for index, original_path in enumerate(original_paths):
        current_path = path_of(products[index])
        if original_path == current_path and original_path[0] != ITAL:
            continue
        allowed_external = {
            BABY_WATER_PATH,
            PLANT_PATH,
            COCOA_PATH,
            GEL_PATH,
            DRAGEE_PATH,
            (COCOA_PATH[0], COCOA_PATH[1], COCOA_OLD_LEAF),
            (COCOA_PATH[0], COCOA_PATH[1], COCOA_MIXED_LEAF),
        }
        if original_path[0] != ITAL and original_path not in allowed_external and current_path not in allowed_external:
            errors.append(
                f"scope-on kívüli termék útja módosult: "
                f"{index} / {product_id(products[index])}"
            )
            break

    return {
        "status": "ok" if not errors else "error",
        "errors": errors,
        "total_products": len(products),
        "ital_products": len(ital_items),
        "ital_paths": len(paths),
        "alcohol_products": len(current_alcohol_products),
        "alcohol_payload_sha256": alcohol_payload_hash(products),
        "path_counts": path_counts(products),
    }


def run_checker(products_path: Path, categories_path: Path) -> dict[str, Any]:
    crash_codes = {-1073741819, 3221225477}
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
            ],
            cwd=str(BASE),
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = None
        transient_crash = (
            completed.returncode in crash_codes
            or (not completed.stdout.strip() and completed.returncode != 0)
        )
        if transient_crash:
            failures.append(
                f"{attempt}. kísérlet: returncode={completed.returncode}, "
                f"stderr={completed.stderr[-1000:]!r}"
            )
            continue
        if completed.returncode != 0:
            raise RuntimeError(
                "A független ellenőrző hibát jelzett.\n"
                f"STDOUT:\n{completed.stdout[-8000:]}\n"
                f"STDERR:\n{completed.stderr[-8000:]}"
            )
        if not isinstance(payload, dict):
            failures.append(
                f"{attempt}. kísérlet: az ellenőrző nem JSON-t adott vissza; "
                f"stdout={completed.stdout[-1000:]!r}"
            )
            continue
        if payload.get("status") != "ok":
            raise RuntimeError(f"Az ellenőrző státusza nem ok: {payload}")
        return payload
    raise RuntimeError(
        "A független ellenőrző három kísérletből sem futott végig. "
        + " | ".join(failures)
    )


def prepare_candidate_files(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
) -> dict[str, Any]:
    # A nevek konstans, repo-lokális tranzakciós fájlok; egy korábbi kemény
    # processzleállás után biztonságosan újragenerálhatók.
    for path in (CANDIDATE_PRODUCTS_PATH, CANDIDATE_CATEGORIES_PATH):
        if path.parent != BASE or "italok-20260725.candidate.json" not in path.name:
            raise RuntimeError(f"Nem biztonságos jelölt útvonal: {path}")
        if path.exists():
            path.unlink()
    dump_json(CANDIDATE_PRODUCTS_PATH, products)
    dump_json(CANDIDATE_CATEGORIES_PATH, categories)
    return run_checker(CANDIDATE_PRODUCTS_PATH, CANDIDATE_CATEGORIES_PATH)


def write_transactionally(
    products: list[dict[str, Any]],
    categories: dict[str, Any],
) -> dict[str, Any]:
    candidate_products = CANDIDATE_PRODUCTS_PATH
    candidate_categories = CANDIDATE_CATEGORIES_PATH
    rollback_products = BASE / ".eredmeny.italok-20260725.rollback.json"
    rollback_categories = BASE / ".kategoriak.italok-20260725.rollback.json"
    backup_products = BASE / "eredmeny.before-italok-20260725.json"
    backup_categories = BASE / "kategoriak_2026-06-13.before-italok-20260725.json"
    artifacts = (
        candidate_products,
        candidate_categories,
        rollback_products,
        rollback_categories,
    )
    leftovers = [
        str(path)
        for path in (rollback_products, rollback_categories)
        if path.exists()
    ]
    if leftovers:
        raise RuntimeError(f"Korábbi tranzakciós maradvány található: {leftovers}")

    candidate_check = prepare_candidate_files(products, categories)

    verified_copy(RESULT_PATH, rollback_products)
    verified_copy(CATEGORY_PATH, rollback_categories)
    if not backup_products.exists():
        verified_copy(RESULT_PATH, backup_products)
    if not backup_categories.exists():
        verified_copy(CATEGORY_PATH, backup_categories)

    try:
        os.replace(candidate_products, RESULT_PATH)
        os.replace(candidate_categories, CATEGORY_PATH)
        final_check = run_checker(RESULT_PATH, CATEGORY_PATH)
    except BaseException:
        verified_copy(rollback_products, RESULT_PATH)
        verified_copy(rollback_categories, CATEGORY_PATH)
        run_checker(RESULT_PATH, CATEGORY_PATH)
        raise
    finally:
        for path in artifacts:
            if path.exists():
                path.unlink()
    return {"candidate": candidate_check, "final": final_check}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--apply",
        action="store_true",
        help="A két fő JSON tranzakciós cseréje",
    )
    mode_group.add_argument(
        "--prepare-only",
        action="store_true",
        help="Ellenőrzött jelölt JSON-ok készítése a főfájlok cseréje nélkül",
    )
    parser.add_argument(
        "--assert-idempotent",
        action="store_true",
        help="A célállapot bármely további változását hibának tekinti",
    )
    parser.add_argument(
        "--products-source",
        type=Path,
        default=RESULT_PATH,
        help="Forrás termék-JSON; alapértelmezésben eredmeny.json",
    )
    parser.add_argument(
        "--categories-source",
        type=Path,
        default=CATEGORY_PATH,
        help="Forrás kategóriafa-JSON; alapértelmezésben a fő kategóriafa",
    )
    args = parser.parse_args()

    if not CHECKER_PATH.is_file():
        raise RuntimeError(f"Hiányzó független ellenőrző: {CHECKER_PATH}")
    products = load_json(args.products_source)
    categories = load_json(args.categories_source)
    if not isinstance(products, list) or len(products) != EXPECTED_TOTAL:
        raise RuntimeError(f"Váratlan termékállomány: {type(products).__name__} / {len(products)}")
    if ITAL not in categories or ALCOHOL not in categories[ITAL][ALK_KEY]:
        raise RuntimeError("Hiányzik az Ital vagy az alkoholos ág")

    original_categories_hash = json_value_sha256(categories)
    original_paths = [path_of(product) for product in products]
    alcohol_node = categories[ITAL][ALK_KEY][ALCOHOL]
    original_alcohol_hash = alcohol_payload_hash(products)

    changed_products = 0
    changed_path_counts: Counter[str] = Counter()
    changed_property_counts: Counter[str] = Counter()
    changed_samples: list[dict[str, Any]] = []
    for product in products:
        before_path = path_of(product)
        before_props = product.get("tulajdonsagok") or {}
        transform_product(product)
        after_path = path_of(product)
        after_props = product.get("tulajdonsagok") or {}
        if after_path != before_path or after_props != before_props:
            product["kategoria_hash"] = category_hash(product)
            changed_products += 1
            if args.assert_idempotent:
                changed_path_counts[" > ".join(before_path)] += 1
                if after_path != before_path:
                    changed_property_counts["<útvonal>"] += 1
                for name in set(before_props) | set(after_props):
                    if before_props.get(name) != after_props.get(name):
                        changed_property_counts[name] += 1
                if len(changed_samples) < 20:
                    changed_samples.append(
                        {
                            "id": product_id(product),
                            "út_előtte": list(before_path),
                            "út_utána": list(after_path),
                            "előtte": before_props,
                            "utána": after_props,
                        }
                    )

    rebuild_categories(categories, products, alcohol_node)
    validation = validate_internal(
        products,
        categories,
        original_paths=original_paths,
        original_alcohol_hash=original_alcohol_hash,
        original_alcohol_node=alcohol_node,
    )
    if validation["status"] != "ok":
        print(json.dumps(validation, ensure_ascii=False, indent=2))
        raise RuntimeError(f"A belső validáció hibás: {validation['errors'][:20]}")
    if validation["alcohol_payload_sha256"] != original_alcohol_hash:
        raise RuntimeError("Az alkoholos payload hash-e megváltozott")

    changed_tree = json_value_sha256(categories) != original_categories_hash
    mode = "target-idempotency-check" if not changed_products and not changed_tree else "migration"

    if args.assert_idempotent and (changed_products or changed_tree):
        print(
            json.dumps(
                {
                    "változó_utak": dict(changed_path_counts.most_common()),
                    "változó_tulajdonságok": dict(
                        changed_property_counts.most_common()
                    ),
                    "minták": changed_samples,
                },
                ensure_ascii=False,
                indent=2,
            ),
            file=sys.stderr,
        )
        raise RuntimeError(
            f"Nem idempotens: termékek={changed_products}, fa={changed_tree}"
        )

    summary = {
        "status": "ok",
        "mode": mode,
        "apply": bool(args.apply),
        "prepare_only": bool(args.prepare_only),
        "changed_products": changed_products,
        "category_tree_changed": changed_tree,
        "validation": validation,
    }
    if not args.apply and not args.prepare_only:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    if args.prepare_only:
        candidate_check = prepare_candidate_files(products, categories)
        summary["checker"] = {"candidate": candidate_check}
        print(
            json.dumps(
                {
                    "status": "ok",
                    "mode": mode,
                    "prepared": True,
                    "changed_products": changed_products,
                    "ital_products": validation["ital_products"],
                    "checker": candidate_check["status"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    transaction = write_transactionally(products, categories)
    summary["checker"] = transaction
    summary["generated_at"] = datetime.now().isoformat(timespec="seconds")
    dump_json(AUDIT_PATH, summary)
    print(
        json.dumps(
            {
                "status": "ok",
                "mode": mode,
                "changed_products": changed_products,
                "ital_products": validation["ital_products"],
                "ital_paths": validation["ital_paths"],
                "checker": transaction["final"]["status"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
