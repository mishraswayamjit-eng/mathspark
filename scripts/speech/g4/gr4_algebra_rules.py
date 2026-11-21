"""Rules that turn printed Grade 4 algebra into words for the voice. Used by gr4_algebra.py.

    from gr4_algebra_rules import say, maths_line
    say("Simplify: 3(2b + 4c)")  ->  "Simplify: 3 times, open bracket, 2 b plus 4 c, close bracket."

The order of the passes matters: money and units first, then brackets (they need the raw
symbols around them), then letters, then operators and fractions, then tidying.
"""
import re

# Private markers, expanded to words at the very end so the passes in between still see
# "symbols only" inside a bracket.
OPEN, CLOSE, TIMES, PAUSE, ALLOVER = "\x01", "\x02", "\x03", "\x04", "\x05"
MARKS = OPEN + CLOSE + TIMES + PAUSE + ALLOVER

OPS = "+−×÷/="
ORDINAL = {"st", "nd", "rd", "th"}
SPELL = {"IPM": "I P M", "HCF": "H C F", "LCM": "L C M"}


def _lower_shouting(s):
    """WHOLE, FIRST, NOT are emphasis in print; a voice may spell them out letter by letter."""
    def fix(m):
        w = m.group(0)
        if w in SPELL:
            return SPELL[w]
        if w == "BODMAS":
            return "Bodmas"
        return w.lower()
    return re.sub(r"\b[A-Z]{3,}\b", fix, s)


def _money(s):
    s = re.sub(r"₹\s*\(([^()]*)\)", r"(\1) rupees", s)
    s = re.sub(r"₹\s*([0-9A-Za-z²/]+)", r"\1 rupees", s)
    s = re.sub(r"\bRs\.?\s*(\d+(?:,\d+)*(?:\.\d+)?)", r"\1 rupees", s)
    return s


def _units(s):
    s = re.sub(r"(\d) cm (?=square\b|pieces\b|edges\b|piece\b)", r"\1 centimetre ", s)
    s = re.sub(r"\bcm\b", "centimetres", s)
    s = re.sub(r"\bkm\b", "kilometres", s)
    s = re.sub(r"\b1 kg\b", "1 kilogram", s)
    s = re.sub(r"\bkg\b", "kilograms", s)
    s = re.sub(r"(\d) g\b(?!\s*[=+−×÷])", r"\1 grams", s)
    # m is a metre only straight after a bracket or a number, and not inside a sum.
    s = re.sub(r"\)\s+m\b(?!\s*[=+−×÷])", ") metres", s)
    s = re.sub(r"(\d) m\b(?=\s+(?:long|wide|and|with)\b|[.,]|$)", r"\1 metres", s)
    return s


def _prev_char(s, i):
    j = i - 1
    while j >= 0 and s[j] == " ":
        j -= 1
    return (s[j] if j >= 0 else ""), (j == i - 1)


def _next_char(s, i):
    j = i
    while j < len(s) and s[j] == " ":
        j += 1
    return (s[j] if j < len(s) else ""), (j == i)


_SIMPLE = re.compile(r"^[−-]?\s*(?:\d+(?:\.\d+)?[A-Za-z]{0,2}|[A-Za-z]{1,2})$")


def _brackets(s):
    """Decide, bracket by bracket, whether it is grouping (say it), a single value, or punctuation."""
    while True:
        m = re.search(r"\(([^()]*)\)", s)
        if not m:
            return s
        inner = m.group(1).strip()
        bare = re.sub("[%s]" % MARKS, " ", inner).strip()
        pc, adjacent = _prev_char(s, m.start())
        nc, nadjacent = _next_char(s, m.end())
        simple = bool(_SIMPLE.match(bare))
        has_op = bool(re.search(r"[+−×÷/]", bare))
        # "(d is more than 1)" is an aside; "(length + breadth)" is grouping.
        wordy = bool(re.search(r"[,:=→✓✗?!]", bare)) or (bool(re.search(r"[A-Za-z]{3,}", bare)) and not has_op)
        compound = (not wordy) and has_op and not simple
        unit_next = bool(re.match(r"\s*(?:centimetres?|metres|kilograms|grams|kilometres|rupees|years|pages)\b", s[m.end():]))
        implicit = adjacent and (pc.isalnum() or pc == CLOSE or pc == "²")
        near_op = (pc != "" and pc in OPS) or (nc != "" and nc in OPS)
        after_times = bool(re.search(r"\btimes\s*$", s[:m.start()]))
        if simple and nc == "²" and nadjacent and not implicit:
            rep = " " + inner                       # (13)² is just 13 squared
        elif simple and implicit:
            rep = TIMES + inner + " "
        elif simple and near_op:
            rep = " " + inner + " "
        elif compound and implicit:
            rep = TIMES + OPEN + inner + CLOSE
        elif compound and nc == "/" and (pc == "" or pc not in "+−×÷/"):
            rep = " " + inner + ALLOVER
            s = s[:m.start()] + rep + re.sub(r"^\s*/\s*", "", s[m.end():])
            continue
        elif compound and nadjacent and nc.isalpha():
            rep = OPEN + inner + CLOSE + TIMES
        elif compound and (after_times or nc == "²" or (pc != "" and pc in "×÷/−") or (nc != "" and nc in "×÷/")):
            rep = OPEN + inner + CLOSE
        elif wordy:
            rep = PAUSE + inner + PAUSE
        else:
            # Brackets that are only punctuation: "(2a + 3) cm", "Add (3x + 4y) and (x + 2y)".
            rep = " " + inner + (" " if unit_next else PAUSE)
        s = s[:m.start()] + rep + s[m.end():]


