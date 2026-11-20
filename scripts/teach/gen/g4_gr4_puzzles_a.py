"""gr4_puzzles lessons written one by one: past-paper questions EXT_G4_FP_... and the
worksheet question EXT_G4_WS2_CH15_002.

product_puzzle() is the shared skeleton for the "which of these can be the product"
questions; each question passes its own numbers, its own wording and its own traps.
"""
from g4_gr4_sequences_lib import ans, b, ch, fig, g, lab, mk, nt, qfig, st, tbl, w

L = {}
TOPIC = "gr4_puzzles"


def product_puzzle(form, open_say, d1, d2, digit_others, choices, by_digit, small, too_small, large, too_big,
                   answer, example, small_ask, end_say, large_say=None, extra=None, made_say=None):
    prod = d1 * d2
    last = prod % 10
    p_small, p_large = small[0] * small[1], large[0] * large[1]
    beats = [
        b(open_say, g("l1", form, True), g("c", "     ".join(str(c) for c in choices), True)),
        b("We can't see the hidden digits. But we can still work out the last digit of the product. What is it?",
          ask=ch("%d, because %d × %d = %d" % (last, d1, d2, prod), digit_others,
                 "The last digit of a product comes only from the last digits of the two numbers. %d times %d is %d, so the product ends in %d." % (
                     d1, d2, prod, last))),
    ]
    if by_digit is not None:
        beats.append(b("%d times %d is %d, so the product must end in %d. One choice ends in %d, so we cross it out." % (
            d1, d2, prod, last, by_digit % 10),
            w("l2", "%d × %d = %d" % (d1, d2, prod)), st("c", str(by_digit), "ends in %d" % (by_digit % 10))))
    else:
        beats.append(b("%d times %d is %d, so the product must end in %d. But look: all four choices end in %d! So we need another test." % (
            d1, d2, prod, last, last), w("l2", "%d × %d = %d" % (d1, d2, prod))))
    beats.append(b(small_ask[0], ask=ch(small_ask[1], small_ask[2], small_ask[3])))
    beats.append(b("The smallest numbers that fit are %d and %d. Their product is %d. So %d is too small." % (
        small[0], small[1], p_small, too_small),
        w("l3", "%d × %d = %d" % (small[0], small[1], p_small)), st("c", str(too_small), "too small")))
    beats.append(b(large_say or "The largest numbers that fit are %d and %d. Their product is %d. So %d is too big." % (
        large[0], large[1], p_large, too_big),
        w("l4", "%d × %d = %d" % (large[0], large[1], p_large)), st("c", str(too_big), "too big")))
    if extra:
        beats += extra
    beats.append(b("Only one choice is left: %d. It ends in %d, and it is the right size." % (answer, last),
                   mk("c", str(answer), "circle"), ans("l5", str(answer))))
    if example:
        beats.append(b(made_say or "And it really can be made. For example, %d times %d is exactly %d." % (example[0], example[1], answer),
                       w("l6", "%d × %d = %d" % (example[0], example[1], answer))))
    beats.append(b(end_say))
    return beats


# ── EXT_G4_FP_2020_001 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2020_001"] = [
    b("There are 25 trays. 15 of them have a cup and 21 have a plate. Some trays have both. How many?",
      g("l1", "25 trays.  Cups: 15.  Plates: 21.  Both = ?", True), fig("f1", qfig(TOPIC, "EXT_G4_FP_2020_001"))),
    b("Let's add the trays with cups and the trays with plates. 15 plus 21 is 36.", w("l2", "15 + 21 = 36")),
    b("But there are only 25 trays! Why did we get 36?",
      ask=ch("trays with both were counted twice", ["we added badly", "some trays are empty"],
             "A tray with a cup and a plate is in the 15, and it is in the 21 as well. So it got counted two times.")),
    b("Every tray with both was counted once with the cups and once again with the plates. So the extra count is exactly the trays with both.",
      mk("l2", "36", "underline")),
    b("36 take away 25 is 11. So 11 trays have both a cup and a plate.", ans("l3", "36 − 25 = 11", "11")),
    b("Check. Cup only: 15 take away 11 is 4. Plate only: 21 take away 11 is 10. And 4 plus 11 plus 10 is 25 trays. It works.",
      w("l4", "15 − 11 = 4"), w("l5", "21 − 11 = 10"), w("l6", "4 + 11 + 10 = 25")),
    b("When two groups overlap, add them, then take away the real total. What is left over is the overlap."),
]


