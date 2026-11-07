"""Greybox: modular ruin kit on the 100 cm grid (brief, Agent 2 > Modular grid).

Run:  ~/.venv-blender/bin/python Source/Blender/Scripts/Greybox_RuinKit.py [--only SM_...] [--no-export]

Conventions (all pieces)
    1 unit = 1 m. Walls run along +X; the front face is -Y (Blender front view).
    Wall pieces: pivot at the bottom of the wall's start end ON the grid line (x=0, y=0, z=0); the 20 cm
      thickness straddles the grid line (y -10..+10 cm) so perpendicular walls meet on a grid point.
    SM_Ruin_Wall_Corner: 30 x 30 cm pillar centred on the grid point; it covers the overlap where walls meet.
    Floor tile: pivot at the cell corner at walking level; the 20 cm slab hangs below (z -20..0), so floor
      tops sit at storey heights 0 / 300 / 600 cm and an upper slab fills the top 20 cm of the walls below.
    Roof, stairs: pivot at the bottom corner of the 400 x 400 / 100 x 400 cell on the grid.
    Rubble pile: not a grid piece; pivot at bottom centre.
"""
import math
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rflib import geo                       # noqa: E402
from rflib.pipeline import AssetSpec, main  # noqa: E402
from rflib.sockets import Socket            # noqa: E402

H = 3.0          # wall height
T = 0.20         # wall thickness
HT = T / 2
C = "Concrete"

DOOR = (1.5, 2.5, 0.0, 2.2)      # opening x0, x1, z0, z1 (100 x 220 cm, centred)
WINDOW = (1.5, 2.5, 0.9, 2.1)    # opening 100 x 120 cm, sill 90 cm
BARRICADE_GAP = 0.01             # barricade back face sits 1 cm off the wall face


def wall_box(length):
    return geo.box((0, -HT, 0), (length, HT, H), C)


def barricade_sockets(opening):
    x0, x1, z0, _ = opening
    xc = (x0 + x1) / 2
    return [
        Socket("SOCKET_BarricadeFront", (xc, -HT - BARRICADE_GAP, z0), (0, 0, 0)),
        Socket("SOCKET_BarricadeBack", (xc, HT + BARRICADE_GAP, z0), (0, 0, 180)),
    ]


def straight_wall(length):
    def build():
        w = wall_box(length)
        return {"parts": [w], "ucx": [w]}
    return build


def corner():
    p = geo.box((-0.15, -0.15, 0), (0.15, 0.15, H), C)
    return {"parts": [p], "ucx": [p]}


def window_wall():
    x0, x1, z0, z1 = WINDOW
    cut = geo.box((x0, -0.3, z0), (x1, 0.3, z1))
    ucx = [geo.box((0, -HT, 0), (x0, HT, H)), geo.box((x1, -HT, 0), (4, HT, H)),
           geo.box((x0, -HT, 0), (x1, HT, z0)), geo.box((x0, -HT, z1), (x1, HT, H))]
    return {"parts": [wall_box(4.0)], "cut": [cut], "ucx": ucx, "sockets": barricade_sockets(WINDOW)}


def door_wall():
    x0, x1, z0, z1 = DOOR
    cut = geo.box((x0, -0.3, z0 - 0.1), (x1, 0.3, z1))
    ucx = [geo.box((0, -HT, 0), (x0, HT, H)), geo.box((x1, -HT, 0), (4, HT, H)),
           geo.box((x0, -HT, z1), (x1, HT, H))]
    return {"parts": [wall_box(4.0)], "cut": [cut], "ucx": ucx, "sockets": barricade_sockets(DOOR)}


# Broken top line of the collapsed wall: (x, top z). Full height at the start end, 40 cm at the far end.
COLLAPSED_TOP = [(0.0, 3.0), (0.6, 3.0), (1.2, 2.3), (1.9, 2.0), (2.5, 1.2), (3.1, 1.0), (3.6, 0.5), (4.0, 0.4)]


def collapsed_wall():
    profile = [(0.0, 0.0), (4.0, 0.0)] + [(x, z) for x, z in reversed(COLLAPSED_TOP)]
    body = geo.prism(profile, 'Y', -HT, HT, C)
    ucx = []
    for (xa, za), (xb, zb) in zip(COLLAPSED_TOP, COLLAPSED_TOP[1:]):
        pts = [(x, y, z) for y in (-HT, HT) for (x, z) in ((xa, 0), (xb, 0), (xb, zb), (xa, za))]
        ucx.append(pts)
    return {"parts": [body], "ucx": ucx}


def floor_tile():
    p = geo.box((0, 0, -T), (4, 4, 0), C)
    return {"parts": [p], "ucx": [p]}


ROOF_RISE = 2.0   # 200 cm rise over the 400 cm run (26.6 degrees); two pieces make an 800 cm gable


def roof():
    profile = [(0.0, 0.0), (4.0, ROOF_RISE), (4.0, ROOF_RISE + T), (0.0, T)]
    slab = geo.prism(profile, 'X', 0.0, 4.0, C)
    return {"parts": [slab], "ucx": [slab]}


STEPS, RISE, RUN, STAIR_W = 15, 0.20, 4.0, 1.0   # 15 x 20 cm = 300 cm rise over 400 cm, 100 cm wide


