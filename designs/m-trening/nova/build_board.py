#!/usr/bin/env python3
"""Планшет трёх концепций нового знака М-ТРЕНИНГ (Nova).

Собирает concepts-board.svg / concepts-board.png: по карточке на концепцию
(знак на тёмном и светлом, горизонтальная компоновка, лестница размеров,
леттеринг), палитра и рекомендация внизу.
"""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nova_lib as nl  # noqa: E402

OUT = HERE
GRAPHITE = "#0A1633"
PANEL = "#12214D"
MUTED = "#9FB0D8"

PAL_ONBLUE = {"main": nl.WHITE, "accent": nl.VOLT, "wm": nl.WHITE}
PAL_DARK = {"main": nl.WHITE, "accent": nl.VOLT, "wm": nl.WHITE}
LIGHT_ACCENT = {"goal": nl.DEEP, "panel": nl.VOLT, "ballbase": nl.DEEP,
                "regata": nl.DEEP, "sailpanel": nl.DEEP}
PAL_LIGHT = {"main": nl.BLUE, "accent": nl.DEEP, "wm": nl.BLUE}
def pal_light(key):
    return {"main": nl.BLUE, "accent": LIGHT_ACCENT[key], "wm": nl.BLUE}
PAL_MONO = {"main": nl.WHITE, "accent": nl.WHITE, "wm": nl.WHITE}


def strip(svg_str):
    s = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", svg_str, flags=re.I)
    m = re.search(r"<svg\b[^>]*>", s)
    tag = m.group(0)
    vb = re.search(r'viewBox="([^"]+)"', tag).group(1)
    inner = s[m.end():s.rindex("</svg>")]
    return vb, inner


def embed(svg_str, x, y, w, h):
    vb, inner = strip(svg_str)
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}" '
            f'preserveAspectRatio="xMidYMid meet">{inner}</svg>')


def wrap(text, limit):
    words, lines, line = text.split(), [], ""
    for w in words:
        if len(line) + len(w) + 1 > limit and line:
            lines.append(line)
            line = ""
        line = (line + " " + w).strip()
    if line:
        lines.append(line)
    return lines


