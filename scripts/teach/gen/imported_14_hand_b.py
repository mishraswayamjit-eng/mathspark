"""Batch 14 lessons: numbers formed from given digits, and three profit-and-loss stories.

gs_diff() and middle_digit() each teach two questions that share a structure, computing
every number from the digits. The rest are written beat by beat. In every ask the FIRST
choice is the right one; finish() moves it to a varied position.
"""
from imported_14_lib import a, al, b, ch, finish, fmt, gl, nt, pick, ring, take_apart, ul, w, wl  # noqa: F401

P = "AIGEN_grade5_"
T = "IPMTB_grade5_ch02_"
F = fmt

RAW = {}


def spoken(ds):
    ds = [str(d) for d in ds]
    return ", ".join(ds[:-1]) + " and " + ds[-1]


def listed(ds):
    return ", ".join(str(d) for d in ds)


# ── Greatest minus smallest, four digits ─────────────────────────────────────

def gs_diff(qid, ds, key, ending_trap):
    hi = sorted(ds, reverse=True)
    lo = sorted(ds)
    assert 0 not in ds
    big = int("".join(map(str, hi)))
    small = int("".join(map(str, lo)))
    r = big - small
    assert r == key, (qid, r)
    steps = take_apart(big, small)
    assert len(steps) == 4
    other = [d for d in ds if d not in (hi[0], lo[0])][0]
    RAW[qid] = [
        b("We have four digits: %s. We build the greatest number they can make, then the smallest, and find the difference between the two." % spoken(ds),
          gl("q", "Digits: %s" % listed(ds))),
        b(pick(qid, "ask", ["For the greatest number, which digit should go in the thousands place?",
                            "Start with the greatest number. Which digit do we put first, in the thousands place?"]),
          ask=ch([hi[0], lo[0], other],
                 "The thousands place is worth the most, so it should get the biggest digit. The biggest of %s is %d." % (spoken(ds), hi[0]))),
        b("Biggest digit first, then the next biggest, all the way down: %s. The greatest number is %d." % (listed(hi), big),
          wl("gr", "Greatest = %d" % big)),
        b("For the smallest number we do the opposite. Smallest digit first, then upwards: %s. That makes %d." % (listed(lo), small),
          wl("sm", "Smallest = %d" % small)),
        b("The question wants the difference between them. Which sum is that?",
          ask=ch(["%d − %d" % (big, small), "%d + %d" % (big, small), "%d − %d" % (small, big)],
                 "Difference means subtract, and the smaller number comes off the bigger one. So it is %d minus %d." % (big, small))),
        b("Let's take %d away one place at a time. First the %d, which leaves %d. Then the %d, which leaves %d." % (
            small, steps[0][2], steps[0][3], steps[1][2], steps[1][3]),
          w("d1", steps[0][0]), w("d2", steps[1][0])),
        b("Next the %d, which leaves %d. And last the %d: %d minus %d is %d." % (
            steps[2][2], steps[2][3], steps[3][2], steps[3][1], steps[3][2], r),
          w("d3", steps[2][0]), w("d4", steps[3][0])),
        b("So the difference is %d. %s" % (r, ending_trap),
          a("ans", "%d − %d = %d" % (big, small, r)), ring("ans", str(r))),
        b("Check by adding back: %d plus %d is %d, our greatest number." % (r, small, big),
          w("k", "%d + %d = %d" % (r, small, big))),
        b(pick(qid, "sum", [
            "So: biggest digit first for the greatest number, smallest digit first for the smallest. Then subtract carefully, one place at a time.",
            "So the greatest number runs from the biggest digit down, and the smallest runs from the smallest digit up. Then take one from the other.",
        ])),
    ]


gs_diff(T + "q019", [7, 4, 8, 1], 7263,
        "Careful: adding the two numbers is the slip to watch for. Difference always means subtract.")
gs_diff(T + "q043", [3, 1, 4, 7], 6084,
        "Careful with the 0 in the hundreds place. It has to be written, or the number shrinks to three digits.")


# ── Greatest minus smallest with a zero, then the middle digit ───────────────

