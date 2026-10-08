#!/usr/bin/env python3
"""Сборка концепций нового знака М-ТРЕНИНГ (Nova).

Запуск:  python3 designs/m-trening/nova/build_concepts.py
Пишет в nova/: concept-<имя>-{symbol,lockup-h}-{dark,light}.svg и превью PNG
в nova/renders/, затем вызывает build_board для планшета.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import nova_lib as nl  # noqa: E402

OUT = HERE
REN = os.path.join(HERE, "renders")
os.makedirs(REN, exist_ok=True)

PAL_DARK = {"main": nl.WHITE, "accent": nl.VOLT, "wm": nl.WHITE}
PAL_ONBLUE = {"main": nl.WHITE, "accent": nl.VOLT, "wm": nl.WHITE}
LIGHT_ACCENT = {"goal": nl.DEEP, "panel": nl.VOLT, "ballbase": nl.DEEP}
PAL_LIGHT = {"main": nl.BLUE, "accent": nl.DEEP, "wm": nl.BLUE}
def pal_light(key):
    return {"main": nl.BLUE, "accent": LIGHT_ACCENT[key], "wm": nl.BLUE}
PAL_MONO = {"main": nl.WHITE, "accent": nl.WHITE, "wm": nl.WHITE}

CONCEPTS = [("goal", "d-goal"), ("panel", "e-panel"), ("ballbase", "f-ballbase")]
SYM = {"goal": "symbol_goal", "panel": "symbol_panel", "ballbase": "symbol_ballbase"}
STYLE = {"goal": "srez", "panel": "pulse", "ballbase": "penta"}


def build():
    for key, slug in CONCEPTS:
        sym = getattr(nl, SYM[key])()
        style = STYLE[key]
        files = {
            f"concept-{slug}-symbol-dark.svg": nl.svg_symbol(sym, PAL_DARK, f"М-ТРЕНИНГ Nova {slug} знак"),
            f"concept-{slug}-symbol-light.svg": nl.svg_symbol(sym, pal_light(key), f"М-ТРЕНИНГ Nova {slug} знак"),
            f"concept-{slug}-lockup-h-dark.svg": nl.svg_from_layout(nl.lockup_h(sym, style), PAL_DARK, f"М-ТРЕНИНГ Nova {slug}"),
            f"concept-{slug}-lockup-h-light.svg": nl.svg_from_layout(nl.lockup_h(sym, style), pal_light(key), f"М-ТРЕНИНГ Nova {slug}"),
            f"concept-{slug}-lockup-v-dark.svg": nl.svg_from_layout(nl.lockup_v(sym, style), PAL_DARK, f"М-ТРЕНИНГ Nova {slug}"),
        }
        for name, svg in files.items():
            with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
                f.write(svg + "\n")
        # превью PNG
        nl.render(files[f"concept-{slug}-symbol-dark.svg"], 1024, 1024,
                  os.path.join(REN, f"concept-{slug}-symbol-dark-1024.png"), bg=nl.BLUE)
        nl.render(files[f"concept-{slug}-symbol-light.svg"], 1024, 1024,
                  os.path.join(REN, f"concept-{slug}-symbol-light-1024.png"), bg=nl.WHITE)
        lay = nl.lockup_h(sym, style)
        vb = lay["vb"]
        nl.render(files[f"concept-{slug}-lockup-h-dark.svg"],
                  int(vb[2] * 1.6), int(vb[3] * 1.6),
                  os.path.join(REN, f"concept-{slug}-lockup-h-dark.png"), bg=nl.DEEP)
        print("ok", slug)


if __name__ == "__main__":
    build()
    import build_board
    build_board.main()
