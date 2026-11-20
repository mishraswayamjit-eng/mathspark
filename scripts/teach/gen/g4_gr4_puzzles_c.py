"""gr4_puzzles lessons written one by one: G4A_PUZZLES_014 to G4A_PUZZLES_025 and
the previous-year questions PYQ_2018_Q24, PYQ_2018_Q33, PYQ_2019_Q31.
"""
from g4_gr4_puzzles_a import product_puzzle
from g4_gr4_sequences_lib import ans, b, ch, fig, g, lab, mk, nt, qfig, st, tbl, w

L = {}
TOPIC = "gr4_puzzles"


# ── G4A_PUZZLES_014 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_014"] = [
    b("A number riddle with three clues. It is a 2-digit number less than 50. It is a multiple of 7. And its digits add up to 6.",
      g("l1", "2-digit, less than 50, multiple of 7", True), g("l2", "digits add up to 6", True)),
    b("Start with the clue that leaves the fewest numbers. The 2-digit multiples of 7 below 50 are 14, 21, 28, 35, 42 and 49.",
      lab("l3", "14, 21, 28, 35, 42, 49")),
    b("Now the last clue. Which of these has digits that add up to 6?",
      ask=ch("42", ["35", "21"], "4 plus 2 is 6. Check the others: 3 plus 5 is 8, and 2 plus 1 is 3.")),
    b("Add the digits of each. 14 gives 5. 21 gives 3. 28 gives 10. 35 gives 8. 42 gives 6. 49 gives 13.",
      tbl("f1", [["14", "21", "28", "35", "42"], ["5", "3", "10", "8", "6"]], "Top: the multiple of 7. Below: its digits added"),
      lab("l4", "49: 4 + 9 = 13")),
    b("Only 42 has digits that add up to 6. So the number is 42.", mk("l3", "42", "circle"), ans("l5", "42")),
    b("Careful: 24 also has digits that add up to 6. But 24 is not in the 7 times table. 42 is, because 7 times 6 is 42.",
      lab("l6", "24 is not a multiple of 7"), w("l7", "7 × 6 = 42")),
    b("With several clues, list the numbers that fit one clue. Then let the other clues cross numbers off."),
]


