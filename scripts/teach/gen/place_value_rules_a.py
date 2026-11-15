"""Place-value lessons by rule, part A: the three generated 'place value' wordings.

  1. In the number N, what is the place value of the digit D in the P place?
  2. In the number N, the place value of A (in P place) is how many times the place value of B (in Q place)?
  3. Which of the following K-digit numbers has a digit sum of S?
"""
import re
from fractions import Fraction

from place_value_lib import (PLACE_NAMES, a, al, b, ch, fig, g, gl, key_text, nt, nth_digit, nth_of,
                             option_texts, pchart, pick, place_index, ring, ul, w, x)


def expanded(n):
    """['20000', '6000', '50', '1'] for '26051' (zero digits give no part)."""
    out = []
    for i, c in enumerate(n):
        if c != "0":
            out.append(c + "0" * (len(n) - 1 - i))
    return out


def plus_words(parts):
    return " plus ".join(parts)


# ── 1. The place value of one digit ──────────────────────────────────────────

ONE = re.compile(r"^In the number (\d+), what is the place value of the digit (\d) in the ([\w-]+) place\?$")


def one_digit(q):
    m = ONE.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    n, d, pname = m.group(1), int(m.group(2)), m.group(3)
    p = place_index(pname)
    i = len(n) - 1 - p
    assert n[i] == str(d), qid
    mult = 10 ** p
    val = d * mult
    assert key_text(q) == str(val), qid
    nth = nth_digit(n, i)
    twice = n.count(str(d)) > 1

    beats = []
    beats.append(b(pick(qid, "open", [
        "Here is our number, %s. The question points at the %d in the %s place, and asks what that digit is really worth." % (n, d, pname),
        "Let's write the number down: %s. We want the place value of the %d sitting in the %s place." % (n, d, pname),
        "This is %s. One of its digits, the %d in the %s place, has a value for us to find." % (n, d, pname),
    ]), g("n", n)))

    if p == 0:
        where = "The units place is the very last column, on the right."
    else:
        where = "Every digit lives in its own column. Counting from the right: %s." % ", ".join(PLACE_NAMES[:p + 1])
    if twice and p == 0:
        where += " Careful, this number has more than one %d. We want the one in the units column." % d
    elif twice:
        where = "Count the columns from the right: %s. Careful, this number has more than one %d. We want the one in the %s column." % (
            ", ".join(PLACE_NAMES[:p + 1]), d, pname)
    else:
        where += pick(qid, "there", [" There is our %d." % d, " And there sits our %d." % d, " So that is where our %d lives." % d])
    beats.append(b(where, fig("chart", pchart(n, hi=[i])), ul("n", str(d), nth), nt("n", str(d), pname, "below", nth)))

    if p == 0:
        choices = ["1", "10", "0"]
        if_not = "The units column counts single ones. So each one in that column is worth just 1."
        ask_say = "The units column is the smallest of them all. What is each one in that column worth?"
    else:
        choices = [str(mult), str(mult // 10), str(mult * 10)]
        if_not = "Look at the chart again. The column is called %s, so each one in it stands for %d." % (pname, mult)
        ask_say = pick(qid, "ask", [
            "A digit in the %s column counts %s. So what is each one in that column worth?" % (pname, pname),
            "Now think about the column itself. What is a single 1 worth when it sits in the %s place?" % pname,
        ])
    beats.append(b(ask_say, ask=ch(choices, if_not)))

    if d == 0:
        say = "And how many of them do we have? Zero. 0 times %d is 0, so this digit is worth nothing at all." % mult
    elif p == 0:
        say = "We have %d ones. %d times 1 is just %d." % (d, d, d)
    elif d == 1:
        say = "We have just 1 of them. 1 times %d is %d." % (mult, val)
    else:
        say = pick(qid, "mul", [
            "We have %d of them. So %d times %d is %d." % (d, d, mult, val),
            "Our digit says there are %d of those. %d times %d makes %d." % (d, d, mult, val),
            "So the %d means %d lots of %d. That is %d." % (d, d, mult, val),
        ])
    beats.append(b(say, w("pv", "%d × %d = %d" % (d, mult, val))))

    if d == 0 and p == 0:
        say = "Zero is special. Wherever it sits, its place value is 0, because zero lots of anything is nothing."
    elif d == 0:
        say = "Zero is special. Wherever it sits, its place value is 0. The %d belongs to the column, not to the digit." % mult
    elif p == 0:
        say = "Here is something neat. In the units place, the place value and the face value are the same: %d." % d
    else:
        zeros = "The zero on the end is there because 1 more place sits" if p == 1 else "The %d zeros are there because %d more places sit" % (p, p)
        say = "Careful: %d on its own is only the face value, the digit as it looks. Its place value is %d. %s to its right." % (d, val, zeros)
    beats.append(b(say))

    parts = expanded(n)
    line = "%s = %s" % (n, " + ".join(parts))
    ops = [w("exp", line)]
    if d == 0:
        say = "Let's check by breaking the number into its parts: %s. No %s part at all, so the 0 really adds nothing." % (plus_words(parts), pname)
    else:
        at = len(n) + 3 + sum(len(t) + 3 for t in parts[:parts.index(str(val))])
        ops.append(ring("exp", str(val), nth_of(line, str(val), at)))
        say = "Let's check by breaking the number into its parts: %s. %s" % (plus_words(parts), pick(qid, "chk", [
            "There is our %d, right where it should be." % val,
            "And look, %d is one of the parts." % val,
        ]))
    beats.append(b(say, *ops))

    ans = "Place value of %d = %d" % (d, val)
    beats.append(b("So the place value of the %d in the %s place is %d." % (d, pname, val),
                   al("ans", ans), ring("ans", str(val), nth_of(ans, str(val), len(ans) - len(str(val))))))
    beats.append(b(pick(qid, "sum", [
        "The plan every time: find the digit's column, see what that column is worth, and multiply.",
        "Remember it like this: place value is the digit times the worth of its column. Your turn next!",
        "So, find the column, then multiply the digit by what the column is worth. That works for any number.",
    ])))
    return beats


# ── 2. How many times one place value is another ─────────────────────────────

TIMES = re.compile(r"^In the number (\d+), the place value of (\d) \(in ([\w-]+) place\) is how many times "
                   r"the place value of (\d) \(in ([\w-]+) place\)\?$")


def how_many_times(q):
    m = TIMES.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    n = m.group(1)
    da, pa_name, db, pb_name = int(m.group(2)), m.group(3), int(m.group(4)), m.group(5)
    pa, pb = place_index(pa_name), place_index(pb_name)
    ia, ib = len(n) - 1 - pa, len(n) - 1 - pb
    assert n[ia] == str(da) and n[ib] == str(db) and db != 0 and da != 0, qid
    ma, mb = 10 ** pa, 10 ** pb
    va, vb = da * ma, db * mb
    quo = Fraction(va, vb)
    if quo.denominator == 1:
        ans = str(quo.numerator)
    else:
        ans = ("%f" % float(quo)).rstrip("0")
        assert Fraction(ans) == quo, qid
    assert key_text(q) == ans, qid
    same = da == db

    beats = []
    if same:
        say = "Here is %s. We are comparing two %ds: one in the %s place, and one in the %s place." % (n, da, pa_name, pb_name)
    else:
        say = pick(qid, "open", [
            "Here is %s. We are comparing two digits: the %d in the %s place, and the %d in the %s place." % (n, da, pa_name, db, pb_name),
            "Let's write %s on the board. Two digits matter here: the %d in the %s place and the %d in the %s place." % (n, da, pa_name, db, pb_name),
        ])
    beats.append(b(say, g("n", n),
                   ul("n", str(da), nth_digit(n, ia)), nt("n", str(da), pa_name, "above", nth_digit(n, ia)),
                   ul("n", str(db), nth_digit(n, ib)), nt("n", str(db), pb_name, "below", nth_digit(n, ib))))

    cands = [c for c in ([1, da * 10, da * 100] if pa == 0 else [ma, da, va * 10]) if c != va]
    seen = []
    for c in cands:
        if c not in seen:
            seen.append(c)
    choices = [str(va)] + [str(c) for c in seen[:2]]
    if pa == 0 and da == 1:
        if_not = "It is in the units column, so it is worth just 1."
    elif pa == 0:
        if_not = "It is in the units column, so it stands for just %d ones. That is %d." % (da, da)
    elif da == 1:
        if_not = "It is 1 in the %s column, so it stands for one lot of %d." % (pa_name, ma)
    else:
        if_not = "It is %d in the %s column, so it stands for %d lots of %d. That makes %d." % (da, pa_name, da, ma, va)
    beats.append(b("Here they are in the chart. Start with the %d in the %s column. What is it worth?" % (da, pa_name),
                   fig("chart", pchart(n, hi=sorted([ia, ib]))), ask=ch(choices, if_not)))

    if pa == 0:
        say = "In the units place a digit is worth just itself. So this %d is worth %d." % (da, va)
    else:
        say = "%d times %d is %d. So that %d is worth %d." % (da, ma, va, da, va)
    beats.append(b(say, w("va", "%d × %d = %d" % (da, ma, va))))

    if pb == 0:
        say = "Now the %s in the units place. There it is worth just itself: %d." % ("other %d" % db if same else str(db), vb)
    else:
        say = "Now the %s in the %s place. %d times %d is %d." % ("other %d" % db if same else str(db), pb_name, db, mb, vb)
    beats.append(b(say, w("vb", "%d × %d = %d" % (db, mb, vb))))

    third = "%d × %d" % (va, vb) if same else "%d ÷ %d" % (da, db)
    choices = ["%d ÷ %d" % (va, vb), "%d − %d" % (va, vb), third]
    if quo < 1:
        if_not = "To compare by 'how many times', we divide the first value by the second, even when the first one is smaller."
    else:
        if_not = "'How many times' asks how many lots of %d fit into %d. Fitting in means dividing the place values, not taking away." % (vb, va)
    beats.append(b(pick(qid, "ask2", [
        "Now for the words 'how many times'. Which sum answers that?",
        "The question says 'how many times'. So which sum do we need?",
    ]), ask=ch(choices, if_not)))

    if quo.denominator == 1:
        if same and pb > 0:
            say = "%d divided by %d is %d. Both digits are %d, so it is just like %d divided by %d." % (va, vb, quo.numerator, da, ma, mb)
        elif same:
            say = "%d divided by %d is %d. Both digits are %d, so only their columns make the difference." % (va, vb, quo.numerator, da)
        else:
            say = pick(qid, "div", [
                "%d divided by %d is %s." % (va, vb, ans),
                "So we divide. %d divided by %d gives %s." % (va, vb, ans),
            ])
    elif quo < 1:
        assert quo == Fraction(1, 10), qid
        say = "%d divided by %d is one tenth, which we write as %s. It is less than 1, because the first digit is worth less than the second." % (va, vb, ans)
    else:
        assert quo.denominator == 2, qid
        whole = quo.numerator // 2
        say = "%d divided by %d does not come out whole. It is %d and a half, which we write as %s." % (va, vb, whole, ans)
    beats.append(b(say, w("div", "%d ÷ %d = %s" % (va, vb, ans))))

    beats.append(b(pick(qid, "chk", [
        "Check it by going backwards: %s times %d gives back %d. It works." % (ans, vb, va),
        "Good mathematicians check. %s times %d is %d, just as it should be." % (ans, vb, va),
    ]), w("chk", "%s × %d = %d" % (ans, vb, va))))

    beats.append(b("So the %d in the %s place is worth %s times the %d in the %s place." % (da, pa_name, ans, db, pb_name),
                   al("ans", "%s times" % ans), ring("ans", ans)))
    if same:
        say = "Find each place value first, then divide. And when the digits are the same, only their columns matter."
    else:
        say = pick(qid, "sum", [
            "The plan: find each place value first, then divide. Never just divide the digits as they look.",
            "So, two place values first, then one division. The digits alone would have fooled us.",
        ])
    beats.append(b(say))
    return beats


# ── 3. Which number has this digit sum ───────────────────────────────────────

DSUM = re.compile(r"^Which of the following (\d)-digit numbers has a digit sum of (\d+)\?$")


def digit_sum(q):
    m = DSUM.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    target = int(m.group(2))
    opts = option_texts(q)
    sums = [sum(int(c) for c in o) for o in opts]
    key = "ABCD".index(q["correctAnswer"])
    assert sums[key] == target and sums.count(target) == 1, qid
    line = "   ".join(opts)
    starts = []
    pos = 0
    for o in opts:
        starts.append(pos)
        pos += len(o) + 3

    beats = []
    beats.append(b(pick(qid, "open", [
        "We are hunting for the number whose digits add up to %d. Here are the four to choose from." % target,
        "One of these four numbers has a digit sum of %d. Let's find out which." % target,
    ]), gl("q", "Digit sum = %d. Which number?" % target), gl("opts", line)))
    beats.append(b("First, what does 'digit sum' ask us to do?",
                   ask=ch(["add up all the digits", "count how many digits", "multiply the digits"],
                          "Digit sum is just what it says. Take each digit of the number and add them all together.")))
    if any("0" in o for o in opts):
        say = "So we test the numbers one at a time. A tip: a zero adds nothing, so you can skip straight over any zeros."
    else:
        say = "So we test the numbers one at a time. Add slowly, one digit at a time, and nothing can go astray."
    beats.append(b(say))

    found = False
    misses = 0
    after_found = 0
    for k, o in enumerate(opts):
        digits = list(o)
        sum_line = "%s = %d" % (" + ".join(digits), sums[k])
        nth = nth_of(line, o, starts[k])
        if k == key:
            if k == 0:
                say = "Start with %s. Add its digits yourself before I do. What do you get?" % o
            else:
                say = pick(qid, "try", [
                    "Now %s. Add its digits yourself before I do. What do you get?" % o,
                    "Next is %s. Your turn: add up its digits. What do they make?" % o,
                ])
            beats.append(b(say, ask=ch([str(target), str(target + 1), str(target - 1)],
                       "Go one digit at a time: %s. Keep a running total as you go." % ", ".join(digits))))
            beats.append(b("%s makes %d. %s" % (plus_words(digits), target, pick(qid, "yes", [
                "That is the one!", "We have found it!", "There it is!"])),
                w("s%d" % k, sum_line), ring("opts", o, nth)))
            found = True
        else:
            verdict = "too big" if sums[k] > target else "too small"
            lead = pick(qid, "lead%d" % k, ["Try %s." % o, "Take %s." % o, "Look at %s." % o])
            if found:
                lead = ["Let's make sure of the others. First %s." % o, "Then %s." % o, "And last, %s." % o][min(after_found, 2)]
                after_found += 1
            if misses == 0:
                tail = "makes %d. That is %s, so we cross it out." % (sums[k], verdict)
            elif misses == 1:
                tail = "makes %d. Not %d either, so out it goes." % (sums[k], target)
            else:
                tail = "makes %d, which is %s. Cross it out." % (sums[k], verdict)
            misses += 1
            beats.append(b("%s %s %s" % (lead, plus_words(digits), tail),
                           w("s%d" % k, sum_line), x("opts", o, str(sums[k]), nth)))

    beats.append(b("So the number with a digit sum of %d is %s." % (target, opts[key]),
                   a("ans", opts[key]), ring("ans", opts[key])))
    beats.append(b(pick(qid, "sum", [
        "Digit sum means add the digits, nothing more. Test each choice calmly and cross out the ones that miss.",
        "That is the whole method: add the digits of each choice, and keep the one that hits the target.",
    ])))
    return beats


RULES = [one_digit, how_many_times, digit_sum]
