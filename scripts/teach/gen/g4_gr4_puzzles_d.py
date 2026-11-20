"""gr4_puzzles lessons written one by one: Q_CH15_001 to Q_CH15_025 and Q_CH16_019."""
from g4_gr4_sequences_lib import ans, b, ch, fig, g, grp, lab, mk, nt, qfig, ring, tbl, w

L = {}
TOPIC = "gr4_puzzles"


def magic19(fig_id="m19"):
    """The magic square made from 1 to 9: every line adds up to 15."""
    return tbl(fig_id, [["2", "7", "6"], ["9", "5", "1"], ["4", "3", "8"]], "A magic square made from 1 to 9")


# ── Q_CH15_001 ───────────────────────────────────────────────────────────────
L["Q_CH15_001"] = [
    b("What makes a square of numbers magic? Let's look at a real 3 by 3 magic square and find out.",
      g("l1", "In a 3 × 3 magic square, the sums are ... ?", True), magic19()),
    b("Add each row. 2 plus 7 plus 6 is 15. 9 plus 5 plus 1 is 15. 4 plus 3 plus 8 is 15.",
      w("l2", "2 + 7 + 6 = 15"), w("l3", "9 + 5 + 1 = 15"), w("l4", "4 + 3 + 8 = 15")),
    b("Now add the first column: 2 plus 9 plus 4. What do you expect?",
      ask=ch("15 again", ["a bigger number", "a smaller number"], "2 plus 9 plus 4 also makes 15. The same as the rows.")),
    b("The column makes 15 too. And the diagonals: 2 plus 5 plus 8 is 15, and 6 plus 5 plus 4 is 15.",
      w("l5", "2 + 9 + 4 = 15"), w("l6", "2 + 5 + 8 = 15"), w("l7", "6 + 5 + 4 = 15")),
    b("Every row, every column and both diagonals give the same sum. That is the magic."),
    b("Careful: 15 is the sum only for this square, built from 1 to 9. Another magic square can have a different sum. What never changes is that the sums match."),
    b("So in a magic square, the sums of the rows, columns and diagonals are equal.", ans("l8", "The sums are equal", None, True)),
]


# ── Q_CH15_002 ───────────────────────────────────────────────────────────────
L["Q_CH15_002"] = [
    b("The magic constant is the sum of each row. How is it tied to the number in the central box? Let's test with a square we know.",
      g("l1", "Magic constant = ? × central box number", True), magic19()),
    b("Add a row: 2 plus 7 plus 6 is 15. So the magic constant here is 15. And the central box holds 5.",
      w("l2", "2 + 7 + 6 = 15"), lab("l3", "centre: 5")),
    b("Look at 15 and 5. How do you get 15 from 5?",
      ask=ch("3 × 5", ["2 × 5", "9 × 5"], "2 times 5 is only 10. 3 times 5 is 15. So the constant is 3 times the centre.")),
    b("15 is 3 times 5. And that makes sense: a row has 3 boxes, and the centre number is the fair share for each box.",
      w("l4", "3 × 5 = 15")),
    b("One square is not proof, so test another. In this magic square the centre is 6, and the top row is 9 plus 2 plus 7, which is 18. And 3 times 6 is 18.",
      tbl("f2", [["9", "2", "7"], ["4", "6", "8"], ["5", "10", "3"]], "Another magic square"),
      w("l5", "9 + 2 + 7 = 18"), w("l6", "3 × 6 = 18")),
    b("It works again. So the magic constant equals 3 times the central box number.",
      ans("l7", "Magic constant = 3 × central box number", None, True)),
    b("Careful: 9 times the centre gives the sum of all nine boxes. One row is only 3 times the centre."),
    b("To discover a rule, test it on an example you know well. Then test it once more on a different one."),
]


