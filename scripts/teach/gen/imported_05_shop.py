"""Batch 05: shopping with decimals (several of one thing, a weight times a price, change).

Builders write the lessons for questions that tell the same story with different
numbers, computing every line; the rest are written one by one.
"""
from imported_05_lib import ANS, B, D, GIVEN, M, N, RING, W, ask, lesson, mon, num, rs

LESSONS = {}

P = "AIGEN_grade5_"


# ── Several at one price, one more thing, and change from a note ─────────────

def buy_change(qid, intro, given, n, price, one, things, extra, extra_name, note, closing):
    price, extra, note = D(price), D(extra), D(note)
    whole = int(price)
    frac = price - whole
    a, b = n * whole, n * frac
    cost = n * price
    bill = cost + extra
    chg = note - bill
    LESSONS[qid] = lesson(
        B(intro, GIVEN("q", given, True)),
        B("What does %s rupees pay for?" % mon(price),
          ask=ask("one %s" % one, ["all %d %s" % (n, things)],
                  "The word each is the clue. %s rupees is for one %s, and there are %d of them." % (mon(price), one, n))),
        B("So multiply, in two easy parts. %d times %d is %s, and %d times %s is %s." % (n, whole, mon(a), n, num(frac), num(b)),
          W("m1", "%d × %d = %s" % (n, whole, mon(a))), W("m2", "%d × %s = %s" % (n, num(frac), num(b)))),
        B("%s plus %s is %s rupees for the %s." % (mon(a), num(b), mon(cost), things),
          W("m3", "%d × %s = %s" % (n, rs(price), rs(cost)))),
        B("Add %s. %s plus %s is %s. That is the whole bill." % (extra_name, mon(cost), mon(extra), mon(bill)),
          W("t", "%s + %s = %s" % (rs(cost), rs(extra), rs(bill))), N("t", rs(bill), "the bill")),
        B("Now the change. Careful: take the whole bill from the note, not just one of the prices. %s minus %s is %s rupees." % (
            mon(note), mon(bill), mon(chg)),
          ANS("a", "%s − %s = %s" % (rs(note), rs(bill), rs(chg))), RING("a", rs(chg))),
        B("Check: the bill and the change together should make the note. %s plus %s is %s." % (mon(bill), mon(chg), mon(note)),
          W("c", "%s + %s = %s" % (rs(bill), rs(chg), rs(note)))),
        B(closing),
    )


buy_change(P + "665f4585-19ff-48d3-a792-908df02673a3",
           "Rina buys 3 notebooks at 12.65 rupees each, and a story book for 45.50. She pays with a 100 rupee note. How much change does she get?",
           "3 notebooks at ₹12.65 each, book ₹45.50, pays ₹100", 3, "12.65", "notebook", "notebooks",
           "45.50", "the story book", 100,
           "For a shopping bill: multiply for the things bought in a bunch, add the rest, and take the total from the note.")
buy_change(P + "6c1d02ae-5a24-446e-b75f-b213f17c4419",
           "A customer buys 3 boxes of bangles at 45.75 rupees a box, and a golden bangle for 28.50. The customer pays with a 200 rupee note. How much change must Meera return?",
           "3 boxes at ₹45.75 each, bangle ₹28.50, pays ₹200", 3, "45.75", "box", "boxes",
           "28.50", "the golden bangle", 200,
           "Three steps, in order: multiply for the boxes, add the single thing, subtract the bill from the note.")


LESSONS[P + "c0469b90-2d89-4fdc-aea0-946899187f2c"] = lesson(
    B("Priya buys 4 packets of sparklers at 12.75 rupees each, and a box of diyas for 8.50. How much does she spend altogether?",
      GIVEN("q", "4 packets at ₹12.75 each, and diyas ₹8.50", True)),
    B("What does 12.75 rupees pay for?",
      ask=ask("one packet of sparklers", ["all 4 packets"],
              "The word each is the clue. 12.75 is the price of one packet, and Priya buys 4 of them.")),
    B("So multiply, in two easy parts. 4 times 12 is 48, and 4 times 0.75 is 3.",
      W("m1", "4 × 12 = 48"), W("m2", "4 × 0.75 = 3")),
    B("48 plus 3 is 51 rupees for the sparklers.",
      W("m3", "4 × ₹12.75 = ₹51")),
    B("Careful: 51 is one of the choices, but the diyas are not in it yet.",
      N("m3", "₹51", "sparklers only")),
    B("51 plus 8.50 is 59.50 rupees in all.",
      ANS("a", "₹51 + ₹8.50 = ₹59.50"), RING("a", "₹59.50")),
    B("Check with round numbers. 4 packets at about 13 rupees is 52, and about 8 more makes 60. Our 59.50 is right beside it.",
      W("c1", "4 × 13 = 52"), W("c2", "52 + 8 = 60")),
    B("So when a story says each, multiply first. Then add on everything else that was bought."),
)

