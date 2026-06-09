import ast
import csv
import glob
import json
import os
import re
from typing import Optional, Tuple


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
    if value in {"true", "1", "yes"}:
        return True
    if value in {"false", "0", "no"}:
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
    unit = unit.lower().strip()
    if unit in {"kg", "kilogram", "kilograms"}:
        return value * 1000, "g"
    if unit in {"g", "gram", "grams"}:
        return value, "g"
    if unit in {"l", "litre", "liter", "litres", "liters"}:
        return value * 1000, "ml"
    if unit in {"ml", "millilitre", "milliliter", "millilitres", "milliliters"}:
        return value, "ml"
    if unit == "cl":
        return value * 10, "ml"
    if unit in {"each", "piece", "pc", "pcs", "db", "number_of_items"}:
        return value, "db"
    return value, unit


def parse_pack_from_text(text: str) -> Tuple[Optional[float], Optional[str]]:
    text = clean_text(text).lower()
    if not text:
        return None, None

    multipack = re.findall(
        r"(\d+(?:[\.,]\d+)?)\s*[x×]\s*(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|pcs|pc)",
        text,
        flags=re.IGNORECASE,
    )
    if multipack:
        count, value, unit = multipack[-1]
        total = float(count.replace(",", ".")) * float(value.replace(",", "."))
        if total > 0:
            return normalize_unit(total, unit)

    reverse_multipack = re.findall(
        r"(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|pcs|pc)\s*[x×]\s*(\d+(?:[\.,]\d+)?)",
        text,
        flags=re.IGNORECASE,
    )
    if reverse_multipack:
        value, unit, count = reverse_multipack[-1]
        total = float(value.replace(",", ".")) * float(count.replace(",", "."))
        if total > 0:
            return normalize_unit(total, unit)

    matches = re.findall(r"(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|pcs|pc)\b", text, flags=re.IGNORECASE)
    if matches:
        for value, unit in reversed(matches):
            numeric_value = float(value.replace(",", "."))
            if numeric_value > 0:
                return normalize_unit(numeric_value, unit)

    if text.endswith(" db"):
        return 1.0, "db"
    return None, None


def parse_pack_size_field(row) -> Tuple[Optional[float], Optional[str]]:
    pack_size = parse_structured(row.get("details.packSize"))
    if isinstance(pack_size, dict):
        pack_size = [pack_size]
    if isinstance(pack_size, list):
        for item in pack_size:
            if not isinstance(item, dict):
                continue
            value = to_float(item.get("value"))
            unit = clean_text(item.get("units")).lower()
            if value is not None and value > 0 and unit and unit not in {"sngl", "single"}:
                return normalize_unit(value, unit)

    pack_value = to_float(row.get("details.packSize.value"))
    pack_unit = clean_text(row.get("details.packSize.units")).lower()
    if pack_value is not None and pack_value > 0 and pack_unit and pack_unit not in {"sngl", "single"}:
        return normalize_unit(pack_value, pack_unit)

    return None, None


def parse_pack_from_details(row) -> Tuple[Optional[float], Optional[str]]:
    value, unit = parse_pack_size_field(row)
    if value is not None and value > 0 and unit:
        return value, unit

    for field in ["details.netContents", "details.drainedWeight", "details.boxContents"]:
        value, unit = parse_pack_from_text(row.get(field, ""))
        if value is not None and value > 0 and unit:
            return value, unit
    return None, None


def parse_pack_from_title(row) -> Tuple[Optional[float], Optional[str]]:
    return parse_pack_from_text(row.get("title", ""))


def selected_catch_weight(row):
    items = parse_structured(row.get("catchWeightList"))
    if not isinstance(items, list) or not items:
        return None
    for item in items:
        if isinstance(item, dict) and item.get("default") is True:
            return item
    return items[0] if isinstance(items[0], dict) else None


def step_from_unit_price(actual, base_price, measure):
    measure = clean_text(measure).lower()
    if actual is None or base_price in (None, 0):
        return None, None
    if measure in {"kg", "kilogram", "kilograms"}:
        return round(actual / base_price * 1000, 3), "g"
    if measure in {"l", "litre", "liter", "litres", "liters"}:
        return round(actual / base_price * 1000, 3), "ml"
    if measure in {"each", "piece", "pc", "pcs", "db"}:
        return 1.0, "db"
    return None, None


