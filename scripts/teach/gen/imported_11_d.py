"""Batch 11, part D: multiplication and division stories, each written by hand (second half)."""
from imported_11_lib import (ANS, ANSL, ARC, B, BOX, CHOOSE, CIRC, GIVEN, GROUP, LB, LESSON, NOTE,  # noqa: F401
                             STRIKE, UL, W)

P = "AIGEN_grade5_"

LESSONS = {}

# 164 red and 236 blue packets, all at 45 rupees.
LESSONS[P + "30f964e1-aa7c-4b8c-8e34-9fa245732030"] = LESSON(
    B("Meera's class bought 164 packets of red powder and 236 packets of blue, and every packet cost 45 rupees. Meera found a shortcut for the total.",
      GIVEN("q", "164 packets and 236 packets, each ₹45")),
    B("Both colours cost the same. What is Meera's shortcut?",
      ask=CHOOSE(["multiply 164 by 236", "add the packets, then multiply once", "add 45 and 45"], 1,
                 "When every packet costs the same, the colour does not matter. Count all the packets together first, then multiply by 45 just once.")),
    B("164 plus 236 is 400. A lovely round number, which is why the shortcut is worth spotting.",
      W("l1", "164 + 236 = 400"), UL("l1", "400")),
    B("Now 400 times 45. Start with 4 times 45, which is 180.",
      W("l2", "4 × 45 = 180")),
    B("400 is 4 hundreds, so 400 times 45 is 180 hundreds. That is 18,000 rupees.",
      ANS("l3", "400 × 45 = 18,000"), CIRC("l3", "18,000")),
    B("Here is why the shortcut works. 164 lots of 45 and 236 lots of 45 are the same as 164 plus 236 lots of 45.",
      W("l4", "164 × 45 + 236 × 45 = (164 + 236) × 45"), UL("l4", "(164 + 236)")),
    B("Check the long way. Red costs 7,380 and blue costs 10,620. Together they make 18,000.",
      W("l5", "164 × 45 = 7,380"), W("l6", "236 × 45 = 10,620"), W("l7", "7,380 + 10,620 = 18,000")),
    B("Both of those, 7,380 and 10,620, are among the choices. Each is just one colour. The question asks for the total."),
    B("So when different things cost the same, add them first and multiply once."),
)

# 125 laddoos a day for 8 days, 40 given away.
LESSONS[P + "321a7e1c-9ab9-466f-96b4-afe1f6e12b8a"] = LESSON(
    B("Ananya's mother makes 125 laddoos each day for 8 days. On the last day she gives 40 away. How many does she have at the end?",
      GIVEN("q", "125 laddoos a day for 8 days. 40 given away")),
    B("125 laddoos every day, for 8 days. How do we find how many she made?",
      ask=CHOOSE(["125 + 8", "125 × 8", "125 − 40"], 1,
                 "The same number, 125, is made again and again, 8 times over. Adding the same number many times is multiplication.")),
    B("125 times 8. Split 125 into 100 and 25. 100 times 8 is 800, and 25 times 8 is 200.",
      W("l1", "100 × 8 = 800"), W("l2", "25 × 8 = 200")),
    B("800 plus 200 is 1000. She made 1000 laddoos.",
      W("l3", "800 + 200 = 1000")),
    B("Careful: 1000 is among the choices, but the story is not over. She gives 40 away.",
      UL("q", "40 given away")),
    B("Giving away means taking off. 1000 minus 40 is 960. She has 960 laddoos.",
      ANS("l4", "1000 − 40 = 960"), CIRC("l4", "960")),
    B("Check by adding back. 960 plus 40 is 1000, and 1000 is 8 days of 125.",
      W("l5", "960 + 40 = 1000"), W("l6", "125 × 8 = 1000")),
    B("So read to the very end of the story. Multiply to find what was made, then take away what was given."),
)

