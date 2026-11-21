"""Analysis of the pilot study. Writes results/summary.json and the pilot figures."""
import json, os, itertools
import numpy as np, pandas as pd
from scipy.stats import binomtest, spearmanr
import krippendorff
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "results")
FIG = os.environ.get("FIG_DIR", os.path.join(HERE, "figures"))
DATA = json.load(open(os.path.join(HERE, "golden_dataset.json")))
CATS = ["IDI", "ISA", "REG", "MM"]
DIMS = ["C", "O", "S", "T", "A", "R"]
L1, L2 = 0.2, 0.8
rng = np.random.default_rng(20261109)
S = {}

def jl(f):
    p = os.path.join(RES, f)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []

def fprag(sc): return float(np.mean([(sc[d] - 1) / 4 for d in DIMS]))

# ------------------------------------------------------------------ assemble scores per variant
met = pd.DataFrame(json.load(open(os.path.join(RES, "contrast_metrics.json"))))
met = met.set_index(["item", "cand"])
j1 = pd.DataFrame(jl("contrast_j1.jsonl")); j2 = pd.DataFrame(jl("contrast_j2.jsonl"))

def judge_col(df, cond, name):
    if df.empty: return
    d = df[df.condition == cond]
    for _, r in d.iterrows():
        sc = r["scores"]
        met.loc[(r["item"], r["cand"]), name] = fprag(sc) if "C" in sc else (sc["score"] - 1) / 9
        if "C" in sc:
            for k in DIMS: met.loc[(r["item"], r["cand"]), f"{name}_{k}"] = sc[k]
judge_col(j1, "costar", "J1_costar"); judge_col(j1, "spec_holistic", "J1_spec_holistic"); judge_col(j1, "plain", "J1_plain")
judge_col(j1, "costar_nokey", "J1_costar_nokey"); judge_col(j2, "costar", "J2_costar")
if "J1_costar" in met: met["M_eval"] = L1 * met["f_syntax"] + L2 * met["J1_costar"]
met = met.reset_index()

# ------------------------------------------------------------------ pairwise accuracy machinery
def contrasts(col, cats=CATS, kinds=("B", "C")):
    rows = []
    for it in DATA:
        if it["category"] not in cats: continue
        a = met[(met.item == it["id"]) & (met.cand == "A")][col].values
        for k in kinds:
            x = met[(met.item == it["id"]) & (met.cand == k)][col].values
            if len(a) and len(x) and not (np.isnan(a[0]) or np.isnan(x[0])):
                rows.append(dict(item=it["id"], cat=it["category"], kind=k, a=a[0], x=x[0],
                                 credit=1.0 if a[0] > x[0] else (0.5 if a[0] == x[0] else 0.0),
                                 strict=int(a[0] > x[0]), tie=int(a[0] == x[0])))
    return pd.DataFrame(rows)

def boot_ci(df, B=10000):
    if df.empty: return (np.nan, np.nan)
    items = df["item"].unique(); g = {i: df[df.item == i]["credit"].values for i in items}
    vals = []
    for _ in range(B):
        samp = rng.choice(items, len(items), replace=True)
        v = np.concatenate([g[i] for i in samp]); vals.append(v.mean())
    return tuple(np.percentile(vals, [2.5, 97.5]).round(3))

def acc_summary(col, cats=CATS):
    out = {}
    for label, kinds in [("all", ("B", "C")), ("AB", ("B",)), ("AC", ("C",))]:
        d = contrasts(col, cats, kinds)
        if d.empty: continue
        out[label] = dict(n=len(d), acc=round(d.credit.mean(), 3), strict=round(d.strict.mean(), 3), ties=round(d.tie.mean(), 3), ci=boot_ci(d))
    out["by_cat"] = {c: round(contrasts(col, [c]).credit.mean(), 3) for c in cats if not contrasts(col, [c]).empty}
    return out

def mcnemar(col1, col2, cats=CATS):
    d1, d2 = contrasts(col1, cats), contrasts(col2, cats)
    m = d1.merge(d2, on=["item", "kind"], suffixes=("_1", "_2"))
    b = int(((m.strict_1 == 1) & (m.strict_2 == 0)).sum()); c = int(((m.strict_1 == 0) & (m.strict_2 == 1)).sum())
    p = binomtest(b, b + c, 0.5).pvalue if b + c else 1.0
    return dict(b=b, c=c, p=float(p))

def holm(ps):
    order = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for rank, i in enumerate(order):
        run = max(run, min(1, (len(ps) - rank) * ps[i])); adj[i] = run
    return adj

METRICS = [("bleu", "BLEU"), ("chrf", "chrF"), ("rougeL", "ROUGE-L"), ("bertscore", "BERTScore"), ("f_syntax", "f_syntax (CoLA)")]
JUDGES = [("J1_plain", "J1 plain holistic"), ("J1_spec_holistic", "J1 holistic + spec"), ("J1_costar", "J1 CO-STAR f_prag"), ("M_eval", "M_eval (0.2/0.8)")]

