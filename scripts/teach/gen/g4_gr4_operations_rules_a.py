"""Rule lessons for the plain sums 'a + b = ?' and 'a - b = ?' (Grade 4 operations)."""
from g4_gr4_operations_common import (B, W, GIVEN, ANSR, M, pick, ask_of, has, hop_figure, lesson, tw, ow, rivals)


def _tens(n):
    return n - n % 10


# ── Adding ───────────────────────────────────────────────────────────────────

def add_rule(q, a, b):
    qid = q["id"]
    s = a + b
    sign = ""
    if has(q, a * b):
        sign = pick(qid, "sign", [" The sign is a plus, so we are adding, not multiplying.",
                                  " Look at the sign first. It is a plus, so we add.", ""])
    opening = pick(qid, "open", ["Here is our sum. %d plus %d.", "Let us add %d and %d.",
                                 "%d plus %d. Let us work it out together."]) % (a, b) + sign
    beats = [B(opening, GIVEN("q", "%d + %d = ?" % (a, b)))]
    answer = B(pick(qid, "ans", ["So %d plus %d equals %d.", "There it is. %d plus %d makes %d.",
                                 "So %d plus %d is %d."]) % (a, b, s),
               *ANSR("ans", "%d + %d = %d" % (a, b, s), str(s)))
    check = B(pick(qid, "chk", ["Let us check by going backwards. %d take away %d brings us back to %d.",
                                "A quick check. Take the %d away from %d again, and we are back at %d. It fits."][:1]
                   + ["A quick check. %d take away %d is %d, right where we started. It fits."]) % (s, b, a),
              W("chk", "%d − %d = %d" % (s, b, a)))
    big, small = max(a, b), min(a, b)
    ones, tens = big % 10, _tens(big)

    if small < 10:
        if a < b:
            beats.append(B("Adding works in any order. So let us start from the bigger number, %d, and add the %d to it." % (big, small),
                           W("sw", "%d + %d = ?" % (big, small))))
        if ones == 0:
            beats.append(B("%d is a round number. It has full tens and no ones at all." % big,
                           M("q", str(big), "underline")))
            beats.append(B("So the %d ones have the ones place all to themselves. What is %d and %d more?" % (small, big, small),
                           ask=ask_of(qid, "a1", str(s), rivals(q, [str(big * small), "%d%d" % (big, small)]),
                                      "Keep the %d as it is and put the %d in the empty ones place. That makes %d." % (big, small, s))))
            beats.append(answer)
            beats.append(check)
            beats.append(B("So when one number is a round ten, the small number simply drops into the ones place."))
            return lesson(*beats, origin="rule")
        if ones + small < 10:
            o = ones + small
            beats.append(B("%d is %d and %d. Let us split it into its tens and its ones." % (big, tens, ones),
                           W("sp", "%d = %d + %d" % (big, tens, ones)), M("sp", str(ones), "underline", ("%d = %d + %d" % (big, tens, ones)).count(str(ones)))))
            beats.append(B("There is room in the ones place, so only the ones will change. What is %d plus %d?" % (ones, small),
                           ask=ask_of(qid, "a1", str(o), [str(ones * small) if ones * small != o else str(o + 2), str(o + 1)],
                                      "Start at %d and count on %d more. You land on %d." % (ones, small, o))))
            beats.append(B("%s and %s make %s." % (ow(ones), ow(small), ow(o)),
                           W("o", "%d + %d = %d" % (ones, small, o)), hop_figure(qid)))
            beats.append(B("The tens have not changed, so put them back. %d and %d make %d." % (tens, o, s),
                           W("j", "%d + %d = %d" % (tens, o, s))))
            beats.append(answer)
            beats.append(check)
            beats.append(B(pick(qid, "sum", ["So when you add a small number and there is room in the ones, keep the tens and just add the ones.",
                                             "The plan: split off the ones, add the ones, then put the tens back."])))
            return lesson(*beats, origin="rule")
        need = 10 - ones
        rest = small - need
        nxt = tens + 10
        beats.append(B("%d is very close to %d. It needs just %d more to get there." % (big, nxt, need),
                       W("n", "%d + %d = %d" % (big, need, nxt)), hop_figure(qid)))
        beats.append(B("So we use %d of the %d to reach %d. How much of the %d is still left to add?" % (need, small, nxt, small),
                       ask=ask_of(qid, "a1", str(rest), [str(small), str(rest + 1)],
                                  "We used %d out of the %d to reach %d. Take %d from %d and %d is left." % (need, small, nxt, need, small, rest))))
        beats.append(B("%d is %d and %d. The %d took us to %d, and the %d is still waiting." % (small, need, rest, need, nxt, rest),
                       W("sp", "%d = %d + %d" % (small, need, rest))))
        beats.append(B("Now it is easy. %d plus %d is %d." % (nxt, rest, s), W("j", "%d + %d = %d" % (nxt, rest, s))))
        beats.append(answer)
        beats.append(check)
        beats.append(B(pick(qid, "sum", ["So when the ones spill over, fill up to the next ten first, then add what is left.",
                                         "The plan: make the next ten first, then add the rest."])))
        return lesson(*beats, origin="rule")

    if a % 10 == 0 or b % 10 == 0:
        rnd, other = (a, b) if a % 10 == 0 else (b, a)
        ot, oo = _tens(other), other % 10
        T = rnd + ot
        beats.append(B("%d is a round number, full tens and no ones. So we only need to split the %d, into %d and %d." % (rnd, other, ot, oo),
                       W("sp", "%d = %d + %d" % (other, ot, oo))))
        beats.append(B("Add the tens first. What is %d plus %d?" % (rnd, ot),
                       ask=ask_of(qid, "a1", str(T), [str(T // 10), str(T + 10)],
                                  "%s and %s make %d tens. And %d tens is %d." % (tw(rnd // 10), tw(ot // 10), T // 10, T // 10, T))))
        beats.append(B("%s and %s make %d tens. That is %d." % (tw(rnd // 10), tw(ot // 10), T // 10, T),
                       W("t", "%d + %d = %d" % (rnd, ot, T))))
        beats.append(B("Now bring in the %d ones. %d and %d make %d." % (oo, T, oo, s), W("j", "%d + %d = %d" % (T, oo, s))))
        beats.append(answer)
        beats.append(check)
        beats.append(B("So add the tens first, then drop the ones in."))
        return lesson(*beats, origin="rule")

    ta, oa, tb, ob = _tens(a), a % 10, _tens(b), b % 10
    T, O = ta + tb, oa + ob
    beats.append(B(pick(qid, "split", ["Two big numbers are easier in pieces. Let us split each one into tens and ones.",
                                       "Big numbers are friendlier in pieces. So we split each one into its tens and its ones."]),
                   W("s1", "%d = %d + %d" % (a, ta, oa)), W("s2", "%d = %d + %d" % (b, tb, ob))))
    beats.append(B("Start with the tens. What is %d plus %d?" % (ta, tb),
                   ask=ask_of(qid, "a1", str(T), [str(T // 10), str(T + 10)],
                              "%s and %s make %d tens. And %d tens is %d." % (tw(ta // 10), tw(tb // 10), T // 10, T // 10, T))))
    beats.append(B("%s and %s make %d tens. That is %d." % (tw(ta // 10), tw(tb // 10), T // 10, T),
                   W("t", "%d + %d = %d" % (ta, tb, T))))
    extra = " That is more than 9, and that is fine. We just add it on." if O > 9 else ""
    beats.append(B("Now the ones. %d plus %d is %d.%s" % (oa, ob, O, extra), W("o", "%d + %d = %d" % (oa, ob, O))))
    beats.append(B(pick(qid, "join", ["Last, join the two parts. %d plus %d is %d.", "Now put the two parts together. %d and %d make %d."]) % (T, O, s),
                   W("j", "%d + %d = %d" % (T, O, s))))
    beats.append(answer)
    beats.append(check)
    beats.append(B(pick(qid, "sum", ["So the plan is: split into tens and ones, add the tens, add the ones, then join them.",
                                     "Tens with tens, ones with ones, then put them together. That works every time."])))
    return lesson(*beats, origin="rule")


# ── Taking away ──────────────────────────────────────────────────────────────

def sub_rule(q, a, b):
    qid = q["id"]
    d = a - b
    sign = ""
    if has(q, a + b):
        sign = pick(qid, "sign", [" The sign is a minus, so we are taking away, not adding.",
                                  " Look at the sign first. It is a minus, so we take away.", ""])
    opening = pick(qid, "open", ["Here is our sum. %d take away %d.", "%d minus %d. Let us work it out together.",
                                 "Let us take %d away from %d."])
    opening = (opening % ((b, a) if opening.startswith("Let us take") else (a, b))) + sign
    beats = [B(opening, GIVEN("q", "%d − %d = ?" % (a, b)))]
    answer = B(pick(qid, "ans", ["So %d take away %d equals %d.", "There it is. %d minus %d leaves %d.",
                                 "So %d minus %d is %d."]) % (a, b, d),
               *ANSR("ans", "%d − %d = %d" % (a, b, d), str(d)))
    check = B(pick(qid, "chk", ["Check by adding back. %d plus %d makes %d, the number we started with.",
                                "Let us check by going backwards. %d plus %d is %d. It fits."]) % (d, b, a),
              W("chk", "%d + %d = %d" % (d, b, a)))
    ones, tens = a % 10, _tens(a)

    if a < 10:
        beats.append(B("Picture a number line. We start at %d and hop back %d times, one hop for each one we take away." % (a, b),
                       hop_figure(qid)))
        beats.append(B("Where do we land?",
                       ask=ask_of(qid, "a1", str(d), rivals(q, [str(a + b), str(d + 1)]),
                                  "Start at %d and hop back one at a time, %d hops in all. You land on %d." % (a, b, d))))
        beats.append(answer)
        beats.append(check)
        beats.append(B("So taking away means hopping back along the number line."))
        return lesson(*beats, origin="rule")

    if b < 10 and ones >= b:
        o = ones - b
        beats.append(B("%d is %d and %d. Let us split it into its tens and its ones." % (a, tens, ones),
                       W("sp", "%d = %d + %d" % (a, tens, ones))))
        beats.append(B("There are enough ones to take %d from. So only the ones change. What is %d take away %d?" % (b, ones, b),
                       ask=ask_of(qid, "a1", str(o), [str(ones + b), str(o + 1)],
                                  "Start at %d and hop back %d. You land on %d." % (ones, b, o))))
        left = "no ones at all" if o == 0 else ow(o)
        beats.append(B("%s take away %s leaves %s." % (ow(ones), ow(b), left), W("o", "%d − %d = %d" % (ones, b, o))))
        beats.append(B("The tens have not changed, so put them back. %d and %d make %d." % (tens, o, d),
                       W("j", "%d + %d = %d" % (tens, o, d)), hop_figure(qid)))
        beats.append(answer)
        beats.append(check)
        beats.append(B("So when there are enough ones, keep the tens and just take away from the ones."))
        return lesson(*beats, origin="rule")

    if b < 10:
        rest = b - ones
        beats.append(B("%d has only %d ones, and we need to take away %d. So first take away %d, to land on the round number %d." % (a, ones, b, ones, tens),
                       W("n", "%d − %d = %d" % (a, ones, tens))))
        beats.append(B("We have taken %d so far, out of %d. How many more do we still have to take away?" % (ones, b),
                       ask=ask_of(qid, "a1", str(rest), [str(b), str(rest + 1)],
                                  "%d is %d and %d. We have taken the %d, so %s still to go." % (b, ones, rest, ones, "1 more is" if rest == 1 else "%d more are" % rest))))
        beats.append(B("%d is %d and %d. The %d is done, and the %d is still waiting." % (b, ones, rest, ones, rest),
                       W("sp", "%d = %d + %d" % (b, ones, rest))))
        beats.append(B("Now hop back %d more from %d. That lands on %d." % (rest, tens, d),
                       W("j", "%d − %d = %d" % (tens, rest, d)), hop_figure(qid)))
        beats.append(answer)
        beats.append(check)
        beats.append(B(pick(qid, "sum", ["So when there are not enough ones, hop back to the round number first, then take away what is left.",
                                         "The plan: go back to the round ten first, then take away the rest."])))
        return lesson(*beats, origin="rule")

    if b % 10 == 0:
        T = tens - b
        beats.append(B("%d is a round number, full tens and no ones. So split the %d into %d and %d." % (b, a, tens, ones),
                       W("sp", "%d = %d + %d" % (a, tens, ones))))
        beats.append(B("Take the tens away first. What is %d take away %d?" % (tens, b),
                       ask=ask_of(qid, "a1", str(T), [str(tens + b), str(T + 10)],
                                  "%s take away %s leaves %s. And %s is %d." % (tw(tens // 10), tw(b // 10), tw(T // 10), tw(T // 10), T))))
        beats.append(B("%s take away %s leaves %s. That is %d." % (tw(tens // 10), tw(b // 10), tw(T // 10), T),
                       W("t", "%d − %d = %d" % (tens, b, T))))
        beats.append(B("The %d ones were never touched, so put them back. %d and %d make %d." % (ones, T, ones, d),
                       W("j", "%d + %d = %d" % (T, ones, d))))
        beats.append(answer)
        beats.append(check)
        beats.append(B("So when you take away a round number, only the tens change. The ones stay as they are."))
        return lesson(*beats, origin="rule")

    if d < 10 and _tens(a) == _tens(b):
        beats.append(B("Look how close these two numbers are. So here is a neat way: ask how far it is from %d up to %d." % (b, a),
                       M("q", str(b), "underline"), M("q", str(a), "underline"), hop_figure(qid)))
        beats.append(B("Count the hops from %d up to %d. How many are there?" % (b, a),
                       ask=ask_of(qid, "a1", str(d), rivals(q, [str(d + 1), str(a + b)]),
                                  "Start at %d and hop up one at a time until you reach %d. That takes %d hops." % (b, a, d))))
        beats.append(B("%d hops. So %d and %d more make %d." % (d, b, d, a), W("u", "%d + %d = %d" % (b, d, a))))
        beats.append(answer)
        beats.append(B("The answer cannot be a big number here, because %d and %d are almost the same size." % (a, b)))
        beats.append(B("So when two numbers are close together, count up from the smaller one to the bigger one."))
        return lesson(*beats, origin="rule")

    tb, ob = _tens(b), b % 10
    mid = a - tb
    beats.append(B(pick(qid, "split", ["Let us take the %d away in two easy pieces. Split it into %d and %d.",
                                       "Taking away %d in one go is hard. So split it into %d and %d."]) % (b, tb, ob),
                   W("sp", "%d = %d + %d" % (b, tb, ob))))
    beats.append(B("Take the tens away first. What is %d take away %d?" % (a, tb),
                   ask=ask_of(qid, "a1", str(mid), [str(a + tb), str(mid + 10) if mid + 10 != a else str(mid - 10)],
                              "Only the tens change. %s take away %s leaves %s, and the %s stay. That is %d."
                              % (tw(tens // 10), tw(tb // 10), tw((tens - tb) // 10) if tens != tb else "no tens", ow(ones) if ones != 1 else "ones", mid))))
    beats.append(B("Only the tens change, and the ones stay. So we have %d." % mid, W("t", "%d − %d = %d" % (a, tb, mid))))
    if ones >= ob:
        left = "nothing in the ones place" if ones == ob else "%d" % d
        beats.append(B("Now take away the %d ones. %d take away %d is %d." % (ob, mid, ob, d), W("j", "%d − %d = %d" % (mid, ob, d))))
    else:
        rest = ob - ones
        rnd = mid - ones
        beats.append(B("Now take away the %d. Careful here: %d has only %d ones. So take %d first, to land on %d." % (ob, mid, ones, ones, rnd),
                       W("j1", "%d − %d = %d" % (mid, ones, rnd))))
        beats.append(B("%d is %d and %d, so there are %d more to take. %d take away %d is %d." % (ob, ones, rest, rest, rnd, rest, d),
                       W("j2", "%d − %d = %d" % (rnd, rest, d))))
    beats.append(answer)
    beats.append(check)
    beats.append(B(pick(qid, "sum", ["So the plan is: take away the tens first, then take away the ones.",
                                     "Split the number you are taking away. Tens first, then ones."])))
    return lesson(*beats, origin="rule")
