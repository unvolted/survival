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
        hole = (ox + 50, 0, ox + 150, 210)
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
    sh.panel(30, 130, 2400, 1150, "A  Barricaded door / window · SM_Build_Barricade", "fits ruin-kit openings: window 100 × 120 (sill 90), door 100 × 210")
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
    v2.dim_v(0, 210, 150, "210", off=22, size=13)
    vb = View(sh, 110 + 780, 735, s)
    vb.dim_h(30, 170, 210 - 16, "plank 140 × 20 × 3", off=-205, size=14)
    vc = View(sh, 110 + 1560, 735, s)
    vc.dim_h(35, 165, 225, "sheet 130 × 150", off=-24, size=14)
    bnotes = ("T1: poles Ø10 × 140, 4 (window) / 7 (door), nailed into the frame 20 cm past each side. "
              "T2: planks 140 × 20 × 3, 4 / 6 across with ±8° random tilt plus one diagonal brace, 2 nails each end. "
              "T3: one scrap sheet 130 × 150 (window) or 130 × 225 (door), 1 cm thick, welded to steel angle tabs anchored in the wall; "
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
        sh.label_box(ox, 215, {1: "T1 · log", 2: "T2 · + plank", 3: "T3 · + plated"}[t], 19, "Bold", "#FFFFFF", tcol[t])
        v = View(sh, ox, 1000, s3)
        v.grid(0, 0, 200, 500, 100, labels=(t == 1))
        tower(v, t)
        if t == 3:
            scale_figure(View(sh, ox, 1000 - 400 * s3, s3), 140, label=False)
    v = View(sh, 2540, 1000, s3)
    v.dim_v(0, 400, 0, "deck 400", off=-44, size=13)
    v.dim_v(400, 500, 0, "100", off=-44, size=13)
    v.dim_h(0, 200, 0, "200 footprint", off=34, size=13, ext_from=0)
    v.dim_h(75, 125, 30, "50", off=-14, size=12)
    # plan of deck
    sh.text(2540, 1090, "Deck plan (T2)", 18, "Bold")
    vp = View(sh, 2600, 1470, 1.5)
    vp.grid(0, 0, 200, 200, 100, labels=True, ground=False)
    for i in range(11):
        vp.rect(-10, -10 + i * 20, 210, 10 + i * 20, fill=C["Weathered Plank"], width=1)
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
    sh.text(3000, 1130, tnotes, 18, "Regular", INK, maxw=1020)
    blocked_box(sh, 2540, 1600, 1480, 260, "Painted watchtower reference",
                "Generation refused: free-tier daily image limit reached (429 free_tier_image_limit_reached) on 2026-11-07. "
                "Model from the drawn elevations; painted reference to be generated on a later run.")
    sh.text(2540, 1880, "180 cm figure stands on the T3 deck for scale.", 16, "Regular", INK2)
    sh.save(os.path.join(CONCEPT, "CA_Buildables_GateTower_Sheet.png"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["walls"]
    if "walls" in which:
        build_walls()
    if "gatetower" in which:
        build_gatetower()
