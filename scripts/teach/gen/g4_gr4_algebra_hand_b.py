"""Lessons written one by one: newly written questions G4A_ALGEBRA_001 to 016."""
from g4_gr4_algebra_lib import (B, L, T, W, answer, arc, box, choose, fig, given, group, lesson, mark, note, strike,
                                under)

LESSONS = {}

# Meera had ₹p. 3 pencils at ₹q each. Money left?   (p − 3q)
LESSONS["G4A_ALGEBRA_001"] = lesson([
    B("Meera had p rupees. She bought 3 pencils, and each one cost q rupees. "
      "We want an expression for the money she has left.",
      given("g1", "had: ₹p,   3 pencils at ₹q each", label=True), fig("G4A_ALGEBRA_001")),
    B("First, how much did the 3 pencils cost altogether?",
      ask=choose(["3q", "q + 3", "3p"], 0,
                 "One pencil costs q. Three pencils cost q plus q plus q. That is 3 times q, which we write as 3 q.")),
    B("q, and q, and q again. Three lots of q is 3 q rupees. That is what she spent.",
      L("l1", "q + q + q = 3q"), note("l1", "3q", "spent")),
    B("Money left is the money she had, take away the money she spent.", L("l2", "left = had − spent")),
    B("She had p and she spent 3 q. Which expression is the money left?",
      ask=choose(["p − 3q", "3p − q", "p − q − 3"], 0,
                 "The 3 belongs to the pencils, so it sits with q, not with p. "
                 "Her own money p is counted just once. So it is p minus 3 q.")),
    B("So she has p minus 3 q rupees left.", answer("a1", "p − 3q", label=True), mark("a1", "p − 3q")),
    B("Test it. Say she had 50 rupees and each pencil cost 10. Three pencils cost 30, and 50 minus 30 leaves 20.",
      W("l3", "50 − 3 × 10 = 50 − 30 = 20")),
    B("The number of things multiplies the price of one. Then take that from the money she had: p minus 3 q."),
])

# r runs, then 40 fewer. Total?   (2r − 40)
LESSONS["G4A_ALGEBRA_002"] = lesson([
    B("A team scored r runs in the first innings. In the second innings it scored 40 runs fewer. "
      "We want the total for both innings.",
      given("g1", "first innings: r,   second: 40 fewer", label=True), fig("G4A_ALGEBRA_002")),
    B("The second innings was 40 runs fewer than the first. How do we write that?",
      ask=choose(["r − 40", "r + 40", "40 − r"], 0,
                 "Fewer means less. So we start from the first score, r, and take 40 away from it.")),
    B("Fewer means take away. So the second innings is r minus 40.", L("l1", "second innings = r − 40")),
    B("Careful: r minus 40 is only the second innings. The question wants the total of both.",
      under("l1", "r − 40")),
    B("Total means add. So we write r, plus r minus 40.", W("l2", "r + r − 40")),
    B("Look at r plus r. What is that?",
      ask=choose(["2r", "r", "rr"], 0,
                 "One r and another r make two r's. We write that as 2 r.")),
    B("Two r's make 2 r. The 40 is taken away just once, because only one innings was 40 fewer.",
      group("l2", [T("r", 1), T("r", 2)], "2r"), answer("a1", "r + r − 40 = 2r − 40"), mark("a1", "2r − 40")),
    B("Test it. If the first score was 100, the second was 60. Together that is 160. "
      "And 2 times 100, minus 40, is 160 too.",
      W("l3", "100 + 60 = 160"), W("l4", "2 × 100 − 40 = 160")),
    B("Write each part with the letter, then add. The total is 2 r minus 40."),
], "r", 40)

