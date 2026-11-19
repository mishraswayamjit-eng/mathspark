"""Notation rules for the newly added Grade 5 questions: print to speech, one string at a time."""
import re

# Words printed in capitals for emphasis: said as ordinary words.
_PLAIN_CAPS = {
    "EVERY", "EACH", "BOTH", "NOT", "ALL", "ONE", "ONLY", "MUST", "SAME", "EXACTLY", "NEVER",
    "ALWAYS", "BEFORE", "AFTER", "LEAST", "MOST", "TOTAL", "WHOLE", "NEW", "OLD", "ANY", "TWO", "THREE",
    "FIRST", "LAST", "LEFT", "RIGHT", "MORE", "LESS", "THAN",
    "PER", "FROM", "ORIGINAL", "COST", "SELLING", "MARKED", "PRICE", "DIFFERENT", "TOGETHER", "SMALLER",
    "LARGER", "GREATEST", "SMALLEST", "ODD", "EVEN", "SUM", "PRODUCT", "DIFFERENCE", "BODMAS",
}
_KEEP_CAPS = {"BODMAS"}

_UNIT_WORDS = {
    "mm": "millimetre", "cm": "centimetre", "km": "kilometre", "kg": "kilogram", "mg": "milligram",
    "ml": "millilitre", "mL": "millilitre", "m": "metre", "g": "gram", "l": "litre", "L": "litre",
}
_SAFE_UNITS = "mm|cm|km|kg|mg|ml|mL"          # never a variable name
_ALL_UNITS = _SAFE_UNITS + "|m|g|l|L"

_OPS = "+−×÷="

_MEASURED_THINGS = ("poles?|pieces?|overlaps?|drop|strips?|gaps?|rods?|sticks?|lengths?|ropes?|ribbons?|bottles?|jugs?|"
                    "bags?|packets?|walk|race|track|squares?|cubes?|rulers?|tapes?|wires?|logs?|planks?|tiles?|steps?|"
                    "jumps?|marks?|sides?|cups?|glass|glasses|tins?|jars?|buckets?|weights?|parts?|sections?|"
                    "blocks?|bars?|borders?|paths?|margins?|laps?|stretch|journey|trip|intervals?|spacing|"
                    "towers?|edges?|width|height|doses?|walls?|candles?|models?|piles?|planks?|sheets?|cards?|"
                    "rectangles?|ladders?|trains?|bridges?|tunnels?|platforms?|roads?|fences?|tanks?|drums?|"
                    "packs?|boxes|box|weights?|loads?|servings?|portions?|spoons?|mugs?|coins?|notes?")


def _plural(word, one):
    return word if one else word + "s"


def _is_one(num):
    return num is not None and re.fullmatch(r"1(?:\.0+)?", num) is not None


def _units(s):
    # Speeds and other "per" units.
    s = re.sub(r"\bkm\s*/\s*(?:hr?|hour)\b", "kilometres per hour", s)
    s = re.sub(r"\bkmph\b", "kilometres per hour", s)
    s = re.sub(r"\bm\s*/\s*(?:s|sec)\b", "metres per second", s)
    s = re.sub(r"\bm\s*/\s*min\b", "metres per minute", s)
    s = re.sub(r"\bkm\s*/\s*(?:l|L|litre)\b", "kilometres per litre", s)
    s = re.sub(r"₹\s*/\s*kg\b", "rupees per kilogram", s)

    # Square and cubic units.
    s = re.sub(r"\bsq\.?\s*(?P<u>cm|mm|km|m)\b", lambda m: "square " + _UNIT_WORDS[m.group("u")] + "s", s)
    s = re.sub(r"\bsq\.?\s*units?\b", "square units", s)
    s = re.sub(r"\bcu\.?\s*(?P<u>cm|mm|m)\b", lambda m: "cubic " + _UNIT_WORDS[m.group("u")] + "s", s)
    s = re.sub(r"\b(?P<u>cm|mm|km|m)\s*²", lambda m: "square " + _UNIT_WORDS[m.group("u")] + "s", s)
    s = re.sub(r"\b(?P<u>cm|mm|km|m)\s*³", lambda m: "cubic " + _UNIT_WORDS[m.group("u")] + "s", s)

    # A unit after a number: singular after exactly 1.
    def after_number(m):
        num, unit = m.group("n"), m.group("u")
        return "%s %s" % (num, _plural(_UNIT_WORDS[unit], _is_one(num)))
    s = re.sub(r"(?<![\d.,])(?P<n>\d[\d,]*(?:\.\d+)?)\s?(?P<u>%s)\b(?!\s*[+−×÷(])" % _ALL_UNITS, after_number, s)

    # A unit after a word that means "one of them".
    s = re.sub(r"\b(?P<w>every|each|per|a|one|first|last|next|extra|another|whole) (?P<u>%s)\b" % _SAFE_UNITS,
               lambda m: "%s %s" % (m.group("w"), _UNIT_WORDS[m.group("u")]), s, flags=re.I)
    # Any other unambiguous unit (after a letter, a bracket, or a word).
    s = re.sub(r"\b(?P<u>%s)\b" % _SAFE_UNITS, lambda m: _UNIT_WORDS[m.group("u")] + "s", s)
    # Hours and minutes after a number.
    s = re.sub(r"(\d)\s?(?:hrs|hr)\b\.?", r"\1 hours", s)
    s = re.sub(r"(\d)\s?mins?\b\.?(?=\s|$|[,;:)])", r"\1 minutes", s)
    s = re.sub(r"(\d)\s?secs?\b\.?(?=\s|$|[,;:)])", r"\1 seconds", s)
    return s


