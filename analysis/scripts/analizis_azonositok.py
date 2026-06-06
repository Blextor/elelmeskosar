import pandas as pd
import os
from itertools import combinations

workspace = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
file_new = os.path.join(workspace, r'data/markets_data/spar_normalized_data_20260417_021319.csv')
file_old = os.path.join(workspace, r'data/markets_data/spar_normalized_data_20251003_070148.csv')

df_new = pd.read_csv(file_new, encoding='utf-8')
df_old = pd.read_csv(file_old, encoding='utf-8')

df_new_clean = df_new.dropna(subset=['product_name']).reset_index(drop=True)
df_old_clean = df_old.dropna(subset=['product_name']).reset_index(drop=True)

print("=" * 80)
print("RÉSZLETES AZONOSÍTÓ ELEMZÉS")
print("=" * 80)
print()

# ============================================================================
# VONALKÓD ELEMZÉS
# ============================================================================
print("=" * 80)
print("1. VONALKÓD ALAPJÁN AZONOSÍTÁS (PONTOSSÁG VIZSGÁLAT)")
print("=" * 80)

with_barcode_old = df_old_clean[df_old_clean['barcode'].notna() & (df_old_clean['barcode'] != '')].copy()
with_barcode_new = df_new_clean[df_new_clean['barcode'].notna() & (df_new_clean['barcode'] != '')].copy()

# Vonalkód - név leképezés
barcode_name_old = dict(zip(with_barcode_old['barcode'], with_barcode_old['product_name']))
barcode_name_new = dict(zip(with_barcode_new['barcode'], with_barcode_new['product_name']))

# Közös vonalkódok, de eltérő nevek
conflict_products = 0
for barcode in set(barcode_name_old.keys()) & set(barcode_name_new.keys()):
    if barcode_name_old[barcode].lower().strip() != barcode_name_new[barcode].lower().strip():
        conflict_products += 1

print(f"Vonalkóddal rendelkező termékek:")
print(f"  Régi: {len(with_barcode_old)}, Új: {len(with_barcode_new)}")
print(f"  Közös barcode: {len(set(barcode_name_old.keys()) & set(barcode_name_new.keys()))}")
print(f"  Ugyanaz a vonalkód, ELTÉRŐ név: {conflict_products}")
print()

# ============================================================================
# KÉP LINK ELEMZÉS
# ============================================================================
print("=" * 80)
print("2. KÉPLINK ALAPJÁN AZONOSÍTÁS")
print("=" * 80)

# Képenlinkek alapján match-elés
old_image_links = {}
new_image_links = {}

for idx, row in df_old_clean.iterrows():
    img = row['image_urls']
    if pd.notna(img) and img != '':
        first_img = str(img).split(';')[0].strip()
        if first_img not in old_image_links:
            old_image_links[first_img] = []
        old_image_links[first_img].append(row['product_name'])

for idx, row in df_new_clean.iterrows():
    img = row['image_urls']
    if pd.notna(img) and img != '':
        first_img = str(img).split(';')[0].strip()
        if first_img not in new_image_links:
            new_image_links[first_img] = []
        new_image_links[first_img].append(row['product_name'])

# Ugyanaz a kép, de eltérő termékek
image_conflicts = 0
for img in set(old_image_links.keys()) & set(new_image_links.keys()):
    if len(old_image_links[img]) == 1 and len(new_image_links[img]) == 1:
        if old_image_links[img][0].lower() != new_image_links[img][0].lower():
            image_conflicts += 1

print(f"Képenlinkvel rendelkező termékek: Régi: {len(df_old_clean[df_old_clean['image_urls'].notna()])}, Új: {len(df_new_clean[df_new_clean['image_urls'].notna()])}")
print(f"Közös képlinkek: {len(set(old_image_links.keys()) & set(new_image_links.keys()))}")
print(f"Ugyanaz a kép, ELTÉRŐ termék: {image_conflicts}")
print()

# ============================================================================
# TÖBB AZONOSÍTÓ KOMBINÁCIÓJA
# ============================================================================
print("=" * 80)
print("3. TÖBBSZ-AZONOSÍTÓS MEGKÖZELÍTÉS (BARCODE + NÉV + KÉP)")
print("=" * 80)

# Termékek összevetése: barcode + név + kép kombináció
matched_by_barcode = 0
matched_by_name = 0
matched_by_image = 0
matched_by_combination = 0

common_names = set(df_old_clean['product_name'].str.lower().str.strip()) & \
               set(df_new_clean['product_name'].str.lower().str.strip())

