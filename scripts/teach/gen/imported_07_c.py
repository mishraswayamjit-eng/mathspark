"""Imported batch 07, part c: discounts and coupons, change from a note, long sums of expressions, find x then use it."""
from imported_07_a import three
from imported_07_lib import ANS, B, E, G, GIVEN, M, N, W, choose, lesson, tail

P = "AIGEN_grade5_"
LESSONS = {}

# ── Powder, a discount and stencils: 8x − 18 + 32 = 174 ──────────────────────
qid = P + "d33534d9-6622-4779-affd-3cb76d3cf83e"
LESSONS[qid] = lesson(
    B("Priya and her friends buy 5 packets of red powder and 3 of blue, each costing x rupees. They get 18 rupees off, pay 32 rupees for stencils, and pay 174 rupees in all.",
      GIVEN("q", "5 + 3 packets at ₹x, ₹18 off, ₹32 stencils, paid ₹174", True)),
    B("5 packets and 3 packets make 8 packets, so the powder costs 8 x. The discount comes off, and the stencils go on.",
      W("n", "5 + 3 = 8"), W("e", "8x − 18 + 32 = 174"), N("e", "− 18", "discount"), N("e", "+ 32", "stencils")),
    B("Tidy the plain numbers first: minus 18, then plus 32. What do they make together?",
      ask=choose(["+ 14", "− 14", "+ 50"], 0,
                 "18 comes off and 32 goes on. More goes on than comes off, by 32 minus 18, which is 14. So together they add 14.")),
    B("So the equation is 8 x plus 14 equals 174. Careful with the signs: a discount is taken off, and a charge is added on.",
      G("e", ["− 18", "+ 32"], "+ 14"), W("e2", "8x + 14 = 174")),
    tail(qid, "x", 8, 14, 174, "e2", found="Each packet costs 20 rupees."),
    B("Check. 8 packets at 20 rupees is 160. Take off 18 and add 32, and we get 174. It works.",
      W("c", "8 × 20 − 18 + 32 = 174")),
    B("So: count the packets, put a minus on what comes off and a plus on what goes on, tidy the numbers, then solve."),
    check=("x", 20))

# ── Red and blue powder with glitter: 3x + 4x + 15 = 85 ──────────────────────
qid = P + "d418503e-9478-48c6-926e-57787bd56fa0"
LESSONS[qid] = lesson(
    B("Vikram buys 3 packets of red powder and 4 of blue, each costing x rupees. He pays 15 rupees for glitter, and the bill comes to 85 rupees.",
      GIVEN("q", "3 + 4 packets at ₹x each, ₹15 glitter, bill ₹85", True)),
    B("The red costs 3 x, the blue costs 4 x, and the glitter is 15. Together they make 85.",
      W("e", "3x + 4x + 15 = 85"), N("e", "3x", "red"), N("e", "4x", "blue"), N("e", "15", "glitter")),
    B("3 x and 4 x are like terms. What do they make together?",
      ask=choose(["12x", "7x", "7"], 1,
                 "3 packets and 4 packets make 7 packets, each costing x. So we add the 3 and the 4, and keep the x: 7 x.")),
    B("So 7 x plus 15 equals 85. Red and blue cost the same, so we can count all the packets together.",
      G("e", ["3x", "4x"], "7x"), W("e2", "7x + 15 = 85")),
    tail(qid, "x", 7, 15, 85, "e2", asks=("div",), found="Each packet costs 10 rupees."),
    B("Check. 7 packets at 10 rupees is 70 rupees, and 15 for the glitter makes 85. It works.",
      W("c", "7 × 10 + 15 = 85")),
    B("Like terms first, then the loose number, then divide. Three small steps."),
    check=("x", 10))

