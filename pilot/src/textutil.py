# -*- coding: utf-8 -*-
"""Small deterministic text utilities shared by the dataset checks, the format tool and f_syntax."""
import re

_ABBR = r"\b(?:Mr|Mrs|Ms|Dr|Prof|St|vs|e\.g|i\.e|a\.m|p\.m|approx|No)\."


def strip_subject(text):
    return re.sub(r"^\s*Subject:.*?(?:\n+|$)", "", text, count=1, flags=re.I)


def is_list(text):
    """True when at least two lines open with a bullet or an enumerator."""
    return len(re.findall(r"(?m)^\s*(?:[-*\u2022]|\d+[.)])\s+\S", text)) >= 2


def sentences(text):
    """Split into sentences; every non-empty line of a list or line-broken text counts separately."""
    text = strip_subject(text)
    out = []
    for line in [l.strip() for l in text.split("\n") if l.strip()]:
        line = re.sub(r"^\s*(?:[-*\u2022]|\d+[.)])\s+", "", line)
        protected = re.sub(_ABBR, lambda m: m.group(0).replace(".", "\u2024"), line)
        protected = re.sub(r"(\d)\.(\d)", "\\1\u2024\\2", protected)
        parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])", protected)
        out += [p.replace("\u2024", ".").strip() for p in parts if p.strip()]
    return out


def words(text):
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'%.,-]*", text)


def check_format(text, rule):
    """Deterministic check of a reply against a machine-readable format rule.
    Returns (ok, list_of_violations). rule keys: sent_min, sent_max, max_chars, max_words, no_list, subject_line."""
    if not rule:
        return None, []
    v = []
    n = len(sentences(text))
    if "sent_min" in rule and n < rule["sent_min"]:
        v.append(f"{n} sentences < {rule['sent_min']}")
    if "sent_max" in rule and n > rule["sent_max"]:
        v.append(f"{n} sentences > {rule['sent_max']}")
    if "max_chars" in rule and len(text) > rule["max_chars"]:
        v.append(f"{len(text)} characters > {rule['max_chars']}")
    if "max_words" in rule and len(words(text)) > rule["max_words"]:
        v.append(f"{len(words(text))} words > {rule['max_words']}")
    if rule.get("no_list") and is_list(text):
        v.append("list layout")
    if rule.get("subject_line") and not re.match(r"\s*Subject:", text, flags=re.I):
        v.append("no subject line")
    return (len(v) == 0), v
