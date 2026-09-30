#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, "skills/logo-design/scripts")
sys.path.insert(0, "designs/m-trening/evo")
import render_png
from build_evo_v5 import build_ball_dome_v5, wm_main, wm_p, orb_uniform, orb_swoosh, orb_aero
from build_evo_v4 import build_tall_ship_v4

ball_paths = build_ball_dome_v5(cx=110.0, cy=186.0, R=102.0)
ship_a_solids, ship_a_hull = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style="classic")
ship_b_solids, ship_b_hull = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style="sail_m")
ship_c_solids, ship_c_hull = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style="wave_flow")

def render_logo_group(ball, orb, ship_solids, ship_hull, main_col, accent_col, include_wordmark=True):
    lines = []
    for p in ball:
        lines.append(f'<path fill="{main_col}" d="{p}"/>')
    for p in orb:
        lines.append(f'<path fill="{accent_col}" d="{p}"/>')
    for p in ship_solids:
        lines.append(f'<path fill="{accent_col}" d="{p}"/>')
    if ship_hull:
        lines.append(f'<path fill="{accent_col}" fill-rule="evenodd" d="{ship_hull}"/>')
    if include_wordmark:
        lines.append(f'<path fill="{main_col}" d="{wm_main}"/>')
        lines.append(f'<path fill="{main_col}" fill-rule="evenodd" d="{wm_p}"/>')
    return "\n".join(lines)

logo_a_white = render_logo_group(ball_paths, orb_uniform, ship_a_solids, ship_a_hull, "#FFFFFF", "#FFFFFF")
logo_b_white = render_logo_group(ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, "#FFFFFF", "#FFFFFF")
logo_b_coral = render_logo_group(ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, "#FFFFFF", "#FF5733")
logo_b_light = render_logo_group(ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, "#0F172A", "#D9381E")
logo_c_cyan  = render_logo_group(ball_paths, orb_aero, ship_c_solids, ship_c_hull, "#FFFFFF", "#38BDF8")
logo_c_white = render_logo_group(ball_paths, orb_aero, ship_c_solids, ship_c_hull, "#FFFFFF", "#FFFFFF")

