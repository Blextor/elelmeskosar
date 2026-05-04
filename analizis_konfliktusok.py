import pandas as pd
import os

workspace = r'c:\Users\Bobo\Documents\GitHub\elelmeskosar'
file_new = os.path.join(workspace, r'data/markets_data/spar_normalized_data_20260417_021319.csv')
file_old = os.path.join(workspace, r'data/markets_data/spar_normalized_data_20251003_070148.csv')

df_new = pd.read_csv(file_new, encoding='utf-8')
df_old = pd.read_csv(file_old, encoding='utf-8')

df_new_clean = df_new.dropna(subset=['product_name']).reset_index(drop=True)
df_old_clean = df_old.dropna(subset=['product_name']).reset_index(drop=True)

print("=" * 100)
print("RÉSZLETES AZONOSÍTÓ KONFLIKTUS ELEMZÉS")
print("=" * 100)
print()

# ============================================================================
# 1. AZONOS NÉV, DE ELTÉRŐ VONALKÓD
# ============================================================================
print("=" * 100)
print("1. AZONOS NÉV, DE ELTÉRŐ VONALKÓD")
print("=" * 100)
print()

name_barcode_conflicts = []

for name_group_new in df_new_clean.groupby(df_new_clean['product_name'].str.lower().str.strip()):
    name_lower = name_group_new[0]
    rows_new = name_group_new[1]
    
    # Közös név a régi fájlban
    rows_old = df_old_clean[df_old_clean['product_name'].str.lower().str.strip() == name_lower]
    
    if len(rows_old) > 0 and len(rows_new) > 0:
        old_row = rows_old.iloc[0]
        new_row = rows_new.iloc[0]
        
        old_barcode = str(old_row['barcode']).strip() if pd.notna(old_row['barcode']) else None
        new_barcode = str(new_row['barcode']).strip() if pd.notna(new_row['barcode']) else None
        
        # Konfliktus: egyik van vonalkód, másiknak nincs
        if (old_barcode != 'nan' and new_barcode == 'nan') or \
           (old_barcode == 'nan' and new_barcode != 'nan') or \
           (old_barcode != 'nan' and new_barcode != 'nan' and old_barcode != new_barcode):
            
            name_barcode_conflicts.append({
                'product_name': new_row['product_name'],
                'old_barcode': old_barcode if old_barcode != 'nan' else '(nincs)',
                'new_barcode': new_barcode if new_barcode != 'nan' else '(nincs)',
                'old_price': old_row['unit_price'],
                'new_price': new_row['unit_price'],
            })

print(f"Talált: {len(name_barcode_conflicts)} termék")
print()

if name_barcode_conflicts:
    print("RÉSZLETESEN:")
    for i, conflict in enumerate(name_barcode_conflicts[:20], 1):
        print(f"{i}. {conflict['product_name']}")
        print(f"   Regi vonalkod: {conflict['old_barcode']}")
        print(f"   Uj vonalkod:   {conflict['new_barcode']}")
        print(f"   Ar: {conflict['old_price']:.2f} Ft -> {conflict['new_price']:.2f} Ft")
        print()

print()

# ============================================================================
# 2. AZONOS VONALKÓD, DE ELTÉRŐ NÉV
# ============================================================================
print("=" * 100)
print("2. AZONOS VONALKÓD, DE ELTÉRŐ TERMÉKNÉV")
print("=" * 100)
print()

barcode_name_conflicts = []

old_with_barcode = df_old_clean[df_old_clean['barcode'].notna() & (df_old_clean['barcode'] != '')]
new_with_barcode = df_new_clean[df_new_clean['barcode'].notna() & (df_new_clean['barcode'] != '')]

for barcode_group in new_with_barcode.groupby('barcode'):
    barcode = barcode_group[0]
    rows_new = barcode_group[1]
    
    # Közös vonalkód a régi fájlban
    rows_old = old_with_barcode[old_with_barcode['barcode'] == barcode]
    
    if len(rows_old) > 0 and len(rows_new) > 0:
        old_row = rows_old.iloc[0]
        new_row = rows_new.iloc[0]
        
        if old_row['product_name'].lower().strip() != new_row['product_name'].lower().strip():
            barcode_name_conflicts.append({
                'barcode': barcode,
                'old_name': old_row['product_name'],
                'new_name': new_row['product_name'],
                'old_price': old_row['unit_price'],
                'new_price': new_row['unit_price'],
                'old_category': old_row['categories'],
                'new_category': new_row['categories'],
            })

print(f"Talált: {len(barcode_name_conflicts)} termék")
print()

if barcode_name_conflicts:
    print("RÉSZLETESEN:")
    for i, conflict in enumerate(barcode_name_conflicts[:20], 1):
        print(f"{i}. Vonalkod: {conflict['barcode']}")
        print(f"   Regi nev: {conflict['old_name']}")
        print(f"   Uj nev:   {conflict['new_name']}")
        print(f"   Ar: {conflict['old_price']:.2f} Ft -> {conflict['new_price']:.2f} Ft")
        print(f"   Kategoria: {conflict['old_category']} -> {conflict['new_category']}")
        print()

print()

