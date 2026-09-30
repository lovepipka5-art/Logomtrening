#!/usr/bin/env python3
import math
import os
import sys

sys.path.insert(0, "skills/logo-design/scripts")
import render_png

OUT_DIR = "designs/m-trening/evo"
os.makedirs(OUT_DIR, exist_ok=True)

from build_evo_v4 import fmt, dist, unit, pt, build_panel_with_arcs, build_tall_ship_v4
from build_evo_v3 import build_single_contour_wordmark, arc_band, tapered_orbit_arc

def build_ball_dome_v5(cx=110.0, cy=186.0, R=102.0, mode="classic"):
    def on_circle(deg):
        return pt(cx, cy, R, deg)

    panels = []
    # 1. Large Left-Center Hexagon:
    p1 = [
        (94, 108),   # top
        (126, 128),  # upper-right
        (116, 166),  # lower-right
        (68, 184),   # bottom
        (42, 150),   # lower-left
        (54, 120),   # upper-left
    ]
    panels.append(build_panel_with_arcs(p1, set(), r_corner=7.0, cx=cx, cy=cy, R=R))

    # 2. Large Right-Center Hexagon (shifted slightly left on its right edge so p8 has generous thickness!):
    p2 = [
        (138, 130),  # upper-left
        (168, 122),  # top-right
        (190, 154),  # middle-right
        (182, 190),  # bottom-right on horizon
        (136, 190),  # bottom-left on horizon
        (128, 168),  # middle-left
    ]
    panels.append(build_panel_with_arcs(p2, set(), r_corner=7.0, cx=cx, cy=cy, R=R))

    # 3. Top-Left Rim Panel (generous thickness, parallel to p1's upper-left edge):
    p3 = [
        on_circle(217),  # (28.5, 124.6)
        on_circle(260),  # (92.3, 85.5)
        (88, 97),
        (64, 105),
        (42, 117),
    ]
    panels.append(build_panel_with_arcs(p3, {0}, r_corner=4.5, cx=cx, cy=cy, R=R))

    # 4. Top-Right Pentagon/Hexagon Rim Panel:
    p4 = [
        on_circle(267),
        on_circle(306),
        (162, 111),
        (132, 118),
        (104, 97),
    ]
    panels.append(build_panel_with_arcs(p4, {0}, r_corner=5.5, cx=cx, cy=cy, R=R))

    # 5. Far-Left Middle Rim Panel:
    p5 = [
        on_circle(191),
        on_circle(211),
        (38, 126),
        (29, 152),
    ]
    panels.append(build_panel_with_arcs(p5, {0}, r_corner=4.5, cx=cx, cy=cy, R=R))

    # 6. Bottom-Left Horizon Rim Panel:
    p6 = [
        (8.1, 190),
        on_circle(185),
        (32, 162),
        (54, 190),
    ]
    panels.append(build_panel_with_arcs(p6, {0}, r_corner=4.5, cx=cx, cy=cy, R=R))

    # 7. Bottom-Center Horizon Wedge:
    p7 = [
        (84, 190),
        (118, 177),
        (124, 190),
    ]
    panels.append(build_panel_with_arcs(p7, set(), r_corner=3.5, cx=cx, cy=cy, R=R))

    # 8. Far-Right Upper Rim Panel (generous 10-unit thickness so it never looks like a thin scratch!):
    p8 = [
        on_circle(312),  # (178.3, 110.2)
        on_circle(344),  # (208.0, 157.9)
        (199, 148),
        (188, 131),
        (177, 116),
    ]
    panels.append(build_panel_with_arcs(p8, {0}, r_corner=4.0, cx=cx, cy=cy, R=R))

    # 9. Far-Right Lower Horizon Panel (generous wedge at bottom right):
    p9 = [
        on_circle(349),
        (211.9, 190),
        (194, 190),
        (202, 163),
    ]
    panels.append(build_panel_with_arcs(p9, {0}, r_corner=3.0, cx=cx, cy=cy, R=R))

    return panels

wm_main, wm_p = build_single_contour_wordmark(y_top=204.0, h=36.0, sw=5.6)

orb_uniform = [
    arc_band(114, 184, 122, 130, 214, 276),
    arc_band(114, 184, 122, 130, 326, 363),
]
orb_swoosh = [
    tapered_orbit_arc(114, 184, 126, 212, 277, 3.0, 9.5, 5.0),
    tapered_orbit_arc(114, 184, 126, 325, 363, 9.0, 7.5, 3.5),
]
orb_aero = [
    tapered_orbit_arc(114, 184, 126, 208, 282, 2.5, 10.0, 6.0),
    tapered_orbit_arc(114, 184, 126, 324, 363, 8.5, 7.0, 2.5),
]

for code, title, orb, ship_style in [
    ("evo-a", "М-ТРЕНИНГ — Вариант A (Ювелирный ремастеринг оригинала)", orb_uniform, "classic"),
    ("evo-b", "М-ТРЕНИНГ — Вариант B (Парус-М на орбите)", orb_swoosh, "sail_m"),
    ("evo-c", "М-ТРЕНИНГ — Вариант C (Скоростной Аэро-Поток)", orb_aero, "wave_flow"),
]:
    ball = build_ball_dome_v5(cx=110.0, cy=186.0, R=102.0)
    ship_solids, hull_eo = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style=ship_style)
    path_tags_w = [f'    <path fill="#FFFFFF" d="{p}"/>' for p in (ball + orb + ship_solids)]
    if hull_eo:
        path_tags_w.append(f'    <path fill="#FFFFFF" fill-rule="evenodd" d="{hull_eo}"/>')

    svg_dark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <g id="symbol">
{chr(10).join(path_tags_w)}
  </g>
  <g id="wordmark">
    <path fill="#FFFFFF" d="{wm_main}"/>
    <path fill="#FFFFFF" fill-rule="evenodd" d="{wm_p}"/>
  </g>
</svg>
'''
    p_dark = os.path.join(OUT_DIR, f"{code}-v5-dark.svg")
    with open(p_dark, "w", encoding="utf-8") as f:
        f.write(svg_dark)
    render_png.render(p_dark, os.path.join(OUT_DIR, f"{code}-v5-dark.png"), 512, 512, bg="#05070A")

print("Built v5 evolutionary marks")
