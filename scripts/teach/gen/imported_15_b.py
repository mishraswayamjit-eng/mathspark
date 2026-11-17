"""Batch 15, stories with a twist after the profit: a profit percentage, a donation,
an unknown number bought, or a "how much more" comparison.

Keyed by the first 8 characters of the question's uuid.
"""
from imported_15_lib import ANS, CHOOSE, CIRC, GIVEN, L, LB, MINUS, NOTE, STRIKE, UL, W

LESSONS = {}

PCT_SUM = [
    "So for a profit percentage: find the profit, put it over the cost, and turn that fraction into a percentage.",
    "So the method is: find the profit in rupees, compare it with the money spent, and write that as a percentage.",
]

# ── Profit as a percentage of the cost ──

# Meera's samosas: cost 240 + 60, 50 of 60 sold at 8.
l = L("0b7c7609", "Meera")
l.intro("Meera spends 240 rupees on ingredients and 60 rupees on packaging. She makes 60 samosas at 8 rupees each, but 10 are left over and given away. What is her profit, as a percentage of what she spent?",
        "Costs ₹240 + ₹60; 60 samosas at ₹8 each, 10 unsold")
l.plan()
l.costs([("the ingredients", 240), ("the packaging", 60)])
l.sold("Meera made 60 samosas.", 60, 10, "samosas", "were given away", "10 unsold")
l.sale(50, 8, "{n} samosas at {p} rupees each", only=True)
l.profit(answer=False)
l.b("Now the percentage. A profit percentage compares the profit with one other amount. Which one?",
    ask=CHOOSE(["the ₹300 she spent", "the ₹400 she earned", "the 60 samosas"], 0,
               "The question says it: a percentage of the money she spent. A profit percentage is always measured against the cost."))
l.line("100/300 = 1/3", "So write the profit over the cost: 100 over 300. Both numbers divide by 100, so that fraction is one third.")
lid = l.nid()
l.b("one third of 100 per cent is 33 and a third per cent. That is Meera's profit percentage.",
    LB(lid, "Profit % = 1/3 of 100% = 33⅓%", "answer"), CIRC(lid, "33⅓%"))
l.b("Careful: putting the profit over the 400 rupees she earned gives a smaller answer, and it is one of the choices. The cost goes underneath, not the sales.")
l.line("1/3 of 300 = 100", "Check: one third of 300 is 100, and 100 rupees is exactly her profit.")
l.b(l.pk("psum", PCT_SUM))
LESSONS[l.qid] = l.done()

# Ravi's samosas: cost 600, 160 of 200 sold at 5.
l = L("916a4ec4", "Ravi", "he", "his")
l.intro("Ravi spends 600 rupees on ingredients and makes 200 samosas to sell at 5 rupees each. At the end, 40 samosas are still unsold. What percentage profit or loss does he make on the money he spent?",
        "Ingredients ₹600; 200 samosas at ₹5 each, 40 unsold")
l.plan()
l.costs([("ingredients", 600)], "₹600")
l.sold("Ravi made 200 samosas.", 200, 40, "samosas", "stayed unsold", "40 unsold")
l.sale(160, 5, "{n} samosas at {p} rupees each", only=True)
l.calc(800, MINUS, 600, "He earned more than he spent, so it is a profit. {a} minus {b} is {r} rupees.")
l.b("Now the percentage. We compare that 200 rupees of profit with which amount?",
    ask=CHOOSE(["the ₹800 he earned", "the ₹600 he spent", "the 200 samosas"], 1,
               "The question asks for the percentage on his investment, the money he put in. That is the 600 rupees he spent."))
l.line("200/600 = 1/3", "So write the profit over the cost: 200 over 600. Both numbers divide by 200, so that fraction is one third.")
lid = l.nid()
l.b("one third of 100 per cent is 33 and a third per cent. Ravi makes a profit of 33 and a third per cent.",
    LB(lid, "Profit % = 1/3 of 100% = 33⅓%", "answer"), CIRC(lid, "33⅓%"))
l.line("1/3 of 600 = 200", "Check: one third of 600 is 200, and 200 rupees is exactly his profit.")
l.b(l.pk("psum", PCT_SUM))
LESSONS[l.qid] = l.done()