# ── Q_CH15_003 ───────────────────────────────────────────────────────────────
L["Q_CH15_003"] = [
    b("This time we add all nine numbers of a 3 by 3 magic square. How is that total tied to the central box? Let's test with a square we know.",
      g("l1", "Sum of all nine numbers = ? × central box number", True), magic19()),
    b("This square has three rows, and each row adds up to 15. So all nine numbers add up to 15 plus 15 plus 15, which is 45.",
      w("l2", "15 + 15 + 15 = 45")),
    b("The centre is 5. So 45 is how many times the centre?",
      ask=ch("9 times", ["3 times", "6 times"], "9 times 5 is 45. 3 times 5 is only 15, and that is just one row.")),
    b("9 times 5 is 45. So here the sum of all nine numbers is 9 times the centre.", w("l3", "9 × 5 = 45")),
    b("Here is why it always works. One row adds up to 3 times the centre. There are 3 rows. And 3 times 3 is 9.",
      lab("l4", "one row = 3 × centre"), lab("l5", "three rows = 3 × 3 × centre"), w("l6", "3 × 3 = 9")),
    b("So the sum of all nine numbers equals 9 times the central box number.",
      ans("l7", "Sum of all nine = 9 × central box number", None, True)),
    b("The trap is to stop at 3 times the centre. That is one row only. The question asks for all nine numbers, which is three rows."),
]


# ── Q_CH15_004 ───────────────────────────────────────────────────────────────
L["Q_CH15_004"] = [
    b("This magic square hides two letters, A and B. Every row, column and diagonal adds up to the same total. Let's find both.",
      g("l1", "Magic square.  Find A and B.", True), fig("f1", qfig(TOPIC, "Q_CH15_004"))),
    b("First we need the magic total. Which row can give it to us?",
      ask=ch("the top row: 9, 15, 6", ["the middle row", "the bottom row"],
             "The middle row hides A and the bottom row hides B. The top row is complete.")),
    b("9 plus 15 plus 6 is 30. So every line adds up to 30.", w("l2", "9 + 15 + 6 = 30")),
    b("The middle row is A, 10 and 13. 10 plus 13 is 23, and 30 take away 23 is 7. So A is 7.",
      w("l3", "10 + 13 = 23"), w("l4", "30 − 23 = 7"), lab("l5", "A = 7")),
    b("The bottom row is 14, 5 and B. So what is B?",
      ask=ch("11", ["12", "7"], "Add 14 and 5 first. Then see how many more are needed to reach 30.")),
    b("14 plus 5 is 19, and 30 take away 19 is 11. So B is 11.",
      w("l6", "14 + 5 = 19"), w("l7", "30 − 19 = 11"), lab("l8", "B = 11")),
    b("Check A with the first column: 9 plus 7 plus 14 is 30. It works.", w("l9", "9 + 7 + 14 = 30")),
    b("So A is 7 and B is 11. Careful not to swap them: A sits in the row with 10 and 13.",
      ans("l10", "A = 7, B = 11", None, True)),
    b("Find the magic total from a full line. Then each letter is the total, take away the other two numbers in its line."),
]


# ── Q_CH15_006 ───────────────────────────────────────────────────────────────
L["Q_CH15_006"] = [
    b("A magic square has 4 and 8 in the top corners and 5 in the centre. When it is finished, which of the four choices will not be in it?",
      g("l1", "Top row: 4, ?, 8.   Centre: 5.", True), fig("f1", qfig(TOPIC, "Q_CH15_006"))),
    b("We have no complete line. Can we still find the magic total?",
      ask=ch("yes: 3 times the centre", ["no, we need a full row", "yes: 4 plus 8"],
             "In a 3 by 3 magic square, every line adds up to 3 times the centre number.")),
    b("3 times 5 is 15. So every row, column and diagonal adds up to 15.", w("l2", "3 × 5 = 15")),
    b("Top row: 4 plus 8 is 12, so the box between them is 15 take away 12, which is 3.",
      w("l3", "4 + 8 = 12"), w("l4", "15 − 12 = 3")),
    b("Every line through the centre already has the 5. So its two ends must add up to 10. Opposite 4 goes 6. Opposite 8 goes 2. Opposite 3 goes 7.",
      w("l5", "15 − 5 = 10"), w("l6", "4 + 6 = 10"), w("l7", "8 + 2 = 10"), w("l8", "3 + 7 = 10")),
    b("So the bottom row is 2, 7, 6. Two boxes are left, both in the middle row.",
      tbl("f2", [["4", "3", "8"], ["?", "5", "?"], ["2", "7", "6"]], "Every line adds up to 15")),
    b("First column: 4 and 2 are there, so the middle box is 9. Last column: 8 and 6 are there, so the middle box is 1.",
      w("l9", "15 − 4 − 2 = 9"), w("l10", "15 − 8 − 6 = 1")),
    b("The finished square uses 1, 2, 3, 4, 5, 6, 7, 8 and 9. Every box was forced by the total of 15, so nothing bigger than 9 can fit.",
      tbl("f3", [["4", "3", "8"], ["9", "5", "1"], ["2", "7", "6"]], "The finished square")),
    b("So 3, 6 and 9 are all used. The number that is not used is 11.", ans("l11", "11 is not used", "11", True)),
    b("The key idea: once you know the centre, you know the total. And once you know the total, every box is fixed."),
]


