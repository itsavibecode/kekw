"""Generate og.png — 1200x630 social-media share card for KEKWClips.

Run from repo root: python .og-gen.py
Output: og.png (committed) — referenced by og:image / twitter:image meta tags.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 630

# Brand palette (matches index.html :root)
BG       = (10, 10, 11)        # #0a0a0b
PANEL    = (22, 22, 26)        # #16161a
BORDER   = (42, 42, 52)        # #2a2a34
GREEN    = (83, 252, 24)       # #53fc18
ORANGE   = (255, 77, 0)        # #ff4d00
PURPLE   = (168, 85, 247)      # #a855f7
GOLD     = (251, 191, 36)      # #fbbf24
TEXT     = (240, 240, 240)     # #f0f0f0
MUTED    = (136, 136, 160)     # #8888a0

# ── canvas ────────────────────────────────────────────────────────────────────
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Subtle diagonal grid texture in panel color (very faint)
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(grid)
for i in range(-H, W, 40):
    gd.line([(i, 0), (i + H, H)], fill=(255, 255, 255, 6), width=1)
img.paste(grid, (0, 0), grid)

# Top + bottom green accent bars
d.rectangle([(0, 0), (W, 6)], fill=GREEN)
d.rectangle([(0, H - 6), (W, H)], fill=GREEN)

# ── KEKW face on the left with purple glow ────────────────────────────────────
kekw = Image.open("img_kekw.png").convert("RGBA")
FACE = 420
kekw = kekw.resize((FACE, FACE), Image.LANCZOS)

# Build a soft purple glow by blurring a tinted disc
glow = Image.new("RGBA", (FACE + 240, FACE + 240), (0, 0, 0, 0))
gd2 = ImageDraw.Draw(glow)
gd2.ellipse([(60, 60), (FACE + 180, FACE + 180)], fill=(168, 85, 247, 110))
glow = glow.filter(ImageFilter.GaussianBlur(60))

face_x, face_y = 80, (H - FACE) // 2
img.paste(glow, (face_x - 120, face_y - 120), glow)

# Rounded mask for the face itself
mask = Image.new("L", (FACE, FACE), 0)
ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (FACE, FACE)], radius=24, fill=255)
img.paste(kekw, (face_x, face_y), mask)

# Subtle green border around the face
d.rounded_rectangle(
    [(face_x - 2, face_y - 2), (face_x + FACE + 2, face_y + FACE + 2)],
    radius=26, outline=GREEN, width=3,
)

# ── vertical divider ──────────────────────────────────────────────────────────
DIV_X = 560
d.line([(DIV_X, 80), (DIV_X, H - 80)], fill=BORDER, width=2)

# ── right column — wordmark + taglines ────────────────────────────────────────
F_HUGE  = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 138)
F_BETA  = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 36)
F_TAG   = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 34)
F_SUB   = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 22)
F_URL   = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 20)

LX = 610  # left edge of right column
TY = 150  # top of wordmark

# "KEKW" green + "CLIPS" white, single line
kekw_w = d.textlength("KEKW", font=F_HUGE)
d.text((LX, TY), "KEKW", font=F_HUGE, fill=GREEN)
d.text((LX + kekw_w, TY), "CLIPS", font=F_HUGE, fill=TEXT)

# BETA badge to the right of wordmark
total_w = kekw_w + d.textlength("CLIPS", font=F_HUGE)
beta_x = LX + total_w + 14
beta_y = TY + 18
d.rectangle([(beta_x, beta_y), (beta_x + 96, beta_y + 38)], fill=ORANGE)
d.text((beta_x + 12, beta_y + 1), "BETA", font=F_BETA, fill=BG)

# Tagline
d.text((LX, TY + 168), "Kick.com Highlight Monitor", font=F_TAG, fill=TEXT)

# Sub-tagline (mono, dim)
d.text(
    (LX, TY + 222),
    "Real-time KEKW spike detector",
    font=F_SUB, fill=MUTED,
)
d.text(
    (LX, TY + 252),
    "Session stats  ·  Auto-clips  ·  No install",
    font=F_SUB, fill=MUTED,
)

# Bottom URL chip
url = "itsavibecode.github.io/kekw"
url_w = d.textlength(url, font=F_URL)
chip_pad_x, chip_pad_y = 16, 8
chip_x = LX
chip_y = TY + 320
d.rounded_rectangle(
    [
        (chip_x, chip_y),
        (chip_x + url_w + chip_pad_x * 2, chip_y + 22 + chip_pad_y * 2),
    ],
    radius=6, fill=PANEL, outline=GREEN, width=2,
)
d.text((chip_x + chip_pad_x, chip_y + chip_pad_y - 2), url, font=F_URL, fill=GREEN)

img.save("og.png", "PNG", optimize=True)
print(f"og.png written  {W}x{H}")
