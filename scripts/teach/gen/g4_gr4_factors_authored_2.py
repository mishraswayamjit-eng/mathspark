"""Hand-written lessons, part 2: past-paper questions 2023 to 2025."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANS, ANSM, B, CIRC, GIVEN, LB, LESSON, Q, STRIKE, TABLE, UL, W,
)

LESSONS = {}

LESSONS["EXT_G4_FP_2023_018"] = LESSON(
    B("A five-digit number: 1, A, 9, A, 5. Both A's are the same digit, and 7 divides the number exactly. Which digit is A?",
      GIVEN("q", "1A9A5 is divisible by 7.  A = ?"), LB("o", "Choices: 4, 5, 7, 2"),
      TABLE("f", [["1", "A", "9", "A", "5"]], note="Both A's are the same digit.")),
    B("There is no easy digit test for 7. So here is the smart move: try each choice, and divide by 7."),
    B("Start with 4. The number becomes 14945.", LB("n", "A = 4 gives 14945")),
    B("Divide in easy chunks. 7 times 2000 is 14000. Take that away from 14945, and 945 is left.",
      W("a0", "7 × 2000 = 14000"), W("a", "14945 − 14000 = 945")),
    Q("Now 945. 7 times 100 is 700, and that leaves 245. Is 245 in the 7 times table?",
      ["Yes, 7 × 35 = 245", "No, some is left over"], 0,
      "7 times 35 is 245. So it is in the 7 times table, with nothing left over.",
      W("b0", "7 × 100 = 700"), W("b", "945 − 700 = 245")),
    B("So 14945 is made of 2000 sevens, 100 sevens and 35 sevens. That is 7 times 2135, with nothing left over. A is 4.",
      W("c0", "7 × 35 = 245"), W("c", "7 × 2135 = 14945"), ANS("ans", "A = 4"), CIRC("ans", "A = 4")),
    B("Let's test another choice, to be sure. With 5 the number is 15955. But 7 times 2279 is 15953, so 2 is left over.",
      W("d", "7 × 2279 = 15953"), W("e", "15955 − 15953 = 2")),
    B("The other two choices give 17975 and 12925. Each of those leaves a remainder too. Only 4 works.",
      LB("g", "17975 and 12925 leave remainders")),
    B("So when there is no quick test, try the choices one by one. And split a big division into easy chunks."),
)

LESSONS["EXT_G4_FP_2023_026"] = LESSON(
    B("Two jobs in one. Add up the first ten two-digit prime numbers. Then write the total in Roman numerals.",
      GIVEN("q", "Sum of the first 10 two-digit primes, in Roman numerals")),
    B("First list them. The two-digit primes start at 11. Here are the first ten, ending at 43.",
      LB("p", "11, 13, 17, 19, 23, 29, 31, 37, 41, 43")),
    B("Careful with the ones we skipped. 21, 27, 33 and 39 look prime, but each one is in the 3 times table.",
      W("s1", "21 = 3 × 7"), W("s2", "27 = 3 × 9"), W("s3", "33 = 3 × 11"), W("s4", "39 = 3 × 13")),
    B("Now add, in friendly pairs. 11 plus 19 is 30. 13 plus 17 is 30. 23 plus 37 is 60. 29 plus 31 is 60. And 41 plus 43 is 84.",
      W("a1", "11 + 19 = 30"), W("a2", "13 + 17 = 30"), W("a3", "23 + 37 = 60"), W("a4", "29 + 31 = 60"),
      W("a5", "41 + 43 = 84")),
    Q("Add the pair totals: 30, 30, 60, 60 and 84. What do they make?", ["264", "244", "266"], 0,
      "Add the four round numbers first, then the 84. One at a time, and you reach 264."),
    B("The total is 264.", W("t", "30 + 30 + 60 + 60 + 84 = 264")),
    B("Now Roman numerals. Split 264 into 200, 60 and 4. 200 is C C. 60 is L X. And 4 is I V, one before five.",
      W("r", "264 = 200 + 60 + 4"), LB("r1", "200 = CC"), LB("r2", "60 = LX"), LB("r3", "4 = IV")),
    B("Put the three parts together: C C, L X, I V. That is 264 in Roman numerals.",
      ANS("ans", "264 = CCLXIV"), CIRC("ans", "CCLXIV")),
    B("Watch the order of the letters. L X is 60, but X L is 40, because a smaller letter in front is taken away.",
      LB("x", "LX = 60,  XL = 40")),
)

LESSONS["EXT_G4_FP_2023_036"] = LESSON(
    B("Which of these four numbers can be divided exactly by 18? We will not divide. We will use two quick tests.",
      GIVEN("q", "Divisible by 18?  9486, 9672, 9876, 9567")),
    B("18 is 2 times 9. So the number must pass the test for 2 and the test for 9. Both, not just one.",
      W("a", "18 = 2 × 9")),
    B("Test for 2: the number must be even. 9567 ends in 7, so it is odd. It is out.", STRIKE("q", "9567", "odd")),
    B("Test for 9: the digits must add up to a number in the 9 times table. 9672 gives 24, and 9876 gives 30. Neither is in the 9 times table.",
      W("b", "9 + 6 + 7 + 2 = 24"), W("c", "9 + 8 + 7 + 6 = 30"), STRIKE("q", "9672"), STRIKE("q", "9876")),
    Q("Now 9486. What do its digits add up to?", ["27", "26", "28"], 0,
      "Add them one at a time: 9, then 4, then 8, then 6. You reach 27."),
    B("The digits add up to 27, and 27 is 9 times 3. And 9486 ends in 6, so it is even. Both tests are passed!",
      W("d", "9 + 4 + 8 + 6 = 27"), W("e", "27 = 9 × 3"), ANS("ans", "9486 is divisible by 18"), CIRC("ans", "9486")),
    B("Here is the trap. The digits of 9567 add up to 27 as well, so 9 divides it. But it is odd, so 2 does not, and 18 cannot.",
      W("f", "9 + 5 + 6 + 7 = 27")),
    B("So for 18, use two tests together: an even last digit for 2, and the digit sum for 9."),
)

LESSONS["EXT_G4_FP_2023_040"] = LESSON(
    B("Four statements, and only one of them is true. So we test every one, like a detective.",
      GIVEN("q", "Which one is true?")),
    B("First: 18 plus 18 divided by 2 equals 18. But we divide before we add. 18 divided by 2 is 9, and 18 plus 9 is 27, not 18.",
      LB("s1", "18 + 18 ÷ 2 = 18 ?"), W("a", "18 + 18 ÷ 2 = 27"), STRIKE("s1", "18 + 18 ÷ 2 = 18 ?")),
    B("Second: a leap year has 8760 hours. A leap year has 366 days, and 366 times 24 is 8784. It is the ordinary year, with 365 days, that has 8760 hours.",
      LB("s2", "1 leap year = 8760 hours ?"), W("b", "366 × 24 = 8784"), W("b2", "365 × 24 = 8760"),
      STRIKE("s2", "1 leap year = 8760 hours ?")),
    B("Next: 586 is a square number. 24 times 24 is 576, and 25 times 25 is 625. 586 sits between them, so it is not a square.",
      LB("s4", "586 is a square number ?"), W("c", "24 × 24 = 576"), W("d", "25 × 25 = 625"),
      STRIKE("s4", "586 is a square number ?")),
    Q("That leaves: 2816 is divisible by 11. Use the test for 11. The 1st and 3rd digits add up to 3. The 2nd and 4th add up to 14. How far apart are 3 and 14?",
      ["11", "17", "3"], 0,
      "Take the smaller sum from the bigger one. 14 take away 3 is 11.",
      LB("s3", "2816 is divisible by 11 ?"), W("e", "2 + 1 = 3"), W("f", "8 + 6 = 14")),
    B("The two sums differ by 11, and that is just what the test for 11 needs. So 11 divides 2816. In fact 11 times 256 is 2816.",
      W("g", "14 − 3 = 11"), W("h", "11 × 256 = 2816"), ANS("ans", "2816 is divisible by 11"), CIRC("ans", "2816")),
    B("When a question asks which one is true, test every statement. Do not stop at the first one that looks right."),
)

LESSONS["EXT_G4_FP_2024_008"] = LESSON(
    B("Find the one-digit prime numbers, add them, and then square the total.",
      GIVEN("q", "(sum of the one-digit primes)² = ?"), LB("o", "Choices: 361, 324, 441, None of these")),
    Q("Which list shows all the one-digit primes?", ["2, 3, 5, 7", "1, 2, 3, 5, 7", "2, 3, 5, 7, 9"], 0,
      "1 is not prime, because it has only one factor. And 9 is 3 times 3, so it is not prime either."),
    B("The one-digit primes are 2, 3, 5 and 7. Add them up, and we get 17.", W("a", "2 + 3 + 5 + 7 = 17")),
    B("Now square 17. That means 17 times 17. 17 times 10 is 170, and 17 times 7 is 119. Together they make 289.",
      W("b", "17 × 10 = 170"), W("c", "17 × 7 = 119"), W("d", "170 + 119 = 289"), W("e", "17² = 289")),
    Q("Our answer is 289. Now look at the choices: 361, 324, 441, or none of these. Which do we pick?",
      ["None of these", "324", "361"], 0,
      "Our answer is 289. It is not 361, 324 or 441. So we pick none of these."),
    B("289 is not in the list, so the answer is none of these. When your working checks out, trust it.",
      ANS("ans", "None of these (17² = 289)"), CIRC("ans", "None of these")),
    B("See where the other choices come from. Count 1 as a prime and the sum is 18, which gives 324. Count 9 as a prime and the sum is 21, which gives 441.",
      W("f", "18 × 18 = 324"), W("g", "21 × 21 = 441")),
)

LESSONS["EXT_G4_FP_2024_021"] = LESSON(
    B("Three numbers with a missing digit each: A 5 9, 5 B 2 and 6 C 9. 9 divides all three. Then we make the greatest odd number from A, B and C.",
      GIVEN("q", "A59, 5B2, 6C9 are divisible by 9"), LB("q2", "Greatest odd number from A, B, C = ?"),
      TABLE("f", [["A", "5", "9"], ["5", "B", "2"], ["6", "C", "9"]], note="9 divides the number in each row.")),
    B("The test for 9: the digits must add up to a number in the 9 times table. We will use it three times."),
    B("First number. 5 plus 9 is 14. The next number in the 9 times table is 18, and 14 needs 4 more to get there. So A is 4.",
      W("a", "5 + 9 = 14"), W("a2", "14 + 4 = 18"), LB("a3", "A = 4")),
    Q("Second number. 5 plus 2 is 7. What must B be, to reach the 9 times table?", ["2", "7", "9"], 0,
      "The next number in the 9 times table after 7 is 9 itself. And 7 needs 2 more to reach 9.",
      W("b", "5 + 2 = 7")),
    B("So B is 2. Third number: 6 plus 9 is 15, and 15 needs 3 more to reach 18. So C is 3.",
      W("b2", "7 + 2 = 9"), W("c", "6 + 9 = 15"), W("c2", "15 + 3 = 18"), LB("abc", "A = 4, B = 2, C = 3")),
    Q("Our digits are 4, 2 and 3. We want the greatest odd number. Which digit must go last?", ["3", "4", "2"], 0,
      "An odd number ends in an odd digit. Of 4, 2 and 3, only 3 is odd."),
    B("3 goes last. Then put the bigger of the other two first: 4, then 2. The greatest odd number is 423.",
      ANS("ans", "423"), CIRC("ans", "423")),
    B("The trap is 432. It is bigger, but it ends in 2, so it is even. Odd numbers must end in an odd digit.",
      LB("t", "432 is even")),
)

LESSONS["EXT_G4_FP_2024_027"] = LESSON(
    B("A five-digit number: A, 0, 4, 8, A. Both A's are the same digit, and 11 divides the number exactly. Which digit is A?",
      GIVEN("q", "A048A is divisible by 11.  A = ?"), LB("o", "Choices: 6, 3, 1, None of these")),
    B("The test for 11. Add the 1st, 3rd and 5th digits. Then add the 2nd and 4th digits. The two sums must be equal, or differ by 11.",
      LB("r", "Test for 11: two sums equal, or differ by 11")),
    B("The 2nd and 4th digits are 0 and 8. They add up to 8.", W("a", "0 + 8 = 8"), UL("q", "0"), UL("q", "8")),
    B("The 1st, 3rd and 5th digits are A, 4 and A. For the sums to be equal, these must add up to 8 as well."),
    Q("So A, plus 4, plus A makes 8. What do the two A's add up to?", ["4", "8", "12"], 0,
      "Take the 4 away from 8. 8 minus 4 is 4, so the two A's together make 4."),
    B("8 minus 4 is 4, and half of 4 is 2. So A is 2.", W("b", "8 − 4 = 4"), W("c", "4 ÷ 2 = 2"), LB("s", "A = 2")),
    B("Let's check. The number is 20482, and 11 times 1862 is 20482. It works.", W("d", "11 × 1862 = 20482")),
    Q("Now look at the choices: 6, 3, 1, or none of these. Which one do we pick?", ["None of these", "6", "1"], 0,
      "Our digit is 2. It is not 6, 3 or 1, so the right choice is none of these."),
    B("2 is not in the list, so the answer is none of these. When your working checks out, trust it.",
      ANS("ans", "None of these (A = 2)"), CIRC("ans", "None of these")),
)

LESSONS["EXT_G4_FP_2024_034"] = LESSON(
    B("Four pairs of numbers. For one pair, the L C M is a square number: a number times itself. We find each L C M and test it.",
      GIVEN("q", "Which pair has an LCM that is a square number?"), LB("o", "6 and 15,  8 and 36,  16 and 30,  4 and 18")),
    B("6 and 15. Count up in 15s: 15, then 30, and 6 divides 30. So the L C M is 30. But 5 times 5 is 25 and 6 times 6 is 36, so 30 is not a square.",
      LB("a", "LCM of 6 and 15 = 30"), W("a2", "5 × 5 = 25"), W("a3", "6 × 6 = 36")),
    B("8 and 36. Count up in 36s: 36, then 72, and 8 divides 72. The L C M is 72. But 8 times 8 is 64 and 9 times 9 is 81, so 72 is not a square.",
      LB("b", "LCM of 8 and 36 = 72"), W("b2", "8 × 8 = 64"), W("b3", "9 × 9 = 81")),
    B("16 and 30. Counting up in 30s, the first one that 16 divides is 240. But 15 times 15 is 225 and 16 times 16 is 256, so 240 is not a square.",
      LB("c", "LCM of 16 and 30 = 240"), W("c2", "15 × 15 = 225"), W("c3", "16 × 16 = 256")),
    Q("Last pair: 4 and 18. Count up in 18s: 18, then 36. Which is the first one that 4 divides?", ["36", "18", "72"], 0,
      "4 does not go into 18 exactly. But 4 times 9 is 36, so 36 is the first.",
      LB("d0", "Multiples of 18: 18, 36")),
    B("The L C M of 4 and 18 is 36. And 36 is 6 times 6, a square number! So the pair is 4 and 18.",
      LB("d", "LCM of 4 and 18 = 36"), ANS("ans", "4 and 18"), CIRC("ans", "4 and 18")),
    B("Watch the trap in 16 and 30. 16 is a square number itself, but the question is about the L C M of the pair, not the numbers in it."),
)

LESSONS["EXT_G4_FP_2025_001"] = LESSON(
    B("Three jobs in a row. Add the one-digit primes. Multiply by the greatest two-digit number. Then add up the digits of that product.",
      GIVEN("q", "(sum of one-digit primes) × (greatest 2-digit number)"), LB("q2", "Sum of the digits of the product = ?")),
    B("The one-digit primes are 2, 3, 5 and 7. Remember, 1 is not a prime. They add up to 17.", W("a", "2 + 3 + 5 + 7 = 17")),
    Q("What is the greatest two-digit number?", ["99", "100", "98"], 0,
      "100 has three digits. The biggest number with just two digits is 99."),
    B("So we need 17 times 99. Here is a trick: 99 is 1 less than 100. 17 times 100 is 1700. Take away one 17, and we get 1683.",
      W("b", "17 × 100 = 1700"), W("c", "1700 − 17 = 1683"), W("d", "17 × 99 = 1683")),
    Q("The face value of a digit is just the digit itself. The digits of 1683 are 1, 6, 8 and 3. What do they add up to?",
      ["18", "17", "19"], 0,
      "Add them one at a time: 1, then 6, then 8, then 3. You reach 18."),
    B("1 plus 6 plus 8 plus 3 is 18. That is our answer.", ANSM("ans", "1 + 6 + 8 + 3 = 18"), CIRC("ans", "18")),
    B("Careful: 17 is only the sum of the primes. This question has three steps, so do not stop early. Add, multiply, then add the digits."),
)

LESSONS["EXT_G4_FP_2025_006"] = LESSON(
    B("We need two primes: the greatest one with one digit, and the smallest one with two digits. Then we square each and add.",
      GIVEN("q", "(greatest 1-digit prime)² + (smallest 2-digit prime)²")),
    Q("What is the greatest one-digit prime?", ["7", "9", "8"], 0,
      "9 is 3 times 3, and 8 is even. So neither is prime. 7 is the greatest one-digit prime."),
    B("It is 7. Now the smallest two-digit prime. 10 is 2 times 5, so it is not prime. Next comes 11, and 11 is prime.",
      LB("a", "Greatest 1-digit prime: 7"), W("b0", "10 = 2 × 5"), LB("b", "Smallest 2-digit prime: 11")),
    B("Square each one. 7 times 7 is 49. And 11 times 11 is 121.", W("c", "7² = 49"), W("d", "11² = 121")),
    Q("The question asks for the sum of the two squares. Which is that?", ["49 + 121", "49 × 121", "7 + 11"], 0,
      "Sum means add. And we add the two squares, not the primes themselves."),
    B("49 plus 121 is 170. That is our answer.", ANSM("ans", "49 + 121 = 170"), CIRC("ans", "170")),
    B("The trap is using 9 as the greatest one-digit prime. 9 is 3 times 3, so it is not prime. Always test before you trust."),
)

LESSONS["EXT_G4_FP_2025_008"] = LESSON(
    B("Four pairs of numbers. Three pairs have the same H C F, and one pair is different. Let's find each H C F.",
      GIVEN("q", "Which pair has a different HCF?"), LB("o", "30 & 45,  45 & 60,  15 & 75,  30 & 90")),
    B("30 and 45. Both are in the 15 times table: 15 times 2, and 15 times 3. 2 and 3 share nothing more, so the H C F is 15.",
      W("a", "30 = 15 × 2"), W("a2", "45 = 15 × 3"), LB("a3", "HCF of 30 and 45 = 15")),
    B("45 and 60. That is 15 times 3, and 15 times 4. Again the H C F is 15.",
      W("b", "60 = 15 × 4"), LB("b2", "HCF of 45 and 60 = 15")),
    Q("15 and 75. 15 times 5 is 75, so 15 divides 75. What is their H C F?", ["15", "75", "5"], 0,
      "When the smaller number divides the bigger one, the smaller number is the H C F. Here that is 15.",
      W("c", "75 = 15 × 5")),
    B("15 again. That is three pairs with an H C F of 15.", LB("c2", "HCF of 15 and 75 = 15")),
    B("Last pair: 30 and 90. 30 times 3 is 90, so 30 divides 90. That makes the H C F 30. This pair is the different one!",
      W("d", "90 = 30 × 3"), LB("d2", "HCF of 30 and 90 = 30"), ANS("ans", "30, 90"), CIRC("ans", "30, 90")),
    B("The trap is saying 15 for the last pair too. 15 does divide 30 and 90, but 30 divides both as well, and 30 is higher."),
)

LESSONS["EXT_G4_FP_2025_022"] = LESSON(
    B("What fraction of all the two-digit numbers are prime? We need two counts: how many two-digit numbers, and how many two-digit primes.",
      GIVEN("q", "Fraction of 2-digit numbers that are prime = ?")),
    Q("The two-digit numbers run from 10 to 99. How many are there?", ["90", "89", "99"], 0,
      "From 1 to 99 there are 99 numbers. Take away the 9 one-digit numbers, and 90 are left.",
      LB("r", "2-digit numbers: 10 to 99")),
    B("There are 90. Careful: 99 minus 10 gives 89, and that misses one end. Take the 9 one-digit numbers away from 99 instead.",
      W("a", "99 − 9 = 90")),
    B("Now the two-digit primes. Here they all are, from 11 up to 97, with 7 in each row.",
      LB("p1", "11, 13, 17, 19, 23, 29, 31"), LB("p2", "37, 41, 43, 47, 53, 59, 61"), LB("p3", "67, 71, 73, 79, 83, 89, 97")),
    B("3 rows of 7 makes 21 primes. Some numbers only look prime: 51, 57 and 87 are in the 3 times table, and 91 is 7 times 13.",
      W("c", "3 × 7 = 21"), W("t1", "51 = 3 × 17"), W("t2", "57 = 3 × 19"), W("t3", "87 = 3 × 29"), W("t4", "91 = 7 × 13")),
    Q("So the fraction is 21 out of 90. Both numbers are in the 3 times table. What is the fraction in its simplest form?",
      ["7/30", "7/18", "21/30"], 0,
      "Divide the top and the bottom by 3. 21 divided by 3 is 7, and 90 divided by 3 is 30."),
    B("21 divided by 3 is 7, and 90 divided by 3 is 30. So the fraction is 7 out of 30.",
      W("f", "21 ÷ 3 = 7"), W("g", "90 ÷ 3 = 30"), ANSM("ans", "21/90 = 7/30"), CIRC("ans", "7/30")),
    B("So the plan was: count the whole group, count the part we want, write part over whole, and simplify."),
)

LESSONS["EXT_G4_FP_2025_024"] = LESSON(
    B("A number is divisible by 9. Which of these must then be true, every single time?",
      GIVEN("q", "A number is divisible by 9. What is always true?"), LB("o", "Divisible by 12, by 6, by 3, or by 18?")),
    B("Always true means true for every multiple of 9. So if we find just one multiple of 9 where a choice breaks, that choice is out."),
    B("Let's test with 27. 27 divided by 9 is 3, so 27 is a multiple of 9. And notice that 27 is odd.",
      W("a", "27 ÷ 9 = 3")),
    Q("27 is odd. Can 6, 12 or 18 divide an odd number exactly?", ["No, their multiples are all even", "Yes, sometimes"], 0,
      "6, 12 and 18 are even, so every number in their tables is even. An odd number like 27 cannot be in those tables."),
    B("So 12, 6 and 18 are all out. They work for some multiples of 9, but not for every one.",
      STRIKE("o", "12"), STRIKE("o", "6"), STRIKE("o", "18")),
    B("Why does 3 always work? Because 9 is 3 times 3. Anything built from 9s is built from 3s. Look: 27 divided by 3 is 9.",
      W("b", "9 = 3 × 3"), W("c", "27 ÷ 3 = 9"), ANS("ans", "Divisible by 3"), CIRC("ans", "Divisible by 3")),
    B("So remember: if 9 divides a number, then every factor of 9 divides it too. And 3 is a factor of 9."),
)

LESSONS["EXT_G4_FP_2025_025"] = LESSON(
    B("We want the greatest three-digit number that both 12 and 18 divide exactly.",
      GIVEN("q", "Greatest 3-digit number divisible by 12 and 18 = ?")),
    B("A number that 12 and 18 both divide is a common multiple. So first find the L C M. Count up in 18s: 18, then 36. And 12 times 3 is 36.",
      LB("m", "Multiples of 18: 18, 36"), W("a", "36 = 12 × 3"), LB("l", "LCM = 36")),
    Q("So our number must be in which times table?", ["the 36 times table", "the 6 times table", "the 12 times table only"], 0,
      "Every number that 12 and 18 both divide is a multiple of their L C M. And the L C M is 36."),
    B("Now we hunt for the biggest multiple of 36 with three digits. A good landmark: 36 times 25 is 900.",
      W("b", "36 × 25 = 900")),
    B("Keep adding 36. 900 plus 36 is 936. 936 plus 36 is 972. One more gives 1008, and that has four digits.",
      W("c", "900 + 36 = 936"), W("d", "936 + 36 = 972"), W("e", "972 + 36 = 1008"), STRIKE("e", "1008", "4 digits")),
    B("So the greatest three-digit number is 972. That is 36 times 27.",
      W("f", "36 × 27 = 972"), ANS("ans", "972"), CIRC("ans", "972")),
    B("The trap is stopping at 936. Both numbers divide it, but it is not the greatest. Keep adding until the next one is too big."),
)

LESSONS["EXT_G4_FP_2025_026"] = LESSON(
    B("Find the greatest two-digit number in the 13 times table. Then square it.",
      GIVEN("q", "(greatest 2-digit multiple of 13)² = ?")),
    B("Count up in 13s near the top of the two-digit numbers. 13 times 7 is 91. 13 times 8 is 104.",
      W("a", "13 × 7 = 91"), W("b", "13 × 8 = 104")),
    Q("So what is the greatest two-digit multiple of 13?", ["91", "104", "78"], 0,
      "104 has three digits, so it is too big. 91 is the last one with two digits."),
    B("It is 91. Now square it: 91 times 91. Split it up. First 91 times 90. 91 times 9 is 819, so 91 times 90 is 8190.",
      W("c0", "91 × 9 = 819"), W("c", "91 × 90 = 8190")),
    B("We need 91 lots of 91, and we have 90 lots. So add one more 91. 8190 plus 91 is 8281.",
      W("d", "8190 + 91 = 8281"), ANSM("ans", "91² = 8281"), CIRC("ans", "8281")),
    B("One trap: 78 is in the 13 times table too, because 13 times 6 is 78. But 91 is bigger, and it still has two digits.",
      W("e", "13 × 6 = 78")),
    B("So: find the number first, then square it by splitting the multiplication into easy parts."),
)

LESSONS["EXT_G4_FP_2025_030"] = LESSON(
    B("A five-digit number: 2, 5, N, 4, 8. It is a multiple of 12. Which digit is N?",
      GIVEN("q", "25N48 is a multiple of 12.  N = ?"), LB("o", "Choices: 6, 7, 8, 9")),
    B("12 is 3 times 4. So the number must pass two tests: the test for 3, and the test for 4.", W("a", "12 = 3 × 4")),
    B("Test for 4: look only at the last two digits, 48. 48 divided by 4 is 12, with nothing left over. So this test is passed, whatever N is.",
      UL("q", "48"), W("b", "48 ÷ 4 = 12")),
    B("Test for 3: the digits must add up to a number in the 3 times table. The digits we know are 2, 5, 4 and 8. They add up to 19.",
      W("c", "2 + 5 + 4 + 8 = 19")),
    Q("So 19 plus N must be in the 3 times table. Which choice does that?", ["8", "6", "7", "9"], 0,
      "Add each choice to 19 and test the total. Only one total is in the 3 times table, and that is 19 plus 8."),
    B("19 plus 6 is 25, 19 plus 7 is 26, and 19 plus 9 is 28. None of those is in the 3 times table. But 19 plus 8 is 27, and 27 is 3 times 9.",
      W("d1", "19 + 6 = 25"), W("d2", "19 + 7 = 26"), W("d3", "19 + 9 = 28"), W("d4", "19 + 8 = 27"), W("e", "27 = 3 × 9")),
    B("So N is 8, and the number is 25848.", LB("n", "25848"), ANS("ans", "N = 8"), CIRC("ans", "N = 8")),
    B("So for 12, use two tests: the last two digits for 4, and the digit sum for 3."),
)

LESSONS["G4A_FACTORS_001"] = LESSON(
    B("Which of these numbers is a factor of 36? A factor of 36 is a number that divides 36 exactly.",
      GIVEN("q", "Which is a factor of 36?  8, 9, 10, 14")),
    B("Here is another way to say it. A number is a factor of 36 if 36 is in its times table. So let's check each table."),
    B("8 first. 8 times 4 is 32, and 8 times 5 is 40. The 8 times table jumps right over 36. So 8 is out.",
      W("a", "8 × 4 = 32"), W("b", "8 × 5 = 40"), STRIKE("q", "8")),
    B("Multiples of 10 always end in 0, and 36 does not. For 14: 14 times 2 is 28, and 14 times 3 is 42. That skips 36 too.",
      W("c", "14 × 2 = 28"), W("d", "14 × 3 = 42"), STRIKE("q", "10"), STRIKE("q", "14")),
    Q("Now 9. Count up in 9s: 9, 18, 27, 36. So 9 times what makes 36?", ["4", "3", "5"], 0,
      "Count the jumps: 9, 18, 27, 36. That is 4 jumps, so 9 times 4 is 36.",
      LB("e", "9, 18, 27, 36")),
    B("9 times 4 is 36, with nothing left over. So 9 is a factor of 36.",
      W("f", "9 × 4 = 36"), ANS("ans", "9 is a factor of 36"), CIRC("ans", "9")),
    B("So to test for a factor, ask: is the big number in this number's times table? If yes, it is a factor."),
)
