"""Shared drawing library for ROOTFALL concept sheets (Agent 1).

Everything here is deterministic: sheets can be rebuilt with
    python3 Tools/concept/build_all.py
Drawing is done at SS x resolution and downsampled with Lanczos for clean anti-aliasing.
Units: sheet coordinates are final pixels; View coordinates are centimetres, y up.
"""
import io
import math
import os
import random

from PIL import Image, ImageCms, ImageDraw, ImageEnhance, ImageFilter, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CONCEPT = os.path.join(ROOT, "Concept")
RAW = os.path.join(CONCEPT, "_raw")
SS = 2
FONT_DIR = "/usr/share/fonts/opentype/inter/"

# ---------------------------------------------------------------- palette
# Single source of truth for the ROOTFALL palette (mirrored in Concept/StyleGuide.md).
PALETTE = [
    # group, name, hex, use
    ("Greens", "Deep Forest", "#2F3A2C", "Shadowed foliage, forest floor, deep ivy"),
    ("Greens", "Ivy", "#3F5236", "Ivy, creepers, conifer needles"),
    ("Greens", "Moss", "#5B6B47", "Moss, grass, broadleaf foliage"),
    ("Greens", "Lichen", "#8A9474", "Lichen, dry grass, foliage highlights"),
    ("Rust", "Old Rust", "#6E3B22", "Deep rust, rust streaks and stains"),
    ("Rust", "Rust Orange", "#9C4F26", "Main rust colour on all metal"),
    ("Rust", "Rust Bloom", "#B8683A", "Fresh rust, rust highlights (small areas)"),
    ("Concrete", "Shadow Concrete", "#3A3D3F", "Concrete in shade, wet cracks, voids"),
    ("Concrete", "Wet Concrete", "#5D6163", "Main concrete and asphalt, rain state"),
    ("Concrete", "Dry Concrete", "#8C8F8C", "Concrete in sun, dust, rubble"),
    ("Concrete", "Old Plaster", "#A7A294", "Render and plaster on ruined walls"),
    ("Concrete", "Weathered Brick", "#7A4A3A", "Exposed brick behind broken plaster"),
    ("Bone", "Bone White", "#D9D2C1", "Bone, paper, highlights, ghost lines"),
    ("Wood", "Bark", "#4A3A2C", "Bark on logs and stakes"),
    ("Wood", "Fresh-cut Wood", "#C9A26B", "Cut log ends, sharpened tips, new planks"),
    ("Wood", "Weathered Plank", "#8A7C66", "Scavenged and old planks"),
    ("Wood", "Rotten Wood", "#5A4E40", "Rotten beams, floors, fallen trees"),
    ("Metal", "Steel", "#6F7578", "Scrap sheet, plates, tools, frames"),
    ("Metal", "Weld Scorch", "#4A4644", "Heat-tinted and scorched steel at welds"),
    ("Light", "Firelight", "#E08A3C", "Fire, torch and lamp light (light only)"),
    ("Light", "Ember", "#B5471F", "Embers, glowing coals (light only)"),
    ("Light", "Sunset", "#D9A05B", "Low sun at dawn and dusk (light only)"),
    ("Night", "Night Sky", "#12161C", "Night sky, unlit interiors"),
    ("Night", "Moonlit Shadow", "#1C2430", "Night ambient, deepest fill"),
    ("Gore", "Dried Blood", "#4E2320", "Blood stains, wounds (never bright red)"),
    ("Gore", "Grave Skin", "#8C8A72", "Infected skin base tone"),
]
C = {name: hexv for _, name, hexv, _ in PALETTE}

BG = "#DEDCD6"       # sheet background (warm neutral grey)
PANEL = "#ECEAE5"    # panel background
INK = "#26282A"      # line work and text
INK2 = "#5A5D60"     # secondary text
GRID = "#AEB2B4"     # 100 cm grid
GRID_FAINT = "#CBCDCD"
DIM = "#8A3B1E"      # dimension lines (dark rust, readable on grey)
NOTE = "#2F4A5E"     # callout text colour (desaturated blue ink)
GHOST = "#E3DED0"
GHOST_BAD = "#B5502E"


def rgb(h, a=None):
    h = h.lstrip("#")
    v = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return v if a is None else v + (int(a),)