# ── G4A_PUZZLES_015 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_015"] = [
    b("A pencil and an eraser cost 12 rupees together. Two pencils and an eraser cost 19 rupees. How much is the eraser?",
      g("l1", "pencil + eraser = ₹12", True), g("l2", "2 pencils + eraser = ₹19", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_015"))),
    b("Compare the two purchases. What extra thing is in the second one?",
      ask=ch("1 more pencil", ["1 more eraser", "nothing extra"],
             "Both have an eraser. The first has 1 pencil and the second has 2. So the only extra is 1 pencil.")),
    b("The only difference is 1 extra pencil, and the price went up from 12 to 19. So a pencil costs 7 rupees.",
      w("l3", "19 − 12 = 7"), lab("l4", "pencil = ₹7")),
    b("A pencil and an eraser cost 12 rupees together, and the pencil is 7. So what do we work out for the eraser?",
      ask=ch("12 − 7", ["12 ÷ 2", "19 − 7"],
             "The pencil and the eraser together make 12. Take the pencil's 7 away, and the eraser is left.")),
    b("12 take away 7 is 5. So the eraser costs 5 rupees.", w("l5", "12 − 7 = 5"), ans("l6", "eraser = ₹5", None, True)),
    b("Check both purchases. 7 plus 5 is 12. And 7 plus 7 plus 5 is 19. Both fit.",
      w("l7", "7 + 5 = 12"), w("l8", "7 + 7 + 5 = 19")),
    b("When two purchases are nearly the same, look at what is different. The difference in price belongs to the extra thing."),
]


# ── G4A_PUZZLES_016 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_016"] = [
    b("R is a hidden digit in the three-digit number 2 R 5. When that number is multiplied by 3, the answer is 735.",
      g("l1", "2R5 × 3 = 735", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_016"))),
    b("Some number times 3 gives 735. How do we find that number?",
      ask=ch("735 ÷ 3", ["735 × 3", "735 − 3"], "Dividing undoes multiplying. So divide 735 by 3.")),
    b("Split 735 into 600 and 135. 600 divided by 3 is 200. 135 divided by 3 is 45. So the number is 245.",
      w("l2", "735 = 600 + 135"), w("l3", "600 ÷ 3 = 200"), w("l4", "135 ÷ 3 = 45"), w("l5", "735 ÷ 3 = 245")),
    b("So 2 R 5 is 245. Which digit is R?",
      ask=ch("4", ["2", "5"], "R is the middle digit, in the tens place. The tens digit of 245 is 4.")),
    b("R is in the tens place, and the tens digit of 245 is 4. So R is 4.",
      lab("l6", "2R5 = 245"), ans("l7", "R = 4", None, True)),
    b("Check: 245 times 3. 200 threes are 600 and 45 threes are 135. Together that is 735. It works.",
      w("l8", "245 × 3 = 735")),
    b("To find a hidden digit, find the whole number first by undoing the sum. Then pick out the digit in the right place."),
]


# ── G4A_PUZZLES_017 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_017"] = [
    b("Five children ran a race. We have three clues about the order they finished in. Who came second?",
      g("l1", "Dev: after Farah, before Esha", True), g("l2", "Hari: between Dev and Esha", True), g("l3", "Gita: last.   Who was 2nd?", True)),
    b("Take the first clue. Dev finished after Farah but before Esha. So the order is Farah, then Dev, then Esha.",
      lab("l4", "Farah, Dev, Esha")),
    b("Now the second clue. Hari finished between Dev and Esha. What is the order now?",
      ask=ch("Farah, Dev, Hari, Esha", ["Farah, Hari, Dev, Esha", "Farah, Dev, Esha, Hari"],
             "Between Dev and Esha means after Dev and before Esha. So Hari slots in right there.")),
    b("Hari slots in between Dev and Esha: Farah, Dev, Hari, Esha.", lab("l5", "Farah, Dev, Hari, Esha")),
    b("Gita finished last. So the full order is Farah, Dev, Hari, Esha, Gita.", lab("l6", "Farah, Dev, Hari, Esha, Gita")),
    b("Now count from the front. Farah is 1st, and Dev is 2nd.",
      nt("l6", "Farah", "1st"), nt("l6", "Dev", "2nd"), ans("l7", "2nd: Dev", None, True)),
    b("For an order puzzle, write the names in a line and slot each new clue into it. Then just read off the place you want."),
]


# ── G4A_PUZZLES_018 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_018"] = [
    b("On a dice, opposite faces always add up to 7. Neha can see the faces 1, 2 and 3. What do the three hidden faces add up to?",
      g("l1", "Opposite faces add up to 7.  She sees 1, 2, 3.", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_018"))),
    b("Each hidden face is opposite a face she can see. Which face is opposite the 1?",
      ask=ch("6", ["7", "1"], "The two opposite faces add up to 7. 1 plus what makes 7? It is 6.")),
    b("Opposite 1 is 6. Opposite 2 is 5. Opposite 3 is 4.",
      w("l2", "7 − 1 = 6"), w("l3", "7 − 2 = 5"), w("l4", "7 − 3 = 4")),
    b("Now add the hidden faces. 6 plus 5 plus 4 is 15.", ans("l5", "6 + 5 + 4 = 15", "15")),
    b("Here is another way to check. All six faces add up to 21. The faces she sees add up to 6. And 21 take away 6 is 15.",
      w("l6", "1 + 2 + 3 + 4 + 5 + 6 = 21"), w("l7", "1 + 2 + 3 = 6"), w("l8", "21 − 6 = 15")),
    b("The slip here is to add the faces she can see. Read the question: we want the faces she cannot see."),
    b("So the hidden faces total 15. Use the rule to find each hidden face, then add them up."),
]


# ── G4A_PUZZLES_019 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_019"] = [
    b("A magic square with many blank boxes. Every row, column and diagonal has the same total. We must find Q.",
      g("l1", "Magic square.  Q = ?", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_019"))),
    b("We need the magic total, so we need one complete line. Which line is complete?",
      ask=ch("the diagonal 9, 11, 13", ["Row 1", "Row 3"],
             "Row 1 hides P, and Row 3 has a blank and Q. But the diagonal from 9 down to 13 has all three numbers.")),
    b("9 plus 11 plus 13 is 33. So every line adds up to 33.", w("l2", "9 + 11 + 13 = 33")),
    b("Row 1 is P, 16 and 9. 16 plus 9 is 25, and 33 take away 25 is 8. So P is 8.",
      w("l3", "16 + 9 = 25"), w("l4", "33 − 25 = 8"), lab("l5", "P = 8")),
    b("Now we want Q. Which line holds Q and two numbers we know?",
      ask=ch("the diagonal P, 11, Q", ["Row 3", "the last column"],
             "Row 3 and the last column each have a blank box as well as Q. The diagonal from P to Q is missing only Q.")),
    b("The diagonal is 8, 11 and Q. 8 plus 11 is 19, and 33 take away 19 is 14. So Q is 14.",
      w("l6", "8 + 11 = 19"), w("l7", "33 − 19 = 14"), ans("l8", "Q = 14", None, True)),
    b("Here is the whole square filled in. Every row, column and diagonal makes 33.",
      tbl("f2", [["8", "16", "9"], ["12", "11", "10"], ["13", "6", "14"]], "Every line adds up to 33")),
    b("Don't forget the diagonals! When rows and columns have too many blanks, a diagonal may be the line that helps."),
]


# ── G4A_PUZZLES_020 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_020"] = product_puzzle(
    "(□3) × (□4) = ?",
    "A two-digit number ending in 3 is multiplied by a two-digit number ending in 4. We don't know the other digits. Which choice can be the product?",
    3, 4, ["7, because 3 + 4 = 7", "4, the bigger digit"],
    [1037, 9872, 1032, 172], 1037,
    (13, 14), 172, (93, 94), 9872, 1032, (43, 24),
    ("Next, the size. What is the smallest two-digit number that ends in 3?", "13", ["03", "23"],
     "A two-digit number cannot start with 0. So the smallest one ending in 3 is 13."),
    "Check the last digit, then the smallest and largest products. Those three tests can settle a puzzle without knowing the hidden digits.")


# ── G4A_PUZZLES_021 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_021"] = [
    b("P and Q are two different digits. P plus P plus P gives the two-digit number Q P. We want P plus Q.",
      g("l1", "P + P + P = QP", True)),
    b("P plus P plus P is 3 times P. And look at the answer, Q P: its last digit is P again. So 3 times P must end in P.",
      lab("l2", "3 × P ends in the digit P"), lab("l3", "and 3 × P has two digits")),
    b("There are only nine digits to try. Here is each one, times 3.",
      tbl("f1", [["1", "2", "3", "4", "5"], ["3", "6", "9", "12", "15"]], "Top: P.   Below: 3 × P"),
      tbl("f2", [["6", "7", "8", "9"], ["18", "21", "24", "27"]], "Top: P.   Below: 3 × P")),
    b("Which answer is a two-digit number that ends in the digit we started with?",
      ask=ch("15, from P = 5", ["12, from P = 4", "18, from P = 6"],
             "15 ends in 5, and it came from 5. The others end in a digit that is different from the one we started with.")),
    b("5 plus 5 plus 5 is 15. So P is 5. And Q P is 15, so Q is 1.", w("l4", "5 + 5 + 5 = 15"), lab("l5", "P = 5,  Q = 1")),
    b("Careful with the last step. The question wants P plus Q. That is 5 plus 1, which is 6. Not 15, and not just 5.",
      ans("l6", "5 + 1 = 6", "6")),
    b("When a letter puzzle has only a few possible digits, test them all in a tidy table. Then answer exactly what was asked."),
]


# ── G4A_PUZZLES_022 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_022"] = [
    b("A 3-digit riddle. The hundreds digit is double the ones digit. The tens digit is the hundreds digit plus the ones digit. All three add up to 12.",
      g("l1", "hundreds = double the ones", True), g("l2", "tens = hundreds + ones", True), g("l3", "digits add up to 12", True)),
    b("Everything depends on the ones digit. So let's try a ones digit and build the number from it."),
    b("Try ones digit 1. The hundreds digit is double that, 2. The tens digit is 2 plus 1, which is 3. But the digits add up to only 6. Too small.",
      lab("l4", "ones 1:  hundreds 2,  tens 3"), w("l5", "2 + 3 + 1 = 6")),
    b("Try ones digit 2. The hundreds digit is double that, 4. So what is the tens digit?",
      ask=ch("6", ["8", "2"], "The tens digit is the hundreds digit plus the ones digit. That is 4 plus 2.")),
    b("The tens digit is 4 plus 2, which is 6. Now add all three digits: 4 plus 6 plus 2 is 12. Every clue fits!",
      lab("l6", "ones 2:  hundreds 4,  tens 6"), w("l7", "4 + 6 + 2 = 12")),
    b("Put the digits in their places: 4 hundreds, 6 tens, 2 ones. The number is 462.", ans("l8", "462")),
    b("Careful with the order. The same digits the other way round would not fit, because the hundreds digit must be double the ones digit."),
    b("When clues link the digits together, pick one digit to try. Build the rest from it, and test the total."),
]


