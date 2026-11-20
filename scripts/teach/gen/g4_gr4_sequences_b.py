"""gr4_sequences lessons written one by one: worksheet questions (EXT_G4_WS2_CH16_...)
and the newly written ones (G4A_SEQUENCES_...).

A few worksheet questions are also in the bank as Q_CH16_...; those lessons are
functions taking v (0 or 1) so the twin gets its own wording.
"""
from g4_gr4_sequences_a import far_term
from g4_gr4_sequences_lib import ans, b, ch, fig, g, grp, jumps, lab, mk, nt, qfig, ring, tbl, w

L = {}
TOPIC = "gr4_sequences"


# ── 9999999, 777777, ___, 3333, 111 ──────────────────────────────────────────
def repeated_digits(v):
    return [
        b(["Look at these strange numbers. Each one is a single digit written again and again. One term in the middle is missing.",
           "What an odd list! Every number is just one digit, repeated. And one of the numbers has gone missing from the middle."][v],
          g("l1", "9999999, 777777, ___, 3333, 111", True)),
        b("Don't try to subtract these giants. Look at which digit each one uses: 9, then 7, then the gap, then 3, then 1.",
          lab("l2", "digit used: 9, 7, ?, 3, 1")),
        b("So which digit does the missing term use?",
          ask=ch("5", ["6", "4"], "The digits go down by 2 each time: 9, 7, then 5, then 3, then 1.")),
        b("The digit is 5. Now count how many times each digit is written. Seven 9s. Six 7s. Then the gap. Then four 3s and three 1s.",
          lab("l3", "how many digits: 7, 6, ?, 4, 3")),
        b("So how many 5s does the missing term have?",
          ask=ch("five 5s", ["six 5s", "four 5s"],
                 "The lengths go 7, 6, then the gap, then 4, 3. They go down by 1 each time, so the gap has 5 digits.")),
        b("The digit is 5 and it is written 5 times. So the missing term is five 5s in a row.", ans("l4", "55555")),
        b("Two things had to be right at once: the digit and the length. Four 5s or six 5s would have the right digit, but not the right length."),
        b(["When numbers look huge, don't panic. Look at how they are built: which digits, and how many of them.",
           "So with odd-looking numbers, ask how each one is built. Here it was the digit used, and how many times."][v]),
    ]


L["EXT_G4_WS2_CH16_001"] = repeated_digits(0)


# ── EXT_G4_WS2_CH16_002: 416, 525, 636, 749 (by splitting the digits) ────────
L["EXT_G4_WS2_CH16_002"] = [
    b("Here is the sequence: 416, 525, 636, 749. We want the next term. There is a neat secret hiding inside these numbers.",
      g("l1", "416, 525, 636, 749, ___", True)),
    b("Split each number into its first digit and its last two digits. 4 and 16. 5 and 25. 6 and 36. 7 and 49.",
      lab("l2", "4 | 16    5 | 25    6 | 36    7 | 49")),
    b("Look at 4 and 16, then 5 and 25. How is the second part made from the first part?",
      ask=ch("the first part times itself", ["the first part plus 12", "the first part times 4"],
             "4 times 4 is 16, and 5 times 5 is 25. Each second part is the first part multiplied by itself.")),
    b("4 times 4 is 16. 5 times 5 is 25. 6 times 6 is 36. 7 times 7 is 49. It works for every term.",
      w("l3", "4 × 4 = 16"), w("l4", "5 × 5 = 25"), w("l5", "6 × 6 = 36"), w("l6", "7 × 7 = 49")),
    b("The first parts go 4, 5, 6, 7. So what are the two parts of the next term?",
      ask=ch("8 and 64", ["8 and 81", "9 and 81"], "After 7 comes 8. And 8 times 8 is 64.")),
    b("The first part is 8. The second part is 8 times 8, which is 64. Join them together to get 864.",
      w("l7", "8 × 8 = 64"), ans("l8", "864")),
    b("Let's check another way, with jumps. 525 minus 416 is 109. The next jumps are 111 and 113. They grow by 2, so the next jump is 115.",
      jumps("l1", ["+109", "+111", "+113", "+115"])),
    b("And 749 plus 115 is 864. Both ways agree!", w("l9", "749 + 115 = 864")),
    b("When the jumps look awkward, look inside the numbers. Sometimes each number is built from parts with their own rule."),
]


