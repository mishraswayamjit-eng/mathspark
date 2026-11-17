"""Batch 05: divisibility, factors and primes (eleven one-off questions)."""
from imported_05_lib import ANS, B, GIVEN, M, N, RING, S, W, ask, lesson

LESSONS = {}

P = "AIGEN_grade5_"

# ── A number that splits into several group sizes ────────────────────────────

LESSONS[P + "1bac6564-782c-49c3-a343-aaebe55372db"] = lesson(
    B("Rohan's coins split into groups of 5 with none left over, and into groups of 3 with none left over. And he has between 40 and 60 coins.",
      GIVEN("q", "Groups of 5: none left. Groups of 3: none left.", True), W("q2", "Between 40 and 60", True)),
    B("None left over in 5s means the number is a multiple of 5. None left over in 3s means it is a multiple of 3 as well."),
    B("A number that is a multiple of both 3 and 5 must be a multiple of what?",
      ask=ask("15", ["8", "30"],
              "Count in 5s until you land on a multiple of 3: 5, 10, 15. So 15 is the first number they share, and every other shared one is a multiple of 15.")),
    B("3 times 5 is 15. So let's count in 15s: 15, 30, 45, 60.",
      W("m", "3 × 5 = 15"), W("l", "15, 30, 45, 60", True)),
    B("Which of these lies between 40 and 60? Only 45. And 60 itself is the edge, so it is not between.",
      M("l", "45", "circle"), S("l", "60", "the edge")),
    B("Rohan has 45 coins.",
      ANS("a", "Coins = 45", True), RING("a", "45")),
    B("Check both clues. 45 divided by 5 is 9, and 45 divided by 3 is 15. Nothing left over either time.",
      W("c1", "45 ÷ 5 = 9"), W("c2", "45 ÷ 3 = 15")),
    B("Careful: plenty of numbers here split into 5s but leave coins over in 3s. For two clues at once, find the first number both share, then count in that."),
)

LESSONS[P + "a157f53d-ee23-4909-9dc2-1e56c48673c5"] = lesson(
    B("Arjun's samosas go into groups of 2, or 3, or 5, with none left over each time. He has more than 50 but fewer than 80.",
      GIVEN("q", "Groups of 2, 3 or 5: none left over", True), W("q2", "More than 50, fewer than 80", True)),
    B("Nothing left over in 2s, 3s or 5s. So the number is a multiple of 2, and of 3, and of 5, all at the same time."),
    B("What is the smallest number that 2, 3 and 5 all divide?",
      ask=ask("30", ["10", "15"],
              "10 splits into 2s and 5s, but not into 3s. 15 splits into 3s and 5s, but not into 2s. We need all three at once, and that first happens at 30.")),
    B("2 times 3 times 5 is 30. Every number that works is a multiple of 30.",
      W("m", "2 × 3 × 5 = 30"), W("l", "30, 60, 90, ...", True)),
    B("Which one is more than 50 and fewer than 80? 30 is too small and 90 is too big. Only 60 fits.",
      M("l", "60", "circle"), ANS("a", "Samosas = 60", True), RING("a", "60")),
    B("Check. 60 divided by 2 is 30. 60 divided by 3 is 20. 60 divided by 5 is 12. No remainders.",
      W("c1", "60 ÷ 2 = 30"), W("c2", "60 ÷ 3 = 20"), W("c3", "60 ÷ 5 = 12")),
    B("Careful with the other choices. 70 will not split into 3s, 75 will not split into 2s, and 72 will not split into 5s. Each one passes two tests but not all three.",
      W("x", "70 ÷ 3, 75 ÷ 2, 72 ÷ 5: each leaves some over", True)),
    B("So when a number must split into several group sizes, find the smallest number they all share, then count in that."),
)

