"""Narration for the imported measurement-speed questions (ids AIGEN_grade5_, IPMTB_grade5_, IPM2020_G5_).

These are one-off story problems about time, distance and speed. Each string goes through the
rules below unless a hand-written line exists for it (measurement_speed_imported_hand*.py).

A step that has a maths line is narrated as its text followed by that maths line, read aloud:
"Find the total distance. Total distance equals 3 plus 3, which is 6 kilometres."

Notation rules added here:
  - km/hr, m/s                 "kilometres per hour", "metres per second"
  - 7:00 AM, 12:15 PM          "7:00 a m", "12 15 p m"
  - hr, hrs, min, 15-min       "hour", "hours", "minutes", "15-minute"
  - 1/3 hour, 3/4 hr           "one third of an hour", "three quarters of an hour"
  - 90/60 (a division)         "90 divided by 60";  T/2  "T over 2"
  - A = B = C, once per clause "A equals B, which is C"
  - ≈                          "is about"
  - Time₁ (print), Time_1 (maths line)   "Time one", "Time 1"
  - (with the current)         ", with the current,"   (brackets that are only punctuation)
  - (12 − 8), 2(360 − d)       "open bracket, 12 minus 8, close bracket" (brackets that group a sum)
  - TOTAL TIME, NOT            said as ordinary words, so the voice does not spell them out
"""
import re

from common import number_tokens, source_strings
from measurement_speed_rules import units
from validate import check_string

IMPORTED_PREFIXES = ("AIGEN_grade5_", "IPMTB_grade5_", "IPM2020_G5_")

# Pictures and ticks that decorate a line and are not said.
_DECORATION = re.compile("[\u2300-\u23ff\u2600-\u27bf\ufe0f\U0001F000-\U0001FAFF]")
_SUBSCRIPT = {"₁": " one", "₂": " two", "₃": " three"}
_FRACTION_WORDS = {("1", "2"): "one half", ("1", "3"): "one third", ("2", "3"): "two thirds",
                   ("1", "4"): "one quarter", ("3", "4"): "three quarters"}
_SPELT = {"LCM": "L C M", "HCF": "H C F"}
# Names for the labelled times of a maths line: \text{Time}_{\text{return}}.
_NAMED_TIME = {"return": "Return time", "jog": "Jogging time", "walk": "Walking time",
               "boat": "Time for the boat", "Arjun": "Time for Arjun"}


def is_imported(q):
    return q["id"].startswith(IMPORTED_PREFIXES)


def _clock(m):
    hour, minutes, half = m.group(1), m.group(2), m.group(3)
    said = "%s:00" % hour if minutes == "00" else "%s %s" % (hour, minutes)
    return said + (" %s m" % half.lower() if half else "")


def _fraction(m):
    a, b, hour = m.group(1), m.group(2), m.group(3)
    proper = int(a) < int(b) and int(b) <= 10
    if hour:
        if (a, b) == ("1", "2"):
            return "half an hour"
        if proper:
            return "%s of an hour" % _FRACTION_WORDS.get((a, b), "%s over %s" % (a, b))
        return "%s over %s hours" % (a, b)
    if proper:
        return _FRACTION_WORDS.get((a, b), "%s over %s" % (a, b))
    return "%s divided by %s" % (a, b)


def _is_sum(inside):
    """True for brackets that group a sum, false for brackets that are only punctuation."""
    if re.search(r"[A-Za-z]{2,}", inside):
        return False
    return bool(re.search(r"[+−×÷/-]", inside))


def _forced_fraction(m):
    """A fraction the maths line means as a fraction (not a division): a⁄b."""
    a, b, hour = m.group(1), m.group(2), m.group(3)
    words = _FRACTION_WORDS.get((a, b), "%s over %s" % (a, b))
    if not hour:
        return words
    if (a, b) == ("1", "2"):
        return "half an hour"
    return "%s of an hour" % words if int(a) < int(b) else "%s over %s hours" % (a, b)