# ── Garlands, a stencil and a coupon: 15g + 22 − 7 = 120 ─────────────────────
qid = P + "d6b9df35-5210-472d-b5a1-043b8fdd5db2"
LESSONS[qid] = lesson(
    B("Deepa buys garlands at 15 rupees each and a kolam stencil for 22 rupees. A coupon takes 7 rupees off, and she pays 120 rupees. How many garlands did she buy?",
      GIVEN("q", "₹15 a garland, ₹22 stencil, ₹7 coupon, paid ₹120", True)),
    B("Let g be the number of garlands. The garlands cost 15 g, and the stencil adds 22. What does the coupon do to the bill?",
      ask=choose(["adds 7", "takes off 7", "changes nothing"], 1,
                 "A coupon is a discount. It makes the bill smaller, so the 7 rupees is taken off.")),
    B("So the equation is 15 g, plus 22, minus 7, equals 120.",
      W("e", "15g + 22 − 7 = 120"), N("e", "15g", "garlands"), N("e", "+ 22", "stencil"), N("e", "− 7", "coupon")),
    B("Tidy the plain numbers. 22 minus 7 is 15. So 15 g plus 15 equals 120.",
      G("e", ["+ 22", "− 7"], "+ 15"), W("e2", "15g + 15 = 120")),
    tail(qid, "g", 15, 15, 120, "e2", found="Deepa bought 7 garlands."),
    B("Check. 7 garlands at 15 rupees is 105 rupees. Add 22 and take off 7, and she pays 120. It works.",
      W("c", "7 × 15 + 22 − 7 = 120")),
    B("A coupon comes off, a purchase goes on. Get the signs right, tidy up, and the rest is two steps."),
    check=("g", 7))

# ── Gulal, balloons and a coupon: 7x + 35 − 20 = 120 ─────────────────────────
qid = P + "d884593d-612a-4e2e-b9ac-63db18bfd033"
LESSONS[qid] = lesson(
    B("Priya buys 7 packets of gulal and spends 35 rupees on water balloons. A coupon takes 20 rupees off, and she pays 120 rupees. What does one packet cost?",
      GIVEN("q", "7 packets, ₹35 balloons, ₹20 coupon, paid ₹120", True)),
    B("Call the price of a packet x. Then 7 packets cost 7 x. The balloons add 35, and the coupon takes off 20.",
      W("e", "7x + 35 − 20 = 120"), N("e", "7x", "gulal"), N("e", "+ 35", "balloons"), N("e", "− 20", "coupon")),
    B("Let's tidy the plain numbers. Plus 35 and minus 20: what do they make together?",
      ask=choose(["+ 55", "+ 15", "− 15"], 1,
                 "35 goes on and 20 comes off. 35 minus 20 leaves 15, and it is still added on.")),
    B("So 7 x plus 15 equals 120.",
      G("e", ["+ 35", "− 20"], "+ 15"), W("e2", "7x + 15 = 120")),
    tail(qid, "x", 7, 15, 120, "e2", asks=("div",), found="Each packet of gulal costs 15 rupees."),
    B("Check. 7 packets at 15 rupees is 105 rupees. Add 35 for the balloons, take off the coupon of 20, and she pays 120. It works.",
      W("c", "7 × 15 + 35 − 20 = 120")),
    B("Careful with a coupon: it is money off, so it goes in with a minus. Then tidy, clear and divide."),
    check=("x", 15))

# ── Sachets in packets: 4x + 9 = 53 ──────────────────────────────────────────
qid = P + "d8ce2dbb-ba75-4f8e-bebd-4d00ba50dd78"
LESSONS[qid] = lesson(
    B("Meera starts with 53 sachets. She fills 4 packets with the same number in each, and 9 sachets are left over. How many did she put in each packet?",
      GIVEN("q", "53 sachets, 4 equal packets, 9 left over", True)),
    B("Let x be the number of sachets in one packet. Which equation fits the story?",
      ask=choose(["4x + 9 = 53", "4x − 9 = 53", "4x = 53"], 0,
                 "The 53 is everything she started with. Some went into the 4 packets, and 9 were left. So the packets and the leftovers together make 53.")),
    B("4 packets of x, plus 9 left over, equals 53. Careful: sharing all 53 among 4 packets would not even come out whole. The leftovers must come off first.",
      W("e", "4x + 9 = 53"), N("e", "4x", "in packets"), N("e", "9", "left over")),
    tail(qid, "x", 4, 9, 53, "e", found="Each packet has 11 sachets."),
    B("Check. 4 packets of 11 is 44, and 9 left over makes 53. It works.",
      W("c", "4 × 11 + 9 = 53")),
    B("The total is the packets plus the leftovers. Take the leftovers off, then share among the packets."),
    check=("x", 11))