# ── Q_CH15_007 ───────────────────────────────────────────────────────────────
L["Q_CH15_007"] = [
    b("The nine numbers from 3 to 11 are put into a magic square. Which of them goes in the central box?",
      g("l1", "Numbers 3 to 11 in a magic square.  Centre = ?", True), fig("f1", qfig(TOPIC, "Q_CH15_007"))),
    b("Write the nine numbers in order: 3, 4, 5, 6, 7, 8, 9, 10, 11.", lab("l2", "3, 4, 5, 6, 7, 8, 9, 10, 11")),
    b("The centre of a magic square holds a special one of these numbers. Which one?",
      ask=ch("the middle number", ["the biggest number", "the smallest number"],
             "The centre sits in four lines at once. So it must be the fair, middle-sized number, not the biggest or the smallest.")),
    b("The middle number has four numbers before it and four after it. That is 7.",
      mk("l2", "7", "circle"), grp("l2", ["3", "4", "5", "6"], "four before"), grp("l2", ["8", "9", "10", "11"], "four after")),
    b("Let's check with the totals. Pair the ends: 3 and 11 make 14, and so do 4 and 10. 4 pairs of 14 make 56, and the 7 in the middle brings it to 63.",
      w("l3", "3 + 11 = 14"), w("l4", "4 × 14 = 56"), w("l5", "56 + 7 = 63")),
    b("Three rows share the 63, so each row adds up to 21. And the centre is a row total divided by 3. 21 divided by 3 is 7. It agrees.",
      w("l6", "63 ÷ 3 = 21"), w("l7", "21 ÷ 3 = 7")),
    b("So the number in the central box is 7.", ans("l8", "Centre = 7", None, True)),
    b("When a magic square is made from nine numbers in a row, the middle number of the list always sits in the centre."),
]


# ── Q_CH15_008 ───────────────────────────────────────────────────────────────
L["Q_CH15_008"] = [
    b("A 3 by 3 magic square has 8 in the centre. We must find its magic constant, the total of each line.",
      g("l1", "Centre: 8.   Magic constant = ?", True), fig("f1", qfig(TOPIC, "Q_CH15_008"))),
    b("Think of the magic square made from 1 to 9. Its centre is 5 and every line adds up to 15. And 15 is 3 times 5.",
      magic19(), w("l2", "3 × 5 = 15")),
    b("That rule holds for every 3 by 3 magic square. So with 8 in the centre, what do we work out?",
      ask=ch("3 × 8", ["2 × 8", "9 × 8"], "The magic constant is 3 times the centre, because a line has 3 boxes. So it is 3 times 8.")),
    b("3 times 8 is 24. So the magic constant is 24.", ans("l3", "3 × 8 = 24", "24")),
    b("Here is one magic square with 8 in the centre. 5 plus 10 plus 9 is 24, and every other line makes 24 as well.",
      tbl("f2", [["5", "10", "9"], ["12", "8", "4"], ["7", "6", "11"]], "Every line adds up to 24"), w("l4", "5 + 10 + 9 = 24")),
    b("Careful: 9 times 8 would be the sum of all nine boxes. One line is only 3 times the centre."),
    b("So remember: in a 3 by 3 magic square, the magic constant is always 3 times the number in the centre."),
]


