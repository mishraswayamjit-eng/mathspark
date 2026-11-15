"""Rule-written lessons: Find the LCM of a and b.

Three ways, chosen by the numbers, and the teacher says which and why:
  - one number is a multiple of the other: the bigger one is the LCM;
  - small numbers: count up both tables until they meet;
  - otherwise: prime factors, each prime the most times it appears.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from factors_lib import (  # noqa: E402
    ANS, B, CHOOSE, CIRC, GIVEN, LB, LESSON, TREE, VENN, W,
    count_of, factor_marks, factor_write, gcd, join_times, lcm, nth_at, only, pf, pick, say_list,
    say_times, shared, shuffled,
)
from factors_rules import factor_say, region  # noqa: E402


def lcm_opening(qid, a, b):
    """The first beats: what an LCM is, and the child's first turn."""
    hi = max(a, b)
    given = GIVEN("q", "LCM of %d and %d = ?" % (a, b))
    if pick(qid, "open", [0, 1]) == 0:
        intro = pick(qid, "intro", [
            "Find the L C M of %d and %d. L C M stands for lowest common multiple: the first number both %d and %d will reach when you count up in their tables." % (a, b, a, b),
            "We need the L C M of %d and %d. That is the lowest common multiple: the first number that is in the %d times table and in the %d times table." % (a, b, a, b),
        ])
        choices, at = shuffled(qid, "bound", "No, %d has to fit into it" % hi, ["Yes, it could be smaller"])
        ask = B("Before we start, a quick thought. Could the L C M be smaller than %d?" % hi,
                ask=CHOOSE(choices, at,
                           "A multiple of %d is %d or something bigger. So the L C M can never be smaller than %d, the bigger of our two numbers." % (hi, hi, hi)))
        return [B(intro, given), ask], ""
    choices, at = shuffled(qid, "mean", "The first number in both tables",
                           ["The biggest number dividing both", "%d + %d" % (a, b)])
    intro = B("Find the L C M of %d and %d. L C M is short for lowest common multiple. So what are we hunting for?" % (a, b),
              given,
              ask=CHOOSE(choices, at,
                         "A multiple of a number is anything in its times table. So the lowest common multiple is the first number that is in both tables."))
    lead = pick(qid, "lead", [
        "So we want the first number that both tables reach. ",
        "The first number in both tables: that is our target. ",
    ])
    return [intro], lead


def table_line(n, count):
    """('Multiples of 6: 6, 12, 18', {6: pos, 12: pos, 18: pos})."""
    text = "Multiples of %d: " % n
    places = {}
    for i in range(1, count + 1):
        if i > 1:
            text += ", "
        places[n * i] = len(text)
        text += str(n * i)
    return text, places


def circle_in_table(id, n, count, value):
    text, places = table_line(n, count)
    return CIRC(id, str(value), nth_at(text, str(value), places[value]))


def lcm_divides(qid, a, b, beats, lead):
    """One number is a multiple of the other."""
    big, small = max(a, b), min(a, b)
    k = big // small
    beats.append(B(
        lead + "Look closely at these two numbers. %d is in the %d times table: %d times %d is %d." % (big, small, small, k, big),
        W("n", "%d × %d = %d" % (small, k, big))))
    choices, at = shuffled(qid, "div", str(big), [str(small * big), str(small)])
    beats.append(B(
        "So where do the two tables first meet?",
        ask=CHOOSE(choices, at,
                   "%d is the very first number in its own table, and we just saw it is in the %d times table too. So the two tables first meet at %d." % (big, small, big))))
    ta, _ = table_line(small, k + 1)
    tb, _ = table_line(big, 2)
    beats.append(B(
        "Here are both tables. %d is in each of them, and nothing smaller can be, because %d is where its own table starts. So the L C M is %d." % (big, big, big),
        LB("la", ta), LB("lb", tb), circle_in_table("la", small, k + 1, big), circle_in_table("lb", big, 2, big),
        ANS("ans", "LCM = %d" % big), CIRC("ans", "LCM = %d" % big)))
    beats.append(B(
        "One trap to watch for: do not just multiply them. %d times %d is %d, which is a common multiple, but not the lowest one." % (small, big, small * big),
        W("t", "%d × %d = %d" % (small, big, small * big))))
    beats.append(B(pick(qid, "sum", [
        "So here is a shortcut worth keeping. When one number is a multiple of the other, the bigger number is the L C M straight away.",
        "Remember this one. If the bigger number is already in the smaller number's table, the bigger number is the L C M.",
    ])))


