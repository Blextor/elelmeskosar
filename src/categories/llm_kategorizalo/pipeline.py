# -*- coding: utf-8 -*-
"""
LLM-alapú tömeges termékkategorizáló pipeline (Batches API + prompt caching +
structured output + determinisztikus utóvalidáció).

A `docs/plans/kategoria_iteracios_terv.md` 2. fázisát (besorolás) gépesíti a
`kategorizalatlan_termekek.csv` backlogon, a `kategoriak_2026-06-13.json` fa ellen.

Rétegek:
  0) Betöltés      – fa + backlog (a CSV-sor MAGA a rekord `termek` mezője).
  1) Routing       – olcsó, szabályalapú előbesorolás EGY főkategóriára
                     (a bolti út + terméknév token-egyezés alapján). Az LLM
                     `fo_override`-ral felülbírálhatja, ha rossz ágba esett.
  2) LLM-besorolás – főkategóriánként csak az ADOTT ág részfáját küldjük be,
                     cache-elt prefixként; a modell alkategória + altípus +
                     tulajdonságok JSON-t ad vissza (structured output).
  3) Validáció     – az eredmény útjait és értékeit a fa ellen ellenőrizzük,
                     a tulajdonság-értékeket a megengedett listákra szűrjük,
                     a `kategoria_hash`-t a kat25.py-vel BITRE azonos képlettel
                     számoljuk. Ami nem fér be / kétséges → review-listára.

Futás (a saját ANTHROPIC_API_KEY-eddel):
  # 1) gyors próba élő (sync) hívással, 20 terméken:
  python -m src.categories.llm_kategorizalo.pipeline sync --limit 20
  # 2) teljes köteg beküldése (Batches API, -50%):
  python -m src.categories.llm_kategorizalo.pipeline batch-submit
  # 3) elkészült kötegek begyűjtése + validáció + eredmeny írás:
  python -m src.categories.llm_kategorizalo.pipeline batch-collect

A szkript SOHA nem ír felül kézi adatot; minden kimenete az `out/` almappába kerül.
"""
from __future__ import annotations
import argparse
import base64
import csv
import hashlib
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict

# ─────────────────────────── útvonalak ───────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
KAT_DIR = os.path.join(REPO_ROOT, "data", "categories", "kategorizalando_termekek", "Claude_Opus")
TREE_PATH = os.path.join(KAT_DIR, "kategoriak_2026-06-13.json")
BACKLOG_CSV = os.path.join(KAT_DIR, "kategorizalatlan_termekek.csv")
OUT_DIR = os.path.join(SCRIPT_DIR, "out")

TERMEK_COLS = [
    "store_name", "store_product_id", "product_name", "brand_name", "unit_price",
    "unit_type", "unit_step", "vegso_mennyiseg", "vegso_egyseg", "ledig",
    "categories", "local_image_paths", "fo_kategoria", "alkategoria", "altipus",
    "tulajdonsagok", "besorolas_alapja", "besorolva",
]

# ─────────────────────────── modell ───────────────────────────
DEFAULT_MODEL = "claude-sonnet-4-6"   # ár/érték optimum; lásd a /claude-api ajánlást
HAIKU = "claude-haiku-4-5"
OPUS = "claude-opus-4-8"
DEFAULT_EFFORT = "medium"             # klasszifikációhoz a medium a sweet spot

SYSTEM_INSTRUKCIO = """\
Te egy magyar élelmiszer-katalogizáló vagy. Egy terméket kell besorolnod a megadott
KATEGÓRIAFA-ÁGBA, és kinyerned a hozzá tartozó tulajdonságokat.

DÖNTÉSI ELVEK (kötelező):
- A bolti kategóriaút csak KIINDULÁS; a terméknév és a kiszerelés (mennyiség/egység)
  együtt dönt. A boltok gyakran rossz helyre sorolnak.
- Tulajdonság-érték CSAK a megadott listából választható. Ha egy listás tulajdonságra
  nincs illő érték, hagyd ki. A flag-tulajdonság értéke true/false.
- Fagyasztott termék a Fagyasztott áruk ágba tartozik (kivéve a fagyasztott
  péksütemény → Pékáru). A HAL kivétel: a fagyasztott hal a "Fagyasztott hal, tengeri áru"
  alkategóriában marad, a friss hal a Hús-hal alatt.
- Készétel CSAK az, ami készen van és legfeljebb mikrózni kell, főétel-jellegű.
  NEM készétel: nyers tészta/pizzatészta (sütni/főzni kell), snack, instant/bögrés leves.
- Olajos magvak: az EGÉSZ, rágcsálható mag (sózott, pörkölt ÉS natúr) az Édesség >
  Rágcsálnivaló magvak ágba megy; a darált/reszelt sütőforma az Alapanyagba.
- A "mentes/bio/vegán/laktózmentes/gluténmentes/protein" jelleget a rokon ág megfelelő
  FLAG-jével jelöld, ne külön "Mentes" ágba tedd (kivéve fehérjepor, vitamin, paleo).

KIMENET: ha a termék NEM ebbe a főkategóriába tartozik, töltsd ki a `fo_override`
mezőt a helyes főkategória nevével (különben üres). A `tulajdonsagok` egy JSON-objektum
STRINGként, a megadott tulajdonság-nevekkel. A `confidence` a besorolás biztossága.
"""

