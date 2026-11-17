"""Batch 15, stories with a twist before the profit: a discount or a percentage
turned into a price, a count to work out first, or one item at a time.

Keyed by the first 8 characters of the question's uuid.
"""
from imported_15_lib import CHOOSE, L, MINUS, UL, W, f

LESSONS = {}

# ── A percentage has to become a price first ──

# Kabir's mom: 50 plates at 24, rent 100; 35 at +25%, 15 at 10% below cost.
l = L("50f220f0", "Kabir's mom")
l.intro("Kabir's mom buys 50 samosa plates at 24 rupees each and pays 100 rupees stall rent. She sells 35 plates at a profit of 25 per cent, and the other 15 at 10 per cent below the cost price. Does she make a profit or a loss overall?",
        "50 plates at ₹24, rent ₹100; 35 at +25%, 15 at −10%")
l.plan()
l.costs([("the plates", 50, 24), ("the stall rent", 100)])
l.b("35 plates sell at a profit of 25 per cent. But 25 per cent of what?",
    ask=CHOOSE(["of ₹24, the cost of a plate", "of ₹100, the rent", "of ₹35"], 0,
               "A profit percentage is always counted on the cost price. Each plate cost 24 rupees, so the profit on one plate is 25 per cent of 24."))
l.b("25 per cent is one quarter, and a quarter of 24 is 6. So each of these plates sells for 24 plus 6, which is 30 rupees.",
    W(l.nid(), "25% of 24 = 6"), W(l.nid(), "24 + 6 = 30"), UL("q", "35 at +25%"))
l.sale(35, 30, "{n} plates at {p} rupees each")
l.b("The other 15 plates sell below cost. 10 per cent of 24 is not a whole number of rupees, so let's take all 15 plates together.",
    UL("q", "15 at −10%"))
l.calc(15, "×", 24, "Those 15 plates cost {a} times {b}, which is {r} rupees.")
l.b("10 per cent is one tenth, so 10 per cent of 360 is 36. She gets 360 minus 36, which is 324 rupees for those plates.",
    W(l.nid(), "10% of 360 = 36"), W(l.nid(), "360 − 36 = 324"))
l.sale_vals.append(324)
l.sales_total()
l.profit()
l.b("Did you notice the rent? Leave it out and the profit looks 100 rupees bigger. The rent is money spent, so it belongs in the cost.")
l.check()
l.b("So with percentages: turn each one into rupees first, using the cost price. Then it is the usual plan: earned, take away spent.")
LESSONS[l.qid] = l.done()

# Meera's sparklers: 40 boxes at 75; 30 at +20%, 10 at 10% below cost.
l = L("66809e3b", "Meera")
l.intro("Meera buys 40 boxes of sparklers at 75 rupees each. She sells 30 boxes at a profit of 20 per cent, and the other 10 boxes at 10 per cent below her cost price. What is her profit or loss on all 40 boxes?",
        "40 boxes at ₹75; 30 at +20%, 10 at −10%")
l.plan()
l.costs([("the boxes", 40, 75)])
l.b("30 boxes sell at a profit of 20 per cent. But 20 per cent of what?",
    ask=CHOOSE(["of ₹75, the cost of a box", "of ₹40", "of ₹30"], 0,
               "A profit percentage is always counted on the cost price. Each box cost 75 rupees, so the profit on one box is 20 per cent of 75."))
l.b("20 per cent is one fifth, and 75 divided by 5 is 15. So each of these boxes sells for 75 plus 15, which is 90 rupees.",
    W(l.nid(), "20% of 75 = 15"), W(l.nid(), "75 + 15 = 90"), UL("q", "30 at +20%"))
l.sale(30, 90, "{n} boxes at {p} rupees each")
l.calc(10, "×", 75, "The 10 damp boxes sell below cost. Take them all together: they cost {a} times {b}, which is {r} rupees.",
       UL("q", "10 at −10%"))
l.b("10 per cent is one tenth, so 10 per cent of 750 is 75. She gets 750 minus 75, which is 675 rupees for those boxes.",
    W(l.nid(), "10% of 750 = 75"), W(l.nid(), "750 − 75 = 675"))
l.sale_vals.append(675)
l.sales_total()
l.profit()
l.b("Two different percentages, and both are counted on the cost price. One goes up from the cost, and the other comes down from it.")
l.check()
l.b("So with percentages: turn each one into rupees first, using the cost price. Then it is the usual plan: earned, take away spent.")
LESSONS[l.qid] = l.done()

# Vikram's chai: costs 450 + 150 + 100; 140 cups at 10, 15 of them at 20% off.
l = L("17b56841", "Vikram", "he", "his")
l.intro("Vikram spends 450 rupees on tea leaves, 150 on milk and 100 on sugar. He makes 140 cups of chai at 10 rupees a cup. 15 teachers each buy one cup at a 20 per cent discount, and the rest sell at full price.",
        "Costs ₹450, ₹150, ₹100; 140 cups at ₹10; 15 at 20% off")
