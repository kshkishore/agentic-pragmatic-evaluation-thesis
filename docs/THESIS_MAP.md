# Map from the thesis to the repository

This file lists, for each table and figure of the thesis, the files that hold its data and the code that produces it.
- All statistics come from `study/results/summary_v2.json`, which `study/analyze_v2.py` writes.
- File paths are relative to the repository root.

## Chapter 3: Methodology

| Thesis | Content | Source |
|---|---|---|
| Section 3.2 | Pilot study | `pilot/` (code), `pilot/results/` (logs and `summary.json`, `summary2.json`) |
| Table 3.1 | Composition of the Golden Dataset | `study/golden_dataset_v2.json` (`category`, `origin`) |
| Table 3.2 | Fields of a Golden Dataset entry | `docs/CODEBOOK.md` |
| Table 3.3 | Example item EMP-01 | `study/golden_dataset_v2.json` → `EMP-01` |
| Table 3.4 | Design check on the 480 variants | `summary_v2.json` → `design_check`, `design_check_new` |
| Tables 3.5–3.6 | Software, hardware, models | `docs/MODELS.md`, `study/pipeline.py`, `requirements.txt` |
| Table 3.7 | Experiments of the main study | `study/run2.py` (phases), `docs/REPRODUCING.md` |
| Figure 3.1 | Research design | `figures/fig_design.png`; drawn by `tools/diagrams.py` |
| Figure 3.2 | The sixteen chart stimuli | `figures/fig_charts.png` (from `study/images/`); `tools/diagrams.py` |
| Figure 3.3 | Pipeline architecture | `figures/fig_pipeline.png`; `tools/diagrams.py` |

## Chapter 4: Results

| Thesis | Content | Data | Table/figure file |
|---|---|---|---|
| Table 4.1 | Model calls and time | `summary_v2.json` → `throughput` | `tables/throughput.md` |
| Table 4.2, Figure 4.1 | Metrics vs. J1 (Experiment 1) | `exp1`; `results/metrics_contrast.json` | `tables/metrics.md`, `figures/fig_metrics.png` |
| Figure 4.2 | Variant score distributions | `results/variant_table_v2.csv` | `figures/fig_variants.png` |
| Figures 4.3, 4.5 | Accuracy by category | `by_cat` of each measure in `exp1`, `exp2` | `figures/fig_cat_heat_AB.png`, `fig_cat_heat_all.png` |
| Figure 4.4 | M_eval as a function of λ | `exp2` → `lambda_curve` | `figures/fig_lambda.png` |
| Table 4.3 | J1 under three prompts (Experiment 2) | `exp2` | `tables/j1conds.md` |
| Table 4.4 | McNemar comparisons | `exp2` → `mcnemar` | `tables/mcnemar2.md` |
| Table 4.5 | Development vs. post-freeze items | `exp2` → `dev_vs_post` | `tables/devpost.md` |
| Table 4.6, Figure 4.6 | CO-STAR dimension scores | `exp2` → `dims_acc`, `profiles`, `score_means` | `tables/dims.md`, `figures/fig_profiles.png` |
| Table 4.7 | Charts with and without the answer key (Experiment 3) | `exp3` | `tables/charts.md` |
| Table 4.8 | Second judge J2 | `exp4` | `tables/j2.md` |
| Table 4.9 | J1–J2 agreement | `exp4` → `agreement` | `tables/agree.md` |
| Table 4.10 | Position consistency | `exp4` → `pairwise`; `results/pairwise_j1.jsonl` | `tables/pairwise.md` |
| Table 4.11, Figure 4.7 | Rewording and sampling | `exp4` → `robustness`; `results/robust_j1.jsonl` | `tables/robust.md`, `figures/fig_robust.png` |
| Table 4.12, Figure 4.8 | Generators (Experiment 5) | `exp5`; `results/gen_table_v2.csv` | `tables/gens.md`, `figures/fig_generators.png` |
| Figure 4.9 | Judge scores vs. rule-based checks | `exp5` → `criterion` | `figures/fig_criterion.png` |
| Section 4.7.1 | Manual check of 14 misreading flags | `study/results/qual_check_G1_O_le2.md` | — |
| Section 4.2 | Carried-over pilot calls re-run | `study/results/reuse_check.json` | — |
| Section 4.4.5 | Error analysis of J1's rubric; rule-based format check | `exp2` → `errors`, `error_dims`, `hybrid_rule_R`; `format_rule_on_variants` | — |
| Section 4.6.3 | Dimension profiles and halo | `exp2` → `halo`, `dim_corr_text` | — |

## Other chapters and appendices

| Thesis | Content | Source |
|---|---|---|
| Figure 1.1 | Example item IRO-02 with scores | `figures/fig_example.png`; `study/fig_example.py` |
| Figure 2.1 | Conceptual framework | `figures/fig_conceptual.png`; `tools/diagrams.py` |
| Appendix A (Tables A.1, A.2) | All 160 items; designed failures | `study/golden_dataset_v2.json`, `data_exports/items.csv` |
| Appendix B | Prompt templates and output grammars | `study/pipeline.py` (`COSTAR_SYS`, `SPEC_HOL_SYS`, `PLAIN_SYS`, `PAIR_SYS`, `SPEC_BLOCK`; GBNF grammars) |
| Appendix C | Core code | `study/pipeline.py`, `study/run.py`, `study/run2.py` |
| Appendix D (Tables D.1, D.2) | Model files, checksums, metric models | `docs/MODELS.md`, `study/results/sha256.json` |
| Appendix E (Tables E.1–E.6) | Detailed results by category | `by_cat` entries in `summary_v2.json` (E.1–E.3), `exp2` → `profiles_by_cat` (E.4), `exp5` → `by_cat`, `by_cat_J2` (E.5), `exp1` → `variant_means` (E.6) |

## Regenerating

```bash
cd study && python analyze_v2.py && python figures_v2.py && python fig_example.py
cd .. && python tools/tables_ch4.py && python tools/diagrams.py
```

Set `FIG_DIR` to write the figures somewhere other than `figures/`.
