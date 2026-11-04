#!/usr/bin/env python3
"""Hype story v2: realistic dual-monitor desk setup. Left = website build, right = coding."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H, FPS, DUR = 1080, 1920, 30, 15
N = FPS * DUR
OUT = "/tmp/hype2_frames"
os.makedirs(OUT, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

BG = (10, 13, 12); PANEL = (21, 28, 26); GREEN = (122, 193, 67)
TEXT = (238, 243, 238); MUTED = (154, 165, 160); LINE = (34, 43, 41)
YEL = (230, 197, 71); DESK = (32, 26, 22); DESK2 = (22, 18, 15)

f_name = ImageFont.truetype(FB, 52)
f_sub = ImageFont.truetype(FR, 28)
f_code = ImageFont.truetype(FM, 26)
f_code_b = ImageFont.truetype(FMB, 27)
f_big = ImageFont.truetype(FB, 92)
f_title = ImageFont.truetype(FB, 60)
f_mid = ImageFont.truetype(FB, 42)
f_small = ImageFont.truetype(FR, 24)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def fade(t, t0, d=0.6): return clamp((t - t0) / d)
def pop(t, t0, d=0.35):
    x = clamp((t - t0) / d); return 1.18 - 0.18 * (1 - (1 - x) ** 3) if x < 1 else 1.0

def rr(d, xy, r, fill=None, outline=None, w=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

def txt_center(d, y, s, font, fill):
    bb = d.textbbox((0, 0), s, font=font)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), s, font=font, fill=fill)

# --- circular photo ---
ph = Image.open("/home/hatch/workspace/atikur-site/photo.jpg").convert("RGB")
S = 300
side = min(ph.size)
ph = ph.crop(((ph.width - side)//2, (ph.height - side)//2, (ph.width + side)//2, (ph.height + side)//2)).resize((S, S), Image.LANCZOS)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).ellipse((0, 0, S, S), fill=255)
ring = Image.new("RGBA", (S + 14, S + 14), (0, 0, 0, 0))
ImageDraw.Draw(ring).ellipse((0, 0, S + 14, S + 14), outline=GREEN + (255,), width=7)
photo_img = Image.new("RGBA", (S + 14, S + 14), (0, 0, 0, 0))
photo_img.paste(ph, (7, 7), mask)
photo_img.alpha_composite(ring)

# monitor geometry
MON = [
    {"x0": 40, "x1": 510, "title": "atikur.cyou — live preview"},
    {"x0": 570, "x1": 1040, "title": "code — portfolio"},
]
CY0, CH = 700, 470          # screen content top / height
BEZ, CHIN = 14, 42

CODE_LINES = [
    (2.0, "$ whoami", GREEN, f_code_b),
    (2.8, "> atikur_rahman", TEXT, f_code),
    (3.6, "$ npx create-site atikur", GREEN, f_code_b),
    (4.4, "> scaffolding ...", MUTED, f_code),
    (5.2, '<section class="hero">', TEXT, f_code),
    (6.0, "  <h1>Atikur Rahman</h1>", YEL, f_code),
    (6.8, "</section>", TEXT, f_code),
    (7.6, "$ npm run deploy", GREEN, f_code_b),
    (8.6, ">> LIVE: atikur.cyou", YEL, f_code_b),
]

def draw_monitor(d, mx0, mx1, t, pa, build_fn):
    # bezel
    ox0, ox1 = mx0 - BEZ, mx1 + BEZ
    oy0, oy1 = CY0 - BEZ, CY0 + CH + CHIN
    rr(d, (ox0, oy0, ox1, oy1), 22, fill=(8, 10, 9, int(255 * pa)), outline=(50, 58, 54, int(255 * pa)), w=2)
    # screen
    rr(d, (mx0, CY0, mx1, CY0 + CH), 8, fill=(13, 17, 16, int(255 * pa)))
    # screen-on flicker glow
    fl = fade(t, 1.5, 0.25)
    if fl > 0:
        d.rounded_rectangle((mx0, CY0, mx1, CY0 + CH), radius=8, outline=GREEN + (int(90 * fl * pa),), width=3)
    # power LED
    cx = (ox0 + ox1) // 2
    d.ellipse((cx - 5, oy1 - 26, cx + 5, oy1 - 16), fill=GREEN + (int(255 * pa),))
    # stand neck + base
    d.rectangle((cx - 28, oy1, cx + 28, 1360), fill=(16, 19, 18, int(255 * pa)))
    rr(d, (cx - 120, 1340, cx + 120, 1372), 14, fill=(16, 19, 18, int(255 * pa)), outline=(50, 58, 54, int(255 * pa)), w=2)
    # content (clipped look via inner draws)
    build_fn(d, mx0, mx1, t, pa)

def left_screen(d, x0, x1, t, pa):
    w = x1 - x0
    # browser chrome
    rr(d, (x0 + 10, CY0 + 12, x1 - 10, CY0 + 52), 10, fill=(30, 38, 36, int(255 * pa)))
    for cx, cc in zip((x0 + 34, x0 + 56, x0 + 78), ((255, 95, 86), (255, 189, 46), (39, 201, 63))):
        d.ellipse((cx - 7, CY0 + 26, cx + 7, CY0 + 40), fill=cc + (int(255 * pa),))
    bb = d.textbbox((0, 0), "atikur.cyou", font=f_small)
    d.text((x0 + 100, CY0 + 26), "atikur.cyou", font=f_small, fill=MUTED + (int(255 * pa),))
    # nav
    s = pop(t, 3.4)
    if t >= 3.4:
        nw = int((w - 40) * s); nx = x0 + 20 + (w - 40 - nw) // 2
        rr(d, (nx, CY0 + 66, nx + nw, CY0 + 100), 10, fill=(26, 34, 31, int(255 * pa)))
        d.ellipse((nx + 12, CY0 + 74, nx + 32, CY0 + 94), fill=GREEN + (int(255 * pa),))
        for k in range(3):
            d.rounded_rectangle((nx + 150 + k * 62, CY0 + 78, nx + 192 + k * 62, CY0 + 90), radius=6, fill=(60, 70, 66, int(255 * pa)))
    # hero
    s = pop(t, 4.6)
    if t >= 4.6:
        hw = int((w - 40) * s); hx = x0 + 20 + (w - 40 - hw) // 2
        rr(d, (hx, CY0 + 114, hx + hw, CY0 + 280), 14, fill=(18, 24, 22, int(255 * pa)), outline=LINE + (int(255 * pa),), w=2)
        d.rounded_rectangle((hx + 20, CY0 + 140, hx + 20 + int(190 * s), CY0 + 160), radius=8, fill=GREEN + (int(255 * pa),))
        d.rounded_rectangle((hx + 20, CY0 + 170, hx + 20 + int(130 * s), CY0 + 186), radius=8, fill=(70, 80, 76, int(255 * pa)))
        d.rounded_rectangle((hx + hw - 130, CY0 + 140, hx + hw - 20, CY0 + 260), radius=12, fill=(35, 46, 42, int(255 * pa)), outline=GREEN + (int(255 * pa),), width=2)
    # cards
    for k, ct in enumerate((5.8, 6.6, 7.4)):
        s = pop(t, ct)
        if t >= ct:
            cw = int(128 * s); cx = x0 + 20 + k * 142 + (128 - cw) // 2
            rr(d, (cx, CY0 + 296, cx + cw, CY0 + 430), 12, fill=(26, 34, 31, int(255 * pa)), outline=GREEN + (int(200 * pa),), w=2)
            d.rounded_rectangle((cx + 12, CY0 + 310, cx + cw - 12, CY0 + 324), radius=6, fill=GREEN + (int(255 * pa),))
    # deployed badge
    a = fade(t, 8.8)
    if a > 0:
        rr(d, (x0 + 120, CY0 + CH - 62, x1 - 120, CY0 + CH - 14), 24, fill=GREEN + (int(255 * a),))
        bb = d.textbbox((0, 0), "DEPLOYED", font=f_small)
        d.text(((x0 + x1 - (bb[2] - bb[0])) / 2 - bb[0], CY0 + CH - 52), "DEPLOYED", font=f_small, fill=(12, 17, 16, int(255 * a)))

def right_screen(d, x0, x1, t, pa):
    d.text((x0 + 18, CY0 + 18), "~/portfolio", font=f_small, fill=MUTED + (int(255 * pa),))
    ly = CY0 + 56
    for (st, txt, col, fn) in CODE_LINES:
        if t < st: break
        nch = int(clamp((t - st) / 0.7) * len(txt))
        if nch > 0:
            d.text((x0 + 18, ly), txt[:nch], font=fn, fill=col + (int(255 * pa),))
        if t < st + 0.7 and int(t * 3) % 2 == 0:
            bb = d.textbbox((0, 0), txt[:nch], font=fn)
            d.rectangle((x0 + 18 + bb[2] + 4, ly + 3, x0 + 18 + bb[2] + 16, ly + 30), fill=GREEN + (int(255 * pa),))
        ly += 44
        if ly > CY0 + CH - 30: break

def draw_frame(i):
    t = i / FPS
    im = Image.new("RGB", (W, H), BG)
    # wall glow behind monitors
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow)
    ga = fade(t, 1.5, 1.0)
    gd.ellipse((140, 480, 940, 1420), fill=(20, 38, 24))
    im = Image.blend(im, glow, 0.5 * ga + 0.15).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")

    # top: photo + name
    a = fade(t, 0.1)
    if a > 0:
        tmp = photo_img.copy()
        tmp.putalpha(tmp.split()[3].point(lambda v: int(v * a)))
        im.paste(tmp, ((W - S - 14) // 2, 84), tmp)
        d = ImageDraw.Draw(im, "RGBA")
    a = fade(t, 0.6)
    if a > 0:
        bb = d.textbbox((0, 0), "ATIKUR RAHMAN", font=f_name)
        d.text(((W - (bb[2]-bb[0]))/2 - bb[0], 412), "ATIKUR RAHMAN", font=f_name, fill=TEXT + (int(255*a),))
    a = fade(t, 1.1)
    if a > 0:
        bb = d.textbbox((0, 0), "coding live — dual setup", font=f_sub)
        d.text(((W - (bb[2]-bb[0]))/2 - bb[0], 478), "coding live — dual setup", font=f_sub, fill=GREEN + (int(255*a),))

    # desk surface
    pa = fade(t, 1.2)
    if pa > 0:
        d.rectangle((0, 1330, W, 1560), fill=DESK + (int(255*pa),))
        d.rectangle((0, 1330, W, 1352), fill=DESK2 + (int(255*pa),))
        # keyboard
        rr(d, (300, 1400, 780, 1500), 16, fill=(14, 17, 16, int(255*pa)), outline=(50,58,54,int(255*pa)), w=2)
        for r in range(3):
            for c in range(12):
                kx, ky = 322 + c*38, 1416 + r*26
                d.rounded_rectangle((kx, ky, kx+28, ky+18), radius=4, fill=(30,36,34,int(255*pa)))
        # mug
        d.rounded_rectangle((880, 1230, 950, 1330), radius=10, fill=(40, 48, 44, int(255*pa)))
        d.arc((950, 1252, 986, 1300), 270, 90, fill=(40,48,44,int(255*pa)), width=8)

    # monitors
    if pa > 0:
        draw_monitor(d, MON[0]["x0"], MON[0]["x1"], t, pa, left_screen)
        draw_monitor(d, MON[1]["x0"], MON[1]["x1"], t, pa, right_screen)
        # labels under monitors
        a2 = fade(t, 3.0)
        if a2 > 0:
            for m, lab in ((MON[0], "WEBSITE"), (MON[1], "CODE")):
                bb = d.textbbox((0, 0), lab, font=f_small)
                cx = (m["x0"] + m["x1"]) // 2
                d.text((cx - (bb[2]-bb[0])/2 - bb[0], 1380), lab, font=f_small, fill=MUTED + (int(255*a2),))

    # status
    if t < 12:
        st = "BUILDING" if t < 7.6 else "DEPLOYING"
        col = GREEN if t < 7.6 else YEL
        a = fade(t, 2.0)
        if a > 0:
            blink = "" if int(t*2) % 2 == 0 else " "
            bb = d.textbbox((0, 0), "> " + st + " ..." + blink, font=f_mid)
            d.text(((W-(bb[2]-bb[0]))/2 - bb[0], 1600), "> " + st + " ..." + blink, font=f_mid, fill=col + (int(255*a),))
    pw = int(W * clamp(t / 12))
    d.rectangle((0, H - 26, pw, H - 14), fill=GREEN)

    # finale
    fa = fade(t, 12.0, 0.8)
    if fa > 0:
        im.alpha_composite(Image.new("RGBA", (W, H), (6, 9, 8, int(205 * fa))))
        d = ImageDraw.Draw(im, "RGBA")
        bb = d.textbbox((0, 0), "atikur.cyou", font=f_big)
        d.text(((W-(bb[2]-bb[0]))/2 - bb[0], 700), "atikur.cyou", font=f_big, fill=GREEN + (int(255*fa),))
        bb = d.textbbox((0, 0), "LIVE NOW", font=f_title)
        d.text(((W-(bb[2]-bb[0]))/2 - bb[0], 830), "LIVE NOW", font=f_title, fill=TEXT + (int(255*fa),))
        bb = d.textbbox((0, 0), "Built by Atikur Rahman", font=f_sub)
        d.text(((W-(bb[2]-bb[0]))/2 - bb[0], 950), "Built by Atikur Rahman", font=f_sub, fill=MUTED + (int(255*fa),))
        bw, bh = 560, 110
        rr(d, ((W-bw)//2, 1080, (W+bw)//2, 1080+bh), 55, fill=GREEN + (int(255*fa),))
        bb = d.textbbox((0, 0), "Visit the site", font=f_mid)
        d.text(((W-(bb[2]-bb[0]))/2 - bb[0], 1080 + (bh-(bb[3]-bb[1]))/2 - bb[1]), "Visit the site", font=f_mid, fill=(12,17,16,int(255*fa)))

    im.convert("RGB").save(f"{OUT}/f{i:04d}.png")

for i in range(N):
    draw_frame(i)
    if i % 90 == 0: print(i, flush=True)
print("frames done")
