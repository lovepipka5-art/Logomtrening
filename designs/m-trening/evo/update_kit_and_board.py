#!/usr/bin/env python3
import os
import sys

sys.path.insert(0, "skills/logo-design/scripts")
sys.path.insert(0, "designs/m-trening/evo")
import render_png
from build_evo_v5 import build_ball_dome_v5, wm_main, wm_p, orb_uniform, orb_swoosh, orb_aero
from build_evo_v4 import build_tall_ship_v4

KIT_DIR = "designs/m-trening/kit"
EXP_DIR = os.path.join(KIT_DIR, "exports")
EVO_DIR = "designs/m-trening/evo"
os.makedirs(KIT_DIR, exist_ok=True)
os.makedirs(EXP_DIR, exist_ok=True)

NAVY = "#0F172A"
CORAL_LIGHT_BG = "#D9381E"  # 4.63:1 on #FFFFFF
CORAL_DARK_BG  = "#FF5733"  # 5.66:1 on #0F172A
CYAN_DARK_BG   = "#38BDF8"  # 8.20:1 on #0F172A
WHITE = "#FFFFFF"
BLACK = "#000000"

# Build the components for Variant B (Signature Sail-M) and Variant A (Original Remaster):
ball_paths = build_ball_dome_v5(cx=110.0, cy=186.0, R=102.0)
ship_a_solids, ship_a_hull = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style="classic")
ship_b_solids, ship_b_hull = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style="sail_m")
ship_c_solids, ship_c_hull = build_tall_ship_v4(ox=182.0, oy=62.0, angle_deg=32.0, style="wave_flow")

def render_symbol_paths(ball, orb, ship_solids, ship_hull, ball_color, accent_color):
    tags = []
    for p in ball:
        tags.append(f'    <path fill="{ball_color}" d="{p}"/>')
    for p in orb:
        tags.append(f'    <path fill="{accent_color}" d="{p}"/>')
    for p in ship_solids:
        tags.append(f'    <path fill="{accent_color}" d="{p}"/>')
    if ship_hull:
        tags.append(f'    <path fill="{accent_color}" fill-rule="evenodd" d="{ship_hull}"/>')
    return "\n".join(tags)

def make_lockup_svg(title, ball, orb, ship_solids, ship_hull, main_col, accent_col):
    sym_xml = render_symbol_paths(ball, orb, ship_solids, ship_hull, main_col, accent_col)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <g id="symbol">
{sym_xml}
  </g>
  <g id="wordmark">
    <path fill="{main_col}" d="{wm_main}"/>
    <path fill="{main_col}" fill-rule="evenodd" d="{wm_p}"/>
  </g>
</svg>
'''

def make_glyph_svg(title, ball, orb, ship_solids, ship_hull, main_col, accent_col):
    # Centered vertically in 256x256 by translating y +24
    sym_xml = render_symbol_paths(ball, orb, ship_solids, ship_hull, main_col, accent_col)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <g id="symbol" transform="translate(0, 24)">
{sym_xml}
  </g>
</svg>
'''

def make_horizontal_svg(title, ball, orb, ship_solids, ship_hull, main_col, accent_col):
    sym_xml = render_symbol_paths(ball, orb, ship_solids, ship_hull, main_col, accent_col)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 200" width="640" height="200" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <g id="symbol" transform="translate(16, -6) scale(0.92)">
{sym_xml}
  </g>
  <g id="wordmark" transform="translate(248, -198) scale(1.42)">
    <path fill="{main_col}" d="{wm_main}"/>
    <path fill="{main_col}" fill-rule="evenodd" d="{wm_p}"/>
  </g>
</svg>
'''

def make_wordmark_svg(title, main_col):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 120" width="520" height="120" role="img" aria-labelledby="title">
  <title id="title">{title}</title>
  <g id="wordmark" transform="translate(-6, -372) scale(2.0)">
    <path fill="{main_col}" d="{wm_main}"/>
    <path fill="{main_col}" fill-rule="evenodd" d="{wm_p}"/>
  </g>
</svg>
'''

# Save all 3 evolutionary variants in mono-white, mono-black, and 2-tone color in EVO_DIR:
variants = [
    ("evo-a", "Вариант A — Чистая Классика (Original Remaster)", orb_uniform, ship_a_solids, ship_a_hull),
    ("evo-b", "Вариант B — Фирменный Парус-М (Signature Sail-M)", orb_swoosh, ship_b_solids, ship_b_hull),
    ("evo-c", "Вариант C — Скоростной Импульс (Aero Flow)", orb_aero, ship_c_solids, ship_c_hull),
]