def _brackets(s):
    # "(10+20)÷2" is said "10 plus 20, all divided by 2"
    s = re.sub(r"\(\s*(\d+)\s*\+\s*(\d+)\s*\)\s*÷\s*(\d+)(\s*=)?",
               lambda m: "%s + %s, all divided by %s%s" % (m.group(1), m.group(2), m.group(3), ", =" if m.group(4) else ""), s)

    def one(m):
        inside = m.group(1).strip()
        if inside.startswith("="):
            return ", which is %s," % inside[1:].strip()
        if not _is_sum(inside):
            return ", %s," % inside
        if not re.search(r"[+−-]", inside):
            return " %s " % inside            # one product or one fraction: the brackets change nothing
        return " ⟦ %s ⟧ " % inside            # said as open bracket, close bracket, after the sums are done
    return re.sub(r"\s*\(([^()]*)\)", one, s)


_INLINE_SUM = re.compile(
    r"\b(?:is|are|covers|covered|after|in|by|arrives|taking|traveled|travelled)\s+"
    r"[\d.]+(?:\s*(?:[×÷+−]|divided by)\s*[\d.]+)+\s*$")


def _equals(s):
    """'=' is 'equals' the first time in a clause, then ', which is'."""
    out = []
    for piece in re.split(r"((?<=[.,;:!?])\s+)", s):
        seen = [0]

        def eq(m):
            seen[0] += 1
            about = "≈" in m.group(0)
            # "Deepa covers 8 × 0.5 = 4 km": the sum sits inside a sentence, so its result is ", which is"
            inline = _INLINE_SUM.search(piece[:m.start()])
            if seen[0] == 1 and not inline and not piece.lstrip().startswith(m.group(0).strip()):
                return " is about " if about else " equals "
            return ", which is about " if about else ", which is "

        out.append(re.sub(r"\s*[=≈]\s*", eq, piece))
    return "".join(out)


def say(text):
    """One printed string as spoken words."""
    s = (text or "").strip()
    if not s:
        return ""
    s = _DECORATION.sub("", s)
    s = re.sub(r"\s*\n\s*", " ", s)
    for k, v in _SUBSCRIPT.items():
        s = s.replace(k, v)
    s = re.sub(r"\s+[—–]\s+", ", ", s)
    s = s.replace("vs.", "versus").replace("i.e.,", "that is,")
    s = re.sub(r"~\s*(?=\d)", "about ", s)
    s = re.sub(r"\b(\d{1,2}):(\d{2})(?:\s*([AP])M\b)?", _clock, s)
    s = re.sub(r"\b[A-Z]{2,}\b", lambda m: _SPELT.get(m.group(0), m.group(0).lower()), s)
    s = re.sub(r"\bAvg\b", "Average", s)
    s = re.sub(r"\b(Let (?:the )?[A-Za-z' ]+?)\s*=\s*", r"\1 be ", s)
    s = _brackets(s)
    s = re.sub(r"\bkm per hour\b", "kilometres per hour", s, flags=re.I)
    s = re.sub(r"(\d) km (gap|head start|part|distance)\b", r"\1-kilometre \2", s)
    s = re.sub(r"(\d) m (circular|track)\b", r"\1-metre \2", s)
    s = units(s)
    s = re.sub(r"(?<![\d.,])1 kilometres per hour", "1 kilometre per hour", s)
    s = re.sub(r"(\d)-min\b", r"\1-minute", s)
    s = re.sub(r"\bmeter(s?)\b", r"metre\1", s)
    s = re.sub(r"(\d+)⁄(\d+)(\s*(?:hr|hour)s?\b)?", _forced_fraction, s)
    s = re.sub(r"(\d+)\s*/\s*(\d+)(\s*(?:hr|hour)s?\b)?", _fraction, s)
    s = re.sub(r"\b(\d*)([A-Za-z])\s*/\s*(\d+)", lambda m: ("%s %s over %s" % m.groups()).strip(), s)
    s = re.sub(r"\bhrs\b", "hours", s)
    s = re.sub(r"\bhr\b", "hour", s)
    s = re.sub(r"\bmin\b", "minutes", s)
    s = re.sub(r"(\d)([A-Za-z])\b", r"\1 \2", s)
    s = re.sub(r"(\d)\s*⟦", r"\1 times ⟦", s)
    s = _equals(s)
    s = s.replace("≈", " is about ").replace("×", " times ").replace("÷", " divided by ")
    s = s.replace("+", " plus ").replace("−", " minus ")
    s = s.replace("⟦", ", open bracket, ").replace("⟧", ", close bracket, ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([.,?!:;])", r"\1", s)
    s = re.sub(r",(?=[.,?!:;])", "", s)
    s = re.sub(r"([!?])\.", r"\1", s)
    s = re.sub(r"^[,\s]+", "", s).rstrip(", ")
    if s and s[-1] not in ".?!:":
        s += "."
    return s[:1].upper() + s[1:] if len(s) > 1 and s[1] != " " else s


