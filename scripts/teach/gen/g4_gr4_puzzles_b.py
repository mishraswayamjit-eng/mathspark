"""gr4_puzzles lessons written one by one: G4A_PUZZLES_001 to G4A_PUZZLES_013."""
from g4_gr4_sequences_lib import ans, b, ch, fig, g, lab, mk, nt, qfig, ring, st, tbl, w

L = {}
TOPIC = "gr4_puzzles"


# ── G4A_PUZZLES_001 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_001"] = [
    b("In a magic square, every row, every column and both diagonals add up to the same total. One number in Row 3 is missing.",
      g("l1", "Magic square.  Row 3: 5, ?, 3", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_001"))),
    b("To find the missing number we need the magic total. Which line can give it to us?",
      ask=ch("a full line, like Row 1", ["Row 3", "we have to guess"],
             "Row 3 has a gap, so we cannot add it yet. Row 1 is complete: 9, 2 and 7.")),
    b("Row 1 is 9 plus 2 plus 7, which is 18. So the magic total is 18.", w("l2", "9 + 2 + 7 = 18")),
    b("Row 3 must make 18 too. It already has 5 and 3, which make 8. And 18 take away 8 is 10.",
      w("l3", "5 + 3 = 8"), w("l4", "18 − 8 = 10")),
    b("So the missing number is 10.", ans("l5", "5 + 10 + 3 = 18", "10")),
    b("Check with the middle column, which also holds the gap. 2 plus 6 plus 10 is 18. It works there too.",
      w("l6", "2 + 6 + 10 = 18")),
    b("In a magic square, find the total from any full line. Then every gap is just a subtraction."),
]


# ── G4A_PUZZLES_002 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_002"] = [
    b("A number riddle! It is a 2-digit number. Its tens digit is 4. And its two digits add up to 11.",
      g("l1", "Tens digit: 4.  The digits add up to 11.", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_002"))),
    b("The tens digit is 4, so the number is forty-something. We only need the ones digit.", lab("l2", "4 _")),
    b("The two digits add up to 11, and one of them is 4. What is the other?",
      ask=ch("7", ["1", "15"], "4 plus what makes 11? Take 4 away from 11, and 7 is left.")),
    b("11 take away 4 is 7. So the ones digit is 7.", w("l3", "11 − 4 = 7")),
    b("Tens digit 4, ones digit 7. The number is 47.", ans("l4", "47")),
    b("Careful with the order. 74 also has digits that add up to 11, but its tens digit is 7. Ours must have the 4 in the tens place.",
      lab("l5", "74: the tens digit is 7")),
    b("Check: 4 plus 7 is 11. In digit riddles, write down the place of each digit before you do anything else.",
      w("l6", "4 + 7 = 11")),
]


# ── G4A_PUZZLES_003 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_003"] = [
    b("Here P is a hidden digit. 4 P means a two-digit number: 4 tens and P ones. Careful, it does not mean 4 times P.",
      g("l1", "4P + 25 = 71", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_003"))),
    b("The number 4 P, plus 25, makes 71. How do we find the number 4 P?",
      ask=ch("71 − 25", ["71 + 25", "25 − 4"],
             "Something plus 25 gives 71. To undo the adding, take 25 away from 71.")),
    b("71 take away 25 is 46. So the number 4 P is 46.", w("l2", "71 − 25 = 46"), lab("l3", "4P = 46")),
    b("4 P is 46. So which digit is P?",
      ask=ch("6", ["4", "46"], "P sits in the ones place. The ones digit of 46 is 6.")),
    b("P is the ones digit, so P is 6.", mk("l3", "6", "circle"), ans("l4", "P = 6", None, True)),
    b("Check by putting it back. 46 plus 25 is 71. It works.", w("l5", "46 + 25 = 71")),
    b("When a letter hides a digit, find the whole number first by working backwards. Then read off the digit in the right place."),
]


# ── G4A_PUZZLES_004 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_004"] = [
    b("A picture puzzle. A star plus a star makes 14. A star plus a moon makes 10. What is the moon worth?",
      g("l1", "star + star = 14", True), g("l2", "star + moon = 10", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_004"))),
    b("Which clue should we use first?",
      ask=ch("star + star = 14", ["star + moon = 10", "it makes no difference"],
             "The first clue has only stars in it. So it can tell us what one star is worth.")),
    b("Two equal stars make 14. So one star is half of 14, which is 7.", w("l3", "14 ÷ 2 = 7"), lab("l4", "star = 7")),
    b("Now use the second clue. A star plus a moon is 10, and we know the star is 7.", lab("l5", "7 + moon = 10")),
    b("10 take away 7 is 3. So the moon is worth 3.", w("l6", "10 − 7 = 3"), ans("l7", "moon = 3", None, True)),
    b("Careful: the star and the moon are not equal, so we must not halve the 10. We use the 7 we found."),
    b("Check both clues. 7 plus 7 is 14, and 7 plus 3 is 10. Start with the clue that has only one kind of picture.",
      w("l8", "7 + 7 = 14"), w("l9", "7 + 3 = 10")),
]


# ── G4A_PUZZLES_005 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_005"] = [
    b("Four children, three clues. Amit is taller than Bina. Bina is taller than Chetan. Divya is shorter than Chetan. Who is the tallest?",
      g("l1", "Amit is taller than Bina", True), g("l2", "Bina is taller than Chetan", True), g("l3", "Divya is shorter than Chetan", True)),
    b("Let's line them up, with the tallest on the left. Clue 1 says Amit is taller than Bina. So Amit goes first.",
      lab("l4", "Amit, Bina")),
    b("Clue 2 says Bina is taller than Chetan. Where does Chetan go in our line?",
      ask=ch("after Bina", ["before Amit", "between Amit and Bina"],
             "Chetan is shorter than Bina. So he stands after her in the line.")),
    b("So far the line is Amit, Bina, Chetan.", lab("l5", "Amit, Bina, Chetan")),
    b("Careful with clue 3. It says shorter, not taller. Divya is shorter than Chetan, so she goes at the end.",
      mk("l3", "shorter", "underline"), lab("l6", "Amit, Bina, Chetan, Divya")),
    b("The tallest is at the front of the line. That is Amit.", mk("l6", "Amit", "circle"), ans("l7", "Tallest: Amit", None, True)),
    b("For puzzles like this, build one line, a clue at a time. And watch closely for the words taller and shorter."),
]


# ── G4A_PUZZLES_006 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_006"] = [
    b("In this magic square every row adds up to 21. One row has 4, 11 and a missing number.",
      g("l1", "4 + 11 + ? = 21"), fig("f1", qfig(TOPIC, "G4A_PUZZLES_006"))),
    b("Start with the two numbers we know. 4 plus 11 is 15.", w("l2", "4 + 11 = 15")),
    b("The row must reach 21, and we have 15 so far. What do we work out?",
      ask=ch("21 − 15", ["21 + 15", "15 − 4"],
             "21 is the total of the whole row. The missing number is the gap between 15 and 21.")),
    b("21 take away 15 is 6. So the missing number is 6.", ans("l3", "21 − 15 = 6", "6")),
    b("Here is the slip to watch for. The 21 is the total of the row. It is not another number to add on."),
    b("Check: 4 plus 11 plus 6 is 21. It works.", w("l4", "4 + 11 + 6 = 21")),
    b("When you know the total and all the parts but one, add the parts you know and subtract from the total."),
]


# ── G4A_PUZZLES_007 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_007"] = [
    b("Two signs have gone missing: 8, something, 4, something, 2, equals 10. We must put the right signs back.",
      g("l1", "8 __ 4 __ 2 = 10", True)),
    b("8 is already close to 10, so let's try plus first. 8 plus 4 is 12.", w("l2", "8 + 4 = 12")),
    b("Now we have 12, and we need 10. What should we do with the 2?",
      ask=ch("take it away", ["add it", "multiply by it"], "12 is 2 more than 10. So we must take the 2 away.")),
    b("12 take away 2 is 10. So the signs are plus, then minus.", ans("l3", "8 + 4 − 2 = 10")),
    b("Let's make sure nothing else works. Minus then plus gives 6. Plus then plus gives 14. Times then minus gives 30. None of those is 10.",
      w("l4", "8 − 4 + 2 = 6"), w("l5", "8 + 4 + 2 = 14"), w("l6", "8 × 4 − 2 = 30")),
    b("With missing signs, make a sensible first try, see how far off you are, and then fix it."),
]


# ── G4A_PUZZLES_008 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_008"] = [
    b("A palindrome reads the same forwards and backwards, like 353. One of these four numbers is a palindrome. Let's find it.",
      g("l1", "Palindrome: the same forwards and backwards", True), g("c", "1212     1221     1122     2121", True)),
    b("The test is simple: write the number backwards and see if it changes. Take the first one. Its digits are 1, 2, 1, 2. Backwards that is 2, 1, 2, 1.",
      lab("l2", "1212 backwards is 2121")),
    b("That is a different number, so it is not a palindrome. Now take the digits 1, 2, 2, 1. What do you get when you write them backwards?",
      ask=ch("1, 2, 2, 1", ["2, 1, 1, 2", "2, 2, 1, 1"],
             "Start from the last digit and go back: 1, then 2, then 2, then 1. The same as before.")),
    b("It is the same both ways. The first digit matches the last, and the two middle digits match each other.",
      lab("l3", "1221 backwards is 1221"), mk("c", "1221", "circle")),
    b("The other two change as well. 1122 turns into 2211, and 2121 turns into 1212.",
      lab("l4", "1122 backwards is 2211"), lab("l5", "2121 backwards is 1212")),
    b("So the palindrome number is 1221.", ans("l6", "1221")),
    b("A quick test for a palindrome: the first digit must match the last, the second must match the second from last, and so on."),
]


