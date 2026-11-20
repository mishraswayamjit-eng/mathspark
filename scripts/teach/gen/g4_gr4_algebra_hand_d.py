"""Lessons written one by one: real past exam questions (PYQ_...)."""
from g4_gr4_algebra_lib import (B, L, T, W, answer, arc, box, choose, fig, given, group, lesson, mark, note, strike,
                                under)

LESSONS = {}

# Which expression is worth 70 when m = 5 and n = 7?   (7m + 5n)
LESSONS["PYQ_2016_Q19"] = lesson([
    B("m is 5 and n is 7. One of four expressions is worth exactly 70. We test them one by one.",
      given("g1", "m = 5, n = 7", label=True), given("g2", "which one is worth 70?", label=True)),
    B("First, 5 m plus 7 n. 5 times 5 is 25. 7 times 7 is 49. And 25 plus 49 is 74. Close, but not 70.",
      W("l1", "5 × 5 + 7 × 7 = 25 + 49 = 74"), note("l1", "5 × 5 + 7 × 7", "5m + 7n")),
    B("Next, 7 m plus 5 n. What is 7 m when m is 5?",
      ask=choose(["35", "12", "75"], 0,
                 "7 m means 7 times m. And m is 5. So it is 7 times 5.")),
    B("7 times 5 is 35. And 5 n is 5 times 7, which is 35 too. 35 plus 35 is 70. That is the one!",
      W("l2", "7 × 5 + 5 × 7 = 35 + 35 = 70"), note("l2", "7 × 5 + 5 × 7", "7m + 5n"), box("l2", "70")),
    B("Let's make sure about the others. They both have a minus sign. 7 m minus 5 n is 35 minus 35, which is 0.",
      W("l3", "7 × 5 − 5 × 7 = 0"), note("l3", "7 × 5 − 5 × 7", "7m − 5n")),
    B("And 5 m minus 7 n would take 49 away from 25. That cannot reach 70 either."),
    B("So the expression worth 70 is 7 m plus 5 n.",
      answer("a1", "7m + 5n = 70", label=True), mark("a1", "7m + 5n")),
    B("The first one used the very same numbers, but paired them differently. "
      "Which number multiplies which letter matters. The answer is 7 m plus 5 n."),
])

# P odd. The 17th odd number after it?   (P + 34)
LESSONS["PYQ_2016_Q20"] = lesson([
    B("P stands for an odd number. We want the 17th odd number that comes after it.",
      given("g1", "P is an odd number", label=True)),
    B("Try a real odd number first, say 1. The odd numbers after 1 are 3, 5, 7 and so on.",
      L("l1", "after 1:   3, 5, 7, ...")),
    B("How big is each jump from one odd number to the next?",
      ask=choose(["2", "1", "17"], 0,
                 "Between two odd numbers there is always an even number, and we jump over it. "
                 "From 1 to 3 is a jump of 2.")),
    B("Each jump is 2. So the 1st odd number after P is P plus 2. The 2nd is P plus 4. The 3rd is P plus 6.",
      L("l2", "P + 2,   P + 4,   P + 6, ...")),
    B("See the pattern? For the 17th odd number after P, how many jumps of 2 do we make?",
      ask=choose(["17 jumps", "16 jumps", "34 jumps"], 0,
                 "The 1st one took 1 jump. The 2nd took 2 jumps. The 3rd took 3. So the 17th takes 17 jumps.")),
    B("17 jumps of 2. 17 times 2 is 34.", W("l3", "17 × 2 = 34")),
    B("So the 17th odd number after P is P plus 34.", answer("a1", "P + 34", label=True), mark("a1", "P + 34")),
    B("The trap is to add just 17. But an odd number plus 17 is even, so that cannot be right. "
      "Each step is worth 2, so we add 34."),
])