# Deepa's rakhis: cost 400, 40 of 50 sold at 12.
l = L("3ee52de2", "Deepa")
l.intro("Deepa spends 400 rupees on materials and makes 50 rakhis to sell at 12 rupees each. At the end of the day, 10 rakhis are unsold. What percentage profit does she make on the money she spent?",
        "Materials ₹400; 50 rakhis at ₹12 each, 10 unsold")
l.plan()
l.costs([("materials", 400)], "₹400")
l.sold("Deepa made 50 rakhis.", 50, 10, "rakhis", "stayed unsold", "10 unsold")
l.sale(40, 12, "{n} rakhis at {p} rupees each", only=True)
l.profit(answer=False)
l.b("Now the percentage. We compare that 80 rupees of profit with which amount?",
    ask=CHOOSE(["the ₹480 she earned", "the ₹400 she spent", "the 50 rakhis"], 1,
               "The question asks for the percentage on her investment, the money she put in. That is the 400 rupees she spent."))
l.line("80/400 = 1/5", "So write the profit over the cost: 80 over 400. Divide the top and the bottom by 80, and that fraction is one fifth.")
lid = l.nid()
l.b("one fifth of 100 per cent is 20 per cent. Deepa makes a profit of 20 per cent.",
    ANS(lid, "1/5 of 100 = 20"), CIRC(lid, "20"), NOTE(lid, "20", "per cent"))
l.line("20% of 400 = 80", "Check: 20 per cent of 400 is 80, and 80 rupees is exactly her profit.")
l.b(l.pk("psum", PCT_SUM))
LESSONS[l.qid] = l.done()

# ── A share of the profit is given away ──

DON_SUM = [
    "So work in order: the cost, the sales, the profit, and only then the percentage. And always ask: a percentage of which amount?",
    "So the method is: find the profit first, then take the percentage of exactly the amount the story names.",
]

# Kavya: cost 600 + 150, sales 50 × 12 and 40 × 15, gives 20% of the profit.
l = L("22c1cc52", "Kavya")
l.intro("Kavya spends 600 rupees on ingredients and 150 rupees on stall rent. She sells 50 cups of chai at 12 rupees each and 40 samosa plates at 15 rupees each. Then she donates 20 per cent of her profit. How much of the profit is left?",
        "Costs ₹600 + ₹150; 50 × ₹12, 40 × ₹15; gives 20% of profit")
l.plan()
l.costs([("the ingredients", 600), ("the stall rent", 150)])
l.sale(50, 12, "{n} cups of chai at {p} rupees each")
l.sale(40, 15, "{n} samosa plates at {p} rupees each")
l.sales_total()
l.profit(answer=False)
l.b("Now the donation: 20 per cent. But 20 per cent of which amount?",
    ask=CHOOSE(["of the ₹1,200 she earned", "of the ₹450 profit", "of the ₹750 she spent"], 1,
               "The story says 20 per cent of her profit. So the donation is worked out on the 450 rupees, not on everything she earned."),
    )
l.line("10% of 450 = 45", "10 per cent is one tenth, so 10 per cent of 450 is 45.")
l.line("20% of 450 = 90", "20 per cent is double that. So 90 rupees go to the school.", UL("q", "20% of profit"))
l.calc(450, MINUS, 90, "Take the donation away from the profit. {a} minus {b} is {r}, so Kavya has {r} rupees left.", answer=True)
l.calc(360, "+", 90, "Check: what she kept and what she gave should make the whole profit. {a} plus {b} is {r}. It fits.")
l.b(l.pk("dsum", DON_SUM))
LESSONS[l.qid] = l.done()

# Meera: cost 240 + 60, sells 60 at 8, gives 25% of the profit.
l = L("5fefd62f", "Meera")
l.intro("Meera spends 240 rupees on ingredients and 60 rupees on paper plates. She makes 60 samosas and sells each one for 8 rupees. Then she gives 25 per cent of her profit to charity. How much does she donate?",
        "Costs ₹240 + ₹60; 60 samosas at ₹8; gives 25% of profit")
l.plan()
l.costs([("the ingredients", 240), ("the paper plates", 60)])
l.sale(60, 8, "{n} samosas at {p} rupees each", only=True)
l.profit(answer=False)
l.b("Now the donation: 25 per cent. But 25 per cent of which amount?",
    ask=CHOOSE(["of the ₹480 she earned", "of the ₹180 profit", "of the ₹300 she spent"], 1,
               "The story says 25 per cent of her profit. So the donation is worked out on the 180 rupees, not on everything she earned."))
