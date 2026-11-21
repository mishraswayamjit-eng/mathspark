"""Speech rules for the Grade 4 topic gr4_factors (factors, multiples, primes, HCF, LCM, divisibility).

say(text)        print to speech for the notation of this topic
family(text)     whole-line rules for the generated families (None when the line is not one of them)
from_latex(tex)  a step's maths line as print, ready for say()
"""
import re

_MATHS_ONLY = re.compile(r"[\d\s×÷+−\-()]*")
_LEAD = {"is", "gives", "give", "to"}

# A digit pattern with letters or stars standing for digits: 1A9A5, 2★1★, 25N48, A59.
_PATTERN = re.compile(r"(?<![0-9A-Za-z★])(?=[0-9A-Z★]*[A-Z★])(?=[0-9A-Z★]*\d)[0-9A-Z★]{2,}(?![0-9A-Za-z★])")
_ROMAN = re.compile(r"\b[IVXLCDM]{2,}\b")


def _equals(s):
    """'=' is 'equals'; in a chain (a = b = c) the later ones are ', which equals'."""
    # "9 = 3 × 3 is not prime" -> "9, which is 3 × 3, is not prime"
    s = re.sub(r"(\d+) = (\d+(?: × \d+)+) is\b", r"\1, which is \2, is", s)
    # "2 + 3 = 5 is prime" -> "2 + 3 = 5, which is prime"
    s = re.sub(r"= (\d+) is\b", r"= \1, which is", s)
    parts = s.split("=")
    out = parts[0]
    for i in range(1, len(parts)):
        prev = parts[i - 1]
        chain = i >= 2 and prev.strip() and _MATHS_ONLY.fullmatch(prev)
        lead = re.search(r"\b([a-z]+)\s+([\d\s×÷+−\-()]+)$", prev)
        if chain:
            join = ", which equals "
        elif lead and lead.group(1) in _LEAD and re.search(r"[×÷+−\-]", lead.group(2)):
            join = ", which is "        # "the sum is 105 + 3 = 108" -> "is 105 plus 3, which is 108"
        else:
            join = " equals "
        out = out.rstrip() + join + parts[i].lstrip()
    return out


def _spell_pattern(m):
    pieces = re.findall(r"\d+|[A-Z]|★", m.group(0))
    return " ".join("star" if p == "★" else p for p in pieces)


def _time(m):
    hour, minute = m.group(1), m.group(2)
    if minute == "00":
        return "%s:00" % hour        # the voice reads this as "o'clock"; the checker needs the 0
    return "%s %s" % (hour, minute)