def say_option(text):
    return say(text).rstrip(".")


_FRAC = re.compile(r"\\frac\{([^{}]*)\}\{([^{}]*)\}")


def _frac(m):
    a, b = m.group(1).strip(), m.group(2).strip()
    number = r"^\d+(?:\.\d+)?$"
    if re.match(number, a) and re.match(number, b):
        before, after = m.string[:m.start()].rstrip(), m.string[m.end():].lstrip()
        as_fraction = (before.endswith(("×", "+", "{")) or after.startswith("+")
                       or re.match(r"(?:hr|hour)s?\b", after))
        if "." in a or "." in b or not as_fraction:
            return " %s ÷ %s " % (a, b)
        return " %s⁄%s " % (a, b)
    if re.search(r"\s[-+]\s", a):
        return " %s, all over %s, " % (a, b)
    if re.search(r"[A-Za-z]{2,}", a) or "⁄" in b or re.match(number, a):
        return " %s ÷ %s " % (a, b)
    return " %s over %s " % (a, b)


def say_maths(tex):
    """A step's maths line (LaTeX) as spoken words."""
    s = tex.replace("\\!", "").replace("{:}", ":")
    s = re.sub(r"\\text\{Time\}_\{\\text\{(\w+)\}\}", lambda m: _NAMED_TIME.get(m.group(1), "Time for " + m.group(1)), s)
    s = re.sub(r"([A-Za-z])_\{\\text\{(\w+)\}\}", r"\1 \2", s)
    s = re.sub(r"_\{(\d)\}", r" \1", s)
    s = re.sub(r"_(\d)", r" \1", s)
    s = re.sub(r"\\text\{([^{}]*)\}", r" \1 ", s)
    s = s.replace("\\quad", " ").replace("\\checkmark", " ")
    s = s.replace("\\times", " × ").replace("\\approx", " ≈ ").replace("\\implies", ", so ")
    while _FRAC.search(s):
        s = _FRAC.sub(_frac, s)
    s = re.sub(r"(?<![A-Za-z])-\s*(?=[\dA-Za-z(])", "− ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return say(s)


def _already_worked(text, tex):
    """True when the step's text already shows the sum its maths line repeats."""
    if "=" not in text or text.rstrip().endswith(":"):
        return False
    result = number_tokens(re.sub(r"\\[a-zA-Z]+", " ", tex))
    return bool(result) and result[-1] in number_tokens(text)


def narrate(q, hand=None):
    """The entry for one imported question. `hand` holds hand-written lines:
    {"q": str, "options": {index: str}, "hints": {index: str}, "steps": {index: str}}."""
    hand = hand or {}
    src = source_strings(q)
    own = q.get("stepByStep") or []
    steps = []
    for i, text in enumerate(src["steps"]):
        if i in hand.get("steps", {}):
            steps.append(hand["steps"][i])
            continue
        spoken = say(text)
        tex = own[i].get("latex", "") if i < len(own) else ""
        if tex.strip() and text.strip() and not _already_worked(text, tex):
            both = "%s %s" % (spoken, say_maths(tex))
            also = "%s %s" % (text, re.sub(r"\\[a-zA-Z]+", " ", tex))
            if not check_string(both, text, "", also):
                spoken = both
        steps.append(spoken)
    return {
        "q": hand.get("q") or say(src["q"]),
        "options": [hand.get("options", {}).get(i) or say_option(o) for i, o in enumerate(src["options"])],
        "hints": [hand.get("hints", {}).get(i) or say(h) for i, h in enumerate(src["hints"])],
        "steps": steps,
    }
