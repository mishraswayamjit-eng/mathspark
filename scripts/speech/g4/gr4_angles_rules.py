"""Rules that turn printed Grade 4 geometry text (angles, clocks, compass turns) into speakable words.

Used by gr4_angles.py. say() is for prose and inline working; maths_line() is for a step's
separate maths line; narrate() builds one entry from hand-written slots first, rules second.
"""
import re

import common

# One term of a sum: 180°, 67.5, 2x, x°, 67½°.
_TERM = r"(?:\d[\d.]*½?x?°?|x°?)"
_EXPR = _TERM + r"(?:\s*[+−×÷]\s*" + _TERM + r")*"
# After these words a sum is being described, so its result reads ", which is".
_WHICH = {"is", "are", "be", "turns", "turned", "leave", "make", "makes", "share", "has", "give", "gives", "it's", "of", "than", "to", "area", "each"}
# After the result of such a sum, these words carry the sentence on, so a comma closes the aside.
_JOIN = "and|so|to|from|with|in|each|more|past|for|before|after|plus|too|on|at|or|but|equally"


def _time(m):
    hour, minutes, half = m.group(1), m.group(2), m.group(3)
    if minutes == "00":
        said = "%s:00" % hour          # the voice reads this as "o'clock"; the checker needs the 0
    elif minutes[0] == "0":
        said = "%s oh %s" % (hour, minutes[1])
    else:
        said = "%s %s" % (hour, minutes)
    if half:
        said += " " + half.strip().lower().replace(".", "")[0] + " m"
    return said


def _equals(s):
    """Each '=' becomes 'equals', or ', which is' where the sum sits inside a sentence or continues a chain."""
    parts = re.split(r"\s*=\s*", s)
    if len(parts) == 1:
        return s
    out = parts[0]
    if not out.strip():
        out = "That"
    for i, nxt in enumerate(parts[1:]):
        before = parts[i].strip()
        m = re.search(r"(?:([A-Za-z']+)\s+)" + "(?:" + _EXPR + ")$", before)
        chain = i >= 1 and re.fullmatch(_EXPR, before)
        if nxt.strip().startswith("?"):
            nxt = re.sub(r"^\s*\?", "what?", nxt)
        inside = m and m.group(1).lower() in _WHICH and re.search(r"\d", m.group(0).split(None, 1)[1])
        if inside and re.search(r"\bwhich is\s+" + "(?:" + _EXPR + ")$", before):
            inside = False      # "which is 4 × 30° = 120°": one "which is" is enough
        if re.search(r"\d°,\s+\d[\d.]*°\s+and\s+(?:" + _EXPR + ")$", before):
            inside = True       # the last of a list of angles: "40°, 40° and 180 − 40 − 40 = 100°"
        if chain or inside:
            # Close the aside with a comma: after the unit if there is one, or before a joining word.
            nxt = re.sub(r"^(" + _EXPR + r"\s+(?:square )?(?:centimetres?|metres?))(\s+[a-z])", r"\1,\2", nxt)
            nxt = re.sub(r"^(" + _EXPR + r")(?![\d.°x])(\s+(?:" + _JOIN + r")\b)", r"\1,\2", nxt)
            out += ", which is " + nxt
        else:
            out += " equals " + nxt
    return out


