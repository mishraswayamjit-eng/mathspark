"""Lessons written one by one: G4A_RATIO_013 to G4A_RATIO_024."""
from g4_gr4_ratio_lib import (A, C, F, G, Lb, N, U, W, X, ask, bar, bars, beat, lesson, segs, table)

LESSONS = {}
L = LESSONS

L["G4A_RATIO_013"] = lesson(
    beat("5 kilograms of rice cost 300 rupees. We want the cost of 8 kilograms, at the same price.",
         G("q1", "5 kg of rice costs ₹ 300"), G("q2", "8 kg of rice costs ₹ ?")),
    beat("We cannot jump straight from 5 to 8. So we go through 1 kilogram first. How do we find the cost of 1 kilogram?",
         ask=ask(["300 × 5", "300 ÷ 5", "300 − 5"], 1,
                 "5 kilograms cost 300 rupees, and each kilogram costs the same. So share 300 into 5 equal parts.")),
    beat("300 divided by 5 is 60. So 1 kilogram costs 60 rupees.", W("w1", "300 ÷ 5 = 60"), N("w1", "60", "cost of 1 kg")),
    beat("Now 8 kilograms cost 8 times as much. 6 times 8 is 48, so 60 times 8 is 480.", W("w2", "6 × 8 = 48"), W("w3", "60 × 8 = 480")),
    beat("So 8 kilograms of rice cost 480 rupees.", A("ans", "8 kg of rice costs ₹ 480"), C("ans", "₹ 480")),
    beat("Here is the trap. 300 times 8 would be far too much, because 300 rupees is the price of 5 kilograms, not of 1."),
    beat("A quick check. 8 kilograms is 3 more than 5. Those 3 cost 3 times 60, which is 180. And 300 plus 180 is 480.",
         W("c1", "3 × 60 = 180"), W("c2", "300 + 180 = 480")),
    beat("So: find the cost of one first, then multiply by how many you need."),
)

L["G4A_RATIO_014"] = lesson(
    beat("120 rupees are shared among Amit, Bina and Chetan in the ratio 1 to 2 to 3. We want Chetan's share.",
         G("q1", "₹ 120 shared: Amit : Bina : Chetan = 1 : 2 : 3"), G("q2", "Chetan gets ₹ ?")),
    beat("Amit gets 1 part, Bina gets 2 parts and Chetan gets 3 parts. All the parts are the same size.",
         F(bars(bar("Amit", segs(1, "a")), bar("Bina", segs(2, "b")), bar("Chetan", segs(3, "c"))))),
    beat("How many equal parts are there altogether?",
         ask=ask(["3", "5", "6"], 2, "Add all three numbers of the ratio: 1 plus 2 plus 3.")),
    beat("1 plus 2 plus 3 is 6 parts.", W("w1", "1 + 2 + 3 = 6")),
    beat("The 120 rupees are shared into 6 equal parts. 12 divided by 6 is 2, so 120 divided by 6 is 20. One part is 20 rupees.",
         W("w0", "12 ÷ 6 = 2"), W("w2", "120 ÷ 6 = 20"), N("w2", "20", "one part", "below", 2)),
    beat("Chetan has 3 parts. 3 times 20 is 60.", W("w3", "3 × 20 = 60")),
    beat("So Chetan gets 60 rupees. Notice that 20 rupees is only one part. That is Amit's share, not Chetan's.",
         A("ans", "Chetan gets ₹ 60"), C("ans", "₹ 60")),
    beat("Let us check. Amit 20, Bina 40, Chetan 60. Together that is 120 rupees. Nothing is left over.", W("c1", "20 + 40 + 60 = 120")),
    beat("So for sharing in a ratio: count the parts, find one part, then multiply by the parts that person has."),
)

