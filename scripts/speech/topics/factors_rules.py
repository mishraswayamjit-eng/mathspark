"""Notation rules for the factors topic (HCF, LCM, factors, multiples, primes, divisibility).

`say(text)` is the general converter. `generated(q, src)` narrates the regular generated
families, whose wording is known exactly. One-off questions are hand-written in factors_fp.py
and factors_ws*.py; whatever they leave out falls back to `say`.
"""
import os
import re
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")))
from common import speak  # noqa: E402

_POWERS = {"¹": " to the power of one", "²": " squared", "³": " cubed", "⁴": " to the power of four",
           "⁵": " to the power of five", "⁶": " to the power of six"}


def and_list(text):
    """'1, 2, 7, 14' -> '1, 2, 7 and 14'. A list of one is left alone."""
    items = [p.strip() for p in text.split(",") if p.strip()]
    if len(items) < 2:
        return text.strip()
    return ", ".join(items[:-1]) + " and " + items[-1]


def _tidy(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r"([.,:;])\1+", r"\1", s)
    s = re.sub(r",\.", ".", s)
    return s


def _abbr(s):
    """HCF and LCM, said as letters."""
    s = re.sub(r"H\.\s*C\.\s*F\.?", "HCF", s)
    s = re.sub(r"L\.\s*C\.\s*M\.?", "LCM", s)

    def of(m):
        return "the %s of %s" % (m.group(1), and_list(m.group(2)))
    s = re.sub(r"\b(HCF|LCM)\s*\(([^)]*)\)", of, s)
    s = re.sub(r"\bHCF\b", "H C F", s)
    s = re.sub(r"\bLCM\b", "L C M", s)
    return s


def say(text):
    """General converter: good enough for plain sentences, a first draft for working."""
    s = text or ""
    if not s.strip():
        return ""
    s = _abbr(s)
    for k, v in _POWERS.items():
        s = s.replace(k, v)
    s = s.replace("✻", " star ").replace("…", " and so on ")
    s = re.sub(r"(\d)\.\.\.+", r"\1 and so on", s)
    s = re.sub(r"\.\.\.+", " ", s)
    s = s.replace("✓", " ").replace("✗", " ")
    s = s.replace("→", ", which gives ").replace("±", " plus or minus ")
    s = re.sub(r"(\d)-digit", r"\1 digit", s)
    s = re.sub(r"\bQ(\d+)\b", r"question \1", s)
    s = re.sub(r"(\d)\s*[–—]\s*(\d)", r"\1 to \2", s)
    s = re.sub(r"(^|[\s(])[-−](\d)", r"\1minus \2", s)
    s = re.sub(r"(\d)([a-zA-Z])\b", r"\1 \2", s)
    s = speak(s)
    s = s.replace("(", ", ").replace(")", ", ").replace("—", ", ")
    s = re.sub(r"\s*,\s*", ", ", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"(, )+", ", ", s)
    s = re.sub(r"^[,\s]+|[,\s]+$", "", s)
    return _tidy(s)


def option(text):
    t = text.strip()
    m = re.fullmatch(r"[-−](\d+)", t)
    if m:
        return "minus " + m.group(1)
    return say(t)


# ── The generated families: wording is regular, so each line is written out exactly ──

_N = r"(\d+)"
_LIST = r"(\d+(?:, \d+)*)"

_FIXED = {
    "Find the largest number that divides both.": "Find the largest number that divides both.",
    "Try dividing both by small primes.": "Try dividing both by small primes.",
    "Read the question carefully and identify what's being asked.": "Read the question carefully, and identify what is being asked.",
    "Try working step by step.": "Try working step by step.",
    "Check your answer by substituting back.": "Check your answer by substituting back.",
    "Use: LCM = (a×b) ÷ HCF(a,b).": "Use this rule: the L C M equals A times B, divided by the H C F of A and B.",
    "Only one of these gives a remainder of 0.": "Only one of these gives a remainder of 0.",
    "Move the constant to the other side first.": "Move the constant to the other side first.",
    "After that, divide both sides by the coefficient of x.": "After that, divide both sides by the coefficient of x.",
}

