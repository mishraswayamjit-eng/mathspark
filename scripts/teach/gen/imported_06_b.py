"""Imported batch 06, part b: word problems that become one two-step equation, a·x ± b = c.

Each lesson has its own story sentences; the shared builder (imported_06_lib.plain) writes the
equation, computes every board line, and adds the solving beats.
"""
from imported_06_lib import B, FIG, N, W, plain

LESSONS = {}


def add(*args, **kw):
    qid, script = plain(*args, **kw)
    LESSONS[qid] = script


# 9x + 25 = 133
add("01800dd4", "x", 9, "+", 25, 133,
    given="9 packets at ₹x each + ₹25 sweets = ₹133",
    intro="Riya buys 9 packets of samosas and a 25 rupee box of sweets, and the bill is 133 rupees. "
          "One packet costs x rupees, and x is what we are after.",
    eq_q="Let's turn the story into an equation. Which one fits?",
    wrongs=["x + 25 = 133", "9x − 25 = 133"],
    eq_if="There are 9 packets, so the samosas cost 9 times x. The sweets are paid for as well, so the 25 is added on.",
    build="9 packets at x rupees each cost 9 x. Add 25 for the sweets, and that makes the whole bill, 133.",
    marks=[N("e1", "9x", "samosas"), N("e1", "25", "sweets")],
    tail=" So one packet costs 12 rupees.",
    trap=B("Notice we did not stop at 108. That is the cost of all 9 packets together, not of one."),
    check="Let's check with the bill. 9 times 12 is 108, and 108 plus 25 is 133. It matches.",
    summ="So: write the story as an equation, take away the extra, then divide by the number of packets.")

# 3x + 14 = 50
add("022a9095", "x", 3, "+", 14, 50,
    given="3 packets at ₹x each + ₹14 sweets = ₹50",
    intro="Arjun pays 50 rupees in all: for 3 packets of samosas at x rupees each, and a 14 rupee box of sweets. Let's find x.",
    eq_q="Which equation tells this story?",
    wrongs=["3x = 50 + 14", "3 + x + 14 = 50"],
    eq_if="3 packets at x rupees each is 3 times x. The 14 for sweets is part of the 50 he paid, "
          "so it sits on the same side as the 3 x.",
    build="3 x for the samosas, plus 14 for the sweets, equals 50.",
    asks="div",
    tail=" Each packet costs 12 rupees.",
    trap=B("The slip to watch for is dividing 50 by 3 straight away. The sweets have to come off first."),
    check="Check: 3 times 12 is 36, and 36 plus 14 is 50. That is exactly what he paid.",
    summ="First take off what is added, then divide. Undo the plus before the times.")

# 9x + 18 = 99
add("074e034c", "x", 9, "+", 18, 99,
    given="packets at ₹9 each + ₹18 stencils = ₹99",
    intro="Meera spends 99 rupees. Some of it buys packets of powder at 9 rupees each, and 18 rupees goes on stencils. "
          "How many packets? Let's call that number x.",
    eq_q="x packets at 9 rupees each, and the stencils. Which equation fits?",
    wrongs=["9x = 99", "9x − 18 = 99"],
    eq_if="The 99 rupees pays for the packets and the stencils together. So it is 9 x for the packets, with 18 added.",
    build="x packets at 9 rupees each cost 9 x. Add the 18 for stencils to get 99.",
    tail=" Meera bought 9 packets.",
    trap=B("Did you see 11 among the choices? That is 99 divided by 9, which forgets the stencils.",
           W("t", "99 ÷ 9 = 11")),
    check="Check: 9 packets at 9 rupees is 81, and 81 plus 18 is 99. It works.",
    summ="Take off the one-time cost first. What is left paid for the packets, so divide it by the price.")