# Build the 2400x1860 comprehensive presentation board:
board_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 1860" width="2400" height="1860">
  <defs>
    <style>
      .t-h1 {{ font-family: 'DejaVu Sans', sans-serif; font-size: 38px; font-weight: 700; fill: #FFFFFF; }}
      .t-sub {{ font-family: 'DejaVu Sans', sans-serif; font-size: 20px; fill: #94A3B8; }}
      .t-sec {{ font-family: 'DejaVu Sans', sans-serif; font-size: 16px; font-weight: 700; fill: #FF5733; letter-spacing: 2.5px; }}
      .t-card-title {{ font-family: 'DejaVu Sans', sans-serif; font-size: 25px; font-weight: 700; fill: #FFFFFF; }}
      .t-card-desc {{ font-family: 'DejaVu Sans', sans-serif; font-size: 16px; fill: #CBD5E1; }}
      .t-badge {{ font-family: 'DejaVu Sans', sans-serif; font-size: 14px; font-weight: 700; fill: #FFFFFF; letter-spacing: 1.2px; }}
      .t-dark {{ font-family: 'DejaVu Sans', sans-serif; font-size: 20px; font-weight: 700; fill: #0F172A; }}
      .t-dark-sm {{ font-family: 'DejaVu Sans', sans-serif; font-size: 15px; fill: #475569; }}
    </style>
    <linearGradient id="bgGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#070B14"/>
      <stop offset="100%" stop-color="#0B1120"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0F172A"/>
      <stop offset="100%" stop-color="#090D16"/>
    </linearGradient>
    <linearGradient id="jerseyDark" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#131C31"/>
      <stop offset="100%" stop-color="#070B14"/>
    </linearGradient>
    <linearGradient id="jerseyCoral" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#E03E22"/>
      <stop offset="100%" stop-color="#B82810"/>
    </linearGradient>
  </defs>

  <!-- Background -->
  <rect width="2400" height="1860" fill="url(#bgGrad)"/>

  <!-- Header -->
  <text x="80" y="78" class="t-sec">РЕДИЗАЙН И СТИЛИЗАЦИЯ ИСХОДНОГО ЛОГОТИПА · БЕЗ ЩИТОВ И РАМОК</text>
  <text x="80" y="130" class="t-h1">М-ТРЕНИНГ — Футбольная школа силового тренинга</text>
  <text x="80" y="168" class="t-sub">Лёгкий, воздушный и запоминающийся силуэт восходящего мяча, орбиты и парусника — специально для игровой формы и спортивного инвентаря</text>
  <line x1="80" y1="196" x2="2320" y2="196" stroke="#1E293B" stroke-width="2"/>

  <!-- ===================================================================== -->
  <!-- ROW 1: 3 EVOLUTIONARY VARIATIONS OF THE ORIGINAL LOGO (Y = 224..884)  -->
  <!-- ===================================================================== -->

  <!-- CARD A: Вариант A — Чистая Классика (Original Remaster) -->
  <g transform="translate(80, 224)">
    <rect width="714" height="650" rx="24" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="2"/>
    <rect x="28" y="24" width="210" height="32" rx="16" fill="#1E293B"/>
    <text x="133" y="45" text-anchor="middle" class="t-badge">ВАРИАНТ A · КЛАССИКА</text>

    <!-- Main Logo A (White on Pitch Black circle/stage) -->
    <rect x="44" y="76" width="380" height="380" rx="20" fill="#04060B" stroke="#1E293B" stroke-width="1.5"/>
    <g transform="translate(66, 98) scale(1.31)">
      {logo_a_white}
    </g>

    <!-- Secondary Preview: Light BG + Two-Tone -->
    <rect x="444" y="76" width="226" height="182" rx="16" fill="#FFFFFF"/>
    <g transform="translate(480, 90) scale(0.60)">
      {render_logo_group(ball_paths, orb_uniform, ship_a_solids, ship_a_hull, "#0F172A", "#D9381E")}
    </g>

    <rect x="444" y="274" width="226" height="182" rx="16" fill="#0B1325" stroke="#1E293B" stroke-width="1.5"/>
    <g transform="translate(480, 288) scale(0.60)">
      {render_logo_group(ball_paths, orb_uniform, ship_a_solids, ship_a_hull, "#FFFFFF", "#FF5733")}
    </g>

    <text x="36" y="502" class="t-card-title">A. «Чистая Классика» (Ремастеринг)</text>
    <text x="36" y="536" class="t-card-desc">• Бережная ювелирная огранка вашего исходного логотипа</text>
    <text x="36" y="564" class="t-card-desc">• Идеальная сфера мяча, ровные швы и 3 полных прямых паруса</text>
    <text x="36" y="592" class="t-card-desc">• Убрана мелкая паутина вант — чисто печатается в любом размере</text>
    <text x="36" y="620" class="t-card-desc">• Выверенный гео-гротеск «М-ТРЕНИНГ» со скруглёнными штрихами</text>
  </g>

  <!-- CARD B: Вариант B — Фирменный Парус-М (Signature Sail-M) -->
  <g transform="translate(843, 224)">
    <rect width="714" height="650" rx="24" fill="url(#cardGrad)" stroke="#FF5733" stroke-width="3"/>
    <rect x="28" y="24" width="310" height="32" rx="16" fill="#FF5733"/>
    <text x="183" y="45" text-anchor="middle" class="t-badge">ВАРИАНТ B · ФИРМЕННЫЙ ПАРУС-М ★</text>

    <!-- Main Logo B (White on Pitch Black stage) -->
    <rect x="44" y="76" width="380" height="380" rx="20" fill="#04060B" stroke="#1E293B" stroke-width="1.5"/>
    <g transform="translate(66, 98) scale(1.31)">
      {logo_b_white}
    </g>
    <!-- Callout circle highlighting the Sail-M -->
    <circle cx="326" cy="166" r="56" fill="none" stroke="#FF5733" stroke-width="2" stroke-dasharray="6,5"/>

    <!-- Secondary Preview: Light BG + Two-Tone -->
    <rect x="444" y="76" width="226" height="182" rx="16" fill="#FFFFFF"/>
    <g transform="translate(480, 90) scale(0.60)">
      {logo_b_light}
    </g>

    <rect x="444" y="274" width="226" height="182" rx="16" fill="#0B1325" stroke="#1E293B" stroke-width="1.5"/>
    <g transform="translate(480, 288) scale(0.60)">
      {logo_b_coral}
    </g>

    <text x="36" y="502" class="t-card-title">B. «Фирменный Парус-М» (С изюминкой)</text>
    <text x="36" y="536" class="t-card-desc">• Паруса кораблика надуты ветром в форме стильной буквы «М»</text>
    <text x="36" y="564" class="t-card-desc">• Уникальная деталь, которую сразу замечают и запоминают дети и родители</text>
    <text x="36" y="592" class="t-card-desc">• Орбита решена стремительным спортивным росчерком (Swoosh)</text>
    <text x="36" y="620" class="t-card-desc">• Сохраняет 100% родной композиции, делая её эксклюзивной</text>
  </g>

  <!-- CARD C: Вариант C — Скоростной Импульс (Aero Flow) -->
  <g transform="translate(1606, 224)">
    <rect width="714" height="650" rx="24" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="2"/>
    <rect x="28" y="24" width="240" height="32" rx="16" fill="#0284C7"/>
    <text x="148" y="45" text-anchor="middle" class="t-badge">ВАРИАНТ C · АЭРО-ПОТОК</text>

    <!-- Main Logo C -->
    <rect x="44" y="76" width="380" height="380" rx="20" fill="#04060B" stroke="#1E293B" stroke-width="1.5"/>
    <g transform="translate(66, 98) scale(1.31)">
      {logo_c_white}
    </g>

    <!-- Secondary Preview: Light BG + Two-Tone Cyan -->
    <rect x="444" y="76" width="226" height="182" rx="16" fill="#FFFFFF"/>
    <g transform="translate(480, 90) scale(0.60)">
      {render_logo_group(ball_paths, orb_aero, ship_c_solids, ship_c_hull, "#0F172A", "#0284C7")}
    </g>

    <rect x="444" y="274" width="226" height="182" rx="16" fill="#0B1325" stroke="#1E293B" stroke-width="1.5"/>
    <g transform="translate(480, 288) scale(0.60)">
      {logo_c_cyan}
    </g>

    <text x="36" y="502" class="t-card-title">C. «Скоростной Импульс» (Aero Flow)</text>
    <text x="36" y="536" class="t-card-desc">• Лаконичный обтекаемый корпус яхты в едином потоке с орбитой</text>
    <text x="36" y="564" class="t-card-desc">• Упругие паруса-крылья и заострённые динамические дуги</text>
    <text x="36" y="592" class="t-card-desc">• Максимальная читаемость при термотрансфере и мелкой вышивке</text>
    <text x="36" y="620" class="t-card-desc">• Отлично работает с двухцветным неоново-голубым или коралловым акцентом</text>
  </g>

  <!-- ===================================================================== -->
  <!-- ROW 2: FOOTBALL JERSEYS & TRAINING INVENTORY MOCKUPS (Y = 916..1800)  -->
  <!-- ===================================================================== -->
  <text x="80" y="942" class="t-sec">ПРИМЕНЕНИЕ НА ФУТБОЛЬНОЙ ФОРМЕ И СИЛОВОМ ИНВЕНТАРЕ ШКОЛЫ</text>
  <text x="80" y="982" class="t-h1" style="font-size: 30px;">Открытый силуэт без щита «дышит» на ткани формы и легко узнаётся с трибун</text>

  <!-- 1. HOME JERSEY & FULL-CHEST TRAINING TEE CARD (X = 80, Y = 1010, W = 1100, H = 780) -->
  <g transform="translate(80, 1010)">
    <rect width="1100" height="780" rx="24" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="2"/>
    <text x="40" y="48" class="t-card-title">Игровая и тренировочная форма «М-ТРЕНИНГ»</text>
    <text x="40" y="78" class="t-card-desc">Слева — домашняя джерси (эмблема на сердце + крупный знак), справа — гостевая белая джерси</text>

    <!-- HOME JERSEY (DARK NAVY / PITCH BLACK) -->
    <g transform="translate(55, 115)">
      <!-- Jersey Silhouette -->
      <path d="M 145,20 L 205,0 L 295,0 L 355,20 L 465,95 L 420,185 L 355,145 L 355,530 C 355,542 345,550 330,550 L 170,550 C 155,550 145,542 145,530 L 145,145 L 80,185 L 35,95 Z"
            fill="url(#jerseyDark)" stroke="#334155" stroke-width="2.5"/>
      <!-- Collar V-Neck -->
      <path d="M 205,0 L 250,48 L 295,0" fill="none" stroke="#FF5733" stroke-width="6" stroke-linejoin="round"/>
      <!-- Sleeve Cuffs -->
      <path d="M 40,102 L 84,180" stroke="#FF5733" stroke-width="6"/>
      <path d="M 460,102 L 416,180" stroke="#FF5733" stroke-width="6"/>
      <!-- Subtle Speed Stripes on Jersey Body -->
      <path d="M 145,420 Q 250,360 355,400" fill="none" stroke="#1E293B" stroke-width="2"/>
      <path d="M 145,450 Q 250,390 355,430" fill="none" stroke="#1E293B" stroke-width="2"/>

      <!-- Left-Chest Crest (Heart Position: viewer's right x=275, y=92) -->
      <g transform="translate(268, 86) scale(0.24)">
        {logo_b_coral}
      </g>
      <!-- Right-Chest Number / Brand Tag -->
      <text x="182" y="132" font-family="DejaVu Sans" font-size="22" font-weight="700" fill="#FF5733">10</text>

      <!-- Center-Chest Training Print (Airy open silhouette right on fabric!) -->
      <g transform="translate(164, 200) scale(0.68)" opacity="0.96">
        {logo_b_white}
      </g>

      <text x="250" y="595" text-anchor="middle" class="t-card-desc" style="fill:#FFFFFF; font-weight:700;">Домашняя / Тренировочная (Pitch Navy)</text>
      <text x="250" y="620" text-anchor="middle" class="t-card-desc">Белый знак + коралловая орбита без тяжёлой подложки</text>
    </g>

    <!-- AWAY JERSEY (CRISP WHITE) -->
    <g transform="translate(555, 115)">
      <!-- Jersey Silhouette -->
      <path d="M 145,20 L 205,0 L 295,0 L 355,20 L 465,95 L 420,185 L 355,145 L 355,530 C 355,542 345,550 330,550 L 170,550 C 155,550 145,542 145,530 L 145,145 L 80,185 L 35,95 Z"
            fill="#F8FAFC" stroke="#CBD5E1" stroke-width="2.5"/>
      <!-- Collar V-Neck -->
      <path d="M 205,0 L 250,48 L 295,0" fill="none" stroke="#0F172A" stroke-width="6" stroke-linejoin="round"/>
      <path d="M 213,0 L 250,38 L 287,0" fill="none" stroke="#D9381E" stroke-width="3" stroke-linejoin="round"/>
      <!-- Sleeve Cuffs -->
      <path d="M 40,102 L 84,180" stroke="#0F172A" stroke-width="6"/>
      <path d="M 460,102 L 416,180" stroke="#0F172A" stroke-width="6"/>

      <!-- Left-Chest Crest -->
      <g transform="translate(268, 86) scale(0.24)">
        {logo_b_light}
      </g>
      <text x="182" y="132" font-family="DejaVu Sans" font-size="22" font-weight="700" fill="#0F172A">10</text>

      <!-- Center-Chest Print -->
      <g transform="translate(164, 200) scale(0.68)">
        {logo_b_light}
      </g>

      <text x="250" y="595" text-anchor="middle" class="t-card-desc" style="fill:#FFFFFF; font-weight:700;">Гостевая форма (Crisp White)</text>
      <text x="250" y="620" text-anchor="middle" class="t-card-desc">Глубокий тёмно-синий + огненно-коралловый парусник</text>
    </g>
  </g>

  <!-- 2. STRENGTH & FOOTBALL TRAINING EQUIPMENT CARD (X = 1220, Y = 1010, W = 1100, H = 780) -->
  <g transform="translate(1220, 1010)">
    <rect width="1100" height="780" rx="24" fill="url(#cardGrad)" stroke="#1E293B" stroke-width="2"/>
    <text x="40" y="48" class="t-card-title">Силовой и футбольный инвентарь школы</text>
    <text x="40" y="78" class="t-card-desc">Гири, медболы, бутылки, рюкзаки и клубные мячи — лаконичный трафаретный силуэт без мелких деталей</text>

    <!-- ITEM 1: KETTLEBELL / СИЛОВАЯ ГИРЯ (X = 50, Y = 120) -->
    <g transform="translate(50, 120)">
      <rect width="310" height="470" rx="20" fill="#060911" stroke="#1E293B" stroke-width="1.5"/>
      <!-- Kettlebell Handle & Body -->
      <path d="M 95,125 C 95,55 215,55 215,125" fill="none" stroke="#334155" stroke-width="26" stroke-linecap="round"/>
      <path d="M 95,125 C 95,55 215,55 215,125" fill="none" stroke="#475569" stroke-width="18" stroke-linecap="round"/>
      <circle cx="155" cy="245" r="112" fill="#111827" stroke="#334155" stroke-width="3"/>
      <!-- Flat base of kettlebell -->
      <path d="M 85,332 L 225,332 L 210,352 L 100,352 Z" fill="#1E293B"/>
      <!-- Coral Weight Ring -->
      <path d="M 102,140 Q 155,152 208,140" fill="none" stroke="#FF5733" stroke-width="5"/>
      <!-- Logo printed on Kettlebell -->
      <g transform="translate(86, 174) scale(0.54)">
        {logo_b_white}
      </g>
      <text x="155" y="405" text-anchor="middle" class="t-card-desc" style="fill:#FFFFFF; font-weight:700;">Силовые гири и медболы</text>
      <text x="155" y="432" text-anchor="middle" class="t-card-desc" style="font-size:14px;">1-цветная трафаретная печать</text>
    </g>

    <!-- ITEM 2: SPORTS WATER BOTTLE & SHAKER (X = 395, Y = 120) -->
    <g transform="translate(395, 120)">
      <rect width="310" height="470" rx="20" fill="#060911" stroke="#1E293B" stroke-width="1.5"/>
      <!-- Bottle Cap & Spout -->
      <rect x="135" y="34" width="40" height="20" rx="6" fill="#FF5733"/>
      <rect x="110" y="52" width="90" height="28" rx="8" fill="#1E293B" stroke="#334155" stroke-width="2"/>
      <!-- Bottle Body -->
      <rect x="92" y="80" width="126" height="275" rx="22" fill="#0F172A" stroke="#334155" stroke-width="2.5"/>
      <line x1="92" y1="125" x2="218" y2="125" stroke="#FF5733" stroke-width="3"/>
      <!-- Logo on Bottle -->
      <g transform="translate(104, 155) scale(0.40)">
        {logo_b_coral}
      </g>
      <text x="155" y="405" text-anchor="middle" class="t-card-desc" style="fill:#FFFFFF; font-weight:700;">Бутылки и шейкеры</text>
      <text x="155" y="432" text-anchor="middle" class="t-card-desc" style="font-size:14px;">Стойкая УФ-печать по пластику/металлу</text>
    </g>

    <!-- ITEM 3: TRAINING GYM BAG / КОНУСЫ И МЯЧИ (X = 740, Y = 120) -->
    <g transform="translate(740, 120)">
      <rect width="310" height="470" rx="20" fill="#060911" stroke="#1E293B" stroke-width="1.5"/>
      <!-- Training Backpack / Drawstring Bag -->
      <path d="M 85,75 C 85,55 225,55 225,75 L 240,325 C 240,342 228,355 210,355 L 100,355 C 82,355 70,342 70,325 Z"
            fill="#111827" stroke="#334155" stroke-width="2.5"/>
      <!-- Drawstring Cords -->
      <line x1="90" y1="80" x2="65" y2="320" stroke="#FF5733" stroke-width="3"/>
      <line x1="220" y1="80" x2="245" y2="320" stroke="#FF5733" stroke-width="3"/>
      <!-- Top Handle -->
      <path d="M 130,62 C 130,36 180,36 180,62" fill="none" stroke="#475569" stroke-width="6"/>
      <!-- Logo on Bag -->
      <g transform="translate(91, 138) scale(0.50)">
        {logo_b_white}
      </g>
      <text x="155" y="405" text-anchor="middle" class="t-card-desc" style="fill:#FFFFFF; font-weight:700;">Рюкзаки, сумки и манишки</text>
      <text x="155" y="432" text-anchor="middle" class="t-card-desc" style="font-size:14px;">Вышивка и термотрансфер (флекс)</text>
    </g>

    <!-- Bottom Summary Strip inside Equipment Card -->
    <rect x="50" y="612" width="1000" height="128" rx="16" fill="#090D16" stroke="#1E293B" stroke-width="1.5"/>
    <!-- Small scale test icons: 64px, 40px, 28px -->
    <g transform="translate(80, 630) scale(0.36)">
      {logo_b_white}
    </g>
    <g transform="translate(195, 646) scale(0.24)">
      {logo_b_white}
    </g>
    <g transform="translate(275, 658) scale(0.16)">
      {logo_b_white}
    </g>
    <text x="350" y="662" class="t-card-title" style="font-size:21px;">Почему эта геометрия идеально работает на форме и инвентаре:</text>
    <text x="350" y="694" class="t-card-desc">1. Нет замкнутого щита — знак «дышит» за счёт цвета самой футболки или инвентаря.</text>
    <text x="350" y="720" class="t-card-desc">2. Увеличенные зазоры между гранями мяча и парусами не слипаются даже при размере 25 мм.</text>
  </g>
</svg>
'''

svg_out = "designs/m-trening/evo-board.svg"
png_out = "designs/m-trening/evo-board.png"
with open(svg_out, "w", encoding="utf-8") as f:
    f.write(board_svg)

render_png.render(svg_out, png_out, 2400, 1860, bg="#070B14")
# Also copy to brand-board.png so both paths have the latest presentation board
render_png.render(svg_out, "designs/m-trening/brand-board.png", 2400, 1860, bg="#070B14")
print("Rendered evo-board.png and brand-board.png")
