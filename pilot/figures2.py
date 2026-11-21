"""Figures for the second-phase analyses (Chapter 4). Reads results/summary2.json; writes PNGs to FIG_DIR."""
import json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "results")
FIG = os.environ.get("FIG_DIR", os.path.join(HERE, "figures"))
S = json.load(open(f"{RES}/summary2.json"))
BLUE, ORANGE, AQUA, VIOLET = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#b9b8b3", "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlecolor": INK})
SEQ = LinearSegmentedColormap.from_list("seq", ["#f4f8fd", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])

def clean(ax, grid_axis="x"):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, lw=0.8); ax.set_axisbelow(True)

def acc_bars(ax, rows, labels, sep_after=()):
    y = np.arange(len(rows))[::-1]; h = 0.36
    for k, (key, col, name) in enumerate([("AB", BLUE, "A vs B (pragmalinguistic / grounding failure)"), ("AC", ORANGE, "A vs C (sociopragmatic failure)")]):
        vals = [r[key]["acc"] for r in rows]; lo = [r[key]["acc"] - r[key]["ci"][0] for r in rows]; hi = [r[key]["ci"][1] - r[key]["acc"] for r in rows]
        yy = y + (h / 2 if k == 0 else -h / 2)
        ax.barh(yy, vals, height=h - 0.05, color=col, label=name, zorder=2)
        ax.errorbar(vals, yy, xerr=[lo, hi], fmt="none", ecolor=INK2, elinewidth=0.7, capsize=1.8, zorder=3)
        for v, yv, up in zip(vals, yy, hi): ax.text(v + up + 0.012, yv, f"{v:.2f}", va="center", ha="left", fontsize=6.3, color=INK, zorder=4)
    ax.axvline(0.5, color=INK2, lw=0.9, ls=(0, (3, 3)))
    ax.set_yticks(y, labels, fontsize=7.6); ax.set_xlim(0, 1.13); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    for s_ in sep_after: ax.axhline(y[s_] - 0.5, color="#b9b8b3", lw=0.7)
    clean(ax)
    return y

# ---------------------------------------------------------------- extended metric suite on the contrast set
E = S["ext_metrics_contrast"]
order = [("BLEU", "BLEU"), ("chrF", "chrF"), ("ROUGE-1", "ROUGE-1"), ("ROUGE-2", "ROUGE-2"), ("ROUGE-L", "ROUGE-L"), ("METEOR", "METEOR"), ("TER (lower = better)", "TER"),
         ("BERTScore", "BERTScore"), ("SBERT cosine", "Sentence-BERT cosine"), ("BARTScore (F)", "BARTScore (F)"), ("BARTScore (ref->cand)", "BARTScore (ref → cand)"),
         ("NLI entailment (ref->cand)", "NLI entailment"), ("NLI bidirectional entailment", "NLI bidirectional"), ("NLI entail - contradict", "NLI entail − contradict"),
         ("f_syntax", "f_syntax (CoLA)"), ("GPT-2 perplexity (lower = better)", "GPT-2 perplexity"), ("Flesch Reading Ease", "Flesch Reading Ease"), ("Length (words)", "Length"),
         ("J1 CO-STAR f_prag", "J1 CO-STAR f_prag")]
rows = [E[k] for k, _ in order]
fig, ax = plt.subplots(figsize=(6.6, 7.4), dpi=300)
y = acc_bars(ax, rows, [l for _, l in order], sep_after=(6, 8, 10, 13, 17))
ax.set_xlim(0, 1.42)
ax.text(0.5, len(order) - 0.25, "chance", ha="center", fontsize=7, color=INK2)
for (a_, b_), txt in [((0, 6), "n-gram\noverlap"), ((7, 8), "embedding"), ((9, 10), "generative"), ((11, 13), "inference\n(NLI)"), ((14, 17), "reference-\nfree"), ((18, 18), "LLM judge")]:
    ax.text(1.40, (y[a_] + y[b_]) / 2, txt, ha="right", va="center", fontsize=6.6, color=INK2, style="italic")
ax.set_xlabel("Pairwise accuracy on the 64 core contrasts (ties = 0.5); bars show 95% bootstrap CI")
ax.legend(loc="upper center", bbox_to_anchor=(0.42, -0.07), ncol=1, frameon=False, fontsize=7.6)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_ext_acc.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- criterion checks
T = pd.read_csv(f"{RES}/gen_scores_table_ext.csv")
raw = {}
for f in ["gen_qwen3vl-2b.jsonl", "gen_smolvlm2-2.2b.jsonl"]:
    for l in open(f"{RES}/{f}"): r = json.loads(l); raw[(r["generator"], r["item"])] = r
