"""Batch 13: number puzzles, where clues give the digits of a number one by one."""
from imported_13_lib import ANS, B, FIG, GIVEN, M, N, P, RING, W, ask, chart, gi, lakh_words, lesson, pick
from imported_13_place import PLACES, pv_line

LESSONS = {}


# ── The end of a puzzle that asks for a difference from the lakhs digit ──────

def ending(number, L, k2, d2, mode, rest_say):
    """Beats from 'here is the whole number' to the check.

    L is the lakhs digit; d2 is the other digit, in place k2 (counted from the right).
    mode 'pv' subtracts the other digit's place value; 'fv' subtracts its face value.
    """
    big = L * 100000
    v2 = d2 * 10 ** k2 if mode == "pv" else d2
    diff = big - v2
    bigs, v2s, ds = gi(big), gi(v2), gi(diff)
    beats = [
        B(rest_say, W("n", gi(number)), FIG("f", chart(number, 0, 5 - k2))),
        B("The %d sits in the lakhs place. What is its place value?" % L,
          ask=ask(bigs, [str(L), gi(L * 10000)],
                  "Place value is the digit times the worth of its place. In the lakhs place, a %d is worth %d lakh." % (L, L))),
    ]
    if mode == "pv":
        beats.append(B("So the %d is worth %d lakh. And the %d in the %s place is worth %d times %s, which is %s." % (
            L, L, d2, PLACES[k2], d2, gi(10 ** k2), v2s),
            W("pa", "%d × 1,00,000 = %s" % (L, bigs)), W("pb", pv_line(d2, k2))))
        sub = "Careful: we subtract what the digits are worth, not the digits themselves. %d lakh minus %s is %s." % (
            L, v2s, lakh_words(diff))
    else:
        beats.append(B("So the %d is worth %d lakh. For the %d in the %s place, the question asks for face value, and that is just the digit, %d." % (
            L, L, d2, PLACES[k2], d2),
            W("pa", "%d × 1,00,000 = %s" % (L, bigs)), W("pb", "Face value of %d = %d" % (d2, d2), True)))
        sub = "Careful: face value this time, so we take away only %d, not what the %d is worth in its place. %d lakh minus %d is %s." % (
            d2, d2, L, d2, lakh_words(diff))
    beats.append(B(sub, ANS("a", "%s − %s = %s" % (bigs, v2s, ds)), RING("a", ds), N("a", ds, lakh_words(diff))))
    beats.append(B("Check by adding back: %s plus %s makes %d lakh." % (lakh_words(diff), v2s, L),
                   W("c", "%s + %s = %s" % (ds, v2s, bigs))))
    return beats


def tip(qid, second):
    return B(pick(qid, "tip", [
        "Here is a tip: read the last line first. It asks only about the lakhs digit and the %s digit, so those are the 2 we must find.",
        "Before we chase all 6 clues, look at what is asked. Only the lakhs digit and the %s digit matter, so we find those 2 first.",
    ]) % second, M("q", "Lakhs"))


# ── Lakhs = tens + 3, ten-thousands = half of hundreds ───────────────────────

def ravi(qid, who, tens, hundreds, number, mode, rest_say, closing):
    lakhs, tth = tens + 3, hundreds // 2
    value = "place value" if mode == "pv" else "face value"
    return lesson(
        B("%s writes a 6-digit number and gives 6 clues. We want the difference between the place value of the lakhs digit and the %s of the ten-thousands digit." % (who, value),
          GIVEN("q", "Lakhs = tens + 3. Ten-thousands = half of hundreds.", True),
          W("q2", "Hundreds = %d. Tens = %d." % (hundreds, tens), True, "given")),
        tip(qid, "ten-thousands"),
        B("The lakhs digit is 3 more than the tens digit. The tens digit is %d, and %d plus 3 is %d." % (tens, tens, lakhs),
          W("l", "%d + 3 = %d" % (tens, lakhs)), N("l", "= %d" % lakhs, "lakhs digit")),
        B("The ten-thousands digit is half the hundreds digit. The hundreds digit is %d, and half of %d is %d." % (hundreds, hundreds, tth),
          W("t", "%d ÷ 2 = %d" % (hundreds, tth)), N("t", "= %d" % tth, "ten-thousands digit")),
        ending(number, lakhs, 4, tth, mode, rest_say),
        B(closing),
    )


