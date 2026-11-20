"""Rule-written lessons: the LCM and the HCF of two numbers, then one more step.

    Difference between LCM and HCF of a and b?        -> lcm_hcf_lesson(qid, a, b, "diff")
    Sum of LCM and HCF of a and b?                    -> lcm_hcf_lesson(qid, a, b, "sum")
    LCM of a and b divided by HCF of a and b?         -> lcm_hcf_lesson(qid, a, b, "ratio")

Both are found from prime factors, as the bank's own steps do.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANSM, B, CHOOSE, CIRC, GIVEN, GROUP, LB, LESSON, W,
    count_of, factor_marks, factor_write, gcd, join_times, lcm, only, pf, pick, say_list, say_times,
    shared, shuffled,
)
from g4_gr4_factors_rules import factor_say  # noqa: E402


def shared_marks(line, n, sh):
    marks = factor_marks(line, n, sh)
    if len(marks) == 1:
        return marks
    return [GROUP(line, [m["target"] for m in marks], "shared")]


def lcm_hcf_lesson(qid, a, b, kind):
    g, m = gcd(a, b), lcm(a, b)
    sh = shared(a, b)
    fa, fb, fm = pf(a), pf(b), pf(m)
    if kind == "diff":
        given = "LCM − HCF of %d and %d = ?" % (a, b)
        intro = "We need the difference between the L C M and the H C F of %d and %d. That is three jobs: find the H C F, find the L C M, then subtract." % (a, b)
        result = m - g
        final = "%d − %d" % (m, g)
        others = ["%d + %d" % (m, g), "%d − %d" % (max(a, b), min(a, b))]
        if_not = "Difference means subtract. And it is the L C M and the H C F that we subtract, not the two numbers we started with."
        tell = "%d minus %d is %d." % (m, g, result)
        close = "Read the last word of the question with care: difference means subtract. And do finish the last step. The L C M on its own is not the answer."
    elif kind == "sum":
        given = "LCM + HCF of %d and %d = ?" % (a, b)
        intro = "We need the sum of the L C M and the H C F of %d and %d. That is three jobs: find the H C F, find the L C M, then add them." % (a, b)
        result = m + g
        final = "%d + %d" % (m, g)
        others = ["%d − %d" % (m, g), "%d + %d" % (a, b)]
        if_not = "Sum means add. And it is the L C M and the H C F that we add, not the two numbers we started with."
        tell = "%d plus %d is %d." % (m, g, result)
        close = "Read the question with care: sum means add, difference means subtract. And do finish the last step. The L C M on its own is not the answer."
    else:
        given = "(LCM of %d and %d) ÷ (HCF of %d and %d) = ?" % (a, b, a, b)
        intro = "We must divide the L C M of %d and %d by their H C F. That is three jobs: find the H C F, find the L C M, then divide." % (a, b)
        result = m // g
        final = "%d ÷ %d" % (m, g)
        others = ["%d − %d" % (m, g), "%d ÷ %d" % (max(a, b), min(a, b))]
        if_not = "The question says the L C M divided by the H C F. So the L C M goes first, and we divide it by the H C F."
        tell = "%d divided by %d is %d." % (m, g, result)
        close = None

    beats = [B(intro, GIVEN("q", given))]
    beats.append(B("Start by breaking each number into prime factors, the building blocks it is made of."))
    beats.append(B(factor_say(qid, a, "fa"), factor_write("la", a)))
    beats.append(B(factor_say(qid, b, "fb"), factor_write("lb", b)))

    right = join_times(sh)
    distinct = sorted(set(sh))
    if len(sh) > len(distinct):
        third = join_times(distinct)
    elif len(distinct) >= 2:
        third = str(distinct[0])
    else:
        spare = [p for p in only(a, b) + only(b, a) if str(p) != right]
        third = str(spare[0]) if spare else "1"
    choices, at = shuffled(qid, "shared", right, [join_times(fm), third])
    beats.append(B(
        "First the H C F. It is built only from the primes that both numbers have. Which of these is exactly what %d and %d share?" % (a, b),
        ask=CHOOSE(choices, at,
                   "Look for the primes that sit on both lines. A prime that only one number has cannot divide the other one, so it stays out.")))
    have = say_list([count_of(sh.count(p), p) if sh.count(p) > 1 else "%s %d" % ("an" if p == 11 else "a", p) for p in distinct])
    ops = shared_marks("la", a, sh) + shared_marks("lb", b, sh)
    if len(sh) > 1:
        ops.append(W("m", "%s = %d" % (right, g)))
        say = "Both lines have %s. %s is %d, so the H C F is %d." % (have, say_times(sh), g, g)
    else:
        say = "Both lines have %s, and nothing else in common. So the H C F is %d." % (have, g)
    ops.append(LB("h", "HCF = %d" % g))
    beats.append(B(say, *ops))

    need = say_list([count_of(fm.count(p), p) for p in sorted(set(fm))])
    beats.append(B(
        pick(qid, "lcm", [
            "Now the L C M. It must hold all of %d and all of %d. So we take each prime the most times it shows up in one number: %s. Multiply them, and we get %d." % (a, b, need, m),
            "Next the L C M. Both %d and %d must fit inside it. So each prime goes in the most times it appears in one number: %s. Multiplied together, that is %d." % (a, b, need, m),
        ]),
        W("n", "%s = %d" % (join_times(fm), m)), LB("l", "LCM = %d" % m)))
    beats.append(B(
        "A quick check on the L C M. %d divided by %d is %d, and %d divided by %d is %d. Both are exact." % (m, a, m // a, m, b, m // b),
        W("c1", "%d ÷ %d = %d" % (m, a, m // a)), W("c2", "%d ÷ %d = %d" % (m, b, m // b))))
    choices, at = shuffled(qid, "final", final, others)
    beats.append(B(
        "We have the H C F, %d, and the L C M, %d. Now the last job. What do we work out to finish?" % (g, m),
        ask=CHOOSE(choices, at, if_not)))
    beats.append(B(tell + " That is our answer.", ANSM("ans", "%s = %d" % (final, result)),
                   CIRC("ans", str(result), 2 if str(result) in final else 1)))
    if close:
        beats.append(B(close))
    else:
        qa, qb = a // g, b // g
        beats.append(B(
            "Here is something neat. %d is %d times %d, and %d is %d times %d. The leftover parts, %d and %d, multiply to give %d: our answer again." % (
                a, g, qa, b, g, qb, qa, qb, result),
            W("k1", "%d = %d × %d" % (a, g, qa)), W("k2", "%d = %d × %d" % (b, g, qb)), W("k3", "%d × %d = %d" % (qa, qb, result))))
        beats.append(B("So the plan: prime factors first, then the H C F from the shared primes, the L C M from all of them, and last of all the divide."))
    return LESSON(*beats, origin="rule")
