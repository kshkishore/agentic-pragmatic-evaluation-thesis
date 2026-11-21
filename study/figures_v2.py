"""Figures for Chapter 4 of the final thesis. Reads results/summary_v2.json and the variant/generation tables."""
import json, os
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "results")
FIG = os.environ.get("FIG_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures"))
S = json.load(open(f"{RES}/summary_v2.json"))
BLUE, ORANGE, AQUA, VIOLET, GREY = "#2a78d6", "#eb6834", "#1baf7a", "#6250d6", "#8a8984"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": "#b9b8b3", "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlecolor": INK})
SEQ = LinearSegmentedColormap.from_list("seq", ["#fdf3ee", "#f9d3c0", "#f0a07a", "#e2723f", "#c4501f", "#8a3210"])
SEQB = LinearSegmentedColormap.from_list("seqb", ["#f4f8fd", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
CATS = ["IDI", "ISA", "IMP", "IRO", "REF", "REG", "FTA", "EMP", "CUL", "MM"]
CATN = {"IDI": "Idioms", "ISA": "Indirect acts", "IMP": "Implicature", "IRO": "Irony", "REF": "Reference/deixis", "REG": "Register",
        "FTA": "Politeness/FTA", "EMP": "Empathy", "CUL": "Intercultural", "MM": "Charts"}

def clean(ax, grid_axis="x"):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, lw=0.8); ax.set_axisbelow(True)

def acc_bars(ax, rows, labels, sep_after=()):
    y = np.arange(len(rows))[::-1]; h = 0.36
    for k, (key, col, name) in enumerate([("AB", BLUE, "A vs B (pragmalinguistic or grounding failure)"), ("AC", ORANGE, "A vs C (sociopragmatic failure)")]):
        vals = [r[key]["acc"] for r in rows]; lo = [r[key]["acc"] - r[key]["ci"][0] for r in rows]; hi = [r[key]["ci"][1] - r[key]["acc"] for r in rows]
        yy = y + (h / 2 if k == 0 else -h / 2)
        ax.barh(yy, vals, height=h - 0.05, color=col, label=name, zorder=2)
        ax.errorbar(vals, yy, xerr=[lo, hi], fmt="none", ecolor=INK2, elinewidth=0.7, capsize=1.6, zorder=3)
        for v, yv, up in zip(vals, yy, hi): ax.text(v + up + 0.012, yv, f"{v:.2f}", va="center", ha="left", fontsize=6.2, color=INK, zorder=4)
    ax.axvline(0.5, color=INK2, lw=0.9, ls=(0, (3, 3)))
    ax.set_yticks(y, labels, fontsize=7.6); ax.set_xlim(0, 1.12); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    for s_ in sep_after: ax.axhline(y[s_] - 0.5, color="#b9b8b3", lw=0.7)
    clean(ax); return y

# ---------------------------------------------------------------- Figure: metrics and judges, A-B and A-C accuracy
E1, E2 = S.get("exp1"), S.get("exp2")
if E1 and E2:
    order = [("bleu", "BLEU"), ("chrf", "chrF"), ("rouge1", "ROUGE-1"), ("rouge2", "ROUGE-2"), ("rougeL", "ROUGE-L"), ("meteor", "METEOR"), ("ter", "TER"),
             ("bertscore", "BERTScore"), ("sbert", "Sentence-BERT"), ("bartscore", "BARTScore"), ("gpt2_ppl", "GPT-2 perplexity"), ("fre", "Flesch Reading Ease"), ("n_words", "Length"), ("f_syntax", "f_syntax (CoLA)"),
             ("nli_ent", "NLI entailment"), ("nli_e_minus_c", "NLI entail. − contrad."), ("nli_bi", "NLI bidirectional")]
    rows = [E1[k]["acc"] for k, _ in order] + [E2[k]["acc"] for k in ["J1_plain", "J1_spec_holistic", "J1_costar", "M_eval"]]
    labels = [l for _, l in order] + ["J1 plain holistic", "J1 holistic + spec.", "J1 CO-STAR", "M_eval (J1)"]
    fig, ax = plt.subplots(figsize=(6.6, 8.4), dpi=300)
    y = acc_bars(ax, rows, labels, sep_after=(6, 9, 13, 16))
    ax.text(0.5, len(rows) - 0.3, "chance", ha="center", fontsize=7, color=INK2)
    ax.set_xlabel("Pairwise accuracy on 320 contrasts (ties = 0.5); whiskers: 95% bootstrap CI")
    ax.legend(loc="upper center", bbox_to_anchor=(0.4, -0.06), ncol=1, frameon=False, fontsize=7.6)
    fig.tight_layout(); fig.savefig(f"{FIG}/fig_metrics.png", facecolor=SURF); plt.close(fig)

    # ------------------------------------------------------------ heatmap: accuracy by category
    cols = [("bleu", "BLEU", E1), ("bertscore", "BERTScore", E1), ("bartscore", "BARTScore", E1), ("nli_bi", "NLI bidir.", E1),
            ("J1_plain", "J1 plain", E2), ("J1_spec_holistic", "J1 spec.", E2), ("J1_costar", "J1 CO-STAR", E2)]
    E4 = S.get("exp4", {})
    if "J2_costar" in E4: cols.append(("J2_costar", "J2 CO-STAR", E4))
    for key in ["AB", "all"]:
        M = np.array([[c[2][c[0]]["by_cat"].get(cat, {}).get(key, np.nan) if c[2][c[0]]["by_cat"].get(cat) else np.nan for c in cols] for cat in CATS], dtype=float)
        fig, ax = plt.subplots(figsize=(6.6, 4.4), dpi=300)
        im = ax.imshow(M, cmap=SEQB, vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(cols)), [c[1] for c in cols], rotation=30, ha="right", fontsize=7.6); ax.set_yticks(range(len(CATS)), [CATN[c] for c in CATS], fontsize=7.8)
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if not np.isnan(M[i, j]): ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=6.8, color="white" if M[i, j] > 0.6 else INK)
        ax.axvline(3.5, color="white", lw=2.5)
        cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02); cb.ax.tick_params(labelsize=7)
        cb.set_label("A-B accuracy" if key == "AB" else "Accuracy, all contrasts", fontsize=7.5)
        for s in ax.spines.values(): s.set_visible(False)
        fig.tight_layout(); fig.savefig(f"{FIG}/fig_cat_heat_{key}.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- dimension profiles (halo)
if E2:
    fig, axes = plt.subplots(1, 2 if "J2_profiles" in S.get("exp4", {}) else 1, figsize=(6.6, 2.7), dpi=300, sharey=True, squeeze=False)
    for ax, (prof, title) in zip(axes[0], [(E2["profiles"], "J1 (Qwen3-VL-4B), 480 variants"), (S.get("exp4", {}).get("J2_profiles"), "J2 (Phi-4-mini), 432 text variants")]):
        if not prof: continue
        x = np.arange(6); w = 0.26
        for k, (v, col, lab) in enumerate([("A", AQUA, "A appropriate"), ("B", BLUE, "B pragmalinguistic failure"), ("C", ORANGE, "C sociopragmatic failure")]):
            ax.bar(x + (k - 1) * w, [prof[v][d] for d in "COSTAR"], w - 0.03, color=col, label=lab, zorder=2)
        ax.set_xticks(x, ["Context", "Objective", "Style", "Tone", "Audience", "Format"], fontsize=6.5); ax.set_ylim(1, 5.3); ax.set_title(title, fontsize=8.5)
        clean(ax, "y")
    axes[0][0].set_ylabel("Mean score (1-5)")
    fig.legend(*axes[0][0].get_legend_handles_labels(), loc="lower center", ncol=3, frameon=False, fontsize=7.4, bbox_to_anchor=(0.5, -0.01))
    fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(f"{FIG}/fig_profiles.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- lambda curve
if E2 and "lambda_curve" in E2:
    lam = E2["lambda_curve"]; xs = [float(k) for k in lam]; ys = [lam[k] for k in lam]
    fig, ax = plt.subplots(figsize=(4.6, 2.6), dpi=300)
    ax.plot(xs, ys, marker="o", color=BLUE, lw=1.6, ms=4, zorder=3)
    ax.axvline(0.8, color=ORANGE, lw=1, ls=(0, (3, 3))); ax.text(0.79, min(ys) + 0.01, "default λ2 = 0.8", ha="right", fontsize=7, color=ORANGE)
    for x_, y_ in zip(xs, ys): ax.text(x_, y_ + 0.012, f"{y_:.2f}", ha="center", fontsize=6.3, color=INK)
    ax.set_xlabel("Weight of the pragmatic component, λ2 (λ1 = 1 − λ2)"); ax.set_ylabel("Pairwise accuracy"); ax.set_ylim(min(ys) - 0.04, 1.02)
    clean(ax, "y"); fig.tight_layout(); fig.savefig(f"{FIG}/fig_lambda.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- robustness
R = S.get("exp4", {}).get("robustness")
if R and "costar_s3" in R:
    conds = [("reference", "Reference (greedy)"), ("costar_para", "Reworded rubric"), ("costar_s1", "Sampled, seed 101"), ("costar_s2", "Sampled, seed 202"), ("costar_s3", "Sampled, seed 303"), ("mean_of_3", "Mean of 3 samples")]
    vals = [(R[c]["acc"]["all"] if c not in ("reference", "mean_of_3") else R[c]["all"]) for c, _ in conds]
    fig, ax = plt.subplots(figsize=(6.4, 2.6), dpi=300)
    y = np.arange(len(conds))[::-1]
    ax.errorbar([v["acc"] for v in vals], y, xerr=[[v["acc"] - v["ci"][0] for v in vals], [v["ci"][1] - v["acc"] for v in vals]], fmt="o", color=BLUE, ecolor=INK2, elinewidth=0.8, capsize=2, ms=5)
    import matplotlib.transforms as mtrans
    tr = mtrans.blended_transform_factory(ax.transAxes, ax.transData)
    for xx, h in [(1.09, "Accuracy"), (1.27, "α with\nreference"), (1.45, "Verdicts\nchanged")]:
        ax.text(xx, y[0] + 0.75, h, transform=tr, ha="center", va="bottom", fontsize=6.8, color=INK2)
    for v, yy, (c, _) in zip(vals, y, conds):
        has = c in R and isinstance(R[c], dict) and "alpha" in R[c]
        for xx, t in [(1.09, f"{v['acc']:.2f}"), (1.27, f"{R[c]['alpha']:.2f}" if has else "–"), (1.45, f"{R[c]['flips']} of {2 * R['n_items']}" if has else "–")]:
            ax.text(xx, yy, t, transform=tr, ha="center", va="center", fontsize=7)
    ax.set_yticks(y, [l for _, l in conds], fontsize=7.6); ax.set_xlim(min(v["ci"][0] for v in vals) - 0.03, 1.0)
    ax.set_ylim(y[-1] - 0.6, y[0] + 1.3)
    ax.set_xlabel(f"Pairwise accuracy with 95% CI, {R['n_items']}-item robustness subset ({2 * R['n_items']} contrasts)", fontsize=7.4); clean(ax)
    fig.subplots_adjust(left=0.2, right=0.66, bottom=0.18, top=0.97)
    fig.savefig(f"{FIG}/fig_robust.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- generators by category
E5 = S.get("exp5")
if E5 and "by_cat" in E5:
    fig, axes = plt.subplots(1, 2, figsize=(6.6, 3.1), dpi=300, gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axes[0]; y = np.arange(len(CATS))[::-1]
    for g, col, lab in [("qwen3vl-2b", BLUE, "G1 Qwen3-VL-2B"), ("smolvlm2-2.2b", ORANGE, "G2 SmolVLM2-2.2B")]:
        ax.scatter([E5["by_cat"][c][g] for c in CATS], y, color=col, label=lab, s=22, zorder=3)
    for c, yy in zip(CATS, y): ax.plot([E5["by_cat"][c]["qwen3vl-2b"], E5["by_cat"][c]["smolvlm2-2.2b"]], [yy, yy], color=GRID, lw=2, zorder=1)
    ax.set_yticks(y, [CATN[c] for c in CATS], fontsize=7.4); ax.set_xlim(0, 1.02); ax.set_xlabel("Mean J1 $f_{pragmatics}$"); ax.set_title("By category", fontsize=8.5); clean(ax)
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    ax = axes[1]; x = np.arange(6); w = 0.38; m = E5["means"]
    for k, (g, col) in enumerate([("qwen3vl-2b", BLUE), ("smolvlm2-2.2b", ORANGE)]):
        ax.bar(x + (k - 0.5) * w, [m[g][f"J1_{d}"] for d in "COSTAR"], w - 0.04, color=col, zorder=2)
    ax.set_xticks(x, list("COSTAR"), fontsize=7.6); ax.set_ylim(1, 5.2); ax.set_ylabel("Mean J1 score (1-5)"); ax.set_title("By dimension", fontsize=8.5); clean(ax, "y")
    fig.tight_layout(); fig.savefig(f"{FIG}/fig_generators.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- criterion checks
if E5 and "criterion" in E5 and os.path.exists(f"{RES}/gen_table_v2.csv"):
    G = pd.read_csv(f"{RES}/gen_table_v2.csv"); CR = E5["criterion"]
    panels = [("fmt_ok", "J1_R", "J1 Response format\nvs format rule", G), ("fmt_ok", "J2_R", "J2 Response format\nvs format rule", G[G.category != "MM"])]
    if "facts_J1_O" in CR: panels.append(("facts_ok", "J1_O", "J1 Objective\nvs chart-fact rule", G[G.category == "MM"]))
    fig, axes = plt.subplots(1, len(panels), figsize=(6.6, 2.8), dpi=300, sharey=True)
    for ax, (flag, sc, title, d) in zip(axes, panels):
        d = d.dropna(subset=[sc]); dd = d[flag].astype(bool)
        for k, (mask, col, lab) in enumerate([(dd, AQUA, "passes rule"), (~dd, ORANGE, "fails rule")]):
            vc = d[mask][sc].value_counts(normalize=True).reindex([1, 2, 3, 4, 5], fill_value=0)
            ax.bar(np.arange(1, 6) + (k - 0.5) * 0.38, vc.values, 0.36, color=col, label=f"{lab} (n = {mask.sum()})", zorder=2)
        key = {"J1_R": "format_J1_R", "J2_R": "format_J2_R", "J1_O": "facts_J1_O"}[sc]
        ax.set_title(f"{title} (AUC = {CR[key].get('auc', float('nan')):.2f})", fontsize=7.2); ax.set_xticks(range(1, 6)); ax.set_xlabel("Judge score", fontsize=7.5)
        ax.legend(frameon=False, fontsize=6.4, loc="upper left"); clean(ax, "y")
    axes[0].set_ylabel("Share of responses")
    fig.tight_layout(); fig.savefig(f"{FIG}/fig_criterion.png", facecolor=SURF); plt.close(fig)

# ---------------------------------------------------------------- score distributions by variant (160 items)
if os.path.exists(f"{RES}/variant_table_v2.csv"):
    V = pd.read_csv(f"{RES}/variant_table_v2.csv")
    panels = [("bleu", "BLEU", 100), ("bertscore", "BERTScore F1", 100), ("nli_bi", "Bidirectional NLI", 1), ("J1_costar", "J1 CO-STAR", 1)]
    fig, axes = plt.subplots(1, 4, figsize=(6.8, 2.7), dpi=300)
    rng = np.random.default_rng(20261109)
    for ax, (col, title, mult) in zip(axes, panels):
        for k, (v, c) in enumerate([("A", AQUA), ("B", BLUE), ("C", ORANGE)]):
            vals = V[V.cand == v][col].astype(float).values
            ax.scatter(k + rng.uniform(-0.22, 0.22, len(vals)), vals, s=3.5, color=c, alpha=0.55, lw=0, zorder=2)
            ax.plot([k - 0.3, k + 0.3], [np.median(vals)] * 2, color=INK, lw=1.6, zorder=3)
        ax.set_xticks([0, 1, 2], ["A", "B", "C"]); ax.set_title(title, fontsize=7.6); ax.tick_params(labelsize=7); clean(ax, "y")
    fig.tight_layout(); fig.savefig(f"{FIG}/fig_variants.png", facecolor=SURF); plt.close(fig)
print("figures written to", FIG)
