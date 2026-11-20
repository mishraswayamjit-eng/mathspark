"""Rules for the generated families in gr4_squares: 'Find the square root of N' and 'Find the square of N'."""
import re

from g4_gr4_numbers_lib import A, G, Q, W, b, build, opts, pick

RE_ROOT = re.compile(r"Find the square root of (\d+)\.$")
RE_SQUARE = re.compile(r"Find the square of (\d+)\.$")

ENDINGS = {0: [0], 1: [1, 9], 4: [2, 8], 9: [3, 7], 6: [4, 6], 5: [5]}


def square_root(q):
    m = RE_ROOT.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    n = int(m.group(1))
    r = int(round(n ** 0.5))
    assert r * r == n and opts(q)["ABCD".index(q["correctAnswer"])] == str(r), qid
    beats = [
        b(pick(qid, "open", [
            "We want the square root of %d. That means: which number, times itself, makes %d?" % (n, n),
            "The square root of %d is the number that, multiplied by itself, gives %d. Let us hunt for it." % (n, n),
        ]), G("√%d = ?" % n), W("? × ? = %d" % n)),
    ]
    if r <= 10:
        lo = r - 1
        beats.append(b("Let us try a number. %d times %d is %d. That is too small." % (lo, lo, lo * lo),
                       W("%d × %d = %d" % (lo, lo, lo * lo))))
        beats.append(b(
            "So try the next number, %d. What is %d times %d?" % (r, r, r),
            Q([str(n), str(2 * r), str(n - r)],
              "%d times %d means %d lots of %d, and that makes %d. Adding %d and %d gives only %d." % (r, r, r, r, n, r, r, 2 * r))))
        beats.append(b("%d times %d is %d. That is exactly our number!" % (r, r, n), W("%d × %d = %d" % (r, r, n))))
    else:
        lo = (r // 10) * 10
        hi = lo + 10
        d = n % 10
        ends = ENDINGS[d]
        beats.append(b(
            "%d times %d is %d, and %d times %d is %d. Our %d lies in between, so the answer is between %d and %d." % (lo, lo, lo * lo, hi, hi, hi * hi, n, lo, hi),
            W("%d × %d = %d" % (lo, lo, lo * lo)), W("%d × %d = %d" % (hi, hi, hi * hi))))
        right = " or ".join(str(e) for e in ends)
        others = [" or ".join(str(e) for e in v) for k, v in sorted(ENDINGS.items()) if k != d and k != 0][:2]
        beats.append(b(
            "Now a clever clue. %d ends in %d. Which last digit gives a square that ends in %d?" % (n, d, d),
            Q([right] + others,
              "Square each digit and look at the last digit of the result. Only %s gives a square that ends in %d." % (right, d))))
        cands = [lo + e for e in ends]
        beats.append(b(
            " ".join("%d times %d is %d." % (e, e, e * e) for e in ends)
            + (" Both end in %d. So we try %s." % (d, " or ".join(str(c) for c in cands)) if len(ends) == 2
               else " So we try %d." % cands[0]),
            *([W("%d × %d = %d" % (e, e, e * e)) for e in ends]
              + [W("try: " + " or ".join(str(c) for c in cands))])))
        t, u = (r // 10) * 10, r % 10
        beats.append(b(
            "Try %d. %d times %d is %d, and %d times %d is %d. Together that is %d. That is our number!" % (r, r, t, r * t, r, u, r * u, n),
            W("%d × %d = %d" % (r, t, r * t)), W("%d × %d = %d" % (r, u, r * u)), W("%d × %d = %d" % (r, r, n))))
    beats.append(b("So the square root of %d is %d." % (n, r), A(str(r))))
    if n % 2 == 0:
        half = n // 2
        if half > 20:
            beats.append(b(
                "Careful: a square root is not a half. Half of %d is %d. But %d times just 2 is already %d, so %d times itself is far too big." % (n, half, half, n, half),
                W("%d × 2 = %d" % (half, n))))
        else:
            beats.append(b(
                "Careful: a square root is not a half. Half of %d is %d, and %d times %d is far too big." % (n, half, half, half),
                W("%d × %d = %d" % (half, half, half * half))))
    beats.append(b("So remember: a square root undoes squaring. Ask yourself which number, times itself, gives %d." % n))
    return build(qid, beats, origin="rule")


def square_of(q):
    m = RE_SQUARE.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    n = int(m.group(1))
    t, u = (n // 10) * 10, n % 10
    assert 10 < n < 100 and u > 0, qid
    sq = n * n
    assert opts(q)["ABCD".index(q["correctAnswer"])] == str(sq), qid
    beats = [
        b("We want the square of %d. Squaring a number means multiplying it by itself." % n, G("%d² = ?" % n)),
        b("So which sum is the square of %d?" % n,
          Q(["%d × %d" % (n, n), "%d × 2" % n, "%d + %d" % (n, n)],
            "Squaring means multiplying a number by itself. So the square of %d is %d times %d." % (n, n, n))),
        b("%d times %d is a big sum, so split the second %d into %d and %d." % (n, n, n, t, u),
          W("%d × %d = %d × %d + %d × %d" % (n, n, n, t, n, u))),
        b("%d times %d is %d." % (n, t, n * t), W("%d × %d = %d" % (n, t, n * t))),
        b("%d times %d is %d." % (n, u, n * u), W("%d × %d = %d" % (n, u, n * u))),
        b("Add the two parts. %d plus %d is %d." % (n * t, n * u, sq), W("%d + %d = %d" % (n * t, n * u, sq)), A(str(sq))),
        b("A quick check on the last digit: %d times %d is %d, so the square must end in %d. It does." % (u, u, u * u, (u * u) % 10)),
        b("Careful: %d is just %d doubled. Squaring is times itself, and that grows much faster." % (2 * n, n),
          W("%d × 2 = %d" % (n, 2 * n))),
    ]
    return build(qid, beats, origin="rule")


RULES = [square_root, square_of]


def rule_lessons(qs):
    out = {}
    for q in qs:
        if not re.match(r"(VAR|BOOST|PH3)", q["id"]):
            continue
        for rule in RULES:
            script = rule(q)
            if script:
                out[q["id"]] = script
                break
    return out
