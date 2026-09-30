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

def build_ball_dome(cx=110.0, cy=186.0, R=102.0, clean_mode=False):
    def on_circle(deg):
        return pt(cx, cy, R, deg)

    panels = []
    # 1. Large Left-Center Hexagon:
    p1 = [
        (94, 104),   # top
        (128, 126),  # upper-right
        (118, 166),  # lower-right
        (68, 184),   # bottom
        (42, 150),   # lower-left
        (54, 116),   # upper-left
    ]
    panels.append(build_panel_with_arcs(p1, set(), r_corner=6.5, cx=cx, cy=cy, R=R))

    # 2. Large Right-Center Hexagon:
    p2 = [
        (140, 128),  # upper-left
        (174, 118),  # top-right
        (196, 152),  # middle-right
        (186, 190),  # bottom-right on horizon
        (138, 190),  # bottom-left on horizon
        (130, 168),  # middle-left
    ]
    panels.append(build_panel_with_arcs(p2, set(), r_corner=6.5, cx=cx, cy=cy, R=R))

    # 3. Top-Left Rim Panel (thick, generous panel like in the original image!):
    # Outer arc from 220 deg (31.9, 120.4) to 260 deg (92.3, 85.5)
    # Inner edge parallel to p1's top-left edge (54,116)->(94,104), offset up-left by 12 units:
    p3 = [
        on_circle(220),  # (31.9, 120.4)
        on_circle(260),  # (92.3, 85.5)
        (88, 94),        # inner right
        (46, 106),       # inner left
    ]
    panels.append(build_panel_with_arcs(p3, {0}, r_corner=4.5, cx=cx, cy=cy, R=R))

    # 4. Top-Right Pentagon/Hexagon Rim Panel (outer edge on circle from 268 deg to 308 deg):
    p4 = [
        on_circle(268),
        on_circle(308),
        (168, 108),
        (134, 116),
        (104, 96),
    ]
    panels.append(build_panel_with_arcs(p4, {0}, r_corner=5.5, cx=cx, cy=cy, R=R))

    # 5. Far-Left Middle Rim Panel (outer edge on circle from 191 deg to 214 deg):
    p5 = [
        on_circle(191),
        on_circle(214),
        (42, 118),
        (30, 152),
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

    # 8. Far-Right Upper Rim Panel (outer arc from 315 deg to 344 deg):
    # At 315 deg: (182.1, 113.9); at 344 deg: (208.0, 157.9)
    # Inner edge parallel to p2's upper-right edge (174, 118) -> (196, 152):
    p8 = [
        on_circle(315),
        on_circle(344),
        (204, 146),
        (184, 115),
    ]
    panels.append(build_panel_with_arcs(p8, {0}, r_corner=3.0, cx=cx, cy=cy, R=R))

    if not clean_mode:
        # 9. Far-Right Lower Sliver (in strict original remaster):
        p9 = [
            on_circle(350),
            (211.9, 190),
            (199, 190),
            (207, 164),
        ]
        panels.append(build_panel_with_arcs(p9, {0}, r_corner=2.5, cx=cx, cy=cy, R=R))

    return panels

def build_tall_ship_v3(ox=182.0, oy=62.0, angle_deg=32.0, style="classic"):
    """
    Returns (solid_paths_list, evenodd_hull_path_or_none) so NO overlapping shapes create holes!
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

    if style == "classic":
        # Hull with stern oval cutout (placed in its own evenodd path so it only cuts the stern window!)
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

        # Bow pennant flag:
        solids.append(f"M {uvs(-33, 13)} L {uvs(-31, 19)} L {uvs(-39, 18)} L {uvs(-37, 15)} L {uvs(-40, 13)} Z")

        # 3 Full-Bellied Sails + Non-overlapping Masts + Flags:
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
            # Lower mast (from hull deck v=1 to sail bottom vb+1):
            solids.append(f"M {uvs(um - 1.6, 1)} L {uvs(um + 1.6, 1)} L {uvs(um + 1.6, vb + 1)} L {uvs(um - 1.6, vb + 1)} Z")
            # Upper mast + pennant flag (from sail top vt-1 to vt+7):
            solids.append(
                f"M {uvs(um - 1.3, vt - 1)} L {uvs(um + 1.3, vt - 1)} "
                f"L {uvs(um + 1.3, vt + 7)} L {uvs(um - 9, vt + 5.5)} "
                f"L {uvs(um - 7, vt + 3.5)} L {uvs(um - 9, vt + 2)} "
                f"L {uvs(um - 1.3, vt + 2.5)} Z"
            )

    elif style == "sail_m":
        # Variant B: Signature Sail-M — Classic Hull with stern window + Wind-filled Sails forming a stylish "М"!
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

        # Billowing Sail-M connected to deck by 2 clean masts + 2 mast flags:
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
            solids.append(f"M {uvs(um - 1.6, 1)} L {uvs(um + 1.6, 1)} L {uvs(um + 1.6, 9)} L {uvs(um - 1.6, 9)} Z")
            solids.append(
                f"M {uvs(um - 1.3, 34)} L {uvs(um + 1.3, 34)} "
                f"L {uvs(um + 1.3, 41)} L {uvs(um - 8, 39.5)} "
                f"L {uvs(um - 6, 37.5)} L {uvs(um - 8, 36)} "
                f"L {uvs(um - 1.3, 36.5)} Z"
            )

    elif style == "aero":
        # Variant C: Sleek Aero-Dynamic Ship (clean curved hull + 3 full wind-sails without tiny rigging, ideal for small jersey crests)
        hull = (
            f"M {uvs(-36, 13)} "
            f"C {uvs(-28, 4)} {uvs(-18, 1)} {uvs(24, 1)} "
            f"L {uvs(36, 5)} "
            f"C {uvs(30, -6)} {uvs(20, -11)} {uvs(-16, -11)} "
            f"C {uvs(-26, -11)} {uvs(-33, -1)} {uvs(-36, 13)} Z"
        )
        solids.append(hull)
        for (ul, ur, vb, vt, push) in [(-22, -9, 7, 29, -6.0), (-6, 9, 7, 34, -7.0), (12, 24, 7, 26, -5.5)]:
            um = (ul + ur) / 2.0
            vm = (vb + vt) / 2.0
            sail = (
                f"M {uvs(ul, vt)} L {uvs(ur, vt)} "
                f"C {uvs(ur + push*0.65, vm + 2)} {uvs(ur + push*0.65, vm - 2)} {uvs(ur, vb)} "
                f"L {uvs(ul, vb)} "
                f"C {uvs(ul + push, vm - 2)} {uvs(ul + push, vm + 2)} {uvs(ul, vt)} Z"
            )
            solids.append(sail)
            solids.append(f"M {uvs(um - 1.6, 0)} L {uvs(um + 1.6, 0)} L {uvs(um + 1.6, vb + 1)} L {uvs(um - 1.6, vb + 1)} Z")
            solids.append(f"M {uvs(um - 1.2, vt - 1)} L {uvs(um + 1.2, vt - 1)} L {uvs(um + 1.2, vt + 6)} L {uvs(um - 8, vt + 3.5)} Z")

    return solids, hull_evenodd

# =============================================================================
# PERFECT SINGLE-CONTOUR ROUNDED WORDMARK "М - Т Р Е Н И Н Г"
# Every glyph is a single closed non-self-intersecting path with rounded corners!
# =============================================================================
def build_single_contour_wordmark(y_top=204.0, h=36.0, sw=5.8):
    """
    Constructs each Cyrillic letter of 'М - Т Р Е Н И Н Г' as a single closed polygon
    with rounded corners (using rounded_poly_path with r=2.4) so there are ZERO self-intersections
    and every terminal and junction is smooth and rounded like the original logo!
    """
    y0, y1 = y_top, y_top + h
    ym = y_top + h * 0.5
    s = sw

    def rpoly(pts, r=2.2):
        n = len(pts)
        segs = []
        for i in range(n):
            p_prev = pts[(i - 1) % n]
            p_curr = pts[i]
            p_next = pts[(i + 1) % n]
            d1 = dist(p_curr, p_prev)
            d2 = dist(p_curr, p_next)
            rc = min(r, d1 * 0.42, d2 * 0.42)
            u1 = unit(p_curr, p_prev)
            u2 = unit(p_curr, p_next)
            a = (p_curr[0] + u1[0] * rc, p_curr[1] + u1[1] * rc)
            b = (p_curr[0] + u2[0] * rc, p_curr[1] + u2[1] * rc)
            c1 = (a[0] - u1[0] * rc * 0.58, a[1] - u1[1] * rc * 0.58)
            c2 = (b[0] - u2[0] * rc * 0.58, b[1] - u2[1] * rc * 0.58)
            segs.append((a, c1, c2, b))
        d = [f"M {fmt(segs[0][0][0])} {fmt(segs[0][0][1])}"]
        for i in range(n):
            a, c1, c2, b = segs[i]
            next_a = segs[(i + 1) % n][0]
            d.append(f"C {fmt(c1[0])} {fmt(c1[1])} {fmt(c2[0])} {fmt(c2[1])} {fmt(b[0])} {fmt(b[1])}")
            d.append(f"L {fmt(next_a[0])} {fmt(next_a[1])}")
        d.append("Z")
        return " ".join(d)

    glyphs = []

    # 1. М (x = 10..36, width 26, slightly angled outer legs like in original logo!):
    x = 10.0
    w = 26.0
    xm = x + w / 2.0
    pts_m = [
        (x + 2.5, y0),
        (x + 2.5 + s, y0),
        (xm, y1 - 11),
        (x + w - 2.5 - s, y0),
        (x + w - 2.5, y0),
        (x + w, y1),
        (x + w - s, y1),
        (x + w - 2.2 - s*0.85, y0 + 14),
        (xm + s*0.42, y1),
        (xm - s*0.42, y1),
        (x + 2.2 + s*0.85, y0 + 14),
        (x + s, y1),
        (x, y1),
    ]
    glyphs.append(rpoly(pts_m, r=2.0))

    # 2. - (x = 46..60):
    pts_hyph = [(46, ym - s/2 + 2), (60, ym - s/2 + 2), (60, ym + s/2 + 2), (46, ym + s/2 + 2)]
    glyphs.append(rpoly(pts_hyph, r=2.6))

    # 3. Т (x = 70..90, width 20):
    xt = 70.0
    wt = 20.0
    xmt = xt + wt / 2.0
    pts_t = [
        (xt, y0), (xt + wt, y0), (xt + wt, y0 + s),
        (xmt + s/2, y0 + s), (xmt + s/2, y1), (xmt - s/2, y1),
        (xmt - s/2, y0 + s), (xt, y0 + s)
    ]
    glyphs.append(rpoly(pts_t, r=2.2))

    # 4. Р (x = 99..117, width 18):
    xp = 99.0
    # Outer contour of Р + inner counter (using evenodd on its own path):
    p_outer = (
        f"M {fmt(xp)} {fmt(y0+2.2)} A 2.2 2.2 0 0 1 {fmt(xp+2.2)} {fmt(y0)} "
        f"L {fmt(xp+8.5)} {fmt(y0)} A 10.2 10.2 0 0 1 {fmt(xp+8.5)} {fmt(y0+20.4)} "
        f"L {fmt(xp+s)} {fmt(y0+20.4)} L {fmt(xp+s)} {fmt(y1-2.2)} "
        f"A 2.2 2.2 0 0 1 {fmt(xp)} {fmt(y1-2.2)} Z "
        f"M {fmt(xp+s)} {fmt(y0+s*0.92)} L {fmt(xp+8.2)} {fmt(y0+s*0.92)} "
        f"A {fmt(10.2-s*0.92)} {fmt(10.2-s*0.92)} 0 0 1 {fmt(xp+8.2)} {fmt(y0+20.4-s*0.92)} "
        f"L {fmt(xp+s)} {fmt(y0+20.4-s*0.92)} Z"
    )

    # 5. Е (x = 126..143, width 17):
    xe = 126.0
    we = 17.0
    pts_e = [
        (xe, y0), (xe + we, y0), (xe + we, y0 + s),
        (xe + s, y0 + s), (xe + s, ym - s/2),
        (xe + we - 2.5, ym - s/2), (xe + we - 2.5, ym + s/2),
        (xe + s, ym + s/2), (xe + s, y1 - s),
        (xe + we, y1 - s), (xe + we, y1), (xe, y1)
    ]
    glyphs.append(rpoly(pts_e, r=2.0))

    # 6. Н (x = 152..171, width 19):
    def make_n(xn, wn=19.0):
        pts_n = [
            (xn, y0), (xn + s, y0), (xn + s, ym - s/2),
            (xn + wn - s, ym - s/2), (xn + wn - s, y0), (xn + wn, y0),
            (xn + wn, y1), (xn + wn - s, y1), (xn + wn - s, ym + s/2),
            (xn + s, ym + s/2), (xn + s, y1), (xn, y1)
        ]
        return rpoly(pts_n, r=2.0)

    glyphs.append(make_n(152.0, 19.0))

    # 7. И (x = 180..199, width 19):
    xi = 180.0
    wi = 19.0
    pts_i = [
        (xi, y0), (xi + s, y0), (xi + s, y1 - 13),
        (xi + wi - s, y0), (xi + wi, y0), (xi + wi, y1),
        (xi + wi - s, y1), (xi + wi - s, y0 + 13),
        (xi + s, y1), (xi, y1)
    ]
    glyphs.append(rpoly(pts_i, r=1.8))

    # 8. Н (x = 208..227, width 19):
    glyphs.append(make_n(208.0, 19.0))

    # 9. Г (x = 236..251, width 15):
    xg = 236.0
    wg = 15.0
    pts_g = [
        (xg, y0), (xg + wg, y0), (xg + wg, y0 + s),
        (xg + s, y0 + s), (xg + s, y1), (xg, y1)
    ]
    glyphs.append(rpoly(pts_g, r=2.0))

    return " ".join(glyphs), p_outer

def arc_band(cx, cy, r1, r2, deg1, deg2):
    rcap = (r2 - r1) / 2.0
    x1o, y1o = pt(cx, cy, r2, deg1)
    x2o, y2o = pt(cx, cy, r2, deg2)
    x2i, y2i = pt(cx, cy, r1, deg2)
    x1i, y1i = pt(cx, cy, r1, deg1)
    return (f"M {fmt(x1o)} {fmt(y1o)} "
            f"A {fmt(r2)} {fmt(r2)} 0 0 1 {fmt(x2o)} {fmt(y2o)} "
            f"A {fmt(rcap)} {fmt(rcap)} 0 0 1 {fmt(x2i)} {fmt(y2i)} "
            f"A {fmt(r1)} {fmt(r1)} 0 0 0 {fmt(x1i)} {fmt(y1i)} "
            f"A {fmt(rcap)} {fmt(rcap)} 0 0 1 {fmt(x1o)} {fmt(y1o)} Z")

def tapered_orbit_arc(cx, cy, r_mid, deg1, deg2, w_start, w_mid, w_end):
    deg_m = (deg1 + deg2) / 2.0
    p1_o = pt(cx, cy, r_mid + w_start / 2.0, deg1)
    pm_o = pt(cx, cy, r_mid + w_mid / 2.0, deg_m)
    p2_o = pt(cx, cy, r_mid + w_end / 2.0, deg2)
    p2_i = pt(cx, cy, r_mid - w_end / 2.0, deg2)
    pm_i = pt(cx, cy, r_mid - w_mid / 2.0, deg_m)
    p1_i = pt(cx, cy, r_mid - w_start / 2.0, deg1)
    r_o = r_mid + w_mid / 2.0
    r_i = r_mid - w_mid / 2.0
    rc1 = max(1.5, w_start / 2.0)
    rc2 = max(1.5, w_end / 2.0)
    return (f"M {fmt(p1_o[0])} {fmt(p1_o[1])} "
            f"A {fmt(r_o)} {fmt(r_o)} 0 0 1 {fmt(pm_o[0])} {fmt(pm_o[1])} "
            f"A {fmt(r_o)} {fmt(r_o)} 0 0 1 {fmt(p2_o[0])} {fmt(p2_o[1])} "
            f"A {fmt(rc2)} {fmt(rc2)} 0 0 1 {fmt(p2_i[0])} {fmt(p2_i[1])} "
            f"A {fmt(r_i)} {fmt(r_i)} 0 0 0 {fmt(pm_i[0])} {fmt(pm_i[1])} "
            f"A {fmt(r_i)} {fmt(r_i)} 0 0 0 {fmt(p1_i[0])} {fmt(p1_i[1])} "
            f"A {fmt(rc1)} {fmt(rc1)} 0 0 1 {fmt(p1_o[0])} {fmt(p1_o[1])} Z")

wm_main, wm_p = build_single_contour_wordmark(y_top=204.0, h=36.0, sw=5.6)

orb_uniform = [
    arc_band(114, 184, 122, 130, 214, 276),
    arc_band(114, 184, 122, 130, 326, 363),
]
orb_swoosh = [
    tapered_orbit_arc(114, 184, 126, 212, 277, 3.0, 9.5, 5.0),
    tapered_orbit_arc(114, 184, 126, 325, 363, 9.0, 7.5, 3.5),
]

for code, title, clean_ball, orb, ship_style in [
    ("evo-a", "М-ТРЕНИНГ — Вариант A (Ювелирный ремастеринг оригинала)", False, orb_uniform, "classic"),
    ("evo-b", "М-ТРЕНИНГ — Вариант B (Парус-М на орбите)", True, orb_swoosh, "sail_m"),
    ("evo-c", "М-ТРЕНИНГ — Вариант C (Скоростной Аэро-Поток)", True, orb_swoosh, "aero"),
]:
    ball = build_ball_dome(cx=110.0, cy=186.0, R=102.0, clean_mode=clean_ball)
    ship_solids, hull_eo = build_tall_ship_v3(ox=182.0, oy=62.0, angle_deg=32.0, style=ship_style)
    sym_d = " ".join(ball + orb + ship_solids)
    hull_xml = f'\n    <path fill="#FFFFFF" fill-rule="evenodd" d="{hull_eo}"/>' if hull_eo else ""
    svg_dark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <g id="symbol">
    <path fill="#FFFFFF" d="{sym_d}"/>{hull_xml}
  </g>
  <g id="wordmark">
    <path fill="#FFFFFF" d="{wm_main}"/>
    <path fill="#FFFFFF" fill-rule="evenodd" d="{wm_p}"/>
  </g>
</svg>
'''
    p_dark = os.path.join(OUT_DIR, f"{code}-v3-dark.svg")
    with open(p_dark, "w", encoding="utf-8") as f:
        f.write(svg_dark)
    render_png.render(p_dark, os.path.join(OUT_DIR, f"{code}-v3-dark.png"), 512, 512, bg="#05070A")

print("Built v3 evolutionary marks")