LESSONS[P + "37ec9774-1a37-4d8b-81d9-79e57a46d036"] = ravi(
    P + "37ec9774", "Ravi", 4, 8, 746842, "pv",
    "The thousands digit is the tens digit plus the units digit: 4 plus 2 is 6. So the whole number reads 7, 4, 6, 8, 4, 2.",
    "So in a clue puzzle, read the question first and find the digits it needs. Then turn each digit into its place value before you subtract.")

LESSONS[P + "54ce7dae-0b5f-4ae5-b4a7-ef9876cb50ea"] = ravi(
    P + "54ce7dae", "Ravi", 2, 8, 547826, "pv",
    "The thousands digit is 7, and the units digit is 4 plus 2, which is 6. So the whole number reads 5, 4, 7, 8, 2, 6.",
    "A digit is worth its face times its place. So find the digits from the clues, change them into place values, and only then subtract.")

LESSONS[P + "578a4973-9cc6-4c60-bf80-a19e9e9dbc5e"] = ravi(
    P + "578a4973", "Ravi", 5, 8, 840850, "pv",
    "The thousands digit and the units digit are both 0. So the whole number reads 8, 4, 0, 8, 5, 0.",
    "So: let the question tell you which digits to find. Then it is place value minus place value, never digit minus digit.")

LESSONS[P + "7dfbff5d-8316-45a3-ab9d-3aba8b1994d8"] = ravi(
    P + "7dfbff5d", "Priya", 4, 8, 745841, "fv",
    "The thousands digit is the units digit plus the tens digit: 1 plus 4 is 5. So the whole number reads 7, 4, 5, 8, 4, 1.",
    "So read every word. Place value is the digit times its place, and face value is just the digit. This question wanted one of each.")


# ── Lakhs = twice tens, tens = units + 1 ─────────────────────────────────────

Q = P + "0e7fdbc0-6472-4534-ba11-2b690bf40b2d"
LESSONS[Q] = lesson(
    B("Arjun writes a secret 6-digit number and gives 6 clues. We want the difference between the place value of the lakhs digit and the place value of the tens digit.",
      GIVEN("q", "Lakhs = 2 × tens. Tens = units + 1. Units = 1.", True)),
    tip(Q, "tens"),
    B("Start at the end of the chain. The units digit is 1, and the tens digit is one more than that: 1 plus 1 is 2.",
      W("t", "1 + 1 = 2"), N("t", "= 2", "tens digit")),
    B("The lakhs digit is twice the tens digit. 2 times 2 is 4.",
      W("l", "2 × 2 = 4"), N("l", "= 4", "lakhs digit")),
    ending(454321, 4, 1, 2, "pv",
           "The other clues give ten-thousands 5, thousands 4 and hundreds 3. So the whole number reads 4, 5, 4, 3, 2, 1."),
    B("So in a clue puzzle, find the digit that the other clues lean on first. Then change digits into place values before you subtract."),
)


# ── Lakhs = largest one-digit prime, thousands = square root of 81 ───────────

