"""Imported batch 06, part a: factors and primes (11 lessons, each written for its question)."""
from imported_06_lib import ANS, B, C, FIG, GIVEN, M, N, QID, S, W, choose, lesson

LESSONS = {}

# 72 samosas on equal plates: count the factors of 72 in pairs.
LESSONS[QID("bbb676d2")] = lesson(
    B("Aarav shares 72 samosas equally on plates, with none left over. We want to know how many different numbers of plates will work.",
      GIVEN("g", "72 samosas, equal plates, none left over", True)),
    B("If 72 shares out exactly among the plates, what kind of number must the number of plates be?",
      ask=choose(["a multiple of 72", "a factor of 72", "an even number"], 1,
                 "Try 5 plates: 72 does not share out exactly by 5, so 5 is no good. The number of plates has to divide 72 exactly, "
                 "and a number that does that is a factor of 72.")),
    B("So we count the factors of 72. Factors come in pairs that multiply to make 72. Start with 1: its partner is 72 itself.",
      W("p1", "1 × 72 = 72")),
    B("Carry on in order. 2 times 36. 3 times 24. 4 times 18.",
      W("p2", "2 × 36 = 72"), W("p3", "3 × 24 = 72"), W("p4", "4 × 18 = 72")),
    B("5 does not go into 72. 6 does: 6 times 12. 7 does not. And 8 times 9 is 72.",
      W("p5", "6 × 12 = 72"), W("p6", "8 × 9 = 72")),
    B("The next number to try is 9. Do we need to keep going?",
      ask=choose(["Yes, all the way to 72", "No, the pairs have met", "Yes, up to 36"], 1,
                 "Look at the last pair: 9 is already there, as the partner of 8. From here on, every factor is one we have "
                 "written down already.")),
    B("So the list is complete: 6 pairs, with 2 factors in each. 6 times 2 is 12.",
      W("n", "6 × 2 = 12"), ANS("ans", "72 has 12 factors", True), C("ans", "12")),
    B("Here they are in order, from 1 plate up to 72 plates. Count them: 12.",
      W("list", "1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72", label=True)),
    B("Careful: the question counts 1 plate and 72 plates as well. Leave those two out and you would say 10.",
      M("list", "1"), M("list", "72")),
    B("So to count the ways to share equally, count factors. Write them in pairs, starting from 1, and stop when the pairs meet. "
      "Aarav has 12 choices."),
)

# 72 bulbs in equal rows: the same count, done with primes and a table.
LESSONS[QID("bd9683ef")] = lesson(
    B("Priya has 72 bulbs to put in equal rows, with none left over. We need to count how many row sizes are possible.",
      GIVEN("g", "72 bulbs in equal rows, none left over", True)),
    B("A row size works only if it divides 72 exactly. So we are counting the factors of 72. Let's do it a clever way, "
      "by breaking 72 into primes.",
      FIG("f1", {"kind": "factorTree", "number": 72})),
    B("72 is 8 times 9. And 8 is 2 times 2 times 2, while 9 is 3 times 3.",
      W("a", "72 = 8 × 9"), W("b", "72 = 2 × 2 × 2 × 3 × 3")),
    B("Every factor of 72 is built from some of those 2s and some of those 3s. From the 2s alone we can make 1, 2, 4 or 8. "
      "What can we make from the 3s alone?",
      ask=choose(["3 or 9", "1, 3 or 9", "3, 6 or 9"], 1,
                 "We may use no 3s at all, and that gives 1. One 3 gives 3, and both 3s give 9. So there are 3 choices: 1, 3 and 9.")),
    B("Now match every choice from the 2s with every choice from the 3s, and multiply. This table shows them all.",
      FIG("f2", {"kind": "table", "headers": ["×", "1", "2", "4", "8"],
                 "rows": [["1", "1", "2", "4", "8"], ["3", "3", "6", "12", "24"], ["9", "9", "18", "36", "72"]]})),
    B("The table has 4 columns and 3 rows of answers. 4 times 3 is 12 boxes, and each box holds a different factor.",
      W("n", "4 × 3 = 12")),
    B("So 72 has 12 factors, and Priya can arrange her bulbs in 12 ways.",
      ANS("ans", "72 has 12 factors", True), C("ans", "12")),
    B("Test a couple of boxes. 24 is in the table, and 24 times 3 is 72. 18 is there too, and 18 times 4 is 72.",
      W("c1", "24 × 3 = 72"), W("c2", "18 × 4 = 72")),
    B("Don't leave out the two ends: 1 bulb in each row, and all 72 in one row. They are equal rows too."),
    B("To count factors, break the number into primes, see how many choices each prime gives, and multiply. "
      "Here that was 4 times 3, which is 12."),
)

