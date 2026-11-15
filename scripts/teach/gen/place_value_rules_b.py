"""Place-value lessons by rule, part B: the generated counting wordings.

  4. How many numbers from A to B are divisible by K?
  5. A book has N pages. How many digits are used to number all the pages?
  6. How many K-digit (even / odd) numbers are there (in all)?
  7. How many odd / even numbers are there from A to B?
  8. Find the sum of first N natural / even / odd numbers.
"""
import re

from place_value_lib import (PLACE_NAMES, a, al, arc, b, ch, fig, gl, key_text, nline, nt, nth_of, pick,
                             ring, tbl, w, wl, x)


# ── 4. Multiples in a range ──────────────────────────────────────────────────

DIV = re.compile(r"^How many numbers from (\d+) to (\d+) are divisible by (\d+)\?$")


def multiples_in_range(q):
    m = DIV.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    lo, hi, k = int(m.group(1)), int(m.group(2)), int(m.group(3))
    lm = hi // k
    last = lm * k
    bm = (lo - 1) // k
    below = bm * k
    first = below + k
    count = lm - bm
    assert key_text(q) == str(count) and 3 <= k <= 9, qid
    exact = last == hi

    beats = []
    beats.append(b(pick(qid, "open", [
        "We are counting the numbers from %d to %d that %d divides exactly, with nothing left over." % (lo, hi, k),
        "From %d to %d, some numbers can be divided by %d exactly. Our job is to count them." % (lo, hi, k),
    ]), gl("q", "From %d to %d: how many are divisible by %d?" % (lo, hi, k))))
    beats.append(b("Divisible by %d means the number is in the %d times table. So really, we are counting multiples of %d." % (k, k, k),
                   wl("idea", "divisible by %d = a multiple of %d" % (k, k))))

    if exact:
        choices = [str(last), str(last - k), str(last + k)]
        if_not = "%d itself is in the %d times table, and it is inside our range. So %d is the last one." % (hi, k, hi)
    else:
        choices = [str(last), str(last + k), str(last - k)]
        if_not = "%d is past %d, and %d is not the last one we can reach. The last multiple of %d inside the range is %d." % (
            last + k, hi, last - k, k, last)
    beats.append(b(pick(qid, "ask1", [
        "Let's find the far end first. Which is the last multiple of %d that does not go past %d?" % (k, hi),
        "Start at the top end. What is the biggest multiple of %d that is not more than %d?" % (k, hi),
    ]), ask=ch(choices, if_not)))

    if exact:
        beats.append(b("%d times %d is exactly %d. It lands right on the end of our range, so it counts." % (k, lm, last),
                       w("top", "%d × %d = %d" % (k, lm, last))))
    else:
        beats.append(b("%d times %d is %d. One more step gives %d, and that is past %d." % (k, lm, last, last + k, hi),
                       w("top", "%d × %d = %d" % (k, lm, last)),
                       w("over", "%d × %d = %d" % (k, lm + 1, last + k)),
                       x("over", str(last + k), "past %d" % hi, nth_of("%d × %d = %d" % (k, lm + 1, last + k), str(last + k),
                                                                     len("%d × %d = " % (k, lm + 1))))))

    rows = [["1", str(k)], ["2", str(2 * k)], ["3", str(3 * k)], ["…", "…"], [str(lm), str(last)]]
    beats.append(b("Look at the %d times table from its very start. %d is multiple number %d. So up to %d there are %d multiples of %d."
                   % (k, last, lm, hi, lm, k),
                   fig("table", tbl(["%d ×" % k, "multiple"], rows, hi=[4]))))

    if bm == 0:
        beats.append(b("Do we lose any at the start? No. Our range begins at %d, and the first multiple, %d, is already inside. All %d count."
                       % (lo, k, lm),
                       w("first", "%d × 1 = %d" % (k, k))))
    else:
        lo_line = "%d × %d = %d" % (k, bm, below)
        in_line = "%d × %d = %d" % (k, bm + 1, first)
        if first == lo:
            say = "Careful here: %d itself is in the %d times table, so it counts. The ones that are too small stop at %d, which is %d times %d." % (
                lo, k, below, k, bm)
        else:
            say = "But our range only starts at %d. %d times %d is %d, still too small. The next one, %d, is the first one inside." % (
                lo, k, bm, below, first)
        beats.append(b(say, w("low", lo_line), nt("low", str(below), "too small", "above", nth_of(lo_line, str(below), len(lo_line) - len(str(below)))),
                       w("in", in_line), nt("in", str(first), "first one in", "above", nth_of(in_line, str(first), len(in_line) - len(str(first))))))
        wrong = [c for c in [bm + 1, lm - bm, bm - 1] if c != bm]
        seen = []
        for c in wrong:
            if c not in seen and c > 0:
                seen.append(c)
        beats.append(b("So out of the %d multiples, how many are too small and have to go?" % lm,
                       ask=ch([str(bm)] + [str(c) for c in seen[:2]],
                              "The too small ones run up to %d, and %d is %d times %d. So exactly %d of them go." % (below, below, k, bm, bm))))
        beats.append(b(pick(qid, "sub", [
            "%d take away %d leaves %d." % (lm, bm, count),
            "So we take %d away from %d, and %d are left." % (bm, lm, count),
        ]), w("cnt", "%d − %d = %d" % (lm, bm, count))))

    listed = ", ".join(str(v) for v in range(first, last + 1, k))
    if count <= 9 and len(listed) <= 60:
        beats.append(b("Check by listing them: %s. Count them, and there are %d." % (listed, count), wl("list", listed)))
    else:
        span = last - first
        jumps = span // k
        beats.append(b("Check another way. From %d to %d is %d. That is %d jumps of %d, and %d jumps join %d numbers."
                       % (first, last, span, jumps, k, jumps, count),
                       w("j1", "%d − %d = %d" % (last, first, span)),
                       w("j2", "%d ÷ %d = %d" % (span, k, jumps)),
                       w("j3", "%d + 1 = %d" % (jumps, count))))

    beats.append(b("So %d numbers from %d to %d are divisible by %d." % (count, lo, hi, k),
                   al("ans", "%d numbers" % count), ring("ans", str(count))))
    if bm == 0:
        say = "When the range starts at 1, just find the last multiple and see which number it is in the times table."
    else:
        say = pick(qid, "sum", [
            "The plan: find the last multiple, count from the start of the table, then take away the ones that are too small.",
            "So, count the multiples up to the top end, then remove the ones below the bottom end. No long lists needed.",
        ])
    beats.append(b(say))
    return beats