Q = P + "20ea0eaf-d2fc-4e33-9d93-64ce1ba52ca1"
LESSONS[Q] = lesson(
    B("Arjun thinks of a 6-digit number and gives 6 clues. We want the difference between the place value of the lakhs digit and the place value of the thousands digit.",
      GIVEN("q", "Lakhs = largest single-digit prime. Thousands = √81.", True)),
    tip(Q, "thousands"),
    B("The lakhs digit is the largest prime number that has just one digit. Which number is that?",
      ask=ask("7", ["9", "8"],
              "A prime has no factors except 1 and itself. But 9 is 3 times 3, and 8 is 2 times 4, so neither is prime. The largest one-digit prime is 7.")),
    B("The one-digit primes are 2, 3, 5 and 7, so the lakhs digit is 7. That was the trap: 9 is the biggest digit, but it is not prime.",
      W("pr", "Primes below 10: 2, 3, 5, 7", True), M("pr", "7", "circle"), N("pr", "7", "lakhs digit")),
    B("The thousands digit is the square root of 81: the number that, times itself, makes 81. 9 times 9 is 81, so the digit is 9.",
      W("sq", "9 × 9 = 81"), N("sq", "9", "thousands digit")),
    ending(719303, 7, 3, 9, "pv",
           "The other clues, worked the same way, give 1 for the ten-thousands digit, then 3, 0 and 3. So the whole number reads 7, 1, 9, 3, 0, 3."),
    B("So: let the question tell you which digits to find, crack those clues with care, and then subtract place values, not digits."),
)


# ── Build the whole 6-digit number ───────────────────────────────────────────

Q = P + "646a6965-a648-4131-a4f3-d89b3c3aa444"
LESSONS[Q] = lesson(
    B("Arjun's father counts the money from the chai stall. The total is a 6-digit number, and 6 clues tell us its digits. Let's build it, one seat at a time.",
      GIVEN("q", "Ten-thousands 5. Hundreds 3. Units 1.", True),
      W("q2", "Lakhs = 2 × tens. Tens = units + 1.", True, "given"),
      W("q3", "Thousands = hundreds + units.", True, "given")),
    B("3 digits are simply told to us: 5 in the ten-thousands place, 3 in the hundreds place, and 1 in the units place.",
      M("q", "5"), M("q", "3"), M("q", "1")),
    B("The lakhs digit is twice the tens digit. So which digit must we find before the lakhs digit?",
      ask=ask("the tens digit", ["the thousands digit", "the hundreds digit"],
              "The lakhs clue leans on the tens digit. Until we know the tens digit, there is nothing to double.")),
    B("The tens digit is one more than the units digit. 1 plus 1 is 2.",
      W("t", "1 + 1 = 2"), N("t", "= 2", "tens")),
    B("Now the lakhs digit: twice the tens digit. 2 times 2 is 4.",
      W("l", "2 × 2 = 4"), N("l", "= 4", "lakhs")),
    B("And the thousands digit is the hundreds digit plus the units digit. 3 plus 1 is 4.",
      W("th", "3 + 1 = 4"), N("th", "= 4", "thousands")),
    B("Seat them in order, starting from the lakhs place: 4, 5, 4, 3, 2, 1. That is 4 lakh 54 thousand 321 rupees.",
      ANS("a", "₹4,54,321"), RING("a", "₹4,54,321"), N("a", "4,54,321", "4 lakh 54 thousand 321"), FIG("f", chart(454321))),
    B("Careful with the choices: some use the very same digits in different seats. Say the clue for each seat as you check it."),
    B("Check 2 of the clues. The lakhs digit, 4, is twice the tens digit, 2. And the thousands digit, 4, is 3 plus 1. It all fits."),
    B("So in a clue puzzle, write down what you are told, then find each digit that the others lean on, and seat them in order at the end."),
)


# ── Build a 5-digit cheque amount ────────────────────────────────────────────