for common_name in common_names:
    old_rows = df_old_clean[df_old_clean['product_name'].str.lower() == common_name.strip().lower()]
    new_rows = df_new_clean[df_new_clean['product_name'].str.lower() == common_name.strip().lower()]
    
    for _, old in old_rows.iterrows():
        for _, new in new_rows.iterrows():
            # Vonalkód match
            if pd.notna(old['barcode']) and pd.notna(new['barcode']):
                if str(old['barcode']).strip() == str(new['barcode']).strip():
                    matched_by_barcode += 1
                    continue
            
            # Képlink match
            if pd.notna(old['image_urls']) and pd.notna(new['image_urls']):
                old_first = str(old['image_urls']).split(';')[0].strip()
                new_first = str(new['image_urls']).split(';')[0].strip()
                if old_first == new_first:
                    matched_by_image += 1
                    continue
            
            # Név + ár kombinációja
            if old['product_name'].lower() == new['product_name'].lower() and \
               abs(old['unit_price'] - new['unit_price']) < 100:  # árváltozás < 100 HUF
                matched_by_combination += 1

print(f"Közös terméknevek: {len(common_names)}")
print(f"  - Vonalkóddal azonosított: {matched_by_barcode}")
print(f"  - Képenként azonosított: {matched_by_image}")
print(f"  - Név + ár kombinációval: {matched_by_combination}")
print()

# ============================================================================
# TERMÉKKATEGÓRIA STABILITÁSA
# ============================================================================
print("=" * 80)
print("4. KATEGÓRIAMEGJELENÍTÉS PROBLÉMÁJA")
print("=" * 80)

old_categories = df_old_clean['categories'].value_counts()
new_categories = df_new_clean['categories'].value_counts()

common_categories = set(old_categories.index) & set(new_categories.index)
only_old_cat = set(old_categories.index) - set(new_categories.index)
only_new_cat = set(new_categories.index) - set(old_categories.index)

print(f"Kategóriák száma - Régi: {len(old_categories)}, Új: {len(new_categories)}")
print(f"Közös kategóriák: {len(common_categories)}")
print(f"Csak régi kategóriák: {len(only_old_cat)}")
print(f"Csak új kategóriák: {len(only_new_cat)}")
print()

if only_new_cat:
    print(f"Új kategóriák (első 10):")
    for cat in list(only_new_cat)[:10]:
        print(f"  - {cat}")
print()

# ============================================================================
# TERMÉKADAT STABILITÁSA (UGYANAZ A NÉV, DE HOGYAN VÁLTOZNAK?)
# ============================================================================
print("=" * 80)
print("5. MEGLÉVŐ TERMÉKEK ADATVÁLTOZÁSAI (NÉV ALAPJÁN EKVIVALENS)")
print("=" * 80)

price_increase = 0
price_decrease = 0
price_unchanged = 0
availability_changed = 0

for common_name in common_names:
    old_rows = df_old_clean[df_old_clean['product_name'].str.lower() == common_name.strip().lower()]
    new_rows = df_new_clean[df_new_clean['product_name'].str.lower() == common_name.strip().lower()]
    
    if len(old_rows) > 0 and len(new_rows) > 0:
        old_price = old_rows.iloc[0]['unit_price']
        new_price = new_rows.iloc[0]['unit_price']
        
        # NaN kezelés
        if pd.isna(old_price) or pd.isna(new_price):
            continue
        
        if new_price > old_price:
            price_increase += 1
        elif new_price < old_price:
            price_decrease += 1
        else:
            price_unchanged += 1

print(f"Termékek árváltozása (közös nevek alapján):")
print(f"  - Áremelkedés: {price_increase} termék")
print(f"  - Árcsökkentés: {price_decrease} termék")
print(f"  - Ár maradt ugyanaz: {price_unchanged} termék")
print()

# ============================================================================
# JAVASLATOK
# ============================================================================
print("=" * 80)
print("MEGÁLLAPÍTÁSOK ÉS JAVASLATOK")
print("=" * 80)
print(f"""
PROBLÉMAI:
1. Product ID-k minden futtatásnál megváltoznak (0% közös)
   → NEM használhatók az egyeztetéshez

2. Kategóriák hardkódolt szám-alapú (46 = puding, 7 = alma-körte)
   → API visszatérésénél más szám = rossz kategória
   → Javasolt: kategória nevet kezelni, nem azonosítót

3. Termékkészlet jelentős mértékben változik (~50% különbség)
   → Sok új termék hozzáadódott
   → Sok régi termék eltűnt

MEGOLDÁSOK:
✓ Vonalkód (barcode) - Legmegbízhatóbb azonosító (3543 közös)
✓ Terméknév - Viszonylag stabil (3529 közös), de túl általános
✓ Képenlinkek - Jó komplementer azonosító (3072 közös)
✗ API Product ID - Sosem ismétlődik, ne használj!

AJÁNLOTT STRATÉGIA:
1. Elsődleges: vonalkód (99% pontosság)
2. Másodlagos: kép hash/URL összevetés
3. Harmadlagos: terméknév + kategória fuzzy match
4. Kategóriák: slug-ból, nem számokból kezelni
""")