# 84 chocolates, more than 5 each: the largest factor whose partner is above 5.
LESSONS[QID("c2bc13fb")] = lesson(
    B("Riya shares 84 chocolates equally among her friends, with none left over. Each friend must get more than 5. "
      "What is the largest number of friends she can invite?",
      GIVEN("g", "84 chocolates, shared equally, more than 5 each", True)),
    B("None are left over, so the number of friends must be a factor of 84. Let's write the factor pairs, starting from 1.",
      W("p1", "1 × 84 = 84"), W("p2", "2 × 42 = 84"), W("p3", "3 × 28 = 84")),
    B("Then 4 times 21, 6 times 14, and 7 times 12. After that the pairs just repeat.",
      W("p4", "4 × 21 = 84"), W("p5", "6 × 14 = 84"), W("p6", "7 × 12 = 84")),
    B("In each pair, one number can be the friends and the other is what each friend gets. We want as many friends as we can. "
      "So what do we want each share to be?",
      ask=choose(["as big as possible", "as small as the rule allows", "exactly 5"], 1,
                 "More friends means fewer chocolates each. So for the most friends, we want the smallest share that is "
                 "still allowed: just over 5.")),
    B("The share must be more than 5. Careful: 5 itself is not more than 5. Looking down our pairs, the smallest share above 5 is 6.",
      C("p5", "6")),
    B("A share of 6 goes with 14 friends. So 14 friends get 6 chocolates each.",
      ANS("ans", "84 ÷ 14 = 6"), C("ans", "14")),
    B("Could she invite more? The next factor up is 21. But then each friend gets only 4, and that breaks the rule.",
      W("t", "84 ÷ 21 = 4"), S("p4", "21", "share is only 4")),
    B("So 14 is the most friends Riya can invite. For a question like this, list the factor pairs, then pick the pair that fits the rule."),
)

# How many factors does 60 have?
LESSONS[QID("dcb89086")] = lesson(
    B("Priya has 60 packets. We are told 60 shares equally among 2, 3, 4, 5 or 6 teams. The question is: "
      "how many factors does 60 have in total?",
      GIVEN("g", "How many factors does 60 have?", True)),
    B("The story hands us 5 factors already: 2, 3, 4, 5 and 6. But each factor has a partner that multiplies with it to make 60. "
      "What is the partner of 4?",
      ask=choose(["15", "16", "56"], 0,
                 "We need the number that 4 multiplies by to make 60. 4 times 15 is 60, so the partner of 4 is 15.")),
    B("Let's write every pair, in order from 1. 1 times 60, 2 times 30, 3 times 20.",
      W("p1", "1 × 60 = 60"), W("p2", "2 × 30 = 60"), W("p3", "3 × 20 = 60")),
    B("4 times 15, 5 times 12, 6 times 10.",
      W("p4", "4 × 15 = 60"), W("p5", "5 × 12 = 60"), W("p6", "6 × 10 = 60")),
    B("7, 8 and 9 do not go into 60. And 10 is already on the board, as the partner of 6. So the pairs have met, "
      "and the list is complete.",
      M("p6", "10")),
    B("6 pairs, with 2 factors in each. 6 times 2 is 12.",
      W("n", "6 × 2 = 12"), ANS("ans", "60 has 12 factors", True), C("ans", "12")),
    B("In order they are 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30 and 60. Count them: 12.",
      W("list", "1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60", label=True)),
    B("Two slips to watch. Stopping at the 5 factors in the story misses their partners. And forgetting 1 and 60 themselves gives 10."),
    B("So to count factors, hunt in pairs from 1 upwards, and stop when the pairs meet. 60 has 12 factors."),
)

