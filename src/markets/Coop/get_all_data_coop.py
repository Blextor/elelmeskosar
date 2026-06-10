import argparse
import csv
import html
import json
import os
import re
import time
from collections import defaultdict
from datetime import datetime

import requests


MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "coop"
DEFAULT_CATEGORY_FILE = "kategoriak.txt"
DEFAULT_API_BASE = "https://cooponline.hu/wp-json/wc/store/v1"
DEFAULT_REFERER = "https://cooponline.hu/termekeink/"
DEFAULT_PER_PAGE = 100
DEFAULT_FOOD_ROOT_SLUGS = [
    "ital",
    "edesseg-nassolni-valo",
    "konzerv",
    "tartos-elelmiszer",
    "teszta",
    "sutes-fozes",
    "sajtok-vajak-margarinok",
    "szalamik-kolbaszok",
    "zoldseg-gyumolcs-tojas",
    "fuszer",
    "kenyer-peksutemeny",
    "egeszseges-eletmod",
    "teak-es-mezek",
]
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def clean_text(value):
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def get_current_dir_name():
    return MARKET_NAME


def generate_filename(y_base, extension=".csv"):
    x = get_current_dir_name()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{now}{extension}"


def request_headers():
    return {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": DEFAULT_REFERER,
    }


def get_with_retries(session, url, params=None, retries=3, retry_delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        retry_after = None
        try:
            response = session.get(url, params=params, headers=request_headers(), timeout=60)
            response.encoding = "utf-8"
            if response.status_code == 200:
                return response
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


def get_json_with_retries(session, url, params=None, retries=3, retry_delay=2):
    return get_with_retries(session, url, params=params, retries=retries, retry_delay=retry_delay).json()


def parse_root_slugs(value):
    if not value:
        return DEFAULT_FOOD_ROOT_SLUGS
    return [clean_text(item) for item in value.split(",") if clean_text(item)]


def category_image_url(category):
    image = category.get("image")
    if isinstance(image, dict):
        return clean_text(image.get("src") or image.get("thumbnail"))
    return ""


def build_category_rows(categories, root_slugs):
    by_id = {category.get("id"): category for category in categories}
    children_by_parent = defaultdict(list)
    for category in categories:
        children_by_parent[category.get("parent", 0)].append(category.get("id"))

    root_ids = {category.get("id") for category in categories if category.get("slug") in set(root_slugs)}
    missing_roots = sorted(set(root_slugs) - {category.get("slug") for category in categories})
    if missing_roots:
        raise ValueError(f"Hiányzó Coop gyökérkategória slug(ok): {', '.join(missing_roots)}")

    food_scope_ids = set()

    def collect_descendants(category_id):
        if category_id in food_scope_ids:
            return
        food_scope_ids.add(category_id)
        for child_id in children_by_parent.get(category_id, []):
            collect_descendants(child_id)

    for root_id in root_ids:
        collect_descendants(root_id)

    path_cache = {}

    def path_for(category_id):
        if category_id in path_cache:
            return path_cache[category_id]
        category = by_id.get(category_id)
        if not category:
            return []
        parent_path = path_for(category.get("parent")) if category.get("parent") else []
        path = parent_path + [clean_text(category.get("name"))]
        path_cache[category_id] = path
        return path

    rows = []
    for category in sorted(categories, key=lambda item: (path_for(item.get("id")), item.get("id"))):
        category_id = category.get("id")
        if category_id not in food_scope_ids:
            continue
        parent = category.get("parent") or ""
        path_names = path_for(category_id)
        rows.append(
            {
                "index": len(rows),
                "id": category_id,
                "name": clean_text(category.get("name")),
                "slug": clean_text(category.get("slug")),
                "parent_id": parent,
                "count": category.get("count", 0),
                "child_count": len(children_by_parent.get(category_id, [])),
                "is_leaf": "true" if not children_by_parent.get(category_id) else "false",
                "is_fetch_root": "true" if category_id in root_ids else "false",
                "path": " > ".join(path_names),
                "path_ids": "|".join(str(item.get("id")) for item in (by_id.get(id_value) for id_value in path_cache_ids(category_id, by_id)) if item),
                "permalink": clean_text(category.get("permalink")),
                "image_url": category_image_url(category),
            }
        )
    return rows, root_ids


def path_cache_ids(category_id, by_id):
    ids = []
    current_id = category_id
    while current_id and current_id in by_id:
        ids.append(current_id)
        current_id = by_id[current_id].get("parent")
    return list(reversed(ids))


def save_categories(categories, category_file):
    fieldnames = [
        "index",
        "id",
        "name",
        "slug",
        "parent_id",
        "count",
        "child_count",
        "is_leaf",
        "is_fetch_root",
        "path",
        "path_ids",
        "permalink",
        "image_url",
    ]
    with open(category_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(categories)

    snapshot = generate_filename("categories")
    with open(snapshot, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(categories)
    return snapshot


def fetch_categories(session, args):
    data = get_json_with_retries(
        session,
        f"{args.api_base}/products/categories",
        retries=args.retries,
        retry_delay=args.retry_delay,
    )
    categories, root_ids = build_category_rows(data, parse_root_slugs(args.root_slugs))
    if not categories:
        raise ValueError("A Coop kategóriafa üres.")
    return categories, root_ids


def category_path_map(categories):
    return {str(row["id"]): row["path"] for row in categories}


def json_value(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def flatten(data, prefix=""):
    row = {}
    for key, value in data.items():
        if str(key).startswith("_"):
            continue
        column = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            row.update(flatten(value, column))
        elif isinstance(value, list):
            row[column] = json_value(value)
        else:
            row[column] = value
    return row


def product_category_paths(product, path_by_id):
    result = []
    for category in product.get("categories") or []:
        category_id = str(category.get("id"))
        path = path_by_id.get(category_id)
        if path and path not in result:
            result.append(path)
    return result


def fetch_products_for_category(session, args, category_row):
    products = []
    page = 1
    total_pages = None
    category_id = category_row["id"]

    while True:
        if args.page_limit and page > args.page_limit:
            break

        params = {
            "category": category_id,
            "per_page": args.per_page,
            "page": page,
        }
        response = get_with_retries(
            session,
            f"{args.api_base}/products",
            params=params,
            retries=args.retries,
            retry_delay=args.retry_delay,
        )
        page_products = response.json()
        if total_pages is None:
            try:
                total_pages = int(response.headers.get("X-WP-TotalPages") or 1)
            except ValueError:
                total_pages = 1
            total_items = response.headers.get("X-WP-Total") or ""
            print(
                f"Coop kategória: {category_row['name']} ({category_id}), "
                f"termékek: {total_items}, oldalak: {total_pages}",
                flush=True,
            )

        products.extend(page_products)
        print(f"  oldal {page}/{total_pages}: {len(page_products)} termék", flush=True)

        if not page_products or page >= total_pages:
            break
        page += 1
        if args.page_delay:
            time.sleep(args.page_delay)

    return products


def merge_product(existing, incoming, fetch_category, path_by_id):
    fetch_id = str(fetch_category["id"])
    fetch_name = clean_text(fetch_category["name"])
    fetch_path = clean_text(fetch_category["path"])
    existing.setdefault("_fetch_category_ids", set()).add(fetch_id)
    existing.setdefault("_fetch_category_names", set()).add(fetch_name)
    existing.setdefault("_fetch_category_paths", set()).add(fetch_path)
    for path in product_category_paths(incoming, path_by_id):
        existing.setdefault("_product_category_paths", set()).add(path)


def product_output_row(product, path_by_id):
    row = flatten(product)
    row["fetch_category_ids"] = json.dumps(sorted(product.get("_fetch_category_ids", [])), ensure_ascii=False)
    row["fetch_category_names"] = json.dumps(sorted(product.get("_fetch_category_names", [])), ensure_ascii=False)
    row["fetch_category_paths"] = json.dumps(sorted(product.get("_fetch_category_paths", [])), ensure_ascii=False)
    row["product_category_paths"] = json.dumps(sorted(product.get("_product_category_paths", [])), ensure_ascii=False)
    if not row.get("product_category_paths"):
        row["product_category_paths"] = json.dumps(product_category_paths(product, path_by_id), ensure_ascii=False)
    return row


def write_rows(path, rows):
    fieldnames = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_failed(path, failed_rows):
    fieldnames = ["category_id", "category_name", "category_path", "error"]
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(failed_rows)


def parse_args():
    parser = argparse.ArgumentParser(description="CoopOnline élelmiszer termékek letöltése WooCommerce Store API-ból.")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--category-file", default=DEFAULT_CATEGORY_FILE)
    parser.add_argument("--root-slugs", default=",".join(DEFAULT_FOOD_ROOT_SLUGS))
    parser.add_argument("--per-page", type=int, default=DEFAULT_PER_PAGE)
    parser.add_argument("--category-limit", type=int, default=None)
    parser.add_argument("--page-limit", type=int, default=None)
    parser.add_argument("--page-delay", type=float, default=0.0)
    parser.add_argument("--category-delay", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--allow-partial-download", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    products_by_id = {}
    failed_rows = []

    with requests.Session() as session:
        categories, root_ids = fetch_categories(session, args)
        category_snapshot = save_categories(categories, args.category_file)
        path_by_id = category_path_map(categories)
        fetch_categories_rows = [row for row in categories if row["id"] in root_ids]
        fetch_categories_rows.sort(key=lambda row: row["path"])
        if args.category_limit:
            fetch_categories_rows = fetch_categories_rows[: args.category_limit]

        print(f"Coop kategóriafájl mentve: {category_snapshot}")
        print(f"Letöltendő Coop gyökérkategóriák: {len(fetch_categories_rows)}")

        for index, category in enumerate(fetch_categories_rows, start=1):
            print(f"[{index}/{len(fetch_categories_rows)}] {category['path']}", flush=True)
            try:
                products = fetch_products_for_category(session, args, category)
                for product in products:
                    product_id = product.get("id")
                    if product_id not in products_by_id:
                        products_by_id[product_id] = product
                    merge_product(products_by_id[product_id], product, category, path_by_id)
            except Exception as error:
                failed_rows.append(
                    {
                        "category_id": category["id"],
                        "category_name": category["name"],
                        "category_path": category["path"],
                        "error": str(error),
                    }
                )
                if not args.allow_partial_download:
                    raise

            if args.category_delay:
                time.sleep(args.category_delay)

    rows = [product_output_row(product, path_by_id) for product in products_by_id.values()]
    output_file = generate_filename("all_data")
    write_rows(output_file, rows)
    print(f"{len(rows)} Coop termék mentve ide: {output_file}")

    failed_file = generate_filename("failed_requests")
    write_failed(failed_file, failed_rows)
    print(f"{len(failed_rows)} sikertelen Coop kategória mentve ide: {failed_file}")


if __name__ == "__main__":
    main()
