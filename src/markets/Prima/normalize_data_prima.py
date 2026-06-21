import csv
import json
import os
import glob
from datetime import datetime
import re
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_size import to_full_size

csv.field_size_limit(1024 * 1024 * 1024)

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

# Fájlnevek
input_file = 'all_data'
output_file = 'normalized_data'

# Kimeneti mezők
output_fields = [
    "store_name",
    "store_product_id",
    "product_name",
    "brand_name",
    "available",
    "expected_restock",
    "barcode",
    "unit_price",
    "unit_type",
    "unit_step",
    "is_discounted",
    "original_unit_price",
    "secondary_unit_price",
    "secondary_unit_type",
    "secondary_unit_step",
    "image_urls",
    "description",
    "categories"
]

import re
from typing import Optional, Tuple

def kiszereles_kivalasztas(szoveg: str) -> Tuple[Optional[float], Optional[str]]:
    # Egység minták, kis- és nagybetűt is figyelembe véve
    pattern = r'(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|db|pcs|pc|x\s*\d+\s*(?:g|db|ml|l))'
    matches = re.findall(pattern, szoveg, flags=re.IGNORECASE)

    if not matches:
        oks = szoveg.split(" ")
        if oks[-1] == "db" or oks[-1] == "DB":
            return 1.0, "db"
        if oks[-1] == "kg" or oks[-1] == "KG":
            return 1.0, "kg"
        return None, None

    for value_str, unit in reversed(matches):
        if 'x' in unit.lower():
            oks = unit.split(" ")

            try:
                new_val = float(value_str) * float(oks[1])
                new_unit = oks[2]
                return new_val, new_unit
            except ValueError:
                continue

    # Ha nincs ilyen, akkor fallback az utolsó találatra
    value_str, unit = matches[-1]
    value_str = value_str.replace(',', '.')
    try:
        value = float(value_str)
    except ValueError:
        return None, None
    unit = unit.lower().replace(" ", "")
    if unit == "pc" or unit == "pcs":
        return value, "db"
    return value, unit

def kiszereles_kivalasztas3(szoveg: str) -> Tuple[Optional[float], Optional[str]]:
    pattern = r'(\d+(?:[\.,]\d+)?)\s*(kg|g|ml|l|db|pcs|pc|cl|x\s*\d+(?:[\.,]\d+)?\s*(?:g|db|ml|cl|l))'
    matches = re.findall(pattern, szoveg, flags=re.IGNORECASE)

    if not matches:
        oks = szoveg.strip().split(" ")
        if oks[-1].lower() == "db":
            return 1.0, "db"
        if oks[-1].lower() == "kg":
            return 1.0, "kg"
        return None, None

    for value_str, unit in reversed(matches):
        if 'x' in unit.lower():
            # Pl. unit = "x 0,5 l" → szám és mértékegység kinyerése
            multi_match = re.match(r'x\s*(\d+(?:[\.,]\d+)?)\s*(g|ml|l|cl|db)', unit, flags=re.IGNORECASE)
            if multi_match:
                multiplier_str, multi_unit = multi_match.groups()
                try:
                    value = float(value_str.replace(',', '.'))
                    multiplier = float(multiplier_str.replace(',', '.'))
                    return value * multiplier, multi_unit.lower()
                except ValueError:
                    continue

    # fallback: az utolsó normál egység
    value_str, unit = matches[-1]
    try:
        value = float(value_str.replace(',', '.'))
        unit = unit.lower().replace(" ", "")
        if unit in ("pc", "pcs"):
            unit = "db"
        return value, unit
    except ValueError:
        return None, None

def kiszereles_normalizalas(kiszereles):
    if kiszereles[1] == "l":
        return kiszereles[0]*1000, "ml"
    if kiszereles[1] == "kg":
        return kiszereles[0]*1000, "g"
    if kiszereles[1] == "cl":
        return kiszereles[0]*10, "ml"
    if kiszereles[1] == "number_of_items":
        return kiszereles[0], "g"
    if kiszereles[1] == "grams":
        return kiszereles[0], "g"
    return kiszereles[0], kiszereles[1]

