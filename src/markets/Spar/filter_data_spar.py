import pandas as pd

# Fájl beolvasása
input_file = "osszes_termek.csv"
output_file = "lenyeges_oszlopok.csv"

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
df = pd.read_csv(input_file)

# Nem lényeges oszlopok eltávolítása (csak ha valóban szerepel a táblázatban)
df = df.drop(columns=[col for col in irrelevant_columns if col in df.columns])

# Eredmény mentése új CSV fájlba
df.to_csv(output_file, index=False)

print(f"Lényeges oszlopokat tartalmazó fájl mentve ide: {output_file}")
