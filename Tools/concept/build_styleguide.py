"""Style guide sheet (Agent 1): Concept/CA_StyleGuide_Sheet.png

Palette swatches with hex values, lighting-mood colour keys, material language swatches, overgrowth rules, 5 do / 5 don't.
Palette values come from sheetlib.PALETTE (the single source; Concept/StyleGuide.md mirrors it).
"""
import colorsys
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from sheetlib import *  # noqa: E402,F401,F403
import build_ruinkit as rk  # noqa: E402

MOODS = [
    dict(name="Dawn", sky=("#4E5A68", "#C9A27A"), key="#D9B48A", shadow="#3B4250", fog="#B9B6AE", sil="#2E3530",
         note="Low warm sun 3–8° (with sunset, the only warm light that isn't fire). Long shadows, ground mist in hollows, ~3500 K. Birdsong peak."),
    dict(name="Noon", sky=("#8E9BA3", "#BCC0BA"), key="#E6E2D6", shadow="#4A4F4A", fog="#C4C6C0", sil="#4A5246",
         note="High hazy sun, short shadows, ~5800 K. Colours stay muted even in full sun; no blue-sky postcard."),
    dict(name="Overcast (default)", sky=("#8C908E", "#A6A9A5"), key=None, shadow="#5C605C", fog="#9A9E9C", sil="#465043",
         note="Default weather. Soft sky light only, no hard shadows. Greens read richest; ruins read as wet grey."),
    dict(name="Rain", sky=("#4F5658", "#6B7275"), key=None, shadow="#3A3F42", fog="#7A8285", sil="#363D3A", rain=True,
         note="Surfaces 20–30% darker, roughness −0.3, puddles mirror the sky. Visibility ~150 m. Rain lowers noise radius."),
    dict(name="Night + firelight", sky=("#0E1116", "#1C2430"), key="#E08A3C", shadow="#0B0D10", fog="#1C2430", sil="#0A0C0E", fire=True,
         note="True dark: no auto-exposure lift. Moon ambient #1C2430 only. Fire #E08A3C lights ~8–12 m and is seen from far away."),
]


def clip_draw(sh, x, y, w, h, fn):
    """Draw fn(sub, 0, 0) into an offscreen w x h sheet and paste it, so nothing spills outside the box."""
    sub = Sheet(int(w), int(h), bg=PANEL)
    fn(sub)
    sh.im.paste(sub.im, (int(x * SS), int(y * SS)))


def mood_card(sh, x, y, w, h, m, extra=None):
    def f(sub):
        _mood_card_raw(sub, 0, 0, w, h, m)
        if extra:
            extra(sub)
    clip_draw(sh, x, y, w, h, f)
    sh.rect(x, y, w, h, outline="#9A9890", width=1)