det = pd.DataFrame(S["criterion_chart"]["detail"])
fig, axes = plt.subplots(1, 2, figsize=(6.6, 2.9), dpi=300, gridspec_kw={"width_ratios": [1.15, 1]})
rng = np.random.default_rng(3)
for ax, (df, flag, col, title, xl) in zip(axes, [(T, "fmt_ok", "J1_R", "Format: J1 Response-format score", ["fails rule", "passes rule"]),
                                                 (det, "facts_ok", "J1_O", "Charts: J1 Objective score", ["missing fact", "facts stated"])]):
    for j, ok in enumerate([False, True]):
        sub = df[df[flag] == ok]
        for g, colr, mk in [("qwen3vl-2b", BLUE, "o"), ("smolvlm2-2.2b", ORANGE, "s")]:
            v = sub[sub.generator == g][col].values
            ax.scatter(j + rng.uniform(-0.17, 0.17, len(v)) + (-0.06 if g == "qwen3vl-2b" else 0.06), v + rng.uniform(-0.12, 0.12, len(v)), s=12, color=colr, marker=mk, alpha=0.8, lw=0, zorder=2,
                       label=({"qwen3vl-2b": "G1 Qwen3-VL-2B", "smolvlm2-2.2b": "G2 SmolVLM2-2.2B"}[g] if (j == 1 and ax is axes[0]) else None))
        m = sub[col].mean(); ax.plot([j - 0.3, j + 0.3], [m, m], color=INK, lw=1.6, zorder=3); ax.text(j + 0.33, m, f"{m:.2f}", va="center", fontsize=7, color=INK)
        ax.text(j, 0.35, f"n = {len(sub)}", ha="center", fontsize=6.8, color=INK2)
    ax.set_xticks([0, 1], xl, fontsize=7.8); ax.set_ylim(0.1, 5.5); ax.set_yticks([1, 2, 3, 4, 5]); ax.set_xlim(-0.5, 1.6); ax.set_title(title, fontsize=8.6)
    clean(ax, "y")
