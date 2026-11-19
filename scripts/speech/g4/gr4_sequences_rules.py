"""Rules that turn printed Grade 4 sequence questions into words for the voice. Used by gr4_sequences.py.

    from gr4_sequences_rules import say
    say("10th term: 24,39,53,66,78,...?")  ->  "10th term: 24, 39, 53, 66, 78, and so on?"

The notation of this topic is handled here (lists of numbers, trailing dots, blanks), and the
rest is left to the algebra rules, which already say operators, brackets, letters and units.
"""
import re

from gr4_algebra_rules import say as say_algebra, maths_line  # noqa: F401  (maths_line is re-exported)

DOTS = r"\s*,?\s*\.{3,}\s*"

NOTES = [
    (r"\bSo next (difference|term|number|numerator) = ", r"So the next \1 is "),
    (r"\bNext (difference|term|number|numerator) = ", r"The next \1 is "),
    (r"\bNext = ", "The next one is "),
    (r"\bCommon difference = ", "The common difference is "),
    (r"\bMissing (number|digit|count) = ", r"The missing \1 is "),
    (r"\bMissing = ", "The missing number is "),
]


def prepare(text):
    s = (text or "").replace("…", "...")
    # A list printed without spaces: 64,81,100  ->  64, 81, 100 (never one big number).
    s = re.sub(r"(?<=\d),(?=[\dA-Za-z?.])", ", ", s)
    # Dots that stand for "the pattern carries on".
    s = re.sub(DOTS + r",?\s*(\d+)(?= [a-z])", r", and so on, up to \1,", s)
    s = re.sub(DOTS + r",?\s*(?=\d)", ", and so on, up to ", s)
    s = re.sub(DOTS + r"(?=\?|$)", ", and so on", s)
    s = re.sub(DOTS + r"(?=[A-Z])", ", and so on. ", s)
    s = re.sub(DOTS + r",?\s*", ", and so on, ", s)
    # Places to be filled in.
    s = re.sub(r"_{2,}", "blank", s)
    s = s.replace("★", "star")
    s = re.sub(r"(?<=, )[?*](?=\s*[,.]|\s*$)", "blank", s)
    s = re.sub(r"\bAP\b", "A P", s)
    # Notes-style working: "Next term = 19 + 4 = 23" is read as a sentence.
    for pattern, words in NOTES:
        s = re.sub(pattern, words, s)
    # A mixed number: 3 1/5 is "3 and 1 over 5".
    s = re.sub(r"\b(\d+) (\d+)/(\d+)\b", r"\1 and \2/\3", s)
    s = re.sub(r"\b1 km\b", "1 kilometre", s)
    return s


def say(text, sentence=True):
    if not (text or "").strip():
        return ""
    return say_algebra(prepare(text), sentence)
