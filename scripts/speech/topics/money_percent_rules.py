"""Rules that turn printed money and percent text into speech. Used by money-percent.py."""
import re

NUM = r"\d+(?:,\d+)*(?:\.\d+)?"

# Whole strings that recur (formula hints). Written by hand once, used wherever they appear.
EXACT = {}

_B = "open bracket, %s, close bracket"

# Formulas printed with letters and brackets, said in words a child knows. Brackets are spoken
# only where the grouping changes the answer. Longest first: the first match wins.
FORMULAS = [
    ("(SI × 100) ÷ (P × T)", "simple interest times 100, divided by, " + _B % "principal times time"),
    ("SI × 100 ÷ (P × T)", "simple interest times 100, divided by, " + _B % "principal times time"),
    ("(SI × 100) ÷ (R × T)", "simple interest times 100, divided by, " + _B % "rate times time"),
    ("SI × 100 ÷ (R × T)", "simple interest times 100, divided by, " + _B % "rate times time"),
    ("SI × 100 ÷ (P × R)", "simple interest times 100, divided by, " + _B % "principal times rate"),
    ("(P × R × T) ÷ 100", "principal times rate times time, divided by 100"),
    ("P × R × T ÷ 100", "principal times rate times time, divided by 100"),
    ("SP × 100 ÷ (100 + Profit%)", "selling price times 100, divided by, " + _B % "100 plus profit percent"),
    ("SP × 100 ÷ (100 − Loss%)", "selling price times 100, divided by, " + _B % "100 minus loss percent"),
    ("CP × (100 + new profit%) ÷ 100", "cost price times, " + _B % "100 plus new profit percent" + ", divided by 100"),
    ("CP × (100 − Loss%) ÷ 100", "cost price times, " + _B % "100 minus loss percent" + ", divided by 100"),
    ("CP × (100 + %) ÷ 100", "cost price times, " + _B % "100 plus the percent" + ", divided by 100"),
    ("CP × (100 − %) ÷ 100", "cost price times, " + _B % "100 minus the percent" + ", divided by 100"),
    ("(SP − CP) ÷ CP × 100", _B % "selling price minus cost price" + ", divided by cost price, times 100"),
    ("(Discount ÷ Original price) × 100", "discount divided by original price, times 100"),
    ("(Loss ÷ Cost price) × 100", "loss divided by cost price, times 100"),
    ("(Marks scored ÷ Total marks) × 100", "marks scored divided by total marks, times 100"),
    ("(scored ÷ total) × 100", "scored divided by total, times 100"),
    ("(part ÷ whole) × 100", "part divided by whole, times 100"),
    ("(Part ÷ Whole) × 100", "part divided by whole, times 100"),
    ("x × (N ÷ 100)", "x times, N divided by 100"),
    ("(Target total) − (marks already scored)", "target total minus marks already scored"),
]


def _money(m):
    n = m.group(1)
    return "%s %s" % (n, "rupee" if n == "1" else "rupees")


def _abbreviations(s, si):
    s = re.sub(r"p\.\s?c\.\s?p\.\s?a\.?", "percent per year", s)
    s = re.sub(r"\bp\.\s?a\.(?=\s+[A-Z][a-z])", "per year.", s)
    s = re.sub(r"\bp\.\s?a\.?", "per year", s)
    s = re.sub(r"\bS\.\s?I\.(?=\s+[A-Z][a-z])", "simple interest.", s)
    s = re.sub(r"\bS\.\s?I\.?", "simple interest", s)
    s = re.sub(r"\bC\.\s?P\.?", "cost price", s)
    s = re.sub(r"\bS\.\s?P\.?", "selling price", s)
    s = re.sub(r"\bSI\b", "simple interest", s)
    s = re.sub(r"\bSP\b", "selling price", s)
    s = re.sub(r"\bCP\b", "cost price", s)
    s = re.sub(r"\bMBA\b", "M B A", s)
    if si:
        s = re.sub(r"\bof P\b", "of the principal", s)
        s = re.sub(r"\bP\b", "principal", s)
        s = re.sub(r"\bR\b", "rate", s)
        s = re.sub(r"\bT\b", "time", s)
    return s


def _money_percent(s):
    s = re.sub(r"(?:₹|\bRs\.?|\bRe\.?)\s*(%s)(?:\s*/-)?" % NUM, _money, s)
    s = re.sub(r"\s*%", " percent", s)
    s = s.replace("¼", "one quarter").replace("½", "one half").replace("¾", "three quarters")
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    s = s.replace("/", " or ")
    return s


_OPS = {"×": "times", "÷": "divided by", "+": "plus", "−": "minus"}


