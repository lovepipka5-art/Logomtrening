#!/usr/bin/env python3
"""Геометрия НОВОГО знака «М-ТРЕНИНГ» (Nova, 2026).

Знак строится с нуля и НЕ наследует прежнюю сюжетную композицию
(купол мяча + парусник + орбитальная дуга). Новая идея — монограмма «М»:
простая, спортивная, работающая на форме, в вышивке и в 16 px.

Три независимые концепции:
  A «ПУЛЬС»     — монолинейная «М», средний зуб уходит ниже базовой линии,
                  как пик кардиограммы: буква, прочерченная ударом сердца.
  B «СРЕЗ»      — бейдж-пластина со срезанным углом и вырубленной
                  атлетической «М» со срезанными углами (нашивка / аватар /
                  чеканка на гире).
  C «ПЕНТАГОН»  — геометрическая «М», в основании которой — панель
                  футбольного мяча (пентагон). Мяч не нарисован, он встроен
                  в букву.

Техника: все фигуры — булевы операции над примитивами (skia-pathops),
сериализуются в чистые заполненные контуры. Без <text>, без растров,
без фильтров и градиентов. Кириллический леттеринг «М-ТРЕНИНГ» построен
как собственные геометрические контуры (шрифтовая сетка 100 единиц).
"""

import math

import pathops
from fontTools.pens.svgPathPen import SVGPathPen

# ---------------------------------------------------------------- палитра
INK = "#12161C"      # чернильный (раунд 1)
PITCH = "#0B3B2C"    # тёмная зелень поля (раунд 1)
BLUE = "#1B44D8"     # основной цвет школы — королевский синий
DEEP = "#0A1633"     # ночной синий — тёмные поверхности
VOLT = "#D8F74E"     # вольтовый акцент (только на тёмном / на синем)
WHITE = "#FFFFFF"

K = 0.5522847498307936  # каппа для кубических дуг окружности


# ---------------------------------------------------------------- сериализация
def ntos(v):
    v = round(float(v), 2)
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return ("%.2f" % v).rstrip("0").rstrip(".")


def to_d(path):
    """pathops.Path -> строка атрибута d (конусы -> квадратики)."""
    path.convertConicsToQuads()
    pen = SVGPathPen(None, ntos=ntos)
    path.draw(pen)
    return pen.getCommands()


# ---------------------------------------------------------------- примитивы
def poly(points):
    pts = [tuple(p) for p in points]
    # убираем дубликаты соседних вершин
    clean = []
    for p in pts:
        if not clean or (abs(p[0] - clean[-1][0]) > 1e-6 or abs(p[1] - clean[-1][1]) > 1e-6):
            clean.append(p)
    if len(clean) > 1 and abs(clean[0][0] - clean[-1][0]) < 1e-6 and abs(clean[0][1] - clean[-1][1]) < 1e-6:
        clean.pop()
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo(clean[0])
    for pt in clean[1:]:
        pen.lineTo(pt)
    pen.closePath()
    return p


def rect(x, y, w, h):
    return poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])


def circle(cx, cy, r):
    p = pathops.Path()
    pen = p.getPen()
    k = K * r
    pen.moveTo((cx, cy - r))
    pen.curveTo((cx + k, cy - r), (cx + r, cy - k), (cx + r, cy))
    pen.curveTo((cx + r, cy + k), (cx + k, cy + r), (cx, cy + r))
    pen.curveTo((cx - k, cy + r), (cx - r, cy + k), (cx - r, cy))
    pen.curveTo((cx - r, cy - k), (cx - k, cy - r), (cx, cy - r))
    pen.closePath()
    return p


