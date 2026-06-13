import csv
import glob
import os
import re
from datetime import datetime
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

SUTEMENY = "Sütemény, desszert, torta"
KESZETEL = "Készétel"

# --- Elozetes szures: nem elelmiszer, csomag, ertelmetlen sorok ---

# Nem-elelmiszer bolti agak (gyoker- vagy alut-szinten).
NONFOOD_PATH = re.compile(
    r"^elektronika|^otthon, háztartás|^kert, hobbi|^játék, sport|^medence|^kültér|"
    r"^auchan madárka|^grillezés mesterei > grill világ > grillező eszközök|"
    r"^otthon-hobbi|^drogéria|^háztartás( >|\||$)|^kisállat|^állateledel|"
    r"^középső sor|minden, ami nem élelmiszer|"
    r"szépségápolás|egészség, higiénia|pelenkáz|pelenka|cumisüveg|babafelszerelés|"
    r"babaápolás|babaapol|törlőkendő|torlokendo|vitamin, pezsgőtabletta|"
    r"higienia|sampon|tusfurdo|szappan|dezodor|borotv|fogkrem|fogapolas|szajapolas|"
    r"kozmetik|testapol|arcapol|mosogat|mososzer|mosopor|oblito|tisztitoszer|takarito|"
    r"wc-|toalett|haztartas|szemeteszsak|alufolia|folpack|allateledel|macskaeledel|"
    r"kutyaeledel|madareledel|etrend-kiegeszito",
    re.IGNORECASE,
)
# Kivetel: elelmiszer-alagak vegyes (pl. baba) agakon belul.
NONFOOD_PATH_FOOD_OVERRIDE = re.compile(r"bébiétel|bebietel|babaétel|babaetel|bébiital|bebital", re.IGNORECASE)

# Szepseg/egeszseg gyokerag (Roksh, Auchan) - elelmiszer-alag kivetelevel.
NONFOOD_SZEPSEG = re.compile(r"^szépség, egészség|^szepseg-egeszseg", re.IGNORECASE)

# Vegyes ajandekcsomagok, szezonalis csomagok. Az egy-termekes diszdobozos
# italok (pl. whisky diszdobozban) NEM szurendok.
CSOMAG_NAME = re.compile(
    r"ajándékcsomag|ajandekcsomag|ajándék csomag|ajándékkosár|ajandekkosar|ajándék kosár|"
    r"mikulás ?csomag|mikulascsomag|adventi kalendárium|adventi naptár|"
    r"ünnepi csomag|unnepi csomag|karácsonyi csomag|karacsonyi csomag|"
    r"húsvéti csomag|husveti csomag|ajándékszett|ajándék szett|ajandekszett",
    re.IGNORECASE,
)


NONFOOD_NAME = re.compile(r"pelenka|bugyipelenka|pelenkatároló|pelenkatarolo", re.IGNORECASE)


def safe_search(pattern, text):
    # A CPython sre motor ritkan, szorvanyosan "internal error"-t dobhat;
    # egyetlen ilyen hiba ne allitsa meg a teljes futast.
    try:
        return pattern.search(text)
    except RuntimeError:
        try:
            return pattern.search(text)
        except RuntimeError:
            print(f"FIGYELEM: regex hiba, kihagyva: {text[:80]!r}", flush=True)
            return None


def screen_row(product_name, categories, unit_price):
    price_value = None
    try:
        price_value = float(str(unit_price).replace(",", "."))
    except (TypeError, ValueError):
        pass
    if not product_name or price_value is None or price_value <= 0:
        return "ertelmetlen"
    if safe_search(NONFOOD_NAME, product_name):
        return "nem_elelmiszer"
    if safe_search(CSOMAG_NAME, product_name):
        return "csomag"
    if safe_search(NONFOOD_PATH_FOOD_OVERRIDE, categories):
        return ""
    if safe_search(NONFOOD_PATH, categories) or safe_search(NONFOOD_SZEPSEG, categories):
        return "nem_elelmiszer"
    return ""

