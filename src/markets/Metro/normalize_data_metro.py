import ast
import csv
import glob
import json
import os
import re
from typing import Optional, Tuple


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

price_tier_fields = [
    "store_name",
    "store_product_id",
    "product_name",
    "tier_min_quantity",
    "tier_final_gross_price",
    "tier_final_net_price",
    "tier_base_unit_price",
    "tier_base_unit",
    "tier_base_content_units",
    "tier_discount_value",
    "product_unit_step",
    "product_unit_type",
    "tier_label",
    "tier_valid_from",
    "tier_valid_to",
    "tier_source",
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


def read_latest_optional_file(y_base: str, extension=".csv"):
    x = get_current_dir_name()
    pattern = f"{MAIN_FOLDER}{x}_{y_base}_*{extension}"
    candidates = glob.glob(pattern)
    if not candidates:
        return None, None

    latest = max(candidates, key=os.path.getmtime)
    match = re.search(rf"{re.escape(x)}_{re.escape(y_base)}_(\d{{8}}_\d{{6}}){re.escape(extension)}", latest)
    return (latest, match.group(1) if match else None)


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
    if value in {"true", "1", "yes", "available", "availableforsale"}:
        return True
    if value in {"false", "0", "no", "unavailable", "not_available", "delisted"}:
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


def nested_value(data, path):
    current = data
    for part in path:
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


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
    if unit in {"db", "darab", "piece", "pieces", "pc", "pcs", "pce", "st", "unit", "units", "ea"}:
        return value, "db"
    return value, unit


def parse_pack_from_text(text: str) -> Tuple[Optional[float], Optional[str]]:
    text = clean_text(text).lower().replace("×", "x")
    if not text:
        return None, None

    multipack = re.findall(
        r"(\d+(?:[\.,]\d+)?)\s*x\s*(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|pcs|pc|darab)",
        text,
        flags=re.IGNORECASE,
    )
    if multipack:
        count, value, unit = multipack[-1]
        total = float(count.replace(",", ".")) * float(value.replace(",", "."))
        if total > 0:
            return normalize_unit(total, unit)

    matches = re.findall(r"(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|cl|db|pcs|pc|darab)\b", text, flags=re.IGNORECASE)
    if matches:
        for value, unit in reversed(matches):
            numeric_value = float(value.replace(",", "."))
            if numeric_value > 0:
                return normalize_unit(numeric_value, unit)

    return None, None


def first_float(row, fields):
    for field in fields:
        value = to_float(row.get(field))
        if value is not None:
            return value
    return None


def has_promotion(row):
    adjustments = parse_structured(row.get("price.appliedAdjustments"))
    if isinstance(adjustments, list):
        values = {clean_text(value).lower() for value in adjustments}
        if values.intersection({"promotion", "dnr"}):
            return True

    for key, value in row.items():
        if key.startswith("price.promotionLabels.") and clean_text(value):
            return True
    return False


def explicit_original_price(row):
    direct = first_float(row, ["price.grossStrikeThrough"])
    if direct is not None:
        return direct

    strike = parse_structured(row.get("price.strikeThrough"))
    if isinstance(strike, dict):
        candidates = [
            strike.get("grossPrice"),
            strike.get("gross"),
            strike.get("amount"),
        ]
        for candidate in candidates:
            value = to_float(candidate)
            if value is not None:
                return value
    return None


def price_fields(row):
    unit_price = first_float(
        row,
        [
            "price.finalPricesInfo.articleGross",
            "price.finalPricesInfo.articleWithTaxesGross",
            "price.finalPricesInfo.singleItemGross",
            "price.listGrossPrice",
            "price.grossPrice",
            "price.finalPrice",
            "search_price",
        ],
    )
    secondary_unit_price = first_float(row, ["price.finalPricesInfo.emptiesGross"])
    original_unit_price = explicit_original_price(row)
    is_discounted = has_promotion(row) or (
        original_unit_price is not None and unit_price is not None and original_unit_price > unit_price + 0.01
    )
    return unit_price, is_discounted, original_unit_price, secondary_unit_price


def package_step(row):
    net_weight = to_float(row.get("bundle.contentData.netPieceWeight.value"))
    net_weight_unit = clean_text(row.get("bundle.contentData.netPieceWeight.uom"))
    net_value, net_unit = normalize_unit(net_weight, net_weight_unit)

    base_content = to_float(row.get("bundle.basePriceContent"))
    base_unit = clean_text(row.get("bundle.basePriceContentMeasureUnit"))
    value, unit = normalize_unit(base_content, base_unit)
    if value is not None and value > 0 and unit:
        if unit == "g" and value < 1 and net_value is not None and net_value > value and net_unit == "g":
            return net_value, net_unit
        return value, unit

    if net_value is not None and net_value > 0 and net_unit:
        return net_value, net_unit

    weight = to_float(row.get("bundle.weightPerPiece.value"))
    weight_unit = clean_text(row.get("bundle.weightPerPiece.uom"))
    value, unit = normalize_unit(weight, weight_unit)
    if value is not None and value > 0 and unit:
        return value, unit

    for field in ["bundle.description", "variant.description"]:
        value, unit = parse_pack_from_text(row.get(field, ""))
        if value is not None and value > 0 and unit:
            return value, unit

    bundle_size = to_float(row.get("bundle.bundleSize"))
    if bundle_size is not None and bundle_size > 0:
        return bundle_size, "db"

    return 1.0, "db"


def first_barcode_value(value):
    parsed = parse_structured(value)
    if isinstance(parsed, list):
        for item in parsed:
            if isinstance(item, dict):
                for key in ["gtin", "ean", "value", "code", "id"]:
                    candidate = clean_text(item.get(key))
                    if candidate:
                        return candidate
            else:
                candidate = clean_text(item)
                if candidate:
                    return candidate
    if isinstance(parsed, dict):
        for key in ["gtin", "ean", "value", "code", "id"]:
            candidate = clean_text(parsed.get(key))
            if candidate:
                return candidate
    value = clean_text(value)
    return value if value and value not in {"[]", "{}"} else ""


def barcode(row):
    for field in ["bundle.eanNumber", "bundle.gtins"]:
        value = first_barcode_value(row.get(field))
        if value:
            return value
    return ""


def product_facts_barcodes():
    facts_file, facts_date = read_latest_optional_file("product_facts")
    if not facts_file:
        return {}

    result = {}
    with open(facts_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            product_id = clean_text(row.get("store_product_id"))
            fact_barcode = clean_text(row.get("barcode"))
            if product_id and fact_barcode:
                result[product_id] = fact_barcode

    print(f"Metro PDF adatlap vonalkodok betoltve: {len(result)} ({facts_file}, datum: {facts_date})")
    return result


def image_urls(row):
    values = []
    for field in [
        "bundle.imageUrl",
        "bundle.imageUrlL",
        "bundle.imageUrlS",
        "variant.imageUrl",
        "variant.imageUrlL",
        "variant.imageUrlS",
    ]:
        value = clean_text(row.get(field))
        if value and value not in values:
            values.append(value)
    return ";".join(values)


def category_path_from_field(value):
    parsed = parse_structured(value)
    paths = []
    if isinstance(parsed, list):
        for item in parsed:
            if not isinstance(item, dict):
                continue
            levels = item.get("levels")
            if isinstance(levels, list):
                path = " > ".join(clean_text(level.get("displayName") or level.get("id")) for level in levels if isinstance(level, dict))
            else:
                path = clean_text(item.get("name"))
            if path and path not in paths:
                paths.append(path)
    return paths


def categories(row):
    paths = category_path_from_field(row.get("bundle.categories"))
    if not paths:
        paths = category_path_from_field(row.get("variant.categories"))
    return "|".join(paths)


def description(row):
    parts = [
        clean_text(row.get("bundle.longDescription")),
        clean_text(row.get("bundle.variantText")),
    ]
    base_content = clean_text(row.get("bundle.basePriceContent"))
    base_unit = clean_text(row.get("bundle.basePriceContentMeasureUnit"))
    if base_content and base_unit:
        parts.append(f"Kiszerelés: {base_content} {base_unit}")
    return " | ".join(part for part in parts if part)


def availability(row):
    delisted = to_bool(row.get("store.delisted"))
    if delisted is True:
        return False

    for field in ["search_is_available", "customer_buyable", "price.valid"]:
        value = to_bool(row.get(field))
        if value is not None:
            return value

    status = clean_text(row.get("bundle.availability") or row.get("variant.availability")).lower()
    if status:
        return status in {"available", "available_for_sale"}
    return True


def dnr_validity(row, summary):
    valid_from = clean_text(summary.get("start"))
    valid_to = clean_text(summary.get("end"))
    if valid_from or valid_to:
        return valid_from, valid_to

    # A summaryDnrInfo-ban a start/end gyakran ures, a reszletes dnrInfo
    # bejegyzesekben viszont kitoltott - nev alapjan parositunk.
    dnr_info = parse_structured(row.get("price.dnrInfo"))
    if not isinstance(dnr_info, dict):
        return "", ""
    entries = [entry for entry in dnr_info.values() if isinstance(entry, dict)]
    summary_name = clean_text(summary.get("name"))
    matching = [entry for entry in entries if clean_text(entry.get("name")) == summary_name]
    if not matching and len(entries) == 1:
        matching = entries
    if not matching:
        return "", ""
    return clean_text(matching[0].get("start")), clean_text(matching[0].get("end"))


def price_tier_rows(row, unit_step, unit_type):
    summary = parse_structured(row.get("price.summaryDnrInfo"))
    if not isinstance(summary, dict):
        return []

    levels = summary.get("levels")
    if not isinstance(levels, dict) or len(levels) <= 1:
        return []

    label = clean_text(summary.get("customerLabel") or summary.get("name"))
    valid_from, valid_to = dnr_validity(row, summary)
    tiers = []
    for level_key, level in levels.items():
        if not isinstance(level, dict):
            continue

        min_quantity = to_float(level_key)
        gross_price = to_float(level.get("finalSingleGrossPrice"))
        net_price = to_float(level.get("finalSingleNetPrice"))
        base_price = nested_value(level, ["basePrice", "pricePerUnit", "grossPrice"])
        base_unit = nested_value(level, ["basePrice", "unit"])
        base_content_units = nested_value(level, ["basePrice", "contentUnits"])

        tiers.append(
            {
                "store_name": "Metro",
                "store_product_id": clean_text(
                    row.get("bundle_id")
                    or row.get("bundle.bundleId.bettyBundleId")
                    or row.get("variant_id")
                    or row.get("search_result_id")
                ),
                "product_name": clean_text(row.get("bundle.description") or row.get("variant.description")),
                "tier_min_quantity": min_quantity if min_quantity is not None else clean_text(level_key),
                "tier_final_gross_price": round(gross_price, 3) if gross_price is not None else "",
                "tier_final_net_price": round(net_price, 3) if net_price is not None else "",
                "tier_base_unit_price": round(to_float(base_price), 3) if to_float(base_price) is not None else "",
                "tier_base_unit": clean_text(base_unit),
                "tier_base_content_units": clean_text(base_content_units),
                "tier_discount_value": clean_text(level.get("value")),
                "product_unit_step": round(float(unit_step), 3) if unit_step is not None else "",
                "product_unit_type": unit_type or "",
                "tier_label": label,
                "tier_valid_from": valid_from,
                "tier_valid_to": valid_to,
                "tier_source": "price.summaryDnrInfo",
            }
        )

    return tiers


input_file_name, input_date = read_latest_file("filtered_data")
output_file_name = generate_filename("normalized_data", input_date)
price_tiers_file_name = generate_filename("price_tiers", input_date)
fact_barcodes = product_facts_barcodes()

cnt_all = 0
cnt_discounted = 0
cnt_secondary = 0
cnt_price_tiers = 0

with open(input_file_name, mode="r", encoding="utf-8-sig", newline="") as infile, open(
    output_file_name, mode="w", encoding="utf-8", newline=""
) as outfile:
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=output_fields)
    writer.writeheader()
    has_price_tier_source = "price.summaryDnrInfo" in (reader.fieldnames or [])
    tiers_outfile = None
    tiers_writer = None
    if has_price_tier_source:
        tiers_outfile = open(price_tiers_file_name, mode="w", encoding="utf-8", newline="")
        tiers_writer = csv.DictWriter(tiers_outfile, fieldnames=price_tier_fields)
        tiers_writer.writeheader()

    try:
        for row in reader:
            cnt_all += 1
            unit_price, is_discounted, original_unit_price, secondary_unit_price = price_fields(row)
            unit_step, unit_type = package_step(row)
            if is_discounted:
                cnt_discounted += 1
            if secondary_unit_price is not None and secondary_unit_price > 0:
                cnt_secondary += 1

            if tiers_writer is not None:
                tiers = price_tier_rows(row, unit_step, unit_type)
                for tier in tiers:
                    tiers_writer.writerow(tier)
                    cnt_price_tiers += 1
            store_product_id = clean_text(row.get("bundle_id") or row.get("bundle.bundleId.bettyBundleId") or row.get("variant_id") or row.get("search_result_id"))
            row_barcode = barcode(row) or fact_barcodes.get(store_product_id, "")

            writer.writerow(
                {
                    "store_name": "Metro",
                    "store_product_id": store_product_id,
                    "product_name": clean_text(row.get("bundle.description") or row.get("variant.description")),
                    "brand_name": empty_to_none(row.get("bundle.brandName") or row.get("article.brandName")),
                    "available": availability(row),
                    "expected_restock": "",
                    "barcode": row_barcode,
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
    finally:
        if tiers_outfile is not None:
            tiers_outfile.close()

print(f"{cnt_all} Metro sor normalizalva")
print(f"{cnt_discounted} akcios/promocios sor")
print(f"{cnt_secondary} sor masodlagos dijjal")
print(f"Normalizalt fajl mentve ide: {output_file_name}")
if has_price_tier_source:
    print(f"{cnt_price_tiers} Metro mennyisegi arsav sor")
    print(f"Metro mennyisegi arsav fajl mentve ide: {price_tiers_file_name}")
else:
    print("=" * 72)
    print("FIGYELEM: a bemeneti fajl nem tartalmaz price.summaryDnrInfo mezot,")
    print("ezert NEM keszult uj mennyisegi arsav (price_tiers) fajl!")
    print("A korabbi arsav fajl elavulhat - ellenorizd a letoltest (get_all_data_metro.py).")
    print("=" * 72)