def product_step_and_price(row):
    actual = to_float(row.get("price.actual"))
    base_price = to_float(row.get("price.unitPrice"))
    measure = clean_text(row.get("price.unitOfMeasure")).lower()

    catch_weight = selected_catch_weight(row)
    if catch_weight:
        catch_price = to_float(catch_weight.get("price"))
        catch_weight_value = to_float(catch_weight.get("weight"))
        if catch_price is not None and catch_weight_value is not None and catch_weight_value > 0:
            value, unit = normalize_unit(catch_weight_value, measure or "kg")
            return catch_price, value, unit

    pack_value, pack_unit = parse_pack_from_details(row)
    if pack_value is not None and pack_value > 0 and pack_unit:
        return actual, pack_value, pack_unit

    step_value, step_unit = step_from_unit_price(actual, base_price, measure)
    if step_value is not None and step_value > 0 and step_unit:
        return actual, step_value, step_unit

    title_value, title_unit = parse_pack_from_title(row)
    if title_value is not None and title_value > 0 and title_unit:
        return actual, title_value, title_unit

    return actual, 1.0, "db"


def first_promotion_price(row):
    promotions = parse_structured(row.get("promotions"))
    if not isinstance(promotions, list):
        return None, None
    for promotion in promotions:
        if not isinstance(promotion, dict):
            continue
        price = promotion.get("price") or {}
        before = to_float(price.get("beforeDiscount"))
        after = to_float(price.get("afterDiscount"))
        if before is not None:
            return before, after
    return None, None


def original_price_for_step(row, unit_price, unit_step, unit_type):
    before, after = first_promotion_price(row)
    if before is None:
        return None

    actual = to_float(row.get("price.actual"))
    base_price = to_float(row.get("price.unitPrice"))
    measure = clean_text(row.get("price.unitOfMeasure")).lower()

    if after is not None and actual is not None and abs(after - actual) < 0.01:
        return before

    if after is not None and base_price is not None and abs(after - base_price) < 0.01:
        if measure in {"kg", "kilogram", "kilograms"} and unit_type == "g":
            return round(before * unit_step / 1000, 3)
        if measure in {"l", "litre", "liter", "litres", "liters"} and unit_type == "ml":
            return round(before * unit_step / 1000, 3)

    if measure in {"kg", "kilogram", "kilograms"} and unit_type == "g" and unit_step:
        return round(before * unit_step / 1000, 3)
    if measure in {"l", "litre", "liter", "litres", "liters"} and unit_type == "ml" and unit_step:
        return round(before * unit_step / 1000, 3)
    return before


def category_path(row):
    parts = [
        clean_text(row.get("superDepartmentName")),
        clean_text(row.get("departmentName")),
        clean_text(row.get("aisleName")),
        clean_text(row.get("shelfName")),
    ]
    return "|".join(part for part in parts if part)


def description_from_row(row):
    parts = [
        clean_text(row.get("shortDescription")),
        clean_text(row.get("details.netContents")),
        clean_text(row.get("details.drainedWeight")),
    ]
    return " | ".join(part for part in parts if part) or None


input_file_name, input_date = read_latest_file("all_data")
output_file_name = generate_filename("normalized_data", input_date)

cnt_all = 0
cnt_no_step = 0
cnt_discounted = 0

with open(input_file_name, mode="r", encoding="utf-8", newline="") as infile, open(
    output_file_name, mode="w", encoding="utf-8", newline=""
) as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=output_fields)
    writer.writeheader()

    for row in reader:
        cnt_all += 1
        unit_price, unit_step, unit_type = product_step_and_price(row)
        if unit_step is None or unit_type is None:
            unit_step, unit_type = 1.0, "db"
            cnt_no_step += 1

        original_unit_price = original_price_for_step(row, unit_price, unit_step, unit_type)
        is_discounted = original_unit_price is not None
        if is_discounted:
            cnt_discounted += 1

        available = to_bool(row.get("isForSale"))
        if available is None:
            status = clean_text(row.get("status")).lower()
            available = status in {"availableforsale", "available"}

        writer.writerow(
            {
                "store_name": "Tesco",
                "store_product_id": clean_text(row.get("id") or row.get("tpnc")),
                "product_name": clean_text(row.get("title")),
                "brand_name": empty_to_none(row.get("brandName")),
                "available": available,
                "expected_restock": None,
                "barcode": empty_to_none(row.get("gtin")),
                "unit_price": unit_price,
                "unit_type": unit_type,
                "unit_step": round(float(unit_step), 3) if unit_step is not None else None,
                "is_discounted": is_discounted,
                "original_unit_price": original_unit_price,
                "secondary_unit_price": None,
                "secondary_unit_type": None,
                "secondary_unit_step": None,
                "image_urls": empty_to_none(row.get("defaultImageUrl")),
                "description": description_from_row(row),
                "categories": category_path(row),
            }
        )

print(f"{cnt_all} Tesco sor normalizalva")
print(f"{cnt_discounted} akcios sor")
print(f"{cnt_no_step} sor fallback 1 db kiszerelessel")
print(f"Normalizalt fajl mentve ide: {output_file_name}")
