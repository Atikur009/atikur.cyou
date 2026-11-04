#!/usr/bin/env python3
"""Hype story video: coding on left, website building on right, his photo on top."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

W, H, FPS, DUR = 1080, 1920, 30, 15
N = FPS * DUR
OUT = "/tmp/hype_frames"
os.makedirs(OUT, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FMB = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

BG = (12, 17, 16); PANEL = (21, 28, 26); GREEN = (122, 193, 67)
TEXT = (238, 243, 238); MUTED = (154, 165, 160); LINE = (34, 43, 41)
YEL = (230, 197, 71); CYAN = (79, 195, 247)

f_title = ImageFont.truetype(FB, 64)
f_name = ImageFont.truetype(FB, 54)
f_sub = ImageFont.truetype(FR, 30)
f_code = ImageFont.truetype(FM, 30)
f_code_b = ImageFont.truetype(FMB, 32)
f_big = ImageFont.truetype(FB, 96)
f_mid = ImageFont.truetype(FB, 44)
f_small = ImageFont.truetype(FR, 26)

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def fade(t, t0, d=0.6): return clamp((t - t0) / d)
def pop(t, t0, d=0.35):
    x = clamp((t - t0) / d); return 1.15 - 0.15 * (1 - (1 - x) ** 3) if x < 1 else 1.0

def rr(d, xy, r, fill=None, outline=None, w=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=w)

def txt_center(d, y, s, font, fill, alpha=255):
    img = Image.new("RGBA", (W, 120), (0, 0, 0, 0))
    dd = ImageDraw.Draw(img)
    bb = dd.textbbox((0, 0), s, font=font)
    dd.text(((W - (bb[2] - bb[0])) / 2 - bb[0], 10), s, font=font, fill=fill + (alpha,))
    return img, y

# --- photo (circular, once) ---
ph = Image.open("/home/hatch/workspace/atikur-site/photo.jpg").convert("RGB")
S = 340
side = min(ph.size)
ph = ph.crop(((ph.width - side)//2, (ph.height - side)//2, (ph.width + side)//2, (ph.height + side)//2)).resize((S, S), Image.LANCZOS)
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).ellipse((0, 0, S, S), fill=255)
ring = Image.new("RGBA", (S + 16, S + 16), (0, 0, 0, 0))
ImageDraw.Draw(ring).ellipse((0, 0, S + 16, S + 16), outline=GREEN + (255,), width=8)
photo_img = Image.new("RGBA", (S + 16, S + 16), (0, 0, 0, 0))
photo_img.paste(ph, (8, 8), mask)
photo_img.alpha_composite(ring)

CODE_LINES = [
    (2.6, "$ whoami", GREEN, f_code_b),
    (3.4, "> atikur_rahman", TEXT, f_code),
    (4.2, "$ git init portfolio", GREEN, f_code_b),
    (5.0, "> repo ready", MUTED, f_code),
    (5.8, "$ build --pages 7", GREEN, f_code_b),
    (6.6, "> compiled OK", MUTED, f_code),
    (7.4, "$ deploy --prod", GREEN, f_code_b),
    (8.4, ">> LIVE: atikur.cyou", YEL, f_code_b),
]

def draw_frame(i):
    t = i / FPS
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im, "RGBA")
    # glow
    glow = Image.new("RGB", (W, H), BG)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((W/2 - 500, -260, W/2 + 500, 420), fill=(24, 40, 26))
    im = Image.blend(im, glow, 0.55).convert("RGBA")
    d = ImageDraw.Draw(im, "RGBA")

    # ---- top: photo + name ----
    a = fade(t, 0.1)
    if a > 0:
        px, py = (W - (S + 16)) // 2, 120
        tmp = photo_img.copy()
        alpha = tmp.split()[3].point(lambda v: int(v * a))
        tmp.putalpha(alpha)
        im.paste(tmp, (px, py), tmp)
    a = fade(t, 0.7)
    if a > 0:
        ov, oy = txt_center(d, 0, "ATIKUR RAHMAN", f_name, TEXT, int(255 * a))
        im.alpha_composite(ov, (0, 500))
    a = fade(t, 1.3)
    if a > 0:
        ov, oy = txt_center(d, 0, "I BUILD BRANDS & WEBSITES", f_sub, GREEN, int(255 * a))
        im.alpha_composite(ov, (0, 572))

    # ---- panels ----
    pa = fade(t, 2.2)
    if pa > 0:
        for (x0, title) in ((40, "terminal — zsh"), (560, "atikur.cyou — preview")):
            x1 = x0 + 480
            rr(d, (x0, 660, x1, 1360), 26, fill=PANEL + (int(255 * pa),), outline=LINE + (int(255 * pa),), w=2)
            # title bar
            d.rounded_rectangle((x0, 660, x1, 716), radius=26, fill=(30, 38, 36, int(255 * pa)))
            d.rectangle((x0, 690, x1, 716), fill=(30, 38, 36, int(255 * pa)))
            for cx, cc in zip((x0 + 28, x0 + 52, x0 + 76), ((255, 95, 86), (255, 189, 46), (39, 201, 63))):
                d.ellipse((cx - 8, 680, cx + 8, 696), fill=cc + (int(255 * pa),))
            bb = d.textbbox((0, 0), title, font=f_small)
            d.text((x0 + 100, 688 - bb[1]), title, font=f_small, fill=MUTED + (int(255 * pa),))

        # LEFT: code typing
        ly = 748
        for (st, txt, col, fn) in CODE_LINES:
            if t < st: break
            nch = int(clamp((t - st) / 0.7) * len(txt))
            if nch > 0:
                d.text((70, ly), txt[:nch], font=fn, fill=col + (int(255 * pa),))
            # cursor on active line
            if t < st + 0.7 and int(t * 3) % 2 == 0:
                bb = d.textbbox((0, 0), txt[:nch], font=fn)
                d.rectangle((70 + bb[2] + 4, ly + 4, 70 + bb[2] + 18, ly + 34), fill=GREEN + (int(255 * pa),))
            ly += 52
            if ly > 1300: break

        # RIGHT: website assembling
        bx0, bx1 = 560, 1040
        def popw(t0): return pop(t, t0)
        # nav bar
        s = popw(4.0)
        if t >= 4.0:
            nw, nh = int(440 * s), 44
            nx = bx0 + 20 + (440 - nw) // 2
            rr(d, (nx, 748, nx + nw, 748 + nh), 12, fill=(26, 34, 31, int(255 * pa)))
            d.ellipse((nx + 16, 758, nx + 40, 782), fill=GREEN + (int(255 * pa),))
            for k in range(3):
                d.rounded_rectangle((nx + 200 + k * 70, 762, nx + 250 + k * 70, 778), radius=8, fill=(60, 70, 66, int(255 * pa)))
        # hero
        s = popw(5.2)
        if t >= 5.2:
            hw, hh = int(440 * s), 200
            hx = bx0 + 20 + (440 - hw) // 2
            rr(d, (hx, 820, hx + hw, 820 + hh), 16, fill=(18, 24, 22, int(255 * pa)), outline=LINE + (int(255 * pa),), w=2)
            d.rounded_rectangle((hx + 24, 850, hx + 24 + int(220 * s), 872), radius=8, fill=GREEN + (int(255 * pa),))
            d.rounded_rectangle((hx + 24, 884, hx + 24 + int(160 * s), 902), radius=8, fill=(70, 80, 76, int(255 * pa)))
            d.rounded_rectangle((hx + 280, 850, hx + 400, 990), radius=14, fill=(35, 46, 42, int(255 * pa)), outline=GREEN + (int(255 * pa),), width=2)
        # cards
        for k, ct in enumerate((6.4, 7.2, 8.0)):
            s = popw(ct)
            if t >= ct:
                cw, chh = int(132 * s), int(150 * s)
                cx = bx0 + 20 + k * 148 + (132 - cw) // 2
                rr(d, (cx, 1050, cx + cw, 1050 + chh), 12, fill=(26, 34, 31, int(255 * pa)), outline=GREEN + (int(200 * pa),), w=2)
                d.rounded_rectangle((cx + 14, 1066, cx + cw - 14, 1080), radius=6, fill=GREEN + (int(255 * pa),))
        # deployed badge
        a = fade(t, 9.2)
        if a > 0:
            rr(d, (bx0 + 110, 1240, bx1 - 110, 1300), 30, fill=GREEN + (int(255 * a),))
            bb = d.textbbox((0, 0), "DEPLOYED", font=f_small)
            d.text((W - 260 - (bb[2] - bb[0]) / 2 - bb[0], 1252), "DEPLOYED", font=f_small, fill=(12, 17, 16, int(255 * a)))

    # ---- bottom status ----
    if t < 12:
        st = "CODING" if t < 7.4 else "DEPLOYING"
        col = GREEN if t < 7.4 else YEL
        a = fade(t, 2.4)
        if a > 0:
            blink = "" if int(t * 2) % 2 == 0 else " "
            ov, _ = txt_center(d, 0, "> " + st + " ..." + blink, f_mid, col, int(255 * a))
            im.alpha_composite(ov, (0, 1420))
    # progress bar
    pw = int(W * clamp(t / 12))
    d.rectangle((0, H - 26, pw, H - 14), fill=GREEN)

    # ---- finale ----
    fa = fade(t, 12.0, 0.8)
    if fa > 0:
        ov = Image.new("RGBA", (W, H), (6, 9, 8, int(200 * fa)))
        im.alpha_composite(ov)
        d = ImageDraw.Draw(im, "RGBA")
        ov2, _ = txt_center(d, 0, "atikur.cyou", f_big, GREEN, int(255 * fa))
        im.alpha_composite(ov2, (0, 700))
        ov3, _ = txt_center(d, 0, "LIVE NOW", f_title, TEXT, int(255 * fa))
        im.alpha_composite(ov3, (0, 830))
        ov4, _ = txt_center(d, 0, "Built by Atikur Rahman", f_sub, MUTED, int(255 * fa))
        im.alpha_composite(ov4, (0, 950))
        # cta button
        bw, bh = 560, 110
        rr(d, ((W - bw)//2, 1080, (W + bw)//2, 1080 + bh), 55, fill=GREEN + (int(255 * fa),))
        bb = d.textbbox((0, 0), "Visit the site", f_mid)
        d.text(((W - (bb[2]-bb[0]))/2 - bb[0], 1080 + (bh - (bb[3]-bb[1]))/2 - bb[1]), "Visit the site", font=f_mid, fill=(12,17,16,int(255*fa)))

    im.convert("RGB").save(f"{OUT}/f{i:04d}.png")

for i in range(N):
    draw_frame(i)
    if i % 90 == 0: print(i, flush=True)
print("frames done")