_FRACTION_WORDS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters",
                   ("1", "3"): "one third", ("2", "3"): "two thirds"}


def _fractions(s):
    def mixed(m):
        frac = _FRACTION_WORDS.get((m.group(2), m.group(3)), "%s over %s" % (m.group(2), m.group(3)))
        return "%s and %s" % (m.group(1), frac)
    s = re.sub(r"(?<![\d/.,])(\d+) (\d+)/(\d+)(?![\d/])", mixed, s)

    def simple(m):
        return _FRACTION_WORDS.get((m.group(1), m.group(2)), "%s over %s" % (m.group(1), m.group(2)))
    s = re.sub(r"(?<![\d/.,])(\d+)/(\d+)(?![\d/])", simple, s)
    s = re.sub(r"\b([a-z])/(\d+)\b", r"\1 over \2", s)
    return s


def _caps(s):
    def fix(m):
        w = m.group(0)
        if w in _KEEP_CAPS:
            return w
        if w in _PLAIN_CAPS:
            return w.lower()
        if len(w) <= 4 or not w.strip("IVXLCDM"):
            return " ".join(w)
        return w.lower()
    return re.sub(r"\b[A-Z]{2,}\b", fix, s)


_UNIT_AFTER = re.compile(r"\s*(?:cm|km|mm|kg|ml|m\b|g\b|sq\b|rupees|years|°|%|centimetres|kilometres|metres)")


def _brackets(s):
    """Maths brackets are spoken; brackets that only set words aside become commas."""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "(":
            j = s.find(")", i)
            if j == -1 or "(" in s[i + 1:j]:
                out.append(" open bracket ")
                i += 1
                continue
            inner = s[i + 1:j]
            rest = s[j + 1:]
            before = s[:i].rstrip()
            words = re.findall(r"[A-Za-z]{3,}", inner)
            is_maths = bool(re.search(r"[+−×÷]", inner)) and not words and "=" not in inner and "," not in inner
            if is_maths:
                prev_char = before[-1] if before else ""
                multiplied = (i > 0 and s[i - 1] != " " and prev_char.isalnum()) or prev_char in "×÷+−="
                if _UNIT_AFTER.match(rest) and not multiplied:
                    out.append(inner)
                else:
                    prev = s[i - 1] if i else ""
                    prev2 = s[i - 2] if i > 1 else ""
                    if prev.isdigit() or (prev.islower() and not prev2.isalpha()):
                        out.append(" times")
                    out.append(" open bracket " + inner + " close bracket")
                    if re.match(r"\s*[+−×÷=]", rest):
                        out.append(",")
            else:
                lead = "" if (not before or before[-1] in ",:;.?!") else ","
                tail = "" if (not rest.strip() or rest.lstrip()[0] in ",:;.?!") else ","
                out.append(lead + " " + inner + tail)
            i = j + 1
            continue
        if c == ")":
            out.append(" close bracket ")
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _equals(s):
    """'=' is 'equals'; a second one in the same sentence is ', which equals'."""
    out = []
    seen = 0
    last = -1
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == "=":
            prefix = "".join(out).rstrip()
            if not prefix or prefix[-1] in ".:;?!":
                out.append(" That equals ")
            elif seen >= 1 and not _breaks(s[last + 1:i]):
                while out and out[-1] == " ":
                    out.pop()
                out.append(", which equals ")
            else:
                out.append(" equals ")
            seen += 1
            last = i
        else:
            if c in "?!;" or (c in ".:" and (i + 1 == n or s[i + 1] == " ")):
                seen = 0
            out.append(c)
        i += 1
    return "".join(out)


