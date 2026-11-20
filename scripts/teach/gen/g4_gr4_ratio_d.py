"""Lessons written one by one: G4A_RATIO_037 to G4A_RATIO_046, and Q_CH09_018."""
from g4_gr4_ratio_lib import (A, C, F, G, Lb, N, U, W, X, ask, bar, bars, beat, lesson, seg, segs)

LESSONS = {}
L = LESSONS

L["G4A_RATIO_037"] = lesson(
    beat("A temple bell rings 4 times in 6 seconds, timed from the first ring to the last. How long will it take to ring 12 times?",
         G("q1", "4 rings take 6 seconds, first ring to last"), G("q2", "12 rings take ? seconds")),
    beat("The clock starts at the first ring and stops at the last one. So the time is not in the rings. It is in the quiet gaps between them."),
    beat("4 rings. How many gaps are there between them?",
         ask=ask(["3 gaps", "4 gaps", "5 gaps"], 0, "Hold up 4 fingers and count the spaces between them. There are 3 spaces.")),
    beat("3 gaps take 6 seconds. So each gap is 6 divided by 3, which is 2 seconds. See the rings on the line, 2 seconds apart.",
         W("w1", "4 − 1 = 3"), W("w2", "6 ÷ 3 = 2"), N("w2", "2", "seconds per gap"),
         F({"kind": "numberLine", "min": 0, "max": 6, "step": 2,
            "points": [{"at": 0, "label": "ring"}, {"at": 2, "label": "ring"}, {"at": 4, "label": "ring"}, {"at": 6, "label": "ring"}]})),
    beat("Now 12 rings. The gaps are one fewer than the rings. 12 minus 1 is 11 gaps.", W("w3", "12 − 1 = 11")),
    beat("11 gaps of 2 seconds each. 11 times 2 is 22. So 12 rings take 22 seconds.",
         W("w4", "11 × 2 = 22"), A("ans", "12 rings take 22 seconds"), C("ans", "22")),
    beat("Two traps here. 12 rings is 3 times 4 rings, but 3 times 6 seconds is not the answer. And 12 gaps would be one gap too many."),
    beat("Whenever something happens again and again, the time is in the gaps. And the gaps are one fewer than the rings."),
)

L["G4A_RATIO_038"] = lesson(
    beat("Two jugs, 8 cups each. Jug A is juice to water 1 to 3. Jug B is juice to water 1 to 1. We pour both into a pot and want the new ratio.",
         G("q1", "Jug A: 8 cups, juice : water = 1 : 3"), G("q2", "Jug B: 8 cups, juice : water = 1 : 1"),
         G("q3", "Mixed together, juice : water = ?")),
    beat("It is tempting to add the ratio numbers. But a part in Jug A is not the same size as a part in Jug B. So we find the real cups in each jug."),
    beat("Jug A has 1 plus 3, which is 4 parts. 8 cups divided by 4 is 2 cups in each part. So it has 2 cups of juice, and 3 times 2 is 6 cups of water.",
         W("w1", "1 + 3 = 4"), W("w2", "8 ÷ 4 = 2"), W("w3", "3 × 2 = 6"), Lb("w4", "Jug A: 2 cups juice, 6 cups water")),
    beat("Jug B is 1 to 1, and it also holds 8 cups. How many cups of juice are in Jug B?",
         ask=ask(["1 cup", "2 cups", "4 cups"], 2, "1 to 1 means equal amounts of juice and water. Half of 8 cups is 4 cups.")),
    beat("Half of 8 is 4. Jug B has 4 cups of juice and 4 cups of water.", W("w5", "8 ÷ 2 = 4"), Lb("w6", "Jug B: 4 cups juice, 4 cups water")),
    beat("Now pour them together. Juice: 2 plus 4 is 6 cups. Water: 6 plus 4 is 10 cups.",
         W("w7", "2 + 4 = 6"), N("w7", "6", "juice"), W("w8", "6 + 4 = 10"), N("w8", "10", "water")),
    beat("So juice to water is 6 to 10. Halve both numbers: 3 to 5.", Lb("w9", "6 : 10"), W("w10", "6 ÷ 2 = 3"), W("w11", "10 ÷ 2 = 5")),
    beat("The ratio in the pot is 3 to 5. Juice comes first, because the question says juice to water.",
         A("ans", "Juice : water = 3 : 5"), C("ans", "3 : 5")),
    beat("Never add ratio numbers from two different mixes. Go to real amounts, add those, then simplify."),
)

