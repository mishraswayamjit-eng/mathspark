"""Simple-interest lessons. The method throughout: find what the money earns in ONE year, then count years."""
from imported_10_lib import ANS, ASK, B, GIVEN, L, M, N, RING, W, add, f, hundreds, table, FIG

# ── Arjun's bat: interest, then the amount, then what is left ────────────────

Q = "9a285be2"
h1, h2 = hundreds(4000, 5, "a")
add(Q,
    B("Arjun puts 4000 rupees in a bank that pays 5 per cent simple interest a year, for 3 years. Then he buys a bat for 4500. We want what he has left.",
      GIVEN("q", "₹4,000 at 5% a year for 3 years. Bat costs ₹4,500.")),
    h1, h2,
    ASK(Q, "a1", "The money stays in the bank for 3 years. So what is the interest altogether?",
        "200 × 3", ["200 + 3", "just 200"],
        "Simple interest pays the same 200 rupees every single year. So 3 years means 3 lots of 200."),
    B("3 lots of 200 is 600. That is all the interest Arjun earns.",
      W("i", "200 × 3 = 600"), N("i", "= 600", "interest for 3 years")),
    B("Careful here: the bank gives back his 4000 as well as the interest. 4000 plus 600 is 4600.",
      W("t", "4,000 + 600 = 4,600"), N("t", "= 4,600", "what he has")),
    B("Now the bat. 4600 minus 4500 leaves 100 rupees.",
      ANS("ans", "4,600 − 4,500 = 100"), RING("ans", "100")),
    B("Check by going back. The bat, 4500, plus the 100 left over, is 4600. That is exactly what the bank gave him.",
      W("c", "4,500 + 100 = 4,600")),
    B("So the plan is: interest for 1 year, times the years, add it to the deposit, and only then do the shopping."),
    )

# ── Ravi and Priya: can the interests ever be equal? ─────────────────────────

Q = "9d213c43"
add(Q,
    B("Ravi deposits 4500 rupees at 6 per cent. Priya deposits 3500 at 8 per cent. We want to know when their interest will be the same.",
      GIVEN("q", "Ravi: ₹4,500 at 6%.   Priya: ₹3,500 at 8%."), L("q2", "Same interest after ? years")),
    B("Let's see what each of them earns in 1 year. Ravi first. 4500 is 45 hundreds, and each hundred earns 6 rupees. 45 times 6 is 270.",
      W("r1", "4,500 ÷ 100 = 45"), W("r2", "45 × 6 = 270"), N("r2", "= 270", "Ravi, 1 year")),
    B("Now Priya. 3500 is 35 hundreds, and each hundred earns 8 rupees. 35 times 8 is 280.",
      W("p1", "3,500 ÷ 100 = 35"), W("p2", "35 × 8 = 280"), N("p2", "= 280", "Priya, 1 year")),
    ASK(Q, "a1", "So every year Ravi gets 270 and Priya gets 280. As the years go by, what happens to the gap between them?",
        "It grows by 10 every year", ["It shrinks until they are level", "It stays at 10 for ever"],
        "Each year Priya adds 10 rupees more than Ravi does. So she is 10 ahead after 1 year, and every year after that puts another 10 on the gap.",
        W("g", "280 − 270 = 10")),
    B("Here are the first 3 years in a table. After 3 years Ravi has 810 and Priya has 840. Priya is ahead in every row.",
      FIG("t", table(["Years", "Ravi", "Priya"], [["1", "270", "280"], ["2", "540", "560"], ["3", "810", "840"]]))),
    B("They both start from 0, and Priya pulls ahead in the very first year. Ravi never catches up, so their interest can never be equal.",
      ANS("ans", "Never equal: Priya always earns more", True), RING("ans", "Never equal")),
    B("The trap is to look at only one thing. Ravi has more money in the bank, but Priya has the higher rate. Only the interest for a year settles it."),
    B("So to compare two deposits, work out 1 year for each. If one earns more every year, it stays ahead for good."),
    )

# ── Two amounts, two years apart: find the principal ─────────────────────────

