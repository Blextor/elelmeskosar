import argparse
import csv
import os
import re
import time
from datetime import datetime

import pandas as pd
import requests


MAIN_FOLDER = "./../../../data/markets_data/"
DEFAULT_VENUE_SLUG = "sparszupermarket-szegedarkad"
DEFAULT_LANGUAGE = "hu"
DEFAULT_CATEGORY_FILE = "kategoriak.txt"
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def get_current_dir_name():
    return os.path.basename(os.getcwd()).lower()


def generate_filename(y_base, extension=".csv"):
    x = get_current_dir_name()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{now}{extension}"


def build_assortment_url(venue_slug):
    return (
        "https://consumer-api.wolt.com/consumer-api/consumer-assortment/v1/"
        f"venues/slug/{venue_slug}/assortment"
    )


def build_category_url(venue_slug, category_slug):
    return (
        "https://consumer-api.wolt.com/consumer-api/consumer-assortment/v1/"
        f"venues/slug/{venue_slug}/assortment/categories/slug/{category_slug}"
    )


def get_json_with_retries(session, url, params, retries, retry_delay):
    last_error = None

    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()
            last_error = requests.HTTPError(f"HTTP {response.status_code}: {url}")
        except Exception as error:
            last_error = error

        if attempt < retries:
            time.sleep(retry_delay * attempt)

    raise last_error


def slug_index(slug, fallback):
    match = re.search(r"-(\d+)$", slug or "")
    if match:
        return match.group(1)
    return str(fallback)


def flatten_categories(categories, parent_slug="", depth=0):
    rows = []
    for category in categories:
        subcategories = category.get("subcategories") or []
        slug = category.get("slug", "")
        rows.append(
            {
                "index": slug_index(slug, len(rows) + 1),
                "name": category.get("name", ""),
                "slug": slug,
                "id": category.get("id", ""),
                "parent_slug": parent_slug,
                "depth": depth,
                "subcategories": len(subcategories),
            }
        )
        rows.extend(flatten_categories(subcategories, slug, depth + 1))
    return rows


def fetch_current_categories(session, venue_slug, language, retries, retry_delay):
    data = get_json_with_retries(
        session,
        build_assortment_url(venue_slug),
        params={"language": language},
        retries=retries,
        retry_delay=retry_delay,
    )
    categories = flatten_categories(data.get("categories") or [])
    if not categories:
        raise ValueError("Az assortment valasz nem tartalmaz kategoriakat.")
    return categories, data.get("assortment_id", "")


