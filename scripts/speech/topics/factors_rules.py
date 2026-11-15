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
    s = re.sub(r"(\d)([a-rt-zA-Z])\b", r"\1 \2", s)  # "5a" is "5 a", but "the 2s" stays a plural
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

# Wordings from the rewritten hints and solutions.
_ALIST = r"(\d+(?:, \d+)*(?: and \d+)?)"
_PROD = r"(\d+(?: × \d+)*)"
_TAIL = r" Each time, ask: is this number in the %s times table too\? The first one that is, is the LCM\." % _N
_TAIL_SAID = " Each time, ask: is this number in the {%d} times table too? The first one that is, is the L C M."
_PATTERNS += [
    (r"LCM means Lowest Common Multiple: the smallest number that is in both the %s times table and the %s times table\." % (_N, _N),
     "L C M means Lowest Common Multiple: the smallest number that is in both the {1} times table, and the {2} times table."),
    (r"HCF means Highest Common Factor: the biggest number that divides both %s and %s exactly, with nothing left over\." % (_N, _N),
     "H C F means Highest Common Factor: the biggest number that divides both {1} and {2} exactly, with nothing left over."),
    (r"Write down every number that divides %s exactly\. These are its factors, and they come in pairs: 1 × %s is one pair\. Do the same for %s\. Then look for the biggest number that is on both lists\." % (_N, _N, _N),
     "Write down every number that divides {1} exactly. These are its factors, and they come in pairs: 1 times {2} is one pair. Do the same for {3}. Then look for the biggest number that is on both lists."),
    (r"Count up in %ss: %s, and keep going\.%s" % (_N, _LIST, _TAIL),
     "Count up in {1}s: {C2}, and keep going." + _TAIL_SAID % 3),
    (r"Count up in %ss, starting with %s itself\.%s" % (_N, _N, _TAIL),
     "Count up in {1}s, starting with {2} itself." + _TAIL_SAID % 3),
    (r"Try another one: the LCM of %s and %s\. Count up in %ss: %s\. The first one that is also in the %s times table is %s, because %s × %s = %s\. So the LCM of %s and %s is %s\." % (_N, _N, _N, _LIST, _N, _N, _N, _N, _N, _N, _N, _N),
     "Try another one: the L C M of {1} and {2}. Count up in {3}s: {C4}. The first one that is also in the {5} times table is {6}, because {7} times {8} equals {9}. So the L C M of {10} and {11} is {12}."),
    (r"Try another one: the HCF of %s and %s\. Factors of %s: %s\. Factors of %s: %s\. The biggest number on both lists is %s, so the HCF is %s\." % (_N, _N, _N, _LIST, _N, _LIST, _N, _N),
     "Try another one: the H C F of {1} and {2}. The factors of {3} are {L4}. The factors of {5} are {L6}. The biggest number on both lists is {7}, so the H C F is {8}."),
    (r"So the HCF of %s and %s is %s\." % (_N, _N, _N), "So the H C F of {1} and {2} is {3}."),
    (r"List the factors of %s: %s\." % (_N, _ALIST), "List the factors of {1}: {2}."),
    (r"The factors in both lists are %s\. The largest of them is %s\." % (_ALIST, _N),
     "The factors in both lists are {1}. The largest of them is {2}."),
    (r"Pick out the prime factors that appear in both: %s\." % _ALIST, "Pick out the prime factors that appear in both: {1}."),
    (r"Multiply them: %s = %s\." % (_PROD, _N), "Multiply them: {P1} equals {2}."),
    (r"Break each number into prime factors: %s = %s, and %s = %s\." % (_N, _PROD, _N, _PROD),
     "Break each number into prime factors. {1} equals {G2}. And {3} equals {G4}."),
    (r"Add %s to both sides to undo the [−-] %s: %sx = %s \+ %s = %s\." % ((_N,) * 6),
     "Add {1} to both sides, to undo the minus {2}. {3} x equals {4} plus {5}, which is {6}."),
    (r"Subtract %s from both sides to undo the \+ %s: %sx = %s [−-] %s = %s\." % ((_N,) * 6),
     "Subtract {1} from both sides, to undo the plus {2}. {3} x equals {4} minus {5}, which is {6}."),
    (r"Divide both sides by %s: x = %s ÷ %s = %s\." % ((_N,) * 4),
     "Divide both sides by {1}. x equals {2} divided by {3}, which is {4}."),
    (r"Check: %s × %s ([−+-]) %s = %s\. So x = %s\." % ((_N,) * 5),
     "Check: {1} times {2}, {S3} {4}, equals {5}. So x equals {6}."),
]
_COMPILED = [(re.compile(p), t) for p, t in _PATTERNS]


def grouped_product(text):
    """'2 × 2 × 2 × 3 × 5' -> '2 times 2 times 2, times 3, times 5': a breath between different primes."""
    nums = [n.strip() for n in text.split("×")]
    groups = []
    for n in nums:
        if groups and groups[-1][0] == n:
            groups[-1].append(n)
        else:
            groups.append([n])
    if len(groups) == len(nums) and len(nums) <= 3:
        return " times ".join(nums)
    return ", times ".join(" times ".join(g) for g in groups)


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
        if kind == "P":
            return " times ".join(n.strip() for n in g.split("×"))
        if kind == "G":
            return grouped_product(g)
        return g
    return re.sub(r"\{([LCASPG]?)(\d+)\}", sub, template)


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
