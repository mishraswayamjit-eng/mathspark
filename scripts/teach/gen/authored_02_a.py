"""authored-02, first group: three decimal warm-ups and divisibility 001 to 005."""
from authored_02_lib import ANSC, ANSLC, B, CHOOSE, CIRC, GIVEN, LB, LESSON, STRIKE, UL, W

LESSONS = {}

# 3.25 × 100 (warm-up).
LESSONS["G5A_DECIMALS_014"] = LESSON(
    B("What is 3.25 multiplied by 100?",
      W("q", "3.25 × 100 = ?", "given")),
    B("Multiplying by 100 makes every digit worth 100 times as much. So the decimal point ends up further to the right.",
      UL("q", "100")),
    B("Start with the 3 ones. 3 times 100 is 300, so the 3 becomes 3 hundreds.",
      W("l1", "3 × 100 = 300")),
    B("Now the whole number. Where does the point in 3.25 land when we multiply by 100?",
      ask=CHOOSE(["32.5", "325", "3250"], 1,
                 "Times 10 moves the point one place, and that gives 32.5. Times 100 is times 10 twice, so the point moves two places.")),
    B("Two places to the right: past the 2, then past the 5. 3.25 becomes 325.",
      *ANSC("l2", "3.25 × 100 = 325", 325)),
    B("Check with the parts: 0.25 times 100 is 25, and 300 plus 25 is 325.",
      W("l3", "0.25 × 100 = 25"), W("l4", "300 + 25 = 325")),
    B("So to multiply by 100, move the decimal point two places to the right: one place for each zero in 100."),
)

# 57 ÷ 10 (warm-up).
LESSONS["G5A_DECIMALS_015"] = LESSON(
    B("What is 57 divided by 10?",
      W("q", "57 ÷ 10 = ?", "given")),
    B("First, where is the decimal point in 57? It is hiding at the end: 57 is the same as 57.0.",
      W("l1", "57 = 57.0")),
    B("Dividing by 10 moves the point one place. Which way does it go?",
      ask=CHOOSE(["to the left: smaller", "to the right: bigger"], 0,
                 "Dividing shares the number out, so the answer must be smaller than 57. The point moves to the left.")),
    B("One place to the left puts the point between the 5 and the 7. So 57 becomes 5.7.",
      *ANSC("l2", "57 ÷ 10 = 5.7", "5.7")),
    B("The 5 tens became 5 ones, and the 7 ones became 7 tenths. No zero sneaks in between them, so it is not 5.07.",
      W("l3", "5.07 ≠ 5.7")),
    B("Check by going back: 5.7 times 10 moves the point one place to the right, and gives 57 again.",
      W("l4", "5.7 × 10 = 57")),
    B("So to divide by 10, move the decimal point one place to the left. 57 divided by 10 is 5.7."),
)

# Seven tenths as a decimal (warm-up).
LESSONS["G5A_DECIMALS_016"] = LESSON(
    B("How do we write seven tenths as a decimal?",
      GIVEN("q", "seven tenths = ?")),
    B("Tenths are what you get when one whole is cut into 10 equal parts. Seven tenths is 7 of those parts.",
      W("l1", "7/10")),
    B("Is seven tenths more than 1 whole, or less than 1 whole?",
      ask=CHOOSE(["more than 1", "less than 1"], 1,
                 "We have only 7 of the 10 parts, so we do not have the whole thing yet. It is less than 1.")),
    B("Less than 1, so there are no ones. We write 0 in the ones place, and then the decimal point.",
      LB("l2", "ones . tenths")),
    B("The first place after the point is the tenths place. That is where our 7 goes.",
      *ANSC("l3", "7/10 = 0.7", "0.7")),
    B("Careful: 0.07 has the 7 in the second place. That means seven hundredths, which is much smaller.",
      W("l4", "0.07 = 7/100")),
    B("So tenths live in the first place after the point. Seven tenths is 0.7."),
)

