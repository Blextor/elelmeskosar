import argparse
import base64
import csv
import json
import os
import re
import time
import urllib.parse
from datetime import datetime
from html import unescape
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests


MAIN_FOLDER = "./../../../data/markets_data/"
LANDING_URL = "https://bevasarlas.tesco.hu/shop/hu-HU/landing/groceries"
API_URL = "https://xapi.tesco.com/"
DEFAULT_CATEGORY_FILE = "kategoriak.txt"
DEFAULT_API_KEY = "TvOSZJHlEk0pjniDGQFAc9Q59WGAR4dA"
DEFAULT_COUNT = 100
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

PRODUCT_QUERY = """
query GetCategoryProducts(
  $facet: ID,
  $page: Int = 1,
  $count: Int,
  $sortBy: String,
  $filterCriteria: [filterCriteria],
  $includeVariations: Boolean = true,
  $showDepositReturnCharge: Boolean = false
) {
  category(
    page: $page,
    count: $count,
    sortBy: $sortBy,
    facet: $facet,
    filterCriteria: $filterCriteria
  ) {
    pageInformation: info {
      totalCount: total
      pageNo: page
      count
      pageSize
      offset
      __typename
    }
    results {
      node {
        ... on ProductType {
          ...ProductFields
          __typename
        }
        ... on MPProduct {
          ...ProductFields
          seller {
            id
            name
            __typename
          }
          variations {
            ...Variation @include(if: $includeVariations)
            __typename
          }
          __typename
        }
        ... on FNFProduct {
          ...ProductFields
          variations {
            ...Variation @include(if: $includeVariations)
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
  }
}

fragment ProductFields on ProductInterface {
  id
  tpnb
  tpnc
  gtin
  baseProductId
  title
  brandName
  shortDescription
  defaultImageUrl
  superDepartmentName
  departmentName
  aisleName
  shelfName
  displayType
  productType
  averageWeight
  isForSale
  isNew
  status
  price {
    actual
    unitPrice
    unitOfMeasure
    __typename
  }
  promotions {
    id
    promotionType
    startDate
    endDate
    description
    unitSellingInfo
    price {
      beforeDiscount
      afterDiscount
      __typename
    }
    attributes
    __typename
  }
  details {
    ingredients
    packSize {
      value
      units
      __typename
    }
    netContents
    drainedWeight
    features
    otherInformation
    __typename
  }
  catchWeightList {
    price
    weight
    default
    __typename
  }
  charges @include(if: $showDepositReturnCharge) {
    ... on ProductDepositReturnCharge {
      amount
      __typename
    }
    __typename
  }
}

fragment Variation on VariationsType {
  products {
    id
    baseProductId
    variationAttributes {
      attributeGroup
      attributeGroupData {
        name
        value
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}
"""


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def get_current_dir_name():
    return os.path.basename(os.getcwd()).lower()


def generate_filename(y_base, extension=".csv"):
    x = get_current_dir_name()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{now}{extension}"


def encode_facet_path(path):
    url_encoded = urllib.parse.quote(path, safe="-,.")
    return base64.b64encode(url_encoded.encode("utf-8")).decode("ascii")


def headers(api_key):
    return {
        "accept": "application/json",
        "accept-language": "hu-HU",
        "content-type": "application/json",
        "language": "hu-HU",
        "region": "HU",
        "origin": "https://bevasarlas.tesco.hu",
        "referer": LANDING_URL,
        "user-agent": "Mozilla/5.0",
        "x-apikey": api_key,
    }


def get_with_retries(session, url, retries, retry_delay):
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, headers={"user-agent": "Mozilla/5.0"}, timeout=30)
            if response.status_code == 200:
                return response
            if response.status_code not in RETRYABLE_STATUS_CODES:
                response.raise_for_status()
            last_error = requests.HTTPError(f"HTTP {response.status_code}: {url}")
        except Exception as error:
            last_error = error
        if attempt < retries:
            time.sleep(retry_delay * attempt)
    raise last_error