def stairs():
    t = RUN / STEPS
    prof = [(0.0, 0.0)]
    for k in range(1, STEPS + 1):
        prof += [((k - 1) * t, RISE * k), (k * t, RISE * k)]
    prof.append((RUN, 0.0))
    body = geo.prism(prof, 'X', 0.0, STAIR_W, C)
    ramp = [(x, y, z) for x in (0.0, STAIR_W)
            for (y, z) in ((0, 0), (0, RISE), ((STEPS - 1) * t, STEPS * RISE), (RUN, STEPS * RISE), (RUN, 0))]
    return {"parts": [body], "ucx": [ramp],
            "sockets": [Socket("SOCKET_StairBottom", (STAIR_W / 2, 0.0, 0.0)),
                        Socket("SOCKET_StairTop", (STAIR_W / 2, RUN, STEPS * RISE))]}


RUBBLE_X, RUBBLE_Y, RUBBLE_Z = 1.0, 0.8, 0.8    # half-length, half-width, height (200 x 160 x 80 cm)


def rubble():
    rng = random.Random(20261107)
    pts = [(RUBBLE_X, 0, 0), (-RUBBLE_X, 0, 0), (0, RUBBLE_Y, 0), (0, -RUBBLE_Y, 0), (0, 0, RUBBLE_Z)]
    for i in range(14):                                   # base ring
        a = 6.2832 * i / 14 + rng.uniform(-0.1, 0.1)
        r = rng.uniform(0.82, 0.97)
        pts.append((RUBBLE_X * r * math.cos(a), RUBBLE_Y * r * math.sin(a), 0.0))
    for i in range(26):                                   # lumpy upper surface
        a = rng.uniform(0, 6.2832)
        r = rng.uniform(0.15, 0.85)
        h = RUBBLE_Z * (1 - r * r) ** 0.8 * rng.uniform(0.55, 0.95)
        pts.append((RUBBLE_X * r * math.cos(a), RUBBLE_Y * r * math.sin(a), h))
    mound = geo.hull(pts, C)
    chunks = [
        geo.box((-0.12, -0.10, 0), (0.12, 0.10, 0.18), C).transformed(geo.rot_z(28)).translated((0.70, 0.52, 0)),
        geo.box((-0.15, -0.09, 0), (0.15, 0.09, 0.14), C).transformed(geo.rot_z(-35)).translated((-0.72, -0.48, 0)),
        geo.box((-0.09, -0.09, 0), (0.09, 0.09, 0.12), C).transformed(geo.rot_z(12)).translated((0.20, -0.66, 0)),
    ]
    return {"parts": [mound] + chunks, "ucx": [mound] + chunks}


GRID = "pivot bottom of start end on grid line, thickness straddles line"
SPECS = [
    AssetSpec("SM_Ruin_Wall_400", "Ruin_Wall_400", "Modular", straight_wall(4.0),
              ((0, -HT, 0), (4, HT, H)), 8000, GRID),
    AssetSpec("SM_Ruin_Wall_200", "Ruin_Wall_200", "Modular", straight_wall(2.0),
              ((0, -HT, 0), (2, HT, H)), 8000, GRID, "filler"),
    AssetSpec("SM_Ruin_Wall_100", "Ruin_Wall_100", "Modular", straight_wall(1.0),
              ((0, -HT, 0), (1, HT, H)), 8000, GRID, "filler"),
    AssetSpec("SM_Ruin_Wall_Corner", "Ruin_Wall_Corner", "Modular", corner,
              ((-0.15, -0.15, 0), (0.15, 0.15, H)), 8000, "pivot bottom centre on the grid point",
              "30x30 cm pillar hides the wall overlap at L, T and X joins"),
    AssetSpec("SM_Ruin_Wall_Window_400", "Ruin_Wall_Window_400", "Modular", window_wall,
              ((0, -HT, 0), (4, HT, H)), 8000, GRID,
              "opening 100x120 cm at x 150-250, sill 90 cm; SOCKET_BarricadeFront/Back"),
    AssetSpec("SM_Ruin_Wall_Door_400", "Ruin_Wall_Door_400", "Modular", door_wall,
              ((0, -HT, 0), (4, HT, H)), 8000, GRID,
              "opening 100x220 cm at x 150-250; SOCKET_BarricadeFront/Back"),
    AssetSpec("SM_Ruin_Wall_Collapsed_400", "Ruin_Wall_Collapsed_400", "Modular", collapsed_wall,
              ((0, -HT, 0), (4, HT, H)), 8000, GRID, "broken top 300 cm down to 40 cm"),
    AssetSpec("SM_Ruin_Floor_400", "Ruin_Floor_400", "Modular", floor_tile,
              ((0, 0, -T), (4, 4, 0)), 8000, "pivot at cell corner at walking level; slab z -20..0"),
    AssetSpec("SM_Ruin_Roof_400", "Ruin_Roof_400", "Modular", roof,
              ((0, 0, 0), (4, 4, ROOF_RISE + T)), 8000, "pivot bottom corner at the eave on the grid",
              "slope rises +Y 200 cm over 400 cm; 20 cm slab"),
    AssetSpec("SM_Ruin_Stairs_300", "Ruin_Stairs_300", "Modular", stairs,
              ((0, 0, 0), (STAIR_W, RUN, STEPS * RISE)), 8000,
              "pivot bottom corner of first step on the grid; climbs +Y",
              "15 steps 20 cm rise x 26.7 cm tread, 100 cm wide; ramp UCX"),
    AssetSpec("SM_Ruin_RubblePile_01", "Ruin_RubblePile_01", "Modular", rubble,
              ((-RUBBLE_X, -RUBBLE_Y, 0), (RUBBLE_X, RUBBLE_Y, RUBBLE_Z)), 3000, "pivot bottom centre",
              "200x160x80 cm mound + 3 chunks"),
]

if __name__ == "__main__":
    _, failed = main(SPECS)
    sys.exit(1 if failed else 0)
