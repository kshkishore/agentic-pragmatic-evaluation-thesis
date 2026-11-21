"""Builds the result tables of Chapter 4 (Markdown, in ../tables/) from study/results/summary_v2.json."""
import json, glob, re, sys, os
S = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "study", "results", "summary_v2.json")))
E1, E2, E4, E5 = S.get("exp1", {}), S.get("exp2", {}), S.get("exp4", {}), S.get("exp5", {})
def f2(x): return "n/a" if x is None else f"{x:.2f}"
def ci(a): return f"{a['acc']:.2f} [{a['ci'][0]:.2f}, {a['ci'][1]:.2f}]" if a.get("ci") else f"{a['acc']:.2f}"
def pfmt(p):
    if p < 0.001: return "< .001"
    s = f"{p:.3f}"; return s[1:] if s.startswith("0") else s
CATN = {"IDI": "Idioms and proverbs", "ISA": "Indirect speech acts", "IMP": "Implicature and presupposition", "IRO": "Irony and stance", "REF": "Reference and deixis",
        "REG": "Register", "FTA": "Politeness and FTAs", "EMP": "Empathy", "CUL": "Intercultural", "MM": "Charts"}
CATS = list(CATN)
T = {}

FAM = {"bleu": "N-gram overlap", "chrf": "N-gram overlap", "rouge1": "N-gram overlap", "rouge2": "N-gram overlap", "rougeL": "N-gram overlap", "meteor": "N-gram overlap",
       "ter": "Edit distance", "bertscore": "Embedding", "sbert": "Embedding", "bartscore": "Generative", "nli_ent": "Inference", "nli_bi": "Inference",
       "nli_e_minus_c": "Inference", "gpt2_ppl": "Reference-free", "fre": "Reference-free", "n_words": "Reference-free", "f_syntax": "Reference-free"}
if E1:
    r = ["Table 4.2: Pairwise accuracy of the automatic metrics and of the CO-STAR evaluator on the 320 contrasts (95% bootstrap confidence intervals for all contrasts; p: exact McNemar test against J1 CO-STAR on strict correctness, Holm-adjusted)", "",
         "| Metric | Family | A-B | A-C | All contrasts | p |", "|---|---|---|---|---|---|"]
    mc = E1.get("mcnemar_J1_vs", {})
    for col in FAM:
        a = E1[col]["acc"]; r.append(f"| {E1[col]['label']} | {FAM[col]} | {f2(a['AB']['acc'])} | {f2(a['AC']['acc'])} | {ci(a['all'])} | {pfmt(mc[col]['p_holm']) if col in mc else ''} |")
    c = E1.get("clipscore_MM")
    if c: r.append(f"| CLIPScore (charts only, 32 contrasts) | Image-text | {f2(c['AB']['acc'])} | {f2(c['AC']['acc'])} | {ci(c['all'])} | |")
    a = E2["J1_costar"]["acc"]; r.append(f"| **J1 CO-STAR evaluator** | LLM judge | **{f2(a['AB']['acc'])}** | **{f2(a['AC']['acc'])}** | **{ci(a['all'])}** | |")
    T["metrics"] = "\n".join(r)

