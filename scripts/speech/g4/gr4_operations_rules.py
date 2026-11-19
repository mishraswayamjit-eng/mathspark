"""Rules that turn printed whole-number arithmetic (Grade 4 operations and BODMAS) into speech.

    say(text, kind="text")   the spoken form of one printed string ("option" for an answer choice)
    say_maths(latex)         a step's maths line, spoken

How a sum is read:
  - signs between numbers: "times", "divided by", "plus", "minus", "equals";
  - brackets that group a sum are spoken, because here they change the answer:
    "open bracket, 15 plus 5, close bracket, times 3" (square and curly brackets are named);
  - a long sum that mixes multiplying or dividing with adding gets a short pause before each
    plus and minus, the way a teacher reads it: "13, minus 2 times 3, plus 15 divided by 3";
  - a chain of equals reads "..., equals ..., which equals ...";
  - a sum ending "= ?" becomes "What is ...?";
  - a sign on its own is named: "plus", "minus", "times", "divide", "greater than";
  - a box or blank between numbers is "box" (when the print talks of a box) or "blank";
  - a bracket shown on its own, as a choice of where to put it, is "a bracket around ...".
"""
import re

SIGN_NAMES = {"+": "plus", "−": "minus", "-": "minus", "×": "times", "÷": "divide", "=": "equals",
              ">": "greater than", "<": "less than", "≈": "about"}
BINARY = {"+": "plus", "−": "minus", "-": "minus", "×": "times", "÷": "divided by", "of": "of"}
COMPARE = {"=": "equals", ">": "is greater than", "<": "is less than", "≈": "is about"}
BRACKET = {"(": "bracket", "[": "square bracket", "{": "curly bracket"}
CLOSER = {"(": ")", "[": "]", "{": "}"}
WORD_FRACTIONS = {("1", "2"): "one half", ("1", "3"): "one third", ("2", "3"): "two thirds",
                  ("1", "4"): "one quarter", ("3", "4"): "three quarters"}

TOKEN = re.compile(r"""
    (?P<FRAC>(?<![\d/.,])\d+\s*/\s*\d+(?![\d/]))
  | (?P<NUM>(?:(?:₹|Rs\.?)\s*)?\d+(?:,\d+)*(?:\.\d+)?(?:\s*%)?)
  | (?P<OF>(?<=\d)\s+of\s+(?=[\d(\[{]))
  | (?P<OP>[×÷+−=≈<>] | (?<=\d)\s*[-–]\s*(?=\d) | (?<![\w.])-(?=\d))
  | (?P<LB>[(\[{])
  | (?P<RB>[)\]}])
  | (?P<BOX>□|_{2,}|★)
  | (?P<QM>\?)
  | (?P<WS>\s+)
  | (?P<TEXT>[A-Za-z']+|.)
""", re.X)

MATHS = {"FRAC", "NUM", "OF", "OP", "LB", "RB", "BOX", "QM"}

UNITS = [
    (r"\bkm\s*/\s*h(?:r|our)?\b", "kilometres per hour"),
    (r"(?<=\d)\s*ml\b", " millilitres"), (r"(?<=\d)\s*km\b", " kilometres"), (r"(?<=\d)\s*cm\b", " centimetres"),
    (r"(?<=\d)\s*kg\b", " kilograms"), (r"(?<=\d)\s*m\b", " metres"), (r"(?<=\d)\s*g\b", " grams"),
]


def number(tok):
    m = re.match(r"(₹|Rs\.?)?\s*([\d,]+(?:\.\d+)?)\s*(%)?$", tok)
    if not m:
        return tok
    n = m.group(2)
    if m.group(1):
        return n + (" rupee" if n == "1" else " rupees")
    if m.group(3):
        return n + " percent"
    return n


def fraction(tok):
    a, b = [p.strip() for p in tok.split("/")]
    return WORD_FRACTIONS.get((a, b)) or "%s over %s" % (a, b)


