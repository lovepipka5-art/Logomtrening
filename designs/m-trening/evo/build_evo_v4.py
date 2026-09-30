#!/usr/bin/env python3
import math
import os
import sys

sys.path.insert(0, "skills/logo-design/scripts")
import render_png

OUT_DIR = "designs/m-trening/evo"
os.makedirs(OUT_DIR, exist_ok=True)

def fmt(v):
    return f"{round(v, 2):g}"

def dist(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

def unit(a, b):
    d = dist(a, b)
    return ((b[0] - a[0]) / d, (b[1] - a[1]) / d) if d > 1e-6 else (0.0, 0.0)

def pt(cx, cy, r, deg):
    rad = math.radians(deg)
    return (cx + r * math.cos(rad), cy + r * math.sin(rad))

def build_panel_with_arcs(vertices, arc_edges=None, r_corner=5.0, cx=110.0, cy=186.0, R=102.0):
    arc_edges = arc_edges or set()
    n = len(vertices)

    def edge_dirs(i):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % n]
        if i in arc_edges:
            r1 = unit((cx, cy), p1)
            t_start = (-r1[1], r1[0])
            r2 = unit((cx, cy), p2)
            t_end = (-r2[1], r2[0])
            ang1 = math.atan2(p1[1] - cy, p1[0] - cx)
            ang2 = math.atan2(p2[1] - cy, p2[0] - cx)
            dang = (ang2 - ang1) % (2 * math.pi)
            arc_len = R * dang
            return t_start, t_end, arc_len
        else:
            u = unit(p1, p2)
            return u, u, dist(p1, p2)

    edges = [edge_dirs(i) for i in range(n)]

    corners = []
    for i in range(n):
        p = vertices[i]
        _, t_in, len_prev = edges[(i - 1) % n]
        t_out, _, len_next = edges[i]
        u_prev = (-t_in[0], -t_in[1])
        u_next = (t_out[0], t_out[1])
        rc = min(r_corner, len_prev * 0.28, len_next * 0.28)
        if (i - 1) % n in arc_edges:
            ang_p = math.atan2(p[1] - cy, p[0] - cx)
            ang_a = ang_p - (rc / R)
            a = (cx + R * math.cos(ang_a), cy + R * math.sin(ang_a))
            ra = unit((cx, cy), a)
            ta = (-ra[1], ra[0])
            u_prev_a = (-ta[0], -ta[1])
        else:
            a = (p[0] + u_prev[0] * rc, p[1] + u_prev[1] * rc)
            u_prev_a = u_prev

        if i in arc_edges:
            ang_p = math.atan2(p[1] - cy, p[0] - cx)
            ang_b = ang_p + (rc / R)
            b = (cx + R * math.cos(ang_b), cy + R * math.sin(ang_b))
            rb = unit((cx, cy), b)
            tb = (-rb[1], rb[0])
            u_next_b = tb
        else:
            b = (p[0] + u_next[0] * rc, p[1] + u_next[1] * rc)
            u_next_b = u_next

        c1 = (a[0] - u_prev_a[0] * rc * 0.55, a[1] - u_prev_a[1] * rc * 0.55)
        c2 = (b[0] - u_next_b[0] * rc * 0.55, b[1] - u_next_b[1] * rc * 0.55)
        corners.append((a, c1, c2, b))

    d = [f"M {fmt(corners[0][0][0])} {fmt(corners[0][0][1])}"]
    for i in range(n):
        a, c1, c2, b = corners[i]
        next_a = corners[(i + 1) % n][0]
        d.append(f"C {fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(b[0])} {fmt(b[1])}")
        if i in arc_edges:
            d.append(f"A {fmt(R)} {fmt(R)} 0 0 1 {fmt(next_a[0])} {fmt(next_a[1])}")
        else:
            d.append(f"L {fmt(next_a[0])} {fmt(next_a[1])}")
    d.append("Z")
    return " ".join(d)

