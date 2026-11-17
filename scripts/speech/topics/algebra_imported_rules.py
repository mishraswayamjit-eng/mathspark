"""Rules for the imported Grade 5 algebra questions (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

These are story problems and textbook items, so the text is mostly prose with an equation here and
there. The rules wrap `algebra_rules.say` (which stays as it is, for the older questions) and deal
with what the imported text adds: the article "a" next to variables, "₹x", bullets, "*" for times,
explanations in brackets, and maths lines written in LaTeX.

    from algebra_imported_rules import say_imported, step_line
"""
import re

from algebra_rules import say
from common import number_tokens

ARTICLE = "\x06"
EQUALS = "\x07"

# After the letter a, these words mean it is a variable ("a and b", "a is 3"), not the article.
_AFTER_VARIABLE = {
    "and", "or", "is", "in", "into", "to", "for", "from", "by", "with", "when", "then", "are", "has",
    "was", "will", "must", "can", "gives", "becomes", "on", "equals", "times", "plus", "minus",
    "squared", "cubed", "if", "so", "we", "as", "at", "the", "of", "which", "but", "because",
}

_VULGAR = {"½": "one half", "¼": "one quarter", "¾": "three quarters", "⅓": "one third", "⅔": "two thirds"}

# Picture characters that carry no words.
_DROP = re.compile("[\U0001F000-\U0001FFFF\u2600-\u26FF\u2700-\u2713\u2715\u2716\u2718-\u27BF\uFE0F\u200D\u2B50\u2B06\u2B07]")


def _article(s):
    def fix(m):
        return "A" if m.group(1).lower() in _AFTER_VARIABLE else ARTICLE
    s = re.sub(r"\ba(?=\s+([A-Za-z]{2,}))", fix, s)
    s = re.sub(r"(?<![\d=+−×÷] )\ba(?=\s+[₹\d])", ARTICLE, s)
    return s


def _wordy_brackets(s):
    """(since Profit = Earnings − Cost) is an aside, not grouping: make it a clause of its own."""
    def fix(m):
        inner = m.group(1)
        if re.search(r"[A-Za-z]{3,}", inner):
            return ", " + inner.strip() + ", "
        return m.group(0)
    for _ in range(3):
        s = re.sub(r"\(([^()]*)\)", fix, s)
    return s


