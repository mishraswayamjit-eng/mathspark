"""Lessons written by hand: puzzles with several unknowns, and "which is true / greatest / least" questions."""
from algebra_lib import B, W, answer, choose, given, group, lesson, mark, note, strike

LESSONS = {}

# Uncle's Cafe: toast + tea = 4, 2 toast + 2 sandwich = 9, sandwich + 2 tea = 2.
LESSONS["EXT_G5_FP_2016_027"] = lesson([
    B("A cafe puzzle. Toast and tea cost 4 rupees. 2 toasts and 2 sandwiches cost 9. "
      "A sandwich and 2 teas cost 2. We want the cost of one of each.",
      given("l1", "toast + tea = 4", label=True), given("l2", "2 toast + 2 sandwich = 9", label=True),
      given("l3", "sandwich + 2 tea = 2", label=True)),
    B("Look at the middle line. 2 toasts and 2 sandwiches cost 9 rupees. So what do 1 toast and 1 sandwich cost?",
      ask=choose(["Rs. 18", "Rs. 4.50", "Rs. 9"], 1,
                 "Half as much food costs half as much money. Half of 9 rupees is 4 and a half rupees.")),
    B("Half of 9 is 4 and a half. So a toast and a sandwich together cost 4 and a half rupees.",
      W("l4", "9 ÷ 2 = 4.5"), W("l5", "toast + sandwich = 4.5", label=True)),
    B("Compare two lines. Toast and tea cost 4. Toast and sandwich cost 4 and a half. "
      "The toast is the same in both. So which costs more, the sandwich or the tea?",
      ask=choose(["the tea, by half a rupee", "the sandwich, by half a rupee", "they cost the same"], 1,
                 "Only one thing changed: the tea became a sandwich. And the price went up by half a rupee. "
                 "So the sandwich costs half a rupee more than the tea.")),
    B("4 and a half, minus 4, is a half. So a sandwich is a tea plus half a rupee.",
      W("l6", "4.5 − 4 = 0.5"), W("l7", "sandwich = tea + 0.5", label=True)),
    B("Now use the last line: a sandwich and 2 teas cost 2 rupees. Swap the sandwich for a tea plus a half. "
      "That gives 3 teas, plus a half, making 2.",
      note("l3", "sandwich", "tea + 0.5"), W("l8", "3 tea + 0.5 = 2", label=True)),
    B("Take the half away from both sides, and 3 teas cost 1 and a half rupees. "
      "Share that by 3, and one tea costs half a rupee.",
      W("l9", "2 − 0.5 = 1.5"), W("l10", "1.5 ÷ 3 = 0.5"), note("l10", "0.5", "tea", "below")),
    B("A sandwich is half a rupee more than that, so 1 rupee. And toast plus tea is 4, "
      "so the toast is 4 minus a half, which is 3 and a half.",
      W("l11", "0.5 + 0.5 = 1"), W("l12", "4 − 0.5 = 3.5")),
    B("Now add one of each: 3 and a half, plus 1, plus a half. That is 5 rupees.",
      answer("l13", "3.5 + 1 + 0.5 = 5"), mark("l13", ("5", 3))),
    B("Check the middle line. 2 toasts are 7 rupees and 2 sandwiches are 2 rupees. 7 plus 2 is 9. It fits.",
      W("l14", "2 × 3.5 + 2 × 1 = 9")),
    B("So with a puzzle like this: compare two lines that share something, see what changed, "
      "and work out one price at a time."),
])