# 6x − 3y + 5z, when x = 3, y = x − 1 and z = x + y   (37)
LESSONS["PYQ_2016_Q39"] = lesson([
    B("This is a chain. x is 3. But y is given using x, and z is given using x and y. "
      "So we find the letters first, in order.",
      given("g1", "x = 3,  y = x − 1,  z = x + y", label=True), given("g2", "6x − 3y + 5z", label=True)),
    B("We know x. Which letter can we find next?",
      ask=choose(["y", "z", "both at once"], 0,
                 "z needs both x and y, and we do not have y yet. But y needs only x, and we know x. "
                 "So y comes next.")),
    B("y is x minus 1. 3 minus 1 is 2. So y is 2.", W("l1", "3 − 1 = 2"), note("l1", "2", "y")),
    B("Now z is x plus y. 3 plus 2 is 5. So z is 5. It is x and y added together, not x on its own.",
      W("l2", "3 + 2 = 5"), note("l2", "5", "z")),
    B("Now the big expression. 6 x is 6 times 3, which is 18. 3 y is 3 times 2, which is 6. "
      "5 z is 5 times 5, which is 25.",
      W("l3", "6 × 3 = 18"), W("l4", "3 × 2 = 6"), W("l5", "5 × 5 = 25")),
    B("We have 18, 6 and 25. How do they go together?",
      ask=choose(["18 − 6 + 25", "18 + 6 + 25", "18 − 6 − 25"], 0,
                 "Each part keeps the sign in front of it. 3 y has a minus in front, and 5 z has a plus. "
                 "So it is 18, minus 6, plus 25.")),
    B("Left to right. 18 minus 6 is 12. And 12 plus 25 is 37.",
      W("l6", "18 − 6 = 12"), answer("a1", "12 + 25 = 37"), mark("a1", "37")),
    B("So the value is 37. In a chain, find each letter in order. Then swap them all in, "
      "and keep every sign in its place."),
])

# Sum of ages 5 years ago was 5x. Sum 5 years hence?   (5x + 20)
LESSONS["PYQ_2017_Q18"] = lesson([
    B("5 years ago, the ages of a mother and her daughter added up to 5 x. "
      "We want the sum of their ages 5 years hence. Hence means from now.",
      given("g1", "5 years ago: sum of ages = 5x", label=True), fig("PYQ_2017_Q18")),
    B("There are three moments: 5 years ago, today, and 5 years hence. We will walk forward one step at a time.",
      L("l1", "5 years ago   →   today   →   5 years hence")),
    B("From 5 years ago to today, the mother gets 5 years older. What about the daughter?",
      ask=choose(["5 years older too", "she stays the same", "10 years older"], 0,
                 "Time passes for both of them. Each one has 5 more birthdays. "
                 "So the daughter is 5 years older as well.")),
    B("Two people, each 5 years older. So the sum grows by 5 plus 5, which is 10. Today the sum is 5 x plus 10.",
      W("l2", "5 + 5 = 10"), W("l3", "5x + 10"), note("l3", "5x + 10", "today")),
    B("Is 5 x plus 10 our answer?",
      ask=choose(["No, that is only today", "Yes, we are done"], 0,
                 "The question asks for 5 years hence, which is 5 years after today. "
                 "So far we have only reached today.")),
    B("From today to 5 years hence, both grow 5 years older again. The sum grows by another 10.",
      W("l4", "5x + 10 + 10 = 5x + 20")),
    B("So 5 years hence, the sum of their ages will be 5 x plus 20.",
      answer("a1", "5x + 20"), mark("a1", "5x + 20")),
    B("Two traps. Count the years for both people, not just one. And go all the way from 5 years ago "
      "to 5 years hence. That is 10 years for each of them, so 20 in all."),
], "x", 5)

# Equilateral triangle, side (7m − 2n). Perimeter?   (21m − 6n)
LESSONS["PYQ_2017_Q22"] = lesson([
    B("An equilateral triangle. Each side is 7 m minus 2 n. We want its perimeter.",
      given("g1", "side = (7m − 2n)", label=True), fig("PYQ_2017_Q22")),
    B("How many equal sides does an equilateral triangle have?",
      ask=choose(["3", "2", "4"], 0,
                 "Equilateral means all the sides are equal, and a triangle has 3 sides. So there are 3 equal sides.")),
    B("So the perimeter is 3 times one side. 3 times, 7 m minus 2 n.", L("l1", "3(7m − 2n)")),
    B("The 3 multiplies each part. First, 3 times 7 m is 21 m.",
      arc("l1", "3", "7m"), L("l2", "3 × 7m = 21m")),
    B("Then 3 times 2 n is 6 n.", arc("l1", "3", "2n"), L("l3", "3 × 2n = 6n")),
    B("What sign goes between 21 m and 6 n?",
      ask=choose(["minus", "plus"], 0,
                 "In each side, 2 n is taken away. Three sides means it is taken away three times. "
                 "So 6 n is still taken away.")),
    B("So the perimeter is 21 m minus 6 n.", answer("a1", "21m − 6n", label=True), mark("a1", "21m − 6n")),
    B("Test it with m as 1 and n as 1. One side is 7 minus 2, which is 5, and 3 sides make 15. "
      "Our answer gives 21 minus 6, also 15.",
      W("l4", "3 × (7 − 2) = 15"), W("l5", "21 − 6 = 15")),
    B("m and n are different letters, so they never join into one term. Multiply each by 3, and keep the minus."),
])