# ── Q_CH15_009 ───────────────────────────────────────────────────────────────
L["Q_CH15_009"] = [
    b("This magic square has fractions in it. Every row, column and diagonal adds up to the same total. We must find the number in the middle.",
      g("l1", "Magic square with fractions. Find the ?", True), fig("f1", qfig(TOPIC, "Q_CH15_009"))),
    b("The top row is complete: 2, 7 thirds and 2 thirds. To add them, turn everything into thirds. 2 wholes is 6 thirds.",
      w("l2", "2 = 6/3")),
    b("6 thirds plus 7 thirds plus 2 thirds is 15 thirds.", w("l3", "6/3 + 7/3 + 2/3 = 15/3")),
    b("15 thirds. What is that as a whole number?",
      ask=ch("5", ["15", "45"], "3 thirds make 1 whole. So 15 thirds is 15 divided by 3, which is 5.")),
    b("So every line adds up to 5. Now the middle row: 1 third, the gap, and 3. Write 3 as 9 thirds. 1 third plus 9 thirds is 10 thirds.",
      w("l4", "15/3 = 5"), w("l5", "3 = 9/3"), w("l6", "1/3 + 9/3 = 10/3")),
    b("The row must reach 15 thirds, and we have 10 thirds. How much more do we need?",
      ask=ch("5/3", ["5", "25/3"], "15 thirds take away 10 thirds leaves 5 thirds.")),
    b("15 thirds take away 10 thirds is 5 thirds. So the missing number is 5 thirds.",
      w("l7", "15/3 − 10/3 = 5/3", "answer"), ring("l7", "5/3", 2)),
    b("Careful: 5 is the total of each line. The missing number is 5 thirds, which is much smaller."),
    b("Check with the middle column: 7 thirds plus 5 thirds plus 1 whole is 15 thirds. With fractions, put everything in the same parts first.",
      w("l8", "7/3 + 5/3 + 3/3 = 15/3")),
]


# ── Q_CH15_010 ───────────────────────────────────────────────────────────────
L["Q_CH15_010"] = [
    b("In this square every row, column and diagonal has the same sum. Three letters are hiding: X, Y and Z. We want all three added together.",
      g("l1", "Equal sums.  X + Y + Z = ?", True), fig("f1", qfig(TOPIC, "Q_CH15_010"))),
    b("We need the magic sum first. Which line is complete?",
      ask=ch("the last column: 4, 15, 8", ["the top row", "the middle row"],
             "Every row has a blank box or a letter. The last column has three numbers: 4, 15 and 8.")),
    b("4 plus 15 plus 8 is 27. So every line adds up to 27.", w("l2", "4 + 15 + 8 = 27")),
    b("Y is in the centre. And the centre is always the magic sum divided by 3. 27 divided by 3 is 9. So Y is 9.",
      w("l3", "27 ÷ 3 = 9"), lab("l4", "Y = 9")),
    b("One diagonal is Z, Y and 8. We know Y is 9. So what is Z?",
      ask=ch("10", ["17", "19"], "9 plus 8 is 17. And 27 take away 17 is 10.")),
    b("9 plus 8 is 17, and 27 take away 17 is 10. So Z is 10.",
      w("l5", "9 + 8 = 17"), w("l6", "27 − 17 = 10"), lab("l7", "Z = 10")),
    b("The other diagonal is 4, Y and X. 4 plus 9 is 13, and 27 take away 13 is 14. So X is 14.",
      w("l8", "4 + 9 = 13"), w("l9", "27 − 13 = 14"), lab("l10", "X = 14")),
    b("The trap is to stop early. The question wants all three letters added: 14 plus 9 plus 10 is 33.",
      ans("l11", "14 + 9 + 10 = 33", "33")),
    b("Here is the whole square. Every line makes 27. Find the sum, then the centre, then use the diagonals.",
      tbl("f2", [["10", "13", "4"], ["3", "9", "15"], ["14", "5", "8"]], "Every line adds up to 27")),
]


# ── Q_CH15_011 ───────────────────────────────────────────────────────────────
L["Q_CH15_011"] = [
    b("Three columns of numbers, and one gap. Each column follows the same secret rule, going down.",
      g("l1", "Each column follows the same rule. Find the ?", True), fig("f1", qfig(TOPIC, "Q_CH15_011"))),
    b("The first column is 4, 3 and 49. The second is 6, 4 and 100. Which rule fits both?",
      ask=ch("add, then times itself", ["multiply, then add 37", "subtract, then times 49"],
             "4 plus 3 is 7, and 7 times 7 is 49. 6 plus 4 is 10, and 10 times 10 is 100.")),
    b("4 plus 3 is 7, and 7 times 7 is 49. 6 plus 4 is 10, and 10 times 10 is 100. The rule fits both columns.",
      w("l2", "4 + 3 = 7"), w("l3", "7 × 7 = 49"), w("l4", "6 + 4 = 10"), w("l5", "10 × 10 = 100")),
    b("The third column is 8, the gap, and 169. We know the bottom number this time, so we work backwards."),
    b("Which number, multiplied by itself, makes 169?",
      ask=ch("13", ["12", "14"], "Try 13. 13 times 13 is 169.")),
    b("13 times 13 is 169. So the top two numbers must add up to 13.", w("l6", "13 × 13 = 169"), w("l7", "8 + ? = 13")),
    b("8 plus what makes 13? 13 take away 8 is 5. So the missing number is 5.", ans("l8", "13 − 8 = 5", "5")),
    b("Check: 8 plus 5 is 13, and 13 times 13 is 169. Just like the other two columns.", w("l9", "8 + 5 = 13")),
    b("The key idea: test a rule on the complete columns before you use it. Then run it backwards to fill the gap."),
]


