"""Simple interest: one deposit (find the interest, the amount, the time or the rate)."""
from imported_09_lib import ANS, B, FORMULA, GIVEN, M, S, W, choose, lesson, pct_ask, per_year, yearly

LESSONS = {}

FORMULA_SAY = "principal times rate times time, divided by 100"

# ── Riya's ₹2500 at 6% for 2 years: the interest ─────────────────────────────
LESSONS["1a5c5992"] = lesson(
    B("Riya puts 2500 rupees in a bank that pays 6 percent simple interest a year, and leaves it there for 2 years. How much interest does she earn?",
      GIVEN("g", "P = ₹2500, R = 6% a year, T = 2 years")),
    pct_ask(6),
    yearly(2500, 6, "y", "So for 1 year:"),
    B("That is 150 rupees for 1 year. She leaves the money for 2 years. What do we do?",
      M("g", "T = 2 years"),
      ask=choose(["150 × 2", "150 + 2", "150 ÷ 2"], 0,
                 "Simple interest pays the same amount every year. 2 years means 2 lots of 150.")),
    B("150 times 2 is 300. Riya earns 300 rupees of interest, to spend on her cricket bat.",
      ANS("a", "150 × 2 = 300"), M("a", "300", "circle")),
    B("Here is the same working as one formula: " + FORMULA_SAY + ". 2500 times 6 times 2, divided by 100, is 300 again.",
      W("f", FORMULA, label=True), W("c", "2500 × 6 × 2 ÷ 100 = 300")),
    B("The slip to watch for is stopping at 150. That is only the interest for 1 year."),
    B("So: find the interest for 1 year, then multiply by the number of years."),
)

# ── Arjun's ₹4000 at 5% for 3 years: the total amount ────────────────────────
LESSONS["56c0860d"] = lesson(
    B("Arjun puts 4000 rupees in a bank at 5 percent simple interest a year. After 3 years he takes out everything: his deposit and the interest. How much will he have?",
      GIVEN("g", "P = ₹4000, R = 5% a year, T = 3 years")),
    pct_ask(5),
    yearly(4000, 5, "y", "So for 1 year:"),
    B("Simple interest pays the same every year. For 3 years, 200 times 3 is 600 rupees of interest.",
      M("g", "T = 3 years"), W("i", "200 × 3 = 600")),
    B("The question asks how much money he will have. Is 600 the answer?",
      ask=choose(["No, add the ₹4000 he put in", "Yes, ₹600", "No, take ₹600 off the ₹4000"], 0,
                 "600 rupees is only the extra money the bank adds. His own 4000 rupees is still there too, so he has both.")),
    B("4000 plus 600 is 4600. Arjun will have 4600 rupees.",
      ANS("a", "4000 + 600 = 4600"), M("a", "4600", "circle")),
    B("Check the interest with the formula: " + FORMULA_SAY + ". 4000 times 5 times 3, divided by 100, is 600.",
      W("f", FORMULA, label=True), W("c", "4000 × 5 × 3 ÷ 100 = 600")),
    B("So: interest for 1 year, times the number of years. And when the question says total amount, add the deposit back on."),
)

# ── School fees: ₹3000 at 8% for 2 years, then pay ₹3200 ─────────────────────
LESSONS["4f505a57"] = lesson(
    B("Meera's father puts 3000 rupees in a bank at 8 percent simple interest a year. After 2 years he takes out everything, pays 3200 in school fees, and we want to know what is left.",
      GIVEN("g", "P = ₹3000, R = 8% a year, T = 2 years"), GIVEN("g2", "Then pays fees of ₹3200")),
    yearly(3000, 8, "y", "Start with the interest for 1 year."),
    B("That is 240 rupees for 1 year. The money stays for 2 years. What do we do?",
      M("g", "T = 2 years"),
      ask=choose(["240 × 2", "240 + 2", "240 ÷ 2"], 0,
                 "Simple interest pays the same amount every year. 2 years means 2 lots of 240.")),
    B("240 times 2 is 480 rupees of interest.",
      W("i", "240 × 2 = 480")),
    B("He takes out everything, the deposit and the interest. How much is that?",
      ask=choose(["3000 + 480", "just 480", "3000 − 480"], 0,
                 "The bank gives back his own 3000 rupees, and on top of that the 480 it added. So we add the two.")),
    B("3000 plus 480 is 3480 rupees in his hand.",
      W("t", "3000 + 480 = 3480")),
    B("He pays 3200 in fees. 3480 minus 3200 is 280. He has 280 rupees left.",
      M("g2", "₹3200"), ANS("a", "3480 − 3200 = 280"), M("a", "280", "circle")),
    B("Check: the 3200 of fees plus the 280 left makes 3480 again.",
      W("c", "3200 + 280 = 3480")),
    B("This question has several steps, and each one leaves a tempting number behind: 240, then 480, then 3480. Keep going until you have answered what was asked."),
    B("So: interest for 1 year, times the years, add the deposit, then take away what is spent."),
)

