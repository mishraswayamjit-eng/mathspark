"""Shared helpers for generated_hints.py: number formatting, plurals, and choosing a worked example."""
import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from check import numbers_in  # noqa: E402


class Skip(Exception):
    """This question cannot be given hints by rule; the message says why."""


def fmt(value):
    """A number as a child would write it: 12, 7.5."""
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    text = ("%.3f" % float(value)).rstrip("0").rstrip(".")
    if Fraction(text) != value:
        raise Skip("number %s has no short decimal form" % value)
    return text


def frac(value):
    """A fraction in lowest terms as text: 3/4, or 2 for a whole number."""
    value = Fraction(value)
    return str(value.numerator) if value.denominator == 1 else "%d/%d" % (value.numerator, value.denominator)


def plural(n, word, many=None):
    return "%s %s" % (n, word if n == 1 else (many or word + "s"))


def factors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def lcm(a, b):
    return a * b // math.gcd(a, b)


def nums(*values):
    return {Fraction(v) for v in values}


class Example:
    """A candidate worked example: the hint text, and the numbers that matter in it."""

    def __init__(self, text, key):
        self.text = text
        self.key = nums(*key)
        self.all = numbers_in(text)


def pick(cands, question, options, answer, giveaway):
    """The first example (in the fixed order given) that shares the fewest numbers with the question.

    Tier 1: its key numbers appear nowhere in the question or in any answer choice.
    Tier 2: its key numbers appear nowhere in the question or in the correct choice.
    Tier 3: its key numbers avoid the correct choice, and it shares at most one number with the question.
    An example whose text contains a number the checker treats as the answer is never used.
    Returns (example, tier), or (None, 0).
    """
    usable = [c for c in cands if not (c.all & giveaway)]
    for c in usable:
        if not (c.key & (question | options | answer)):
            return c, 1
    for c in usable:
        if not (c.key & (question | answer)):
            return c, 2
    for c in usable:
        if not (c.key & answer) and len(c.key & question) <= 1:
            return c, 3
    return None, 0
