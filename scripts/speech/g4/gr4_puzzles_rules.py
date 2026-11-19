"""Rules that turn the printed text of Grade 4 questions into speech.

Written for gr4_puzzles; gr4_time_rules and gr4_data_rules (same author) build on say() through
its `pre` and `post` hooks.
"""
import re

KEEP_CAPS = {"MATH", "AM", "PM", "II", "III", "IV", "VI", "VII", "VIII", "IX", "XI", "XII"}
SPELL = {"IPM": "I P M", "HCF": "H C F", "LCM": "L C M"}
ROW_NAMES = ["First row", "Second row", "Third row", "Fourth row", "Fifth row", "Sixth row", "Seventh row", "Eighth row"]
OPS = "+−×÷"


def from_latex(latex):
    s = latex
    for _ in range(3):
        s = re.sub(r"\\boxed\{((?:[^{}]|\{[^{}]*\})*)\}", r"\1", s)
        s = re.sub(r"\\d?frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", s)
        s = re.sub(r"\\(?:text|mathbf|mathrm|textbf|mathit)\{([^{}]*)\}", r"\1", s)
    for a, b in ((r"\times", "×"), (r"\div", "÷"), (r"\qquad", ". "), (r"\quad", ". "), (r"\checkmark", ""),
                 (r"\cdot", "×"), (r"\ldots", "..."), (r"\dots", "..."), (r"\rightarrow", "→"), (r"\Rightarrow", "→"),
                 (r"\to", "→"), (r"\%", "%"), (r"\,", " "), (r"\;", " "), (r"\!", ""), (r"\ ", " "),
                 (r"^\circ", "°"), (r"\circ", "°"), (r"\neq", "≠"), (r"\left", ""), (r"\right", "")):
        s = s.replace(a, b)
    s = s.replace("^2", "²").replace("^{2}", "²")
    s = re.sub(r"(?<=[\dA-Za-z)?]) ?- ?(?=[\dA-Za-z(?])", " − ", s)
    s = re.sub(r"\s*\.\s*\.\s+", ". ", s)
    s = re.sub(r",\s*\.\s+", ". ", s)
    return re.sub(r"\s+", " ", s).strip()


def table(lines):
    """Rows printed as | a | b | c | become 'Top row: a, b, c.'"""
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r"[-: ]*", c) for c in cells) and any("-" in c for c in cells):
            continue
        rows.append(["blank" if c in ("", "?", "_", "__", "___") else c for c in cells])
    names = ["Top row", "Middle row", "Bottom row"] if len(rows) == 3 else ROW_NAMES
    return " ".join("%s: %s." % (names[i] if i < len(names) else "Next row", ", ".join(r)) for i, r in enumerate(rows))


def join_lines(text):
    out = []
    block = []
    for line in text.split("\n") + [""]:
        if line.strip().startswith("|"):
            block.append(line)
            continue
        if block:
            out.append(table(block))
            block = []
        if line.strip():
            out.append(line.strip())
    s = ""
    for piece in out:
        if s and s[-1] not in ".?!:;,":
            s += "."
        elif s and s[-1] == ":" and piece.startswith(("Top row", "First row")):
            s = s[:-1] + "."
        s += (" " if s else "") + piece
    return s


def placeholder(m):
    s = m.string
    before = s[:m.start()].rstrip()
    after = s[m.end():].lstrip()
    prev, nxt = before[-1:], after[:1]
    if prev and prev in OPS:
        return "what number"
    if nxt == "=":
        return "the missing number"
    if prev == "=":
        return "what?" if (not after or after[0].isupper()) else "what"
    if (prev and prev in OPS) or (nxt and nxt in OPS):
        return "what number"
    return "blank"


def equals(s):
    """The first = in a clause is 'equals'; later ones in the same clause are ', which is'."""
    out = []
    for piece in re.split(r"((?<!\d)[.,;:?!]|[.,;:?!](?!\d)|\band\b|\bso\b|\bthen\b|\bbecause\b|\bsince\b)", s):
        n = [0]

        def rep(m):
            n[0] += 1
            return " equals " if n[0] == 1 else ", which is "
        out.append(re.sub(r"\s*=\s*", rep, piece))
    return "".join(out)