l.line("25% = 1/4", "25 per cent is the same as one quarter. So we need a quarter of the profit, and that means dividing by 4.",
       UL("q", "25% of profit"))
l.calc(180, "÷", 4, "{a} divided by 4 is {r}. Meera donates {r} rupees.", answer=True)
l.calc(45, "×", 4, "Check: 4 quarters make the whole. {a} times 4 is {r}, and that is the profit.")
l.b(l.pk("dsum", DON_SUM))
LESSONS[l.qid] = l.done()

# Meera: cost 400 + 100, sells 80% of 100 at 8, spends 25% of the profit on a book.
l = L("6e6134ea", "Meera")
l.intro("Meera spends 400 rupees on ingredients and 100 rupees on packaging. She makes 100 samosas and sells 80 per cent of them at 8 rupees each. Then she spends 25 per cent of her profit on a maths book. What does the book cost?",
        "Costs ₹400 + ₹100; 80% of 100 at ₹8; book 25% of profit")
l.plan()
l.costs([("the ingredients", 400), ("the packaging", 100)])
l.b("She made 100 samosas and sold 80 per cent of them. How many is that?",
    ask=CHOOSE(["100", "80", "20"], 1,
               "Per cent means out of 100. She made exactly 100 samosas, so 80 per cent of them is 80 samosas."))
l.line("80% of 100 = 80", "80 per cent of 100 is 80. The other 20 were given away, so they bring in nothing.")
l.sale(80, 8, "{n} samosas at {p} rupees each", only=True)
l.profit(answer=False)
l.line("25% = 1/4", "The book costs 25 per cent of the profit. 25 per cent is one quarter, so we divide the profit by 4.",
       UL("q", "25% of profit"))
l.calc(140, "÷", 4, "{a} divided by 4 is {r}. The maths book costs {r} rupees.", answer=True)
l.b("Here is the trap: taking a quarter of the 640 rupees she earned. The story says a quarter of the profit, and the profit is much smaller.")
l.calc(35, "×", 4, "Check: 4 quarters make the whole. {a} times 4 is {r}, and that is the profit.")
l.b(l.pk("dsum", DON_SUM))
LESSONS[l.qid] = l.done()

# Vikram: cost 250, sales 350, gives 20% of the profit.
l = L("9041aab7", "Vikram", "he", "his")
l.intro("Vikram buys ingredients for 250 rupees and sells samosas worth 350 rupees in total. He donates 20 per cent of his profit to a charity for planting trees. How much does he donate?",
        "Spent ₹250, sold for ₹350; gives 20% of profit")
l.calc(350, MINUS, 250, "First we need the profit: money earned, take away money spent. {a} minus {b} is {r} rupees.")
l.b("Now the donation: 20 per cent. But 20 per cent of which amount?",
    ask=CHOOSE(["of the ₹350 he earned", "of the ₹100 profit", "of the ₹250 he spent"], 1,
               "The story says 20 per cent of his profit. So the donation is worked out on the 100 rupees, not on the 350 rupees he took in."))
l.b("Per cent means out of every 100. And his profit is exactly 100 rupees, which makes this a friendly one.",
    UL("q", "20% of profit"))
lid = l.nid()
l.b("20 per cent of 100 is 20. Vikram donates 20 rupees.",
    ANS(lid, "20% of 100 = 20"), CIRC(lid, "20", 2))
lid = l.nid()
l.b("Here is the trap. 20 per cent of the 350 rupees he earned would be 70 rupees, and that is one of the choices. But the gift comes out of the profit.",
    W(lid, "20% of 350 = 70"), STRIKE(lid, "20% of 350 = 70", "not the profit"))
l.calc(100, MINUS, 20, "Check that it makes sense: {a} minus {b} leaves him {r} rupees of profit. He gives the small share and keeps the big one.")
l.b(l.pk("dsum", DON_SUM))
LESSONS[l.qid] = l.done()

# Sneha: cost 750, sells 150 at 8, gives 10% of her EARNINGS.
l = L("83b1192f", "Sneha")
l.intro("Sneha spends 750 rupees on tea leaves, sugar and milk. She sells 150 cups of chai at 8 rupees each, then gives 10 per cent of her total earnings to the school. How much profit is left after the donation?",
        "Spent ₹750; 150 cups at ₹8 each; gives 10% of earnings")