def mix(h1, h2, t):
    a, b = rgb(h1), rgb(h2)
    return "#%02X%02X%02X" % tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


_font_cache = {}


def font(size, weight="Regular"):
    key = (size, weight)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, f"Inter-{weight}.otf"), int(round(size * SS)))
    return _font_cache[key]


def wrap(draw, text, fnt, maxw_px):
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=fnt) <= maxw_px * SS or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


class Sheet:
    def __init__(self, w, h, bg=BG):
        self.W, self.H = w, h
        self.im = Image.new("RGB", (w * SS, h * SS), rgb(bg))
        self.d = ImageDraw.Draw(self.im, "RGBA")

    # ---- basic primitives in final-pixel coordinates
    def _c(self, col, a=None):
        if col is None:
            return None
        if isinstance(col, tuple):
            return col
        return rgb(col, a) if a is not None else rgb(col)

    def rect(self, x, y, w, h, fill=None, outline=None, width=1, radius=0, alpha=None):
        box = [x * SS, y * SS, (x + w) * SS, (y + h) * SS]
        f = self._c(fill, alpha)
        if radius:
            self.d.rounded_rectangle(box, radius * SS, fill=f, outline=self._c(outline), width=int(width * SS))
        else:
            self.d.rectangle(box, fill=f, outline=self._c(outline), width=int(width * SS))

    def line(self, pts, fill=INK, width=1, alpha=None):
        self.d.line([(x * SS, y * SS) for x, y in pts], fill=self._c(fill, alpha), width=max(1, int(width * SS)), joint="curve")

    def poly(self, pts, fill=None, outline=None, width=1, alpha=None):
        self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=self._c(fill, alpha))
        if outline:
            self.line(list(pts) + [pts[0]], outline, width)

    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, width=1, alpha=None):
        self.d.ellipse([(cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS],
                       fill=self._c(fill, alpha), outline=self._c(outline), width=int(width * SS))

    def text(self, x, y, s, size=22, weight="Regular", fill=INK, anchor="la", maxw=None, lh=1.3, alpha=None):
        """Draw text (optionally wrapped to maxw px). Returns y below the block (final px)."""
        fnt = font(size, weight)
        lines = wrap(self.d, s, fnt, maxw) if maxw else s.split("\n")
        yy = y
        for ln in lines:
            self.d.text((x * SS, yy * SS), ln, font=fnt, fill=self._c(fill, alpha), anchor=anchor)
            yy += size * lh
        return yy

    def textw(self, s, size=22, weight="Regular"):
        return self.d.textlength(s, font=font(size, weight)) / SS

    def label_box(self, x, y, s, size=18, weight="SemiBold", fg="#FFFFFF", bg=INK, pad=6):
        w = self.textw(s, size, weight)
        self.rect(x, y, w + 2 * pad, size + 2 * pad, fill=bg, radius=3)
        self.text(x + pad, y + pad - 1, s, size, weight, fg)
        return w + 2 * pad

    def panel(self, x, y, w, h, title=None, sub=None, fill=PANEL):
        self.rect(x, y, w, h, fill=fill, outline="#C3C1BB", width=2, radius=6)
        if title:
            self.text(x + 22, y + 16, title, 30, "Bold")
            if sub:
                self.text(x + 24 + self.textw(title, 30, "Bold") + 14, y + 25, sub, 19, "Regular", INK2)

    def paste(self, img, x, y, w=None, h=None, border=True):
        """Paste a PIL image into the box (final px), keeping aspect. Returns (x, y, w, h) used."""
        iw, ih = img.size
        if w and h:
            s = min(w / iw, h / ih)
        elif w:
            s = w / iw
        else:
            s = h / ih
        nw, nh = int(iw * s), int(ih * s)
        im2 = img.convert("RGB").resize((nw * SS, nh * SS), Image.LANCZOS)
        ox = x + ((w - nw) // 2 if (w and h) else 0)
        oy = y + ((h - nh) // 2 if (w and h) else 0)
        self.im.paste(im2, (int(ox * SS), int(oy * SS)))
        if border:
            self.rect(ox, oy, nw, nh, outline="#9A9890", width=1)
        return ox, oy, nw, nh

    def paste_rgba(self, img, x, y):
        self.im.paste(img, (int(x * SS), int(y * SS)), img)

    def title_block(self, title, filename, scale_note, notes=""):
        W, H = self.W, self.H
        self.rect(0, 0, W, 108, fill=INK)
        self.text(40, 22, title, 44, "Bold", "#EDEAE2")
        self.text(42, 76, "ROOTFALL  ·  Concept Art (Agent 1)  ·  " + filename, 20, "Regular", "#B9B5AA")
        right = "2026-11-07  ·  rev A  ·  " + scale_note
        self.text(W - 40, 30, right, 20, "Medium", "#D9D2C1", anchor="ra")
        if notes:
            self.text(W - 40, 62, notes, 18, "Regular", "#B9B5AA", anchor="ra")

    def save(self, path):
        out = self.im.resize((self.W, self.H), Image.LANCZOS)
        prof = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB"))
        out.save(path, "PNG", icc_profile=prof.tobytes(), optimize=True)
        return path


class View:
    """Centimetre drawing space on a sheet. (ox, oy) = final-px position of cm (0, 0); y is up."""

    def __init__(self, sheet, ox, oy, scale):
        self.sh, self.ox, self.oy, self.s = sheet, ox, oy, scale
        self.d = sheet.d

    def px(self, x, y):
        return self.ox + x * self.s, self.oy - y * self.s

    def P(self, x, y):
        a, b = self.px(x, y)
        return a * SS, b * SS

    def poly(self, pts, fill=None, outline=INK, width=2, alpha=None):
        self.sh.poly([self.px(*p) for p in pts], fill, outline, width, alpha)

    def rect(self, x0, y0, x1, y1, fill=None, outline=INK, width=2, alpha=None):
        self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, outline, width, alpha)

    def line(self, pts, fill=INK, width=2, alpha=None):
        self.sh.line([self.px(*p) for p in pts], fill, width, alpha)

    def circle(self, cx, cy, r, fill=None, outline=INK, width=2, alpha=None):
        x, y = self.px(cx, cy)
        self.sh.ellipse(x, y, r * self.s, r * self.s, fill, outline, width, alpha)

    def text(self, x, y, s, size=18, weight="Regular", fill=INK, anchor="mm", **kw):
        a, b = self.px(x, y)
        return self.sh.text(a, b, s, size, weight, fill, anchor, **kw)

    def grid(self, x0, y0, x1, y1, step=100, labels=True, ground=True, sub=None):
        if sub:
            g = math.ceil(x0 / sub) * sub
            while g <= x1:
                self.line([(g, y0), (g, y1)], GRID_FAINT, 1)
                g += sub
            g = math.ceil(y0 / sub) * sub
            while g <= y1:
                self.line([(x0, g), (x1, g)], GRID_FAINT, 1)
                g += sub
        g = math.ceil(x0 / step) * step
        while g <= x1 + 0.01:
            self.line([(g, y0), (g, y1)], GRID, 1)
            if labels:
                a, b = self.px(g, y0)
                self.sh.text(a, b + 6, f"{int(g)}", 14, "Medium", INK2, anchor="mt")
            g += step
        g = math.ceil(y0 / step) * step
        while g <= y1 + 0.01:
            self.line([(x0, g), (x1, g)], GRID, 1)
            if labels:
                a, b = self.px(x0, g)
                self.sh.text(a - 6, b, f"{int(g)}", 14, "Medium", INK2, anchor="rm")
            g += step
        if ground and y0 <= 0 <= y1:
            self.line([(x0, 0), (x1, 0)], "#7C7A72", 2)

    # ---- dimensions
    def _arrow(self, x, y, ang, size=9, col=DIM):
        a, b = self.px(x, y)
        p1 = (a + size * math.cos(ang + 0.38), b + size * math.sin(ang + 0.38))
        p2 = (a + size * math.cos(ang - 0.38), b + size * math.sin(ang - 0.38))
        self.sh.poly([(a, b), p1, p2], fill=col)

    def dim_h(self, x0, x1, y, text=None, off=0, ext_from=None, size=17, col=DIM):
        """Horizontal dimension at cm height y (+off px below). ext_from: cm y of the measured feature."""
        a0, b = self.px(x0, y)
        a1, _ = self.px(x1, y)
        b += off
        if ext_from is not None:
            _, e = self.px(x0, ext_from)
            self.sh.line([(a0, e + (4 if e < b else -4)), (a0, b + (6 if e < b else -6))], col, 1)
            self.sh.line([(a1, e + (4 if e < b else -4)), (a1, b + (6 if e < b else -6))], col, 1)
        self.sh.line([(a0, b), (a1, b)], col, 1.5)
        for xx, ang in ((a0, 0), (a1, math.pi)):
            p1 = (xx + 10 * math.cos(ang + 0.38), b + 10 * math.sin(ang + 0.38))
            p2 = (xx + 10 * math.cos(ang - 0.38), b + 10 * math.sin(ang - 0.38))
            self.sh.poly([(xx, b), p1, p2], fill=col)
        t = text if text is not None else f"{x1 - x0:g} cm"
        w = self.sh.textw(t, size, "SemiBold")
        mid = (a0 + a1) / 2
        self.sh.rect(mid - w / 2 - 4, b - size / 2 - 3, w + 8, size + 6, fill=PANEL)
        self.sh.text(mid, b, t, size, "SemiBold", col, anchor="mm")

    def dim_v(self, y0, y1, x, text=None, off=0, ext_from=None, size=17, col=DIM):
        a, b0 = self.px(x, y0)
        _, b1 = self.px(x, y1)
        a += off
        if ext_from is not None:
            e, _ = self.px(ext_from, y0)
            sgn = 1 if a > e else -1
            self.sh.line([(e + 4 * sgn, b0), (a + 6 * sgn, b0)], col, 1)
            self.sh.line([(e + 4 * sgn, b1), (a + 6 * sgn, b1)], col, 1)
        self.sh.line([(a, b0), (a, b1)], col, 1.5)
        for yy, ang in ((b0, -math.pi / 2), (b1, math.pi / 2)):
            p1 = (a + 10 * math.cos(ang + 0.38), yy + 10 * math.sin(ang + 0.38))
            p2 = (a + 10 * math.cos(ang - 0.38), yy + 10 * math.sin(ang - 0.38))
            self.sh.poly([(a, yy), p1, p2], fill=col)
        t = text if text is not None else f"{y1 - y0:g} cm"
        w = self.sh.textw(t, size, "SemiBold")
        mid = (b0 + b1) / 2
        # vertical text: render rotated
        fnt = font(size, "SemiBold")
        tw, th = int((w + 10) * SS), int((size + 8) * SS)
        tim = Image.new("RGBA", (tw, th), rgb(PANEL, 255))
        ImageDraw.Draw(tim).text((tw / 2, th / 2), t, font=fnt, fill=rgb(col, 255), anchor="mm")
        tim = tim.rotate(90, expand=True)
        self.sh.im.paste(tim, (int(a * SS - tim.size[0] / 2), int(mid * SS - tim.size[1] / 2)), tim)

    def callout(self, x, y, tx, ty, text, maxw=300, size=17, col=NOTE, anchor="la"):
        """Leader from cm point (x, y) to text at final px (tx, ty)."""
        a, b = self.px(x, y)
        self.sh.ellipse(a, b, 4, 4, fill=col)
        lx = tx if anchor == "la" else tx
        self.sh.line([(a, b), (lx, ty + size * 0.6)], col, 1.3)
        if anchor == "ra":
            lines = wrap(self.sh.d, text, font(size, "Medium"), maxw)
            yy = ty
            for ln in lines:
                self.sh.text(tx - 4, yy, ln, size, "Medium", col, anchor="ra")
                yy += size * 1.3
            return yy
        return self.sh.text(tx + 4, ty, text, size, "Medium", col, maxw=maxw)


# ------------------------------------------------------------------ shared drawing helpers
def rng(seed):
    return random.Random(seed)


def scale_figure(v, x, label=True):
    """Simple 180 cm standing figure, front view, feet at (x, 0)."""
    col = "#6E7174"
    v.circle(x, 168, 11, fill=col, outline=None)
    v.poly([(x - 5, 156), (x + 5, 156), (x + 5, 151), (x - 5, 151)], fill=col, outline=None)
    v.poly([(x - 22, 150), (x + 22, 150), (x + 18, 96), (x - 18, 96)], fill=col, outline=None)
    v.poly([(x - 22, 150), (x - 28, 148), (x - 30, 84), (x - 23, 84), (x - 19, 130)], fill=col, outline=None)
    v.poly([(x + 22, 150), (x + 28, 148), (x + 30, 84), (x + 23, 84), (x + 19, 130)], fill=col, outline=None)
    v.poly([(x - 18, 96), (x - 2, 96), (x - 4, 0), (x - 16, 0)], fill=col, outline=None)
    v.poly([(x + 18, 96), (x + 2, 96), (x + 4, 0), (x + 16, 0)], fill=col, outline=None)
    if label:
        v.dim_v(0, 180, x - 34, "180 cm", size=14, col=INK2)


def log_h(v, x0, x1, yc, d=30, seed=0, bark=None, ends=True, outline=INK):
    """Horizontal log seen side-on (front elevation)."""
    r = rng(seed)
    bark = bark or C["Bark"]
    rad = d / 2
    top, bot = yc + rad, yc - rad
    # body with slight irregular ends
    j0 = r.uniform(-1.5, 1.5)
    j1 = r.uniform(-1.5, 1.5)
    pts = [(x0 + j0, bot + 2), (x0 + j0 - 1.2, yc), (x0 + j0, top - 2), (x1 + j1, top - 2), (x1 + j1 + 1.2, yc), (x1 + j1, bot + 2)]
    v.poly([(x0 + j0 + 2, top), (x1 + j1 - 2, top), (x1 + j1, top - 2)] + pts[3:] + [(x1 + j1 - 2, bot), (x0 + j0 + 2, bot)] + pts[:3],
           fill=bark, outline=None)
    v.rect(x0 + j0 + 2, yc + rad * 0.35, x1 + j1 - 2, top - 1, fill=mix(bark, C["Lichen"], 0.28), outline=None)
    v.rect(x0 + j0 + 2, bot + 1, x1 + j1 - 2, yc - rad * 0.45, fill=mix(bark, "#000000", 0.35), outline=None)
    # bark streaks
    n = int((x1 - x0) / 22)
    for _ in range(n):
        sx = r.uniform(x0 + 6, x1 - 20)
        sy = r.uniform(bot + 4, top - 4)
        v.line([(sx, sy), (sx + r.uniform(8, 26), sy + r.uniform(-1, 1))], mix(bark, "#000000", 0.45), 1)
    # knots
    for _ in range(max(1, n // 6)):
        kx, ky = r.uniform(x0 + 20, x1 - 20), r.uniform(bot + 8, top - 8)
        v.circle(kx, ky, r.uniform(1.6, 2.6), fill=mix(bark, "#000000", 0.5), outline=None)
    if ends:
        # visible fresh-cut sliver at each end (axe-cut chamfer)
        v.poly([(x0 + j0, bot + 3), (x0 + j0 + 3.5, bot + 2), (x0 + j0 + 3.5, top - 2), (x0 + j0, top - 3)], fill=C["Fresh-cut Wood"], outline=None)
        v.poly([(x1 + j1, bot + 3), (x1 + j1 - 3.5, bot + 2), (x1 + j1 - 3.5, top - 2), (x1 + j1, top - 3)], fill=C["Fresh-cut Wood"], outline=None)
    v.line([(x0 + j0 + 2, top), (x1 + j1 - 2, top)], outline, 1.5)
    v.line([(x0 + j0 + 2, bot), (x1 + j1 - 2, bot)], outline, 1.5)
    v.line([(x0 + j0 + 2, top), (x0 + j0, top - 3), (x0 + j0 - 1.2, yc), (x0 + j0, bot + 3), (x0 + j0 + 2, bot)], outline, 1.5)
    v.line([(x1 + j1 - 2, top), (x1 + j1, top - 3), (x1 + j1 + 1.2, yc), (x1 + j1, bot + 3), (x1 + j1 - 2, bot)], outline, 1.5)


def log_end(v, cx, cy, d=30, seed=0, outline=INK):
    """Cut end of a log (end / section view)."""
    r = rng(seed)
    rad = d / 2
    v.circle(cx, cy, rad, fill=C["Bark"], outline=outline, width=1.5)
    v.circle(cx, cy, rad - 2.2, fill=C["Fresh-cut Wood"], outline=None)
    ox, oy = r.uniform(-1.5, 1.5), r.uniform(-1.5, 1.5)
    for k in (0.75, 0.5, 0.28):
        v.circle(cx + ox * k, cy + oy * k, (rad - 2.2) * k, fill=None, outline=mix(C["Fresh-cut Wood"], C["Bark"], 0.45), width=1)
    v.circle(cx + ox * 0.2, cy + oy * 0.2, 1.0, fill=mix(C["Fresh-cut Wood"], C["Bark"], 0.6), outline=None)
    a = r.uniform(0, 6.28)
    v.line([(cx + ox * 0.2, cy + oy * 0.2), (cx + math.cos(a) * rad * 0.8, cy + math.sin(a) * rad * 0.8)], mix(C["Fresh-cut Wood"], C["Bark"], 0.65), 1)


def pole_v(v, xc, y0, y1, d=20, seed=0, bark=None, sharpen=0, outline=INK):
    """Vertical log/pole/stake, front elevation. sharpen = length of pointed tip at y1 (cm)."""
    r = rng(seed)
    bark = bark or C["Bark"]
    rad = d / 2
    body_top = y1 - sharpen
    v.rect(xc - rad, y0, xc + rad, body_top, fill=bark, outline=None)
    v.rect(xc - rad, y0, xc - rad * 0.45, body_top, fill=mix(bark, "#000000", 0.3), outline=None)
    v.rect(xc + rad * 0.3, y0, xc + rad * 0.85, body_top, fill=mix(bark, C["Lichen"], 0.25), outline=None)
    for _ in range(int((body_top - y0) / 25)):
        sy = r.uniform(y0 + 5, body_top - 10)
        sx = r.uniform(xc - rad + 2, xc + rad - 2)
        v.line([(sx, sy), (sx + r.uniform(-1, 1), sy + r.uniform(6, 18))], mix(bark, "#000000", 0.45), 1)
    if sharpen:
        v.poly([(xc - rad, body_top), (xc + rad, body_top), (xc + r.uniform(-1, 1), y1)], fill=C["Fresh-cut Wood"], outline=outline, width=1.5)
    v.line([(xc - rad, y0), (xc - rad, body_top)], outline, 1.5)
    v.line([(xc + rad, y0), (xc + rad, body_top)], outline, 1.5)
    if not sharpen:
        v.line([(xc - rad, body_top), (xc + rad, body_top)], outline, 1.5)


def stake(v, x, y, ang_deg, length, d=8, tip=25, col=None, tipcol=None, outline=INK, width=1.3):
    """Stake from base (x, y) pointing at angle (deg, 0 = +x, 90 = up)."""
    col = col or C["Bark"]
    tipcol = tipcol or C["Fresh-cut Wood"]
    a = math.radians(ang_deg)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    r = d / 2
    bx, by = x + ux * (length - tip), y + uy * (length - tip)
    ex, ey = x + ux * length, y + uy * length
    v.poly([(x + nx * r, y + ny * r), (bx + nx * r, by + ny * r), (bx - nx * r, by - ny * r), (x - nx * r, y - ny * r)], fill=col, outline=outline, width=width)
    v.poly([(bx + nx * r, by + ny * r), (ex, ey), (bx - nx * r, by - ny * r)], fill=tipcol, outline=outline, width=width)


def plank(v, x0, y0, x1, y1, seed=0, col=None, nails=(), outline=INK):
    r = rng(seed)
    col = col or C["Weathered Plank"]
    v.rect(x0, y0, x1, y1, fill=col, outline=outline, width=1.5)
    vertical = (y1 - y0) > (x1 - x0)
    n = 3
    for i in range(n):
        if vertical:
            gx = x0 + (x1 - x0) * (i + 1) / (n + 1) + r.uniform(-2, 2)
            v.line([(gx, y0 + 3), (gx + r.uniform(-1.5, 1.5), y1 - 3)], mix(col, "#000000", 0.28), 1)
        else:
            gy = y0 + (y1 - y0) * (i + 1) / (n + 1) + r.uniform(-1, 1)
            v.line([(x0 + 3, gy), (x1 - 3, gy + r.uniform(-1, 1))], mix(col, "#000000", 0.28), 1)
    for (nx, ny) in nails:
        v.circle(nx, ny, 1.4, fill="#2A2A2A", outline=None)


def plate(v, x0, y0, x1, y1, seed=0, welds=True, outline=INK, rust=0.35):
    r = rng(seed)
    v.rect(x0, y0, x1, y1, fill=C["Steel"], outline=None)
    # rust blotches and streaks
    for _ in range(int(abs((x1 - x0) * (y1 - y0)) / 900 * rust * 3)):
        cx, cy = r.uniform(x0 + 4, x1 - 4), r.uniform(y0 + 4, y1 - 4)
        rr = r.uniform(2, 8)
        v.circle(cx, cy, rr, fill=r.choice([C["Rust Orange"], C["Old Rust"], C["Rust Bloom"]]), outline=None, alpha=150)
    for _ in range(int((x1 - x0) / 25)):
        sx = r.uniform(x0 + 5, x1 - 5)
        sy = r.uniform(y0 + (y1 - y0) * 0.5, y1 - 4)
        v.line([(sx, sy), (sx + r.uniform(-1, 1), sy - r.uniform(15, 50))], C["Old Rust"], 1.5, alpha=170)
    v.rect(x0, y0, x1, y1, fill=None, outline=outline, width=1.5)
    if welds:
        # weld bead around the edge (dashed light line inset 1.5 cm)
        for (a, b) in [((x0 + 1.5, y0 + 1.5), (x1 - 1.5, y0 + 1.5)), ((x1 - 1.5, y0 + 1.5), (x1 - 1.5, y1 - 1.5)),
                       ((x1 - 1.5, y1 - 1.5), (x0 + 1.5, y1 - 1.5)), ((x0 + 1.5, y1 - 1.5), (x0 + 1.5, y0 + 1.5))]:
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            n = int(L / 4)
            for i in range(0, n, 2):
                t0, t1 = i / n, min(1, (i + 1.2) / n)
                v.line([(a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0), (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)],
                       "#B9B2A4", 2)


def rope(v, pts, width=2):
    v.line(pts, "#8C7A58", width + 1)
    v.line(pts, "#B59C6E", max(1, width - 1))


def barbed_wire(v, x0, y0, x1, y1, step=12, col="#55595B"):
    v.line([(x0, y0), (x1, y1)], col, 1.6)
    L = math.hypot(x1 - x0, y1 - y0)
    n = int(L / step)
    for i in range(1, n):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        v.line([(x - 2, y - 2.5), (x + 2, y + 2.5)], col, 1.3)
        v.line([(x - 2, y + 2.5), (x + 2, y - 2.5)], col, 1.3)


def ivy_cluster(v, cx, cy, spread, n, seed=0, cols=None, leaf=3.2, up=1.0):
    """Cluster of ivy leaves around (cx, cy); 'up' > 1 elongates vertically."""
    r = rng(seed)
    cols = cols or [C["Ivy"], C["Moss"], C["Deep Forest"], C["Lichen"]]
    weights = [0.42, 0.3, 0.2, 0.08]
    for _ in range(n):
        x = cx + r.gauss(0, spread)
        y = cy + r.gauss(0, spread * up)
        col = r.choices(cols, weights=weights[:len(cols)])[0]
        rr = leaf * r.uniform(0.7, 1.25)
        v.circle(x, y, rr, fill=col, outline=None)


def ivy_vine(v, x, y, length, seed=0, drift=0.0, down=False, density=1.0, leaf=3.0):
    """Vine growing up (or hanging down) from (x, y)."""
    r = rng(seed)
    pts = [(x, y)]
    cx, cy = x, y
    step = 6
    for i in range(int(length / step)):
        cx += r.uniform(-3, 3) + drift
        cy += -step if down else step
        pts.append((cx, cy))
    v.line(pts, "#3B3426", 1.2)
    for (px_, py_) in pts[1:]:
        if r.random() < 0.85 * density:
            ivy_cluster(v, px_, py_, 3.2, 3, seed=r.randint(0, 1 << 30), leaf=leaf)


def moss_band(v, x0, x1, y0, h, seed=0, density=1.0):
    r = rng(seed)
    n = int((x1 - x0) * h / 14 * density)
    for _ in range(n):
        x = r.uniform(x0, x1)
        y = y0 + abs(r.gauss(0, h * 0.5))
        y = min(y, y0 + h)
        v.circle(x, y, r.uniform(1.6, 3.6), fill=r.choice([C["Moss"], C["Moss"], C["Lichen"], C["Ivy"]]), outline=None, alpha=225)


def grass_tufts(v, x0, x1, y, n, seed=0, h=14):
    r = rng(seed)
    for _ in range(n):
        x = r.uniform(x0, x1)
        for k in range(5):
            a = math.radians(r.uniform(60, 120))
            L = r.uniform(h * 0.5, h)
            v.line([(x, y), (x + math.cos(a) * L, y + math.sin(a) * L)], r.choice([C["Moss"], C["Lichen"], C["Ivy"]]), 1.3)


def sapling(v, x, y, h=120, seed=0):
    r = rng(seed)
    v.line([(x, y), (x + r.uniform(-4, 4), y + h)], "#4A3A2C", 2.2)
    for i in range(6):
        t = 0.35 + i * 0.11
        bx, by = x, y + h * t
        side = -1 if i % 2 else 1
        ex, ey = bx + side * r.uniform(12, 24) * (1.1 - t), by + r.uniform(8, 16)
        v.line([(bx, by), (ex, ey)], "#4A3A2C", 1.3)
        ivy_cluster(v, ex, ey, 4, 7, seed=r.randint(0, 1 << 30), cols=[C["Moss"], C["Lichen"], C["Ivy"]], leaf=2.8)
    ivy_cluster(v, x, y + h, 6, 10, seed=r.randint(0, 1 << 30), cols=[C["Moss"], C["Lichen"], C["Ivy"]], leaf=3)


def tin_can(v, x, ytop, seed=0):
    r = rng(seed)
    w, h = 7.5, 11
    ang = r.uniform(-8, 8)
    v.rect(x - w / 2, ytop - h, x + w / 2, ytop, fill=mix(C["Steel"], C["Rust Orange"], r.uniform(0.2, 0.6)), outline=INK, width=1.2)
    v.line([(x - w / 2, ytop - 2), (x + w / 2, ytop - 2)], "#9EA3A5", 1)
    v.line([(x - w / 2, ytop - h + 2), (x + w / 2, ytop - h + 2)], "#9EA3A5", 1)


def rock(v, cx, cy, rr, seed=0, col=None):
    r = rng(seed)
    col = col or "#7D7F7A"
    pts = []
    n = 8
    for i in range(n):
        a = 2 * math.pi * i / n + r.uniform(-0.2, 0.2)
        k = r.uniform(0.75, 1.1)
        pts.append((cx + math.cos(a) * rr * k, cy + math.sin(a) * rr * k * 0.75))
    v.poly(pts, fill=col, outline=INK, width=1.2)
    v.poly(pts[1:4] + [(cx, cy)], fill=mix(col, "#FFFFFF", 0.15), outline=None)


def load_raw(name):
    return Image.open(os.path.join(RAW, name)).convert("RGB")


def caveat(sheet, x, y, w, text, size=17):
    """Amber caveat strip (used to flag drift or blocked items on the sheet itself)."""
    lines = wrap(sheet.d, text, font(size, "Medium"), w - 24)
    h = len(lines) * size * 1.3 + 16
    sheet.rect(x, y, w, h, fill="#E9D8B8", outline="#A0692E", width=1.5, radius=4)
    sheet.text(x + 12, y + 8, text, size, "Medium", "#5B3A12", maxw=w - 24)
    return y + h


def blocked_box(sheet, x, y, w, h, title, text):
    sheet.rect(x, y, w, h, fill="#D5D2CB", outline="#8C887E", width=2, radius=6)
    # hatching
    step = 26
    for k in range(0, int(w + h), step):
        xa, ya = x + k, y
        xb, yb = x + k - h, y + h
        if xa > x + w:
            ya += xa - (x + w)
            xa = x + w
        if xb < x:
            yb -= x - xb
            xb = x
        if ya < y + h and yb > y:
            sheet.line([(xa, ya), (xb, yb)], "#C4C0B8", 2)
    sheet.label_box(x + 18, y + 18, "BLOCKED", 18, "Bold", "#FFFFFF", "#8A3B1E")
    sheet.text(x + 20, y + 60, title, 22, "Bold", INK, maxw=w - 40)
    sheet.text(x + 20, y + 92, text, 17, "Regular", INK2, maxw=w - 40)
