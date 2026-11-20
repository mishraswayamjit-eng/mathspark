"""Lessons written one by one: the previous-year questions PYQ_... and G4A_EQUATIONS_001 to 005.

In every ask the right choice is written first; the build script rotates them.
"""
from g4_gr4_equations_lib import (B, E, L, W, answer, balance, bars, both, choose, divide, fig, given, group, lesson,
                                  mark, note, strike)

LESSONS = {}

# m = 21, n = 3, m = n × p. Find m ÷ p.
_MNP = {"m": 21, "n": 3, "p": 7}
LESSONS["PYQ_2016_Q07"] = lesson([
    B("We are told m is 21 and n is 3. We also know that m equals n times p. We must find m divided by p.",
      E("g1", "m = 21", _MNP, "given"), E("g2", "n = 3", _MNP, "given"), E("g3", "m = n × p", _MNP, "given"),
      W("g4", "m ÷ p = ?")),
    B("One letter has no value yet: p. So first we find p. Let's put the numbers we know into m equals n times p.",
      mark("g3", "m = n × p", "underline"), E("l1", "21 = 3 × p", _MNP)),
    B("21 equals 3 times p. So what is p?",
      ask=choose(["7", "18", "63"], 0,
                 "Which number times 3 makes 21? In the 3 times table, 3 times 7 is 21. So p is 7.")),
    B("3 times 7 is 21, so p equals 7.", E("l2", "p = 21 ÷ 3 = 7", _MNP)),
    B("Careful: 7 is one of the choices, but it is only p. The question asks for m divided by p.",
      mark("g4", "m ÷ p", "underline")),
    B("m is 21 and p is 7. So which sum do we need?",
      ask=choose(["21 ÷ 7", "21 ÷ 3", "21 × 7"], 0,
                 "m is 21 and p is 7. So m divided by p is 21 divided by 7.")),
    B("21 divided by 7 is 3. So m divided by p equals 3.", answer("l3", "21 ÷ 7 = 3"), mark("l3", "3", "circle")),
    B("Notice something neat. The answer 3 is the same as n. That is because 21 is 3 times 7, "
      "so dividing by 7 brings back the 3."),
    B("So put in the numbers you know, find the missing letter, and then do what the question asks."),
])

# Radhika's 24 fruits
LESSONS["PYQ_2016_Q16"] = lesson([
    B("Radhika bought 24 fruits. She bought three times as many oranges as bananas. "
      "Let's first find how many of each she bought.",
      given("g1", "24 fruits: oranges = 3 × bananas", label=True)),
    B("For every 1 banana there are 3 oranges. So the fruits come in groups of 4: 3 oranges and 1 banana.",
      bars("f1", ("Oranges", [(2, "1 share", "a")] * 3), ("Bananas", [(2, "1 share", "b")]))),
    B("How many groups of 4 are there in 24 fruits?",
      ask=choose(["6", "8", "3"], 0,
                 "Each group has 4 fruits: 3 oranges and 1 banana. 24 divided by 4 is 6. So there are 6 groups.")),
    B("6 groups. So she bought 6 bananas, and 3 times 6, which is 18 oranges.",
      W("l1", "24 ÷ 4 = 6"), W("l2", "3 × 6 = 18")),
    B("Now the accident. She took home 15 fruits, so she dropped 24 minus 15. That is 9 fruits.",
      W("l3", "24 − 15 = 9")),
    B("She dropped twice as many oranges as bananas. So the dropped fruits come in groups of 3: "
      "2 oranges and 1 banana.", L("l4", "Dropped: 2 oranges for each banana")),
    B("9 fruits were dropped, in groups of 3. How many oranges were dropped?",
      ask=choose(["6", "3", "9"], 0,
                 "9 divided by 3 is 3 groups. Each group has 2 oranges, so 3 groups have 6 oranges. "
                 "The other 3 are bananas.")),
    B("So 6 oranges fell. She had bought 18 oranges. 18 minus 6 is 12.",
      W("l5", "9 ÷ 3 = 3"), W("l6", "2 × 3 = 6"), answer("l7", "18 − 6 = 12"), mark("l7", "12", "circle")),
    B("Let's check. At home she has 12 oranges, and 6 minus 3, that is 3 bananas. 12 plus 3 is 15. It works!",
      W("l8", "12 + 3 = 15")),
    B("Watch the traps. 9 is all the dropped fruits, and 6 is the dropped oranges. "
      "The question asks for the oranges at home, which is 12."),
])

