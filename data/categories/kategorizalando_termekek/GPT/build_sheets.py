# -*- coding: utf-8 -*-
"""Kontaktív-generátor: 5x5-ös számozott blokkok a Claude-os vizuális
kategorizáláshoz. Csak képcsoportosítás (a rules.txt által engedett kód)."""
import csv, json, os, sys
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, "..", "..", "..", ".."))
CSV = os.path.join(BASE, "kategorizalatlan_termekek.csv")
OUT = os.path.join(BASE, "_contact_sheets")
os.makedirs(OUT, exist_ok=True)

CELL = 300          # cellaméret px
PAD = 8
LABEL_H = 28
GRID = 5            # 5x5

def load_rows():
    with open(CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def resolve_img(p):
    if not p:
        return None
    cand = p.split(";")[0].strip()
    for full in (os.path.join(REPO, cand), os.path.join(BASE, cand), cand):
        if os.path.exists(full):
            return full
    return None

def make_sheet(rows, start, sheet_no, prefix):
    n = GRID * GRID
    W = GRID * (CELL + PAD) + PAD
    H = GRID * (CELL + LABEL_H + PAD) + PAD
    sheet = Image.new("RGB", (W, H), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = ImageFont.load_default()
    for i in range(n):
        ridx = start + i
        if ridx >= len(rows):
            break
        row = rows[ridx]
        gx = i % GRID
        gy = i // GRID
        x = PAD + gx * (CELL + PAD)
        y = PAD + gy * (CELL + LABEL_H + PAD)
        # label: szám (1-25)
        label = f"{i+1}"
        draw.rectangle([x, y, x + CELL, y + LABEL_H], fill=(30, 30, 60))
        draw.text((x + 4, y + 4), label, fill=(255, 255, 255), font=font)
        # kép
        imgp = resolve_img(row.get("local_image_paths", ""))
        box_y = y + LABEL_H
        if imgp:
            try:
                im = Image.open(imgp).convert("RGB")
                im.thumbnail((CELL - 2 * PAD, CELL - 2 * PAD))
                ox = x + (CELL - im.width) // 2
                oy = box_y + (CELL - im.height) // 2
                sheet.paste(im, (ox, oy))
            except Exception as e:
                draw.text((x + 6, box_y + 6), f"[hiba]", fill=(200, 0, 0), font=font)
        else:
            draw.text((x + 6, box_y + 6), "[nincs kép]", fill=(150, 0, 0), font=font)
        draw.rectangle([x, y, x + CELL, box_y + CELL], outline=(180, 180, 180))
    path = os.path.join(OUT, f"{prefix}_sheet_{sheet_no}.jpg")
    sheet.save(path, quality=85)
    return path

def main():
    start = int(sys.argv[1])
    nsheets = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    prefix = sys.argv[3] if len(sys.argv) > 3 else f"batch_{start}"
    rows = load_rows()
    print(f"CSV sorok: {len(rows)}; kezdő index: {start}")
    for s in range(nsheets):
        st = start + s * 25
        if st >= len(rows):
            break
        p = make_sheet(rows, st, s + 1, prefix)
        end = min(st + 25, len(rows))
        print(f"sheet {s+1}: CSV {st}..{end-1} -> {p}")

if __name__ == "__main__":
    main()