# ── Jerseys, a kit bag and change: 200x + 250 = 1850 ─────────────────────────
qid = P + "d9d91fe0-40c4-46c4-8d06-105ed62d59ff"
LESSONS[qid] = lesson(
    B("Coach Sharma buys jerseys at 200 rupees each and a kit bag for 250 rupees. He hands over 2000 rupees and gets 150 rupees back. How many jerseys did he buy?",
      GIVEN("q", "₹200 a jersey, ₹250 bag. Gave ₹2000, got ₹150 back.", True)),
    B("First things first. How much did the coach actually spend?",
      ask=choose(["2000 rupees", "2150 rupees", "1850 rupees"], 2,
                 "He handed over 2000 rupees, but 150 came back to him. So the shop kept 2000 minus 150, which is 1850 rupees.")),
    B("He spent 1850 rupees. Careful: 2000 is only what he handed over. It is not the bill.",
      W("s", "2000 − 150 = 1850"), M("s", "1850")),
    B("Now the equation. x jerseys at 200 rupees each cost 200 x. Add the bag at 250, and that is the 1850 he spent.",
      W("e", "200x + 250 = 1850"), N("e", "200x", "jerseys"), N("e", "250", "kit bag")),
    tail(qid, "x", 200, 250, 1850, "e", found="The coach bought 8 jerseys."),
    B("Check. 8 jerseys at 200 rupees is 1600. Add the bag and we get 1850. And 2000 minus 1850 is the 150 change. It all fits.",
      W("c1", "8 × 200 + 250 = 1850"), W("c2", "2000 − 1850 = 150")),
    B("So: find what was really spent, write the equation, then undo one thing at a time."),
    check=("x", 8))

# ── Four innings: 10x + 10 = 210, then the 4th innings ───────────────────────
qid = P + "dcc25204-3a07-443d-8b1d-a95d33cbde3d"
vv = ("x", 20)
LESSONS[qid] = lesson(
    B("Team India's 4 innings are 3 x plus 10, 2 x minus 5, x plus 20, and 4 x minus 15. The total is 210 runs. We want x, and then the runs in the 4th innings.",
      E("q", "(3x + 10) + (2x − 5) + (x + 20) + (4x − 15) = 210", *vv, tone="given")),
    B("That is a long line, so let's gather like terms. The x terms are 3 x, 2 x, x and 4 x.",
      M("q", "3x"), M("q", "2x"), M("q", ("x", 3)), M("q", "4x")),
    B("The x standing alone counts as 1 x. So 3 and 2 and 1 and 4 make 10, and that is 10 x.",
      G("q", ["3x", "2x", ("x", 3), "4x"], "10x")),
    B("Now the plain numbers: plus 10, minus 5, plus 20, minus 15. What do they come to?",
      ask=choose(["+ 50", "+ 10", "+ 20"], 1,
                 "The plus numbers are 10 and 20. The minus numbers are 5 and 15, and those are taken away. Work along the line and you land on 10.")),
    B("So the long line shrinks to 10 x plus 10 equals 210.",
      W("n", "10 − 5 + 20 − 15 = 10"), E("e2", "10x + 10 = 210", *vv)),
    tail(qid, "x", 10, 10, 210, "e2", vv=vv, asks=(), final=False),
    B("We have x. Are we finished?",
      ask=choose(["Yes, the answer is 20", "No, now work out 4x − 15"], 1,
                 "Read the question again. It asks for the runs in the 4th innings, and that is 4 x minus 15.")),
    B("Careful: 20 is only x. The 4th innings is 4 x minus 15.",
      M("q", "(4x − 15)", "box")),
    B("4 times 20 is 80, and 80 minus 15 is 65. The 4th innings was 65 runs.",
      W("a0", "4 × 20 = 80"), ANS("a", "80 − 15 = 65"), M("a", "65", "circle")),
    B("Check all 4 innings with x as 20. They are 70, 35, 40 and 65. Add them up and we get 210.",
      W("c1", "3 × 20 + 10 = 70"), W("c2", "2 × 20 − 5 = 35"), W("c3", "20 + 20 = 40"), W("c4", "70 + 35 + 40 + 65 = 210")),
    B("So: gather the x terms, gather the numbers, solve for x, and then put x back into the part the question asks for."),
)

