"""Grade 4 fractions rules: comparing two fractions, a missing top number, a fraction of an
amount, and the marbles and sweets stories."""
from math import gcd

from g4_gr4_fractions_lib import (B, FIG, MARKT, NOTE, NOTET, TA, W, bars, cap, choose, fr, lesson, option_texts,
                                  pick, pieces)


def compare(q, a, b, c, d):
    qid = q["id"]
    big = b * d // gcd(b, d)
    m1, m2 = big // b, big // d
    aa, cc = a * m1, c * m2
    assert b != d and aa != cc, qid
    fa, fc = fr(a, b), fr(c, d)
    pb, pd, pl = pieces(b), pieces(d), pieces(big)
    first_wins = aa > cc
    beats = []

    beats.append(B(pick(qid, "open", [
        "Which is greater, %s or %s? Let's find out." % (fa, fc),
        "Two fractions, %s and %s. We want the greater one." % (fa, fc),
    ]), W("l1", "Which is greater: %d/%d or %d/%d?" % (a, b, c, d), "given", True)))

    beats.append(B(pick(qid, "draw", [
        "Here they are as two bars of the same length. The first is cut into %d pieces with %d shaded. The second is cut into %d pieces with %d shaded." % (b, a, d, c),
        "Let's draw them as two bars, both the same length. One has %d pieces with %d shaded, and the other has %d pieces with %d shaded." % (b, a, d, c),
        "A picture first. Two equal bars: the top one cut into %d with %d shaded, the bottom one cut into %d with %d shaded." % (b, a, d, c),
    ]), FIG("fig", bars((b, a, "%d/%d" % (a, b)), (d, c, "%d/%d" % (c, d))))))

    if a == c:
        beats.append(B(
            "Both tops are %d. Does that mean the two fractions are equal?" % a,
            ask=choose(qid, "a1", "No, the pieces are different sizes", ["Yes, same top means same amount"],
                       "Look at the bars. %s and %s are different sizes, so %d of one is not the same as %d of the other." % (cap(pb), pd, a, a))))
    else:
        beats.append(B(
            pick(qid, "ask1", ["Can we just compare the top numbers, %d and %d?" % (a, c),
                               "Is it fair to compare the tops, %d and %d, straight away?" % (a, c)]),
            ask=choose(qid, "a1", "No, the pieces are different sizes", ["Yes, the bigger top always wins"],
                       "Look at the bars. %s and %s are different sizes, so counting pieces is not fair yet. First the pieces must be the same size." % (cap(pb), pd))))

    if big == b:
        beats.append(B(
            "So let's cut both bars into the same size of piece. %d goes into %d, so we can turn the %s into %s." % (d, b, pd, pb),
            W("l2", "%d × %d = %d" % (d, m2, b))))
    elif big == d:
        beats.append(B(
            "So let's cut both bars into the same size of piece. %d goes into %d, so we can turn the %s into %s." % (b, d, pb, pd),
            W("l2", "%d × %d = %d" % (b, m1, d))))
    else:
        beats.append(B(
            "So let's cut both bars into the same size of piece. We need a number that %d and %d both go into, and the smallest one is %d." % (b, d, big),
            W("l2", "%d × %d = %d" % (b, m1, big)), W("l3", "%d × %d = %d" % (d, m2, big))))

    new_fig = FIG("fig", bars((big, aa, "%d/%d" % (aa, big)), (big, cc, "%d/%d" % (cc, big)))) if big <= 24 else None
    style = pick(qid, "conv", [0, 1])

    def convert(lead, f, top, mult, new_top):
        if style == 0:
            return "%s %s, the bottom was multiplied by %d, so the top must be too. %d times %d is %d, so %s is %d over %d." % (
                lead, f, mult, top, mult, new_top, f, new_top, big)
        return "%s %s, whatever we do to the bottom we do to the top. So we multiply the top by %d as well: %d times %d is %d. That makes %d over %d." % (
            lead, f, mult, top, mult, new_top, new_top, big)

    if m1 > 1:
        say = convert("For", fa, a, m1, aa)
        board = [W("c1", "%d/%d = %d/%d" % (a, b, aa, big)), NOTE("c1", "%d/%d" % (a, b), "× %d top and bottom" % m1)]
        if m2 == 1:
            say += " And %s stays as it is." % fc
            if new_fig:
                board.append(new_fig)
        beats.append(B(say, *board))
    if m2 > 1:
        say = convert("For" if m1 == 1 else "And for", fc, c, m2, cc)
        board = [W("c2", "%d/%d = %d/%d" % (c, d, cc, big)), NOTE("c2", "%d/%d" % (c, d), "× %d top and bottom" % m2)]
        if m1 == 1:
            say += " And %s stays as it is." % fa
        if new_fig:
            board.append(new_fig)
        beats.append(B(say, *board))

    hi, lo = max(aa, cc), min(aa, cc)
    beats.append(B(
        "Now every piece is the same size: they are all %s. Which is greater, %d over %d or %d over %d?" % (pl, aa, big, cc, big),
        ask=choose(qid, "a2", "%d/%d" % (hi, big), ["%d/%d" % (lo, big), "they are equal"],
                   "The pieces are the same size now, so just count them. %d pieces is more than %d pieces." % (hi, lo))))

    win, lose = ((a, b), (c, d)) if first_wins else ((c, d), (a, b))
    fw = fr(*win)
    ans = "%d/%d > %d/%d" % (win[0], win[1], lose[0], lose[1])
    if (hi, big) != win:
        verdict = pick(qid, "verdict", [
            "%d is more than %d, so %d over %d is greater. And %d over %d is just %s cut into smaller pieces." % (hi, lo, hi, big, hi, big, fw),
            "%d pieces beat %d pieces. And %d over %d is only another name for %s, so %s is the greater fraction." % (hi, lo, hi, big, fw, fw),
        ])
    else:
        verdict = "%d is more than %d, so %s is the greater fraction." % (hi, lo, fw)
    beats.append(B(
        verdict,
        W("l5", "%d/%d > %d/%d" % (hi, big, lo, big)),
        W("l6", ans, "answer"), MARKT("l6", TA(ans, "%d/%d" % win, 0), "circle")))

    if a == c:
        small_b, large_b = min(b, d), max(b, d)
        beats.append(B("Did you notice? Both tops were %d, but %s are bigger pieces than %s. Same top, smaller bottom, greater fraction." % (
            a, pieces(small_b), pieces(large_b))))
    elif win[0] < lose[0]:
        beats.append(B("And look: %s has the smaller top, yet it is the greater fraction. That is why we never compare tops until the pieces match." % fw))
    else:
        beats.append(B("The picture agrees. The bar for %s has more of it shaded." % fw))
    beats.append(B(pick(qid, "sum", [
        "So to compare fractions: make the pieces the same size, then compare the tops.",
        "Keep this plan. Same bottom number first, and only then compare the tops.",
    ])))
    return lesson(beats, "rule")


