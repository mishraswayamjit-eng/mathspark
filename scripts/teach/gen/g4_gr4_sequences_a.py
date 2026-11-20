"""gr4_sequences lessons written one by one: the past-paper questions EXT_G4_FP_...

far_term() is a shared skeleton for "find a term far along a steady pattern"; each
question that uses it supplies its own opening, its own trap line and its own ending.
"""
from g4_gr4_sequences_lib import ans, b, ch, g, jumps, lab, mk, nt, ordinal, w

L = {}


def far_term(terms, n, word, open_say, near_miss, end_say, down=False):
    a, last = terms[0], terms[-1]
    d = abs(terms[1] - terms[0])
    m = n - 1
    total = m * d
    result = a - total if down else a + total
    nth = ordinal(n)
    sign = "−" if down else "+"
    k = len(terms)
    if down:
        jump_say = "First find the jump. %d minus %d is %d, and %d minus %d is %d too. So each %s is %d less than the one before." % (
            terms[0], terms[1], d, terms[1], terms[2], d, word, d)
        lines = [w("l2", "%d − %d = %d" % (terms[0], terms[1], d)), w("l3", "%d − %d = %d" % (terms[1], terms[2], d))]
    else:
        jump_say = "First find the jump. %d minus %d is %d, and %d minus %d is %d too. So each %s is %d more than the one before." % (
            terms[1], terms[0], d, terms[2], terms[1], d, word, d)
        lines = [w("l2", "%d − %d = %d" % (terms[1], terms[0], d)), w("l3", "%d − %d = %d" % (terms[2], terms[1], d))]
    beats = [
        b(open_say, g("l1", ", ".join(str(t) for t in terms) + ", ...", True), g("l1b", "%s %s = ?" % (nth, word), True)),
        b(jump_say, lines, jumps("l1", ["%s%d" % (sign, d)] * (k - 1))),
        b("We could keep going one step at a time, but that is slow. From the 1st %s to the %s, how many jumps do we make?" % (word, nth),
          ask=ch(str(m), [str(n), str(n + 1)],
                 "From the 1st to the 2nd is 1 jump. From the 1st to the 3rd is 2 jumps. The jumps are always 1 fewer than the place number.")),
        b("Careful, this is the trap. The 1st %s is there before any jump. So we make 1 fewer jump than %d. That is %d jumps." % (word, n, m),
          w("l4", "%d − 1 = %d" % (n, m)), lab("l4b", "%d jumps of %d" % (m, d))),
    ]
    tens, ones = (m // 10) * 10, m % 10
    if m > 12 and ones:
        p1, p2 = tens * d, ones * d
        beats.append(b("%d jumps of %d is a big sum, so split it. %d times %d is %d, and %d times %d is %d." % (m, d, tens, d, p1, ones, d, p2),
                       w("l5", "%d × %d = %d" % (tens, d, p1)), w("l6", "%d × %d = %d" % (ones, d, p2))))
        beats.append(b("%d plus %d makes %d. So %d jumps of %d cover %d." % (p1, p2, total, m, d, total),
                       w("l7", "%d × %d = %d" % (m, d, total))))
    else:
        beats.append(b("%d jumps of %d. %d times %d is %d." % (m, d, m, d, total), w("l7", "%d × %d = %d" % (m, d, total))))
    if down:
        beats.append(b("The jumps cover %d. The numbers are going down, so what do we do with the %d?" % (total, total),
                       ask=ch("take it away from %d" % a, ["add it to %d" % a, "take it away from %d" % last],
                              "The jumps start at the 1st %s, %d, and they go down. So we take the %d away from %d." % (word, a, total, a))))
        beats.append(b("%d take away %d is %d. So the %s %s is %d. %s" % (a, total, result, nth, word, result, near_miss),
                       ans("l8", "%d − %d = %d" % (a, total, result), str(result))))
    else:
        beats.append(b("The jumps cover %d. What do we do with the %d?" % (total, total),
                       ask=ch("add it to the 1st %s, %d" % (word, a), ["nothing, %d is the answer" % total, "add it to %d" % last],
                              "The jumps start at the 1st %s, which is %d. So the %d is added on to %d." % (word, a, total, a))))
        beats.append(b("%d plus %d is %d. So the %s %s is %d. %s" % (a, total, result, nth, word, result, near_miss),
                       ans("l8", "%d + %d = %d" % (a, total, result), str(result))))
    part = (k - 1) * d
    beats.append(b("Test the idea on the %s %s, which we can see. %d jumps of %d make %d, and %d %s %d is %d. It matches." % (
        ordinal(k), word, k - 1, d, part, a, "take away" if down else "plus", part, last),
        w("l9", "%d × %d = %d" % (k - 1, d, part)), w("l10", "%d %s %d = %d" % (a, sign, part, last))))
    beats.append(b(end_say))
    for beat in beats:
        beat["say"] = beat["say"].strip()
    return beats


# ── EXT_G4_FP_2020_003 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2020_003"] = [
    b("Here is our series: 64, 81, 100, 121, and it keeps going. One of the four choices does not belong to it. Let's find the odd one out.",
      g("l1", "64, 81, 100, 121, ...", True)),
    b("First we need the rule. What kind of numbers are these? Think about 8 times 8.",
      ask=ch("a number times itself", ["numbers that go up by 17", "even numbers"],
             "Look again. 8 times 8 is 64, and 9 times 9 is 81. Each one is a number multiplied by itself.")),
    b("8 times 8 is 64. 9 times 9 is 81. Then 10 times 10, and 11 times 11. These are the square numbers, in order.",
      w("l2", "8 × 8 = 64"), w("l3", "9 × 9 = 81"), w("l4", "10 × 10 = 100"), w("l5", "11 × 11 = 121")),
    b("So a number belongs only if it is some number times itself. Let's test the choices. 13 times 13 is 169, and 15 times 15 is 225.",
      w("l6", "13 × 13 = 169"), w("l7", "15 × 15 = 225")),
    b("17 times 17 is 289. So those three all belong. That leaves 176, but let's prove it.",
      w("l8", "17 × 17 = 289"), lab("l8b", "Is 176 a square number?")),
    b("176 is a little more than 169, which is 13 times 13. What is the very next square number after that?",
      ask=ch("14 × 14 = 196", ["14 × 14 = 176", "13 × 14 = 182"],
             "The next square after 13 times 13 is 14 times 14, and that is 196.")),
    b("13 times 13 is 169 and 14 times 14 is 196. 176 sits between them, and there is no whole number between 13 and 14. So 176 is not a square.",
      w("l9", "14 × 14 = 196"), w("l10", "169 < 176 < 196"), mk("l10", "176", "box")),
    b("So the number that is not in the series is 176.", ans("l11", "176")),
    b("When a list looks odd, ask what family the numbers belong to. Then test each choice against that family."),
]