# ── EXT_G4_FP_2020_010 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2020_010"] = [
    b("The teacher has a 3-digit odd number. Its hundreds digit is more than 8. Its tens digit is 4 more than its ones digit. We want the sum of its digits.",
      g("l1", "3-digit odd number", True), g("l2", "hundreds > 8,  tens = ones + 4", True), g("l3", "sum of digits = ?", True)),
    b("Take one clue at a time. The hundreds digit is more than 8. Which digit can that be?",
      ask=ch("only 9", ["8 or 9", "any digit"], "Digits stop at 9. The only digit bigger than 8 is 9.")),
    b("So the hundreds digit is 9. Next clue: the number is odd. So its ones digit is odd: 1, 3, 5, 7 or 9.",
      lab("l4", "hundreds digit: 9"), lab("l5", "ones digit: 1, 3, 5, 7 or 9")),
    b("The tens digit is 4 more than the ones digit, and it must still be a single digit. Which ones digits are possible?",
      ask=ch("1, 3 or 5", ["1, 3, 5, 7 or 9", "only 1"],
             "Try 7. Adding 4 gives more than 9, and that is not a single digit. So the ones digit can only be 1, 3 or 5.")),
    b("Ones digit 1 gives tens digit 5: the number 951. Ones digit 3 gives 973. Ones digit 5 gives 995. Three numbers fit the clues!",
      tbl("f1", [["1", "5", "951"], ["3", "7", "973"], ["5", "9", "995"]], "Tens digit = ones digit + 4", ["Ones", "Tens", "Number"])),
    b("Add the digits of each one. 951 gives 15. 973 gives 19. 995 gives 23.",
      w("l6", "9 + 5 + 1 = 15"), w("l7", "9 + 7 + 3 = 19"), w("l8", "9 + 9 + 5 = 23")),
    b("Now look at the choices. 19 and 23 are not there, but 15 is. So the teacher's number must be 951.",
      mk("l6", "15", "box")),
    b("So the sum of the digits is 15.", ans("l9", "Sum of digits = 15", "15", True)),
    b("Use one clue at a time to cut down the possibilities. Then test whatever is left."),
]


# ── EXT_G4_FP_2020_011 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2020_011"] = [
    b("Our number is 2, 1, 3, and then two hidden digits, a and b. Divide it by 100 and the remainder is less than 10. And all five digits add up to 13.",
      g("l1", "5-digit number 213ab", True), g("l2", "÷ 100 leaves a remainder under 10", True), g("l3", "digits add up to 13.  b = ?", True)),
    b("When you divide a number by 100, what is the remainder? Think of 21345. It is 213 hundreds, and 45 left over.",
      lab("l4", "21345 = 213 hundreds + 45"),
      ask=ch("its last two digits", ["its last digit", "its first three digits"],
             "Look at 21345. The hundreds use up 213, and the 45 at the end is left over. The remainder is the last two digits.")),
    b("So here the remainder is the two-digit ending, a b. And it is less than 10. An ending below 10 must start with 0. So a is 0.",
      lab("l5", "remainder = ab, less than 10"), lab("l6", "a = 0")),
    b("Now add the digits we know: 2 plus 1 plus 3 plus 0. That is 6.", w("l7", "2 + 1 + 3 + 0 = 6")),
    b("All five digits add up to 13, and we have 6 so far. So what is b?",
      ask=ch("7", ["6", "13"], "b is what must be added to 6 to reach 13. And 13 take away 6 is 7.")),
    b("13 take away 6 is 7. So b is 7.", w("l8", "13 − 6 = 7"), ans("l9", "b = 7", None, True)),
    b("Check. The number is 21307. Its digits add up to 13. And dividing by 100 leaves 7, which is less than 10.",
      lab("l10", "21307"), w("l11", "2 + 1 + 3 + 0 + 7 = 13")),
    b("The remainder clue looked scary, but it only told us that a is 0. Turn each clue into a plain fact about the digits."),
]