LESSONS[P + "382913bb-709d-424f-b9c1-e4ea45a9cf42"] = lesson(
    B("Three clues about Rohan's coins. In 2s, 1 is left over. In 3s, 1 is left over. In 5s, none is left over. And there are fewer than 50.",
      GIVEN("q", "2s: 1 left. 3s: 1 left. 5s: none left.", True), W("q2", "Fewer than 50 coins", True)),
    B("Which clue is the easiest one to start with?",
      ask=ask("groups of 5, none left over", ["groups of 2, 1 left over", "groups of 3, 1 left over"],
              "A clue with nothing left over gives a simple list: the multiples of 5. The other clues can then cross numbers off that list.")),
    B("So write the multiples of 5 below 50.",
      W("l", "5, 10, 15, 20, 25, 30, 35, 40, 45", True)),
    B("Next clue: in 2s, 1 is left over. That means the number is odd. So cross out the even ones.",
      S("l", "10"), S("l", "20"), S("l", "30"), S("l", "40")),
    B("5 numbers are still standing: 5, 15, 25, 35 and 45. Last clue: in 3s, there must be 1 left over.",
      W("l2", "5, 15, 25, 35, 45", True)),
    B("15 and 45 are in the 3 times table, so they leave nothing over. 5 leaves 2 over, and so does 35.",
      W("d1", "15 = 3 × 5"), W("d2", "45 = 3 × 15"), W("d3", "35 = 3 × 11 + 2"),
      S("l2", "15"), S("l2", "45"), S("l2", "35")),
    B("That leaves 25. It is 8 threes, and 1 more. So 1 is left over, just as the clue says.",
      W("d4", "25 = 3 × 8 + 1"), M("l2", "25", "circle")),
    B("Rohan has 25 coins.",
      ANS("a", "Coins = 25", True), RING("a", "25")),
    B("Check all three clues. 25 is 12 twos and 1 more, 8 threes and 1 more, and exactly 5 fives.",
      W("c1", "25 = 2 × 12 + 1"), W("c2", "25 = 5 × 5")),
    B("With several clues, start with the simplest one to make a list. Then let each of the other clues cross numbers off."),
)

# ── Greatest common factor ───────────────────────────────────────────────────

LESSONS[P + "24d92d6d-e0e5-49c9-a5e9-9d4d08e2d87e"] = lesson(
    B("Riya has 84 chocolates, 126 toffees and 42 diyas. Every bag must get the same of each, with nothing left over. What is the greatest number of bags?",
      GIVEN("q", "84 chocolates, 126 toffees, 42 diyas", True), W("q2", "Greatest number of equal bags = ?", True)),
    B("Each pile is shared out equally among the bags. So the number of bags must divide 84, and 126, and 42 exactly."),
    B("We want the greatest number of bags. So what are we looking for?",
      ask=ask("the biggest number that divides all 3", ["the smallest number all 3 go into", "84 + 126 + 42"],
              "The bags share each pile out, so the number of bags has to divide each pile. The most bags means the greatest number that divides all 3.")),
    B("Here is a shortcut. There cannot be more than 42 bags, because there are only 42 diyas. So let's test 42 itself.",
      M("q", "42", "circle")),
    B("Does 42 divide 84? Yes, 2 times. Does it divide 126? Yes, 3 times. And it divides itself once.",
      W("t1", "84 ÷ 42 = 2"), W("t2", "126 ÷ 42 = 3"), W("t3", "42 ÷ 42 = 1")),
    B("So 42 divides all 3 piles, and nothing bigger could. The greatest number of bags is 42.",
      ANS("a", "Greatest number of bags = 42", True), RING("a", "42")),
    B("We can check with prime factors too. 84 is 2 times 2 times 3 times 7. 126 is 2 times 3 times 3 times 7. And 42 is 2 times 3 times 7.",
      W("p1", "84 = 2 × 2 × 3 × 7"), W("p2", "126 = 2 × 3 × 3 × 7"), W("p3", "42 = 2 × 3 × 7")),
    B("What all 3 share is one 2, one 3 and one 7. And 2 times 3 times 7 is 42. It agrees.",
      W("p4", "2 × 3 × 7 = 42")),
    B("Careful: a smaller number like 7 divides all 3 piles too. But the question wants the greatest, so always test the biggest number that could work."),
    B("Each bag gets 2 chocolates, 3 toffees and 1 diya. Sharing several piles into the most equal groups means finding their greatest common factor."),
)

# ── Largest multiple in a range ──────────────────────────────────────────────