# Five gifts, total 21. A + B = 6, B + C = 10, C + D = 7, D + E = 9. Find A + E.
LESSONS["EXT_G5_FP_2016_035"] = lesson([
    B("Five gifts, costing 21 rupees in all. And we know four pair totals. We want A and E together.",
      given("l1", "A + B + C + D + E = 21", label=True), given("l2", "A + B = 6,   B + C = 10", label=True),
      given("l3", "C + D = 7,   D + E = 9", label=True)),
    B("Look at two of the pairs: A with B, and C with D. Together they cover four gifts. Which gift is left out?",
      ask=choose(["A", "C", "E"], 2,
                 "A, B, C and D are all inside those two pairs. The only gift not counted is E.")),
    B("So take those two pairs away from the total, and what is left is E. 21 minus 6 minus 7 is 8.",
      group("l1", ["A + B", "C + D"], "6 + 7"), W("l4", "21 − 6 − 7 = 8"), note("l4", "8", "E")),
    B("Now we want A. Which two pairs leave only A out?",
      ask=choose(["A + B and D + E", "B + C and D + E", "B + C and C + D"], 1,
                 "We need two pairs that cover B, C, D and E, with no A in them. "
                 "That is B with C, together with D and E.")),
    B("B and C cost 10, and D and E cost 9. 21 minus 10 minus 9 is 2. So A costs 2 rupees.",
      group("l1", ["B + C", "D + E"], "10 + 9"), W("l5", "21 − 10 − 9 = 2"), note("l5", "2", "A")),
    B("A is 2 and E is 8. Together, 2 plus 8 is 10 rupees.",
      answer("l6", "2 + 8 = 10"), mark("l6", "10")),
    B("Let's check with the others. B is 6 minus 2, which is 4. C is 10 minus 4, which is 6. "
      "D is 7 minus 6, which is 1. And D plus E is 1 plus 8, which is 9. It all fits.",
      W("l7", "6 − 2 = 4"), W("l8", "10 − 4 = 6"), W("l9", "7 − 6 = 1"), W("l10", "1 + 8 = 9")),
    B("When you know a total and some pairs, take away pairs that do not overlap. "
      "Whatever is left out is what you have found."),
])

# Five ages, total 105. A + B = 39, B + C = 40, C + D = 38, D + E = 44. Youngest?
LESSONS["EXT_G5_FP_2017_001"] = lesson([
    B("Five people, and their ages add up to 105. We know four pair totals. "
      "We need the youngest, so we have to find everyone.",
      given("l1", "A + B + C + D + E = 105", label=True), given("l2", "A + B = 39,   B + C = 40", label=True),
      given("l3", "C + D = 38,   D + E = 44", label=True)),
    B("A and B make 39, and C and D make 38. Those two pairs cover four people. Who is left out?",
      ask=choose(["A", "E", "C"], 1,
                 "A, B, C and D are all inside those two pairs. The only person not counted is E.")),
    B("So E is the total, minus those two pairs. 105 minus 39 minus 38 is 28.",
      group("l1", ["A + B", "C + D"], "39 + 38"), W("l4", "105 − 39 − 38 = 28"), note("l4", "28", "E")),
    B("The same trick finds A. B and C make 40, D and E make 44, and only A is left out. "
      "105 minus 40 minus 44 is 21.",
      group("l1", ["B + C", "D + E"], "40 + 44"), W("l5", "105 − 40 − 44 = 21"), note("l5", "21", "A")),
    B("Now we know A is 21. Which fact gives us B straight away?",
      ask=choose(["B + C = 40", "A + B = 39", "D + E = 44"], 1,
                 "We want a fact with B and one other person whose age we already know. "
                 "A and B make 39, and we know A.")),
    B("B is 39 minus 21, which is 18. Then C is 40 minus 18, which is 22. And D is 38 minus 22, which is 16.",
      W("l6", "39 − 21 = 18"), W("l7", "40 − 18 = 22"), W("l8", "38 − 22 = 16")),
    B("Line them up: A is 21, B is 18, C is 22, D is 16 and E is 28. The smallest is 16.",
      W("l9", "A 21,  B 18,  C 22,  D 16,  E 28", label=True), mark("l9", "D 16"),
      answer("l10", "youngest = 16", label=True)),
    B("Check the one pair we did not use. D and E are 16 plus 28, which is 44. Just what the question said.",
      W("l11", "16 + 28 = 44")),
    B("So with a total and some pairs: remove pairs that do not overlap to find one person, "
      "then walk along the chain. The youngest is 16."),
])

