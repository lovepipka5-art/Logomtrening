#!/usr/bin/env python3
"""Полный логотип-комплект М-ТРЕНИНГ на концепте E «ПАНЕЛЬ» (раунд 2).

Знак: футбольный мяч, у которого центральная панель заменена вырубленной «М»;
пять швов мяча на месте. Палитра школы: Blue #1B44D8 (основной),
Deep #0A1633, Volt #D8F74E (акцент на тёмном и на синем), White.

Пишет в nova/kit/: мастер-SVG, exports/*.png (1024/1600/иконки/favicon.ico),
site.webmanifest, head-snippet.html, brand-guidelines.md,
application-board.svg/png.
"""
import math
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nova_lib as nl  # noqa: E402

KIT = os.path.join(HERE, "kit")
EXP = os.path.join(KIT, "exports")
os.makedirs(EXP, exist_ok=True)

STYLE = "pulse"
SYM = nl.symbol_panel()
SYM_SMALL = nl.symbol_panel(seam_w=0.0001)  # заглушка, ниже пересоберём


def symbol_small():
    """Упрощённый знак для 16-32 px: мяч + вырубная М, без швов."""
    cx = cy = 128.0
    r = 104.0
    m = nl.solid_m(cx - 59, 84, 172, 118, 25, apex_flat=0.09)
    body = nl.dif(nl.circle(cx, cy, r), m)
    return {
        "shapes": [(nl.to_d(body), "main")],
        "bbox": (24, 24, 232, 232),
        "baseline": 232,
        "name": "ПАНЕЛЬ",
        "letter": "E",
        "idea": "",
    }


SMALL = symbol_small()

PAL_COLOR = {"main": nl.BLUE, "accent": nl.VOLT, "wm": nl.BLUE}
PAL_ONDARK = {"main": nl.WHITE, "accent": nl.VOLT, "wm": nl.WHITE}
PAL_MONO_W = {"main": nl.WHITE, "accent": nl.WHITE, "wm": nl.WHITE}
PAL_MONO_B = {"main": nl.BLUE, "accent": nl.BLUE, "wm": nl.BLUE}
PAL_MONO_D = {"main": nl.DEEP, "accent": nl.DEEP, "wm": nl.DEEP}


def write_svg(name, svg):
    with open(os.path.join(KIT, name), "w", encoding="utf-8") as f:
        f.write(svg + "\n")


def png(svg, w, h, name, bg=None):
    nl.render(svg, w, h, os.path.join(EXP, name), bg=bg)


def ico(sizes, names):
    """ICO с PNG-вставками (16/32/48)."""
    blobs = []
    for s, n in zip(sizes, names):
        with open(os.path.join(EXP, n), "rb") as f:
            blobs.append((s, f.read()))
    n = len(blobs)
    head = struct.pack("<HHH", 0, 1, n)
    entries = b""
    offset = 6 + 16 * n
    body = b""
    for s, data in blobs:
        w = 0 if s >= 256 else s
        entries += struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
        body += data
    with open(os.path.join(EXP, "favicon.ico"), "wb") as f:
        f.write(head + entries + body)


