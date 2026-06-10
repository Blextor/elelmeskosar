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
MARKET_NAME = "aldi"


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
        raise FileNotFoundError(f"Nincs fajl: {pattern}")

    latest = max(candidates, key=os.path.getmtime)
    match = re.search(rf"{re.escape(x)}_{re.escape(y_base)}_(\d{{8}}_\d{{6}}){re.escape(extension)}", latest)
    if not match:
        raise ValueError("Nem sikerult datumot kinyerni a fajlnevbol.")
    date_str = match.group(1)

    print(f"Fajl kivalasztva: {latest} (datum: {date_str})")
    return latest, date_str


def clean_text(value):
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def html_to_text(value):
    value = html.unescape(str(value or ""))
    value = re.sub(r"<[^>]+>", " ", value)
    return clean_text(value)


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
    if unit in {"db", "darab", "piece", "pieces", "pc", "pcs", "st", "stück", "stuk", "rl", "pa", "pk"}:
        return value, "db"
    return value, unit


def normalize_base_unit(unit):
    unit = clean_text(unit).lower()
    if unit in {"kg", "kilogram", "kilogramm"}:
        return 1000.0, "g"
    if unit in {"l", "liter", "litre", "literes"}:
        return 1000.0, "ml"
    if unit in {"db", "darab", "piece", "pieces", "pc", "pcs", "st", "stück", "stuk", "rl", "pa", "pk"}:
        return 1.0, "db"
    if unit in {"g", "gr", "gram", "gramm"}:
        return 1.0, "g"
    if unit in {"ml", "milliliter", "millilitre"}:
        return 1.0, "ml"
    return None, None


def parse_pack_from_text(text: str) -> Tuple[Optional[float], Optional[str]]:
    text = clean_text(text).lower().replace("×", "x")
    if not text:
        return None, None

    number_pattern = r"(?:\d{1,3}(?:[\s\xa0]\d{3})+|\d+)(?:[\.,]\d+)?"
    unit_pattern = r"kg|g|ml|liter(?:es)?|l|cl|db|darab|pcs|pc"
    multipack = re.findall(
        rf"(?<![a-záéíóöőúüű])({number_pattern})\s*x\s*({number_pattern})\s*({unit_pattern})\b",
        text,
        flags=re.IGNORECASE,
    )
    if multipack:
        count, value, unit = multipack[-1]
        total = number_from_text(count) * number_from_text(value)
        if total > 0:
            return normalize_unit(total, unit)

    matches = re.findall(
        rf"(?<![a-záéíóöőúüű])({number_pattern})\s*({unit_pattern})\b",
        text,
        flags=re.IGNORECASE,
    )
    if matches:
        value, unit = matches[-1]
        numeric_value = number_from_text(value)
        if numeric_value > 0:
            return normalize_unit(numeric_value, unit)

    return None, None


def provider_row(row):
    providers = parse_structured(row.get("productProvider"))
    if isinstance(providers, list) and providers and isinstance(providers[0], dict):
        selected_provider_id = clean_text(row.get("fetch_provider_id"))
        for provider in providers:
            if clean_text(provider.get("providerID")) == selected_provider_id:
                return provider
        return providers[0]
    return {}


def direct_name_provider_pack_conflict(row):
    name_step, name_unit = parse_pack_from_text(row.get("productName"))
    provider = provider_row(row)
    provider_step, provider_unit = parse_pack_from_text(provider.get("providerProductName"))
    if (
        name_step is None
        or provider_step is None
        or not name_unit
        or name_unit != provider_unit
        or provider_step <= 0
    ):
        return None, None
    if abs(name_step - provider_step) / max(name_step, provider_step) > 0.05:
        return name_step, name_unit
    return None, None


