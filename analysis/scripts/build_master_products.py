import argparse
import csv
import glob
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
from urllib.parse import urlsplit, urlunsplit


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


ROOT_DIR = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = ROOT_DIR / "data" / "markets_data"
DEFAULT_REPORTS_DIR = ROOT_DIR / "analysis" / "reports"
STORE_PREFIXES = {
    "Spar": "spar",
    "Prima": "prima",
    "Tesco": "tesco",
}


@dataclass
class SourceRecord:
    source_id: str
    row_index: int
    store_name: str
    store_product_id: str
    product_name: str
    brand_name: str
    barcode: str
    barcode_norm: str
    unit_price: Optional[float]
    unit_type: str
    unit_step: Optional[float]
    base_price: Optional[float]
    base_unit: str
    available: str
    is_discounted: str
    original_unit_price: str
    image_urls: str
    image_key: str
    categories: str
    name_key: str
    name_core: str


class UnionFind:
    def __init__(self, items: Iterable[str]):
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item: str) -> str:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, a: str, b: str) -> bool:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        return True


def clean_text(value) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def to_float(value) -> Optional[float]:
    value = clean_text(value).replace(",", ".")
    if not value:
        return None
    try:
        return float(value)
    except ValueError:
        return None


def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def normalize_name(value: str) -> str:
    value = strip_accents(clean_text(value).casefold())
    value = value.replace("×", "x")
    value = re.sub(r"[^0-9a-z]+", " ", value)
    return clean_text(value)


def normalize_name_core(value: str) -> str:
    value = normalize_name(value)
    value = re.sub(r"\b\d+(?:[.,]\d+)?\s*x\s*\d+(?:[.,]\d+)?\s*(kg|g|ml|l|cl|db|pcs|pc|lap|darab)\b", " ", value)
    value = re.sub(r"\b\d+(?:[.,]\d+)?\s*(kg|g|ml|l|cl|db|pcs|pc|lap|darab)\b", " ", value)
    value = re.sub(r"\b\d+(?:[.,]\d+)?\s*%\b", " ", value)
    value = re.sub(r"\b\d+\b", " ", value)
    return clean_text(value)


def normalize_barcode(value: str) -> str:
    digits = re.sub(r"\D+", "", clean_text(value))
    if not digits:
        return ""
    return digits.lstrip("0") or "0"


def first_image_url(value: str) -> str:
    for part in re.split(r"[;|]", clean_text(value)):
        part = part.strip()
        if part:
            return part
    return ""


def normalize_image_key(value: str) -> str:
    url = first_image_url(value)
    if not url:
        return ""
    parsed = urlsplit(url)
    if not parsed.netloc:
        return clean_text(url).lower()
    path = re.sub(r"/+", "/", parsed.path.rstrip("/"))
    if "no-image" in path.lower():
        return ""
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", "")).lower()


def base_price(unit_price: Optional[float], unit_step: Optional[float], unit_type: str) -> Tuple[Optional[float], str]:
    if unit_price is None or unit_step is None or unit_step <= 0:
        return None, ""
    unit_type = clean_text(unit_type).lower()
    if unit_type == "g":
        return round(unit_price / unit_step * 1000, 3), "kg"
    if unit_type == "ml":
        return round(unit_price / unit_step * 1000, 3), "l"
    if unit_type == "db":
        return round(unit_price / unit_step, 3), "db"
    return None, ""


def package_relation(a: SourceRecord, b: SourceRecord) -> str:
    if not a.unit_type or not b.unit_type or a.unit_step is None or b.unit_step is None:
        return "unknown"
    if a.unit_type != b.unit_type:
        return "different_unit"
    smaller = min(a.unit_step, b.unit_step)
    larger = max(a.unit_step, b.unit_step)
    if smaller <= 0:
        return "unknown"
    ratio = larger / smaller
    if ratio <= 1.03:
        return "same"
    if ratio <= 1.25:
        return "close"
    return "different_size"


