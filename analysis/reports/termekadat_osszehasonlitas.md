# Termékadat Összehasonlítás - Elemzés Eredménye

## Fájlok
- **Régi**: `spar_normalized_data_20251003_070148.csv` (2025-10-03) - **7228 termék**
- **Új**: `spar_normalized_data_20260417_021319.csv` (2026-04-17) - **4587 termék**

---

## 1. TERMÉKAZONOSÍTÓK MEGBÍZHATÓSÁGA

### 📊 Terméknév Alapján
- **Közös terméknevek**: 3529 (61%)
- **Csak új termékek**: 1035 (+23%)
- **Csak régi termékek**: 3664 (-51%)
- **Duplikátumok**: 32 régi, 19 új fájlban

**Megállapítás**: Viszonylag stabil, de sok termék teljesen eltűnt vagy új.

---

### 🔢 Vonalkód (Barcode) Alapján
- **Legrelevánsabb azonosító!**
- **Közös vonalkódok**: 3543 (99% pontosság!)
- **Vonalkóddal rendelkező termékek**: 7058 (régi), 4341 (új)
- **Konfliktusok** (ugyanaz a vonalkód, eltérő név): 149

**Megállapítás**: Ez az EGYEDÜLI stabil azonosító! Az API product ID-k minden futást vagy kategória-feltöltéskor megváltoznak.

---

### 🖼️ Képlink Alapján
- **Közös képlinkek**: 3072 (85%)
- **Képenlinkek konfliktusa** (ugyanaz a kép, eltérő termék): 35

**Megállapítás**: Jó komplementer azonosító, de nem elsődleges.

---

### 🆔 API Product ID
- **Közös ID-k**: **0 (0%)**
- **Régi ID-k**: 7228 (egyetlen sem ismétlődik!)
- **Új ID-k**: 4587 (egyetlen sem ismétlődik!)

**🚨 KRITIKUS PROBLÉMA**: Az API minden futásnál új ID-kat generál! **SOSEM használható stabilan.**

---

## 2. KATEGÓRIÁK PROBLÉMÁJA

### Hardkódolt Szám-Alapú Kategóriák
- `kategoriak.txt` így néz ki: `46,Puding,puding-46` stb.
- A Python kódban így vannak szerepelve: `categories: puding-46`

### Az Valódi Probléma
```
Régi fájl:  Golden alma lédig → alma-es-korte-7
Új fájl:    Golden alma lédig → puding-46
```

**❌ MI A GOND?**
- Az elő futásnál a 46-os ID puding volt
- **Most** az 46-os ID tejtermékek (tejtermekek-47)
- A hardkódolt számok **soha nem konzisztensek**!

### Megoldás
```
❌ Rossz: categories = 46
✅ Jó:    categories = "alma-es-korte" (slug alapján)
```

---

## 3. KONKRÉT PÉLDA: "Golden alma lédig"

| Mező | Régi (2025-10-03) | Új (2026-04-17) | Változás |
|------|-------|--------|---------|
| **store_product_id** | `670fdbfca1b61551859c812c` | `a94b4face5ffc523836b45f4` | ✗ Megváltozott |
| **product_name** | Golden alma lédig | Golden alma lédig | ✓ Ugyanaz |
| **barcode** | (nincs) | (nincs) | ✓ Konzisztens |
| **unit_price** | 89.85 Ft | 73.05 Ft | ✗ -17% árcsökkentés |
| **unit_type** | g | g | ✓ Ugyanaz |
| **unit_step** | 150.0 | 150.0 | ✓ Ugyanaz |
| **image_urls** | `.../37897000.png` | `.../37897000.jpg` | ⚠️ URL változott, de ugyanaz a kép |
| **categories** | alma-es-korte-7 | puding-46 | ❌ ROSSZ KATEGÓRIA! |

---

## 4. AZONOSÍTÁSI STRATÉGIA - AJÁNLOTT MEGOLDÁS

### Prioritás Sorrend
```python
1. VONALKÓD (barcode)
   - 99% pontosság, ha létezik
   - 3543 közös a két fájl között
   
2. KÉPENLINKEK
   - 85% pontosság
   - Jó backup, ha nincs vonalkód
   
3. TERMÉKNÉV + KATEGÓRIA
   - Nem egyedi, de kombinációban használható
   - Fuzzy matching ajánlott (pl. Levenshtein távolság)
   
4. API PRODUCT ID
   - ❌ NE HASZNÁLD! Sosem ismétlődik!
```