l.plan()
l.costs([("the tea leaves", 450), ("the milk", 150), ("the sugar", 100)])
l.b("A teacher gets 20 per cent off a cup that costs 10 rupees. What does the teacher pay?",
    ask=CHOOSE(["₹2", "₹8", "₹10"], 1,
               "20 per cent of 10 rupees is 2 rupees. That is the discount, the part taken off. So the teacher pays 10 minus 2, which is 8 rupees."))
l.b("20 per cent of 10 is 2, so 2 rupees come off. The 2 is the discount, not the price: a teacher pays 8 rupees.",
    W(l.nid(), "20% of 10 = 2"), W(l.nid(), "10 − 2 = 8"), UL("q", "15 at 20% off"))
l.sale(15, 8, "{n} teachers' cups at {p} rupees each")
l.calc(140, MINUS, 15, "The other cups go at full price. {a} minus {b} leaves {r} cups.")
l.sale(125, 10, "{n} cups at the full {p} rupees")
l.sales_total()
l.profit()
l.check()
l.sumup("two")
LESSONS[l.qid] = l.done()

# Ravi's father's chai: supplies 1,500 + rent 300; 120 at 15, then 80 at 20% off.
l = L("44298d3a", "Ravi's father", "he", "his")
l.intro("Ravi's father buys tea supplies for 1,500 rupees and pays 300 rupees stall rent. He sells 120 cups of chai at 15 rupees each. Then he takes 20 per cent off the price and sells the last 80 cups.",
        "Supplies ₹1,500, rent ₹300; 120 cups at ₹15; 80 at 20% off")
l.plan()
l.costs([("the tea supplies", 1500), ("the stall rent", 300)])
l.sale(120, 15, "{n} cups at the full price of {p} rupees")
l.b("For the second half, 20 per cent comes off the 15 rupee price. What is the new price?",
    ask=CHOOSE(["₹3", "₹13", "₹12"], 2,
               "20 per cent is one fifth, and one fifth of 15 is 3. That 3 rupees is the discount. The new price is 15 minus 3, which is 12 rupees."))
l.b("One fifth of 15 is 3, so 3 rupees come off. The 3 is the discount, not the price: each cup now sells for 12 rupees.",
    W(l.nid(), "20% of 15 = 3"), W(l.nid(), "15 − 3 = 12"), UL("q", "80 at 20% off"))
l.sale(80, 12, "{n} cups at the lower price of {p} rupees")
l.sales_total()
l.profit()
l.b("One more thing to watch: the rent is paid after the match, but it is still a cost of the day. Leave it out and the profit looks 300 rupees too big.")
l.check()
l.sumup("two")
LESSONS[l.qid] = l.done()

# Priya's family: 200 diyas at 3, extras 250 + 350; 3/4 at 12, the rest at 25% off.
l = L("476ac6ba", "Priya's family", "they", "their")
l.intro("Priya's family buys 200 diyas at 3 rupees each, and spends 250 rupees on paint and 350 on wax and wicks. They sell 3 quarters of the diyas at 12 rupees each, and the rest at 25 per cent off that price.",
        "200 at ₹3, extras ₹250 + ₹350; 3/4 at ₹12, rest 25% off")
l.plan()
l.costs([("the diyas", 200, 3), ("the paint and glitter", 250), ("the wax and wicks", 350)])
l.b("3 quarters of the 200 diyas sell at the full price. How many diyas is that?",
    ask=CHOOSE(["50", "150", "75"], 1,
               "One quarter of 200 is 200 divided by 4, which is 50. So 3 quarters is 3 times 50, and that is 150 diyas."))
l.b("A quarter of 200 is 50, so 3 quarters is 150 diyas. The last quarter, 50 diyas, gets the discount.",
    W(l.nid(), "200 ÷ 4 = 50"), W(l.nid(), "3 × 50 = 150"), UL("q", "3/4 at ₹12"))
l.sale(150, 12, "{n} diyas at {p} rupees each")
l.b("25 per cent off means a quarter of the price comes off. A quarter of 12 is 3, so the discount price is 12 minus 3, which is 9 rupees.",
    W(l.nid(), "25% of 12 = 3"), W(l.nid(), "12 − 3 = 9"), UL("q", "rest 25% off"))
l.sale(50, 9, "{n} diyas at the discount price of {p} rupees")
l.sales_total()
l.profit()
l.check()
l.sumup("two")
LESSONS[l.qid] = l.done()

# ── A count to work out first ──