def middle_digit(qid, ds, key, lead_wrong):
    hi = sorted(ds, reverse=True)
    lo = sorted(ds)
    assert lo[0] == 0
    first = lo[1]
    lo_order = [first, 0] + lo[2:]
    big = int("".join(map(str, hi)))
    small = int("".join(map(str, lo_order)))
    r = big - small
    rs = str(r)
    assert len(rs) == 5 and int(rs[2]) == key, (qid, r)
    steps = take_apart(big, small)
    assert len(steps) == 4
    wrong_mid = [c for c in (rs[1], rs[3], rs[0]) if c != rs[2]]
    wrong_mid = list(dict.fromkeys(wrong_mid))[:2]
    ans_text = "Middle digit of %s = %s" % (F(r), rs[2])
    RAW[qid] = [
        b("Five digits: %s. We make the greatest number and the smallest number from them, subtract, and then look at the middle digit of the answer." % spoken(ds),
          gl("q", "Digits: %s" % listed(ds))),
        b("For the greatest number, the biggest digit goes first and we work down: %s. That is %s." % (listed(hi), F(big)),
          wl("gr", "Greatest = %s" % F(big))),
        b("For the smallest number, the small digits go first. But which digit can go in the very first place?",
          ask=ch([first, 0, lead_wrong],
                 "0 is the smallest digit, but a number cannot start with 0. If it did, only four digits would count. "
                 "So the first place takes the next smallest digit, %d." % first)),
        b("So %d leads, because a 0 in front would not count. The 0 sits straight after it, and the rest go up in order: %s. The smallest number is %s." % (
            first, listed(lo[2:]), F(small)),
          wl("sm", "Smallest = %s" % F(small)), ul("sm", "0")),
        b("Now subtract, one place at a time. Take off the %s first, which leaves %s. Then the %s, which leaves %s." % (
            F(steps[0][2]), F(steps[0][3]), F(steps[1][2]), F(steps[1][3])),
          w("d1", steps[0][0]), w("d2", steps[1][0])),
        b("Then the %s, which leaves %s. And last the %s: %s minus %s is %s." % (
            F(steps[2][2]), F(steps[2][3]), F(steps[3][2]), F(steps[3][1]), F(steps[3][2]), F(r)),
          w("d3", steps[2][0]), w("d4", steps[3][0]), w("d", "%s − %s = %s" % (F(big), F(small), F(r)))),
        b("Check by adding back: %s plus %s is %s, our greatest number." % (F(r), F(small), F(big)),
          w("k", "%s + %s = %s" % (F(r), F(small), F(big)))),
        b("The answer, %s, has 5 digits. Which one is in the middle?" % F(r),
          ask=ch([rs[2]] + wrong_mid,
                 "With 5 digits, the middle one is the 3rd, because it has 2 digits on each side. Counting along %s, the 3rd digit is %s." % (
                     listed(rs), rs[2]))),
        b("The 3rd digit has two digits on its left and two on its right. So the middle digit is %s." % rs[2],
          al("ans", ans_text), ring("ans", rs[2], ans_text.count(rs[2]))),
        b(pick(qid, "sum", [
            "So: greatest means digits from biggest to smallest. Smallest means smallest to biggest, but never with 0 in front. Then subtract, and read off what was asked.",
            "So remember the 0. It cannot lead the smallest number, so it goes second. Then subtract carefully and pick out the digit the question wants.",
        ])),
    ]


middle_digit(T + "q021", [3, 0, 9, 2, 4], 9, 9)
middle_digit(T + "q048", [1, 5, 0, 9, 7], 9, 5)


# ── Odd or even numbers from given digits ────────────────────────────────────

# Smallest odd number from 3, 0, 4, 8, 7 -> 30,487
RAW[T + "q015"] = [
    b("We have the digits 3, 0, 4, 8 and 7, and two jobs at once: the number must be odd, and it must be as small as possible.",
      gl("q", "Digits: 3, 0, 4, 8, 7    smallest odd number")),
    b("What makes a number odd?",
      ask=ch(["its last digit is odd", "its first digit is odd", "any one digit is odd"],
             "Only the ones digit decides. If the last digit is 1, 3, 5, 7 or 9, the whole number is odd.")),
    b("So the ones place needs an odd digit. Our odd digits are 3 and 7.",
      ul("q", "3"), ul("q", "7")),
    b("For a small number, the first place wants the smallest digit it can have. Which digit goes first?",
      ask=ch(["3", "0", "4"],
             "0 cannot lead, because then the number would really have only four digits. The smallest digit after 0 is 3, so 3 goes first.")),
    b("3 goes in front. That uses up one odd digit, so the other one, 7, must go at the end to keep the number odd.",
      wl("s1", "3 _ _ _ 7")),
    b("The middle places take what is left, 0, 4 and 8, from smallest to biggest. That gives 30,487.",
      a("ans", "30,487"), ring("ans", "30,487")),
    b("Careful: starting with the 0 looks even smaller, but a 0 in front does not count as a digit. And with 3 at the end, a bigger digit would have to lead.",
      wl("t", "with 3 at the end: 40,783"), w("t2", "30,487 < 40,783")),
    b("Check: it ends in 7, so it is odd. It uses 3, 0, 4, 8 and 7 once each. And the digits after the 3 are as small as they can be."),
    b("So fix the two ends first: an odd digit at the end, and the smallest digit that is not 0 in front. Then fill the middle from smallest to biggest."),
]

