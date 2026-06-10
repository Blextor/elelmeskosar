import argparse
import csv
import json
import math
import os
import re
import time
from datetime import datetime

import pandas as pd
import requests


MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "lidl"
DEFAULT_CATEGORY_FILE = "kategoriak.txt"
DEFAULT_PAGE_URL = "https://www.lidl.hu/c/etel-ital/s10068374"
DEFAULT_SEARCH_API_URL = "https://www.lidl.de/q/api/search"
DEFAULT_CATEGORY_ID = "10068374"
DEFAULT_CATEGORY_NAME = "Étel & ital"
DEFAULT_LOCALE = "hu_HU"
DEFAULT_ASSORTMENT = "HU"
DEFAULT_SEARCH_VERSION = "2.1.0"
DEFAULT_FETCH_SIZE = 108
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def get_current_dir_name():
    return MARKET_NAME


def generate_filename(y_base, extension=".csv"):
    x = get_current_dir_name()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{now}{extension}"


def request_headers(referer=DEFAULT_PAGE_URL):
    return {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/mindshift.search+json;version=2",
        "Accept-Language": "hu-HU,hu;q=0.9,en;q=0.8",
        "Referer": referer,
    }


def get_json_with_retries(session, url, params=None, headers=None, retries=3, retry_delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        retry_after = None
        try:
            response = session.get(url, params=params, headers=headers, timeout=60)
            response.encoding = "utf-8"
            if response.status_code == 200:
                return response.json()
            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()
            retry_after = response.headers.get("Retry-After")
            last_error = requests.HTTPError(f"HTTP {response.status_code}: {response.url}")
        except requests.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else None
            if status_code not in RETRYABLE_STATUS_CODES:
                raise
            last_error = error
        except Exception as error:
            last_error = error

        if attempt < retries:
            delay = retry_delay * attempt
            if retry_after:
                try:
                    delay = max(delay, float(retry_after))
                except ValueError:
                    pass
            time.sleep(delay)

    raise last_error


def search_params(args, offset):
    return {
        "assortment": args.assortment,
        "locale": args.locale,
        "version": args.search_version,
        "sort": args.sort,
        "category.id": args.category_id,
        "fetchsize": str(args.fetch_size),
        "offset": str(offset),
    }


def fetch_search_page(session, args, offset):
    return get_json_with_retries(
        session=session,
        url=args.search_api_url,
        params=search_params(args, offset),
        headers=request_headers(args.page_url),
        retries=args.retries,
        retry_delay=args.retry_delay,
    )


def item_code(item):
    data = (item.get("gridbox") or {}).get("data") or {}
    return clean_text(item.get("code") or data.get("erpNumber") or data.get("productId") or data.get("itemId"))


def collect_products(session, args):
    products_by_code = {}
    failed_pages = []
    offset = 0
    num_found = None
    page_index = 1

    while num_found is None or offset < num_found:
        if args.page_limit and page_index > args.page_limit:
            break

        try:
            data = fetch_search_page(session, args, offset)
            num_found = int(data.get("numFound") or 0)
            actual_fetch_size = int(data.get("fetchsize") or args.fetch_size or DEFAULT_FETCH_SIZE)
            page_items = data.get("items") or []
            response_offset = int(data.get("offset") or offset)

            for rank, item in enumerate(page_items, start=1):
                code = item_code(item)
                if not code:
                    continue
                row = dict(item)
                row["fetch_category_id"] = args.category_id
                row["fetch_category_name"] = args.category_name
                row["fetch_category_url"] = args.page_url
                row["search_offset"] = response_offset
                row["search_rank"] = response_offset + rank
                products_by_code[code] = row

            total_pages = max(1, math.ceil(num_found / max(1, actual_fetch_size)))
            print(
                f"Lidl oldal {page_index}/{total_pages}: offset={response_offset}, "
                f"{len(page_items)} sor, {len(products_by_code)} egyedi termék, numFound={num_found}",
                flush=True,
            )

            if not page_items:
                break
            offset = response_offset + actual_fetch_size
            page_index += 1
        except Exception as error:
            failed_pages.append({"offset": offset, "error": str(error)})
            print(f"Lidl keresési oldal hiba: offset={offset} - {error}", flush=True)
            if not args.allow_partial_download:
                raise
            if num_found is None:
                # Az első sikeres válasz előtt nem ismert a találatszám, ilyenkor
                # a további próbálkozás végtelen ciklushoz vezetne.
                break
            offset += args.fetch_size
            page_index += 1

        if args.page_delay:
            time.sleep(args.page_delay)

    return list(products_by_code.values()), failed_pages, num_found or 0


def split_category_path(path):
    parts = [clean_text(part) for part in clean_text(path).split("/") if clean_text(part)]
    return parts


def build_category_rows(products, args):
    rows_by_path = {}
    root_path = args.category_name
    rows_by_path[root_path] = {
        "index": 0,
        "id": args.category_id,
        "name": args.category_name,
        "parent_id": "",
        "path": root_path,
        "path_ids": args.category_id,
        "source": "root",
        "product_count": 0,
        "url": args.page_url,
    }

    for item in products:
        data = (item.get("gridbox") or {}).get("data") or {}
        keyfacts = data.get("keyfacts") or {}
        path = clean_text(keyfacts.get("wonCategoryPrimary") or data.get("category"))
        path_ids = clean_text(keyfacts.get("wonCategoryPrimaryPath"))
        if not path:
            continue

        parts = split_category_path(path)
        id_parts = [clean_text(part) for part in path_ids.split("/") if clean_text(part)]
        for depth in range(len(parts)):
            current_parts = parts[: depth + 1]
            current_path = " > ".join(current_parts)
            current_id_parts = id_parts[: depth + 1] if id_parts else []
            row = rows_by_path.setdefault(
                current_path,
                {
                    "index": 0,
                    "id": current_id_parts[-1] if current_id_parts else "",
                    "name": current_parts[-1],
                    "parent_id": current_id_parts[-2] if len(current_id_parts) > 1 else "",
                    "path": current_path,
                    "path_ids": "|".join(current_id_parts),
                    "source": "product_won_category",
                    "product_count": 0,
                    "url": "",
                },
            )
            row["product_count"] += 1

        root = rows_by_path[root_path]
        root["product_count"] += 1

    rows = sorted(rows_by_path.values(), key=lambda row: (row["path"].count(" > "), row["path"]))
    for index, row in enumerate(rows):
        row["index"] = index
    return rows


def save_categories(products, args):
    categories = build_category_rows(products, args)
    fieldnames = ["index", "id", "name", "parent_id", "path", "path_ids", "source", "product_count", "url"]
    with open(args.category_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(categories)

    snapshot = generate_filename("categories")
    pd.DataFrame(categories).to_csv(snapshot, index=False)
    return snapshot, categories


def make_csv_safe(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def make_dataframe_csv_safe(df):
    for column in df.columns:
        df[column] = df[column].map(make_csv_safe)
    return df


def save_products(products):
    if not products:
        raise RuntimeError("A Lidl letöltés 0 terméket adott vissza, ezért nem írok üres all_data fájlt.")
    df = pd.json_normalize(products)
    df = make_dataframe_csv_safe(df)
    output_file = generate_filename("all_data")
    df.to_csv(output_file, index=False)
    return output_file


def save_failures(failed_pages):
    if not failed_pages:
        return None
    output_file = generate_filename("failed_requests")
    pd.DataFrame(failed_pages).to_csv(output_file, index=False)
    return output_file


def parse_args():
    parser = argparse.ArgumentParser(description="Lidl Étel & ital termékek letöltése a Lidl search API-ból.")
    parser.add_argument("--search-api-url", default=DEFAULT_SEARCH_API_URL)
    parser.add_argument("--page-url", default=DEFAULT_PAGE_URL)
    parser.add_argument("--category-id", default=DEFAULT_CATEGORY_ID)
    parser.add_argument("--category-name", default=DEFAULT_CATEGORY_NAME)
    parser.add_argument("--category-file", default=DEFAULT_CATEGORY_FILE)
    parser.add_argument("--locale", default=DEFAULT_LOCALE)
    parser.add_argument("--assortment", default=DEFAULT_ASSORTMENT)
    parser.add_argument("--search-version", default=DEFAULT_SEARCH_VERSION)
    parser.add_argument("--sort", default="relevancy")
    parser.add_argument("--fetch-size", type=int, default=DEFAULT_FETCH_SIZE)
    parser.add_argument("--page-limit", type=int)
    parser.add_argument("--page-delay", type=float, default=0.05)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--allow-partial-download", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    args.fetch_size = max(1, int(args.fetch_size))

    with requests.Session() as session:
        products, failed_pages, num_found = collect_products(session, args)

    category_snapshot, categories = save_categories(products, args)
    output_file = save_products(products)
    failed_file = save_failures(failed_pages)

    print(f"Lidl kategóriák mentve: {args.category_file} és {category_snapshot}")
    print(f"Lidl termékadatok mentve: {output_file}")
    print(f"Kereső numFound: {num_found}")
    print(f"Egyedi termékek: {len(products)}")
    print(f"Kategóriaútvonalak: {len(categories)}")
    if failed_file:
        print(f"Sikertelen oldalak: {len(failed_pages)} ({failed_file})")
    else:
        print("Sikertelen oldalak: 0")

    if failed_pages and not args.allow_partial_download:
        raise RuntimeError(f"{len(failed_pages)} Lidl oldal letöltése sikertelen volt.")


if __name__ == "__main__":
    main()
