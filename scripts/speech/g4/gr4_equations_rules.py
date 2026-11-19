"""Rules that turn printed equation / word-problem text into words for the voice.

Used by gr4_equations.py (and reused by gr4_ages.py).

    say(text)          the spoken line for a printed line
    from_latex(latex)  a step's maths line as plain print, ready for say()
"""
import re

_WORD_FRACTION = {
    ("1", "2"): "one half", ("1", "3"): "one third", ("2", "3"): "two thirds",
    ("1", "4"): "one quarter", ("3", "4"): "three quarters",
}
_KEEP_CAPS = {"IPM", "LHS", "RHS"}
_UNITS = [
    ("kg", "kilogram"), ("km", "kilometre"), ("cm", "centimetre"), ("mm", "millimetre"),
    ("ml", "millilitre"), ("m", "metre"), ("g", "gram"), ("l", "litre"),
]
# What ends one sum and starts the next, so that only a second "=" inside ONE sum becomes "which is".
_BOUNDARY = re.compile(r"[.?!:;,]\s|\b(?:and|so|but|then|means|same as)\b")


def from_latex(latex):
    """The maths line of a step, as print: fractions as a/b (or a ÷ b when it divides exactly)."""
    s = latex or ""
    s = re.sub(r"\\text\{([^{}]*)\}", r" \1 ", s)
    s = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", s)

    def frac(m):
        a, b = m.group(1).strip(), m.group(2).strip()
        if a.isdigit() and b.isdigit() and int(b) and int(a) % int(b) == 0:
            return "%s ÷ %s" % (a, b)
        if not a.isdigit() and b.isdigit() and re.fullmatch(r"\d+[a-zA-Z]", a):
            return "%s ÷ %s" % (a, b)
        return "%s/%s" % (a, b)

    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\neq", "≠").replace("\\checkmark", "✓")
    s = s.replace("\\quad", " ").replace("\\,", " ")
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def _fraction(m):
    a, b = m.group(1), m.group(2)
    if (a, b) in _WORD_FRACTION:
        return _WORD_FRACTION[(a, b)]
    return "%s over %s" % (a, b)


def _unit(m):
    n, word = m.group(1), dict(_UNITS)[m.group(2)]
    if m.group(3):                      # "a 2 kg weight": the unit describes the thing, so no plural
        return "%s %s%s" % (n, word, m.group(3))
    return "%s %s" % (n, word if n == "1" else word + "s")


_VERBS = {
    "is", "are", "be", "was", "cost", "costs", "gained", "give", "gives", "gave", "by", "takes", "has", "have",
    "had", "won", "weigh", "weighs", "in", "gets", "get", "turns", "total", "totalled", "after", "then",
    "still", "always", "of", "with", "leaves", "make", "year",
}


def _equals(s):
    """The first "=" of a sum is "equals"; a second one in the same sum is ", which is".

    A sum inside a sentence that already has its verb ("x is 13 − 4 = 9") also takes ", which is".
    """
    out, last, seen = [], 0, False
    for m in re.finditer(r"\s*=\s*", s):
        between = s[last:m.start()]
        if _BOUNDARY.search(between):
            seen = False
        word = " equals "
        if seen:
            word = ", which is "
        else:
            run = re.search(r"([\d.,/×÷+−\s()]*)$", between).group(1)
            run = re.split(r"[.,]\s", run)[-1]                 # never reach back into the sentence before
            before = re.search(r"([A-Za-z]+)\s*$", between[:len(between) - len(run)])
            if re.search(r"\d", run) and re.search(r"[×÷+−]", run) and before and before.group(1) in _VERBS:
                word = ", which is "
        out.append(between)
        out.append(word)
        seen = True
        last = m.end()
    out.append(s[last:])
    return "".join(out)


