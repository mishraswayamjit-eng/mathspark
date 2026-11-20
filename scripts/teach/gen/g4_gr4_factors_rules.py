"""Rule-written lessons for the Grade 4 factors families: HCF.

    Find the HCF of a and b.   -> hcf_lesson
        small numbers: list the factors of each, and take the biggest number in both lists;
        a number with a long list of factors: prime factors, and multiply the shared ones.

Every number on the board is computed here; the words adapt to the case.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANS, B, CHOOSE, CIRC, GIVEN, LB, LESSON, TREE, VENN, W,
    count_of, factor_marks, factor_write, factors, first_divisor_words, gcd, join_times, lcm, list_line,
    mark_in, only, pairs, pf, pick, pulled_out, say_list, say_times, shared, shuffled,
)


def hcf_by_lists(a, b):
    return len(factors(a)) <= 9 and len(factors(b)) <= 9


def factor_say(qid, n, salt):
    """What the teacher says while writing n as a product of primes."""
    primes = pf(n)
    if len(primes) == 1:
        return "%d is a prime number already. It cannot be split, so we leave it as it is." % n
    if len(set(primes)) == 1:
        return "Take %d. It is made only of %ds: %s." % (n, primes[0], say_times(primes))
    if pick(qid, salt, [0, 1]) == 0:
        if len(primes) == 2:
            return "%s That leaves %d, so %d is %s." % (first_divisor_words(n), primes[1], n, say_times(primes))
        return "%s Keep splitting, and %d is %s." % (first_divisor_words(n), n, say_times(primes))
    return "Take %d. Keep pulling out the smallest prime that fits: %s. So %d is %s." % (
        n, pulled_out(n), n, say_times(primes))


def region(primes):
    return join_times(primes) if primes else "nothing"


def hcf_opening(qid, a, b, plans):
    """The first beats: what an HCF is, and the child's first turn. Returns (beats, plan sentence)."""
    lo = min(a, b)
    given = GIVEN("q", "HCF of %d and %d = ?" % (a, b))
    if pick(qid, "open", [0, 1]) == 0:
        intro = pick(qid, "intro", [
            "Find the H C F of %d and %d. H C F means highest common factor: the biggest number that divides both %d and %d exactly." % (a, b, a, b),
            "We need the H C F of %d and %d. That is the highest common factor: the biggest number that goes into both, with nothing left over." % (a, b),
        ])
        choices, at = shuffled(qid, "bound", "No, it must fit into %d" % lo, ["Yes, it could be bigger"])
        ask = B("Before we start, a quick thought. Could the H C F be bigger than %d?" % lo,
                ask=CHOOSE(choices, at,
                           "A factor has to fit inside the number it divides. So the H C F can never be bigger than %d, the smaller of our two numbers." % lo))
        return [B(intro, given), ask], pick(qid, "plan", plans[0])
    choices, at = shuffled(qid, "mean", "The biggest number dividing both",
                           ["The first number in both tables", "%d × %d" % (a, b)])
    intro = B("Find the H C F of %d and %d. H C F is short for highest common factor. So what are we looking for?" % (a, b),
              given,
              ask=CHOOSE(choices, at,
                         "A factor is a number that divides exactly. So the highest common factor is the biggest number that divides both %d and %d exactly." % (a, b)))
    return [intro], pick(qid, "plan", plans[1])


# ── HCF by listing factors ───────────────────────────────────────────────────

def pairs_say(n):
    return say_list(["%d times %d" % p for p in pairs(n)])


def list_factors_beat(qid, n, line_id, lead, first):
    fs = factors(n)
    text, _ = list_line("Factors of %d: " % n, fs)
    if len(fs) == 2:
        say = "%s%d is a prime number. Only 1 times %d makes it, so its factors are just 1 and %d." % (lead, n, n, n)
    elif first:
        say = "%sFactors come in pairs that multiply to make %d: %s. So the factors of %d are %s." % (
            lead, n, pairs_say(n), n, say_list(fs))
    else:
        say = pick(qid, "second", [
            "Now %d. Its pairs are %s. So the factors of %d are %s.",
            "Do the same for %d. The pairs are %s. That gives the factors of %d: %s.",
        ]) % (n, pairs_say(n), n, say_list(fs))
    if len(say) > 235:
        say = "%sThe factors of %d are %s." % (lead if first else "Now %d. " % n, n, say_list(fs))
    return B(say, LB(line_id, text))


