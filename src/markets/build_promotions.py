import argparse
import csv
import glob
import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


csv.field_size_limit(1024 * 1024 * 1024)

PROMOTION_FIELDS = [
    "promotion_id",
    "promotion_group_id",
    "store_name",
    "store_product_id",
    "product_name",
    "promotion_type",
    "required_program",
    "source",
    "source_promotion_id",
    "label",
    "currency",
    "original_price",
    "discounted_price",
    "discount_percent",
    "discount_amount",
    "min_quantity",
    "buy_quantity",
    "get_quantity",
    "bundle_quantity",
    "bundle_price",
    "tier_quantity",
    "tier_gross_price",
    "tier_net_price",
    "tier_base_unit_price",
    "tier_base_unit",
    "unit_selling_info",
    "valid_from",
    "valid_to",
    "promotion_params",
    "raw_data",
]

PARAM_FIELDS = [
    "original_price",
    "discounted_price",
    "discount_percent",
    "discount_amount",
    "min_quantity",
    "buy_quantity",
    "get_quantity",
    "bundle_quantity",
    "bundle_price",
    "tier_quantity",
    "tier_gross_price",
    "tier_net_price",
    "tier_base_unit_price",
    "tier_base_unit",
]

OFFER_EXTRA_FIELDS = [
    "has_promotion",
    "promotion_count",
    "promotion_ids",
    "promotion_types",
    "promotion_required_programs",
]


def repo_root():
    return Path(__file__).resolve().parents[2]


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def to_float(value):
    if value is None:
        return None
    value = clean_text(value).replace("\xa0", " ").replace(" ", "").replace(",", ".")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def to_bool(value):
    if isinstance(value, bool):
        return value
    value = clean_text(value).lower()
    if value in {"true", "1", "yes", "igen"}:
        return True
    if value in {"false", "0", "no", "nem"}:
        return False
    return False


def parse_structured(value):
    value = clean_text(value)
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return None


def json_dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def latest_file(markets_dir, pattern):
    candidates = glob.glob(str(markets_dir / pattern))
    if not candidates:
        return None
    return Path(max(candidates, key=os.path.getmtime))


def latest_normalized_files(markets_dir):
    result = {}
    pattern = re.compile(r"(.+)_normalized_data_(\d{8}_\d{6})\.csv$")
    for file_name in glob.glob(str(markets_dir / "*_normalized_data_*.csv")):
        path = Path(file_name)
        match = pattern.match(path.name)
        if not match:
            continue
        store_key = match.group(1)
        current = result.get(store_key)
        if current is None or path.stat().st_mtime > current.stat().st_mtime:
            result[store_key] = path
    return result


