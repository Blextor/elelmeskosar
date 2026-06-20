#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategória-szerkesztő — helyi webes eszköz a termék-kategorizálás tisztításához.

A kategóriafát (kategoriak_*.json) ÉS a termékeket (eredmeny.json) szinkronban
tartva lehet:
  1) teljes node-ot (fő-/al-/altípus) áthelyezni és összeolvasztani egy másikba,
  2) altípust (vagy alkategóriát) feloldani a szülőjébe,
  3) tulajdonságot / tulajdonság-értéket áthelyezni, átnevezni, összevonni node-ok közt,
  4) új tulajdonságot létrehozni egy node-ban.

Minden művelethez van ELŐNÉZET (nem ír semmit). Az ALKALMAZ atomi módon
(temp fájl + os.replace) menti a két JSON-t a helyén, .bak nélkül.

Futtatás:
    python kategoria_szerkeszto.py
majd böngészőben: http://127.0.0.1:8765
"""

import copy
import glob
import http.server
import json
import logging
import os
import socketserver
import sys
import tempfile
import threading
import time
import traceback
import webbrowser
from collections import Counter

PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(HERE, "ksz_ui")
EREDMENY = os.path.join(HERE, "eredmeny.json")
LOG_FILE = os.path.join(HERE, "kategoria_szerkeszto.log")


def _setup_logging():
    """Fájlba ÉS konzolra logol. A fájl (kategoria_szerkeszto.log) megőrzi az okot,
    ha a szerver váratlanul kilép, és hogy az egyes műveletek végbementek-e."""
    log = logging.getLogger("ksz")
    if log.handlers:
        return log
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-7s  %(message)s")
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
    fh.setFormatter(fmt)
    log.addHandler(fh)
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    log.addHandler(sh)
    return log


LOG = _setup_logging()


def _log_uncaught(exc_type, exc_value, exc_tb):
    if issubclass(exc_type, KeyboardInterrupt):
        LOG.info("Megszakítva (KeyboardInterrupt).")
    else:
        LOG.critical("Elkapatlan kivétel — a folyamat kilép:\n%s",
                     "".join(traceback.format_exception(exc_type, exc_value, exc_tb)))


sys.excepthook = _log_uncaught
if hasattr(threading, "excepthook"):
    threading.excepthook = lambda a: LOG.error(
        "Szál-kivétel (%s):\n%s", getattr(a.exc_type, "__name__", a.exc_type),
        "".join(traceback.format_exception(a.exc_type, a.exc_value, a.exc_traceback)))

# A fa-fájl neve dátumozott: a legfrissebb kategoriak_*.json-t használjuk.
def _find_tree_file():
    cands = sorted(glob.glob(os.path.join(HERE, "kategoriak_*.json")))
    if not cands:
        raise SystemExit("Nem találom a kategoriak_*.json fájlt itt: " + HERE)
    return cands[-1]

TREE_FILE = _find_tree_file()

# A három szint kulcsnevei a fában.
CHILD_KEY = {1: "alkategóriák", 2: "altípusok", 3: "altípusok"}
PROP_KEY = "tulajdonságok"
GROUPS = ("egyedi", "csoportos")

# Termék-objektum besorolási mezői (szintsorrendben).
LEVEL_FIELDS = ("fokategoria", "alkategoria", "altipus")


# --------------------------------------------------------------------------- #
#  Betöltés / mentés
# --------------------------------------------------------------------------- #
def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_json_atomic(path, data):
    """Atomi mentés: ideiglenes fájlba írunk, majd os.replace. Nincs .bak."""
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(prefix=".ksz_tmp_", dir=d, suffix=".json")
    t0 = time.time()
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
        LOG.info("mentve: %s (%.2f s)", os.path.basename(path), time.time() - t0)
    except Exception:
        LOG.exception("MENTÉSI HIBA: %s", path)
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


# --------------------------------------------------------------------------- #
#  Fa-bejárás segédek
# --------------------------------------------------------------------------- #
def _ensure_props(node):
    p = node.setdefault(PROP_KEY, {})
    p.setdefault("egyedi", {})
    p.setdefault("csoportos", {})
    return p


def _children_container(node, level, create=False):
    """A node gyerek-konténerét adja vissza (alkategóriák/altípusok)."""
    key = CHILD_KEY[level]
    if create:
        return node.setdefault(key, {})
    return node.get(key, {})


def get_node(tree, path):
    """path: nevek listája (1..3 hosszú). None, ha nincs."""
    if not path:
        return None
    node = tree.get(path[0])
    if node is None:
        return None
    for i, name in enumerate(path[1:], start=1):
        cont = node.get(CHILD_KEY[i], {})
        node = cont.get(name)
        if node is None:
            return None
    return node


def get_parent_container(tree, path, create=False):
    """A konténer, amelyben path utolsó eleme kulcsként szerepel."""
    if len(path) == 1:
        return tree
    parent = get_node(tree, path[:-1])
    if parent is None:
        if not create:
            return None
        # Hozzuk létre a hiányzó szülő-láncot.
        parent = _create_chain(tree, path[:-1])
    return _children_container(parent, len(path) - 1, create=create)


def _create_chain(tree, path):
    """Létrehozza (ha kell) a path által megadott node-láncot, visszaadja az utolsót."""
    node = tree.get(path[0])
    if node is None:
        node = {PROP_KEY: {"egyedi": {}, "csoportos": {}}, CHILD_KEY[1]: {}}
        tree[path[0]] = node
    for i, name in enumerate(path[1:], start=1):
        cont = node.setdefault(CHILD_KEY[i], {})
        child = cont.get(name)
        if child is None:
            child = {PROP_KEY: {"egyedi": {}, "csoportos": {}}}
            cont[name] = child
        node = child
    return node


# --------------------------------------------------------------------------- #
#  Tulajdonság / node összeolvasztás
# --------------------------------------------------------------------------- #
def _union_list(dst_list, src_list):
    """Sorrendtartó unió, 'egyéb' a végén marad."""
    seen = list(dst_list)
    for v in src_list:
        if v not in seen:
            # 'egyéb' elé szúrjuk, ha van
            if "egyéb" in seen and v != "egyéb":
                idx = seen.index("egyéb")
                seen.insert(idx, v)
            else:
                seen.append(v)
    return seen


def merge_prop_value(dst_props, group, name, src_val):
    """Egy tulajdonság-definíciót olvaszt a dst (egyedi/csoportos) szótárba."""
    grp = dst_props.setdefault(group, {})
    if name not in grp:
        grp[name] = copy.deepcopy(src_val)
        return
    cur = grp[name]
    if isinstance(cur, list) and isinstance(src_val, list):
        grp[name] = _union_list(cur, src_val)
    elif isinstance(cur, dict) and isinstance(src_val, dict):
        pass  # flag marad {}
    elif isinstance(cur, dict) and isinstance(src_val, list):
        # típuskeveredés: a flag-et listává léptetjük elő
        grp[name] = _union_list([], src_val)
    # egyébként marad a meglévő


def merge_props(dst_node, src_node):
    dst = _ensure_props(dst_node)
    src = src_node.get(PROP_KEY, {})
    for group in GROUPS:
        for name, val in prop_group(src, group).items():
            merge_prop_value(dst, group, name, val)


def merge_node(dst_node, src_node, level):
    """src_node tartalmát (tulajdonságok + gyerekek) dst_node-ba olvasztja."""
    merge_props(dst_node, src_node)
    child_key = CHILD_KEY[level]
    src_children = src_node.get(child_key, {})
    if src_children:
        dst_children = dst_node.setdefault(child_key, {})
        for cname, cnode in src_children.items():
            if cname in dst_children:
                merge_node(dst_children[cname], cnode, level + 1)
            else:
                dst_children[cname] = copy.deepcopy(cnode)


# --------------------------------------------------------------------------- #
#  Termék-illesztés
# --------------------------------------------------------------------------- #
def product_triple(p):
    return tuple(p.get(f, "") or "" for f in LEVEL_FIELDS)


def matches_prefix(p, path):
    """A termék hármasa illeszkedik-e a path (1..3 hosszú) prefixre."""
    trip = product_triple(p)
    for i, seg in enumerate(path):
        if trip[i] != seg:
            return False
    return True


# --------------------------------------------------------------------------- #
#  Adat összeállítás a UI-nak (fa + termékszámok + tulajdonságok + gondok)
# --------------------------------------------------------------------------- #
def prop_group(container, group):
    """A megadott tulajdonság-csoportot dict-ként adja vissza.

    A fában néhol üres lista (`[]`) szerepel dict helyett – ezt üres dict-ként
    kezeljük, hogy ne dőljön el a `.items()` híváson.
    """
    val = container.get(group, {})
    return val if isinstance(val, dict) else {}


def props_summary(node):
    out = []
    p = node.get(PROP_KEY, {})
    for group in GROUPS:
        for name, val in prop_group(p, group).items():
            if isinstance(val, list):
                out.append({"group": group, "name": name, "kind": "lista", "values": val})
            else:
                out.append({"group": group, "name": name, "kind": "flag", "values": []})
    return out


def build_view(tree, prods):
    counts = Counter(product_triple(p) for p in prods)

    def count_prefix(path):
        n = 0
        for trip, c in counts.items():
            if all(trip[i] == seg for i, seg in enumerate(path)):
                n += c
        return n

    def count_exact(path):
        # pontosan ezen a szinten (mélyebb szintek üresek)
        pad = tuple(path) + ("",) * (3 - len(path))
        return counts.get(pad, 0)

    fk_list = []
    idx = {}  # path-tuple -> view-node (a szintetikus árvák beszúrásához)
    for fk, fn in tree.items():
        fk_node = {
            "name": fk, "level": 1, "path": [fk],
            "count": count_prefix([fk]),
            "props": props_summary(fn),
            "children": [], "orphan": False,
        }
        idx[(fk,)] = fk_node
        for ak, an in fn.get("alkategóriák", {}).items():
            ak_node = {
                "name": ak, "level": 2, "path": [fk, ak],
                "count": count_prefix([fk, ak]),
                "direct": count_exact([fk, ak]),
                "props": props_summary(an),
                "children": [], "orphan": False,
            }
            idx[(fk, ak)] = ak_node
            for at, atn in an.get("altípusok", {}).items():
                at_node = {
                    "name": at, "level": 3, "path": [fk, ak, at],
                    "count": count_exact([fk, ak, at]),
                    "props": props_summary(atn),
                    "children": [], "orphan": False,
                }
                idx[(fk, ak, at)] = at_node
                ak_node["children"].append(at_node)
            fk_node["children"].append(ak_node)
        fk_list.append(fk_node)

    # Árva besorolások: olyan termék-hármasok, amikhez nincs node a fában.
    # Szintetikus, "orphan" jelölésű node-ként beszúrjuk, hogy láthatók és
    # kezelhetők legyenek (különben a szülő összege nem stimmel a látható gyerekekkel).
    def _orphan_node(name, level, path, count, direct=None):
        n = {"name": name, "level": level, "path": list(path), "count": count,
             "props": [], "children": [], "orphan": True}
        if direct is not None:
            n["direct"] = direct
        return n

    for trip in counts:
        fk, ak, at = trip
        if (fk,) not in idx:
            n = _orphan_node(fk, 1, [fk], count_prefix([fk]))
            idx[(fk,)] = n
            fk_list.append(n)
        if ak and (fk, ak) not in idx:
            n = _orphan_node(ak, 2, [fk, ak], count_prefix([fk, ak]), direct=count_exact([fk, ak]))
            idx[(fk, ak)] = n
            idx[(fk,)]["children"].append(n)
        if at and (fk, ak, at) not in idx:
            n = _orphan_node(at, 3, [fk, ak, at], count_exact([fk, ak, at]))
            idx[(fk, ak, at)] = n
            idx[(fk, ak)]["children"].append(n)

    issues = find_issues(tree, prods, counts)
    return {"tree": fk_list, "total_products": len(prods),
            "tree_file": os.path.basename(TREE_FILE),
            "eredmeny_file": os.path.basename(EREDMENY),
            "issues": issues}


def find_issues(tree, prods, counts):
    issues = []
    # 1) alkategória és annak altípusa azonos nevű (Citromlé > Citromlé minta)
    for fk, fn in tree.items():
        for ak, an in fn.get("alkategóriák", {}).items():
            if ak in an.get("altípusok", {}):
                issues.append({
                    "type": "azonos_nev",
                    "text": f"Azonos nevű altípus a szülőjében: {fk} > {ak} > {ak}",
                    "path": [fk, ak, ak],
                })
    # 1b) ugyanaz a tulajdonságnév EGY node-on belül egyszerre egyedi ÉS csoportos
    def _check_dup_groups(path, node):
        p = node.get(PROP_KEY, {})
        eg = p.get("egyedi") if isinstance(p.get("egyedi"), dict) else {}
        cs = p.get("csoportos") if isinstance(p.get("csoportos"), dict) else {}
        for name in sorted(set(eg) & set(cs)):
            issues.append({
                "type": "dupla_tulajdonsag",
                "text": f"Tulajdonság két csoportban: {' > '.join(path)} · {name} (egyedi + csoportos)",
                "path": list(path),
                "prop": name,
            })

    for fk, fn in tree.items():
        _check_dup_groups([fk], fn)
        for ak, an in fn.get("alkategóriák", {}).items():
            _check_dup_groups([fk, ak], an)
            for at, atn in an.get("altípusok", {}).items():
                _check_dup_groups([fk, ak, at], atn)

    # 2) termék-hármas, amihez nincs node a fában (árva besorolás)
    orphan = Counter()
    for trip, c in counts.items():
        fk, ak, at = trip
        node_path = [fk, ak] + ([at] if at else [])
        if get_node(tree, node_path) is None:
            orphan[trip] += c
    for trip, c in sorted(orphan.items(), key=lambda x: -x[1])[:50]:
        issues.append({
            "type": "arva",
            "text": f"Árva besorolás ({c} termék): {' > '.join(x for x in trip if x)}",
            "path": [x for x in trip if x],
        })
    return issues


# --------------------------------------------------------------------------- #
#  MŰVELETEK  (mind deepcopy-n dolgozik, és (tree, prods, summary)-t ad vissza)
# --------------------------------------------------------------------------- #
def op_move_node(tree, prods, source, target):
    """Azonos szintű node áthelyezése + összeolvasztása. source/target azonos hosszú."""
    if len(source) != len(target):
        raise ValueError("A forrás és cél útvonal hossza eltér (azonos szint kell).")
    level = len(source)
    if source == target:
        raise ValueError("A forrás és a cél azonos.")
    src_node = get_node(tree, source)

    # 1) Fa: leválaszt + beilleszt/összeolvaszt. A forrás-node lehet, hogy nincs a
    # fában (csak a termékeken él, árva besorolás) — ekkor üres node-ot mozgatunk.
    if src_node is None:
        detached = {PROP_KEY: {"egyedi": {}, "csoportos": {}}}
    else:
        src_cont = get_parent_container(tree, source)
        detached = src_cont.pop(source[-1])
    tgt_cont = get_parent_container(tree, target, create=True)
    merged = target[-1] in tgt_cont
    if merged:
        merge_node(tgt_cont[target[-1]], detached, level)
    else:
        tgt_cont[target[-1]] = detached

    # 2) Termékek: prefix átírása
    affected = 0
    for p in prods:
        if matches_prefix(p, source):
            for i in range(level):
                p[LEVEL_FIELDS[i]] = target[i]
            affected += 1

    summary = {
        "op": "move_node",
        "affected_products": affected,
        "tree_action": "összeolvasztva a meglévő célba" if merged else "új helyre áthelyezve",
        "source": source, "target": target, "level": level,
    }
    return tree, prods, summary


def op_dissolve(tree, prods, source):
    """Altípus (vagy alkategória) feloldása a szülőbe. source len 2 vagy 3."""
    level = len(source)
    if level not in (2, 3):
        raise ValueError("Feloldani alkategóriát (2) vagy altípust (3) lehet.")
    src_node = get_node(tree, source)
    parent_path = source[:-1]
    parent_node = get_node(tree, parent_path)
    if parent_node is None:
        raise ValueError("A szülő node nem létezik a fában.")

    # 1) Fa: a leszármazottak tulajdonságait a szülőbe olvasztjuk, majd töröljük a
    # node-ot. A forrás lehet árva (nincs a fában) — ekkor csak a termékek változnak.
    if src_node is not None:
        _merge_subtree_props_up(parent_node, src_node, level)
        src_cont = get_parent_container(tree, source)
        src_cont.pop(source[-1], None)

    # 2) Termékek: a source-prefix alatti termékek path-ja a szülő hosszára csonkul
    affected = 0
    for p in prods:
        if matches_prefix(p, source):
            for i in range(level - 1, 3):
                p[LEVEL_FIELDS[i]] = ""
            affected += 1

    summary = {
        "op": "dissolve",
        "affected_products": affected,
        "tree_action": f"feloldva ide: {' > '.join(parent_path)}",
        "source": source, "target": parent_path, "level": level,
    }
    return tree, prods, summary


def _merge_subtree_props_up(parent_node, node, level):
    merge_props(parent_node, node)
    for cname, cnode in node.get(CHILD_KEY[level], {}).items():
        _merge_subtree_props_up(parent_node, cnode, level + 1)


def op_create_property(tree, prods, node_path, group, name, kind, values):
    """Új tulajdonság a node-ban (termékek érintetlenek)."""
    node = get_node(tree, node_path)
    if node is None:
        raise ValueError("A node nem létezik.")
    props = _ensure_props(node)
    grp = props.setdefault(group, {})
    if name in grp:
        raise ValueError("Ilyen nevű tulajdonság már van ezen a node-on.")
    grp[name] = (list(values) if kind == "lista" else {})
    return tree, prods, {
        "op": "create_property", "affected_products": 0,
        "tree_action": f"új '{name}' ({group}/{kind}) tulajdonság itt: {' > '.join(node_path)}",
    }


def op_move_property(tree, prods, source_path, source_prop, target_path,
                     target_prop, group, kind, value=None, new_value=None):
    """
    Tulajdonság / érték áthelyezése, átnevezése, összevonása.
      - value=None  -> az egész tulajdonságot mozgatjuk/nevezzük át (source_prop -> target_prop).
      - value adott -> csak azt az egy értéket visszük át (esetleg new_value-ra átnevezve).
    A source_path és target_path lehet azonos (átnevezés) vagy eltérő node.
    """
    src_node = get_node(tree, source_path)
    if src_node is None:
        raise ValueError("A forrás node nem létezik.")
    tgt_node = get_node(tree, target_path)
    if tgt_node is None:
        raise ValueError("A cél node nem létezik.")

    src_props = _ensure_props(src_node)
    tgt_props = _ensure_props(tgt_node)

    # A forrás-tulajdonság a fán lehet, hogy nincs deklarálva (csak a termékeken
    # él) — ez NEM hiba. A fa-módosítás best-effort, a termék-szintű művelet a fő.
    src_group = None
    src_val = None
    for g in GROUPS:
        if source_prop in src_props.get(g, {}):
            src_group, src_val = g, src_props[g][source_prop]
            break

    # --- 1) Termékek módosítása (és a ténylegesen mozgatott értékek gyűjtése) ---
    affected = 0
    collected = []  # a cél-tulajdonság alá került új értékek (fa-szinkronhoz)
    for p in prods:
        if not matches_prefix(p, source_path):
            continue
        tul = p.get("tulajdonsagok")
        if not isinstance(tul, dict) or source_prop not in tul:
            continue
        changed = False
        if value is None:
            if source_prop != target_prop or source_path != target_path:
                vals = _product_merge_key(tul, source_prop, target_prop, tul[source_prop])
                collected += vals
                changed = True
        else:
            moved = new_value or value
            if _product_move_value(tul, source_prop, target_prop, value, moved):
                collected.append(moved)
                changed = True
        if changed:
            affected += 1

    # --- 2) Fa szintű módosítás (best-effort, a termékekből nyert értékekkel) ---
    # cél-tulajdonság a kért csoportban (ha más csoportban már létezik, oda olvad)
    tgt_existing_group = None
    for g in GROUPS:
        if target_prop in tgt_props.get(g, {}):
            tgt_existing_group = g
            break
    tgt_group = tgt_existing_group or group
    tgt_grp = tgt_props.setdefault(tgt_group, {})

    is_flag = (src_val is not None and not isinstance(src_val, list)) or kind == "flag"
    if value is None and is_flag and src_val is not None and not isinstance(src_val, list):
        tgt_grp.setdefault(target_prop, {})
    else:
        cur = tgt_grp.get(target_prop)
        cur = cur if isinstance(cur, list) else []
        add = list(src_val) if (value is None and isinstance(src_val, list)) else []
        add += collected
        if add or target_prop not in tgt_grp:
            tgt_grp[target_prop] = _union_list(cur, add)

    # forrás-tulajdonság törlése/csonkítása a fán
    if src_group is not None:
        if value is None:
            if not (source_path == target_path and source_prop == target_prop):
                del src_props[src_group][source_prop]
        elif isinstance(src_val, list):
            src_props[src_group][source_prop] = [v for v in src_val if v != value]

    label = (f"'{source_prop}' → '{target_prop}'" if value is None
             else f"'{source_prop}:{value}' → '{target_prop}:{new_value or value}'")
    return tree, prods, {
        "op": "move_property", "affected_products": affected,
        "tree_action": f"{label}  ({' > '.join(source_path)}  ⇒  {' > '.join(target_path)})",
    }


def _product_merge_key(tul, src_key, dst_key, src_val):
    """Termékben a src_key értékét a dst_key alá olvasztja, src_key-t törli.
    Visszaadja a (lista)értékeket, amik a célkulcs alá kerültek (fa-szinkronhoz)."""
    if dst_key not in tul:
        tul[dst_key] = src_val
    else:
        dv = tul[dst_key]
        if isinstance(dv, list) or isinstance(src_val, list):
            dl = dv if isinstance(dv, list) else ([dv] if dv not in (None, "", False) else [])
            sl = src_val if isinstance(src_val, list) else ([src_val] if src_val not in (None, "", False) else [])
            tul[dst_key] = _union_list(dl, sl)
        elif isinstance(dv, bool) or isinstance(src_val, bool):
            tul[dst_key] = bool(dv) or bool(src_val)
        else:
            tul[dst_key] = dv or src_val
    if src_key in tul and src_key != dst_key:
        del tul[src_key]
    v = tul.get(dst_key)
    if isinstance(v, list):
        return list(v)
    if isinstance(v, str) and v:
        return [v]
    return []


def _product_move_value(tul, src_key, dst_key, value, moved):
    """Egy konkrét értéket mozgat a termék src_key-jéből a dst_key alá."""
    pv = tul.get(src_key)
    found = False
    if isinstance(pv, list):
        if value in pv:
            tul[src_key] = [v for v in pv if v != value]
            found = True
    elif isinstance(pv, str):
        if pv == value:
            tul[src_key] = ""
            found = True
    if not found:
        return False
    dv = tul.get(dst_key)
    if isinstance(dv, list):
        if moved not in dv:
            dv.append(moved)
    elif dv in (None, "", False):
        tul[dst_key] = [moved]
    else:
        tul[dst_key] = _union_list([dv], [moved])
    return True


# --------------------------------------------------------------------------- #
#  Effektív tulajdonságok (fa-deklarált + termékeken ténylegesen előforduló)
# --------------------------------------------------------------------------- #
def _infer_kind(val):
    return "flag" if isinstance(val, bool) else "lista"


def canon_value(v):
    """Egy tulajdonság-érték STABIL string-kulcsa.

    A kategorizálás néha hibás (nem-string) értéket termel — pl. egy márkanév
    helyére egy objektum (dict) kerül. Az ilyen értékeket nem lehet közvetlenül
    kulcsként/halmazban használni (`unhashable type: 'dict'`), ezért determinisztikus
    JSON-stringgé alakítjuk. A sima stringek változatlanul maradnak, így a UI és a
    fa/termék oldali illesztés ugyanazt a kulcsot látja.
    """
    if isinstance(v, str):
        return v
    return json.dumps(v, ensure_ascii=False, sort_keys=True)


def get_effective_props(tree, prods, path):
    """A node ÖRÖKÖLT effektív tulajdonságai a térkép-UI-hoz: a felmenők + a saját
    fa-deklarált tulajdonságai (érték-listák UNIÓJA, nem felülírás!) ÉS a termékeken
    ténylegesen előfordulók. Visszaad listát:
    {name, group, kind, values, where, product_count, declared[], self_declared,
     inherited, origin}.

    Megjegyzés: a kat25.py get_tulajdonsagok() dict.update()-tel FELÜLÍR (a gyermek
    márka-listája kicseréli a szülőét) — ez itt szándékosan UNIÓ, hogy a felmenők
    értékei (pl. a Citromlé alkategória márkái) is látszódjanak/kezelhetők legyenek.
    """
    res = {}

    def add_tree(name, val, group, level_path, is_self):
        kind = "lista" if isinstance(val, list) else "flag"
        vals = [canon_value(x) for x in val] if isinstance(val, list) else []
        e = res.get(name)
        if e is None:
            res[name] = {"name": name, "group": group, "kind": kind, "values": vals,
                         "where": "fa", "product_count": 0,
                         "declared": [list(level_path)], "self_declared": is_self,
                         "self_groups": [group] if is_self else []}
        else:
            e["values"] = _union_list(e["values"], vals)
            e["declared"].append(list(level_path))
            if is_self:
                e["self_declared"] = True
                if group not in e["self_groups"]:
                    e["self_groups"].append(group)
            if e["kind"] == "flag" and kind == "lista":
                e["kind"] = "lista"

    # felmenők + saját, sekélytől mélyig (öröklés)
    for depth in range(1, len(path) + 1):
        sub = path[:depth]
        node = get_node(tree, sub)
        if node is None:
            continue
        is_self = (depth == len(path))
        for group in GROUPS:
            for name, val in prop_group(node.get(PROP_KEY, {}), group).items():
                add_tree(name, val, group, sub, is_self)

    # termékeken ténylegesen előforduló tulajdonságok
    for p in prods:
        if not matches_prefix(p, path):
            continue
        tul = p.get("tulajdonsagok")
        if not isinstance(tul, dict):
            continue
        for name, val in tul.items():
            e = res.get(name)
            if e is None:
                e = res[name] = {"name": name, "group": "csoportos",
                                 "kind": _infer_kind(val), "values": [],
                                 "where": "termék", "product_count": 0,
                                 "declared": [], "self_declared": False,
                                 "self_groups": []}
            elif e["where"] == "fa":
                e["where"] = "mindkettő"
            e["product_count"] += 1
            if isinstance(val, list):
                for v in val:
                    cv = canon_value(v)
                    if cv != "" and cv not in e["values"]:
                        e["values"].append(cv)
            elif isinstance(val, str):
                if val and val not in e["values"]:
                    e["values"].append(val)
            elif not isinstance(val, bool):
                cv = canon_value(val)  # hibás skalár érték (pl. dict) is kezelhető legyen
                if cv not in e["values"]:
                    e["values"].append(cv)

    # eredet-címke: honnan deklarált / honnan örökölt
    self_depth = len(path)
    for e in res.values():
        # csak a felmenőkön (a node-nál sekélyebb szinten) deklarált forrás-útvonalak
        inh_paths = [d for d in e["declared"] if len(d) < self_depth]
        inh_labels = [" › ".join(d) for d in inh_paths]
        e["inherited_from"] = inh_labels
        if e["self_declared"]:
            e["origin"] = "saját"
            if inh_labels:
                e["origin"] += " + örökölt: " + " ; ".join(inh_labels)
        elif inh_labels:
            e["origin"] = "örökölt: " + " ; ".join(inh_labels)
        elif e["declared"]:
            e["origin"] = "örökölt: " + " › ".join(e["declared"][-1])
        else:
            e["origin"] = "termék"
        e["inherited"] = bool(e["declared"]) and not e["self_declared"]

    # sorrend: saját fa-propok, majd örököltek, majd csak termék — néven belül ABC
    def rank(e):
        return 0 if e["self_declared"] else (1 if e["declared"] else 2)
    return sorted(res.values(), key=lambda e: (rank(e), e["name"].lower()))


def _merge_vals(a, b):
    """Két termék-tulajdonságérték összeolvasztása (list/bool/str)."""
    if isinstance(a, list) or isinstance(b, list):
        al = a if isinstance(a, list) else ([a] if a not in (None, "", False) else [])
        bl = b if isinstance(b, list) else ([b] if b not in (None, "", False) else [])
        return _union_list(al, bl)
    if isinstance(a, bool) or isinstance(b, bool):
        return bool(a) or bool(b)
    return a if a not in (None, "", False) else b


def op_merge_mapping(tree, prods, source, target, mappings):
    """Forrás node + termékei beolvadnak a célba, tulajdonság-térkép szerint.
    mappings: [{src, dst}]. Be nem kötött forrás-tulajdonság törlődik; a célé marad.
    A forrás és a cél lehet ELTÉRŐ szintű is: a termékek a cél szintjére kerülnek
    (a célnál mélyebb szintek kiürülnek, a forrásnál mélyebbek megmaradnak)."""
    if source == target:
        raise ValueError("A forrás és a cél azonos.")
    ls, lt = len(source), len(target)
    level = ls

    map_dict = {m["src"]: m["dst"] for m in mappings if m.get("dst")}
    eff = get_effective_props(tree, prods, source)
    src_names = {e["name"] for e in eff}
    kind_by = {e["name"]: e["kind"] for e in eff}
    group_by = {e["name"]: e["group"] for e in eff}

    # cél node (létrehozzuk, ha nincs)
    tgt_node = get_node(tree, target)
    if tgt_node is None:
        tgt_cont = get_parent_container(tree, target, create=True)
        tgt_node = tgt_cont.setdefault(target[-1], {PROP_KEY: {"egyedi": {}, "csoportos": {}}})
    tgt_props = _ensure_props(tgt_node)

    # forrás fa-tulajdonság értékei (a cél-listák feltöltéséhez)
    src_node = get_node(tree, source)
    src_tree_vals = {}
    if src_node is not None:
        for g in GROUPS:
            for nm, val in prop_group(src_node.get(PROP_KEY, {}), g).items():
                if isinstance(val, list):
                    src_tree_vals[nm] = list(val)

    # --- 1) Termékek: tulajdonság-térkép + áthelyezés a célba ---
    affected = 0
    deleted_keys = set()
    collected = {}  # dst-prop -> a célkulcs alá került értékek (fa-szinkron)
    for p in prods:
        if not matches_prefix(p, source):
            continue
        tul = p.get("tulajdonsagok")
        if isinstance(tul, dict):
            new_tul = {}
            for k, v in tul.items():
                if k in map_dict:
                    dst = map_dict[k]
                    new_tul[dst] = _merge_vals(new_tul.get(dst), v) if dst in new_tul else v
                elif k in src_names:
                    deleted_keys.add(k)  # be nem kötött forrás -> törlés
                else:
                    new_tul[k] = _merge_vals(new_tul.get(k), v) if k in new_tul else v
            for dst, val in new_tul.items():
                if isinstance(val, list):
                    collected.setdefault(dst, [])
                    for x in val:
                        if x not in collected[dst]:
                            collected[dst].append(x)
                elif isinstance(val, str) and val:
                    collected.setdefault(dst, [])
                    if val not in collected[dst]:
                        collected[dst].append(val)
            p["tulajdonsagok"] = new_tul
        # átsorolás: a cél szintjéig a cél értékei; a forrásnál mélyebb szintek
        # megmaradnak; a [cél, forrás) közti (csak a forrásnál létező) szintek kiürülnek
        for i in range(3):
            if i < lt:
                p[LEVEL_FIELDS[i]] = target[i]
            elif i < ls:
                p[LEVEL_FIELDS[i]] = ""
        affected += 1

    # --- 2) Fa: a bekötött forrás-tulajdonságok a célba (union), forrás eltávolítása ---
    for src_name, dst_name in map_dict.items():
        existing_group = None
        for g in GROUPS:
            if dst_name in tgt_props.get(g, {}):
                existing_group = g
                break
        group = existing_group or group_by.get(src_name, "csoportos")
        grp = tgt_props.setdefault(group, {})
        if kind_by.get(src_name) == "flag" and dst_name not in grp:
            grp.setdefault(dst_name, {})
        else:
            cur = grp.get(dst_name)
            cur = cur if isinstance(cur, list) else ([] if not isinstance(cur, dict) else None)
            if cur is None:  # cél flag maradjon flag
                continue
            add = list(src_tree_vals.get(src_name, [])) + list(collected.get(dst_name, []))
            grp[dst_name] = _union_list(cur, add)

    # forrás node leválasztása (ha a fában volt). Azonos szintnél a forrás
    # gyerekei a célba olvadnak; eltérő szintnél a gyerekek (a termékek már
    # átsorolva) a leválasztással együtt megszűnnek.
    if src_node is not None:
        src_cont = get_parent_container(tree, source)
        detached = src_cont.pop(source[-1], None)
        if detached is not None and ls == lt:
            child_key = CHILD_KEY[ls]
            src_children = detached.get(child_key, {})
            if src_children:
                dst_children = tgt_node.setdefault(child_key, {})
                for cname, cnode in src_children.items():
                    if cname in dst_children:
                        merge_node(dst_children[cname], cnode, ls + 1)
                    else:
                        dst_children[cname] = cnode

    summary = {
        "op": "merge_mapping", "affected_products": affected,
        "source": source, "target": target, "level": level,
        "tree_action": f"beolvasztva ide: {' > '.join(target)}"
                       + ("" if ls == lt else f"  (eltérő szint: {ls} → {lt})"),
        "mapped": [{"src": s, "dst": d} for s, d in map_dict.items()],
        "deleted": sorted(deleted_keys),
    }
    return tree, prods, summary


def op_edit_prop_values(tree, prods, node_path, prop, group, value_map):
    """Egy tulajdonság ÉRTÉKEINEK szerkesztése EGYETLEN node-on belül:
    átnevezés, másik értékbe összevonás, vagy törlés.

    value_map: {régi_érték: új_érték}.  új_érték == ""  => az érték törlése.
    A térképben nem szereplő értékek változatlanok. Ha az új_érték már létezik
    a listában, az érték abba olvad (duplikátum-mentes unió, sorrendtartó).

    A node lehet árva (csak a termékeken él) — ekkor a fa érintetlen, csak a
    termékek módosulnak (best-effort, mint a többi műveletnél).
    """
    if not value_map:
        raise ValueError("Nincs megadva érték-változtatás.")

    def remap_list(values):
        """Lista átképezése a value_map szerint. A nem érintett értékek (akár dict
        is) változatlanul maradnak; az illesztés a kanonikus string-kulcson megy."""
        out, seen = [], []
        for v in values:
            cv = canon_value(v)
            if cv in value_map:
                nv = value_map[cv]
                if nv == "":
                    continue  # törlés
            else:
                nv = v        # változatlan (lehet hibás dict-érték is)
            cnv = canon_value(nv)
            if cnv not in seen:
                seen.append(cnv)
                out.append(nv)
        return out

    # --- 1) Termékek ---
    affected = 0
    for p in prods:
        if not matches_prefix(p, node_path):
            continue
        tul = p.get("tulajdonsagok")
        if not isinstance(tul, dict) or prop not in tul:
            continue
        pv = tul[prop]
        if isinstance(pv, list):
            new = remap_list(pv)
            if new != pv:
                tul[prop] = new
                affected += 1
        else:
            cv = canon_value(pv)  # string vagy hibás skalár (dict/objektum)
            if cv in value_map and value_map[cv] != cv:
                tul[prop] = value_map[cv]  # "" törlésnél üres string marad
                affected += 1

    # --- 2) Fa: a node SAJÁT deklarált listáját igazítjuk (best-effort) ---
    node = get_node(tree, node_path)
    tree_changed = False
    if node is not None:
        props = node.get(PROP_KEY, {})
        for g in GROUPS:
            grp = props.get(g)
            if isinstance(grp, dict) and isinstance(grp.get(prop), list):
                new = remap_list(grp[prop])
                if new != grp[prop]:
                    grp[prop] = new
                    tree_changed = True

    renamed = sorted(f"{k} → {v}" for k, v in value_map.items() if v != "")
    deleted = sorted(k for k, v in value_map.items() if v == "")
    parts = []
    if renamed:
        parts.append(f"átnevezés/összevonás: {', '.join(renamed)}")
    if deleted:
        parts.append(f"törölve: {', '.join(deleted)}")
    return tree, prods, {
        "op": "edit_values", "affected_products": affected,
        "tree_action": (f"'{prop}' ({' > '.join(node_path)})"
                        + (" — fa frissítve" if tree_changed else " — fa nem deklarálja itt")),
        "value_detail": "; ".join(parts) if parts else "(nincs változás)",
        "renamed": renamed, "deleted": deleted,
    }


def op_merge_values(tree, prods, node_path, moves, delete_props=None):
    """Érték-szintű, tulajdonságok KÖZÖTTI összevonás/törlés (kötögetős UI).

    moves: [{src_prop, src_val, dst_prop, dst_val}].  Ha dst_prop üres → TÖRLÉS.
    delete_props: teljes tulajdonságok törlése (a fáról ÉS a termékekről).
    A forrás értéket a termékeken (és a fa-listán) eltávolítjuk; ha van cél, a cél
    tulajdonság cél értékét hozzáadjuk. Pl. 'típus:alkoholmentes cider' →
    'alkoholtartalom:0,0%'. Az illesztés a kanonikus érték-kulcson megy, így hibás
    (dict) értékek is mozgathatók/törölhetők."""
    delete_props = [d for d in (delete_props or []) if d]
    norm = []
    for m in moves:
        sp, sv = m.get("src_prop"), m.get("src_val")
        if not sp or sv is None:
            continue
        norm.append((sp, sv, m.get("dst_prop") or "", m.get("dst_val")))
    if not norm and not delete_props:
        raise ValueError("Nincs művelet — köss össze egy értéket, vagy jelölj törlendő tulajdonságot.")

    def remove_val(tul, prop, cval):
        pv = tul.get(prop)
        if isinstance(pv, list):
            new = [x for x in pv if canon_value(x) != cval]
            if len(new) != len(pv):
                tul[prop] = new
                return True
            return False
        if pv not in (None, "", False) and canon_value(pv) == cval:
            tul[prop] = ""
            return True
        return False

    def add_val(tul, prop, val):
        pv = tul.get(prop)
        cv = canon_value(val)
        if isinstance(pv, list):
            if all(canon_value(x) != cv for x in pv):
                pv.append(val)
        elif pv in (None, "", False):
            tul[prop] = [val]
        elif canon_value(pv) != cv:
            tul[prop] = _union_list([pv], [val])

    # --- 1) Termékek ---
    affected = 0
    for p in prods:
        if not matches_prefix(p, node_path):
            continue
        tul = p.get("tulajdonsagok")
        if not isinstance(tul, dict):
            continue
        changed = False
        for sp, sv, dp, dv in norm:
            if remove_val(tul, sp, sv):
                changed = True
                if dp:
                    add_val(tul, dp, dv)
        for dprop in delete_props:
            if dprop in tul:
                del tul[dprop]
                changed = True
        if changed:
            affected += 1

    # --- 2) Fa (best-effort, a node SAJÁT deklarált listáin) ---
    node = get_node(tree, node_path)
    if node is not None:
        props = node.get(PROP_KEY, {})
        for sp, sv, dp, dv in norm:
            for g in GROUPS:
                grp = props.get(g)
                if isinstance(grp, dict) and isinstance(grp.get(sp), list):
                    grp[sp] = [x for x in grp[sp] if canon_value(x) != sv]
            if dp:
                dgroup = next((g for g in GROUPS
                               if isinstance(props.get(g), dict) and dp in props[g]), None) or "csoportos"
                dgrp = props.setdefault(dgroup, {})
                cur = dgrp.get(dp)
                if not isinstance(cur, dict):  # flag-et ne bántsuk
                    dgrp[dp] = _union_list(cur if isinstance(cur, list) else [], [dv])
        for dprop in delete_props:
            for g in GROUPS:
                grp = props.get(g)
                if isinstance(grp, dict) and dprop in grp:
                    del grp[dprop]

    moved = [f"{sp}:{sv}  →  {dp + ':' + str(dv) if dp else '(törlés)'}" for sp, sv, dp, dv in norm]
    return tree, prods, {
        "op": "merge_values", "affected_products": affected,
        "tree_action": f"{len(norm)} érték-művelet, {len(delete_props)} törölt tulajdonság  ({' > '.join(node_path)})",
        "value_moves": moved,
        "deleted_props": list(delete_props),
    }


def get_node_group_props(tree, path):
    """A node SAJÁT (fa-deklarált) tulajdonságai csoport-bontásban, a „kötögetős"
    egyesítő UI-hoz. Minden bejegyzés egyedi kulcsa: '<csoport>|<név>'."""
    out = []
    node = get_node(tree, path)
    if node is None:
        return out
    props = node.get(PROP_KEY, {})
    for g in GROUPS:
        grp = props.get(g)
        if not isinstance(grp, dict):
            continue
        for name, val in grp.items():
            is_list = isinstance(val, list)
            out.append({
                "key": g + "|" + name, "group": g, "name": name,
                "kind": "lista" if is_list else "flag",
                "values": [canon_value(x) for x in val] if is_list else [],
                "count": len(val) if is_list else 0,
            })
    return out


def op_consolidate_prop_groups(tree, prods, node_path, mappings):
    """Egy node tulajdonságainak EGYMÁSBA olvasztása (kötögetős UI).

    mappings: [{"src": "<csoport>|<név>", "dst": "<csoport>|<név>"}].
    A FORRÁS tulajdonság a fában a CÉLBA olvad (érték-listák UNIÓJA), majd törlődik.
    Ha a forrás és a cél NEVE eltér, a termékeken is átkulcsozzuk (tul[forrásnév] a
    tul[célnév] alá). Ha a NÉV azonos (csak a csoport tér el — a tipikus
    egyedi/csoportos besorolási hiba), a termékek NEM változnak: a csoport csak a
    fában létezik, a termékeken névenként egyetlen érték van."""
    node = get_node(tree, node_path)
    if node is None:
        raise ValueError("A node nem létezik a fában.")
    props = _ensure_props(node)

    def parse(k):
        g, _, n = (k or "").partition("|")
        return g, n

    pairs = []
    for m in mappings:
        s, d = m.get("src"), m.get("dst")
        if s and d and s != d:
            pairs.append((parse(s), parse(d)))
    if not pairs:
        raise ValueError("Nincs összekötés — húzz legalább egy forrást egy célba.")

    # 1) Fa: forrás értékek a célba (union), forrás törlése
    name_remap = {}   # eltérő nevű összevonás → termék-szinkronhoz
    done = []
    for (gs, ns), (gd, nd) in pairs:
        sgrp = props.get(gs)
        if not isinstance(sgrp, dict) or ns not in sgrp:
            continue  # már feldolgozva / nincs a fában
        sval = sgrp[ns]
        dgrp = props.setdefault(gd, {})
        if isinstance(sval, list):
            cur = dgrp.get(nd)
            cur = cur if isinstance(cur, list) else []
            dgrp[nd] = _union_list(cur, sval)
        else:
            dgrp.setdefault(nd, {})  # flag marad flag
        del sgrp[ns]
        done.append({"src": f"{gs}|{ns}", "dst": f"{gd}|{nd}"})
        if ns != nd:
            name_remap[ns] = nd

    # 2) Termékek: csak ha a NÉV változik (a csoport a termékeken nem létezik)
    affected = 0
    if name_remap:
        for p in prods:
            if not matches_prefix(p, node_path):
                continue
            tul = p.get("tulajdonsagok")
            if not isinstance(tul, dict):
                continue
            changed = False
            for ns, nd in name_remap.items():
                if ns in tul:
                    _product_merge_key(tul, ns, nd, tul[ns])
                    changed = True
            if changed:
                affected += 1

    note = ("A termékek nem változtak: az 'egyedi'/'csoportos' csak a fában létező "
            "besorolás — a termékeken névenként egyetlen érték van."
            if affected == 0 else "")
    return tree, prods, {
        "op": "consolidate_groups", "affected_products": affected,
        "tree_action": f"{len(done)} tulajdonság egyesítve  ({' > '.join(node_path)})",
        "mapped": done,
        "note": note,
    }


OPS = {
    "move_node": lambda t, p, b: op_move_node(t, p, b["source"], b["target"]),
    "dissolve": lambda t, p, b: op_dissolve(t, p, b["source"]),
    "create_property": lambda t, p, b: op_create_property(
        t, p, b["node"], b["group"], b["name"], b["kind"], b.get("values", [])),
    "move_property": lambda t, p, b: op_move_property(
        t, p, b["source"], b["source_prop"], b["target"], b["target_prop"],
        b["group"], b.get("kind", "lista"), b.get("value"), b.get("new_value")),
    "merge_mapping": lambda t, p, b: op_merge_mapping(
        t, p, b["source"], b["target"], b.get("mappings", [])),
    "edit_values": lambda t, p, b: op_edit_prop_values(
        t, p, b["node"], b["prop"], b.get("group", "csoportos"), b.get("value_map", {})),
    "merge_values": lambda t, p, b: op_merge_values(
        t, p, b["node"], b.get("moves", []), b.get("delete_props", [])),
    "consolidate_groups": lambda t, p, b: op_consolidate_prop_groups(
        t, p, b["node"], b.get("mappings", [])),
}


# Az ÍRÓ műveleteket sorosítjuk: két egyidejű „Alkalmaz" ne versenyezzen ugyanazon
# a két (nagy) fájlon — ez okozhatott korábban beragadást/inkonzisztenciát.
_WRITE_LOCK = threading.Lock()


def _run_operation_inner(body, op, mode, t0, write):
    if op not in OPS:
        raise ValueError(f"Ismeretlen művelet: {op}")
    tree = load_json(TREE_FILE)
    prods = load_json(EREDMENY)
    LOG.debug("%s: fájlok betöltve (%.2f s), művelet számítása…", mode, time.time() - t0)
    work_tree = copy.deepcopy(tree)
    work_prods = copy.deepcopy(prods)
    new_tree, new_prods, summary = OPS[op](work_tree, work_prods, body)
    LOG.debug("%s: művelet kész (%.2f s), %s…", mode, time.time() - t0,
              "mentés" if write else "előnézet építése")
    if write:
        save_json_atomic(TREE_FILE, new_tree)
        save_json_atomic(EREDMENY, new_prods)
        summary["written"] = True
    else:
        summary["written"] = False
        summary["view"] = build_view(new_tree, new_prods)
    LOG.info("%s kész: op=%s  érintett termék=%s  fa=%s  (%.2f s)",
             mode, op, summary.get("affected_products"),
             summary.get("tree_action", ""), time.time() - t0)
    return summary


def run_operation(body, write):
    op = body.get("op")
    mode = "ALKALMAZ" if write else "előnézet"
    LOG.info("%s indul: op=%s  node/source=%s", mode, op, body.get("node") or body.get("source"))
    t0 = time.time()
    if write:
        # Ha másik írás van folyamatban, megvárjuk (és naplózzuk, ha kell várni).
        if not _WRITE_LOCK.acquire(blocking=False):
            LOG.info("%s: várakozás a másik írás befejezésére…", mode)
            _WRITE_LOCK.acquire()
        try:
            return _run_operation_inner(body, op, mode, t0, write)
        finally:
            _WRITE_LOCK.release()
    return _run_operation_inner(body, op, mode, t0, write)


# --------------------------------------------------------------------------- #
#  HTTP
# --------------------------------------------------------------------------- #
class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, data, ctype="application/json; charset=utf-8"):
        body = data if isinstance(data, bytes) else json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass  # csendes

    def do_GET(self):
        try:
            if self.path in ("/", "/index.html"):
                return self._serve_static("index.html", "text/html; charset=utf-8")
            if self.path == "/app.js":
                return self._serve_static("app.js", "application/javascript; charset=utf-8")
            if self.path == "/style.css":
                return self._serve_static("style.css", "text/css; charset=utf-8")
            if self.path == "/api/data":
                tree = load_json(TREE_FILE)
                prods = load_json(EREDMENY)
                return self._send(200, build_view(tree, prods))
            return self._send(404, {"error": "not found"})
        except Exception as e:
            LOG.exception("HIBA a GET %s kérésben", self.path)
            return self._send(500, {"error": str(e)})

    def _serve_static(self, name, ctype):
        path = os.path.join(UI_DIR, name)
        if not os.path.exists(path):
            return self._send(404, {"error": name + " hiányzik"})
        with open(path, "rb") as fh:
            return self._send(200, fh.read(), ctype)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8"))
        except Exception as e:
            return self._send(400, {"error": f"hibás JSON: {e}"})
        try:
            if self.path == "/api/node_props":
                tree = load_json(TREE_FILE)
                prods = load_json(EREDMENY)
                return self._send(200, {"props": get_effective_props(tree, prods, body["path"])})
            if self.path == "/api/node_group_props":
                tree = load_json(TREE_FILE)
                return self._send(200, {"props": get_node_group_props(tree, body["path"])})
            if self.path == "/api/preview":
                return self._send(200, run_operation(body, write=False))
            if self.path == "/api/apply":
                return self._send(200, run_operation(body, write=True))
        except Exception as e:
            LOG.exception("HIBA a(z) %s kérésben (op=%s)", self.path, body.get("op"))
            return self._send(400, {"error": str(e)})
        return self._send(404, {"error": "not found"})


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def main():
    os.chdir(HERE)
    LOG.info("================ Kategória-szerkesztő indul ================")
    LOG.info("PORT=%s  Fa=%s  Termékek=%s  Log=%s",
             PORT, os.path.basename(TREE_FILE), os.path.basename(EREDMENY), LOG_FILE)
    try:
        srv = ThreadingServer(("127.0.0.1", PORT), Handler)
    except OSError:
        LOG.exception("Nem sikerült a porthoz kötni (%s) — fut már egy példány?", PORT)
        raise
    url = f"http://127.0.0.1:{PORT}"
    print("Kategória-szerkesztő fut:", url)
    print("  Fa:       ", TREE_FILE)
    print("  Termékek: ", EREDMENY)
    print("  Napló:    ", LOG_FILE)
    print("Leállítás: Ctrl+C")
    if "--no-browser" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nLeállítva.")
        LOG.info("Leállítva (Ctrl+C).")
    except Exception:
        LOG.exception("A szerver váratlanul leállt")
        raise
    finally:
        LOG.info("================ Szerver kilépett ================")


if __name__ == "__main__":
    main()