def tokenize(s):
    toks = []
    for m in TOKEN.finditer(s):
        kind = m.lastgroup
        text = m.group(0)
        if kind == "OP":
            text = text.strip().replace("–", "−").replace("-", "−")
        if kind == "OF":
            kind, text = "OP", "of"
        toks.append([kind, text])
    # Pair the brackets. A pair is maths only if everything inside it is maths.
    stack = []
    for i, (kind, text) in enumerate(toks):
        if kind == "LB":
            stack.append(i)
        elif kind == "RB":
            if stack and CLOSER[toks[stack[-1]][1]] == text:
                j = stack.pop()
                inside = toks[j + 1:i]
                ok = any(k in ("NUM", "FRAC") for k, _ in inside) and all(k in MATHS or k == "WS" for k, _ in inside)
                if not ok:
                    toks[j][0] = toks[i][0] = "TEXT"
            else:
                toks[i][0] = "TEXT"
    for j in stack:
        toks[j][0] = "TEXT"
    # A question mark is part of a sum only next to a sign ("7 × ? = 91", "= ?").
    solid = [i for i, (k, _) in enumerate(toks) if k != "WS"]
    for n, i in enumerate(solid):
        if toks[i][0] == "QM":
            before = toks[solid[n - 1]] if n else None
            after = toks[solid[n + 1]] if n + 1 < len(solid) else None
            if not ((before and before[0] == "OP") or (after and after[0] == "OP")):
                toks[i][0] = "TEXT"
    return toks


def tree(toks):
    """Nest a flat run of maths tokens by its brackets."""
    root = []
    stack = [root]
    for kind, text in toks:
        if kind == "LB":
            group = ["GROUP", text, []]
            stack[-1].append(group)
            stack.append(group[2])
        elif kind == "RB":
            if len(stack) > 1:
                stack.pop()
        else:
            stack[-1].append([kind, text])
    return root


def side(items, box):
    """One side of an equals sign."""
    if any(it[0] == "BOX" for it in items):
        # A box or blank stands between two sums: read each on its own.
        chunks, cur = [], []
        for it in items:
            if it[0] == "BOX":
                chunks.append(cur)
                cur = []
            else:
                cur.append(it)
        chunks.append(cur)
        spoken = [side(c, box) if c else "" for c in chunks]
        out = spoken[0]
        for more in spoken[1:]:
            out = (out.rstrip(",") + ", " if out else "") + box + (", " + more if more else "")
        return out
    ops = [it[1] for it in items if it[0] == "OP"]
    pauses = len(ops) >= 4 and any(o in ("×", "÷", "of") for o in ops) and any(o in ("+", "−") for o in ops)
    out = []
    for n, it in enumerate(items):
        kind = it[0]
        last = n == len(items) - 1
        if kind == "NUM":
            out.append(number(it[1]))
        elif kind == "FRAC":
            word = fraction(it[1])
            out.append(word + ("," if " over " in word and not last else ""))
        elif kind == "OP":
            unary = it[1] == "−" and (n == 0 or items[n - 1][0] == "OP")
            if pauses and it[1] in ("+", "−") and not unary and out:
                out[-1] = out[-1].rstrip(",") + ","
            out.append(BINARY[it[1]])
        elif kind == "QM":
            out.append("what")
        elif kind == "GROUP":
            name = BRACKET[it[1]]
            out.append("open %s, %s, close %s%s" % (name, expression(it[2], box), name, "" if last else ","))
    return " ".join(out)


def expression(items, box="blank", which=False):
    """A sum, possibly with equals signs, as speech. `which`: say a lone equals as ', which is'."""
    sides, seps, cur = [], [], []
    for it in items:
        if it[0] == "OP" and it[1] in COMPARE:
            sides.append(cur)
            seps.append(it[1])
            cur = []
        else:
            cur.append(it)
    sides.append(cur)
    equals = sum(1 for s in seps if s == "=")
    out = side(sides[0], box) if sides[0] else ""
    for n, sep in enumerate(seps):
        right = side(sides[n + 1], box)
        word = COMPARE[sep]
        if not out:
            out = word + " " + right
            continue
        left = sides[n]
        heavy = left and (any(i[0] == "GROUP" for i in left) or out.endswith(",") or len([i for i in left if i[0] == "OP"]) >= 4
                          or any(i[0] == "BOX" for i in left))
        if sep == "=" and equals > 1:
            word = ", which equals" if n == len(seps) - 1 else ", equals"
        elif sep == "=" and which and len(seps) == 1:
            word = ", or" if which == "or" else ", which is"
        elif heavy:
            word = ", " + word
        else:
            word = " " + word
        out = out.rstrip(",") + word + " " + right
    return out.strip()


