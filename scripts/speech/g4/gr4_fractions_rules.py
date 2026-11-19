"""Rules that turn printed Grade 4 fraction work into speech. Used by gr4_fractions.py.

    say(text)    the general converter for this topic's notation
"""
import re

_WORDS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters",
          ("1", "3"): "one third", ("2", "3"): "two thirds"}

_ABBREV = [
    (r"\bLCM\b", "L C M"), (r"\bHCF\b", "H C F"), (r"\bLCD\b", "L C D"), (r"\bGCD\b", "G C D"),
    (r"\bRHS\b", "the right-hand side"), (r"\bLHS\b", "the left-hand side"),
    (r"(\d)\s*kg\b", r"\1 kilograms"), (r"(\d)\s*km\b", r"\1 kilometres"), (r"(\d)\s*cm\b", r"\1 centimetres"),
    (r"(\d)\s*mm\b", r"\1 millimetres"), (r"(\d)\s*ml\b", r"\1 millilitres"), (r"(\d)\s*mL\b", r"\1 millilitres"),
    (r"(\d)\s*g\b", r"\1 grams"), (r"(\d)\s*m\b", r"\1 metres"), (r"(\d)\s*[lL]\b", r"\1 litres"),
    (r"(\d)\s*min\b", r"\1 minutes"), (r"(\d)\s*hrs?\b", r"\1 hours"),
    (r"\b(\d+)\s*([ap])\.?m\.?(?=\W|$)", r"\1 \2 m"),
    (r"\be\.g\.,?", "for example,"), (r"\bi\.e\.,?", "that is,"),
]

_OPS = [("×", " times "), ("÷", " divided by "), ("+", " plus "), ("−", " minus "), ("≈", " is about "),
        ("<", " is less than "), (">", " is greater than "), ("≠", " is not equal to "),
        ("≤", " is at most "), ("≥", " is at least ")]


def _frac(n, d):
    return _WORDS.get((n, d)) or "%s over %s" % (n, d)


def _of_word(m):
    return _frac(m.group(1), m.group(2)) + " of "


_NOT_VERBS = {"then", "so", "since", "because", "if", "and", "that", "but", "when", "as", "check", "now", "here",
              "of", "plus", "minus", "times", "by", "equals", "to", "rupees", "rupee", "hours", "minutes",
              "metres", "kilometres", "centimetres", "kilograms", "grams", "litres", "percent", "x", "y", "n"}


def _equals(sentence):
    """First '=' is 'equals', later ones in the same clause are ', which is'."""
    parts = sentence.split("=")
    if len(parts) == 1:
        return sentence
    out = parts[0]
    tail = re.search(r"\s*$", sentence).group(0)
    lead = re.search(r"\b([a-z]+)\s+(?:₹\s*)?[\d(][\d\s×÷+−\-().,/]*$", out)
    if not out.strip():
        out = "That equals " + parts[1].strip()
    elif lead and lead.group(1) not in _NOT_VERBS:
        # 'she cycles 60 ÷ 5 = 12 km' reads as 'she cycles 60 divided by 5, which is 12 kilometres'
        out = out.rstrip() + ", which is " + parts[1].strip()
    elif re.search(r"\b(?:is|are|was|were|has|have|had|gives|makes?|gets?|be|costs?|means|becomes|uses?|needs?|takes?|holds?|eats?|travels?|covers?|buys?|fills?|for|weighs?|earns?|reads?|pays?|saves?|runs?|walks?|drinks?|spends?|sells?|got|left|only|mix|mixes|contains?|another|about|adds?|or)\s+(?:about\s+)?[\d(]", out):
        out = out.rstrip() + ", which is " + parts[1].strip()
    else:
        out = out.rstrip() + " equals " + parts[1].strip()
    for p in parts[2:]:
        out = out.rstrip() + ", which is " + p.strip()
    return out + tail


