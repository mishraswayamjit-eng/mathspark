"""Lessons written one by one: G4A_EQUATIONS_006 to 020.

In every ask the right choice is written first; the build script rotates them.
"""
from g4_gr4_equations_lib import (B, E, L, T, W, answer, balance, bars, both, choose, divide, given, lesson, mark,
                                  note, strike)

LESSONS = {}

# Tara's mother: 3 times as old, and 24 years older
LESSONS["G4A_EQUATIONS_006"] = lesson([
    B("Tara's mother is 3 times as old as Tara. She is also 24 years older than Tara. How old is Tara?",
      given("g1", "Mother = 3 × Tara, mother = Tara + 24", label=True)),
    B("Think of Tara's age as 1 share. Her mother's age is 3 of those shares.",
      bars("f1", ("Tara", [(3, "1 share", "a")]), ("Mother", [(3, "1 share", "b")] * 3))),
    B("How many shares more does the mother have than Tara?",
      ask=choose(["2 shares", "3 shares", "4 shares"], 0,
                 "The mother has 3 shares and Tara has 1. The difference is 3 take away 1, which is 2 shares.")),
    B("And we are told that the difference is 24 years. So those 2 extra shares are 24 years.",
      L("l1", "2 shares = 24 years")),
    B("If 2 shares are 24 years, what is 1 share?",
      ask=choose(["12 years", "8 years", "6 years"], 0,
                 "Careful: the 24 years is the gap, and the gap is 2 shares, not 3. "
                 "So one share is half of 24, which is 12.")),
    B("Half of 24 is 12. Tara's age is 1 share, so Tara is 12 years old.",
      W("l2", "24 ÷ 2 = 12"), answer("l3", "Tara = 12 years", label=True), mark("l3", "12", "circle")),
    B("Let's check. Her mother is 3 times 12, which is 36. And 36 minus 12 is 24. Both clues fit!",
      W("l4", "3 × 12 = 36"), W("l5", "36 − 12 = 24")),
    B("So when you know how many times bigger, and the gap, find how many shares the gap is. Then find one share."),
])

# 5 pens, ₹100 paid, ₹35 back
LESSONS["G4A_EQUATIONS_007"] = lesson([
    B("Sana buys 5 pens of the same price. She pays with a 100 rupee note and gets 35 rupees back.",
      given("g1", "5 pens: paid ₹100, got ₹35 back", label=True)),
    B("How much did the 5 pens really cost?",
      ask=choose(["100 − 35", "100 + 35", "just 100"], 0,
                 "She handed over 100 rupees, but 35 rupees came back to her. So the shop kept 100 minus 35.")),
    B("100 minus 35 is 65. So the 5 pens cost 65 rupees.", W("l1", "100 − 35 = 65")),
    B("65 rupees is for all 5 pens. How do we find the price of one?",
      ask=choose(["65 ÷ 5", "65 − 5", "35 ÷ 5"], 0,
                 "The 5 pens cost the same, so we share the 65 rupees equally among 5 pens. "
                 "The 35 is her change, not the cost.")),
    B("65 divided by 5. 5 times 10 is 50. That leaves 15, and 5 times 3 is 15. So it is 10 and 3 more: 13.",
      W("l2", "65 = 50 + 15"), W("l3", "65 ÷ 5 = 13")),
    B("So one pen costs 13 rupees.", answer("l4", "₹13"), mark("l4", "₹13", "circle")),
    B("Let's check. 5 pens at 13 rupees cost 65. And 65 plus the 35 change makes 100. It works!",
      W("l5", "5 × 13 = 65"), W("l6", "65 + 35 = 100")),
    B("So first find what was really spent. Then share it among the things bought."),
])

