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
import os
import socketserver
import sys
import tempfile
import threading
import webbrowser
from collections import Counter

PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(HERE, "ksz_ui")
EREDMENY = os.path.join(HERE, "eredmeny.json")

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
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
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
        for name, val in src.get(group, {}).items():
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
def props_summary(node):
    out = []
    p = node.get(PROP_KEY, {})
    for group in GROUPS:
        for name, val in p.get(group, {}).items():
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
    for fk, fn in tree.items():
        fk_node = {
            "name": fk, "level": 1, "path": [fk],
            "count": count_prefix([fk]),
            "props": props_summary(fn),
            "children": [],
        }
        for ak, an in fn.get("alkategóriák", {}).items():
            ak_node = {
                "name": ak, "level": 2, "path": [fk, ak],
                "count": count_prefix([fk, ak]),
                "direct": count_exact([fk, ak]),
                "props": props_summary(an),
                "children": [],
            }
            for at, atn in an.get("altípusok", {}).items():
                ak_node["children"].append({
                    "name": at, "level": 3, "path": [fk, ak, at],
                    "count": count_exact([fk, ak, at]),
                    "props": props_summary(atn),
                    "children": [],
                })
            fk_node["children"].append(ak_node)
        fk_list.append(fk_node)

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
    if src_node is None:
        raise ValueError("A forrás node nem létezik.")

    # 1) Fa: leválaszt + beilleszt/összeolvaszt
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
    if src_node is None:
        raise ValueError("A forrás node nem létezik.")
    parent_path = source[:-1]
    parent_node = get_node(tree, parent_path)

    # 1) Fa: minden leszármazott tulajdonságát felolvasztjuk a szülőbe, majd töröljük a node-ot
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


OPS = {
    "move_node": lambda t, p, b: op_move_node(t, p, b["source"], b["target"]),
    "dissolve": lambda t, p, b: op_dissolve(t, p, b["source"]),
    "create_property": lambda t, p, b: op_create_property(
        t, p, b["node"], b["group"], b["name"], b["kind"], b.get("values", [])),
    "move_property": lambda t, p, b: op_move_property(
        t, p, b["source"], b["source_prop"], b["target"], b["target_prop"],
        b["group"], b.get("kind", "lista"), b.get("value"), b.get("new_value")),
}


def run_operation(body, write):
    op = body.get("op")
    if op not in OPS:
        raise ValueError(f"Ismeretlen művelet: {op}")
    tree = load_json(TREE_FILE)
    prods = load_json(EREDMENY)
    work_tree = copy.deepcopy(tree)
    work_prods = copy.deepcopy(prods)
    new_tree, new_prods, summary = OPS[op](work_tree, work_prods, body)
    if write:
        save_json_atomic(TREE_FILE, new_tree)
        save_json_atomic(EREDMENY, new_prods)
        summary["written"] = True
    else:
        summary["written"] = False
        summary["view"] = build_view(new_tree, new_prods)
    return summary


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
            if self.path == "/api/preview":
                return self._send(200, run_operation(body, write=False))
            if self.path == "/api/apply":
                return self._send(200, run_operation(body, write=True))
        except Exception as e:
            return self._send(400, {"error": str(e)})
        return self._send(404, {"error": "not found"})


class ThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


def main():
    os.chdir(HERE)
    srv = ThreadingServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}"
    print("Kategória-szerkesztő fut:", url)
    print("  Fa:       ", TREE_FILE)
    print("  Termékek: ", EREDMENY)
    print("Leállítás: Ctrl+C")
    if "--no-browser" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nLeállítva.")


if __name__ == "__main__":
    main()
