import ast
import csv
import glob
import html
import json
import os
import re
from typing import Optional, Tuple
from urllib.parse import urljoin


MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "lidl"
BASE_URL = "https://www.lidl.hu"


output_fields = [
    "store_name",
    "store_product_id",
    "product_name",
    "brand_name",
    "available",
    "expected_restock",
    "barcode",
    "unit_price",
    "unit_type",
    "unit_step",
    "is_discounted",
    "original_unit_price",
    "secondary_unit_price",
    "secondary_unit_type",
    "secondary_unit_step",
    "image_urls",
    "description",
    "categories",
]


def get_current_dir_name():
    return MARKET_NAME


def generate_filename(y_base, date_str: str, extension=".csv"):
    x = get_current_dir_name()
    return f"{MAIN_FOLDER}{x}_{y_base}_{date_str}{extension}"


def read_latest_file(y_base: str, extension=".csv"):
    x = get_current_dir_name()
    pattern = f"{MAIN_FOLDER}{x}_{y_base}_*{extension}"
    candidates = glob.glob(pattern)
    if not candidates:
        raise FileNotFoundError(f"Nincs fájl: {pattern}")

    latest = max(candidates, key=os.path.getmtime)
    match = re.search(rf"{re.escape(x)}_{re.escape(y_base)}_(\d{{8}}_\d{{6}}){re.escape(extension)}", latest)
    if not match:
        raise ValueError("Nem sikerült dátumot kinyerni a fájlnévből.")
    date_str = match.group(1)

    print(f"Fájl kiválasztva: {latest} (dátum: {date_str})")
    return latest, date_str


def clean_text(value):
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def html_to_text(value):
    value = html.unescape(str(value or ""))
    value = re.sub(r"<[^>]+>", " ", value)
    return clean_text(value)


def empty_to_none(value):
    value = clean_text(value)
    return value if value else None


def to_float(value):
    if value is None:
        return None
    value = clean_text(value).replace("\xa0", " ").replace(" ", "").replace(",", ".")
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def number_from_text(value):
    value = clean_text(value).replace("\xa0", " ").replace(" ", "").replace(",", ".")
    return float(value)


def parse_structured(value):
    value = clean_text(value)
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def normalize_unit(value: float, unit: str) -> Tuple[Optional[float], Optional[str]]:
    if value is None or not unit:
        return None, None
    unit = clean_text(unit).lower()
    if unit in {"kg", "kilogram", "kilogramm"}:
        return value * 1000, "g"
    if unit in {"g", "gr", "gram", "gramm"}:
        return value, "g"
    if unit in {"l", "liter", "litre", "literes"}:
        return value * 1000, "ml"
    if unit in {"ml", "milliliter", "millilitre"}:
        return value, "ml"
    if unit == "cl":
        return value * 10, "ml"
    if unit in {"db", "darab", "piece", "pieces", "pc", "pcs"}:
        return value, "db"
    return value, unit


def parse_pack_from_text(text: str) -> Tuple[Optional[float], Optional[str]]:
    text = clean_text(text).lower().replace("×", "x")
    if not text:
        return None, None

    number_pattern = r"\d[\d\s]*(?:[\.,]\d+)?"
    multipack = re.findall(
        rf"(?<![a-záéíóöőúüű])({number_pattern})\s*x\s*({number_pattern})\s*(kg|g|ml|l|cl|db|pcs|pc)\b",
        text,
        flags=re.IGNORECASE,
    )
    if multipack:
        count, value, unit = multipack[0]
        total = number_from_text(count) * number_from_text(value)
        if total > 0:
            return normalize_unit(total, unit)

    matches = re.findall(
        rf"(?<![a-záéíóöőúüű])({number_pattern})\s*(kg|g|ml|l|cl|db|pcs|pc)\b",
        text,
        flags=re.IGNORECASE,
    )
    if matches:
        value, unit = matches[0]
        numeric_value = number_from_text(value)
        if numeric_value > 0:
            return normalize_unit(numeric_value, unit)

    return None, None


def base_price_text(row):
    base_text = clean_text(row.get("gridbox.data.price.basePrice.text"))
    if not base_text:
        plus_price = first_lidl_plus_price(row)
        base_price = plus_price.get("basePrice") if isinstance(plus_price, dict) else None
        if isinstance(base_price, dict):
            base_text = clean_text(base_price.get("text"))
    return base_text


def parse_base_unit_price(text: str):
    text = clean_text(text).lower().replace("\xa0", " ")
    match = re.search(r"1\s*(kg|l|db)\s*=\s*(\d[\d\s]*(?:[\.,]\d+)?)\s*ft", text, flags=re.IGNORECASE)
    if not match:
        return None
    source_unit = match.group(1)
    unit_type = {"kg": "g", "l": "ml", "db": "db"}[source_unit]
    denominator = {"kg": 1000.0, "l": 1000.0, "db": 1.0}[source_unit]
    return number_from_text(match.group(2)), denominator, unit_type