# Simplify: 7a + 3b − 2a + b   (5a + 4b)
LESSONS["G4A_ALGEBRA_003"] = lesson([
    B("Four terms here. Some have an a, and some have a b. Simplify means join the ones that belong together.",
      given("g1", "7a + 3b − 2a + b", label=True)),
    B("Which terms belong to the a family?",
      ask=choose(["7a and 2a", "7a and 3b", "3b and 2a"], 0,
                 "Look at the letter, not the number. 7 a and 2 a both carry an a. Those are like terms.")),
    B("The a family: 7 a, and then minus 2 a. The minus sign in front of 2 a belongs to it. 7 a minus 2 a is 5 a.",
      group("g1", ["7a", "− 2a"], "5a"), L("l1", "7a − 2a = 5a")),
    B("Now the b family: 3 b plus b. A b standing on its own, how many b's is that?",
      ask=choose(["1", "0", "3"], 0,
                 "A letter standing alone is one of that letter. We just do not bother to write the 1. "
                 "So b means 1 b.")),
    B("b on its own is 1 b. So 3 b plus 1 b is 4 b.",
      group("g1", ["3b", "+ b"], "4b"), L("l2", "3b + b = 4b")),
    B("a and b are different hidden numbers, so 5 a and 4 b cannot be joined. They stay side by side.",
      answer("a1", "5a + 4b", label=True), mark("a1", "5a + 4b")),
    B("Test it with a as 1 and b as 1. The long one is 7 plus 3 minus 2 plus 1, which is 9. "
      "The short one is 5 plus 4, also 9.",
      W("l3", "7 + 3 − 2 + 1 = 9"), W("l4", "5 + 4 = 9")),
    B("Collect each letter on its own, and keep every sign with its own term. That gave us 5 a plus 4 b."),
])

# The odd numbers in order are 1, 3, 5, 7, ... nth odd number?   (2n − 1)
LESSONS["G4A_ALGEBRA_004"] = lesson([
    B("The odd numbers go 1, 3, 5, 7 and on. We want a rule that gives the odd number in any position. "
      "The letter n stands for the position.",
      given("g1", "odd numbers:  1, 3, 5, 7, ...", label=True), fig("G4A_ALGEBRA_004")),
    B("Start with something easier: the even numbers. The 1st is 2, the 2nd is 4, the 3rd is 6.",
      L("l1", "even numbers:  2, 4, 6, 8, ...")),
    B("What is the rule for the even number in position n?",
      ask=choose(["2n", "n + 2", "n + 1"], 0,
                 "Each even number is double its position. The 3rd is 6, which is 2 times 3. "
                 "So the nth one is 2 times n.")),
    B("Each even number is 2 times its position. So the nth even number is 2 n.",
      L("l2", "nth even number = 2n")),
    B("Now look at the odd numbers above the even ones. 1 sits above 2. 3 sits above 4. 5 sits above 6. "
      "Each odd number is 1 less.",
      under("g1", "1, 3, 5, 7"), under("l1", "2, 4, 6, 8")),
    B("So the nth odd number is 1 less than 2 n. How do we write that?",
      ask=choose(["2n − 1", "2n + 1", "n − 1"], 0,
                 "1 less means take 1 away. So start from 2 n and take away 1.")),
    B("So the rule is 2 n minus 1.",
      answer("a1", "nth odd number = 2n − 1", label=True), mark("a1", "2n − 1")),
    B("A good rule must fit every position, so we test more than one. For n as 1: 2 times 1, minus 1, is 1. "
      "For n as 4: 2 times 4, minus 1, is 7. Both fit.",
      W("l3", "2 × 1 − 1 = 1"), W("l4", "2 × 4 − 1 = 7")),
    B("Here is the trap. 3 n minus 2 also gives 1 when n is 1. But for n as 2 it gives 4, and 4 is not odd. "
      "One test is never enough.",
      W("l5", "3 × 2 − 2 = 4")),
    B("So the nth odd number is 2 n minus 1. Double the position, then take away 1."),
])