def kiszereles_egysegarbol(kiszereles, egyseg, lepeskoz, failSafe):
    if (None, None) == kiszereles:
        if egyseg == "kilogram":
            return lepeskoz, "kg"
        if egyseg == "litre":
            return lepeskoz, "l"
        if egyseg == "piece":
            return lepeskoz, "db"
        if egyseg == "gram":
            return lepeskoz, "g"
        if egyseg == "grams":
            return lepeskoz, "g"
        if egyseg == "number_of_items":
            return lepeskoz, "g"
        if failSafe:
            return 1.0, "db"
    return kiszereles

def benne_van_sorkent(szoveg: str, fajlnev: str) -> bool:
    with open(fajlnev, 'r', encoding='utf-8') as f:
        for sor in f:
            if sor.strip() == szoveg:
                return True
    return False

def benne_van_sorkent_ertek(szoveg: str, eltolas: int, fajlnev: str) -> str:
    next_item = -1
    with open(fajlnev, 'r', encoding='utf-8') as f:
        for sor in f:
            next_item = next_item - 1
            if next_item == 0:
                return sor.strip()
            if sor.strip() == szoveg:
                next_item = eltolas
    return ""

cnt = 0
cnt_all = 0
cnt4 = 0
cnt5 = 0
cnt3 = 0
cnt2 = 0

input_file_name, input_date = read_latest_file(input_file)
output_file_name = generate_filename(output_file, input_date)