Q = "a133bece"
add(Q,
    B("Some money is in a bank at simple interest. After 3 years it has become 6500 rupees, and after 5 years, 7500. We want the money first put in, and the interest after 7 years.",
      GIVEN("q", "After 3 years: ₹6,500.   After 5 years: ₹7,500.")),
    ASK(Q, "a1", "Between year 3 and year 5 the amount grew. What made it grow?",
        "2 more years of interest", ["5 more years of interest", "more money was put in"],
        "Nothing new was put in. The only thing added between year 3 and year 5 is the interest for those 2 extra years."),
    B("So 2 years of interest is 7500 minus 6500, which is 1000.",
      W("d", "7,500 − 6,500 = 1,000"), N("d", "= 1,000", "interest for 2 years")),
    B("Simple interest is the same every year. So 1 year is half of 1000, which is 500 rupees.",
      W("y", "1,000 ÷ 2 = 500"), N("y", "= 500", "interest for 1 year")),
    ASK(Q, "a2", "After 3 years the amount was 6500. How do we get back to the money first put in?",
        "take off 3 years of interest", ["take off 1 year of interest", "add 3 years of interest"],
        "The 6500 is the starting money with 3 years of interest on top. To get back to the start, peel those 3 years off."),
    B("3 years of interest is 3 times 500, which is 1500. And 6500 minus 1500 is 5000. So the principal is 5000 rupees.",
      W("i3", "500 × 3 = 1,500"), W("p", "6,500 − 1,500 = 5,000"), M("p", "5,000", "box")),
    B("Now 7 years of interest. 7 times 500 is 3500.",
      W("i7", "500 × 7 = 3,500"), ANS("ans", "Principal = ₹5,000; 7 years' interest = ₹3,500", True), RING("ans", "₹3,500")),
    B("Check with the other fact. 5 years of interest is 5 times 500, which is 2500. And 5000 plus 2500 is 7500, just as the question says.",
      W("c1", "500 × 5 = 2,500"), W("c2", "5,000 + 2,500 = 7,500")),
    B("So when you know the amount at two different times, the difference is pure interest. Find 1 year of it, then peel the interest off to reach the principal."),
    )

# ── Ananya: find the rate, then a bigger second deposit ──────────────────────

Q = "ac8c904a"
add(Q,
    B("Ananya deposits 30000 rupees for 4 years. From the interest she spends 4200 and has 1800 left. Then she deposits the 30000 and that 1800 again, at the same rate, for 3 years.",
      GIVEN("q", "₹30,000 for 4 years. Interest: ₹4,200 spent, ₹1,800 left."),
      L("q2", "Then ₹30,000 + ₹1,800 for 3 years, same rate. Interest = ?")),
    B("First, how much interest did the first deposit earn? She spent 4200 of it and still had 1800. So it was 6000 in all.",
      W("i", "4,200 + 1,800 = 6,000"), N("i", "= 6,000", "interest for 4 years")),
    B("That took 4 years, and simple interest is the same every year. 6000 divided by 4 is 1500 a year.",
      W("y", "6,000 ÷ 4 = 1,500"), N("y", "= 1,500", "interest for 1 year")),
    ASK(Q, "a1", "The rate is what every 100 rupees earns in a year. 30000 is 300 hundreds, and together they earn 1500. So what does each hundred earn?",
        "1500 ÷ 300", ["1500 × 300", "1500 ÷ 100"],
        "The 1500 rupees is shared equally among the 300 hundreds. So divide 1500 by 300.",
        W("h", "30,000 ÷ 100 = 300")),
    B("1500 divided by 300 is 5. Each hundred earns 5 rupees a year, so the rate is 5 per cent.",
      W("r", "1,500 ÷ 300 = 5"), N("r", "= 5", "rate: 5% a year")),
    B("Now the second deposit. 30000 plus 1800 is 31800. Careful: this is more money than before, so it will not earn 1500 a year any more.",
      W("p2", "30,000 + 1,800 = 31,800")),
    B("31800 is 318 hundreds, and each hundred earns 5 rupees. 318 times 5 is 1590 a year.",
      W("h2", "31,800 ÷ 100 = 318"), W("y2", "318 × 5 = 1,590"), N("y2", "= 1,590", "interest for 1 year")),
    B("And for 3 years, 1590 times 3 is 4770 rupees.",
      ANS("ans", "1,590 × 3 = 4,770"), RING("ans", "4,770")),
    B("Check another way. The 30000 alone would earn 3 times 1500, which is 4500. The extra 1800 is 18 hundreds: 18 times 5 times 3 is 270. And 4500 plus 270 is 4770.",
      W("c1", "1,500 × 3 = 4,500"), W("c2", "18 × 5 × 3 = 270"), W("c3", "4,500 + 270 = 4,770")),
    B("So first use what you know to find the rate. Then start again with the new deposit: new money, new interest for a year."),
    )

