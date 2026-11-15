"""Rules: adding and subtracting fractions (same bottom number, and one bottom a multiple of the other)."""
from math import gcd

from fractions_lib import B, FIG, MARK, MARKT, NOTE, NOTET, STRIKET, TA, W, bars, cap, choose, fr, lesson, pick, pieces


def _factor_choices(s, b, g):
    cands = [d for d in range(2, 13) if d != g and not (s % d == 0 and b % d == 0)]
    pref = [d for d in cands if s % d == 0 or b % d == 0]
    rest = [d for d in cands if d not in pref]
    return [str(x) for x in (pref + rest)[:2]]


def _pl(n):
    return "1 piece" if n == 1 else "%d pieces" % n


def simplify_beats(qid, line_id, line_text, s, b, next_id):
    """Two beats that divide a common factor out of s/b, which is the last fraction on `line_text`."""
    g = gcd(s, b)
    p, q = s // g, b // g
    assert g > 1 and q > 1
    pos = line_text.rfind("%d/%d" % (s, b))
    top = TA(line_text, str(s), pos)
    bottom = TA(line_text, str(b), pos + len(str(s)) + 1)
    ask = B(
        pick(qid, "simp", [
            "%d over %d is right, but we can make it simpler. What is the biggest number that divides both %d and %d?" % (s, b, s, b),
            "We are not finished: %d over %d can be made simpler. What is the biggest number that goes into both %d and %d?" % (s, b, s, b),
        ]),
        ask=choose(qid, "simp", str(g), _factor_choices(s, b, g),
                   ("%d goes into %d, and the top is %d itself. So %d is the biggest number that goes into both." % (g, b, g, g)) if g == s else
                   ("Try the times tables. %d goes into %d, and %d goes into %d, and nothing bigger goes into both." % (g, s, g, b))))
    do = B(
        "So we divide the top and the bottom by %d. %d divided by %d is %d, and %d divided by %d is %d." % (g, s, g, p, b, g, q),
        STRIKET(line_id, top, "÷ %d" % g), STRIKET(line_id, bottom, "÷ %d" % g),
        W(next_id, "%d/%d = %d/%d" % (s, b, p, q)))
    return [ask, do], p, q


