"""Imported batch 07, part d: marbles, lemonade profit, friendship bands, spend then split, the jersey refund, ring toss."""
from imported_07_a import three
from imported_07_lib import ANS, B, DIV, E, G, GIVEN, M, N, W, choose, lesson, pick, tail

P = "AIGEN_grade5_"
LESSONS = {}

# ── Marbles: (3x + 5) + (2x + 7) = 62, then Arjun's 3x + 5 ───────────────────
qid = P + "ea4cc0a8-dcbb-4dc1-b0e2-45dbff6d51de"
vv = ("x", 10)
LESSONS[qid] = lesson(
    B("Arjun has 3 x plus 5 marbles, and Kavya has 2 x plus 7. Together they have 62. We want to know how many marbles Arjun has.",
      E("q", "(3x + 5) + (2x + 7) = 62", *vv, tone="given")),
    B("Gather the like terms. 3 x and 2 x make 5 x. And 5 and 7 make 12.",
      G("q", ["3x", "2x"], "5x"), G("q", ["+ 5", "+ 7"], "12"), E("e2", "5x + 12 = 62", *vv)),
    tail(qid, "x", 5, 12, 62, "e2", vv=vv, final=False),
    B("We have found x. What is the next move?",
      ask=choose(["tick 10, we are done", "put 10 into 3x + 5", "put 10 into 2x + 7"], 1,
                 "The question asks for Arjun's marbles, and Arjun has 3 x plus 5. So we put 10 in place of x there.")),
    B("3 times 10 is 30, and 30 plus 5 is 35. Arjun has 35 marbles.",
      M("q", "(3x + 5)"), W("a0", "3 × 10 = 30"), ANS("a", "30 + 5 = 35"), M("a", "35", "circle")),
    B("Check with Kavya. She has 2 times 10, plus 7, which is 27. And 35 plus 27 is 62. It works.",
      W("c1", "2 × 10 + 7 = 27"), W("c2", "35 + 27 = 62")),
    B("Careful with the traps: 10 is only x, and 27 is Kavya's. Solve for x, then put it into the expression the question asks about."),
)

# ── Lemonade profit: 3x − 17 = 28 ────────────────────────────────────────────
qid = P + "ea8cf12b-ac77-449e-9454-7dc0c1893926"
LESSONS[qid] = lesson(
    B("Ananya spends 17 rupees on cups and ice, and sells lemonade at 3 rupees a glass. After taking off what she spent, her profit is 28 rupees. She sold x glasses, and we want x.",
      GIVEN("q", "₹3 a glass, spent ₹17, profit ₹28, x glasses", True)),
    B("x glasses bring in 3 x rupees. How do we get from that to her profit?",
      ask=choose(["3x + 17 = 28", "3x − 17 = 28", "17 − 3x = 28"], 1,
                 "Profit is the money that comes in, take away the money spent. 3 x comes in and 17 was spent, so 3 x minus 17 is the profit.")),
    B("Money in, minus money spent, equals profit. So 3 x minus 17 equals 28.",
      W("w", "money in − money spent = profit", label=True), W("e", "3x − 17 = 28")),
    tail(qid, "x", 3, 17, 28, "e", form="ax-b", found="Ananya sold 15 glasses."),
    B("Check. 15 glasses at 3 rupees is 45 rupees. Take away the 17 she spent, and the profit is 28. It works.",
      W("c", "15 × 3 − 17 = 28")),
    B("Careful not to take the 17 away a second time. When something has been taken off, undo it by adding it back. Then divide."),
    check=("x", 15))