def missing_top(q, a, b, d):
    qid = q["id"]
    m = d // b
    aa = a * m
    assert d % b == 0 and m > 1, qid
    fa = fr(a, b)
    drawn = d <= 24
    l1 = "%d/%d = ?/%d" % (a, b, d)
    num = TA(l1, str(a), 0)
    den = TA(l1, str(b), len(str(a)) + 1)
    beats = []

    beats.append(B(pick(qid, "open", [
        "Two equal fractions, but one top number is hiding. %s equals something over %d." % (cap(fa), d),
        "%s equals something over %d. Let's find the missing top number." % (cap(fa), d),
    ]), W("l1", l1, "given")))

    if drawn:
        beats.append(B(
            "Here is %s as a bar: %d pieces, %d shaded. Underneath is the very same bar, cut into %d smaller pieces." % (fa, b, a, d),
            FIG("fig", bars((b, a, "%d/%d" % (a, b)), (d, 0, "?/%d" % d)))))
    else:
        beats.append(B(
            "Here is %s as a bar: %d equal pieces, with %d shaded. To get %d pieces, each one has to be cut into smaller pieces." % (fa, b, a, d),
            FIG("fig", bars((b, a, "%d/%d" % (a, b))))))

    others = []
    for x in (d - b, m + 1, m - 1):
        if x != m and x > 1 and str(x) not in others:
            others.append(str(x))
    beats.append(B(
        "Start with the bottoms. What was %d multiplied by to make %d?" % (b, d),
        ask=choose(qid, "a1", str(m), others[:2],
                   "Use the %d times table. %d times %d is %d, so the bottom was multiplied by %d." % (b, b, m, d, m))))

    beats.append(B(
        "%d times %d is %d. In the picture, that means every piece was cut into %d smaller pieces." % (b, m, d, m),
        W("l2", "%d × %d = %d" % (b, m, d)), NOTET("l1", den, "× %d" % m, "below")))

    beats.append(B(
        "So to keep the two fractions equal, what must happen to the top?",
        ask=choose(qid, "a2", "multiply it by %d too" % m, ["add %d to it" % (d - b), "leave it as %d" % a],
                   "Every shaded piece was cut into %d as well. So the top must be multiplied by the same number, %d." % (m, m))))

    board = [NOTET("l1", num, "× %d" % m), W("l3", "%d × %d = %d" % (a, m, aa))]
    if drawn:
        board.append(FIG("fig", bars((b, a, "%d/%d" % (a, b)), (d, aa, "%d/%d" % (aa, d)))))
    beats.append(B("The top gets the same treatment. %d times %d is %d." % (a, m, aa), *board))

    ans = "%d/%d = %d/%d" % (a, b, aa, d)
    beats.append(B(
        "So %s equals %d over %d. The missing number is %d." % (fa, aa, d, aa),
        W("l4", ans, "answer"), MARKT("l4", TA(ans, str(aa), ans.find("= ") + 2), "circle")))

    if drawn:
        beats.append(B("Check with the picture. The same amount of bar is shaded in both. Only the size of the pieces changed."))
    else:
        beats.append(B(
            "Check it backwards. Divide %d and %d by %d, and we are back at %s." % (aa, d, m, fa),
            W("chk", "%d ÷ %d = %d" % (aa, m, a)), W("chk2", "%d ÷ %d = %d" % (d, m, b))))
    beats.append(B(pick(qid, "sum", [
        "So for equal fractions: whatever you multiply the bottom by, multiply the top by the same number.",
        "The rule to keep: top and bottom always get multiplied by the same number.",
    ])))
    return lesson(beats, "rule")


