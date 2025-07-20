import csv
import requests
import time
import json
import pandas as pd
import os
import glob
from datetime import datetime

MAIN_FOLDER = "./../../../data/markets_data/"
def get_current_dir_name():
    return os.path.basename(os.getcwd()).lower()

def generate_filename(y_base, extension=".csv"):
    x = get_current_dir_name()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{now}{extension}"

def save_file(content: str, y_base: str, extension=".csv"):
    filename = generate_filename(y_base, extension)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Mentve: {filename}")
    return filename

BASE_URL = "https://consumer-api.wolt.com/consumer-api/consumer-assortment/v1/venues/slug/interspar-szentendre/assortment/categories/slug/"

# 1. Slugok beolvasása
slugok = []
with open("kategoriak.txt", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        slug = row.get("slug")
        if slug:
            slugok.append(slug)

# 2. Lekérdezés, duplikációmentes tárolás
items_dict = {}

for slug in slugok:
    next_token = None
    while True:
        url = f"{BASE_URL}{slug}?language=hu"
        if next_token:
            url += f"&page_token={next_token}"

        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                print(f"{slug}: HTTP {resp.status_code}")
                break

            data = resp.json()
            for item in data.get("items", []):
                item_id = item.get("id")
                if item_id:
                    items_dict[item_id] = item  # duplikáció elkerülése

            token = data.get("metadata", {}).get("next_page_token")
            if not token:
                break
            next_token = token

        except Exception as e:
            print(f"{slug}: hiba – {e}")
            break

        time.sleep(2)

    print(f"{slug}: kész ({len(items_dict)} egyedi item eddig)")

# 3. Mentés JSON-be
osszes_item = list(items_dict.values())
#with open("osszes_termek.json", "w", encoding="utf-8") as f:
#    json.dump(osszes_item, f, ensure_ascii=False, indent=2)

# 4. Mentés CSV-be
df = pd.json_normalize(osszes_item)
file_name = generate_filename("all_data")
df.to_csv(file_name, index=False)

print(f"\n✅ Mentés kész: {len(osszes_item)} egyedi termék",file_name)