# Karan's stamps
LESSONS["PYQ_2017_Q11"] = lesson([
    B("Karan buys some 5 paise stamps and some 10 paise stamps. Together they cost 55 paise.",
      given("g1", "5 paise and 10 paise stamps: 55 paise", label=True)),
    B("In a second plan, he buys the same 5 paise stamps, but twice as many 10 paise stamps. "
      "That would cost 1 rupee and 5 paise.", L("g2", "Twice the 10 paise stamps: Rs. 1 and 5 paise")),
    B("1 rupee is 100 paise. So how many paise is 1 rupee and 5 paise?",
      L("l1", "1 rupee = 100 paise"),
      ask=choose(["105 paise", "15 paise", "150 paise"], 0,
                 "1 rupee is 100 paise. Add the 5 paise, and we get 105 paise.")),
    B("So the first plan costs 55 paise and the second costs 105 paise. The second costs 50 paise more.",
      W("l2", "105 − 55 = 50")),
    B("What did that extra 50 paise pay for?",
      ask=choose(["a second lot of 10 paise stamps", "extra 5 paise stamps", "all the stamps"], 0,
                 "Only one thing changed: the 10 paise stamps were doubled. "
                 "So the extra 50 paise paid for a second lot of 10 paise stamps.")),
    B("The second lot is the same size as the first lot. So the 10 paise stamps he really bought cost 50 paise. "
      "That is 5 stamps.", W("l3", "50 ÷ 10 = 5")),
    B("Now back to the first plan. Out of 55 paise, 50 paise went on 10 paise stamps. So only 5 paise is left.",
      W("l4", "55 − 50 = 5")),
    B("5 paise is left for the 5 paise stamps. How many stamps is that?",
      ask=choose(["1", "5", "11"], 0,
                 "Each stamp costs 5 paise, and there is only 5 paise to spend. So that buys just 1 stamp.")),
    B("So Karan bought 1 stamp of 5 paise.",
      answer("l5", "Number of 5 paise stamps: 1", label=True), mark("l5", "1", "circle")),
    B("Let's check. 50 paise and 5 paise make 55. With the 10 paise stamps doubled, 100 paise and 5 paise "
      "make 105. It works!", W("l6", "50 + 5 = 55"), W("l7", "100 + 5 = 105")),
    B("Careful: the 5 we found first was the number of 10 paise stamps. The 5 paise stamps came to just 1."),
])

# 12x − 40 = 2x
LESSONS["PYQ_2017_Q14"] = lesson([
    B("Here is our equation. 12 x, minus 40, equals 2 x. The x is on both sides.", given("l1", "12x − 40 = 2x")),
    B("Think of x as a bag of marbles. 12 bags, with 40 marbles taken out, weigh the same as 2 bags.",
      balance("f1", "12x − 40", "2x")),
    B("Let's take 2 bags off each side. How many x are left on the left?",
      ask=choose(["10x", "14x", "12x"], 0,
                 "12 x take away 2 x leaves 10 x. We are taking away here, not adding.")),
    B("We take 2 x from both sides. The right side is now 0. The left is 10 x, minus 40.",
      both("l1", "− 2x"), W("l2", "10x − 40 = 0")),
    B("If 10 x, minus 40, leaves nothing, then 10 x must be exactly 40.",
      strike("l2", "− 40", "+ 40"), W("l3", "10x = 40")),
    B("10 times x is 40. So what is x?",
      ask=choose(["4", "30", "400"], 0, "To undo times 10, we divide by 10. And 40 divided by 10 is 4.")),
    B("40 divided by 10 is 4. So x equals 4.", divide("l3", 10), answer("l4", "x = 4"), mark("l4", "x = 4", "circle")),
    B("Let's check. Left: 12 times 4 is 48, and 48 minus 40 is 8. Right: 2 times 4 is 8. Both sides are 8!",
      W("l5", "12 × 4 = 48"), W("l6", "48 − 40 = 8"), W("l7", "2 × 4 = 8")),
    B("So gather the x on one side first. After that it is a simple times fact."),
], "x", 4)