def _segment(seg):
    """One side of an equals sign: say its operations, with a breath between them."""
    ops = re.findall(r"[×÷+−]", seg)
    mixed = any(o in "×÷" for o in ops) and any(o in "+−" for o in ops)
    seen = [0]

    def rep(m):
        o = m.group(0).strip()
        seen[0] += 1
        pause = ","
        if seen[0] == 1:
            pause = ""
        elif mixed and o in "×÷":
            pause = ""
        elif not mixed and o in "+−":
            pause = ""
        return "%s %s " % (pause, _OPS[o])

    return re.sub(r"\s*[×÷+−]\s*", rep, seg), len(ops)


def _clause(sent):
    """Operators and equals signs in one clause: 'a = b × c = d' is 'a equals b times c, which is d'."""
    if not re.search(r"[×÷+−=]", sent):
        return sent
    parts = [p.strip() for p in sent.split("=")]
    out = ""
    for i, part in enumerate(parts):
        said, nops = _segment(part)
        if i == 0:
            out = said
            first_ops = nops
            hard = nops >= 2 and re.search(r"[×÷]", part) is not None
            continue
        if i == 1 and not out:
            out = "That equals " + said
        elif i == 1:
            verb = re.search(r"(?:^|[ ,])(?:is|are) [^a-z]*$", parts[0]) is not None
            if re.match(r"(?:For|Per year|At) ", parts[0]) and not first_ops:
                out += ", that is " + said  # "For 5 years = ..." is a label, not a quantity
            elif not re.search(r"[A-Za-z]", parts[0]):
                out += (", equals " if hard else " equals ") + said  # bare working: "a ÷ b × c = d"
            else:
                out += (", which is " if hard or (verb and first_ops) else " equals ") + said
        elif i == 2 and len(parts) >= 4:
            # A long chain of working: take a breath and start again.
            out += ". That is " + said
        else:
            out += ", which is " + said
    return out


def _sentence(sent):
    """An arrow joins two clauses: 'so'."""
    return ", so ".join(_clause(c.strip()) for c in sent.split("→"))


def _tidy(s, option):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"([:;]),", r"\1", s)
    s = re.sub(r",(\s*,)+", ",", s)
    s = re.sub(r"\.(\s*\.)+", ".", s)
    s = re.sub(r"^[,\s]+", "", s)
    s = re.sub(r"(^|[.?!]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    # The checker reads "32,500," (a grouped number with a comma straight after it) as two
    # numbers, so such a number is written without its grouping commas. It is said the same.
    s = re.sub(r"(?<![\d,])\d{1,3}(?:,\d{2,3})+(?=,(?!\d))", lambda m: m.group(0).replace(",", ""), s)
    if option:
        s = s.rstrip(".").strip()
        s = s[:1] + re.sub(r"\b(Profit|Loss)\b", lambda m: m.group(1).lower(), s[1:])
    elif s and s[-1] not in ".?!":
        s = s.rstrip(",:; ") + "."
    return s


def say(text, option=False, si=False):
    """The spoken form of one printed string."""
    s = (text or "").strip()
    if not s:
        return ""
    if s in EXACT:
        return EXACT[s]
    s = s.replace("✓", "").replace("✗", "").replace("—", ", ")
    for printed, spoken in FORMULAS:
        s = s.replace(printed, spoken)
    s = re.sub(r"\s*÷ \((%s) × (%s)\)" % (NUM, NUM), r", divided by, open bracket, \1 times \2, close bracket", s)
    s = _abbreviations(s, si)
    s = _money_percent(s)
    s = re.sub(r"(?<=[A-Za-z])\s*–\s*(?=[A-Za-z])", " to ", s)
    s = re.sub(r"(?<=\d)\s*[-–]\s*(?=\d)", " − ", s)
    s = re.sub(r"\s[-–]\s", " − ", s)
    s = re.sub(r"(?<![A-Za-z])'([^']+)'(?![A-Za-z])", r"\1", s)
    s = s.replace("(", ", ").replace(")", ", ")
    sentences = re.split(r"(?<=[.?!:])\s+", s)
    s = " ".join(_sentence(x) for x in sentences)
    # Capitals used for emphasis or for labels inside a formula are just words when spoken.
    s = re.sub(r"\b[A-Z]{2,}\b", lambda m: m.group(0).lower(), s)
    s = re.sub(r"\b(equals|is|times|by|plus|minus|of) ([A-Z][a-z]+)\b", lambda m: m.group(1) + " " + m.group(2).lower(), s)
    s = re.sub(r"\bpercent (Profit|Loss)\b", lambda m: "percent " + m.group(1).lower(), s)
    s = re.sub(r"\b(equals|times|by|plus|minus) open bracket", r"\1, open bracket", s)
    return _tidy(s, option)