def _mood_card_raw(sh, x, y, w, h, m):
    top, bot = m["sky"]
    for i in range(int(h * 0.62)):
        sh.rect(x, y + i, w, 1, fill=mix(top, bot, i / (h * 0.62)))
    gy = y + h * 0.62
    sh.rect(x, gy, w, h - h * 0.62, fill=mix(m["sil"], m["shadow"], 0.3))
    r = rng(len(m["name"]))
    # sun / moon
    if m["name"] == "Dawn":
        sh.ellipse(x + w * 0.78, gy - 18, 26, 26, fill=m["key"], alpha=230)
    if m["name"] == "Noon":
        sh.ellipse(x + w * 0.7, y + 60, 22, 22, fill=m["key"], alpha=200)
    # far tree line
    pts = [(x, gy)]
    for i in range(0, int(w) + 20, 18):
        pts.append((x + i, gy - 40 - r.uniform(0, 35)))
    pts.append((x + w, gy))
    sh.poly(pts, fill=mix(m["sil"], m["fog"], 0.55))
    # ruin silhouette: two-storey house with broken roof
    hx, hw, hh = x + w * 0.12, w * 0.5, h * 0.42
    house = [(hx, gy), (hx, gy - hh), (hx + hw * 0.35, gy - hh - 40), (hx + hw * 0.5, gy - hh - 10), (hx + hw * 0.62, gy - hh - 28),
             (hx + hw * 0.7, gy - hh + 25), (hx + hw, gy - hh + 10), (hx + hw, gy)]
    wall_col = mix(m["sil"], m["fog"], 0.2)
    if m.get("fire"):
        wall_col = mix(wall_col, m["key"], 0.18)
    sh.poly(house, fill=wall_col)
    for (wx, wy) in ((0.15, 0.35), (0.55, 0.35), (0.15, 0.72), (0.55, 0.72)):
        sh.rect(hx + hw * wx, gy - hh * (1 - wy) - 40, hw * 0.18, 34, fill=mix(m["sil"], "#000000", 0.5))
    # ivy blob
    for k in range(60):
        sh.ellipse(hx + r.uniform(0, hw * 0.4), gy - r.uniform(0, hh * 0.6), 4, 4, fill=mix(C["Ivy"], m["sil"], 0.45))
    # tree
    tx = x + w * 0.82
    sh.rect(tx, gy - h * 0.38, 8, h * 0.38, fill=m["sil"])
    for k in range(40):
        sh.ellipse(tx + 4 + r.gauss(0, 26), gy - h * 0.38 + r.gauss(0, 30), 9, 9, fill=mix(m["sil"], C["Moss"], 0.15))
    if m["name"] == "Dawn":
        for k in range(10):
            sh.rect(x, gy - 30 + k * 4, w, 4, fill=m["fog"], alpha=24)
    if m.get("rain"):
        for k in range(120):
            rx, ry = x + r.uniform(0, w), y + r.uniform(0, h - 20)
            sh.line([(rx, ry), (rx - 6, ry + 18)], "#AEB6B8", 1, alpha=110)
    if m.get("fire"):
        fx, fy = x + w * 0.66, gy + 40
        for k in range(14, 0, -1):
            sh.ellipse(fx, fy - 10, k * 13, k * 8, fill=m["key"], alpha=14)
        sh.poly([(fx - 12, fy), (fx + 12, fy), (fx + 2, fy - 34)], fill=m["key"])
        sh.poly([(fx - 6, fy), (fx + 6, fy), (fx, fy - 18)], fill="#F2C27A")
        sh.ellipse(fx, fy + 2, 16, 4, fill=C["Ember"])


def chips(sh, x, y, m):
    items = [("sky", m["sky"][0]), ("horizon", m["sky"][1]), ("key", m["key"] or "—"), ("shadow", m["shadow"]), ("fog", m["fog"])]
    for i, (k, hv) in enumerate(items):
        cx = x + i * 67
        if hv != "—":
            sh.rect(cx, y, 60, 30, fill=hv, outline=INK, width=1)
        else:
            sh.rect(cx, y, 60, 30, fill=PANEL, outline=INK2, width=1)
            sh.text(cx + 30, y + 15, "none", 12, "Medium", INK2, anchor="mm")
        sh.text(cx, y + 36, k, 12, "SemiBold", INK2)
        sh.text(cx, y + 52, hv, 12, "Regular", INK)


def sat(hv):
    r, g, b = rgb(hv)
    return colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1]


def rotten_wood_swatch(w, h, seed=3):
    """Procedural rotten wood swatch (drawn, not generated)."""
    o = Sheet(w, h, bg=C["Rotten Wood"])
    r = rng(seed)
    for i in range(0, h, 3):
        o.rect(0, i, w, 2, fill=mix(C["Rotten Wood"], r.choice(["#000000", C["Weathered Plank"], C["Bark"]]), r.uniform(0.05, 0.3)))
    for k in range(5):
        y0 = r.uniform(10, h - 10)
        o.line([(0, y0)] + [(xx, y0 + math.sin(xx / r.uniform(20, 40)) * 4 + r.uniform(-1, 1)) for xx in range(0, w + 10, 10)], "#2B241D", 2)
    for k in range(8):
        o.ellipse(r.uniform(0, w), r.uniform(0, h), r.uniform(8, 20), r.uniform(3, 7), fill="#2B241D", alpha=170)
    for k in range(30):
        o.ellipse(r.uniform(0, w), r.uniform(0, h), 3, 3, fill=r.choice([C["Moss"], C["Lichen"]]), alpha=200)
    for k in range(6):
        o.ellipse(r.uniform(0, w), r.uniform(0, h), 5, 3, fill=C["Bone White"], alpha=170)  # fungus
    return o.im.resize((w, h), Image.LANCZOS)