# Auto-rickshaw fare
LESSONS["G4A_EQUATIONS_008"] = lesson([
    B("An auto-rickshaw charges 30 rupees for the first kilometre, and 12 rupees for every kilometre after that. "
      "Imran pays 90 rupees.", given("g1", "₹30 first km, ₹12 each km after, paid ₹90", label=True)),
    B("So the fare has two parts: one special first kilometre, and then some ordinary kilometres.",
      bars("f1", (None, [(3, "first km: ₹30", "c"), (6, "other km: ₹12 each", "a")], "₹90"))),
    B("What should we do first with the 90 rupees?",
      ask=choose(["take away the ₹30", "divide by 12", "add the ₹30"], 0,
                 "The first kilometre has its own price, 30 rupees. Take that off first. "
                 "What is left pays for the ordinary kilometres.")),
    B("90 minus 30 is 60. So 60 rupees paid for the kilometres after the first.", W("l1", "90 − 30 = 60")),
    B("Each of those costs 12 rupees. 12 times 5 is 60. So there were 5 more kilometres.", W("l2", "60 ÷ 12 = 5")),
    B("Here is the trap. Is 5 kilometres the whole ride?",
      ask=choose(["No, add the first kilometre", "Yes, it is 5 km"], 0,
                 "5 is only the kilometres after the first one. "
                 "The first kilometre, the one that cost 30 rupees, counts too.")),
    B("5 plus 1 is 6. So Imran travels 6 kilometres.",
      W("l3", "5 + 1 = 6"), answer("l4", "Ride = 6 km", label=True), mark("l4", "6 km", "circle")),
    B("Let's check. 30 rupees for the first kilometre, and 5 times 12, which is 60, for the rest. "
      "30 plus 60 is 90. It works!", W("l5", "30 + 5 × 12 = 90")),
    B("So take off the special first charge, divide the rest, and remember to count the first kilometre."),
])

# ★ + ★ = 18, ★ + ▲ = 14
_SH = {"★": 9, "▲": 5}
LESSONS["G4A_EQUATIONS_009"] = lesson([
    B("Here are two sums with shapes. Star plus star equals 18. Star plus triangle equals 14. "
      "We want the triangle.", E("g1", "★ + ★ = 18", _SH, "given"), E("g2", "★ + ▲ = 14", _SH, "given")),
    B("Which sum should we start with?",
      ask=choose(["★ + ★ = 18", "★ + ▲ = 14"], 0,
                 "The second sum has two different shapes we do not know. "
                 "The first has only stars, so we can solve it straight away.")),
    B("Star plus star is 18. Two equal numbers make 18, so each is half of 18. The star is 9.",
      mark("g1", "★ + ★", "underline"), W("l1", "18 ÷ 2 = 9"), E("l2", "★ = 9", _SH)),
    B("Now put 9 in place of the star in the second sum. 9 plus triangle equals 14.",
      note("g2", "★", "9"), E("l3", "9 + ▲ = 14", _SH)),
    B("9 plus what makes 14?",
      ask=choose(["5", "7", "9"], 0, "Take 9 away from 14. That leaves 5. So the triangle is 5.")),
    B("14 minus 9 is 5. So the triangle stands for 5.",
      W("l4", "14 − 9 = 5"), E("l5", "▲ = 5", _SH, "answer"), mark("l5", "▲ = 5", "circle")),
    B("Let's check. 9 plus 9 is 18, and 9 plus 5 is 14. Both sums work!",
      W("l6", "9 + 9 = 18"), W("l7", "9 + 5 = 14")),
    B("Careful: 9 is the star, not the triangle. Start with the sum that has one kind of shape, "
      "then use it in the other."),
])

# Half of a number, increased by 8, is 20
LESSONS["G4A_EQUATIONS_010"] = lesson([
    B("Half of a number, increased by 8, is 20. What is the number?",
      given("g1", "Half of a number + 8 = 20", label=True)),
    B("Let's see what happened to the number. First it was halved. Then 8 was added. And 20 came out.",
      L("l1", "Number → half → + 8 → 20")),
    B("We work backwards from 20. What do we undo first?",
      ask=choose(["the plus 8", "the halving"], 0, "The adding of 8 came last, so we undo it first.")),
    B("To undo plus 8, we take away 8. 20 minus 8 is 12.", strike("l1", "+ 8", "− 8"), W("l2", "20 − 8 = 12")),
    B("12 is half of the number. How do we undo halving?",
      ask=choose(["double it", "halve it again", "add 2"], 0,
                 "If 12 is one half, the whole number is two halves. So we double 12.")),
    B("Double 12 is 24. So the number is 24.",
      W("l3", "12 × 2 = 24"), answer("l4", "The number is 24", label=True), mark("l4", "24", "circle")),
    B("Let's check. Half of 24 is 12, and 12 plus 8 is 20. It works!", W("l5", "24 ÷ 2 + 8 = 20")),
    B("Careful: 12 is only half of the number. Undo the adding first, then undo the halving by doubling."),
])