def quantity_fig(n, b, shaded, item=None, unit=None):
    """N things shared into b equal groups: counters when they fit, a bar when they do not."""
    if n <= 60:
        spec = {"kind": "set", "total": n, "groups": b}
        if shaded:
            spec["shadedGroups"] = shaded
        if item:
            spec["item"] = item
        return spec
    segs = [{"units": 1, "label": str(unit) if unit else "?", "tone": "a" if i < shaded else "b"} for i in range(b)]
    return {"kind": "barModel", "bars": [{"segments": segs, "brace": "%d %s" % (n, item) if item else str(n)}]}


def fraction_of(q, a, b, n, who=None):
    """'What is a/b of n?', or with `who`: '<who> has n sweets and gives away a/b of them'."""
    qid = q["id"]
    u = n // b
    p = a * u
    assert u * b == n, qid
    f = fr(a, b)
    counters = n <= 60
    group = "group" if counters else "part"
    item = "sweets" if who else None
    things = "sweets" if who else "counters"
    beats = []

    if who:
        l1 = "%d/%d of %d sweets = ?" % (a, b, n)
        beats.append(B(pick(qid, "open", [
            "%s has %d sweets and gives away %s of them. How many sweets is that?" % (who, n, f),
            "Here is our story. %s has %d sweets, and %s of them are given away. We want to know how many." % (who, n, f),
        ]), W("l1", l1, "given", True)))
    else:
        l1 = "%d/%d of %d = ?" % (a, b, n)
        beats.append(B(pick(qid, "open", [
            "Here is our question. What is %s of %d?" % (f, n),
            "We need %s of %d. Let's work it out together." % (f, n),
            "%s of %d. That little word, of, means we are taking a part of the %d." % (cap(f), n, n),
        ]), W("l1", l1, "given")))
    den = TA(l1, str(b), len(str(a)) + 1)
    num = TA(l1, str(a), 0)

    if counters:
        say = pick(qid, "draw", [
            "Let's draw it. Here are %d %s. The bottom number, %d, tells us to share them into %d equal groups." % (n, things, b, b),
            "A picture helps. These are %d %s, and the bottom number, %d, says share them into %d equal groups." % (n, things, b, b),
        ])
    else:
        whole = "%d sweets" % n if who else "%d" % n
        say = pick(qid, "draw", [
            "Let's draw it. One long bar stands for all %s. The bottom number, %d, tells us to cut it into %d equal parts." % (whole, b, b),
            "A picture helps. This bar is all %s, and the bottom number, %d, says cut it into %d equal parts." % (whole, b, b),
        ])
    beats.append(B(say, FIG("fig", quantity_fig(n, b, 0, item)), NOTET("l1", den, "%d equal %ss" % (b, group), "below")))

    others = ["multiply %d by %d" % (n, b), ("divide %d by %d" % (n, a)) if a > 1 else ("take %d away from %d" % (b, n))]
    beats.append(B(
        pick(qid, "ask1", ["So what is our first job with the %d?" % n, "What do we do to the %d first?" % n]),
        ask=choose(qid, "a1", "divide %d by %d" % (n, b), others,
                   "The bottom number, %d, tells us how many equal %ss to make. Sharing into %d equal %ss means dividing by %d." % (b, group, b, group, b))))

    board = [W("l2", "%d ÷ %d = %d" % (n, b, u))]
    if not counters:
        board.append(FIG("fig", quantity_fig(n, b, 0, item, u)))
    beats.append(B("%d divided by %d is %d. So each %s %s %d." % (n, b, u, group, "holds" if counters else "is worth", u), *board))

    if who:
        closing = pick(qid, "ans", ["So %s gives away %d sweets." % (who, p), "There it is. %s gives away %d sweets." % (who, p)])
    else:
        closing = pick(qid, "ans", ["So %s of %d is %d." % (f, n, p), "There it is. %s of %d is %d." % (cap(f), n, p)])
    ans = "%d/%d of %d = %d" % (a, b, n, p)
    if a > 1:
        wrong = [t for t in option_texts(q) if t not in (str(p), str(u))]
        beats.append(B(
            "Now the top number, %d. It tells us how many of those %ss to take. So what is %s of %d?" % (a, group, f, n),
            ask=choose(qid, "a2", str(p), [str(u)] + wrong[:1],
                       "One %s is %d, and the top number says take %d of them. So we need %d times %d." % (group, u, a, a, u))))
        beats.append(B(
            "%d %ss of %d. %d times %d is %d." % (a, group, u, a, u, p),
            NOTET("l1", num, "take %d %ss" % (a, group)),
            FIG("fig", quantity_fig(n, b, a, item, u)),
            W("l3", "%d × %d = %d" % (a, u, p))))
        beats.append(B(closing, W("l4", ans, "answer"), MARKT("l4", TA(ans, str(p), ans.rfind(str(p))), "circle")))
    else:
        beats.append(B(
            "The top number is 1, so we take just 1 of those %ss." % group,
            NOTET("l1", num, "take 1 %s" % group),
            FIG("fig", quantity_fig(n, b, 1, item, u))))
        beats.append(B(closing, W("l3", ans, "answer"), MARKT("l3", TA(ans, str(u), ans.rfind(str(u))), "circle")))

    beats.append(B(
        "Let's check our %ss were fair. %d %ss of %d should give back %d, and %d times %d is %d. They were." % (group, b, group, u, n, b, u, n),
        W("chk", "%d × %d = %d" % (b, u, n))))
    if a > 1:
        beats.append(B(pick(qid, "sum", [
            "So, for a fraction of an amount: divide by the bottom number, then multiply by the top number.",
            "Here is the plan to keep. Share into the bottom number of groups, then take the top number of them.",
        ])))
    else:
        beats.append(B("So, for a fraction of an amount: divide by the bottom number, then multiply by the top. When the top is 1, the dividing does it all."))
    return lesson(beats, "rule")


