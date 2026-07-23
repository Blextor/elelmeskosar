# -*- coding: utf-8 -*-
"""Célzott képi ellenőrző csomag az Ital-javításokhoz.

A program csak munkafájlokat készít. Az eredmeny.json és a kategóriafa
tartalmát nem módosítja.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[3]
RESULT_PATH = BASE / "eredmeny.json"
CSV_PATH = BASE / "kategorizalatlan_termekek.csv"
OUT = BASE / "italok_munkafajlok" / "kepellenorzes_2026_07_16"

GRID = 5
CELL_W = 330
IMAGE_H = 300
LABEL_H = 76
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
    matches = by_id.get(str(termek.get("store_product_id") or ""), [])
    if len(matches) == 1:
        return matches[0]
    exact = [row for row in matches if row.get("product_name") == termek.get("product_name")]
    if len(exact) == 1:
        return exact[0]
    name_matches = by_name.get(str(termek.get("product_name") or "").casefold(), [])
    return name_matches[0] if len(name_matches) == 1 else None


def first_existing_image(*raw_paths: str | None) -> str | None:
    for raw in raw_paths:
        for value in str(raw or "").split(";"):
            value = value.strip()
            if not value:
                continue
            path = Path(value)
            candidates = (path, REPO / path, BASE / path)
            for candidate in candidates:
                if candidate.is_file():
                    return str(candidate.resolve())
    return None


def plant_target(alap: Any) -> str:
    values = [str(value).casefold() for value in alap] if isinstance(alap, list) else [str(alap).casefold()]
    atoms = {value for value in values if value and value != "none"}
    if len(atoms) > 1:
        return "Kevert növényi ital"
    value = next(iter(atoms), "")
    return {
        "zab": "Zabital",
        "mandula": "Mandulaital",
        "kókusz": "Kókuszital",
        "rizs": "Rizsital",
        "szója": "Szójaital",
    }.get(value, "Egyéb növényi ital")


def candidate_groups(products: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    by_id, by_name = csv_indexes()
    groups: dict[str, list[dict[str, Any]]] = {"novenyi_italok": [], "konkret_hibak": []}

    exact_fragments = (
        "koch frissen préselt",
        "karlskrone radler citromos",
        "peroni nastro azzurro 0,0% 0,5l",
        "peroni 0,0% citrom",
        "peroni 0,0% vérnarancs",
        "torres serena alkoholmentes",
        "natureo natureo muscat alkoholmentes",
        "natureo garnacha - syrah alkoholmentes",
        "celebration party szénsavas",
        "süsü vadmálna",
        "smurfy erdei gyümölcs",
        "sonic prime alma-citrom",
        "homola 100% balaton",
        "tatratea mini set",
        "tatratea tea likőr válogatás",
        "mini szeszek",
    )

    for product_index, product in enumerate(products):
        termek = product.get("termek") or {}
        row = source_row(termek, by_id, by_name)
        image_path = first_existing_image(
            termek.get("local_image_paths"),
            row.get("local_image_paths") if row else None,
        )
        item = {
            "product_index": product_index,
            "store_name": termek.get("store_name") or (row.get("store_name") if row else None),
            "store_product_id": termek.get("store_product_id"),
            "product_name": termek.get("product_name"),
            "source_categories": termek.get("categories") or (row.get("categories") if row else None),
            "source_brand": termek.get("brand_name") or (row.get("brand_name") if row else None),
            "image_path": image_path,
            "current_path": [
                product.get("fokategoria"),
                product.get("alkategoria"),
                product.get("altipus"),
            ],
            "properties": product.get("tulajdonsagok") or {},
        }

        if (
            product.get("fokategoria", "").startswith("Tejterm")
            and product.get("altipus") == "Növényi ital"
        ):
            item["proposed_altipus"] = plant_target(item["properties"].get("alap"))
            groups["novenyi_italok"].append(item)

        name_fold = str(termek.get("product_name") or "").casefold()
        props = product.get("tulajdonsagok") or {}
        if (
            any(fragment in name_fold for fragment in exact_fragments)
            or (name_fold.startswith("1664 blanc") and props.get("sörtípus") == ["alkoholmentes"])
            or (
                product.get("fokategoria") == "Ital"
                and product.get("alkategoria", "").startswith("Pezsg")
                and ("alkoholmentes" in name_fold or props.get("alkoholtartalom") in (["0,0%"], "0,0%"))
            )
        ):
            groups["konkret_hibak"].append(item)

    return groups


def fit_text(draw: ImageDraw.ImageDraw, text: str, width: int, font: ImageFont.ImageFont) -> list[str]:
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
    return lines[:2]


def make_sheets(group_name: str, items: list[dict[str, Any]]) -> list[str]:
    group_dir = OUT / group_name
    group_dir.mkdir(parents=True, exist_ok=True)
    font = load_font(16)
    small_font = load_font(14)
    sheet_paths: list[str] = []
    per_sheet = GRID * GRID

    for sheet_no, start in enumerate(range(0, len(items), per_sheet), start=1):
        sheet_items = items[start : start + per_sheet]
        width = GRID * CELL_W + (GRID + 1) * PAD
        height = GRID * (IMAGE_H + LABEL_H) + (GRID + 1) * PAD
        sheet = Image.new("RGB", (width, height), "#f3f3f3")
        draw = ImageDraw.Draw(sheet)

        for offset, item in enumerate(sheet_items):
            col = offset % GRID
            row = offset // GRID
            x = PAD + col * (CELL_W + PAD)
            y = PAD + row * (IMAGE_H + LABEL_H + PAD)
            draw.rectangle((x, y, x + CELL_W, y + IMAGE_H + LABEL_H), fill="white", outline="#999999")

            image_path = item.get("image_path")
            if image_path:
                try:
                    with Image.open(image_path) as raw:
                        image = raw.convert("RGB")
                        image.thumbnail((CELL_W - 12, IMAGE_H - 12))
                        px = x + (CELL_W - image.width) // 2
                        py = y + (IMAGE_H - image.height) // 2
                        sheet.paste(image, (px, py))
                except OSError:
                    draw.text((x + 8, y + 8), "[kép olvasási hiba]", fill="#aa0000", font=font)
            else:
                draw.text((x + 8, y + 8), "[nincs helyi kép]", fill="#aa0000", font=font)

            ordinal = start + offset + 1
            target = item.get("proposed_altipus")
            header = f"{ordinal:03d} | idx={item['product_index']}"
            if target:
                header += f" | {target}"
            draw.text((x + 6, y + IMAGE_H + 3), header, fill="#111111", font=font)
            for line_no, line in enumerate(
                fit_text(draw, str(item.get("product_name") or ""), CELL_W - 12, small_font)
            ):
                draw.text((x + 6, y + IMAGE_H + 25 + line_no * 18), line, fill="#333333", font=small_font)

        path = group_dir / f"{group_name}_{sheet_no:02d}.jpg"
        sheet.save(path, quality=90)
        sheet_paths.append(str(path.resolve()))
    return sheet_paths


def main() -> None:
    products = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
    groups = candidate_groups(products)
    OUT.mkdir(parents=True, exist_ok=True)
    summary: dict[str, Any] = {}
    for group_name, items in groups.items():
        manifest_path = OUT / f"{group_name}.json"
        manifest_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sheets = make_sheets(group_name, items)
        summary[group_name] = {
            "products": len(items),
            "with_image": sum(bool(item.get("image_path")) for item in items),
            "manifest": str(manifest_path.resolve()),
            "sheets": sheets,
        }
    (OUT / "osszefoglalo.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