# 13 pots of 24 cups at 15 rupees.
LESSONS[P + "3c480d38-865b-48b5-babb-23231022d8bf"] = LESSON(
    B("Each pot makes 24 cups of chai. Ravi's father sold 13 full pots, at 15 rupees a cup. How much did he earn?",
      GIVEN("q", "24 cups a pot, 13 pots, ₹15 a cup")),
    B("He is paid for each cup, not for each pot. So what do we need first?",
      ask=CHOOSE(["13 × 15", "24 + 13", "the number of cups"], 2,
                 "The price, 15 rupees, is for one cup. So before any money, we must know how many cups came out of 13 pots.")),
    B("13 pots of 24 cups. 10 pots make 240 cups, and 3 pots make 72.",
      W("l1", "10 × 24 = 240"), W("l2", "3 × 24 = 72")),
    B("240 plus 72 is 312 cups.",
      W("l3", "240 + 72 = 312")),
    B("Each cup is 15 rupees. 312 times 10 is 3120. 312 times 5 is half of that, 1560.",
      W("l4", "312 × 10 = 3120"), W("l5", "312 × 5 = 1560")),
    B("3120 plus 1560 is 4680. He earned 4,680 rupees.",
      ANS("l6", "3120 + 1560 = 4680"), CIRC("l6", "4680")),
    B("Notice we used all three numbers. Multiply only two of them, and a piece of the story is missing."),
    B("Check in a different order. One pot earns 24 times 15, which is 360 rupees. And 13 pots earn 13 times 360, which is 4680.",
      W("l7", "24 × 15 = 360"), W("l8", "13 × 360 = 4680")),
    B("So pots become cups, and cups become rupees. Two multiplications, one after the other."),
)

# 45 teams of 11 players, jerseys at 215 rupees.
LESSONS[P + "3d39e7e2-2749-41f1-921e-c8b59b14b97f"] = LESSON(
    B("There are 45 teams with 11 players each, and every player gets a jersey costing 215 rupees. What does the school spend?",
      GIVEN("q", "45 teams, 11 players each, ₹215 a jersey")),
    B("Every player needs a jersey. How many jerseys is that?",
      ask=CHOOSE(["45", "45 × 11", "45 + 11"], 1,
                 "There are 45 teams, and each team has 11 players. So the jerseys are 45 lots of 11.")),
    B("45 times 11. A neat way: 45 times 10 is 450, and one more 45 makes 495 jerseys.",
      W("l1", "45 × 10 = 450"), W("l2", "450 + 45 = 495")),
    B("Each jersey costs 215 rupees. 495 is awkward, but it is just 5 less than 500. So price 500 jerseys, then take 5 jerseys off.",
      W("l3", "495 = 500 − 5")),
    B("5 times 215 is 1,075. So 500 times 215 is 1,07,500.",
      W("l4", "5 × 215 = 1,075"), W("l5", "500 × 215 = 1,07,500")),
    B("Now take off the 5 extra jerseys, which cost 1,075. 1,07,500 minus 1,075 is 1,06,425 rupees.",
      ANS("l6", "1,07,500 − 1,075 = 1,06,425"), CIRC("l6", "1,06,425")),
    B("The trap is forgetting the players. 45 times 215 is only 9,675: one jersey for each team. That is among the choices.",
      W("l7", "45 × 215 = 9,675")),
    B("Check with a different split. 495 times 200 is 99,000. 495 times 15 is 7,425. Together, 1,06,425.",
      W("l8", "495 × 200 = 99,000"), W("l9", "495 × 15 = 7,425"), W("l10", "99,000 + 7,425 = 1,06,425")),
    B("So count the things first, teams times players. Then multiply by the price of one."),
)

# 84 batches of 375 mL, packets of 4500 mL.
LESSONS[P + "46e0bf0c-88df-4f60-9eaf-ff0b9af8b449"] = LESSON(
    B("Each batch of chai uses 375 millilitres of milk. Priya's family made 48 batches on Saturday and 36 on Sunday. Milk comes in packets of 4500 millilitres. How many packets?",
      GIVEN("q", "375 mL a batch. Batches 48 + 36. Packets of 4500 mL")),
    B("Every batch uses the same milk, so add the batches. 48 plus 36 is 84.",
      W("l1", "48 + 36 = 84")),
    B("What do we need next?",
      ask=CHOOSE(["84 + 375", "the milk used, 84 × 375", "4500 − 375"], 1,
                 "Packets are measured in millilitres of milk. So we need to know how many millilitres 84 batches use: 84 times 375.")),
    B("84 times 375. Split 375 into 300 and 75. 84 times 300 is 25,200. 84 times 75 is 6,300.",
      W("l2", "84 × 300 = 25,200"), W("l3", "84 × 75 = 6,300")),
    B("25,200 plus 6,300 is 31,500 millilitres.",
      W("l4", "25,200 + 6,300 = 31,500")),
    B("How many packets of 4500 is that? 31,500 divided by 4500. Drop two zeros from each number, and it becomes 315 divided by 45.",
      W("l5", "31,500 ÷ 4500 = 315 ÷ 45")),
    B("45 times 7 is 315. So they used exactly 7 packets, with nothing left over.",
      W("l6", "45 × 7 = 315"), ANS("l7", "31,500 ÷ 4500 = 7"), CIRC("l7", "7")),
    B("Check a second way. One packet makes 4500 divided by 375, which is 12 batches. And 84 batches divided by 12 is 7 packets.",
      W("l8", "4500 ÷ 375 = 12"), W("l9", "84 ÷ 12 = 7")),
    B("The word full is a warning. If the division had left a remainder, we would have had to think again. Here it comes out exactly."),
    B("So find the total used, in the same unit as the packet, and then divide by the size of one packet."),
)