# ── G4A_PUZZLES_023 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_023"] = [
    b("A farmer has hens and goats. Together they have 10 heads and 28 legs. How many goats are there?",
      g("l1", "10 heads, 28 legs.  Goats = ?", True)),
    b("10 heads means 10 animals. Here is a clever trick: pretend that all 10 are hens. Hens have 2 legs, so that would be 20 legs.",
      w("l2", "10 × 2 = 20")),
    b("But there are 28 legs, which is 8 more than 20. Where do the 8 extra legs come from?",
      w("l3", "28 − 20 = 8"),
      ask=ch("the goats: 2 extra legs each", ["some extra hens", "a counting mistake"],
             "A goat has 4 legs and a hen has 2. So every goat brings 2 more legs than we counted.")),
    b("Each goat has 2 more legs than a hen. So 8 extra legs means 8 divided by 2 goats. That is 4 goats.",
      w("l4", "4 − 2 = 2"), w("l5", "8 ÷ 2 = 4")),
    b("So the farmer has 4 goats.", ans("l6", "4 goats", None, True)),
    b("Check. 4 goats and 6 hens make 10 animals. The goats have 16 legs and the hens have 12. And 16 plus 12 is 28.",
      w("l7", "10 − 4 = 6"), w("l8", "4 × 4 = 16"), w("l9", "6 × 2 = 12"), w("l10", "16 + 12 = 28")),
    b("Careful: 6 is the number of hens. The question asks for the goats, and that is 4."),
    b("Pretend they are all the same kind, see how many legs are missing, and share the extra legs out. That trick works every time."),
]