# Bolti kategoriaut-szabalyok: (bolt, "prefix" vagy "exact" vagy "regex", minta, fo_kategoria)
PATH_RULES = [
    # --- Sutemeny, desszert, torta ---
    ("Metro", "exact", "Élelmiszer > Alapvető termék > Pékáru > Sütemény", SUTEMENY),
    ("Metro", "exact", "Élelmiszer > Édesség és snack > Édes keksz > Sütemény", SUTEMENY),
    ("Auchan", "prefix", "Friss élelmiszer > Pékáruk, kenyerek, cukrászat > Cukrászat", SUTEMENY),
    ("Tesco", "prefix", "Pékáru|Sütemény|", SUTEMENY),
    ("Aldi", "prefix", "Nassolnivalók > Sütemények, desszert", SUTEMENY),
    ("Aldi", "prefix", "Fagyasztott élelmiszer > Pizzák, sütemények > Sütemények", SUTEMENY),
    ("Penny", "prefix", "Nassolnivalók > Sütemények, desszert", SUTEMENY),
    ("Penny", "prefix", "Fagyasztott élelmiszer > Pizzák, sütemények > Sütemények", SUTEMENY),
    ("Spar", "exact", "sutemeny-178", SUTEMENY),
    ("Prima", "exact", "cukrasz-sutemeny-73", SUTEMENY),
    # --- Keszetel ---
    # Barmely bolt: az ut "keszetel" tokent tartalmaz (ekezettel vagy slugban anelkul).
    # A vegso dontest a KESZETEL_NAME_EXCLUDE nevszuro hozza meg, mert a bolti
    # "keszetel" kategoriak sok nem-keszetelt is tartalmaznak.
    ("*", "regex", r"készétel|keszetel", KESZETEL),
]

# Kivetel: ezek az utak hiaba esnek keszetel-szabaly ala, NEM keszetelek.
# A mirelit (fagyasztott/melyhutott) termek definicio szerint nem keszetel.
PATH_EXCLUDES = [
    ("*", "regex", r"fagyasztott|mélyhűtött|melyhutott|mirelit", KESZETEL),
    ("Auchan", "prefix", "Friss élelmiszer > Készételek, hidegkonyha > Friss tészta", KESZETEL),
    # A hushelyettesito "keszetel" sutendo alapanyag, nem kesz foetel.
    ("Aldi", "prefix", "Vegetáriánus & vegán > Húshelyettesítők", KESZETEL),
]

# Keszetel = kesz, legfeljebb mikrozando foetel. Nem keszetel: kence/krem,
# marinalt antipasti, szendvics, salata, nyers/fozendo teszta, instant/bogres
# termek, snack. A "krem" tiltas alol a kremleves kivetel.
KESZETEL_NAME_EXCLUDE = re.compile(
    r"marinált|marinalt|olívabogy|olivabogy|olajbogy|krém(?!leves)|krem(?!leves)|pástétom|pastetom|"
    r"szend|baguette|bagett|panini|wrap|friss tészta|körettészta|korettészta|leveles tészta|"
    r"tésztás készétel|réteslap|reteslap|tortell|ravioli|gnocchi|nokedli|"
    r"sztrapacska|salát|salat|coleslaw|guacamole|kaszinótojás|kaszinotojas|sonkatekercs|"
    r"tapas|humm?usz|antipasti|pizza|instant|bögrés|bogres|popcorn|snack|chips|tortilla lap|"
    r"szárított paradicsom|szaritott paradicsom|levespor|leves por|"
    r"olajban|sajttal tölt|kocsonya|hidegtál|hidegtal|keksz|szardínia|szardinia|jalapeno|"
    r"savanyított|savanyitott|savanyúság|savanyusag|"
    r"nyers|félszáraz|felszaraz|coppa|fuet|chorizo|mariná|marinad|palacsint|linzertészta|"
    r"cappelletti|friss tojás|surimi|tzatziki|helyettesít|no need for meat|vegán szelet|"
    r"tepsimix|\balap\b|magic asia|pirított tészta|piritott teszta|gyorsfagyasztott|party|"
    r"képviselőfánk|kepviselofank|májas|majas|hurka|ömlesztett|omlesztett|száraztészta|"
    r"szarazteszta|tavaszi tekercs|toast",
    re.IGNORECASE,
)