# A prime between 40 and 50 that leaves 1 when shared among 3.
LESSONS[QID("eca45cd9")] = lesson(
    B("Priya's coins are a prime number, more than 40 and less than 50. Shared among 3 friends, 1 coin is left over. How many coins?",
      GIVEN("g", "prime, between 40 and 50, ÷ 3 leaves 1 over", True)),
    B("Two clues. Take the first one: a prime between 40 and 50. Here are the numbers from 41 to 49.",
      W("row", "41  42  43  44  45  46  47  48  49", label=True)),
    B("Cross out the even ones straight away. 2 goes into all of them, so they cannot be prime.",
      S("row", "42"), S("row", "44"), S("row", "46"), S("row", "48")),
    B("That leaves 41, 43, 45, 47 and 49. Which of these are not prime?",
      ask=choose(["only 45", "45 and 49", "none, they are all prime"], 1,
                 "45 ends in 5, so 5 goes into it. And 49 is 7 times 7. Each has an extra factor, so neither is prime.")),
    B("45 is 5 times 9, and 49 is 7 times 7. Out they go. The primes are 41, 43 and 47.",
      W("n1", "45 = 5 × 9"), W("n2", "49 = 7 × 7"), S("row", "45"), S("row", "49")),
    B("Now the second clue: share among 3, and 1 is left over. Try 41. It is 3 times 13, plus 2. That leaves 2 over, so not this one.",
      W("d1", "41 = 3 × 13 + 2")),
    B("Try 43. It is 3 times 14, plus 1. Exactly 1 coin left over. That fits!",
      W("d2", "43 = 3 × 14 + 1"), M("d2", "+ 1")),
    B("And to be sure, 47 is 3 times 15, plus 2. So only 43 fits both clues.",
      W("d3", "47 = 3 × 15 + 2"), ANS("ans", "43 coins", True), C("row", "43")),
    B("Did you notice 45 among the choices? It sits between 40 and 50, but it is not prime, so the first clue rules it out."),
    B("With two clues, use one to make a short list, then test each number on the list with the other. Priya has 43 coins."),
)

# Primes between 90 and 100.
LESSONS[QID("ch01_q035")] = lesson(
    B("How many prime numbers are there between 90 and 100? Let's write out the numbers from 91 to 99 and test them.",
      GIVEN("g", "Primes between 90 and 100?", True), W("row", "91  92  93  94  95  96  97  98  99", label=True)),
    B("A prime has exactly 2 factors: 1 and itself. The even numbers have 2 as an extra factor, so cross them out.",
      S("row", "92"), S("row", "94"), S("row", "96"), S("row", "98")),
    B("95 ends in 5, so 5 goes into it. 5 times 19 is 95. Cross it out.",
      W("n1", "5 × 19 = 95"), S("row", "95")),
    B("Now 93 and 99. Is there a quick way to test whether 3 goes into a number?",
      ask=choose(["look at the last digit", "add up the digits", "halve the number"], 1,
                 "For 3, add up the digits. If the total is in the 3 times table, then so is the number.")),
    B("9 plus 3 is 12, and 9 plus 9 is 18. Both totals are in the 3 times table, so 3 goes into 93 and into 99. Cross them out.",
      W("n2", "9 + 3 = 12"), W("n3", "9 + 9 = 18"), S("row", "93"), S("row", "99")),
    B("Only 91 and 97 are left. Here is the trap: 91 looks prime, but 7 times 13 is 91. Always try 7.",
      W("n4", "7 × 13 = 91"), S("row", "91")),
    B("Now 97. It is odd, and it does not end in 5. Its digits add up to 16, which is not in the 3 times table.",
      W("n5", "9 + 7 = 16")),
    B("And 7? 7 times 13 is 91 and 7 times 14 is 98, so the 7 times table jumps right over 97. Nothing goes in. 97 is prime.",
      W("n6", "7 × 14 = 98"), C("row", "97")),
    B("So there is just 1 prime number between 90 and 100.",
      ANS("ans", "Only 97 is prime: 1 prime number", True), C("ans", "1 prime number")),
    B("To test a number below 100, try 2, 3, 5 and 7. If none of them goes in, the number is prime."),
)

