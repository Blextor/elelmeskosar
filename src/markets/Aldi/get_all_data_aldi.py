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
MARKET_NAME = "aldi"
DEFAULT_CATEGORY_FILE = "kategoriak.txt"
DEFAULT_PAGE_URL = "https://www.roksh.com/aldi/kezdooldal"
DEFAULT_API_BASE_URL = "https://shopservice.roksh.com"
DEFAULT_PROVIDER_ROUTE = "aldi"
DEFAULT_PROVIDER_CODE = "ALDI"
DEFAULT_PROVIDER_ID = 13
DEFAULT_PAGE_SIZE = 100
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
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "hu-HU,hu;q=0.9,en;q=0.8",
        "Origin": "https://www.roksh.com",
        "Referer": referer,
    }


def get_json_with_retries(session, method, url, params=None, json_body=None, headers=None, retries=3, retry_delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        retry_after = None
        try:
            response = session.request(
                method,
                url,
                params=params,
                json=json_body,
                headers=headers,
                timeout=60,
            )
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


def configure_session(session, args):
    body = {
        "UserSelectedShops": [],
        "RedirectToDashboardNeeded": False,
        "SetUserSelectedShopsOnFirstSiteLoad": True,
        "ShopsSelectedForRoot": args.provider_route,
        "OwnWebshopProviderCode": None,
    }
    data = get_json_with_retries(
        session=session,
        method="POST",
        url=f"{args.api_base_url.rstrip('/')}/session/configure",
        json_body=body,
        headers=request_headers(args.page_url),
        retries=args.retries,
        retry_delay=args.retry_delay,
    )

    selected_codes = data.get("SelectedShopCodes") or []
    selected_ids = data.get("SelectedShopIds") or []
    selected_names = data.get("SelectedShops") or []
    if selected_codes:
        args.provider_code = selected_codes[0]
    if selected_ids:
        args.provider_id = int(selected_ids[0])

    print(
        "Aldi session: "
        f"nev={selected_names[0] if selected_names else ''}, "
        f"provider_code={args.provider_code}, provider_id={args.provider_id}",
        flush=True,
    )
    return data


def fetch_category_tree(session, args):
    params = {
        "providerCode": args.provider_code,
        "isOwnWebshop": "false",
    }
    data = get_json_with_retries(
        session=session,
        method="GET",
        url=f"{args.api_base_url.rstrip('/')}/category/GetFullCategoryList",
        params=params,
        headers=request_headers(args.page_url),
        retries=args.retries,
        retry_delay=args.retry_delay,
    )
    if not isinstance(data, list):
        raise RuntimeError("Az Aldi kategoria API nem listat adott vissza.")
    return data


def flatten_categories(categories):
    rows = []

    def visit(category, parent_id="", path_parts=None, path_id_parts=None):
        path_parts = list(path_parts or []) + [clean_text(category.get("CategoryName"))]
        path_id_parts = list(path_id_parts or []) + [str(category.get("CategoryID") or "")]
        children = category.get("ChildList") or []
        row = {
            "index": 0,
            "id": category.get("CategoryID") or "",
            "name": clean_text(category.get("CategoryName")),
            "prog_id": clean_text(category.get("ProgID")),
            "parent_id": parent_id,
            "level": category.get("Level") or "",
            "path": " > ".join(part for part in path_parts if part),
            "path_ids": "|".join(part for part in path_id_parts if part),
            "is_leaf": not bool(children),
            "is_root": bool(category.get("IsRoot")),
            "status": clean_text(category.get("Status")),
            "product_count": 0,
            "child_count": len(children),
        }
        rows.append(row)
        for child in children:
            visit(child, row["id"], path_parts, path_id_parts)

    for root in categories:
        visit(root)

    rows.sort(key=lambda row: (int(row["level"] or 0), row["path"]))
    for index, row in enumerate(rows):
        row["index"] = index
    return rows


def category_filter(rows, args):
    selected_prog_ids = {item.strip() for item in (args.category_prog_ids or "").split(",") if item.strip()}
    if selected_prog_ids:
        selected_rows = [row for row in rows if row["prog_id"] in selected_prog_ids]
    elif args.fetch_mode == "root":
        selected_rows = [row for row in rows if row["is_root"] and row["prog_id"]]
    else:
        selected_rows = [row for row in rows if row["is_leaf"] and row["prog_id"]]
    if args.category_limit:
        selected_rows = selected_rows[: args.category_limit]
    return selected_rows


def product_list_params(args, category_row, page):
    include_children = bool(category_row.get("child_count")) or args.children_category_products_needed
    return {
        "UserSession.UserSelectedShopCodes": args.provider_code,
        "UserSession.UserSelectedShopIds": str(args.provider_id),
        "CategoryProgId": category_row["prog_id"],
        "Paging": "true",
        "ItemsPerPage": str(args.page_size),
        "Page": str(page),
        "UserSelectedProviderCodeArray": args.provider_code,
        "ChildrenCategoryProductsNeeded": str(include_children).lower(),
    }


def fetch_product_page(session, args, category_row, page):
    referer = f"https://www.roksh.com/{args.provider_route}/termekek/{category_row['prog_id']}"
    return get_json_with_retries(
        session=session,
        method="GET",
        url=f"{args.api_base_url.rstrip('/')}/productlist/GetProductList",
        params=product_list_params(args, category_row, page),
        headers=request_headers(referer),
        retries=args.retries,
        retry_delay=args.retry_delay,
    )


def product_key(product):
    product_id = clean_text(product.get("productID"))
    if product_id:
        return product_id
    providers = product.get("productProvider") or []
    if providers and isinstance(providers[0], dict):
        provider_product_id = clean_text(providers[0].get("productID"))
        if provider_product_id:
            return provider_product_id
    return clean_text(product.get("productName"))


def fetch_category_products(session, args, category_row, category_index, category_count, category_by_prog_id):
    products = []
    failed_pages = []
    page = 1
    total_pages = None
    total_items = None

    while total_pages is None or page <= total_pages:
        if args.page_limit and page > args.page_limit:
            break
        try:
            data = fetch_product_page(session, args, category_row, page)
            page_products = data.get("ProductList") or []
            total_items = int(data.get("TotalItems") or 0)
            total_pages = int(data.get("TotalPages") or 0)
            if total_pages <= 0:
                total_pages = max(1, math.ceil(total_items / max(1, args.page_size)))

            for rank, product in enumerate(page_products, start=1):
                product = dict(product)
                product_category = product.get("category") or {}
                actual_prog_id = clean_text(product_category.get("progID") or product.get("categorySEOName"))
                actual_category = category_by_prog_id.get(actual_prog_id, category_row)
                product["fetch_category_id"] = actual_category["id"]
                product["fetch_category_name"] = actual_category["name"]
                product["fetch_category_prog_id"] = actual_category["prog_id"]
                product["fetch_category_path"] = actual_category["path"]
                product["fetch_category_level"] = actual_category["level"]
                product["fetch_requested_category_id"] = category_row["id"]
                product["fetch_requested_category_name"] = category_row["name"]
                product["fetch_requested_category_prog_id"] = category_row["prog_id"]
                product["fetch_requested_category_path"] = category_row["path"]
                product["fetch_page"] = page
                product["fetch_rank"] = (page - 1) * args.page_size + rank
                product["fetch_provider_code"] = args.provider_code
                product["fetch_provider_id"] = args.provider_id
                product["fetch_provider_route"] = args.provider_route
                products.append(product)

            if args.verbose or page == 1 or page == total_pages:
                print(
                    f"Aldi kategoria {category_index}/{category_count}: "
                    f"{category_row['path']} | oldal {page}/{total_pages}, "
                    f"{len(page_products)} sor, total={total_items}",
                    flush=True,
                )

            if not page_products:
                break
            page += 1
        except Exception as error:
            failed_pages.append(
                {
                    "category_id": category_row["id"],
                    "category_name": category_row["name"],
                    "category_prog_id": category_row["prog_id"],
                    "category_path": category_row["path"],
                    "page": page,
                    "error": str(error),
                }
            )
            print(f"Aldi termeklista hiba: {category_row['path']} / oldal {page} - {error}", flush=True)
            if not args.allow_partial_download:
                raise
            if total_pages is None:
                # Az elso sikeres valasz elott nem ismert az oldalszam, ilyenkor
                # a tovabbi probalkozas vegtelen ciklushoz vezetne.
                break
            page += 1

        if args.page_delay:
            time.sleep(args.page_delay)

    return products, failed_pages, total_items or 0


def collect_products(session, args, category_rows, all_category_rows):
    products_by_key = {}
    failed_pages = []
    category_product_counts = {}
    category_by_prog_id = {row["prog_id"]: row for row in all_category_rows if row["prog_id"]}

    for index, category_row in enumerate(category_rows, start=1):
        products, failures, total_items = fetch_category_products(
            session=session,
            args=args,
            category_row=category_row,
            category_index=index,
            category_count=len(category_rows),
            category_by_prog_id=category_by_prog_id,
        )
        failed_pages.extend(failures)
        for product in products:
            key = product_key(product)
            if not key:
                continue
            category_info = {
                "id": product.get("fetch_category_id"),
                "name": product.get("fetch_category_name"),
                "prog_id": product.get("fetch_category_prog_id"),
                "path": product.get("fetch_category_path"),
            }
            category_id = str(category_info["id"] or "")
            category_product_counts[category_id] = category_product_counts.get(category_id, 0) + 1
            if key not in products_by_key:
                row = dict(product)
                row["fetch_categories"] = [category_info]
                row["fetch_category_paths"] = category_info["path"] or ""
                products_by_key[key] = row
            else:
                existing = products_by_key[key]
                existing_categories = existing.setdefault("fetch_categories", [])
                if category_info not in existing_categories:
                    existing_categories.append(category_info)
                paths = [item.get("path") for item in existing_categories if item.get("path")]
                existing["fetch_category_paths"] = " | ".join(dict.fromkeys(paths))

        if args.category_delay:
            time.sleep(args.category_delay)

    return list(products_by_key.values()), failed_pages, category_product_counts


def save_categories(rows, category_product_counts, args):
    path_counts = {}
    rows_by_id = {str(row["id"]): row for row in rows}
    for category_id, count in category_product_counts.items():
        row = rows_by_id.get(str(category_id))
        if not row:
            continue
        path_counts[row["path"]] = path_counts.get(row["path"], 0) + count

    for row in rows:
        row_path = row["path"]
        prefix = row_path + " > "
        row["product_count"] = sum(
            count for path, count in path_counts.items() if path == row_path or path.startswith(prefix)
        )

    fieldnames = [
        "index",
        "id",
        "name",
        "prog_id",
        "parent_id",
        "level",
        "path",
        "path_ids",
        "is_leaf",
        "is_root",
        "status",
        "product_count",
        "child_count",
    ]
    with open(args.category_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    snapshot = generate_filename("categories")
    pd.DataFrame(rows).to_csv(snapshot, index=False)
    return snapshot


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
        raise RuntimeError("Az Aldi letoltes 0 termeket adott vissza, ezert nem irok ures all_data fajlt.")
    df = pd.json_normalize(products)
    df = make_dataframe_csv_safe(df)
    output_file = generate_filename("all_data")
    df.to_csv(output_file, index=False)
    return output_file


def save_failed_requests(failed_pages):
    if not failed_pages:
        return None
    output_file = generate_filename("failed_requests")
    pd.DataFrame(failed_pages).to_csv(output_file, index=False)
    return output_file


def parse_args():
    parser = argparse.ArgumentParser(description="Aldi/Roksh kategoriak es termekek letoltese.")
    parser.add_argument("--api-base-url", default=DEFAULT_API_BASE_URL)
    parser.add_argument("--page-url", default=DEFAULT_PAGE_URL)
    parser.add_argument("--provider-route", default=DEFAULT_PROVIDER_ROUTE)
    parser.add_argument("--provider-code", default=DEFAULT_PROVIDER_CODE)
    parser.add_argument("--provider-id", type=int, default=DEFAULT_PROVIDER_ID)
    parser.add_argument("--category-file", default=DEFAULT_CATEGORY_FILE)
    parser.add_argument("--category-prog-ids", default="", help="Vesszovel elvalasztott levellista gyors probahoz.")
    parser.add_argument("--fetch-mode", choices=["root", "leaf"], default="root")
    parser.add_argument("--children-category-products-needed", action="store_true")
    parser.add_argument("--category-limit", type=int, default=0)
    parser.add_argument("--page-limit", type=int, default=0)
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    parser.add_argument("--category-delay", type=float, default=0.05)
    parser.add_argument("--page-delay", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2)
    parser.add_argument("--allow-partial-download", action="store_true")
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(MAIN_FOLDER, exist_ok=True)

    with requests.Session() as session:
        configure_session(session, args)
        category_tree = fetch_category_tree(session, args)
        category_rows = flatten_categories(category_tree)
        fetch_categories = category_filter(category_rows, args)

        print(
            f"Aldi kategoriak: {len(category_rows)} osszesen, "
            f"{len(fetch_categories)} kivalasztott kategoria lesz lekerve ({args.fetch_mode} mod).",
            flush=True,
        )

        products, failed_pages, category_product_counts = collect_products(session, args, fetch_categories, category_rows)

    categories_output = save_categories(category_rows, category_product_counts, args)
    products_output = save_products(products)
    failed_output = save_failed_requests(failed_pages)

    print(f"Aldi kategoriak mentve: {args.category_file}")
    print(f"Aldi kategoria snapshot: {categories_output}")
    print(f"Aldi nyers termekadatok mentve: {products_output}")
    print(f"Aldi egyedi termekek: {len(products)}")
    if failed_output:
        print(f"Aldi sikertelen lekeresek mentve: {failed_output}")
    else:
        print("Aldi sikertelen lekeres: 0")


if __name__ == "__main__":
    main()
