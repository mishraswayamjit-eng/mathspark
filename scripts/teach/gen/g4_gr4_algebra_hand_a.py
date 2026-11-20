"""Lessons written one by one: past exam papers (EXT_G4_FP_...) and worksheet questions (EXT_G4_WS2_...)."""
from g4_gr4_algebra_lib import (B, L, T, W, answer, arc, box, choose, fig, given, group, last_num, lesson, mark, note,
                                strike, under)

LESSONS = {}

# If a=2b and b=3, value of 2a−b?   (9)
LESSONS["EXT_G4_FP_2020_018"] = lesson([
    B("Two letters here. a is 2 b, and b is 3. We want the value of 2 a minus b.",
      given("g1", "a = 2b,  b = 3", label=True), given("g2", "2a − b", label=True)),
    B("We cannot use a until we know its number. a is 2 b. So what is a?",
      ask=choose(["6", "3", "5"], 0,
                 "2 b means 2 times b. And b is 3. So a is 2 times 3.")),
    B("a is 2 times b, and b is 3. 2 times 3 is 6, so a is 6. Careful: 6 is only a. It is not our answer yet.",
      W("l1", "2 × 3 = 6"), note("l1", "6", "a")),
    B("Now both letters have numbers. Put 6 in place of a, and 3 in place of b.",
      note("g2", "a", "6"), note("g2", "b", "3"), W("l2", "2 × 6 − 3")),
    B("A times and a take away. Which one do we do first?",
      ask=choose(["the times: 2 × 6", "the take away: 6 − 3"], 0,
                 "Multiplying goes before taking away. So 2 times 6 comes first.")),
    B("2 times 6 is 12. Then 12 minus 3 is 9.",
      W("l3", "2 × 6 = 12"), answer("l4", "12 − 3 = 9"), mark("l4", "9")),
    B("So the value is 9. The trick was to find a first. When one letter is given through another, "
      "work that letter out before anything else."),
])

# Rectangle: length=breadth+2. Breadth=a+2. Perimeter?   (4a+12)
LESSONS["EXT_G4_FP_2020_037"] = lesson([
    B("Here is a rectangle. Its breadth is a plus 2. Its length is 2 more than its breadth. We want the perimeter.",
      given("g1", "breadth = a + 2", label=True), given("g2", "length = breadth + 2", label=True),
      fig("EXT_G4_FP_2020_037")),
    B("Before the perimeter, we need the length written with a. The length is 2 more than a plus 2. What is it?",
      ask=choose(["a + 4", "a + 2", "2a + 2"], 0,
                 "The breadth is a plus 2. Add 2 more to it. a plus 2, plus 2, is a plus 4.")),
    B("The length is a plus 2, plus 2 more. That makes a plus 4.",
      W("l1", "a + 2 + 2 = a + 4"), note("l1", "a + 4", "length")),
    B("Perimeter means all the way round. That is 2 lengths and 2 breadths. "
      "An easy way: add one length and one breadth, then double.",
      L("l2", "Perimeter = 2 × (length + breadth)")),
    B("Length plus breadth is a plus 4, plus a plus 2. Two a's make 2 a. And 4 plus 2 is 6. So we get 2 a plus 6.",
      W("l3", "a + 4 + a + 2 = 2a + 6"), group("l3", [T("a", 1), T("a", 2)], "2a")),
    B("Now double it. Here is the trap. What is 2 times, 2 a plus 6?",
      ask=choose(["4a + 12", "4a + 6", "2a + 12"], 0,
                 "Doubling doubles both parts. 2 times 2 a is 4 a, and 2 times 6 is 12. Neither part may be left out.")),
    B("The 2 multiplies both parts in the bracket. 2 times 2 a is 4 a. 2 times 6 is 12.",
      answer("l4", "2(2a + 6) = 4a + 12"), arc("l4", "2", "2a", "6"), mark("l4", "4a + 12")),
    B("So the perimeter is 4 a plus 12. Write every side with the letter first. Then add, and double both parts."),
], "a", 4)