# Primes between 1 and 50.
LESSONS[QID("ch01_q036")] = lesson(
    B("How many prime numbers are there between 1 and 50? We will collect them, ten at a time.",
      GIVEN("g", "How many primes between 1 and 50?", True)),
    B("First, a question about the very start. Is 1 a prime number?",
      ask=choose(["Yes, it is the first prime", "No, it has only one factor"], 1,
                 "A prime has exactly 2 different factors: 1 and itself. The number 1 has just one factor. "
                 "So 1 is not prime, and our list starts at 2.")),
    B("From 2 to 10 the primes are 2, 3, 5 and 7. That is 4 of them. Notice 9 is missing: it is 3 times 3.",
      W("r1", "2 to 10:  2, 3, 5, 7", label=True), N("r1", "2, 3, 5, 7", "4 primes")),
    B("From 11 to 20: 11, 13, 17 and 19. 4 more. 15 is left out because it is 3 times 5.",
      W("r2", "11 to 20:  11, 13, 17, 19", label=True), N("r2", "11, 13, 17, 19", "4 primes"), W("x1", "15 = 3 × 5")),
    B("From 21 to 30 there are only 2: 23 and 29. 21 is 3 times 7, 25 is 5 times 5, and 27 is 3 times 9.",
      W("r3", "21 to 30:  23, 29", label=True), W("x2", "21 = 3 × 7"), W("x3", "25 = 5 × 5"), W("x4", "27 = 3 × 9")),
    B("From 31 to 40, again 2: 31 and 37. 33 is 3 times 11, 35 is 5 times 7, and 39 is 3 times 13.",
      W("r4", "31 to 40:  31, 37", label=True), W("x5", "33 = 3 × 11"), W("x6", "35 = 5 × 7"), W("x7", "39 = 3 × 13")),
    B("From 41 to 50 there are 3: 41, 43 and 47. Watch out for 49. It looks prime, but it is 7 times 7.",
      W("r5", "41 to 50:  41, 43, 47", label=True), W("x8", "49 = 7 × 7")),
    B("Now add the groups: 4, 4, 2, 2 and 3. That makes 15.",
      W("sum", "4 + 4 + 2 + 2 + 3 = 15"), ANS("ans", "15 primes between 1 and 50", True), C("ans", "15")),
    B("There are 25 odd numbers below 50, but that is not the answer. Odd numbers like 9, 15 and 21 are not prime."),
    B("So work in tens, and test each odd number with 3, 5 and 7. Between 1 and 50 there are 15 primes."),
)

