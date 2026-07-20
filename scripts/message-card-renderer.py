#!/usr/bin/env python3
"""Render message-bridge command replies as one palserver GUI styled image."""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import re
import sys
import types
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

# pil-utils eagerly imports BuildImage (and therefore OpenCV/Numpy) from its
# package __init__. This renderer only needs Text2Image, so load that submodule
# through a lightweight package shell. Release builds stay much smaller.
pil_utils_spec = importlib.util.find_spec("pil_utils")
if not pil_utils_spec or not pil_utils_spec.submodule_search_locations:
    raise RuntimeError("pil-utils is not installed")
pil_utils_package = types.ModuleType("pil_utils")
pil_utils_package.__path__ = list(pil_utils_spec.submodule_search_locations)
pil_utils_package.__package__ = "pil_utils"
pil_utils_package.__spec__ = pil_utils_spec
sys.modules["pil_utils"] = pil_utils_package
from pil_utils.text2image import Text2Image  # noqa: E402


BG = "#232030"
CARD = "#2d2a3b"
CARD_SOFT = "#363347"
INK = "#eceaf2"
MUTED = "#a9a5bb"
PAL = "#5bb8ec"
PAL_STRONG = "#7ec8f0"
LINE = "#403c52"
BERRY = "#ef6a6a"
SUN = "#f2b64f"
GRASS = "#58ba64"

MAX_DIMENSION = 8000
MAX_DIMENSION_SUM = 9400
GENERIC_WIDTH = 1080
CARD_WIDTH = 420
PAL_CARD_HEIGHT = 174
ITEM_CARD_HEIGHT = 132
GRID_GAP = 16
OUTER_PADDING = 36