L["G4A_RATIO_015"] = lesson(
    beat("Pencils and pens are in the ratio 4 to 3. There are 28 pencils. We want the pencils and pens altogether.",
         G("q1", "Pencils : pens = 4 : 3"), G("q2", "28 pencils. Pencils and pens altogether = ?")),
    beat("Pencils are 4 parts and pens are 3 parts. And we are told the pencils: 28 of them.",
         F(bars(bar("Pencils", segs(4, "a"), brace="28"), bar("Pens", segs(3, "b"))))),
    beat("The 28 pencils are 4 parts. So how big is one part?",
         ask=ask(["28 ÷ 3", "28 ÷ 4 = 7", "28 ÷ 7 = 4"], 1,
                 "The 28 belongs to the pencils, and the pencils have 4 parts. So share 28 into 4 equal parts.")),
    beat("28 divided by 4 is 7. One part is 7.", W("w1", "28 ÷ 4 = 7"), N("w1", "7", "one part")),
    beat("Pens are 3 parts. 3 times 7 is 21 pens.", W("w2", "3 × 7 = 21"), N("w2", "21", "pens")),
    beat("But wait. The question does not ask for the pens. It asks for pencils and pens altogether.", U("q2", "altogether")),
    beat("28 pencils plus 21 pens is 49.", W("w3", "28 + 21 = 49"), A("ans", "49 pencils and pens altogether"), C("ans", "49")),
    beat("Another way to see it: 4 parts and 3 parts make 7 parts, and 7 parts of 7 is 49. The same answer.", W("c1", "7 × 7 = 49")),
    beat("Use the amount you know to find one part. Then read the question again to see what it really asks for."),
)

L["G4A_RATIO_016"] = lesson(
    beat("A train covers 240 kilometres in 4 hours. At the same speed, how many hours does it take to cover 420 kilometres?",
         G("q1", "240 km in 4 hours"), G("q2", "420 km in ? hours")),
    beat("First, how far does the train go in just 1 hour?",
         ask=ask(["240 × 4", "420 − 240", "240 ÷ 4"], 2,
                 "The train covers 240 kilometres in 4 equal hours. Share 240 into 4 parts to get the distance for 1 hour.")),
    beat("24 divided by 4 is 6, so 240 divided by 4 is 60. The train covers 60 kilometres every hour.",
         W("w1", "24 ÷ 4 = 6"), W("w2", "240 ÷ 4 = 60"), N("w2", "60", "km in 1 hour")),
    beat("Now we ask: how many lots of 60 kilometres are there in 420? Each lot takes 1 hour. 42 divided by 6 is 7, so 420 divided by 60 is 7.",
         W("w3", "42 ÷ 6 = 7"), W("w4", "420 ÷ 60 = 7")),
    beat("So the train takes 7 hours.", A("ans", "420 km takes 7 hours"), C("ans", "7 hours")),
    beat("Careful: 60 is not the answer. 60 is the kilometres in one hour, and the question asks for hours."),
    beat("Let us check. 7 hours at 60 kilometres each hour: 60 times 7 is 420. It works.", W("c1", "60 × 7 = 420")),
    beat("So find what happens in 1 hour. Then divide the new distance by it."),
)

L["G4A_RATIO_017"] = lesson(
    beat("A recipe for 6 people needs 300 grams of flour. We want the flour for 4 people.",
         G("q1", "6 people need 300 grams of flour"), G("q2", "4 people need ? grams")),
    beat("Before any sums: fewer people this time. So will we need more flour, or less?",
         ask=ask(["less than 300 grams", "more than 300 grams"], 0,
                 "4 people eat less than 6 people. So the answer must be smaller than 300 grams.")),
    beat("Good. That already tells us 300 times 4 cannot be right. Now find the flour for 1 person. 30 divided by 6 is 5, so 300 divided by 6 is 50 grams.",
         W("w1", "30 ÷ 6 = 5"), W("w2", "300 ÷ 6 = 50"), N("w2", "50", "for 1 person")),
    beat("For 4 people we need 4 times that. 50 times 4 is 200.", W("w3", "50 × 4 = 200")),
    beat("So 4 people need 200 grams of flour.", A("ans", "4 people need 200 grams"), C("ans", "200 grams")),
    beat("Let us check. 200 is less than 300, just as we expected. And the 2 missing people would need 2 times 50, which is 100 more. That takes us back to 300.",
         W("c1", "2 × 50 = 100"), W("c2", "200 + 100 = 300")),
    beat("So find the amount for one person first, then multiply by the number of people you are cooking for."),
)