# Apples, mangoes, oranges: A + M = 400, M + O = 300, A + O = 440. Sell 100 of each.
LESSONS["EXT_G5_FP_2020_015"] = lesson([
    B("A fruit seller has apples, mangoes and oranges. We know three pair totals. "
      "First we find how many of each he has. Then he sells 100 of each.",
      given("l1", "A + M = 400", label=True), given("l2", "M + O = 300", label=True),
      given("l3", "A + O = 440", label=True)),
    B("Suppose we add all three totals together. How many times does each fruit get counted?",
      ask=choose(["once", "twice", "3 times"], 1,
                 "Look for A in the three lines: it appears in 2 of them. The same is true for M and for O. "
                 "So every fruit is counted twice.")),
    B("The three totals add up to 1140. That counts every fruit twice, so we halve it. "
      "All the fruit together is 570.",
      W("l4", "400 + 300 + 440 = 1140"), W("l5", "1140 ÷ 2 = 570"), W("l6", "A + M + O = 570", label=True)),
    B("All three make 570, and apples with mangoes make 400. Which fruit does that give us?",
      ask=choose(["apples", "mangoes", "oranges"], 2,
                 "Take the apples and mangoes away from all the fruit, and only the oranges are left.")),
    B("So oranges are 570 minus 400, which is 170. In the same way, apples are 570 minus 300, which is 270. "
      "And mangoes are 570 minus 440, which is 130.",
      W("l7", "570 − 400 = 170"), W("l8", "570 − 300 = 270"), W("l9", "570 − 440 = 130")),
    B("Do not stop here! He sells 100 of each. Apples go down to 170, mangoes to 30, and oranges to 70.",
      W("l10", "270 − 100 = 170"), W("l11", "130 − 100 = 30"), W("l12", "170 − 100 = 70")),
    B("So he has 170 apples, 30 mangoes and 70 oranges left.",
      answer("l13", "A = 170, M = 30, O = 70", label=True), mark("l13", "A = 170, M = 30, O = 70", "box")),
    B("Check the starting numbers. 270 apples and 130 mangoes make 400. "
      "130 mangoes and 170 oranges make 300. Both match the question.",
      W("l14", "270 + 130 = 400"), W("l15", "130 + 170 = 300")),
    B("So when every pair total is given: add them all, halve, then subtract each pair. "
      "And finish the story: 170, 30 and 70."),
])

# Sum 92, difference 14. Square of the greater number.
LESSONS["EXT_G5_FP_2025_010"] = lesson([
    B("Two numbers. Add them and we get 92. Subtract them and we get 14. We want the square of the greater one.",
      given("l1", "greater + smaller = 92", label=True), given("l2", "greater − smaller = 14", label=True)),
    B("Here is a neat trick: add the two lines together. What happens to the smaller number?",
      ask=choose(["it doubles", "it cancels out", "nothing changes"], 1,
                 "In the first line the smaller number is added. In the second it is taken away. "
                 "Plus smaller and minus smaller cancel each other.")),
    B("So adding the lines leaves 2 lots of the greater number. And that equals 92 plus 14, which is 106.",
      strike("l1", "+ smaller"), strike("l2", "− smaller"),
      W("l3", "2 × greater = 92 + 14", label=True), W("l4", "92 + 14 = 106")),
    B("Half of 106 is 53. So the greater number is 53.",
      W("l5", "106 ÷ 2 = 53"), note("l5", "53", "greater")),
    B("Quick check. The smaller one is 92 minus 53, which is 39. And 53 minus 39 is 14. Good.",
      W("l6", "92 − 53 = 39"), W("l7", "53 − 39 = 14")),
    B("Is 53 our answer?",
      ask=choose(["Yes, 53", "No: we need 53 × 53", "No: we need 53 × 2"], 1,
                 "The question asks for the square of the greater number. Square means the number times itself.")),
    B("53 times 53. Split it into two easier parts: 53 times 50 is 2650, and 53 times 3 is 159.",
      W("l8", "53 × 50 = 2650"), W("l9", "53 × 3 = 159")),
    B("Add them: 2650 plus 159 is 2809. So 53 squared is 2809.",
      answer("l10", "2650 + 159 = 2809"), mark("l10", "2809")),
    B("When you know a sum and a difference: add them and halve to get the greater number. "
      "Then do exactly what the question asks."),
])

# a = 3, b = 5, c = b − a. Which is greatest?
LESSONS["EXT_G5_FP_2019_005"] = lesson([
    B("We know a is 3 and b is 5, and c is made from them. Then we compare three expressions, "
      "to see which is greatest.",
      given("l1", "a = 3,  b = 5,  c = b − a", label=True)),
    B("c first. c is b minus a, so 5 minus 3, which is 2.",
      W("l2", "5 − 3 = 2"), note("l2", "2", "c")),
    B("Take the first expression: a plus c, in a bracket, times b. With the numbers in, "
      "that is 3 plus 2, times 5. What do we do first?",
      W("l3", "(a + c) × b", label=True), W("l4", "(3 + 2) × 5 = ?"),
      ask=choose(["2 × 5", "3 + 2, the bracket", "3 × 5"], 1,
                 "Brackets always come first. So we add 3 and 2 before we multiply.")),
    B("3 plus 2 is 5, and 5 times 5 is 25.",
      W("l5", "5 × 5 = 25")),
    B("The second one: a plus b, times c. 3 plus 5 is 8, and 8 times 2 is 16.",
      W("l6", "(a + b) × c", label=True), W("l7", "(3 + 5) × 2 = 16")),
    B("The third: b plus c, times a. 5 plus 2 is 7, and 7 times 3 is 21.",
      W("l8", "(b + c) × a", label=True), W("l9", "(5 + 2) × 3 = 21")),
    B("So the three values are 25, 16 and 21. The greatest is 25, and that came from a plus c, times b.",
      answer("l10", "(a + c) × b = 25  is greatest", label=True), mark("l3", "(a + c) × b", "box")),
    B("Notice they are not all equal, even though the same three numbers are used each time. "
      "So: find every letter, put the numbers in, do the brackets first, then compare."),
])

