"""Lessons written one by one: G4A_RATIO_001 to G4A_RATIO_012."""
from g4_gr4_ratio_lib import (A, C, F, G, Lb, N, U, W, X, ask, bar, bars, beat, lesson, segs)

LESSONS = {}
L = LESSONS

L["G4A_RATIO_001"] = lesson(
    beat("A class has 12 boys and 18 girls. We want the ratio of boys to girls, in its simplest form.",
         G("q1", "12 boys and 18 girls"), G("q2", "Boys : girls, in simplest form = ?")),
    beat("A ratio follows the order of the words. The question says boys to girls. So which number do we write first?",
         ask=ask(["12", "18"], 0, "Boys are named first, and there are 12 boys. So 12 goes first.")),
    beat("So we write 12 to 18. Boys first, girls second.", U("q2", "Boys"), Lb("r1", "12 : 18")),
    beat("Now let us make it simpler. We need a number that divides both 12 and 18 exactly. Which is the biggest one?",
         ask=ask(["4", "6", "9"], 1, "It must go into both numbers. 4 does not go into 18, and 9 does not go into 12. But 6 times 2 is 12, and 6 times 3 is 18.")),
    beat("Divide both numbers by 6. 12 divided by 6 is 2. 18 divided by 6 is 3.",
         W("w1", "12 ÷ 6 = 2"), W("w2", "18 ÷ 6 = 3")),
    beat("So the ratio of boys to girls is 2 to 3. For every 2 boys there are 3 girls.",
         A("ans", "Boys : girls = 2 : 3"), C("ans", "2 : 3")),
    beat("Two traps to dodge. 3 to 2 would be girls to boys. And 6 to 9 is the same ratio, but 3 still divides both, so it is not the simplest."),
    beat("So: write the numbers in the order asked, then divide both by the biggest number that goes into both."),
)

L["G4A_RATIO_002"] = lesson(
    beat("Here is the ratio 20 to 35. We want to write it with the smallest numbers we can.",
         G("q1", "20 : 35 in its simplest form = ?")),
    beat("To simplify a ratio, we divide both numbers by the same number. Which times table has both 20 and 35 in it?",
         ask=ask(["the 4 times table", "the 5 times table", "the 7 times table"], 1,
                 "4 goes into 20 but not into 35. 7 goes into 35 but not into 20. 5 goes into both of them.")),
    beat("So divide the first number by 5. 20 divided by 5 is 4.", W("w1", "20 ÷ 5 = 4")),
    beat("Careful: the second number must be divided by the very same 5. 35 divided by 5 is 7.", W("w2", "35 ÷ 5 = 7")),
    beat("So 20 to 35 becomes 4 to 7. The order stays the same: the 4 came from the 20, so it stays in front.",
         A("ans", "20 : 35 = 4 : 7"), C("ans", "4 : 7")),
    beat("Can we go further? No number bigger than 1 divides both 4 and 7. So 4 to 7 is the simplest form."),
    beat("Remember: divide both numbers by the same number, and keep them in the same order."),
)

L["G4A_RATIO_003"] = lesson(
    beat("4 notebooks cost 60 rupees. We want the cost of just 1 notebook.",
         G("q1", "4 notebooks cost ₹ 60"), G("q2", "1 notebook costs ₹ ?")),
    beat("Picture the 60 rupees spread equally over the 4 notebooks. Every notebook costs the same.",
         F(bars(bar(None, segs(4, "a", "?"), brace="₹ 60")))),
    beat("Will 1 notebook cost more than 60 rupees, or less?",
         ask=ask(["less than ₹ 60", "more than ₹ 60"], 0,
                 "One notebook is only a part of the four. So it must cost less than all four together.")),
    beat("Less, so we share. Sharing 60 equally into 4 means dividing by 4. And dividing by 4 is halving twice: half of 60 is 30, and half of 30 is 15.",
         W("w1", "60 ÷ 2 = 30"), W("w2", "30 ÷ 2 = 15"), W("w3", "60 ÷ 4 = 15")),
    beat("So 1 notebook costs 15 rupees.", A("ans", "1 notebook costs ₹ 15"), C("ans", "₹ 15")),
    beat("Let us check. 4 notebooks at 15 rupees each: 15 times 4 is 60. It works.", W("c1", "15 × 4 = 60")),
    beat("When you know the cost of several equal things, divide to find the cost of one."),
)