h_, l_ = axes[0].get_legend_handles_labels(); fig.legend(h_, l_, frameon=False, fontsize=7, loc="lower center", ncol=2)
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(f"{FIG}/fig_criterion.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- Experiment 6: robustness
R = S["exp6_j1"]
conds = [("costar (greedy, reference)", "Reference (greedy)"), ("costar_rerun", "Repeated greedy run"), ("costar_nodiag", "No diagnosis"), ("costar_para", "Reworded rubric"),
         ("costar_rev", "Reversed order"), ("costar_s1", "Sampled, seed 101"), ("costar_s2", "Sampled, seed 202"), ("costar_s3", "Sampled, seed 303"), ("costar_s_mean (3 samples)", "Mean of 3 samples")]
conds = [c for c in conds if c[0] in R]
fig, axes = plt.subplots(1, 2, figsize=(6.8, 3.4), dpi=300, gridspec_kw={"width_ratios": [1.05, 1.25]})
ax = axes[0]; yy = np.arange(len(conds))[::-1]
for y_, (k, lab) in zip(yy, conds):
    a = R[k]["acc"]["all"]; ax.errorbar(a["acc"], y_, xerr=[[a["acc"] - a["ci"][0]], [a["ci"][1] - a["acc"]]], fmt="o", color=BLUE if "s" not in k[-2:] else BLUE, ms=4.5, ecolor=INK2, elinewidth=0.8, capsize=2, zorder=3)
    ax.text(1.065, y_, f"{a['acc']:.2f}", va="center", fontsize=7, color=INK)
ax.set_yticks(yy, [l for _, l in conds], fontsize=7.6); ax.set_xlim(0.8, 1.1); ax.set_xticks([0.8, 0.9, 1.0]); ax.set_xlabel("Pairwise accuracy, 48 text contrasts")
ax.axvline(R["costar (greedy, reference)"]["acc"]["all"]["acc"], color=INK2, lw=0.8, ls=":"); clean(ax)
ax2 = axes[1]; dims = list("COSTAR"); cc = [c for c in conds if c[0] not in ("costar (greedy, reference)",)]
M = np.array([[R[k]["alpha_vs_ref_dims"][d] for d in dims] + [R[k]["alpha_vs_ref_fprag"]] for k, _ in cc])
ax2.imshow(M, cmap=SEQ, vmin=0, vmax=1, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]): ax2.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=6.8, color="white" if M[i, j] > 0.72 else INK)
ax2.set_xticks(range(7), ["Context", "Objective", "Style", "Tone", "Audience", "Format", "f_prag"], fontsize=7, rotation=35, ha="right", rotation_mode="anchor")
ax2.set_yticks(range(len(cc)), [l for _, l in cc], fontsize=7.2); ax2.set_title("Alpha with the reference run", fontsize=8.4)
for s_ in ax2.spines.values(): s_.set_visible(False)
ax2.tick_params(length=0)
fig.tight_layout(); fig.savefig(f"{FIG}/fig_robust.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- Experiment 7: generation brief
if "exp7" in S:
    E7 = S["exp7"]; names = {"qwen3vl-2b": "G1 Qwen3-VL-2B", "smolvlm2-2.2b": "G2 SmolVLM2-2.2B"}
    fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.9), dpi=300, sharey=True)
    labs = ["Context", "Objective", "Style", "Tone", "Audience", "Format"]
    for ax, g in zip(axes, ["qwen3vl-2b", "smolvlm2-2.2b"]):
        y = np.arange(6)[::-1]
        for yi, d in zip(y, dims):
            a, b = E7[g][f"J1_{d}"]["plain"], E7[g][f"J1_{d}"]["star"]
            ax.plot([a, b], [yi, yi], color="#b9b8b3", lw=1.6, zorder=1)
            ax.scatter([a], [yi], color=INK2, s=22, zorder=2, label="Prompt only (Exp. 5)" if d == "C" else None)
            ax.scatter([b], [yi], color=AQUA if b >= a else ORANGE, s=26, zorder=3, marker="D", label="With CO-STAR brief (Exp. 7)" if d == "C" else None)
        ax.set_yticks(y, labs, fontsize=7.6); ax.set_xlim(1, 5.2); ax.set_xticks([1, 2, 3, 4, 5]); ax.set_title(names[g], fontsize=8.6); clean(ax)
        ax.set_xlabel("Mean J1 score, 24 text prompts")
    axes[0].legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(1.05, -0.22), ncol=2)
    fig.tight_layout(); fig.subplots_adjust(wspace=0.1); fig.savefig(f"{FIG}/fig_exp7.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- Experiment 8: held-out phenomena
if "exp8" in S:
    E8 = S["exp8"]
    met8 = [("bleu", "BLEU"), ("chrf", "chrF"), ("meteor", "METEOR"), ("ter", "TER (lower = better)"), ("bertscore", "BERTScore"), ("sbert", "Sentence-BERT cosine"),
            ("bartscore", "BARTScore (F)"), ("gpt2_ppl", "GPT-2 perplexity (lower)"), ("f_syntax", "f_syntax (CoLA)"), ("nli_bi", "NLI bidirectional")]
    j28 = [("J2_plain", "J2 holistic, no spec"), ("J2_spec_holistic", "J2 holistic + spec"), ("J2_costar", "J2 CO-STAR f_prag")]
    j18 = [("J1_plain", "J1 holistic, no spec"), ("J1_spec_holistic", "J1 holistic + spec"), ("J1_costar", "J1 CO-STAR f_prag"), ("J1_gate", "J1 gated score")]
    groups = [[o for o in g if o[0] in E8] for g in (met8, j28, j18)]
    order8 = [o for g in groups for o in g]; seps = []; run = -1
    for g in groups[:-1]:
        if g: run += len(g); seps.append(run)
    fig, ax = plt.subplots(figsize=(6.6, 0.36 * len(order8) + 1.3), dpi=300)
    y = acc_bars(ax, [E8[k] for k, _ in order8], [l for _, l in order8], sep_after=tuple(seps))
    ax.set_xlim(0, 1.1)
    ax.text(0.5, len(order8) - 0.25, "chance", ha="center", fontsize=7, color=INK2)
    ax.set_xlabel("Pairwise accuracy, 32 held-out contrasts (ties = 0.5); whiskers: 95% bootstrap CI")
    ax.legend(loc="upper center", bbox_to_anchor=(0.42, -0.09), ncol=1, frameon=False, fontsize=7.6)
    fig.tight_layout(); fig.savefig(f"{FIG}/fig_extset.png", facecolor=SURF); plt.close(fig)
print("figures2 written")
