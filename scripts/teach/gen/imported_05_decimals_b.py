"""Batch 05: litres into cups, runs, and adding money in columns (part B)."""
from imported_05_lib import ANS, B, D, FIG, GIVEN, M, N, RING, S, W, ask, lesson, mon, num, rs, table

LESSONS = {}

P = "AIGEN_grade5_"

LESSONS[P + "86363894-f540-4c97-b61f-24a658ebc331"] = lesson(
    B("Ananya starts with 5 litres of lemonade and pours 12 glasses of 0.35 litres each. How much is left in the bottle?",
      GIVEN("q", "5 litres. 12 glasses of 0.35 litres each.", True)),
    B("What do we work out first?",
      ask=ask("how much the 12 glasses hold", ["5 − 0.35", "5 − 12"],
              "She pours 12 glasses, not 1. So first find how much lemonade all 12 take, and then take that away from the 5 litres.")),
    B("12 times 0.35. 10 glasses take 3.5 litres, and 2 glasses take 0.7 litres.",
      W("m1", "10 × 0.35 = 3.5"), W("m2", "2 × 0.35 = 0.7")),
    B("3.5 plus 0.7 is 4.2 litres poured out.",
      W("m3", "12 × 0.35 = 4.2"), N("m3", "4.2", "poured out")),
    B("Careful: 4.2 is what went into the glasses, and it is one of the choices. The question asks what is still in the bottle."),
    B("5 minus 4.2. From 4.2 up to 5 is 0.8. So 0.8 litres are left.",
      ANS("a", "5 − 4.2 = 0.8"), RING("a", "0.8")),
    B("Check: 4.2 poured, plus 0.8 left, makes 5 litres.",
      W("c", "4.2 + 0.8 = 5")),
    B("So when the same amount is taken many times, multiply first. Then subtract the total from what you started with."),
)

LESSONS[P + "9a3c1e27-b583-48b9-bbef-b6669df9ecd0"] = lesson(
    B("Rohit bats for 2 sessions. We know the overs and the runs per over in each. How many runs does he score altogether?",
      GIVEN("q", "Total runs in both sessions = ?", True),
      FIG("f", table(["Session", "Overs", "Runs per over"], [["First", "12.5", "6.4"], ["Second", "7.5", "8.2"]]))),
    B("Runs per over, times the number of overs, gives the runs. So each session is one multiplication, and then we add the two."),
    B("First session: 12.5 times 6.4. Split 12.5 into 10 and 2.5. 10 times 6.4 is 64.",
      W("a0", "12.5 = 10 + 2.5"), W("a1", "10 × 6.4 = 64")),
    B("And 2.5 times 6.4? Here is a hint: 2.5 is a quarter of 10.",
      ask=ask("16", ["1.6", "160"],
              "10 times 6.4 was 64. And 2.5 is a quarter of 10, so we want a quarter of 64. 4 times 16 is 64, so a quarter of 64 is 16.")),
    B("64 plus 16 is 80 runs in the first session.",
      W("a2", "2.5 × 6.4 = 16"), W("a3", "12.5 × 6.4 = 80")),
    B("Second session: 7.5 times 8.2. 7 times 8.2 is 57.4, and half of 8.2 is 4.1.",
      W("b1", "7 × 8.2 = 57.4"), W("b2", "0.5 × 8.2 = 4.1")),
    B("57.4 plus 4.1 is 61.5 runs in the second session.",
      W("b3", "7.5 × 8.2 = 61.5")),
    B("Altogether: 80 plus 61.5 is 141.5 runs.",
      ANS("ans", "80 + 61.5 = 141.5"), RING("ans", "141.5")),
    B("Check the second session another way. 7.5 times 8 is 60, and 7.5 times 0.2 is 1.5. That makes 61.5 again.",
      W("c1", "7.5 × 8 = 60"), W("c2", "7.5 × 0.2 = 1.5")),
    B("Careful not to drop the 0.5 at the end of 61.5: one of the choices is waiting for that slip. Split an awkward decimal into easy pieces, multiply each, and add."),
)