def names_similarity(a: SourceRecord, b: SourceRecord) -> float:
    if not a.name_key or not b.name_key:
        return 0.0
    return round(SequenceMatcher(None, a.name_key, b.name_key).ratio(), 4)


def latest_normalized_file(data_dir: Path, prefix: str) -> Path:
    pattern = str(data_dir / f"{prefix}_normalized_data_*.csv")
    candidates = glob.glob(pattern)
    if not candidates:
        raise FileNotFoundError(f"Nincs normalizált fájl ehhez: {pattern}")
    return Path(max(candidates, key=os.path.getmtime))


def read_store_file(path: Path, fallback_store_name: str) -> List[SourceRecord]:
    records: List[SourceRecord] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for index, row in enumerate(reader, start=1):
            store_name = clean_text(row.get("store_name")) or fallback_store_name
            store_product_id = clean_text(row.get("store_product_id")) or f"row-{index}"
            product_name = clean_text(row.get("product_name"))
            barcode = clean_text(row.get("barcode"))
            unit_price = to_float(row.get("unit_price"))
            unit_step = to_float(row.get("unit_step"))
            unit_type = clean_text(row.get("unit_type")).lower()
            calculated_base_price, calculated_base_unit = base_price(unit_price, unit_step, unit_type)
            image_urls = clean_text(row.get("image_urls"))
            source_id = f"{store_name}:{store_product_id}"
            records.append(
                SourceRecord(
                    source_id=source_id,
                    row_index=index,
                    store_name=store_name,
                    store_product_id=store_product_id,
                    product_name=product_name,
                    brand_name=clean_text(row.get("brand_name")),
                    barcode=barcode,
                    barcode_norm=normalize_barcode(barcode),
                    unit_price=unit_price,
                    unit_type=unit_type,
                    unit_step=unit_step,
                    base_price=calculated_base_price,
                    base_unit=calculated_base_unit,
                    available=clean_text(row.get("available")),
                    is_discounted=clean_text(row.get("is_discounted")),
                    original_unit_price=clean_text(row.get("original_unit_price")),
                    image_urls=image_urls,
                    image_key=normalize_image_key(image_urls),
                    categories=clean_text(row.get("categories")),
                    name_key=normalize_name(product_name),
                    name_core=normalize_name_core(product_name),
                )
            )
    return records


def pairwise(records: List[SourceRecord]):
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            yield records[i], records[j]


def add_edge(edges: List[dict], a: SourceRecord, b: SourceRecord, method: str, score: int) -> None:
    similarity = names_similarity(a, b)
    edges.append(
        {
            "source_id_a": a.source_id,
            "source_id_b": b.source_id,
            "store_a": a.store_name,
            "store_b": b.store_name,
            "method": method,
            "score": score,
            "name_similarity": similarity,
            "package_relation": package_relation(a, b),
            "barcode_a": a.barcode,
            "barcode_b": b.barcode,
            "barcode_norm_a": a.barcode_norm,
            "barcode_norm_b": b.barcode_norm,
            "unit_a": f"{a.unit_step or ''} {a.unit_type}".strip(),
            "unit_b": f"{b.unit_step or ''} {b.unit_type}".strip(),
            "product_name_a": a.product_name,
            "product_name_b": b.product_name,
            "image_key_a": a.image_key,
            "image_key_b": b.image_key,
        }
    )