L["G4A_RATIO_039"] = lesson(
    beat("The ratio of boys to girls in a class is exactly 4 to 5. Which of these could be the number of children in the class?",
         G("q1", "Boys : girls = 4 : 5 exactly"), G("q2", "Children in the class: 36, 40, 32 or 25?")),
    beat("The class is cut into equal parts: 4 parts are boys and 5 parts are girls.", F(bars(bar(None, segs(4, "a") + segs(5, "b"))))),
    beat("How many equal parts make the whole class?",
         ask=ask(["4", "5", "9"], 2, "Boys and girls together make the class. 4 parts plus 5 parts is 9 parts.")),
    beat("4 plus 5 is 9. And every part is a whole number of children. You cannot have half a child! So the class must be in the 9 times table.",
         W("w1", "4 + 5 = 9")),
    beat("Let us test them. 36 is 9 times 4. Yes! But 40, 32 and 25 are not in the 9 times table.",
         W("w2", "9 × 4 = 36"), C("q2", "36"), X("q2", "40"), X("q2", "32"), X("q2", "25")),
    beat("Why are the others tempting? 40 and 32 can be divided by 4, and 25 by 5. But 4 and 5 are only the boys' parts and the girls' parts. The whole class is 9 parts."),
    beat("Check. Each part is 4 children. Boys are 4 times 4, which is 16. Girls are 5 times 4, which is 20. And 16 plus 20 is 36.",
         W("c1", "4 × 4 = 16"), W("c2", "5 × 4 = 20"), W("c3", "16 + 20 = 36")),
    beat("So the class could have 36 children. With a ratio, the total is always a multiple of the number of parts.",
         A("ans", "The class could have 36 children")),
)

L["G4A_RATIO_040"] = lesson(
    beat("An auto-rickshaw fare is a starting charge plus the same amount for every kilometre. 3 kilometres cost 50 rupees and 5 kilometres cost 70 rupees. What do 10 kilometres cost?",
         G("q1", "Fare = starting charge + the same for every km"), G("q2", "3 km costs ₹ 50.  5 km costs ₹ 70.  10 km = ₹ ?")),
    beat("This fare has two pieces. A starting charge, which you pay only once. And an amount for every kilometre. So doubling the distance will not double the fare.",
         U("q1", "starting charge")),
    beat("Compare the two rides. The second one is 2 kilometres longer, and it costs 20 rupees more.",
         W("w1", "5 − 3 = 2"), W("w2", "70 − 50 = 20")),
    beat("So what does 1 extra kilometre cost?",
         ask=ask(["₹ 20", "₹ 14", "₹ 10"], 2, "2 extra kilometres cost 20 rupees. Share that between the 2 kilometres: 20 divided by 2.")),
    beat("20 divided by 2 is 10. Each kilometre costs 10 rupees.", W("w3", "20 ÷ 2 = 10"), N("w3", "10", "for each km")),
    beat("Now the starting charge. In the 3 kilometre ride, the distance costs 3 times 10, which is 30. The ride cost 50, so the starting charge is 50 minus 30, which is 20.",
         W("w4", "3 × 10 = 30"), W("w5", "50 − 30 = 20"), N("w5", "20", "starting charge")),
    beat("For 10 kilometres: 10 times 10 is 100 for the distance, plus the 20 to start. That is 120.",
         W("w6", "10 × 10 = 100"), W("w7", "100 + 20 = 120")),
    beat("So a 10 kilometre ride costs 120 rupees. It is not double the 5 kilometre fare, because the starting charge is paid only once.",
         A("ans", "A 10 km ride costs ₹ 120"), C("ans", "₹ 120")),
    beat("Check with the other ride. 5 kilometres is 50 for the distance, plus 20 to start. That makes 70. It fits.", W("c1", "5 × 10 + 20 = 70")),
    beat("So compare two cases to find the cost of one extra. Then find the fixed part. The answer here is 120 rupees."),
)

