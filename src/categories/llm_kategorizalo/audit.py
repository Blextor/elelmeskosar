# -*- coding: utf-8 -*-
"""Teljesség-audit: az eredmeny.json adott indextől (alap 1700) minden rekordnál
összeveti a path ÖSSZES tulajdonságát (fő+alk+altípus) a ténylegesen kitöltöttekkel.
Kész = minden flag eldöntve (bool), minden lista ≥1 érték, minden string ≠ ''.
Használat: python src/categories/llm_kategorizalo/audit.py [START]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P
from collections import Counter

START = int(sys.argv[1]) if len(sys.argv) > 1 else 1700
tree = P.load_tree()
ered = json.load(open('data/categories/kategorizalando_termekek/Claude_Opus/eredmeny.json', encoding='utf-8'))
sub = ered[START:]

def fld(v):
    if isinstance(v, bool): return True
    if isinstance(v, list): return len(v) > 0
    if isinstance(v, str): return v != ''
    return v is not None

miss_by_prop = Counter(); miss_by_fo = Counter(); incomplete = 0; total_missing = 0; complete = 0
for r in sub:
    al = P.props_for_path(tree, r['fokategoria'], r['alkategoria'], r['altipus'])
    tul = r['tulajdonsagok']
    miss = [n for n in al if n not in tul or not fld(tul[n])]
    if miss:
        incomplete += 1; total_missing += len(miss); miss_by_fo[r['fokategoria']] += 1
        for n in miss: miss_by_prop[n] += 1
    else:
        complete += 1

print(f"Auditalt ({START}-tol): {len(sub)}")
print(f"  Hianytalan: {complete}  | Hianyos: {incomplete}")
print(f"  Osszes hianyzo slot: {total_missing}  (atlag/rekord: {total_missing/max(len(sub),1):.1f})")
if miss_by_fo:
    print("Hianyos fokategoriankent:")
    for k, v in miss_by_fo.most_common(): print(f"  {v:4d}  {k}")
    print("Leggyakrabban hianyzo tulajdonsagok (top 15):")
    for k, v in miss_by_prop.most_common(15): print(f"  {v:4d}  {k}")