# 4P27Q divisible by 5 and 9: how many numbers?
LESSONS["G5A_DIVISIBILITY_001"] = LESSON(
    B("The number 4 P 2 7 Q can be divided by both 5 and 9. P and Q are missing digits. How many different numbers fit?",
      GIVEN("q", "4P27Q is divisible by 5 and by 9")),
    B("Two rules to use. Start with 5, because it only looks at the last digit. What can Q be?",
      ask=CHOOSE(["only 5", "0 or 5", "any digit"], 1,
                 "Think of 10: it is a multiple of 5 as well, and it ends in 0. So a multiple of 5 ends in 0 or in 5.")),
    B("So there are two cases, Q is 0 and Q is 5, and we must try both.",
      LB("l1", "Q = 0  or  Q = 5")),
    B("Now the rule for 9: the digits must add up to a multiple of 9. With Q as 0, the digits we know are 4, 2, 7 and 0. They add up to 13.",
      W("l2", "4 + 2 + 7 + 0 = 13")),
    B("13 plus P must be a multiple of 9. The next one after 13 is 18, so P is 5. That is one number: 45,270.",
      W("l3", "13 + 5 = 18"), LB("n1", "45,270")),
    B("Now Q as 5. The digits 4, 2, 7 and 5 add up to 18. That is already a multiple of 9!",
      W("l4", "4 + 2 + 7 + 5 = 18")),
    B("So 18 plus P must be a multiple of 9. Which digits can P be?",
      ask=CHOOSE(["only 9", "only 0", "0 or 9"], 2,
                 "18 is already a multiple of 9, so adding 0 keeps it there. Adding 9 takes us to the next multiple. Both work.")),
    B("P can be 0, which gives 40,275. Or P can be 9, which gives 49,275. Two more numbers.",
      W("l5", "18 + 0 = 18"), W("l6", "18 + 9 = 27"), LB("n2", "40,275 and 49,275")),
    B("Count them up: 1 number when Q is 0, and 2 numbers when Q is 5. That makes 3.",
      *ANSC("l7", "1 + 2 = 3", 3)),
    B("Two traps here: forgetting that a multiple of 5 can end in 0, and forgetting that P itself can be 0."),
    B("So take the rule with fewer choices first, split into cases, and count every case. 3 numbers fit."),
)

# 4P8 divisible by 6 but not by 9: how many digits?
LESSONS["G5A_DIVISIBILITY_002"] = LESSON(
    B("The number 4 P 8 can be divided by 6, but NOT by 9. How many different digits can P be?",
      GIVEN("q", "4P8: divisible by 6, NOT by 9")),
    B("Divisible by 6 means divisible by 2 and by 3. The number ends in 8, so it is even whatever P is. That leaves only the rule for 3.",
      UL("q", "8")),
    B("For 3, the digits must add up to a multiple of 3. 4 plus 8 is 12, so the digits add up to 12 plus P.",
      W("l1", "4 + 8 = 12"), LB("l2", "digit sum = 12 + P")),
    B("12 is already a multiple of 3. So which digits can P be?",
      ask=CHOOSE(["3, 6, 9", "0, 3, 6, 9", "6 only"], 1,
                 "12 is a multiple of 3 already, so P must add a multiple of 3: that is 0, 3, 6 or 9. Do not leave out the 0.")),
    B("Four digits pass the rule for 6. Here are their digit sums: 12, 15, 18 and 21.",
      W("l3", "12 + 0 = 12"), W("l4", "12 + 3 = 15"), W("l5", "12 + 6 = 18"), W("l6", "12 + 9 = 21")),
    B("But the question also says NOT divisible by 9. Which of these digit sums is a multiple of 9?",
      ask=CHOOSE(["12", "15", "18", "21"], 2,
                 "Count in nines: 9, then 18. Only 18 is in our list, and it comes from P being 6.")),
    B("So 6 is out, because 468 can be divided by 9. We cross it off.",
      W("l7", "468 ÷ 9 = 52"), STRIKE("l5", "12 + 6 = 18", "÷ 9")),
    B("That leaves 0, 3 and 9. So P can be 3 different digits.",
      *ANSLC("l8", "P = 0, 3 or 9: that is 3 digits", "3 digits")),
    B("The trap is to stop at 4, the digits that pass the rule for 6. Always read on to the word NOT."),
    B("So list everything that fits the first rule, then strike out what breaks the second. 3 digits are left."),
)

# Exactly three factors, 1 to 50.
LESSONS["G5A_DIVISIBILITY_003"] = LESSON(
    B("How many whole numbers from 1 to 50 have exactly three factors?",
      GIVEN("q", "1 to 50: exactly three factors?")),
    B("Factors usually come in pairs. Look at 12: 1 with 12, 2 with 6, 3 with 4. Pairs give an even number of factors.",
      W("l1", "12 = 1 × 12 = 2 × 6 = 3 × 4")),
    B("But three is odd. What kind of number has an odd number of factors?",
      ask=CHOOSE(["a prime number", "a square number", "an even number"], 1,
                 "A prime has just 2 factors. For an odd count, one factor must pair with itself, like 3 times 3. That happens only in a square number.")),
    B("So we only need the square numbers up to 50. Here they are.",
      LB("sq", "1, 4, 9, 16, 25, 36, 49")),
    B("Now count the factors of each. 4 has 1, 2 and 4. 9 has 1, 3 and 9. Three factors each.",
      CIRC("sq", "4"), CIRC("sq", "9")),
    B("Careful with 16. Its factors are 1, 2, 4, 8 and 16. That is five. 36 has even more, and 1 has only one factor.",
      LB("l2", "16: 1, 2, 4, 8, 16"), STRIKE("sq", "16"), STRIKE("sq", "36"), STRIKE("sq", "1")),
    B("25 has 1, 5 and 25. 49 has 1, 7 and 49. Three factors each.",
      CIRC("sq", "25"), CIRC("sq", "49")),
    B("Did you spot it? 4, 9, 25 and 49 are the squares of 2, 3, 5 and 7, the prime numbers.",
      W("l3", "2² = 4"), W("l4", "3² = 9"), W("l5", "5² = 25"), W("l6", "7² = 49")),
    B("So 4 numbers have exactly three factors.",
      *ANSLC("l7", "4, 9, 25, 49: that is 4 numbers", "4 numbers")),
    B("The trap is to count all 7 squares. Only the square of a prime has exactly three factors: 1, the prime, and the square itself."),
)