# Isosceles triangle: (2a + 3), (2a + 3), (a − 2). Perimeter?   ((5a + 4) cm)
LESSONS["G4A_ALGEBRA_005"] = lesson([
    B("An isosceles triangle has two equal sides. Here each one is 2 a plus 3 centimetres. "
      "The third side is a minus 2 centimetres. We want the perimeter.",
      given("g1", "sides: (2a + 3), (2a + 3), (a − 2)", label=True), fig("G4A_ALGEBRA_005")),
    B("Perimeter is the distance all the way round. How many sides do we add?",
      ask=choose(["all 3 sides", "the 2 different sides", "only the equal sides"], 0,
                 "Walk all the way round the triangle. You pass every side once, and there are 3 of them. "
                 "So the equal side is counted twice.")),
    B("So we add all three. 2 a plus 3, then 2 a plus 3 again, then a minus 2.",
      W("l1", "(2a + 3) + (2a + 3) + (a − 2)")),
    B("Gather the a terms first. 2 a, and 2 a, and one more a. That is 5 a.",
      group("l1", [T("2a", 1), T("2a", 2), T("a", 3)], "5a"), W("l2", "2a + 2a + a = 5a")),
    B("Now the plain numbers: 3, and 3, and the 2 from a minus 2. What do they come to?",
      ask=choose(["4", "8", "1"], 0,
                 "The third side is a minus 2, so the 2 is taken away, not added. "
                 "3 plus 3 is 6, and 6 minus 2 is 4.")),
    B("3 plus 3 is 6, and then minus 2 leaves 4. The minus sign travels with its 2.", W("l3", "3 + 3 − 2 = 4")),
    B("So the perimeter is 5 a plus 4 centimetres.", answer("a1", "5a + 4"), mark("a1", "5a + 4")),
    B("Add every side, letters with letters and numbers with numbers. And keep each sign with its own number."),
], "a", 5)

# Garden p long, q wide, one long side along a wall. Fence?   ((p + 2q) m)
LESSONS["G4A_ALGEBRA_006"] = lesson([
    B("A garden is a rectangle, p metres long and q metres wide. One long side is along a wall. "
      "A fence goes round the rest. How long is the fence?",
      given("g1", "long sides: p m,   short sides: q m", label=True), fig("G4A_ALGEBRA_006")),
    B("A rectangle has 4 sides. How many of them need a fence?",
      ask=choose(["3", "4", "2"], 0,
                 "One long side is along the wall, and the wall does the job there. "
                 "So the fence runs along the other 3 sides.")),
    B("One long side is the wall. So the fence goes along the other long side, and both short sides.",
      L("l1", "fence = long + short + short")),
    B("Now in letters. Which three sides are fenced?",
      ask=choose(["p, q and q", "p, p and q", "p and q"], 0,
                 "The wall takes the place of a long side, and the long sides are p. So only one p is left. "
                 "Both short sides, q and q, still need a fence.")),
    B("One long side is p. The two short sides are q and q.", L("l2", "p + q + q")),
    B("q plus q is 2 q. So the fence is p plus 2 q metres.",
      group("l2", [T("q", 1), T("q", 2)], "2q"), answer("a1", "(p + 2q) m", label=True), mark("a1", "(p + 2q) m")),
    B("Try it with numbers. If the garden is 9 metres long and 4 metres wide, "
      "the fence is 9 plus 4 plus 4, which is 17 metres.",
      W("l3", "9 + 4 + 4 = 17")),
    B("The whole way round would be 2 p plus 2 q. But the wall saves us one p. So the fence is p plus 2 q."),
])

# If a = 6 and b = 4, what is the value of 3a − 2b + ab?   (34)
LESSONS["G4A_ALGEBRA_007"] = lesson([
    B("a is 6 and b is 4. We want the value of 3 a, minus 2 b, plus a b. Three parts, so we take them one by one.",
      given("g1", "a = 6, b = 4", label=True), given("g2", "3a − 2b + ab", label=True)),
    B("3 a is 3 times 6, which is 18. And 2 b is 2 times 4, which is 8.",
      under("g2", "3a"), under("g2", "2b"), W("l1", "3 × 6 = 18"), W("l2", "2 × 4 = 8")),
    B("Now the last part, a b. Two letters side by side. What does a b mean here?",
      ask=choose(["6 × 4", "6 + 4", "the number 64"], 0,
                 "Letters side by side have a hidden times sign between them, just like a number next to a letter. "
                 "So a b is 6 times 4.")),
    B("a b is 6 times 4, which is 24.", under("g2", "ab"), W("l3", "6 × 4 = 24")),
    B("Now put the three parts back, each with its own sign. 18, minus 8, plus 24.", W("l4", "18 − 8 + 24")),
    B("Look at the sign in front of the 8. What do we do with the 8?",
      ask=choose(["take it away", "add it"], 0,
                 "The sign in front of 2 b is a minus. So the 8 is taken away from the 18.")),
    B("Left to right. 18 minus 8 is 10. Then 10 plus 24 is 34.",
      answer("a1", "18 − 8 + 24 = 34"), mark("a1", "34")),
    B("So the value is 34. Side by side always means times, for a number with a letter and for two letters."),
])