# ── Sanya's mother: from the interest back to the deposit ────────────────────

Q = "ad2aecc1"
add(Q,
    B("A bank pays 5 per cent simple interest a year. After 4 years the interest is 800 rupees. We want to know how much was deposited.",
      GIVEN("q", "5% a year for 4 years gives ₹800 interest. Deposit = ?")),
    B("The 800 came over 4 years, the same amount each year. So 1 year is 800 divided by 4, which is 200 rupees.",
      W("y", "800 ÷ 4 = 200"), N("y", "= 200", "interest for 1 year")),
    ASK(Q, "a1", "5 per cent means every 100 rupees earns 5 rupees a year. The bank paid 200 a year. So how many hundreds were deposited?",
        "200 ÷ 5", ["200 × 5", "200 ÷ 100"],
        "Each hundred brings in 5 rupees. To see how many hundreds it takes to make 200 rupees, divide 200 by 5.",
        L("m", "5% a year: every ₹100 earns ₹5")),
    B("200 divided by 5 is 40. So there were 40 hundreds in the bank, and 40 hundreds is 4000 rupees.",
      W("h", "200 ÷ 5 = 40"), N("h", "= 40", "hundreds"), ANS("ans", "40 × 100 = 4,000"), RING("ans", "4,000")),
    B("Careful not to add the interest on. 4000 plus 800 is 4800, but that is the deposit and the interest together. The question asks only for the deposit.",
      W("t", "4,000 + 800 = 4,800"), N("t", "= 4,800", "not the deposit")),
    B("Check it forwards. 5 per cent of 4000 is 200 a year, and 4 years of 200 is 800. It matches the question.",
      W("c1", "5% of 4,000 = 200"), W("c2", "200 × 4 = 800")),
    B("So to go from interest back to the deposit: find 1 year's interest, see how many hundreds earn that much, and turn the hundreds into rupees."),
    )

# ── Vikram's dad: how many years? ────────────────────────────────────────────

Q = "b1a13a45"
h1, h2 = hundreds(5000, 6, "a")
add(Q,
    B("5000 rupees goes into a bank at 6 per cent simple interest a year, and grows to 6500. We want to know how many years it stayed there.",
      GIVEN("q", "₹5,000 at 6% a year becomes ₹6,500. Years = ?")),
    ASK(Q, "a1", "How much of that 6500 is interest?",
        "6500 − 5000", ["all 6500 of it", "6500 + 5000"],
        "The 6500 is the 5000 he put in, with the interest on top. Take the 5000 away, and the interest is what is left."),
    B("6500 minus 5000 is 1500. So the bank added 1500 rupees of interest.",
      W("i", "6,500 − 5,000 = 1,500"), N("i", "= 1,500", "all the interest")),
    h1, h2,
    ASK(Q, "a2", "Each year adds 300 rupees, and the interest reached 1500. How do we find the number of years?",
        "1500 ÷ 300", ["1500 − 300", "6500 ÷ 300"],
        "We are counting how many lots of 300 fit into the 1500 of interest. That is a division: 1500 divided by 300."),
    B("300 times 5 is 1500. So it took 5 years.",
      W("m", "300 × 5 = 1,500"), ANS("ans", "1,500 ÷ 300 = 5"), RING("ans", "5")),
    B("Check from the start. 5 years of 300 is 1500, and 5000 plus 1500 is 6500. Just what the question says.",
      W("c", "5,000 + 1,500 = 6,500")),
    B("So for a how-many-years question: find the interest alone, find 1 year's interest, and divide."),
    )

