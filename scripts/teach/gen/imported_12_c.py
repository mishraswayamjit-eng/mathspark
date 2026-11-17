"""Percent and money stories from batch 12."""
from fractions import Fraction

from imported_12_lib import A, AL, B, CH, CIRC, E, G, LB, LESSON, MINUS, NOTE, STRIKE, UL, W, n, pick, shuffled  # noqa: F401

P = "AIGEN_grade5_"

LESSONS = {}


# ── "Has T rupees, spends p% on one thing and a fixed amount on another. What is left?" ──

def pct_spend(qid, who, total, pct, item_costs, fixed, then, intro, given, trap):
    t10 = total // 10
    part = total * pct // 100
    rest = total - part
    left = rest - fixed
    assert part * 100 == total * pct and left > 0
    choices, at = shuffled(qid, "ask", str(t10), [n(Fraction(total, 100)), "10"])
    lead = pick(qid, "lead", [
        "Percent means out of every hundred. The friendliest percent to find is 10 percent, because it is one tenth. What is 10 percent of %d?",
        "A percent is a share of the whole amount, not a number of rupees. The easy way in is 10 percent, which is one tenth. What is 10 percent of %d?",
    ]) % total
    beats = [
        B(intro, G("q", given)),
        B(lead, ask=CH(choices, at,
                       "10 percent is one tenth, and to find a tenth we divide by 10. %d divided by 10 is %d." % (total, t10))),
        B("10 percent of %d is %d." % (total, t10), E("p10", "10%% of %d" % total)),
    ]
    if pct % 10 == 0:
        k = pct // 10
        beats.append(B("%d percent is %d lots of 10 percent. %d times %d is %d. So %s %d rupees." % (pct, k, k, t10, part, item_costs, part),
                       E("p1", "%d × %d" % (k, t10)), E("p", "%d%% of %d" % (pct, total))))
    else:
        assert pct == 15 and t10 % 2 == 0
        half = t10 // 2
        beats.append(B("5 percent is half of 10 percent, and half of %d is %d. So 15 percent is %d plus %d, which is %d. That means %s %d rupees." % (
            t10, half, t10, half, part, item_costs, part),
            E("p5", "5%% of %d" % total), E("p1", "%d + %d" % (t10, half)), E("p", "15%% of %d" % total)))
    beats += [
        B("Take that out of the %d rupees. %d minus %d is %d." % (total, total, part, rest),
          E("r", "%d − %d" % (total, part)), UL("r", str(rest))),
        B("%s %d minus %d is %d. %s has %d rupees left." % (then, rest, fixed, left, who, left),
          A("ans", "%d − %d" % (rest, fixed))),
        B(trap),
        B("Check that every rupee is accounted for. %d plus %d plus %d is %d, the money %s started with." % (part, fixed, left, total, who),
          E("k", "%d + %d + %d" % (part, fixed, left))),
        B(pick(qid, "sum", [
            "So find 10 percent first and build the percent you need from it. Then take away each thing that was spent.",
            "So start from 10 percent, build up to the percent in the question, and then subtract every amount spent.",
        ])),
    ]
    return LESSON(beats)


LESSONS[P + "0c554142-dbeb-4a08-9112-6d4bf8620665"] = pct_spend(
    P + "0c554142-dbeb-4a08-9112-6d4bf8620665", "Riya", 600, 20, "the storybook costs", 150,
    "Then she gives her brother 150 rupees.",
    "Riya saved 600 rupees. She spent 20 percent of it on a storybook, and then gave 150 rupees to her brother. How much does she have left?",
    "₹600: 20% on a storybook, then ₹150 to her brother",
    "The trap is reading 20 percent as 20 rupees. A percent depends on what it is a percent of, and here it came to 120 rupees.")

