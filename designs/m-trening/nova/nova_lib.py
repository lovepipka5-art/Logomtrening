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
VOLT = "#D8F74E"
SUN = "#FFC61A"      # тёплый жёлтый мерч-акцент (раунд 8)
MAGENTA = "#F5164E"  # стритвир-акцент капсулы «ГРАФИТ»
SKY = "#8FA6FF"      # светлый синий для дудл-паттерна     # вольтовый акцент (только на тёмном / на синем)
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
    p.convertConicsToQuads()
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
                  widths=dict(M=88, T=78, R=71, E=66, H=80, I=82, G=64, hy=26,
                          Sh=96, K=78, O=92, L=78, A=86, S=78, B=78)),
    "srez": dict(sw=19, tr=9.5, ch=7, m_drop=0, penta_hyphen=False, bowl=28,
                 widths=dict(M=96, T=86, R=75, E=72, H=88, I=90, G=70, hy=30,
                         Sh=104, K=86, O=98, L=86, A=94, S=84, B=84)),
    "penta": dict(sw=18, tr=8.5, ch=0, m_drop=0, penta_hyphen=True, bowl=28,
                  widths=dict(M=94, T=84, R=74, E=70, H=86, I=88, G=68, hy=36,
                          Sh=102, K=84, O=96, L=84, A=92, S=82, B=82)),
    "varsity": dict(sw=17, tr=13, ch=0, m_drop=0, penta_hyphen=False,
                    barbell_hyphen=True, bowl=27,
                    slab=True,
                    widths=dict(M=92, T=80, R=72, E=66, H=84, I=86, G=66, hy=36,
                                Sh=100, K=82, O=94, L=82, A=90, S=80, B=80)),
}

GLYPH_KEYS = {"М": "M", "Т": "T", "Р": "R", "Е": "E", "Н": "H", "И": "I",
              "Г": "G", "-": "-", "Ш": "Sh", "К": "K", "О": "O", "Л": "L",
              "А": "A", "С": "S", "В": "B", " ": " "}

# Слэбы (колоджевые serif-пластины) на торцах штамбов для стиля varsity.
# Элемент кортежа может быть числом или строкой-выражением от W и sw.
SLAB_RECTS = {
    "M": [(-5, 0, "sw+5", 10), (-5, 90, "sw+5", 10),
          ("W-sw-5", 0, "sw+5", 10), ("W-sw-5", 90, "sw+5", 10)],
    "H": [(-5, 0, "sw+5", 10), (-5, 90, "sw+5", 10),
          ("W-sw-5", 0, "sw+5", 10), ("W-sw-5", 90, "sw+5", 10)],
    "I": [(-5, 0, "sw+5", 10), (-5, 90, "sw+5", 10),
          ("W-sw-5", 0, "sw+5", 10), ("W-sw-5", 90, "sw+5", 10)],
    "T": [("(W-sw)/2-5", 90, "sw+10", 10)],
    "R": [(-5, 0, "sw+5", 10), (-5, 90, "sw+5", 10)],
    "G": [(-5, 90, "sw+5", 10)],
}


def _glyph(key, st):
    """Глиф кегля 100; для стиля varsity добавляет слэбы на торцах штамбов."""
    g, W = _glyph_core(key, st)
    if g is not None and st.get("slab"):
        sw = st["sw"]
        for rx, ry, rw, rh in SLAB_RECTS.get(key, []):
            x = eval(rx, {"W": W, "sw": sw}) if isinstance(rx, str) else rx
            w = eval(rw, {"W": W, "sw": sw}) if isinstance(rw, str) else rw
            g = uni(g, rect(x, ry, w, rh))
    return g, W