# ── EXT_G4_FP_2021_013 and PYQ_2017_Q37 (the same series) ────────────────────
def tenth_of_24(v):
    return [
        b(["Our series starts 24, 39, 53, 66, 78. We want the 10th term, so first we must find the rule.",
           "Here is a series: 24, 39, 53, 66, 78, and on it goes. Which number will be 10th? Let's find the rule first."][v],
          g("l1", "24, 39, 53, 66, 78, ...", True), g("l1b", "10th term = ?", True)),
        b("Look at the jumps between neighbours. They are 15, then 14, then 13, then 12.",
          jumps("l1", ["+15", "+14", "+13", "+12"])),
        b("The jumps are not the same. So what is happening to them?",
          ask=ch("each jump is 1 smaller", ["each jump is 1 bigger", "they stay the same"],
                 "Read the jumps again: 15, 14, 13, 12. Each one is 1 less than the one before.")),
        b("So the next jumps are 11, 10, 9, 8 and 7. Count carefully: 78 is the 5th term, so we need 5 more jumps to reach the 10th.",
          lab("l2", "next jumps: 11, 10, 9, 8, 7"), nt("l1", "78", "5th", "above")),
        b("The 6th term is 78 plus 11, which is 89. The 7th is 89 plus 10, which is 99.",
          w("l3", "78 + 11 = 89"), nt("l3", "89", "6th"), w("l4", "89 + 10 = 99"), nt("l4", "99", "7th")),
        b("The 8th is 99 plus 9, which is 108. Don't stop there! The 9th is 108 plus 8, which is 116.",
          w("l5", "99 + 9 = 108"), nt("l5", "108", "8th"), w("l6", "108 + 8 = 116"), nt("l6", "116", "9th")),
        b("One jump is left. Which jump takes us from the 9th term to the 10th?",
          ask=ch("7", ["8", "12"],
                 "The jumps we listed were 11, 10, 9, 8 and 7. We have used four of them, so the last one is 7.")),
        b("116 plus 7 is 123. So the 10th term is 123.", ans("l7", "116 + 7 = 123", "123")),
        b(["When the jumps change, find how they change. Then walk forward one term at a time, and keep count of which term you are on.",
           "So the plan is: find the pattern in the jumps, then step forward, naming each term as you go, until you reach the one you want."][v]),
    ]


