"""Hand-written lessons, part D: simple interest questions from past papers."""
from money_percent_lib import ANSWER, ASK, B, FIG, GIVEN, MARK, NOTE, RING, W, bar, bars, lesson, rs, seg, table

LESSONS = {}
FORMULA = "Simple interest = Principal × Rate × Time ÷ 100"


def add(qid, beats):
    LESSONS[qid] = lesson(beats, "authored")


def years_table(rows):
    return table(["Year", "Interest"], rows)


def amount_bar(principal, amount, gap="interest ?"):
    """The amount as one bar: the money at the start, with the interest on the end."""
    return bars(bar([seg(6, principal, "a"), seg(2.5, gap, "b")], None, amount))


# ── Interest asked for directly ──────────────────────────────────────────────

Q = "EXT_G5_FP_2017_009"
add(Q, [
    B("3000 rupees earns simple interest at 12 per cent per annum, which means every year, for 5 years. We want the interest.",
      GIVEN("q", "Rs.3000 at 12% per annum for 5 years"), W("q2", "Simple interest = ?", label=True)),
    B("12 per cent means 12 out of every 100. So every 100 rupees earns 12 rupees in one year.",
      W("m", "Every Rs.100 earns Rs.12 in 1 year", label=True), MARK("q", "12%")),
    B("How many hundreds are in 3000? 3000 divided by 100 is 30. So there are 30 hundreds.",
      W("h", "3000 ÷ 100 = 30")),
    ASK(Q, "a1", "30 hundreds, each earning 12 rupees. Which sum gives the interest for one year?",
        "30 × 12", ["30 + 12", "3000 × 12"],
        "Each of the 30 hundreds earns 12 rupees. So it is 12 rupees, 30 times over: 30 times 12."),
    B("3 times 12 is 36, so 30 times 12 is 360. One year earns 360 rupees.",
      W("y1", "3 × 12 = 36"), W("y", "30 × 12 = 360"), NOTE("y", "= 360", "1 year", "below")),
    B("Simple interest earns the same every year. Here are the 5 years, one at a time.",
      FIG("years", years_table([[str(i), "Rs.360"] for i in range(1, 6)]))),
    B("So we need 5 lots of 360. 5 times 300 is 1500, and 5 times 60 is 300. Together, 1800.",
      W("i1", "5 × 300 = 1500"), W("i2", "5 × 60 = 300"), W("i", "5 × 360 = 1800")),
    B("The formula says the same thing. Simple interest is principal, times rate, times time, divided by 100. With our numbers, it also gives 1800.",
      W("f", FORMULA, label=True), W("f2", "3000 × 12 × 5 ÷ 100 = 1800")),
    B("So the simple interest is 1800 rupees.",
      ANSWER("ans", "Simple interest = Rs.1800"), RING("ans", "Rs.1800")),
    B("So: find the interest for one year first, then multiply by the number of years."),
])

Q = "EXT_G5_FP_2018_015"
add(Q, [
    B("A bank pays 6 per cent per annum simple interest. 8000 rupees is deposited for 2 years. How much interest does it earn?",
      GIVEN("q", "Rs.8000 at 6% per annum for 2 years"), W("q2", "Interest = ?", label=True)),
    B("Per annum means every year. And 6 per cent means 6 out of every 100. So every 100 rupees earns 6 rupees in one year.",
      W("m", "Every Rs.100 earns Rs.6 in 1 year", label=True), MARK("q", "6%")),
    B("8000 divided by 100 is 80. So the deposit is 80 hundreds.",
      W("h", "8000 ÷ 100 = 80")),
    ASK(Q, "a1", "80 hundreds, each earning 6 rupees. Which sum gives the interest for one year?",
        "80 × 6", ["80 + 6", "8000 × 6"],
        "Each of the 80 hundreds earns 6 rupees. So it is 6 rupees, 80 times over: 80 times 6."),
    B("8 times 6 is 48, so 80 times 6 is 480. One year earns 480 rupees.",
      W("y1", "8 × 6 = 48"), W("y", "80 × 6 = 480"), NOTE("y", "= 480", "1 year", "below"),
      FIG("years", years_table([["1", "Rs.480"], ["2", "Rs.480"]]))),
    B("Careful not to stop at 480. That is only one year, and the money stays in the bank for 2. Simple interest earns the same again in the second year.",
      MARK("q", "2 years")),
    B("480 and 480 make 960. So the interest is 960 rupees.",
      W("i", "2 × 480 = 960"), ANSWER("ans", "Interest = Rs.960"), RING("ans", "Rs.960")),
    B("Check with the formula: principal, times rate, times time, divided by 100. 8000 times 6 times 2, divided by 100, is 960. It matches.",
      W("f", FORMULA, label=True), W("f2", "8000 × 6 × 2 ÷ 100 = 960")),
    B("So: the interest for one year first, then times the number of years."),
])