# 3x + 7 = 52
add("0f2b3c34", "x", 3, "+", 7, 52,
    given="3 equal boxes + 7 left over = 52 laddoos",
    intro="Aarav has 52 laddoos. He fills 3 boxes with the same number in each, and 7 are left over. "
          "Let x be the number in one box.",
    eq_q="Which equation matches the laddoos?",
    wrongs=["3x − 7 = 52", "x + 7 = 52"],
    eq_if="Count all 52: there are 3 boxes of x, and the 7 loose ones are on top of that. So it is 3 x plus 7.",
    build="3 boxes hold 3 x laddoos. With the 7 left over, that makes all 52.",
    marks=[N("e1", "3x", "in boxes"), N("e1", "7", "left over")],
    tail=" There are 15 laddoos in each box.",
    check="Check: 3 boxes of 15 is 45, and 45 plus the 7 left over is 52. Just right.",
    summ="Leftovers come off first. Then share what remains equally among the boxes.")

# 45 + 7x = 136
add("1e2a3951", "x", 7, "+", 45, 136, const_first=True,
    given="₹45 at the start + 7 cups sold = ₹136",
    intro="Arjun's cash box starts with 45 rupees. He sells 7 cups of chai, and now the box holds 136 rupees. "
          "We want the price of one cup, x.",
    eq_q="Which equation describes the cash box?",
    wrongs=["7x = 136", "45x + 7 = 136"],
    eq_if="The box already had 45 rupees in it. Selling 7 cups at x rupees each added 7 x. Together they make 136.",
    build="45 rupees to begin with, plus 7 x from the chai, equals 136 at the end.",
    marks=[N("e1", "45", "at the start"), N("e1", "7x", "from chai")],
    tail=" One cup of chai costs 13 rupees.",
    trap=B("The trap is to divide 136 by 7. But not all of that money came from chai: 45 was there from the start."),
    check="Check: 7 cups at 13 rupees is 91. Add the 45 he started with, and we get 136.",
    summ="Take away what was there at the start. The rest was earned, so divide it by the number of cups.")

# 4x − 5 = 9 × 7
add("2a3a9d94", "x", 4, "−", 5, 63,
    given="4 boxes − 5 given away = 9 bags of 7",
    intro="Riya buys 4 boxes of chocolates, gives 5 away, and packs the rest into 9 bags with 7 in each. "
          "How many chocolates were in one box? Call it x.",
    pre=[B("Start at the end of the story, where we have real numbers. 9 bags with 7 in each is 63 chocolates.",
           W("p1", "9 × 7 = 63"))],
    eq_q="Those 63 are what was left after 5 were given away. Which equation says that?",
    wrongs=["4x + 5 = 63", "x − 5 = 63"],
    eq_if="She began with 4 boxes of x, which is 4 x. Giving 5 away makes that smaller, so we subtract 5, and 63 are left.",
    build="4 x chocolates to begin with, minus the 5 she gave away, leaves 63.",
    tail=" Each box had 17 chocolates.",
    trap=B("Don't stop at 68. That is all 4 boxes together, and it is sitting among the choices to catch you."),
    check="Check: 4 boxes of 17 is 68. Give away 5 and 63 are left, which is 9 bags of 7.",
    summ="Work out the end of the story first, then add back what was given away, then share among the boxes.")

# x + 2x − 17 = 31
add("3916a850", "x", 3, "−", 17, 31,
    given="Monday: some. Tuesday: twice as many more. Used 17. Left 31",
    intro="Ananya has some stickers on Monday. On Tuesday her friend gives her twice as many as she has. "
          "Then she uses 17, and 31 are left. Let x be her stickers on Monday.",
    eq_q="After her friend's gift on Tuesday, how many stickers does Ananya have?",
    right="3x", wrongs=["2x", "x + 2"],
    eq_if="She keeps her own x stickers and gets 2 x more. x plus 2 x is 3 x. The slip is to forget the ones she already had.",
    build="Her own x, plus 2 x from her friend, makes 3 x. Then she uses 17, and 31 are left.",
    lead=[FIG("f1", {"kind": "barModel", "bars": [{"segments": [
        {"units": 1, "label": "x", "tone": "a"}, {"units": 2, "label": "2x", "tone": "b"}], "brace": "3x"}]}),
        W("s", "x + 2x = 3x")],
    asks="div",
    tail=" Ananya had 16 stickers on Monday.",
    check="Check: 16 on Monday, and 32 more on Tuesday, makes 48. Use 17, and 31 are left.",
    checklines=["16 + 32 = 48", "48 − 17 = 31"],
    summ="Build the story step by step using x, then undo it backwards: add back what was used, then divide.")