# A kesz levesek keszetelek (2026-06-12 felhasznaloi dontes). A leves-nevu
# termek a nev-kizarasok alol mentesul, ha tenyleg kesz leves (nem por,
# kocka, suritmeny, alapanyag vagy levesteszta).
KESZETEL_LEVES = re.compile(r"leves|halászlé|halaszle", re.IGNORECASE)
KESZETEL_LEVES_NEM_KESZ = re.compile(
    r"por\b|kocka|betét|betet|sűrítmény|suritmeny|\balap\b|szárított|szaritott|instant|"
    r"bögrés|bogres|tészta|teszta|zöldség|zoldseg|keverék|keverek|mix\b|levestál|levestal|gyöngy|gyongy",
    re.IGNORECASE,
)


def keszetel_kesz_leves(product_name):
    return bool(KESZETEL_LEVES.search(product_name) and not KESZETEL_LEVES_NEM_KESZ.search(product_name))


# A kesz hamburger (zsemleben) keszetel, az onmagaban allo huspogacsa nem.
KESZETEL_POGACSA = re.compile(r"pogácsa|pogacsa", re.IGNORECASE)
KESZETEL_ZSEMLE = re.compile(r"zsemlé|zsemle", re.IGNORECASE)

# Konzerv keszetelek alkategoria-jelolese: bolti ut vagy ismert konzervmarka.
KESZETEL_KONZERV_PATH = re.compile(r"konzerv", re.IGNORECASE)
KESZETEL_KONZERV_BRAND = re.compile(
    r"^(házias ízek|hazias izek|globus|kamra|ász |asz |menü |menu |primana|rege )",
    re.IGNORECASE,
)

# Szosz/pesto es rantott/panirozott termek csak akkor keszetel, ha koret is
# tartozik hozza (pl. "rantott sertéskaraj burgonyapürével" igen, a 90 g-os
# pesto vagy az elosutott rantott sajt nem).
KESZETEL_COND_EXCLUDE = re.compile(r"szósz|szosz|pesztó|peszto|pesto|panírozott|panirozott|rántott|rantott", re.IGNORECASE)
KESZETEL_KORET_TOKENS = re.compile(
    r"rizzsel|rizs\b|tésztával|tesztaval|burgonyá|burgonya|pürével|purevel|galuská|galuska|"
    r"knédli|knedli|körettel|köret|koret|bulgur|kuszkusz|zöldbab|zoldbab|brokkoli|csirkemellfilével",
    re.IGNORECASE,
)

# Nev-alapu fallback csak a sutemeny korre, szigoru kizarasokkal.
NAME_INCLUDE = re.compile(
    r"(?<![a-záéíóöőúüű])(torta|tiramisu|bejgli|zserbó|zserbo|isler|ischler|mignon|"
    r"képviselőfánk|kepviselofank|brownie|muffin|pite|rétes|retes|puncs ?szelet|desszertkocka)(?![a-záéíóöőúüű])",
    re.IGNORECASE,
)
NAME_EXCLUDE = re.compile(
    r"ízű|izű|ízesít|aroma|bevonó|bevono|tortalap|tortadara|tortadekor|ostya|forma|papír|papir|"
    r"liszt|réteslap|reteslap|tészta|teszta|alap\b|alappor|krémpor|kremespor|cukor|dekor|"
    r"sütőkeret|gyertya|kiszúró|kiszuro|szilikon|szett|sütemény sütéshez|"
    r"jégkrém|jegkrem|fagylalt|sorbet|szorbé|likőr|likor|keksz|süteménypor|sutemenypor|"
    r"mixer|robotgép|robotgep|társasjáték|tarsasjatek|"
    r"sör\b|étcsokoládé|granola|müzli|muzli|\d\s?ml\b|steak|fillet|marha|"
    r"porkeverék|porkeverek|készítéséhez|keszitesehez|készítmén|keszitmen|"
    r"english muffin|toustis|töltetlen|toltetlen",
    re.IGNORECASE,
)

