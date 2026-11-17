"""Rules for the imported Grade 5 geometry questions (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

These are one-off word problems and textbook items, written as prose with a lot of notation:
degrees, "sq. m", rupees, brackets, arrows, bullet lists, and a separate maths line on most steps.

    say_imported(text)            printed text in, speakable words out
    maths_line(latex)             a step's maths line as printed-style text, or None if it cannot be read
"""
import re

IMPORTED_PREFIXES = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")

_KEEP_CAPS = {"NE", "NW", "SE", "SW", "HCF", "LCM", "IPM"}
_COMPASS = {"NE": "North-East", "NW": "North-West", "SE": "South-East", "SW": "South-West"}
_COMPASS1 = {"N": "North", "E": "East", "S": "South", "W": "West"}
_NUM = r"(\d+(?:,\d+)*(?:\.\d+)?)"


def _lower_caps(m):
    w = m.group(0)
    if w in _KEEP_CAPS:
        return w
    before = m.string[:m.start()].rstrip()
    if not before or before[-1] in ".?!:":
        return w.capitalize()
    return w.lower()


def _lines(s):
    """Line breaks and bullets become sentences."""
    out = []
    for line in s.split("\n"):
        line = line.strip()
        line = re.sub(r"^[•→]\s*", "", line)
        if not line:
            continue
        if line.startswith("="):
            line = "That is " + line[1:].strip()
        if out and re.match(r"[a-z]{2,}", line):
            line = line[0].upper() + line[1:]
        out.append(line)
    for i in range(len(out) - 1):
        if out[i][-1] not in ".?!:;,":
            out[i] += "."
    return " ".join(out)


def _arrows(s):
    """An arrow is 'so' in working, 'then' in a count (9 → 10 → 11), nothing at the start of a sentence."""
    if "→" not in s:
        return s
    parts = s.split("→")
    out = parts[0]
    for i in range(1, len(parts)):
        left = re.split(r"[.?!:,]\s", parts[i - 1].strip())[-1].strip()
        right = re.split(r"[.?!:,]\s", parts[i].strip())[0].strip().rstrip(".")
        prev = out.rstrip()
        if not prev or prev[-1] in ".?!:":
            out = prev + " " + parts[i].lstrip()
        elif len(left) <= 12 and len(right) <= 12 and "=" not in left and "=" not in right and not re.search(r"[×÷+−]", left + right):
            out = prev + ", then " + parts[i].lstrip()
        else:
            out = prev + ", so " + parts[i].lstrip()
    return out


def _unit(word):
    def sub(m):
        return "%s %s" % (m.group(1), word[:-1] if m.group(1) == "1" else word)
    return sub


def _units(s):
    # The full stop of a textbook abbreviation in mid-sentence ("16 cm. then", "3.2 cm., 4.6 cm. and").
    s = re.sub(r"\b(cm|mm|km|m)\.(?=\s+[a-z&]|\s*[,;?)])", r"\1", s)
    s = re.sub(r"\bsq\.?\s*(cm|mm|km|m)\.(?=\s*$)", r"sq. \1", s)
    for ab, word in (("cm", "centimetres"), ("mm", "millimetres"), ("km", "kilometres"), ("m", "metres")):
        s = re.sub(_NUM + r"\s*(?:sq\.?\s*%s\b|%s²)" % (ab, ab), _unit("square " + word), s)
        s = re.sub(r"\bsq\.?\s*%s\b|\b%s²" % (ab, ab), "square " + word, s)
        s = re.sub(_NUM + r"\s*%s\b" % ab, _unit(word), s)
    s = re.sub(r"\bsq\.?\s*(metres?|meters?|centimetres?|units?)\b", r"square \1", s)
    s = re.sub(r"\bcm\b", "centimetres", s)
    s = re.sub(r"\bmm\b", "millimetres", s)
    s = re.sub(r"\b(to|in|into|from) m\b", r"\1 metres", s)
    s = re.sub(r"\bper (square )?(metre|centimetre|millimetre|kilometre)s\b", r"per \1\2", s)
    return s