# 21 more women than men; 105 people
LESSONS["PYQ_2018_Q10"] = lesson([
    B("At a meeting there were 21 more women than men. Altogether there were 105 people. "
      "We want the number of women.", given("g1", "Women = men + 21, total = 105", label=True)),
    B("Look at the bars. The women's bar is the same as the men's bar, with 21 extra on the end.",
      bars("f1", ("Women", [(4, "?", "unknown"), (2, "21", "c")]), ("Men", [(4, "?", "unknown")]))),
    B("If we set the 21 extra women aside, what can we say about the people left?",
      ask=choose(["men and women are equal", "they are all men", "there are 21 of them"], 0,
                 "Without the 21 extra, the two bars are the same length. "
                 "So the people left are men and women in equal numbers.")),
    B("105 minus 21 is 84. These 84 people are two equal groups.", W("l1", "105 − 21 = 84")),
    B("Half of 84 is 42. So there were 42 men.", W("l2", "84 ÷ 2 = 42")),
    B("Careful: 42 is the men. How do we get the women?",
      ask=choose(["42 + 21", "42 − 21", "42 × 2"], 0,
                 "There are 21 more women than men. So we add the 21 back on to 42.")),
    B("42 plus 21 is 63. So there were 63 women.", answer("l3", "42 + 21 = 63"), mark("l3", "63", "circle")),
    B("Let's check. 63 women and 42 men make 105 people. And 63 is 21 more than 42. It works!",
      W("l4", "63 + 42 = 105")),
    B("So set the extra aside, halve what is left, and then give the extra back to the bigger group."),
])

# 19/★ + 17/★ = 2
_S = {"★": 18}
LESSONS["PYQ_2018_Q25"] = lesson([
    B("Here is a puzzle with a star. 19 over star, plus 17 over star, equals 2. "
      "The star is the same number both times.", E("g1", "19/★ + 17/★ = 2", _S, "given")),
    B("Both fractions have the same bottom number, the star. When the bottoms are the same, we just add the tops.",
      group("g1", ["19", "17"], "add the tops")),
    B("19 plus 17 is 36. So 36 over star equals 2.", W("l1", "19 + 17 = 36"), E("l2", "36/★ = 2", _S)),
    B("36 over star means 36 divided by star. So 36 is shared into equal groups, and each group gets 2."),
    B("36 divided by which number gives 2?",
      ask=choose(["18", "36", "72"], 0,
                 "If each group gets 2, we need to know how many 2s make 36. "
                 "That is 36 divided by 2, which is 18.")),
    B("36 divided by 2 is 18. So the star is 18.",
      W("l3", "36 ÷ 2 = 18"), E("l4", "★ = 18", _S, "answer"), mark("l4", "★ = 18", "circle")),
    B("Let's check. 19 over 18, plus 17 over 18, is 36 over 18. And 36 divided by 18 is 2. It works!",
      W("l5", "19/18 + 17/18 = 36/18"), W("l6", "36 ÷ 18 = 2")),
    B("Careful with 36. It is only the sum of the tops. With 36 on the bottom, the answer would be 1, not 2."),
    B("So with the same bottom number, add the tops first. Then ask: divided by what gives the answer?"),
])

