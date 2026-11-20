"""Rule lessons for the plain sum 'a × b = ?' (Grade 4 operations)."""
from g4_gr4_operations_common import (B, W, ANSR, GIVEN, M, pick, ask_of, has, step_figure, times_work, lesson)


def _open(q, a, b):
    qid = q["id"]
    sign = ""
    if has(q, a + b):
        sign = pick(qid, "sign", [" The sign is times, so we want %d lots of %d, not %d plus %d." % (a, b, a, b),
                                  " Look at the sign first. It is times, so we multiply.", ""])
    opening = pick(qid, "open", ["Here is our sum. %d times %d.", "%d times %d. Let us work it out together.",
                                 "Let us multiply %d by %d."]) % (a, b)
    return B(opening + sign, GIVEN("q", "%d × %d = ?" % (a, b)))


def _answer(q, a, b):
    p = a * b
    return B(pick(q["id"], "ans", ["So %d times %d equals %d.", "There it is. %d times %d makes %d.",
                                   "So %d times %d is %d."]) % (a, b, p),
             *ANSR("ans", "%d × %d = %d" % (a, b, p), str(p)))


def _last_digit(q, a, b):
    oa, ob = a % 10, b % 10
    if oa == 0 or ob == 0 or oa == a and ob == b:
        return None
    k = oa * ob
    if k < 10:
        say = "A quick check on the last digit. %d times %d is %d, and our answer ends in %d too." % (oa, ob, k, k)
    else:
        say = "A quick check on the last digit. %d times %d is %d, which ends in %d. Our answer ends in %d too." % (oa, ob, k, k % 10, k % 10)
    return B(say, W("ld", "%d × %d = %d" % (oa, ob, k)))


