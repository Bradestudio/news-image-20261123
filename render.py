#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page (1024x1024 PNG).

Drawn with PIL only. Deterministic: no timestamps, no randomness, fixed
fonts and a layout computed from the text itself, so re-running produces
byte-identical output.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (253, 249, 239)
INK = (26, 26, 26)
RED = (179, 39, 30)
NAVY = (31, 58, 95)
TEAL = (14, 107, 107)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
CARD_LINE = (216, 208, 190)
GLOBE_BLUE = (58, 110, 165)
GLOBE_GREEN = (96, 160, 90)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
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


def draw_center(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text,
              font=fnt, fill=fill)


def fit_headline(draw, text, max_w, start=24):
    """Largest bold size (down to 18) at which the headline fits one line."""
    size = start
    while size > 18 and draw.textlength(text, font=font(SANS_B, size)) > max_w:
        size -= 1
    return font(SANS_B, size)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- outer frame ----
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)

    # ---- masthead ----
    draw_center(d, W // 2, 34, "THE WORLD TODAY", font(SERIF_B, 74), INK)
    d.line([48, 128, W - 48, 128], fill=INK, width=2)
    d.line([48, 133, W - 48, 133], fill=INK, width=1)
    draw_center(d, W // 2, 146, "MONDAY  23  NOVEMBER  2026",
                font(SANS_B, 28), RED)
    d.text((48, 152), "WORLD EDITION", font=font(SANS_B, 17), fill=MUTED)
    d.line([48, 182, W - 48, 182], fill=INK, width=3)

    # ---- hero: COP31 ----
    hx, hy = 48, 200
    d.text((hx, hy), "CLIMATE SUMMIT  •  ANTALYA, TURKEY",
           font=font(SANS_B, 19), fill=RED)
    d.text((hx, hy + 30), "COP31 COLLAPSES",
           font=font(SERIF_B, 62), fill=INK)
    deck = ("Nearly 200 nations leave the UN climate talks with no deal "
            "at all \u2014 the final draft never even mentions "
            "\u201cfossil fuels\u201d. The EU delegation walked out.")
    lines = wrap(d, deck, font(SANS, 23), 600)
    y = hy + 108
    for ln in lines:
        d.text((hx, y), ln, font=font(SANS, 23), fill=INK)
        y += 30
    y += 6
    d.text((hx, y), "\u201cDeeply disappointed.\u201d \u2014 UN chief Ant\u00f3nio Guterres",
           font=font(SANS_B, 21), fill=NAVY)
    y += 36
    tag = "LONGEST COP IN HISTORY"
    tf = font(SANS_B, 18)
    tw = d.textlength(tag, font=tf)
    d.rectangle([hx, y, hx + tw + 22, y + 34], outline=RED, width=2)
    d.text((hx + 11, y + 7), tag, font=tf, fill=RED)
    hero_bottom = y + 34

    # ---- globe visual (right of hero) ----
    cx, cy, r = 862, 322, 98
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GLOBE_BLUE,
              outline=INK, width=3)
    # simple landmasses
    d.ellipse([cx - 78, cy - 62, cx - 18, cy - 6], fill=GLOBE_GREEN)
    d.ellipse([cx - 8, cy + 8, cx + 66, cy + 62], fill=GLOBE_GREEN)
    d.ellipse([cx + 30, cy - 70, cx + 78, cy - 22], fill=GLOBE_GREEN)
    # latitude / longitude arcs
    d.arc([cx - r, cy - 46, cx + r, cy + 46], 0, 360, fill=(255, 255, 255), width=2)
    d.arc([cx - 46, cy - r, cx + 46, cy + r], 0, 360, fill=(255, 255, 255), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=2)
    # red crack across the globe
    crack = [(cx - 88, cy - 30), (cx - 40, cy - 8), (cx - 52, cy + 26),
             (cx - 6, cy + 44), (cx + 22, cy + 18), (cx + 58, cy + 52),
             (cx + 90, cy + 30)]
    d.line(crack, fill=RED, width=6, joint="curve")

    # ---- section divider (placed below the hero block) ----
    div_y = hero_bottom + 14
    d.line([48, div_y, W - 48, div_y], fill=INK, width=2)
    d.text((48, div_y + 10), "MORE WORLD NEWS", font=font(SANS_B, 20), fill=INK)
    d.line([268, div_y + 20, W - 48, div_y + 20], fill=CARD_LINE, width=1)

    # ---- story cards: 2 columns x 3 rows, height fills to footer ----
    stories = [
        ("MIDDLE EAST", RED, "WAR SPREADS AT HORMUZ",
         "25 tankers attacked at the Strait of Hormuz in 7 days; Gulf "
         "oil flows plunge. Houthis hit Riyadh a third day; Trump "
         "signals an Iran strike in 2027."),
        ("EUROPE", NAVY, "WAR SPILLS INTO THE BALTIC",
         "A Russian cargo ship burns off Finland after a Baltic "
         "drone strike; 14 missing after drones hit a "
         "building near Kyiv, Zelensky says."),
        ("UNITED NATIONS", TEAL, "AI WEAPONS TALKS DRAG ON",
         "States in Geneva agree to keep negotiating lethal autonomous "
         "weapons \u2014 with no binding rules. The work continues "
         "until 2028."),
        ("ASIA", RED, "EXAM SCANDAL TOPPLES MINISTER",
         "Education minister Choi Kyo-jin resigns over an AI-assisted "
         "college entrance exam cheating scandal."),
        ("ASIA", NAVY, "FACTORY FIRE IN INDONESIA",
         "A candy factory fire kills 3; dozens of workers are missing "
         "\u2014 reports say 36 to 50 people are still unaccounted for."),
    ]
    gx = 48
    gy = div_y + 44
    footer_y = 978
    cw, gap = 468, 20
    chh = (footer_y - gy - 2 * 12) // 3
    for i, (kicker, color, head, body) in enumerate(stories):
        col, row = i % 2, i // 2
        x = gx + col * (cw + gap)
        y0 = gy + row * (chh + 12)
        d.rectangle([x, y0, x + cw, y0 + chh], fill=CARD,
                    outline=CARD_LINE, width=1)
        d.rectangle([x, y0, x + cw, y0 + 6], fill=color)
        d.text((x + 14, y0 + 14), kicker, font=font(SANS_B, 15), fill=color)
        hf = fit_headline(d, head, cw - 28)
        d.text((x + 14, y0 + 36), head, font=hf, fill=INK)
        blines = wrap(d, body, font(SANS, 18), cw - 28)
        assert len(blines) <= 3, (head, blines)
        yy = y0 + 68
        for ln in blines:
            d.text((x + 14, yy), ln, font=font(SANS, 18), fill=(51, 51, 51))
            yy += 24

    # ---- by the numbers box (last grid cell) ----
    x = gx + 1 * (cw + gap)
    y0 = gy + 2 * (chh + 12)
    d.rectangle([x, y0, x + cw, y0 + chh], fill=NAVY)
    d.text((x + 16, y0 + 12), "BY THE NUMBERS", font=font(SANS_B, 19),
           fill=(255, 214, 90))
    stats = [
        ("25", "tankers attacked in 7 days"),
        ("200", "nations at COP31 \u2014 no deal"),
        ("14", "missing after the Kyiv strike"),
        ("36\u201350", "workers missing in factory fire"),
    ]
    yy = y0 + 42
    for num, label in stats:
        d.text((x + 16, yy), num, font=font(SANS_B, 20), fill=(255, 255, 255))
        d.text((x + 96, yy + 1), label, font=font(SANS, 18),
               fill=(220, 228, 240))
        yy += 26

    # ---- footer ----
    d.text((48, 986), "Sources: UN, Reuters, AP  •  23 November 2026  •  6 stories, one page",
           font=font(SANS, 14), fill=MUTED)

    img.save("entry.png", format="PNG", optimize=True)
    print("saved entry.png", img.size, "hero_bottom", hero_bottom,
          "card_h", chh)


if __name__ == "__main__":
    main()