# ── The "which can be the product" questions ─────────────────────────────────
L["EXT_G4_FP_2021_006"] = product_puzzle(
    "(□□7) × (□□8) = ?",
    "Two 3-digit numbers are multiplied. One ends in 7 and the other ends in 8. The boxes hide the other digits. Which choice could be the product?",
    7, 8, ["5, because 7 + 8 = 15", "8, the bigger digit"],
    [10552, 9786, 308256, 9950006], 10552,
    (107, 108), 9786, (997, 998), 9950006, 308256, (507, 608),
    ("Now think about size. What is the smallest 3-digit number that ends in 7?", "107", ["117", "100"],
     "A 3-digit number starts with at least 1, and the middle digit can be 0. So the smallest one ending in 7 is 107."),
    "When digits are hidden, test what you can: the last digit, and the smallest and largest the answer could be.")

L["EXT_G4_FP_2022_005"] = product_puzzle(
    "(*8) × (**7) = ?",
    "A 2-digit number ending in 8 is multiplied by a 3-digit number ending in 7. The stars hide the other digits. Which choice can be the product?",
    8, 7, ["5, because 8 + 7 = 15", "8, the bigger digit"],
    [977006, 97706, 1506, 97704], 97704,
    (18, 107), 1506, (98, 997), 977006, 97706, None,
    ("Now the size. What is the smallest 2-digit number that ends in 8?", "18", ["08", "28"],
     "A 2-digit number cannot start with 0. So the smallest one ending in 8 is 18."),
    "With hidden digits, check the last digit first. Then squeeze the answer between the smallest and the largest product.",
    large_say="The largest numbers that fit are 98 and 997. Their product is 97706. So 977006 is too big. And look: 97706 itself is one of the choices!")

L["EXT_G4_FP_2024_018"] = product_puzzle(
    "(★★8) × (★6) = ?",
    "A 3-digit number ending in 8 is multiplied by a 2-digit number ending in 6. The stars hide the other digits. Which choice can be the product?",
    8, 6, ["4, because 8 + 6 = 14", "6, the smaller digit"],
    [1658, 980808, 87604, 43928], 87604,
    (108, 16), 1658, (998, 96), 980808, 43928, (578, 76),
    ("Next, the size. What are the smallest numbers that fit: a 3-digit number ending in 8 and a 2-digit number ending in 6?",
     "108 and 16", ["100 and 10", "118 and 26"],
     "The first digit must be at least 1, and any middle digit can be 0. So the smallest are 108 and 16."),
    "The last digit rules out one choice, and the size rules out two more. That is how to beat hidden digits.")

L["EXT_G4_FP_2025_021"] = product_puzzle(
    "(**4) × (**8) = ?",
    "Two 3-digit numbers are multiplied. One ends in 4 and the other ends in 8. The stars hide the other digits. Which choice could be the product?",
    4, 8, ["4, the smaller digit", "8, the bigger digit"],
    [672672, 564976, 9092012, 10992], 564976,
    (104, 108), 10992, (994, 998), 9092012, 672672, (784, 858),
    ("Now the size. What is the smallest 3-digit number that ends in 4?", "104", ["114", "004"],
     "A 3-digit number starts with at least 1, and its middle digit can be 0. So the smallest one ending in 4 is 104."),
    "First the last digit, then the smallest and largest products. Three quick tests, and only one choice is still standing.")