def post_graphql_with_retries(session, payload, request_headers, retries, retry_delay):
    last_error = None
    for attempt in range(1, retries + 1):
        retry_after = None
        try:
            response = session.post(API_URL, headers=request_headers, json=payload, timeout=45)
            if response.status_code == 200:
                data = response.json()
                if data.get("errors"):
                    raise RuntimeError(json.dumps(data["errors"], ensure_ascii=False)[:1000])
                return data
            if response.status_code not in RETRYABLE_STATUS_CODES:
                raise requests.HTTPError(f"HTTP {response.status_code}: {response.text[:1000]}")
            retry_after = response.headers.get("Retry-After")
            last_error = requests.HTTPError(f"HTTP {response.status_code}: {response.text[:500]}")
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


def parse_browse_links(html):
    pattern = re.compile(r'<a\b[^>]*href="([^"]*/shop/hu-HU/browse/[^"]+)"[^>]*>(.*?)</a>', re.S)
    links = []
    seen = set()
    for href, raw_text in pattern.findall(html):
        text = re.sub("<.*?>", " ", raw_text)
        text = clean_text(unescape(text))
        if not text:
            continue
        parsed = urlparse(href)
        path = parsed.path or href
        match = re.search(r"/shop/hu-HU/browse/(.+)$", path)
        if not match:
            continue
        browse_path = match.group(1).strip("/")
        parts = [part for part in browse_path.split("/") if part]
        key = (text, path)
        if key in seen:
            continue
        seen.add(key)
        links.append(
            {
                "name": text,
                "url": urljoin(LANDING_URL, href),
                "browse_path": browse_path,
                "parts": parts,
            }
        )
    return links


def discover_fetch_categories(session, retries, retry_delay, include_promotional=True):
    response = get_with_retries(session, LANDING_URL, retries=retries, retry_delay=retry_delay)
    html = response.content.decode("utf-8", errors="replace")
    rows = []
    seen_names = set()
    for link in parse_browse_links(html):
        parts = link["parts"]
        # Main fetch categories are one path segment followed by /all.
        if len(parts) != 2 or parts[-1] != "all":
            continue
        name = clean_text(link["name"])
        if not include_promotional and name in {"Most ajánlott!", "Újdonságok"}:
            continue
        if name in seen_names:
            continue
        seen_names.add(name)
        facet_code = encode_facet_path(name)
        rows.append(
            {
                "index": len(rows) + 1,
                "name": name,
                "path": name,
                "facet_code": facet_code,
                "facet": f"b;{facet_code}",
                "url": link["url"],
                "url_slug": parts[0],
                "depth": 0,
                "parent_path": "",
                "source": "landing",
                "total_count": "",
            }
        )
    if not rows:
        raise ValueError("A Tesco landing oldalrol nem sikerult fo kategoriakat kinyerni.")
    return rows