def build_edges(records: List[SourceRecord]) -> List[dict]:
    edges: List[dict] = []

    by_barcode = defaultdict(list)
    by_image = defaultdict(list)
    by_name = defaultdict(list)
    by_core = defaultdict(list)

    for record in records:
        if record.barcode_norm:
            by_barcode[record.barcode_norm].append(record)
        if record.image_key:
            by_image[record.image_key].append(record)
        if record.name_key:
            by_name[record.name_key].append(record)
        if record.name_core and len(record.name_core) >= 12:
            by_core[record.name_core].append(record)

    for group in by_barcode.values():
        if len(group) < 2:
            continue
        for a, b in pairwise(group):
            add_edge(edges, a, b, "same_barcode", 100)

    for group in by_image.values():
        if len(group) < 2:
            continue
        for a, b in pairwise(group):
            if a.store_name == b.store_name:
                continue
            if names_similarity(a, b) >= 0.72:
                add_edge(edges, a, b, "same_image_key", 95)

    for group in by_name.values():
        if len(group) < 2:
            continue
        for a, b in pairwise(group):
            if a.store_name != b.store_name:
                add_edge(edges, a, b, "same_exact_name", 88)

    for group in by_core.values():
        if len(group) < 2 or len(group) > 50:
            continue
        for a, b in pairwise(group):
            if a.store_name == b.store_name:
                continue
            relation = package_relation(a, b)
            if relation not in {"same", "close"}:
                continue
            if names_similarity(a, b) >= 0.86:
                add_edge(edges, a, b, "same_name_core_compatible_pack", 80)

    return edges


def group_records(records: List[SourceRecord], edges: List[dict]) -> Dict[str, List[SourceRecord]]:
    by_id = {record.source_id: record for record in records}
    union_find = UnionFind(by_id.keys())
    for edge in edges:
        union_find.union(edge["source_id_a"], edge["source_id_b"])

    groups = defaultdict(list)
    for record in records:
        groups[union_find.find(record.source_id)].append(record)
    return dict(groups)


def choose_canonical_name(records: List[SourceRecord]) -> str:
    counts = Counter(record.product_name for record in records if record.product_name)
    if not counts:
        return ""
    return sorted(counts.items(), key=lambda item: (-item[1], len(item[0]), item[0]))[0][0]


def sorted_unique(values: Iterable[str]) -> List[str]:
    return sorted({clean_text(value) for value in values if clean_text(value)})


def group_review_reasons(records: List[SourceRecord], methods: List[str]) -> List[str]:
    reasons = []
    barcode_norms = sorted_unique(record.barcode_norm for record in records)
    if len(barcode_norms) > 1:
        reasons.append("több_normalizált_vonalkód")

    store_counts = Counter(record.store_name for record in records)
    if any(count > 1 for count in store_counts.values()):
        reasons.append("több_ajánlat_azonos_boltból")

    name_keys = sorted_unique(record.name_key for record in records)
    if len(name_keys) >= 4:
        reasons.append("sok_névváltozat")

    unit_groups = defaultdict(list)
    for record in records:
        if record.unit_type and record.unit_step is not None and record.unit_step > 0:
            unit_groups[record.unit_type].append(record.unit_step)
    if len(unit_groups) > 1:
        reasons.append("eltérő_kiszerelési_egység")
    for unit_type, steps in unit_groups.items():
        if len(steps) < 2:
            continue
        smaller = min(steps)
        larger = max(steps)
        if smaller > 0 and larger / smaller > 1.25:
            reasons.append(f"eltérő_kiszerelés_{unit_type}")
            break

    if "same_image_key" in methods and len(barcode_norms) > 1:
        reasons.append("azonos_kép_eltérő_vonalkód")

    return reasons


