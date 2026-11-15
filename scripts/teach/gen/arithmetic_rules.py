"""Lessons by rule for the generated arithmetic families (ids starting VAR_, BOOST_).

Wordings covered:
    Simplify: a + b × c                 times before plus
    Simplify: a + b × c − d             times first, then left to right
    Simplify: a − b × c + d             times first, then left to right (the minus owns only the product)
    Simplify: a × b + c,  a × b − c     times first (with the product split into tens and ones)
    Simplify: a ÷ b + c × d             divide and times before plus (two do not divide evenly)
    Solve: ax + b = c,  ax − b = c      undo the add or take away, then undo the times
    Find the average of: ...            add, count, share
    The average of n numbers is m. If n − 1 of them are ..., find the missing number.
    The average of n numbers is m. When a new number k is added, what is the new average?

Every number on the board is computed here; nothing is typed in by hand.
"""
import re
from fractions import Fraction

from arithmetic_common import (ANS, B, BOTH, DIV, FIG, GIVEN, M, N, S, W, choose, lesson, nth_at, pick, placed)

SUMMARY = [
    "So here is the plan for a line like this. Hunt for times and divide and do those first. Then do the plus and minus, from left to right.",
    "Remember it like this. Times and divide go first, wherever they sit. Plus and minus wait their turn, then go from left to right.",
    "That is the whole trick. Before you work anything out, look at the signs. Times and divide first, then plus and minus in order.",
]


def circle_answer(line_id, text, value):
    return M(line_id, value, "circle", nth_at(text, value, text.index("=")))


def times_fact(b, c, p):
    if c == 1:
        return "%d times 1 is just %d." % (b, p)
    if b == 1:
        return "1 times %d is just %d." % (c, p)
    return "%d times %d is %d." % (b, c, p)


# ── a + b × c ────────────────────────────────────────────────────────────────

def plus_times(qid, a, b, c):
    p, r, t = b * c, a + b * c, (a + b) * c
    l1 = "%d + %d × %d" % (a, b, c)
    pair = "%d × %d" % (b, c)
    l2 = "%s = %d + %d" % (l1, a, p)
    l3 = "%s = %d" % (l1, r)
    choices, right = placed(qid, "c1", pair, ["%d + %d" % (a, b), "either, it makes no difference"])
    beats = [
        B(pick(qid, "i", [
            "Here is our sum. %d plus %d times %d. Only two signs, but there is a trap hiding in it." % (a, b, c),
            "Let's write this one up. %d plus %d times %d. It looks short and friendly, but we must decide where to start." % (a, b, c),
            "Look at this line. %d plus %d times %d. A plus and a times, side by side." % (a, b, c),
        ]), GIVEN("l1", l1)),
        B(pick(qid, "q", [
            "So, which part do we do first?",
            "Before we work anything out: which pair of numbers goes first?",
            "Have a look at the two signs. Where do we start?",
        ]), ask=choose(choices, right, pick(qid, "n", [
            "Starting on the left with %d plus %d is the natural thing to try. But times is stronger than plus, so %d times %d has to go first." % (a, b, b, c),
            "Look for the times sign. Times comes before plus, so %d times %d goes first, even though it sits at the end of the line." % (b, c),
        ]))),
        B(pick(qid, "m", [
            "Times comes before plus, so this pair goes first. I'll underline it. %s" % times_fact(b, c, p),
            "I'll underline %d times %d, because times is always done before plus. %s" % (b, c, times_fact(b, c, p)),
        ]), M("l1", pair), N("l1", pair, str(p))),
        B(pick(qid, "w", [
            "Now we write the line again, with %d sitting where %d times %d was. The %d just waits." % (p, b, c, a),
            "So %d times %d turns into %d, and the %d in front comes down unchanged." % (b, c, p, a),
        ]), W("l2", l2)),
        B(pick(qid, "a", [
            "And %d plus %d is %d. That is our answer." % (a, p, r),
            "Now it is easy. %d plus %d makes %d." % (a, p, r),
        ]), ANS("l3", l3), circle_answer("l3", l3, str(r))),
    ]
    if t != r:
        beats.append(B(pick(qid, "t", [
            "Here is why the order matters. Adding %d and %d first is like putting a bracket round them, and that gives %d. A different sum, so a different answer." % (a, b, t),
            "See the trap? Going straight from the left would add %d and %d first, as if they wore a bracket. That comes to %d, which belongs to a different sum." % (a, b, t),
        ]), W("l4", "(%d + %d) × %d = %d" % (a, b, c, t))))
    else:
        beats.append(B("Times 1 changes nothing, so this one was kind to us. With any other number there, starting from the left would have gone astray."))
    beats.append(B(pick(qid, "s", SUMMARY)))
    return lesson(*beats, origin="rule")