L["EXT_G4_FP_2021_013"] = tenth_of_24(0)


# ── EXT_G4_FP_2021_027 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2021_027"] = [
    b("We must add the odd numbers 1, 3, 5, 7, all the way up to 27. And look, the choices are written as squares. That is a clue.",
      g("l1", "1 + 3 + 5 + 7 + ... + 27 = ?", True)),
    b("Let's start small and hunt for a pattern. 1 plus 3 is 4. And 4 is 2 times 2.",
      w("l2", "1 + 3 = 4"), w("l3", "4 = 2 × 2")),
    b("Now three odd numbers. 1 plus 3 plus 5 is 9. And 9 is 3 times 3.",
      w("l4", "1 + 3 + 5 = 9"), w("l5", "9 = 3 × 3")),
    b("Two odd numbers gave 2 times 2. Three gave 3 times 3. What will the first four odd numbers add up to?",
      ask=ch("4 × 4 = 16", ["4 × 3 = 12", "7 × 7 = 49"],
             "Follow the pattern. Two numbers gave 2 times 2, and three gave 3 times 3. So four give 4 times 4, which is 16.")),
    b("Yes: 1 plus 3 plus 5 plus 7 is 16. So the sum is always the count of odd numbers, multiplied by itself.",
      w("l6", "1 + 3 + 5 + 7 = 16"), lab("l7", "Sum = count × count")),
    b("So all we need is the count. Careful, this is the trap: the count is not 27. How many odd numbers are there from 1 to 27?",
      ask=ch("14", ["13", "27"],
             "Odd and even numbers take turns. Up to 27 there are 14 odd numbers and 13 even ones.")),
    b("Here is a quick way to count them. Add 1 to the last odd number, then halve. 27 plus 1 is 28, and half of 28 is 14.",
      w("l8", "27 + 1 = 28"), w("l9", "28 ÷ 2 = 14")),
    b("There are 14 odd numbers, so the sum is 14 times 14. That is 14 squared.",
      ans("l10", "Sum = 14 × 14 = (14)²", "(14)²", True)),
    b("Remember this lovely fact. Add up the odd numbers starting from 1, and you always get the count times itself."),
]


