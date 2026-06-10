import csv
import glob
import os
import re

import pandas as pd


csv.field_size_limit(1024 * 1024 * 1024)

MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "penny"


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


important_columns = [
    "productID",
    "productName",
    "brand",
    "available",
    "providerAvailable",
    "sEOName",
    "categorySEOName",
    "categoryID",
    "category.categoryName",
    "category.progID",
    "category.level",
    "category.url",
    "price",
    "minPrice",
    "unitPrice",
    "minUnitPrice",
    "priceUnitType",
    "minWeightStep",
    "maxWeightStep",
    "depositFee",
    "isBulk",
    "selectedShopIsBulk",
    "displayUnit",
    "secondaryUnit",
    "secondaryUnitPrice",
    "isOffer",
    "originalPriceIfOffer",
    "originalUnitPriceIfOffer",
    "originalSecondaryUnitPriceIfOffer",
    "originalSecondaryUnitIfOffer",
    "offerValidTo",
    "rokshDiscountLevel",
    "rokshDiscountPrice",
    "rokshDiscountBasketValue",
    "isProductRokshDiscounted",
    "isOneProductForFree",
    "description",
    "legalDisclaimer",
    "manufacturer",
    "providerOrderNumber",
    "mediaUrlS",
    "mediaUrlM",
    "mediaUrlL",
    "galleryImageUrlList",
    "productMediaList",
    "icons",
    "productProvider",
    "providerDepositProductDtoList",
    "productProviderID",
    "productDetails.allergenic",
    "productDetails.textualNutrition",
    "productDetails.ingredients",
    "productDetails.storing",
    "productDetails.consumption",
    "productDetails.description",
    "productDetails.packageType",
    "productDetails.producerAddress",
    "productDetails.supplierAddress",
    "productDetails.manufacturer",
    "productDetails.originCountry",
    "productDetails.preservedName",
    "productDetails.attributes",
    "productDetails.displayUnit",
    "productDetails.secondaryUnit",
    "productDetails.secondaryUnitPrice",
    "productDetails.promotion",
    "fetch_category_id",
    "fetch_category_name",
    "fetch_category_prog_id",
    "fetch_category_path",
    "fetch_category_level",
    "fetch_requested_category_id",
    "fetch_requested_category_name",
    "fetch_requested_category_prog_id",
    "fetch_requested_category_path",
    "fetch_page",
    "fetch_rank",
    "fetch_provider_code",
    "fetch_provider_id",
    "fetch_provider_route",
    "fetch_categories",
    "fetch_category_paths",
]


input_file_name, input_date = read_latest_file("all_data")
df = pd.read_csv(input_file_name, dtype=str, keep_default_na=False)

df = df[[column for column in important_columns if column in df.columns]]
output_file_name = generate_filename("filtered_data", input_date)
df.to_csv(output_file_name, index=False)

print(f"Lenyeges Penny oszlopokat tartalmazo fajl mentve ide: {output_file_name}")