def read_csv(path):
    with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(path, fieldnames, rows):
    with open(path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def compact_number(value):
    number = to_float(value)
    if number is None:
        return ""
    if abs(number - int(number)) < 0.000001:
        return str(int(number))
    return f"{number:.3f}".rstrip("0").rstrip(".")


def first_regex_number(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return compact_number(match.group(1))
    return ""


def extract_discount_percent(text):
    return first_regex_number([r"(\d+(?:[\.,]\d+)?)\s*%"], text)


def extract_discount_amount(text):
    return first_regex_number([r"(\d[\d\s]*(?:[\.,]\d+)?)\s*ft\s+kedvezm"], text)


def extract_min_quantity(text):
    return first_regex_number(
        [
            r"legal[aá]bb\s+(\d+(?:[\.,]\d+)?)\s*(?:db|darab)",
            r"(\d+(?:[\.,]\d+)?)\s*(?:db|darab)\s+v[aá]s[aá]rl[aá]sa",
            r"(\d+(?:[\.,]\d+)?)\s*(?:db|darab)\s+eset[eé]n",
        ],
        text,
    )


def extract_x_pay_y_get(text):
    match = re.search(
        r"(\d+)\s*(?:-?\s*(?:et|t))?\s+fizet.*?(\d+)\s*(?:-?\s*(?:at|et|t))?\s+kap",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return "", ""
    return compact_number(match.group(1)), compact_number(match.group(2))


def extract_bundle_price(text):
    match = re.search(
        r"(\d+(?:[\.,]\d+)?)\s*(?:db|darab).{0,20}?(\d[\d\s]*(?:[\.,]\d+)?)\s*ft",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        return "", ""
    return compact_number(match.group(1)), compact_number(match.group(2))


def extract_leading_price(text):
    match = re.search(r"^\s*(\d[\d\s]*(?:[\.,]\d+)?)\s*ft\b(.*)$", text, flags=re.IGNORECASE)
    if not match:
        return ""
    suffix = clean_text(match.group(2)).lower()
    if suffix.startswith("kedvezm"):
        return ""
    return compact_number(match.group(1))


def required_program(store_name, text, attributes=None, loyalty=False):
    lower_text = clean_text(text).lower()
    attrs = {clean_text(value).upper() for value in (attributes or [])}
    if "CLUBCARD_PRICING" in attrs or "clubcard" in lower_text:
        return "tesco_clubcard"
    if "supershop" in lower_text:
        return "supershop"
    if "lidlplus" in lower_text or "lidl plus" in lower_text:
        return "lidlplus"
    if loyalty:
        if store_name.lower() == "auchan":
            return "auchan_loyalty"
        return f"{store_name.lower()}_loyalty"
    return "none"


def classify_promotion(program, original_price="", discounted_price="", discount_percent="", discount_amount="", min_quantity="", buy_quantity="", get_quantity="", bundle_price="", tier=False, offline=False):
    loyalty = program and program != "none"
    if tier:
        return "quantity_price_tier"
    if buy_quantity and get_quantity:
        return "x_pay_y_get"
    if bundle_price:
        return "bundle_price"
    if min_quantity and (discount_percent or discount_amount or discounted_price):
        return "loyalty_quantity_discount" if loyalty else "quantity_discount"
    if discount_percent:
        return "loyalty_percentage_discount" if loyalty else "percentage_discount"
    if discount_amount:
        return "loyalty_amount_off" if loyalty else "amount_off"
    if original_price and discounted_price:
        return "loyalty_price_cut" if loyalty else "price_cut"
    if loyalty:
        return "loyalty_offer"
    if offline:
        return "store_promotion"
    return "unknown_promotion"


def promotion_group_id(record):
    basis = {
        "store_name": record.get("store_name", ""),
        "store_product_id": record.get("store_product_id", ""),
        "source": record.get("source", ""),
        "source_promotion_id": record.get("source_promotion_id", ""),
        "label": record.get("label", ""),
    }
    digest = hashlib.sha1(json_dump(basis).encode("utf-8")).hexdigest()[:12]
    return f"promogroup_{digest}"


def promotion_id(record):
    basis = {
        key: record.get(key, "")
        for key in [
            "promotion_group_id",
            "store_name",
            "store_product_id",
            "promotion_type",
            "source",
            "source_promotion_id",
            "label",
            "min_quantity",
            "buy_quantity",
            "get_quantity",
            "bundle_quantity",
            "bundle_price",
            "tier_quantity",
            "tier_gross_price",
            "discounted_price",
            "original_price",
            "valid_from",
            "valid_to",
        ]
    }
    digest = hashlib.sha1(json_dump(basis).encode("utf-8")).hexdigest()[:12]
    return f"promo_{digest}"


def finalize_record(record):
    result = {field: "" for field in PROMOTION_FIELDS}
    for key, value in record.items():
        if key in result:
            result[key] = clean_text(value)
    result["currency"] = result["currency"] or "HUF"
    result["promotion_group_id"] = result["promotion_group_id"] or promotion_group_id(result)
    params = {field: result[field] for field in PARAM_FIELDS if clean_text(result[field])}
    result["promotion_params"] = json_dump(params) if params else ""
    result["promotion_id"] = result["promotion_id"] or promotion_id(result)
    return result


def promotion_key(record):
    return (record.get("store_name", ""), record.get("store_product_id", ""))


def add_record(records, record):
    finalized = finalize_record(record)
    records.append(finalized)
    return finalized


def parse_tesco_promotions(markets_dir, records):
    path = latest_file(markets_dir, "tesco_filtered_data_*.csv")
    if path is None:
        return

    for row in read_csv(path):
        promotions = parse_structured(row.get("promotions"))
        if not isinstance(promotions, list) or not promotions:
            continue

        store_product_id = clean_text(row.get("id") or row.get("tpnc"))
        product_name = clean_text(row.get("title"))
        for promotion in promotions:
            if not isinstance(promotion, dict):
                continue

            price = promotion.get("price") if isinstance(promotion.get("price"), dict) else {}
            label = clean_text(promotion.get("description"))
            unit_selling_info = clean_text(promotion.get("unitSellingInfo"))
            text = f"{label} {unit_selling_info}"
            attributes = promotion.get("attributes") if isinstance(promotion.get("attributes"), list) else []
            program = required_program("Tesco", text, attributes)

            original_price = compact_number(price.get("beforeDiscount"))
            discounted_price = compact_number(price.get("afterDiscount"))
            leading_price = extract_leading_price(label)
            if program != "none" and leading_price:
                discounted_price = leading_price
                if not original_price:
                    original_price = compact_number(row.get("price.actual") or price.get("afterDiscount"))
            discount_percent = extract_discount_percent(text)
            discount_amount = extract_discount_amount(text)
            min_quantity = extract_min_quantity(text)
            buy_quantity, get_quantity = extract_x_pay_y_get(text)
            bundle_quantity, bundle_price = extract_bundle_price(text)

            promotion_type = classify_promotion(
                program,
                original_price=original_price,
                discounted_price=discounted_price,
                discount_percent=discount_percent,
                discount_amount=discount_amount,
                min_quantity=min_quantity,
                buy_quantity=buy_quantity,
                get_quantity=get_quantity,
                bundle_price=bundle_price,
            )

            add_record(
                records,
                {
                    "store_name": "Tesco",
                    "store_product_id": store_product_id,
                    "product_name": product_name,
                    "promotion_type": promotion_type,
                    "required_program": program,
                    "source": "tesco.promotions",
                    "source_promotion_id": clean_text(promotion.get("id")),
                    "label": label,
                    "original_price": original_price,
                    "discounted_price": discounted_price,
                    "discount_percent": discount_percent,
                    "discount_amount": discount_amount,
                    "min_quantity": min_quantity,
                    "buy_quantity": buy_quantity,
                    "get_quantity": get_quantity,
                    "bundle_quantity": bundle_quantity,
                    "bundle_price": bundle_price,
                    "unit_selling_info": unit_selling_info,
                    "valid_from": clean_text(promotion.get("startDate")),
                    "valid_to": clean_text(promotion.get("endDate")),
                    "raw_data": json_dump(promotion),
                },
            )


def parse_auchan_promotions(markets_dir, records):
    path = latest_file(markets_dir, "auchan_filtered_data_*.csv")
    if path is None:
        return

    for row in read_csv(path):
        is_discounted = to_bool(row.get("selectedVariant.price.isDiscounted"))
        is_loyalty = to_bool(row.get("selectedVariant.isLoyaltyPriceValid"))
        is_offline = to_bool(row.get("selectedVariant.isOfflinePromotion"))
        if not (is_discounted or is_loyalty or is_offline):
            continue

        product_id = clean_text(row.get("id"))
        variant_id = clean_text(row.get("selectedVariant.id") or row.get("defaultVariant.id"))
        store_product_id = f"{product_id}:{variant_id}" if variant_id else product_id
        product_name = clean_text(row.get("selectedVariant.name") or row.get("defaultVariant.name"))
        gross = compact_number(row.get("selectedVariant.price.gross"))
        discounted = compact_number(row.get("selectedVariant.price.grossDiscounted"))
        discount_percent = compact_number(
            row.get("selectedVariant.price.discountDisplayPercentage")
            or row.get("selectedVariant.price.discountPercentage")
        )
        program = required_program("Auchan", "", loyalty=is_loyalty)

        original_price = ""
        discounted_price = ""
        if gross and discounted and to_float(gross) is not None and to_float(discounted) is not None and to_float(gross) > to_float(discounted):
            original_price = gross
            discounted_price = discounted

        label = "Auchan husegprogramos ar" if is_loyalty else "Auchan akcio"
        if is_offline and not original_price:
            label = "Auchan offline promóció"

        promotion_type = classify_promotion(
            program,
            original_price=original_price,
            discounted_price=discounted_price,
            discount_percent=discount_percent if to_float(discount_percent) else "",
            offline=is_offline,
        )

        raw = {
            "price.gross": row.get("selectedVariant.price.gross"),
            "price.grossDiscounted": row.get("selectedVariant.price.grossDiscounted"),
            "price.discountPercentage": row.get("selectedVariant.price.discountPercentage"),
            "price.discountDisplayPercentage": row.get("selectedVariant.price.discountDisplayPercentage"),
            "price.isDiscounted": row.get("selectedVariant.price.isDiscounted"),
            "isLoyaltyPriceValid": row.get("selectedVariant.isLoyaltyPriceValid"),
            "isOfflinePromotion": row.get("selectedVariant.isOfflinePromotion"),
        }

        add_record(
            records,
            {
                "store_name": "Auchan",
                "store_product_id": store_product_id,
                "product_name": product_name,
                "promotion_type": promotion_type,
                "required_program": program,
                "source": "auchan.selectedVariant.price",
                "label": label,
                "original_price": original_price,
                "discounted_price": discounted_price,
                "discount_percent": discount_percent if to_float(discount_percent) else "",
                "raw_data": json_dump(raw),
            },
        )


def file_date(path):
    match = re.search(r"_(\d{8}_\d{6})\.csv$", path.name)
    return match.group(1) if match else ""


def parse_metro_tier_promotions(markets_dir, records, normalized_files):
    path = latest_file(markets_dir, "metro_price_tiers_*.csv")
    if path is None:
        return

    # Ha az arsav fajl nem ugyanabbol a futasbol szarmazik, mint a legfrissebb
    # Metro normalizalt fajl, akkor elavult arakat parositanank - inkabb kimarad.
    metro_normalized = normalized_files.get("metro")
    if metro_normalized is not None:
        tiers_date = file_date(path)
        normalized_date = file_date(metro_normalized)
        if tiers_date and normalized_date and tiers_date != normalized_date:
            print("=" * 72)
            print(f"FIGYELEM: a Metro arsav fajl ({path.name}) datuma nem egyezik")
            print(f"a legfrissebb Metro normalizalt fajleval ({metro_normalized.name}).")
            print("Az elavult mennyisegi arsavok kimaradnak a promocios tablabol!")
            print("Futtasd ujra a Metro letoltest es normalizalast a frissiteshez.")
            print("=" * 72)
            return

    for row in read_csv(path):
        discount_value = to_float(row.get("tier_discount_value"))
        discount_percent = ""
        if discount_value is not None:
            discount_percent = compact_number(discount_value * 100)

        group_basis = {
            "store_name": "Metro",
            "store_product_id": row.get("store_product_id"),
            "source": row.get("tier_source"),
            "label": row.get("tier_label"),
        }
        group_digest = hashlib.sha1(json_dump(group_basis).encode("utf-8")).hexdigest()[:12]

        add_record(
            records,
            {
                "promotion_group_id": f"promogroup_{group_digest}",
                "store_name": "Metro",
                "store_product_id": clean_text(row.get("store_product_id")),
                "product_name": clean_text(row.get("product_name")),
                "promotion_type": "quantity_price_tier",
                "required_program": "none",
                "source": "metro.price.summaryDnrInfo",
                "label": clean_text(row.get("tier_label")),
                "discount_percent": discount_percent,
                "min_quantity": compact_number(row.get("tier_min_quantity")),
                "tier_quantity": compact_number(row.get("tier_min_quantity")),
                "tier_gross_price": compact_number(row.get("tier_final_gross_price")),
                "tier_net_price": compact_number(row.get("tier_final_net_price")),
                "tier_base_unit_price": compact_number(row.get("tier_base_unit_price")),
                "tier_base_unit": clean_text(row.get("tier_base_unit")),
                "valid_from": clean_text(row.get("tier_valid_from")),
                "valid_to": clean_text(row.get("tier_valid_to")),
                "raw_data": json_dump(row),
            },
        )


def parse_normalized_fallback_promotions(normalized_files, records):
    existing_keys = {promotion_key(record) for record in records}

    for path in normalized_files.values():
        for row in read_csv(path):
            store_name = clean_text(row.get("store_name"))
            store_product_id = clean_text(row.get("store_product_id"))
            if not store_name or not store_product_id:
                continue
            if (store_name, store_product_id) in existing_keys:
                continue
            if not to_bool(row.get("is_discounted")):
                continue

            original_price = compact_number(row.get("original_unit_price"))
            discounted_price = compact_number(row.get("unit_price"))
            if not original_price or not discounted_price:
                # Az akcios jelzes eredeti ar nelkul is keruljon be, kulonben a
                # csak flaggel jelolt akciok (pl. Penny/Roksh, Metro) elvesznek.
                if not discounted_price:
                    continue
                add_record(
                    records,
                    {
                        "store_name": store_name,
                        "store_product_id": store_product_id,
                        "product_name": clean_text(row.get("product_name")),
                        "promotion_type": "discount_flag_only",
                        "required_program": "none",
                        "source": "normalized.is_discounted",
                        "label": "Akciós jelölés eredeti ár nélkül",
                        "discounted_price": discounted_price,
                        "raw_data": json_dump(
                            {
                                "unit_price": row.get("unit_price"),
                                "original_unit_price": row.get("original_unit_price"),
                                "is_discounted": row.get("is_discounted"),
                            }
                        ),
                    },
                )
                continue

            discount_percent = ""
            original_float = to_float(original_price)
            discounted_float = to_float(discounted_price)
            if original_float and discounted_float is not None and original_float > 0:
                discount_percent = compact_number((original_float - discounted_float) / original_float * 100)

            add_record(
                records,
                {
                    "store_name": store_name,
                    "store_product_id": store_product_id,
                    "product_name": clean_text(row.get("product_name")),
                    "promotion_type": "price_cut",
                    "required_program": "none",
                    "source": "normalized.original_unit_price",
                    "label": "Eredeti ár és aktuális ár különbsége",
                    "original_price": original_price,
                    "discounted_price": discounted_price,
                    "discount_percent": discount_percent,
                    "raw_data": json_dump(
                        {
                            "unit_price": row.get("unit_price"),
                            "original_unit_price": row.get("original_unit_price"),
                            "is_discounted": row.get("is_discounted"),
                        }
                    ),
                },
            )


def build_offer_rows(normalized_files, records):
    promotions_by_offer = defaultdict(list)
    for record in records:
        promotions_by_offer[promotion_key(record)].append(record)

    rows = []
    base_fields = []
    seen_base_fields = set()

    for path in sorted(normalized_files.values(), key=lambda value: value.name):
        with open(path, mode="r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)
            for field in reader.fieldnames or []:
                if field not in seen_base_fields:
                    seen_base_fields.add(field)
                    base_fields.append(field)

            for row in reader:
                store_name = clean_text(row.get("store_name"))
                store_product_id = clean_text(row.get("store_product_id"))
                offer_promotions = promotions_by_offer.get((store_name, store_product_id), [])
                promotion_ids = [promotion["promotion_id"] for promotion in offer_promotions]
                promotion_types = sorted({promotion["promotion_type"] for promotion in offer_promotions if promotion["promotion_type"]})
                programs = sorted({promotion["required_program"] for promotion in offer_promotions if promotion["required_program"] and promotion["required_program"] != "none"})

                output_row = {field: row.get(field, "") for field in base_fields}
                output_row.update(
                    {
                        "has_promotion": bool(offer_promotions),
                        "promotion_count": len(offer_promotions),
                        "promotion_ids": ";".join(promotion_ids),
                        "promotion_types": ";".join(promotion_types),
                        "promotion_required_programs": ";".join(programs),
                    }
                )
                rows.append(output_row)

    return base_fields + OFFER_EXTRA_FIELDS, rows


def parse_args():
    parser = argparse.ArgumentParser(description="Kozos bolti kedvezmeny/promocio tabla epitese.")
    parser.add_argument(
        "--markets-dir",
        default=str(repo_root() / "data" / "markets_data"),
        help="A bolti CSV-ket tartalmazo mappa.",
    )
    parser.add_argument("--skip-offers", action="store_true", help="Csak a promotions CSV keszuljon el.")
    return parser.parse_args()


def main():
    args = parse_args()
    markets_dir = Path(args.markets_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    normalized_files = latest_normalized_files(markets_dir)
    if not normalized_files:
        raise FileNotFoundError(f"Nincs normalized_data fajl ebben a mappaban: {markets_dir}")

    records = []
    parse_tesco_promotions(markets_dir, records)
    parse_auchan_promotions(markets_dir, records)
    parse_metro_tier_promotions(markets_dir, records, normalized_files)
    parse_normalized_fallback_promotions(normalized_files, records)

    records.sort(key=lambda row: (row["store_name"], row["store_product_id"], row["promotion_group_id"], row["promotion_id"]))
    promotions_file = markets_dir / f"promotions_{timestamp}.csv"
    write_csv(promotions_file, PROMOTION_FIELDS, records)

    print(f"Promocio tabla mentve ide: {promotions_file}")
    print(f"Promocio sorok: {len(records)}")
    for store_name, count in sorted(Counter(row["store_name"] for row in records).items()):
        print(f"  {store_name}: {count}")
    for promotion_type, count in sorted(Counter(row["promotion_type"] for row in records).items()):
        print(f"  {promotion_type}: {count}")

    if not args.skip_offers:
        offer_fields, offer_rows = build_offer_rows(normalized_files, records)
        offers_file = markets_dir / f"offers_with_promotions_{timestamp}.csv"
        write_csv(offers_file, offer_fields, offer_rows)
        print(f"Termekajanlatok promocio hivatkozassal mentve ide: {offers_file}")
        print(f"Termekajanlat sorok: {len(offer_rows)}")


if __name__ == "__main__":
    main()