# ── G4A_PUZZLES_024 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_024"] = [
    b("The digits of a 2-digit number add up to 9. Swap the two digits, and the new number is 27 more. What is the first number?",
      g("l1", "digits add up to 9", True), g("l2", "swap the digits: 27 more", True)),
    b("After the swap the number gets bigger. So in the first number, which digit is the smaller one?",
      ask=ch("the tens digit", ["the ones digit", "they are equal"],
             "The swap moves the ones digit into the tens place. If the number grows, the ones digit was the bigger one.")),
    b("So we want digits that add up to 9, with the smaller digit in the tens place. That gives 18, 27, 36 and 45.",
      lab("l3", "18, 27, 36, 45")),
    b("Swap the digits of each one and subtract. 81 minus 18 is 63. 72 minus 27 is 45. 63 minus 36 is 27. 54 minus 45 is 9.",
      w("l4", "81 − 18 = 63"), w("l5", "72 − 27 = 45"), w("l6", "63 − 36 = 27"), w("l7", "54 − 45 = 9")),
    b("Only one of them grows by exactly 27. It is 36, which turns into 63.", mk("l6", "27", "box"), mk("l3", "36", "circle")),
    b("So the first number is 36.", ans("l8", "36")),
    b("Careful: 63 is the number after the swap. The question asks for the first number, the smaller one."),
    b("List the numbers that fit the first clue, then test each one against the second clue. A short list makes a hard puzzle easy."),
]