# 600 laddoos in boxes of 24.
LESSONS[P + "476bc237-c567-43a4-9a54-bced0f8e2037"] = LESSON(
    B("Grandmother made 156, 228 and 216 laddoos over three days. She packs them in boxes of 24 and wants none left over. How many boxes does she need?",
      GIVEN("q", "Boxes of 24. Made 156, 228 and 216 laddoos")),
    B("First we need all the laddoos. 156 plus 228 is 384, and 384 plus 216 is 600.",
      W("l1", "156 + 228 = 384"), W("l2", "384 + 216 = 600")),
    B("She wants no laddoo left over. What must be true about 600?",
      ask=CHOOSE(["it is an even number", "it divides exactly by 24", "it is bigger than 24"], 1,
                 "No leftovers means the laddoos fill boxes of 24 exactly. So 600 divided by 24 must leave no remainder.")),
    B("Let's test it. 24 is 4 times 6, so divide by 4 first. 600 divided by 4 is 150.",
      W("l3", "24 = 4 × 6"), W("l4", "600 ÷ 4 = 150")),
    B("Then 150 divided by 6 is 25, with nothing left over.",
      W("l5", "150 ÷ 6 = 25")),
    B("So 600 divides exactly. She does not need to make even one more laddoo, and she needs 25 boxes.",
      ANS("l6", "600 ÷ 24 = 25"), CIRC("l6", "25")),
    B("The story talks about making a few more. That only happens when there is a remainder. Always test first, and don't add extras that are not needed."),
    B("Check. 25 boxes of 24: 25 times 4 is 100, and 100 times 6 is 600.",
      W("l7", "25 × 4 = 100"), W("l8", "100 × 6 = 600")),
    B("So find the total first, then divide. A remainder of 0 means everything packs exactly."),
)

# 148 boxes bought at 235, sold at 310, profit shared by 5.
LESSONS[P + "66077f8a-0238-49e4-8803-3c2d3a5dea3f"] = LESSON(
    B("Priya's family bought 148 boxes of sparklers at 235 rupees each and sold them at 310 rupees each. The whole profit is shared equally among 5 orphanages.",
      GIVEN("q", "148 boxes. Bought at ₹235, sold at ₹310. Shared by 5")),
    B("How much profit does one box make?",
      ask=CHOOSE(["310 + 235", "310", "310 − 235"], 2,
                 "The profit on a box is what it sold for, minus what it cost. It sold for 310 and cost 235, so we subtract.")),
    B("310 minus 235 is 75 rupees on every box.",
      W("l1", "310 − 235 = 75")),
    B("148 boxes, each making 75. Think of 75 as three quarters of 100. 148 times 100 is 14,800.",
      W("l2", "148 × 100 = 14,800")),
    B("A quarter of 14,800 is 3,700. Take that quarter away, and three quarters are left: 11,100 rupees of profit.",
      W("l3", "14,800 ÷ 4 = 3,700"), W("l4", "14,800 − 3,700 = 11,100")),
    B("Share it equally among the 5 orphanages. 11,100 divided by 5 is 2,220 rupees each.",
      ANS("l5", "11,100 ÷ 5 = 2,220"), CIRC("l5", "2,220")),
    B("Don't share out all the money from the sales. Only the profit is given away, so the cost of the boxes comes off first."),
    B("Check the sharing. 5 lots of 2,220 make 11,100.",
      W("l6", "5 × 2,220 = 11,100")),
    B("And check the profit with a different split. 148 times 70 is 10,360, 148 times 5 is 740, and together they make 11,100.",
      W("l7", "148 × 70 = 10,360"), W("l8", "148 × 5 = 740"), W("l9", "10,360 + 740 = 11,100")),
    B("So find the profit on one, multiply by how many, and then share."),
)

