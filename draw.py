#!/usr/bin/env python3
"""Draw the news-image-20261126 front page (deterministic, no network).

Variant 1: masthead + ticker + 3 leads + 3x3 card grid + ALSO TODAY + map/DATE CHECK.
Variant 2: masthead + ticker + 1 full-width lead + 3x3 card grid + ALSO TODAY + map/DATE CHECK.
Usage: VARIANT=1 python3 draw.py [out.png]
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (17, 17, 17)
NAVY = (20, 38, 74)
RED = (163, 22, 33)
BLUE = (31, 78, 121)
GOLD = (201, 162, 39)
GREY = (85, 85, 85)
LIGHTGREY = (120, 120, 120)
RULE = (60, 60, 60)
SKY = (186, 220, 235)
CREAM2 = (238, 230, 210)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, text, name, start, max_w):
    size = start
    while size > 8:
        f = F(name, size)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return F(name, 8)


def text_block(d, x, y, lines, font, fill, leading=None):
    if leading is None:
        leading = font.size + 2
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------- illustrations (drawn, no photos) ----------------

def ill_parade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for bx, bw, bh in [(0, 52, 34), (58, 40, 48), (104, 46, 30), (156, 44, 52),
                       (206, 48, 36), (260, 44, 46)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(120, 124, 128))
        for wy in range(y + h - bh + 5, y + h - 4, 9):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(240, 210, 90))
    d.ellipse([x + w // 2 - 52, y + 6, x + w // 2 + 52, y + 52], fill=(200, 40, 50))
    d.ellipse([x + w // 2 - 52, y + 6, x + w // 2 + 52, y + 30], fill=(220, 70, 70))
    d.polygon([(x + w // 2 - 8, y + 52), (x + w // 2 + 8, y + 52),
               (x + w // 2 + 4, y + h - 8), (x + w // 2 - 4, y + h - 8)], fill=(150, 110, 60))
    d.rectangle([x + w // 2 - 14, y + h - 14, x + w // 2 + 14, y + h - 6], fill=(120, 80, 40))
    d.ellipse([x + w - 46, y + 8, x + w - 18, y + 30], fill=(240, 200, 60))
    for cx, cy, c in [(x + 20, y + 14, RED), (x + 90, y + 10, GOLD),
                      (x + w - 70, y + 44, BLUE), (x + 40, y + 40, (40, 140, 80))]:
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=c)


def ill_eu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    import math
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        sx, sy = cx + 34 * math.cos(ang), cy + 26 * math.sin(ang)
        star(d, sx, sy, 6, (255, 210, 0))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(255, 210, 0))


def ill_candle(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 46))
    d.ellipse([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + 44], fill=(255, 180, 60, 90))
    d.ellipse([x + w // 2 - 7, y + 10, x + w // 2 + 7, y + 28], fill=(255, 160, 40))
    d.ellipse([x + w // 2 - 3, y + 16, x + w // 2 + 3, y + 26], fill=(255, 230, 140))
    d.rectangle([x + w // 2 - 9, y + 30, x + w // 2 + 9, y + h - 6], fill=(245, 240, 225))
    d.rectangle([x + w // 2 - 16, y + h - 8, x + w // 2 + 16, y + h - 4], fill=(180, 170, 150))
    for cx in (x + 24, x + w - 24):
        d.ellipse([cx - 2, y + h - 14, cx + 2, y + h - 10], fill=(200, 200, 200))


def ill_tube(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 232))
    cx, cy = x + 52, y + h // 2
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=RED, width=7)
    d.rectangle([cx - 34, cy - 6, cx + 34, cy + 6], fill=NAVY)
    bx = x + w - 128
    d.rounded_rectangle([bx, y + 8, bx + 118, y + h - 10], radius=8, fill=(200, 30, 40))
    for i in range(4):
        d.rectangle([bx + 10 + i * 28, y + 16, bx + 30 + i * 28, y + 32], fill=(190, 220, 235))
    d.ellipse([bx + 18, y + h - 20, bx + 34, y + h - 6], fill=INK)
    d.ellipse([bx + 84, y + h - 20, bx + 100, y + h - 6], fill=INK)


def ill_chess(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 210, 180))
    s = min(w, h) // 8
    ox, oy = x + (w - s * 8) // 2, y + (h - s * 8) // 2
    for r in range(8):
        for c in range(8):
            if (r + c) % 2 == 0:
                d.rectangle([ox + c * s, oy + r * s, ox + (c + 1) * s, oy + (r + 1) * s],
                            fill=(245, 240, 225))
            else:
                d.rectangle([ox + c * s, oy + r * s, ox + (c + 1) * s, oy + (r + 1) * s],
                            fill=(90, 70, 50))
    for cx, col in [(ox + 2 * s, (255, 255, 255)), (ox + 6 * s, (20, 20, 20))]:
        cy = oy + 3 * s
        d.ellipse([cx - s, cy - s, cx + s, cy + s], fill=col, outline=(60, 60, 60))
        d.polygon([(cx - s, cy - s + 2), (cx - s // 2, cy - s - 4), (cx, cy - s + 2),
                   (cx + s // 2, cy - s - 4), (cx + s, cy - s + 2)], fill=col)


def ill_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 205))
    mid = y + h // 2
    pts = [(x + 4, mid)]
    import random
    random.seed(7)
    xx = x + 4
    while xx < x + w - 8:
        xx += random.randint(6, 14)
        pts.append((xx, mid + random.randint(-16, 16)))
    pts.append((x + w - 4, mid))
    d.line(pts, fill=INK, width=2)
    d.ellipse([x + w - 34, mid - 12, x + w - 14, mid + 8], fill=RED)
    d.text((x + w - 31, mid - 9), "4.0", font=F(SANS_B, 11), fill=(255, 255, 255))


def ill_train(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x + 30, y + 12, x + w - 30, y + h - 22], fill=(0, 120, 130))
    d.rounded_rectangle([x + 30, y + 12, x + w - 30, y + 26], radius=6, fill=(0, 90, 100))
    for i in range(5):
        d.rectangle([x + 42 + i * 34, y + 32, x + 66 + i * 34, y + 50], fill=(190, 225, 240))
    d.rectangle([x + 42, y + 56, x + w - 42, y + 62], fill=(255, 210, 0))
    for ry in (y + h - 14, y + h - 6):
        d.line([x, ry, x + w, ry], fill=(90, 90, 90), width=2)
    for tx in range(x + 8, x + w - 8, 22):
        d.line([tx, y + h - 16, tx + 8, y + h - 4], fill=(90, 90, 90), width=2)


def ill_plane(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for cx, cy in [(x + 30, y + 12), (x + w - 40, y + 8), (x + w - 90, y + 40)]:
        d.ellipse([cx - 14, cy - 5, cx + 14, cy + 5], fill=(255, 255, 255))
    cx, cy = x + w // 2, y + h // 2 + 4
    d.ellipse([cx - 70, cy - 10, cx + 70, cy + 10], fill=(200, 40, 50))
    d.polygon([(cx - 10, cy - 8), (cx + 30, cy - 34), (cx + 52, cy - 34), (cx + 26, cy - 6)],
              fill=(170, 30, 40))
    d.polygon([(cx + 52, cy - 6), (cx + 78, cy - 28), (cx + 84, cy - 20), (cx + 70, cy + 2)],
              fill=(170, 30, 40))
    for i in range(4):
        d.ellipse([cx - 52 + i * 26, cy - 6, cx - 42 + i * 26, cy + 2], fill=(255, 255, 255))


def ill_football(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 140, 70))
    d.rectangle([x + 8, y + 6, x + w - 8, y + h - 6], outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y + 6, x + w // 2, y + h - 6], fill=(255, 255, 255), width=2)
    d.ellipse([x + w // 2 - 16, y + h // 2 - 16, x + w // 2 + 16, y + h // 2 + 16],
              outline=(255, 255, 255), width=2)
    bx, by = x + w - 42, y + h // 2
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 255, 255), outline=INK)
    d.polygon([(bx, by - 6), (bx + 6, by - 2), (bx + 4, by + 5), (bx - 4, by + 5), (bx - 6, by - 2)],
              fill=INK)


def ill_tennis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 90, 160))
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], outline=(255, 255, 255), width=2)
    d.line([x + 10, y + h // 2, x + w - 10, y + h // 2], fill=(255, 255, 255), width=2)
    d.ellipse([x + w // 2 - 14, y + h // 2 - 14, x + w // 2 + 14, y + h // 2 + 14],
              fill=(220, 240, 60), outline=INK)
    d.arc([x + w // 2 - 14, y + h // 2 - 14, x + w // 2 + 14, y + h // 2 + 14],
          start=300, end=60, fill=INK, width=2)


def ill_boxing(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 40))
    for gx, col in [(x + w // 2 - 52, (200, 40, 50)), (x + w // 2 + 8, (40, 90, 200))]:
        d.rounded_rectangle([gx, y + 8, gx + 44, y + h - 14], radius=12, fill=col)
        d.rectangle([gx + 8, y + h - 22, gx + 36, y + h - 10], fill=(240, 230, 210))
    star(d, x + w // 2, y + h // 2, 12, GOLD)
    d.text((x + w // 2 - 5, y + h // 2 - 6), "V", font=F(SANS_B, 11), fill=INK)


def ill_festival(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 235, 210))
    cols = [RED, GOLD, BLUE, (40, 140, 80), (180, 80, 160)]
    for i in range(9):
        fx = x + 6 + i * (w - 12) // 9
        d.polygon([(fx, y + 4), (fx + 14, y + 4), (fx + 7, y + 20)], fill=cols[i % 5])
    d.rectangle([x + 20, y + h - 34, x + w - 20, y + h - 6], fill=NAVY)
    for i in range(5):
        d.rectangle([x + 30 + i * 26, y + h - 28, x + 48 + i * 26, y + h - 12],
                    fill=(240, 210, 90))
    d.ellipse([x + w - 40, y + 26, x + w - 18, y + 48], fill=GOLD)


def ill_tree(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 40, 70))
    cx = x + w // 2
    for i, (tw, ty) in enumerate([(56, 10), (72, 22), (88, 34)]):
        d.polygon([(cx - tw // 2, ty + y), (cx + tw // 2, ty + y), (cx, ty + y - 22)],
                  fill=(30, 130, 60))
    star(d, cx, y + 8, 8, GOLD)
    for ox, oy in [(cx - 14, y + 22), (cx + 16, y + 30), (cx - 6, y + 40), (cx + 10, y + 46)]:
        d.ellipse([ox - 3, oy - 3, ox + 3, oy + 3], fill=RED)
    d.rectangle([cx - 6, y + h - 12, cx + 6, y + h - 4], fill=(120, 80, 40))
    for bx in (x + 12, x + w - 34):
        d.rectangle([bx, y + h - 26, bx + 22, y + h - 6], fill=(60, 60, 90))
        for wy in range(y + h - 22, y + h - 8, 7):
            d.rectangle([bx + 4, wy, bx + 8, wy + 4], fill=(240, 210, 90))
            d.rectangle([bx + 13, wy, bx + 17, wy + 4], fill=(240, 210, 90))


def ill_nkorea(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 205, 210))
    d.polygon([(x, y + h), (x + w // 3, y + 18), (x + 2 * w // 3, y + h)], fill=(120, 130, 140))
    d.rectangle([x + w // 2 - 26, y + 16, x + w // 2 + 26, y + h - 6], fill=(150, 150, 155))
    for wy in range(y + 22, y + h - 10, 10):
        for wx in range(x + w // 2 - 20, x + w // 2 + 20, 12):
            d.rectangle([wx, wy, wx + 6, wy + 5], fill=(240, 210, 90))
    d.line([x + w // 2, y + 6, x + w // 2, y + 16], fill=INK, width=2)
    d.polygon([(x + w // 2, y + 4), (x + w // 2 + 22, y + 8), (x + w // 2, y + 12)], fill=RED)


ILL = {
    "parade": ill_parade, "eu": ill_eu, "candle": ill_candle, "tube": ill_tube,
    "chess": ill_chess, "quake": ill_quake, "train": ill_train, "plane": ill_plane,
    "football": ill_football, "tennis": ill_tennis, "boxing": ill_boxing,
    "festival": ill_festival, "tree": ill_tree, "nkorea": ill_nkorea,
}

# ---------------- story data (all verified 26 Nov 2026) ----------------

LEADS = [
    dict(tag="N. AMERICA — CULTURE", ill="parade",
         head="THANKSGIVING TURNS 100",
         body="The 100th Macy's parade marches on as 81.5m travel and a bomb cyclone lashes the East Coast.",
         src="AP · NBC"),
    dict(tag="SOUTH ASIA — REMEMBRANCE", ill="candle",
         head="INDIA MARKS 18 YEARS SINCE 26/11",
         body="Tributes for the 166 killed in the 2008 Mumbai attacks, on Constitution Day.",
         src="AIR News"),
    dict(tag="EUROPE — TRANSPORT", ill="tube",
         head="LONDON TUBE STOPS AS DRIVERS WALK OUT",
         body="No Piccadilly or Circle line all day in the first of eight strikes to February.",
         src="The Times"),
]

CARDS = [
    dict(tag="EUROPE — POLITICS", ill="eu",
         head="EU SUMMIT OPENS ON €45BN UKRAINE LOAN",
         body="Brussels hosts two days of talks on Kyiv's 2027 funding; Kyiv repays only once Russia pays.",
         src="European Council"),
    dict(tag="EUROPE — SPORT", ill="chess",
         head="GUKESH v SINDAROV: GAME 3 IN GENEVA",
         body="Title match 1–1 after two draws; the champion has White at 15:00 CET.",
         src="ChessBase"),
    dict(tag="SE ASIA — DISASTER", ill="quake",
         head="M4.0 QUAKE OFF LABUAN, INDONESIA",
         body="A magnitude 4.0 tremor struck near Labuan at 01:29 WIB; no damage reported.",
         src="EMSC"),
    dict(tag="EAST ASIA — TRANSPORT", ill="train",
         head="KOREA'S RAIL SLOWS AS KORAIL STAFF ACT",
         body="Work-to-rule begins at 09:00 and runs to 4 Dec, delayed by a derailment.",
         src="Yonhap"),
    dict(tag="OCEANIA — TRANSPORT", ill="plane",
         head="VIRGIN AUSTRALIA HIT BY CREW STRIKE",
         body="Four-hour stoppages in Brisbane, Sydney and Melbourne; flights to run.",
         src="CBT Travel"),
    dict(tag="EUROPE — SPORT", ill="football",
         head="EUROPA LEAGUE: 17 TIES ON MATCHDAY 5",
         body="Milan visit Olympiacos, Juventus host Omonia, Palace face Real Sociedad.",
         src="UEFA"),
    dict(tag="EAST ASIA — SPORT", ill="boxing",
         head="TOKYO: TWO WORLD TITLES ON THE LINE",
         body="Yabuki defends his IBF flyweight crown and Ishii his WBA belt tonight.",
         src="The Ring"),
    dict(tag="EAST ASIA — CULTURE", ill="festival",
         head="SEOUL DESIGN FESTIVAL OPENS AT COEX",
         body="The 25th festival runs 26–29 Nov with designers from across Asia.",
         src="Hip in Korea"),
    dict(tag="EAST ASIA — POLITICS", ill="nkorea",
         head="N. KOREA ORDERS SWISS OFFICE SHUT",
         body="Pyongyang tells Switzerland to close its newly opened office in the capital.",
         src="Yonhap"),
]

ALSO = [
    ("US markets shut for Thanksgiving", "; short session Friday. (Reuters)"),
    ("Korea court rules on Yoon perjury case", ", 10:15 KST. (News1)"),
    ("Fog in the north, rain in the south", ", IMD warns. (IMD)"),
    ("Palm Beach ferries stop", " as workers walk out. (Medianet)"),
    ("Small-business complaints jump 21%", " to 5,644. (AFCA)"),
    ("M4.8 quake off Hicks Bay", "; M3.5 near Mangapapa. (USGS)"),
    ("Sooryavanshi, 15, smashes record 204", " off 53. (BCCI)"),
    ("IPL 2027 auction draws 1,220", " registrations. (IPL)"),
    ("IITs to add 6,000 tech seats", " from 2027. (AIR News)"),
    ("Flipkart chief to step down", " in December. (Reuters)"),
    ("Houthis report deaths", " after Saudi strikes. (AP)"),
    ("Road crash kills 11", " in Ras Al Khaimah. (WAM)"),
    ("Hasina seeks return to Bangladesh", " on 16 Dec. (Dhaka Tribune)"),
    ("Davis Cup: Britain v Germany", " Zverev leads at 10:00 CET. (Davis Cup)"),
]

DATE_CHECK = ("DATE CHECK — These were checked and left out as not 26 Nov news: "
              "Trump tariffs (25 Nov) · Cairo tanker fire (25 Nov) · Ras Tanura claim (25 Nov) · "
              "Shenzhou-24 (25 Nov) · Bangladesh wage rise (25 Nov) · Colombia rescue (25 Nov) · "
              "Solomon treaty (25 Nov) · Nepal quake (24 Nov) · Gaza strike (25 Nov).")


def draw_header(d):
    # top bar
    d.rectangle([0, 0, W, 26], fill=NAVY)
    f = F(SANS_B, 13)
    t = "26 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED THU 26 NOV 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 5), t, font=f, fill=(255, 255, 255))
    # masthead
    f = fit_font(d, "THE WORLD IN ONE DAY", SERIF_B, 56, 690)
    d.text((18, 34), "THE WORLD IN ONE DAY", font=f, fill=INK)
    f2 = F(SANS_B, 22)
    d.text((W - 18 - d.textlength("THURSDAY", font=f2), 36), "THURSDAY", font=f2, fill=RED)
    f3 = F(SANS_B, 22)
    d.text((W - 18 - d.textlength("26 NOVEMBER 2026", font=f3), 62), "26 NOVEMBER 2026",
           font=f3, fill=NAVY)
    d.rectangle([0, 100, W, 103], fill=INK)
    # ticker
    f = F(SANS_B, 16)
    d.text((18, 110), "Thanksgiving turns 100   •   India marks 18 years since 26/11   •   London's Tube stops",
           font=f, fill=RED)
    d.rectangle([0, 132, W, 133], fill=RULE)
    # region chips
    chips = [("N. AMERICA", "2", RED), ("EUROPE", "5", NAVY), ("EAST ASIA", "5", BLUE),
             ("SOUTH ASIA", "7", (120, 60, 0)), ("SE ASIA", "1", (40, 140, 80)),
             ("OCEANIA", "4", (0, 120, 130)), ("MIDDLE EAST", "2", (140, 90, 160))]
    x = 18
    f = F(SANS_B, 12)
    for name, num, col in chips:
        t = f"{name} {num}"
        d.text((x, 139), t, font=f, fill=col)
        x += d.textlength(t, font=f) + 22
    # schedule strip (auto-shrink so the last entry is never cut at the edge)
    d.rectangle([0, 158, W, 176], fill=(222, 230, 238))
    sched = ["01:29 WIB  Labuan quake", "09:00 KST  Korail begins", "10:15 KST  Yoon ruling",
             "15:00 CET  Chess Game 3", "18:45 CET  Europa League", "20:20 ET  Chiefs–Bills"]
    t = "    ·    ".join(sched)
    f = F(SANS, 12)
    while d.textlength(t, font=f) > W - 36 and f.size > 9:
        f = F(SANS, f.size - 1)
    d.text((18, 162), t, font=f, fill=NAVY)


def draw_lead(d, x, y, w, h, lead):
    ILL[lead["ill"]](d, x, y, w, 62)
    yy = y + 66
    f = F(SANS_B, 11)
    d.text((x, yy), lead["tag"], font=f, fill=RED)
    yy += 13
    f = F(SERIF_B, 19)
    lines = wrap(d, lead["head"], f, w)
    yy = text_block(d, x, yy, lines[:2], f, INK, leading=f.size + 3)
    yy += 1
    f = F(SANS, 12)
    lines = wrap(d, lead["body"], f, w)
    text_block(d, x, yy, lines[:2], f, (40, 40, 40), leading=14)


def draw_card(d, x, y, w, h, card):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    ILL[card["ill"]](d, x + 1, y + 1, w - 2, 62)
    yy = y + 67
    f = F(SANS_B, 10)
    d.text((x + 6, yy), card["tag"], font=f, fill=RED)
    yy += 13
    f = F(SERIF_B, 17)
    lines = wrap(d, card["head"], f, w - 12)
    if len(lines) > 2:
        f = F(SERIF_B, 15)
        lines = wrap(d, card["head"], f, w - 12)
    yy = text_block(d, x + 6, yy, lines[:2], f, INK, leading=f.size + 2)
    f = F(SANS, 12)
    lines = wrap(d, card["body"], f, w - 12)
    text_block(d, x + 6, yy + 1, lines[:2], f, (40, 40, 40), leading=14)


def draw_also(d, y, h):
    d.rectangle([0, y, W, y + 20], fill=NAVY)
    f = F(SANS_B, 13)
    d.text((18, y + 3), "ALSO TODAY — 14 MORE STORIES", font=f, fill=(255, 255, 255))
    yy = y + 25
    f1 = F(SANS_B, 11)
    f2 = F(SANS, 11)
    col_w = (W - 36) // 2
    left = ALSO[:7]
    right = ALSO[7:]
    for col_i, items in enumerate((left, right)):
        xx = 18 + col_i * (col_w + 4)
        cy = yy
        for bold, rest in items:
            # normalize the bold/plain join: exactly one space between the
            # bold lead and the plain tail (unless the tail starts with
            # punctuation that attaches directly, like "," or ";").
            if rest[:1] in (",", ";", " "):
                full = bold + rest
            else:
                full = bold + " " + rest
            prefix = "• " + bold
            lines = wrap(d, "• " + full, f2, col_w)
            first = lines[0]
            d.text((xx, cy), prefix, font=f1, fill=INK)
            bw = d.textlength(prefix, font=f1)
            rem = first[len(prefix):]
            # safety net only: prepend a space when the tail starts with a
            # word character (a leading space or punctuation is already
            # correct as-is — never put a space before "," or ";").
            if rem and rem[0].isalnum():
                rem = " " + rem
            d.text((xx + bw, cy), rem, font=f2, fill=(40, 40, 40))
            cy += 13
            for ln in lines[1:]:
                d.text((xx, cy), ln, font=f2, fill=(40, 40, 40))
                cy += 13
    return cy


def draw_bottom(d, y, h):
    # world map (left) + date check (right)
    mx, my, mw, mh = 10, y, 500, h
    d.rectangle([mx, my, mx + mw, my + mh], fill=(205, 225, 235))
    d.text((mx + 8, my + 4), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=NAVY)
    # rough continents (fit above the two footer lines)
    land = (238, 228, 200)
    d.polygon([(mx + 30, my + 26), (mx + 90, my + 20), (mx + 110, my + 38), (mx + 70, my + 50),
               (mx + 40, my + 46)], fill=land)  # N America
    d.polygon([(mx + 60, my + 52), (mx + 95, my + 50), (mx + 105, my + 60), (mx + 70, my + 62)],
              fill=land)  # S America
    d.polygon([(mx + 200, my + 22), (mx + 250, my + 18), (mx + 270, my + 34), (mx + 230, my + 44),
               (mx + 205, my + 38)], fill=land)  # Europe
    d.polygon([(mx + 210, my + 46), (mx + 260, my + 44), (mx + 280, my + 58), (mx + 240, my + 62),
               (mx + 215, my + 56)], fill=land)  # Africa
    d.polygon([(mx + 290, my + 20), (mx + 420, my + 16), (mx + 460, my + 40), (mx + 400, my + 54),
               (mx + 310, my + 48)], fill=land)  # Asia
    d.polygon([(mx + 400, my + 58), (mx + 450, my + 54), (mx + 460, my + 62), (mx + 410, my + 64)],
              fill=land)  # Oceania
    # (name, px, py, label anchor): "right" (default), "left", or "below".
    # Anchors are chosen so no two labels overlap (SEOUL/TOKYO, LABUAN/
    # HICKS BAY/SYDNEY all collided with plain right-side labels).
    pins = [("NEW YORK", 78, 32, "right"), ("LONDON", 218, 26, "right"),
            ("GENEVA", 236, 34, "right"), ("MUMBAI", 330, 44, "right"),
            ("SEOUL", 415, 32, "left"), ("TOKYO", 438, 28, "right"),
            ("LABUAN", 385, 50, "right"), ("SYDNEY", 432, 52, "right"),
            ("HICKS BAY", 462, 58, "below")]
    f = F(SANS_B, 9)
    for name, px, py, anchor in pins:
        d.ellipse([mx + px - 3, my + py - 3, mx + px + 3, my + py + 3], fill=RED)
        tw = d.textlength(name, font=f)
        if anchor == "left":
            lx, ly = mx + px - 5 - tw, my + py - 5
        elif anchor == "below":
            lx, ly = mx + px - 5 - tw, my + py + 8
        else:
            lx, ly = mx + px + 5, my + py - 5
            if lx + tw > mx + mw - 4:
                lx = mx + px - 5 - tw
        d.text((lx, ly), name, font=f, fill=INK)
    d.text((mx + 8, my + mh - 26),
           "Sources: Reuters, AP, Yonhap, UEFA, EMSC, USGS, AFCA, The Times, News1, IMD.",
           font=F(SANS, 9), fill=GREY)
    d.text((mx + 8, my + mh - 14),
           "Every story above happened or was first reported on Thu 26 Nov 2026.",
           font=F(SANS_B, 9), fill=NAVY)
    # date check (right)
    bx = 522
    d.rectangle([bx, y, W - 10, y + h], outline=RED, width=2)
    d.text((bx + 8, y + 5), "DATE CHECK", font=F(SANS_B, 12), fill=RED)
    f = F(SANS, 10)
    lines = wrap(d, DATE_CHECK, f, W - 10 - bx - 16)
    text_block(d, bx + 8, y + 22, lines, f, (40, 40, 40), leading=11.5)


def build(variant):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    if variant == 1:
        # three lead cards
        for i, lead in enumerate(LEADS):
            draw_lead(d, 11 + i * 336, 182, 330, 156, lead)
        d.rectangle([0, 344, W, 345], fill=INK)
        # 3 rows x 3 cols
        cw, ch, gap = 330, 146, 6
        x0, y0 = 8, 350
        for i, card in enumerate(CARDS):
            r, c = divmod(i, 3)
            draw_card(d, x0 + c * (cw + gap), y0 + r * (ch + gap), cw, ch, card)
        draw_also(d, 806, 0)
        draw_bottom(d, 928, 88)
    else:
        # variant 2: full-width Thanksgiving lead + 3x3 grid
        lead = LEADS[0]
        ILL[lead["ill"]](d, 14, 182, 420, 150)
        f = F(SANS_B, 11)
        d.text((448, 186), lead["tag"], font=f, fill=RED)
        f = F(SERIF_B, 34)
        lines = wrap(d, "THANKSGIVING TURNS 100", f, 560)
        yy = text_block(d, 448, 204, lines, f, INK, leading=38)
        f = F(SANS, 15)
        lines = wrap(d, "The 100th Macy's parade marches on as 81.5m travel for the holiday — "
                        "and a bomb cyclone lashes the East Coast. US markets shut for the day.",
                     f, 560)
        text_block(d, 448, yy + 6, lines[:3], f, (40, 40, 40), leading=19)
        d.rectangle([0, 340, W, 341], fill=INK)
        grid = [dict(LEADS[1]), dict(LEADS[2])] + CARDS[:7]
        cw, ch, gap = 330, 146, 6
        x0, y0 = 8, 348
        for i, card in enumerate(grid):
            r, c = divmod(i, 3)
            draw_card(d, x0 + c * (cw + gap), y0 + r * (ch + gap), cw, ch, card)
        draw_also(d, 804, 0)
        draw_bottom(d, 928, 88)
    return img


if __name__ == "__main__":
    variant = int(os.environ.get("VARIANT", "1"))
    out = sys.argv[1] if len(sys.argv) > 1 else f"/tmp/news26-v{variant}.png"
    img = build(variant)
    img.save(out, optimize=True)
    print(out, img.size, os.path.getsize(out), "bytes")
