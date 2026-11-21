"""Exports the 160-item Golden Dataset (study/golden_dataset_v2.json) to flat CSV files in ../data_exports/."""
import json, csv, os
H = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(H, "..", "study", "golden_dataset_v2.json")))
d = d if isinstance(d, list) else d["items"]
out = os.path.join(H, "..", "data_exports"); os.makedirs(out, exist_ok=True)
F = ["id", "category", "phenomenon", "pragmatic_layer", "expected_illocution", "origin", "prompt", "image", "answer_key",
     "context", "objective", "style", "tone", "audience", "response_format", "reference", "A", "B", "C"]
with open(os.path.join(out, "items.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=F); w.writeheader()
    for it in d:
        row = {k: it.get(k) for k in F[:9]}
        row.update({k: it["costar"][k] for k in ["context", "objective", "style", "tone", "audience", "response_format"]})
        row["reference"] = it["reference"]; row.update(it["candidates"]); w.writerow(row)
with open(os.path.join(out, "responses_long.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "category", "variant", "variant_type", "text"])
    T = {"REF": "reference", "A": "appropriate", "B": "pragmalinguistic or grounding failure", "C": "sociopragmatic failure"}
    for it in d:
        w.writerow([it["id"], it["category"], "REF", T["REF"], it["reference"]])
        for v in "ABC": w.writerow([it["id"], it["category"], v, T[v], it["candidates"][v]])
print("exported", len(d), "items")
