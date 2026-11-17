"""Batch 13: money stories with two percents, and the one-off percent stories."""
from imported_13_lib import ANS, B, D, GIVEN, M, N, P, RING, W, ask, lesson, mon, paise_words, pick, rs
from imported_13_money import pct

LESSONS = {}


# ── A percent, then a percent of what is left ────────────────────────────────

def two_pct(qid, who, intro, given, S, p1, t1, n1, p2, goes2, t2, n2, after1, o3=None, for1=None,
            tail=None, closing=None):
    S = D(S)
    s = mon(S)
    work1, a = pct(qid, p1, S, "p", "", n1)
    R = S - a
    av, r = mon(a), mon(R)
    work2, b = pct(qid, p2, R, "x", "", n2)
    L = R - b
    bv, lv = mon(b), mon(L)
    for1 = for1 or ("for " + t1)
    beats = [
        B(intro, GIVEN("q", given, True)),
        B("We take the story one step at a time, in order. First, %s: %d percent of %s." % (t1, p1, s)),
    ] + work1 + [
        B("%s minus %s is %s. That is the money left %s." % (s, av, r, after1),
          W("r", "%s − %s = %s" % (s, av, r)), N("r", "= " + r, "money left")),
        B("Next, %d percent %s. %d percent of which amount?" % (p2, goes2, p2),
          ask=ask("%s, the money left" % r, ["%s, the money at the start" % s, o3 or ("%s, the cost of %s" % (av, t1))],
                  "Listen for the words about what is left. %s, only %s remains. So this percent is taken from %s, not from %s." % (
                      after1[0].upper() + after1[1:], r, r, s))),
        B("That is the trap here: taking both percents of %s. The second percent is of the %s that is left." % (s, r),
          M("r", "= " + r, "box")),
    ] + work2

    if tail is None:
        if L == L.to_integral_value():
            beats.append(B("So %s rupees go on %s. %s minus %s leaves %s with %s rupees." % (bv, t2, r, bv, who, lv),
                           ANS("a", "%s − %s = %s" % (r, bv, rs(L))), RING("a", rs(L))))
        else:
            beats.append(B("So %s rupees go on %s. %s minus %s leaves %s, which is %s." % (
                bv, t2, r, bv, lv, paise_words(L).replace(" rupees ", " rupees and ")),
                ANS("a", "%s − %s = %s" % (r, bv, rs(L))), RING("a", rs(L)),
                W("aw", "%s = %s" % (rs(L), paise_words(L)), True)))
        beats.append(B("Check: %s %s, %s for %s, and %s left. Add them, and we are back at %s." % (av, for1, bv, t2, lv, s),
                       W("c", "%s + %s + %s = %s" % (av, bv, lv, s))))
    else:
        beats.append(B("So %s rupees go on %s. %s minus %s is %s." % (bv, t2, r, bv, lv),
                       W("s2", "%s − %s = %s" % (r, bv, lv))))
        if tail[0] == "minus":
            _, amt, t3 = tail
            F = L - D(amt)
            beats.append(B("We are not done yet. Last come the %s rupees for %s: %s minus %s leaves %s with %s rupees." % (
                mon(amt), t3, lv, mon(amt), who, mon(F)),
                ANS("a", "%s − %s = %s" % (lv, mon(amt), rs(F))), RING("a", rs(F))))
            beats.append(B("Check: %s %s, %s for %s, %s for %s, and %s left. Together they make %s." % (
                av, for1, bv, t2, mon(amt), t3, mon(F), s),
                W("c", "%s + %s + %s + %s = %s" % (av, bv, mon(amt), mon(F), s))))
        else:
            _, n, whom, each = tail
            F = L / n
            beats.append(B("We are not done yet. The %s rupees are shared equally among %d %s. %s divided by %d is %s rupees for %s." % (
                lv, n, whom, lv, n, mon(F), each),
                ANS("a", "%s ÷ %d = %s" % (lv, n, rs(F))), RING("a", rs(F))))
            beats.append(B("Check: %s %s, %s for %s, and %d gifts of %s. Together they make %s." % (
                av, for1, bv, t2, n, mon(F), s),
                W("c", "%s + %s + %d × %s = %s" % (av, bv, n, mon(F), s))))
    beats.append(B(closing or pick(qid, "close", [
        "So when a second percent is of the remaining money, find what remains first. Each percent is taken from the money that is there at that moment.",
        "With two percents, always ask, percent of what? The first was of all the money. The second was only of what was left.",
    ])))
    return lesson(*beats)