if E2:
    r = ["Table 4.3: Pairwise accuracy of the evaluator J1 under three prompts, of the composite and gated scores and of the Objective dimension alone (320 contrasts; 95% bootstrap confidence intervals)", "",
         "| Measure | A-B | A-C | All contrasts | Ties |", "|---|---|---|---|---|"]
    for col, lab in [("J1_plain", "Plain holistic prompt"), ("J1_spec_holistic", "Holistic prompt with specification"), ("J1_costar", "CO-STAR rubric ($f_{pragmatics}$)"),
                     ("M_eval", "$M_{eval}$ ($\\lambda_2 = 0.8$)"), ("J1_gate", "Gated score"), ("J1_costar_O", "Objective dimension alone")]:
        if col in E2:
            a = E2[col]["acc"]; r.append(f"| {lab} | {ci(a['AB'])} | {ci(a['AC'])} | {ci(a['all'])} | {a['all']['ties']:.0%} |")
    if "hybrid_rule_R" in E2:
        a = E2["hybrid_rule_R"]["acc"]; r.append(f"| CO-STAR with rule-based format check (exploratory) | {ci(a['AB'])} | {ci(a['AC'])} | {ci(a['all'])} | {a['all']['ties']:.0%} |")
    T["j1conds"] = "\n".join(r)
    m = E2["mcnemar"]
    r = ["Table 4.4: Paired comparisons of the J1 conditions (exact McNemar tests on strict correctness, 320 contrasts)", "",
         "| Comparison | Correct only under first | Correct only under second | p |", "|---|---|---|---|"]
    for k, lab in [("costar_vs_spec", "CO-STAR vs holistic with specification"), ("costar_vs_plain", "CO-STAR vs plain holistic"), ("spec_vs_plain", "Holistic with specification vs plain holistic"),
                   ("meval_vs_costar", "$M_{eval}$ vs CO-STAR")]:
        if k in m: r.append(f"| {lab} | {m[k]['only_first']} | {m[k]['only_second']} | {pfmt(m[k]['p'])} |")
    T["mcnemar2"] = "\n".join(r)
    r = ["Table 4.5: Pairwise accuracy of J1 on development and post-freeze items (95% bootstrap confidence intervals)", "",
         "| Prompt | Development items (32 items, 64 contrasts) | Post-freeze items (128 items, 256 contrasts) |", "|---|---|---|"]
    for col, lab in [("J1_plain", "Plain holistic"), ("J1_spec_holistic", "Holistic with specification"), ("J1_costar", "CO-STAR rubric")]:
        d = E2["dev_vs_post"][col]; r.append(f"| {lab} | {ci(d['dev'])} | {ci(d['post'])} |")
    T["devpost"] = "\n".join(r)
    da = E2["dims_acc"]; P = E2["profiles"]; DN = {"C": "Context", "O": "Objective", "S": "Style", "T": "Tone", "A": "Audience", "R": "Response format"}
    r = ["Table 4.6: J1 CO-STAR dimension scores: mean score of each variant (scale 1 to 5) and pairwise accuracy of each dimension used alone", "",
         "| Dimension | Mean A | Mean B | Mean C | Accuracy A-B | Accuracy A-C | Ties |", "|---|---|---|---|---|---|---|"]
    for d in "COSTAR":
        r.append(f"| {DN[d]} | {P['A'][d]:.2f} | {P['B'][d]:.2f} | {P['C'][d]:.2f} | {f2(da[d]['AB']['acc'])} | {f2(da[d]['AC']['acc'])} | {da[d]['all']['ties']:.0%} |")
    T["dims"] = "\n".join(r)

if S.get("exp3"):
    E3 = S["exp3"]
    r = ["Table 4.7: J1 on the 32 chart contrasts with and without the answer key", "",
         "| Condition | A-B | A-C | All contrasts | Mean Objective score of A / B / C |", "|---|---|---|---|---|"]
    for k, lab, o in [("key", "CO-STAR with answer key", "J1_costar"), ("nokey", "CO-STAR without answer key", "J1_costar_nokey")]:
        a = E3[k]; om = E3["O_means"][o]; r.append(f"| {lab} | {ci(a['AB'])} | {ci(a['AC'])} | {ci(a['all'])} | {om['A']:.2f} / {om['B']:.2f} / {om['C']:.2f} |")
    for k, lab in [("spec", "Holistic with specification (with key)"), ("plain", "Plain holistic (no specification, no key)")]:
        a = E3[k]; r.append(f"| {lab} | {ci(a['AB'])} | {ci(a['AC'])} | {ci(a['all'])} | |")
    T["charts"] = "\n".join(r)