# Hens and 6 cows: 44 legs
LESSONS["G4A_EQUATIONS_011"] = lesson([
    B("A farmer has some hens and 6 cows. Together the animals have 44 legs. How many hens are there?",
      given("g1", "Hens + 6 cows = 44 legs", label=True)),
    B("A cow has 4 legs. A hen has 2 legs. Let's deal with the cows first, because we know how many there are."),
    B("How many legs do the 6 cows have?",
      ask=choose(["24", "12", "6"], 0, "Each cow has 4 legs. 6 cows have 6 times 4 legs, and that is 24.")),
    B("6 times 4 is 24. So 24 of the legs belong to cows.", W("l1", "6 × 4 = 24")),
    B("The rest are hens' legs. 44 minus 24 is 20.", W("l2", "44 − 24 = 20")),
    B("20 legs belong to hens. So how many hens are there?",
      ask=choose(["10", "20", "5"], 0,
                 "Each hen has 2 legs. So the number of hens is half the number of legs. Half of 20 is 10.")),
    B("Each hen has 2 legs, so we halve. 20 divided by 2 is 10. There are 10 hens.",
      W("l3", "20 ÷ 2 = 10"), answer("l4", "Hens = 10", label=True), mark("l4", "10", "circle")),
    B("Let's check. 10 hens have 20 legs. 6 cows have 24 legs. 20 plus 24 is 44. It works!",
      W("l5", "10 × 2 + 6 × 4 = 44")),
    B("So take out the legs you know about first. Then share the rest, 2 legs to each hen."),
])

# Gopal is x; sister 3 years younger; ages add to 21. Which equation?
LESSONS["G4A_EQUATIONS_012"] = lesson([
    B("Gopal is x years old. His sister is 3 years younger. Their ages add up to 21. "
      "We must pick the equation that tells this story.", given("g1", "Gopal = x years", label=True)),
    B("We do not need to find x. We just have to write the story in maths. Let's do it one person at a time."),
    B("Gopal's age is x. His sister is 3 years younger. What is her age?",
      ask=choose(["x − 3", "x + 3", "3x"], 0,
                 "Younger means fewer years. So we take 3 away from Gopal's age. That is x minus 3. "
                 "3 x would mean 3 times as old.")),
    B("So the sister's age is x minus 3.", L("l1", "Sister = x − 3")),
    B("Their ages add up to 21. So what do we do with x, and x minus 3?",
      ask=choose(["add them", "multiply them", "subtract them"], 0,
                 "Add up means plus. So we add Gopal's age and his sister's age, and that makes 21.")),
    B("Gopal's age, plus his sister's age, equals 21. So x, plus x minus 3, equals 21.",
      E("l2", "x + x − 3 = 21", {"x": 12}, "answer"), note("l2", T("x"), "Gopal", "below"),
      note("l2", "x − 3", "sister", "below"), mark("l2", "x + x − 3 = 21", "circle")),
    B("Let's test it with a number. If Gopal is 12, his sister is 9, and 12 plus 9 is 21. The equation fits.",
      W("l3", "12 + 12 − 3 = 21")),
    B("Watch out for x minus 3 equals 21 on its own. That is only the sister's age. The 21 is both ages together."),
    B("So to turn a story into an equation, write each part with the letter. Then join them the way the story says."),
])

# Six times a number is the number plus 35
LESSONS["G4A_EQUATIONS_013"] = lesson([
    B("Six times a number is the same as the number itself, increased by 35. Let's call the number n.",
      given("l1", "6 × n = n + 35")),
    B("Picture a balance. On the left, 6 bags. On the right, 1 bag and a weight of 35. Each bag holds the number.",
      balance("f1", "6 bags", "1 bag + 35")),
    B("If we lift 1 bag off each side, what is left?",
      ask=choose(["5 bags balance 35", "6 bags balance 35", "5 bags balance 34"], 0,
                 "The left had 6 bags, so 5 stay. The right had 1 bag, so only the 35 stays. "
                 "So 5 bags balance 35.")),
    B("So we take one n from both sides. 5 times n equals 35.", both("l1", "− n"), W("l2", "5 × n = 35")),
    B("Careful: 35 is 5 times the number. So what is the number?",
      ask=choose(["7", "35", "29"], 0,
                 "5 lots of the number make 35. So one lot is 35 divided by 5, which is 7.")),
    B("35 divided by 5 is 7. So the number is 7.",
      divide("l2", 5), answer("l3", "n = 7"), mark("l3", "n = 7", "circle")),
    B("Let's check. 6 times 7 is 42. And 7 plus 35 is also 42. Both sides match!",
      W("l4", "6 × 7 = 42"), W("l5", "7 + 35 = 42")),
    B("So when the number is on both sides, take the same amount of it from each side. Then divide."),
], "n", 7)