# ── Ravi's cricket gear: the interest is already given ───────────────────────
LESSONS["76988107"] = lesson(
    B("Ravi put 4500 rupees in a bank at 6 percent. The interest he earned was 1080 rupees. He takes out everything and spends 2000 on cricket gear. How much is left?",
      GIVEN("g", "Deposit ₹4500, interest ₹1080, spends ₹2000")),
    B("The question gives the rate, 6 percent. Do we need it to find what is left?",
      ask=choose(["No, the interest is already given", "Yes, to find the interest"], 0,
                 "Read the question again: it tells us the interest was 1080 rupees. The bank's work is already done for us, so the 6 percent is extra information.")),
    B("So, what does he take out of the bank? His own deposit, plus the interest.",
      W("w", "Amount = deposit + interest", label=True), M("g", "interest ₹1080")),
    B("4500 plus 1080 is 5580 rupees.",
      W("t", "4500 + 1080 = 5580")),
    B("Then he spends 2000. Which sum do we write?",
      M("g", "spends ₹2000"),
      ask=choose(["5580 − 2000", "5580 + 2000", "4500 − 2000"], 0,
                 "Spending takes money away, and it comes out of everything he withdrew: the deposit and the interest together.")),
    B("5580 minus 2000 is 3580. Ravi has 3580 rupees left.",
      ANS("a", "5580 − 2000 = 3580"), M("a", "3580", "circle")),
    B("If you are curious, the 6 percent does fit. 4500 is 45 hundreds, and 45 times 6 is 270 rupees a year. 1080 is 4 lots of 270, so the money stayed for 4 years.",
      W("c1", "45 × 6 = 270"), W("c2", "270 × 4 = 1080")),
    B("The traps are the leftovers of half-finished working: 5580 is before the spending, and 1080 is only the interest."),
    B("Before you calculate, sort what the question gives you from what it asks. Not every number has to be used."),
)


# ── Find the time ────────────────────────────────────────────────────────────

def find_time(intro, given, p, r, i, ending, trap, summary, amount=None, who="She"):
    y = per_year(p, r)
    assert i % y == 0
    t = i // y
    beats = [B(intro, GIVEN("g", given))]
    if amount:
        assert amount - p == i
        beats += [
            B("%s got back %d rupees in total. How much of that is interest?" % (who, amount),
              ask=choose(["%d − %d" % (amount, p), "%d + %d" % (amount, p), "all %d" % amount], 0,
                         "The total is the deposit plus the interest. Take the deposit away, and what remains is the interest.")),
            B("%d minus %d is %d. So the bank added %d rupees of interest." % (amount, p, i, i),
              W("i", "%d − %d = %d" % (amount, p, i)), M("i", str(i), "underline", ("%d − %d = %d" % (amount, p, i)).count(str(i)))),
            yearly(p, r, "y", "Now think about 1 year."),
        ]
    else:
        beats += [pct_ask(r), yearly(p, r, "y", "So for 1 year:")]
    beats += [
        B("So every year adds %d rupees. The interest was %d altogether. How do we find the number of years?" % (y, i),
          ask=choose(["%d ÷ %d" % (i, y), "%d × %d" % (i, y), "%d − %d" % (i, y)], 0,
                     "Each year brings the same %d rupees. So we ask how many lots of %d fit into %d. That is a division." % (y, y, i))),
        B("%d divided by %d is %d, because %d times %d is %d. %s" % (i, y, t, t, y, i, ending),
          W("t1", "%d ÷ %d = %d" % (i, y, t)), W("t2", "%d × %d = %d" % (t, y, i)),
          ANS("a", "T = %d years" % t, True), M("a", "%d years" % t, "circle")),
        B("Check with the formula: %s. %d times %d times %d, divided by 100, is %d. It matches." % (FORMULA_SAY, p, r, t, i),
          W("f", FORMULA, label=True), W("c", "%d × %d × %d ÷ 100 = %d" % (p, r, t, i))),
        B(trap),
        B(summary),
    ]
    return lesson(beats)


