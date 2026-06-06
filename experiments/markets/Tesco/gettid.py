import json

# JSON fájl beolvasása
with open("kategoriak_termekei_2025_07_21.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# ID-k kigyűjtése a lista elemeiből
ids = [item["id"] for item in data if "id" in item]

# Duplikált ID-k eltávolítása
unique_ids = list(set(ids))

# Eredmény mentése csak az ID-kal, fejléc nélkül
with open("csak_id_k_lista2.csv", "w", encoding="utf-8") as file:
    for uid in unique_ids:
        file.write(uid + "\n")
