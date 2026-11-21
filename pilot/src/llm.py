# -*- coding: utf-8 -*-
"""Local model serving. Each model is exposed through an OpenAI-compatible endpoint (llama-cpp-python server),
so the same client code works unchanged against Ollama, vLLM or llama.cpp's own server."""
import base64, contextlib, os, subprocess, sys, time, urllib.request
from langchain_openai import ChatOpenAI
import config as cfg


@contextlib.contextmanager
def serve(model_key, log_dir=None, text_fast_path=False):
    """Start a local server for one model, yield its base URL, and shut it down afterwards."""
    m = cfg.MODELS[model_key]
    env = dict(os.environ, PILOT_TEXT_FAST_PATH="1" if text_fast_path else "0")
    cmd = [sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "serve_local.py"),
           "--model", os.path.join(cfg.MODELS_DIR, m["gguf"]),
           "--clip_model_path", os.path.join(cfg.MODELS_DIR, m["mmproj"]), "--chat_format", "mtmd",
           "--model_alias", model_key, "--n_ctx", str(cfg.N_CTX), "--n_threads", str(cfg.N_THREADS),
           "--n_batch", "512", "--seed", str(cfg.SEED), "--port", str(cfg.PORT), "--host", "127.0.0.1"]
    log = open(os.path.join(log_dir or cfg.RESULTS, f"server_{model_key}.log"), "a")
    proc = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT, env=env)
    url = f"http://127.0.0.1:{cfg.PORT}/v1"
    try:
        for _ in range(240):
            if proc.poll() is not None:
                raise RuntimeError(f"server for {model_key} exited; see log")
            try:
                urllib.request.urlopen(url + "/models", timeout=2).read()
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError("server did not start")
        yield url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=20)
        except subprocess.TimeoutExpired:
            proc.kill()
        log.close()
        time.sleep(1)


def chat(model_key, base_url, max_tokens, json_schema=None):
    """LangChain chat model bound to the local endpoint. Greedy decoding (temperature 0) and a fixed seed."""
    kwargs = {}
    if json_schema is not None:  # grammar-constrained decoding: output must parse against the schema
        kwargs["response_format"] = {"type": "json_object", "schema": json_schema}
    return ChatOpenAI(model=model_key, base_url=base_url, api_key="local", temperature=0.0, seed=cfg.SEED,
                      max_tokens=max_tokens, timeout=900, max_retries=1, model_kwargs=kwargs,
                      extra_body={"repeat_penalty": 1.0})  # plain greedy decoding, no repetition penalty


def image_part(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}}
