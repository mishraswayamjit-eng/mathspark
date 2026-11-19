"""Rules that turn the printed text of gr4_time questions into speech (clock times, dates, calendars)."""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gr4_puzzles_rules as base  # noqa: E402

MONTHS = {"Jan": "January", "Feb": "February", "Mar": "March", "Apr": "April", "Jun": "June", "Jul": "July",
          "Aug": "August", "Sep": "September", "Sept": "September", "Oct": "October", "Nov": "November", "Dec": "December"}
DAYS = {"Mon": "Monday", "Tue": "Tuesday", "Tues": "Tuesday", "Wed": "Wednesday", "Thu": "Thursday", "Thur": "Thursday",
        "Thurs": "Thursday", "Fri": "Friday", "Sat": "Saturday", "Sun": "Sunday"}
MONTH_NAMES = "|".join(sorted(set(MONTHS.values()) | {"May"}))
DAY_NAMES = "|".join(sorted(set(DAYS.values())))
ROMAN = {"I": "one", "II": "two", "III": "three", "IV": "four", "V": "five", "VI": "six", "VII": "seven",
         "VIII": "eight", "IX": "nine", "X": "ten", "XI": "eleven", "XII": "twelve"}


def from_latex(latex):
    s = re.sub(r"\\xrightarrow\{([^{}]*)\}", r" \1 → ", latex)
    s = s.replace("{:}", ":")
    return base.from_latex(s)


def clock(m):
    h, mm = m.group(1), m.group(2)
    # On the hour, a single-digit minute or a leading zero: the voice reads 8:00, 2:05 and 09:45 well as printed.
    if mm[0] == "0" or (len(h) == 2 and h[0] == "0"):
        return "%s:%s" % (h, mm)
    return "%s %s" % (h, mm)


def meridiem(m):
    """'8:00 a.m.' is '8:00 a m'; the last dot is kept only where it also ends the sentence."""
    rest = m.string[m.end():]
    ends = m.group(2) and (re.match(r"\s+[A-Z]", rest) or (not rest and len(m.string) > 12))
    return " %s m%s" % (m.group(1), "." if ends else "")


def pre(s):
    # a.m. and p.m., however they are printed
    s = re.sub(r"(?<=\d)\s*([ap])\.m(\.?)(?![a-z])", meridiem, s)
    s = re.sub(r"(?<=\d)\s*([ap])m\b", r" \1 m", s)
    s = re.sub(r"(?<=\d)\s*([AP])M\b", lambda m: " %s m" % m.group(1).lower(), s)
    s = re.sub(r"\b([AP])M\b", lambda m: "%s m" % m.group(1).lower(), s)
    s = re.sub(r"\bpm\b", "p m", s)
    s = re.sub(r"\b(\d{1,2}):(\d{2})\b", clock, s)
    # short units of time
    s = re.sub(r"(?<=\d)\s*hrs?\b\.?", " hours", s)
    s = re.sub(r"\b1 hours\b", "1 hour", s)
    s = re.sub(r"(?<=\d)\s*mins?\b\.?(?!\w)", " minutes", s)
    s = re.sub(r"(?<=\d)\s*secs?\b\.?(?!\w)", " seconds", s)
    # months and weekdays printed short
    # (a dot after the short form is dropped only where the sentence clearly carries on)
    s = re.sub(r"\b(%s)\b(?:\.(?=\s+[a-z]))?(?=[\s,.:;()+=]|$)" % "|".join(MONTHS), lambda m: MONTHS[m.group(1)], s)
    s = re.sub(r"\b(%s)\b(?:\.(?=\s+[a-z]))?(?=[\s,.:;()+=]|$)" % "|".join(DAYS), lambda m: DAYS[m.group(1)], s)
    # 'Sep(25) + Oct(31)' and '29 (Oct) + 14 (Nov)': so many days in that month
    s = re.sub(r"\b(%s)\s*\((\d+)\)" % MONTH_NAMES, r"\2 in \1", s)
    s = re.sub(r"\b(\d+)\s*\((%s)\)" % MONTH_NAMES, r"\1 in \2", s)
    s = re.sub(r"(in (?:%s))\s*\+\s*" % MONTH_NAMES, r"\1, + ", s)
    # remainders, 'x' for times, '&'
    s = re.sub(r"(\d)\s*R\s*(\d)", r"\1 remainder \2", s)
    s = re.sub(r"(\d)\s+x\s+(\d)", r"\1 × \2", s)
    s = s.replace(" & ", " and ")
    s = re.sub(r"\b(IS|NO|OR)\b", lambda m: m.group(1).lower(), s)
    s = re.sub(r"(\bhas \d+ days) =", r"\1, which is", s)
    # clock faces with Roman numerals
    roman = "|".join(sorted(ROMAN, key=len, reverse=True))
    s = re.sub(r"\b(%s) to (%s)\b" % (roman, roman), lambda m: "%s to %s" % (ROMAN[m.group(1)], ROMAN[m.group(2)]), s)
    return s


def post(s):
    s = re.sub(r"\bequals (%s)\b" % DAY_NAMES, r"is \1", s)
    s = re.sub(r"\b((?:Those|[Ff]irst) \d+ days (?:of the month )?)is (%s)\b" % DAY_NAMES, r"\1are \2", s)
    # a date followed by a time: pause between them
    s = re.sub(r"\b(%s) (\d{1,2}[ :]\d{2} [ap] m)\b" % MONTH_NAMES, r"\1, \2", s)
    return s


def say(text):
    return base.say(text, pre, post)
