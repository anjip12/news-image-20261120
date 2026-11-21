#!/usr/bin/env python3
"""v2: THE WORLD IN ONE DAY — Friday 20 November 2026.
Dense newspaper front page: 8 lead panels + 18 small items = 26 stories.
Deterministic: stdlib + PIL only, no randomness, no time, no network.
Writes entry.png (1024x1024) next to this script."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
W = H = 1024

PAPER = (247, 242, 231)
INK = (22, 34, 66)
INK_SOFT = (52, 58, 74)
RULE = (150, 140, 120)
CARD = (255, 253, 247)
FOOT = (96, 92, 84)

FDIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)

F_TITLE = font("DejaVuSerif-Bold.ttf", 46)
F_DATE = font("DejaVuSerif-Bold.ttf", 21)
F_STAND = font("DejaVuSerif.ttf", 15)
F_KICK = font("DejaVuSans-Bold.ttf", 12)
F_KICK_M = font("DejaVuSans-Bold.ttf", 11)
F_HEAD_BIG = font("DejaVuSerif-Bold.ttf", 21)
F_HEAD_MED = font("DejaVuSerif-Bold.ttf", 18)
F_BODY_BIG = font("DejaVuSans.ttf", 13)
F_BODY_MED = font("DejaVuSans.ttf", 12)
F_GRID_HEAD = font("DejaVuSans-Bold.ttf", 13)
F_GRID_BODY = font("DejaVuSans.ttf", 11)
F_REGION = font("DejaVuSans-Bold.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 11)

def wrap(text, fnt, max_w, draw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def tint(hexcol, bg, f=0.16):
    r = int(hexcol[0] * f + bg[0] * (1 - f))
    g = int(hexcol[1] * f + bg[1] * (1 - f))
    b = int(hexcol[2] * f + bg[2] * (1 - f))
    return (r, g, b)

# ---------------- drawn art motifs (all PIL primitives) ----------------
def art_court(d, box, ac):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    d.polygon([(x0 + 8, y0 + 52), (cx, y0 + 18), (x1 - 8, y0 + 52)], fill=ac)
    d.rectangle([x0 + 8, y0 + 52, x1 - 8, y0 + 60], fill=ac)
    for cxp in (x0 + 26, cx - 5, x1 - 36):
        d.rectangle([cxp, y0 + 64, cxp + 10, y1 - 26], fill=ac)
    d.rectangle([x0 + 8, y1 - 26, x1 - 8, y1 - 18], fill=ac)
    d.rectangle([x0 + 4, y1 - 18, x1 - 4, y1 - 12], fill=ac)

def art_bridge(d, box, ac):
    x0, y0, x1, y1 = box
    d.arc([x0 + 6, y0 + 30, x1 - 6, y1 - 10], 180, 360, fill=ac, width=4)
    for fx in (0.25, 0.5, 0.75):
        px = x0 + int((x1 - x0) * fx)
        d.line([(px, y0 + 42), (px, y1 - 34)], fill=ac, width=3)
    d.rectangle([x0 + 4, y1 - 34, x1 - 4, y1 - 28], fill=ac)
    for i in range(3):
        sx = x1 - 14 - i * 16
        d.line([(sx, y0 + 12 + i * 8), (sx - 18, y0 + 22 + i * 8)], fill=(200, 60, 40), width=3)

def art_storm(d, box, ac):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    for r in (14, 26, 38):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=ac, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=ac)
    for i in range(4):
        rx = x0 + 12 + i * 26
        d.line([(rx, y1 - 30), (rx - 8, y1 - 12)], fill=ac, width=3)

def art_skyline(d, box, ac):
    x0, y0, x1, y1 = box
    base = y1 - 14
    heights = [52, 78, 64, 92, 58, 84, 48]
    bw = (x1 - x0 - 16) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + 8 + i * bw
        d.rectangle([bx, base - hh, bx + bw - 3, base], fill=ac)
        for wy in range(base - hh + 8, base - 6, 12):
            d.rectangle([bx + 3, wy, bx + 6, wy + 4], fill=(255, 220, 90))
    d.rectangle([x0 + 4, base, x1 - 4, base + 4], fill=INK)

def art_globe(d, box, ac):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    r = 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ac, width=4)
    d.ellipse([cx - 16, cy - r, cx + 16, cy + r], outline=ac, width=2)
    d.line([(x0 + 8, cy), (x1 - 8, cy)], fill=ac, width=2)
    d.arc([cx - r, cy - 18, cx + r, cy + 18], 0, 180, fill=ac, width=2)
    d.line([(cx, y1 - 22), (cx + 26, y1 - 8)], fill=(60, 140, 70), width=4)
    d.ellipse([cx + 20, y1 - 16, cx + 34, y1 - 2], fill=(60, 140, 70))

def art_chart(d, box, ac):
    x0, y0, x1, y1 = box
    d.line([(x0 + 10, y0 + 14), (x0 + 10, y1 - 14)], fill=INK, width=3)
    d.line([(x0 + 10, y1 - 14), (x1 - 8, y1 - 14)], fill=INK, width=3)
    pts = [(x0 + 16, y0 + 22), (x0 + 40, y0 + 34), (x0 + 62, y0 + 30),
           (x0 + 86, y0 + 58), (x0 + 108, y0 + 74), (x1 - 12, y0 + 96)]
    d.line(pts, fill=(200, 50, 40), width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=(200, 50, 40))

def art_flags(d, box, ac):
    x0, y0, x1, y1 = box
    ux0, uy0, ux1, uy1 = x0 + 6, y0 + 34, x0 + 62, y0 + 74
    d.rectangle([ux0, uy0, ux1, uy1], fill=(30, 50, 120))
    d.rectangle([ux0, (uy0 + uy1) // 2 - 4, ux1, (uy0 + uy1) // 2 + 4], fill=(255, 255, 255))
    d.rectangle([(ux0 + ux1) // 2 - 4, uy0, (ux0 + ux1) // 2 + 4, uy1], fill=(255, 255, 255))
    d.rectangle([ux0, (uy0 + uy1) // 2 - 2, ux1, (uy0 + uy1) // 2 + 2], fill=(200, 40, 40))
    d.rectangle([(ux0 + ux1) // 2 - 2, uy0, (ux0 + ux1) // 2 + 2, uy1], fill=(200, 40, 40))
    ex0, ey0, ex1, ey1 = x1 - 62, y0 + 34, x1 - 6, y0 + 74
    d.rectangle([ex0, ey0, ex1, ey1], fill=(20, 40, 140))
    ecx, ecy = (ex0 + ex1) // 2, (ey0 + ey1) // 2
    for i in range(8):
        import math
        a = math.pi * 2 * i / 8 - math.pi / 2
        d.ellipse([ecx + int(13 * math.cos(a)) - 2, ecy + int(11 * math.sin(a)) - 2,
                   ecx + int(13 * math.cos(a)) + 2, ecy + int(11 * math.sin(a)) + 2],
                  fill=(255, 210, 60))
    d.line([(ux1 + 2, uy1 - 6), (ex0 - 2, ey1 - 6)], fill=ac, width=3)

def art_calendar(d, box, ac):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 + 10, y0 + 22, x1 - 10, y1 - 12], radius=6,
                        outline=ac, width=3, fill=(255, 255, 255))
    d.rectangle([x0 + 10, y0 + 22, x1 - 10, y0 + 40], fill=ac)
    d.text(((x0 + x1) // 2 - 26, y0 + 52), "2027", font=font("DejaVuSans-Bold.ttf", 26), fill=INK)
    d.line([(x0 + 22, y1 - 26), (x1 - 22, y1 - 26)], fill=RULE, width=2)

ART = {"court": art_court, "bridge": art_bridge, "storm": art_storm,
       "skyline": art_skyline, "globe": art_globe, "chart": art_chart,
       "flags": art_flags, "calendar": art_calendar}

# ---------------- content (verified facts only) ----------------
LEADS_BIG = [
    dict(kicker="THE HAGUE  •  GENOCIDE RULING", accent=(128, 30, 60),
         art="court",
         head="ICJ: MYANMAR COMMITTED GENOCIDE",
         body=["The Hague, 19 Nov — 9–6 ruling: genocide against the Rohingya in 2017; ~10,000 killed.",
               "A first in the court's 80-year history. Myanmar calls it “unfair”; refugees celebrate."]),
    dict(kicker="KYIV  •  WAR IN UKRAINE", accent=(160, 40, 30),
         art="bridge",
         head="KYIV HIT BY 400+ DRONES, 110+ MISSILES",
         body=["One of the war's largest attacks overnight into 20 Nov; three Dnipro bridges hit. 8–9 killed, 28 hurt; power out in 11 regions.",
               "Two Russian missiles crossed into Poland; Tusk: likely “intentional provocation”."]),
]

LEADS_MED = [
    dict(kicker="INDIA  •  CYCLONE AKVAN", accent=(20, 110, 130), art="storm",
         head="AKVAN LANDFALL: NO DEATHS",
         body=["Landfall near Gopalpur, Odisha, 07:30–08:30 IST; winds 70–80 km/h, gusting 90.",
               "372,000 sheltered; 209 mm rain at Patrapur; third cyclone here in 24 days."]),
    dict(kicker="GAMING  •  TAKE-TWO", accent=(110, 40, 150), art="skyline",
         head="GTA VI: $3.79BN DAY ONE — A RECORD",
         body=["Take-Two: biggest entertainment launch in history.",
               "32.5m units sold pre-release; Metacritic score 99."]),
    dict(kicker="CLIMATE  •  COP31 ANTALYA", accent=(30, 120, 70), art="globe",
         head="COP31 ENDS DAY WITH NO DEAL",
         body=["Talks reach their final scheduled day; the latest draft drops fossil fuels and the $120bn-a-year adaptation figure.",
               "Talks expected to run into the weekend."]),
    dict(kicker="MARKETS  •  ASIA", accent=(180, 60, 20), art="chart",
         head="ASIA: WORST WEEK SINCE 2020",
         body=["Taiwan Taiex −6.75% Friday (−17.5% for the week); Kospi −5.7%; Nikkei −4.8%.",
               "SoftBank −14.6%. Even Anthropic's $81bn IPO and Nvidia's record earnings fail to stop the selling."]),
    dict(kicker="BRUSSELS  •  UK–EU", accent=(30, 60, 140), art="flags",
         head="UK–EU RESET DEAL SEALED",
         body=["Brussels summit: easier food trade, youth mobility for 100,000 a year, linked emissions trading from 2028.",
               "Burnham and von der Leyen call it a “win-win”. Tuition fees unresolved."]),
    dict(kicker="WASHINGTON  •  IRAN", accent=(90, 70, 20), art="calendar",
         head="TRUMP PUSHES IRAN DECISION TO 2027",
         body=["“See what happens” after 1 January, he says — no rush on a war decision."]),
]

# (region, headline, ONE short factual line, <= ~52 chars)
GRID = [
    ("EUROPE", "Merz rejects a “new Yalta”",
     "No settlement on Europe's future without Europe."),
    ("EUROPE", "Ukraine strikes back",
     "Druzhba station in Tatarstan hit; 3 launchers hit."),
    ("EUROPE", "Ukrainian drones hit Dorogobuzh",
     "Chemical plant in Russia's Smolensk region hit."),
    ("EUROPE", "Poland asks NATO for more help",
     "Seeks AWACS planes after the breach."),
    ("EUROPE", "Europe ready for Russia talks",
     "Open to talks on ending the war in Ukraine."),
    ("ASIA", "Hayabusa2 landing plan scrapped",
     "Engine trouble forces a change of plan."),
    ("MARKETS", "Anthropic shares slide after IPO",
     "Opened +34%, closed +17%; fell below $90 Friday."),
    ("MARKETS", "Wall Street: S&P −2%, Nasdaq −3.5%",
     "AI sell-off accelerates on Friday."),
    ("MARKETS", "Gold and silver at 1-year lows",
     "Slide as rate-hike expectations rise."),
    ("WORLD", "Panama vows to block a weak COP31 deal",
     "Demands 8 conditions, incl. an oil-production cap."),
    ("WORLD", "UN accuses Syrian forces of abuses",
     "SDF abuses; Syrian attacks may be war crimes."),
    ("WORLD", "Macron, Trump urge Syria ceasefire",
     "Call for immediate implementation in Syria."),
    ("AMERICAS", "Trump summit: few concrete results",
     "Joint statement, no Ukraine breakthrough."),
    ("AMERICAS", "US shutdown risk as Congress leaves",
     "Congress leaves; 11 Dec deadline unresolved."),
    ("AMERICAS", "Senate rejects Iran-war curb",
     "Republicans block bill requiring approval, 19 Nov."),
    ("AMERICAS", "Vance silent on Iran strikes",
     "Declines to say if he would have authorised strikes."),
    ("AMERICAS", "Haiti police kill 34 gang suspects",
     "Intensified anti-gang push, police say."),
    ("WORLD", "EgyptAir flights to Syria resume",
     "Damascus and Aleppo to be served from December."),
]

COLS = [GRID[0:6], GRID[6:12], GRID[12:18]]

# ---------------- render ----------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 12  # outer margin

# masthead
d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK, anchor="ma")
d.text((W // 2, 70), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=(150, 40, 30), anchor="ma")
d.text((W // 2, 96), "26 stories from one day, around the world", font=F_STAND, fill=INK_SOFT, anchor="ma")
d.line([(M, 120), (W - M, 120)], fill=INK, width=3)
d.line([(M, 125), (W - M, 125)], fill=RULE, width=1)

def panel(x0, y0, x1, y1, accent):
    d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD, outline=RULE, width=1)
    d.rectangle([x0 + 2, y0 + 2, x1 - 2, y0 + 5], fill=accent)

def lead_big(item, x0, y0, x1, y1):
    ac = item["accent"]
    panel(x0, y0, x1, y1, ac)
    pad = 12
    art_w = 148
    tx = x0 + pad
    tw = (x1 - art_w - 10) - tx
    ax0, ay0, ax1, ay1 = x1 - art_w, y0 + 10, x1 - 10, y1 - 10
    d.rounded_rectangle([ax0, ay0, ax1, ay1], radius=5, fill=tint(ac, CARD), outline=RULE, width=1)
    ART[item["art"]](d, (ax0, ay0, ax1, ay1), ac)
    y = y0 + 14
    d.text((tx, y), item["kicker"], font=F_KICK, fill=ac)
    y += 22
    lines = wrap(item["head"], F_HEAD_BIG, tw, d)
    y = draw_lines(d, lines, tx, y, F_HEAD_BIG, INK, 26)
    y += 6  # breathing room above body
    for para in item["body"]:
        bl = wrap(para, F_BODY_BIG, tw, d)
        y = draw_lines(d, bl, tx, y, F_BODY_BIG, INK_SOFT, 17)
        y += 5  # gap between paragraphs, never touching a rule

def lead_med(item, x0, y0, x1, y1):
    ac = item["accent"]
    panel(x0, y0, x1, y1, ac)
    pad = 10
    art_w = 84
    ax0, ay0, ax1, ay1 = x0 + pad, y0 + 10, x0 + pad + art_w, y1 - 10
    d.rounded_rectangle([ax0, ay0, ax1, ay1], radius=5, fill=tint(ac, CARD), outline=RULE, width=1)
    ART[item["art"]](d, (ax0, ay0, ax1, ay1), ac)
    tx = ax1 + 10
    tw = x1 - pad - tx
    y = y0 + 12
    d.text((tx, y), item["kicker"], font=F_KICK_M, fill=ac)
    y += 19
    lines = wrap(item["head"], F_HEAD_MED, tw, d)[:2]
    y = draw_lines(d, lines, tx, y, F_HEAD_MED, INK, 22)
    y += 5
    for para in item["body"]:
        bl = wrap(para, F_BODY_MED, tw, d)
        y = draw_lines(d, bl, tx, y, F_BODY_MED, INK_SOFT, 14)
        y += 4

# big leads row (188 tall)
BH = 188
bw = (W - 2 * M - 10) // 2
lead_big(LEADS_BIG[0], M, 134, M + bw, 134 + BH)
lead_big(LEADS_BIG[1], M + bw + 10, 134, W - M, 134 + BH)

# medium leads: 3 rows x 2 cols (128 tall)
my = 134 + BH + 8
mh = 128
for i, item in enumerate(LEADS_MED):
    row, col = divmod(i, 2)
    x0 = M + col * (bw + 10)
    y0 = my + row * (mh + 8)
    lead_med(item, x0, y0, x0 + bw, y0 + mh)

grid_y0 = my + 3 * mh + 2 * 8 + 10
cw = (W - 2 * M - 20) // 3
for ci, col_items in enumerate(COLS):
    cx = M + ci * (cw + 10)
    y = grid_y0
    cur_region = None
    for region, head, line in col_items:
        if region != cur_region:
            d.text((cx, y), region, font=F_REGION, fill=(150, 40, 30))
            y += 15
            d.line([(cx, y), (cx + cw, y)], fill=RULE, width=1)
            y += 6
            cur_region = region
        hl = wrap(head, F_GRID_HEAD, cw, d)[:1]
        y = draw_lines(d, hl, cx, y, F_GRID_HEAD, INK, 16)
        bl = wrap(line, F_GRID_BODY, cw, d)[:1]
        y = draw_lines(d, bl, cx, y, F_GRID_BODY, INK_SOFT, 14)
        y += 4  # clear gap before the next item

# footer
fy = H - 26
d.line([(M, fy - 6), (W - M, fy - 6)], fill=RULE, width=1)
d.text((W // 2, fy + 2), "Sources: Reuters, CNN, AP, BBC, IMD, Carbon Brief, Morningstar — 20 November 2026",
       font=F_FOOT, fill=FOOT, anchor="ma")

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