def mul_rule(q, a, b):
    qid = q["id"]
    p = a * b
    beats = [_open(q, a, b)]

    # two small numbers: groups
    if a <= 10 and b <= 10:
        rep = " + ".join([str(b)] * a)
        beats.append(B("%d times %d means %d groups of %d. Picture %d rows with %d in each row." % (a, b, a, b, a, b),
                       step_figure(qid, "grid", 0)))
        others = [" + ".join([str(b)] * (a + 1)), "%d + %d" % (a, b)]
        beats.append(B("Which adding sum shows %d groups of %d?" % (a, b),
                       ask=ask_of(qid, "a1", rep, others,
                                  "%d groups of %d means the %d is written %d times, with plus signs in between." % (a, b, b, a))))
        beats.append(B("Add them up. %s makes %d." % (rep.replace("+", "plus"), p), W("g", "%s = %d" % (rep, p))))
        beats.append(_answer(q, a, b))
        if a != b:
            beats.append(B("We can turn it round as well. %d groups of %d also make %d." % (b, a, p), W("t", "%d × %d = %d" % (b, a, p))))
        elif step_figure(qid, "grid", 0):
            beats.append(B("Count the squares in the picture if you like. %d rows of %d, and there are %d squares." % (a, b, p)))
        else:
            beats.append(B("%d groups of %d, and %d altogether. It fits." % (a, b, p)))
        beats.append(B("So times is a quick way of adding the same number again and again."))
        return lesson(*beats, origin="rule")

    # one small number and one two-digit number: split the two-digit one
    if a < 10 or b < 10:
        small, big = (a, b) if a < 10 else (b, a)
        t, o = big - big % 10, big % 10
        fmt = (lambda x: "%d × %d" % (small, x)) if a < 10 else (lambda x: "%d × %d" % (x, small))
        beats.append(B("%d is easier in two pieces. Split it into %d and %d." % (big, t, o),
                       W("sp", "%d = %d + %d" % (big, t, o)), step_figure(qid, "barModel", 0)))
        p1, p2 = small * t, small * o
        d = t // 10
        if d == 1:
            beats.append(B("First the tens piece. What is %d times %d?" % ((small, t) if a < 10 else (t, small)),
                           ask=ask_of(qid, "a1", str(p1), [str(small + t), str(small)],
                                      "%d tens is %d. Multiplying by 10 moves every digit one place to the left." % (small, p1))))
        else:
            beats.append(B("First the tens piece. What is %d times %d?" % ((small, t) if a < 10 else (t, small)),
                           ask=ask_of(qid, "a1", str(p1), [str(small * d), str(small + t)],
                                      "%d times %d is %d. So %d times %d tens is %d tens, and that is %d." % (small, d, small * d, small, d, small * d, p1))))
        beats.append(B("%d times %d is %d. That is the tens piece done." % ((small, t, p1) if a < 10 else (t, small, p1)),
                       W("p1", "%s = %d" % (fmt(t), p1))))
        beats.append(B("Now the ones piece. %d times %d is %d." % ((small, o, p2) if a < 10 else (o, small, p2)),
                       W("p2", "%s = %d" % (fmt(o), p2))))
        beats.append(B("Add the two pieces. %d and %d make %d." % (p1, p2, p), W("sum", "%d + %d = %d" % (p1, p2, p))))
        beats.append(_answer(q, a, b))
        beats.append(B(pick(qid, "sum", ["So split the big number into tens and ones, multiply each piece, then add.",
                                         "The plan: break the big number up, multiply each piece, and add the pieces."])))
        return lesson(*beats, origin="rule")

    # 50 lots: 100 lots, then halve
    if a == 50:
        h = 100 * b
        th, rest = h - h % 1000, h % 1000
        beats.append(B("50 is half of 100. And multiplying by 100 is easy, so let us start there.",
                       M("q", "50", "underline"), step_figure(qid, "barModel", 0)))
        beats.append(B("100 lots of %d is %d." % (b, h), W("h", "100 × %d = %d" % (b, h))))
        beats.append(B("But we only want 50 lots, and 50 is half of 100. So what do we do with %d?" % h,
                       ask=ask_of(qid, "a1", "halve it", ["double it", "take away 50"],
                                  "50 lots is half as many as 100 lots. So we need half of %d." % h)))
        beats.append(B("Halve it in two pieces. Half of %d is %d, and half of %d is %d." % (th, th // 2, rest, rest // 2),
                       W("h1", "%d ÷ 2 = %d" % (th, th // 2)), W("h2", "%d ÷ 2 = %d" % (rest, rest // 2))))
        beats.append(B("Together, %d and %d make %d." % (th // 2, rest // 2, p), W("sum", "%d + %d = %d" % (th // 2, rest // 2, p))))
        beats.append(_answer(q, a, b))
        beats.append(B("Check by doubling. Two lots of %d make %d again. It fits." % (p, h), W("chk", "%d × 2 = %d" % (p, h))))
        beats.append(B("So to multiply by 50, multiply by 100 and then halve."))
        return lesson(*beats, origin="rule")

    if b == 50:
        say, ops = times_work(a, 5, "f")
        beats.append(B("50 is 5 tens. So we can multiply by 5 first, and then make the answer ten times bigger.",
                       W("sp", "50 = 5 × 10"), M("sp", "5", "underline", 2)))
        beats.append(B("First, " + say, *ops))
        beats.append(B("Now make it ten times bigger. What is %d times 50?" % a,
                       ask=ask_of(qid, "a1", str(p), [str(a * 5), str(a * 5 + 10)],
                                  "Ten times bigger means every digit moves one place to the left. So %d becomes %d." % (a * 5, p))))
        beats.append(B("Ten times %d is %d. Just put a 0 on the end." % (a * 5, p), W("t", "%d × 10 = %d" % (a * 5, p))))
        beats.append(_answer(q, a, b))
        beats.append(B("So to multiply by 50, multiply by 5 and then by 10."))
        return lesson(*beats, origin="rule")

    # one less than a round number: round up, then take one lot away
    if a % 10 == 9 and (a + 1) in (20, 100):
        r = a + 1
        R = r * b
        tb, ob = b - b % 10, b % 10
        beats.append(B("%d is just 1 less than %d. And %d is a much friendlier number to multiply by." % (a, r, r),
                       W("sp", "%d = %d − 1" % (a, r)), step_figure(qid, "barModel", 0)))
        if r == 100:
            beats.append(B("So start with 100 lots of %d. That is %d." % (b, R), W("r", "100 × %d = %d" % (b, R))))
        else:
            beats.append(B("So start with %d lots of %d. 2 times %d is %d, so %d times %d is %d." % (r, b, b, 2 * b, r, b, R),
                           W("ra", "2 × %d = %d" % (b, 2 * b)), W("r", "%d × %d = %d" % (r, b, R))))
        beats.append(B("But we only want %d lots, not %d. What do we do now?" % (a, r),
                       ask=ask_of(qid, "a1", "take away one %d" % b, ["add one %d" % b, "take away 1"],
                                  "%d lots is one lot too many. One lot is %d, so we take away %d." % (r, b, b))))
        beats.append(B("Take away %d in two hops. First %d, which leaves %d. Then %d more, which leaves %d." % (b, tb, R - tb, ob, p),
                       W("m1", "%d − %d = %d" % (R, tb, R - tb)), W("m2", "%d − %d = %d" % (R - tb, ob, p))))
        beats.append(_answer(q, a, b))
        beats.append(_last_digit(q, a, b))
        beats.append(B("So when a number is 1 less than a round number, use the round number, then take one lot away."))
        return lesson(*beats, origin="rule")

    # two two-digit numbers: split the second into tens and ones
    tb, ob = b - b % 10, b % 10
    d = tb // 10
    p1, p2 = a * tb, a * ob
    beats.append(B(pick(qid, "split", ["That is a big one, so we break it into two smaller jobs. Split %d into %d and %d.",
                                       "Too big to do in one go. So split %d into %d and %d, and do one piece at a time."]) % (b, tb, ob),
                   W("sp", "%d = %d + %d" % (b, tb, ob)), step_figure(qid, "barModel", 0)))
    if d == 1:
        beats.append(B("First, %d times 10. That is %d, the same digits with a 0 on the end." % (a, p1), W("p1", "%d × 10 = %d" % (a, p1))))
        beats.append(B("We split %d into 10 and %d. The 10 is done. What is still left to multiply %d by?" % (b, ob, a),
                       ask=ask_of(qid, "a1", str(ob), [str(b), "10"],
                                  "%d is 10 and %d. We have done the 10, so the %d is still left." % (b, ob, ob))))
    else:
        say, ops = times_work(a, d, "f")
        beats.append(B("Start with the tens piece, %d. First, " % tb + say, *ops))
        beats.append(B("%d is %d tens. So what is %d times %d?" % (tb, d, a, tb),
                       ask=ask_of(qid, "a1", str(p1), [str(a * d), str(a * d + 10)],
                                  "%d is ten times %d. So the answer is ten times %d, which is %d with a 0 on the end." % (tb, d, a * d, a * d))))
        beats.append(B("Ten times %d is %d. That is the first piece done." % (a * d, p1), W("p1", "%d × %d = %d" % (a, tb, p1))))
    say, ops = times_work(a, ob, "p2")
    beats.append(B("Now the ones piece. " + say, *ops))
    beats.append(B(pick(qid, "join", ["Add the two pieces. %d plus %d is %d.", "Now put the two pieces together. %d and %d make %d."]) % (p1, p2, p),
                   W("sum", "%d + %d = %d" % (p1, p2, p))))
    beats.append(_answer(q, a, b))
    beats.append(_last_digit(q, a, b))
    beats.append(B(pick(qid, "sum", ["So the plan is: split one number into tens and ones, multiply each piece, then add.",
                                     "Break it up, multiply each piece, add the pieces. Big sums are just small sums in a row."])))
    return lesson(*beats, origin="rule")