def span(toks, before, at_end, kind, box):
    """Speech for one run of maths tokens. `before` is the text spoken so far."""
    solid = [t for t in toks if t[0] != "WS"]
    kinds = [t[0] for t in solid]
    # Signs on their own are named.
    if all(k == "OP" for k in kinds):
        if kind == "option" and len(solid) == 1 and solid[0][1] in ("=", "<", ">"):
            return "the %s sign" % SIGN_NAMES[solid[0][1]]
        if len(solid) == 1 and solid[0][1] == "=" and kind != "option":
            return "equals"
        return ", ".join(SIGN_NAMES[t[1]] for t in solid)
    if kinds == ["QM"]:
        return "what"
    if all(k == "BOX" for k in kinds):
        return box
    items = tree(solid)
    # A bracket on its own: a choice of where the bracket goes.
    if len(items) == 1 and items[0][0] == "GROUP" and items[0][1] == "(" and not any(i[0] == "GROUP" for i in items[0][2]):
        inner = expression(items[0][2], box)
        if re.search(r"\baround\s*$", before):
            return inner
        return ("a %s around " % BRACKET[items[0][1]]) + inner
    # "... = ?" at the end of the string.
    if at_end and len(items) >= 3 and items[-1][0] == "QM" and items[-2] == ["OP", "="]:
        body = expression(items[:-2], box)
        if not before.strip() or re.search(r"(?:Work out|Simplify|Solve|Find):\s*$", before):
            return "what is " + body + "?"
        return body + ", equals what?"
    # A line of working that starts with an equals sign.
    if items[0] == ["OP", "="] and not before.strip():
        rest = expression(items[1:], box)
        return "that is " + rest.replace(" equals ", ", which equals ", 1) if ", which equals" not in rest else "that is " + rest
    if items[0][0] == "OP" and items[0][1] in COMPARE:
        return expression(items, box)
    # "which is 6 × 12 = 72": after a verb, the equals reads better as ", which is".
    which = bool(re.search(r"\b(?:is|are|was|be|costs?|gives?|by|gets?|got|makes?|means|ha[ds]|have|needs?|adds?|with|from|to|least|than)(?: also)?\s*$", before))
    if re.search(r"\bwhich is\s*$", before):
        which = "or"            # "which is 6 × 12 = 72": not "which is ..., which is ..."
    return expression(items, box, which)


def presub(s):
    s = s.replace("✓", "")
    s = re.sub(r"\s*\(Q\s*(\d+)\)", r", question \1", s)
    s = re.sub(r"\bIPM\b", "I P M", s)
    for pat, rep in UNITS:
        s = re.sub(pat, rep, s)
    s = re.sub(r"\s+—\s+", ", ", s)
    s = re.sub(r"\b([A-Za-z]{3,})/([A-Za-z]{3,})\b", r"\1 and \2", s)
    s = re.sub(r"\b(?!BODMAS\b)[A-Z]{3,}\b", lambda m: m.group(0).lower(), s)
    return s


def tidy(s):
    s = re.sub(r"\s*\(\s*", ", ", s)          # brackets that were only punctuation
    s = re.sub(r"\s*\)(?=\s*\w)", ",", s)
    s = s.replace(")", "")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",(?=[A-Za-z])", ", ", s)
    s = re.sub(r"\?\?+", "?", s)
    s = re.sub(r",\s*,+", ",", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"([.?!:;])\s*,\s*", r"\1 ", s)
    s = re.sub(r"^[,\s]+", "", s)
    s = s.strip()
    return s