def tidy(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r":\s*,", ":", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"\.\s*\.", ".", s)
    s = re.sub(r"([,?!:;])(?=[A-Za-z])", r"\1 ", s)
    s = re.sub(r"^[,;:]\s*", "", s)
    s = re.sub(r"([.?!] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    if s:
        s = s[0].upper() + s[1:]
    return s


_UNIT = r"(litres?|metres?|kilometres?|kilograms?|grams?|hours?|minutes?|cups?|km|kg|cm|m|l|L|g)\b"
_UNIT_FULL = {"km": "kilometre", "kg": "kilogram", "cm": "centimetre", "m": "metre", "l": "litre", "L": "litre", "g": "gram"}
_MIXED_WORDS = {("1", "2"): "a half", ("1", "4"): "a quarter", ("3", "4"): "three quarters",
                ("1", "3"): "a third", ("2", "3"): "two thirds"}


def _plural(u):
    u = _UNIT_FULL.get(u, u)
    return u if u.endswith("s") else u + "s"


def _mixed(m):
    w, n, d = m.group(1), m.group(2), m.group(3)
    out = "%s and %s" % (w, _MIXED_WORDS.get((n, d)) or "\x01%s/%s" % (n, d))
    if m.lastindex and m.lastindex >= 4 and m.group(4):
        out += " " + _plural(m.group(4))
    return out


def _frac_unit(m):
    n, d, u = m.group(1), m.group(2), m.group(3)
    u = _UNIT_FULL.get(u, u)
    if u.endswith("s"):
        return "%s/%s %s" % (n, d, u)
    if (n, d) == ("1", "2"):
        return "half a%s %s" % ("n" if u[0] in "aeiouh" and u == "hour" else "", u)
    return "%s of a%s %s" % (_frac(n, d), "n" if u == "hour" else "", u)


_NTH = {"2": "half", "3": "3rd", "4": "quarter"}

_FAMILY = [
    # generated families: comparing, fraction of a number, same-denominator sums
    (r"Find common denominator: LCM of (\d+) and (\d+) = (\d+)",
     lambda m: "Find the common denominator. The L C M of %s and %s is %s." % m.groups()),
    (r"Convert: (\d+)/(\d+) = (\d+)/(\d+), (\d+)/(\d+) = (\d+)/(\d+)",
     lambda m: "Convert. %s over %s equals %s over %s, and %s over %s equals %s over %s." % m.groups()),
    (r"Compare numerators: (\d+) vs (\d+)\. So (\d+)/(\d+) is greater\.",
     lambda m: "Compare the numerators, %s and %s. So %s over %s is greater." % m.groups()),
    (r"Think: one-(\d+)th of (\d+) is (\d+)\. Now take (\d+) of those\.",
     lambda m: "Think: one %s of %s is %s. Now take %s of those." % (
         _NTH.get(m.group(1)) if m.group(1) in ("3",) else m.group(1) + "th", m.group(2), m.group(3), m.group(4))),
    (r"Same denominators, so add numerators: \((\d+)\+(\d+)\)/(\d+) = (\d+)/(\d+)",
     lambda m: "The denominators are the same, so add the numerators. %s plus %s, all over %s, equals %s over %s." % m.groups()),
    (r"Same denominators, so subtract numerators: \((\d+)[−-](\d+)\)/(\d+) = (\d+)/(\d+)",
     lambda m: "The denominators are the same, so subtract the numerators. %s minus %s, all over %s, equals %s over %s." % m.groups()),
    (r"Simplify: (\d+)/(\d+) = (\d+)/(\d+)",
     lambda m: "Simplify. %s over %s equals %s over %s." % m.groups()),
    (r"Simplify: (\d+)/(\d+) = (\d+)",
     lambda m: "Simplify. %s over %s equals %s." % m.groups()),
    (r"Simplify: (\d+)/(\d+) ([+−-]) (\d+)/(\d+)",
     lambda m: "Simplify: %s over %s, %s %s over %s." % (m.group(1), m.group(2), "plus" if m.group(3) == "+" else "minus", m.group(4), m.group(5))),
    (r"Add: (\d+) \+ (\d+) = (\d+)\. Keep denominator (\d+)\.",
     lambda m: "Add: %s plus %s equals %s. Keep the denominator, %s." % m.groups()),
    (r"Subtract: (\d+) [−-] (\d+) = (\d+)\. Keep denominator (\d+)\.",
     lambda m: "Subtract: %s minus %s equals %s. Keep the denominator, %s." % m.groups()),
    (r"LCM of (\d+) and (\d+) will help\.",
     lambda m: "The L C M of %s and %s will help." % m.groups()),
    (r"Divide (\d+) by (\d+): (\d+) ÷ (\d+) = (\d+)",
     lambda m: "Divide %s by %s. %s divided by %s equals %s." % m.groups()),
    (r"Multiply by (\d+): (\d+) × (\d+) = (\d+)",
     lambda m: "Multiply by %s. %s times %s equals %s." % m.groups()),
    (r"Denominator multiplied by (\d+): (\d+) × (\d+) = (\d+)",
     lambda m: "The denominator is multiplied by %s. %s times %s equals %s." % m.groups()),
    (r"So numerator also × (\d+): (\d+) × (\d+) = (\d+)",
     lambda m: "So the numerator is also multiplied by %s. %s times %s equals %s." % m.groups()),
    (r"Find the missing number: (\d+)/(\d+) = \?/(\d+)",
     lambda m: "Find the missing number. %s over %s equals what, over %s?" % m.groups()),
    (r"Which is greater: (\d+)/(\d+) or (\d+)/(\d+)\?",
     lambda m: "Which is greater, %s over %s or %s over %s?" % m.groups()),
    (r"(\w+) given = (\d+)/(\d+) of (\d+) = (\d+)",
     lambda m: "%s given equals %s of %s, which is %s." % (m.group(1), _frac(m.group(2), m.group(3)), m.group(4), m.group(5))),
    (r"Remaining = (\d+) − (\d+) = (\d+)",
     lambda m: "Remaining equals %s minus %s, which is %s." % m.groups()),
]


def family(text):
    s = (text or "").strip()
    for pat, fn in _FAMILY:
        m = re.fullmatch(pat, s)
        if m:
            return fn(m)
    return None


def from_latex(latex):
    """A maths line written in LaTeX, as the print it stands for."""
    s = latex or ""
    s = re.sub(r"\\boxed\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"\1", s)
    s = re.sub(r"\s*\\text\s*\{\s*and\s*\}\s*", ", and ", s)
    s = re.sub(r"\\text\s*\{([^{}]*)\}", r" \1 ", s)
    s = re.sub(r"\\d?frac\s*\{([^{}]*\\(?:times|div)[^{}]*|[^{}]*[+-][^{}]*)\}\s*\{([^{}]*)\}", r" (\1)/(\2) ", s)
    s = re.sub(r"(\d)\s*\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\1 \2/\3", s)
    s = re.sub(r"\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r" \1/\2 ", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\cdot", "×").replace("\\%", "%")
    s = re.sub(r"\\(?:Rightarrow|rightarrow|to|implies)\b", "→", s)
    s = re.sub(r"\s*\\q?quad\s*", ", ", s)
    s = re.sub(r"\\(?:,|;|:|!)", " ", s).replace("\\ ", " ")
    s = s.replace("\\left", "").replace("\\right", "").replace("\\", "")
    s = re.sub(r"(?<=[\d\s)])-(?=[\s\d(])", "−", s)
    return re.sub(r"\s+", " ", s).strip()


def say(text, sentence=False):
    s = (text or "").strip()
    if not s:
        return ""
    s = s.replace("\n", " ")
    s = re.sub(r"=\s*\?(?=\s*$|\s*[.,])", "= what?", s)
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    s = re.sub(r"\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\1/\2", s)
    s = s.replace("\\times", "×").replace("\\div", "÷")
    s = s.replace("-", "−") if re.fullmatch(r"-\d+(\.\d+)?", s) else s
    for k, v in {"½": " 1/2 ", "¼": " 1/4 ", "¾": " 3/4 ", "⅓": " 1/3 ", "⅔": " 2/3 ", "²": " squared ", "³": " cubed "}.items():
        s = s.replace(k, v)
    s = s.replace("✓", " ").replace("✗", " ").replace("✔", " ").replace("…", ".").replace("—", ", ").replace("–", "−")
    s = re.sub(r"_{2,}", " blank ", s)
    s = re.sub(r"(?:₹|Rs\.?)\s*(\d[\d,]*\d(?:\.\d+)?|\d(?:\.\d+)?)", r"\1 rupees", s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(\d)\s*°", r"\1 degrees", s)
    # mixed numbers and fractions that carry a unit: '5 1/4 m', '7/8 litre', '1/2 litre'
    s = re.sub(r"\b(\d+) (\d+)/(\d+)\s*" + _UNIT, _mixed, s)
    s = re.sub(r"(?<![\d/] )(?<![\d/])\b(\d+)/(\d+)\s*" + _UNIT, _frac_unit, s)
    for pat, rep in _ABBREV:
        s = re.sub(pat, rep, s)
    s = re.sub(r"\b(\d{1,2}):(\d\d)\b", r"\1 \2", s)                       # clock times
    s = re.sub(r"\bvs\.?\s", "and ", s)
    # clause by clause, so that '=' chains read naturally
    pieces = re.split(r"([.?!:;,]\s+|\s+(?:and|so|but|then|because|since|or)\s+)", s)
    s = "".join(p if i % 2 else _equals(p) for i, p in enumerate(pieces))
    # brackets over a number: (7+1)/9
    s = re.sub(r"\(([^()]+)\)\s*/\s*\(([^()]+)\)", r"\1, all over \2", s)
    s = re.sub(r"\(([^()]+)\)\s*/\s*(\d+|[a-z]\b)", r"\1, all over \2", s)
    # mixed numbers, then fractions
    s = re.sub(r"\b(\d+)\s*\((\d+)\s*/\s*(\d+)\)", r"\1 and \2/\3", s)     # 1(11/19)
    s = re.sub(r"\b(\d+) (\d+)\s*/\s*(\d+)", _mixed, s)
    s = re.sub(r"\b(is|are|equals?):$", r"\1 what?", s)
    s = re.sub(r"(?<!\x01)\b(\d+)/(\d+) (full|empty)\b", lambda m: "%s %s" % (_frac(m.group(1), m.group(2)), m.group(3)), s)
    s = re.sub(r"(?<!\x01)\b(\d+)/(\d+) and (\d+)/(\d+) of ",
               lambda m: "%s and %s of " % (_frac(m.group(1), m.group(2)), _frac(m.group(3), m.group(4))), s)
    s = re.sub(r"(?<!\x01)\b(\d+)\s*/\s*(\d+)\s+of\s+", _of_word, s)
    s = s.replace("\x01", "")
    s = re.sub(r"(\d+)\s*/\s*(\d+)\s*(st|nd|rd|th)\b", r"\1/\2", s)        # '4/7 th full'
    s = re.sub(r"(\d+)\s*/\s*(\d+)\s*(?=[+−×÷])", r"\1 over \2, ", s)     # a pause after a fraction in a sum
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    s = re.sub(r"\b([A-Za-z])\s*/\s*(\d+|[A-Za-z]\b)", r"\1 over \2", s)   # W/23, a/b
    s = re.sub(r"\?\s*/\s*(\d+)", r"what, over \1", s)
    s = re.sub(r"(\d+)\s*/\s*\?", r"\1 over what", s)
    s = re.sub(r"□\s*/\s*(\d+)", r"box over \1", s)
    s = re.sub(r"(\d+)\s*/\s*□", r"\1 over box", s)
    s = re.sub(r"★\s*/\s*(\d+)", r"star over \1", s)
    s = re.sub(r"(\d+)\s*/\s*★", r"\1 over star", s)
    s = re.sub(r"(\d)\(", r"\1 times (", s)                               # 3(5)
    s = s.replace("□", " the box ").replace("★", " the star ").replace("△", " triangle ")
    s = re.sub(r":$", ".", s)
    s = re.sub(r"\s*(?:→|⇒|➜)\s*", ", so ", s)
    for k, v in _OPS:
        s = s.replace(k, v)
    s = re.sub(r"(\d)\s*-\s*(?=\d)", r"\1 minus ", s)
    s = re.sub(r"[()\[\]{}]", ", ", s)
    s = s.replace("/", " or ").replace("*", "").replace("|", ", ")
    s = tidy(s)
    # balance the pauses in a sum of fractions: '1 over 7, plus 2 over 7, equals 3 over 7'
    s = re.sub(r"((?:plus|minus|times|divided by) \d+ over \d+) equals\b", r"\1, equals", s)
    s = re.sub(r"(all over \d+) equals\b", r"\1, equals", s)
    s = re.sub(r"(, (?:plus|minus|times|divided by) [^,.;:?]*?) equals\b", r"\1, equals", s)
    s = re.sub(r"(, all over [^,.;:?]*?) equals\b", r"\1, equals", s)
    s = re.sub(r"\b(\d+ divided by \d+) times (\d+)", r"\1, times \2,", s)
    s = re.sub(r"(, which is [^,.;:?]+), which is ", r"\1, or ", s)
    s = re.sub(r"\b(\d+) (metre|litre|kilometre|kilogram|gram)s (piece|can|jug|bottle|rope|ribbon|stick|bag|packet|ride|walk|run|race|trip|journey|track)\b", r"\1 \2 \3", s)
    s = re.sub(r"(?<![\d.] )(?<![\d.])(?<!over )\b1 (metre|litre|kilometre|kilogram|gram|hour|minute|cup|centimetre|millimetre|millilitre|rupee)s\b", r"1 \1", s)
    s = re.sub(r"\b(\d+) rupees (coins?|notes?)\b", r"\1 rupee \2", s)
    s = re.sub(r"^This is from the (\d+) IPM exam, Q(\d+)\.$", r"This is from the \1 I P M exam, question \2.", s)
    s = re.sub(r"^Correct answer: Option (\d)[,.]? ", r"The correct answer is option \1, ", s)
    s = re.sub(r"\bIPM\b", "I P M", s)
    s = re.sub(r"^Answer: ([A-D])\.?$", r"The answer is \1.", s)
    s = re.sub(r"\b[A-Z]{4,}\b", lambda m: m.group(0).lower(), s)
    s = re.sub(r"\bNOT\b", "not", s)
    s = re.sub(r"[,;:]$", "", s)
    s = tidy(_and_list(s))
    if sentence and " " in s and s[-1].isalnum():
        s += "."
    return s


_ITEM = r"[^,.?:;!]*\d[^,.?:;!]*"


def _and_list(s):
    """'..., 2 over 3, 3 over 4' at the end of a line becomes '..., 2 over 3 and 3 over 4.'"""
    m = re.search(r"(?:^|[?:] )((?:%s, ){2,}%s)([.?]?)$" % (_ITEM, _ITEM), s) or \
        re.search(r"^((?:%s, )+%s)()$" % (_ITEM, _ITEM), s)
    if not m:
        return s
    items = m.group(1).split(", ")
    if any(len(i.split()) > 6 or re.search(r"\b(?:or|so|is|equals)\b", i) for i in items) or " and " in items[-1]:
        return s
    if any(" and " in i for i in items) and not all(re.search(r"\d and ", i) for i in items if " and " in i):
        return s
    head = s[:m.start(1)]
    out = head + ", ".join(items[:-1]) + (" or " if m.group(2) == "?" or head.rstrip().endswith("?") else " and ") + items[-1]
    return out + (m.group(2) or ("." if head else ""))