# 5x − 7 = 93
add("3a5bf65d", "x", 5, "−", 7, 93,
    given="5 equal boxes − 7 eaten = 93 laddoos",
    intro="Sahil fills 5 boxes with the same number of laddoos, then eats 7 from one box. Now 93 are left in all. "
          "How many did each box have at first? Call it x.",
    eq_q="Which equation fits?",
    wrongs=["5x + 7 = 93", "5(x − 7) = 93"],
    eq_if="5 boxes of x is 5 x. He takes 7 out of just one box, so the total drops by 7, only once. That leaves 93.",
    build="5 x laddoos at first, minus the 7 he ate, equals 93.",
    tail=" Each box had 20 laddoos.",
    trap=B("Careful: the 7 came out of one box, not out of every box. So we added back 7 just once."),
    check="Check: 5 boxes of 20 is 100. Eat 7, and 93 are left. It works.",
    summ="To get back to the start, put back what was taken, then share equally.")

# 4x + 11 = 35
add("3b94af7b", "x", 4, "+", 11, 35,
    given="flowers after x mornings = 4x + 11",
    intro="The expression 4 x plus 11 tells us how many flowers Meera has after x mornings. Today she has 35. "
          "How many mornings has she picked?",
    eq_q="We know she has 35 flowers. What do we do with the expression?",
    wrongs=["4 × 35 + 11", "4x = 35 + 11"],
    eq_if="The expression counts her flowers, and we know the count is 35. So we set the expression equal to 35, "
          "and look for the x that makes it true.",
    build="4 flowers each morning for x mornings, plus the 11 she had already, equals 35.",
    asks="div",
    tail=" She picked flowers on 6 mornings.",
    check="Check: 6 mornings of 4 flowers is 24, and 24 plus 11 is 35.",
    summ="When you know what an expression equals, write the equation and undo it: the plus first, then the times.")

# 5x + 7 = 52
add("3d306b01", "x", 5, "+", 7, 52,
    given="bags of 5 + 7 on a plate = 52 chocolates",
    intro="Ananya uses 52 chocolates. She puts 5 in each goodie bag, and 7 more on a plate for the adults. "
          "How many bags did she make? Call it x.",
    eq_q="Which equation fits the chocolates?",
    wrongs=["5x = 52", "5 + x + 7 = 52"],
    eq_if="x bags with 5 in each is 5 x chocolates. The 7 on the plate are extra, so they are added to reach 52.",
    build="5 x in the bags, plus 7 on the plate, equals 52.",
    tail=" She made 9 goodie bags.",
    trap=B("If you divide 52 by 5 straight away, it does not even come out exactly. That is a sign the 7 must come off first."),
    check="Check: 9 bags of 5 is 45, and 45 plus 7 is 52.",
    summ="Take off the extras first, then divide by how many go in each bag.")