# 5 tins + 3 kg = 2 tins + 18 kg
LESSONS["G4A_EQUATIONS_014"] = lesson([
    B("A balance is level. On the left: 5 equal tins and a 3 kilogram weight. "
      "On the right: 2 tins and an 18 kilogram weight.",
      given("g1", "5 tins + 3 kg = 2 tins + 18 kg", label=True), balance("f1", "5 tins + 3 kg", "2 tins + 18 kg")),
    B("A balance stays level if we take the same thing off both pans. Let's use that to get tins on one side only."),
    B("What can we take off both pans, to leave tins on the left only?",
      ask=choose(["2 tins from each pan", "5 tins from each pan", "2 tins from the left only"], 0,
                 "The right pan has only 2 tins, so 2 is the most we can take from both. "
                 "And it must be from both, to stay level.")),
    B("Take 2 tins off each pan. Now the left has 3 tins and 3 kilograms. The right has just 18 kilograms.",
      balance("f2", "3 tins + 3 kg", "18 kg"), L("l1", "3 tins + 3 kg = 18 kg")),
    B("Next, take the 3 kilogram weight off both pans. What is left on the right?",
      ask=choose(["15 kg", "21 kg", "18 kg"], 0,
                 "We are taking 3 kilograms off, so the right pan gets lighter. 18 minus 3 is 15.")),
    B("18 minus 3 is 15. So 3 tins balance 15 kilograms.", W("l2", "18 − 3 = 15"), L("l3", "3 tins = 15 kg")),
    B("3 equal tins weigh 15, so one tin is 15 divided by 3. That is 5 kilograms.",
      W("l4", "15 ÷ 3 = 5"), answer("l5", "One tin = 5 kg", label=True), mark("l5", "5 kg", "circle")),
    B("Let's check. Left: 5 tins of 5, plus 3, makes 28. Right: 2 tins of 5, plus 18, also makes 28. Level!",
      W("l6", "5 × 5 + 3 = 28"), W("l7", "2 × 5 + 18 = 28")),
    B("So take the same tins off both pans, then the same weight. What is left tells you one tin."),
])

# Asha 52 stickers, Bina 28: make them equal
LESSONS["G4A_EQUATIONS_015"] = lesson([
    B("Asha has 52 stickers and Bina has 28. Asha gives some to Bina, so that both have the same number. "
      "How many does she give?", given("g1", "Asha 52 stickers, Bina 28 stickers", label=True)),
    B("When Asha gives stickers to Bina, no stickers are lost. So the total stays the same. 52 plus 28 is 80.",
      W("l1", "52 + 28 = 80")),
    B("At the end both girls have the same number. How many is that?",
      ask=choose(["40", "80", "24"], 0,
                 "The 80 stickers are shared equally between 2 girls. Half of 80 is 40.")),
    B("Half of 80 is 40. So each girl should end with 40.", W("l2", "80 ÷ 2 = 40")),
    B("Asha has 52 and must come down to 40. How many does she give away?",
      ask=choose(["12", "24", "40"], 0,
                 "She goes from 52 down to 40. 52 minus 40 is 12. The 40 is what she keeps, not what she gives.")),
    B("52 minus 40 is 12. So Asha must give 12 stickers.", answer("l3", "52 − 40 = 12"), mark("l3", "12", "circle")),
    B("Let's check. Bina then has 28 plus 12, which is 40. Both girls have 40. It works!", W("l4", "28 + 12 = 40")),
    B("Here is the trap. Asha has 24 more than Bina. But if she gave all 24, Bina would then have more! "
      "She gives only half of the gap, which is 12.", W("l5", "52 − 28 = 24")),
    B("So when things move between two people, find the total and share it equally. "
      "Then see how far each must move. Here it is 12."),
])

