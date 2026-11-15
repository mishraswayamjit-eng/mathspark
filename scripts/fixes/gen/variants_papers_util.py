"""Shared helpers for the variants-papers rules."""
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))
from check import answer_numbers, correct_text, numbers_in  # noqa: E402


class Skip(Exception):
    """The wording matched, but the question should be left alone and reported."""


def text_of(q):
    return q["questionText"].strip()


def step_texts(q):
    return [s.get("text", "") for s in q.get("stepByStep") or []]


def last_latex(q):
    steps = q.get("stepByStep") or []
    return steps[-1].get("latex", "") if steps else ""


def make_steps(q, texts):
    """Steps from plain texts; the last keeps the latex of the old last step (the boxed answer)."""
    steps = [{"text": t, "latex": ""} for t in texts]
    steps[-1]["latex"] = last_latex(q)
    return steps


def need_key(q, value):
    """Stop if the keyed choice is not the value worked out here."""
    key = correct_text(q).strip()
    if isinstance(value, str):
        ok = key == value
    else:
        ok = numbers_in(key) == {Fraction(value)} and not key.startswith(("-", "−"))
    if not ok:
        raise Skip("worked out %s but the key says %r" % (value, key))


def pick(q, candidates, avoid=()):
    """The first candidate text that names no number of the answer and none of `avoid`."""
    blocked = set(answer_numbers(q)) | {Fraction(a) for a in avoid}
    for c in candidates:
        if not (numbers_in(c) & blocked):
            return c
    raise Skip("no example avoids the answer")


def listing(items):
    items = [str(i) for i in items]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def prime_factors(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out


def matches(q, pattern):
    return re.fullmatch(pattern, text_of(q))
