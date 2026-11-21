# Models and run settings

## Language models (thesis Table D.1)

All models are openly licensed and were run as four-bit GGUF files through llama.cpp (`llama-cpp-python==0.3.36`). Vision projectors are eight-bit.

| Role | Model | Licence | File | SHA-256 |
|---|---|---|---|---|
| Judge J1 | Qwen3-VL-4B-Instruct | Apache-2.0 | `Qwen3VL-4B-Instruct-Q4_K_M.gguf` (2.50 GB) | `66358cb18bb6b3b1b6675aa412c7a88ef01d228f481184d13668e5201c730a0a` |
| | vision projector | | `mmproj-Qwen3VL-4B-Instruct-Q8_0.gguf` (0.45 GB) | `30ba2c7dd3127a4561b6cba9d13d0f711c91bdb38742e2f56d73c8cb596bd06d` |
| Judge J2 | Phi-4-mini-instruct | MIT | `microsoft_Phi-4-mini-instruct-Q4_K_M.gguf` (2.49 GB) | `01999f17c39cc3074afae5e9c539bc82d45f2dd7faa3917c66cbef76fce8c0c2` |
| Generator G1 | Qwen3-VL-2B-Instruct | Apache-2.0 | `Qwen3VL-2B-Instruct-Q4_K_M.gguf` (1.11 GB) | `089d75c52f4b7ffc56ba998ffc50aae89fcafc755f9e7208aacca281dca6c2ae` |
| | vision projector | | `mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf` (0.45 GB) | `f9a68fabba69c3b81e153367b2c7521030b0fa8bb0de400c9599c8e6725f9c82` |
| Generator G2 | SmolVLM2-2.2B-Instruct | Apache-2.0 | `SmolVLM2-2.2B-Instruct-Q4_K_M.gguf` (1.11 GB) | `0cf76814555b8665149075b74ab6b5c1d428ea1d3d01c1918c12012e8d7c9f58` |
| | vision projector | | `mmproj-SmolVLM2-2.2B-Instruct-Q8_0.gguf` (0.59 GB) | `ae07ea1facd07dd3230c4483b63e8cda96c6944ad2481f33d531f79e892dd024` |

**Where to download:**
- The Qwen files come from the Hugging Face repositories `Qwen/Qwen3-VL-4B-Instruct-GGUF` and `Qwen/Qwen3-VL-2B-Instruct-GGUF`.
- The SmolVLM2 files come from `ggml-org/SmolVLM2-2.2B-Instruct-GGUF`.
- Download Phi-4-mini-instruct from any GGUF repository that offers a file with the name and checksum above.

Always check the file against `study/results/sha256.json` before use. A different file can give different outputs.

The checksums are also in `study/results/sha256.json`. The model registry is `MODEL_REGISTRY` in `study/pipeline.py`.

## Metric models (thesis Table D.2)

| Hugging Face model | Used for | Revision (first 12 hex digits) |
|---|---|---|
| `textattack/roberta-base-CoLA` | f_syntax | `3ccf3a400f2f`, `dc430df56cf8` |
| `roberta-large` | BERTScore | `722cf37b1afa` |
| `sentence-transformers/all-mpnet-base-v2` | Sentence-BERT | `e8c3b32edf54` |
| `facebook/bart-large-cnn` | BARTScore | `37f520fa929c` |
| `FacebookAI/roberta-large-mnli` | NLI scores | `2a8f12d27941` |
| `openai-community/gpt2` | Perplexity | `607a30d783df` |
| `openai/clip-vit-base-patch32` | CLIPScore | `3d74acf9a28c`, `c237dc49a33f` |

## Run settings

- **Context and hardware:** context window 4,096 tokens, `n_threads=2`, `n_batch=512`, on a CPU only, with two virtual cores and 8 GB of memory.
- **Decoding:** greedy (temperature 0) with seed `20261109`. The sampled robustness runs are the exception: temperature 0.7 with seeds 101, 202 and 303.
- **Output constraints:** every judge output was constrained by a GBNF grammar, defined in `study/pipeline.py`:
  - rubric conditions return a JSON object with a diagnosis of 8–140 characters and six integers from 1 to 5;
  - holistic and plain conditions return one integer from 1 to 10;
  - side-by-side judgments return `{"better": 1|2}`.
- **Generators:** system prompt "You are a helpful assistant.", greedy decoding, at most 180 output tokens, no specification.
- **Statistics:** bootstrap resampling over items, 10,000 resamples, seed `20261109`.