Q = "EXT_G5_FP_2024_038"
add(Q, [
    B("4250 rupees earns simple interest for 5 years, at 8 per cent per annum. We want the simple interest.",
      GIVEN("q", "Rs.4250 for 5 years at 8% per annum"), W("q2", "Simple interest = ?", label=True)),
    B("8 per cent per annum means every 100 rupees earns 8 rupees in a year. But 4250 is not a whole number of hundreds, so we go through 10 per cent.",
      W("m", "Every Rs.100 earns Rs.8 in 1 year", label=True)),
    B("10 per cent of 4250 is 425. And 1 per cent is 42.5, so 2 per cent is double that: 85.",
      W("p1", "10% of 4250 = 425"), W("p2", "1% of 4250 = 42.5"), W("p3", "2% of 4250 = 2 × 42.5 = 85")),
    ASK(Q, "a1", "We have 10 per cent and 2 per cent. How do we make 8 per cent from them?",
        "10% − 2%", ["10% + 2%", "10% × 2%"],
        "8 is 2 less than 10. So 8 per cent is 10 per cent, with 2 per cent taken off."),
    B("425 minus 85 is 340. So one year earns 340 rupees.",
      W("p4", "8% of 4250 = 425 − 85 = 340"), NOTE("p4", "= 340", "1 year", "below"),
      FIG("years", years_table([[str(i), "Rs.340"] for i in range(1, 6)]))),
    B("Simple interest earns the same each year, for 5 years. 5 times 300 is 1500, and 5 times 40 is 200. Together, 1700.",
      W("i1", "5 × 300 = 1500"), W("i2", "5 × 40 = 200"), W("i", "5 × 340 = 1700")),
    B("Check with the formula: principal, times rate, times time, divided by 100. It gives 1700 as well.",
      W("f", FORMULA, label=True), W("f2", "4250 × 8 × 5 ÷ 100 = 1700")),
    B("So the simple interest is 1700 rupees.",
      ANSWER("ans", "Simple interest = Rs.1700"), RING("ans", "Rs.1700")),
    B("So: the interest for one year first, then times the number of years. And an awkward per cent can be built from easy ones."),
])

Q = "EXT_G5_FP_2022_022"
add(Q, [
    B("26500 rupees is deposited in a bank at 8 per cent per annum simple interest. We want the amount at the end of 4 years: everything that is there.",
      GIVEN("q", "Rs.26500 at 8% per annum for 4 years"), W("q2", "Amount = ?", label=True)),
    B("8 per cent means 8 out of every 100. So every 100 rupees earns 8 rupees in one year.",
      W("m", "Every Rs.100 earns Rs.8 in 1 year", label=True)),
    B("26500 divided by 100 is 265. So there are 265 hundreds, each earning 8 rupees a year.",
      W("h", "26500 ÷ 100 = 265")),
    B("265 times 8, in easy bites. 200 times 8 is 1600, 60 times 8 is 480, and 5 times 8 is 40. Together, 2120 rupees a year.",
      W("y1", "200 × 8 = 1600"), W("y2", "60 × 8 = 480"), W("y3", "5 × 8 = 40"), W("y", "265 × 8 = 1600 + 480 + 40 = 2120")),
    B("Simple interest earns the same every year. 4 years, each earning 2120. 4 times 2000 is 8000, and 4 times 120 is 480. So the interest is 8480 rupees.",
      FIG("years", years_table([[str(i), "Rs.2120"] for i in range(1, 5)])),
      W("i1", "4 × 2000 = 8000"), W("i2", "4 × 120 = 480"), W("i", "4 × 2120 = 8480")),
    ASK(Q, "a1", "Careful now. The question asks for the amount. Is 8480 the answer?",
        "No: add back the Rs.26500", ["Yes: Rs.8480", "No: take it from Rs.26500"],
        "8480 rupees is only the interest, the extra money. The amount is everything in the bank: the 26500 put in, plus the interest."),
    B("26500 plus 8480 is 34980. So the amount is 34980 rupees.",
      W("a", "26500 + 8480 = 34980"), NOTE("a", "26500", "principal"), NOTE("a", "+ 8480", "interest"),
      ANSWER("ans", "Amount = Rs.34980"), RING("ans", "Rs.34980")),
    B("Check the interest with the formula: principal, times rate, times time, divided by 100. It gives 8480 too.",
      W("f", FORMULA, label=True), W("f2", "26500 × 8 × 4 ÷ 100 = 8480")),
    B("So: interest for one year, then for all the years. And when the question says amount, add the interest on to the money at the start."),
])