# ── 5. Digits used to number the pages of a book ─────────────────────────────

BOOK = re.compile(r"^A book has (\d+) pages\. How many digits are used to number all the pages\?$")


def book_pages(q):
    m = BOOK.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    n = int(m.group(1))
    assert 10 <= n <= 999, qid
    big = n >= 100
    n2 = 90 if big else n - 9
    d2 = n2 * 2
    n3 = n - 99 if big else 0
    d3 = n3 * 3
    total = 9 + d2 + d3
    assert key_text(q) == str(total), qid

    beats = []
    beats.append(b("A book with %d pages. Every page has its number printed on it, and we are counting all the digits in those numbers." % n,
                   gl("q", "A book has %d pages. How many digits?" % n)))
    beats.append(b("Careful: this is not the same as counting pages. Page 5 uses 1 digit, but page %d uses %d." % (n, len(str(n))),
                   wl("eg", "page 5: 1 digit      page %d: %d digits" % (n, len(str(n))))))
    beats.append(b("So we sort the pages by how many digits they use. Which pages use just 1 digit?",
                   ask=ch(["pages 1 to 9", "pages 1 to 10", "pages 0 to 9"],
                          "Page 10 already needs 2 digits, a 1 and a 0. And there is no page 0. So the 1 digit pages are 1 to 9.")))
    beats.append(b("That is 9 pages with 1 digit each. 9 digits so far.", w("d1", "9 × 1 = 9")))

    if big:
        beats.append(b("Next come the 2 digit pages, from 10 up to 99. How many pages is that?",
                       ask=ch(["90", "89", "99"],
                              "From 1 to 99 there are 99 pages. Take away the 9 we have already counted, and 90 are left.")))
        beats.append(b("99 minus 9 is 90 pages. Each has 2 digits, so 90 times 2 is 180 digits.",
                       w("p2", "99 − 9 = 90"), w("d2", "90 × 2 = 180")))
        if n == 100:
            beats.append(b("Last comes page 100, the only page with 3 digits. Take away the first 99 pages and just 1 is left.",
                           wl("h3", "page 100"), w("p3", "100 − 99 = 1")))
            beats.append(b("1 page with 3 digits is 3 more digits.", w("d3", "1 × 3 = 3")))
        else:
            beats.append(b("Last come the 3 digit pages, 100 up to %d. Take away the first 99 pages: %d minus 99 leaves %d pages." % (n, n, n3),
                           wl("h3", "pages 100 to %d" % n), w("p3", "%d − 99 = %d" % (n, n3))))
            beats.append(b("%d pages with 3 digits each: %d times 3 is %d digits." % (n3, n3, d3), w("d3", "%d × 3 = %d" % (n3, d3))))
        rows = [["1 to 9", "9", "9"], ["10 to 99", "90", "180"], ["100 to %d" % n if n > 100 else "100", str(n3), str(d3)]]
        beats.append(b("Now add up all the digits: 9 plus 180 plus %d makes %d." % (d3, total),
                       fig("table", tbl(["pages", "how many", "digits"], rows)),
                       w("tot", "9 + 180 + %d = %d" % (d3, total))))
    else:
        beats.append(b("Next come the 2 digit pages, from 10 up to %d. How many pages is that?" % n,
                       ask=ch([str(n2), str(n2 - 1), str(n)],
                              "Take away the 9 pages we have already counted. %d minus 9 leaves %d." % (n, n2))))
        beats.append(b("%d minus 9 is %d pages. Each has 2 digits, so %d times 2 is %d digits." % (n, n2, n2, d2),
                       w("p2", "%d − 9 = %d" % (n, n2)), w("d2", "%d × 2 = %d" % (n2, d2))))
        rows = [["1 to 9", "9", "9"], ["10 to %d" % n, str(n2), str(d2)]]
        beats.append(b("Now add up the digits: 9 plus %d makes %d." % (d2, total),
                       fig("table", tbl(["pages", "how many", "digits"], rows)),
                       w("tot", "9 + %d = %d" % (d2, total))))

    beats.append(b("So numbering all %d pages takes %d digits." % (n, total), al("ans", "%d digits" % total), ring("ans", str(total))))
    beats.append(b(pick(qid, "sum", [
        "The plan: sort the pages by how many digits they have, count each group, then add.",
        "Group the pages by the length of their numbers, work out each group, and add them up. That works for any book.",
    ])))
    return beats


