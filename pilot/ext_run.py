"""Experiment 8: replication on the held-out extension set (golden_dataset_ext.json, 16 text items).

The evaluator prompts, grammars, decoding settings and weights are exactly those of Experiments 1, 2 and 4.
Also contains the determinism check of Experiment 6 (a second greedy pass of J1 over the core text items).
Usage: python ext_run.py <j1|j2|rerun>
"""
import sys, gc, json, os
from pipeline import *
from robust import chain, esc, TEXT_ITEMS

EXT = json.load(open(os.path.join(HERE, "golden_dataset_ext.json")))

def run(judge, conds, items, log_name, tag=""):
    log = Log(log_name); llm = load_model(judge, False)
    for cond in conds:
        if cond == "costar": ch = chain(llm, esc(COSTAR_SYS.format(mm_note="", mm_c="")), COSTAR_HUMAN, CostarScores, G_COSTAR, 110)
        elif cond == "spec_holistic": ch = chain(llm, esc(SPEC_HOL_SYS.format(mm_note="")), COSTAR_HUMAN, Holistic, G_HOL, 8)
        elif cond == "plain": ch = chain(llm, esc(PLAIN_SYS.format(mm_note="")), PLAIN_HUMAN, Holistic, G_HOL, 8)
        for it in items:
            for cand in "ABC":
                key = f"{judge}|{cond}{tag}|{it['id']}|{cand}"
                if log.has(key): continue
                v = spec_vars(it); v["response"] = it["candidates"][cand]
                parsed, meta = ch(v)
                log.add(dict(key=key, judge=judge, condition=cond + tag, item=it["id"], category=it["category"], cand=cand, scores=parsed, **meta))
                print(key, {k: v for k, v in parsed.items() if k != "diagnosis"}, meta["latency"], flush=True)
    del llm; gc.collect()

if __name__ == "__main__":
    if sys.argv[1] == "j1": run("qwen3vl-4b", ["costar", "spec_holistic", "plain"], EXT, "extset_j1.jsonl")
    if sys.argv[1] == "j2": run("phi4-mini", ["costar", "spec_holistic", "plain"], EXT, "extset_j2.jsonl")
    if sys.argv[1] == "rerun": run("qwen3vl-4b", ["costar"], TEXT_ITEMS, "robust_j1.jsonl", tag="_rerun")
