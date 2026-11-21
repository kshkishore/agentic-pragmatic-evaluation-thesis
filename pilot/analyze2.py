"""Analysis of the extension experiments (Chapter 4, Sections 4.8-4.12). Writes results/summary2.json.

Sections: ext_metrics (extended metric suite on the contrast set and on generated outputs), dims_acc (per-dimension
discrimination), criterion checks (rule-based format compliance vs R; rule-based chart facts vs O), effect sizes,
jury, lambda curve on contrasts, exp6 (robustness of the evaluator), exp7 (CO-STAR generation brief), exp8 (held-out
extension set) and the determinism check.
"""
import json, os, re, itertools
import numpy as np, pandas as pd
from scipy.stats import spearmanr, wilcoxon, binomtest, mannwhitneyu
import krippendorff
from sklearn.metrics import cohen_kappa_score, roc_auc_score
from metrics import sentences, strip_markdown

HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, "results")
DATA = json.load(open(os.path.join(HERE, "golden_dataset.json"))); BYID = {it["id"]: it for it in DATA}
EXTP = os.path.join(HERE, "golden_dataset_ext.json"); EXT = json.load(open(EXTP)) if os.path.exists(EXTP) else []
DIMS = list("COSTAR"); TEXT = ["IDI", "ISA", "REG"]; rng = np.random.default_rng(20261109)
S = {}

def jl(f):
    p = os.path.join(RES, f); return [json.loads(l) for l in open(p)] if os.path.exists(p) else []
def fprag(sc): return float(np.mean([(sc[d] - 1) / 4 for d in DIMS]))
def r3(x): return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 3)

# ------------------------------------------------------------------ generic pairwise-contrast machinery on a long table
def contrast_df(tab, col, higher=True, kinds=("B", "C")):
    """tab: rows (item, cand, category, col). Returns one row per (item, kind) contrast."""
    t = tab.set_index(["item", "cand"])[col]; rows = []
    for item in tab.item.unique():
        if (item, "A") not in t.index or pd.isna(t[(item, "A")]): continue
        a = t[(item, "A")]
        for k in kinds:
            if (item, k) not in t.index or pd.isna(t[(item, k)]): continue
            x = t[(item, k)]; a2, x2 = (a, x) if higher else (-a, -x)
            rows.append(dict(item=item, kind=k, cat=item.split("-")[0], credit=1.0 if a2 > x2 else (0.5 if a2 == x2 else 0.0), strict=int(a2 > x2), tie=int(a2 == x2), sign=int(np.sign(a2 - x2))))
    return pd.DataFrame(rows)

def boot(d, B=10000):
    if d.empty: return [None, None]
    items = d.item.unique(); g = {i: d[d.item == i].credit.values for i in items}
    v = [np.concatenate([g[i] for i in rng.choice(items, len(items))]).mean() for _ in range(B)]
    return [round(float(x), 3) for x in np.percentile(v, [2.5, 97.5])]

def acc(tab, col, higher=True):
    out = {}
    for lab, kinds in [("all", ("B", "C")), ("AB", ("B",)), ("AC", ("C",))]:
        d = contrast_df(tab, col, higher, kinds)
        if d.empty: continue
        out[lab] = dict(n=len(d), acc=r3(d.credit.mean()), strict=r3(d.strict.mean()), ties=r3(d.tie.mean()), ci=boot(d))
    return out

def mcn(tab1, c1, tab2, c2, h1=True, h2=True, kinds=("B", "C")):
    m = contrast_df(tab1, c1, h1, kinds).merge(contrast_df(tab2, c2, h2, kinds), on=["item", "kind"], suffixes=("_1", "_2"))
    b = int(((m.strict_1 == 1) & (m.strict_2 == 0)).sum()); c = int(((m.strict_1 == 0) & (m.strict_2 == 1)).sum())
    return dict(n=len(m), only_first=b, only_second=c, p=float(binomtest(b, b + c, 0.5).pvalue) if b + c else 1.0)

def holm(ps):
    order = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for rank, i in enumerate(order): run = max(run, min(1, (len(ps) - rank) * ps[i])); adj[i] = run
    return adj

def kalpha(arr, level): return r3(krippendorff.alpha(reliability_data=np.array(arr, dtype=float), level_of_measurement=level))

def cliffs_delta(x, y):
    x, y = np.asarray(x), np.asarray(y); gt = sum((xi > y).sum() for xi in x); lt = sum((xi < y).sum() for xi in x)
    return (gt - lt) / (len(x) * len(y))

