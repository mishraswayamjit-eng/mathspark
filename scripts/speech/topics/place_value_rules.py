"""Narration rules for the generated place-value families (BOOST_, VAR_, PH3_ ids).

Every generated string must match a rule here or already be plain speakable words;
anything else raises, so nothing reaches the voice through a blind fallback.
"""
import re

N = r"(\d[\d,]*(?:\.\d+)?)"

# (pattern on the whole string, spoken template). Tried in order; first match wins.
RULES = [
    # ── questions ──
    (r"In the number N, the place value of N \(in ([a-z-]+) place\) is how many times the place value of N \(in ([a-z-]+) place\)\?",
     r"In the number \1, the place value of \2, in the \3 place, is how many times the place value of \4, in the \5 place?"),
    (r"Find the sum of first N (odd|even|natural) numbers\.", r"Find the sum of the first \1 \2 numbers."),

    # ── place value of one digit ──
    (r"Place value = digit × value of its position\.", r"Place value equals the digit, times the value of its position."),
    (r"The ([a-z-]+) place has value N\.", r"The \1 place has a value of \2."),
    (r"Place value = N × N = N", r"Place value equals \1 times \2, which is \3."),
    (r"The digit N is in the ([a-z-]+) place\.", r"The digit \1 is in the \2 place."),

    # ── how many times one place value is of another ──
    (r"Ratio = N ÷ N = N", r"The ratio is \1 divided by \2, which is \3."),

    # ── digit sums ──
    (r"Digits of N: ([\d +]+) = N", None),  # handled in code: needs the plus signs spoken

    # ── counting multiples in a range ──
    (r"First: N, Last: N\.", r"The first is \1, and the last is \2."),
    (r"Count = \(last − first\) ÷ N \+ 1\.", r"The count is last minus first, divided by \1, plus 1."),
    (r"Use the formula: \(last − first\) ÷ 2 \+ 1\.", r"Use the formula: last minus first, divided by 2, plus 1."),
    (r"First multiple of N ≥ N: N", r"The first multiple of \1, from \2 onwards, is \3."),
    (r"Last multiple of N ≤ N: N", r"The last multiple of \1, up to \2, is \3."),
    (r"Count = \(N\s*−\s*N\)\s*÷\s*N \+ 1 = N", r"The count is \1 minus \2, divided by \3, plus 1. That equals \4."),

    # ── counting odd and even numbers in a range ──
    (r"First (odd|even) in range is N, last is N\.", r"The first \1 number in the range is \2, and the last is \3."),
    (r"First (odd|even): N, Last (?:odd|even): N", r"The first \1 number is \2, and the last \1 number is \3."),

    # ── how many n-digit numbers ──
    (r"Total count = largest − smallest \+ 1 = N\.", r"The total count is largest minus smallest, plus 1, which is \1."),
    (r"Smallest N-digit: N, Largest: N", r"The smallest \1-digit number is \2, and the largest is \3."),
    (r"Total N-digit = N\. All = N", r"The total of \1-digit numbers is \2. So all of them make \3."),
    (r"Total N-digit = N\. (Even|Odd) = N", None),  # handled in code: lower-case the word

    # ── digits used to number the pages of a book ──
    (r"Pages 1-9 use 1 digit each, 10-99 use 2 digits each, 100\+ use 3 digits each\.",
     r"Pages 1 to 9 use 1 digit each, pages 10 to 99 use 2 digits each, and pages from 100 onwards use 3 digits each."),
    (r"Pages N-N: N pages × N digits? = N digits", r"Pages \1 to \2: that is \3 pages, times \4 digit, which is \5 digits."),
    (r"Pages N-N: 1 pages × N digits = N", r"Pages \1 to \2: that is 1 page, times \3 digits, which is \4."),
    (r"Pages N-N: N pages × N digits = N", r"Pages \1 to \2: that is \3 pages, times \4 digits, which is \5."),
    (r"Total = N digits", r"The total is \1 digits."),

    # ── sums of the first n numbers ──
    (r"There's a formula for the sum of first N (odd|even|natural) numbers\.",
     r"There's a formula for the sum of the first \1 \2 numbers."),
    (r"For odd: n² = N²\.", r"For odd numbers, it is n squared, which is \1 squared."),
    (r"For even: n\(n\+1\) = N×N\.", r"For even numbers, it is n, times n plus 1, which is \1 times \2."),
    (r"For natural: n\(n\+1\)/2 = N×N/2\.",
     r"For natural numbers, it is n, times n plus 1, divided by 2. That is \1 times \2, divided by 2."),
    (r"Formula for sum of first N odd numbers: n² = N²",
     r"The formula for the sum of the first \1 odd numbers is n squared, which is \2 squared."),
    (r"Formula for sum of first N even numbers: n\(n\+1\) = N×N",
     r"The formula for the sum of the first \1 even numbers is n, times n plus 1, which is \2 times \3."),
    (r"Formula for sum of first N natural numbers: n\(n\+1\)/2 = N×N/2",
     r"The formula for the sum of the first \1 natural numbers is n, times n plus 1, divided by 2. That is \2 times \3, divided by 2."),
    (r"= N", r"That equals \1."),

    # ── options ──
    (r"-N", r"minus \1"),
]

_COMPILED = [(re.compile("^" + pat.replace("N", N) + "$"), tpl) for pat, tpl in RULES]
_PLAIN = re.compile(r"^[A-Za-z0-9 .,?'’:-]+$")
_PV_PAIR = re.compile(r"^PV of (\d) = (\d+), PV of (\d) = (\d+)$")
_Q_PAIR = re.compile(r"\(in ([a-z-]+) place\).*\(in ([a-z-]+) place\)")


def say(text, question=""):
    """Spoken form of one generated string. `question` is the printed question it belongs to."""
    s = (text or "").strip()
    if not s:
        return ""
    m = _PV_PAIR.match(s)
    if m:
        # "PV of 8 = 80000, PV of 5 = 500": name the places, taken from the question, so that
        # two equal digits are not confused by ear.
        places = _Q_PAIR.search(question)
        if not places:
            raise ValueError("no places in question for: " + s)
        return "The place value of %s, in the %s place, is %s. The place value of %s, in the %s place, is %s." % (
            m.group(1), places.group(1), m.group(2), m.group(3), places.group(2), m.group(4))
    for rx, tpl in _COMPILED:
        m = rx.match(s)
        if not m:
            continue
        if tpl is not None:
            return m.expand(tpl)
        if s.startswith("Digits of"):
            return "The digits of %s add up like this: %s equals %s." % (
                m.group(1), m.group(2).strip().replace(" + ", " plus "), m.group(3))
        if s.startswith("Total"):
            return "The total of %s-digit numbers is %s. The %s ones are %s." % (
                m.group(1), m.group(2), m.group(3).lower(), m.group(4))
    if _PLAIN.match(s) and not re.search(r"\d\s*-\s*\d", s):
        return s
    raise ValueError("no narration rule for generated string: %r" % s)