def package_step_from_unit_price(row):
    price = to_float(row.get("price"))
    unit_price = to_float(row.get("unitPrice"))
    unit_denominator, unit_type = normalize_base_unit(row.get("priceUnitType"))
    if price is None or unit_price is None or unit_price <= 0 or unit_denominator is None:
        return None, None
    step = price / unit_price * unit_denominator
    if step <= 0:
        return None, None

    rounded = round(step)
    if abs(step - rounded) <= max(0.35, abs(step) * 0.0015):
        step = float(rounded)
    if step <= 0:
        return None, None
    return step, unit_type


def package_step_from_provider(row):
    provider = provider_row(row)
    quantity = to_float(provider.get("packageQuantity"))
    base_unit = clean_text(provider.get("packageBaseUnit") or provider.get("unit"))
    if quantity is None or quantity <= 0 or not base_unit:
        return None, None

    base_unit_lower = base_unit.lower()
    unit_hint = clean_text(row.get("priceUnitType") or provider.get("unit")).lower()
    if unit_hint in {"l", "liter", "litre"} and base_unit_lower in {"g", "gr"}:
        return quantity, "ml"
    if unit_hint in {"kg", "kilogram"} and base_unit_lower in {"g", "gr"}:
        return quantity, "g"
    return normalize_unit(quantity, base_unit_lower)


def package_step(row):
    conflict_step, conflict_unit = direct_name_provider_pack_conflict(row)
    if conflict_step is not None and conflict_unit:
        return conflict_step, conflict_unit

    step, unit = package_step_from_unit_price(row)
    provider_step, provider_unit = package_step_from_provider(row)
    name_step, name_unit = parse_pack_from_text(row.get("productName"))

    # Ha a nev es a provider kiszerelese egyezik, de az egysegarbol szamolt
    # ertek nagyon eltavolodik toluk, akkor a forras egysegara hibas - a
    # nev/provider konszenzus nyer.
    if (
        step is not None
        and name_step is not None
        and provider_step is not None
        and name_unit == provider_unit
        and name_step > 0
        and provider_step > 0
        and abs(name_step - provider_step) / max(name_step, provider_step) <= 0.05
        and (unit != name_unit or abs(step - name_step) / name_step > 0.5)
    ):
        return name_step, name_unit

    if step is not None and unit:
        if (
            name_step is not None
            and name_unit == unit
            and name_step > 0
            and abs(step - name_step) / name_step <= 0.02
        ):
            return name_step, name_unit
        if (
            provider_step is not None
            and provider_unit == unit
            and provider_step > 0
            and abs(step - provider_step) / provider_step <= 0.02
        ):
            return provider_step, provider_unit
        return step, unit

    if provider_step is not None and provider_unit:
        return provider_step, provider_unit

    for field in ["displayUnit", "productDetails.displayUnit", "productName"]:
        step, unit = parse_pack_from_text(row.get(field))
        if step is not None and unit:
            return step, unit

    _, unit = normalize_base_unit(row.get("priceUnitType"))
    if unit == "g":
        return 1000.0, "g"
    if unit == "ml":
        return 1000.0, "ml"
    return 1.0, "db"


def price_fields(row):
    unit_price = to_float(row.get("price"))
    is_discounted = clean_text(row.get("isOffer")).lower() == "true"
    original_unit_price = to_float(row.get("originalPriceIfOffer"))

    if original_unit_price is not None and original_unit_price <= 0:
        original_unit_price = None
    if original_unit_price is not None and unit_price is not None and original_unit_price <= unit_price + 0.01:
        original_unit_price = None
    if original_unit_price is None:
        is_discounted = is_discounted or clean_text(row.get("isProductRokshDiscounted")).lower() == "true"

    return unit_price, is_discounted, original_unit_price


def secondary_fee(row):
    values = [row.get("depositFee")]
    provider = provider_row(row)
    values.append(provider.get("depositFee"))

    deposit_list = parse_structured(row.get("providerDepositProductDtoList"))
    if isinstance(deposit_list, list):
        for item in deposit_list:
            if isinstance(item, dict):
                values.extend(item.values())

    for value in values:
        numeric = to_float(value)
        if numeric is not None and numeric > 0:
            return numeric
    return None