# ── 1, 8, 27, 64, 125 ────────────────────────────────────────────────────────
def cubes(v):
    return [
        b(["Our numbers are 1, 8, 27, 64, 125. They grow quickly. What comes next?",
           "Here is the sequence: 1, 8, 27, 64, 125. Each number is much bigger than the last. Let's find the next one."][v],
          g("l1", "1, 8, 27, 64, 125, ___", True)),
        b("Try the jumps first: 7, then 19, then 37, then 61. No easy pattern there. So let's look at each number on its own.",
          jumps("l1", ["+7", "+19", "+37", "+61"])),
        b("Think about the 8. Which of these makes 8?",
          ask=ch("2 × 2 × 2", ["2 × 2", "2 × 3"],
                 "2 times 2 is 4, and 4 times 2 is 8. So 8 is 2 used three times in a multiplication.")),
        b("1 times 1 times 1 is 1. 2 times 2 times 2 is 8. 3 times 3 times 3 is 27. Each counting number is used three times.",
          w("l2", "1 × 1 × 1 = 1"), w("l3", "2 × 2 × 2 = 8"), w("l4", "3 × 3 × 3 = 27")),
        b("It carries on. 4 times 4 times 4 is 64, and 5 times 5 times 5 is 125.",
          w("l5", "4 × 4 × 4 = 64"), w("l6", "5 × 5 × 5 = 125")),
        b("So what do we work out for the next term?",
          ask=ch("6 × 6 × 6", ["6 × 6", "5 × 5 × 6"],
                 "The numbers used so far are 1, 2, 3, 4, 5. Next is 6, and it is used three times: 6 times 6 times 6.")),
        b("Careful: 6 times 6 is 36, but we are not done. That is only two 6s. Now 36 times 6: 30 sixes are 180, and 6 sixes are 36.",
          w("l7", "6 × 6 = 36"), w("l8", "30 × 6 = 180"), w("l9", "180 + 36 = 216")),
        b("180 plus 36 is 216. So the next number is 216.", ans("l10", "6 × 6 × 6 = 216", "216")),
        b(["Numbers made like this are called cube numbers. When jumps don't help, ask how each number is made.",
           "So when the jumps give no clue, look at how each number is built. These are the cube numbers: a number used three times."][v]),
    ]


L["EXT_G4_WS2_CH16_004"] = cubes(0)


# ── 53, 56, 62, 71, 83, then two more ────────────────────────────────────────
def next_two_53(v):
    return [
        b(["The sequence goes 53, 56, 62, 71, 83. This time we need the next two terms, not just one.",
           "Here are five terms: 53, 56, 62, 71, 83. Two more are missing at the end. Let's find them both."][v],
          g("l1", "53, 56, 62, 71, 83, ___, ___", True)),
        b("Measure the jumps. 53 to 56 is 3. 56 to 62 is 6. Then 9, then 12.",
          jumps("l1", ["+3", "+6", "+9", "+12"])),
        b("The jumps are 3, 6, 9, 12. What will the next two jumps be?",
          ask=ch("15 and then 18", ["15 and then 15", "24 and then 48"],
                 "3, 6, 9, 12 are the multiples of 3. The jump grows by 3 every time, so next come 15 and then 18.")),
        b("The jumps go up by 3 each time. So the next two are 15 and 18. The trap is to use 15 twice.",
          jumps("l1", ["+15", "+18"], first=5)),
        b("83 plus 15 is 98. That is the first new term.", w("l2", "83 + 15 = 98")),
        b("Now the jump grows again. 98 plus 18 is 116. That is the second new term.", w("l3", "98 + 18 = 116")),
        b("So the next two terms are 98 and 116.", ans("l4", "98, 116", None, True)),
        b(["When the jumps keep growing, find how they grow. And remember the jump changes for every new term.",
           "So: find the jumps, see how the jumps grow, and let them keep growing for each new term you add."][v]),
    ]


L["EXT_G4_WS2_CH16_005"] = next_two_53(0)


