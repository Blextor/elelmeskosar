import ast
import csv
import glob
import json
import os
import re
from typing import Optional, Tuple

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_size import to_full_size


csv.field_size_limit(1024 * 1024 * 1024)

MAIN_FOLDER = "./../../../data/markets_data/"


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
    return os.path.basename(os.getcwd()).lower()


def generate_filename(y_base, date_str: str, extension=".csv"):
    x = get_current_dir_name()
    return f"{MAIN_FOLDER}{x}_{y_base}_{date_str}{extension}"


def read_latest_file(y_base: str, extension=".csv"):
    x = get_current_dir_name()
    pattern = f"{MAIN_FOLDER}{x}_{y_base}_*{extension}"
    candidates = glob.glob(pattern)
    if not candidates:
        raise FileNotFoundError(f"Nincs fajl: {pattern}")

    latest = max(candidates, key=os.path.getmtime)
    match = re.search(rf"{re.escape(x)}_{re.escape(y_base)}_(\d{{8}}_\d{{6}}){re.escape(extension)}", latest)
    if not match:
        raise ValueError("Nem sikerult datumot kinyerni a fajlnevbol.")
    date_str = match.group(1)

    print(f"Fajl kivalasztva: {latest} (datum: {date_str})")
    return latest, date_str


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def empty_to_none(value):
    value = clean_text(value)
    return value if value else None


def to_float(value):
    if value is None:
        return None
    value = clean_text(value).replace(",", ".")
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
    if value in {"true", "1", "yes", "available"}:
        return True
    if value in {"false", "0", "no", "unavailable"}:
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
    if unit in {"kilogram", "kilograms", "kg", "kilo"}:
        return value * 1000, "g"
    if unit in {"gram", "grams", "g"}:
        return value, "g"
    if unit in {"liter", "litre", "liters", "litres", "l", "literes"}:
        return value * 1000, "ml"
    if unit in {"milliliter", "millilitre", "milliliters", "millilitres", "ml"}:
        return value, "ml"
    if unit == "cl":
        return value * 10, "ml"
    if unit in {"piece", "pieces", "db", "darab", "each"}:
        return value, "db"
    return value, unit


def parse_pack_from_text(text: str) -> Tuple[Optional[float], Optional[str]]:
    text = clean_text(text).lower().replace("×", "x")
    if not text:
        return None, None

    multipack = re.findall(
        r"(\d+(?:[\.,]\d+)?)\s*[x]\s*(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|piece|pieces)",
        text,
        flags=re.IGNORECASE,
    )
    if multipack:
        count, value, unit = multipack[-1]
        total = float(count.replace(",", ".")) * float(value.replace(",", "."))
        if total > 0:
            return normalize_unit(total, unit)

    matches = re.findall(r"(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|piece|pieces)\b", text, flags=re.IGNORECASE)
    if matches:
        for value, unit in reversed(matches):
            numeric_value = float(value.replace(",", "."))
            if numeric_value > 0:
                return normalize_unit(numeric_value, unit)
    return None, None


def price_fields(row):
    gross = to_float(row.get("selectedVariant.price.gross"))
    gross_discounted = to_float(row.get("selectedVariant.price.grossDiscounted"))
    is_discounted = to_bool(row.get("selectedVariant.price.isDiscounted"))

    price = gross_discounted if gross_discounted is not None else gross
    original = None
    if gross is not None and price is not None and abs(gross - price) > 0.01:
        original = gross
        is_discounted = True

    if is_discounted is None:
        is_discounted = False
    return price, is_discounted, original


