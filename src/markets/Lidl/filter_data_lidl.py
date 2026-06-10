import csv
import glob
import os
import re

import pandas as pd


csv.field_size_limit(1024 * 1024 * 1024)

MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "lidl"


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
    "code",
    "resultClass",
    "type",
    "label",
    "fetch_category_id",
    "fetch_category_name",
    "fetch_category_url",
    "search_offset",
    "search_rank",
    "gridbox.country",
    "gridbox.sequence",
    "gridbox.data.erpNumber",
    "gridbox.data.productId",
    "gridbox.data.itemId",
    "gridbox.data.productType",
    "gridbox.data.title",
    "gridbox.data.fullTitle",
    "gridbox.data.canonicalPath",
    "gridbox.data.canonicalUrl",
    "gridbox.data.category",
    "gridbox.data.brand.name",
    "gridbox.data.brand.showBrand",
    "gridbox.data.keyfacts.title",
    "gridbox.data.keyfacts.fullTitle",
    "gridbox.data.keyfacts.description",
    "gridbox.data.keyfacts.wonCategoryPrimary",
    "gridbox.data.keyfacts.wonCategoryPrimaryPath",
    "gridbox.data.price.price",
    "gridbox.data.price.oldPrice",
    "gridbox.data.price.basePrice.text",
    "gridbox.data.price.discount.discountText",
    "gridbox.data.price.discount.percentageDiscount",
    "gridbox.data.price.discount.deletedPrice",
    "gridbox.data.price.priceTheme",
    "gridbox.data.price.specialTaxes",
    "gridbox.data.lidlPlus",
    "gridbox.data.ribbons",
    "gridbox.data.flashSales",
    "gridbox.data.dealOfDay.active",
    "gridbox.data.stockAvailability.availabilityIndicator",
    "gridbox.data.stockAvailability.badgeInfo.badges",
    "gridbox.data.stockAvailability.onlineAvailable",
    "gridbox.data.stockAvailability.minOrderableQuantity",
    "gridbox.data.image",
    "gridbox.data.imageList",
    "gridbox.data.image_V1",
    "gridbox.data.imageList_V1",
    "gridbox.data.ians",
    "gridbox.data.gs1Attributes",
    "gridbox.data.productOrigin",
    "gridbox.data.ageRestriction",
    "gridbox.data.multipack",
    "gridbox.data.regionsPrices",
]


input_file_name, input_date = read_latest_file("all_data")
df = pd.read_csv(input_file_name, dtype=str, keep_default_na=False)

df = df[[column for column in important_columns if column in df.columns]]
output_file_name = generate_filename("filtered_data", input_date)
df.to_csv(output_file_name, index=False)

print(f"Lényeges Lidl oszlopokat tartalmazó fájl mentve ide: {output_file_name}")