# 248 crates of 35 mangoes and 15 loose.
LESSONS[P + "6d058827-0035-4f1d-9410-97607edc8933"] = LESSON(
    B("Kiran's family filled 248 crates with 35 mangoes each, and had 15 loose mangoes left over. How many mangoes did the orchard produce?",
      GIVEN("q", "248 crates × 35 mangoes, and 15 loose mangoes")),
    B("The mangoes are in two places: packed in crates, and lying loose. Crates first. That is 248 times 35.",
      W("l1", "248 × 35 = ?")),
    B("Split 35 into 30 and 5. 248 times 30 is 7440.",
      W("l2", "248 × 30 = 7440")),
    B("248 times 10 is 2480, so 248 times 5 is half of that, 1240.",
      W("l3", "248 × 10 = 2480"), W("l4", "248 × 5 = 1240")),
    B("7440 plus 1240 is 8680 mangoes in crates.",
      W("l5", "7440 + 1240 = 8680")),
    B("Is 8680 the answer?",
      ask=CHOOSE(["Yes", "No, add the 15 loose mangoes", "No, take away 15"], 1,
                 "The 15 loose mangoes grew in the orchard too. They did not fit in a crate, but they still count, so we add them on.")),
    B("8680 plus 15 is 8695 mangoes in all.",
      UL("q", "15 loose mangoes"), ANS("l6", "8680 + 15 = 8695"), CIRC("l6", "8695")),
    B("Left over does not mean take away. Those 15 are extra mangoes, on top of the full crates."),
    B("Check the crates another way. 250 crates would hold 8750. We have 2 crates fewer, which is 70 mangoes, and 8750 minus 70 is 8680.",
      W("l7", "250 × 35 = 8750"), W("l8", "2 × 35 = 70"), W("l9", "8750 − 70 = 8680")),
    B("So the total is the full crates times the size of a crate, plus the loose ones."),
)

# 48 packets of 25 diyas, bags of 12.
LESSONS[P + "6ee00e3c-a631-4e21-a24f-633e70e7916a"] = LESSON(
    B("Ananya buys 48 packets with 25 diyas in each. She puts 12 diyas in every gift bag. How many bags can she make?",
      GIVEN("q", "48 packets × 25 diyas. Bags of 12 diyas")),
    B("What do we need to know before we fill any bags?",
      ask=CHOOSE(["how many diyas there are", "how many bags there are", "the price of a packet"], 0,
                 "Bags are filled with diyas, so first we count the diyas: 48 packets of 25.")),
    B("48 times 25. 4 times 25 is 100, and 48 is 4 times 12. So 48 times 25 is 12 hundreds, which is 1200 diyas.",
      W("l1", "4 × 25 = 100"), W("l2", "48 × 25 = 1200")),
    B("Now put 12 diyas in each bag. How many 12s are in 1200? 12 hundreds, shared into 12s, gives 1 hundred. She can make 100 bags.",
      ANS("l3", "1200 ÷ 12 = 100"), CIRC("l3", "100")),
    B("Careful with the zeros when dividing 1200 by 12. Both zeros stay, so the answer is 100, not 10."),
    B("Check by multiplying back. 100 bags of 12 diyas is 1200 diyas, exactly what she bought.",
      W("l4", "100 × 12 = 1200")),
    B("So multiply to find how many there are altogether. Then divide to share them into equal bags."),
)

# 215 + 148 crates, 12 damaged, 36 mangoes each.
LESSONS[P + "73619f49-2ba0-45b9-8720-d860671f667d"] = LESSON(
    B("Raju's uncle packs 36 mangoes in a crate. He packed 215 crates on Monday and 148 on Tuesday, and then 12 crates were damaged. How many mangoes are ready to sell?",
      GIVEN("q", "36 in a crate. Crates: 215 + 148, then 12 damaged")),
    B("All the crates first. 215 plus 148 is 363 crates.",
      W("l1", "215 + 148 = 363")),
    B("12 were damaged and thrown away. 12 of what?",
      UL("q", "12 damaged"),
      ask=CHOOSE(["12 mangoes", "12 crates", "12 days"], 1,
                 "The 12 that were damaged are whole crates, each one full of mangoes. So we take 12 away from the number of crates, before we count any mangoes.")),
    B("363 minus 12 is 351 good crates.",
      W("l2", "363 − 12 = 351")),
    B("Each holds 36 mangoes. Split 36 into 30 and 6. 351 times 30 is 10530.",
      W("l3", "351 × 30 = 10530")),
    B("And 351 times 6 is 2106.",
      W("l4", "351 × 6 = 2106")),
    B("10530 plus 2106 is 12636 mangoes, ready to sell.",
      ANS("l5", "10530 + 2106 = 12636"), CIRC("l5", "12636")),
    B("The slip to avoid is taking 12 off at the very end. 12 mangoes are not the same as 12 crates of mangoes."),
    B("Check another way. All 363 crates would hold 13068 mangoes. The 12 damaged crates held 432. And 13068 minus 432 is 12636.",
      W("l6", "363 × 36 = 13068"), W("l7", "12 × 36 = 432"), W("l8", "13068 − 432 = 12636")),
    B("So sort out the crates first: add what was packed, take off what was lost. Then multiply by the mangoes in one crate."),
)

