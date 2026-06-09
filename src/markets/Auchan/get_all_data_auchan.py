import argparse
import csv
import math
import os
import re
import time
from datetime import datetime

import pandas as pd
import requests


MAIN_FOLDER = "./../../../data/markets_data/"
DEFAULT_SHOP_URL = "https://auchan.hu/shop"
DEFAULT_FE_TOKEN_URL = "https://auchan.hu/fe-api/get-token"
DEFAULT_API_BASE = "https://auchan.hu/api/v2"
DEFAULT_CATEGORY_FILE = "kategoriak.txt"
DEFAULT_AREA_TYPE = "department_store"
DEFAULT_AREA_ID = 47
DEFAULT_COUNT = 100
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def get_current_dir_name():
    return os.path.basename(os.getcwd()).lower()


def generate_filename(y_base, extension=".csv"):
    x = get_current_dir_name()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{now}{extension}"


def request_headers(access_token=None):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Referer": DEFAULT_SHOP_URL,
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


def get_with_retries(session, url, headers, params=None, retries=3, retry_delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        retry_after = None
        try:
            response = session.get(url, headers=headers, params=params, timeout=40)
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


def post_with_retries(session, url, headers, payload, retries=3, retry_delay=2):
    last_error = None
    for attempt in range(1, retries + 1):
        retry_after = None
        try:
            response = session.post(url, headers=headers, json=payload, timeout=40)
            if response.status_code in {200, 201, 202, 204}:
                if not response.text.strip():
                    return None
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


def login_anonymous(session, retries, retry_delay):
    data = post_with_retries(
        session=session,
        url=DEFAULT_FE_TOKEN_URL,
        headers=request_headers(),
        payload={"grant_type": "anonymous"},
        retries=retries,
        retry_delay=retry_delay,
    )
    access_token = data.get("access_token") if isinstance(data, dict) else None
    if not access_token:
        raise ValueError("Az Auchan anon token valasz nem tartalmaz access_token mezot.")
    return access_token


def setup_delivery_area(session, api_base, headers, area_type, area_id, retries, retry_delay):
    post_with_retries(
        session=session,
        url=f"{api_base}/delivery-area",
        headers=headers,
        payload={"type": area_type, "areaId": int(area_id)},
        retries=retries,
        retry_delay=retry_delay,
    )
    return get_with_retries(
        session=session,
        url=f"{api_base}/delivery-area",
        headers=headers,
        retries=retries,
        retry_delay=retry_delay,
    )


def flatten_categories(root):
    rows = []

    def walk(node, parent_id="", path_names=None, path_ids=None):
        path_names = list(path_names or [])
        path_ids = list(path_ids or [])
        node_id = node.get("id", "")
        name = clean_text(node.get("name", ""))
        children = node.get("children") or []
        current_path_names = path_names + ([name] if name and name != "root" else [])
        current_path_ids = path_ids + ([str(node_id)] if node_id != "" and node_id is not None else [])
        rows.append(
            {
                "index": len(rows),
                "id": node_id,
                "name": name,
                "slug": clean_text(node.get("slug", "")),
                "parent_id": parent_id,
                "level": node.get("level", ""),
                "product_count": node.get("productCount", 0) or 0,
                "discounted_count": node.get("discountedCount", 0) or 0,
                "child_count": node.get("childCount", len(children)) or len(children),
                "is_leaf": "true" if not children else "false",
                "path": " > ".join(current_path_names),
                "path_ids": "|".join(current_path_ids),
                "thumbnail_url": clean_text(node.get("thumbnailUrl", "")),
                "mobile_image_url": clean_text(node.get("mobileImageUrl", "")),
            }
        )
        for child in children:
            walk(child, node_id, current_path_names, current_path_ids)

    walk(root)
    return rows


def save_categories(categories, category_file):
    fieldnames = [
        "index",
        "id",
        "name",
        "slug",
        "parent_id",
        "level",
        "product_count",
        "discounted_count",
        "child_count",
        "is_leaf",
        "path",
        "path_ids",
        "thumbnail_url",
        "mobile_image_url",
    ]
    with open(category_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(categories)
    snapshot = generate_filename("categories")
    pd.DataFrame(categories).to_csv(snapshot, index=False)
    return snapshot


def fetch_current_categories(session, api_base, headers, retries, retry_delay):
    root = get_with_retries(
        session=session,
        url=f"{api_base}/tree/0",
        headers=headers,
        retries=retries,
        retry_delay=retry_delay,
    )
    categories = flatten_categories(root)
    if not categories:
        raise ValueError("Az Auchan kategoriafa ures.")
    return categories, root


def product_key(product):
    product_id = clean_text(product.get("id"))
    variant = product.get("selectedVariant") or product.get("defaultVariant") or {}
    variant_id = clean_text(variant.get("id"))
    sku = clean_text(variant.get("sku"))
    return f"{product_id}:{variant_id or sku}"


def add_product(products_by_key, product, category):
    key = product_key(product)
    if not key or key == ":":
        return

    category_id = clean_text(category.get("id"))
    category_name = clean_text(category.get("name"))
    category_path = clean_text(category.get("path"))

    if key not in products_by_key:
        item = dict(product)
        item["fetch_category_id"] = category_id
        item["fetch_category_name"] = category_name
        item["fetch_category_path"] = category_path
        item["fetch_category_ids"] = [category_id]
        item["fetch_category_names"] = [category_name]
        item["fetch_category_paths"] = [category_path]
        products_by_key[key] = item
        return

    existing = products_by_key[key]
    if category_id and category_id not in existing["fetch_category_ids"]:
        existing["fetch_category_ids"].append(category_id)
    if category_name and category_name not in existing["fetch_category_names"]:
        existing["fetch_category_names"].append(category_name)
    if category_path and category_path not in existing["fetch_category_paths"]:
        existing["fetch_category_paths"].append(category_path)


def category_for_product(product, fallback_category, categories_by_id):
    category_id = clean_text(product.get("categoryId"))
    if category_id in categories_by_id:
        return categories_by_id[category_id]
    return fallback_category


def page_size_candidates(count):
    candidates = [count, 100, 50, 20, 10, 5, 1]
    seen = set()
    result = []
    for value in candidates:
        try:
            value = int(value)
        except (TypeError, ValueError):
            continue
        if value <= 0 or value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def fetch_product_page(session, api_base, headers, category_id, count, page, retries, retry_delay):
    return get_with_retries(
        session=session,
        url=f"{api_base}/products",
        headers=headers,
        params={"itemsPerPage": count, "page": page, "categoryId": category_id},
        retries=retries,
        retry_delay=retry_delay,
    )


def retry_failed_pages(
    session,
    api_base,
    headers,
    category_id,
    failed_pages,
    failed_page_retries,
    failed_page_retry_delay,
    retries,
    retry_delay,
):
    recovered_products = []
    remaining_failures = []
    for failure in failed_pages:
        page = failure["page"]
        count = failure["count"]
        recovered = False
        last_error = failure["error"]
        for attempt in range(1, failed_page_retries + 1):
            if failed_page_retry_delay:
                time.sleep(failed_page_retry_delay)
            try:
                data = fetch_product_page(
                    session=session,
                    api_base=api_base,
                    headers=headers,
                    category_id=category_id,
                    count=count,
                    page=page,
                    retries=retries,
                    retry_delay=retry_delay,
                )
                recovered_products.extend(data.get("results") or [])
                recovered = True
                print(f"    hibas oldal ujraprobalva: page={page}, attempt={attempt}, sikeres")
                break
            except Exception as error:
                last_error = str(error)
                print(f"    hibas oldal ujraprobalva: page={page}, attempt={attempt}, hiba={last_error}")
        if not recovered:
            remaining_failures.append({**failure, "error": last_error})
    return recovered_products, remaining_failures


def fetch_products_for_category(
    session,
    api_base,
    headers,
    category,
    count,
    page_limit,
    page_delay,
    retries,
    retry_delay,
    failed_page_retries,
    failed_page_retry_delay,
):
    category_id = category["id"]
    last_error = None
    for candidate_count in page_size_candidates(count):
        first_page = None
        try:
            first_page = fetch_product_page(
                session=session,
                api_base=api_base,
                headers=headers,
                category_id=category_id,
                count=candidate_count,
                page=1,
                retries=retries,
                retry_delay=retry_delay,
            )
        except Exception as error:
            last_error = error
            continue

        pages = int(math.ceil(float(first_page.get("pageCount") or 1)))
        if page_limit is not None:
            pages = min(pages, page_limit)

        products = list(first_page.get("results") or [])
        failed_pages = []
        for page in range(2, pages + 1):
            if page_delay:
                time.sleep(page_delay)
            try:
                data = fetch_product_page(
                    session=session,
                    api_base=api_base,
                    headers=headers,
                    category_id=category_id,
                    count=candidate_count,
                    page=page,
                    retries=retries,
                    retry_delay=retry_delay,
                )
                products.extend(data.get("results") or [])
            except Exception as error:
                last_error = error
                failed_pages.append({"page": page, "count": candidate_count, "error": str(error)})
                if candidate_count > 1:
                    products = []
                    break

        if failed_pages and candidate_count > 1:
            continue
        if failed_pages and failed_page_retries > 0:
            recovered_products, failed_pages = retry_failed_pages(
                session=session,
                api_base=api_base,
                headers=headers,
                category_id=category_id,
                failed_pages=failed_pages,
                failed_page_retries=failed_page_retries,
                failed_page_retry_delay=failed_page_retry_delay,
                retries=retries,
                retry_delay=retry_delay,
            )
            products.extend(recovered_products)
        return products, first_page, candidate_count, failed_pages

    raise last_error


def fetch_all_products(
    session,
    api_base,
    headers,
    categories,
    count,
    category_ids,
    category_limit,
    page_limit,
    page_delay,
    category_delay,
    retries,
    retry_delay,
    failed_page_retries,
    failed_page_retry_delay,
):
    selected_category_ids = {clean_text(value) for value in (category_ids or []) if clean_text(value)}
    if selected_category_ids:
        fetch_categories = [category for category in categories if clean_text(category.get("id")) in selected_category_ids]
    else:
        fetch_categories = [
            category
            for category in categories
            if clean_text(category.get("id"))
            and category.get("is_leaf") == "true"
            and float(category.get("level") or 0) > 0
            and float(category.get("product_count") or 0) > 0
        ]

    if category_limit is not None:
        fetch_categories = fetch_categories[:category_limit]

    products_by_key = {}
    failed_categories = []
    categories_by_id = {clean_text(category.get("id")): category for category in categories if clean_text(category.get("id"))}
    parent_fallback_ids = set()

    def add_products(products, source_category):
        for product in products:
            add_product(products_by_key, product, category_for_product(product, source_category, categories_by_id))

    def fetch_parent_fallback(category, fallback_for):
        if selected_category_ids:
            return
        parent_id = clean_text(category.get("parent_id"))
        if not parent_id or parent_id in parent_fallback_ids:
            return
        parent_category = categories_by_id.get(parent_id)
        if not parent_category:
            return

        parent_fallback_ids.add(parent_id)
        try:
            products, page_info, selected_count, failed_pages = fetch_products_for_category(
                session=session,
                api_base=api_base,
                headers=headers,
                category=parent_category,
                count=count,
                page_limit=page_limit,
                page_delay=page_delay,
                retries=retries,
                retry_delay=retry_delay,
                failed_page_retries=failed_page_retries,
                failed_page_retry_delay=failed_page_retry_delay,
            )
            before_count = len(products_by_key)
            add_products(products, parent_category)
            added_count = len(products_by_key) - before_count
            print(
                f"  szulo fallback {parent_id} {parent_category['name']}: {len(products)} sor, "
                f"+{added_count} uj egyedi, lapmeret={selected_count}, hibas_oldal={len(failed_pages)}"
            )
            if failed_pages:
                failed_categories.append(
                    {
                        "id": parent_id,
                        "name": parent_category.get("name", ""),
                        "path": parent_category.get("path", ""),
                        "partial": "true",
                        "fallback_for": fallback_for,
                        "error": "; ".join(
                            f"itemsPerPage={failure['count']} page={failure['page']}: {failure['error']}"
                            for failure in failed_pages
                        ),
                    }
                )
        except Exception as error:
            print(f"  szulo fallback {parent_id} hiba: {error}")
            failed_categories.append(
                {
                    "id": parent_id,
                    "name": parent_category.get("name", ""),
                    "path": parent_category.get("path", ""),
                    "partial": "false",
                    "fallback_for": fallback_for,
                    "error": str(error),
                }
            )

    for index, category in enumerate(fetch_categories, start=1):
        category_id = category["id"]
        try:
            products, page_info, selected_count, failed_pages = fetch_products_for_category(
                session=session,
                api_base=api_base,
                headers=headers,
                category=category,
                count=count,
                page_limit=page_limit,
                page_delay=page_delay,
                retries=retries,
                retry_delay=retry_delay,
                failed_page_retries=failed_page_retries,
                failed_page_retry_delay=failed_page_retry_delay,
            )
            add_products(products, category)
            if failed_pages:
                failed_categories.append(
                    {
                        "id": category_id,
                        "name": category.get("name", ""),
                        "path": category.get("path", ""),
                        "partial": "true",
                        "error": "; ".join(
                            f"itemsPerPage={failure['count']} page={failure['page']}: {failure['error']}"
                            for failure in failed_pages
                        ),
                    }
                )
                fetch_parent_fallback(category, category_id)
            print(
                f"{index}/{len(fetch_categories)} {category_id} {category['name']}: "
                f"{len(products)} sor, {len(products_by_key)} egyedi termek, lapmeret={selected_count}, "
                f"hibas_oldal={len(failed_pages)}"
            )
        except Exception as error:
            print(f"{index}/{len(fetch_categories)} {category_id} hiba: {error}")
            failed_categories.append(
                {
                    "id": category_id,
                    "name": category.get("name", ""),
                    "path": category.get("path", ""),
                    "partial": "false",
                    "error": str(error),
                }
            )
            fetch_parent_fallback(category, category_id)

        if category_delay:
            time.sleep(category_delay)

    return list(products_by_key.values()), failed_categories, fetch_categories


def save_products(products):
    output_file = generate_filename("all_data")
    if products:
        pd.json_normalize(products).to_csv(output_file, index=False)
    else:
        pd.DataFrame().to_csv(output_file, index=False)
    return output_file


def save_department_stores(session, api_base, headers, retries, retry_delay):
    stores = get_with_retries(
        session=session,
        url=f"{api_base}/department_stores",
        headers=headers,
        retries=retries,
        retry_delay=retry_delay,
    )
    snapshot = generate_filename("department_stores")
    pd.json_normalize(stores).to_csv(snapshot, index=False)
    return snapshot


def parse_args():
    parser = argparse.ArgumentParser(description="Auchan termekek letoltese az auchan.hu REST API-rol.")
    parser.add_argument("--api-base", default=DEFAULT_API_BASE)
    parser.add_argument("--category-file", default=DEFAULT_CATEGORY_FILE)
    parser.add_argument("--area-type", default=DEFAULT_AREA_TYPE)
    parser.add_argument("--area-id", type=int, default=DEFAULT_AREA_ID)
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--category-ids", default="")
    parser.add_argument("--category-limit", type=int)
    parser.add_argument("--page-limit", type=int)
    parser.add_argument("--page-delay", type=float, default=0.05)
    parser.add_argument("--category-delay", type=float, default=0.02)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2)
    parser.add_argument("--failed-page-retries", type=int, default=1)
    parser.add_argument("--failed-page-retry-delay", type=float, default=30)
    parser.add_argument("--allow-partial-download", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    session = requests.Session()
    access_token = login_anonymous(session, retries=args.retries, retry_delay=args.retry_delay)
    headers = request_headers(access_token)

    delivery_area = setup_delivery_area(
        session=session,
        api_base=args.api_base,
        headers=headers,
        area_type=args.area_type,
        area_id=args.area_id,
        retries=args.retries,
        retry_delay=args.retry_delay,
    )
    print(f"Auchan delivery area: {delivery_area}")

    department_store_snapshot = save_department_stores(
        session=session,
        api_base=args.api_base,
        headers=headers,
        retries=args.retries,
        retry_delay=args.retry_delay,
    )
    print(f"Atveteli pontok mentve: {department_store_snapshot}")

    categories, _ = fetch_current_categories(
        session=session,
        api_base=args.api_base,
        headers=headers,
        retries=args.retries,
        retry_delay=args.retry_delay,
    )
    category_snapshot = save_categories(categories, args.category_file)
    print(f"Kategoriak mentve: {args.category_file} es {category_snapshot}")

    products, failed_categories, fetch_categories = fetch_all_products(
        session=session,
        api_base=args.api_base,
        headers=headers,
        categories=categories,
        count=args.count,
        category_ids=args.category_ids.split(",") if args.category_ids else None,
        category_limit=args.category_limit,
        page_limit=args.page_limit,
        page_delay=args.page_delay,
        category_delay=args.category_delay,
        retries=args.retries,
        retry_delay=args.retry_delay,
        failed_page_retries=args.failed_page_retries,
        failed_page_retry_delay=args.failed_page_retry_delay,
    )

    if failed_categories:
        failed_file = generate_filename("failed_categories")
        pd.DataFrame(failed_categories).to_csv(failed_file, index=False)
        print(f"Sikertelen kategoriak mentve: {failed_file}")

    output_file = save_products(products)
    print(f"Auchan termekadatok mentve: {output_file}")
    print(f"Fetch kategoriak: {len(fetch_categories)}")
    print(f"Egyedi termek/varians sorok: {len(products)}")

    if failed_categories and not args.allow_partial_download:
        raise RuntimeError(f"{len(failed_categories)} kategoria letoltese sikertelen volt.")


if __name__ == "__main__":
    main()