# ── Q_CH15_013 ───────────────────────────────────────────────────────────────
L["Q_CH15_013"] = [
    b("Three rows of numbers. Each row follows the same rule, and the last number of the bottom row is missing.",
      g("l1", "Each row follows the same rule. Find the ?", True), fig("f1", qfig(TOPIC, "Q_CH15_013"))),
    b("Top row: 3, 4 and 25. Here is one idea. 3 times 3, plus 4 times 4, is 25. It fits!",
      w("l2", "3 × 3 + 4 × 4 = 25")),
    b("Before we trust that rule, what must we do?",
      ask=ch("test it on the second row", ["use it on the last row", "nothing, it fits"],
             "A rule must fit every row. One row can fit just by luck.")),
    b("Second row: 5, 7 and 71. But 5 times 5, plus 7 times 7, is 74, not 71. So that rule is out. That was the trap!",
      w("l3", "5 × 5 + 7 × 7 = 74")),
    b("Try again. Multiply the first two numbers: 3 times 4 is 12. Double it to get 24. Add 1 to get 25.",
      w("l4", "3 × 4 = 12"), w("l5", "12 × 2 = 24"), w("l6", "24 + 1 = 25")),
    b("Test it on the second row. 5 times 7 is 35. Double it to get 70. Add 1 to get 71. This rule fits both rows.",
      w("l7", "5 × 7 = 35"), w("l8", "35 × 2 = 70"), w("l9", "70 + 1 = 71")),
    b("Now the last row: 6 and 8. What is the first step?",
      ask=ch("6 × 8 = 48", ["6 + 8 = 14", "6 × 6 + 8 × 8 = 100"],
             "The rule that fits both rows starts by multiplying the two numbers. 6 times 8 is 48.")),
    b("6 times 8 is 48. Double it to get 96. Add 1 to get 97. So the missing number is 97.",
      w("l10", "6 × 8 = 48"), w("l11", "48 × 2 = 96"), ans("l12", "96 + 1 = 97", "97")),
    b("A rule that fits one row is only a guess. It becomes the rule when it fits every row."),
]


# ── Q_CH15_014 ───────────────────────────────────────────────────────────────
L["Q_CH15_014"] = [
    b("These sums look silly. 5 plus 3 is not 28! So the plus sign here must be a secret code. Let's crack it.",
      g("l1", "5 + 3 = 28", True), g("l2", "9 + 1 = 810", True), g("l3", "8 + 6 = 214", True), g("l4", "5 + 4 = ?", True)),
    b("Look at 5 and 3 giving 28. Try the real sum: 5 plus 3 is 8. And try the difference: 5 take away 3 is 2.",
      w("l5", "5 − 3 = 2"), w("l6", "5 + 3 = 8")),
    b("We have a 2 and an 8. How could they make 28?",
      ask=ch("write the 2, then the 8", ["multiply 2 by 8", "add 2 and 8"],
             "Multiplying or adding 2 and 8 does not give 28. But write the 2 and then the 8 next to each other, and you see 28.")),
    b("So the code is: write the difference first, then the sum. This is the trap: 28 is not one number. It is two parts stuck together.",
      nt("l1", "28", "2 then 8")),
    b("Test it. 9 and 1: the difference is 8 and the sum is 10. That gives 8, then 10. And 8 and 6: difference 2, sum 14. That gives 2, then 14.",
      w("l7", "9 − 1 = 8"), w("l8", "9 + 1 = 10"), w("l9", "8 − 6 = 2"), w("l10", "8 + 6 = 14"),
      nt("l2", "810", "8 then 10"), nt("l3", "214", "2 then 14")),
    b("The code fits every line. Now 5 and 4. What are the difference and the sum?",
      ask=ch("1 and 9", ["9 and 1", "1 and 20"], "5 take away 4 is 1. 5 plus 4 is 9. The difference comes first, then the sum.")),
    b("The difference is 1 and the sum is 9. Write the 1, then the 9. That makes 19.",
      w("l11", "5 − 4 = 1"), w("l12", "5 + 4 = 9"), ans("l13", "19")),
    b("When sums look impossible, the signs are a code. Try the real sum, difference and product, and see how the answer is built from them."),
]