S["exp1"] = {}
for col, lab in METRICS + JUDGES:
    if col in met: S["exp1"][lab] = acc_summary(col)
if "J1_costar" in met and met["J1_costar"].notna().sum() >= 90:
    tests = {lab: mcnemar("J1_costar", col) for col, lab in METRICS}
    adj = holm(np.array([t["p"] for t in tests.values()]))
    for (lab, t), a in zip(tests.items(), adj): t["p_holm"] = float(a)
    S["exp1_mcnemar_vs_J1costar"] = tests
    S["exp2_mcnemar"] = {"costar_vs_spec_holistic": mcnemar("J1_costar", "J1_spec_holistic") if "J1_spec_holistic" in met else None,
                         "costar_vs_plain": mcnemar("J1_costar", "J1_plain") if "J1_plain" in met else None,
                         "spec_holistic_vs_plain": mcnemar("J1_spec_holistic", "J1_plain") if "J1_plain" in met else None}

# overlap profile of the variants
S["variant_profile"] = met.groupby("cand")[["bleu", "chrf", "rougeL", "bertscore", "f_syntax", "n_words"]].mean().round(2).to_dict()

# ------------------------------------------------------------------ Experiment 3: answer key
if "J1_costar_nokey" in met:
    S["exp3"] = {"with_key": acc_summary("J1_costar", ["MM"]), "without_key": acc_summary("J1_costar_nokey", ["MM"])}
    mm = met[met.item.str.startswith("MM")]
    S["exp3"]["mean_O"] = {k: mm.groupby("cand")[f"{k}_O"].mean().round(2).to_dict() for k in ["J1_costar", "J1_costar_nokey"] if f"{k}_O" in mm}

# ------------------------------------------------------------------ dimension profiles (discriminant validity)
for jn in ["J1_costar", "J2_costar"]:
    cols = [f"{jn}_{d}" for d in DIMS]
    if all(c in met for c in cols):
        sub = met.dropna(subset=cols)
        S[f"dims_{jn}"] = sub.groupby("cand")[cols].mean().round(2).rename(columns=lambda c: c[-1]).to_dict(orient="index")
        S[f"dims_{jn}_by_cat"] = {c: sub[sub.category == c].groupby("cand")[cols].mean().round(2).rename(columns=lambda x: x[-1]).to_dict(orient="index") for c in CATS if (sub.category == c).any()}

# ------------------------------------------------------------------ Experiment 4: inter-judge agreement and position
def kalpha(a, b, level):
    return float(krippendorff.alpha(reliability_data=np.array([a, b], dtype=float), level_of_measurement=level))
if "J2_costar" in met:
    sub = met.dropna(subset=["J1_costar", "J2_costar"])
    if len(sub) >= 10:
        S["exp4_agreement_contrast"] = dict(n=len(sub), alpha_fprag_interval=round(kalpha(sub.J1_costar, sub.J2_costar, "interval"), 3),
            spearman=round(float(spearmanr(sub.J1_costar, sub.J2_costar)[0]), 3),
            alpha_dims_ordinal={d: round(kalpha(sub[f"J1_costar_{d}"], sub[f"J2_costar_{d}"], "ordinal"), 3) for d in DIMS},
            exact_agreement_dims={d: round(float((sub[f"J1_costar_{d}"] == sub[f"J2_costar_{d}"]).mean()), 3) for d in DIMS})
        S["exp4_J2_accuracy_text"] = acc_summary("J2_costar", ["IDI", "ISA", "REG"])
        S["exp4_J1_accuracy_text"] = acc_summary("J1_costar", ["IDI", "ISA", "REG"])
pw = pd.DataFrame(jl("pairwise_j1.jsonl"))
if not pw.empty:
    g = pw.groupby(["item", "pair"])
    cons = g.apply(lambda d: d["a_wins"].nunique() == 1 if len(d) == 2 else np.nan, include_groups=False).dropna()
    both = g.apply(lambda d: bool(d["a_wins"].all()) if len(d) == 2 else np.nan, include_groups=False).dropna()
    S["exp4_position"] = dict(n_calls=len(pw), n_pairs=int(len(cons)), acc_all_calls=round(float(pw.a_wins.mean()), 3),
        acc_A_first=round(float(pw[pw.order == "A-first"].a_wins.mean()), 3), acc_A_second=round(float(pw[pw.order == "A-second"].a_wins.mean()), 3),
        consistency=round(float(cons.mean()), 3), correct_in_both_orders=round(float(both.mean()), 3),
        first_position_choice_rate=round(float((pw.choice == 1).mean()), 3),
        by_pair={p: round(float(pw[pw.pair == p].a_wins.mean()), 3) for p in ["AB", "AC"]})