Q = "EXT_G5_FP_2025_040"
add(Q, [
    B("16000 rupees is invested for 18 months, at 8 per cent per annum. We want the simple interest.",
      GIVEN("q", "Rs.16000 for 18 months at 8% per annum"), W("q2", "Simple interest = ?", label=True)),
    B("Per annum means every year. 8 per cent means every 100 rupees earns 8 rupees in one year. And 16000 is 160 hundreds.",
      W("m", "Every Rs.100 earns Rs.8 in 1 year", label=True), W("h", "16000 ÷ 100 = 160")),
    B("So one year earns 160 times 8. 16 times 8 is 128, so 160 times 8 is 1280 rupees.",
      W("y1", "16 × 8 = 128"), W("y", "160 × 8 = 1280"), NOTE("y", "= 1280", "1 year", "below")),
    ASK(Q, "a1", "The rate is for a year, but the money is invested for 18 months. How long is 18 months?",
        "1 year and 6 months", ["18 years", "1 year and 8 months"],
        "A year has 12 months. 18 months is 12 months and 6 more. That is 1 year, and half a year.",
        W("t", "18 months = 12 months + 6 months", label=True)),
    B("Careful, that is the trap here: the 18 is months, not years. The first year earns 1280. The extra 6 months is half a year, so it earns half of 1280, which is 640.",
      W("s3", "1280 ÷ 2 = 640"),
      FIG("years", table(["Time", "Interest"], [["1 year", "Rs.1280"], ["6 months", "Rs.640"]]))),
    B("1280 plus 640 is 1920. So the simple interest is 1920 rupees.",
      W("s4", "1280 + 640 = 1920"), ANSWER("ans", "Simple interest = Rs.1920"), RING("ans", "Rs.1920")),
    B("Check with the formula. The time must be in years, and 18 months is 1.5 years. 16000 times 8 times 1.5, divided by 100, is 1920.",
      W("f", FORMULA, label=True), W("f2", "16000 × 8 × 1.5 ÷ 100 = 1920")),
    B("So always check the time. If it is in months, turn it into years before you use the yearly rate."),
])


# ── The rate, from the principal and the amount ──────────────────────────────

def rate_lesson(qid, opener, givens, P, A, T, R, start, div_say, div_ops, answer_line, ring, extra=None):
    """Find the rate: amount − principal, then per year, then per hundred. `start` is 'borrowed' or 'put in'."""
    interest = A - P
    year = interest // T
    h = P // 100
    assert year * T == interest and h * 100 == P and h * R == year, qid
    first = [GIVEN("q", givens[0])] + [GIVEN("q%d" % i, g) for i, g in enumerate(givens[1:], 1)]
    beats = [
        B(opener, *(first + [W("want", "Rate of interest = ? % per annum", label=True)])),
        B("%d rupees is called the amount. It is the %d rupees that was %s, with the interest on top." % (A, P, start),
          FIG("f", amount_bar(rs(P), rs(A)))),
        ASK(qid, "a1", "So how do we find the interest?",
            "%d − %d" % (A, P), ["%d + %d" % (A, P), "%s is the interest" % rs(A)],
            "The amount is the starting money and the interest together. Take the starting money away, and the interest is what is left."),
        B("%d minus %d is %d. So the interest is %d rupees, for all %d years." % (A, P, interest, interest, T),
          W("s1", "%d − %d = %d" % (A, P, interest)), NOTE("s1", "= %d" % interest, "interest", "below")),
        B("Careful: the rate is for one year, not for all %d. Simple interest is the same every year, so one year's interest is %d divided by %d, which is %d."
          % (T, interest, T, year),
          W("s2", "%d ÷ %d = %d" % (interest, T, year)), NOTE("s2", "= %d" % year, "1 year", "below"),
          FIG("years", years_table([[str(i), rs(year)] for i in range(1, T + 1)]))),
        B("The rate tells us what every 100 rupees earns in one year. %d divided by 100 is %d, so the money is %d hundreds." % (P, h, h),
          W("m", "Rate = interest on each Rs.100 in 1 year", label=True), W("s3", "%d ÷ 100 = %d" % (P, h))),
        B(div_say, *(div_ops + [W("s4", "%d ÷ %d = %d" % (year, h, R))])),
        B("Each 100 rupees earns %d rupees a year. That is a rate of %d per cent per annum." % (R, R),
          ANSWER("ans", answer_line), RING("ans", ring)),
        B("Check with the formula: principal, times rate, times time, divided by 100. %d times %d times %d, divided by 100, is %d. That is our interest."
          % (P, R, T, interest),
          W("f", FORMULA, label=True), W("c", "%d × %d × %d ÷ 100 = %d" % (P, R, T, interest))),
        B(extra or "So for the rate: amount minus principal gives the interest. Share it over the years, and then over the hundreds."),
    ]
    add(qid, beats)


rate_lesson(
    "EXT_G5_FP_2019_031",
    "3200 rupees grows to 3680 rupees in 3 years, at simple interest. We want the rate of interest.",
    ["Rs.3200 amounts to Rs.3680 in 3 years"], 3200, 3680, 3, 5, "put in",
    "32 hundreds earn 160 rupees a year. 32 times 5 is 160, so each hundred earns 5 rupees.",
    [W("d1", "32 × 5 = 160")], "Rate = 5% per annum", "5%")