def image_urls(row):
    values = []
    for field in ["mediaUrlL", "mediaUrlM", "mediaUrlS"]:
        value = clean_text(row.get(field))
        if value and value not in values:
            values.append(value)

    for field in ["galleryImageUrlList", "productMediaList"]:
        parsed = parse_structured(row.get(field))
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict):
                    for key in ["MediaUrlL", "mediaUrlL", "url", "imageUrl", "src"]:
                        value = clean_text(item.get(key))
                        if value and value not in values:
                            values.append(value)
                else:
                    value = clean_text(item)
                    if value and value not in values:
                        values.append(value)
    return ";".join(values)


def product_description(row):
    parts = []
    for field in [
        "productDetails.description",
        "description",
        "productDetails.preservedName",
        "productDetails.ingredients",
        "productDetails.allergenic",
        "productDetails.textualNutrition",
        "productDetails.storing",
        "productDetails.consumption",
        "legalDisclaimer",
    ]:
        text = html_to_text(row.get(field))
        if text and text not in parts:
            parts.append(text)
    return " | ".join(parts)


def categories(row):
    paths = clean_text(row.get("fetch_category_paths"))
    if paths:
        return paths
    path = clean_text(row.get("fetch_category_path"))
    if path:
        return path
    names = [clean_text(row.get("category.categoryName")), clean_text(row.get("category.progID"))]
    return " > ".join(item for item in names if item)


def availability(row):
    for field in ["available", "providerAvailable"]:
        value = clean_text(row.get(field)).lower()
        if value in {"false", "0", "no", "nem"}:
            return False
    return True


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
    for key, value in row.items():
        if any(token in key.lower() for token in ["gtin", "ean", "barcode"]):
            valid = valid_gtin(value)
            if valid:
                return valid
    return ""


input_file_name, input_date = read_latest_file("filtered_data")
output_file_name = generate_filename("normalized_data", input_date)

cnt_all = 0
cnt_discounted = 0
cnt_secondary = 0
cnt_barcode = 0
cnt_missing_step = 0

with open(input_file_name, mode="r", encoding="utf-8", newline="") as infile, open(
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
        code = barcode(row)

        if is_discounted:
            cnt_discounted += 1
        if secondary_unit_price is not None and secondary_unit_price > 0:
            cnt_secondary += 1
        if code:
            cnt_barcode += 1
        if unit_step is None or not unit_type:
            cnt_missing_step += 1
            unit_step, unit_type = 1.0, "db"

        writer.writerow(
            {
                "store_name": "Aldi",
                "store_product_id": clean_text(row.get("productID")),
                "product_name": clean_text(row.get("productName")),
                "brand_name": clean_text(row.get("brand")),
                "available": availability(row),
                "expected_restock": "",
                "barcode": code,
                "unit_price": round(unit_price, 3) if unit_price is not None else "",
                "unit_type": unit_type or "",
                "unit_step": round(float(unit_step), 3) if unit_step is not None else "",
                "is_discounted": is_discounted,
                "original_unit_price": round(original_unit_price, 3) if original_unit_price is not None else "",
                "secondary_unit_price": round(secondary_unit_price, 3)
                if secondary_unit_price is not None and secondary_unit_price > 0
                else "",
                "secondary_unit_type": "db" if secondary_unit_price is not None and secondary_unit_price > 0 else "",
                "secondary_unit_step": 1.0 if secondary_unit_price is not None and secondary_unit_price > 0 else "",
                "image_urls": image_urls(row),
                "description": product_description(row),
                "categories": categories(row),
            }
        )

print(f"{cnt_all} Aldi sor normalizalva: {output_file_name}")
print(f"{cnt_discounted} akcios sor")
print(f"{cnt_secondary} sor visszavaltasi/betetdijjal")
print(f"{cnt_barcode} sor ervenyes vonalkoddal")
print(f"{cnt_missing_step} sor fallback kiszerelessel")