# a=2, b=5. Value of (a+b)×(b−a)?   (21)
LESSONS["EXT_G4_FP_2020_039"] = lesson([
    B("a is 2 and b is 5. We want the value of two brackets multiplied together: a plus b, times b minus a.",
      given("g1", "a = 2, b = 5", label=True), given("g2", "(a + b) × (b − a)", label=True)),
    B("Two brackets, with a times sign between them. What do we work out first?",
      ask=choose(["each bracket", "the times in the middle"], 0,
                 "Brackets always come first. They are like parcels: open each one before you do anything else.")),
    B("First bracket: a plus b. That is 2 plus 5, which is 7.",
      under("g2", "(a + b)"), W("l1", "2 + 5 = 7")),
    B("Second bracket: b minus a. Careful, it is not the same as the first one. b comes first: 5 minus 2 is 3.",
      under("g2", "(b − a)"), W("l2", "5 − 2 = 3")),
    B("Now we have 7 and 3. What do we do with them?",
      ask=choose(["multiply: 7 × 3", "add: 7 + 3"], 0,
                 "Look at the sign between the two brackets. It is a times sign. So we multiply 7 by 3.")),
    B("7 times 3 is 21.", answer("l3", "7 × 3 = 21"), mark("l3", "21")),
    B("So the value is 21. Brackets first, one at a time. Then the times that joins them."),
])

# 6x−3y+5z when x=3, y=x−1, z=x+y?   (37)
LESSONS["EXT_G4_FP_2021_008"] = lesson([
    B("Three letters here. x is 3. y is x minus 1. And z is x plus y. We want 6 x, minus 3 y, plus 5 z.",
      given("g1", "x = 3,  y = x − 1,  z = x + y", label=True), given("g2", "6x − 3y + 5z", label=True)),
    B("Only x is a plain number so far. So we find y next. y is x minus 1, and 3 minus 1 is 2.",
      W("l1", "3 − 1 = 2"), note("l1", "2", "y")),
    B("Now z. z is x plus y. What is z?",
      ask=choose(["5", "3", "4"], 0,
                 "z is x plus y. x is 3 and y is 2. So z is 3 plus 2.")),
    B("z is 3 plus 2, which is 5. Now every letter has its own number.",
      W("l2", "3 + 2 = 5"), note("l2", "5", "z")),
    B("Put them in. 6 x is 6 times 3. 3 y is 3 times 2. 5 z is 5 times 5.",
      W("l3", "6 × 3 − 3 × 2 + 5 × 5")),
    B("Do the times first. 6 times 3 is 18. 3 times 2 is 6. 5 times 5 is 25.",
      W("l4", "18 − 6 + 25")),
    B("Now go left to right. 18 minus 6 is 12. Then 12 plus 25 is 37.",
      W("l5", "18 − 6 = 12"), answer("l6", "12 + 25 = 37"), mark("l6", "37")),
    B("So the value is 37. When letters depend on other letters, find them one at a time, in order. "
      "Only then touch the big expression."),
])

# If a=3 and b=6, which expression has least value?   (3b−5a)
_L3 = "3 × 6 − 5 × 3 = 18 − 15 = 3"
LESSONS["EXT_G4_FP_2022_038"] = lesson([
    B("a is 3 and b is 6. We have four expressions, and we want the one with the least value. "
      "Least means smallest. So we find the value of every one.",
      given("g1", "a = 3, b = 6", label=True)),
    B("First, 4 a minus b. 4 times 3 is 12, and 12 minus 6 is 6.",
      W("l1", "4 × 3 − 6 = 12 − 6 = 6"), note("l1", "4 × 3 − 6", "4a − b")),
    B("Next, 5 b minus 7 a. 5 times 6 is 30. 7 times 3 is 21. And 30 minus 21 is 9.",
      W("l2", "5 × 6 − 7 × 3 = 30 − 21 = 9"), note("l2", "5 × 6 − 7 × 3", "5b − 7a")),
    B("Your turn. What is 3 b minus 5 a?",
      ask=choose(["3", "33", "1"], 0,
                 "3 b means 3 times 6. 5 a means 5 times 3. Work out each one, then take the second from the first.")),
    B("3 times 6 is 18. 5 times 3 is 15. And 18 minus 15 is 3.",
      W("l3", _L3), note("l3", "3 × 6 − 5 × 3", "3b − 5a")),
    B("Last one, 7 a minus 2 b. 7 times 3 is 21. 2 times 6 is 12. And 21 minus 12 is 9.",
      W("l4", "7 × 3 − 2 × 6 = 21 − 12 = 9"), note("l4", "7 × 3 − 2 × 6", "7a − 2b")),
    B("Now compare the four values: 6, 9, 3 and 9. The smallest is 3.",
      box("l3", last_num(_L3, 3))),
    B("That 3 came from 3 b minus 5 a. So that one has the least value.",
      answer("a1", "3b − 5a is the least", label=True), mark("a1", "3b − 5a")),
    B("When you are asked for the least or the greatest, do not guess from the look. "
      "Work out every one, then compare. Here the least is 3 b minus 5 a."),
])