def prepare(text):
    s = text or ""
    s = re.sub(r"\s*%s+\s*(?=[A-Z])" % _DROP.pattern, ". ", s)          # a picture between two sentences
    s = _DROP.sub(" ", s)
    s = s.replace("**", "")                                              # bold marks
    s = re.sub(r"(?<![.!?:;,\s])\s*\n+\s*(?:•\s*)?", ". ", s)            # a line break ends a sentence
    s = re.sub(r"\s*\n+\s*(?:•\s*)?", " ", s)
    s = s.replace("•", ". ").replace("⇒", "→").replace("≤", " is at most ").replace("≥", " is at least ")
    s = re.sub(r"\byrs?\b\.?(?=\s+[A-Z])", "years,", s)
    s = re.sub(r"\byrs?\b\.?", "years", s)
    s = re.sub(r"\s&\s", " and ", s)
    s = re.sub(r"\b([A-D])\)\s+(?=[\dA-Za-z(])", r"\1, ", s)             # "the answer is B) 5y + x"
    s = re.sub(r"(?<=[A-Za-z]{3})/(?=[A-Za-z]{3})", " or ", s)           # add/subtract
    s = re.sub(r"(?<![\d/.])(\d+) (\d+)/(\d+)(?![\d/])", r"\1 and \2/\3", s)   # 27 1/2
    # n-1, 3n-5, x-2: a minus sign typed without spaces (but not x-terms, two-step, 50-paise)
    s = re.sub(r"(?<![A-Za-z\d])(\d*[A-Za-z]|\d+)-(\d+[A-Za-z]?|[A-Za-z])(?![A-Za-z\d])", r"\1 − \2", s)
    # a hyphen typed for minus, with spaces: "2b - (a + b)c", "x - y + z"
    s = re.sub(r"(\d|\)|(?<![A-Za-z])[A-Za-z]) - (?=[\d(−-]|[A-Za-z](?![A-Za-z]))", r"\1 − ", s)
    s = re.sub(r"\)\s*\((?=[^()]*\))", ") × (", s)                       # (4)(0) is 4 times 0
    s = re.sub(r"\)(?=[A-Za-z](?![A-Za-z]))", ") × ", s)                 # (a + b)c is the bracket times c
    s = re.sub(r":\s*→\s*", ": ", s)
    s = re.sub(r"\bIS\b", "is", s)
    s = re.sub(r"\b(gh|pq|lm|mn)\b", lambda m: " ".join(m.group(1)), s)
    s = re.sub(r"\ba(?=\s*[=+−×÷])", "A", s)
    s = re.sub(r"(?<=[=+−×÷]\s)a\b", "A", s)
    s = re.sub(r"\ba(?=,\s*b\b)", "A", s)
    s = re.sub(r"\ba(?=\s*[.,:;!?)]|\s*$)", "A", s)                       # "now multiply by a."
    # "the equation becomes 78 = 13 × N" is an equation, not a line of working
    s = re.sub(r"(\b(?:is|gives|becomes|holds?)\s+[\d\s+−×÷().]+)=(?=[^=.,;:!?→]*(?<![A-Za-z])[A-Za-z](?![A-Za-z]))", r"\1" + EQUALS, s)
    s = re.sub(r"(?<=\d)\s*([½¼¾⅓⅔])", lambda m: " and " + _VULGAR[m.group(1)], s)
    for k, v in _VULGAR.items():
        s = s.replace(k, " " + v + " ")
    s = re.sub(r"\s*\*\s*", " × ", s)
    s = re.sub(r"(?<=[a-z])\s*/\s*(?=(?:hour|week|day|month|minute|cup|box|packet|person|bag|row|piece|plate|game|ticket|child|student)\b)", " per ", s)
    s = re.sub(r"(?<=[\dA-Za-z)])\s*>\s*(?=[\dA-Za-z(−-])", " is greater than ", s)
    s = re.sub(r"(?<=[\dA-Za-z)])\s*<\s*(?=[\dA-Za-z(−-])", " is less than ", s)
    s = re.sub(r"(?:₹|Rs\.?)\s*(\d+(?:\.\d+)?)([a-z])\b", r"\1\2 rupees", s)   # ₹2x -> 2x rupees
    s = re.sub(r"(?:₹|Rs\.?)\s*([A-Za-z])\b", r"\1 rupees", s)          # ₹x -> x rupees
    s = re.sub(r"₹\s*\(([^()]*)\)", r"(\1) rupees", s)                   # ₹(3x − 15) -> (3x − 15) rupees
    s = re.sub(r"\(\s*in ₹\s*\)", "(in rupees)", s)
    s = re.sub(r"₹(?!\s*\d)", "rupees", s)
    s = re.sub(r"\b([Ll])et ([^.=:;,]{1,70}?) = ", r"\1et \2 be ", s)
    s = re.sub(r"=\s*\?", "= what?", s)
    s = _wordy_brackets(s)
    s = _separate_equations(s)
    s = _article(s)
    return s


def _separate_equations(s):
    """'substitute y = 10 into the equation 5x + 3y = 95' is two equations, not one chain of working.

    algebra_rules reads a second '=' in a clause as ', which is'. Where words stand between two
    equals signs, the second one is marked so that it is said as 'equals'.
    """
    out = []
    since = None            # text since the previous '=' in this clause, or None
    for ch in s:
        if ch in ".,:;!?→":
            since = None
        elif ch == "=":
            if since is not None and re.search(r"[A-Za-z]{2,}", since):
                ch = EQUALS
            since = ""
            out.append(ch)
            continue
        if since is not None:
            since += ch
        out.append(ch)
    s = "".join(out)
    # A clause word that algebra_rules splits on also ends a chain.
    return s


