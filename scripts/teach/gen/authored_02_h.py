"""authored-02, eighth group: measurement 007 to 011."""
from authored_02_lib import ANSC, ANSLC, B, CHOOSE, GIVEN, LB, LESSON, UL, W

LESSONS = {}

# A watch that gains 5 minutes every real hour.
LESSONS["G5A_MEASUREMENT_007"] = LESSON(
    B("Meena's watch gains 5 minutes in every real hour. She sets it right at 6:00 a.m. Later the same day it shows 7:00 p.m. What is the real time then?",
      GIVEN("q", "Gains 5 min each real hour. Set 6:00 a.m. Shows 7:00 p.m.")),
    B("The watch runs fast. So is the real time earlier or later than 7:00 p.m.?",
      ask=CHOOSE(["earlier than 7:00 p.m.", "later than 7:00 p.m."], 0,
                 "A fast watch races ahead of the real time. So the real time is still behind what the watch shows: it is earlier.")),
    B("Earlier. Now, how far has the watch moved? From 6:00 a.m. to 6:00 p.m. is 12 hours, and 1 more hour reaches 7:00 p.m. That is 13 hours on the watch.",
      W("l1", "12 + 1 = 13")),
    B("In minutes, 13 times 60 is 780 minutes on the watch.",
      W("l2", "13 × 60 = 780")),
    B("Here is the key. During 1 real hour, how many minutes does the watch move?",
      ask=CHOOSE(["60 minutes", "65 minutes", "55 minutes"], 1,
                 "A real hour is 60 minutes, and the watch gains 5 on top of that. So it moves 60 plus 5.")),
    B("The watch moves 65 minutes for every real hour. How many lots of 65 are in 780? 65 times 10 is 650, and 65 times 2 is 130. Together, 780. So 12 lots.",
      W("l3", "60 + 5 = 65"), W("l4", "65 × 10 = 650"), W("l5", "65 × 2 = 130"), W("l6", "780 ÷ 65 = 12")),
    B("So 12 real hours have passed. 12 hours after 6:00 a.m. is 6:00 p.m.",
      *ANSLC("l7", "6:00 a.m. + 12 hours = 6:00 p.m.", "6:00 p.m.")),
    B("Check: in 12 real hours the watch gains 12 times 5, which is 60 minutes. So it shows 1 hour too much: 7:00 p.m. It fits.",
      W("l8", "12 × 5 = 60")),
    B("The trap is 13 times 5, which is 65 minutes, taken off 7:00 p.m. But the 13 hours are watch hours, not real hours.",
      W("l9", "13 × 5 = 65")),
    B("So find how far the watch moved, and divide by what it moves in one real hour. The real time is 6:00 p.m."),
)

# Buses every 25 minutes from 6:40 a.m.
LESSONS["G5A_MEASUREMENT_008"] = LESSON(
    B("Buses leave a depot every 25 minutes. The first bus leaves at 6:40 a.m. How many buses leave before 1:00 p.m.?",
      GIVEN("q", "Every 25 min. First bus 6:40 a.m. Before 1:00 p.m.?")),
    B("First, how long is it from 6:40 a.m. to 1:00 p.m.? Go through noon carefully. From 6:40 a.m. to 12:40 p.m. is 6 hours. Then 20 minutes more reaches 1:00 p.m.",
      LB("l1", "6:40 a.m. to 12:40 p.m. = 6 hours"), W("l2", "40 + 20 = 60")),
    B("6 hours 20 minutes. In minutes, 6 times 60 is 360, and 360 plus 20 is 380 minutes.",
      W("l3", "6 × 60 = 360"), W("l4", "360 + 20 = 380")),
    B("How many whole gaps of 25 minutes fit into 380? 4 gaps make 100 minutes, so 300 minutes hold 12 gaps. The 80 left over hold 3 more, with 5 minutes to spare.",
      W("l5", "25 × 4 = 100"), W("l6", "25 × 12 = 300"), W("l7", "380 − 300 = 80"), W("l8", "25 × 3 = 75")),
    B("12 plus 3 is 15 gaps. 15 times 25 is 375 minutes, so the last bus leaves 5 minutes before 1:00 p.m., at 12:55.",
      W("l9", "12 + 3 = 15"), W("l10", "15 × 25 = 375"), LB("l11", "last bus: 12:55 p.m.")),
    B("15 gaps between buses. So how many buses is that?",
      ask=CHOOSE(["15 buses", "16 buses", "14 buses"], 1,
                 "A gap needs a bus at each end. The very first bus, at 6:40 a.m., leaves before any gap has passed, so it has to be counted too.")),
    B("The first bus leaves at the start of the first gap. So the buses are one more than the gaps: 15 plus 1 is 16.",
      *ANSC("l12", "15 + 1 = 16", 16)),
    B("Test it small: buses at 6:40, 7:05 and 7:30 are 3 buses, but only 2 gaps.",
      LB("l13", "6:40, 7:05, 7:30")),
    B("So find the time, count the whole gaps, and add 1 for the first bus. 16 buses leave before 1:00 p.m."),
)

