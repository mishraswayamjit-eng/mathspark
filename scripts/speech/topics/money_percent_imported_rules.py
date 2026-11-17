"""Rules for the imported Grade 5 story problems (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

Used by money-percent.py for those ids only, so the narration of the older questions is untouched.
These questions are long stories with rupees, percents and lines of working inside hints.
Letters in a formula (P, R, T, N, x) are said as letters; SI, CP and SP are said in full.
"""
import re

NUM = r"\d+(?:,\d+)*(?:\.\d+)?"

# Capitals that are names, not emphasis.
SPELL = {"IPL": "I P L"}

_WORD_FRACTION = {"1/2": "one half", "1/4": "one quarter", "3/4": "three quarters", "1/3": "one third", "2/3": "two thirds"}
_SUBSCRIPT = {"₁": " one", "₂": " two"}
_PER = r"kg|year|month|day|piece|box|cup|plate|packet|dozen|hour|glass|kite"


def _early(s):
    """Typography and notation that is not arithmetic."""
    s = s.replace("⏰", "").replace("*", "").replace('"', "").replace("“", "").replace("”", "")
    s = s.replace("—", ", ").replace("…", ",").replace(" & ", " and ")
    s = re.sub(r"\s*≈\s*", ", which is about ", s)
    s = re.sub(r"=\s*\?", "= what?", s)
    # An arrow that starts a new labelled line ("→ Profit = ...") is a new sentence, not "so".
    s = re.sub(r"[.!?]?\s*→\s*(?=[A-Z][a-z]+(?: [A-Za-z]+)? =)", ". ", s)
    s = re.sub(r"([.!?])\s*→\s*", r"\1 ", s)
    s = re.sub(r"(?<![A-Za-z])'([^']+)'(?![A-Za-z])", r"\1", s)
    s = re.sub(r"\(i\.e\.,?\s*", "(in other words, ", s)
    s = re.sub(r"\bvs\.?(?=\s)", "versus", s)
    s = re.sub(r"\betc\.(?=\s*[,)])", "and so on", s)
    s = re.sub(r"\(\s*=\s*", "(which is ", s)
    s = re.sub(r"\(in ₹\)", "in rupees", s)
    for k, v in _SUBSCRIPT.items():
        s = s.replace(k, v)
    # An abbreviation in brackets after its own name: "cost price (CP)" is "cost price, C P,".
    s = re.sub(r"\((CP|SP|SI)\)", lambda m: ", %s %s," % (m.group(1)[0], m.group(1)[1]), s)
    s = re.sub(r"\(([PRTN])\)", r", \1,", s)
    s = re.sub(r"\bSI_([A-Z])\b", r"simple interest for \1", s)
    s = re.sub(r"\bSI\b", "simple interest", s)
    s = re.sub(r"\bSP\b", "selling price", s)
    s = re.sub(r"\bCP\b", "cost price", s)
    for k, v in SPELL.items():
        s = re.sub(r"\b%s\b" % k, v, s)
    s = re.sub(r"\b[A-Z]{2,}\b", lambda m: m.group(0).lower(), s)  # capitals for emphasis
    # Mixed numbers and fraction signs.
    for sign, words in (("⅓", "one third"), ("⅔", "two thirds"), ("½", "one half"), ("¼", "one quarter"), ("¾", "three quarters")):
        s = re.sub(r"(\d)\s*" + sign, r"\1 and " + words, s)
        s = s.replace(sign, words)
    s = re.sub(r"\b(1/2|1/4|3/4|1/3|2/3)(?= (?:of|and)\b)", lambda m: _WORD_FRACTION[m.group(1)], s)
    # A hyphen used as a minus sign.
    s = re.sub(r"(?<=[\d)])\s+-\s+(?=[\d₹(])", " − ", s)
    return s


def _equals(s):
    """'=' is 'equals' the first time in a line of working, then 'which is', 'that is'."""
    state = {"end": None, "n": 0}

    def rep(m):
        between = s[state["end"]:m.start()] if state["end"] is not None else None
        fresh = between is None or re.search(
            r"[→:;?!≈]|, |\. |\b(?:and|then|so|but|if|when|giving|means|is|are|be)\b", between) is not None
        state["end"] = m.end()
        if fresh:
            state["n"] = 0
            return " equals "
        state["n"] += 1
        return ", that is " if state["n"] % 2 == 0 else ", which is "

    s = re.sub(r"^\s*=\s*", "That equals ", s)
    return re.sub(r"\s*=\s*", rep, s)