# ── Riya: two banks, find the second rate ────────────────────────────────────

Q = "b47ed985"
add(Q,
    B("12000 rupees is in Bank A at 8 per cent, and 9000 rupees is in Bank B at a rate we do not know. After 5 years the two banks have paid 9300 in interest between them.",
      GIVEN("q", "Bank A: ₹12,000 at 8%.   Bank B: ₹9,000 at ?%."), L("q2", "After 5 years, interest from both = ₹9,300")),
    B("Start with Bank A, because we know everything about it. 12000 is 120 hundreds, each earning 8 rupees a year. 120 times 8 is 960.",
      W("a1", "12,000 ÷ 100 = 120"), W("a2", "120 × 8 = 960"), N("a2", "= 960", "Bank A, 1 year")),
    B("Over 5 years, Bank A pays 960 times 5, which is 4800.",
      W("a3", "960 × 5 = 4,800"), N("a3", "= 4,800", "Bank A, 5 years")),
    ASK(Q, "a1", "Both banks together paid 9300, and Bank A paid 4800 of it. So how much came from Bank B?",
        "9300 − 4800", ["9300 + 4800", "9300 ÷ 2"],
        "The 9300 is made of two parts, Bank A's and Bank B's. Take Bank A's 4800 away and Bank B's part is left."),
    B("9300 minus 4800 is 4500. Careful: that is Bank B's interest for all 5 years. For 1 year, divide by 5: 900 rupees.",
      W("b1", "9,300 − 4,800 = 4,500"), W("b2", "4,500 ÷ 5 = 900"), N("b2", "= 900", "Bank B, 1 year")),
    B("Bank B holds 9000, which is 90 hundreds. Share the 900 among 90 hundreds, and each hundred earns 10 rupees. So the rate is 10 per cent.",
      W("b3", "9,000 ÷ 100 = 90"), W("b4", "900 ÷ 90 = 10"),
      ANS("ans", "Bank B's rate = 10% a year", True), RING("ans", "10%")),
    B("Check Bank B forwards. 10 per cent of 9000 is 900 a year, so 4500 in 5 years. And 4800 plus 4500 is 9300.",
      W("c1", "10% of 9,000 = 900"), W("c2", "900 × 5 = 4,500"), W("c3", "4,800 + 4,500 = 9,300")),
    B("So with two banks, finish the one you know first. Take its interest out of the total, and what is left tells you about the other bank."),
    )

# ── Meera: equal interest from two banks ─────────────────────────────────────

Q = "b9233dff"
add(Q,
    B("Meera's 15000 rupees is split in two. 9000 goes to Bank P at 4 per cent, and the rest goes to Bank Q. After 2 years both banks have paid the same interest. We want Bank Q's rate.",
      GIVEN("q", "₹15,000: ₹9,000 in Bank P at 4%, the rest in Bank Q"), L("q2", "After 2 years: the same interest from both")),
    B("First, the rest. 15000 minus 9000 is 6000, so Bank Q holds 6000 rupees.",
      W("r", "15,000 − 9,000 = 6,000"), N("r", "= 6,000", "in Bank Q")),
    B("Now Bank P for 1 year. 9000 is 90 hundreds, each earning 4 rupees. 90 times 4 is 360.",
      W("p1", "9,000 ÷ 100 = 90"), W("p2", "90 × 4 = 360"), N("p2", "= 360", "Bank P, 1 year")),
    ASK(Q, "a1", "Both banks pay the same interest over the same 2 years. So what does Bank Q pay in 1 year?",
        "360, the same as Bank P", ["half of 360", "double 360"],
        "The totals match and the number of years match. So each single year must match too: Bank Q also pays 360 a year."),
    B("Bank Q holds 6000, which is 60 hundreds. Share the 360 among 60 hundreds, and each hundred earns 6 rupees. So Bank Q pays 6 per cent.",
      W("q1", "6,000 ÷ 100 = 60"), W("q3", "360 ÷ 60 = 6"),
      ANS("ans", "Bank Q's rate = 6% a year", True), RING("ans", "6%")),
    B("Does that make sense? Bank Q has less money but pays just as much interest. So its rate had to be higher than 4, and 6 is."),
    B("Check over the 2 years. Bank P pays 2 times 360, which is 720. Bank Q: 6 per cent of 6000 is 360 a year, so 720 as well.",
      W("c1", "360 × 2 = 720"), W("c2", "6% of 6,000 = 360")),
    B("So when two deposits earn the same interest in the same time, match them year for year, then ask what each hundred earns."),
    )

