"""Rules for the imported Grade 5 questions of the topic ratio-word-problems
(ids AIGEN_grade5_..., IPMTB_grade5_..., IPM2020_G5_...).

These are one-off story problems: ratio sharing, and stories that end in a BODMAS expression.
`say_imported` turns one printed string into speech. It is only ever used for the imported
questions, so the narration of the older questions cannot change.

Notation rules:
  - "3 : 5" is "3 is to 5"; "Riya : Sameer = 3 : 5" is "Riya is to Sameer, as 3 is to 5".
  - A line of working is read operation by operation. A bracket that groups part of a longer
    expression is said aloud ("open bracket ... close bracket"); a bracket that only wraps a
    whole sum, or a remark in words, becomes a pause.
  - In an expression with three or more operations there is a breath before each plus and minus
    outside brackets, which is also where BODMAS splits the expression.
  - "a = b = c" is "a equals b, which equals c". A line that starts with "=" is "That equals ...".
  - "Step 1: Brackets -> ..." is "Step 1, Brackets: ...". Other arrows are "so".
  - Words printed in capitals for emphasis are said as ordinary words (a voice may spell them).
"""
import re

NUM = r"\d+(?:,\d{2,3})*(?:\.\d+)?"
OPERAND = NUM + r"k?"
RUN = re.compile(
    r"(?:\(\s*)*%(o)s(?:\s*\))*(?:\s*[×÷+−]\s*(?:\(\s*)*%(o)s(?:\s*\))*)+" % {"o": OPERAND})
TOKEN = re.compile(r"%s|[×÷+−()]" % OPERAND)
OP_WORDS = {"×": "times", "÷": "divided by", "+": "plus", "−": "minus"}
KEEP_CAPS = {"BODMAS"}
SPELL_CAPS = {"HCF": "H C F", "LCM": "L C M"}


def _operand(t):
    return t[:-1] + " k" if t.endswith("k") else t


def _run(match):
    """One run of working, such as '120 ÷ (4 + 2) × 3 − 8', as words."""
    run = match.group(0)
    lead = trail = ""
    # A bracket that opens before the run or closes after it belongs to the sentence, not the sum.
    while run.count("(") > run.count(")") and run.lstrip().startswith("("):
        run = run.lstrip()[1:]
        lead += "("
    while run.count(")") > run.count("(") and run.rstrip().endswith(")"):
        run = run.rstrip()[:-1]
        trail += ")"
    tokens = TOKEN.findall(run)

    def wrapped(ts):
        if not ts or ts[0] != "(" or ts[-1] != ")":
            return False
        depth = 0
        for i, t in enumerate(ts):
            depth += t == "("
            depth -= t == ")"
            if depth == 0 and i < len(ts) - 1:
                return False
        return True

    while wrapped(tokens):
        tokens = tokens[1:-1]
    n_ops = sum(1 for t in tokens if t in OP_WORDS)
    out, depth, seen = [], 0, 0
    for t in tokens:
        if t == "(":
            out.append(", open bracket,")
            depth += 1
        elif t == ")":
            out.append(", close bracket,")
            depth -= 1
        elif t in OP_WORDS:
            breath = depth == 0 and t in "+−" and n_ops >= 3 and seen > 0
            out.append((", " if breath else "") + OP_WORDS[t])
            seen += 1
        else:
            out.append(_operand(t))
    s = " ".join(out)
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r",(\s*,)+", ",", s)
    return lead + " " + s.strip(" ,") + (", " if tokens and tokens[-1] == ")" else " ") + trail


_VERB = re.compile(r"\b(?:gets?|keeps?|has|have|is|are|eats|buys?|receives?|worth|represents)\b")


def _equals(s):
    """'=' as words.

    'a = b = c' with only working in between is 'a equals b, which equals c'.
    After a verb in the same clause ('she gets 3 × 30 = 90 samosas') it is ', which is'.
    '=?' is 'equals what?'.
    """
    out, had, clause = [], False, 0
    i = 0
    while i < len(s):
        c = s[i]
        if c == "=":
            if s[i + 1:i + 2] == "?":
                out.append(" equals what?")
                i += 2
                had = False
                continue
            if had:
                out.append(", which equals ")
            elif _VERB.search(s[clause:i]):
                out.append(", which is ")
            else:
                out.append(" equals ")
            had = True
        else:
            if c in ".!?;:," and (i + 1 == len(s) or s[i + 1].isspace()):
                had = False
                clause = i + 1
            elif c.isalpha():
                had = False
            out.append(c)
        i += 1
    return "".join(out)