# m=2, n=3, p=5. Which expression has least value?   ((p−n)×m)
LESSONS["EXT_G4_FP_2024_001"] = lesson([
    B("m is 2, n is 3 and p is 5. Four expressions, and we want the one with the least value. "
      "So we work out each one.",
      given("g1", "m = 2, n = 3, p = 5", label=True)),
    B("First, m times n, plus p. Times first: 2 times 3 is 6. Then 6 plus 5 is 11.",
      W("l1", "2 × 3 + 5 = 11"), note("l1", "2 × 3 + 5", "m × n + p")),
    B("Next, p minus m in a bracket, times n. Bracket first: 5 minus 2 is 3. Then 3 times 3 is 9.",
      W("l2", "(5 − 2) × 3 = 9"), note("l2", "(5 − 2) × 3", "(p − m) × n")),
    B("Now p minus n in a bracket, times m. With the numbers in, that is 5 minus 3 in a bracket, times 2. "
      "What do we do first?",
      W("l3", "(5 − 3) × 2"), note("l3", "(5 − 3) × 2", "(p − n) × m"),
      ask=choose(["5 − 3, the bracket", "3 × 2, the times"], 0,
                 "A bracket always goes first. So work out 5 minus 3, and then multiply by 2.")),
    B("5 minus 3 is 2. And 2 times 2 is 4.", W("l4", "2 × 2 = 4")),
    B("Last, p plus n minus m. 5 plus 3 is 8, and 8 minus 2 is 6.",
      W("l5", "5 + 3 − 2 = 6"), note("l5", "5 + 3 − 2", "p + n − m")),
    B("Compare the four values: 11, 9, 4 and 6. The smallest is 4.", box("l4", "4")),
    B("That 4 came from p minus n, in a bracket, times m. So that one has the least value.",
      answer("a1", "(p − n) × m is the least", label=True), mark("a1", "(p − n) × m")),
    B("To find the least, work out every expression, brackets first. Then compare the numbers, not the letters."),
])

# Insert sign: 4A+17 □ 8A−9, where A=7.   (<)
LESSONS["EXT_G4_FP_2024_022"] = lesson([
    B("Two expressions, with an empty box between them. On the left, 4 A plus 17. On the right, 8 A minus 9. "
      "And A is 7. We must choose the sign that fits in the box.",
      given("g1", "4A + 17 □ 8A − 9", label=True), given("g2", "A = 7", label=True)),
    B("How can we tell which side is bigger?",
      ask=choose(["find the value of each side", "the side with 17 is bigger", "the side with 8A is bigger"], 0,
                 "We cannot tell just by looking. Each side has to be worked out with A as 7. "
                 "Then we compare the two numbers.")),
    B("Left side first. 4 A is 4 times 7, which is 28. Then 28 plus 17 is 45.",
      under("g1", "4A + 17"), W("l1", "4 × 7 + 17 = 28 + 17 = 45")),
    B("Now the right side. 8 A is 8 times 7, which is 56. Then 56 minus 9 is 47.",
      under("g1", "8A − 9"), W("l2", "8 × 7 − 9 = 56 − 9 = 47")),
    B("So it is 45 on the left and 47 on the right. Which of these is true?",
      ask=choose(["45 is less than 47", "45 is greater than 47", "they are equal"], 0,
                 "They are close, but not the same. 45 comes before 47 when we count, so 45 is the smaller one.")),
    B("45 is less than 47. The less than sign has its small pointed end towards the smaller number, "
      "and its open end towards the bigger one.",
      answer("a1", "45 < 47"), mark("a1", "<")),
    B("So the less than sign goes in the box. Work out both sides first. "
      "Then let the open mouth of the sign face the bigger number.",
      L("l3", "4A + 17 < 8A − 9")),
])