# ── Friendship bands: 7 × 4x + 20 = 216 ──────────────────────────────────────
qid = P + "ec40c77b-03e0-4a71-af14-731fb1834b69"
LESSONS[qid] = lesson(
    B("Kabir sells friendship bands at 7 rupees each. He sells some in the morning and 3 times as many in the afternoon. With a bonus of 20 rupees, he earns 216 rupees. How many did he sell in the morning?",
      GIVEN("q", "₹7 a band. Afternoon = 3 times morning. Bonus ₹20. ₹216.", True)),
    B("Call the morning bands x. Then the afternoon is 3 x. How many bands is that in the whole day?",
      W("d", "morning x, afternoon 3x", label=True),
      ask=choose(["3x", "4x", "x + 3"], 1,
                 "Add the morning and the afternoon. 1 x and 3 x make 4 x. The morning bands count too.")),
    B("4 x bands in the day, at 7 rupees each. That is 7 times 4 x rupees. Add the bonus of 20, and we get 216.",
      W("d2", "x + 3x = 4x"), W("e", "7 × 4x + 20 = 216"), N("e", "7 × 4x", "bands"), N("e", "20", "bonus")),
    B("7 times 4 is 28, so the bands bring in 28 x rupees.",
      W("m", "7 × 4 = 28"), W("e2", "28x + 20 = 216")),
    tail(qid, "x", 28, 20, 216, "e2", found="Kabir sold 7 bands in the morning."),
    B("Check. 7 in the morning, and 3 times 7, which is 21, in the afternoon. That is 28 bands. At 7 rupees each they bring in 196, and the bonus makes 216.",
      W("c1", "3 × 7 = 21"), W("c2", "7 + 21 = 28"), W("c3", "28 × 7 + 20 = 216")),
    B("Careful: 28 is all the bands in the day, and the question asks only about the morning. Say clearly what your letter stands for, and you will know what your answer means."),
    check=("x", 7))


# ── Spend from the total, then split in 2: (255 − spend) ÷ 2 ─────────────────
def split(qid, brother, spend, on, intro):
    left = 255 - spend
    big = left - 15
    half = big // 2
    whole = half + 7
    money = "%d.50" % whole
    return lesson(
        B(intro, GIVEN("q", "Riya ₹x, %s ₹(2x + 15), total ₹255. Spend ₹%d." % (brother, spend), True)),
        B("Read the last part again. What is it that gets split equally?",
          ask=choose(["Riya's savings, x", "what is left of the 255 rupees", "%s's savings" % brother], 1,
                     "They spend from the total, and then split what remains. So it is the total, less what they spend, that gets shared.")),
        B("And the total is handed to us: 255 rupees. So first take off the %d they spend on %s. 255 minus %d is %d." % (spend, on, spend, left),
          M("q", "₹255"), W("s", "255 − %d = %d" % (spend, left))),
        B("%d rupees is left, to be split equally between Riya and %s. What do we do?" % (left, brother),
          ask=choose(["%d − 2" % left, "%d ÷ 3" % left, "%d ÷ 2" % left], 2,
                     "Splitting equally between 2 people means dividing by 2.")),
        B("%d is odd, so it will not halve into whole rupees. Split it into %d and 15. Half of %d is %d, and half of 15 is 7 and a half." % (left, big, big, half),
          W("h1", "%d ÷ 2 = %d" % (big, half)), W("h2", "15 ÷ 2 = 7.50")),
        B("%d and 7 and a half make %d and a half. So each of them gets %d rupees and 50 paise." % (half, whole, whole),
          ANS("a", "%d ÷ 2 = %s" % (left, money)), M("a", money, "circle"),
          W("r", "₹%s = %d rupees 50 paise" % (money, whole), label=True)),
        B("Check. 2 shares of %d rupees 50 paise make %d rupees. Add back the %d they spent, and we have the 255 they began with." % (whole, left, spend),
          W("c", "2 × %s + %d = 255" % (money, spend))),
        B(pick(qid, "x", [
            "And x? Solve x plus 2 x plus 15 equals 255 and you get x equal to 80. That is Riya's savings, and it is one of the choices. But the question never asked for it.",
            "What about x? If you solve x plus 2 x plus 15 equals 255, x comes to 80. That is only Riya's savings. It sits among the choices, but it is not what was asked."]),
          E("x1", "x + (2x + 15) = 255", "x", 80), E("x2", "x = 80", "x", 80)),
        B("So read what is being asked before you reach for the algebra. Here the total was already given: spend first, then share."),
    )


LESSONS[P + "f22f3fd3-e90c-44be-9b99-4c8b5576c49c"] = split(
    P + "f22f3fd3-e90c-44be-9b99-4c8b5576c49c", "Arjun", 40, "rangoli colours",
    "Riya has saved x rupees and Arjun has 2 x plus 15. Together that is 255 rupees. They spend 40 rupees on rangoli colours and split the rest equally. How much does each get?")

