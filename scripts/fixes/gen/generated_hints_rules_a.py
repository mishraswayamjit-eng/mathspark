"""Hint rules for the angles, bodmas, equation and fraction_arithmetic families.

Each rule takes the numbers pulled out of the question text and returns
    {"answer": Fraction, "h1": str, "h2": str, "cands": [Example, ...], "qnums": set}
or raises Skip. `cands` is a fixed, ordered list of worked examples; the caller picks one.
"""
import math
from fractions import Fraction

from generated_hints_common import Example, Skip, nums


# ── Angles ───────────────────────────────────────────────────────────────────

def _angle(total, word, h1, a, examples):
    if not 0 < a < total:
        raise Skip("angle out of range")
    h2 = ("The two angles add up to %d°. One of them is %d°. So ask: %d° plus what makes %d°? "
          "You can find it by taking %d away from %d." % (total, a, a, total, a, total))
    cands = []
    for e in examples:
        other = total - e
        cands.append(Example(
            "Try another one: the %s angle of %d° is %d°, because %d° − %d° = %d°. Check: %d° + %d° = %d°."
            % (word, e, other, total, e, other, e, other, total), (e, other)))
    return {"answer": Fraction(total - a), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(a)}


def supplementary(a):
    return _angle(180, "supplementary",
                  "Supplementary angles are two angles that sit together on a straight line. "
                  "What do the angles on a straight line add up to?",
                  int(a), (110, 130, 100, 140, 120, 50, 60, 150, 70, 160))


def complementary(a):
    return _angle(90, "complementary",
                  "Complementary angles are two angles that fit together to make a right angle, "
                  "like the corner of a page. How many degrees is a right angle?",
                  int(a), (30, 40, 20, 50, 60, 70, 10, 80, 35, 55))


# ── BODMAS: a + b × c − d ────────────────────────────────────────────────────

def bodmas(a, b, c, d):
    a, b, c, d = int(a), int(b), int(c), int(d)
    answer = a + b * c - d
    h1 = ("This sum has adding, multiplying and taking away. They are not always done from left to right. "
          "Which one does the BODMAS rule say to do first?")
    h2 = ("Multiplication comes before addition and subtraction. So do not start with %d + %d. "
          "Work out %d × %d first, then do the adding and taking away from left to right." % (a, b, b, c))
    cands = []
    for ea in (2, 3, 4, 5, 6, 1, 7, 8):
        for eb in (3, 2, 4, 5):
            for ec in (4, 5, 2, 3, 6, 7):
                for ed in (5, 1, 2, 3, 4, 6, 7, 8, 9):
                    if len({ea, eb, ec, ed}) < 4:
                        continue
                    prod = eb * ec
                    mid = ea + prod
                    res = mid - ed
                    if len({ea, eb, ec, ed, prod, mid, res}) < 7:
                        continue
                    cands.append(Example(
                        "Try another one: %d + %d × %d − %d. Multiply first: %d × %d = %d. "
                        "Now go from left to right: %d + %d = %d, and %d − %d = %d."
                        % (ea, eb, ec, ed, eb, ec, prod, ea, prod, mid, mid, ed, res),
                        (ea, eb, ec, ed, prod, mid, res)))
    return {"answer": Fraction(answer), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(a, b, c, d)}


# ── Equation: ax + b = c ─────────────────────────────────────────────────────

def equation(a, b, c):
    a, b, c = int(a), int(b), int(c)
    if a < 2 or c <= b or (c - b) % a:
        raise Skip("equation does not give a whole number by this method")
    h1 = ("x stands for a hidden number. It was multiplied by %d, then %d was added, and the result was %d. "
          "To find x, undo those steps in reverse order." % (a, b, c))
    h2 = ("Undo the '+ %d' first: take %d away from both sides. Work out %d − %d. "
          "That number is equal to %dx, which means %d times x." % (b, b, c, b, a, a))
    cands = []
    for ea in (2, 3, 5, 4, 10):
        for ex in (4, 3, 5, 2, 6, 7):
            for eb in (3, 1, 5, 7, 2, 4, 6):
                ec = ea * ex + eb
                if len({ea, ex, eb, ec, ea * ex}) < 5:
                    continue
                cands.append(Example(
                    "Try another one: %dx + %d = %d. Take %d away from both sides: %dx = %d. "
                    "Now divide by %d: x = %d, because %d × %d = %d."
                    % (ea, eb, ec, eb, ea, ea * ex, ea, ex, ea, ex, ea * ex),
                    (ea, eb, ec, ea * ex, ex)))
    return {"answer": Fraction(c - b, a), "h1": h1, "h2": h2, "cands": cands, "qnums": nums(a, b, c)}


# ── Fractions: n1/d1 ± n2/d2 ─────────────────────────────────────────────────

_SAME = [(n1, n2, d) for d in (7, 9, 5, 8, 10, 6, 11, 13) for n1 in (5, 4, 6, 7, 3, 8, 9) for n2 in (2, 1, 3, 4)
         if n1 < d and n2 < n1 and math.gcd(n1, d) == 1 and math.gcd(n2, d) == 1]
_UNLIKE = [(7, 8, 1, 4), (5, 8, 1, 4), (7, 9, 1, 3), (5, 9, 1, 3), (7, 8, 1, 2), (5, 6, 1, 2), (9, 10, 2, 5),
           (7, 10, 1, 5), (5, 6, 1, 3), (11, 12, 1, 4), (9, 10, 1, 2), (7, 12, 1, 3), (7, 10, 2, 5), (9, 14, 2, 7)]