# ── 6. How many K-digit numbers ──────────────────────────────────────────────

KDIG = re.compile(r"^How many (\d)-digit (even |odd )?numbers are there( in all)?\?$")


def k_digit_numbers(q):
    m = KDIG.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    k = int(m.group(1))
    kind = (m.group(2) or "").strip()
    assert 2 <= k <= 4, qid
    lo, hi = 10 ** (k - 1), 10 ** k - 1
    total = hi - (lo - 1)
    ans = total // 2 if kind else total
    assert key_text(q) == str(ans), qid
    kind_sp = kind + " " if kind else ""

    beats = []
    beats.append(b("How many %d-digit %snumbers are there? Far too many to list, so we will count them cleverly." % (k, kind_sp),
                   gl("q", "How many %d-digit %snumbers?" % (k, kind_sp))))
    short = "1 digit" if k == 2 else "%d digits" % (k - 1)
    beats.append(b("First, the smallest %d-digit number. What is it?" % k,
                   ask=ch([str(lo), str(lo + 1), str(lo - 1)],
                          "%d has only %s. One more than that is %d, the very first number with %d digits." % (lo - 1, short, lo, k))))
    beats.append(b("And the largest is %d, because one more makes %d, and that needs %d digits." % (hi, hi + 1, k + 1),
                   wl("ends", "smallest %d      largest %d" % (lo, hi)), w("big", "%d + 1 = %d" % (hi, hi + 1))))
    beats.append(b("Now count. From 1 up to %d there are %d numbers. But 1 to %d are too short, so we take those %d away. %d are left."
                   % (hi, hi, lo - 1, lo - 1, total),
                   w("cnt", "%d − %d = %d" % (hi, lo - 1, total))))

    heads = list(reversed(PLACE_NAMES[:k]))
    if not kind:
        prod = " × ".join(["9"] + ["10"] * (k - 1))
        beats.append(b("Check it place by place. The first digit can be 1 to 9, never 0, so 9 choices. Every other place can be 0 to 9, so 10 choices. Multiply, and we get %d again." % total,
                       fig("table", tbl(heads, [["1 to 9"] + ["0 to 9"] * (k - 1), ["9 choices"] + ["10 choices"] * (k - 1)])),
                       w("chk", "%s = %d" % (prod, total))))
    else:
        other = "odd" if kind == "even" else "even"
        beats.append(b("Now, how many of these %d are %s? Think of them in order: even, odd, even, odd. They take turns." % (total, kind),
                       ask=ch(["exactly half", "all of them", "one more than half"],
                              "The list starts at %d, which is even, and ends at %d, which is odd. So they pair up neatly, one even and one odd in every pair. Half are %s."
                              % (lo, hi, kind))))
        beats.append(b("Pair them up: %d with %d, %d with %d, all the way to %d with %d. Each pair has one %s number. So %d divided by 2 is %d."
                       % (lo, lo + 1, lo + 2, lo + 3, hi - 1, hi, kind, total, ans),
                       wl("pairs", "(%d, %d) (%d, %d) … (%d, %d)" % (lo, lo + 1, lo + 2, lo + 3, hi - 1, hi)),
                       w("half", "%d ÷ 2 = %d" % (total, ans))))
        ends = "0, 2, 4, 6, 8" if kind == "even" else "1, 3, 5, 7, 9"
        prod = " × ".join(["9"] + ["10"] * (k - 2) + ["5"])
        if k == 2:
            say = "Check it place by place. 9 choices for the tens digit, because it cannot be 0. And only 5 for the units digit, which must be %s. 9 times 5 is %d." % (kind, ans)
        else:
            say = "Check it place by place. 9 choices for the first digit, 10 for each middle place, and only 5 for the last digit, which must be %s. That gives %d again." % (kind, ans)
        beats.append(b(say,
                       fig("table", tbl(heads, [["1 to 9"] + ["0 to 9"] * (k - 2) + [ends], ["9 choices"] + ["10 choices"] * (k - 2) + ["5 choices"]])),
                       w("chk", "%s = %d" % (prod, ans))))
        assert other

    beats.append(b("So the count of %d-digit %snumbers is %d." % (k, kind_sp, ans), al("ans", "%d numbers" % ans), ring("ans", str(ans))))
    if kind:
        say = "Count them all first, then halve, because even and odd numbers take turns."
    else:
        say = "Smallest, largest, then take away the ones that are too short. Or count the choices for each place and multiply."
    beats.append(b(say))
    return beats