# Sugarcane juice: 80 canes at 10, extras 240; 2 canes make 5 glasses at 15.
l = L("3c4c96a1", "Meera's father", "he", "his")
l.intro("Meera's father buys 80 sugarcanes at 10 rupees each, and spends 240 rupees on ice, cups and lemon. Every 2 sugarcanes fill 5 glasses, and he sells each glass for 15 rupees. What is his profit?",
        "80 canes at ₹10, extras ₹240; 2 canes fill 5 glasses at ₹15")
l.plan()
l.costs([("the sugarcanes", 80, 10), ("the ice, cups and lemon", 240)])
l.b("He sells glasses, not sugarcanes. Every 2 sugarcanes fill 5 glasses. How do we find the glasses from 80 sugarcanes?",
    ask=CHOOSE(["80 × 5", "80 ÷ 2, then × 5", "80 ÷ 5, then × 2"], 1,
               "The sugarcanes go into the machine 2 at a time. So first count the pairs, 80 divided by 2, and then each pair gives 5 glasses."),
    )
l.calc(80, "÷", 2, "{a} divided by 2 is {r} pairs of sugarcanes.", UL("q", "2 canes fill 5 glasses"))
l.calc(40, "×", 5, "Each pair fills 5 glasses, so {a} times 5 is {r} glasses.")
l.sale(200, 15, "{n} glasses at {p} rupees each", only=True)
l.profit()
l.b("The slip to avoid is selling 80 glasses, one for each sugarcane. The story sells glasses, so the sugarcanes had to be turned into glasses first.")
l.check()
l.sumup("plain")
LESSONS[l.qid] = l.done()

# Chikki: 5 boxes at 360 with 24 bars each, transport 200; 12 crushed; 25 a bar.
l = L("82f365e9", "Priya's father", "he", "his")
l.intro("Priya's father buys 5 boxes of chikki at 360 rupees a box, with 24 bars in each box, and pays 200 rupees for transport. 12 bars get crushed, and he sells the rest at 25 rupees each. What is his profit from this sale?",
        "5 boxes at ₹360, 24 bars each; transport ₹200; 12 crushed")
l.plan()
l.costs([("the boxes", 5, 360), ("the transport", 200)])
l.calc(5, "×", 24, "He buys boxes, but he sells bars. So how many bars are there? 5 boxes of 24 bars: {a} times {b} is {r} bars.")
l.sold("He had 120 bars.", 120, 12, "bars", "were crushed", "12 crushed")
l.sale(108, 25, "{n} bars at {p} rupees each", only=True)
l.b("The story adds that he later spends 180 rupees on packaging for the next order. Does that come off this profit?",
    ask=CHOOSE(["Yes, subtract ₹180", "No, it belongs to the next order"], 1,
               "The question asks for the profit from this sale, before the packaging is counted. That 180 rupees is a cost of the next order, so we leave it out."))
l.profit()
l.check()
l.sumup("lost")
LESSONS[l.qid] = l.done()

# Diyas: 200 at 4, paints 300; 20 break; half at 12, half at 8.
l = L("9c6d7c7e", "Priya's father", "he", "his")
l.intro("Priya's father buys 200 diyas at 4 rupees each and spends 300 rupees on paints and glitter. While he paints, 20 diyas break. He sells half of the rest at 12 rupees each, and the other half at 8 rupees each.",
        "200 diyas at ₹4, paint ₹300; 20 break; half ₹12, half ₹8")
l.plan()
l.costs([("the diyas", 200, 4), ("the paints and glitter", 300)])
l.sold("He bought 200 diyas.", 200, 20, "diyas", "broke", "20 break")
l.calc(180, "÷", 2, "Half of them go at each price. {a} divided by 2 is {r} diyas in each half.", UL("q", "half ₹12, half ₹8"))
l.sale(90, 12, "{n} premium diyas at {p} rupees each")
l.sale(90, 8, "{n} simple diyas at {p} rupees each")
l.sales_total()
l.profit()
l.check()
l.sumup("two")
LESSONS[l.qid] = l.done()

# Kavya's class: cost 600, 90% of 200 samosas sold at 8.
l = L("cd9ea9ff", "Kavya's class", "they", "their")
l.intro("Kavya's class spends 600 rupees on ingredients and makes 200 samosas to sell at 8 rupees each. They sell 90 per cent of the samosas and give the rest away. What is their profit?",
        "Ingredients ₹600; 200 samosas at ₹8 each; 90% sold")
l.plan()
l.costs([("ingredients", 600)], "₹600")
l.b("They sold 90 per cent of the 200 samosas. How many samosas is that?",
    ask=CHOOSE(["90", "180", "20"], 1,
               "10 per cent of 200 is 20. And 90 per cent is 9 lots of that, so 9 times 20, which is 180 samosas."))
l.b("10 per cent of 200 is 20 samosas. So 90 per cent is 9 times as many, and that is 180 samosas sold.",
    W(l.nid(), "10% of 200 = 20"), W(l.nid(), "90% of 200 = 180"), UL("q", "90% sold"))