# 30th odd number minus 12th even number   (35)
LESSONS["G4A_ALGEBRA_008"] = lesson([
    B("We are given two rules. The nth odd number is 2 n minus 1. The nth even number is 2 n. "
      "How much more is the 30th odd number than the 12th even number?",
      given("g1", "nth odd number = 2n − 1", label=True), given("g2", "nth even number = 2n", label=True)),
    B("Can we just take 12 away from 30?",
      ask=choose(["No, find the two numbers first", "Yes, 30 − 12"], 0,
                 "30 and 12 are only positions, like places in a queue. We need the numbers standing in those places. "
                 "So we use the rules first.")),
    B("The 30th odd number. Put 30 in place of n. 2 times 30 is 60, and 60 minus 1 is 59.",
      note("g1", T("n", 3), "30"), W("l1", "2 × 30 − 1 = 60 − 1 = 59")),
    B("Notice it is 59, not 60. An odd number is 1 less than double its position. Never 1 more.",
      box("l1", "59")),
    B("The 12th even number. Put 12 in place of n. 2 times 12 is 24.",
      note("g2", T("n", 4), "12"), W("l2", "2 × 12 = 24")),
    B("How much more is 59 than 24? Which sum tells us?",
      ask=choose(["59 − 24", "59 + 24", "30 − 12"], 0,
                 "How much more means the gap between the two numbers. We find a gap by taking the smaller from the bigger.")),
    B("59 minus 24 is 35.", answer("a1", "59 − 24 = 35"), mark("a1", "35")),
    B("So the 30th odd number is 35 more. Use each rule to find the real number first, then compare."),
])

# Anu x, father 4 more than three times. Sum after 5 years?   (4x + 14)
LESSONS["G4A_ALGEBRA_009"] = lesson([
    B("Anu is x years old. Her father's age is 4 years more than three times Anu's age. "
      "We want the sum of their ages after 5 years.",
      given("g1", "Anu: x years", label=True), given("g2", "Father: 4 more than 3 times Anu", label=True),
      fig("G4A_ALGEBRA_009")),
    B("First, the father's age now. 4 more than three times x. Which is it?",
      ask=choose(["3x + 4", "4x + 3", "3(x + 4)"], 0,
                 "Three times x is 3 x. Then 4 more means add 4 after that. So it is 3 x plus 4.")),
    B("Three times x is 3 x, and 4 more makes 3 x plus 4. That is the father today.",
      W("l1", "3x + 4"), note("l1", "3x + 4", "father now")),
    B("Now jump ahead 5 years. Anu will be x plus 5.", W("l2", "x + 5"), note("l2", "x + 5", "Anu in 5 years")),
    B("Who else gets 5 years older?",
      ask=choose(["her father too", "only Anu", "nobody else"], 0,
                 "Time passes for everyone. If Anu is 5 years older, her father is 5 years older as well.")),
    B("The father gains 5 years too. 3 x plus 4, plus 5, is 3 x plus 9.", W("l3", "3x + 4 + 5 = 3x + 9")),
    B("Now add the two ages. x plus 3 x is 4 x. And 5 plus 9 is 14.",
      W("l4", "x + 5 + 3x + 9"), group("l4", [T("x", 1), "3x"], "4x"), group("l4", ["+ 5", "+ 9"], "14"),
      answer("a1", "4x + 14"), mark("a1", "4x + 14")),
    B("So the sum will be 4 x plus 14. The trap was the 5 years. "
      "Two people each grow 5 years older, so the sum grows by 10."),
], "x", 4)

