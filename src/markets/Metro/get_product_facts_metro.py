import argparse
import csv
import faulthandler
import glob
import json
import os
import re
import threading
import time
import zlib
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

import requests


csv.field_size_limit(1024 * 1024 * 1024)

MAIN_FOLDER = "./../../../data/markets_data/"
DEFAULT_CACHE_DIR = "./../../../data/markets_data/metro_product_facts_pdfs"
DEFAULT_PDF_URL_TEMPLATE = "https://cdn.metro-group.com/hu/hu_fir_{display_id}_hu.pdf"
DEFAULT_PRODUCT_URL_TEMPLATE = "https://termekek.metro.hu/shop/pv/{article_id}/{variant_key}/{bundle_key}/{slug}"
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

output_fields = [
    "store_name",
    "store_product_id",
    "article_id",
    "variant_key",
    "bundle_key",
    "display_id",
    "customer_display_id",
    "product_name",
    "product_page_url",
    "pdf_url",
    "pdf_downloaded",
    "pdf_status_code",
    "pdf_error",
    "barcode",
    "ingredients",
    "nutrition_text",
    "storage_instructions",
    "serving_info",
    "legal_name",
    "responsible_company",
    "communication_address",
    "status_date",
    "fact_text",
]


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_multiline(value):
    lines = [clean_text(line) for line in str(value or "").splitlines()]
    text = "\n".join(line for line in lines if line)
    return re.sub(r"(?<=\d),\s+(?=\d)", ",", text)


def get_current_dir_name():
    return os.path.basename(os.getcwd()).lower()


def generate_filename(y_base, date_str=None, extension=".csv"):
    x = get_current_dir_name()
    date_str = date_str or datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{MAIN_FOLDER}{x}_{y_base}_{date_str}{extension}"


def read_latest_file(y_base: str, extension=".csv"):
    x = get_current_dir_name()
    pattern = f"{MAIN_FOLDER}{x}_{y_base}_*{extension}"
    candidates = glob.glob(pattern)
    if not candidates:
        raise FileNotFoundError(f"Nincs fajl: {pattern}")

    latest = max(candidates, key=os.path.getmtime)
    match = re.search(rf"{re.escape(x)}_{re.escape(y_base)}_(\d{{8}}_\d{{6}}){re.escape(extension)}", latest)
    if not match:
        raise ValueError("Nem sikerult datumot kinyerni a fajlnevbol.")
    date_str = match.group(1)
    print(f"Fajl kivalasztva: {latest} (datum: {date_str})")
    return latest, date_str


def slugify_product_name(name):
    slug = re.sub(r"\s+", "-", clean_text(name))
    return quote(slug, safe="")


def product_page_url(row):
    article_id = clean_text(row.get("article.bettyArticleId.bettyArticleId") or row.get("article_key"))
    variant_key = clean_text(row.get("variant_key"))
    bundle_key = clean_text(row.get("bundle_key"))
    product_name = clean_text(row.get("bundle.description") or row.get("variant.description"))
    if not article_id or not variant_key or not bundle_key:
        return ""
    return DEFAULT_PRODUCT_URL_TEMPLATE.format(
        article_id=article_id,
        variant_key=variant_key,
        bundle_key=bundle_key,
        slug=slugify_product_name(product_name),
    )


def request_with_retries(session, url, retries=3, retry_delay=2.0, timeout=60):
    last_error = None
    for attempt in range(1, retries + 1):
        retry_after = None
        try:
            response = session.get(
                url,
                headers={"User-Agent": "Mozilla/5.0", "Accept": "application/pdf,*/*"},
                timeout=timeout,
            )
            if response.status_code == 200:
                return response
            if response.status_code not in RETRYABLE_STATUS_CODES:
                return response
            retry_after = response.headers.get("Retry-After")
            last_error = requests.HTTPError(f"HTTP {response.status_code}: {url}")
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
    if last_error:
        raise last_error
    raise RuntimeError(f"Sikertelen lekeres: {url}")


def object_bodies(pdf_bytes):
    return {
        int(match.group(1)): match.group(2)
        for match in re.finditer(rb"\b(\d+)\s+0\s+obj(.*?)endobj", pdf_bytes, re.S)
    }


