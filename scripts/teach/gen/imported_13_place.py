"""Batch 13: place value and face value of the digits of one number.

  pf   place value of a digit minus its own face value
  pp   place value of one digit minus the place value of another
"""
from imported_13_lib import ANS, B, FIG, GIVEN, M, N, P, RING, W, ask, chart, gi, lesson, pick

LESSONS = {}

PLACES = ["ones", "tens", "hundreds", "thousands", "ten-thousands", "lakhs"]


def where(number, digit, occurrence=1):
    """(index from the left, place index from the right, nth occurrence) of a digit in the number."""
    s = str(number)
    idx = -1
    for _ in range(occurrence):
        idx = s.index(str(digit), idx + 1)
    return idx, len(s) - 1 - idx, s[:idx + 1].count(str(digit))


def count_right(number, k):
    """Counting the places from the right, as far as place k."""
    s = str(number)
    if k == 0:
        return "It is the very last digit, so it sits in the ones place."
    parts = ["%s is in the %s" % (s[-1], PLACES[0])]
    for i in range(1, k + 1):
        parts.append("%s in the %s" % (s[-1 - i], PLACES[i]))
    return "Count from the right, one digit at a time: " + ", ".join(parts[:-1]) + ", and " + parts[-1] + "."


def place_ask(number, digit, k, say):
    others = []
    if k > 0:
        others.append("the %s place" % PLACES[k - 1])
    if k < 5:
        others.append("the %s place" % PLACES[k + 1])
    if len(others) < 2:
        others.append("the %s place" % PLACES[k + 2 if k == 0 else k - 2])
    return B(say, ask=ask("the %s place" % PLACES[k], others, count_right(number, k)))


def pv_line(digit, k):
    return "%d × %s = %s" % (digit, gi(10 ** k), gi(digit * 10 ** k))


# ── Place value minus face value of the same digit ───────────────────────────

def pf(qid, number, d, context, rupee=False):
    idx, k, nth = where(number, d)
    pv = d * 10 ** k
    diff = pv - d
    n, pvs, ds = gi(number), gi(pv), gi(diff)
    out = ("₹" if rupee else "") + ds
    return lesson(
        B("%s We want the difference between the place value of the %d and the face value of the %d." % (context, d, d),
          GIVEN("q", n), M("q", str(d), "circle", nth), FIG("f", chart(number, idx))),
        B(pick(qid, "face", [
            "Face value is the easy one. It is just the digit itself, wherever it sits, so the face value of %d is %d.",
            "Start with the face value. That is simply the digit as you see it, so the face value of %d is %d.",
        ]) % (d, d), W("fv", "Face value of %d = %d" % (d, d), True)),
        place_ask(number, d, k, "Place value is different: it depends on the seat. Which place is the %d sitting in?" % d),
        B("So this %d means %d %s. %d times %s is %s." % (d, d, PLACES[k], d, gi(10 ** k), pvs),
          N("q", str(d), PLACES[k], nth=nth), W("pv", pv_line(d, k)), N("pv", "= " + pvs, "place value")),
        B("Now, the difference between the two values. Which sum is that?",
          ask=ask("%s − %d" % (pvs, d), ["%s + %d" % (pvs, d), "%d − %d" % (d, d)],
                  "Difference means how far apart two numbers are, so we subtract. And the two numbers are the place value, %s, and the face value, %d." % (pvs, d))),
        B("%s minus %d is %s. That is the difference." % (pvs, d, ds),
          ANS("a", "%s − %d = %s" % (pvs, d, out)), RING("a", out)),
        B("Check by adding back: %s plus %d is %s, the place value we started from." % (ds, d, pvs),
          W("c", "%s + %d = %s" % (ds, d, pvs))),
        B(pick(qid, "close", [
            "So: face value is the digit itself. Place value is the digit times the worth of its place. Find both, then do what the question asks.",
            "Remember the two values. Face value never changes. Place value grows with the seat: tens, hundreds, thousands. Then subtract as asked.",
        ])),
    )


LESSONS[P + "0c7f86b9-d3fd-456e-bed7-4fa36bdb409c"] = pf(
    P + "0c7f86b9", 83147, 3, "The crowd at the cricket matches was 83,147.")