# ── G4A_PUZZLES_009 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_009"] = [
    b("A magic square with two letters hiding in it, P and Q. Every row, column and diagonal has the same total. We want P plus Q.",
      g("l1", "Magic square.  P + Q = ?", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_009"))),
    b("First we need the magic total. Which row can give it to us?",
      ask=ch("Row 3: 8, 18, 4", ["Row 1: 16, 2, P", "Row 2: 6, Q, 14"],
             "Rows 1 and 2 each hide a letter. Row 3 is complete, so we can add it.")),
    b("8 plus 18 plus 4 is 30. So every line adds up to 30.", w("l2", "8 + 18 + 4 = 30")),
    b("Row 1 is 16, 2 and P. 16 plus 2 is 18, and 30 take away 18 is 12. So P is 12.",
      w("l3", "16 + 2 = 18"), w("l4", "30 − 18 = 12"), lab("l5", "P = 12")),
    b("Row 2 is 6, Q and 14. 6 plus 14 is 20, and 30 take away 20 is 10. So Q is 10.",
      w("l6", "6 + 14 = 20"), w("l7", "30 − 20 = 10"), lab("l8", "Q = 10")),
    b("We have P and we have Q. What does the question want?",
      ask=ch("P + Q", ["the magic total", "just P"], "Read the last line of the question again. It asks for P plus Q.")),
    b("12 plus 10 is 22. So P plus Q is 22. Don't stop at 30: that is the magic total.", ans("l9", "12 + 10 = 22", "22")),
    b("Check Q with a diagonal: 16 plus 10 plus 4 is 30. Find the total from a full line, fill the gaps, then answer what was asked.",
      w("l10", "16 + 10 + 4 = 30")),
]


# ── G4A_PUZZLES_010 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_010"] = [
    b("P is the same hidden digit both times. 3 P is a number in the thirties. P 8 is a number ending in 8. Together they make 82.",
      g("l1", "3P + P8 = 82", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_010"))),
    b("Write it as a column sum and start with the ones column, just as we always do. In the ones column we add P and 8.",
      lab("l2", "ones column: P + 8 ends in 2")),
    b("P plus 8 must end in 2, and P is a single digit. Which digit works?",
      ask=ch("4", ["6", "2"],
             "8 plus 4 makes a number that ends in 2. Taking 2 from 8 gives 6, but here the digits are added, not subtracted.")),
    b("4 plus 8 is 12. That ends in 2, and 1 ten is carried over.", w("l3", "4 + 8 = 12")),
    b("Now test the whole sum with P as 4. The two numbers are 34 and 48. And 34 plus 48 is 82. It works!",
      w("l4", "34 + 48 = 82")),
    b("So P is 4.", ans("l5", "P = 4", None, True)),
    b("Look at the tens as well. 3 tens and 4 tens and the 1 carried over make 8 tens. Everything fits.",
      w("l6", "3 + 4 + 1 = 8")),
    b("In a letter sum, start with the ones column. It often gives the digit away. Then check the whole sum."),
]


# ── G4A_PUZZLES_011 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_011"] = [
    b("P and Q are digits. The numbers P Q and Q P add up to 77. And P is 1 more than Q. We want the number P Q.",
      g("l1", "PQ + QP = 77,  P is 1 more than Q", True), fig("f1", qfig(TOPIC, "G4A_PUZZLES_011"))),
    b("Stack them as a column sum. In the ones column we add Q and P. In the tens column we add P and Q. The same two digits each time!"),
    b("The total is 77. So what is P plus Q?",
      ask=ch("7", ["77", "14"], "Each column adds P and Q, and each column of the answer shows a 7. So P plus Q is 7.")),
    b("So we need two digits that add up to 7, where one is 1 more than the other.",
      lab("l2", "P + Q = 7"), lab("l3", "P is 1 more than Q")),
    b("Which pair of digits is it?",
      ask=ch("4 and 3", ["5 and 2", "6 and 1"],
             "5 and 2 make 7, but they are 3 apart. 4 and 3 make 7 and are just 1 apart.")),
    b("P is the bigger one. So P is 4 and Q is 3, and the number P Q is 43. Careful: not 34.", lab("l4", "P = 4,  Q = 3"), lab("l4b", "so PQ is 43, not 34")),
    b("Check: 43 plus 34 is 77. So the number is 43.", w("l5", "43 + 34 = 77"), ans("l6", "PQ = 43", "43", True)),
    b("When two letters swap places in a sum, look at one column at a time. Each column tells you what the letters add up to."),
]


# ── G4A_PUZZLES_012 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_012"] = [
    b("I think of a number. I double it and then add 3. The answer is 17. What was my number?",
      g("l1", "? × 2 + 3 = 17"), fig("f1", qfig(TOPIC, "G4A_PUZZLES_012"))),
    b("To get back to the start, we undo the steps. Which step do we undo first?",
      ask=ch("the adding of 3", ["the doubling", "it makes no difference"],
             "Adding 3 was done last. It is like shoes and socks: the last thing on is the first thing off.")),
    b("To undo adding 3, take 3 away. 17 take away 3 is 14. So the doubled number was 14.", w("l2", "17 − 3 = 14")),
    b("Now undo the doubling. How?",
      ask=ch("halve 14", ["double 14", "take 2 away from 14"], "Doubling means times 2. Halving is what undoes it.")),
    b("Half of 14 is 7. So the number was 7.", ans("l3", "14 ÷ 2 = 7", "7")),
    b("Check by going forwards. 7 doubled is 14, and 14 plus 3 is 17. It works.", w("l4", "7 × 2 + 3 = 17")),
    b("To find a starting number, work backwards. Undo the last step first, using the opposite move each time."),
]