# ── 525, 438, ___, 264, 177, 90 ──────────────────────────────────────────────
def missing_351(qid, v):
    return [
        b(["Our list is 525, 438, then a gap, then 264, 177, 90. One number in the middle is missing.",
           "Here are the numbers: 525, 438, a gap, 264, 177, 90. Let's find the one that fell out."][v],
          g("l1", "525, 438, ___, 264, 177, 90", True), fig("f1", qfig(TOPIC, qid))),
        b("The numbers are going down. Find the drop from 525 to 438. 525 minus 438 is 87.",
          w("l2", "525 − 438 = 87"), nt("l1", ",", "−87")),
        b("One pair is not enough to be sure of the rule. Which other pair can we use to check the drop?",
          ask=ch("264 and 177", ["438 and 264", "525 and 90"],
                 "We need two numbers that are next-door neighbours, with no gap between them. 264 and 177 are neighbours.")),
        b("264 minus 177 is 87. And 177 minus 90 is 87 again. So every drop is 87.",
          w("l3", "264 − 177 = 87"), w("l4", "177 − 90 = 87"), nt("l1", ",", "−87", "below", 4), nt("l1", ",", "−87", "below", 5)),
        b("Now take 87 away from 438. Take away 80 first to get 358. Then take away 7 to get 351.",
          w("l5", "438 − 80 = 358"), w("l6", "358 − 7 = 351")),
        b("So the missing number is 351.", ans("l7", "438 − 87 = 351", "351")),
        b("Does the drop after the gap fit too? 351 take away 87 is 264. Yes, that is the very next number in the list.",
          w("l8", "351 − 87 = 264")),
        b(["For a gap in the middle, find the jump from neighbours you can see. Then check on both sides of the gap.",
           "So when a number is missing in the middle, use the neighbours you can see to find the jump, and test your answer on both sides."][v]),
    ]


L["EXT_G4_WS2_CH16_006"] = missing_351("EXT_G4_WS2_CH16_006", 0)


# ── 4, 7, 11, 18, 29, then two more ──────────────────────────────────────────
def add_two_before(v):
    return [
        b(["The sequence is 4, 7, 11, 18, 29, and we need the next two terms.",
           "Here are five terms: 4, 7, 11, 18, 29. Two more belong at the end. Let's find them."][v],
          g("l1", "4, 7, 11, 18, 29, ___, ___", True)),
        b("Try the jumps: 3, then 4, then 7, then 11. They don't grow in a steady way. So the jumps are not the key here.",
          jumps("l1", ["+3", "+4", "+7", "+11"])),
        b("Here is the idea that unlocks it. Look at 4, 7 and 11. How can you make 11 from the two numbers before it?",
          ask=ch("4 + 7", ["7 × 2 − 4", "4 × 2 + 4"], "Just add the two numbers before it. 4 plus 7 is 11.")),
        b("4 plus 7 is 11. 7 plus 11 is 18. 11 plus 18 is 29. Each term is the sum of the two terms before it.",
          w("l2", "4 + 7 = 11"), w("l3", "7 + 11 = 18"), w("l4", "11 + 18 = 29")),
        b("So the next term is the last two added together. 18 plus 29 is 47.", w("l5", "18 + 29 = 47")),
        b("Now for the second new term. Which two numbers do we add this time?",
          ask=ch("29 and 47", ["18 and 47", "18 and 29"], "Always the two newest terms. Now those are 29 and 47.")),
        b("Careful: use the two newest terms. 29 plus 47 is 76.", w("l6", "29 + 47 = 76")),
        b("So the next two terms are 47 and 76.", ans("l7", "47, 76", None, True)),
        b(["When the jumps make no sense, try adding neighbours. Here every term is the two before it, added together.",
           "So if the jumps look messy, test whether each term is made from the two before it. That was the secret here."][v]),
    ]


L["EXT_G4_WS2_CH16_009"] = add_two_before(0)


# ── EXT_G4_WS2_CH16_015 ──────────────────────────────────────────────────────
L["EXT_G4_WS2_CH16_015"] = far_term(
    [92, 88, 84, 80, 76], 18, "term",
    "The series goes 92, 88, 84, 80, 76. It goes down by 4 each time, and we want the 18th term.",
    "",
    "Going down works just like going up. Count 1 fewer jump than the term number, multiply, and take that away from the 1st term.",
    down=True)


