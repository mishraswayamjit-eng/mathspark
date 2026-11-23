"""Figures for Grade 4 fractions (node gr4_fractions).

    python -X utf8 scripts/figures/authoring/g4_gr4_fractions.py            # write the part file, print counts
    python -X utf8 scripts/figures/authoring/g4_gr4_fractions.py all        # also print every entry for review
    python -X utf8 scripts/figures/authoring/g4_gr4_fractions.py <text>     # print entries whose id or rule matches

Writes data/question-figures/parts/g4-gr4_fractions.json.
Generated families are drawn by the rules below; the rest are in g4_gr4_fractions_own.py.
"""
import math
import re
import sys
from fractions import Fraction

from g4_gr4_fractions_lib import Q, bar, bm, entry, fb, ft, load, report, seg, segs, setf, w, write
from g4_gr4_fractions_own import OWN

NODE = "gr4_fractions"
RULES = []


def rule(name):
    def deco(fn):
        RULES.append((name, fn))
        return fn
    return deco


def whole_and_rest(p, q):
    """Bars for an improper fraction p/q between 1 and 2."""
    return [(q, q, "%s = 1" % ft(q, q)), (q, p - q, ft(p - q, q))]


@rule("which is greater")
def r_compare(Qq):
    m = re.match(r"Which is greater: (\d+)/(\d+) or (\d+)/(\d+)\?$", Qq.text)
    if not m or Qq.n != 3:
        return None
    a, b, c, d = [int(g) for g in m.groups()]
    if not (0 < a <= b and 0 < c <= d) or max(b, d) > 24:
        return None
    l = b * d // math.gcd(b, d)
    x, y = a * (l // b), c * (l // d)
    if x == y or ft(a, b) not in Qq.answer and ft(c, d) not in Qq.answer:
        return None
    if Qq.answer.strip() != (ft(a, b) if x > y else ft(c, d)):
        raise ValueError("%s: answer key disagrees" % Qq.id)
    first, second = ft(a, b), ft(c, d)

    def lab(orig, top):
        return orig if orig == ft(top, l) else "%s = %s" % (orig, ft(top, l))

    before = fb([(b, a, first), (d, c, second)])
    relabel = fb([(b, a, lab(first, x)), (d, c, lab(second, y))])
    same = [fb([(l, x, lab(first, x)), (l, y, lab(second, y))])] if l <= 24 else []
    same.append(relabel)
    hl = ["b0" if x > y else "b1"]
    last_note = "%d is more than %d" % (max(x, y), min(x, y))
    # No figure before answering: strips drawn to scale would show which fraction is bigger.
    return entry(Qq, None, [
        w(before, "Pieces of different sizes. Cut both into %d" % l),
        [w(f, "Now every piece is the same size" if f is not relabel else "Both written with %d below" % l) for f in same],
        [w(f, last_note, hl) for f in same],
    ], origin="rule")


def quantity_bar(a, b, brace, label=None, note=None, hl=None):
    pieces = [seg(label, 1, "a" if i < a else "b") for i in range(b)]
    return bm([bar(pieces, brace=brace)], note, hl)


@rule("a/b of N")
def r_of(Qq):
    m = re.match(r"What is (\d+)/(\d+) of (\d+)\?$", Qq.text)
    if not m or Qq.n not in (2, 3):
        return None
    a, b, total = [int(g) for g in m.groups()]
    if not (0 < a < b <= 12) or total % b:
        return None
    one = total // b
    ans = one * a
    if Qq.answer.strip() != str(ans):
        raise ValueError("%s: answer key disagrees" % Qq.id)
    hi = ["b0s%d" % i for i in range(a)] if a <= 8 else None
    # The bank's steps: split into b equal parts, take a of them, (state the answer).
    take = ("One part is %d" % one) if a == 1 else "%d parts of %d: %d × %d = %d" % (a, one, one, a, ans)
    last = "%s of %d is %d" % (ft(a, b), total, ans)
    if total <= 60:
        figs = [
            setf(total, b, note="%d split into %d equal parts: %d in each" % (total, b, one)),
            setf(total, b, a, note=take, hl=["shaded"]),
            setf(total, b, a, note=last, hl=["shaded"]),
        ]
    else:
        figs = [
            quantity_bar(a, b, str(total), str(one), "%d ÷ %d = %d in each part" % (total, b, one)),
            quantity_bar(a, b, str(total), str(one), take, hi),
            quantity_bar(a, b, str(total), str(one), last, hi),
        ]
    if Qq.n == 2:
        # Two steps: the second both takes the parts and states the answer.
        figs = [figs[0], [w(figs[1], last, ["shaded"] if total <= 60 else hi)]]
    return entry(Qq, quantity_bar(a, b, str(total), note="%s of %d = ?" % (ft(a, b), total)), figs, origin="rule")


@rule("gives away a/b, how many left")
def r_left(Qq):
    m = re.match(r"([A-Z][a-z]+) has (\d+) marbles\. \1 gives (\d+)/(\d+) of them to a friend\. How many marbles does \1 have left\?$", Qq.text)
    if not m or Qq.n != 3:
        return None
    total, a, b = int(m.group(2)), int(m.group(3)), int(m.group(4))
    if not (0 < a < b <= 12) or total % b:
        return None
    one = total // b
    given = one * a
    left = total - given
    if Qq.answer.strip() != str(left):
        raise ValueError("%s: answer key disagrees" % Qq.id)
    brace = "%d marbles" % total
    pieces = [seg(None, 1, "a" if i < a else "unknown") for i in range(b)]
    split = "%d ÷ %d = %d marbles in each group" % (total, b, one)
    gives = ("1 group is given away: %d marbles" % given) if a == 1 else \
        "%d groups are given away: %d × %d = %d marbles" % (a, one, a, given)
    hi = ["b0s%d" % i for i in range(a)] if a <= 8 else None
    # The bank's steps: split into b equal groups, give away a of them, subtract.
    if total <= 60:
        first = setf(total, b, item="marbles", note=split)
        second = setf(total, b, a, item="marbles", note=gives, hl=["shaded"])
    else:
        each = [seg(str(one), 1, "a" if i < a else "b") for i in range(b)]
        first = bm([bar(each, brace=brace)], split)
        second = bm([bar(each, brace=brace)], gives, hi)
    third = bm([bar([seg("%d given" % given, a, "a"), seg("%d left" % left, b - a, "b")], brace=brace)],
               "%d − %d = %d marbles left" % (total, given, left), ["b0s1"])
    return entry(Qq, bm([bar(pieces, brace=brace)], "%s given away. How many are left?" % ft(a, b)),
                 [first, second, third], origin="rule")


@rule("gives away a/b of the sweets")
def r_sweets(Qq):
    m = re.match(r"([A-Z][a-z]+) has (\d+) sweets and gives away (\d+)/(\d+) of them\. How many sweets does \1 give away\?$", Qq.text)
    if not m or Qq.n != 3:
        return None
    total, a, b = int(m.group(2)), int(m.group(3)), int(m.group(4))
    if not (0 < a < b <= 12) or total % b:
        return None
    one = total // b
    given = one * a
    brace = "%d sweets" % total
    before = quantity_bar(a, b, brace, note="%s given away = ?" % ft(a, b))
    groups_note = "%d of the %d groups %s given away" % (a, b, "is" if a == 1 else "are")
    work = ("One group is %d sweets" % given) if a == 1 else "%d × %d = %d sweets given away" % (a, one, given)
    plain = "%d sweets are given away" % given
    hi = ["b0s%d" % i for i in range(a)] if a <= 8 else None
    if total <= 60:
        figs = [
            setf(total, b, item="sweets", note="%d sweets in %d equal groups" % (total, b)),
            setf(total, b, a, item="sweets", note=groups_note, hl=["shaded"]),
            [setf(total, b, a, item="sweets", note=work, hl=["shaded"]),
             setf(total, b, a, item="sweets", note=plain, hl=["shaded"])],
        ]
    else:
        figs = [
            quantity_bar(a, b, brace, note="%d sweets in %d equal groups" % (total, b)),
            quantity_bar(a, b, brace, note=groups_note, hl=hi),
            [quantity_bar(a, b, brace, str(one), work, hi), quantity_bar(a, b, brace, note=plain, hl=hi)],
        ]
    return entry(Qq, before, figs, origin="rule")


@rule("a/n + b/n")
def r_add_like(Qq):
    m = re.match(r"Simplify: (\d+)/(\d+) \+ (\d+)/(\d+)$", Qq.text)
    if not m or Qq.n != 2:
        return None
    a, d1, b, d2 = [int(g) for g in m.groups()]
    if d1 != d2 or not (0 < a <= d1 and 0 < b <= d1) or d1 > 24:
        return None
    top = a + b
    res = Fraction(top, d1)
    p, q = res.numerator, res.denominator
    raw = ft(top, d1)
    before = fb([(d1, a, ft(a, d1)), (d1, b, ft(b, d1))])
    if top <= d1:
        first = fb([(d1, top, raw)], "%d + %d = %d pieces shaded" % (a, b, top), ["b0"])
    else:
        first = [fb(whole_and_rest(top, d1), "%d + %d = %d pieces: one whole and %d more" % (a, b, top, top - d1)),
                 w(before, "%d + %d = %d pieces: more than one whole" % (a, b, top))]
    if p == q:
        second = fb([(d1, d1, "%s = 1" % raw)], "Every piece is shaded: one whole", ["b0"])
    elif p < q and (p, q) != (top, d1):
        second = fb([(d1, top, raw), (q, p, ft(p, q))], "The same amount, in bigger pieces", ["b1"])
    elif p < q:
        second = fb([(d1, top, raw)], "%s is already in its simplest form" % raw, ["b0"])
    elif q < p < 2 * q:
        second = [fb(whole_and_rest(p, q), "%s = %s: one whole and %s" % (raw, ft(p, q), ft(p - q, q))), None]
    else:
        second = None
    return entry(Qq, before, [first, second], origin="rule")


@rule("equivalent fraction, missing top")
def r_missing(Qq):
    m = re.match(r"Find the missing number: (\d+)/(\d+) = \?/(\d+)$", Qq.text)
    if not m or Qq.n != 3:
        return None
    a, b, d = [int(g) for g in m.groups()]
    if d % b or not (0 < a <= b) or d == b or b > 24:
        return None
    k = d // b
    if Qq.answer.strip() != str(a * k):
        raise ValueError("%s: answer key disagrees" % Qq.id)
    # The bank's steps: the bottom was multiplied by k, do the same to the top, state the answer.
    cut = "Each piece is cut into %d: %d × %d = %d pieces" % (k, b, k, d)
    equal = "%s = %s" % (ft(a, b), ft(a * k, d))
    if d <= 24:
        before = fb([(b, a, ft(a, b)), (d, 0, "?/%d" % d)])
        done = fb([(b, a, ft(a, b)), (d, a * k, ft(a * k, d))])
        figs = [w(before, cut, ["b1"]),
                w(done, "Same amount shaded: %d × %d = %d" % (a, k, a * k), ["b1"]),
                w(done, "%s, so the missing number is %d" % (equal, a * k), ["b1"])]
    else:
        # Too many pieces to draw: keep the one strip and say what happens to it.
        before = fb([(b, a, ft(a, b))], "%s = ?/%d" % (ft(a, b), d))
        done = fb([(b, a, equal)])
        figs = [w(before, cut),
                w(done, "%d × %d = %d of the small pieces are shaded" % (a, k, a * k), ["b0"]),
                w(done, "The missing number is %d" % (a * k), ["b0"])]
    return entry(Qq, before, figs, origin="rule")


@rule("a/b plus or minus c/d")
def r_arith(Qq):
    m = re.match(r"What is (\d+)/(\d+) ([+−-]) (\d+)/(\d+)\?$", Qq.text)
    if not m or Qq.n not in (2, 3):
        return None
    a, b, c, d = int(m.group(1)), int(m.group(2)), int(m.group(4)), int(m.group(5))
    plus = m.group(3) == "+"
    sign = "+" if plus else "−"
    l = b * d // math.gcd(b, d)
    if l > 24 or a > b or c > d:
        return None
    x, y = a * (l // b), c * (l // d)
    top = x + y if plus else x - y
    if top <= 0:
        return None
    res = Fraction(top, l)
    p, q = res.numerator, res.denominator
    answer = str(p) if q == 1 else ft(p, q)
    if Qq.answer.strip() != answer:
        raise ValueError("%s: answer key %r, computed %s" % (Qq.id, Qq.answer, answer))

    def lab(orig, t):
        return orig if orig == ft(t, l) else "%s = %s" % (orig, ft(t, l))

    sum_text = "%s %s %s" % (ft(a, b), sign, ft(c, d))
    before = fb([(b, a, ft(a, b)), (d, c, ft(c, d))], "%s = ?" % sum_text)
    same = fb([(l, x, lab(ft(a, b), x)), (l, y, lab(ft(c, d), y))], "Now every piece is the same size")
    count = "%d %s %d = %d pieces" % (x, sign, y, top)
    if top <= l:
        combine = fb([(l, top, ft(top, l))], count, ["b0"])
    else:
        combine = [fb(whole_and_rest(top, l), "%s: one whole and %d more" % (count, top - l)),
                   w(same, "%s: more than one whole" % count)]
    raw = ft(top, l)
    if p == q:
        final = fb([(l, l, "%s = 1" % raw)], "Every piece is shaded: one whole", ["b0"])
    elif p < q and q != l:
        final = fb([(l, top, raw), (q, p, ft(p, q))], "The same amount, in bigger pieces", ["b1"])
    elif p < q:
        final = fb([(l, top, raw)], "%s = %s" % (sum_text, raw), ["b0"])
    elif q < p < 2 * q:
        final = [fb(whole_and_rest(p, q), "%s = %s: more than one whole" % (sum_text, ft(p, q))),
                 w(same, "%s = %s: more than one whole" % (sum_text, ft(p, q)))]
    else:
        final = None
    seq = ([same] if b != d else []) + [combine]
    while len(seq) < Qq.n:
        seq.append(final)
    return entry(Qq, before, seq, origin="rule")


def build():
    questions = load(NODE)
    out, rule_of = {}, {}
    for q in questions:
        Qq = Q(q)
        if q["id"] in OWN:
            e = OWN[q["id"]](Qq)
            if e:
                if e["origin"] != "authored":
                    raise ValueError(q["id"])
                out[q["id"]], rule_of[q["id"]] = e, "own"
            continue
        for name, fn in RULES:
            e = fn(Qq)
            if e:
                out[q["id"]], rule_of[q["id"]] = e, name
                break
    missing = [i for i in OWN if i not in {q["id"] for q in questions}]
    if missing:
        raise ValueError("not in this topic: %s" % missing)
    return questions, out, rule_of


if __name__ == "__main__":
    questions, out, rule_of = build()
    print("wrote", write("g4-%s.json" % NODE, out))
    report(NODE, questions, out, rule_of, sys.argv[1] if len(sys.argv) > 1 else None)
    left_out = [q["id"] for q in questions if q["id"] not in out]
    print("  no visual (%d): %s" % (len(left_out), " ".join(left_out)))