def board(concepts, recommend):
    CW = 800
    GAP = 40
    n = len(concepts)
    W = n * CW + (n + 1) * GAP
    H = 1500
    el = [f'<rect width="{W}" height="{H}" fill="{GRAPHITE}"/>']
    el.append('<text x="%d" y="86" font-family="DejaVu Sans" font-size="52" '
              'font-weight="bold" fill="#FFFFFF">М-ТРЕНИНГ — раунд 4: '
              'эволюция исходного знака</text>' % GAP)
    el.append('<text x="%d" y="132" font-family="DejaVu Sans" font-size="26" '
              'fill="%s">ДНК старого знака — мяч, парусник, орбита — собрана заново: '
              'ровная мачта, чистые панели, одна орбита-волна.</text>' % (GAP, MUTED))

    for i, (key, sym, style) in enumerate(concepts):
        cx = GAP + i * (CW + GAP)
        y = 180
        # --- шапка карточки
        el.append(f'<text x="{cx}" y="{y+40}" font-family="DejaVu Sans" '
                  f'font-size="40" font-weight="bold" fill="{nl.VOLT}">'
                  f'{sym["letter"]}</text>')
        el.append(f'<text x="{cx+44}" y="{y+40}" font-family="DejaVu Sans" '
                  f'font-size="40" font-weight="bold" fill="#FFFFFF">'
                  f'«{sym["name"]}»</text>')
        for j, line in enumerate(wrap(sym["idea"], 60)):
            el.append(f'<text x="{cx}" y="{y+84+j*34}" font-family="DejaVu Sans" '
                      f'font-size="24" fill="{MUTED}">{line}</text>')
        y += 176
        # --- два тайла: тёмный и светлый
        tw = (CW - 24) / 2
        el.append(f'<rect x="{cx}" y="{y}" width="{tw}" height="{tw}" rx="28" '
                  f'fill="{nl.BLUE}"/>')
        el.append(embed(nl.svg_symbol(sym, PAL_ONBLUE), cx + 24, y + 24,
                        tw - 48, tw - 48))
        el.append(f'<rect x="{cx+tw+24}" y="{y}" width="{tw}" height="{tw}" '
                  f'rx="28" fill="#FFFFFF"/>')
        el.append(embed(nl.svg_symbol(sym, pal_light(key)), cx + tw + 48, y + 24,
                        tw - 48, tw - 48))
        y += tw + 28
        # --- горизонтальная компоновка на тёмном
        lay = nl.lockup_h(sym, style)
        lh = 210
        el.append(f'<rect x="{cx}" y="{y}" width="{CW}" height="{lh}" rx="24" '
                  f'fill="{PANEL}"/>')
        el.append(embed(nl.svg_from_layout(lay, PAL_DARK), cx + 30, y + 25,
                        CW - 60, lh - 50))
        y += lh + 24
        # --- лестница размеров (монохром на тёмном)
        lad = 150
        el.append(f'<rect x="{cx}" y="{y}" width="{CW}" height="{lad}" rx="24" '
                  f'fill="{PANEL}"/>')
        px = cx + 60
        for size in (104, 64, 40, 24, 16):
            el.append(embed(nl.svg_symbol(sym, PAL_MONO), px, y + (lad - size) / 2 - 4,
                            size, size))
            el.append(f'<text x="{px+size/2}" y="{y+lad-14}" text-anchor="middle" '
                      f'font-family="DejaVu Sans" font-size="17" fill="{MUTED}">'
                      f'{size}</text>')
            px += size + 46
        el.append(f'<text x="{cx+CW-30}" y="{y+34}" text-anchor="end" '
                  f'font-family="DejaVu Sans" font-size="19" fill="{MUTED}">'
                  f'тест масштаба, 1 цвет</text>')
        y += lad + 24
        # --- леттеринг на светлом
        wmh = 110
        el.append(f'<rect x="{cx}" y="{y}" width="{CW}" height="{wmh}" rx="24" '
                  f'fill="#FFFFFF"/>')
        d, w, wb = nl.wordmark("М-ТРЕНИНГ", style)
        lay = {"vb": (wb[0] - 6, wb[1] - 8, (wb[2] - wb[0]) + 12, (wb[3] - wb[1]) + 16),
               "groups": [("translate(0 0)", [(d, "wm")])]}
        el.append(embed(nl.svg_from_layout(lay, pal_light(key)), cx + 40, y + 20,
                        CW - 80, wmh - 40))
        y += wmh
        if key == recommend:
            el.append(f'<rect x="{cx+CW-190}" y="{180+8}" width="190" height="46" '
                      f'rx="23" fill="{nl.VOLT}"/>')
            el.append(f'<text x="{cx+CW-95}" y="{180+39}" text-anchor="middle" '
                      f'font-family="DejaVu Sans" font-size="23" font-weight="bold" '
                      f'fill="{GRAPHITE}">рекомендуем</text>')

    # --- палитра
    y = H - 150
    el.append(f'<text x="{GAP}" y="{y}" font-family="DejaVu Sans" font-size="26" '
              f'font-weight="bold" fill="#FFFFFF">Новая палитра</text>')
    chips = [("Blue", nl.BLUE), ("Deep", nl.DEEP), ("Volt", nl.VOLT),
             ("White", nl.WHITE)]
    x = GAP
    for name, col in chips:
        el.append(f'<rect x="{x}" y="{y+22}" width="150" height="70" rx="16" '
                  f'fill="{col}" stroke="#2A3238" stroke-width="1"/>')
        el.append(f'<text x="{x+16}" y="{y+116}" font-family="DejaVu Sans" '
                  f'font-size="20" fill="{MUTED}">{name} {col}</text>')
        x += 170
    el.append(f'<text x="{x+40}" y="{y+52}" font-family="DejaVu Sans" '
              f'font-size="22" fill="{MUTED}">Blue — основной цвет школы; Volt — '
              f'акцент на тёмном и на синем, на белом знак монохромный.</text>')
    el.append(f'<text x="{x+40}" y="{y+86}" font-family="DejaVu Sans" '
              f'font-size="22" fill="{MUTED}">Все контуры — вектор без растров и градиентов.</text>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">' + "".join(el) + "</svg>")


def main():
    concepts = [("regata", nl.symbol_regata(), "penta"),
                ("sailpanel", nl.symbol_sailpanel(), "penta")]
    svg = board(concepts, "regata")
    with open(os.path.join(OUT, "concepts-board.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    nl.render(svg, 2680, 1500, os.path.join(OUT, "concepts-board.png"))
    print("board ok")


if __name__ == "__main__":
    main()