# ── Q_CH15_017 ───────────────────────────────────────────────────────────────
L["Q_CH15_017"] = [
    b("The numbers 11 to 19 fill a 3 by 3 magic square. We want the magic constant, the total of each line.",
      g("l1", "Numbers 11 to 19.  Magic constant = ?", True), fig("f1", qfig(TOPIC, "Q_CH15_017"))),
    b("Write the nine numbers in order: 11, 12, 13, 14, 15, 16, 17, 18, 19.", lab("l2", "11, 12, 13, 14, 15, 16, 17, 18, 19")),
    b("One of these goes in the centre of the square. Which one?",
      ask=ch("15, the middle number", ["19, the biggest", "11, the smallest"],
             "The centre always holds the middle number of the list. 15 has four numbers before it and four after it.")),
    b("15 goes in the centre. And the magic constant is always 3 times the centre.", mk("l2", "15", "circle")),
    b("3 times 15 is 45. So the magic constant is 45.", ans("l3", "3 × 15 = 45", "45")),
    b("Check another way. Pair the ends: 11 and 19 make 30. There are 4 pairs like that, which makes 120. The 15 in the middle brings it to 135.",
      w("l4", "11 + 19 = 30"), w("l5", "4 × 30 = 120"), w("l6", "120 + 15 = 135")),
    b("Three rows share the 135 equally. 135 divided by 3 is 45. The same answer.", w("l7", "135 ÷ 3 = 45")),
    b("The trap is to stop at 135. That is the sum of all nine numbers. One line is a third of it."),
]


# ── Q_CH15_020 ───────────────────────────────────────────────────────────────
L["Q_CH15_020"] = [
    b("Three blue balls balance two red balls. And one red ball balances three green balls. How many green balls balance the three blue ones?",
      g("l1", "3 blue = 2 red", True), g("l2", "1 red = 3 green", True), g("l3", "3 blue = ? green", True),
      fig("f1", qfig(TOPIC, "Q_CH15_020"))),
    b("Blue and green are never compared directly. Red is the bridge between them. So let's swap the reds for greens."),
    b("3 blues are worth 2 reds. Each red is worth 3 greens. So what are 2 reds worth?",
      ask=ch("6 greens", ["3 greens", "9 greens"], "One red is 3 greens. So two reds are 3 greens, and 3 greens more.")),
    b("2 reds are 2 lots of 3 greens. 2 times 3 is 6.", w("l4", "2 × 3 = 6"), lab("l5", "2 red = 6 green")),
    b("So 3 blues balance 2 reds, and 2 reds balance 6 greens. That means 3 blues balance 6 greens.",
      ans("l6", "3 blue = 6 green", None, True)),
    b("The slip is to multiply the 3 blues by the 3 greens and say 9. But the 3 greens belong to each red, and there are only 2 reds."),
    b("When two things are not compared directly, find the thing that links them, and swap it for its equal."),
]


# ── Q_CH15_021 ───────────────────────────────────────────────────────────────
L["Q_CH15_021"] = [
    b("All nine numbers in a 3 by 3 magic square add up to 72. What is the number in the centre?",
      g("l1", "All nine numbers add up to 72.  Centre = ?", True), fig("f1", qfig(TOPIC, "Q_CH15_021"))),
    b("The square has 3 rows, and in a magic square the rows have equal sums. So how do we find the sum of one row?",
      ask=ch("72 ÷ 3", ["72 − 3", "72 ÷ 2"], "The 3 rows have equal sums and share the 72. So one row is 72 divided by 3.")),
    b("Split 72 into 60 and 12. 60 divided by 3 is 20, and 12 divided by 3 is 4. So each row adds up to 24.",
      w("l2", "60 ÷ 3 = 20"), w("l3", "12 ÷ 3 = 4"), w("l4", "72 ÷ 3 = 24")),
    b("Now, the centre. What part of a row total is the centre number?",
      ask=ch("one third", ["one half", "all of it"], "A row total is always 3 times the centre. So the centre is one third of the row total.")),
    b("24 divided by 3 is 8. So the centre number is 8.", ans("l5", "24 ÷ 3 = 8", "8")),
    b("Careful: 24 is the sum of one row, not the centre. We had to divide by 3 twice."),
    b("Check: all nine boxes add up to 9 times the centre, and 9 times 8 is 72. So you could also divide 72 by 9 straight away.",
      w("l6", "9 × 8 = 72")),
]