def say(text, stop=True):
    s = (text or "").replace("\n", " ")
    if not s.strip():
        return ""
    # Past-paper filler.
    m = re.fullmatch(r"\s*Correct answer: Option (\d) — (.+?)\s*", s)
    if m:
        s = "The correct answer is option %s, which is %s." % (m.group(1), m.group(2))
    s = re.sub(r"\(Q(\d+)\)", r", question \1", s)
    s = s.replace("IPM", "I P M")
    s = re.sub(r"\bLHS\b", "left side", s)
    s = re.sub(r"\bRHS\b", "right side", s)
    s = re.sub(r"\b[A-Z]{3,}\b", lambda m: m.group(0) if m.group(0) in _KEEP_CAPS else m.group(0).lower(), s)

    # Signs and dashes.
    s = s.replace("–", "−")
    s = re.sub(r"(?<![A-Za-z0-9])-(?=\s*\d)", "−", s)        # "-2", "= -1"
    s = re.sub(r"(?<=\s)-(?=\s)", "−", s)                      # " - "
    s = s.replace("—", ", ")

    # "(100 − 12) ÷ 4 = 22": the bracket is worked out first, so say it first.
    s = re.sub(r"\(([^()]+)\)\s*÷\s*(\d+)\s*=", r"\1, then ÷ \2, equals ", s)
    # Blanks, then "=" while the sums are still in print.
    s = re.sub(r"(\d)\((\d+)\)", r"\1 × \2", s)                        # 3(5)
    s = re.sub(r"\bleft side\s*=\s*", "the left side is ", s)
    s = re.sub(r"\bright side\s*=\s*", "the right side is ", s)
    s = re.sub(r"(^|[.!?] )the (left|right) side is", r"\1The \2 side is", s)
    s = re.sub(r"\bLet ([^=.]*?)\s*=\s*", r"Let \1 be ", s)
    s = re.sub(r"\b([A-Za-z])\s*=\s*\?", r"What is \1?", s)
    s = re.sub(r"=\s*\?", "= what?", s)
    s = re.sub(r"([×÷+−])\s*\?", r"\1 what", s)
    s = s.replace("what??", "what?")
    s = _equals(s)

    # Money, then units.
    s = re.sub(r"(?:₹|Rs\.?)\s*(\d+(?:,\d+)*(?:\.\d+)?)( note)?",
               lambda m: "%s %s%s" % (m.group(1), "rupee" if m.group(1) == "1" or m.group(2) else "rupees", m.group(2) or ""), s)
    s = re.sub(r"(\d+(?:\.\d+)?) ?(kg|km|cm|mm|ml)\b( weight| note| ruler)?", _unit, s)
    s = re.sub(r"(\d+(?:\.\d+)?) (m|g|l)\b(?! ?[+×÷−=/])( weight| note| ruler)?", _unit, s)   # "3 m", never "3m"

    # Squares, roots, shapes that stand for numbers.
    s = re.sub(r"√\s*([A-Za-z0-9]+)", r"the square root of \1", s)
    s = s.replace("²", " squared").replace("³", " cubed")
    s = s.replace("★", "star").replace("▲", "triangle").replace("□", "blank")
    s = re.sub(r"\s*✓\s*\.?", ". That is correct.", s)
    s = s.replace("✗", "")

    # Algebra: 2x, 8P, 3(5), then fractions.
    s = re.sub(r"(\d)\((\d+)\)", r"\1 × \2", s)
    s = re.sub(r"(\d)([A-Za-z])(?![A-Za-z])", r"\1 \2", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", _fraction, s)
    s = re.sub(r"([A-Za-z0-9]+)\s*/\s*([A-Za-z0-9]+)", r"\1 over \2", s)

    # Operations.
    s = s.replace("≠", ", which is not equal to ")
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    s = re.sub(r"\s+", " ", s)
    # "6 times 5, plus 8, equals 38": a breath where the kind of operation changes.
    s = re.sub(r"\b(times|divided by|over|the square root of) (\w+) (plus|minus) ", r"\1 \2, \3 ", s)
    s = re.sub(r"(, (?:plus|minus) [\w ]+?) equals ", r"\1, equals ", s)
    # "15 minus 9 equals 6 centimetres is the breadth": the result needs its own breath.
    s = re.sub(r"(equals \d+(?: [a-z]+)?) (is|are) (the|half|hens)", r"\1, which \2 \3", s)
    s = re.sub(r"(equals \d+) and (?=\d)", r"\1, and ", s)
    # The letter a, used as a number's name, is said as a letter.
    s = re.sub(r"(which is \d+) and ", r"\1, and ", s)
    s = re.sub(r"(?<=\d )a\b(?! (?:year|day|week|month|time)s?\b)", "A", s)
    s = re.sub(r"\ba(?= (?:plus|minus|equals|over)\b| times (?!table))", "A", s)

    # Brackets and quotes that are only punctuation.
    s = re.sub(r"(?<![A-Za-z])'([A-Za-z ]+)'(?![A-Za-z])", r"\1", s)
    s = re.sub(r"\s*\(\s*", ", ", s)
    s = re.sub(r"\s*\)", ",", s)

    # Tidy.
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",([.?!:;,])", r"\1", s)
    s = re.sub(r"\.{2,}", ".", s)
    s = re.sub(r"([:;]),", r"\1", s)
    s = s.strip(" ,")
    if stop and re.match(r"[a-z]{2,}", s):
        s = s[0].upper() + s[1:]
    if stop and s and s[-1] not in ".?!":
        s += "."
    return s
