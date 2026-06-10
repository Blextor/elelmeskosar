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
DEFAULT_CATEGORY_FILE = "kategoriak.txt"
DEFAULT_CATEGORY_PATH = "élelmiszer"
DEFAULT_STORE_ID = "00010"
DEFAULT_COUNTRY = "HU"
DEFAULT_LOCALE = "hu-HU"
DEFAULT_SEARCH_URL = "https://termekek.metro.hu/searchdiscover/articlesearch/search"
DEFAULT_CATEGORIES_URL = "https://termekek.metro.hu/searchdiscover/articlesearch/mainCategories"
DEFAULT_DETAIL_URL = "https://termekek.metro.hu/evaluate.article.v1/betty-variants"
DEFAULT_REFERER = "https://termekek.metro.hu/shop/category/%C3%A9lelmiszer"
DEFAULT_ROWS = 500
DEFAULT_DETAIL_BATCH_SIZE = 25
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
JSON_DICT_PREFIXES = {
    "bundle.referencedSubsystemNumbers",
    "price.dnrInfo",
    "price.summaryDnrInfo",
}


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def get_current_dir_name():
    return os.path.basename(os.getcwd()).lower()


def generate_filename(y_base, extension=".csv"):
    x = get_current_dir_name()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{now}{extension}"


def base36_timestamp():
    value = int(time.time() * 1000)
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    if value == 0:
        return "0"
    chars = []
    while value:
        value, remainder = divmod(value, 36)
        chars.append(alphabet[remainder])
    return "".join(reversed(chars))


def request_headers(sd_token=False):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": DEFAULT_REFERER,
    }
    if sd_token:
        headers["X-SD-Token"] = base36_timestamp()
    return headers


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


def flatten_categories(category_tree, root_path):
    rows = []
    root_children = (category_tree or {}).get("children") or {}

    def walk(node, parent_category_id="", parent_path="", path_names=None, path_ids=None, depth=0):
        path_names = list(path_names or [])
        path_ids = list(path_ids or [])
        category_id = clean_text(node.get("categoryId"))
        name = clean_text(node.get("name"))
        display_name = clean_text(node.get("displayName") or name)
        url_category_path = clean_text(node.get("urlCategoryPath"))
        children = node.get("children") or {}
        current_path_names = path_names + ([display_name] if display_name else [])
        current_path_ids = path_ids + ([category_id] if category_id else [])

        rows.append(
            {
                "index": len(rows),
                "category_id": category_id,
                "name": name,
                "display_name": display_name,
                "url_category_path": url_category_path,
                "parent_category_id": parent_category_id,
                "parent_url_category_path": parent_path,
                "depth": depth,
                "amounts": node.get("amounts", 0) or 0,
                "child_count": len(children),
                "is_leaf": "true" if not children else "false",
                "path": " > ".join(current_path_names),
                "path_ids": "|".join(current_path_ids),
                "image_url": clean_text(node.get("imageUrl")),
            }
        )

        for child in children.values():
            walk(
                child,
                parent_category_id=category_id,
                parent_path=url_category_path,
                path_names=current_path_names,
                path_ids=current_path_ids,
                depth=depth + 1,
            )

    root = None
    for node in root_children.values():
        if clean_text(node.get("urlCategoryPath")) == root_path:
            root = node
            break
    if root is None:
        available = ", ".join(clean_text(node.get("urlCategoryPath")) for node in root_children.values())
        raise ValueError(f"A Metro kategoriafa nem tartalmazza ezt az utat: {root_path}. Elso szintek: {available}")

    walk(root)
    return rows