# ── a + b × c − d ────────────────────────────────────────────────────────────

def plus_times_minus(qid, a, b, c, d):
    p = b * c
    s = a + p
    r = s - d
    t = (a + b) * c - d
    l1 = "%d + %d × %d − %d" % (a, b, c, d)
    pair = "%d × %d" % (b, c)
    rhs = "%d + %d − %d" % (a, p, d)
    l2 = "%s = %s" % (l1, rhs)
    l3 = "%s = %d − %d" % (rhs, s, d)
    l4 = "%s = %d" % (l1, r)
    choices, right = placed(qid, "c1", pair, ["%d + %d" % (a, b), "%d − %d" % (c, d)])
    beats = [
        B(pick(qid, "i", [
            "Here is our sum. %d plus %d times %d, minus %d. Three different signs, so the order we work in really matters." % (a, b, c, d),
            "Let's write it up. %d plus %d times %d, minus %d. A plus, a times and a minus, all in one line." % (a, b, c, d),
            "Look at this one. %d plus %d times %d, minus %d. Before we work anything out, we need to decide where to start." % (a, b, c, d),
        ]), GIVEN("l1", l1)),
        B(pick(qid, "q", [
            "So, which part do we do first?",
            "Have a look at the signs. Which pair of numbers goes first?",
            "Where shall we start?",
        ]), ask=choose(choices, right, pick(qid, "n", [
            "Starting from the left with %d plus %d is the natural thing to try. But times is stronger than plus and minus, so %d times %d has to go first." % (a, b, b, c),
            "Look for the times sign. Times comes before plus and minus, so %d times %d goes first, wherever it sits in the line." % (b, c),
        ]))),
        B(pick(qid, "m", [
            "Times comes before plus and minus, so this pair goes first. I'll underline it. %s" % times_fact(b, c, p),
            "I'll underline %d times %d, because times is done before plus and minus. %s" % (b, c, times_fact(b, c, p)),
        ]), M("l1", pair), N("l1", pair, str(p))),
        B(pick(qid, "w", [
            "Now we write the line again, with %d sitting where %d times %d was. Everything else stays put." % (p, b, c),
            "So %d times %d turns into %d, and the rest of the line comes down unchanged." % (b, c, p),
        ]), W("l2", l2)),
        B(pick(qid, "l", [
            "Only plus and minus are left, and those two we do in order, from left to right. %d plus %d is %d." % (a, p, s),
            "Now there is just a plus and a minus. Neither is stronger, so we go from left to right. %d plus %d makes %d." % (a, p, s),
        ]), M("l2", "%d + %d" % (a, p), "underline", nth_at(l2, "%d + %d" % (a, p), l2.index("="))), W("l3", l3)),
        B(pick(qid, "a", [
            "And %d minus %d is %d. So the whole line comes to %d." % (s, d, r, r),
            "Last step. %d minus %d leaves %d. That is our answer." % (s, d, r),
        ]), ANS("l4", l4), circle_answer("l4", l4, str(r))),
    ]
    if t != r and t > 0:
        beats.append(B(pick(qid, "t", [
            "Here is why the order matters. Going straight from the left means adding %d and %d first, as if they had a bracket round them. That gives %d, the answer to a different sum." % (a, b, t),
            "See the trap? If we add %d and %d first, it is like slipping a bracket round them, and the line comes to %d. Same numbers, different sum." % (a, b, t),
        ]), W("l5", "(%d + %d) × %d − %d = %d" % (a, b, c, d, t))))
    beats.append(B(pick(qid, "s", SUMMARY)))
    return lesson(*beats, origin="rule")


# ── a − b × c + d ────────────────────────────────────────────────────────────

