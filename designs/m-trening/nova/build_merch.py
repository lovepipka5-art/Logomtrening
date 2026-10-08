#!/usr/bin/env python3
"""Мерч-капсулы М-ТРЕНИНГ (раунд 8): стритвир-стиль и цвета по референсам.

Две капсулы:
  * «ГРАФИТ» — чёрный оверсайз, магента + белый, чёрные волны-паттерн;
  * «РОЯЛ»   — белый оверсайз, роял-синий + тёплый жёлтый Sun, дудл-паттерн
               из бренд-примитивов (пентагон, дуги-панели, штанга, вымпел).
Собирает kit/merch-board.png/svg и мерч-файлы в kit/merch/.
"""
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nova_lib as nl  # noqa: E402

OUT = HERE
KIT = os.path.join(HERE, "kit")
MERCH = os.path.join(KIT, "merch")

BLACK = "#0B0B0F"
GRAPHITE_TEE = "#101016"
WHITE_TEE = "#F7F9FC"
MUTED = "#9FB0D8"

SYM = nl.symbol_horizont()
PAL_CHEST_G = {"main": nl.WHITE, "accent": nl.MAGENTA, "wm": nl.WHITE}
PAL_CHEST_R = {"main": nl.BLUE, "accent": nl.SUN, "wm": nl.BLUE}
PAL_ART_G = {"main": nl.WHITE, "accent": nl.MAGENTA, "wm": nl.WHITE}
PAL_ART_R = {"main": nl.WHITE, "accent": nl.SUN, "wm": nl.WHITE}


# ---------------------------------------------------------------- узоры
def _sq(rnd, x, y, col, sw):
    step = rnd.randint(16, 26)
    amp = rnd.randint(8, 14)
    d = f"M {x} {y}"
    for i in range(4):
        d += f" q {step/2} {amp if i % 2 else -amp} {step} 0"
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'


def _spiral(rnd, x, y, col, sw):
    pts = []
    t = 0.0
    r = 2.0
    while t < math.pi * 5:
        pts.append((x + r * math.cos(t), y + r * math.sin(t)))
        t += 0.45
        r += 1.9
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'


def _zig(rnd, x, y, col, sw):
    step = rnd.randint(12, 18)
    dy = rnd.randint(10, 16)
    pts = [(x, y)]
    for i in range(4):
        pts.append((x + step * (i + 1), y + (dy if i % 2 == 0 else -dy)))
    d = "M " + " L ".join(f"{px} {py}" for px, py in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>'


def _ring(rnd, x, y, col, sw):
    r = rnd.randint(9, 16)
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{col}" stroke-width="{sw}"/>'


def _dot(rnd, x, y, col, sw):
    r = rnd.randint(4, 7)
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>'


def _pent(rnd, x, y, col, sw):
    r = rnd.randint(12, 18)
    pts = nl.pentagon_pts(x, y, r)
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts) + " Z"
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"/>'


def _barbell(rnd, x, y, col, sw):
    h = rnd.randint(14, 20)
    w = rnd.randint(20, 28)
    return (f'<path d="M {x-w} {y} L {x+w} {y}" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="M {x-w+4} {y-h} L {x-w+4} {y+h}" stroke="{col}" stroke-width="{sw+2}" stroke-linecap="round"/>'
            f'<path d="M {x+w-4} {y-h} L {x+w-4} {y+h}" stroke="{col}" stroke-width="{sw+2}" stroke-linecap="round"/>')


def _arc(rnd, x, y, col, sw):
    r = rnd.randint(16, 24)
    a0 = rnd.randint(0, 360)
    pts = nl.arc_pts(x, y, r, a0, a0 + 120)
    d = "M " + " L ".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'


def _pennant(rnd, x, y, col, sw):
    h = rnd.randint(16, 24)
    return f'<path d="M {x} {y-h/2} L {x+h} {y} L {x} {y+h/2} Z" fill="{col}"/>'


_MOTIFS = (_sq, _spiral, _zig, _ring, _dot, _pent, _barbell, _arc, _pennant)