LESSONS[P + "f35e1ab1-083d-45d7-9487-60a203745e0c"] = split(
    P + "f35e1ab1-083d-45d7-9487-60a203745e0c", "Aarav", 80, "Diwali gifts",
    "Riya has saved x rupees and Aarav has 2 x plus 15. Their savings total 255 rupees. They spend 80 rupees on Diwali gifts and split what remains equally. How much does each person get?")

# ── The jersey refund: 3x = 2030 − 1670 ──────────────────────────────────────
qid = P + "fa604f35-5f46-48d6-abf0-e188df031369"
LESSONS[qid] = lesson(
    B("Coach Sharma buys jerseys, and a kit bag for 350 rupees. The bill is 2030 rupees. He returns 3 jerseys, and after the refund his spending is 1670 rupees. What does one jersey cost?",
      GIVEN("q", "Bill ₹2030. Returns 3 jerseys. Now ₹1670. Bag ₹350.", True)),
    B("We are not told how many jerseys he bought. But his spending dropped. What made it drop?",
      ask=choose(["the kit bag went back", "3 jerseys went back", "the price went down"], 1,
                 "Only the 3 jerseys went back to the shop. So the whole drop in spending is the price of exactly 3 jerseys.")),
    B("So how big is the drop? 2030 minus 1670 is 360 rupees. That is the refund.",
      W("r", "2030 − 1670 = 360"), M("r", "360")),
    B("Call the price of one jersey x. The refund is for 3 jerseys, so 3 x equals 360.",
      W("e", "3x = 360"), N("e", "3x", "3 jerseys"), N("e", "360", "refund")),
    B("3 x means 3 times x. What undoes times 3?",
      ask=choose(["subtract 3", "multiply by 3", "divide by 3"], 2,
                 "Times and divide are partners. To undo times 3, we divide both sides by 3.")),
    B("Divide both sides by 3. 360 divided by 3 is 120. Each jersey costs 120 rupees.",
      DIV("e", 3), ANS("a", "x = 120"), M("a", "x = 120", "circle")),
    B("Check with the first bill. Take off the bag: 2030 minus 350 is 1680. And 1680 is exactly 14 jerseys at 120 rupees. A whole number of jerseys, so it fits.",
      W("c1", "2030 − 350 = 1680"), W("c2", "14 × 120 = 1680")),
    B("Careful: the kit bag is a distraction here. The clue is the change. When a total changes, look at the difference and ask what caused it."),
    check=("x", 120))

LESSONS[P + "fc149ca4-5b38-4c2c-bd92-29876a65df6e"] = three(
    P + "fc149ca4-5b38-4c2c-bd92-29876a65df6e", "Priya", "Ankit", "Meera", "packs", "fewer", 3, 58, "boxes",
    "Priya and her cousins Ankit and Meera pack sweets into boxes. Together they pack exactly 58 boxes, and we want to know how many Meera packs.",
    "Priya + Ankit + Meera = 58 boxes")

# ── Ring toss: 3 + 4x = 31 ───────────────────────────────────────────────────
qid = P + "fca57786-d62e-42a9-b54f-f23f2905f79c"
LESSONS[qid] = lesson(
    B("At the school fair, the ring toss costs 3 rupees to enter, and then 4 rupees for each ring. Rohan spent 31 rupees. How many rings did he toss?",
      GIVEN("q", "₹3 to enter, ₹4 a ring, ₹31 spent", True)),
    B("Let x be the number of rings. Which number gets multiplied by x?",
      ask=choose(["the 3", "the 4", "the 31"], 1,
                 "The 4 rupees is paid again for every ring, so it is 4 times x. The 3 rupees is paid just once, to get in.")),
    B("3 to enter, plus 4 x for the rings, equals 31.",
      W("e", "3 + 4x = 31"), N("e", "3", "entry"), N("e", "4x", "rings")),
    tail(qid, "x", 4, 3, 31, "e", form="b+ax", asks=("div",), found="Rohan tossed 7 rings."),
    B("Check. 7 rings at 4 rupees is 28 rupees. Add the 3 to enter, and he spent 31. It works.",
      W("c", "3 + 4 × 7 = 31")),
    B("Once only, or every time? The every time number goes with the letter. The once only number comes off first."),
    check=("x", 7))
