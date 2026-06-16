# -*- coding: utf-8 -*-
"""SABLON a teljes-kitöltéses pótláshoz (montázs-munkamenet 3. lépése).
Másold le, töltsd ki a FULL dictet (index -> a path ÖSSZES tulajdonsága), futtasd.
A KATEGORIZALAS_SZABALYOK.md 7. szakasza írja le a teljes folyamatot.

Szabály: minden flag true/false; minden lista ≥1 érték (szükség esetén 'egyéb'
felvételével a fába); hiányzó márka/érték/csoport -> előbb a fába; a hiány-ellenőrzés
a coerce UTÁNI (clean) értéken fut."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P

TREE = P.TREE_PATH
ERED = 'data/categories/kategorizalando_termekek/Claude_Opus/eredmeny.json'
tree = P.load_tree()
ered = json.load(open(ERED, encoding='utf-8'))

# --- (opcionális) FA-BŐVÍTÉS: hiányzó márka/érték/csoport felvétele ---
# pl.: tree['Pékáru']['alkategóriák']['Hotdog buci és hamburger zsemle']
#         ['tulajdonságok']['egyedi']['márka'].append('Azon Melegében')

# --- DÖNTÉSEK: index -> teljes tulajdonsagok dict (MINDEN flag + MINDEN lista) ---
FULL = {
    # 1887: {'fagyasztott': False, 'márka': '...', 'helyben sütött': True, ...},
}

def fld(v):
    return isinstance(v, bool) or (isinstance(v, list) and v) or (isinstance(v, str) and v != '')

bad = 0
for i, tul in FULL.items():
    r = ered[i]
    al = P.props_for_path(tree, r['fokategoria'], r['alkategoria'], r['altipus'])
    clean = P.coerce_tulajdonsagok(al, tul)            # a fa listáira szűr
    miss = [n for n in al if n not in clean or not fld(clean[n])]   # CLEAN-en ellenőriz
    if miss:
        print(f"#{i} {r['alkategoria']}>{r['altipus']} miss={miss}"); bad += 1
    r['tulajdonsagok'] = clean
    r['kategoria_hash'] = P.kategoriak_hash(r['fokategoria'], r['alkategoria'], r['altipus'], clean)

if bad == 0 and FULL:
    json.dump(tree, open(TREE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    json.dump(ered, open(ERED, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f"Mentve: {len(FULL)} rekord")
else:
    print("NEM mentve (hiányos vagy ures FULL)")
