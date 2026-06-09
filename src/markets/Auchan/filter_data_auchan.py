import glob
import os
import re

import pandas as pd


MAIN_FOLDER = "./../../../data/markets_data/"


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


input_file_name, input_date = read_latest_file("all_data")
df = pd.read_csv(input_file_name, dtype=str, keep_default_na=False)

important_columns = [
    "id",
    "categoryId",
    "categoryName",
    "brandName",
    "eancode",
    "isNewProduct",
    "adultsOnly",
    "ageConfirmed",
    "isNonFood",
    "type",
    "stockInfos",
    "shipmentDays",
    "categories",
    "inCategories",
    "fetch_category_id",
    "fetch_category_name",
    "fetch_category_path",
    "fetch_category_ids",
    "fetch_category_names",
    "fetch_category_paths",
    "selectedVariant.id",
    "selectedVariant.name",
    "selectedVariant.brandName",
    "selectedVariant.sku",
    "selectedVariant.unit",
    "selectedVariant.eanCode",
    "selectedVariant.status",
    "selectedVariant.aided",
    "selectedVariant.price.net",
    "selectedVariant.price.gross",
    "selectedVariant.price.netDiscounted",
    "selectedVariant.price.grossDiscounted",
    "selectedVariant.price.discountPercentage",
    "selectedVariant.price.discountDisplayPercentage",
    "selectedVariant.price.isDiscounted",
    "selectedVariant.packageInfo.packageUnit",
    "selectedVariant.packageInfo.packageSize",
    "selectedVariant.packageInfo.unitPrice.net",
    "selectedVariant.packageInfo.unitPrice.gross",
    "selectedVariant.packageInfo.unitPrice.netDiscounted",
    "selectedVariant.packageInfo.unitPrice.grossDiscounted",
    "selectedVariant.packageInfo.unitPrice.isDiscounted",
    "selectedVariant.loose.loose",
    "selectedVariant.loose.weightPerPiece",
    "selectedVariant.cartInfo.quantitySteps",
    "selectedVariant.cartInfo.quantityStepSize",
    "selectedVariant.cartInfo.availability",
    "selectedVariant.roll.name",
    "selectedVariant.roll.type",
    "selectedVariant.roll.quantity.quantity",
    "selectedVariant.roll.quantity.type",
    "selectedVariant.roll.price.gross",
    "selectedVariant.media.images",
    "selectedVariant.media.mainImage",
    "selectedVariant.media.listImage",
    "selectedVariant.details",
    "selectedVariant.isInVirtualStock",
    "selectedVariant.isLoyaltyPriceValid",
    "selectedVariant.isOfflinePromotion",
    "defaultVariant.id",
    "defaultVariant.name",
    "defaultVariant.eanCode",
    "defaultVariant.price.gross",
    "defaultVariant.price.grossDiscounted",
    "defaultVariant.packageInfo.packageUnit",
    "defaultVariant.packageInfo.packageSize",
]

df = df[[column for column in important_columns if column in df.columns]]
output_file_name = generate_filename("filtered_data", input_date)
df.to_csv(output_file_name, index=False)

print(f"Lenyeges Auchan oszlopokat tartalmazo fajl mentve ide: {output_file_name}")