# Between two "=" signs, a comma or any ordinary word means a new equation has begun, not a chain.
_CHAIN_WORDS = {
    "degrees", "degree", "rupees", "rupee", "percent", "centimetres", "metres", "kilometres", "grams",
    "kilograms", "litres", "millilitres", "millimetres", "centimetre", "metre", "kilometre", "gram",
    "kilogram", "litre", "millilitre", "millimetre", "square", "cubic", "minutes", "hours", "seconds",
    "over", "one", "half", "quarter", "quarters", "third", "thirds", "two", "three", "squared", "cubed",
    "open", "close", "bracket", "times", "negative", "paise", "celsius", "of", "per", "hour", "blank",
}


def _breaks(between):
    if "," in between:
        return True
    return any(w.lower() not in _CHAIN_WORDS for w in re.findall(r"[A-Za-z]{2,}", between))


def say(text, ratio=False, option=False):
    s = (text or "").strip()
    if not s:
        return ""
    s = s.replace("\u00a0", " ")
    for k, v in {"½": " one half ", "¼": " one quarter ", "¾": " three quarters ", "⅓": " one third ", "⅔": " two thirds "}.items():
        s = s.replace(k, v)
    # "and so on" for trailing dots in a list.
    s = s.replace("…", "...")
    s = re.sub(r",\s*\.\.\.\s*,\s*(?=\d)", ", and so on, up to ", s)
    s = re.sub(r",?\s*\.\.\.\s*(?=[.?!]|$)", ", and so on", s)
    s = re.sub(r",?\s*\.\.\.\s+(?=[A-Z][a-z])", ", and so on. ", s)
    s = re.sub(r",?\s*\.\.\.\s*,?\s*", ", and so on, ", s)

    # Geometry marks.
    s = re.sub(r"∠\s*", "angle ", s)
    s = re.sub(r"[△Δ]\s*", "triangle ", s)

    # Clock times and ratios.
    s = re.sub(r"\b([ap])\.m\.(?=\s+[A-Z0-9]|\s*$)", r"\1 m.", s)
    s = re.sub(r"(?<=\d )([ap])\.?m\.?(?=[\s,;:)?!]|$)", r"\1 m", s)
    if option:
        s = re.sub(r"([ap]) m\.$", r"\1 m", s)
    # A digit named in the plural ("no more 5s"), and digits mixed with letters ("4P27Q").
    s = re.sub(r"(?<![A-Za-z\d.,])(\d{1,2})s\b", r"\1's", s)
    s = re.sub(r"\b(?=[\dA-Z]*\d)(?=[\dA-Z]*[A-Z])[\dA-Z]{2,}\b",
               lambda m: " ".join(re.findall(r"\d+|[A-Z]", m.group(0))), s)
    # Empty boxes between numbers.
    s = re.sub(r"(?<=\d) □ (?=\d)", ", □, ", s)
    if ratio:
        s = re.sub(r"(?<=\d)\s*:\s*(?=\d)", " is to ", s)
        s = re.sub(r"(?<=[\dA-Za-z)]) : (?=[\dA-Za-z(])", " is to ", s)
    else:
        # 9:33 is "9 33"; a time on the hour or just after (7:00, 8:05) keeps its colon,
        # which the voice reads as a time ("7 o'clock", "8 oh 5").
        s = re.sub(r"(?<![\d:])(\d{1,2}):([1-5]\d)(?!\d|:\d)", r"\1 \2", s)
        s = re.sub(r"(?<=\d) : (?=\d)", " is to ", s)

    # Money.
    s = re.sub(r"(?:₹|Rs\.?)\s*([\d,]*\d(?:\.\d+)?)(?:\s*/-)?", r"\1 rupees", s)
    s = re.sub(r"(?:₹|Rs\.?)\s*([a-z])\b", r"\1 rupees", s)
    s = re.sub(r"(?<![\d.,])1 rupees", "1 rupee", s)
    s = re.sub(r"(\d) rupees (?=(?:items?|notes?|coins?|stamps?|tickets?|pens?|pencils?|toys?|books?)\b)", r"\1 rupee ", s)
    # Percent, degrees, powers, roots.
    s = re.sub(r"\s*%", " percent", s)
    s = re.sub(r"(?<![\d.,])1\s*°\s*C\b", "1 degree Celsius", s)
    s = re.sub(r"\s*°\s*C\b", " degrees Celsius", s)
    s = re.sub(r"(?<![\d.,])1\s*°", "1 degree", s)
    s = re.sub(r"\s*°", " degrees", s)
    s = re.sub(r"(\d) degrees (angles?|turns?|gaps?)\b", r"\1 degree \2", s)
    s = _units(s)
    # "a 6 cm by 3 cm rectangle": the units describe the thing, so they are singular.
    s = re.sub(r"\b(an?|the|this|that) (\d[\d.]*) (\w+metre)s by (\d[\d.]*) (\w+metre)s (?=rectangle|sheet|card|field|room|garden|floor|grid|board|plot|tile|photo|page|park|hall|wall|lawn|strip|piece)",
               r"\1 \2 \3 by \4 \5 ", s)
    # "a 2 m pole", "50 cm pieces", "the 200 g drop": a measure used as a describing word is singular.
    s = re.sub(r"(\d) (\w*(?:metre|gram|litre))s (?=(?:%s)\b)" % _MEASURED_THINGS, r"\1 \2 ", s)
    s = re.sub(r"\s*²", " squared", s).replace("³", " cubed")
    s = re.sub(r"\s*\^\s*2\b", " squared", s)
    s = re.sub(r"\s*\^\s*3\b", " cubed", s)
    s = re.sub(r"\s*\^\s*(\d+)", r" to the power \1", s)
    s = s.replace("√", " the square root of ")
    s = _fractions(s)
    s = _caps(s)
    # A negative number in brackets: (−14) is "negative 14".
    s = re.sub(r"\(\s*−\s*(\d[\d,]*(?:\.\d+)?)\s*\)", r"negative \1", s)
    s = _brackets(s)

    # Algebra: 2n is "2 n".
    s = re.sub(r"(?<![A-Za-z\d.,])(\d[\d,]*(?:\.\d+)?)([a-z])(?![A-Za-z])", r"\1 \2", s)

    # Operations.
    s = re.sub(r"(?<=\d)\s*-\s*(?=\d)", " − ", s)
    s = re.sub(r"(?<=\s)-(?=\s)", "−", s)
    s = _equals(s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    s = s.replace("≠", " is not equal to ").replace("≤", " is less than or equal to ").replace("≥", " is greater than or equal to ")
    s = s.replace("<", " is less than ").replace(">", " is greater than ")
    s = s.replace("→", " gives ").replace("⇒", " so ")
    s = s.replace("□", " box ")       # these questions call the empty squares "boxes"

    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r",\s*([.?!:;])", r"\1", s)
    s = re.sub(r"([:;])\s*,", r"\1", s)
    if s and s[0].islower() and (text.strip()[:1] in "(=−-" or text.strip()[:1].isupper()) and not re.match(r"[a-z] ", s):
        s = s[0].upper() + s[1:]
    return s


def latex_to_plain(latex):
    """A step's maths line as plain print, or None when it is not simple enough to read by rule."""
    s = latex
    s = re.sub(r"\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r"\1/\2", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\%", "%").replace("\\,", " ").replace("\\;", " ")
    s = s.replace("^\\circ", "°").replace("^{\\circ}", "°").replace("\\circ", "°")
    s = re.sub(r"\\text\s*\{([^{}]*)\}", r" \1 ", s)
    s = s.replace("\\left", "").replace("\\right", "").replace("\\quad", " ").replace("\\ ", " ")
    s = s.replace("-", "−")
    if re.search(r"[\\{}_&]", s):
        return None
    return re.sub(r"\s+", " ", s).strip()