# 97 − 17x = 5x + 31
LESSONS["PYQ_2018_Q27"] = lesson([
    B("Here is our equation. 97, minus 17 x, equals 5 x, plus 31. The x is on both sides.",
      given("l1", "97 − 17x = 5x + 31")),
    B("On the left, 17 x is being taken away. Let's clear it, so that all the x are together on the right.",
      mark("l1", "17x", "underline")),
    B("How do we clear the minus 17 x?",
      ask=choose(["add 17x to both sides", "take 17x from both sides", "take 5x from both sides"], 0,
                 "The 17 x is being taken away. To undo taking away, we add. So we add 17 x to both sides.")),
    B("We add 17 x to both sides. The left is just 97. On the right, 5 x and 17 x make 22 x.",
      strike("l1", "− 17x", "+ 17x"), both("l1", "+ 17x"), W("l2", "97 = 22x + 31")),
    B("Now what do we do with the plus 31?",
      ask=choose(["take 31 from both sides", "add 31 to both sides", "divide 31 by 22"], 0,
                 "The 31 is added on the right. To undo adding, we take away. So 31 comes off both sides.")),
    B("97 minus 31 is 66. So 66 equals 22 x.",
      strike("l2", "+ 31", "− 31"), both("l2", "− 31"), W("l3", "66 = 22x")),
    B("22 times x is 66. Try 3: 22 times 3 is 66. So x equals 3.",
      divide("l3", 22), W("l4", "22 × 3 = 66"), answer("l5", "x = 3"), mark("l5", "x = 3", "circle")),
    B("Let's check. Left: 17 times 3 is 51, and 97 minus 51 is 46. Right: 5 times 3 is 15, and 15 plus 31 is 46. "
      "Both match!", W("l6", "17 × 3 = 51"), W("l7", "97 − 51 = 46"), W("l8", "15 + 31 = 46")),
    B("So when something with x is being taken away, add it to both sides. Then all the x sit together."),
], "x", 3)

# Tom's 100 marbles in four boxes
_BOXES = ["Box 1", "Box 2", "Box 3", "Box 4"]
LESSONS["PYQ_2018_Q31"] = lesson([
    B("Tom puts 100 marbles into four boxes. Each box has 2 more marbles than the one before.",
      given("g1", "100 marbles, 4 boxes, each has 2 more", label=True)),
    B("Compare every box with the first one. The second has 2 more. The third has 4 more. The fourth has 6 more.",
      fig("f1", {"kind": "table", "headers": _BOXES, "rows": [["?", "? + 2", "? + 4", "? + 6"]]})),
    B("How many extra marbles is that altogether?",
      ask=choose(["12", "6", "8"], 0, "The extras are 2, 4 and 6. Add all three: 2 plus 4 plus 6 is 12.")),
    B("2 plus 4 plus 6 is 12. Take those 12 extras away, and all four boxes are equal. 100 minus 12 is 88.",
      W("l1", "2 + 4 + 6 = 12"), W("l2", "100 − 12 = 88")),
    B("Now 88 marbles are shared equally among 4 boxes. 88 divided by 4 is 22. So the first box has 22.",
      W("l3", "88 ÷ 4 = 22")),
    B("Each box has 2 more than the one before. So the boxes hold 22, 24, 26 and 28.",
      fig("f2", {"kind": "table", "headers": _BOXES, "rows": [["22", "24", "26", "28"]]})),
    B("Careful! Read the question again. Which boxes does it ask about?",
      ask=choose(["the first 3 boxes", "all 4 boxes", "the last box"], 0,
                 "The question says the total in the first 3 boxes. So we leave out the fourth box, the one with 28.")),
    B("The first three boxes are everything except the last box. 100 minus 28 is 72.",
      W("l4", "100 − 28 = 72"), answer("l5", "22 + 24 + 26 = 72"), mark("l5", "72", "circle")),
    B("So find every box first. Then answer exactly what was asked: here, only the first three boxes."),
])