# ---------------------------------------------------------------- do / don't thumbnails
def thumb_night(sh, x, y, w, h, neon=False):
    m = dict(MOODS[4])
    extra = None
    if neon:
        m = dict(m, key="#FF2BD6", name="neon", fire=True)

        def extra(sub):
            fx, fy = w * 0.3, h * 0.4
            for k in range(10, 0, -1):
                sub.ellipse(fx, fy, k * 16, k * 10, fill="#22E3FF", alpha=18)
            sub.rect(w * 0.2, h * 0.35, w * 0.25, 12, fill="#22E3FF")
    mood_card(sh, x, y, w, h, m, extra)


def thumb_carpet(sh, x, y, w, h):
    sh.rect(x, y, w, h, fill="#C9CBC6")
    sh.rect(x + 30, y + 30, w - 60, h - 50, fill="#4CB050", outline=INK, width=1)
    sh.rect(x + w * 0.4, y + h * 0.35, w * 0.2, h * 0.3, fill="#4CB050", outline="#2E7D32", width=2)
    for k in range(6):
        sh.ellipse(x + 40 + k * 50, y + 18, 14, 9, fill="#66D96A")


def thumb_ornament(sh, x, y, w, h):
    sh.rect(x, y, w, h, fill="#C9CBC6")
    gy = y + h - 30
    sh.rect(x, gy, w, 30, fill="#7FA36A")
    for i in range(9):
        px_ = x + 20 + i * (w - 40) / 8
        sh.rect(px_ - 7, gy - 110, 14, 110, fill="#F2F0EA", outline=INK, width=1)
        sh.poly([(px_ - 7, gy - 110), (px_ + 7, gy - 110), (px_, gy - 126)], fill="#F2F0EA", outline=INK, width=1)
        sh.ellipse(px_, gy - 132, 6, 6, fill="#D4A017")
    sh.rect(x + 20, gy - 80, w - 40, 10, fill="#F2F0EA", outline=INK, width=1)
    sh.rect(x + 20, gy - 40, w - 40, 10, fill="#F2F0EA", outline=INK, width=1)
    pts = [(x + w / 2 + math.cos(math.pi * t / 20) * 60, gy - 120 - math.sin(math.pi * t / 20) * 50) for t in range(21)]
    sh.line(pts, "#D4A017", 4)