# Smallest number with exactly 6 factors.
LESSONS["G5A_DIVISIBILITY_004"] = LESSON(
    B("What is the smallest whole number that has exactly 6 factors? The choices are 12, 18, 32 and 16.",
      GIVEN("q", "Smallest number with exactly 6 factors?"), LB("o", "12, 18, 32, 16")),
    B("Count factors in pairs, so none get lost. Start with 12: 1 times 12, 2 times 6, 3 times 4.",
      W("l1", "12 = 1 × 12 = 2 × 6 = 3 × 4")),
    B("How many factors does 12 have?",
      ask=CHOOSE(["3", "6", "5"], 1,
                 "Each pair holds two factors. Three pairs make 6 factors: 1, 2, 3, 4, 6 and 12.")),
    B("6 factors. But wait: 18 and 32 have three pairs each, so they have 6 factors as well.",
      W("l2", "18 = 1 × 18 = 2 × 9 = 3 × 6"), W("l3", "32 = 1 × 32 = 2 × 16 = 4 × 8")),
    B("And 16 has only five: 1, 2, 4, 8 and 16, because 4 pairs with itself.",
      W("l4", "16 = 1 × 16 = 2 × 8 = 4 × 4"), STRIKE("o", "16")),
    B("So three of the choices have 6 factors. The question asks for the smallest, and 12 is the smallest of them.",
      CIRC("o", "12")),
    B("Could a number below 12 have 6 factors? No: 6, 8 and 10 have four each, 4 and 9 have three, and the primes have two.",
      W("l5", "6 = 1 × 6 = 2 × 3"), W("l6", "8 = 1 × 8 = 2 × 4"), W("l7", "10 = 1 × 10 = 2 × 5")),
    B("So the smallest number with exactly 6 factors is 12.",
      *ANSLC("l8", "12 has 6 factors: 1, 2, 3, 4, 6, 12", "12")),
    B("The trap is to stop at the first number you check, or to pick a bigger one that also works. Count in pairs, then choose the smallest."),
)

# p, p + 2, p + 4 all prime.
LESSONS["G5A_DIVISIBILITY_005"] = LESSON(
    B("p, p plus 2 and p plus 4 are all prime numbers. What is the sum of the three primes?",
      GIVEN("q", "p, p + 2, p + 4 are all prime")),
    B("We do not know p, so let's try the small primes one by one. Try 2: we get 2, 4 and 6. But 4 and 6 are even, so they are not prime.",
      LB("l1", "p = 2:  2, 4, 6"), STRIKE("l1", "2, 4, 6")),
    B("Try 3: we get 3, 5 and 7. Are all three prime?",
      LB("l2", "p = 3:  3, 5, 7"),
      ask=CHOOSE(["yes, all three", "no, 5 is not", "no, 7 is not"], 0,
                 "3, 5 and 7 each have only two factors: 1 and the number itself. So all three are prime.")),
    B("All prime! But is it the only set? Try 5: we get 5, 7 and 9. And 9 is 3 times 3.",
      LB("l3", "p = 5:  5, 7, 9"), W("l4", "9 = 3 × 3"), STRIKE("l3", "9")),
    B("Try 7: we get 7, 9 and 11. There is 9 again. Try 11: we get 11, 13 and 15, and 15 is 3 times 5.",
      LB("l5", "p = 7:  7, 9, 11"), LB("l6", "p = 11:  11, 13, 15"), W("l7", "15 = 3 × 5")),
    B("Here is why it keeps breaking. In three numbers that go up in twos like this, one is always a multiple of 3. It can only be prime if it is 3 itself."),
    B("So the only set is 3, 5 and 7. Add them: 3 plus 5 plus 7 is 15.",
      *ANSC("l8", "3 + 5 + 7 = 15", 15)),
    B("One trap is to start from 1: 1, 3 and 5. But 1 is not a prime number, because it has only one factor."),
    B("So when you do not know the number, test small cases in order and look for the reason the others break. The sum is 15."),
)