# a = 7, m = a − 2, p = m + 5. Which is least?
LESSONS["EXT_G5_FP_2023_022"] = lesson([
    B("Only a is given. m is built from a, and p is built from m. "
      "So we find them in order, and then compare three expressions.",
      given("l1", "a = 7,  m = a − 2,  p = m + 5", label=True)),
    B("Which letter can we find first?",
      ask=choose(["p", "m", "both at the same time"], 1,
                 "p needs m, and m needs a. We know a, so m comes first.")),
    B("m is 7 minus 2, which is 5. Then p is 5 plus 5, which is 10.",
      W("l2", "7 − 2 = 5"), note("l2", "5", "m"), W("l3", "5 + 5 = 10"), note("l3", "10", "p")),
    B("First expression: m plus p is 15, and 15 times 7 is 105.",
      W("l4", "(m + p) × a", label=True), W("l5", "(5 + 10) × 7 = 15 × 7"), W("l6", "15 × 7 = 105")),
    B("Second: p plus a is 17, and 17 times 5 is 85.",
      W("l7", "(p + a) × m", label=True), W("l8", "(10 + 7) × 5 = 17 × 5"), W("l9", "17 × 5 = 85")),
    B("Third: a plus m is 12, and 12 times 10 is 120.",
      W("l10", "(a + m) × p", label=True), W("l11", "(7 + 5) × 10 = 12 × 10"), W("l12", "12 × 10 = 120")),
    B("We have 105, 85 and 120. Careful now: what does the question want?",
      ask=choose(["the greatest value", "the least value"], 1,
                 "Read the question again. It asks which one has the least value, so we want the smallest.")),
    B("The smallest is 85, and that came from p plus a, times m.",
      answer("l13", "(p + a) × m = 85  is least", label=True), mark("l7", "(p + a) × m", "box")),
    B("So: find the letters in order, work out each expression with the bracket first, "
      "and check whether the question wants the greatest or the least."),
])

# p = 7, q = 2p − 9. Which is greatest?
LESSONS["EXT_G5_FP_2025_017"] = lesson([
    B("p is 7, and q is built from p. Then there are four expressions, and we want the one with the greatest value.",
      given("l1", "p = 7,  q = 2p − 9", label=True)),
    B("First q. It is 2 p minus 9. What is 2 p when p is 7?",
      ask=choose(["the number 27", "2 × 7 = 14", "2 + 7 = 9"], 1,
                 "A number next to a letter means times. 2 p is 2 times 7, which is 14.")),
    B("So q is 14 minus 9, which is 5.",
      W("l2", "2 × 7 − 9 = 5"), note("l2", "5", "q")),
    B("Now the first expression. 2 p is 14 and 3 q is 15. "
      "14 minus 15 dips 1 below zero, and plus 5 brings us up to 4.",
      W("l3", "A:  2p − 3q + 5", label=True), W("l4", "14 − 15 + 5 = 4")),
    B("The second. 4 q is 20 and 2 p is 14. 20 minus 14 is 6.",
      W("l5", "B:  4q − 2p", label=True), W("l6", "20 − 14 = 6")),
    B("The third. 7 plus 5 is 12, and 12 minus 12 is 0.",
      W("l7", "C:  p + q − 12", label=True), W("l8", "7 + 5 − 12 = 0")),
    B("The last one. 7 q is 35, and 5 p is also 35. They cancel each other, and 3 is left.",
      W("l9", "D:  7q − 5p + 3", label=True), W("l10", "35 − 35 + 3 = 3")),
    B("The four values are 4, 6, 0 and 3. Which expression wins?",
      ask=choose(["2p − 3q + 5", "4q − 2p", "7q − 5p + 3"], 1,
                 "The greatest of 4, 6, 0 and 3 is 6. And 6 came from 4 q minus 2 p.")),
    B("So 4 q minus 2 p has the greatest value, 6.",
      answer("l11", "4q − 2p = 6  is greatest", label=True), mark("l5", "4q − 2p", "box")),
    B("Find the missing letter first, work out each expression carefully, and only then compare."),
])