Q = P + "1793fb6c-a077-417e-af22-3f3fd11525a6"
LESSONS[Q] = lesson(
    B("Riya's cheque is for a 5-digit amount, and 5 clues tell us its digits. Let's build it, one seat at a time.",
      GIVEN("q", "Units 2. Thousands 7.", True),
      W("q2", "Ten-thousands = units + 3. Hundreds = half of 7, down.", True, "given"),
      W("q3", "Tens = units + hundreds.", True, "given")),
    B("2 digits are simply told to us: the units digit is 2, and the thousands digit is 7.",
      M("q", "2"), M("q", "7")),
    B("The ten-thousands digit is 3 more than the units digit. 2 plus 3 is 5.",
      W("tt", "2 + 3 = 5"), N("tt", "= 5", "ten-thousands")),
    B("The hundreds digit is half of the thousands digit, rounded down. Half of 7, rounded down, is what?",
      ask=ask("3", ["4", "3.5"],
              "Half of 7 is 3 and a half. A digit has to be a whole number, and rounded down means we drop the half. So it is 3.")),
    B("7 divided by 2 is 3.5. Rounding down drops the half, so the hundreds digit is 3.",
      W("h", "7 ÷ 2 = 3.5"), N("h", "3.5", "round down: 3")),
    B("The tens digit is the units digit plus the hundreds digit. 2 plus 3 is 5.",
      W("t", "2 + 3 = 5"), N("t", "= 5", "tens")),
    B("Seat them in order, from the ten-thousands place: 5, 7, 3, 5, 2. The cheque is for 57,352 rupees.",
      ANS("a", "₹57,352"), RING("a", "₹57,352"), FIG("f", chart(57352))),
    B("Look at the 4 choices: they are the same except for the tens digit. So that last clue, 2 plus 3, is the one that decides it.",
      M("t", "= 5", "box")),
    B("So in a clue puzzle, write down what you are told, find the digits that other clues lean on, and seat them in order at the end."),
)


# ── Find the number, then add its digits ─────────────────────────────────────

Q = P + "05e3dee5-df17-4b19-bfa5-f2b873646c7d"
LESSONS[Q] = lesson(
    B("Riya writes a 5-digit number and gives 5 clues. We must find the number, and then the sum of all its digits.",
      GIVEN("q", "Place value of ten-thousands digit = 50,000", True),
      W("q2", "It is units + 3. Tens = 2 × units.", True, "given"),
      W("q3", "Thousands 7. Hundreds 0.", True, "given")),
    B("Start with the place value clue: the digit in the ten-thousands place is worth 50,000. So what is that digit?",
      W("g", "? × 10,000 = 50,000"),
      ask=ask("5", ["50", "8"],
              "A digit in the ten-thousands place is worth the digit times 10,000. And 5 times 10,000 makes 50,000, so the digit is 5.")),
    B("5 times 10,000 is 50,000, so the ten-thousands digit is 5.",
      W("tt", "5 × 10,000 = 50,000")),
    B("Careful here: that 5 is 3 more than the units digit, so the units digit is the smaller one. Go backwards and subtract: 5 minus 3 is 2.",
      W("u", "5 − 3 = 2"), N("u", "= 2", "units")),
    B("The tens digit is twice the units digit. 2 times 2 is 4.",
      W("t", "2 × 2 = 4"), N("t", "= 4", "tens")),
    B("The thousands digit is 7 and the hundreds digit is 0. So the number reads 5, 7, 0, 4, 2.",
      W("n", "57,042"), FIG("f", chart(57042))),
    B("We are not done: the question asks for the sum of the digits. 5 plus 7 is 12, and the 0 adds nothing.",
      W("s1", "5 + 7 + 0 = 12")),
    B("12 plus 4 is 16, and 16 plus 2 is 18. The digits add up to 18.",
      W("s2", "12 + 4 = 16"), ANS("a", "5 + 7 + 0 + 4 + 2 = 18"), RING("a", "18")),
    B("Check the clues against 5, 7, 0, 4, 2. The first digit, 5, is 3 more than the last digit, 2. And the tens digit, 4, is twice 2."),
    B("So find the digits from the clues, seat them in order, and then answer what was asked. Here it was the sum of the digits, not the number."),
)