def inferred_step_from_base_price(base_text, parsed_step, parsed_unit, item_price):
    if parsed_step is None or not parsed_unit or item_price is None:
        return None, None
    parsed = parse_base_unit_price(base_text)
    if not parsed:
        return None, None
    base_unit_price, denominator, unit_type = parsed
    if base_unit_price <= 0 or parsed_unit != unit_type or unit_type == "db":
        return None, None
    if re.search(r"\d[\d\s]*(?:[\.,]\d+)?\s*x\s*\d[\d\s]*(?:[\.,]\d+)?", base_text, re.I):
        return None, None

    inferred_step = item_price / base_unit_price * denominator
    if inferred_step <= 0:
        return None, None
    rounded_step = round(inferred_step)
    if abs(inferred_step - rounded_step) < 0.2:
        inferred_step = float(rounded_step)
    if inferred_step >= parsed_step * 1.25:
        return inferred_step, unit_type
    return None, None


def package_step(row, item_price=None):
    base_text = base_price_text(row)
    value, unit = parse_pack_from_text(base_text)
    if value is not None and value > 0 and unit:
        inferred_value, inferred_unit = inferred_step_from_base_price(base_text, value, unit, item_price)
        if inferred_value is not None:
            return inferred_value, inferred_unit
        return value, unit

    title = clean_text(row.get("gridbox.data.fullTitle") or row.get("gridbox.data.title"))
    value, unit = parse_pack_from_text(title)
    if value is not None and value > 0 and unit:
        return value, unit

    if base_text.startswith("/kg") or "1 kg" in base_text.lower():
        return 1000.0, "g"
    if base_text.startswith("/l") or "1 l" in base_text.lower() or "1l" in base_text.lower():
        return 1000.0, "ml"
    if "1 db" in base_text.lower() or base_text.lower() == "db":
        return 1.0, "db"
    return 1.0, "db"


def first_lidl_plus_price(row):
    offers = parse_structured(row.get("gridbox.data.lidlPlus"))
    if not isinstance(offers, list) or not offers:
        return {}
    first = offers[0]
    if isinstance(first, dict) and isinstance(first.get("price"), dict):
        return first.get("price") or {}
    return {}


def price_fields(row):
    unit_price = to_float(row.get("gridbox.data.price.price"))
    original_unit_price = to_float(row.get("gridbox.data.price.oldPrice"))
    is_discounted = False

    plus_price = first_lidl_plus_price(row)
    plus_current = to_float(plus_price.get("price"))
    plus_old = to_float(plus_price.get("oldPrice") or (plus_price.get("discount") or {}).get("deletedPrice"))

    if unit_price is None and plus_current is not None:
        unit_price = plus_current
        original_unit_price = plus_old
        is_discounted = plus_old is not None and plus_old > plus_current + 0.01
    elif unit_price is not None and original_unit_price is not None and original_unit_price > unit_price + 0.01:
        is_discounted = True
    else:
        original_unit_price = None

    return unit_price, is_discounted, original_unit_price


def secondary_fee(row):
    description = html_to_text(row.get("gridbox.data.keyfacts.description"))
    match = re.search(r"\+\s*(\d+(?:[\s.,]\d+)?)\s*ft\s*(?:bet[ée]td[ií]j|visszav[aá]lt[aá]si\s+d[ií]j)", description, re.I)
    if match:
        return to_float(match.group(1))
    return None


def valid_gtin(value):
    digits = re.sub(r"\D", "", clean_text(value))
    if len(digits) not in {8, 12, 13, 14}:
        return ""
    body = digits[:-1]
    check_digit = int(digits[-1])
    total = 0
    for index, digit in enumerate(reversed(body), start=1):
        total += int(digit) * (3 if index % 2 == 1 else 1)
    expected = (10 - (total % 10)) % 10
    return digits if expected == check_digit else ""


def barcode(row):
    gs1 = parse_structured(row.get("gridbox.data.gs1Attributes"))
    if isinstance(gs1, dict):
        for key in ["gtin", "ean", "barcode", "upc"]:
            value = valid_gtin(gs1.get(key))
            if value:
                return value
    return ""


def image_urls(row):
    values = []
    for field in ["gridbox.data.image", "gridbox.data.image_V1"]:
        value = clean_text(row.get(field))
        if value and value not in values:
            values.append(value)
    for field in ["gridbox.data.imageList", "gridbox.data.imageList_V1"]:
        parsed = parse_structured(row.get(field))
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    for key in ["url", "src", "image", "imageUrl"]:
                        value = clean_text(item.get(key))
                        if value and value not in values:
                            values.append(value)
                else:
                    value = clean_text(item)
                    if value and value not in values:
                        values.append(value)
    return ";".join(values)


def availability(row):
    value = to_float(row.get("gridbox.data.stockAvailability.availabilityIndicator"))
    if value is None:
        return True
    return int(value) != 1