# ── EXT_G4_FP_2023_007 (two choices pass the quick tests) ────────────────────
L["EXT_G4_FP_2023_007"] = product_puzzle(
    "(★★6) × (★9) = ?",
    "A 3-digit number ending in 6 is multiplied by a 2-digit number ending in 9. The stars hide the other digits. Which choice can be the product?",
    6, 9, ["5, because 6 + 9 = 15", "9, the bigger digit"],
    [1854, 986004, 51684, 40548], None,
    (106, 19), 1854, (996, 99), 986004, 51684, (876, 59),
    ("So let's test the size. What are the smallest numbers that fit: a 3-digit number ending in 6 and a 2-digit number ending in 9?",
     "106 and 19", ["100 and 10", "116 and 29"],
     "The first digit must be at least 1, and a middle digit can be 0. So the smallest are 106 and 19."),
    "Most hidden-digit puzzles fall to the last digit and the size. When two choices are still standing, test whether each one can really be made.",
    extra=[
        b("Two choices are still standing: 51684 and 40548. This is the hard part. The product must divide exactly by a 2-digit number ending in 9.",
          lab("l4b", "divides by 19, 29, 39, ... or 99?")),
        b("Here is 40548 divided by each of them. Every time something is left over. So 40548 cannot be made.",
          tbl("f1", [["÷ by", "19", "29", "39", "49"], ["left over", "2", "6", "27", "25"],
                     ["÷ by", "59", "69", "79", "89"], ["left over", "15", "45", "21", "53"],
                     ["÷ by", "99", "·", "·", "·"], ["left over", "57", "·", "·", "·"]],
              "40548 never divides exactly"),
          st("c", "40548", "cannot be made")),
    ],
    made_say="And this one really can be made: 876 times 59 is exactly 51684.")


# ── EXT_G4_FP_2021_034 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2021_034"] = [
    b("Here is a square of numbers. Top row: 4, 5, 7. Middle row: 2, 2, 2. Bottom row: 64, 100 and A. The secret is in the columns.",
      g("l1", "4, 5, 7 / 2, 2, 2 / 64, 100, A", True),
      tbl("f1", [["4", "5", "7"], ["2", "2", "2"], ["64", "100", "A"]], "Each column follows the same rule")),
    b("Look down the first column: 4, then 2, then 64. What can we do with 4 and 2 to make 64?",
      ask=ch("multiply them, then times itself", ["add them, then times itself", "multiply them, then double"],
             "4 times 2 is 8, and 8 times 8 is 64. Adding gives 6, and 6 times 6 is not 64.")),
    b("4 times 2 is 8. And 8 times 8 is 64. That fits the first column.", w("l2", "4 × 2 = 8"), w("l3", "8 × 8 = 64")),
    b("A rule must work every time, so test the second column. 5 times 2 is 10, and 10 times 10 is 100. It works again.",
      w("l4", "5 × 2 = 10"), w("l5", "10 × 10 = 100")),
    b("Now the third column. 7 times 2 is 14.", w("l6", "7 × 2 = 14")),
    b("So what is A?",
      ask=ch("14 × 14", ["14 × 2", "9 × 9"],
             "The second step of the rule is to multiply the result by itself. So A is 14 times 14.")),
    b("14 times 14. 14 tens are 140, and 14 fours are 56. Together that is 196.",
      w("l7", "14 × 10 = 140"), w("l8", "14 × 4 = 56"), w("l9", "140 + 56 = 196")),
    b("So A is 196.", ans("l10", "14 × 14 = 196", "196")),
    b("Find a rule in one complete column, test it on another, and only then use it on the column with the gap."),
]


# ── EXT_G4_FP_2022_028 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2022_028"] = [
    b("A square of numbers. Each column follows the same rule, going down. We must find Z, in the middle of the third column.",
      g("l1", "Each column follows the same rule.  Z = ?", True), fig("f1", qfig(TOPIC, "EXT_G4_FP_2022_028"))),
    b("The first column is 7, 3 and 16. The second is 13, 6 and 49. Which rule works for both columns?",
      ask=ch("subtract, then times itself", ["add, then add 6", "multiply, then take away 5"],
             "7 take away 3 is 4, and 4 times 4 is 16. 13 take away 6 is 7, and 7 times 7 is 49. That rule fits both columns.")),
    b("7 take away 3 is 4, and 4 times 4 is 16. 13 take away 6 is 7, and 7 times 7 is 49. The rule fits both.",
      w("l2", "7 − 3 = 4"), w("l3", "4 × 4 = 16"), w("l4", "13 − 6 = 7"), w("l5", "7 × 7 = 49")),
    b("The third column is 24, then Z, then 169. This time we know the bottom number and not the middle. So we work backwards."),
    b("Which number, multiplied by itself, makes 169?",
      ask=ch("13", ["12", "14"], "Try 13. 13 times 13 is 169.")),
    b("13 times 13 is 169. So 24 take away Z must be 13.", w("l6", "13 × 13 = 169"), lab("l7", "24 − Z = 13")),
    b("Careful: 13 is not Z. Z is what we take from 24 to leave 13. 24 take away 13 is 11.",
      w("l8", "24 − 13 = 11"), ans("l9", "Z = 11", None, True)),
    b("Check the whole column. 24 take away 11 is 13, and 13 times 13 is 169. So Z is 11.", w("l10", "24 − 11 = 13")),
    b("When the gap is in the middle of a rule, find the rule from the full columns, then run it backwards."),
]


