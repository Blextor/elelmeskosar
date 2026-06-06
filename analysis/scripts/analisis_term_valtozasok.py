import pandas as pd
import os
from collections import defaultdict

# Fájlok betöltése
workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
file_new = os.path.join(workspace, r'data/markets_data/spar_normalized_data_20260417_021319.csv')
file_old = os.path.join(workspace, r'data/markets_data/spar_normalized_data_20251003_070148.csv')

df_new = pd.read_csv(file_new, encoding='utf-8')
df_old = pd.read_csv(file_old, encoding='utf-8')

print("=" * 80)
print("ADATOK BETÖLTÉSE")
print("=" * 80)
print(f"Új fájl (2026-04-17): {len(df_new)} termék")
print(f"Régi fájl (2025-10-03): {len(df_old)} termék")
print()

# Tisztítás - üres sorok eltávolítása
df_new_clean = df_new.dropna(subset=['product_name']).reset_index(drop=True)
df_old_clean = df_old.dropna(subset=['product_name']).reset_index(drop=True)

print(f"Új fájl (tisztítva): {len(df_new_clean)} termék")
print(f"Régi fájl (tisztítva): {len(df_old_clean)} termék")
print()

# ============================================================================
# 1. TERMÉKNÉV ALAPJÁN ÖSSZEHASONLÍTÁS
# ============================================================================
print("=" * 80)
print("1. TERMÉKNÉV ALAPJÁN ÖSSZEHASONLÍTÁS")
print("=" * 80)

old_names = set(df_old_clean['product_name'].str.strip().str.lower())
new_names = set(df_new_clean['product_name'].str.strip().str.lower())

common_names = old_names & new_names
only_new_names = new_names - old_names
only_old_names = old_names - new_names

print(f"Közös terméknevek: {len(common_names)}")
print(f"Csak az új fájlban: {len(only_new_names)}")
print(f"Csak a régi fájlban: {len(only_old_names)}")
print()

if only_new_names:
    print("Új termékek (első 10):")
    for name in list(only_new_names)[:10]:
        print(f"  - {name}")
    print()

if only_old_names:
    print("Eltűnt termékek (első 10):")
    for name in list(only_old_names)[:10]:
        print(f"  - {name}")
    print()

# ============================================================================
# 2. VONALKÓD ALAPJÁN ÖSSZEHASONLÍTÁS
# ============================================================================
print("=" * 80)
print("2. VONALKÓD ALAPJÁN ÖSSZEHASONLÍTÁS")
print("=" * 80)

df_new_with_barcode = df_new_clean[df_new_clean['barcode'].notna() & (df_new_clean['barcode'] != '')]
df_old_with_barcode = df_old_clean[df_old_clean['barcode'].notna() & (df_old_clean['barcode'] != '')]

old_barcodes = set(df_old_with_barcode['barcode'].astype(str).str.strip())
new_barcodes = set(df_new_with_barcode['barcode'].astype(str).str.strip())

common_barcodes = old_barcodes & new_barcodes
only_new_barcodes = new_barcodes - old_barcodes
only_old_barcodes = old_barcodes - new_barcodes

print(f"Termékek vonalkóddal - Régi: {len(df_old_with_barcode)}, Új: {len(df_new_with_barcode)}")
print(f"Közös vonalkódok: {len(common_barcodes)}")
print(f"Csak új vonalkódok: {len(only_new_barcodes)}")
print(f"Csak régi vonalkódok: {len(only_old_barcodes)}")
print()

# ============================================================================
# 3. KÉPEK ALAPJÁN ÖSSZEHASONLÍTÁS
# ============================================================================
print("=" * 80)
print("3. KÉPEK ALAPJÁN ÖSSZEHASONLÍTÁS")
print("=" * 80)

df_new_with_image = df_new_clean[df_new_clean['image_urls'].notna() & (df_new_clean['image_urls'] != '')]
df_old_with_image = df_old_clean[df_old_clean['image_urls'].notna() & (df_old_clean['image_urls'] != '')]

old_images = set(df_old_with_image['image_urls'].astype(str).str.strip())
new_images = set(df_new_with_image['image_urls'].astype(str).str.strip())

common_images = old_images & new_images
only_new_images = new_images - old_images
only_old_images = old_images - new_images

print(f"Termékek képekkel - Régi: {len(df_old_with_image)}, Új: {len(df_new_with_image)}")
print(f"Közös képek: {len(common_images)}")
print(f"Csak új képek: {len(only_new_images)}")
print(f"Csak régi képek: {len(only_old_images)}")
print()

# ============================================================================
# 4. STORE_PRODUCT_ID ALAPJÁN
# ============================================================================
print("=" * 80)
print("4. STORE_PRODUCT_ID ALAPJÁN ÖSSZEHASONLÍTÁS")
print("=" * 80)

old_ids = set(df_old_clean['store_product_id'].astype(str).str.strip())
new_ids = set(df_new_clean['store_product_id'].astype(str).str.strip())

common_ids = old_ids & new_ids
only_new_ids = new_ids - old_ids
only_old_ids = old_ids - new_ids

print(f"Közös product ID-k: {len(common_ids)}")
print(f"Csak új ID-k: {len(only_new_ids)}")
print(f"Csak régi ID-k: {len(only_old_ids)}")
print()

