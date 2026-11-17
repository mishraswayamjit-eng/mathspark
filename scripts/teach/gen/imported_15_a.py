"""Batch 15, the plain profit stories: total cost, (how many sold), sales, profit.

Keyed by the first 8 characters of the question's uuid; imported_15.py resolves them.
"""
from imported_15_lib import stall

LESSONS = {}


def S(key, who, pro, intro, given, costs, sales, lost=None, trap=None):
    LESSONS[key] = stall(key, who, intro, given, costs, sales, pro=pro, poss={"she": "her", "he": "his"}[pro],
                         lost=lost, trap=trap)


# ── Easy: everything is sold ──

S("2b38226b", "Vikram", "he",
  "Vikram buys 40 kites at 12 rupees each. He also spends 80 rupees on strings and 40 rupees on stickers. Then he sells all 40 kites at 20 rupees each. What is his profit?",
  "40 kites at ₹12, strings ₹80, stickers ₹40; sold at ₹20",
  [("the kites", 40, 12), ("the strings", 80), ("the stickers", 40)],
  [(40, 20, "{n} kites at {p} rupees each")],
  trap="The slip to watch for is counting only the kites as the cost. The strings and the stickers were paid for too.")

S("2d5f2d51", "Kiran", "she",
  "Kiran buys thread for 120 rupees and beads for 80 rupees. She makes 10 bracelets and sells each one for 30 rupees. What is her profit?",
  "Thread ₹120, beads ₹80; 10 bracelets at ₹30 each",
  [("the thread", 120), ("the beads", 80)],
  [(10, 30, "{n} bracelets at {p} rupees each")])

S("3f66346a", "Neha's aunt", "she",
  "Neha's aunt buys glitter sheets for 150 rupees and coloured paper for 90 rupees. She makes 60 rangoli stickers and sells each one for 7 rupees. What is her profit?",
  "Glitter ₹150, paper ₹90; 60 stickers at ₹7 each",
  [("the glitter sheets", 150), ("the coloured paper", 90)],
  [(60, 7, "{n} stickers at {p} rupees each")])

S("40c8583a", "Ravi's mother", "she",
  "Ravi's mother buys 5 kilograms of coconut at 60 rupees a kilogram and 2 kilograms of sugar at 45 rupees a kilogram, and spends 50 rupees on ghee and cardamom. She sells 120 pieces of barfi at 5 rupees each.",
  "Coconut 5 × ₹60, sugar 2 × ₹45, ghee ₹50; 120 barfi at ₹5",
  [("the coconut", 5, 60), ("the sugar", 2, 45), ("the ghee and cardamom", 50)],
  [(120, 5, "{n} pieces of barfi at {p} rupees each")],
  trap="There are three costs in this story, and it is easy to drop one. The ghee and cardamom count just as much as the coconut and the sugar.")

S("59ad8df2", "Pooja", "she",
  "Pooja buys 25 rakhis at 20 rupees each, and spends 150 rupees on ribbons and boxes. She sells every rakhi for 35 rupees. What is her profit?",
  "25 rakhis at ₹20, wrapping ₹150; sold at ₹35 each",
  [("the rakhis", 25, 20), ("the ribbons and boxes", 150)],
  [(25, 35, "{n} rakhis at {p} rupees each")],
  trap="The slip to watch for is forgetting the wrapping. The ribbons and boxes were paid for too, so they belong in the cost.")

S("65546185", "Arjun's grandmother", "she",
  "Arjun's grandmother buys clay for 200 rupees and paints for 100 rupees. She makes 60 diyas and sells each one for 8 rupees. What is her profit?",
  "Clay ₹200, paints ₹100; 60 diyas at ₹8 each",
  [("the clay", 200), ("the paints", 100)],
  [(60, 8, "{n} diyas at {p} rupees each")])

S("80e0ca8b", "Kiran", "she",
  "Kiran buys threads for 200 rupees and beads for 100 rupees. She makes 15 bracelets and sells each one for 30 rupees. What is her profit?",
  "Threads ₹200, beads ₹100; 15 bracelets at ₹30 each",
  [("the threads", 200), ("the beads", 100)],
  [(15, 30, "{n} bracelets at {p} rupees each")])