# 15 − 3x = x − 9
LESSONS["PYQ_2019_Q13"] = lesson([
    B("Here is our equation. 15, minus 3 x, equals x, minus 9. Something is being taken away on each side.",
      given("l1", "15 − 3x = x − 9")),
    B("Here is the key idea. Things that are taken away are cleared by adding. Let's start with the minus 3 x.",
      mark("l1", "− 3x", "underline")),
    B("What do we do to both sides to clear the minus 3 x?",
      ask=choose(["add 3x", "take away 3x", "take away x"], 0,
                 "The 3 x is being taken away. Adding 3 x puts it back, and the two cancel. "
                 "So we add 3 x to both sides.")),
    B("We add 3 x to both sides. The left is just 15. On the right, x and 3 x make 4 x.",
      strike("l1", "− 3x", "+ 3x"), both("l1", "+ 3x"), W("l2", "15 = 4x − 9")),
    B("Now the minus 9 on the right. How do we clear it?",
      ask=choose(["add 9 to both sides", "take 9 from both sides", "divide by 9"], 0,
                 "Same idea again. The 9 is being taken away, so we clear it by adding 9 to both sides.")),
    B("15 plus 9 is 24. So 24 equals 4 x.", strike("l2", "− 9", "+ 9"), both("l2", "+ 9"), W("l3", "24 = 4x")),
    B("Careful: x and 3 x made 4 x, so we divide by 4, not by 2. 24 divided by 4 is 6. So x equals 6.",
      divide("l3", 4), answer("l4", "x = 6"), mark("l4", "x = 6", "circle")),
    B("Let's check in our middle line. 4 times 6 is 24, and 24 minus 9 is 15. It works!", W("l5", "4 × 6 − 9 = 15")),
    B("So whenever something is being taken away, clear it by adding the same thing to both sides."),
], "x", 6)

# 31 − T = 2T + 7
_T8 = {"T": 8}
LESSONS["PYQ_2019_Q29"] = lesson([
    B("Here is our equation. 31, minus T, equals 2 T, plus 7. The letter T is on both sides.",
      E("g1", "31 − T = 2T + 7", _T8, "given")),
    B("On the left, one T is being taken away. Let's clear it, so that all the T are on the right.",
      mark("g1", "− T", "underline")),
    B("What do we add to both sides?",
      ask=choose(["T", "2T", "7"], 0,
                 "One T is being taken away on the left. Adding one T to both sides cancels it.")),
    B("We add T to both sides. The left is just 31. On the right, 2 T and 1 more T make 3 T.",
      strike("g1", "− T", "+ T"), both("g1", "+ T"), E("l2", "31 = 3T + 7", _T8)),
    B("Next, the plus 7. What do we do?",
      ask=choose(["take 7 from both sides", "add 7 to both sides", "divide by 7"], 0,
                 "The 7 is added on the right. To undo adding, we take away. So 7 comes off both sides.")),
    B("31 minus 7 is 24. So 24 equals 3 T.",
      strike("l2", "+ 7", "− 7"), both("l2", "− 7"), E("l3", "24 = 3T", _T8)),
    B("Careful: 24 is 3 T, not T. We divide both sides by 3. 24 divided by 3 is 8. So T equals 8.",
      divide("l3", 3), E("l4", "T = 8", _T8, "answer"), mark("l4", "T = 8", "circle")),
    B("Let's check. Left: 31 minus 8 is 23. Right: 2 times 8, plus 7, is also 23. Both sides match.",
      W("l5", "31 − 8 = 23"), W("l6", "2 × 8 + 7 = 23")),
    B("So bring the letters together first, by adding the one that is taken away. Then solve the two steps."),
])