def like_fractions(q, a, b, c, plus, simplest_asked=False):
    qid = q["id"]
    s = a + c if plus else a - c
    sign = "+" if plus else "−"
    word = "plus" if plus else "take away"
    fa, fc = fr(a, b), fr(c, b)
    pc = pieces(b)
    l1 = "%d/%d %s %d/%d = ?" % (a, b, sign, c, b)
    beats = []

    if plus:
        opening = pick(qid, "open", ["Here is our sum. %s, plus %s." % (cap(fa), fc), "We are adding two fractions. %s, plus %s." % (cap(fa), fc)])
        if simplest_asked:
            opening += " And we must give the answer in its simplest form."
    else:
        opening = pick(qid, "open", ["Here is our question. %s, take away %s." % (cap(fa), fc), "This one is a take away. %s, take away %s." % (cap(fa), fc)])
    beats.append(B(opening, W("l1", l1, "given")))

    if plus:
        beats.append(B(
            "Let's draw them. Two bars, each cut into %d equal pieces. The first has %d shaded, and the second has %d." % (b, a, c),
            FIG("fig", bars((b, a, "%d/%d" % (a, b)), (b, c, "%d/%d" % (c, b))))))
        beats.append(B(
            "Every piece here is the same size. They are all %s. So when we add, what happens to the bottom number?" % pc,
            ask=choose(qid, "a1", "it stays %d" % b, ["it becomes %d" % (2 * b)],
                       "Careful, this is the classic slip. The bottom number is only the name of the pieces, %s. Adding more %s does not change their size, so the bottom stays %d." % (pc, pc, b))))
    else:
        beats.append(B(
            "Let's draw it. One bar cut into %d equal pieces, with %d of them shaded. We are going to take %d of those shaded pieces away." % (b, a, c),
            FIG("fig", bars((b, a, "%d/%d" % (a, b))))))
        beats.append(B(
            "Every piece here is the same size. They are all %s. So when we take some away, what happens to the bottom number?" % pc,
            ask=choose(qid, "a1", "it stays %d" % b, ["it becomes 0"],
                       "The bottom number is only the name of the pieces, %s. Taking some away does not change their size, so the bottom stays %d." % (pc, b))))

    l2 = "%d/%d %s %d/%d = (%d %s %d)/%d = %d/%d" % (a, b, sign, c, b, a, sign, c, b, s, b)
    bracket = "(%d %s %d)" % (a, sign, c)
    if plus:
        say = pick(qid, "count", [
            "So we only count the pieces. %s and %s make %d pieces." % (_pl(a), _pl(c), s),
            "So adding is just counting. %s, and %s more, is %d pieces." % (_pl(a), _pl(c), s),
        ])
        if s <= b:
            fig = bars((b, a, "%d/%d" % (a, b)), (b, c, "%d/%d" % (c, b)), (b, s, "%d/%d" % (s, b)))
        else:
            fig = bars((b, a, "%d/%d" % (a, b)), (b, c, "%d/%d" % (c, b)), (b, b, "%d/%d" % (b, b)), (b, s - b, "%d/%d" % (s - b, b)))
    else:
        say = pick(qid, "count", [
            "So we only count the pieces. %s, take away %d, leaves %d." % (_pl(a), c, s),
            "So taking away is just counting. Start with %s, remove %d, and %d are left." % (_pl(a), c, s) if s != 1 else
            "So taking away is just counting. Start with %s, remove %d, and 1 is left." % (_pl(a), c),
        ])
        fig = bars((b, a, "%d/%d" % (a, b)), (b, s, "%d/%d" % (s, b)))
    beats.append(B(
        say, W("l2", l2), MARK("l2", bracket, "box"),
        NOTET("l2", TA(l2, "/%d" % b, l2.find(")/") + 1), "same size pieces", "below"),
        FIG("fig", fig)))

    lhs = "%d/%d %s %d/%d" % (a, b, sign, c, b)
    if s == 0:
        beats.append(B("No pieces are left at all. And 0 over %d is simply 0." % b, W("l3", "0/%d = 0" % b)))
        ans = lhs + " = 0"
        beats.append(B(
            "So %s take away %s is 0. Take a number away from itself and nothing is left." % (fa, fc),
            W("l4", ans, "answer"), MARKT("l4", TA(ans, "0", len(ans) - 1), "circle")))
    elif s == b:
        beats.append(B(
            "We have %d over %d: every single piece of the bar. What is that worth?" % (b, b),
            ask=choose(qid, "a2", "1 whole", ["%d wholes" % b, "nothing"],
                       "When all %d of the %d pieces are shaded, the whole bar is full. So %d over %d is 1 whole." % (b, b, b, b))))
        ans = lhs + " = 1"
        beats.append(B(
            "%d over %d is exactly 1. So %s plus %s is 1 whole." % (b, b, fa, fc),
            W("l3", "%d/%d = 1" % (b, b)), W("l4", ans, "answer"), MARKT("l4", TA(ans, "1", len(ans) - 1), "circle")))
    else:
        if s > b:
            extra = s - b
            beats.append(B(
                "%d over %d. The top is bigger than the bottom, and that is fine. It means more than 1 whole: one full bar, and %d more %s." % (
                    s, b, extra, "piece" if extra == 1 else "pieces"),
                MARKT("l2", TA(l2, "%d/%d" % (s, b), l2.rfind("%d/%d" % (s, b))), "underline")))
        g = gcd(s, b)
        if g > 1:
            two, p, qq = simplify_beats(qid, "l2", l2, s, b, "l3")
            beats += two
            ans = lhs + " = %d/%d" % (p, qq)
            beats.append(B(
                "So %s %s %s is %s, in its simplest form." % (fa, word, fc, fr(p, qq)),
                W("l4", ans, "answer"), MARKT("l4", TA(ans, "%d/%d" % (p, qq), ans.rfind("%d/%d" % (p, qq))), "circle")))
        else:
            ans = lhs + " = %d/%d" % (s, b)
            beats.append(B(
                "Can we make %d over %d simpler? %d and %d share no factor except 1, so it is already in its simplest form." % (s, b, s, b),
                W("l3", ans, "answer"), MARKT("l3", TA(ans, "%d/%d" % (s, b), ans.rfind("%d/%d" % (s, b))), "circle")))
            beats.append(B("So %s %s %s is %s." % (fa, word, fc, fr(s, b))))

    if plus:
        beats.append(B(pick(qid, "chk", [
            "Quick check with the picture. Count the shaded pieces in the first two bars: %d and %d make %d. It matches." % (a, c, s),
            "Let's check against the picture. %d shaded pieces, and %d more, is %d pieces. Just what we wrote." % (a, c, s),
        ])))
        beats.append(B(pick(qid, "sum", [
            "So when the bottom numbers match: add the tops, keep the bottom, and then simplify if you can.",
            "Remember it like this. Same size pieces? Just count them: add the tops, and the bottom stays as it is.",
        ])))
    else:
        beats.append(B(
            "Let's check by adding back. %d pieces, plus the %d we took away, is %d pieces again. It works." % (s, c, a),
            W("chk", "%d/%d + %d/%d = %d/%d" % (s, b, c, b, a, b))))
        beats.append(B("So when the bottom numbers match: subtract the tops, keep the bottom, and then simplify if you can."))
    return lesson(beats, "rule")


