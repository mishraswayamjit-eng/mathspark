"""Rules for the imported Grade 5 questions of squares-patterns (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

These are one-off word problems, so there are no templates: `say` turns one printed string into
speech, and `say_latex` does the same for a step's maths line. Hand-written lines in
squares_patterns_imported*.py replace whatever still does not sound right.
"""
import re

IMPORTED_PREFIXES = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")

# Capitals that are abbreviations, not emphasis.
_ABBREV = {"AP": "A P", "GP": "G P", "HCF": "H C F", "LCM": "L C M", "IPM": "I P M", "BODMAS": "BODMAS",
           "LED": "L E D"}

_SUPER = {"⁰": " to the power zero", "¹": " to the power one", "⁴": " to the power four", "⁵": " to the power five"}
_SUB = {"₀": " zero", "₁": " one", "₂": " two", "₃": " three", "₄": " four", "₅": " five", "₆": " six",
        "₇": " seven", "₈": " eight", "₉": " nine", "ₙ": " n"}

_OPS = "+−×÷"
_OPEN, _CLOSE = "\x01", "\x02"      # round brackets that are only punctuation, put back at the end
_INNER = re.compile(r"\(([^()]*)\)(²)?")
_OVER, _ALLOVER, _SO, _FAIL = "\x03", "\x04", "\x05", "\x06"   # marks say_latex passes through say
_OB, _CB, _ALLSQ, _PAUSE = "\x07", "\x08", "\x0e", "\x0f"       # spoken brackets, written out at the end
_LINKING = re.compile(r"\b(?:is|are|was|be|has|had|have|becomes|makes it)\s+(?:always |just |only |now )?(?:[\d√]|the square root)[^=(]*$")


def _caps(m):
    word = m.group(0)
    if word in _ABBREV:
        return _ABBREV[word]
    start = m.start() == 0 or m.string[max(0, m.start() - 2):m.start()].strip() in (".", "!", "?")
    return word.capitalize() if start else word.lower()


def _brackets(s):
    """Say brackets that group maths; drop or keep the ones that are punctuation."""
    while True:
        m = _INNER.search(s)
        if not m:
            return s
        inner, squared = m.group(1).strip(), m.group(2)
        before, after = s[:m.start()], s[m.end():]
        has_op = bool(re.search(r"[+−×÷]|\s-\s|\d-\d|/", inner)) and "=" not in inner and "," not in inner
        stuck_before = bool(re.search(r"[\dA-Za-z²]$", before)) and not re.search(r"\b[A-Za-z]{2,}$", before)
        stuck_after = bool(re.match(r"[A-Za-z\d]", after))
        near_op = bool(re.search(r"[+−×÷/]\s*$|\s-\s*$", before)) or bool(re.match(r"\s*[×÷/+−]|\s-\s", after))
        lead = " times " if stuck_before else " "
        tail = " times " if stuck_after else " "
        if squared:
            if has_op and re.search(r"[+−×÷/]\s*$", before):
                piece = lead + _OB + inner + _CB + " squared " + tail      # "N² − (N − 1)²"
            elif has_op:
                piece = lead + inner + _ALLSQ + tail
            else:
                piece = lead + inner + " squared " + tail
        elif re.fullmatch(r"\w+\s*/\s*\w+", inner) and (near_op or stuck_before or stuck_after):
            piece = lead + inner + _PAUSE + tail
        elif has_op and (near_op or stuck_before or stuck_after):
            piece = lead + _OB + inner + _CB + tail
        elif has_op and (re.fullmatch(r"(?:[A-Za-z'-]{2,}|[\s+−×÷])+", inner) or re.match(r"[×÷+]", inner)):
            piece = _OPEN + inner + _CLOSE          # words only: an aside, "(courtyard + path)"
        elif has_op and re.match(r"(?:which|that|since|because|so|or|i\.e|like)\b", inner):
            piece = _OPEN + inner + _CLOSE          # an aside that happens to hold a sum
        elif has_op or (stuck_before and re.fullmatch(r"[\d.,]+|[a-z]", inner)):
            piece = lead + inner + tail
        else:
            piece = _OPEN + inner + _CLOSE
        s = before + piece + after


