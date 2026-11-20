"""Rule-written lessons for the Grade 4 factors families: LCM, counting factors, counting multiples.

    Find the LCM of a and b.                        -> lcm_lesson
        one number is a multiple of the other: the bigger one is the LCM;
        both tables fit on the board: count up both until they meet;
        otherwise: count up in the bigger number and test each one with the smaller.
    How many factors does n have?                   -> count_factors_lesson
    How many numbers from lo to hi are divisible by d?  -> count_multiples_lesson

Every number on the board is computed here; the words adapt to the case.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANS, B, CHOOSE, CIRC, FIG, GIVEN, LB, LESSON, TABLE, W,
    factors, gcd, lcm, list_line, mark_in, ordinal, pairs, pick, say_list, shuffled,
)


# ── LCM ──────────────────────────────────────────────────────────────────────

def lcm_opening(qid, a, b):
    """The first beats: what an LCM is, and the child's first turn. Returns (beats, lead-in words)."""
    hi = max(a, b)
    given = GIVEN("q", "LCM of %d and %d = ?" % (a, b))
    if pick(qid, "open", [0, 1]) == 0:
        intro = pick(qid, "intro", [
            "Find the L C M of %d and %d. L C M means lowest common multiple: the first number that both %d and %d reach when you count up in their tables." % (a, b, a, b),
            "We need the L C M of %d and %d. That is the lowest common multiple: the first number that is in the %d times table and in the %d times table." % (a, b, a, b),
        ])
        choices, at = shuffled(qid, "bound", "No, %d must fit into it" % hi, ["Yes, it could be smaller"])
        ask = B("Before we start, a quick thought. Could the L C M be smaller than %d?" % hi,
                ask=CHOOSE(choices, at,
                           "A multiple of %d is %d or something bigger. So the L C M can never be smaller than %d, the bigger of our two numbers." % (hi, hi, hi)))
        return [B(intro, given), ask], ""
    choices, at = shuffled(qid, "mean", "The first number in both tables",
                           ["The biggest number dividing both", "%d + %d" % (a, b)])
    intro = B("Find the L C M of %d and %d. L C M is short for lowest common multiple. So what are we looking for?" % (a, b),
              given,
              ask=CHOOSE(choices, at,
                         "A multiple of a number is anything in its times table. So the lowest common multiple is the first number that is in both tables."))
    return [intro], ""


def table_text(n, count):
    return list_line("Multiples of %d: " % n, [n * i for i in range(1, count + 1)])[0]


def circle_in_table(id, n, count, value):
    return mark_in(id, "Multiples of %d: " % n, [n * i for i in range(1, count + 1)], value)


def counted(n, count):
    return ", ".join(str(n * i) for i in range(1, count + 1))


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
    beats.append(B(
        "Here are both tables. %d is in each of them. Nothing smaller can be, because %d is where its own table starts. So the L C M is %d." % (big, big, big),
        LB("la", table_text(small, k + 1)), LB("lb", table_text(big, 2)),
        circle_in_table("la", small, k + 1, big), circle_in_table("lb", big, 2, big),
        ANS("ans", "LCM = %d" % big), CIRC("ans", "LCM = %d" % big)))
    beats.append(B(
        "One trap to watch for: do not just multiply them. %d times %d is %d. That is a common multiple, but not the lowest one." % (small, big, small * big),
        W("t", "%d × %d = %d" % (small, big, small * big))))
    beats.append(B(pick(qid, "sum", [
        "So here is a shortcut worth keeping. When one number is a multiple of the other, the bigger number is the L C M straight away.",
        "Remember this one. If the bigger number is already in the smaller number's table, the bigger number is the L C M.",
    ])))


def tables_fit(a, b):
    m = lcm(a, b)
    try:
        table_text(a, m // a)
        table_text(b, m // b)
    except AssertionError:
        return False
    return True


def lcm_tables(qid, a, b, beats, lead):
    """Count up both tables until they meet."""
    m = lcm(a, b)
    ka, kb = m // a, m // b
    beats.append(B(
        lead + pick(qid, "why", [
            "The simplest way is to count up in both tables until they meet. Count up in %ds: %s." % (a, counted(a, ka)),
            "Let's write out both tables and watch for a match. First the %ds: %s." % (a, counted(a, ka)),
        ]),
        LB("la", table_text(a, ka))))
    beats.append(B("Now count up in %ds: %s." % (b, counted(b, kb)), LB("lb", table_text(b, kb))))
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
        "Let's check. %d divided by %d is %d, and %d divided by %d is %d. Both divide exactly, so %d really is a multiple of each." % (m, a, ka, m, b, kb, m),
        W("c1", "%d ÷ %d = %d" % (m, a, ka)), W("c2", "%d ÷ %d = %d" % (m, b, kb))))
    if a * b != m:
        beats.append(B(
            "One trap to watch for. Multiplying %d by %d gives %d. That is a common multiple, but not the lowest one. %d gets there first." % (a, b, a * b, m),
            W("t", "%d × %d = %d" % (a, b, a * b))))
    else:
        beats.append(B(
            "Did you notice? Here the L C M is just %d times %d. That happens when the two numbers share no factor except 1." % (a, b),
            W("t", "%d × %d = %d" % (a, b, a * b))))
    beats.append(B(pick(qid, "sum", [
        "So for an L C M: count up in both tables, and the first number in both is the answer. Your turn next!",
        "That is the idea of an L C M: the first meeting point of the two tables. Write out the multiples and look for the first match.",
    ])))


