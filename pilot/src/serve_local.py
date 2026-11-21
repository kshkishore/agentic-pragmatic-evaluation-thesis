# -*- coding: utf-8 -*-
"""Launcher for the llama-cpp-python OpenAI-compatible server with one adjustment:
chat messages are normalised to the shape each model's own chat template expects, so that one client
message format (OpenAI style: text and image_url parts) works for every model family.
With PILOT_TEXT_FAST_PATH=1, requests without images are routed through the model's standard text chat
handler, which re-uses the cached prompt prefix (the fixed rubric) between consecutive calls.
Usage: python serve_local.py <normal llama_cpp.server arguments>"""
import os
import llama_cpp.llama_chat_format as lcf

_Base = lcf.MTMDChatHandler


class NormalisingMTMD(_Base):
    def _mode(self, llama):
        tpl = self._get_chat_template(llama)
        if "message['content'][0]" in tpl:
            return "list"            # template iterates over content parts (SmolVLM2)
        if "is string" in tpl:
            return "flex"            # template accepts strings and part lists (Qwen3-VL, Gemma 3)
        return "string"              # template concatenates content as a string (InternVL3)

    def _normalise(self, messages, llama, marker=None):
        mode, out = self._mode(llama), []
        for m in messages:
            m = dict(m)
            c = m.get("content")
            parts = [{"type": "text", "text": c}] if isinstance(c, str) else list(c or [])
            if marker is not None:
                parts = [self._convert_content_part_for_template(p, marker) for p in parts]
            if mode == "list":
                m["content"] = parts
            elif mode == "string" or (mode == "flex" and isinstance(c, str)):
                m["content"] = "\n".join(p["text"] for p in parts if p.get("type") == "text")
            else:
                m["content"] = parts
            out.append(m)
        return out

    def _get_template_messages(self, messages, media_marker):
        return self._normalise(messages, self._llama_ref, media_marker)

    def __call__(self, *, llama, messages, **kwargs):
        self._llama_ref = llama
        if os.environ.get("PILOT_TEXT_FAST_PATH") == "1" and not self.get_image_urls(messages):
            text_handler = llama._chat_handlers.get("chat_template.default")
            if text_handler is not None:
                return text_handler(llama=llama, messages=self._normalise(messages, llama), **kwargs)
        return super().__call__(llama=llama, messages=messages, **kwargs)


lcf.MTMDChatHandler = NormalisingMTMD

if __name__ == "__main__":
    from llama_cpp.server.__main__ import main
    main()
