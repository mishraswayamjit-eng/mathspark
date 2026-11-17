"""Festival and shop stories from batch 12: multiply, divide, and what to do with a remainder."""
from imported_12_lib import A, AL, B, CH, CIRC, E, G, LB, LESSON, MINUS, NOTE, STRIKE, UL, W, split_times  # noqa: F401

P = "AIGEN_grade5_"

LESSONS = {}

# Rangoli powder: 48 × 125 g, 36 × 250 g, 64 × 75 g, at ₹8 per 100 g.
LESSONS[P + "a19e4e39-db0e-4e12-ace4-daff9aecd896"] = LESSON(
    B("Anita's grandmother sells rangoli powder at 8 rupees for every 100 grams. The shopkeeper orders 48 red bags, 36 yellow bags and 64 green bags, and each colour has its own bag size.",
      G("q", "Red 48 × 125 g, yellow 36 × 250 g, green 64 × 75 g"), LB("q2", "Price: ₹8 for every 100 g", "given")),
    B("The price is for grams, not for bags. So what must we find before we can work out the cost?",
      ask=CH(["the total number of bags", "the total weight in grams", "8 times each bag size"], 1,
             "Look at the price again: 8 rupees for every 100 grams. It is all about weight, so first we need the total grams of powder.")),
    B("Red first: 48 bags of 125 grams. 40 bags weigh 5000 grams and 8 bags weigh 1000 grams, so red is 6000 grams.",
      E("r1", "40 × 125"), E("r2", "8 × 125"), E("r", "48 × 125")),
    B("Yellow: 36 bags of 250 grams. 4 of those bags make 1000 grams, and 36 bags is 9 lots of 4. So yellow is 9000 grams.",
      E("y1", "4 × 250"), E("y", "36 × 250")),
    B("Green: 64 bags of 75 grams. 60 bags weigh 4500 grams and 4 bags weigh 300 grams, so green is 4800 grams.",
      E("g1", "60 × 75"), E("g2", "4 × 75"), E("g", "64 × 75")),
    B("Now add the three colours. 6000 plus 9000 is 15,000, and 4800 more makes 19,800 grams of powder.",
      E("t1", "6000 + 9000"), E("t", "15,000 + 4800")),
    B("Now the money. 8 rupees pays for a whole 100 grams. What do we do with 19,800?",
      ask=CH(["19,800 × 8", "19,800 ÷ 100, then × 8", "19,800 ÷ 8"], 1,
             "The 8 rupees pays for 100 grams, not for 1 gram. So first count how many hundreds of grams there are, then multiply by 8.")),
    B("19,800 divided by 100 is 198. So there are 198 lots of 100 grams.",
      E("h", "19,800 ÷ 100"), UL("h", "198")),
    B("Each lot costs 8 rupees. 200 times 8 is 1600, and we have 2 lots fewer, so take off 16. That leaves 1584 rupees.",
      E("c1", "200 × 8"), E("c2", "2 × 8"), A("c", "1600 − 16")),
    B("Check it the long way. 198 times 8 really is 1584. And notice that adding up the bags would not have helped, because the bags are different sizes.",
      E("k", "198 × 8")),
    B("So when a price is for a weight: find the total weight, count how many lots of that weight you have, then multiply by the price."),
)

# 48 laddoos a box; 25 boxes and 17 boxes.
LESSONS[P + "aa51d21b-91e9-4811-ba54-2c93ae112588"] = LESSON(
    B("Riya's grandmother packs 48 laddoos in every box. She made 25 boxes for relatives and 17 boxes for neighbours. We want all the laddoos.",
      G("q", "48 laddoos in a box; 25 boxes and 17 boxes")),
    B("Every box holds the same 48. So what is a quick first step?",
      ask=CH(["25 + 17, the boxes in all", "48 + 25 + 17", "48 × 25, and stop there"], 0,
             "All the boxes are the same size, so we can count the boxes first. Adding 48 to the boxes would mix laddoos up with boxes.")),
    B("25 plus 17 is 42. So there are 42 boxes in all.",
      E("b", "25 + 17"), UL("b", "42")),
    split_times(42, 48, 50, MINUS, 2, "m",
                "Now 42 boxes of 48. 48 is a fiddly number, but it is just 2 less than 50. So we find 42 times 50, then take off 42 times 2.",
                mid="42 times 50 is 2100. And 42 times 2 is 84.",
                end="2100 minus 84 is 2016. She made 2016 laddoos.", final=True),
    B("Careful with that last step. 50 is more than 48, so 2100 is too many laddoos. That is why the 84 comes off, and is not added on."),
    B("Check by doing the two groups one at a time. 25 boxes hold 1200, 17 boxes hold 816, and 1200 plus 816 is 2016 again.",
      E("k1", "25 × 48"), E("k2", "17 × 48"), E("k3", "1200 + 816")),
    B("So when every group is the same size, add up the groups first. Then you only have to multiply once."),
)