# Ha a bolti ut egyertelmuen masik fo kategoriat jelez, a nev-szabaly nem fut ra.
NAME_PATH_VETO = re.compile(
    r"dobozos jégkrém|pálcikás|tégelyes|családi jégkrém|jégkrém torta|>\s*jégkrém\s*($|\|)|"
    r"tejalapú ital|tejital|likőr|szeszes ital|táblás csokoládé|keksz, nápolyi|"
    r"töltött és mártott keksz|szeletes termék|cukorka|puding és desszertpor|"
    r"elektronika|játék|háztartási kisgép|konyha felszerelés|"
    r"sütemény ?alap|süteményalap",
    re.IGNORECASE,
)


def repo_root():
    return Path(__file__).resolve().parents[2]


def latest_normalized_files(markets_dir):
    result = {}
    pattern = re.compile(r"(.+)_normalized_data_(\d{8}_\d{6})\.csv$")
    for file_name in glob.glob(str(markets_dir / "*_normalized_data_*.csv")):
        path = Path(file_name)
        match = pattern.match(path.name)
        if not match:
            continue
        store_key = match.group(1)
        current = result.get(store_key)
        if current is None or path.stat().st_mtime > current.stat().st_mtime:
            result[store_key] = path
    return result


def excluded_for_target(store_name, categories, target):
    for rule_store, mode, pattern, rule_target in PATH_EXCLUDES:
        if rule_target != target or rule_store not in ("*", store_name):
            continue
        if mode == "prefix" and pattern in categories:
            return True
        if mode == "regex" and re.search(pattern, categories, re.IGNORECASE):
            return True
    return False


def path_rule_matches(store_name, categories, product_name):
    for rule_store, mode, pattern, target in PATH_RULES:
        if rule_store not in ("*", store_name):
            continue
        matched = False
        if mode == "exact" and categories == pattern:
            matched = True
        elif mode == "prefix" and (categories.startswith(pattern) or f"| {pattern}" in categories or f"|{pattern}" in categories):
            matched = True
        elif mode == "regex" and re.search(pattern, categories, re.IGNORECASE):
            matched = True
        if not matched:
            continue
        if excluded_for_target(store_name, categories, target):
            continue
        if target == KESZETEL and not keszetel_kesz_leves(product_name):
            if KESZETEL_NAME_EXCLUDE.search(product_name):
                continue
            if (
                KESZETEL_COND_EXCLUDE.search(product_name)
                and not KESZETEL_KORET_TOKENS.search(product_name)
            ):
                continue
            if (
                KESZETEL_POGACSA.search(product_name)
                and not KESZETEL_ZSEMLE.search(product_name)
            ):
                continue
        return target
    return None


def keszetel_alkategoria(product_name, categories):
    if KESZETEL_KONZERV_PATH.search(categories) or KESZETEL_KONZERV_BRAND.search(product_name):
        return "Konzerv készételek"
    return ""


def name_rule_matches(product_name, categories):
    if NAME_PATH_VETO.search(categories):
        return None
    if NAME_EXCLUDE.search(product_name):
        return None
    if NAME_INCLUDE.search(product_name):
        return SUTEMENY
    return None


OUTPUT_FIELDS = [
    "store_name",
    "store_product_id",
    "product_name",
    "brand_name",
    "unit_price",
    "unit_type",
    "unit_step",
    "vegso_mennyiseg",
    "vegso_egyseg",
    "ledig",
    "categories",
    "local_image_paths",
    "fo_kategoria",
    "alkategoria",
    "altipus",
    "tulajdonsagok",
    "besorolas_alapja",
    "besorolva",
]