# ================================================================== 1. contrast table with all metrics
T = pd.read_csv(os.path.join(RES, "contrast_scores_table.csv"))
E = pd.DataFrame(json.load(open(os.path.join(RES, "ext_metrics_contrast.json"))))
T = T.merge(E.drop(columns=["category", "n_words"]), on=["item", "cand"], how="left")
EXTM = [("rouge1", "ROUGE-1", True), ("rouge2", "ROUGE-2", True), ("meteor", "METEOR", True), ("ter", "TER (lower = better)", False),
        ("sbert", "SBERT cosine", True), ("bartscore", "BARTScore (F)", True), ("bart_p", "BARTScore (ref->cand)", True),
        ("nli_ent", "NLI entailment (ref->cand)", True), ("nli_bi", "NLI bidirectional entailment", True), ("nli_e_minus_c", "NLI entail - contradict", True),
        ("gpt2_ppl", "GPT-2 perplexity (lower = better)", False), ("fre", "Flesch Reading Ease", True), ("n_words", "Length (words)", True)]
BASE = [("bleu", "BLEU", True), ("chrf", "chrF", True), ("rougeL", "ROUGE-L", True), ("bertscore", "BERTScore", True), ("f_syntax", "f_syntax", True), ("J1_costar", "J1 CO-STAR f_prag", True)]
S["ext_metrics_contrast"] = {lab: acc(T, col, hi) for col, lab, hi in BASE + EXTM}
mm = T[T.category == "MM"]
if "clipscore" in T: S["ext_metrics_contrast"]["CLIPScore (charts only)"] = acc(mm, "clipscore", True)
tests = {lab: mcn(T, "J1_costar", T, col, True, hi) for col, lab, hi in EXTM if col not in ("n_words", "fre")}
adj = holm(np.array([t["p"] for t in tests.values()]))
for (lab, t), a in zip(tests.items(), adj): t["p_holm"] = float(a)
S["ext_mcnemar_vs_J1"] = tests
S["variant_profile_ext"] = T.groupby("cand")[["rouge1", "rouge2", "meteor", "ter", "sbert", "bartscore", "nli_ent", "nli_con", "nli_bi", "gpt2_ppl", "fre", "fkgl", "n_sents"]].mean().round(2).to_dict()

# per-dimension discrimination: which CO-STAR dimension separates A from B / C?
S["dims_acc"] = {}
for jn, cats in [("J1_costar", None), ("J2_costar", TEXT)]:
    sub = T if cats is None else T[T.category.isin(cats)]
    S["dims_acc"][jn] = {d: {k: (acc(sub, f"{jn}_{d}")[k]["acc"] if k in acc(sub, f"{jn}_{d}") else None) for k in ("AB", "AC")} for d in DIMS}

# accuracy vs lambda on the contrast set
lam = np.round(np.linspace(0, 1, 11), 2); S["lambda_contrast"] = {}
for l2 in lam:
    T["_m"] = (1 - l2) * T.f_syntax + l2 * T.J1_costar; a = acc(T, "_m")
    S["lambda_contrast"][str(l2)] = dict(all=a["all"]["acc"], AB=a["AB"]["acc"], AC=a["AC"]["acc"])
# jury: mean of J1 and J2 on text items
TT = T[T.category.isin(TEXT)].copy(); TT["jury"] = (TT.J1_costar + TT.J2_costar) / 2
S["jury_text"] = {"J1": acc(TT, "J1_costar"), "J2": acc(TT, "J2_costar"), "J1+J2 mean": acc(TT, "jury")}
# weighted kappa J1 vs J2 per dimension (contrast, text)
S["kappa_qw_J1_J2_contrast"] = {d: r3(cohen_kappa_score(TT[f"J1_costar_{d}"].astype(int), TT[f"J2_costar_{d}"].astype(int), weights="quadratic")) for d in DIMS}
# rank correlations among metrics on the contrast set (all 96 variants)
mcols = ["J1_costar", "bleu", "rougeL", "meteor", "bertscore", "sbert", "bartscore", "nli_ent", "f_syntax", "gpt2_ppl", "n_words"]
S["spearman_contrast"] = {a: {b: r3(spearmanr(T[a], T[b], nan_policy="omit")[0]) for b in mcols} for a in ["J1_costar", "bertscore", "nli_ent"]}