LESSONS[P + "0fc47074-0ab2-439e-820e-4dc4f177e4a3"] = pct_spend(
    P + "0fc47074-0ab2-439e-820e-4dc4f177e4a3", "Meera", 650, 40, "the kites cost", 110,
    "Then she buys tilgul for 110 rupees.",
    "Meera has 650 rupees to spend at the fair. She spends 40 percent of it on kites, and then buys tilgul for 110 rupees. How much does she have left?",
    "₹650: 40% on kites, then ₹110 on tilgul",
    "Careful: 260 is among the choices. But 260 is what the kites cost, not what Meera has left.")

LESSONS[P + "1ebecdc8-3435-454c-ba91-055ce493faa5"] = pct_spend(
    P + "1ebecdc8-3435-454c-ba91-055ce493faa5", "Kiran", 800, 15, "the gloves cost", 95,
    "Then he buys a cricket ball for 95 rupees.",
    "Kiran has 800 rupees for cricket gear. He spends 15 percent of it on batting gloves, and then buys a ball for 95 rupees. How much does he have left?",
    "₹800: 15% on gloves, then ₹95 on a ball",
    "Careful not to stop after the gloves. 680 is among the choices, and that is the money he had before he bought the ball.")

LESSONS[P + "1efc799d-e9fe-4c6b-8c1a-91bafb1cd786"] = pct_spend(
    P + "1efc799d-e9fe-4c6b-8c1a-91bafb1cd786", "Meera", 500, 30, "the bangles cost", 80,
    "Then she buys a box of sweets for 80 rupees.",
    "Meera goes to the mela with 500 rupees. She spends 30 percent of it on bangles, and then buys a box of sweets for 80 rupees. How much does she have left?",
    "₹500: 30% on bangles, then ₹80 on sweets",
    "The trap is reading 30 percent as 30 rupees. It is 30 out of every hundred, and with 500 rupees that came to 150.")


# ── Chains, written one by one ──────────────────────────────────────────────

# Kavya: ₹1,200, saves 25%, 40% of the rest on a bat, samosas at ₹15.
LESSONS[P + "0907882b-c663-4775-972c-b7ce060504a8"] = LESSON(
    B("Kavya has 1200 rupees. She saves 25 percent, spends 40 percent of the remaining money on a bat, and buys samosas at 15 rupees each with the rest. How many samosas?",
      G("q", "₹1,200: saves 25%; 40% of the rest on a bat; samosas ₹15")),
    B("25 percent is one quarter. A quarter of 1200 is 300, so she saves 300 rupees.",
      E("a", "25% of 1200")),
    B("1200 minus 300 leaves 900 rupees.",
      E("b", "1200 − 300"), UL("b", "900")),
    B("Now the bat: 40 percent. But 40 percent of what?",
      ask=CH(["40% of 1200", "40% of 900", "40% of 300"], 1,
             "The question says 40 percent of the remaining money. What remained after saving was 900 rupees, so the 40 percent comes out of 900.")),
    B("10 percent of 900 is 90, and 40 percent is 4 times that: 360 rupees for the bat.",
      E("c1", "10% of 900"), E("c", "40% of 900")),
    B("900 minus 360 leaves 540 rupees for samosas.",
      E("d", "900 − 360"), UL("d", "540")),
    B("Each samosa costs 15 rupees. 30 samosas cost 450, which leaves 90, and 90 rupees buys 6 more. So that is 36 samosas.",
      E("e1", "15 × 30"), E("e2", "540 − 450"), E("e3", "15 × 6"), A("e", "540 ÷ 15")),
    B("Check that all the money is used: 300 saved, 360 on the bat and 540 on samosas. Together that is 1200.",
      E("k", "300 + 360 + 540")),
    B("So in a chain like this, each percent is taken from what is left at that moment, not from the amount at the start."),
)