def build_ball_dome_v4(cx=110.0, cy=186.0, R=102.0, mode="classic"):
    """
    Returns list of individual panel path strings (zero pinching on p3 and p8!).
    """
    def on_circle(deg):
        return pt(cx, cy, R, deg)

    panels = []
    # 1. Large Left-Center Hexagon:
    p1 = [
        (94, 108),   # top
        (128, 128),  # upper-right
        (118, 166),  # lower-right
        (68, 184),   # bottom
        (42, 150),   # lower-left
        (54, 118),   # upper-left
    ]
    panels.append(build_panel_with_arcs(p1, set(), r_corner=7.0, cx=cx, cy=cy, R=R))

    # 2. Large Right-Center Hexagon:
    p2 = [
        (140, 130),  # upper-left
        (174, 120),  # top-right
        (196, 152),  # middle-right
        (186, 190),  # bottom-right on horizon
        (138, 190),  # bottom-left on horizon
        (130, 168),  # middle-left
    ]
    panels.append(build_panel_with_arcs(p2, set(), r_corner=7.0, cx=cx, cy=cy, R=R))

    # 3. Top-Left Rim Panel (parallel to p1's top-left edge (54,118)->(94,108)!):
    # Note: p1's top-left edge goes from (54, 118) to (94, 108) (slope dy/dx = -10/40 = -0.25).
    # Offset up-left by 12 units: inner edge runs from (46, 108) to (88, 97.5).
    # On circle R=102 around (110, 186):
    # At 219 deg: (30.7, 121.8) -> inner point (48, 108) is down-right of the arc!
    # Wait: at 220 deg, the circle is at (31.9, 120.4), and at 261 deg it is at (94.0, 85.3).
    # The chord from (31.9, 120.4) to (94.0, 85.3) has midpoint (63, 102.8).
    # So the inner edge inside the circle must have y > 103 (e.g., from (88, 96) to (48, 107) — wait: at x=48, the chord y is 120.4 - (48-31.9)*(35.1/62.1) = 111.3!
    # THAT'S why (46, 106) was outside the chord (106 < 111.3)!
    # For the panel to be inside the circle, at x=50, y must be > 111 (e.g. (50, 108) is outside, (50, 112) is inside)!
    # Let's shift p1's upper-left vertex slightly down to (54, 122) and top vertex to (94, 106),
    # and set p3's inner edge to (88, 96) -> (46, 114) while outer arc runs from 217 deg (28.5, 124.6) to 260 deg (92.3, 85.5)!
    # Let's check the chord from (28.5, 124.6) to (92.3, 85.5):
    # At x=46, chord y = 124.6 - (46-28.5)*(39.1/63.8) = 113.9, and outer arc y at x=46 (dx=-64) is 186 - sqrt(102^2 - 64^2) = 186 - 79.4 = 106.6!
    # So at x=46, the circle arc is at y=106.6, and the inner edge at (46, 112) is 5.4 units inside, or even better:
    # if we add an intermediate inner point (66, 102) or use a concave inner curve, the panel has a lush 14-unit thickness!
    p3 = [
        on_circle(217),  # (28.5, 124.6)
        on_circle(260),  # (92.3, 85.5)
        (88, 96),
        (64, 103),
        (42, 116),
    ]
    panels.append(build_panel_with_arcs(p3, {0}, r_corner=4.5, cx=cx, cy=cy, R=R))

    # 4. Top-Right Pentagon/Hexagon Rim Panel (outer arc from 267 deg to 308 deg):
    p4 = [
        on_circle(267),
        on_circle(308),
        (168, 109),
        (134, 118),
        (104, 97),
    ]
    panels.append(build_panel_with_arcs(p4, {0}, r_corner=5.5, cx=cx, cy=cy, R=R))

    # 5. Far-Left Middle Rim Panel (outer arc from 191 deg to 211 deg):
    p5 = [
        on_circle(191),  # (9.9, 166.5)
        on_circle(211),  # (22.6, 133.5)
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
        (120, 177),
        (126, 190),
    ]
    panels.append(build_panel_with_arcs(p7, set(), r_corner=3.5, cx=cx, cy=cy, R=R))

    # 8. Far-Right Upper Rim Panel (outer arc from 314 deg to 344 deg):
    # At 314 deg: (180.9, 112.6); at 344 deg: (208.0, 157.9); midpoint on circle at 329 deg is (197.4, 133.5)
    p8 = [
        on_circle(314),
        on_circle(344),
        (203, 146),
        (192, 129),
        (182, 116),
    ]
    panels.append(build_panel_with_arcs(p8, {0}, r_corner=3.0, cx=cx, cy=cy, R=R))

    if mode == "classic":
        # 9. Far-Right Lower Sliver:
        p9 = [
            on_circle(350),
            (211.9, 190),
            (199, 190),
            (207, 164),
        ]
        panels.append(build_panel_with_arcs(p9, {0}, r_corner=2.5, cx=cx, cy=cy, R=R))

    return panels