def _fractions(s):
    s = re.sub(r"(\d)\s*½", r"\1 and a half", s)
    s = re.sub(r"(\d)\s*¼", r"\1 and a quarter", s)
    s = re.sub(r"(\d)\s*¾", r"\1 and three quarters", s)
    s = re.sub(r"(\d)\s*⅓", r"\1 and one third", s)
    s = re.sub(r"(\d)\s*⅔", r"\1 and two thirds", s)
    s = re.sub(r"\b(\d+) 1/3(?!\d)", r"\1 and one third", s)
    s = re.sub(r"\b(\d+) 2/3(?!\d)", r"\1 and two thirds", s)
    s = re.sub(r"½\s*°", "half a degree", s)
    s = re.sub(r"½\s*×\s*", "half of ", s)
    s = s.replace("½", "half")
    s = re.sub(r"\b(\d+) 1/2(?!\d)", r"\1 and a half", s)
    s = re.sub(r"\b(\d+) 1/4(?!\d)", r"\1 and a quarter", s)
    s = re.sub(r"\b(\d+) 3/4(?!\d)", r"\1 and three quarters", s)
    s = re.sub(r"\b(\d+) (\d+)/(\d+)(?!\d)", r"\1 and \2 over \3", s)
    s = re.sub(r"(?<![\d/.])1/2\s*°", "half a degree", s)
    s = re.sub(r"(?<![\d/.])1/2(?![\d/])", "one half", s)
    s = re.sub(r"(?<![\d/.])1/4(?![\d/])", "one quarter", s)
    s = re.sub(r"(?<![\d/.])3/4(?![\d/])", "three quarters", s)
    return s


def _equals(s):
    """A chain of equals signs: the first is 'equals', the rest ', which is'. A new sentence or clause starts a new chain."""
    out = []
    first = True
    clause = ""
    pos = 0
    mixed = r"(?!\d+ over|a half|a quarter|three quarters|one third|two thirds)"
    for m in re.finditer(r"([.?!:;,]\s|\s\(|\swhere\s|\sand\s" + mixed + r"(?=\d|[A-Za-z ]{1,30}=))|\s*=\s*", s):
        piece = s[pos:m.start()]
        pos = m.end()
        out.append(piece)
        clause += piece
        if m.group(1):
            out.append(m.group(1))
            first = True
            clause = ""
            continue
        if not first:
            word = ", which is "
        elif re.match(r"\s*(?:Is|is|Are|are)\s+\d", clause):
            # "is 15² + 20² = 25²?"
            word = " equal to "
        elif re.search(r"\b(?:has|have)\s+(?:(?:the|an?|its|each)\s+)?(?:[a-z]+\s+){0,5}[a-z]+$", clause) or re.search(
                r"\bwith\s+(?:(?:the|an?|its|each)\s+)?(?:largest |smallest |third |equal )?(?:angle|side|sides|base|height|length|breadth|width|area|perimeter)$", clause):
            # "the outer square has side = 29 m"
            word = " equal to "
        elif re.search(r"\b(?:is|are|was|be|(?<![Hh]alf )of|subtract|add|needs?|covers|becomes|represents)\s+\d[^=]*[×÷+−][^=]*$", clause):
            # "the angle next to it is 180° − 50° = 130°"
            word = ", which is "
        else:
            word = " equals "
        first = False
        clause += word
        out.append(word)
    out.append(s[pos:])
    return "".join(out)


def _degree_runs(s):
    """'180 degrees minus 45 degrees minus 65 degrees' gets a breath before each operation."""
    term = r"\d[\d.]*(?: and (?:a half|a quarter|three quarters))? degrees"

    def run(m):
        return re.sub(r" (plus|minus) ", r", \1 ", m.group(0))
    return re.sub(r"%s(?: (?:plus|minus) %s){2,}" % (term, term), run, s)