def _slashes(s):
    s = re.sub(r"\s*/\s*(%s)\b" % _PER, r" per \1", s)
    s = re.sub(r"\)\s*/\s*", ") ÷ ", s)
    s = re.sub(r"\s*/\s*\(", " ÷ (", s)
    # "a × b / 100" is a division; "45/200" on its own is a fraction.
    s = re.sub(r"(×\s*[\dA-Za-z.,]+)\s*/\s*(?=\d)", r"\1 ÷ ", s)
    s = re.sub(r"(?<=[\dA-Za-z])\s*/\s*(?=\d)", " over ", s)
    s = re.sub(r"\b(ghee|strings)/(cardamom|decorations)\b", r"\1 and \2", s)  # one cost for two things
    s = re.sub(r"(?<=[A-Za-z])/(?=[A-Za-z])", " or ", s)
    return s


def _money_units(s):
    s = re.sub(r"₹\s*\(([^()]*)\)", r"\1 rupees", s)
    s = re.sub(r"₹\s*(%s)" % NUM, lambda m: "%s %s" % (m.group(1), "rupee" if m.group(1) == "1" else "rupees"), s)
    s = re.sub(r"₹\s*([a-z])\b", r"\1 rupees", s)
    s = re.sub(r"\bper kg\b", "per kilogram", s)
    s = re.sub(r"\b1 kg\b", "1 kilogram", s)
    s = re.sub(r"\bkg\b", "kilograms", s)
    s = re.sub(r"\s*%", " percent", s)
    s = re.sub(r"(\d)([A-Za-z])\b", r"\1 \2", s)  # 3N is "3 N"
    return s


def _brackets(s):
    """Brackets are spoken only where the grouping changes the answer; otherwise they are a pause."""
    pat = re.compile(r"\(([^()]*)\)")
    while True:
        m = pat.search(s)
        if not m:
            return s
        inner = m.group(1).strip()
        before = s[:m.start()].rstrip()
        prev = before[-1:] if before else ""
        glued = s[m.start() - 1:m.start()].isalnum() if m.start() else False
        low = re.search(r"[+−]", inner) is not None
        need = prev in ("÷",) or (prev in ("×", "−") and low) or (glued and re.search(r"[×÷+−]", inner) is not None)
        if need:
            lead = " times, " if glued else ", "
            s = s[:m.start()] + lead + "open bracket, " + inner + ", close bracket, " + s[m.end():]
        elif re.search(r"\b(?:calculate|multiply|it's|that's|is)$", before, re.I) and re.search(r"\d", inner) and re.search(r"[×÷+−]", inner):
            # "calculate (15 × 800) ÷ 100": working after a word needs no pause before it.
            s = s[:m.start()] + inner + ", " + s[m.end():]
        else:
            s = s[:m.start()] + ", " + inner + ", " + s[m.end():]


_OPS = {"×": "times", "÷": "divided by", "+": "plus", "−": "minus"}


def _ops(piece):
    ops = re.findall(r"[×÷+−]", piece)
    if not ops:
        return piece
    mixed = any(o in "×÷" for o in ops) and any(o in "+−" for o in ops)
    seen = []

    def rep(m):
        o = m.group(1)
        pause = ""
        if seen:
            if mixed and o in "+−":
                pause = ","
            elif not mixed and o == "÷" and "×" in seen:
                pause = ","
        seen.append(o)
        return "%s %s " % (pause, _OPS[o])

    return re.sub(r"\s*([×÷+−])\s*", rep, piece)


_SPAN = re.compile(r"( equals |, which is |, that is |\s*→\s*|[.?!:;](?:\s+|$))")


def _tidy(s, option):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",(\s*,)+", ",", s)
    s = re.sub(r"\b(plus|minus|times|divided by|equals),\s+(?!open bracket)", r"\1 ", s)
    s = re.sub(r"\b(which is|that is),\s+(?=\d)", r"\1 ", s)
    s = re.sub(r"([:;]),", r"\1", s)
    # A left side that already has a pause in it takes a pause before "equals".
    s = re.sub(r"(, (?:divided by|plus|minus) [\d,.]+(?: rupees| percent)?) equals ", r"\1, equals ", s)
    s = re.sub(r"!\s*,", ",", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"([!?])\s*\.", r"\1", s)
    s = re.sub(r"\.(\s*\.)+", ".", s)
    s = re.sub(r"^[,\s]+", "", s)
    s = re.sub(r"(^|[.?!]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    if option:
        s = s.rstrip(".").strip()
    elif s and s[-1] not in ".?!":
        s = s.rstrip(",:; ") + "."
    return s


def say(text, option=False):
    """The spoken form of one printed string."""
    s = (text or "").strip()
    if not s:
        return ""
    s = _early(s)
    s = _equals(s)
    s = _slashes(s)
    s = _money_units(s)
    s = _brackets(s)
    s = s.replace(">", " is greater than ").replace("<", " is less than ")
    pieces = _SPAN.split(s)
    out = []
    for i, p in enumerate(pieces):
        if i % 2:
            out.append(", so " if "→" in p else p)
        else:
            out.append(_ops(p))
    return _tidy("".join(out), option)