def build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style="classic"):
    """
    Returns list of individual path strings and optional evenodd hull path string.
    Zero overlap between masts and hull/sails!
    """
    ca, sa = math.cos(math.radians(angle_deg)), math.sin(math.radians(angle_deg))
    def uv(u, v):
        x = ox + u * ca + v * sa
        y = oy + u * sa - v * ca
        return (x, y)

    def uvs(u, v):
        x, y = uv(u, v)
        return f"{fmt(x)} {fmt(y)}"

    solids = []
    hull_evenodd = None

    if style in ("classic", "sail_m"):
        hull_outer = (
            f"M {uvs(-34, 14)} "
            f"C {uvs(-30, 14)} {uvs(-27, 9)} {uvs(-25, 2)} "
            f"L {uvs(18, 2)} "
            f"C {uvs(21, 5)} {uvs(24, 9)} {uvs(28, 10)} "
            f"L {uvs(31, 6)} "
            f"L {uvs(38, 6)} "
            f"C {uvs(38, 3)} {uvs(35, 1)} {uvs(28, 1)} "
            f"C {uvs(25, -4)} {uvs(22, -12)} {uvs(17, -12)} "
            f"L {uvs(-18, -12)} "
            f"C {uvs(-26, -12)} {uvs(-31, -2)} {uvs(-32, 7)} "
            f"C {uvs(-34, 10)} {uvs(-35, 12)} {uvs(-34, 14)} Z"
        )
        stern_hole = (
            f"M {uvs(21, 0)} "
            f"C {uvs(23, 5)} {uvs(26, 6)} {uvs(27, 4)} "
            f"C {uvs(26, 0)} {uvs(24, -2)} {uvs(21, 0)} Z"
        )
        hull_evenodd = hull_outer + " " + stern_hole
        solids.append(f"M {uvs(-33, 13)} L {uvs(-31, 19)} L {uvs(-39, 18)} L {uvs(-37, 15)} L {uvs(-40, 13)} Z")

    if style == "classic":
        sails_spec = [
            (-22, -9,  10, 29, -5.5),
            (-6,   9,  10, 33, -6.5),
            (12,  24,   9, 26, -5.0),
        ]
        for (ul, ur, vb, vt, push) in sails_spec:
            um = (ul + ur) / 2.0
            vm = (vb + vt) / 2.0
            sail = (
                f"M {uvs(ul, vt)} "
                f"L {uvs(ur, vt)} "
                f"C {uvs(ur + push*0.7, vm + 3)} {uvs(ur + push*0.7, vm - 3)} {uvs(ur, vb)} "
                f"L {uvs(ul, vb)} "
                f"C {uvs(ul + push, vm - 3)} {uvs(ul + push, vm + 3)} {uvs(ul, vt)} Z"
            )
            solids.append(sail)
            solids.append(f"M {uvs(um - 1.6, 1.5)} L {uvs(um + 1.6, 1.5)} L {uvs(um + 1.6, vb + 0.5)} L {uvs(um - 1.6, vb + 0.5)} Z")
            solids.append(
                f"M {uvs(um - 1.3, vt - 0.5)} L {uvs(um + 1.3, vt - 0.5)} "
                f"L {uvs(um + 1.3, vt + 7)} L {uvs(um - 9, vt + 5.5)} "
                f"L {uvs(um - 7, vt + 3.5)} L {uvs(um - 9, vt + 2)} "
                f"L {uvs(um - 1.3, vt + 2.5)} Z"
            )

    elif style == "sail_m":
        sail_m = (
            f"M {uvs(-22, 8)} "
            f"C {uvs(-28, 17)} {uvs(-27, 27)} {uvs(-19, 35)} "
            f"L {uvs(-9, 35)} "
            f"L {uvs(1, 20)} "
            f"L {uvs(11, 35)} "
            f"L {uvs(21, 35)} "
            f"C {uvs(15, 26)} {uvs(15, 16)} {uvs(21, 8)} "
            f"L {uvs(10, 8)} "
            f"C {uvs(6, 14)} {uvs(6, 20)} {uvs(9, 25)} "
            f"L {uvs(1, 11)} "
            f"L {uvs(-8, 25)} "
            f"C {uvs(-12, 19)} {uvs(-12, 13)} {uvs(-9, 8)} Z"
        )
        solids.append(sail_m)
        for um in (-14, 15):
            solids.append(f"M {uvs(um - 1.6, 1.5)} L {uvs(um + 1.6, 1.5)} L {uvs(um + 1.6, 8.5)} L {uvs(um - 1.6, 8.5)} Z")
            solids.append(
                f"M {uvs(um - 1.3, 34.5)} L {uvs(um + 1.3, 34.5)} "
                f"L {uvs(um + 1.3, 41)} L {uvs(um - 8, 39.5)} "
                f"L {uvs(um - 6, 37.5)} L {uvs(um - 8, 36)} "
                f"L {uvs(um - 1.3, 36.5)} Z"
            )

    elif style == "wave_flow":
        # Variant C: Continuous Wave-Orbit + Sleek Modern Ship (hull and upper orbit flow smoothly together!)
        hull = (
            f"M {uvs(-38, 13)} "
            f"C {uvs(-28, 4)} {uvs(-18, 1)} {uvs(24, 1)} "
            f"L {uvs(37, 5)} "
            f"C {uvs(31, -6)} {uvs(21, -11)} {uvs(-16, -11)} "
            f"C {uvs(-26, -11)} {uvs(-33, -1)} {uvs(-38, 13)} Z"
        )
        solids.append(hull)
        # Three dynamic wind-filled sails with integrated mast-pennants:
        for (ul, ur, vb, vt, push) in [(-22, -9, 6, 29, -6.5), (-6, 9, 6, 35, -7.5), (12, 24, 6, 26, -5.5)]:
            um = (ul + ur) / 2.0
            vm = (vb + vt) / 2.0
            sail = (
                f"M {uvs(ul, vt)} L {uvs(ur, vt)} "
                f"C {uvs(ur + push*0.65, vm + 2)} {uvs(ur + push*0.65, vm - 2)} {uvs(ur, vb)} "
                f"L {uvs(ul, vb)} "
                f"C {uvs(ul + push, vm - 2)} {uvs(ul + push, vm + 2)} {uvs(ul, vt)} Z"
            )
            solids.append(sail)
            solids.append(f"M {uvs(um - 1.6, 0.5)} L {uvs(um + 1.6, 0.5)} L {uvs(um + 1.6, vb + 0.5)} L {uvs(um - 1.6, vb + 0.5)} Z")
            solids.append(f"M {uvs(um - 1.2, vt - 0.5)} L {uvs(um + 1.2, vt - 0.5)} L {uvs(um + 1.2, vt + 6.5)} L {uvs(um - 8.5, vt + 3.8)} Z")

    return solids, hull_evenodd