L["G4A_RATIO_004"] = lesson(
    beat("A bag has 3 red balls and 5 blue balls. We want the ratio of red balls to all the balls.",
         G("q1", "3 red balls and 5 blue balls"), G("q2", "Red : all the balls = ?")),
    beat("Read the last part slowly. Red is compared with all the balls, not with the blue ones. That is the trap in this question.",
         U("q2", "all the balls")),
    beat("So what do we need to find first?",
         ask=ask(["how many balls in all", "how many more blue than red", "nothing: just use 3 and 5"], 0,
                 "The ratio compares red with the whole bag. So first we need the number of balls in the whole bag.")),
    beat("3 red and 5 blue. 3 plus 5 is 8 balls in all.", W("w1", "3 + 5 = 8"), N("w1", "8", "all the balls")),
    beat("Red comes first, then all the balls. So the ratio is 3 to 8.", A("ans", "Red : all = 3 : 8"), C("ans", "3 : 8")),
    beat("3 to 5 would be red to blue. 5 to 8 would be blue to all. Each of those answers a different question.",
         Lb("n1", "(3 : 5 is red to blue)")),
    beat("So always ask yourself: which two things are being compared, and in which order?"),
)

L["G4A_RATIO_005"] = lesson(
    beat("We want a ratio that is equal to 2 to 3. There are four to choose from.",
         G("q1", "Which ratio is equal to 2 : 3?"), G("q2", "6 : 9     4 : 9     3 : 2     5 : 6")),
    beat("First, how do we make an equal ratio from 2 to 3?",
         ask=ask(["add the same number to both", "multiply both by the same number", "swap the two numbers"], 1,
                 "Adding changes a ratio, and swapping turns it round. Only multiplying both numbers by the same number keeps a ratio equal.")),
    beat("Let us try multiplying both by 3. 2 times 3 is 6, and 3 times 3 is 9.", W("w1", "2 × 3 = 6"), W("w2", "3 × 3 = 9")),
    beat("So 6 to 9 is equal to 2 to 3. And there it is in our list!", Lb("w3", "2 : 3 = 6 : 9"), C("q2", "6 : 9")),
    beat("What about 4 to 9? The 2 was multiplied by 2, but the 3 was multiplied by 3. Not the same multiplier, so it is not equal.",
         X("q2", "4 : 9")),
    beat("3 to 2 is the same numbers turned round, which is a different ratio. And 5 to 6 was made by adding 3 to both. Adding does not keep a ratio equal.",
         X("q2", "3 : 2"), X("q2", "5 : 6")),
    beat("So the answer is 6 to 9.", A("ans", "6 : 9 is equal to 2 : 3")),
    beat("Remember: equal ratios come from multiplying, or dividing, both numbers by the same number."),
)

L["G4A_RATIO_006"] = lesson(
    beat("Sana makes lemonade with 1 cup of lemon juice and 4 cups of water. Now she uses 3 cups of juice. How much water does she need?",
         G("q1", "1 cup juice with 4 cups water"), G("q2", "3 cups juice with ? cups water")),
    beat("Here is her mix. Every cup of juice brings 4 cups of water with it.",
         F(bars(bar("Juice", segs(1, "a")), bar("Water", segs(4, "b"))))),
    beat("The juice goes from 1 cup to 3 cups. How many times as much juice is that?",
         ask=ask(["2 times", "3 times", "4 times"], 1, "The juice went from 1 cup to 3 cups. 1 times 3 is 3, so it is 3 times as much.")),
    beat("To keep the same taste, the water must be 3 times as much too. Careful: we multiply the water. We do not just add 2 or 3 cups.",
         N("q1", "4 cups water", "× 3")),
    beat("4 times 3 is 12.", W("w1", "4 × 3 = 12")),
    beat("So she needs 12 cups of water.", A("ans", "She needs 12 cups of water"), C("ans", "12")),
    beat("Let us check. 1 to 4, and 3 to 12. Both numbers were multiplied by 3, so the lemonade tastes just the same.",
         Lb("c1", "1 : 4 = 3 : 12")),
    beat("When a mix must stay the same, whatever you multiply one part by, multiply the other part by the same number."),
)

