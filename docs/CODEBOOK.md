# Codebook

## Identifiers used throughout

| Name | Values |
|---|---|
| `item` / `id` | `CAT-NN`, for example `IDI-01` or `MM-16` |
| `category` | `IDI`, `ISA`, `IMP`, `IRO`, `REF`, `REG`, `FTA`, `EMP`, `CUL`, `MM` |
| `cand` / variant | `A` (appropriate), `B` (pragmalinguistic or grounding failure), `C` (sociopragmatic failure) |
| `origin` | `pilot` (32 development items), `pilot-heldout` (16 held-out items), `new` (112 items written for the main study) |
| `judge` | `qwen3vl-4b` (J1, Qwen3-VL-4B-Instruct), `phi4-mini` (J2, Phi-4-mini-instruct) |
| `generator` | `qwen3vl-2b` (G1, Qwen3-VL-2B-Instruct), `smolvlm2-2.2b` (G2, SmolVLM2-2.2B-Instruct) |
| `condition` | `costar` (analytic rubric with specification), `spec_holistic` (one 1–10 score with specification), `plain` (one 1–10 score, no specification), `costar_nokey` (rubric on charts without the answer key), `costar_para` (reworded rubric), `costar_s1`/`s2`/`s3` (rubric, sampled at temperature 0.7 with seeds 101/202/303) |

## `study/golden_dataset_v2.json`

This file is a list of 160 objects.

| Field | Type | Description |
|---|---|---|
| `id` | str | Item identifier |
| `category` | str | Category code |
| `phenomenon` | str | The phenomenon tested, for example `idiom: make or break` |
| `pragmatic_layer` | str | `pragmalinguistic` or `sociopragmatic`, the main layer the item targets |
| `expected_illocution` | str | Speech-act class and type of the expected response |
| `prompt` | str | The user's message |
| `image` | str or null | Chart file in `study/images/` (MM items only) |
| `answer_key` | str or null | Facts derived from the chart data (MM items only) |
| `chart` | object or null | The data the chart was rendered from: `kind`, `title`, `x`, `y`, axis labels, and so on (MM only) |
| `costar` | object | The specification, with fields `context`, `objective`, `style`, `tone`, `audience` and `response_format` |
| `reference` | str | The reference response, used by the reference-based metrics |
| `candidates` | object | `{"A": str, "B": str, "C": str}` |
| `origin` | str | See above |

`study/golden_dataset.json` and `study/golden_dataset_ext.json` hold the 32 development items and the 16 held-out items, in the same format.

## Log files (`study/results/*.jsonl`)

Every line is one model call. These fields are common to all log files:

| Field | Description |
|---|---|
| `key` | Unique call key, for example `qwen3vl-4b\|costar\|IDI-01\|A`. A phase skips any key already in its log |
| `latency` | Wall-clock seconds for the call |
| `usage` | `prompt_tokens`, `completion_tokens`, `total_tokens` |
| `raw` | The raw model output (a JSON string, constrained by the grammar) |
| `reused_from_pilot` | `true` if the call was made in the pilot and carried over (see `PROVENANCE.md`) |

| File | Rows | Specific fields |
|---|---|---|
| `contrast_j1.jsonl` | 1,488 | `judge`, `condition` (`costar`, `spec_holistic`, `plain`, `costar_nokey`), `item`, `category`, `cand`, `scores` |
| `contrast_j2.jsonl` | 1,296 | As above, text items only, without `costar_nokey` |
| `robust_j1.jsonl` | 636 | `condition` (`costar_para`, `costar_s1`, `costar_s2`, `costar_s3`). Only the 36 items in `robust_subset.json` are analysed; the other rows are pilot robustness calls, kept for completeness |
| `pairwise_j1.jsonl` | 576 | `pair` (`AB` or `AC`), `order` (`A-first` or `A-second`), `choice` (1 or 2), `a_wins` (bool) |
| `gen_qwen3vl-2b.jsonl`, `gen_smolvlm2-2.2b.jsonl` | 160 each | `generator`, `item`, `category`, `output` (the generated response), `finish` (`stop` or `length`) |
| `genjudge_j1.jsonl`, `genjudge_j2.jsonl` | 320 / 288 | `judge`, `generator`, `item`, `category`, `scores` |