l.sale(180, 8, "{n} samosas at {p} rupees each", only=True)
l.profit()
l.b("Did you spot the trap? Selling all 200 would bring in more money, but 20 samosas were given away and earned nothing.")
l.check()
l.sumup("lost")
LESSONS[l.qid] = l.done()

# ── One item at a time ──


def per_item(key, who, pro, poss, intro, given, cost, price, n, things, one):
    l = L(key, who, pro, poss)
    l.intro(intro, given)
    l.b("Every %s costs the same and sells for the same. So we can find the profit on just one %s first." % (one, one),
        UL("q", given.split(";")[0]))
    gain = l.calc(price, MINUS, cost, "Selling price, take away cost price: {a} minus {b} is {r}. Each %s earns {who} {r} rupees." % one)
    choices = ["%s × %s" % (f(price), f(n)), "%s + %s" % (f(gain), f(n))]
    at = l.pk("piat", [0, 1, 2])
    choices.insert(at, "%s × %s" % (f(gain), f(n)))
    l.b("That is one %s. What do we do for all %s %s?" % (one, f(n), things),
        ask=CHOOSE(choices, at, "Each of the %s %s earns the same %s rupees. %s lots of %s means we multiply." % (
            f(n), things, f(gain), f(n), f(gain))))
    total = l.calc(gain, "×", n, "{a} times {b} is {r}. The total profit is {r} rupees.", answer=True)
    l.b("Careful with %s times %s. That is all the money that came in, not the profit, because every %s cost money too." % (f(price), f(n), one))
    sales = price * n
    spent = cost * n
    l.b("Check the long way. %s took in %s times %s, which is %s rupees, and spent %s times %s, which is %s rupees." % (
        l.who, f(n), f(price), f(sales), f(n), f(cost), f(spent)),
        W(l.nid(), "%s × %s = %s" % (f(n), f(price), f(sales))), W(l.nid(), "%s × %s = %s" % (f(n), f(cost), f(spent))))
    assert sales - spent == total
    l.calc(sales, MINUS, spent, "{a} minus {b} is {r}. Both ways agree.")
    l.b("So when every item has the same cost and the same price, find the profit on one, then multiply by how many were sold.")
    LESSONS[key] = l.done()


per_item("7eb928b5", "Ravi", "he", "his",
         "Ravi buys cricket balls for 45 rupees each and sells them for 63 rupees each. During the season he sells 20 balls. What is his total profit?",
         "Buys at ₹45, sells at ₹63; 20 balls sold",
         45, 63, 20, "balls", "ball")

per_item("a7e98512", "Meena's mother", "she", "her",
         "Meena's mother spends 8 rupees on ingredients for each samosa, and sells each one for 12 rupees. She makes and sells 25 samosas. What is her total profit?",
         "Each samosa costs ₹8, sells for ₹12; 25 sold",
         8, 12, 25, "samosas", "samosa")

# Ananya: packet 35 + ribbon 5, sold at 56, 12 packets.
l = L("ce5f4a38", "Ananya")
l.intro("Ananya buys packets of chai masala for 35 rupees each, and ties a ribbon that costs 5 rupees on each one. She sells them for 56 rupees each, and sells 12 packets. What is her total profit?",
        "Packet ₹35 + ribbon ₹5; sells at ₹56; 12 packets sold")
l.b("Every packet costs the same and sells for the same. So we can find the profit on just one packet first.",
    UL("q", "sells at ₹56"))
l.b("What does one finished packet really cost Ananya?",
    ask=CHOOSE(["₹35", "₹35 + ₹5 = ₹40", "₹56"], 1,
               "She pays 35 rupees for the packet, and then 5 rupees more for its ribbon. Both are money spent on that one packet."))
l.calc(35, "+", 5, "The packet and its ribbon together: {a} plus {b} is {r} rupees. Leaving out the ribbon is the trap in this story.",
       UL("q", "ribbon ₹5"))
l.calc(56, MINUS, 40, "Selling price, take away cost: {a} minus {b} is {r}. Each packet earns her {r} rupees.")
l.calc(12, "×", 16, "She sells 12 packets, so we multiply. {a} times {b} is {r}. Ananya's total profit is {r} rupees.", answer=True)
l.b("Check the long way. She took in 12 times 56, which is 672 rupees, and spent 12 times 40, which is 480 rupees.",
    W(l.nid(), "12 × 56 = 672"), W(l.nid(), "12 × 40 = 480"))
l.calc(672, MINUS, 480, "{a} minus {b} is {r}. Both ways agree.")
l.b("So when every item has the same cost and the same price, find the full cost of one, then the profit on one, then multiply.")
LESSONS[l.qid] = l.done()