# ── EXT_G4_FP_2021_030 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2021_030"] = [
    b("We are walking backwards from 726, stepping only on odd numbers. We want the 59th one we land on.",
      g("l1", "59th odd number before 726 = ?", True)),
    b("Let's begin at the beginning. What is the 1st odd number before 726?",
      ask=ch("725", ["724", "727"],
             "Before means smaller. One step down from 726 is 725, and 725 is odd.")),
    b("So 725 is the 1st. Then 723 is the 2nd, and 721 is the 3rd. Each jump back is 2.",
      lab("l2", "1st: 725"), lab("l3", "2nd: 723"), lab("l4", "3rd: 721")),
    b("From the 1st odd number to the 59th, how many jumps of 2 do we make?",
      ask=ch("58", ["59", "60"],
             "From the 1st to the 2nd is 1 jump. From the 1st to the 3rd is 2 jumps. So to the 59th it is 1 fewer than 59.")),
    b("That is the trap. 725 is already the 1st, so we need only 58 jumps. And 58 jumps of 2 make 116.",
      w("l5", "59 − 1 = 58"), w("l6", "58 × 2 = 116")),
    b("Now go back 116 from 725. Take away 100 to get 625. Then take away 16 more to get 609.",
      w("l7", "725 − 100 = 625"), w("l8", "625 − 16 = 609")),
    b("So the 59th odd number before 726 is 609.", ans("l9", "725 − 116 = 609", "609")),
    b("Quick check. 609 ends in 9, so it is odd, just as it must be. An even answer could never be right here."),
    b("When you count along a list, the jumps are always 1 fewer than the place number. Keep that in your pocket."),
]


# ── EXT_G4_FP_2022_014 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2022_014"] = [
    b("This one has three small jobs hidden inside. Find the greatest 2-digit prime. Find two even numbers after it. Then add them.",
      g("l1", "7th + 11th even numbers after the greatest 2-digit prime", True)),
    b("A prime number has no factors except 1 and itself. Which is the greatest 2-digit prime?",
      ask=ch("97", ["99", "98"],
             "99 is 9 times 11, and 98 is even. So neither is prime. 97 has no factors like that.")),
    b("99 is 9 times 11. 98 is even, so 2 goes into it. That makes 97 the greatest 2-digit prime.",
      w("l2", "99 = 9 × 11"), w("l3", "98 = 2 × 49"), lab("l4", "97 is prime")),
    b("The 1st even number after 97 is 98. The 2nd is 100. Each jump is 2.",
      lab("l5", "1st even: 98"), lab("l6", "2nd even: 100")),
    b("From the 1st even number to the 7th, how many jumps of 2 do we make?",
      ask=ch("6", ["7", "8"],
             "The 1st one needs no jump at all. So to reach the 7th we make 6 jumps.")),
    b("6 jumps of 2 make 12, and 98 plus 12 is 110. So the 7th even number is 110.",
      w("l7", "6 × 2 = 12"), w("l8", "98 + 12 = 110")),
    b("For the 11th we make 10 jumps. 10 twos are 20, and 98 plus 20 is 118.",
      w("l9", "10 × 2 = 20"), w("l10", "98 + 20 = 118")),
    b("Now add the two numbers. 110 plus 118 is 228.", w("l11", "110 + 118 = 228")),
    b("Look at the choices. 228 is not there! Don't bend your working to fit a choice. When your careful answer is not listed, pick none of these.",
      ans("l12", "228 is not listed: None of these", "None of these", True)),
    b("Break a long question into small jobs and do them one at a time. And trust your careful working."),
]


# ── EXT_G4_FP_2022_017 and EXT_G4_FP_2025_017 (drops that grow by 5) ─────────
L["EXT_G4_FP_2022_017"] = [
    b("Our series is 122, 117, 107, 92, 72, and then a letter A. A stands for the next number, and we must find it.",
      g("l1", "122, 117, 107, 92, 72, A", True)),
    b("The numbers are getting smaller. Let's see how much they drop each time. The drops are 5, then 10, then 15, then 20.",
      jumps("l1", ["−5", "−10", "−15", "−20"])),
    b("The drops are not the same. So what is the next drop?",
      ask=ch("25", ["20", "30"],
             "Look at the drops: 5, 10, 15, 20. Each drop is 5 bigger than the last. So after 20 comes 25.")),
    b("The drops grow by 5 each time, so the next drop is 25. This is the trap: don't just take away 20 again.",
      nt("l1", ",", "−25", "below", 5)),
    b("72 take away 25. First take away 20 to get 52. Then take away 5 more to get 47.",
      w("l2", "72 − 20 = 52"), w("l3", "52 − 5 = 47")),
    b("So A is 47.", ans("l4", "72 − 25 = 47", "47")),
    b("Check the whole chain of drops: 5, 10, 15, 20, 25. It grows steadily, so 47 fits."),
    b("When the jumps are not all the same, look at the jumps themselves. They often have a little pattern of their own."),
]

