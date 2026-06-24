from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


BASE_DIR = Path(__file__).resolve().parent
PRODUCT_PATH = BASE_DIR / "eredmeny.json"
MILK_EXPORT_PATH = BASE_DIR / "tejtermekek_munkafajlok" / "tejtermekek_termekek_2026-06-24.json"
GIT_PATH = "data/categories/kategorizalando_termekek/GPT/eredmeny.json"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def product_id(product: dict[str, Any]) -> str:
    termek = product.get("termek")
    if isinstance(termek, dict):
        return str(termek.get("store_product_id", ""))
    return ""


def load_git_head_products() -> list[dict[str, Any]]:
    raw = subprocess.check_output(["git", "show", f"HEAD:{GIT_PATH}"], cwd=BASE_DIR.parents[3])
    return json.loads(raw.decode("utf-8"))


def load_salvageable_prefix() -> list[dict[str, Any]]:
    text = PRODUCT_PATH.read_text(encoding="utf-8")
    marker = '\n  {\n    "termek"'
    pos = text.rfind(marker)
    if pos == -1:
        raise RuntimeError("Could not find the last product-object marker in the truncated file.")

    prefix = text[:pos].rstrip()
    if prefix.endswith(","):
        prefix = prefix[:-1]
    return json.loads(prefix + "\n]")


def main() -> None:
    head_products = load_git_head_products()
    partial_products = load_salvageable_prefix()
    milk_export = load_json(MILK_EXPORT_PATH)["termekek"]

    recovered = list(head_products)
    prefix_replaced = 0
    prefix_mismatches = []
    id_to_index = {product_id(product): index for index, product in enumerate(recovered) if product_id(product)}

    for index, product in enumerate(partial_products):
        if index < len(recovered) and product_id(recovered[index]) == product_id(product):
            recovered[index] = product
            prefix_replaced += 1
            continue

        fallback_index = id_to_index.get(product_id(product))
        if fallback_index is None:
            prefix_mismatches.append({"index": index, "product_id": product_id(product)})
            continue
        recovered[fallback_index] = product
        prefix_replaced += 1

    milk_replaced = 0
    for exported in milk_export:
        index = exported["_forras_index"]
        product = {key: value for key, value in exported.items() if key != "_forras_index"}
        if index >= len(recovered):
            raise RuntimeError(f"Milk export index is out of range: {index}")
        recovered[index] = product
        milk_replaced += 1

    if len(recovered) != len(head_products):
        raise RuntimeError(f"Recovered product count changed: {len(recovered)} != {len(head_products)}")

    tmp_path = PRODUCT_PATH.with_suffix(".json.recovered.tmp")
    dump_json(tmp_path, recovered)
    loaded = load_json(tmp_path)
    if len(loaded) != len(recovered):
        raise RuntimeError("Recovered temp file did not round-trip correctly.")

    tmp_path.replace(PRODUCT_PATH)

    report = {
        "head_products": len(head_products),
        "partial_products": len(partial_products),
        "prefix_replaced": prefix_replaced,
        "prefix_mismatches": prefix_mismatches[:20],
        "prefix_mismatch_count": len(prefix_mismatches),
        "milk_replaced": milk_replaced,
        "output": str(PRODUCT_PATH),
    }
    report_path = BASE_DIR / "tejtermekek_munkafajlok" / "eredmeny_recovery_2026-06-24.json"
    dump_json(report_path, report)

    print(f"head_products={len(head_products)}")
    print(f"partial_products={len(partial_products)}")
    print(f"prefix_replaced={prefix_replaced}")
    print(f"prefix_mismatch_count={len(prefix_mismatches)}")
    print(f"milk_replaced={milk_replaced}")
    print(f"report={report_path}")


if __name__ == "__main__":
    main()
