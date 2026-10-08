#!/usr/bin/env python3
"""Планшет применения логотипа М-ТРЕНИНГ (раунд 3, герб).

Шесть сцен: шеврон на груди формы, принт на спине, печать на мяче и диске
штанги, аватары, favicon и вкладка браузера, шапка сайта и документов.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nova_lib as nl  # noqa: E402

KIT = os.path.join(HERE, "kit")
MUTED = "#9FB0D8"
PANEL = "#12214D"

STYLE = "varsity"
SYM = nl.symbol_lion_mascot()
SYM_MONO = nl.symbol_lion_mono()
SYM_MONO_NT = SYM_MONO
EMB = nl.symbol_comic_crest()
EMB_MONO = nl.symbol_gem_shield_mono()
SMALL = nl.symbol_gem_small()

PAL_LIGHT = dict(nl.PAL_FULL)
PAL_BLUE = dict(nl.PAL_FULL, wm=nl.WHITE)
PAL_DEEP = dict(nl.PAL_FULL, wm=nl.WHITE, wmo=nl.BLUE)
PAL_MW = {"main": nl.WHITE}
PAL_MB = {"main": nl.BLUE}

TEE = ("M140 44 C158 26 178 20 200 20 C222 20 242 26 260 44 L356 100 L312 170 "
       "L286 152 L286 396 L114 396 L114 152 L88 170 L44 100 Z")


def embed(svg_str, x, y, w, h):
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
              'font-weight="bold" fill="#FFFFFF">М-ТРЕНИНГ «ЛЕВ» — применение</text>')
    el.append('<text x="60" y="138" font-family="DejaVu Sans" font-size="26" '
              f'fill="{MUTED}">Футбольная школа силового тренинга · основной цвет '
              'комикс-маскот: лев с гранёным мячом в зубах, контур и сел-шейдинг; эмблема — комикс-герб</text>')

    TW, TH, G = 740, 620, 40
    x0, y0 = 60, 190

    # 1 — шеврон на груди
    x, y = x0, y0
    el += tile(x, y, TW, TH, "Форма: шеврон на груди", "65-75 мм, монохром белым")
    el.append(f'<g transform="translate({x+170} {y+60})"><path d="{TEE}" fill="{nl.BLUE}"/></g>')
    el.append(embed(nl.svg_symbol(SYM_MONO_NT, PAL_MW), x + 292, y + 158, 116, 116))
    el.append(f'<text x="{x+200}" y="{y+440}" font-family="DejaVu Sans" font-size="22" '
              f'fill="{MUTED}">джерси домашняя, Blue</text>')

    # 2 — принт на спине
    x = x0 + TW + G
    el += tile(x, y, TW, TH, "Форма: принт на спине", "200-240 мм, полный знак")
    el.append(embed(nl.svg_symbol(SYM, PAL_DEEP), x + 190, y + 60, 360, 360))

    # 3 — мяч и инвентарь
    x = x0 + 2 * (TW + G)
    el += tile(x, y, TW, TH, "Мяч, гири, диски штанги", "монохром в 1 цвет")
    el.append(f'<circle cx="{x+210}" cy="{y+230}" r="150" fill="#FFFFFF"/>')
    el.append(embed(nl.svg_symbol(SYM_MONO, PAL_MB), x + 105, y + 125, 210, 210))
    el.append(f'<circle cx="{x+530}" cy="{y+240}" r="120" fill="{nl.DEEP}" '
              f'stroke="#2A3B6E" stroke-width="12"/>')
    el.append(embed(nl.svg_symbol(SYM_MONO, PAL_MW), x + 450, y + 160, 160, 160))

    y = y0 + TH + G
    # 4 — аватары
    x = x0
    el += tile(x, y, TW, TH, "Аватары и соцсети", "эмблема «Комикс-герб» для аватаров")
    el.append(f'<rect x="{x+70}" y="{y+70}" width="280" height="280" rx="64" fill="{nl.DEEP}"/>')
    el.append(embed(nl.svg_symbol(EMB, PAL_DEEP), x + 100, y + 100, 220, 220))
    el.append(f'<circle cx="{x+540}" cy="{y+210}" r="140" fill="{nl.BLUE}"/>')
    el.append(embed(nl.svg_symbol(EMB, PAL_BLUE), x + 430, y + 100, 220, 220))

    # 5 — favicon и вкладка
    x = x0 + TW + G
    el += tile(x, y, TW, TH, "Favicon и вкладка браузера", "16-48 px: гранёный мяч")
    el.append(f'<rect x="{x+60}" y="{y+90}" width="{TW-120}" height="120" rx="18" fill="#E8ECF6"/>')
    el.append(f'<rect x="{x+80}" y="{y+110}" width="360" height="80" rx="14" fill="#FFFFFF"/>')
    el.append(f'<g transform="translate({x+96} {y+126}) scale(0.1875)">'
              f'<path fill="{nl.BLUE}" d="{SMALL["shapes"][0][0]}"/></g>')
    el.append(f'<text x="{x+140}" y="{y+162}" font-family="DejaVu Sans" font-size="26" '
              f'fill="#26314F">М-ТРЕНИНГ — футбольная школа</text>')
    el.append(f'<rect x="{x+60}" y="{y+230}" width="{TW-120}" height="70" rx="14" fill="#FFFFFF"/>')
    el.append(f'<text x="{x+84}" y="{y+275}" font-family="DejaVu Sans" font-size="24" '
              f'fill="#8A94B0">m-trening.ru</text>')
    el.append(embed(nl.svg_symbol(SMALL, PAL_MB), x + 90, y + 350, 64, 64))
    el.append(embed(nl.svg_symbol(SMALL, PAL_MW), x + 170, y + 350, 64, 64))
    el.append(f'<text x="{x+260}" y="{y+395}" font-family="DejaVu Sans" font-size="21" '
              f'fill="{MUTED}">16, 32, 48 px — упрощённый знак</text>')

    # 6 — сайт и документы
    x = x0 + 2 * (TW + G)
    el += tile(x, y, TW, TH, "Сайт, презентации, документы", "горизонтальная компоновка")
    el.append(f'<rect x="{x+50}" y="{y+70}" width="{TW-100}" height="170" rx="20" fill="#FFFFFF"/>')
    lay = nl.lockup_h(SYM, STYLE, comic=True)
    vb = lay["vb"]
    el.append(embed(nl.svg_from_layout(lay, PAL_LIGHT), x + 80, y + 95,
                    520, 520 * vb[3] / vb[2]))
    el.append(f'<rect x="{x+50}" y="{y+270}" width="{TW-100}" height="170" rx="20" fill="{nl.BLUE}"/>')
    el.append(embed(nl.svg_from_layout(lay, PAL_BLUE), x + 80, y + 295,
                    520, 520 * vb[3] / vb[2]))

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'width="{W}" height="{H}">' + "".join(el) + "</svg>")
    with open(os.path.join(KIT, "application-board.svg"), "w", encoding="utf-8") as f:
        f.write(svg)
    nl.render(svg, W, H, os.path.join(KIT, "application-board.png"))
    print("apply board ok")


if __name__ == "__main__":
    main()