with open(input_file_name, mode='r', encoding='utf-8') as infile, \
     open(output_file_name, mode='w', encoding='utf-8', newline='') as outfile:

    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=output_fields)
    writer.writeheader()

    for row in reader:
        cnt_all = cnt_all + 1
        # 🌟 Itt egyéni változókba rendezzük a bemeneti mezőket
        nev = row.get("name", "").strip()
        vonalkod = row.get("barcode_gtin", "").strip()
        uzlet = "Prima"
        termek_id = row.get("id", "").strip()
        kiszereles = row.get("unit_info", "").strip()
        #marka = "???"
        keszleten = row.get("disabled_info.disable_text", "").strip().lower()
        #varhato = "???"#row.get("Várható érkezés", "").strip()
        eredeti_ar = row.get("original_price", "").replace(",", ".").strip()
        ar = row.get("price", "").replace(",", ".").strip()
        egyseg = row.get("unit_price.unit", "").strip().lower()
        lepeskoz = row.get("unit_price.base", "").strip()
        unit_ar = row.get("unit_price.price", "").strip()
        slug = row.get("category_slug", "").strip()
        #akcios = row.get("Akciós", "").strip().lower()
        eredeti_egyseg_ar = row.get("unit_price.original_price", "").strip()

        egyedi_egyseg = row.get("sell_by_weight_config.input_type", "").strip().lower()
        egyedi_lepeskoz = row.get("sell_by_weight_config.grams_per_step", "").strip().lower()
        egyedi_kilos_ar = row.get("sell_by_weight_config.price_per_kg", "").strip().lower()

        kepek_raw = row.get("images", "").strip()
        # 🌐 Próbáljuk parse-olni mint JSON-listát
        kepek_split = kepek_raw.split("'")
        kepek_url_lista = []
        for darab in kepek_split:
            if darab.find("https") == 0:
                kepek_url_lista.append(darab)

        # Kép1 és kép2 külön változók (csak ha léteznek)
        kep1 = kepek_url_lista[0] if len(kepek_url_lista) > 0 else ""
        kep2 = kepek_url_lista[1] if len(kepek_url_lista) > 1 else ""

        #leiras = row.get("Leírás", "").strip()
        #osszetevok = row.get("Összetevők", "").strip()

        # 🛠️ Kimeneti mezők feldolgozása

        kiszereles_eredeti = kiszereles_kivalasztas(kiszereles)
        if not kiszereles_eredeti == (None, None):
            kiszereles_eredeti = (float(kiszereles_eredeti[0]), kiszereles_eredeti[1])
        kiszereles_eredeti = kiszereles_normalizalas(kiszereles_eredeti)

        kiszereles_tenyleg = kiszereles_kivalasztas3(nev)
        if kiszereles_eredeti==(None, None):
            kiszereles_tenyleg = kiszereles_egysegarbol(kiszereles_tenyleg,egyseg,lepeskoz,False)
        kiszereles_tenyleg = kiszereles_egysegarbol(kiszereles_tenyleg,egyedi_egyseg,egyedi_lepeskoz,True)
        kiszereles_tenyleg = (round(float(kiszereles_tenyleg[0]), 3), kiszereles_tenyleg[1])
        kiszereles_tenyleg = kiszereles_normalizalas(kiszereles_tenyleg)

        vegleges_kiszereles_1 = (None, None)
        vegleges_kiszereles_2 = (None, None)

        if not kiszereles_eredeti == kiszereles_tenyleg and not kiszereles_eredeti == (None, None):
            if kiszereles_eredeti[1] == kiszereles_tenyleg[1]:
                if kiszereles_eredeti[0] > kiszereles_tenyleg[0]*1.05:
                    vegleges_kiszereles_1 = kiszereles_tenyleg
                    vegleges_kiszereles_2 = (1.0, 'db')
                    if benne_van_sorkent(nev, "./elírt termékek/eredeti nagyobb és maradjon úgy.txt"):
                        nev = benne_van_sorkent_ertek(nev, 1, "./elírt termékek/eredeti nagyobb és maradjon úgy.txt")
                        val = benne_van_sorkent_ertek(nev, 1, "./elírt termékek/eredeti nagyobb és maradjon úgy.txt")
                        val_s = str.split(val, " ")
                        vegleges_kiszereles_2 = (float(val_s[0]), val_s[1])
                        vegleges_kiszereles_1 = kiszereles_eredeti
                    #print("too1:", kiszereles_eredeti, kiszereles_tenyleg, vegleges_kiszereles_1, vegleges_kiszereles_2, nev)
                    cnt = cnt + 1
                elif kiszereles_eredeti[0]*1.05 < kiszereles_tenyleg[0]:
                    vegleges_kiszereles_1 = kiszereles_eredeti
                    vegleges_kiszereles_2 = (1.0, 'db')
                    if benne_van_sorkent(nev, "./elírt termékek/nevében a kiszerelés nagyobb és helyes.txt"):
                        val = benne_van_sorkent_ertek(nev, 1, "./elírt termékek/nevében a kiszerelés nagyobb és helyes.txt")
                        val_s = str.split(val, " ")
                        vegleges_kiszereles_2 = (float(val_s[0]), val_s[1])
                        vegleges_kiszereles_1 = kiszereles_tenyleg
                    #print("too2:", kiszereles_eredeti, kiszereles_tenyleg, vegleges_kiszereles_1, vegleges_kiszereles_2, nev)
                    cnt4 = cnt4 + 1
                else:  # DONE
                    vegleges_kiszereles_1 = kiszereles_tenyleg
                    vegleges_kiszereles_2 = (1.0, 'db')
                    #print("too3:",kiszereles_eredeti,kiszereles_tenyleg,nev)
                    cnt5 = cnt5 + 1

            else:
                if kiszereles_eredeti[1] == 'db' or kiszereles_tenyleg[1] == 'db':
                    if kiszereles_eredeti[1] == 'db':
                        vegleges_kiszereles_1 = kiszereles_tenyleg
                        vegleges_kiszereles_2 = kiszereles_eredeti
                    else:
                        vegleges_kiszereles_1 = kiszereles_eredeti
                        vegleges_kiszereles_2 = kiszereles_tenyleg

                else:
                    if benne_van_sorkent(nev, "./elírt termékek/különböznek a mértékegységek.txt"):
                        if kiszereles_eredeti[1] == 'ml':
                            vegleges_kiszereles_1 = kiszereles_tenyleg
                            vegleges_kiszereles_2 = (1.0, 'db')
                        else:
                            vegleges_kiszereles_1 = kiszereles_eredeti
                            vegleges_kiszereles_2 = (1.0, 'db')
                    else:
                        if kiszereles_eredeti[1] == 'ml':
                            vegleges_kiszereles_1 = kiszereles_eredeti
                            vegleges_kiszereles_2 = (1.0, 'db')
                        else:
                            vegleges_kiszereles_1 = kiszereles_tenyleg
                            vegleges_kiszereles_2 = (1.0, 'db')

                    #print("tol:", kiszereles_eredeti, kiszereles_tenyleg, vegleges_kiszereles_1, vegleges_kiszereles_2, nev)
                    cnt3 = cnt3 + 1
        else:
            vegleges_kiszereles_1 = kiszereles_tenyleg
            #print("ok1:", kiszereles_eredeti, kiszereles_tenyleg, vegleges_kiszereles_1, vegleges_kiszereles_2, nev)

        if not egyedi_lepeskoz == "" and not egyedi_egyseg == "":
            vegleges_kiszereles_1 = float(egyedi_lepeskoz), egyedi_egyseg
            vegleges_kiszereles_1 = kiszereles_normalizalas(vegleges_kiszereles_1)

        if kiszereles_eredeti == kiszereles_tenyleg and kiszereles_eredeti == (None, None):
            print("hup:",nev)
            cnt2 = cnt2 + 1

        #PRICE
        unit_price = ""
        original_price = ""
        if not kiszereles == "":
            unit_price = int(float(ar)) / 100
            if len(eredeti_ar) > 0:
                original_price = int(float(eredeti_ar)) / 100
        elif not egyedi_kilos_ar == "":
            unit_price = int(float(egyedi_kilos_ar))*float(egyedi_lepeskoz)/1000/100
            if len(eredeti_ar) > 0 and len(eredeti_egyseg_ar) > 0:
                original_price = int(float(eredeti_egyseg_ar))*float(egyedi_lepeskoz)/1000/100
        elif not unit_ar == "":
            print(nev)
            if egyseg == "kilogram":
                unit_price = float(unit_ar)/float(lepeskoz)/100
        else:
            unit_price = int(float(ar)) / 100
            if len(eredeti_ar) > 0:
                original_price = int(float(eredeti_ar)) / 100

        store_name = uzlet
        store_product_id = termek_id
        product_name = f"{nev}"
        brand_name = None #marka or None
        available = False if keszleten == "sold out" else True
        expected_restock = None #varhato or None
        barcode = int(vonalkod) if vonalkod.isdigit() else None
        #unit_price = int(float(ar))/100 if ar else 0
        #unit_type = egyseg
        #unit_step = int(lepeskoz) if lepeskoz.isdigit() else None
        unit_type = vegleges_kiszereles_1[1]
        unit_step = vegleges_kiszereles_1[0]
        #print(eredeti_ar, print(len(eredeti_ar)))
        is_discounted = original_price != ""
        #print(nev)
        original_unit_price = original_price if is_discounted else None
        secondary_unit_price = None
        secondary_unit_type = vegleges_kiszereles_2[1]
        secondary_unit_step = vegleges_kiszereles_2[0]
        image_urls = ";".join([to_full_size(url) for url in [kep1, kep2] if url]) or None
        description = None #f"{leiras} {osszetevok}".strip() or None

        # ✍️ Írás a kimeneti fájlba
        writer.writerow({
            "store_name": store_name,
            "store_product_id": store_product_id,
            "product_name": product_name,
            "brand_name": brand_name,
            "available": available,
            "expected_restock": expected_restock,
            "barcode": barcode,
            "unit_price": unit_price,
            "unit_type": unit_type,
            "unit_step": unit_step,
            "is_discounted": is_discounted,
            "original_unit_price": original_unit_price,
            "secondary_unit_price": secondary_unit_price,  # használaton kívül
            "secondary_unit_type": secondary_unit_type,
            "secondary_unit_step": secondary_unit_step,
            "image_urls": image_urls,
            "description": description,
            "categories": slug
        })

print(cnt,"elteresek, kinyert kisebb")
print(cnt4,"elteresek, kinyert nagyobb")
print(cnt5,"elteresek, elenyésző")
print(cnt3,"más mértékegység")
print(cnt2,"üresek")
print(cnt_all,"összes")
