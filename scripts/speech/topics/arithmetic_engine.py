"""Rules that turn printed arithmetic into speech (topic: arithmetic).

    from arithmetic_engine import say, say_option

The rules know about BODMAS brackets (round, square, curly), negative numbers, chains of
equals signs, ticks and crosses, arrows, long expressions that need commas, and the small
set of units and abbreviations this topic uses. Lines the rules cannot read well are written
by hand in the arithmetic_fp / arithmetic_ws_* override tables.
"""
import re

# Bracket markers (control characters never appear in the source).
O_R, C_R, O_S, C_S, O_C, C_C = "\x01", "\x02", "\x03", "\x04", "\x05", "\x06"
EQ1, EQM, EQL, EQT, EQ1C = "\x0e", "\x0f", "\x10", "\x11", "\x12"
_OPEN = {"(": O_R, "[": O_S, "{": O_C}
_CLOSE = {"(": C_R, "[": C_S, "{": C_C}
_MARK_WORDS = {
    O_R: ", open bracket, ", C_R: ", close bracket, ",
    O_S: ", open square bracket, ", C_S: ", close square bracket, ",
    O_C: ", open curly bracket, ", C_C: ", close curly bracket, ",
}
_MARKS = "".join(_MARK_WORDS)

_KEEP_CAPS = {"BODMAS"}
_SPELL = {"HCF": "H C F", "LCM": "L C M", "GCD": "G C D", "OT": "overtime", "SI": "simple interest"}
_ORDINAL = re.compile(r"\d+(?:st|nd|rd|th)$")
_FRACTION_WORDS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters",
                   ("1", "3"): "one third", ("2", "3"): "two thirds"}

_NUM = r"\d+(?:,\d{2,3})*(?:\.\d+)?(?:/\d+)?"
_OPND = r"(?:%s|(?<![A-Za-z])[A-Za-z](?![A-Za-z]))" % _NUM
_RUN = re.compile(r"%s(?:\s*[+\-−×÷]\s*%s)+" % (_OPND, _OPND))
_OP_WORD = {"+": "plus", "-": "minus", "−": "minus", "×": "times", "÷": "divided by"}
_OP_NAME = {"+": "addition", "−": "subtraction", "×": "multiplication", "÷": "division"}


def _caps(s):
    def fix(m):
        w = m.group(0)
        if w in _SPELL:
            return _SPELL[w]
        if w in _KEEP_CAPS:
            return w
        return w.lower()
    return re.sub(r"\b[A-Z]{2,}\b", fix, s)


def _is_math(c):
    """True when a bracket's content is maths (numbers, single letters, operators), not words."""
    if not re.fullmatch(r"[\d\s.,+\-−×÷/=?a-zA-Z%s]*" % _MARKS, c):
        return False
    if re.search(r"[A-Za-z]{3,}", c) or re.search(r"\d(?:st|nd|rd|th)\b", c):
        return False
    return bool(re.search(r"[\d+\-−×÷]", c)) or bool(re.fullmatch(r"\s*[a-zA-Z]\s*", c))


def _brackets(s):
    """Innermost first: maths brackets become markers, word brackets become commas."""
    s = re.sub(r"(?:\b[Bb]racket\s+)?\(([^()\[\]{}]*)\):",
               lambda m: "brackets around %s:" % m.group(1) if _is_math(m.group(1)) and re.search(r"[+−×÷]", m.group(1)) else m.group(0), s)
    pat = re.compile(r"([\(\[\{])([^()\[\]{}]*)[\)\]\}]")
    while True:
        m = pat.search(s)
        if not m:
            return s
        kind, c = m.group(1), m.group(2).strip()
        before, after = s[:m.start()], s[m.end():]
        prev = before.rstrip()[-1:] if before.strip() else ""
        nxt = after.lstrip()[:1]
        lone = re.fullmatch(r"[−-]?\s*\d[\d,.]*", c)
        if not c:
            rep = {"(": " round brackets ", "[": " square brackets ", "{": " curly brackets "}[kind]
        elif lone:
            mathy = (prev and prev in "+-−×÷=" + _MARKS) or (before[-1:].isdigit()) or (nxt and nxt in "+−×÷=")
            if not mathy:
                rep = ", %s, " % c
            elif c[0] in "−-" and prev and prev in "+-−×÷":
                rep = _OPEN[kind] + c + _CLOSE[kind]
            else:
                rep = " " + c + " "
            if mathy and (before[-1:].isdigit() or before[-1:] in (C_R, C_S, C_C)):
                rep = " × " + rep
        elif _is_math(c) and re.search(r"(?<!\bof)(?<![A-Z])[a-z]{2}\s*$", before) and re.match(r"\s*(?:[.,;!?]|$|[a-z]{2})", after):
            # A sum mentioned in passing inside a sentence: "Check the last digit (9 × 3)."
            rep = ", %s, " % c
        elif _is_math(c):
            rep = _OPEN[kind] + c + _CLOSE[kind]
            if before[-1:].isdigit() or before[-1:] in (C_R, C_S, C_C):
                rep = " × " + rep
        else:
            rep = ", %s, " % c
        s = before + rep + after


