# -*- coding: utf-8 -*-
"""Draws the 12 synthetic stimuli for the multimodal items. Deterministic; no external assets."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "images")
os.makedirs(OUT, exist_ok=True)
S = 448
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F = lambda size, bold=True: ImageFont.truetype(BOLD if bold else REG, size)
INK, GRID = "#1a1a1a", "#d9d9d9"


def centred(d, xy, text, font, fill=INK):
    box = d.textbbox((0, 0), text, font=font)
    d.text((xy[0] - (box[2] - box[0]) / 2 - box[0], xy[1] - (box[3] - box[1]) / 2 - box[1]), text, font=font, fill=fill)


def chart(name, draw):
    fig, ax = plt.subplots(figsize=(4.48, 4.48), dpi=100)
    draw(ax)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=100)
    plt.close(fig)


def mm01(ax):  # quarterly sales
    q, v = ["Q1", "Q2", "Q3", "Q4"], [120, 135, 150, 95]
    bars = ax.bar(q, v, color="#2a78d6", width=0.62)
    for b, val in zip(bars, v):
        ax.text(b.get_x() + b.get_width() / 2, val + 3, str(val), ha="center", fontsize=15, fontweight="bold", color=INK)
    ax.set_ylim(0, 175); ax.set_title("Quarterly sales (lakh rupees)", fontsize=14, fontweight="bold")
    ax.tick_params(labelsize=13); ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)


def mm02(ax):  # advertising spend vs sales, six stores
    pts = {"A": (0.9, 12), "B": (1.5, 27), "C": (2.3, 16), "D": (2.9, 33), "E": (3.7, 22), "F": (8.6, 92)}
    for k, (x, y) in pts.items():
        ax.scatter([x], [y], s=110, color="#2a78d6", zorder=3)
        ax.text(x + 0.22, y + 2, k, fontsize=15, fontweight="bold", color=INK)
    ax.set_xlim(0, 10); ax.set_ylim(0, 100)
    ax.set_xlabel("Advertising spend (lakh rupees)", fontsize=12); ax.set_ylabel("Monthly sales (lakh rupees)", fontsize=12)
    ax.set_title("Stores A to F", fontsize=14, fontweight="bold"); ax.grid(True, color=GRID); ax.set_axisbelow(True)
    ax.tick_params(labelsize=11)


def mm08(ax):  # lunch survey
    k, v = ["A", "B", "C"], [45, 30, 25]
    bars = ax.bar(k, v, color="#2a78d6", width=0.6)
    for b, val in zip(bars, v):
        ax.text(b.get_x() + b.get_width() / 2, val + 1.2, f"{val}%", ha="center", fontsize=16, fontweight="bold", color=INK)
    ax.set_ylim(0, 55); ax.set_title("Preferred lunch option (% of staff)", fontsize=13, fontweight="bold")
    ax.tick_params(labelsize=14); ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)


def canvas(bg="white"):
    im = Image.new("RGB", (S, S), bg)
    return im, ImageDraw.Draw(im)


def mm03():  # wet-floor sign in a corridor
    im, d = canvas("#eef1f4")
    d.polygon([(0, 448), (448, 448), (300, 250), (148, 250)], fill="#c9d1d9")       # floor
    d.rectangle([148, 60, 300, 250], fill="#f7f8fa", outline="#9aa4ae", width=2)      # end wall
    d.line([(0, 0), (148, 60)], fill="#9aa4ae", width=2); d.line([(448, 0), (300, 60)], fill="#9aa4ae", width=2)
    d.polygon([(224, 150), (120, 400), (328, 400)], fill="#ffd400", outline=INK)      # A-frame sign
    centred(d, (224, 276), "CAUTION", F(19)); centred(d, (224, 318), "WET", F(38)); centred(d, (224, 366), "FLOOR", F(38))
    im.save(os.path.join(OUT, "MM-03.png"))


def mm04():  # exam notice on a door
    im, d = canvas("#e7e2d8")
    d.rectangle([70, 20, 378, 448], fill="#8a5a3a", outline="#4a2f1d", width=4)
    d.ellipse([336, 240, 362, 266], fill="#d9b45a", outline=INK)
    d.rectangle([98, 110, 350, 330], fill="white", outline=INK, width=3)
    centred(d, (224, 160), "QUIET", F(46), "#b00020"); centred(d, (224, 212), "PLEASE", F(40), "#b00020")
    d.line([(118, 246), (330, 246)], fill=INK, width=2)
    centred(d, (224, 276), "EXAM IN", F(30)); centred(d, (224, 308), "PROGRESS", F(30))
    im.save(os.path.join(OUT, "MM-04.png"))


def mm05():  # departures board
    im, d = canvas("#101418")
    centred(d, (224, 34), "DEPARTURES", F(30), "#ffd400")
    d.text((14, 74), "TIME", font=F(15), fill="#9aa4ae"); d.text((92, 74), "TO", font=F(15), fill="#9aa4ae")
    d.text((238, 74), "PLAT", font=F(15), fill="#9aa4ae"); d.text((300, 74), "STATUS", font=F(15), fill="#9aa4ae")
    rows = [("14:05", "NEW DELHI", "2", "DELAYED", "40 MIN", "#ff5a4d"),
            ("14:20", "MUMBAI", "3", "ON TIME", "", "#5fd16a"),
            ("14:35", "KOLKATA", "1", "ON TIME", "", "#5fd16a")]
    y = 112
    for t, to, p, st, st2, col in rows:
        d.rectangle([8, y - 8, 440, y + 86], outline="#2a3138", width=2)
        d.text((14, y + 22), t, font=F(22), fill="white"); d.text((92, y + 22), to, font=F(22), fill="white")
        d.text((252, y + 22), p, font=F(24), fill="white")
        d.text((300, y + (8 if st2 else 22)), st, font=F(22), fill=col)
        if st2:
            d.text((300, y + 40), st2, font=F(22), fill=col)
        y += 106
    im.save(os.path.join(OUT, "MM-05.png"))


def mm06():  # room booking schedule
    im, d = canvas("white")
    centred(d, (224, 30), "MEETING ROOM A", F(26)); centred(d, (224, 62), "Tuesday", F(20, False))
    rows = [("9 - 10", "FREE", None), ("10 - 12", "BOOKED", "Finance"), ("12 - 2", "FREE", None),
            ("2 - 4", "FREE", None), ("4 - 5", "BOOKED", "HR")]
    y = 92
    for t, s, who in rows:
        col = "#fbd5d0" if s == "BOOKED" else "#d6f0d8"
        d.rectangle([20, y, 428, y + 62], fill=col, outline=INK, width=2)
        d.text((34, y + 17), t, font=F(24), fill=INK)
        d.text((170, y + 17), s + (": " + who if who else ""), font=F(24), fill="#8a1c12" if s == "BOOKED" else "#14532d")
        y += 68
    im.save(os.path.join(OUT, "MM-06.png"))


def mm07():  # two power banks
    im, d = canvas("white")
    for x0, label, pct, col in [(40, "A", 5, "#d03b2f"), (250, "B", 80, "#2e9e44")]:
        d.rounded_rectangle([x0, 90, x0 + 158, 370], radius=18, fill="#f2f4f6", outline=INK, width=4)
        centred(d, (x0 + 79, 52), label, F(46))
        d.rectangle([x0 + 24, 130, x0 + 134, 300], outline=INK, width=3)
        h = int(166 * pct / 100)
        d.rectangle([x0 + 27, 298 - max(h, 6), x0 + 131, 298], fill=col)
        centred(d, (x0 + 79, 336), f"{pct}%", F(34), col)
    im.save(os.path.join(OUT, "MM-07.png"))


def mm09():  # no-entry sign
    im, d = canvas("#dfe9f2")
    d.rectangle([214, 300, 234, 448], fill="#6b7280")
    d.ellipse([84, 30, 364, 310], fill="#d0021b", outline="white", width=8)
    d.rectangle([124, 146, 324, 194], fill="white")
    d.rectangle([110, 330, 338, 392], fill="white", outline=INK, width=3)
    centred(d, (224, 361), "NO ENTRY", F(36))
    im.save(os.path.join(OUT, "MM-09.png"))


def mm10():  # weekend forecast
    im, d = canvas("white")
    centred(d, (224, 28), "WEEKEND FORECAST", F(26))
    # Saturday: rain
    d.rectangle([14, 60, 218, 430], fill="#e6ebf0", outline=INK, width=2)
    centred(d, (116, 92), "SATURDAY", F(26))
    d.ellipse([56, 130, 130, 190], fill="#7b8794"); d.ellipse([96, 120, 176, 190], fill="#7b8794"); d.rectangle([70, 160, 160, 190], fill="#7b8794")
    for x in (76, 106, 136):
        d.line([(x, 200), (x - 10, 230)], fill="#2a78d6", width=5)
    centred(d, (116, 276), "Rain", F(30), "#1f4f8f"); centred(d, (116, 326), "19°C", F(34))
    centred(d, (116, 378), "Chance of rain", F(17, False)); centred(d, (116, 408), "90%", F(28), "#1f4f8f")
    # Sunday: sun
    d.rectangle([230, 60, 434, 430], fill="#fff6d6", outline=INK, width=2)
    centred(d, (332, 92), "SUNDAY", F(26))
    d.ellipse([292, 126, 372, 206], fill="#f5a623")
    centred(d, (332, 276), "Sunny", F(30), "#a85b00"); centred(d, (332, 326), "26°C", F(34))
    centred(d, (332, 378), "Chance of rain", F(17, False)); centred(d, (332, 408), "5%", F(28), "#a85b00")
    im.save(os.path.join(OUT, "MM-10.png"))


def mm11():  # care label
    im, d = canvas("#c9b8a6")
    d.rectangle([64, 40, 384, 410], fill="white", outline=INK, width=3)
    centred(d, (224, 86), "100% WOOL", F(34))
    d.line([(84, 122), (364, 122)], fill=INK, width=2)
    centred(d, (224, 170), "HAND WASH", F(32)); centred(d, (224, 208), "ONLY", F(32))
    centred(d, (224, 268), "DO NOT", F(32), "#b00020"); centred(d, (224, 306), "TUMBLE DRY", F(32), "#b00020")
    centred(d, (224, 366), "DRY FLAT", F(32))
    im.save(os.path.join(OUT, "MM-11.png"))


def mm12():  # cafe menu
    im, d = canvas("#fffaf0")
    centred(d, (224, 34), "LUNCH MENU", F(32))
    d.line([(30, 62), (418, 62)], fill=INK, width=2)
    rows = [("1. Tomato soup", "Rs 120", None), ("2. Paneer tikka", "Rs 220", None),
            ("3. Cashew korma", "Rs 260", "CONTAINS NUTS"), ("4. Lemon rice", "Rs 150", None)]
    y = 84
    for name, price, warn in rows:
        d.text((28, y), name, font=F(25), fill=INK); d.text((326, y), price, font=F(23, False), fill=INK)
        if warn:
            d.rectangle([28, y + 38, 262, y + 72], fill="#b00020"); centred(d, (145, y + 55), warn, F(21), "white")
        y += 92 if warn else 78
    im.save(os.path.join(OUT, "MM-12.png"))


if __name__ == "__main__":
    chart("MM-01.png", mm01); chart("MM-02.png", mm02); chart("MM-08.png", mm08)
    for f in (mm03, mm04, mm05, mm06, mm07, mm09, mm10, mm11, mm12):
        f()
    for n in sorted(os.listdir(OUT)):
        print(n, Image.open(os.path.join(OUT, n)).size)