# ── Ravi's cricket gear: the interest is already given ───────────────────────

Q = "b9f2d16b"
add(Q,
    B("Ravi deposits 4500 rupees at 6 per cent a year and earns 810 rupees of interest. He takes out everything and spends 2000 on cricket gear. We want what is left.",
      GIVEN("q", "Deposit ₹4,500. Interest ₹810. Cricket gear ₹2,000.")),
    ASK(Q, "a1", "The story already tells us the interest: 810 rupees. Do we still need the 6 per cent, or the number of years?",
        "No: the interest is already known", ["Yes: work out the years first", "Yes: find 6% of 4500 first"],
        "The rate and the years are only there to find the interest. Here the story hands us the interest, 810 rupees, so that job is done."),
    B("He withdraws all of it: the money he put in, and the interest. 4500 plus 810 is 5310.",
      W("t", "4,500 + 810 = 5,310"), N("t", "= 5,310", "deposit + interest")),
    B("Then the cricket gear. 5310 minus 2000 is 3310 rupees.",
      ANS("ans", "5,310 − 2,000 = 3,310"), RING("ans", "3,310")),
    B("Careful: taking the 2000 from just the 4500 would forget the interest he earned. The interest is his money too."),
    B("Check by adding back. 3310 plus the 2000 he spent is 5310, which is what he took out of the bank.",
      W("c", "3,310 + 2,000 = 5,310")),
    B("If you are curious about the years: 45 hundreds at 6 rupees each is 270 a year, and 3 lots of 270 is 810. So it was 3 years, and the story holds together.",
      W("x1", "45 × 6 = 270"), W("x2", "270 × 3 = 810")),
    B("So read for what you are given. If the interest is already there, go straight to the amount: deposit plus interest."),
    )

# ── Deepa's mother: work backwards to the years ──────────────────────────────

Q = "bf836bd4"
h1, h2 = hundreds(1500, 10, "a")
add(Q,
    B("1500 rupees goes into a bank at 10 per cent simple interest a year. Later she takes it all out, spends 200 on decorations, and has 1600 left. How many years was it in the bank?",
      GIVEN("q", "₹1,500 at 10% a year. Spent ₹200, left with ₹1,600.")),
    ASK(Q, "a1", "Let's work backwards. Just before she spent the 200, how much did she have?",
        "1600 + 200", ["1600 − 200", "1500 + 200"],
        "She spent 200 and ended up with 1600. So just before spending, she had 200 more than 1600."),
    B("1600 plus 200 is 1800. That is what the bank gave back. Her own deposit was 1500, so the interest is 1800 minus 1500, which is 300.",
      W("t", "1,600 + 200 = 1,800"), W("i", "1,800 − 1,500 = 300"), N("i", "= 300", "all the interest")),
    h1, h2,
    B("The interest was 300, and each year brings 150. 300 is 2 lots of 150, so the money stayed for 2 years.",
      ANS("ans", "300 ÷ 150 = 2"), RING("ans", "2", 1)),
    B("Here is the trap. Forget to put the 200 back, and the interest looks like only 100, which is not even 1 full year. Always undo the spending first."),
    B("Check from the start. 1500, plus 2 years of 150, minus the 200 she spent, is 1600. It fits.",
      W("c", "1,500 + 150 × 2 − 200 = 1,600")),
    B("So when a story ends after some spending, walk backwards: undo the spending, take off the deposit, and count the years in what is left."),
    )