LESSONS[P + "214a159e-f463-42ca-820a-3cf3c3a4746f"] = lesson(
    B("Riya has 500 rupees. She buys 3 boxes of sparklers, 4 packets of diyas, and a bag to carry them. How much does she have left?",
      GIVEN("q", "₹500. 3 boxes at ₹45.75, 4 packets at ₹32.50", True), W("q2", "and a bag for ₹12.25. Left = ?", True)),
    B("Three kinds of spending. What is the plan?",
      ask=ask("cost each kind, add, take from 500", ["add the 3 prices, take from 500", "take only the bag from 500"],
              "The prices say each. So 45.75 is for one box, and 32.50 is for one packet. We must multiply by how many she buys before we add.")),
    B("Sparklers: 3 times 45 is 135, and 3 times 0.75 is 2.25. So 137.25 rupees.",
      W("s1", "3 × 45 = 135"), W("s2", "3 × 0.75 = 2.25"), W("s3", "3 × ₹45.75 = ₹137.25")),
    B("Diyas: 4 times 32 is 128, and 4 halves are 2 more. So 130 rupees.",
      W("d1", "4 × 32 = 128"), W("d2", "4 × ₹32.50 = ₹130")),
    B("Now add everything. 137.25 plus 130 is 267.25.",
      W("t1", "₹137.25 + ₹130 = ₹267.25")),
    B("Don't leave the bag behind. It is only one small thing, so it is easy to forget. 267.25 plus 12.25 is 279.50.",
      W("t2", "₹267.25 + ₹12.25 = ₹279.50"), N("t2", "₹279.50", "all she spent")),
    B("Riya had 500. 500 minus 279.50 is 220.50 rupees left.",
      ANS("a", "₹500 − ₹279.50 = ₹220.50"), RING("a", "₹220.50")),
    B("Check: what she spent and what she has left should make 500. 279.50 plus 220.50 is 500.",
      W("c", "₹279.50 + ₹220.50 = ₹500")),
    B("So: multiply for each kind, add up every single thing, and subtract once from the money she started with."),
)

LESSONS[P + "acf07f25-c7f2-4468-a96a-e9dc6f4eae76"] = lesson(
    B("Riya has 500 rupees. She buys 3 boxes of sparklers and 2 packets of rangoli powder, then shares what is left equally among 4 friends. How much does each friend get?",
      GIVEN("q", "₹500. 3 boxes at ₹48.75, 2 packets at ₹62.50", True), W("q2", "The rest is shared equally by 4 friends", True)),
    B("Sparklers: 3 times 48 is 144, and 3 times 0.75 is 2.25. So 146.25 rupees.",
      W("s1", "3 × 48 = 144"), W("s2", "3 × 0.75 = 2.25"), W("s3", "3 × ₹48.75 = ₹146.25")),
    B("Rangoli powder: 2 times 62.50 is 125 rupees.",
      W("r1", "2 × ₹62.50 = ₹125")),
    B("Spent altogether: 146.25 plus 125 is 271.25. So what is left is 500 minus 271.25, which is 228.75.",
      W("t1", "₹146.25 + ₹125 = ₹271.25"), W("t2", "₹500 − ₹271.25 = ₹228.75")),
    B("228.75 rupees for 4 friends. What is a quick way to divide by 4?",
      ask=ask("halve, then halve again", ["halve once", "take away 4"],
              "Sharing among 4 is the same as cutting in half, and then cutting each half in half. 2 times 2 is 4.")),
    B("Half of 228.75 is 114.375. And half of that is 57.1875.",
      W("h1", "228.75 ÷ 2 = 114.375"), W("h2", "114.375 ÷ 2 = 57.1875")),
    B("Money stops at paise, 2 places after the point. So we round 57.1875. The digit after the 8 is a 7, so the 8 rounds up to 9.",
      W("r", "57.1875 ≈ 57.19"), M("h2", "57.1875")),
    B("Each friend gets about 57.19 rupees.",
      ANS("a", "Each friend ≈ ₹57.19", True), RING("a", "₹57.19")),
    B("Check: 4 times 57.19 is 228.76. That is just 1 paisa more than 228.75, and that tiny gap is the rounding.",
      W("c", "4 × 57.19 = 228.76")),
    B("So: find what is left, share it, and when the answer is money, round it to 2 places at the very end."),
)

