import csv
import glob
import os
import re

import pandas as pd


csv.field_size_limit(1024 * 1024 * 1024)

MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "coop"


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


important_columns = [
    "id",
    "name",
    "slug",
    "permalink",
    "sku",
    "type",
    "parent",
    "variation",
    "short_description",
    "description",
    "on_sale",
    "prices.price",
    "prices.regular_price",
    "prices.sale_price",
    "prices.currency_code",
    "prices.currency_symbol",
    "prices.currency_minor_unit",
    "price_html",
    "average_rating",
    "review_count",
    "images",
    "categories",
    "tags",
    "brands",
    "attributes",
    "is_purchasable",
    "is_in_stock",
    "is_on_backorder",
    "low_stock_remaining",
    "stock_availability.text",
    "stock_availability.class",
    "sold_individually",
    "weight",
    "formatted_weight",
    "dimensions.length",
    "dimensions.width",
    "dimensions.height",
    "formatted_dimensions",
    "add_to_cart.text",
    "add_to_cart.minimum",
    "add_to_cart.maximum",
    "add_to_cart.multiple_of",
    "fetch_category_ids",
    "fetch_category_names",
    "fetch_category_paths",
    "product_category_paths",
]


input_file_name, input_date = read_latest_file("all_data")
df = pd.read_csv(input_file_name, dtype=str, keep_default_na=False)

df = df[[column for column in important_columns if column in df.columns]]
output_file_name = generate_filename("filtered_data", input_date)
df.to_csv(output_file_name, index=False)

print(f"Lényeges Coop oszlopokat tartalmazó fájl mentve ide: {output_file_name}")
