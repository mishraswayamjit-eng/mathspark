"""Rules that turn printed Grade 4 measurement work (units, dozens, scores, gross) into speech.

Built on gr4_decimals_rules (the same writer's rules for decimals, money and units); this file adds
the whole-line patterns of the measurement families. Used by gr4_units.py.
"""
import re

import gr4_decimals_rules as base

say = base.say
from_latex = base.from_latex
UNITS = base.UNITS

_U = "|".join(sorted(UNITS, key=len, reverse=True)) + "|tonnes?|litres?|metres?|grams?|kilograms?"


def _plural(u):
    if u in UNITS:
        return UNITS[u][1]
    return u if u.endswith("s") else u + "s"


def _qty(text):
    return say(text).rstrip(".")


_FAMILY = [
    # fill the blank: '3 m = _______ cm', '2.5 kg = _______ kg _______ g'
    (r"(.+?)\s*=\s*_{2,}\s*(%s)\s*_{2,}\s*(%s)" % (_U, _U),
     lambda m: "%s equals how many %s, and how many %s?" % (_qty(m.group(1)), _plural(m.group(2)), _plural(m.group(3)))),
    (r"(.+?)\s*=\s*_{2,}\s*(%s)" % _U,
     lambda m: "%s equals how many %s?" % (_qty(m.group(1)), _plural(m.group(2)))),
    # (the whole-line patterns for the old 'bags of a given weight' and 'glasses from a container'
    #  families were removed in round 3: their hints and steps are now plain sentences that say() reads)
]


def family(text):
    s = (text or "").strip()
    for pat, fn in _FAMILY:
        m = re.fullmatch(pat, s)
        if m:
            return fn(m)
    return base.family(text)