# 8 trays of 45 a day, for 5 days.
LESSONS[P + "c30d9280-1d51-48ea-b19c-0a6a186af282"] = LESSON(
    B("Ananya's mother fills 8 trays of laddoos every day, with 45 laddoos on each tray. She does this for 5 days. How many laddoos is that?",
      G("q", "8 trays a day, 45 laddoos on a tray, for 5 days")),
    B("Let's start with just one day. Which sum gives the laddoos made in one day?",
      ask=CH(["8 × 45", "8 + 45", "45 × 5"], 0,
             "One day means 8 trays, and each tray holds 45. 8 lots of 45 is 8 times 45.")),
    B("8 times 40 is 320, and 8 times 5 is 40. Together that is 360 laddoos in one day.",
      E("a1", "8 × 40"), E("a2", "8 × 5"), E("a", "8 × 45")),
    B("360 is one of the answer choices. Have we finished?",
      ask=CH(["Yes, the answer is 360", "No, 360 is only one day"], 1,
             "Read the end of the question again. She makes laddoos for 5 days, and 360 is just one day's work.")),
    B("5 days means 5 lots of 360. 360 times 10 is 3600, and 5 is half of 10, so we halve it: 1800 laddoos.",
      E("b1", "360 × 10"), A("b", "360 × 5")),
    B("Check by changing the order. 5 days of 8 trays is 40 trays, and 40 trays of 45 is 1800 as well.",
      E("k1", "5 × 8"), E("k2", "40 × 45")),
    B("So in a story with trays and days, find one day first, then multiply by the number of days."),
)

# 48 crates of 35 mangoes.
LESSONS[P + "cbf1e9cf-0305-4f05-be8f-f03f20d78ae1"] = LESSON(
    B("Ravi's father fills 48 crates, and every crate holds 35 mangoes. We want to know how many mangoes he packed.",
      G("q", "48 crates, 35 mangoes in each crate")),
    B("Which sum gives the total?",
      ask=CH(["35 + 48", "35 × 48", "48 ÷ 35"], 1,
             "Every crate holds the same 35 mangoes, and there are 48 crates. 48 equal lots means we multiply.")),
    split_times(35, 48, 50, MINUS, 2, "m",
                "35 times 48 looks hard. But 48 is only 2 less than 50, and 50 is friendly. So we find 35 times 50, then take away 35 times 2.",
                mid="35 times 50 is 1750. And 35 times 2 is 70.",
                end="1750 minus 70 is 1680. He packed 1680 mangoes.", final=True),
    B("Here is the slip to watch for. We counted 50 crates, which is 2 crates too many. So the 70 mangoes come off. They are not added on."),
    B("Check by splitting 48 another way, into 40 and 8. 35 times 40 is 1400, 35 times 8 is 280, and together they make 1680 again.",
      E("k1", "35 × 40"), E("k2", "35 × 8"), E("k3", "1400 + 280")),
    B("So to multiply by a number just under a round one, multiply by the round number, then take off the extra."),
)