# ================================================================== 2. rule-based criterion checks
def n_sent(text):
    lines = [l for l in strip_markdown(text).split("\n") if l.strip()]
    body = [l for l in lines if not re.match(r"^\s*(dear|hi|hello|good (morning|afternoon|evening))\b[^.!?]*,?\s*$", l, re.I) and not re.match(r"^\s*(best|kind|warm)?\s*(regards|wishes|thanks|sincerely|cheers)\b[^.!?]*,?\s*$", l, re.I) and not re.match(r"^\s*\[?[A-Z][a-z]+( [A-Z][a-z]+)?\]?\s*$", l)]
    return len(sentences(" ".join(body))) if body else 0

def fmt_ok(text, spec):
    s = spec.lower(); n = n_sent(text); w = len(strip_markdown(text).split())
    if "at most 60 words" in s: return w <= 60
    if "exactly two" in s: ok = n == 2
    elif "two or three" in s: ok = 2 <= n <= 3
    elif "one or two" in s: ok = 1 <= n <= 2
    elif s.startswith("one") and "sentence" in s: ok = n == 1
    elif "short direct answer" in s: ok = n <= 2 and w <= 40
    else: ok = True
    if "salutation" in s: ok = ok and bool(re.match(r"^\s*(dear|hi|hello)\b", strip_markdown(text), re.I))
    return bool(ok)

FACTS = {  # minimal core facts each chart answer must state (lower-case regex, all required)
    "MM-01": [r"\bapril|\bapr\b", r"\b31\b|31,000|31 ?k"], "MM-02": [r"\brent\b", r"\b40\s?%|40 per ?cent"], "MM-03": [r"telugu", r"\b9\b|nine"],
    "MM-04": [r"saturday|\bsat\b", r"\b55\b"], "MM-05": [r"\b30\s?%", r"\b55\s?%", r"online"], "MM-06": [r"\b95\b", r"\b2 hours|\(2,|2 hours|two hours|\b2\b"],
    "MM-07": [r"august|\baug\b", r"\b185\b"], "MM-08": [r"\b60\b", r"week 4|\bw4\b|fourth week"]}
def facts_ok(item, text): return all(re.search(p, strip_markdown(text).lower()) for p in FACTS[item])

G = pd.read_csv(os.path.join(RES, "gen_scores_table.csv"))
raw = {(r["generator"], r["item"]): r for f in ["gen_qwen3vl-2b.jsonl", "gen_smolvlm2-2.2b.jsonl"] for r in jl(f)}
G["output"] = [raw[(g, i)]["output"] for g, i in zip(G.generator, G.item)]
G["finish"] = [raw[(g, i)]["finish"] for g, i in zip(G.generator, G.item)]
G["fmt_ok"] = [fmt_ok(o, BYID[i]["costar"]["response_format"]) for o, i in zip(G.output, G.item)]
G["n_sent_rule"] = [n_sent(o) for o in G.output]
T["fmt_ok"] = [fmt_ok(BYID[i]["candidates"][c], BYID[i]["costar"]["response_format"]) for i, c in zip(T.item, T.cand)]
def crit(df, flag, score):
    d = df.dropna(subset=[score]); y = d[flag].astype(int)
    out = dict(n=len(d), n_ok=int(y.sum()), mean_ok=r3(d[d[flag]][score].mean()), mean_fail=r3(d[~d[flag]][score].mean()))
    if 0 < y.sum() < len(y): out.update(auc=r3(roc_auc_score(y, d[score])), mwu_p=float(mannwhitneyu(d[d[flag]][score], d[~d[flag]][score]).pvalue))
    return out
S["criterion_format"] = {"gen_J1_R": crit(G, "fmt_ok", "J1_R"), "gen_J2_R": crit(G[G.category != "MM"], "fmt_ok", "J2_R"),
                         "contrast_J1_R": crit(T, "fmt_ok", "J1_costar_R"), "contrast_J2_R": crit(T[T.category.isin(TEXT)], "fmt_ok", "J2_costar_R"),
                         "gen_fmt_rate": G.groupby("generator").fmt_ok.mean().round(3).to_dict(), "gen_truncated": G.groupby("generator").finish.apply(lambda s: int((s == "length").sum())).to_dict()}
