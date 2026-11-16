"""Recompute the answer of every Grade 5 question whose wording is regular enough to parse exactly.

    python -X utf8 scripts/fixes/gen/answers_scan.py            # flags only
    python -X utf8 scripts/fixes/gen/answers_scan.py --unparsed # also list generated questions no template matched

A question is parsed only when its whole text matches a template with re.fullmatch. For each
parsed question the answer is computed from the numbers in the text and compared with the choices:
  KEY       the computed answer is not the keyed choice
  TWICE     the computed answer appears in two choices
  NOWHERE   the computed answer is in no choice
  SAME      two choices are identical (checked for EVERY Grade 5 question, parsed or not)
  EQUAL     two choices are different text but the same number, e.g. 6/10 and 3/5 (every question)
  INEXACT   the question needs a whole number but the calculation does not give one
  BROKEN    the question contradicts itself (e.g. names a digit that is not in that place)
Read-only: prints a report, changes nothing.
"""
import io
import json
import os
import re
import sys
from collections import Counter
from fractions import Fraction
from math import gcd, isqrt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)

RESERVED = os.path.join(ROOT, "scripts", "fixes", "answers_ids.txt")
GENERATED = ("VAR_G5_vary_", "VAR_EXT_", "VAR2_EXT_", "BOOST_EXT_", "PH3_EXT_")

PLACES = {"units": 0, "ones": 0, "tens": 1, "hundreds": 2, "thousands": 3, "ten-thousands": 4, "lakhs": 5}
PLACE_RE = "(" + "|".join(PLACES) + ")"


class Inexact(Exception):
    pass


class Broken(Exception):
    pass


def whole(x, what="answer"):
    x = Fraction(x)
    if x.denominator != 1:
        raise Inexact("%s is %s, not a whole number" % (what, show(x)))
    return x


def show(x):
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        if x.denominator in (2, 4, 5, 8, 10, 20, 25, 50, 100, 1000):
            return "%s (= %s)" % (x, float(x))
        return str(x)
    return str(x)


# ── Arithmetic expression evaluator (exact) ──────────────────────────────────

_TOKEN = re.compile(r"\d+(?:\.\d+)?|[()+\-*/]")


def evaluate(expr):
    s = expr.replace("×", "*").replace("÷", "/").replace("−", "-").replace("–", "-")
    s = s.replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")").strip()
    if not s or re.search(r"[^0-9 .()+\-*/]", s):
        return None
    tokens = _TOKEN.findall(s)
    if "".join(tokens) != s.replace(" ", ""):
        return None
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def take():
        pos[0] += 1
        return tokens[pos[0] - 1]

    def atom():
        t = peek()
        if t == "(":
            take()
            v = total()
            if peek() != ")":
                raise ValueError
            take()
            return v
        if t == "-":
            take()
            return -atom()
        if t is None or not re.match(r"\d", t):
            raise ValueError
        return Fraction(take())

    def product():
        v = atom()
        while peek() in ("*", "/"):
            op = take()
            w = atom()
            v = v * w if op == "*" else v / w
        return v

    def total():
        v = product()
        while peek() in ("+", "-"):
            op = take()
            w = product()
            v = v + w if op == "+" else v - w
        return v

    try:
        v = total()
        return v if pos[0] == len(tokens) else None
    except (ValueError, ZeroDivisionError):
        return None


# ── Reading a choice ─────────────────────────────────────────────────────────

_UNIT = r"(?:°|cm|sq\. ?cm|sq cm|cm²|m|km|mm|g|kg|ml|l|litres|years|marks|%)?"
_OPT = re.compile(r"(?:Rs\.? ?|₹ ?)?(-?\d+(?:\.\d+)?)(?:/(\d+))? ?" + _UNIT)
_MIXED = re.compile(r"(-?\d+) (\d+)/(\d+)")