def load_corrections(output_dir):
    corrections = {}
    path = output_dir / "kiszereles_korrekciok.csv"
    if not path.exists():
        return corrections
    with open(path, mode="r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            corrections[(row["store_name"], row["store_product_id"])] = row
    return corrections


def apply_correction(output, corrections):
    # Az eredeti unit_step/unit_type erintetlen marad; a vegso_* oszlopok a
    # korrekciok utani, hasznalando kiszerelest adjak. Ledignel a mennyiseg
    # ures: ott az egysegar (Ft/kg, Ft/l) a hasznalando ertek.
    key = (output["store_name"], output["store_product_id"])
    correction = corrections.get(key)
    if correction is None:
        output["vegso_mennyiseg"] = output["unit_step"]
        output["vegso_egyseg"] = output["unit_type"]
        output["ledig"] = ""
        return
    if correction.get("korrekcio_tipus") == "ledig":
        output["vegso_mennyiseg"] = ""
        output["vegso_egyseg"] = correction.get("javitott_egyseg") or output["unit_type"]
        output["ledig"] = "true"
        return
    output["vegso_mennyiseg"] = correction.get("javitott_mennyiseg") or output["unit_step"]
    output["vegso_egyseg"] = correction.get("javitott_egyseg") or output["unit_type"]
    output["ledig"] = ""


def main():
    markets_dir = repo_root() / "data" / "markets_data"
    output_dir = repo_root() / "data" / "categories"
    output_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")

    normalized = latest_normalized_files(markets_dir)
    if not normalized:
        raise FileNotFoundError(f"Nincs normalized_data fajl itt: {markets_dir}")

    corrections = load_corrections(output_dir)
    categorized = []
    backlog = []
    kiszurt = []
    counts = {}
    screen_counts = {}

    for store_key in sorted(normalized):
        with open(normalized[store_key], mode="r", encoding="utf-8-sig", newline="") as file:
            for row in csv.DictReader(file):
                store_name = (row.get("store_name") or "").strip()
                categories = (row.get("categories") or "").strip()
                product_name = (row.get("product_name") or "").strip()

                screen_reason = screen_row(product_name, categories, row.get("unit_price"))

                target = None
                basis = ""
                if not screen_reason:
                    target = path_rule_matches(store_name, categories, product_name)
                    basis = "bolti_kategoriaut" if target else ""
                if not target:
                    target = name_rule_matches(product_name, categories)
                    basis = "termeknev" if target else ""

                output = {
                    "store_name": store_name,
                    "store_product_id": (row.get("store_product_id") or "").strip(),
                    "product_name": product_name,
                    "brand_name": (row.get("brand_name") or "").strip(),
                    "unit_price": (row.get("unit_price") or "").strip(),
                    "unit_type": (row.get("unit_type") or "").strip(),
                    "unit_step": (row.get("unit_step") or "").strip(),
                    "categories": categories,
                    "local_image_paths": (row.get("local_image_paths") or "").strip(),
                    "fo_kategoria": target or "",
                    "alkategoria": keszetel_alkategoria(product_name, categories) if target == KESZETEL else "",
                    "altipus": "",
                    "tulajdonsagok": "",
                    "besorolas_alapja": basis,
                    "besorolva": today if target else "",
                }
                apply_correction(output, corrections)

                if screen_reason:
                    output["kiszures_oka"] = screen_reason
                    kiszurt.append(output)
                    screen_counts[(store_name, screen_reason)] = screen_counts.get((store_name, screen_reason), 0) + 1
                elif target:
                    categorized.append(output)
                    counts[(store_name, target, basis)] = counts.get((store_name, target, basis), 0) + 1
                else:
                    backlog.append(output)

    categorized_path = output_dir / "kategorizalt_termekek.csv"
    backlog_path = output_dir / "kategorizalatlan_termekek.csv"
    kiszurt_path = output_dir / "kiszurt_termekek.csv"
    for path, rows in [(categorized_path, categorized), (backlog_path, backlog)]:
        with open(path, mode="w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    with open(kiszurt_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS + ["kiszures_oka"])
        writer.writeheader()
        writer.writerows(kiszurt)

    print(f"Kategorizalt termekek: {len(categorized)} -> {categorized_path}")
    print(f"Kategorizalatlan (backlog): {len(backlog)} -> {backlog_path}")
    print(f"Kiszurt termekek: {len(kiszurt)} -> {kiszurt_path}")
    print()
    for (store, target, basis), count in sorted(counts.items()):
        print(f"  {store:8s} | {target:28s} | {basis:18s} | {count}")
    print()
    for (store, reason), count in sorted(screen_counts.items()):
        print(f"  KISZURT {store:8s} | {reason:15s} | {count}")


if __name__ == "__main__":
    main()