def save_categories(categories, category_file):
    fieldnames = [
        "index",
        "category_id",
        "name",
        "display_name",
        "url_category_path",
        "parent_category_id",
        "parent_url_category_path",
        "depth",
        "amounts",
        "child_count",
        "is_leaf",
        "path",
        "path_ids",
        "image_url",
    ]
    with open(category_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(categories)

    snapshot = generate_filename("categories")
    pd.DataFrame(categories).to_csv(snapshot, index=False)
    return snapshot


def fetch_categories(session, args):
    params = {
        "storeId": args.store_id,
        "language": args.locale,
        "country": args.country,
        "profile": args.locale,
        "role": args.role,
    }
    data = get_json_with_retries(
        session,
        DEFAULT_CATEGORIES_URL,
        params=params,
        headers=request_headers(sd_token=True),
        retries=args.retries,
        retry_delay=args.retry_delay,
    )
    categories = flatten_categories(data, args.category_path)
    if not categories:
        raise ValueError("A Metro kategoriafa ures.")
    return categories


def search_params(args, category_path, page):
    return {
        "storeId": args.store_id,
        "language": args.locale,
        "country": args.country,
        "query": "*",
        "rows": args.rows,
        "page": page,
        "filter": f"category:{category_path}",
        "profile": args.locale,
        "role": args.role,
        "facets": "true",
        "categories": "true",
    }


def fetch_search_page(session, args, category_path, page):
    return get_json_with_retries(
        session,
        DEFAULT_SEARCH_URL,
        params=search_params(args, category_path, page),
        headers=request_headers(sd_token=True),
        retries=args.retries,
        retry_delay=args.retry_delay,
    )


def selected_search_categories(categories, args):
    if args.category_mode == "root":
        return [
            {
                "url_category_path": args.category_path,
                "display_name": args.category_path,
                "amounts": "",
            }
        ]

    rows = [
        category
        for category in categories
        if clean_text(category.get("is_leaf")).lower() == "true"
        and clean_text(category.get("url_category_path"))
        and int(category.get("amounts") or 0) > 0
    ]
    if args.category_limit:
        rows = rows[: args.category_limit]
    return rows


def merge_search_meta(search_meta_by_id, result_id, summary, page, offset, category):
    category_path = clean_text(category.get("url_category_path"))
    category_name = clean_text(category.get("display_name") or category.get("name"))

    if result_id not in search_meta_by_id:
        summary = dict(summary)
        summary.update(
            {
                "search_result_id": result_id,
                "search_page": page,
                "search_rank": offset,
                "fetch_category_path": category_path,
                "fetch_category_name": category_name,
                "fetch_category_paths": [category_path] if category_path else [],
                "fetch_category_names": [category_name] if category_name else [],
            }
        )
        search_meta_by_id[result_id] = summary
        return True

    existing = search_meta_by_id[result_id]
    if category_path and category_path not in existing.get("fetch_category_paths", []):
        existing.setdefault("fetch_category_paths", []).append(category_path)
    if category_name and category_name not in existing.get("fetch_category_names", []):
        existing.setdefault("fetch_category_names", []).append(category_name)
    return False


def collect_search_results(session, args, categories):
    search_meta_by_id = {}
    result_ids = []
    failed_pages = []
    total_amount = 0
    search_categories = selected_search_categories(categories, args)

    for category_index, category in enumerate(search_categories, start=1):
        category_path = clean_text(category.get("url_category_path"))
        total_pages = None
        page = 1
        category_amount = None

        while total_pages is None or page <= total_pages:
            try:
                data = fetch_search_page(session, args, category_path, page)
                if total_pages is None:
                    category_amount = int(data.get("amount") or 0)
                    total_amount += category_amount
                    total_pages = max(1, int(data.get("totalPages") or math.ceil(category_amount / max(1, args.rows)) or 1))
                    if args.page_limit:
                        total_pages = min(total_pages, args.page_limit)

                ids = data.get("resultIds") or []
                summaries = data.get("results") or {}
                for offset, result_id in enumerate(ids, start=1):
                    result_id = clean_text(result_id)
                    if not result_id:
                        continue
                    is_new = merge_search_meta(
                        search_meta_by_id,
                        result_id,
                        summaries.get(result_id) or {},
                        page,
                        (page - 1) * args.rows + offset,
                        category,
                    )
                    if is_new:
                        result_ids.append(result_id)

                print(
                    f"Metro kategoria: {category_index}/{len(search_categories)} "
                    f"{category_path} oldal {page}/{total_pages}, "
                    f"{len(result_ids)} egyedi termek ID eddig",
                    flush=True,
                )
            except Exception as error:
                print(f"Metro keresesi oldal hiba: {category_path} page={page} - {error}", flush=True)
                failed_pages.append({"category_path": category_path, "page": page, "error": str(error)})
                if not args.allow_partial_download:
                    raise

            if args.page_delay:
                time.sleep(args.page_delay)
            page += 1

    return result_ids, search_meta_by_id, total_amount, failed_pages


def chunks(values, size):
    for index in range(0, len(values), size):
        yield values[index : index + size]


def without_keys(data, keys):
    if not isinstance(data, dict):
        return {}
    return {key: value for key, value in data.items() if key not in keys}


def price_info_from_store(store):
    if not isinstance(store, dict):
        return {}
    direct = store.get("sellingPriceInfo")
    if isinstance(direct, dict):
        return direct

    delivery_mode = store.get("selectedDeliveryMode") or "STORE"
    fulfillment_type = store.get("selectedFulfillmentType") or "STORE"
    modes = store.get("possibleDeliveryModes") or {}
    fulfillments = ((modes.get(delivery_mode) or {}).get("possibleFulfillmentTypes") or {})
    selected = fulfillments.get(fulfillment_type) or fulfillments.get("STORE") or {}
    price = selected.get("sellingPriceInfo")
    return price if isinstance(price, dict) else {}


def variant_id_from_meta(article_key, variant_key, variant):
    nested = variant.get("bettyVariantId") or {}
    return clean_text(nested.get("bettyVariantId") or variant.get("variantId") or f"{article_key}{variant_key}")


def bundle_id_from_meta(bundle, variant_id, bundle_key):
    nested = bundle.get("bundleId") or {}
    return clean_text(nested.get("bettyBundleId") or bundle.get("bettyBundleId") or f"{variant_id}{bundle_key}")


def rows_from_detail_response(data, search_meta_by_id, default_store_id):
    rows = []
    enriched_variant_ids = set()
    result = data.get("result") or {}

    for article_key, article in result.items():
        article_meta = without_keys(article, ["variants"])
        variants = article.get("variants") or {}
        for variant_key, variant in variants.items():
            variant_id = variant_id_from_meta(article_key, variant_key, variant)
            enriched_variant_ids.add(variant_id)
            variant_meta = without_keys(variant, ["bundles"])
            bundles = variant.get("bundles") or {}

            if not bundles:
                meta = dict(search_meta_by_id.get(variant_id) or {})
                rows.append(
                    {
                        **meta,
                        "detail_enriched": True,
                        "article_key": article_key,
                        "variant_key": variant_key,
                        "variant_id": variant_id,
                        "article": article_meta,
                        "variant": variant_meta,
                    }
                )
                continue

            for bundle_key, bundle in bundles.items():
                bundle_id = bundle_id_from_meta(bundle, variant_id, bundle_key)
                bundle_meta = without_keys(bundle, ["stores"])
                stores = bundle.get("stores") or {default_store_id: {}}
                for store_id, store in stores.items():
                    store_meta = without_keys(store, ["possibleDeliveryModes", "sellingPriceInfo"])
                    meta = dict(search_meta_by_id.get(variant_id) or {})
                    rows.append(
                        {
                            **meta,
                            "detail_enriched": True,
                            "article_key": article_key,
                            "variant_key": variant_key,
                            "bundle_key": bundle_key,
                            "variant_id": variant_id,
                            "bundle_id": bundle_id,
                            "detail_store_id": store_id,
                            "selected_delivery_mode": store.get("selectedDeliveryMode") if isinstance(store, dict) else "",
                            "selected_fulfillment_type": store.get("selectedFulfillmentType") if isinstance(store, dict) else "",
                            "customer_buyable": store.get("customerBuyable") if isinstance(store, dict) else "",
                            "article": article_meta,
                            "variant": variant_meta,
                            "bundle": bundle_meta,
                            "store": store_meta,
                            "price": price_info_from_store(store),
                        }
                    )

    return rows, enriched_variant_ids


def fetch_detail_batch(session, args, batch_ids):
    params = [
        ("storeIds", args.store_id),
        ("country", args.country),
        ("locale", args.locale),
    ]
    params.extend(("ids", result_id) for result_id in batch_ids)
    return get_json_with_retries(
        session,
        DEFAULT_DETAIL_URL,
        params=params,
        headers=request_headers(sd_token=False),
        retries=args.retries,
        retry_delay=args.retry_delay,
    )


def collect_detail_rows(session, args, result_ids, search_meta_by_id):
    rows_by_key = {}
    failed_batches = []
    enriched_variant_ids = set()
    ids_to_fetch = result_ids[: args.max_detail_ids] if args.max_detail_ids else result_ids
    total_batches = max(1, math.ceil(len(ids_to_fetch) / args.detail_batch_size))

    for batch_index, batch_ids in enumerate(chunks(ids_to_fetch, args.detail_batch_size), start=1):
        try:
            print(
                f"Metro reszletes batch: {batch_index}/{total_batches}, "
                f"{(batch_index - 1) * args.detail_batch_size + 1}-{(batch_index - 1) * args.detail_batch_size + len(batch_ids)}/{len(ids_to_fetch)}",
                flush=True,
            )
            data = fetch_detail_batch(session, args, batch_ids)
            rows, batch_enriched_ids = rows_from_detail_response(data, search_meta_by_id, args.store_id)
            enriched_variant_ids.update(batch_enriched_ids)
            for row in rows:
                key = clean_text(row.get("bundle_id") or row.get("variant_id") or row.get("search_result_id"))
                if key:
                    rows_by_key[key] = row
        except Exception as error:
            print(f"Metro reszletes batch hiba: {batch_index}/{total_batches} - {error}", flush=True)
            failed_batches.append({"batch_index": batch_index, "ids": "|".join(batch_ids), "error": str(error)})
            if not args.allow_partial_download:
                raise

        if args.detail_delay:
            time.sleep(args.detail_delay)

    for result_id in ids_to_fetch:
        if result_id in enriched_variant_ids:
            continue
        key = f"missing:{result_id}"
        rows_by_key[key] = {
            **dict(search_meta_by_id.get(result_id) or {}),
            "detail_enriched": False,
            "variant_id": result_id,
        }

    return list(rows_by_key.values()), failed_batches


def flatten_value(prefix, value, output):
    if isinstance(value, dict):
        if prefix in JSON_DICT_PREFIXES or mostly_dynamic_keys(value):
            output[prefix] = json.dumps(value, ensure_ascii=False)
            return
        if not value:
            output[prefix] = ""
            return
        for key, child in value.items():
            child_key = f"{prefix}.{key}" if prefix else str(key)
            flatten_value(child_key, child, output)
        return
    if isinstance(value, list):
        output[prefix] = json.dumps(value, ensure_ascii=False)
        return
    output[prefix] = value


def mostly_dynamic_keys(value):
    if not isinstance(value, dict) or len(value) < 20:
        return False
    dynamic_count = sum(1 for key in value if re.fullmatch(r"\d+(?:\.\d+)?", str(key)))
    return dynamic_count / len(value) >= 0.8


def flatten_row(row):
    output = {}
    for key, value in row.items():
        flatten_value(str(key), value, output)
    return output


def save_rows(rows):
    if not rows:
        raise ValueError("Nincs mentheto Metro termeksor.")
    output_file = generate_filename("all_data")
    flat_rows = [flatten_row(row) for row in rows]
    fieldnames = []
    seen = set()
    for row in flat_rows:
        for key in row.keys():
            if key not in seen:
                fieldnames.append(key)
                seen.add(key)

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_rows)
    return output_file