# ------------------------------------------------------------------ Experiment 5: generators
gm_path = os.path.join(RES, "gen_metrics.json")
gj1 = pd.DataFrame(jl("genjudge_j1.jsonl")); gj2 = pd.DataFrame(jl("genjudge_j2.jsonl"))
if os.path.exists(gm_path) and not gj1.empty:
    gm = pd.DataFrame(json.load(open(gm_path)))
    gj1["J1_fprag"] = gj1.scores.apply(fprag)
    for d in DIMS: gj1[f"J1_{d}"] = gj1.scores.apply(lambda s: s[d])
    gm = gm.merge(gj1[["generator", "item", "J1_fprag"] + [f"J1_{d}" for d in DIMS]], on=["generator", "item"], how="left")
    if not gj2.empty:
        gj2["J2_fprag"] = gj2.scores.apply(fprag)
        for d in DIMS: gj2[f"J2_{d}"] = gj2.scores.apply(lambda s: s[d])
        gm = gm.merge(gj2[["generator", "item", "J2_fprag"] + [f"J2_{d}" for d in DIMS]], on=["generator", "item"], how="left")
    gm["M_eval"] = L1 * gm.f_syntax + L2 * gm.J1_fprag
    gens = list(gm.generator.unique())
    S["exp5"] = dict(
        overall=gm.groupby("generator")[["M_eval", "J1_fprag", "f_syntax", "bleu", "rougeL", "bertscore", "n_words"]].mean().round(3).to_dict(orient="index"),
        by_cat={g: gm[gm.generator == g].groupby("category")["J1_fprag"].mean().round(3).to_dict() for g in gens},
        meval_by_cat={g: gm[gm.generator == g].groupby("category")["M_eval"].mean().round(3).to_dict() for g in gens},
        dims={g: gm[gm.generator == g][[f"J1_{d}" for d in DIMS]].mean().round(2).rename(lambda c: c[-1]).to_dict() for g in gens},
        spearman={a: {b: round(float(spearmanr(gm[a], gm[b], nan_policy="omit")[0]), 3) for b in ["J1_fprag", "M_eval", "f_syntax", "bleu", "chrf", "rougeL", "bertscore"]} for a in ["J1_fprag", "bleu", "bertscore"]},
        n=len(gm))
    # paired difference between generators (Wilcoxon) on M_eval
    from scipy.stats import wilcoxon
    pv = gm.pivot(index="item", columns="generator", values="M_eval").dropna()
    if len(gens) == 2 and len(pv) > 5:
        w = wilcoxon(pv[gens[0]], pv[gens[1]]); S["exp5"]["wilcoxon_meval"] = dict(n=len(pv), stat=float(w.statistic), p=float(w.pvalue), mean_diff=round(float((pv[gens[0]] - pv[gens[1]]).mean()), 3), gens=gens)
    if "J2_fprag" in gm:
        sub = gm.dropna(subset=["J1_fprag", "J2_fprag"])
        S["exp5"]["agreement"] = dict(n=len(sub), alpha_fprag_interval=round(kalpha(sub.J1_fprag, sub.J2_fprag, "interval"), 3),
                                      spearman=round(float(spearmanr(sub.J1_fprag, sub.J2_fprag)[0]), 3),
                                      J2_overall=sub.groupby("generator")["J2_fprag"].mean().round(3).to_dict(),
                                      J1_overall_text=sub.groupby("generator")["J1_fprag"].mean().round(3).to_dict())
    lam = np.linspace(0, 1, 21)
    S["exp5"]["lambda_curve"] = {g: [round(float((l * gm[gm.generator == g].J1_fprag + (1 - l) * gm[gm.generator == g].f_syntax).mean()), 4) for l in lam] for g in gens}
    gm.to_csv(os.path.join(RES, "gen_scores_table.csv"), index=False)
    S["exp5"]["empty_or_truncated"] = {g: int(((gm.generator == g) & (gm.n_words < 2)).sum()) for g in gens}

# ------------------------------------------------------------------ throughput
lat = []
for f in ["contrast_j1.jsonl", "contrast_j2.jsonl", "genjudge_j1.jsonl", "genjudge_j2.jsonl", "pairwise_j1.jsonl"]:
    for r in jl(f):
        lat.append(dict(file=f, cond=r.get("condition", "pair" if "pair" in f else "costar"), mm=r.get("category") == "MM", latency=r["latency"], ctoks=r["usage"]["completion_tokens"], ptoks=r["usage"]["prompt_tokens"]))
lat = pd.DataFrame(lat)
if not lat.empty:
    S["throughput"] = dict(n_calls=len(lat), by=lat.groupby(["cond", "mm"])[["latency", "ctoks", "ptoks"]].mean().round(1).reset_index().to_dict(orient="records"),
                           total_hours=round(float(lat.latency.sum()) / 3600, 2))
gens_raw = jl("gen_qwen3vl-2b.jsonl") + jl("gen_smolvlm2-2.2b.jsonl")
if gens_raw:
    g = pd.DataFrame(gens_raw); S["generation_stats"] = g.groupby("generator").agg(latency=("latency", "mean"), finish_length=("finish", lambda s: int((s == "length").sum()))).round(1).to_dict(orient="index")
met.to_csv(os.path.join(RES, "contrast_scores_table.csv"), index=False)
json.dump(S, open(os.path.join(RES, "summary.json"), "w"), indent=1, default=str)
print(json.dumps(S, indent=1, default=str)[:6000])