def build():
    sh = Sheet(4096, 2990)
    sh.title_block("Style guide · ROOTFALL", "CA_StyleGuide_Sheet.png", "written page: Concept/StyleGuide.md",
                   "Quiet, melancholy, tense · nature has won · warm light only from fire and sunset")

    # ---- A palette
    sh.panel(30, 130, 2190, 1190, "A  Palette", "hex values · use · HSV saturation")
    groups = []
    for g, name, hv, use in PALETTE:
        groups.append((g, name, hv, use))
    groups += [("Ghost", "Ghost Line", GHOST, "Build ghost edge + fill (24%)"), ("Ghost", "Ghost Invalid", GHOST_BAD, "Ghost when placement is blocked")]
    cols, sw_w, sw_h = 6, 340, 190
    for i, (g, name, hv, use) in enumerate(groups):
        cx = 60 + (i % cols) * (sw_w + 15)
        cy = 210 + (i // cols) * (sw_h + 18)
        sh.rect(cx, cy, sw_w, 92, fill=hv, outline=INK, width=1)
        light = sum(rgb(hv)) > 420
        sh.text(cx + 12, cy + 10, g.upper(), 13, "SemiBold", INK if light else "#E9E5DA")
        sh.text(cx + 12, cy + 56, hv, 22, "Bold", INK if light else "#F2EEE4")
        sh.text(cx + sw_w - 12, cy + 64, f"S {sat(hv) * 100:.0f}%", 14, "Medium", INK if light else "#D9D4C8", anchor="ra")
        sh.text(cx, cy + 100, name, 18, "Bold")
        sh.text(cx, cy + 126, use, 14, "Regular", INK2, maxw=sw_w)
    sh.text(60, 1240, "Rules: large surfaces stay at saturation ≤ 45% (foliage, concrete, wood, plaster). Rust may reach ~75% only in small "
            "areas. Firelight, Ember and Sunset are LIGHT colours, never paint. No pure white, no pure black, no saturated blue, purple or red.",
            17, "Medium", NOTE, maxw=2120)

    # ---- B lighting moods
    sh.panel(2240, 130, 1826, 1190, "B  Lighting moods", "drawn colour keys (painted mood strip BLOCKED, see report)")
    pos = [(2270, 200), (2630, 200), (2990, 200), (3350, 200), (3710, 200)]
    cw = 335
    for i, m in enumerate(MOODS):
        cx, cy = pos[i]
        mood_card(sh, cx, cy, cw, 520, m)
        sh.label_box(cx + 8, cy + 8, m["name"], 15, "Bold", "#FFFFFF", "#26282A")
        chips(sh, cx, cy + 535, m)
        sh.text(cx, cy + 610, m["note"], 15, "Regular", INK, maxw=cw)
    sh.text(2270, 1010, "Exposure: fixed per mood (no eye adaptation brightening at night). Fog colour = horizon colour. "
            "Shadows are never pure black; at night, unlit areas fall to Night Sky #12161C. Light sources draw zombies: "
            "the brighter the warm light, the more visible the player.", 16, "Medium", NOTE, maxw=1770)
    blocked_box(sh, 2270, 1120, 1770, 180, "Painted lighting-mood strip (5 panels)",
                "Generation refused, free-tier daily image limit (2026-11-07). These drawn keys carry the hex values and are enough for Agent 3's "
                "post-process / sky setup; the painting is mood reference only.")

    # ---- C material language
    sh.panel(30, 1340, 4036, 660, "C  Material language", "real samples cropped from the generated concept paintings (raw files in Concept/_raw/), rotten wood drawn")
    g1 = load_raw("G01_Buildables_Walls.png")
    g2 = load_raw("G02_RuinKit_Walls.png")
    g3 = load_raw("G03_Buildables_SpikeGateBarricade.png")
    mats = [
        ("Rust", ImageEnhance.Color(g3.crop((1110, 320, 1260, 470))).enhance(0.55),
         "Rust Orange / Old Rust / Rust Bloom. Rough 0.8–0.95, non-metallic where rusted (mask). Streaks run DOWN from edges, bolts, welds.", "G03, desat. 45%"),
        ("Wet concrete", g2.crop((1105, 125, 1195, 250)),
         "Wet / Shadow / Dry Concrete. Rough 0.85 dry → 0.35 wet; 25% darker wet. Damp band at the base, stains under ledges.", "G02"),
        ("Rotten wood", None,
         "Rotten Wood #5A4E40. Rough 0.95, soft rounded edges, grain splits, moss and pale fungus. Ruins only, never player builds.", "drawn"),
        ("Moss", g2.crop((470, 610, 640, 705)),
         "Moss / Lichen. On tops, ledges and shaded bases. Rough 1.0, soft edges, slight subsurface. Decal or vertex blend.", "G02"),
        ("Ivy", g2.crop((80, 505, 240, 620)),
         "Ivy / Deep Forest / Moss leaves 4–8 cm on cards. Climbs from soil, hangs from lintels and roof edges, leaves face the light.", "G02"),
        ("Fresh-cut logs", g1.crop((250, 130, 410, 330)),
         "Bark + Fresh-cut Wood ends. Clean bright ends = player-made marker. Bark rough 0.9, cut end 0.7. Tone ends to #C9A26B.", "G01"),
        ("Welded steel", g1.crop((1020, 270, 1150, 400)),
         "Steel + Weld Scorch. Bare steel metallic 1.0, rough 0.45–0.6; lumpy weld bead, 3–5 cm heat tint ring; rust creeps in later.", "G01"),
    ]
    tw, th = 530, 430
    for i, (name, im, note, src) in enumerate(mats):
        cx = 60 + i * (tw + 46)
        cy = 1420
        if im is None:
            im = rotten_wood_swatch(tw, th)
        # centre-crop to tile aspect
        iw, ih = im.size
        ta = tw / th
        if iw / ih > ta:
            nw = int(ih * ta)
            im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
        else:
            nh = int(iw / ta)
            im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
        sh.paste(im, cx, cy, tw, th)
        sh.label_box(cx + 8, cy + 8, name, 17, "Bold", "#FFFFFF", "#26282A")
        sh.text(cx + tw - 8, cy + th - 26, src, 13, "Medium", "#F2EEE4", anchor="ra")
        sh.text(cx, cy + th + 14, note, 16, "Regular", INK, maxw=tw)

    # ---- D overgrowth rules
    sh.panel(30, 2020, 2190, 940, "D  Overgrowth rules", "15 years of neglect · growth follows light, water and gravity")
    S_ = 0.75
    GY = 2860
    v = View(sh, 110, GY, S_)
    rk.wall_piece(v, 0, 400, "window", "Overgrown", seed=5)
    rk.wall_piece(v, 400, 400, "door", "Overgrown", seed=9)
    v2 = View(sh, 110, GY - 300 * S_, S_)
    rk.wall_piece(v2, 0, 400, "window", "Overgrown", seed=13)
    v3 = View(sh, 110, GY - 600 * S_, S_)
    rk.roof_profile(v3, "Overgrown", seed=4)
    v.rect(400, 300, 800, 320, fill=C["Dry Concrete"], width=1)
    moss_band(v, 400, 800, 318, 8, seed=2, density=2)
    sapling(v, 700, 320, 120, seed=3)
    v.rect(820, -6, 1150, 0, fill=C["Wet Concrete"], outline=None)
    grass_tufts(v, 820, 1150, 0, 22, seed=4, h=18)
    sapling(v, 1060, 0, 170, seed=6)
    grass_tufts(v, -60, 0, 0, 8, seed=7, h=26)
    # player wall, no growth
    for i in range(4):
        log_h(v, 1180, 1400, 15 + 30 * i, 30, seed=300 + i)
    marks = [(1, -40, 14), (3, 120, 150), (4, 600, 335), (5, 250, 720), (6, 200, 195), (9, 1290, 150), (2, 900, 14)]
    for n, mx, my in marks:
        a, b = v.px(mx, my)
        sh.ellipse(a, b, 15, 15, fill="#26282A")
        sh.text(a, b, str(n), 15, "Bold", "#FFFFFF", anchor="mm")
    rules = [
        ("1 Ground, verges", "70–100%", "grass, ferns, shrubs; leaf litter"),
        ("2 Roads, floors open to sky", "20–50%", "in cracks only; saplings in wide cracks"),
        ("3 Exterior walls", "0–70%", "ivy from the ground up; denser on shaded faces and corners; moss band 0–40 cm"),
        ("4 Ledges, sills, wall tops, flat roofs", "60–100%", "moss, grass tufts, saplings on broken tops"),
        ("5 Pitched roofs", "20–50%", "moss on tiles; saplings at holes and gutters"),
        ("6 Openings", "30–60%", "ivy curtains hang from lintels and pour out of windows"),
        ("7 Interiors", "0–15%", "only within ~2 m of openings or under roof holes"),
        ("8 Metal, vehicles", "0–20%", "rust first; grass through floors, saplings through hulls"),
        ("9 Player-built", "0%", "fresh wood and steel always read as new"),
        ("10 Forest-swallowed zones", "80–100%", "trees inside buildings, roofs gone"),
    ]
    yy = 2100
    for name, pct, rule in rules:
        sh.text(1330, yy, name, 16, "Bold")
        lo, hi = [int(p.strip("%")) for p in pct.replace("%", "").split("–")] if "–" in pct else (0, 0)
        sh.rect(1330, yy + 24, 300, 10, fill="#CFCCC4")
        sh.rect(1330 + lo * 3, yy + 24, max(3, (hi - lo) * 3), 10, fill=C["Moss"])
        sh.text(1640, yy + 18, pct, 14, "SemiBold", NOTE)
        sh.text(1730, yy + 18, rule, 14, "Regular", INK2, maxw=470)
        yy += 80
    sh.text(110, 2900, "Never: floating foliage, ivy without a contact surface, green on freshly built player pieces, uniform coverage.",
            15, "Medium", NOTE, maxw=1150)

    # ---- E do / don't
    sh.panel(2240, 2020, 1826, 940, "E  5 do / 5 don't", "top row DO · bottom row DON'T")
    tw, th = 330, 250
    items = [
        ("Warm light only from fire", "Neon or coloured artificial light"),
        ("Ivy rises from soil, pours from openings", "Uniform bright-green carpet, floating foliage"),
        ("Every ruin shows war damage and neglect", "Clean, freshly painted, pastel buildings"),
        ("Player builds: rough, functional, fresh-cut", "Ornamental, symmetrical, decorative builds"),
        ("Muted painterly render, value carries the read", "Black cartoon outlines, saturated orange"),
    ]
    for i, (do, dont) in enumerate(items):
        cx = 2270 + i * (tw + 22)
        y_do, y_dont = 2100, 2500
        if i == 0:
            thumb_night(sh, cx, y_do, tw, th)
            thumb_night(sh, cx, y_dont, tw, th, neon=True)
        elif i == 1:
            sh.paste(g2.crop((70, 500, 400, 710)), cx, y_do, tw, th)
            thumb_carpet(sh, cx, y_dont, tw, th)
        elif i == 2:
            sh.paste(g2.crop((85, 290, 400, 480)), cx, y_do, tw, th)
            bad = g2.crop((740, 80, 1000, 268)).filter(ImageFilter.GaussianBlur(2))
            bad = ImageEnhance.Brightness(bad).enhance(1.35)
            tint = Image.new("RGB", bad.size, (150, 200, 235))
            bad = Image.blend(bad, tint, 0.45)
            sh.paste(bad, cx, y_dont, tw, th)
        elif i == 3:
            sh.paste(g1.crop((40, 40, 420, 330)), cx, y_do, tw, th)
            thumb_ornament(sh, cx, y_dont, tw, th)
        else:
            sh.paste(g2.crop((740, 80, 1000, 268)), cx, y_do, tw, th)
            sh.paste(g3.crop((1070, 230, 1330, 610)), cx, y_dont, tw, th)
        sh.rect(cx, y_do, tw, th, outline="#3F5236", width=4)
        sh.rect(cx, y_dont, tw, th, outline="#8A3B1E", width=4)
        sh.label_box(cx + 6, y_do + 6, "DO", 15, "Bold", "#FFFFFF", "#3F5236")
        sh.label_box(cx + 6, y_dont + 6, "DON'T", 15, "Bold", "#FFFFFF", "#8A3B1E")
        sh.text(cx, y_do + th + 10, do, 15, "SemiBold", INK, maxw=tw)
        sh.text(cx, y_dont + th + 10, dont, 15, "SemiBold", INK, maxw=tw)
    sh.text(2270, 2915, "Counter-examples are drawn or processed on purpose (DON'T 3 = G02 crop brightened and tinted; DON'T 5 = raw G03 drift).",
            13, "Regular", INK2, maxw=1780)
    sh.save(os.path.join(CONCEPT, "CA_StyleGuide_Sheet.png"))


if __name__ == "__main__":
    build()
