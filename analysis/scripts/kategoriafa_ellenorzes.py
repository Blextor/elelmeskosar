"""A GPT-munkapéldány kategóriafájának ellenőrzése. Futtatás: python analysis/scripts/kategoriafa_ellenorzes.py"""

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/categories/kategorizalando_termekek/GPT"
OUTPUT = ROOT / "analysis/reports/kategoriafa_ellenorzes"
LEVELS = ("Főkategória", "Alkategória", "Altípus")


def walk(branch, parent=()):
    for name in sorted(branch, key=str.casefold):
        path = parent + (name,)
        node = branch[name]
        yield path, node
        children = node.get("alkategóriák", {}) if len(path) == 1 else node.get("altípusok", {})
        yield from walk(children, path)


def filled(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(filled(item) for item in value)
    if isinstance(value, dict):
        return any(filled(item) for item in value.values())
    return value is not None


def cell(value):
    return " ".join(str(value).split()).replace("\\", "\\\\").replace("|", "\\|").replace("<", "&lt;")


def section(lines, title, headers, rows):
    lines.extend(["", f"## {title}", ""])
    if not rows:
        lines.append("Nincs találat.")
        return
    lines.extend(["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"])
    for row in rows:
        lines.append("| " + " | ".join(map(cell, row)) + " |")


def path_label(path):
    return " → ".join(path)


def grouped_sections(lines, groups, headers):
    if groups:
        links = [f"[{main} ({len(rows)})](#ag-{index})"
                 for index, (main, rows) in enumerate(groups.items(), 1)]
        lines.extend(["", "A főkategória nevére kattintva a találataihoz ugorhatsz.", "",
                      " · ".join(links)])
    for index, (main, rows) in enumerate(groups.items(), 1):
        lines.extend(["", f'<a id="ag-{index}"></a>'])
        section(lines, f"{main} ({len(rows)} találat)", headers, rows)


def product_label(record):
    product = record["termek"]
    ident = " ".join(str(product.get(key) or "") for key in ("store_name", "store_product_id")).strip()
    return f"{product.get('product_name') or 'Név nélkül'} ({ident})" if ident else product.get("product_name", "")


def make_reports(tree, products, tree_name):
    nodes = dict(walk(tree))
    sibling_counts = Counter(path[:-1] for path in nodes)
    declarations = {}
    effective = {}
    for path, node in nodes.items():
        groups = defaultdict(list)
        for group, properties in node.get("tulajdonságok", {}).items():
            for name in properties:
                groups[name].append(group)
        declarations[path] = groups
        effective[path] = {**effective.get(path[:-1], {}), **dict.fromkeys(groups, path)}

    direct = Counter()
    subtree = Counter()
    absent = Counter()
    empty = Counter()
    missing_example = {}
    first_product = {}
    unmatched = 0
    for record in products:
        parts = [record.get(key) or "" for key in ("fokategoria", "alkategoria", "altipus")]
        while parts and not parts[-1]:
            parts.pop()
        path = tuple(parts)
        for depth in range(1, len(path) + 1):
            prefix = path[:depth]
            subtree[prefix] += 1
            first_product.setdefault(prefix, record)
        if path not in nodes:
            unmatched += 1
            continue
        direct[path] += 1
        values = record.get("tulajdonsagok") or {}
        for name in effective[path]:
            key = (path, name)
            if name not in values:
                absent[key] += 1
            elif not filled(values[name]):
                empty[key] += 1
            else:
                continue
            missing_example.setdefault(key, record)

    source = f"A vizsgálat a GPT mappa `{tree_name}` és `eredmeny.json` fájljait használta. " + (
        f"A fa {len(nodes)} csomópontot tartalmaz. A termékszám {len(products)} mentett bolti termékrekord."
    )
    if unmatched:
        source += (f" A fában {unmatched} rekord teljes útvonala nem található. Ezeket a létező "
                   "felmenők áglétszámába beszámítottuk. A kitöltöttség vizsgálatából kimaradtak.")

    only_children = []
    single_products = []
    empty_nodes = []
    duplicates = defaultdict(list)
    gaps = defaultdict(list)
    affected_paths = set()
    duplicate_pairs = set()
    direct_pairs = set()

    for path in nodes:
        level = LEVELS[len(path) - 1]
        label = path_label(path)
        if len(path) > 1 and sibling_counts[path[:-1]] == 1:
            only_children.append((label, level, subtree[path], direct[path[:-1]]))
        if subtree[path] == 1:
            single_products.append((label, level, product_label(first_product[path])))
        if not subtree[path]:
            empty_nodes.append((label, level, sibling_counts[path]))

        for name in sorted(declarations[path], key=str.casefold):
            for depth in range(len(path) - 1, 0, -1):
                ancestor = path[:depth]
                if name not in declarations[ancestor]:
                    continue
                duplicate_pairs.add((path, name))
                relationship = "Szülő" if depth == len(path) - 1 else "Nagyszülő"
                if relationship == "Szülő":
                    direct_pairs.add((path, name))
                duplicates[path[0]].append((
                    label, name, relationship, path_label(ancestor),
                    " + ".join(declarations[ancestor][name]), " + ".join(declarations[path][name]),
                ))

        if not direct[path]:
            continue
        for name, origin in sorted(effective[path].items(), key=lambda item: item[0].casefold()):
            key = (path, name)
            missing = absent[key] + empty[key]
            if missing:
                affected_paths.add(path)
                gaps[path[0]].append((
                    label, name, LEVELS[len(origin) - 1], direct[path],
                    direct[path] - missing, absent[key], empty[key], product_label(missing_example[key]),
                ))

    lonely = ["# Magányos kategóriák és altípusok", "", source, "",
              f"**{len(only_children)} kategóriának nincs testvére, {len(single_products)} ágban egyetlen termék van.** "
              "Az első lista a fában szereplő testvéreket számolja. A szülőhöz közvetlenül besorolt "
              "termékek külön oszlopban láthatók. A második lista a teljes ág termékszámát vizsgálja. "
              "Egy útvonal mindkét listában szerepelhet."]
    section(lonely, "A szülő egyetlen alkategóriája vagy altípusa",
            ("Útvonal", "Szint", "Termék az ágban", "Közvetlenül a szülőn lévő termék"), only_children)
    section(lonely, "Egyetlen termék az egész ágban", ("Útvonal", "Szint", "Termék"), single_products)

    repeated = ["# Felmenőn megismételt tulajdonságok", "", source, "",
                f"**{len(direct_pairs)} útvonal–tulajdonság pár ismétli a közvetlen szülőt.** "
                f"További {len(duplicate_pairs - direct_pairs)} pár csak a nagyszülőn szerepel korábban. "
                "Az egyezés alapja a pontos tulajdonságnév. A megengedett értékek és a tulajdonság "
                "csoportja eltérhetnek. Ha két felmenő is deklarálja a nevet, mindkét kapcsolat látható."]
    grouped_sections(repeated, duplicates,
                     ("Ismétlő útvonal", "Tulajdonság", "Kapcsolat", "Felmenő útvonala",
                      "Csoport a felmenőn", "Csoport a gyereken"))

    unused = ["# Termék nélküli kategóriák és altípusok", "", source, "",
              f"**{len(empty_nodes)} üres ág.** A vizsgálat minden szinten a közvetlenül besorolt "
              "termékeket és az összes leszármazott termékeit együtt számolja."]
    section(unused, "Üres ágak", ("Útvonal", "Szint", "Közvetlen gyerekkategóriák száma"), empty_nodes)

    coverage = ["# Hiányosan kitöltött tulajdonságok", "", source, "",
                f"**{sum(map(len, gaps.values()))} útvonal–tulajdonság pár, {len(affected_paths)} érintett útvonal.** "
                "Minden termék a saját mentett besorolási szintjén szerepel. Az altípus nélkül besorolt "
                "termékek külön sorokat kapnak az alkategóriájuk alatt. A vizsgálat kiterjed a helyben "
                "deklarált és az örökölt tulajdonságokra is. A deklaráció oszlopa a legközelebbi "
                "deklaráló szintet jelöli.", "",
                "A „Hiányzó kulcs” oszlop a tulajdonság nélküli termékeket számolja. Az „Üres érték” "
                "oszlopba a null, az üres vagy csak szóközökből álló szöveg, illetve a kitöltött elemet "
                "nem tartalmazó gyűjtemény kerül. A false és a 0 kitöltött érték. Minden sorban "
                "a kitöltött, a hiányzó és az üres darabszám összege adja a termékszámot."]
    grouped_sections(coverage, gaps, ("Besorolás", "Tulajdonság", "Deklaráció", "Termék",
                                      "Kitöltött", "Hiányzó kulcs", "Üres érték", "Példatermék"))

    return {"01_maganyos.md": lonely, "02_duplikalt_tulajdonsagok.md": repeated,
            "03_ures_agak.md": unused, "04_hianyos_tulajdonsagok.md": coverage}


def main():
    tree_path = max(DATA.glob("kategoriak_????-??-??.json"))
    tree = json.loads(tree_path.read_text(encoding="utf-8"))
    products = json.loads((DATA / "eredmeny.json").read_text(encoding="utf-8"))
    reports = make_reports(tree, products, tree_path.name)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, lines in reports.items():
        (OUTPUT / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(OUTPUT.relative_to(ROOT) / filename)


if __name__ == "__main__":
    main()
