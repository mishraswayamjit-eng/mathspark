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
    # generated: bags of a given weight
    (r"Convert (\d+) kg (\d+) g to grams: (\d+) × (\d+) \+ (\d+) = (\d+) g",
     lambda m: "Convert %s kilograms %s grams to grams: %s times %s, plus %s, equals %s grams." % m.groups()),
    (r"(\d+) kg = (\d+) g, plus (\d+) g = (\d+) g\.",
     lambda m: "%s kilograms is %s grams, and %s grams more makes %s grams." % m.groups()),
    (r"One bag = (\d+) kg (\d+) g = (\d+) g",
     lambda m: "One bag is %s kilograms %s grams, which is %s grams." % m.groups()),
    (r"Total = (\d+) × (\d+) = (\d+) g",
     lambda m: "The total is %s times %s, which is %s grams." % m.groups()),
    # generated: glasses from a container
    (r"First convert litres to ml: 1 litre = 1000 ml\.",
     lambda m: "First convert litres to millilitres: 1 litre is 1000 millilitres."),
    (r"Then divide total ml by the glass size\.",
     lambda m: "Then divide the total millilitres by the glass size."),
    (r"(\d+) litres = (\d+) ml\.",
     lambda m: "%s litres is %s millilitres." % m.groups()),
    (r"Convert: (\d+) litres = (\d+) ml",
     lambda m: "Convert: %s litres is %s millilitres." % m.groups()),
    (r"Number of glasses = (\d+) ÷ (\d+) = (\d+)",
     lambda m: "The number of glasses is %s divided by %s, which is %s." % m.groups()),
]


def family(text):
    s = (text or "").strip()
    for pat, fn in _FAMILY:
        m = re.fullmatch(pat, s)
        if m:
            return fn(m)
    return base.family(text)
