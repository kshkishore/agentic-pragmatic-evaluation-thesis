import json, os, collections, statistics as st
RES = "results"
files = {"phase1": ["contrast_j1.jsonl", "contrast_j2.jsonl", "genjudge_j1.jsonl", "genjudge_j2.jsonl", "pairwise_j1.jsonl"],
         "phase2": ["robust_j1.jsonl", "robust_j2.jsonl", "genjudge_star_j1.jsonl", "genjudge_star_j2.jsonl", "extset_j1.jsonl", "extset_j2.jsonl"]}
gens = {"phase1": ["gen_qwen3vl-2b.jsonl", "gen_smolvlm2-2.2b.jsonl"], "phase2": ["gen_star_qwen3vl-2b.jsonl", "gen_star_smolvlm2-2.2b.jsonl"]}
out = {}
for ph, fs in files.items():
    n = 0; lat = 0; valid = 0; by = collections.defaultdict(list)
    for f in fs:
        p = os.path.join(RES, f)
        if not os.path.exists(p): continue
        for l in open(p):
            r = json.loads(l); n += 1; lat += r["latency"]
            raw = r.get("raw", "")
            try: json.loads(raw); valid += 1
            except Exception: pass
            cond = r.get("condition", "pair" if "pair" in f else "costar"); judge = r.get("judge", "qwen3vl-4b")
            by[(judge, cond.split("_s")[0] if cond.startswith("costar_s") else cond, r.get("category") == "MM")].append(r["latency"])
    g = [json.loads(l) for f in gens[ph] if os.path.exists(os.path.join(RES, f)) for l in open(os.path.join(RES, f))]
    out[ph] = dict(eval_calls=n, valid_json=valid, eval_hours=round(lat / 3600, 2), gen_calls=len(g), gen_hours=round(sum(x["latency"] for x in g) / 3600, 2),
                   by={f"{k[0]}|{k[1]}|{'MM' if k[2] else 'text'}": (len(v), round(st.mean(v), 1)) for k, v in sorted(by.items())})
print(json.dumps(out, indent=1))
