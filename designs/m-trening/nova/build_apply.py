#!/usr/bin/env python3
"""Планшет применения логотипа М-ТРЕНИНГ (концепт E «ПАНЕЛЬ»).

Шесть сцен: шеврон на груди формы, крупный принт на спине, печать на мяче и
диске штанги, аватары соцсетей, favicon и вкладка браузера, шапка сайта/документа.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nova_lib as nl  # noqa: E402

KIT = os.path.join(HERE, "kit")
MUTED = "#9FB0D8"
PANEL = "#12214D"

SYM = nl.symbol_panel()
SMALL_SHAPES = None
STYLE = "pulse"

PAL_W = {"main": nl.WHITE, "accent": nl.VOLT, "wm": nl.WHITE}
PAL_C = {"main": nl.BLUE, "accent": nl.VOLT, "wm": nl.BLUE}

TEE = ("M140 44 C158 26 178 20 200 20 C222 20 242 26 260 44 L356 100 L312 170 "
       "L286 152 L286 396 L114 396 L114 152 L88 170 L44 100 Z")


def sym_svg(pal):
    return nl.svg_symbol(SYM, pal)


def embed(svg_str, x, y, w, h):
    import re
    m = re.search(r"<svg\b[^>]*>", svg_str)
    tag = m.group(0)
    vb = re.search(r'viewBox="([^"]+)"', tag).group(1)
    inner = svg_str[m.end():svg_str.rindex("</svg>")]
    return (f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}" '
            f'preserveAspectRatio="xMidYMid meet">{inner}</svg>')


def tile(x, y, w, h, label, note):
    el = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="{PANEL}"/>']
    el.append(f'<text x="{x+34}" y="{y+h-58}" font-family="DejaVu Sans" font-size="27" '
              f'font-weight="bold" fill="#FFFFFF">{label}</text>')
    el.append(f'<text x="{x+34}" y="{y+h-26}" font-family="DejaVu Sans" font-size="21" '
              f'fill="{MUTED}">{note}</text>')
    return el


def main():
    W, H = 2400, 1560
    el = [f'<rect width="{W}" height="{H}" fill="{nl.DEEP}"/>']
    el.append('<text x="60" y="92" font-family="DejaVu Sans" font-size="52" '
              'font-weight="bold" fill="#FFFFFF">М-ТРЕНИНГ «ПАНЕЛЬ» — применение</text>')
    el.append('<text x="60" y="138" font-family="DejaVu Sans" font-size="26" '
              f'fill="{MUTED}">Футбольная школа силового тренинга · основной цвет '
              'Blue #1B44D8 · знак: мяч с вырубной панелью «М»</text>')

    TW, TH = 740, 620
    G = 40
    x0, y0 = 60, 190

    # 1 — шеврон на груди формы
    x, y = x0, y0
    el += tile(x, y, TW, TH, "Форма: шеврон на груди", "65-75 мм, монохром белым по синему")
    el.append(f'<g transform="translate({x+170} {y+70}) scale(1.0)">'
              f'<path d="{TEE}" fill="{nl.BLUE}"/></g>')
    el.append(embed(sym_svg(PAL_W), x + 296, y + 168, 104, 104))
    el.append(f'<text x="{x+200}" y="{y+430}" font-family="DejaVu Sans" font-size="22" '
              f'fill="{MUTED}">джерси домашняя, Blue</text>')

    # 2 — крупный принт на спине
    x = x0 + TW + G
    el += tile(x, y, TW, TH, "Форма: принт на спине", "200-240 мм, двухцветный")
    lay = nl.lockup_v(SYM, STYLE)
    vb = lay["vb"]
    el.append(embed(nl.svg_from_layout(lay, PAL_W), x + 150, y + 80, 440,
                    440 * vb[3] / vb[2]))

    # 3 — мяч и инвентарь
    x = x0 + 2 * (TW + G)
    el += tile(x, y, TW, TH, "Мяч, гири, диски штанги", "1 цвет: белый или синий")
    el.append(embed(sym_svg(PAL_C), x + 70, y + 80, 300, 300))
    el.append(f'<circle cx="{x+540}" cy="{y+230}" r="130" fill="{nl.DEEP}" '
              f'stroke="#2A3B6E" stroke-width="12"/>')
    el.append(embed(nl.svg_symbol(SYM, {"main": nl.WHITE, "accent": nl.WHITE, "wm": nl.WHITE}),
                    x + 455, y + 145, 170, 170))

    y = y0 + TH + G
    # 4 — аватары
    x = x0
    el += tile(x, y, TW, TH, "Аватары и соцсети", "квадрат и круг, Deep и Blue")
    el.append(f'<rect x="{x+70}" y="{y+70}" width="280" height="280" rx="64" fill="{nl.DEEP}"/>')
    el.append(embed(sym_svg(PAL_W), x + 110, y + 110, 200, 200))
    el.append(f'<circle cx="{x+540}" cy="{y+210}" r="140" fill="{nl.BLUE}"/>')
    el.append(embed(sym_svg(PAL_W), x + 440, y + 110, 200, 200))

    # 5 — favicon и вкладка
    x = x0 + TW + G
    el += tile(x, y, TW, TH, "Favicon и вкладка браузера", "16-32 px: версия без швов")
    el.append(f'<rect x="{x+60}" y="{y+90}" width="{TW-120}" height="120" rx="18" fill="#E8ECF6"/>')
    el.append(f'<rect x="{x+80}" y="{y+110}" width="330" height="80" rx="14" fill="#FFFFFF"/>')
    import nova_lib
    small = nl.symbol_panel(seam_w=0.0001)
    small_d = nl.to_d(nl.dif(nl.circle(128, 128, 104),
                             nl.solid_m(69, 84, 172, 118, 25, apex_flat=0.09)))
    el.append(f'<g transform="translate({x+96} {y+126}) scale(0.1875)">'
              f'<path fill="{nl.BLUE}" d="{small_d}"/></g>')
    el.append(f'<text x="{x+140}" y="{y+162}" font-family="DejaVu Sans" font-size="26" '
              f'fill="#26314F">М-ТРЕНИНГ — футбольная школа</text>')
    el.append(f'<rect x="{x+60}" y="{y+230}" width="{TW-120}" height="70" rx="14" fill="#FFFFFF"/>')
    el.append(f'<text x="{x+84}" y="{y+275}" font-family="DejaVu Sans" font-size="24" '
              f'fill="#8A94B0">m-trening.ru</text>')
    el.append(embed(nl.svg_symbol(small, {"main": nl.BLUE, "accent": nl.BLUE, "wm": nl.BLUE}),
                    x + 90, y + 350, 64, 64))
    el.append(embed(nl.svg_symbol(small, {"main": nl.WHITE, "accent": nl.WHITE, "wm": nl.WHITE}),
                    x + 170, y + 350, 64, 64))
    el.append(f'<text x="{x+260}" y="{y+395}" font-family="DejaVu Sans" font-size="21" '
              f'fill="{MUTED}">16, 32, 48 px — упрощённый знак</text>')

    # 6 — сайт и документы
    x = x0 + 2 * (TW + G)
    el += tile(x, y, TW, TH, "Сайт, презентации, документы", "горизонтальная компоновка")
    el.append(f'<rect x="{x+50}" y="{y+80}" width="{TW-100}" height="180" rx="20" fill="#FFFFFF"/>')
    lay = nl.lockup_h(SYM, STYLE)
    vb = lay["vb"]
    el.append(embed(nl.svg_from_layout(lay, PAL_C), x + 110, y + 115,
                    480, 480 * vb[3] / vb[2]))
    el.append(f'<rect x="{x+50}" y="{y+290}" width="{TW-100}" height="150" rx="20" fill="{nl.BLUE}"/>')
    el.append(embed(nl.svg_from_layout(lay, PAL_W), x + 110, y + 315,
                    480, 480 * vb[3] / vb[2]))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">' + "".join(el) + "</svg>")
    with open(os.path.join(KIT, "application-board.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    nl.render(svg, W, H, os.path.join(KIT, "application-board.png"))
    print("apply board ok")


if __name__ == "__main__":
    main()
