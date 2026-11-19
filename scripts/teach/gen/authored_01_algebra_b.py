"""Algebraic expressions, G5A_ALGEBRA_009 to 016: one lesson each, written by hand."""
from authored_01_lib import (ANS, ANSC, ARC, B, BOTH, CHOOSE, CIRC, DIVIDE, GIVEN, GROUP, LANS, LB,  # noqa: F401
                             LESSON, NOTE, STRIKE, UL, W)

LESSONS = {}
P = "G5A_ALGEBRA_"

# 4 pens: ₹3 off the bill against ₹3 off each pen  ->  ₹9 more
LESSONS[P + "009"] = LESSON(
    B("A pen costs p rupees. Ravi buys 4 pens and gets 3 rupees off his whole bill. Sana buys 4 pens and gets 3 rupees off each pen. How much more than Sana does Ravi pay?",
      GIVEN("q", "Ravi: 4 pens, ₹3 off the bill. Sana: 4 pens, ₹3 off each")),
    B("Ravi first. 4 pens cost 4 p, and 3 rupees comes off just once. So he pays 4 p minus 3.",
      W("l1", "4p − 3")),
    B("Now Sana. Each of her pens costs p minus 3. What does she pay for 4 of them?",
      ask=CHOOSE(["4p − 3", "4(p − 3)", "p − 12"], 1,
                 "Each pen costs the whole of p minus 3, and she buys 4 of them. So the 4 multiplies the whole bracket.")),
    B("Sana pays 4 times the bracket. 4 times p is 4 p, and 4 times 3 is 12. So she pays 4 p minus 12.",
      W("l2", "4(p − 3) = 4p − 12"), ARC("l2", "4", ["p", "3"])),
    B("See what happened? Sana's 3 rupees comes off 4 times, once for each pen. She saves 12 rupees. Ravi saves only 3.",
      UL("l2", "12"), UL("l1", "3")),
    B("Both start from 4 p. So Ravi pays more by the gap between the two savings: 12 minus 3, which is 9 rupees.",
      *ANSC("l3", "12 − 3 = 9", 9)),
    B("The trap is thinking the two deals are the same, because both say 3 rupees off. Off the bill happens once. Off each pen happens 4 times."),
    B("Check with pens at 10 rupees. Ravi pays 4 tens minus 3, which is 37. Sana pays 4 sevens, which is 28. And 37 minus 28 is 9.",
      W("c1", "4 × 10 − 3 = 37"), W("c2", "4 × (10 − 3) = 28"), W("c3", "37 − 28 = 9")),
    B("So write an expression for each person, open the brackets, and compare. Ravi pays 9 rupees more."),
    check=("p", 9),
)

# p = 2q, q = 3r  ->  p + q + r = 10r
LESSONS[P + "010"] = LESSON(
    B("We are told p equals 2 q, and q equals 3 r. We want one expression that is equal to p plus q plus r.",
      GIVEN("q", "p = 2q and q = 3r. Find p + q + r")),
    B("Three different letters can't be added as they stand. So the plan is to write all three using the same letter."),
    B("q is already written with r: q equals 3 r. So let's put everything in terms of r.",
      UL("q", "q = 3r")),
    B("p is 2 lots of q, and each q is 3 r. So what is p, written with r?",
      ask=CHOOSE(["2r", "5r", "6r"], 2,
                 "p is 2 lots of q, and each q is worth 3 r. 2 lots of 3 r make 6 r.")),
    B("p is 2 times 3 r, which is 6 r. The slip to avoid is adding the 2 and the 3. 2 lots of something is a multiplication.",
      W("l1", "2 × 3r = 6r"), LB("l2", "p = 6r")),
    B("Now add the three. p is 6 r, q is 3 r, and r is just 1 r. Don't leave that last one out.",
      W("l3", "6r + 3r + r"), UL("l3", "r", 3)),
    B("6 and 3 and 1 make 10. So p plus q plus r equals 10 r.",
      ANS("l4", "6r + 3r + r = 10r"), CIRC("l4", "10r")),
    B("Check with r as 1. Then q is 3 and p is 6. And 6 plus 3 plus 1 is 10, which is 10 times r.",
      W("c1", "6 + 3 + 1 = 10")),
    B("So to add different letters, first write each one using the same letter. Then just count how many you have."),
    check=("r", 10),
)