L["G4A_RATIO_018"] = lesson(
    beat("45 mangoes are shared between Kiran and Leela in the ratio 4 to 5. How many more mangoes does Leela get than Kiran?",
         G("q1", "45 mangoes. Kiran : Leela = 4 : 5"), G("q2", "How many more does Leela get?")),
    beat("Kiran gets 4 parts and Leela gets 5 parts.", F(bars(bar("Kiran", segs(4, "a")), bar("Leela", segs(5, "b"))))),
    beat("4 plus 5 is 9 parts in all. 45 divided by 9 is 5. So one part is 5 mangoes.",
         W("w1", "4 + 5 = 9"), W("w2", "45 ÷ 9 = 5"), N("w2", "5", "one part", "below", 2)),
    beat("Now look at the two bars. How many parts longer is Leela's bar than Kiran's?",
         ask=ask(["1 part", "5 parts", "9 parts"], 0, "Leela has 5 parts and Kiran has 4. 5 minus 4 is 1, so Leela has just 1 part more.")),
    beat("Just 1 part more. And one part is 5 mangoes. So Leela gets 5 more mangoes.",
         W("w3", "5 − 4 = 1"), A("ans", "Leela gets 5 more mangoes"), C("ans", "5 more")),
    beat("Let us check with the real shares. Kiran gets 4 times 5, which is 20. Leela gets 5 times 5, which is 25. And 25 minus 20 is 5.",
         W("c1", "4 × 5 = 20"), W("c2", "5 × 5 = 25"), W("c3", "25 − 20 = 5")),
    beat("Notice that 20 and 25 are the two shares, and 9 is the number of parts. The question asked only for how many more."),
    beat("To compare two shares, find one part, then count how many parts apart they are."),
)

L["G4A_RATIO_019"] = lesson(
    beat("On a map, 2 centimetres stands for 10 kilometres. Two towns are 7 centimetres apart on the map. How far apart are they really?",
         G("q1", "On the map: 2 cm stands for 10 km"), G("q2", "7 cm stands for ? km")),
    beat("We know what 2 centimetres stands for. Let us find what 1 centimetre stands for. How?",
         ask=ask(["10 × 2", "10 ÷ 2", "10 − 2"], 1, "1 centimetre is half of 2 centimetres. So it stands for half of 10 kilometres.")),
    beat("10 divided by 2 is 5. So every centimetre on the map is 5 kilometres on the ground.",
         W("w1", "10 ÷ 2 = 5"), N("w1", "5", "km for 1 cm")),
    beat("The towns are 7 centimetres apart. 7 times 5 is 35.", W("w2", "7 × 5 = 35")),
    beat("So the towns are really 35 kilometres apart.", A("ans", "The towns are 35 km apart"), C("ans", "35 km")),
    beat("The trap is 7 times 10. But 10 kilometres goes with 2 centimetres, not with 1. That is why we halved first.", U("q1", "2 cm")),
    beat("Check by counting along the map. 2 centimetres is 10, 4 is 20, 6 is 30, and 1 more centimetre adds 5. That makes 35.",
         F(table(["On the map (cm)", "Really (km)"], [["2", "10"], ["4", "20"], ["6", "30"], ["7", "35"]]))),
    beat("So find what 1 centimetre stands for, then multiply by the number of centimetres."),
)

