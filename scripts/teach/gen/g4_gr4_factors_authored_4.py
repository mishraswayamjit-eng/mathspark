"""Hand-written lessons, part 4: G4A_FACTORS_025 to 032, and the past-paper questions PYQ 2016 to 2019."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANS, ANSM, B, CIRC, FIG, GIVEN, LB, LESSON, Q, STRIKE, TABLE, VENN, W,
)

LESSONS = {}

LESSONS["G4A_FACTORS_025"] = LESSON(
    B("Rina has fewer than 50 sweets. Packed in fives, 3 are left over. Packed in sevens, 2 are left over. How many sweets does she have?",
      GIVEN("q", "Fewer than 50. In 5s: 3 left. In 7s: 2 left.")),
    B("Start with the sevens clue. 2 left over means the number is 2 more than something in the 7 times table. So add 2 to each multiple of 7.",
      LB("s", "7 times table: 7, 14, 21, 28, 35, 42"), LB("t", "Add 2:  9, 16, 23, 30, 37, 44")),
    B("Now the fives clue. Numbers in the 5 times table end in 0 or 5. So a number with 3 left over must end in 3 or 8."),
    Q("Which number in our list ends in 3 or 8?", ["23", "37", "30"], 0,
      "Look at the last digit of each number in the list. Only 23 ends in 3, and none of them ends in 8."),
    B("23 fits both clues. It is 20 and 3 more: four fives, with 3 left over. And it is 21 and 2 more: three sevens, with 2 left over.",
      CIRC("t", "23"), W("a", "23 = 20 + 3"), W("b", "23 = 21 + 2"), ANS("ans", "23 sweets"), CIRC("ans", "23 sweets")),
    B("Here is the trap. 37 fits the sevens clue, but in fives it is 35 and 2 more. That is 2 left over, not 3.",
      W("c", "37 = 35 + 2")),
    B("So with two clues: list the numbers that fit one clue, then test them with the other. The answer must fit both."),
)

LESSONS["G4A_FACTORS_026"] = LESSON(
    B("Children stand in rows. In rows of 6, the last row has only 5. In rows of 8, the last row has only 7. There are between 40 and 60 children.",
      GIVEN("q", "Rows of 6: last row 5. Rows of 8: last row 7."), LB("q2", "More than 40, fewer than 60. How many?")),
    B("Look closely at the clues. 5 is 1 short of 6. And 7 is 1 short of 8. Each time, the last row is just 1 child short."),
    Q("Imagine 1 more child joins the class. What happens to the rows?",
      ["Every row is full", "Nothing changes", "Two rows are short"], 0,
      "The last row is missing just 1 child each time. One more child fills it, so every row is full."),
    B("So the number of children, plus 1, makes full rows of 6 and full rows of 8. It is a common multiple of 6 and 8. Those are 24, 48, 72.",
      LB("m", "Common multiples of 6 and 8: 24, 48, 72")),
    B("The class has between 40 and 60 children. The only common multiple that fits is 48.", CIRC("m", "48")),
    B("Now send the extra child away again. 48 minus 1 is 47. There are 47 children.",
      ANSM("ans", "48 − 1 = 47"), CIRC("ans", "47")),
    B("Let's check. 47 is 42 and 5 more: 7 full rows of 6, then a row of 5. And 47 is 40 and 7 more: 5 full rows of 8, then a row of 7.",
      W("c", "47 = 42 + 5"), W("d", "47 = 40 + 7")),
    B("Two traps. 48 children would fill every row exactly. And 49 comes from adding 1 at the end, when we should take it away.",
      W("t", "48 + 1 = 49")),
)

LESSONS["G4A_FACTORS_027"] = LESSON(
    B("A two-digit prime below 50. Its digits add up to 10. And when the digits swap places, the new number is prime as well. Which is it?",
      GIVEN("q", "2-digit prime below 50. Digits add to 10."), LB("q2", "Swapped, it is still prime. 19, 13, 37 or 17?")),
    B("First clue: the digits add up to 10. 1 plus 9 is 10. 3 plus 7 is 10. But 1 plus 3 is only 4, and 1 plus 7 is only 8. So 13 and 17 are out.",
      W("a", "1 + 9 = 10"), W("b", "3 + 7 = 10"), W("c", "1 + 3 = 4"), W("d", "1 + 7 = 8"),
      STRIKE("q2", "13"), STRIKE("q2", "17")),
    Q("19 and 37 are left, and both are prime. Now swap the digits. 19 becomes 91. Is 91 a prime number?",
      ["No, 7 × 13 = 91", "Yes, it is prime"], 0,
      "91 looks prime, but 7 times 13 is 91. So it is not a prime number.",
      LB("s1", "19 swapped is 91")),
    B("91 is 7 times 13, so it is not prime. That knocks out 19.", W("e", "91 = 7 × 13"), STRIKE("q2", "19")),
    B("Now 37 swapped is 73. Test it. It is odd. Its digits add to 10, so 3 does not divide it. It does not end in 0 or 5. And 7 skips it: 70, then 77.",
      LB("s2", "37 swapped is 73"), W("f", "7 × 10 = 70"), W("g", "7 × 11 = 77")),
    B("So 73 is prime, and 37 is prime. The number is 37.", ANS("ans", "37"), CIRC("ans", "37")),
    B("The big trap here is 91. It is in the 7 times table, just past where most of us stop learning it."),
)

LESSONS["G4A_FACTORS_028"] = LESSON(
    B("Two prime numbers add up to 25. We must find them, and then multiply them.",
      GIVEN("q", "prime + prime = 25. Their product = ?")),
    B("Here is the key idea. 25 is odd. But two odd numbers always add up to an even number. So the two primes cannot both be odd.",
      LB("k", "odd + odd = even")),
    Q("So one of the primes must be even. Which is the only even prime number?", ["2", "4", "There is none"], 0,
      "Every even number bigger than 2 can be divided by 2, so it is not prime. 2 is the only even prime."),
    B("One prime is 2. The other is 25 minus 2, which is 23. And 23 is prime: it is odd, it is not in the 3 times table, and it does not end in 0 or 5.",
      W("a", "25 − 2 = 23")),
    B("So the two primes are 2 and 23. Their product is 2 times 23, which is 46.",
      ANSM("ans", "2 × 23 = 46"), CIRC("ans", "46")),
    B("The traps are pairs like 11 and 14, or 12 and 13. They do add up to 25, but 14 and 12 are not prime.",
      W("t1", "11 + 14 = 25"), W("t2", "12 + 13 = 25")),
    B("So remember: when two primes add up to an odd number, one of them is always 2."),
)

LESSONS["G4A_FACTORS_029"] = LESSON(
    B("We want the greatest three-digit number that 6 divides exactly, but 4 does not.",
      GIVEN("q", "Greatest 3-digit number: 6 divides it, 4 does not")),
    B("Start at the top and come down. For 6, a number must be even, and its digits must add up to a number in the 3 times table. 999 is odd. 998 has a digit sum of 26. 996 has 24, which works.",
      LB("l", "999 is odd.  998 and 996 are even."), W("a", "9 + 9 + 8 = 26"), W("b", "9 + 9 + 6 = 24"), LB("c", "Greatest 3-digit multiple of 6: 996")),
    Q("Now test 996 for 4. Look at its last two digits, 96. Does 4 divide 96?", ["Yes, 4 × 24 = 96", "No, it does not"], 0,
      "4 times 24 is 96. So 4 divides 96, and that means 4 divides 996 too."),
    B("4 divides 996, so it does not fit. Step down to the next multiple of 6. 996 minus 6 is 990.",
      W("d", "96 = 4 × 24"), STRIKE("c", "996"), W("e", "996 − 6 = 990")),
    B("Test 990 for 4. Its last two digits are 90. 4 times 22 is 88, and 4 times 23 is 92. So 4 skips 90, and 4 does not divide 990.",
      LB("e2", "Last two digits of 990: 90"), W("f", "4 × 22 = 88"), W("g", "4 × 23 = 92")),
    B("And 6 does divide 990: it is even, and 9 plus 9 plus 0 is 18. So the answer is 990.",
      W("h", "9 + 9 + 0 = 18"), ANS("ans", "990"), CIRC("ans", "990")),
    B("So the plan: start from the greatest multiple of 6, and step down by 6 until the second rule fits too."),
)

LESSONS["G4A_FACTORS_030"] = LESSON(
    B("From 1 to 100, how many numbers are multiples of 4, but not multiples of 6?",
      GIVEN("q", "From 1 to 100: multiples of 4, but not of 6 = ?")),
    B("First count all the multiples of 4. 4 times 25 is 100, so there are 25 of them.", W("a", "4 × 25 = 100")),
    Q("Some of those 25 are multiples of 6 as well. The numbers in both tables are the multiples of which number?",
      ["12", "24", "6"], 0,
      "Count up in 6s: 6, then 12. 12 is the first one that 4 divides too. So the numbers in both tables are the multiples of 12."),
    B("So list the multiples of 12 up to 100. 12 times 8 is 96, so there are 8 of them.",
      LB("m", "12, 24, 36, 48, 60, 72, 84, 96"), W("b", "12 × 8 = 96")),
    B("Take those 8 away from the 25. 25 minus 8 is 17. So 17 numbers are multiples of 4 but not of 6.",
      VENN("v", "Multiples of 4", "Multiples of 6", "17", "8", "8", highlight=["left"],
           note="From 1 to 100. We want only the left part."),
      ANSM("ans", "25 − 8 = 17"), CIRC("ans", "17")),
    B("Here is the trap. There are 16 multiples of 6 up to 100. But do not take away all 16. Many of them, like 6 itself, were never multiples of 4.",
      W("t", "6 × 16 = 96")),
    B("So: count the whole group, then remove only the ones that are in both tables."),
)

LESSONS["G4A_FACTORS_031"] = LESSON(
    B("A number puzzle with four clues. It is a factor of 60. It is a multiple of 4. It is not a multiple of 3. And it is greater than 4.",
      GIVEN("q", "Factor of 60. Multiple of 4. Not a multiple of 3."), LB("o", "Greater than 4:  12, 20, 40 or 60?")),
    B("First clue: a factor of 60. 12, 20 and 60 all divide 60. But 40 does not: 40 times 2 is 80, which jumps past 60. So 40 is out.",
      W("a", "40 × 2 = 80"), STRIKE("o", "40")),
    B("Second clue: a multiple of 4. 12 is 4 times 3. 20 is 4 times 5. 60 is 4 times 15. All three pass.",
      W("b", "12 = 4 × 3"), W("c", "20 = 4 × 5"), W("d", "60 = 4 × 15")),
    Q("Third clue: not a multiple of 3. Which of 12, 20 and 60 is not in the 3 times table?", ["20", "12", "60"], 0,
      "Add the digits to test for 3. 1 plus 2 is 3, and 6 plus 0 is 6, so 12 and 60 are in the 3 times table. 2 plus 0 is 2, so 20 is not."),
    B("12 is 3 times 4, and 60 is 3 times 20. Both are multiples of 3, so they are out.",
      W("e", "12 = 3 × 4"), W("f", "60 = 3 × 20"), STRIKE("o", "12"), STRIKE("o", "60")),
    B("Only 20 is left, and it is greater than 4. So the number is 20.", ANS("ans", "20"), CIRC("ans", "20")),
    B("With several clues, take them one at a time, and cross out every number that breaks a clue."),
)

LESSONS["G4A_FACTORS_032"] = LESSON(
    B("We want the greatest number that divides 50 and 74, and leaves a remainder of 2 each time.",
      GIVEN("q", "Divides 50 and 74, remainder 2 each time. Greatest = ?")),
    B("A remainder of 2 means 2 is left over. So take the 2 away first. Then the number divides what is left exactly. 50 minus 2 is 48, and 74 minus 2 is 72.",
      W("a", "50 − 2 = 48"), W("b", "74 − 2 = 72")),
    Q("So our number divides 48 and 72 exactly, and it is as big as possible. What is that called?",
      ["their HCF", "their LCM", "their sum"], 0,
      "The biggest number that divides both exactly is the highest common factor, the H C F."),
    B("Here are the factors of 48. Test from the big end. 48 itself does not divide 72. But 24 does: 24 times 3 is 72.",
      LB("la", "Factors of 48: 1, 2, 3, 4, 6, 8, 12, 16, 24, 48"), STRIKE("la", "48", None, 2),
      W("c", "24 × 2 = 48"), W("d", "24 × 3 = 72"), CIRC("la", "24")),
    B("So the H C F of 48 and 72 is 24. That is our number.", ANS("ans", "24"), CIRC("ans", "24")),
    B("Check with the numbers we started from. 24 times 2 is 48, plus 2 is 50. 24 times 3 is 72, plus 2 is 74. A remainder of 2 each time.",
      W("e", "24 × 2 + 2 = 50"), W("f", "24 × 3 + 2 = 74")),
    B("The trap is the number 2. It is the H C F of 50 and 74, but it leaves no remainder at all. Always take the remainder away first."),
)

LESSONS["PYQ_2016_Q03"] = LESSON(
    B("In how many ways can 98 be written as one number times another? Each way is a pair of factors of 98.",
      GIVEN("q", "98 = ? × ?   How many ways?"),
      TABLE("f", [["1", "×", "98"], ["?", "×", "?"]], note="How many pairs multiply to 98?")),
    B("Every number has the pair made with 1. So the first way is 1 times 98.", W("p1", "1 × 98 = 98")),
    B("98 is even, so 2 divides it. Half of 98 is 49. The second way is 2 times 49.", W("p2", "2 × 49 = 98")),
    Q("Keep going in order. Which of these numbers divides 98 exactly?", ["7", "3", "5"], 0,
      "5 needs a last digit of 0 or 5. 3 needs a digit sum in the 3 times table. Neither works for 98. But 7 goes in exactly."),
    B("7 times 14 is 98. That is a third way. And 3, 4, 5 and 6 do not divide 98 at all.", W("p3", "7 × 14 = 98")),
    B("The next factors are 14 and 49, and both are already on the board as partners. So there are no new pairs. 98 can be written in 3 ways.",
      ANS("ans", "3 ways"), CIRC("ans", "3 ways")),
    B("The trap is 6. That is how many factors 98 has. But each way uses two factors, so six factors make three pairs.",
      LB("fl", "Factors: 1, 2, 7, 14, 49, 98")),
)


def twos_in_primes(intro, given):
    return LESSON(
        B(intro, GIVEN("q", given)),
        B("A 2 can sit in the ones place or in the tens place. Take the ones place first. Any number that ends in 2 is even."),
        Q("Which is the only prime number that ends in 2?", ["2 itself", "12", "22"], 0,
          "12 and 22 are even, so 2 divides them and they are not prime. The only even prime is 2 itself."),
        B("So the ones place gives us one 2: the prime number 2.", LB("a", "Ends in 2: only the prime 2")),
        B("Now the tens place: the numbers from 20 to 29. The even ones are not prime. That leaves the odd ones: 21, 23, 25, 27 and 29.",
          LB("b", "20 to 29, odd ones: 21, 23, 25, 27, 29")),
        B("Careful here. 21 is 3 times 7. 25 is 5 times 5. 27 is 3 times 9. None of those is prime.",
          W("c", "21 = 3 × 7"), W("d", "25 = 5 × 5"), W("e", "27 = 3 × 9"),
          STRIKE("b", "21"), STRIKE("b", "25"), STRIKE("b", "27")),
        B("23 and 29 are prime, and each has one 2. So the primes with a 2 are 2, 23 and 29. That is 3 times.",
          ANS("ans", "3 times (2, 23, 29)"), CIRC("ans", "3 times")),
        B("The trap is counting numbers like 12 and 22. They have a 2 in them, but they are not prime. And do not forget the prime 2 itself."),
    )


LESSONS["PYQ_2016_Q06"] = twos_in_primes(
    "A typist types every prime number between 1 and 100. How many times does she press the 2 key? We need the primes that have a 2 in them.",
    "Primes from 1 to 100: how many times is 2 typed?")
LESSONS["PYQ_2019_Q04"] = twos_in_primes(
    "Write down every prime number between 1 and 100. How many times is the digit 2 used? We need the primes that have a 2 in them.",
    "Primes from 1 to 100: how many times is 2 used?")

LESSONS["PYQ_2016_Q13"] = LESSON(
    B("Three numbers, each with a hidden digit: a star, a heart and a third symbol. 11 divides all three. Then we build the greatest number from the hidden digits.",
      GIVEN("q", "5★7, 57♥, Ψ59 are divisible by 11"), LB("q2", "Greatest number from ★, ♥, Ψ = ?"),
      TABLE("f", [["5", "★", "7"], ["5", "7", "♥"], ["Ψ", "5", "9"]], note="11 divides the number in each row.")),
    B("The test for 11 with three digits: add the first and last digits, then take away the middle one. The result must be 0 or 11.",
      LB("r", "first + last − middle = 0 or 11")),
    B("First number. 5 plus 7 is 12. Take away the star, and we need 0 or 11. One digit cannot bring 12 all the way down to 0, so it must leave 11.",
      W("a0", "5 + 7 = 12")),
    B("12 take away 1 is 11. So the star is 1. The number is 517, which is 11 times 47.",
      W("a", "5 + 7 − 1 = 11"), LB("a2", "★ = 1"), W("a3", "11 × 47 = 517")),
    Q("Second number: 5, 7, heart. The middle digit is 7. So 5 plus the heart, take away 7, must be 0. What is the heart?",
      ["2", "7", "12"], 0,
      "5 plus the heart must equal 7, so that taking 7 away leaves 0. And 5 plus 2 is 7."),
    B("The heart is 2. The number is 572, which is 11 times 52.",
      W("b", "5 + 2 − 7 = 0"), LB("b2", "♥ = 2"), W("b3", "11 × 52 = 572")),
    B("Third number. The hidden digit plus 9, take away 5. That is the hidden digit plus 4, which can never be 0. So it must be 11.",
      W("c0", "9 − 5 = 4")),
    B("7 plus 4 is 11, so the hidden digit is 7. The number is 759, which is 11 times 69.",
      W("c", "7 + 9 − 5 = 11"), LB("c2", "Ψ = 7"), W("c3", "11 × 69 = 759")),
    Q("The hidden digits are 1, 2 and 7. What is the greatest number we can make from them?", ["721", "712", "127"], 0,
      "For the greatest number, put the biggest digit first, then the next biggest. That is 7, then 2, then 1."),
    B("Biggest digit first: 7, then 2, then 1. The greatest number is 721.", ANS("ans", "721"), CIRC("ans", "721")),
    B("One trap: the 9 is printed in the question. It is not a hidden digit, so it cannot be used in the answer."),
)

LESSONS["PYQ_2016_Q28"] = LESSON(
    B("Four pairs of numbers. Which pair has the greatest L C M? We must work out all four before we choose.",
      GIVEN("q", "Which pair has the greatest LCM?"), LB("o", "15 & 25,  15 & 20,  15 & 18,  15 & 12")),
    B("Every pair has 15 in it. So write out the 15 times table just once, and use it four times.",
      LB("m", "Multiples of 15: 15, 30, 45, 60, 75, 90")),
    B("15 and 25. The first number in the list that 25 divides is 75, because 25 times 3 is 75.",
      W("a", "25 × 3 = 75"), LB("a2", "LCM of 15 and 25 = 75")),
    B("15 and 20: the first one is 60, because 20 times 3 is 60. 15 and 12: also 60, because 12 times 5 is 60.",
      W("b", "20 × 3 = 60"), LB("b2", "LCM of 15 and 20 = 60"), W("c", "12 × 5 = 60"), LB("c2", "LCM of 15 and 12 = 60")),
    Q("Now 15 and 18. Which is the first number in the list that 18 divides?", ["90", "45", "60"], 0,
      "18 times 5 is 90. None of the earlier numbers in the list is in the 18 times table."),
    B("18 times 5 is 90. So the L C M of 15 and 18 is 90, the greatest of the four.",
      W("d", "18 × 5 = 90"), LB("d2", "LCM of 15 and 18 = 90"), ANS("ans", "15 & 18"), CIRC("ans", "15 & 18")),
    B("Here is the trap. 25 is the biggest partner, so it looks like the winner. But 25 shares the factor 5 with 15, and that keeps their L C M down to 75."),
)

LESSONS["PYQ_2017_Q01"] = LESSON(
    B("Three of these numbers can be made by adding two primes. One cannot. We test each one.",
      GIVEN("q", "Which is NOT prime + prime?  5, 7, 11, 12")),
    B("5 is 2 plus 3. 7 is 2 plus 5. Remember, 2 is a prime number. So both of those can be made.",
      W("a", "5 = 2 + 3"), W("b", "7 = 2 + 5"), STRIKE("q", "5"), STRIKE("q", "7")),
    B("12 is 5 plus 7, and both are prime. So 12 can be made too.", W("c", "12 = 5 + 7"), STRIKE("q", "12")),
    B("Now 11. It is odd. Two odd primes add up to an even number, so to make 11, one of the primes has to be 2, the only even prime."),
    Q("11 minus 2 is 9. Is 9 a prime number?", ["No, 3 × 3 = 9", "Yes, it is prime"], 0,
      "3 times 3 is 9. So 9 has a factor other than 1 and itself, and it is not prime.",
      W("d", "11 − 2 = 9")),
    B("9 is 3 times 3, so it is not prime. There is no other way to try. So 11 is not the sum of two primes.",
      W("e", "9 = 3 × 3"), ANS("ans", "11 is not prime + prime"), CIRC("ans", "11")),
    B("The trap: 11 is a prime number itself. But that does not mean it can be split into two primes."),
)

LESSONS["PYQ_2017_Q06"] = LESSON(
    B("Ajay rolls three dice. The three numbers multiply to make 90. What do they add up to? Remember, a die only shows 1 to 6.",
      GIVEN("q", "Three dice. Product = 90. Sum = ?")),
    B("Break 90 into its prime factors: 2 times 3 times 3 times 5.", W("a", "90 = 2 × 3 × 3 × 5")),
    Q("Look at the 5. Could it join with another prime on one die? 5 times 2 is 10, and 5 times 3 is 15.",
      ["No, 10 and 15 are too big", "Yes, 10 fits on a die"], 0,
      "A die only goes up to 6. 10 and 15 are both too big, so the 5 must sit on a die by itself.",
      W("b", "5 × 2 = 10"), W("c", "5 × 3 = 15")),
    B("So one die shows 5. The other two dice must multiply to make 90 divided by 5, which is 18.", W("d", "90 ÷ 5 = 18")),
    B("How can two dice make 18? 2 times 9 would need a 9, and a die has no 9. So it must be 3 times 6.",
      W("e", "2 × 9 = 18"), STRIKE("e", "9", "not on a die"), W("f", "3 × 6 = 18")),
    B("The dice show 3, 5 and 6. Check: 3 times 5 times 6 is 90.", W("g", "3 × 5 × 6 = 90")),
    B("Add them up. 3 plus 5 plus 6 is 14.", ANSM("ans", "3 + 5 + 6 = 14"), CIRC("ans", "14")),
    B("Only one set of dice fits, so we do have enough information. The key was that a die stops at 6."),
)

LESSONS["PYQ_2017_Q16"] = LESSON(
    B("What is the smallest number we can add to 267 times 348, so that 5 divides the total? Good news: we do not need the whole product.",
      GIVEN("q", "267 × 348 + ? is divisible by 5")),
    B("A number is divisible by 5 only when it ends in 0 or 5. So all that matters is the last digit of the product."),
    Q("The last digit of a product comes from the two ones digits. Here they are 7 and 8, and 7 times 8 is 56. So what digit does the product end in?",
      ["6", "5", "8"], 0,
      "7 times 8 is 56, and 56 ends in 6. So the whole product ends in 6.",
      W("a", "7 × 8 = 56")),
    B("The product ends in 6. Counting on from 6, the next ending that 5 likes is 0. And 6 needs 4 more to reach 10.",
      W("b", "6 + 4 = 10")),
    B("So the smallest number to add is 4.", ANS("ans", "Add 4"), CIRC("ans", "4")),
    B("Let's check with the full product. 267 times 348 is 92,916. Add 4, and we get 92,920. It ends in 0, so 5 divides it.",
      W("c", "267 × 348 = 92,916"), W("d", "92,916 + 4 = 92,920")),
    B("The trap is adding 5. That would make the number end in 1. For the 5 test, only the last digit matters."),
)

LESSONS["PYQ_2018_Q01"] = LESSON(
    B("Two ribbons, 84 metres and 108 metres long. Both are cut into pieces of the same length, with nothing left over. How long can each piece be?",
      GIVEN("q", "Ribbons: 84 m and 108 m. Equal pieces, none left."), LB("q2", "Greatest length of each piece = ?"),
      FIG("f", {"kind": "barModel", "bars": [
          {"label": "Ribbon 1", "segments": [{"units": 9.333, "label": "84 m", "tone": "a"}]},
          {"label": "Ribbon 2", "segments": [{"units": 12.0, "label": "108 m", "tone": "b"}]}],
          "note": "Equal pieces, as long as possible."})),
    Q("The piece length must divide 84 exactly, and 108 exactly. We want the greatest such length. What is that?",
      ["The HCF of 84 and 108", "The LCM of 84 and 108", "108 − 84"], 0,
      "A length that divides both ribbons exactly is a common factor. The greatest one is the highest common factor."),
    B("So we want the H C F. Here are the factors of 84. We will test them on 108, starting from the big end.",
      LB("la", "Factors of 84: 1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84")),
    B("84, 42, 28, 21 and 14 do not divide 108. It is not in any of their tables. Cross them out.",
      STRIKE("la", "84", None, 2), STRIKE("la", "42"), STRIKE("la", "28"), STRIKE("la", "21"), STRIKE("la", "14")),
    Q("Next is 12. Does 12 divide 108 exactly?", ["Yes, 12 × 9 = 108", "No, it does not"], 0,
      "12 times 9 is 108. So 12 divides 108 exactly."),
    B("12 times 9 is 108, and 12 times 7 is 84. So each piece can be 12 metres long: 7 pieces from one ribbon, and 9 from the other.",
      W("a", "12 × 9 = 108"), W("b", "12 × 7 = 84"), CIRC("la", "12"), ANS("ans", "12 metres"), CIRC("ans", "12 metres")),
    B("Watch the traps. 6 divides both ribbons, but it is not the greatest. And 14 divides only 84, so the longer ribbon would have some left over."),
)


def _or(nums):
    nums = [str(n) for n in nums]
    return nums[0] if len(nums) == 1 else ", ".join(nums[:-1]) + " or " + nums[-1]


def star9(first, third, known, tries, star, pair, number_text, quotient, trap):
    """A four-digit number with the same hidden digit twice, divisible by 9."""
    given = "%d★%d★ is divisible by 9.  ★ = ?" % (first, third)
    total = known + pair
    lines = [W("t%d" % i, "%d + %d = %d" % (known, add, known + add)) for i, add in enumerate(tries)]
    odd = [str(t) for t in tries if t != pair]
    return LESSON(
        B("A four-digit number: %d, star, %d, star. Both stars are the same digit, and 9 divides the number exactly. Which digit is the star?" % (first, third),
          GIVEN("q", given),
          TABLE("f", [[str(first), "★", str(third), "★"]], headers=["Thousands", "Hundreds", "Tens", "Ones"],
                note="Both stars are the same digit.")),
        B("The test for 9: add up all the digits. If the total is in the 9 times table, then 9 divides the number."),
        B("The digits we know are %d and %d. They add up to %d." % (first, third, known), W("a", "%d + %d = %d" % (first, third, known))),
        B("The two stars are the same digit. So together they add up to double that digit, and a double is always an even number."),
        Q("The total must land in the 9 times table: %s. For that, the stars must add %s. Which of those can two equal digits make?" % (
            _or([known + t for t in tries]), _or(tries)),
          [str(pair)] + odd, 0,
          "Two equal digits always add up to an even number. %s odd, so it must be %d." % (" and ".join(odd) + (" is" if len(odd) == 1 else " are"), pair),
          *lines),
        B("The two stars add up to %d, and half of %d is %d. So each star is %d." % (pair, pair, star, star),
          W("h", "%d ÷ 2 = %d" % (pair, star)), ANS("ans", "★ = %d" % star), CIRC("ans", "★ = %d" % star)),
        B("Let's check. The digits add up to %d, which is in the 9 times table. And the number is %s, which is 9 times %d." % (total, number_text, quotient),
          W("c", "%d + %d + %d + %d = %d" % (first, star, third, star, total)), W("d", "9 × %d = %s" % (quotient, number_text))),
        B(trap),
    )


LESSONS["PYQ_2018_Q16"] = star9(
    8, 2, 10, [8, 17], 4, 8, "8,424", 936,
    "One trap: 8 is what the two stars add up to together. It is not one star. Share it equally between the two.")
LESSONS["PYQ_2019_Q21"] = star9(
    9, 8, 17, [1, 10, 19], 5, 10, "9,585", 1065,
    "One trap: adding 1 just once would reach the 9 times table. But the star is there twice, so whatever we add is added twice.")

LESSONS["PYQ_2019_Q11"] = LESSON(
    B("Use every one-digit prime number, once each, to make the greatest odd number.",
      GIVEN("q", "Use all the one-digit primes. Greatest odd number = ?")),
    Q("First, which are the one-digit primes?", ["2, 3, 5, 7", "2, 3, 5, 7, 9", "1, 3, 5, 7"], 0,
      "9 is 3 times 3, so it is not prime. 1 is not prime either. And do not forget 2, the only even prime."),
    B("So our digits are 2, 3, 5 and 7.", LB("a", "Digits to use: 2, 3, 5, 7")),
    B("For the greatest number, we put the biggest digits first. That would give 7532. But look at the end: it finishes in 2, so it is even.",
      LB("b", "7532 is even")),
    Q("The number must be odd. Keep 7 and 5 at the front. Which digit must go last: 3 or 2?", ["3", "2"], 0,
      "An odd number must end in an odd digit. 2 is even, so the 3 goes last."),
    B("So 7, then 5, then 2, and 3 at the end. The greatest odd number is 7523.", ANS("ans", "7523"), CIRC("ans", "7523")),
    B("Two traps. 9 is not prime, so it cannot be used. And 7325 is odd too, but it is smaller, because 5 hundreds beats 3 hundreds.",
      W("t", "7523 > 7325")),
)

LESSONS["PYQ_2019_Q22"] = LESSON(
    B("In how many ways can 136 be written as one number times another? Each way is a pair of factors of 136.",
      GIVEN("q", "136 = ? × ?   How many ways?"),
      TABLE("f", [["1", "×", "136"], ["?", "×", "?"]], note="How many pairs multiply to 136?")),
    B("Start small. 1 times 136 is the first way. 136 is even, and half of it is 68. So 2 times 68 is the second way.",
      W("p1", "1 × 136 = 136"), W("p2", "2 × 68 = 136")),
    B("Try 3. The digits of 136 add up to 10, which is not in the 3 times table. So 3 does not divide it.",
      W("n", "1 + 3 + 6 = 10")),
    Q("Try 4. For 4, look at the last two digits: 36. Does 4 divide 36?", ["Yes, 4 × 9 = 36", "No, it does not"], 0,
      "4 times 9 is 36. So 4 divides 136 as well."),
    B("4 times 34 is 136. Then 5, 6 and 7 do not divide 136. But 8 does: 8 times 17 is 136.",
      W("p3", "4 × 34 = 136"), W("p4", "8 × 17 = 136")),
    B("After 8, the next factor is 17, and that is already on the board as a partner. Going on would only repeat the pairs backwards."),
    B("So there are 4 ways.", ANS("ans", "4 ways"), CIRC("ans", "4 ways")),
    B("Two traps. 17 times 8 is the same way as 8 times 17, so do not count it twice. And do not leave out 1 times 136."),
)

LESSONS["PYQ_2019_Q35"] = LESSON(
    B("Ajay writes the multiples of 4 up to 100. Vijay writes the multiples of 5 up to 100. How many numbers are in both notebooks?",
      GIVEN("q", "Multiples of 4 and of 5, up to 100. In both = ?")),
    B("A number in both notebooks is a multiple of 4 and of 5. Count up in 5s: 5, 10, 15, 20. The first one that 4 divides is 20.",
      LB("m", "Multiples of 5: 5, 10, 15, 20"), W("a", "4 × 5 = 20")),
    Q("So the numbers in both notebooks go up in steps of what?", ["20", "10", "9"], 0,
      "Every number in both tables is a multiple of 20, the lowest common multiple. So they go up in steps of 20."),
    B("Count up in 20s, up to 100: 20, 40, 60, 80, 100.", LB("l", "20, 40, 60, 80, 100")),
    B("That is 5 numbers. Or work it out: 100 divided by 20 is 5.",
      W("b", "100 ÷ 20 = 5"), ANS("ans", "5 numbers"), CIRC("ans", "5 numbers")),
    B("Two traps. 10 is in Vijay's notebook but not in Ajay's, so do not count in tens. And 20 is the smallest common number, not how many there are."),
    B("So for numbers in two tables at once: find the L C M, and count its multiples."),
)

LESSONS["Q_CH01_026"] = LESSON(
    B("What is the 8th multiple of 9? The multiples of 9 are the numbers in the 9 times table.",
      GIVEN("q", "8th multiple of 9 = ?")),
    B("The 1st multiple is 9 times 1. The 2nd is 9 times 2. The 3rd is 9 times 3. See the pattern?",
      LB("m", "9 × 1,  9 × 2,  9 × 3,  ...")),
    Q("So which sum gives the 8th multiple of 9?", ["9 × 8", "9 + 8", "9 × 9"], 0,
      "The 1st multiple is 9 times 1, and the 2nd is 9 times 2. So the 8th multiple is 9 times 8."),
    B("9 times 8 is 72. So the 8th multiple of 9 is 72.", ANSM("ans", "9 × 8 = 72"), CIRC("ans", "72")),
    B("Check by counting up in 9s, eight times: 9, 18, 27, 36, 45, 54, 63, 72.",
      LB("c", "9, 18, 27, 36, 45, 54, 63, 72"), CIRC("c", "72")),
    B("Watch the neighbours. 81 is 9 times 9, the 9th multiple. And 63 is 9 times 7, the 7th multiple.",
      W("t", "9 × 9 = 81"), W("t2", "9 × 7 = 63")),
    B("So the multiple number tells you what to multiply by. Easy!"),
)
