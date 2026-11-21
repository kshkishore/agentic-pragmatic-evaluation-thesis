# Agentic Evaluation of Pragmatic Competence in Multimodal LLMs: thesis data and code

This is the research repository for the PhD thesis

> **Agentic Evaluation of Pragmatic Competence in Multimodal Large Language Models: A Prompt Engineering Approach**
> Katikela Sreeharsha Kishore, Centre for Applied Linguistics and Translation Studies, University of Hyderabad (2026)

It contains every dataset item and every model call made for the thesis, together with the code, figures and tables. With these, every number in the thesis can be checked and reproduced. Running `study/analyze_v2.py` on the shipped logs regenerates `study/results/summary_v2.json` exactly, and `tools/tables_ch4.py` then regenerates the Chapter 4 tables exactly.

## The study in brief

- **The Golden Dataset** has 160 items in ten categories of pragmatic phenomena, sixteen items per category: idioms, indirect speech acts, implicature and presupposition, irony, reference and deixis, register, politeness, empathy, intercultural pragmatics, and charts. Each item has:
  - a user prompt;
  - a six-field CO-STAR specification (Context, Objective, Style, Tone, Audience, Response format);
  - a reference response;
  - three response variants: **A**, appropriate; **B**, a pragmalinguistic or grounding failure that reuses the reference's wording; **C**, a sociopragmatic failure.

  Together they give 320 contrasts whose correct ordering is known.
- **The two judges** are Qwen3-VL-4B-Instruct (J1, the main evaluator, which also reads charts) and Phi-4-mini-instruct (J2, text only). Each judged every variant under three prompts: plain, holistic with the specification, and the CO-STAR analytic rubric.
- **17 automatic metrics** were computed as baselines: overlap, embedding, generative, inference-based and reference-free.
- **Further experiments** were:
  - charts judged without the answer key;
  - side-by-side judgments in both orders;
  - a reworded rubric and three sampled runs;
  - two generators (Qwen3-VL-2B-Instruct and SmolVLM2-2.2B-Instruct) answering all 160 prompts, with their replies judged by both judges and checked with rule-based checks.
- **How it ran:** all models were openly licensed four-bit GGUF files run through llama.cpp on a two-core CPU without a GPU. Decoding was deterministic and judge outputs were grammar-constrained. The study made 4,720 logged calls in about 11.9 hours, and all 4,400 judgments were valid at the first attempt.

## Repository layout

| Folder | Contents | Thesis |
|---|---|---|
| `study/` | Main study: dataset, chart images, all code, and `results/` with the complete call logs and statistics | Chapters 3–4, Appendices A, D, E |
| `pilot/` | Pilot study (32 development items and 16 held-out items): code, data, complete logs, and the early prototype pipeline in `pilot/src/` | Section 3.2 |
| `figures/` | Every figure of the thesis (PNG) | All chapters |
| `tables/` | The Chapter 4 result tables (Markdown), generated from `summary_v2.json` | Chapter 4 |
| `data_exports/` | The 160 items as flat CSV files, for use without Python | Appendix A |
| `tools/` | Table builder, diagram script, CSV exporter | — |
| `docs/` | Guides to the thesis, files, models, reproduction and history (listed below) | — |

### Documentation

- [`DATASET_CARD.md`](DATASET_CARD.md): what the Golden Dataset is, how it was built, intended uses and limitations.
- [`docs/THESIS_MAP.md`](docs/THESIS_MAP.md): which file produces each table and figure in the thesis.
- [`docs/CODEBOOK.md`](docs/CODEBOOK.md): the fields of every data and log file.
- [`docs/MODELS.md`](docs/MODELS.md): the model files, checksums, metric models and run settings.
- [`docs/REPRODUCING.md`](docs/REPRODUCING.md): how to re-run the analysis or the whole study.
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md): pilot, freeze, items written after the freeze, carried-over calls and the discarded run.

## Quick start

Load the dataset:
```python
import json
items = json.load(open("study/golden_dataset_v2.json"))
print(items[0]["prompt"], items[0]["candidates"]["B"])
```

Reproduce all statistics from the logs. This needs no language models and takes a few minutes on a CPU:
```bash
pip install -r requirements.txt
cd study && python analyze_v2.py      # rewrites results/summary_v2.json
cd .. && python tools/tables_ch4.py   # rewrites tables/*.md
```

Re-running the models themselves is described in [`docs/REPRODUCING.md`](docs/REPRODUCING.md).

## Related articles

Two journal manuscripts draw on this thesis:

- **Contrast-set results:** "Pragmatic failure and the limits of automatic evaluation: Reference-based metrics and open-source LLM judges on linguistic contrast sets". Data repository: `pragmatic-failure-contrast-sets`.
- **Generator study:** "Do Validated LLM Judges Transfer to Real Chatbot Replies?". Data repository: `llm-judge-transfer-chatbots`.

## Content note

Some designed C variants deliberately contain condescension, slang or a cultural stereotype, as examples of sociopragmatic failure. Do not use them as generation or training targets.

## Licence and citation

- **Data** (items, responses, chart images, logs, tables, figures): [CC BY 4.0](LICENSE-DATA).
- **Code:** [MIT](LICENSE).
- **Citation:** see [`CITATION.cff`](CITATION.cff).