LESSONS["54d4577b"] = find_time(
    "Kavya puts 8000 rupees in a bank that pays 4 percent simple interest a year. After some years she has earned 1600 rupees of interest. How many years was that?",
    "P = ₹8000, R = 4% a year, Interest = ₹1600, T = ?", 8000, 4, 1600,
    "So Kavya kept the money in the bank for 5 years.",
    "A slip to avoid: dividing 1600 by the rate, 4, straight away. The 4 is rupees per hundred, so first find what the whole 8000 earns in a year.",
    "To find the time: work out 1 year's interest, then see how many of those make up the whole interest.")

LESSONS["94a89f10"] = find_time(
    "Priya puts 6000 rupees in a bank that pays 4 percent simple interest a year. After some years the interest has grown to 1440 rupees. For how many years did she leave the money there?",
    "P = ₹6000, R = 4% a year, Interest = ₹1440, T = ?", 6000, 4, 1440,
    "So Priya kept her money in the bank for 6 years.",
    "Careful not to stop at 240. That is the interest for 1 year, and the question asks for the number of years.",
    "The interest grows by the same step every year. Find the step, then count the steps.")

LESSONS["49fa24cd"] = find_time(
    "Rohan's father puts 3500 rupees in a bank at 8 percent simple interest a year. When he takes it out, the total has become 4340 rupees. For how many years was the money in the bank?",
    "P = ₹3500, R = 8% a year, Amount = ₹4340, T = ?", 3500, 8, 840,
    "So the money was in the bank for 3 years.",
    "The trap is treating 4340 as the interest. Most of that is the father's own deposit coming back.",
    "Amount take away deposit gives the interest. Then find 1 year's interest and count how many years make it up.",
    amount=4340, who="He")

LESSONS["8f54931a"] = find_time(
    "Riya puts 2500 rupees in a bank that pays 8 percent simple interest a year. Later she receives 3100 rupees in total, with her deposit included. For how many years did she keep the money there?",
    "P = ₹2500, R = 8% a year, Amount = ₹3100, T = ?", 2500, 8, 600,
    "So Riya kept her money in the bank for 3 years.",
    "The trap is dividing the whole 3100 by 200. Only the 600 of interest was earned by waiting. The rest was hers from the start.",
    "First separate the interest from the deposit. Then it is 1 year's interest, and how many of those.",
    amount=3100)

# ── Neha's mother: find the rate ─────────────────────────────────────────────
LESSONS["35a7e6d5"] = lesson(
    B("Neha's mother puts 2000 rupees in a bank. After 3 years she receives 2480 rupees in total. What rate of simple interest did the bank pay each year?",
      GIVEN("g", "P = ₹2000, T = 3 years, Amount = ₹2480, R = ?")),
    B("She got back 2480 rupees in total. How much of that is interest?",
      ask=choose(["2480 − 2000", "2480 + 2000", "all 2480"], 0,
                 "The total is the deposit plus the interest. Take the deposit away, and what remains is the interest.")),
    B("2480 minus 2000 is 480. The bank added 480 rupees.",
      W("i", "2480 − 2000 = 480")),
    B("That 480 built up over 3 years, the same amount each year. 480 divided by 3 is 160 rupees a year.",
      M("g", "T = 3 years"), W("y", "480 ÷ 3 = 160")),
    B("The rate is the interest on each 100 rupees for 1 year. 2000 rupees is 20 hundreds, and together they earn 160 a year. So what does each hundred earn?",
      W("h", "2000 ÷ 100 = 20"),
      ask=choose(["160 ÷ 20", "160 × 20", "160 ÷ 100"], 0,
                 "The 160 rupees is shared equally among the 20 hundreds. Sharing equally is dividing: 160 divided by 20.")),
    B("160 divided by 20 is 8. Each 100 rupees earns 8 rupees a year, so the rate is 8 percent.",
      W("r", "160 ÷ 20 = 8"), ANS("a", "R = 8% a year", True), M("a", "8%", "circle")),
    B("Check with the formula: " + FORMULA_SAY + ". 2000 times 8 times 3, divided by 100, is 480. And 2000 plus 480 is 2480.",
      W("f", FORMULA, label=True), W("c1", "2000 × 8 × 3 ÷ 100 = 480"), W("c2", "2000 + 480 = 2480")),
    B("Watch out for 480 divided by 20, which gives 24. That is what each hundred earned over all 3 years, not in 1 year.",
      W("x", "480 ÷ 20 = 24"), S("x", "24", "3 years, not 1")),
    B("To find a rate: get the interest, cut it down to 1 year, then cut it down to 1 hundred."),
)

