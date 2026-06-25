from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
WORK_DIR = BASE_DIR / "tejtermekek_munkafajlok"

MAIN_PRODUCTS = BASE_DIR / "eredmeny.json"
MAIN_CATEGORIES = BASE_DIR / "kategoriak_2026-06-13.json"
REPORT_OUT = WORK_DIR / "tejtermekek_finomitas_2026-06-25.md"
AUDIT_JSON_OUT = WORK_DIR / "tejtermekek_finomitas_2026-06-25.json"

ROOT_NAME = "Tejtermékek és tojás"

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

NOISY_PROPS = {
    "bevonat tipusa",
    "jelleg",
    "termekcsalad",
    "termektipus",
    "toltott",
    "uht",
    "zsirtartalom_jelleg",
}

FORM_ALLOWED_BY_ALK = {
    "sajt": {
        "szeletelt",
        "reszelt",
        "tömb",
        "kenhető",
        "korong",
        "lapka",
        "mini",
        "darabolt",
        "körcikk",
        "rúd",
        "golyó",
        "kocka",
        "fonott",
        "tekercs",
        "falat",
        "félkör",
        "piramis",
    },
    "turo": {
        "rögös",
        "szemcsés",
        "krémes",
        "tömb",
        "leveles",
    },
    "vaj": {
        "tömb",
        "kenhető",
        "adagolt",
        "folyékony",
        "rúd",
    },
    "novenyi alternativa": {
        "tömb",
        "szeletelt",
        "reszelt",
        "kenhető",
        "spray",
        "rúd",
        "kocka",
    },
}

FLAVOR_ATOMS = [
    ("fehér csokoládé", ["feher csokolade", "fehercsokolade", "white chocolate"]),
    ("tejcsokoládé", ["tejcsokolade", "tejes tejcsokolade"]),
    ("étcsokoládé", ["etcsokolade", "et csokolade"]),
    ("csokoládé", ["csokolade", "csokis", "csoki", "choco"]),
    ("kakaó", ["kakao", "kakaos"]),
    ("mogyoró", ["mogyoro", "mogyoros", "mogyorokrem", "mogyorovaj"]),
    ("mogyoróvaj", ["mogyorovajas", "mogyorovaj"]),
    ("eper", ["eper", "epres"]),
    ("málna", ["malna", "malnas"]),
    ("meggy", ["meggy", "meggyes"]),
    ("áfonya", ["afonya", "afonyas"]),
    ("feketeszeder", ["feketeszeder", "fekete szeder"]),
    ("ribizli", ["ribizli", "ribizlis"]),
    ("vörös áfonya", ["vorosafonya", "voros afonya", "vörös áfonya"]),
    ("őszibarack", ["oszibarack", "oszibarackos"]),
    ("sárgabarack", ["sargabarack", "sargabarackos", "kajszibarack", "kajszibarackos"]),
    ("barack", ["barack", "barackos"]),
    ("banán", ["banan", "bananos"]),
    ("alma", ["alma", "almas"]),
    ("szilva", ["szilva", "szilvas"]),
    ("cseresznye", ["cseresznye", "cseresznyes"]),
    ("datolya", ["datolya", "datolyas"]),
    ("kivi", ["kivi", "kiwi"]),
    ("ananász", ["ananasz", "ananászos"]),
    ("narancs", ["narancs", "narancsos"]),
    ("citrom", ["citrom", "citromos"]),
    ("lime", ["lime"]),
    ("mangó", ["mango", "mangos"]),
    ("maracuja", ["maracuja", "passio"]),
    ("piros gyümölcs", ["piros gyumolcs"]),
    ("gránátalma", ["granatalma", "gránátalma"]),
    ("chia", ["chia"]),
    ("kókusz", ["kokusz", "kokuszos"]),
    ("mandula", ["mandula", "mandulas"]),
    ("pisztácia", ["pisztacia", "pisztacias"]),
    ("dió", ["dio", "dios"]),
    ("karamell", ["karamell", "karamellas", "caramel"]),
    ("vanília", ["vanilia", "vanilias"]),
    ("fahéj", ["fahej", "fahejas"]),
    ("méz", ["mez", "mezes"]),
    ("mustár", ["mustar", "mustaros"]),
    ("kávé", ["kave", "kaves", "jegeskave", "tejeskave", "coffee"]),
    ("latte", ["latte"]),
    ("cappuccino", ["cappuccino", "kapuciner"]),
    ("espresso", ["espresso"]),
    ("macchiato", ["macchiato"]),
    ("flat white", ["flat white"]),
    ("madártej", ["madartej"]),
    ("sajttorta", ["sajttorta"]),
    ("keksz", ["keksz", "kekszes", "cookie"]),
    ("brownie", ["brownie"]),
    ("ostya", ["ostya", "ostyas"]),
    ("mák", ["mak", "makos"]),
    ("gríz", ["griz"]),
    ("stracciatella", ["stracciatella", "sztracsatella"]),
    ("natúr", ["natur", "natúr", "original"]),
    ("füstölt", ["fustolt"]),
    ("sós", ["sos", "sós", "sozott", "sózott", "enyhen sozott"]),
    ("édes", ["edes", "édes"]),
    ("tejszín", ["tejszin", "tejszines"]),
    ("tej", ["tejes", "tej"]),
    ("fokhagyma", ["fokhagyma", "fokhagymas"]),
    ("petrezselyem", ["petrezselyem", "petrezselymes"]),
    ("snidling", ["snidling", "metelohagyma", "metélőhagyma"]),
    ("zöldfűszer", ["zoldfuszer", "zoldfuszeres"]),
    ("medvehagyma", ["medvehagyma", "medvehagymas"]),
    ("paradicsom", ["paradicsom", "paradicsomos"]),
    ("bazsalikom", ["bazsalikom", "bazsalikomos"]),
    ("paprika", ["paprika", "paprikas"]),
    ("chili", ["chili", "chilis"]),
    ("csípős", ["csipos", "csípős"]),
    ("sonka", ["sonka", "sonkas"]),
    ("pulykasonka", ["pulykasonka", "pulykasonkas"]),
    ("csirkemell sonka", ["csirkemell sonka", "csirkemell sonkas"]),
    ("szalámi", ["szalami", "szalámis"]),
    ("kolbász", ["kolbasz", "kolbaszos"]),
    ("gomba", ["gomba", "gombas"]),
    ("uborka", ["uborka", "uborkas"]),
    ("rukkola", ["rukkola"]),
    ("bors", ["bors", "borsos", "zoldborsos"]),
    ("olívaolaj", ["olivaolaj", "olivaolajjal"]),
    ("cheddar", ["cheddar"]),
    ("gouda", ["gouda"]),
    ("ementáli", ["ementali", "emmental"]),
    ("márványsajt", ["marvanysajt", "márványsajt"]),
    ("kék sajt", ["kek sajt", "kekpeneszes"]),
    ("mascarpone", ["mascarpone"]),
    ("ayran", ["ayran"]),
    ("rizs", ["rizs"]),
    ("tea", ["tea", "matcha"]),
]