def _equals(s):
    """Mark each equals sign by its place in a chain: A = B = C is 'A equals B, which is C'."""
    s = re.sub(r"=\s*\?", lambda m: (EQ1C if len(re.findall(r"[+−×÷]", s[:m.start()])) >= 3 else EQ1) + " what?", s)
    parts = re.split(r"((?<=[.;:!?,])\s+|\s+and\s+|\s+so\s+|\s+then\s+)", s)
    out = []
    for i, seg in enumerate(parts):
        n = seg.count("=")
        if i % 2 or not n:
            out.append(seg)
            continue
        k = [0]

        def rep(m, n=n, seg=seg):
            k[0] += 1
            if k[0] == 1:
                left = seg[:m.start()]
                if not left.strip():
                    return EQT
                # A long or bracketed left side needs a breath before "equals".
                long_left = any(c in left for c in _MARKS) or len(re.findall(r"[+−×÷]|\s-\s", left)) >= 3
                # A sum inside a sentence: "There are 18 × 30 = 540 girls" is "18 times 30, which is 540 girls".
                if n == 1 and not long_left and re.search(r"\b(?:is|are|was|were|costs?|uses?|earns?|with|ha(?:s|ve)|out|doubles?|to|needs?|by)\s+\d[\d.,/]*(?:\s*[+−×÷]\s*\d[\d.,/]*)+\s*$", left):
                    return EQL
                return EQ1C if long_left else EQ1
            return EQL if k[0] == n else EQM
        out.append(re.sub("=", rep, seg))
    return "".join(out)


def _run(m):
    """A flat expression such as 21 ÷ 84 × 16 − 7 × 3, with commas where a speaker would breathe."""
    toks = re.split(r"\s*([+\-−×÷])\s*", m.group(0))
    ops = toks[1::2]
    md = sum(1 for o in ops if o in "×÷")
    ads = len(ops) - md
    out = [toks[0]]
    for i, op in enumerate(ops):
        comma = False
        if md and ads and (md >= 2 or len(ops) >= 4):
            comma = op in "+-−"
        elif len(ops) >= 5 and (md == 0 or ads == 0):
            comma = (i + 1) % 3 == 0
        out.append("%s %s %s" % ("," if comma else "", _OP_WORD[op], toks[2 * i + 2]))
    return " ".join(out).replace(" ,", ",")


def _fraction(m):
    a, b = m.group(1), m.group(2)
    return _FRACTION_WORDS.get((a, b), "%s over %s" % (a, b))


def _list(m):
    """'0,2,4,6,8' is a list to read with pauses; '98,307' and '23,45,678' are single numbers."""
    parts = m.group(0).split(",")
    if len(parts[-1]) == 3 and all(len(p) in (2, 3) for p in parts[1:-1]):
        return m.group(0)
    return ", ".join(parts)


def _plural(m, one, many):
    return "%s %s" % (m.group(1), one if m.group(1) == "1" else many)


