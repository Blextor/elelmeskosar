# -*- coding: utf-8 -*-
"""
Termék-böngésző webszerver.

Egyszerű, függőség nélküli (csak Python stdlib) HTTP szerver, ami a
GPT/eredmeny.json (kategorizált termékek) és GPT/kategoriak_*.json
(kategóriafa) alapján egy böngészhető, szűrhető termékfelületet szolgál ki.

A szűrés/lapozás szerveroldalon történik, így a 41 MB-os JSON-t nem kell
a böngészőbe tölteni.

Indítás:
    python server.py
majd nyisd meg:  http://localhost:8765
"""

import csv
import json
import os
import re
import sys
import unicodedata
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote

HERE = os.path.dirname(os.path.abspath(__file__))
GPT_DIR = os.path.dirname(HERE)                       # .../GPT
# repo gyökér (a local_image_paths innen relatív): .../GPT/termek_bongeszo -> 5 szint föl
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

EREDMENY = os.path.join(GPT_DIR, "eredmeny.json")
# A CSV ugyanazt a 47030 terméket tartalmazza, és az eredmeny.json-ből gyakran
# hiányzó store_name / local_image_paths mezőket innen pótoljuk (store_product_id alapján).
CSV_FORRAS = os.path.join(GPT_DIR, "kategorizalatlan_termekek.csv")
PORT = int(os.environ.get("PORT", "8764"))

# Hány tulajdonság-érték (fazetta) jöjjön vissza maximum egy tulajdonságnál.
MAX_FACET_VALUES = 300

# ----------------------------------------------------------------------------
# Adatbetöltés és indexelés
# ----------------------------------------------------------------------------

PRODUCTS = []        # slim rekordok listája (kereséshez)
TREE = {}            # fokat -> {alkat -> {altipus -> count}}
RAW = []             # a teljes eredmeny.json rekordok (részletes nézethez)
CSV_FULL = {}        # store_product_id -> teljes CSV sor (részletes nézethez)


