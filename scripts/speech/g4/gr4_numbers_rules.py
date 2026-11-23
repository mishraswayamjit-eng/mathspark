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
        if re.search(r"\b(is|are|equals|gives|makes|add)\b", clause):
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
    # (The whole-line templates for the old terse hints and steps of the generated families and
    # past papers were removed when that text was rewritten in the bank as full sentences.)
    return None


def say(text):
    t = (text or "").strip()
    if not t:
        return ""
    fam = _family(t)
    if fam:
        return fam
    s = t
    # counting odd numbers in pairs: two sums in one clause read better as two short sentences
    s = re.sub(r"there are (\d+) − (\d+) = (\d+) numbers, which make (\d+) ÷ 2 = (\d+) pairs",
               r"there are \1 minus \2 equals \3 numbers. These make \4 divided by 2 equals \5 pairs", s)
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
    # a semicolon between sentences is a full stop; between numbers in a list it is a comma
    s = re.sub(r"(?<=[A-Za-z]);\s+(\S)", lambda m: ". " + m.group(1).upper(), s)
    s = re.sub(r";\s*", ", ", s)
    # algebra: 3m, 5mn are said letter by letter
    s = re.sub(r"(?<![\d,.])(\d)([mnpq]{1,2})\b", lambda m: m.group(1) + " " + " ".join(m.group(2)), s)
    # words printed in capitals for emphasis (NOT, NEVER) are said as ordinary words
    s = re.sub(r"\b(?![IVXLCDM]+\b)(?!IPM\b|HCF\b|LCM\b)[A-Z]{3,}(?:'[A-Z])?\b", lambda m: m.group(0).lower(), s)
    s = re.sub(r"\bIPM\b", "I P M", s)
    s = re.sub(r"\bPV\b", "place value", s)
    s = roman(s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    # "X X I V is 10 plus 10 plus 4, which is 24 and X V I I I is ..." needs a pause after the total
    s = re.sub(r"(, which is \d+(?:,\d+)*) and ", r"\1, and ", s)
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