# For Z = 7, which equation is true?
LESSONS["EXT_G5_FP_2022_018"] = lesson([
    B("We are told Z is 7. One of these equations may be true for that Z. "
      "An equation is true when both of its sides come out the same.",
      given("l1", "Z = 7", label=True)),
    B("So how do we test each one?",
      ask=choose(["solve each one for Z", "put 7 in on one side only", "put 7 in for Z on both sides"], 2,
                 "We put 7 in place of every Z, on the left and on the right, "
                 "and then see whether the two sides match.")),
    B("A first. The left side is 5, plus 2 times 7, which is 19. The right side is 3 times 7, plus 2, which is 23. "
      "Not the same, so A is out.",
      W("a0", "A:  5 + 2Z = 3Z + 2", label=True), W("a1", "5 + 2 × 7 = 19"), W("a2", "3 × 7 + 2 = 23"),
      strike("a0", "5 + 2Z = 3Z + 2")),
    B("Now B. The left side is 5 times 7, plus 6, which is 41. What is the right side, 7 Z minus 8?",
      W("b0", "B:  5Z + 6 = 7Z − 8", label=True), W("b1", "5 × 7 + 6 = 41"),
      ask=choose(["57", "41", "49"], 1,
                 "7 Z is 7 times 7, which is 49. Take away 8 and we get 41.")),
    B("7 times 7 is 49, and 49 minus 8 is 41. Both sides are 41. B is true!",
      W("b2", "7 × 7 − 8 = 41"), mark("b0", "5Z + 6 = 7Z − 8", "box")),
    B("Let's be sure about C. The left side is 35 and the right side is 42. Not equal.",
      W("c0", "C:  4Z + 7 = 2Z + 28", label=True), W("c1", "4 × 7 + 7 = 35"), W("c2", "2 × 7 + 28 = 42"),
      strike("c0", "4Z + 7 = 2Z + 28")),
    B("So the true equation is 5 Z plus 6 equals 7 Z minus 8.",
      answer("l9", "5Z + 6 = 7Z − 8", label=True), mark("l9", "5Z + 6 = 7Z − 8")),
    B("To test an equation, put the number in on both sides and compare. Equal sides mean it is true."),
])

# For d = 6, which is true?
LESSONS["EXT_G5_FP_2024_012"] = lesson([
    B("d is 6. We must find which statement is true. "
      "True means the left side and the right side are worth the same.",
      given("l1", "d = 6", label=True)),
    B("Put 6 in place of d on both sides. For A, the left is 5 times 6, plus 19, which is 49. "
      "The right is 7 times 6, minus 17, which is 25. Nowhere near.",
      W("a0", "A:  5d + 19 = 7d − 17", label=True), W("a1", "5 × 6 + 19 = 49"), W("a2", "7 × 6 − 17 = 25"),
      strike("a0", "5d + 19 = 7d − 17")),
    B("Now B. The left side is 8, plus 4 times 6, which is 32. What is the right side, 6 d minus 6?",
      W("b0", "B:  8 + 4d = 6d − 6", label=True), W("b1", "8 + 4 × 6 = 32"),
      ask=choose(["60", "30", "32"], 1,
                 "6 d means 6 times 6. Take 6 away from that, and we get 30.")),
    B("The right side is 30, but the left side was 32. Close, but not equal. B is out.",
      W("b2", "6 × 6 − 6 = 30"), strike("b0", "8 + 4d = 6d − 6")),
    B("Now C. The left is 12 times 6, minus 14, which is 58. "
      "The right is 16, plus 7 times 6, which is also 58. They match!",
      W("c0", "C:  12d − 14 = 16 + 7d", label=True), W("c1", "12 × 6 − 14 = 58"), W("c2", "16 + 7 × 6 = 58"),
      mark("c0", "12d − 14 = 16 + 7d", "box")),
    B("So the true statement is 12 d minus 14 equals 16 plus 7 d.",
      answer("l9", "12d − 14 = 16 + 7d", label=True), mark("l9", "12d − 14 = 16 + 7d")),
    B("One of them worked, so we do not need none of these. "
      "But we only knew that because we tested every one."),
    B("To check whether a statement is true: put the number in on both sides, work each side out, and compare."),
])