LESSONS[P + "b02cd211-6b05-4720-b2a7-42b930d76360"] = lesson(
    B("Priya buys 3 packets of diyas and a rangoli colour set. She gets a discount, and hands over a 200 rupee note. How much more does she still have to pay?",
      GIVEN("q", "3 packets at ₹45.75 each, colour set ₹128.60", True), W("q2", "Discount ₹12.35. She pays ₹200.", True)),
    B("Diyas: 3 times 45 is 135, and 3 times 0.75 is 2.25. That is 137.25 rupees.",
      W("d1", "3 × 45 = 135"), W("d2", "3 × 0.75 = 2.25"), W("d3", "3 × ₹45.75 = ₹137.25")),
    B("Add the colour set. 137.25 plus 128.60 is 265.85.",
      W("t", "₹137.25 + ₹128.60 = ₹265.85")),
    B("The shopkeeper gives a discount of 12.35. What does a discount do to the bill?",
      ask=ask("makes it smaller, so subtract", ["makes it bigger, so add"],
              "A discount is money taken off the price, a little gift from the shopkeeper. So the bill goes down, and we subtract.")),
    B("265.85 minus 12.35 is 253.50. That is the final bill.",
      W("f", "₹265.85 − ₹12.35 = ₹253.50"), N("f", "₹253.50", "final bill")),
    B("Now look closely. The bill is 253.50, but Priya handed over only 200. This time there is no change: she still owes money."),
    B("253.50 minus 200 is 53.50 rupees more to pay.",
      ANS("a", "₹253.50 − ₹200 = ₹53.50"), RING("a", "₹53.50")),
    B("Check: the 200 she paid, plus 53.50 more, is 253.50, the final bill.",
      W("c", "₹200 + ₹53.50 = ₹253.50")),
    B("Careful: we usually take the bill from the note. Here the bill is bigger, so we take the note from the bill. Always look at which number is larger."),
)


# ── A weight with a half in it, times a price, and change ────────────────────

SPLIT = [
    "First the cost. %s kilograms is %d whole kilograms and half a kilogram more. So we can split the multiplying into two easy parts.",
    "We need the cost before the change. Think of %s kilograms as %d whole kilograms, and then half a kilogram. Two easy parts.",
    "Cost first, change second. %s kilograms means %d whole kilograms and one half kilogram. Let's cost the two parts one at a time.",
]


def kg_one(qid, v, fruit, w, price, note, intro, closing):
    w, price, note = D(w), D(price), D(note)
    whole = int(w)
    assert w - whole == D("0.5")
    a = whole * price
    h = price / 2
    cost = a + h
    chg = note - cost
    LESSONS[qid] = lesson(
        B(intro, GIVEN("q", "%s kg at %s per kg. Pays %s." % (num(w), rs(price), rs(note)), True)),
        B(SPLIT[v] % (num(w), whole),
          W("sp", "%s = %d + 0.5" % (num(w), whole))),
        B("The %d whole kilograms: %d times %s is %s." % (whole, whole, mon(price), mon(a)),
          W("m1", "%d × %s = %s" % (whole, rs(price), rs(a)))),
        B("Now the half kilogram. What does it cost?",
          ask=ask("half of the price of 1 kilogram", ["the price of 1 kilogram, plus 0.5", "5 times the price of 1 kilogram"],
                  "0.5 means one half. So half a kilogram costs half of what a whole kilogram costs.")),
        B("Half of %s is %s." % (mon(price), mon(h)),
          W("m2", "0.5 × %s = %s" % (rs(price), rs(h)))),
        B("Add the two parts. %s plus %s is %s. That is the cost of the %s." % (mon(a), mon(h), mon(cost), fruit),
          W("m3", "%s + %s = %s" % (rs(a), rs(h), rs(cost))), N("m3", rs(cost), "the bill")),
        B("Careful: %s is the bill, not the change. Take it from the %s rupee note. %s minus %s is %s rupees." % (
            mon(cost), mon(note), mon(note), mon(cost), mon(chg)),
          ANS("a", "%s − %s = %s" % (rs(note), rs(cost), rs(chg))), RING("a", rs(chg))),
        B("Check: the bill and the change should make the note again. %s plus %s is %s." % (mon(cost), mon(chg), mon(note)),
          W("c", "%s + %s = %s" % (rs(cost), rs(chg), rs(note)))),
        B(closing),
    )


