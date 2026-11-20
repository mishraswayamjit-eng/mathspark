"""Lessons by rule for the generated families in gr4_decimals.

One wording: "<Name> buys <n> <things> at Rs.<p> each and pays Rs.<paid>. How much change
does <Name> get back?"  The rule reads the numbers, computes every line and adapts the words.
"""
import re

from g4_gr4_decimals_lib import (ANS, B, FIG, GIVEN, NOTE, RING, UL, W, choose, figure_of, lesson, pick)

CHANGE = re.compile(r"^(\w+) buys (\d+) (\w+) at Rs\.(\d+) each and pays Rs\.(\d+)\. How much change does \w+ get back\?$")


def times_beats(qid, n, p, things):
    """n lots of p, the way a child does it in their head. Returns (beats, id of the line with the total)."""
    total = n * p
    if p == 10:
        say = pick(qid, "t10", [
            "%d lots of 10 is a friendly one. %d tens are %d." % (n, n, total),
            "Each one costs 10 rupees, so we count in tens. %d tens make %d." % (n, total),
        ])
        return [B(say, W("m1", "%d × %d = %d" % (n, p, total)))], "m1"
    if p < 10:
        say = pick(qid, "tt", [
            "%d %s at %d rupees each is %d lots of %d. From our tables, %d times %d is %d." % (n, things, p, n, p, n, p, total),
            "We need %d lots of %d. %d times %d is %d." % (n, p, n, p, total),
        ])
        return [B(say, W("m1", "%d × %d = %d" % (n, p, total)))], "m1"
    rest = p - 10
    a, b = n * 10, n * rest
    return [
        B("%d is 10 and %d, so we can do this in two easy bites. First, %d lots of 10 make %d." % (p, rest, n, a),
          W("m1", "%d × 10 = %d" % (n, a))),
        B("Then %d lots of %d make %d." % (n, rest, b), W("m2", "%d × %d = %d" % (n, rest, b))),
        B("Put the two bites together. %d plus %d makes %d." % (a, b, total),
          W("m3", "%d × %d = %d + %d = %d" % (n, p, a, b, total))),
    ], "m3"


def change_lesson(q):
    m = CHANGE.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    name, n, things, p, paid = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    total = n * p
    change = paid - total
    if change < 0:
        return None
    one = things[:-1] if things.endswith("s") else things

    beats = []
    beats.append(B(
        pick(qid, "open", [
            "%s buys %d %s, and each %s costs %d rupees. %s hands over %d rupees. We want to know how much money comes back." % (name, n, things, one, p, name, paid),
            "Here is a shop sum. %d %s at %d rupees each, and %s pays with %d rupees. How much change comes back?" % (n, things, p, name, paid),
        ]),
        GIVEN("q", "%d %s at Rs.%d each. Pays Rs.%d. Change = ?" % (n, things, p, paid)),
        FIG("f", figure_of(qid))))
    beats.append(B(
        pick(qid, "bar", [
            "The long bar is all the money %s paid. Part of it pays for the %s, and the piece with the question mark is the change. So, what should we find first?" % (name, things),
            "Look at the bar. The whole bar is the money %s paid. The %s take up part of it, and the change is the piece at the end. What do we need to find first?" % (name, things),
            "The picture shows the money %s paid as one long bar. Some of it goes on the %s, and what is left is the change. So where do we start?" % (name, things),
        ]),
        ask=choose(qid, "first", "the cost of all %d %s" % (n, things),
                   ["Rs.%d − Rs.%d" % (paid, p), "Rs.%d + Rs.%d" % (paid, p)],
                   "The shopkeeper wants money for all %d %s, not just one. So first we find what all of them cost together." % (n, things))))
    tb, last = times_beats(qid, n, p, things)
    beats += tb
    beats.append(B(
        pick(qid, "cost", [
            "So the %s cost %d rupees altogether. That is the part of the bar that stays in the shop." % (things, total),
            "So the whole bill is %d rupees. That much stays with the shopkeeper." % total,
        ]),
        NOTE(last, "= %d" % total, "the bill", "below")))
    beats.append(B(
        "%s paid %d rupees, and the bill is %d rupees. How do we find the change?" % (name, paid, total),
        ask=choose(qid, "second", "Rs.%d − Rs.%d" % (paid, total),
                   ["Rs.%d + Rs.%d" % (paid, total), "Rs.%d − Rs.%d" % (total, p)],
                   "Change is the money left over after the bill is paid. So we take the bill away from the money paid.")))
    if change == 0:
        sub = "%d take away %d leaves nothing at all." % (paid, total)
    elif change <= 10:
        sub = "Count up from %d to %d. It is just %d steps, so %d take away %d is %d." % (total, paid, change, paid, total, change)
    else:
        sub = pick(qid, "sub", [
            "Take the bill away from the money paid. %d take away %d leaves %d." % (paid, total, change),
            "Count up from %d to %d: that is a jump of %d. So %d take away %d is %d." % (total, paid, change, paid, total, change),
        ])
    beats.append(B(sub, W("s1", "Rs.%d − Rs.%d = Rs.%d" % (paid, total, change)), UL("s1", "= Rs.%d" % change)))
    beats.append(B(
        pick(qid, "ans", [
            "So %s gets %d rupees back." % (name, change),
            "So the change is %d rupees. That is what %s gets back." % (change, name),
        ]),
        ANS("a", "Change = Rs.%d" % change, label=True), RING("a", "Rs.%d" % change)))
    beats.append(B(
        "Let's check. The bill, %d, plus the change, %d, makes %d. That is exactly what %s paid." % (total, change, paid, name),
        W("c", "%d + %d = %d" % (total, change, paid))))
    beats.append(B(pick(qid, "sum", [
        "So for change, there are two steps. First find the whole bill, then take it away from the money paid.",
        "Remember the plan for change: multiply to find the bill, then subtract the bill from the money paid.",
    ])))
    return lesson(beats, "rule")


def rule_for(q):
    """(name of the rule, lesson) or None."""
    found = change_lesson(q)
    if found:
        return "change from a shop", found
    return None