def rounded_rect(x, y, w, h, r):
    p = pathops.Path()
    pen = p.getPen()
    k = K * r
    pen.moveTo((x + r, y))
    pen.lineTo((x + w - r, y))
    pen.curveTo((x + w - r + k, y), (x + w, y + r - k), (x + w, y + r))
    pen.lineTo((x + w, y + h - r))
    pen.curveTo((x + w, y + h - r + k), (x + w - r + k, y + h), (x + w - r, y + h))
    pen.lineTo((x + r, y + h))
    pen.curveTo((x + r - k, y + h), (x, y + h - r + k), (x, y + h - r))
    pen.lineTo((x, y + r))
    pen.curveTo((x, y + r - k), (x + r - k, y), (x + r, y))
    pen.closePath()
    return p


def pentagon_pts(cx, cy, r):
    pts = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def pentagon(cx, cy, r):
    return poly(pentagon_pts(cx, cy, r))


def chamfer_poly(points, idxs, c):
    """Срезать указанные вершины многоугольника фаской (по длине рёбер c)."""
    n = len(points)
    out = []
    for i, pt in enumerate(points):
        if i not in idxs:
            out.append(pt)
            continue
        prev = points[(i - 1) % n]
        nxt = points[(i + 1) % n]

        def along(other):
            dx, dy = other[0] - pt[0], other[1] - pt[1]
            L = (dx * dx + dy * dy) ** 0.5
            return (pt[0] + dx / L * c, pt[1] + dy / L * c)

        out.append(along(prev))
        out.append(along(nxt))
    return poly(out)


def cbar(x, y, w, h, c=0, corners=()):
    """Прямоугольник со срезанными углами: corners ⊂ {tl,tr,bl,br}."""
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    idx = [i for i, k in enumerate(("tl", "tr", "br", "bl")) if k in corners]
    if not idx or not c:
        return poly(pts)
    return chamfer_poly(pts, idx, c)


def stroke_polyline(points, w, cap="butt", join="miter", miter=6.0):
    """Полилиния -> заполненный контур заданной толщины."""
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo(tuple(points[0]))
    for pt in points[1:]:
        pen.lineTo(tuple(pt))
    caps = {"butt": pathops.LineCap.BUTT_CAP, "round": pathops.LineCap.ROUND_CAP,
            "square": pathops.LineCap.SQUARE_CAP}[cap]
    joins = {"miter": pathops.LineJoin.MITER_JOIN, "round": pathops.LineJoin.ROUND_JOIN,
             "bevel": pathops.LineJoin.BEVEL_JOIN}[join]
    p.stroke(w, caps, joins, miter)
    return p


# ---------------------------------------------------------------- булевы
def uni(*paths):
    out = paths[0]
    for p in paths[1:]:
        out = pathops.op(out, p, pathops.PathOp.UNION)
    return out


def dif(a, b):
    return pathops.op(a, b, pathops.PathOp.DIFFERENCE)


def itr(a, b):
    return pathops.op(a, b, pathops.PathOp.INTERSECTION)


def halfplane_below(y):
    return rect(-4000, -4000, 12000, y + 4000)


def bounds(path):
    return path.bounds  # (x0, y0, x1, y1)


# ================================================================ СИМВОЛЫ
def solid_m(x0, cap, base, w, s, apex_y=None, apex_flat=0.09, chamfers=0):
    """Классическая геометрическая М одним контуром (13 вершин).

    apex_y    — куда опускается средний зуб (по умолчанию base);
    apex_flat — полуширина плоского среза зуба (доля w), 0 = острый зуб;
    chamfers  — размер фаски 4-х внешних углов (0 = без).
    """
    A = base if apex_y is None else apex_y
    F = w * apex_flat
    Hb = base
    k = (w / 2 - F) / (A - cap)   # наклон внешних диагоналей (x на y)
    a_i = cap + (w / 2 - s) / k   # внутренний вершинный узел
    y_open = cap + s / k          # где внешняя диагональ уходит от ствола
    xm = x0 + w / 2
    pts = [
        (x0, cap), (x0 + s, cap), (xm, a_i), (x0 + w - s, cap), (x0 + w, cap),
        (x0 + w, Hb), (x0 + w - s, Hb), (x0 + w - s, y_open),
        (xm + F, A), (xm - F, A),
        (x0 + s, y_open), (x0 + s, Hb), (x0, Hb),
    ]
    if chamfers:
        return chamfer_poly(pts, [0, 4, 5, 12], chamfers)
    return poly(pts)