L["G4A_RATIO_020"] = lesson(
    beat("Here is a ratio with three numbers: 18 to 24 to 30. We want its simplest form.",
         G("q1", "18 : 24 : 30 in its simplest form = ?")),
    beat("Three numbers, but the idea is the same: divide all of them by the same number. Which times table has 18, 24 and 30 in it?",
         ask=ask(["the 6 times table", "the 8 times table", "the 9 times table"], 0,
                 "8 goes into 24 but not into 18. 9 goes into 18 but not into 24. 6 goes into all three.")),
    beat("Divide each one by 6. 18 gives 3. 24 gives 4. 30 gives 5.",
         W("w1", "18 ÷ 6 = 3"), W("w2", "24 ÷ 6 = 4"), W("w3", "30 ÷ 6 = 5")),
    beat("So the simplest form is 3 to 4 to 5.", A("ans", "18 : 24 : 30 = 3 : 4 : 5"), C("ans", "3 : 4 : 5")),
    beat("What if you had only halved them? You would get 9 to 12 to 15. A fine start, but 3 still divides all of those, so it is not finished.",
         Lb("n1", "9 : 12 : 15 (3 still divides all)")),
    beat("How do we know 3 to 4 to 5 is finished? No number bigger than 1 goes into all of 3, 4 and 5."),
    beat("So keep dividing all the numbers by the same number, until nothing more divides them all."),
)

L["G4A_RATIO_021"] = lesson(
    beat("Careful with this one: it asks which ratio is NOT equal to 4 to 6. Three are equal, and one is the odd one out.",
         G("q1", "Which ratio is NOT equal to 4 : 6?"), G("q2", "6 : 8     2 : 3     8 : 12     12 : 18"), U("q1", "NOT")),
    beat("A good plan is to simplify 4 to 6 first. Halve both numbers and we get 2 to 3.",
         W("w1", "4 ÷ 2 = 2"), W("w2", "6 ÷ 2 = 3"), Lb("w3", "4 : 6 = 2 : 3")),
    beat("So 2 to 3 is equal: cross it off. Next, 8 to 12. Divide both by 4 and we get 2 to 3 again. Equal, so cross it off too.",
         X("q2", "2 : 3"), W("w4", "8 ÷ 4 = 2"), W("w5", "12 ÷ 4 = 3"), X("q2", "8 : 12")),
    beat("12 to 18. Divide both by 6, and it is 2 to 3 once more. Equal.",
         W("w6", "12 ÷ 6 = 2"), W("w7", "18 ÷ 6 = 3"), X("q2", "12 : 18")),
    beat("That leaves 6 to 8. Halve both numbers. What do we get?",
         ask=ask(["2 : 3", "3 : 4", "3 : 2"], 1, "Half of 6 is 3, and half of 8 is 4. So 6 to 8 becomes 3 to 4.")),
    beat("6 to 8 simplifies to 3 to 4, not 2 to 3. So it is not equal to 4 to 6.", W("w8", "6 ÷ 2 = 3"), W("w9", "8 ÷ 2 = 4")),
    beat("The odd one out is 6 to 8.", C("q2", "6 : 8"), A("ans", "6 : 8 is NOT equal to 4 : 6")),
    beat("Why does it look so tempting? 6 to 8 is 4 to 6 with 2 added to each number. Adding does not keep a ratio equal. Only multiplying or dividing does."),
)

L["G4A_RATIO_022"] = lesson(
    beat("A machine fills 45 bottles in 9 minutes. We want to know how many it fills in 1 hour, at the same rate.",
         G("q1", "45 bottles in 9 minutes"), G("q2", "? bottles in 1 hour")),
    beat("First, how many bottles in 1 minute? 45 divided by 9 is 5. So the machine fills 5 bottles every minute.",
         W("w1", "45 ÷ 9 = 5"), N("w1", "5", "in 1 minute", "below", 2)),
    beat("Now look: the question says 1 hour, not minutes. How many minutes are there in 1 hour?",
         ask=ask(["10", "60", "100"], 1, "An hour on the clock has 60 minutes. Not 100, even though 100 feels like a round number.")),
    beat("1 hour is 60 minutes. Always make the units match before you multiply.", U("q2", "1 hour"), Lb("w2", "1 hour = 60 minutes")),
    beat("5 bottles a minute, for 60 minutes. 5 times 6 is 30, so 5 times 60 is 300.", W("w3", "5 × 6 = 30"), W("w4", "5 × 60 = 300")),
    beat("So the machine fills 300 bottles in 1 hour.", A("ans", "300 bottles in 1 hour"), C("ans", "300")),
    beat("There were two traps. One is stopping at 5, which is only one minute. The other is treating an hour as 100 minutes."),
    beat("So find the amount for 1 minute, change the hour into minutes, and then multiply."),
)