# Three numbers one after another, smallest n. Sum?   (3n + 3)
LESSONS["G4A_ALGEBRA_010"] = lesson([
    B("Three numbers come one after another, like 4, 5, 6. The smallest is n. We want the sum of all three.",
      given("g1", "three numbers in a row, smallest n", label=True), fig("G4A_ALGEBRA_010")),
    B("If the smallest is n, what is the next number?",
      ask=choose(["n + 1", "n", "2n"], 0,
                 "The next number is always 1 more. After 4 comes 4 plus 1. So after n comes n plus 1.")),
    B("The next is n plus 1. And the one after that is 1 more again: n plus 2.",
      L("l1", "n,    n + 1,    n + 2")),
    B("Now add all three together.", W("l2", "n + n + 1 + n + 2")),
    B("How many n's are there in that sum?",
      ask=choose(["3", "1", "2"], 0,
                 "Every one of the three numbers has an n inside it. Count them on the board: n, n, and n.")),
    B("Three n's make 3 n. The plain numbers, 1 and 2, make 3. So the sum is 3 n plus 3.",
      group("l2", [T("n", 1), T("n", 2), T("n", 3)], "3n"), group("l2", ["+ 1", "+ 2"], "3"),
      answer("a1", "3n + 3"), mark("a1", "3n + 3")),
    B("Test it with 4, 5 and 6. Their sum is 15. And 3 times 4, plus 3, is 15 too.",
      W("l3", "4 + 5 + 6 = 15"), W("l4", "3 × 4 + 3 = 15")),
    B("Write each number using n first. Then add the letters and the numbers on their own. "
      "That gives 3 n plus 3."),
], "n", 3)

# Taxi: ₹50 first km, ₹12 each km after. Fare for d km?   (12d + 38)
LESSONS["G4A_ALGEBRA_011"] = lesson([
    B("A taxi charges 50 rupees for the first kilometre, and 12 rupees for every kilometre after that. "
      "We want the fare for a ride of d kilometres.",
      given("g1", "first km: ₹50,   each km after: ₹12", label=True), fig("G4A_ALGEBRA_011")),
    B("Try a short ride first. For 2 kilometres: 50 for the first, then 12 for one more. That is 62 rupees.",
      W("l1", "50 + 12 = 62")),
    B("Now a ride of d kilometres. The first one costs 50. How many kilometres are left at 12 rupees each?",
      ask=choose(["d − 1", "d", "d + 1"], 0,
                 "The first kilometre has its own price, so it is not charged again at 12. "
                 "Take that 1 kilometre away from d. That leaves d minus 1.")),
    B("d minus 1 kilometres, at 12 rupees each. That costs 12 times, d minus 1.", W("l2", "12(d − 1)")),
    B("Open the bracket. 12 times d is 12 d. 12 times 1 is 12. So that part is 12 d minus 12.",
      arc("l2", "12", "d", T("1", 2)), W("l3", "12(d − 1) = 12d − 12")),
    B("Now add the 50 for the first kilometre. 50 minus 12 is 38.",
      W("l4", "50 + 12d − 12"), W("l5", "50 − 12 = 38")),
    B("So the fare is 12 d plus 38 rupees.", answer("a1", "12d + 38"), mark("a1", "12d + 38")),
    B("Check with our 2 kilometre ride. 12 times 2 is 24, and 24 plus 38 is 62. The same as before!",
      W("l6", "12 × 2 + 38 = 24 + 38 = 62")),
    B("The trap is to charge 12 for all d kilometres and then 50 on top. "
      "The first kilometre is paid for only once. That is why we get 12 d plus 38."),
], "d", 12)

# Riya 3 boxes + 5, Sameer 2 boxes + 4, Riya gives one box. Sameer has how many more?   (m − 1)
LESSONS["G4A_ALGEBRA_012"] = lesson([
    B("Each box holds m mangoes. Riya has 3 boxes and 5 loose mangoes. Sameer has 2 boxes and 4 loose ones. "
      "Then Riya gives one full box to Sameer.",
      given("g1", "Riya: 3 boxes + 5,   Sameer: 2 boxes + 4", label=True), fig("G4A_ALGEBRA_012")),
    B("After the box moves, how many boxes does each child have?",
      ask=choose(["Riya 2, Sameer 3", "Riya 3, Sameer 2", "Riya 2, Sameer 2"], 0,
                 "Riya gives one away, so her 3 boxes become 2. Sameer gets it, so his 2 boxes become 3. "
                 "The loose mangoes do not move.")),
    B("Riya now has 2 boxes and 5 loose: 2 m plus 5. Sameer has 3 boxes and 4 loose: 3 m plus 4.",
      L("l1", "Riya: 2m + 5"), L("l2", "Sameer: 3m + 4")),
    B("How many more does Sameer have? To find how many more, we take Riya's from Sameer's.",
      W("l3", "(3m + 4) − (2m + 5)")),
    B("Compare the boxes first. 3 m take away 2 m leaves one box, which is m.", W("l4", "3m − 2m = m")),
    B("Now the loose mangoes. Sameer has 4 and Riya has 5. Who has more loose ones?",
      ask=choose(["Riya, by 1", "Sameer, by 1", "they are equal"], 0,
                 "5 is more than 4. So in loose mangoes Riya is 1 ahead, and that takes 1 off Sameer's lead.")),
    B("So Sameer is ahead by a whole box, m, but behind by 1 loose mango. Altogether he has m minus 1 more.",
      answer("a1", "(3m + 4) − (2m + 5) = m − 1"), mark("a1", "m − 1")),
    B("Test it. If a box holds 10, Riya has 25 and Sameer has 34. And 34 minus 25 is 9, which is 10 minus 1.",
      W("l5", "2 × 10 + 5 = 25"), W("l6", "3 × 10 + 4 = 34"), W("l7", "34 − 25 = 9")),
    B("Write what each child has after the move, then subtract. Sameer has m minus 1 more."),
], "m", 1)