def symbol_pulse(w=27, cap=52, base=168, tip=204, x0=40.22, w_full=175.55):
    """A «ПУЛЬС»: монолинейная М с пиком ниже базовой линии.

    Диагонали выведены точно под 60° к горизонтали (tan 60 = 1.7320):
    w_full = 2 * (tip - cap) / 1.7320508.
    """
    m = solid_m(x0, cap, base, w_full, w, apex_y=tip, apex_flat=0.0)
    above = itr(m, halfplane_below(base))
    spike = dif(m, halfplane_below(base))
    return {
        "shapes": [(to_d(above), "main"), (to_d(spike), "accent")],
        "bbox": (x0, cap, x0 + w_full, tip),
        "baseline": base,
        "name": "ПУЛЬС",
        "letter": "A",
        "idea": "Одна линия-кардиограмма: средний зуб «М» бьёт ниже базовой "
                "линии — импульс усилия и роста.",
    }


def symbol_srez():
    """B «СРЕЗ»: пластина со срезанным углом + вырубленная атлетическая М."""
    plate = rounded_rect(16, 16, 224, 224, 46)
    # полуплоскость ниже линии среза (через точки (176,16) и (240,80)):
    # растягиваем и вдоль линии, и вглубь сохраняемой стороны
    cut = poly([(176 - 4000, 16 - 4000), (240 + 4000, 80 + 4000),
                (240, 80 + 8000), (176 - 8000, 16)])
    plate = itr(plate, cut)
    m = solid_m(58, 64, 200, 148, 30, apex_flat=0.08, chamfers=12)
    knockout = dif(plate, m)
    return {
        "shapes": [(to_d(knockout), "main"), (to_d(m), "accent")],
        "bbox": (16, 16, 240, 240),
        "baseline": 188,
        "name": "СРЕЗ",
        "letter": "B",
        "idea": "Нашивка-пластина со срезанным углом: атлетическая «М» "
                "вырублена насквозь — знак готов к форме, аватару и чеканке.",
    }


def symbol_penta(x0=36, cap=42, base=214, w=184, s=32, r=40):
    """C «ПЕНТАГОН»: М, в основании которой панель мяча."""
    cy = base - 0.809 * r
    cx = x0 + w / 2
    verts = pentagon_pts(cx, cy, r)
    T, UR, LR, LL, UL = verts
    left_arm = poly([(x0, cap), (x0 + s, cap), T, UL])
    right_arm = poly([(x0 + w, cap), (x0 + w - s, cap), T, UR])
    left_stem = rect(x0, cap, s, base - cap)
    right_stem = rect(x0 + w - s, cap, s, base - cap)
    pent = poly(verts)
    body = uni(left_stem, left_arm, right_arm, right_stem)
    return {
        "shapes": [(to_d(body), "main"), (to_d(pent), "accent")],
        "bbox": (x0, cap, x0 + w, base),
        "baseline": base,
        "name": "ПЕНТАГОН",
        "letter": "C",
        "idea": "Панель футбольного мяча встроена в основание буквы «М»: "
                "мяч — фундамент, из которого растёт сила.",
    }


# ================================================================ ЛЕТТЕРИНГ
# Сетка: кегль 100 (cap height), базовая линия y=100.
STYLES = {
    "pulse": dict(sw=15, tr=7.5, ch=0, m_drop=15, penta_hyphen=False, bowl=27,
                  widths=dict(M=88, T=78, R=71, E=66, H=80, I=82, G=64, hy=26)),
    "srez": dict(sw=19, tr=9.5, ch=7, m_drop=0, penta_hyphen=False, bowl=28,
                 widths=dict(M=96, T=86, R=75, E=72, H=88, I=90, G=70, hy=30)),
    "penta": dict(sw=18, tr=8.5, ch=0, m_drop=0, penta_hyphen=True, bowl=28,
                  widths=dict(M=94, T=84, R=74, E=70, H=86, I=88, G=68, hy=36)),
}