LESSONS[P + "1075cba6-ed27-49f0-a925-414a7d5d0d4d"] = pf(
    P + "1075cba6", 47562, 5, "The big screen at the stadium shows 47,562.")
LESSONS[P + "2b3c80ef-88f2-4f2c-a505-dc3965e151f0"] = pf(
    P + "2b3c80ef", 63509, 5, "The book fair sold 63,509 books.")
LESSONS[P + "4602a73d-48b2-420f-b189-1dc06e5f1973"] = pf(
    P + "4602a73d", 52483, 2, "The train number on the board is 52,483.")
LESSONS[P + "8c0fae1e-edf2-40ff-91b3-c909ad16c251"] = pf(
    P + "8c0fae1e", 46352, 3, "Aarav's class collected 46,352 rupees.", rupee=True)


# ── Place value of one digit minus place value of another ────────────────────

def pp(qid, number, a, b, context, rupee=False, ending=None):
    ia, ka, na = where(number, a)
    ib, kb, nb = where(number, b)
    pa, pb = a * 10 ** ka, b * 10 ** kb
    diff = pa - pb
    n, pas, pbs, ds = gi(number), gi(pa), gi(pb), gi(diff)
    out = ("₹" if rupee else "") + ds
    return lesson(
        B("%s We want the difference between the place value of the %d and the place value of the %d." % (context, a, b),
          GIVEN("q", n), M("q", str(a), "circle", na), M("q", str(b), "circle", nb), FIG("f", chart(number, ia, ib))),
        place_ask(number, a, ka, "Place value depends on where a digit sits. Start with the %d: which place is it in?" % a),
        B("So the %d means %d %s. %d times %s is %s." % (a, a, PLACES[ka], a, gi(10 ** ka), pas),
          N("q", str(a), PLACES[ka], nth=na), W("pa", pv_line(a, ka)), N("pa", "= " + pas, "place value of %d" % a)),
        B("Now the %d. It sits in the %s place, so it means %d times %s, which is %s." % (b, PLACES[kb], b, gi(10 ** kb), pbs),
          N("q", str(b), PLACES[kb], nth=nb), W("pb", pv_line(b, kb)), N("pb", "= " + pbs, "place value of %d" % b)),
        B("Which subtraction gives the difference between the place values?",
          ask=ask("%s − %s" % (pas, pbs), ["%d − %d" % (a, b), "%s − %d" % (pas, b)],
                  "The question asks about place values, so we use what each digit is worth: %s and %s, not the bare digits %d and %d." % (pas, pbs, a, b))),
        B("%s minus %s is %s. Take care with the zeros: we are taking away %d %s." % (pas, pbs, ds, b, PLACES[kb]),
          ANS("a", "%s − %s = %s" % (pas, pbs, out)), RING("a", out)),
        B("Check by adding back: %s plus %s is %s." % (ds, pbs, pas),
          W("c", "%s + %s = %s" % (ds, pbs, pas))),
        B(ending or pick(qid, "close", [
            "So: find the place of each digit, turn each into its place value, and only then subtract. Never subtract the bare digits.",
            "A digit is worth its face times its place. Work out both place values first, and the subtraction at the end is the easy part.",
        ])),
    )


LESSONS[P + "43332488-b05e-4e16-87c5-0a02f0b1c989"] = pp(
    P + "43332488", 76482, 7, 4, "Arjun has saved 76,482 rupees.", rupee=True)
LESSONS[P + "45aa0de4-ab33-4797-af61-e9ed6d841218"] = pp(
    P + "45aa0de4", 76308, 7, 3, "Ravi's train ticket has the number 76,308.")
LESSONS[P + "6356a365-216c-45e4-b2e4-fe386fc1ca35"] = pp(
    P + "6356a365", 60508, 6, 5, "Kavya's lucky token says 60,508.", rupee=True)
LESSONS[P + "7eab7fb8-c267-4184-b19e-c911814b45ed"] = pp(
    P + "7eab7fb8", 52748, 5, 7, "The chai stall collected 52,748 rupees.", rupee=True)
LESSONS[P + "9e438cb2-44b2-4b99-95f4-a7f6dafda183"] = pp(
    P + "9e438cb2", 76258, 6, 2, "Riya writes 76,258 on the board.",
    ending="So: find the place of each digit first. The 6 here was in the thousands, not the ten-thousands. Then subtract the place values.")
