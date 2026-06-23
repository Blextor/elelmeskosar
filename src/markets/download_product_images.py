import argparse
import csv
import glob
import hashlib
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

import requests

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from image_size import to_full_size


csv.field_size_limit(1024 * 1024 * 1024)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
THREAD_LOCAL = threading.local()


def repo_root():
    return Path(__file__).resolve().parents[2]


def markets_dir():
    return repo_root() / "data" / "markets_data"


def images_root():
    return markets_dir() / "product_images"


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def latest_normalized_files(directory):
    result = {}
    pattern = re.compile(r"(.+)_normalized_data_(\d{8}_\d{6})\.csv$")
    for file_name in glob.glob(str(directory / "*_normalized_data_*.csv")):
        path = Path(file_name)
        match = pattern.match(path.name)
        if not match:
            continue
        store_key = match.group(1)
        current = result.get(store_key)
        if current is None or path.stat().st_mtime > current.stat().st_mtime:
            result[store_key] = path
    return result


def split_image_urls(value):
    urls = []
    for part in str(value or "").split(";"):
        part = clean_text(part)
        if part and part.lower() not in {"none", "nan"} and part.lower().startswith("http"):
            part = to_full_size(part)  # mindig az eredeti/legnagyobb méretet töltjük
            if part not in urls:
                urls.append(part)
    return urls


def extension_for_url(url):
    path = urlsplit(url).path
    suffix = Path(path).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".jpg"


def local_path_for_url(store_key, url):
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    return images_root() / store_key / f"{digest}{extension_for_url(url)}"


def relative_path(path):
    return path.relative_to(repo_root()).as_posix()


def get_session():
    session = getattr(THREAD_LOCAL, "session", None)
    if session is None:
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0",
                "Accept": "image/*,*/*",
            }
        )
        THREAD_LOCAL.session = session
    return session


def download_image(url, target_path, timeout, retries, retry_delay, delay=0.0):
    session = get_session()
    last_error = ""
    for attempt in range(1, retries + 1):
        try:
            if delay:
                time.sleep(delay)
            response = session.get(url, timeout=timeout)
            if response.status_code != 200:
                last_error = f"HTTP {response.status_code}"
                if response.status_code in {429, 500, 502, 503, 504} and attempt < retries:
                    time.sleep(retry_delay * attempt)
                    continue
                return "failed", str(response.status_code), 0, last_error
            content = response.content
            content_type = response.headers.get("Content-Type", "").lower()
            if not content or "text/html" in content_type or content[:1].lstrip() == b"<":
                return "failed", str(response.status_code), len(content), f"Nem kep valasz: {content_type}"
            target_path.parent.mkdir(parents=True, exist_ok=True)
            tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")
            tmp_path.write_bytes(content)
            os.replace(tmp_path, target_path)
            return "downloaded", "200", len(content), ""
        except Exception as error:
            last_error = str(error)
            if attempt < retries:
                time.sleep(retry_delay * attempt)
    return "failed", "", 0, last_error


def collect_store_rows(path, max_per_product):
    rows = []
    with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        if "image_urls" not in (reader.fieldnames or []):
            return None
        for row in reader:
            urls = split_image_urls(row.get("image_urls"))
            if max_per_product > 0:
                urls = urls[:max_per_product]
            rows.append(
                {
                    "store_name": clean_text(row.get("store_name")),
                    "store_product_id": clean_text(row.get("store_product_id")),
                    "product_name": clean_text(row.get("product_name")),
                    "urls": urls,
                }
            )
    return rows