def say(text, sentence=True):
    """Printed text in, speakable words out."""
    s = (text or "").strip()
    if not s:
        return ""
    s = s.replace("✓", "").replace("→", " gives ").replace("≈", " is about ")
    # The filler lines of the past-paper questions.
    s = re.sub(r"^Correct answer: Option (\d) — (?=[A-Z][a-z]+ [a-z])", r"The correct answer is option \1. ", s)
    s = re.sub(r"^Correct answer: Option (\d) — (.*)$", r"The correct answer is option \1, which is \2", s)
    s = re.sub(r"\s*\(Q(\d+)\)", r", question \1", s)
    s = re.sub(r"\bIPM\b", "I P M", s)
    # Labelled working: "Answer: 125°", "Other = 180° − 89°", "Vertically opposite angle = 22°".
    s = re.sub(r"^Answer: (?=\d)", "The answer is ", s)
    s = re.sub(r"^Other = ", "The other angle is ", s)
    s = re.sub(r"^(Vertically opposite angle|Third angle|Angle|Sum|Missing angle|Remaining angle) = ",
               lambda m: "The %s is " % m.group(1).lower(), s)
    # Shouted words are only emphasis in print.
    s = re.sub(r"\b[A-Z]{4,}\b", lambda m: m.group(0).lower(), s)
    s = re.sub(r"\b(?:NOT|AND|ARE|ALL|ANY|NO)\b", lambda m: m.group(0).lower(), s)
    # Clock times, before anything else touches the colon.
    s = re.sub(r"\b(\d{1,2}):(\d{2})\b(\s*(?:[ap]\.m\.|[ap]m\b))?", _time, s)
    s = re.sub(r"\b(\d{1,2})\s*([ap])\.m\.(?=\s+[A-Z])", r"\1 \2 m.", s)
    s = re.sub(r"\b(\d{1,2})\s*([ap])\.m\.", r"\1 \2 m", s)
    s = re.sub(r"\b(\d{1,2})\s*([ap])m\b", r"\1 \2 m", s)
    # Ratios: 2:3.
    s = re.sub(r"\b(\d+):(?!00\b)(\d+)\b", r"\1 is to \2", s)
    # Named angles and rays: AOB, OC.
    s = re.sub(r"\b([A-Z])O([A-Z])\b", r"\1 O \2", s)
    s = re.sub(r"\bO([A-Z])\b", r"O \1", s)
    s = re.sub(r"\b([A-Z])([A-Z])([A-Z])\b(?= is| =|\.|,| and| must| could|\?)", r"\1 \2 \3", s)
    s = re.sub(r"∠\s*", "angle ", s)
    s = re.sub(r"[△Δ]\s*", "triangle ", s)
    s = re.sub(r"\bclock-wise\b", "clockwise", s)
    s = re.sub(r"\banticlock-wise\b", "anticlockwise", s)
    # A minus written with a hyphen.
    s = re.sub(r"(\d°?)\s+-\s+(?=\d)", r"\1 − ", s)
    s = re.sub(r"(^|(?<=\s))-(?=\d)", "minus ", s)
    s = _equals(s)
    # Mixed numbers and halves. A half degree on its own: "the ½°", "take away ½°".
    s = re.sub(r"\b(the|extra) ½°", r"\1 half degree", s)
    s = re.sub(r"(?<![\d ])½°|(?<=[a-z] )½°", "half a degree", s)
    s = re.sub(r"(\d)\s*½", r"\1 and a half", s)
    s = re.sub(r"(\d+) 1/4\b", r"\1 and one quarter", s)
    s = re.sub(r"(\d+) 3/4\b", r"\1 and three quarters", s)
    s = re.sub(r"(\d+) 1/2\b", r"\1 and a half", s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)", r"\1 over \2", s)
    # Degrees. "a 90° clockwise turn" and "the 45° steps" describe, so the word stays singular.
    s = re.sub(r"\b([Aa]n?) (\d+)° (?=[a-z])", r"\1 \2 degree ", s)
    s = re.sub(r"(\d)° (?=steps?\b|turns?\b|angles?\b)", r"\1 degree ", s)
    s = re.sub(r"(?<![\d.])1°", "1 degree", s)
    s = re.sub(r"([\dxyz])\s*°", r"\1 degrees", s)
    s = re.sub(r"(half|quarter|quarters)°", r"\1 degrees", s)
    # Algebra: 2x is "2 x".
    s = re.sub(r"(\d)([xyz])\b", r"\1 \2", s)
    s = re.sub(r"\bcm\b", "centimetres", s)
    s = s.replace("&", " and ").replace("—", ", ")
    s = re.sub(r"([.?!])\s*\(([^()]*)\)", r"\1 \2", s)       # a whole sentence in brackets
    s = re.sub(r"\s*\(([^()]*)\)", r", \1,", s)
    s = s.replace("×", " times ").replace("÷", " divided by ").replace("+", " plus ").replace("−", " minus ")
    s = re.sub(r"_{2,}", "blank", s)
    s = re.sub(r"\s+", " ", s).strip()
    # "2 + 3 = 5 is less than 7": the result is then compared.
    s = re.sub(r"(equals \d[\d.]*) is (?=more|less|only|not|greater|smaller|bigger|exactly|equal|the same)", r"\1, which is ", s)
    # A list printed without spaces: "70°,60°,40°".
    s = re.sub(r"([a-z]),(?=\S)", r"\1, ", s)
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",+([.?!:;])", r"\1", s)
    s = re.sub(r",\s*,", ",", s)
    s = s.rstrip(",")
    if sentence and s and s[-1] not in ".?!:":
        s += "."
    return s


