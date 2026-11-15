"""Rules: comparing two fractions, finding a missing top number, and the plain "ax ± b = c" equations."""
from math import gcd

from fractions_lib import (B, BOTH, DIVIDE, FIG, MARKT, NOTE, NOTET, STRIKET, TA, W, bars, cap, choose, fr, lesson,
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


def equation(q, a, minus, b, c):
    qid = q["id"]
    r = c + b if minus else c - b
    v = r // a
    assert v * a == r, qid
    sign = "−" if minus else "+"
    was, undo = ("minus", "plus") if minus else ("plus", "minus")
    undo_verb = "add" if minus else "subtract"
    undo_sign = "+" if minus else "−"
    l1 = "%dx %s %d = %d" % (a, sign, b, c)
    term = "%s %d" % (sign, b)
    beats = []

    beats.append(B(pick(qid, "open", [
        "Here is our equation. %d x, %s %d, equals %d. Somewhere behind that x a number is hiding, and we are going to find it." % (a, was, b, c),
        "Let's solve this one. %d x, %s %d, equals %d. Our job is to get x all on its own." % (a, was, b, c),
        "%d x, %s %d, equals %d. There is a mystery number called x, and we are going to track it down." % (a, was, b, c),
    ]), W("l1", l1, "given")))

    first_ask = pick(qid, "ask1", [0, 1])
    if first_ask == 0:
        beats.append(B(
            "Think of the equals sign as a balance. Whatever we do to one side, we do to the other. So, what is in the way of the %d x?" % a,
            ask=choose(qid, "a1", "the %s" % term, ["the %d" % c, "the %d" % a],
                       "Look at the left side once more. The %d x has a %s %d hanging on to it. That is the first thing to clear away." % (a, was, b))))
    else:
        beats.append(B(
            "Think of the equals sign as a balance: both sides must stay level. First we clear away the %s %d. What undoes %s %d?" % (was, b, was, b),
            ask=choose(qid, "a1", "%s %d" % (undo_verb, b), ["%s %d" % ("subtract" if minus else "add", b), "divide by %d" % b],
                       "Adding and subtracting are partners: each one undoes the other. So to undo %s %d, we %s %d." % (was, b, undo_verb, b))))

    both = "add it to both sides" if minus else "subtract it from both sides"
    beats.append(B(
        ("To undo %s %d, we %s %d. And to keep the balance level, we %s." % (was, b, undo_verb, b, both)) if first_ask == 0 else
        ("So we %s %d. And to keep the balance level, we %s." % (undo_verb, b, both)),
        STRIKET("l1", TA(l1, term, l1.find(term)), "%s %d" % (undo_sign, b)), BOTH("l1", "%s %d" % (undo_sign, b))))

    beats.append(B(pick(qid, "do", [
        "On the left, %s %d and %s %d cancel each other out. On the right, %d %s %d makes %d." % (was, b, undo, b, c, undo, b, r),
        "The %s %d and the %s %d cancel on the left, leaving just %d x. On the right, %d %s %d is %d." % (was, b, undo, b, a, c, undo, b, r),
    ]), W("l2", "%dx = %d %s %d" % (a, c, undo_sign, b)), W("l3", "%dx = %d" % (a, r))))

    beats.append(B(
        pick(qid, "ask2", ["Nearly there. %d x means %d times x. What undoes times %d?" % (a, a, a),
                           "One step to go. %d x is %d times x. So what undoes times %d?" % (a, a, a)]),
        ask=choose(qid, "a2", "divide by %d" % a, ["subtract %d" % a, "multiply by %d" % a],
                   "Times and divide are partners. Whatever times does, divide undoes. So to undo times %d, we divide by %d." % (a, a))))

    beats.append(B("So we divide both sides by %d." % a, DIVIDE("l3", str(a))))

    ans = "x = %d" % v
    beats.append(B(
        "%d divided by %d is %d. So x equals %d. %s" % (r, a, v, v, pick(qid, "yay", ["There is our hidden number!", "Found it!", "That is our x."])),
        W("l4", ans, "answer"), MARKT("l4", TA(ans, ans, 0), "circle")))

    beats.append(B(
        "Good mathematicians always check. Put %d back in place of x. %d times %d is %d, and %d %s %d is %d. It works." % (v, a, v, r, r, was, b, c),
        W("l5", "%d × %d %s %d = %d" % (a, v, sign, b, c))))

    beats.append(B(pick(qid, "sum", [
        "So here is the plan for any equation like this. First clear away what is added or taken off. Then undo the times.",
        "Two moves, in this order: undo the plus or minus first, then undo the times. And always do the same to both sides.",
    ])))
    return lesson(beats, "rule", ("x", v))