def minus_times_plus(qid, a, b, c, d):
    p = b * c
    l1 = "%d − %d × %d + %d" % (a, b, c, d)
    pair = "%d × %d" % (b, c)
    rhs = "%d − %d + %d" % (a, p, d)
    l2 = "%s = %s" % (l1, rhs)
    r = a - p + d
    l_ans = "%s = %d" % (l1, r)
    choices, right = placed(qid, "c1", pair, ["%d − %d" % (a, b), "%d + %d" % (c, d)])
    beats = [
        B(pick(qid, "i", [
            "Here is our sum. %d minus %d times %d, plus %d. Three different signs, so the order we work in really matters." % (a, b, c, d),
            "Let's write it up. %d minus %d times %d, plus %d. A minus, a times and a plus, all in one line." % (a, b, c, d),
            "Look at this one. %d minus %d times %d, plus %d. Before we work anything out, we need to decide where to start." % (a, b, c, d),
        ]), GIVEN("l1", l1)),
        B(pick(qid, "q", [
            "So, which part do we do first?",
            "Have a look at the signs. Which pair of numbers goes first?",
            "Where shall we start?",
        ]), ask=choose(choices, right, pick(qid, "n", [
            "Starting from the left with %d minus %d is the natural thing to try. But times is stronger than plus and minus, so %d times %d has to go first." % (a, b, b, c),
            "Look for the times sign. Times comes before plus and minus, so %d times %d goes first, wherever it sits in the line." % (b, c),
        ]))),
        B(pick(qid, "m", [
            "Times comes before plus and minus, so this pair goes first. I'll underline it. %s" % times_fact(b, c, p),
            "I'll underline %d times %d, because times is done before plus and minus. %s" % (b, c, times_fact(b, c, p)),
        ]), M("l1", pair), N("l1", pair, str(p))),
        B(pick(qid, "w", [
            "Now we write the line again, with %d sitting where %d times %d was. Everything else stays put." % (p, b, c),
            "So %d times %d turns into %d, and the rest of the line comes down unchanged." % (b, c, p),
        ]), W("l2", l2)),
    ]
    if a >= p:
        m = a - p
        first = "%d − %d" % (a, p)
        c2, right2 = placed(qid, "c2", first, ["%d + %d" % (p, d)])
        l3 = "%s = %d + %d" % (rhs, m, d)
        beats += [
            B(pick(qid, "q2", [
                "Now there is only a minus and a plus. Which of these do we do next?",
                "Two signs left, a minus and a plus. Which pair goes next?",
            ]), ask=choose(c2, right2,
                           "Plus and minus are equally strong, so neither jumps the queue. We simply go from left to right, and %d minus %d is on the left." % (a, p))),
            B(pick(qid, "l", [
                "%d minus %d is %d. Careful here: the minus belongs only to the %d. The plus %d must not get swallowed up with it." % (a, p, m, p, d),
                "Left to right, so %d minus %d first, and that is %d. Watch out: we are taking away %d only, not %d and %d together." % (a, p, m, p, p, d),
            ]), M("l2", first, "underline", nth_at(l2, first, l2.index("="))), W("l3", l3)),
            B(pick(qid, "a", [
                "And %d plus %d is %d. So the whole line comes to %d." % (m, d, r, r),
                "Last step. %d plus %d makes %d. That is our answer." % (m, d, r),
            ]), ANS("l4", l_ans), circle_answer("l4", l_ans, str(r))),
        ]
    else:
        up = a + d
        assert up >= p, qid
        l3 = "%s = %d + %d − %d" % (rhs, a, d, p)
        l4 = "%d + %d − %d = %d − %d" % (a, d, p, up, p)
        beats += [
            B("Now look closely. %d minus %d would take us below zero. But the plus %d belongs to this line too, so let's bring it forward and add first."
              % (a, p, d), W("l3", l3)),
            B("%d plus %d is %d. We have moved the plus %d, and the minus %d has kept its own sign." % (a, d, up, d, p), W("l4", l4)),
            B("And %d minus %d leaves %d. So the whole line comes to %d." % (up, p, r, r),
              ANS("l5", l_ans), circle_answer("l5", l_ans, str(r))),
        ]
    beats.append(B(pick(qid, "s", SUMMARY)))
    return lesson(*beats, origin="rule")