# 48 students × ₹375, ₹1,800 left over.
LESSONS[P + "ccccf078-4592-4e4f-ae0b-199b6f027160"] = LESSON(
    B("48 students each collect 375 rupees to buy cricket kits. After buying the kits, 1800 rupees are left over. We want to know what the kits cost.",
      G("q", "48 students × ₹375 collected; ₹1,800 left after the kits")),
    split_times(48, 375, 400, MINUS, 25, "m",
                "First, the money collected: 48 times 375. 375 is 25 less than 400, so we find 48 times 400 and take off 48 times 25.",
                mid="48 times 400 is 19,200. And 48 times 25 is 1200.",
                end="19,200 minus 1200 is 18,000. So the class collected 18,000 rupees."),
    B("They collected 18,000 rupees, and 1800 was left over. How do we find what the kits cost?",
      ask=CH(["18,000 + 1800", "18,000 − 1800", "1800 ÷ 48"], 1,
             "The money collected is the money spent plus the money left. So to find the spending, take the leftover away from the collection.")),
    B("18,000 minus 1800 is 16,200. The kits cost 16,200 rupees.",
      A("s", "18,000 − 1800")),
    B("Two things to watch. 18,000 is among the choices, but that is the money collected. And the snacks at the end of the story are extra: nobody asked about them."),
    B("Check by adding back. 16,200 for the kits plus 1800 left over is 18,000, the money they collected.",
      E("k", "16,200 + 1800")),
    B("So read to the very end to see what is asked. Here it was collected money, take away leftover money."),
)

# 1250 people, boxes of 48 sweets: 27 boxes.
LESSONS[P + "cd50e3f1-1312-4ab7-ade9-be49fab6564e"] = LESSON(
    B("Meera's family needs one sweet for each of 1250 people. The sweets come in boxes of 48. What is the smallest number of boxes that will do?",
      G("q", "1250 people, 1 sweet each; boxes of 48 sweets")),
    B("How do we find the number of boxes?",
      ask=CH(["1250 ÷ 48", "1250 × 48", "1250 − 48"], 0,
             "We are asking how many groups of 48 are needed to cover 1250. Making equal groups is dividing.")),
    B("48 is close to 50, and 25 fifties make exactly 1250. So let's try 25 boxes. 25 times 48 is 1200. Not enough yet.",
      E("a1", "25 × 50"), E("a2", "25 × 48")),
    B("One more box, the 26th, adds 48 and brings us to 1248. That is still 2 sweets short of 1250.",
      E("b1", "1200 + 48"), E("b2", "1250 − 1248"), LB("b3", "1250 ÷ 48 = 26, remainder 2")),
    B("With 26 boxes, 2 people are left without a sweet. So how many boxes must the family buy?",
      ask=CH(["26", "27", "25"], 1,
             "With 26 boxes, 2 people get nothing. The shop will not sell part of a box, so the family needs one whole extra box.")),
    B("26 boxes and 1 more is 27 boxes.",
      A("c", "26 + 1")),
    B("Check: 27 boxes hold 1296 sweets. That is more than 1250, so everyone gets one, with a few to spare.",
      E("k", "27 × 48")),
    B("So when everybody must get one, divide. If anything is left over, go up to the next whole box."),
)

# 48 packets × 125 sparklers, bags of 25.
LESSONS[P + "d2b897eb-ed30-46b2-a325-fe24034efaa6"] = LESSON(
    B("Priya buys 48 packets of sparklers with 125 in each packet. She puts all of them into gift bags of 25. How many bags can she fill?",
      G("q", "48 packets × 125 sparklers; gift bags of 25")),
    B("First, all the sparklers. Here is a fact worth keeping: 8 times 125 is 1000. And 48 is 6 lots of 8, so 48 times 125 is 6 thousands, 6000.",
      E("a1", "8 × 125"), E("a2", "6 × 8"), E("a", "48 × 125")),
    B("6000 sparklers go into bags of 25. Which sum gives the number of bags?",
      ask=CH(["6000 × 25", "6000 − 25", "6000 ÷ 25"], 2,
             "We are making equal groups of 25 out of 6000. Making equal groups is dividing.")),
    B("4 lots of 25 make 100, so every 100 sparklers fill 4 bags. 6000 is 60 hundreds, and 60 times 4 is 240 bags.",
      E("b1", "100 ÷ 25"), E("b2", "60 × 4"), A("b", "6000 ÷ 25")),
    B("Careful: 6000 is among the choices too. But 6000 is the number of sparklers, and the question asks for bags."),
    B("Check a second way. One packet of 125 fills 5 bags. So 48 packets fill 48 times 5, which is 240 bags.",
      E("k1", "125 ÷ 25"), E("k2", "48 × 5")),
    B("So in a pack and repack story, find the total first, then divide by the size of the new group."),
)
