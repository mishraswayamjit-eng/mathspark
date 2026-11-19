"""Rules that turn printed Grade 4 geometry work (quadrilaterals) into speech. Used by gr4_quads.py.

    say(text)          the general converter for this topic's notation
    from_latex(latex)  a step's maths line, as the print it stands for
"""
import re

_WORDS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters",
          ("1", "3"): "one third", ("2", "3"): "two thirds"}

_UNIT_NAMES = {"cm": "centimetres", "mm": "millimetres", "km": "kilometres", "m": "metres",
               "kg": "kilograms", "g": "grams", "ml": "millilitres", "mL": "millilitres",
               "units": "units", "unit": "units", "ft": "feet"}
_SINGULAR = {"centimetres": "centimetre", "millimetres": "millimetre", "kilometres": "kilometre", "metres": "metre",
             "kilograms": "kilogram", "grams": "gram", "millilitres": "millilitre", "units": "unit", "feet": "foot",
             "degrees": "degree"}

# things a measurement can describe: '5 m gaps' is 'five metre gaps', not 'five metres gaps'
_THINGS = (r"(?:path|paths|gap|gaps|rope|ropes|wire|wires|tile|tiles|square|squares|rectangle|rectangles|angle|angles|"
           r"length|width|strip|strips|side|sides|lawn|sheet|ruler|ribbon|circle|circles|string|line|radius|diameter)")


def _unit(u, n=None):
    name = _UNIT_NAMES.get(u, u)
    return _SINGULAR.get(name, name) if n == "1" else name


def _sq(m):
    return "%s square %s" % (m.group(1), _unit(m.group(2), m.group(1)))


def _plain(m):
    return "%s %s" % (m.group(1), _unit(m.group(2), m.group(1)))


_NUM = r"(\d[\d,]*(?:\.\d+)?)"
_LONG = r"(centimetres|millimetres|kilometres|metres|degrees|feet)"

_ABBREV = [
    (r"\bLCM\b", "L C M"), (r"\bHCF\b", "H C F"), (r"\bIPM\b", "I P M"),
    (r"\bRHS\b", "the right-hand side"), (r"\bLHS\b", "the left-hand side"),
    (r"\be\.g\.,?", "for example,"), (r"\bi\.e\.,?", "that is,"),
    (r"\bvs\.?(?=\s)", "and"),
    (r"\bQ\.?\s*(\d+)\b", r"question \1"),
]

_OPS = [("×", " times "), ("÷", " divided by "), ("+", " plus "), ("−", " minus "), ("≈", " is about "),
        ("<", " is less than "), (">", " is greater than "), ("≠", " is not equal to "),
        ("≤", " is at most "), ("≥", " is at least "), ("∥", " is parallel to "), ("⊥", " is perpendicular to ")]

_EXPR_TAIL = re.compile(r"^(.*[A-Za-z,])\s+((?:\d[\d.,]*|[()×÷+−/\s])+)$")
_NOT_INSIDE = re.compile(r"\b(?:Use|Check|Verify|Try|First|Then|Now|Next|Since|Here|and|so|because|since)$")
_VERB = re.compile(r"\b(?:is|are|was|were|has|have|had|gives?|makes?|gets?|be|costs?|means|becomes)\s+(?:about\s+)?[\d(]")


def _frac(n, d):
    return _WORDS.get((n, d)) or "%s over %s" % (n, d)


def _mode(left, previous, joiner):
    """How the first '=' of a clause is said: 'equals' after a name or a bare sum, 'which is' inside a sentence."""
    if not left.strip():
        return "that"
    if _VERB.search(left):
        return "which"
    m = _EXPR_TAIL.match(left.strip())
    if m and re.search(r"[×÷+−]", m.group(2)) and not _NOT_INSIDE.search(m.group(1).strip()):
        return "which"
    if previous == "which" and joiner.strip() == "and" and not re.search(r"[A-Za-z]{2}", left):
        return "which"
    return "equals"


def _equals(clause, mode):
    parts = clause.split("=")
    tail = re.search(r"\s*$", clause).group(0)
    if mode == "that":
        out = "That equals " + parts[1].strip()
    elif mode == "which":
        out = parts[0].rstrip() + ", which is " + parts[1].strip()
    else:
        out = parts[0].rstrip() + " equals " + parts[1].strip()
    for p in parts[2:]:
        out = out.rstrip() + ", which is " + p.strip()
    return out + tail


