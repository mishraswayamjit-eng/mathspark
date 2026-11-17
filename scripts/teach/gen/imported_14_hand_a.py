"""Batch 14 lessons written beat by beat: single place values, clue puzzles, a digit swap, even numbers.

In every ask the FIRST choice is the right one; finish() moves it to a varied position.
"""
from imported_14_lib import a, al, b, box, ch, fig, finish, g, gl, nt, pchart, ring, ul, w, wl, x  # noqa: F401

P = "AIGEN_grade5_"
T = "IPMTB_grade5_"

RAW = {}

# ── Clue puzzles ─────────────────────────────────────────────────────────────

# Ravi's 5-digit number: 7 _ _ 5 1, thousands digit worth 3000, hundreds twice thousands -> 73651, digit sum 22
RAW[P + "bededa81-f160-4900-acf0-be30c0a9d05c"] = [
    b("Ravi's number has 5 digits, and five clues tell us what they are. We will fill the places one by one, then add up the digits.",
      gl("q", "_ _ _ _ _    sum of the digits = ?")),
    b("Clue 1 puts 7 in the ten-thousands place. Clues 3 and 4 put 5 in the tens place and 1 in the units place. Those three are simply given.",
      wl("s1", "7 _ _ 5 1")),
    b("Clue 5 says the place value of the thousands digit is 3000. So which digit sits in the thousands place?",
      ask=ch(["3", "3000", "30"],
             "In the thousands place a digit counts thousands. It takes 3 thousands to make 3000, so the digit is 3.")),
    b("3 times 1000 is 3000, so the thousands digit is 3. Careful: the digit is 3, not 3000. A place holds only one digit.",
      w("t", "3 × 1000 = 3000"), wl("s2", "7 3 _ 5 1")),
    b("Clue 2 says the hundreds digit is twice the thousands digit. What is the hundreds digit?",
      ask=ch(["6", "5", "3"],
             "Twice means 2 times. The thousands digit is 3, and 2 times 3 is 6.")),
    b("2 times 3 is 6. Now every place is filled, and Ravi's number is 73651.",
      w("h", "2 × 3 = 6"), wl("s3", "Ravi's number = 73651"), fig("chart", pchart("73651"))),
    b("The question asks for the sum of the digits, not the number itself. 7 plus 3 is 10, and 6 more makes 16.",
      w("p1", "7 + 3 = 10"), w("p2", "10 + 6 = 16")),
    b("Then 16 plus 5 is 21, and 1 more makes 22. The digits add up to 22.",
      w("p3", "16 + 5 = 21"), a("ans", "7 + 3 + 6 + 5 + 1 = 22"), ring("ans", "22")),
    b("Check the clues once more. 6 is twice 3, the tens digit is 5, the units digit is 1, and the 3 in the thousands place is worth 3000. All five fit."),
    b("So in a clue puzzle, draw the places as blanks, fill in what is given straight away, and leave the clues that depend on other digits for last."),
]

# Riya's 6-digit number -> 5,47,826; place value of lakhs digit minus face value of units digit = 4,99,994
RAW[P + "dbdee766-0e97-4938-86de-7dd493ff43d9"] = [
    b("Riya's number has 6 digits and six clues. Some clues give a digit straight away, and some depend on other digits. We start with the ones that are simply given.",
      gl("q", "_ _ _ _ _ _    lakhs down to units")),
    b("The thousands digit is 7, the hundreds digit is 8 and the tens digit is 2. Write those in.",
      wl("s1", "_ _ 7 8 2 _")),
    b("The lakhs digit is 3 more than the tens digit. So what goes in the lakhs place?",
      ask=ch(["5", "6", "1"],
             "The tens digit is 2. 3 more than 2 means 2 plus 3, and that is 5.")),
    b("2 plus 3 is 5. And the ten-thousands digit is half of the hundreds digit: half of 8 is 4.",
      w("l", "2 + 3 = 5"), w("tt", "8 ÷ 2 = 4"), wl("s2", "5 4 7 8 2 _")),
    b("The units digit is the ten-thousands digit plus the tens digit. 4 plus 2 is 6. So the number is 5,47,826.",
      w("u", "4 + 2 = 6"), wl("s3", "Riya's number = 5,47,826"), fig("chart", pchart("547826", hi=[0, 5]))),
    b("Now the question. First we need the place value of the 5 in the lakhs place. What is it?",
      ask=ch(["5,00,000", "50,000", "5"],
             "The lakhs place is the sixth place from the right. A 5 there stands for 5 lakhs, and that is a 5 followed by five zeros: 5,00,000.")),
    b("5 times 1,00,000 is 5,00,000. And the face value of the units digit is just the digit itself, 6.",
      w("pv", "5 × 1,00,000 = 5,00,000"), wl("fv", "Face value of 6 = 6")),
    b("The difference is 5,00,000 minus 6. Taking 6 away drops us just below 5 lakh, to 4,99,994.",
      a("ans", "5,00,000 − 6 = 4,99,994"), ring("ans", "4,99,994")),
    b("Careful: adding the 6 instead would give 5,00,006. But difference means subtract.",
      w("no", "5,00,000 + 6 = 5,00,006")),
    b("Check by adding back: 4,99,994 plus 6 is 5,00,000. It fits.",
      w("k", "4,99,994 + 6 = 5,00,000")),
    b("So build the number from the clues first, given digits before linked ones. Then answer what was asked, using place value for one digit and face value for the other."),
]

