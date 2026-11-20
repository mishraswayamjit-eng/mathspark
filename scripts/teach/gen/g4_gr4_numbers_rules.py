"""Rules for the generated families in gr4_numbers: one lesson per wording, numbers read from the question."""
import re

from g4_gr4_numbers_lib import A, BX, C, FIG, G, Q, U, W, b, build, chart, opts, pick

PLACE = {"units": 0, "ones": 0, "tens": 1, "hundreds": 2, "thousands": 3, "ten-thousands": 4, "lakhs": 5}
SEATS = ["ones", "tens", "hundreds", "thousands", "ten-thousands", "lakhs"]

RE_PV = re.compile(r"In the number (\d+), what is the place value of the digit (\d) in the ([\w-]+) place\?$")
RE_TIMES = re.compile(r"In the number (\d+), the place value of (\d) \(in ([\w-]+) place\) is how many times "
                      r"the place value of (\d) \(in ([\w-]+) place\)\?$")
RE_DSUM = re.compile(r"Which of the following (\d)-digit numbers has a digit sum of (\d+)\?$")
RE_ODD = re.compile(r"How many odd numbers are there from (\d+) to (\d+)\?$")


def seats_upto(k, first):
    names = [first] + SEATS[1:]
    return names[:max(k + 1, 3)]


def join_words(words):
    return ", ".join(words[:-1]) + " and " + words[-1]


def zeros(n):
    return "1 zero" if n == 1 else "%d zeros" % n


def last(line, s):
    return (s, line.count(s))


# ── "What is the place value of the digit D in the P place?" ─────────────────

def place_value(q):
    m = RE_PV.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    N, D, P = m.group(1), m.group(2), m.group(3)
    k = PLACE[P]
    unit = 10 ** k
    V = int(D) * unit
    pos = len(N) - 1 - k
    assert N[pos] == D, qid
    first = "units" if P == "units" else "ones"
    seats = seats_upto(k, first)
    beats = []
    beats.append(b(
        pick(qid, "open", [
            "Here is our number, %s. We want the place value of the %s in the %s place." % (N, D, P),
            "Look at %s. Our job is to find what the %s in the %s place is really worth." % (N, D, P),
            "This is %s. Let us find out how much the %s in the %s place stands for." % (N, D, P),
        ]),
        G("Place value of %s in %s (%s place)" % (D, N, P)),
        FIG(chart(N, [pos], note="How much is the marked digit worth?"))))
    if N.count(D) > 1:
        beats.append(b("Careful: %s has more than one %s. We only want the one sitting in the %s place." % (N, D, P)))
    beats.append(b(
        "Every digit has a seat. Counting from the right, the seats are %s." % join_words(seats),
        W("From right: " + ", ".join(seats))))
    others = [10, 100] if k == 0 else [10 ** (k - 1), 10 ** (k + 1)]
    beats.append(b(
        pick(qid, "ask", [
            "Our %s is in the %s seat. What is the %s place worth?" % (D, P, P),
            "Our %s sits in the %s place. How much is that place worth?" % (D, P),
        ]),
        Q([str(unit)] + [str(x) for x in others],
          "Count the seats from the right once more: %s. The %s place is worth %d." % (join_words(seats), P, unit))))
    line = "%s × %d = %d" % (D, unit, V)
    beats.append(b(
        pick(qid, "mult", [
            "Place value is the digit times what its seat is worth. So we multiply %s by %d." % (D, unit),
            "To get the place value, we multiply the digit by the worth of its seat. That is %s times %d." % (D, unit),
        ]),
        W("Place value = digit × value of its place"),
        W(line), U((str(unit), 2 if (unit == 1 and D == "1") else 1))))
    if k == 0:
        say = "%s times 1 is just %s. So in the %s place, this %s is worth only %d." % (D, D, P, D, V)
    elif D == "1":
        say = "1 times %d is just %d. So this 1 is worth %d." % (unit, unit, V)
    else:
        say = "%s times %d is %d. So this %s is worth %d." % (D, unit, V, D, V)
    beats.append(b(say, A(str(V))))
    if k == 0:
        beats.append(b("Here is something neat. In the %s place, the place value and the face value are the same number." % P))
        beats.append(b("So remember: find the seat first, then multiply the digit by what the seat is worth. Your turn next!"))
    else:
        beats.append(b("Careful: %s by itself is only the face value. The place value also counts the seat, and that is why we get %d." % (D, V)))
        beats.append(b(
            "A quick check: %d is %s followed by %s, one for each seat to its right. " % (V, D, zeros(k))
            + pick(qid, "close", [
                "So remember: find the seat, then multiply the digit by what the seat is worth.",
                "So the plan is: find the seat, then multiply the digit by the worth of that seat.",
            ])))
    return build(qid, beats, origin="rule")