# ── How many terms? ──────────────────────────────────────────────────────────
def count_terms(qid, terms, last, split, v):
    a, d = terms[0], terms[1] - terms[0]
    dist = last - a
    n_jumps = dist // d
    p1, p2 = split
    shown = ", ".join(str(t) for t in terms)
    return [
        b(["The sequence is %s, and it carries on until %d. We are not asked for a term. We are asked how many terms there are." % (shown, last),
           "Here is a long list: %s, all the way up to %d. How many numbers are in it? Let's count without writing them all." % (shown, last)][v],
          g("l1", "%s, ..., %d" % (shown, last), True), g("l1b", "How many terms?", True)),
        b("First the jump. %d minus %d is %d, and %d minus %d is %d too. Each term is %d more than the one before." % (
            terms[1], a, d, terms[2], terms[1], d, d),
          w("l2", "%d − %d = %d" % (terms[1], a, d)), w("l2b", "%d − %d = %d" % (terms[2], terms[1], d)),
          jumps("l1", ["+%d" % d] * (len(terms) - 1))),
        b("How far is it from the first term to the last? %d minus %d is %d." % (last, a, dist),
          w("l3", "%d − %d = %d" % (last, a, dist))),
        b("That distance of %d is covered in jumps of %d. How do we find the number of jumps?" % (dist, d),
          ask=ch("%d ÷ %d" % (dist, d), ["%d × %d" % (dist, d), "%d − %d" % (dist, d)],
                 "We want to know how many %ds fit into %d. That is a division." % (d, dist))),
        b("Split %d into %d and %d. %d divided by %d is 10. %d divided by %d is %d. So there are %d jumps." % (
            dist, p1, p2, p1, d, p2, d, p2 // d, n_jumps),
          w("l4", "%d = %d + %d" % (dist, p1, p2)), w("l5", "%d ÷ %d = 10" % (p1, d)), w("l6", "%d ÷ %d = %d" % (p2, d, p2 // d)),
          w("l7", "%d ÷ %d = %d" % (dist, d, n_jumps))),
        b("There are %d jumps. So how many terms are there?" % n_jumps,
          ask=ch(str(n_jumps + 1), [str(n_jumps), str(n_jumps - 1)],
                 "Think small. 1 jump joins 2 numbers. 2 jumps join 3 numbers. There is always 1 more number than jumps.")),
        b("Here is the trap. Jumps sit between the terms, and the first term is there before any jump. So we add 1.",
          ans("l8", "%d + 1 = %d" % (n_jumps, n_jumps + 1), str(n_jumps + 1))),
        b("Check with the start of the list. From %d to %d is 4 jumps, and there are 5 terms. One more than the jumps. So there are %d terms in all." % (
            a, terms[4], n_jumps + 1)),
        b(["To count the terms: find the distance, divide by the jump, then add 1 for the first term.",
           "So the plan is: last take away first, divide by the jump to count the jumps, and add 1 to count the terms."][v]),
    ]


L["EXT_G4_WS2_CH16_017"] = count_terms("EXT_G4_WS2_CH16_017", [1, 7, 13, 19, 25], 103, (60, 42), 0)


# ── EXT_G4_WS2_CH16_018: five repeating symbols ──────────────────────────────
L["EXT_G4_WS2_CH16_018"] = [
    b("Five symbols repeat in the same order, again and again: star, square, circle, triangle, circled plus. Which one lands in the 37th place?",
      g("l1", "*, ■, ○, △, ⊕, *, ■, ○, △, ⊕, ...", True), g("l1b", "37th symbol = ?", True)),
    b("We won't draw 37 symbols. Think in groups of 5. The last symbol of each group sits in place 5, then 10, then 15, then 20, and so on.",
      grp("l1", [("*", 1), ("⊕", 1)], "one group of 5"), lab("l2", "groups end at 5, 10, 15, 20, ...")),
    b("Which is the last group to finish before the 37th place? It ends at place...",
      ask=ch("35", ["30", "40"],
             "7 groups of 5 end at place 35. The next group would end at 40, which is past 37.")),
    b("7 full groups use up 35 places. And 37 minus 35 leaves 2 more places.",
      w("l3", "7 × 5 = 35"), w("l4", "37 − 35 = 2")),
    b("So the 37th symbol is the same as which symbol in a group?",
      ask=ch("the 2nd", ["the 1st", "the 5th"],
             "After place 35 a new group starts. One place on is the 1st symbol, and two places on is the 2nd.")),
    b("Place 36 starts a new group with the star. Place 37 comes next, and that is the square.",
      lab("l5", "place 36: *"), lab("l6", "place 37: ■")),
    b("So the 37th symbol is the square.", ans("l7", "■", None, True)),
    b("Here is the same idea in one line. 37 is 7 fives and 2 more. The 2 left over tells you the place inside the group.",
      w("l8", "37 = 7 × 5 + 2")),
    b("For any repeating pattern: take out the full groups, then count on with what is left over."),
]


# ── G4A_SEQUENCES_001 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_001"] = [
    b("What a jumpy pattern! 2, 50, 5, 46, 8, 42, 11, 38. Up, down, up, down. We want the 15th number.",
      g("l1", "2, 50, 5, 46, 8, 42, 11, 38, ...", True), g("l1b", "15th number = ?", True)),
    b("It looks messy, but there is a trick. What do you get if you read only every second number, starting with the 2?",
      ask=ch("2, 5, 8, 11: up by 3", ["2, 50, 5: no pattern", "2, 5, 8, 11: up by 2"],
             "Skip one each time: 2, then 5, then 8, then 11. Those go up by 3.")),
    b("Two patterns are woven together. In the odd places: 2, 5, 8, 11, going up by 3. In the even places: 50, 46, 42, 38, going down by 4.",
      lab("l2", "odd places: 2, 5, 8, 11, ...  (+3)"), lab("l3", "even places: 50, 46, 42, 38, ...  (−4)")),
    b("15 is an odd number, so the 15th place is an odd place. Our answer comes from the pattern that goes up by 3.",
      mk("l2", "odd places", "underline")),
    b("Here is the trap. The 15th number of the mixed pattern is which number of 2, 5, 8, 11?",
      ask=ch("the 8th", ["the 15th", "the 7th"],
             "That pattern uses only every second place: 1, 3, 5, 7, and so on up to 15. Count those places and you get 8.")),
    b("The odd places are 1, 3, 5, 7, 9, 11, 13 and 15. That is 8 places. So we want the 8th number of 2, 5, 8, 11.",
      lab("l4", "places 1, 3, 5, 7, 9, 11, 13, 15"), lab("l5", "8 places")),
    b("The 8th number is 7 jumps from the 1st. 7 jumps of 3 make 21.",
      w("l6", "8 − 1 = 7"), w("l7", "7 × 3 = 21")),
    b("2 plus 21 is 23. So the 15th number in the pattern is 23.", ans("l8", "2 + 21 = 23", "23")),
    b("Check by listing that pattern: 2, 5, 8, 11, 14, 17, 20, 23. The 8th one is 23.",
      lab("l9", "2, 5, 8, 11, 14, 17, 20, 23")),
    b("When a pattern zigzags, split it into two. Then work out which of the two your place belongs to."),
]


# ── G4A_SEQUENCES_002 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_002"] = [
    b("The pattern 4, 9, 14, 19 goes up by 5 each time and stops at 99. We must count how many of its numbers are even.",
      g("l1", "4, 9, 14, 19, ..., 99", True), g("l1b", "How many are even?", True)),
    b("Look at the first few. 4 is even. 9 is odd. 14 is even. 19 is odd. They take turns.",
      nt("l1", "4", "even"), nt("l1", "9", "odd"), nt("l1", "14", "even"), nt("l1", "19", "odd")),
    b("Why do they take turns like that?",
      ask=ch("adding 5 flips odd and even", ["it is just luck", "adding 5 keeps even numbers even"],
             "5 is an odd number. Adding an odd number always changes even to odd, and odd to even.")),
    b("So the even ones are every second number: 4, 14, 24, and so on. They go up by 10 and all end in 4. The last one before 99 is 94.",
      lab("l2", "even ones: 4, 14, 24, ..., 94")),
    b("Now count them. From 4 to 94 is a distance of 90. Each jump is 10, so that is 9 jumps.",
      w("l3", "94 − 4 = 90"), w("l4", "90 ÷ 10 = 9")),
    b("There are 9 jumps. So how many even numbers are there?",
      ask=ch("10", ["9", "20"], "Jumps sit between the numbers. 9 jumps join 10 numbers, because both ends count.")),
    b("Careful with this last step. 9 jumps join 10 numbers. So 10 of the numbers are even.",
      ans("l5", "9 + 1 = 10", "10")),
    b("We can list them to be sure: 4, 14, 24, 34, 44, 54, 64, 74, 84, 94. Count them, and there are 10.",
      lab("l6", "4, 14, 24, 34, 44, 54, 64, 74, 84, 94")),
    b("So: pick out the numbers you want, see their own pattern, count the jumps, and add 1."),
]


# ── G4A_SEQUENCES_003 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_003"] = [
    b("The numbers climb up to 4 and come back down, over and over. We want the 100th number, and we are not going to write 100 numbers!",
      g("l1", "1, 2, 3, 4, 3, 2, 1, 2, 3, 4, 3, 2, 1, 2, 3, 4, ...", True), g("l1b", "100th number = ?", True)),
    b("A repeating pattern is made of one block, copied again and again. So first we must find the block."),
    b("Which block is copied again and again?",
      ask=ch("1, 2, 3, 4, 3, 2", ["1, 2, 3, 4, 3, 2, 1", "1, 2, 3, 4"],
             "This is the trap. If the block ended in 1, the next block would start with 1 too, and we would see 1, 1. So that 1 starts the next block.")),
    b("The block is 1, 2, 3, 4, 3, 2. It has 6 numbers, not 7. The next 1 begins a new block.",
      lab("l2", "block: 1, 2, 3, 4, 3, 2"), lab("l3", "6 numbers in a block")),
    b("Now fill up with blocks of 6. 10 blocks use 60 numbers. 6 more blocks use 36. So 16 blocks use 96 numbers.",
      w("l4", "10 × 6 = 60"), w("l5", "6 × 6 = 36"), w("l6", "16 × 6 = 96")),
    b("100 take away 96 leaves 4. So the 100th number is the 4th number of the next block.",
      w("l7", "100 − 96 = 4")),
    b("What is the 4th number in the block 1, 2, 3, 4, 3, 2?",
      ask=ch("4", ["3", "2"], "Count along the block. The 1st is 1, the 2nd is 2, the 3rd is 3 and the 4th is 4.")),
    b("So the 100th number in the pattern is 4.", mk("l2", "4", "circle"), ans("l8", "100th number = 4", "4", True)),
    b("For a repeating pattern: find the true block, take out the full blocks, and count on with what is left."),
]