# ── Two amounts at two times: after 3 years and after 5 years ────────────────
LESSONS["20e7bc3c"] = lesson(
    B("Ravi's deposit grows by simple interest. After 3 years the amount is 7800 rupees. After 5 years it is 9000. We are not told the deposit or the rate, and we want the rate.",
      GIVEN("g", "After 3 years: ₹7800. After 5 years: ₹9000"), GIVEN("g2", "R = ?")),
    B("Between year 3 and year 5 the amount grew. What made it grow?",
      ask=choose(["2 more years of interest", "5 years of interest", "a new deposit"], 0,
                 "Ravi did not add any money. From year 3 to year 5 the bank simply paid interest for 2 more years.")),
    B("So 2 years of interest is 9000 minus 7800, which is 1200. Simple interest is the same every year, so 1 year is 600.",
      W("d", "9000 − 7800 = 1200"), W("y", "1200 ÷ 2 = 600")),
    B("Now we can peel the interest off. In the first 3 years the bank added 3 times 600, which is 1800.",
      W("i3", "3 × 600 = 1800")),
    B("After 3 years the amount was 7800, and 1800 of it is interest. What was the deposit?",
      ask=choose(["7800 − 1800", "7800 + 1800", "7800 − 600"], 0,
                 "The amount is the deposit plus the interest added so far. Take away the 3 years of interest, and the deposit is what remains.")),
    B("7800 minus 1800 is 6000. Ravi deposited 6000 rupees.",
      W("p", "7800 − 1800 = 6000"), M("p", "6000")),
    B("6000 is 60 hundreds, earning 600 a year between them. 600 divided by 60 is 10 rupees per hundred. So the rate is 10 percent.",
      W("h", "6000 ÷ 100 = 60"), W("r", "600 ÷ 60 = 10"), ANS("a", "R = 10% a year", True), M("a", "10%", "circle")),
    B("Check the 5 year amount. 5 years of interest is 5 times 600, which is 3000. And 6000 plus 3000 is 9000. It fits.",
      W("c1", "5 × 600 = 3000"), W("c2", "6000 + 3000 = 9000")),
    B("The trap is treating 7800 as the deposit. It already has 3 years of interest inside it."),
    B("Two amounts at two different times: subtract them, and you have the interest for the years in between."),
)

# ── Interest put into a second bank ──────────────────────────────────────────
LESSONS["98c88c51"] = lesson(
    B("Meera's mother put 8000 rupees in a bank and got back 9920 after 3 years. She then puts only the interest into a second bank, at 8 percent a year, for 2 years. How much interest does the second bank pay?",
      GIVEN("g", "First bank: ₹8000 becomes ₹9920"), GIVEN("g2", "Second bank: the interest only, at 8% for 2 years")),
    B("What goes into the second bank?",
      ask=choose(["only the interest from the first bank", "all ₹9920", "the ₹8000 deposit"], 0,
                 "Read that line again: she deposits the interest she had earned. So the second bank's principal is just the extra money, not the whole amount.")),
    B("So first we find that interest. 9920 minus 8000 is 1920 rupees. That is the new principal.",
      W("i", "9920 − 8000 = 1920"), M("i", "1920", "box")),
    B("The second bank pays 8 rupees on every 100, each year. So for 1 year we want 1920 times 8, divided by 100. First, 1920 times 8 is 15360.",
      M("g2", "8%"), W("f", "1 year: 1920 × 8 ÷ 100", label=True), W("m", "1920 × 8 = 15360")),
    B("Now divide 15360 by 100. What happens to the digits?",
      ask=choose(["they slide 2 places: 153.60", "they slide 1 place: 1536", "nothing changes: 15360"], 0,
                 "Dividing by 100 makes a number 100 times smaller. Every digit slides 2 places to the right, so a decimal point appears before the last 2 digits.")),
    B("15360 divided by 100 is 153.60. That is 153 rupees and 60 paise of interest for 1 year.",
      W("y", "15360 ÷ 100 = 153.60"), W("yw", "₹153.60 = 153 rupees 60 paise", label=True)),
    B("For 2 years, double it. 153.60 times 2 is 307.20. That is 307 rupees and 20 paise.",
      ANS("a", "153.60 × 2 = 307.20"), M("a", "307.20", "circle"), W("aw", "₹307.20 = 307 rupees 20 paise", label=True)),
    B("A rough check: 8 percent of about 2000 rupees, for 2 years, is 320. Our 307.20 is close, and a little less, as it should be, because 1920 is a little less than 2000.",
      W("c", "2000 × 8 × 2 ÷ 100 = 320")),
    B("The first bank's 3 years are not needed at all. And the tempting slip is using 8000 or 9920 as the new principal."),
    B("Work out exactly what money goes into the bank. Then it is the usual interest: 1 year first, then times the years."),
)
