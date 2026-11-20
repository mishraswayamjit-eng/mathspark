"""Rule lessons for the order-of-operations families (Grade 4 operations)."""
from g4_gr4_operations_common import (B, W, ANSR, GIVEN, M, N, pick, ask_of, times_work, lesson)


def _times_say(b, c):
    p = b * c
    if c == 1:
        return "%d times 1 is just %d." % (b, p)
    if b == 1:
        return "1 times %d is just %d." % (c, p)
    return "%d times %d is %d." % (b, c, p)


def minus_times_plus(q, a, b, c, d):
    """a − b × c + d"""
    qid = q["id"]
    p = b * c
    m = a - p
    r = m + d
    bc = "%d × %d" % (b, c)
    beats = [B(pick(qid, "open", ["Here is our sum. It has three signs in it: a minus, a times and a plus.",
                                  "Three signs in one sum: a minus, a times and a plus. The trick is knowing where to start.",
                                  "Look at the signs here. A minus, then a times, then a plus."]),
               GIVEN("q", "%d − %d × %d + %d" % (a, b, c, d)))]
    beats.append(B(pick(qid, "ask1", ["Which part do we work out first?", "Where do we begin?", "So, which bit goes first?"]),
                   ask=ask_of(qid, "a1", bc, ["%d − %d" % (a, b), "%d + %d" % (c, d)],
                              pick(qid, "if1", ["Times goes before plus and minus, even when it sits in the middle. So we begin with %d times %d.",
                                                "It is tempting to start on the left. But multiplying always goes first, so %d times %d is our first job."]) % (b, c))))
    beats.append(B(pick(qid, "box", ["Multiplying goes before adding and taking away. So we box the %d times %d. It goes first.",
                                     "Times is the boss here. It goes before plus and minus, so put a box round %d times %d."]) % (b, c),
                   M("q", bc, "box"), N("q", bc, "first", "below")))
    beats.append(B(_times_say(b, c) + " " + pick(qid, "copy", ["Write %d in its place, and copy everything else just as it was.",
                                                               "So %d goes where the box was. The rest of the sum stays the same."]) % p,
                   W("l2", "%d − %d + %d" % (a, p, d))))
    beats.append(B(pick(qid, "ask2", ["Now only a minus and a plus are left. Which do we do first?",
                                      "Just a minus and a plus now. Which one comes first?"]),
                   ask=ask_of(qid, "a2", "%d − %d" % (a, p), ["%d + %d" % (p, d)],
                              "Plus and minus are equal partners, so we go from left to right, just like reading. The minus comes first: %d take away %d." % (a, p))))
    if m == 0:
        beats.append(B("Left to right, just like reading. %d take away %d leaves nothing at all. That is 0." % (a, p),
                       M("l2", "%d − %d" % (a, p), "underline"), W("l3", "%d − %d = %d" % (a, p, m))))
    else:
        beats.append(B("Left to right, just like reading. %d take away %d is %d." % (a, p, m),
                       M("l2", "%d − %d" % (a, p), "underline"), W("l3", "%d − %d = %d" % (a, p, m))))
    beats.append(B(pick(qid, "last", ["And now the plus. %d plus %d is %d.", "Last of all, add the %s. %d plus %d is %d."][:1]
                        + ["One job left, the plus. %d and %d make %d."]) % (m, d, r),
                   *ANSR("ans", "%d + %d = %d" % (m, d, r), str(r))))
    beats.append(B(pick(qid, "trap", ["Did you spot the trap? Going left to right from the very start would mean taking away before multiplying, and that gives a different number.",
                                      "The trap in this sum is the minus at the front. It looks like the place to start, but the times must go first."])))
    beats.append(B(pick(qid, "sum", ["So remember: times first, then plus and minus from left to right.",
                                     "The rule: multiply first. Then add and take away in order, from left to right."])))
    return lesson(*beats, origin="rule")


def plus_times(q, a, b, c):
    """a + b × c"""
    qid = q["id"]
    p = b * c
    r = a + p
    bc = "%d × %d" % (b, c)
    beats = [B(pick(qid, "open", ["Here is our sum. Two signs in it: a plus and a times.",
                                  "Two signs in one sum, a plus and a times. The trick is knowing which goes first."]),
               GIVEN("q", "%d + %d × %d" % (a, b, c)))]
    beats.append(B(pick(qid, "ask1", ["Which part do we work out first?", "Where do we begin?", "So, which bit goes first?"]),
                   ask=ask_of(qid, "a1", bc, ["%d + %d" % (a, b)],
                              pick(qid, "if1", ["Times goes before plus, even though the plus is written first. So we begin with %d times %d.",
                                                "It is tempting to start on the left. But multiplying always goes before adding, so %d times %d is our first job."]) % (b, c))))
    beats.append(B(pick(qid, "box", ["Multiplying goes before adding. So we box the %d times %d. It goes first.",
                                     "Times goes before plus, so put a box round %d times %d."]) % (b, c),
                   M("q", bc, "box"), N("q", bc, "first", "below")))
    beats.append(B(_times_say(b, c) + " " + pick(qid, "copy", ["Write %d in its place, and copy the rest just as it was.",
                                                               "So %d goes where the box was. The %s and the plus stay."][:1]
                                                 + ["So %d goes where the box was, and the rest stays the same."]) % p,
                   W("l2", "%d + %d" % (a, p))))
    beats.append(B(pick(qid, "last", ["Now the plus. %d plus %d is %d.", "One job left, the adding. %d and %d make %d."]) % (a, p, r),
                   *ANSR("ans", "%d + %d = %d" % (a, p, r), str(r))))
    beats.append(B("Careful with the trap here. Adding %d and %d first, just because they come first, gives a different number. The %d belongs to the times." % (a, b, b)))
    beats.append(B(pick(qid, "sum", ["So remember: times first, then the plus.", "The rule: multiply before you add, wherever the times sign sits."])))
    return lesson(*beats, origin="rule")