# ── G4A_SEQUENCES_004 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_004"] = [
    b("A long chain: 20 minus 19, plus 18, minus 17, and so on, down to plus 2, minus 1. We won't work from left to right. There is a smarter way.",
      g("l1", "20 − 19 + 18 − 17 + ... + 2 − 1 = ?", True)),
    b("Look at the numbers two at a time. 20 minus 19. Then 18 minus 17. Right down to 2 minus 1.",
      grp("l1", ["20 − 19", "18 − 17", "2 − 1"], "pairs")),
    b("What is each pair worth?",
      ask=ch("1", ["0", "2"], "20 minus 19 is 1. 18 minus 17 is 1. Every pair leaves exactly 1.")),
    b("Each pair is worth 1. So the whole chain is just 1 plus 1 plus 1, once for every pair.",
      w("l2", "20 − 19 = 1"), w("l3", "18 − 17 = 1"), w("l4", "2 − 1 = 1")),
    b("There are 20 numbers in the chain. How many pairs do they make?",
      ask=ch("10", ["20", "19"], "A pair uses up 2 numbers. So 20 numbers make half of 20 pairs, which is 10.")),
    b("That is the step to be careful with. 20 numbers, but only 10 pairs.", w("l5", "20 ÷ 2 = 10")),
    b("10 pairs, each worth 1. So the value of the whole chain is 10.", ans("l6", "10 × 1 = 10", "10", False)),
    b("When a long sum has a rhythm, group it into pairs. Often every pair is worth the same, and the rest is easy."),
]