def finish(s, sentence=True):
    s = s.replace(ARTICLE, "a")
    s = re.sub(r"\s*%s\s*" % EQUALS, " equals ", s)
    s = re.sub(r"\b(\d+(?:\.\d+)?) rupees (discount|notes?|coins?|gift|bonus|snack|voucher|coupon|ticket|tip|packets?)\b", r"\1 rupee \2", s)
    s = re.sub(r"(\d), and (one|two|three) (half|thirds?|quarters?)\b", r"\1 and \2 \3", s)
    s = re.sub(r"\b(an?) (\d+(?:\.\d+)?) rupees (?=[a-z]{3,})(?!each|per|for|and|more|less|extra|from|with|total)", r"\1 \2 rupee ", s)
    s = re.sub(r"(?<![\d.,])1 rupees\b", "1 rupee", s)
    s = re.sub(r"\bminus minus\b", "minus, minus", s)
    s = re.sub(r"\byears (?=[A-Z][a-z])", "years, ", s)
    s = re.sub(r"(\d)([a-z]) (squared|cubed)\b", r"\1 \2 \3", s)
    s = re.sub(r"(\d) (?=(?:It|That|This|So|Now|Yes|Correct|Perfect|Great|The|She|He|Each|We|Do|Is|Are|And|Both|Step|They|Then|Check|Total|Everything|Find|What)\b)", r"\1. ", s)
    s = re.sub(r"(\d) (find|then|which of)\b", r"\1, \2", s)
    s = re.sub(r"\bequals what\?\.", "equals what?", s)
    s = re.sub(r":\.$", ".", s)
    s = re.sub(r"!\.", "!", s)
    if sentence and s and s[0].islower() and len(s) > 1 and s[1].islower():
        s = s[0].upper() + s[1:]
    return s.strip()


def say_imported(text, sentence=True):
    if not (text or "").strip():
        return ""
    return finish(say(prepare(text), sentence), sentence)


# ── Maths lines ──────────────────────────────────────────────────────────────

def latex_plain(latex):
    """A LaTeX maths line as plain print: \\frac{108}{9} -> 108/9, \\text{Total} -> Total."""
    s = latex or ""
    s = s.replace("\\\\", " . ")
    s = re.sub(r"\\(?:text|mathrm|textbf|mathbf)\{([^{}]*)\}", r" \1 ", s)
    s = re.sub(r"\\boxed\{([^{}]*)\}", r"\1", s)
    for _ in range(4):
        def frac(m):
            a, b = m.group(1).strip(), m.group(2).strip()
            simple = r"^[\w.₹ ]+$"
            a = a if re.match(simple, a) else "(%s)" % a
            b = b if re.match(simple, b) else "(%s)" % b
            return "%s/%s" % (a, b)
        s = re.sub(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    s = s.replace("\\times", "×").replace("\\cdot", "×").replace("\\div", "÷")
    # "2 − 2 = 0 ≠ 2" at the end of a line of working: "..., which is 0, not 2"
    s = re.sub(r"(=[^=]*?)\s*\\neq\s*", r"\1, not ", s)
    s = s.replace("\\neq", "≠")
    s = re.sub(r"\\(?:Rightarrow|implies|rightarrow|to)\b", "→", s)
    s = re.sub(r"\\(?:left|right|checkmark|displaystyle)\b", "", s)
    s = re.sub(r"\\(?:quad|qquad)\b|\\[,;! ]", " ", s)
    s = s.replace("\\%", "%").replace("\\$", "").replace("\\{", "(").replace("\\}", ")")
    s = re.sub(r"\^\{?2\}?", "²", s)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("{", " ").replace("}", " ")
    s = re.sub(r"(?<=[\w )])\s*-\s*(?=[\w (])", " − ", s)
    return re.sub(r"\s+", " ", s).strip()


def _norm(s):
    return re.sub(r"[\s₹,]", "", s).replace("-", "−").lower()


def _subsequence(small, big):
    it = iter(big)
    return bool(small) and all(x in it for x in small)


def step_line(text, latex):
    """A solution step: its text, then its maths line unless the text already says it."""
    spoken = say_imported(text)
    plain = latex_plain(latex)
    if not plain or _norm(plain) in _norm(text):
        return spoken
    ends_open = (text or "").rstrip().endswith(":")
    if not ends_open:
        if plain.startswith("="):
            return spoken                       # "= 20" under "the result equals 20"
        terms = [t for t in re.split(r"=|→|,|\band\b|≠|\bnot\b", plain) if t.strip()]
        if "=" in (text or "") and all(_norm(t) in _norm(text) for t in terms):
            return spoken                       # the text already walks through this working
    maths = say_imported(plain)
    if not maths:
        return spoken
    if re.search(r"[:,]\.?$", spoken) or (text or "").rstrip().endswith(":"):
        if maths.startswith("That equals "):
            maths = "that" + maths[4:]
        head = re.sub(r"[:,.]+$", "", spoken)
        return head + (" " if head[-1:] in "!?" else ": ") + maths
    return spoken + " " + maths