# P even. The 3rd even number before it?   (P − 6)
LESSONS["PYQ_2017_Q24"] = lesson([
    B("P stands for an even number. We want the 3rd even number before it.",
      given("g1", "P is an even number", label=True)),
    B("Try a real even number first, say 20. The even numbers before 20 are 18, 16 and 14.",
      L("l1", "before 20:   18, 16, 14")),
    B("How big is each jump back?",
      ask=choose(["2", "1", "3"], 0,
                 "Even numbers are 2 apart, with an odd number in between. From 20 back to 18 is a jump of 2.")),
    B("Each jump back takes away 2. So before P come P minus 2, then P minus 4, then P minus 6.",
      L("l2", "P − 2,   P − 4,   P − 6")),
    B("Which one is the 3rd even number before P?",
      ask=choose(["P − 6", "P − 3", "P + 6"], 0,
                 "Count along the list: 1st, 2nd, 3rd. Three jumps of 2 take away 6. "
                 "And before means smaller, so we subtract.")),
    B("3 jumps of 2 is 6. So it is P minus 6.",
      W("l3", "3 × 2 = 6"), answer("a1", "P − 6", label=True), mark("a1", "P − 6")),
    B("Check with 20. The 3rd even number before 20 was 14. And 20 minus 6 is 14.", W("l4", "20 − 6 = 14")),
    B("Before means go back, so we take away. And each even step is worth 2, not 1. That gives P minus 6."),
])

# Rectangle: length (2a + 5b) cm, breadth 7 cm. Perimeter?   ((4a + 10b + 14) cm)
LESSONS["PYQ_2018_Q04"] = lesson([
    B("A rectangle is 2 a plus 5 b centimetres long, and 7 centimetres wide. We want its perimeter.",
      given("g1", "length (2a + 5b) cm,   breadth 7 cm", label=True), fig("PYQ_2018_Q04")),
    B("Walk all the way round a rectangle. What do you pass?",
      ask=choose(["2 lengths and 2 breadths", "1 length and 1 breadth", "2 lengths and 1 breadth"], 0,
                 "A rectangle has 4 sides. The top and the bottom are both lengths. "
                 "The left and the right are both breadths.")),
    B("So the perimeter is 2 lengths and 2 breadths.", L("l1", "Perimeter = 2 lengths + 2 breadths")),
    B("Two lengths first. Double each part of 2 a plus 5 b. 2 times 2 a is 4 a. 2 times 5 b is 10 b.",
      L("l2", "2(2a + 5b) = 4a + 10b"), arc("l2", "2", "2a", "5b")),
    B("Now the breadths. The breadth is 7. What do two breadths make?",
      ask=choose(["14", "7", "9"], 0,
                 "There are 2 breadths, one on each side. 7 and 7 make 14.")),
    B("2 times 7 is 14.", W("l3", "2 × 7 = 14")),
    B("Now add. 4 a, 10 b and 14 are three different kinds, so they just stand side by side.",
      answer("a1", "(4a + 10b + 14) cm", label=True), mark("a1", "(4a + 10b + 14) cm")),
    B("Every side is counted, so the length and the breadth are both doubled. "
      "The perimeter is 4 a plus 10 b plus 14."),
])

