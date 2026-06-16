from pathlib import Path
import csv
from PIL import Image, ImageDraw, ImageFont

CSV = Path("data/categories/kategorizalando_termekek/GPT/kategorizalatlan_termekek.csv")
OUT = Path(".tmp_contact_sheets")
OUT.mkdir(exist_ok=True)

with CSV.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

try:
    font = ImageFont.truetype("arial.ttf", 18)
    small = ImageFont.truetype("arial.ttf", 14)
except OSError:
    font = ImageFont.load_default()
    small = ImageFont.load_default()

for block in range(4):
    start = 3199 + block * 25
    sheet = Image.new("RGB", (5 * 260, 5 * 310), "white")
    draw = ImageDraw.Draw(sheet)
    for pos, idx in enumerate(range(start, start + 25)):
        r = rows[idx]
        x = (pos % 5) * 260
        y = (pos // 5) * 310
        draw.rectangle([x, y, x + 259, y + 309], outline=(180, 180, 180))
        draw.text((x + 6, y + 5), f"{idx + 1}. {r['store_product_id']}", fill=(0, 0, 0), font=font)
        img_path = Path(r["local_image_paths"].split("|")[0])
        try:
            img = Image.open(img_path).convert("RGB")
            img.thumbnail((220, 210))
            ix = x + (260 - img.width) // 2
            iy = y + 35 + (210 - img.height) // 2
            sheet.paste(img, (ix, iy))
        except Exception as e:
            draw.text((x + 20, y + 120), f"IMAGE ERROR: {e}", fill=(180, 0, 0), font=small)
        name = r["product_name"]
        if len(name) > 58:
            name = name[:55] + "..."
        draw.text((x + 6, y + 255), name, fill=(0, 0, 0), font=small)
        brand = r["brand_name"] or "-"
        if len(brand) > 35:
            brand = brand[:32] + "..."
        draw.text((x + 6, y + 282), f"brand: {brand}", fill=(30, 30, 30), font=small)
    out = OUT / f"batch_3200_3299_{block + 1}.jpg"
    sheet.save(out, quality=92)
    print(out)