# ─────────────────────────── fa-segédek ───────────────────────────

def load_tree():
    with open(TREE_PATH, encoding="utf-8") as f:
        return json.load(f)


def _norm(s: str) -> str:
    return unicodedata.normalize("NFKD", str(s)).casefold()


def props_for_path(tree, fo, alk, alt):
    """A path-on érvényes tulajdonságok: name -> ('flag'|'single'|'multi', allowed_values).

    flag  → érték bool;  single (egyedi lista) → érték string;  multi (csoportos) → érték lista.
    Üres lista [] = szabad (bármilyen érték elfogadott).
    """
    out = {}

    def add(node):
        t = node.get("tulajdonságok", {}) or {}
        for nev, v in (t.get("egyedi", {}) or {}).items():
            if isinstance(v, dict):
                out[nev] = ("flag", None)
            else:  # lista
                out[nev] = ("single", list(v) if isinstance(v, list) else [])
        for nev, v in (t.get("csoportos", {}) or {}).items():
            out[nev] = ("multi", list(v) if isinstance(v, list) else [])

    if fo in tree:
        add(tree[fo])
        alkmap = tree[fo].get("alkategóriák", {})
        if alk in alkmap:
            add(alkmap[alk])
            altmap = alkmap[alk].get("altípusok", {})
            if alt and alt in altmap:
                add(altmap[alt])
    return out


def compact_branch(tree, fo):
    """Az adott főkategória teljes részfája (cache-elt prefixként ezt küldjük be).

    A fa már a kívánt {tulajdonságok:{egyedi,csoportos}, alkategóriák:{...}} alakú,
    így gyakorlatilag a teljes ág megy – a részletes érték-listák a pontossághoz kellenek,
    a prompt-caching pedig olcsóvá teszi az ismételt beolvasást.
    """
    return {fo: tree[fo]}


def kategoriak_hash(fok, al, alt, tul):
    """BITRE azonos a kat25.py képletével."""
    key = f"{fok}|{al}|{alt}|{json.dumps(tul, sort_keys=True, ensure_ascii=False)}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


# ─────────────────────────── routing (szabály) ───────────────────────────

def build_router(tree):
    """Főkategóriánként szókincs (alk- és altípusnevek tokenjei) a token-egyezéshez."""
    vocab = {}
    for fo, node in tree.items():
        toks = Counter()
        for alk, anode in node.get("alkategóriák", {}).items():
            for w in re.findall(r"\w+", _norm(alk)):
                if len(w) >= 3:
                    toks[w] += 2
            for alt in anode.get("altípusok", {}):
                for w in re.findall(r"\w+", _norm(alt)):
                    if len(w) >= 3:
                        toks[w] += 1
        vocab[fo] = toks
    return vocab


def route(termek, vocab):
    """Egy főkategóriára routol; None, ha bizonytalan (akkor a top-szintű listából választ az LLM)."""
    text = _norm(termek.get("product_name", "") + " " + termek.get("categories", ""))
    words = set(re.findall(r"\w+", text))
    best_fo, best_score = None, 0
    for fo, toks in vocab.items():
        score = sum(toks[w] for w in words if w in toks)
        if score > best_score:
            best_fo, best_score = fo, score
    return best_fo if best_score >= 2 else None


# ─────────────────────────── backlog ───────────────────────────