L["EXT_G4_FP_2025_017"] = [
    b("Here is the series: 90, 85, 75, 60, 40, and then a question mark. Let's find the number that belongs there.",
      g("l1", "90, 85, 75, 60, 40, ?", True)),
    b("The numbers go down. From 90 to 85 is a drop of 5. From 85 to 75 is a drop of 10. Then 15, then 20.",
      jumps("l1", ["−5", "−10", "−15", "−20"])),
    b("Look at those drops: 5, 10, 15, 20. What will the next drop be?",
      ask=ch("25", ["20", "30"],
             "Each drop is 5 more than the one before. After 20 comes 25.")),
    b("Careful here. It is tempting to take away 20 again, but the drops keep growing by 5. The next drop is 25.",
      nt("l1", ",", "−25", "below", 5)),
    b("40 take away 25. Take away 20 first to get 20. Then take away 5 more to get 15.",
      w("l2", "40 − 20 = 20"), w("l3", "20 − 5 = 15")),
    b("So the missing number is 15.", ans("l4", "40 − 25 = 15", "15"), mk("l1", "?", "box")),
    b("Check: the drops now read 5, 10, 15, 20, 25. Every drop is 5 bigger than the last, so 15 fits."),
    b("So the plan is: find the drops, spot how the drops change, then make the next drop from the last number."),
]


# ── EXT_G4_FP_2022_030 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2022_030"] = [
    b("Our series starts 13, 15, 18, 23, 30, 41. We want the 12th term. First, the rule.",
      g("l1", "13, 15, 18, 23, 30, 41, ...", True), g("l1b", "12th term = ?", True)),
    b("Look at the jumps between neighbours. They are 2, 3, 5, 7 and 11.",
      jumps("l1", ["+2", "+3", "+5", "+7", "+11"])),
    b("Those jumps belong to a famous family of numbers. Which one?",
      ask=ch("prime numbers", ["odd numbers", "numbers that go up by 2"],
             "They are not the odd numbers, because 2 is there and 9 is missing. 2, 3, 5, 7, 11 are the prime numbers in order.")),
    b("So each jump is the next prime. Now the trap: to go from the 1st term to the 12th we make 11 jumps, not 12.",
      w("l2", "12 − 1 = 11")),
    b("So we need the first 11 primes. After 11 come 13, 17, 19, 23, 29 and 31.",
      lab("l3", "2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31")),
    b("Let's add them in friendly groups. The first five make 28. Then 13 and 17 make 30.",
      w("l4", "2 + 3 + 5 + 7 + 11 = 28"), w("l5", "13 + 17 = 30")),
    b("19 and 23 make 42. 29 and 31 make 60. All together, 28 plus 30 plus 42 plus 60 is 160.",
      w("l6", "19 + 23 = 42"), w("l7", "29 + 31 = 60"), w("l8", "28 + 30 + 42 + 60 = 160")),
    b("The 11 jumps add up to 160. Where do we add them on?",
      ask=ch("to the 1st term, 13", ["to the last term shown, 41", "nowhere, 160 is the answer"],
             "All 11 jumps were counted from the very start. So they are added to the 1st term, 13.")),
    b("13 plus 160 is 173. So the 12th term is 173.", ans("l9", "13 + 160 = 173", "173")),
    b("When jumps look strange, ask which family they belong to. And remember: reaching the 12th term takes only 11 jumps."),
]


