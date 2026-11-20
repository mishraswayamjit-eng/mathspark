"""Lessons by rule for the generated families of gr4_ages (see g4_gr4_ages.py)."""
import re

from g4_gr4_ratio_lib import (A, C, G, N, U, W, beat, choose, lesson, pick)

DIFF = re.compile(r"^(\w+) is (\d+) years old and (\w+) is (\d+) years old\. What was the difference in their ages (\d+) years ago\?$")
SUM = re.compile(r"^(\w+) is (\d+) years old and (\w+) is (\d+) years old\. What will be the sum of their ages after (\d+) years\?$")


def difference(q, m):
    qid = q["id"]
    x, p, y, r, k = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    assert p != r and min(p, r) - k >= 0
    p2, r2 = p - k, r - k
    big, small = max(p, r), min(p, r)
    big2, small2 = big - k, small - k
    d = big - small
    third = str(d - k) if d - k > 0 and d - k != d + k else str(big2)
    l3 = "%d − %d = %d" % (big2, small2, d)
    l4 = "%d − %d = %d" % (big, small, d)
    beats = [
        beat(pick(qid, "open", [
            "%s is %d and %s is %d. We want the difference in their ages, but %d years ago." % (x, p, y, r, k),
            "Two ages today: %d for %s and %d for %s. The question takes us back %d years and asks for the gap between them." % (p, x, r, y, k),
        ]), G("q1", "%s = %d years, %s = %d years" % (x, p, y, r)), G("q2", "Difference %d years ago = ?" % k)),
        beat("The word ago means we go back in time, so both ages get smaller. %d years ago %s was %d minus %d, which is %d." % (k, x, p, k, p2),
             W("w1", "%d − %d = %d" % (p, k, p2))),
        beat("%s was %d years younger too. %d minus %d is %d." % (y, k, r, k, r2),
             W("w2", "%d − %d = %d" % (r, k, r2))),
        beat("So back then they were %d and %d. What is the gap between those two ages?" % (p2, r2),
             ask=choose(qid, "gap", str(d), [str(d + k), third],
                        "For a gap, take the smaller age away from the bigger one: %d minus %d." % (big2, small2))),
        beat("%d minus %d is %d. The difference %d years ago was %d years." % (big2, small2, d, k, d),
             W("w3", l3), C("w3", str(d), l3.count(str(d)))),
        beat("Now look at today's ages. %d minus %d is also %d. The very same gap!" % (big, small, d),
             W("w4", l4), C("w4", str(d), l4.count(str(d)))),
        beat(pick(qid, "why", [
            "That is no accident. Both of them grew older by the same %d years, so the gap between them did not change." % k,
            "Here is why. Every birthday adds 1 year to both of them, so the gap between two ages never changes.",
        ]), A("ans", "Difference %d years ago = %d years" % (k, d)), U("ans", "%d years" % d, ("Difference %d years ago = %d years" % (k, d)).count("%d years" % d))),
        beat(pick(qid, "sum", [
            "So remember: the gap between two people's ages stays the same, in the past, today and for ever. Here it is %d." % d,
            "Next time you can go straight there. The difference in ages never changes, so just subtract today's ages. The answer is %d." % d,
        ])),
    ]
    return lesson(*beats, origin="rule")


def total(q, m):
    qid = q["id"]
    x, p, y, r, k = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    p2, r2 = p + k, r + k
    s0, s = p + r, p + r + 2 * k
    l1 = "%d + %d = %d" % (p, k, p2)
    l2 = "%d + %d = %d" % (r, k, r2)
    l3 = "%d + %d = %d" % (p2, r2, s)
    beats = [
        beat(pick(qid, "open", [
            "%s is %d and %s is %d. We want the sum of their ages, but after %d years." % (x, p, y, r, k),
            "Two ages today: %d for %s and %d for %s. The question jumps %d years ahead and asks what the ages add up to then." % (p, x, r, y, k),
        ]), G("q1", "%s = %d years, %s = %d years" % (x, p, y, r)), G("q2", "Sum after %d years = ?" % k)),
        beat("The word after means we go forward in time, so ages go up. After %d years %s will be %d plus %d, which is %d." % (k, x, p, k, p2),
             W("w1", l1), N("w1", str(p2), x, "below", l1.count(str(p2)))),
        beat("Now %s. What do we do with %s's age?" % (y, y),
             ask=choose(qid, "second", "add %d too" % k, ["leave it as %d" % r, "take away %d" % k],
                        "Time passes for everybody. %s also grows %d years older, so we add %d to %d as well." % (y, k, k, r))),
        beat("%s grows older as well. %d plus %d is %d." % (y, r, k, r2),
             W("w2", l2), N("w2", str(r2), y, "below", l2.count(str(r2)))),
        beat(pick(qid, "add", [
            "Now we add the two new ages. %d plus %d is %d." % (p2, r2, s),
            "Sum means add. So add the two new ages: %d plus %d makes %d." % (p2, r2, s),
        ]), W("w3", l3)),
        beat("So after %d years, their ages will add up to %d." % (k, s),
             A("ans", "Sum after %d years = %d years" % (k, s)), C("ans", "%d years" % s, ("Sum after %d years = %d years" % (k, s)).count("%d years" % s))),
        beat("Here is a quick check. Today they add up to %d. Each of them gains %d years, so we add %d twice. We reach %d again." % (s0, k, k, s),
             W("c1", "%d + %d = %d" % (p, r, s0)), W("c2", "%d + %d + %d = %d" % (s0, k, k, s))),
        beat(pick(qid, "sum", [
            "So when time passes, everyone in the sum grows older. Two people means the years are added twice.",
            "Remember the trap: adding the years only once. Two people grow older, so the sum grows twice as much.",
        ])),
    ]
    return lesson(*beats, origin="rule")


def by_rule(q):
    text = q["questionText"].strip()
    m = DIFF.match(text)
    if m:
        return difference(q, m)
    m = SUM.match(text)
    if m:
        return total(q, m)
    return None