# Perimeter 4k + 10, length k + 4  ->  breadth k + 1
LESSONS[P + "011"] = LESSON(
    B("A rectangle has a perimeter of 4 k plus 10 centimetres, and its length is k plus 4 centimetres. We want an expression for its breadth.",
      GIVEN("q", "Perimeter (4k + 10) cm, length (k + 4) cm. Breadth?")),
    B("A rectangle's perimeter is made of 2 lengths and 2 breadths. We'll work backwards from it, one stage at a time.",
      LB("l1", "Perimeter = 2 lengths + 2 breadths")),
    B("If we halve the perimeter, what do we have?",
      ask=CHOOSE(["1 length + 1 breadth", "2 breadths", "1 breadth"], 0,
                 "The perimeter is 2 lengths and 2 breadths. Half of that is 1 length and 1 breadth.")),
    B("Half of 4 k is 2 k, and half of 10 is 5. So one length and one breadth together make 2 k plus 5.",
      W("l2", "(4k + 10) ÷ 2 = 2k + 5")),
    B("Now take the length away, and the breadth is what is left. The length is k plus 4.",
      W("l3", "(2k + 5) − (k + 4)")),
    B("Do the k parts and the number parts one at a time. 2 k minus k is k. And 5 minus 4 is 1.",
      W("l4", "5 − 4 = 1")),
    B("So the breadth is k plus 1.",
      ANS("l5", "(2k + 5) − (k + 4) = k + 1"), CIRC("l5", "k + 1")),
    B("Two traps to dodge. Taking the length from the whole perimeter leaves a length and 2 breadths. And stopping at 2 k plus 5 gives a length and a breadth together."),
    B("Check: a length and a breadth are k plus 4 and k plus 1. Add them and double it, and we get 4 k plus 10, our perimeter.",
      W("c1", "2 × (k + 4 + k + 1) = 4k + 10")),
    B("So to get from a perimeter to a side: halve it first, then take away the side you know. The breadth is k plus 1."),
    check=("k", 1),
)

# Arjun y, father 3y + 4: sum in 5 years is 4y + 14
LESSONS[P + "012"] = LESSON(
    B("Arjun is y years old now. His father's age is 4 more than 3 times Arjun's age. We want the sum of their ages 5 years from now.",
      GIVEN("q", "Arjun: y. Father: 4 more than 3 times y. Sum in 5 years?")),
    B("Take it in three stages. Their ages now, their ages in 5 years, and only then the sum."),
    B("Arjun is y now. His father is 3 times y, plus 4. So his father is 3 y plus 4.",
      LB("l1", "Now: Arjun y, Father 3y + 4")),
    B("Think about 5 years from now. Who will be 5 years older?",
      ask=CHOOSE(["only Arjun", "only his father", "both of them"], 2,
                 "Time passes for everyone. In 5 years, Arjun is 5 years older, and so is his father.")),
    B("Arjun will be y plus 5. His father will be 3 y plus 4, plus 5, which is 3 y plus 9.",
      W("l2", "y + 5"), W("l3", "3y + 4 + 5 = 3y + 9")),
    B("Now add the two ages: y plus 5, plus 3 y plus 9.",
      W("l4", "y + 5 + 3y + 9")),
    B("y and 3 y make 4 y. 5 and 9 make 14. So the sum of their ages will be 4 y plus 14.",
      GROUP("l4", ["y", "3y"], "4y"), ANS("l5", "y + 5 + 3y + 9 = 4y + 14"), CIRC("l5", "4y + 14")),
    B("The trap is adding the 5 years only once. There are two people, and each of them grows 5 years older, so the sum grows by 10.",
      W("l6", "5 + 5 = 10")),
    B("Check with Arjun aged 10. His father is 34. In 5 years they are 15 and 39, which add up to 54. And 4 times 10, plus 14, is 54 too.",
      W("c1", "3 × 10 + 4 = 34"), W("c2", "15 + 39 = 54"), W("c3", "4 × 10 + 14 = 54")),
    B("So with ages: write each age now, then each age later, and add at the very end."),
    check=("y", 4),
)