# ── EXT_G4_FP_2023_003 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2023_003"] = [
    b("W is a mystery number. We are told that W plus 9 is odd, and we want the 48th even number after it.",
      g("l1", "W + 9 is odd", True), g("l1b", "48th even number after it = ?", True)),
    b("If W plus 9 is odd, what kind of number is the very next one, W plus 10?",
      ask=ch("even", ["odd", "we cannot tell"],
             "Odd and even numbers take turns. Straight after an odd number comes an even one.")),
    b("So W plus 10 is the 1st even number after it. The 2nd is W plus 12. Each jump is 2.",
      lab("l2", "1st even: W + 10"), lab("l3", "2nd even: W + 12")),
    b("From the 1st even number to the 48th, how many jumps of 2 do we make?",
      ask=ch("47", ["48", "49"],
             "The 1st one needs no jump. From the 1st to the 2nd is 1 jump, to the 3rd is 2 jumps. So to the 48th it is 47.")),
    b("This is the trap. W plus 10 is already the 1st, so we make only 47 jumps. 47 twos are 94.",
      w("l4", "48 − 1 = 47"), w("l5", "47 × 2 = 94")),
    b("We started at W plus 10 and moved 94 further on. 10 plus 94 is 104.", w("l6", "10 + 94 = 104")),
    b("So the 48th even number is W plus 104.", ans("l7", "W + 104", None, True)),
    b("Quick check. W plus 10 is even, and we added 94, which is even. Even plus even stays even. Good."),
    b("Even with a letter in it, the idea is the same. Find the 1st one, count 1 fewer jump than the place number, and step on."),
]


# ── EXT_G4_FP_2024_002 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2024_002"] = [
    b("Here x is a mystery number, and x plus 9 is a 2-digit prime. We want the 12th even number after it.",
      g("l1", "x + 9 is a 2-digit prime", True), g("l1b", "12th even number after it = ?", True)),
    b("We don't know which prime it is. But we can still say something. Is a 2-digit prime odd or even?",
      ask=ch("always odd", ["always even", "it can be either"],
             "An even number has 2 as a factor. The only even prime is 2 itself, and that has just 1 digit.")),
    b("So x plus 9 is odd. That makes x plus 10 the 1st even number after it, and x plus 12 the 2nd. Each jump is 2.",
      lab("l2", "1st even: x + 10"), lab("l3", "2nd even: x + 12")),
    b("From the 1st even number to the 12th, how many jumps of 2 do we make?",
      ask=ch("11", ["12", "13"],
             "The 1st one needs no jump. So the jumps are 1 fewer than 12, which is 11.")),
    b("Careful, that is the trap. x plus 10 is already the 1st, so we make 11 jumps. 11 twos are 22.",
      w("l4", "12 − 1 = 11"), w("l5", "11 × 2 = 22")),
    b("We started at x plus 10 and moved 22 further on. 10 plus 22 is 32.", w("l6", "10 + 22 = 32")),
    b("So the 12th even number is x plus 32.", ans("l7", "x + 32", None, True)),
    b("Quick check. x plus 10 is even, and 22 is even. Even plus even stays even, so x plus 32 is an even number. Good."),
    b("So the plan is: find the 1st even number, count 1 fewer jump than the place number, and step on in 2s."),
]


# ── Terms far along a steady pattern ─────────────────────────────────────────
L["EXT_G4_FP_2023_015"] = far_term(
    [24, 41, 58, 75, 92], 28, "term",
    "Our series starts 24, 41, 58, 75, 92, and keeps going. We want the 28th term. That is a long way along!",
    "",
    "For a term far along: find the jump, make 1 fewer jump than the term number, multiply, then add the 1st term.")

L["EXT_G4_FP_2024_007"] = far_term(
    [7, 10, 13, 16, 19], 11, "number",
    "The series goes 7, 10, 13, 16, 19, and on. We want the 11th number in it.",
    "",
    "So remember: the 11th number is only 10 jumps from the 1st. Count the jumps, not the numbers.")