# Odd primes between 1 and 100: all 25, less the 2.
LESSONS[QID("ch01_q037")] = lesson(
    B("How many odd prime numbers are there between 1 and 100? That little word odd is the key to this one.",
      GIVEN("g", "How many odd primes between 1 and 100?", True)),
    B("Nearly every prime number is odd. Which primes are even?",
      ask=choose(["2 and 4", "only 2", "none of them"], 1,
                 "2 has exactly 2 factors, 1 and 2, so it is prime, and it is even. Every other even number has 2 as an "
                 "extra factor. So 2 is the only even prime.")),
    B("So here is the plan. Count all the primes up to 100, then take away 1 for the number 2.",
      W("plan", "odd primes = all primes − 1", label=True)),
    B("From 1 to 20 there are 8 primes. Here they are.",
      W("r1", "1 to 20:  2, 3, 5, 7, 11, 13, 17, 19", label=True), N("r1", "2, 3, 5, 7, 11, 13, 17, 19", "8 primes")),
    B("From 21 to 50 there are 7. Remember 49 is not one of them: it is 7 times 7.",
      W("r2", "21 to 50:  23, 29, 31, 37, 41, 43, 47", label=True), N("r2", "23, 29, 31, 37, 41, 43, 47", "7 primes"),
      W("x1", "49 = 7 × 7")),
    B("From 51 to 80 there are 7 more. Careful with 51 and 57: 3 goes into both. And 77 is 7 times 11.",
      W("r3", "51 to 80:  53, 59, 61, 67, 71, 73, 79", label=True), N("r3", "53, 59, 61, 67, 71, 73, 79", "7 primes"),
      W("x2", "51 = 3 × 17"), W("x3", "57 = 3 × 19"), W("x4", "77 = 7 × 11")),
    B("From 81 to 100 there are just 3: 83, 89 and 97. The sneaky ones here are 87, which is 3 times 29, and 91, which is 7 times 13.",
      W("r4", "81 to 100:  83, 89, 97", label=True), N("r4", "83, 89, 97", "3 primes"),
      W("x5", "87 = 3 × 29"), W("x6", "91 = 7 × 13")),
    B("Add them up: 8, 7, 7 and 3 make 25. There are 25 primes below 100. That is a number worth remembering.",
      W("sum", "8 + 7 + 7 + 3 = 25")),
    B("Now take away the even one, the 2. 25 minus 1 is 24.",
      S("r1", "2", "even", nth=2), ANS("ans", "25 − 1 = 24"), C("ans", "24")),
    B("The trap is to stop at 25 and forget that the question said odd. Count all the primes, then remove the 2. "
      "There are 24 odd primes."),
)

# Even primes between 1 and 100: only the number 2.
LESSONS[QID("ch01_q038")] = lesson(
    B("How many even prime numbers are there between 1 and 100? Let's remind ourselves what the two words mean.",
      GIVEN("g", "How many even primes between 1 and 100?", True)),
    B("An even number is one that 2 goes into. A prime has exactly 2 factors: 1 and itself. Start with the first even number, 2. "
      "Its only factors are 1 and 2, so 2 is prime.",
      W("a", "2 = 1 × 2"), C("a", "2")),
    B("Now try the next even number, 4. How many factors does 4 have?",
      ask=choose(["2", "3", "4"], 1,
                 "1 times 4 is 4, and 2 times 2 is 4. So the factors of 4 are 1, 2 and 4. That is 3 factors, one too many for a prime.")),
    B("4 is 2 times 2. 6 is 2 times 3. 8 is 2 times 4. Can you see the pattern?",
      W("b", "4 = 2 × 2"), W("c", "6 = 2 × 3"), W("d", "8 = 2 × 4")),
    B("Every even number after 2 is 2 times something. So it always has at least 3 factors: 1, 2 and itself. It can never be prime.",
      W("rule", "even number after 2: factors 1, 2 and itself", label=True)),
    B("That goes all the way up to 100, which is 2 times 50.",
      W("e", "100 = 2 × 50")),
    B("So the only even prime is 2. That makes 1 even prime number.",
      ANS("ans", "Even primes: only the number 2, so 1", True), C("ans", "1")),
    B("Read the question carefully, though. It asks how many, not which one. The prime is 2, but the count is 1."),
    B("Remember this fact: 2 is the only even prime. Every other prime is odd."),
)

