"""Rules that turn printed Grade 4 ratio work into speech. Used by gr4_ratio.py.

Ratio notation is put into words here; everything else (fractions, money, units, sums)
is left to the fraction rules this topic shares.

    say(text)    the converter for this topic's notation
"""
import re

import gr4_fractions_rules as fr

from_latex = fr.from_latex

_N = r"(\d+(?:\.\d+)?|[A-Za-z]|\?|□)"


def _term(t):
    return {"?": "what", "□": "box"}.get(t, t)


def _ratio(m):
    text = m if isinstance(m, str) else m.group(0)
    return " is to ".join(_term(t) for t in re.split(r"\s*:\s*", text.strip()))


def ratios(s):
    """'3 : 5' is '3 is to 5'; 'a : b = c : d' (or '::') is 'a is to b, as c is to d'."""
    pair = r"%s\s*:\s*%s" % (_N, _N)
    s = re.sub(r"(?<![\w:])(%s)\s*(?:=|::)\s*(%s)(?![\w:])" % (pair, pair),
               lambda m: "%s, as %s" % (_ratio(m.group(1)), _ratio(m.group(4))), s)
    # a ratio is written with no spaces, or with a space on both sides of the colon
    s = re.sub(r"(?<![\w:.])\d+(?:\.\d+)?(?::\d+(?:\.\d+)?)+(?![\w:])", _ratio, s)
    s = re.sub(r"(?<![\w:.])\d+(?:\.\d+)?(?: : \d+(?:\.\d+)?)+(?![\w:])", _ratio, s)
    s = re.sub(r"(?<![\w:.])%s : %s(?: : %s)?(?![\w:])" % (_N, _N, _N), _ratio, s)
    return s


_FAMILY = [
    (r"Ratio = (\d+):(\d+), (\w+) = (\d+)",
     lambda m: "The ratio is %s is to %s, and %s is %s." % m.groups()),]


def labels(s):
    """'One part = 15 ÷ 5' reads as 'One part is 15 divided by 5'."""
    return re.sub(r"(^|[.,:;] )((?:Then |So |Now )?[A-Z][a-z']*(?: [a-z']+){0,4}) = (?=[\d₹])", r"\1\2 is ", s)


def family(text):
    s = (text or "").strip()
    for pat, fn in _FAMILY:
        m = re.fullmatch(pat, s)
        if m:
            return fn(m)
    return fr.family(text)


def say(text, sentence=False):
    s = (text or "").strip()
    if not s:
        return ""
    s = labels(ratios(s))
    return fr.say(s, sentence)