# n even. 5th odd number after n?   (n + 9)
LESSONS["G4A_ALGEBRA_013"] = lesson([
    B("The letter n stands for an even number. We want the 5th odd number that comes after it.",
      given("g1", "n is an even number", label=True)),
    B("Let's try it with a real even number first. Say n is 10. "
      "The odd numbers after 10 are 11, 13, 15, 17 and 19.",
      L("l1", "after 10:   11, 13, 15, 17, 19")),
    B("Look at the very first jump, from 10 to 11. How big is it?",
      ask=choose(["1", "2"], 0,
                 "10 is even, and the very next number, 11, is already odd. So the first jump is only 1. "
                 "After that, the jumps are 2.")),
    B("The first jump is just 1, because the number right after an even number is odd. "
      "Then the odd numbers go up in twos.",
      L("l2", "n + 1,  n + 3,  n + 5,  n + 7,  n + 9"), under("l2", "n + 1")),
    B("Count along the list. Which one is the 5th?",
      ask=choose(["n + 9", "n + 10", "n + 5"], 0,
                 "Point at each one and count: 1st, 2nd, 3rd, 4th, 5th. The 5th in the list is n plus 9.")),
    B("The 5th one is n plus 9.", mark("l2", "n + 9"), answer("a1", "n + 9", label=True)),
    B("Check with our 10. The 5th odd number after 10 was 19. And 10 plus 9 is 19.", W("l3", "10 + 9 = 19")),
    B("The trap is to make 5 jumps of 2, which gives n plus 10. "
      "But the first jump from an even number is only 1. So the answer is n plus 9."),
])

# Square of side (3a + 6) cm, same wire bent into a triangle with equal sides.   ((4a + 8) cm)
LESSONS["G4A_ALGEBRA_014"] = lesson([
    B("A wire is bent into a square. Each side is 3 a plus 6 centimetres. "
      "Then the same wire is bent into a triangle with three equal sides. How long is each side of the triangle?",
      given("g1", "square: each side (3a + 6) cm", label=True), fig("G4A_ALGEBRA_014")),
    B("The wire is bent into a new shape. What stays the same?",
      ask=choose(["the length of the wire", "the length of each side", "the number of sides"], 0,
                 "Bending does not stretch the wire or cut it. So the whole length stays the same. "
                 "Only the shape changes.")),
    B("So first we find the whole wire. It goes round the square, and a square has 4 equal sides.",
      L("l1", "wire = 4 sides of the square")),
    B("4 times, 3 a plus 6. The 4 multiplies both parts. 4 times 3 a is 12 a. 4 times 6 is 24. "
      "So the wire is 12 a plus 24 centimetres long.",
      W("l2", "4 × (3a + 6) = 12a + 24"), arc("l2", "4", "3a", "6")),
    B("The triangle has 3 equal sides, made from this whole wire. How do we find one side?",
      ask=choose(["divide the wire by 3", "multiply the wire by 3", "divide one square side by 3"], 0,
                 "The whole wire is shared equally among the 3 sides of the triangle. "
                 "Sharing equally means dividing by 3.")),
    B("Share each part by 3. 12 a divided by 3 is 4 a. And 24 divided by 3 is 8.",
      W("l3", "12a ÷ 3 = 4a"), W("l4", "24 ÷ 3 = 8")),
    B("So each side of the triangle is 4 a plus 8 centimetres.",
      answer("a1", "(12a + 24) ÷ 3 = 4a + 8"), mark("a1", "4a + 8")),
    B("Same wire, same total length. Find the total first, then share it among the sides of the new shape."),
], "a", 4)