LESSONS[P + "53d85183-e50f-4999-97ab-5d8a145faf89"] = two_pct(
    P + "53d85183", "Kavya",
    "Kavya is given 1,200 rupees. She spends 25 percent on clothes, then 40 percent of the remaining money on sweets and snacks. The rest goes in her piggy bank. How much is that?",
    "₹1,200. 25% on clothes, then 40% of the rest.", 1200, 25, "the clothes", "clothes",
    40, "of the remaining money goes on sweets and snacks", "the sweets and snacks", "sweets, snacks", "after the clothes",
    closing="With two percents, always ask, percent of what? The first was of all 1,200. The second was only of what was left.")

LESSONS[P + "a3d81fb0-9a0f-45f8-bacf-5527a3cd1924"] = two_pct(
    P + "a3d81fb0", "Meera",
    "Meera goes to a Diwali mela with 500 rupees. She spends 30 percent on bangles, and then 25 percent of the remaining money on sweets. How much does she have left?",
    "₹500. 30% on bangles, then 25% of the rest.", 500, 30, "the bangles", "bangles",
    25, "of the remaining money goes on sweets", "the sweets", "sweets", "after the bangles")

LESSONS[P + "a58d41ac-0ce9-4c99-b2a2-0705016115e8"] = two_pct(
    P + "a58d41ac", "Meera",
    "Meera goes to a Diwali mela with 500 rupees. She spends 30 percent on bangles, and then 40 percent of the remaining money on sweets. How much does she have left?",
    "₹500. 30% on bangles, then 40% of the rest.", 500, 30, "the bangles", "bangles",
    40, "of the remaining money goes on sweets", "the sweets", "sweets", "after the bangles")

LESSONS[P + "acbc7ff9-1e4d-461d-9187-7702d7f3dce7"] = two_pct(
    P + "acbc7ff9", "Farhan",
    "Farhan earns 1,200 rupees at the chai stall. He saves 50 percent, and then spends 25 percent of the remaining amount on a cricket ball. How much is left after that?",
    "₹1,200. Saves 50%, then 25% of the rest.", 1200, 50, "the savings", "saved",
    25, "of the remaining amount goes on a cricket ball", "the cricket ball", "ball", "after saving",
    o3="25, because 25% is ₹25", for1="saved",
    closing="So when a percent is of the remaining amount, find what remains first. Here that was the 600 left after saving, not the whole 1,200.")

LESSONS[P + "706626a4-55e9-4e67-a0ed-7d037c983e2f"] = two_pct(
    P + "706626a4", "Amit",
    "Amit is given 2,000 rupees. He spends 20 percent on a cricket bat, then 25 percent of the remaining amount on cricket balls, and gives 150 rupees to charity. How much is left?",
    "₹2,000. 20% bat, 25% of the rest, ₹150 charity.", 2000, 20, "the bat", "bat",
    25, "of the remaining amount goes on cricket balls", "the balls", "balls", "after the bat",
    tail=("minus", 150, "charity"),
    closing="Three steps, in the order of the story. And each percent is taken from the money that is there at that moment, not always from the start.")

LESSONS[P + "e07781ec-a4d8-4f97-84ba-e99a697457c3"] = two_pct(
    P + "e07781ec", "Kavya",
    "Kavya is given 2,000 rupees. She saves 40 percent, spends 25 percent of the remaining amount on rangoli colours, and shares the rest equally on gifts for 3 friends. How much for each gift?",
    "₹2,000. Saves 40%. 25% of the rest. Then ÷ 3.", 2000, 40, "the savings", "saved",
    25, "of the remaining amount goes on rangoli colours", "the colours", "colours", "after saving",
    o3="800, the money saved", for1="saved", tail=("share", 3, "friends", "each friend's gift"),
    closing="A long story, but each step is small. Take the steps in order, and take each percent from the money that is there at that moment.")


# ── One-off stories ──────────────────────────────────────────────────────────

