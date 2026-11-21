"""Rules that turn printed Grade 4 decimal and measurement work into speech.

Used by gr4_decimals.py (and extended by gr4_units_rules.py).

    say(text)          the general converter for this notation
    family(text)       whole-line patterns of the generated and filler families
    from_latex(latex)  a maths line written in LaTeX, as the print it stands for
"""
import re

_WORDS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters",
          ("1", "3"): "one third", ("2", "3"): "two thirds"}
_MIXED_WORDS = {("1", "2"): "a half", ("1", "4"): "a quarter", ("3", "4"): "three quarters",
                ("1", "3"): "a third", ("2", "3"): "two thirds"}

_NUM = r"\d+(?:,\d+)*(?:\.\d+)?"

# unit abbreviation: (singular, plural)
UNITS = {
    "km": ("kilometre", "kilometres"), "kg": ("kilogram", "kilograms"), "cm": ("centimetre", "centimetres"),
    "mm": ("millimetre", "millimetres"), "ml": ("millilitre", "millilitres"), "mL": ("millilitre", "millilitres"),
    "mg": ("milligram", "milligrams"), "dm": ("decimetre", "decimetres"), "kl": ("kilolitre", "kilolitres"),
    "kL": ("kilolitre", "kilolitres"), "cl": ("centilitre", "centilitres"), "cg": ("centigram", "centigrams"),
    "hm": ("hectometre", "hectometres"), "dam": ("decametre", "decametres"), "hg": ("hectogram", "hectograms"),
    "dag": ("decagram", "decagrams"), "dg": ("decigram", "decigrams"), "dl": ("decilitre", "decilitres"),
    "dal": ("decalitre", "decalitres"), "hl": ("hectolitre", "hectolitres"),
    "Kg": ("kilogram", "kilograms"),
    "m": ("metre", "metres"), "g": ("gram", "grams"), "gm": ("gram", "grams"), "gms": ("gram", "grams"),
    "l": ("litre", "litres"), "L": ("litre", "litres"),
    "hr": ("hour", "hours"), "hrs": ("hour", "hours"),
    "min": ("minute", "minutes"), "mins": ("minute", "minutes"),
    "sec": ("second", "seconds"), "secs": ("second", "seconds"),
}
_UNIT_ALT = "|".join(sorted(UNITS, key=len, reverse=True))

_WORD_SUBS = [
    (r"\bLCM\b", "L C M"), (r"\bHCF\b", "H C F"), (r"\bIPM\b", "I P M"),
    (r"\bLEFT\b", "left"), (r"\bRIGHT\b", "right"), (r"\bNOT\b", "not"),
    (r"\be\.g\.,?", "for example,"), (r"\bi\.e\.,?", "that is,"),
    (r"\bvs\.?\s", "and "),
    (r"\bR\s?(\d)", r"remainder \1"),
    (r"'([A-Za-z])'", r"\1"),
]


def _frac(n, d):
    return _WORDS.get((n, d)) or "%s over %s" % (n, d)


def _unit(m):
    num, u = m.group(1), m.group(2)
    one = num in ("1", "1.0")
    return "%s %s" % (num, UNITS[u][0 if one else 1])


def _money(m):
    num = m.group(1)
    return "%s %s" % (num, "rupee" if num == "1" else "rupees")


def _equals(sentence):
    """First '=' is 'equals', later ones in the same clause are ', which is'."""
    parts = sentence.split("=")
    if len(parts) == 1:
        return sentence
    tail = re.search(r"\s*$", sentence).group(0)
    out = parts[0]
    if not out.strip():
        out = "That equals " + parts[1].strip()
    elif re.search(r"\b(?:is|are|was|were|has|have|had|gives?|makes?|gets?|be|costs?|means|becomes|weighs?|gains?|takes?"
                   r"|rises?|needs?|loses?|away|holds?|pays?|spends?|walks?|runs?|got)\s+(?:about\s+)?[\d(]", out):
        out = out.rstrip() + ", which is " + parts[1].strip()
    else:
        out = out.rstrip() + " equals " + parts[1].strip()
    for p in parts[2:]:
        out = out.rstrip() + ", which is " + p.strip()
    return out + tail


_PAUSE = "\x01"