def bracket_first(s):
    """'(50 - 12) ÷ 2 = 19' is said in the order it is worked: '50 minus 12, then divided by 2, equals 19'."""
    m = re.fullmatch(r"\s*\(([\d.°\s+-]+)\)\s*([÷×])\s*([\d.°]+)\s*=\s*([\d.°]+)\s*", s)
    if not m:
        return s
    return "%s, then %s %s, = %s" % (m.group(1).strip(), "divided by" if m.group(2) == "÷" else "times",
                                     m.group(3), m.group(4))


def maths_line(latex):
    """A step's maths line as speech, or None where it does not read as a plain sum."""
    s = latex
    if "boxed" in s:
        return None
    s = s.replace("^\\circ", "°").replace("\\div", "÷").replace("\\times", "×")
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1 over \2", s)
    s = s.replace("\\text{ and }", ", and ")
    s = bracket_first(s)
    if re.search(r"[\\{}?()<>]", s) or not re.search(r"[=+×÷-]", s):
        return None
    s = s.replace("-", "−")
    s = re.sub(r"(×\s*\d[\d.]*°?)\s*([+−])", r"\1, \2", s)   # "4 × 30, plus 15"
    s = re.sub(r"(, [+−]\s*\d[\d.]*°?)\s*=", r"\1, =", s)
    return say(s)


def _subsequence(small, big):
    it = iter(big)
    return all(x in it for x in small)


def narrate(q, hand, counts, used, say=say, maths_line=maths_line):
    """One entry: hand-written slots ("<id>:q", ":o0", ":h1", ":s2") first, rules for the rest."""
    src = common.source_strings(q)
    own = q.get("stepByStep") or []

    def line(text, slot, sentence=True, latex=None):
        if not text.strip():
            return ""
        key = "%s:%s" % (q["id"], slot)
        if key in hand:
            used.add(key)
            counts["hand"] += 1
            return hand[key]
        counts["rule"] += 1
        spoken = say(text, sentence)
        extra = maths_line(latex) if latex else None
        if extra:
            # Read the maths line too, unless the text has already said that working.
            repeat = "=" in text and _subsequence(common.number_tokens(extra), common.number_tokens(text))
            allowed = common.number_tokens("%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", latex)))
            both = "%s %s" % (spoken, extra)
            if not repeat and common.number_tokens(both) == allowed and len(both) <= 700:
                spoken = both
            elif not repeat:
                counts.setdefault("dropped", []).append(key)   # the checker would not accept the maths line
        return spoken

    return {
        "q": line(src["q"], "q"),
        "options": [line(t, "o%d" % i, sentence=False) for i, t in enumerate(src["options"])],
        "hints": [line(t, "h%d" % i) for i, t in enumerate(src["hints"])],
        "steps": [line(t, "s%d" % i, latex=own[i].get("latex") if i < len(own) else None)
                  for i, t in enumerate(src["steps"])],
    }