# nth term 6n + 5: 15 terms are less than 100
LESSONS[P + "013"] = LESSON(
    B("The n-th term of a sequence is 6 n plus 5, so the first term is 11. How many terms of the sequence are less than 100?",
      GIVEN("q", "nth term is 6n + 5. How many terms are less than 100?")),
    B("The terms go 11, 17, 23, and keep climbing by 6. We need the last one that is still below 100, and its position, n.",
      LB("l0", "11, 17, 23, ...")),
    B("For a term to be below 100, 6 n plus 5 must be less than 100.",
      W("l1", "6n + 5 < 100")),
    B("Take the 5 off both sides. So 6 n must be less than 95.",
      STRIKE("l1", "+ 5", "− 5"), W("l2", "6n < 95")),
    B("What is the biggest n that keeps 6 n below 95?",
      ask=CHOOSE(["14", "15", "16"], 1,
                 "Try the 6 times table near 95. 6 times 15 stays under it, but 6 times 16 goes just over.")),
    B("6 times 15 is 90, which fits. 6 times 16 is 96, which is too big. So the biggest n is 15.",
      W("l3", "6 × 15 = 90"), W("l4", "6 × 16 = 96")),
    B("Here is the trap. 100 divided by 6 is 16 and a bit, so 16 looks right. But that forgets the plus 5. The 16th term is 96 plus 5, which is 101. That is over 100.",
      W("l5", "6 × 16 + 5 = 101")),
    B("And the 15th term is 90 plus 5, which is 95. That is the last one below 100.",
      W("l6", "6 × 15 + 5 = 95")),
    B("The terms below 100 run from the 1st up to the 15th. So there are 15 of them.",
      ANS("l7", "n = 15"), CIRC("l7", "n = 15")),
    B("So: set the rule below the limit, undo it step by step, then check the term on each side of the cut."),
    check=("n", 15),
)

# Always odd: n × (n + 1) + 1
LESSONS[P + "014"] = LESSON(
    B("Four expressions: n plus 1, 3 n, 2 n plus 4, and n times the bracket n plus 1, then plus 1. Which one gives an odd number for every whole number n?",
      GIVEN("q", "Always odd?   n + 1,   3n,   2n + 4,   n × (n + 1) + 1")),
    B("Every whole number means odd ones and even ones. So we test each expression with one of each: n as 1, and n as 2.",
      LB("l1", "Test n = 1 and n = 2")),
    B("n plus 1: with n as 1, it gives 2. That is even already, so it is out.",
      W("l2", "1 + 1 = 2"), STRIKE("q", "n + 1")),
    B("3 n: with n as 1, it gives 3, which is odd. Is that enough to trust it?",
      ask=CHOOSE(["Yes, 3 is odd", "No, try n = 2 as well"], 1,
                 "One odd answer is not every answer. We said we would test an even n too, so try n as 2.")),
    B("With n as 2, 3 n is 6. That is even, so 3 n is out too. This is the trap: an expression can look right for one value and still let us down.",
      W("l3", "3 × 2 = 6"), STRIKE("q", "3n")),
    B("2 n plus 4 gives 6, and then 8. Both of its parts are even, so it is always even. Out.",
      W("l4", "2 × 1 + 4 = 6"), W("l5", "2 × 2 + 4 = 8"), STRIKE("q", "2n + 4")),
    B("The last one. With n as 1, it is 1 times 2, plus 1, which is 3. With n as 2, it is 2 times 3, plus 1, which is 7. Both are odd.",
      W("l6", "1 × 2 + 1 = 3"), W("l7", "2 × 3 + 1 = 7")),
    B("Why does it always work? n and n plus 1 are neighbours, so one of them is even. That makes their product even. And an even number plus 1 is odd.",
      LB("l8", "even + 1 = odd")),
    B("So the expression that is always odd is n times the bracket n plus 1, then plus 1.",
      LANS("a", "n × (n + 1) + 1 is always odd"), CIRC("q", "n × (n + 1) + 1")),
    B("To test every n, try an odd one and an even one. A single even answer is enough to rule an expression out."),
)