def say_imported(text, sentence=True, maths=False):
    s = (text or "").strip()
    if not s:
        return ""
    # Layout and decoration.
    s = s.replace("**", "").replace("*", "").replace("⏰", "").replace('"', "").replace("“", "").replace("”", "")
    s = _lines(s)
    s = re.sub(r"(?<![A-Za-z])['‘]([^'‘’]+)['’](?![A-Za-z])", r"\1", s)
    s = re.sub(r"_{2,}", "blank", s)
    s = re.sub(r"\s+—\s+", ", ", s)
    s = s.replace("&", "and")
    s = re.sub(r"\b[A-Z]{2,}(?:'[A-Z]+)?\b", _lower_caps, s)
    # Compass points: NE is North-East; single letters only in a line that is plainly about the compass.
    if re.search(r"\b(?:NE|NW|SE|SW)\b", s):
        s = re.sub(r"\b([NESW])\b(?=\s*(?:,|→|\.|$))", lambda m: _COMPASS1[m.group(1)], s)
    s = re.sub(r"\b(NE|NW|SE|SW)\b", lambda m: _COMPASS[m.group(1)], s)
    s = _arrows(s)
    s = re.sub(r"\s+-\s+", " − ", s)
    s = re.sub(r"\b(\d)-(\d)-(\d)\b", r"\1, \2, \3", s)
    # Option letters used as labels: "D) None of these", "(B)".
    s = re.sub(r"\(([A-D])\)", r"\1", s)
    s = re.sub(r"\b([A-D])\)\s", r"\1, ", s)
    # Money, percent, ratio.
    s = re.sub(r"(?:₹|Rs\.?)\s*" + _NUM, _unit("rupees"), s)
    s = re.sub(_NUM + r"\s*Rs\b\.?", _unit("rupees"), s)
    s = re.sub(r"(\d)\s*%", r"\1 percent", s)
    s = re.sub(r"(\d):(?=\d)", r"\1 is to ", s)
    s = re.sub(r"(\d)\s+:\s*(?=\d)", r"\1 is to ", s)
    s = _fractions(s)
    s = _units(s)
    # Squares and roots.
    s = s.replace("²", " squared")
    s = re.sub(r"√\s*", "the square root of ", s)
    # Algebra: 3x is "3 x"; 2(3b + b) is 2 times the bracket.
    s = re.sub(r"(\d)([a-z])(?![a-z])", r"\1 \2", s)
    s = re.sub(r"(\d)\s*\((?=[^()]*[×÷+−])", r"\1 × (", s)
    s = re.sub(r"(\d)\((\d+)\)", r"\1 × \2", s)
    # Angles and degrees.
    s = re.sub(r"∠\s*([A-Z]{1,3})\b", lambda m: "angle " + " ".join(m.group(1)), s)
    s = s.replace("∠", "angle ")
    s = re.sub(r"\(([^()]*)\)\s*°", r"\1°", s)
    s = re.sub(r"(?<![\d.,])1\s*°", "1 degree", s)
    s = re.sub(r"\s*°\s*/\s*(\d)", r" degrees ÷ \1", s)
    s = re.sub(r"\s*°", " degrees", s)
    # "Let breadth = b" is "Let breadth be b".
    s = re.sub(r"\b([Ll]et (?:the |each )?[a-z ]{1,24}?)\s*=\s*", r"\1 be ", s)
    # Questions in working: "180° − 72° =?"
    s = re.sub(r"=\s*\?", "= what?", s)
    # A product inside a longer sum gets a breath after it.
    s = re.sub(r"(\d\s*×\s*\d+(?:\.\d+)?)\s*([+−])", r"\1, \2", s)
    # A bracket after an operation: the pause goes before the operation, not after it.
    # (\x01 is a comma that does not start a new chain of equals signs.)
    s = re.sub(r"=\s*\(([^()]*[×÷+−][^()]*)\)", "= \\1\x01", s)
    s = re.sub(r"\s*([+−])\s*\(([^()]*)\)", r", \1 \2,", s)
    s = re.sub(r"([),\x01])\s*([×÷])\s*\(([^()]*)\)", r"\1, \2 \3,", s)
    s = _equals(s).replace("\x01", ",")
    # "4 + 4 = 8 > 7" is "4 plus 4 equals 8, which is greater than 7".
    s = re.sub(r"(equals|which is) (\d[\d.]*)\s*>", r"\1 \2, which is greater than", s)
    s = re.sub(r"(equals|which is) (\d[\d.]*)\s*<", r"\1 \2, which is less than", s)
    s = re.sub(r"\b(equals|is|be|are)\s+\(([^()]*)\)", r"\1 \2,", s)
    # Brackets: around working they become pauses; around words they become commas too.
    s = re.sub(r"\s*\(\s*", ", ", s)
    s = re.sub(r"\s*\)", ",", s)
    # Comparisons and operations.
    s = s.replace("≠", " is not equal to ").replace("≥", " is greater than or equal to ").replace("≤", " is less than or equal to ")
    s = s.replace("≈", " is about ").replace("<", " is less than ").replace(">", " is greater than ")
    s = re.sub(r"(metres|centimetres|millimetres)\s*×\s*(\d[\d.]* (?:metres|centimetres|millimetres))(?! equals|, which)", r"\1 by \2", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    s = s.replace("/", " over ")
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ")
    s = re.sub(r"\s*[−–]\s*", " minus ", s)
    s = _degree_runs(s)
    # Tidy.
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r"([:;]),", r"\1", s)
    s = re.sub(r",(?:\s*,)+", ",", s)
    s = re.sub(r",([.?!:;])", r"\1", s)
    s = re.sub(r"([.?!]),\s*", r"\1 ", s)
    s = re.sub(r"([?!])\.", r"\1", s)
    s = re.sub(r"^,\s*", "", s).strip()
    s = s.rstrip(",").strip()
    # "the 72 degrees angle" is "the 72 degree angle"; "a 2 metres wide path" is "a 2 metre wide path".
    s = re.sub(r"(\d) degrees (angle|turn)\b", r"\1 degree \2", s)
    # "Is 50° < 90°?" is "Is 50 degrees less than 90 degrees?"
    s = re.sub(r"\b(Is|is|Are|are) (\d[\d.]*(?: degrees)?(?: plus \d[\d.]*)?) is (less|greater) than\b", r"\1 \2 \3 than", s)
    s = re.sub(r"(\d) (centimetre|metre)s (and \d[\d.]* )(centimetre|metre)s (sides|sticks)\b", r"\1 \2 \3\4 \5", s)
    s = re.sub(r"(\d) (centimetre|metre)s (side|sides|stick|sticks|border|piece|pieces|strip)\b", r"\1 \2 \3", s)
    s = re.sub(r"(^|[.;:,] )((?:[A-Z][a-z]+ )?(?:[Aa]ngles|[Ss]ides)) equals\b", r"\1\2 are", s)
    s = re.sub(r"((?:equals|which is) [^,.;:?!]*?) (is (?:greater|less) than|is about)\b", r"\1, which \2", s)
    # A lost tick mark leaves a remark stuck to the working: "equals 40 centimetres Perfect, it matches".
    s = re.sub(r"(\d(?: (?:degrees|centimetres|metres|square \w+))?) (Perfect|They're|Yes|Supplementary|Valid|Not|not supplementary)\b", r"\1. \2", s)
    s = re.sub(r"\. not supplementary", ". Not supplementary", s)
    s = re.sub(r"\bvs\.?(?= )", "versus", s)
    s = re.sub(r"\bi\.e\.,?", "that is,", s)
    s = re.sub(r"([.?!] )half\b", r"\1Half", s)
    s = re.sub(r"\b(Does|does) ([^?.!]*?) equals\b", r"\1 \2 equal", s)
    s = re.sub(r"\b(and|or),", r"\1", s)
    s = re.sub(r"\b([Aa]n?) (\d[\d.]*) (metre|centimetre)s (wide|long|tall|high|thick) (?=[a-z])", r"\1 \2 \3 \4 ", s)
    s = re.sub(r"\b([Aa]n?) (\d[\d.]*) (metre|centimetre)s by (\d[\d.]*) (metre|centimetre)s (?=[a-z])", r"\1 \2 \3 by \4 \5 ", s)
    if s and s[0].islower() and sentence and not re.match(r"[b-z]\b", s) and not (maths and re.match(r"a\b", s)):
        s = s[0].upper() + s[1:]
    if sentence and s and s[-1] not in ".?!:":
        s += "."
    return s