GM = G[G.category == "MM"].copy(); GM["facts_ok"] = [facts_ok(i, o) for i, o in zip(GM.item, GM.output)]
S["criterion_chart"] = dict(gen=crit(GM, "facts_ok", "J1_O"), by_gen=GM.groupby("generator").facts_ok.mean().round(3).to_dict(),
                            detail=GM[["generator", "item", "facts_ok", "J1_O", "J1_C"]].to_dict(orient="records"))
TM = T[T.category == "MM"].copy(); TM["facts_ok"] = [facts_ok(i, BYID[i]["candidates"][c]) for i, c in zip(TM.item, TM.cand)]
S["criterion_chart"]["contrast"] = crit(TM, "facts_ok", "J1_costar_O")
S["criterion_chart"]["contrast_by_cand"] = TM.groupby("cand").facts_ok.mean().round(3).to_dict()

# ================================================================== 3. generated outputs: extended metrics, effect sizes
EG = pd.DataFrame(json.load(open(os.path.join(RES, "ext_metrics_gen.json"))))
G = G.merge(EG.drop(columns=["category", "n_words"]), on=["generator", "item"], how="left")
gcols = ["J1_fprag", "J2_fprag", "f_syntax", "bleu", "rougeL", "meteor", "ter", "bertscore", "sbert", "bartscore", "nli_ent", "gpt2_ppl", "fre", "n_words"]
S["gen_ext_means"] = G.groupby("generator")[[c for c in gcols if c in G]].mean().round(2).to_dict(orient="index")
S["gen_spearman_J1"] = {c: r3(spearmanr(G.J1_fprag, G[c], nan_policy="omit")[0]) for c in gcols if c in G}
gens = ["qwen3vl-2b", "smolvlm2-2.2b"]
eff = {}
for c in ["J1_fprag", "J2_fprag", "M_eval", "f_syntax", "bleu", "bertscore", "sbert", "nli_ent", "bartscore"] + [f"J1_{d}" for d in DIMS]:
    pv = G.pivot(index="item", columns="generator", values=c).dropna()
    if len(pv) < 5: continue
    d = pv[gens[0]] - pv[gens[1]]
    p = float(wilcoxon(pv[gens[0]], pv[gens[1]]).pvalue) if (d != 0).any() else 1.0
    eff[c] = dict(n=len(pv), mean_G1=r3(pv[gens[0]].mean()), mean_G2=r3(pv[gens[1]].mean()), cliffs_delta=r3(cliffs_delta(pv[gens[0]], pv[gens[1]])),
                  G1_better=int((d > 0).sum()), G2_better=int((d < 0).sum()), ties=int((d == 0).sum()), wilcoxon_p=p)
S["gen_effects"] = eff
S["gen_by_cat"] = {g: G[G.generator == g].groupby("category")[["J1_fprag", "f_syntax", "bleu", "bertscore", "nli_ent"]].mean().round(3).to_dict(orient="index") for g in gens}
S["kappa_qw_J1_J2_gen"] = {d: r3(cohen_kappa_score(G.dropna(subset=["J2_C"])[f"J1_{d}"].astype(int), G.dropna(subset=["J2_C"])[f"J2_{d}"].astype(int), weights="quadratic")) for d in DIMS}
G.drop(columns=["output"]).to_csv(os.path.join(RES, "gen_scores_table_ext.csv"), index=False)
T.drop(columns=["_m"], errors="ignore").to_csv(os.path.join(RES, "contrast_scores_table_ext.csv"), index=False)

# ================================================================== 4. Experiment 6: robustness of the evaluator (text items)
R1 = pd.DataFrame(jl("robust_j1.jsonl")); R2 = pd.DataFrame(jl("robust_j2.jsonl"))
base = pd.DataFrame([r for r in jl("contrast_j1.jsonl") if r["category"] in TEXT and r["condition"] in ("costar", "spec_holistic", "plain")])
base2 = pd.DataFrame([r for r in jl("contrast_j2.jsonl") if r["condition"] == "costar"])
def long(df, cond, name=None):
    d = df[df.condition == cond].copy()
    d["val"] = d.scores.apply(lambda s: fprag(s) if "C" in s else (s["score"] - 1) / 9)
    for k in DIMS: d[k] = d.scores.apply(lambda s: s.get(k, np.nan))
    return d[["item", "cand", "category", "val", "latency"] + DIMS].assign(condition=name or cond)
conds = {"costar (greedy, reference)": long(base, "costar")}
for c in ["costar_nodiag", "costar_para", "costar_rev", "costar_s1", "costar_s2", "costar_s3", "costar_rerun"]:
    if not R1.empty and (R1.condition == c).sum(): conds[c] = long(R1, c)
