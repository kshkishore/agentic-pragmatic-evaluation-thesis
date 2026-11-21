# -*- coding: utf-8 -*-
"""Model registry and run settings for the pilot. All weights are 4-bit (Q4_K_M) GGUF files served locally."""
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT, "models")
DATA = os.path.join(ROOT, "data")
RESULTS = os.path.join(ROOT, "results")
PORT = 8765
SEED = 7
N_CTX = 4096
N_THREADS = 2

MODELS = {
    # Linguistic Evaluator (judge) and a smaller sibling used for the inter-judge check
    "qwen3-vl-4b": dict(role="judge", name="Qwen3-VL-4B-Instruct", developer="Alibaba Cloud (Qwen)", licence="Apache-2.0",
                        repo="Qwen/Qwen3-VL-4B-Instruct-GGUF", gguf="Qwen3VL-4B-Instruct-Q4_K_M.gguf",
                        mmproj="mmproj-Qwen3VL-4B-Instruct-Q8_0.gguf"),
    "qwen3-vl-2b": dict(role="judge-2", name="Qwen3-VL-2B-Instruct", developer="Alibaba Cloud (Qwen)", licence="Apache-2.0",
                        repo="Qwen/Qwen3-VL-2B-Instruct-GGUF", gguf="Qwen3VL-2B-Instruct-Q4_K_M.gguf",
                        mmproj="mmproj-Qwen3VL-2B-Instruct-Q8_0.gguf"),
    # Generators (the subjects of the evaluation)
    "smolvlm2-2.2b": dict(role="generator", name="SmolVLM2-2.2B-Instruct", developer="Hugging Face", licence="Apache-2.0",
                          repo="ggml-org/SmolVLM2-2.2B-Instruct-GGUF", gguf="SmolVLM2-2.2B-Instruct-Q4_K_M.gguf",
                          mmproj="mmproj-SmolVLM2-2.2B-Instruct-Q8_0.gguf"),
    "internvl3-2b": dict(role="generator", name="InternVL3-2B-Instruct", developer="OpenGVLab", licence="Apache-2.0",
                         repo="ggml-org/InternVL3-2B-Instruct-GGUF", gguf="InternVL3-2B-Instruct-Q4_K_M.gguf",
                         mmproj="mmproj-InternVL3-2B-Instruct-Q8_0.gguf"),
    "gemma-3-4b": dict(role="generator", name="Gemma 3 4B (instruction-tuned)", developer="Google DeepMind", licence="Gemma Terms of Use",
                       repo="ggml-org/gemma-3-4b-it-GGUF", gguf="gemma-3-4b-it-Q4_K_M.gguf",
                       mmproj="mmproj-gemma-3-4b-it-f16.gguf"),
}
GENERATORS = [k for k, v in MODELS.items() if v["role"] == "generator"]
JUDGE, JUDGE_2 = "qwen3-vl-4b", "qwen3-vl-2b"
CRITERIA = ["C", "O", "S", "T", "A", "R"]