def _equals_chain(s):
    """'a = b = c' in one clause becomes 'a equals b, which equals c'."""
    out = []
    for clause in re.split(r"([.;:!?]['\"’”]?(?:\s|$)|,\s| and | so | then | but | means | meaning | because | since "
                           r"| where | while | which | if | when |" + _SO + ")", s):
        parts = clause.split("=")
        text = parts[0]
        # "the total is 12 × 12 = 144": the sum is already the thing being named.
        first = not (len(parts) > 1 and _LINKING.search(parts[0]))
        for p in parts[1:]:
            text += ("=" if first else ", which equals ") + p
            first = False
        out.append(text)
    return "".join(out)


def say(text):
    """One printed string as speech. The caller checks the numbers and hand-writes what fails."""
    s = text or ""
    if not s.strip():
        return ""
    s = re.sub(r"(?<![.!?:,;\s])[ \t]*\n\s*", ". ", s.strip())
    s = s.replace("\n", " ")
    s = re.sub(r"(?<![\w(])([A-D])\)\s+", r"\1, ", s)          # "C) 2": a lettered answer choice
    s = re.sub(r"(\d)!(?=\s*=)", r"\1 factorial", s)
    s = re.sub(r"\be\.g\.,?", "for example,", s)
    s = re.sub(r"\bi\.e\.,?", "that is,", s)
    s = re.sub(r",?\s*\betc\.(?=\s+[A-Z]|$)", ", and so on.", s)
    s = re.sub(r",?\s*\betc\.?", ", and so on", s)
    # Emphasis marks and blanks.
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*([A-Za-z][^*]*?)\*", r"\1", s)
    s = re.sub(r"\[box\]|_{2,}", " blank ", s)
    s = re.sub(r"\*\s*marks?\b", lambda m: "star " + m.group(0).lstrip("* "), s)
    s = s.replace("*", " star ")
    s = re.sub(r"\b([A-Za-z])_\{?(\w+)\}?", lambda m: ("A" if m.group(1) == "a" else m.group(1)) + " " + m.group(2), s)
    s = re.sub(r"\ba(?=[₀-₉ₙ])", "A", s)
    for k, v in _SUB.items():
        s = s.replace(k, v)
    for k, v in _SUPER.items():
        s = s.replace(k, v)
    # Money and units.
    s = re.sub(r"(?:₹|Rs\.?)\s*(1)(?![\d,.]*\d)", r"\1 rupee", s)
    s = re.sub(r"(?:₹|Rs\.?)\s*([\d,]*\d(?:\.\d+)?)", r"\1 rupees", s)
    s = re.sub(r"\bsq\.?\s*cm\b", "square centimetres", s)
    s = re.sub(r"\bsq\.?\s*mm\b", "square millimetres", s)
    s = re.sub(r"\bmm\b", "millimetres", s)
    s = re.sub(r"\bsq\.?\s*m\b", "square metres", s)
    s = re.sub(r"\bsq\.?\s*units?\b", "square units", s)
    s = re.sub(r"(?<=\d)\s*cm\b", " centimetres", s)
    s = re.sub(r"\bcm\b", "centimetres", s)
    s = re.sub(r"(?<=\d)\s*km\b", " kilometres", s)
    s = re.sub(r"(?<=\d)\s*m\b", " metres", s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(?<![\d.,])1 ((?:square )?(?:centi|milli|kilo)?metre)s\b", r"1 \1", s)
    # Capitals used for emphasis.
    s = re.sub(r"\b[A-Z]{2,}\b", _caps, s)
    # Roots and powers.
    s = re.sub(r"√\s*\(\s*([\d,]+)\s*\)", r"√\1", s)
    s = re.sub(r"√\s*([A-Za-z\d][\d,]*(?:\.\d+)?)", r"the square root of \1", s)
    s = s.replace("√", "the square root of ")
    s = re.sub(r"\^\s*\{?2\}?", "²", s)
    s = re.sub(r"\^\s*\{?3\}?", "³", s)
    s = re.sub(r"\^\s*\{?(\d+)\}?", r" to the power \1", s)
    # The letter a as a variable is written as a capital, so the voice says the letter.
    s = re.sub(r"\ba(?=\s?[=²+−×÷)]|\s-\s)", "A", s)
    s = re.sub(r"(?<=[+−×÷])a\b", "A", s)
    s = re.sub(r"(?<=[+−×÷] )a\b", "A", s)
    s = re.sub(r"\ba and b\b", "A and b", s)
    s = re.sub(r"(\d)a\b", r"\1 A", s)
    s = re.sub(r"(\d)ab\b", r"\1 A b", s)
    # A grid is "15 by 15"; a sum is "15 times 15".
    s = re.sub(r"\b(\d+|n)\s*×\s*(\d+|n)(?=\s+(?:grid|square|arrangement|tray|array|formation|rangoli|garden|pattern)\b)", r"\1 by \2", s)
    s = re.sub(r"(\d+) ([a-z]+)\s*×\s*(\d+) \2\b(?!\s*=)", r"\1 \2 by \3 \2", s)
    s = re.sub(r"\((\d+)\s*×\s*(\d+)\)(?!\s*[+−×÷=²])", r"(\1 by \2)", s)
    # Dashes.
    s = re.sub(r"(?:(?<=[\d)²])|(?<=\b[A-Za-z]))\s+-\s+(?=[\d(]|[A-Za-z](?![A-Za-z]))", " − ", s)
    s = re.sub(r"(\d)\s*–\s*(\d)", r"\1 to \2", s)
    s = re.sub(r"\b\d(?:-\d){2,}\b", lambda m: m.group(0).replace("-", ", "), s)
    s = re.sub(r"(\d)-(\d)", r"\1 − \2", s)
    s = re.sub(r"\s*—\s*", ", ", s)
    s = re.sub(r"\s+–\s+", ", ", s)
    # Sums that run on: "a = b = c".
    s = re.sub(r"=\s*\?,", " equals what,", s)
    s = re.sub(r"=\s*\?\s*\.?", " equals what? ", s)
    s = re.sub(r"(\b[Dd]oes [^=?.!]*?)\s*=\s*", r"\1 equal ", s)
    s = _equals_chain(s)
    # Brackets, then letters stuck to numbers.
    s = _brackets(s)
    s = s.replace(_OB, " open bracket, ").replace(_CB, ", close bracket, ")
    s = s.replace(_ALLSQ, ", all squared, ").replace(_PAUSE, ", ")
    s = re.sub(r"(\d)([bdknxyN])\b(?!')", r"\1 \2", s)
    s = s.replace("²", " squared").replace("³", " cubed")
    # Fractions and division by slash.
    s = re.sub(r"(\d+|\b[a-z])\s*/\s*(\d+)", r"\1 over \2", s)
    s = s.replace("/", " divided by ")
    # Sequences.
    s = re.sub(r",\s*\?(?=\s*[,.]|\s*$)", ", blank", s)             # a "?" standing in a list
    s = re.sub(r",\s*(?:…|\.\.\.)\s*\?", ", and so on?", s)
    s = re.sub(r"\s*[+]\s*(?:…|\.\.\.)\s*", ", and so on, ", s)
    s = re.sub(r",\s*(?:…|\.\.\.)\s*(?=[A-Z])", ", and so on. ", s)
    s = re.sub(r",\s*(?:…|\.\.\.)\s*", ", and so on, ", s)
    s = re.sub(r"(,\s*\d[\d.]*(?:st|nd|rd|th)?)\s*(?:…|\.\.\.)\s*(?=[A-Z])", r"\1, and so on. ", s)
    s = re.sub(r"(,\s*\d[\d.]*(?:st|nd|rd|th)?)\s*(?:…|\.\.\.)\s*", r"\1, and so on, ", s)
    s = re.sub(r"\s*(?:…|\.\.\.)\s*(?=[A-Z])", ". ", s)   # dots that are only a pause
    s = re.sub(r"\s*(?:…|\.\.\.)\s*", ", ", s)
    s = re.sub(r"\s*→\s*\?", ", then what?", s)
    s = re.sub(r"(\d|\ds|blank)\s*→\s*(?=\d|blank|[a-z]+ \d)", r"\1, then ", s)
    s = re.sub(r"\s*→\s*", ", which gives ", s)
    s = re.sub(r"(=\s*[\d,.]+)\s*≠", r"\1, which is not equal to ", s)
    # Operators.
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    s = s.replace("=", " equals ").replace("≈", " is about ").replace("≠", " is not equal to ")
    s = s.replace("≤", " is less than or equal to ").replace("≥", " is greater than or equal to ")
    s = s.replace("<", " is less than ").replace(">", " is greater than ").replace("&", " and ")
    s = s.replace("{", "").replace("}", "").replace("✓", "").replace("✗", "")
    # Tidy.
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\b(plus|minus|times|divided by|equals) open bracket", r"\1, open bracket", s)
    s = re.sub(r"\b(over \w+) times\b", r"\1, times", s)
    if s.startswith("the square root"):
        s = "T" + s[1:]
    s = re.sub(r"([.!?] )the square root", r"\1The square root", s)
    s = re.sub(r"(\d) 's\b", r"\1s", s)
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",(?:\s*,)+", ",", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"([:;])\s*,", r"\1", s)
    s = s.replace(_OPEN + " ", _OPEN).replace(" " + _CLOSE, _CLOSE)
    s = re.sub(_OPEN + r",?\s*", "(", s)
    s = re.sub(r",?\s*" + _CLOSE, ")", s)
    s = re.sub(r"\s+", " ", s).strip().rstrip(",")
    s = re.sub(r"(, and so on)(?:,? and so on)+", r"\1", s)
    s = s.replace(" is is less than", " is less than").replace(" is is greater than", " is greater than")
    s = re.sub(r"\?\s*\.", "?", s)
    if s.endswith("and so on"):
        s += "."
    # A sentence that starts straight after a number, where print had only a tick or a line break.
    s = re.sub(r"(\d) (That|That's|The|Yes|This|It|It's|So|Now|Perfect|Find|Then|Check|Let's|Since|Nope)\b(?! \d)", r"\1. \2", s)
    if s.startswith("star"):
        s = "S" + s[1:]
    return s