LESSONS[P + "3aed085e-2457-485c-b7be-4937c98b5cd5"] = lesson(
    B("N is divisible by both 4 and 9, it lies between 300 and 400, and it is as large as it can be. We want the sum of its digits.",
      GIVEN("q", "N divisible by 4 and 9, between 300 and 400", True), W("q2", "N as large as possible. Sum of digits = ?", True)),
    B("4 and 9 share no factors. So a number that both of them divide must be a multiple of 4 times 9, which is 36.",
      W("m", "4 × 9 = 36")),
    B("So we are hunting for the largest multiple of 36 below 400. Start from an easy one: 36 times 10 is 360.",
      W("t1", "36 × 10 = 360")),
    B("360 is in the range. Can we fit one more 36 in before 400?",
      ask=ask("Yes: 360 + 36 = 396", ["No: 360 is the largest", "Yes: and 432 fits as well"],
              "Add 36 to 360 and you get 396, which is still below 400. Add another 36 and you jump past 400. So 396 is the largest.")),
    B("36 times 11 is 396. The next one, 432, is too big. So N is 396.",
      W("t2", "36 × 11 = 396"), W("t3", "36 × 12 = 432"), S("t3", "432", "past 400"), M("t2", "396", "circle")),
    B("Careful, we are not finished. The question asks for the sum of the digits of N, not for N itself."),
    B("3 plus 9 plus 6 is 18.",
      ANS("a", "3 + 9 + 6 = 18"), RING("a", "18")),
    B("Check N. 396 divided by 4 is 99, and 396 divided by 9 is 44. Both are exact.",
      W("c1", "396 ÷ 4 = 99"), W("c2", "396 ÷ 9 = 44")),
    B("So: join the two divisors into one, find the largest multiple in the range, and then answer what was really asked."),
)

# ── Testing divisors ─────────────────────────────────────────────────────────

LESSONS[P + "5555e2f5-13bc-427e-8342-f376e3c717f6"] = lesson(
    B("Riya has 2023 diyas. She tries rows of 7, rows of 11 and rows of 17. How many of those row sizes leave no diyas over?",
      GIVEN("q", "2023 diyas: rows of 7, 11 or 17?", True)),
    B("A row size works only if it divides 2023 exactly. So we test each one. Start with 7, and here is a neat way: 2023 is 2100 minus 77.",
      W("a1", "2023 = 2100 − 77")),
    B("7 goes into 2100 exactly 300 times, and into 77 exactly 11 times. So 7 goes into 2023 exactly: 300 minus 11, which is 289 times.",
      W("a2", "2023 ÷ 7 = 300 − 11 = 289"), N("a2", "289", "exact, so 7 works")),
    B("Now 11. There is a quick test: take the digits in turn, subtracting and adding. For 2023 that is 2 minus 0 plus 2 minus 3. What do we get?",
      W("b1", "2 − 0 + 2 − 3 = ?"),
      ask=ask("1", ["7", "0"],
              "Go one digit at a time. 2 minus 0 is 2, plus 2 is 4, minus 3 is 1.")),
    B("11 divides a number only when that test gives 0 or a multiple of 11. We got 1, so 11 does not work. Rows of 11 would leave 10 diyas over.",
      W("b2", "2 − 0 + 2 − 3 = 1"), W("b3", "2023 = 11 × 183 + 10")),
    B("Last, 17. We found that 2023 is 7 times 289. And 289 is 17 times 17. So 17 goes in exactly too: 119 times.",
      W("c1", "289 = 17 × 17"), W("c2", "2023 ÷ 17 = 119")),
    B("Careful: the question does not ask which row sizes work. It asks how many of them work."),
    B("7 works, 11 does not, and 17 works. That is 2 of the 3 row sizes.",
      W("s", "7 yes, 11 no, 17 yes", True), ANS("a", "Row sizes that work = 2", True), RING("a", "2")),
    B("Check by multiplying back: 7 times 17 times 17 is 2023.",
      W("k", "7 × 17 × 17 = 2023")),
    B("To test a divisor, divide, or use a quick rule if you know one. Then read the question again to see what it really wants."),
)

