import pandas as pd
import os
import glob
from datetime import datetime
import re

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
        raise FileNotFoundError(f"Nincs fájl: {pattern}")

    # Legújabb fájl kiválasztása
    latest = max(candidates, key=os.path.getmtime)

    # Dátum/idő kivonása a fájlnévből
    match = re.search(rf"{re.escape(x)}_{re.escape(y_base)}_(\d{{8}}_\d{{6}}){re.escape(extension)}", latest)
    if not match:
        raise ValueError("Nem sikerült dátumot kinyerni a fájlnévből.")
    date_str = match.group(1)

    print(f"Fájl kiválasztva: {latest} (dátum: {date_str})")
    return latest, date_str

# Fájl beolvasása
input_file = "all_data"
output_file = "filtered_data"

# Nem lényeges oszlopok listája
irrelevant_columns = [
    "advertising_info", "caffeine_info", "allowed_delivery_methods", "available_times",
    "deposit", "dietary_preferences", "fulfillment_lead_time", "is_cutlery",
    "is_no_contact_delivery_allowed", "is_wolt_plus_only", "lowest_price",
    "lowest_price_v2", "min_quantity_per_purchase", "options",
    "original_price", "item_price_discount_validity_period", "return_policy",
    "should_display_purchasable_balance", "unit_price", "variant",
    "vat_category_code", "external_compliance_link", "consent_info.ask_consent",
    "consent_info.blur_image", "disabled_info", "unit_price.original_price",
    "sell_by_weight_config", "deposit.label"
]

# CSV beolvasása
input_file_name, input_date = read_latest_file(input_file)
df = pd.read_csv(input_file_name)

# Nem lényeges oszlopok eltávolítása (csak ha valóban szerepel a táblázatban)
df = df.drop(columns=[col for col in irrelevant_columns if col in df.columns])

output_file_name = generate_filename(output_file, input_date)
# Eredmény mentése új CSV fájlba
df.to_csv(output_file_name, index=False)

print(f"Lényeges oszlopokat tartalmazó fájl mentve ide: {output_file_name}")
