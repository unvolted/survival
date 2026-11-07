"""Greybox: player buildables from the Fortifications table, T1 (log) tier, plus the metal plate.

Run:  ~/.venv-blender/bin/python Source/Blender/Scripts/Greybox_Buildables.py [--only SM_...] [--no-export]

Pivot conventions (also written to the manifest notes)
    Line pieces (log, log wall, spiked wall, barbed wire, fire ring trench, welded gate frame):
        run along +X from the pivot; pivot = bottom of the START end, centred on the thickness (x=0, y=0, z=0).
        SOCKET_SnapEnd marks the far end, so the next segment's pivot goes there (free-form lines).
    Placed pieces (watchtower, spike pit, traps): pivot at bottom centre. Pit and trench pivots are at
        ground level; their dug part is below z=0, so the terrain needs a hole there.
    Attachments (metal plate, barricades, pit cover, deadfall weight, gate leaf): pivot at the mount point
        (back face / hinge / bottom centre). Snap the attachment's pivot to the host's SOCKET_ and copy its rotation.
    Front faces -Y (Blender front view), the side zombies attack; spikes point -Y.

Logs are 30 cm in diameter (12-sided). A log wall segment is 10 logs stacked on 30 cm centres:
log i sits at (0, 0, 0.30 * i) in the wall's space, so the ghost can be filled one SM_Build_Log_T1_Intact
at a time and swapped for the wall mesh when complete.
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rflib import geo                       # noqa: E402
from rflib.pipeline import AssetSpec, main  # noqa: E402
from rflib.sockets import Socket            # noqa: E402

W, M, S, R = "Wood", "Metal", "Soil", "Rope"

LOG_D = 0.30
LOG_R = LOG_D / 2
LOG_LEN = 4.0
LOG_SEG = 12
WALL_LOGS = 10
WALL_H = WALL_LOGS * LOG_D          # 3.0 m
PLATE_GAP = 0.02                    # plates sit 2 cm proud of the wood surface
PLATE_T = 0.01                      # 1 cm sheet (greybox)


def log_part(z0=0.0, x0=0.0, length=LOG_LEN):
    return geo.cylinder((x0, 0, z0 + LOG_R), (x0 + length, 0, z0 + LOG_R), LOG_R, LOG_SEG, W)


def log_wall_parts():
    return [log_part(z0=i * LOG_D) for i in range(WALL_LOGS)]


def log_wall_box():
    return geo.box((0, -LOG_R, 0), (LOG_LEN, LOG_R, WALL_H))


def plate_sockets(front=True, back=True):
    s = []
    if front:
        s.append(Socket("SOCKET_PlateMount", (LOG_LEN / 2, -LOG_R - PLATE_GAP, 0), (0, 0, 0)))
    if back:
        s.append(Socket("SOCKET_PlateMountBack", (LOG_LEN / 2, LOG_R + PLATE_GAP, 0), (0, 0, 180)))
    return s


SNAP_END = Socket("SOCKET_SnapEnd", (LOG_LEN, 0, 0))


# ---------------------------------------------------------------- log + walls
def single_log():
    p = log_part()
    return {"parts": [p], "ucx": [p],
            "sockets": [SNAP_END, Socket("SOCKET_Carry", (LOG_LEN / 2, 0, LOG_R))]}


def log_wall():
    return {"parts": log_wall_parts(), "ucx": [log_wall_box()],
            "sockets": [SNAP_END] + plate_sockets()}


SPIKE_ROWS = (0.75, 1.35)           # stake base heights (zombie hip and chest)
SPIKE_X = [0.25 + 0.5 * i for i in range(8)]
SPIKE_LEN, SPIKE_ANGLE, SPIKE_HALF = 0.90, 20.0, 0.04
SPIKE_BASE_Y = -0.10                # 5 cm into the front logs
_dy = -SPIKE_LEN * math.cos(math.radians(SPIKE_ANGLE))
_dz = SPIKE_LEN * math.sin(math.radians(SPIKE_ANGLE))
SPIKE_TIP_Y = SPIKE_BASE_Y + _dy


def spiked_wall():
    parts = log_wall_parts()
    for z in SPIKE_ROWS:
        for x in SPIKE_X:
            parts.append(geo.stake((x, SPIKE_BASE_Y, z), (x, SPIKE_BASE_Y + _dy, z + _dz), SPIKE_HALF, W))
    spike_zone = geo.box((0, SPIKE_TIP_Y, SPIKE_ROWS[0] - 0.05), (LOG_LEN, -LOG_R, SPIKE_ROWS[1] + _dz + 0.02))
    return {"parts": parts, "ucx": [log_wall_box(), spike_zone],
            "sockets": [SNAP_END] + plate_sockets(front=False)}


def metal_plate():
    p = geo.box((-LOG_LEN / 2, -PLATE_T, 0), (LOG_LEN / 2, 0, WALL_H), M)
    return {"parts": [p], "ucx": [p]}


# ---------------------------------------------------------------- fence, gate
FENCE_H = 1.30
POST_HALF = 0.05
WIRE_Z = (0.30, 0.60, 0.90, 1.20)
WIRE_Y0, WIRE_Y1 = -0.067, -0.051   # 1.6 cm strands just in front of the posts


def barbed_wire():
    parts = [geo.box((x - POST_HALF, -POST_HALF, 0), (x + POST_HALF, POST_HALF, FENCE_H), W) for x in (1.0, 3.0)]
    parts += [geo.box((0, WIRE_Y0, z - 0.008), (LOG_LEN, WIRE_Y1, z + 0.008), R) for z in WIRE_Z]
    ucx = [geo.box((0, WIRE_Y0, 0), (LOG_LEN, POST_HALF, FENCE_H))]
    return {"parts": parts, "ucx": ucx, "sockets": [SNAP_END]}


GATE_POST = 0.20
GATE_H = 3.0
GATE_BEAM_Z = 2.80
LEAF_W, LEAF_T, LEAF_Z0, LEAF_Z1 = 1.795, 0.05, 0.05, 2.75


def gate_frame():
    posts = [geo.box((0, -0.1, 0), (GATE_POST, 0.1, GATE_H), M),
             geo.box((LOG_LEN - GATE_POST, -0.1, 0), (LOG_LEN, 0.1, GATE_H), M)]
    beam = geo.box((GATE_POST, -0.1, GATE_BEAM_Z), (LOG_LEN - GATE_POST, 0.1, GATE_H), M)
    return {"parts": posts + [beam], "ucx": posts + [beam],
            "sockets": [SNAP_END,
                        Socket("SOCKET_HingeLeft", (GATE_POST, 0, 0), (0, 0, 0)),
                        Socket("SOCKET_HingeRight", (LOG_LEN - GATE_POST, 0, 0), (0, 0, 180))]}


def gate_leaf():
    p = geo.box((0.005, -LEAF_T / 2, LEAF_Z0), (LEAF_W, LEAF_T / 2, LEAF_Z1), M)
    return {"parts": [p], "ucx": [p]}


# ---------------------------------------------------------------- barricades
PLANK_L, PLANK_H, PLANK_T = 1.40, 0.20, 0.03


def planks(centres):
    return [geo.box((-PLANK_L / 2, -PLANK_T, zc - PLANK_H / 2), (PLANK_L / 2, 0, zc + PLANK_H / 2), W)
            for zc in centres]


DOOR_PLANKS = (0.5, 1.0, 1.5, 2.0)      # door opening 100 x 220 cm
WINDOW_PLANKS = (0.2, 0.6, 1.0)         # window opening 100 x 120 cm (pivot at the sill)


def barricade(centres):
    def build():
        ps = planks(centres)
        z0, z1 = centres[0] - PLANK_H / 2, centres[-1] + PLANK_H / 2
        return {"parts": ps, "ucx": [geo.box((-PLANK_L / 2, -PLANK_T, z0), (PLANK_L / 2, 0, z1))]}
    return build


# ---------------------------------------------------------------- watchtower
TW_POST = 0.85              # post centres at +-85 cm (footprint 230 x 230 cm deck)
TW_DECK = 1.15
TW_DECK_Z = 4.0             # deck top 400 cm
TW_TOP = 5.0
RAIL_R = 0.075
RAIL_Z = (4.45, 4.90)
LADDER_Y0, LADDER_Y1 = -1.22, -1.16
LADDER_RAIL_X = (0.22, 0.28)


def watchtower():
    parts, ucx = [], []
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * TW_POST, sy * TW_POST
            parts.append(geo.cylinder((x, y, 0), (x, y, TW_TOP), LOG_R, LOG_SEG, W))
            ucx.append(geo.box((x - LOG_R, y - LOG_R, 0), (x + LOG_R, y + LOG_R, TW_TOP)))
    deck = geo.box((-TW_DECK, -TW_DECK, TW_DECK_Z - 0.3), (TW_DECK, TW_DECK, TW_DECK_Z), W)
    parts.append(deck)
    ucx.append(deck)
    rz0, rz1 = RAIL_Z[0] - RAIL_R, RAIL_Z[1] + RAIL_R
    spans = [((-1.0, TW_POST), (1.0, TW_POST)),            # back
             ((-TW_POST, -1.0), (-TW_POST, 1.0)),           # left
             ((TW_POST, -1.0), (TW_POST, 1.0)),             # right
             ((-1.0, -TW_POST), (-0.35, -TW_POST)),         # front, gap for the ladder
             ((0.35, -TW_POST), (1.0, -TW_POST))]
    for (ax, ay), (bx, by) in spans:
        for z in RAIL_Z:
            parts.append(geo.cylinder((ax, ay, z), (bx, by, z), RAIL_R, 8, W))
        ucx.append(geo.box((min(ax, bx) - RAIL_R, min(ay, by) - RAIL_R, rz0),
                           (max(ax, bx) + RAIL_R, max(ay, by) + RAIL_R, rz1)))
    for sx in (-1, 1):
        x0, x1 = sorted((sx * LADDER_RAIL_X[0], sx * LADDER_RAIL_X[1]))
        parts.append(geo.box((x0, LADDER_Y0, 0), (x1, LADDER_Y1, TW_TOP), W))
    for k in range(1, 17):
        z = 0.30 * k
        parts.append(geo.box((-0.23, -1.21, z - 0.02), (0.23, -1.17, z + 0.02), W))
    ucx.append(geo.box((-LADDER_RAIL_X[1], LADDER_Y0, 0), (LADDER_RAIL_X[1], LADDER_Y1, TW_TOP)))
    return {"parts": parts, "ucx": ucx,
            "sockets": [Socket("SOCKET_LadderBottom", (0, -1.55, 0)),
                        Socket("SOCKET_LadderTop", (0, -0.70, TW_DECK_Z)),
                        Socket("SOCKET_Lookout", (0, 0, TW_DECK_Z))]}


# ---------------------------------------------------------------- pit, trench
PIT_IN, PIT_WALL, PIT_DEPTH, PIT_FLOOR = 1.0, 0.10, 1.50, 0.10   # 200 x 200 x 150 cm hole
PIT_OUT = PIT_IN + PIT_WALL
PIT_SPIKE_H = 0.60
COVER_T = 0.05


def spike_pit():
    tub = geo.box((-PIT_OUT, -PIT_OUT, -PIT_DEPTH - PIT_FLOOR), (PIT_OUT, PIT_OUT, 0), S)
    cut = geo.box((-PIT_IN, -PIT_IN, -PIT_DEPTH), (PIT_IN, PIT_IN, 0.2))
    parts = [tub]
    for x in (-0.6, 0.0, 0.6):
        for y in (-0.6, 0.0, 0.6):
            parts.append(geo.stake((x, y, -PIT_DEPTH - 0.02), (x, y, -PIT_DEPTH + PIT_SPIKE_H), SPIKE_HALF, W))
    zf = -PIT_DEPTH
    ucx = [geo.box((-PIT_OUT, -PIT_OUT, zf - PIT_FLOOR), (PIT_OUT, PIT_OUT, zf)),
           geo.box((-PIT_OUT, -PIT_OUT, zf), (-PIT_IN, PIT_OUT, 0)),
           geo.box((PIT_IN, -PIT_OUT, zf), (PIT_OUT, PIT_OUT, 0)),
           geo.box((-PIT_IN, -PIT_OUT, zf), (PIT_IN, -PIT_IN, 0)),
           geo.box((-PIT_IN, PIT_IN, zf), (PIT_IN, PIT_OUT, 0))]
    return {"parts": parts, "cut": [cut], "ucx": ucx,
            "sockets": [Socket("SOCKET_Cover", (0, 0, -COVER_T))]}


def pit_cover():
    p = geo.box((-PIT_IN + 0.01, -PIT_IN + 0.01, 0), (PIT_IN - 0.01, PIT_IN - 0.01, COVER_T), W)
    return {"parts": [p], "ucx": [p]}


# Trench cross-section (y, z): 60 cm wide, 30 cm deep, 15 cm earth berms either side, 10 cm floor.
TRENCH = [(-0.6, -0.4), (0.6, -0.4), (0.6, 0.0), (0.45, 0.15), (0.3, 0.15), (0.3, -0.3),
          (-0.3, -0.3), (-0.3, 0.15), (-0.45, 0.15), (-0.6, 0.0)]
FUEL_R = 0.075


def fire_ring():
    body = geo.prism(TRENCH, 'X', 0.0, LOG_LEN, S)
    fuel = [geo.cylinder((0.1, y, -0.3 + FUEL_R - 0.005), (LOG_LEN - 0.1, y, -0.3 + FUEL_R - 0.005), FUEL_R, 8, W)
            for y in (-0.12, 0.12)]
    floor = [(x, y, z) for x in (0, LOG_LEN) for y in (-0.3, 0.3) for z in (-0.4, -0.3)]
    berm_r = [(x, y, z) for x in (0, LOG_LEN) for (y, z) in ((0.3, -0.4), (0.6, -0.4), (0.6, 0.0), (0.45, 0.15), (0.3, 0.15))]
    berm_l = [(x, -y, z) for (x, y, z) in berm_r]
    return {"parts": [body] + fuel, "ucx": [floor, berm_l, berm_r], "sockets": [SNAP_END]}


# ---------------------------------------------------------------- traps
def noise_trap():
    parts = [geo.box((x - 0.025, -0.025, 0), (x + 0.025, 0.025, 0.5), W) for x in (-1.5, 1.5)]
    parts.append(geo.box((-1.5, -0.005, 0.245), (1.5, 0.005, 0.255), R))
    for x in (-0.75, 0.0, 0.75):
        parts.append(geo.cylinder((x, 0, 0.10), (x, 0, 0.21), 0.035, 8, M))
        parts.append(geo.box((x - 0.003, -0.003, 0.205), (x + 0.003, 0.003, 0.25), R))
    ucx = [geo.box((x - 0.025, -0.025, 0), (x + 0.025, 0.025, 0.5)) for x in (-1.5, 1.5)]
    return {"parts": parts, "ucx": ucx,
            "sockets": [Socket("SOCKET_TripLineStart", (-1.5, 0, 0.25)),
                        Socket("SOCKET_TripLineEnd", (1.5, 0, 0.25))]}


DF_POST_X = 1.1
DF_H = 2.5
DF_WEIGHT_Z = 1.8           # weight bottom when armed
DF_WEIGHT_HALF = 0.95


def deadfall_frame():
    posts = [geo.box((sx * DF_POST_X - 0.1, -0.1, 0), (sx * DF_POST_X + 0.1, 0.1, DF_H), W) for sx in (-1, 1)]
    bar = geo.box((-DF_POST_X - 0.1, -0.1, DF_H - 0.2), (DF_POST_X + 0.1, 0.1, DF_H), W)
    rope = geo.box((-0.01, -0.01, DF_WEIGHT_Z + LOG_D - 0.01), (0.01, 0.01, DF_H - 0.19), R)
    trip = geo.box((-DF_POST_X + 0.09, -0.005, 0.195), (DF_POST_X - 0.09, 0.005, 0.205), R)
    return {"parts": posts + [bar, rope, trip], "ucx": posts + [bar],
            "sockets": [Socket("SOCKET_WeightArmed", (0, 0, DF_WEIGHT_Z))]}


def deadfall_weight():
    p = geo.cylinder((-DF_WEIGHT_HALF, 0, LOG_R), (DF_WEIGHT_HALF, 0, LOG_R), LOG_R, LOG_SEG, W)
    return {"parts": [p], "ucx": [p]}


SN_RING_C, SN_RING_R, SN_TUBE = (0.30, 0.0, 0.20), 0.12, 0.01


def snare():
    st = geo.box((-0.025, -0.025, 0), (0.025, 0.025, 0.6), W)
    ring = geo.torus(SN_RING_C, SN_RING_R, SN_TUBE, 8, 4, normal=(0, 1, 0), mat=R)
    line = geo.cylinder((0.0, 0, 0.55), (SN_RING_C[0], 0, SN_RING_C[2] + SN_RING_R + SN_TUBE - 0.004),
                        0.004, 4, R, up=(0, 1, 0))
    return {"parts": [st, ring, line], "ucx": [geo.box((-0.025, -0.025, 0), (0.025, 0.025, 0.6))]}


# ---------------------------------------------------------------- specs
LINE = "pivot bottom of start end, centred on thickness; runs +X; SOCKET_SnapEnd at far end"
SPECS = [
    AssetSpec("SM_Build_Log_T1_Intact", "Build_Log_T1", "Buildable", single_log,
              ((0, -LOG_R, 0), (LOG_LEN, LOG_R, LOG_D)), 3000, LINE,
              "repeatable free-form log 400 x 30 cm, cut ends; SOCKET_Carry at centre"),
    AssetSpec("SM_Build_LogWall_T1_Intact", "Build_LogWall_T1", "Buildable", log_wall,
              ((0, -LOG_R, 0), (LOG_LEN, LOG_R, WALL_H)), 8000, LINE,
              "10 logs on 30 cm centres; SOCKET_PlateMount (front -Y) / PlateMountBack 2 cm proud"),
    AssetSpec("SM_Build_SpikedWall_T1_Intact", "Build_SpikedWall_T1", "Buildable", spiked_wall,
              ((0, SPIKE_TIP_Y, 0), (LOG_LEN, LOG_R, WALL_H)), 8000, LINE,
              "log wall + 16 stakes pointing -Y, 20 deg up; UCX_01 = spike zone; PlateMountBack only"),
    AssetSpec("SM_Build_MetalPlate_T3_Intact", "Build_MetalPlate_T3", "Buildable", metal_plate,
              ((-LOG_LEN / 2, -PLATE_T, 0), (LOG_LEN / 2, 0, WALL_H)), 3000,
              "pivot bottom centre of back face; attach to SOCKET_PlateMount",
              "400x300x1 cm sheet; back face lands 2 cm proud of the wood"),
    AssetSpec("SM_Build_BarbedWire_T1_Intact", "Build_BarbedWire_T1", "Buildable", barbed_wire,
              ((0, WIRE_Y0, 0), (LOG_LEN, POST_HALF, FENCE_H)), 3000, LINE,
              "130 cm, posts at x 100/300, 4 strands; segments chain without doubled posts"),
    AssetSpec("SM_Build_WeldedGate_T1_Intact", "Build_WeldedGate_T1", "Buildable", gate_frame,
              ((0, -0.1, 0), (LOG_LEN, 0.1, GATE_H)), 8000, LINE,
              "frame replaces a 400 cm wall segment; 360x280 cm clear; SOCKET_HingeLeft/Right"),
    AssetSpec("SM_Build_WeldedGate_Leaf_T1_Intact", "Build_WeldedGate_Leaf_T1", "Buildable", gate_leaf,
              ((0.005, -LEAF_T / 2, LEAF_Z0), (LEAF_W, LEAF_T / 2, LEAF_Z1)), 3000,
              "pivot on the hinge axis at ground; leaf extends +X; swing = rotate about Z",
              "use twice (one per hinge socket); 179x5x270 cm, 5 cm ground gap"),
    AssetSpec("SM_Build_BarricadeDoor_T1_Intact", "Build_BarricadeDoor_T1", "Buildable",
              barricade(DOOR_PLANKS),
              ((-PLANK_L / 2, -PLANK_T, DOOR_PLANKS[0] - PLANK_H / 2), (PLANK_L / 2, 0, DOOR_PLANKS[-1] + PLANK_H / 2)),
              3000, "pivot at opening bottom centre on the back face; attach to SOCKET_BarricadeFront/Back",
              "4 planks 140x20x3 cm over the 100x220 door opening"),
    AssetSpec("SM_Build_BarricadeWindow_T1_Intact", "Build_BarricadeWindow_T1", "Buildable",
              barricade(WINDOW_PLANKS),
              ((-PLANK_L / 2, -PLANK_T, WINDOW_PLANKS[0] - PLANK_H / 2), (PLANK_L / 2, 0, WINDOW_PLANKS[-1] + PLANK_H / 2)),
              3000, "pivot at sill centre on the back face; attach to SOCKET_BarricadeFront/Back",
              "3 planks 140x20x3 cm over the 100x120 window opening"),
    AssetSpec("SM_Build_Watchtower_T1_Intact", "Build_Watchtower_T1", "Buildable", watchtower,
              ((-TW_DECK, LADDER_Y0, 0), (TW_DECK, TW_DECK, TW_TOP)), 8000, "pivot bottom centre",
              "230x230 cm deck top at 400 cm, rails to 500 cm, ladder on -Y; SOCKET_LadderBottom/Top/Lookout"),
    AssetSpec("SM_Build_SpikePit_T1_Intact", "Build_SpikePit_T1", "Buildable", spike_pit,
              ((-PIT_OUT, -PIT_OUT, -PIT_DEPTH - PIT_FLOOR), (PIT_OUT, PIT_OUT, 0)), 3000,
              "pivot top centre at ground level; hole goes down to -160 cm (terrain needs a hole)",
              "200x200x150 cm hole, 9 stakes 60 cm; SOCKET_Cover"),
    AssetSpec("SM_Build_SpikePit_Cover_T1_Intact", "Build_SpikePit_Cover_T1", "Buildable", pit_cover,
              ((-PIT_IN + 0.01, -PIT_IN + 0.01, 0), (PIT_IN - 0.01, PIT_IN - 0.01, COVER_T)), 3000,
              "pivot bottom centre; attach to SOCKET_Cover (top lands flush with ground)",
              "198x198x5 cm stick-and-leaf cover; hide/remove when triggered"),
    AssetSpec("SM_Build_FireRing_T1_Intact", "Build_FireRing_T1", "Buildable", fire_ring,
              ((0, -0.6, -0.4), (LOG_LEN, 0.6, 0.15)), 3000,
              LINE + "; ground level at z=0, trench to -40 cm (terrain needs a hole)",
              "400 cm burn-trench segment, 60x30 cm channel, 15 cm berms, 2 fuel logs"),
    AssetSpec("SM_Build_NoiseTrap_T1_Intact", "Build_NoiseTrap_T1", "Buildable", noise_trap,
              ((-1.525, -0.035, 0), (1.525, 0.035, 0.5)), 3000, "pivot bottom centre",
              "2 stakes, 300 cm string at 25 cm, 3 cans; SOCKET_TripLineStart/End for the trigger"),
    AssetSpec("SM_Build_Deadfall_T1_Intact", "Build_Deadfall_T1", "Buildable", deadfall_frame,
              ((-DF_POST_X - 0.1, -0.1, 0), (DF_POST_X + 0.1, 0.1, DF_H)), 3000, "pivot bottom centre",
              "2 posts + crossbar 250 cm, trip line at 20 cm; SOCKET_WeightArmed at 180 cm"),
    AssetSpec("SM_Build_Deadfall_Weight_T1_Intact", "Build_Deadfall_Weight_T1", "Buildable", deadfall_weight,
              ((-DF_WEIGHT_HALF, -LOG_R, 0), (DF_WEIGHT_HALF, LOG_R, LOG_D)), 3000,
              "pivot bottom centre; attach to SOCKET_WeightArmed, drops to z=0",
              "190 x 30 cm log"),
    AssetSpec("SM_Build_Snare_T1_Intact", "Build_Snare_T1", "Buildable", snare,
              ((-0.025, -0.025, 0), (SN_RING_C[0] + SN_RING_R + SN_TUBE, 0.025, 0.6)), 3000,
              "pivot bottom centre of the stake", "small-animal snare: 60 cm stake, 24 cm noose loop on +X"),
]

if __name__ == "__main__":
    _, failed = main(SPECS)
    sys.exit(1 if failed else 0)