l.plan()
l.costs([("tea leaves, sugar and milk", 750)], "₹750")
l.sale(150, 8, "{n} cups at {p} rupees each", only=True)
l.b("Now the donation: 10 per cent. But 10 per cent of which amount?",
    ask=CHOOSE(["of the ₹1,200 she earned", "of her profit", "of the ₹750 she spent"], 0,
               "Read that line once more: 10 per cent of her total earnings. Earnings means all the money that came in, the 1,200 rupees."))
l.calc(1200, "÷", 10, "10 per cent is one tenth, so we divide by 10. {a} divided by 10 is {r} rupees for the school.",
       UL("q", "10% of earnings"))
l.calc(1200, MINUS, 120, "After the donation she has {a} minus {b}, which is {r} rupees.")
l.calc(1080, MINUS, 750, "Now take away what she spent. {a} minus {b} is {r}. Sneha has {r} rupees of profit left.", answer=True)
l.b("Careful: in this story the donation comes out of the earnings, not out of the profit. Always read which amount the percentage belongs to.")
l.add([330, 120, 750], "Check: profit, donation and cost together should use up all she earned. {sum} is {r}. It fits.")
l.b(l.pk("dsum", DON_SUM))
LESSONS[l.qid] = l.done()

# ── How many were bought? ──

# Diyas at 3; extras 200 + 100; 80% at 12, 20% at 7; profit 500.
l = L("0b810d43", "Priya's father", "he", "his")
l.intro("Priya's father buys diyas at 3 rupees each, and spends 200 rupees on paints and 100 on glitter. He sells 80 per cent at 12 rupees and 20 per cent at 7 rupees, and makes 500 rupees profit. How many diyas did he buy?",
        "Buys at ₹3 each; extras ₹200 + ₹100; profit ₹500")
l.beats[0]["board"].append(GIVEN("q2", "Sells 80% at ₹12 and 20% at ₹7"))
l.b("We don't know how many diyas there are, so let's watch a small group of 10. Out of every 10 diyas, 8 sell at the full price and 2 at the lower price.",
    UL("q2", "80% at ₹12"), UL("q2", "20% at ₹7"), W(l.nid(), "80% of 10 = 8"), W(l.nid(), "20% of 10 = 2"))
l.calc(8, "×", 12, "The 8 diyas at 12 rupees each bring in {r} rupees.")
l.calc(2, "×", 7, "The 2 diyas at 7 rupees each bring in {r} rupees.")
l.calc(96, "+", 14, "Together, {a} plus {b} is {r} rupees coming in from every 10 diyas.")
l.calc(10, "×", 3, "But those 10 diyas cost 3 rupees each to buy. 10 times 3 is {r} rupees.")
l.calc(110, MINUS, 30, "So every group of 10 diyas leaves him {a} minus {b}, which is {r} rupees.", note="from every 10 diyas")
l.b("That 80 rupees from each group has two jobs to do. What must all the groups add up to?",
    ask=CHOOSE(["₹500, just the profit", "₹300 + ₹500 = ₹800", "₹500 − ₹300 = ₹200"], 1,
               "Before there is any profit, the paints and glitter must be paid for. That is 300 rupees, and then the 500 rupees of profit comes on top."))
l.add([200, 100, 500], "Paints, glitter and profit: {sum} is {r} rupees to be covered.")
l.calc(800, "÷", 80, "Each group gives 80 rupees. {a} divided by {b} is {r}, so he needs 10 groups.")
l.calc(10, "×", 10, "10 groups of 10 diyas is {r} diyas. That is how many he bought.", answer=True)
l.b("Check with 100 diyas. 80 of them sell at 12 rupees and 20 at 7 rupees. That is 960 plus 140, which is 1,100 rupees.",
    W(l.nid(), "80 × 12 = 960"), W(l.nid(), "20 × 7 = 140"), W(l.nid(), "960 + 140 = 1,100"))
l.b("The cost is 100 times 3, plus the 300 for paints and glitter, so 600 rupees. And 1,100 minus 600 is 500, the profit in the story.",
    W(l.nid(), "100 × 3 + 300 = 600"), W(l.nid(), "1,100 − 600 = 500"))
