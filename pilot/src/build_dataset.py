# -*- coding: utf-8 -*-
"""Assembles, validates and writes the Golden Dataset (data/golden_dataset.json + JSON Schema)."""
import collections, hashlib, json, os, sys
import jsonschema
sys.path.insert(0, os.path.dirname(__file__))
from items_text import SPEECH_ACTS, FIGURATIVE, REGISTER_CULTURE
from items_mm import MULTIMODAL
from textutil import check_format, words

ROOT = os.path.join(os.path.dirname(__file__), "..", "data")
CATS = [("speech_acts", SPEECH_ACTS), ("figurative", FIGURATIVE), ("register_culture", REGISTER_CULTURE), ("multimodal", MULTIMODAL)]

SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Golden Dataset item",
    "type": "object", "additionalProperties": False,
    "required": ["id", "category", "phenomenon", "costar", "user_turn", "image", "format_rule", "reference", "appropriate", "foils"],
    "properties": {
        "id": {"type": "string", "pattern": "^(SA|ID|RC|MM)-[0-9]{2}$"},
        "category": {"enum": ["speech_acts", "figurative", "register_culture", "multimodal"]},
        "phenomenon": {"type": "string", "minLength": 5},
        "costar": {"type": "object", "additionalProperties": False,
                   "required": ["context", "objective", "style", "tone", "audience", "response"],
                   "properties": {k: {"type": "string", "minLength": 5} for k in ["context", "objective", "style", "tone", "audience", "response"]}},
        "user_turn": {"type": "string", "minLength": 3},
        "image": {"type": ["string", "null"], "pattern": "^images/MM-[0-9]{2}\\.png$"},
        "image_sha256": {"type": "string"},
        "format_rule": {"type": ["object", "null"]},
        "reference": {"type": "string", "minLength": 10},
        "appropriate": {"type": "string", "minLength": 10},
        "foils": {"type": "array", "minItems": 2, "maxItems": 2,
                  "items": {"type": "object", "additionalProperties": False, "required": ["target", "text"],
                            "properties": {"target": {"enum": ["C", "O", "S", "T", "A", "R"]}, "text": {"type": "string", "minLength": 10}}}},
    },
}

items, problems = [], []
for cat, lst in CATS:
    for it in lst:
        it = dict(it); it["category"] = cat
        if it["image"]:
            p = os.path.join(ROOT, it["image"])
            if not os.path.exists(p):
                problems.append(f"{it['id']}: missing image")
            else:
                it["image_sha256"] = hashlib.sha256(open(p, "rb").read()).hexdigest()
        items.append(it)

validator = jsonschema.Draft202012Validator(SCHEMA)
for it in items:
    for e in validator.iter_errors(it):
        problems.append(f"{it['id']}: schema: {e.message[:120]}")
    # unicode hygiene
    for field in [it["user_turn"], it["reference"], it["appropriate"]] + [f["text"] for f in it["foils"]] + list(it["costar"].values()):
        if any(ch in field for ch in "\u201c\u201d\u2018\u2019\u00a0\t"):
            problems.append(f"{it['id']}: typographic quote/nbsp/tab present")
    if (it["category"] == "multimodal") != bool(it["image"]):
        problems.append(f"{it['id']}: image/category mismatch")
    if it["foils"][0]["target"] == it["foils"][1]["target"]:
        problems.append(f"{it['id']}: duplicate foil target")
    rule = it["format_rule"]
    for name in ("reference", "appropriate"):
        ok, v = check_format(it[name], rule)
        if ok is False:
            problems.append(f"{it['id']}: {name} breaks its own format rule: {v}")
    for f in it["foils"]:
        ok, v = check_format(f["text"], rule)
        if f["target"] == "R" and ok is not False:
            problems.append(f"{it['id']}: R-foil does not break the format rule")
        if f["target"] != "R" and ok is False:
            problems.append(f"{it['id']}: {f['target']}-foil also breaks the format rule: {v}")

ids = [it["id"] for it in items]
if len(set(ids)) != len(ids):
    problems.append("duplicate ids")
alloc = collections.Counter((it["category"], f["target"]) for it in items for f in it["foils"])
tot = collections.Counter(f["target"] for it in items for f in it["foils"])
print("items:", len(items), "| per category:", dict(collections.Counter(it["category"] for it in items)))
print("foils per target:", dict(sorted(tot.items())))
for cat, _ in CATS:
    print("  ", cat, {t: alloc[(cat, t)] for t in "COSTAR" if alloc[(cat, t)]})
wl = lambda k: [len(words(it[k])) for it in items]
fl = [len(words(f["text"])) for it in items for f in it["foils"]]
import statistics as st
print("mean words: reference %.1f, appropriate %.1f, foils %.1f" % (st.mean(wl("reference")), st.mean(wl("appropriate")), st.mean(fl)))
if problems:
    print("PROBLEMS:"); [print("  -", p) for p in problems]; sys.exit(1)
json.dump(items, open(os.path.join(ROOT, "golden_dataset.json"), "w"), indent=2, ensure_ascii=False)
json.dump(SCHEMA, open(os.path.join(ROOT, "golden_dataset.schema.json"), "w"), indent=2)
print("OK: wrote golden_dataset.json; sha256", hashlib.sha256(open(os.path.join(ROOT, "golden_dataset.json"), "rb").read()).hexdigest()[:16])