def load_backlog(limit=None):
    rows = []
    with open(BACKLOG_CSV, encoding="utf-8") as f:
        for i, row in enumerate(csv.DictReader(f)):
            rows.append({c: row.get(c, "") for c in TERMEK_COLS})
            if limit and len(rows) >= limit:
                break
    return rows


# ─────────────────────────── prompt + séma ───────────────────────────

def output_schema(tree, fo):
    """Per-ág structured-output séma: az alkategória ENUM-mal kötött, a többit utólag validáljuk."""
    alk_names = list(tree[fo].get("alkategóriák", {}).keys())
    return {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "required": ["alkategoria", "altipus", "tulajdonsagok_json", "fo_override", "confidence"],
            "properties": {
                "alkategoria": {"type": "string", "enum": alk_names + [""]},
                "altipus": {"type": "string"},
                "tulajdonsagok_json": {"type": "string"},
                "fo_override": {"type": "string", "enum": list(tree.keys()) + [""]},
                "confidence": {"type": "string", "enum": ["magas", "kozepes", "alacsony"]},
            },
        },
    }


def user_text(termek):
    return (
        "Termék:\n"
        f"- név: {termek.get('product_name','')}\n"
        f"- márka: {termek.get('brand_name','')}\n"
        f"- bolti út: {termek.get('categories','')}\n"
        f"- kiszerelés: {termek.get('vegso_mennyiseg','')} {termek.get('vegso_egyseg','')}"
        f" (lédig: {'igen' if termek.get('ledig') else 'nem'})\n"
        f"- egységár: {termek.get('unit_price','')} / {termek.get('unit_type','')}\n\n"
        "Add meg a besorolást a sémának megfelelő JSON-ban."
    )


