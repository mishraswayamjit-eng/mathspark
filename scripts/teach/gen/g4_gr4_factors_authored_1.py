"""Hand-written lessons, part 1: past-paper questions 2020 to 2022, and the HCF × LCM questions."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANS, ANSM, B, CIRC, GIVEN, LB, LESSON, Q, STRIKE, TABLE, UL, W,
)

LESSONS = {}

LESSONS["EXT_G4_FP_2020_007"] = LESSON(
    B("We need two prime numbers: the smallest one above 50, and the greatest one below 50. Then we multiply them.",
      GIVEN("q", "(smallest prime > 50) × (greatest prime < 50) = ?")),
    B("A prime number has exactly two factors: 1 and itself. Let's hunt just above 50. 51 looks prime, but 3 times 17 is 51. And 52 is even.",
      W("a", "51 = 3 × 17"), LB("b", "52 is even")),
    Q("So what is the smallest prime above 50?", ["53", "51", "52"], 0,
      "51 is 3 times 17, and 52 is even, so both are out. 53 has no factors except 1 and itself."),
    B("53 it is. Now look just below 50. Careful: 49 is 7 times 7, so it is not prime. 48 is even. So the greatest prime below 50 is 47.",
      LB("p1", "Smallest prime above 50: 53"), W("c", "49 = 7 × 7"), LB("c2", "48 is even"),
      LB("p2", "Greatest prime below 50: 47")),
    B("Now multiply 53 by 47. Here is a neat way. 47 is 50 take away 3. So work out 53 times 50, then take away 53 times 3.",
      W("m1", "53 × 50 = 2650"), W("m2", "53 × 3 = 159")),
    B("53 times 50 is 2650. 53 times 3 is 159. And 2650 minus 159 is 2491.",
      W("m3", "2650 − 159 = 2491"), ANSM("ans", "53 × 47 = 2491"), CIRC("ans", "2491")),
    B("The trap in this one is 51 and 49. They look prime, but they are not. Always test with 3 and with 7 before you trust a number."),
)

LESSONS["EXT_G4_FP_2020_014"] = LESSON(
    B("Which of these four numbers can be divided exactly by 9? We do not need long division. There is a quick test.",
      GIVEN("q", "Divisible by 9?  5776, 5446, 6228, 5969")),
    B("Here is the test for 9. Add up the digits of the number. If the digit sum is in the 9 times table, the number is too.",
      LB("r", "Test for 9: add the digits")),
    B("Try 5776. 5 plus 7 plus 7 plus 6 is 25. 25 is not in the 9 times table, so 5776 is out.",
      W("a", "5 + 7 + 7 + 6 = 25"), STRIKE("q", "5776")),
    B("5446 gives 19, and 5969 gives 29. Neither of those is in the 9 times table.",
      W("b", "5 + 4 + 4 + 6 = 19"), W("d", "5 + 9 + 6 + 9 = 29"), STRIKE("q", "5446"), STRIKE("q", "5969")),
    Q("Now 6228. What do its digits add up to?", ["18", "16", "20"], 0,
      "Add them slowly. 6 plus 2 is 8. Plus 2 more is 10. Plus 8 is 18."),
    B("6 plus 2 plus 2 plus 8 is 18, and 18 is 9 times 2. So 6228 is divisible by 9.",
      W("c", "6 + 2 + 2 + 8 = 18"), W("c2", "18 = 9 × 2"), ANS("ans", "6228 is divisible by 9"), CIRC("ans", "6228")),
    B("Remember the test for 9: add the digits, and see if the total is in the 9 times table. It saves a lot of dividing!"),
)

LESSONS["EXT_G4_FP_2020_015"] = LESSON(
    B("A roll number puzzle with three clues. It is not a multiple of 3. It is not a perfect square. And its digits add up to a prime number.",
      GIVEN("q", "Roll number: 16, 14, 12 or 26?"), LB("r", "Not a multiple of 3. Not a square. Digit sum is prime.")),
    B("Let's use one clue at a time and cross numbers out. First clue: not a multiple of 3. But 12 is 3 times 4, so 12 is out.",
      W("a", "12 = 3 × 4"), STRIKE("q", "12")),
    Q("Second clue: not a perfect square. Which of these is a perfect square?", ["16", "14", "26"], 0,
      "A perfect square is a number times itself. 4 times 4 is 16, so 16 is a perfect square."),
    B("4 times 4 is 16, so 16 is out too.", W("b", "16 = 4 × 4"), STRIKE("q", "16")),
    B("Two are left: 14 and 26. Last clue: the digits add up to a prime. For 26, 2 plus 6 is 8. And 8 is not prime, because 2 times 4 is 8.",
      W("c", "2 + 6 = 8"), STRIKE("q", "26")),
    B("For 14, 1 plus 4 is 5, and 5 is prime. So the roll number is 14.",
      W("d", "1 + 4 = 5"), ANS("ans", "Roll number = 14"), CIRC("ans", "14")),
    B("When a puzzle has several clues, take them one at a time and cross out what does not fit. Whatever is left is the answer."),
)

LESSONS["EXT_G4_FP_2020_016"] = LESSON(
    B("Four square numbers: 4, 9, 16 and 25. One of them can be made by adding two prime numbers in two different ways. Which one?",
      GIVEN("q", "4, 9, 16, 25: which is prime + prime in two ways?")),
    B("Start with 4. The only way is 2 plus 2. That is just one way.", W("a", "4 = 2 + 2")),
    B("Now the key idea. 9 and 25 are odd. Two odd primes always add up to an even number. So to make an odd total, one of the primes must be 2, the only even prime.",
      LB("k", "odd + odd = even")),
    B("So for 9 the only way is 2 plus 7. For 25 the only way is 2 plus 23. One way each.",
      W("b", "9 = 2 + 7"), W("c", "25 = 2 + 23")),
    Q("That leaves 16. One way is 3 plus 13. Which of these is another way, using two primes?", ["5 + 11", "7 + 9", "1 + 15"], 0,
      "Both numbers must be prime. 9 is 3 times 3, 15 is 3 times 5, and 1 is not a prime. But 5 and 11 are both prime.",
      W("d", "16 = 3 + 13")),
    B("16 is 3 plus 13, and also 5 plus 11. Two different ways! So the answer is 16.",
      W("e", "16 = 5 + 11"), ANS("ans", "Answer: 16"), CIRC("ans", "16")),
    B("The trap is 7 plus 9. It does make 16, but 9 is not prime. And remember the key idea: an odd total always needs the prime 2."),
)

LESSONS["EXT_G4_FP_2020_036"] = LESSON(
    B("How many two-digit numbers can be divided exactly by 4, by 6 and by 8? Notice that it asks how many, not which one.",
      GIVEN("q", "How many 2-digit numbers are divisible by 4, 6 and 8?")),
    B("A number that 4, 6 and 8 all divide is a common multiple of them. So first find the lowest one, the L C M. Count up in 8s: 8, 16, 24.",
      LB("m", "Multiples of 8: 8, 16, 24")),
    Q("Which is the first of these that 4 and 6 both divide?", ["24", "8", "16"], 0,
      "6 does not go into 8 or 16 exactly. But 6 times 4 is 24, and 4 times 6 is 24. So 24 is the first."),
    B("24 it is: 4 times 6, and 8 times 3. So every number we want is in the 24 times table.",
      W("a", "24 = 4 × 6"), W("b", "24 = 8 × 3"), LB("l", "LCM = 24")),
    B("Now count up in 24s, and keep only the two-digit ones: 24, 48, 72, 96. The next one is 120, and that has three digits.",
      LB("t", "24, 48, 72, 96, 120"), STRIKE("t", "120", "3 digits")),
    Q("So how many two-digit numbers are there?", ["4", "24", "3"], 0,
      "Count the ones left on the board: 24, 48, 72 and 96. That is 4 numbers."),
    B("There are 4 of them. Careful: 24 is the smallest such number, but the question asked how many there are.",
      ANS("ans", "4 numbers"), CIRC("ans", "4 numbers")),
    B("So the plan was: find the L C M first, then count the multiples of it that fit."),
)

STAR_HEADERS = ["Thousands", "Hundreds", "Tens", "Ones"]

LESSONS["EXT_G4_FP_2020_040"] = LESSON(
    B("A four-digit number: 2, star, 1, star. Both stars are the same digit, and 11 divides the number exactly. Which digit is the star?",
      GIVEN("q", "2★1★ is divisible by 11.  ★ = ?"),
      TABLE("f", [["2", "★", "1", "★"]], headers=STAR_HEADERS, note="Both stars are the same digit.")),
    B("Here is the test for 11. Add the 1st and 3rd digits. Then add the 2nd and 4th digits. The two sums must be equal, or differ by 11.",
      LB("r", "Test for 11: two sums equal, or differ by 11")),
    B("The 1st and 3rd digits are 2 and 1. They add up to 3.", W("a", "2 + 1 = 3"), UL("q", "2"), UL("q", "1")),
    B("The 2nd and 4th digits are the two stars. The same digit twice is double that digit. Double a digit is always even, so it can never be 3."),
    Q("So the two sums cannot be equal. They must differ by 11. What must the two stars add up to?", ["14", "3", "11"], 0,
      "We need a sum that is 11 more than 3. And 3 plus 11 is 14."),
    B("3 plus 11 is 14. So the two stars add up to 14, and half of 14 is 7. Each star is 7.",
      W("b", "3 + 11 = 14"), W("c", "14 ÷ 2 = 7"), ANS("ans", "★ = 7"), CIRC("ans", "★ = 7")),
    B("Let's check. The number is 2717, and 11 times 247 is 2717. It works!", W("d", "11 × 247 = 2717")),
    B("So for 11: add every other digit, and compare the two sums. They must be equal, or 11 apart."),
)


def swap_73251(open_say, close_say):
    return LESSON(
        B(open_say, W("q", "73251", "given")),
        B("6 is 2 times 3. So a number that 6 divides must pass two tests: the test for 2, and the test for 3.",
          W("a", "6 = 2 × 3")),
        B("Test for 3: add the digits. 7 plus 3 plus 2 plus 5 plus 1 is 18, and 18 is in the 3 times table. Swapping digits never changes the sum, so this test is always passed.",
          W("b", "7 + 3 + 2 + 5 + 1 = 18")),
        Q("Test for 2: the number must be even. So what kind of digit must be at the end?",
          ["an even digit", "an odd digit", "the biggest digit"], 0,
          "Even numbers end in 0, 2, 4, 6 or 8. So the last digit has to be even."),
        B("Look at the digits: 7, 3, 2, 5, 1. Only one of them is even: the 2. So the 2 must move to the end, where the 1 is now.",
          CIRC("q", "2"), CIRC("q", "1")),
        B("Swap the 2 and the 1, and we get 73152. It ends in 2, so it is even, and its digits still add to 18.",
          W("c", "73152"), ANS("ans", "Swap 2 & 1"), CIRC("ans", "2 & 1")),
        B("The trap is swapping the 2 with some other digit, or leaving it where it is. Then the number still ends in an odd digit, and 6 can never divide an odd number."),
        B(close_say),
    )


LESSONS["EXT_G4_FP_2021_020"] = swap_73251(
    "Here is the number 73251. We may swap two of its digits so that 6 divides it exactly. Which two should we swap?",
    "So for 6, think of two tests together: even at the end for 2, and a digit sum in the 3 times table for 3.")
LESSONS["PYQ_2019_Q12"] = swap_73251(
    "Look at 73251. Two of its digits change places, and then 6 must divide the new number exactly. Which two digits?",
    "Remember: divisible by 6 means divisible by 2 and by 3. Check the digit sum for 3, and the last digit for 2.")

LESSONS["EXT_G4_FP_2021_025"] = LESSON(
    B("Five numbers this time! We need the L C M: the lowest number that all five of them divide exactly.",
      GIVEN("q", "LCM of 14, 35, 40, 56, 28 = ?")),
    B("First, make the job smaller. 14 and 28 both divide 56. So any multiple of 56 already takes care of them, and we can set them aside.",
      W("a", "56 = 14 × 4"), W("b", "56 = 28 × 2"), STRIKE("q", "14"), STRIKE("q", "28")),
    B("Now break the other three into primes. 35 is 5 times 7. 40 is 2 times 2 times 2 times 5. 56 is 2 times 2 times 2 times 7.",
      W("c", "35 = 5 × 7"), W("d", "40 = 2 × 2 × 2 × 5"), W("e", "56 = 2 × 2 × 2 × 7")),
    Q("The L C M needs each prime the most times it shows up in any one number. So how many 2s does it need?",
      ["three", "six", "one"], 0,
      "40 has three 2s, and 56 has three 2s. We do not add them up. We take the most in any one number, which is three."),
    B("So we take three 2s, one 5 and one 7. 2 times 2 times 2 is 8. 8 times 5 is 40. And 40 times 7 is 280.",
      W("f", "2 × 2 × 2 × 5 × 7 = 280"), ANS("ans", "LCM = 280"), CIRC("ans", "LCM = 280")),
    B("Check the two biggest. 280 divided by 40 is 7, and 280 divided by 56 is 5. Both are exact.",
      W("g", "280 ÷ 40 = 7"), W("h", "280 ÷ 56 = 5")),
    B("Careful with 560. All five numbers divide it too, but it is double 280, so it is not the lowest.",
      W("i", "280 × 2 = 560")),
    B("So for an L C M of many numbers: drop the ones that divide a bigger one, split the rest into primes, and take each prime the most times it appears."),
)


def product_lesson(first, lcm_first, hcf, lcm, known, other, product, working, check_extra):
    """HCF × LCM = product of the two numbers. `working` is the beat that does the dividing."""
    if lcm_first:
        given = "LCM = %d, HCF = %d. One number is %d. Other = ?" % (lcm, hcf, known)
        a, b = lcm, hcf
    else:
        given = "HCF = %d, LCM = %d. One number is %d. Other = ?" % (hcf, lcm, known)
        a, b = hcf, lcm
    return LESSON(
        B(first, GIVEN("q", given)),
        B("Here is a handy fact. For any two numbers, the H C F times the L C M equals the two numbers multiplied together.",
          LB("f", "HCF × LCM = one number × other number")),
        B("So %d times %d is the same as %d times the other number. And %d times %d is %d." % (a, b, known, a, b, product),
          W("a", "%d × %d = %d" % (a, b, product))),
        Q("So %d is %d times the other number. How do we find the other number?" % (product, known),
          ["%d ÷ %d" % (product, known), "%d × %d" % (product, known), "%d − %d" % (product, known)], 0,
          "Times and divide are partners. To undo times %d, we divide by %d." % (known, known)),
        working,
        B("Let's check. %d times %d is %d as well. %s" % (known, other, product, check_extra[0]),
          W("c", "%d × %d = %d" % (known, other, product)), W("d", check_extra[1])),
        B("So remember: H C F times L C M gives the product of the two numbers. Divide by the number you know, and the other one appears."),
    )


LESSONS["EXT_G4_FP_2022_003"] = product_lesson(
    "Two mystery numbers. Their H C F is 15 and their L C M is 600. One of the numbers is 120. We must find the other.",
    False, 15, 600, 120, 75, 9000,
    B("9000 divided by 120. Take one zero off each, and it is 900 divided by 12, which is 75.",
      W("b", "9000 ÷ 120 = 75"), W("b2", "900 ÷ 12 = 75"), ANS("ans", "Other number = 75"), CIRC("ans", "75")),
    ("And 15 goes into 75 exactly 5 times, just as an H C F should.", "75 ÷ 15 = 5"))

LESSONS["EXT_G4_FP_2023_027"] = product_lesson(
    "Two mystery numbers. Their L C M is 2040 and their H C F is 8. One of the numbers is 120. We must find the other.",
    True, 8, 2040, 120, 136, 16320,
    B("16320 divided by 120. Take one zero off each, and it is 1632 divided by 12, which is 136.",
      W("b", "16320 ÷ 120 = 136"), W("b2", "1632 ÷ 12 = 136"), ANS("ans", "Other number = 136"), CIRC("ans", "136")),
    ("And 8 goes into 136 exactly 17 times, just as an H C F should.", "136 ÷ 8 = 17"))

LESSONS["Q_CH06_021"] = product_lesson(
    "Two mystery numbers. Their H C F is 6 and their L C M is 36. One of the numbers is 12. We must find the other.",
    False, 6, 36, 12, 18, 216,
    B("216 divided by 12. 12 times 10 is 120, and 12 times 8 is 96. Together that is 216, so the answer is 18.",
      W("b0", "120 + 96 = 216"), W("b", "216 ÷ 12 = 18"), ANS("ans", "Other number = 18"), CIRC("ans", "18")),
    ("And 6 goes into 18 exactly 3 times, just as an H C F should.", "18 ÷ 6 = 3"))

LESSONS["EXT_G4_FP_2022_027"] = LESSON(
    B("A five-digit number: 3, A, A, 4, 8. Both A's are the same digit. We want the greatest digit for A that lets 12 divide the number.",
      GIVEN("q", "3A,A48 is divisible by 12. Greatest A = ?")),
    B("12 is 3 times 4. So the number must pass two tests: the test for 3, and the test for 4.", W("a", "12 = 3 × 4")),
    B("Test for 4: look only at the last two digits, 48. 48 divided by 4 is 12, with nothing left over. So this test is passed, whatever A is.",
      UL("q", "48"), W("b", "48 ÷ 4 = 12")),
    B("Test for 3: the digits must add up to a number in the 3 times table. The digits we know are 3, 4 and 8. They add up to 15.",
      W("c", "3 + 4 + 8 = 15")),
    Q("A is there twice. We want the greatest digit, so try 9 first. 15 plus 9 plus 9 is 33. Is 33 in the 3 times table?",
      ["Yes, 3 × 11 = 33", "No, it is not"], 0,
      "3 times 11 is 33. So 33 is in the 3 times table.",
      W("d", "15 + 9 + 9 = 33")),
    B("33 is 3 times 11, so A equals 9 works. No digit is bigger than 9, so we are done. The number is 39,948.",
      W("e", "33 = 3 × 11"), LB("n", "39,948"), ANS("ans", "A = 9"), CIRC("ans", "A = 9")),
    B("Here is the trap. 3 works as well, because 15 plus 3 plus 3 is 21. But the question asks for the greatest digit, so always start from the top.",
      W("f", "15 + 3 + 3 = 21")),
    B("So for 12, use two tests: the last two digits for 4, and the digit sum for 3."),
)

LESSONS["EXT_G4_FP_2022_036"] = LESSON(
    B("A four-digit number: 9, star, 3, star. Both stars are the same digit, and 11 divides the number exactly. Which digit is the star?",
      GIVEN("q", "9★3★ is divisible by 11.  ★ = ?"), LB("o", "Choices: 4, 5, 7, None of these"),
      TABLE("f", [["9", "★", "3", "★"]], headers=STAR_HEADERS, note="Both stars are the same digit.")),
    B("Here is the test for 11. Add the 1st and 3rd digits. Then add the 2nd and 4th digits. The two sums must be equal, or differ by 11.",
      LB("r", "Test for 11: two sums equal, or differ by 11")),
    B("The 1st and 3rd digits are 9 and 3. They add up to 12.", W("a", "9 + 3 = 12"), UL("q", "9"), UL("q", "3")),
    Q("The two stars are the 2nd and 4th digits. For the two sums to be equal, what must the two stars add up to?",
      ["12", "11", "6"], 0,
      "The two sums must match. The first sum is 12, so the two stars must add up to 12 as well."),
    B("Two equal digits that add up to 12: each one is 6. So the star is 6.", W("b", "6 + 6 = 12"), LB("s", "★ = 6")),
    B("Let's check. The number is 9636, and 11 times 876 is 9636. It works.", W("c", "11 × 876 = 9636")),
    Q("Now look at the choices: 4, 5, 7, or none of these. Which one do we pick?", ["None of these", "7", "5"], 0,
      "Our digit is 6. It is not 4, 5 or 7, so the right choice is none of these."),
    B("6 is not in the list, so the answer is none of these. Do not let that shake you. When your working checks out, trust it.",
      ANS("ans", "None of these (★ = 6)"), CIRC("ans", "None of these")),
)

LESSONS["EXT_G4_FP_2022_037"] = LESSON(
    B("The letter Q stands for the greatest two-digit number. We must write the smallest two-digit prime using Q.",
      GIVEN("q", "Q = greatest 2-digit number"), LB("q2", "Smallest 2-digit prime = Q − ?")),
    Q("First, what is the greatest two-digit number?", ["99", "100", "90"], 0,
      "100 has three digits. The biggest number with just two digits is 99."),
    B("So Q is 99.", LB("a", "Q = 99")),
    B("Now the smallest two-digit prime. The smallest two-digit number is 10, but 10 is 2 times 5, so it is not prime. Next comes 11. Its only factors are 1 and 11, so 11 is prime.",
      W("b", "10 = 2 × 5"), LB("c", "Smallest 2-digit prime: 11")),
    Q("What must we take away from 99 to leave 11?", ["88", "89", "84"], 0,
      "99 take away 11 is 88. So taking 88 away from 99 leaves 11."),
    B("99 minus 88 is 11. So the smallest two-digit prime is Q minus 88.",
      W("d", "99 − 88 = 11"), ANS("ans", "Q − 88"), CIRC("ans", "Q − 88")),
    B("The trap is Q minus 89. That gives 10, the smallest two-digit number. But 10 is not prime.", W("e", "99 − 89 = 10")),
)