# Smallest odd number from 1, 2, 4, 0, 6 -> 20,461
RAW[T + "q040"] = [
    b("Our digits are 1, 2, 4, 0 and 6. We want the smallest number they can make that is also odd.",
      gl("q", "Digits: 1, 2, 4, 0, 6    smallest odd number")),
    b("An odd number must end in an odd digit. Which of our digits can go in the ones place?",
      ask=ch(["only 1", "1 or 0", "any of them"],
             "Check each digit. 2, 4, 0 and 6 are all even. The only odd digit we have is 1, so 1 must go last.")),
    b("So 1 is locked into the ones place, even though it is our smallest digit apart from 0 and we would love to put it in front.",
      ul("q", "1"), wl("s1", "_ _ _ _ 1")),
    b("Four digits are left: 2, 4, 0 and 6. Which one goes in the first place?",
      ask=ch(["2", "0", "6"],
             "0 cannot lead a number. So the first place takes the smallest digit that is not 0, and that is 2.")),
    b("2 goes first. Now the 0 can sit right behind it, in the thousands place, where it keeps the number small.",
      wl("s2", "2 0 _ _ 1")),
    b("The last two, 4 and 6, go in order, smaller first. That gives 20,461.",
      a("ans", "20,461"), ring("ans", "20,461")),
    b("Careful: 20,641 looks almost the same, but it has the 6 before the 4. The smaller digit must take the bigger place.",
      w("t", "20,461 < 20,641")),
    b("Check: it ends in 1, so it is odd. It does not start with 0. And after the 2, the digits run 0, 4, 6, from smallest to biggest."),
    b("So lock the odd digit at the end, put the smallest digit that is not 0 in front, then line up the rest from smallest to biggest."),
]

# Greatest even number from 2, 8, 7, 3, 1 -> 87,312
RAW[T + "q016"] = [
    b("Our digits are 2, 8, 7, 3 and 1. We want the greatest number they can make that is also even.",
      gl("q", "Digits: 2, 8, 7, 3, 1    greatest even number")),
    b("An even number ends in an even digit. Our even digits are 2 and 8, so one of them has to go last.",
      ul("q", "2"), ul("q", "8")),
    b("We want the number as big as possible. Which even digit should we give up to the ones place?",
      ask=ch(["2, the smaller one", "8, the bigger one"],
             "The ones place is worth the least. So we spend the smaller even digit there, and save the 8 for the front, where it is worth far more.")),
    b("2 goes last. Careful: putting 8 at the end is the trap, because then the number could only start with 7.",
      wl("s1", "_ _ _ _ 2")),
    b("Now the other four digits: 8, 7, 3 and 1. In what order do they go?",
      ask=ch(["8, 7, 3, 1", "1, 3, 7, 8", "7, 8, 3, 1"],
             "For the greatest number, the biggest digit takes the biggest place. So they go from biggest to smallest: 8, 7, 3, 1.")),
    b("Biggest first: 8, 7, 3, 1, and then the 2 at the end. Our number is 87,312.",
      a("ans", "87,312"), ring("ans", "87,312")),
    b("Let's test the other way. With 8 at the end, the best we could make is 73,218. That is smaller, so 87,312 wins.",
      wl("o", "with 8 at the end: 73,218"), w("cmp", "87,312 > 73,218")),
    b("One more trap: 87,321 is bigger still, but it ends in 1, so it is odd and not allowed.",
      wl("odd", "87,321 ends in 1: odd")),
    b("So for the greatest even number, put the smallest even digit at the end, then line up all the others from biggest to smallest."),
]