# (V+38) is 2-digit prime. Find 13th even number before it?   (V+13)
LESSONS["EXT_G4_FP_2025_010"] = lesson([
    B("Here is a puzzle. V plus 38 is a 2 digit prime number. We want the 13th even number before it.",
      given("g1", "V + 38 is a 2-digit prime", label=True)),
    B("First clue. Is a 2 digit prime number odd or even?",
      ask=choose(["odd", "even", "it could be either"], 0,
                 "An even number can be divided by 2, so it cannot be prime, except for 2 itself. "
                 "And 2 has only one digit. So every 2 digit prime is odd.")),
    B("So V plus 38 is odd. The even number just before an odd number is only 1 less. "
      "So the 1st even number before it is V plus 37.",
      W("l1", "38 − 1 = 37"), L("l2", "1st even number before: V + 37")),
    B("Even numbers are 2 apart. So each one further back is 2 less than the one before.",
      L("l3", "V + 37,  V + 35,  V + 33, ...")),
    B("Here is the trap. From the 1st even number to the 13th, how many jumps of 2 do we make?",
      ask=choose(["12 jumps", "13 jumps", "14 jumps"], 0,
                 "Try a small case. From the 1st to the 3rd is only 2 jumps. "
                 "The number of jumps is always 1 less. So here it is 12 jumps.")),
    B("12 jumps of 2 is 24. So we go back 24 from V plus 37.", W("l4", "12 × 2 = 24")),
    B("37 minus 24 is 13. So the 13th even number before it is V plus 13.",
      W("l5", "37 − 24 = 13"), answer("a1", "V + 13", label=True), mark("a1", "V + 13")),
    B("Two traps here. The prime is odd, so the first step back is only 1. "
      "And 13 numbers have just 12 gaps between them. That gives V plus 13."),
])

# p=4 and q=2p+1. Value of (q−p)×(q+p)?   (65)
LESSONS["EXT_G4_FP_2025_012"] = lesson([
    B("p is 4, and q is 2 p plus 1. We want q minus p in one bracket, times q plus p in another.",
      given("g1", "p = 4,  q = 2p + 1", label=True), given("g2", "(q − p) × (q + p)", label=True)),
    B("We need a number for q before we can open any bracket. q is 2 p plus 1. What is q?",
      ask=choose(["9", "7", "25"], 0,
                 "2 p means 2 times p. So q is 2 times 4, and then 1 more.")),
    B("2 times 4 is 8, and 1 more is 9. So q is 9.",
      W("l1", "2 × 4 + 1 = 9"), note("l1", "9", "q")),
    B("First bracket: q minus p. 9 minus 4 is 5.", under("g2", "(q − p)"), W("l2", "9 − 4 = 5")),
    B("Second bracket: q plus p. 9 plus 4 is 13.", under("g2", "(q + p)"), W("l3", "9 + 4 = 13")),
    B("Now multiply the two brackets. What is 5 times 13?",
      ask=choose(["65", "56", "18"], 0,
                 "Split 13 into 10 and 3. Multiply each part by 5, and add the two answers.")),
    B("5 times 10 is 50. 5 times 3 is 15. And 50 plus 15 is 65.",
      W("l4", "5 × 10 + 5 × 3 = 50 + 15 = 65"), answer("a1", "5 × 13 = 65"), mark("a1", "65")),
    B("So the value is 65. Find every letter first, then each bracket, and multiply last."),
])

# p=4, a=2p−1, y=a+2. Which expression has greatest value?   (3p+a−y)
LESSONS["EXT_G4_FP_2025_038"] = lesson([
    B("Three letters, and each one leans on the one before. We want the expression with the greatest value. "
      "So first we find each letter.",
      given("g1", "p = 4,  a = 2p − 1,  y = a + 2", label=True)),
    B("a is 2 p minus 1. 2 times 4 is 8, and 8 minus 1 is 7. So a is 7.",
      W("l1", "2 × 4 − 1 = 7"), note("l1", "7", "a")),
    B("y is a plus 2. What is y?",
      ask=choose(["9", "6", "7"], 0,
                 "y is built from a, not from p. And a is 7. So y is 7 plus 2.")),
    B("7 plus 2 is 9. So p is 4, a is 7 and y is 9.", W("l2", "7 + 2 = 9"), note("l2", "9", "y")),
    B("First expression: 3 a, minus 2 y, plus p. 3 times 7 is 21. 2 times 9 is 18. "
      "21 minus 18 is 3, and 3 plus 4 is 7.",
      W("l3", "3 × 7 − 2 × 9 + 4 = 21 − 18 + 4 = 7"), note("l3", "3 × 7 − 2 × 9 + 4", "3a − 2y + p")),
    B("Second: 3 p, plus a, minus y. 3 times 4 is 12. Then 12 plus 7, minus 9, is 10.",
      W("l4", "3 × 4 + 7 − 9 = 12 + 7 − 9 = 10"), note("l4", "3 × 4 + 7 − 9", "3p + a − y")),
    B("Third: y, minus a, plus p. 9 minus 7 is 2, and 2 plus 4 is 6.",
      W("l5", "9 − 7 + 4 = 6"), note("l5", "9 − 7 + 4", "y − a + p")),
    B("The three values are 7, 10 and 6. One of the choices says they all have the same value. Is that true?",
      ask=choose(["No, 10 is the greatest", "Yes, they are all the same"], 0,
                 "Look at the three values again: 7, 10 and 6. They are different, and the biggest is 10.")),
    B("10 is the greatest. It came from 3 p, plus a, minus y.",
      box("l4", "10"), answer("a1", "3p + a − y is the greatest", label=True), mark("a1", "3p + a − y")),
    B("So the answer is 3 p plus a minus y. When letters lean on each other, find them in order. "
      "Then work out every expression before you choose."),
])

