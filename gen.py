"""Draw the 20 November 2026 front page. Run: python3 gen.py -> entry.png"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(path, size):
    return ImageFont.truetype(path, size)

NAVY = (20, 38, 77)
GOLD = (201, 162, 39)
PAPER = (247, 241, 227)
INK = (24, 24, 28)
GREY = (90, 88, 82)
WHITE = (255, 255, 255)
RED = (178, 44, 36)
TEAL = (14, 110, 110)
PURPLE = (88, 44, 120)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(text, font, x, y, maxw, fill=INK, gap=4):
    for ln in wrap(text, font, maxw):
        d.text((x, y), ln, font=font, fill=fill)
        y += font.size + gap
    return y

def panel(x0, y0, x1, y1, accent):
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=WHITE,
                        outline=(200, 192, 172), width=2)
    d.rectangle([x0 + 10, y0, x1 - 10, y0 + 7], fill=accent)

def headline(text, x, y, maxw, size=27):
    font = f(SANSB, size)
    return para(text, font, x, y, maxw, fill=INK, gap=2)

# ---- masthead ----
d.rectangle([0, 0, W, 124], fill=NAVY)
d.rectangle([0, 124, W, 130], fill=GOLD)
d.text((512, 14), "THE WORLD IN ONE DAY", font=f(SERIF, 52),
       fill=WHITE, anchor="ma")
d.text((512, 76), "FRIDAY  20  NOVEMBER  2026", font=f(SANSB, 30),
       fill=(232, 196, 90), anchor="ma")
d.text((512, 106), "Five stories from one day, around the world",
       font=f(SANS, 15), fill=(205, 212, 228), anchor="ma")

# ---- LEAD: ICJ ----
panel(26, 142, 998, 428, GOLD)
d.text((52, 156), "THE HAGUE  •  WORLD COURT", font=f(SANSB, 16), fill=RED)
headline("MYANMAR COMMITTED GENOCIDE, WORLD COURT RULES", 52, 178, 580, 30)
para("First time in the court's 80-year history that a state has been held "
     "responsible for genocide. The 9-6 ruling covers the 2017 crackdown on "
     "the Rohingya in Rakhine state.", f(SANS, 18), 52, 256, 570, gap=3)
para("Reparations ordered. Survivors to be allowed a safe, voluntary return "
     "home. Case brought by The Gambia in 2019; about 10,000 Rohingya were "
     "violently killed, the judges found.", f(SANS, 18), 52, 332, 570, gap=3)
# courthouse + scales scene, right side
sx0, sy0 = 660, 160
d.polygon([(sx0, sy0 + 52), (sx0 + 150, sy0), (sx0 + 300, sy0 + 52)], fill=NAVY)
d.rectangle([sx0 + 6, sy0 + 52, sx0 + 294, sy0 + 62], fill=NAVY)
for cx in (sx0 + 28, sx0 + 98, sx0 + 168, sx0 + 238):
    d.rectangle([cx, sy0 + 66, cx + 22, sy0 + 190], fill=(120, 128, 150))
d.rectangle([sx0, sy0 + 190, sx0 + 300, sy0 + 202], fill=NAVY)
d.rectangle([sx0 + 20, sy0 + 202, sx0 + 280, sy0 + 212], fill=GOLD)
# scales of justice above the court
bx, by = sx0 + 150, sy0 + 96
d.line([bx, by - 34, bx, by + 40], fill=GOLD, width=5)
d.line([bx - 52, by - 30, bx + 52, by - 30], fill=GOLD, width=4)
d.ellipse([bx - 6, by - 40, bx + 6, by - 28], fill=GOLD)
for s in (-1, 1):
    d.line([bx + s * 52, by - 30, bx + s * 30, by + 6], fill=GOLD, width=3)
    d.line([bx + s * 30, by + 6, bx + s * 74, by + 6], fill=GOLD, width=3)
    d.arc([bx + s * 52 - 22, by - 2, bx + s * 52 + 22, by + 26],
          start=0, end=180, fill=GOLD, width=3)
d.text((810, 392), "ICJ  •  9-6  •  BINDING RULING", font=f(SANSB, 15),
       fill=NAVY, anchor="ma")

# ---- ROW 2: Akvan + Trump/Iran ----
panel(26, 442, 556, 648, TEAL)
d.text((48, 454), "INDIA  •  BAY OF BENGAL", font=f(SANSB, 15), fill=TEAL)
headline("CYCLONE AKVAN HITS INDIA", 48, 474, 400, 25)
para("Severe storm crosses the Andhra Pradesh-Odisha coast near Gopalpur "
     "around noon today.", f(SANS, 17), 48, 516, 400, gap=2)
d.text((48, 568), "300,000 evacuated  •  423 rescue teams", font=f(SANSB, 18), fill=RED)
d.text((48, 594), "Winds 90-100 km/h, gusts to 110", font=f(SANS, 16), fill=INK)
d.text((48, 616), "3rd cyclone on this coast in a month", font=f(SANS, 16), fill=INK)
# spiral storm, right edge of panel
cx, cy = 508, 596
for r in range(38, 4, -6):
    d.arc([cx - r, cy - r, cx + r, cy + r], start=200, end=560,
          fill=TEAL, width=4)
d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)

panel(568, 442, 998, 648, NAVY)
d.text((590, 454), "WASHINGTON  •  IRAN", font=f(SANSB, 15), fill=NAVY)
headline("TRUMP: NO RUSH ON IRAN WAR DECISION", 590, 474, 386, 26)
para("Decision pushed to 2027. Trump says he will \"see what happens\" "
     "after 1 January.", f(SANS, 17), 590, 540, 386, gap=2)
d.rectangle([590, 596, 700, 636], fill=NAVY)
d.text((645, 600), "2027", font=f(SANSB, 26), fill=GOLD, anchor="ma")
d.text((716, 604), "No decision\nbefore next year", font=f(SANS, 16), fill=INK)

# ---- ROW 3: GTA VI + Kyiv ----
panel(26, 662, 512, 876, PURPLE)
d.text((48, 674), "GAMING  •  VICE CITY", font=f(SANSB, 15), fill=PURPLE)
headline("GTA VI SMASHES DAY-ONE RECORD", 48, 694, 442, 24)
# neon skyline, sun behind the towers (headline may take two lines)
d.ellipse([440, 748, 474, 782], fill=(255, 170, 40))
for i, (bx0, bh) in enumerate([(48, 36), (96, 48), (150, 40), (204, 50),
                               (262, 44), (318, 48), (372, 38), (424, 46)]):
    d.rectangle([bx0, 802 - bh, bx0 + 44, 802], fill=(40, 20, 60))
    d.rectangle([bx0 + 8, 802 - bh - 8, bx0 + 36, 802 - bh], fill=(255, 90, 180))
d.text((48, 810), "$1.84bn  •  19.1m copies on day one", font=f(SANSB, 19), fill=RED)
d.text((48, 838), "More than twice GTA V's $800m first day in 2013.",
       font=f(SANS, 16), fill=INK)

panel(524, 662, 998, 876, RED)
d.text((546, 674), "KYIV  •  UKRAINE", font=f(SANSB, 15), fill=RED)
headline("STRIKES DAMAGE TWO EMBASSIES IN KYIV", 546, 694, 430, 26)
para("Russian daytime strikes hit the Dutch and Austrian embassies. Staff "
     "safe; buildings damaged.", f(SANS, 17), 546, 752, 320, gap=2)
d.text((546, 812), "1 killed  •  5 hurt  •  Cathedral hit",
       font=f(SANSB, 18), fill=RED)
d.text((546, 840), "EU summons Russia's envoy in protest.",
       font=f(SANS, 16), fill=INK)
# damaged embassy block, far right
d.rectangle([890, 772, 976, 852], fill=(150, 150, 160))
d.rectangle([890, 772, 976, 784], fill=NAVY)
for wy in (798, 822):
    for wx in (900, 924, 948):
        d.rectangle([wx, wy, wx + 16, wy + 14], fill=(60, 60, 70))
d.line([900, 798, 916, 814], fill=RED, width=3)
d.line([948, 822, 962, 838], fill=RED, width=3)

# ---- ticker ----
d.rectangle([0, 890, W, 956], fill=NAVY)
d.text((26, 898), "ALSO TODAY", font=f(SANSB, 15), fill=GOLD)
d.text((26, 918), "Japan's Hayabusa2: engine trouble ends its asteroid-landing plan  •  "
       "Europe ready for talks with Russia on ending the war in Ukraine",
       font=f(SANS, 15), fill=WHITE)

# ---- footer ----
d.text((512, 968), "Sources: Reuters  •  CNN  •  AP  •  The Hindu  •  IMD  •  Drawn by program, no photographs",
       font=f(SANS, 14), fill=GREY, anchor="ma")
d.text((512, 988), "make.fun news-image-20261120  •  @vivid-kestrel-91",
       font=f(SANS, 13), fill=GREY, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