GLYPH_KEYS = {"М": "M", "Т": "T", "Р": "R", "Е": "E", "Н": "H", "И": "I",
              "Г": "G", "-": "-"}


def _glyph(key, st):
    """Возвращает (path, advance) глифа в сетке кегля 100."""
    sw, c = st["sw"], st["ch"]
    W = st["widths"]["hy" if key == "-" else key]
    mid = (100 - sw) / 2.0
    if key == "M":
        return solid_m(0, 0, 100, W, sw, apex_y=100 + st["m_drop"],
                       apex_flat=0.10, chamfers=c), W
    if key == "T":
        bar = cbar(0, 0, W, sw, c, ("tl", "tr"))
        stem = cbar((W - sw) / 2.0, 0, sw, 100, c, ("bl", "br"))
        return uni(bar, stem), W
    if key == "R":
        ro = st["bowl"]
        ri = ro - sw
        cx = W - ro
        p = pathops.Path()
        pen = p.getPen()
        pen.moveTo((0, 0))
        pen.lineTo((cx, 0))
        pen.curveTo((cx + K * ro, 0), (cx + ro, 2 * ro - K * ro), (cx + ro, 2 * ro))
        pen.lineTo((0, 2 * ro))
        pen.closePath()
        hole = pathops.Path()
        pen = hole.getPen()
        pen.moveTo((sw, sw))
        pen.lineTo((cx, sw))
        pen.curveTo((cx + K * ri, sw), (cx + ri, 2 * ro - sw - K * ri),
                    (cx + ri, 2 * ro - sw))
        pen.lineTo((sw, 2 * ro - sw))
        pen.closePath()
        stem = cbar(0, 0, sw, 100, c, ("bl", "br"))
        return uni(stem, dif(p, hole)), W
    if key == "E":
        top = cbar(0, 0, W, sw, c, ("tl", "tr"))
        midbar = cbar(0, mid, W - 9, sw, c, ("tr", "br"))
        bot = cbar(0, 100 - sw, W, sw, c, ("bl", "br"))
        stem = rect(0, 0, sw, 100)
        return uni(stem, top, midbar, bot), W
    if key == "H":
        left = cbar(0, 0, sw, 100, c, ("tl", "bl"))
        right = cbar(W - sw, 0, sw, 100, c, ("tr", "br"))
        return uni(left, right, rect(0, mid, W, sw)), W
    if key == "I":  # «И»
        left = cbar(0, 0, sw, 100, c, ("tl", "bl"))
        right = cbar(W - sw, 0, sw, 100, c, ("tr", "br"))
        diag = poly([(0, 0), (sw, 0), (W, 100), (W - sw, 100)])
        return uni(left, right, diag), W
    if key == "G":
        bar = cbar(0, 0, W, sw, c, ("tl", "tr"))
        stem = cbar(0, 0, sw, 100, c, ("bl", "br"))
        return uni(bar, stem), W
    if key == "-":
        if st["penta_hyphen"]:
            return pentagon(W / 2.0, 54, 16), W
        return cbar(0, 54 - sw / 2.0, W, sw, max(2, c // 2),
                    ("tl", "tr", "bl", "br")), W
    raise ValueError(key)


def wordmark(text, style):
    """Собирает леттеринг. Возвращает (d, width, bounds)."""
    st = STYLES[style]
    x = 0.0
    out = None
    for ch in text:
        g, adv = _glyph(GLYPH_KEYS[ch], st)
        shifted = g.transform(1, 0, 0, 1, x, 0)
        out = shifted if out is None else pathops.op(out, shifted, pathops.PathOp.UNION)
        x += adv + st["tr"]
    x -= st["tr"]
    return to_d(out), x, bounds(out)


# ================================================================ КОМПОНОВКИ
def lockup_h(sym, style, text="М-ТРЕНИНГ"):
    """Горизонтальная компоновка: знак слева, леттеринг справа."""
    d, w_wm, wb = wordmark(text, style)
    ink_w = wb[2] - wb[0]
    bx0, by0, bx1, by1 = sym["bbox"]
    sym_w = bx1 - bx0
    sym_h = by1 - by0
    H = 256.0
    ty = (H - sym_h) / 2.0 - by0
    base_y = sym["baseline"] + ty
    hc = 0.44 * sym_h                      # кегль леттеринга
    ws = hc / 100.0
    wx = sym_w + 0.55 * hc - wb[0] * ws
    wy = base_y - hc - wb[1] * ws
    total = wx + wb[0] * ws + ink_w * ws
    return {
        "vb": (0, 0, math.ceil(total), int(H)),
        "groups": [
            (f"translate({ntos(-bx0)} {ntos(ty)})", sym["shapes"]),
            (f"translate({ntos(wx)} {ntos(wy)}) scale({ntos(ws)})",
             [(d, "wm")]),
        ],
    }


def lockup_v(sym, style, text="М-ТРЕНИНГ"):
    """Вертикальная компоновка: знак сверху, леттеринг снизу по центру."""
    d, w_wm, _b = wordmark(text, style)
    bx0, by0, bx1, by1 = sym["bbox"]
    sym_w = bx1 - bx0
    sym_h = by1 - by0
    hc = 0.34 * sym_w
    ws = hc / 100.0
    wm_w = w_wm * ws
    W = max(sym_w, wm_w) + 40
    tx = (W - sym_w) / 2.0 - bx0
    ty = 12
    base_y = ty + sym_h
    wx = (W - wm_w) / 2.0
    wy = base_y + 0.42 * hc
    H = math.ceil(wy + hc + 0.30 * hc + 12)
    return {
        "vb": (0, 0, math.ceil(W), H),
        "groups": [
            (f"translate({ntos(tx)} {ntos(ty)})", sym["shapes"]),
            (f"translate({ntos(wx)} {ntos(wy)}) scale({ntos(ws)})",
             [(d, "wm")]),
        ],
    }


def svg_from_layout(layout, palette, title="", bg=None):
    parts = []
    if bg:
        x, y, w, h = layout["vb"]
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>')
    for tr, shapes in layout["groups"]:
        inner = "".join(f'<path fill="{palette.get(r, palette["main"])}" d="{d}"/>'
                        for d, r in shapes)
        parts.append(f'<g transform="{tr}">{inner}</g>')
    x, y, w, h = layout["vb"]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>'
            + "".join(parts) + "</svg>")


