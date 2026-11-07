"""Rebuild every Agent 1 concept sheet from Concept/_raw/ and the drawing scripts.

    python3 Tools/concept/build_all.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_buildables  # noqa: E402
import build_ruinkit  # noqa: E402
import build_styleguide  # noqa: E402

if __name__ == "__main__":
    build_styleguide.build()
    build_buildables.build_walls()
    build_buildables.build_gatetower()
    build_buildables.build_traps()
    build_buildables.build_ghost()
    build_ruinkit.build_walls()
    build_ruinkit.build_floors()
    print("built all sheets")
