Table 4.12: Scores of the two generators on the 160 prompts (means; paired Wilcoxon signed-rank tests and Cliff's delta; agreement: share of prompts on which a measure prefers the same generator as J1 among those on which neither is tied)

| Measure | G1 | G2 | G1 higher | G2 higher | p | Cliff's delta | Agreement with J1 |
|---|---|---|---|---|---|---|---|
| J1 $f_{pragmatics}$ | 0.83 | 0.64 | 110 | 26 | < .001 | 0.51 |  |
| J1 gated score | 0.58 | 0.42 | 82 | 33 | < .001 | 0.24 |  |
| J1 with rule-based format check (exploratory) | 0.82 | 0.63 | 110 | 28 | < .001 | 0.50 |  |
| J2 $f_{pragmatics}$ (text prompts) | 0.95 | 0.94 | 42 | 32 | .648 | 0.04 | 0.62 (n = 69) |
| $M_{eval}$ | 0.85 | 0.70 | 120 | 35 | < .001 | 0.51 |  |
| $f_{syntax}$ | 0.94 | 0.94 | 84 | 71 | .305 | 0.08 | 0.57 (n = 136) |
| BLEU | 10.1 | 5.4 | 99 | 55 | < .001 | 0.27 | 0.74 (n = 135) |
| chrF | 35.2 | 30.6 | 91 | 63 | .002 | 0.16 | 0.60 (n = 135) |
| ROUGE-L | 31.9 | 23.6 | 116 | 37 | < .001 | 0.31 | 0.77 (n = 134) |
| BERTScore F1 | 90.1 | 88.4 | 112 | 43 | < .001 | 0.34 | 0.74 (n = 136) |
| SBERT cosine | 72.6 | 65.2 | 109 | 46 | < .001 | 0.24 | 0.65 (n = 136) |
| Bidirectional NLI | 26.8 | 22.6 | 77 | 78 | .245 | 0.01 | 0.54 (n = 136) |
| BARTScore | -2.66 | -2.80 | 83 | 72 | .067 | 0.08 | 0.52 (n = 136) |
| GPT-2 perplexity, median (lower is better) | 28.2 | 16.9 | 119 | 36 | < .001 | 0.35 |  |
| Length in words | 34.0 | 67.7 | 31 | 122 | < .001 | -0.38 | 0.81 (shorter preferred; n = 134) |