# Greatest odd number from 7, 0, 3, 2, 6 -> 76,203
RAW[T + "q017"] = [
    b("Our digits are 7, 0, 3, 2 and 6. We want the greatest number they can make that is also odd.",
      gl("q", "Digits: 7, 0, 3, 2, 6    greatest odd number")),
    b("An odd number ends in an odd digit. Which of our digits are odd?",
      ask=ch(["7 and 3", "7, 3 and 0", "only 7"],
             "Odd digits are 1, 3, 5, 7 and 9. From our list that is 7 and 3. The 0, the 2 and the 6 are even.")),
    b("7 and 3 are odd, so one of them must sit in the ones place.",
      ul("q", "7"), ul("q", "3")),
    b("Which one do we put at the end, to keep the number as big as possible?",
      ask=ch(["3", "7"],
             "7 is our biggest digit, so it is worth the most in the front place. We spend the smaller odd digit, 3, on the ones place.")),
    b("3 goes last, and that saves the 7 for the front.",
      wl("s1", "_ _ _ _ 3")),
    b("The rest go from biggest to smallest: 7, 6, 2, 0. So the number is 76,203.",
      a("ans", "76,203"), ring("ans", "76,203")),
    b("Careful: 76,320 is the greatest number these digits can make, but it ends in 0, so it is even. Moving the 3 to the end is what makes it odd.",
      w("t", "76,320 > 76,203")),
    b("Check the other choice too. With 7 at the end, the best we could make is 63,207, and that is smaller.",
      wl("o", "with 7 at the end: 63,207"), w("cmp", "76,203 > 63,207")),
    b("So for the greatest odd number, put the smallest odd digit at the end, then line up the others from biggest to smallest."),
]

# Smallest even number using every one-digit prime once -> 3572
RAW[T + "q020"] = [
    b("First we need the one digit prime numbers. A prime number has exactly two factors, 1 and itself.",
      gl("q", "One-digit primes, each once: smallest even number")),
    b("Which are the one digit primes?",
      ask=ch(["2, 3, 5, 7", "1, 3, 5, 7", "2, 3, 5, 7, 9"],
             "1 is not prime, because it has only one factor. 9 is not prime, because 3 times 3 is 9. That leaves 2, 3, 5 and 7.")),
    b("2, 3, 5 and 7. Those are our four digits.",
      wl("d", "Digits: 2, 3, 5, 7")),
    b("The number must be even. Which digit has to go in the ones place?",
      ask=ch(["2", "7", "3"],
             "An even number ends in an even digit. Of 2, 3, 5 and 7, only 2 is even. So 2 must go last.")),
    b("2 is the only even one, so it goes last. Careful: the smallest arrangement of all, 2357, ends in 7, so it is odd and will not do.",
      ul("d", "2"), wl("odd", "2357 ends in 7: odd"), wl("s1", "_ _ _ 2")),
    b("The other three, 3, 5 and 7, fill the front from smallest to biggest. That gives 3572.",
      a("ans", "3572"), ring("ans", "3572")),
    b("Check: 3572 ends in 2, so it is even. It uses 2, 3, 5 and 7 once each. And no digit smaller than 3 was free for the front."),
    b("So list the digits, lock the even digit at the end, then arrange the rest from smallest to biggest."),
]

# Smallest odd number using every one-digit prime -> 2357
RAW[T + "q044"] = [
    b("We need the one digit prime numbers first. Then we make the smallest odd number that uses all of them.",
      gl("q", "All one-digit primes: smallest odd number")),
    b("Let's begin with a tricky one. Is 1 a prime number?",
      ask=ch(["No", "Yes"],
             "A prime number has exactly two different factors. 1 has only one factor, itself, so it is not prime.")),
    b("So the one digit primes are 2, 3, 5 and 7. Not 1, and not 9, because 3 times 3 is 9.",
      wl("d", "Digits: 2, 3, 5, 7")),
    b("For the smallest number, the smallest digit takes the biggest place, and we work upwards: 2, 3, 5, 7. That makes 2357.",
      w("s", "2357")),
    b("But the number must be odd. Is 2357 odd?",
      ask=ch(["Yes, it ends in 7", "No, it starts with 2"],
             "Only the last digit decides odd or even. 2357 ends in 7, and 7 is odd, so the whole number is odd.")),
    b("It ends in 7, so it is odd already. The smallest arrangement passes the test, and nothing needs to move.",
      ul("s", "7"), al("ans", "Smallest odd number = 2357"), ring("ans", "2357")),
    b("Careful: the 2 in front does not make the number even. Odd or even is decided by the ones place alone."),
    b("Check: any other order, such as 3527, starts with a bigger digit, so it is a bigger number.",
      w("c", "2357 < 3527")),
    b("So make the smallest number first, then test the condition. If it already passes, you are done."),
]