L["EXT_G4_FP_2025_037"] = far_term(
    [12, 19, 26, 33, 40], 38, "term",
    "This series begins 12, 19, 26, 33, 40. We need its 38th term, far too far to count one by one.",
    "",
    "Find the jump, count 1 fewer jump than the term number, multiply, and add the 1st term. That works for any steady pattern.")


# ── EXT_G4_FP_2024_039 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2024_039"] = [
    b("The series starts 12, 23, 33, 42, 50. We want the 9th number, so first we need the rule.",
      g("l1", "12, 23, 33, 42, 50, ...", True), g("l1b", "9th number = ?", True)),
    b("Look at the jumps. From 12 to 23 is 11. Then the jumps are 10, then 9, then 8.",
      jumps("l1", ["+11", "+10", "+9", "+8"])),
    b("So is this a pattern where we add the same amount each time?",
      ask=ch("no, each jump is 1 smaller", ["yes, add 11 each time", "no, each jump is 1 bigger"],
             "Read the jumps again: 11, 10, 9, 8. They shrink by 1 each time.")),
    b("The jumps shrink by 1. So the next ones are 7, 6, 5 and 4. And 50 is the 5th number, so 4 more jumps reach the 9th.",
      lab("l2", "next jumps: 7, 6, 5, 4"), nt("l1", "50", "5th", "above")),
    b("The 6th number is 50 plus 7, which is 57. The 7th is 57 plus 6, which is 63.",
      w("l3", "50 + 7 = 57"), nt("l3", "57", "6th"), w("l4", "57 + 6 = 63"), nt("l4", "63", "7th")),
    b("The 8th number is 63 plus 5, which is 68. One more jump to go.",
      w("l5", "63 + 5 = 68"), nt("l5", "68", "8th")),
    b("Which jump takes us from the 8th number to the 9th?",
      ask=ch("4", ["5", "8"], "The jumps after 50 are 7, 6, 5 and 4. We have used three of them, so the last one is 4.")),
    b("68 plus 4 is 72. So the 9th number is 72.", ans("l6", "68 + 4 = 72", "72")),
    b("When the jumps change, find how they change. Then step forward, and name each number as you go so you stop at the right one."),
]


# ── EXT_G4_FP_2025_004 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2025_004"] = [
    b("We need to add the first 12 odd numbers: 1, 3, 5, and so on. Adding 12 numbers is slow, so let's hunt for a short cut.",
      g("l1", "Sum of the first 12 odd numbers = ?", True)),
    b("Start small. The first 2 odd numbers are 1 and 3. They add to 4, and 4 is 2 times 2.",
      w("l2", "1 + 3 = 4"), w("l3", "4 = 2 × 2")),
    b("The first 3 odd numbers are 1, 3 and 5. They add to 9, and 9 is 3 times 3.",
      w("l4", "1 + 3 + 5 = 9"), w("l5", "9 = 3 × 3")),
    b("Can you see it coming? What do the first 4 odd numbers add up to?",
      ask=ch("4 × 4 = 16", ["4 × 3 = 12", "4 × 5 = 20"],
             "2 odd numbers made 2 times 2. 3 odd numbers made 3 times 3. So 4 odd numbers make 4 times 4, which is 16.")),
    b("Yes: 1 plus 3 plus 5 plus 7 is 16. The sum is always the count, multiplied by itself.",
      w("l6", "1 + 3 + 5 + 7 = 16"), lab("l7", "Sum = count × count")),
    b("So what is the sum of the first 12 odd numbers?",
      ask=ch("12 × 12", ["12 × 11", "12 × 13"],
             "The count is 12, and the rule is the count times itself. So it is 12 times 12.")),
    b("12 times 12. 12 tens are 120, and 12 twos are 24. Together that makes 144.",
      w("l8", "12 × 10 = 120"), w("l9", "12 × 2 = 24"), w("l9b", "120 + 24 = 144")),
    b("So the first 12 odd numbers add up to 144.", ans("l10", "12 × 12 = 144", "144")),
    b("Keep this fact. Add the odd numbers starting from 1, and the total is always the count times itself."),
]