def write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_outputs(records: List[SourceRecord], groups: Dict[str, List[SourceRecord]], edges: List[dict]):
    methods_by_root = defaultdict(set)
    roots_by_source = {}
    temp_union = UnionFind([record.source_id for record in records])
    for edge in edges:
        temp_union.union(edge["source_id_a"], edge["source_id_b"])
    for record in records:
        roots_by_source[record.source_id] = temp_union.find(record.source_id)
    for edge in edges:
        root = roots_by_source[edge["source_id_a"]]
        methods_by_root[root].add(edge["method"])

    master_rows = []
    offer_rows = []
    review_rows = []

    sorted_groups = sorted(groups.items(), key=lambda item: (choose_canonical_name(item[1]).casefold(), item[0]))
    for index, (root, group_records_list) in enumerate(sorted_groups, start=1):
        master_product_id = f"MP{index:06d}"
        canonical_name = choose_canonical_name(group_records_list)
        methods = sorted(methods_by_root.get(root, []))
        review_reasons = group_review_reasons(group_records_list, methods)
        barcodes = sorted_unique(record.barcode for record in group_records_list)
        barcode_norms = sorted_unique(record.barcode_norm for record in group_records_list)
        image_keys = sorted_unique(record.image_key for record in group_records_list)
        stores = sorted_unique(record.store_name for record in group_records_list)
        representative_image_url = first_image_url(next((record.image_urls for record in group_records_list if record.image_urls), ""))

        master_row = {
            "master_product_id": master_product_id,
            "canonical_name": canonical_name,
            "representative_name": canonical_name,
            "primary_barcode": barcode_norms[0] if barcode_norms else "",
            "barcodes": ";".join(barcodes),
            "barcode_norms": ";".join(barcode_norms),
            "representative_image_url": representative_image_url,
            "image_keys": ";".join(image_keys),
            "stores_count": len(stores),
            "stores": ";".join(stores),
            "offers_count": len(group_records_list),
            "match_methods": ";".join(methods),
            "needs_review": "true" if review_reasons else "false",
            "review_reason": ";".join(review_reasons),
        }
        master_rows.append(master_row)

        if review_reasons:
            review_rows.append(
                {
                    **master_row,
                    "offer_names": " | ".join(record.product_name for record in group_records_list),
                    "offer_units": " | ".join(f"{record.store_name}: {record.unit_step or ''} {record.unit_type}".strip() for record in group_records_list),
                }
            )

        for record in sorted(group_records_list, key=lambda item: (item.store_name, item.product_name, item.store_product_id)):
            offer_rows.append(
                {
                    "master_product_id": master_product_id,
                    "store_name": record.store_name,
                    "store_product_id": record.store_product_id,
                    "product_name": record.product_name,
                    "brand_name": record.brand_name,
                    "barcode": record.barcode,
                    "barcode_norm": record.barcode_norm,
                    "unit_price": record.unit_price if record.unit_price is not None else "",
                    "unit_type": record.unit_type,
                    "unit_step": record.unit_step if record.unit_step is not None else "",
                    "base_price": record.base_price if record.base_price is not None else "",
                    "base_unit": record.base_unit,
                    "available": record.available,
                    "is_discounted": record.is_discounted,
                    "original_unit_price": record.original_unit_price,
                    "image_urls": record.image_urls,
                    "image_key": record.image_key,
                    "categories": record.categories,
                    "name_key": record.name_key,
                    "name_core": record.name_core,
                }
            )

    return master_rows, offer_rows, review_rows