def lcm_tables(qid, a, b, beats, lead):
    """Small numbers: count up both tables until they meet."""
    m = lcm(a, b)
    ka, kb = m // a + 1, m // b + 1
    ta, _ = table_line(a, ka)
    tb, _ = table_line(b, kb)
    beats.append(B(
        pick(qid, "why", [
            "These numbers are small, so the simplest way is to count up in both tables until they meet. Count up in %ds: %s." % (a, ", ".join(str(a * i) for i in range(1, ka + 1))),
            "With small numbers like these we can just write out both tables and watch for a match. First the %ds: %s." % (a, ", ".join(str(a * i) for i in range(1, ka + 1))),
        ]),
        LB("la", ta)))
    beats.append(B("Now count up in %ds: %s." % (b, ", ".join(str(b * i) for i in range(1, kb + 1))), LB("lb", tb)))
    other = str(a * b) if a * b != m else str(a + b)
    choices, at = shuffled(qid, "tab", str(m), [other, str(max(a, b))])
    beats.append(B(
        "Look along both lists. What is the L C M of %d and %d?" % (a, b),
        ask=CHOOSE(choices, at,
                   "We want the first number that shows up in both lists. Run a finger along each one: %d is in both, and nothing before it is." % m)))
    beats.append(B(
        pick(qid, "found", [
            "There it is. %d is the first number in both lists, so the L C M is %d." % (m, m),
            "%d is in both lists, and nothing before it is. So the L C M is %d." % (m, m),
        ]),
        circle_in_table("la", a, ka, m), circle_in_table("lb", b, kb, m),
        ANS("ans", "LCM = %d" % m), CIRC("ans", "LCM = %d" % m)))
    beats.append(B(
        "Let's check. %d divided by %d is %d, and %d divided by %d is %d. Both divide exactly, so %d really is a multiple of each." % (m, a, m // a, m, b, m // b, m),
        W("c1", "%d ÷ %d = %d" % (m, a, m // a)), W("c2", "%d ÷ %d = %d" % (m, b, m // b))))
    if a * b != m:
        beats.append(B(
            "One trap to watch for. Multiplying %d by %d gives %d, which is a common multiple, but not the lowest one. %d gets there first." % (a, b, a * b, m),
            W("t", "%d × %d = %d" % (a, b, a * b))))
    else:
        beats.append(B(
            "Did you notice? Here the L C M is just %d times %d. That happens when the two numbers share no factor except 1." % (a, b),
            W("t", "%d × %d = %d" % (a, b, a * b))))
    beats.append(B(pick(qid, "sum", [
        "So for small numbers: count up in both tables, and the first number in both is the L C M. Your turn next!",
        "That is the idea of an L C M: the first meeting point of the two tables. Write out the multiples and look for the first match.",
    ])))


def lcm_primes(qid, a, b, beats, lead):
    """Bigger numbers: each prime the most times it appears in either number."""
    m = lcm(a, b)
    fa, fb, fm = pf(a), pf(b), pf(m)
    sh = shared(a, b)
    tree_a = [TREE("ta", a)] if len(fa) > 1 else []
    tree_b = [TREE("tb", b)] if len(fb) > 1 else []
    beats.append(B(
        lead + pick(qid, "why", [
            "Counting up in %ds and %ds would take a while. So we build the L C M from prime factors instead, the building blocks of each number." % (a, b),
            "We could count up both tables, but with %d and %d that is a long walk. Prime factors get us there faster." % (a, b),
        ]),
        *tree_a))
    beats.append(B(factor_say(qid, a, "fa"), factor_write("la", a)))
    beats.append(B(factor_say(qid, b, "fb"), *(tree_b + [factor_write("lb", b)])))

    right = join_times(fm)
    if sh:
        others = [join_times(sh), join_times(sorted(fa + fb))]
    else:
        big = max(a, b)
        others = [join_times(pf(big)), join_times(sorted(set(fm))) if len(set(fm)) < len(fm) else str(fm[0])]
    if others[1] == right or others[1] == others[0]:
        others[1] = "1"
    choices, at = shuffled(qid, "build", right, others)
    beats.append(B(
        pick(qid, "key", [
            "Now the key idea. The L C M must contain all of %d and all of %d. So we take each prime the most times it appears in one number. Which of these builds the L C M?" % (a, b),
            "Here is the important part. Both %d and %d must fit inside the L C M. So each prime goes in the most times it shows up in either number. Which of these does that?" % (a, b),
        ]),
        ask=CHOOSE(choices, at,
                   "The L C M has to hold all of %d and all of %d, but nothing twice over. So each prime goes in the most times it shows up in one number." % (a, b))))

    # Box the picks: each prime on the line where it appears most.
    from_a, from_b = [], []
    for p in sorted(set(fm)):
        if fa.count(p) >= fb.count(p):
            from_a += [p] * fa.count(p)
        else:
            from_b += [p] * fb.count(p)
    marks = factor_marks("la", a, from_a, "box") + factor_marks("lb", b, from_b, "box")
    assert len(marks) <= 6, qid

    def some(n, p):
        return "the %d" % p if n == 1 else count_of(n, p)

    def picks(primes):
        return say_list([some(primes.count(p), p) for p in sorted(set(primes))])

    def source(primes, n):
        return "%d itself" % n if len(pf(n)) == 1 else "%s from %d" % (picks(primes), n)

    if from_a and from_b:
        say = "Box our picks: %s, and %s." % (source(from_a, a), source(from_b, b))
    elif from_a:
        say = "Box our picks. Everything we need is already in %d: %s." % (a, picks(from_a))
    else:
        say = "Box our picks. Everything we need is already in %d: %s." % (b, picks(from_b))
    if sh:
        p = sh[0]
        if fa.count(p) >= fb.count(p):
            winner, loser, n, less = a, b, fa.count(p), fb.count(p)
        else:
            winner, loser, n, less = b, a, fb.count(p), fa.count(p)
        say += " Careful: we do not add %s in %d on top, because %s from %d already cover%s %s." % (
            some(less, p) if less == 1 else "the " + some(less, p), loser,
            some(n, p) if n == 1 else "the " + some(n, p), winner,
            "s" if n == 1 else "", "it" if less == 1 else "them")
    else:
        say += " These two share no prime at all, so every prime goes in."
    beats.append(B(say, *marks))

    beats.append(B(
        "In the picture, the L C M is everything, counted once. %s is %d. So the L C M is %d." % (say_times(fm), m, m),
        VENN("v", "Primes of %d" % a, "Primes of %d" % b, region(only(a, b)), region(sh), region(only(b, a)),
             highlight=["left", "both", "right"], note="The L C M uses every prime in the picture, once each."),
        W("m", "%s = %d" % (right, m)), ANS("ans", "LCM = %d" % m), CIRC("ans", "LCM = %d" % m)))
    beats.append(B(
        pick(qid, "check", [
            "Let's check. %d divided by %d is %d, and %d divided by %d is %d. Both divide exactly, so %d is a multiple of each." % (m, a, m // a, m, b, m // b, m),
            "Good mathematicians always check. %d divided by %d is %d, and %d divided by %d is %d, with nothing left over." % (m, a, m // a, m, b, m // b),
        ]),
        W("c1", "%d ÷ %d = %d" % (m, a, m // a)), W("c2", "%d ÷ %d = %d" % (m, b, m // b))))
    beats.append(B(pick(qid, "sum", [
        "So for an L C M with bigger numbers: split both into primes, then take each prime the most times it appears in one number. Multiply, and you are done!",
        "Remember the difference. For an H C F we keep only the shared primes. For an L C M we take every prime, the most times it appears.",
    ])))


def lcm_lesson(qid, a, b):
    m = lcm(a, b)
    beats, lead = lcm_opening(qid, a, b)
    if m == max(a, b):
        lcm_divides(qid, a, b, beats, lead)
    elif max(m // a, m // b) <= 6 and max(a, b) <= 20:
        lcm_tables(qid, a, b, beats, lead)
    else:
        lcm_primes(qid, a, b, beats, lead)
    return LESSON(*beats, origin="rule")
