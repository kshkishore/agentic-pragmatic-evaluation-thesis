# Reproducing the thesis

There are three levels of reproduction, from minutes to about twelve hours.

## 1. Statistics, tables and figures from the logs (no language models needed)

```bash
pip install -r requirements.txt        # the first block of packages is enough
cd study
python analyze_v2.py                   # -> results/summary_v2.json (and the derived CSV tables)
python figures_v2.py                   # -> ../figures/fig_*.png (Chapter 4)
python fig_example.py                  # -> ../figures/fig_example.png (Figure 1.1)
cd ..
python tools/tables_ch4.py             # -> tables/*.md (Chapter 4 tables)
python tools/diagrams.py               # -> figures/fig_conceptual.png, fig_design.png, fig_pipeline.png, fig_charts.png
python tools/export_csv.py             # -> data_exports/*.csv
```

This takes a few minutes on a CPU. The outputs were checked against the shipped files:
- `analyze_v2.py` reproduces `summary_v2.json` exactly, with no differing values;
- `tables_ch4.py` reproduces every table in `tables/` exactly.

Set `FIG_DIR` to write the figures elsewhere.

## 2. Automatic metrics

```bash
cd study
python metrics_v2.py contrast          # -> results/metrics_contrast.json (480 variants)
python metrics_v2.py gen               # -> results/metrics_gen.json (320 generated responses)
```

The metric models are downloaded from the Hugging Face Hub (see `docs/MODELS.md` for their revisions). On a CPU this takes about an hour.

## 3. All model calls

1. Download the seven GGUF files listed in `docs/MODELS.md` into one folder and check them:
   ```bash
   cd /path/to/models && sha256sum *.gguf     # compare with study/results/sha256.json
   export MODELS_DIR=/path/to/models
   ```
2. Build and validate the dataset, render the charts and check the design rules:
   ```bash
   cd study && python build_v2.py
   ```
3. Run the experiment phases. Each phase skips any call already in its log, so start from empty `results/*.jsonl` files to re-run everything, or keep them to resume:
   ```bash
   ./phases.sh j1_text j1_mm j1_hol j2 gen j1_gen j2_gen pair rob
   ```

   | Phase | What it runs | Log |
   |---|---|---|
   | `j1_text` | J1, rubric, text variants | `contrast_j1.jsonl` |
   | `j1_mm` | J1 on chart variants: rubric, rubric without the answer key, holistic, plain | `contrast_j1.jsonl` |
   | `j1_hol` | J1, holistic and plain, text variants | `contrast_j1.jsonl` |
   | `j2` | J2, three prompts, text variants | `contrast_j2.jsonl` |
   | `gen` | G1 and G2 answer the 160 prompts | `gen_*.jsonl` |
   | `j1_gen`, `j2_gen` | Judges score the generated responses | `genjudge_j1.jsonl`, `genjudge_j2.jsonl` |
   | `pair` | J1 side by side, both orders | `pairwise_j1.jsonl` |
   | `rob` | J1, reworded rubric and three sampled runs on the 36-item subset | `robust_j1.jsonl` |

4. Then run steps 1 and 2 above.

The whole study took 11.9 hours on two CPU cores; the time per phase is in `summary_v2.json` → `throughput`. Greedy decoding with fixed model files is deterministic:
- `check_reuse.py` re-runs a random sample of logged calls and compares the outputs character for character (`results/reuse_check.json`: 14 of 14 identical);
- outputs can still differ on other hardware or with other versions of llama.cpp.

## The pilot study

`pilot/` contains the pilot's code and complete logs. The pilot used the same models and the frozen instrument developed on its 32 items. Its analysis scripts are `pilot/analyze.py` and `pilot/analyze2.py`, which write `pilot/results/summary.json` and `summary2.json`. `pilot/src/` is an earlier prototype pipeline that ran the models through a local server; it was replaced by the in-process pipeline in `pilot/pipeline.py`, which the main study's `study/pipeline.py` continues.