def _letters(s):
    """2x -> 2 x, 12xy -> 12 x y, 4ab -> 4 a b; and lone products of letters."""
    def split(m):
        if m.group(2).lower() in ORDINAL or m.group(2) == "s":      # 13th; "count on in 2s"
            return m.group(0)
        return m.group(1) + " " + " ".join(m.group(2))
    s = re.sub(r"(\d)([A-Za-z]{1,3})\b", split, s)
    s = re.sub(r"\b(ab|mn|xy)\b", lambda m: " ".join(m.group(1)), s)
    return s


# Words that can follow the letter a when it is a variable, and never follow the word "a".
_AFTER_A = r"(?:terms|times|multiplied|on its own|stands|means|and|is|centimetres|from|first|when|before|by|with|squared|cubed|b)\b"


def _variable_a(s):
    """The letter a, used as a variable, is written A so the voice says the letter, not the word."""
    marks = MARKS
    s = re.sub(r"(?<=\d )a\b(?! (?:term|whole|multiple|number)\b)", "A", s)   # 4 a, but not "is 35 a term"
    s = re.sub(r"\ba(?=\s*[=+−×÷/%s]|\s*[.,;:?!](?:\s|$)|\s*$)" % marks, "A", s)   # a = , a + , "of a."
    s = re.sub(r"([=+−×÷/%s]\s*)a\b" % marks, r"\1A", s)                # + a
    s = re.sub(r"\ba(?= %s)" % _AFTER_A, "A", s)                         # a terms, a times a
    s = re.sub(r"\ba's\b", "A's", s)
    s = re.sub(r"\b(letter|the|each) a\b(?! [a-z]{2,})", r"\1 A", s)     # "the letter a", "where the a is"
    return s


def _equals(s):
    """First equals in a clause is 'equals'; later ones in the same clause are ', which is'."""
    parts = re.split(r"(\.\s|,\s|:\s|;\s|!\s|\?\s|→|\band\b|\bbut\b|\bthen\b|\bso\b|\bNow\b)", s)
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(part)
            continue
        seen = 0
        buf = []
        for j, piece in enumerate(part.split("=")):
            if j:
                if seen == 0 and not "".join(buf).strip():
                    buf.append("That equals " if i == 0 else " equals ")
                elif seen == 0 and re.search(r"\b(?:is|be|gives|becomes)\s+[\dA-Za-z\s+−×÷().]{1,24}$", "".join(buf)) \
                        and re.search(r"\b(?:is|be|gives|becomes)\s+[^=]*[+−×÷]", "".join(buf)):
                    buf.append(", which is ")      # "6a is 6 × 4 = 24"
                elif seen == 0:
                    buf.append(" equals ")
                else:
                    buf.append(", which is ")
                seen += 1
            buf.append(piece)
        out.append("".join(buf))
    return "".join(out)


def _operators(s):
    s = re.sub(r"(?<![A-Za-z0-9])-(?=\s*[\dA-Za-z(])", "−", s)
    s = s.replace("≠", " is not equal to ")
    s = re.sub(r"=\s*\?", " equals what?", s)
    s = _equals(s)
    s = s.replace("→", ", so ")
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    return s


def _fractions(s):
    return re.sub(r"\s*/\s*", " over ", s)