S("8308df8c", "Priya's uncle", "he",
  "Priya's uncle buys 80 diyas at 4 rupees each, and spends 80 rupees on paint and glitter. He sells all 80 diyas at 7 rupees each. What is his profit?",
  "80 diyas at ₹4, paint ₹80; sold at ₹7 each",
  [("the diyas", 80, 4), ("the paint and glitter", 80)],
  [(80, 7, "{n} diyas at {p} rupees each")],
  trap="The slip to watch for is leaving out the paint and glitter. Nobody buys the paint from him, but he still paid for it.")

S("9b569049", "Arjun's dad", "he",
  "Arjun's dad buys 50 kilograms of mangoes at 40 rupees a kilogram, and pays 200 rupees for transport. He sells all the mangoes at 52 rupees a kilogram. What is his profit?",
  "50 kg at ₹40, transport ₹200; sold at ₹52 per kg",
  [("the mangoes", 50, 40), ("the transport", 200)],
  [(50, 52, "{n} kilograms at {p} rupees a kilogram")],
  trap="The slip to watch for is forgetting the transport. Bringing the mangoes to the stall cost money, so it joins the cost.")

S("9c4f9610", "Sanjay's uncle", "he",
  "Sanjay's uncle buys 5 kilograms of corn at 40 rupees a kilogram, and spends 50 rupees on butter, salt and paper bags. He sells 50 packets of popcorn at 9 rupees each. What is his profit?",
  "Corn 5 × ₹40, extras ₹50; 50 packets at ₹9 each",
  [("the corn", 5, 40), ("the butter, salt and bags", 50)],
  [(50, 9, "{n} packets at {p} rupees each")])

S("aef2b172", "Priya's dad", "he",
  "Every morning Priya's dad spends 180 rupees on tea leaves, 90 rupees on milk, and 30 rupees on sugar and cups. He sells 60 cups of chai at 8 rupees each. What is his profit?",
  "Tea ₹180, milk ₹90, sugar and cups ₹30; 60 cups at ₹8",
  [("the tea leaves", 180), ("the milk", 90), ("the sugar and cups", 30)],
  [(60, 8, "{n} cups at {p} rupees each")])

S("b9edb79f", "Deepa's mother", "she",
  "Deepa's mother spends 250 rupees on flour, 150 rupees on sugar and saffron, and 100 rupees on oil. She makes 100 jalebis and sells each one for 8 rupees. What is her profit?",
  "Flour ₹250, sugar ₹150, oil ₹100; 100 jalebis at ₹8",
  [("the flour", 250), ("the sugar and saffron", 150), ("the oil", 100)],
  [(100, 8, "{n} jalebis at {p} rupees each")])

S("b9f657f8", "Suresh's father", "he",
  "Suresh's father buys 60 notebooks at 12 rupees each, and pays 120 rupees for an auto-rickshaw to carry them. He sells each notebook for 16 rupees. What is his profit?",
  "60 notebooks at ₹12, auto ₹120; sold at ₹16 each",
  [("the notebooks", 60, 12), ("the auto-rickshaw", 120)],
  [(60, 16, "{n} notebooks at {p} rupees each")],
  trap="The slip to watch for is forgetting the auto-rickshaw. Carrying the notebooks home cost money, so it joins the cost.")

S("bb4d5081", "Ananya", "she",
  "Ananya buys 25 ribbons at 6 rupees each and turns them into 25 friendship bands. She sells every band for 10 rupees. What is her profit?",
  "25 ribbons at ₹6 each; 25 bands sold at ₹10 each",
  [("the ribbons", 25, 6)],
  [(25, 10, "{n} bands at {p} rupees each")])

S("c203fa46", "Vikram's aunt", "she",
  "Vikram's aunt buys 40 packets of gulal at 15 rupees each, and spends 100 rupees on banners for her stall. She sells every packet for 22 rupees. What is her profit?",
  "40 packets at ₹15, banners ₹100; sold at ₹22 each",
  [("the packets of gulal", 40, 15), ("the banners", 100)],
  [(40, 22, "{n} packets at {p} rupees each")],
  trap="The slip to watch for is leaving out the banners. Nobody buys a banner, but it still cost her 100 rupees.")

S("c6403df8", "Kiran", "she",
  "Kiran buys 12 mangoes at 15 rupees each, and spends 60 rupees on yogurt, sugar and cups. She makes 20 glasses of lassi and sells each glass for 18 rupees. What is her profit?",
  "12 mangoes at ₹15, extras ₹60; 20 glasses at ₹18",
  [("the mangoes", 12, 15), ("the yogurt, sugar and cups", 60)],
  [(20, 18, "{n} glasses at {p} rupees each")],
  trap="Watch the two counts in this story. The 12 is mangoes bought, the 20 is glasses sold. Each goes with its own price.")