def package_step(row):
    package_size = to_float(row.get("selectedVariant.packageInfo.packageSize"))
    package_unit = clean_text(row.get("selectedVariant.packageInfo.packageUnit"))
    value, unit = normalize_unit(package_size, package_unit)
    if value is not None and value > 0 and unit:
        return value, unit

    loose_weight = to_float(row.get("selectedVariant.loose.weightPerPiece"))
    loose = to_bool(row.get("selectedVariant.loose.loose"))
    if loose and loose_weight is not None and loose_weight > 0:
        return normalize_unit(loose_weight, "kg")

    cart_step = to_float(row.get("selectedVariant.cartInfo.quantityStepSize"))
    variant_unit = clean_text(row.get("selectedVariant.unit"))
    value, unit = normalize_unit(cart_step, variant_unit)
    if value is not None and value > 0 and unit:
        return value, unit

    value, unit = parse_pack_from_text(row.get("selectedVariant.name", ""))
    if value is not None and value > 0 and unit:
        return value, unit

    return 1.0, "db"


def images(row):
    values = []
    raw_images = parse_structured(row.get("selectedVariant.media.images"))
    if isinstance(raw_images, list):
        values.extend(clean_text(value) for value in raw_images if clean_text(value))
    for field in ["selectedVariant.media.mainImage", "selectedVariant.media.listImage"]:
        value = clean_text(row.get(field))
        if value and value not in values:
            values.append(value)
    return ";".join(to_full_size(value) for value in values)


def category_path(row):
    fetch_paths = parse_structured(row.get("fetch_category_paths"))
    if isinstance(fetch_paths, list) and fetch_paths:
        return "|".join(clean_text(path) for path in fetch_paths if clean_text(path))
    return clean_text(row.get("fetch_category_path")) or clean_text(row.get("categoryName"))


def roll_fields(row):
    roll_price = to_float(row.get("selectedVariant.roll.price.gross"))
    roll_quantity = to_float(row.get("selectedVariant.roll.quantity.quantity"))
    roll_unit = clean_text(row.get("selectedVariant.roll.quantity.type"))
    if roll_price is None:
        return None, None, None
    value, unit = normalize_unit(roll_quantity or 1.0, roll_unit or "piece")
    return roll_price, unit or "db", value or 1.0


input_file_name, input_date = read_latest_file("filtered_data")
output_file_name = generate_filename("normalized_data", input_date)

with open(input_file_name, mode="r", encoding="utf-8-sig", newline="") as infile, open(
    output_file_name, mode="w", encoding="utf-8", newline=""
) as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=output_fields)
    writer.writeheader()

    for row in reader:
        product_id = clean_text(row.get("id"))
        variant_id = clean_text(row.get("selectedVariant.id") or row.get("defaultVariant.id"))
        unit_price, is_discounted, original_unit_price = price_fields(row)
        unit_step, unit_type = package_step(row)
        availability = clean_text(row.get("selectedVariant.cartInfo.availability")).lower()
        available = availability == "available" if availability else True
        barcode = clean_text(row.get("selectedVariant.eanCode") or row.get("eancode") or row.get("defaultVariant.eanCode"))
        secondary_unit_price, secondary_unit_type, secondary_unit_step = roll_fields(row)

        writer.writerow(
            {
                "store_name": "Auchan",
                "store_product_id": f"{product_id}:{variant_id}" if variant_id else product_id,
                "product_name": clean_text(row.get("selectedVariant.name") or row.get("defaultVariant.name")),
                "brand_name": clean_text(row.get("selectedVariant.brandName") or row.get("brandName")),
                "available": available,
                "expected_restock": "",
                "barcode": barcode,
                "unit_price": unit_price if unit_price is not None else "",
                "unit_type": unit_type or "",
                "unit_step": round(float(unit_step), 3) if unit_step is not None else "",
                "is_discounted": is_discounted,
                "original_unit_price": original_unit_price if original_unit_price is not None else "",
                "secondary_unit_price": secondary_unit_price if secondary_unit_price is not None else "",
                "secondary_unit_type": secondary_unit_type or "",
                "secondary_unit_step": secondary_unit_step if secondary_unit_step is not None else "",
                "image_urls": images(row),
                "description": "",
                "categories": category_path(row),
            }
        )

print(f"Auchan normalizalt fajl mentve ide: {output_file_name}")