def times_then(q, a, b, sign, c):
    """a × b + c  or  a × b − c"""
    qid = q["id"]
    p = a * b
    r = p + c if sign == "+" else p - c
    word = "plus" if sign == "+" else "minus"
    sym = "+" if sign == "+" else "−"
    ab = "%d × %d" % (a, b)
    beats = [B("Here is our sum. Two signs in it: a times and a %s." % word, GIVEN("q", "%d × %d %s %d" % (a, b, sym, c)))]
    beats.append(B(pick(qid, "ask1", ["Which part do we work out first?", "Where do we begin?", "So, which bit goes first?"]),
                   ask=ask_of(qid, "a1", ab, ["%d %s %d" % (b, sym, c)],
                              "Times goes before plus and minus. So %d times %d is our first job. The %d has to wait." % (a, b, c))))
    beats.append(B("Times always goes before plus and minus. This time it is also first in line, so we start on the left.",
                   M("q", ab, "box"), N("q", ab, "first", "below")))
    say, ops = times_work(a, b, "p")
    beats.append(B(say, *ops))
    beats.append(B("So %d goes where the box was. The %s %d is still there." % (p, word, c), W("l2", "%d %s %d" % (p, sym, c))))
    if sign == "+":
        beats.append(B("Now the plus. %d plus %d is %d." % (p, c, r), *ANSR("ans", "%d + %d = %d" % (p, c, r), str(r))))
    else:
        beats.append(B("Now the minus. %d take away %d is %d." % (p, c, r), *ANSR("ans", "%d − %d = %d" % (p, c, r), str(r))))
    beats.append(B("Careful with one thing. The %d is not part of the times. It is only %s after the multiplying is done." % (
        c, "added on" if sign == "+" else "taken away")))
    beats.append(B("So remember: times first, then plus or minus."))
    return lesson(*beats, origin="rule")


def divide_plus_times(q, a, b, c, d):
    """a ÷ b + c × d"""
    qid = q["id"]
    q1 = a // b
    p = c * d
    r = q1 + p
    ab = "%d ÷ %d" % (a, b)
    cd = "%d × %d" % (c, d)
    line = "%d ÷ %d + %d × %d" % (a, b, c, d)
    beats = [B(pick(qid, "open", ["Here is our sum. It has three signs in it: a divide, a plus and a times.",
                                  "Three signs in one sum: a divide, a plus and a times. The trick is knowing where to start."]),
               GIVEN("q", line))]
    beats.append(B("One of these three signs has to wait until the very end. Which one?",
                   ask=ask_of(qid, "a1", "the +", ["the ÷", "the ×"],
                              "Divide and times both go before plus. So the plus is the one that waits until the end.")))
    beats.append(B("Dividing and multiplying go before adding. So we box %d divided by %d, and we box %d times %d." % (a, b, c, d),
                   M("q", ab, "box"), M("q", cd, "box", line.count(cd)), N("q", "+", "last", "below")))
    beats.append(B("First box. %d divided by %d is %d, because %d times %d is %d." % (a, b, q1, b, q1, a), W("d", "%d ÷ %d = %d" % (a, b, q1))))
    beats.append(B("Second box. " + _times_say(c, d), W("m", "%d × %d = %d" % (c, d, p))))
    beats.append(B("Put each answer where its box was, with the plus still in between.", W("l2", "%d + %d" % (q1, p))))
    beats.append(B("Now the plus gets its turn. %d plus %d is %d." % (q1, p, r), *ANSR("ans", "%d + %d = %d" % (q1, p, r), str(r))))
    beats.append(B(pick(qid, "trap", ["The trap here is going straight along from left to right. The %d must not be added until the times is done." % q1,
                                      "Careful with the trap. Do not add in the middle first. The plus joins the two boxes, so it comes last."])))
    beats.append(B(pick(qid, "sum", ["So remember: divide and multiply first, then add.",
                                     "The rule: do the dividing and the multiplying first. The adding comes last."])))
    return lesson(*beats, origin="rule")
