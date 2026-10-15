"""Locate enclosed near-white regions (blank bubbles, labels, badges).

Usage:
  python tools/detect_regions.py panel.png [more.png ...]
  python tools/detect_regions.py panel.png --json

Prints boxes in original-image pixels: x0 y0 x1 y1 width height fill%.
Exit code 0 even when no region is found; the caller must notice an empty list.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque

from PIL import Image

try:
    import numpy as np
except ImportError:  # pragma: no cover
    np = None


def analyze(path: str, white_threshold: int = 238, min_cells: int = 25, sample: int = 256):
    im = Image.open(path).convert("L")
    w, h = im.size
    scale = max(w, h) / float(sample)
    dw = max(1, int(round(w / scale)))
    dh = max(1, int(round(h / scale)))
    small = im.resize((dw, dh), Image.BILINEAR)
    if np is not None:
        white = np.asarray(small) > white_threshold
    else:
        white = [[small.getpixel((x, y)) > white_threshold for x in range(dw)] for y in range(dh)]

    def is_white(y, x):
        return bool(white[y][x] if np is None else white[y, x])

    seen = [[False] * dw for _ in range(dh)] if np is None else np.zeros((dh, dw), dtype=bool)
    comps = []
    for y in range(dh):
        for x in range(dw):
            if not is_white(y, x) or seen[y][x]:
                continue
            q = deque([(y, x)])
            seen[y][x] = True
            pts = []
            touches = False
            while q:
                cy, cx = q.popleft()
                pts.append((cy, cx))
                if cy == 0 or cx == 0 or cy == dh - 1 or cx == dw - 1:
                    touches = True
                for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                    if 0 <= ny < dh and 0 <= nx < dw and is_white(ny, nx) and not seen[ny][nx]:
                        seen[ny][nx] = True
                        q.append((ny, nx))
            comps.append((pts, touches))

    out = []
    for pts, touches in comps:
        if touches or len(pts) < min_cells:
            continue
        ys = [p[0] for p in pts]
        xs = [p[1] for p in pts]
        x0 = int(min(xs) * scale)
        y0 = int(min(ys) * scale)
        x1 = int(min(w, round((max(xs) + 1) * scale)))
        y1 = int(min(h, round((max(ys) + 1) * scale)))
        box_area = max(1, (x1 - x0) * (y1 - y0))
        fill = len(pts) * (scale * scale) / box_area
        out.append({
            "box": [x0, y0, x1, y1],
            "width": x1 - x0,
            "height": y1 - y0,
            "fill": round(fill, 3),
        })
    out.sort(key=lambda b: (b["box"][1], b["box"][0]))
    return {"path": path, "size": [w, h], "regions": out}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("images", nargs="+")
    p.add_argument("--json", action="store_true")
    p.add_argument("--white", type=int, default=238)
    p.add_argument("--min-cells", type=int, default=25)
    args = p.parse_args(argv)
    reports = [analyze(path, args.white, args.min_cells) for path in args.images]
    if args.json:
        json.dump(reports if len(reports) > 1 else reports[0], sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return 0
    for rep in reports:
        print(f"--- {rep['path']} {rep['size'][0]}x{rep['size'][1]} ---")
        if not rep["regions"]:
            print("   (no enclosed white region)")
        for i, b in enumerate(rep["regions"]):
            x0, y0, x1, y1 = b["box"]
            print(f"   [{i}] x{x0:4d} y{y0:4d} -> x{x1:4d} y{y1:4d}  w{b['width']:4d} h{b['height']:4d}  fill {b['fill']:.0%}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
