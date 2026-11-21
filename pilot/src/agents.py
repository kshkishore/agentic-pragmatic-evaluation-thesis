# -*- coding: utf-8 -*-
"""The two agents of the pipeline, written as LangChain runnables.

GeneratorAgent  - the subject model. Produces a reply to a Golden Dataset item.
EvaluatorAgent  - the Linguistic Evaluator (LLM-as-a-judge). Rates a reply on the six CO-STAR criteria.
                  Output is grammar-constrained to a JSON schema and validated with Pydantic;
                  a reply that fails validation is re-requested (at most twice)."""
import os, time
from typing import Literal
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.runnables import RunnableLambda
import config as cfg, llm, prompts

Score = Literal[1, 2, 3, 4, 5]


class Verdict(BaseModel):
    evidence: str = Field(max_length=400)
    C: Score
    O: Score
    S: Score
    T: Score
    A: Score
    R: Score


def _with_image(text, item):
    """Human message for an item: text only, or image followed by text."""
    if item.get("image"):
        return HumanMessage([llm.image_part(os.path.join(cfg.DATA, item["image"])), {"type": "text", "text": text}])
    return HumanMessage(text)


class GeneratorAgent:
    def __init__(self, model_key, base_url, condition, max_tokens=200):
        self.model_key, self.condition = model_key, condition
        self.template = prompts.generator_prompt[condition]
        self.chain = llm.chat(model_key, base_url, max_tokens) | StrOutputParser()

    def __call__(self, item):
        msgs = self.template.format_messages(user_turn=item["user_turn"], **item["costar"])
        messages = [msgs[0], _with_image(msgs[1].content, item)]
        t = time.time()
        text = self.chain.invoke(messages).strip()
        return {"text": text, "seconds": round(time.time() - t, 2)}


class EvaluatorAgent:
    def __init__(self, model_key, base_url, order=cfg.CRITERIA, max_tokens=160):
        self.model_key, self.order = model_key, list(order)
        self.system = SystemMessage(prompts.judge_system(self.order))
        parser = PydanticOutputParser(pydantic_object=Verdict)
        model = llm.chat(model_key, base_url, max_tokens, json_schema=prompts.judge_schema(self.order))
        self.chain = (model | parser).with_retry(stop_after_attempt=3)
        self.build = RunnableLambda(self._messages)

    def _messages(self, x):
        item, candidate = x["item"], x["candidate"]
        note = "An image is attached to the user message; use it to check the reply.\n" if item.get("image") else ""
        text = prompts.JUDGE_USER.format(user_turn=item["user_turn"], candidate=candidate, image_note=note, **item["costar"])
        return [self.system, _with_image(text, item)]

    def __call__(self, item, candidate):
        t = time.time()
        v = (self.build | self.chain).invoke({"item": item, "candidate": candidate})
        return {"evidence": v.evidence, **{k: getattr(v, k) for k in cfg.CRITERIA}, "seconds": round(time.time() - t, 2)}