from build_evo_v3 import build_single_contour_wordmark, arc_band, tapered_orbit_arc

wm_main, wm_p = build_single_contour_wordmark(y_top=204.0, h=36.0, sw=5.6)

orb_uniform = [
    arc_band(114, 184, 122, 130, 214, 276),
    arc_band(114, 184, 122, 130, 326, 363),
]
orb_swoosh = [
    tapered_orbit_arc(114, 184, 126, 212, 277, 3.0, 9.5, 5.0),
    tapered_orbit_arc(114, 184, 126, 325, 363, 9.0, 7.5, 3.5),
]

for code, title, ball_mode, orb, ship_style in [
    ("evo-a", "М-ТРЕНИНГ — Вариант A (Ювелирный ремастеринг оригинала)", "classic", orb_uniform, "classic"),
    ("evo-b", "М-ТРЕНИНГ — Вариант B (Парус-М на орбите)", "clean", orb_swoosh, "sail_m"),
    ("evo-c", "М-ТРЕНИНГ — Вариант C (Скоростной Аэро-Поток)", "clean", orb_swoosh, "wave_flow"),
]:
    ball = build_ball_dome_v4(cx=110.0, cy=186.0, R=102.0, mode=ball_mode)
    ship_solids, hull_eo = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style=ship_style)
    # Put each path as its own <path> element so zero overlap cancellation can ever occur!
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
    p_dark = os.path.join(OUT_DIR, f"{code}-v4-dark.svg")
    with open(p_dark, "w", encoding="utf-8") as f:
        f.write(svg_dark)
    render_png.render(p_dark, os.path.join(OUT_DIR, f"{code}-v4-dark.png"), 512, 512, bg="#05070A")

print("Built v4 evolutionary marks")