def _units(s):
    s = re.sub(r"Rs\.?\s*(\d+(?:,\d{2,3})*(?:\.\d+)?)", lambda m: _plural(m, "rupee", "rupees"), s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*hrs?\b", lambda m: _plural(m, "hour", "hours"), s)
    s = re.sub(r"\bhrs?\b", "hour", s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*min\b", lambda m: _plural(m, "minute", "minutes"), s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*cm\b", lambda m: _plural(m, "centimetre", "centimetres"), s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*mg\b", lambda m: _plural(m, "milligram", "milligrams"), s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s+m\b", lambda m: _plural(m, "metre", "metres"), s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s+g\b", lambda m: _plural(m, "gram", "grams"), s)
    return s


def _tidy(s):
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    for _ in range(3):
        s = re.sub(r",\s*,", ",", s)
        s = re.sub(r"([:;.!?])\s*,", r"\1", s)
        s = re.sub(r",\s*([.;:!?])", r"\1", s)
        s = re.sub(r"\.\s*\.", ".", s)
    s = s.strip(" ,")
    s = re.sub(r"(^|[.!?]\s+)([a-z])(?=[a-z'])", lambda m: m.group(1) + m.group(2).upper(), s)
    return s


def say(text, stop=True):
    """Print to speech. `stop` adds a full stop to a line that ends without one."""
    s = (text or "").replace("\n", " ")
    if not s.strip():
        return ""
    s = _caps(s)
    for k, v in {"½": " 1/2 ", "¼": " 1/4 ", "¾": " 3/4 ", "²": " squared", "–": "−", "’": "'"}.items():
        s = s.replace(k, v)
    s = re.sub(r"\d+(?:,\d+)+", _list, s)
    s = re.sub(r"(\d) remainder (\d)", r"\1, remainder \2", s)
    s = re.sub(r"\s*—\s*", ", ", s)
    s = re.sub(r"\s*✓\s*[.!]?", ". That works. ", s)
    s = re.sub(r"\s*✗\s*[.!]?", ". That does not work. ", s)
    s = re.sub(r"\s*(?:→|⇒)\s*", ", so ", s)
    # A sum or a list that trails off: "1 + 2 + … + 28", "1 + 2 + 3 + … up to 28", "1, 2, 4, …".
    s = re.sub(r"\+\s*(?:\.\.\.|…)\s*\+\s*(?=\d)", " plus, and so on, up to ", s)
    s = re.sub(r"\+\s*(?:\.\.\.|…)\s*", " plus, and so on, ", s)
    s = re.sub(r",\s*(?:\.\.\.|…)\s*,\s*(?=\d)", ", and so on up to ", s)
    s = re.sub(r",\s*(?:\.\.\.|…)", ", and so on", s)
    # A bare run of signs, "+ × −" or "+, × and −", is a list of signs, not of operations.
    s = re.sub(r"[+−×÷](?:\s*,?\s*[+−×÷])+(?:\s+and\s+(?:then\s+)?[+−×÷=])?(?!\s*[\w(\[{])",
               lambda m: re.sub(r"[+−×÷=]", lambda c: _SIGN[c.group(0)], re.sub(r"(?<=[+−×÷])\s+(?=[+−×÷])", ", ", m.group(0))), s)
    s = re.sub(r"(?<=\d)\s*(?:\.\.\.|…)", " and so on", s)
    s = re.sub(r"\s*(?:\.\.\.|…)\s*", ". ", s)
    s = re.sub(r"\b(\d+)([a-zA-Z]{1,2})\b", lambda m: m.group(0) if _ORDINAL.match(m.group(0)) or m.group(2) in ("cm", "mg", "hr", "m", "g", "s") else m.group(1) + " " + " ".join(m.group(2)), s)
    s = _units(s)
    s = re.sub(r"(brackets?)\s*\(\s*\)", r"\1", s)
    s = re.sub(r"\b(round|curly|square)\s*[\(\[\{]\s*[\)\]\}]", r"\1", s)
    s = _brackets(s)
    s = _equals(s)
    # A minus sign that belongs to a number, not between two numbers.
    s = re.sub(r"(?:^|(?<=[^\w%s]))[−-](?=\d)" % (C_R + C_S + C_C), "minus ", s)
    s = _RUN.sub(_run, s)
    # Operators left over sit next to a bracket, or stand alone as the name of an operation.
    s = re.sub(r"([+−×÷])(?=\s*(?:and|or|first|before|next|last|after|signs?)\b|\s*[,.;:!?)]|\s*$|\s*[+−×÷])",
               lambda m: " %s " % _OP_NAME[m.group(1)], s)
    s = re.sub(r"[+−×÷]", lambda m: " %s " % _OP_WORD[m.group(0)], s)
    s = re.sub(r"(?<=\s)-(?=\s)", "minus", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", _fraction, s)
    s = re.sub(r"(?<=[A-Za-z]{2})/(?=[A-Za-z]{2})", " and ", s)
    s = s.replace("/", " over ")
    for k, v in _MARK_WORDS.items():
        s = s.replace(k, v)
    s = s.replace(EQT, " that equals ").replace(EQ1C, ", equals ").replace(EQ1, " equals ").replace(EQM, ", that is ").replace(EQL, ", which is ")
    s = s.replace("=", " equals ").replace("≠", " is not equal to ").replace("≈", " is about ")
    s = s.replace("<", " is less than ").replace(">", " is greater than ")
    s = re.sub(r"_+|□", " blank ", s)
    s = re.sub(r"[♣✻*]", " blank ", s)
    s = _tidy(s).rstrip(":")
    if stop and s and s[-1] not in ".!?":
        s += "."
    return s


_SIGN = {"+": "plus", "−": "minus", "-": "minus", "×": "times", "÷": "divided by", "=": "equals"}


def say_option(text):
    """An answer choice: a bare value, a set of signs, or a bracket to insert."""
    t = (text or "").strip()
    if re.fullmatch(r"[+\-−×÷=,\s]+", t):
        return ", ".join(_SIGN[c] for c in t if c in _SIGN)
    m = re.fullmatch(r"\(([^()]*)\)", t)
    if m and re.search(r"[+−×÷]", t):
        return "Brackets around " + say(m.group(1), stop=False)
    s = say(t, stop=False)
    return s[:-1] if s.endswith(".") and not t.endswith(".") else s