# 10 vehicles, 34 wheels
LESSONS["G4A_EQUATIONS_016"] = lesson([
    B("A parking lot has auto-rickshaws with 3 wheels and cars with 4 wheels. "
      "There are 10 vehicles and 34 wheels. How many cars?",
      given("g1", "10 vehicles, 34 wheels: autos 3, cars 4", label=True)),
    B("Here is a clever trick. Let's pretend all 10 vehicles are auto-rickshaws, and count the wheels."),
    B("If all 10 were auto-rickshaws, how many wheels would there be?",
      ask=choose(["30", "40", "34"], 0,
                 "Each auto-rickshaw has 3 wheels. 10 of them have 10 times 3, which is 30 wheels.")),
    B("10 times 3 is 30. But there are really 34 wheels. That is 4 wheels more than we counted.",
      W("l1", "10 × 3 = 30"), W("l2", "34 − 30 = 4")),
    B("Where do the 4 extra wheels come from?",
      ask=choose(["each car has 1 extra wheel", "each car has 4 extra wheels", "there are 4 more vehicles"], 0,
                 "A car has 4 wheels and an auto-rickshaw has 3. So each time a pretend auto-rickshaw "
                 "is really a car, we get 1 extra wheel.")),
    B("Each car adds just 1 extra wheel. So 4 extra wheels mean 4 cars.",
      answer("l3", "Cars = 4", label=True), mark("l3", "4", "circle")),
    B("Then the auto-rickshaws are 10 minus 4, which is 6. Careful: 6 is in the choices too, "
      "but the question asks for cars.", W("l4", "10 − 4 = 6")),
    B("Let's check. 4 cars have 16 wheels. 6 auto-rickshaws have 18 wheels. 16 plus 18 is 34. It works!",
      W("l5", "4 × 4 = 16"), W("l6", "6 × 3 = 18"), W("l7", "16 + 18 = 34")),
    B("So pretend they are all the smaller kind, and count. The wheels that are missing tell you there are 4 cars."),
])

# Jaya, Bala and Chitra's shells
LESSONS["G4A_EQUATIONS_017"] = lesson([
    B("Jaya has twice as many shells as Bala. Chitra has 5 more than Bala. Together they have 45 shells. "
      "How many has Bala?", given("g1", "Jaya = 2 × Bala, Chitra = Bala + 5, total 45", label=True)),
    B("Call Bala's shells 1 share. Jaya has 2 shares. Chitra has 1 share, and 5 more.",
      bars("f1", ("Bala", [(3, "1 share", "a")]), ("Jaya", [(3, "1 share", "b"), (3, "1 share", "b")]),
           ("Chitra", [(3, "1 share", "a"), (1.2, "5", "c")]))),
    B("How many shares are there altogether, not counting the extra 5?",
      ask=choose(["4 shares", "3 shares", "5 shares"], 0,
                 "Bala has 1, Jaya has 2 and Chitra has 1. 1 plus 2 plus 1 is 4 shares. The extra 5 is not a share.")),
    B("So 4 shares, and 5 more, make 45.", L("l1", "4 shares + 5 = 45")),
    B("What do we do first?",
      ask=choose(["take away the extra 5", "divide 45 by 4", "divide 45 by 5"], 0,
                 "The extra 5 is not part of the equal shares. Take it away first. "
                 "Then what is left can be shared equally.")),
    B("45 minus 5 is 40. So 4 shares make 40.", W("l2", "45 − 5 = 40")),
    B("40 divided by 4 is 10. One share is 10, so Bala has 10 shells.",
      W("l3", "40 ÷ 4 = 10"), answer("l4", "Bala = 10 shells", label=True), mark("l4", "10", "circle")),
    B("Let's check. Jaya has twice 10, which is 20. Chitra has 10 plus 5, which is 15. "
      "And 10 plus 20 plus 15 is 45. It works!", W("l5", "10 + 20 + 15 = 45")),
    B("So write everyone in shares of the smallest. Take off any extras, then divide. Bala's share is 10."),
])

# Garden: length is 3 m more than twice the breadth; perimeter 48 m
LESSONS["G4A_EQUATIONS_018"] = lesson([
    B("The length of a garden is 3 metres more than twice its breadth. Its perimeter is 48 metres. "
      "We want the length.", given("g1", "Length = 2 × breadth + 3 m, perimeter 48 m", label=True)),
    B("The perimeter is two lengths and two breadths. So one length and one breadth make half of it. "
      "Half of 48 is 24.", W("l1", "48 ÷ 2 = 24"), L("l2", "length + breadth = 24 m")),
    B("Now, the length is 2 breadths, and 3 metres more.",
      bars("f1", ("Length", [(3, "breadth", "a"), (3, "breadth", "a"), (1, "3 m", "c")]),
           ("Breadth", [(3, "breadth", "a")]))),
    B("So length plus breadth is how many breadths, and how many extra metres?",
      ask=choose(["3 breadths and 3 m", "2 breadths and 3 m", "3 breadths"], 0,
                 "The length gives 2 breadths and 3 metres. Add the breadth itself, "
                 "and we have 3 breadths and 3 metres.")),
    B("So 3 breadths, and 3 metres, make 24 metres. Take away the 3. 24 minus 3 is 21.",
      L("l3", "3 breadths + 3 m = 24 m"), W("l4", "24 − 3 = 21")),
    B("3 breadths make 21, so one breadth is 21 divided by 3. That is 7 metres.", W("l5", "21 ÷ 3 = 7")),
    B("Careful! 7 metres is the breadth. What does the question ask for?",
      ask=choose(["the length", "the breadth", "the perimeter"], 0,
                 "Read the last line again. It asks for the length of the garden. So we have one more step.")),
    B("The length is twice 7, plus 3. Twice 7 is 14, and 14 plus 3 is 17. So the length is 17 metres.",
      W("l6", "2 × 7 = 14"), W("l7", "14 + 3 = 17"), answer("l8", "Length = 17 m", label=True),
      mark("l8", "17 m", "circle")),
    B("Let's check. 17 plus 7 is 24. And twice 24 is 48, the perimeter. It works!",
      W("l9", "17 + 7 = 24"), W("l10", "2 × 24 = 48")),
    B("So halve the perimeter, find the breadth, and then build the length from it. The length is 17 metres."),
])