# Smallest odd number divisible by 5 from the first three one-digit primes -> 235
RAW[T + "q047"] = [
    b("Three things to sort out here: which digits we may use, what divisible by 5 tells us, and how to keep the number small.",
      gl("q", "First three one-digit primes: odd, divisible by 5")),
    b("What are the first three one digit prime numbers?",
      ask=ch(["2, 3, 5", "1, 2, 3", "3, 5, 7"],
             "1 is not prime, so the primes start at 2. Counting up, the first three are 2, 3 and 5.")),
    b("2, 3 and 5. Careful: 1 is not a prime, and 7 is the fourth prime, so neither of them is allowed.",
      wl("d", "Digits: 2, 3, 5")),
    b("A number that divides exactly by 5 ends in 0 or 5. So which of our digits goes in the ones place?",
      ask=ch(["5", "2", "3"],
             "We have no 0. So the only way to end in 0 or 5 is to put the 5 last.")),
    b("5 goes last. And a number ending in 5 is odd as well, so both conditions are taken care of at once.",
      ul("d", "5"), wl("s1", "_ _ 5")),
    b("Now make it small. Of 2 and 3, the smaller one goes in the hundreds place. That gives 235.",
      a("ans", "235"), ring("ans", "235")),
    b("Check: 235 divided by 5 is 47, with nothing left over. It ends in 5, so it is odd. And it uses 2, 3 and 5 once each.",
      w("k", "235 ÷ 5 = 47")),
    b("The other order, 325, passes the tests too, but it is bigger. We were asked for the smallest.",
      w("c", "235 < 325")),
    b("So let the conditions fix the last digit first. Then arrange the remaining digits from smallest to biggest."),
]


# ── Profit and loss ──────────────────────────────────────────────────────────

# Meera: cost 250 + 50; 60 samosas, 10 unsold, 8 rupees each -> profit of 33⅓%
RAW[P + "00942e8a-69f6-4e0d-bdd7-4b962326513b"] = [
    b("Meera spends 250 rupees on ingredients and 50 rupees on plates. She makes 60 samosas to sell at 8 rupees each, but 10 are left over and given away. We want her profit or loss as a percentage of her cost.",
      gl("q", "Cost ₹250 + ₹50; 60 made, 10 unsold, ₹8 each")),
    b("Start with the cost. 250 plus 50 is 300 rupees.",
      w("cp", "250 + 50 = 300"), nt("cp", "300", "total cost", "below")),
    b("Now the money that comes in. How many samosas actually earn her money?",
      ask=ch(["50", "60", "10"],
             "The 10 given away bring in nothing. Only the ones she sells count, and that is 60 minus 10, which is 50.")),
    b("60 minus 10 is 50 sold. At 8 rupees each, 50 times 8 is 400 rupees.",
      w("n", "60 − 10 = 50"), w("sp", "50 × 8 = 400")),
    b("She took in 400 and spent 300, so she made a profit. 400 minus 300 is 100 rupees.",
      w("pr", "400 − 300 = 100")),
    b("For the percentage, we compare the profit with something. With what?",
      ask=ch(["the cost, 300", "the money taken in, 400", "the 60 samosas"],
             "The question says percentage on the total cost. So the profit, 100, is compared with the cost, 300.")),
    b("100 out of 300 is the fraction 100 over 300, and that is one third.",
      w("f", "100/300 = 1/3")),
    b("One third as a percentage is one third of 100. 100 divided by 3 is 33 and a third. So her profit is 33 and a third percent.",
      w("pc", "100 ÷ 3 = 33 + 1/3"), al("ans", "Profit = 33⅓%"), ring("ans", "33⅓%")),
    b("Careful: counting all 60 samosas would give 480 rupees and a much bigger profit. But the 10 unsold ones earned nothing.",
      w("t", "60 × 8 = 480")),
    b("Check: one third of the cost, 300, is 100. And 100 rupees is exactly her profit.",
      w("k", "300 ÷ 3 = 100")),
    b("So: find the total cost, then the money from what was really sold, then the difference. Last, put that difference over the cost to get the percentage."),
]