# ============================================================================
# 3. AZONOS KÉPLINK, DE ELTÉRŐ NÉV
# ============================================================================
print("=" * 100)
print("3. AZONOS KÉPLINK, DE ELTÉRŐ TERMÉKNÉV")
print("=" * 100)
print()

image_name_conflicts = []

old_with_image = df_old_clean[df_old_clean['image_urls'].notna() & (df_old_clean['image_urls'] != '')]
new_with_image = df_new_clean[df_new_clean['image_urls'].notna() & (df_new_clean['image_urls'] != '')]

old_image_dict = {}
new_image_dict = {}

for idx, row in old_with_image.iterrows():
    first_img = str(row['image_urls']).split(';')[0].strip()
    if first_img not in old_image_dict:
        old_image_dict[first_img] = []
    old_image_dict[first_img].append(row)

for idx, row in new_with_image.iterrows():
    first_img = str(row['image_urls']).split(';')[0].strip()
    if first_img not in new_image_dict:
        new_image_dict[first_img] = []
    new_image_dict[first_img].append(row)

# Közös képlinkek, de eltérő nevek
for img_link in set(old_image_dict.keys()) & set(new_image_dict.keys()):
    old_rows = old_image_dict[img_link]
    new_rows = new_image_dict[img_link]
    
    # Ha csak egy-egy termék az adott képpel
    if len(old_rows) == 1 and len(new_rows) == 1:
        old_row = old_rows[0]
        new_row = new_rows[0]
        
        if old_row['product_name'].lower().strip() != new_row['product_name'].lower().strip():
            image_name_conflicts.append({
                'image_url': img_link[:100] + '...' if len(img_link) > 100 else img_link,
                'old_name': old_row['product_name'],
                'new_name': new_row['product_name'],
                'old_barcode': old_row['barcode'] if pd.notna(old_row['barcode']) else '(nincs)',
                'new_barcode': new_row['barcode'] if pd.notna(new_row['barcode']) else '(nincs)',
                'old_price': old_row['unit_price'],
                'new_price': new_row['unit_price'],
            })

print(f"Talált: {len(image_name_conflicts)} termék")
print()

if image_name_conflicts:
    print("RÉSZLETESEN:")
    for i, conflict in enumerate(image_name_conflicts[:20], 1):
        print(f"{i}. Keplink: {conflict['image_url']}")
        print(f"   Regi nev: {conflict['old_name']}")
        print(f"   Uj nev:   {conflict['new_name']}")
        print(f"   Regi vonalkod: {conflict['old_barcode']} -> Uj: {conflict['new_barcode']}")
        print(f"   Ar: {conflict['old_price']:.2f} Ft -> {conflict['new_price']:.2f} Ft")
        print()

print()

# ============================================================================
# 4. AZONOS NÉV, DE ELTÉRŐ KÉPLINK
# ============================================================================
print("=" * 100)
print("4. AZONOS NÉV, DE ELTÉRŐ KÉPLINK (ELSŐ)")
print("=" * 100)
print()

name_image_conflicts = []

for name_group_new in df_new_clean.groupby(df_new_clean['product_name'].str.lower().str.strip()):
    name_lower = name_group_new[0]
    rows_new = name_group_new[1]
    
    rows_old = df_old_clean[df_old_clean['product_name'].str.lower().str.strip() == name_lower]
    
    if len(rows_old) > 0 and len(rows_new) > 0:
        old_row = rows_old.iloc[0]
        new_row = rows_new.iloc[0]
        
        old_img = str(old_row['image_urls']).split(';')[0].strip() if pd.notna(old_row['image_urls']) else None
        new_img = str(new_row['image_urls']).split(';')[0].strip() if pd.notna(new_row['image_urls']) else None
        
        if old_img and new_img and old_img != new_img:
            name_image_conflicts.append({
                'product_name': new_row['product_name'],
                'old_image': old_img[:80] + '...' if len(old_img) > 80 else old_img,
                'new_image': new_img[:80] + '...' if len(new_img) > 80 else new_img,
                'old_barcode': old_row['barcode'] if pd.notna(old_row['barcode']) else '(nincs)',
                'new_barcode': new_row['barcode'] if pd.notna(new_row['barcode']) else '(nincs)',
                'old_price': old_row['unit_price'],
                'new_price': new_row['unit_price'],
            })

print(f"Talált: {len(name_image_conflicts)} termék")
print()

if name_image_conflicts:
    print("RÉSZLETESEN (első 15):")
    for i, conflict in enumerate(name_image_conflicts[:15], 1):
        print(f"{i}. {conflict['product_name']}")
        print(f"   Regi kep: ...{conflict['old_image'][-40:]}")
        print(f"   Uj kep:   ...{conflict['new_image'][-40:]}")
        print(f"   Vonalkod: {conflict['old_barcode']} -> {conflict['new_barcode']}")
        print(f"   Ar: {conflict['old_price']:.2f} Ft -> {conflict['new_price']:.2f} Ft")
        print()

print()

# ============================================================================
# 5. AZONOS VONALKÓD, DE ELTÉRŐ KÉP
# ============================================================================
print("=" * 100)
print("5. AZONOS VONALKÓD, DE ELTÉRŐ KÉPLINK (ELSŐ)")
print("=" * 100)
print()