# Two models of the same tower.
LESSONS["G5A_MEASUREMENT_009"] = LESSON(
    B("In a model of a tower, 1 centimetre stands for 6 metres of the real tower, and the model is 15 centimetres tall. A second model uses 1 centimetre for 4 metres. How tall is the second model?",
      GIVEN("q", "Model 1: 1 cm = 6 m, 15 cm tall. Model 2: 1 cm = 4 m")),
    B("Both models show the same real tower. Its height is the bridge between them. How do we find the real height from the first model?",
      ask=CHOOSE(["15 × 6", "15 × 4", "15 ÷ 6"], 0,
                 "Each centimetre of the first model stands for 6 metres. The model is 15 centimetres tall, so the tower is 15 lots of 6 metres.")),
    B("15 times 6 is 90. The real tower is 90 metres tall.",
      W("l1", "15 × 6 = 90")),
    B("In the second model each centimetre stands for only 4 metres. Will this model be taller or shorter than the first?",
      ask=CHOOSE(["taller", "shorter"], 0,
                 "Each centimetre now covers fewer metres. So we need more centimetres to cover the same 90 metres. The model is taller.")),
    B("Taller. We need to know how many fours are in 90. 4 times 22 is 88, and 2 metres are left over.",
      W("l2", "4 × 22 = 88"), W("l3", "90 − 88 = 2")),
    B("2 metres is half of 4 metres, so it needs half a centimetre more. That makes 22 and a half centimetres.",
      W("l4", "90 ÷ 4 = 22.5")),
    B("Half a centimetre is 5 millimetres. So the second model is 22 centimetres 5 millimetres tall.",
      *ANSLC("l5", "22 cm 5 mm", "22 cm 5 mm")),
    B("The trap is 10 centimetres, from 15 times 4 divided by 6. That makes the model shorter, when fewer metres to each centimetre must make it taller.",
      W("l6", "15 × 4 ÷ 6 = 10")),
    B("So go through the real thing: model to real tower, then real tower to the new model. The answer is 22 centimetres 5 millimetres."),
)

# Pieces of 35 cm from 6 planks of 2 m.
LESSONS["G5A_MEASUREMENT_010"] = LESSON(
    B("A carpenter has 6 planks, each 2 metres long. He needs pieces exactly 35 centimetres long, and each piece must be cut from a single plank. What is the greatest number of pieces he can cut?",
      GIVEN("q", "6 planks of 2 m. Pieces of 35 cm, each from one plank")),
    B("The key words are from a single plank. So think about one plank on its own first. 2 metres is 200 centimetres.",
      W("l1", "2 × 100 = 200"), UL("q", "each from one plank")),
    B("How many whole pieces of 35 fit into 200? 35 times 5 is 175, and 35 times 6 is 210.",
      W("l2", "35 × 5 = 175"), W("l3", "35 × 6 = 210"),
      ask=CHOOSE(["5 pieces", "6 pieces"], 0,
                 "6 pieces would need 210 centimetres, and the plank is only 200. So 5 is the most that fit.")),
    B("5 pieces fit, using 175 centimetres. That leaves 200 minus 175, which is 25 centimetres at the end of the plank.",
      W("l4", "200 − 175 = 25")),
    B("25 is too short for another piece of 35. And it cannot be joined to a leftover from another plank. So that bit is wasted."),
    B("Every plank gives 5 pieces. 6 planks give 6 times 5, which is 30 pieces.",
      *ANSC("l5", "6 × 5 = 30", 30)),
    B("The trap is to add all the wood together: 6 planks make 1200 centimetres, and 35 goes into 1200 as many as 34 times. But 4 of those pieces would be made from joined scraps.",
      W("l6", "6 × 200 = 1200"), W("l7", "35 × 34 = 1190")),
    B("So when each piece must come from one plank, work out one plank first, then multiply. The greatest number is 30 pieces."),
)

# Cards 80 mm by 50 mm from a sheet 32 cm by 22 cm.
LESSONS["G5A_MEASUREMENT_011"] = LESSON(
    B("A sheet of card is 32 centimetres long and 22 centimetres wide. Asha cuts cards 80 millimetres by 50 millimetres from it, all placed the same way round. What is the greatest number she can cut?",
      GIVEN("q", "Sheet 32 cm by 22 cm. Cards 80 mm by 50 mm")),
    B("Match the units first. 80 millimetres is 8 centimetres, and 50 millimetres is 5 centimetres. So each card is 8 by 5.",
      W("l1", "80 ÷ 10 = 8"), W("l2", "50 ÷ 10 = 5")),
    B("Whole cards must fit along the length and along the width, so think in rows. Put the 8 side along the 32 edge. How many cards fit along it?",
      ask=CHOOSE(["4 cards", "6 cards", "5 cards"], 0,
                 "Each card takes up 8 centimetres of the 32. 8 times 4 is exactly 32, so 4 cards fit.")),
    B("4 cards along the length. Up the 22 width, each row is 5 tall. 5 times 4 is 20, so 4 rows fit, and 2 centimetres are left over.",
      W("l3", "32 ÷ 8 = 4"), W("l4", "5 × 4 = 20"), W("l5", "22 − 20 = 2")),
    B("4 rows of 4 cards. 4 times 4 is 16 cards.",
      W("l6", "4 × 4 = 16")),
    B("But the card could be turned. Put the 5 side along the 32 edge: 5 times 6 is 30, so 6 fit. Each row is now 8 tall, and 8 times 3 is 24, too tall for 22. Only 2 rows fit.",
      W("l7", "5 × 6 = 30"), W("l8", "8 × 3 = 24")),
    B("Turned, that is 2 rows of 6, which is 12 cards. Which way is better?",
      W("l9", "6 × 2 = 12"),
      ask=CHOOSE(["the first way: 16", "turned: 12", "they are the same"], 0,
                 "16 is more than 12. The question asks for the greatest number, so we keep the first way.")),
    B("The first way wins. The greatest number of cards is 16.",
      *ANSLC("l10", "4 rows of 4 = 16 cards", "16")),
    B("The trap is dividing the areas: 704 divided by 40 says 17 and a bit. But the strip left over is only 2 centimetres wide, and no card fits in it.",
      W("l11", "32 × 22 = 704"), W("l12", "8 × 5 = 40"), W("l13", "17 × 40 = 680")),
    B("So for cutting cards from a sheet, count rows and columns of whole cards, try both ways round, and take the bigger. Here it is 16."),
)