if E4:
    r = ["Table 4.8: Pairwise accuracy of the second judge J2 and of J1 on the 288 text contrasts", "",
         "| Prompt | J2 A-B | J2 A-C | J2 all contrasts | J2 ties | J1 all contrasts |", "|---|---|---|---|---|---|"]
    for col, lab, j1 in [("J2_plain", "Plain holistic", "J1_plain"), ("J2_spec_holistic", "Holistic with specification", "J1_spec_holistic"), ("J2_costar", "CO-STAR rubric", "J1_costar")]:
        if col in E4:
            a = E4[col]["acc"]; r.append(f"| {lab} | {ci(a['AB'])} | {ci(a['AC'])} | {ci(a['all'])} | {a['all']['ties']:.0%} | {f2(E4['J1_on_text'][j1])} |")
    if "jury" in E4: a = E4["jury"]; r.append(f"| Mean of J1 and J2 CO-STAR scores (exploratory) | {ci(a['AB'])} | {ci(a['AC'])} | {ci(a['all'])} | {a['all']['ties']:.0%} | |")
    T["j2"] = "\n".join(r)
    g = E4["agreement"]; DN = {"C": "Context", "O": "Objective", "S": "Style", "T": "Tone", "A": "Audience", "R": "Response format"}
    r = [f"Table 4.9: Agreement between J1 and J2 on the CO-STAR scores of the {g['n']} text variants", "",
         "| Score | Krippendorff's alpha | Quadratically weighted kappa | Exact agreement |", "|---|---|---|---|"]
    for d in "COSTAR":
        x = g["dims"][d]; r.append(f"| {DN[d]} | {x['alpha_ord']:.2f} (ordinal) | {x['qwk']:.2f} | {x['exact']:.0%} |")
    r.append(f"| $f_{{pragmatics}}$ | {g['alpha_fprag']:.2f} (interval) | | Spearman's rho = {g['rho_fprag']:.2f} |")
    T["agree"] = "\n".join(r)

TP = S.get("throughput")
if TP:
    bfc, bg = TP["by_file_cond"], TP["by_gen"]
    rows = [("contrast_j1.jsonl|costar", "J1", "CO-STAR rubric, contrast variants"), ("contrast_j1.jsonl|costar_nokey", "J1", "CO-STAR rubric, charts without answer key"),
            ("contrast_j1.jsonl|spec_holistic", "J1", "Holistic with specification"), ("contrast_j1.jsonl|plain", "J1", "Plain holistic"),
            ("contrast_j2.jsonl|costar", "J2", "CO-STAR rubric, text variants"), ("contrast_j2.jsonl|spec_holistic", "J2", "Holistic with specification"),
            ("contrast_j2.jsonl|plain", "J2", "Plain holistic"), ("pairwise_j1.jsonl|pair", "J1", "Pairwise judgments, both orders"),
            ("robust_j1.jsonl|costar_para", "J1", "Reworded rubric (robustness subset)"), ("robust_j1.jsonl|costar_sampled", "J1", "Three sampled runs (robustness subset)"),
            ("genjudge_j1.jsonl|pair", "J1", "CO-STAR rubric, generated responses"), ("genjudge_j2.jsonl|pair", "J2", "CO-STAR rubric, generated text responses")]
    r = ["Table 4.1: Model calls of the main study: number of calls, calls carried over from the pilot, time per call and total time", "",
         "| Model | Task | Calls | From pilot | Mean s per call | Median s per call | Hours |", "|---|---|---|---|---|---|---|"]
    tot_n = tot_h = tot_re = 0
    for g, lab in [("qwen3vl-2b", "G1"), ("smolvlm2-2.2b", "G2")]:
        x = bg[g]; r.append(f"| {lab} | Generation, 160 prompts | {x['n']} | {x['reused']} | {x['mean_s']:.1f} | {x.get('median_s', 0):.1f} | {x['hours']:.2f} |")
        tot_n += x["n"]; tot_h += x["hours"]; tot_re += x["reused"]
    for k, m, lab in rows:
        if k in bfc:
            x = bfc[k]; r.append(f"| {m} | {lab} | {x['n']:,} | {x['reused']} | {x['mean_s']:.1f} | {x['median_s']:.1f} | {x['hours']:.2f} |")
            tot_n += x["n"]; tot_h += x["hours"]; tot_re += x["reused"]
    r.append(f"| **Total** | | **{tot_n:,}** | **{tot_re:,}** | | | **{tot_h:.1f}** |")
    T["throughput"] = "\n".join(r)