# Sia purchased x kg of apples and 2 kg of bananas. Total weight?   ((x+2) kg)
LESSONS["EXT_G4_WS2_CH13_001"] = lesson([
    B("Sia bought x kilograms of apples and 2 kilograms of bananas. We want the total weight. "
      "The x just stands for a number we do not know yet.",
      given("g1", "apples: x kg,   bananas: 2 kg", label=True), fig("EXT_G4_WS2_CH13_001")),
    B("Pretend for a moment that the apples weigh 3 kilograms. Then the total is 3 plus 2, which is 5 kilograms.",
      W("l1", "3 + 2 = 5")),
    B("So what did we do to get the total?",
      ask=choose(["we added", "we multiplied", "we took away"], 0,
                 "Total means everything put together. The apples and the bananas go into one bag, "
                 "so the two weights are added.")),
    B("Now do the very same thing with x in place of the 3. That gives x plus 2.",
      strike("l1", "3", "x"), L("l2", "x + 2")),
    B("Can we squash x plus 2 into one piece, like 2 x?",
      ask=choose(["No, x + 2 stays as it is", "Yes, it becomes 2x"], 0,
                 "2 x would mean 2 times x. But we are adding 2, not multiplying. "
                 "We do not know x, so x plus 2 just stays x plus 2.")),
    B("So the total weight is x plus 2 kilograms. The brackets keep the x plus 2 together as one weight.",
      answer("a1", "(x + 2) kg", label=True), mark("a1", "(x + 2) kg")),
    B("When a question says total or altogether, we add. If one part is a letter, the answer keeps the letter in it."),
])

# Mann reads k pages in an hour. How many pages in 6 hours?   (6k pages)
LESSONS["EXT_G4_WS2_CH13_002"] = lesson([
    B("Mann reads k pages in one hour. We want to know how many pages he reads in 6 hours.",
      given("g1", "1 hour: k pages", label=True), fig("EXT_G4_WS2_CH13_002")),
    B("Every hour he reads another k pages. So for 6 hours we count k, six times over.",
      L("l1", "k + k + k + k + k + k")),
    B("Adding the same thing 6 times is the same as which of these?",
      ask=choose(["6 × k", "k + 6", "k − 6"], 0,
                 "Adding 6 gives him only 6 extra pages, once. But he reads k pages in every one of the 6 hours. "
                 "Six lots of k is 6 times k.")),
    B("Six lots of k is 6 times k. In algebra we leave out the times sign and write the number first. So it is 6 k.",
      L("l2", "6 × k = 6k")),
    B("Let's test it with a number. If k were 10 pages, he would read 10 pages six times. "
      "6 times 10 is 60 pages. That makes sense.",
      W("l3", "6 × 10 = 60")),
    B("So Mann can read 6 k pages in 6 hours.", answer("a1", "6k pages", label=True), mark("a1", "6k")),
    B("More hours means more pages, so we multiply. Adding the same thing again and again always turns into times."),
])

