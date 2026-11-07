"""Modular ruin kit sheets (Agent 1).

Builds:
  Concept/CA_RuinKit_Walls_Sheet.png              walls 400/200/100, window, door, corner x intact/damaged/overgrown
  Concept/CA_RuinKit_FloorsRoofsStairs_Sheet.png  floor tile, roof slope, stairs, collapsed wall/floor/roof, rubble x 3 states

Brief numbers: 100 cm grid, walls 400 x 300 x 20, fillers 200 and 100, floor tiles 400 x 400.
Openings, roof pitch, stair rise/run, collapsed and rubble sizes are Agent 1 assumptions (listed in the report).
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sheetlib import *  # noqa: E402,F401,F403

VOID = "#1E2124"
STATES = ("Intact", "Damaged", "Overgrown")
WIN = (100, 120, 90)   # width, height, sill
DOOR = (100, 220)


# ---------------------------------------------------------------- texture helpers
def brick_patch(v, x0, y0, x1, y1, seed=0):
    r = rng(seed)
    v.rect(x0, y0, x1, y1, fill=C["Weathered Brick"], outline=None)
    y = y0
    row = 0
    while y < y1:
        v.line([(x0, y), (x1, y)], mix(C["Weathered Brick"], "#000000", 0.35), 1)
        off = 0 if row % 2 else 11
        x = x0 + off
        while x < x1:
            v.line([(x, y), (x, min(y + 7.5, y1))], mix(C["Weathered Brick"], "#000000", 0.35), 1)
            x += 22
        y += 7.5
        row += 1


def crack(v, x, y, n=6, seed=0, step=10, bounds=None):
    r = rng(seed)
    pts = [(x, y)]
    a = r.uniform(0, 6.28)
    for _ in range(n):
        a += r.uniform(-0.7, 0.7)
        nx_, ny_ = x + math.cos(a) * step, y + math.sin(a) * step
        if bounds and not (bounds[0] + 3 < nx_ < bounds[2] - 3 and bounds[1] + 3 < ny_ < bounds[3] - 3):
            break
        x, y = nx_, ny_
        pts.append((x, y))
    if len(pts) < 2:
        return
    v.line(pts, "#3A3634", 1.2)


def pocks(v, x0, x1, y0, y1, n, seed=0):
    r = rng(seed)
    for _ in range(n):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        v.circle(x, y, r.uniform(2.2, 3.5), fill=mix(C["Old Plaster"], "#FFFFFF", 0.2), outline=None)
        v.circle(x, y, r.uniform(0.9, 1.6), fill="#2A2725", outline=None)


def scorch(v, x, y, rad, seed=0):
    for k in range(6, 0, -1):
        v.circle(x, y, rad * k / 6, fill="#1A1817", outline=None, alpha=28)


def jag(r, a, b, n, amp):
    """Jagged polyline from point a to b."""
    pts = [a]
    for i in range(1, n):
        t = i / n
        pts.append((a[0] + (b[0] - a[0]) * t + r.uniform(-amp, amp), a[1] + (b[1] - a[1]) * t + r.uniform(-amp, amp)))
    pts.append(b)
    return pts


def rebar(v, x, y, ang, L):
    a = math.radians(ang)
    v.line([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], C["Old Rust"], 2.2)


# ---------------------------------------------------------------- wall pieces
def wall_piece(v, x0, L, kind, state, seed=0, H=300):
    """Ruin wall elevation. kind: plain | window | door. state: Intact | Damaged | Overgrown."""
    r = rng(seed)
    v.rect(x0, 0, x0 + L, H, fill=C["Old Plaster"], width=1.5)
    # damp base + top staining
    for k in range(8):
        v.rect(x0, 0, x0 + L, 8 + k * 5, fill=C["Wet Concrete"], outline=None, alpha=16)
    for k in range(4):
        v.rect(x0, H - 6 - k * 6, x0 + L, H, fill=C["Wet Concrete"], outline=None, alpha=14)
    # plaster loss patches
    for _ in range(max(1, L // 130)):
        bx = x0 + r.uniform(10, L - 50)
        by = r.uniform(30, H - 60)
        brick_patch(v, bx, by, bx + r.uniform(25, 45), by + r.uniform(15, 30), seed=r.randint(0, 999))
    for _ in range(max(1, L // 100)):
        crack(v, x0 + r.uniform(10, L - 10), r.uniform(20, H - 20), n=r.randint(3, 7), seed=r.randint(0, 999), bounds=(x0, 0, x0 + L, H))
    cx = x0 + L / 2
    hole = None
    if kind == "window":
        w, h, sill = WIN
        hole = (cx - w / 2, sill, cx + w / 2, sill + h)
    elif kind == "door":
        w, h = DOOR
        hole = (cx - w / 2, 0, cx + w / 2, h)
    if hole:
        a, b, c, d = hole
        v.rect(a, b, c, d, fill=VOID, width=1.5)
        v.rect(a - 15, d, c + 15, d + 20, fill=C["Dry Concrete"], width=1.2)   # lintel
        if kind == "window":
            v.rect(a - 8, b - 6, c + 8, b, fill=C["Dry Concrete"], width=1.2)  # sill
            # broken glass shards in frame
            for (gx, gy, sgn) in ((a, d, 1), (c, d, -1), (a, b, 1)):
                v.poly([(gx, gy), (gx + sgn * r.uniform(10, 22), gy), (gx, gy + (r.uniform(-25, -12) if gy == d else r.uniform(12, 22)))],
                       fill="#7E8B8E", outline="#B9C2C2", width=1, alpha=150)
            for k in range(3):
                sx = a + 10 + k * 35
                v.line([(sx, b - 6), (sx + r.uniform(-2, 2), b - 6 - r.uniform(30, 70))], C["Old Rust"], 1.5, alpha=140)
        if kind == "door" and state == "Intact":
            v.rect(a + 2, b, c - 2, d - 2, fill=C["Rotten Wood"], width=1.2)
            v.rect(a + 12, b + 110, a + 40, d - 20, fill=None, outline=mix(C["Rotten Wood"], "#000000", 0.3), width=1)
            v.rect(a + 12, b + 15, a + 40, b + 95, fill=None, outline=mix(C["Rotten Wood"], "#000000", 0.3), width=1)
            v.circle(c - 12, 100, 2.2, fill=C["Old Rust"], outline=None)
    if state in ("Damaged", "Overgrown"):
        # missing top chunk
        tx0 = x0 + r.uniform(0.15, 0.45) * L
        tx1 = tx0 + r.uniform(0.25, 0.45) * L
        tx1 = min(tx1, x0 + L + 0.01)
        depth = r.uniform(50, 110) if L > 150 else r.uniform(30, 70)
        top = jag(r, (tx0, H + 1), (tx0 + (tx1 - tx0) * 0.3, H - depth), 4, 5) + jag(r, (tx0 + (tx1 - tx0) * 0.3, H - depth), (tx1, H + 1), 5, 6)[1:]
        brick = [(x, y - 7) for (x, y) in top[1:-1]]
        v.poly(top, fill=C["Weathered Brick"], outline=None)
        v.poly([(top[0][0], H + 3)] + [(x, y + 4) for (x, y) in top[1:-1]] + [(top[-1][0], H + 3)], fill=PANEL, outline=None)
        v.line([(x, y + 4) for (x, y) in top[1:-1]], INK, 1.5)
        for i in range(2):
            p = top[1 + i * 2]
            rebar(v, p[0], p[1] + 4, r.uniform(60, 110), r.uniform(15, 30))
        # shell hole (plain/window/door walls >= 200)
        if L >= 200:
            hx = x0 + (L * 0.2 if kind != "plain" else L * r.uniform(0.25, 0.7))
            hy = r.uniform(60, 140) if kind != "window" else 60
            if kind == "door":
                hx = x0 + L * 0.82
            rr = r.uniform(18, 28)
            pts = [(hx + math.cos(t) * rr * r.uniform(0.7, 1.2), hy + math.sin(t) * rr * r.uniform(0.7, 1.2)) for t in [i * 0.52 for i in range(12)]]
            ring = [(hx + (x - hx) * 1.35, hy + (y - hy) * 1.35) for (x, y) in pts]
            scorch(v, hx, hy, rr * 2.4)
            v.poly(ring, fill=C["Weathered Brick"], outline=None)
            v.poly(pts, fill=VOID, width=1.5)
        pocks(v, x0 + 5, x0 + L - 5, 80, 230, int(L / 18), seed=seed + 1)
        if kind == "door":
            # door leaf hanging from one hinge
            a, b, c, d = hole
            v.poly([(a + 2, d - 4), (a + 14, d - 2), (a + 40, b + 30), (a + 22, b + 20)], fill=C["Rotten Wood"], width=1.2)
    if state == "Overgrown":
        for i in range(max(2, L // 45)):
            x = x0 + 8 + i * (L - 16) / max(1, (L // 45) - 1 if L // 45 > 1 else 1)
            ivy_vine(v, x, 0, r.uniform(60, 210 if L > 100 else 160), seed=seed * 7 + i, drift=r.uniform(-0.6, 0.6))
        moss_band(v, x0, x0 + L, 0, 30, seed=seed + 3)
        moss_band(v, x0, x0 + L, H - 10, 10, seed=seed + 4, density=0.6)
        grass_tufts(v, x0 - 5, x0 + L + 5, 0, int(L / 12), seed=seed + 5, h=22)
        if hole:
            a, b, c, d = hole
            for i in range(4):
                ivy_vine(v, a + 12 + i * 25, d, r.uniform(40, 90 if kind == "window" else 140), seed=seed * 11 + i, down=True, drift=r.uniform(-0.4, 0.4))
        if L >= 200:
            sapling(v, x0 + L * 0.72, H - 40, 90, seed=seed + 9)


def corner_elev(v, x0, state, seed=0, H=300):
    """Corner pillar 30 x 30 x 300, centred on the grid intersection (hides wall overlaps at L, T and X joins)."""
    r = rng(seed)
    v.rect(x0, 0, x0 + 30, H, fill=mix(C["Old Plaster"], C["Dry Concrete"], 0.4), width=1.5)
    v.rect(x0 + 22, 0, x0 + 30, H, fill=mix(C["Old Plaster"], "#000000", 0.25), outline=None)
    for k in range(8):
        v.rect(x0, 0, x0 + 30, 8 + k * 5, fill=C["Wet Concrete"], outline=None, alpha=16)
    if state != "Intact":
        top = [(x0, H + 1), (x0, H - 22), (x0 + 12, H - 34), (x0 + 20, H - 12), (x0 + 30, H - 18), (x0 + 30, H + 1)]
        v.poly(top, fill=PANEL, outline=None)
        v.line(top[1:-1], INK, 1.5)
        brick_patch(v, x0 + 2, 120, x0 + 22, 150, seed=seed)
        rebar(v, x0 + 12, H - 34, 95, 20)
        pocks(v, x0 + 4, x0 + 26, 60, 220, 5, seed=seed)
    if state == "Overgrown":
        ivy_vine(v, x0 + 8, 0, 230, seed=seed + 2)
        ivy_vine(v, x0 + 22, 0, 150, seed=seed + 3)
        moss_band(v, x0, x0 + 30, 0, 30, seed=seed + 4)


def build_walls():
    sh = Sheet(4096, 3340)
    sh.title_block("Modular ruin kit · Walls, fillers, windows, doors, corners",
                   "CA_RuinKit_Walls_Sheet.png", "100 cm grid · all dimensions in cm",
                   "Drawn elevations are authoritative; painted reference is for look and material only")
    s = 1.5
    cols = [("Wall_400", 400, "plain"), ("Wall_200", 200, "plain"), ("Wall_100", 100, "plain"),
            ("Window_400", 400, "window"), ("Door_400", 400, "door"), ("Corner", 30, "corner")]
    sh.panel(30, 130, 4036, 1770, "A  Wall pieces · SM_Ruin_<Piece>_<State>", "front elevation, outside face · 300 tall · 20 thick")
    x = 190
    xs = []
    for name, L, kind in cols:
        xs.append(x)
        sh.text(x, 186, "SM_Ruin_" + name, 20, "Bold")
        x += max(L, 100) * s + 95
    for row, st in enumerate(STATES):
        oy = 710 + row * 545
        sh.label_box(48, oy - 240, "_" + st, 18, "Bold", "#FFFFFF", {0: "#4E5457", 1: "#7A4A3A", 2: "#3F5236"}[row])
        for i, (name, L, kind) in enumerate(cols):
            v = View(sh, xs[i], oy, s)
            v.grid(0, 0, max(L, 100), 300, 100, labels=(i == 0), ground=True)
            if kind == "corner":
                corner_elev(v, 0, st, seed=60 + row)
            else:
                wall_piece(v, 0, L, kind, st, seed=10 * i + row * 3 + 1)
            if row == 0:
                v.dim_h(0, L, 300, f"{L}", off=-14, size=14)
                if kind == "window":
                    v.dim_h(150, 250, 90, "100", off=0, size=12)
                    v.dim_v(90, 210, 250, "120", off=14, size=12)
                    v.dim_v(0, 90, 250, "sill 90", off=14, size=12)
                if kind == "door":
                    v.dim_v(0, 220, 250, "220", off=14, size=12)
                    v.dim_h(150, 250, 120, "100", off=0, size=12)
        if row == 0:
            View(sh, xs[0], oy, s).dim_v(0, 300, 0, "300", off=-62, size=14)
    scale_figure(View(sh, xs[-1] + 290, 710, s), 0)
    sh.text(190, 1835,
            "Intact = structurally whole but 15 years old: damp base, plaster loss showing brick, cracks, rust streaks under sills, broken glass "
            "remnants. Damaged = war damage: missing top chunk with exposed brick and rebar, shell hole with scorch ring, bullet pocking, door leaf "
            "hanging. Overgrown = the Damaged mesh + overgrowth layer (moss band, ivy climbing from the base, ivy pouring out of openings, a sapling "
            "on broken tops). Ivy and moss are separate cards / decals (Agent 2 rule), so any state can be overgrown in-engine.",
            18, "Regular", INK, maxw=3860)

    # ---- B: plan / section / modular rules
    sh.panel(30, 1920, 2000, 1390, "B  Grid, thickness, corner and stacking", "plan and section")
    vp = View(sh, 250, 2400, 0.7)
    vp.grid(-100, -100, 700, 500, 100, labels=True, ground=False)
    # walls on grid lines: centreline on line, thickness +-10
    vp.rect(0, -10, 400, 10, fill=C["Old Plaster"], width=1.2)
    vp.rect(400, -10, 500, 10, fill=C["Old Plaster"], width=1.2)
    vp.rect(-10, 0, 10, 400, fill=C["Old Plaster"], width=1.2)
    for (cx_, cy_) in ((0, 0), (400, 0), (0, 400)):
        vp.rect(cx_ - 15, cy_ - 15, cx_ + 15, cy_ + 15, fill=mix(C["Old Plaster"], "#000000", 0.3), width=1.5)
    vp.text(200, 40, "Wall_400", 14, "SemiBold")
    vp.text(450, 40, "_100", 14, "SemiBold")
    vp.text(30, 200, "Wall_400", 14, "SemiBold", anchor="lm")
    vp.text(60, -50, "Corner pillar 30 × 30", 14, "SemiBold", anchor="lm")
    vp.circle(0, 0, 4, fill=DIM, outline=None)
    vp.dim_h(-15, 15, -15, "30", off=34, size=12)
    vp.dim_v(-10, 10, 500, "20", off=20, size=12)
    sh.text(110, 2500, "Plan: wall centrelines sit ON grid lines; thickness 20 = ±10; walls run grid point to grid point (400 / 200 / 100). "
            "Corner = 30 × 30 × 300 pillar centred on the grid intersection; it hides the 10 cm wall overlaps at L, T and X joins "
            "(same rule as Agent 2's greybox). Pivot of every wall: bottom of the centreline at the piece's start end (grid intersection), "
            "+Z up, outside face toward −Y (Blender front).", 17, "Regular", INK, maxw=1150)
    vs = View(sh, 1560, 3240, 0.95)
    vs.grid(-60, 0, 260, 620, 100, labels=True)
    for lvl in (0, 300):
        vs.rect(-10, lvl, 10, lvl + 300 - (20 if lvl == 0 else 0), fill=C["Old Plaster"], width=1.2)
        vs.rect(-10, lvl - 20 if lvl else -20, 250, lvl, fill=C["Dry Concrete"], width=1.2)
    vs.rect(-10, 600 - 20, 250, 600, fill=C["Dry Concrete"], width=1.2)
    vs.dim_v(280, 300, 250, "20 slab", off=18, size=12)
    vs.dim_v(0, 300, -10, "storey 300", off=-36, size=12)
    sh.text(1300, 2010, "Section", 18, "Bold")
    sh.text(1300, 2040, "Floor tiles 400 × 400 × 20 with the top face on the grid level (slab occupies −20…0). Upper slabs sit inside the "
            "top 20 cm of the wall below, so storeys stack every 300 cm.", 16, "Regular", INK, maxw=700)
    # door leaf + window notes
    sh.text(110, 2660, "Separate / moving meshes", 18, "Bold", NOTE)
    sh.text(110, 2690, "Door leaf 96 × 218 × 4 (SM_Ruin_DoorLeaf, hinged on the left jamb, opens 0–100°, barricade-ready). Window glass shards "
            "and frames are separate small meshes (break → glass noise 25 m). SOCKET_Opening at the centre of every window and door opening "
            "(barricades snap there). Window 100 × 120, sill 90; door 100 × 220; lintel 130 × 20.", 17, "Regular", INK, maxw=1150)

    # ---- C: painted reference
    sh.panel(2050, 1920, 2016, 1390, "C  Painted reference", "look + materials only")
    g2 = load_raw("G02_RuinKit_Walls.png")
    ox_, oy_, w_, h_ = sh.paste(g2, 2080, 1990, 1956, 1110)
    for i, st in enumerate(STATES):
        sh.label_box(ox_ + 8, oy_ + 40 + i * (h_ / 3.05), st, 15, "Bold")
    caveat(sh, 2080, 3130, 1956,
           "Use for rendering, materials and the overgrowth read (base moss, ivy curtains from the top and openings). Drift: proportions are "
           "squarer than 400 × 300; the damaged row switched to tan render (keep the SAME plaster as intact, Old Plaster #A7A294); intact row "
           "already shows broken edges. The painted corner is an L with short legs; the kit uses a 30 × 30 pillar (drawn in A/B). Source: G02, recraft-v4.1-flash.", 16)
    sh.save(os.path.join(CONCEPT, "CA_RuinKit_Walls_Sheet.png"))


# ======================================================================== FLOORS / ROOFS / STAIRS / COLLAPSED / RUBBLE
def floor_plan(v, state, seed=0):
    r = rng(seed)
    v.rect(0, 0, 400, 400, fill=C["Dry Concrete"], width=1.5)
    # remnant floor tiles
    for i in range(10):
        for j in range(10):
            if (i + j) % 2 == 0 and r.random() < (0.75 if state == "Intact" else 0.45):
                v.rect(40 + i * 32, 40 + j * 32, 72 + i * 32, 72 + j * 32, fill=mix(C["Bone White"], C["Dry Concrete"], 0.45), outline=None)
    for _ in range(3 if state == "Intact" else 6):
        crack(v, r.uniform(40, 360), r.uniform(40, 360), n=r.randint(4, 9), seed=r.randint(0, 999), step=18)
    for k in range(6):
        v.circle(r.uniform(60, 340), r.uniform(60, 340), r.uniform(15, 40), fill=C["Wet Concrete"], outline=None, alpha=45)
    if state != "Intact":
        hx, hy = 250, 170
        pts = [(hx + math.cos(t) * r.uniform(45, 75), hy + math.sin(t) * r.uniform(40, 70)) for t in [i * 0.45 for i in range(14)]]
        v.poly([(hx + (x - hx) * 1.25, hy + (y - hy) * 1.25) for x, y in pts], fill=C["Wet Concrete"], outline=None)
        v.poly(pts, fill=VOID, width=1.5)
        for i in range(5):
            p = pts[i * 3 % len(pts)]
            rebar(v, p[0], p[1], math.degrees(math.atan2(p[1] - hy, p[0] - hx)) + 180, 22)
        scorch(v, hx, hy, 110)
    if state == "Overgrown":
        for i in range(10):
            ivy_cluster(v, r.uniform(20, 380), r.uniform(20, 380), 12, 18, seed=seed + i, leaf=4)
        for i in range(5):
            grass_tufts(v, r.uniform(20, 380), r.uniform(20, 380), r.uniform(20, 380), 3, seed=seed + 20 + i, h=16)
        ivy_cluster(v, 250, 170, 25, 60, seed=seed + 99, cols=[C["Moss"], C["Lichen"], C["Ivy"]], leaf=6)
    v.rect(0, 0, 400, 400, fill=None, width=1.5)


def roof_profile(v, state, seed=0):
    """Side profile: eave at (0,0) (= wall top), ridge at (400, 200); 20 thick."""
    r = rng(seed)
    sag = 0 if state == "Intact" else 22
    n = 16
    top, bot = [], []
    for i in range(n + 1):
        t = i / n
        x = t * 400
        y = t * 200 - sag * math.sin(t * math.pi)
        top.append((x - 4 * t, y + 20))
        bot.append((x, y))
    v.poly(bot + top[::-1], fill=C["Rotten Wood"], width=1.5)
    # tiles sawtooth
    for i in range(n):
        if state != "Intact" and 6 <= i <= 9:
            continue
        a, b = top[i], top[i + 1]
        v.poly([a, b, (b[0], b[1] + 6), (a[0] + 3, a[1] + 6)], fill=mix(C["Weathered Brick"], C["Rust Orange"], 0.25), width=1)
    if state != "Intact":
        # hole: broken rafters
        for k in (6.5, 8.2):
            p = bot[int(k)]
            v.line([p, (p[0] + 8, p[1] - 40)], C["Rotten Wood"], 5)
            v.line([p, (p[0] + 8, p[1] - 40)], INK, 1)
        for i in range(4):
            q = top[6 + i]
            rock(v, q[0] + 5, q[1] - 70 - i * 6, 6, seed=i, col=mix(C["Weathered Brick"], C["Rust Orange"], 0.25))
    if state == "Overgrown":
        for i in range(0, n, 2):
            ivy_cluster(v, top[i][0], top[i][1] + 8, 6, 10, seed=seed + i, cols=[C["Moss"], C["Lichen"], C["Moss"]], leaf=3.5)
        sapling(v, top[8][0], top[8][1], 110, seed=seed + 5)
        for i in range(3):
            ivy_vine(v, bot[1 + i][0], bot[1 + i][1], 60, seed=seed + 30 + i, down=True)


def stairs(v, state, seed=0):
    r = rng(seed)
    n = 15
    rise, run = 20, 400 / 15
    pts = [(0, 0)]
    for i in range(n):
        pts.append((i * run, (i + 1) * rise))
        pts.append(((i + 1) * run, (i + 1) * rise))
    under = [(400, 300 - 25), (40, 0)]
    poly = pts + under
    v.poly(poly, fill=C["Dry Concrete"], width=1.5)
    if state != "Intact":
        # chunk missing from steps 6-9: cut the stepped profile down to a jagged line
        seg = [p for p in pts if 6 * run - 0.1 <= p[0] <= 9 * run + 0.1]
        a, b = seg[0], seg[-1]
        jagl = jag(r, a, b, 6, 4)
        jagl = [(x, y - 28 * math.sin(math.pi * (x - a[0]) / (b[0] - a[0]))) for x, y in jagl]
        v.poly(seg + jagl[::-1], fill=PANEL, outline=None)
        v.line(jagl, INK, 1.5)
        for k in range(3):
            q = jagl[2 + k]
            rebar(v, q[0], q[1], 70 + k * 15, 18)
        for _ in range(4):
            crack(v, r.uniform(80, 360), r.uniform(60, 220), n=4, seed=r.randint(0, 999), step=12)
        pocks(v, 50, 380, 30, 240, 10, seed=seed)
    if state == "Overgrown":
        for i in range(n):
            if state != "Intact" and 6 <= i <= 8:
                continue
            moss_band(v, i * run, (i + 1) * run, (i + 1) * rise, 4, seed=seed + i, density=1.5)
        ivy_vine(v, 380, 0, 240, seed=seed + 1, drift=-0.5)
        ivy_vine(v, 340, 0, 200, seed=seed + 2, drift=-0.3)
        grass_tufts(v, -10, 60, 0, 6, seed=seed + 3, h=20)


def collapsed_wall(v, state, seed=0):
    r = rng(seed)
    top = jag(r, (0, 150), (400, 60), 10, 14)
    v.poly([(0, 0), (400, 0)] + top[::-1], fill=C["Old Plaster"] if state == "Intact" else mix(C["Old Plaster"], C["Wet Concrete"], 0.35), width=1.5)
    v.poly([(x, y) for x, y in top] + [(400, top[-1][1] - 12)] + [(x, y - 12) for x, y in top[::-1]][1:], fill=C["Weathered Brick"], outline=None)
    for i in range(0, 10, 3):
        rebar(v, top[i][0], top[i][1], r.uniform(50, 120), r.uniform(15, 30))
    rubble_pile(v, 120, 470, 60, state, seed=seed + 1, base=0)
    if state == "Overgrown":
        for i in range(5):
            ivy_vine(v, 20 + i * 70, 0, r.uniform(50, 120), seed=seed + i)
        moss_band(v, 0, 400, 0, 25, seed=seed + 9)


def collapsed_floor(v, state, seed=0):
    r = rng(seed)
    # upper slab at 300 from x 0..170 (broken edge), fallen half hanging to ground
    col = C["Dry Concrete"] if state == "Intact" else mix(C["Dry Concrete"], C["Wet Concrete"], 0.4)
    v.rect(0, 280, 170, 300, fill=col, width=1.5)
    ang = math.radians(-48)
    L = 260
    ex, ey = 170 + math.cos(ang) * L, 300 + math.sin(ang) * L
    nx, ny = -math.sin(ang) * 20, math.cos(ang) * 20
    v.poly([(172, 300), (ex, ey), (ex - nx, ey - ny), (172 - nx, 300 - ny)], fill=col, width=1.5)
    for k in range(4):
        rebar(v, 168, 285 + k * 4, r.uniform(-60, -20), r.uniform(18, 30))
    v.rect(-10, 0, 10, 300, fill=C["Old Plaster"], width=1.2)
    rubble_pile(v, 220, 400, 40, state, seed=seed + 2, base=0)
    if state == "Overgrown":
        for i in range(4):
            ivy_vine(v, 20 + i * 40, 280, r.uniform(60, 150), seed=seed + i, down=True)
        moss_band(v, 172, ex, 0, 6, seed=seed, density=0.4)
        sapling(v, 330, 30, 130, seed=seed + 4)


def collapsed_roof(v, state, seed=0):
    r = rng(seed)
    v.rect(-10, -190, 10, 0, fill=C["Old Plaster"], width=1.2)
    v.rect(390, -190, 410, 0, fill=C["Old Plaster"], width=1.2)
    # sagged roof: eave left at 0, ridge collapsed into the room
    for k in range(0, 400, 16):
        v.line([(k, k / 2 + 20), (k + 8, (k + 8) / 2 + 20)], INK2, 1.2)
    v.text(120, 110, "original slope", 13, "Medium", INK2)
    pts_b = [(0, 0), (130, -50), (250, -170), (330, 40), (400, 200)]
    pts_t = [(x, y + 20) for x, y in pts_b]
    v.poly(pts_b + pts_t[::-1], fill=C["Rotten Wood"], width=1.5)
    for i in range(len(pts_t) - 1):
        a, b = pts_t[i], pts_t[i + 1]
        for k in range(6):
            t0 = k / 6
            p = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            v.rect(p[0], p[1], p[0] + 12, p[1] + 5, fill=mix(C["Weathered Brick"], C["Rust Orange"], 0.25), width=0.8)
    v.line([(250, -150), (225, -60)], C["Rotten Wood"], 6)
    v.line([(250, -150), (225, -60)], INK, 1)
    v.line([(262, -150), (300, -90)], C["Rotten Wood"], 6)
    v.line([(262, -150), (300, -90)], INK, 1)
    if state == "Overgrown":
        for i in range(len(pts_t)):
            ivy_cluster(v, pts_t[i][0], pts_t[i][1] + 6, 10, 18, seed=seed + i, cols=[C["Moss"], C["Lichen"], C["Ivy"]])
        sapling(v, 250, -140, 170, seed=seed + 3)


def rubble_pile(v, x0, x1, h, state, seed=0, base=0):
    r = rng(seed)
    w = x1 - x0
    mound = [(x0, base)]
    for i in range(1, 12):
        t = i / 12
        mound.append((x0 + w * t, base + h * math.sin(t * math.pi) * r.uniform(0.75, 1.1)))
    mound.append((x1, base))
    v.poly(mound, fill=C["Dry Concrete"] if state == "Intact" else mix(C["Dry Concrete"], C["Wet Concrete"], 0.45), width=1.3)
    for _ in range(int(w / 12)):
        x = r.uniform(x0 + 10, x1 - 10)
        t = (x - x0) / w
        y = base + r.uniform(0, h * math.sin(t * math.pi) * 0.9)
        if r.random() < 0.45:
            v.rect(x, y, x + 11, y + 6, fill=C["Weathered Brick"], width=0.8)
        else:
            rock(v, x, y, r.uniform(4, 10), seed=r.randint(0, 999), col=r.choice([C["Dry Concrete"], C["Old Plaster"], C["Wet Concrete"]]))
    for _ in range(max(1, int(w / 120))):
        x = r.uniform(x0 + 20, x1 - 20)
        rebar(v, x, base + h * 0.5, r.uniform(30, 150), r.uniform(20, 40))
    if r.random() < 0.7:
        v.poly([(x0 + w * 0.2, base + h * 0.5), (x0 + w * 0.6, base + h * 0.9), (x0 + w * 0.6, base + h * 0.9 + 5), (x0 + w * 0.2, base + h * 0.5 + 5)],
               fill=C["Rotten Wood"], width=1)
    if state == "Overgrown":
        grass_tufts(v, x0, x1, base, int(w / 10), seed=seed + 1, h=20)
        for i in range(int(w / 50)):
            ivy_cluster(v, r.uniform(x0 + 10, x1 - 10), base + r.uniform(5, h * 0.8), 8, 14, seed=seed + 10 + i, cols=[C["Moss"], C["Lichen"], C["Ivy"]])


def rubble(v, state, seed=0):
    rubble_pile(v, 0, 400, 120, state, seed=seed)
    rubble_pile(v, 440, 640, 80, state, seed=seed + 5)


def build_floors():
    sh = Sheet(4096, 2200)
    sh.title_block("Modular ruin kit · Floors, roofs, stairs, collapsed pieces, rubble",
                   "CA_RuinKit_FloorsRoofsStairs_Sheet.png", "100 cm grid · all dimensions in cm",
                   "Drawn views are authoritative")
    caveat(sh, 30, 122, 4036,
           "Painted reference for this sheet BLOCKED: generation refused (free-tier daily image limit, 2026-11-07). Use the wall sheet's painted "
           "reference (CA_RuinKit_Walls_Sheet.png, panel C) for rendering and materials. For collapsed pieces and rubble the three states are "
           "Fresh (= _Intact: clean breaks, dust), Weathered (= _Damaged: stained, softened, more debris) and Overgrown.", 18)
    rows = [
        ("Floor tile · SM_Ruin_Floor_400", floor_plan, 0.85, (0, 0, 400, 400), "plan", 470),
        ("Roof slope · SM_Ruin_Roof_400", roof_profile, 1.05, (0, 0, 400, 220), "side profile (eave on wall top)", 330),
        ("Stairs · SM_Ruin_Stairs_300", stairs, 1.0, (0, 0, 400, 300), "side elevation", 380),
        ("Collapsed wall · SM_Ruin_WallCollapsed_400", collapsed_wall, 1.0, (0, 0, 400, 300), "elevation", 0),
    ]
    rows2 = [
        ("Collapsed floor · SM_Ruin_FloorCollapsed_400", collapsed_floor, 0.9, (0, 0, 400, 300), "section", 0),
        ("Collapsed roof · SM_Ruin_RoofCollapsed_400", collapsed_roof, 1.0, (0, -200, 400, 220), "side profile, walls below", 0),
        ("Rubble piles · SM_Ruin_Rubble_400 / _200", rubble, 0.85, (0, 0, 640, 150), "elevation", 0),
    ]
    y = 200
    # left group: rows; each row a panel spanning full width with 3 states
    heights = [560, 420, 460, 440]
    for (title, fn, s, box, view, _), hgt in zip(rows, heights):
        sh.panel(30, y, 2400, hgt, title, view)
        for i, st in enumerate(STATES):
            ox = 110 + i * 780
            oy = y + hgt - 70 if box[1] >= 0 else y + 70 + box[3] * s
            v = View(sh, ox, oy, s)
            v.grid(box[0], box[1], box[2], box[3], 100, labels=(i == 0), ground=(box[1] >= 0 and fn is not floor_plan))
            fn(v, st, seed=31 + i * 7)
            sh.label_box(ox + box[2] * s + 18, y + 60, "_" + st, 15, "Bold", "#FFFFFF", {0: "#4E5457", 1: "#7A4A3A", 2: "#3F5236"}[i])
        y += hgt + 18
    yr = 200
    heights2 = [480, 520, 400]
    for (title, fn, s, box, view, _), hgt in zip(rows2, heights2):
        sh.panel(2450, yr, 1616, hgt, title, view)
        for i, st in enumerate(STATES):
            sc = s * (0.95 if fn is not rubble else 0.88)
            ox = 2510 + i * 520
            oy = yr + hgt - 60 if box[1] >= 0 else yr + 100 + box[3] * sc
            v = View(sh, ox, oy, sc)
            v.grid(box[0], box[1], box[2], box[3], 100, labels=False, ground=True)
            fn(v, st, seed=51 + i * 5)
            sh.label_box(ox, yr + 60, "_" + st, 15, "Bold", "#FFFFFF", {0: "#4E5457", 1: "#7A4A3A", 2: "#3F5236"}[i])
        yr += hgt + 18
    # dimension annotations on the intact views
    v = View(sh, 110, 200 + 560 - 70, 0.85)
    v.dim_h(0, 400, 400, "400", off=-22, size=13)
    v.dim_v(0, 400, 400, "400", off=22, size=13)
    y2 = 200 + 560 + 18
    v = View(sh, 110, y2 + 420 - 70, 1.05)
    v.dim_v(0, 200, 400, "rise 200", off=22, size=13)
    v.dim_h(0, 400, 0, "run 400 (26.6°)", off=26, size=13)
    y3 = y2 + 420 + 18
    v = View(sh, 110, y3 + 460 - 70, 1.0)
    v.dim_v(0, 300, 400, "300 = 15 × 20", off=22, size=13)
    v.dim_h(0, 400, 0, "400 = 15 × 26.7", off=26, size=13)
    y4 = y3 + 460 + 18
    v = View(sh, 110, y4 + 440 - 70, 1.0)
    v.dim_v(0, 150, 0, "max 150", off=-40, size=13)

    # notes panel bottom right
    yn = yr
    sh.panel(2450, yn, 1616, 2170 - yn, "Notes for Agent 2", None)
    notes = ("• Floor tile 400 × 400 × 20, top face on the grid level; remnant floor tiles are a decal/trim, not geometry. Damaged: Ø≈120 shell hole "
             "with rebar, cracks, scorch. Overgrown: moss patches, grass in cracks, a bush through the hole.\n"
             "• Roof slope covers 400 × 400 in plan, eave on the wall top (300), rise 200 over 400 (26.6°), 20 thick (rafters + clay tiles "
             "#9A5537-ish = Weathered Brick + Rust Orange). Gable end = triangle 400 × 200 × 20 in the wall plaster; ridge cap 400 long. Damaged: "
             "sag 22, missing tiles over two rafters.\n"
             "• Stairs: straight concrete flight, 100 wide, 15 risers × 20 = 300, 15 treads × 26.7 = 400, footprint 400 × 100.\n"
             "• Collapsed wall: 400 long, broken top 60–150, rubble skirt. Collapsed floor: upper slab broken at 170, half hanging to the ground. "
             "Collapsed roof: ridge fallen into the room. Rubble: 400 × 200 × 120 and 200 × 200 × 80 piles (brick, concrete, rebar, a plank).\n"
             "• All pieces: pivot at the bottom-left grid corner; custom UCX collision (rubble: 2–3 simple hulls, walkable).")
    sh.text(2480, yn + 70, notes, 16, "Regular", INK, maxw=1560, lh=1.32)
    scale_figure(View(sh, 2380, 200 + 560 - 70 + 0, 0.85), 0, label=False)
    sh.save(os.path.join(CONCEPT, "CA_RuinKit_FloorsRoofsStairs_Sheet.png"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["walls", "floors"]
    if "walls" in which:
        build_walls()
    if "floors" in which:
        build_floors()