def stream_data(body):
    match = re.search(rb"stream\r?\n(.*?)\r?\nendstream", body, re.S)
    if not match:
        return b""
    data = match.group(1)
    if b"/FlateDecode" in body:
        try:
            return zlib.decompress(data)
        except zlib.error:
            return b""
    return data


def parse_cmap(data):
    text = data.decode("latin1", errors="ignore")
    mapping = {}

    for block in re.findall(r"beginbfchar(.*?)endbfchar", text, re.S):
        for source, target in re.findall(r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", block):
            codepoint = int(target, 16)
            mapping[int(source, 16)] = chr(codepoint) if codepoint <= 0x10FFFF else ""

    for block in re.findall(r"beginbfrange(.*?)endbfrange", text, re.S):
        for source_start, source_end, target in re.findall(
            r"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>",
            block,
        ):
            start = int(source_start, 16)
            end = int(source_end, 16)
            target_start = int(target, 16)
            # Hibas/serult cmap-ban a tartomany lehet ertelmetlenul nagy, ami
            # orakig tarto ciklust okozna - a valos cmap-ok 2 bajtosak (<=64k).
            if end < start or end - start > 0xFFFF:
                continue
            for offset, source_code in enumerate(range(start, end + 1)):
                codepoint = target_start + offset
                mapping[source_code] = chr(codepoint) if codepoint <= 0x10FFFF else ""
    return mapping


def font_maps_from_pdf(pdf_bytes):
    objects = object_bodies(pdf_bytes)
    font_objects = {}
    for body in objects.values():
        text = body.decode("latin1", errors="ignore")
        for font_name, object_id in re.findall(r"/(F\d+)\s+(\d+)\s+0\s+R", text):
            if "/Font" in text:
                font_objects[font_name] = int(object_id)

    font_maps = {}
    for font_name, object_id in font_objects.items():
        body = objects.get(object_id, b"").decode("latin1", errors="ignore")
        match = re.search(r"/ToUnicode\s+(\d+)\s+0\s+R", body)
        if not match:
            continue
        cmap_body = objects.get(int(match.group(1)), b"")
        font_maps[font_name] = parse_cmap(stream_data(cmap_body))
    return objects, font_maps


def decode_hex_with_font(hex_value, font_map):
    output = []
    for index in range(0, len(hex_value), 4):
        chunk = hex_value[index : index + 4]
        if len(chunk) != 4:
            continue
        try:
            output.append(font_map.get(int(chunk, 16), "?"))
        except ValueError:
            continue
    return "".join(output)


COMMON_TEXT_MARKERS = [
    "Milka",
    "alpesi",
    "tej",
    "csokol",
    "készül",
    "GTIN",
    "EAN",
    "Összetevő",
    "Tápérték",
    "Energia",
    "Zsír",
    "Rost",
    "Szénhidrát",
    "Fehérje",
    "Só",
    "Fogyasztói",
    "tárolási",
    "javaslat",
    "Hozzávetőleges",
    "Leíró",
    "terméknév",
    "Felelős",
    "Kommunikációs",
    "cím",
    "cukor",
    "pálma",
    "kakaó",
    "BÚZALISZT",
    "TEJPOR",
    "Budapest",
    "Neumann",
    "conserver",
    "kJ",
    "kcal",
]


def text_score(value):
    value = value or ""
    if not value:
        return -1000

    # GTIN-szeru szamcsoportonkent jar bonusz, mert a vonalkod-sorban tobb,
    # elvalasztoval felsorolt GTIN is lehet - a rossz fonttal dekodolt
    # betuszemet kulonben tobb pontot kapna, mint a helyes szamsor.
    barcode_bonus = 60 * len(re.findall(r"(?<!\d)\d{8,14}(?!\d)", value))
    good_chars = sum(
        char.isalnum()
        or char.isspace()
        or char in ".,;:!?%/()=-+–…ÁÉÍÓÖŐÚÜŰáéíóöőúüűàÀ"
        for char in value
    )
    bad_chars = value.count("?") * 4 + sum(ord(char) < 32 and char not in "\n\t" for char in value)
    marker_bonus = sum(8 for marker in COMMON_TEXT_MARKERS if marker in value)
    unit_bonus = 12 if re.search(r"\d+(?:[,.]\d+)?\s*(?:g|kg|mg|ml|l|kJ|kcal|%)\b", value) else 0
    word_bonus = 6 if re.search(r"[A-Za-zÁÉÍÓÖŐÚÜŰáéíóöőúüű]{4,}", value) else 0
    return good_chars - bad_chars + marker_bonus + unit_bonus + word_bonus + barcode_bonus


def best_decode(hex_values, current_font, font_maps):
    candidates = []
    ordered_fonts = [current_font] + [font for font in font_maps if font != current_font]
    for font_name in ordered_fonts:
        font_map = font_maps.get(font_name)
        if not font_map:
            continue
        text = "".join(decode_hex_with_font(hex_value, font_map) for hex_value in hex_values)
        candidates.append((text_score(text), text, font_name))
    if not candidates:
        return ""
    return max(candidates, key=lambda item: item[0])[1]


def merge_text_segments(segments):
    merged = []
    buffer = []

    def flush_buffer():
        if buffer:
            merged.append(clean_text("".join(buffer)))
            buffer.clear()

    for segment in segments:
        value = str(segment or "").strip()
        if not value:
            continue
        if len(value) == 1:
            buffer.append(value)
            continue
        flush_buffer()
        merged.append(value)
    flush_buffer()

    text = "\n".join(clean_text(line) for line in merged if clean_text(line))
    text = re.sub(r",(?=\S)", ", ", text)
    text = re.sub(r"(?<=\d),\s+(?=\d)", ",", text)
    text = re.sub(r"\.(?=[A-ZÁÉÍÓÖŐÚÜŰ])", ". ", text)
    return text


def extract_pdf_text(pdf_bytes):
    objects, font_maps = font_maps_from_pdf(pdf_bytes)
    if not font_maps:
        return ""

    segments = []
    for body in objects.values():
        data = stream_data(body)
        if b" TJ" not in data and b" Tj" not in data:
            continue
        content = data.decode("latin1", errors="ignore")
        current_font = None
        pending_font = None
        pending_hex_values = []

        def flush_pending():
            nonlocal pending_font, pending_hex_values
            if pending_font and pending_hex_values:
                text = best_decode(pending_hex_values, pending_font, font_maps)
                if clean_text(text):
                    segments.append(text)
            pending_font = None
            pending_hex_values = []

        token_pattern = r"/(F\d+)\s+[\d.]+\s+Tf|\[([^\]]*)\]\s*TJ|<([0-9A-Fa-f]+)>\s*Tj"
        for match in re.finditer(token_pattern, content, re.S):
            if match.group(1):
                flush_pending()
                current_font = match.group(1)
                continue
            if not current_font:
                continue
            if match.group(2) is not None:
                flush_pending()
                hex_values = re.findall(r"<([0-9A-Fa-f]+)>", match.group(2))
            elif match.group(3):
                if pending_font and pending_font != current_font:
                    flush_pending()
                pending_font = current_font
                pending_hex_values.append(match.group(3))
                continue
            else:
                hex_values = []
            if not hex_values:
                continue
            text = best_decode(hex_values, current_font, font_maps)
            if clean_text(text):
                segments.append(text)
        flush_pending()
    return merge_text_segments(segments)


def section_after_label(text, label, stop_labels):
    pattern = re.compile(re.escape(label) + r"\s*:?\s*(.*)", re.I | re.S)
    match = pattern.search(text)
    if not match:
        return ""
    rest = match.group(1)
    stop_indexes = []
    for stop_label in stop_labels:
        stop_match = re.search(re.escape(stop_label), rest, re.I)
        if stop_match:
            stop_indexes.append(stop_match.start())
    if stop_indexes:
        rest = rest[: min(stop_indexes)]
    return normalize_multiline(rest)


def gtin_checksum_valid(digits):
    if len(digits) not in {8, 12, 13, 14}:
        return False
    body = digits[:-1]
    check_digit = int(digits[-1])
    total = 0
    for index, digit in enumerate(reversed(body), start=1):
        total += int(digit) * (3 if index % 2 == 1 else 1)
    return (10 - (total % 10)) % 10 == check_digit


def select_barcode(candidates):
    valid = [value for value in candidates if gtin_checksum_valid(value)]
    # A fogyasztoi egyseg jellemzoen EAN-13, de a 2-vel kezdodo EAN-13 a bolti
    # belso tartomany (a Metro a sajat cikkszamat is igy sorolja fel), ezert az
    # csak vegso fallback. A 14 jegyu inkabb gyujtokarton.
    preferred = [value for value in valid if len(value) == 13 and not value.startswith("2")]
    if preferred:
        return preferred[0]
    for length in (8, 12, 14, 13):
        for value in valid:
            if len(value) == length:
                return value
    if valid:
        return valid[0]
    return candidates[0] if candidates else ""


def extract_facts_from_text(text):
    text = normalize_multiline(text)
    barcode_section = re.search(r"(?:GTIN\s*/\s*EAN|GTIN|EAN)\s*:?\s*([\d\s.,;/]{8,120})", text, re.I)
    barcode_candidates = (
        re.findall(r"(?<!\d)\d{8,14}(?!\d)", barcode_section.group(1)) if barcode_section else []
    )

    ingredients = section_after_label(
        text,
        "Összetevő",
        ["Tápérték információ", "Fogyasztói tárolási javaslat", "Leíró terméknév", "Status"],
    )
    nutrition_text = section_after_label(
        text,
        "Tápérték információ",
        ["Fogyasztói tárolási javaslat", "Hozzávetőleges adagok száma", "Leíró terméknév", "Status"],
    )
    storage = section_after_label(
        text,
        "Fogyasztói tárolási javaslat",
        ["Hozzávetőleges adagok száma", "Leíró terméknév", "Felelős cég neve", "Status"],
    )
    serving_info = section_after_label(
        text,
        "Hozzávetőleges adagok száma",
        ["Leíró terméknév", "Felelős cég neve", "Status"],
    )
    legal_name = section_after_label(
        text,
        "Leíró terméknév",
        ["Felelős cég neve", "Kommunikációs cím", "Status"],
    )
    responsible_company = section_after_label(
        text,
        "Felelős cég neve",
        ["Kommunikációs cím", "Status"],
    )
    communication_address = section_after_label(
        text,
        "Kommunikációs cím",
        ["Status"],
    )
    status_match = re.search(r"Status\s+(\d{2}\.\d{2}\.\d{4})", text)

    return {
        "barcode": select_barcode(barcode_candidates),
        "ingredients": ingredients,
        "nutrition_text": nutrition_text,
        "storage_instructions": storage,
        "serving_info": serving_info,
        "legal_name": legal_name,
        "responsible_company": responsible_company,
        "communication_address": communication_address,
        "status_date": status_match.group(1) if status_match else "",
        "fact_text": text,
    }


def select_rows(input_file, product_id=None, display_id=None, limit=None):
    rows = []
    with open(input_file, mode="r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row_product_id = clean_text(
                row.get("bundle_id")
                or row.get("bundle.bundleId.bettyBundleId")
                or row.get("variant_id")
                or row.get("search_result_id")
            )
            row_display_id = clean_text(row.get("bundle.displayId"))
            if product_id and row_product_id != product_id:
                continue
            if display_id and row_display_id != display_id:
                continue
            if not row_display_id:
                continue
            rows.append(row)
            if limit and len(rows) >= limit:
                break
    return rows


def cached_pdf_path(cache_dir, display_id):
    return Path(cache_dir) / f"hu_fir_{display_id}_hu.pdf"


def pdf_bytes_for_row(session, row, args):
    display_id = clean_text(row.get("bundle.displayId"))
    pdf_url = args.pdf_url_template.format(display_id=display_id)
    cache_path = cached_pdf_path(args.cache_dir, display_id)
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    if cache_path.exists() and not args.refresh:
        return cache_path.read_bytes(), pdf_url, True, "cache", ""

    response = request_with_retries(
        session,
        pdf_url,
        retries=args.retries,
        retry_delay=args.retry_delay,
        timeout=args.timeout,
    )
    if response.status_code != 200:
        return b"", pdf_url, False, str(response.status_code), f"HTTP {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    if b"%PDF" not in response.content[:16] and "pdf" not in content_type.lower():
        return response.content, pdf_url, False, str(response.status_code), f"Nem PDF valasz: {content_type}"

    cache_path.write_bytes(response.content)
    return response.content, pdf_url, True, str(response.status_code), ""


def output_row_from_source(row):
    article_id = clean_text(row.get("article.bettyArticleId.bettyArticleId") or row.get("article_key"))
    store_product_id = clean_text(
        row.get("bundle_id")
        or row.get("bundle.bundleId.bettyBundleId")
        or row.get("variant_id")
        or row.get("search_result_id")
    )
    return {
        "store_name": "Metro",
        "store_product_id": store_product_id,
        "article_id": article_id,
        "variant_key": clean_text(row.get("variant_key")),
        "bundle_key": clean_text(row.get("bundle_key")),
        "display_id": clean_text(row.get("bundle.displayId")),
        "customer_display_id": clean_text(row.get("bundle.customerDisplayId")),
        "product_name": clean_text(row.get("bundle.description") or row.get("variant.description")),
        "product_page_url": product_page_url(row),
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Metro PDF termekadatlapok letoltese es feldolgozasa.")
    parser.add_argument("--input-base", default="filtered_data")
    parser.add_argument("--product-id", default=None)
    parser.add_argument("--display-id", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--cache-dir", default=DEFAULT_CACHE_DIR)
    parser.add_argument("--pdf-url-template", default=DEFAULT_PDF_URL_TEMPLATE)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--retry-delay", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--allow-partial-download", action="store_true")
    return parser.parse_args()


WATCHDOG_PROGRESS = {"index": 0, "display_id": "", "time": time.time()}
WATCHDOG_STALL_SECONDS = 600


def watchdog_loop():
    while True:
        time.sleep(60)
        stalled = time.time() - WATCHDOG_PROGRESS["time"]
        if stalled > WATCHDOG_STALL_SECONDS:
            print(
                f"WATCHDOG: {int(stalled)} masodperce nincs elorelepes a(z) "
                f"{WATCHDOG_PROGRESS['index']}. sornal (display_id={WATCHDOG_PROGRESS['display_id']}), "
                "kenyszeritett leallas.",
                flush=True,
            )
            faulthandler.dump_traceback()
            os._exit(3)


def main():
    args = parse_args()
    threading.Thread(target=watchdog_loop, daemon=True).start()
    input_file, input_date = read_latest_file(args.input_base)
    selected_rows = select_rows(input_file, product_id=args.product_id, display_id=args.display_id, limit=args.limit)
    if not selected_rows:
        raise ValueError("Nincs feldolgozhato Metro sor a megadott feltetelekkel.")

    output_file = generate_filename("product_facts")
    counters = {
        "all": 0,
        "downloaded": 0,
        "barcode": 0,
        "ingredients": 0,
        "nutrition": 0,
        "errors": 0,
    }

    with requests.Session() as session, open(output_file, mode="w", encoding="utf-8", newline="") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=output_fields)
        writer.writeheader()

        for index, row in enumerate(selected_rows, start=1):
            counters["all"] += 1
            base_row = output_row_from_source(row)
            WATCHDOG_PROGRESS.update({"index": index, "display_id": base_row["display_id"], "time": time.time()})
            print(
                f"Metro PDF adatlap: {index}/{len(selected_rows)} "
                f"{base_row['display_id']} {base_row['product_name'][:80]}",
                flush=True,
            )

            facts = {field: "" for field in output_fields}
            try:
                pdf_bytes, pdf_url, downloaded, status_code, error = pdf_bytes_for_row(session, row, args)
                facts.update(base_row)
                facts.update(
                    {
                        "pdf_url": pdf_url,
                        "pdf_downloaded": downloaded,
                        "pdf_status_code": status_code,
                        "pdf_error": error,
                    }
                )
                if downloaded:
                    counters["downloaded"] += 1
                    parsed = extract_facts_from_text(extract_pdf_text(pdf_bytes))
                    facts.update(parsed)
                    if facts["barcode"]:
                        counters["barcode"] += 1
                    if facts["ingredients"]:
                        counters["ingredients"] += 1
                    if facts["nutrition_text"]:
                        counters["nutrition"] += 1
                elif error:
                    counters["errors"] += 1
            except Exception as error:
                counters["errors"] += 1
                facts.update(base_row)
                facts.update(
                    {
                        "pdf_url": args.pdf_url_template.format(display_id=base_row["display_id"]),
                        "pdf_downloaded": False,
                        "pdf_error": str(error),
                    }
                )
                if not args.allow_partial_download:
                    raise

            writer.writerow({field: facts.get(field, "") for field in output_fields})
            outfile.flush()

            if args.delay:
                time.sleep(args.delay)

    print(json.dumps(counters, ensure_ascii=False, indent=2))
    print(f"Metro PDF adatlap fajl mentve ide: {output_file}")


if __name__ == "__main__":
    main()