# Taxi: ₹40 for the first 2 km, then ₹c per km  ->  40 + c × (d − 2)
LESSONS[P + "015"] = LESSON(
    B("A taxi charges 40 rupees for the first 2 kilometres, and c rupees for every kilometre after that. We want the fare for a ride of d kilometres.",
      GIVEN("q", "₹40 for the first 2 km, then ₹c per km. Fare for d km?")),
    B("Split the ride into two parts. The first 2 kilometres, with a fixed charge. And the rest, charged for each kilometre."),
    B("The first part is simple. The first 2 kilometres cost 40 rupees altogether, paid once.",
      LB("l1", "First 2 km: 40")),
    B("The whole ride is d kilometres. How many kilometres are left to pay for, at c rupees each?",
      ask=CHOOSE(["d", "d − 2", "d + 2"], 1,
                 "The first 2 kilometres are already covered by the 40 rupees. So out of d kilometres, d minus 2 are left.")),
    B("d minus 2 kilometres are left, at c rupees each. That costs c times the whole of d minus 2. The brackets keep d minus 2 together.",
      LB("l2", "The rest: c × (d − 2)"), UL("l2", "(d − 2)")),
    B("Add the two parts. The fare is 40, plus c times the bracket d minus 2.",
      LANS("l3", "Fare = 40 + c × (d − 2)"), CIRC("l3", "40 + c × (d − 2)")),
    B("Watch the traps. c times d would charge for every kilometre, but the first 2 are already paid for. And without brackets, we would take 2 rupees off the fare, not 2 kilometres off the distance."),
    B("Check with numbers. Say c is 10 and the ride is 5 kilometres. Then 3 kilometres are left, costing 30. With the 40, the fare is 70.",
      W("c1", "5 − 2 = 3"), W("c2", "10 × 3 = 30"), W("c3", "40 + 30 = 70")),
    B("So for a charge in two parts: work out each part on its own, then add. The fare is 40, plus c times the bracket d minus 2."),
)

# Number machine: double, add 6, halve, subtract n  ->  always 3
LESSONS[P + "016"] = LESSON(
    B("A number machine takes a number n. It doubles it, adds 6, halves the result, and then subtracts the n that went in. What comes out?",
      GIVEN("q", "n: double, add 6, halve the result, subtract n")),
    B("Follow the machine one action at a time. Doubling n gives 2 n. Adding 6 gives 2 n plus 6.",
      W("l1", "2n + 6")),
    B("Now the machine halves the result. What is half of 2 n plus 6?",
      ask=CHOOSE(["n + 6", "n + 3", "2n + 3"], 1,
                 "The result is the whole of 2 n plus 6, so both parts are halved. Half of 2 n is n, and half of 6 is 3.")),
    B("Halving goes to both parts. Half of 2 n is n, and half of 6 is 3. So now the machine holds n plus 3.",
      W("l2", "(2n + 6) ÷ 2 = n + 3"), UL("l2", "3")),
    B("That was the trap: halving only the 2 n and leaving the 6 as it is. The 6 is part of the result, so it is halved as well."),
    B("Last action: subtract the n that went in. n plus 3, take away n.",
      W("l3", "n + 3 − n")),
    B("The n and the minus n cancel each other. All that is left is 3.",
      STRIKE("l3", "n"), STRIKE("l3", "− n"), ANS("l4", "n + 3 − n = 3"), CIRC("l4", "3", 2)),
    B("Look, there is no n left in the answer. Whatever number goes in, 3 comes out."),
    B("Check with 5. Double it and add 6, and we have 16. Halve it, 8. Take away the 5 we started with, and we get 3.",
      W("c1", "5 × 2 + 6 = 16"), W("c2", "16 ÷ 2 = 8"), W("c3", "8 − 5 = 3")),
    B("So follow a machine one action at a time, and remember that halving a result halves every part of it."),
    check=("n", 3),
)