LESSONS[P + "9d323719-681e-43d8-85e2-18ec0e94b6b2"] = lesson(
    B("Sneha has 15.6 kilograms of besan. She uses 2.35 kilograms a day for 4 days, and on day 5 she uses all that is left. How much is that?",
      GIVEN("q", "15.6 kg of besan. Uses 2.35 kg a day for 4 days.", True), W("q2", "Day 5: all that is left = ?", True)),
    B("What do we need before we can find day 5?",
      ask=ask("the total used in 4 days", ["15.6 − 2.35", "15.6 ÷ 5"],
              "She uses 2.35 kilograms on each of 4 days, not just once. And day 5 is not an equal share: it is whatever is left. So first find what the 4 days used.")),
    B("4 times 2.35. Double it: 4.70. Double again: 9.40. So 9.40 kilograms are gone after 4 days.",
      W("m1", "2 × 2.35 = 4.70"), W("m2", "4 × 2.35 = 9.40")),
    B("Now subtract from 15.6. Write it as 15.60, so the decimal points line up.",
      W("z", "15.6 = 15.60")),
    B("15.60 minus 9.40 is 6.20. On day 5 she uses 6.20 kilograms.",
      ANS("a", "15.60 − 9.40 = 6.20"), RING("a", "6.20")),
    B("Check: 9.40 used in 4 days, plus 6.20 on day 5, is 15.60. That is all the besan.",
      W("c", "9.40 + 6.20 = 15.60")),
    B("Notice that day 5 uses far more than the other days. That is fine: the story says she uses whatever is left."),
    B("So multiply for the equal days, then subtract from the start. And write in a zero when one number has fewer decimal places."),
)


# ── Litres of chai into cups, cups into rupees ───────────────────────────────

def chai(qid, intro, given, given2, a, b, cup, per, price, what, cup_if_not, others, closing):
    a, b, cup, price = D(a), D(b), D(cup), D(price)
    total = a + b
    cups = total * per
    assert cup * per == 1 and cups == cups.to_integral_value()
    whole = int(price)
    x, y = cups * whole, cups * (price - whole)
    assert price - whole == D("0.5")
    earn = cups * price
    if total == total.to_integral_value():
        count = B("Every litre makes %d cups. So %s litres make %s times %d, which is %s cups." % (
            per, num(total), num(total), per, num(cups)),
            W("u", "%d × %s = 1" % (per, num(cup))), W("n", "%s ÷ %s = %s" % (num(total), num(cup), num(cups))))
    else:
        t0 = int(total)
        assert total - t0 == D("0.25") and per == 4
        count = B("Every litre makes %d cups. So the %d whole litres make %s cups, and the extra quarter litre makes 1 more. That is %s cups." % (
            per, t0, num(t0 * per), num(cups)),
            W("u", "%d × %s = 1" % (per, num(cup))), W("n0", "%d × %d = %s" % (t0, per, num(t0 * per))),
            W("n", "%s ÷ %s = %s" % (num(total), num(cup), num(cups))))
    LESSONS[qid] = lesson(
        B(intro, GIVEN("q", given, True), W("q2", given2, True)),
        B("First, all the %s together. %s plus %s is %s litres." % (what, num(a), num(b), num(total)),
          W("t", "%s + %s = %s" % (num(a), num(b), num(total)))),
        B("Each cup takes %s litres. How many cups come out of 1 litre?" % num(cup),
          ask=ask(str(per), others, cup_if_not)),
        count,
        B("Careful: do not multiply the litres by the price. The %s rupees is for a cup, not for a litre. That is why we needed the number of cups." % mon(price)),
        B("Now the money. %s cups at %s each. %s times %d is %s, and %s halves are %s." % (
            num(cups), mon(price), num(cups), whole, num(x), num(cups), mon(y)),
          W("e1", "%s × %d = %s" % (num(cups), whole, num(x))), W("e2", "%s × 0.50 = %s" % (num(cups), mon(y)))),
        B("%s plus %s is %s rupees." % (num(x), mon(y), mon(earn)),
          ANS("a", "%s × %s = %s" % (num(cups), rs(price), rs(earn))), RING("a", rs(earn))),
        B("Check by going back. %s rupees at %s a cup is %s cups, and %s cups of %s litres is %s litres. It fits." % (
            mon(earn), mon(price), num(cups), num(cups), num(cup), num(total)),
          W("c1", "%s ÷ %s = %s" % (mon(earn), mon(price), num(cups))), W("c2", "%s × %s = %s" % (num(cups), num(cup), num(total)))),
        B(closing),
    )