def save_fetch_categories(categories, category_file):
    fieldnames = [
        "index",
        "name",
        "path",
        "facet_code",
        "facet",
        "url",
        "url_slug",
        "depth",
        "parent_path",
        "source",
        "total_count",
    ]
    with open(category_file, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(categories)
    snapshot = generate_filename("fetch_categories")
    pd.DataFrame(categories).to_csv(snapshot, index=False)
    return snapshot


def load_fetch_categories(category_file):
    with open(category_file, encoding="utf-8") as file:
        categories = list(csv.DictReader(file))
    categories = [category for category in categories if category.get("facet") or category.get("facet_code")]
    if not categories:
        raise ValueError(f"Nincs hasznalhato Tesco facet ebben a fajlban: {category_file}")
    for index, category in enumerate(categories, start=1):
        category["index"] = category.get("index") or index
        category["name"] = clean_text(category.get("name") or category.get("path"))
        category["path"] = clean_text(category.get("path") or category.get("name"))
        if not category.get("facet_code"):
            category["facet_code"] = encode_facet_path(category["path"])
        if not category.get("facet"):
            category["facet"] = f"b;{category['facet_code']}"
    return categories


def build_payload(category, page, count):
    return {
        "operationName": "GetCategoryProducts",
        "variables": {
            "page": page,
            "includeRestrictions": True,
            "includeVariations": True,
            "showDepositReturnCharge": True,
            "count": count,
            "facet": category["facet"],
            "filterCriteria": [{"name": "0", "values": ["groceries"]}],
            "sortBy": "relevance",
        },
        "extensions": {"mfeName": "mfe-plp"},
        "query": PRODUCT_QUERY,
    }


def add_product(products_by_id, product, category):
    product_id = clean_text(product.get("id"))
    if not product_id:
        return

    if product_id not in products_by_id:
        item = dict(product)
        item["fetch_category_names"] = [category["name"]]
        item["fetch_category_paths"] = [category["path"]]
        item["fetch_category_facets"] = [category["facet"]]
        products_by_id[product_id] = item
        return

    existing = products_by_id[product_id]
    for field, value in [
        ("fetch_category_names", category["name"]),
        ("fetch_category_paths", category["path"]),
        ("fetch_category_facets", category["facet"]),
    ]:
        values = existing.setdefault(field, [])
        if value and value not in values:
            values.append(value)


def fetch_products(session, categories, request_headers, count, page_delay, retries, retry_delay, page_limit=None):
    products_by_id = {}
    failed_categories = []

    for category in categories:
        page = 1
        total_pages = 1
        downloaded_pages = 0

        while page <= total_pages:
            try:
                data = post_graphql_with_retries(
                    session=session,
                    payload=build_payload(category, page, count),
                    request_headers=request_headers,
                    retries=retries,
                    retry_delay=retry_delay,
                )
                category_data = data.get("data", {}).get("category") or {}
                page_info = category_data.get("pageInformation") or {}
                total_count = int(page_info.get("totalCount") or 0)
                category["total_count"] = total_count
                total_pages = max(1, (total_count + count - 1) // count)

                for result in category_data.get("results") or []:
                    product = result.get("node") or {}
                    add_product(products_by_id, product, category)

                downloaded_pages += 1
                if page_limit and downloaded_pages >= page_limit:
                    break
                page += 1
            except Exception as error:
                print(f"{category['name']}: hiba - {error}")
                failed_categories.append({"name": category["name"], "error": str(error)})
                break

            if page_delay:
                time.sleep(page_delay)

        print(
            f"{category['name']}: kesz "
            f"({len(products_by_id)} egyedi termek eddig, {downloaded_pages}/{total_pages} oldal)"
        )

    return list(products_by_id.values()), failed_categories


def path_parts_from_product(product):
    return [
        clean_text(product.get("superDepartmentName")),
        clean_text(product.get("departmentName")),
        clean_text(product.get("aisleName")),
        clean_text(product.get("shelfName")),
    ]


def build_detailed_categories(products):
    categories = {}
    for product in products:
        parts = [part for part in path_parts_from_product(product) if part]
        for depth in range(len(parts)):
            path = "|".join(parts[: depth + 1])
            parent_path = "|".join(parts[:depth])
            row = categories.setdefault(
                path,
                {
                    "index": len(categories) + 1,
                    "name": parts[depth],
                    "path": path,
                    "facet_code": encode_facet_path(path),
                    "facet": f"b;{encode_facet_path(path)}",
                    "parent_path": parent_path,
                    "depth": depth,
                    "product_count": 0,
                },
            )
            row["product_count"] += 1
    return sorted(categories.values(), key=lambda row: (int(row["depth"]), row["path"]))


def save_detailed_categories(products):
    categories = build_detailed_categories(products)
    if not categories:
        return None
    file_name = generate_filename("categories")
    pd.DataFrame(categories).to_csv(file_name, index=False)
    return file_name


def make_csv_safe(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def prepare_products_for_csv(products):
    rows = []
    for product in products:
        row = dict(product)
        # These are fetch metadata lists, not Tesco nested objects.
        # Keep them compact and readable in the flattened CSV.
        for field in ["fetch_category_names", "fetch_category_paths", "fetch_category_facets"]:
            row[field] = ";".join(row.get(field) or [])
        rows.append(row)
    return rows


def make_dataframe_csv_safe(df):
    for column in df.columns:
        df[column] = df[column].map(make_csv_safe)
    return df


def parse_args():
    parser = argparse.ArgumentParser(description="Tesco termekadatok letoltese a Tesco GraphQL API-bol.")
    parser.add_argument("--api-key", default=os.environ.get("TESCO_API_KEY", DEFAULT_API_KEY))
    parser.add_argument("--category-file", default=DEFAULT_CATEGORY_FILE)
    parser.add_argument("--no-category-refresh", action="store_true")
    parser.add_argument("--allow-stale-categories", action="store_true")
    parser.add_argument("--allow-partial-download", action="store_true")
    parser.add_argument("--refresh-categories-only", action="store_true")
    parser.add_argument("--without-promotional-categories", action="store_true")
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    parser.add_argument("--page-delay", type=float, default=0.2)
    parser.add_argument("--retries", type=int, default=4)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--category-limit", type=int)
    parser.add_argument("--page-limit", type=int)
    return parser.parse_args()


def main():
    args = parse_args()
    session = requests.Session()

    if args.no_category_refresh:
        categories = load_fetch_categories(args.category_file)
        print(
            f"Kategoriak betoltve helyi fajlbol: {args.category_file} ({len(categories)} db). "
            "Ez explicit --no-category-refresh futas."
        )
    else:
        try:
            categories = discover_fetch_categories(
                session=session,
                retries=args.retries,
                retry_delay=args.retry_delay,
                include_promotional=not args.without_promotional_categories,
            )
            snapshot = save_fetch_categories(categories, args.category_file)
            print(f"Fetch kategoriak frissitve: {len(categories)} db, snapshot={snapshot}")
        except Exception as error:
            if args.refresh_categories_only or not args.allow_stale_categories:
                raise
            print(f"Kategoriafrissites sikertelen, helyi fajl hasznalata explicit engedellyel: {error}")
            categories = load_fetch_categories(args.category_file)

    if args.category_limit:
        categories = categories[: args.category_limit]

    if args.refresh_categories_only:
        return

    products, failed_categories = fetch_products(
        session=session,
        categories=categories,
        request_headers=headers(args.api_key),
        count=args.count,
        page_delay=args.page_delay,
        retries=args.retries,
        retry_delay=args.retry_delay,
        page_limit=args.page_limit,
    )

    save_fetch_categories(categories, args.category_file)

    if failed_categories and not args.allow_partial_download:
        failed = ", ".join(f"{item['name']} ({item['error']})" for item in failed_categories[:10])
        raise RuntimeError(
            f"{len(failed_categories)} Tesco kategoria letoltese sikertelen, ezert nem irok hianyos all_data fajlt. "
            f"Elso hibak: {failed}"
        )
    if not products:
        raise RuntimeError("A Tesco letoltes 0 termeket adott vissza, ezert nem irok ures all_data fajlt.")

    detailed_categories_file = save_detailed_categories(products)

    df = pd.json_normalize(prepare_products_for_csv(products))
    df = make_dataframe_csv_safe(df)
    file_name = generate_filename("all_data")
    df.to_csv(file_name, index=False)

    print(f"\nMentes kesz: {len(products)} egyedi Tesco termek", file_name)
    if detailed_categories_file:
        print(f"Reszletes kategoriafa mentve: {detailed_categories_file}")


if __name__ == "__main__":
    main()