def product_name(row):
    full_title = clean_text(row.get("gridbox.data.fullTitle") or row.get("gridbox.data.keyfacts.fullTitle"))
    if full_title:
        return full_title
    brand = clean_text(row.get("gridbox.data.brand.name"))
    title = clean_text(row.get("gridbox.data.title") or row.get("gridbox.data.keyfacts.title"))
    if brand and title and not title.lower().startswith(brand.lower()):
        return f"{brand} {title}"
    return title


def categories(row):
    values = []
    root = clean_text(row.get("fetch_category_name"))
    if root:
        values.append(root)
    won = clean_text(row.get("gridbox.data.keyfacts.wonCategoryPrimary"))
    if won:
        values.append(won.replace("/", " > "))
    simple = clean_text(row.get("gridbox.data.category"))
    if simple:
        values.append(simple)
    result = []
    for value in values:
        if value and value not in result:
            result.append(value)
    return "|".join(result)


def promotions_text(row):
    parts = []
    discount = clean_text(row.get("gridbox.data.price.discount.discountText"))
    if discount:
        parts.append(f"Árkedvezmény: {discount}")

    offers = parse_structured(row.get("gridbox.data.lidlPlus"))
    if isinstance(offers, list):
        for offer in offers:
            if not isinstance(offer, dict):
                continue
            label = clean_text(offer.get("lidlPlusText"))
            highlight = clean_text(offer.get("highlightText"))
            if label or highlight:
                parts.append("Lidl Plus: " + " ".join(part for part in [label, highlight] if part))

    ribbons = parse_structured(row.get("gridbox.data.ribbons"))
    if isinstance(ribbons, list):
        for ribbon in ribbons:
            if isinstance(ribbon, dict):
                text = clean_text(ribbon.get("text"))
                if text:
                    parts.append(f"Szalag: {text}")
    return " | ".join(parts)


def description(row):
    parts = []
    desc = html_to_text(row.get("gridbox.data.keyfacts.description"))
    if desc:
        parts.append(desc)
    promo = promotions_text(row)
    if promo:
        parts.append(promo)
    canonical = clean_text(row.get("gridbox.data.canonicalUrl") or row.get("gridbox.data.canonicalPath"))
    if canonical:
        parts.append(f"URL: {urljoin(BASE_URL, canonical)}")
    ians = clean_text(row.get("gridbox.data.ians"))
    if ians:
        parts.append(f"Lidl IAN/cikkszám mező: {ians}")
    return " | ".join(parts)


input_file_name, input_date = read_latest_file("filtered_data")
output_file_name = generate_filename("normalized_data", input_date)

cnt_all = 0
cnt_discounted = 0
cnt_secondary = 0
cnt_barcode = 0

with open(input_file_name, mode="r", encoding="utf-8-sig", newline="") as infile, open(
    output_file_name, mode="w", encoding="utf-8", newline=""
) as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=output_fields)
    writer.writeheader()

    for row in reader:
        cnt_all += 1
        unit_price, is_discounted, original_unit_price = price_fields(row)
        unit_step, unit_type = package_step(row, unit_price)
        secondary_unit_price = secondary_fee(row)
        barcode_value = barcode(row)

        if is_discounted:
            cnt_discounted += 1
        if secondary_unit_price is not None and secondary_unit_price > 0:
            cnt_secondary += 1
        if barcode_value:
            cnt_barcode += 1

        writer.writerow(
            {
                "store_name": "Lidl",
                "store_product_id": clean_text(row.get("gridbox.data.erpNumber") or row.get("code")),
                "product_name": product_name(row),
                "brand_name": empty_to_none(row.get("gridbox.data.brand.name")),
                "available": availability(row),
                "expected_restock": "",
                "barcode": barcode_value,
                "unit_price": round(unit_price, 3) if unit_price is not None else "",
                "unit_type": unit_type or "",
                "unit_step": round(float(unit_step), 3) if unit_step is not None else "",
                "is_discounted": is_discounted,
                "original_unit_price": round(original_unit_price, 3) if original_unit_price is not None else "",
                "secondary_unit_price": round(secondary_unit_price, 3) if secondary_unit_price is not None and secondary_unit_price > 0 else "",
                "secondary_unit_type": "db" if secondary_unit_price is not None and secondary_unit_price > 0 else "",
                "secondary_unit_step": 1.0 if secondary_unit_price is not None and secondary_unit_price > 0 else "",
                "image_urls": image_urls(row),
                "description": description(row),
                "categories": categories(row),
            }
        )

print(f"{cnt_all} Lidl sor normalizálva")
print(f"{cnt_discounted} akciós sor")
print(f"{cnt_secondary} sor betétdíjjal")
print(f"{cnt_barcode} sor vonalkóddal")
print(f"Normalizált fájl mentve ide: {output_file_name}")
