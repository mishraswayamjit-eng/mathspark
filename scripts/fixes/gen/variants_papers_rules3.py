"""Rules for generated variants, part 3: squares, ages, counting, place value, angles, BODMAS, equations."""
import math
import re
from fractions import Fraction

from variants_papers_util import Skip, correct_text, make_steps, matches, need_key, numbers_in, pick, step_texts

ROOT_EXAMPLES = [
    "Try a smaller one: for 169, 10 × 10 = 100 and 20 × 20 = 400, so the root is between 10 and 20. 169 ends in 9, so try 13 or 17: 13 × 13 = 169.",
    "Try a smaller one: for 576, 20 × 20 = 400 and 30 × 30 = 900, so the root is between 20 and 30. 576 ends in 6, so try 24 or 26: 24 × 24 = 576.",
    "Try a smaller one: for 225, 10 × 10 = 100 and 20 × 20 = 400, so the root is between 10 and 20. 225 ends in 5, so try 15: 15 × 15 = 225.",
]
ROUND_ROOT_EXAMPLES = [
    "Try a smaller one: 400 = 4 × 100. Since 2 × 2 = 4 and 10 × 10 = 100, the square root of 400 is 2 × 10 = 20.",
    "Try a smaller one: 1600 = 16 × 100. Since 4 × 4 = 16 and 10 × 10 = 100, the square root of 1600 is 4 × 10 = 40.",
]