L["G4A_RATIO_007"] = lesson(
    beat("A car travels 60 kilometres in 1 hour. We want to know how far it goes in 3 hours, at the same speed.",
         G("q1", "60 km in 1 hour"), G("q2", "? km in 3 hours")),
    beat("The same speed means it covers 60 kilometres in every single hour. One hour, then another, then another.",
         F({"kind": "journey", "places": ["Start", "1 hour", "2 hours", "3 hours"],
            "legs": [{"top": "60 km"}, {"top": "60 km"}, {"top": "60 km"}]})),
    beat("So how do we find the distance for 3 hours?",
         ask=ask(["60 + 3", "60 ÷ 3", "60 × 3"], 2, "Each of the 3 hours adds another 60 kilometres. 3 lots of 60 means 60 times 3.")),
    beat("60 and 60 and 60 is 60 times 3. We know 6 times 3 is 18, so 60 times 3 is 180.",
         W("w1", "60 + 60 + 60 = 180"), W("w2", "6 × 3 = 18"), W("w3", "60 × 3 = 180")),
    beat("So the car travels 180 kilometres in 3 hours.", A("ans", "180 km in 3 hours"), C("ans", "180 km")),
    beat("Does that make sense? More time on the road means more distance, and 180 is bigger than 60. Good."),
    beat("At a steady speed, multiply the distance for 1 hour by the number of hours."),
)

L["G4A_RATIO_008"] = lesson(
    beat("10 rupees buys 2 samosas. We want to know how many samosas 50 rupees buys, at the same price.",
         G("q1", "₹ 10 buys 2 samosas"), G("q2", "₹ 50 buys ? samosas")),
    beat("Think of the 50 rupees as a little pile of 10 rupee notes. How many tens are there in 50?",
         ask=ask(["5", "25", "40"], 0, "50 divided by 10 is 5. So there are 5 tens in 50.")),
    beat("50 divided by 10 is 5. So 50 rupees is 5 lots of 10 rupees.", W("w1", "50 ÷ 10 = 5"), N("w1", "5", "lots of ₹ 10", nth=2)),
    beat("Each lot of 10 rupees buys 2 samosas. So 5 lots buy 5 times as many. 2 times 5 is 10.", W("w2", "2 × 5 = 10")),
    beat("So 50 rupees buys 10 samosas.", A("ans", "₹ 50 buys 10 samosas"), C("ans", "10 samosas")),
    beat("Careful with one trap. The 5 is only the number of lots. Each lot buys 2 samosas, so we must still double it."),
    beat("Let us check. 10 samosas is 5 pairs. Each pair costs 10 rupees, and 5 times 10 is 50 rupees. It fits.", W("c1", "5 × 10 = 50")),
    beat("So find how many times bigger the money is. The samosas grow by the same number of times."),
)

L["G4A_RATIO_009"] = lesson(
    beat("Sweets are shared between two children in the ratio 3 to 7. Into how many equal parts are they divided altogether?",
         G("q1", "Sweets shared in the ratio 3 : 7"), G("q2", "Equal parts altogether = ?")),
    beat("The ratio tells us how the sweets are cut up. One child gets 3 equal parts. The other child gets 7 equal parts.",
         F(bars(bar(None, segs(3, "a") + segs(7, "b"))))),
    beat("To count all the parts, what do we do with 3 and 7?",
         ask=ask(["add them", "multiply them", "subtract them"], 0,
                 "We are putting the first child's parts and the second child's parts together. Putting together means adding.")),
    beat("3 parts and 7 parts. 3 plus 7 is 10.", W("w1", "3 + 7 = 10")),
    beat("So the sweets are divided into 10 equal parts altogether.", A("ans", "10 equal parts altogether"), C("ans", "10")),
    beat("You can count the pieces in the bar to check: 3 in one colour, 7 in the other, 10 in all."),
    beat("This is the first step of every sharing question: add the ratio numbers to count the parts."),
)