# ── G4A_SEQUENCES_005 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_005"] = [
    b("Farid makes a triangle of dots. Row 1 has 1 dot, row 2 has 2 dots, row 3 has 3, and so on. He has 60 dots. How many will be left over?",
      g("l1", "Rows of 1, 2, 3, 4, ... dots", True), g("l1b", "60 dots. Left over = ?", True)),
    b("Let's keep a running total of the dots he has used. After row 1: 1. After row 2: 3. After row 3: 6. After row 4: 10.",
      lab("l2", "dots used: 1, 3, 6, 10")),
    b("Carry on. Row 5 brings the total to 15. Row 6 makes 21. Row 7 makes 28. Row 8 makes 36.",
      lab("l3", "then: 15, 21, 28, 36")),
    b("Row 9 adds 9 dots: 36 plus 9 is 45. Row 10 adds 10 dots: 45 plus 10 is 55.",
      w("l4", "36 + 9 = 45"), w("l5", "45 + 10 = 55")),
    b("After 10 rows he has used 55 of his 60 dots. Can he finish row 11?",
      ask=ch("no, row 11 needs 11 dots", ["yes, 55 is less than 60", "yes, he has 11 dots left"],
             "After 10 rows, only 60 take away 55 dots are left. Row 11 needs 11 dots, and that is too many.")),
    b("Row 11 would bring the total to 66. That is more than 60, so he stops after 10 complete rows.",
      w("l6", "55 + 11 = 66"), w("l7", "66 > 60")),
    b("He used 55 dots. 60 take away 55 leaves 5.", ans("l8", "60 − 55 = 5", "= 5")),
    b("Careful with what the question asks. 10 is the number of rows. We were asked for the dots left over, and that is 5."),
    b("Keep a running total, stop before you go past the limit, and then subtract."),
]


