#!/usr/bin/env python3
"""Полный логотип-комплект М-ТРЕНИНГ, раунд 6: «ГОРИЗОНТ» + новый леттеринг varsity.

Система:
  * «ГОРИЗОНТ» (M) — основной знак: мяч над ватерлинией, яхта рядом, дуга орбиты;
    парусник с ровной мачтой; компоновки с леттерингом «М-ТРЕНИНГ»;
  * «ПАНЕЛЬ-ПАРУС» (K) — эмблема для аватаров, app-icon, соцсетей;
  * мяч с вырубным парусом — упрощённый знак 16-48 px (favicon);
  * леттеринг «М-ТРЕНИНГ» — единственный текст системы.

Палитра: Blue #1B44D8, Deep #0A1633, Volt #D8F74E, White.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nova_lib as nl  # noqa: E402

KIT = os.path.join(HERE, "kit")
EXP = os.path.join(KIT, "exports")
os.makedirs(EXP, exist_ok=True)

STYLE = "varsity"
SYM = nl.symbol_lion_mascot()
SYM_MONO = nl.symbol_lion_mono()
EMB = nl.symbol_comic_crest()
EMB_MONO = nl.symbol_gem_shield_mono()
SMALL = nl.symbol_gem_small()

PAL_LIGHT = dict(nl.PAL_FULL)
PAL_BLUE = dict(nl.PAL_FULL, wm=nl.WHITE)
PAL_DEEP = dict(nl.PAL_FULL, wm=nl.WHITE, wmo=nl.BLUE)
PAL_MW = {"main": nl.WHITE, "accent": nl.WHITE, "wm": nl.WHITE}
PAL_MB = {"main": nl.BLUE, "accent": nl.BLUE, "wm": nl.BLUE}
PAL_MD = {"main": nl.DEEP, "accent": nl.DEEP, "wm": nl.DEEP}


def write_svg(name, svg):
    with open(os.path.join(KIT, name), "w", encoding="utf-8") as f:
        f.write(svg + "\n")


def png(svg, w, h, name, bg=None):
    nl.render(svg, w, h, os.path.join(EXP, name), bg=bg)


def ico(sizes, names):
    blobs = []
    for s, n in zip(sizes, names):
        with open(os.path.join(EXP, n), "rb") as f:
            blobs.append((s, f.read()))
    n = len(blobs)
    head = struct.pack("<HHH", 0, 1, n)
    entries, offset, body = b"", 6 + 16 * n, b""
    for s, data in blobs:
        w = 0 if s >= 256 else s
        entries += struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
        body += data
    with open(os.path.join(EXP, "favicon.ico"), "wb") as f:
        f.write(head + entries + body)


def main():
    write_svg("logo-symbol.svg", nl.svg_symbol(SYM, PAL_LIGHT, "М-ТРЕНИНГ — знак «Кристалл»"))
    write_svg("logo-symbol-on-blue.svg", nl.svg_symbol(SYM, PAL_BLUE, "М-ТРЕНИНГ — знак на синем"))
    write_svg("logo-symbol-on-dark.svg", nl.svg_symbol(SYM, PAL_DEEP, "М-ТРЕНИНГ — знак на тёмном"))
    write_svg("logo-symbol-mono-white.svg", nl.svg_symbol(SYM_MONO, PAL_MW, "М-ТРЕНИНГ — знак монохром белый"))
    write_svg("logo-symbol-mono-blue.svg", nl.svg_symbol(SYM_MONO, PAL_MB, "М-ТРЕНИНГ — знак монохром синий"))
    write_svg("logo-symbol-mono-deep.svg", nl.svg_symbol(SYM_MONO, PAL_MD, "М-ТРЕНИНГ — знак монохром тёмный"))
    write_svg("logo-emblem.svg", nl.svg_symbol(EMB, PAL_LIGHT, "М-ТРЕНИНГ — эмблема «Панель-парус»"))
    write_svg("logo-emblem-on-dark.svg", nl.svg_symbol(EMB, PAL_DEEP, "М-ТРЕНИНГ — эмблема на тёмном"))
    write_svg("logo-emblem-mono-white.svg", nl.svg_symbol(EMB_MONO, PAL_MW, "М-ТРЕНИНГ — эмблема монохром"))
    write_svg("logo-symbol-small.svg", nl.svg_symbol(SMALL, PAL_MB, "М-ТРЕНИНГ — знак 16-48 px"))
    write_svg("logo-symbol-small-mono-white.svg", nl.svg_symbol(SMALL, PAL_MW, "М-ТРЕНИНГ — знак 16-48 px"))
    write_svg("logo-horizontal.svg", nl.svg_from_layout(nl.lockup_h(SYM, STYLE, comic=True), PAL_LIGHT, "М-ТРЕНИНГ"))
    write_svg("logo-horizontal-on-blue.svg", nl.svg_from_layout(nl.lockup_h(SYM, STYLE, comic=True), PAL_BLUE, "М-ТРЕНИНГ"))
    write_svg("logo-horizontal-on-dark.svg", nl.svg_from_layout(nl.lockup_h(SYM, STYLE, comic=True), PAL_DEEP, "М-ТРЕНИНГ"))
    write_svg("logo-stacked.svg", nl.svg_from_layout(nl.lockup_v(SYM, STYLE, comic=True), PAL_LIGHT, "М-ТРЕНИНГ"))
    write_svg("logo-stacked-on-dark.svg", nl.svg_from_layout(nl.lockup_v(SYM, STYLE, comic=True), PAL_DEEP, "М-ТРЕНИНГ"))
    d, w, wb = nl.wordmark("М-ТРЕНИНГ", STYLE)
    lay = {"vb": (wb[0] - 4, wb[1] - 4, (wb[2] - wb[0]) + 8, (wb[3] - wb[1]) + 8),
           "groups": [("translate(0 0)", [(d, "wm")])]}
    write_svg("logo-wordmark.svg", nl.svg_from_layout(lay, PAL_MB, "М-ТРЕНИНГ — леттеринг"))

    png(nl.svg_symbol(SYM, PAL_LIGHT), 1024, 1024, "symbol-on-white-1024.png", bg=nl.WHITE)
    png(nl.svg_symbol(SYM, PAL_BLUE), 1024, 1024, "symbol-on-blue-1024.png", bg=nl.BLUE)
    png(nl.svg_symbol(SYM, PAL_DEEP), 1024, 1024, "symbol-on-deep-1024.png", bg=nl.DEEP)
    png(nl.svg_symbol(SYM, PAL_LIGHT), 1024, 1024, "symbol-transparent-1024.png")
    png(nl.svg_symbol(SYM_MONO, PAL_MW), 1024, 1024, "symbol-mono-white-transparent-1024.png")
    png(nl.svg_symbol(SYM_MONO, PAL_MB), 1024, 1024, "symbol-mono-blue-transparent-1024.png")
    png(nl.svg_symbol(EMB, PAL_LIGHT), 512, 512, "emblem-on-white-512.png", bg=nl.WHITE)
    png(nl.svg_symbol(EMB, PAL_DEEP), 512, 512, "emblem-on-deep-512.png", bg=nl.DEEP)
    lh = nl.lockup_h(SYM, STYLE, comic=True)
    vb = lh["vb"]
    png(nl.svg_from_layout(lh, PAL_LIGHT), int(vb[2] * 1.5625), 400,
        "horizontal-on-white-1600.png", bg=nl.WHITE)
    png(nl.svg_from_layout(lh, PAL_BLUE), int(vb[2] * 1.5625), 400,
        "horizontal-on-blue-1600.png", bg=nl.BLUE)
    png(nl.svg_from_layout(lh, PAL_DEEP), int(vb[2] * 1.5625), 400,
        "horizontal-on-deep-1600.png", bg=nl.DEEP)
    lv = nl.lockup_v(SYM, STYLE, comic=True)
    vbv = lv["vb"]
    png(nl.svg_from_layout(lv, PAL_LIGHT), 1024, int(1024 * vbv[3] / vbv[2]),
        "stacked-on-white-1024w.png", bg=nl.WHITE)

    png(nl.svg_symbol(SMALL, PAL_MB), 16, 16, "favicon-16.png")
    png(nl.svg_symbol(SMALL, PAL_MB), 32, 32, "favicon-32.png")
    png(nl.svg_symbol(SMALL, PAL_MB), 48, 48, "favicon-48.png")
    ico([16, 32, 48], ["favicon-16.png", "favicon-32.png", "favicon-48.png"])
    png(nl.svg_symbol(EMB, PAL_LIGHT), 180, 180, "apple-touch-icon.png", bg=nl.WHITE)
    png(nl.svg_symbol(EMB, PAL_DEEP), 192, 192, "icon-192.png", bg=nl.DEEP)
    png(nl.svg_symbol(EMB, PAL_DEEP), 512, 512, "icon-512.png", bg=nl.DEEP)
    mask = nl.svg_symbol(EMB, PAL_BLUE).replace('viewBox="0 0 256 256"',
                                                'viewBox="-26 -26 308 308"')
    png(mask, 512, 512, "maskable-512.png", bg=nl.BLUE)
    png(nl.svg_symbol(SMALL, PAL_MB), 64, 64, "glyph-64.png")

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
<link rel="icon" href="/logo-symbol.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#0A1633">
''')
    print("kit ok")


if __name__ == "__main__":
    main()
