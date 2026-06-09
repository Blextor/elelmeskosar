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
    "__typename",
    "id",
    "baseProductId",
    "tpnb",
    "tpnc",
    "gtin",
    "title",
    "brandName",
    "shortDescription",
    "defaultImageUrl",
    "superDepartmentName",
    "departmentName",
    "aisleName",
    "shelfName",
    "displayType",
    "productType",
    "averageWeight",
    "isForSale",
    "isNew",
    "status",
    "price.actual",
    "price.unitPrice",
    "price.unitOfMeasure",
    "promotions",
    "details_enriched",
    "details.packSize",
    "details.packSize.value",
    "details.packSize.units",
    "details.netContents",
    "details.drainedWeight",
    "details.boxContents",
    "details.storage",
    "details.ingredients",
    "details.features",
    "details.otherInformation",
    "catchWeightList",
    "charges",
    "fetch_category_names",
    "fetch_category_paths",
    "fetch_category_facets",
]

df = df[[column for column in important_columns if column in df.columns]]
output_file_name = generate_filename("filtered_data", input_date)
df.to_csv(output_file_name, index=False)

print(f"Lenyeges Tesco oszlopokat tartalmazo fajl mentve ide: {output_file_name}")