FONTS = {
    "zh-CN": ("PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "Noto Sans SC"),
    "zh-TW": ("PingFang TC", "Microsoft JhengHei", "Noto Sans CJK TC", "Noto Sans TC"),
    "ja": ("Hiragino Sans", "Yu Gothic", "Meiryo", "Noto Sans CJK JP", "Noto Sans JP"),
    "en": ("Nunito", "Segoe UI", "Arial"),
}


@lru_cache(maxsize=4096)
def text_image(
    text: str,
    language: str,
    size: int,
    color: str,
    bold: bool = False,
    max_width: int | None = None,
) -> Image.Image:
    rendered = Text2Image.from_text(
        text,
        size,
        font_style="bold" if bold else "normal",
        fill=color,
        font_families=list(FONTS.get(language, FONTS["zh-CN"])),
    )
    return rendered.to_image(max_width=max_width)


def paste_text(
    canvas: Image.Image,
    text: str,
    language: str,
    pos: tuple[int, int],
    *,
    size: int,
    color: str,
    bold: bool = False,
    max_width: int | None = None,
) -> Image.Image:
    image = text_image(text, language, size, color, bold, max_width)
    canvas.alpha_composite(image, pos)
    return image


def fit_platform_dimensions(image: Image.Image) -> Image.Image:
    width, height = image.size
    scale = min(1.0, MAX_DIMENSION / max(width, height), MAX_DIMENSION_SUM / (width + height))
    if scale >= 1:
        return image
    return image.resize((max(1, round(width * scale)), max(1, round(height * scale))), Image.Resampling.LANCZOS)


def rounded_image(source: Path | None, size: int) -> Image.Image:
    tile = Image.new("RGBA", (size, size), CARD_SOFT)
    if source and source.is_file():
        try:
            portrait = Image.open(source).convert("RGBA")
            portrait.thumbnail((size, size), Image.Resampling.LANCZOS)
            tile.alpha_composite(portrait, ((size - portrait.width) // 2, (size - portrait.height) // 2))
        except Exception:
            pass
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), 14, fill=255)
    tile.putalpha(mask)
    return tile


def brand_icon_path(game_data_dir: str | None) -> Path | None:
    if not game_data_dir:
        return None
    root = Path(game_data_dir)
    return next((candidate for candidate in (root.parent / "logo.png", root / "logo.png") if candidate.is_file()), None)


def paste_brand_icon(canvas: Image.Image, draw: ImageDraw.ImageDraw, source: Path | None, x: int, y: int, size: int) -> None:
    if source:
        canvas.alpha_composite(rounded_image(source, size), (x, y))
        return
    draw.rounded_rectangle((x, y, x + size, y + size), 11, fill=PAL)
    logo = text_image("P", "en", 24, "white", True)
    canvas.alpha_composite(logo, (x + (size - logo.width) // 2, y + (size - logo.height) // 2))


def draw_badge(
    canvas: Image.Image,
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    language: str,
    *,
    color: str,
    background: str = CARD_SOFT,
    size: int = 17,
) -> int:
    label = text_image(text, language, size, color, True)
    width = label.width + 20
    height = max(28, label.height + 6)
    draw.rounded_rectangle((x, y, x + width, y + height), height // 2, fill=background)
    canvas.alpha_composite(label, (x + 10, y + (height - label.height) // 2))
    return width


@dataclass
class CatalogPal:
    icon: Path | None


@dataclass
class CatalogItem:
    icon: Path | None


@dataclass
class PalRow:
    name: str
    level: int
    gender: str
    rank: int
    boss: bool
    ivs: list[tuple[str, str]]
    passives: list[str]
    section: str
    icon: Path | None


@dataclass
class ItemRow:
    name: str
    count: int
    section: str
    icon: Path | None


def normalized_name(value: str) -> str:
    return re.sub(r"[\s·・'’\-_.]+", "", value).casefold()


def load_catalog(game_data_dir: str | None) -> dict[str, CatalogPal]:
    if not game_data_dir:
        return {}
    root = Path(game_data_dir)
    try:
        records = json.loads((root / "pals.json").read_text(encoding="utf-8"))
    except Exception:
        return {}
    result: dict[str, CatalogPal] = {}
    for record in records:
        icon_name = record.get("icon")
        icon = root / "pals" / icon_name if icon_name else None
        entry = CatalogPal(icon if icon and icon.is_file() else None)
        for key in ("id", "name", "zh", "zh-CN", "zhCN", "ja"):
            value = record.get(key)
            if value:
                result[normalized_name(str(value))] = entry
    return result


def load_item_catalog(game_data_dir: str | None) -> dict[str, CatalogItem]:
    if not game_data_dir:
        return {}
    root = Path(game_data_dir)
    try:
        records = json.loads((root / "items.json").read_text(encoding="utf-8"))
    except Exception:
        return {}
    result: dict[str, CatalogItem] = {}
    for record in records:
        icon_name = record.get("icon")
        icon = root / "items" / icon_name if icon_name else None
        entry = CatalogItem(icon if icon and icon.is_file() else None)
        for key in ("id", "name", "zh", "zh-CN", "zhCN", "ja"):
            value = record.get(key)
            if value and value != "-":
                result[normalized_name(str(value))] = entry
    return result


def parse_passives(value: str) -> list[str]:
    match = re.search(r"\[([^\]]*)\]", value)
    if not match:
        return []
    content = match.group(1).strip()
    if not content or content in {"无词条", "無詞條", "No passives", "パッシブなし"}:
        return []
    return [part.strip() for part in content.split("|") if part.strip()]


def parse_ivs(value: str) -> list[tuple[str, str]]:
    match = re.search(r"IVs\(([^)]*)\)", value)
    if not match:
        return []
    result = []
    for part in match.group(1).split("|"):
        stat = re.match(r"(.+?)(\d+)$", part.strip())
        if stat:
            result.append((stat.group(1), stat.group(2)))
    return result


def catalog_icon(name: str, catalog: dict[str, CatalogPal]) -> Path | None:
    species = name.split("·")[-1].strip()
    return catalog.get(normalized_name(species), CatalogPal(None)).icon


def parse_pal_reply(text: str, catalog: dict[str, CatalogPal]) -> tuple[str, list[PalRow]] | None:
    lines = text.replace("\r", "").split("\n")
    title = next((line.strip() for line in lines if line.strip()), "Pal Collection")
    section = ""
    rows: list[PalRow] = []
    index = 0
    pattern = re.compile(r"^-\s+(.+?)\s+Lv\.(\d+)(?:\s+\(([♂♀])\))?(?:\s+-\s+(.*))?$")
    while index < len(lines):
        stripped = lines[index].strip()
        if stripped.startswith("【") and stripped.endswith("】"):
            section = stripped
            index += 1
            continue
        match = pattern.match(stripped)
        if not match:
            index += 1
            continue
        raw_name, level, gender, details = match.groups()
        rank = len(raw_name) - len(raw_name.lstrip("★"))
        boss = "(BOSS)" in raw_name.upper()
        name = raw_name.lstrip("★").replace("(BOSS)", "").strip()
        detail_text = details or ""
        passives = parse_passives(detail_text)
        if index + 1 < len(lines) and re.search(r"\[[^\]]*\]", lines[index + 1]):
            passives = parse_passives(lines[index + 1]) or passives
            index += 1
        rows.append(PalRow(
            name=name,
            level=int(level),
            gender=gender or "",
            rank=rank,
            boss=boss,
            ivs=parse_ivs(detail_text),
            passives=passives,
            section=section,
            icon=catalog_icon(name, catalog),
        ))
        index += 1
    return (title, rows) if rows else None


def parse_inventory_reply(text: str, catalog: dict[str, CatalogItem]) -> tuple[str, list[ItemRow]] | None:
    lines = text.replace("\r", "").split("\n")
    title = next((line.strip() for line in lines if line.strip()), "Inventory")
    section = ""
    rows: list[ItemRow] = []
    pattern = re.compile(r"^-\s+(.+?)\s+[×xX]\s*(\d+)$")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("【") and stripped.endswith("】"):
            section = stripped
            continue
        match = pattern.match(stripped)
        if not match:
            continue
        name, count = match.groups()
        entry = catalog.get(normalized_name(name), CatalogItem(None))
        rows.append(ItemRow(name=name, count=int(count), section=section, icon=entry.icon))
    return (title, rows) if rows else None


def pal_columns(count: int) -> int:
    return max(3, min(9, math.ceil(count / 65)))


def section_label(section: str) -> str:
    return section.strip("【】 ")


def render_pal_card(canvas: Image.Image, row: PalRow, language: str, x: int, y: int) -> None:
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((x, y, x + CARD_WIDTH, y + PAL_CARD_HEIGHT), 18, fill=CARD, outline=LINE, width=3)
    portrait = rounded_image(row.icon, 104)
    canvas.alpha_composite(portrait, (x + 16, y + 18))

    text_x = x + 136
    paste_text(canvas, row.name, language, (text_x, y + 14), size=25, color=INK, bold=True, max_width=CARD_WIDTH - 152)
    meta_y = y + 52
    level = paste_text(canvas, f"Lv.{row.level}", "en", (text_x, meta_y), size=21, color=MUTED, bold=True)
    cursor = text_x + level.width + 10
    if row.gender:
        gender_color = PAL if row.gender == "♂" else BERRY
        gender = paste_text(canvas, row.gender, "en", (cursor, meta_y - 2), size=24, color=gender_color, bold=True)
        cursor += gender.width + 10
    if row.rank:
        paste_text(canvas, "★" * row.rank, "en", (cursor, meta_y), size=20, color=SUN, bold=True)

    badge_y = y + 84
    cursor = text_x
    if row.boss:
        cursor += draw_badge(canvas, draw, cursor, badge_y, "♛ BOSS", "en", color=BERRY, background="#4b303d", size=15) + 7
    iv_icons = (("心", "♥", BERRY), ("HP", "♥", BERRY), ("攻", "⚔", SUN), ("ATK", "⚔", SUN), ("防", "◆", PAL), ("DEF", "◆", PAL), ("工速", "⚙", GRASS), ("Work", "⚙", GRASS))
    for stat, value in row.ivs:
        icon, color = next(((symbol, tone) for prefix, symbol, tone in iv_icons if stat.startswith(prefix)), ("•", MUTED))
        width = draw_badge(canvas, draw, cursor, badge_y, f"{icon} {value}", "en", color=color, size=14)
        cursor += width + 6
        if cursor > x + CARD_WIDTH - 54:
            break

    if row.passives:
        passive_text = "✦ " + " · ".join(row.passives)
        paste_text(canvas, passive_text, language, (text_x, y + 126), size=15, color=PAL_STRONG, max_width=CARD_WIDTH - 152)


def render_pal_grid(title: str, rows: list[PalRow], language: str, brand_icon: Path | None) -> Image.Image:
    columns = pal_columns(len(rows))
    width = OUTER_PADDING * 2 + columns * CARD_WIDTH + (columns - 1) * GRID_GAP
    grouped: list[tuple[str, list[PalRow]]] = []
    for row in rows:
        if not grouped or grouped[-1][0] != row.section:
            grouped.append((row.section, [row]))
        else:
            grouped[-1][1].append(row)

    header_height = 122
    title_height = 72
    section_header = 54
    height = OUTER_PADDING + header_height + title_height
    for _, entries in grouped:
        height += section_header + math.ceil(len(entries) / columns) * (PAL_CARD_HEIGHT + GRID_GAP)
    height += OUTER_PADDING

    canvas = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((OUTER_PADDING, OUTER_PADDING, width - OUTER_PADDING, OUTER_PADDING + 82), 18, fill=CARD, outline=LINE, width=3)
    paste_brand_icon(canvas, draw, brand_icon, OUTER_PADDING + 22, OUTER_PADDING + 21, 40)
    paste_text(canvas, "palserver GUI", "en", (OUTER_PADDING + 78, OUTER_PADDING + 19), size=29, color=INK, bold=True)
    paste_text(canvas, title.strip("[] "), language, (OUTER_PADDING, OUTER_PADDING + header_height), size=34, color=INK, bold=True, max_width=width - OUTER_PADDING * 2)

    y = OUTER_PADDING + header_height + title_height
    for section, entries in grouped:
        label = section_label(section) or "Pals"
        draw.rounded_rectangle((OUTER_PADDING, y, width - OUTER_PADDING, y + 38), 12, fill=CARD_SOFT)
        paste_text(canvas, f"▦  {label}", language, (OUTER_PADDING + 16, y + 4), size=22, color=PAL_STRONG, bold=True)
        y += section_header
        for index, row in enumerate(entries):
            column = index % columns
            row_index = index // columns
            x = OUTER_PADDING + column * (CARD_WIDTH + GRID_GAP)
            card_y = y + row_index * (PAL_CARD_HEIGHT + GRID_GAP)
            render_pal_card(canvas, row, language, x, card_y)
        y += math.ceil(len(entries) / columns) * (PAL_CARD_HEIGHT + GRID_GAP)
    return fit_platform_dimensions(canvas)


def render_item_card(canvas: Image.Image, row: ItemRow, language: str, x: int, y: int) -> None:
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((x, y, x + CARD_WIDTH, y + ITEM_CARD_HEIGHT), 18, fill=CARD, outline=LINE, width=3)
    canvas.alpha_composite(rounded_image(row.icon, 92), (x + 16, y + 20))
    text_x = x + 124
    paste_text(canvas, row.name, language, (text_x, y + 20), size=24, color=INK, bold=True, max_width=CARD_WIDTH - 144)
    draw_badge(canvas, draw, text_x, y + 70, f"▣  ×{row.count}", language, color=PAL_STRONG, size=17)


def render_item_grid(title: str, rows: list[ItemRow], language: str, brand_icon: Path | None) -> Image.Image:
    columns = pal_columns(len(rows))
    width = OUTER_PADDING * 2 + columns * CARD_WIDTH + (columns - 1) * GRID_GAP
    grouped: list[tuple[str, list[ItemRow]]] = []
    for row in rows:
        if not grouped or grouped[-1][0] != row.section:
            grouped.append((row.section, [row]))
        else:
            grouped[-1][1].append(row)

    header_height = 122
    title_height = 72
    section_header = 54
    height = OUTER_PADDING + header_height + title_height
    for _, entries in grouped:
        height += section_header + math.ceil(len(entries) / columns) * (ITEM_CARD_HEIGHT + GRID_GAP)
    height += OUTER_PADDING

    canvas = Image.new("RGBA", (width, height), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((OUTER_PADDING, OUTER_PADDING, width - OUTER_PADDING, OUTER_PADDING + 82), 18, fill=CARD, outline=LINE, width=3)
    paste_brand_icon(canvas, draw, brand_icon, OUTER_PADDING + 22, OUTER_PADDING + 21, 40)
    paste_text(canvas, "palserver GUI", "en", (OUTER_PADDING + 78, OUTER_PADDING + 19), size=29, color=INK, bold=True)
    paste_text(canvas, title.strip("[] "), language, (OUTER_PADDING, OUTER_PADDING + header_height), size=34, color=INK, bold=True, max_width=width - OUTER_PADDING * 2)

    y = OUTER_PADDING + header_height + title_height
    for section, entries in grouped:
        label = section_label(section) or "Items"
        draw.rounded_rectangle((OUTER_PADDING, y, width - OUTER_PADDING, y + 38), 12, fill=CARD_SOFT)
        paste_text(canvas, f"▦  {label}", language, (OUTER_PADDING + 16, y + 4), size=22, color=PAL_STRONG, bold=True)
        y += section_header
        for index, row in enumerate(entries):
            column = index % columns
            row_index = index // columns
            x = OUTER_PADDING + column * (CARD_WIDTH + GRID_GAP)
            card_y = y + row_index * (ITEM_CARD_HEIGHT + GRID_GAP)
            render_item_card(canvas, row, language, x, card_y)
        y += math.ceil(len(entries) / columns) * (ITEM_CARD_HEIGHT + GRID_GAP)
    return fit_platform_dimensions(canvas)


def generic_line_style(line: str, first: bool) -> tuple[int, str, bool, int]:
    stripped = line.strip()
    if not stripped:
        return 0, INK, False, 18
    if first:
        return 34, PAL_STRONG, True, 18
    if stripped.startswith("【") and stripped.endswith("】"):
        return 28, PAL_STRONG, True, 14
    if stripped.startswith("[") and stripped.endswith("]") and not stripped.startswith("[-]"):
        return 28, PAL_STRONG, True, 14
    return 25, INK, False, 8


def render_generic(text: str, language: str, brand_icon: Path | None) -> Image.Image:
    content_width = GENERIC_WIDTH - 156
    lines: list[tuple[Image.Image | None, int]] = []
    first = True
    for raw in text.replace("\r", "").split("\n"):
        size, color, bold, gap = generic_line_style(raw, first)
        if not raw.strip():
            lines.append((None, gap))
            continue
        lines.append((text_image(raw, language, size, color, bold, content_width), gap))
        first = False
    content_height = sum(gap if image is None else image.height + gap for image, gap in lines)
    height = 136 + content_height + 118
    canvas = Image.new("RGBA", (GENERIC_WIDTH, height), BG)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((30, 30, GENERIC_WIDTH - 30, height - 30), 18, fill=CARD, outline=LINE, width=2)
    draw.line((30, 118, GENERIC_WIDTH - 30, 118), fill=LINE, width=2)
    paste_brand_icon(canvas, draw, brand_icon, 78, 57, 36)
    paste_text(canvas, "palserver GUI", "en", (128, 54), size=27, color=INK, bold=True)
    y = 152
    for image, gap in lines:
        if image is None:
            y += gap
        else:
            canvas.alpha_composite(image, (78, y))
            y += image.height + gap
    return fit_platform_dimensions(canvas)


def render(payload: dict, output_dir: Path) -> list[str]:
    language = str(payload.get("language") or "zh-CN")
    source_pages = payload.get("pages")
    if not isinstance(source_pages, list) or not source_pages:
        raise ValueError("pages must be a non-empty list")
    text = "\n\n".join(str(page) for page in source_pages)
    game_data_dir = payload.get("gameDataDir")
    catalog = load_catalog(game_data_dir)
    item_catalog = load_item_catalog(game_data_dir)
    brand_icon = brand_icon_path(game_data_dir)
    pals = parse_pal_reply(text, catalog)
    inventory = parse_inventory_reply(text, item_catalog) if not pals else None
    if pals:
        image = render_pal_grid(pals[0], pals[1], language, brand_icon)
    elif inventory:
        image = render_item_grid(inventory[0], inventory[1], language, brand_icon)
    else:
        image = render_generic(text, language, brand_icon)

    output_dir.mkdir(parents=True, exist_ok=True)
    name = "page-001.png"
    image.convert("RGB").save(output_dir / name, "PNG", compress_level=6)
    return [name]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps({"files": render(payload, args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
