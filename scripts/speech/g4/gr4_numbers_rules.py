"""Notation rules for gr4_numbers narration: print to speech.

    say(text)          a printed line as spoken words
    from_latex(latex)  a step's maths line as a printed line (or "" when it is not plain arithmetic)
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import common  # noqa: E402

NUM = r"\d[\d,]*(?:\.\d+)?"

# A Roman numeral of two or more letters is spelt out letter by letter: MCMXLV -> "M C M X L V".
_ROMAN = re.compile(r"(?<![A-Za-z'’])[IVXLCDM]{2,}(?![A-Za-z'’])")


def roman(s):
    return _ROMAN.sub(lambda m: " ".join(m.group(0)), s)


def _equals(s):
    """'=' is 'equals' the first time in a clause, and ', which is' after an 'is' or an earlier 'equals'."""
    out = ""
    for piece in re.split(r"(\s*=\s*)", s):
        if not re.fullmatch(r"\s*=\s*", piece or " "):
            out += piece
            continue
        clause = re.split(r"[.?!:;(]\s|, | and | so | because ", out)[-1]
        if re.search(r"\b(is|are|equals|gives)\b", clause):
            out = out.rstrip() + ", which is "
        else:
            out = out.rstrip() + " equals "
    return out


def _compare(s, sign, words):
    parts = s.split(sign)
    if len(parts) == 1:
        return s
    out = parts[0].rstrip() + " is " + words + " " + parts[1].strip()
    for p in parts[2:]:
        out += ", which is " + words + " " + p.strip()
    return out


def _family(t):
    """Whole lines of the generated families, written out in full."""
    m = re.fullmatch(r"In the number (\d+), the place value of (\d) \(in ([a-z-]+) place\) is how many times the place value of (\d) \(in ([a-z-]+) place\)\?", t)
    if m:
        return "In the number %s, the place value of the %s in the %s place is how many times the place value of the %s in the %s place?" % m.groups()
    m = re.fullmatch(r"PV of (\d) = (%s), PV of (\d) = (%s)" % (NUM, NUM), t)
    if m:
        a, b, c, d = m.groups()
        if a == c:
            return "The place value of one %s is %s, and the place value of the other %s is %s." % (a, b, c, d)
        return "The place value of %s is %s, and the place value of %s is %s." % (a, b, c, d)
    m = re.fullmatch(r"Ratio = (%s) ÷ (%s) = (%s)" % (NUM, NUM, NUM), t)
    if m:
        return "The ratio is %s divided by %s, which is %s." % m.groups()
    if t == "Place value = digit × value of its position.":
        return "Place value equals the digit, times the value of its position."
    m = re.fullmatch(r"Place value = (%s) × (%s) = (%s)" % (NUM, NUM, NUM), t)
    if m:
        return "Place value equals %s times %s, which is %s." % m.groups()
    m = re.fullmatch(r"Digits of (\d+): ([\d +]+) = (\d+)", t)
    if m:
        return "The digits of %s: %s, which equals %s." % (m.group(1), m.group(2).replace("+", "plus"), m.group(3))
    if t == "Use the formula: (last − first) ÷ 2 + 1.":
        return "Use the formula: last minus first, then divide by 2, then add 1."
    m = re.fullmatch(r"Count = \((\d+) − (\d+)\) ÷ 2 \+ 1 = (\d+)", t)
    if m:
        return "Count: %s minus %s, then divide by 2, then add 1. That gives %s." % m.groups()
    m = re.fullmatch(r"First odd: (\d+), Last odd: (\d+)", t)
    if m:
        return "The first odd is %s, and the last odd is %s." % m.groups()
    m = re.fullmatch(r"This is from the (\d+) IPM exam \(Q(\d+)\)\.", t)
    if m:
        return "This is from the %s I P M exam, question %s." % m.groups()
    m = re.fullmatch(r"Correct answer: Option (\d) — (.+)", t)
    if m:
        rest = say(m.group(2))
        return "Correct answer: option %s, %s%s" % (m.group(1), rest, "" if rest[-1] in ".?!" else ".")
    m = re.fullmatch(r"(Largest|Smallest) = (%s)" % NUM, t)
    if m:
        return "The %s is %s." % (m.group(1).lower(), m.group(2))
    return None


def say(text):
    t = (text or "").strip()
    if not t:
        return ""
    fam = _family(t)
    if fam:
        return fam
    s = t
    # money
    s = re.sub(r"₹\s*(%s)(?=\s+notes?\b)" % NUM, r"\1 rupee", s)
    s = re.sub(r"₹\s*(\d[\d,]*\d(?:\.\d+)?|\d)", r"\1 rupees", s)
    # blanks between digits: 3 _ 0 _ 9
    s = re.sub(r"(?<=\d) _+ (?=\d)", ", blank, ", s)
    # a line of working that starts with "="
    s = re.sub(r"^=\s*", "That equals ", s)
    s = re.sub(r"=\s*\?", "equals what?", s)
    # brackets that are only punctuation become pauses
    s = re.sub(r"\s*\(([^()]*)\)", r", \1,", s)
    s = re.sub(r",\s*([.?!,:;])", r"\1", s)
    s = re.sub(r",\s*$", "", s)
    # signs
    s = s.replace("≥", " is greater than or equal to ").replace("≤", " is less than or equal to ")
    s = s.replace("≈", " is about ")
    s = re.sub(r"\s*(?:→|⇒)\s*", ", so ", s)
    s = _compare(s, ">", "greater than")
    s = _compare(s, "<", "less than")
    s = _equals(s)
    s = re.sub(r"\s*×\s*", " times ", s)
    s = re.sub(r"\s*÷\s*", " divided by ", s)
    s = re.sub(r"\s*\+\s*", " plus ", s)
    s = re.sub(r"(?<=[\d\s'’)])\s*−\s*", " minus ", s)
    s = re.sub(r"(\d)\s*[-–]\s*(?=\d)", r"\1 minus ", s)
    s = re.sub(r"\bvs\b\.?", "versus", s)
    s = s.replace("★", " star ").replace("—", ", ")
    s = re.sub(r";\s*", ", ", s)
    # words printed in capitals for emphasis (NOT, NEVER) are said as ordinary words
    s = re.sub(r"\b(?![IVXLCDM]+\b)(?!IPM\b|HCF\b|LCM\b)[A-Z]{3,}(?:'[A-Z])?\b", lambda m: m.group(0).lower(), s)
    s = re.sub(r"\bIPM\b", "I P M", s)
    s = re.sub(r"\bPV\b", "place value", s)
    s = roman(s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    if " " in s and re.search(r"[a-z]", s) and s[-1] not in ".?!:":
        s += "."
    return s


_PLAIN_MATHS = re.compile(r"[\d\s+\-=.]+")


def from_latex(latex):
    """Plain arithmetic maths lines as print ('998 - 101 = 897' -> '998 − 101 = 897'); anything else gives ''."""
    s = (latex or "").replace("\\times", "×").replace("\\div", "÷")
    if "\\" in s or "{" in s:
        return ""
    if not _PLAIN_MATHS.fullmatch(s.replace("×", "+").replace("÷", "+")):
        return ""
    if not re.search(r"[+\-×÷=]", s):
        return ""
    return re.sub(r"\s*-\s*", " − ", s).strip()