def svg_symbol(sym, palette, title="", bg=None):
    shapes = [(d, palette.get(r, palette["main"])) for d, r in sym["shapes"]]
    parts = []
    if bg:
        parts.append(f'<rect x="0" y="0" width="256" height="256" fill="{bg}"/>')
    parts += [f'<path fill="{col}" d="{d}"/>' for d, col in shapes]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" '
            f'role="img" aria-labelledby="t"><title id="t">{title}</title>'
            + "".join(parts) + "</svg>")


def render(svg_str, w, h, out, bg=None):
    import resvg_py
    kw = dict(svg_string=svg_str, width=w, height=h,
              font_dirs=["/usr/share/fonts"])
    if bg:
        kw["background"] = bg
    data = resvg_py.svg_to_bytes(**kw)
    with open(out, "wb") as f:
        f.write(bytes(data))
    return out

# ================================================================ РАУНД 2: ФУТБОЛ
def symbol_goal(t=22, x0=36, x1=220, top=52, ground=204, ball_r=30):
    """D «ГОЛ»: штанги ворот, прогиб сетки и мяч в сетке.

    Силуэт читается и как сцена «мяч в сетке», и как буква «М»
    (штанги — стволы, прогиб сетки — средний зуб).
    """
    bar_h = t
    left_post = rect(x0, top, t, ground - top)
    right_post = rect(x1 - t, top, t, ground - top)
    crossbar = rect(x0, top, x1 - x0, bar_h)
    frame = uni(left_post, right_post, crossbar)
    cx = (x0 + x1) / 2.0
    net = stroke_polyline([(x0 + t, top + bar_h), (cx, ground - 46),
                           (x1 - t, top + bar_h)], 17, "butt", "miter", 8)
    ball = dif(circle(cx, ground - 30, ball_r), pentagon(cx, ground - 30, 15))
    return {
        "shapes": [(to_d(uni(frame, net)), "main"), (to_d(ball), "accent")],
        "bbox": (x0, top, x1, ground),
        "baseline": ground,
        "name": "ГОЛ",
        "letter": "D",
        "idea": "Штанги ворот и прогиб сетки от удара: мяч уже в сетке — "
                "сила удара видна без слов. Силуэт читается и как «М».",
    }