# ── Five overs: 12n + 10 = 82, then the 4th over ─────────────────────────────
qid = P + "e14c9928-5051-4b07-b14c-d5a2d2b8b9ee"
LESSONS[qid] = lesson(
    B("Team India's 5 overs are 2 n plus 3, 3 n minus 1, n plus 7, 4 n minus 5, and 2 n plus 6. The total is 82 runs. We want n, and the runs in the 4th over.",
      GIVEN("q", "(2n + 3) + (3n − 1) + (n + 7) + (4n − 5) + (2n + 6) = 82")),
    B("That is a long line, so gather the n terms first: 2 n, 3 n, n, 4 n and 2 n.",
      M("q", "2n"), M("q", "3n"), M("q", ("n", 3)), M("q", "4n"), M("q", ("2n", 2))),
    B("The n standing alone counts as 1 n. So 2 and 3 and 1 and 4 and 2 make 12, and that is 12 n.",
      W("n1", "2n + 3n + n + 4n + 2n = 12n")),
    B("Now the plain numbers: plus 3, minus 1, plus 7, minus 5, plus 6. What do they come to?",
      ask=choose(["+ 22", "+ 10", "+ 12"], 1,
                 "Plus 3, plus 7 and plus 6 go on. Minus 1 and minus 5 come off. Work along the line and you land on 10.")),
    B("So the long line shrinks to 12 n plus 10 equals 82.",
      W("n2", "3 − 1 + 7 − 5 + 6 = 10"), W("e2", "12n + 10 = 82")),
    tail(qid, "n", 12, 10, 82, "e2", asks=(), final=False),
    B("We have n. But the question also asks for the 4th over. Which expression is that?",
      ask=choose(["3n − 1", "4n − 5", "2n + 6"], 1,
                 "Count along the overs: 1st, 2nd, 3rd, 4th. The 4th expression is 4 n minus 5.")),
    B("4 times 6 is 24, and 24 minus 5 is 19. So n is 6, and the 4th over brought 19 runs.",
      M("q", "(4n − 5)", "box"), W("a0", "4 × 6 = 24"), W("a1", "24 − 5 = 19"),
      ANS("a", "n = 6, 4th over = 19 runs", True), M("a", "n = 6, 4th over = 19 runs", "circle")),
    B("Check the 5 overs with n as 6. They are 15, 17, 13, 19 and 18. Add them up and we get 82.",
      W("c", "15 + 17 + 13 + 19 + 18 = 82")),
    B("Careful with the choices here: more than one has n as 6. Only working out 4 n minus 5 tells you which is right. So finish every part of the question."),
    check=("n", 6))