# ── EXT_G4_FP_2023_029 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2023_029"] = [
    b("Each column of this square follows the same rule, going down. We must find Q at the bottom of the third column.",
      g("l1", "Each column follows the same rule.  Q = ?", True), fig("f1", qfig(TOPIC, "EXT_G4_FP_2023_029"))),
    b("Look at the first two columns. 3 goes to 9, and 7 goes to 21. How do we get from the top number to the middle one?",
      ask=ch("multiply by 3", ["add 6", "multiply it by itself"],
             "3 times 3 is 9, and 7 times 3 is 21. Multiplying by 3 works in both columns.")),
    b("3 times 3 is 9. 7 times 3 is 21. And in the third column, 8 times 3 is 24. Good, the rule holds.",
      w("l2", "3 × 3 = 9"), w("l3", "7 × 3 = 21"), w("l4", "8 × 3 = 24")),
    b("Now from the middle to the bottom. 9 becomes 81, and 21 becomes 441. What is the rule?",
      ask=ch("multiply it by itself", ["multiply by 9", "multiply by 21"],
             "9 times 9 is 81. And 21 times 21 is 441. Each middle number is multiplied by itself.")),
    b("9 times 9 is 81, and 21 times 21 is 441. So each bottom number is the middle number times itself.",
      w("l5", "9 × 9 = 81"), w("l6", "21 × 21 = 441")),
    b("So Q is 24 times 24. Split it: 24 twenties are 480, and 24 fours are 96.",
      w("l7", "24 × 20 = 480"), w("l8", "24 × 4 = 96")),
    b("480 plus 96 is 576. So Q is 576.", ans("l9", "24 × 24 = 576", "576")),
    b("A rule can have two steps. Find each step from the complete columns, then follow both steps down the last column."),
]


# ── EXT_G4_FP_2024_015 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2024_015"] = [
    b("In a magic square, every row, every column and both diagonals add up to the same total. We must find m plus n.",
      g("l1", "Magic square.  m + n = ?", True), fig("f1", qfig(TOPIC, "EXT_G4_FP_2024_015"))),
    b("We don't know the total yet. But look at two lines that both pass through x: the middle row 4, x, m, and the diagonal 6, x, 16.",
      lab("l2", "row: 4 + x + m"), lab("l3", "diagonal: 6 + x + 16")),
    b("Both lines have the same total, and both contain x. So what must be equal?",
      ask=ch("4 + m and 6 + 16", ["4 and 6", "m and x"],
             "Take x away from both lines. What is left must still be equal: 4 plus m on one line, 6 plus 16 on the other.")),
    b("6 plus 16 is 22. So 4 plus m is 22 too, and m is 18.",
      w("l4", "6 + 16 = 22"), w("l5", "22 − 4 = 18"), lab("l6", "m = 18")),
    b("Now for the magic total. Here is a fact about every 3 by 3 magic square: each line adds up to 3 times the middle number.",
      lab("l7", "line total = 3 × middle number")),
    b("The diagonal is 22 plus x, and that must be 3 lots of x. So 22 is 2 lots of x. That makes x 11, and the magic total 3 times 11, which is 33.",
      w("l8", "22 ÷ 2 = 11"), w("l9", "3 × 11 = 33")),
    b("The first column is n, 4 and 16, and it must add up to 33. So what is n?",
      ask=ch("13", ["20", "11"], "4 plus 16 is 20. And 33 take away 20 is 13.")),
    b("4 plus 16 is 20, and 33 take away 20 is 13. So n is 13.",
      w("l10", "4 + 16 = 20"), w("l11", "33 − 20 = 13"), lab("l12", "n = 13")),
    b("m is 18 and n is 13. So m plus n is 31.", ans("l13", "18 + 13 = 31", "31")),
    b("Here is the finished square. Every row, column and diagonal adds up to 33.",
      tbl("f2", [["13", "14", "6"], ["4", "11", "18"], ["16", "8", "9"]], "Every line adds up to 33")),
    b("In a magic square, compare two lines that share a box. And remember: each line is 3 times the middle number."),
]