# ── Two selling prices, everything accounted for ──

S("25704843", "Priya's father", "he",
  "Priya's father buys 80 boxes of sweets at 125 rupees each, and spends 400 rupees on wrapping, 200 on ribbons and 400 on transport. He sells 60 boxes at 200 rupees and 15 boxes at 150 rupees. The last 5 expire.",
  "80 boxes at ₹125; extras ₹400, ₹200, ₹400; sold 60 and 15",
  [("the boxes", 80, 125), ("the wrapping paper", 400), ("the ribbons", 200), ("the transport", 400)],
  [(60, 200, "{n} boxes at the full price of {p} rupees"), (15, 150, "{n} boxes at the lower price of {p} rupees")],
  trap="Notice the 5 boxes that expired. They earn nothing, yet he paid for all 80. So the cost uses 80 boxes, and the sales use only 60 and 15.")

S("49851824", "Priya's father", "he",
  "Priya's father buys 10 kilograms of rice at 40 rupees a kilogram and 5 kilograms of urad dal at 90 rupees a kilogram. He spends 200 rupees on chutney, oil and gas, and 250 on stall rent. He sells 100 dosas at 15 rupees and 50 at 10 rupees.",
  "Rice 10 × ₹40, dal 5 × ₹90, extras ₹200, rent ₹250",
  [("the rice", 10, 40), ("the urad dal", 5, 90), ("the chutney, oil and gas", 200), ("the stall rent", 250)],
  [(100, 15, "the first {n} dosas at {p} rupees each"), (50, 10, "the last {n} dosas at {p} rupees each")],
  trap="The cost that is easy to miss is the stall rent. It comes at the very end of the story, but it is money spent like all the rest.")

S("a57920d9", "Meera's uncle", "he",
  "Meera's uncle buys 80 diyas at 5 rupees each. He spends 120 rupees on paint and glitter, and 80 rupees on packaging. He sells 60 diyas at 12 rupees each and gives the other 20 away as gifts.",
  "80 diyas at ₹5, paint ₹120, packaging ₹80; 60 sold at ₹12",
  [("the diyas", 80, 5), ("the paint and glitter", 120), ("the packaging", 80)],
  [(60, 12, "{n} diyas at {p} rupees each")],
  trap="Notice the 20 diyas he gave away. They earn nothing, yet he paid for all 80. So the cost uses 80 diyas, and the sales use only 60.")

S("a62bebf7", "Meera's father", "he",
  "Meera's father buys 80 boxes of sweets at 125 rupees each. He spends 400 rupees on ribbons and 200 rupees on gift bags. He sells 60 boxes at 200 rupees each, and the other 20 at 150 rupees each.",
  "80 boxes at ₹125, ribbons ₹400, bags ₹200; 60 and 20 sold",
  [("the boxes", 80, 125), ("the ribbons", 400), ("the gift bags", 200)],
  [(60, 200, "{n} boxes at the full price of {p} rupees"), (20, 150, "{n} boxes at the lower price of {p} rupees")])

# ── Some are not sold ──

S("24671057", "Priya", "she",
  "Priya spends 60 rupees on potatoes, 45 on flour, 35 on spices and 80 on oil, and makes 40 samosas. She gives 5 away and sells the rest at 12 rupees each. What is her profit?",
  "Costs ₹60, ₹45, ₹35, ₹80; 40 samosas, 5 given away, ₹12 each",
  [("the potatoes", 60), ("the flour", 45), ("the spices", 35), ("the oil", 80)],
  [("sold", 12, "{n} samosas at {p} rupees each")],
  lost=("Priya made 40 samosas.", 40, 5, "samosas", "were given away", "5 given away"))

S("45c5c0c1", "Farhan's sister", "she",
  "Farhan's sister spends 240 rupees on fruits, 80 on sugar and milk, and 40 on sticks and wrapping. She makes 60 popsicles, gives 12 away for free, and sells the rest at 12 rupees each.",
  "Costs ₹240, ₹80, ₹40; 60 popsicles, 12 free, ₹12 each",
  [("the fruits", 240), ("the sugar and milk", 80), ("the sticks and wrapping", 40)],
  [("sold", 12, "{n} popsicles at {p} rupees each")],
  lost=("She made 60 popsicles.", 60, 12, "popsicles", "were given away free", "12 free"))