# 45 + 28 packets of 36 chanas.
LESSONS[P + "80fb143f-d584-42f0-ab8c-e74cf4dcc85f"] = LESSON(
    B("Raju's uncle packs 36 chanas in each packet. He sold 45 packets in the morning and 28 in the evening. How many chanas is that?",
      GIVEN("q", "36 chanas a packet. Packets: 45 + 28")),
    B("Every packet holds 36. So what is the quickest plan?",
      ask=CHOOSE(["multiply 45 by 28", "add the packets, then × 36", "add 36, 45 and 28"], 1,
                 "Morning packets and evening packets are the same size. So count all the packets together, then multiply by 36 once.")),
    B("45 plus 28 is 73 packets.",
      W("l1", "45 + 28 = 73")),
    B("Careful: 73 is among the choices, but that counts packets. The question asks for chanas.",
      BOX("l1", "73")),
    B("73 times 36. Split 36 into 30 and 6. 73 times 30 is 2190, and 73 times 6 is 438.",
      W("l2", "73 × 30 = 2190"), W("l3", "73 × 6 = 438")),
    B("2190 plus 438 is 2628 chanas.",
      ANS("l4", "2190 + 438 = 2628"), CIRC("l4", "2628")),
    B("Check morning and evening separately. 45 times 36 is 1620. 28 times 36 is 1008. And 1620 plus 1008 is 2628.",
      W("l5", "45 × 36 = 1620"), W("l6", "28 × 36 = 1008"), W("l7", "1620 + 1008 = 2628")),
    B("So when the groups are all the same size, add the groups first and multiply once."),
)

# 18 teams, 3 need no jerseys, 15 players, 245 rupees.
LESSONS[P + "87e1960d-9843-44b7-8f2f-d591c1e6d180"] = LESSON(
    B("There are 18 teams of 15 players, and a jersey costs 245 rupees. But 3 teams already have jerseys. What is spent on new ones?",
      GIVEN("q", "18 teams, 15 players each, ₹245 a jersey. 3 teams skip")),
    B("3 teams already have jerseys. What do we do about them first?",
      ask=CHOOSE(["18 + 3 teams", "18 − 3 teams need jerseys", "leave the 3 teams in"], 1,
                 "Those 3 teams buy nothing. So take them out before counting any players: 18 minus 3.")),
    B("18 minus 3 is 15 teams.",
      UL("q", "3 teams skip"), W("l1", "18 − 3 = 15")),
    B("Each of those teams has 15 players. 15 times 10 is 150, 15 times 5 is 75, and together that is 225 jerseys.",
      W("l2", "15 × 10 = 150"), W("l3", "15 × 5 = 75"), W("l4", "150 + 75 = 225")),
    B("Each jersey costs 245 rupees. Split 245 into 200, 40 and 5, and let 225 multiply each part.",
      W("l5", "225 × (200 + 40 + 5)"), ARC("l5", "225", ["200", "40", ("5", 2)])),
    B("225 times 200 is 45,000. 225 times 40 is 9,000. 225 times 5 is 1,125.",
      W("l6", "225 × 200 = 45,000"), W("l7", "225 × 40 = 9,000"), W("l8", "225 × 5 = 1,125")),
    B("Add them. 45,000 plus 9,000 plus 1,125 is 55,125 rupees.",
      ANS("l9", "45,000 + 9,000 + 1,125 = 55,125"), CIRC("l9", "55,125")),
    B("Buying for all 18 teams would cost 66,150, and that is among the choices. The 3 teams have to come out first.",
      W("l10", "18 × 15 × 245 = 66,150")),
    B("And that gives a check. The 3 teams we left out would have cost 11,025. 66,150 minus 11,025 is 55,125.",
      W("l11", "3 × 15 × 245 = 11,025"), W("l12", "66,150 − 11,025 = 55,125")),
    B("So decide who is buying first. Then it is teams times players times the price of one jersey."),
)

