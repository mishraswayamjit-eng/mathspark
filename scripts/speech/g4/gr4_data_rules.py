"""Rules that turn the printed text of gr4_data questions into speech (tables, lists, graphs in words)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr4_puzzles_rules as base  # noqa: E402

from_latex = base.from_latex

DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Tues": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Thur": "Thursday",
        "Thurs": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}
DAY_NAMES = "|".join(sorted(set(DAYS.values())))
UNITS = {"cm": "centimetre", "mm": "millimetre", "km": "kilometre", "kg": "kilogram", "ml": "millilitre"}
WORD_FRACTIONS = {("1", "2"): "one half", ("1", "4"): "one quarter", ("3", "4"): "three quarters"}


def unit(m):
    number, name = m.group(1), UNITS[m.group(2)]
    return "%s %s%s" % (number, name, "" if number == "1" else "s")


def missing(m):
    """'Missing = 232 − (71 + 56 + 72) = 232 − 199 = 33' in two short sentences."""
    return "The missing number equals %s − the total of %s. That is %s − %s, which is %s" % (
        m.group(1), m.group(2).strip(), m.group(3), m.group(4), m.group(5))


def pre(s):
    s = re.sub(r"^Missing = (\d+) − \(([\d +]+)\) = (\d+) − (\d+) = (\d+)", missing, s)
    s = re.sub(r"(\d+(?:\.\d+)?)\s*(%s)\b" % "|".join(UNITS), unit, s)
    # weekdays printed short, and 'Mon=12' in a table read as 'Monday 12'
    s = re.sub(r"\b(%s)\b(?:\.(?=\s+[a-z]))?(?=[\s,.:;()+=]|$)" % "|".join(DAYS), lambda m: DAYS[m.group(1)], s)
    s = re.sub(r"\b(%s)\s*=\s*(?=\d)" % DAY_NAMES, r"\1 ", s)
    # 'Match 1 34, Match 2 52': keep the label and its value apart
    s = re.sub(r"\b(Match|Game|Day|Test|Week|Round) (\d+) (\d+)\b", r"\1 \2: \3", s)
    s = re.sub(r"(\d)\s+x\s+(\d)", r"\1 × \2", s)
    s = re.sub(r"\b(\d)/(\d)\b", lambda m: WORD_FRACTIONS.get((m.group(1), m.group(2)), m.group(0)), s)
    return s


def post(s):
    return s


def say(text):
    return base.say(text, pre, post)