if all(c in conds for c in ["costar_s1", "costar_s2", "costar_s3"]):
    m = conds["costar_s1"].copy()
    for k in ["val"] + DIMS: m[k] = (conds["costar_s1"][k].values + conds["costar_s2"][k].values + conds["costar_s3"][k].values) / 3
    for a, b in [("costar_s2", "costar_s1"), ("costar_s3", "costar_s1")]: assert (conds[a].item.values == conds[b].item.values).all() and (conds[a].cand.values == conds[b].cand.values).all()
    conds["costar_s_mean (3 samples)"] = m.assign(condition="costar_s_mean")
ref = conds["costar (greedy, reference)"].set_index(["item", "cand"])
E6 = {}
for name, d in conds.items():
    a = acc(d, "val"); dd = d.set_index(["item", "cand"]).loc[ref.index]
    cr = contrast_df(d, "val"); c0 = contrast_df(conds["costar (greedy, reference)"], "val"); mm_ = cr.merge(c0, on=["item", "kind"], suffixes=("", "_ref"))
    E6[name] = dict(acc=a, mean_by_cand=d.groupby("cand").val.mean().round(3).to_dict(), dims_by_cand=d.groupby("cand")[DIMS].mean().round(2).to_dict(orient="index"),
                    alpha_vs_ref_fprag=kalpha([ref.val.values, dd.val.values], "interval"), rho_vs_ref=r3(spearmanr(ref.val, dd.val)[0]),
                    alpha_vs_ref_dims={k: kalpha([ref[k].values, dd[k].values], "ordinal") for k in DIMS},
                    exact_vs_ref_dims={k: r3((ref[k].values == dd[k].values).mean()) for k in DIMS},
                    flips_vs_ref=int((mm_.sign != mm_.sign_ref).sum()), n_contrasts=len(mm_),
                    O_on_C=r3(d[d.cand == "C"].O.mean()), O_on_B=r3(d[d.cand == "B"].O.mean()),
                    rho_S_A=r3(spearmanr(d["S"], d["A"])[0]), rho_T_A=r3(spearmanr(d["T"], d["A"])[0]), rho_O_C=r3(spearmanr(d["O"], d["C"])[0]),
                    latency=r3(d.latency.mean()) if d.latency.notna().all() else None)
    if name != "costar (greedy, reference)": E6[name]["mcnemar_vs_ref"] = mcn(d, "val", conds["costar (greedy, reference)"], "val")
S["exp6_j1"] = E6
if all(c in conds for c in ["costar_s1", "costar_s2", "costar_s3"]):
    s = [conds[c].set_index(["item", "cand"]).loc[ref.index] for c in ["costar_s1", "costar_s2", "costar_s3"]]
    S["exp6_sampling"] = dict(alpha_3runs_fprag=kalpha([x.val.values for x in s], "interval"),
                              alpha_3runs_dims={k: kalpha([x[k].values for x in s], "ordinal") for k in DIMS},
                              alpha_4runs_fprag_incl_greedy=kalpha([ref.val.values] + [x.val.values for x in s], "interval"),
                              identical_all3_dims={k: r3(np.mean((s[0][k].values == s[1][k].values) & (s[1][k].values == s[2][k].values))) for k in DIMS},
                              identical_all3_vector=r3(np.mean(np.all([(s[0][k].values == s[1][k].values) & (s[1][k].values == s[2][k].values) for k in DIMS], axis=0))),
                              sd_fprag_mean=r3(np.mean(np.std(np.vstack([x.val.values for x in s]), axis=0))),
                              contrast_sign_agree_all3=None)
    sg = [contrast_df(c_.reset_index(), "val").sort_values(["item", "kind"]).sign.values for c_ in s]
    S["exp6_sampling"]["contrast_sign_agree_all3"] = r3(np.mean((sg[0] == sg[1]) & (sg[1] == sg[2])))
    S["exp6_sampling"]["contrast_correct_all3"] = r3(np.mean((sg[0] == 1) & (sg[1] == 1) & (sg[2] == 1)))
    S["exp6_sampling"]["contrast_correct_atleast1"] = r3(np.mean((sg[0] == 1) | (sg[1] == 1) | (sg[2] == 1)))