# 5x + 3 × 10 = 95
add("5b86c2a9", "x", 5, "+", 30, 95,
    given="5 chai at ₹x + 3 biscuits at ₹10 = ₹95",
    intro="Raju sells 5 cups of chai and 3 packets of biscuits for 95 rupees in all. A packet of biscuits is 10 rupees. "
          "What does one cup of chai cost? That is x.",
    pre=[B("Start with what we know. 3 packets at 10 rupees each is 30 rupees for biscuits.", W("p1", "3 × 10 = 30"))],
    eq_q="Now, which equation fits the 95 rupees?",
    wrongs=["5x = 95", "5x + 10 = 95"],
    eq_if="The 95 rupees is chai and biscuits together. The chai is 5 x, and all 3 packets of biscuits add 30.",
    build="5 x for the chai, plus 30 for the biscuits, equals 95.",
    tail=" A cup of chai costs 13 rupees.",
    trap=B("Watch out for 19. That is 95 divided by 5, as if the biscuits were free.", W("t", "95 ÷ 5 = 19")),
    check="Check: 5 cups at 13 rupees is 65, and 65 plus 30 is 95.",
    summ="Work out the part you know, take it off the total, then divide what is left.")

# 12x − 35 = 109
add("62c00bfa", "x", 12, "−", 35, 109,
    given="x cups at ₹12 − ₹35 costs = ₹109 profit",
    intro="Ravi sells x cups of chai at 12 rupees each. After paying 35 rupees for milk and sugar, he has 109 rupees profit. "
          "How many cups did he sell?",
    eq_q="Profit is the money that comes in, minus the costs. Which equation fits?",
    wrongs=["12x + 35 = 109", "12x = 109 − 35"],
    eq_if="x cups at 12 rupees bring in 12 x. The 35 for milk and sugar is paid out of that, so we subtract it, and 109 is left.",
    build="12 x comes in, 35 goes out, and 109 is the profit.",
    marks=[N("e1", "12x", "money in"), N("e1", "35", "costs")],
    tail=" Ravi sold 12 cups.",
    trap=B("See why we added? Ravi took in more than his profit. The 35 he spent has to go back on."),
    check="Check: 12 cups at 12 rupees is 144. Take away the 35 he spent, and 109 is left.",
    summ="Profit plus costs gives the money taken. Then divide by the price of one cup.")

# 5x + 9 = 54
add("694737de", "x", 5, "+", 9, 54,
    given="5 equal boxes + 9 extra = 54 bags",
    intro="Meera has 54 bags of rangoli powder. She packs 5 boxes with the same number in each, and 9 bags are left over. "
          "How many are in one box? Call it x.",
    eq_q="Which equation counts all 54 bags?",
    wrongs=["5x − 9 = 54", "5x = 54"],
    eq_if="The 54 bags are in two places: 5 boxes of x, and 9 loose ones. So it is 5 x plus 9.",
    build="5 x in the boxes, plus the 9 extra, makes 54.",
    asks="div",
    tail=" Each box holds 9 bags.",
    check="Check: 5 boxes of 9 is 45, and 45 plus the 9 extra is 54.",
    summ="Leftovers come off first, then divide by the number of boxes.")

# 4n + 7 = 35
add("6ad87304", "n", 4, "+", 7, 35,
    given="4 rows of n lamps + 7 border lamps = 35",
    intro="Kavita uses 35 lamps: 4 rows with n lamps in each, and 7 extra lamps round the border. Let's find n.",
    eq_q="Which equation shows the lamps?",
    wrongs=["4 + n + 7 = 35", "4n − 7 = 35"],
    eq_if="4 rows of n lamps means 4 times n. The 7 border lamps are extra, so they are added on to make 35.",
    build="4 n in the rows, plus 7 on the border, equals 35.",
    marks=[N("e1", "4n", "rows"), N("e1", "7", "border")],
    tail=" There are 7 lamps in each row.",
    trap=B("Don't mix up the two 7s. One is the border lamps we were told about. The other is n, which we worked out."),
    check="Check: 4 rows of 7 is 28, and 28 plus 7 border lamps is 35.",
    summ="Take off the border lamps first, then share the rest among the rows.")