# ── EXT_G4_FP_2024_035 ───────────────────────────────────────────────────────
L["EXT_G4_FP_2024_035"] = [
    b("63 students stand in a queue. You are 13th from the beginning. Your friend is 19th from the end. How many students are between you?",
      g("l1", "Queue of 63.  You: 13th from the beginning.", True), g("l2", "Friend: 19th from the end.  Between = ?", True),
      fig("f1", qfig(TOPIC, "EXT_G4_FP_2024_035"))),
    b("The two places are counted from different ends. So let's find your friend's place from the beginning. First: how many students stand behind your friend?",
      ask=ch("18", ["19", "20"], "Your friend is the 19th from the end. So 18 students come after your friend.")),
    b("18 students stand behind your friend. So your friend's place from the beginning is 63 take away 18, which is 45.",
      w("l3", "19 − 1 = 18"), w("l4", "63 − 18 = 45")),
    b("You are 13th and your friend is 45th. So the students between you are in places 14 up to 44.",
      lab("l5", "You: 13th     Friend: 45th"), lab("l6", "between: places 14 to 44")),
    b("How many places are there from 14 to 44?",
      ask=ch("31", ["30", "32"],
             "44 take away 14 is 30, but that leaves out one end. Places 14 and 44 both count, so add 1.")),
    b("44 take away 14 is 30. But place 14 and place 44 are both students between you, so add 1. That makes 31.",
      w("l7", "44 − 14 = 30"), ans("l8", "30 + 1 = 31", "31")),
    b("Another way: 45 take away 13 is 32, but that count includes your friend. Take away 1 more, and again we get 31.",
      w("l9", "45 − 13 = 32"), w("l10", "32 − 1 = 31")),
    b("Change both places so they are counted from the same end. Then count only the places strictly between."),
]


# ── EXT_G4_WS2_CH15_002 ──────────────────────────────────────────────────────
L["EXT_G4_WS2_CH15_002"] = [
    b("A magic square has top row 4, 3, 8 and middle row 9, 5, 1. The bottom row is empty. When we finish it, which number will not be used?",
      g("l1", "Top: 4, 3, 8.  Middle: 9, 5, 1.  Bottom: ?", True), fig("f1", qfig(TOPIC, "EXT_G4_WS2_CH15_002"))),
    b("The top row is full, so add it. 4 plus 3 plus 8 is 15. Every line must add up to 15.", w("l2", "4 + 3 + 8 = 15")),
    b("The first column already has 4 and 9. What goes below them?",
      ask=ch("2", ["13", "6"], "4 plus 9 is 13. To reach 15 we need 2 more.")),
    b("First column: 15 take away 4 and 9 leaves 2. Second column: take away 3 and 5, which leaves 7. Third column: take away 8 and 1, which leaves 6.",
      w("l3", "15 − 4 − 9 = 2"), w("l4", "15 − 3 − 5 = 7"), w("l5", "15 − 8 − 1 = 6")),
    b("So the bottom row is 2, 7, 6. Check it: 2 plus 7 plus 6 is 15 as well.",
      tbl("f2", [["4", "3", "8"], ["9", "5", "1"], ["2", "7", "6"]], "Every line adds up to 15"), w("l6", "2 + 7 + 6 = 15")),
    b("Look at the finished square. Which numbers does it use?",
      ask=ch("1 to 9, once each", ["only even numbers", "some numbers twice"],
             "Read them off: 4, 3, 8, 9, 5, 1, 2, 7, 6. That is every number from 1 to 9, once each.")),
    b("The square uses only 1 to 9. So 3, 6 and 9 are all in it. The number that is not used is 11.",
      ans("l7", "11 is not used", "11", True)),
    b("Finish the square first, using the magic total. Then the question about which numbers are used answers itself."),
]
