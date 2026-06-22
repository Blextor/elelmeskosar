import ast
import csv
import glob
import html
import json
import os
import re
from typing import Optional, Tuple


csv.field_size_limit(1024 * 1024 * 1024)

MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "coopshop"


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


def to_bool(value):
    if isinstance(value, bool):
        return value
    value = clean_text(value).lower()
    if value in {"true", "1", "yes", "igen", "in-stock"}:
        return True
    if value in {"false", "0", "no", "nem", "out-of-stock"}:
        return False
    return None


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
    if unit in {"kg", "kilogram", "kilograms", "kilogramm"}:
        return value * 1000, "g"
    if unit in {"g", "gr", "gram", "grams", "gramm"}:
        return value, "g"
    if unit in {"l", "liter", "litre", "liters", "litres", "literes"}:
        return value * 1000, "ml"
    if unit in {"ml", "milliliter", "millilitre", "milliliters", "millilitres"}:
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

    multipack = re.findall(
        r"(?<![a-záéíóöőúüű])(\d+(?:[\.,]\d+)?)\s*x\s*(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|pcs|pc)\b",
        text,
        flags=re.IGNORECASE,
    )
    if multipack:
        count, value, unit = multipack[-1]
        total = float(count.replace(",", ".")) * float(value.replace(",", "."))
        if total > 0:
            return normalize_unit(total, unit)

    piece_matches = re.findall(
        r"(?<![a-záéíóöőúüű])(\d+(?:[\.,]\d+)?)\s*(db|darab|kapsz\.?|kapszula|tabl\.?|tabletta|tasak)(?=\s|$|[.,;:)])",
        text,
        flags=re.IGNORECASE,
    )
    if piece_matches:
        value, _unit = piece_matches[-1]
        numeric_value = float(value.replace(",", "."))
        if numeric_value > 0:
            return numeric_value, "db"

    matches = re.findall(
        r"(?<![a-záéíóöőúüű])(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|pcs|pc)\b",
        text,
        flags=re.IGNORECASE,
    )
    if matches:
        for value, unit in reversed(matches):
            numeric_value = float(value.replace(",", "."))
            if numeric_value > 0:
                return normalize_unit(numeric_value, unit)

    return None, None


def price_to_huf(amount, minor_unit):
    value = to_float(amount)
    if value is None:
        return None
    minor = to_float(minor_unit)
    if minor is None:
        minor = 0
    return value / (10 ** int(minor))


def price_fields(row):
    unit_price = price_to_huf(row.get("prices.price"), row.get("prices.currency_minor_unit"))
    regular_price = price_to_huf(row.get("prices.regular_price"), row.get("prices.currency_minor_unit"))
    sale_price = price_to_huf(row.get("prices.sale_price"), row.get("prices.currency_minor_unit"))
    on_sale = to_bool(row.get("on_sale"))

    original_unit_price = None
    is_discounted = False
    if on_sale and regular_price is not None and unit_price is not None and regular_price > unit_price + 0.01:
        original_unit_price = regular_price
        is_discounted = True
    elif sale_price is not None and regular_price is not None and regular_price > sale_price + 0.01:
        original_unit_price = regular_price
        unit_price = sale_price
        is_discounted = True

    return unit_price, is_discounted, original_unit_price


def secondary_fee(row):
    price_text = html_to_text(row.get("price_html"))
    match = re.search(r"\+\s*(\d+(?:[\s.,]\d+)?)\s*ft\s*visszav[aá]lt[aá]si\s+d[ií]j", price_text, re.I)
    if not match:
        return None
    return to_float(match.group(1))


def package_step(row):
    value, unit = parse_pack_from_text(row.get("name", ""))
    if value is not None and value > 0 and unit:
        return value, unit

    value, unit = parse_pack_from_text(row.get("formatted_weight", ""))
    if value is not None and value > 0 and unit:
        return value, unit

    return 1.0, "db"


def first_brand(row):
    brands = parse_structured(row.get("brands"))
    if isinstance(brands, list):
        for brand in brands:
            if isinstance(brand, dict):
                value = clean_text(brand.get("name"))
                if value:
                    return value
            else:
                value = clean_text(brand)
                if value:
                    return value
    return ""


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


def image_urls(row):
    values = []
    images = parse_structured(row.get("images"))
    if isinstance(images, list):
        for image in images:
            if isinstance(image, dict):
                for field in ["src", "thumbnail"]:
                    value = clean_text(image.get(field))
                    if value and value not in values:
                        values.append(value)
            else:
                value = clean_text(image)
                if value and value not in values:
                    values.append(value)
    return ";".join(values)


def category_paths(row):
    paths = []
    for field in ["fetch_category_paths", "product_category_paths"]:
        parsed_paths = parse_structured(row.get(field))
        if isinstance(parsed_paths, list):
            for path in parsed_paths:
                value = clean_text(path)
                if value and value not in paths:
                    paths.append(value)
    if paths:
        return "|".join(paths)

    categories = parse_structured(row.get("categories"))
    names = []
    if isinstance(categories, list):
        for category in categories:
            if isinstance(category, dict):
                name = clean_text(category.get("name"))
                if name and name not in names:
                    names.append(name)
    if names:
        return "|".join(names)

    fetch_paths = parse_structured(row.get("fetch_category_paths"))
    if isinstance(fetch_paths, list):
        return "|".join(clean_text(path) for path in fetch_paths if clean_text(path))
    return ""


def availability(row):
    in_stock = to_bool(row.get("is_in_stock"))
    purchasable = to_bool(row.get("is_purchasable"))
    if in_stock is False or purchasable is False:
        return False
    stock_class = clean_text(row.get("stock_availability.class")).lower()
    if stock_class:
        return stock_class == "in-stock"
    return True


def description(row):
    parts = []
    short_description = html_to_text(row.get("short_description"))
    if short_description:
        parts.append(short_description)
    sku = clean_text(row.get("sku"))
    if sku:
        parts.append(f"SKU: {sku}")
    stock = clean_text(row.get("stock_availability.text"))
    if stock:
        parts.append(f"Készlet: {stock}")
    formatted_weight = clean_text(row.get("formatted_weight"))
    if formatted_weight:
        parts.append(f"Coopshop súly mező: {formatted_weight}")
    return " | ".join(parts)


input_file_name, input_date = read_latest_file("filtered_data")
output_file_name = generate_filename("normalized_data", input_date)

cnt_all = 0
cnt_discounted = 0
cnt_secondary = 0

with open(input_file_name, mode="r", encoding="utf-8-sig", newline="") as infile, open(
    output_file_name, mode="w", encoding="utf-8", newline=""
) as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=output_fields)
    writer.writeheader()

    for row in reader:
        cnt_all += 1
        unit_price, is_discounted, original_unit_price = price_fields(row)
        unit_step, unit_type = package_step(row)
        secondary_unit_price = secondary_fee(row)

        if is_discounted:
            cnt_discounted += 1
        if secondary_unit_price is not None and secondary_unit_price > 0:
            cnt_secondary += 1

        writer.writerow(
            {
                "store_name": "Coopshop",
                "store_product_id": clean_text(row.get("id")),
                "product_name": clean_text(row.get("name")),
                "brand_name": empty_to_none(first_brand(row)),
                "available": availability(row),
                "expected_restock": "",
                "barcode": valid_gtin(row.get("sku")),
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
                "categories": category_paths(row),
            }
        )

print(f"{cnt_all} Coopshop sor normalizálva")
print(f"{cnt_discounted} akciós sor")
print(f"{cnt_secondary} sor visszaváltási díjjal")
print(f"Normalizált fájl mentve ide: {output_file_name}")
