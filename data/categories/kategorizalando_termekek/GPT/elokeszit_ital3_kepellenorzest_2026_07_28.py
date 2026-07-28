# -*- coding: utf-8 -*-
"""5x5-ös címkeellenőrző rácsok az ital_eszrevetelek3 feldolgozásához.

A program kizárólag a rendszer ideiglenes könyvtárába ír. A kategóriafát és
az eredmeny.json fájlt nem módosítja.
"""

from __future__ import annotations

import csv
import json
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[3]
RESULT_PATH = BASE / "eredmeny.json"
CSV_PATH = BASE / "kategorizalatlan_termekek.csv"
OUT = Path(tempfile.gettempdir()) / "codex_ital3_20260728"

GRID = 5
CELL_W = 420
IMAGE_H = 370
LABEL_H = 100
PAD = 8


def load_font(size: int) -> ImageFont.ImageFont:
    for font_name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def csv_indexes() -> tuple[dict[str, list[dict[str, str]]], dict[str, list[dict[str, str]]]]:
    by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    with CSV_PATH.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            by_id[row.get("store_product_id", "")].append(row)
            by_name[row.get("product_name", "").casefold()].append(row)
    return by_id, by_name


def source_row(
    termek: dict[str, Any],
    by_id: dict[str, list[dict[str, str]]],
    by_name: dict[str, list[dict[str, str]]],
) -> dict[str, str] | None:
    product_id = str(termek.get("store_product_id") or "")
    matches = by_id.get(product_id, [])
    exact = [row for row in matches if row.get("product_name") == termek.get("product_name")]
    if len(exact) == 1:
        return exact[0]
    if len(matches) == 1:
        return matches[0]
    by_exact_name = by_name.get(str(termek.get("product_name") or "").casefold(), [])
    return by_exact_name[0] if len(by_exact_name) == 1 else None


def first_existing_image(*raw_paths: Any) -> str | None:
    for raw in raw_paths:
        values = raw if isinstance(raw, list) else str(raw or "").split(";")
        for value in values:
            path = Path(str(value).strip())
            if not str(path):
                continue
            for candidate in (path, REPO / path, BASE / path):
                if candidate.is_file():
                    return str(candidate.resolve())
    return None


def missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def candidate_groups(products: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_id, by_name = csv_indexes()
    groups: dict[str, list[dict[str, Any]]] = {
        "hianyzo_alkoholtartalom": [],
        "hianyzo_marka": [],
        "hianyzo_kiszereles": [],
    }

    for product_index, product in enumerate(products):
        if product.get("fokategoria") != "Ital":
            continue
        properties = product.get("tulajdonsagok") or {}
        if properties.get("alkoholstátusz") != "alkoholos":
            continue
        termek = product.get("termek") or {}
        row = source_row(termek, by_id, by_name)
        image_path = first_existing_image(
            termek.get("local_image_paths"),
            row.get("local_image_paths") if row else None,
        )
        if not image_path:
            continue

        item = {
            "product_index": product_index,
            "store_name": termek.get("store_name") or (row.get("store_name") if row else None),
            "store_product_id": termek.get("store_product_id"),
            "product_name": termek.get("product_name"),
            "current_path": [
                product.get("fokategoria"),
                product.get("alkategoria"),
                product.get("altipus"),
            ],
            "image_path": image_path,
            "properties": properties,
        }
        if missing(properties.get("alkoholtartalom")):
            groups["hianyzo_alkoholtartalom"].append(item)
        if missing(properties.get("márka")):
            groups["hianyzo_marka"].append(item)
        if missing(properties.get("kiszerelés")):
            groups["hianyzo_kiszereles"].append(item)

    return groups


def fit_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    width: int,
    font: ImageFont.ImageFont,
    max_lines: int,
) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines[:max_lines]


def make_sheets(group_name: str, items: list[dict[str, Any]]) -> list[str]:
    group_dir = OUT / group_name
    group_dir.mkdir(parents=True, exist_ok=True)
    font = load_font(17)
    small_font = load_font(15)
    paths: list[str] = []
    per_sheet = GRID * GRID

    for sheet_no, start in enumerate(range(0, len(items), per_sheet), start=1):
        sheet_items = items[start : start + per_sheet]
        width = GRID * CELL_W + (GRID + 1) * PAD
        height = GRID * (IMAGE_H + LABEL_H) + (GRID + 1) * PAD
        sheet = Image.new("RGB", (width, height), "#eeeeee")
        draw = ImageDraw.Draw(sheet)

        for offset, item in enumerate(sheet_items):
            col = offset % GRID
            row = offset // GRID
            x = PAD + col * (CELL_W + PAD)
            y = PAD + row * (IMAGE_H + LABEL_H + PAD)
            draw.rectangle(
                (x, y, x + CELL_W, y + IMAGE_H + LABEL_H),
                fill="white",
                outline="#777777",
            )
            try:
                with Image.open(item["image_path"]) as raw:
                    image = raw.convert("RGB")
                    image.thumbnail((CELL_W - 12, IMAGE_H - 12))
                    px = x + (CELL_W - image.width) // 2
                    py = y + (IMAGE_H - image.height) // 2
                    sheet.paste(image, (px, py))
            except OSError:
                draw.text((x + 8, y + 8), "[kép olvasási hiba]", fill="#aa0000", font=font)

            ordinal = start + offset + 1
            header = (
                f"{ordinal:03d} | idx={item['product_index']} | "
                f"{item['current_path'][2]}"
            )
            draw.text((x + 6, y + IMAGE_H + 3), header, fill="#111111", font=font)
            name = str(item.get("product_name") or "")
            for line_no, line in enumerate(
                fit_text(draw, name, CELL_W - 12, small_font, max_lines=3)
            ):
                draw.text(
                    (x + 6, y + IMAGE_H + 27 + line_no * 19),
                    line,
                    fill="#333333",
                    font=small_font,
                )

        path = group_dir / f"{group_name}_{sheet_no:02d}.jpg"
        sheet.save(path, quality=92)
        paths.append(str(path.resolve()))
    return paths


def main() -> None:
    products = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    groups = candidate_groups(products)
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {}
    for group_name, items in groups.items():
        manifest_path = OUT / f"{group_name}.json"
        manifest_path.write_text(
            json.dumps(items, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        summary[group_name] = {
            "products": len(items),
            "manifest": str(manifest_path.resolve()),
            "sheets": make_sheets(group_name, items),
        }
    summary_path = OUT / "osszefoglalo.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(summary_path.resolve())
    for group_name, details in summary.items():
        print(f"{group_name}: {details['products']} termék, {len(details['sheets'])} rács")


if __name__ == "__main__":
    main()