# ── A digit swap ─────────────────────────────────────────────────────────────

# 86,473 with 6 and 4 swapped -> 84,673; change 1800
RAW[P + "f4e5ebb5-48e9-4336-82ea-09cdcba6b3b0"] = [
    b("Meena's family spent 86,473 rupees. We swap the digits 6 and 4, and ask by how much the number changes.",
      g("n", "86,473"), ul("n", "6"), ul("n", "4")),
    b("Here it is in the chart. The 6 is in the thousands place and the 4 is in the hundreds place. After the swap, what is the new number?",
      fig("chart", pchart("86473", hi=[1, 2])),
      ask=ch(["84,673", "86,743", "48,673"],
             "Only the 6 and the 4 change places. The 8 in front and the 7 and 3 at the end stay where they are. So it reads 8, 4, 6, 7, 3.")),
    b("The new number is 84,673. The 4 has moved up to the thousands and the 6 has moved down to the hundreds.",
      w("m", "84,673"), ul("m", "4"), ul("m", "6")),
    b("Is the new number bigger or smaller than 86,473?",
      ask=ch(["smaller", "bigger"],
             "Compare the thousands place. The old number has 6 thousands there, and the new one has only 4. So the new number is smaller.")),
    b("Smaller. So the change is the old number minus the new one. The 8 in front and the 7 and 3 at the end are the same in both, so only the middle matters.",
      w("d0", "86,473 − 84,673 = ?")),
    b("In the middle, the old number has 6 thousands and 4 hundreds, which is 6400. The new one has 4 thousands and 6 hundreds, which is 4600.",
      w("o", "6000 + 400 = 6400"), w("p", "4000 + 600 = 4600")),
    b("6400 minus 4600 is 1800. So the number goes down by 1800 rupees.",
      w("d", "6400 − 4600 = 1800"), a("ans", "86,473 − 84,673 = 1800"), ring("ans", "1800")),
    b("Careful: the answer is not 2000. The 6 and the 4 do differ by 2 in the thousands place, but the swap hands 2 hundreds back in the hundreds place.",
      w("t", "2000 − 200 = 1800")),
    b("Check by adding: 84,673 plus 1800 is 86,473, the number we began with.",
      w("k", "84,673 + 1800 = 86,473")),
    b("So when two digits swap, write the new number, see which one is bigger, and subtract. Only the places that changed matter."),
]

# ── Even numbers ─────────────────────────────────────────────────────────────

# Even number before 50 and after 50: 52 − 48 = 4
RAW[T + "ch01_q041"] = [
    b("We need two even numbers: the one just before 50 and the one just after 50. Then we find the difference between them.",
      gl("q", "even number before 50, even number after 50")),
    b("Even numbers go up in twos. Here are the ones around 50.",
      wl("e", "46    48    50    52    54"), box("e", "50")),
    b("Which even number comes just before 50?",
      ask=ch(["48", "49", "46"],
             "49 is right next to 50, but it is odd. Even numbers are 2 apart, so the even number just before 50 is 48.")),
    b("48. Careful: 49 is nearer, but it is odd, so it does not count.",
      ul("e", "48"), w("b", "50 − 2 = 48")),
    b("In the same way, the even number just after 50 is 2 more than 50. That is 52.",
      ul("e", "52"), w("c", "50 + 2 = 52")),
    b("Now the difference between 52 and 48. What is it?",
      ask=ch(["4", "2", "100"],
             "Difference means take the smaller from the bigger. From 48 it is 2 steps up to 50, and 2 more steps up to 52. That is 4 steps.")),
    b("52 minus 48 is 4. That makes sense: 48 is 2 below 50 and 52 is 2 above it, and 2 plus 2 is 4.",
      a("ans", "52 − 48 = 4"), ring("ans", "4", 2)),
    b("Careful: adding the two numbers gives 100. But the question asks for the difference, so we subtract.",
      w("t", "52 + 48 = 100")),
    b("Check by adding back: 48 plus 4 is 52.", w("k", "48 + 4 = 52")),
    b("So remember that even numbers are 2 apart. Find the one on each side, then subtract the smaller from the bigger."),
]

