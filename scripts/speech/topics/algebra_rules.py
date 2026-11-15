"""Rules that turn printed algebra into words for the voice. Used by algebra.py.

    from algebra_rules import say
    say("Solve: 4x + 17 = 25")   ->  "Solve: 4 x plus 17 equals 25."

The order of the passes matters: brackets first (they need the raw symbols around them),
then coefficients and letters, then fractions and operators, then tidying.
"""
import re

# Private markers, expanded to words at the very end so that the passes in between
# still see "symbols only" inside a bracket.
OPEN, CLOSE, TIMES, PAUSE, ALLOVER = "\x01", "\x02", "\x03", "\x04", "\x05"

OPS = "+−×÷/="
KEEP_CAPS = {"HCF", "LCM"}
ORDINAL = {"st", "nd", "rd", "th"}


def _lower_shouting(s):
    """BOTH, EACH, SUM are emphasis in print; a voice may spell them out."""
    def fix(m):
        w = m.group(0)
        if w in KEEP_CAPS:
            return " ".join(w)
        if w == "BODMAS":
            return "Bodmas"
        return w.lower()
    return re.sub(r"\b[A-Z]{3,}\b", fix, s)


def _money(s):
    s = re.sub(r"(?:₹|Rs\.?)\s*(\d[\d,]*(?:\.\d+)?)", r"\1 rupees", s)
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
    return s[j] if j < len(s) else ""


_SIMPLE = re.compile(r"^[−-]?\s*(?:\d+(?:\.\d+)?[A-Za-z]{0,2}|[A-Za-z]{1,2})$")


def _brackets(s):
    """Decide, bracket by bracket, whether it is grouping (say it), a single value, or punctuation."""
    marks = OPEN + CLOSE + TIMES + PAUSE + ALLOVER
    while True:
        m = re.search(r"\(([^()]*)\)", s)
        if not m:
            return s
        inner = m.group(1).strip()
        bare = re.sub("[%s]" % marks, " ", inner)
        pc, adjacent = _prev_char(s, m.start())
        nc = _next_char(s, m.end())
        simple = bool(_SIMPLE.match(bare.strip()))
        wordy = bool(re.search(r"[A-Za-z]{3,}|[,:=→✓✗?]", bare))
        compound = (not wordy) and bool(re.search(r"[+−×÷]", bare)) and not simple
        implicit = adjacent and (pc.isalnum() or pc == CLOSE or pc == "²")
        near_op = (pc != "" and pc in OPS) or (nc != "" and nc in OPS)
        if simple and implicit:
            rep = TIMES + inner + " "
        elif simple and near_op:
            rep = " " + inner + " "
        elif compound and implicit:
            rep = TIMES + OPEN + inner + CLOSE
        elif compound and nc == "/" and not implicit and (pc == "" or pc not in "+−×÷/"):
            rep = " " + inner + ALLOVER
            s = s[:m.start()] + rep + re.sub(r"^\s*/\s*", "", s[m.end():])
            continue
        elif compound and (pc in "×÷/−" and pc != "" or nc in "×÷/" and nc != ""):
            rep = OPEN + inner + CLOSE
        elif compound:
            rep = PAUSE + inner + PAUSE
        else:
            rep = PAUSE + inner + PAUSE
        s = s[:m.start()] + rep + s[m.end():]


def _letters(s):
    """2x -> 2 x, 12xy -> 12 x y, 91abc -> 91 a b c; and lone products of letters."""
    def split(m):
        if m.group(2).lower() in ORDINAL:
            return m.group(0)
        return m.group(1) + " " + " ".join(m.group(2))
    s = re.sub(r"(\d)([A-Za-z]{1,3})\b", split, s)
    s = re.sub(r"\b(abc|ab|xy|mp)\b", lambda m: " ".join(m.group(1)), s)
    return s