# If 2x + y = 10, what is the value of 6x + 3y − 4?   (26)
LESSONS["G4A_ALGEBRA_015"] = lesson([
    B("We are told that 2 x plus y is 10. We want 6 x plus 3 y, minus 4. "
      "But we do not know x or y on their own!",
      given("g1", "2x + y = 10", label=True), given("g2", "6x + 3y − 4", label=True), fig("G4A_ALGEBRA_015")),
    B("That is fine. Look for the first expression hiding inside the second one. "
      "Compare 2 x with 6 x, and y with 3 y.",
      under("g2", "6x"), under("g2", "3y")),
    B("6 x is how many times 2 x?",
      ask=choose(["3 times", "4 times", "6 times"], 0,
                 "2 x, and 2 x, and 2 x make 6 x. That is 3 lots. And y has become 3 y, which is 3 lots too.")),
    B("Both parts are 3 times as big. So 6 x plus 3 y is 3 lots of, 2 x plus y.",
      L("l1", "6x + 3y = 3 × (2x + y)")),
    B("And we know that 2 x plus y is 10. So 3 lots of it is 3 times 10, which is 30.",
      W("l2", "3 × 10 = 30")),
    B("Is 30 our final answer?",
      ask=choose(["No, take away 4 first", "Yes, it is 30"], 0,
                 "30 is only 6 x plus 3 y. The expression we want has a minus 4 at the end. One small step is left.")),
    B("30 minus 4 is 26.", under("g2", "− 4"), answer("a1", "30 − 4 = 26"), mark("a1", "26")),
    B("So the value is 26. We never found x or y. We spotted the whole of 2 x plus y, three times over, "
      "and used it as one block."),
])

# p odd. Which is always a multiple of 4?   (2p + 2)
LESSONS["G4A_ALGEBRA_016"] = lesson([
    B("p stands for an odd number. We want the expression that is always a multiple of 4. "
      "The key word is always. It must work for every odd number, not just one.",
      given("g1", "p is an odd number", label=True)),
    B("Let's test with p as 1. p plus 3 gives 4. And 2 p plus 2 gives 4 as well. Both are multiples of 4, so far.",
      W("l1", "1 + 3 = 4"), note("l1", "1 + 3", "p + 3"), W("l2", "2 × 1 + 2 = 4"), note("l2", "2 × 1 + 2", "2p + 2")),
    B("Still with p as 1: 4 p plus 2 gives 6, and 2 p gives 2. Neither is a multiple of 4. Those two are out.",
      W("l3", "4 × 1 + 2 = 6"), note("l3", "4 × 1 + 2", "4p + 2"), W("l4", "2 × 1 = 2"), note("l4", "2 × 1", "2p")),
    B("Two are left: p plus 3, and 2 p plus 2. Both gave 4. Can we stop here?",
      ask=choose(["No, test another odd number", "Yes, pick either one"], 0,
                 "Always means every time. One test cannot show that. So we try the next odd number, 3.")),
    B("Try p as 3. p plus 3 is 6. That is not a multiple of 4, so it is out. "
      "2 p plus 2 is 8, and 8 is a multiple of 4.",
      W("l5", "3 + 3 = 6"), strike("l1", "1 + 3 = 4"), W("l6", "2 × 3 + 2 = 8")),
    B("Why does it always work? 2 p plus 2 is 2 lots of, p plus 1. p is odd, so p plus 1 is even. "
      "And double an even number is always a multiple of 4.",
      L("l7", "2p + 2 = 2 × (p + 1)")),
    B("So the one that is always a multiple of 4 is 2 p plus 2.",
      answer("a1", "2p + 2", label=True), mark("a1", "2p + 2")),
    B("When a question says always, test more than one number. One lucky fit is not proof."),
])