def say(text):
    s = text or ""
    # "H.C.F." closing a sentence keeps its full stop.
    s = re.sub(r"\b(H\.C\.F|L\.C\.M)\.(?=\s+[A-Z]|\s*$)", lambda m: m.group(1).replace(".", "") + ".", s)
    s = s.replace("H.C.F.", "HCF").replace("L.C.M.", "LCM")
    s = s.replace("♥", " heart ").replace("Ψ", " psi ").replace("□", " blank ")
    s = re.sub(r"\b(HCF|LCM)\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)", r"the \1 of \2 and \3", s)
    s = re.sub(r"\bExample: (HCF|LCM) of\b", r"Example: the \1 of", s)
    s = re.sub(r"\bIf (HCF|LCM) of\b", r"If the \1 of", s)
    s = re.sub(r"\bHCF\b", "H C F", s)
    s = re.sub(r"\bLCM\b", "L C M", s)
    s = re.sub(r"\bIPM\b", "I P M", s)
    s = re.sub(r"\bNOT\b", "not", s)
    s = re.sub(r"\bAND\b", "and", s)
    s = s.replace("upto", "up to")
    s = s.replace("✓", "")
    s = re.sub(r",\s*(?:\.\.\.|…)", " and so on", s)
    s = re.sub(r"\.\.\.|…", " and so on", s)
    # Clock times, before anything touches the colon.
    s = re.sub(r"\b(\d{1,2}):(\d\d)\b", _time, s)
    s = re.sub(r"\bAM\b", "a m", s)
    s = re.sub(r"\bPM\b", "p m", s)
    # Brackets that are only punctuation become commas.
    s = re.sub(r"\s*\(([^()]*)\)(?=[.,:;?!])", r", \1", s)
    s = re.sub(r"\s*\(([^()]*)\)", r", \1,", s)
    s = _equals(s)
    s = re.sub(r"\s*×\s*", " times ", s)
    s = re.sub(r"\s*÷\s*", " divided by ", s)
    s = re.sub(r"\s*\+\s*", " plus ", s)
    s = re.sub(r"\s*−\s*", " minus ", s)
    s = re.sub(r"(?<=\d)\s*-\s*(?=\d)", " minus ", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    s = re.sub(r"\s*&\s*", " and ", s)
    s = _PATTERN.sub(_spell_pattern, s)
    s = re.sub(r"\b([A-Z]),([A-Z])\b", r"\1, \2", s)
    s = s.replace("★", " star ")
    s = _ROMAN.sub(lambda m: " ".join(m.group(0)), s)
    s = re.sub(r"(\d)\s*cm\b", r"\1 centimetres", s)
    s = re.sub(r"(\d)\s*min\b", r"\1 minutes", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",([.:;?!])", r"\1", s)
    s = re.sub(r",,+", ",", s)
    s = re.sub(r"(, which is \d+(?:,\d+)*) and\b", r"\1, and", s)
    if s.endswith("and so on"):
        s += "."
    return s


_FAMILIES = [
    (r"First multiple of (\d+) ≥ (\d+): (\d+)", r"The first multiple of \1 that is \2 or more is \3."),
    (r"Last multiple of (\d+) ≤ (\d+): (\d+)", r"The last multiple of \1 that is \2 or less is \3."),
    (r"Count = \((\d+)−(\d+)\)÷(\d+) \+ 1 = (\d+)", r"Count equals \1 minus \2, divided by \3, plus 1. That equals \4."),
    (r"Count = \(last − first\) ÷ (\d+) \+ 1\.", r"Count equals last minus first, divided by \1, plus 1."),
    (r"First: (\d+), Last: (\d+)\.", r"The first is \1, and the last is \2."),
    (r"Use: LCM = \(a×b\) ÷ HCF\(a,b\)\.", "Use this rule: the L C M equals a times b, divided by the H C F of a and b."),
    (r"LCM × HCF = (\d+) × (\d+) = (\d+)", r"L C M times H C F equals \1 times \2, which is \3."),
    (r"HCF\((\d+),(\d+)\) = (\d+), so LCM = (\d+) ÷ (\d+) = (\d+)",
     r"The H C F of \1 and \2 is \3, so the L C M is \4 divided by \5, which is \6."),
    (r"HCF = (\d+)", r"The H C F is \1."),
    (r"LCM = (\d+)", r"The L C M is \1."),
    (r"Find factors of (\d+) and (\d+)\.", r"Find the factors of \1 and \2."),
    (r"First find HCF of (\d+) and (\d+)\.", r"First find the H C F of \1 and \2."),
    (r"LCM is the smallest number divisible by both (\d+) and (\d+)\.", r"The L C M is the smallest number divisible by both \1 and \2."),
    (r"This is from the (\d+) IPM exam \(Q(\d+)\)\.", r"This is from the \1 I P M exam, question \2."),
]


def family(text):
    t = text.strip()
    for pat, rep in _FAMILIES:
        m = re.fullmatch(pat, t)
        if m:
            return m.expand(rep)
    m = re.fullmatch(r"Correct answer: Option (\d) — (.+)", t)
    if m:
        return "The correct answer is option %s, which is %s." % (m.group(1), say(m.group(2)))
    return None


def from_latex(tex):
    """A maths line as a spoken sentence (without its full stop)."""
    s = re.sub(r"\\boxed\{(.*)\}", r"\1", tex.strip())
    s = re.sub(r"\\frac\{(\d+)\}\{(\d+)\}", r"\1/\2", s)
    s = re.sub(r"\\text\{([^}]*)\}", r" \1 ", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("{:}", ":")
    parts = [say(p) for p in s.split("\\quad") if p.strip()]
    if len(parts) > 1:
        return ", ".join(parts[:-1]) + ", and " + parts[-1]
    return parts[0] if parts else ""