# J2 replication of Experiment 2
E62 = {}
if not R2.empty:
    j2c = {"costar": long(base2, "costar"), "spec_holistic": long(R2, "spec_holistic"), "plain": long(R2, "plain")}
    for n_, d in j2c.items(): E62[n_] = dict(acc=acc(d, "val"), mean_by_cand=d.groupby("cand").val.mean().round(3).to_dict(), latency=r3(d.latency.mean()))
    E62["mcnemar"] = {"costar_vs_spec_holistic": mcn(j2c["costar"], "val", j2c["spec_holistic"], "val"), "costar_vs_plain": mcn(j2c["costar"], "val", j2c["plain"], "val"),
                      "spec_holistic_vs_plain": mcn(j2c["spec_holistic"], "val", j2c["plain"], "val")}
    j1t = {"costar": long(base, "costar"), "spec_holistic": long(base, "spec_holistic"), "plain": long(base, "plain")}
    E62["J1_text_same_items"] = {n_: acc(d, "val") for n_, d in j1t.items()}
S["exp6_j2_prompt_conditions"] = E62

# ================================================================== 5. Experiment 7: CO-STAR fields as a generation brief
st = pd.DataFrame(jl("genjudge_star_j1.jsonl"))
if len(st) >= 48:
    st["J1_fprag"] = st.scores.apply(fprag)
    for d in DIMS: st[f"J1_{d}"] = st.scores.apply(lambda s: s[d])
    s2 = pd.DataFrame(jl("genjudge_star_j2.jsonl"))
    if len(s2): s2["J2_fprag"] = s2.scores.apply(fprag); st = st.merge(s2[["generator", "item", "J2_fprag"]], on=["generator", "item"], how="left")
    if "J2_fprag" not in st: st["J2_fprag"] = np.nan
    gs = pd.DataFrame(jl("gen_star_qwen3vl-2b.jsonl") + jl("gen_star_smolvlm2-2.2b.jsonl"))
    gs["n_words"] = gs.output.apply(lambda o: len(strip_markdown(o).split())); gs["fmt_ok"] = [fmt_ok(o, BYID[i]["costar"]["response_format"]) for o, i in zip(gs.output, gs.item)]
    st = st.merge(gs[["generator", "item", "n_words", "fmt_ok", "finish", "latency"]].rename(columns={"latency": "gen_latency"}), on=["generator", "item"])
    base5 = G[G.category.isin(TEXT)][["generator", "item", "category", "J1_fprag", "J2_fprag", "n_words", "fmt_ok"] + [f"J1_{d}" for d in DIMS]]
    M = base5.merge(st[["generator", "item", "J1_fprag", "J2_fprag", "n_words", "fmt_ok", "finish"] + [f"J1_{d}" for d in DIMS]], on=["generator", "item"], suffixes=("_plain", "_star"))
    E7 = {}
    for g in gens:
        m = M[M.generator == g]; out = dict(n=len(m))
        for c in ["J1_fprag", "J2_fprag", "n_words"] + [f"J1_{d}" for d in DIMS]:
            a, b = m[f"{c}_plain"], m[f"{c}_star"]; ok = a.notna() & b.notna(); dif = (b - a)[ok]
            out[c] = dict(plain=r3(a[ok].mean()), star=r3(b[ok].mean()), improved=int((dif > 0).sum()), worse=int((dif < 0).sum()), same=int((dif == 0).sum()),
                          p=float(wilcoxon(a[ok], b[ok]).pvalue) if (dif != 0).any() else 1.0, cliffs_delta=r3(cliffs_delta(b[ok], a[ok])) if ok.sum() else None)
        out["fmt_rate"] = dict(plain=r3(m.fmt_ok_plain.mean()), star=r3(m.fmt_ok_star.mean()))
        out["truncated_star"] = int((m.finish == "length").sum())
        out["by_cat_J1"] = {c: dict(plain=r3(m[m.category == c].J1_fprag_plain.mean()), star=r3(m[m.category == c].J1_fprag_star.mean())) for c in TEXT}
        E7[g] = out
    S["exp7"] = E7