L["G4A_RATIO_023"] = lesson(
    beat("Arun's stamps and Bela's stamps are in the ratio 3 to 5. Bela has 12 more stamps than Arun. How many does Arun have?",
         G("q1", "Arun : Bela = 3 : 5"), G("q2", "Bela has 12 more stamps. Arun = ?")),
    beat("Arun has 3 parts and Bela has 5 parts. Look at the bars: Bela's bar sticks out past Arun's.",
         F(bars(bar("Arun", segs(3, "a")), bar("Bela", segs(3, "a") + segs(2, "c"))))),
    beat("How many parts longer is Bela's bar?",
         ask=ask(["2 parts", "5 parts", "8 parts"], 0, "Bela has 5 parts and Arun has 3. 5 minus 3 is 2 extra parts.")),
    beat("5 minus 3 is 2. And here is the key idea: those 2 extra parts are exactly the 12 extra stamps.",
         W("w1", "5 − 3 = 2"), N("w1", "2", "= 12 stamps")),
    beat("Careful, this is the trap. 12 is not one part. 12 is 2 parts. So one part is 12 divided by 2, which is 6.",
         W("w2", "12 ÷ 2 = 6"), N("w2", "6", "one part")),
    beat("Arun has 3 parts. 3 times 6 is 18. So Arun has 18 stamps.", W("w3", "3 × 6 = 18"), A("ans", "Arun has 18 stamps"), C("ans", "18")),
    beat("Let us check. Bela has 5 times 6, which is 30. And 30 minus 18 is 12 more. It fits.", W("c1", "5 × 6 = 30"), W("c2", "30 − 18 = 12")),
    beat("When you are told how many more, match it with the extra parts. Then find one part."),
)

L["G4A_RATIO_024"] = lesson(
    beat("A playground's length and breadth are in the ratio 5 to 3. The length is 40 metres. We want the perimeter.",
         G("q1", "Length : breadth = 5 : 3"), G("q2", "Length = 40 m. Perimeter = ? m")),
    beat("There are two jobs here. First use the ratio to find the breadth. Then go all the way round for the perimeter."),
    beat("The length is 5 parts and it is 40 metres. How big is one part?",
         ask=ask(["40 ÷ 3", "40 ÷ 5 = 8", "40 ÷ 8 = 5"], 1,
                 "The 40 metres is the length, and the length has 5 parts. So share 40 into 5 equal parts.")),
    beat("40 divided by 5 is 8. The breadth is 3 parts, and 3 times 8 is 24 metres.",
         W("w1", "40 ÷ 5 = 8"), W("w2", "3 × 8 = 24"), N("w2", "24", "breadth")),
    beat("Now the perimeter. Here is where many children slip. A rectangle has 2 lengths and 2 breadths. So what do we add?",
         ask=ask(["40 + 24", "40 × 24", "40 + 24 + 40 + 24"], 2,
                 "40 plus 24 is one length and one breadth, only halfway round. And 40 times 24 would be the area. Go round all four sides.")),
    beat("One length and one breadth make 64. That is halfway round. Double it: 64 times 2 is 128.",
         W("w3", "40 + 24 = 64"), W("w4", "64 × 2 = 128")),
    beat("So the perimeter of the playground is 128 metres.", A("ans", "Perimeter = 128 m"), C("ans", "128 m")),
    beat("Use the ratio to find the missing side. Then remember: perimeter means all the way round."),
)
