# Provenance and history of the data

## Stages

1. **Original design.** The original research design specified a proprietary model (Google's Gemini) as the evaluator. The thesis replaced it with openly licensed models run locally, so that every judgment can be repeated exactly and no data leaves the machine (thesis Section 1.4).
2. **Early prototype** (`pilot/src/`). This was a first pipeline that ran several small vision-language models through a local server, including Qwen3-VL, SmolVLM2, InternVL3 and Gemma 3. It was used to test feasibility and to choose models.
3. **Pilot study** (`pilot/`), thesis Section 3.2. 32 development items in four categories (IDI, ISA, REG, MM) were used to develop the CO-STAR rubric, the prompts, the output grammars, the decoding settings and the default weights of the composite metric `M_eval`. Determinism was confirmed: the reference condition was repeated in a separate process about fourteen hours later, and all 72 raw outputs were identical.
4. **Freeze.** After the pilot, the rubric, prompts, grammars, decoding settings and default weights were frozen and never changed afterwards.
5. **Held-out items.** Sixteen items in four new categories (IRO, IMP, FTA, REF) were written first as a held-out check (`origin = "pilot-heldout"`; pilot logs `pilot/results/extset_*`).
6. **Main study** (`study/`). 112 further items (`origin = "new"`) completed ten categories of sixteen. The frozen instrument was applied to all 160 items.

## Carried-over calls

The configuration is deterministic, so the logged outputs of pilot calls were carried over for the 48 items that the pilot had already scored with the same prompt, model and settings. This covers 1,172 of the 4,720 calls; these rows are marked `reused_from_pilot: true`.
- `study/seed_logs.py` performed the carry-over.
- `study/check_reuse.py` re-ran a random sample of 14 carried-over calls, covering both judges, all prompt types, charts and a generator. All 14 fresh outputs were identical to the logged ones (`study/results/reuse_check.json`).

## Discarded and auxiliary runs

- `pilot/results/discarded_gen_smolvlm2-2.2b_template_bug.jsonl` is a pilot generation run with SmolVLM2 that was discarded. SmolVLM2's chat template renders only list-structured message content, so the prompts were not passed correctly. The run was repeated with structured content (see `pilot/exp7.py`). It is kept for transparency and is not used in any analysis.
- `pilot/results/gen_star_*` and `genjudge_star_*` are a pilot condition in which the generators were given the specification as a system prompt.
- `study/results/robust_j1.jsonl` also contains pilot robustness rows for items outside the 36-item subset (`robust_subset.json`). The analysis ignores them.

## Analyses defined before and after seeing results

- **Fixed before the main runs:** hypotheses H1–H3, the default weights of `M_eval`, and the gated score (defined after the pilot).
- **Suggested by the results, and labelled exploratory in the thesis:** the rule-based replacement of the Response format score (`J1_hybrid`) and the mean of the two judges (`jury`).