# ================================================================== 6. Experiment 8: held-out extension set
x1 = pd.DataFrame(jl("extset_j1.jsonl")); x2 = pd.DataFrame(jl("extset_j2.jsonl"))
if len(x2) < 144: x2 = pd.DataFrame()  # use the second judge only once its run is complete
xm = os.path.join(RES, "extset_metrics_ext.json")
if len(x1) >= 144:
    E8 = {}
    X = pd.DataFrame(json.load(open(xm))) if os.path.exists(xm) else pd.DataFrame([dict(item=it["id"], cand=c, category=it["category"]) for it in EXT for c in "ABC"])
    for nm, df in [("J1", x1), ("J2", x2)]:
        if df.empty: continue
        for c in ["costar", "spec_holistic", "plain"]:
            d = long(df, c); X = X.merge(d[["item", "cand", "val"] + (DIMS if c == "costar" else [])].rename(columns={"val": f"{nm}_{c}", **({k: f"{nm}_{c}_{k}" for k in DIMS} if c == "costar" else {})}), on=["item", "cand"], how="left")
    cols = [c for c in X.columns if c.startswith(("J1_", "J2_")) and c.split("_")[-1] not in DIMS]
    lex = [("bleu", True), ("chrf", True), ("rougeL", True), ("meteor", True), ("ter", False), ("bertscore", True), ("sbert", True), ("nli_ent", True), ("nli_bi", True), ("bartscore", True), ("f_syntax", True), ("gpt2_ppl", False)]
    for c in cols: E8[c] = acc(X, c)
    for c, hi in lex:
        if c in X: E8[c] = acc(X, c, hi)
    E8["by_cat_J1_costar"] = {cat: acc(X[X.category == cat], "J1_costar").get("all", {}).get("acc") for cat in ["IRO", "IMP", "FTA", "REF"]}
    E8["by_cat_J2_costar"] = {cat: acc(X[X.category == cat], "J2_costar").get("all", {}).get("acc") for cat in ["IRO", "IMP", "FTA", "REF"]} if "J2_costar" in X else {}
    E8["dims"] = {nm: X.groupby("cand")[[f"{nm}_costar_{k}" for k in DIMS]].mean().round(2).rename(columns=lambda c: c[-1]).to_dict(orient="index") for nm in ["J1", "J2"] if f"{nm}_costar_C" in X}
    E8["mcnemar"] = {f"{nm}_costar_vs_{c}": mcn(X, f"{nm}_costar", X, f"{nm}_{c}") for nm in ["J1", "J2"] for c in ["spec_holistic", "plain"] if f"{nm}_{c}" in X}
    if "J2_costar" in X:
        sub = X.dropna(subset=["J1_costar", "J2_costar"])
        E8["agreement"] = dict(alpha=kalpha([sub.J1_costar, sub.J2_costar], "interval"), rho=r3(spearmanr(sub.J1_costar, sub.J2_costar)[0]))
    # gated score (pragmatic score capped at the normalised Objective score), Objective alone and the composite M_eval
    for nm in ["J1", "J2"]:
        if f"{nm}_costar_O" not in X: continue
        X[f"{nm}_gate"] = np.minimum(X[f"{nm}_costar"], (X[f"{nm}_costar_O"] - 1) / 4)
        X[f"{nm}_O_only"] = X[f"{nm}_costar_O"]
        X[f"{nm}_meval"] = 0.2 * X.f_syntax + 0.8 * X[f"{nm}_costar"]
        for c in ["gate", "O_only", "meval"]: E8[f"{nm}_{c}"] = acc(X, f"{nm}_{c}")
        E8["mcnemar"][f"nli_bi_vs_{nm}_costar"] = mcn(X, "nli_bi", X, f"{nm}_costar")
        E8[f"by_cat_{nm}_spec_holistic"] = {cat: acc(X[X.category == cat], f"{nm}_spec_holistic").get("all", {}).get("acc") for cat in ["IRO", "IMP", "FTA", "REF"]}
    E8["by_cat_nli_bi"] = {cat: acc(X[X.category == cat], "nli_bi").get("all", {}).get("acc") for cat in ["IRO", "IMP", "FTA", "REF"]}
    E8["by_cat_bertscore"] = {cat: acc(X[X.category == cat], "bertscore").get("all", {}).get("acc") for cat in ["IRO", "IMP", "FTA", "REF"]}
    if "J2_costar" in X and X.J2_costar.notna().all():
        X["jury_costar"] = (X.J1_costar + X.J2_costar) / 2; E8["jury_costar"] = acc(X, "jury_costar")
    X.to_csv(os.path.join(RES, "extset_scores_table.csv"), index=False)
    S["exp8"] = E8

json.dump(S, open(os.path.join(RES, "summary2.json"), "w"), indent=1, default=str)
print("sections:", list(S))
