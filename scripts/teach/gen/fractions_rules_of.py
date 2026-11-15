"""Rules: a fraction of a quantity ("What is 3/4 of 36?") and the marbles-left word problem."""
from fractions_lib import B, FIG, MARKT, NOTET, TA, W, cap, choose, fr, lesson, option_texts, pick


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


def fraction_of(q, a, b, n):
    qid = q["id"]
    u = n // b
    p = a * u
    f = fr(a, b)
    counters = n <= 60
    group = "group" if counters else "part"
    l1 = "%d/%d of %d = ?" % (a, b, n)
    den = TA(l1, str(b), len(str(a)) + 1)
    num = TA(l1, str(a), 0)
    beats = []

    beats.append(B(pick(qid, "open", [
        "Here is our question. What is %s of %d?" % (f, n),
        "We need %s of %d. Let's work it out together." % (f, n),
        "%s of %d. That little word, of, means we are taking a part of the %d." % (cap(f), n, n),
    ]), W("l1", l1, "given")))

    if counters:
        say = pick(qid, "draw", [
            "Let's draw it. Here are %d counters. The bottom number, %d, tells us to share them into %d equal groups." % (n, b, b),
            "A picture helps. These are %d counters, and the bottom number, %d, says share them into %d equal groups." % (n, b, b),
        ])
    else:
        say = pick(qid, "draw", [
            "Let's draw it. One long bar stands for all %d. The bottom number, %d, tells us to cut it into %d equal parts." % (n, b, b),
            "A picture helps. This bar is the whole %d, and the bottom number, %d, says cut it into %d equal parts." % (n, b, b),
        ])
    beats.append(B(say, FIG("fig", quantity_fig(n, b, 0)), NOTET("l1", den, "%d equal %ss" % (b, group), "below")))

    others = ["multiply %d by %d" % (n, b), ("divide %d by %d" % (n, a)) if a > 1 else ("take %d away from %d" % (b, n))]
    beats.append(B(
        pick(qid, "ask1", ["So what is our first job with the %d?" % n, "What do we do to the %d first?" % n]),
        ask=choose(qid, "a1", "divide %d by %d" % (n, b), others,
                   "The bottom number, %d, tells us how many equal %ss to make. Sharing into %d equal %ss means dividing by %d." % (b, group, b, group, b))))

    board = [W("l2", "%d ÷ %d = %d" % (n, b, u))]
    if not counters:
        board.append(FIG("fig", quantity_fig(n, b, 0, unit=u)))
    beats.append(B("%d divided by %d is %d. So each %s %s %d." % (n, b, u, group, "holds" if counters else "is worth", u), *board))

    if a > 1:
        wrong = [t for t in option_texts(q) if t not in (str(p), str(u))]
        beats.append(B(
            "Now the top number, %d. It tells us how many of those %ss to take. So what is %s of %d?" % (a, group, f, n),
            ask=choose(qid, "a2", str(p), [str(u)] + wrong[:1],
                       "One %s is %d, and the top number says take %d of them. So we need %d times %d." % (group, u, a, a, u))))
        beats.append(B(
            "%d %ss of %d. %d times %d is %d." % (a, group, u, a, u, p),
            NOTET("l1", num, "take %d %ss" % (a, group)),
            FIG("fig", quantity_fig(n, b, a, unit=u)),
            W("l3", "%d × %d = %d" % (a, u, p))))
        ans = "%d/%d of %d = %d" % (a, b, n, p)
        beats.append(B(
            pick(qid, "ans", ["So %s of %d is %d." % (f, n, p), "There it is. %s of %d is %d." % (cap(f), n, p)]),
            W("l4", ans, "answer"), MARKT("l4", TA(ans, str(p), ans.rfind(str(p))), "circle")))
    else:
        beats.append(B(
            "The top number is 1, so we take just 1 of those %ss." % group,
            NOTET("l1", num, "take 1 %s" % group),
            FIG("fig", quantity_fig(n, b, 1, unit=u))))
        ans = "%d/%d of %d = %d" % (a, b, n, u)
        beats.append(B(
            pick(qid, "ans", ["So %s of %d is %d." % (f, n, u), "There it is. %s of %d is %d." % (cap(f), n, u)]),
            W("l3", ans, "answer"), MARKT("l3", TA(ans, str(u), ans.rfind(str(u))), "circle")))

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
        ask=choose(qid, "a2", "take it away from %d" % n, ["nothing, %d is the answer" % g, "add it to %d" % n],
                   "%d is how many marbles went to the friend. %s started with %d, so what is left is %d take away %d." % (g, name, n, n, g))))

    ans = "%d − %d = %d" % (n, g, left)
    beats.append(B(
        pick(qid, "ans", [
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