def unlike_subtract(q, a, b, c, d):
    """a/b − c/d where d goes into b."""
    qid = q["id"]
    assert b % d == 0 and b != d
    m = b // d
    cc = c * m
    s = a - cc
    assert s > 0
    fa, fc = fr(a, b), fr(c, d)
    pb, pd = pieces(b), pieces(d)
    l1 = "%d/%d − %d/%d = ?" % (a, b, c, d)
    beats = [
        B("Here is our question. %s, take away %s." % (cap(fa), fc), W("l1", l1, "given")),
        B("Let's draw them. One bar is cut into %d pieces, with %d shaded. The other is cut into %d pieces, with %d shaded." % (b, a, d, c),
          FIG("fig", bars((b, a, "%d/%d" % (a, b)), (d, c, "%d/%d" % (c, d))))),
        B("Look at the pieces. Can we take %s away from %s straight away?" % (fc, fa),
          ask=choose(qid, "a1", "No, the pieces are different sizes", ["Yes, subtract tops and bottoms"],
                     "Look at the two bars. %s are much bigger pieces than %s. We can only take away when the pieces are the same size." % (cap(pd), pb))),
        B("So let's turn the %s into %s. %d times %d is %d, so each piece gets cut into %d smaller pieces." % (pd, pb, d, m, b, m),
          W("l2", "%d × %d = %d" % (d, m, b))),
        B("Whatever we do to the bottom, we do to the top. %d times %d is %d, so %s is the same as %d over %d." % (c, m, cc, fc, cc, b),
          W("l3", "%d/%d = %d/%d" % (c, d, cc, b)), NOTE("l3", "%d/%d" % (c, d), "× %d top and bottom" % m),
          FIG("fig", bars((b, a, "%d/%d" % (a, b)), (b, cc, "%d/%d" % (cc, b))))),
    ]
    l4 = "%d/%d − %d/%d = %d/%d" % (a, b, cc, b, s, b)
    beats.append(B(
        "Now both are %s, so we just count. %d pieces, take away %d pieces, leaves %d. The bottom stays %d." % (pb, a, cc, s, b),
        W("l4", l4)))
    g = gcd(s, b)
    lhs = "%d/%d − %d/%d" % (a, b, c, d)
    if g > 1:
        two, p, qq = simplify_beats(qid, "l4", l4, s, b, "l5")
        beats += two
    else:
        p, qq = s, b
    ans = lhs + " = %d/%d" % (p, qq)
    beats.append(B(
        "So %s take away %s is %s." % (fa, fc, fr(p, qq)),
        W("l6", ans, "answer"), MARKT("l6", TA(ans, "%d/%d" % (p, qq), ans.rfind("%d/%d" % (p, qq))), "circle")))
    beats.append(B(
        "Let's check by adding back. %d over %d, plus %d over %d, is %d over %d. It works." % (s, b, cc, b, a, b),
        W("chk", "%d/%d + %d/%d = %d/%d" % (s, b, cc, b, a, b))))
    beats.append(B("So when the bottom numbers are different: make the pieces the same size first. Then count the tops, and keep the bottom."))
    return lesson(beats, "rule")