# G + 12 is even. The 6th even number prior to it?   (G)
LESSONS["PYQ_2018_Q21"] = lesson([
    B("G plus 12 is an even number. We want the 6th even number prior to it. Prior means before.",
      given("g1", "G + 12 is an even number", label=True)),
    B("Which number do we start counting back from?",
      ask=choose(["G + 12", "G", "12"], 0,
                 "The even number in the question is G plus 12, the whole thing. "
                 "That is our starting point, not G on its own.")),
    B("We start at G plus 12. Even numbers are 2 apart, so each step back takes away 2.",
      L("l1", "G + 12,   G + 10,   G + 8, ...")),
    B("How much do 6 steps back take away?",
      ask=choose(["12", "6", "8"], 0,
                 "Each step back is worth 2, not 1. Six steps of 2 make 12.")),
    B("6 times 2 is 12. So we take 12 away from G plus 12.", W("l2", "6 × 2 = 12")),
    B("Plus 12, then minus 12. They cancel each other, and nothing extra is left. Just G.",
      L("l3", "G + 12 − 12 = G"), strike("l3", "+ 12"), strike("l3", "− 12")),
    B("So the 6th even number before G plus 12 is G itself.", answer("a1", "G", label=True), mark("a1", "G")),
    B("Check with a number. If G were 20, then G plus 12 is 32. Going back 12 from 32 brings us to 20. Back at G.",
      W("l4", "20 + 12 = 32"), W("l5", "32 − 12 = 20")),
    B("The trap is to count back from G and get G minus 12. Always start from the number the question gives you."),
])

# Square of side (3a + 2b). Perimeter?   (2(6a + 4b))
LESSONS["PYQ_2018_Q37"] = lesson([
    B("A square. Each side measures 3 a plus 2 b. We want its perimeter.",
      given("g1", "side = (3a + 2b)", label=True), fig("PYQ_2018_Q37")),
    B("How do we get the perimeter of a square from its side?",
      ask=choose(["4 × side", "2 × side", "side × side"], 0,
                 "A square has 4 equal sides. Walking round, you pass all 4. So the perimeter is 4 times the side.")),
    B("4 times, 3 a plus 2 b. 4 times 3 a is 12 a. 4 times 2 b is 8 b.",
      L("l1", "4(3a + 2b) = 12a + 8b"), arc("l1", "4", "3a", "2b")),
    B("So the perimeter is 12 a plus 8 b. But look at the choices. 12 a plus 8 b is not there! "
      "Do not panic. It may be hiding in another form."),
    B("Open each choice and see. The first one: 2 times, 3 a plus 2 b, is 6 a plus 4 b. "
      "That is only 2 sides, so it is too small.",
      L("l2", "2(3a + 2b) = 6a + 4b")),
    B("Now this one: 2 times, 6 a plus 4 b. What does it open out to?",
      ask=choose(["12a + 8b", "8a + 6b", "12a + 4b"], 0,
                 "The 2 multiplies both parts. 2 times 6 a is 12 a. And 2 times 4 b is 8 b.")),
    B("2 times 6 a is 12 a, and 2 times 4 b is 8 b. That is exactly our perimeter, in disguise.",
      answer("a1", "2(6a + 4b) = 12a + 8b", label=True), arc("a1", "2", "6a", "4b"), mark("a1", "2(6a + 4b)")),
    B("And the choices with 5 a b cannot be right. 3 a and 2 b are different letters, "
      "so they never join into one term."),
    B("Work out your own answer first. If it is not among the choices, open the brackets in each choice "
      "and compare. Here it is 2 times, 6 a plus 4 b."),
])

# Sum of (5m − 3n) and (7m − 2n)   (12m − 5n)
LESSONS["PYQ_2019_Q03"] = lesson([
    B("We need the sum of two expressions: 5 m minus 3 n, and 7 m minus 2 n. Sum means add them.",
      given("g1", "(5m − 3n) + (7m − 2n)", label=True)),
    B("Which terms can be put together?",
      ask=choose(["5m with 7m, 3n with 2n", "5m with 3n, 7m with 2n", "all four into one term"], 0,
                 "Only like terms join, and like terms have the same letter. "
                 "So the m terms go together, and the n terms go together.")),
    B("The m family first. 5 m and 7 m make 12 m.",
      group("g1", ["5m", "7m"], "12m"), L("l1", "5m + 7m = 12m")),
    B("Now the n family. Look at the signs. 3 n is taken away. Then 2 n is taken away as well.",
      under("g1", "− 3n"), under("g1", "− 2n")),
    B("Taking away 3 n, and then taking away 2 n more. Altogether, how much is taken away?",
      ask=choose(["5n", "1n", "6n"], 0,
                 "Think of sweets. I take 3 of your sweets, then 2 more. I have taken 5 altogether. "
                 "So 5 n is taken away.")),
    B("3 n and 2 n are both taken away, so 5 n is taken away in all.", L("l2", "− 3n − 2n = − 5n")),
    B("So the sum is 12 m minus 5 n.", answer("a1", "12m − 5n", label=True), mark("a1", "12m − 5n")),
    B("Test with m as 1 and n as 1. The first bracket is 5 minus 3, which is 2. The second is 7 minus 2, "
      "which is 5. Together 7. And 12 minus 5 is 7.",
      W("l3", "(5 − 3) + (7 − 2) = 7"), W("l4", "12 − 5 = 7")),
    B("Two take aways do not turn into a plus. They make one bigger take away. The sum is 12 m minus 5 n."),
])

