"""Hand-written lessons, part 5: the chapter questions Q_CH06_002 to 025 and Q_CH16_012."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_factors_lib import (  # noqa: E402
    ANS, ANSM, B, CIRC, FIG, GIVEN, LB, LESSON, Q, STRIKE, TREE, W,
)

LESSONS = {}

LESSONS["Q_CH06_002"] = LESSON(
    B("Which of these is a prime number? A prime has exactly two factors: 1 and itself. So we look for factors, and cross out any number that has more.",
      GIVEN("q", "Which is prime?  29, 35, 21, 15")),
    B("35 and 15 both end in 5, so 5 divides them. 35 is 5 times 7, and 15 is 3 times 5. Neither is prime.",
      W("a", "35 = 5 × 7"), W("b", "15 = 3 × 5"), STRIKE("q", "35"), STRIKE("q", "15")),
    Q("Now 21. Is 21 in the 3 times table?", ["Yes, 3 × 7 = 21", "No, it is not"], 0,
      "3 times 7 is 21. So 21 has factors other than 1 and itself."),
    B("21 is 3 times 7, so it is not prime either.", W("c", "21 = 3 × 7"), STRIKE("q", "21")),
    B("That leaves 29. It is odd. Its digits add up to 11, so 3 does not divide it. It does not end in 0 or 5. And 7 times 4 is 28, which just misses it.",
      W("d", "2 + 9 = 11"), W("e", "7 × 4 = 28")),
    B("Nothing divides 29 except 1 and 29. So 29 is the prime number.", ANS("ans", "29 is prime"), CIRC("ans", "29")),
    B("So to test for a prime, try the small primes 2, 3, 5 and 7. If none of them goes in, a number this size is prime."),
)

LESSONS["Q_CH06_003"] = LESSON(
    B("Which of these four numbers can be divided exactly by 3? There is a quick test, so we will not need long division.",
      GIVEN("q", "Divisible by 3?  7,251  5,123  4,532  8,206")),
    B("The test for 3: add up the digits. If the total is in the 3 times table, then 3 divides the number.",
      LB("r", "Test for 3: add the digits")),
    B("5,123 gives 11. 4,532 gives 14. 8,206 gives 16. None of those totals is in the 3 times table.",
      W("a", "5 + 1 + 2 + 3 = 11"), W("b", "4 + 5 + 3 + 2 = 14"), W("c", "8 + 2 + 0 + 6 = 16"),
      STRIKE("q", "5,123"), STRIKE("q", "4,532"), STRIKE("q", "8,206")),
    Q("Now 7,251. What do its digits add up to?", ["15", "14", "16"], 0,
      "Add them one at a time: 7, then 2, then 5, then 1. You reach 15."),
    B("The digits add up to 15, and 15 divided by 3 is 5, with nothing left over. So 7,251 is divisible by 3.",
      W("d", "7 + 2 + 5 + 1 = 15"), W("e", "15 ÷ 3 = 5"), ANS("ans", "7,251 is divisible by 3"), CIRC("ans", "7,251")),
    B("Let's check that the test told the truth. 3 times 2,417 is 7,251. It did!", W("f", "3 × 2,417 = 7,251")),
    B("So for 3, never mind how big the number is. Just add its digits and test the total."),
)

LESSONS["Q_CH06_004"] = LESSON(
    B("Which of these four numbers can be divided exactly by 4? Again there is a quick test.",
      GIVEN("q", "Divisible by 4?  2,316  5,634  7,531  3,718")),
    B("The test for 4: look only at the last two digits. If they make a number in the 4 times table, then 4 divides the whole number.",
      LB("r", "Test for 4: look at the last two digits")),
    B("7,531 is odd, so it is out at once. 5,634 ends in 34. But 4 times 8 is 32 and 4 times 9 is 36, so 4 skips 34.",
      STRIKE("q", "7,531", "odd"), LB("a0", "5,634 ends in 34"), W("a", "4 × 8 = 32"), W("b", "4 × 9 = 36"), STRIKE("q", "5,634")),
    B("3,718 ends in 18. 4 times 4 is 16 and 4 times 5 is 20, so 4 skips 18 as well.",
      LB("c0", "3,718 ends in 18"), W("c", "4 × 4 = 16"), W("d", "4 × 5 = 20"), STRIKE("q", "3,718")),
    Q("That leaves 2,316. Its last two digits make 16. Is 16 in the 4 times table?", ["Yes, 4 × 4 = 16", "No, it is not"], 0,
      "4 times 4 is 16. So the last two digits pass the test."),
    B("16 divided by 4 is 4, with nothing left over. So 2,316 is divisible by 4.",
      W("e", "16 ÷ 4 = 4"), ANS("ans", "2,316 is divisible by 4"), CIRC("ans", "2,316")),
    B("Here is the trap. 5,634 and 3,718 are even, but being even is not enough for 4. Always test the last two digits."),
)

LESSONS["Q_CH06_007"] = LESSON(
    B("We must write 60 as a product of prime numbers only. That is called its prime factorization.",
      GIVEN("q", "Prime factorization of 60 = ?"), TREE("f", 60)),
    B("Start with the smallest prime, 2. 60 is even, and 60 is 2 times 30.", W("a", "60 = 2 × 30")),
    Q("30 is not prime, so we split it again. 30 is 2 times what?", ["15", "10", "28"], 0,
      "Half of 30 is 15. So 30 is 2 times 15."),
    B("30 is 2 times 15. And 15 is not prime either: it is 3 times 5.", W("b", "60 = 2 × 2 × 15"), W("c", "15 = 3 × 5")),
    B("Now every piece is prime: 2, 2, 3 and 5. So 60 is 2 times 2 times 3 times 5.",
      ANSM("ans", "60 = 2 × 2 × 3 × 5"), CIRC("ans", "2 × 2 × 3 × 5")),
    B("Watch the traps. 2 times 3 times 10 does make 60, and so does 4 times 15. But 10, 4 and 15 are not prime.",
      W("t1", "10 = 2 × 5"), W("t2", "4 = 2 × 2")),
    B("So keep splitting until every number is prime. If any piece can still be split, you are not finished."),
)

LESSONS["Q_CH06_008"] = LESSON(
    B("If a number can be divided by 6, which two numbers must also divide it, every time?",
      GIVEN("q", "A number divisible by 6 must be divisible by ... ?")),
    Q("Start with 6 itself. Which two numbers, other than 1 and 6, multiply to make 6?", ["2 and 3", "2 and 4", "3 and 4"], 0,
      "2 times 3 is 6. The other pairs multiply to make numbers bigger than 6."),
    B("6 is 2 times 3. So every multiple of 6 is built from a 2 and a 3. That means 2 divides it, and 3 divides it.",
      W("a", "6 = 2 × 3")),
    B("Let's test with 18, which is 6 times 3. 18 divided by 2 is 9. 18 divided by 3 is 6. Both are exact.",
      W("b", "18 = 6 × 3"), W("c", "18 ÷ 2 = 9"), W("d", "18 ÷ 3 = 6")),
    B("Why not 4? Try 6 itself. 4 goes into 6 once, with 2 left over. So 4 does not always work.",
      LB("t", "6 ÷ 4 leaves 2 over")),
    B("So a number divisible by 6 must be divisible by 2 and 3.", ANS("ans", "2 and 3"), CIRC("ans", "2 and 3")),
    B("This works backwards too. To test for 6, test for 2 and for 3. If both pass, 6 divides the number."),
)

LESSONS["Q_CH06_009"] = LESSON(
    B("Which pair of numbers is co-prime? Two numbers are co-prime when the only factor they share is 1.",
      GIVEN("q", "Which pair is co-prime?"), LB("o", "8 and 12,  15 and 35,  9 and 16,  6 and 9")),
    B("So we look for a shared factor in each pair. If we find one bigger than 1, that pair is out."),
    B("8 and 12 are both even, and 4 divides both of them. 15 and 35 both end in 5, so 5 divides both. Those two pairs are out.",
      LB("a", "8 and 12 share 4"), LB("b", "15 and 35 share 5")),
    Q("Now 6 and 9. Which number divides both of them?", ["3", "2", "6"], 0,
      "6 is 3 times 2, and 9 is 3 times 3. So 3 divides both."),
    B("6 and 9 share 3, so they are out as well.", LB("c", "6 and 9 share 3")),
    B("That leaves 9 and 16. The factors of 9 are 1, 3 and 9. The factors of 16 are 1, 2, 4, 8 and 16. The only number in both lists is 1.",
      LB("d", "Factors of 9: 1, 3, 9"), LB("e", "Factors of 16: 1, 2, 4, 8, 16"),
      ANS("ans", "9 and 16 are co-prime"), CIRC("ans", "9 and 16")),
    B("Notice something. Neither 9 nor 16 is a prime number. Co-prime is about the pair: it means they share nothing but 1."),
)

LESSONS["Q_CH06_010"] = LESSON(
    B("Is 4,518 divisible by 9? We can find out without dividing.", GIVEN("q", "Is 4,518 divisible by 9?")),
    B("The test for 9: add up the digits. If the total is in the 9 times table, then 9 divides the number.",
      LB("r", "Test for 9: add the digits")),
    Q("So add the digits of 4,518. What is 4 plus 5 plus 1 plus 8?", ["18", "17", "9"], 0,
      "Add them one at a time: 4, then 5, then 1, then 8. You reach 18."),
    B("The digit sum is 18.", W("a", "4 + 5 + 1 + 8 = 18")),
    B("And 18 is 9 times 2, so it is in the 9 times table. Yes, 4,518 is divisible by 9.",
      W("b", "18 = 9 × 2"), ANS("ans", "Yes, digit sum = 18"), CIRC("ans", "Yes")),
    B("Let's check that the test told the truth. 9 times 502 is 4,518. It did!", W("c", "9 × 502 = 4,518")),
    B("One thing to notice. The digit sum does not have to be 9 itself. Any number in the 9 times table will do, and 18 is one."),
)

LESSONS["Q_CH06_011"] = LESSON(
    B("What is the smallest composite number? A composite number has more than two factors.",
      GIVEN("q", "Smallest composite number = ?"), LB("o", "9, 2, 1 or 4")),
    B("We want the smallest, so start from the bottom and count factors. 1 has just one factor. It is not prime, and it is not composite.",
      LB("a", "1: one factor only")),
    B("2 has two factors, 1 and 2. 3 has two factors, 1 and 3. Exactly two factors means they are prime, not composite.",
      LB("b", "2: 1, 2 (prime)"), LB("c", "3: 1, 3 (prime)")),
    Q("Now 4. How many factors does 4 have?", ["3", "2", "4"], 0,
      "1 times 4 is 4, and 2 times 2 is 4. So the factors are 1, 2 and 4. That is 3 factors."),
    B("4 has three factors: 1, 2 and 4. That is more than two, so 4 is composite. And it is the first one we met.",
      W("e", "2 × 2 = 4"), LB("d", "4: 1, 2, 4 (composite)"), ANS("ans", "4"), CIRC("ans", "4")),
    B("9 is composite too, because 3 times 3 is 9. But it is not the smallest.", W("f", "3 × 3 = 9")),
    B("So the order at the start is: 1 is neither, 2 and 3 are prime, and 4 is the smallest composite number."),
)

LESSONS["Q_CH06_012"] = LESSON(
    B("Is 8,294 divisible by 11? There is a neat test for 11 that uses the digits.",
      GIVEN("q", "Is 8,294 divisible by 11?")),
    B("Here is the test. Add the 1st and 3rd digits. Then add the 2nd and 4th digits. If the two sums are equal, or differ by 11, then 11 divides the number.",
      LB("r", "Test for 11: two sums equal, or differ by 11")),
    B("The 1st and 3rd digits are 8 and 9. They add up to 17.", W("a", "8 + 9 = 17")),
    B("The 2nd and 4th digits are 2 and 4. They add up to 6.", W("b", "2 + 4 = 6")),
    Q("How far apart are the two sums, 17 and 6?", ["11", "23", "6"], 0,
      "Take the smaller sum from the bigger one. 17 take away 6 is 11."),
    B("17 minus 6 is 11. The sums differ by exactly 11, so yes, 8,294 is divisible by 11.",
      W("c", "17 − 6 = 11"), ANS("ans", "Yes"), CIRC("ans", "Yes")),
    B("Let's check that the test told the truth. 11 times 754 is 8,294. It did!", W("d", "11 × 754 = 8,294")),
    B("So for 11: add every other digit, and compare the two sums. Equal, or 11 apart, means yes."),
)

LESSONS["Q_CH06_013"] = LESSON(
    B("One bell rings every 12 minutes, and another every 18 minutes. They ring together at 9 o'clock. When do they next ring together?",
      GIVEN("q", "Bells ring every 12 and 18 minutes. Together at 9:00."), LB("q2", "Together again at = ?")),
    B("Each bell rings at the multiples of its own number. They ring together at a common multiple, and the next time is the lowest one: the L C M."),
    B("The first bell rings after 12, 24, 36 and 48 minutes. The second rings after 18, 36 and 54 minutes.",
      LB("la", "Multiples of 12: 12, 24, 36, 48"), LB("lb", "Multiples of 18: 18, 36, 54")),
    Q("What is the first number in both lists?", ["36", "18", "30"], 0,
      "Run a finger along both lists. 36 is in both, and nothing before it is."),
    B("36 is the first number in both lists. So the L C M is 36, and the bells ring together after 36 minutes.",
      CIRC("la", "36"), CIRC("lb", "36"), LB("l", "LCM = 36")),
    B("36 minutes after 9 o'clock is 36 minutes past 9.", ANS("ans", "9:36 AM"), CIRC("ans", "9:36 AM")),
    B("Two traps. At 18 minutes past, only the second bell rings. And 30 is 12 plus 18, but it is in neither table, so no bell rings then."),
)

LESSONS["Q_CH06_014"] = LESSON(
    B("48 apples and 36 oranges go into boxes. Every box holds the same number of fruits, all of one kind. What is the most each box can hold?",
      GIVEN("q", "48 apples, 36 oranges. Same number in each box."), LB("q2", "Most fruits in a box = ?"),
      FIG("f", {"kind": "barModel", "bars": [
          {"label": "Apples", "segments": [{"units": 12.0, "label": "48", "tone": "a"}]},
          {"label": "Oranges", "segments": [{"units": 9.0, "label": "36", "tone": "b"}]}],
          "note": "Same number in every box, as many as possible."})),
    Q("The number in a box must divide 48 exactly, and 36 exactly. We want the biggest such number. What is that?",
      ["The HCF of 48 and 36", "The LCM of 48 and 36", "48 − 36"], 0,
      "A number that divides both exactly is a common factor. The biggest one is the highest common factor."),
    B("So we want the H C F. Here are the factors of 36. We test them on 48, starting from the big end.",
      LB("la", "Factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36")),
    B("36 does not divide 48. 18 does not: 18 times 2 is 36 and 18 times 3 is 54, so it skips 48.",
      W("a", "18 × 2 = 36"), W("b", "18 × 3 = 54"), STRIKE("la", "36", None, 2), STRIKE("la", "18")),
    Q("Next is 12. Does 12 divide 48 exactly?", ["Yes, 12 × 4 = 48", "No, it does not"], 0,
      "12 times 4 is 48. So 12 divides 48 exactly."),
    B("48 divided by 12 is 4, and 36 divided by 12 is 3. So each box holds 12 fruits: 4 boxes of apples, and 3 boxes of oranges.",
      W("c", "48 ÷ 12 = 4"), W("d", "36 ÷ 12 = 3"), CIRC("la", "12"), ANS("ans", "12 fruits"), CIRC("ans", "12 fruits")),
    B("Watch the traps. 24 divides 48, but it does not divide 36. And 6 and 4 divide both, but they are not the biggest.",
      W("t", "24 × 2 = 48")),
)

LESSONS["Q_CH06_015"] = LESSON(
    B("Which of these is a pair of twin primes? Twin primes are two prime numbers that are exactly 2 apart, like 3 and 5.",
      GIVEN("q", "Which pair is twin primes?"), LB("o", "13 & 17,  3 & 7,  11 & 13,  7 & 13")),
    B("Every number in these pairs is prime. So the only thing to test is the gap. Subtract the smaller from the bigger."),
    B("17 minus 13 is 4. 7 minus 3 is 4. 13 minus 7 is 6. None of those gaps is 2.",
      W("a", "17 − 13 = 4"), W("b", "7 − 3 = 4"), W("c", "13 − 7 = 6")),
    Q("Now the pair 11 and 13. What is the gap between them?", ["2", "4", "3"], 0,
      "Count on from 11 to 13. That is 2 steps."),
    B("13 minus 11 is 2. Both are prime, and they are 2 apart. So 11 and 13 are twin primes.",
      W("d", "13 − 11 = 2"), ANS("ans", "11 and 13"), CIRC("ans", "11 and 13")),
    B("The trap is thinking any two primes are twins. They must be exactly 2 apart, with just one number between them."),
)

LESSONS["Q_CH06_016"] = LESSON(
    B("Which of these four numbers can be divided exactly by 8? There is a test for 8 too.",
      GIVEN("q", "Divisible by 8?  3,214  7,234  5,648  9,342")),
    B("The test for 8: look only at the last three digits. If 8 divides the number they make, then 8 divides the whole number.",
      LB("r", "Test for 8: look at the last three digits")),
    B("3,214 ends in 214. 8 times 26 is 208, so 6 is left over. 7,234 ends in 234. 8 times 29 is 232, so 2 is left over.",
      W("a0", "8 × 26 = 208"), W("a", "214 = 208 + 6"), W("b0", "8 × 29 = 232"), W("b", "234 = 232 + 2"),
      STRIKE("q", "3,214"), STRIKE("q", "7,234")),
    B("9,342 ends in 342. 8 times 42 is 336, so 6 is left over. That one is out as well.",
      W("c0", "8 × 42 = 336"), W("c", "342 = 336 + 6"), STRIKE("q", "9,342")),
    Q("Now 5,648, which ends in 648. 8 times 80 is 640, and that leaves 8. Does 8 go into what is left exactly?",
      ["Yes, 8 × 1 = 8", "No, some is left over"], 0,
      "8 times 1 is 8. So after 640 there is exactly one more 8, with nothing left over.",
      W("e0", "8 × 80 = 640"), W("e", "648 = 640 + 8")),
    B("80 eights and 1 more eight make 81 eights. So 648 divided by 8 is 81, and 5,648 is divisible by 8.",
      W("f", "648 ÷ 8 = 81"), ANS("ans", "5,648 is divisible by 8"), CIRC("ans", "5,648")),
    B("So for 8, cover up everything except the last three digits, and divide just those."),
)

LESSONS["Q_CH06_017"] = LESSON(
    B("A number has exactly 2 factors. What kind of number must it be?",
      GIVEN("q", "A number has exactly 2 factors. It must be ... ?"), LB("o", "composite, 1, even or prime")),
    B("Every number bigger than 1 has at least two factors: 1, and the number itself. Exactly 2 factors means nothing else divides it."),
    B("Take 5. Only 1 times 5 makes it. So its factors are just 1 and 5.", LB("a", "5: 1, 5")),
    Q("What do we call a number whose only factors are 1 and itself?", ["prime", "composite", "even"], 0,
      "A number with only 1 and itself as factors is called a prime number."),
    B("It is called a prime number. So a number with exactly 2 factors must be prime.", ANS("ans", "prime"), CIRC("ans", "prime")),
    B("Look at the other choices. A composite number has more than 2 factors: 6 has four. The number 1 has only one factor. And an even number like 4 has three.",
      LB("b", "6: 1, 2, 3, 6"), LB("c", "1: just 1"), LB("d", "4: 1, 2, 4")),
    B("So remember: exactly two factors, 1 and itself, is what prime means."),
)

LESSONS["Q_CH06_018"] = LESSON(
    B("6 is called a perfect number. Why? The secret is in its factors.", GIVEN("q", "Why is 6 called a perfect number?")),
    B("List the factors of 6. 1 times 6, and 2 times 3. So the factors are 1, 2, 3 and 6.",
      LB("a", "Factors of 6: 1, 2, 3, 6")),
    B("Now leave out 6 itself. The factors that are left are 1, 2 and 3.", STRIKE("a", "6", "leave out", 2)),
    Q("Add up the factors that are left. What is 1 plus 2 plus 3?", ["6", "5", "7"], 0,
      "1 plus 2 is 3. And 3 plus 3 more is 6."),
    B("1 plus 2 plus 3 is 6. The smaller factors add up to the number itself! That is what makes 6 a perfect number.",
      ANSM("ans", "1 + 2 + 3 = 6"), CIRC("ans", "6")),
    B("It is not about having four factors. 8 has four factors as well, but 1 plus 2 plus 4 is only 7, not 8. So 8 is not perfect.",
      LB("b", "Factors of 8: 1, 2, 4, 8"), W("c", "1 + 2 + 4 = 7")),
    B("So a perfect number equals the sum of its factors, leaving out the number itself. They are very rare!"),
)

LESSONS["Q_CH06_019"] = LESSON(
    B("How can we tell that 5 divides a number, just by looking at its last digit?",
      GIVEN("q", "Divisible by 5: the last digit is ... ?")),
    B("Let's look at the 5 times table itself: 5, 10, 15, 20, 25, 30.", LB("m", "5, 10, 15, 20, 25, 30")),
    Q("Read only the last digit of each number. What pattern do you see?", ["5, 0, 5, 0, ...", "always 5", "always even"], 0,
      "Read just the last digit of each number in the list: 5, 0, 5, 0, 5, 0."),
    B("The last digits go 5, 0, 5, 0, again and again. They are never anything else.", LB("p", "Last digits: 5, 0, 5, 0, 5, 0")),
    B("So a number is divisible by 5 when its last digit is 0 or 5.", ANS("ans", "Last digit: 0 or 5"), CIRC("ans", "0 or 5")),
    B("Watch the traps. Saying 0 only would miss 15 and 25. Saying 5 only would miss 10 and 20. We need both."),
    B("And an even last digit is not the rule. 8 is even, but 5 does not divide 8."),
)

M4 = [4, 8, 12, 16, 20, 24, 28, 32, 36]
M6 = [6, 12, 18, 24, 30, 36]


def _circle(line, prefix, nums, value):
    from g4_gr4_factors_lib import mark_in
    return mark_in(line, prefix, nums, value)


LESSONS["Q_CH06_020"] = LESSON(
    B("We need the first three common multiples of 4 and 6: the first three numbers that are in both times tables.",
      GIVEN("q", "First three common multiples of 4 and 6 = ?")),
    B("Count up in 4s: 4, 8, 12, 16, 20, 24, 28, 32, 36.", LB("la", "Multiples of 4: 4, 8, 12, 16, 20, 24, 28, 32, 36")),
    B("Now count up in 6s: 6, 12, 18, 24, 30, 36.", LB("lb", "Multiples of 6: 6, 12, 18, 24, 30, 36")),
    Q("What is the first number that is in both lists?", ["12", "24", "6"], 0,
      "6 is not in the 4 times table. 12 is the first number that is in both lists."),
    B("12 is in both. Keep looking along the lists: 24 is in both, and so is 36. Ring them.",
      _circle("la", "Multiples of 4: ", M4, 12), _circle("la", "Multiples of 4: ", M4, 24), _circle("la", "Multiples of 4: ", M4, 36),
      _circle("lb", "Multiples of 6: ", M6, 12), _circle("lb", "Multiples of 6: ", M6, 24), _circle("lb", "Multiples of 6: ", M6, 36)),
    B("So the first three common multiples are 12, 24 and 36. Did you notice? They are the 12 times table.",
      ANS("ans", "12, 24, 36"), CIRC("ans", "12, 24, 36")),
    B("One trap: 18 is in the 6 times table, but not in the 4 times table. A common multiple must be in both."),
)

LESSONS["Q_CH06_022"] = LESSON(
    B("Which of these four numbers can be divided exactly by 10?", GIVEN("q", "Divisible by 10?  7,105  8,901  4,055  3,200")),
    B("Think of the 10 times table: 10, 20, 30, 40. Every number in it ends in 0. That is the whole test.",
      LB("m", "10, 20, 30, 40, ...")),
    B("7,105 ends in 5. 8,901 ends in 1. 4,055 ends in 5. None of them ends in 0, so they are out.",
      STRIKE("q", "7,105"), STRIKE("q", "8,901"), STRIKE("q", "4,055")),
    Q("Which number ends in 0?", ["3,200", "7,105", "8,901"], 0,
      "Look only at the very last digit. 3,200 is the one that ends in 0."),
    B("3,200 ends in 0, so it is divisible by 10. In fact 3,200 divided by 10 is 320.",
      W("a", "3,200 ÷ 10 = 320"), ANS("ans", "3,200 is divisible by 10"), CIRC("ans", "3,200")),
    B("Here is the trap. The other three numbers have a 0 in the middle. That does not count. Only the last digit matters."),
)

LESSONS["Q_CH06_023"] = LESSON(
    B("How many prime numbers are there between 10 and 20? Let's write out the numbers in between, and cross out the ones that are not prime.",
      GIVEN("q", "How many primes are there between 10 and 20?"), LB("l", "11, 12, 13, 14, 15, 16, 17, 18, 19")),
    B("The even numbers can all be divided by 2, so they are not prime. Cross out 12, 14, 16 and 18.",
      STRIKE("l", "12"), STRIKE("l", "14"), STRIKE("l", "16"), STRIKE("l", "18")),
    Q("The odd ones are left: 11, 13, 15, 17 and 19. Which of these is not prime?", ["15", "13", "17"], 0,
      "15 ends in 5, so 5 divides it. 3 times 5 is 15."),
    B("15 is 3 times 5, so it is not prime. Cross it out.", W("a", "15 = 3 × 5"), STRIKE("l", "15")),
    B("11, 13, 17 and 19 are left. None of them is in the 3 times table, and none ends in 5. They are all prime."),
    B("Count them: 11, 13, 17, 19. There are 4 prime numbers between 10 and 20.",
      ANS("ans", "4 primes: 11, 13, 17, 19"), CIRC("ans", "4 primes")),
    B("The trap is 15. It is odd, so it can look prime. Always test odd numbers for 3 and for 5."),
)

LESSONS["Q_CH06_024"] = LESSON(
    B("There is only one even number that is prime. Which one is it?",
      GIVEN("q", "The only even prime number = ?"), LB("o", "6, 4, 2 or 0")),
    B("A prime number has exactly two factors: 1 and itself. So let's count the factors of the even numbers."),
    B("Start with 2. Only 1 times 2 makes it. Its factors are 1 and 2. Exactly two, so 2 is prime.", LB("a", "2: 1, 2")),
    Q("Now 4. What are the factors of 4?", ["1, 2 and 4", "1 and 4", "2 and 4"], 0,
      "1 times 4 is 4, and 2 times 2 is 4. So the factors are 1, 2 and 4."),
    B("4 has three factors, which is too many for a prime. 6 has four: 1, 2, 3 and 6.",
      LB("b", "4: 1, 2, 4"), LB("c", "6: 1, 2, 3, 6")),
    B("Here is why. Every even number bigger than 2 can be divided by 2, as well as by 1 and itself. That is at least three factors. So 2 is the only even prime.",
      ANS("ans", "2"), CIRC("ans", "2")),
    B("And 0 is not a prime number at all. The primes start from 2."),
)

LESSONS["Q_CH06_025"] = LESSON(
    B("The Sieve of Eratosthenes is a way of sifting numbers. Up to 50, we cross out the multiples of 2, 3, 5 and 7. What kind of numbers are left?",
      GIVEN("q", "Sieve up to 50: cross out multiples of 2, 3, 5, 7."), LB("q2", "What kind of numbers are left?")),
    B("In the sieve, 1 is crossed out at the very start. We keep 2, 3, 5 and 7 themselves, and cross out all their other multiples."),
    B("A composite number is made by multiplying smaller numbers. Up to 50, one of those smaller numbers must be 2, 3, 5 or 7."),
    B("Why? 7 times 7 is 49, nearly 50. The next prime is 11, and 11 times 11 is 121, far past 50. So nothing up to 50 can be built from bigger primes alone.",
      W("a", "7 × 7 = 49"), W("b", "11 × 11 = 121")),
    Q("So does every composite number up to 50 get crossed out?", ["Yes, every one", "No, some are left"], 0,
      "Every composite number up to 50 has 2, 3, 5 or 7 as a factor. So it is a multiple of one of them, and it gets crossed out."),
    B("Every composite number is gone. The numbers left have no smaller factor at all. Here are the ones after 7.",
      LB("l", "Left: 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47")),
    B("A number with no factor except 1 and itself is prime. So the numbers left in the sieve are prime numbers.",
      ANS("ans", "prime numbers"), CIRC("ans", "prime numbers")),
    B("They are not all multiples of 11, because 13 and 17 are there too. And they are not even: the even numbers went first."),
)

LESSONS["Q_CH16_012"] = LESSON(
    B("Five numbers: 31, 41, 51, 61 and 71. One of them does not belong with the others. Which one?",
      GIVEN("q", "Which does NOT belong?  31, 41, 51, 61, 71")),
    B("They all end in 1, and they go up in tens. So the pattern is not the clue. Think instead about what kind of numbers they are. 31 and 41 are prime."),
    Q("Let's test 51 for 3, by adding its digits. 5 plus 1 is 6. Is 6 in the 3 times table?", ["Yes, 3 × 2 = 6", "No, it is not"], 0,
      "3 times 2 is 6. So the digit sum is in the 3 times table, and that means 3 divides 51.",
      W("a", "5 + 1 = 6")),
    B("So 3 divides 51. In fact 51 is 3 times 17. It is not prime!", W("b", "51 = 3 × 17"), CIRC("q", "51")),
    B("Now the others. Their digits add up to 4, 5, 7 and 8. None of those is in the 3 times table. They are odd, they do not end in 5, and 7 skips them all. They are prime.",
      W("c", "3 + 1 = 4"), W("d", "4 + 1 = 5"), W("e", "6 + 1 = 7"), W("f", "7 + 1 = 8")),
    B("Four primes, and one number that is not. So 51 does not belong.", ANS("ans", "51 does not belong"), CIRC("ans", "51")),
    B("The trap is that 51 looks prime. It is odd and it ends in 1. But adding the digits shows that 3 divides it."),
)