def main():
    # ---------------- мастер-SVG
    write_svg("logo-symbol-color.svg", nl.svg_symbol(SYM, PAL_COLOR, "М-ТРЕНИНГ — знак (мяч-панель М)"))
    write_svg("logo-symbol-on-dark.svg", nl.svg_symbol(SYM, PAL_ONDARK, "М-ТРЕНИНГ — знак для тёмного фона"))
    write_svg("logo-symbol-mono-white.svg", nl.svg_symbol(SYM, PAL_MONO_W, "М-ТРЕНИНГ — знак монохром белый"))
    write_svg("logo-symbol-mono-blue.svg", nl.svg_symbol(SYM, PAL_MONO_B, "М-ТРЕНИНГ — знак монохром синий"))
    write_svg("logo-symbol-mono-deep.svg", nl.svg_symbol(SYM, PAL_MONO_D, "М-ТРЕНИНГ — знак монохром тёмный"))
    write_svg("logo-symbol-small-mono-white.svg", nl.svg_symbol(SMALL, PAL_MONO_W, "М-ТРЕНИНГ — знак для мелких размеров"))
    write_svg("logo-symbol-small-mono-blue.svg", nl.svg_symbol(SMALL, PAL_MONO_B, "М-ТРЕНИНГ — знак для мелких размеров"))
    write_svg("logo-horizontal.svg", nl.svg_from_layout(nl.lockup_h(SYM, STYLE), PAL_COLOR, "М-ТРЕНИНГ"))
    write_svg("logo-horizontal-on-dark.svg", nl.svg_from_layout(nl.lockup_h(SYM, STYLE), PAL_ONDARK, "М-ТРЕНИНГ"))
    write_svg("logo-stacked.svg", nl.svg_from_layout(nl.lockup_v(SYM, STYLE), PAL_COLOR, "М-ТРЕНИНГ"))
    write_svg("logo-stacked-on-dark.svg", nl.svg_from_layout(nl.lockup_v(SYM, STYLE), PAL_ONDARK, "М-ТРЕНИНГ"))
    d, w, wb = nl.wordmark("М-ТРЕНИНГ", STYLE)
    lay = {"vb": (wb[0] - 4, wb[1] - 4, (wb[2] - wb[0]) + 8, (wb[3] - wb[1]) + 8),
           "groups": [("translate(0 0)", [(d, "wm")])]}
    write_svg("logo-wordmark.svg", nl.svg_from_layout(lay, PAL_MONO_B, "М-ТРЕНИНГ — леттеринг"))

    # ---------------- PNG
    png(nl.svg_symbol(SYM, PAL_COLOR), 1024, 1024, "symbol-color-transparent-1024.png")
    png(nl.svg_symbol(SYM, PAL_ONDARK), 1024, 1024, "symbol-on-blue-1024.png", bg=nl.BLUE)
    png(nl.svg_symbol(SYM, PAL_ONDARK), 1024, 1024, "symbol-on-deep-1024.png", bg=nl.DEEP)
    png(nl.svg_symbol(SYM, PAL_COLOR), 1024, 1024, "symbol-on-white-1024.png", bg=nl.WHITE)
    png(nl.svg_symbol(SYM, PAL_MONO_W), 1024, 1024, "symbol-mono-white-transparent-1024.png")
    png(nl.svg_symbol(SYM, PAL_MONO_B), 1024, 1024, "symbol-mono-blue-transparent-1024.png")
    lh = nl.lockup_h(SYM, STYLE)
    vb = lh["vb"]
    png(nl.svg_from_layout(lh, PAL_COLOR), int(vb[2] * 1.5625), 400,
        "horizontal-color-transparent-1600.png")
    png(nl.svg_from_layout(lh, PAL_ONDARK), int(vb[2] * 1.5625), 400,
        "horizontal-on-dark-transparent-1600.png")
    png(nl.svg_from_layout(lh, PAL_COLOR), int(vb[2] * 1.5625), 400,
        "horizontal-on-blue-1600.png", bg=nl.BLUE)
    lv = nl.lockup_v(SYM, STYLE)
    vbv = lv["vb"]
    png(nl.svg_from_layout(lv, PAL_COLOR), 1024, int(1024 * vbv[3] / vbv[2]),
        "stacked-color-transparent-1024w.png")

    # иконки / favicon
    png(nl.svg_symbol(SMALL, PAL_MONO_W), 16, 16, "favicon-16.png", bg=None)
    png(nl.svg_symbol(SMALL, PAL_MONO_W), 32, 32, "favicon-32.png")
    png(nl.svg_symbol(SMALL, PAL_MONO_W), 48, 48, "favicon-48.png")
    ico([16, 32, 48], ["favicon-16.png", "favicon-32.png", "favicon-48.png"])
    png(nl.svg_symbol(SYM, PAL_COLOR), 180, 180, "apple-touch-icon.png", bg=nl.WHITE)
    png(nl.svg_symbol(SYM, PAL_ONDARK), 192, 192, "icon-192.png", bg=nl.DEEP)
    png(nl.svg_symbol(SYM, PAL_ONDARK), 512, 512, "icon-512.png", bg=nl.DEEP)
    mask = nl.svg_symbol(SYM, PAL_ONDARK)
    mask = mask.replace('viewBox="0 0 256 256"', 'viewBox="-26 -26 308 308"')
    png(mask, 512, 512, "maskable-512.png", bg=nl.BLUE)
    png(nl.svg_symbol(SMALL, PAL_MONO_W), 64, 64, "glyph-64.png")

    with open(os.path.join(EXP, "site.webmanifest"), "w", encoding="utf-8") as f:
        f.write('''{
  "name": "М-ТРЕНИНГ — футбольная школа силового тренинга",
  "short_name": "М-ТРЕНИНГ",
  "icons": [
    {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ],
  "theme_color": "#0A1633",
  "background_color": "#0A1633",
  "display": "standalone"
}
''')
    with open(os.path.join(EXP, "head-snippet.html"), "w", encoding="utf-8") as f:
        f.write('''<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/logo-symbol-color.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0A1633">
''')
    print("kit ok")


if __name__ == "__main__":
    main()