# ── Q_CH15_022 ───────────────────────────────────────────────────────────────
L["Q_CH15_022"] = [
    b("A cross has 5 in the centre. The numbers 1, 3, 7 and 9 go at the four ends, so that both lines through the centre have the same sum. Which number is opposite 1?",
      g("l1", "Cross: 5 in the centre.  Ends: 1, 3, 7, 9.", True), g("l2", "Both lines have the same sum.  Opposite 1 = ?", True),
      fig("f1", qfig(TOPIC, "Q_CH15_022"))),
    b("Each line is one end, the 5, and the opposite end. Both lines share the 5. So the two ends of one line must add up to the same as the two ends of the other."),
    b("So split 1, 3, 7 and 9 into two pairs with equal sums. Which pairs?",
      ask=ch("1 + 9 and 3 + 7", ["1 + 3 and 7 + 9", "1 + 7 and 3 + 9"],
             "1 plus 9 is 10, and 3 plus 7 is 10. Those are the two equal pairs.")),
    b("1 plus 9 is 10, and 3 plus 7 is 10. So 1 and 9 sit at the two ends of one line.",
      w("l3", "1 + 9 = 10"), w("l4", "3 + 7 = 10")),
    b("One line is 1, 5, 9, and the other is 3, 5, 7. Both add up to 15.",
      w("l5", "1 + 5 + 9 = 15"), w("l6", "3 + 5 + 7 = 15"),
      tbl("f2", [["·", "1", "·"], ["3", "5", "7"], ["·", "9", "·"]], "Both lines add up to 15")),
    b("So the number opposite 1 is 9.", ans("l7", "Opposite 1: 9", None, True)),
    b("When two lines share a middle number, forget the middle. Just make the ends of each line add up to the same amount."),
]


# ── Q_CH15_023 ───────────────────────────────────────────────────────────────
L["Q_CH15_023"] = [
    b("A magic square has 6, 15 and 3 in its first row. We want two things: the magic constant, and the number in the centre.",
      g("l1", "First row: 6, 15, 3.", True), g("l2", "Magic constant = ?   Centre = ?", True), fig("f1", qfig(TOPIC, "Q_CH15_023"))),
    b("The magic constant is the sum of any row. Add the first row: 6 plus 15 plus 3 is 24.", w("l3", "6 + 15 + 3 = 24")),
    b("Now the centre. How do we get it from the magic constant, 24?",
      ask=ch("24 ÷ 3", ["24 ÷ 2", "pick a number from the first row"],
             "The magic constant is always 3 times the centre. So the centre is the constant divided by 3.")),
    b("24 divided by 3 is 8. So the centre is 8.", w("l4", "24 ÷ 3 = 8")),
    b("Here is the trap. The centre is a new number. It is not 6, 15 or 3 from the first row, and it is not 24 itself."),
    b("So the constant is 24 and the centre is 8.", ans("l5", "Constant = 24, Centre = 8", None, True)),
    b("Here is the finished square, with 8 in the centre. Every row, column and diagonal makes 24.",
      tbl("f2", [["6", "15", "3"], ["5", "8", "11"], ["13", "1", "10"]], "Every line adds up to 24")),
    b("One full row gives you the magic constant. Divide that by 3 and you have the centre."),
]