rate_lesson(
    "EXT_G5_FP_2020_030",
    "Kedar borrowed 12000 rupees from his friend at simple interest. After 5 years he paid back 15600 rupees to settle the loan. What rate did his friend charge?",
    ["Borrowed Rs.12000. Paid back Rs.15600 after 5 years."], 12000, 15600, 5, 6, "borrowed",
    "120 hundreds earn 720 rupees a year. 12 times 6 is 72, so 120 times 6 is 720. Each hundred earns 6 rupees.",
    [W("d1", "12 × 6 = 72"), W("d2", "120 × 6 = 720")], "Rate = 6% per annum", "6%",
    "So for the rate: what was paid back, minus what was borrowed, is the interest. Share it over the years, and then over the hundreds.")

rate_lesson(
    "EXT_G5_FP_2021_034",
    "Aniket borrowed 18000 rupees to open a grocery shop. He cleared the loan by paying 25560 rupees at the end of 3 years. We want the rate of interest.",
    ["Borrowed Rs.18000. Paid Rs.25560 after 3 years."], 18000, 25560, 3, 14, "borrowed",
    "180 hundreds earn 2520 rupees a year. 10 times 180 is 1800, and 4 times 180 is 720. Together that is 2520, so each hundred earns 14 rupees.",
    [W("d1", "10 × 180 = 1800"), W("d2", "4 × 180 = 720"), W("d3", "1800 + 720 = 2520")], "Rate = 14% per annum", "14%",
    "So for the rate: what was paid, minus what was borrowed, is the interest. Share it over the years, and then over the hundreds.")

rate_lesson(
    "EXT_G5_FP_2024_017",
    "Medha borrowed 3500 rupees from a friend at simple interest. After 3 years she repaid the loan with 4340 rupees. What was the rate of interest per annum?",
    ["Borrowed Rs.3500. Repaid Rs.4340 after 3 years."], 3500, 4340, 3, 8, "borrowed",
    "35 hundreds earn 280 rupees a year. Try 8: 30 times 8 is 240, and 5 times 8 is 40. Together that is 280, so each hundred earns 8 rupees.",
    [W("d1", "30 × 8 = 240"), W("d2", "5 × 8 = 40"), W("d3", "240 + 40 = 280")], "Rate = 8% per annum", "8%")

rate_lesson(
    "EXT_G5_FP_2025_007",
    "28500 rupees amounts to 38760 rupees in 3 years, at simple interest. We want the rate of interest, as a per cent per annum.",
    ["Rs.28500 amounts to Rs.38760 in 3 years"], 28500, 38760, 3, 12, "put in",
    "285 hundreds earn 3420 rupees a year. 10 times 285 is 2850, and 2 times 285 is 570. Together that is 3420, so each hundred earns 12 rupees.",
    [W("d1", "10 × 285 = 2850"), W("d2", "2 × 285 = 570"), W("d3", "2850 + 570 = 3420")], "Rate = 12% per annum", "12%")

Q = "EXT_G5_FP_2023_009"
add(Q, [
    B("6420 rupees amounts to 10272 rupees in 4 years, at simple interest. We want the rate of interest per annum.",
      GIVEN("q", "Rs.6420 amounts to Rs.10272 in 4 years"), W("want", "Rate of interest = ? % per annum", label=True)),
    B("10272 rupees is the amount: the 6420 rupees at the start, with the interest on top.",
      FIG("f", amount_bar("Rs.6420", "Rs.10272"))),
    ASK(Q, "a1", "So how do we find the interest?",
        "10272 − 6420", ["10272 + 6420", "Rs.10272 is the interest"],
        "The amount is the starting money and the interest together. Take the starting money away, and the interest is what is left."),
    B("10272 minus 6420 is 3852. So the interest is 3852 rupees, for all 4 years.",
      W("s1", "10272 − 6420 = 3852"), NOTE("s1", "= 3852", "interest", "below")),
    B("Careful: the rate is for one year, not for all 4. Simple interest is the same each year, so one year's interest is 3852 divided by 4, which is 963.",
      W("s2", "3852 ÷ 4 = 963"), NOTE("s2", "= 963", "1 year", "below")),
    B("The rate is that 963 as a per cent of the starting money. 1 per cent of 6420 is 64.2. So how many lots of 64.2 make 963?",
      W("s3", "1% of 6420 = 64.2")),
    B("10 lots of 64.2 make 642. 5 lots are half of that, 321. And 642 plus 321 is 963. So it is 15 lots: the rate is 15 per cent.",
      W("d1", "10 × 64.2 = 642"), W("d2", "5 × 64.2 = 321"), W("d3", "642 + 321 = 963"), W("d4", "15% of 6420 = 963")),
    B("Before we trust it, check with the formula: principal, times rate, times time, divided by 100. It gives 3852, our interest.",
      W("f", FORMULA, label=True), W("c", "6420 × 15 × 4 ÷ 100 = 3852")),
    ASK(Q, "a2", "So the rate is 15 per cent per annum. Now look at the choices. Which one matches?",
        "none of these", ["12%", "10%", "20%"],
        "Our rate is 15 per cent, and that is not on the list. When careful, checked working matches none of the choices, the answer is none of these."),
    B("So the answer is none of these. The rate is 15 per cent per annum, and that is not one of the choices.",
      ANSWER("ans", "Rate = 15%: none of these"), RING("ans", "none of these")),
    B("So for the rate: find the interest, bring it down to one year, then see what per cent of the starting money it is."),
])

