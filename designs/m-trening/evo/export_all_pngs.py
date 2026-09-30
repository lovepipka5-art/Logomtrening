#!/usr/bin/env python3
import os
import sys
import shutil
import resvg_py

sys.path.insert(0, "skills/logo-design/scripts")
sys.path.insert(0, "designs/m-trening/evo")
from update_kit_and_board import (
    ball_paths, orb_uniform, orb_swoosh, orb_aero,
    ship_a_solids, ship_a_hull,
    ship_b_solids, ship_b_hull,
    ship_c_solids, ship_c_hull,
    make_lockup_svg, make_horizontal_svg, make_glyph_svg,
    NAVY, CORAL_LIGHT_BG, CORAL_DARK_BG, CYAN_DARK_BG, WHITE, BLACK
)

OUT_PNG = "logos-png"
os.makedirs(OUT_PNG, exist_ok=True)

def save_and_render(name, svg_content, w=1024, h=1024, bg=None):
    png_path = os.path.join(OUT_PNG, f"{name}.png")
    kwargs = dict(
        svg_string=svg_content,
        width=w,
        height=h,
        font_dirs=["/usr/share/fonts"],
    )
    if bg:
        kwargs["background"] = bg
    png_bytes = resvg_py.svg_to_bytes(**kwargs)
    with open(png_path, "wb") as f:
        f.write(png_bytes)
    return png_path

# ============================================================================
# 1. ВАРИАНТ A — ЧИСТАЯ КЛАССИКА (ORIGINAL REMASTER)
# ============================================================================
svg_a_white = make_lockup_svg("М-ТРЕНИНГ A White", ball_paths, orb_uniform, ship_a_solids, ship_a_hull, WHITE, WHITE)
svg_a_black = make_lockup_svg("М-ТРЕНИНГ A Black", ball_paths, orb_uniform, ship_a_solids, ship_a_hull, BLACK, BLACK)
svg_a_dark_coral = make_lockup_svg("М-ТРЕНИНГ A Dark Coral", ball_paths, orb_uniform, ship_a_solids, ship_a_hull, WHITE, CORAL_DARK_BG)
svg_a_light_coral = make_lockup_svg("М-ТРЕНИНГ A Light Coral", ball_paths, orb_uniform, ship_a_solids, ship_a_hull, NAVY, CORAL_LIGHT_BG)

save_and_render("variant-a-classic-white-on-dark-1024", svg_a_white, 1024, 1024, bg="#05070A")
save_and_render("variant-a-classic-white-transparent-1024", svg_a_white, 1024, 1024, bg=None)
save_and_render("variant-a-classic-black-transparent-1024", svg_a_black, 1024, 1024, bg=None)
save_and_render("variant-a-classic-color-on-dark-1024", svg_a_dark_coral, 1024, 1024, bg=NAVY)
save_and_render("variant-a-classic-color-on-white-1024", svg_a_light_coral, 1024, 1024, bg=WHITE)
save_and_render("variant-a-classic-color-transparent-1024", svg_a_light_coral, 1024, 1024, bg=None)

# ============================================================================
# 2. ВАРИАНТ B — ФИРМЕННЫЙ ПАРУС-М (SIGNATURE SAIL-M)
# ============================================================================
svg_b_white = make_lockup_svg("М-ТРЕНИНГ B White", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, WHITE, WHITE)
svg_b_black = make_lockup_svg("М-ТРЕНИНГ B Black", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, BLACK, BLACK)
svg_b_dark_coral = make_lockup_svg("М-ТРЕНИНГ B Dark Coral", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, WHITE, CORAL_DARK_BG)
svg_b_light_coral = make_lockup_svg("М-ТРЕНИНГ B Light Coral", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, NAVY, CORAL_LIGHT_BG)
svg_b_horiz_dark = make_horizontal_svg("М-ТРЕНИНГ B Horizontal Dark", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, WHITE, CORAL_DARK_BG)
svg_b_horiz_light = make_horizontal_svg("М-ТРЕНИНГ B Horizontal Light", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, NAVY, CORAL_LIGHT_BG)
svg_b_glyph_white = make_glyph_svg("М-ТРЕНИНГ B Glyph White", ball_paths, orb_swoosh, ship_b_solids, ship_b_hull, WHITE, CORAL_DARK_BG)

save_and_render("variant-b-sail-m-white-on-dark-1024", svg_b_white, 1024, 1024, bg="#05070A")
save_and_render("variant-b-sail-m-white-transparent-1024", svg_b_white, 1024, 1024, bg=None)
save_and_render("variant-b-sail-m-black-transparent-1024", svg_b_black, 1024, 1024, bg=None)
save_and_render("variant-b-sail-m-color-on-dark-1024", svg_b_dark_coral, 1024, 1024, bg=NAVY)
save_and_render("variant-b-sail-m-color-on-white-1024", svg_b_light_coral, 1024, 1024, bg=WHITE)
save_and_render("variant-b-sail-m-color-transparent-1024", svg_b_light_coral, 1024, 1024, bg=None)
save_and_render("variant-b-sail-m-horizontal-on-dark-1600", svg_b_horiz_dark, 1600, 500, bg=NAVY)
save_and_render("variant-b-sail-m-horizontal-on-white-1600", svg_b_horiz_light, 1600, 500, bg=WHITE)
save_and_render("variant-b-sail-m-horizontal-transparent-1600", svg_b_horiz_light, 1600, 500, bg=None)
save_and_render("variant-b-sail-m-symbol-only-on-dark-1024", svg_b_glyph_white, 1024, 1024, bg=NAVY)

# ============================================================================
# 3. ВАРИАНТ C — СКОРОСТНОЙ ИМПУЛЬС (AERO FLOW)
# ============================================================================
svg_c_white = make_lockup_svg("М-ТРЕНИНГ C White", ball_paths, orb_aero, ship_c_solids, ship_c_hull, WHITE, WHITE)
svg_c_black = make_lockup_svg("М-ТРЕНИНГ C Black", ball_paths, orb_aero, ship_c_solids, ship_c_hull, BLACK, BLACK)
svg_c_dark_cyan = make_lockup_svg("М-ТРЕНИНГ C Dark Cyan", ball_paths, orb_aero, ship_c_solids, ship_c_hull, WHITE, CYAN_DARK_BG)
svg_c_light_cyan = make_lockup_svg("М-ТРЕНИНГ C Light Cyan", ball_paths, orb_aero, ship_c_solids, ship_c_hull, NAVY, "#0284C7")

save_and_render("variant-c-aero-white-on-dark-1024", svg_c_white, 1024, 1024, bg="#05070A")
save_and_render("variant-c-aero-white-transparent-1024", svg_c_white, 1024, 1024, bg=None)
save_and_render("variant-c-aero-black-transparent-1024", svg_c_black, 1024, 1024, bg=None)
save_and_render("variant-c-aero-cyan-on-dark-1024", svg_c_dark_cyan, 1024, 1024, bg=NAVY)
save_and_render("variant-c-aero-cyan-on-white-1024", svg_c_light_cyan, 1024, 1024, bg=WHITE)
save_and_render("variant-c-aero-cyan-transparent-1024", svg_c_light_cyan, 1024, 1024, bg=None)

# Copy presentation board into logos-png as well:
shutil.copyfile("logo-board.png", os.path.join(OUT_PNG, "logo-board-presentation.png"))
print("Exported all high-res PNG logos into logos-png/")
