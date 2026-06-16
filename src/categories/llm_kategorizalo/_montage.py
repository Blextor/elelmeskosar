# -*- coding: utf-8 -*-
"""Montázs + szöveges adatlap N termékről (eredmeny.json adott indextől).
Használat: python _montage.py START [COUNT]  (alap COUNT=25)
Kimenet: _montage.png (rács, cellánként sorszámmal) + _lst.txt (szöveges info)."""
import sys, os, json, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pipeline as P
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = P.REPO_ROOT
START = int(sys.argv[1]) if len(sys.argv) > 1 else 1712
COUNT = int(sys.argv[2]) if len(sys.argv) > 2 else 25
ered = json.load(open('data/categories/kategorizalando_termekek/Claude_Opus/eredmeny.json', encoding='utf-8'))
tree = P.load_tree()
recs = ered[START:START+COUNT]

COLS = 5
CELL = 500
LBL = 34
rows = (len(recs) + COLS - 1) // COLS
W = COLS * CELL
H = rows * (CELL + LBL)
canvas = Image.new('RGB', (W, H), (255, 255, 255))
draw = ImageDraw.Draw(canvas)
try:
    font = ImageFont.truetype("arialbd.ttf", 30)
except Exception:
    font = ImageFont.load_default()

def resolve(pth):
    if not pth: return None
    f = pth if os.path.isabs(pth) else os.path.join(REPO, pth)
    return f if os.path.exists(f) else None

for k, r in enumerate(recs):
    idx = START + k
    cx = (k % COLS) * CELL
    cy = (k // COLS) * (CELL + LBL)
    # címke-sáv
    draw.rectangle([cx, cy, cx+CELL, cy+LBL], fill=(20, 20, 20))
    draw.text((cx+6, cy+2), f"#{idx}", fill=(255, 230, 0), font=font)
    box = (cx, cy+LBL, cx+CELL, cy+LBL+CELL)
    f = resolve(r['termek'].get('local_image_paths', ''))
    if f:
        try:
            im = Image.open(f).convert('RGB')
            im.thumbnail((CELL-10, CELL-10))
            ox = cx + (CELL - im.width)//2
            oy = cy + LBL + (CELL - im.height)//2
            canvas.paste(im, (ox, oy))
        except Exception:
            draw.text((cx+10, cy+LBL+10), "KÉP HIBA", fill=(200, 0, 0), font=font)
    else:
        draw.text((cx+10, cy+LBL+10), "NINCS KÉP", fill=(200, 0, 0), font=font)
    draw.rectangle([cx, cy, cx+CELL-1, cy+LBL+CELL-1], outline=(180, 180, 180))

canvas.save(os.path.join(HERE, '_montage.png'))

with io.open(os.path.join(HERE, '_lst.txt'), 'w', encoding='utf-8') as o:
    for k, r in enumerate(recs):
        idx = START + k; t = r['termek']
        o.write(f"#{idx} {t['product_name']}  [{t.get('vegso_mennyiseg','')} {t.get('vegso_egyseg','')}]\n")
        o.write(f"  PATH: {r['fokategoria']} > {r['alkategoria']} > {r['altipus']}\n")
        al = P.props_for_path(tree, r['fokategoria'], r['alkategoria'], r['altipus'])
        for nm, (kind, vals) in al.items():
            o.write(f"    [{'flag' if kind=='flag' else kind}] {nm}" + ("" if kind == 'flag' else f": {vals}") + "\n")
        o.write("\n")
print(f"OK montage {START}..{START+len(recs)-1} ({len(recs)} db)")