# ── The time ─────────────────────────────────────────────────────────────────

Q = "EXT_G5_FP_2017_017"
add(Q, [
    B("2000 rupees is to grow to 3500 rupees, at simple interest of 5 per cent per annum. How many years will it take?",
      GIVEN("q", "Rs.2000 grows to Rs.3500 at 5% per annum"), W("q2", "Time = ? years", label=True)),
    B("3500 is the amount: the 2000 at the start, with the interest on top. So first, how much interest is needed?",
      FIG("f", amount_bar("Rs.2000", "Rs.3500"))),
    B("3500 minus 2000 is 1500. The money must earn 1500 rupees of interest.",
      W("s1", "3500 − 2000 = 1500"), NOTE("s1", "= 1500", "interest needed", "below")),
    B("Now, one year. 5 per cent means every 100 rupees earns 5 rupees in a year. 2000 is 20 hundreds, so one year earns 20 times 5, which is 100 rupees.",
      W("m", "Every Rs.100 earns Rs.5 in 1 year", label=True), W("s2", "2000 ÷ 100 = 20"), W("s3", "20 × 5 = 100"),
      NOTE("s3", "= 100", "1 year", "below")),
    ASK(Q, "a1", "Every year adds 100 rupees of interest. Which sum gives the number of years?",
        "1500 ÷ 100", ["3500 ÷ 100", "1500 × 100"],
        "Each year brings in 100 rupees, and we need 1500 rupees of interest. So we count how many hundreds fit into 1500."),
    B("Careful: we divide the interest, 1500, not the amount, 3500. 1500 divided by 100 is 15. So it takes 15 years.",
      W("s4", "1500 ÷ 100 = 15"), ANSWER("ans", "Time = 15 years"), RING("ans", "15 years")),
    B("Check: 15 years at 100 rupees a year is 1500. And 2000 plus 1500 is 3500, the amount. It works.",
      W("c1", "15 × 100 = 1500"), W("c2", "2000 + 1500 = 3500")),
    B("So for the time: find the interest needed, find the interest for one year, and divide."),
])

Q = "EXT_G5_FP_2018_031"
add(Q, [
    B("4000 rupees is to double, at 12.5 per cent simple interest. How many years will that take?",
      GIVEN("q", "Rs.4000 doubles at 12.5% simple interest"), W("q2", "Time = ? years", label=True)),
    ASK(Q, "a1", "The 4000 rupees must double. So how much interest has to be earned?",
        "Rs.4000", ["Rs.8000", "Rs.2000"],
        "Double 4000 is 8000. But the money starts at 4000, so the interest only has to bring in another 4000."),
    B("Double 4000 is 8000. Take away the 4000 we began with, and the interest needed is 4000 rupees.",
      W("s1", "2 × 4000 = 8000"), W("s2", "8000 − 4000 = 4000"), NOTE("s2", "= 4000", "interest needed", "below"),
      FIG("f", bars(bar([seg(4, "Rs.4000", "a"), seg(4, "interest", "b")], None, "Rs.8000"), note="To double, the interest must equal the start"))),
    B("Now one year, at 12.5 per cent. Start with 10 per cent of 4000, which is 400.",
      W("s3", "10% of 4000 = 400")),
    B("The other 2.5 per cent is a quarter of 10 per cent. A quarter of 400 is 100. So one year earns 400 plus 100, which is 500 rupees.",
      W("s4", "2.5% of 4000 = 400 ÷ 4 = 100"), W("s5", "12.5% of 4000 = 400 + 100 = 500"), NOTE("s5", "= 500", "1 year", "below")),
    B("Each year adds 500 rupees. How many years to reach 4000? 4000 divided by 500 is 8.",
      W("s6", "4000 ÷ 500 = 8"), ANSWER("ans", "Time = 8 years"), RING("ans", "8 years")),
    B("Here is a lovely way to check. 8 times 12.5 is 100. So in 8 years the interest reaches 100 per cent of the money: the whole sum again.",
      W("c", "8 × 12.5% = 100%")),
    B("So for doubling: the interest must equal the starting money. Find one year's interest, and divide."),
])