S("4dcb7702", "Priya's dad", "he",
  "Priya's dad buys 4 kilograms of semolina at 50 rupees a kilogram, spices and chutneys for 180 rupees, and 200 cups at 1.50 rupees each. He makes 200 plates of pani puri at 20 rupees a plate, but 15 plates stay unsold.",
  "Semolina 4 × ₹50, spices ₹180, 200 cups at ₹1.50; 15 unsold",
  [("the semolina", 4, 50), ("the cups", 200, "1.50"), ("the spices and chutneys", 180)],
  [("sold", 20, "{n} plates at {p} rupees each")],
  lost=("He made 200 plates of pani puri.", 200, 15, "plates", "stayed unsold", "15 unsold"))

S("5187ca5f", "Ritu's mother", "she",
  "Ritu's mother buys clay for 200 rupees and spends 150 rupees on paints, glitter and brushes. She makes 50 diyas to sell at 12 rupees each, but 5 break on the way to the market.",
  "Clay ₹200, paints ₹150; 50 diyas at ₹12 each, 5 break",
  [("the clay", 200), ("the paints, glitter and brushes", 150)],
  [("sold", 12, "{n} diyas at {p} rupees each")],
  lost=("She made 50 diyas.", 50, 5, "diyas", "broke on the way", "5 break"))

S("6b41bc80", "Ravi's father", "he",
  "Ravi's father buys 25 kilograms of sugarcane at 8 rupees a kilogram, and pays 75 rupees for ice, cups and lemon. He makes 50 glasses of juice to sell at 12 rupees each, but 5 glasses stay unsold.",
  "Sugarcane 25 × ₹8, extras ₹75; 50 glasses at ₹12, 5 unsold",
  [("the sugarcane", 25, 8), ("the ice, cups and lemon", 75)],
  [("sold", 12, "{n} glasses at {p} rupees each")],
  lost=("He made 50 glasses of juice.", 50, 5, "glasses", "stayed unsold", "5 unsold"))

S("73b146df", "Rohan's sister", "she",
  "Rohan's sister spends 180 rupees on coloured paper, 70 on glue and glitter, and 50 on little flags. She makes 40 paper boats to sell at 12 rupees each, but the rain damages 5 of them.",
  "Costs ₹180, ₹70, ₹50; 40 boats at ₹12 each, 5 damaged",
  [("the coloured paper", 180), ("the glue and glitter", 70), ("the flags", 50)],
  [("sold", 12, "{n} boats at {p} rupees each")],
  lost=("She made 40 paper boats.", 40, 5, "boats", "were damaged by the rain", "5 damaged"))

S("a1dcf4af", "Deepa's mom", "she",
  "Deepa's mom spends 250 rupees on silk threads, 150 on decorative stones and 100 on packaging. She makes 25 rakhi sets, gives 5 away as gifts, and sells the rest at 40 rupees each.",
  "Costs ₹250, ₹150, ₹100; 25 sets, 5 gifts, ₹40 each",
  [("the silk threads", 250), ("the stones", 150), ("the packaging", 100)],
  [("sold", 40, "{n} rakhi sets at {p} rupees each")],
  lost=("She made 25 rakhi sets.", 25, 5, "sets", "were given as gifts", "5 gifts"))

S("afe0e807", "Priya's mother", "she",
  "Priya's mother spends 60 rupees on potatoes, 40 on spices, 100 on oil and 50 on flour. She makes 50 samosas, keeps 5 for the family, and sells the rest at 12 rupees each.",
  "Costs ₹60, ₹40, ₹100, ₹50; 50 samosas, 5 eaten, ₹12 each",
  [("the potatoes", 60), ("the spices", 40), ("the oil", 100), ("the flour", 50)],
  [("sold", 12, "{n} samosas at {p} rupees each")],
  lost=("She made 50 samosas.", 50, 5, "samosas", "were eaten at home", "5 eaten"))

# ── Some are not sold, and there are two prices ──

S("13bca1d7", "Priya's father", "he",
  "Priya's father buys 200 plain diyas at 3 rupees each and 100 fancy ones at 8 rupees each, and spends 250 rupees on paint. He sells painted diyas at 9 rupees and fancy ones at 12 rupees, but 20 painted ones break.",
  "200 plain at ₹3, 100 fancy at ₹8, paint ₹250; 20 break",
  [("the plain diyas", 200, 3), ("the fancy diyas", 100, 8), ("the paint and glitter", 250)],
  [("sold", 9, "{n} painted diyas at {p} rupees each"), (100, 12, "{n} fancy diyas at {p} rupees each")],
  lost=("All 200 plain diyas were painted.", 200, 20, "painted diyas", "broke", "20 break"))