# ── G4A_PUZZLES_013 ──────────────────────────────────────────────────────────
L["G4A_PUZZLES_013"] = [
    b("Isha, Jay, Kiran and Lata each have one pet: a cat, a dog, a parrot and a rabbit. We have three clues, and we want Lata's pet.",
      g("l1", "Jay: cat.   Kiran: rabbit.", True), g("l2", "Isha: not the dog.   Lata: ?", True), lab("l3", "cat, dog, parrot, rabbit")),
    b("Jay has the cat and Kiran has the rabbit. Which pets are left for Isha and Lata?",
      ask=ch("the dog and the parrot", ["the cat and the dog", "the parrot and the rabbit"],
             "Cross off the cat and the rabbit. The two pets left are the dog and the parrot.")),
    b("Cross off the cat for Jay, and the rabbit for Kiran. The dog and the parrot are left.",
      st("l3", "cat", "Jay"), st("l3", "rabbit", "Kiran")),
    b("Now the last clue. Isha does not have the dog. So Isha must have the parrot.", st("l3", "parrot", "Isha")),
    b("Only one pet is left, and only one child. So Lata has the dog.",
      mk("l3", "dog", "circle"), ans("l4", "Lata: dog", None, True)),
    b("Here is everyone with their pet. Every clue fits.",
      tbl("f1", [["Isha", "parrot"], ["Jay", "cat"], ["Kiran", "rabbit"], ["Lata", "dog"]], None, ["Child", "Pet"])),
    b("In a matching puzzle, use the sure clues first and cross things off. A clue that says not is useful once only two choices are left."),
]
