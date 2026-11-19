"""Notation rules for gr4_squares narration: print to speech.

    say(text)          a printed line as spoken words
    from_latex(latex)  a step's maths line as a printed line (or "" when it is not plain arithmetic)
"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import common  # noqa: E402

NUM = r"\d+(?:,\d+)*(?:\.\d+)?"


def _equals(s):
    """'=' is 'equals' the first time in a clause, and ', which is' after an 'is' or an earlier 'equals'."""
    out = ""
    for piece in re.split(r"(\s*=\s*)", s):
        if not re.fullmatch(r"\s*=\s*", piece or " "):
            out += piece
            continue
        clause = re.split(r"[.?!:;(]\s|, | and | so | because ", out)[-1]
        if re.search(r"\b(is|are|equals|gives|makes|make|buy|needs|hold|try|with|from|than)\b", clause):
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
    if t in _SIGNS:
        return _SIGNS[t]
    m = re.fullmatch(r"This is from the (\d+) IPM exam \(Q(\d+)\)\.", t)
    if m:
        return "This is from the %s I P M exam, question %s." % m.groups()
    m = re.fullmatch(r"Correct answer: Option (\d) — (.+)", t)
    if m:
        rest = say(m.group(2))
        return "Correct answer: option %s, %s%s" % (m.group(1), rest, "" if rest[-1] in ".?!" else ".")
    m = re.fullmatch(r"√(\d+) = (\d+) because (\d+) × (\d+) = (\d+)", t)
    if m:
        return "The square root of %s is %s, because %s times %s equals %s." % m.groups()
    m = re.fullmatch(r"Square of (\d+) = (\d+) × (\d+)", t)
    if m:
        return "The square of %s equals %s times %s." % m.groups()
    return None


_SIGNS = {"<": "is less than", ">": "is greater than", "=": "is equal to"}
_SIGN_NAMES = {"<": "less than", ">": "greater than", "=": "equals"}


def say(text):
    t = (text or "").strip()
    if not t:
        return ""
    fam = _family(t)
    if fam:
        return fam
    s = t
    s = s.replace("²", " squared").replace("³", " cubed")
    s = re.sub(r"√\s*", "the square root of ", s)
    s = re.sub(r"\bsign is ([<>=])", lambda m: "sign is " + _SIGN_NAMES[m.group(1)], s)
    s = re.sub(r"\s*&\s*", " and ", s)
    s = re.sub(r"^=\s*", "That equals ", s)
    s = re.sub(r"\s*=\s*\?", " equals what?", s)
    s = re.sub(r"\s*\(([^()]*)\)", r", \1,", s)
    s = re.sub(r",\s*([.?!,:;])", r"\1", s)
    s = re.sub(r",\s*$", "", s)
    s = re.sub(r"\s*(?:→|⇒)\s*", ", so ", s)
    s = _compare(s, ">", "greater than")
    s = _compare(s, "<", "less than")
    s = _equals(s)
    s = re.sub(r"\s*×\s*", " times ", s)
    s = re.sub(r"\s*÷\s*", " divided by ", s)
    s = re.sub(r"\s*\+\s*", " plus ", s)
    s = re.sub(r"(?<=[\d\s'’)a-z])\s*−\s*", " minus ", s)
    s = re.sub(r"(\d)\s*[-–]\s*(?=\d)", r"\1 minus ", s)
    s = s.replace("—", ", ")
    s = re.sub(r";\s*", ", ", s)
    s = re.sub(r"\b(?!IPM\b|HCF\b|LCM\b)[A-Z]{3,}(?:'[A-Z])?\b", lambda m: m.group(0).lower(), s)
    s = re.sub(r"\bIPM\b", "I P M", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    # a sum that carries on as a sentence: "8 x 8 = 64 is too small", "70 - 64 = 6 must be taken away"
    s = re.sub(r"\bbetween (%s) times (%s) equals (%s) and (%s) times (%s) equals (%s)(?= lie\b)" % ((NUM,) * 6),
               r"between \1 times \2, which is \3, and \4 times \5, which is \6,", s)
    s = re.sub(r"\bbetween (%s) times (%s) equals (%s) and (%s) times (%s) equals (%s)" % ((NUM,) * 6),
               r"between \1 times \2, which is \3, and \4 times \5, which is \6", s)
    s = re.sub(r"\bequals (%s) (is|fits|has)\b" % NUM, r"equals \1, which \2", s)
    s = re.sub(r"\bequals (%s) (must|would)\b" % NUM, r", which is \1, \2", s)
    s = re.sub(r"\s+,", ",", s)
    s = s[0].upper() + s[1:]
    if " " in s and re.search(r"[a-z]", s) and s[-1] not in ".?!:":
        s += "."
    return s


_PLAIN_MATHS = re.compile(r"[\d\s+\-=.,]+")


def from_latex(latex):
    """Plain arithmetic maths lines as print ('998 - 101 = 897' -> '998 − 101 = 897'); anything else gives ''.

    Several sums on one line (separated by \\quad) become a list separated by commas.
    """
    s = (latex or "").replace("\\times", "×").replace("\\div", "÷")
    s = re.sub(r",?\s*\\quad\s*", ", ", s)
    if "\\" in s or "{" in s:
        return ""
    if not _PLAIN_MATHS.fullmatch(s.replace("×", "+").replace("÷", "+")):
        return ""
    if not re.search(r"[+\-×÷=]", s):
        return ""
    return re.sub(r"\s*-\s*", " − ", s).strip()
