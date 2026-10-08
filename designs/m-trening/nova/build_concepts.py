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
PAL_LIGHT = {"main": nl.INK, "accent": nl.PITCH, "wm": nl.INK}
PAL_MONO = {"main": nl.WHITE, "accent": nl.WHITE, "wm": nl.WHITE}

CONCEPTS = [("pulse", "a-pulse"), ("srez", "b-srez"), ("penta", "c-penta")]


def build():
    for style, slug in CONCEPTS:
        sym = getattr(nl, {"pulse": "symbol_pulse", "srez": "symbol_srez",
                           "penta": "symbol_penta"}[style])()
        files = {
            f"concept-{slug}-symbol-dark.svg": nl.svg_symbol(sym, PAL_DARK, f"М-ТРЕНИНГ Nova {slug} знак"),
            f"concept-{slug}-symbol-light.svg": nl.svg_symbol(sym, PAL_LIGHT, f"М-ТРЕНИНГ Nova {slug} знак"),
            f"concept-{slug}-lockup-h-dark.svg": nl.svg_from_layout(nl.lockup_h(sym, style), PAL_DARK, f"М-ТРЕНИНГ Nova {slug}"),
            f"concept-{slug}-lockup-h-light.svg": nl.svg_from_layout(nl.lockup_h(sym, style), PAL_LIGHT, f"М-ТРЕНИНГ Nova {slug}"),
            f"concept-{slug}-lockup-v-dark.svg": nl.svg_from_layout(nl.lockup_v(sym, style), PAL_DARK, f"М-ТРЕНИНГ Nova {slug}"),
        }
        for name, svg in files.items():
            with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
                f.write(svg + "\n")
        # превью PNG
        nl.render(files[f"concept-{slug}-symbol-dark.svg"], 1024, 1024,
                  os.path.join(REN, f"concept-{slug}-symbol-dark-1024.png"), bg=nl.PITCH)
        nl.render(files[f"concept-{slug}-symbol-light.svg"], 1024, 1024,
                  os.path.join(REN, f"concept-{slug}-symbol-light-1024.png"), bg=nl.WHITE)
        lay = nl.lockup_h(sym, style)
        vb = lay["vb"]
        nl.render(files[f"concept-{slug}-lockup-h-dark.svg"],
                  int(vb[2] * 1.6), int(vb[3] * 1.6),
                  os.path.join(REN, f"concept-{slug}-lockup-h-dark.png"), bg=nl.PITCH)
        print("ok", slug)


if __name__ == "__main__":
    build()
    import build_board
    build_board.main()