def rule_square_root(q):
    m = matches(q, r"Find the square root of (\d+)\.")
    if not m:
        return None
    old = q.get("hints") or []
    if len(old) != 3 or not old[1].startswith("Try numbers:"):
        return None
    n = int(m.group(1))
    r = math.isqrt(n)
    if r * r != n:
        raise Skip("not a perfect square")
    need_key(q, r)
    first = "The square root of %d is the number that, multiplied by itself, gives %d." % (n, n)
    if r <= 10:
        hints = [first, "Go through the squares in order: 1 × 1, 2 × 2, 3 × 3 and so on. Which one gives %d?" % n,
                 pick(q, ["Try a smaller one: the square root of 49 is 7, because 7 × 7 = 49.",
                          "Try a smaller one: the square root of 36 is 6, because 6 × 6 = 36."], avoid=[n, r])]
    elif r % 10 == 0:
        hints = [first,
                 "%d = %d × 100. Find the number whose square is %d and the number whose square is 100, then multiply the two." % (n, n // 100, n // 100),
                 pick(q, ROUND_ROOT_EXAMPLES, avoid=[n])]
    else:
        lo = r // 10 * 10
        hi = lo + 10
        hints = [first,
                 "Narrow it down: %d × %d = %d and %d × %d = %d. %d lies between them, so its square root is between %d and %d. Now use the last digit of %d."
                 % (lo, lo, lo * lo, hi, hi, hi * hi, n, lo, hi, n),
                 pick(q, ROOT_EXAMPLES, avoid=[n])]
    return {"hints": hints, "why": "Hint 3 stated the answer ('Try 22: 22×22=484. Yes!')."}


def rule_square(q):
    m = matches(q, r"Find the square of (\d+)\.")
    if not m:
        return None
    old = step_texts(q)
    if len(old) != 2 or not re.fullmatch(r"Square of \d+ = \d+ × \d+", old[0]):
        return None
    n = int(m.group(1))
    need_key(q, n * n)
    texts = ["Squaring a number means multiplying it by itself, so the square of %d is %d × %d." % (n, n, n),
             "%d × %d = %d. So the square of %d is %d." % (n, n, n * n, n, n * n)]
    return {"steps": make_steps(q, texts), "why": "Step 1 read as an untrue sum ('Square of 9 = 9 × 9' parses as 9 = 9 × 9); step 2 was a bare number."}


def rule_perfect_square(q):
    if not matches(q, r"Which of the following is a perfect square\?"):
        return None
    old = q.get("hints") or []
    if len(old) != 3 or not re.fullmatch(r"\d+² = \d+\. Check the others too\.", old[2]):
        return None
    key = correct_text(q).strip()
    if not key.isdigit() or math.isqrt(int(key)) ** 2 != int(key):
        raise Skip("the keyed choice is not a perfect square")
    r = math.isqrt(int(key))
    hints = [old[0],
             "Square a few whole numbers near the choices: work out %d × %d, %d × %d and %d × %d. Does one of the choices turn up?"
             % (r - 1, r - 1, r, r, r + 1, r + 1),
             pick(q, ["For example, 49 is a perfect square because 7 × 7 = 49. But 50 is not: 7 × 7 is too small and 8 × 8 = 64 is too big.",
                      "For example, 81 is a perfect square because 9 × 9 = 81. But 85 is not: 9 × 9 is too small and 10 × 10 = 100 is too big."])]
    return {"hints": hints, "why": "Hint 3 stated the answer ('12² = 144')."}


def rule_age_difference(q):
    m = matches(q, r"(\w+) is (\d+) years old and (\w+) is (\d+) years old\. What was the difference in their ages (\d+) years ago\?")
    if not m:
        return None
    old = q.get("hints") or []
    if len(old) != 3 or not old[2].startswith("The difference was, is, and always will be"):
        return None
    x, y, z = int(m.group(2)), int(m.group(4)), int(m.group(5))
    need_key(q, abs(x - y))
    hints = ["Both of them get one year older every year. So does the gap between their ages ever change?",
             "The gap %d years ago was the same as the gap today. So subtract today's ages: %d − %d." % (z, max(x, y), min(x, y)),
             pick(q, ["Try a smaller one: a 9-year-old and a 6-year-old are 3 years apart. Two years ago they were 7 and 4, still 3 years apart.",
                      "Try a smaller one: a 12-year-old and a 7-year-old are 5 years apart. Two years ago they were 10 and 5, still 5 years apart."],
                  avoid=[abs(x - y)])]
    return {"hints": hints, "why": "Hint 3 stated the answer ('always will be N years')."}


def rule_digit_count(q):
    m = matches(q, r"How many (\d)-digit (even numbers|odd numbers|numbers) are there( in all)?\?")
    if not m:
        return None
    old = q.get("hints") or []
    if len(old) != 3 or not old[2].startswith("Total count = largest − smallest + 1 ="):
        return None
    d, kind = int(m.group(1)), m.group(2).split()[0]
    if d < 2:
        raise Skip("one-digit numbers need their own treatment")
    lo, hi = 10 ** (d - 1), 10 ** d - 1
    total = hi - lo + 1
    ends = "The smallest %d-digit number is %d and the largest is %d." % (d, lo, hi)
    if kind == "numbers":
        need_key(q, total)
        hints = [ends + " You need to count every number from one to the other.",
                 "To count from %d to %d, subtract and then add 1, so that both ends are counted: %d − %d + 1." % (lo, hi, hi, lo),
                 "Try a smaller one: from 5 to 9 there are 9 − 5 + 1 = 5 numbers. Count them to check: 5, 6, 7, 8, 9."]
        texts = [ends,
                 "Count from %d to %d, counting both ends: %d − %d + 1 = %d." % (lo, hi, hi, lo, total),
                 "So there are %d %d-digit numbers in all." % (total, d)]
        why = "Hint 3 stated the answer; the last step read 'Total N-digit = X. All = X'."
    else:
        half = total // 2
        need_key(q, half)
        hints = [ends + " Count all of them first, then think about how many are %s." % kind,
                 "Count them all: %d − %d + 1. Then remember that even and odd numbers take turns." % (hi, lo),
                 "Even and odd numbers alternate, so here exactly half are %s. Try a smaller one: from 10 to 19 there are 10 numbers, and 5 of them are %s." % (kind, kind)]
        texts = [ends,
                 "Count them all, counting both ends: %d − %d + 1 = %d." % (hi, lo, total),
                 "Even and odd numbers alternate. The list starts with an even number and ends with an odd number, so exactly half are %s: %d ÷ 2 = %d." % (kind, total, half),
                 "So there are %d %d-digit %s numbers." % (half, d, kind)]
        why = "Hint 3 gave the total outright; the last step ('Total N-digit = X. Even = Y') did not say why half."
    return {"hints": hints, "steps": make_steps(q, texts), "why": why}


PLACES = ["units", "tens", "hundreds", "thousands", "ten-thousands"]
PLACE_SINGULAR = {"units": "unit", "tens": "ten", "hundreds": "hundred", "thousands": "thousand", "ten-thousands": "ten-thousand"}


def rule_place_value_one(q):
    m = matches(q, r"In the number (\d+), what is the place value of the digit 1 in the (units|tens|hundreds|thousands|ten-thousands) place\?")
    if not m:
        return None
    old = q.get("hints") or []
    if len(old) != 3 or not re.fullmatch(r"The \S+ place has value \d+\.", old[1]):
        return None
    number, place = m.group(1), m.group(2)
    idx = PLACES.index(place)
    if len(number) <= idx or number[-idx - 1] != "1":
        raise Skip("the digit in that place is not 1")
    need_key(q, 10 ** idx)
    single = PLACE_SINGULAR[place]
    hints = ["A digit's place value is the digit multiplied by what its place is worth.",
             "The digit 1 sits in the %s place, so it stands for 1 %s. How do you write 1 %s as a number?" % (place, single, single),
             pick(q, ["For example, in 365 the digit 6 is in the tens place, so its place value is 6 × 10 = 60.",
                      "For example, in 4,270 the digit 2 is in the hundreds place, so its place value is 2 × 100 = 200."],
                  avoid=[10 ** idx])]
    return {"hints": hints, "why": "With the digit 1, hint 2 ('The %s place has value %d') stated the answer." % (place, 10 ** idx)}


def rule_vertically_opposite(q):
    m = matches(q, r"Two straight lines cross\. One angle formed is (\d+)°\. Find the vertically opposite angle\.")
    if not m:
        return None
    old = q.get("hints") or []
    if len(old) != 3 or not old[2].startswith("So the answer is simply"):
        return None
    need_key(q, int(m.group(1)))
    hints = [old[0], old[1],
             pick(q, ["For example, if two crossing lines make an angle of 50°, the angle directly opposite it is also 50°.",
                      "For example, if two crossing lines make an angle of 70°, the angle directly opposite it is also 70°."],
                  avoid=[int(m.group(1))])]
    return {"hints": hints, "why": "Hint 3 stated the answer ('So the answer is simply N°')."}


def rule_bodmas(q):
    m = matches(q, r"Simplify: (\d+(?: [+\-−×÷] \d+)+)")
    if not m:
        return None
    old = step_texts(q)
    if not (len(old) == 2 and old[0].startswith("Follow BODMAS") and old[1].startswith("The answer is")):
        return None
    tokens = m.group(1).replace("-", "−").split()
    # Split into terms joined by + and −; each term is a chain of × and ÷.
    terms, signs, chain = [], ["+"], [tokens[0]]
    for op, num in zip(tokens[1::2], tokens[2::2]):
        if op in "+−":
            terms.append(chain)
            signs.append(op)
            chain = [num]
        else:
            chain += [op, num]
    terms.append(chain)
    worked, values, kinds = [], [], set()
    for chain in terms:
        v = Fraction(chain[0])
        for op, num in zip(chain[1::2], chain[2::2]):
            kinds.add(op)
            v = v * int(num) if op == "×" else v / int(num)
        if v.denominator != 1:
            raise Skip("a division is not exact")
        values.append(int(v))
        if len(chain) > 1:
            worked.append("%s = %d" % (" ".join(chain), v))
    if not worked or len(terms) == 1:
        raise Skip("no mix of operations to order")
    name = {"×": "Multiplication comes", "÷": "Division comes"}.get("".join(kinds), "Multiplication and division come")
    texts = ["%s before addition and subtraction: %s." % (name, " and ".join(worked))]
    running, moves, dipped = values[0], [], False
    for sign, v in zip(signs[1:], values[1:]):
        after = running + v if sign == "+" else running - v
        dipped = dipped or after < 0
        moves.append("%d %s %d = %d" % (running, sign, v, after))
        running = after
    if running < 0:
        raise Skip("the answer is below zero")
    need_key(q, running)
    if dipped:
        # e.g. 35 − 40 + 5: add first, so that a child never has to go below zero.
        if signs[1:] != ["−", "+"]:
            raise Skip("a running total goes below zero")
        added = values[0] + values[2]
        texts.append("Now the sum reads %d − %d + %d." % (values[0], values[1], values[2]))
        texts.append("Taking %d from %d would go below zero, so do the adding first: %d + %d = %d, then %d − %d = %d."
                     % (values[1], values[0], values[0], values[2], added, added, values[1], running))
    elif len(moves) == 1:
        texts.append("Now %s: %s." % ("add" if signs[1] == "+" else "subtract", moves[0]))
    else:
        texts.append("Now the sum reads %s." % " ".join([str(values[0])] + ["%s %d" % (s, v) for s, v in zip(signs[1:], values[1:])]))
        texts.append("Work from left to right: %s." % ", then ".join(moves))
    texts.append("So the answer is %d." % running)
    return {"steps": make_steps(q, texts), "why": "Step 1 only recited the BODMAS rule and step 2 was 'The answer is N': no working shown."}


def rule_linear(q):
    m = matches(q, r"Solve: (\d+)x ([+\-−]) (\d+) = (\d+)")
    if not m:
        return None
    old = step_texts(q)
    if not (len(old) == 2 and re.fullmatch(r"(Add \d+ to|Subtract \d+ from) both sides", old[0]) and re.fullmatch(r"Divide both sides by \d+", old[1])):
        return None
    a, sign, b, c = int(m.group(1)), m.group(2).replace("-", "−"), int(m.group(3)), int(m.group(4))
    rhs = c + b if sign == "−" else c - b
    if a < 2 or rhs <= 0 or rhs % a:
        raise Skip("x is not a positive whole number")
    x = rhs // a
    need_key(q, x)
    if sign == "−":
        first = "Add %d to both sides to undo the − %d: %dx = %d + %d = %d." % (b, b, a, c, b, rhs)
    else:
        first = "Subtract %d from both sides to undo the + %d: %dx = %d − %d = %d." % (b, b, a, c, b, rhs)
    texts = [first,
             "Divide both sides by %d: x = %d ÷ %d = %d." % (a, rhs, a, x),
             "Check: %d × %d %s %d = %d. So x = %d." % (a, x, sign, b, c, x)]
    # Keep each old formula beside the step it belongs to; the new closing step has none.
    latex = [s.get("latex", "") for s in q["stepByStep"]] + [""]
    steps = [{"text": t, "latex": l} for t, l in zip(texts, latex)]
    return {"steps": steps, "why": "The steps named the moves but showed no working and never reached the answer."}


RULES = [
    ("square-root-hints", rule_square_root),
    ("square-steps", rule_square),
    ("perfect-square-hint", rule_perfect_square),
    ("age-difference-hints", rule_age_difference),
    ("digit-count-hints-and-steps", rule_digit_count),
    ("place-value-digit-1-hints", rule_place_value_one),
    ("vertically-opposite-hint", rule_vertically_opposite),
    ("bodmas-thin-steps", rule_bodmas),
    ("linear-equation-thin-steps", rule_linear),
]