def brackets(s):
    """Brackets that group maths next to more maths are said aloud; the rest become pauses."""
    def rep(m):
        inner = m.group(1)
        before = m.string[:m.start()].rstrip()[-1:]
        after = m.string[m.end():].lstrip()[:1]
        if re.search(r"[+−×÷]", inner) and ((before and (before in OPS or before.isdigit())) or (after and after in OPS + "²(")):
            return " open bracket " + inner + " close bracket "
        return ", " + inner + ", "
    for _ in range(2):
        s = re.sub(r"\(([^()]*)\)", rep, s)
    return s


def space_lists(s):
    """'11,12,13' is a list, so say it with pauses; '2,345' is one number, so leave it."""
    def rep(m):
        run = m.group(0)
        if common_grouped.fullmatch(run):
            return run
        return run.replace(",", ", ")
    return re.sub(r"\d+(?:,\d+)+", rep, s)


common_grouped = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})+,\d{3})")


def say(text, pre=None, post=None):
    s = join_lines(text or "")
    lower_start = s[:1].islower()
    if pre:
        s = pre(s)
    s = re.sub(r"^Correct answer: Option (\d+)\s*[—–-]\s*", r"The correct answer is option \1: ", s)
    s = s.replace("✓", "").replace("✔", "").replace("…", "...")
    s = re.sub(r"\.\.\.\s*(?=[a-z])", ", and so on, ", s)
    s = re.sub(r"\.\.\.", ".", s)
    s = re.sub(r"\s*[→⇒]\s*", ", so ", s)
    s = re.sub(r"\s+[—–]\s+", ", ", s)
    s = space_lists(s)
    # money, percent, degrees
    s = re.sub(r"(?:₹|\bRs\.?)\s*(\d+(?:,\d+)*(?:\.\d+)?)", r"\1 rupees", s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(\d)\s*°", r"\1 degrees", s)
    # exam references and abbreviations
    s = re.sub(r"\s*\(Q\.?\s*(\d+)\)", r", question \1", s)
    for k, v in SPELL.items():
        s = re.sub(r"\b%s\b" % k, v, s)
    # a range printed with a hyphen
    s = re.sub(r"(\d)[-–](\d)", r"\1 to \2", s)
    s = re.sub(r"(\d)\s+[-–]\s+(?=\d)", r"\1 − ", s)
    # grid sizes
    s = re.sub(r"(\d)\s*[×x]\s*(\d)(?=\s+(?:magic|grid|square|array|table))", r"\1 by \2", s)
    # placeholders
    s = re.sub(r"_{2,}", " blank ", s)
    s = s.replace("□", " blank ").replace("★", " star ").replace("*", " star ")
    s = re.sub(r"(?<![\w)'\"!?.’”])\?", placeholder, s)
    for k, v in {"½": " one half ", "¼": " one quarter ", "¾": " three quarters ", "²": " squared ", "³": " cubed "}.items():
        s = s.replace(k, v)
    # letters that stand for digits or numbers
    s = re.sub(r"\b(\d+)([A-Z])(\d*)\b", lambda m: " ".join(x for x in m.groups() if x), s)
    s = re.sub(r"\b([A-Z])(\d+)\b", r"\1 \2", s)
    s = re.sub(r"\b([PQRS])([PQRS])\b", r"\1 \2", s)
    s = re.sub(r"\b(\d+)ab\b", r"\1 a b", s)
    s = re.sub(r"\bab\b", "a b", s)
    # emphasis in capitals
    s = re.sub(r"\b[A-Z]{3,}\b", lambda m: m.group(0) if m.group(0) in KEEP_CAPS else m.group(0).lower(), s)
    # a line of working that starts with =
    s = re.sub(r"^\s*=\s*", "That equals ", s)
    s = brackets(s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    s = equals(s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    s = s.replace("√", " the square root of ").replace("≠", " is not equal to ")
    s = s.replace("<", " is less than ").replace(">", " is greater than ")
    if post:
        s = post(s)
    # tidy
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*([.?!:;,])", r"\1", s)
    s = re.sub(r"([:;])\s*,", r"\1", s)
    s = re.sub(r"([.?!])\s*\.(?!\.)", r"\1", s)
    s = re.sub(r"^[,.\s]+", "", s)
    s = re.sub(r"\b(of|and|times|by|plus|minus),\s", r"\1 ", s)
    s = re.sub(r",\s+(times|plus|minus|divided by),\s", r" \1 ", s)
    s = re.sub(r"\s*,\s*$", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"([.?!] )([a-z])(?=[a-z])", lambda m: m.group(1) + m.group(2).upper(), s)
    if s and not lower_start:
        s = s[0].upper() + s[1:]
    return s
