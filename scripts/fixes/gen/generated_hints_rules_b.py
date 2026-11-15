"""Hint rules for the hcf_lcm, percentage, perimeter_area and simple_interest families.

Same contract as generated_hints_rules_a.py.
"""
import math
from fractions import Fraction

from generated_hints_common import Example, Skip, factors, fmt, lcm, nums, plural


# ── HCF and LCM ──────────────────────────────────────────────────────────────

def hcf(m, n):
    m, n = int(m), int(n)
    if m == n or min(m, n) < 2:
        raise Skip("HCF of equal or tiny numbers")
    h1 = ("HCF means Highest Common Factor: the biggest number that divides both %d and %d exactly, "
          "with nothing left over." % (m, n))
    h2 = ("Write down every number that divides %d exactly. These are its factors, and they come in pairs: "
          "1 × %d is one pair. Do the same for %d. Then look for the biggest number that is on both lists."
          % (m, m, n))
    cands = []
    for a, b in ((8, 12), (6, 15), (10, 15), (6, 8), (9, 21), (8, 20), (10, 25), (6, 14), (4, 10), (9, 15), (10, 14)):
        g = math.gcd(a, b)
        cands.append(Example(
            "Try another one: the HCF of %d and %d. Factors of %d: %s. Factors of %d: %s. "
            "The biggest number on both lists is %d, so the HCF is %d."
            % (a, b, a, ", ".join(map(str, factors(a))), b, ", ".join(map(str, factors(b))), g, g), (a, b, g)))
    return {"answer": Fraction(math.gcd(m, n)), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(m, n)}