# Anil: add 6, multiply by 4, get 60
LESSONS["G4A_EQUATIONS_001"] = lesson([
    B("Anil thinks of a number. He adds 6, then multiplies by 4, and gets 60. We want his starting number.",
      given("g1", "Number → + 6 → × 4 → 60", label=True)),
    B("We know the end, and we want the start. So we walk backwards, undoing each step."),
    B("Which step do we undo first?",
      ask=choose(["the times 4", "the plus 6"], 0,
                 "Going backwards, the last thing done is the first thing undone. "
                 "The last thing Anil did was multiply by 4.")),
    B("To undo times 4, we divide by 4. Half of 60 is 30, and half of 30 is 15.",
      strike("g1", "× 4", "÷ 4"), W("l1", "60 ÷ 2 = 30"), W("l2", "30 ÷ 2 = 15")),
    B("So before multiplying, Anil had 15. He got 15 by adding 6. How do we undo that?",
      ask=choose(["15 − 6", "15 + 6", "15 ÷ 6"], 0,
                 "Adding 6 is undone by taking 6 away. Adding again would take us further from the start.")),
    B("15 minus 6 is 9. So Anil thought of 9.",
      strike("g1", "+ 6", "− 6"), answer("l3", "15 − 6 = 9"), mark("l3", "9", "circle")),
    B("Let's go forwards to check. 9 plus 6 is 15, and 15 times 4 is 60. It works!", W("l4", "(9 + 6) × 4 = 60")),
    B("So when you know the end and want the start, work backwards. Undo the last step first."),
])

# Kabir and Diya save ₹96; Diya saves twice as much
LESSONS["G4A_EQUATIONS_002"] = lesson([
    B("Kabir and Diya save 96 rupees altogether. Diya saves twice as much as Kabir.",
      given("g1", "Kabir + Diya = ₹96, Diya = 2 × Kabir", label=True)),
    B("Think of Kabir's money as 1 share. Then Diya's money is 2 shares of the same size.",
      bars("f1", ("Kabir", [(3, "1 share", "a")]), ("Diya", [(3, "1 share", "b"), (3, "1 share", "b")]))),
    B("How many equal shares are there altogether?",
      ask=choose(["3", "2", "4"], 0, "Kabir has 1 share and Diya has 2 shares. 1 plus 2 is 3 shares.")),
    B("So 3 equal shares make 96 rupees. One share is 96 divided by 3.", W("l1", "96 ÷ 3 = ?")),
    B("3 times 30 is 90, and 3 times 2 is 6. So 96 divided by 3 is 32.",
      W("l2", "3 × 30 = 90"), W("l3", "3 × 2 = 6"), W("l4", "96 ÷ 3 = 32")),
    B("32 rupees is one share. Whose money is that?",
      ask=choose(["Kabir's", "Diya's", "both together"], 0,
                 "Kabir has 1 share and Diya has 2. So one share, 32 rupees, is Kabir's saving.")),
    B("So Kabir saves 32 rupees.", answer("l5", "₹32"), mark("l5", "₹32", "circle")),
    B("Let's check. Diya saves twice 32, which is 64. And 32 plus 64 is 96. It works!",
      W("l6", "2 × 32 = 64"), W("l7", "32 + 64 = 96")),
    B("Careful not to just halve the money. Twice as much means 3 shares in all, not 2."),
])

# 8 children get 7 toffees each, 5 left over
LESSONS["G4A_EQUATIONS_003"] = lesson([
    B("A teacher shares toffees among 8 children. Each child gets 7, and 5 toffees are left over. "
      "How many did she have?", given("g1", "8 children × 7 toffees, 5 left over", label=True)),
    B("Her toffees went to two places. Some went to the children, and some stayed left over.",
      bars("f1", (None, [(5.6, "given out", "a"), (1, "left: 5", "b")], "?"))),
    B("How many toffees did the 8 children get altogether?",
      ask=choose(["8 × 7", "8 + 7", "7 + 5"], 0,
                 "8 children each get 7 toffees. That is 8 lots of 7, so we multiply.")),
    B("8 times 7 is 56. So 56 toffees were given out.", W("l1", "8 × 7 = 56")),
    B("And the 5 left over: do we add them, or take them away?",
      ask=choose(["add them", "take them away"], 0,
                 "The left-over toffees were with the teacher at the start too. "
                 "So they are part of her total, and we add them.")),
    B("56 plus 5 is 61. So the teacher had 61 toffees.", answer("l2", "56 + 5 = 61"), mark("l2", "61", "circle")),
    B("Let's check. From 61 toffees, 56 are given out, 7 to each of the 8 children. That leaves 5. It works!",
      W("l3", "61 − 56 = 5")),
    B("So to get back to the start, put everything back together: what was given out, and what was left."),
])