def build_params(tree, fo, termek, model, effort, with_image=False):
    branch = json.dumps(compact_branch(tree, fo), ensure_ascii=False)
    system = [
        {"type": "text", "text": SYSTEM_INSTRUKCIO},
        {"type": "text", "text": "KATEGÓRIAFA-ÁG:\n" + branch,
         "cache_control": {"type": "ephemeral"}},
    ]
    content = []
    if with_image:
        b64, media = load_image(termek.get("local_image_paths", ""))
        if b64:
            content.append({"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}})
    content.append({"type": "text", "text": user_text(termek)})

    params = {
        "model": model,
        "max_tokens": 1024,
        "system": system,
        "messages": [{"role": "user", "content": content}],
        "output_config": {"format": output_schema(tree, fo)},
    }
    if model != HAIKU:  # a Haiku nem fogad el effort paramétert
        params["output_config"]["effort"] = effort
    return params


def load_image(path):
    if not path:
        return None, None
    full = path if os.path.isabs(path) else os.path.join(REPO_ROOT, path)
    if not os.path.exists(full):
        return None, None
    media = "image/png" if full.lower().endswith(".png") else "image/jpeg"
    with open(full, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("ascii"), media


# ─────────────────────────── validáció + rekord ───────────────────────────

def coerce_tulajdonsagok(allowed, raw):
    """A modell nyers tulajdonság-dictjét a fa megengedett értékeire szűri."""
    clean = {}
    if not isinstance(raw, dict):
        return clean
    for nev, val in raw.items():
        if nev not in allowed:
            continue
        kind, vlist = allowed[nev]
        if kind == "flag":
            clean[nev] = bool(val)
        elif kind == "single":
            v = val[0] if isinstance(val, list) and val else val
            if v in (None, "", False):
                continue
            if not vlist or v in vlist:
                clean[nev] = v
        else:  # multi
            vals = val if isinstance(val, list) else [val]
            keep = [x for x in vals if x not in (None, "", False) and (not vlist or x in vlist)]
            if keep:
                clean[nev] = keep
    return clean


def validate_and_build(tree, fo, termek, parsed):
    """Visszaad: (rekord | None, statusz, indok). statusz: 'kesz' | 'override' | 'review'."""
    fo_override = (parsed.get("fo_override") or "").strip()
    if fo_override and fo_override != fo and fo_override in tree:
        return None, "override", fo_override

    alk = (parsed.get("alkategoria") or "").strip()
    alt = (parsed.get("altipus") or "").strip()
    alkmap = tree[fo].get("alkategóriák", {})
    if alk not in alkmap:
        return None, "review", f"ismeretlen alkategória: {alk!r}"
    altmap = alkmap[alk].get("altípusok", {})
    if alt and alt not in altmap:
        alt = ""  # rossz altípus → ürítjük (a levél-alkategóriáknak nincs altípusa)

    try:
        raw = json.loads(parsed.get("tulajdonsagok_json") or "{}")
    except (ValueError, TypeError):
        raw = {}
    allowed = props_for_path(tree, fo, alk, alt)
    tul = coerce_tulajdonsagok(allowed, raw)

    rec = {
        "termek": termek,
        "fokategoria": fo,
        "alkategoria": alk,
        "altipus": alt,
        "tulajdonsagok": tul,
        "kategoria_hash": kategoriak_hash(fo, alk, alt, tul),
        "statusz": "kesz",
    }
    statusz = "review" if parsed.get("confidence") == "alacsony" else "kesz"
    return rec, statusz, ""


# ─────────────────────────── kimenet ───────────────────────────

def ensure_out():
    os.makedirs(OUT_DIR, exist_ok=True)


def write_json(name, data):
    ensure_out()
    with open(os.path.join(OUT_DIR, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─────────────────────────── SYNC mód (próba) ───────────────────────────

def cmd_sync(args):
    import anthropic
    client = anthropic.Anthropic()
    tree = load_tree()
    vocab = build_router(tree)
    rows = load_backlog(limit=args.limit)

    kesz, review, override = [], [], []
    for i, termek in enumerate(rows):
        fo = route(termek, vocab)
        if fo is None:  # bizonytalan routing → a legnagyobb ágba esünk vissza próbához
            fo = max(vocab, key=lambda k: sum(vocab[k].values()))
        params = build_params(tree, fo, termek, args.model, args.effort, with_image=args.image)
        try:
            resp = client.messages.create(**params)
        except Exception as e:  # noqa: BLE001 – a próba ne álljon le egy hibán
            review.append({"termek": termek, "hiba": str(e)})
            continue
        parsed = parse_response(resp)
        rec, statusz, indok = validate_and_build(tree, fo, termek, parsed)
        if rec is None and statusz == "override":
            override.append({"termek": termek, "fo_override": indok})
        elif rec is None:
            review.append({"termek": termek, "indok": indok, "nyers": parsed})
        elif statusz == "review":
            review.append({"rekord": rec})
            kesz.append(rec)
        else:
            kesz.append(rec)
        print(f"[{i+1}/{len(rows)}] {termek['product_name'][:42]:42} → {fo} > {rec['alkategoria'] if rec else indok}")

    write_json("sync_eredmeny.json", kesz)
    write_json("sync_review.json", review + override)
    print(f"\nKész: {len(kesz)}  | review: {len(review)}  | másik ágba (override): {len(override)}")
    print(f"Kimenet: {OUT_DIR}")


def parse_response(resp):
    for block in resp.content:
        if block.type == "text":
            try:
                return json.loads(block.text)
            except (ValueError, TypeError):
                return {}
    return {}


# ─────────────────────────── BATCH mód ───────────────────────────

def cmd_batch_submit(args):
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    client = anthropic.Anthropic()
    tree = load_tree()
    vocab = build_router(tree)
    rows = load_backlog(limit=args.limit)

    # 1) routing + csoportosítás főkategóriánként (azonos cache-elt prefix klaszterezése)
    by_fo = defaultdict(list)
    routing_index = {}
    fallback_fo = max(vocab, key=lambda k: sum(vocab[k].values()))
    for idx, termek in enumerate(rows):
        fo = route(termek, vocab) or fallback_fo
        by_fo[fo].append(idx)
        routing_index[str(idx)] = {"fo": fo, "termek": termek}
    write_json("batch_routing_index.json", routing_index)

    # 2) kötegek beküldése főkategóriánként
    batch_ids = {}
    for fo, idxs in by_fo.items():
        reqs = [
            Request(
                custom_id=str(idx),
                params=MessageCreateParamsNonStreaming(
                    **build_params(tree, fo, rows[idx], args.model, args.effort)
                ),
            )
            for idx in idxs
        ]
        # max 100k kérés / köteg – darabolás, ha kell
        for part, start in enumerate(range(0, len(reqs), 100_000)):
            chunk = reqs[start:start + 100_000]
            b = client.messages.batches.create(requests=chunk)
            batch_ids[f"{fo}#{part}"] = b.id
            print(f"Beküldve: {fo} (#{part}) – {len(chunk)} termék → batch {b.id}")
    write_json("batch_ids.json", batch_ids)
    print(f"\n{len(batch_ids)} köteg beküldve. Begyűjtés: batch-collect")


def cmd_batch_collect(args):
    import anthropic
    client = anthropic.Anthropic()
    tree = load_tree()
    batch_ids = json.load(open(os.path.join(OUT_DIR, "batch_ids.json"), encoding="utf-8"))
    routing_index = json.load(open(os.path.join(OUT_DIR, "batch_routing_index.json"), encoding="utf-8"))

    # 1) várakozás a kötegekre
    pending = dict(batch_ids)
    while pending:
        done = []
        for tag, bid in pending.items():
            b = client.messages.batches.retrieve(bid)
            if b.processing_status == "ended":
                done.append(tag)
            else:
                print(f"  {tag}: {b.processing_status} (feldolgozás alatt: {b.request_counts.processing})")
        for tag in done:
            pending.pop(tag)
        if pending:
            time.sleep(60)

    # 2) eredmények begyűjtése + validáció
    kesz, review, override, hiba = [], [], [], []
    for tag, bid in batch_ids.items():
        for result in client.messages.batches.results(bid):
            cid = result.custom_id
            entry = routing_index[cid]
            fo, termek = entry["fo"], entry["termek"]
            if result.result.type != "succeeded":
                hiba.append({"custom_id": cid, "tipus": result.result.type, "termek": termek})
                continue
            parsed = parse_message(result.result.message)
            rec, statusz, indok = validate_and_build(tree, fo, termek, parsed)
            if rec is None and statusz == "override":
                override.append({"termek": termek, "fo_override": indok})
            elif rec is None:
                review.append({"termek": termek, "indok": indok, "nyers": parsed})
            else:
                kesz.append(rec)
                if statusz == "review":
                    review.append({"rekord_hash": rec["kategoria_hash"]})

    write_json("eredmeny_llm.json", kesz)
    write_json("review.json", review)
    write_json("masik_agba.json", override)
    if hiba:
        write_json("hibak.json", hiba)
    print(f"\nKész: {len(kesz)}  | review: {len(review)}  | másik ágba: {len(override)}  | hiba: {len(hiba)}")
    print("A 'masik_agba.json' termékeit a routing felülbírálta – futtasd újra rájuk a megfelelő ággal.")
    print(f"Kimenet: {OUT_DIR}")


def parse_message(message):
    for block in message.content:
        if block.type == "text":
            try:
                return json.loads(block.text)
            except (ValueError, TypeError):
                return {}
    return {}


# ─────────────────────────── routing-statisztika (LLM nélkül) ───────────────────────────

def cmd_route_stats(args):
    tree = load_tree()
    vocab = build_router(tree)
    rows = load_backlog(limit=args.limit)
    c = Counter()
    for termek in rows:
        c[route(termek, vocab) or "(bizonytalan)"] += 1
    print(f"Routing-eloszlás {len(rows)} terméken (LLM nélkül):")
    for fo, n in c.most_common():
        print(f"  {n:6d}  {fo}")


# ─────────────────────────── CLI ───────────────────────────

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--model", default=DEFAULT_MODEL, help=f"alapértelmezés: {DEFAULT_MODEL}")
        p.add_argument("--effort", default=DEFAULT_EFFORT, choices=["low", "medium", "high", "max"])
        p.add_argument("--limit", type=int, default=None, help="csak az első N termék (próbához)")

    p = sub.add_parser("route-stats", help="routing-eloszlás LLM nélkül (ingyenes ellenőrzés)")
    p.add_argument("--limit", type=int, default=None)

    p = sub.add_parser("sync", help="élő (nem köteges) próbafutás kis mintán")
    common(p)
    p.add_argument("--image", action="store_true", help="küldje be a termékképet is (látás)")

    p = sub.add_parser("batch-submit", help="teljes köteg beküldése (Batches API, -50%)")
    common(p)

    p = sub.add_parser("batch-collect", help="elkészült kötegek begyűjtése + validáció + eredmeny")

    args = ap.parse_args()
    if args.cmd == "route-stats":
        cmd_route_stats(args)
    elif args.cmd == "sync":
        cmd_sync(args)
    elif args.cmd == "batch-submit":
        cmd_batch_submit(args)
    elif args.cmd == "batch-collect":
        cmd_batch_collect(args)


if __name__ == "__main__":
    main()
