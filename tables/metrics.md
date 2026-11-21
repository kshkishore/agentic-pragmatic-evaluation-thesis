Table 4.2: Pairwise accuracy of the automatic metrics and of the CO-STAR evaluator on the 320 contrasts (95% bootstrap confidence intervals for all contrasts; p: exact McNemar test against J1 CO-STAR on strict correctness, Holm-adjusted)

| Metric | Family | A-B | A-C | All contrasts | p |
|---|---|---|---|---|---|
| BLEU | N-gram overlap | 0.00 | 0.88 | 0.44 [0.42, 0.47] | < .001 |
| chrF | N-gram overlap | 0.01 | 0.89 | 0.45 [0.42, 0.47] | < .001 |
| ROUGE-1 | N-gram overlap | 0.01 | 0.86 | 0.43 [0.41, 0.46] | < .001 |
| ROUGE-2 | N-gram overlap | 0.00 | 0.73 | 0.37 [0.34, 0.40] | < .001 |
| ROUGE-L | N-gram overlap | 0.01 | 0.81 | 0.41 [0.38, 0.44] | < .001 |
| METEOR | N-gram overlap | 0.02 | 0.89 | 0.46 [0.43, 0.48] | < .001 |
| TER | Edit distance | 0.03 | 0.71 | 0.37 [0.34, 0.41] | < .001 |
| BERTScore | Embedding | 0.06 | 0.94 | 0.50 [0.47, 0.53] | < .001 |
| Sentence-BERT | Embedding | 0.21 | 0.88 | 0.54 [0.50, 0.58] | < .001 |
| BARTScore | Generative | 0.05 | 0.89 | 0.47 [0.44, 0.50] | < .001 |
| NLI entailment | Inference | 0.89 | 0.80 | 0.84 [0.80, 0.89] | .090 |
| NLI bidirectional | Inference | 0.88 | 0.87 | 0.88 [0.83, 0.92] | .370 |
| NLI entailment minus contradiction | Inference | 0.93 | 0.80 | 0.87 [0.83, 0.90] | .370 |
| GPT-2 perplexity | Reference-free | 0.33 | 0.68 | 0.50 [0.44, 0.56] | < .001 |
| Flesch Reading Ease | Reference-free | 0.45 | 0.43 | 0.44 [0.38, 0.50] | < .001 |
| Length (words) | Reference-free | 0.31 | 0.85 | 0.58 [0.54, 0.62] | < .001 |
| f_syntax (CoLA) | Reference-free | 0.49 | 0.62 | 0.56 [0.49, 0.62] | < .001 |
| CLIPScore (charts only, 32 contrasts) | Image-text | 0.25 | 0.81 | 0.53 [0.38, 0.69] | |
| **J1 CO-STAR evaluator** | LLM judge | **0.91** | **0.93** | **0.92 [0.88, 0.95]** | |