# 8 years hence, Rahul will be y years old. What is his present age?   ((y−8) years)
LESSONS["EXT_G4_WS2_CH13_003"] = lesson([
    B("8 years hence means 8 years from now. In 8 years Rahul will be y years old. We want his age today.",
      given("g1", "in 8 years: y years old", label=True), fig("EXT_G4_WS2_CH13_003")),
    B("Is Rahul younger or older today than he will be in 8 years?",
      ask=choose(["younger today", "older today", "the same age"], 0,
                 "Every year we grow one year older. So 8 years from now he will be older, "
                 "and today he is younger than that.")),
    B("Try it with a number. Suppose he will be 20 then. Today he is 8 years younger: 20 minus 8, which is 12.",
      W("l1", "20 − 8 = 12")),
    B("Now put y back where the 20 was. Today he is y minus 8.",
      strike("l1", "20", "y"), L("l2", "y − 8")),
    B("Careful: y plus 8 would be bigger than y. That is an even older Rahul, further in the future. "
      "It is not today's Rahul."),
    B("So his present age is y minus 8 years.",
      answer("a1", "(y − 8) years", label=True), mark("a1", "(y − 8) years")),
    B("Hence means later. To come back from later to now, we take the years away."),
])

# What is 4 more than the sum of a and b?   (a+b+4)
LESSONS["EXT_G4_WS2_CH13_004"] = lesson([
    B("Let's turn words into algebra. 4 more than the sum of a and b. We take it one piece at a time.",
      given("g1", "4 more than the sum of a and b", label=True), fig("EXT_G4_WS2_CH13_004")),
    B("Start with the sum of a and b. What does sum mean?",
      ask=choose(["a + b", "a × b", "a − b"], 0,
                 "Sum is the word for adding. The sum of 2 and 3 is 5. So the sum of a and b is a plus b.")),
    B("So the sum of a and b is a plus b.", under("g1", "the sum of a and b"), L("l1", "a + b")),
    B("Now, 4 more than that. What do we do with the 4?",
      ask=choose(["add 4", "multiply by 4", "take away 4"], 0,
                 "More than means extra. If you have 4 more sweets than me, you add 4 to my number. So we add 4.")),
    B("4 more means add 4. So we get a plus b plus 4.",
      under("g1", "4 more than"), answer("a1", "a + b + 4", label=True), mark("a1", "a + b + 4")),
    B("Test it. Say a is 1 and b is 2. Their sum is 3, and 4 more than 3 is 7. "
      "Our expression gives 1 plus 2 plus 4, also 7.",
      W("l2", "1 + 2 + 4 = 7")),
    B("Remember the signal words. Sum means add, and more than means add too. So the answer is a plus b plus 4."),
])

# What is 4 times the difference of x and y?   (4(x−y))
LESSONS["EXT_G4_WS2_CH13_005"] = lesson([
    B("Words into algebra again. 4 times the difference of x and y. One piece at a time.",
      given("g1", "4 times the difference of x and y", label=True)),
    B("Start with the difference of x and y. What does difference mean?",
      ask=choose(["x − y", "x + y", "x × y"], 0,
                 "Difference is how far apart two numbers are. We find it by taking one away from the other. "
                 "So it is x minus y.")),
    B("So the difference of x and y is x minus y.", under("g1", "the difference of x and y"), L("l1", "x − y")),
    B("Now we need 4 times the whole difference, not just 4 times x. "
      "So we wrap x minus y in brackets, to keep it together.",
      L("l2", "(x − y)")),
    B("Which of these shows 4 times the whole difference?",
      ask=choose(["4(x − y)", "4x − y", "x − 4y"], 0,
                 "Without brackets, the 4 only touches the letter next to it. "
                 "The brackets tie x minus y into one parcel, so the 4 multiplies all of it.")),
    B("So we write 4, then the bracket. The 4 multiplies everything inside.",
      answer("a1", "4(x − y)", label=True), arc("a1", "4", "x", "y")),
    B("Test it. Say x is 5 and y is 2. The difference is 3, and 4 times 3 is 12. "
      "Without the brackets we would get 20 minus 2, which is 18. Not the same!",
      W("l3", "4 × (5 − 2) = 12"), W("l4", "4 × 5 − 2 = 20 − 2 = 18")),
    B("So when a number multiplies a whole difference, use brackets. Our answer is 4, bracket, x minus y."),
])