def lcm_bigger_only(qid, a, b, beats, lead):
    """Count up in the bigger number, and test each multiple with the smaller one."""
    m = lcm(a, b)
    big, small = max(a, b), min(a, b)
    kb = m // big
    before = [big * i for i in range(1, kb)]
    beats.append(B(
        lead + "Counting up in %ds would take a long time. Here is a quicker way: count up in the bigger number, %d, and test each one." % (small, big)))
    beats.append(B("Count up in %ds: %s." % (big, counted(big, kb)), LB("la", table_text(big, kb))))
    choices, at = shuffled(qid, "tab", str(m), [str(big), str(big * 2)])
    if small == 5:
        tip = "A number in the 5 times table ends in 0 or 5. Look along the list for the first one that does."
    else:
        tip = "Try dividing each one by %d. It only goes in exactly when we reach %d." % (small, m)
    beats.append(B(
        "Which is the first number in the list that %d divides exactly?" % small,
        ask=CHOOSE(choices, at, tip)))
    why = "Numbers in the 5 times table end in 0 or 5, and %d is the first in our list that does. And yes, " % m if small == 5 else \
        "%d does not go exactly into %s. But " % (small, say_list(before, "or"))
    beats.append(B(
        why + "%d times %d is %d. So the L C M is %d." % (small, m // small, m, m),
        W("n", "%d × %d = %d" % (small, m // small, m)), circle_in_table("la", big, kb, m),
        ANS("ans", "LCM = %d" % m), CIRC("ans", "LCM = %d" % m)))
    beats.append(B(
        "Let's check. %d divided by %d is %d, and %d divided by %d is %d. Both divide exactly." % (m, a, m // a, m, b, m // b),
        W("c1", "%d ÷ %d = %d" % (m, a, m // a)), W("c2", "%d ÷ %d = %d" % (m, b, m // b))))
    if gcd(a, b) == 1:
        beats.append(B("Did you notice? The L C M is just %d times %d. That happens when the two numbers share no factor except 1." % (a, b)))
    beats.append(B(pick(qid, "sum", [
        "So here is a quick way to an L C M: count up in the bigger number, and stop at the first one the smaller number divides.",
        "Remember the trick: write the multiples of the bigger number, and test each with the smaller one. The first that works is the L C M.",
    ])))


def lcm_how(a, b):
    m = lcm(a, b)
    if m == max(a, b):
        return "one divides the other"
    if tables_fit(a, b):
        return "count up both tables"
    return "multiples of the bigger number"


def lcm_lesson(qid, a, b):
    beats, lead = lcm_opening(qid, a, b)
    how = lcm_how(a, b)
    if how == "one divides the other":
        lcm_divides(qid, a, b, beats, lead)
    elif how == "count up both tables":
        lcm_tables(qid, a, b, beats, lead)
    else:
        lcm_bigger_only(qid, a, b, beats, lead)
    return LESSON(*beats, origin="rule")


# ── How many factors does n have? ────────────────────────────────────────────

def pair_text(p):
    return "%d × %d" % p


def pair_say(ps):
    return say_list(["%d times %d" % p for p in ps])


def count_factors_lesson(qid, n):
    ps = pairs(n)
    fs = factors(n)
    square = ps[-1][0] == ps[-1][1]
    count = len(fs)
    assert len(ps) >= 3 and ps[1][0] == 2, "written for an even number with at least 3 pairs"
    beats = []
    beats.append(B(
        pick(qid, "intro", [
            "How many factors does %d have? A factor of %d is a number that divides %d exactly, with nothing left over." % (n, n, n),
            "We are counting the factors of %d. A factor is a number that goes into %d exactly, with nothing left over." % (n, n),
        ]),
        GIVEN("q", "How many factors does %d have?" % n)))
    beats.append(B(
        pick(qid, "pairs", [
            "Here is a neat trick. Factors come in pairs that multiply to make %d. The first pair is easy: 1 times %d." % (n, n),
            "Factors always come with a partner. The two partners multiply to make %d. Start with the easy pair: 1 times %d." % (n, n),
        ]),
        W("p1", "1 × %d = %d" % (n, n))))
    half = n // 2
    choices, at = shuffled(qid, "partner", str(half), [str(n - 2), str(half + 2)])
    beats.append(B(
        "Next we try 2. %d is even, so 2 is a factor. What is its partner?" % n,
        ask=CHOOSE(choices, at,
                   "The partner is the number we multiply 2 by to make %d. Half of %d is %d, so the partner of 2 is %d." % (n, n, half, half))))
    beats.append(B("2 times %d is %d. That is our second pair." % (half, n), W("p2", "2 × %d = %d" % (half, n))))

    rest = ps[2:]
    last_small = ps[-1][0]
    skipped = [d for d in range(3, last_small) if n % d]
    skip_say = ""
    if skipped:
        skip_say = " %s %s not divide %d, so we skip %s." % (
            say_list(skipped), "does" if len(skipped) == 1 else "do", n, "it" if len(skipped) == 1 else "them")
    chunks = [rest] if len(rest) <= 3 else [rest[:len(rest) // 2], rest[len(rest) // 2:]]
    pid = 3
    for i, chunk in enumerate(chunks):
        ops = []
        for p in chunk:
            ops.append(W("p%d" % pid, "%s = %d" % (pair_text(p), n)))
            pid += 1
        if i == 0 and len(rest) == 1:
            say = "Keep going in order. The next number that works is %d: %d times %d is %d." % (chunk[0][0], chunk[0][0], chunk[0][1], n)
        elif i == 0:
            say = "Keep going in order: try 3, then 4, then 5, and so on. We get %s." % pair_say(chunk)
        else:
            say = "Carry on the same way: %s." % pair_say(chunk)
        if i == len(chunks) - 1:
            say += skip_say
        beats.append(B(say, *ops))

    last_id = "p%d" % (pid - 1)
    if square:
        r = ps[-1][0]
        beats.append(B(
            "Look at the last pair: %d times %d. Both partners are the same number, so the pairs have met in the middle. We can stop." % (r, r),
            CIRC(last_id, pair_text(ps[-1]))))
        choices, at = shuffled(qid, "count", str(count), [str(count + 1), str(len(ps))])
        beats.append(B(
            "Now count. We have %d pairs. But careful with %d times %d. How many different factors are there?" % (len(ps), r, r),
            ask=CHOOSE(choices, at,
                       "The first %d pairs give 2 factors each. The pair %d times %d gives only one factor, because it is the same number twice." % (len(ps) - 1, r, r))))
        sum_line = W("s", "%d × 2 + 1 = %d" % (len(ps) - 1, count))
        tell = "%d pairs give 2 factors each, and %d times %d adds just 1 more. So %d has %d factors." % (len(ps) - 1, r, r, n, count)
    else:
        nxt = ps[-1][1]
        beats.append(B(
            "When do we stop? The next factor after %d is %d, and %d is already on the board as a partner. So the pairs would only repeat." % (
                last_small, nxt, nxt),
            CIRC(last_id, str(nxt))))
        choices, at = shuffled(qid, "count", str(count), [str(len(ps)), str(count + 1)])
        beats.append(B(
            "Now count. We have %d pairs, and each pair gives 2 different factors. How many factors is that?" % len(ps),
            ask=CHOOSE(choices, at,
                       "Each pair holds 2 factors, and there are %d pairs. So we double %d." % (len(ps), len(ps)))))
        sum_line = W("s", "%d × 2 = %d" % (len(ps), count))
        tell = "%d pairs, 2 factors in each, makes %d. So %d has %d factors." % (len(ps), count, n, count)
    list_ops = []
    if count <= 12:
        list_ops = [LB("fl", list_line("", fs)[0])]
        tell += " Here they all are, in order."
    beats.append(B(tell, sum_line, *(list_ops + [ANS("ans", "%d has %d factors" % (n, count)),
                                                 CIRC("ans", "%d factors" % count)])))
    if square:
        beats.append(B(pick(qid, "sum", [
            "So to count factors: write the pairs in order, stop when they meet, and count. And a pair with the same number twice counts only once.",
            "Remember the plan: find the pairs in order, then count the numbers in them. Watch out for a pair like %d times %d: it is one factor, not two." % (ps[-1][0], ps[-1][0]),
        ])))
    else:
        beats.append(B(pick(qid, "sum", [
            "So to count factors: write the pairs in order, stop when they start to repeat, and count 2 for each pair. Your turn next!",
            "Remember the plan: go up in order, 1, 2, 3 and so on, and write each pair that works. Then count the numbers in the pairs.",
        ])))
    return LESSON(*beats, origin="rule")


# ── How many numbers from lo to hi are divisible by d? ───────────────────────

def count_multiples_lesson(qid, lo, hi, d, figure=None):
    i1 = -(-lo // d)
    i2 = hi // d
    first, last = i1 * d, i2 * d
    count = i2 - i1 + 1
    beats = []
    ops = [GIVEN("q", "From %d to %d: how many are divisible by %d?" % (lo, hi, d))]
    if figure:
        ops.append(FIG("f", figure))
    beats.append(B(
        pick(qid, "intro", [
            "How many numbers from %d to %d are divisible by %d? Divisible by %d means it is in the %d times table." % (lo, hi, d, d, d),
            "We are counting the numbers from %d to %d that %d divides exactly. Those are the numbers in the %d times table." % (lo, hi, d, d),
        ]), *ops))
    beats.append(B("Writing them all out would take ages. So we find the first one and the last one, and count smartly."))
    plan = ""
    if i1 == 1:
        beats.append(B(plan + "The first is easy: %d itself, which is %d times 1." % (d, d), W("a", "%d × 1 = %d" % (d, d))))
    elif first == lo:
        beats.append(B(plan + "The first is %d itself: %d times %d is %d." % (lo, d, i1, lo), W("a", "%d × %d = %d" % (d, i1, first))))
    else:
        beats.append(B(
            plan + "%d times %d is %d, which is just too small. %d times %d is %d. So %d is the first." % (d, i1 - 1, first - d, d, i1, first, first),
            W("a0", "%d × %d = %d" % (d, i1 - 1, first - d)), W("a", "%d × %d = %d" % (d, i1, first)),
            CIRC("a", str(first))))
    if last == hi:
        beats.append(B("Now the last one. %d itself works: %d times %d is %d." % (hi, d, i2, hi),
                       W("b", "%d × %d = %d" % (d, i2, last)), CIRC("b", str(last))))
    else:
        beats.append(B(
            "Now the last one. Divide %d by %d: it goes %d times, with a bit left over. %d times %d is %d, and one more step gives %d, which is past %d. So %d is the last." % (
                hi, d, i2, d, i2, last, last + d, hi, last),
            W("b", "%d × %d = %d" % (d, i2, last)), W("b1", "%d × %d = %d" % (d, i2 + 1, last + d)),
            CIRC("b", str(last))))
    if i1 == 1:
        choices, at = shuffled(qid, "count", str(count), [str(count + 1), str(count - 1)])
        beats.append(B(
            "So our numbers are %d times 1, %d times 2, and so on, up to %d times %d. How many numbers is that?" % (d, d, d, i2),
            ask=CHOOSE(choices, at,
                       "We are counting 1, 2, 3 and so on, up to %d. Counting from 1 up to %d gives exactly %d numbers." % (i2, i2, i2))))
        beats.append(B(
            "Counting from 1 up to %d gives %d numbers. So %d numbers from %d to %d are divisible by %d." % (i2, count, count, lo, hi, d),
            ANS("ans", "%d numbers" % count), CIRC("ans", "%d numbers" % count)))
        beats.append(B(
            "Careful with the end. %d is not in the %d times table, so the count stops at %d." % (hi, d, last)
            if last != hi else "And %d itself is counted, because it is in the %d times table." % (hi, d)))
        beats.append(B("So here is the plan: find the last multiple, and see which number in the table it is. That number is the count."))
        return LESSON(*beats, origin="rule")

    gap = i2 - i1
    choices, at = shuffled(qid, "count", str(count), [str(gap), str(i2)])
    beats.append(B(
        "So we want the %s number in the table, up to the %s. How many numbers is that, counting both ends?" % (ordinal(i1), ordinal(i2)),
        ask=CHOOSE(choices, at,
                   "Taking away gives %d, but that is only the number of jumps from the first to the last. We count the first one too, so we add 1." % gap)))
    beats.append(B(
        "%d minus %d is %d jumps. Add 1 for the number we started on. That makes %d." % (i2, i1, gap, count),
        W("c", "%d − %d + 1 = %d" % (i2, i1, count)), CIRC("c", "+ 1")))
    beats.append(B(
        pick(qid, "tiny", [
            "Why add 1? Try a tiny case. From the 2nd to the 4th there are three: the 2nd, the 3rd and the 4th. And 4 minus 2, plus 1, is 3.",
            "The plus 1 is the trap here. Think of counting from 2 to 4: that is 2, 3, 4, which is three numbers. And 4 minus 2, plus 1, is 3.",
        ]),
        W("t", "4 − 2 + 1 = 3")))
    beats.append(B(
        "So %d numbers from %d to %d are divisible by %d." % (count, lo, hi, d),
        ANS("ans", "%d numbers" % count), CIRC("ans", "%d numbers" % count)))
    beats.append(B(pick(qid, "sum", [
        "So here is the plan: find the first and last multiples, see which numbers in the table they are, subtract, and add 1.",
        "Remember: first multiple, last multiple, subtract their places in the table, then add 1 because both ends count.",
    ])))
    return LESSON(*beats, origin="rule")