# Priya's uncle: costs 120 + 230 + 150; 200 samosas, 20 free, 5 rupees each -> profit 400
RAW[P + "017769ba-51ca-44c3-ab61-9531a2549540"] = [
    b("Priya's uncle spends 120 rupees on potatoes, 230 on spices and flour, and 150 on oil. He makes 200 samosas, gives 20 away as samples, and sells the rest at 5 rupees each. What is his profit?",
      gl("q", "Costs ₹120, ₹230, ₹150; 200 made, 20 free, ₹5 each")),
    b("First the total cost. 120 plus 230 is 350, and 150 more makes 500 rupees.",
      w("c1", "120 + 230 = 350"), w("c2", "350 + 150 = 500")),
    b("How many samosas does he actually sell?",
      ask=ch(["180", "200", "220"],
             "The 20 samples are given away free, so they come off the 200. 200 minus 20 is 180.")),
    b("200 minus 20 is 180. The free samples cost him money to make, but they bring none in.",
      w("n", "200 − 20 = 180")),
    b("Each one sells for 5 rupees. For 180 times 5, split the 180: 100 fives are 500, and 80 fives are 400. Together that is 900 rupees.",
      w("s1", "100 × 5 = 500"), w("s2", "80 × 5 = 400"), w("sp", "180 × 5 = 900")),
    b("He took in 900 rupees and spent 500. How do we find the profit?",
      ask=ch(["900 − 500", "900 + 500", "it is the whole 900"],
             "Profit is what is left after the costs are paid back. So we take the cost away from the money taken in: 900 minus 500.")),
    b("900 minus 500 is 400. His profit is 400 rupees.",
      a("ans", "900 − 500 = 400"), ring("ans", "400")),
    b("Careful: 900 is the money he collected, not his profit. And selling all 200 would have brought in 1000, but 20 of them were never sold.",
      w("t", "200 × 5 = 1000")),
    b("Check: cost plus profit should give the money taken in. 500 plus 400 is 900. It fits.",
      w("k", "500 + 400 = 900")),
    b("So in a profit story: add up every cost, count only what was really sold, then take the cost away from the money that came in."),
]

# Priya's father: 8 kg at 800, 12 kg at 300, 600, 200; 40 boxes at 350, 5 unsold -> profit 1450
RAW[P + "0937e6f4-93a6-47f5-bc0b-2e01667f95e8"] = [
    b("Priya's father buys 8 kilograms of kaju katli at 800 rupees a kilogram, and 12 kilograms of gulab jamun at 300. He spends 600 on boxes and 200 on ribbons. He makes 40 gift boxes to sell at 350 rupees each, and 5 stay unsold.",
      gl("q", "8 kg × ₹800, 12 kg × ₹300, ₹600, ₹200; 40 boxes, 5 unsold")),
    b("A long story, so we take it in parts. First the sweets. 8 times 800 is 6400, and 12 times 300 is 3600.",
      w("k1", "8 × 800 = 6400"), w("k2", "12 × 300 = 3600")),
    b("Now add the boxes and the ribbons. 6400 plus 3600 is 10,000, and 600 plus 200 is 800. So the total cost is 10,800 rupees.",
      w("t1", "6400 + 3600 = 10,000"), w("t2", "600 + 200 = 800"), w("t3", "10,000 + 800 = 10,800")),
    b("Now the money coming in. How many boxes does he get paid for?",
      ask=ch(["35", "40", "45"],
             "He made 40 boxes, but 5 were given away as gifts. Only sold boxes bring in money, and 40 minus 5 is 35.")),
    b("40 minus 5 is 35 boxes sold, at 350 rupees each.",
      w("n", "40 − 5 = 35")),
    b("For 35 times 350, split the 35. 30 times 350 is 10,500, and 5 times 350 is 1750. Together that is 12,250 rupees.",
      w("s1", "30 × 350 = 10,500"), w("s2", "5 × 350 = 1750"), w("sp", "10,500 + 1750 = 12,250")),
    b("He took in 12,250 and spent 10,800. Is that a profit or a loss?",
      ask=ch(["a profit", "a loss"],
             "Compare the two amounts. He took in more than he spent, so money is left over. That is a profit.")),
    b("More came in than went out, so it is a profit. 12,250 minus 10,800 is 1450 rupees.",
      a("ans", "12,250 − 10,800 = 1450"), ring("ans", "1450")),
    b("Careful: counting all 40 boxes is the classic slip here. The 5 gift boxes cost money to fill, but they earned nothing."),
    b("Check: cost plus profit should equal the money taken in. 10,800 plus 1450 is 12,250. It fits.",
      w("k", "10,800 + 1450 = 12,250")),
    b("So in a profit story: add up every cost, count only what was really sold, then compare the two totals."),
]

LESSONS = {qid: finish(qid, beats) for qid, beats in RAW.items()}