def tidy(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r":\s*,", ":", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"\.(?:\s*\.)+", ".", s)
    s = re.sub(r"([,?!:;])(?=[A-Za-z])", r"\1 ", s)
    s = re.sub(r"^[,;:]\s*", "", s)
    s = re.sub(r"[,;]$", "", s)
    s = re.sub(r"([.?!] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    if s:
        s = s[0].upper() + s[1:]
    return s


def from_latex(latex):
    """A maths line written in LaTeX, as the print it stands for."""
    s = latex or ""
    s = re.sub(r"\\boxed\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", r"\1", s)
    s = re.sub(r"\\text\s*\{([^{}]*)\}", r" \1 ", s)
    s = re.sub(r"(\d)\s*\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\1 \2/\3", s)
    s = re.sub(r"\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r" \1/\2 ", s)
    s = s.replace("^\\circ", "°").replace("^{\\circ}", "°").replace("\\circ", "°").replace("\\angle", "∠").replace("\\triangle", "△")
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\cdot", "×").replace("\\%", "%")
    s = s.replace("\\parallel", "∥").replace("\\perp", "⊥").replace("\\neq", "≠").replace("\\pi", "π").replace("\\sqrt", "√")
    s = re.sub(r"\^\s*\{?2\}?", "²", s)
    s = re.sub(r"\\(?:Rightarrow|rightarrow|to|implies)\b", "→", s)
    s = re.sub(r"\s*\\q?quad\s*", ". ", s)                                 # two sums side by side
    s = re.sub(r"\\(?:,|;|:|!)", " ", s).replace("\\ ", " ")
    s = s.replace("\\left", "").replace("\\right", "").replace("\\", "")
    s = re.sub(r"(?<![\w)°])-(?=\s*\d)", "−", s)
    s = re.sub(r"(?<=[\w)°])\s*-\s*(?=[\d(a-zA-Z])", " − ", s)
    return re.sub(r"\s+", " ", s).strip()


def say(text):
    s = (text or "").strip()
    if not s:
        return ""
    s = s.replace("\n", " ")
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    s = re.sub(r"\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\1/\2", s)
    s = s.replace("\\times", "×").replace("\\div", "÷")
    if re.fullmatch(r"-\d+(\.\d+)?.*", s):
        s = "−" + s[1:]
    for k, v in {"½": " 1/2 ", "¼": " 1/4 ", "¾": " 3/4 ", "⅓": " 1/3 ", "⅔": " 2/3 "}.items():
        s = s.replace(k, v)
    s = s.replace("✓", " ").replace("✗", " ").replace("✔", " ").replace("…", ".").replace("—", ", ").replace("–", "−")
    s = s.replace("&", " and ")
    s = re.sub(r"_{2,}", " blank ", s)
    if re.search(r"\dn\b", s):                                              # algebra in m and n: m is a letter, not metres
        s = re.sub(r"(\d)m\b", "\\1 \x02", s)
    s = re.sub(r"^Answer\s*=\s*", "The answer is ", s)
    s = re.sub(r"(\d)\s+-\s+(?=\d)", r"\1 − ", s)                           # a hyphen used as a minus sign
    s = re.sub(r"(?<=[\d)]) x (?=[\d(])", " × ", s)                         # a letter x used as a times sign
    s = re.sub(r"(?<=\d) x (?=(?:breadth|length|side|width)\b)", " × ", s)
    s = re.sub(r"\b(breadth|length|side|width) x (?=(?:breadth|length|side|width)\b)", r"\1 × ", s)
    s = re.sub(r"(?:₹|Rs\.?)\s*(\d[\d,]*\d(?:\.\d+)?|\d(?:\.\d+)?)", r"\1 rupees", s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(\d)\s*°", r"\1 degrees", s)
    s = s.replace("°", " degrees ")
    # units: square ones first
    s = re.sub(_NUM + r"\s*(cm|mm|km|m|units?)\s*(?:²|\^2)", _sq, s)
    s = re.sub(_NUM + r"\s*(cm|mm|km|m)[. ]\s*sq\b", _sq, s)               # '1089 cm.sq', '168cm sq'
    s = re.sub(_NUM + r"\s*sq\.?\s*(cm|mm|km|m|units?)\b", _sq, s)
    s = re.sub(r"\b(cm|mm|km|m)\s*(?:²|\^2)", lambda m: "square " + _unit(m.group(1)), s)
    s = re.sub(r"\bunits?\s*(?:²|\^2)", "square units", s)
    s = re.sub(r"\bsq\.?\s*(cm|mm|km|m|units?)\b", lambda m: "square " + _unit(m.group(1)), s)
    s = re.sub(r"\bsquare (cm|mm|km)\b", lambda m: "square " + _unit(m.group(1)), s)
    s = re.sub(_NUM + r"\s*(cm|mm|km|kg|ml|mL|ft|m|g)\b", _plain, s)
    s = re.sub(r"\b(cm|mm|km|kg|ml)\b", lambda m: _unit(m.group(1)), s)
    s = re.sub(r"(square (?:centi|milli|kilo)?metres),? \(square \w+\)", r"\1", s)   # 'sq.cm (square centimetres)'
    # a measurement used to describe a thing: 'a 1 m path', 'the 70° angle', 'a 4 cm by 1 cm rectangle'
    s = re.sub(_NUM + " " + _LONG + r" by " + _NUM + " " + _LONG + r"(?= (?:rectangle|rectangles|sheet|lawn)\b)",
               lambda m: "%s %s by %s %s" % (m.group(1), _SINGULAR[m.group(2)], m.group(3), _SINGULAR[m.group(4)]), s)
    s = re.sub(_NUM + " " + _LONG + r"(?= " + _THINGS + r"\b)", lambda m: "%s %s" % (m.group(1), _SINGULAR[m.group(2)]), s)
    s = s.replace("²", " squared ").replace("³", " cubed ")
    for pat, rep in _ABBREV:
        s = re.sub(pat, rep, s)
    # words printed in capitals for stress are ordinary words to the voice
    s = re.sub(r"\b[A-Z]{2,}\b", lambda m: m.group(0).lower(), s)
    s = re.sub(r"√\s*(\d[\d,]*|[A-Za-z]+)", r"the square root of \1", s)
    s = re.sub(r"(\d)([a-zA-Z])\b", r"\1 \2", s)                             # 3a, 4s, 2L
    s = re.sub(r"\b(\d{1,2}):(\d\d)\b", r"\1 \2", s)                        # clock times
    s = re.sub(r"(\d) : (\d)", r"\1 is to \2", s)                           # ratios
    s = re.sub(r"\s*(?:→|⇒|➜|➔)\s*", ", so ", s)
    s = re.sub(r"\+\s*\?\s*=", "+ what =", s)
    s = re.sub(r"(\d)\s*[(\[](\d[\d.]*)[)\]]", r"\1 × \2", s)               # 2(21), 3(5)
    s = re.sub(r"(\d)\[(\d+)([a-z])\]", r"\1 × \2\3", s)                    # 2[4a]
    s = re.sub(r"(?<!\w)'(\w[^']*?)'(?!\w)", r"\1", s)                      # quotation marks, not apostrophes
    s = re.sub(r"=\s*\?", "= what?", s)
    # clause by clause, so that '=' chains read naturally
    pieces = re.split(r"([.?!:;,]\s+|\s+(?:and|so|but|then|because|since|or)\s+)", s)
    out, previous = [], None
    for i, p in enumerate(pieces):
        if i % 2 or "=" not in p:
            out.append(p)
            if not i % 2 and re.search(r"[A-Za-z]{2}", p):
                previous = None
            continue
        previous = _mode(p.split("=")[0], previous, pieces[i - 1] if i else "")
        out.append(_equals(p, previous))
    s = "".join(out)
    s = re.sub(r"\(([^()]+)\)\s*/\s*(\d+)", r"\1, all over \2", s)
    s = re.sub(r"\b(\d+) (\d+)\s*/\s*(\d+)", lambda m: "%s and %s" % (m.group(1), _frac(m.group(2), m.group(3))), s)
    s = re.sub(r"\b(\d+)\s*/\s*(\d+)\s+of\s+", lambda m: _frac(m.group(1), m.group(2)) + " of ", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", lambda m: _frac(m.group(1), m.group(2)), s)
    s = re.sub(r"\b([A-Za-z])\s*/\s*(\d+|[A-Za-z]\b)", r"\1 over \2", s)    # d/2, C/d
    s = re.sub(r"(\d|\b[a-zA-Z])\((?=[\w(])", r"\1 times (", s)             # 2(l + b)
    s = re.sub(r"\)\s*\(", ") times (", s)
    for k, v in _OPS:
        s = s.replace(k, v)
    s = re.sub(r"(\d)\s*-\s*(?=\d)", r"\1 minus ", s)
    s = re.sub(r"[()\[\]{}]", ", ", s)
    s = s.replace("/", " or ").replace("*", "").replace("|", ", ").replace("π", " pi ")
    s = re.sub(r"[\"“”]", "", s).replace("\x02", "m")
    return tidy(s)
