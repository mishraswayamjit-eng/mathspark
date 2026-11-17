"""Lessons for the questions that find two values in one number and then subtract, add or divide them.

pv_pair() teaches every one of them: find what the first digit is worth, find the
second value (a place value, or a face value), choose the sum, work it out, check it.
Every number on the board is computed from the printed number.
"""
from imported_14_lib import (MINUS, a, al, b, ch, digits_of, fig, finish, fmt, g, nt, nth_digit, pchart, pick,  # noqa: F401
                             place_name, ring, ul, w, wl)

P = "AIGEN_grade5_"
T = "IPMTB_grade5_"

LESSONS = {}


def pv_pair(qid, shown, iA, iB, op, intro, ending, unit="ones", faceB=False, ask_sum=None, wrongs=None,
            sum_ifnot=None, compute=None, how="", trap=None, summary=None):
    F = fmt
    ds = digits_of(shown)
    n = len(ds)
    dA, dB = int(ds[iA]), int(ds[iB])
    kA, kB = n - 1 - iA, n - 1 - iB
    mA, mB = 10 ** kA, 10 ** kB
    vA = dA * mA
    vB = dB if faceB else dB * mB
    assert vA > vB
    if op == "÷":
        assert vA % vB == 0
    r = {MINUS: vA - vB, "+": vA + vB, "÷": vA // vB}[op]
    same = dA == dB and not faceB
    refA = "the %d on the left" % dA if same else "the %d" % dA
    refB = "the %d on the right" % dB if same else "the %d" % dB
    pA, pB = place_name(kA, unit), place_name(kB, unit)
    nA, nB = nth_digit(shown, iA), nth_digit(shown, iB)
    cap = lambda s: s[0].upper() + s[1:]

    beats = []
    ops = [g("n", shown), ul("n", ds[iA], nA)]
    if iB != iA:
        ops.append(ul("n", ds[iB], nB))
    beats.append(b(intro, *ops))

    # What is the first digit worth?
    alt = vA // 10 if kA >= 2 else vA * 10
    places = ", ".join(place_name(k, unit) for k in range(kA + 1))
    beats.append(b(
        pick(qid, "chart", [
            "Here is the number in a place-value chart. %s sits in the %s column. So what is it worth?" % (cap(refA), pA),
            "Look at the chart. %s is in the %s column. What is it worth there?" % (cap(refA), pA),
            "A digit is worth more the further left it sits. In the chart, %s is in the %s column. So what is it worth?" % (refA, pA),
        ]),
        fig("chart", pchart(shown, hi=sorted({iA, iB}))),
        ask=ch([F(vA), F(alt), str(dA)],
               "Count the columns from the right: %s. So this %d means %d %s, and that is %s." % (places, dA, dA, pA, F(vA)))))
    beats.append(b(
        pick(qid, "a", [
            "%d times %s is %s. That is the place value of %s." % (dA, F(mA), F(vA), refA),
            "So %s is worth %d times %s, which is %s." % (refA, dA, F(mA), F(vA)),
        ]),
        w("a", "%d × %s = %s" % (dA, F(mA), F(vA))), nt("n", ds[iA], pA, "above", nA)))

    # The second value.
    if faceB:
        if kB > 0 and iB != iA:
            beats.append(b(
                "Now the face value of %d. In this number the %d sits in the %s column, so its place value is %s. "
                "But face value is just the digit as it looks, so it is simply %d." % (dB, dB, pB, F(dB * mB), dB),
                nt("n", ds[iB], "place value %s" % F(dB * mB), "below", nB), wl("b", "Face value of %d = %d" % (dB, dB))))
        else:
            beats.append(b(
                "Now the face value of %d. Face value is just the digit as it looks, whatever column it sits in. "
                "So the face value of %d is simply %d." % (dB, dB, dB),
                wl("b", "Face value of %d = %d" % (dB, dB))))
    elif kB == 0:
        beats.append(b(
            pick(qid, "b0", [
                "Now %s. It is in the %s column, so it is worth just %d." % (refB, pB, dB),
                "And %s sits in the %s column, the smallest one. There it is worth just %d." % (refB, pB, dB),
            ]),
            w("b", "%d × 1 = %d" % (dB, dB)), nt("n", ds[iB], pB, "below", nB)))
    else:
        beats.append(b(
            pick(qid, "b", [
                "Now %s. It is in the %s column, so it is worth %d times %s, which is %s." % (refB, pB, dB, F(mB), F(vB)),
                "And %s sits in the %s column. %d times %s is %s." % (refB, pB, dB, F(mB), F(vB)),
            ]),
            w("b", "%d × %s = %s" % (dB, F(mB), F(vB))), nt("n", ds[iB], pB, "below", nB)))

    # Which sum?
    sA, sB = F(vA), F(vB)
    if op == MINUS:
        say = ask_sum or "Now, the difference between %s and %s. Which sum gives it?" % (sA, sB)
        default_wrongs = ["%d − %d" % (max(dA, dB), min(dA, dB)), "%s + %s" % (sA, sB)]
        default_ifnot = "Difference means subtract. And we subtract what the digits are worth, %s and %s, not the bare digits." % (sA, sB)
    elif op == "+":
        say = ask_sum or "Now we put %s and %s together. Which line gives their sum?" % (sA, sB)
        default_wrongs = ["%d + %d" % (dA, dB), "%s − %s" % (sA, sB)]
        default_ifnot = "Sum means add. And we add what the digits are worth, %s and %s, not the bare digits." % (sA, sB)
    else:
        say = ask_sum or "How many times %s is %s? Which sum tells us?" % (sB, sA)
        default_wrongs = ["%s − %s" % (sA, sB), "%s × %s" % (sA, sB)]
        default_ifnot = "How many times means divide. So we divide what the digits are worth: %s by %s." % (sA, sB)
    right = "%s %s %s" % (sA, op, sB)
    beats.append(b(say, ask=ch([right] + (wrongs or default_wrongs), sum_ifnot or default_ifnot)))

    # Work it out.
    opw = {MINUS: "minus", "+": "plus", "÷": "divided by"}[op]
    if compute:
        beats += compute
    else:
        if trap is None:
            if op == MINUS and same:
                trap = "Careful: the two %ds look alike, but they are not worth the same, so the difference is not 0." % dA
            elif op == MINUS:
                trap = "Careful: subtracting the bare digits, %d and %d, would forget their columns." % (dA, dB)
            elif op == "+":
                trap = "Careful: adding the bare digits, %d and %d, would forget their columns." % (dA, dB)
            else:
                trap = ""
        say = "%s %s %s is %s. %s %s" % (sA, opw, sB, F(r), how, trap)
        beats.append(b(" ".join(say.split()), w("c", "%s = %s" % (right, F(r)))))

    # Check.
    if op == MINUS:
        beats.append(b(pick(qid, "chk", ["Check by adding back: %s plus %s is %s. It fits.",
                                        "Let's check by putting it back: %s plus %s is %s, just where we started."]) % (F(r), sB, sA),
                       w("k", "%s + %s = %s" % (F(r), sB, sA))))
    elif op == "+":
        beats.append(b("Check by taking it off again: %s minus %s is %s. It fits." % (F(r), sB, sA),
                       w("k", "%s − %s = %s" % (F(r), sB, sA))))
    else:
        beats.append(b("Check by multiplying back: %s times %s is %s. It works." % (F(r), sB, sA),
                       w("k", "%s × %s = %s" % (F(r), sB, sA))))

    # The answer.
    label = {MINUS: "Difference = %s", "+": "Sum = %s", "÷": "%s times"}[op] % F(r)
    beats.append(b(ending, al("ans", label), ring("ans", F(r))))

    if summary is None:
        verb = {MINUS: "subtract", "+": "add", "÷": "divide"}[op]
        if faceB:
            summary = "So remember: place value depends on the column, and face value is just the digit. Find both, then %s." % verb
        elif op == "÷":
            summary = "So for how many times: find what each digit is worth, then divide the bigger value by the smaller."
        else:
            summary = pick(qid, "sum", [
                "So the method is: find what each digit is worth in its own column, then %s." % (
                    "take the smaller value from the bigger one" if op == MINUS else "add the two values"),
                "So: the place value of each digit first, from its column. Only then do we %s." % verb,
                "So every time: read each digit's column, write down what it is worth, then %s." % verb,
            ])
    beats.append(b(summary))
    return finish(qid, beats), r


def add(qid, key, *args, **kw):
    lesson, r = pv_pair(qid, *args, **kw)
    assert r == key, (qid, r, key)
    LESSONS[qid] = lesson


# ── How many times ───────────────────────────────────────────────────────────

add(P + "b1c91564-cf56-4484-9be9-3c1173947993", 1000, "52,752", 1, 4, "÷",
    "Team Superstars has the ID 52,752. It has two 2s. The coach asks how many times greater the 2 in the thousands place is than the 2 in the units place.",
    "So the 2 in the thousands place is worth 1000 times the 2 in the units place.",
    unit="units",
    ask_sum="How many times greater is 2000 than 2? Which sum tells us?",
    wrongs=["2000 − 2", "2 ÷ 2"],
    how="That is just half of 2000.",
    trap="Careful: taking 2 away from 2000 would tell us how much more, not how many times.")

add(P + "cf809cdc-c593-4f99-a744-5c3a51752d51", 1500, "63,842", 1, 4, "÷",
    "Ananya's tile shows 63,842. She wonders how many times bigger the place value of the 3 is than the place value of the 2.",
    "So the place value of the 3 is 1500 times the place value of the 2.",
    unit="units",
    wrongs=["3 ÷ 2", "3000 − 2"],
    how="That is just half of 3000.",
    trap="Careful: dividing the bare digits, 3 by 2, forgets that the 3 stands for thousands.")

HALVE_A = [
    b("Dividing by 8 looks hard. But 8 is 2 times 2 times 2, so we can simply halve, 3 times over.",
      w("h0", "8 = 2 × 2 × 2")),
    b("Half of 70,000 is 35,000. Half of 35,000 is 17,500. And half of 17,500 is 8750.",
      w("h1", "70,000 ÷ 2 = 35,000"), w("h2", "35,000 ÷ 2 = 17,500"), w("h3", "17,500 ÷ 2 = 8750")),
    b("Three halvings make a divide by 8. So 70,000 divided by 8 is 8750.",
      w("c", "70,000 ÷ 8 = 8750")),
]

add(P + "e4f3ec79-bcf9-441c-a7c5-ea590866ec99", 8750, "76,308", 0, 4, "÷",
    "Arjun has saved 76,308 rupees. He wonders how many times the place value of the 7 is greater than the face value of the 8.",
    "So the place value of the 7 is 8750 times the face value of the 8.",
    unit="units", faceB=True,
    wrongs=["70,000 × 8", "70,000 − 8"],
    sum_ifnot="How many times one number goes into another is a divide. So it is 70,000 divided by 8.",
    compute=HALVE_A)

HALVE_B = [
    b("Here is a neat way to divide by 8: halve, halve again, and halve once more. That works because 2 times 2 times 2 is 8.",
      w("h0", "2 × 2 × 2 = 8")),
    b("70,000 halved is 35,000. Halve again: 17,500. And once more: 8750.",
      w("h1", "70,000 ÷ 2 = 35,000"), w("h2", "35,000 ÷ 2 = 17,500"), w("h3", "17,500 ÷ 2 = 8750")),
    b("So 70,000 divided by 8 is 8750. Careful: dividing by 80, the place value of the 8, would give a much smaller answer.",
      w("c", "70,000 ÷ 8 = 8750")),
]

add(P + "fb264797-c1c7-4001-abf2-a47b8f7fb920", 8750, "76,482", 0, 3, "÷",
    "Ananya has 76,482 rupees in her piggy bank. Her father asks: the place value of the 7 is how many times the face value of the 8?",
    "So Ananya should say 8750 times.",
    faceB=True,
    wrongs=["70,000 ÷ 80", "70,000 − 8"],
    sum_ifnot="How many times means divide. And we divide by the face value of the 8, which is 8, not by 80.",
    compute=HALVE_B)

# ── Place value minus face value ─────────────────────────────────────────────

add(P + "be9ccf78-94f6-45c4-98a1-742afbccdbdf", 6993, "47,652", 1, 1, MINUS,
    "Ananya's card shows 47,652. Her teacher asks for the difference between the place value of the 7 and the face value of the 7.",
    "So the difference is 6993.",
    faceB=True,
    ask_sum="Now we want the difference between the two. Which sum is it?",
    wrongs=["7 − 7", "7000 + 7"],
    sum_ifnot="The place value is 7000 and the face value is 7. Difference means subtract, so it is 7000 minus 7.",
    trap="Careful: it is the same digit, but its place value and its face value are not the same, so the answer is not 0.")

# ── Difference between two place values ──────────────────────────────────────

add(P + "b68fd5df-2b16-46dd-b017-a532cefddda7", 79600, "86,452", 0, 2, MINUS,
    "The firecrackers cost 86,452 rupees. Arjun takes the place value of the 4 away from the place value of the 8. Let's find what he gets.",
    "So Arjun gets 79,600.",
    ask_sum="Arjun subtracts the place value of the 4 from the place value of the 8. Which sum is that?",
    trap="Careful: 8 minus 4 would give just 4, and that forgets the columns completely.")

add(P + "cf8eb684-7c68-419b-8814-6919efbdc6fe", 2200, "73809", 1, 2, MINUS,
    "Riya's number is 73809. We want the difference between the place value of the 8 and the place value of the 3. Let's start with the 3, because it sits further left.",
    "So her friend should answer 2200.",
    trap="Careful: 8 is the bigger digit, but the 3 is worth more, because it sits further left. So the 800 comes off the 3000.")

add(P + "dfd627e9-76db-49e9-91db-6d63282073a9", 68000, "72,836", 0, 1, MINUS,
    "The chai stall collected 72,836 rupees. Priya subtracts the place value of the 2 from the place value of the 7. What does she get?",
    "So Priya gets 68,000.",
    ask_sum="Priya takes the place value of the 2 away from the place value of the 7. Which sum is that?",
    trap="Careful: 7 minus 2 gives 5, but that only compares the digits. The 7 stands for ten-thousands and the 2 for thousands.")

add(T + "ch02_q002", 7920, "48,183", 1, 3, MINUS,
    "The number 48,183 has two 8s in it. We want the difference between their place values.",
    "So the difference between the two place values is 7920.")

add(T + "ch02_q025", 69993, "3976217", 2, 6, MINUS,
    "Here is 3976217. The digit 7 appears twice, and we want the difference between its two place values.",
    "So the difference between the place values of the two 7s is 69,993.",
    how="Taking 7 away drops us just below 70,000.")

add(T + "ch02_q036", 69993, "58,70,257", 2, 6, MINUS,
    "Here is 58,70,257, with the commas placed the Indian way. It has two 7s, and we want the difference between their place values.",
    "So the difference is 69,993.",
    trap="Careful: 70,000 itself is one of the choices, but that is only the bigger place value. The 7 still has to come off.")

add(T + "ch05_q021", 491000, "25,69,183", 1, 3, MINUS,
    "In 25,69,183 we want the difference between the place values of the 5 and the 9.",
    "So the difference is 4,91,000.",
    trap="Careful: 9 is the bigger digit, but the 5 is worth far more, because it sits further left.")

add(T + "ch05_q046", 2990, "23516", 1, 3, MINUS,
    "In 23516 we want the difference between the place values of the 3 and the 1.",
    "So the difference is 2990.",
    trap="Careful: 3 minus 1 is only 2, and that forgets the columns. The 3 stands for thousands and the 1 for tens.")

# ── Sum of two place values ──────────────────────────────────────────────────

add(T + "ch02_q037", 90900, "897923", 1, 3, "+",
    "Here is 897923. The digit 9 appears twice, and we want the sum of its two place values.",
    "So the sum of the place values of the two 9s is 90,900.",
    how="The 900 slots straight into the empty hundreds place.",
    trap="Careful: 9 plus 9 would add the bare digits and forget their columns.")

add(T + "ch05_q020", 7000100, "73,46,125", 0, 4, "+",
    "In 73,46,125 we want the sum of the place values of the 7 and the 1.",
    "So the sum is 70,00,100.",
    how="The 100 drops into the empty hundreds place.",
    trap="Careful with the zeros: the 1 belongs in the hundreds place, not the thousands.")

add(T + "ch05_q045", 80001, "987321", 1, 5, "+",
    "In 987321 we want the sum of the place values of the 8 and the 1.",
    "So the sum is 80,001.",
    how="The 1 drops into the empty ones place.",
    trap="Careful: sum means add. Taking the 1 away instead would land just below 80,000.")
