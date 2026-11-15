"""Rules for the generated families of the measurement-speed topic.

Units are said in full, singular after 1 and plural otherwise; compound units become
"kilometres per hour" and "metres per second"; a chain of working "A = B = C" becomes
"A equals B, which is C."
"""
import re

# abbreviation -> (singular, plural)
UNIT_WORDS = {
    "km": ("kilometre", "kilometres"), "m": ("metre", "metres"), "cm": ("centimetre", "centimetres"),
    "mm": ("millimetre", "millimetres"), "dm": ("decimetre", "decimetres"),
    "kg": ("kilogram", "kilograms"), "g": ("gram", "grams"), "mg": ("milligram", "milligrams"),
    "hg": ("hectogram", "hectograms"), "dag": ("decagram", "decagrams"),
    "l": ("litre", "litres"), "ml": ("millilitre", "millilitres"), "kl": ("kilolitre", "kilolitres"),
    "dal": ("decalitre", "decalitres"), "hl": ("hectolitre", "hectolitres"),
    "h": ("hour", "hours"), "hr": ("hour", "hours"), "hrs": ("hour", "hours"),
    "min": ("minute", "minutes"), "mins": ("minute", "minutes"),
    "s": ("second", "seconds"), "sec": ("second", "seconds"), "secs": ("second", "seconds"),
    "ft": ("foot", "feet"),
    "litre": ("litre", "litres"), "litres": ("litre", "litres"),
}
_ABBR = "|".join(sorted((re.escape(u) for u in UNIT_WORDS), key=len, reverse=True))
# Units safe to expand even without a number in front (never a variable or a word).
_BARE = {"km", "cm", "mm", "kg", "mg", "ml", "kl"}

_COMPOUND = [
    (r"\bkm\s*/\s*h(?:r|our)?\b|\bkmph\b|\bkm per hour\b", "kilometres per hour"),
    (r"\bm\s*/\s*s(?:ec)?\b", "metres per second"),
    (r"\bcm\s*/\s*s(?:ec)?\b", "centimetres per second"),
    (r"\bkm\s*/\s*min\b", "kilometres per minute"),
    (r"\bm\s*/\s*min\b", "metres per minute"),
]


def _numbered(m):
    number, unit = m.group(1), m.group(2)
    single, plural = UNIT_WORDS[unit]
    one = number.replace(",", "") in ("1", "1.0")
    return "%s %s" % (number, single if one else plural)


def units(s):
    """Expand unit abbreviations in a piece of text."""
    for pat, rep in _COMPOUND:
        s = re.sub(pat, rep, s)
    s = re.sub(r"\bsq\.?\s*cm\b", "square centimetres", s)
    s = re.sub(r"\bsq\.?\s*m\b", "square metres", s)
    s = re.sub(r"\bsq\.?\s*km\b", "square kilometres", s)
    s = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*(%s)\b" % _ABBR, _numbered, s)
    s = re.sub(r"\b(%s)\b" % "|".join(sorted(_BARE)), lambda m: UNIT_WORDS[m.group(1)][1], s)
    # "Convert 1400 cm to m." : a bare single letter after "to" or "in" is a unit here
    s = re.sub(r"\b(to|in|many) m\b", r"\1 metres", s)
    s = re.sub(r"\b(to|in) g\b", r"\1 grams", s)
    s = re.sub(r"\b(to|in) l\b", r"\1 litres", s)
    return s


def chain(s):
    """Working with symbols to a spoken sentence: first '=' is 'equals', later ones ', which is'."""
    seen = [0]

    def eq(_m):
        seen[0] += 1
        return " equals " if seen[0] == 1 else ", which is "

    s = re.sub(r"\s*=\s*", eq, s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    return s


def tidy(s):
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    if s and s[-1] not in ".?!:":
        s += "."
    return s


# Lines that are the same in every question of a family, written by hand.
FIXED = {
    "Area = l×w": "Area equals length times width.",
    "Area = side×side": "Area equals side times side.",
    "Perimeter = 2×(l+w)": "Perimeter equals 2 times, open bracket, length plus width, close bracket.",
    "Perimeter = 4×side": "Perimeter equals 4 times side.",
    "Average speed = Total distance ÷ Total time (NOT the average of speeds!).":
        "Average speed equals total distance, divided by total time. Not the average of speeds!",
    "Use the formula: Time = Distance ÷ Speed.": "Use the formula: time equals distance divided by speed.",
    "Use: Distance = Speed × Time.": "Use: distance equals speed times time.",
    "Use: Speed = Distance ÷ Time.": "Use: speed equals distance divided by time.",
    "Find the time for each part: time = distance ÷ speed.":
        "Find the time for each part: time equals distance divided by speed.",
    "Time = Distance ÷ Speed": "Time equals distance divided by speed.",
    "Distance = Speed × Time": "Distance equals speed times time.",
    "Speed = Distance ÷ Time": "Speed equals distance divided by time.",
    "The answer is in sq.cm.": "The answer is in square centimetres.",
}


def _legs(m):
    parts = re.findall(r"(\d+)÷(\d+)=(\d+)h", m.group(1))
    said = ["%s divided by %s equals %s %s" % (a, b, c, "hour" if c == "1" else "hours") for a, b, c in parts]
    return "Time for each leg: " + ", ".join(said[:-1]) + ", and " + said[-1] + "."


TEMPLATES = [
    (r"^Time for each leg: (.+)$", _legs),
    (r"^Answer = (\d+) (sq\.cm|cm)$",
     lambda m: "The answer is %s %s." % (m.group(1), "square centimetres" if m.group(2) != "cm" else "centimetres")),
    (r"^One bag = (\d+) kg (\d+) g = (\d+) g$",
     lambda m: "One bag is %s, which equals %s grams." % (units("%s kg %s g" % (m.group(1), m.group(2))), m.group(3))),
    (r"^(\d+) kg = (\d+) g, plus (\d+) g = (\d+) g\.$",
     lambda m: "%s equals %s grams, plus %s grams, which makes %s grams." % (units(m.group(1) + " kg"), m.group(2), m.group(3), m.group(4))),
]


def say(text):
    """One generated-family string as spoken words."""
    if not text.strip():
        return ""
    if text in FIXED:
        return FIXED[text]
    for pat, fn in TEMPLATES:
        m = re.match(pat, text)
        if m:
            return fn(m)
    return tidy(chain(units(text)))


def say_option(text):
    return tidy(units(text)).rstrip(".") if not re.match(r"^[\d,.]+$", text) else text