# Neha: ₹2,000, saves 40%, 25% of the rest on books, ₹150, donates half.
LESSONS[P + "24b08eb7-b9a1-4283-a59d-7d4c85adc075"] = LESSON(
    B("Neha has 2000 rupees. She saves 40 percent, spends 25 percent of the remaining amount on books, spends 150 rupees on rangoli colours, and donates half of what is still left. How much does she donate?",
      G("q", "₹2,000: save 40%; 25% of rest on books; ₹150; donate half")),
    B("First the savings. 10 percent of 2000 is 200, so 40 percent is 4 times that: 800 rupees.",
      E("a1", "10% of 2000"), E("a", "40% of 2000")),
    B("2000 minus 800 leaves 1200 rupees.",
      E("b", "2000 − 800"), UL("b", "1200")),
    B("Now the books: 25 percent. Of which amount?",
      ask=CH(["2000", "1200", "800"], 1,
             "The question says 25 percent of the remaining amount. After saving, 1200 rupees remained, so the books come out of 1200.")),
    B("25 percent is one quarter, and a quarter of 1200 is 300. The books cost 300 rupees.",
      E("c", "25% of 1200")),
    B("1200 minus 300 leaves 900. Then the rangoli colours: 900 minus 150 leaves 750 rupees.",
      E("d", "1200 − 300"), E("e", "900 − 150"), UL("e", "750")),
    B("She donates half of what is still left. What is half of 750?",
      ask=CH(["325", "350", "375"], 2,
             "Half means two equal shares. Two lots of 375 make 750, so each half is 375.")),
    B("750 divided by 2 is 375. Neha donates 375 rupees.",
      A("f", "750 ÷ 2")),
    B("The trap in this question is the word remaining. Take 25 percent of the full 2000 and the books would cost 500, which throws out everything after it.",
      E("t", "25% of 2000")),
    B("Check every rupee: 800 saved, 300 on books, 150 on colours, 375 donated and 375 kept. That adds up to 2000.",
      E("k", "800 + 300 + 150 + 375 + 375")),
    B("So go one step at a time, and after each step write down what is left. The next step always starts from there."),
)

# Riya: ₹1,000; 8 × ₹65 and 5 × ₹40; 10% off the bill.
LESSONS[P + "2a7e4ecf-6ef1-488b-a444-5c32e886bf9c"] = LESSON(
    B("Riya has 1000 rupees. She buys 8 packets of coloured powder at 65 rupees each and 5 bottles of glue at 40 rupees each. The shopkeeper takes 10 percent off the bill. How much money does she have left?",
      G("q", "₹1,000; 8 × ₹65 and 5 × ₹40; 10% discount on the bill")),
    B("First the powder. 8 times 60 is 480 and 8 times 5 is 40, so 8 packets cost 520 rupees.",
      E("a1", "8 × 60"), E("a2", "8 × 5"), E("a", "8 × 65")),
    B("The glue: 5 bottles at 40 rupees cost 200 rupees. So the bill is 520 plus 200, which is 720 rupees.",
      E("b", "5 × 40"), E("c", "520 + 200"), UL("c", "720")),
    B("The discount is 10 percent of the bill. What is 10 percent of 720?",
      ask=CH(["10", "72", "7.2"], 1,
             "10 percent is one tenth, so divide the bill by 10. It is not simply 10 rupees: it depends on the size of the bill.")),
    B("10 percent of 720 is 72. So 72 rupees come off the bill.",
      E("d", "10% of 720")),
    B("A discount makes the bill smaller. 720 minus 72 is 648, so Riya pays 648 rupees.",
      E("e", "720 − 72"), UL("e", "648")),
    B("648 is what she pays. Is that the answer to the question?",
      ask=CH(["Yes, 648", "No, take it away from 1000"], 1,
             "The question asks how much money Riya has left. She started with 1000 rupees and paid 648, so there is one more subtraction to do.")),
    B("1000 minus 648 is 352. Riya has 352 rupees left.",
      A("f", "1000 − 648")),
    B("Check it another way. With no discount she would have 1000 minus 720, which is 280 rupees. The discount gives her 72 back, and 280 plus 72 is 352.",
      E("k1", "1000 − 720"), E("k2", "280 + 72")),
    B("And notice that 280 is among the choices. That is the answer if you forget the discount."),
    B("So work out the bill, take the discount off the bill, and then take what she pays away from her money."),
)