barcode_image_conflicts = []

for barcode_group in new_with_barcode.groupby('barcode'):
    barcode = barcode_group[0]
    rows_new = barcode_group[1]
    
    rows_old = old_with_barcode[old_with_barcode['barcode'] == barcode]
    
    if len(rows_old) > 0 and len(rows_new) > 0:
        old_row = rows_old.iloc[0]
        new_row = rows_new.iloc[0]
        
        old_img = str(old_row['image_urls']).split(';')[0].strip() if pd.notna(old_row['image_urls']) else None
        new_img = str(new_row['image_urls']).split(';')[0].strip() if pd.notna(new_row['image_urls']) else None
        
        if old_img and new_img and old_img != new_img:
            barcode_image_conflicts.append({
                'product_name': new_row['product_name'],
                'barcode': barcode,
                'old_image': old_img[-50:] if len(old_img) > 50 else old_img,
                'new_image': new_img[-50:] if len(new_img) > 50 else new_img,
                'old_price': old_row['unit_price'],
                'new_price': new_row['unit_price'],
            })

print(f"Talált: {len(barcode_image_conflicts)} termék")
print()

if barcode_image_conflicts:
    print("RÉSZLETESEN (első 15):")
    for i, conflict in enumerate(barcode_image_conflicts[:15], 1):
        print(f"{i}. {conflict['product_name']}")
        print(f"   Vonalkod: {conflict['barcode']}")
        print(f"   Regi kep: ...{conflict['old_image']}")
        print(f"   Uj kep:   ...{conflict['new_image']}")
        print(f"   Ar: {conflict['old_price']:.2f} Ft -> {conflict['new_price']:.2f} Ft")
        print()

print()

# ============================================================================
# 6. ÖSSZEFOGLALÁS
# ============================================================================
print("=" * 100)
print("ÖSSZEFOGLALÁS - KONFLIKTUSOK SZÁMA")
print("=" * 100)
print()
print(f"1. Azonos név, eltérő vonalkód:  {len(name_barcode_conflicts)}")
print(f"2. Azonos vonalkód, eltérő név:  {len(barcode_name_conflicts)}")
print(f"3. Azonos képlink, eltérő név:   {len(image_name_conflicts)}")
print(f"4. Azonos név, eltérő képlink:   {len(name_image_conflicts)}")
print(f"5. Azonos vonalkód, eltérő kép:  {len(barcode_image_conflicts)}")
print()

total_conflicts = len(name_barcode_conflicts) + len(barcode_name_conflicts) + \
                  len(image_name_conflicts) + len(name_image_conflicts) + \
                  len(barcode_image_conflicts)

print(f"ÖSSZESEN konfliktus eset: {total_conflicts}")
print()

# ============================================================================
# 7. EXPORTÁLÁS CSV-BE
# ============================================================================
print("=" * 100)
print("EXPORTÁLÁS CSV FÁJLOKBA")
print("=" * 100)
print()

output_dir = os.path.join(workspace, 'konfliktus_elemzes')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 1. Azonos név, eltérő vonalkód
if name_barcode_conflicts:
    df_conflict = pd.DataFrame(name_barcode_conflicts)
    output_file = os.path.join(output_dir, '1_azonos_nev_elter_vonalkod.csv')
    df_conflict.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✓ Mentve: 1_azonos_nev_elter_vonalkod.csv ({len(df_conflict)} sor)")

# 2. Azonos vonalkód, eltérő név
if barcode_name_conflicts:
    df_conflict = pd.DataFrame(barcode_name_conflicts)
    output_file = os.path.join(output_dir, '2_azonos_vonalkod_elter_nev.csv')
    df_conflict.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✓ Mentve: 2_azonos_vonalkod_elter_nev.csv ({len(df_conflict)} sor)")

# 3. Azonos képlink, eltérő név
if image_name_conflicts:
    df_conflict = pd.DataFrame(image_name_conflicts)
    output_file = os.path.join(output_dir, '3_azonos_keplink_elter_nev.csv')
    df_conflict.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✓ Mentve: 3_azonos_keplink_elter_nev.csv ({len(df_conflict)} sor)")

# 4. Azonos név, eltérő képlink
if name_image_conflicts:
    df_conflict = pd.DataFrame(name_image_conflicts)
    output_file = os.path.join(output_dir, '4_azonos_nev_elter_keplink.csv')
    df_conflict.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✓ Mentve: 4_azonos_nev_elter_keplink.csv ({len(df_conflict)} sor)")

# 5. Azonos vonalkód, eltérő képlink
if barcode_image_conflicts:
    df_conflict = pd.DataFrame(barcode_image_conflicts)
    output_file = os.path.join(output_dir, '5_azonos_vonalkod_elter_keplink.csv')
    df_conflict.to_csv(output_file, index=False, encoding='utf-8')
    print(f"✓ Mentve: 5_azonos_vonalkod_elter_keplink.csv ({len(df_conflict)} sor)")

print()
print(f"📁 Mappa: {output_dir}")