def process_store(store_key, normalized_path, args):
    rows = collect_store_rows(normalized_path, args.max_per_product)
    if rows is None:
        print(f"{store_key}: nincs image_urls oszlop, kihagyva ({normalized_path.name})", flush=True)
        return

    url_targets = {}
    for row in rows:
        for url in row["urls"]:
            if url not in url_targets:
                url_targets[url] = local_path_for_url(store_key, url)

    missing = {
        url: path for url, path in url_targets.items() if args.refresh or not path.exists()
    }
    cached_count = len(url_targets) - len(missing)
    print(
        f"{store_key}: {len(rows)} termek, {len(url_targets)} egyedi kep URL, "
        f"{cached_count} mar megvan, {len(missing)} letoltendo",
        flush=True,
    )

    url_results = {url: ("cached", "", 0, "") for url in url_targets if url not in missing}
    if missing:
        done = 0
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    download_image, url, path, args.timeout, args.retries, args.retry_delay, args.delay
                ): url
                for url, path in missing.items()
            }
            for future in as_completed(futures):
                url = futures[future]
                try:
                    url_results[url] = future.result()
                except Exception as error:
                    url_results[url] = ("failed", "", 0, str(error))
                done += 1
                if done % 500 == 0 or done == len(missing):
                    print(f"  {store_key}: {done}/{len(missing)} kep letoltve", flush=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    index_path = markets_dir() / f"{store_key}_image_index_{timestamp}.csv"
    counters = {"downloaded": 0, "cached": 0, "failed": 0, "no_url": 0}
    local_paths_by_product = {}

    with open(index_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "store_name",
                "store_product_id",
                "product_name",
                "image_url",
                "local_path",
                "status",
                "http_status",
                "bytes",
                "error",
            ],
        )
        writer.writeheader()
        for row in rows:
            if not row["urls"]:
                counters["no_url"] += 1
                writer.writerow(
                    {
                        "store_name": row["store_name"],
                        "store_product_id": row["store_product_id"],
                        "product_name": row["product_name"],
                        "image_url": "",
                        "local_path": "",
                        "status": "no_url",
                        "http_status": "",
                        "bytes": "",
                        "error": "",
                    }
                )
                continue
            collected = []
            for url in row["urls"]:
                status, http_status, size, error = url_results.get(url, ("failed", "", 0, "ismeretlen"))
                target = url_targets[url]
                ok = status in {"downloaded", "cached"} and target.exists()
                if ok:
                    collected.append(relative_path(target))
                counters[status if status in counters else "failed"] += 1
                writer.writerow(
                    {
                        "store_name": row["store_name"],
                        "store_product_id": row["store_product_id"],
                        "product_name": row["product_name"],
                        "image_url": url,
                        "local_path": relative_path(target) if ok else "",
                        "status": status,
                        "http_status": http_status,
                        "bytes": size or "",
                        "error": error,
                    }
                )
            key = (row["store_name"], row["store_product_id"])
            local_paths_by_product[key] = ";".join(collected)

    enrich_normalized_file(normalized_path, local_paths_by_product)

    print(
        f"{store_key}: kesz | uj letoltes: {counters['downloaded']}, cache: {counters['cached']}, "
        f"hibas: {counters['failed']}, kep nelkul: {counters['no_url']}",
        flush=True,
    )
    print(f"{store_key}: kep index mentve: {index_path}", flush=True)
    if counters["failed"]:
        print(f"{store_key}: FIGYELEM, {counters['failed']} kep letoltese nem sikerult.", flush=True)


def enrich_normalized_file(normalized_path, local_paths_by_product):
    with open(normalized_path, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if "local_image_paths" not in fieldnames:
        fieldnames.append("local_image_paths")

    for row in rows:
        key = (clean_text(row.get("store_name")), clean_text(row.get("store_product_id")))
        row["local_image_paths"] = local_paths_by_product.get(key, "")

    tmp_path = normalized_path.with_suffix(".csv.tmp")
    with open(tmp_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(tmp_path, normalized_path)
    print(f"local_image_paths oszlop frissitve: {normalized_path.name}", flush=True)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Termekkepek inkrementalis letoltese a normalizalt CSV-k alapjan."
    )
    parser.add_argument(
        "--stores",
        default="",
        help="Vesszovel elvalasztott bolt-kulcsok (pl. penny,aldi). Ures = osszes.",
    )
    parser.add_argument(
        "--max-per-product",
        type=int,
        default=1,
        help="Hany kepet toltsunk termekenkent (0 = osszes URL).",
    )
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-delay", type=float, default=1.5)
    parser.add_argument(
        "--delay",
        type=float,
        default=0.0,
        help="Keslektetes (mp) minden kep-lekeres elott szalankent. WAF/rate limit mogotti boltoknal hasznos (pl. coopshop).",
    )
    parser.add_argument("--refresh", action="store_true", help="Meglevo kepek ujraletoltese is.")
    return parser.parse_args()


def main():
    args = parse_args()
    normalized_files = latest_normalized_files(markets_dir())
    if not normalized_files:
        raise FileNotFoundError(f"Nincs normalized_data fajl itt: {markets_dir()}")

    selected = {item.strip().lower() for item in args.stores.split(",") if item.strip()}
    if selected:
        unknown = selected - set(normalized_files)
        if unknown:
            raise ValueError(f"Ismeretlen bolt-kulcs(ok): {sorted(unknown)}. Elerheto: {sorted(normalized_files)}")
        normalized_files = {key: path for key, path in normalized_files.items() if key in selected}

    images_root().mkdir(parents=True, exist_ok=True)
    for store_key in sorted(normalized_files):
        process_store(store_key, normalized_files[store_key], args)


if __name__ == "__main__":
    main()