# Gift boxes: 3 layers × 4 rows × 7 sweets, 15 boxes less 2, 12 rupees a sweet.
LESSONS[P + "964e6e9c-4d7e-497f-a253-3c737857326d"] = LESSON(
    B("Each gift box has 3 layers, each layer has 4 rows, and each row has 7 sweets. Grandmother made 15 boxes, gave 2 away, and sold every sweet in the rest for 12 rupees.",
      GIVEN("q", "Box: 3 layers × 4 rows × 7 sweets. 15 boxes − 2. ₹12 each")),
    B("Start small, with one layer. 4 rows of 7 is 28 sweets.",
      W("l1", "4 × 7 = 28")),
    B("A box has 3 layers. 3 times 28 is 84 sweets in one box.",
      W("l2", "3 × 28 = 84")),
    B("She made 15 boxes but gave 2 away. How many boxes does she sell?",
      ask=CHOOSE(["15", "17", "13"], 2,
                 "Boxes that were given away earn no money. 15 minus 2 leaves 13 boxes to sell.")),
    B("13 boxes of 84. 10 boxes hold 840, and 3 boxes hold 252. Together, 1092 sweets.",
      W("l3", "15 − 2 = 13"), W("l4", "10 × 84 = 840"), W("l5", "3 × 84 = 252"), W("l6", "840 + 252 = 1092")),
    B("Careful: 1092 is among the choices, but that counts sweets, not rupees. Each sweet sells for 12 rupees.",
      BOX("l6", "1092")),
    B("1092 times 10 is 10,920, and 1092 times 2 is 2,184. Together, 13,104 rupees.",
      W("l7", "1092 × 10 = 10,920"), W("l8", "1092 × 2 = 2,184"), ANS("l9", "10,920 + 2,184 = 13,104"), CIRC("l9", "13,104")),
    B("Selling all 15 boxes would bring 15,120, which is also among the choices. But the 2 gift boxes earn nothing.",
      W("l10", "15 × 84 × 12 = 15,120")),
    B("Use that as a check. The 2 gift boxes would have earned 2,016. And 15,120 minus 2,016 is 13,104.",
      W("l11", "2 × 84 × 12 = 2,016"), W("l12", "15,120 − 2,016 = 13,104")),
    B("So build it up in layers: one box, then the boxes sold, then the money."),
)

# 1,548 cups, sold at 12, cost 8. The 36 cups a pot is not needed.
LESSONS[P + "9be5361f-fa0a-4aeb-99d9-11c5cab81bf3"] = LESSON(
    B("Ankit's family sold 1,548 cups of chai at 12 rupees each. Each cup cost 8 rupees to make. We want the profit for the day.",
      GIVEN("q", "1,548 cups sold at ₹12. Each cup costs ₹8 to make")),
    B("The story also says each pot makes 36 cups. Do we need that to find the profit?",
      ask=CHOOSE(["Yes, pots matter", "No, we know the cups"], 1,
                 "We already know how many cups were sold: 1,548. The pots do not change the money, so the 36 is extra information.")),
    B("The profit on one cup is what it sells for, minus what it costs. 12 minus 8 is 4 rupees.",
      W("l1", "12 − 8 = 4")),
    B("So every cup brings 4 rupees of profit, and there are 1,548 cups.",
      W("l2", "1,548 × 4 = ?")),
    B("Split 1,548 into 1500 and 48. 1500 times 4 is 6000. 48 times 4 is 192.",
      W("l3", "1500 × 4 = 6000"), W("l4", "48 × 4 = 192")),
    B("6000 plus 192 is 6192. The profit is 6,192 rupees.",
      ANS("l5", "6000 + 192 = 6192"), CIRC("l5", "6192")),
    B("The trap is stopping at the sales. 1,548 times 12 is all the money taken in, but 8 rupees of every 12 went on milk, sugar and tea leaves."),
    B("Check the long way. Money in is 18,576. Money out is 12,384. And 18,576 minus 12,384 is 6,192.",
      W("l6", "1,548 × 12 = 18,576"), W("l7", "1,548 × 8 = 12,384"), W("l8", "18,576 − 12,384 = 6,192")),
    B("So find the profit on one cup, then multiply by the number of cups. And leave out numbers the question does not need."),
)