Q = "EXT_G5_FP_2020_018"
add(Q, [
    B("25 rupees is to become 37 rupees, at 16 per cent per annum simple interest. How long will it take?",
      GIVEN("q", "Rs.25 becomes Rs.37 at 16% per annum"), W("q2", "Time = ?", label=True)),
    B("37 rupees is the amount: the 25 at the start, with the interest on top. The interest needed is 37 minus 25, which is 12 rupees.",
      FIG("f", amount_bar("Rs.25", "Rs.37")), W("s1", "37 − 25 = 12"), NOTE("s1", "= 12", "interest needed", "below")),
    ASK(Q, "a1", "Now the interest for one year. It is 16 per cent of what?",
        "of Rs.25, the starting money", ["of Rs.37, the amount", "of Rs.12, the interest"],
        "Interest is always worked on the money at the start, the principal. That is 25 rupees."),
    B("16 per cent means 16 rupees on every 100. But 25 is only a quarter of 100. So it earns a quarter of 16, which is 4 rupees a year.",
      W("m", "4 × 25 = 100"), W("s2", "16 ÷ 4 = 4"), W("s3", "16% of 25 = 4"), NOTE("s3", "= 4", "1 year", "below")),
    B("Each year adds 4 rupees, and we need 12. 12 divided by 4 is 3. So it takes 3 years.",
      W("s4", "12 ÷ 4 = 3"), ANSWER("ans", "Time = 3 years"), RING("ans", "3 years")),
    B("Check it a year at a time, in the table. 25 grows to 29, then 33, then 37. After 3 years it reaches 37 rupees.",
      FIG("years", table(["Year", "Interest", "Money now"], [["1", "Rs.4", "Rs.29"], ["2", "Rs.4", "Rs.33"], ["3", "Rs.4", "Rs.37"]]))),
    B("So for the time: find the interest needed, find the interest for one year, and divide."),
])

Q = "EXT_G5_FP_2023_024"
add(Q, [
    B("450 rupees is to become four times itself, at 24 per cent per annum simple interest. How long will it take?",
      GIVEN("q", "Rs.450 becomes four times itself at 24% per annum"), W("q2", "Time = ?", label=True)),
    ASK(Q, "a1", "The money becomes 4 times itself. How many lots of 450 must come from the interest?",
        "3 lots", ["4 lots", "1 lot"],
        "There are 4 lots at the end, but 1 of them is the money we began with. So the interest must bring in the other 3 lots."),
    B("That is the trap: one of the 4 lots is already there. So the interest needed is 3 times 450, which is 1350 rupees.",
      W("s1", "3 × 450 = 1350"), NOTE("s1", "= 1350", "interest needed", "below"),
      FIG("f", bars(bar([seg(1, "450", "a"), seg(1, "450", "b"), seg(1, "450", "b"), seg(1, "450", "b")], None, "4 times Rs.450"),
                    note="1 lot is the start, 3 lots are interest"))),
    B("Now one year, at 24 per cent. 1 per cent of 450 is 4.5, so we need 24 lots of 4.5.",
      W("s2", "1% of 450 = 4.5")),
    B("24 times 4 is 96, and 24 halves are 12. Together, 108. So one year earns 108 rupees.",
      W("s3", "24 × 4 = 96"), W("s4", "24 × 0.5 = 12"), W("s5", "24% of 450 = 96 + 12 = 108"), NOTE("s5", "= 108", "1 year", "below")),
    B("How many years to earn 1350, at 108 a year? 10 years earn 1080. That leaves 1350 minus 1080, which is 270.",
      W("t1", "10 × 108 = 1080"), W("t2", "1350 − 1080 = 270")),
    B("2 more years earn 216, which leaves 54. And 54 is exactly half of 108, so that is half a year more. 10 and 2 make 12 years, and a half.",
      W("t3", "2 × 108 = 216"), W("t4", "270 − 216 = 54"), W("t5", "2 × 54 = 108"), W("t6", "10 + 2 = 12")),
    B("Half a year is 6 months. So the time is 12 years 6 months.",
      ANSWER("ans", "Time = 12 years 6 months"), RING("ans", "12 years 6 months")),
    B("Check: 12.5 years at 108 rupees a year comes to 1350, the interest we needed.",
      W("c", "12.5 × 108 = 1350")),
    B("So when money becomes so many times itself, take away the lot you began with. The rest is interest: divide it by one year's interest."),
])

# ── The principal ────────────────────────────────────────────────────────────