L["G4A_RATIO_041"] = lesson(
    beat("Ravi and Sita share 60 sweets in the ratio 7 to 3. Ravi wants them both to have the same number. How many must he give to Sita?",
         G("q1", "60 sweets. Ravi : Sita = 7 : 3"), G("q2", "Ravi gives Sita some. Now equal. How many?")),
    beat("First the shares. 7 plus 3 is 10 parts, and 60 divided by 10 is 6. One part is 6 sweets.",
         W("w1", "7 + 3 = 10"), W("w2", "60 ÷ 10 = 6"), N("w2", "6", "one part", "below", 2)),
    beat("Ravi has 7 times 6, which is 42. Sita has 3 times 6, which is 18.",
         W("w3", "7 × 6 = 42"), N("w3", "42", "Ravi"), W("w4", "3 × 6 = 18"), N("w4", "18", "Sita")),
    beat("When they are equal, how many sweets will each child have?",
         ask=ask(["24", "30", "42"], 1, "There are still 60 sweets altogether. Equal shares means half each, and half of 60 is 30.")),
    beat("Half of 60 is 30. Each child should end with 30.", W("w5", "60 ÷ 2 = 30")),
    beat("Ravi must come down from 42 to 30. 42 minus 30 is 12.", W("w6", "42 − 30 = 12")),
    beat("So Ravi must give 12 sweets. Check Sita: 18 plus 12 is 30. Both have 30.",
         A("ans", "Ravi must give 12 sweets"), C("ans", "12"), W("c1", "18 + 12 = 30")),
    beat("Here is the trap. Ravi has 24 more than Sita, but he gives only half of that. Every sweet he gives lowers him by 1 and lifts her by 1.",
         W("c2", "42 − 18 = 24")),
    beat("So to make two shares equal, find what each should have, and move the difference. The answer is 12."),
)

L["G4A_RATIO_042"] = lesson(
    beat("Two-thirds of Asha's stickers is the same number as one-half of Bina's stickers. We want the ratio of Asha's stickers to Bina's.",
         G("q1", "2/3 of Asha's stickers = 1/2 of Bina's stickers"), G("q2", "Asha : Bina = ?")),
    beat("No numbers of stickers are given. So let us choose one! Pick an easy number for the equal amount. Let us say it is 6 stickers.",
         Lb("t1", "Try: the equal amount is 6 stickers")),
    beat("Half of Bina's stickers is 6. So Bina has 6 times 2, which is 12.", W("w1", "6 × 2 = 12"), N("w1", "12", "Bina")),
    beat("Two-thirds of Asha's stickers is 6. So how much is one-third of Asha's stickers?",
         ask=ask(["3", "6", "12"], 0, "Two-thirds means 2 equal pieces out of 3. If 2 pieces make 6, then one piece is half of 6, which is 3.")),
    beat("One-third is 3. Asha's stickers are 3 thirds, so 3 times 3 is 9.", W("w2", "6 ÷ 2 = 3"), W("w3", "3 × 3 = 9"), N("w3", "9", "Asha")),
    beat("Look at the bars. Asha has 9 and Bina has 12. Two of Asha's pieces match one of Bina's.",
         F(bars(bar("Asha", [seg("3", 3, "a"), seg("3", 3, "a"), seg("3", 3, "a")]),
                bar("Bina", [seg("6", 6, "b"), seg("6", 6, "b")])))),
    beat("Asha to Bina is 9 to 12. Divide both by 3, and we get 3 to 4.", Lb("w4", "9 : 12"), W("w5", "9 ÷ 3 = 3"), W("w6", "12 ÷ 3 = 4")),
    beat("So the ratio is 3 to 4. Asha has fewer stickers. That makes sense: she needs a bigger fraction of hers to match Bina.",
         A("ans", "Asha : Bina = 3 : 4"), C("ans", "3 : 4")),
    beat("Check: two-thirds of 9 is 6, and half of 12 is 6. Equal, just as the question says.", W("c1", "2/3 of 9 = 6"), W("c2", "1/2 of 12 = 6")),
    beat("When no numbers are given, choose an easy one and try it. The ratio comes out as 3 to 4."),
)

