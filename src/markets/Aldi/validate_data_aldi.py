import ast
import csv
import glob
import json
import os
import re


csv.field_size_limit(1024 * 1024 * 1024)

MAIN_FOLDER = "./../../../data/markets_data/"
MARKET_NAME = "aldi"
DEFAULT_PROVIDER_ID = "13"


def get_current_dir_name():
    return MARKET_NAME


def generate_filename(y_base, date_str: str, extension=".csv"):
    x = get_current_dir_name()
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


def clean_text(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def to_float(value):
    try:
        return float(clean_text(value).replace("\xa0", " ").replace(" ", "").replace(",", "."))
    except (TypeError, ValueError):
        return None


def parse_structured(value):
    value = clean_text(value)
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        pass
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def normalize_unit(value, unit):
    unit = clean_text(unit).lower()
    if value is None or not unit:
        return None, None
    if unit in {"kg", "kilogram", "kilogramm"}:
        return value * 1000, "g"
    if unit in {"g", "gr", "gram", "gramm"}:
        return value, "g"
    if unit in {"l", "liter", "litre"}:
        return value * 1000, "ml"
    if unit == "ml":
        return value, "ml"
    if unit == "cl":
        return value * 10, "ml"
    if unit in {"db", "darab", "pc", "pcs", "st", "rl", "pa", "pk", "csomag"}:
        return value, "db"
    return value, unit


NUMBER_PATTERN = r"(?:\d{1,3}(?:[ \xa0]\d{3})+|\d+)(?:[\.,]\d+)?"
UNIT_PATTERN = r"kg|g|ml|liter(?:es)?|l|cl|db|darab|pc|pcs"


def parse_number(value):
    return float(clean_text(value).replace("\xa0", " ").replace(" ", "").replace(",", "."))


def pack_candidates(text):
    text = clean_text(text).lower().replace("×", "x")
    results = []
    spans = []

    multipack_pattern = (
        rf"(?<![a-záéíóöőúüű0-9])({NUMBER_PATTERN})\s*x\s*({NUMBER_PATTERN})\s*"
        rf"(?:x\s*({NUMBER_PATTERN})\s*)?({UNIT_PATTERN})\b"
    )
    for match in re.finditer(multipack_pattern, text, flags=re.IGNORECASE):
        numbers = [match.group(1), match.group(2)]
        if match.group(3):
            numbers.append(match.group(3))
        total = 1.0
        for number in numbers:
            total *= parse_number(number)
        results.append(normalize_unit(total, match.group(4)))
        spans.append((match.start(), match.end()))

    single_pattern = rf"(?<![a-záéíóöőúüű0-9])({NUMBER_PATTERN})\s*({UNIT_PATTERN})\b"
    for match in re.finditer(single_pattern, text, flags=re.IGNORECASE):
        if any(start <= match.start() < end for start, end in spans):
            continue
        results.append(normalize_unit(parse_number(match.group(1)), match.group(2)))

    return results


def best_pack(text):
    packs = pack_candidates(text)
    return packs[-1] if packs else (None, None)


def format_pack(pack):
    value, unit = pack
    if value is None:
        return "", ""
    if abs(value - round(value)) < 0.000001:
        value = int(round(value))
    return value, unit


def selected_provider(row):
    providers = parse_structured(row.get("productProvider"))
    if not isinstance(providers, list):
        return {}
    selected_provider_id = clean_text(row.get("fetch_provider_id") or DEFAULT_PROVIDER_ID)
    for provider in providers:
        if isinstance(provider, dict) and clean_text(provider.get("providerID")) == selected_provider_id:
            return provider
    return providers[0] if providers and isinstance(providers[0], dict) else {}


def inferred_pack(row):
    price = to_float(row.get("price"))
    unit_price = to_float(row.get("unitPrice"))
    price_unit_type = clean_text(row.get("priceUnitType")).lower()
    if price is None or unit_price is None or unit_price <= 0:
        return None, None
    if price_unit_type == "kg":
        denominator, unit = 1000.0, "g"
    elif price_unit_type == "l":
        denominator, unit = 1000.0, "ml"
    elif price_unit_type in {"db", "darab", "csomag"}:
        denominator, unit = 1.0, "db"
    else:
        return None, None

    value = price / unit_price * denominator
    if value > 0 and abs(value - round(value)) <= max(0.35, value * 0.0015):
        value = float(round(value))
    return value, unit


def relative_difference(left_pack, right_pack):
    left_value, left_unit = left_pack
    right_value, right_unit = right_pack
    if left_value is None or right_value is None or left_unit != right_unit:
        return None
    return abs(left_value - right_value) / max(left_value, right_value)


def likely_drained_or_net_weight(row):
    text = clean_text(" ".join([row.get("productName", ""), row.get("fetch_category_path", "")])).lower()
    keywords = [
        "konzerv",
        "savany",
        "olíva",
        "oliva",
        "uborka",
        "befőtt",
        "befott",
        "lében",
        "leben",
        "olajban",
        "halkonzerv",
        "zöldségkonzerv",
        "zoldsegkonzerv",
    ]
    return any(keyword in text for keyword in keywords)


def classify_issue(row, provider, name_pack, provider_name_pack, unit_price_pack):
    direct_difference = relative_difference(name_pack, provider_name_pack)
    unit_difference = relative_difference(name_pack, unit_price_pack)

    if direct_difference is not None and direct_difference > 0.05:
        return "high", "direct_name_provider_package_conflict", direct_difference
    if unit_difference is not None and unit_difference > 0.05:
        if likely_drained_or_net_weight(row):
            return "info", "likely_net_or_drained_weight_unit_price", unit_difference
        if clean_text(row.get("priceUnitType")).lower() in {"darab", "db", "csomag"}:
            return "info", "piece_or_package_unit_price_rounding", unit_difference
        return "medium", "name_unit_price_package_conflict", unit_difference
    return None, None, None


def anomaly_rows(rows):
    result = []
    for row in rows:
        provider = selected_provider(row)
        name_pack = best_pack(row.get("productName"))
        provider_name_pack = best_pack(provider.get("providerProductName"))
        unit_price_pack = inferred_pack(row)
        severity, issue_type, diff = classify_issue(row, provider, name_pack, provider_name_pack, unit_price_pack)
        if not issue_type:
            continue

        name_value, name_unit = format_pack(name_pack)
        provider_value, provider_unit = format_pack(provider_name_pack)
        unit_price_value, unit_price_unit = format_pack(unit_price_pack)
        result.append(
            {
                "severity": severity,
                "issue_type": issue_type,
                "relative_difference": round(diff, 4) if diff is not None else "",
                "product_id": row.get("productID", ""),
                "product_name": row.get("productName", ""),
                "provider_product_name": provider.get("providerProductName", ""),
                "price": row.get("price", ""),
                "unit_price": row.get("unitPrice", ""),
                "price_unit_type": row.get("priceUnitType", ""),
                "name_pack_value": name_value,
                "name_pack_unit": name_unit,
                "provider_name_pack_value": provider_value,
                "provider_name_pack_unit": provider_unit,
                "unit_price_pack_value": unit_price_value,
                "unit_price_pack_unit": unit_price_unit,
                "provider_package_quantity": provider.get("packageQuantity", ""),
                "provider_package_base_unit": provider.get("packageBaseUnit", ""),
                "category": row.get("fetch_category_path", ""),
                "image_url": row.get("mediaUrlL") or row.get("mediaUrlM") or row.get("mediaUrlS") or "",
            }
        )
    severity_order = {"high": 0, "medium": 1, "info": 2}
    result.sort(key=lambda item: (severity_order.get(item["severity"], 99), -float(item["relative_difference"] or 0)))
    return result


def write_csv(path, rows):
    fieldnames = [
        "severity",
        "issue_type",
        "relative_difference",
        "product_id",
        "product_name",
        "provider_product_name",
        "price",
        "unit_price",
        "price_unit_type",
        "name_pack_value",
        "name_pack_unit",
        "provider_name_pack_value",
        "provider_name_pack_unit",
        "unit_price_pack_value",
        "unit_price_pack_unit",
        "provider_package_quantity",
        "provider_package_base_unit",
        "category",
        "image_url",
    ]
    with open(path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    input_file, input_date = read_latest_file("filtered_data")
    with open(input_file, mode="r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    anomalies = anomaly_rows(rows)
    output_file = generate_filename("package_anomalies", input_date)
    write_csv(output_file, anomalies)

    counts = {}
    for row in anomalies:
        counts[row["issue_type"]] = counts.get(row["issue_type"], 0) + 1
    print(f"Aldi kiszerelesi anomalia riport mentve: {output_file}")
    print(f"Anomalia sorok: {len(anomalies)}")
    for issue_type, count in sorted(counts.items()):
        print(f"  {issue_type}: {count}")


if __name__ == "__main__":
    main()
