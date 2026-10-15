"""Stage 6: composite Chinese text onto blank-bubble panels and stack a strip.

layout.json
{
  "out_dir": "output",
  "width": 1080,
  "margin": 28,
  "background": [255, 255, 255],
  "fonts": {"bold": "C:/Windows/Fonts/msyhbd.ttc", "regular": "C:/Windows/Fonts/msyh.ttc"},
  "title": {"kicker": "科普漫画", "title": "标题", "subtitle": "副标题"},
  "footer": {"disclaimer": "科普仅供参考，不替代医生诊断。", "lines": ["来源：……"]},
  "panels": [
    {
      "image": "panels/p01/panel-01.png",
      "number": 1,
      "watermark": {"mode": "fade-bottom", "crop": 36, "pixels": 48, "color": [255, 255, 255]},
      "placements": [
        {"kind": "bubble", "text": "怎么会？", "box": [32, 344, 184, 492]},
        {"kind": "card", "text": "长句放这里。\n第二行不会被再拆开。", "box": [80, 760, 960, 940],
         "region": null}
      ]
    }
  ]
}

`box` is in source-image pixels (from detect_regions.py). `region` is that
script's index and is used only when `box` is omitted. Write the spoken line so a reader understands it. If it does not fit at min_size,
the script exits with an error instead of shrinking the type. Move that line to
kind=card or redraw a larger bubble.

Usage: python tools/compose.py layout.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

CLOSERS = set("，。？！、；：）】》〉」』…％%,.!?;:)]}")
FONT_CANDIDATES = {
    "bold": [
        r"C:/Windows/Fonts/msyhbd.ttc",
        r"C:/Windows/Fonts/msyh.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    ],
    "regular": [
        r"C:/Windows/Fonts/msyh.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ],
}


def resolve_font(explicit, role):
    if explicit and os.path.exists(explicit):
        return explicit
    for path in FONT_CANDIDATES[role]:
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"no CJK font for {role}; set fonts.{role} in layout.json")


def font(path, size):
    return ImageFont.truetype(path, size)


def tokenize(text):
    toks, buf = [], ""
    for ch in text:
        if ch.isalnum() or ch in ".%×":
            buf += ch
        else:
            if buf:
                toks.append(buf)
                buf = ""
            toks.append(ch)
    if buf:
        toks.append(buf)
    return toks


def wrap(text, fnt, max_w, draw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for tok in tokenize(para):
            trial = cur + tok
            if draw.textlength(trial, font=fnt) <= max_w or not cur or tok in CLOSERS:
                cur = trial
            else:
                lines.append(cur)
                cur = tok
        lines.append(cur)
    return lines


def fit_text(draw, text, box, font_path, max_size, min_size, pad=10, line_gap=8, keep_paragraphs=True):
    bw = max(1, box[2] - box[0] - pad * 2)
    bh = max(1, box[3] - box[1] - pad * 2)
    n_para = max(1, len(text.split("\n")))
    size = max_size
    while size >= min_size:
        f = font(font_path, size)
        lines = wrap(text, f, bw, draw)
        lh = size + line_gap
        total = lh * len(lines) - line_gap
        widest = max((draw.textlength(ln, font=f) for ln in lines), default=0)
        if total <= bh and widest <= bw and (not keep_paragraphs or len(lines) <= n_para):
            return lines, f, lh, total, False
        size -= 1
    f = font(font_path, min_size)
    lines = wrap(text, f, bw, draw)
    lh = min_size + line_gap
    total = lh * max(1, len(lines)) - line_gap
    widest = max((draw.textlength(ln, font=f) for ln in lines), default=0)
    overflow = total > bh or widest > bw or (keep_paragraphs and len(lines) > n_para)
    return lines, f, lh, total, overflow


def draw_block(draw, text, box, font_path, max_size, min_size, color, pad=8, line_gap=6):
    lines, f, lh, total, overflow = fit_text(draw, text, box, font_path, max_size, min_size, pad, line_gap)
    if overflow:
        raise RuntimeError(f"text does not fit at {min_size}px: {text!r}")
    y = box[1] + max(0, (box[3] - box[1] - total) // 2)
    for ln in lines:
        w = draw.textlength(ln, font=f)
        x = box[0] + max(0, (box[2] - box[0] - w) / 2)
        draw.text((x, y), ln, font=f, fill=tuple(color))
        y += lh


def draw_card(draw, text, box, font_path, max_size, min_size, color, fill, border, radius=18):
    shadow = (box[0] + 4, box[1] + 5, box[2] + 4, box[3] + 5)
    draw.rounded_rectangle(shadow, radius=radius, fill=(232, 238, 242))
    draw.rounded_rectangle(box, radius=radius, fill=tuple(fill), outline=tuple(border), width=4)
    draw_block(draw, text, box, font_path, max_size, min_size, color, pad=16, line_gap=8)


def apply_watermark(im, spec):
    if not spec or spec.get("mode") in (None, "none"):
        return im
    if spec.get("mode") != "fade-bottom":
        raise ValueError(f"unsupported watermark mode: {spec.get('mode')}")
    im = im.convert("RGB")
    crop = int(spec.get("crop", 0))
    if crop > 0:
        w, h = im.size
        im = im.crop((0, 0, w, max(1, h - crop)))
    pixels = int(spec.get("pixels", 72))
    color = tuple(spec.get("color", [255, 255, 255]))
    px = im.load()
    w, h = im.size
    start = max(0, h - pixels)
    span = max(1, h - start - 1)
    for y in range(start, h):
        t = (y - start) / span
        for x in range(w):
            r, g, b = px[x, y]
            px[x, y] = (
                int(r * (1 - t) + color[0] * t),
                int(g * (1 - t) + color[1] * t),
                int(b * (1 - t) + color[2] * t),
            )
    return im


def scale_box(box, src_size, dst_origin, scale):
    x0, y0, x1, y1 = box
    ox, oy = dst_origin
    return [
        int(ox + x0 * scale),
        int(oy + y0 * scale),
        int(ox + x1 * scale),
        int(oy + y1 * scale),
    ]


def render_panel(panel, fonts, canvas_w, margin, background):
    src = Image.open(panel["image"]).convert("RGB")
    src = apply_watermark(src, panel.get("watermark"))
    inner_w = canvas_w - margin * 2
    scale = inner_w / src.width
    dst_h = int(round(src.height * scale))
    resized = src.resize((inner_w, dst_h), Image.LANCZOS)
    canvas = Image.new("RGB", (canvas_w, dst_h), tuple(background))
    canvas.paste(resized, (margin, 0))
    draw = ImageDraw.Draw(canvas)
    regions = None
    for place in panel.get("placements", []):
        if "box" in place and place["box"]:
            box = place["box"]
        else:
            if regions is None:
                from detect_regions import analyze
                regions = analyze(panel["image"])["regions"]
            box = regions[int(place["region"])]["box"]
        mapped = scale_box(box, src.size, (margin, 0), scale)
        kind = place.get("kind", "bubble")
        text = place["text"]
        color = place.get("color", [43, 43, 43])
        if kind == "card":
            draw_card(
                draw, text, mapped, fonts["bold"],
                int(place.get("max_size", 42)), int(place.get("min_size", 24)),
                color, place.get("fill", [255, 255, 255]), place.get("border", [46, 155, 181]),
            )
        else:
            draw_block(
                draw, text, mapped, fonts["bold"],
                int(place.get("max_size", 40)), int(place.get("min_size", 32)),
                color,
            )
    number = panel.get("number")
    if number is not None:
        badge = (margin + 16, 16, margin + 78, 78)
        draw.ellipse(badge, fill=(46, 155, 181))
        f = font(fonts["bold"], 36)
        label = str(number)
        tw = draw.textlength(label, font=f)
        draw.text((margin + 47 - tw / 2, 24), label, font=f, fill=(255, 255, 255))
    return canvas


def text_width(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def build_title(spec, width, fonts, background):
    if not spec:
        return None
    height = 280
    im = Image.new("RGB", (width, height), tuple(background))
    d = ImageDraw.Draw(im)
    y = 28
    if spec.get("kicker"):
        f = font(fonts["bold"], 32)
        tw = text_width(d, spec["kicker"], f)
        d.rounded_rectangle(((width - tw) / 2 - 22, y, (width + tw) / 2 + 22, y + 52), radius=26, fill=(46, 155, 181))
        d.text(((width - tw) / 2, y + 8), spec["kicker"], font=f, fill=(255, 255, 255))
        y += 78
    if spec.get("title"):
        f = font(fonts["bold"], 72)
        tw = text_width(d, spec["title"], f)
        d.text(((width - tw) / 2, y), spec["title"], font=f, fill=(43, 43, 43))
        y += 96
    if spec.get("subtitle"):
        f = font(fonts["regular"], 32)
        tw = text_width(d, spec["subtitle"], f)
        d.text(((width - tw) / 2, y), spec["subtitle"], font=f, fill=(110, 118, 128))
    return im


def build_footer(spec, width, fonts, background):
    if not spec:
        return None
    lines = list(spec.get("lines") or [])
    height = 88 + 36 * max(1, len(lines)) + (48 if spec.get("disclaimer") else 0)
    im = Image.new("RGB", (width, height), tuple(background))
    d = ImageDraw.Draw(im)
    y = 24
    if spec.get("disclaimer"):
        d.text((36, y), spec["disclaimer"], font=font(fonts["bold"], 28), fill=(201, 74, 61))
        y += 52
    f = font(fonts["regular"], 22)
    for ln in lines:
        d.text((36, y), ln, font=f, fill=(110, 118, 128))
        y += 34
    return im


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("layout")
    args = p.parse_args(argv)
    with open(args.layout, encoding="utf-8") as f:
        layout = json.load(f)
    here = os.path.dirname(os.path.abspath(args.layout))
    os.chdir(here)
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
    fonts = {
        "bold": resolve_font((layout.get("fonts") or {}).get("bold"), "bold"),
        "regular": resolve_font((layout.get("fonts") or {}).get("regular"), "regular"),
    }
    width = int(layout.get("width", 1080))
    margin = int(layout.get("margin", 28))
    background = layout.get("background", [255, 255, 255])
    out_dir = layout.get("out_dir", "output")
    os.makedirs(out_dir, exist_ok=True)
    panels = []
    for i, panel in enumerate(layout["panels"], 1):
        rendered = render_panel(panel, fonts, width, margin, background)
        name = f"panel-{int(panel.get('number', i)):02d}-text.png"
        rendered.save(os.path.join(out_dir, name))
        panels.append(rendered)
    title = build_title(layout.get("title"), width, fonts, background)
    footer = build_footer(layout.get("footer"), width, fonts, background)
    parts = [p for p in (title, *panels, footer) if p is not None]
    total_h = sum(im.height for im in parts)
    strip = Image.new("RGB", (width, total_h), tuple(background))
    y = 0
    for im in parts:
        strip.paste(im, (0, y))
        y += im.height
    final_path = os.path.join(out_dir, "comic-final.png")
    strip.save(final_path)
    print(json.dumps({"comic": final_path, "size": list(strip.size), "panels": len(panels)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