def symbol_panel(r=104, seam_w=17, seam_r0=78, mw=118, ms=25, cap=84, base=172):
    """E «ПАНЕЛЬ»: мяч, у которого вместо центральной панели — буква «М»."""
    cx = cy = 128.0
    ball = circle(cx, cy, r)
    m = solid_m(cx - mw / 2.0, cap, base, mw, ms, apex_flat=0.09)
    body = dif(ball, m)
    seams = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        p0 = (cx + seam_r0 * math.cos(a), cy + seam_r0 * math.sin(a))
        p1 = (cx + r * math.cos(a), cy + r * math.sin(a))
        seams.append(stroke_polyline([p0, p1], seam_w, "butt", "miter", 4))
    seams_p = uni(*seams)
    seams_p = itr(seams_p, ball)
    return {
        "shapes": [(to_d(body), "main"), (to_d(seams_p), "accent")],
        "bbox": (cx - r, cy - r, cx + r, cy + r),
        "baseline": cy + r,
        "name": "ПАНЕЛЬ",
        "letter": "E",
        "idea": "Мяч, у которого центральная панель заменена вырубленной «М»: "
                "буква буквально вшита в рисунок мяча, пять швов на месте.",
    }


def symbol_ballbase(x0=36, cap=42, base=214, w=184, s=32, r=40, hole=19):
    """F «МЯЧ-В-БУКВЕ»: в основании «М» — мяч-блин (круг с пентагоном).

    Круг с пентагоном внутри читается и как панель мяча, и как диск штанги:
    футбол + силовой тренинг в одной фигуре.
    """
    cx = x0 + w / 2.0
    cy = base - r
    left_arm = poly([(x0, cap), (x0 + s, cap), (cx, cy - 10), (cx - 34, cy + 6)])
    right_arm = poly([(x0 + w, cap), (x0 + w - s, cap), (cx, cy - 10), (cx + 34, cy + 6)])
    left_stem = rect(x0, cap, s, base - cap)
    right_stem = rect(x0 + w - s, cap, s, base - cap)
    body = uni(left_stem, left_arm, right_arm, right_stem)
    ball = dif(circle(cx, cy, r), pentagon(cx, cy, hole))
    return {
        "shapes": [(to_d(body), "main"), (to_d(ball), "accent")],
        "bbox": (x0, cap, x0 + w, base),
        "baseline": base,
        "name": "МЯЧ-В-БУКВЕ",
        "letter": "F",
        "idea": "В основании «М» — мяч-блин: круг с пентагоном внутри читается "
                "и как мяч, и как диск штанги. Футбол и сила в одной фигуре.",
    }