def doodles(w, h, seed, cols, sw=7, n=None):
    rnd = random.Random(seed)
    n = n or int(w * h / 16000)
    el = []
    for _ in range(n):
        f = rnd.choice(_MOTIFS)
        x = rnd.randint(20, w - 20)
        y = rnd.randint(20, h - 20)
        el.append(f(rnd, x, y, rnd.choice(cols), sw))
    return "".join(el)


def star4(cx, cy, r, col):
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.32
        a = math.pi / 4 * i - math.pi / 2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return f'<path d="M ' + " L ".join(f"{p:.1f} {q:.1f}" for p, q in pts) + f' Z" fill="{col}"/>'


def waves(w, h, seed, col=BLACK, sw=9, rows=None):
    rnd = random.Random(seed)
    rows = rows or max(4, h // 90)
    el = []
    for i in range(rows):
        y = (i + 0.7) * h / (rows + 0.4)
        step = rnd.randint(46, 64)
        amp = rnd.randint(14, 24) * (1 if i % 2 else -1)
        d = f"M -20 {y}"
        x = -20
        while x < w + 20:
            d += f" q {step/2} {amp} {step} 0"
            x += step
        el.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}"/>')
    for _ in range(max(3, w // 220)):
        el.append(star4(rnd.randint(30, w - 30), rnd.randint(30, h - 30),
                        rnd.randint(14, 24), "#FFFFFF"))
    return "".join(el)


# ---------------------------------------------------------------- футболка
def tee(fill, collar):
    outer = ("M 150 38 L 230 38 L 322 56 L 374 164 L 302 200 L 292 168 "
             "L 292 442 L 88 442 L 88 168 L 78 200 L 6 164 L 58 56 Z")
    neck = ("M 152 42 A 38 13 0 1 0 228 42 A 38 13 0 1 0 152 42 Z")
    return (f'<path fill-rule="evenodd" fill="{fill}" d="{outer} {neck}"/>'
            f'<path fill="none" stroke="{collar}" stroke-width="6" '
            f'd="M 152 42 A 38 13 0 1 0 228 42 A 38 13 0 1 0 152 42"/>')


def strip(svg_str):
    s = re.sub(r"<\?xml[^>]*\?>|<!DOCTYPE[^>]*>", "", svg_str, flags=re.I)
    m = re.search(r"<svg\b[^>]*>", s)
    tag = m.group(0)
    vb = re.search(r'viewBox="([^"]+)"', tag).group(1)
    return vb, s[m.end():s.rindex("</svg>")]


def embed(svg_str, x, y, w, h):
    vb, inner = strip(svg_str)
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}" '
            f'preserveAspectRatio="xMidYMid meet">{inner}</svg>')


# ---------------------------------------------------------------- арт принта
def artwork(cap):
    """Прямоугольник принта на спину: 300x420, паттерн + знак + леттеринг."""
    if cap == "graphite":
        bg, pat = BLACK, waves(300, 330, 11, col=nl.MAGENTA)
        pal = PAL_ART_G
        wm_col = nl.WHITE
    else:
        bg = nl.BLUE
        pat = doodles(300, 330, 21, [nl.SUN, nl.WHITE, nl.SKY], sw=6, n=26)
        pal = PAL_ART_R
        wm_col = nl.WHITE
    d, w, b = nl.wordmark("М-ТРЕНИНГ", "varsity")
    ws = 190.0 / w
    sym = embed(nl.svg_symbol(SYM, pal), 75, 60, 150, 150)
    wm = (f'<g transform="translate(55 372) scale({ws:.4f})">'
          f'<path fill="{wm_col}" d="{d}"/></g>')
    stroke = nl.MAGENTA if cap == "graphite" else nl.WHITE
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 420">'
            f'<rect width="300" height="420" fill="{bg}" stroke="{stroke}" '
            f'stroke-width="3"/>'
            f'<svg x="0" y="0" width="300" height="330" viewBox="0 0 300 330">{pat}</svg>'
            f'{sym}{wm}</svg>')