def write_summary(path: Path, inputs: Dict[str, Path], records: List[SourceRecord], master_rows: List[dict], review_rows: List[dict], edges: List[dict]) -> None:
    store_counts = Counter(record.store_name for record in records)
    method_counts = Counter(edge["method"] for edge in edges)
    review_reason_counts = Counter()
    for row in review_rows:
        for reason in row["review_reason"].split(";"):
            if reason:
                review_reason_counts[reason] += 1

    lines = [
        "# Mestertermék riport",
        "",
        "## Bemeneti fájlok",
        "",
    ]
    for store, input_path in inputs.items():
        lines.append(f"- {store}: `{input_path.name}`")
    lines.extend(
        [
            "",
            "## Összkép",
            "",
            f"- Forrássorok száma: {len(records)}",
            f"- Mestertermékek száma: {len(master_rows)}",
            f"- Ellenőrzést igénylő mestertermékek: {len(review_rows)}",
            f"- Párosító élek száma: {len(edges)}",
            "",
            "## Bolti sorok",
            "",
        ]
    )
    for store, count in sorted(store_counts.items()):
        lines.append(f"- {store}: {count}")

    lines.extend(["", "## Párosítási módszerek", ""])
    for method, count in sorted(method_counts.items()):
        lines.append(f"- {method}: {count}")

    lines.extend(["", "## Ellenőrzési okok", ""])
    if review_reason_counts:
        for reason, count in sorted(review_reason_counts.items()):
            lines.append(f"- {reason}: {count}")
    else:
        lines.append("- Nincs ellenőrzést igénylő csoport.")

    lines.extend(
        [
            "",
            "## Kimeneti fájlok",
            "",
            "- `master_products.csv`",
            "- `master_offers.csv`",
            "- `match_edges.csv`",
            "- `review_candidates.csv`",
            "",
            "## Megjegyzés",
            "",
            "Ez determinisztikus első verzió. A `review_candidates.csv` lista nem hibajegyzék, hanem azoknak a termékcsoportoknak a sora, ahol a vonalkód, név, kép vagy kiszerelés alapján további ellenőrzés indokolt.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(description="Mestertermék- és bolti ajánlat táblák építése normalizált bolti CSV-kből.")
    parser.add_argument("--data-dir", default=str(DEFAULT_DATA_DIR), help="A normalizált bolti CSV-k mappája.")
    parser.add_argument("--reports-dir", default=str(DEFAULT_REPORTS_DIR), help="Riport kimeneti mappa.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d_%H%M%S"), help="Kimeneti riport időbélyege.")
    return parser.parse_args()


def main():
    args = parse_args()
    data_dir = Path(args.data_dir)
    reports_dir = Path(args.reports_dir)
    output_dir = reports_dir / f"master_products_{args.timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    inputs = {
        store_name: latest_normalized_file(data_dir, prefix)
        for store_name, prefix in STORE_PREFIXES.items()
    }

    records: List[SourceRecord] = []
    for store_name, path in inputs.items():
        records.extend(read_store_file(path, store_name))

    edges = build_edges(records)
    groups = group_records(records, edges)
    master_rows, offer_rows, review_rows = build_outputs(records, groups, edges)

    master_fields = [
        "master_product_id",
        "canonical_name",
        "representative_name",
        "primary_barcode",
        "barcodes",
        "barcode_norms",
        "representative_image_url",
        "image_keys",
        "stores_count",
        "stores",
        "offers_count",
        "match_methods",
        "needs_review",
        "review_reason",
    ]
    offer_fields = [
        "master_product_id",
        "store_name",
        "store_product_id",
        "product_name",
        "brand_name",
        "barcode",
        "barcode_norm",
        "unit_price",
        "unit_type",
        "unit_step",
        "base_price",
        "base_unit",
        "available",
        "is_discounted",
        "original_unit_price",
        "image_urls",
        "image_key",
        "categories",
        "name_key",
        "name_core",
    ]
    edge_fields = [
        "source_id_a",
        "source_id_b",
        "store_a",
        "store_b",
        "method",
        "score",
        "name_similarity",
        "package_relation",
        "barcode_a",
        "barcode_b",
        "barcode_norm_a",
        "barcode_norm_b",
        "unit_a",
        "unit_b",
        "product_name_a",
        "product_name_b",
        "image_key_a",
        "image_key_b",
    ]
    review_fields = master_fields + ["offer_names", "offer_units"]

    write_csv(output_dir / "master_products.csv", master_rows, master_fields)
    write_csv(output_dir / "master_offers.csv", offer_rows, offer_fields)
    write_csv(output_dir / "match_edges.csv", edges, edge_fields)
    write_csv(output_dir / "review_candidates.csv", review_rows, review_fields)
    write_summary(output_dir / "summary.md", inputs, records, master_rows, review_rows, edges)

    print(f"Kimenet: {output_dir}")
    print(f"Forrássorok: {len(records)}")
    print(f"Mestertermékek: {len(master_rows)}")
    print(f"Ellenőrzést igénylő csoportok: {len(review_rows)}")


if __name__ == "__main__":
    main()