def _pause_chain(seg):
    """Mark the pauses in one run of working: 'a + b − c', 'a × b + c × d', 'a × b ÷ c'."""
    ops = re.findall(r"[+−×÷]", seg)
    if len(ops) < 2:
        return seg
    low = [o for o in ops if o in "+−"]
    high = [o for o in ops if o in "×÷"]
    count = [0]

    def mark(m):
        count[0] += 1
        op = m.group(0)
        if low and high:
            return _PAUSE + op if op in "+−" else op
        return (_PAUSE + op) if count[0] >= 2 else op

    return re.sub(r"[+−×÷]", mark, seg)


def _pauses(s):
    pieces = re.split(r"(=|[.?!;:,](?=\s|$)|[()⟋]|[A-Za-z]{2,})", s)
    out = []
    for i, p in enumerate(pieces):
        if i % 2:
            # an equals sign after a long run of working gets a pause too
            if p == "=" and i >= 1 and _PAUSE in out[-1]:
                out.append(_PAUSE)
            out.append(p)
        else:
            out.append(_pause_chain(p))
    return "".join(out)


def tidy(s):
    s = s.replace(_PAUSE, ", ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    for _ in range(2):
        s = re.sub(r",\s*,", ",", s)
        s = re.sub(r"([:;])\s*,", r"\1", s)
        s = re.sub(r",\s*([.?!:;])", r"\1", s)
        s = re.sub(r"\.\s*\.(?!\.)", ".", s)
        s = re.sub(r"([?!])\s*\.", r"\1", s)
        s = re.sub(r":\s*\.", ".", s)
    s = re.sub(r"([,?!:;])(?=[A-Za-z])", r"\1 ", s)
    s = re.sub(r"^[,;:.]\s*", "", s)
    s = re.sub(r"([.?!] )([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    if s:
        s = s[0].upper() + s[1:]
    return s


def _arrows(s):
    """'12.5 → 1.25 → 0.125' is 'becomes ..., then ...'; elsewhere an arrow is ', so'."""
    def chain(m):
        nums = re.split(r"\s*→\s*", m.group(0))
        out = nums[0] + " becomes " + nums[1]
        for n in nums[2:]:
            out += ", then " + n
        return out

    s = re.sub(r"(?<![\d.])%s(?:\s*→\s*%s)+(?![\d.]*\d)" % (_NUM, _NUM), chain, s)
    return re.sub(r"\s*→\s*", ", so ", s)


def _compare_chain(s):
    """'a < b < c' is 'a is less than b, which is less than c'."""
    for sym, word in (("<", "less than"), (">", "greater than")):
        def chain(m, word=word, sym=sym):
            items = [x.strip() for x in m.group(0).split(sym)]
            out = "%s is %s %s" % (items[0], word, items[1])
            for x in items[2:]:
                out += ", which is %s %s" % (word, x)
            return out
        item = r"(?:%s(?:\s*/\s*\d+)?)" % _NUM
        s = re.sub(r"%s(?:\s*%s\s*%s)+" % (item, sym, item), chain, s)
        s = s.replace(sym, " is %s " % word)
    return s


def pre(s):
    """Hook for topics that extend these rules: runs before anything else."""
    return s


def say(text, pre_hook=None):
    s = (text or "").strip()
    if not s:
        return ""
    s = s.replace("\n", " ")
    if pre_hook:
        s = pre_hook(s)
    for k, v in {"½": " 1/2 ", "¼": " 1/4 ", "¾": " 3/4 ", "⅓": " 1/3 ", "⅔": " 2/3 "}.items():
        s = s.replace(k, v)
    s = s.replace("²", " squared ").replace("³", " cubed ")
    s = s.replace(" & ", " and ").replace("&", " and ")
    s = s.replace("✓", " ").replace("✗", " ").replace("✔", " ").replace("…", ".").replace("–", "−")
    s = re.sub(r"\s+—\s+", ". ", s).replace("—", ", ")
    s = re.sub(r"(\d)\s*-\s*(?=\d)", r"\1 − ", s)
    s = re.sub(r"(?<=\d)\s+-\s+(?=[A-Za-z(])", " − ", s)
    s = re.sub(r"(\d),?\s*\.\.\.\s*(?=[a-z])", r"\1, and so on, ", s)
    s = re.sub(r"(\d),?\s*\.\.\.\s*", r"\1, and so on. ", s)
    s = re.sub(r"=\s*_{2,}", "= what", s)
    s = re.sub(r"_{2,}", " blank ", s)
    s = re.sub(r"=\s*\?", "= what?", s)
    # money
    s = re.sub(r"(?:₹|Rs\.?)\s*(%s)\s+(notes?|coins?)\b" % _NUM, r"\1 rupee \2", s)
    s = re.sub(r"\b([Aa]n?) (?:₹|Rs\.?)\s*(%s)\s+(?=[a-z])" % _NUM, r"\1 \2 rupee ", s)
    s = re.sub(r"(?:₹|Rs\.?)\s*(%s)" % _NUM, _money, s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(\d)\s*°\s*C\b", r"\1 degrees Celsius", s)
    s = re.sub(r"(\d)\s*°", r"\1 degrees", s)
    # a plain fraction of a unit: '1/8 l' is '1/8 of a litre' (not a mixed number such as '2 1/2 m')
    s = re.sub(r"(?<![\d.] )(?<![\d./])\b(\d+)\s*/\s*(\d+)\s*(%s)\b(?!\.\d)" % _UNIT_ALT,
               lambda m: "%s/%s of a%s %s" % (m.group(1), m.group(2), "n" if UNITS[m.group(3)][0] == "hour" else "", UNITS[m.group(3)][0]), s)
    # terse labels
    s = re.sub(r"(^|[.:!?] )Total\s*[=:]\s*", r"\1The total is ", s)
    s = re.sub(r"(^|[.:!?] )Answer\s*[=:]\s*", r"\1The answer is ", s)
    # 'the 3 m piece' is 'the 3 metre piece'
    s = re.sub(r"\b([Tt]he|one|each|every) (%s)\s*(%s) (?=(?:piece|rope|basket|climb|box|ribbon|rod|fence|jump|strip|bottle"
               r"|packet|bag|jug|plank|pipe|tub|tank|overlap|ruler|stick|wire|track|path|gap|step)s?\b)" % (_NUM, _UNIT_ALT),
               lambda m: "%s %s %s " % (m.group(1), m.group(2), UNITS[m.group(3)][0]), s)
    # 'a 2 m ribbon' is 'a 2 metre ribbon'
    s = re.sub(r"\b([Aa]n?) (%s)\s*(%s)\s+(?=[a-z])" % (_NUM, _UNIT_ALT),
               lambda m: "%s %s %s " % (m.group(1), m.group(2), UNITS[m.group(3)][0]), s)
    # units after a number, and 'per kg'
    s = re.sub(r"(%s)\s*(%s)\b(?!\.\d)" % (_NUM, _UNIT_ALT), _unit, s)
    s = re.sub(r"\bper (%s)\b" % _UNIT_ALT, lambda m: "per " + UNITS[m.group(1)][0], s)
    # a two-letter (or longer) abbreviation standing alone: 'in kg', 'cm'
    s = re.sub(r"\b((?:a|one|each|every) )(km|kg|Kg|cm|mm|ml|mL|mg|dm|hm|hg|dag|dg|dl|hl|kl|kL|gm)\b(?!\.\d)",
               lambda m: m.group(1) + UNITS[m.group(2)][0], s)          # 'half a kg' is 'half a kilogram'
    s = re.sub(r"\b(km|kg|Kg|cm|mm|ml|mL|mg|dm|hm|hg|dag|dg|dl|hl|kl|kL|gm|gms)\b(?!\.\d)", lambda m: UNITS[m.group(1)][1], s)
    # a one-letter unit named in a conversion: 'convert g to kg', 'divide m by 1000', 'from mg to g'
    s = re.sub(r"\b([Cc]onvert|[Dd]ivide|[Mm]ultiply|to|from|into|many) (m|g|l)\b(?!['.]\w)", lambda m: "%s %s" % (m.group(1), UNITS[m.group(2)][1]), s)
    for pat, rep in _WORD_SUBS:
        s = re.sub(pat, rep, s)
    # 'divide 126.4 ÷ 4' and 'multiply 0.25 × 0.4' (with no result after them) read as 'by'
    s = re.sub(r"\b([Dd]ivide) (%s) ÷ (%s)(?!\s*[=\d])" % (_NUM, _NUM), r"\1 \2 by \3", s)
    s = re.sub(r"\b([Mm]ultiply) (%s) × (%s)(?!\s*[=\d])" % (_NUM, _NUM), r"\1 \2 by \3", s)
    s = _arrows(s)
    s = _compare_chain(s)
    s = _pauses(s)
    # clause by clause, so that '=' chains read naturally
    pieces = re.split(r"([.?!:;,](?:\s+|$)|\s*[()]\s*|\s+(?:and|so|but|then|because|since|or)\s+)", s)
    s = "".join(p if i % 2 else _equals(p) for i, p in enumerate(pieces))
    # fractions over brackets, mixed numbers, then plain fractions
    s = re.sub(r"\(([^()]+)\)\s*/\s*\(([^()]+)\)", r"\1, all over \2", s)
    s = re.sub(r"\(([^()]+)\)\s*/\s*(\d+)", r"\1, all over \2", s)
    s = re.sub(r"(?<![\d.,/])\b(\d+) (\d+)\s*/\s*(\d+)(?![\d.]*\d)",
               lambda m: "%s and %s" % (m.group(1), _MIXED_WORDS.get((m.group(2), m.group(3))) or "%s over %s" % (m.group(2), m.group(3))), s)
    s = re.sub(r"(?<![\d.])(\d+)\s*/\s*(\d+)(?![\d.]*\d)", lambda m: _frac(m.group(1), m.group(2)), s)
    s = re.sub(r"\b([A-Za-z])\s*/\s*(\d+|[A-Za-z]\b)", r"\1 over \2", s)
    s = s.replace("⟋", ", over ")
    s = s.replace("□", " the box ").replace("★", " the star ")
    for k, v in (("×", " times "), ("÷", " divided by "), ("+", " plus "), ("−", " minus "), ("≈", " is about "),
                 ("≠", " is not equal to "), ("≤", " is at most "), ("≥", " is at least ")):
        s = s.replace(k, v)
    s = re.sub(r":$", ".", s)
    s = re.sub(r"[()\[\]{}]", ", ", s)
    s = s.replace("/", " or ").replace("*", "").replace("|", ", ")
    s = tidy(s)
    s = re.sub(r"(, over [^,.?!]+?) (equals|is)\b", r"\1, \2", s)
    return s


_MATHS = r"[\d.,\s+−×÷/()-]+"

_FAMILY = [
    (r"This is from the (\d{4}) IPM exam \(Q(\d+)\)\.",
     lambda m: "This is from the %s I P M exam, question %s." % m.groups()),
    (r"Correct answer: Option (\d) — (.+)",
     lambda m: "The correct answer is option %s, %s." % (m.group(1), _lower_first(say(m.group(2))).rstrip("."))),
    (r"(%s)\s*=\s*\?" % _MATHS,
     lambda m: "What is %s?" % _lower_first(say(m.group(1))).rstrip(".")),
    (r"Solve:\s*(%s?)\s*(?:=\s*\?)?" % _MATHS,
     lambda m: "Solve: %s." % _lower_first(say(m.group(1))).rstrip(".")),
    (r"First find the total cost: price × quantity\.",
     lambda m: "First find the total cost: the price times the quantity."),
    (r"Change = Amount paid − Total cost\.",
     lambda m: "The change is the amount paid, minus the total cost."),
    (r"Total cost = (\d+) × (\d+) = Rs\.(\d+)",
     lambda m: "The total cost is %s times %s, which is %s rupees." % m.groups()),
    (r"Change = Rs\.(\d+) − Rs\.(\d+) = Rs\.(\d+)",
     lambda m: "The change is %s rupees minus %s rupees, which is %s %s." % (m.group(1), m.group(2), m.group(3), "rupee" if m.group(3) == "1" else "rupees")),
]


def _lower_first(s):
    return s


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
    s = re.sub(r"\\text\s*\{([^{}]*)\}", r" \1 ", s)

    def frac(m):
        whole, n, d = m.group(1) or "", m.group(2).strip(), m.group(3).strip()
        if re.fullmatch(r"\d+", n) and re.fullmatch(r"\d+", d):
            return "%s %s/%s " % (whole, n, d)
        return "%s %s ⟋ %s " % (whole, n, d)

    s = re.sub(r"(\d+)?\s*\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", frac, s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\cdot", "×").replace("\\%", "%")
    s = re.sub(r"\\(?:Rightarrow|rightarrow|to|implies)\b", "→", s)
    s = re.sub(r",?\s*\\q?quad\s*", ". ", s)
    s = re.sub(r"\\(?:,|;|:|!)", " ", s).replace("\\ ", " ")
    s = s.replace("\\left", "").replace("\\right", "").replace("\\", "")
    s = re.sub(r"(?<=[\d\s)])-(?=[\s\d(])", "−", s)
    return re.sub(r"\s+", " ", s).strip()
