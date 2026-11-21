"""Experiment 7: the CO-STAR fields as a *generation* prompt (text items only).

The generators of Experiment 5 received only the user's prompt. Here each generator additionally receives a
system brief containing the four situational fields of the item's specification: Style, Tone, Audience and
Response format. Context and Objective are withheld on purpose: they name the phenomenon and the expected
content, so including them would hand the generator the answer. The evaluators then score the new outputs with
exactly the same rubric prompt as in Experiment 5.
Usage: python exp7.py <gen|j1|j2>
"""
import sys, gc, json, os, time
from pipeline import *

TEXT_ITEMS = [it for it in DATA if it["category"] != "MM"]
GENS = ["qwen3vl-2b", "smolvlm2-2.2b"]
STAR_SYS = """You are a helpful assistant. Write your reply according to this brief.
Style: {style}
Tone: {tone}
Audience: {audience}
Response format: {response_format}"""

def generate(gen):
    log = Log(f"gen_star_{gen}.jsonl"); llm = load_model(gen, True)
    structured = gen == "smolvlm2-2.2b"      # SmolVLM2's chat template renders only list-structured content
    for it in TEXT_ITEMS:
        key = f"{gen}|star|{it['id']}"
        if log.has(key): continue
        sysm = STAR_SYS.format(**{k: it["costar"][k] for k in ("style", "tone", "audience", "response_format")})
        msgs = [{"role": "system", "content": [{"type": "text", "text": sysm}] if structured else sysm},
                {"role": "user", "content": [{"type": "text", "text": it["prompt"]}] if structured else it["prompt"]}]
        t = time.time()
        r = llm.create_chat_completion(messages=msgs, temperature=0.0, max_tokens=180, seed=SEED)
        txt = r["choices"][0]["message"]["content"].strip()
        log.add(dict(key=key, generator=gen, condition="star", item=it["id"], category=it["category"], system=sysm, output=txt,
                     finish=r["choices"][0]["finish_reason"], latency=round(time.time() - t, 2), usage=r["usage"]))
        print(key, round(time.time() - t, 1), repr(txt[:160]), flush=True)
    del llm; gc.collect()

def judge(judge_name, log_name):
    log = Log(log_name); llm = load_model(judge_name, False)
    byid = {it["id"]: it for it in DATA}
    ch = build_chain(llm, COSTAR_SYS.format(mm_note="", mm_c="").replace("{", "{{").replace("}", "}}"), COSTAR_HUMAN, CostarScores, G_COSTAR, 110)
    for gen in GENS:
        for l in open(os.path.join(RES, f"gen_star_{gen}.jsonl")):
            g = json.loads(l); it = byid[g["item"]]
            key = f"{judge_name}|costar|{gen}|star|{it['id']}"
            if log.has(key): continue
            v = spec_vars(it, True); v["response"] = g["output"][:1500]
            parsed, meta = ch(v)
            log.add(dict(key=key, judge=judge_name, generator=gen, condition="star", item=it["id"], category=it["category"], scores=parsed, **meta))
            print(key, parsed, meta["latency"], flush=True)
    del llm; gc.collect()

if __name__ == "__main__":
    if sys.argv[1] == "gen":
        for g in GENS: generate(g)
    if sys.argv[1] == "j1": judge("qwen3vl-4b", "genjudge_star_j1.jsonl")
    if sys.argv[1] == "j2": judge("phi4-mini", "genjudge_star_j2.jsonl")
    if sys.argv[1] == "check":
        it = TEXT_ITEMS[0]; print(STAR_SYS.format(**{k: it["costar"][k] for k in ("style", "tone", "audience", "response_format")}))