# 5p + 6q − 12, when p = 7 and q = p − 3   (47)
LESSONS["PYQ_2019_Q27"] = lesson([
    B("p is 7, and q is p minus 3. We want the value of 5 p, plus 6 q, minus 12.",
      given("g1", "p = 7,  q = p − 3", label=True), given("g2", "5p + 6q − 12", label=True)),
    B("Before we can use q, we need its number. What is q?",
      ask=choose(["4", "3", "10"], 0,
                 "q is p minus 3. And p is 7. So q is 7 minus 3.")),
    B("q is 7 minus 3, which is 4.", W("l1", "7 − 3 = 4"), note("l1", "4", "q")),
    B("Now 5 p. That is 5 times 7, which is 35. Careful: that is only the first part, not the answer.",
      under("g2", "5p"), W("l2", "5 × 7 = 35")),
    B("Next, 6 q. That is 6 times 4, which is 24.", under("g2", "6q"), W("l3", "6 × 4 = 24")),
    B("We have 35 and 24, and there is still the 12. How do they go together?",
      ask=choose(["35 + 24 − 12", "35 × 24 − 12", "35 + 24 + 12"], 0,
                 "Look at the signs in the expression. There is a plus in front of 6 q, and a minus in front of 12. "
                 "So add 24, then take away 12.")),
    B("35 plus 24 is 59. Then 59 minus 12 is 47.",
      W("l4", "35 + 24 = 59"), answer("a1", "59 − 12 = 47"), mark("a1", "47")),
    B("So the value is 47. Find q first, work out each part, then join the parts with their own signs."),
])

# Square of side (4x − 3y) cm. Perimeter?   ((16x − 12y) cm)
LESSONS["PYQ_2019_Q36"] = lesson([
    B("A square. Each side is 4 x minus 3 y centimetres. We want an expression for its perimeter.",
      given("g1", "side = (4x − 3y) cm", label=True), fig("PYQ_2019_Q36")),
    B("A square has 4 equal sides. So its perimeter is 4 times one side.", L("l1", "4(4x − 3y)")),
    B("Look at the 4 outside the bracket. What does it multiply?",
      ask=choose(["both 4x and 3y", "only 4x", "only 3y"], 0,
                 "All four sides are the whole of 4 x minus 3 y. So every part of the side is multiplied by 4.")),
    B("4 times 4 x is 16 x.", arc("l1", "4", "4x"), L("l2", "4 × 4x = 16x")),
    B("And 4 times 3 y is 12 y.", arc("l1", "4", "3y"), L("l3", "4 × 3y = 12y")),
    B("In each side, 3 y is taken away. So in the perimeter, is 12 y added or taken away?",
      ask=choose(["taken away", "added"], 0,
                 "Each of the 4 sides loses 3 y. Four lots of losing 3 y is losing 12 y. So the minus stays.")),
    B("So the perimeter is 16 x minus 12 y centimetres.",
      answer("a1", "(16x − 12y) cm", label=True), mark("a1", "(16x − 12y) cm")),
    B("Test with x as 1 and y as 1. A side is 4 minus 3, which is 1, so the perimeter is 4. "
      "Our answer gives 16 minus 12, also 4.",
      W("l4", "4 × (4 − 3) = 4"), W("l5", "16 − 12 = 4")),
    B("x and y are different letters, so they stay apart. Multiply each by 4, and keep the minus between them."),
])