Q = "EXT_G5_FP_2016_039"
add(Q, [
    B("Some money is put away at 10 per cent simple interest per annum, for 5 years. It grows to 4500 rupees. How much was put in at the start?",
      GIVEN("q", "10% per annum for 5 years. Amount = Rs.4500."), W("q2", "Sum at the start = ?", label=True)),
    B("Think of the starting sum as 100 per cent. Each year, it earns 10 per cent of itself.",
      W("w", "Starting sum = 100%", label=True)),
    ASK(Q, "a1", "It earns 10 per cent every year, for 5 years. How much interest is that altogether?",
        "50% of the sum", ["10% of the sum", "15% of the sum"],
        "Simple interest earns the same each year. 10 per cent, 5 times over, is 50 per cent."),
    B("5 times 10 is 50. So the interest is 50 per cent of the starting sum: exactly half of it.",
      W("s1", "5 × 10% = 50%"),
      FIG("f", bars(bar([seg(2, "50%", "a"), seg(2, "50%", "a"), seg(2, "50%", "b")], None, "Rs.4500"),
                    note="Starting sum (100%) + interest (50%) = amount"))),
    ASK(Q, "a2", "Careful now. Is 4500 the starting sum, the interest, or both together?",
        "both together", ["the starting sum", "the interest"],
        "Amount means everything at the end: the starting sum and the interest together."),
    B("So 4500 is the starting sum plus half as much again. That is 150 per cent: 3 equal pieces of 50 per cent.",
      W("s2", "100% + 50% = 150%")),
    B("3 equal pieces make 4500. So one piece is 4500 divided by 3, which is 1500.",
      W("s3", "4500 ÷ 3 = 1500"), NOTE("s3", "= 1500", "50%", "below")),
    B("The starting sum is 2 of those pieces. 2 times 1500 is 3000. So 3000 rupees was put in.",
      W("s4", "2 × 1500 = 3000"), ANSWER("ans", "Sum at the start = Rs.3000"), RING("ans", "Rs.3000")),
    B("Check: 10 per cent of 3000 is 300 a year. 5 years gives 1500. And 3000 plus 1500 is 4500. It works.",
      W("c1", "10% of 3000 = 300"), W("c2", "5 × 300 = 1500"), W("c3", "3000 + 1500 = 4500")),
    B("So when you are given the amount, remember it is the starting sum and the interest together. Work out what per cent that is, then go back to 100 per cent."),
])

Q = "EXT_G5_FP_2019_004"
add(Q, [
    B("Some money earns 189 rupees of simple interest in 3 years, at 9 per cent per annum. We want that sum of money.",
      GIVEN("q", "Interest Rs.189 in 3 years at 9% per annum"), W("q2", "Sum of money = ?", label=True)),
    B("Simple interest earns the same each year. So first, the interest for just one year: 189 divided by 3 is 63.",
      W("s1", "189 ÷ 3 = 63"), NOTE("s1", "= 63", "1 year", "below"),
      FIG("years", years_table([["1", "Rs.63"], ["2", "Rs.63"], ["3", "Rs.63"]]))),
    ASK(Q, "a1", "63 rupees is one year's interest, at 9 per cent. So 63 is 9 per cent of what?",
        "of the sum we want", ["of Rs.189", "of Rs.3"],
        "The rate is always a per cent of the money at the start. So 9 per cent of the sum is 63 rupees."),
    B("9 per cent of the sum is 63. So 1 per cent is 63 divided by 9, which is 7 rupees.",
      W("s2", "9% of the sum = 63", label=True), W("s3", "63 ÷ 9 = 7"), NOTE("s3", "= 7", "1%", "below")),
    B("The whole sum is 100 per cent. 100 times 7 is 700. So the sum is 700 rupees.",
      W("s4", "100 × 7 = 700"), ANSWER("ans", "Sum of money = Rs.700"), RING("ans", "Rs.700")),
    B("Careful: the slip here is to forget the years, and treat 189 as one year's interest. Always bring it down to one year first."),
    B("Check: every 100 rupees earns 9, and 700 is 7 hundreds, so one year earns 63. 3 years earn 3 times 63, which is 189. It works.",
      W("c1", "7 × 9 = 63"), W("c2", "3 × 63 = 189")),
    B("So for the sum: interest for one year first, then 1 per cent, then 100 per cent."),
])

Q = "EXT_G5_FP_2022_005"
add(Q, [
    B("A principal, the money at the start, earns 160 rupees of simple interest in 5 years, at 8 per cent per annum. We want the principal.",
      GIVEN("q", "Interest Rs.160 in 5 years at 8% per annum"), W("q2", "Principal = ?", label=True)),
    B("Each year the principal earns 8 per cent of itself. Here are the 5 years, one at a time.",
      FIG("years", years_table([[str(i), "8%"] for i in range(1, 6)]))),
    ASK(Q, "a1", "8 per cent every year, for 5 years. So the 160 rupees is what per cent of the principal?",
        "40%", ["8%", "13%"],
        "Simple interest earns the same each year. 8 per cent, 5 times over, is 5 times 8, which is 40 per cent."),
    B("5 times 8 is 40. So 40 per cent of the principal is 160 rupees.",
      W("s1", "5 × 8% = 40%"), W("s2", "40% of the principal = 160", label=True)),
    B("40 per cent is 4 lots of 10 per cent. So 10 per cent is 160 divided by 4, which is 40 rupees.",
      W("s3", "160 ÷ 4 = 40"), NOTE("s3", "= 40", "10%", "below")),
    B("The whole principal is 100 per cent: 10 lots of 10 per cent. 10 times 40 is 400. So the principal is 400 rupees.",
      W("s4", "10 × 10% = 100%"), W("s5", "10 × 40 = 400"), ANSWER("ans", "Principal = Rs.400"), RING("ans", "Rs.400")),
    B("Careful: 160 is the interest, not the principal. The principal is the bigger sum that earned it."),
    B("Check: 8 per cent of 400 is 32 rupees a year. 5 years earn 5 times 32, which is 160. It works.",
      W("c1", "8% of 400 = 32"), W("c2", "5 × 32 = 160")),
    B("So for the principal: find what per cent the interest is altogether, then build up to 100 per cent."),
])