def option_value(text):
    """The number a choice states, as a Fraction, or None."""
    t = text.strip().replace("−", "-").replace("–", "-").replace(",", "")
    m = _MIXED.fullmatch(t)
    if m:
        a, b, c = int(m.group(1)), int(m.group(2)), int(m.group(3))
        return None if c == 0 else Fraction(a) + (Fraction(b, c) if a >= 0 else -Fraction(b, c))
    m = _OPT.fullmatch(t)
    if not m:
        return None
    if m.group(2):
        return None if int(m.group(2)) == 0 else Fraction(m.group(1)) / int(m.group(2))
    return Fraction(m.group(1))


def norm(text):
    return re.sub(r"\s+", "", text.replace("−", "-").replace("–", "-")).lower()


# ── Templates ────────────────────────────────────────────────────────────────

TEMPLATES = []


def T(pattern, fn, family):
    """N = whole number, @ = a first name, ~ = a thing (one or two lowercase words), P = a place name."""
    out = []
    for ch in pattern:
        if ch == "N":
            out.append(r"(\d+)")
        elif ch == "@":
            out.append(r"(?:[A-Z][a-z]+)")
        elif ch == "~":
            out.append(r"(?:[a-z]+(?: [a-z]+)?)")
        elif ch == "P":
            out.append(PLACE_RE)
        else:
            out.append(re.escape(ch))
    TEMPLATES.append((re.compile("".join(out)), fn, family))


def ints(fn):
    return lambda *g: fn(*[int(x) for x in g])


def lcm(a, b):
    return a * b // gcd(a, b)


T("Find the HCF of N and N.", ints(lambda a, b: gcd(a, b)), "hcf")
T("Find the LCM of N and N.", ints(lambda a, b: lcm(a, b)), "lcm")
T("Find the value of x: Nx + N = N", ints(lambda a, b, c: whole(Fraction(c - b, a), "x")), "equation")
T("Solve: Nx + N = N", ints(lambda a, b, c: whole(Fraction(c - b, a), "x")), "equation")
T("Solve: Nx − N = N", ints(lambda a, b, c: whole(Fraction(c + b, a), "x")), "equation")
T("Solve: Nx - N = N", ints(lambda a, b, c: whole(Fraction(c + b, a), "x")), "equation")
T("Find the value of x: Nx − N = N", ints(lambda a, b, c: whole(Fraction(c + b, a), "x")), "equation")
T("Find the supplementary angle of N°.", ints(lambda a: 180 - a), "angles")
T("Find the complementary angle of N°.", ints(lambda a: 90 - a), "angles")
T("If √x + N = N, find x.", ints(lambda a, b: (b - a) ** 2), "roots")
T("Rs.N is invested at N% simple interest. What is the amount after N years?",
  ints(lambda p, r, t: p + Fraction(p * r * t, 100)), "simple interest")
T("Find the simple interest on Rs.N at N% per annum for N years.",
  ints(lambda p, r, t: Fraction(p * r * t, 100)), "simple interest")