for code, label, orb, s_solids, s_hull in variants:
    # 1. Pure White on Dark
    svg_w = make_lockup_svg(f"М-ТРЕНИНГ — {label} (White)", ball_paths, orb, s_solids, s_hull, WHITE, WHITE)
    with open(os.path.join(EVO_DIR, f"{code}-white.svg"), "w", encoding="utf-8") as f:
        f.write(svg_w)
    # 2. Dark + Coral Accent
    svg_dc = make_lockup_svg(f"М-ТРЕНИНГ — {label} (Dark + Coral)", ball_paths, orb, s_solids, s_hull, WHITE, CORAL_DARK_BG)
    with open(os.path.join(EVO_DIR, f"{code}-dark-coral.svg"), "w", encoding="utf-8") as f:
        f.write(svg_dc)
    # 3. Light BG (Navy + Coral Accent)
    svg_lc = make_lockup_svg(f"М-ТРЕНИНГ — {label} (Light BG)", ball_paths, orb, s_solids, s_hull, NAVY, CORAL_LIGHT_BG)
    with open(os.path.join(EVO_DIR, f"{code}-light-coral.svg"), "w", encoding="utf-8") as f:
        f.write(svg_lc)

# Update the primary kit in designs/m-trening/kit/ with the evolved logo:
kit_files = {
    "logo-primary.svg": make_lockup_svg("М-ТРЕНИНГ — Основной логотип", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, NAVY, CORAL_LIGHT_BG),
    "logo-stacked.svg": make_lockup_svg("М-ТРЕНИНГ — Вертикальный логотип", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, NAVY, CORAL_LIGHT_BG),
    "logo-horizontal.svg": make_horizontal_svg("М-ТРЕНИНГ — Горизонтальный логотип", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, NAVY, CORAL_LIGHT_BG),
    "logo-glyph.svg": make_glyph_svg("М-ТРЕНИНГ — Знак", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, NAVY, CORAL_LIGHT_BG),
    "logo-wordmark.svg": make_wordmark_svg("М-ТРЕНИНГ — Текстовый знак", NAVY),
    "logo-inverted.svg": make_lockup_svg("М-ТРЕНИНГ — Инверсный логотип (для тёмной формы)", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, WHITE, CORAL_DARK_BG),
    "logo-mono-black.svg": make_lockup_svg("М-ТРЕНИНГ — Монохромный чёрный", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, BLACK, BLACK),
    "logo-mono-white.svg": make_lockup_svg("М-ТРЕНИНГ — Монохромный белый", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, WHITE, WHITE),
    # Also include Variant A (Classic Remaster) and Variant C (Aero Flow) directly in kit/ so the user has all 3 masters ready:
    "logo-classic-remaster-white.svg": make_lockup_svg("М-ТРЕНИНГ — Классический ремастеринг (Белый)", ball_paths, orb_uniform, ship_a_solids, ship_a_hull, WHITE, WHITE),
    "logo-classic-remaster-color.svg": make_lockup_svg("М-ТРЕНИНГ — Классический ремастеринг (Цветной)", ball_paths, orb_uniform, ship_a_solids, ship_a_hull, NAVY, CORAL_LIGHT_BG),
    "logo-aero-flow-white.svg": make_lockup_svg("М-ТРЕНИНГ — Скоростной Импульс (Белый)", ball_paths, orb_aero, ship_c_solids, ship_c_hull, WHITE, WHITE),
    "logo-aero-flow-color.svg": make_lockup_svg("М-ТРЕНИНГ — Скоростной Импульс (Цветной)", ball_paths, orb_aero, ship_c_solids, ship_c_hull, WHITE, CYAN_DARK_BG),
}

for fname, content in kit_files.items():
    with open(os.path.join(KIT_DIR, fname), "w", encoding="utf-8") as f:
        f.write(content)

# Re-render PNG exports in kit/exports/:
for sz in [16, 32, 64, 128, 180, 192, 512, 1024]:
    render_png.render(os.path.join(KIT_DIR, "logo-glyph.svg"), os.path.join(EXP_DIR, f"glyph-{sz}.png"), sz, sz)
    render_png.render(os.path.join(KIT_DIR, "logo-primary.svg"), os.path.join(EXP_DIR, f"primary-{sz}.png"), sz, sz)
    render_png.render(os.path.join(KIT_DIR, "logo-inverted.svg"), os.path.join(EXP_DIR, f"inverted-{sz}.png"), sz, sz, bg=NAVY)
    render_png.render(os.path.join(KIT_DIR, "logo-mono-white.svg"), os.path.join(EXP_DIR, f"mono-white-{sz}.png"), sz, sz, bg="#05070A")

print("Updated kit and exports successfully.")
