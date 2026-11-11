#!/usr/bin/env python3
"""Draw the cutest cat (cutest-cat-01 entry image).

Pure stdlib + Pillow at BUILD time only. The submitted entry is main.ts,
which copies the PNG this script renders (entry.png) to /output/entry.png.
The drawing is fully procedural: no photo, no copied artwork, no network.

Design, aimed at the judge's criteria in order:
  1. One cat, huge in frame, unmistakable at a glance.
  2. Cute: giant round head, oversized bright eyes with big highlights,
     tiny pink nose, small smile, pink blush, soft round shapes.
  3. Charm: slight head tilt, curled tail wrapping around, front paws
     on a red yarn ball with a loose strand.
  4. Craft: correct anatomy (2 ears, 2 eyes, whiskers, 1 tail), clean
     vector-style shapes, no text, no artefacts.
  5. Reads small: cat fills ~75% of the frame, plain warm background,
     nothing crowds it.
"""

from PIL import Image, ImageDraw, ImageFilter

S = 2  # supersample factor; final image is 1024x1024
W = 1024 * S
H = 1024 * S
CX = W // 2

# Palette (warm, soft, high contrast where it matters)
BG_TOP = (255, 246, 232)
BG_BOT = (255, 227, 194)
GLOW = (255, 214, 170)
FUR = (255, 214, 150)        # ginger-cream
FUR_DARK = (244, 178, 105)    # ginger stripes / ear backs
FUR_LIGHT = (255, 240, 214)   # belly / muzzle
PINK = (255, 170, 185)
PINK_DEEP = (240, 120, 140)
NOSE = (235, 110, 130)
EYE_BROWN = (94, 58, 28)
EYE_AMBER = (176, 110, 44)
BLUSH = (255, 150, 160)
WHISKER = (120, 95, 80)
YARN = (226, 62, 78)
YARN_DARK = (178, 38, 54)
SHADOW = (210, 160, 110)

img = Image.new("RGB", (W, H), BG_TOP)
d = ImageDraw.Draw(img, "RGBA")


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(top, bot):
    for y in range(H):
        d.line([(0, y), (W, y)], fill=lerp(top, bot, y / H))


def ellipse(cx, cy, rx, ry, fill=None, outline=None, width=1):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
              fill=fill, outline=outline, width=width)


def circle(cx, cy, r, **kw):
    ellipse(cx, cy, r, r, **kw)


def rpoly(points, fill=None, outline=None, width=1):
    d.polygon(points, fill=fill, outline=outline, width=width)


def tube(points, radius, fill):
    """A smooth thick curve: circles along a polyline."""
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        steps = max(2, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 / 6))
        for s in range(steps + 1):
            t = s / steps
            circle(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, radius, fill=fill)


def arc(cx, cy, rx, ry, a0, a1, fill, width):
    d.arc([cx - rx, cy - ry, cx + rx, cy + ry], a0, a1, fill=fill, width=width)


# ---------------------------------------------------------------- background
vgrad(BG_TOP, BG_BOT)

# soft glow disc behind the cat
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([CX - 700, 180, CX + 700, 1780], fill=GLOW + (90,))
glow = glow.filter(ImageFilter.GaussianBlur(120))
img.paste(glow, (0, 0), glow)
d = ImageDraw.Draw(img, "RGBA")

# faint polka dots, kept sparse and far from the face
for (x, y, r, a) in [(220, 260, 26, 26), (1830, 300, 30, 22), (160, 1500, 24, 24),
                     (1900, 1560, 26, 20), (330, 700, 18, 18), (1730, 820, 18, 18),
                     (1024, 150, 20, 16), (560, 1800, 22, 18), (1500, 1830, 22, 18)]:
    circle(x, y, r, fill=(255, 190, 140, a))

# ground shadow
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([CX - 560, 1690, CX + 560, 1830], fill=SHADOW + (70,))
shadow = shadow.filter(ImageFilter.GaussianBlur(28))
img.paste(shadow, (0, 0), shadow)
d = ImageDraw.Draw(img, "RGBA")

# ---------------------------------------------------------------- tail (behind body)
# thin tail slipping out from behind the body, curling on the ground
# at the lower right with its tip flicked up
tail_pts = [(CX + 400, 1450), (CX + 580, 1560), (CX + 640, 1680),
            (CX + 580, 1780), (CX + 460, 1790)]
for i in range(len(tail_pts) - 1):
    x0, y0 = tail_pts[i]
    x1, y1 = tail_pts[i + 1]
    steps = max(2, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 / 6))
    for s in range(steps + 1):
        t = s / steps
        gt = (i + t) / (len(tail_pts) - 1)  # 0 at base, 1 at tip
        r = 56 - 26 * gt
        circle(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, r, fill=FUR)
# one ginger ring near the middle of the visible tail
d.arc([CX + 560, 1600, CX + 700, 1740], 120, 300, fill=FUR_DARK, width=20)