Q = "EXT_G5_FP_2023_019"
add(Q, [
    B("A principal, the money at the start, earns 2205 rupees of simple interest in 12 months, at 18 per cent per annum. We want the principal.",
      GIVEN("q", "Interest Rs.2205 in 12 months at 18% per annum"), W("q2", "Principal = ?", label=True)),
    ASK(Q, "a1", "The rate is per annum, which means per year. How long is 12 months?",
        "exactly 1 year", ["12 years", "half a year"],
        "A year has 12 months. So 12 months is exactly 1 year, and 2205 rupees is one year's interest."),
    B("12 months is exactly 1 year. So 2205 rupees is one year's interest, and that is 18 per cent of the principal.",
      W("s1", "18% of the principal = 2205", label=True),
      FIG("f", bars(bar([seg(1.8, "18%", "b"), seg(8.2)], None, "principal = ?"), note="The 18% piece is Rs.2205"))),
    B("Here is a neat stepping stone. 18 per cent is 9 lots of 2 per cent. So 2 per cent is 2205 divided by 9.",
      W("s2", "18% = 9 × 2%")),
    B("9 times 200 is 1800. That leaves 2205 minus 1800, which is 405. And 9 times 45 is 405. So 2205 divided by 9 is 200 and 45: that is 245.",
      W("d1", "9 × 200 = 1800"), W("d2", "2205 − 1800 = 405"), W("d3", "9 × 45 = 405"), W("d4", "2205 ÷ 9 = 245"),
      NOTE("d4", "= 245", "2%", "below")),
    B("The whole principal is 100 per cent, which is 50 lots of 2 per cent. 100 times 245 is 24500, and 50 times is half of that: 12250.",
      W("s3", "100% = 50 × 2%"), W("s4", "100 × 245 = 24500"), W("s5", "50 × 245 = 24500 ÷ 2 = 12250")),
    B("So the principal is 12250 rupees.",
      ANSWER("ans", "Principal = Rs.12250"), RING("ans", "Rs.12250")),
    B("Check: 18 per cent of 12250 should give back 2205, one year's interest. It does.",
      W("c", "18% of 12250 = 2205")),
    B("So: make sure the time is in years, then use the interest as a known per cent of the principal, and build up to 100 per cent."),
])

Q = "EXT_G5_FP_2025_026"
add(Q, [
    B("We want to earn 280 rupees of simple interest every month. The rate is 15 per cent per annum. How much must we invest?",
      GIVEN("q", "Interest Rs.280 every month at 15% per annum"), W("q2", "Amount to invest = ?", label=True)),
    ASK(Q, "a1", "The interest is given per month, but the rate is per annum, per year. What must we do first?",
        "find the interest for 1 year", ["use 280 as it is", "divide 280 by 12"],
        "The rate, 15 per cent, is for a whole year. So the interest must be for a whole year too: 12 months of 280 rupees."),
    B("Careful, that is the trap in this question. A year has 12 months, so we need 12 times 280. 10 times 280 is 2800, and 2 times 280 is 560. Together, 3360.",
      W("s1", "10 × 280 = 2800"), W("s2", "2 × 280 = 560"), W("s3", "12 × 280 = 3360"), NOTE("s3", "= 3360", "1 year", "below"),
      FIG("t", table(["Time", "Interest"], [["1 month", "Rs.280"], ["12 months", "Rs.3360"]]))),
    B("So in one year the interest is 3360 rupees. And that is 15 per cent of the money invested.",
      W("s4", "15% of the money = 3360", label=True)),
    B("15 per cent is 3 lots of 5 per cent. So 5 per cent is 3360 divided by 3, which is 1120.",
      W("s5", "3360 ÷ 3 = 1120"), NOTE("s5", "= 1120", "5%", "below")),
    B("The whole is 100 per cent, which is 20 lots of 5 per cent. 20 times 1120 is 22400. So we must invest 22400 rupees.",
      W("s6", "20 × 5% = 100%"), W("s7", "20 × 1120 = 22400"),
      ANSWER("ans", "Amount to invest = Rs.22400"), RING("ans", "Rs.22400")),
    B("Check: 10 per cent of 22400 is 2240, and 5 per cent is 1120. Together that is 3360 a year. Shared over 12 months, it is 280 a month.",
      W("c1", "2240 + 1120 = 3360"), W("c2", "3360 ÷ 12 = 280")),
    B("So match the time to the rate first: monthly interest becomes yearly interest. Then build from the known per cent up to 100 per cent."),
])
