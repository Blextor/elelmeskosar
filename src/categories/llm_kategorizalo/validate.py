# -*- coding: utf-8 -*-
"""Az eredmeny.json teljes integritás-ellenőrzése a fa ellen:
  - fő/alkategória/altípus út érvényes-e,
  - minden tulajdonság-kulcs a path megengedett tulajdonságai közül való-e,
  - minden listás érték a fa megengedett értéklistájában van-e, flag bool-e,
  - a kategoria_hash bitre egyezik-e (sha256("fok|al|alt|json(tul,sort_keys)")).
Csak összesítést és néhány mintát ír ki. Használat: python .../validate.py"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P
from collections import defaultdict

tree = P.load_tree()
ered = json.load(open('data/categories/kategorizalando_termekek/Claude_Opus/eredmeny.json', encoding='utf-8'))

def kh(fok, al, alt, tul):
    return hashlib.sha256(f"{fok}|{al}|{alt}|{json.dumps(tul, sort_keys=True, ensure_ascii=False)}".encode('utf-8')).hexdigest()

err = defaultdict(list); hash_bad = 0
for i, r in enumerate(ered):
    fo, alk, alt, tul = r['fokategoria'], r['alkategoria'], r['altipus'], r['tulajdonsagok']
    if fo not in tree:
        err['fo_ismeretlen'].append(i); continue
    alks = tree[fo].get('alkategóriák', {})
    if alk not in alks:
        err['alk_ismeretlen'].append(i)
    else:
        alts = alks[alk].get('altípusok', {})
        if alt and alt not in alts:
            err['altipus_ismeretlen'].append(i)
        allowed = P.props_for_path(tree, fo, alk, alt)
        for nm, val in (tul.items() if isinstance(tul, dict) else []):
            if nm not in allowed:
                err['tulajdonsag_kulcs_ismeretlen'].append((i, nm)); continue
            kind, vals = allowed[nm]
            if kind == 'flag':
                if not isinstance(val, bool): err['flag_nem_bool'].append((i, nm))
            elif vals:
                for v in (val if isinstance(val, list) else [val]):
                    if v not in ('', None, False) and v not in vals:
                        err['ertek_nincs_listaban'].append((i, nm, v))
    if kh(fo, alk, alt, tul) != r.get('kategoria_hash'):
        hash_bad += 1

print(f"Rekordok: {len(ered)}")
print(f"Hash-elteres: {hash_bad}")
if not err:
    print("Integritas: TISZTA (0 ut-/ertek-hiba)")
else:
    for k, v in sorted(err.items(), key=lambda x: -len(x[1])):
        print(f"{k}: {len(v)}  pl: {v[:5]}")