**`scores`:**
- **Rubric conditions:** `{"diagnosis": str (8–140 characters), "C", "O", "S", "T", "A", "R": int 1–5}`. The letters are Context, Objective, Style, Tone, Audience and Response format.
- **Holistic and plain conditions:** `{"score": int 1–10}`.

## Derived tables

| File | One row per | Main columns |
|---|---|---|
| `variant_table_v2.csv` | Variant (480) | `item`, `cand`, `category`, `origin`; normalised judge scores (`J1_costar`, `J1_costar_C`…`R`, `J1_spec_holistic`, `J1_plain`, `J1_costar_nokey…`, `J2_…`); every metric (see below) |
| `gen_table_v2.csv` | Generated response (320) | `generator`, `item`, `category`, `origin`, `finish`, `latency`, `n_words`, `fmt_ok` (format rule), `facts_ok` (chart-fact rule, MM only); `J1`, `J1_C`…`J1_R`, `J2`, `J2_C`…`J2_R`; metrics; `M_eval`, `J1_gate`, `J1_hybrid` |
| `metrics_contrast.json`, `metrics_gen.json` | Variant / response | Raw metric values |

**Judge scores in the tables:**
- Overall rubric scores are normalised, f_prag = mean over the six dimensions of (s − 1)/4, in the range 0–1.
- Holistic scores are normalised as (h − 1)/9.
- Dimension columns keep the raw 1–5 scale.
- `J1_gate` = min(f_prag, (O − 1)/4).
- `J1_hybrid` replaces R with the format rule's verdict.

**Metric columns:**
- **Overlap:** `bleu`, `chrf`, `rouge1`, `rouge2`, `rougeL`, `meteor`, `ter` (0–100).
- **Embedding and generative:** `bertscore` (F1 × 100), `sbert` (cosine × 100), `bartscore` (mean log-likelihood).
- **Inference** (probabilities × 100):
  - `nli_ent`: P(entailment), reference → response;
  - `nli_con`: contradiction;
  - `nli_ent_rev` and `nli_con_rev`: the reverse direction;
  - `nli_bi`: mean of the two entailment directions;
  - `nli_e_minus_c`: entailment minus contradiction.
- **Reference-free:** `gpt2_nll`, `gpt2_ppl`, `fre` (Flesch Reading Ease), `fkgl`, `n_words`, `n_sents`, `f_syntax` (CoLA acceptability probability).
- **Charts:** `clip_cos`, `clipscore`.
- **Composite:** `M_eval`, the composite metric of the thesis (Section 3.5).

## `summary_v2.json`

All statistics in the thesis come from this file. Top-level keys:

| Key | Content |
|---|---|
| `design_check`, `design_check_new` | Similarity and length checks on the variants |
| `exp1` | Pairwise accuracy of each metric (`acc` with bootstrap CI and ties, `by_cat`), `variant_means`, McNemar against J1 |
| `exp2` | J1 conditions, composite and gated scores, McNemar, origin and development vs. post-freeze, λ curve, dimension accuracy and profiles, halo, errors, rule-based hybrid |
| `exp3` | Charts with and without the answer key |
| `exp4` | J2 conditions, J1–J2 agreement, the two-judge mean (`jury`), position consistency (`pairwise`), rewording and sampling (`robustness`) |
| `exp5` | Generators: means, effects (Wilcoxon, Cliff's δ), by category, agreement, features, misreading flags, criterion checks |
| `format_rule_on_variants` | The format rule applied to the contrast variants |
| `throughput` | Calls, carried-over calls, hours, median latencies |

**Accuracy objects:**
- An accuracy object has the form `{"acc", "lo", "hi", "ties", "n"}`.
- Ties count ½ in `acc`. `lo` and `hi` are 95% percentile-bootstrap bounds over items (10,000 resamples, seed 20261109).

## Other files

| File | Content |
|---|---|
| `study/results/robust_subset.json` | The 36 items of the robustness subset |
| `study/results/reuse_check.json` | Fresh re-runs of 14 carried-over calls, compared with their logs |
| `study/results/sha256.json` | SHA-256 of every model file |
| `study/results/qual_check_G1_O_le2.md` | Annotated random sample of 14 G1 responses that J1 scored O ≤ 2 |
| `pilot/results/*` | Pilot logs in the same formats. `extset_*` is the 16 held-out items; `gen_star_*` and `genjudge_star_*` are the generator runs with the specification; `discarded_gen_smolvlm2-2.2b_template_bug.jsonl` is a discarded run (see `PROVENANCE.md`) |