# 8th even after 50 (66) + 8th even before 100 (84) = 150
RAW[T + "ch01_q042"] = [
    b("Two numbers to find here: the 8th even number after 50, and the 8th even number before 100. Then we add them.",
      gl("q", "8th even after 50 + 8th even before 100")),
    b("Even numbers go up in twos. After 50 the first one is 52, then 54, then 56. Let's keep going until we have 8 of them.",
      wl("u", "52  54  56  58  60  62  64  66")),
    b("Count along the list. Which is the 8th even number after 50?",
      ask=ch(["66", "58", "68"],
             "Start counting at 52, not at 50, because we want numbers after 50. Then 52 is the 1st, 54 is the 2nd, and the 8th one is 66.")),
    b("66. Here is a quick way to see it: 8 even numbers means 8 jumps of 2, and that is 16. And 50 plus 16 is 66.",
      ring("u", "66"), w("j", "8 × 2 = 16"), w("a1", "50 + 16 = 66")),
    b("Now count backwards from 100. The 1st even number before it is 98, then 96, then 94, and on down.",
      wl("d", "98  96  94  92  90  88  86  84")),
    b("That is 8 jumps of 2 back from 100. Where do we land?",
      ask=ch(["84", "92", "82"],
             "8 jumps of 2 make 16. Going back means subtract, and 100 minus 16 is 84.")),
    b("100 minus 16 is 84, the last number in our list.",
      ring("d", "84"), w("a2", "100 − 16 = 84")),
    b("Now add the two. 60 plus 80 is 140, and 6 plus 4 is 10. So 66 plus 84 is 150.",
      w("s1", "60 + 80 = 140"), w("s2", "6 + 4 = 10"), a("ans", "66 + 84 = 150"), ring("ans", "150")),
    b("Careful: 50 and 100 themselves are not counted. The question says after 50 and before 100, so the counting starts at 52 and at 98."),
    b("Check: 66 is 16 above 50, and 84 is 16 below 100. The two 16s cancel, so the sum is just 50 plus 100, which is 150.",
      w("k", "50 + 100 = 150")),
    b("So for the 8th even number, make 8 jumps of 2, forwards or backwards. Then do what the question asks with the two numbers."),
]

# ── One place value ──────────────────────────────────────────────────────────

# Place value of 5 in 25,61,174 -> 5,00,000
RAW[T + "ch02_q001"] = [
    b("Here is 25,61,174, written with commas the Indian way. We want the place value of the digit 5.",
      g("n", "25,61,174"), ul("n", "5")),
    b("Let's put it in a place-value chart and name the columns from the right: ones, tens, hundreds, thousands, ten-thousands, lakhs, ten-lakhs.",
      fig("chart", pchart("2561174", hi=[1]))),
    b("Which column is the 5 sitting in?",
      ask=ch(["lakhs", "ten-thousands", "ten-lakhs"],
             "Count from the right. The 4 is in the ones, then 7, 1, 1 and 6 take the tens up to the ten-thousands. The 5 is the sixth digit, and the sixth place is lakhs.")),
    b("The 5 is in the lakhs place. One lakh is 1,00,000, a 1 with five zeros.",
      nt("n", "5", "lakhs", "above"), wl("l", "1 lakh = 1,00,000")),
    b("So what is the 5 worth?",
      ask=ch(["5,00,000", "50,000", "50,00,000"],
             "5 in the lakhs place means 5 lakhs. That is 5 times 1,00,000, so a 5 with five zeros: 5,00,000.")),
    b("5 times 1,00,000 is 5,00,000. That is the place value of the 5.",
      a("ans", "5 × 1,00,000 = 5,00,000"), ring("ans", "5,00,000")),
    b("Careful with the zeros. Five digits come after the 5 in the number, so five zeros come after the 5 in its place value. Not four, and not six."),
    b("Check with the commas. From the right, the first comma comes after the hundreds and the next after the ten-thousands. The 5 is the very next digit, so it is lakhs."),
    b("So to find a place value, find the digit's column. Then write the digit, with a zero for every place to its right."),
]