def panel(cap, x, y, w, h):
    """Панель капсулы: фон с паттерном, арт слева, футболки спереди и сзади."""
    el = []
    if cap == "graphite":
        bg = nl.MAGENTA
        el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>')
        el.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" '
                  f'viewBox="0 0 {w} {h}">{waves(w, h, 5)}</svg>')
        tee_fill, collar = GRAPHITE_TEE, "#26262E"
        chest_pal = PAL_CHEST_G
        name = "КАПСУЛА «ГРАФИТ»"
        subs = ("чёрный оверсайз-футболка · Magenta #F5164E + White + Black",
                "грудь: знак 90 мм · спина: принт-пласт 240×336 мм")
    else:
        bg = nl.BLUE
        el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>')
        el.append(f'<svg x="{x}" y="{y}" width="{w}" height="{h}" '
                  f'viewBox="0 0 {w} {h}">{doodles(w, h, 9, [nl.SUN, nl.WHITE, nl.SKY], sw=8)}</svg>')
        tee_fill, collar = WHITE_TEE, "#DDE3F2"
        chest_pal = PAL_CHEST_R
        name = "КАПСУЛА «РОЯЛ»"
        subs = ("белый оверсайз-футболка · Blue #1B44D8 + Sun #FFC61A + White",
                "грудь: знак 90 мм · спина: принт-пласт 240×336 мм")
    art = artwork(cap)
    # слева — арт принта
    el.append(embed(art, x + 50, y + 70, 280, 392))
    el.append(f'<text x="{x+50}" y="{y+500}" font-family="DejaVu Sans" font-size="30" '
              f'font-weight="bold" fill="{WHITE_TEE if cap == "graphite" else nl.WHITE}">{name}</text>')
    for i, s in enumerate(subs):
        el.append(f'<text x="{x+50}" y="{y+534+i*30}" font-family="DejaVu Sans" '
                  f'font-size="20" fill="{WHITE_TEE if cap == "graphite" else nl.WHITE}">{s}</text>')
    # футболка спереди
    fx, fy = x + 390, y + 60
    el.append(f'<g transform="translate({fx} {fy})">{tee(tee_fill, collar)}'
              f'{embed(nl.svg_symbol(SYM, chest_pal), 142, 92, 96, 96)}</g>')
    # футболка сзади
    bx, by = x + 790, y + 60
    el.append(f'<g transform="translate({bx} {by})">{tee(tee_fill, collar)}'
              f'{embed(art, 105, 78, 170, 238)}</g>')
    return "".join(el)


def board():
    W, H = 1200, 1700
    el = [f'<rect width="{W}" height="{H}" fill="#0A1633"/>']
    el.append('<text x="40" y="64" font-family="DejaVu Sans" font-size="40" '
              'font-weight="bold" fill="#FFFFFF">М-ТРЕНИНГ — мерч-капсулы 2026</text>')
    el.append(f'<text x="40" y="100" font-family="DejaVu Sans" font-size="22" '
              f'fill="{MUTED}">Sun #FFC61A и Magenta #F5164E — мерч-акценты системы.</text>')
    el.append(panel("graphite", 0, 130, W, 760))
    el.append(panel("royal", 0, 910, W, 760))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
            f'width="{W}" height="{H}">' + "".join(el) + "</svg>")


def main():
    os.makedirs(MERCH, exist_ok=True)
    svg = board()
    with open(os.path.join(KIT, "merch-board.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    nl.render(svg, 1600, 2266, os.path.join(KIT, "merch-board.png"))
    # отдельные мерч-файлы
    for cap, bg, pat, seed in (("graphite", nl.MAGENTA, None, 3),
                               ("royal", nl.BLUE, "dood", 4)):
        p = (waves(600, 600, seed) if pat is None
             else doodles(600, 600, seed, [nl.SUN, nl.WHITE, nl.SKY], sw=9))
        with open(os.path.join(MERCH, f"pattern-{cap}.svg"), "w",
                  encoding="utf-8") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" '
                    f'width="600" height="600"><rect width="600" height="600" '
                    f'fill="{bg}"/>{p}</svg>')
        with open(os.path.join(MERCH, f"merch-back-{cap}.svg"), "w",
                  encoding="utf-8") as f:
            f.write(artwork(cap))
        pal = PAL_CHEST_G if cap == "graphite" else PAL_CHEST_R
        with open(os.path.join(MERCH, f"merch-chest-{cap}.svg"), "w",
                  encoding="utf-8") as f:
            f.write(nl.svg_symbol(SYM, pal, "М-ТРЕНИНГ — принт на грудь"))
    print("merch ok")


if __name__ == "__main__":
    main()