def _tidy(s, sentence):
    s = s.replace(TIMES + OPEN, " times" + OPEN)
    s = s.replace(CLOSE + TIMES, CLOSE + " times ")
    s = s.replace(OPEN, ", open bracket, ").replace(CLOSE, ", close bracket, ")
    s = s.replace(TIMES, " times ").replace(PAUSE, ", ").replace(ALLOVER, ", all over ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    for _ in range(3):
        s = re.sub(r",\s*,", ",", s)
        s = re.sub(r",\s*([.?!:;])", r"\1", s)
        s = re.sub(r"([.:;!?])\s*,", r"\1", s)
        s = re.sub(r"\.\s*\.", ".", s)
        s = re.sub(r"([!?])\s*\.", r"\1", s)
        s = re.sub(r":\s*\.", ".", s)
    # A comma left behind by a bracket ("equals, 5"), never one the sentence itself has ("3 times, so ...").
    s = re.sub(r"\b(equals|is|times|plus|minus|by),\s+(?=\d|[A-Za-z]\b)", r"\1 ", s)
    s = re.sub(r"(?<!left )\bover,\s+(?=[\dA-Za-z]\b)", "over ", s)
    s = s.strip(" ,")
    s = re.sub(r"\s*:$", "", s)                     # "its perimeter will be:"
    # Breaths in long working: "5 times 6, plus 10" and "3 times 7, minus 3".
    s = re.sub(r"\b(\d+ times \d+) (plus|minus)\b", r"\1, \2", s)
    s = re.sub(r"\b(\d+ times \d+, (?:plus|minus) \d+) (plus|minus|equals)\b", r"\1, \2", s)
    s = re.sub(r"\b(\d+ times \d+) (and|separately)\b", r"\1, \2", s)
    s = re.sub(r"\b(\d+ times \d+, (?:plus|minus) \d+ times \d+(?:, (?:plus|minus) \d+ times \d+)?) equals\b", r"\1, equals", s)
    s = re.sub(r"\b(close bracket, (?:times|divided by) \w+) (equals|has)\b", r"\1, \2", s)
    s = re.sub(r"\b(all over \w+) (equals|and|is)\b", r"\1, \2", s)
    s = re.sub(r"\b(which is [\d.]*\d) (and|but)\b(?! \d+ over\b)", r"\1, \2", s)
    if sentence and s:
        if s[-1] not in ".?!":
            s += "."
        first = re.match(r"[a-z]{2,}", s)
        if first:
            s = s[0].upper() + s[1:]
        s = re.sub(r"([.?!]\s+)([a-z])(?=[a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    return s


def _dots(s):
    """A trailing '...' in a list of numbers is 'and so on'."""
    s = s.replace("…", "...")
    s = re.sub(r"(?<=[A-Za-z])\.\.\.\s*$", "", s)
    s = re.sub(r"\s*,?\s*\.\.\.\s*(?=[A-Z])", ", and so on. ", s)
    s = re.sub(r"\s*,?\s*\.\.\.\s*$", ", and so on.", s)
    s = re.sub(r"\s*,?\s*\.\.\.\s*,?\s*", ", and so on, ", s)
    return s


def say(text, sentence=True):
    """Printed text to spoken words. `sentence=False` for answer choices (no forced capital or full stop)."""
    s = text or ""
    if not s.strip():
        return ""
    s = s.replace("\n", " ")
    s = _dots(s)
    s = re.sub(r"\s+[—–]\s+", ", ", s)
    s = re.sub(r"\(Q(\d+)\)", r", question \1", s)
    s = re.sub(r"(?<![A-Za-z])'([^']+?)'(?![A-Za-z])", lambda m: "A" if m.group(1) == "a" else m.group(1), s)
    s = s.replace("✓", ". ").replace("✗", ". ")
    s = _lower_shouting(s)
    s = _money(s)
    s = _units(s)
    s = _brackets(s)
    s = s.replace("²", " squared").replace("³", " cubed")
    s = _letters(s)
    s = _variable_a(s)
    s = _operators(s)
    s = _fractions(s)
    return _tidy(s, sentence)


def maths_line(latex):
    """A step's maths line as plain print, ready for the rules: \\frac{77}{7} -> 77/7, \\boxed{11} -> 11."""
    s = latex

    def frac(m):
        top, bottom = m.group(1), m.group(2)
        if re.search(r"[+\-−]", top):
            top = "(%s)" % top
        return "%s/%s" % (top, bottom)
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    s = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\mathbf\{([^{}]*)\}", r"\1", s)
    # \quad sets equations side by side: each is said as its own short sentence.
    s = re.sub(r"\s*,?\s*\\q?quad\s*", ". ", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\,", " ")
    s = s.replace("\\checkmark", " ").replace("\\ldots", "...").replace("\\neq", "≠")
    s = re.sub(r"\^\{?2\}?", "²", s)
    return re.sub(r"(?<=[\w )])\s*-\s*(?=[\w (])", " − ", s)
