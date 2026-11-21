"""Figure 1.1: one Golden Dataset item (IRO-02) with the scores that BLEU, BERTScore and J1 (CO-STAR) gave its three variants.
All values are read from results/variant_table_v2.csv and golden_dataset_v2.json."""
import json, os, textwrap
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "results")
FIG = os.environ.get("FIG_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures"))
ITEM = "IRO-02"
BLUE, ORANGE, AQUA, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})

ds = json.load(open(os.path.join(HERE, "golden_dataset_v2.json"))); ds = ds["items"] if isinstance(ds, dict) else ds
it = {x["id"]: x for x in ds}[ITEM]
V = pd.read_csv(os.path.join(RES, "variant_table_v2.csv")); V = V[V.item == ITEM].set_index("cand")

fig = plt.figure(figsize=(6.7, 4.6), dpi=300)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")

def box(x, y, w, h, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2", fc=fc, ec=ec, lw=0.8))

def para(x, y, s, width, **kw):
    t = "\n".join(textwrap.wrap(s, width)); ax.text(x, y, t, va="top", ha="left", linespacing=1.35, **kw); return t.count("\n") + 1

box(1.5, 77.5, 97, 21, "#f6f6f4", "#c9c8c3")
ax.text(3, 97, "User prompt", fontsize=7.5, fontweight="bold", color=INK2, va="top")
para(3, 94.2, it["prompt"], 118, fontsize=7.6, color=INK)
ax.text(3, 87.3, "Reference", fontsize=7.5, fontweight="bold", color=INK2, va="top")
para(3, 84.5, it["reference"], 118, fontsize=7.6, color=INK, style="italic")

rows = [("A", "Appropriate", AQUA), ("B", "Pragmalinguistic failure: irony read literally", BLUE), ("C", "Sociopragmatic failure: wrong register", ORANGE)]
ax.text(63, 73.2, "BLEU", fontsize=7.2, color=INK2, ha="center", fontweight="bold")
ax.text(76, 73.2, "BERTScore", fontsize=7.2, color=INK2, ha="center", fontweight="bold")
ax.text(90, 73.2, "J1 CO-STAR", fontsize=7.2, color=INK2, ha="center", fontweight="bold")
top = 70.5
for c, lab, col in rows:
    nl = len(textwrap.wrap("\u201c" + it["candidates"][c] + "\u201d", 62)); h = 8.5 + 3.4 * nl
    box(1.5, top - h, 97, h, "white", col)
    ax.add_patch(plt.Rectangle((1.5, top - h), 1.3, h, color=col, lw=0))
    ax.text(4.2, top - 2.2, f"{c}  {lab}", fontsize=7.5, fontweight="bold", color=INK, va="top")
    para(4.2, top - 6.3, "“" + it["candidates"][c] + "”", 62, fontsize=7.3, color=INK)
    r = V.loc[c]
    for x0, val, scale, fmt in [(57, r.bleu, 100, "{:.1f}"), (70, r.bertscore, 100, "{:.1f}"), (84, r.J1_costar, 1, "{:.2f}")]:
        frac = val / scale
        yb = top - h / 2 - 1.8
        ax.add_patch(plt.Rectangle((x0, yb), 12, 3.6, color=GRID, lw=0))
        ax.add_patch(plt.Rectangle((x0, yb), 12 * frac, 3.6, color=col, lw=0))
        ax.text(x0 + 6, yb + 5.2, fmt.format(val), fontsize=7.6, ha="center", color=INK, fontweight="bold")
    top -= h + 2.6
fig.savefig(f"{FIG}/fig_example.png", facecolor="white", bbox_inches="tight", pad_inches=0.04); plt.close(fig)
print("written", f"{FIG}/fig_example.png", {c: (round(V.loc[c].bleu, 1), round(V.loc[c].bertscore, 1), round(V.loc[c].J1_costar, 2)) for c in "ABC"})