# ── G4A_SEQUENCES_006 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_006"] = [
    b("Arun saves 5 rupees on day 1. Each day after, he saves 3 rupees more than the day before. On which day does his total first go past 100 rupees?",
      g("l1", "Day 1: ₹5.  Each day: ₹3 more.", True), g("l1b", "Total first more than ₹100 on day ?", True)),
    b("Two different things are growing here. Which one has to go past 100?",
      ask=ch("the total saved so far", ["the amount saved on one day", "the number of days"],
             "Read the question again. It asks about the total money he has saved, with all the days added together.")),
    b("Let's make a table. Each day he saves 3 more: 5, 8, 11, 14. And we keep a running total: 5, 13, 24, 38.",
      tbl("f1", [[1, 5, 5], [2, 8, 13], [3, 11, 24], [4, 14, 38]], "Add each day's saving to the total", ["Day", "Saved", "Total"])),
    b("Day 5: he saves 17, and the total is 55. Day 6: he saves 20, total 75. Day 7: he saves 23, total 98.",
      w("l2", "38 + 17 = 55"), w("l3", "55 + 20 = 75"), w("l4", "75 + 23 = 98")),
    b("After day 7 the total is 98. Has it gone past 100 yet?",
      ask=ch("not yet", ["yes, 98 is close enough"],
             "98 is close, but it is still less than 100. More than 100 means past it.")),
    b("On day 8 he saves 26. 98 plus 26 is 124. Now the total is past 100.", w("l5", "98 + 26 = 124")),
    b("So the total first goes past 100 rupees on the 8th day.", ans("l6", "8th day", None, True)),
    b("When a question is about a total, keep a running total, and stop at the first moment it crosses the line."),
]


# ── G4A_SEQUENCES_007 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_007"] = [
    b("Here is the pattern: 2, 6, 4, 12, 10, 30, 28. It jumps up a lot, then drops a little. We want the 10th number.",
      g("l1", "2, 6, 4, 12, 10, 30, 28, ...", True), g("l1b", "10th number = ?", True)),
    b("How do we get from 2 to 6, and then from 6 to 4?",
      ask=ch("times 3, then take away 2", ["add 4, then take away 2", "times 3, then halve"],
             "Test it further along. 4 times 3 is 12, and 12 take away 2 is 10. Times 3, then take away 2, works every time.")),
    b("2 times 3 is 6. 6 take away 2 is 4. 4 times 3 is 12. 12 take away 2 is 10. The two moves take turns.",
      w("l2", "2 × 3 = 6"), w("l3", "6 − 2 = 4"), w("l4", "4 × 3 = 12"), w("l5", "12 − 2 = 10")),
    b("7 numbers are given. The last move was take away 2, from 30 down to 28. So the next move is times 3.",
      nt("l1", "28", "7th", "above")),
    b("The 8th number is 28 times 3, which is 84. The 9th is 84 take away 2, which is 82.",
      w("l6", "28 × 3 = 84"), nt("l6", "84", "8th"), w("l7", "84 − 2 = 82"), nt("l7", "82", "9th")),
    b("What is the move from the 9th number to the 10th?",
      ask=ch("times 3", ["take away 2", "add 3"], "The moves take turns. We just took away 2, so now it is times 3.")),
    b("82 times 3. 80 threes are 240, and 2 threes are 6. That makes 246.",
      w("l8", "80 × 3 = 240"), w("l9", "2 × 3 = 6"), ans("l10", "82 × 3 = 246", "246")),
    b("So the 10th number is 246. Don't stop early: 84 is only the 8th, and 82 is only the 9th."),
    b("When a pattern goes up and down, look for two moves that take turns. Then keep careful count of which number you are on."),
]