# ── "The place value of A is how many times the place value of B?" ───────────

def how_many_times(q):
    m = RE_TIMES.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    N, Ad, P1, Bd, P2 = m.groups()
    k1, k2 = PLACE[P1], PLACE[P2]
    u1, u2 = 10 ** k1, 10 ** k2
    VA, VB = int(Ad) * u1, int(Bd) * u2
    p1, p2 = len(N) - 1 - k1, len(N) - 1 - k2
    assert N[p1] == Ad and N[p2] == Bd, qid
    small = VA < VB
    if small:
        assert VB == 10 * VA, qid
        R = "0.1"
    else:
        assert VA % VB == 0, qid
        R = str(VA // VB)
    assert opts(q)["ABCD".index(q["correctAnswer"])] == R, qid

    given = "In %s: (%s in %s) is ? times (%s in %s)" % (N, Ad, P1, Bd, P2)
    if len(given) > 60:
        given = "%s: value of first %s is ? times value of second" % (N, Ad)
    beats = []
    beats.append(b(
        pick(qid, "open", [
            "Here is %s. Two digits are marked: the %s in the %s place and the %s in the %s place. We must compare what they are worth." % (N, Ad, P1, Bd, P2),
            "Look at %s. We want to compare two digits: the %s in the %s place and the %s in the %s place." % (N, Ad, P1, Bd, P2),
        ]),
        G(given), FIG(chart(N, sorted([p1, p2]), note="Compare the two marked digits"))))
    c1 = [str(VA), str(VA * 10)] + ([Ad] if k1 > 0 else [str(VA * 100)])
    beats.append(b(
        "Start with the %s in the %s place. What is it worth?" % (Ad, P1),
        Q(c1, "Count the seats from the right. This %s sits in the %s place, so it is worth %d." % (Ad, P1, VA))))
    l1 = "%s × %d = %d" % (Ad, u1, VA)
    if k1 == 0:
        say = "The %s place is worth just 1, so this %s is worth %d." % (P1, Ad, VA)
    else:
        say = "The %s place is worth %d, and %s times %d is %d." % (P1, u1, Ad, u1, VA)
    beats.append(b(say, W(l1, name="va"), BX(last(l1, str(VA)))))
    l2 = "%s × %d = %d" % (Bd, u2, VB)
    if k2 == 0:
        say = "Now the %s in the %s place. That seat is worth just 1, so this %s is worth %d." % (Bd, P2, Bd, VB)
    else:
        say = "Now the %s in the %s place. That seat is worth %d, so %s times %d is %d." % (Bd, P2, u2, Bd, u2, VB)
    beats.append(b(say, W(l2, name="vb"), BX(last(l2, str(VB)))))

    if small:
        beats.append(b(
            "How many times means we divide the first value by the second. Which sum is that?",
            Q(["%d ÷ %d" % (VA, VB), "%d ÷ %d" % (VB, VA), "%d − %d" % (VB, VA)],
              "The question starts with the %s in the %s place, so its value goes first: %d divided by %d." % (Ad, P1, VA, VB))))
        beats.append(b(
            "%d is smaller than %d, so the answer is less than 1. %d is 10 times %d, so %d is one tenth of %d. One tenth is written 0.1." % (VA, VB, VB, VA, VA, VB),
            W("%d ÷ %d = 0.1" % (VA, VB))))
        beats.append(b(
            "So the %s in the %s place is worth only 0.1 times the %s in the %s place. It is the smaller one!" % (Ad, P1, Bd, P2),
            A("0.1")))
        beats.append(b("Check: one tenth of %d is %d. It works." % (VB, VA), W("%d × 0.1 = %d" % (VB, VA))))
        beats.append(b("So the plan: find what each digit is worth, then divide the first by the second. And each seat is worth 10 times the seat on its right."))
        return build(qid, beats, origin="rule")

    beats.append(b(
        pick(qid, "ask2", [
            "How many times means: how many lots of %d fit into %d? Which sum finds that?" % (VB, VA),
            "Now, how many times. That asks how many lots of %d fit into %d. Which sum tells us?" % (VB, VA),
        ]),
        Q(["%d ÷ %d" % (VA, VB), "%d − %d" % (VA, VB), "%d + %d" % (VA, VB)],
          "Taking away tells us how much more. How many times asks how many lots of %d fit into %d, and that is a division." % (VB, VA))))
    z = min(k1, k2)
    a, bb = VA // 10 ** z, VB // 10 ** z
    checked = False
    if z > 0 and bb == 1:
        beats.append(b(
            "A neat trick: cross off the same number of zeros from both. Here that is %s from each, leaving %d divided by 1, and that is just %d." % (zeros(z), a, a),
            W("%d ÷ %d = %d ÷ 1" % (VA, VB, a))))
    elif z > 0:
        beats.append(b(
            "A neat trick: cross off the same number of zeros from both. Here that is %s from each, leaving %d divided by %d." % (zeros(z), a, bb),
            W("%d ÷ %d = %d ÷ %d" % (VA, VB, a, bb))))
        q_ = a // bb
        if a == bb * 10 or a < 100 and q_ <= 10:
            beats.append(b("%d divided by %d is %s." % (a, bb, R), W("%d ÷ %d = %s" % (a, bb, R))))
        elif bb == 2:
            beats.append(b("Dividing by 2 is halving. Half of %d is %s." % (a, R), W("%d ÷ %d = %s" % (a, bb, R))))
        elif bb == 4 and a % 4 == 0:
            beats.append(b(
                "Dividing by 4 is halving twice. Half of %d is %d, and half of %d is %s." % (a, a // 2, a // 2, R),
                W("%d ÷ 2 = %d" % (a, a // 2)), W("%d ÷ 2 = %s" % (a // 2, R)), W("%d ÷ %d = %s" % (a, bb, R))))
        elif bb == 5 and a % 10 == 0:
            beats.append(b(
                "Here is a way to divide by 5. Divide by 10 first, which gives %d. Then double it, because 5 is half of 10. That makes %s." % (a // 10, R),
                W("%d ÷ 10 = %d" % (a, a // 10)), W("%d × 2 = %s" % (a // 10, R)), W("%d ÷ %d = %s" % (a, bb, R))))
        else:
            beats.append(b(
                "%d times %s is %d. So %d divided by %d is %s." % (bb, R, a, a, bb, R),
                W("%d × %s = %d" % (bb, R, a)), W("%d ÷ %d = %s" % (a, bb, R))))
    elif VB == 1:
        beats.append(b("Dividing by 1 changes nothing. So %d divided by 1 is %d." % (VA, VA), W("%d ÷ 1 = %s" % (VA, R))))
    else:
        beats.append(b(
            "We need the number that, times %d, makes %d. That number is %s, because %s times %d is %d." % (VB, VA, R, R, VB, VA),
            W("%d ÷ %d = %s" % (VA, VB, R)), W("%s × %d = %d" % (R, VB, VA))))
        checked = True
    beats.append(b(
        "So the %s in the %s place is worth %s times the %s in the %s place." % (Ad, P1, R, Bd, P2),
        A(R)))
    if not checked:
        beats.append(b(
            pick(qid, "check", [
                "Check by multiplying back: %d times %s is %d. It works." % (VB, R, VA),
                "Good mathematicians check. %d times %s takes us back to %d." % (VB, R, VA),
            ]),
            W("%d × %s = %d" % (VB, R, VA))))
    close = "So the plan: find what each digit is worth, then divide the first by the second."
    if Ad == Bd and k1 - k2 == 1:
        close += " And notice: each seat is worth 10 times the seat on its right."
    beats.append(b(close))
    return build(qid, beats, origin="rule")


# ── "Which of the following k-digit numbers has a digit sum of T?" ───────────

def digit_sum(q):
    m = RE_DSUM.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    T = int(m.group(2))
    options = opts(q)
    key = "ABCD".index(q["correctAnswer"])
    sums = [sum(int(c) for c in o) for o in options]
    assert sums[key] == T and sums.count(T) == 1, qid

    def spoken(o):
        return " plus ".join(o)

    beats = []
    beats.append(b(
        pick(qid, "open", [
            "We are hunting for the number whose digits add up to %d. Digit sum simply means: add up the digits." % T,
            "One of these numbers has digits that add up to %d. Digit sum just means we add the digits together." % T,
        ]),
        G("Which number has a digit sum of %d?" % T)))
    o = options[0]
    near = sums[0] + 1 if sums[0] + 1 != T or key == 0 else sums[0] + 2
    beats.append(b(
        "Let us try the first one, %s. What do its digits add up to?" % o,
        W(o, lab=True),
        Q([str(sums[0]), str(near), str(sums[0] - 1)],
          "Add them one at a time: %s. That makes %d." % (spoken(o), sums[0]))))
    for i, o in enumerate(options):
        line = "%s = %d" % (" + ".join(o), sums[i])
        hit = sums[i] == T
        if i == 0:
            say = "%s makes %d. " % (spoken(o).capitalize(), sums[i])
        else:
            say = pick(qid, "o%d" % i, ["Next, %s. ", "Now %s. ", "Then %s. "]) % o + "%s makes %d. " % (spoken(o).capitalize(), sums[i])
        if hit:
            say += pick(qid, "hit", ["That is the %d we are looking for!" % T, "There it is, %d!" % T])
        elif sums[i] > T:
            say += "That is more than %d, so not this one." % T
        else:
            say += "That is less than %d, so not this one." % T
        things = ([] if i == 0 else [W(o, lab=True)]) + [W(line, name="s%d" % i)]
        if hit:
            things.append(BX(last(line, str(T))))
        beats.append(b(say, *things))
    ans = options[key]
    beats.append(b("So the number with a digit sum of %d is %s." % (T, ans), A(ans)))
    if any("0" in o for o in options):
        tip = "A tip for next time: a zero adds nothing, so you can skip over it. And check every choice, so nothing surprises you."
    else:
        tip = "A tip for next time: look for digits that make 10 together, and add those first. It makes the adding quick."
    beats.append(b(tip))
    return build(qid, beats, origin="rule")


# ── "How many odd numbers are there from a to b?" (a and b are tens) ─────────

def odd_count(q):
    m = RE_ODD.match(q["questionText"])
    if not m:
        return None
    qid = q["id"]
    a, c = int(m.group(1)), int(m.group(2))
    assert a % 10 == 0 and c % 10 == 0 and c > a, qid
    blocks = (c - a) // 10
    n = blocks * 5
    first, lastodd = a + 1, c - 1
    assert opts(q)["ABCD".index(q["correctAnswer"])] == str(n), qid
    beats = []
    beats.append(b(
        "We want to count the odd numbers from %d to %d. Counting them one by one would take a while, so let us be clever." % (a, c),
        G("Odd numbers from %d to %d: how many?" % (a, c))))
    beats.append(b(
        "Odd numbers end in 1, 3, 5, 7 or 9. %d and %d are both even, so the first odd number is %d and the last is %d." % (a, c, first, lastodd),
        W("first odd: %d      last odd: %d" % (first, lastodd))))
    beats.append(b(
        "Odd and even numbers take turns. So in any 10 numbers in a row, how many are odd?",
        Q(["5", "10", "4"], "Odd and even take turns, so exactly half of them are odd. Half of 10 is 5.")))
    row = ", ".join(str(first + 2 * i) for i in range(5))
    beats.append(b(
        "Look at the 10 numbers from %d to %d. The odd ones are %s. That is 5 of them." % (first, a + 10, row.replace(", %d" % (first + 8), " and %d" % (first + 8))),
        W("%d to %d:  %s" % (first, a + 10, row)), W("5 odd numbers in each ten")))
    tens = ["%d to %d" % (a + 10 * i + 1, a + 10 * i + 10) for i in range(blocks)]
    beats.append(b(
        "From %d to %d there are %d lots of ten like that. So we need %d lots of 5." % (first, c, blocks, blocks),
        W("%d tens: %s" % (blocks, ", ".join(tens)) if blocks <= 3 else "%d tens, from %d up to %d" % (blocks, first, c)),
        W("%d × 5 = %d" % (blocks, n))))
    beats.append(b("%d times 5 is %d. So there are %d odd numbers." % (blocks, n, n), A(str(n))))
    gap = lastodd - first
    beats.append(b(
        "Let us check another way. From %d to %d we jump in twos. %d minus %d is %d, and half of %d is %d jumps." % (first, lastodd, lastodd, first, gap, gap, gap // 2),
        W("%d − %d = %d" % (lastodd, first, gap)), W("%d ÷ 2 = %d" % (gap, gap // 2))))
    beats.append(b(
        "Careful here: %d jumps touch %d numbers, because the starting number counts too. So it is %d again." % (gap // 2, n, n),
        W("%d + 1 = %d" % (gap // 2, n))))
    beats.append(b("So the plan: find the first and last odd number, then count in tens, 5 odd numbers for every ten."))
    return build(qid, beats, origin="rule")


RULES = [place_value, how_many_times, digit_sum, odd_count]


def rule_lessons(qs):
    out = {}
    for q in qs:
        for rule in RULES:
            script = rule(q)
            if script:
                out[q["id"]] = script
                break
    return out