def say_latex(latex):
    """A step's maths line as a spoken sentence, or None where it is a table or anything unusual."""
    s = (latex or "").strip()
    if not s:
        return None
    if re.search(r"\\begin|\\\\|&|\\left|\\right(?!arrow)|\\cdot|\\over", s) or s.count("<") > 1:
        return None
    s = s.replace("{,}", ",")
    s = re.sub(r"\\boxed\{\s*\?\s*\}", " ___ ", s)
    s = re.sub(r"(?<=[,;])(\s*(?:\\[;, ])?\s*)\?(?=\s*(?:,|$))", r"\1 ___ ", s)
    for _ in range(3):
        s = re.sub(r"\\(?:text|mathbf|boxed|mathrm|textbf)\{([^{}]*)\}", r" \1 ", s)
    s = re.sub(r"\\sqrt\{([^{}]*)\}", lambda m: "√" + (m.group(1) if re.fullmatch(r"[\w.,]+", m.group(1)) else "(" + m.group(1) + ")"), s)

    def frac(m):
        top, bottom = m.group(1).strip(), m.group(2).strip()
        simple = r"[\w.,₹ ]+"
        if not re.fullmatch(simple, bottom):
            return _FAIL
        if re.fullmatch(simple, top):
            return " %s %s %s " % (top, _OVER, bottom)
        return " %s %s %s " % (top, _ALLOVER, bottom)

    for _ in range(3):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    s = re.sub(r"\\(?:quad|qquad)", " , ", s)
    s = re.sub(r"\\[;,! ]", " ", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\approx", "≈").replace("\\neq", "≠")
    s = re.sub(r"\\(?:implies|Rightarrow)", " " + _SO + " ", s)
    s = re.sub(r"\\(?:rightarrow|to)\b", "→", s)
    s = s.replace("\\ldots", "...").replace("\\dots", "...").replace("\\checkmark", "")
    s = s.replace("\\{", "").replace("\\}", "").replace("\\leq", "≤").replace("\\geq", "≥")
    if "\\" in s:
        return None
    s = re.sub(r"\^\s*\{(\w+)\}", r"^\1", s)
    s = re.sub(r"_\{(\w+)\}", r"_\1", s)
    if "{" in s or "}" in s:
        return None
    s = s.replace("-", "−").strip()
    if s.startswith("="):
        s = "That is " + s[1:]
    out = say(s)
    out = re.sub(r"\s*%s\s*" % _OVER, " over ", out)
    out = re.sub(r"\b(over \w+) times\b", r"\1, times", out)
    out = re.sub(r",?\s*%s\s*" % _ALLOVER, ", all divided by ", out)
    out = re.sub(r",?\s*%s\s*,?\s*" % _SO, ", so ", out)
    out = re.sub(r",? (and|or),", r", \1", out)
    out = re.sub(r"\s+", " ", out).strip().strip(",").strip()
    if not out or _FAIL in out:
        return None
    return out[0].upper() + out[1:]
