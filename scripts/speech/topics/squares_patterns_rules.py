"""Rules for the squares-patterns topic: generated families by template, plus a plain fallback.

Imported by squares-patterns.py. Templates are keyed by the source text with every number
replaced by N; the spoken form uses {0}, {1}, ... for those numbers in order.
"""
import re

_NUM = re.compile(r"\d+(?:,\d{2,3})*(?:\.\d+)?")

OPEN = "open bracket,"
CLOSE = "close bracket,"

# The variable a is written as a capital so the voice says the letter, not the article.
TEMPLATES = {
    # ── questions ──
    "Find the next number in the sequence: N, N, N, N, N, ?":
        "Find the next number in the sequence: {0}, {1}, {2}, {3}, {4}, and then what comes next?",
    "Find the next number: N, N, N, ?":
        "Find the next number: {0}, {1}, {2}, and then what comes next?",
    "Find the next number: N, N, N, N, ?":
        "Find the next number: {0}, {1}, {2}, {3}, and then what comes next?",
    "Find the square of N.": "Find the square of {0}.",
    "Find the square root of N.": "Find the square root of {0}.",
    "Find the sum of the arithmetic series: N, N, N, ..., N.":
        "Find the sum of the arithmetic series: {0}, {1}, {2}, and so on, up to {3}.",
    "If √x + N = N, find x.": "If the square root of x, plus {0}, equals {1}, find x.",
    "In an arithmetic sequence starting N, N, N, ..., find the Nth term.":
        "In an arithmetic sequence starting {0}, {1}, {2}, and so on, find the {3}th term.",
    "Solve: Nx + N = N": "Solve: {0} x, plus {1}, equals {2}.",
    "Solve: Nx − N = N": "Solve: {0} x, minus {1}, equals {2}.",
    "Which of the following is a perfect square?": "Which of the following is a perfect square?",

    # ── hints ──
    "After subtracting: Nx = N. Now divide both sides by N.":
        "After subtracting: {0} x equals {1}. Now divide both sides by {2}.",
    "Calculate: N + (N−N) × N.":
        "Calculate: {0} plus, " + OPEN + " {1} minus {2}, " + CLOSE + " times {3}.",
    "First = N, last = N, n = N.": "The first term is {0}, the last term is {1}, and n is {2}.",
    "First isolate √x by subtracting N from both sides.":
        "First isolate the square root of x, by subtracting {0} from both sides.",
    "Here a = N, d = N, n = N.": "Here, A is {0}, d is {1}, and n is {2}.",
    "If √x = N, then x = N².": "If the square root of x is {0}, then x equals {1} squared.",
    "N² = N. Check the others too.": "{0} squared equals {1}. Check the others too.",
    "So N² = N × N.": "So {0} squared equals {1} times {2}.",
    "Sum = N/N × (N + N).":
        "The sum equals {0} over {1}, times, " + OPEN + " {2} plus {3}, close bracket.",
    "Sum of AP = n/N × (first term + last term).":
        "The sum of an A P equals n over {0}, times, " + OPEN + " first term plus last term, close bracket.",
    "Try N: N×N=N. Yes!": "Try {0}: {1} times {2} equals {3}. Yes!",
    "Try numbers: is it N? N×N=N. No.": "Try numbers: is it {0}? {1} times {2} equals {3}. No.",
    "When you move −N to the right side, it becomes +N.":
        "When you move minus {0} to the right side, it becomes plus {1}.",
    "nth term of an AP = a + (n−N)d.":
        "The nth term of an A P equals A plus, " + OPEN + " n minus {0}, " + CLOSE + " times d.",

    # ── steps ──
    "= N": "That equals {0}.",
    "Check each: √N = N (exact). It's a perfect square!":
        "Check each: the square root of {0} is {1}, exactly. It's a perfect square!",
    "Common difference = N − N = N": "The common difference is {0} minus {1}, which equals {2}.",
    "Each term is multiplied by N: ×N pattern": "Each term is multiplied by {0}: a times {1} pattern.",
    "First term (a) = N, Common diff (d) = N": "The first term, A, is {0}. The common difference, d, is {1}.",
    "Next = N + N = N": "The next number is {0} plus {1}, which equals {2}.",
    "Next = N × N = N": "The next number is {0} times {1}, which equals {2}.",
    "Number of terms (n) = N, first = N, last = N":
        "The number of terms, n, is {0}. The first term is {1}, and the last term is {2}.",
    "Square of N = N × N": "The square of {0} is {1} times {2}.",
    "Sum = n/N × (first + last) = N/N × (N+N) = N × N":
        "The sum equals n over {0}, times, " + OPEN + " first plus last, close bracket. "
        "That is {1} over {2}, times, " + OPEN + " {3} plus {4}, close bracket. So we get {5} times {6}.",
    "We need: what number × itself = N?": "We need: what number, times itself, equals {0}?",
    "nth term = a + (n−N)d = N + (N−N)×N = N + N = N":
        "The nth term equals A plus, " + OPEN + " n minus {0}, " + CLOSE + " times d. "
        "That is {1} plus, " + OPEN + " {2} minus {3}, " + CLOSE + " times {4}. "
        "So we get {5} plus {6}, which equals {7}.",
    "x = N² = N": "x equals {0} squared, which is {1}.",
    "√N = N because N × N = N": "The square root of {0} is {1}, because {2} times {3} equals {4}.",
    "√x + N = N, so √x = N":
        "The square root of x, plus {0}, equals {1}. So the square root of x equals {2}.",
}


def by_template(text):
    """The spoken form if the text matches a known family template, else None."""
    nums = _NUM.findall(text)
    key = _NUM.sub("N", text)
    out = TEMPLATES.get(key)
    if out is None:
        return None
    return out.format(*nums)


def equation_step(text, latex):
    """Steps of the 'Solve: ax ± b = c' family: say the instruction, then its line of working."""
    m = re.match(r"(\d+)x = (\d+) ([+-]) (\d+) = (\d+)$", latex or "")
    if m:
        a, c, op, b, r = m.groups()
        return "%s. %s x equals %s %s %s, which is %s." % (
            text.rstrip("."), a, c, "plus" if op == "+" else "minus", b, r)
    m = re.match(r"x = \\frac\{(\d+)\}\{(\d+)\} = \\boxed\{(\d+)\}$", latex or "")
    if m:
        return "%s. x equals %s divided by %s, which is %s." % ((text.rstrip("."),) + m.groups())
    return None


def basic(text):
    """Plain fallback for strings with no hand-written line. Good for numbers and simple sentences."""
    s = text or ""
    if not s.strip():
        return ""
    s = re.sub(r"Rs\.?\s*([\d,]+(?:\.\d+)?)", r"\1 rupees", s)
    s = re.sub(r"√\s*([A-Za-z\d,.]*[A-Za-z\d])", r"the square root of \1", s)
    s = s.replace("²", " squared").replace("³", " cubed")
    s = re.sub(r"\^\s*2\b", " squared", s)
    s = re.sub(r"\s*(?:…|\.\.\.)\s*", ", and so on ", s)
    s = re.sub(r"\b([A-D])–([A-D])\b", r"\1 to \2", s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ")
    s = s.replace("−", " minus ").replace("=", " equals ").replace("≈", " is about ")
    s = s.replace("≤", " is at most ").replace("≥", " is at least ").replace("≠", " is not equal to ")
    s = s.replace("→", ", which gives ").replace("✓", "").replace("✗", "")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;)])", r"\1", s)
    s = re.sub(r",\s*([.?!])", r"\1", s)
    return s