# ---------------------------------------------------------------- body
ellipse(CX, 1520, 430, 300, fill=FUR)                    # torso
ellipse(CX, 1560, 300, 220, fill=FUR_LIGHT)             # cream belly
# stripes on the back
for x in (CX - 260, CX - 90, CX + 90, CX + 260):
    d.rounded_rectangle([x - 26, 1300, x + 26, 1460], radius=26, fill=FUR_DARK)

# ---------------------------------------------------------------- yarn ball (charm prop, right paw)
YB = (CX + 470, 1640)
circle(*YB, 150, fill=YARN)
# visible wound strands: offset arcs across the ball
for (ox, oy, rr) in [(-40, -30, 120), (30, -50, 110), (-10, 40, 125), (50, 30, 100)]:
    arc(YB[0] + ox, YB[1] + oy, rr, rr, 20, 200, YARN_DARK, 9)
ellipse(YB[0] - 70, YB[1] - 80, 46, 30, fill=(255, 255, 255, 70))  # sheen
# loose strand curling toward the paw
tube([(YB[0] - 120, YB[1] + 90), (CX + 220, 1760), (CX + 60, 1720),
      (CX - 40, 1760)], 10, YARN_DARK)

# ---------------------------------------------------------------- head (own layer, tilted)
head = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(head, "RGBA")


def he(cx, cy, rx, ry, **kw):
    hd.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], **kw)


def hc(cx, cy, r, **kw):
    he(cx, cy, r, r, **kw)


def hp(points, **kw):
    hd.polygon(points, **kw)


def harc(cx, cy, rx, ry, a0, a1, fill, width):
    hd.arc([cx - rx, cy - ry, cx + rx, cy + ry], a0, a1, fill=fill, width=width)


# ears (behind head): rounded triangles
for sgn in (-1, 1):
    ex = CX + sgn * 430
    hp([(ex - 210, 620), (ex + 60 * sgn, 300), (ex + 250, 560)], fill=FUR_DARK)
    hp([(ex - 130, 570), (ex + 45 * sgn, 390), (ex + 165, 540)], fill=PINK)
# head
he(CX, 900, 640, 560, fill=FUR)
# forehead stripes
for dx in (-150, 0, 150):
    hd.rounded_rectangle([CX + dx - 34, 380, CX + dx + 34, 520],
                         radius=34, fill=FUR_DARK)
# muzzle patch
he(CX, 1080, 300, 190, fill=FUR_LIGHT)

# ---- eyes: huge, bright, glossy
for sgn in (-1, 1):
    ex = CX + sgn * 270
    ey = 830
    he(ex, ey, 128, 158, fill=(255, 255, 255))            # white
    he(ex, ey + 6, 104, 132, fill=EYE_AMBER)              # iris
    he(ex, ey + 6, 62, 82, fill=EYE_BROWN)                # pupil
    hc(ex - 34, ey - 52, 34, fill=(255, 255, 255))         # big highlight
    hc(ex + 40, ey + 44, 16, fill=(255, 255, 255, 220))    # small highlight
    harc(ex, ey, 128, 158, 180, 360, (60, 40, 25), 10)     # upper lash line
# tiny happy eye creases
harc(CX - 270, 640, 90, 60, 200, 340, FUR_DARK, 8)
harc(CX + 270, 640, 90, 60, 200, 340, FUR_DARK, 8)

# ---- nose + mouth
hp([(CX - 62, 1010), (CX + 62, 1010), (CX, 1085)], fill=NOSE)
harc(CX - 62, 1060, 62, 55, 10, 170, (150, 80, 70), 10)
harc(CX + 62, 1060, 62, 55, 10, 170, (150, 80, 70), 10)

# ---- blush
he(CX - 420, 1060, 110, 62, fill=BLUSH + (150,))
he(CX + 420, 1060, 110, 62, fill=BLUSH + (150,))

# ---- whiskers
for sgn in (-1, 1):
    for j, (dy, bend) in enumerate(((-40, -70), (0, -10), (40, 60))):
        x0 = CX + sgn * 300
        y0 = 1030 + dy
        x1 = CX + sgn * 590
        y1 = y0 + bend
        xm = (x0 + x1) / 2
        ym = (y0 + y1) / 2 - 18
        hd.line([(x0, y0), (xm, ym), (x1, y1)], fill=WHISKER + (200,),
                width=7, joint="curve")

# tilt the whole head ~5 degrees around the neck and paste
head = head.rotate(5, resample=Image.BICUBIC, center=(CX, 1420))
img.paste(head, (0, 0), head)
d = ImageDraw.Draw(img, "RGBA")

# ---------------------------------------------------------------- paws (in front of body)
for sgn in (-1, 1):
    px = CX + sgn * 210
    ellipse(px, 1690, 130, 95, fill=FUR_LIGHT)
    ellipse(px, 1690, 130, 95, outline=FUR_DARK, width=6)
    # toe lines
    for dx in (-45, 0, 45):
        d.line([(px + dx, 1640), (px + dx, 1710)], fill=FUR_DARK, width=7)
# left paw rests on the yarn strand
ellipse(CX - 210, 1690, 130, 95, fill=FUR_LIGHT)

img = img.convert("RGB").resize((1024, 1024), Image.LANCZOS)
img.save("entry.png", optimize=True)
print("saved entry.png")