# ── 7. Odd or even numbers in a range ────────────────────────────────────────

PARITY = re.compile(r"^How many (odd|even) numbers are there from (\d+) to (\d+)\?$")


def parity_in_range(q):
    m = PARITY.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    kind, lo, hi = m.group(1), int(m.group(2)), int(m.group(3))
    other = "odd" if kind == "even" else "even"
    want = 0 if kind == "even" else 1
    first = lo if lo % 2 == want else lo + 1
    last = hi if hi % 2 == want else hi - 1
    span = last - first
    jumps = span // 2
    count = jumps + 1
    assert key_text(q) == str(count), qid
    assert (hi - lo) % 10 == 0, qid
    runs = (hi - lo) // 10
    extra = 1 if hi % 2 == want else 0
    assert runs * 5 + extra == count and 2 <= runs <= 10, qid

    beats = []
    beats.append(b(pick(qid, "open", [
        "We want to know how many %s numbers there are from %d to %d. Both ends count, if they are %s." % (kind, lo, hi, kind),
        "From %d to %d, how many of the numbers are %s? Let's count them without writing every one." % (lo, hi, kind),
    ]), gl("q", "%s numbers from %d to %d: how many?" % (kind.capitalize(), lo, hi))))

    if first == lo:
        choices = [str(lo), str(lo + 1), str(lo + 2)]
        if_not = "%d itself is %s, and it is inside the range, so it counts. Our list starts right at %d." % (lo, kind, lo)
    else:
        choices = [str(lo + 1), str(lo), str(lo + 2)]
        if_not = "%d is %s, so it does not count. The very next number, %d, is the first %s one." % (lo, other, lo + 1, kind)
    beats.append(b("Where does our list start? Which is the first %s number in the range?" % kind, ask=ch(choices, if_not)))

    if last == hi:
        say = "So we start at %d. And the last one is %d itself, because %d is %s." % (first, hi, hi, kind)
    else:
        say = "So we start at %d. And the last one is %d, because %d is %s." % (first, last, hi, other)
    beats.append(b(say, wl("ends", "first %d       last %d" % (first, last))))

    step = 2 if jumps <= 40 else 4
    beats.append(b("%s numbers go up in jumps of 2: %d, %d, %d and so on, all the way to %d." % (kind.capitalize(), first, first + 2, first + 4, last),
                   fig("line", nline(first, last, step, points=[(first, "first"), (last, "last")],
                                     hops=[(first, first + 2, "+2"), (first + 2, first + 4, "+2")], labels="ends"))))
    beats.append(b("From %d to %d is %d. Each jump is 2, so that is %d jumps." % (first, last, span, jumps),
                   w("span", "%d − %d = %d" % (last, first, span)), w("j", "%d ÷ 2 = %d" % (span, jumps))))
    beats.append(b("%d jumps. So how many numbers are on our list?" % jumps,
                   ask=ch([str(count), str(jumps), str(span)],
                          "Think of fence posts. 1 jump joins 2 numbers, and 2 jumps join 3. There is always one more number than jumps.")))
    beats.append(b(pick(qid, "plus", [
        "%d jumps join %d numbers. The extra 1 is the number we started on." % (jumps, count),
        "One more than the jumps: %d plus 1 is %d. That extra 1 is our starting number." % (jumps, count),
    ]), w("cnt", "%d + 1 = %d" % (jumps, count))))

    if extra:
        say = "Check another way. Any 10 numbers in a row hold 5 %s ones. From %d up to %d there are %d runs of 10, plus %d itself, which is %s. That gives %d again." % (
            kind, lo, hi, runs, hi, kind, count)
        line = "%d × 5 + 1 = %d" % (runs, count)
    else:
        say = "Check another way. Any 10 numbers in a row hold 5 %s ones. From %d up to %d there are %d runs of 10. The %d left at the end is %s, so it adds nothing. %d again." % (
            kind, lo, hi, runs, hi, other, count)
        line = "%d × 5 = %d" % (runs, count)
    beats.append(b(say, w("chk", line)))

    beats.append(b("So there are %d %s numbers from %d to %d." % (count, kind, lo, hi),
                   al("ans", "%d %s numbers" % (count, kind)), ring("ans", str(count))))
    beats.append(b(pick(qid, "sum", [
        "First one, last one, count the jumps of 2, and add 1. The add 1 is the step people forget.",
        "Find the two ends, count the jumps between them, then add 1 for the starting number. That works every time.",
    ])))
    return beats