# ── G4A_PUZZLES_025 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_025"] = [
    b("A laddoo is hidden in one of three boxes. Each box has a label, but only one of the three labels is true. Where is the laddoo?",
      g("l1", "Box 1 says: it is in this box", True), g("l2", "Box 2 says: it is not in this box", True),
      g("l3", "Box 3 says: it is not in Box 1", True)),
    b("We can't tell which label to trust. So let's test each box in turn, and count how many labels would be true."),
    b("Suppose it is in Box 1. Then label 1 is true. Label 2 says it is not in Box 2, and that is true as well. Does Box 1 fit?",
      ask=ch("no, 2 labels would be true", ["yes, label 1 is true"],
             "Only one label may be true. With the laddoo in Box 1, labels 1 and 2 are both true. That is one too many.")),
    b("Box 1 gives two true labels, so it is out. Now suppose it is in Box 3. Label 2 is true, and label 3 is true. Two again, so Box 3 is out.",
      lab("l4", "in Box 1: labels 1 and 2 are true"), lab("l5", "in Box 3: labels 2 and 3 are true")),
    b("Now suppose it is in Box 2. Label 1 is not true. Label 2 says it is not in this box, so that is not true either. Label 3 is true.",
      lab("l6", "in Box 2: only label 3 is true")),
    b("Exactly one true label! That is what the puzzle needs. So the laddoo is in Box 2.", ans("l7", "Box 2", None, True)),
    b("Here are all three tests side by side. Only one row has exactly one true label.",
      tbl("f1", [["Box 1", "true", "true", "not true"], ["Box 3", "not true", "true", "true"], ["Box 2", "not true", "not true", "true"]],
          "Only one label may be true", ["If it is in", "Label 1", "Label 2", "Label 3"])),
    b("When you can't trust the clues, don't guess. Test each possibility and see which one fits the rule."),
]


# ── PYQ_2018_Q24 ─────────────────────────────────────────────────────────────
L["PYQ_2018_Q24"] = [
    b("A boy has six cards: three 4s and three 9s. He uses 5 of them to make a 3-digit number and a 2-digit number. Which choice can be their difference?",
      g("l1", "Cards: 4, 4, 4, 9, 9, 9.  Use 5 cards.", True), g("l2", "3-digit number − 2-digit number = ?", True),
      g("c", "359     450     550     150", True)),
    b("Every digit is a 4 or a 9. So the ones digit of the answer comes from a 4 or a 9, take away a 4 or a 9. What can it be?",
      ask=ch("0 or 5", ["4 or 9", "any digit"],
             "4 take away 4 is 0, and 9 take away 9 is 0. 9 take away 4 is 5. So only 0 or 5 can appear.")),
    b("Equal digits leave 0. 9 take away 4 leaves 5. And 4 take away 9 borrows a ten: 14 take away 9 is 5. So the answer ends in 0 or 5.",
      w("l3", "4 − 4 = 0"), w("l4", "9 − 4 = 5"), w("l5", "14 − 9 = 5"), st("c", "359", "ends in 9")),
    b("Now the size. Suppose the 3-digit number starts with 4. The smallest difference is 444 take away 99, which is 345. The largest is 499 take away 44, which is 455.",
      w("l6", "444 − 99 = 345"), w("l7", "499 − 44 = 455")),
    b("So 150 is too small. And if the 3-digit number starts with 9, the difference is at least 944 take away 99, which is 845. 550 falls in the gap.",
      w("l8", "944 − 99 = 845"), st("c", "150", "too small"), st("c", "550", "between 455 and 845")),
    b("Only 450 is left. But can he really make it? Which of these works with his cards?",
      ask=ch("499 − 49", ["494 − 44", "449 − 99"],
             "494 take away 44 does make 450, but it needs four 4s, and he has only three. 499 take away 49 uses two 4s and three 9s.")),
    b("499 take away 49 is 450. It uses two 4s and three 9s, and he has those cards. So the difference can be 450.",
      mk("c", "450", "circle"), ans("l9", "499 − 49 = 450", "450")),
    b("When you can't try every case, test the last digit and the size. Then make sure the choice that is left can really be built."),
]


