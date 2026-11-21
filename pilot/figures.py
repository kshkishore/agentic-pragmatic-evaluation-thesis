"""Result figures for Chapter 4 (static, print-oriented). Reads results/summary.json and score tables."""
import json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"); FIG = os.environ.get("FIG_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures"))
S = json.load(open(f"{RES}/summary.json"))
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#b9b8b3", "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlecolor": INK})
SEQ = LinearSegmentedColormap.from_list("seq", ["#f4f8fd", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
DIV = LinearSegmentedColormap.from_list("div", ["#e34948", "#f3b3b2", "#f0efec", "#9ec5f4", "#2a78d6"])

def clean(ax, grid_axis="x"):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, lw=0.8); ax.set_axisbelow(True)

# ---------------------------------------------------------------- Fig 4.1 pairwise accuracy by metric
order = ["BLEU", "chrF", "ROUGE-L", "BERTScore", "f_syntax (CoLA)", "J1 plain holistic", "J1 holistic + spec", "J1 CO-STAR f_prag", "M_eval (0.2/0.8)"]
labels = {"f_syntax (CoLA)": "f_syntax (CoLA)", "J1 plain holistic": "J1 holistic, no spec", "J1 holistic + spec": "J1 holistic + spec", "J1 CO-STAR f_prag": "J1 CO-STAR (f_prag)", "M_eval (0.2/0.8)": "M_eval (λ = 0.2/0.8)"}
e1 = S["exp1"]; order = [m for m in order if m in e1]
fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=300)
y = np.arange(len(order))[::-1]; h = 0.36
for k, (key, col, name) in enumerate([("AB", BLUE, "A vs B (pragmalinguistic / grounding failure)"), ("AC", ORANGE, "A vs C (sociopragmatic failure)")]):
    vals = [e1[m][key]["acc"] for m in order]; lo = [e1[m][key]["acc"] - e1[m][key]["ci"][0] for m in order]; hi = [e1[m][key]["ci"][1] - e1[m][key]["acc"] for m in order]
    yy = y + (h / 2 if k == 0 else -h / 2)
    ax.barh(yy, vals, height=h - 0.04, color=col, label=name, zorder=2)
    ax.errorbar(vals, yy, xerr=[lo, hi], fmt="none", ecolor=INK2, elinewidth=0.8, capsize=2, zorder=3)
    for v, yv, up in zip(vals, yy, hi): ax.text(v + up + 0.015, yv, f"{v:.2f}", va="center", ha="left", fontsize=7.0, color=INK, zorder=4)
ax.axvline(0.5, color=INK2, lw=0.9, ls=(0, (3, 3))); ax.text(0.5, len(order) - 0.35, "chance", ha="center", fontsize=7.5, color=INK2)
ax.set_yticks(y, [labels.get(m, m) for m in order]); ax.set_xlim(0, 1.12); ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_xlabel("Pairwise accuracy (ties = 0.5); bars show 95% bootstrap CI")
ax.axhline(y[4] - 0.5, color="#b9b8b3", lw=0.8)
clean(ax); ax.legend(loc="lower center", bbox_to_anchor=(0.42, -0.32), ncol=1, frameon=False, fontsize=8)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_acc.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- Fig 4.2 scores of A/B/C under three metrics (small multiples)
T = pd.read_csv(f"{RES}/contrast_scores_table.csv")
panels = [("bleu", "BLEU (0-100)"), ("bertscore", "BERTScore F1 (x100)"), ("J1_costar", "J1 CO-STAR f_prag (0-1)")]
fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.9), dpi=300)
rng = np.random.default_rng(1)
for ax, (col, title) in zip(axes, panels):
    for j, (c, colr) in enumerate(zip("ABC", [AQUA, BLUE, ORANGE])):
        v = T[T.cand == c][col].dropna().values
        ax.scatter(j + rng.uniform(-0.18, 0.18, len(v)), v, s=9, color=colr, alpha=0.75, lw=0, zorder=2)
        ax.plot([j - 0.28, j + 0.28], [np.median(v)] * 2, color=INK, lw=1.6, zorder=3)
    ax.set_xticks([0, 1, 2], ["A", "B", "C"], fontsize=8.5); ax.set_title(title, fontsize=8.8)
    clean(ax, "y")