# Sparklers with a discount, paid from ₹500.
Q = P + "7d96407d-06d1-4f88-97a7-798b112ed5b9"
_w, _ = pct(Q, 10, 270, "p", "", "discount")
LESSONS[Q] = lesson(
    B("Meera has 500 rupees. She buys 6 boxes of sparklers at 45 rupees each, and gets 10 percent off the bill. How much money does she have left?",
      GIVEN("q", "₹500. 6 boxes at ₹45 each. 10% off the bill.", True)),
    B("First, the bill before any discount. 6 boxes at 45 rupees each: 6 times 45 is 270.",
      W("b", "6 × 45 = 270"), N("b", "= 270", "bill")),
    B("The shop takes 10 percent off. 10 percent of which amount?",
      ask=ask("270, the bill", ["500, Meera's money", "45, the price of a box"],
              "A discount comes off what you are asked to pay. The bill is 270, so the 10 percent is taken from 270.")),
    _w,
    B("A discount makes the bill smaller. 270 minus 27 is 243, and that is what Meera pays.",
      W("pay", "270 − 27 = 243"), N("pay", "= 243", "she pays")),
    B("Careful: 243 is what she pays, and it is one of the choices. But the question asks what she has left.",
      M("pay", "= 243", "box")),
    B("So take 243 from her 500. 500 minus 243 leaves Meera with 257 rupees.",
      ANS("a", "500 − 243 = ₹257"), RING("a", "₹257")),
    B("Check: the 243 she paid and the 257 she kept should make 500 again. And they do.",
      W("c", "243 + 257 = 500")),
    B("So: the full bill first, then take off the discount, then take what you pay from your money. Three small steps, in order."),
)

# Chai and samosas with a discount.
Q = P + "9e5ffbee-f49d-4a1d-a13e-dc3a6181980f"
_w, _ = pct(Q, 10, 360, "p", "", "discount")
LESSONS[Q] = lesson(
    B("Kavya's dad buys 8 cups of chai at 15 rupees each, and 12 samosas at 20 rupees each. He gets 10 percent off the total bill. How much does he pay?",
      GIVEN("q", "8 chai at ₹15. 12 samosas at ₹20. 10% off.", True)),
    B("Start with the chai. 8 cups at 15 rupees each: 8 times 15 is 120.",
      W("ch", "8 × 15 = 120"), N("ch", "= 120", "chai")),
    B("Now the samosas. 12 of them at 20 rupees each: 12 times 20 is 240.",
      W("sa", "12 × 20 = 240"), N("sa", "= 240", "samosas")),
    B("Add the two for the whole bill. 120 plus 240 is 360.",
      W("t", "120 + 240 = 360"), N("t", "= 360", "total bill")),
    B("Now the 10 percent discount. What do we do with it?",
      ask=ask("find 10% of 360, then subtract it", ["subtract 10 from 360", "find 10% of 360: that is the answer"],
              "10 percent is not 10 rupees. It is one tenth of the bill. And a discount is taken off, so we subtract it from the 360.")),
    _w,
    B("Take the discount off the bill. 360 minus 36 is 324, so Kavya's dad pays 324 rupees.",
      ANS("a", "360 − 36 = ₹324"), RING("a", "₹324")),
    B("Check: the 324 he pays and the 36 he saves should make the full bill of 360. And they do.",
      W("c", "324 + 36 = 360")),
    B("So with a discount on a whole bill: add up the bill first, find the percent of that total, and take it off."),
)

# Friendship bands, then a donation.
Q = P + "d4b9d3ae-0eee-4a23-a405-a782adfdd00c"
_w, _ = pct(Q, 20, 360, "p", "", "to charity")
LESSONS[Q] = lesson(
    B("Neha sells 24 friendship bands at 15 rupees each. She gives 20 percent of her earnings to charity. How much money does she have left?",
      GIVEN("q", "24 bands at ₹15 each. 20% to charity.", True)),
    B("First, what did she earn? That is 24 times 15. Split the 15 into 10 and 5, to make it easy.",
      W("e0", "24 × 15 = 24 × 10 + 24 × 5"), M("e0", "10"), M("e0", "5", nth=2)),
    B("24 times 10 is 240, and 24 times 5 is half of that, 120. Together, 360 rupees earned.",
      W("e", "240 + 120 = 360"), N("e", "= 360", "earned")),
    B("Now the charity gets 20 percent of the 360.", M("e", "= 360", "box")),
    _w,
    B("So 72 rupees go to charity. Is 72 our answer?",
      ask=ask("No: take 72 away from 360", ["Yes: 72 is the answer", "No: add 72 to 360"],
              "72 is the money Neha gives away. The question asks what she has left, so we take it from her 360.")),
    B("360 minus 72 is 288. Neha has 288 rupees left.",
      ANS("a", "360 − 72 = ₹288"), RING("a", "₹288")),
    B("Check: the 288 she keeps and the 72 she gives should make 360 again. And they do.",
      W("c", "288 + 72 = 360")),
    B("So: find the total, turn the percent into rupees, and then read the question once more. It asked for what is left, not what was given."),
)