kg_one(P + "8e5f5cd3-f95a-439d-90e1-395dd1f82cc2", 0, "mangoes", "3.5", "48.60", 200,
       "Ravi buys 3.5 kilograms of mangoes at 48.60 rupees a kilogram, and pays with a 200 rupee note. How much change should he get?",
       "So when a weight has a decimal, split it into whole kilograms and the bit left over. Cost each part, add, and then find the change.")
kg_one(P + "a8e8a44e-4ac3-4998-a958-00b714d76500", 1, "mangoes", "2.5", "84.60", 500,
       "Ravi buys 2.5 kilograms of mangoes. Each kilogram costs 84.60 rupees, and he pays with a 500 rupee note. What change does he receive?",
       "A decimal weight is just whole kilograms plus a part of one. Multiply each piece by the price, add them, and subtract from the note.")
kg_one(P + "aad20ffd-0e63-400e-9836-72d773fd8af6", 2, "mangoes", "3.5", "64.50", 500,
       "Mangoes cost 64.50 rupees a kilogram. Ravi buys 3.5 kilograms and pays with a 500 rupee note. How much change does he receive?",
       "Remember the two stops on the way: the whole kilograms, then the half. Only after both are added do we subtract from the note.")


# ── Two weights times two prices, and change ─────────────────────────────────

def kg_two(qid, intro, item1, w1, p1, item2, p2, note, closing):
    w1, p1, p2, note = D(w1), D(p1), D(p2), D(note)
    whole = int(w1)
    assert w1 - whole == D("0.5")
    a, h = whole * p1, p1 / 2
    c1 = a + h
    h2, q2 = p2 / 2, p2 / 4
    c2 = p2 + h2 + q2
    assert c2 == D("1.75") * p2
    bill = c1 + c2
    chg = note - bill
    LESSONS[qid] = lesson(
        B(intro,
          GIVEN("q", "%s kg at %s per kg, 1.75 kg at %s per kg" % (num(w1), rs(p1), rs(p2)), True),
          W("q2", "Pays with %s. Change = ?" % rs(note), True)),
        B("Two things to cost, and then the change. Start with the %s. %s kilograms is %d whole kilograms and a half." % (item1, num(w1), whole),
          W("sp", "%s = %d + 0.5" % (num(w1), whole))),
        B("%d times %s is %s, and half of %s is %s." % (whole, mon(p1), mon(a), mon(p1), mon(h)),
          W("a1", "%d × %s = %s" % (whole, rs(p1), rs(a))), W("a2", "0.5 × %s = %s" % (rs(p1), rs(h)))),
        B("%s plus %s makes %s rupees for the %s." % (mon(a), mon(h), mon(c1), item1),
          W("a3", "%s + %s = %s" % (rs(a), rs(h), rs(c1))), N("a3", rs(c1), item1)),
        B("Now the %s: 1.75 kilograms. How can we split 1.75 into friendly pieces?" % item2,
          W("sp2", "1.75 = 1 + 0.75"),
          ask=ask("1 + 0.5 + 0.25", ["1 + 0.7 + 0.5", "1 + 7 + 5"],
                  "0.75 is three quarters, and three quarters is a half and a quarter. So 1.75 is 1 whole, plus 0.5, plus 0.25.")),
        B("1 kilogram costs %s. Half of that is %s. And a quarter is half of the half: %s." % (mon(p2), mon(h2), mon(q2)),
          W("b1", "0.5 × %s = %s" % (rs(p2), rs(h2))), W("b2", "0.25 × %s = %s" % (rs(p2), rs(q2)))),
        B("Add the three pieces. %s plus %s plus %s is %s rupees for the %s." % (mon(p2), mon(h2), mon(q2), mon(c2), item2),
          W("b3", "%s + %s + %s = %s" % (rs(p2), rs(h2), rs(q2), rs(c2))), N("b3", rs(c2), item2)),
        B("Now the whole bill. %s plus %s is %s." % (mon(c1), mon(c2), mon(bill)),
          W("t", "%s + %s = %s" % (rs(c1), rs(c2), rs(bill)))),
        B("We are not finished: the question asks for the change. %s minus %s is %s rupees." % (mon(note), mon(bill), mon(chg)),
          ANS("ans", "%s − %s = %s" % (rs(note), rs(bill), rs(chg))), RING("ans", rs(chg))),
        B("Check: the bill and the change should make the note again. %s plus %s is %s." % (mon(bill), mon(chg), mon(note)),
          W("c", "%s + %s = %s" % (rs(bill), rs(chg), rs(note)))),
        B(closing),
    )