LESSONS[P + "adc40db0-b11c-4d90-a8e8-c4fc49d77d32"] = lesson(
    B("Riya shares 84 chocolates equally among her friends, with none left over. One of these numbers of friends is impossible. Which?",
      GIVEN("q", "84 chocolates shared equally, none left over", True), W("q2", "Friends: 6, 12, 14 or 16?", True)),
    B("Equal shares with none left over means the number of friends divides 84 exactly. We are hunting for the one that does not. So we test each choice."),
    B("84 divided by 6 is 14. Exact, so 6 friends is possible. And the same fact tells us 14 works too: 84 divided by 14 is 6.",
      W("t1", "84 ÷ 6 = 14"), W("t2", "84 ÷ 14 = 6")),
    B("84 divided by 12 is 7. Exact again.",
      W("t3", "84 ÷ 12 = 7")),
    B("Now 16. If each of 16 friends takes 5 chocolates, that uses 80. What happens to the last 4 chocolates?",
      W("t4", "16 × 5 = 80"),
      ask=ask("they are left over", ["they make one more share", "they do not matter"],
              "Each friend has 5, and that uses 80 of the 84. Only 4 remain, far too few to give another one to all 16 friends. So they are left over.")),
    B("84 is 16 times 5, with 4 left over. So 16 does not divide 84.",
      W("t5", "84 = 16 × 5 + 4"), N("t5", "+ 4", "left over")),
    B("The number of friends cannot be 16.",
      ANS("a", "Cannot be: 16", True), RING("a", "16"), S("q2", "16")),
    B("A quick check: 84 is 4 times 21. Now 16 is 4 times 4, and 4 does not go into 21. So 16 cannot go into 84.",
      W("c", "84 = 4 × 21")),
    B("Careful with the word cannot: we wanted the one that does not fit. Test each choice by dividing, and look for a remainder."),
)

# ── Counting factors ─────────────────────────────────────────────────────────

LESSONS[P + "79b0b1e1-ff48-47a9-89ee-a7852e714922"] = lesson(
    B("Arjun has 180 players to put into equal teams, with nobody left out. Each team must have more than 10 but fewer than 25 players. How many team sizes are possible?",
      GIVEN("q", "180 players in equal teams", True), W("q2", "Team size: more than 10, fewer than 25", True)),
    B("Equal teams with nobody left out means the team size divides 180 exactly. It must be a factor of 180."),
    B("Factors come in pairs that multiply to 180. Start from 1 and work up: 1 times 180, 2 times 90, 3 times 60, and on, until the pairs meet at 12 times 15.",
      W("p1", "180 = 1 × 180 = 2 × 90 = 3 × 60"), W("p2", "180 = 4 × 45 = 5 × 36 = 6 × 30"),
      W("p3", "180 = 9 × 20 = 10 × 18 = 12 × 15")),
    B("The team size must be more than 10 and fewer than 25. Does 10 itself count?",
      ask=ask("No: more than 10 starts at 11", ["Yes: 10 is allowed"],
              "More than 10 means bigger than 10. So 10 itself is left out, and so is 25 at the other end.")),
    B("Now pick out the factors that lie between 10 and 25. They are 12, 15, 18 and 20.",
      M("p3", "20", "circle"), M("p3", "18", "circle", 2), M("p3", "12", "circle"), M("p3", "15", "circle")),
    B("The next factor up is 30, which is too big. And 9 and 10 are too small."),
    B("So there are 4 possible team sizes.",
      W("l", "12, 15, 18, 20", True), ANS("a", "Team sizes = 4", True), RING("a", "4")),
    B("Check a couple. Teams of 18 make 10 teams, because 10 times 18 is 180. And teams of 15 make 12 teams.",
      M("p3", "10 × 18"), M("p3", "12 × 15")),
    B("Careful: the answer is how many sizes there are, not one of the sizes. List the factor pairs in order so that none is missed, then count the ones in range."),
)

LESSONS[P + "7ba06750-8e75-483a-9e5b-cc7627c95f09"] = lesson(
    B("Strip the story away, and this question asks one thing: how many factors does 60 have? Each factor is one possible team size.",
      GIVEN("q", "How many factors does 60 have?", True)),
    B("Factors come in pairs that multiply to 60. If we go up in order, we will not miss any."),
    B("1 times 60. 2 times 30. 3 times 20.",
      W("p1", "1 × 60 = 60"), W("p2", "2 × 30 = 60"), W("p3", "3 × 20 = 60")),
    B("4 times 15. 5 times 12. 6 times 10.",
      W("p4", "4 × 15 = 60"), W("p5", "5 × 12 = 60"), W("p6", "6 × 10 = 60")),
    B("After 6 comes 7, 8 and 9. How far do we need to keep testing?",
      ask=ask("test 7, 8 and 9, then stop at 10", ["keep going all the way to 60", "stop now, without testing them"],
              "7, 8 and 9 still need a look. But 10 is already in our list, as the partner of 6. Once we reach a number we already have, every pair has been found.")),
    B("7, 8 and 9 do not divide 60. And 10 is already on the board, so the pairs have met. We are done.",
      M("p6", "10", "circle")),
    B("6 pairs, with 2 factors in each. 6 times 2 is 12 factors.",
      ANS("a", "6 × 2 = 12"), RING("a", "12")),
    B("Here they are in order: 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60. Count them, and there are 12.",
      W("l", "1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60", True)),
    B("Careful not to forget 1 and 60 itself: they are factors too. Work up in pairs, and stop when the pairs meet."),
)