L["G4A_RATIO_043"] = lesson(
    beat("4 hens lay 12 eggs in 3 days. At the same steady rate, how many eggs will 6 hens lay in 5 days?",
         G("q1", "4 hens lay 12 eggs in 3 days"), G("q2", "6 hens in 5 days lay ? eggs")),
    beat("Two things change at once here: the number of hens, and the number of days. So let us find what 1 hen does in 1 day."),
    beat("4 hens, each working for 3 days. Let us call that hen-days. 4 times 3 is 12 hen-days.",
         W("w1", "4 × 3 = 12"), N("w1", "12", "hen-days")),
    beat("12 hen-days gave 12 eggs. So how many eggs does 1 hen lay in 1 day?",
         ask=ask(["1 egg", "3 eggs", "4 eggs"], 0, "12 eggs shared over 12 hen-days: 12 divided by 12 is 1. One egg for each hen, each day.")),
    beat("12 divided by 12 is 1. Each hen lays 1 egg a day. Lovely and simple.", W("w2", "12 ÷ 12 = 1")),
    beat("Now 6 hens for 5 days. That is 6 times 5, which is 30 hen-days.", W("w3", "6 × 5 = 30"), N("w3", "30", "hen-days")),
    beat("At 1 egg for each hen-day, that is 30 eggs.", A("ans", "6 hens lay 30 eggs in 5 days"), C("ans", "30")),
    beat("The traps are changing only the hens, or only the days. Both changed, so we had to count both."),
    beat("When two things change together, go back to one of each: one hen, one day. Then build up again."),
)

L["G4A_RATIO_044"] = lesson(
    beat("Sweets are shared between Anu and Bala in the ratio 3 to 4, with none left over. The total is between 40 and 50, and Bala gets more than 25. How many does Anu get?",
         G("q1", "Anu : Bala = 3 : 4, none left over"), G("q2", "Total is between 40 and 50. Bala gets more than 25."),
         G("q3", "Anu gets ?")),
    beat("3 plus 4 is 7 parts. With none left over, the total must be in the 7 times table.", W("w1", "3 + 4 = 7")),
    beat("Which numbers in the 7 times table lie between 40 and 50?",
         ask=ask(["35 and 42", "42 and 49", "only 49"], 1, "7 times 6 is 42, and 7 times 7 is 49. Both of them are more than 40 and fewer than 50.")),
    beat("7 times 6 is 42, and 7 times 7 is 49. Two possible totals. Now we use the other clue to choose between them.",
         W("w2", "7 × 6 = 42"), W("w3", "7 × 7 = 49")),
    beat("Try 42. One part is 6, so Bala gets 4 times 6, which is 24. Is that more than 25? Not quite. So 42 is out.",
         W("w4", "4 × 6 = 24"), X("w2", "42")),
    beat("Try 49. One part is 7, so Bala gets 4 times 7, which is 28. That is more than 25. So there are 49 sweets.",
         W("w5", "4 × 7 = 28"), C("w3", "49")),
    beat("Anu gets 3 parts of 7. 3 times 7 is 21. So Anu gets 21 sweets.", W("w6", "3 × 7 = 21"), A("ans", "Anu gets 21 sweets"), C("ans", "21")),
    beat("Careful at the end: 28 is Bala's share, and the question asks for Anu. Check: 21 plus 28 is 49. It all fits.", W("c1", "21 + 28 = 49")),
    beat("When a puzzle has several clues, list what is possible, then test each one against the next clue."),
)