def save_failures(failed_pages, failed_batches):
    failures = []
    for row in failed_pages:
        failures.append({"type": "search_page", **row})
    for row in failed_batches:
        failures.append({"type": "detail_batch", **row})
    if not failures:
        return None
    output_file = generate_filename("failed_requests")
    pd.DataFrame(failures).to_csv(output_file, index=False)
    return output_file


def parse_args():
    parser = argparse.ArgumentParser(description="Metro elelmiszer termekadatok letoltese.")
    parser.add_argument("--store-id", default=DEFAULT_STORE_ID)
    parser.add_argument("--country", default=DEFAULT_COUNTRY)
    parser.add_argument("--locale", default=DEFAULT_LOCALE)
    parser.add_argument("--role", default="anonymous")
    parser.add_argument("--category-path", default=DEFAULT_CATEGORY_PATH)
    parser.add_argument("--category-mode", choices=["leaves", "root"], default="leaves")
    parser.add_argument("--category-limit", type=int, default=None)
    parser.add_argument("--category-file", default=DEFAULT_CATEGORY_FILE)
    parser.add_argument("--rows", type=int, default=DEFAULT_ROWS)
    parser.add_argument("--detail-batch-size", type=int, default=DEFAULT_DETAIL_BATCH_SIZE)
    parser.add_argument("--page-limit", type=int, default=None)
    parser.add_argument("--max-detail-ids", type=int, default=None)
    parser.add_argument("--page-delay", type=float, default=0.0)
    parser.add_argument("--detail-delay", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--allow-partial-download", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    args.rows = max(1, int(args.rows))
    args.detail_batch_size = max(1, int(args.detail_batch_size))

    with requests.Session() as session:
        categories = fetch_categories(session, args)
        categories_snapshot = save_categories(categories, args.category_file)
        print(f"Metro kategoriafa mentve: {args.category_file}")
        print(f"Metro kategoria snapshot mentve: {categories_snapshot}")

        result_ids, search_meta_by_id, amount, failed_pages = collect_search_results(session, args, categories)
        print(f"Metro kereses kesz: {len(result_ids)} egyedi termek ID, kategoriankenti API amount osszeg={amount}")

        rows, failed_batches = collect_detail_rows(session, args, result_ids, search_meta_by_id)
        failures_file = save_failures(failed_pages, failed_batches)

        if (failed_pages or failed_batches) and not args.allow_partial_download:
            raise RuntimeError("Volt sikertelen Metro kereses/reszlet batch, es nincs engedelyezve a reszleges mentes.")

        output_file = save_rows(rows)
        print(f"Mentes kesz: {len(rows)} Metro termeksor {output_file}")
        if failures_file:
            print(f"Metro hibak mentve: {failures_file}")


if __name__ == "__main__":
    main()