L["G4A_RATIO_010"] = lesson(
    beat("A tailor needs 2 metres of cloth for 1 shirt. He has 14 metres. How many shirts can he make?",
         G("q1", "1 shirt needs 2 metres of cloth"), G("q2", "14 metres make ? shirts")),
    beat("Each shirt uses up 2 metres. So we are really asking: how many 2s fit into 14?", U("q1", "2 metres")),
    beat("Which sum tells us how many 2s are in 14?",
         ask=ask(["14 × 2", "14 − 2", "14 ÷ 2"], 2,
                 "14 times 2 would be the cloth for 14 shirts. Here 14 is the cloth, and we cut it into pieces of 2 metres. That is dividing.")),
    beat("14 divided by 2 is 7. Look at the cloth cut into 2 metre pieces: there are 7 of them.",
         W("w1", "14 ÷ 2 = 7"), F(bars(bar(None, segs(7, "a", "2 m"), brace="14 m")))),
    beat("So he can make 7 shirts.", A("ans", "He can make 7 shirts"), C("ans", "7 shirts")),
    beat("Let us check. 7 shirts with 2 metres each: 7 times 2 is 14 metres. All the cloth is used.", W("c1", "7 × 2 = 14")),
    beat("When each thing uses the same amount, divide the total by that amount to see how many you can make."),
)

L["G4A_RATIO_011"] = lesson(
    beat("We want the ratio of 50 paise to 2 rupees, in its simplest form.", G("q1", "50 paise : ₹ 2 in simplest form = ?")),
    beat("Stop! One amount is in paise and the other is in rupees. A ratio only works when both are in the same unit. And 1 rupee is 100 paise.",
         U("q1", "paise"), U("q1", "₹ 2"), Lb("f1", "₹ 1 = 100 paise")),
    beat("So how many paise make 2 rupees?",
         ask=ask(["20 paise", "200 paise", "2 paise"], 1, "1 rupee is 100 paise. So 2 rupees is 2 lots of 100 paise.")),
    beat("2 times 100 is 200. So 2 rupees is 200 paise, and our ratio is 50 to 200.", W("w1", "2 × 100 = 200"), Lb("w2", "50 : 200")),
    beat("Now simplify. Both numbers can be divided by 50. 50 divided by 50 is 1, and 200 divided by 50 is 4.",
         W("w3", "50 ÷ 50 = 1"), W("w4", "200 ÷ 50 = 4")),
    beat("So the ratio is 1 to 4. A 50 paise coin fits into 2 rupees exactly 4 times.",
         A("ans", "50 paise : ₹ 2 = 1 : 4"), C("ans", "1 : 4")),
    beat("If we had written 50 to 2 without changing the units, it would look as if 50 paise were more than 2 rupees. That cannot be right."),
    beat("So before any ratio: same units first, then simplify."),
)

L["G4A_RATIO_012"] = lesson(
    beat("A kabaddi club has 20 children, and 8 of them are girls. We want the ratio of girls to boys, in its simplest form.",
         G("q1", "20 children, 8 are girls"), G("q2", "Girls : boys in simplest form = ?")),
    beat("We know the girls: 8. But look closely. The 20 is all the children, not the boys. That is the trap here.",
         U("q1", "20 children")),
    beat("So how do we find the number of boys?",
         ask=ask(["20 + 8", "20 − 8", "20 ÷ 8"], 1, "The club has 20 children and 8 of them are girls. Take the girls away, and the boys are left.")),
    beat("20 minus 8 is 12. There are 12 boys.", W("w1", "20 − 8 = 12"), N("w1", "12", "boys")),
    beat("Girls first, then boys. That is 8 to 12.", Lb("w2", "8 : 12")),
    beat("Now simplify. 4 goes into both. 8 divided by 4 is 2, and 12 divided by 4 is 3.", W("w3", "8 ÷ 4 = 2"), W("w4", "12 ÷ 4 = 3")),
    beat("So the ratio of girls to boys is 2 to 3.", A("ans", "Girls : boys = 2 : 3"), C("ans", "2 : 3")),
    beat("Two things to remember: check what each number stands for, and keep the order the question asks for."),
)