SIMPLE_FLAVOR_CANONICAL = {
    "vegyes gyumolcsos valogatas": "vegyes gyümölcs",
    "vegyes gyumolcsos": "vegyes gyümölcs",
    "vegyes gyumolcs": "vegyes gyümölcs",
    "erdei gyumolcsos": "erdei gyümölcs",
    "erdei gyumolcs": "erdei gyümölcs",
    "piros gyumolcs": "piros gyümölcs",
    "gyumolcsos": "gyümölcs",
    "gyumolcs": "gyümölcs",
    "slim vanilia": "vanília",
    "bourbon vanilia": "vanília",
    "irish cream": "ír krém",
    "ir krem": "ír krém",
    "provence-i": "zöldfűszer",
    "provence-i zoldfuszeres": "zöldfűszer",
}

CHEESE_KIND_ATOMS = [
    ("mozzarella", ["mozzarella", "fiordilatte mozzarella", "pizza mozzarella", "mozzarella di bufala", "mozzarella snack"]),
    ("trappista", ["trappista"]),
    ("cheddar", ["cheddar"]),
    ("gouda", ["gouda"]),
    ("edami", ["edam", "edami", "edámi"]),
    ("ementáli", ["emental", "emmental", "ementali"]),
    ("maasdam", ["maasdam", "maasdamer"]),
    ("camembert", ["camembert"]),
    ("brie", ["brie"]),
    ("kék sajt", ["kek sajt", "kekpeneszes", "blue cheese"]),
    ("gorgonzola", ["gorgonzola"]),
    ("roquefort", ["roquefort"]),
    ("feta", ["feta"]),
    ("krémfehér sajt", ["kremfeher", "krémfehér"]),
    ("parenyica", ["parenyica"]),
    ("halloumi", ["halloumi"]),
    ("mascarpone", ["mascarpone"]),
    ("ricotta", ["ricotta"]),
    ("burrata", ["burrata"]),
    ("parmezán", ["parmezan", "parmesan", "parmigiano"]),
    ("grana padano", ["grana padano"]),
    ("pecorino", ["pecorino"]),
    ("sajtkeverék", ["sajtkeverek", "sajtok kevereke", "sajtmix", "reszelt sajt keverek"]),
    ("kecskesajt", ["kecskesajt", "kecsketejbol"]),
    ("juhsajt", ["juhsajt", "juhtejes"]),
    ("gomolya", ["gomolya"]),
    ("raclette", ["raclette"]),
    ("scamorza", ["scamorza"]),
    ("leerdammer", ["leerdammer"]),
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


def dedupe(values: list[Any]) -> list[Any]:
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
    text = text.replace("ízü", "ízű").replace("Ízü", "Ízű")
    text = re.sub(r"\s+ízű$", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+ízesítésű$", "", text, flags=re.IGNORECASE)
    return text.strip()


def canonical_prop_name(name: str) -> str | None:
    folded = fold_text(name)
    if folded in NOISY_PROPS:
        return None
    return {
        "marka": "márka",
        "iz": "íz",
        "izesites": "íz",
        "bevonat tipusa": "bevonat",
        "bevonat": "bevonat",
        "forma": "forma",
        "fajta": "fajta",
        "alap": "alap",
        "dusitas": "dúsítás",
        "edesites": "édesítés",
        "allat": "állat",
        "hokezeles": "hőkezelés",
        "kiszereles": "kiszerelés",
        "meret": "méret",
        "tartas": "tartás",
        "zsirtartalom": "zsírtartalom",
        "elo floras/probiotikus": "élőflórás/probiotikus",
        "elofloras/probiotikus": "élőflórás/probiotikus",
        "erlelt": "érlelt",
        "sotott": "sózott",
    }.get(folded, name)


def canonical_brand(value: Any) -> str:
    text = clean_text(value)
    folded = fold_text(text)
    if not folded:
        return text

    exact = {
        "alpro": "Alpro",
        "muller": "Müller",
        "muller riso": "Müller",
        "muller mullermilch": "Müller",
        "minusl": "Minus L",
        "minus l": "Minus L",
        "hulala": "HuLaLá",
        "hu la la": "HuLaLá",
        "venusz+": "Vénusz",
        "actimel": "Danone",
        "actimel+": "Danone",
        "actimel actikids": "Danone",
        "activia": "Danone",
        "oikos": "Danone",
        "yopro": "Danone",
        "danette": "Danone",
        "danonino": "Danone",
        "jogobella": "Zott",
        "zottarella": "Zott",
    }
    if folded in exact:
        return exact[folded]

    prefixes = [
        ("Danone", ["danone"]),
        ("Zott", ["zott"]),
        ("Pöttyös", ["pottyos"]),
        ("Mizo", ["mizo"]),
        ("Müller", ["muller"]),
        ("SPAR", ["spar"]),
        ("Tesco", ["tesco"]),
        ("Pilos", ["pilos"]),
        ("Tihany", ["tihany"]),
        ("Szarvasi", ["szarvasi"]),
        ("Dr. Oetker", ["dr. oetker", "dr oetker"]),
        ("The Bridge", ["the bridge"]),
        ("METRO Chef", ["metro chef"]),
        ("Medve", ["medve"]),
        ("Hajdú", ["hajdu"]),
        ("Vénusz", ["venusz"]),
        ("Magyar Tej", ["magyar tej"]),
        ("Hell", ["hell ice coffee", "hell coffee", "hell"]),
        ("Alpro", ["alpro"]),
    ]
    for canonical, options in prefixes:
        for prefix in options:
            if folded == prefix or folded.startswith(prefix + " ") or folded.startswith(prefix + "-"):
                return canonical
    return text


def atom_matches(folded: str, atoms: list[tuple[str, list[str]]]) -> list[str]:
    matches: list[str] = []
    for canonical, patterns in atoms:
        if any(pattern in folded for pattern in patterns):
            matches.append(canonical)
    return dedupe(matches)


def atomize_flavor(value: Any) -> list[str]:
    text = clean_text(value)
    folded = fold_text(text)
    if not folded:
        return []
    if folded in SIMPLE_FLAVOR_CANONICAL:
        return [SIMPLE_FLAVOR_CANONICAL[folded]]

    matches = atom_matches(folded, FLAVOR_ATOMS)
    if "fehér csokoládé" in matches and "csokoládé" in matches:
        matches.remove("csokoládé")
    if "tejcsokoládé" in matches and "csokoládé" in matches:
        matches.remove("csokoládé")
    if "étcsokoládé" in matches and "csokoládé" in matches:
        matches.remove("csokoládé")
    if "mogyoróvaj" in matches and "mogyoró" in matches:
        matches.remove("mogyoró")
    if "pulykasonka" in matches and "sonka" in matches:
        matches.remove("sonka")
    if "csirkemell sonka" in matches and "sonka" in matches:
        matches.remove("sonka")

    if matches:
        return matches

    return split_generic(text)


def atomize_bevonat(value: Any) -> list[str]:
    folded = fold_text(value)
    if not folded or folded == "egyeb":
        return []
    out: list[str] = []
    if "tejcsokolade" in folded:
        out.append("tejcsokoládé")
    if "tejbevon" in folded or folded in {"tejes", "tejes bevonat"}:
        out.append("tejbevonat")
    if "etbevon" in folded or "etbevono" in folded:
        out.append("étbevonat")
    if "kakao" in folded:
        out.append("kakaó")
    if "csokolade" in folded and not out:
        out.append("csokoládé")
    return dedupe(out)


def normalize_form(value: Any, alkategoria: str) -> list[str]:
    folded = fold_text(value)
    alk_folded = fold_text(alkategoria)
    mapped: list[str] = []

    form_map = [
        ("szeletelt", ["szeletelt", "szeletelt vegan sajt", "szeletelt vegan szendvicsfeltet"]),
        ("reszelt", ["reszelt", "gyalult", "forgacs"]),
        ("tömb", ["tomb", "tömb", "tegla", "tégla"]),
        ("kenhető", ["kenheto", "kenhető", "kenheto krem", "kenhető krém", "kenheto keszitmeny", "vajkrem", "creamy original", "hummus"]),
        ("korong", ["korong", "sajtkorong", "taller", "tallér"]),
        ("lapka", ["lapka", "toast"]),
        ("mini", ["mini"]),
        ("darabolt", ["darab", "darabolt"]),
        ("körcikk", ["korcikk", "körcikk", "gerezd"]),
        ("rúd", ["rud", "rúd", "rudacska", "szalas", "szálas"]),
        ("golyó", ["golyo", "golyó"]),
        ("kocka", ["kocka", "kockazott"]),
        ("fonott", ["fonott"]),
        ("tekercs", ["tekercs"]),
        ("falat", ["falat", "snack"]),
        ("félkör", ["felkor", "félkör"]),
        ("piramis", ["piramis"]),
        ("rögös", ["rogos", "rögös", "rogos turo", "rögös túró"]),
        ("szemcsés", ["szemcses", "szemcsés", "cottage cheese"]),
        ("krémes", ["kremes", "krémes", "kremes turo", "krémes túró"]),
        ("leveles", ["leveles"]),
        ("adagolt", ["adagolt"]),
        ("folyékony", ["folyekony", "folyékony"]),
        ("spray", ["spray"]),
    ]
    for canonical, patterns in form_map:
        if any(pattern in folded for pattern in patterns):
            mapped.append(canonical)

    allowed = FORM_ALLOWED_BY_ALK.get(alk_folded, set())
    return [value for value in dedupe(mapped) if value in allowed]


def atomize_kind(value: Any) -> list[str]:
    text = clean_text(value)
    folded = fold_text(text)
    if not folded or folded == "egyeb":
        return []
    matches = atom_matches(folded, CHEESE_KIND_ATOMS)
    if "kecskesajt" in matches and "juhsajt" in matches and "kecske-juh" in folded:
        return ["kecskesajt", "juhsajt"]
    if matches:
        return matches
    return split_generic(text)


def atomize_base(value: Any) -> list[str]:
    folded = fold_text(value)
    if not folded or folded == "egyeb":
        return []
    out: list[str] = []
    if "szoja" in folded:
        out.append("szója")
    if "zab" in folded:
        out.append("zab")
    if "kokusz" in folded:
        out.append("kókusz")
    if "mandula" in folded:
        out.append("mandula")
    if "rizs" in folded:
        out.append("rizs")
    if "mogyoro" in folded:
        out.append("mogyoró")
    if "csicseriborso" in folded:
        out.append("csicseriborsó")
    if "napraforgo" in folded:
        out.append("napraforgóolaj")
    if "novenyi zsir" in folded or "novenyi zsiradek" in folded:
        out.append("növényi zsír")
    if "novenyi olaj" in folded:
        out.append("növényi olaj")
    if folded in {"novenyi", "novenyi alap"}:
        out.append("növényi")
    return dedupe(out or [clean_text(value)])


def atomize_dusitas(value: Any) -> list[str]:
    folded = fold_text(value)
    if not folded or folded == "egyeb":
        return []
    out: list[str] = []
    options = [
        ("kalcium", ["kalcium"]),
        ("D-vitamin", ["d-vitamin", "d vitamin"]),
        ("D2-vitamin", ["d2-vitamin", "d2 vitamin"]),
        ("B6-vitamin", ["b6-vitamin", "b6 vitamin"]),
        ("B12-vitamin", ["b12-vitamin", "b12 vitamin"]),
        ("C-vitamin", ["c-vitamin", "c vitamin"]),
        ("vitamin", ["vitamin"]),
        ("magnézium", ["magnezium"]),
        ("folsav", ["folsav"]),
        ("jód", ["jod"]),
        ("protein", ["protein", "feherje"]),
        ("omega-3", ["omega-3", "omega 3"]),
    ]
    for canonical, patterns in options:
        if any(pattern in folded for pattern in patterns):
            out.append(canonical)
    if "D2-vitamin" in out and "D-vitamin" in out:
        out.remove("D-vitamin")
    return dedupe(out)


def atomize_edesites(value: Any) -> list[str]:
    folded = fold_text(value)
    if not folded:
        return []
    out: list[str] = []
    if "hozzaadott cukor nelkul" in folded:
        out.append("hozzáadott cukor nélkül")
    if "csokkentett cukor" in folded:
        out.append("csökkentett cukortartalmú")
    if "edesitoszer" in folded:
        out.append("édesítőszer")
    if re.search(r"\bcukor\b", folded) and "cukor nelkul" not in folded:
        out.append("cukor")
    if not out:
        out = split_generic(value)
    return dedupe(out)


def atomize_allat(value: Any) -> list[str]:
    folded = fold_text(value)
    out: list[str] = []
    if "tehen" in folded:
        out.append("tehén")
    if "kecske" in folded:
        out.append("kecske")
    if "juh" in folded:
        out.append("juh")
    if "bivaly" in folded:
        out.append("bivaly")
    return dedupe(out)


def atomize_hokezeles(value: Any) -> list[str]:
    folded = fold_text(value)
    out: list[str] = []
    if "uht" in folded:
        out.append("UHT")
    if "esl" in folded:
        out.append("ESL")
    if "pasztorozott" in folded:
        out.append("pasztőrözött")
    return dedupe(out or [clean_text(value)])


def split_generic(value: Any) -> list[str]:
    text = clean_text(value)
    text = re.sub(r"\s+(?:és|and)\s+", ",", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*[/,&+;]\s*", ",", text)
    parts = [part.strip() for part in text.split(",") if part.strip()]
    out: list[str] = []
    for part in parts or [text]:
        folded = fold_text(part)
        if not folded or folded == "egyeb":
            continue
        out.append(part[:1].lower() + part[1:])
    return dedupe(out)


def normalize_values(prop_name: str, raw_value: Any, product: dict[str, Any]) -> list[Any]:
    alkategoria = product.get("alkategoria", "")
    out: list[Any] = []
    for value in values_of(raw_value):
        if prop_name == "márka":
            out.append(canonical_brand(value))
        elif prop_name == "íz":
            out.extend(atomize_flavor(value))
        elif prop_name == "bevonat":
            out.extend(atomize_bevonat(value))
        elif prop_name == "forma":
            out.extend(normalize_form(value, alkategoria))
        elif prop_name == "fajta":
            out.extend(atomize_kind(value))
        elif prop_name == "alap":
            out.extend(atomize_base(value))
        elif prop_name == "dúsítás":
            out.extend(atomize_dusitas(value))
        elif prop_name == "édesítés":
            out.extend(atomize_edesites(value))
        elif prop_name == "állat":
            out.extend(atomize_allat(value))
        elif prop_name == "hőkezelés":
            out.extend(atomize_hokezeles(value))
        else:
            out.extend(split_generic(value))
    return dedupe(out)


def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    folded = fold_text(value)
    return folded in {"true", "igen", "yes", "1", "bio", "vegan", "vegán", "laktozmentes"}


def kategoriak_hash(fok: str, alk: str, alt: str, props: dict[str, Any]) -> str:
    key = f"{fok}|{alk}|{alt}|{json.dumps(props, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def normalize_product(product: dict[str, Any], audit: dict[str, Any]) -> dict[str, Any]:
    original_props = product.get("tulajdonsagok") or {}
    value_acc: dict[str, list[Any]] = defaultdict(list)
    bool_acc: dict[str, bool] = {}

    for raw_prop_name, raw_value in original_props.items():
        prop_name = canonical_prop_name(raw_prop_name)
        if prop_name is None:
            audit["props_removed"][raw_prop_name] += 1
            continue
        if prop_name != raw_prop_name:
            audit["props_merged"][f"{raw_prop_name} -> {prop_name}"] += 1

        if prop_name in BOOL_PROPS:
            bool_acc[prop_name] = bool_acc.get(prop_name, False) or normalize_bool(raw_value)
            continue

        normalized = normalize_values(prop_name, raw_value, product)
        old_values = values_of(raw_value)
        if normalized != old_values:
            audit["value_changes"][prop_name] += 1
            for old in old_values:
                for new in normalized:
                    if fold_text(old) != fold_text(new):
                        audit["value_change_examples"][prop_name][f"{old} -> {new}"] += 1
                        break
        if not normalized:
            audit["props_removed"][prop_name] += 1
        value_acc[prop_name].extend(normalized)

    # The flavor list is now atomic; keep the boolean aligned where it already exists.
    if "ízesített" in bool_acc and "íz" in value_acc:
        flavor_keys = {fold_text(value) for value in value_acc["íz"]}
        bool_acc["ízesített"] = bool(flavor_keys - {"natur", "natúr"})

    new_props: dict[str, Any] = {}
    for prop_name in sorted(bool_acc, key=fold_text):
        new_props[prop_name] = bool_acc[prop_name]

    for prop_name in sorted(value_acc, key=fold_text):
        values = dedupe(value_acc[prop_name])
        if not values:
            continue
        if prop_name in SCALAR_PROPS:
            new_props[prop_name] = values[0] if len(values) == 1 else values
        else:
            new_props[prop_name] = values

    if new_props != original_props:
        audit["changed_products"] += 1

    product["tulajdonsagok"] = new_props
    product["kategoria_hash"] = kategoriak_hash(
        product.get("fokategoria", ""),
        product.get("alkategoria", ""),
        product.get("altipus", ""),
        new_props,
    )
    return product


def folded_get(mapping: dict[str, Any], folded_name: str, default: Any = None) -> Any:
    target = fold_text(folded_name)
    for key, value in mapping.items():
        if fold_text(key) == target:
            return value
    return default


def build_prop_block(products: list[dict[str, Any]]) -> dict[str, Any]:
    values_by_prop: dict[str, list[Any]] = defaultdict(list)
    bool_props: set[str] = set()
    for product in products:
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            if prop_name in BOOL_PROPS:
                bool_props.add(prop_name)
            else:
                values_by_prop[prop_name].extend(values_of(raw_value))

    block = {"egyedi": {}, "csoportos": {}}
    for prop_name in sorted(bool_props, key=fold_text):
        block["egyedi"][prop_name] = {}
    for prop_name in sorted(values_by_prop, key=fold_text):
        values = sorted(dedupe(values_by_prop[prop_name]), key=fold_text)
        if not values:
            continue
        target = block["egyedi"] if prop_name in EGYEDI_PROPS else block["csoportos"]
        target[prop_name] = values
    return block


def rebuild_tej_category(main_categories: dict[str, Any], products: list[dict[str, Any]]) -> None:
    old_root = main_categories[ROOT_NAME]
    old_alks = folded_get(old_root, "alkategoriak", {}) or {}
    old_order = list(old_alks)

    by_alk: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_path: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for product in products:
        by_alk[product["alkategoria"]].append(product)
        by_path[(product["alkategoria"], product["altipus"])].append(product)

    ordered_alks = [alk for alk in old_order if alk in by_alk]
    ordered_alks.extend(sorted([alk for alk in by_alk if alk not in ordered_alks], key=fold_text))

    new_alks: dict[str, Any] = {}
    for alk in ordered_alks:
        old_alt_order = list((folded_get(old_alks.get(alk, {}), "altipusok", {}) or {}).keys())
        alt_counts = Counter(product["altipus"] for product in by_alk[alk])
        ordered_alts = [alt for alt in old_alt_order if alt in alt_counts]
        ordered_alts.extend([alt for alt, _count in alt_counts.most_common() if alt not in ordered_alts])
        new_alks[alk] = {
            "tulajdonságok": build_prop_block(by_alk[alk]),
            "altípusok": {
                alt: {"tulajdonságok": build_prop_block(by_path[(alk, alt)])}
                for alt in ordered_alts
            },
        }

    main_categories[ROOT_NAME] = {
        "tulajdonságok": build_prop_block(products),
        "alkategóriák": new_alks,
    }


def collect_declared_paths(category_node: dict[str, Any]) -> set[tuple[str, str]]:
    paths: set[tuple[str, str]] = set()
    alks = folded_get(category_node, "alkategoriak", {}) or {}
    for alk, alk_node in alks.items():
        alts = folded_get(alk_node, "altipusok", {}) or {}
        for alt in alts:
            paths.add((alk, alt))
    return paths


def collect_declared_props(category_node: dict[str, Any]) -> set[str]:
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

    walk(category_node)
    return props


def validate(products: list[dict[str, Any]], category_node: dict[str, Any]) -> dict[str, Any]:
    declared_paths = collect_declared_paths(category_node)
    product_paths = Counter((product.get("alkategoria", ""), product.get("altipus", "")) for product in products)
    product_props: set[str] = set()
    prop_values: dict[str, Counter[str]] = defaultdict(Counter)
    forbidden_props = Counter()
    compound_flavors = Counter()
    for product in products:
        for prop_name, raw_value in (product.get("tulajdonsagok") or {}).items():
            product_props.add(prop_name)
            if fold_text(prop_name) in NOISY_PROPS:
                forbidden_props[prop_name] += 1
            for value in values_of(raw_value):
                prop_values[prop_name][str(value)] += 1
                if prop_name == "íz":
                    text = str(value)
                    folded = fold_text(text)
                    if (
                        any(sep in text for sep in ["/", ",", "&", "+"])
                        or ("-" in text and folded not in {"provence-i", "omega-3"})
                        or " es " in folded
                    ):
                        compound_flavors[text] += 1

    declared_props = collect_declared_props(category_node)
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
        "compound_flavors_left": dict(compound_flavors),
        "brand_top": prop_values["márka"].most_common(80),
        "flavor_top": prop_values["íz"].most_common(80),
        "forma_top": prop_values["forma"].most_common(80),
        "bevonat_top": prop_values["bevonat"].most_common(80),
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        safe = [str(cell).replace("\n", " ").replace("|", "\\|") for cell in row]
        lines.append("| " + " | ".join(safe) + " |")
    return lines


def main() -> None:
    generated_at = datetime.now().isoformat(timespec="seconds")
    all_products = load_json(MAIN_PRODUCTS)
    categories = load_json(MAIN_CATEGORIES)

    dairy_indexes = [
        index
        for index, product in enumerate(all_products)
        if fold_text(product.get("fokategoria")) == "tejtermekek es tojas"
    ]
    if not dairy_indexes:
        raise RuntimeError("No dairy products found in main product file")
    if ROOT_NAME not in categories:
        raise RuntimeError(f"{ROOT_NAME!r} not found in category file")

    audit: dict[str, Any] = {
        "meta": {
            "generated_at": generated_at,
            "products_file": MAIN_PRODUCTS.name,
            "categories_file": MAIN_CATEGORIES.name,
            "report_file": REPORT_OUT.name,
        },
        "changed_products": 0,
        "props_removed": Counter(),
        "props_merged": Counter(),
        "value_changes": Counter(),
        "value_change_examples": defaultdict(Counter),
        "brand_changes": Counter(),
    }

    before_brands = Counter()
    after_brands = Counter()
    before_flavors = Counter()
    after_flavors = Counter()
    before_forms = Counter()
    after_forms = Counter()
    before_bevonat = Counter()
    after_bevonat = Counter()

    dairy_products: list[dict[str, Any]] = []
    for index in dairy_indexes:
        product = all_products[index]
        props_before = product.get("tulajdonsagok") or {}
        for value in values_of(props_before.get("márka")):
            before_brands[str(value)] += 1
        for value in values_of(props_before.get("íz")):
            before_flavors[str(value)] += 1
        for value in values_of(props_before.get("forma")):
            before_forms[str(value)] += 1
        for value in values_of(props_before.get("bevonat")):
            before_bevonat[str(value)] += 1

        normalized = normalize_product(product, audit)
        props_after = normalized.get("tulajdonsagok") or {}
        for value in values_of(props_after.get("márka")):
            after_brands[str(value)] += 1
        for value in values_of(props_after.get("íz")):
            after_flavors[str(value)] += 1
        for value in values_of(props_after.get("forma")):
            after_forms[str(value)] += 1
        for value in values_of(props_after.get("bevonat")):
            after_bevonat[str(value)] += 1

        all_products[index] = normalized
        dairy_products.append(normalized)

    for old_brand, count in before_brands.items():
        new_brand = canonical_brand(old_brand)
        if new_brand != old_brand:
            audit["brand_changes"][f"{old_brand} -> {new_brand}"] += count

    rebuild_tej_category(categories, dairy_products)
    validation = validate(dairy_products, categories[ROOT_NAME])

    if validation["missing_paths"]:
        raise RuntimeError(f"Missing category paths: {validation['missing_paths'][:10]}")
    if validation["empty_altipus_products"]:
        raise RuntimeError(f"Empty altipus products: {validation['empty_altipus_products']}")
    if validation["product_only_props"]:
        raise RuntimeError(f"Product-only props: {validation['product_only_props'][:20]}")
    if validation["category_only_props"]:
        raise RuntimeError(f"Category-only props: {validation['category_only_props'][:20]}")
    if validation["forbidden_props_left"]:
        raise RuntimeError(f"Forbidden props left: {validation['forbidden_props_left']}")

    dump_json(MAIN_PRODUCTS, all_products)
    dump_json(MAIN_CATEGORIES, categories)

    audit_json = {
        **audit,
        "props_removed": dict(audit["props_removed"]),
        "props_merged": dict(audit["props_merged"]),
        "value_changes": dict(audit["value_changes"]),
        "value_change_examples": {
            prop: dict(counter.most_common(50))
            for prop, counter in audit["value_change_examples"].items()
        },
        "brand_changes": dict(audit["brand_changes"].most_common()),
        "counts": {
            "dairy_products": len(dairy_products),
            "changed_products": audit["changed_products"],
            "brand_unique_before": len(before_brands),
            "brand_unique_after": len(after_brands),
            "flavor_unique_before": len(before_flavors),
            "flavor_unique_after": len(after_flavors),
            "forma_unique_before": len(before_forms),
            "forma_unique_after": len(after_forms),
            "bevonat_unique_before": len(before_bevonat),
            "bevonat_unique_after": len(after_bevonat),
        },
        "validation": validation,
    }
    dump_json(AUDIT_JSON_OUT, audit_json)

    lines = [
        "# Tejtermékek finomítása",
        "",
        f"- Generálva: {generated_at}",
        f"- Módosított termékfájl: `{MAIN_PRODUCTS.name}`",
        f"- Módosított kategóriafájl: `{MAIN_CATEGORIES.name}`",
        "",
        "## Összesítés",
    ]
    for key, value in audit_json["counts"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "## Validáció",
            f"- Hiányzó kategóriaút: {validation['missing_paths']}",
            f"- Üres altípusú termék: {validation['empty_altipus_products']}",
            f"- Termékben van, kategóriafából hiányzik tulajdonság: {validation['product_only_props']}",
            f"- Kategóriafában van, termékben nincs tulajdonság: {validation['category_only_props']}",
            f"- Tiltott/zajos tulajdonság maradt: {validation['forbidden_props_left']}",
            f"- Összetett ízérték maradt: {validation['compound_flavors_left']}",
            "",
            "## Márka-összevonások",
        ]
    )
    lines.extend(markdown_table(["Márka csere", "Termék"], [[k, v] for k, v in audit_json["brand_changes"].items()]))

    lines.extend(["", "## Tulajdonságérték-változások"])
    lines.extend(markdown_table(["Tulajdonság", "Érintett termék"], [[k, v] for k, v in audit_json["value_changes"].items()]))

    lines.extend(["", "## Bevonat értékek tisztítás után"])
    lines.extend(markdown_table(["Bevonat", "Termék"], validation["bevonat_top"]))

    lines.extend(["", "## Forma értékek tisztítás után"])
    lines.extend(markdown_table(["Forma", "Termék"], validation["forma_top"]))

    lines.extend(["", "## Leggyakoribb ízek tisztítás után"])
    lines.extend(markdown_table(["Íz", "Termék"], validation["flavor_top"][:50]))

    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")

    print(f"dairy_products={len(dairy_products)}")
    print(f"changed_products={audit['changed_products']}")
    print(f"brand_unique={len(before_brands)}->{len(after_brands)}")
    print(f"flavor_unique={len(before_flavors)}->{len(after_flavors)}")
    print(f"forma_unique={len(before_forms)}->{len(after_forms)}")
    print(f"bevonat_unique={len(before_bevonat)}->{len(after_bevonat)}")
    print(f"missing_paths={len(validation['missing_paths'])}")
    print(f"product_only_props={len(validation['product_only_props'])}")
    print(f"category_only_props={len(validation['category_only_props'])}")
    print(f"forbidden_props_left={sum(validation['forbidden_props_left'].values())}")
    print(f"compound_flavors_left={sum(validation['compound_flavors_left'].values())}")
    print(f"report={REPORT_OUT}")


if __name__ == "__main__":
    main()