def _variable_a(s):
    """The letter a, used as a variable, is written A so the voice says the letter, not the word."""
    s = re.sub(r"(?<=\d )a\b", "A", s)                       # 4 a
    s = re.sub(r"\ba(?= [a-z]\b)", "A", s)                    # a b c
    s = re.sub(r"(?<=\b[a-z] )a\b", "A", s)                   # b a
    s = re.sub(r"\ba(?=\s*[=+−×÷/²→%s%s%s])" % (CLOSE, PAUSE, ALLOVER), "A", s)
    s = re.sub(r"([=+−×÷/→%s%s%s]\s*)a\b" % (OPEN, PAUSE, TIMES), r"\1A", s)
    s = re.sub(r"\ba's\b", "A's", s)
    s = re.sub(r"\ba(?= squared\b| cubed\b)", "A", s)
    s = re.sub(r"\bFind a when\b", "Find A when", s)
    s = re.sub(r"\b(from|for) a\b(?! [a-z]{2,})", r"\1 A", s)
    return s


def _fractions(s):
    s = re.sub(r"(?<![\d.])1\s*/\s*2(?!\.?\d)", "one half", s)
    s = re.sub(r"\s*/\s*", " over ", s)
    return s


def _equals(s):
    """First equals in a clause is 'equals'; later ones in the same clause are ', which is'."""
    parts = re.split(r"(\.\s|,\s|:\s|;\s|!\s|\?\s|→|\band\b|\bbut\b|\bthen\b|\bso\b|\bversus\b|\bNow\b)", s)
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
    s = s.replace("≠", " is not equal to ").replace("≈", " is about ")
    s = re.sub(r"=\s*\?", " equals what?", s)
    s = re.sub(r"\bvs\b\.?", "versus", s)
    s = _equals(s)
    s = s.replace("→", ", so ")
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    return s


def _tidy(s, sentence):
    s = s.replace(TIMES + OPEN, " times" + OPEN)
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
    s = re.sub(r"\b(equals|is|times|plus|minus|by|over),\s+(?!open bracket)", r"\1 ", s)
    s = s.strip(" ,")
    # Breaths in long working: "5 times 5, plus 1 times 1" and "6 x plus 9, plus 8 x minus 5".
    s = re.sub(r"\b(\d+ times \d+) (plus|minus)\b", r"\1, \2", s)
    s = re.sub(r"\b(\d+ [A-Za-z] (?:plus|minus) \d+) (plus|minus) (\d+ [A-Za-z])\b", r"\1, \2 \3", s)
    s = re.sub(r"\b(all over \S+) (equals|and)\b", r"\1, \2", s)
    s = re.sub(r"\b((?:which is|equals) [\d.]*\d) (and|but)\b", r"\1, \2", s)
    if sentence and s:
        if s[-1] not in ".?!":
            s += "."
        first = re.match(r"[a-z]{2,}", s)
        if first:
            s = s[0].upper() + s[1:]
        s = re.sub(r"([.?!]\s+)([a-z])(?=[a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    return s


def say(text, sentence=True):
    """Printed text to spoken words. `sentence=False` for answer choices (no capital, no full stop)."""
    s = text or ""
    if not s.strip():
        return ""
    s = re.sub(r"(?<=\d)\.\.\.", ". ", s).replace("…", " ").replace("...", " ")
    s = re.sub(r"\s+[—–]\s+", ", ", s)
    s = re.sub(r"\b([A-D])–([A-D])\b", r"\1 to \2", s)
    s = re.sub(r"(?<![A-Za-z])'([^']+?)'(?![A-Za-z])", lambda m: "A" if m.group(1) == "a" else m.group(1), s)
    s = s.replace("✓", ". That works. ").replace("✗", ". That does not work. ")
    s = re.sub(r"\s*&\s*", ", and ", s)
    s = _lower_shouting(s)
    s = _money(s)
    s = _brackets(s)
    s = _letters(s)
    s = s.replace("²", " squared").replace("³", " cubed")
    s = _variable_a(s)
    s = _operators(s)
    s = _fractions(s)
    return _tidy(s, sentence)