def lcm_rule(m, n):
    m, n = int(m), int(n)
    small, big = min(m, n), max(m, n)
    answer = lcm(m, n)
    steps = answer // big
    if small < 2 or steps < 2:
        raise Skip("LCM is one of the two numbers")
    h1 = ("LCM means Lowest Common Multiple: the smallest number that is in both the %d times table "
          "and the %d times table." % (m, n))
    if steps >= 3:
        start = "Count up in %ds: %d, %d, and keep going." % (big, big, 2 * big)
    else:
        start = "Count up in %ds, starting with %d itself." % (big, big)
    h2 = "%s Each time, ask: is this number in the %d times table too? The first one that is, is the LCM." % (start, small)
    cands = []
    # Every example pair shares a factor, so that no example suggests "just multiply the two numbers".
    for a, b in ((4, 6), (6, 8), (4, 10), (6, 9), (6, 10), (8, 12), (10, 15), (9, 12), (6, 15), (4, 14)):
        l = lcm(a, b)
        cands.append(Example(
            "Try another one: the LCM of %d and %d. Count up in %ds: %s. The first one that is also in the "
            "%d times table is %d, because %d × %d = %d. So the LCM of %d and %d is %d."
            % (a, b, b, ", ".join(str(b * i) for i in range(1, l // b + 1)), a, l, a, l // a, l, a, b, l), (a, b, l)))
    return {"answer": Fraction(answer), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(m, n),
            "variant": "third multiple or later" if steps >= 3 else "second multiple"}


# ── Percentage: p% of n ──────────────────────────────────────────────────────

_CONTEXT = {
    "girls": {
        "h1": "Per cent means 'out of every 100'. So %(p)d%% girls means %(p)d girls in every 100 students.",
        "h1_hundred": "Per cent means 'out of every 100'. Now look at how many students there are in this question. That makes it a quick one.",
        "hundred": "There are exactly 100 students here. %(p)d%% means %(p)d out of every 100. So how many of these 100 students are girls?",
        "half": "50%% is the same as one half. So half of the %(n)d students are girls. What is half of %(n)d?",
        "quarter": "25%% is the same as one quarter. So share the %(n)d students into 4 equal groups. One group is the girls.",
        "tenth": "10%% is the same as one tenth. So share the %(n)d students into 10 equal groups. One group is the girls.",
        "lots": "%(n)d students is %(k)d lots of 100 students. Each lot of 100 has %(p)d girls. So how many girls are in %(k)d lots?",
    },
    "marks": {
        "h1": "Per cent means 'out of every 100'. So scoring %(p)d%% means getting %(p)d marks for every 100 marks in the test.",
        "h1_hundred": "Per cent means 'out of every 100'. Now look at how many marks the test has. That makes it a quick one.",
        "hundred": "This test has exactly 100 marks. %(p)d%% means %(p)d out of every 100. So how many of these 100 marks did the student score?",
        "half": "50%% is the same as one half. So the student scored half of the %(n)d marks. What is half of %(n)d?",
        "quarter": "25%% is the same as one quarter. So share the %(n)d marks into 4 equal parts. The student scored one part.",
        "tenth": "10%% is the same as one tenth. So share the %(n)d marks into 10 equal parts. The student scored one part.",
        "lots": "%(n)d marks is %(k)d lots of 100 marks. The student gets %(p)d marks from each lot. So how many marks come from %(k)d lots?",
    },
    "plain": {
        "h1": "Per cent means 'out of every 100'. So %(p)d%% of a number means %(p)d for every 100 in it.",
        "h1_hundred": "Per cent means 'out of every 100'. Now look at the number you are finding the per cent of. That makes it a quick one.",
        "hundred": "The number here is exactly 100. %(p)d%% means %(p)d out of every 100. So how much is that out of this 100?",
        "half": "50%% is the same as one half. So you need half of %(n)d.",
        "quarter": "25%% is the same as one quarter. So share %(n)d into 4 equal parts and take one part.",
        "tenth": "10%% is the same as one tenth. So share %(n)d into 10 equal parts and take one part.",
        "lots": "%(n)d is %(k)d lots of 100. Each lot of 100 gives %(p)d. So how much do %(k)d lots give?",
    },
}
_TENS = "First find 10%% of %(n)d by dividing %(n)d by 10. Then %(p)d%% is %(t)d lots of that."


def _percent_examples(method):
    out = []
    if method == "hundred":
        for p in (30, 40, 20, 60, 70, 35, 45):
            out.append(Example(
                "Try another one: %d%% of 100 is %d, because %d%% means %d out of every 100. "
                "Any per cent of 100 works the same way." % (p, p, p, p), (p,)))
    elif method == "half":
        for n in (80, 60, 40, 120, 20, 140):
            out.append(Example("Try another one: 50%% of %d. 50%% is one half, and half of %d is %d. So 50%% of %d is %d."
                               % (n, n, n // 2, n, n // 2), (n, n // 2)))
    elif method == "quarter":
        for n in (80, 40, 120, 20, 60, 160):
            out.append(Example("Try another one: 25%% of %d. 25%% is one quarter, and %d ÷ 4 = %d. So 25%% of %d is %d."
                               % (n, n, n // 4, n, n // 4), (n, n // 4)))
    elif method == "tenth":
        for n in (70, 90, 50, 30, 80, 40):
            out.append(Example("Try another one: 10%% of %d. 10%% is one tenth, and %d ÷ 10 = %d. So 10%% of %d is %d."
                               % (n, n, n // 10, n, n // 10), (n, n // 10)))
    elif method == "lots":
        for p in (30, 20, 40, 10, 60, 35, 45):
            for n in (200, 300, 400):
                k = n // 100
                out.append(Example(
                    "Try another one: %d%% of %d. %d is %d lots of 100, and each lot gives %d. "
                    "%d × %d = %d, so %d%% of %d is %d." % (p, n, n, k, p, k, p, k * p, p, n, k * p), (p, n, k * p)))
    elif method == "tens":
        for p in (30, 20, 40, 60, 70):
            for n in (70, 60, 90, 80, 30):
                t, tenth = p // 10, n // 10
                if t == tenth:
                    continue
                out.append(Example(
                    "Try another one: %d%% of %d. 10%% of %d is %d ÷ 10 = %d. %d%% is %d lots of that, "
                    "and %d × %d = %d. So %d%% of %d is %d."
                    % (p, n, n, n, tenth, p, t, t, tenth, t * tenth, p, n, t * tenth), (p, n, t * tenth)))
    return out


def _percent(context, p, n):
    p, n = int(p), int(n)
    if not 0 < p < 100 or (p * n) % 100:
        raise Skip("percentage does not come to a whole number")
    words = _CONTEXT[context]
    values = {"p": p, "n": n, "k": n // 100, "t": p // 10}
    qnums = nums(p, n)
    # When the answer is itself 100, no hint may show "100": the idea is spelled out in words instead,
    # and the "lots of 100" method gives way to the "10% first" method.
    answer_is_100 = p * n == 10000 and n != 100
    if n == 100:
        method = "hundred"
    elif p == 50:
        method, qnums = "half", nums(n)
    elif p == 25 and n % 4 == 0:
        method, qnums = "quarter", nums(n)
    elif p == 10:
        method, qnums = "tenth", nums(n)
    elif n % 100 == 0 and not answer_is_100:
        method = "lots"
    elif p % 10 == 0 and n % 10 == 0:
        method = "tens"
    else:
        raise Skip("no child-friendly method for this percentage")
    h1 = words["h1_hundred" if method == "hundred" else "h1"] % values
    if answer_is_100:
        h1 = h1.replace("100", "hundred")
    h2 = (_TENS if method == "tens" else words[method]) % values
    return {"answer": Fraction(p * n, 100), "h1": h1, "h2": h2,
            "cands": _percent_examples(method), "qnums": qnums, "variant": method}


def percent_girls(n, p):
    return _percent("girls", p, n)


def percent_marks(n, p):
    return _percent("marks", p, n)


def percent_plain(p, n):
    return _percent("plain", p, n)


# ── Perimeter and area ───────────────────────────────────────────────────────

def _split(x, y):
    """A hint for a harder multiplication x × y, splitting whichever number is two-digit. '' if not needed."""
    for which, v in (("x", x), ("y", y)) if x >= y else (("y", y), ("x", x)):
        if v >= 11 and v % 10:
            tens, ones = v - v % 10, v % 10
            if which == "x":
                return " To make it easier, split %d into %d and %d: %d × %d = %d × %d + %d × %d." % (
                    v, tens, ones, x, y, tens, y, ones, y)
            return " To make it easier, split %d into %d and %d: %d × %d = %d × %d + %d × %d." % (
                v, tens, ones, x, y, x, tens, x, ones)
    return ""


def triangle_area(b, h):
    b, h = int(b), int(h)
    h1 = ("A triangle is half of a rectangle that has the same base and height. "
          "So its area is half of base × height.")
    h2 = "First multiply the base by the height: %d × %d.%s Then find half of that number." % (
        b, h, "" if 10 in (b, h) else _split(b, h))
    odd = (b * h) % 2 == 1
    pairs = ((3, 5), (5, 7), (3, 7), (5, 9), (3, 9), (7, 9), (1, 5)) if odd else ((6, 4), (4, 3), (8, 5), (10, 3), (6, 5), (4, 7), (2, 9))
    cands = []
    for eb, eh in pairs:
        area = fmt(Fraction(eb * eh, 2))
        cands.append(Example(
            "Try another one: a triangle with base %d cm and height %d cm. %d × %d = %d, and half of %d is %s. "
            "So its area is %s sq. cm." % (eb, eh, eb, eh, eb * eh, eb * eh, area, area),
            (eb, eh, eb * eh, Fraction(eb * eh, 2))))
    return {"answer": Fraction(b * h, 2), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(b, h),
            "variant": "answer ends in .5" if odd else "whole-number answer"}


def rectangle_perimeter(l, b):
    l, b = int(l), int(b)
    h1 = ("Perimeter is the distance all the way round a shape. A rectangle has 2 lengths and 2 breadths, "
          "and you go along every one of them.")
    h2 = ("Add one length and one breadth: %d + %d. That takes you halfway round. "
          "Then double it to go all the way round." % (l, b))
    cands = []
    for el, eb in ((5, 3), (6, 4), (7, 2), (8, 3), (9, 4), (10, 5), (6, 1), (9, 2), (8, 5)):
        cands.append(Example(
            "Try another one: a rectangle with length %d cm and breadth %d cm. %d + %d = %d, and %d × 2 = %d. "
            "So its perimeter is %d cm." % (el, eb, el, eb, el + eb, el + eb, 2 * (el + eb), 2 * (el + eb)),
            (el, eb, el + eb, 2 * (el + eb))))
    return {"answer": Fraction(2 * (l + b)), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(l, b)}


def rectangle_area(l, b):
    l, b = int(l), int(b)
    h1 = ("Area is the amount of flat space inside a shape. Picture the rectangle filled with small squares, "
          "each 1 cm wide: %s, with %d squares in each row." % (plural(b, "row"), l))
    h2 = "To count all the squares, multiply the length by the breadth: %d × %d." % (l, b)
    if 10 in (l, b):
        h2 += " A quick way to multiply a whole number by 10 is to write a 0 on the end of it."
    else:
        h2 += _split(l, b) or " You can also count up in %ds, once for each of the %s." % (l, plural(b, "row"))
    cands = []
    for el, eb in ((5, 3), (6, 4), (7, 2), (8, 3), (9, 2), (6, 5), (4, 3), (8, 5), (9, 4)):
        cands.append(Example(
            "Try another one: a rectangle with length %d cm and breadth %d cm. %d × %d = %d, "
            "so its area is %d sq. cm." % (el, eb, el, eb, el * eb, el * eb), (el, eb, el * eb)))
    return {"answer": Fraction(l * b), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(l, b),
            "variant": "times 10" if 10 in (l, b) else "split a two-digit number" if _split(l, b) else "small numbers"}


def square_perimeter(s):
    s = int(s)
    h1 = ("Perimeter is the distance all the way round a shape. A square has 4 sides, "
          "and they are all the same length.")
    h2 = "Each of the 4 sides is %d cm. So add %d four times, or work out 4 × %d." % (s, s, s)
    cands = []
    for e in (3, 5, 8, 2, 9, 12, 15):
        cands.append(Example("Try another one: a square with side %d cm. 4 × %d = %d, so its perimeter is %d cm."
                             % (e, e, 4 * e, 4 * e), (e, 4 * e)))
    return {"answer": Fraction(4 * s), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(s)}


def square_area(s):
    s = int(s)
    h1 = ("Area is the amount of flat space inside a shape. A square's length and breadth are the same, "
          "so picture %d rows with %d small squares in each row." % (s, s))
    h2 = ("Multiply the side by itself: %d × %d. Take care not to work out %d × 4: that is the perimeter, "
          "the distance round the outside." % (s, s, s))
    h2 += _split(s, s)
    cands = []
    for e in (3, 5, 6, 8, 2, 12):
        cands.append(Example("Try another one: a square with side %d cm. %d × %d = %d, so its area is %d sq. cm."
                             % (e, e, e, e * e, e * e), (e, e * e)))
    return {"answer": Fraction(s * s), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(s),
            "variant": "split a two-digit number" if _split(s, s) else "small numbers"}


# ── Simple interest ──────────────────────────────────────────────────────────

def _interest(p, r, t, amount):
    p, r, t = int(p), int(r), int(t)
    if p % 100 or p < 200 or t < 1:
        raise Skip("principal is not a whole number of hundreds")
    hundreds = p // 100
    interest = hundreds * r * t
    if amount:
        h1 = ("The amount is the money at the start plus the interest it earns. "
              "%d%% simple interest means every Rs.100 earns Rs.%d each year." % (r, r))
        h2 = ("Find the interest for 1 year first: Rs.%d is %d hundreds, and each hundred earns Rs.%d. "
              "Multiply by %d for the %s. Then add that interest to the Rs.%d you started with."
              % (p, hundreds, r, t, plural(t, "year"), p))
    else:
        h1 = ("Simple interest is the extra money that a sum of money earns. %d%% per annum means "
              "every Rs.100 earns Rs.%d each year, and it earns the same again every year." % (r, r))
        h2 = ("First find the interest for 1 year: Rs.%d is %d hundreds, and each hundred earns Rs.%d. "
              "Then multiply that 1-year interest by %d for the %s." % (p, hundreds, r, t, plural(t, "year")))
    cands = []
    for ep in (200, 300, 400):
        for er in (5, 4, 3, 2, 6):
            for et in (3, 2, 4):
                eh = ep // 100
                if len({eh, er, et}) < 3:
                    continue
                year, total = eh * er, eh * er * et
                text = ("Try another one: Rs.%d at %d%% for %d years. Rs.%d is %d hundreds, so 1 year earns "
                        "%d × %d = %d rupees. %d years earn %d × %d = %d rupees. "
                        % (ep, er, et, ep, eh, eh, er, year, et, et, year, total))
                if amount:
                    text += "Add the money at the start: %d + %d = %d. So the amount is Rs.%d." % (ep, total, ep + total, ep + total)
                    key = (ep, er, et, total, ep + total)
                else:
                    text += "So the simple interest is Rs.%d." % total
                    key = (ep, er, et, total)
                cands.append(Example(text, key))
    return {"answer": Fraction(p + interest if amount else interest), "h1": h1, "h2": h2, "cands": cands,
            "qnums": nums(p, r, t)}


def simple_interest(p, r, t):
    return _interest(p, r, t, False)


def amount(p, r, t):
    return _interest(p, r, t, True)


RULES_B = [
    ("hcf_lcm", "HCF of two numbers", r"Find the HCF of (\d+) and (\d+)\.", hcf),
    ("hcf_lcm", "LCM of two numbers", r"Find the LCM of (\d+) and (\d+)\.", lcm_rule),
    ("percentage", "girls among students", r"Out of (\d+) students, (\d+)% are girls\. How many girls are there\?", percent_girls),
    ("percentage", "marks scored in a test", r"A test has (\d+) marks\. A student scored (\d+)%\. How many marks did the student score\?", percent_marks),
    ("percentage", "p% of n", r"What is (\d+)% of (\d+)\?", percent_plain),
    ("perimeter_area", "area of a triangle", r"Find the area of a triangle with base (\d+) cm and height (\d+) cm\.", triangle_area),
    ("perimeter_area", "perimeter of a rectangle", r"Find the perimeter of a rectangle with length (\d+) cm and breadth (\d+) cm\.", rectangle_perimeter),
    ("perimeter_area", "area of a rectangle", r"Find the area of a rectangle with length (\d+) cm and breadth (\d+) cm\.", rectangle_area),
    ("perimeter_area", "perimeter of a square", r"Find the perimeter of a square with side (\d+) cm\.", square_perimeter),
    ("perimeter_area", "area of a square", r"Find the area of a square with side (\d+) cm\.", square_area),
    ("simple_interest", "simple interest", r"Find the simple interest on Rs\.(\d+) at (\d+)% per annum for (\d+) years\.", simple_interest),
    ("simple_interest", "amount after t years", r"Rs\.(\d+) is invested at (\d+)% simple interest\. What is the amount after (\d+) years\?", amount),
]
