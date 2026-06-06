import requests
import json
import time

# Kategóriakódok beolvasása
with open("kodolt_kategoriak_2025_07_21.txt", "r", encoding="utf-8") as f:
    category_codes = [line.strip() for line in f if line.strip()]
with open("kat1_2025_07_21.txt", "r", encoding="utf-8") as f:
    category_names = [line.strip() for line in f if line.strip()]

url = "https://api.tesco.com/shoppingexperience"

headers = {
    "Connection": "keep-alive",
    "Origin": "https://bevasarlas.tesco.hu",
    "Referer": "https://bevasarlas.tesco.hu/groceries/hu-HU",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "accept": "application/json",
    "accept-language": "hu-HU",
    "content-type": "application/json",
    "language": "hu-HU",
    "region": "HU",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "x-apikey": "TvOSZJHlEk0pjniDGQFAc9Q59WGAR4dA"
}

all_products = []
cat_cnt = len(category_codes)
i = 0
for code in category_codes:
    print(f"Kategória feldolgozása {i+1}/{cat_cnt}: {category_names[i]}")
    i = i + 1
    facet = "b;" + code
    page = 1
    total_pages = 1

    while page <= total_pages:
        payload = {
            "operationName": "GetCategoryProducts",
            "variables": {
                "page": page,
                "includeRestrictions": True,
                "includeVariations": True,
                "showStarRating": False,
                "showDepositReturnCharge": True,
                "count": 100,
                "facet": facet,
                "configs": [
                    {
                        "featureKey": "dynamic_filter",
                        "params": [{"name": "enable", "value": "true"}]
                    }
                ],
                "filterCriteria": [
                    {"name": "0", "values": ["groceries"]}
                ],
                "appliedFacetArgs": [],
                "sortBy": "relevance"
            },
            "extensions": {
                "mfeName": "unknown"
            },
            "query": "query GetCategoryProducts($facet: ID, $page: Int = 1, $count: Int, $sortBy: String, $offset: Int, $favourites: Boolean, $configs: [ConfigArgType], $filterCriteria: [filterCriteria], $appliedFacetArgs: [AppliedFacetArgs]) { category(page: $page, count: $count, configs: $configs, sortBy: $sortBy, offset: $offset, facet: $facet, favourites: $favourites, filterCriteria: $filterCriteria, appliedFacetArgs: $appliedFacetArgs) { pageInformation: info { totalCount: total pageNo: page } results { node { ... on MPProduct { id title brandName price { actual unitPrice } } ... on ProductType { id title brandName price { actual unitPrice } } } } } }"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print(f"⚠️ Hiba ({response.status_code}) a(z) {code} kóddal")
            break

        try:
            data = response.json()
        except ValueError:
            print("⚠️ Nem JSON válasz")
            break

        #print(data)

        category_data = data.get("data", {}).get("category", {})
        if not category_data:
            print("⚠️ Nincs adat a válaszban.")
            break

        # Lapozáshoz a termékszám alapján
        total_count = category_data.get("pageInformation", {}).get("totalCount", 0)
        total_pages = (total_count + 99) // 100

        if total_count == 0:
            print("Hiba: Nincs termék a kategóriában.")

        for item in category_data.get("results", []):
            product = item.get("node", {})
            product["category_code"] = code
            all_products.append(product)

        print(f" → Oldal {page}/{total_pages} ({len(all_products)} termék eddig)")
        page += 1

        time.sleep(1)  # kíméljük az API-t

#exit(0)

# Eredmény mentése
with open("kategoriak_termekei_2025_07_21.json", "w", encoding="utf-8") as f:
    json.dump(all_products, f, indent=2, ensure_ascii=False)

print(f"✅ Lekérdezés kész. Termékek száma: {len(all_products)}")
print("→ kategoriak_termekei_2025_07_21.json létrehozva.")