def latex_text(latex):
    """A step's maths line, as the kind of text say_imported reads."""
    s = latex.replace("{,}", ",")
    s = re.sub(r"\\(?:mathbf|overline|boxed)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\text\{([^{}]*)\}", r" \1 ", s)

    def frac(m):
        a, b = m.group(1).strip(), m.group(2).strip()
        if a.isdigit() and b.isdigit() and int(a) < int(b):
            return "%s/%s" % (a, b)
        return ("%s ÷ %s" if re.fullmatch(NUM, a) else "%s, ÷ %s") % (a, b)

    s = re.sub(r"\\[td]?frac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    s = re.sub(r",\s*\\quad\s*", ", then ", s)
    s = re.sub(r"\\quad\s*and\s*\\quad", " and ", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\neq", "≠").replace("\\checkmark", "")
    s = s.replace("\\{", "").replace("\\}", "")
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("-", "−")
    return re.sub(r"\s+", " ", s).strip()


def with_maths(spoken_text, latex):
    """A step that ends in a colon is finished by its maths line: say both."""
    maths = say_imported(latex_text(latex))
    if not maths:
        return spoken_text
    head = spoken_text.rstrip()
    if head.endswith("."):
        if maths.startswith("Open bracket"):
            maths = "o" + maths[1:]
        if head[-2:-1].isdigit():
            # "Subtract 8: 40 minus 8" would put "8: 40" in the voice's mouth, which reads like a time.
            return head + " So, " + maths
        return head[:-1] + ": " + maths
    return head + " " + maths[0].upper() + maths[1:]


def _lines(s):
    """Line breaks become sentence breaks; a line of working that starts with '=' is 'That equals'."""
    parts = []
    for line in s.replace("\r", "").split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("="):
            line = "That equals " + line[1:].strip()
        elif line.startswith("→"):
            line = line[1:].strip()
        elif line.startswith("•"):
            line = line[1:].strip()
        parts.append(line)
    out = ""
    for line in parts:
        if not out:
            out = line
        elif out[-1] in ".!?:,;":
            out += " " + line
        else:
            out += ". " + line
    return out


def _caps(match):
    w = match.group(0)
    if w in KEEP_CAPS:
        return w
    if w in SPELL_CAPS:
        return SPELL_CAPS[w]
    return w.lower()


def say_imported(text):
    s = (text or "").strip()
    if not s:
        return ""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"Step (\d+): ([^→\n:]+?)\s*→\s*", r"Step \1, \2§ ", s)
    s = _lines(s)
    s = re.sub(r"Step (\d+):", r"Step \1§", s)
    s = re.sub(r"\s*→\s*", ", so ", s)
    s = re.sub(r"\s*[—–]\s*", ", ", s)
    s = s.replace("i.e.,", "that is,").replace("i.e.", "that is,")
    s = re.sub(r"\bmL\b", "millilitres", s)
    # ratios between names, then equals signs
    s = re.sub(r"\b([A-Za-z]+) : ([A-Za-z]+) : ([A-Za-z]+)\s*=\s*", r"\1 is to \2 is to \3, as ", s)
    s = re.sub(r"\b([A-Za-z]+) : ([A-Za-z]+)\s*=\s*", r"\1 is to \2, as ", s)
    s = re.sub(r"\b([A-Z]):([A-Z]):([A-Z])\s*=\s*", r"\1 is to \2 is to \3, as ", s)
    s = re.sub(r"\b([A-Z]):([A-Z])\s*=\s*", r"\1 is to \2, as ", s)
    s = _equals(s)
    # fractions
    s = re.sub(r"\(\s*(\d+)\s*/\s*(\d+)\s*\)", r"\1/\2", s)
    s = re.sub(r"(\d+)/(\d+)", r"\1 over \2", s)
    # money, then ratios between numbers
    s = re.sub(r"\(in ₹\)", "in rupees", s)
    s = re.sub(r"₹\s*(%s)" % NUM, r"\1 rupees", s)
    s = re.sub(r"(\d) rupees (note|tip|boxes|budget)\b", r"\1 rupee \2", s)
    s = re.sub(r"rupees\s*:\s*(?=\d)", "rupees is to ", s)
    s = re.sub(r"(\d)\s*:\s*(?=\d)", r"\1 is to ", s)
    s = re.sub(r"(as %s is to %s(?: is to %s)?) and " % (NUM, NUM, NUM), r"\1, and ", s)
    # working
    s = RUN.sub(_run, s)
    for sym, word in OP_WORDS.items():
        s = s.replace(sym, " %s " % word)
    s = s.replace("≈", ", which is about ").replace("≠", " is not equal to ").replace(">", " is greater than ")
    s = re.sub(r"(\d)k\b", r"\1 k", s)
    # words
    s = re.sub(r"\b([A-Za-z]{3,})/([A-Za-z]{3,})\b", r"\1 and \2", s)
    s = s.replace("&", "and")
    s = re.sub(r"\b[A-Z]{2,}\b", _caps, s)
    s = re.sub(r"(?<![A-Za-z])'|'(?![A-Za-z])", "", s)
    s = re.sub(r"(?<=[A-Za-z])-(?=[A-Za-z])", " ", s)
    s = s.replace("(", ", ").replace(")", ", ")
    s = s.replace("§", ":")
    # tidy
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    for _ in range(3):
        s = re.sub(r",\s*([.?!:;,])", r"\1", s)
        s = re.sub(r"([.?!:;])\s*,", r"\1", s)
        s = re.sub(r"\?\s*\.", "?", s)
        s = re.sub(r"!\s*\.", "!", s)
        s = re.sub(r":\s*([.?!])", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip(" ,")
    s = re.sub(r"\b(times|divided by|plus|minus) open bracket", r"\1, open bracket", s)
    s = re.sub(r"(which (?:is|equals) %s(?: [a-z]+)?) and " % NUM, r"\1, and ", s)
    s = re.sub(r"(?<=[.?!] )open bracket", "Open bracket", s)
    if s.startswith("open bracket"):
        s = "O" + s[1:]
    if s.endswith(":"):
        s = s[:-1].rstrip() + "."
    s = re.sub(r"([!?])\.$", r"\1", s)
    if s and s[-1] not in ".?!\"”":
        s += "."
    return s