# If a = 3, b = 2, find the value of 5a + 3b.   (21)
LESSONS["EXT_G4_WS2_CH13_006"] = lesson([
    B("a is 3 and b is 2. We want the value of 5 a plus 3 b.",
      given("g1", "a = 3, b = 2", label=True), given("g2", "5a + 3b", label=True)),
    B("First, what does 5 a mean when a is 3?",
      ask=choose(["5 × 3", "5 + 3", "the number 53"], 0,
                 "When a number sits right next to a letter, there is a hidden times sign between them. "
                 "So 5 a means 5 times a. Here that is 5 times 3.")),
    B("So 5 a is 5 times 3. In the same way, 3 b is 3 times 2.",
      note("g2", "a", "3"), note("g2", "b", "2"), W("l1", "5 × 3 + 3 × 2")),
    B("Times first. 5 times 3 is 15. And 3 times 2 is 6.",
      W("l2", "5 × 3 = 15"), W("l3", "3 × 2 = 6")),
    B("Now we add. But which two numbers?",
      ask=choose(["15 and 6", "15 and 2", "5 and 3"], 0,
                 "The second part is 3 b, which is 3 times 2. That is 6, not just 2. So we add 15 and 6.")),
    B("15 plus 6 is 21.", answer("a1", "15 + 6 = 21"), mark("a1", "21")),
    B("So the value is 21. Swap each letter for its number, do both times, and only then add."),
])

# Simplify: 3(2b + 4c)   (6b+12c)
LESSONS["EXT_G4_WS2_CH13_007"] = lesson([
    B("A 3 stands outside a bracket. Inside are 2 b and 4 c. To simplify this, we open the bracket.",
      given("g1", "3(2b + 4c)", label=True)),
    B("The 3 is right next to the bracket. What does it do to the terms inside?",
      ask=choose(["multiplies both terms", "multiplies only the first term", "is added to each term"], 0,
                 "A number touching a bracket multiplies everything inside it. Think of 3 bags, "
                 "each holding 2 b and 4 c. Both things get tripled.")),
    B("First, 3 times 2 b. Three lots of 2 b make 6 b.",
      arc("g1", "3", "2b"), L("l1", "3 × 2b = 6b")),
    B("Now the part people forget. The 3 multiplies the 4 c as well. 3 times 4 c is 12 c.",
      arc("g1", "3", "4c"), L("l2", "3 × 4c = 12c")),
    B("Can we add 6 b and 12 c together to make one term?",
      ask=choose(["No, b and c are different letters", "Yes, it makes 18bc"], 0,
                 "b and c stand for different hidden numbers. They are different families, "
                 "so they stay side by side with a plus between them.")),
    B("So the answer is 6 b plus 12 c.", answer("a1", "6b + 12c", label=True), mark("a1", "6b + 12c")),
    B("Let's test it with b as 1 and c as 1. The bracket is 2 plus 4, which is 6, and 3 times 6 is 18. "
      "Our answer gives 6 plus 12, also 18.",
      W("l3", "3 × (2 + 4) = 18"), W("l4", "6 + 12 = 18")),
    B("The number outside visits every term inside the bracket. That gave us 6 b plus 12 c."),
])

# Simplify: 5(3 − 4n)   (15−20n)
LESSONS["EXT_G4_WS2_CH13_008"] = lesson([
    B("A 5 stands outside a bracket. Inside is 3 minus 4 n. We need to open the bracket.",
      given("g1", "5(3 − 4n)")),
    B("What does the 5 multiply?",
      ask=choose(["both the 3 and the 4n", "only the 3", "only the 4n"], 0,
                 "A number touching a bracket multiplies everything inside it. "
                 "So the 5 multiplies the 3, and it multiplies the 4 n too.")),
    B("First, 5 times 3. That is 15.", arc("g1", "5", "3"), W("l1", "5 × 3 = 15")),
    B("Next, 5 times 4 n. Five lots of 4 n make 20 n.", arc("g1", "5", "4n"), W("l2", "5 × 4n = 20n")),
    B("What sign goes between the 15 and the 20 n?",
      ask=choose(["minus", "plus"], 0,
                 "Look inside the bracket. The sign between the 3 and the 4 n is a minus. "
                 "Opening the bracket with a 5 does not change it.")),
    B("So it is 15 minus 20 n.", answer("a1", "5(3 − 4n) = 15 − 20n"), mark("a1", "15 − 20n")),
    B("Keep the order as well. The 3 came first and was not being taken away. So the 15 stays in front."),
    B("To open a bracket: multiply every term inside by the number outside, and keep the sign between them. "
      "That gave us 15 minus 20 n."),
], "n", 15)