def hcf_lists(qid, a, b):
    g = gcd(a, b)
    lo, hi = min(a, b), max(a, b)
    fa, fb = factors(a), factors(b)
    common = [f for f in fa if f in fb]
    beats, plan = hcf_opening(qid, a, b, (
        ["Here is the plan. These numbers have only a few factors, so we list every factor of each one. Then we look for the biggest number in both lists. ",
         "So how do we find it? We write down all the factors of each number. Then we pick the biggest one they share. "],
        ["So we want the biggest number that goes into both. These numbers have only a few factors, so let's list them all. ",
         "The biggest number that divides both: that is our target. Let's write down every factor of each number. "],
    ))
    beats.append(B(plan.strip()))
    beats.append(list_factors_beat(qid, a, "la", "", True))
    beats.append(list_factors_beat(qid, b, "lb", "", False))

    # The child's turn: the biggest number in both lists.
    if g == lo:
        d1 = hi
    else:
        d1 = max(f for f in factors(lo) if f not in common)
    smaller = [f for f in common if 1 < f < g]
    if smaller:
        d2 = max(smaller)
    else:
        spare = [f for f in factors(hi) if f not in common and f not in (d1, hi)] or [f for f in factors(lo) if f not in common and f != d1]
        d2 = spare[0] if spare else 1
    choices, at = shuffled(qid, "big", str(g), [str(d1), str(d2)])
    beats.append(B(
        pick(qid, "key", [
            "Now look along both lists. Which is the biggest number that is in both of them?",
            "Here is the important part. Run a finger along both lists. What is the biggest number that shows up in both?",
        ]),
        ask=CHOOSE(choices, at,
                   "It has to be in both lists, not just one. Check each number against the other list, and take the biggest one that is in both.")))

    ca = "Factors of %d: " % a
    cb = "Factors of %d: " % b
    ctext, _ = list_line("In both lists: ", common)
    if len(common) == 1:
        both_say = "The only number in both lists is 1."
    else:
        both_say = "The numbers in both lists are %s. These are the common factors, and the biggest is %d." % (say_list(common), g)
    trap = ""
    if g == lo:
        trap = " Did you see? %d itself divides %d, so the smaller number is the H C F." % (lo, hi)
    elif lo not in common:
        trap = " Careful: %d is in its own list, but it does not divide %d, so it is out." % (lo, hi)
    beats.append(B(both_say + trap, LB("lc", ctext), mark_in("la", ca, fa, g), mark_in("lb", cb, fb, g),
                   mark_in("lc", "In both lists: ", common, g)))

    def side(nums):
        return ", ".join(str(n) for n in nums) if nums else "none"

    beats.append(B(
        pick(qid, "ans", [
            "The picture shows it too: the shared factors sit in the middle. So the H C F of %d and %d is %d." % (a, b, g),
            "In the picture, the middle part holds the factors they share. The biggest one there is %d, so the H C F is %d." % (g, g),
        ]),
        VENN("v", "Factors of %d" % a, "Factors of %d" % b, side([f for f in fa if f not in common]), side(common),
             side([f for f in fb if f not in common]), highlight=["both"], note="The middle holds the common factors."),
        ANS("ans", "HCF = %d" % g), CIRC("ans", "HCF = %d" % g)))

    qa, qb = a // g, b // g
    beats.append(B(
        pick(qid, "check", [
            "Let's check. %d divided by %d is %d, and %d divided by %d is %d. Nothing is left over either time." % (a, g, qa, b, g, qb),
            "Good mathematicians always check. %d divided by %d is %d, and %d divided by %d is %d. Both divide exactly." % (a, g, qa, b, g, qb),
        ]),
        W("c1", "%d ÷ %d = %d" % (a, g, qa)), W("c2", "%d ÷ %d = %d" % (b, g, qb))))
    beats.append(B(pick(qid, "sum", [
        "So the plan for an H C F like this one: list the factors of each number, find the ones in both lists, and take the biggest. Your turn next!",
        "Remember the three moves: list the factors, spot the common ones, pick the biggest. And the H C F is never bigger than the smaller number.",
        "That is the whole method. Write both lists of factors, look for the numbers in both, and the biggest of those is the H C F.",
    ])))
    return LESSON(*beats, origin="rule")


# ── HCF by prime factors ─────────────────────────────────────────────────────