LESSONS[P + "905c1d7b-ed53-42fa-bd43-f2c424c5c743"] = lesson(
    B("How many factors does 72 have? A factor is a number that divides 72 exactly, like a number of samosas on each plate with none left over.",
      GIVEN("q", "How many factors does 72 have?", True)),
    B("Factors come with a partner. 1 goes with 72. And 2 goes with 36, because 2 times 36 is 72.",
      W("p1", "1 × 72 = 72"), W("p2", "2 × 36 = 72")),
    B("Carry on in order. 3 times 24 is 72. 4 times 18 is 72.",
      W("p3", "3 × 24 = 72"), W("p4", "4 × 18 = 72")),
    B("Next is 5. Is 5 a factor of 72?",
      ask=ask("No: 72 does not end in 0 or 5", ["Yes: 72 is a big number", "Yes: 72 is even"],
              "Multiples of 5 always end in 0 or 5. 72 ends in 2, so 5 is not a factor, and we skip it.")),
    B("6 times 12 is 72. 7 does not go in. 8 times 9 is 72. After 8 comes 9, which we already have, so the pairs have met.",
      W("p6", "6 × 12 = 72"), W("p8", "8 × 9 = 72")),
    B("Count the pairs: there are 6, with 2 factors in each. 6 times 2 is 12 factors.",
      ANS("a", "6 × 2 = 12"), RING("a", "12")),
    B("In order they are 1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36 and 72. That is 12.",
      W("l", "1, 2, 3, 4, 6, 8, 9, 12, 18, 24, 36, 72", True)),
    B("Go up in order, give each factor its partner, and stop when the pairs meet. And don't leave out 1 or the number itself."),
)

# ── Prime factors ────────────────────────────────────────────────────────────

LESSONS[P + "9630683a-6cce-40b5-a39e-d887f856b868"] = lesson(
    B("Riya lists the factors of 720 that are prime numbers, and adds them up. What total does she get?",
      GIVEN("q", "Prime factors of 720, added together", True)),
    B("To find the prime factors, we break 720 down until only prime numbers are left. 720 is 72 times 10. That is a friendly start.",
      W("s1", "720 = 72 × 10")),
    B("10 is 2 times 5. And 72 is 8 times 9.",
      W("s2", "10 = 2 × 5"), W("s3", "72 = 8 × 9")),
    B("8 is 2 times 2 times 2, and 9 is 3 times 3. Now every piece is prime.",
      W("s4", "8 = 2 × 2 × 2"), W("s5", "9 = 3 × 3"), W("s6", "720 = 2 × 2 × 2 × 2 × 3 × 3 × 5")),
    B("Riya writes each prime factor once in her list. Which list is hers?",
      ask=ask("2, 3 and 5", ["2, 2, 2, 2, 3, 3 and 5", "1, 2, 3 and 5"],
              "A list of factors names each number once, however many times it is used. And 1 is not a prime number. So her list is 2, 3 and 5.")),
    B("2 plus 3 plus 5 is 10.",
      M("s6", "2 × 2 × 2 × 2"), M("s6", "3 × 3"), M("s6", "5"), ANS("a", "2 + 3 + 5 = 10"), RING("a", "10")),
    B("Check that each one really divides 720. It is even, so 2 works. It ends in 0, so 5 works. And its digits add to 9, so 3 works.",
      W("c", "7 + 2 + 0 = 9")),
    B("Careful not to add every 2 and every 3 in the long line. Break the number into primes, then count each prime once."),
)