def marbles_left(q, name, n, a, b):
    qid = q["id"]
    u = n // b
    g = a * u
    left = n - g
    assert u * b == n, qid
    f = fr(a, b)
    counters = n <= 60
    group = "group" if counters else "part"
    beats = []

    beats.append(B(pick(qid, "open", [
        "%s has %d marbles and gives away %s of them. We want to know how many are left." % (name, n, f),
        "Here is our story. %s has %d marbles, and %s of them go to a friend. How many does %s keep?" % (name, n, f, name),
    ]), W("l1", "%s: %d marbles, gives away %d/%d" % (name, n, a, b), "given", True)))

    if counters:
        say = "Let's draw the %d marbles. The bottom number is %d, so we share them into %d equal groups." % (n, b, b)
    else:
        say = "Let's draw all %d marbles as one long bar. The bottom number is %d, so we cut it into %d equal parts." % (n, b, b)
    beats.append(B(say, FIG("fig", quantity_fig(n, b, 0, "marbles"))))

    others = [str(n - b)]
    if a > 1 and n % a == 0 and n // a != u:
        others.append(str(n // a))
    elif b != u:
        others.append(str(b))
    else:
        others.append(str(n))
    beats.append(B(
        pick(qid, "ask1", ["How many marbles are in each %s?" % group, "So how many marbles does one %s hold?" % group]),
        ask=choose(qid, "a1", str(u), others,
                   "We are sharing %d marbles equally into %d %ss. Sharing equally is dividing, so we need %d divided by %d." % (n, b, group, n, b))))

    l2 = "%d ÷ %d = %d" % (n, b, u)
    board = [W("l2", l2)]
    if not counters:
        board.append(FIG("fig", quantity_fig(n, b, 0, "marbles", u)))
    beats.append(B(pick(qid, "unit", [
        "%d divided by %d is %d. So each %s holds %d marbles." % (n, b, u, group, u),
        "%d shared into %d equal %ss gives %d in each. So one %s is %d marbles." % (n, b, group, u, group, u),
    ]), *board))

    if a > 1:
        l3 = "%d × %d = %d" % (a, u, g)
        beats.append(B(
            pick(qid, "give", [
                "%s gives away %d of those %ss. %d times %d is %d marbles." % (name, a, group, a, u, g),
                "The top number is %d, so %d %ss go to the friend. %d times %d is %d marbles." % (a, a, group, a, u, g),
            ]),
            FIG("fig", quantity_fig(n, b, a, "marbles", u)),
            W("l3", l3), NOTET("l3", TA(l3, str(g), l3.rfind(str(g))), "given away", "below")))
    else:
        beats.append(B(
            "%s gives away 1 of those %ss, so %d marbles go to the friend." % (name, group, u),
            FIG("fig", quantity_fig(n, b, 1, "marbles", u)),
            NOTET("l2", TA(l2, str(u), l2.rfind(str(u))), "given away", "below")))

    beats.append(B(
        pick(qid, "ask2", [
            "Careful now. Read the question again: it asks how many are left. So what do we do with the %d?" % g,
            "Here is the trap. The question asks how many are left, not how many were given. What do we do with the %d?" % g,
        ]),
        ask=choose(qid, "a2", "take it away from %d" % n,
                   ["add it to %d" % n, "multiply it by %d" % b] if g == left else ["nothing, %d is the answer" % g, "add it to %d" % n],
                   "%d is how many marbles went to the friend. %s started with %d, so what is left is %d take away %d." % (g, name, n, n, g))))

    ans = "%d − %d = %d" % (n, g, left)
    beats.append(B(
        ("%d take away %d leaves %d. The same number again, because %s gave away exactly half and kept the other half." % (n, g, left, name))
        if g == left else pick(qid, "ans", [
            "%d minus %d is %d. So %s has %d marbles left." % (n, g, left, name, left),
            "%d take away %d leaves %d. %s keeps %d marbles." % (n, g, left, name, left),
        ]),
        W("l4", ans, "answer"), MARKT("l4", TA(ans, str(left), ans.rfind(str(left))), "circle")))

    rem = b - a
    if rem > 1:
        beats.append(B(
            "Let's check with the picture. %d %ss were not given away, and %d times %d is %d. It matches." % (rem, group, rem, u, left),
            W("chk", "%d × %d = %d" % (rem, u, left))))
    else:
        beats.append(B("Let's check with the picture. Just 1 %s was not given away, and one %s is %d marbles. It matches." % (group, group, u)))
    beats.append(B(pick(qid, "sum", [
        "So: find the fraction of the amount first. Then read the question once more, to see if it wants what was given or what is left.",
        "The plan: divide by the bottom number, multiply by the top, and then check what the question is really asking for.",
    ])))
    return lesson(beats, "rule")
