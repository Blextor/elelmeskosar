# -*- coding: utf-8 -*-
import csv
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(".")
CSV = ROOT / "data/categories/kategorizalando_termekek/GPT/kategorizalatlan_termekek.csv"
OUT = ROOT / ".tmp_contact_sheets"
OUT.mkdir(exist_ok=True)

rows = list(csv.DictReader(CSV.open(encoding="utf-8")))
items = rows[6600:6700]

try:
    font = ImageFont.truetype("arial.ttf", 18)
    small = ImageFont.truetype("arial.ttf", 14)
except Exception:
    font = ImageFont.load_default()
    small = ImageFont.load_default()

cell_w, cell_h = 320, 360
img_h = 250
for sheet_idx in range(4):
    sheet = Image.new("RGB", (cell_w * 5, cell_h * 5), "white")
    draw = ImageDraw.Draw(sheet)
    for j, row in enumerate(items[sheet_idx * 25:(sheet_idx + 1) * 25]):
        x = (j % 5) * cell_w
        y = (j // 5) * cell_h
        draw.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], outline=(180, 180, 180))
        idx = 6601 + sheet_idx * 25 + j
        try:
            im = Image.open(ROOT / row["local_image_paths"]).convert("RGB")
            im.thumbnail((cell_w - 20, img_h - 10), Image.LANCZOS)
            sheet.paste(im, (x + (cell_w - im.width) // 2, y + 8))
        except Exception as exc:
            draw.text((x + 10, y + 90), f"NO IMAGE\n{exc}", fill=(180, 0, 0), font=small)
        lines = [
            f"{idx}. {row['store_product_id']}",
            row["brand_name"][:32],
            row["product_name"][:42],
            row["categories"].split(">")[-1].strip()[:42],
        ]
        yy = y + img_h + 8
        for line in lines:
            draw.text((x + 8, yy), line, fill=(0, 0, 0), font=font if line.startswith(str(idx)) else small)
            yy += 24
    out = OUT / f"batch_6601_6700_{sheet_idx + 1}.jpg"
    sheet.save(out, quality=90)
    print(out)