# ── PYQ_2018_Q33 ─────────────────────────────────────────────────────────────
L["PYQ_2018_Q33"] = [
    b("A palindrome reads the same backwards. A 3-digit palindrome is added to 2018, and the total is a 4-digit palindrome. We want the sum of the 3-digit number's digits.",
      g("l1", "3-digit palindrome + 2018 = 4-digit palindrome", True), g("l2", "sum of its digits = ?", True)),
    b("First, how big is the total? The smallest 3-digit palindrome is 101 and the largest is 999. So the total is between 2119 and 3017.",
      w("l3", "2018 + 101 = 2119"), w("l4", "2018 + 999 = 3017")),
    b("Could the total start with 3? The only palindrome that small is 3003. But 3003 take away 2018 is 985, and 985 is not a palindrome.",
      w("l5", "3003 − 2018 = 985")),
    b("So the total starts with 2. It is a palindrome, so it ends with 2 as well. Now, 2018 ends in 8. So what must our 3-digit number end in?",
      lab("l6", "total: 2 _ _ 2"),
      ask=ch("4", ["6", "0"], "8 plus 4 makes a number that ends in 2. So the ones digit must be 4.")),
    b("8 plus 4 is 12, which ends in 2. So our palindrome ends in 4, and it must start with 4 too. It looks like 4, something, 4.",
      w("l7", "8 + 4 = 12"), lab("l8", "palindrome: 4 ? 4")),
    b("Try the middle digit. 404 gives 2422. 414 gives 2432. 424 gives 2442. Only the last one reads the same backwards!",
      w("l9", "404 + 2018 = 2422"), w("l10", "414 + 2018 = 2432"), w("l11", "424 + 2018 = 2442"), mk("l11", "2442", "box")),
    b("So the 3-digit palindrome is 424. Its digits are 4, 2 and 4, and they add up to 10.",
      ans("l12", "4 + 2 + 4 = 10", "10")),
    b("Use the ends first. The size gave us the first digit of the total, and the ones digits gave us the last digit. Then only a few tries were left."),
]


# ── PYQ_2019_Q31 ─────────────────────────────────────────────────────────────
L["PYQ_2019_Q31"] = [
    b("In this 3 by 3 magic square, every row, column and diagonal adds up to 54. Which number can be in the central box?",
      g("l1", "3 by 3 magic square.  Every line adds up to 54.", True), g("l2", "Central box = ?", True),
      fig("f1", qfig(TOPIC, "PYQ_2019_Q31"))),
    b("Let's learn from a magic square we know well. This one uses 1 to 9. Every line adds up to 15, and the centre is 5.",
      tbl("f2", [["2", "7", "6"], ["9", "5", "1"], ["4", "3", "8"]], "Every line adds up to 15")),
    b("Look at 15 and 5. How is the centre related to the line total?",
      ask=ch("it is one third of it", ["it is half of it", "it is 10 less than it"],
             "3 times 5 is 15. So the centre is the line total divided by 3.")),
    b("15 divided by 3 is 5. And this is true for every 3 by 3 magic square: the centre is the line total divided by 3.",
      w("l3", "15 ÷ 3 = 5"), lab("l4", "centre = line total ÷ 3")),
    b("So divide 54 by 3. Split 54 into 30 and 24. 30 divided by 3 is 10, and 24 divided by 3 is 8. Together that is 18.",
      w("l5", "30 ÷ 3 = 10"), w("l6", "24 ÷ 3 = 8"), ans("l7", "54 ÷ 3 = 18", "18")),
    b("Check: three 18s make 54. So the central box holds 18.", w("l8", "18 + 18 + 18 = 54")),
    b("Careful not to halve the total. A line has 3 boxes, so the centre is one third of it, not one half."),
    b("Remember this for any 3 by 3 magic square: the line total is 3 times the centre, and the centre is the line total divided by 3."),
]