def maths_line(latex):
    """A step's maths line, turned back into printed-style text for say_imported. None if it cannot be read."""
    s = (latex or "").strip()
    if not s:
        return None
    # The checker reads "3{,}915" in a maths line as 3 then 915, so it is said as "3 thousand 915".
    # (A round thousand, "6{,}000", cannot be said that way; such a line is left unread.)
    def thousand(m):
        if len(m.group(2)) > 2 or int(m.group(3)) == 0:
            return m.group(0)
        said = "%s thousand %d" % (m.group(2), int(m.group(3)))
        return said + " rupees" if m.group(1) else said
    s = re.sub(r"(₹\s*)?(?<![\d}])(\d+)\{,\}(\d{3})(?!\{,\}|\d)", thousand, s)
    s = s.replace("{,}", ",")
    s = re.sub(r"\\(?:quad|qquad|;|,|!|:| )", " ", s)
    s = re.sub(r"\bs_\{?(\d)\}?", r"side \1", s)
    s = s.replace("\\checkmark", "")
    # Labels with a subscript: Area_floor is "floor area", Angle_1 is "Angle 1".
    s = re.sub(r"\\text\{\s*(\w+)\s*\}_\{\\text\{\s*(\w+)\s*\}\}", lambda m: "%s %s" % (m.group(2).capitalize(), m.group(1).lower()), s)
    s = re.sub(r"\\text\{\s*(\w+)\s*\}_\{?(\d)\}?", r"\1 \2", s)
    s = re.sub(r"\\angle\s*_\{?(\d)\}?", r"angle \1", s)
    s = re.sub(r"\\text\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\^\s*\{\s*\\circ\s*\}", "°", s)
    s = re.sub(r"\^\s*\\circ", "°", s)
    s = re.sub(r"\^\s*\{?2\}?", "²", s)
    # Fractions: a mixed number, a half, a small proper fraction, or a division.
    s = re.sub(r"(\d)\s*\\t?frac\{(\d+)\}\{(\d+)\}", r"\1 \2/\3", s)

    def frac(m):
        a, b = m.group(1).strip(), m.group(2).strip()
        if (a, b) == ("1", "2"):
            return "½ "
        if re.fullmatch(r"\d", a) and re.fullmatch(r"\d", b):
            return "%s/%s" % (a, b)
        if re.search(r"[+\-−×]", a):
            return "%s, ÷ %s" % (a, b)
        return "%s ÷ %s" % (a, b)
    for _ in range(2):
        s = re.sub(r"\\t?frac\{([^{}]*)\}\{([^{}]*)\}", frac, s)
    s = re.sub(r"\\sqrt\{([^{}]*)\}", r"√\1", s)
    s = s.replace("\\times", "×").replace("\\div", "÷").replace("\\cdot", "×")
    s = re.sub(r"\\(?:implies|Rightarrow|rightarrow|to)\b", "→", s)
    s = s.replace("\\approx", "≈").replace("\\neq", "≠").replace("\\ne ", "≠ ")
    s = re.sub(r"\\angle\s*", "∠", s)
    s = s.replace("\\%", "%")
    if re.search(r"[\\{}^_]", s):
        return None
    # The keyboard hyphen is a minus sign in a maths line.
    s = re.sub(r"\s+-\s+", " − ", s)
    s = re.sub(r"(?<=[\d°)²])-(?=[\d(])", " − ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s or None