def hcf_primes(qid, a, b):
    g = gcd(a, b)
    sh = shared(a, b)
    fa, fb = pf(a), pf(b)
    beats, plan = hcf_opening(qid, a, b, (
        ["Here is the plan. These numbers have lots of factors, so listing them all is slow. We break each number into prime factors, its smallest building blocks.",
         "So how do we find it? Listing every factor would take a while. Instead we split each number into prime factors, the building blocks it is made of."],
        ["So we want the biggest number that goes into both. Listing every factor would be slow, so we break each number into prime factors instead.",
         "The biggest number that divides both: that is our target. To find it, we split each number into prime factors, its building blocks."],
    ))
    beats.append(B(plan, TREE("ta", a)))
    beats.append(B(factor_say(qid, a, "fa"), factor_write("la", a)))
    beats.append(B(factor_say(qid, b, "fb"), TREE("tb", b), factor_write("lb", b)))

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
                highlight=["both"], note="The middle holds the primes both numbers share.")
    if len(sh) > 1:
        beats.append(B(
            "The middle of the picture shows what they share. Multiply those together: %s is %d. So the H C F is %d." % (say_times(sh), g, g),
            venn, W("m", "%s = %d" % (right, g)), ANS("ans", "HCF = %d" % g), CIRC("ans", "HCF = %d" % g)))
    else:
        beats.append(B(
            "The middle of the picture shows what they share: just the %d. So the H C F is %d." % (g, g),
            venn, ANS("ans", "HCF = %d" % g), CIRC("ans", "HCF = %d" % g)))

    qa, qb = a // g, b // g
    beats.append(B(
        pick(qid, "check", [
            "Let's check. %d divided by %d is %d, and %d divided by %d is %d, with nothing left over. And %d and %d share no factor except 1, so nothing bigger works." % (a, g, qa, b, g, qb, qa, qb),
            "Good mathematicians always check. %d divided by %d is %d, and %d divided by %d is %d. Both divide exactly, and %d and %d have nothing more in common." % (a, g, qa, b, g, qb, qa, qb),
        ]),
        W("c1", "%d ÷ %d = %d" % (a, g, qa)), W("c2", "%d ÷ %d = %d" % (b, g, qb))))
    beats.append(B(pick(qid, "sum", [
        "So the plan for an H C F of bigger numbers: break both into primes, keep only the primes they share, and multiply those. Your turn next!",
        "Remember the three moves: split into primes, ring what is shared, multiply. And the H C F is never bigger than the smaller number.",
        "That is the whole method. Split both numbers into primes, ring the ones on both lines, and multiply what you ringed.",
    ])))
    return LESSON(*beats, origin="rule")


def hcf_divides(qid, a, b):
    """The smaller number divides the bigger one, so it is the HCF."""
    lo, hi = min(a, b), max(a, b)
    k = hi // lo
    p = pf(lo)[0]
    part = lo // p
    beats, plan = hcf_opening(qid, a, b, (
        ["Before any long working, look closely at the two numbers. ", "Here is a tip: always look at the two numbers first. "],
        ["So we want the biggest number that goes into both. Look closely at the two numbers first. ",
         "The biggest number that divides both: that is our target. Before any long working, look at the numbers. "],
    ))
    beats.append(B(plan + "%d is in the %d times table: %d times %d is %d." % (hi, lo, lo, k, hi),
                   W("n", "%d × %d = %d" % (lo, k, hi))))
    choices, at = shuffled(qid, "self", str(lo), [str(part), str(hi)])
    beats.append(B(
        "So %d divides %d. Now think about %d on its own. What is the biggest factor of %d?" % (lo, hi, lo, lo),
        ask=CHOOSE(choices, at,
                   "Every number divides itself exactly. So the biggest factor of %d is %d itself. Nothing bigger can fit into it." % (lo, lo))))
    beats.append(B(
        "%d divides itself, and %d divides %d. So it is a common factor, and nothing bigger can fit into %d. The H C F is %d." % (lo, lo, hi, lo, lo),
        W("c1", "%d ÷ %d = 1" % (lo, lo)), W("c2", "%d ÷ %d = %d" % (hi, lo, k)),
        ANS("ans", "HCF = %d" % lo), CIRC("ans", "HCF = %d" % lo)))
    if part > 1:
        beats.append(B(
            "One trap to watch for. %d divides both numbers too, so it is a common factor. But it is not the highest one. %d beats it." % (part, lo),
            W("t1", "%d ÷ %d = %d" % (lo, part, p)), W("t2", "%d ÷ %d = %d" % (hi, part, hi // part))))
    else:
        beats.append(B("And %d cannot be the answer: it is far too big to fit into %d." % (hi, lo)))
    beats.append(B(pick(qid, "sum", [
        "So here is a shortcut worth keeping. When the smaller number divides the bigger one, the smaller number is the H C F straight away.",
        "Remember this one. If the bigger number is in the smaller number's table, the smaller number is the H C F.",
    ])))
    return LESSON(*beats, origin="rule")


def hcf_how(a, b):
    if max(a, b) % min(a, b) == 0:
        return "one divides the other"
    return "list the factors" if hcf_by_lists(a, b) else "prime factors"


def hcf_lesson(qid, a, b):
    if max(a, b) % min(a, b) == 0:
        return hcf_divides(qid, a, b)
    if hcf_by_lists(a, b):
        return hcf_lists(qid, a, b)
    return hcf_primes(qid, a, b)
