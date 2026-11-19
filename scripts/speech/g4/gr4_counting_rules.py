"""Speech rules for the Grade 4 topic gr4_counting (counting, arrangements, positions, pairs).

say(text)        print to speech for the notation of this topic
family(text)     whole-line rules for filler lines (None when the line is not one of them)
from_latex(tex)  a step's maths line as print, ready for say()
"""
import re

_MATHS_ONLY = re.compile(r"[\d\s×÷+−\-()]*")
# After one of these words, "a + b = c" is said "a plus b, which is c" ("has 12 ÷ 4 = 3 gaps").
_LEAD = {"is", "gives", "give", "to", "are", "has", "makes", "in", "takes", "numbers"}
# Players, points and orders named by letters: AB, CD, ABC, CBA.
_LETTERS = re.compile(r"\b[A-H]{2,3}\b")


def _equals(s):
    """'=' is 'equals'; in a chain (a = b = c) the later ones are ', which equals'."""
    parts = s.split("=")
    out = parts[0]
    for i in range(1, len(parts)):
        prev = parts[i - 1]
        chain = i >= 2 and prev.strip() and _MATHS_ONLY.fullmatch(prev)
        lead = re.search(r"\b([a-z]+)\s+([\d\s×÷+−\-()]+)$", prev)
        if chain:
            join = ", which equals "
        elif lead and lead.group(1) in _LEAD and re.search(r"[×÷+−\-]", lead.group(2)):
            join = ", which is "
        else:
            join = " equals "
        out = out.rstrip() + join + parts[i].lstrip()
    return out


def say(text):
    s = text or ""
    s = re.sub(r"\bIPM\b", "I P M", s)
    s = re.sub(r"\bNOT\b", "not", s)
    # Brackets that are only punctuation become commas.
    s = re.sub(r"\s*\(([^()]*)\)(?=[.,:;?!])", r", \1", s)
    s = re.sub(r"\s*\(([^()]*)\)", r", \1,", s)
    s = _equals(s)
    s = re.sub(r"\s*×\s*", " times ", s)
    s = re.sub(r"\s*÷\s*", " divided by ", s)
    s = re.sub(r"\s*\+\s*", " plus ", s)
    s = re.sub(r"\s*−\s*", " minus ", s)
    s = re.sub(r"(?<=\d)\s*-\s*(?=\d)", " minus ", s)
    s = _LETTERS.sub(lambda m: " ".join(m.group(0)), s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",([.:;?!])", r"\1", s)
    s = re.sub(r",,+", ",", s)
    return s


def family(text):
    t = text.strip()
    m = re.fullmatch(r"This is from the (\d+) IPM exam \(Q(\d+)\)\.", t)
    if m:
        return "This is from the %s I P M exam, question %s." % (m.group(1), m.group(2))
    m = re.fullmatch(r"Correct answer: Option (\d) — (.+)", t)
    if m:
        return "The correct answer is option %s, which is %s." % (m.group(1), say(m.group(2)))
    return None


def from_latex(tex):
    """A maths line as a spoken sentence (without its full stop)."""
    s = re.sub(r"\\boxed\{(.*)\}", r"\1", tex.strip())
    s = re.sub(r"\\text\{([^}]*)\}", r" \1 ", s)
    s = s.replace("\\times", "×").replace("\\div", "÷")
    return say(s)