# ── G4A_SEQUENCES_008 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_008"] = [
    b("Two patterns. A goes up in 4s: 5, 9, 13, 17. B goes up in 7s: 2, 9, 16, 23. Both have 9. Where do they meet next?",
      g("l1", "A: 5, 9, 13, 17, ...  (+4)", True), g("l2", "B: 2, 9, 16, 23, ...  (+7)", True),
      ring("l1", "9"), ring("l2", "9")),
    b("Start from the 9 they share. A moves on by 4, 8, 12, 16, and so on. B moves on by 7, 14, 21, 28, and so on.",
      lab("l3", "A is 9 plus: 4, 8, 12, 16, 20, 24, 28"), lab("l4", "B is 9 plus: 7, 14, 21, 28")),
    b("They meet when the distance from 9 is in both lists. What is the first distance that is in both?",
      ask=ch("28", ["11", "14"], "Look along both lists. 28 is in the 4s list and in the 7s list. It is the first number in both.")),
    b("4 times 7 is 28. It is the smallest number that both 4 and 7 go into. So the patterns meet again 28 after the 9.",
      w("l5", "4 × 7 = 28"), mk("l3", "28", "box"), mk("l4", "28", "box")),
    b("Careful now. Is 28 our answer?",
      ask=ch("no, add 28 to 9", ["yes, 28 is the number"],
             "28 is how far apart the shared numbers are. The number itself is 9 plus 28.")),
    b("28 is the distance, not the number. 9 plus 28 is 37.", ans("l6", "9 + 28 = 37", "37")),
    b("Let's check by writing them out. A carries on 21, 25, 29, 33, 37. B carries on 30, then 37. Both reach 37.",
      lab("l7", "A: 5, 9, 13, 17, 21, 25, 29, 33, 37"), lab("l8", "B: 2, 9, 16, 23, 30, 37")),
    b("Two patterns meet again after a distance that both step sizes can make. Find that distance, then add it to the number they share."),
]


# ── G4A_SEQUENCES_009 ────────────────────────────────────────────────────────
L["G4A_SEQUENCES_009"] = [
    b("A pattern goes up by the same amount each time. Its 5th number is 23 and its 8th number is 35. We want the 1st number.",
      g("l1", "5th number = 23,  8th number = 35", True), g("l1b", "1st number = ?", True),
      fig("f1", qfig(TOPIC, "G4A_SEQUENCES_009"))),
    b("We don't know the jump yet. But we know two numbers. From the 5th number to the 8th, how many jumps are there?",
      ask=ch("3", ["4", "8"], "5th to 6th, 6th to 7th, 7th to 8th. That is 3 jumps.")),
    b("In those 3 jumps the numbers rise from 23 to 35. That is a rise of 12. So one jump is 12 divided by 3, which is 4.",
      w("l2", "35 − 23 = 12"), w("l3", "12 ÷ 3 = 4")),
    b("Now walk back from the 5th number to the 1st. How many jumps back is that?",
      ask=ch("4", ["5", "3"], "5th to 4th, to 3rd, to 2nd, to 1st. Count them: 4 jumps.")),
    b("This is the trap. It is the 5th number, but it is only 4 jumps away from the 1st. 4 jumps of 4 make 16.",
      w("l4", "5 − 1 = 4"), w("l5", "4 × 4 = 16")),
    b("So go back 16 from 23. 23 take away 16 is 7. The 1st number is 7.", ans("l6", "23 − 16 = 7", "7")),
    b("Check by writing the pattern: 7, 11, 15, 19, 23, 27, 31, 35. The 5th is 23 and the 8th is 35. It works.",
      lab("l7", "7, 11, 15, 19, 23, 27, 31, 35")),
    b("Two known numbers give you the jump. Then count the jumps carefully and walk to the number you want."),
]
