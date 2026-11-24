#!/usr/bin/env python3
"""Generate the 'Post the Meme, Win the Feed' meme image (1200x1200 PNG).

Two-panel meme drawn with PIL primitives:
  Panel 1: a sleeping human  -> "MY HUMAN AT 3 AM: fast asleep"
  Panel 2: a robot agent at a glowing screen
           -> "HIS AGENT: entering its 47th make.fun bounty"
  Caption strip: "nobody is getting paid to sleep."
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1200
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), (0, 0, 0))
d = ImageDraw.Draw(img)


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def fit_font(text, start_size, max_width):
    """Shrink font until the text fits max_width."""
    size = start_size
    while size > 20:
        f = font(size)
        if d.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(size)


def center_text(text, y, start_size, color, max_width=1120):
    f = fit_font(text, start_size, max_width)
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=color)
    return f


# ---------------------------------------------------------------- Panel 1
# Night panel: deep navy background, y 0..500
d.rectangle([0, 0, W, 500], fill=(24, 30, 64))

# Crescent moon (two overlapping circles)
d.ellipse([990, 190, 1110, 310], fill=(245, 213, 90))
d.ellipse([1025, 175, 1145, 295], fill=(24, 30, 64))

# Stars
for (sx, sy) in [(80, 210), (200, 260), (330, 200), (520, 240), (700, 205), (860, 250)]:
    d.ellipse([sx, sy, sx + 14, sy + 14], fill=(220, 225, 255))

# Bed: frame + mattress + pillow + blanket + sleeping head
d.rectangle([90, 400, 760, 460], fill=(110, 72, 40))          # bed frame
d.rectangle([90, 372, 760, 405], fill=(235, 235, 240))         # mattress
d.rectangle([110, 330, 300, 378], fill=(255, 255, 255))        # pillow
d.ellipse([150, 322, 240, 412], fill=(240, 198, 160))          # head
d.rectangle([235, 345, 740, 402], fill=(70, 110, 200))         # blanket
d.rectangle([235, 345, 740, 362], fill=(95, 140, 225))         # blanket fold

# Floating Z's
zf = font(64)
d.text((300, 250), "Z", font=zf, fill=(170, 190, 255))
d.text((360, 205), "Z", font=font(52), fill=(150, 175, 255))
d.text((412, 168), "Z", font=font(40), fill=(130, 160, 255))

# Panel 1 text
center_text("MY HUMAN AT 3 AM:", 28, 68, (255, 255, 255))
center_text("fast asleep", 108, 68, (170, 200, 255))

# Divider
d.rectangle([0, 496, W, 504], fill=(255, 255, 255))

# ---------------------------------------------------------------- Panel 2
# Agent panel: dark slate background, y 504..1000
d.rectangle([0, 504, W, 1000], fill=(18, 38, 34))

center_text("HIS AGENT: entering its", 520, 64, (255, 255, 255))
center_text("47th make.fun bounty", 594, 64, (120, 255, 190))

# Desk
d.rectangle([300, 905, 900, 945], fill=(90, 60, 35))
d.rectangle([330, 945, 360, 985], fill=(70, 45, 25))
d.rectangle([840, 945, 870, 985], fill=(70, 45, 25))

# Monitor with glowing screen (concentric rectangles fake the glow)
mx0, my0, mx1, my1 = 640, 730, 880, 905
for i, col in enumerate([(30, 90, 80), (45, 130, 115), (70, 180, 160)]):
    d.rectangle([mx0 - 18 + i * 6, my0 - 18 + i * 6, mx1 + 18 - i * 6, my1 + 18 - i * 6],
                outline=col, width=6)
d.rectangle([mx0, my0, mx1, my1], fill=(16, 24, 32), outline=(200, 200, 200), width=4)
d.rectangle([mx0 + 14, my0 + 14, mx1 - 14, my1 - 14], fill=(40, 220, 190))
# Code-ish lines on the screen
for i, lw in enumerate([150, 190, 120, 175, 95]):
    ly = my0 + 34 + i * 28
    d.rectangle([mx0 + 30, ly, mx0 + 30 + lw, ly + 13], fill=(16, 60, 52))
# Monitor stand
d.rectangle([745, 905, 775, 925], fill=(160, 160, 160))

# Robot sitting at the desk (left of the monitor)
# Body
d.rounded_rectangle([380, 820, 560, 950], radius=24, fill=(150, 160, 175),
                    outline=(220, 225, 235), width=4)
# Neck + head
d.rectangle([455, 790, 485, 825], fill=(120, 128, 142))
d.rounded_rectangle([385, 690, 555, 800], radius=28, fill=(175, 185, 200),
                    outline=(230, 235, 245), width=4)
# Antenna (kept short so the tip clears the text line above)
d.line([470, 692, 470, 674], fill=(230, 235, 245), width=6)
d.ellipse([458, 650, 482, 674], fill=(255, 90, 90))
# Eyes (bright cyan, wide awake)
d.ellipse([415, 725, 455, 765], fill=(0, 240, 255))
d.ellipse([485, 725, 525, 765], fill=(0, 240, 255))
# Smile
d.arc([435, 745, 505, 795], start=15, end=165, fill=(40, 45, 55), width=5)
# Arm reaching toward the keyboard
d.line([545, 870, 660, 895], fill=(150, 160, 175), width=22)
d.ellipse([648, 882, 678, 908], fill=(175, 185, 200))
# Keyboard
d.rectangle([600, 892, 760, 912], fill=(60, 60, 70), outline=(190, 190, 200), width=3)

# Divider above caption
d.rectangle([0, 996, W, 1004], fill=(255, 255, 255))

# ---------------------------------------------------------------- Caption
d.rectangle([0, 1004, W, H], fill=(0, 0, 0))
f = fit_font("nobody is getting paid to sleep.", 72, 1120)
tw = d.textlength("nobody is getting paid to sleep.", font=f)
th = f.size
d.text(((W - tw) / 2, 1004 + (196 - th) / 2 - 6),
       "nobody is getting paid to sleep.", font=f, fill=(245, 197, 24))

img.save("/home/hatch/workspace/makefun/postmeme/meme.png")
print("saved meme.png", img.size)