if E5 and "effects" in E5:
    ef, pa = E5["effects"], E5.get("pref_agree_J1", {})
    r = ["Table 4.12: Scores of the two generators on the 160 prompts (means; paired Wilcoxon signed-rank tests and Cliff's delta; agreement: share of prompts on which a measure prefers the same generator as J1 among those on which neither is tied)", "",
         "| Measure | G1 | G2 | G1 higher | G2 higher | p | Cliff's delta | Agreement with J1 |", "|---|---|---|---|---|---|---|---|"]
    for c, lab, fmt in [("J1", "J1 $f_{pragmatics}$", "{:.2f}"), ("J1_gate", "J1 gated score", "{:.2f}"), ("J1_hybrid", "J1 with rule-based format check (exploratory)", "{:.2f}"),
                        ("J2", "J2 $f_{pragmatics}$ (text prompts)", "{:.2f}"), ("M_eval", "$M_{eval}$", "{:.2f}"), ("f_syntax", "$f_{syntax}$", "{:.2f}"),
                        ("bleu", "BLEU", "{:.1f}"), ("chrf", "chrF", "{:.1f}"), ("rougeL", "ROUGE-L", "{:.1f}"), ("bertscore", "BERTScore F1", "{:.1f}"),
                        ("sbert", "SBERT cosine", "{:.1f}"), ("nli_bi", "Bidirectional NLI", "{:.1f}"), ("bartscore", "BARTScore", "{:.2f}"),
                        ("gpt2_ppl", "GPT-2 perplexity, median (lower is better)", "{:.1f}"), ("n_words", "Length in words", "{:.1f}")]:
        if c not in ef: continue
        x = ef[c]; ag = pa.get(c)
        agt = "" if c in ("J1", "J1_gate", "J1_hybrid", "M_eval", "gpt2_ppl") else (f"{ag['agree']:.2f} (n = {ag['n']})" if ag else "")
        if c == "n_words" and ag: agt = f"{ag['agree']:.2f} (shorter preferred; n = {ag['n']})"
        if c == "gpt2_ppl": x = dict(x, g1=x.get("g1_med", x["g1"]), g2=x.get("g2_med", x["g2"]))
        r.append(f"| {lab} | {fmt.format(x['g1'])} | {fmt.format(x['g2'])} | {x['g1_higher']} | {x['g2_higher']} | {pfmt(x['p'])} | {x['delta']:.2f} | {agt} |")
    T["gens"] = "\n".join(r)

if E4.get("pairwise"):
    pw = E4["pairwise"]
    r = [f"Table 4.10: Position consistency of J1 in side-by-side judgments ({pw['n_pairs']} text contrasts, each judged with A first and with A second; {pw['n_calls']} calls)", "",
         "| Contrast | A chosen when first | A chosen when second | Same verdict in both orders | Correct in both orders |", "|---|---|---|---|---|"]
    for k, lab in [("AB", "A-B"), ("AC", "A-C")]:
        if k in pw["by_pair"]:
            x = pw["by_pair"][k]; r.append(f"| {lab} | {x['a_first']:.2f} | {x['a_second']:.2f} | {x.get('consistent', float('nan')):.2f} | {x.get('both_correct', float('nan')):.2f} |")
    r.append(f"| All | {pw['a_first']:.2f} | {pw['a_second']:.2f} | {pw['consistent']:.2f} | {pw['both_correct']:.2f} |")
    T["pairwise"] = "\n".join(r)

RB = E4.get("robustness")
if RB:
    r = [f"Table 4.11: J1 CO-STAR judgments under a reworded rubric and three sampled runs on the robustness subset ({RB['n_items']} items, {2 * RB['n_items']} contrasts; reference: the original greedy run on the same items)", "",
         "| Condition | Pairwise accuracy | Ties | Krippendorff's alpha with reference | Contrasts whose verdict changes |", "|---|---|---|---|---|"]
    r.append(f"| Original rubric, greedy decoding (reference) | {ci(RB['reference']['all'])} | {RB['reference']['all']['ties']:.0%} | | |")
    for c, lab in [("costar_para", "Reworded rubric, greedy decoding"), ("costar_s1", "Original rubric, sampled (seed 101)"), ("costar_s2", "Original rubric, sampled (seed 202)"), ("costar_s3", "Original rubric, sampled (seed 303)")]:
        if c in RB:
            x = RB[c]; r.append(f"| {lab} | {ci(x['acc']['all'])} | {x['acc']['all']['ties']:.0%} | {x['alpha']:.2f} | {x['flips']} |")
    if "mean_of_3" in RB: r.append(f"| Mean of the three sampled runs | {ci(RB['mean_of_3']['all'])} | {RB['mean_of_3']['all']['ties']:.0%} | | |")
    T["robust"] = "\n".join(r)

for k, v in T.items(): open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tables", f"{k}.md"), "w").write(v + "\n")
print("tables:", list(T))
