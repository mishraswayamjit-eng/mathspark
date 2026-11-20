"""Hand-written lessons, part 3: the newly written questions G4A_FACTORS_002 to 024."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANS, ANSM, B, CIRC, FIG, GIVEN, LB, LESSON, NOTE, Q, STRIKE, TABLE, TREE, VENN, W,
)

LESSONS = {}

LESSONS["G4A_FACTORS_002"] = LESSON(
    B("Three of these numbers are in the 7 times table, and one is not. We are hunting for the odd one out.",
      GIVEN("q", "Which is NOT a multiple of 7?  42, 63, 54, 91")),
    B("Start with the easy ones. 7 times 6 is 42, and 7 times 9 is 63. Both are multiples of 7.",
      NOTE("q", "42", "7 × 6"), NOTE("q", "63", "7 × 9")),
    Q("Now 91. It is past the tables we know by heart, so split it. 7 times 10 is 70, and that leaves 21. Is 21 in the 7 times table?",
      ["Yes, 7 × 3 = 21", "No, it is not"], 0,
      "7 times 3 is 21. So 91 is 70 plus 21, and both parts are in the 7 times table.",
      W("a0", "7 × 10 = 70"), W("a", "91 = 70 + 21")),
    B("10 sevens and 3 more sevens make 13 sevens. So 91 is 7 times 13. It is a multiple of 7 as well.",
      W("b", "91 = 7 × 13"), NOTE("q", "91", "7 × 13")),
    B("That leaves 54. 7 times 7 is 49, and 7 times 8 is 56. The 7 times table jumps right over 54.",
      W("c", "7 × 7 = 49"), W("d", "7 × 8 = 56"), CIRC("q", "54")),
    B("So 54 is the one that is not a multiple of 7.", ANS("ans", "54 is not a multiple of 7"), CIRC("ans", "54")),
    B("The trap is 91. It looks as if it cannot be in the 7 times table, but it is. Split a big number into parts you know."),
)

LESSONS["G4A_FACTORS_003"] = LESSON(
    B("Which of these is a composite number? A composite number has a factor other than 1 and itself. A prime number does not.",
      GIVEN("q", "Which is composite?  39, 23, 29, 37")),
    B("To test, try the small primes: 2, 3 and 5. None of these numbers is even, and none ends in 0 or 5. So 2 and 5 are no help."),
    B("That leaves the test for 3: add the digits. 2 plus 3 is 5. 2 plus 9 is 11. 3 plus 7 is 10. None of those is in the 3 times table.",
      W("a", "2 + 3 = 5"), W("b", "2 + 9 = 11"), W("c", "3 + 7 = 10")),
    Q("Now 39. 3 plus 9 is 12. Is 12 in the 3 times table?", ["Yes, 3 × 4 = 12", "No, it is not"], 0,
      "3 times 4 is 12. So 12 is in the 3 times table, and that means 3 divides 39.",
      W("d", "3 + 9 = 12")),
    B("So 3 divides 39. In fact 3 times 13 is 39. It has factors other than 1 and itself, so 39 is composite.",
      W("e", "39 = 3 × 13"), ANS("ans", "39 is composite"), CIRC("ans", "39")),
    B("23, 29 and 37 are all prime. Nothing divides them except 1 and themselves.",
      STRIKE("q", "23", "prime"), STRIKE("q", "29", "prime"), STRIKE("q", "37", "prime")),
    B("Odd numbers often look prime when they are not. Add the digits to test for 3 before you decide."),
)

LESSONS["G4A_FACTORS_004"] = LESSON(
    B("We need every factor of 18: every number that divides 18 exactly. Miss none, and add no extras.",
      GIVEN("q", "All the factors of 18 = ?"),
      TABLE("f", [["1", "×", "18"], ["?", "×", "?"]], note="Find every pair that multiplies to 18.")),
    B("Factors come in pairs that multiply to make 18. The first pair is always 1 and the number itself: 1 times 18.",
      W("p1", "1 × 18 = 18")),
    Q("Next try 2. 18 is even, so 2 is a factor. What is its partner?", ["9", "8", "16"], 0,
      "The partner is the number we multiply 2 by to make 18. 2 times 9 is 18."),
    B("2 times 9 is 18. And 3 works too: 3 times 6 is 18.", W("p2", "2 × 9 = 18"), W("p3", "3 × 6 = 18")),
    B("Now 4. 4 times 4 is 16 and 4 times 5 is 20, so 4 skips 18. And 5 does not divide a number ending in 8. Next is 6, which we already have, so we stop.",
      W("n1", "4 × 4 = 16"), W("n2", "4 × 5 = 20")),
    B("Collect the numbers from the pairs, in order: 1, 2, 3, 6, 9, 18. That is every factor of 18.",
      ANS("ans", "1, 2, 3, 6, 9, 18"), CIRC("ans", "1, 2, 3, 6, 9, 18")),
    B("Two things to remember. 1 and the number itself are always factors, so never leave them out. And do not let 4 sneak in."),
)

LESSONS["G4A_FACTORS_005"] = LESSON(
    B("Laddoos are packed 8 in a box, with none left over. Which of these could be the total number of laddoos?",
      GIVEN("q", "8 in a box, none left over: 44, 54, 56 or 62?")),
    B("None left over means the total is made of full boxes of 8. So the total must be in the 8 times table."),
    B("Let's write the part of the 8 times table near our numbers. 8 times 5 is 40, then 48, then 56, then 64.",
      LB("t", "8 times table: 40, 48, 56, 64")),
    Q("Which of our choices is in that list?", ["56", "54", "62"], 0,
      "Look along the list: 40, 48, 56, 64. Only 56 is one of our choices."),
    B("8 times 7 is 56. So 56 laddoos fill exactly 7 boxes, with none left over.",
      W("a", "8 × 7 = 56"), ANS("ans", "56 laddoos"), CIRC("ans", "56 laddoos")),
    B("Look at the others. 44 is 40 and 4 more, so 4 laddoos are left over. 54 is 48 and 6 more. 62 is 56 and 6 more.",
      W("b", "44 = 40 + 4"), W("c", "54 = 48 + 6"), W("d", "62 = 56 + 6")),
    B("So whenever a question says none left over, think: it must be in the times table."),
)

LESSONS["G4A_FACTORS_006"] = LESSON(
    B("Which of these is a common factor of 12 and 20? Common means shared. So it must divide 12 exactly, and 20 exactly.",
      GIVEN("q", "Common factor of 12 and 20?  3, 5, 6 or 4")),
    B("List the factors of 12 in pairs: 1 times 12, 2 times 6, 3 times 4.", LB("la", "Factors of 12: 1, 2, 3, 4, 6, 12")),
    B("Now 20: 1 times 20, 2 times 10, 4 times 5.", LB("lb", "Factors of 20: 1, 2, 4, 5, 10, 20")),
    Q("Which of our choices is in both lists?", ["4", "3", "5", "6"], 0,
      "3 and 6 are only in the first list. 5 is only in the second list. But 4 is in both."),
    B("4 is in both lists, so 4 is a common factor of 12 and 20. In the picture it sits in the middle.",
      CIRC("la", "4"), CIRC("lb", "4"),
      VENN("v", "Factors of 12", "Factors of 20", "3, 6, 12", "1, 2, 4", "5, 10, 20", highlight=["both"],
           note="The middle holds the common factors."),
      ANS("ans", "4 is a common factor"), CIRC("ans", "4")),
    B("Let's check. 12 divided by 4 is 3, and 20 divided by 4 is 5. Both are exact.",
      W("c", "12 ÷ 4 = 3"), W("d", "20 ÷ 4 = 5")),
    B("Remember: a common factor must fit both numbers. 3 and 6 fit only 12, and 5 fits only 20."),
)

LESSONS["G4A_FACTORS_007"] = LESSON(
    B("Three lights blink every 4 seconds, every 6 seconds and every 9 seconds. They all blink together now. When do they next blink together?",
      GIVEN("q", "Lights blink every 4, 6 and 9 seconds. Together next = ?")),
    B("Each light blinks at the multiples of its own number. All three together means a common multiple. And the next time means the lowest one."),
    B("Count up in the biggest number, 9, and test each one: 9, 18, 27, 36.", LB("m", "Multiples of 9: 9, 18, 27, 36")),
    B("9 and 27 are odd, so 4 and 6 cannot divide them. 18 is in the 6 times table, but 4 skips it: 4 times 4 is 16, and 4 times 5 is 20.",
      W("a", "4 × 4 = 16"), W("b", "4 × 5 = 20"), STRIKE("m", "9", None, 2), STRIKE("m", "18"), STRIKE("m", "27")),
    Q("Now 36. Do 4 and 6 both divide 36 exactly?", ["Yes, both do", "Only 6 does", "Only 4 does"], 0,
      "4 times 9 is 36, and 6 times 6 is 36. So both of them divide 36 exactly."),
    B("4 times 9 is 36, and 6 times 6 is 36. So all three lights blink together after 36 seconds.",
      W("c", "4 × 9 = 36"), W("d", "6 × 6 = 36"), ANS("ans", "36 seconds"), CIRC("ans", "36 seconds")),
    B("Two traps. At 18 seconds, the light that blinks every 4 seconds is dark. And multiplying all three gives 216, a common multiple, but not the first one.",
      W("e", "4 × 6 × 9 = 216")),
    B("So for things that repeat and meet again: find the lowest common multiple."),
)

LESSONS["G4A_FACTORS_008"] = LESSON(
    B("A wall panel is 48 centimetres long and 60 centimetres wide. Equal square tiles must cover it exactly, with no cutting. How big can a tile be?",
      GIVEN("q", "Panel 48 cm by 60 cm. Largest square tile = ?"),
      FIG("f", {"kind": "rectangle", "length": "60 cm", "breadth": "48 cm", "proportion": 1.25,
                "note": "Equal square tiles, no cutting."})),
    Q("The tiles must fit exactly along the 48 side and along the 60 side. So what are we looking for?",
      ["The HCF of 48 and 60", "The LCM of 48 and 60", "48 + 60"], 0,
      "The side of the tile must divide 48 exactly, and 60 exactly. We want the biggest such number: the highest common factor."),
    B("So we want the H C F of 48 and 60. Here are the factors of 48. We want the biggest one that also divides 60, so test from the big end.",
      LB("la", "Factors of 48: 1, 2, 3, 4, 6, 8, 12, 16, 24, 48")),
    B("48 does not divide 60. 24 does not: 24 times 2 is 48 and 24 times 3 is 72, so it skips 60. 16 does not: 16 times 4 is 64.",
      W("a", "24 × 3 = 72"), W("b", "16 × 4 = 64"), STRIKE("la", "48", None, 2), STRIKE("la", "24"), STRIKE("la", "16")),
    Q("Next is 12. Does 12 divide 60 exactly?", ["Yes, 12 × 5 = 60", "No, it does not"], 0,
      "12 times 5 is 60. So 12 divides 60 exactly."),
    B("12 times 4 is 48, and 12 times 5 is 60. So the largest tile has a side of 12 centimetres: 4 tiles one way, and 5 tiles the other.",
      W("c", "12 × 4 = 48"), W("d", "12 × 5 = 60"), CIRC("la", "12"), ANS("ans", "12 cm"), CIRC("ans", "12 cm")),
    B("One trap: tiles of 6 centimetres would fit too, but they are not the largest. Always look for the highest common factor."),
)

LESSONS["G4A_FACTORS_009"] = LESSON(
    B("Two prime numbers add up to 30. One of these four numbers can never be one of the two. Which one?",
      GIVEN("q", "prime + prime = 30. Which cannot be used?"), LB("o", "7, 11, 13 or 5")),
    B("Here is the plan. For each choice, find its partner by taking it away from 30. The partner must be a prime number too."),
    B("30 minus 7 is 23, and 23 is prime. 30 minus 11 is 19, and 19 is prime. So 7 and 11 can both be used.",
      W("a", "30 − 7 = 23"), W("b", "30 − 11 = 19")),
    B("30 minus 13 is 17, and 17 is prime. So 13 can be used as well.", W("c", "30 − 13 = 17")),
    Q("Now 5. 30 minus 5 is 25. Is 25 a prime number?", ["No, 5 × 5 = 25", "Yes, it is prime"], 0,
      "5 times 5 is 25. So 25 has a factor other than 1 and itself, and it is not prime.",
      W("d", "30 − 5 = 25")),
    B("25 is 5 times 5, so it is not prime. The partner fails, so 5 cannot be one of the two primes.",
      W("e", "25 = 5 × 5"), ANS("ans", "5 cannot be used"), CIRC("ans", "5")),
    B("Notice the trap. 5 is a prime number itself. But both numbers in the pair must be prime, and its partner is not."),
)

LESSONS["G4A_FACTORS_010"] = LESSON(
    B("A three-digit number has 7 hundreds and 4 ones. The tens digit is missing. We want the smallest tens digit that lets 3 divide the number.",
      GIVEN("q", "7 _ 4 is divisible by 3. Smallest tens digit = ?"),
      TABLE("f", [["7", "?", "4"]], headers=["Hundreds", "Tens", "Ones"], note="Which is the smallest digit that works?")),
    B("The test for 3: add up the digits. If the total is in the 3 times table, then 3 divides the number."),
    B("The digits we know are 7 and 4. They add up to 11.", W("a", "7 + 4 = 11")),
    Q("11 is not in the 3 times table. What is the next number after 11 that is?", ["12", "13", "14"], 0,
      "Count up in 3s: 3, 6, 9, 12. So 12 is the next one after 11."),
    B("12 is next, and 11 needs just 1 more to get there. So the tens digit is 1, and the number is 714.",
      W("b", "11 + 1 = 12"), LB("n", "714"), ANS("ans", "Smallest digit = 1"), CIRC("ans", "1")),
    B("Could 0 work? It is smaller. But 7 plus 0 plus 4 is still 11, which is not in the 3 times table. So 1 really is the smallest.",
      W("c", "7 + 0 + 4 = 11")),
    B("One trap: 4 works as well, because 7 plus 4 plus 4 is 15. But the question asks for the smallest digit.",
      W("d", "7 + 4 + 4 = 15")),
)

LESSONS["G4A_FACTORS_011"] = LESSON(
    B("Which of these four numbers can be divided exactly by 6? We will use two quick tests instead of dividing.",
      GIVEN("q", "Divisible by 6?  2,134  3,471  4,572  5,224")),
    B("6 is 2 times 3. So the number must be even, for 2. And its digits must add up to a number in the 3 times table, for 3.",
      W("a", "6 = 2 × 3")),
    B("3,471 ends in 1, so it is odd. It is out straight away.", STRIKE("q", "3,471", "odd")),
    B("Now add digits. 2,134 gives 10. 5,224 gives 13. Neither 10 nor 13 is in the 3 times table.",
      W("b", "2 + 1 + 3 + 4 = 10"), W("c", "5 + 2 + 2 + 4 = 13"), STRIKE("q", "2,134"), STRIKE("q", "5,224")),
    Q("That leaves 4,572. What do its digits add up to?", ["18", "17", "19"], 0,
      "Add them one at a time: 4, then 5, then 7, then 2. You reach 18."),
    B("The digits add up to 18, and 18 is 3 times 6. And 4,572 ends in 2, so it is even. Both tests are passed!",
      W("d", "4 + 5 + 7 + 2 = 18"), W("e", "18 = 3 × 6"), ANS("ans", "4,572 is divisible by 6"), CIRC("ans", "4,572")),
    B("Here is the trap. The digits of 3,471 add up to 15, so 3 divides it. But it is odd, so 6 cannot. A number needs both tests.",
      W("f", "3 + 4 + 7 + 1 = 15")),
)

LESSONS["G4A_FACTORS_012"] = LESSON(
    B("Which of these numbers has exactly 3 factors? Let's list the factors of each one and count.",
      GIVEN("q", "Exactly 3 factors?  15, 21, 25, 27")),
    B("15 is 1 times 15, and 3 times 5. 21 is 1 times 21, and 3 times 7. That is four factors each.",
      LB("a", "15: 1, 3, 5, 15"), LB("b", "21: 1, 3, 7, 21")),
    B("27 is 1 times 27, and 3 times 9. Four factors again.", LB("d", "27: 1, 3, 9, 27")),
    Q("Now 25. Its pairs are 1 times 25, and 5 times 5. How many different factors is that?", ["3", "4", "2"], 0,
      "1 times 25 gives two factors, 1 and 25. But 5 times 5 gives only one factor, because it is the same number twice.",
      W("c0", "5 × 5 = 25")),
    B("So 25 has just three factors: 1, 5 and 25.",
      LB("c", "25: 1, 5, 25"), ANS("ans", "25 has exactly 3 factors"), CIRC("ans", "25")),
    B("Why is 25 special? It is a square number. One of its pairs uses the same number twice, so that pair gives one factor, not two."),
    B("So remember: most numbers have an even number of factors, because factors come in pairs. Square numbers are the odd ones out."),
)

LESSONS["G4A_FACTORS_013"] = LESSON(
    B("How many of the factors of 48 are even numbers? First we find all the factors. Then we sort them.",
      GIVEN("q", "How many factors of 48 are even?"),
      TABLE("f", [["1", "×", "48"], ["?", "×", "?"]], note="Find every pair that multiplies to 48.")),
    B("Factors come in pairs. 1 times 48, 2 times 24, 3 times 16, 4 times 12, and 6 times 8. 5 does not divide 48, so we skip it.",
      W("p1", "1 × 48 = 48"), W("p2", "2 × 24 = 48"), W("p3", "3 × 16 = 48"), W("p4", "4 × 12 = 48"), W("p5", "6 × 8 = 48")),
    B("5 pairs give 10 factors. Here they are in order.", LB("l", "1, 2, 3, 4, 6, 8, 12, 16, 24, 48")),
    Q("It is quicker to spot the odd ones. Which of the factors are odd?", ["1 and 3", "1, 3 and 6", "only 1"], 0,
      "Odd numbers end in 1, 3, 5, 7 or 9. In our list, only 1 and 3 are odd."),
    B("Only 1 and 3 are odd. Cross them out. 10 take away 2 leaves 8. So 8 of the factors are even.",
      STRIKE("l", "1"), STRIKE("l", "3"), W("s", "10 − 2 = 8"), ANS("ans", "8 even factors"), CIRC("ans", "8 even factors")),
    B("Watch the traps. 10 is the number of all the factors. 5 is the number of pairs. And 2 is the number of odd factors."),
    B("So read what is being counted. Here it is only the even factors."),
)

LESSONS["G4A_FACTORS_014"] = LESSON(
    B("A flower seller can make garlands of 10 flowers, or garlands of 15 flowers, with none left over either way. What is the smallest number of flowers she could have?",
      GIVEN("q", "Garlands of 10 or of 15, none left over. Smallest = ?")),
    B("None left over in 10s means the number is in the 10 times table. None left over in 15s means it is in the 15 times table. We want the first number in both: the L C M."),
    B("Count up in the bigger number, 15: 15, 30, 45.", LB("m", "Multiples of 15: 15, 30, 45")),
    Q("Which is the first of these that is also in the 10 times table?", ["30", "15", "45"], 0,
      "Numbers in the 10 times table end in 0. In our list, 30 is the first one that does."),
    B("30 is 10 times 3, and 15 times 2. So she could have 30 marigolds: 3 garlands of 10, or 2 garlands of 15.",
      W("a", "10 × 3 = 30"), W("b", "15 × 2 = 30"), ANS("ans", "30 marigolds"), CIRC("ans", "30 marigolds")),
    B("One trap: 10 times 15 is 150. That number works too, but it is not the smallest.", W("c", "10 × 15 = 150")),
    B("And 5 is not the answer either. 5 divides 10 and 15, but she needs a number that 10 and 15 both go into."),
)

LESSONS["G4A_FACTORS_015"] = LESSON(
    B("What is the greatest prime factor of 84? We split 84 into smaller and smaller pieces, until every piece is prime.",
      GIVEN("q", "Greatest prime factor of 84 = ?"), TREE("f", 84)),
    B("84 is even, so start with 2. 84 is 2 times 42.", W("a", "84 = 2 × 42")),
    B("42 is even too: it is 2 times 21. And 21 is 3 times 7.", W("b", "84 = 2 × 2 × 21"), W("c", "84 = 2 × 2 × 3 × 7")),
    Q("Look at the pieces now: 2, 2, 3 and 7. Can any of them be split further?", ["No, they are all prime", "Yes, 7 can be split"], 0,
      "2, 3 and 7 each have only two factors: 1 and themselves. So none of them can be split any more."),
    B("So the prime factors of 84 are 2, 3 and 7. The greatest of them is 7.",
      CIRC("c", "7"), ANS("ans", "Greatest prime factor = 7"), CIRC("ans", "7")),
    B("Here is the trap. 21 and 42 are bigger factors of 84, but they are not prime. 21 is 3 times 7, and 42 is 2 times 21.",
      W("d", "21 = 3 × 7"), W("e", "42 = 2 × 21")),
    B("So keep splitting until nothing can be split. Only then pick the greatest piece."),
)

LESSONS["G4A_FACTORS_016"] = LESSON(
    B("We must take a number away from 4,729 so that 9 divides what is left. And we want the smallest such number.",
      GIVEN("q", "4,729 − ? is divisible by 9")),
    B("Use the test for 9: add the digits. 4 plus 7 plus 2 plus 9 is 22.", W("a", "4 + 7 + 2 + 9 = 22")),
    Q("22 is not in the 9 times table. Which number in the 9 times table is just below 22?", ["18", "20", "27"], 0,
      "Count up in 9s: 9, then 18, then 27. The one just below 22 is 18."),
    B("22 is 4 more than 18. That tells us 4,729 is 4 more than a multiple of 9. So we take away 4.",
      W("b", "22 − 18 = 4")),
    B("4,729 take away 4 is 4,725. Check its digits: 4 plus 7 plus 2 plus 5 is 18. Yes, 9 divides it.",
      W("c", "4,729 − 4 = 4,725"), W("d", "4 + 7 + 2 + 5 = 18"), ANS("ans", "Subtract 4"), CIRC("ans", "4")),
    B("One trap: adding 5 also reaches the 9 times table, because 22 plus 5 is 27. But the question says subtract, so the answer is 4.",
      W("e", "22 + 5 = 27")),
    B("So the digit sum tells you how far a number is past a multiple of 9. Take that much away."),
)

LESSONS["G4A_FACTORS_017"] = LESSON(
    B("A staircase has 50 steps. Anu steps on every 3rd step, and Biju on every 4th step. How many steps does nobody touch?",
      GIVEN("q", "50 steps. Anu: every 3rd. Biju: every 4th. Neither = ?")),
    B("Anu touches the multiples of 3. 3 times 16 is 48, and 3 times 17 is 51, which is past 50. So Anu touches 16 steps.",
      W("a", "3 × 16 = 48"), W("a2", "3 × 17 = 51")),
    B("Biju touches the multiples of 4. 4 times 12 is 48, and 4 times 13 is 52, which is too far. So Biju touches 12 steps.",
      W("b", "4 × 12 = 48"), W("b2", "4 × 13 = 52")),
    Q("Careful now! Some steps are touched by both children. Which steps are those?",
      ["Multiples of 12", "Multiples of 7", "Multiples of 3 only"], 0,
      "A step touched by both is in the 3 times table and in the 4 times table. The first such number is 12, so they are the multiples of 12."),
    B("The multiples of 12 up to 50 are 12, 24, 36 and 48. So 4 steps are touched by both.", LB("c", "Both: 12, 24, 36, 48")),
    B("If we just add 16 and 12, those 4 steps get counted twice. So take 4 away once. 16 plus 12 minus 4 is 24 steps touched.",
      W("t", "16 + 12 − 4 = 24"),
      VENN("v", "Anu: every 3rd", "Biju: every 4th", "12", "4", "8", highlight=["both"],
           note="4 steps are touched by both.")),
    B("50 steps in all, and 24 are touched. 50 minus 24 is 26. So 26 steps are touched by nobody.",
      ANSM("ans", "50 − 24 = 26"), CIRC("ans", "26")),
    B("The trap is the steps both children touch. Count them once, not twice. And 24 is the touched steps, not the answer."),
)

LESSONS["G4A_FACTORS_018"] = LESSON(
    B("Pune buses leave every 15 minutes, and Nashik buses every 20 minutes. Both leave at 6 o'clock. Up to 10 o'clock, how many times do they leave together?",
      GIVEN("q", "Pune: every 15 min. Nashik: every 20 min."), LB("q2", "From 6:00 to 10:00, together how many times?")),
    B("They leave together at the common multiples of 15 and 20. So first find the lowest one. Count up in 20s: 20, 40, 60.",
      LB("m", "Multiples of 20: 20, 40, 60")),
    Q("Which is the first of these that 15 divides exactly?", ["60", "40", "30"], 0,
      "15 does not go into 20 or 40 exactly. But 15 times 4 is 60."),
    B("15 times 4 is 60. And 60 minutes is one hour. So the two buses leave together once every hour.",
      W("a", "15 × 4 = 60"), LB("h", "Together every 60 minutes")),
    B("Now list the times, one hour apart: 6 o'clock, 7 o'clock, 8 o'clock, 9 o'clock and 10 o'clock.",
      LB("t", "6:00, 7:00, 8:00, 9:00, 10:00")),
    Q("How many times is that?", ["5", "4", "8"], 0,
      "Count the times on the board, and do not skip the first one. 6 o'clock counts too. That makes 5."),
    B("They leave together 5 times.", ANS("ans", "5 times"), CIRC("ans", "5 times")),
    B("Here is the trap. From 6 o'clock to 10 o'clock is 4 hours, but there are 5 leaving times, because both ends count."),
)

LESSONS["G4A_FACTORS_019"] = LESSON(
    B("Rohan puts his marbles in groups of 4, or 5, or 6. Every time, 3 marbles are left over. What is the smallest number he could have?",
      GIVEN("q", "Groups of 4, 5 or 6: always 3 left over. Smallest = ?")),
    B("Here is the trick. Put the 3 extra marbles to one side. What is left makes exact groups of 4, of 5 and of 6. So it is a common multiple of all three."),
    B("Start with 5 and 6. 5 times 6 is 30, and that is the first number both of them divide. The next is 60.",
      W("a0", "5 × 6 = 30"), LB("m", "Multiples of 30: 30, 60")),
    Q("Which is the first of these that 4 divides as well?", ["60", "30", "120"], 0,
      "4 does not go into 30 exactly. But 4 does go into 60, with nothing left over."),
    B("60 divided by 4 is 15, by 5 is 12, and by 6 is 10. All exact. So 60 is the lowest common multiple.",
      W("a", "60 ÷ 4 = 15"), W("b", "60 ÷ 5 = 12"), W("c", "60 ÷ 6 = 10"), LB("l", "LCM of 4, 5 and 6 = 60")),
    B("Now bring back the 3 extra marbles. 60 plus 3 is 63. So Rohan has 63 marbles.",
      ANSM("ans", "60 + 3 = 63"), CIRC("ans", "63")),
    B("Two traps. 60 on its own leaves nothing over. And 57 comes from taking the 3 away. The extras are added, not taken off.",
      W("t", "60 − 3 = 57")),
    B("So when the same amount is always left over: find the L C M, then add the leftover."),
)

LESSONS["G4A_FACTORS_020"] = LESSON(
    B("A riddle with clues. I have two digits. I am a multiple of 7. I am odd. My two digits add up to 10. Which number am I?",
      GIVEN("q", "2-digit, multiple of 7, odd, digits add to 10"), LB("o", "91, 28, 73 or 49?")),
    B("Take one clue at a time. First, the digits add up to 10. 9 plus 1 is 10. 2 plus 8 is 10. 7 plus 3 is 10. But 4 plus 9 is 13, so 49 is out.",
      W("a", "9 + 1 = 10"), W("b", "2 + 8 = 10"), W("c", "7 + 3 = 10"), W("d", "4 + 9 = 13"), STRIKE("o", "49")),
    Q("Next clue: I am odd. Which number does that knock out?", ["28", "91", "73"], 0,
      "28 ends in 8, so it is even. The number must be odd, so 28 is out."),
    B("28 is even, so it is out. Two numbers are left: 91 and 73.", STRIKE("o", "28")),
    B("Last clue: a multiple of 7. 7 times 10 is 70 and 7 times 11 is 77, so 73 is skipped. But 7 times 13 is 91.",
      W("e", "7 × 10 = 70"), W("f", "7 × 11 = 77"), W("g", "7 × 13 = 91"), STRIKE("o", "73")),
    B("Only 91 fits every clue. The number is 91.", ANS("ans", "91"), CIRC("ans", "91")),
    B("With a riddle like this, use the clues one by one, and cross out as you go."),
)

LESSONS["G4A_FACTORS_021"] = LESSON(
    B("Which is the smallest number with exactly 6 factors? We want the smallest, so we test the choices from the smallest up.",
      GIVEN("q", "Smallest number with exactly 6 factors: 12, 18, 6 or 16?")),
    B("Start with 6 itself. Its pairs are 1 times 6, and 2 times 3. That is only four factors. Do not mix up the number 6 with six factors!",
      LB("a", "6: 1, 2, 3, 6")),
    Q("Next is 12. Its pairs are 1 times 12, 2 times 6, and 3 times 4. How many factors is that?", ["6", "3", "5"], 0,
      "There are 3 pairs, and each pair has 2 different numbers. 3 times 2 is 6."),
    B("12 has six factors: 1, 2, 3, 4, 6 and 12.", LB("b", "12: 1, 2, 3, 4, 6, 12")),
    B("Could a number smaller than 12 have six? No. The numbers below 12 have four factors at most. Look at 8 and 10.",
      LB("c", "8: 1, 2, 4, 8"), LB("d", "10: 1, 2, 5, 10")),
    B("So the smallest number with exactly 6 factors is 12.", ANS("ans", "12"), CIRC("ans", "12")),
    B("The trap is 18. It has six factors too, but 12 is smaller. And 16 has only five.",
      LB("e", "18: 1, 2, 3, 6, 9, 18"), LB("f", "16: 1, 2, 4, 8, 16")),
)

LESSONS["G4A_FACTORS_022"] = LESSON(
    B("How many numbers from 1 to 50 have exactly 3 factors? Testing all 50 would take far too long. We need a clever idea.",
      GIVEN("q", "From 1 to 50: how many have exactly 3 factors?")),
    B("Factors come in pairs, so most numbers have an even number of them. An odd number of factors only happens when a pair is the same number twice. That means a square number."),
    B("So only square numbers can have 3 factors. Here are the squares up to 50.",
      LB("s", "Squares: 1, 4, 9, 16, 25, 36, 49")),
    B("Count the factors of each. 4 has three: 1, 2 and 4. 9 has three. 25 has three. And 49 has three.",
      LB("f1", "4: 1, 2, 4"), LB("f2", "9: 1, 3, 9"), LB("f3", "25: 1, 5, 25"), LB("f4", "49: 1, 7, 49")),
    Q("What about 16? Its factors are 1, 2, 4, 8 and 16. How many is that?", ["5", "3", "4"], 0,
      "Count them on the board: 1, 2, 4, 8, 16. That is 5 factors, which is too many.",
      LB("x", "16: 1, 2, 4, 8, 16")),
    B("16 has five factors, so it is out. 36 has even more. And 1 has only one factor, itself. Cross those three out.",
      STRIKE("s", "1"), STRIKE("s", "16"), STRIKE("s", "36")),
    B("That leaves 4, 9, 25 and 49. So 4 numbers have exactly 3 factors.",
      ANS("ans", "4 numbers"), CIRC("ans", "4 numbers")),
    B("Did you spot the pattern? They are the squares of the primes 2, 3, 5 and 7. A number with exactly 3 factors is always the square of a prime."),
)

LESSONS["G4A_FACTORS_024"] = LESSON(
    B("Pune buses leave every 12 minutes, starting at 7 o'clock. Nashik buses leave every 18 minutes, starting at 6 minutes past 7. When do two buses first leave together?",
      GIVEN("q", "Pune: 7:00, then every 12 min"), LB("q2", "Nashik: 7:06, then every 18 min. Together first = ?")),
    B("Watch out. It is tempting to find the L C M of 12 and 18. But the two buses do not start at the same time. So the safe way is to list the times."),
    B("Pune buses: 7 o'clock, then 12 minutes past, 24 minutes past, and 36 minutes past.",
      LB("p", "Pune: 7:00, 7:12, 7:24, 7:36")),
    Q("The first Nashik bus leaves at 6 minutes past 7. Add 18 minutes. When does the next one leave?", ["7:24", "7:18", "7:26"], 0,
      "6 plus 18 is 24. So the next Nashik bus leaves at 24 minutes past 7."),
    B("6 plus 18 is 24, and 24 plus 18 is 42. So the Nashik buses leave at 6, 24 and 42 minutes past 7.",
      W("a", "6 + 18 = 24"), W("b", "24 + 18 = 42"), LB("n", "Nashik: 7:06, 7:24, 7:42")),
    B("Now look for the first time on both lists. There it is: 24 minutes past 7.",
      CIRC("p", "7:24"), CIRC("n", "7:24"), ANS("ans", "7:24"), CIRC("ans", "7:24")),
    B("The L C M of 12 and 18 is 36. That would point to 36 minutes past 7. But no Nashik bus leaves then. It only works when both start together."),
    B("So when the starting times are different, list the times and look for the first match."),
)
