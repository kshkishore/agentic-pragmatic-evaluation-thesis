# -*- coding: utf-8 -*-
"""CO-STAR prompt templates for the two agents.

CO-STAR (Context, Objective, Style, Tone, Audience, Response) is used twice:
  1. to describe each communicative situation in the Golden Dataset (and, in the 'costar' condition,
     to prompt the Generator), and
  2. to structure the standing instructions of the Linguistic Evaluator, whose rubric has one criterion per field.
"""
from langchain_core.prompts import ChatPromptTemplate

GENERATOR_SYSTEM = "You are a helpful assistant."

# Condition 'costar': the Generator sees all six fields.
GENERATOR_COSTAR = """# CONTEXT #
{context}

# OBJECTIVE #
{objective}

# STYLE #
{style}

# TONE #
{tone}

# AUDIENCE #
{audience}

# RESPONSE #
{response} Write only the reply itself, with no preamble or commentary.

# MESSAGE #
{user_turn}"""

# Condition 'bare': the Generator sees only the situation and the message; style, tone, audience and
# format have to be inferred, as they would be from an ordinary unstructured prompt.
GENERATOR_BARE = """{context}

{user_turn}"""

CRITERIA_TEXT = {
    "C": "C  Context: the reply is consistent with the facts given in the Context and with the attached image if there is one. Nothing is contradicted or invented.",
    "O": "O  Objective: the reply does what the Objective asks and performs the communicative act the user intends. Idioms, sarcasm, hints and indirect requests are read as intended, not literally. A reply that only describes or restates, when advice, an answer or an action was wanted, fails.",
    "S": "S  Style: the wording and register match the Style field (for example formal or casual, technical or plain).",
    "T": "T  Tone: the attitude shown towards the addressee matches the Tone field (for example warm, respectful, apologetic, calm).",
    "A": "A  Audience: the content, amount of detail and vocabulary suit the person named in the Audience field (their knowledge, status, needs and relationship to the writer).",
    "R": "R  Response: the reply obeys the Response field (length, number of sentences, layout).",
}

JUDGE_SYSTEM = """# CONTEXT #
You are the Linguistic Evaluator in an automated evaluation pipeline. You are shown a communicative situation described by six fields (Context, Objective, Style, Tone, Audience, Response), the message a user sent in that situation, sometimes an image the user attached, and a candidate reply written by another AI system.

# OBJECTIVE #
Rate how well the candidate reply fits the situation on six criteria, one for each field. Rate pragmatic appropriateness only. Do not reward length. Do not rate grammar or spelling.

# STYLE #
Analytical and exact, like an applied linguist coding data with a rubric.

# TONE #
Neutral and strict. Do not give the benefit of the doubt.

# AUDIENCE #
A computer program that will parse your output. No human will read it.

# RESPONSE #
Return one JSON object. First "evidence": one sentence of at most 30 words naming the most important strength or failure of the reply. Then the six ratings {keys}, each an integer from 1 to 5.

RUBRIC
5 = fully appropriate, 4 = minor lapse, 3 = partly appropriate, 2 = mostly inappropriate, 1 = clearly inappropriate.
{criteria}
Rate each criterion independently: a reply can fail one criterion and pass the others."""

JUDGE_USER = """SITUATION
Context: {context}
Objective: {objective}
Style: {style}
Tone: {tone}
Audience: {audience}
Response: {response}
{image_note}
USER MESSAGE
{user_turn}

CANDIDATE REPLY
<<<
{candidate}
>>>"""


def judge_system(order):
    """order: sequence of criterion letters; the rubric lists them, and the output schema emits them, in this order."""
    return JUDGE_SYSTEM.format(keys=", ".join('"%s"' % k for k in order),
                               criteria="\n".join(CRITERIA_TEXT[k] for k in order))


def judge_schema(order):
    props = {"evidence": {"type": "string", "maxLength": 240}}
    props.update({k: {"type": "integer", "enum": [1, 2, 3, 4, 5]} for k in order})
    return {"type": "object", "properties": props, "required": ["evidence"] + list(order), "additionalProperties": False}


generator_prompt = {
    "costar": ChatPromptTemplate.from_messages([("system", GENERATOR_SYSTEM), ("human", GENERATOR_COSTAR)]),
    "bare": ChatPromptTemplate.from_messages([("system", GENERATOR_SYSTEM), ("human", GENERATOR_BARE)]),
}