# Place value of 2 in 1,21,753 -> 20,000
RAW[T + "ch02_q024"] = [
    b("Here is 1,21,753. We want the place value of the digit 2.",
      g("n", "1,21,753"), ul("n", "2")),
    b("Count the places from the right. 3 is in the ones, 5 in the tens, 7 in the hundreds, and the 1 after the comma is in the thousands.",
      fig("chart", pchart("121753", hi=[1]))),
    b("The 2 comes next. Which place is that?",
      ask=ch(["ten-thousands", "thousands", "lakhs"],
             "After ones, tens, hundreds and thousands comes ten-thousands. The 2 is the fifth digit from the right, so it is in the ten-thousands place.")),
    b("The 2 is in the ten-thousands place, so it stands for 2 ten-thousands. One ten-thousand is written 10,000.",
      nt("n", "2", "ten-thousands", "above"), wl("tt", "ten-thousand = 10,000")),
    b("What is 2 ten-thousands, written as a number?",
      ask=ch(["20,000", "2000", "2,00,000"],
             "Ten-thousand is 10,000. 2 times 10,000 is 20,000, a 2 with four zeros.")),
    b("2 times 10,000 is 20,000. That is the place value of the 2.",
      a("ans", "2 × 10,000 = 20,000"), ring("ans", "20,000")),
    b("Careful: 21,753 is the 2 together with all the digits after it. The place value is the 2 alone, with zeros where those other digits were.",
      w("t", "21,753 = 20,000 + 1753")),
    b("Check by counting: four digits follow the 2 in the number, and four zeros follow the 2 in 20,000."),
    b("So find the column first, then write the digit with a zero for each place to its right. The other digits play no part."),
]

# Greatest place value of 7 in 17,32,727 -> 7,00,000
RAW[T + "ch02_q033"] = [
    b("Here is 17,32,727. The digit 7 appears more than once, and we want the greatest of its place values.",
      g("n", "17,32,727")),
    b("First, how many 7s are in the number?",
      ask=ch(["3", "2", "4"],
             "Go through the digits one at a time: 1, 7, 3, 2, 7, 2, 7. The 7 turns up 3 times.")),
    b("Three 7s. Here they are in the chart: one in the ones, one in the hundreds and one in the lakhs.",
      ul("n", "7", 1), ul("n", "7", 2), ul("n", "7", 3), fig("chart", pchart("1732727", hi=[1, 4, 6]))),
    b("The 7 in the ones place is worth just 7. The 7 in the hundreds place is worth 7 times 100, which is 700.",
      w("v1", "7 × 1 = 7"), w("v2", "7 × 100 = 700")),
    b("And the 7 in the lakhs place. What is that one worth?",
      ask=ch(["7,00,000", "70,000", "70,00,000"],
             "7 in the lakhs place means 7 lakhs. A lakh has five zeros, so write 7 and then five zeros: 7,00,000.")),
    b("7 times 1,00,000 is 7,00,000. Same digit, three very different values.",
      w("v3", "7 × 1,00,000 = 7,00,000")),
    b("The greatest of the three is 7,00,000. It comes from the 7 furthest to the left.",
      w("cmp", "7,00,000 > 700 > 7"), al("ans", "Greatest place value of 7 = 7,00,000"), ring("ans", "7,00,000")),
    b("Careful: this 7 is not in the ten-lakhs place. The 1 in front holds that place, so the 7 stands for lakhs and not for ten times as much."),
    b("So the same digit is worth the most in the place furthest left. Find every copy of the digit, and take the leftmost one."),
]

# Digit with the least place value in 4,37,896 -> 6
RAW[T + "ch02_q034"] = [
    b("Here is 4,37,896. Every digit in it has a place value. We want the digit whose place value is the smallest.",
      g("n", "4,37,896")),
    b("Place value depends on the column. Each step to the left makes a digit worth 10 times more, so the columns on the right are worth the least.",
      fig("chart", pchart("437896"))),
    b("So which column gives the smallest place value?",
      ask=ch(["the ones, far right", "the lakhs, far left", "wherever the smallest digit is"],
             "The size of the digit is not what matters here. A digit in the ones place is worth only itself, and every place to the left multiplies it by 10 or more.")),
    b("The ones place. The digit there is 6, and it is worth just 6.",
      ul("n", "6"), nt("n", "6", "ones", "below"), w("v1", "6 × 1 = 6")),
    b("Let's test the digit that looks smallest, the 3. It sits in the ten-thousands place, so it is worth 30,000.",
      ul("n", "3"), w("v2", "3 × 10,000 = 30,000")),
    b("Which is smaller: the place value of the 6, or the place value of the 3?",
      ask=ch(["6, from the digit 6", "30,000, from the digit 3"],
             "Compare what they are worth, not how the digits look. 6 is far smaller than 30,000.")),
    b("6 is much less than 30,000. Even the 9 next door is worth more than our 6: it is in the tens place, so it is worth 90.",
      w("cmp", "6 < 30,000"), w("v3", "9 × 10 = 90")),
    b("So the digit with the smallest place value is 6.",
      al("ans", "Digit with the least place value: 6"), ring("ans", "6")),
    b("Careful: don't hunt for the smallest digit. Hunt for the smallest column, and read the digit that sits there."),
    b("So place value is about the column, not the size of the digit. Here the ones place holds the least, and the lakhs place holds the most."),
]