chai(P + "5ce76247-8d7c-4031-8b8a-0a46da1e2439",
     "Arjun's family sold 12.5 litres of chai in the morning and 8.75 litres in the evening. Each cup uses 0.25 litres and sells for 15.50 rupees. How much did they earn?",
     "Sold 12.5 litres and 8.75 litres of chai", "Each cup: 0.25 litres, sold for ₹15.50",
     "12.5", "8.75", "0.25", 4, "15.50", "chai",
     "0.25 is a quarter, and 4 quarters make 1 whole. So 1 litre fills 4 cups.", ["25", "2.5"],
     "So the chain is: litres, then cups, then rupees. Find how many cups there are before you touch the price.")
chai(P + "d383d448-cc1a-4b38-a85b-1a3ed618cabb",
     "Ananya's mother buys 5.75 litres of milk in the morning and 3.25 litres in the evening. Each cup of chai needs 0.125 litres of milk and sells for 12.50 rupees. How much does she earn?",
     "Milk: 5.75 litres and 3.25 litres", "Each cup: 0.125 litres of milk, sold for ₹12.50",
     "5.75", "3.25", "0.125", 8, "12.50", "milk",
     "0.125 is one eighth. Count up in steps of 0.125, and the 8th step lands exactly on 1. So 1 litre makes 8 cups.", ["125", "12"],
     "Milk, then cups, then money. Each step needs the one before it, so take them in order.")


LESSONS[P + "42bcf72c-5d03-4484-9f0b-8657ab692af0"] = lesson(
    B("On Monday the stall sold 12.5 litres of chai and then 8.75 litres, in cups of 0.25 litres. On Tuesday it took in 1085 rupees at 15.50 a cup. How many more cups were sold on Monday?",
      GIVEN("q", "Monday: 12.5 + 8.75 litres, 0.25 litres a cup", True), W("q2", "Tuesday: ₹1085 at ₹15.50 a cup", True)),
    B("We must compare cups with cups. Monday is told in litres and Tuesday in rupees, so we turn each day into cups."),
    B("Monday first. 12.5 plus 8.75 is 21.25 litres.",
      W("m1", "12.5 + 8.75 = 21.25")),
    B("A cup holds 0.25 litres. How many cups are there in 1 litre?",
      ask=ask("4", ["25", "2.5"],
              "0.25 is a quarter. 4 quarters make a whole, so 1 litre fills 4 cups.")),
    B("So the 21 whole litres fill 84 cups, and the extra quarter litre fills 1 more. Monday: 85 cups.",
      W("m2", "21 × 4 = 84"), W("m3", "21.25 ÷ 0.25 = 85"), N("m3", "85", "Monday")),
    B("Tuesday: 15.50 is awkward, so double it. 2 cups cost 31 rupees.",
      W("t1", "2 × ₹15.50 = ₹31")),
    B("1085 divided by 31 is 35. So that is 35 pairs of cups, which makes 70 cups on Tuesday.",
      W("t2", "1085 ÷ 31 = 35"), W("t3", "35 × 2 = 70"), N("t3", "70", "Tuesday")),
    B("Monday 85 cups, Tuesday 70 cups. 85 minus 70 is 15 more cups on Monday.",
      ANS("a", "85 − 70 = 15"), RING("a", "15")),
    B("Check Tuesday: 70 cups at 15.50 each is 1085 rupees. It works.",
      W("c", "70 × ₹15.50 = ₹1085")),
    B("Careful: 85 and 70 are both among the choices, but each is only half the story. Turn both days into the same thing, then compare."),
)


# ── Adding rupees and paise ──────────────────────────────────────────────────