def capitalise(s):
    def up(m):
        return m.group(1) + m.group(2).upper()
    s = re.sub(r"^(\s*)([a-z])", up, s)
    return re.sub(r"([.?!]\s+)([a-z])", up, s)


def say(text, kind="text", box=None):
    """`box`: the word for a box or blank in a sum; by default "box" if the line talks of a box."""
    s = (text or "").strip()
    if not s:
        return ""
    m = re.match(r"Correct answer: Option (\d) — (.*)$", s)
    if m:
        choice = say(m.group(2), "option").rstrip(".")
        if re.match(r"(A|The|None) ", choice):
            choice = choice[0].lower() + choice[1:]
        return "The correct answer is option %s: %s." % (m.group(1), choice)
    m = re.match(r"([÷×+−]) \((\w+)\)$", s)
    if m and kind == "option":
        return "The %s sign" % m.group(2)
    # Profit and loss working, printed as a chain of equals signs.
    m = re.match(r"(Profit|Loss) = (\d+)% of Rs\.(\d+) = Rs\.(\d+)$", s)
    if m:
        return "The %s is %s percent of %s rupees, which is %s rupees." % ((m.group(1).lower(),) + m.groups()[1:])
    m = re.match(r"SP = CP ([+−]) (Profit|Loss) = (\d+) [+−] (\d+) = Rs\.(\d+)$", s)
    if m:
        sign = "plus" if m.group(1) == "+" else "minus"
        return "Selling price equals cost price %s %s. That is %s %s %s, which equals %s rupees." % (
            sign, m.group(2).lower(), m.group(3), sign, m.group(4), m.group(5))
    s = presub(s)
    box = box or ("box" if re.search(r"\bbox", s) else "blank")
    toks = tokenize(s)
    out = ""
    i = 0
    while i < len(toks):
        if toks[i][0] in MATHS:
            j = i
            end = i + 1
            while j < len(toks) and (toks[j][0] in MATHS or toks[j][0] == "WS"):
                if toks[j][0] in MATHS:
                    end = j + 1
                j += 1
            at_end = not "".join(t[1] for t in toks[end:]).strip()
            spoken = span(toks[i:end], out, at_end, kind, box)
            lone = end - i == 1 and toks[i][0] == "NUM" and toks[i][1][0].isdigit()
            if out and out[-1].isalnum() and not lone:
                out += " "
            out += spoken
            nxt = toks[end][1] if end < len(toks) else ""
            if nxt[:1].isalpha() and not lone:
                out += " "
            elif re.search(r", (?:plus|minus|close|box|blank)\b", spoken) and ", which" not in spoken and nxt.isspace() and end + 1 < len(toks) and toks[end + 1][1][:1].isalpha():
                out += ","          # a long sum ends: pause before the sentence carries on
            elif re.search(r", (?:which is|or) ", spoken) and nxt.isspace() and end + 1 < len(toks) and toks[end + 1][1] in ("and", "up", "but"):
                out += ","
            i = end
        else:
            out += toks[i][1]
            i += 1
    out = capitalise(tidy(out))
    if s.endswith("?") and out[-1:] not in "?.!":
        out += "?"
    return out


def from_latex(latex):
    s = latex
    s = re.sub(r"\\boxed\{(.*)\}", r"\1", s)
    s = re.sub(r"\\text\{([^}]*)\}", r"\1", s)
    s = re.sub(r"\\frac\{([^}]*)\}\{([^}]*)\}", r"\1/\2", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\,", " ")
    s = re.sub(r"(?<=\d)\s*-\s*(?=[\d(])", " − ", s)
    return s


def say_maths(latex):
    """A maths line as speech. Two sums side by side are joined with 'and'."""
    parts = [p.strip(" ,;") for p in re.split(r"\\q?quad", from_latex(latex)) if p.strip(" ,;")]
    spoken = [say(p) for p in parts]
    if not spoken or not all(spoken):
        return ""
    out = spoken[0]
    for more in spoken[1:]:
        out += ", and " + more[0].lower() + more[1:]
    return out