# Greatest place value minus least place value in 9,37,451 -> 8,99,999
RAW[T + "ch02_q035"] = [
    b("Here is 9,37,451. We want the greatest place value in it, the smallest place value in it, and then the difference between the two.",
      g("n", "9,37,451")),
    b("Place value comes from the column. The column furthest left is worth the most, and the column furthest right is worth the least.",
      fig("chart", pchart("937451", hi=[0, 5])), ul("n", "9"), ul("n", "1")),
    b("The 9 is furthest left, in the lakhs place. What is it worth?",
      ask=ch(["9,00,000", "90,000", "9"],
             "9 in the lakhs place means 9 lakhs. A lakh has five zeros, so write 9 and then five zeros: 9,00,000.")),
    b("9 times 1,00,000 is 9,00,000. That is the greatest place value in the number.",
      w("mx", "9 × 1,00,000 = 9,00,000"), nt("n", "9", "greatest", "above")),
    b("The digit furthest right is the 1, in the ones place. It is worth just 1, the smallest place value.",
      w("mn", "1 × 1 = 1"), nt("n", "1", "least", "below")),
    b("Now the difference. Which sum is it?",
      ask=ch(["9,00,000 − 1", "9 − 1", "9,00,000 + 1"],
             "Difference means subtract. And we subtract the place values, 9,00,000 and 1, not the bare digits.")),
    b("Take 1 away from 9,00,000. The 9 in front drops to 8, and every zero turns into a 9. That gives 8,99,999.",
      a("ans", "9,00,000 − 1 = 8,99,999"), ring("ans", "8,99,999")),
    b("Careful: 9,00,000 on its own is only the greatest place value. And count the 9s in the answer: there should be five of them after the 8."),
    b("Check by adding the 1 back: 8,99,999 plus 1 is 9,00,000. It fits.",
      w("k", "8,99,999 + 1 = 9,00,000")),
    b("So the greatest place value belongs to the digit furthest left, and the least to the digit furthest right. Find both, then subtract."),
]

# Which digit's place value always equals the digit itself? -> 0
RAW[T + "ch02_q009"] = [
    b("We want a digit whose place value is always the same as the digit itself, whichever column it sits in.",
      gl("q", "place value = the digit itself, in every place?")),
    b("Place value is the digit times its column. Let's test 5 in the tens column. 5 times 10 is 50, and 50 is not 5. So 5 is out.",
      w("t5", "5 × 10 = 50"), fig("chart", pchart("50", hi=[0]))),
    b("Now try 1, in the hundreds column. Is its place value still 1?",
      ask=ch(["No, it is worth 100", "Yes, it is worth 1"],
             "1 in the hundreds column means one hundred. 1 times 100 is 100, not 1.")),
    b("1 times 100 is 100. So 1 does not work either. And 9 goes the same way: in the tens column it is worth 90.",
      w("t1", "1 × 100 = 100"), w("t9", "9 × 10 = 90")),
    b("Is there any digit that stays the same when it is multiplied by 10, by 100, or by any bigger column?",
      ask=ch(["0", "1", "there is none"],
             "Think about 0. Zero lots of anything is still nothing. So 0 times 10 and 0 times 100 both come to 0, and so does every other column.")),
    b("Zero! 0 times 10 is 0, 0 times 100 is 0, and 0 times 1000 is 0.",
      w("z1", "0 × 10 = 0"), w("z2", "0 × 100 = 0"), w("z3", "0 × 1000 = 0")),
    b("So the place value of 0 is 0 in every column, exactly its own value. The answer is 0.",
      al("ans", "The digit 0"), ring("ans", "0")),
    b("Careful: in the ones column every digit equals its place value. But the question says always, and only 0 passes that test."),
    b("So to test a rule that says always, try the digit in different columns. One column where it breaks is enough to rule that digit out."),
]

LESSONS = {qid: finish(qid, beats) for qid, beats in RAW.items()}