L["G4A_RATIO_045"] = lesson(
    beat("In a club, the ratio of girls to all the children is 3 to 8. There are 40 boys. How many girls are there?",
         G("q1", "Girls : all the children = 3 : 8"), G("q2", "There are 40 boys. Girls = ?")),
    beat("Read the ratio slowly. It is girls to all the children. The 8 is the whole club, not the boys. That is the trap.",
         U("q1", "all the children")),
    beat("Out of every 8 parts, 3 are girls. So how many parts are boys?",
         ask=ask(["5 parts", "8 parts", "11 parts"], 0, "The whole club is 8 parts. Take away the girls' 3 parts and the boys are left: 8 minus 3.")),
    beat("8 minus 3 is 5. The boys are 5 parts.", W("w1", "8 − 3 = 5"),
         F(bars(bar("The club", segs(3, "a", "girls") + segs(5, "b", "boys"))))),
    beat("The 40 boys are 5 parts. 40 divided by 5 is 8. So one part is 8 children.", W("w2", "40 ÷ 5 = 8"), N("w2", "8", "one part")),
    beat("Girls are 3 parts. 3 times 8 is 24. So there are 24 girls.", W("w3", "3 × 8 = 24"), A("ans", "There are 24 girls"), C("ans", "24")),
    beat("Check. 24 girls plus 40 boys is 64 children. That is 8 parts of 8, and the girls are 3 of those parts. It fits.",
         W("c1", "24 + 40 = 64"), W("c2", "64 ÷ 8 = 8")),
    beat("Always check what each number in a ratio stands for: one group, or the whole lot."),
)

L["G4A_RATIO_046"] = lesson(
    beat("Asha cycles 5 kilometres in the time Bala cycles 4. They start a 30 kilometre ride together. When Asha finishes, how far does Bala still have to go?",
         G("q1", "Asha cycles 5 km while Bala cycles 4 km"), G("q2", "30 km ride. Asha finishes. Bala has ? km to go")),
    beat("Every time Asha does 5 kilometres, Bala does only 4. So Bala slips 1 kilometre behind, again and again."),
    beat("Asha rides 30 kilometres. How many lots of 5 kilometres is that?",
         ask=ask(["5 lots", "6 lots", "25 lots"], 1, "Count how many 5s fit into 30. 30 divided by 5 is 6.")),
    beat("30 divided by 5 is 6. Asha rides 6 lots of 5 kilometres.", W("w1", "30 ÷ 5 = 6")),
    beat("In each of those 6 lots, Bala rides 4 kilometres. 6 times 4 is 24. So Bala has done 24 kilometres.",
         W("w2", "6 × 4 = 24"), N("w2", "24", "Bala so far")),
    beat("The ride is 30 kilometres. 30 minus 24 is 6. So Bala still has 6 kilometres to go.",
         W("w3", "30 − 24 = 6"), A("ans", "Bala still has 6 km to go"), C("ans", "6 km")),
    beat("Careful: 24 is how far Bala has gone. The question asks how far Bala still has to go."),
    beat("Here is another way to see it. Bala falls 1 kilometre behind in every lot, and there are 6 lots. So Bala is 6 kilometres behind."),
)

L["Q_CH09_018"] = lesson(
    beat("12 workers can build a wall in 10 days. We want to know how many days 15 workers need.",
         G("q1", "12 workers build a wall in 10 days"), G("q2", "15 workers take ? days")),
    beat("More workers this time. Will the wall take more days, or fewer?",
         ask=ask(["more than 10 days", "fewer than 10 days"], 1, "More hands share the same work, so each has less to do. The job finishes sooner.")),
    beat("Fewer days. So this is not like buying more pens for more money. Here, when one number goes up, the other comes down."),
    beat("Think of the whole wall as days of work for one worker. 12 workers for 10 days is 12 times 10, which is 120 days of work.",
         W("w1", "12 × 10 = 120"), N("w1", "120", "the whole wall")),
    beat("Now share those 120 days of work among 15 workers. 15 times 8 is 120, so 120 divided by 15 is 8.",
         W("w2", "15 × 8 = 120"), W("w3", "120 ÷ 15 = 8")),
    beat("So 15 workers need 8 days.", A("ans", "15 workers take 8 days"), C("ans", "8 days")),
    beat("Does it fit our guess? 8 is fewer than 10. Yes, more workers finished sooner."),
    beat("For workers and days: multiply to find the total work, then divide by the new number of workers."),
)