kg_two(P + "38ad1bf1-f165-4478-b52b-3867840e7e5c",
       "Ravi buys 3.5 kilograms of rice at 48.60 rupees a kilogram, and 1.75 kilograms of dal at 96.40 a kilogram. He pays with a 500 rupee note. What is his change?",
       "rice", "3.5", "48.60", "dal", "96.40", 500,
       "Break each awkward weight into wholes, halves and quarters. Cost the pieces, add for the bill, and take the bill from the note.")
kg_two(P + "6b82de24-6629-424a-8690-a5a60c96bc7a",
       "Riya buys 2.5 kilograms of almonds at 864 rupees a kilogram, and 1.75 kilograms of cashews at 1120 a kilogram. She pays with 5000 rupees. What is her change?",
       "almonds", "2.5", "864", "cashews", "1120", 5000,
       "Big prices, but the same small idea: wholes, halves and quarters. Cost each piece, add for the bill, then subtract from the money paid.")
kg_two(P + "b3e45ca3-0aa0-45f6-9cbc-7d47aadd3402",
       "Ravi buys 2.5 kilograms of apples at 120.50 rupees a kilogram, and 1.75 kilograms of oranges at 80.40 a kilogram. He pays with a 500 rupee note. What is his change?",
       "apples", "2.5", "120.50", "oranges", "80.40", 500,
       "Halves and quarters turn a hard multiplication into a few easy ones. Keep each piece on the board, add them up, and then find the change.")


# ── A discount that depends on the weight ────────────────────────────────────

LESSONS[P + "a9f9046f-1fd4-4cc0-9407-80128e5e023f"] = lesson(
    B("Ananya buys 3.75 kilograms of kaju katli and 2.5 kilograms of gulab jamun. The shopkeeper takes off 0.50 rupees for every 100 grams she buys. What does she pay?",
      GIVEN("q", "3.75 kg at ₹480 per kg, 2.5 kg at ₹260 per kg", True), W("q2", "Discount: ₹0.50 for every 100 g", True)),
    B("First the price with no discount. Kaju katli: 3.75 is 3 and three quarters. 3 times 480 is 1440, and three quarters of 480 is 360.",
      W("k1", "3 × 480 = 1440"), W("k2", "0.75 × 480 = 360")),
    B("1440 plus 360 is 1800 rupees.",
      W("k3", "3.75 × ₹480 = ₹1800")),
    B("Gulab jamun: 2 times 260 is 520, and half of 260 is 130. That makes 650 rupees.",
      W("g1", "2 × 260 = 520"), W("g2", "520 + 130 = 650"), W("g3", "2.5 × ₹260 = ₹650")),
    B("Before the discount, the bill is 1800 plus 650, which is 2450 rupees.",
      W("t", "₹1800 + ₹650 = ₹2450")),
    B("Now the discount. It depends on the weight, so add the weights: 3.75 plus 2.5 is 6.25 kilograms of sweets.",
      W("w", "3.75 + 2.5 = 6.25")),
    B("The discount is 0.50 rupees for every 100 grams. How many lots of 100 grams are there in 1 kilogram?",
      ask=ask("10", ["100", "1000"],
              "1 kilogram is 1000 grams, and 1000 is 10 hundreds. So each kilogram holds 10 lots of 100 grams.")),
    B("10 lots of 0.50 is 5. So the discount is 5 rupees for every kilogram.",
      W("d1", "10 × ₹0.50 = ₹5")),
    B("6.25 kilograms, with 5 rupees off each: 6.25 times 5 is 31.25 rupees off.",
      W("d2", "6.25 × 5 = 31.25"), N("d2", "31.25", "discount")),
    B("2450 minus 31.25 is 2418.75 rupees. That is what Ananya pays.",
      ANS("a", "₹2450 − ₹31.25 = ₹2418.75"), RING("a", "₹2418.75")),
    B("Check the discount another way. 6.25 kilograms is 62.5 lots of 100 grams, and 62.5 times 0.50 is 31.25 again.",
      W("c", "62.5 × 0.50 = 31.25")),
    B("Careful: the discount is not 0.50 just once. It is 0.50 for every 100 grams, so it grows with the weight. Price first, discount second, then subtract."),
)


