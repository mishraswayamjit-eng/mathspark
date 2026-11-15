"""Rule-written lessons for the generated factors families.

    Find the HCF of a and b.      -> hcf_lesson
    Find the LCM of a and b.      -> lcm_lesson (count up both tables, or prime factors, or "one divides the other")
    Which ... is divisible by d?  -> divisible_lesson
    Solve: ax ± b = c             -> equation_lesson

Every number on the board is computed here; the words adapt to the case.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factors_lib import (  # noqa: E402
    ANS, B, BOTH, CHOOSE, CIRC, DIVIDE, GIVEN, GIVENM, LB, LESSON, NOTE, STRIKE, TREE, UL, VENN, W,
    count_of, factor_line, factor_marks, factor_write, first_divisor_words, gcd, join_times, lcm, nth_at,
    only, pf, pick, pulled_out, say_list, say_plus, say_times, shared, shuffled,
)


def factor_say(qid, n, salt):
    """What the teacher says while writing n as a product of primes."""
    primes = pf(n)
    if len(primes) == 1:
        return "%d is a prime number already. It cannot be split, so we leave it just as it is." % n
    if pick(qid, salt, [0, 1]) == 0:
        if len(primes) == 2:
            return "%s That leaves %d, so %d is %s." % (first_divisor_words(n), primes[1], n, say_times(primes))
        return "%s Keep splitting, and %d is %s." % (first_divisor_words(n), n, say_times(primes))
    return "Take %d. Keep pulling out the smallest prime that fits: %s. So %d is %s." % (
        n, pulled_out(n), n, say_times(primes))


def region(primes):
    return join_times(primes) if primes else "nothing"


# ── HCF ──────────────────────────────────────────────────────────────────────

def hcf_opening(qid, a, b):
    lo = min(a, b)
    given = GIVEN("q", "HCF of %d and %d = ?" % (a, b))
    if pick(qid, "open", [0, 1]) == 0:
        intro = pick(qid, "intro", [
            "Find the H C F of %d and %d. H C F stands for highest common factor: the biggest number that divides both %d and %d exactly." % (a, b, a, b),
            "We need the H C F of %d and %d. That is the highest common factor: the biggest number that goes into both of them with nothing left over." % (a, b),
        ])
        choices, at = shuffled(qid, "bound", "No, it has to fit into %d" % lo, ["Yes, it could be bigger"])
        ask = B("Before we start, a quick thought. Could the H C F be bigger than %d?" % lo,
                ask=CHOOSE(choices, at,
                           "A factor has to fit inside the number it divides. So the H C F can never be bigger than %d, the smaller of our two numbers." % lo))
        plan = pick(qid, "plan", [
            "Here is the plan. We break each number into prime factors, the building blocks that cannot be split any further.",
            "So how do we find it? We split each number into its prime factors, the smallest building blocks it is made of.",
        ])
        return [B(intro, given), ask], plan
    choices, at = shuffled(qid, "mean", "The biggest number dividing both",
                           ["The first number in both tables", "%d × %d" % (a, b)])
    intro = B("Find the H C F of %d and %d. H C F is short for highest common factor. So what are we hunting for?" % (a, b),
              given,
              ask=CHOOSE(choices, at,
                         "A factor is a number that divides exactly. So the highest common factor is the biggest number that divides both %d and %d exactly." % (a, b)))
    plan = pick(qid, "plan", [
        "So we want the biggest number that goes into both %d and %d. The plan: break each number into prime factors, its building blocks." % (a, b),
        "The biggest number that divides both %d and %d: that is our target. To find it, we split each number into its prime factors." % (a, b),
    ])
    return [intro], plan


def hcf_lesson(qid, a, b):
    g = gcd(a, b)
    sh = shared(a, b)
    fa, fb = pf(a), pf(b)
    beats, plan = hcf_opening(qid, a, b)
    beats.append(B(plan, TREE("ta", a)))
    beats.append(B(factor_say(qid, a, "fa"), factor_write("la", a)))
    beats.append(B(factor_say(qid, b, "fb"), TREE("tb", b), factor_write("lb", b)))

    # The turning point: which primes are shared.
    right = join_times(sh)
    every = join_times(pf(lcm(a, b)))
    distinct = sorted(set(sh))
    if len(sh) > len(distinct):
        third = join_times(distinct)
    elif len(distinct) >= 2:
        third = str(distinct[0])
    else:
        spare = [p for p in only(a, b) + only(b, a) if str(p) != right]
        third = str(spare[0]) if spare else "1"
    choices, at = shuffled(qid, "shared", right, [every, third])
    beats.append(B(
        pick(qid, "key", [
            "Now the key idea. The H C F is built only from the primes that both numbers have. Which of these is exactly what %d and %d share?" % (a, b),
            "Here comes the important part. A common factor can only use primes that are in both numbers. So which of these do %d and %d share?" % (a, b),
        ]),
        ask=CHOOSE(choices, at,
                   "Look for the primes that sit on both lines. A prime that only one number has cannot divide the other one, so it stays out.")))

    # Ring the shared primes, and name the trap.
    have = say_list([count_of(sh.count(p), p) if sh.count(p) > 1 else "%s %d" % ("an" if p == 11 else "a", p)
                     for p in distinct])
    trap = ""
    for p in distinct:
        ca, cb = fa.count(p), fb.count(p)
        if ca != cb:
            big, small = (a, b) if ca > cb else (b, a)
            n = min(ca, cb)
            trap = " Careful: %d has %s, but %d has only %s. So only %s %s shared." % (
                big, count_of(max(ca, cb), p), small, count_of(n, p), count_of(n, p), "is" if n == 1 else "are")
            break
    if not trap:
        oa, ob = sorted(set(only(a, b))), sorted(set(only(b, a)))
        bits = []
        if oa:
            bits.append("the %d belongs only to %d" % (oa[0], a))
        if ob:
            bits.append("the %d belongs only to %d" % (ob[0], b))
        if bits:
            text = " and ".join(bits)
            trap = " %s%s, so %s out." % (text[0].upper(), text[1:], "they stay" if len(bits) == 2 else "it stays")
    marks = factor_marks("la", a, sh) + factor_marks("lb", b, sh)
    assert len(marks) <= 6, qid
    ring = pick(qid, "ring", ["Ring them on the board.", "Let's ring them.", "Circle them on both lines."])
    beats.append(B("%s Both lines have %s.%s" % (ring, have, trap), *marks))

    venn = VENN("v", "Primes of %d" % a, "Primes of %d" % b, region(only(a, b)), region(sh), region(only(b, a)),
                highlight=["both"], note="The overlap holds the primes both numbers share.")
    if len(sh) > 1:
        beats.append(B(
            "The overlap in the picture shows what they share. Multiply those together: %s is %d. So the H C F is %d." % (say_times(sh), g, g),
            venn, W("m", "%s = %d" % (right, g)), ANS("ans", "HCF = %d" % g), CIRC("ans", "HCF = %d" % g)))
    else:
        beats.append(B(
            "The overlap in the picture shows what they share: just the %d. So the H C F is %d." % (g, g),
            venn, ANS("ans", "HCF = %d" % g), CIRC("ans", "HCF = %d" % g)))

    qa, qb = a // g, b // g
    beats.append(B(
        pick(qid, "check", [
            "Let's check. %d divided by %d is %d, and %d divided by %d is %d, with nothing left over. And %d and %d share no factor, so nothing bigger would work." % (a, g, qa, b, g, qb, qa, qb),
            "Good mathematicians always check. %d divided by %d is %d, and %d divided by %d is %d. Both divide exactly, and %d and %d have nothing more in common." % (a, g, qa, b, g, qb, qa, qb),
        ]),
        W("c1", "%d ÷ %d = %d" % (a, g, qa)), W("c2", "%d ÷ %d = %d" % (b, g, qb))))
    beats.append(B(pick(qid, "sum", [
        "So the plan for any H C F: break both numbers into primes, keep only the primes they share, and multiply those. Your turn next!",
        "Remember the three moves: split into primes, ring what is shared, multiply. And the H C F is never bigger than the smaller number.",
        "That is the whole method. Split both numbers into primes, ring the ones on both lines, and multiply what you ringed.",
    ])))
    return LESSON(*beats, origin="rule")