# ── Savings, then gloves: 35 + 3x = 110, spend 2x ────────────────────────────
qid = P + "e16975ee-46ba-4910-a911-3f758434be17"
vv = ("x", 25)
LESSONS[qid] = lesson(
    B("Ravi has 35 rupees saved and earns x rupees a week. After 3 weeks he has exactly 110 rupees. Then he spends 2 x rupees on gloves. How much is left?",
      GIVEN("q", "₹35 + 3 weeks at ₹x = ₹110.   Gloves cost ₹2x.", True)),
    B("The gloves cost 2 x, so we cannot know their price until we know x. Which equation will find x?",
      ask=choose(["35 + 3x = 110", "35x + 3 = 110", "3x = 110 + 35"], 0,
                 "He earns x rupees in each of 3 weeks, which is 3 x. Add the 35 he already had, and the total is 110.")),
    B("35 saved, plus 3 x earned, equals 110.",
      E("e", "35 + 3x = 110", *vv), N("e", "35", "saved"), N("e", "3x", "earned")),
    tail(qid, "x", 3, 35, 110, "e", form="b+ax", vv=vv, asks=(), final=False, found="Ravi earns 25 rupees a week."),
    B("Now the gloves. They cost 2 x, which is 2 times 25. That is 50 rupees.",
      W("g", "2 × 25 = 50")),
    B("So how do we find what Ravi has left?",
      ask=choose(["110 − 50", "75 − 50", "110 − 25"], 0,
                 "He had 110 rupees altogether before buying the gloves, and the gloves cost 50. So we take 50 from 110.")),
    B("110 minus 50 is 60. Ravi has 60 rupees left.",
      ANS("a", "110 − 50 = 60"), M("a", "60", "circle")),
    B("Careful with the numbers we met on the way. 25 is his weekly pay, and 50 is the price of the gloves. Neither is what the question asks. Check: 60 left, plus 50 spent, is 110.",
      W("c", "60 + 50 = 110")),
    B("So: find x first, use it to find the cost, and then take the cost from the total."),
)

# ── Rows of chairs: 8x + 5 = 53 ──────────────────────────────────────────────
qid = P + "e4de9a7a-ffdc-4e70-8a33-84eb3d4682ec"
LESSONS[qid] = lesson(
    B("Vikram sets up equal rows of 8 chairs, and puts 5 extra chairs at the front for the teachers. There are 53 chairs in all. How many rows did he set up?",
      GIVEN("q", "8 chairs in a row, 5 extra, 53 in all", True)),
    B("Let x be the number of rows. The rows hold 8 times x chairs. With the 5 chairs for the teachers, that makes 53.",
      W("e", "8x + 5 = 53"), N("e", "8x", "in rows"), N("e", "5", "teachers")),
    tail(qid, "x", 8, 5, 53, "e", asks=("clear", "div"), found="Vikram set up 6 rows."),
    B("Check. 6 rows of 8 is 48 chairs. Add the 5 at the front, and there are 53. It works.",
      W("c", "6 × 8 + 5 = 53")),
    B("The teachers' chairs are not in any row. So they come off first, and the rest are shared into rows of 8."),
    check=("x", 6))

# ── Water balloons in bags: 3x + 11 = 50 ─────────────────────────────────────
qid = P + "e7f0e32d-40af-4e18-8f88-59cafb7bf6c0"
LESSONS[qid] = lesson(
    B("Priya fills 3 bags with the same number of water balloons in each. She adds 11 balloons left over from last year, and has 50 ready for the party. How many are in each bag?",
      GIVEN("q", "3 equal bags + 11 old balloons = 50", True)),
    B("Let x be the number of balloons in one bag. Which equation fits?",
      ask=choose(["3 + 11x = 50", "3x = 50 + 11", "3x + 11 = 50"], 2,
                 "There are 3 bags with x in each, so 3 x. The 11 old balloons are added to those. Together they make 50.")),
    B("3 bags of x, plus the 11 from last year, equals 50.",
      W("e", "3x + 11 = 50"), N("e", "3x", "in bags"), N("e", "11", "last year")),
    tail(qid, "x", 3, 11, 50, "e", found="Each bag has 13 balloons."),
    B("Check. 3 bags of 13 is 39, and 11 more makes 50. It works.",
      W("c", "3 × 13 + 11 = 50")),
    B("Careful not to share out the 11 as well. Those balloons were never in a bag, so they come off before we divide by 3."),
    check=("x", 13))

LESSONS[P + "e9060e09-7551-4b39-ba22-d0f77e8130fb"] = three(
    P + "e9060e09-7551-4b39-ba22-d0f77e8130fb", "Meena", "Priya", "Kavya", "uses", "fewer", 4, 47, "packets",
    "Three sisters make rangoli designs: Meena, Priya and Kavya. Together they use exactly 47 packets of powder, and we want to know how many Kavya uses.",
    "Meena + Priya + Kavya = 47 packets")