LESSONS["IPMTB_grade5_ch05_q016"] = lesson(
    B("Poonam has 16.75 rupees, Urmila has 25.25 and Anjali has 9.05. How much do they have in all?",
      GIVEN("q", "Rs. 16.75 + Rs. 25.25 + Rs. 9.05 = ?")),
    B("With money, the part before the point is rupees, and the part after it is paise. A tidy way is to add the rupees and the paise separately.",
      FIG("f", table(["Rupees", "Paise"], [["16", "75"], ["25", "25"], ["9", "05"]]))),
    B("Rupees first: 16 plus 25 plus 9 is 50.",
      W("r", "16 + 25 + 9 = 50")),
    B("Now the paise: 75 plus 25 plus 5 is 105.",
      W("p", "75 + 25 + 5 = 105"), W("h", "100 paise = 1 rupee", True)),
    B("105 paise. How do we write that in rupees?",
      ask=ask("Rs. 1.05", ["Rs. 10.5", "Rs. 0.105"],
              "100 paise make 1 rupee. So 105 paise is 1 rupee and 5 paise more, and we write that as 1.05.")),
    B("So the total is 50 rupees plus 1.05 rupees. That is 51.05.",
      ANS("a", "50 + 1.05 = 51.05"), RING("a", "51.05")),
    B("Careful with 9.05. It is 9 rupees and 5 paise, not 50 paise. The zero after the point holds the place.",
      M("q", "9.05", "box")),
    B("Check by adding with the points in line. 16.75 plus 25.25 is 42, and 42 plus 9.05 is 51.05.",
      W("c1", "16.75 + 25.25 = 42"), W("c2", "42 + 9.05 = 51.05")),
    B("So add rupees to rupees and paise to paise. When the paise pass 100, they hand 1 rupee over."),
)

LESSONS["IPMTB_grade5_ch05_q039"] = lesson(
    B("Asha has 16.25 rupees, Reeta has 60.05 and Geeta has 33.75. How much do they have in all?",
      GIVEN("q", "Rs. 16.25 + Rs. 60.05 + Rs. 33.75 = ?")),
    B("Write the three amounts one under another, with the decimal points in line. Then add from the right, just as with whole numbers.",
      FIG("f", table(["Tens", "Ones", "Point", "Tenths", "Hundredths"],
                     [["1", "6", ".", "2", "5"], ["6", "0", ".", "0", "5"], ["3", "3", ".", "7", "5"]]))),
    B("Hundredths: 5 plus 5 plus 5 is 15. Write the 5 and carry 1.",
      W("h", "5 + 5 + 5 = 15"), N("h", "15", "write 5, carry 1")),
    B("Tenths: 2 plus 0 plus 7 is 9, and the carried 1 makes 10. Write 0 and carry 1.",
      W("t", "2 + 0 + 7 + 1 = 10"), N("t", "10", "write 0, carry 1")),
    B("Ones: 6 plus 0 plus 3 is 9, and the carried 1 makes 10 again. Write 0 and carry 1.",
      W("o", "6 + 0 + 3 + 1 = 10"), N("o", "10", "write 0, carry 1")),
    B("Tens column: 1 plus 6 plus 3, and the carried 1. What goes there?",
      ask=ask("11", ["10", "1"],
              "1 plus 6 plus 3 is 10, and the carry makes it 11. Leave out that carry and you get 10, which is exactly the trap in this question.")),
    B("So the total is 110.05 rupees.",
      W("s", "16.25 + 60.05 + 33.75 = 110.05"), M("s", "110.05")),
    B("Now look at the choices: 100, 100.05 and 100.75. Ours is 110.05, and it is not there. So the answer is None of these.",
      W("ch", "Choices: 100, 100.05, 100.75", True), ANS("a", "None of these", True), RING("a", "None of these")),
    B("Check with rupees and paise apart. 16 plus 60 plus 33 is 109 rupees. The paise make 105, which is 1 rupee more and 5 paise. 110.05 again.",
      W("c1", "16 + 60 + 33 = 109"), W("c2", "25 + 5 + 75 = 105")),
    B("Careful: 100.05 looks so close that it is tempting. Trust your working. If you carried properly and your total is not listed, None of these is right."),
)