def norm(s):
    """Ékezet- és kisbetű-érzéketlen normalizálás kereséshez."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


def normalize_props(raw):
    """A nyers tulajdonság-szótárt {név: [str értékek]} alakra hozza.

    - bool True  -> ["igen"], False -> ["nem"]
    - str        -> [str]
    - list       -> a lista string elemei
    Az üres/None értékeket kihagyja.
    """
    out = {}
    if not isinstance(raw, dict):
        return out
    for k, v in raw.items():
        if v is None or v == "":
            continue
        if isinstance(v, bool):
            out[k] = ["igen" if v else "nem"]
        elif isinstance(v, list):
            vals = [str(x) for x in v if x is not None and x != ""]
            if vals:
                out[k] = vals
        else:
            out[k] = [str(v)]
    return out


def load_csv_index():
    """store_product_id -> teljes CSV sor (kép/áruház pótláshoz és részletes nézethez)."""
    idx = {}
    if not os.path.isfile(CSV_FORRAS):
        sys.stderr.write("Figyelem: nincs CSV (%s), képpótlás kihagyva.\n" % CSV_FORRAS)
        return idx
    with open(CSV_FORRAS, "r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            spid = (row.get("store_product_id") or "").strip()
            if not spid:
                continue
            idx[spid] = dict(row)
    return idx


def load():
    global PRODUCTS, TREE, RAW, CSV_FULL
    sys.stderr.write("Betöltés: %s ...\n" % EREDMENY)
    with open(EREDMENY, "r", encoding="utf-8") as f:
        data = json.load(f)
    csv_idx = load_csv_index()
    RAW = data
    CSV_FULL = csv_idx

    products = []
    tree = {}
    filled = 0
    for i, x in enumerate(data):
        t = x.get("termek", {}) or {}
        fokat = x.get("fokategoria", "") or ""
        alkat = x.get("alkategoria", "") or ""
        altipus = x.get("altipus", "") or ""
        props = normalize_props(x.get("tulajdonsagok"))
        name = t.get("product_name", "") or ""

        store = t.get("store_name", "") or ""
        img = (t.get("local_image_paths", "") or "").split(";")[0].strip()
        # hiányzó áruház / kép pótlása a CSV-ből store_product_id alapján
        if not img or not store:
            extra = csv_idx.get((t.get("store_product_id") or "").strip())
            if extra:
                if not store:
                    store = (extra.get("store_name") or "").strip()
                csv_img = (extra.get("local_image_paths") or "").split(";")[0].strip()
                if not img and csv_img:
                    img = csv_img
                    filled += 1

        rec = {
            "id": i,
            "name": name,
            "name_norm": norm(name),
            "brand": t.get("brand_name", "") or props.get("márka", [""])[0],
            "store": store,
            "price": t.get("unit_price", "") or "",
            "unit": t.get("unit_type", "") or "",
            "qty": t.get("vegso_mennyiseg", "") or "",
            "qunit": t.get("vegso_egyseg", "") or "",
            "img": img,
            "fokat": fokat,
            "alkat": alkat,
            "altipus": altipus,
            "props": props,
        }
        products.append(rec)

        a = tree.setdefault(fokat, {})
        b = a.setdefault(alkat, {})
        b[altipus] = b.get(altipus, 0) + 1

    PRODUCTS = products
    TREE = tree
    sys.stderr.write("Kész: %d termék, %d főkategória. CSV-ből pótolt kép: %d.\n"
                     % (len(products), len(tree), filled))


# ----------------------------------------------------------------------------
# Szűrés
# ----------------------------------------------------------------------------

def candidate_match(rec, fokat, alkat, altipus, name_q):
    if fokat and rec["fokat"] != fokat:
        return False
    if alkat and rec["alkat"] != alkat:
        return False
    if altipus and rec["altipus"] != altipus:
        return False
    if name_q and name_q not in rec["name_norm"]:
        return False
    return True


def prop_match(rec, propname, selected):
    """A rekord adott tulajdonsága metszi-e a kiválasztott értékeket (OR)."""
    have = rec["props"].get(propname)
    if not have:
        return False
    return any(v in selected for v in have)


def search(params):
    fokat = params.get("fokategoria", [""])[0]
    alkat = params.get("alkategoria", [""])[0]
    altipus = params.get("altipus", [""])[0]
    name_q = norm(params.get("name", [""])[0])
    page = max(1, int(params.get("page", ["1"])[0] or 1))
    page_size = min(200, max(1, int(params.get("page_size", ["48"])[0] or 48)))
    sort = params.get("sort", ["name"])[0]

    try:
        prop_filters = json.loads(params.get("props", ["{}"])[0] or "{}")
    except Exception:
        prop_filters = {}
    # csak nem-üres szűrők
    prop_filters = {k: set(v) for k, v in prop_filters.items() if v}

    # 1) kategória + név szerinti alaphalmaz
    base = [r for r in PRODUCTS
            if candidate_match(r, fokat, alkat, altipus, name_q)]

    # 2) tulajdonság-szűrők alkalmazása (AND a tulajdonságok között)
    def passes_all_props(rec, skip=None):
        for pn, sel in prop_filters.items():
            if pn == skip:
                continue
            if not prop_match(rec, pn, sel):
                return False
        return True

    filtered = [r for r in base if passes_all_props(rec=r)]

    # 3) fazetták: minden tulajdonsághoz a (skip=önmaga) szűrt halmazon számolunk.
    #    - A NEM szűrt tulajdonságok a teljes szűrt halmazon (filtered) számolnak,
    #      így mutatják, hány termék érintett az aktuális szűrés mellett (akár 0).
    #    - A szűrt tulajdonság a saját szűrőjét kihagyva (skip-self) számol, így
    #      ugyanazon tulajdonságon belül további értéket is be lehet jelölni (VAGY).
    facet_counts = {}   # propname -> {value: count}
    prop_total = {}     # propname -> hány terméknek van egyáltalán ilyen tulajdonsága
    for pn in set(_iter_propnames(base)):
        subset = filtered if pn not in prop_filters else [r for r in base if passes_all_props(rec=r, skip=pn)]
        vc = {}
        n_have = 0
        for r in subset:
            vals = r["props"].get(pn)
            if not vals:
                continue
            n_have += 1
            for v in vals:
                vc[v] = vc.get(v, 0) + 1
        if vc:
            facet_counts[pn] = vc
            prop_total[pn] = n_have

    # fazetták rendezése: gyakoriság szerint, értékek is gyakoriság szerint
    facets = []
    for pn in sorted(facet_counts, key=lambda p: (-prop_total[p], norm(p))):
        vals = sorted(facet_counts[pn].items(), key=lambda kv: (-kv[1], norm(kv[0])))
        facets.append({
            "name": pn,
            "total": prop_total[pn],
            "truncated": len(vals) > MAX_FACET_VALUES,
            "values": [{"value": v, "count": c} for v, c in vals[:MAX_FACET_VALUES]],
            "selected": sorted(prop_filters.get(pn, [])),
        })

    # 4) rendezés
    if sort == "price_asc":
        filtered.sort(key=lambda r: (_num(r["price"]), r["name_norm"]))
    elif sort == "price_desc":
        filtered.sort(key=lambda r: (-_num(r["price"]), r["name_norm"]))
    else:
        filtered.sort(key=lambda r: r["name_norm"])

    total = len(filtered)
    start = (page - 1) * page_size
    page_items = filtered[start:start + page_size]

    items = [{
        "id": r["id"],
        "name": r["name"],
        "brand": r["brand"],
        "store": r["store"],
        "price": r["price"],
        "unit": r["unit"],
        "qty": r["qty"],
        "qunit": r["qunit"],
        "img": r["img"],
        "fokat": r["fokat"],
        "alkat": r["alkat"],
        "altipus": r["altipus"],
        "props": r["props"],
    } for r in page_items]

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": (total + page_size - 1) // page_size,
        "items": items,
        "facets": facets,
    }


def _iter_propnames(recs):
    for r in recs:
        for k in r["props"].keys():
            yield k


def _num(s):
    try:
        return float(str(s).replace(",", "."))
    except Exception:
        return float("inf")


# ----------------------------------------------------------------------------
# HTTP
# ----------------------------------------------------------------------------

STATIC = {".html": "text/html; charset=utf-8",
          ".js": "application/javascript; charset=utf-8",
          ".css": "text/css; charset=utf-8"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send_json(self, obj, code=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path, ctype):
        try:
            with open(path, "rb") as f:
                body = f.read()
        except OSError:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        path = u.path

        if path == "/" or path == "/index.html":
            return self._send_file(os.path.join(HERE, "index.html"), STATIC[".html"])
        if path in ("/app.js", "/style.css"):
            ext = os.path.splitext(path)[1]
            return self._send_file(os.path.join(HERE, path.lstrip("/")), STATIC[ext])

        if path == "/api/tree":
            tree = {fk: {ak: dict(sorted(bk.items()))
                         for ak, bk in sorted(a.items())}
                    for fk, a in sorted(TREE.items())}
            counts = {fk: sum(sum(bk.values()) for bk in a.values())
                      for fk, a in TREE.items()}
            return self._send_json({"tree": tree, "counts": counts,
                                    "total": len(PRODUCTS)})

        if path == "/api/search":
            params = parse_qs(u.query, keep_blank_values=True)
            try:
                return self._send_json(search(params))
            except Exception as e:
                return self._send_json({"error": str(e)}, 500)

        if path == "/api/product":
            params = parse_qs(u.query, keep_blank_values=True)
            try:
                pid = int(params.get("id", ["-1"])[0])
            except ValueError:
                pid = -1
            if pid < 0 or pid >= len(RAW):
                return self._send_json({"error": "ismeretlen termék"}, 404)
            rec = RAW[pid]
            slim = PRODUCTS[pid]
            spid = (rec.get("termek", {}) or {}).get("store_product_id", "")
            return self._send_json({
                "id": pid,
                "store": slim["store"],          # az esetleg CSV-ből pótolt áruház
                "img": slim["img"],              # a ténylegesen használt képútvonal
                "eredmeny": rec,                 # a teljes eredmeny.json rekord
                "csv": CSV_FULL.get((spid or "").strip()),  # a hozzá tartozó teljes CSV sor (vagy null)
            })

        if path.startswith("/img/"):
            rel = unquote(path[len("/img/"):])
            rel = rel.replace("\\", "/").lstrip("/")
            full = os.path.abspath(os.path.join(REPO_ROOT, rel))
            if not full.startswith(REPO_ROOT) or not os.path.isfile(full):
                self.send_error(404)
                return
            ext = os.path.splitext(full)[1].lower()
            ctype = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                     ".png": "image/png", ".webp": "image/webp",
                     ".gif": "image/gif"}.get(ext, "application/octet-stream")
            return self._send_file(full, ctype)

        self.send_error(404)


def main():
    load()
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = "http://localhost:%d" % PORT
    sys.stderr.write("\n  Termék-böngésző fut:  %s\n  (Ctrl+C a leállításhoz)\n\n" % url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        sys.stderr.write("\nLeállítva.\n")


if __name__ == "__main__":
    main()