T("What is N/N of N?", ints(lambda a, b, n: Fraction(a * n, b)), "fraction of")
T("Find the missing number: N/N = ?/N", ints(lambda a, b, d: whole(Fraction(a * d, b))), "equivalent fractions")
T("How many numbers from N to N are divisible by N?", ints(lambda a, b, k: b // k - (a - 1) // k), "counting")
T("How many odd numbers are there from N to N?", ints(lambda a, b: (b + 1) // 2 - a // 2), "counting")
T("How many even numbers are there from N to N?", ints(lambda a, b: b // 2 - (a - 1) // 2), "counting")
T("Find the area of a triangle with base N cm and height N cm.", ints(lambda b, h: Fraction(b * h, 2)), "area")
T("Find the perimeter of a rectangle with length N cm and breadth N cm.", ints(lambda l, b: 2 * (l + b)), "perimeter")
T("Find the perimeter of a rectangle with length N cm and width N cm.", ints(lambda l, b: 2 * (l + b)), "perimeter")
T("Find the area of a rectangle with length N cm and breadth N cm.", ints(lambda l, b: l * b), "area")
T("Find the area of a rectangle with length N cm and width N cm.", ints(lambda l, b: l * b), "area")
T("Find the area of a square with side N cm.", ints(lambda s: s * s), "area")
T("Find the perimeter of a square with side N cm.", ints(lambda s: 4 * s), "perimeter")
T("Out of N students, N% are girls. How many girls are there?",
  ints(lambda n, p: whole(Fraction(n * p, 100), "number of girls")), "percentage")
T("A test has N marks. A student scored N%. How many marks did the student score?",
  ints(lambda n, p: Fraction(n * p, 100)), "percentage")
T("What is N% of N?", ints(lambda p, n: Fraction(n * p, 100)), "percentage")
T("If N : N = N : x, find x.", ints(lambda a, b, c: Fraction(b * c, a)), "ratio")
T("If x = N and y = N, find the value of Nx + Ny.", ints(lambda x, y, a, b: a * x + b * y), "substitution")
T("Think of a number N. Multiply it by N and add N. What do you get?", ints(lambda n, a, b: n * a + b), "substitution")
T("If x = N, find the value of Nx + N − N.", ints(lambda x, a, b, c: a * x + b - c), "substitution")
T("Find the square of N.", ints(lambda a: a * a), "roots")
T("Find the sum of first N odd numbers.", ints(lambda n: n * n), "series")
T("Find the sum of first N even numbers.", ints(lambda n: n * (n + 1)), "series")
T("Find the sum of first N natural numbers.", ints(lambda n: n * (n + 1) // 2), "series")
T("Convert N cm to m.", ints(lambda n: Fraction(n, 100)), "units")
T("Convert N mm to cm.", ints(lambda n: Fraction(n, 10)), "units")
T("Convert N m to km.", ints(lambda n: Fraction(n, 1000)), "units")
T("Convert N m to cm.", ints(lambda n: n * 100), "units")
T("Convert N km to m.", ints(lambda n: n * 1000), "units")
T("Convert N kg to g.", ints(lambda n: n * 1000), "units")
T("If N ~ cost Rs.N, what is the cost of one ~?", ints(lambda n, c: Fraction(c, n)), "unitary")
T("A ~ holds N litres of water. How many glasses of N ml each can be filled?",
  ints(lambda l, ml: whole(Fraction(l * 1000, ml), "litres ÷ glass")), "glasses")
T("@ has N marbles. @ gives N/N of them to a friend. How many marbles does @ have left?",
  ints(lambda n, a, b: whole(n - Fraction(n * a, b), "marbles left")), "fraction of")
T("@ buys N ~ at Rs.N each and pays Rs.N. How much change does @ get back?",
  ints(lambda n, c, p: p - n * c), "money")
T("@ buys N ~ at Rs.N each. What is the total cost?", ints(lambda n, c: n * c), "money")
T("@ buys a ~ for Rs.N and sells it at a profit of N%. What is the selling price?",
  ints(lambda c, p: c + Fraction(c * p, 100)), "profit and loss")
T("@ bought a ~ for Rs.N and sold it at a loss of N%. What is the selling price?",
  ints(lambda c, p: c - Fraction(c * p, 100)), "profit and loss")
T("@ buys a ~ for Rs.N and sells it at a loss of N%. What is the selling price?",
  ints(lambda c, p: c - Fraction(c * p, 100)), "profit and loss")
T("@ bought a ~ for Rs.N and sold it at a profit of N%. What is the selling price?",
  ints(lambda c, p: c + Fraction(c * p, 100)), "profit and loss")
T("@ has N bags of ~, each weighing N kg N g. What is the total weight in grams?",
  ints(lambda n, kg, g: n * (kg * 1000 + g)), "units")
T("Divide N in the ratio N:N. What is the smaller share?",
  ints(lambda n, a, b: whole(Fraction(n * min(a, b), a + b), "share")), "ratio")
T("Divide N in the ratio N:N. What is the larger share?",
  ints(lambda n, a, b: whole(Fraction(n * max(a, b), a + b), "share")), "ratio")
T("@ has N ~ and divides them in the ratio N:N. How many ~ are in the larger group?",
  ints(lambda n, a, b: whole(Fraction(n * max(a, b), a + b), "group")), "ratio")
T("@ has N ~ and divides them in the ratio N:N. How many ~ are in the smaller group?",
  ints(lambda n, a, b: whole(Fraction(n * min(a, b), a + b), "group")), "ratio")
T("The average of N numbers is N. When a new number N is added, what is the new average?",
  ints(lambda n, avg, x: Fraction(n * avg + x, n + 1)), "average")
T("How many N-digit numbers are there in all?", ints(lambda d: 9 * 10 ** (d - 1)), "counting")
T("How many N-digit even numbers are there?", ints(lambda d: 9 * 10 ** (d - 1) // 2), "counting")
T("How many N-digit odd numbers are there?", ints(lambda d: 9 * 10 ** (d - 1) // 2), "counting")


def _sqrt(a):
    a = int(a)
    r = isqrt(a)
    if r * r != a:
        raise Inexact("%d is not a perfect square" % a)
    return r


T("Find the square root of N.", _sqrt, "roots")


def _pages(n):
    n = int(n)
    return sum(len(str(i)) for i in range(1, n + 1))


T("A book has N pages. How many digits are used to number all the pages?", _pages, "counting")


def _place_value(number, digit, place):
    k = PLACES[place]
    if len(number) <= k or number[len(number) - 1 - k] != digit:
        raise Broken("the %s digit of %s is not %s" % (place, number, digit))
    return int(digit) * 10 ** k


T("In the number N, what is the place value of the digit N in the P place?", _place_value, "place value")


def _times(number, d1, p1, d2, p2):
    for d, p in ((d1, p1), (d2, p2)):
        k = PLACES[p]
        if len(number) <= k or number[len(number) - 1 - k] != d:
            raise Broken("the %s digit of %s is not %s" % (p, number, d))
    if int(d2) == 0:
        raise Broken("dividing by a place value of 0")
    return Fraction(int(d1) * 10 ** PLACES[p1], int(d2) * 10 ** PLACES[p2])


T("In the number N, the place value of N (in P place) is how many times the place value of N (in P place)?",
  _times, "place value")


def _avg_missing(*g):
    n, avg, k = int(g[0]), int(g[1]), int(g[2])
    known = [int(x) for x in g[3].split(", ")]
    if len(known) != k or k != n - 1:
        raise Broken("%d numbers listed, %d expected" % (len(known), n - 1))
    return n * avg - sum(known)


TEMPLATES.append((re.compile(r"The average of (\d+) numbers is (\d+)\. If (\d+) of the numbers are (\d+(?:, \d+)*), find the missing number\."),
                  _avg_missing, "average"))
TEMPLATES.append((re.compile(r"Find the average of: (\d+(?:, \d+)*)"),
                  lambda s: Fraction(sum(int(x) for x in s.split(", ")), len(s.split(", "))), "average"))


def _ap_term(a, b, c, n):
    a, b, c, n = int(a), int(b), int(c), int(n)
    if b - a != c - b:
        raise Broken("not an arithmetic sequence")
    return a + (n - 1) * (b - a)


TEMPLATES.append((re.compile(r"In an arithmetic sequence starting (\d+), (\d+), (\d+), \.\.\., find the (\d+)(?:st|nd|rd|th) term\."),
                  _ap_term, "series"))


def _ap_sum(a, b, c, last):
    a, b, c, last = int(a), int(b), int(c), int(last)
    d = b - a
    if d <= 0 or c - b != d or (last - a) % d:
        raise Broken("not an arithmetic series ending at %d" % last)
    n = (last - a) // d + 1
    return n * (a + last) // 2


TEMPLATES.append((re.compile(r"Find the sum of the arithmetic series: (\d+), (\d+), (\d+), \.\.\., (\d+)\."), _ap_sum, "series"))


def _simplify(expr):
    v = evaluate(expr)
    if v is None:
        raise LookupError
    return v


TEMPLATES.append((re.compile(r"Simplify: ([0-9 .()\[\]{}+\-−×÷]+)"), _simplify, "bodmas"))
TEMPLATES.append((re.compile(r"(?:Evaluate|Calculate|Find the value of): ([0-9 .()\[\]{}+\-−×÷]+)"), _simplify, "bodmas"))
TEMPLATES.append((re.compile(r"What is (\d+/\d+ [+−\-] \d+/\d+)\?"), _simplify, "fraction arithmetic"))
TEMPLATES.append((re.compile(r"Simplify: (\d+/\d+ [+−\-] \d+/\d+)"), _simplify, "fraction arithmetic"))


def _greater(a, b, c, d):
    x, y = Fraction(int(a), int(b)), Fraction(int(c), int(d))
    if x == y:
        return ("text", "They are equal")
    return ("text", "%s/%s" % ((a, b) if x > y else (c, d)))


T("Which is greater: N/N or N/N?", _greater, "compare fractions")


def _smaller(a, b, c, d):
    x, y = Fraction(int(a), int(b)), Fraction(int(c), int(d))
    if x == y:
        return ("text", "They are equal")
    return ("text", "%s/%s" % ((a, b) if x < y else (c, d)))


T("Which is smaller: N/N or N/N?", _smaller, "compare fractions")


def _like_terms(sign):
    def fn(a, b, c, d):
        a, b, c, d = int(a), int(b), int(c), int(d)
        k = b + d if sign > 0 else b - d
        if k == 0:
            return ("text", "%dx" % (a + c))
        return ("text", "%dx %s %d" % (a + c, "+" if k > 0 else "−", abs(k)))
    return fn


T("Simplify: Nx + N + Nx + N", _like_terms(+1), "like terms")
T("Simplify: Nx + N + Nx − N", _like_terms(-1), "like terms")

T("Which of the following N-digit numbers has a digit sum of N?",
  lambda d, s: ("pick", lambda t: t.isdigit() and len(t) == int(d) and sum(int(c) for c in t) == int(s)), "digit sum")
T("Which of the following numbers is divisible by N?",
  lambda k: ("pick", lambda t: t.isdigit() and int(t) % int(k) == 0), "divisibility")


# ── Scan ─────────────────────────────────────────────────────────────────────

def parse(text):
    """(family, computed) or None. Tries every template; they must agree."""
    found = []
    for rx, fn, family in TEMPLATES:
        m = rx.fullmatch(text.strip())
        if not m:
            continue
        try:
            found.append((family, fn(*m.groups())))
        except LookupError:
            continue
        except Inexact as e:
            found.append((family, e))
        except Broken as e:
            found.append((family, e))
    return found[0] if found else None


def judge(q, computed):
    """List of (kind, detail)."""
    opts = [o["text"] for o in q["options"]]
    key = "ABCD".find(q["correctAnswer"])
    flags = []
    if isinstance(computed, Inexact):
        return [("INEXACT", str(computed))]
    if isinstance(computed, Broken):
        return [("BROKEN", str(computed))]
    if isinstance(computed, tuple) and computed[0] == "pick":
        hits = [i for i, t in enumerate(opts) if computed[1](t.strip())]
        label = "choices that fit: %s" % (", ".join("%s=%s" % ("ABCD"[i], opts[i]) for i in hits) or "none")
    elif isinstance(computed, tuple) and computed[0] == "text":
        hits = [i for i, t in enumerate(opts) if norm(t) == norm(computed[1])]
        label = "computed %s" % computed[1]
    else:
        value = Fraction(computed)
        values = [option_value(t) for t in opts]
        hits = [i for i, v in enumerate(values) if v is not None and v == value]
        label = "computed %s" % show(value)
        if any(v is None for v in values) and not hits:
            if 0 <= key < len(opts) and re.fullmatch(r"none of (these|the above)", opts[key].strip().lower()):
                return []  # the computed value is in no choice and the key says exactly that
            return [("UNREADABLE", "%s; a choice could not be read as a number" % label)]
    if len(hits) > 1:
        flags.append(("TWICE", label + "; in choices " + ", ".join("ABCD"[i] for i in hits)))
    if not hits:
        flags.append(("NOWHERE", label + "; keyed %s=%s" % (q["correctAnswer"], opts[key] if key >= 0 else "?")))
    elif key not in hits:
        flags.append(("KEY", label + "; that is choice %s, but keyed %s=%s" % (
            "ABCD"[hits[0]], q["correctAnswer"], opts[key] if key >= 0 else "?")))
    return flags


def main():
    qs = bank.load_pool("grade5")
    with io.open(RESERVED, encoding="utf-8") as f:
        reserved = {line.strip() for line in f if line.strip()}

    parsed = Counter()
    flagged = []
    unparsed = []
    for q in qs:
        opts = [o["text"] for o in q["options"]]
        flags = []
        seen = {}
        for i, t in enumerate(opts):
            k = norm(t)
            if k in seen:
                flags.append(("SAME", "choices %s and %s are both %r" % ("ABCD"[seen[k]], "ABCD"[i], t)))
            seen.setdefault(k, i)
        # Two choices that are bare numbers or fractions with the same value ("6/10" and "3/5").
        bare = [(i, option_value(t)) for i, t in enumerate(opts) if re.fullmatch(r"-?\d+(?:\.\d+)?(?:/\d+)?", norm(t))]
        for a in range(len(bare)):
            for b in range(a + 1, len(bare)):
                if bare[a][1] is not None and bare[a][1] == bare[b][1] and norm(opts[bare[a][0]]) != norm(opts[bare[b][0]]):
                    flags.append(("EQUAL", "choices %s=%s and %s=%s have the same value" % (
                        "ABCD"[bare[a][0]], opts[bare[a][0]], "ABCD"[bare[b][0]], opts[bare[b][0]])))
        if len(opts) != 4 or q.get("correctAnswer") not in ("A", "B", "C", "D"):
            flags.append(("BROKEN", "%d choices, key %r" % (len(opts), q.get("correctAnswer"))))
        got = parse(q["questionText"])
        if got:
            parsed[got[0]] += 1
            flags += judge(q, got[1])
        elif q["id"].startswith(GENERATED):
            unparsed.append(q)
        if flags:
            flagged.append((q, got[0] if got else "-", flags))

    print("Grade 5 questions: %d; parsed exactly: %d; generated but not parsed: %d" % (len(qs), sum(parsed.values()), len(unparsed)))
    print("parsed by family: " + ", ".join("%s %d" % kv for kv in sorted(parsed.items())))
    print("\n%d questions flagged (%d of them already on the reserved list)\n" % (
        len(flagged), sum(1 for q, _, _ in flagged if q["id"] in reserved)))
    for q, family, flags in flagged:
        mark = "reserved" if q["id"] in reserved else "NEW"
        print("%s  [%s, %s]" % (q["id"], family, mark))
        print("    Q: %s" % q["questionText"])
        print("    choices: %s   keyed: %s" % (" | ".join("%s=%s" % ("ABCD"[i], o["text"]) for i, o in enumerate(q["options"])), q["correctAnswer"]))
        for kind, detail in flags:
            print("    %-8s %s" % (kind, detail))
    if "--unparsed" in sys.argv:
        print("\nGenerated questions no template matched:")
        for q in unparsed:
            print("  %s | %s | %s | %s" % (q["id"], q["questionText"], [o["text"] for o in q["options"]], q["correctAnswer"]))


if __name__ == "__main__":
    main()