# Raju and Sonu's notebooks
LESSONS["G4A_EQUATIONS_019"] = lesson([
    B("Raju and Sonu start with the same money. Raju buys 3 notebooks and has 14 rupees left. "
      "Sonu buys 4 notebooks and has 2 rupees left.",
      given("g1", "3 notebooks + ₹14 = 4 notebooks + ₹2", label=True)),
    B("Both boys had the same money. So Raju's 3 notebooks and 14 rupees are worth the same as "
      "Sonu's 4 notebooks and 2 rupees.", balance("f1", "3 notebooks + ₹14", "4 notebooks + ₹2")),
    B("Let's compare. How many more notebooks did Sonu buy than Raju?",
      ask=choose(["1 more", "2 more", "4 more"], 0,
                 "Sonu bought 4 and Raju bought 3. 4 take away 3 is 1. So Sonu bought just 1 more notebook.")),
    B("Sonu bought 1 more notebook. And because of that, he has less money left: 2 rupees, not 14."),
    B("How much less money does Sonu have left?",
      ask=choose(["₹12", "₹16", "₹7"], 0,
                 "Raju has 14 rupees left and Sonu has 2. The gap is 14 minus 2, which is 12. "
                 "We subtract here. We do not add.")),
    B("14 minus 2 is 12. That 12 rupees is exactly what the one extra notebook cost.", W("l1", "14 − 2 = 12")),
    B("So one notebook costs 12 rupees.", answer("l2", "₹12"), mark("l2", "₹12", "circle")),
    B("Let's check. Raju: 3 notebooks at 12, plus 14 left, makes 50. Sonu: 4 notebooks at 12, plus 2 left, "
      "also makes 50. The same money!", W("l3", "3 × 12 + 14 = 50"), W("l4", "4 × 12 + 2 = 50")),
    B("So when two people start the same, compare them. The extra thing bought explains the money that is missing."),
])

# Neha: half on a book, ₹30 on a pen, ₹45 left
LESSONS["G4A_EQUATIONS_020"] = lesson([
    B("Neha spends half of her money on a book. Then she spends 30 rupees on a pen. She has 45 rupees left.",
      given("g1", "Money → half spent → − ₹30 → ₹45 left", label=True)),
    B("We know the end, so we work backwards. We undo the last thing first."),
    B("What was the last thing Neha did?",
      ask=choose(["spent ₹30 on a pen", "spent half on a book"], 0,
                 "The story says the book came first, then the pen. So the pen was last, and we undo that first.")),
    B("To undo spending 30 rupees, we add it back. 45 plus 30 is 75. "
      "So she had 75 rupees after buying the book.", strike("g1", "− ₹30", "+ ₹30"), W("l1", "45 + 30 = 75")),
    B("She spent half her money on the book. So what is the 75 rupees?",
      ask=choose(["the other half of her money", "all of her money", "a quarter of her money"], 0,
                 "She spent one half on the book. What she still had, 75 rupees, is the other half.")),
    B("75 rupees is half of her money. So we double it. 75 plus 75 is 150.", W("l2", "75 + 75 = 150")),
    B("So Neha had 150 rupees at first.", answer("l3", "₹150"), mark("l3", "₹150", "circle")),
    B("Let's check. Half of 150 is 75, spent on the book. That leaves 75. Take away 30 for the pen, "
      "and 45 is left. It works!", W("l4", "150 − 75 − 30 = 45")),
    B("Careful with the order. Going backwards, add back the 30 first, and only then double."),
])