def save_categories(categories, category_file):
    fieldnames = [
        "index",
        "name",
        "slug",
        "id",
        "parent_slug",
        "depth",
        "subcategories",
    ]
    with open(category_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(categories)
    snapshot = generate_filename("categories")
    pd.DataFrame(categories).to_csv(snapshot, index=False)
    return snapshot


def load_categories(category_file):
    with open(category_file, encoding="utf-8") as file:
        categories = list(csv.DictReader(file))
    categories = [category for category in categories if category.get("slug")]
    if not categories:
        raise ValueError(f"Nincs hasznalhato slug ebben a fajlban: {category_file}")
    return categories


def add_item(items_dict, item, category):
    item_id = item.get("id")
    if not item_id:
        return

    slug = category.get("slug", "")
    name = category.get("name", "")
    parent_slug = category.get("parent_slug", "")
    depth = int(category.get("depth") or 0)

    if item_id not in items_dict:
        item = dict(item)
        item["category_slug"] = slug
        item["category_name"] = name
        item["category_parent_slug"] = parent_slug
        item["category_depth"] = depth
        item["category_slugs"] = [slug]
        item["category_names"] = [name]
        items_dict[item_id] = item
        return

    existing = items_dict[item_id]
    if slug and slug not in existing["category_slugs"]:
        existing["category_slugs"].append(slug)
    if name and name not in existing["category_names"]:
        existing["category_names"].append(name)

    # If the same item appears in parent and child categories, keep the more
    # specific category as the primary category for the existing normalizer.
    if depth >= int(existing.get("category_depth") or 0):
        existing["category_slug"] = slug
        existing["category_name"] = name
        existing["category_parent_slug"] = parent_slug
        existing["category_depth"] = depth


def fetch_items(session, venue_slug, language, categories, page_delay, retries, retry_delay):
    items_dict = {}
    failed_categories = []

    for category in categories:
        slug = category["slug"]
        next_token = None
        downloaded_pages = 0

        while True:
            params = {"language": language}
            if next_token:
                params["page_token"] = next_token

            try:
                data = get_json_with_retries(
                    session,
                    build_category_url(venue_slug, slug),
                    params=params,
                    retries=retries,
                    retry_delay=retry_delay,
                )
                for item in data.get("items", []):
                    add_item(items_dict, item, category)
                downloaded_pages += 1

                next_token = data.get("metadata", {}).get("next_page_token")
                if not next_token:
                    break
            except Exception as error:
                print(f"{slug}: hiba - {error}")
                failed_categories.append({"slug": slug, "error": str(error)})
                break

            time.sleep(page_delay)

        print(f"{slug}: kesz ({len(items_dict)} egyedi item eddig, {downloaded_pages} oldal)")

    return list(items_dict.values()), failed_categories


def prepare_items_for_csv(items):
    for item in items:
        item["category_slugs"] = ";".join(item.get("category_slugs") or [])
        item["category_names"] = ";".join(item.get("category_names") or [])
    return items


def parse_args():
    parser = argparse.ArgumentParser(description="SPAR termekadatok letoltese Wolt API-bol.")
    parser.add_argument("--venue-slug", default=os.environ.get("SPAR_VENUE_SLUG", DEFAULT_VENUE_SLUG))
    parser.add_argument("--language", default=DEFAULT_LANGUAGE)
    parser.add_argument("--category-file", default=DEFAULT_CATEGORY_FILE)
    parser.add_argument("--no-category-refresh", action="store_true")
    parser.add_argument("--allow-stale-categories", action="store_true")
    parser.add_argument("--allow-partial-download", action="store_true")
    parser.add_argument("--refresh-categories-only", action="store_true")
    parser.add_argument("--page-delay", type=float, default=2.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    return parser.parse_args()


def main():
    args = parse_args()
    session = requests.Session()

    if args.no_category_refresh:
        categories = load_categories(args.category_file)
        print(
            f"Kategoriak betoltve helyi fajlbol: {args.category_file} ({len(categories)} db). "
            "Ez explicit --no-category-refresh futas, nem alapertelmezett mukodes."
        )
    else:
        try:
            categories, assortment_id = fetch_current_categories(
                session,
                args.venue_slug,
                args.language,
                args.retries,
                args.retry_delay,
            )
            snapshot = save_categories(categories, args.category_file)
            print(
                f"Kategoriak frissitve: {len(categories)} db, "
                f"assortment_id={assortment_id}, snapshot={snapshot}"
            )
        except Exception as error:
            if args.refresh_categories_only or not args.allow_stale_categories:
                raise
            print(f"Kategoriafrissites sikertelen, helyi fajl hasznalata explicit engedellyel: {error}")
            categories = load_categories(args.category_file)

    if args.refresh_categories_only:
        return

    items, failed_categories = fetch_items(
        session=session,
        venue_slug=args.venue_slug,
        language=args.language,
        categories=categories,
        page_delay=args.page_delay,
        retries=args.retries,
        retry_delay=args.retry_delay,
    )

    if failed_categories and not args.allow_partial_download:
        failed = ", ".join(f"{item['slug']} ({item['error']})" for item in failed_categories[:10])
        raise RuntimeError(
            f"{len(failed_categories)} kategoria letoltese sikertelen, ezert nem irok hianyos all_data fajlt. "
            f"Elso hibak: {failed}"
        )
    if not items:
        raise RuntimeError("A letoltes 0 termeket adott vissza, ezert nem irok ures all_data fajlt.")

    df = pd.json_normalize(prepare_items_for_csv(items))
    file_name = generate_filename("all_data")
    df.to_csv(file_name, index=False)

    print(f"\nMentes kesz: {len(items)} egyedi termek", file_name)


if __name__ == "__main__":
    main()