def _same_example(n1, n2, d, sign, want_simpler, avoid):
    top = n1 + n2 if sign == "+" else n1 - n2
    if not 0 < top < d or {Fraction(n1, d), Fraction(n2, d), Fraction(top, d)} & avoid:
        return None
    g = math.gcd(top, d)
    if (g > 1) != want_simpler:
        return None
    text = "Try another one: %d/%d %s %d/%d. The bottom number stays %d. On top, %d %s %d = %d. " % (
        n1, d, sign, n2, d, d, n1, sign, n2, top)
    if g > 1:
        text += "That gives %d/%d. Both %d and %d can be divided by %d, which makes it %d/%d." % (
            top, d, top, d, g, top // g, d // g)
        key = (n1, n2, d, top, top // g, d // g)
    else:
        text += "So the answer is %d/%d." % (top, d)
        key = (n1, n2, d, top)
    return Example(text, key)


def _unlike_example(n1, d1, n2, d2, want_simpler, avoid):
    f = d1 // d2
    top = n1 - n2 * f
    g = math.gcd(top, d1)
    if top <= 0 or (g > 1) != want_simpler or {Fraction(n1, d1), Fraction(n2, d2), Fraction(top, d1)} & avoid:
        return None
    text = ("Try another one: %d/%d − %d/%d. Multiply the top and bottom of %d/%d by %d to get %d/%d. "
            "Now %d/%d − %d/%d = %d/%d" % (n1, d1, n2, d2, n2, d2, f, n2 * f, d1, n1, d1, n2 * f, d1, top, d1))
    if g > 1:
        text += ", which is the same as %d/%d." % (top // g, d1 // g)
        key = (n1, d1, n2, d2, top // g, d1 // g)
    else:
        text += "."
        key = (n1, d1, n2, d2, top)
    return Example(text, key)


def fraction(n1, d1, sign, n2, d2):
    n1, d1, n2, d2 = int(n1), int(d1), int(n2), int(d2)
    if not (0 < n1 < d1 and 0 < n2 < d2):
        raise Skip("not two proper fractions")
    answer = Fraction(n1, d1) + Fraction(n2, d2) if sign == "+" else Fraction(n1, d1) - Fraction(n2, d2)
    qnums = nums(n1, d1, n2, d2)
    # Examples are compared with the answer as a fraction, not number by number: no example may use or
    # reach the question's answer or either of its fractions.
    avoid = {answer, Fraction(n1, d1), Fraction(n2, d2)}
    verb ="add" if sign == "+" else "subtract"

    if answer == 0:
        h1 = "Look closely at the two fractions before you do any working. Is there anything special about them?"
        h2 = ("Both fractions are exactly the same: %d/%d. What is left when you take a number away from itself?"
              % (n1, d1))
        h3 = ("Think of whole numbers first: if you have 5 sweets and you eat all 5, how many are left? "
              "Taking a fraction away from itself works the same way.")
        return {"answer": answer, "h1": h1, "h2": h2, "cands": [Example(h3, ())], "qnums": set(),
                "variant": "a fraction taken from itself"}
    if answer < 0 or answer.denominator == 1:
        raise Skip("fraction answer is negative or a whole number")

    if d1 == d2:
        top = n1 + n2 if sign == "+" else n1 - n2
        simpler = math.gcd(top, d1) > 1
        h1 = ("Both fractions have the same bottom number, %d. That means all the pieces are the same size, "
              "so %s is just like counting pieces." % (d1, "adding them" if sign == "+" else "taking some away"))
        h2 = "Keep the bottom number as %d. For the top, work out %d %s %d. " % (d1, n1, sign, n2)
        h2 += "That tells you how many pieces there are altogether." if sign == "+" else "That tells you how many pieces are left."
        if simpler:
            h2 += " Then see if the fraction can be made simpler."
        cands = [e for e in (_same_example(a, b, d, sign, simpler, avoid) for a, b, d in _SAME) if e]
        return {"answer": answer, "h1": h1, "h2": h2, "cands": cands, "qnums": qnums, "answer_nums": set(),
                "variant": "same bottom numbers, %s%s" % (verb, ", then simplify" if simpler else "")}

    if sign != "−" or d1 % d2:
        raise Skip("unlike fractions of a kind there is no rule for")
    f = d1 // d2
    simpler = math.gcd(n1 - n2 * f, d1) > 1
    h1 = ("The bottom numbers, %d and %d, are different, so the pieces are not the same size. "
          "Before you can subtract, both fractions need the same bottom number." % (d1, d2))
    h2 = ("%d is in the %d times table, so change %d/%d into a fraction with %d on the bottom: "
          "multiply its top and its bottom by %d. Then subtract the top numbers." % (d1, d2, n2, d2, d1, f))
    if simpler:
        h2 += " Last, see if the fraction can be made simpler."
    cands = [e for e in (_unlike_example(a, b, c, d, simpler, avoid) for a, b, c, d in _UNLIKE) if e]
    return {"answer": answer, "h1": h1, "h2": h2, "cands": cands, "qnums": qnums, "answer_nums": set(),
            "variant": "different bottom numbers%s" % (", then simplify" if simpler else "")}


RULES_A = [
    ("angles", "supplementary", r"Find the supplementary angle of (\d+)°\.", supplementary),
    ("angles", "complementary", r"Find the complementary angle of (\d+)°\.", complementary),
    ("bodmas", "a + b × c − d", r"Simplify: (\d+) \+ (\d+) × (\d+) − (\d+)", bodmas),
    ("equation", "ax + b = c", r"Find the value of x: (\d+)x \+ (\d+) = (\d+)", equation),
    ("fraction_arithmetic", "fraction ± fraction", r"What is (\d+)/(\d+) ([+−]) (\d+)/(\d+)\?", fraction),
]