# ============================================================================
# 5. KÖZÖS TERMÉKNEVEK - ID VÁLTOZÁS VIZSGÁLATA
# ============================================================================
print("=" * 80)
print("5. KÖZÖS TERMÉKNEVEKNÉL AZ ID VÁLTOZÁS")
print("=" * 80)

id_changed = 0
id_same = 0
price_changed = 0
category_changed = 0

for common_name in common_names:
    name_lower = common_name.strip().lower()
    old_rows = df_old_clean[df_old_clean['product_name'].str.lower() == name_lower]
    new_rows = df_new_clean[df_new_clean['product_name'].str.lower() == name_lower]
    
    # Ha több azonos nevű termék van, csak az elsőt vesszük
    if len(old_rows) > 0 and len(new_rows) > 0:
        old_row = old_rows.iloc[0]
        new_row = new_rows.iloc[0]
        
        if old_row['store_product_id'] != new_row['store_product_id']:
            id_changed += 1
        else:
            id_same += 1
        
        if old_row['unit_price'] != new_row['unit_price']:
            price_changed += 1
        
        if old_row['categories'] != new_row['categories']:
            category_changed += 1

print(f"Közös termékek között:")
print(f"  - ID változott: {id_changed}")
print(f"  - ID maradt ugyanaz: {id_same}")
print(f"  - Ár változott: {price_changed}")
print(f"  - Kategória változott: {category_changed}")
print()

# ============================================================================
# 6. DUPLIKÁLT TERMÉKEK (TÖBB AZONOS NÉV UGYANABBAN A FÁJLBAN)
# ============================================================================
print("=" * 80)
print("6. DUPLIKÁLT TERMÉKEK (AZONOS NÉV)")
print("=" * 80)

old_duplicates = df_old_clean['product_name'].value_counts()
new_duplicates = df_new_clean['product_name'].value_counts()

old_dups_list = old_duplicates[old_duplicates > 1]
new_dups_list = new_duplicates[new_duplicates > 1]

print(f"Régi fájlban duplikált termékek: {len(old_dups_list)}")
if len(old_dups_list) > 0:
    print("  Példák:")
    for name, count in old_dups_list.head(5).items():
        print(f"    - '{name}': {count}x")

print()
print(f"Új fájlban duplikált termékek: {len(new_dups_list)}")
if len(new_dups_list) > 0:
    print("  Példák:")
    for name, count in new_dups_list.head(5).items():
        print(f"    - '{name}': {count}x")
print()

# ============================================================================
# 7. ELSŐ TERMÉK RÉSZLETES ELEMZÉSE
# ============================================================================
print("=" * 80)
print("7. ELSŐ TERMÉK (Golden alma lédig) RÉSZLETES ELEMZÉSE")
print("=" * 80)

first_old = df_old_clean[df_old_clean['product_name'].str.contains('Golden alma', regex=False, na=False, case=False)]
first_new = df_new_clean[df_new_clean['product_name'].str.contains('Golden alma', regex=False, na=False, case=False)]

if len(first_old) > 0:
    print("\nRÉGI FÁJL:")
    for col in first_old.columns:
        print(f"  {col}: {first_old.iloc[0][col]}")

if len(first_new) > 0:
    print("\nÚJ FÁJL:")
    for col in first_new.columns:
        print(f"  {col}: {first_new.iloc[0][col]}")

if len(first_old) > 0 and len(first_new) > 0:
    print("\nKÜLÖNBSÉGEK:")
    for col in first_old.columns:
        old_val = first_old.iloc[0][col]
        new_val = first_new.iloc[0][col]
        if str(old_val) != str(new_val):
            print(f"  {col}:")
            print(f"    Régi: {old_val}")
            print(f"    Új:   {new_val}")

print()

# ============================================================================
# 8. ÖSSZEFOGLALÁS
# ============================================================================
print("=" * 80)
print("ÖSSZEFOGLALÁS")
print("=" * 80)
print(f"""
TERMÉKAZONOSÍTÁS MEGBÍZHATÓSÁGA:
1. Terméknév:      {len(common_names)} közös (megnövekedett: {len(only_new_names)}, csökkent: {len(only_old_names)})
2. Vonalkód:       {len(common_barcodes)} közös (új: {len(only_new_barcodes)}, eltűnt: {len(only_old_barcodes)})
3. Képek:          {len(common_images)} közös (új: {len(only_new_images)}, eltűnt: {len(only_old_images)})
4. Product ID:     {len(common_ids)} közös (új: {len(only_new_ids)}, eltűnt: {len(only_old_ids)})

PROBLÉMA SZIGNALIZÁLÁS:
✗ A kategoriak.txt-ben hardkódolt számok (id-k) -> kategória mapping PROBLÉMÁS
✗ Termékek ID-ja változik, de neve marad ugyanaz
✗ Vonalkód alapján szinte jól azonosíthatók a termékek
✗ Képlinkek is viszonylag stabil azonosítók

JAVASLAT:
- Vonalkód alapján kellene azonosítani a termékeket, nem az API product ID-ja alapján
- Ha nincs vonalkód, akkor képlink vagy név kombinációja
- Kategóriákat dinamikusan kellene kezelni, nem hardkódolt számok alapján
""")