# Perimeter 46 cm, length 15 cm
LESSONS["G4A_EQUATIONS_004"] = lesson([
    B("A rectangular photo frame has a perimeter of 46 centimetres. Its length is 15 centimetres. "
      "We want its breadth.", given("g1", "Perimeter = 46 cm, length = 15 cm", label=True)),
    B("The perimeter is the distance all the way round. That is two lengths and two breadths.",
      L("l1", "Perimeter = 2 lengths + 2 breadths")),
    B("How much of the 46 centimetres do the two lengths use up?",
      ask=choose(["30 cm", "15 cm", "23 cm"], 0,
                 "There are two lengths, one at the top and one at the bottom. "
                 "Each is 15, so together they use 30 centimetres.")),
    B("2 times 15 is 30. So the two lengths use 30 centimetres.", W("l2", "2 × 15 = 30")),
    B("What is left is for the two breadths. 46 minus 30 is 16.", W("l3", "46 − 30 = 16")),
    B("Careful: 16 centimetres is the two breadths together. What is one breadth?",
      ask=choose(["8 cm", "16 cm", "32 cm"], 0,
                 "The two breadths are equal, and together they are 16. So one breadth is half of 16, which is 8.")),
    B("Half of 16 is 8. So the breadth is 8 centimetres.",
      W("l4", "16 ÷ 2 = 8"), answer("l5", "Breadth = 8 cm", label=True), mark("l5", "8 cm", "circle")),
    B("Let's check by going all the way round. 15 plus 8 plus 15 plus 8 is 46. It works!",
      W("l6", "15 + 8 + 15 + 8 = 46")),
    B("So for a rectangle, take both lengths away from the perimeter. Then halve what is left."),
])

# 3 boxes and a 2 kg weight balance 14 kg
LESSONS["G4A_EQUATIONS_005"] = lesson([
    B("On one pan are 3 equal boxes and a 2 kilogram weight. On the other pan is a 14 kilogram weight. "
      "The balance is level.",
      given("g1", "3 boxes + 2 kg = 14 kg", label=True), balance("f1", "3 boxes + 2 kg", "14 kg")),
    B("Level means both pans weigh the same. So 3 boxes and 2 kilograms together weigh 14 kilograms."),
    B("If we lift the 2 kilogram weight off the left pan, what must we do to keep the balance level?",
      ask=choose(["take 2 kg off the right too", "add 2 kg to the right", "nothing"], 0,
                 "If only one pan gets lighter, the balance tips. "
                 "So 2 kilograms must come off the right pan as well.")),
    B("14 minus 2 is 12. So the 3 boxes weigh 12 kilograms together.",
      W("l1", "14 − 2 = 12"), balance("f2", "3 boxes", "12 kg")),
    B("12 kilograms is all 3 boxes. How do we find one box?",
      ask=choose(["12 ÷ 3", "12 ÷ 2", "12 − 3"], 0,
                 "The 3 boxes are equal, so we share 12 equally among 3. That is 12 divided by 3.")),
    B("12 divided by 3 is 4. So one box weighs 4 kilograms.",
      W("l2", "12 ÷ 3 = 4"), answer("l3", "One box = 4 kg", label=True), mark("l3", "4 kg", "circle")),
    B("Let's check. 3 boxes of 4 kilograms weigh 12. Add the 2 kilogram weight, and we get 14. Level!",
      W("l4", "3 × 4 + 2 = 14")),
    B("So take the loose weight off both pans first. Then share what is left among the boxes."),
])