def _glyph_core(key, st):
    """Возвращает (path, advance) глифа в сетке кегля 100."""
    if key == " ":
        return None, 45
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
    if key == "Sh":
        l = cbar(0, 0, sw, 100, c, ("tl", "bl"))
        m = cbar((W - sw) / 2.0, 0, sw, 100, c)
        r = cbar(W - sw, 0, sw, 100, c, ("tr", "br"))
        return uni(l, m, r, rect(0, 100 - sw, W, sw)), W
    if key == "K":
        stem = cbar(0, 0, sw, 100, c, ("tl", "bl"))
        up = poly([(sw, 52), (sw, 30), (W, 0), (W, 22)])
        lo = poly([(sw, 48), (sw, 70), (W, 100), (W, 78)])
        return uni(stem, up, lo), W
    if key == "O":
        outer = rounded_rect(0, 0, W, 100, 40)
        inner = rounded_rect(sw, sw, W - 2 * sw, 100 - 2 * sw, 40 - sw)
        return dif(outer, inner), W
    if key == "L":
        xt = W * 0.30
        pts = [(0, 100), (xt, 0), (W, 0), (W, sw * 1.0 + 0), (xt + sw * 1.30, sw),
               (sw * 1.25, 100)]
        pts = [(0, 100), (xt, 0), (W, 0), (W, sw), (xt + sw * 1.30, sw),
               (sw * 1.25, 100)]
        return chamfer_poly(pts, [2], c) if c else poly(pts), W
    if key == "A":
        left = poly([(0, 100), (W / 2 - sw / 2, 0), (W / 2 + sw / 2, 0), (sw, 100)])
        right = poly([(W, 100), (W / 2 + sw / 2, 0), (W / 2 - sw / 2, 0), (W - sw, 100)])
        bar = rect(W * 0.16, 60, W * 0.68, sw)
        return uni(left, right, bar), W
    if key == "S":
        outer = rounded_rect(0, 0, W, 100, 40)
        inner = rounded_rect(sw, sw, W - 2 * sw, 100 - 2 * sw, 40 - sw)
        ring = dif(outer, inner)
        cut = dif(rect(W - 40, 26, 60, 24), rect(0, 0, 0, 0))
        cut2 = rect(-20, 50, 60, 24)
        return dif(dif(ring, cut), cut2), W
    if key == "B":
        stem = cbar(0, 0, sw, 100, c, ("tl", "bl"))
        ro1, ro2 = 26.0, 26.0
        c1 = W - ro1
        top = pathops.Path()
        pen = top.getPen()
        pen.moveTo((0, 0)); pen.lineTo((c1, 0))
        pen.curveTo((c1 + K * ro1, 0), (c1 + ro1, 52 - K * ro1), (c1 + ro1, 52))
        pen.lineTo((0, 52)); pen.closePath()
        ri1 = ro1 - sw
        hole1 = pathops.Path()
        pen = hole1.getPen()
        pen.moveTo((sw, sw)); pen.lineTo((c1, sw))
        pen.curveTo((c1 + K * ri1, sw), (c1 + ri1, 52 - sw - K * ri1), (c1 + ri1, 52 - sw))
        pen.lineTo((sw, 52 - sw)); pen.closePath()
        c2 = W - ro2
        bot = pathops.Path()
        pen = bot.getPen()
        pen.moveTo((0, 48)); pen.lineTo((c2, 48))
        pen.curveTo((c2 + K * ro2, 48), (c2 + ro2, 100 - K * ro2), (c2 + ro2, 100))
        pen.lineTo((0, 100)); pen.closePath()
        ri2 = ro2 - sw
        hole2 = pathops.Path()
        pen = hole2.getPen()
        pen.moveTo((sw, 48 + sw)); pen.lineTo((c2, 48 + sw))
        pen.curveTo((c2 + K * ri2, 48 + sw), (c2 + ri2, 100 - sw - K * ri2),
                    (c2 + ri2, 100 - sw))
        pen.lineTo((sw, 100 - sw)); pen.closePath()
        return uni(stem, dif(top, hole1), dif(bot, hole2)), W
    if key == "-":
        if st.get("barbell_hyphen"):
            bar = rounded_rect(4, 50, W - 8, 9, 4)
            pl = rounded_rect(0, 40, 8, 29, 3)
            pr = rounded_rect(W - 8, 40, 8, 29, 3)
            return uni(bar, pl, pr), W
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
        if g is None:
            x += adv + st["tr"]
            continue
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
    total = wx + wb[0] * ws + ink_w * ws + 8
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
    # швы — сужающиеся к центру панели (трапеции), как у настоящего мяча
    seams = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        w0, w1 = seam_w * 0.62, seam_w          # внутри уже, у кромки шире
        p0 = (cx + seam_r0 * ux, cy + seam_r0 * uy)
        p1 = (cx + (r + 2) * ux, cy + (r + 2) * uy)
        seams.append(poly([(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2),
                           (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
                           (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2),
                           (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)]))
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



# ================================================================ РАУНД 3: ПЛОТНОСТЬ
def _glyph_path(ch, style):
    g, adv = _glyph(GLYPH_KEYS[ch], STYLES[style])
    return g, adv


def arc_text(text, style, cap, r_base, where, cx=128.0, cy=128.0, tracking=1.0):
    """Леттеринг по дуге: where='top' (верха наружу) или 'bottom' (верха к центру)."""
    st = STYLES[style]
    sc = cap / 100.0
    advs = []
    for ch in text:
        _g, adv = _glyph_path(ch, style)
        advs.append(adv + st["tr"] * tracking)
    total = (sum(advs) - st["tr"] * tracking) * sc
    span = total / r_base                      # полный угол в радианах
    out = None
    acc = 0.0
    for ch, adv in zip(text, advs):
        g, _a = _glyph_path(ch, style)
        if g is None:
            acc += adv
            continue
        mid = (acc + (adv - st["tr"] * tracking) / 2.0) * sc / r_base
        delta = mid - span / 2.0
        if where == "top":
            theta = -math.pi / 2 + delta
            px, py = cx + r_base * math.cos(theta), cy + r_base * math.sin(theta)
        else:
            theta = math.pi / 2 + delta
            px, py = cx + r_base * math.cos(theta), cy + r_base * math.sin(theta)
        rot = delta
        cosr, sinr = math.cos(rot), math.sin(rot)
        # T(P) * R(rot) * S(sc) * T(-adv/2, -100)
        a = cosr * sc
        b = sinr * sc
        c = -sinr * sc
        d = cosr * sc
        e = px + cosr * sc * (-(adv - st["tr"] * tracking) / 2.0) - sinr * sc * (-100)
        f = py + sinr * sc * (-(adv - st["tr"] * tracking) / 2.0) + cosr * sc * (-100)
        gp = g.transform(a, b, c, d, e, f)
        out = gp if out is None else pathops.op(out, gp, pathops.PathOp.UNION)
        acc += adv
    return out


def rot_about(path, deg, cx=128.0, cy=128.0):
    r = math.radians(deg)
    cosr, sinr = math.cos(r), math.sin(r)
    e = cx - cosr * cx + sinr * cy
    f = cy - sinr * cx - cosr * cy
    return path.transform(cosr, sinr, -sinr, cosr, e, f)


def symbol_crest(mono=False, ring_text=True):
    """G «ГЕРБ»: круглый клубный герб — кольцо с леттерингом по дуге,
    фактура скошенного поля, мяч-панель над штангой."""
    cx = cy = 128.0
    ring = dif(circle(cx, cy, 126), circle(cx, cy, 102))
    hair = dif(circle(cx, cy, 105), circle(cx, cy, 102))
    top = arc_text("М-ТРЕНИНГ", "pulse", 17, 114 - 8.5, "top")
    bot = arc_text("ШКОЛА СИЛОВОГО ТРЕНИНГА", "pulse", 12, 114 + 6.0, "bottom",
                   tracking=0.7)
    sep_l = pentagon(cx - 114, cy, 7)
    sep_r = pentagon(cx + 114, cy, 7)
    field = circle(cx, cy, 102)
    stripes = []
    for i in range(-4, 5):
        stripes.append(rect(cx - 160 + i * 32, cy - 160, 14, 320))
    stripes = itr(rot_about(uni(*stripes), -18), field)
    # штанга под наклоном (масштаб 0.88 от центра, чтобы не касаться кольца)
    bar = rect(cx - 65, cy + 30, 130, 10)
    plate_l = rounded_rect(cx - 81, cy + 10, 16, 50, 6)
    plate_r = rounded_rect(cx + 65, cy + 10, 16, 50, 6)
    col_l = rect(cx - 61, cy + 19, 6, 32)
    col_r = rect(cx + 55, cy + 19, 6, 32)
    bar_all = rot_about(uni(bar, plate_l, plate_r), -14)
    collars = rot_about(uni(col_l, col_r), -14)
    # мяч с панелью и пятью швами
    bcx, bcy, br = cx, cy - 18, 46
    ball = circle(bcx, bcy, br)
    panel = pentagon(bcx, bcy, 18)
    seams = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        p0 = (bcx + 33 * ux, bcy + 33 * uy)
        p1 = (bcx + (br + 2) * ux, bcy + (br + 2) * uy)
        seams.append(poly([(p0[0] + nx * 3.2, p0[1] + ny * 3.2),
                           (p1[0] + nx * 5.0, p1[1] + ny * 5.0),
                           (p1[0] - nx * 5.0, p1[1] - ny * 5.0),
                           (p0[0] - nx * 3.2, p0[1] - ny * 3.2)]))
    seams = itr(uni(*seams), ball)
    if mono:
        parts = [ring, hair, bar_all, collars,
                 dif(ball, circle(bcx, bcy, br - 9)), panel, seams]
        if ring_text:
            parts += [top, bot, sep_l, sep_r]
        one = uni(*parts)
        return {
            "shapes": [(to_d(one), "main")],
            "bbox": (2, 2, 254, 254),
            "baseline": 254,
            "name": "ГЕРБ",
            "letter": "G",
            "idea": "",
        }
    return {
        "shapes": [
            (to_d(ring), "ring"),
            (to_d(uni(top, bot)), "text"),
            (to_d(uni(sep_l, sep_r)), "accent"),
            (to_d(field), "field"),
            (to_d(stripes), "stripe"),
            (to_d(hair), "accent"),
            (to_d(bar_all), "metal"),
            (to_d(collars), "accent"),
            (to_d(dif(ball, panel)), "ball"),
            (to_d(uni(panel, seams)), "accent"),
        ],
        "bbox": (2, 2, 254, 254),
        "baseline": 254,
        "name": "ГЕРБ",
        "letter": "G",
        "idea": "Круглый клубный герб: кольцо с леттерингом по дуге, фактура "
                "скошенного поля, мяч-панель над штангой — клубный характер "
                "и силовая суть в одной эмблеме.",
    }


def symbol_strike():
    """H «УДАР»: мяч-М в момент удара — диагональное поле, вспышка, штрихи."""
    cx = cy = 128.0
    field = rot_about(rounded_rect(cx - 118, cy - 74, 236, 148, 46), -10)
    burst = []
    for i in range(8):
        a = math.radians(i * 45 + 22)
        bx, by = cx + 34, cy - 26
        burst.append(poly([(bx + 58 * math.cos(a) - 6 * math.sin(a),
                            by + 58 * math.sin(a) + 6 * math.cos(a)),
                           (bx + 92 * math.cos(a), by + 92 * math.sin(a)),
                           (bx + 58 * math.cos(a) + 6 * math.sin(a),
                            by + 58 * math.sin(a) - 6 * math.cos(a))]))
    burst = uni(*burst)
    ball = circle(cx - 12, cy - 6, 72)
    m = solid_m(cx - 12 - 41, cy - 6 - 31, cy - 6 + 31, 82, 18, apex_flat=0.09)
    seams = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        ux, uy = math.cos(a), math.sin(a)
        nx, ny = -uy, ux
        p0 = (cx - 12 + 54 * ux, cy - 6 + 54 * uy)
        p1 = (cx - 12 + 74 * ux, cy - 6 + 74 * uy)
        seams.append(poly([(p0[0] + nx * 4.5, p0[1] + ny * 4.5),
                           (p1[0] + nx * 7.0, p1[1] + ny * 7.0),
                           (p1[0] - nx * 7.0, p1[1] - ny * 7.0),
                           (p0[0] - nx * 4.5, p0[1] - ny * 4.5)]))
    seams = itr(uni(*seams), ball)
    ballbody = dif(ball, m)
    streaks = []
    for i, (yy, ln) in enumerate(((cy - 44, 74), (cy - 6, 104), (cy + 32, 60))):
        streaks.append(poly([(cx - 118, yy), (cx - 118 + ln, yy - 7),
                             (cx - 118 + ln, yy + 1), (cx - 118, yy + 8)]))
    streaks = rot_about(uni(*streaks), -10)
    return {
        "shapes": [
            (to_d(field), "field"),
            (to_d(burst), "burst"),
            (to_d(streaks), "accent"),
            (to_d(ballbody), "ball"),
            (to_d(seams), "accent"),
        ],
        "bbox": (8, 26, 248, 230),
        "baseline": 208,
        "name": "УДАР",
        "letter": "H",
        "idea": "Мяч-М в момент удара: диагональное поле, вспышка за мячом и "
                "три штриха скорости — движение и сила без единого слова.",
    }


# ================================================================ РАУНД 4: ЭВОЛЮЦИЯ ИСХОДНОГО ЗНАКА
def arc_pts(cx, cy, r, a0, a1, n=14):
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def banana(cx, cy, r, a0, a1, w):
    """Панель мяча — толстая дуга со скруглёнными торцами."""
    return stroke_polyline(arc_pts(cx, cy, r, a0, a1), w, "round", "round", 4)


def rounded_pentagon(cx, cy, r, w=9, rot=-12):
    pts = pentagon_pts(cx, cy, r)
    if rot:
        pts = [(cx + (p[0] - cx) * math.cos(math.radians(rot)) -
                 (p[1] - cy) * math.sin(math.radians(rot)),
                cy + (p[0] - cx) * math.sin(math.radians(rot)) +
                 (p[1] - cy) * math.cos(math.radians(rot))) for p in pts]
    p = stroke_polyline(pts + [pts[0]], w, "round", "round", 4)
    return uni(p, poly(pts))


def boat(scale=1.0):
    """Парусник: ровная мачта, два паруса с ветровым изгибом, два флажка."""
    hull = poly([(-38, -2), (34, -2), (24, 14), (-28, 14)])
    mast = rect(-2, -60, 4, 60)
    main_s = pathops.Path()
    pen = main_s.getPen()
    pen.moveTo((3, -56))
    pen.qCurveTo((30, -40), (34, -6))
    pen.lineTo((3, -6))
    pen.closePath()
    jib = pathops.Path()
    pen = jib.getPen()
    pen.moveTo((-3, -48))
    pen.qCurveTo((-25, -32), (-29, -6))
    pen.lineTo((-3, -6))
    pen.closePath()
    flag_top = poly([(2, -60), (16, -55), (2, -50)])
    flag_stern = poly([(-36, -2), (-50, -9), (-36, -16)])
    b = uni(hull, mast, main_s, jib, flag_top, flag_stern)
    if scale != 1.0:
        b = b.transform(scale, 0, 0, scale, 0, 0)
    return b


def symbol_regata():
    """J «РЕГАТА»: эволюция исходного знака — сфера мяча с чистыми панелями,
    одна орбита-волна (заострённые концы) и парусник с ровной мачтой."""
    bx, by, br = 108, 152, 78
    panels = [rounded_pentagon(bx, by, 30, w=7)]
    for i in range(5):                      # средний пояс панелей
        a = -90 + i * 72
        panels.append(banana(bx, by, 54, a - 17, a + 17, 24))
    for i in range(5):                      # крайний пояс, в шахматном порядке
        a = -54 + i * 72
        panels.append(banana(bx, by, 75, a - 22, a + 22, 8))
    ball = itr(uni(*panels), circle(bx, by, br))
    # орбита-волна: лента с заострёнными концами, левое крыло -> волна под boat
    wave = pathops.Path()
    pen = wave.getPen()
    pen.moveTo((14, 142))
    pen.qCurveTo((52, 40), (126, 36))
    pen.qCurveTo((190, 34), (210, 64))
    pen.qCurveTo((190, 52), (126, 54))
    pen.qCurveTo((60, 58), (14, 142))
    pen.closePath()
    bt = boat(0.85)
    bt = bt.transform(1, 0, 0, 1, 188, 56)
    return {
        "shapes": [(to_d(ball), "main"), (to_d(wave), "accent"),
                   (to_d(bt), "main")],
        "bbox": (14, 6, 240, 230),
        "baseline": 230,
        "name": "РЕГАТА",
        "letter": "J",
        "idea": "Эволюция исходного знака: сфера мяча с чистыми панелями, одна "
                "орбита, которая становится волной, и парусник с ровной мачтой "
                "на её крыле. Ничего лишнего, ничего кривого.",
    }


def symbol_sailpanel():
    """K «ПАНЕЛЬ-ПАРУС»: мяч, у которого центральная панель — парусник."""
    cx = cy = 128.0
    r = 104.0
    cuts = [banana(cx, cy, 66, a - 20, a + 20, 15) for a in (-90, -18, 54, 126, 198)]
    bt = boat(1.05)
    bt = bt.transform(1, 0, 0, 1, cx, cy + 16)
    body = dif(circle(cx, cy, r), uni(*cuts))
    return {
        "shapes": [(to_d(body), "main"), (to_d(bt), "accent")],
        "bbox": (24, 24, 232, 232),
        "baseline": 232,
        "name": "ПАНЕЛЬ-ПАРУС",
        "letter": "K",
        "idea": "Мяч, у которого центральная панель вырублена силуэтом "
                "парусника: два героя старого знака сплавлены в одну фигуру.",
    }


def symbol_small_sail():
    """Упрощённый знак для 16-48 px: мяч с вырубным парусом."""
    cx = cy = 128.0
    sail = pathops.Path()
    pen = sail.getPen()
    pen.moveTo((cx - 6, cy - 62))
    pen.qCurveTo((cx + 40, cy - 34), (cx + 46, cy + 20))
    pen.lineTo((cx - 6, cy + 20))
    pen.closePath()
    hull = rect(cx - 40, cy + 30, 84, 16)
    return {"shapes": [(to_d(dif(dif(circle(cx, cy, 104), sail), hull)), "main")],
            "bbox": (24, 24, 232, 232), "baseline": 232, "name": "М", "letter": "M",
            "idea": ""}


def boat3(scale=1.0):
    """Трёхпарусный парусник исходного знака, но поставленный ровно:
    горизонтальный корпус, две вертикальные мачты, три паруса, три флажка."""
    hull = poly([(-42, 0), (38, 0), (27, 15), (-31, 15)])
    mast_f = rect(-12, -64, 4, 66)
    mast_a = rect(14, -42, 4, 44)
    main_s = pathops.Path()
    pen = main_s.getPen()
    pen.moveTo((-7, -60))
    pen.qCurveTo((18, -42), (22, -6))
    pen.lineTo((-7, -6))
    pen.closePath()
    jib = pathops.Path()
    pen = jib.getPen()
    pen.moveTo((-10, -52))
    pen.qCurveTo((-34, -34), (-37, -6))
    pen.lineTo((-10, -6))
    pen.closePath()
    mizzen = pathops.Path()
    pen = mizzen.getPen()
    pen.moveTo((19, -38))
    pen.qCurveTo((34, -24), (36, -4))
    pen.lineTo((19, -4))
    pen.closePath()
    flag_f = poly([(-10, -64), (4, -59), (-10, -54)])
    flag_a = poly([(16, -42), (28, -38), (16, -34)])
    flag_stern = poly([(-40, 2), (-54, -6), (-40, -10)])
    b = uni(hull, mast_f, mast_a, main_s, jib, mizzen, flag_f, flag_a, flag_stern)
    if scale != 1.0:
        b = b.transform(scale, 0, 0, scale, 0, 0)
    return b


def symbol_orbita():
    """L «ОРБИТА»: исходный знак школы, пересобранный по правилам. Та же
    грамматика — мяч, две дуги орбиты, парусник на орбите, леттеринг ниже —
    но панели по правильной сетке с вертикальным пентагоном, дуги одной
    толщины со скруглёнными концами, мачты строго вертикальны."""
    bx, by, br = 128, 150, 86
    panels = [rounded_pentagon(bx, by, 33, w=9, rot=0)]
    for i in range(5):                      # средний пояс панелей
        a = -90 + i * 72
        panels.append(banana(bx, by, 59, a - 15, a + 15, 25))
    for i in range(5):                      # крайний пояс, в шахматном порядке
        a = -54 + i * 72
        panels.append(banana(bx, by, 81, a - 20, a + 20, 9))
    ball = itr(uni(*panels), circle(bx, by, br))
    orbit_a = banana(bx, by, 112, 185, 285, 10)    # левое верхнее крыло орбиты
    orbit_b = banana(bx, by, 112, -25, 45, 10)     # правое крыло
    bt = boat3(0.88)
    bt = bt.transform(1, 0, 0, 1, 204, 72)
    return {
        "shapes": [(to_d(ball), "main"), (to_d(uni(orbit_a, orbit_b)), "accent"),
                   (to_d(bt), "main")],
        "bbox": (11, 13, 243, 243),
        "baseline": 243,
        "name": "ОРБИТА",
        "letter": "L",
        "idea": "Исходный знак школы, пересобранный по правилам: мяч, две дуги "
                "орбиты и трёхпарусник — мачты вертикальны, панели по сетке.",
    }


def symbol_horizont():
    """M «ГОРИЗОНТ»: мяч всходит над ватерлинией, яхта идёт рядом по воде,
    дуга орбиты — над мячом. Старые герои в спокойной горизонтальной
    композиции: сильная базовая линия, ничего наклонного."""
    bx, by, br = 100, 126, 74
    panels = [rounded_pentagon(bx, by, 29, w=8, rot=0)]
    for i in range(5):                      # средний пояс панелей
        a = -90 + i * 72
        panels.append(banana(bx, by, 51, a - 15, a + 15, 23))
    for i in range(5):                      # крайний пояс, в шахматном порядке
        a = -54 + i * 72
        panels.append(banana(bx, by, 70, a - 19, a + 19, 8))
    ball = itr(uni(*panels), circle(bx, by, br))
    handle = banana(bx, by, 79, 215, 325, 18)     # рукоять гири = дуга орбиты
    ball = uni(ball, handle)
    bar = stroke_polyline([(16, 198), (240, 198)], 10, "round", "round", 1)
    pl_l = rounded_rect(6, 176, 11, 44, 5)        # диски штанги на торцах грифа
    pl_r = rounded_rect(239, 176, 11, 44, 5)
    barbell = uni(bar, pl_l, pl_r)
    bt = boat3(0.75)
    bt = bt.transform(1, 0, 0, 1, 204, 184)
    return {
        "shapes": [(to_d(ball), "main"),
                   (to_d(barbell), "accent"),
                   (to_d(bt), "main")],
        "bbox": (6, 38, 250, 220),
        "baseline": 220,
        "name": "ГОРИЗОНТ",
        "letter": "M",
        "idea": "Мяч-гиря всходит над штангой-ватерлинией: рукоять-орбита, "
                "гриф с дисками, яхта рядом — футбол и силовой тренинг "
                "в одной спокойной композиции.",
    }


# ================================================================ РАУНД 9: ГЕРБЫ
BLUE_LITE = "#6E8CFF"
GOLD = "#F2C230"
GOLD_LITE = "#FFE28A"
GOLD_DEEP = "#C08A00"


def shield_base():
    p = pathops.Path()
    pen = p.getPen()
    pen.moveTo((40, 40))
    pen.lineTo((216, 40))
    pen.lineTo((216, 118))
    pen.qCurveTo((216, 192), (128, 238))
    pen.qCurveTo((40, 192), (40, 118))
    pen.closePath()
    return p


def _scaled(p, s, cx=128.0, cy=132.0):
    return p.transform(s, 0, 0, s, cx * (1 - s), cy * (1 - s))


def gem_ball(cx, cy, r):
    """Гранёный мяч-кристалл: пентагон-ядро и два пояса фасетов с зазорами."""
    out = []
    core = poly(pentagon_pts(cx, cy, r * 0.40))
    out.append((to_d(core), "white"))
    for i in range(5):                     # средний пояс фасетов
        a0 = -90 + i * 72 + 4
        a1 = -90 + (i + 1) * 72 - 4
        pts = arc_pts(cx, cy, r * 0.46, a0, a1, 2) + arc_pts(cx, cy, r * 0.74, a1, a0, 2)
        out.append((to_d(poly(pts)), "lite"))
    for i in range(5):                     # внешний пояс, в шахматном порядке
        a0 = -54 + i * 72 + 4
        a1 = -54 + (i + 1) * 72 - 4
        pts = arc_pts(cx, cy, r * 0.80, a0, a1, 2) + arc_pts(cx, cy, r * 1.0, a1, a0, 2)
        out.append((to_d(poly(pts)), "dark"))
    return out


def star5(cx, cy, r):
    pts = []
    for i in range(10):
        rr = r if i % 2 == 0 else r * 0.46
        a = math.pi / 5 * i - math.pi / 2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return poly(pts)


def symbol_gem_shield():
    """N «КРИСТАЛЛ»: клубный щит с гранёным мячом-кристаллом, звездой и шевроном."""
    sh = shield_base()
    shapes = [(to_d(sh), "gold"),
              (to_d(_scaled(sh, 0.945)), "dark"),
              (to_d(_scaled(sh, 0.86)), "main")]
    field = _scaled(sh, 0.86)
    shapes += gem_ball(128, 122, 50)
    shapes.append((to_d(star5(128, 56, 11)), "gold"))
    chev = poly([(52, 196), (128, 168), (204, 196), (204, 212), (128, 184), (52, 212)])
    shapes.append((to_d(itr(chev, field)), "gold"))
    return {
        "shapes": shapes,
        "bbox": (40, 40, 216, 238),
        "baseline": 238,
        "name": "КРИСТАЛЛ",
        "letter": "N",
        "idea": "Клубный щит с двойным кантом: гранёный мяч-кристалл, звезда и "
                "золотой шеврон — объём через фасеты, как у профессиональных клубов.",
    }


def symbol_mono_shield():
    """P «МОНОГРАММА»: щит с монументальной золотой «М», в седле которой — кристалл."""
    sh = shield_base()
    shapes = [(to_d(sh), "gold"),
              (to_d(_scaled(sh, 0.945)), "dark"),
              (to_d(_scaled(sh, 0.86)), "main")]
    field = _scaled(sh, 0.86)
    m = solid_m(64, 78, 150, 128, 26, apex_flat=0.10)
    shadow = m.transform(1, 0, 0, 1, 5, 5)
    shapes.append((to_d(shadow), "gold2"))
    shapes.append((to_d(m), "gold"))
    shapes.append((to_d(circle(128, 116, 36)), "dark"))
    shapes += [(d, r) for d, r in gem_ball(128, 116, 30)]
    chev = poly([(52, 196), (128, 170), (204, 196), (204, 212), (128, 186), (52, 212)])
    shapes.append((to_d(itr(chev, field)), "gold"))
    return {
        "shapes": shapes,
        "bbox": (40, 40, 216, 238),
        "baseline": 238,
        "name": "МОНОГРАММА",
        "letter": "P",
        "idea": "Щит с монументальной золотой «М» в два тона; в её седле — "
                "гранёный мяч-кристалл: буква школы держит игру.",
    }


def symbol_mane_roundel():
    """Q «ГРИВА»: круглый значок — гранёный мяч в золотой гриве из языков пламени."""
    shapes = [(to_d(circle(128, 128, 104)), "gold"),
              (to_d(circle(128, 128, 96)), "dark"),
              (to_d(circle(128, 128, 84)), "main")]
    spikes = []
    for i in range(12):
        a = math.radians(i * 30 + 15)
        tip = (128 + 84 * math.cos(a), 128 + 84 * math.sin(a))
        b0 = (128 + 46 * math.cos(a - 0.20), 128 + 46 * math.sin(a - 0.20))
        b1 = (128 + 46 * math.cos(a + 0.20), 128 + 46 * math.sin(a + 0.20))
        spikes.append(poly([b0, tip, b1]))
    mane = uni(*spikes)
    shapes.append((to_d(itr(mane, circle(128, 128, 84))), "gold"))
    shapes += gem_ball(128, 128, 54)
    return {
        "shapes": shapes,
        "bbox": (24, 24, 232, 232),
        "baseline": 232,
        "name": "ГРИВА",
        "letter": "Q",
        "idea": "Круглый значок: гранёный мяч в золотой гриве-пламени — сила и "
                "скорость, читается как эмблема клуба с любого расстояния.",
    }


def symbol_gem_small():
    """Упрощённый знак 16-48 px: гранёный мяч с зазорами-швами."""
    shapes = gem_ball(128, 128, 104)
    return {"shapes": [(d, "main") for d, _ in shapes],
            "bbox": (24, 24, 232, 232), "baseline": 232,
            "name": "КРИСТАЛЛ-МИНИ", "letter": "n", "idea": ""}


PAL_FULL = {"main": BLUE, "lite": BLUE_LITE, "dark": DEEP, "gold": GOLD,
            "gold2": GOLD_DEEP, "white": "#FFFFFF", "wm": BLUE}


def _gem_cut(cx, cy, r):
    cuts = [poly(pentagon_pts(cx, cy, r * 0.40))]
    for i in range(5):
        a0 = -90 + i * 72 + 4
        a1 = -90 + (i + 1) * 72 - 4
        cuts.append(poly(arc_pts(cx, cy, r * 0.46, a0, a1, 2) +
                         arc_pts(cx, cy, r * 0.74, a1, a0, 2)))
        b0 = -54 + i * 72 + 4
        b1 = -54 + (i + 1) * 72 - 4
        cuts.append(poly(arc_pts(cx, cy, r * 0.80, b0, b1, 2) +
                         arc_pts(cx, cy, r * 1.0, b1, b0, 2)))
    return uni(*cuts)


def symbol_gem_shield_mono():
    """Моно-«КРИСТАЛЛ»: кант щита + поле, в котором кристалл, звезда и шеврон
    вырублены негативом — читается в один цвет на любом размере."""
    sh = shield_base()
    ring = dif(sh, _scaled(sh, 0.945))
    field = _scaled(sh, 0.86)
    chev = poly([(52, 196), (128, 168), (204, 196), (204, 212), (128, 184), (52, 212)])
    holes = uni(_gem_cut(128, 122, 50), star5(128, 56, 11), itr(chev, field))
    return {"shapes": [(to_d(ring), "main"), (to_d(dif(field, holes)), "main")],
            "bbox": (40, 40, 216, 238), "baseline": 238,
            "name": "КРИСТАЛЛ", "letter": "N", "idea": ""}


def symbol_mono_shield_mono():
    """Моно-«МОНОГРАММА»: кант, М, кристалл на тарелке и шеврон без поля."""
    sh = shield_base()
    ring = dif(sh, _scaled(sh, 0.945))
    m = solid_m(64, 78, 150, 128, 26, apex_flat=0.10)
    plate = dif(circle(128, 116, 36), _gem_cut(128, 116, 30))
    chev = poly([(52, 196), (128, 170), (204, 196), (204, 212), (128, 186), (52, 212)])
    return {"shapes": [(to_d(ring), "main"), (to_d(m), "main"),
                       (to_d(plate), "main"), (to_d(chev), "main")],
            "bbox": (40, 40, 216, 238), "baseline": 238,
            "name": "МОНОГРАММА", "letter": "P", "idea": ""}


def symbol_mane_roundel_mono():
    """Моно-«ГРИВА»: кольцо + диск, в котором языки пламени и кристалл вырублены."""
    ring = dif(circle(128, 128, 104), circle(128, 128, 96))
    spikes = []
    for i in range(12):
        a = math.radians(i * 30 + 15)
        tip = (128 + 84 * math.cos(a), 128 + 84 * math.sin(a))
        b0 = (128 + 46 * math.cos(a - 0.20), 128 + 46 * math.sin(a - 0.20))
        b1 = (128 + 46 * math.cos(a + 0.20), 128 + 46 * math.sin(a + 0.20))
        spikes.append(poly([b0, tip, b1]))
    field = circle(128, 128, 84)
    holes = uni(uni(*spikes), _gem_cut(128, 128, 54))
    return {"shapes": [(to_d(ring), "main"), (to_d(dif(field, holes)), "main")],
            "bbox": (24, 24, 232, 232), "baseline": 232,
            "name": "ГРИВА", "letter": "Q", "idea": ""}
