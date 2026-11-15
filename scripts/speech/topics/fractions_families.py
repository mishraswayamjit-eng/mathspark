"""The generated families of the fractions topic: one carefully written sentence pattern each.

    family(text)               the spoken line for a generated line, or None if no pattern fits
    equation_step(text, latex) an equation step read together with its maths line, or None
"""
import re

N = r"(\d+)"
F = r"(\d+)/(\d+)"

_WORDS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters",
          ("1", "3"): "one third", ("2", "3"): "two thirds"}


def _of(a, b):
    return _WORDS.get((a, b)) or "%s over %s" % (a, b)


def _same(a, b, c, d):
    """'2/8 = 14/56', or 'stays as' when the fraction does not change."""
    return "%s over %s %s %s over %s" % (a, b, "stays as" if (a, b) == (c, d) else "equals", c, d)


def _think(m):
    d, n, r, k = m.groups()
    if d == "2":
        return "Think: one of the 2 equal parts of %s is %s. Now take %s of those." % (n, r, k)
    nth = "one 3rd" if d == "3" else "one %sth" % d
    return "Think: %s of %s is %s. Now take %s of those." % (nth, n, r, k)


def _simplify(m):
    a, b, rest = m.group(1), m.group(2), m.group(3)
    if "/" in rest:
        c, d = rest.split("/")
        if (a, b) == (c, d):
            return "Simplify. %s over %s stays as %s over %s." % (a, b, c, d)
        return "Simplify. %s over %s equals %s over %s." % (a, b, c, d)
    return "Simplify. %s over %s equals %s." % (a, b, rest)


_QUESTIONS = [
    (r"(\w+) has %s marbles\. (\w+) gives %s of them to a friend\. How many marbles does (\w+) have left\?" % (N, F),
     lambda m: "%s has %s marbles. %s gives %s of them to a friend. How many marbles does %s have left?" % (
         m.group(1), m.group(2), m.group(3), _of(m.group(4), m.group(5)), m.group(6))),
    (r"Which is greater: %s or %s\?" % (F, F), r"Which is greater: \1 over \2, or \3 over \4?"),
    (r"Simplify: %s \+ %s" % (F, F), r"Simplify: \1 over \2, plus \3 over \4."),
    (r"What is %s of %s\?" % (F, N), lambda m: "What is %s of %s?" % (_of(m.group(1), m.group(2)), m.group(3))),
    (r"Find the missing number: %s = \?/%s" % (F, N), r"Find the missing number. \1 over \2 equals what, over \3?"),
    (r"Solve: %sx − %s = %s" % (N, N, N), r"Solve: \1 x, minus \2, equals \3."),
    (r"Solve: %sx \+ %s = %s" % (N, N, N), r"Solve: \1 x, plus \2, equals \3."),
    (r"What is %s − %s\?" % (F, F), r"What is \1 over \2, minus \3 over \4?"),
    (r"What is %s \+ %s\?" % (F, F), r"What is \1 over \2, plus \3 over \4?"),
]

_HINTS = [
    (r"First find %s of %s\." % (F, N), lambda m: "First find %s of %s." % (_of(m.group(1), m.group(2)), m.group(3))),
    (r"LCM of %s and %s will help\." % (N, N), r"The L C M of \1 and \2 will help."),
    (r"Add: %s \+ %s = %s\. Keep denominator %s\." % (N, N, N, N), r"Add: \1 plus \2 equals \3. Keep the denominator, \4."),
    (r"To find %s of %s, first divide %s by %s\." % (F, N, N, N),
     lambda m: "To find %s of %s, first divide %s by %s." % (_of(m.group(1), m.group(2)), m.group(3), m.group(4), m.group(5))),
    (r"Think: one-%s\w+ of %s is %s\. Now take %s of those\." % (N, N, N, N), _think),
    (r"When you move −%s to the right side, it becomes \+%s\." % (N, N), r"When you move minus \1 to the right side, it becomes plus \2."),
    (r"After subtracting: %sx = %s\. Now divide both sides by %s\." % (N, N, N), r"After subtracting: \1 x equals \2. Now divide both sides by \3."),
]

_STEPS = [
    (r"Marbles given = %s of %s = %s" % (F, N, N),
     lambda m: "The marbles given are %s of %s, which is %s." % (_of(m.group(1), m.group(2)), m.group(3), m.group(4))),
    (r"Remaining = %s − %s = %s" % (N, N, N), r"What remains is \1 minus \2, which is \3."),
    (r"Find common denominator: LCM of %s and %s = %s" % (N, N, N), r"Find a common denominator. The L C M of \1 and \2 is \3."),
    (r"Convert: %s = %s, %s = %s" % (F, F, F, F), lambda m: "Convert. %s. And %s." % (_same(*m.groups()[:4]), _same(*m.groups()[4:]))),
    (r"Compare numerators: %s vs %s\. So %s is greater\." % (N, N, F), r"Compare the numerators: \1 and \2. So \3 over \4 is greater."),
    (r"Compare numerators: %s vs %s\. ([A-Za-z .]*)" % (N, N), r"Compare the numerators: \1 and \2. \3"),
    (r"Same denominators, so add numerators: \(%s\+%s\)/%s = %s" % (N, N, N, F),
     r"The denominators are the same, so add the numerators. \1 plus \2, over \3, equals \4 over \5."),
    (r"Simplify: %s = (\d+(?:/\d+)?)" % F, _simplify),
    (r"Divide %s by %s: %s ÷ %s = %s" % (N, N, N, N, N), r"Divide \1 by \2. \3 divided by \4 equals \5."),
    (r"Multiply by %s: %s × %s = %s" % (N, N, N, N), r"Multiply by \1. \2 times \3 equals \4."),
    (r"Denominator multiplied by %s: %s × %s = %s" % (N, N, N, N), r"The denominator was multiplied by \1. \2 times \3 equals \4."),
    (r"So numerator also × %s: %s × %s = %s" % (N, N, N, N), r"So multiply the numerator by \1 as well. \2 times \3 equals \4."),
]

_FAMILY = [(re.compile(p), t) for p, t in _QUESTIONS + _HINTS + _STEPS]


def family(text):
    s = (text or "").strip()
    for pat, tmpl in _FAMILY:
        m = pat.fullmatch(s)
        if m:
            return tmpl(m) if callable(tmpl) else m.expand(tmpl)
    return None


def equation_step(text, latex):
    """'Add 2 to both sides' with its maths line '6x = 58 + 2 = 60', read as one step."""
    latex = (latex or "").strip()
    m = re.fullmatch(r"%sx = %s ([+-]) %s = %s" % (N, N, N, N), latex)
    if m:
        op = "plus" if m.group(3) == "+" else "minus"
        return "%s. %s x equals %s %s %s, which is %s." % (text.strip(), m.group(1), m.group(2), op, m.group(4), m.group(5))
    m = re.fullmatch(r"x = \\frac\{%s\}\{%s\} = \\boxed\{(-?\d+)\}" % (N, N), latex)
    if m:
        ans = m.group(3).replace("-", "minus ")
        return "%s. x equals %s over %s, which is %s." % (text.strip(), m.group(1), m.group(2), ans)
    return None