l.b("So when the number of things is hidden, find what one small group leaves you. Then see how many groups cover the extra costs and the profit.")
LESSONS[l.qid] = l.done()

# Diyas at 3, sold at 8; extras 400 + 200 + 300; profit 600.
l = L("2c17fea1", "Priya's father", "he", "his")
l.intro("Priya's father buys diyas at 3 rupees each. He spends 400 rupees on paints, 200 on glitter and 300 on a tempo. He sells every diya at 8 rupees and makes a profit of 600 rupees. How many diyas did he buy?",
        "Buys ₹3, sells ₹8; extras ₹400, ₹200, ₹300; profit ₹600")
l.calc(8, MINUS, 3, "We don't know how many diyas there are, so start with just one. He buys it for 3 rupees and sells it for 8, so each diya leaves him {r} rupees.",
       UL("q", "Buys ₹3, sells ₹8"), note="from each diya")
l.add([400, 200, 300], "Now the extra costs: the paints, the glitter and the tempo. {sum} is {r} rupees.", note="extra costs")
l.b("Those 5 rupees from each diya have to add up to how much?",
    ask=CHOOSE(["₹600, just the profit", "₹900 + ₹600 = ₹1,500", "₹900 − ₹600 = ₹300"], 1,
               "The 5 rupees from each diya must first pay back the 900 rupees of extras. Only after that does the 600 rupees of profit appear. So they cover both."))
l.calc(900, "+", 600, "So the diyas must bring in {a} plus {b}, which is {r} rupees, 5 rupees at a time.")
l.calc(1500, "÷", 5, "How many 5s make {a}? {a} divided by 5 is {r}. He bought {r} diyas.", answer=True)
l.b("The slip here is dividing only the 600 rupees of profit by 5. That forgets the paints, the glitter and the tempo, which the diyas have to pay for first.")
l.calc(300, "×", 8, "Check with 300 diyas. Selling them brings in {a} times 8, which is {r} rupees.")
l.b("Buying them costs 300 times 3, which is 900, plus 900 of extras: 1,800 rupees. And 2,400 minus 1,800 is 600, the profit in the story.",
    W(l.nid(), "300 × 3 + 900 = 1,800"), W(l.nid(), "2,400 − 1,800 = 600"))
l.b("So when the number of things is hidden, find what one of them leaves you. Then see how many it takes to cover the extra costs and the profit.")
LESSONS[l.qid] = l.done()

# ── How much more? ──

# Deepa: 20 unsold rose garlands at 40.
l = L("249c24ef", "Deepa")
l.intro("Deepa sells all her marigold garlands, and 60 of her 80 rose garlands at 40 rupees each. The other 20 rose garlands are donated. If she had sold those 20 as well, how much more profit would she have made?",
        "80 rose garlands bought at ₹25; 60 sold at ₹40, 20 unsold")
l.b("This story is full of numbers, and we could work out two whole profits. There is a quicker way: compare the real day with the imagined day, where every rose garland sells.")
l.b("Between the two days, which amount changes?",
    ask=CHOOSE(["what she paid for the garlands", "the marigold sales", "the money from 20 rose garlands"], 2,
               "She bought the same garlands on both days, and sold the same marigolds. The only difference is whether those last 20 rose garlands bring in money."))
l.b("She paid for all 80 rose garlands either way, so the cost does not move. The ribbons, the transport and the marigolds stay the same too.",
    UL("q", "80 rose garlands bought at ₹25"))
l.calc(20, "×", 40, "So the only extra is 20 more garlands sold at 40 rupees each. {a} times {b} is {r}. She would have made {r} rupees more.",
       CIRC("q", "20 unsold"), answer=True)
l.b("It is tempting to take the 25 rupees cost off each of those garlands. But that money was already spent on both days, so it does not change the gap.")
l.b("Check with the rose sales. On the imagined day, 80 times 40 is 3,200 rupees. On the real day, 60 times 40 is 2,400 rupees.",
    W(l.nid(), "80 × 40 = 3,200"), W(l.nid(), "60 × 40 = 2,400"))
l.calc(3200, MINUS, 2400, "{a} minus {b} is {r}. The same answer, and everything else in the story cancels out.")
l.b("So when a question asks how much more, look for the one thing that changes. Everything that stays the same can be left alone.")
LESSONS[l.qid] = l.done()