# ── 8. The sum of the first N numbers of a kind ──────────────────────────────

SUM = re.compile(r"^Find the sum of first (\d+) (even|odd|natural) numbers\.$")


def sum_of_first(q):
    m = SUM.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    n, kind = int(m.group(1)), m.group(2)
    if kind == "odd":
        return _sum_odd(q, qid, n)
    s = 1 if kind == "natural" else 2
    first, last = s, s * n
    ps = first + last
    pairs = n // 2
    odd_n = n % 2 == 1
    middle = ps // 2
    total = pairs * ps + (middle if odd_n else 0)
    assert total == sum(range(first, last + 1, s)) and key_text(q) == str(total) and n >= 6, qid
    a2, l2 = first + s, last - s

    head = "%d + %d + %d + … + " % (s, 2 * s, 3 * s)
    line = head + "%d + %d" % (l2, last)
    pos_last = len(line) - len(str(last))
    pos_l2 = len(head)
    pos_a2 = len("%d + " % s)

    beats = []
    beats.append(b(pick(qid, "open", [
        "We need to add up the first %d %s numbers. That is a long sum, so let's find a clever way." % (n, kind),
        "The first %d %s numbers, all added together. Adding them one by one is slow, so here is a smarter way." % (n, kind),
        "Add up the first %d %s numbers. There is a lovely shortcut for sums like this." % (n, kind),
    ]), gl("q", "Sum of the first %d %s numbers = ?" % (n, kind))))
    if kind == "natural":
        beats.append(b("Natural numbers are the counting numbers: 1, 2, 3 and so on. The first %d of them end at %d." % (n, n), wl("list", line)))
    else:
        beats.append(b("Even numbers go 2, 4, 6 and so on. Each one is 2 times its position in the list, so the last one is 2 times %d, which is %d." % (n, last),
                       w("last", "2 × %d = %d" % (n, last)), wl("list", line)))
    beats.append(b(pick(qid, "trick", [
        "Here is the trick. Add the first and the last: %d plus %d makes %d." % (first, last, ps),
        "Do not start adding from the left. Join the two ends instead: %d plus %d makes %d." % (first, last, ps),
    ]),
                   arc("list", (str(first), nth_of(line, str(first), 0)), [(str(last), nth_of(line, str(last), pos_last))]),
                   w("p1", "%d + %d = %d" % (first, last, ps))))
    beats.append(b("Now the second and the second last: %d and %d. What do they make?" % (a2, l2),
                   ask=ch([str(ps), str(ps - s), str(ps + s)],
                          "%d plus %d is %d again. One number went up by %d and the other came down by %d, so the total did not change." % (a2, l2, ps, s, s))))
    beats.append(b(pick(qid, "again", [
        "Yes, %d again. Every pair, working inwards from the two ends, makes %d." % (ps, ps),
        "%d once more. Keep stepping inwards from both ends, and every pair makes %d." % (ps, ps),
    ]),
                   arc("list", (str(a2), nth_of(line, str(a2), pos_a2)), [(str(l2), nth_of(line, str(l2), pos_l2))]),
                   w("p2", "%d + %d = %d" % (a2, l2, ps))))
    if odd_n:
        beats.append(b("%d is an odd count, so one number is left alone in the middle. It is half of %d, which is %d. The rest make %d pairs." % (n, ps, middle, pairs),
                       w("mid", "%d ÷ 2 = %d" % (ps, middle)), w("np", "(%d − 1) ÷ 2 = %d" % (n, pairs))))
        beats.append(b("%d pairs of %d, plus the middle %d, makes %d." % (pairs, ps, middle, total),
                       w("tot", "%d × %d + %d = %d" % (pairs, ps, middle, total))))
    else:
        beats.append(b("%d numbers make %d pairs, because each pair uses up 2 numbers." % (n, pairs), w("np", "%d ÷ 2 = %d" % (n, pairs))))
        beats.append(b("%d pairs of %d: %d times %d is %d." % (pairs, ps, pairs, ps, total), w("tot", "%d × %d = %d" % (pairs, ps, total))))
    if n <= 8 and kind == "natural":
        full = " + ".join(str(v) for v in range(1, n + 1))
        beats.append(b("This one is short enough to check by adding straight through. It really is %d." % total, w("chk", "%s = %d" % (full, total))))
    else:
        beats.append(b("Check another way. Write the list twice, once forwards and once backwards. That makes %d columns of %d, and half of that is %d." % (n, ps, total),
                       w("chk", "%d × %d ÷ 2 = %d" % (n, ps, total))))
    beats.append(b("So the sum of the first %d %s numbers is %d." % (n, kind, total), a("ans", str(total)), ring("ans", str(total))))
    beats.append(b(pick(qid, "sum", [
        "Pair the ends, count the pairs, multiply. That trick turns a long sum into a short one.",
        "Whenever numbers go up in equal steps, pair the first with the last. Every pair gives the same total.",
    ])))
    return beats