# Which digit can never be the units digit of a prime?
LESSONS[QID("ch01_q039")] = lesson(
    B("Which of these digits can never be the last digit of a prime number? The choices are 5, 3, 7 and 4.",
      GIVEN("g", "Which digit can never end a prime number?", True), W("ch", "Choices:  5,  3,  7,  4", label=True)),
    B("To show a digit can end a prime, one example is enough. 13 is prime and ends in 3. 17 is prime and ends in 7. "
      "So 3 and 7 are fine.",
      W("ex", "13 and 17 are prime", label=True), S("ch", "3", "13"), S("ch", "7", "17")),
    B("What about 5? Numbers like 15, 25 and 35 are in the 5 times table, so they are not prime. "
      "Is there any prime at all that ends in 5?",
      W("fives", "5, 15, 25, 35, ...", label=True),
      ask=choose(["No, never", "Yes, 5 itself", "Yes, 15"], 1,
                 "15 is 3 times 5, so it is not prime. But look at the smallest number ending in 5, which is 5 itself. "
                 "Its only factors are 1 and 5, so it is prime.")),
    B("So 5 can end a prime, because 5 is prime. Cross it off.",
      S("ch", "5", "5 is prime"), C("fives", "5")),
    B("That leaves 4. The numbers that end in 4 are 4, 14, 24, 34 and so on.",
      W("fours", "4, 14, 24, 34, ...", label=True)),
    B("Every one of them is even, so 2 goes into it. 4 is 2 times 2, 14 is 2 times 7, 24 is 2 times 12. "
      "Each has 2 as an extra factor.",
      W("f1", "4 = 2 × 2"), W("f2", "14 = 2 × 7"), W("f3", "24 = 2 × 12")),
    B("So a number ending in 4 is never prime. The digit is 4.",
      ANS("ans", "A prime never ends in 4", True), C("ch", "4"), C("ans", "4")),
    B("The trap here is 5. Almost every number ending in 5 is not prime, but one example is enough, and 5 itself is prime."),
    B("In fact, a prime with 2 digits or more can only end in 1, 3, 7 or 9."),
)

# 13, 17, 19, 23, 27, 29: the one that is not prime.
LESSONS[QID("ch03_q032")] = lesson(
    B("Here are 6 numbers. One of them does not belong with the rest. Let's find out what the others have in common.",
      GIVEN("g", "13, 17, 19, 23, 27, 29", True)),
    B("They are all odd, so that cannot be what splits them. What else could the group be?",
      ask=choose(["multiples of 3", "prime numbers", "numbers in the 7 times table"], 1,
                 "Look at 13. Nothing goes into it except 1 and 13. A number like that is prime. "
                 "So let's test whether each number here is prime.")),
    B("For numbers this small, we only need to try 2, 3 and 5. Start with 13, 17 and 19. All odd, none ends in 5, "
      "and none is in the 3 times table. They are prime.",
      M("g", "13"), M("g", "17"), M("g", "19")),
    B("23 and 29 pass the same tests. They are prime as well.",
      M("g", "23"), M("g", "29")),
    B("Now 27. It is odd, and it does not end in 5. But does 3 go into it?",
      ask=choose(["No, 27 is prime", "Yes, 3 × 9 = 27"], 1,
                 "Add the digits: 2 plus 7 is 9, and 9 is in the 3 times table. So 27 is too. In fact 3 times 9 is 27.")),
    B("3 times 9 is 27. So 27 has extra factors, 3 and 9, and it is not prime.",
      W("n", "27 = 3 × 9"), C("g", "27")),
    B("Every other number in the group is prime. 27 is the one that does not belong.",
      ANS("ans", "27 does not belong: it is not prime", True)),
    B("The trap is thinking that odd means prime. 27 is odd, but 3 goes into it. To find the odd one out, "
      "look for what the others share, then test each number."),
)