fig.tight_layout(); fig.savefig(f"{FIG}/fig_variants.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- Fig 4.3 dimension profiles (J1 and J2)
dims = list("COSTAR")
keys = [k for k in ["dims_J1_costar", "dims_J2_costar"] if k in S]
fig, axes = plt.subplots(1, len(keys), figsize=(3.4 * len(keys), 2.4), dpi=300, squeeze=False)
for ax, k in zip(axes[0], keys):
    M = np.array([[S[k][c][d] for d in dims] for c in "ABC"])
    ax.imshow(M, cmap=SEQ, vmin=1, vmax=5, aspect="auto")
    for i in range(3):
        for j in range(6): ax.text(j, i, f"{M[i, j]:.1f}", ha="center", va="center", fontsize=8, color="white" if M[i, j] > 3.4 else INK)
    ax.set_xticks(range(6), ["Context", "Objective", "Style", "Tone", "Audience", "Format"], fontsize=7.2, rotation=35, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(3), ["A appropriate", "B prag./ground.", "C socioprag."], fontsize=7.5)
    ax.set_title(("J1 Qwen3-VL-4B, all items" if "J1" in k else "J2 Phi-4-mini, text items"), fontsize=8.8)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_dims.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- Fig 4.4 generator profiles by category
if "exp5" in S:
    E = S["exp5"]; gens = list(E["by_cat"].keys()); cats = ["IDI", "ISA", "REG", "MM"]
    names = {"qwen3vl-2b": "G1 Qwen3-VL-2B", "smolvlm2-2.2b": "G2 SmolVLM2-2.2B"}
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.8), dpi=300, gridspec_kw={"width_ratios": [1, 1.2]})
    x = np.arange(len(cats)); w = 0.36
    for k, g in enumerate(gens):
        v = [E["meval_by_cat"][g].get(c, np.nan) for c in cats]
        b = axes[0].bar(x + (k - 0.5) * w, v, w - 0.04, color=[BLUE, ORANGE][k], label=names.get(g, g), zorder=2)
        axes[0].bar_label(b, fmt="%.2f", fontsize=6.8, color=INK2, padding=1)
    axes[0].set_xticks(x, ["Idioms", "Indirect\nacts", "Register", "Charts"], fontsize=7.8); axes[0].set_ylim(0, 1.05); axes[0].set_ylabel("Mean M_eval (λ = 0.2/0.8)")
    clean(axes[0], "y"); axes[0].legend(frameon=False, fontsize=7.5, loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2)
    x2 = np.arange(6)
    for k, g in enumerate(gens):
        v = [E["dims"][g][d] for d in dims]
        b = axes[1].bar(x2 + (k - 0.5) * w, v, w - 0.04, color=[BLUE, ORANGE][k], zorder=2)
    axes[1].set_xticks(x2, ["Context", "Objective", "Style", "Tone", "Audience", "Format"], fontsize=7.2, rotation=35, ha="right", rotation_mode="anchor"); axes[1].set_ylim(1, 5.2); axes[1].set_ylabel("Mean J1 score (1-5)")
    clean(axes[1], "y")
    fig.tight_layout(); fig.savefig(f"{FIG}/fig_gen.png", facecolor=SURF); plt.close(fig)

    # ------------------------------------------------------------ Fig 4.5 lambda sensitivity
    lam = np.linspace(0, 1, 21)
    fig, ax = plt.subplots(figsize=(5.6, 3.0), dpi=300)
    Tm = T.dropna(subset=["J1_costar"])
    for c, colr, nm in zip("ABC", [AQUA, "#6250d6", "#9a9994"], ["variant A", "variant B", "variant C"]):
        sub = Tm[Tm.cand == c]; yv = [float((l * sub.J1_costar + (1 - l) * sub.f_syntax).mean()) for l in lam]
        ax.plot(lam, yv, color=colr, lw=1.4, ls=(0, (4, 2)), zorder=2); ax.text(1.01, yv[-1], nm, fontsize=7.3, color=INK2, va="center")
    for k, g in enumerate(gens):
        yv = E["lambda_curve"][g]; ax.plot(lam, yv, color=[BLUE, ORANGE][k], lw=2, zorder=3); ax.text(1.01, yv[-1], names.get(g, g), fontsize=7.3, color=INK, va="center")
    ax.axvline(0.8, color=INK2, lw=0.8, ls=":"); ax.text(0.79, ax.get_ylim()[1] - 0.005, "default λ2 = 0.8 ", fontsize=7.2, color=INK2, ha="right", va="top")
    ax.set_xlabel("λ2 (weight on f_pragmatics);  λ1 = 1 - λ2"); ax.set_ylabel("Mean M_eval"); ax.set_xlim(0, 1)
    clean(ax, "y"); fig.subplots_adjust(right=0.74, bottom=0.17, left=0.11, top=0.96); fig.savefig(f"{FIG}/fig_lambda.png", facecolor=SURF); plt.close(fig)

    # ------------------------------------------------------------ Fig 4.6 correlation matrix on generated outputs
    G = pd.read_csv(f"{RES}/gen_scores_table.csv")
    cols = [("J1_fprag", "J1 f_prag"), ("J2_fprag", "J2 f_prag"), ("f_syntax", "f_syntax"), ("bleu", "BLEU"), ("chrf", "chrF"), ("rougeL", "ROUGE-L"), ("bertscore", "BERTScore"), ("n_words", "Length")]
    cols = [c for c in cols if c[0] in G]
    C = G[[c for c, _ in cols]].corr(method="spearman").values
    fig, ax = plt.subplots(figsize=(4.8, 4.0), dpi=300)
    ax.imshow(C, cmap=DIV, vmin=-1, vmax=1)
    for i in range(len(cols)):
        for j in range(len(cols)): ax.text(j, i, f"{C[i, j]:.2f}", ha="center", va="center", fontsize=7, color="white" if abs(C[i, j]) > 0.7 else INK)
    ax.set_xticks(range(len(cols)), [n for _, n in cols], rotation=40, ha="right", fontsize=7.5); ax.set_yticks(range(len(cols)), [n for _, n in cols], fontsize=7.5)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(length=0); fig.tight_layout(); fig.savefig(f"{FIG}/fig_corr.png", facecolor=SURF); plt.close(fig)
print("figures written")
