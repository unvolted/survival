"""Player-built structure sheets (Agent 1).

Builds:
  Concept/CA_Buildables_Walls_Sheet.png      log wall T1/T2/T3, spiked wall, metal plate kit, log mesh, damage states
  Concept/CA_Buildables_GateTower_Sheet.png  barricaded door/window, welded gate, watchtower (T1/T2/T3)
  Concept/CA_Buildables_Traps_Sheet.png      spike pit, barbed wire, noise trap, tripwire, deadfall, snare, burn trench
  Concept/CA_Buildables_Ghost_Sheet.png      ghost / blueprint look

All dimensions in cm. Numbers from Design/ROOTFALL_Brief.md (30 cm logs, 10 logs = 300 cm, up to 400 cm long,
plates 2 cm proud); everything else is an Agent 1 assumption listed in the report.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sheetlib import *  # noqa: E402,F401,F403

# ---------------------------------------------------------------- shared wall geometry
LOG_D = 30
WALL_L = 400
N_LOGS = 10
PLANK_X = (50, 150, 250, 350)
PLANK_W, PLANK_T = 25, 4
PLATE_GAP, PLATE_T = 2, 1


def wall_t1(v, x0=0, L=WALL_L, seed=1):
    for i in range(N_LOGS):
        log_h(v, x0, x0 + L, LOG_D / 2 + i * LOG_D, LOG_D, seed=seed * 100 + i)


def wall_t2(v, x0=0, L=WALL_L, seed=1):
    wall_t1(v, x0, L, seed)
    for k, px_ in enumerate(PLANK_X):
        if px_ > L:
            continue
        nails = []
        for i in range(N_LOGS):
            yc = LOG_D / 2 + i * LOG_D
            nails += [(x0 + px_ - 6, yc), (x0 + px_ + 6, yc)]
        plank(v, x0 + px_ - PLANK_W / 2, 0, x0 + px_ + PLANK_W / 2, 300, seed=seed * 10 + k, nails=nails)


def wall_t3(v, x0=0, L=WALL_L, seed=1):
    k = 0
    for xx in range(0, L, 100):
        for yy in (0, 150):
            plate(v, x0 + xx, yy, x0 + xx + 100, yy + 150, seed=seed * 50 + k)
            k += 1


def wall_end(v, cx, tier, seed=3):
    """End/section view: depth along x (outside face to the right), height up."""
    for i in range(N_LOGS):
        log_end(v, cx + LOG_D / 2, LOG_D / 2 + i * LOG_D, LOG_D, seed=seed + i)
    if tier >= 2:
        v.rect(cx + LOG_D, 0, cx + LOG_D + PLANK_T, 300, fill=C["Weathered Plank"], width=1.5)
    if tier >= 3:
        p0 = cx + LOG_D + PLANK_T + PLATE_GAP
        for yy in (20, 130, 170, 280):
            v.rect(cx + LOG_D + PLANK_T, yy - 3, p0, yy + 3, fill=C["Weld Scorch"], width=1)
        v.rect(p0, 0, p0 + PLATE_T, 150, fill=C["Steel"], width=1.5)
        v.rect(p0, 150, p0 + PLATE_T, 300, fill=C["Steel"], width=1.5)


def spikes_front(v, x0=0, tier=1, L=WALL_L, crown=True):
    rise = 140 * math.sin(math.radians(20))
    col = C["Steel"] if tier == 3 else None
    tipc = C["Rust Orange"] if tier == 3 else None
    d = 4 if tier == 3 else 8
    for row_y in (90, 190):
        for i in range(8):
            x = x0 + 25 + 50 * i
            if x > x0 + L:
                continue
            v.circle(x, row_y, d / 2 + 0.5, fill=col or C["Bark"], width=1.2)
            stake(v, x, row_y, 90, rise, d=d, tip=10, col=col, tipcol=tipc)
    if crown:
        for i in range(8):
            x = x0 + 25 + 50 * i
            stake(v, x, 300, 90, 80, d=d, tip=30, col=col, tipcol=tipc)


def spikes_side(v, cx, tier=1, face=None):
    face = face if face is not None else {1: 30, 2: 34, 3: 37}[tier]
    col = C["Steel"] if tier == 3 else None
    tipc = C["Rust Orange"] if tier == 3 else None
    d = 4 if tier == 3 else 8
    for row_y in (90, 190):
        stake(v, cx + 2, row_y, 20, 140, d=d, tip=25 if tier < 3 else 15, col=col, tipcol=tipc)
    stake(v, cx - 4, 200, 90, 180, d=d, tip=30, col=col, tipcol=tipc)


def damage_t1(v, x0, state, seed=7):
    """T1 wall in Intact / Damaged / Broken state (schematic)."""
    r = rng(seed)
    if state == "Intact":
        wall_t1(v, x0, seed=seed)
        return
    keep = N_LOGS if state == "Damaged" else 6
    for i in range(keep):
        yc = LOG_D / 2 + i * LOG_D
        if state == "Broken" and i == keep - 1:
            log_h(v, x0, x0 + 230, yc, LOG_D, seed=seed * 100 + i)
            # snapped end
            v.poly([(x0 + 230, yc - 15), (x0 + 246, yc - 6), (x0 + 236, yc), (x0 + 252, yc + 7), (x0 + 230, yc + 15)], fill=C["Fresh-cut Wood"], width=1.2)
            continue
        log_h(v, x0, x0 + WALL_L, yc, LOG_D, seed=seed * 100 + i)
    # claw gouges and split logs (fresh wood showing)
    n = 7 if state == "Damaged" else 12
    for _ in range(n):
        gx = x0 + r.uniform(40, 360)
        gy = r.uniform(30, 150 if state == "Damaged" else 140)
        for k in range(3):
            v.line([(gx + k * 4, gy), (gx + k * 4 + r.uniform(-3, 3), gy - r.uniform(12, 22))], C["Fresh-cut Wood"], 2)
    if state == "Damaged":
        v.poly([(x0 + 150, 135), (x0 + 210, 138), (x0 + 205, 147), (x0 + 152, 145)], fill=C["Fresh-cut Wood"], width=1.2)
        v.poly([(x0 + 270, 225), (x0 + 330, 222), (x0 + 326, 230), (x0 + 272, 232)], fill=C["Fresh-cut Wood"], width=1.2)
    else:
        # fallen log leaning against the base
        v.poly([(x0 + 260, 0), (x0 + 420, 70), (x0 + 412, 92), (x0 + 252, 22)], fill=C["Bark"], width=1.5)
        log_end(v, x0 + 416, 81, 26, seed=seed)
        # splinters on broken top
        for i in range(8):
            sx = x0 + 10 + i * 45 + r.uniform(-6, 6)
            v.poly([(sx, 180), (sx + 8, 180), (sx + 3 + r.uniform(-3, 3), 180 + r.uniform(12, 30))], fill=C["Fresh-cut Wood"], width=1)


# ======================================================================== WALLS SHEET
def build_walls():
    sh = Sheet(4096, 2860)
    sh.title_block("Player-built structures · Log walls, spiked walls, metal plating",
                   "CA_Buildables_Walls_Sheet.png", "100 cm grid · all dimensions in cm",
                   "Drawn elevations are authoritative; painted reference is for look and material only")

    # ---------------- Panel A: log wall tiers
    sh.panel(30, 130, 2690, 1120, "A  Log wall · SM_Build_LogWall", "T1 log · T2 log + plank · T3 metal-plated   (front elevation + end section)")
    s = 1.65
    tiers = [(1, "T1 · log", wall_t1), (2, "T2 · log + plank", wall_t2), (3, "T3 · metal-plated", wall_t3)]
    bx = 150
    for idx, (t, name, fn) in enumerate(tiers):
        ox = bx + idx * 840
        v = View(sh, ox, 860, s)
        v.grid(0, 0, 400, 300, 100, labels=True)
        if t == 3:
            wall_t2(v)  # T3 sits on T2
        fn(v)
        sh.label_box(ox, 220, name, 22, "Bold", "#FFFFFF", {1: C["Bark"], 2: "#6B5E48", 3: "#4E5457"}[t])
        sh.text(ox + 4, 262, "front elevation (outside face)", 16, "Regular", INK2)
        v.dim_h(0, 400, 0, "400 cm (max segment)", off=46, ext_from=0)
        v.dim_v(0, 300, 0, "300 cm = 10 logs", off=-48, ext_from=0)
        # end section
        ve = View(sh, ox + 400 * s + 70, 860, s)
        ve.grid(0, 0, 40, 300, 100, labels=False, ground=True)
        wall_end(ve, 0, t)
        depth = {1: 30, 2: 34, 3: 37}[t]
        ve.dim_h(0, depth, 0, f"{depth}", off=46, ext_from=0, size=15)
        sh.text(ox + 400 * s + 70 + 20 * s, 262, "end section", 16, "Regular", INK2, anchor="ma")
        sh.text(ox + 400 * s + 70 + 20 * s, 282, "outside →", 14, "Regular", INK2, anchor="ma")
        if t == 1:
            ve.dim_v(15, 45, 0, "Ø30", off=-26, size=13)
    scale_figure(View(sh, 2655, 860, s), 0)

    notes = [
        ("T1  SM_Build_LogWall_T1", "10 logs Ø30 × 400, stacked tangent (no notching), bark on, axe-cut fresh ends. "
         "Each log is its own element so the ghost fills one log per deposit (Forest flow). Pivot: bottom-left corner on grid, "
         "front faces outside. Snap points at both ends every 100 cm."),
        ("T2  SM_Build_LogWall_T2", "T1 + 4 vertical planks 25 × 4 × 300 on the OUTSIDE face at 50 / 150 / 250 / 350, 2 nails per log per plank. "
         "Planks are separate meshes, added one at a time. Weathered scavenged wood, not new timber."),
        ("T3  SM_Build_LogWall_T3", "T2 + 8 scrap steel plates 100 × 150 × 1 (separate meshes, SM_Build_MetalPlate_100x150). "
         "Plate back face sits 2 cm proud of the plank face on welded steel tabs (no z-fighting). Rust streaks run down from the top edge "
         "and from weld seams."),
    ]
    yy = 1000
    for i, (hd, body) in enumerate(notes):
        x = 150 + i * 840
        sh.text(x, yy, hd, 18, "Bold", NOTE)
        sh.text(x, yy + 28, body, 18, "Regular", INK, maxw=780)

    # ---------------- Panel B: painted reference
    sh.panel(2740, 130, 1326, 1120, "B  Painted reference", "look + materials only")
    g1 = load_raw("G01_Buildables_Walls.png")
    ox_, oy_, w_, h_ = sh.paste(g1, 2770, 200, 1266, 724)
    for i, t in enumerate(["T1", "T2", "T3"]):
        sh.label_box(ox_ + 60 + i * 420, oy_ + 10, t, 18, "Bold")
    y2 = caveat(sh, 2770, 945, 1266,
                "Drift: the painting shows 11 logs and a tall narrow panel, and its T3 plates sit straight on the logs. "
                "Follow panel A for geometry (10 logs, 400 × 300, plates over T2 planks). Cut-end orange is over-saturated: "
                "use Fresh-cut Wood #C9A26B.")
    sh.text(2770, y2 + 14, "Source: recraft-v4.1-flash, Concept/_raw/G01_Buildables_Walls.png (see report for prompt).", 15, "Regular", INK2, maxw=1266)

    # ---------------- Panel C: spiked wall
    sh.panel(30, 1270, 2140, 1560, "C  Spiked wall · SM_Build_SpikeSet (add-on)", "wall + sharpened stakes; one spike set layers onto any log wall tier")
    s2 = 1.05
    for idx, t in enumerate((1, 2, 3)):
        ox = 130 + idx * 690
        v = View(sh, ox, 1835, s2)
        v.grid(0, 0, 400, 400, 100, labels=(idx == 0))
        {1: wall_t1, 2: wall_t2, 3: lambda vv: (wall_t2(vv), wall_t3(vv))}[t](v)
        spikes_front(v, 0, t)
        sh.label_box(ox, 1345, {1: "T1 · sticks on log wall", 2: "T2 · sticks on plank wall", 3: "T3 · rebar spikes on plated wall"}[t], 19, "Bold",
                     "#FFFFFF", {1: C["Bark"], 2: "#6B5E48", 3: "#4E5457"}[t])
        v.dim_h(0, 400, 0, "400", off=40, ext_from=0, size=15)
        if idx == 0:
            v.dim_v(0, 380, 0, "380 incl. crown", off=-46, ext_from=0, size=15)
    vside = View(sh, 200, 2770, 1.75)
    vside.grid(-30, 0, 200, 400, 100, labels=True)
    for i in range(N_LOGS):
        log_end(vside, 15, 15 + 30 * i, 30, seed=40 + i)
    spikes_side(vside, 0, 1, 30)
    vside.dim_h(30, 133.6, 90, "≈104 in front of face", off=30, size=14)
    vside.line([(2, 90), (60, 90)], DIM, 1)
    vside.text(70, 104, "20°", 15, "Bold", DIM)
    vside.dim_v(300, 380, -4, "80 above top", off=-40, size=14)
    vside.dim_v(200, 300, -4, "100 lashed", off=-40, size=14)
    sh.text(150, 1935, "Side section T1 (outside → right)", 20, "Bold")
    cnotes = ("Stakes Ø8, 140 long, fire-hardened 25 cm tip (Fresh-cut Wood tip, charred edge). Two rows at 90 and 190 cm, 8 per row at "
              "50 cm centres (x = 25 … 375), driven between logs at 20° above horizontal, tips ≈100 cm in front of the face, at zombie chest and head height. "
              "Crown: 8 vertical stakes Ø8 × 180 lashed to the inside face from 200 cm, 80 cm above the wall top (total height 380). "
              "T2: same stakes, nailed through the planks. T3: Ø4 sharpened rebar / scrap spikes welded to the plates, same layout, rusted tips. "
              "Spike set = one separate mesh per tier (SM_Build_SpikeSet_T1/T2/T3), pivot shared with the wall. Damage-back is gameplay; "
              "show dark stains (Dried Blood #4E2320) on tips in the Damaged state.")
    sh.text(760, 1960, "Notes", 20, "Bold", NOTE)
    y3 = sh.text(760, 1992, cnotes, 18, "Regular", INK, maxw=1360) + 16
    g3 = load_raw("G03_Buildables_SpikeGateBarricade.png").crop((0, 0, 410, 768))
    g3 = ImageEnhance.Color(g3).enhance(0.7)
    sh.text(760, y3, "Painted reference (look only)", 18, "Bold")
    px_, py_, pw_, ph_ = sh.paste(g3, 760, y3 + 30, None, 2800 - y3 - 60)
    caveat(sh, px_ + pw_ + 30, y3 + 30, 2120 - (px_ + pw_ + 30),
           "Drift: outlined cartoon rendering, logs stacked unevenly and stakes driven straight through log ends; cropped at the frame edge. "
           "Use it only for the idea: horizontal stakes between logs plus a vertical crown. Geometry = drawings on this panel. "
           "Saturation reduced 30% toward the palette (raw file unchanged in Concept/_raw).")

    # ---------------- Panel D: plate kit + offset detail
    sh.panel(2190, 1270, 1876, 760, "D  Metal plating · plate kit + 2 cm offset", "scrap steel sheets welded on any wall piece")
    vp = View(sh, 2260, 1900, 1.25)
    vp.grid(0, 0, 360, 150, 50, labels=False, ground=False)
    plate(vp, 0, 0, 100, 150, seed=81)
    plate(vp, 130, 0, 230, 100, seed=82)
    plate(vp, 260, 0, 310, 150, seed=83)
    vp.dim_h(0, 100, 0, "100", off=28, size=14)
    vp.dim_v(0, 150, 0, "150", off=-26, size=14)
    vp.dim_h(130, 230, 0, "100", off=28, size=14)
    vp.dim_v(0, 100, 130, "100", off=-26, size=14)
    vp.dim_h(260, 310, 0, "50", off=28, size=14)
    vp.text(50, 168, "MetalPlate_100x150", 14, "SemiBold", INK)
    vp.text(180, 118, "MetalPlate_100x100", 14, "SemiBold", INK)
    vp.text(285, 168, "_50x150", 14, "SemiBold", INK)
    sh.text(2260, 1990, "Plate thickness 1 cm (modelled), bevelled edges, weld bead 1.5 cm in from edge.\nSOCKET_PlateMount at each plate slot on every wall piece.", 15, "Regular", INK)
    # zoomed section
    vz = View(sh, 3480, 1960, 7.0)
    sh.text(3330, 1335 + 30, "Section detail (scale ×5)", 18, "Bold")
    vz.circle(-2, 30, 15, fill=C["Bark"], width=1.5)
    vz.circle(-2, 30, 12.8, fill=C["Fresh-cut Wood"], outline=None)
    vz.circle(-2, 60, 15, fill=C["Bark"], width=1.5)
    vz.circle(-2, 60, 12.8, fill=C["Fresh-cut Wood"], outline=None)
    vz.rect(13, 12, 17, 78, fill=C["Weathered Plank"], width=1.5)
    vz.rect(17, 40, 19, 46, fill=C["Weld Scorch"], width=1)
    vz.rect(19, 12, 20, 78, fill=C["Steel"], width=1.5)
    vz.dim_h(13, 17, 78, "4 plank", off=-22, size=13)
    vz.dim_h(17, 19, 12, "2 gap", off=24, size=13)
    vz.dim_h(19, 20, 12, "1", off=50, size=13)
    vz.callout(18, 43, 3720, 1700, "welded steel tab bridges the 2 cm gap", 220, 15)
    vz.callout(19.5, 70, 3720, 1560, "plate back face 2 cm proud of wood", 220, 15)
    vz.callout(-2, 60, 3290, 1560, "log Ø30 (crown at 15)", 160, 15, anchor="ra")

    # ---------------- Panel E: log mesh + damage states
    sh.panel(2190, 2050, 1876, 780, "E  Log mesh + damage states", "Intact > 66% HP · Damaged 33–66% · Broken < 33% · 0 HP = physics debris")
    vl = View(sh, 2260, 2190, 0.9)
    log_h(vl, 0, 400, 15, 30, seed=91)
    vle = View(sh, 2260 + 400 * 0.9 + 40, 2190, 0.9)
    log_end(vle, 15, 15, 30, seed=92)
    vl.dim_h(0, 400, 0, "SM_Build_Log · Ø30 × 400 (free-form walls: one repeatable log, cut ends)", off=22, size=14)
    for i, st in enumerate(("Intact", "Damaged", "Broken")):
        ox = 2260 + i * 600
        v = View(sh, ox, 2700, 1.1)
        v.grid(0, 0, 400, 300, 100, labels=False)
        damage_t1(v, 0, st, seed=7 + i)
        sh.label_box(ox, 2330, "_" + st, 17, "Bold")
    sh.text(2260, 2730, "Damaged: claw gouges and split logs show Fresh-cut Wood. Broken: top logs gone, one snapped log, a fallen log, splinters. "
            "Same states for T2 (loose / missing planks) and T3 (plates bent off, hanging on one weld).", 15, "Regular", INK, maxw=1790)

    sh.save(os.path.join(CONCEPT, "CA_Buildables_Walls_Sheet.png"))


# ======================================================================== GATE / BARRICADE / TOWER SHEET
def plank_rot(v, cx, cy, L, W, ang, seed=0, col=None, nails_at=(), steel=False):
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    pts = [(cx - ux * L / 2 - nx * W / 2, cy - uy * L / 2 - ny * W / 2), (cx + ux * L / 2 - nx * W / 2, cy + uy * L / 2 - ny * W / 2),
           (cx + ux * L / 2 + nx * W / 2, cy + uy * L / 2 + ny * W / 2), (cx - ux * L / 2 + nx * W / 2, cy - uy * L / 2 + ny * W / 2)]
    col = col or C["Weathered Plank"]
    v.poly(pts, fill=col, width=1.5)
    r = rng(seed)
    for k in (-0.25, 0.2):
        v.line([(cx - ux * (L / 2 - 4) + nx * W * k, cy - uy * (L / 2 - 4) + ny * W * k),
                (cx + ux * (L / 2 - 4) + nx * W * k, cy + uy * (L / 2 - 4) + ny * W * k)], mix(col, "#000000", 0.28), 1)
    for t in nails_at:
        for k in (-0.25, 0.25):
            v.circle(cx + ux * L * t + nx * W * k, cy + uy * L * t + ny * W * k, 1.3, fill="#2A2A2A", outline=None)


def ruin_wall_patch(v, x0, x1, y0, y1, holes, seed=0):
    """Plain grey ruin wall section with rectangular openings (x0, y0, x1, y1)."""
    v.rect(x0, y0, x1, y1, fill=C["Old Plaster"], width=1.5)
    r = rng(seed)
    for _ in range(int((x1 - x0) * (y1 - y0) / 1500)):
        bx, by = r.uniform(x0 + 5, x1 - 25), r.uniform(y0 + 5, y1 - 10)
        v.rect(bx, by, bx + 22, by + 7, fill=C["Weathered Brick"], outline=None, alpha=110)
    v.rect(x0, y0, x1, y0 + 25, fill=C["Wet Concrete"], outline=None, alpha=110)
    for (a, b, c, d) in holes:
        v.rect(a, b, c, d, fill="#1E2124", width=1.5)


def barricade(v, kind, tier, ox, oy_floor=0):
    """Barricade in a ruin opening. kind: 'window' (100 x 120, sill 90) or 'door' (100 x 210)."""
    if kind == "window":
        hole = (ox + 50, 90, ox + 150, 210)
    else:
        hole = (ox + 50, 0, ox + 150, 220)
    ruin_wall_patch(v, ox, ox + 200, 0, 300, [hole], seed=int(ox))
    x0, y0, x1, y1 = hole
    cx = (x0 + x1) / 2
    if tier == 1:
        n = 4 if kind == "window" else 7
        for i in range(n):
            yc = y0 + 14 + i * ((y1 - y0 - 28) / (n - 1))
            log_h(v, x0 - 20, x1 + 20, yc, 10, seed=int(ox) + i, ends=True)
            v.circle(x0 - 10, yc, 1.4, fill="#2A2A2A", outline=None)
            v.circle(x1 + 10, yc, 1.4, fill="#2A2A2A", outline=None)
    elif tier == 2:
        r = rng(int(ox))
        n = 4 if kind == "window" else 6
        for i in range(n):
            yc = y0 + 16 + i * ((y1 - y0 - 32) / (n - 1))
            plank_rot(v, cx, yc, 140, 20, r.uniform(-8, 8), seed=i, nails_at=(-0.43, 0.43))
        plank_rot(v, cx, (y0 + y1) / 2, math.hypot(110, y1 - y0 - 10), 20, math.degrees(math.atan2(y1 - y0 - 10, 110)), seed=9, nails_at=(-0.45, 0.45))
    else:
        plate(v, x0 - 15, y0 - (0 if kind == "door" else 15), x1 + 15, y1 + 15, seed=int(ox) + 3, welds=True, rust=0.6)
        for yy in ((y0 + 15, y1 - 10) if kind == "window" else (y0 + 20, (y0 + y1) / 2, y1 - 10)):
            v.rect(x0 - 22, yy - 4, x0 - 12, yy + 4, fill=C["Weld Scorch"], width=1)
            v.rect(x1 + 12, yy - 4, x1 + 22, yy + 4, fill=C["Weld Scorch"], width=1)


def gate(v, tier):
    pole = lambda x: pole_v(v, x, 0, 320, 40, seed=int(x))  # noqa: E731
    pole(20)
    pole(380)
    for leaf, (lx0, lx1) in enumerate(((40, 200), (200, 360))):
        if tier == 1:
            for i in range(10):
                pole_v(v, lx0 + 8 + i * 16, 10, 290 - (i % 2) * 6, 15, seed=leaf * 20 + i, sharpen=18)
            for yy in (60, 240):
                log_h(v, lx0 + 2, lx1 - 2, yy, 12, seed=leaf * 5 + yy, ends=False)
            v.line([(lx0 + 10, 66), (lx1 - 10, 234)] if leaf == 0 else [(lx1 - 10, 66), (lx0 + 10, 234)], C["Bark"], 6)
            for yy in (60, 240):
                hx = lx0 if leaf == 0 else lx1
                rope(v, [(hx - 12, yy + 8), (hx + 6, yy - 8)], 3)
                rope(v, [(hx - 12, yy - 8), (hx + 6, yy + 8)], 3)
        elif tier == 2:
            for i in range(8):
                plank(v, lx0 + i * 20, 10, lx0 + i * 20 + 20, 290, seed=leaf * 10 + i, nails=[(lx0 + i * 20 + 10, 60), (lx0 + i * 20 + 10, 240)])
            for yy in (60, 240):
                plank_rot(v, (lx0 + lx1) / 2, yy, 160, 18, 0, seed=yy)
            dy = 180
            plank_rot(v, (lx0 + lx1) / 2, 150, math.hypot(140, dy), 18, math.degrees(math.atan2(dy, 140)) * (1 if leaf else -1), seed=3 + leaf)
            hx = lx0 if leaf == 0 else lx1
            for yy in (60, 240):
                v.rect(hx - 4 if leaf == 0 else hx - 60, yy - 4, hx + 60 if leaf == 0 else hx + 4, yy + 4, fill="#3C3B3A", width=1)
        else:
            plate(v, lx0 + 2, 10, lx1 - 2, 290, seed=leaf + 70, rust=0.5)
            for yy in (10, 150, 285):
                v.rect(lx0 + 2, yy, lx1 - 2, yy + 5, fill=C["Weld Scorch"], width=1)
            v.rect(lx0 + 2, 10, lx0 + 7, 290, fill=C["Weld Scorch"], width=1)
            v.rect(lx1 - 7, 10, lx1 - 2, 290, fill=C["Weld Scorch"], width=1)
            hx = lx0 if leaf == 0 else lx1
            for yy in (40, 150, 260):
                v.rect(hx - 6, yy - 8, hx + 6, yy + 8, fill="#2F3133", width=1)
    if tier == 3:
        v.rect(30, 145, 370, 155, fill="#3C4042", width=1.5)
        v.rect(160, 135, 175, 165, fill="#2F3133", width=1)
        v.rect(225, 135, 240, 165, fill="#2F3133", width=1)


def gate_plan(v, tier):
    v.circle(20, 20, 20, fill=C["Bark"], width=1.5)
    v.circle(380, 20, 20, fill=C["Bark"], width=1.5)
    th = {1: 15, 2: 4 + 18, 3: 8}[tier]
    v.rect(40, 20 - th / 2, 200, 20 + th / 2, fill=C["Weathered Plank"] if tier == 2 else (C["Steel"] if tier == 3 else C["Bark"]), width=1.2)
    v.rect(200, 20 - th / 2, 360, 20 + th / 2, fill=C["Weathered Plank"] if tier == 2 else (C["Steel"] if tier == 3 else C["Bark"]), width=1.2)
    for hx, sgn in ((40, 1), (360, -1)):
        pts = [(hx + sgn * 160 * math.cos(math.radians(a)), 20 - 160 * math.sin(math.radians(a))) for a in range(0, 91, 5)]
        v.line(pts, DIM, 1.2)
    v.line([(40, 20), (40, -140)], DIM, 1.2)
    v.line([(360, 20), (360, -140)], DIM, 1.2)


def tower(v, tier, x0=0):
    # legs
    for xc in (12.5, 187.5):
        pole_v(v, x0 + xc, 0, 500, 25, seed=int(xc) + tier)
    # cross bracing (front face)
    for (ya, yb) in ((0, 200), (200, 390)):
        v.line([(x0 + 25, ya + 10), (x0 + 175, yb - 10)], C["Bark"], 9)
        v.line([(x0 + 175, ya + 10), (x0 + 25, yb - 10)], C["Bark"], 9)
        v.line([(x0 + 25, ya + 10), (x0 + 175, yb - 10)], INK, 1)
        v.line([(x0 + 175, ya + 10), (x0 + 25, yb - 10)], INK, 1)
    # ladder (front, centred), rails x 75 / 125
    for xr in (75, 125):
        v.rect(x0 + xr - 5, 0, x0 + xr + 5, 450, fill=mix(C["Bark"], C["Lichen"], 0.2), width=1.2)
    for yy in range(30, 450, 30):
        v.rect(x0 + 70, yy - 4, x0 + 130, yy + 4, fill=C["Fresh-cut Wood"] if tier == 1 else C["Weathered Plank"], width=1)
    # deck
    if tier == 1:
        log_h(v, x0 - 10, x0 + 210, 395, 10, seed=5, ends=True)
        log_h(v, x0 - 10, x0 + 210, 385, 10, seed=6, ends=True)
    else:
        v.rect(x0 - 10, 380, x0 + 210, 400, fill=C["Weathered Plank"], width=1.5)
    # parapet 400..500
    if tier == 1:
        for yy in (430, 465, 495):
            log_h(v, x0 - 5, x0 + 205, yy, 12, seed=yy, ends=True)
        for xx in (60, 100, 140):
            pole_v(v, x0 + xx, 400, 500, 8, seed=xx)
        for xx in (25, 175):
            rope(v, [(x0 + xx - 8, 425), (x0 + xx + 8, 435)], 2)
    else:
        for i in range(10):
            plank(v, x0 + i * 20, 400, x0 + i * 20 + 20, 500, seed=i + 40, nails=[(x0 + i * 20 + 10, 420), (x0 + i * 20 + 10, 480)])
        if tier == 3:
            plate(v, x0, 400, x0 + 100, 500, seed=61, rust=0.5)
            plate(v, x0 + 100, 400, x0 + 200, 500, seed=62, rust=0.5)


def build_gatetower():
    sh = Sheet(4096, 2900)
    sh.title_block("Player-built structures · Barricades, welded gate, watchtower",
                   "CA_Buildables_GateTower_Sheet.png", "100 cm grid · all dimensions in cm",
                   "Drawn elevations are authoritative; painted reference is for look and material only")
    tcol = {1: C["Bark"], 2: "#6B5E48", 3: "#4E5457"}

    # ---------------- A: barricades
    sh.panel(30, 130, 2400, 1150, "A  Barricaded door / window · SM_Build_Barricade", "fits ruin-kit openings: window 100 × 120 (sill 90), door 100 × 220")
    s = 1.55
    names = {1: "T1 · poles", 2: "T2 · planks + nails", 3: "T3 · welded sheet"}
    for t in (1, 2, 3):
        ox = 110 + (t - 1) * 780
        sh.label_box(ox, 215, names[t], 20, "Bold", "#FFFFFF", tcol[t])
        for k, kind in enumerate(("window", "door")):
            v = View(sh, ox + k * 360, 735, s)
            v.grid(0, 0, 200, 300, 100, labels=(k == 0 and t == 1))
            barricade(v, kind, t, 0)
            sh.text(ox + k * 360 + 155, 772, kind, 16, "Medium", INK2, anchor="ma")
    v = View(sh, 110, 735, s)
    v.dim_h(50, 150, 90, "100", off=-205, size=14)
    v.dim_v(90, 210, 50, "120", off=-20, size=13)
    v.dim_v(0, 90, 50, "sill 90", off=-20, size=13)
    v2 = View(sh, 110 + 360, 735, s)
    v2.dim_v(0, 220, 150, "220", off=22, size=13)
    vb = View(sh, 110 + 780, 735, s)
    vb.dim_h(30, 170, 210 - 16, "plank 140 × 20 × 3", off=-172, size=14)
    vc = View(sh, 110 + 1560, 735, s)
    vc.dim_h(35, 165, 225, "sheet 130 × 150", off=-24, size=14)
    bnotes = ("T1: poles Ø10 × 140, 4 (window) / 7 (door), nailed into the frame 20 cm past each side. "
              "T2: planks 140 × 20 × 3, 4 / 6 across with ±8° random tilt plus one diagonal brace, 2 nails each end. "
              "T3: one scrap sheet 130 × 150 (window) or 130 × 235 (door), 1 cm thick, welded to steel angle tabs anchored in the wall; "
              "same 2 cm stand-off from the wall face as wall plates. Each pole, plank and sheet is a separate mesh added one at a time; "
              "the barricade snaps to SOCKET_Opening on ruin window and door pieces. Damaged: planks split, hanging by one nail; sheet bent outward at one corner.")
    sh.text(110, 820, bnotes, 18, "Regular", INK, maxw=1460)
    g3 = load_raw("G03_Buildables_SpikeGateBarricade.png").crop((700, 170, 1344, 768))
    g3 = ImageEnhance.Color(g3).enhance(0.55)
    sh.text(1640, 820, "Painted reference (look only)", 18, "Bold")
    px_, py_, pw_, ph_ = sh.paste(g3, 1640, 850, 460, 400)
    caveat(sh, 2120, 850, 290, "Drift: cartoon outlines, sheet painted saturated orange (saturation reduced 45% here). "
           "Use for the plank X layout and the corner-cut sheet idea only.", 15)

    # ---------------- B: welded gate
    sh.panel(30, 1300, 2400, 1570, "B  Gate · SM_Build_Gate (welded gate at T3)", "400 module · 2 leaves 160 × 280 · opens 90° inward")
    s2 = 1.6
    gnames = {1: "T1 · log gate, rope hinges", 2: "T2 · plank gate, strap hinges", 3: "T3 · welded steel gate"}
    for t in (1, 2, 3):
        ox = 110 + (t - 1) * 780
        sh.label_box(ox, 1380, gnames[t], 20, "Bold", "#FFFFFF", tcol[t])
        v = View(sh, ox, 1960, s2)
        v.grid(0, 0, 400, 300, 100, labels=(t == 1))
        gate(v, t)
        vp = View(sh, ox, 2070, s2 * 0.8)
        gate_plan(vp, t)
        sh.text(ox + 330, 2160, "plan · leaves swing\n90° inward (down)", 15, "Regular", INK2)
        if t == 1:
            v.dim_h(0, 400, 0, "400", off=34, size=14, ext_from=0)
            v.dim_h(40, 200, 290, "leaf 160", off=-32, size=14)
            v.dim_v(10, 290, 200, "280", off=20, size=13)
            v.dim_v(0, 320, 20, "post Ø40 × 320", off=-58, size=13)
    gnotes = ("Posts Ø40, 320 above ground (+60 below ground), at x 0–40 and 360–400; clear opening 320. Two leaves 160 × 280, 10 cm ground gap. "
              "Moving parts (separate meshes): leaf L and leaf R rotate about vertical hinge axes on the inner post faces, 0–90° inward; "
              "T3 drop bar 340 × 10 × 10 slides in two welded brackets (separate mesh, moving). "
              "T1: 10 sharpened poles Ø15 per leaf on 2 rails + diagonal brace, lashed with rope hinges. "
              "T2: 8 planks 20 wide per leaf on rails + Z-brace, scavenged iron strap hinges. "
              "T3 (the brief's welded gate): 5 × 5 steel box frame with mid rail, 1 cm sheet welded on, 3 barrel hinges per leaf (SOCKET_Hinge_L/R_0–2). "
              "Damaged: leaves sag on hinges, planks/poles missing; T3 sheet dented and torn at the bottom.")
    sh.text(110, 2310, gnotes, 19, "Regular", INK, maxw=2250)

    # ---------------- C: watchtower
    sh.panel(2450, 130, 1616, 2740, "C  Watchtower · SM_Build_Watchtower", "logs + ladder · deck at 400 · parapet 100")
    s3 = 1.45
    for t in (1, 2, 3):
        ox = 2540 + (t - 1) * 510
        sh.label_box(ox, 1105, {1: "T1 · log", 2: "T2 · + plank", 3: "T3 · + plated"}[t], 19, "Bold", "#FFFFFF", tcol[t])
        v = View(sh, ox, 1060, s3)
        v.grid(0, 0, 200, 500, 100, labels=(t == 1))
        tower(v, t)
        if t == 3:
            scale_figure(View(sh, ox, 1060 - 400 * s3, s3), 140, label=False)
    v = View(sh, 2540, 1060, s3)
    v.dim_v(0, 400, 0, "deck 400", off=-44, size=13)
    v.dim_v(400, 500, 0, "100", off=-44, size=13)
    v.dim_h(0, 200, 0, "200 footprint", off=34, size=13, ext_from=0)
    v.dim_h(75, 125, 30, "50", off=-14, size=12)
    # plan of deck
    sh.text(2540, 1200, "Deck plan (T2)", 18, "Bold")
    vp = View(sh, 2600, 1580, 1.5)
    vp.grid(0, 0, 200, 200, 100, labels=True, ground=False)
    for i in range(11):
        vp.rect(-10, -10 + i * 20, 210, 10 + i * 20, fill=C["Weathered Plank"], width=1)
    vp.grid(0, 0, 200, 200, 100, labels=True, ground=False)
    for (xx, yy) in ((12.5, 12.5), (187.5, 12.5), (12.5, 187.5), (187.5, 187.5)):
        vp.circle(xx, yy, 12.5, fill=C["Bark"], width=1.5)
    vp.rect(70, 10, 130, 70, fill="#1E2124", width=1.5)
    vp.text(100, 40, "hatch 60×60", 13, "SemiBold", "#EDEAE2")
    vp.text(100, -30, "ladder ↓ (front)", 14, "Regular", INK2)
    tnotes = ("4 legs Ø25 × 500 at the corners of a 200 × 200 footprint (centres 12.5 cm in). Deck top at 400: T1 two layers of lashed poles Ø10, "
              "T2/T3 planks 220 × 20 × 4 overhanging 10 cm. Parapet 400–500: T1 three horizontal poles Ø12 + 3 uprights Ø8, rope lashings; "
              "T2 closed-board planks 20 × 100; T3 adds 2 plates 100 × 100 per side, 2 cm proud. X-bracing Ø15 on all four faces in two bays. "
              "Ladder 50 wide, rails 10 × 10, rungs every 30 cm, from ground up through a 60 × 60 hatch to 450. "
              "Separate meshes: ladder (climbable volume), hatch lid (moving, hinged on the back edge), parapet sets, plates. "
              "Pivot bottom-left corner of footprint. Damaged: missing parapet boards, one brace snapped; Broken: deck partly collapsed, tower leans 5°.")
    sh.text(3000, 1220, tnotes, 18, "Regular", INK, maxw=1020)
    blocked_box(sh, 2540, 1720, 1480, 260, "Painted watchtower reference",
                "Generation refused: free-tier daily image limit reached (429 free_tier_image_limit_reached) on 2026-11-07. "
                "Model from the drawn elevations; painted reference to be generated on a later run.")
    sh.text(2540, 2000, "180 cm figure stands on the T3 deck for scale.", 16, "Regular", INK2)
    sh.save(os.path.join(CONCEPT, "CA_Buildables_GateTower_Sheet.png"))


# ======================================================================== TRAPS SHEET
SOIL = "#5E4E3C"
VOID = "#2A2520"


def ground(v, x0, x1, y=0, depth=40):
    v.rect(x0, y - depth, x1, y, fill=SOIL, outline=None)
    v.line([(x0, y), (x1, y)], INK, 2)


def leaf_litter(v, x0, x1, y, seed=0, n=40):
    r = rng(seed)
    for _ in range(n):
        v.circle(r.uniform(x0, x1), y + r.uniform(0, 5), r.uniform(1.5, 3.5),
                 fill=r.choice([C["Lichen"], C["Moss"], C["Bark"], C["Rotten Wood"], "#8C7A50"]), outline=None)


def spike_pit_section(v, t):
    v.rect(-50, -190, 250, 0, fill=SOIL, outline=None)
    v.rect(0, -150, 200, 0, fill=VOID, width=1.5)
    if t == 2:
        for (a, b) in ((0, 4), (196, 200)):
            v.rect(a, -150, b, 0, fill=C["Weathered Plank"], width=1)
        v.rect(0, -150, 200, -146, fill=C["Weathered Plank"], width=1)
    if t == 3:
        v.rect(4, -150, 196, -147, fill=C["Steel"], width=1.2)
    for x in (25, 75, 125, 175):
        if t == 3:
            stake(v, x, -147, 90, 75, d=3.5, tip=12, col=C["Steel"], tipcol=C["Rust Orange"], width=1)
        else:
            stake(v, x, -150, 90, 75, d=6, tip=22)
    # cover lattice + litter
    v.rect(-15, -3, 215, 1, fill=C["Bark"], width=1.2)
    for x in range(-10, 215, 20):
        v.line([(x, -2), (x + 10, 1)], C["Fresh-cut Wood"], 1)
    leaf_litter(v, -15, 215, 1, seed=t, n=50)
    v.line([(-50, 0), (0, 0)], INK, 2)
    v.line([(200, 0), (250, 0)], INK, 2)


def spike_pit_plan(v):
    v.rect(0, 0, 200, 200, fill=VOID, width=1.5)
    for x in (25, 75, 125, 175):
        for y in (25, 75, 125, 175):
            v.circle(x, y, 3, fill=C["Fresh-cut Wood"], width=1)
    for k in range(0, 231, 23):
        v.line([(-15 + k, -15), (-15 + k, 215)], C["Bark"], 2, alpha=200)
        v.line([(-15, -15 + k), (215, -15 + k)], C["Bark"], 2, alpha=200)
    v.rect(-15, -15, 215, 215, fill=None, outline=C["Bark"], width=2)


def barbed_fence(v, t):
    ground(v, -20, 420)
    for x in (0, 200, 400):
        if t == 1:
            pole_v(v, x, 0, 125, 10, seed=x, sharpen=10)
        elif t == 2:
            v.rect(x - 5, 0, x + 5, 125, fill=C["Weathered Plank"], width=1.5)
            if x < 400:
                v.line([(x + 5, 10), (x + 195, 110)], C["Weathered Plank"], 5)
                v.line([(x + 5, 110), (x + 195, 10)], C["Weathered Plank"], 5)
        else:
            v.rect(x - 2.5, 0, x + 2.5, 125, fill=C["Steel"], width=1.2)
            v.rect(x - 8, 0, x + 8, 2, fill=C["Weld Scorch"], width=1)
    strands = (30, 60, 90, 115) if t < 3 else (20, 45, 70, 95, 120)
    for yy in strands:
        sag = 4
        for a in (0, 200):
            barbed_wire(v, a, yy, a + 100, yy - sag)
            barbed_wire(v, a + 100, yy - sag, a + 200, yy)
    if t == 3:
        for i in range(13):
            v.circle(15 + i * 31, 140, 18, fill=None, outline="#55595B", width=1.3)


def noise_trap(v, t):
    ground(v, -20, 320)
    for x in (0, 300):
        if t == 1:
            pole_v(v, x, 0, 60, 5, seed=x, sharpen=6)
        elif t == 2:
            v.rect(x - 4, 0, x + 4, 60, fill=C["Weathered Plank"], width=1.2)
        else:
            v.rect(x - 1.5, 0, x + 1.5, 60, fill=C["Steel"], width=1)
    if t == 3:
        v.line([(0, 40), (300, 38)], "#55595B", 1.4)
    else:
        rope(v, [(0, 40), (150, 37), (300, 40)], 1)
    k = 0
    for cx in (75, 150, 225):
        for dx in (-9, 0, 9):
            v.line([(cx + dx, 38), (cx + dx, 30)], "#8C7A58", 1)
            if t == 3 and dx == 0:
                v.poly([(cx - 5, 30), (cx + 6, 30), (cx + 8, 16), (cx - 3, 14)], fill=mix(C["Steel"], C["Rust Orange"], 0.5), width=1)
            else:
                tin_can(v, cx + dx, 30, seed=k)
            k += 1


def tripwire(v, t):
    ground(v, -20, 340)
    for x in (0, 260):
        pole_v(v, x, -10, 20, 4, seed=x)
    if t == 3:
        v.line([(0, 15), (260, 15)], "#55595B", 1.3)
    else:
        rope(v, [(0, 15), (260, 15)], 1)
    # tripod + bundle at right
    pole_v(v, 300, 0, 150, 6, seed=3)
    v.line([(270, 0), (300, 150)], C["Bark"], 5)
    v.line([(330, 0), (300, 150)], C["Bark"], 5)
    rope(v, [(300, 150), (300, 95)], 1)
    rope(v, [(260, 15), (285, 60), (300, 95)], 1)
    for i, (dx, dy) in enumerate(((-6, 85), (6, 86), (0, 76))):
        rock(v, 300 + dx, dy, 7, seed=i)
    v.line([(288, 92), (312, 92), (306, 70), (294, 70), (288, 92)], "#8C7A58", 1)
    if t == 1:
        log_h(v, 280, 320, 5, 10, seed=2)
    elif t == 2:
        v.rect(275, 0, 325, 4, fill=C["Weathered Plank"], width=1.2)
    else:
        v.rect(275, 0, 325, 2, fill=C["Steel"], width=1.2)


def deadfall(v, t):
    ground(v, -20, 260)
    # figure-4 trigger at x 200, prop height 60
    v.line([(200, 0), (200, 55)], C["Fresh-cut Wood"], 3)
    v.line([(185, 30), (225, 50)], C["Fresh-cut Wood"], 3)
    v.line([(196, 56), (230, 45)], C["Fresh-cut Wood"], 3)
    # log from ground at x 0 to prop at x 205,y 65 (angle)
    ang = math.atan2(62, 205)
    L = 230
    cx, cy = 0, 15
    ux, uy = math.cos(ang), math.sin(ang)
    nx, ny = -uy, ux
    r = 15
    pts = [(cx + nx * r, cy + ny * r), (cx + ux * L + nx * r, cy + uy * L + ny * r), (cx + ux * L - nx * r, cy + uy * L - ny * r), (cx - nx * r, cy - ny * r)]
    v.poly(pts, fill=C["Bark"], width=1.5)
    if t == 2:
        for k in (0.3, 0.55, 0.8):
            px_, py_ = cx + ux * L * k + nx * (r + 7), cy + uy * L * k + ny * (r + 7)
            rock(v, px_, py_, 9, seed=int(k * 10))
        rope(v, [(cx + ux * 50 + nx * 15, cy + uy * 50 + ny * 15), (cx + ux * 50 - nx * 15, cy + uy * 50 - ny * 15)], 2)
    if t == 3:
        for k in (0.25, 0.45, 0.65, 0.85):
            bx, by = cx + ux * L * k - nx * r, cy + uy * L * k - ny * r
            stake(v, bx, by, math.degrees(ang) - 90, 18, d=3, tip=8, col=C["Steel"], tipcol=C["Rust Orange"], width=1)
        q0 = (cx + ux * 60 + nx * r, cy + uy * 60 + ny * r)
        v.poly([q0, (q0[0] + ux * 80, q0[1] + uy * 80), (q0[0] + ux * 80 + nx * 6, q0[1] + uy * 80 + ny * 6), (q0[0] + nx * 6, q0[1] + ny * 6)], fill=C["Steel"], width=1)
    v.circle(205, 8, 5, fill=C["Dried Blood"], outline=None)


def snare(v, t):
    ground(v, -20, 280)
    # springpole: anchored at x 0, bent towards x 200
    pts = []
    for i in range(21):
        a = i / 20
        pts.append((a * 170, 250 * math.sin(a * math.pi * 0.55) - (a ** 2) * 60))
    v.line(pts, C["Bark"], 7)
    v.line(pts, INK, 1)
    tip = pts[-1]
    line_col_rope = t != 3
    if line_col_rope:
        rope(v, [tip, (200, 30)], 1)
    else:
        v.line([tip, (200, 30)], "#55595B", 1.3)
    # trigger peg
    pole_v(v, 200, -10, 30, 5, seed=1)
    v.line([(190, 26), (215, 26)], C["Fresh-cut Wood"] if t != 2 else C["Weathered Plank"], 4)
    if t == 2:
        v.rect(185, 0, 189, 30, fill=C["Weathered Plank"], width=1)
        v.rect(211, 0, 215, 30, fill=C["Weathered Plank"], width=1)
    # noose (ellipse on ground)
    v.sh.ellipse(*v.px(235, 4), 20 * v.s, 6 * v.s, fill=None, outline=rgb("#55595B" if t == 3 else "#8C7A58"), width=2)
    if line_col_rope:
        rope(v, [(215, 26), (235, 10)], 1)
    else:
        v.line([(215, 26), (235, 10)], "#55595B", 1.3)


def burn_trench_section(v, t, state="unlit"):
    v.rect(-30, -70, 90, 0, fill=SOIL, outline=None)
    v.poly([(0, 0), (60, 0), (52, -40), (8, -40)], fill=VOID, width=1.5)
    if t == 2:
        v.poly([(0, 0), (4, 0), (12, -40), (8, -40)], fill=C["Weathered Plank"], width=1)
        v.poly([(56, 0), (60, 0), (52, -40), (48, -40)], fill=C["Weathered Plank"], width=1)
    if t == 3:
        v.line([(1, 0), (9, -39), (51, -39), (59, 0)], C["Steel"], 4)
    r = rng(t)
    for i in range(9):
        log_end(v, r.uniform(14, 46), r.uniform(-34, -6), r.uniform(6, 10), seed=i)
    v.line([(-30, 0), (0, 0)], INK, 2)
    v.line([(60, 0), (90, 0)], INK, 2)


def burn_trench_elev(v, state):
    ground(v, -10, 410, 0, 50)
    v.rect(0, -40, 400, 0, fill=VOID, width=1.2)
    r = rng(5)
    for i in range(26):
        x = r.uniform(5, 380)
        log_h(v, x, x + r.uniform(30, 70), r.uniform(-34, -4), r.uniform(5, 9), seed=i, ends=True)
    if state == "burning":
        for i in range(16):
            x = 15 + i * 25 + r.uniform(-5, 5)
            h = r.uniform(30, 70)
            v.poly([(x - 10, 0), (x + 10, 0), (x + r.uniform(-4, 4), h)], fill=C["Firelight"], outline=None, alpha=210)
            v.poly([(x - 5, 0), (x + 5, 0), (x, h * 0.55)], fill="#F2C27A", outline=None, alpha=220)
    if state == "burnt":
        v.rect(0, -40, 400, -10, fill="#1B1A19", outline=None)
        for i in range(20):
            v.circle(r.uniform(10, 390), r.uniform(-12, -2), r.uniform(1.5, 3), fill=C["Ember"] if i % 4 == 0 else "#3A3634", outline=None)


def build_traps():
    sh = Sheet(4096, 2960)
    sh.title_block("Player-built structures · Traps and area denial",
                   "CA_Buildables_Traps_Sheet.png", "100 cm grid · all dimensions in cm",
                   "Drawn elevations and sections are authoritative")
    caveat(sh, 30, 122, 4036,
           "Painted trap reference BLOCKED: generation refused (free-tier daily image limit, 2026-11-07). "
           "Tiers for noise trap, tripwire, deadfall, snare and burn trench are Agent 1 PROPOSALS (the brief lists only rope, rocks, sticks, string, cans "
           "and fuel for them): T2 adds plank parts, T3 swaps rope for wire or adds scrap steel. Confirm with design before modelling T2/T3 of these.", 18)
    tcol = {1: C["Bark"], 2: "#6B5E48", 3: "#4E5457"}
    tn = {1: "T1", 2: "T2", 3: "T3"}
    Y0 = 200

    # ---- A spike pit
    sh.panel(30, Y0, 2020, 900, "A  Spike pit · SM_Build_SpikePit", "dug pit (shovel) + sharpened sticks + cover · section through centre")
    s = 1.6
    for t in (1, 2, 3):
        ox = 110 + (t - 1) * 510
        v = View(sh, ox + 50 * s, Y0 + 200, s)
        v.grid(-50, -190, 250, 0, 100, labels=(t == 1), ground=False)
        spike_pit_section(v, t)
        sh.label_box(ox, Y0 + 80, {1: "T1 · sticks", 2: "T2 · plank-lined", 3: "T3 · rebar on steel base"}[t], 18, "Bold", "#FFFFFF", tcol[t])
        if t == 1:
            v.dim_h(0, 200, -150, "200", off=26, size=14)
            v.dim_v(-150, 0, 200, "150 deep", off=48, size=13)
            v.dim_v(-150, -75, 25, "75", off=-18, size=12)
    vp = View(sh, 1690, Y0 + 470, 1.15)
    spike_pit_plan(vp)
    sh.text(1660, Y0 + 80, "Plan (cover 230 × 230 over pit)", 18, "Bold")
    vp.dim_h(-15, 215, -15, "cover 230", off=26, size=13)
    sh.text(110, Y0 + 580,
            "Pit 200 × 200 × 150, 16 stakes Ø6 × 75 on a 50 cm grid (4 × 4), fire-hardened tips. Cover: lattice of sticks 230 × 230 with leaf litter, "
            "one separate mesh that breaks and falls in when stepped on (sprung state). States: Armed (cover on), Sprung (cover in pit, zombie impaled), "
            "Needs re-arm (2–6 stakes snapped, tips stained Dried Blood #4E2320). T2: planks 4 cm line the walls and floor (no cave-in, faster re-arm). "
            "T3: Ø3.5 rebar spikes welded to a 192 × 192 steel base plate (does not snap; bends). Pit volume is a terrain cut, not part of the mesh: "
            "the mesh is lining + stakes + cover; pivot at the pit's top-left corner at ground level.",
            18, "Regular", INK, maxw=1880)

    # ---- B barbed wire
    sh.panel(2070, Y0, 1996, 900, "B  Barbed wire fence · SM_Build_BarbedFence", "posts + barbed wire · 400 module")
    s = 1.35
    for t in (1, 2, 3):
        ox = 2150 + (t - 1) * 640
        v = View(sh, ox, Y0 + 430, s)
        v.grid(0, 0, 400, 200, 100, labels=(t == 1), ground=False)
        barbed_fence(v, t)
        sh.label_box(ox, Y0 + 80, {1: "T1 · stick posts", 2: "T2 · plank posts + X-brace", 3: "T3 · steel posts + coil"}[t], 17, "Bold", "#FFFFFF", tcol[t])
        if t == 1:
            v.dim_v(0, 125, 0, "125", off=-34, size=13)
            v.dim_h(0, 200, 0, "200 c/c", off=40, size=13)
    sh.text(2140, Y0 + 580,
            "Posts at 0 / 200 / 400 (end posts shared between modules), 125 above ground. 4 strands at 30 / 60 / 90 / 115 with 4 cm sag "
            "(T3: 5 strands + Ø36 concertina coil along the top). Wire strands are separate spline meshes that can deform when zombies tangle "
            "(Agent 3 may swap to cable components). Posts: T1 sharpened sticks Ø10; T2 sawn plank posts 10 × 10 with X-brace; T3 5 × 5 angle steel "
            "welded to 16 × 2 base plates. Wire: dark steel #55595B with rust flecks.", 18, "Regular", INK, maxw=1860)

    # ---- C noise trap
    Y1 = Y0 + 920
    sh.panel(30, Y1, 1330, 860, "C  Noise trap · SM_Build_NoiseTrap", "string + tin cans")
    s = 1.8
    for t in (1, 2, 3):
        v = View(sh, 160, Y1 + 40 + t * 190, s)
        sh.label_box(160 + 320 * s + 30, Y1 + 40 + t * 190 - 60, tn[t], 17, "Bold", "#FFFFFF", tcol[t])
        noise_trap(v, t)
        if t == 1:
            v.dim_v(0, 40, 0, "40", off=-22, size=12)
            v.dim_h(0, 300, 60, "300", off=-20, size=13)
    sh.text(110, Y1 + 720, "Stakes 60 high, 300 apart; string at 40. 3 clusters of 3 cans (Ø7.5 × 11), hung 8 cm, each can a physics part "
            "(rattle anim). T2 plank stakes. T3 wire + scrap steel pieces (louder).", 17, "Regular", INK, maxw=1200)

    # ---- D tripwire
    sh.panel(1380, Y1, 1330, 860, "D  Tripwire alarm · SM_Build_Tripwire", "rope, rocks, sticks")
    for t in (1, 2, 3):
        v = View(sh, 1430 + (t - 1) * 425, Y1 + 420, 1.12)
        tripwire(v, t)
        sh.label_box(1430 + (t - 1) * 425, Y1 + 80, tn[t], 17, "Bold", "#FFFFFF", tcol[t])
        if t == 1:
            v.dim_v(0, 150, 335, "150", off=14, size=12)
            v.dim_h(0, 260, 15, "260", off=-16, size=12)
    sh.text(1460, Y1 + 560, "Line at 15 cm between pegs. Pulling it slips the release; a net of 3 rocks drops from a 150 tripod onto a "
            "strike log (T2 plank, T3 steel plate = loudest). Moving: rock net, line.", 17, "Regular", INK, maxw=1200)

    # ---- E snare
    sh.panel(2730, Y1, 1336, 860, "E  Snare · SM_Build_Snare", "springpole + noose (animals, zombie ankles)")
    for t in (1, 2, 3):
        v = View(sh, 2800 + (t - 1) * 420, Y1 + 500, 1.25)
        snare(v, t)
        sh.label_box(2800 + (t - 1) * 420, Y1 + 80, {1: "T1 rope", 2: "T2 plank trigger", 3: "T3 steel wire"}[t], 16, "Bold", "#FFFFFF", tcol[t])
        if t == 1:
            v.dim_v(0, 250, -5, "≈250 pole", off=-20, size=12)
    sh.text(2800, Y1 + 560, "Bent sapling or cut pole (Ø7, ~280 long) held by a notched trigger peg; noose Ø40 lies on the ground. "
            "Moving: springpole (bend → release anim), noose. Catches rabbits; holds a zombie ankle for a few seconds (gameplay).",
            17, "Regular", INK, maxw=1200)

    # ---- F deadfall
    Y2 = Y1 + 880
    sh.panel(30, Y2, 2020, 840, "F  Deadfall · SM_Build_Deadfall", "heavy log on a figure-4 trigger")
    for t in (1, 2, 3):
        ox = 110 + (t - 1) * 640
        v = View(sh, ox, Y2 + 400, 2.1 if False else 2.0)
        v.grid(0, 0, 250, 100, 100, labels=(t == 1), ground=False)
        deadfall(v, t)
        sh.label_box(ox, Y2 + 80, {1: "T1 · log", 2: "T2 · log + lashed rocks", 3: "T3 · + welded spikes / weight"}[t], 17, "Bold", "#FFFFFF", tcol[t])
        if t == 1:
            v.dim_v(0, 62, 215, "62", off=26, size=12)
            v.dim_h(0, 230, 0, "log Ø30 × 230", off=34, size=13)
    sh.text(110, Y2 + 520, "Log Ø30 × 230 propped at 62 cm by a figure-4 trigger (3 sticks, separate meshes, they scatter when sprung). "
            "Bait at the trigger. The log is a physics body when sprung (falls, ~120 kg). T2: rocks lashed on top for weight. "
            "T3: rebar spikes welded to steel straps on the underside plus a scrap steel weight. Footprint 250 × 60.", 18, "Regular", INK, maxw=1880)

    # ---- G burn trench / fire ring
    sh.panel(2070, Y2, 1996, 840, "G  Burn trench / fire ring · SM_Build_BurnTrench", "dug trench + fuel, lit to block a horde")
    for t in (1, 2, 3):
        v = View(sh, 2150 + (t - 1) * 200, Y2 + 260, 1.6)
        burn_trench_section(v, t)
        sh.label_box(2150 + (t - 1) * 200 - 30, Y2 + 80, tn[t] + {1: " dug", 2: " plank", 3: " steel"}[t], 15, "Bold", "#FFFFFF", tcol[t])
    vv = View(sh, 2150, Y2 + 260, 1.6)
    vv.dim_h(0, 60, 0, "60", off=-18, size=12)
    vv.dim_v(-40, 0, 60, "40", off=16, size=12)
    for i, stt in enumerate(("unlit", "burning", "burnt")):
        v = View(sh, 2780, Y2 + 200 + i * 120, 0.75)
        burn_trench_elev(v, stt)
        sh.text(2780 + 300 + 20, Y2 + 200 + i * 120 - 40, stt, 16, "SemiBold", INK)
    v = View(sh, 2780, Y2 + 200, 0.75)
    v.dim_h(0, 400, 0, "400 segment", off=-60, size=12)
    # fire ring plan
    vr = View(sh, 3700, Y2 + 330, 0.55)
    vr.circle(0, 0, 200, fill=VOID, width=1.5)
    vr.circle(0, 0, 140, fill=C["Moss"], width=1.5)
    for i in range(24):
        a = i / 24 * 2 * math.pi
        vr.circle(math.cos(a) * 170, math.sin(a) * 170, 8, fill=C["Bark"], outline=None)
    vr.dim_h(-200, 200, -200, "fire ring Ø400 outer", off=26, size=12)
    sh.text(2150, Y2 + 600, "Trench 60 wide × 40 deep, straight segments of 400 (free-form, drag like walls) or a fire ring "
            "(Ø400 outer, trench 60, built around a point). Fuel: branches and split logs, then fuel units (petrol/alcohol). States: Unlit, Burning "
            "(fire VFX by Agent 3, light #E08A3C, large light radius: it lights the player up too), Burnt (charcoal + embers, must be refilled). "
            "T2: plank edging stops the sides crumbling; T3: steel sheet channel liner, reusable, burns longer. Trench cut = terrain; mesh = liner + fuel.",
            17, "Regular", INK, maxw=1830)
    sh.save(os.path.join(CONCEPT, "CA_Buildables_Traps_Sheet.png"))


# ======================================================================== GHOST SHEET
from PIL import ImageChops  # noqa: E402

MAGENTA = "#FF00FF"


def offscreen(fn, w, h, ox, oy, scale):
    """Render fn(view) offscreen; return (RGB image, alpha mask) at SS resolution."""
    o = Sheet(w, h, bg=MAGENTA)
    v = View(o, ox, oy, scale)
    fn(v)
    im = o.im
    import numpy as np
    a = np.asarray(im).astype(int)
    dist = np.abs(a[..., 0] - 255) + np.abs(a[..., 1] - 0) + np.abs(a[..., 2] - 255)
    m = np.clip((dist - 30) * 4, 0, 255).astype("uint8")
    return im, Image.fromarray(m, "L")


def ghostify(im, mask, col=GHOST, fill_a=0.24, edge_a=0.95, pulse=None):
    """Turn rendered geometry into the ghost look: translucent fill + bright edges."""
    import numpy as np
    g = im.convert("L").filter(ImageFilter.FIND_EDGES)
    me = mask.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
    e = np.maximum(np.asarray(g).astype(float) / 255 * 1.6, np.asarray(me).astype(float) / 255)
    e = np.clip(e, 0, 1) * (np.asarray(mask).astype(float) / 255 > 0.02)
    a = np.asarray(mask).astype(float) / 255 * fill_a
    alpha = np.clip(a + e * edge_a * 0.75, 0, 1)
    out = Image.new("RGBA", im.size, rgb(col, 0))
    out.putalpha(Image.fromarray((alpha * 255).astype("uint8"), "L"))
    return out


def solid(im, mask):
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


def night_bg(sh, x, y, w, h, day=False, seed=1):
    import numpy as np
    top, bot = (C["Moonlit Shadow"], C["Night Sky"]) if not day else ("#8E9693", C["Moss"])
    for i in range(int(h)):
        sh.rect(x, y + i, w, 1, fill=mix(top, bot, i / h))
    r = rng(seed)
    for _ in range(9):
        tw = r.uniform(14, 34)
        tx = x + r.uniform(0, w - tw)
        sh.rect(tx, y, tw, h * 0.86, fill=mix(C["Deep Forest"] if day else "#0B0E12", bot, 0.25), alpha=230)
    sh.rect(x, y + h * 0.86, w, h * 0.14, fill=C["Deep Forest"] if day else "#0E1210")


def paste_ss(sh, img, x, y):
    sh.im.paste(img, (int(x * SS), int(y * SS)), img)


def build_ghost():
    sh = Sheet(4096, 2700)
    sh.title_block("Player-built structures · Ghost / blueprint look",
                   "CA_Buildables_Ghost_Sheet.png", "100 cm grid · all dimensions in cm",
                   "Drawn with the same geometry as the build sheets")

    # ---- A: progression at night
    sh.panel(30, 130, 2700, 1130, "A  Ghost fills piece by piece", "night, T1 log wall · each deposit turns one ghost log solid · next slot pulses")
    s = 1.15
    W, H = 600, 470
    for i, (n_done, label) in enumerate(((0, "placed · 0 / 10 logs"), (4, "4 / 10 · next slot pulses"), (9, "9 / 10"))):
        x0 = 80 + i * 870
        y0 = 280
        night_bg(sh, x0, y0, W + 200, H + 120, seed=i + 3)
        ox, oy = 100, H + 60

        def all_logs(v):
            wall_t1(v)

        def done_logs(v, n=n_done):
            for k in range(n):
                log_h(v, 0, 400, 15 + 30 * k, 30, seed=100 + k)

        def next_log(v, n=n_done):
            log_h(v, 0, 400, 15 + 30 * n, 30, seed=100 + n)

        im, m = offscreen(all_logs, W + 200, H + 120, ox, oy, s)
        paste_ss(sh, ghostify(im, m), x0, y0)
        if n_done:
            im2, m2 = offscreen(done_logs, W + 200, H + 120, ox, oy, s)
            paste_ss(sh, solid(im2, m2), x0, y0)
        if n_done < 10:
            im3, m3 = offscreen(next_log, W + 200, H + 120, ox, oy, s)
            paste_ss(sh, ghostify(im3, m3, fill_a=0.5, edge_a=1.0), x0, y0)
        # snap points
        for (sx, sy) in ((0, 0), (400, 0), (0, 300), (400, 300)):
            px_, py_ = x0 + ox + sx * s, y0 + oy - sy * s
            sh.poly([(px_, py_ - 9), (px_ + 9, py_), (px_, py_ + 9), (px_ - 9, py_)], fill=GHOST, outline=INK, width=1)
        # material strip
        mx, my = x0 + 20, y0 + 20
        sh.ellipse(mx + 16, my + 16, 15, 15, fill=C["Fresh-cut Wood"], outline=INK, width=1.5)
        sh.text(mx + 40, my + 2, f"{10 - n_done}", 26, "Bold", GHOST)
        sh.text(x0 + 10, y0 + H + 130, label, 20, "SemiBold", INK)
    sh.text(80, 975,
            "Placement: the ghost snaps to terrain and to snap points (diamonds) at piece ends and every 100 cm. "
            "Material strip: one icon per material still needed with the remaining count, drawn in the world beside the ghost "
            "(icons, no other numbers on screen). Each deposit plays a hammer/thud and swaps one ghost log for the solid mesh. "
            "The next slot to fill is drawn at 50% fill and pulses. Finished pieces stop being ghost entirely.",
            19, "Regular", INK, maxw=2560)

    # ---- B: ghost material spec
    sh.panel(2750, 130, 1316, 1130, "B  Ghost material spec", "M_Ghost / MI_Ghost_Valid, MI_Ghost_Invalid")
    rows = [
        ("Valid colour", GHOST, "Bone-white ghost #E3DED0: the palette's Bone White, slightly lifted. Never cyan or neon (no sci-fi hologram)."),
        ("Invalid colour", GHOST_BAD, "Rust red #B5502E when blocked (overlap, too steep, no snap, not enough room)."),
        ("Fill opacity", None, "24% (next slot 50%). Unlit / emissive 0.6 so it reads at night without lighting the scene."),
        ("Edge", None, "Bright edge from geometry edges + Fresnel, 95% opacity, about 1.5 px at 1080p. Hand-drawn chalk feel, not scanlines."),
        ("Pulse", None, "Next slot: opacity 35 → 60% at 1.2 Hz, ease in/out. Whole ghost does not flicker."),
        ("Depth", None, "Ghost renders through foliage (custom depth) at 40% so the player can place behind ferns."),
        ("Shadow / sound", None, "Casts no shadow, makes no noise; the world does not react to a ghost."),
    ]
    yy = 220
    for name, col, txt in rows:
        if col:
            sh.rect(2790, yy + 2, 60, 40, fill=col, outline=INK, width=1)
            sh.text(2862, yy + 10, col, 17, "SemiBold", INK)
        sh.text(2790 if not col else 2960, yy + (0 if not col else 10), name, 20, "Bold", NOTE)
        yy = sh.text(2790, yy + 50, txt, 18, "Regular", INK, maxw=1240) + 24

    # ---- C: invalid + plating ghost + day readability
    sh.panel(30, 1280, 2700, 1390, "C  States", "invalid placement · metal plating ghost on a T2 wall · daytime readability")
    s = 1.0
    W, H = 560, 420
    # invalid
    x0, y0 = 80, 1420
    night_bg(sh, x0, y0, W + 160, H + 100, seed=11)
    im, m = offscreen(lambda v: wall_t1(v), W + 160, H + 100, 90, H + 40, s)
    paste_ss(sh, ghostify(im, m, col=GHOST_BAD, fill_a=0.3), x0, y0)
    sh.rect(x0 + 90 + 250, y0 + H + 40 - 140, 120, 140, fill="#3B3226", outline=INK, width=1.5)
    sh.text(x0 + 90 + 310, y0 + H + 40 - 70, "rock", 16, "Medium", "#D9D2C1", anchor="mm")
    sh.text(x0, y0 + H + 115, "Invalid: whole ghost turns rust red; cannot confirm.", 19, "SemiBold", INK)
    # plating ghost
    x0 = 900

    def t2(v):
        wall_t2(v)

    def plates_all(v):
        wall_t3(v)

    def plates_done(v):
        k = 0
        for xx in range(0, 400, 100):
            for yyy in (0, 150):
                if k < 3:
                    plate(v, xx, yyy, xx + 100, yyy + 150, seed=50 + k)
                k += 1
    night_bg(sh, x0, y0, W + 160, H + 100, seed=12)
    im, m = offscreen(t2, W + 160, H + 100, 90, H + 40, s)
    paste_ss(sh, solid(im, m), x0, y0)
    im, m = offscreen(plates_all, W + 160, H + 100, 90, H + 40, s)
    paste_ss(sh, ghostify(im, m, fill_a=0.5, edge_a=1.0), x0, y0)
    im, m = offscreen(plates_done, W + 160, H + 100, 90, H + 40, s)
    paste_ss(sh, solid(im, m), x0, y0)
    sh.text(x0, y0 + H + 115, "Plating: same flow on top of a finished wall; 3 / 8 plates welded.", 19, "SemiBold", INK)
    # day
    x0 = 1720
    night_bg(sh, x0, y0, W + 160, H + 100, day=True, seed=13)
    im, m = offscreen(lambda v: (wall_t1(v), spikes_front(v, 0, 1)), W + 160, H + 100, 90, H + 40, s * 0.95)
    paste_ss(sh, ghostify(im, m), x0, y0)
    sh.text(x0, y0 + H + 115, "Daytime, overcast forest: the bone-white edge still reads.", 19, "SemiBold", INK)
    # painted-to-ghost demo
    g1 = load_raw("G01_Buildables_Walls.png").crop((40, 30, 420, 740))
    g1s = g1.resize((int(g1.width * 0.62) * SS, int(g1.height * 0.62) * SS), Image.LANCZOS)
    import numpy as np
    arr = np.asarray(g1s.convert("RGB")).astype(int)
    d = np.abs(arr - np.array([200, 200, 205])).sum(axis=2)
    m = Image.fromarray(np.clip((d - 45) * 5, 0, 255).astype("uint8"), "L").filter(ImageFilter.MedianFilter(5))
    gray = ImageEnhance.Contrast(g1s.convert("RGB")).enhance(1.4)
    yb = 2120
    sh.text(80, yb - 10, "Same look applied to the painted T1 reference:", 19, "Bold", INK)
    night_bg(sh, 80, yb + 25, 520, 470, seed=14)
    paste_ss(sh, ghostify(gray, m, fill_a=0.18, edge_a=0.9), 80 + 20, yb + 25 + 10)
    sh.text(640, yb + 30,
            "Other buildables use the same material with their own meshes: spike pit (cover lattice + stakes), "
            "watchtower (legs first, then bracing, deck, parapet), gate (posts, then leaves). Free-form walls: the player drags "
            "between two points; the ghost shows a dashed centre line and one ghost log per 30 cm of height for the full dragged "
            "length; the material strip shows the log count, which depends on length (one log per 400 cm, partial logs cut).",
            19, "Regular", INK, maxw=2040)
    # free-form schematic
    vf = View(sh, 700, 2600, 0.7)
    for k in range(0, 1000, 24):
        vf.line([(k, 0), (k + 12, 0)], GHOST_BAD if False else INK2, 2)
    for xx in (0, 1000):
        a, b = vf.px(xx, 0)
        sh.poly([(a, b - 10), (a + 10, b), (a, b + 10), (a - 10, b)], fill=GHOST, outline=INK, width=1)
    vf.dim_h(0, 1000, 0, "dragged length 1000 cm → 3 log lengths per course (400 + 400 + 200 cut) × 10 courses", off=30, size=15)

    # ---- D: painted note
    sh.panel(2750, 1280, 1316, 1390, "D  Notes for Agent 2 / Agent 3", None)
    notes = ("• The ghost uses the final meshes (no separate ghost mesh): Agent 3 swaps materials per element (log, plank, plate, stake).\n\n"
             "• Every buildable must therefore be split into the same elements the player deposits: one element per log, plank, plate, stake set, "
             "post, leaf. Name elements in order of filling (Log_00 … Log_09, Plank_00 …, Plate_00 …).\n\n"
             "• Ghost colours come from the palette in Concept/StyleGuide.md; no new hues.\n\n"
             "• Painted ghost concept is not needed; this sheet is drawn from the build-sheet geometry so it is exact. "
             "No image generation was used for this sheet except the G01 crop in panel C.")
    sh.text(2790, 1360, notes, 19, "Regular", INK, maxw=1240)
    sh.save(os.path.join(CONCEPT, "CA_Buildables_Ghost_Sheet.png"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["walls"]
    if "walls" in which:
        build_walls()
    if "gatetower" in which:
        build_gatetower()
    if "traps" in which:
        build_traps()
    if "ghost" in which:
        build_ghost()