def _sum_odd(q, qid, n):
    total = n * n
    assert key_text(q) == str(total) and n >= 6, qid
    last = 2 * n - 1
    ps = 1 + last
    grid = {"kind": "grid", "rows": 4, "cols": 4, "shaded": [[3, 0], [3, 1], [3, 2], [3, 3], [0, 3], [1, 3], [2, 3]]}

    beats = []
    beats.append(b(pick(qid, "open", [
        "Add up the first %d odd numbers: 1, 3, 5 and so on. Let's start small and hunt for a pattern." % n,
        "The first %d odd numbers, all added together. Before the big sum, let's try some tiny ones and watch what happens." % n,
    ]), gl("q", "Sum of the first %d odd numbers = ?" % n)))
    beats.append(b("The first odd number on its own is 1. The first 2 odd numbers, 1 plus 3, make 4. And 4 is 2 times 2.",
                   w("o1", "1 = 1 × 1"), w("o2", "1 + 3 = 2 × 2")))
    beats.append(b("The first 3 odd numbers: 1 plus 3 plus 5 makes 9. That is 3 times 3. Interesting!", w("o3", "1 + 3 + 5 = 3 × 3")))
    beats.append(b("So what do you think the first 4 odd numbers, 1, 3, 5 and 7, add up to?",
                   ask=ch(["4 × 4", "4 × 3", "7 × 7"], "Add them up: 1, 3, 5 and 7. Then compare with 4 times 4. They match.")))
    beats.append(b("Yes, 4 times 4. Look at the picture: each new odd number wraps round the square like a letter L, and makes the next bigger square.",
                   w("o4", "1 + 3 + 5 + 7 = 4 × 4"), fig("square", grid)))
    beats.append(b("So the first %d odd numbers must add up to %d times %d." % (n, n, n),
                   wl("rule", "Sum of first %d odd numbers = %d × %d" % (n, n, n))))
    tens, units = (n // 10) * 10, n % 10
    if n <= 12:
        beats.append(b("And %d times %d is %d." % (n, n, total), w("sq", "%d × %d = %d" % (n, n, total))))
    elif units == 0:
        beats.append(b("%d times %d is %d." % (n, n, total), w("sq", "%d × %d = %d" % (n, n, total))))
    else:
        beats.append(b("Split it to make it easy. %d times %d is %d. %d times %d is %d. Together that is %d." % (n, tens, n * tens, n, units, n * units, total),
                       w("s1", "%d × %d = %d" % (n, tens, n * tens)), w("s2", "%d × %d = %d" % (n, units, n * units)),
                       w("sq", "%d + %d = %d" % (n * tens, n * units, total))))
    beats.append(b("Check with pairs. The last odd number is %d. First plus last, 1 plus %d, is %d. Forwards and backwards gives %d columns of %d, and half of that is %d."
                   % (last, last, ps, n, ps, total),
                   w("last", "2 × %d − 1 = %d" % (n, last)), w("pair", "1 + %d = %d" % (last, ps)),
                   w("chk", "%d × %d ÷ 2 = %d" % (n, ps, total))))
    beats.append(b("So the sum of the first %d odd numbers is %d." % (n, total), a("ans", str(total)), ring("ans", str(total))))
    beats.append(b(pick(qid, "sum", [
        "The first so many odd numbers always add up to that number times itself. A pattern worth remembering!",
        "So, count how many odd numbers there are, and multiply that count by itself. Isn't that neat?",
    ])))
    return beats


RULES = [multiples_in_range, book_pages, k_digit_numbers, parity_in_range, sum_of_first]