# Bank, storybook, and a third for her brother.
Q = P + "805b7422-bbbe-473b-abe1-ce1e4247e16f"
_w, _ = pct(Q, 40, 1500, "p", "", "bank")
LESSONS[Q] = lesson(
    B("Neha has 1,500 rupees. She puts 40 percent in the bank. From the money at home she spends 180 rupees on a storybook, then gives one third of what is left to her brother. How much is at home now?",
      GIVEN("q", "₹1,500. 40% to bank. Home: − ₹180, then give 1/3.", True)),
    B("Take the story one step at a time. First the bank: 40 percent of 1,500."),
    _w,
    B("1,500 minus 600 is 900. That is the money Neha keeps at home, and the rest of the story is about this 900.",
      W("h", "1,500 − 600 = 900"), N("h", "= 900", "at home")),
    B("Then the storybook: 900 minus 180 is 720.",
      W("s", "900 − 180 = 720")),
    B("Her brother gets one third of what is left. To find one third, divide by 3: 720 divided by 3 is 240.",
      W("b", "1/3 of 720 = 720 ÷ 3 = 240"), N("b", "= 240", "brother")),
    B("So 240 rupees go to her brother. How much does Neha keep at home?",
      ask=ask("720 − 240", ["240", "900 − 240"],
              "240 is her brother's share. Neha keeps the rest of the 720, so we take the 240 away from 720.")),
    B("720 minus 240 is 480. Neha has 480 rupees at home.",
      ANS("a", "720 − 240 = ₹480"), RING("a", "₹480")),
    B("Check: 600 in the bank, 180 for the book, 240 for her brother, and 480 kept. Together they make 1,500.",
      W("c", "600 + 180 + 240 + 480 = 1,500")),
    B("A long story is just small steps in a row. Do them in order, and at the end check whose money the question is asking about."),
)

# Mark up by 40%, then 10% off.
Q = P + "efabbd25-0656-49d7-a223-3e6f5c9d7ec0"
_w1, _ = pct(Q, 40, 1500, "p", "", "added on")
_w2, _ = pct(Q, 10, 2100, "d", "", "discount")
LESSONS[Q] = lesson(
    B("A shopkeeper buys a bat for 1,500 rupees and marks its price 40 percent higher. In a sale he gives 10 percent off the marked price. What is the selling price?",
      GIVEN("q", "Cost ₹1,500. Marked 40% higher. Sale: 10% off.", True)),
    B("First, the marked price. It is 40 percent higher than the cost, so we need 40 percent of 1,500."),
    _w1,
    B("Higher means we add it on. 1,500 plus 600 is 2,100, and that is the price on the tag.",
      W("m", "1,500 + 600 = 2,100"), N("m", "= 2,100", "marked price")),
    B("Now the sale: 10 percent off. 10 percent of which price?",
      ask=ask("2,100, the marked price", ["1,500, the cost price", "600, the amount added on"],
              "A discount is taken off the price on the tag. The tag says 2,100, so we want 10 percent of 2,100.")),
    B("Here is the trap. 40 percent up and 10 percent down is not 30 percent up, because the two percents are of different amounts.",
      W("t", "Trap: 40% up then 10% off is not 30% up", True), M("m", "= 2,100", "box")),
    _w2,
    B("Off means we subtract. 2,100 minus 210 is 1,890, so the bat sells for 1,890 rupees.",
      ANS("a", "2,100 − 210 = ₹1,890"), RING("a", "₹1,890")),
    B("Check: put the discount back. 1,890 plus 210 is 2,100, the marked price.",
      W("c", "1,890 + 210 = 2,100")),
    B("So: work out the marked price first, and take the discount from that. Each percent belongs to its own amount."),
)
