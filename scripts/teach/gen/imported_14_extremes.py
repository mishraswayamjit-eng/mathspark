"""Lessons about the greatest and smallest numbers with so many digits.

ext() teaches the two-number questions (greatest 4-digit number minus smallest 3-digit
number, and so on): name each special number, do the sum, check it. Every value is
computed from the number of digits. The add-one and take-one questions, and the two
"write the smallest number" questions, are written out beat by beat below.
"""
from imported_14_lib import MINUS, a, al, b, ch, fig, finish, fmt, gl, nt, pchart, pick, ring, ul, w, wl, x  # noqa: F401

T = "IPMTB_grade5_ch02_"
F = fmt

LESSONS = {}


def G(n, even=False):
    return {"kind": "G", "n": n, "even": even, "value": 10 ** n - (2 if even else 1)}


def S(n, even=False):
    return {"kind": "S", "n": n, "even": even, "value": 10 ** (n - 1)}


def board_name(s, cap=True):
    name = "%s %d-digit %snumber" % ("greatest" if s["kind"] == "G" else "smallest", s["n"], "even " if s["even"] else "")
    return name[0].upper() + name[1:] if cap else name


def say_name(s):
    return board_name(s, False).replace("-", " ")


def ask_for(s, qid, second):
    n, v = s["n"], s["value"]
    lead = "And the %s?" if second else pick(qid, "askq", ["What is the %s?", "First, the %s. Which one is it?"])
    say = lead % say_name(s)
    if s["kind"] == "G" and not s["even"]:
        return say, ch([F(v), F(10 ** n), F(10 ** (n - 1))],
                       "The greatest %d digit number has the biggest digit, 9, in all %d places. That is %s. "
                       "One more than that would need another digit." % (n, n, F(v)))
    if s["kind"] == "G":
        return say, ch([F(v), F(v + 1), F((10 ** n - 1) // 9 * 8)],
                       "%s is the greatest %d digit number, but it ends in 9, so it is odd. "
                       "One step down is %s. It ends in 8, so it is even." % (F(v + 1), n, F(v)))
    if not s["even"]:
        return say, ch([F(v), F((10 ** n - 1) // 9), F(v - 1)],
                       "A number cannot start with 0, so the smallest digit we can put in front is 1. "
                       "Then every other place gets a 0. That makes %s." % F(v))
    return say, ch([F(v), F(v + 2), F(2 * v)],
                   "The smallest %d digit number is %s. It ends in 0, and a number ending in 0 is even. "
                   "So it is already the one we want." % (n, F(v)))


def name_ops(s, lid):
    v = s["value"]
    ops = []
    if s["kind"] == "G" and s["even"]:
        ops.append(w(lid + "0", "%s − 1 = %s" % (F(v + 1), F(v))))
    ops += [wl(lid, "%s = %s" % (board_name(s), F(v))), ul(lid, F(v))]
    return ops


def confirm(s, qid, lid):
    n, v = s["n"], s["value"]
    if s["kind"] == "G" and not s["even"]:
        say = pick(qid, "cG" + lid, ["Yes, a 9 in every one of the %d places: %s.", "That is it. All %d places hold a 9, so it is %s."]) % (n, F(v))
    elif s["kind"] == "G":
        say = "Yes. %s is odd, so we step down 1 to %s, which ends in 8." % (F(v + 1), F(v))
    elif not s["even"]:
        say = pick(qid, "cS" + lid, ["Yes: a 1 in front, then zeros. %s.", "That is it. A 1 to lead, and 0 in every other place: %s."]) % F(v)
    else:
        say = "Yes, %s. It ends in 0, so it is even already." % F(v)
    return b(say, *name_ops(s, lid))


def tell(s, qid, lid, second):
    n, v = s["n"], s["value"]
    if s["kind"] == "G" and not s["even"]:
        say = pick(qid, "tG" + lid, [
            "The %s has the biggest digit, 9, in every place. With %d places that is %s.",
            "For the %s, fill every place with the biggest digit, 9. There are %d places, so it is %s.",
        ]) % (say_name(s), n, F(v))
    elif s["kind"] == "G":
        say = "The greatest %d digit number is %s, but it ends in 9, so it is odd. Step down 1 to %s. That ends in 8, so it is even." % (
            n, F(v + 1), F(v))
    elif not s["even"]:
        say = pick(qid, "tS" + lid, [
            "For the %s, put a 1 in front, because a number cannot start with 0. Fill the other places with 0, and we get %s.",
            "The %s starts with 1, since a number cannot start with 0. Every other place takes a 0. That gives %s.",
        ]) % (say_name(s), F(v))
    else:
        say = "The smallest %d digit number is %s. It ends in 0, so it is even already. Nothing to change." % (n, F(v))
    if second:
        say = "Now the other one. " + say
    return b(say, *name_ops(s, lid))


def ext(qid, key, A, op, B, intro, how, ending, ask="A", compute=None, answer_beats=None, summary=None):
    vA, vB = A["value"], B["value"]
    r = vA + vB if op == "+" else vA - vB
    assert r == key, (qid, r, key)
    task = "%s %s %s" % (board_name(A), op, board_name(B, False))
    assert len(task) <= 60, task
    beats = [b(intro, gl("q", task))]
    for s, lid, tag in ((A, "a", "A"), (B, "b", "B")):
        second = tag == "B"
        if tag in ask:
            say, c = ask_for(s, qid, second)
            beats.append(b(say, ask=c))
            beats.append(confirm(s, qid, lid))
        else:
            beats.append(tell(s, qid, lid, second))
    line = "%s %s %s = %s" % (F(vA), op, F(vB), F(r))
    if compute:
        beats += compute
    else:
        beats.append(b("%s %s %s is %s. %s" % (F(vA), "plus" if op == "+" else "minus", F(vB), F(r), how), w("c", line)))
    if op == "+":
        beats.append(b(pick(qid, "chk", ["Check by taking it off again: %s minus %s is %s. It fits.",
                                        "Let's check by undoing it: %s minus %s is %s, right where we started."]) % (F(r), F(vB), F(vA)),
                       w("k", "%s − %s = %s" % (F(r), F(vB), F(vA)))))
    else:
        beats.append(b(pick(qid, "chk", ["Check by adding back: %s plus %s is %s. It fits.",
                                        "Let's check by undoing it: %s plus %s is %s, right where we started."]) % (F(r), F(vB), F(vA)),
                       w("k", "%s + %s = %s" % (F(r), F(vB), F(vA)))))
    if answer_beats:
        beats += answer_beats
    else:
        beats.append(b(ending, al("ans", "%s = %s" % ("Sum" if op == "+" else "Difference", F(r))), ring("ans", F(r))))
    beats.append(b(summary or pick(qid, "sum", [
        "So in a question like this, write down each special number first: 9s for the greatest, a 1 and zeros for the smallest. Then do the sum.",
        "So the plan is: name the two special numbers, write them down, and only then add or subtract.",
        "So remember: the greatest is all 9s, the smallest is a 1 followed by zeros. Find both, then work out the sum.",
    ])))
    LESSONS[qid] = finish(qid, beats)


# ── Two special numbers, then a sum ──────────────────────────────────────────

ext(T + "q005", 100999, G(5), "+", S(4),
    "We are adding two special numbers: the smallest 4 digit number and the greatest 5 digit number. Let's name each one before we add.",
    "", "So the two numbers add up to 1,00,999.",
    compute=[
        b("Here is a quick way to add 1000. Just 1 more lifts 99,999 up to 1,00,000, a round number.",
          w("c1", "99,999 + 1 = 1,00,000")),
        b("We have used 1 of the 1000, so 999 are still to go on. 1,00,000 plus 999 is 1,00,999.",
          w("c2", "1000 − 1 = 999"), w("c3", "1,00,000 + 999 = 1,00,999")),
        b("So 99,999 plus 1000 is 1,00,999. Careful: the 1000 goes on at the thousands place. It is not just a 1 stuck on the front.",
          w("c", "99,999 + 1000 = 1,00,999")),
    ])

ext(T + "q006", 9899, G(4), MINUS, S(3),
    "Two special numbers here: the greatest 4 digit number and the smallest 3 digit number. We find each one, then take the smaller from the bigger.",
    "Only the hundreds change: 9 hundreds take away 1 hundred leaves 8 hundreds. Careful: taking away 1 instead of 100 is the slip here.",
    "So the difference is 9899.", ask="B")

ext(T + "q008", 8998, G(4, True), MINUS, S(4, True),
    "This time both numbers must be even: the greatest 4 digit even number and the smallest 4 digit even number. An even number ends in 0, 2, 4, 6 or 8.",
    "Only the thousands change: 9 thousands take away 1 thousand leaves 8 thousands. Careful: starting from 9999 instead would use an odd number.",
    "So the difference is 8998.",
    summary="So when a number must be even, look at its last digit. Find the greatest and the smallest that end in an even digit, then subtract.")

ext(T + "q011", 1999, G(3), "+", S(4),
    "We want the sum of the greatest 3 digit number and the smallest 4 digit number. Let's name them one at a time.",
    "The 999 simply fills the three empty places after the 1. Careful: the smallest 4 digit number is a 1 with three zeros, not a row of 1s.",
    "So the sum is 1999.")

ext(T + "q012", 11000, S(5), "+", S(4),
    "Two smallest numbers this time: the smallest 5 digit number and the smallest 4 digit number. We name each one, then add.",
    "The 1 thousand slots into the empty thousands place. Careful: the smallest numbers are a 1 with zeros, not a row of 1s.",
    "So together they make 11,000.")

ext(T + "q013", 10998, G(4), "+", G(3),
    "Two greatest numbers this time: the greatest 3 digit number and the greatest 4 digit number. Both are made the same way.",
    "", "So the sum is 10,998.", ask="B",
    compute=[
        b("Adding 999 is fiddly, but 999 is just 1 less than 1000. So let's add 1000 first. That gives 10,999.",
          w("c1", "999 = 1000 − 1"), w("c2", "9999 + 1000 = 10,999")),
        b("We added 1 too many, so take 1 back off. 10,999 minus 1 is 10,998. Careful: stopping at 10,999 is the slip here.",
          w("c3", "10,999 − 1 = 10,998"), w("c", "9999 + 999 = 10,998")),
    ],
    summary="So the greatest number with so many digits is all 9s. And to add a row of 9s, add the round number just above it, then take 1 off.")

ext(T + "q028", 1, S(5), MINUS, G(4),
    "We want the difference between the smallest 5 digit number and the greatest 4 digit number. Name them both first, and then something neat shows up.",
    "9999 is the very last 4 digit number, and 10,000 is the very next number after it. They are neighbours, so they are just 1 apart.",
    "So the difference is only 1.", ask="AB",
    summary="So the smallest number with 5 digits comes straight after the greatest number with 4 digits. Neighbours are always 1 apart.")

ext(T + "q029", 10099, G(4), "+", S(3),
    "We are adding the smallest 3 digit number and the greatest 4 digit number. Let's name each one first.",
    "", "So the sum is 10,099.", ask="B",
    compute=[
        b("To add 100 to 9999, use just 1 of the 100 first. That lifts 9999 up to 10,000, a round number.",
          w("c1", "9999 + 1 = 10,000")),
        b("That leaves 99 still to add. 10,000 plus 99 is 10,099.",
          w("c2", "100 − 1 = 99"), w("c3", "10,000 + 99 = 10,099")),
        b("So 9999 plus 100 is 10,099. Careful with the zeros: the 99 sits in the tens and ones places, so a 0 stays in the hundreds.",
          w("c", "9999 + 100 = 10,099")),
    ])

ext(T + "q031", 98998, G(5, True), MINUS, S(4, True),
    "Both numbers must be even here: the greatest 5 digit even number and the smallest 4 digit even number. Then we subtract.",
    "Only the thousands change: 9 thousands take away 1 thousand leaves 8 thousands.",
    "", ask="A",
    answer_beats=[
        b("Now look at the three numbers on offer: 98,999, then 99,900, then 98,099. Is our 98,998 one of them?",
          wl("opts", "98,999    99,900    98,099"),
          ask=ch(["No, none of them match", "Yes, the first one", "Yes, the last one"],
                 "Look at the very last digit. Ours ends in 8, and 98,999 ends in 9. Close, but not the same number.")),
        b("None of them is 98,998. The first is 1 too big, because it uses the odd number 99,999. So the right choice is none of these.",
          x("opts", "98,999"), x("opts", "99,900"), x("opts", "98,099"),
          al("ans", "98,998 is not listed: None of these"), ring("ans", "None of these")),
    ],
    summary="So trust your own working. If your answer is checked and it is not in the list, none of these is the right choice.")

ext(T + "q038", 1099, S(4), "+", G(2),
    "We want the sum of the greatest 2 digit number and the smallest 4 digit number. Let's name each one first.",
    "Careful with the hundreds place: it stays 0, because the 99 only fills the tens and the ones.",
    "So the sum is 1099.", ask="B")


# ── One more, one less ───────────────────────────────────────────────────────

LESSONS[T + "q003"] = finish(T + "q003", [
    b("We take the greatest 5 digit number and add one to it. First we need to know which number that is.",
      gl("q", "Greatest 5-digit number + 1 = ?")),
    b("So, what is the greatest 5 digit number?",
      ask=ch(["99,999", "1,00,000", "10,000"],
             "The greatest 5 digit number has the biggest digit, 9, in all 5 places. That is 99,999.")),
    b("Yes, five 9s: 99,999.", wl("a", "Greatest 5-digit number = 99,999"), ul("a", "99,999")),
    b("Now we add 1. Before we work it out, how many digits will the answer have?",
      w("s", "99,999 + 1 = ?"),
      ask=ch(["6 digits", "5 digits"],
             "99,999 is already the greatest number that fits in 5 places. One more cannot fit, so it spills over into a 6th place.")),
    b("Start in the ones place. 9 plus 1 is 10, so we write 0 and carry 1. That carry turns the next 9 into 10 as well, and so on, all the way along.",
      ul("s", "99,999"), nt("s", "99,999", "every 9 becomes 0", "below")),
    b("Every 9 becomes 0, and a new 1 appears in front. That is 1,00,000, which we call 1 lakh.",
      a("ans", "99,999 + 1 = 1,00,000"), ring("ans", "1,00,000")),
    b("Careful: the 1 is not stuck on the end of the number, and it does not just swap places with the last 9. It is added to the ones, and the carry runs the whole way."),
    b("Check by stepping back: 1,00,000 minus 1 is 99,999. It fits.", w("k", "1,00,000 − 1 = 99,999")),
    b("So one more than the greatest 5 digit number is the smallest 6 digit number. A row of 9s always rolls over to a 1 and zeros."),
])

LESSONS[T + "q030"] = finish(T + "q030", [
    b("Add 1 to the greatest 5 digit number. Think of the counter on a scooter that shows how far it has gone, with every wheel showing its biggest digit.",
      gl("q", "Greatest 5-digit number + 1 = ?")),
    b("The biggest digit is 9, and we have 5 places. So the greatest 5 digit number is 99,999.",
      wl("a", "Greatest 5-digit number = 99,999"), fig("chart", pchart("99999"))),
    b("Now add 1 in the ones place. 9 plus 1 makes 10. What do we do with that 10?",
      w("s", "99,999 + 1 = ?"), ul("s", "9", 5),
      ask=ch(["write 0, carry 1", "write 10 at the end", "write 1 at the end"],
             "A place can only hold one digit. So of the 10, the 0 stays in the ones place and the 1 is carried to the tens.")),
    b("Write 0, carry 1. But in the tens place that carry meets another 9, and 9 plus 1 is 10 again. Write 0, carry 1 once more.",
      nt("s", "9", "+1", "above", 5), nt("s", "9", "+1", "above", 4)),
    b("The same thing happens in every place, like wheels on the counter clicking over one after another. In the end the carry has nowhere to go, so it opens a new place in front."),
    b("So we get a 1 followed by five zeros: 1,00,000. That is 1 lakh.",
      a("ans", "99,999 + 1 = 1,00,000"), ring("ans", "1,00,000")),
    b("Careful: the answer has 6 digits, not 5. Count the zeros after the 1, and there should be five of them."),
    b("Check by going back one step: 1,00,000 minus 1 is 99,999, our five 9s.", w("k", "1,00,000 − 1 = 99,999")),
    b("So adding 1 to a row of 9s turns every 9 into 0 and puts a 1 in front. The greatest 5 digit number plus 1 is the smallest 6 digit number."),
])

LESSONS[T + "q026"] = finish(T + "q026", [
    b("This one asks what we get when 1 is added to the greatest 6 digit number. So first, the number itself.",
      gl("q", "Greatest 6-digit number + 1 = ?")),
    b("What is the greatest 6 digit number?",
      ask=ch(["9,99,999", "10,00,000", "1,00,000"],
             "For the greatest number, every place takes the biggest digit, 9. With 6 places that is 9,99,999.")),
    b("Six 9s. With the commas placed the Indian way, it is 9,99,999.",
      wl("a", "Greatest 6-digit number = 9,99,999"), fig("chart", pchart("999999"))),
    b("Now add 1. In the ones place, 9 plus 1 is 10, so we write 0 and carry 1. The carry meets a 9 in the tens place, and the same thing happens again.",
      w("s", "9,99,999 + 1 = ?"), nt("s", "9,99,999", "every 9 becomes 0", "below")),
    b("The carry travels through all six places. What does it leave behind?",
      ask=ch(["a 1 and six zeros", "a 1 and five zeros", "six 9s and a 1"],
             "Each of the six 9s turns into a 0 as the carry passes. Then the carry itself lands in a new place in front, as a 1.")),
    b("A 1 followed by six zeros: 10,00,000. That is 10 lakh.",
      a("ans", "9,99,999 + 1 = 10,00,000"), ring("ans", "10,00,000")),
    b("Careful: adding 1 does not mean writing one more 9, or putting a 1 on the end. The number grows by just one step."),
    b("Check by stepping back: 10,00,000 minus 1 is 9,99,999. It fits.", w("k", "10,00,000 − 1 = 9,99,999")),
    b("So the greatest 6 digit number plus 1 is the smallest 7 digit number. A row of 9s always rolls over to a 1 and zeros."),
])

LESSONS[T + "q004"] = finish(T + "q004", [
    b("We take the largest 3 digit number and subtract one from it. First, which number is the largest with 3 digits?",
      gl("q", "Largest 3-digit number − 1 = ?")),
    b("What is the largest 3 digit number?",
      ask=ch(["999", "1000", "100"],
             "Count the digits. 1000 has 4 digits, so it is too long. The largest number with 3 digits has a 9 in every place: 999.")),
    b("Yes, three 9s: 999.", wl("a", "Largest 3-digit number = 999"), ul("a", "999")),
    b("Now, one is subtracted. Which way do we move from 999?",
      ask=ch(["1 step down", "1 step up"],
             "Subtract means take away, so the number gets smaller. We step down from 999, not up.")),
    b("One step down. Only the ones place changes: 9 ones take away 1 leaves 8 ones. The hundreds and the tens stay as they are.",
      a("ans", "999 − 1 = 998"), ul("ans", "9", 3), ring("ans", "998")),
    b("Careful: one step up would be 1000, and that is adding 1. Read the question word by word: it says subtracted."),
    b("Check by adding the 1 back: 998 plus 1 is 999.", w("k", "998 + 1 = 999")),
    b("So name the special number first, then do exactly what the question says. Here that gives 998."),
])

LESSONS[T + "q027"] = finish(T + "q027", [
    b("We take the smallest 4 digit number and subtract 1 from it. First we need that smallest number.",
      gl("q", "Smallest 4-digit number − 1 = ?")),
    b("What is the smallest 4 digit number?",
      ask=ch(["1000", "1111", "1001"],
             "A number cannot start with 0, so a 1 goes in front. Every other place can take a 0, the smallest digit. That makes 1000.")),
    b("Yes: a 1 in front, then three zeros. 1000.", wl("a", "Smallest 4-digit number = 1000"), ul("a", "1000")),
    b("Now take away 1. Before we work it out, how many digits will the answer have?",
      w("s", "1000 − 1 = ?"),
      ask=ch(["3 digits", "4 digits"],
             "1000 is the very first number with 4 digits. Step back from it and we fall below, so only 3 digits are left.")),
    b("We cannot take 1 from 0, so we borrow all the way from the 1 in front. Each 0 turns into a 9, and the 1 in front is used up.",
      nt("s", "1000", "borrow from the 1", "below")),
    b("That leaves three 9s: 999.", a("ans", "1000 − 1 = 999"), ring("ans", "999")),
    b("Careful: the answer is not still 1000, and the zeros do not just stay put. One less than a 1 with zeros is always a row of 9s."),
    b("Check by adding the 1 back: 999 plus 1 is 1000.", w("k", "999 + 1 = 1000")),
    b("So one less than the smallest 4 digit number is the greatest 3 digit number. They are neighbours on the number line."),
])


# ── Write the smallest number ────────────────────────────────────────────────

LESSONS[T + "q023"] = finish(T + "q023", [
    b("We want the smallest three digit number. Three digits means three places to fill: hundreds, tens and ones.",
      gl("q", "Smallest three-digit number = ?")),
    b("To keep a number small we choose small digits. What is the smallest digit that can go in the hundreds place?",
      ask=ch(["1", "0", "9"],
             "With a 0 in the hundreds place, only two real digits would be left. So the smallest digit that can lead is 1.")),
    b("So 1 goes in front. A 0 there would not count, because a number does not start with 0.",
      wl("h", "hundreds: 1")),
    b("Now the tens and the ones. Which digit keeps the number as small as it can be?",
      ask=ch(["0", "1"],
             "0 is smaller than 1, and 0 is allowed in the tens and ones places. Only the front place cannot be 0.")),
    b("So both of them get a 0. Our number is 100.",
      wl("t", "tens: 0    ones: 0"), fig("chart", pchart("100")), a("ans", "100"), ring("ans", "100")),
    b("Careful: 111 looks small, but 100 is smaller, because 0 is a smaller digit than 1. And 999 is the greatest three digit number, not the smallest.",
      w("c1", "100 < 111"), w("c2", "100 < 999")),
    b("Check: go one step below 100 and we reach 99, which has only two digits. So nothing smaller has three.",
      w("k", "100 − 1 = 99")),
    b("So the smallest number with so many digits is always a 1 followed by zeros."),
])

LESSONS[T + "q046"] = finish(T + "q046", [
    b("We need to write the smallest four digit number. Four digits means four places: thousands, hundreds, tens and ones.",
      gl("q", "Smallest four-digit number = ?")),
    b("Let's fill the places from the left. Which digit goes in the thousands place?",
      ask=ch(["1", "0", "9"],
             "A 0 in the thousands place would leave only three real digits. The smallest digit that can stand in front is 1.")),
    b("A 1 in the thousands place. That is the smallest start a four digit number can have.",
      wl("h", "thousands: 1")),
    b("Three places are left. To stay as small as possible, what goes in each of them?",
      ask=ch(["0 in all three", "1 in all three", "0, 0 and then 1"],
             "Any digit bigger than 0 makes the number bigger. And 0 is allowed everywhere except the front. So all three places get a 0.")),
    b("So we have a 1 and three zeros: 1000.",
      fig("chart", pchart("1000")), a("ans", "1000"), ring("ans", "1000")),
    b("Careful: 1001 and 1111 both start the right way, but each one is bigger than 1000. And 9999 is the greatest, at the other end.",
      w("c1", "1000 < 1001"), w("c2", "1000 < 1111"), w("c3", "1000 < 9999")),
    b("Check: one step below 1000 is 999, and that has only three digits. So 1000 really is the first four digit number.",
      w("k", "1000 − 1 = 999")),
    b("So for the smallest number with so many digits: a 1 in front, and 0 in every other place."),
])