# ── Q_CH15_024 ───────────────────────────────────────────────────────────────
L["Q_CH15_024"] = [
    b("A, B and C are three numbers. We know them only in pairs: A plus B is 10, B plus C is 15, and A plus C is 11. We want all three added together.",
      g("l1", "A + B = 10", True), g("l2", "B + C = 15", True), g("l3", "A + C = 11", True), g("l4", "A + B + C = ?", True)),
    b("We can't see any single letter. So let's add all three sums together: 10 plus 15 plus 11 is 36.",
      w("l5", "10 + 15 + 11 = 36")),
    b("In that total of 36, how many times is each letter counted?",
      ask=ch("twice", ["once", "three times"],
             "A is in the first sum and the third. B is in the first and the second. C is in the second and the third. Each letter appears twice.")),
    b("So 36 is two lots of A plus B plus C. Every letter was counted twice.", lab("l6", "A + B + B + C + A + C = 36")),
    b("So halve it. Half of 36 is 18. The trap is to stop at 36, which counts every letter twice.",
      ans("l7", "36 ÷ 2 = 18", "18")),
    b("Check. C is 18 take away 10, which is 8. A is 18 take away 15, which is 3. B is 18 take away 11, which is 7. And 3 plus 7 is 10, as the first clue says.",
      w("l8", "18 − 10 = 8"), w("l9", "18 − 15 = 3"), w("l10", "18 − 11 = 7"), w("l11", "3 + 7 = 10")),
    b("So A plus B plus C is 18. When you only know things in pairs, add all the pairs and see how many times each one was counted."),
]


# ── Q_CH15_025 ───────────────────────────────────────────────────────────────
L["Q_CH15_025"] = [
    b("Rohan makes a 3 by 3 magic square from 9 odd numbers in a row, starting from 5. Which number goes in the centre?",
      g("l1", "9 odd numbers in a row, starting from 5.  Centre = ?", True)),
    b("Odd numbers go up in 2s. Starting from 5, the nine of them are 5, 7, 9, 11, 13, 15, 17, 19 and 21.",
      lab("l2", "5, 7, 9, 11, 13, 15, 17, 19, 21")),
    b("The centre of the magic square holds the middle number of this list. Which is it?",
      ask=ch("13", ["11", "15"],
             "The middle of nine numbers is the 5th one, with four before it and four after it. Count along: 5, 7, 9, 11, and then 13.")),
    b("The 5th number is 13. It has four numbers before it and four after it.",
      mk("l2", "13", "circle"), grp("l2", ["5", "7", "9", "11"], "four before"), grp("l2", ["15", "17", "19", "21"], "four after")),
    b("Check. The magic constant would be 3 times 13, which is 39. And the smallest, middle and largest numbers do add up to 39.",
      w("l3", "3 × 13 = 39"), w("l4", "5 + 13 + 21 = 39")),
    b("So the number in the centre is 13.", ans("l5", "Centre = 13", None, True)),
    b("Careful: 9 is how many numbers there are, not the answer. Write the list out and find the one in the middle."),
]


# ── Q_CH16_019 ───────────────────────────────────────────────────────────────
L["Q_CH16_019"] = [
    b("Each letter is worth its place in the alphabet: A is 1, B is 2, C is 3, and so on. We want the letters of the word MATH added up.",
      g("l1", "A = 1, B = 2, C = 3, ...   M + A + T + H = ?", True), fig("f1", qfig(TOPIC, "Q_CH16_019"))),
    b("Count along the alphabet. A is 1. H is the 8th letter. Keep going to 10 for J, and M is the 13th letter.",
      lab("l2", "A B C D E F G H I J K L M"), lab("l3", "A = 1,  H = 8,  M = 13")),
    b("T comes later. After M come N, O, P, Q, R and S, which are 14, 15, 16, 17, 18 and 19. So what is T?",
      lab("l4", "N 14,  O 15,  P 16,  Q 17,  R 18,  S 19"),
      ask=ch("20", ["19", "21"], "S is 19, and T comes straight after S. So T is 20.")),
    b("T is the 20th letter. So the four letters are worth 13, 1, 20 and 8.", lab("l5", "M = 13,  A = 1,  T = 20,  H = 8")),
    b("Now add them. 13 plus 1 is 14. Add 20 to get 34. Add 8 to get 42.",
      w("l6", "13 + 1 = 14"), w("l7", "14 + 20 = 34"), w("l8", "34 + 8 = 42")),
    b("So the letters of MATH add up to 42.", ans("l9", "13 + 1 + 20 + 8 = 42", "42")),
    b("It is easy to be one place out when counting letters. Two handy markers: J is the 10th letter and T is the 20th."),
]
