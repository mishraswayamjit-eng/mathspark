"""Rules that turn printed Grade 4 circle work into speech. Used by gr4_circle.py.

The general geometry converter is shared with quadrilaterals (gr4_quads_rules); this adds circle notation:
pi and the formulas written with it, 'Use pi = 22/7', and points and lines named by capital letters.

    say(text)          the converter for this topic's notation
    from_latex(latex)  a step's maths line, as the print it stands for
"""
import re

import gr4_quads_rules as base

from_latex = base.from_latex

# words printed in capitals for stress; any other run of capitals names points (OA, AB, ABC)
_STRESS = {"NOT", "CANNOT", "AND", "OR", "ALL", "ANY", "ONLY", "TRUE", "FALSE", "IS", "ARE", "NO", "ONE", "TWO",
           "BOTH", "SAME", "EVERY", "MOST", "LEAST", "EXACTLY", "ALWAYS", "NEVER", "HALF", "TWICE", "LONGEST",
           "INFINITE", "INFINITELY", "MANY", "IPM", "LCM", "HCF", "ON", "IN", "OF", "TO", "BUT", "THE", "DOUBLE",
           "SQUARE", "SQUARED", "RADIUS", "DIAMETER", "INSIDE", "OUTSIDE", "CENTRE"}


def _points(m):
    w = m.group(0)
    return w if w in _STRESS else " ".join(w)


def say(text):
    s = (text or "").strip()
    if not s:
        return ""
    s = s.replace("\\pi", "π")
    # 'Use pi = 22/7' is an instruction after the question
    s = re.sub(r"\s*\(\s*[Uu]se π\s*=\s*22\s*/\s*7\s*\)\.?", " Use pi as 22 over 7.", s)
    s = re.sub(r"\b([Uu]se|[Tt]ake|[Ww]ith|[Uu]sing) π\s*=\s*22\s*/\s*7", r"\1 pi as 22 over 7", s)
    # formulas: 2πr, πr², πd, C/π, C/(2π)
    s = re.sub(r"\b([A-Za-z])\s*/\s*\(\s*2\s*π\s*\)", r"\1 over 2 π", s)
    s = re.sub(r"\b([A-Za-z])\s*/\s*π", r"\1 over π", s)
    s = re.sub(r"π\s*r\s*(?:²|\^2)", "π r squared", s)
    s = re.sub(r"π\s*([rdRD])\b", r"π \1", s)
    s = re.sub(r"(\d)\s*π", r"\1 π", s)
    s = re.sub(r"\b([rd])\s*(?:²|\^2)", r"\1 squared", s)
    s = re.sub(r"\b(\d+)([rd])\b", r"\1 \2", s)
    s = re.sub(r"\b[A-Z]{2,4}\b", _points, s)
    return base.say(s)