# (pattern, template). In a template, {1}, {2}... are the groups; {L1} is group 1 read as a list.
_PATTERNS = [
    (r"Find the (HCF|LCM) of %s and %s\." % (_N, _N), "Find the {A1} of {2} and {3}."),
    (r"Which of the following numbers is divisible by %s\?" % _N, "Which of the following numbers is divisible by {1}?"),
    (r"Solve: %sx ([−+-]) %s = %s" % (_N, _N, _N), "Solve: {1} x {S2} {3} equals {4}."),
    # hints
    (r"List the factors of %s and %s\." % (_N, _N), "List the factors of {1} and {2}."),
    (r"LCM is the smallest number divisible by both %s and %s\." % (_N, _N), "The L C M is the smallest number divisible by both {1} and {2}."),
    (r"First find HCF of %s and %s\." % (_N, _N), "First find the H C F of {1} and {2}."),
    (r"A number is divisible by %s if it divides exactly with no remainder\." % _N, "A number is divisible by {1} if it divides exactly, with no remainder."),
    (r"Try dividing each option by %s\." % _N, "Try dividing each option by {1}."),
    (r"When you move [−-]%s to the right side, it becomes \+%s\." % (_N, _N), "When you move minus {1} to the right side, it becomes plus {2}."),
    (r"First, move %s to the other side by subtracting it from both sides\." % _N, "First, move {1} to the other side, by subtracting it from both sides."),
    (r"After subtracting: %sx = %s\. Now divide both sides by %s\." % (_N, _N, _N), "After subtracting, {1} x equals {2}. Now divide both sides by {3}."),
    (r"Think: %s times what number gives %s\?" % (_N, _N), "Think: {1} times what number gives {2}?"),
    # steps written with the question
    (r"Find factors of %s and %s\." % (_N, _N), "Find the factors of {1} and {2}."),
    (r"HCF = %s" % _N, "The H C F is {1}."),
    (r"LCM × HCF = %s × %s = %s" % (_N, _N, _N), "L C M times H C F equals {1} times {2}, which is {3}."),
    (r"HCF\(%s,%s\) = %s, so LCM = %s ÷ %s = %s" % (_N, _N, _N, _N, _N, _N),
     "The H C F of {1} and {2} is {3}. So the L C M is {4} divided by {5}, which is {6}."),
    (r"Check each number for divisibility by %s\." % _N, "Check each number for divisibility by {1}."),
    (r"%s ÷ %s = %s \(exact division\)" % (_N, _N, _N), "{1} divided by {2} equals {3}, an exact division."),
    # computed steps
    (r"The LCM is the smallest number that both %s and %s divide into exactly\. Count up in jumps of the bigger number, %s: %s\." % (_N, _N, _N, _LIST),
     "The L C M is the smallest number that both {1} and {2} divide into exactly. Count up in jumps of the bigger number, {3}. That gives {C4}."),
    (r"Check each one: can %s divide it exactly\? %s is the first that works: %s × %s = %s, and it is also %s × %s\." % ((_N,) * 7),
     "Check each one: can {1} divide it exactly? {2} is the first that works. {3} times {4} equals {5}, and it is also {6} times {7}."),
    (r"So the LCM of %s and %s is %s\." % (_N, _N, _N), "So the L C M of {1} and {2} is {3}."),
    (r"A factor divides a number exactly\. The factors of %s are %s\." % (_N, _LIST), "A factor divides a number exactly. The factors of {1} are {L2}."),
    (r"The factors of %s are %s\." % (_N, _LIST), "The factors of {1} are {L2}."),
    (r"The numbers in both lists are %s\. The biggest of these is %s, so the HCF of %s and %s is %s\." % (_LIST, _N, _N, _N, _N),
     "The numbers in both lists are {L1}. The biggest of these is {2}, so the H C F of {3} and {4} is {5}."),
]
_COMPILED = [(re.compile(p), t) for p, t in _PATTERNS]


def _fill(template, groups):
    def sub(m):
        kind, i = m.group(1), int(m.group(2))
        g = groups[i - 1]
        if kind == "L":
            return and_list(g)
        if kind == "C":  # a counting list: commas only, the last one is the answer being reached
            return ", ".join(x.strip() for x in g.split(","))
        if kind == "A":
            return " ".join(g)
        if kind == "S":
            return "plus" if g == "+" else "minus"
        return g
    return re.sub(r"\{([LCAS]?)(\d+)\}", sub, template)


def family_line(text):
    """The narration of a generated-family line, or None if the wording is not one we know."""
    if text in _FIXED:
        return _FIXED[text]
    for pat, template in _COMPILED:
        m = pat.fullmatch(text)
        if m:
            return _fill(template, m.groups())
    return None


def latex_words(latex):
    """The maths line under a 'Solve' step: '2x = 1 + 11 = 12', or x = a fraction = the boxed answer."""
    m = re.fullmatch(r"(\d+)x = (\d+) ([+-]) (\d+) = (\d+)", latex)
    if m:
        a, b, op, c, d = m.groups()
        return "%s x equals %s %s %s, which is %s." % (a, b, "plus" if op == "+" else "minus", c, d)
    m = re.fullmatch(r"x = \\frac\{(\d+)\}\{(\d+)\} = \\boxed\{(-?\d+)\}", latex)
    if m:
        a, b, c = m.groups()
        return "x equals %s over %s, which is %s." % (a, b, c.replace("-", "minus "))
    return None