# 23 + 7x = 72
add("6ed91733", "x", 7, "+", 23, 72, const_first=True,
    given="₹23 saved + ₹7 each week = ₹72",
    intro="Arjun has 23 rupees saved, and earns 7 rupees every week. Now he has exactly 72 rupees. "
          "How many weeks has he worked? Call it x.",
    eq_q="Which equation fits his savings?",
    wrongs=["23x + 7 = 72", "7x = 72"],
    eq_if="The 23 rupees is there once, at the start. The 7 rupees comes every week, so after x weeks that is 7 x.",
    build="23 to begin with, plus 7 x earned, equals 72.",
    asks="div",
    tail=" Arjun worked for 7 weeks.",
    check="Check: 7 weeks at 7 rupees is 49, and 23 plus 49 is 72.",
    summ="Take off what he had at the start. The rest was earned, so divide by what he earns each week.")

# 7p + 15 = 57
add("7b97b226", "p", 7, "+", 15, 57,
    given="p packets at ₹7 + ₹15 rangoli colours = ₹57",
    intro="Riya spends 57 rupees: on p packets of diyas at 7 rupees each, and a 15 rupee box of rangoli colours. "
          "How many packets is p?",
    eq_q="Which equation fits her shopping?",
    wrongs=["7p − 15 = 57", "7 + p + 15 = 57"],
    eq_if="p packets at 7 rupees each cost 7 times p. The colours cost 15 more, and the two together come to 57.",
    build="7 p for the diyas, plus 15 for the colours, equals 57.",
    tail=" Riya bought 6 packets.",
    trap=B("Don't stop at 42. That is the money spent on diyas, not the number of packets."),
    check="Check: 6 packets at 7 rupees is 42, and 42 plus 15 is 57.",
    summ="Total, minus the one-off cost, divided by the price of one.")

# 5x + 15 = 100
add("7c64e0a7", "x", 5, "+", 15, 100,
    given="5 plates at ₹x + ₹15 drink = ₹100, nothing left",
    intro="Rohan has 100 rupees. He buys 5 plates of chaat at x rupees each and a 15 rupee cold drink, and has nothing left. "
          "What does one plate cost?",
    eq_q="He spent everything. Which equation says so?",
    wrongs=["5x − 15 = 100", "5x = 100"],
    eq_if="Nothing was left, so the chaat and the drink together used up all 100 rupees. The chaat is 5 x, and the drink adds 15.",
    build="5 x for the chaat, plus 15 for the drink, equals the whole 100.",
    asks="div",
    tail=" Each plate of chaat costs 17 rupees.",
    trap=B("Two slips to dodge. 100 divided by 5 is 20, which forgets the drink. And adding the 15 instead of taking it away gives 23.",
           W("t1", "100 ÷ 5 = 20"), W("t2", "(100 + 15) ÷ 5 = 23")),
    check="Check: 5 plates at 17 rupees is 85, and 85 plus 15 is 100. Every rupee is used.",
    summ="Money spent on something else comes off first. Then share the rest among the plates.")

# 9x + 12 = 75
add("81c833be", "x", 9, "+", 12, 75,
    given="boxes at ₹9 each + ₹12 gift bag = ₹75",
    intro="Priya spends 75 rupees on boxes of ladoos at 9 rupees each, and a 12 rupee gift bag. "
          "How many boxes did she buy? Let's call it x.",
    eq_q="Which equation fits?",
    wrongs=["9x = 75 + 12", "x + 12 = 75"],
    eq_if="x boxes at 9 rupees each cost 9 x. The bag is part of the 75 too, so the 12 is added on the same side.",
    build="9 x for the ladoos, plus 12 for the bag, equals 75.",
    marks=[N("e1", "9x", "ladoos"), N("e1", "12", "bag")],
    tail=" Priya bought 7 boxes.",
    check="Check: 7 boxes at 9 rupees is 63, and 63 plus 12 for the bag is 75.",
    summ="Take the bag off the bill, then divide by the price of a box.")