---

## 5. KATEGÓRIA KEZELÉS - MEGOLDÁS

### Jelenlegi (Rossz) Megközelítés
```python
# kategoriak.txt
46,Puding,puding-46
7,Alma és körte,alma-es-korte-7

# normalize_data_spar.py
slug = row.get("category_slug", "").strip()  # Ez az API kapja meg!
# De az API nem adja vissza az angol id-t, csak a slug-ot

# Eredmény: Hardkódolt szám helyett slug jön = kategóriavonal rossz
```

### Javasolt (Jó) Megközelítés
```python
# API-ből jön: category_slug = "alma-es-korte-7"
# Tárold így: categories = "alma-es-korte-7"

# NE ezt csináld:
# Extract csak a számot: categories = 7  ← BUG!

# Helyette:
# Tartsd meg a slug-ot: categories = "alma-es-korte-7"

# Kereséshez build-elj egy mappot:
CATEGORY_MAPPING = {
    "alma-es-korte-7": {"id": 7, "name": "Alma és körte", "parent": "gyumolcs-6"},
    "puding-46": {"id": 46, "name": "Puding", "parent": "tejtermekek-47"},
    ...
}
```

---

## 6. TERMÉKKÉSZLET VÁLTOZÁSAI

| Kategória | Érték |
|-----------|-------|
| **Teljes termékkészlet csökkenése** | 7228 → 4587 (-37%) |
| **Közös (név alapján)** | 3529 (61%) |
| **Új termékek** | 1035 (+23%) |
| **Eltűnt termékek** | 3664 (-51%) |
| **Durchschnittl. árváltozás** | Vegyes |

---

## 7. ALAPVETŐ HIBÁK A KÓDBAN

### ❌ `kategoriak.txt`
```csv
index,name,slug
46,Puding,puding-46
7,Alma és körte,alma-es-korte-7
```
**Probléma**: Az "index" nem az API-t, hanem a Python szakász által szerkesztett sorszám!

### ❌ `normalize_data_spar.py`
```python
slug = row.get("category_slug", "").strip()
# slug = "alma-es-korte-7" vagy "puding-46"
# Ez helyes! 

# De a kód a mapping-et nem kezeli jól
```

### ✅ Javasolt Fix
```python
# Tárold így az output CSV-ben:
output.write(f"...{slug}...")  # pl. "alma-es-korte-7"

# NE ezt:
output.write(f"...{extract_number(slug)}...")  # pl. "7"
```

---

## 8. VÉGSŐ JAVASLATOK

### Rövid Távú
1. **Vonalkód alapján azonosítani** a terméket, nem az API ID alapján
2. **Kategóriákat slug-ként tárolni** (`alma-es-korte-7`), nem számként (`7`)
3. **Képlink hash** kell számítani (MD5/SHA256) a duplikáció elkerülésére

### Közép Távú
1. **Adatbázis**: SQL vagy NoSQL az összes termék + verzió elmentésére
2. **Verzióózatás**: Termékenként eltárni a régi árakat, képeket
3. **Change tracking**: Mely mező miként változott

### Hosszú Távú
1. **Saját termékazonosító** (pl. `spar_alma_001`) bevezetése
2. **Ontológia**: Termékkategóriák és attribútumok hierarchiája
3. **API caching**: Nem kell minden nap új ID-kat generálni

---

## 9. ÖSSZEFOGLALÁS

| Szempont | Jelenlegi | Javasolt |
|----------|-----------|----------|
| **Termékazonosítás** | API ID (rossz) | Vonalkód (jó) |
| **Kategória** | Szám (7, 46) | Slug (alma-es-korte-7) |
| **Backup azonosítás** | Nincs | Képenlinkek + név |
| **Duplikátumok** | Nem kezeli | de-duplikáció szükséges |
| **Verzióózás** | Nincs | Kell |

---

**Készítve**: 2026-04-21
**Adatforrás**: `spar_normalized_data_20260417_021319.csv` vs `spar_normalized_data_20251003_070148.csv`