S("179ea186", "Priya", "she",
  "Priya buys 8 kilograms of khoya at 250 rupees a kilogram, 3 kilograms of sugar at 40 rupees a kilogram, and dry fruits for 460 rupees. She sells 60 kaju katli at 45 rupees and barfi at 30 rupees, but 5 of the 40 barfi are damaged.",
  "Khoya 8 × ₹250, sugar 3 × ₹40, dry fruits ₹460; 5 damaged",
  [("the khoya", 8, 250), ("the sugar", 3, 40), ("the dry fruits", 460)],
  [(60, 45, "{n} pieces of kaju katli at {p} rupees each"), ("sold", 30, "{n} pieces of barfi at {p} rupees each")],
  lost=("Priya made 40 pieces of barfi.", 40, 5, "pieces of barfi", "were damaged", "5 damaged"))

S("43d26a1a", "Priya's father", "he",
  "Priya's father buys 200 diyas at 3 rupees each and spends 250 rupees on paints and glitter. While he paints, 20 diyas break. He sells the first 100 at 8 rupees each, and the rest at 6 rupees each.",
  "200 diyas at ₹3, paint ₹250; 20 break; 100 at ₹8, rest at ₹6",
  [("the diyas", 200, 3), ("the paints and glitter", 250)],
  [(100, 8, "the first {n} diyas at {p} rupees each"), ("rest", 6, "{n} diyas at the lower price of {p} rupees")],
  lost=("He bought 200 diyas.", 200, 20, "diyas", "broke", "20 break"))

S("5887181f", "Priya's father", "he",
  "Priya's father buys 200 diyas at 3 rupees each and spends 250 rupees on paint and glitter. While drying, 20 diyas crack. He sells 120 to a shopkeeper at 8 rupees each, and the rest at a street stall for 10 rupees each.",
  "200 diyas at ₹3, paint ₹250; 20 crack; 120 at ₹8, rest ₹10",
  [("the diyas", 200, 3), ("the paint and glitter", 250)],
  [(120, 8, "{n} diyas to the shopkeeper at {p} rupees each"), ("rest", 10, "{n} diyas at the stall for {p} rupees each")],
  lost=("He bought 200 diyas.", 200, 20, "diyas", "cracked", "20 crack"))

S("5eae9393", "Priya", "she",
  "Priya buys 200 diyas at 3 rupees each, and spends 250 rupees on paints and 150 on packaging. While drying, 20 diyas crack. She sells 120 to a shopkeeper at 12 rupees each, and the rest at a stall for 15 rupees each.",
  "200 at ₹3, paint ₹250, packing ₹150; 20 crack; 120 at ₹12",
  [("the diyas", 200, 3), ("the paints and glitter", 250), ("the packaging", 150)],
  [(120, 12, "{n} diyas to the shopkeeper at {p} rupees each"), ("rest", 15, "{n} diyas at the stall for {p} rupees each")],
  lost=("She bought 200 diyas.", 200, 20, "diyas", "cracked", "20 crack"))

S("7d389314", "Priya's father", "he",
  "Priya's father buys 200 packets of biscuits at 8 rupees each, and pays 200 rupees for transport. He finds 10 packets crushed. He sells 120 of the good ones at 14 rupees each, and the rest at 11 rupees each.",
  "200 packets at ₹8, transport ₹200; 10 crushed; 120 at ₹14",
  [("the packets", 200, 8), ("the transport", 200)],
  [(120, 14, "{n} packets at the full price of {p} rupees"), ("rest", 11, "{n} packets at the lower price of {p} rupees")],
  lost=("He bought 200 packets.", 200, 10, "packets", "were crushed", "10 crushed"))

S("8cfff8a8", "Priya's father", "he",
  "Priya's father buys 200 diyas at 3 rupees each and spends 250 rupees on paint and glitter. While drying, 20 diyas crack. He sells 120 to a shop owner at 8 rupees each, and the rest at a street stall for 6 rupees each.",
  "200 diyas at ₹3, paint ₹250; 20 crack; 120 at ₹8, rest ₹6",
  [("the diyas", 200, 3), ("the paint and glitter", 250)],
  [(120, 8, "{n} diyas to the shop owner at {p} rupees each"), ("rest", 6, "{n} diyas at the stall for {p} rupees each")],
  lost=("He bought 200 diyas.", 200, 20, "diyas", "cracked", "20 crack"))