# ── Three shops, three ways of pricing ───────────────────────────────────────

LESSONS[P + "f1393612-5bbb-4810-bb1e-94631c7172f6"] = lesson(
    B("Three shops sell fairy lights, each with its own kind of price. We need exactly 25 metres. Which shop is cheapest, and what do we pay there?",
      GIVEN("q", "25 metres needed. Cheapest shop = ?", True),
      W("pa", "Shop A: ₹12.75 per metre", True), W("pb", "Shop B: ₹1350 per 100 metres", True),
      W("pc", "Shop C: 10 m for ₹140, then ₹15.50 a metre", True)),
    B("The prices are told in three different ways, so we cannot compare them yet. We work out what 25 metres costs at each shop."),
    B("Shop A: 25 times 12.75. 25 times 12 is 300, and 25 times 0.75 is 18.75. So 318.75 rupees.",
      W("a1", "25 × 12 = 300"), W("a2", "25 × 0.75 = 18.75"), W("a3", "25 × ₹12.75 = ₹318.75"), N("a3", "₹318.75", "Shop A")),
    B("Shop B charges 1350 rupees for 100 metres. What is a quick way to get the price of 25 metres?",
      ask=ask("a quarter of 1350", ["1350 × 25", "1350 − 25"],
              "25 metres is a quarter of 100 metres. So it costs a quarter of the price of 100 metres.")),
    B("Half of 1350 is 675, and half of 675 is 337.50. So Shop B costs 337.50 rupees.",
      W("b1", "1350 ÷ 2 = 675"), W("b2", "₹1350 ÷ 4 = ₹337.50"), N("b2", "₹337.50", "Shop B")),
    B("Shop C: the first 10 metres cost 140 rupees. That leaves 15 metres to buy at 15.50 each.",
      W("c1", "25 − 10 = 15")),
    B("15 times 15 is 225, and 15 halves are 7.50 more. That is 232.50 for the extra metres.",
      W("c2", "15 × 15 = 225"), W("c2b", "15 × 0.50 = 7.50"), W("c3", "15 × ₹15.50 = ₹232.50")),
    B("With the 140 for the first 10 metres, Shop C costs 372.50 rupees.",
      W("c4", "₹140 + ₹232.50 = ₹372.50"), N("c4", "₹372.50", "Shop C")),
    B("Now we can compare: 318.75, 337.50 and 372.50. The smallest is Shop A, at 318.75 rupees.",
      W("cmp", "318.75 < 337.50 < 372.50"), ANS("ans", "Cheapest: Shop A, ₹318.75", True), RING("ans", "₹318.75")),
    B("Check A against B another way. 100 metres at Shop A would cost 1275 rupees, which is less than Shop B's 1350. So A really does beat B.",
      W("k1", "100 × 12.75 = 1275"), W("k2", "1275 < 1350")),
    B("Careful with Shop C: its 15.50 price is only for the metres after the first 10. When prices come in different forms, turn each into the cost of exactly what you need."),
)
