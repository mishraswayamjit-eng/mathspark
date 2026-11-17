"""Notation rules for the imported factors questions (AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

These are one-off word problems and textbook items. `say(text)` builds on factors_rules.say and
adds what their wording needs; `latex_words(latex)` reads the maths line printed under a step.
Lines that still do not sound right are hand-written in factors_imported_hand*.py.

Kept apart from factors_rules.py so that nothing here can change an existing entry.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import factors_rules as R  # noqa: E402

# Capitals that are names of things, said as letters; every other word in capitals is only emphasis.
_LETTERS = {"HCF": "H C F", "LCM": "L C M", "GCF": "G C F", "GCD": "G C D", "LED": "L E D"}
_KEEP = {"HCF", "LCM", "IPM", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII"}

_GROUPED = re.compile(r"(?<![\d,])(?:\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})+,\d{3})(?!\d)(?!,\d)")
_COMMA = "ˌ"  # stands in for the comma inside a number such as 3,312

_UNITS = [
    (r"(\d)\s*m\b(?!\.)", r"\1 metres"), (r"(\d)\s*g\b", r"\1 grams"), (r"(\d)\s*[lL]\b(?! [A-Z]\b)", r"\1 litres"),
    (r"\bmins?\b\.?", "minutes"), (r"\bsecs?\b\.?", "seconds"), (r"\bhrs?\b\.?", "hours"),
    (r"\bft\b\.?", "feet"),
]


def _clock(m):
    h, mins, half = m.group(1), m.group(2), m.group(3).lower()
    if mins.startswith("0"):
        return "%s:%s %s m" % (h, mins, half)
    return "%s %s %s m" % (h, mins, half)


def _chain_equals(s):
    """'HCF = 2² × 3 = 12' -> 'HCF = 2² × 3, which is 12': a second equals sign in one statement."""
    out = []
    seen = False
    i = 0
    while i < len(s):
        c = s[i]
        rest = s[i:]
        if c == "=":
            if seen:
                while out and out[-1] == " ":
                    out.pop()
                out.append(", which is")
            else:
                out.append("=")
                seen = True
        else:
            if (c in ".?!;:" and (i + 1 == len(s) or s[i + 1] in " \n")) or c == "\n" or rest.startswith(", ") \
                    or re.match(r" (?:and|so|then|but|or|with|from) ", rest):
                seen = False
            out.append(c)
        i += 1
    return "".join(out)


def _products(s):
    """A long run of plain factors gets a breath between different primes."""
    def rep(m):
        return R.grouped_product(m.group(0)).replace("times", "×")
    # grouped_product puts ", " between groups; keep the commas, restore the sign for the later pass
    return re.sub(r"(?<![\d.])\d+(?:\s*×\s*\d+){3,}(?![\d²³⁴⁵⁶¹])", rep, s)


def _which_is(s):
    """'Each bag gets 12\u00f76 = 2 apples, 18\u00f76 = 3 oranges' -> '... 12\u00f76, which is 2 apples, ...'.

    Inside a sentence that is already running, a division and its result read better joined by
    'which is' than by 'equals'."""
    out = []
    for sentence in re.split(r"(?<=[.!?])\s+", s):
        m = re.search(r"\b(?:gets?|with|ha(?:ve|s|d)|contains?)\s+\d+\s*\u00f7\s*\d+\s*=", sentence)
        if m:
            head, tail = sentence[:m.start()], sentence[m.start():]
            tail = re.sub(r"(\d+\s*\u00f7\s*\d+)\s*=\s*", r"\1, which is ", tail)
            sentence = head + tail
        out.append(sentence)
    return " ".join(out)


def _pre(s):
    s = s.replace("\u20e3", ".")  # keycap digits number a list
    s = re.sub(r"\s*\n\s*\u2192\s*", "\n", s)  # an arrow that starts a line is a bullet
    s = re.sub(r"[ \t]*\n+[ \t]*", lambda m: " ", re.sub(r"([^.?!:;,\s])[ \t]*\n+", r"\1. ", s))
    s = re.sub(r"\s*\u2192\s*", ". ", s)  # any other arrow starts a new sentence
    s = re.sub(r"\*+([^*\n]+?)\*+", r"\1", s)  # emphasis marks
    s = re.sub(r"^(\d+) — ", r"\1: ", s)
    s = re.sub(r"\b([Dd]ivid(?:e|ing)) (\d+) ÷ (\d+)", r"\1 \2 by \3", s)
    s = re.sub(r"\b(GCF|GCD)\s*\(\s*(\d+(?:\s*,\s*\d+)+)\s*\)", lambda m: "the %s of %s" % (m.group(1), R.and_list(m.group(2))), s)
    s = re.sub(r"\(([A-Z][^()]*[.!?])\)", r"\1", s)  # a whole sentence in brackets
    s = re.sub(r"\s*=\s*(?:\.\.\.+|…)", ", and so on", s)
    s = re.sub(r",\s*(?:\.\.\.+|…)\s*,\s*(?=\d)", ", and so on, up to ", s)
    s = re.sub(r",\s*(?:\.\.\.+|…)\s*", ", and so on. ", s)
    s = re.sub(r"\s*(?:\.\.\.+|…)\s*(?=[a-z])", ", ", s)
    s = re.sub(r"\s*(?:\.\.\.+|…)\s+(?=[A-Z\d])", ". ", s)
    s = re.sub(r"\b([A-Z]{2,})/([A-Z]{2,})\b", r"\1 or \2", s)
    # a whole-number division written with a slash is a division, not a fraction
    s = re.sub(r"(?<![\d/.])(\d+)\s*/\s*(\d+)(?![\d/.])",
               lambda m: "%s ÷ %s" % m.groups() if int(m.group(2)) and int(m.group(1)) % int(m.group(2)) == 0
               and int(m.group(1)) > int(m.group(2)) else m.group(0), s)
    # a small sum in brackets inside a product: the grouping changes the meaning
    s = re.sub(r"\)\s*\(", ") , (", s)
    s = re.sub(r"\((\d+|[a-z])\s*([+×÷−-])\s*(\d+|[a-z])\)",
               lambda m: " open bracket %s %s %s close bracket " % (m.group(1), "−" if m.group(2) == "-" else m.group(2), m.group(3)), s)
    s = re.sub(r"\u20b9\s*(\d+(?:,\d+)*(?:\.\d+)?)(?!\d|,\d|\.\d|[- ](?:coin|note))", r"\1 rupees", s)
    s = re.sub(r"(\d+)\s*(cm|m)\s*\u00d7\s*(\d+)\s*(cm|m)\b", r"\1 \2 by \3 \4", s)
    s = re.sub(r"(\d+)\s*\u00d7\s*(\d+)\s*(cm|m)\b(?!\s*[\u00d7=])", r"\1 by \2 \3", s)
    s = s.replace("{", "").replace("}", "")  # a set of numbers is read as a list
    # the comma inside one number must survive the list tidying in factors_rules.say
    s = _GROUPED.sub(lambda m: m.group(0).replace(",", _COMMA), s)
    s = _which_is(s)
    s = re.sub(r"(\d{1,2}):(\d{2})\s*([AaPp])\.?\s*[Mm]\b\.?", _clock, s)
    # "HCF (Highest Common Factor)": the name in brackets is an aside, not a list of numbers
    s = re.sub(r"\b(HCF|LCM|GCF|GCD)\s*\(([A-Za-z ]+)\)",
               lambda m: "%s, the %s," % (" ".join(m.group(1)), m.group(2)), s)
    s = re.sub(r"(\d)\s*cm (ribbon|rope|strip|wire|pipe|rod|stick|tape|tile|plank|cloth|board|piece|ruler|side)\b",
               r"\1 centimetre \2", s)
    s = re.sub(r"(\d)\s*m (ribbon|rope|strip|wire|pipe|rod|stick|tape|tile|plank|cloth|board|piece|side)\b",
               r"\1 metre \2", s)
    for k, v in _LETTERS.items():
        s = re.sub(r"\b%s\b" % k, k if k in _KEEP else v, s)
    s = re.sub(r"\b[A-Z]{2,}\b", lambda m: m.group(0) if m.group(0) in _KEEP else m.group(0).lower(), s)
    s = re.sub(r"\bi\.e\.,?", "that is,", s)
    s = re.sub(r"\be\.g\.,?", "for example,", s)
    s = s.replace("&", " and ").replace("≤", " less than or equal to ").replace("≥", " greater than or equal to ")
    s = re.sub(r"(?:₹|Rs\.?)\s*([\d,]+)(?=[- ](?:coin|note))", r"\1 rupee", s)
    for pat, rep in _UNITS:
        s = re.sub(pat, rep, s)
    s = _chain_equals(s)
    s = _products(s)
    return s


def _post(s):
    s = s.replace(_COMMA, ",")
    s = re.sub(r"([!?]),", ",", s)
    s = re.sub(r"([!?])\.", r"\1", s)
    s = re.sub(r"close bracket (times|divided by|plus|minus) open bracket", r"close bracket, \1 open bracket", s)
    s = re.sub(r"\b(equals \d+), (\d+) equals\b", r"\1. \2 equals", s)
    s = re.sub(r"\b(squared|cubed|to the power of \w+) times\b", r"\1, times", s)
    s = re.sub(r"(?<![\d,.])1 rupees\b", "1 rupee", s)
    # A list of factorisations: each one is its own sentence.
    power = r"(times \d+|squared|cubed|to the power of \w+)"
    s = re.sub(power + r",? and (\d+) equals\b", r"\1. And \2 equals", s)
    s = re.sub(power + r", (\d+) equals\b", r"\1. \2 equals", s)
    s = re.sub(r"([.!?] )the (H C F|L C M|G C F) of\b", r"\1The \2 of", s)
    s = re.sub(r"^the (H C F|L C M|G C F) of\b", r"The \1 of", s)
    s = re.sub(r",\s*the the\b", ", the", s).replace(" the the ", " the ")
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r"\bequals product of\b", "equals the product of", s)
    # "... which is 4, Tennis per bag equals ...": each labelled result is its own sentence
    s = re.sub(r"(\d), ([A-Z][a-z]+(?: [a-z]+)? per [a-z]+\b)", r"\1. \2", s)
    s = re.sub(r"([.!?]) ([a-z])", lambda m: "%s %s" % (m.group(1), m.group(2).upper()), s)
    s = re.sub(r"([.!?] )The (G C F) of\b", r"\1The \2 of", s)
    return s.strip()


def say(text):
    if not (text or "").strip():
        return ""
    return _post(R.say(_pre(text)))


def option(text):
    t = text.strip()
    m = re.fullmatch(r"[-−](\d+)", t)
    if m:
        return "minus " + m.group(1)
    return say(t)


def latex_words(latex):
    """The maths line under a step, as a sentence; None if it has notation this does not know."""
    s = latex or ""
    if not s.strip():
        return None
    s = re.sub(r"\\text\{([^{}]*)\}", r" \1 ", s)
    s = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r" \1 ÷ \2 ", s)
    s = s.replace("\\times", " × ").replace("\\div", " ÷ ").replace("\\quad", " ").replace("\\,", " ")
    s = s.replace("\\ldots", " and so on ").replace("\\dots", " and so on ").replace("\\cdot", " × ")
    s = re.sub(r"\\(?:Rightarrow|rightarrow|implies)", ", so ", s)
    s = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\bR\s+(\d+)\b", r"remainder \1", s)

    def power(m):
        base, exp = m.group(1), m.group(2)
        if exp == "2":
            return base + " squared "
        if exp == "3":
            return base + " cubed "
        return "%s to the power of %s " % (base, exp)
    s = re.sub(r"(\d+|[a-z])\s*\^\s*\{?(\d+)\}?", power, s)
    if "\\" in s or "^" in s or "{" in s or "_" in s:
        return None
    s = re.sub(r"\s+", " ", s).strip()
    words = say(s)
    words = re.sub(r"(\d) and so on\b", r"\1, and so on", words)
    if not words:
        return None
    if words[-1].isalnum():
        words += "."
    return words[0].upper() + words[1:]
