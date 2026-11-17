"""One-off stories: tickets, villages, shopkeepers, a corrected total, pooled money, and two averages."""
from imported_10_lib import ANS, ASK, B, FIG, GIVEN, L, M, N, RING, S, W, add, bar, bars, f, table, take

# ── Tickets sold and refunded, ₹50 donated for each one used ─────────────────

Q = "074fe35c"
sub = take(Q, 13575, 764, "used", "A refunded ticket was not used, so it comes off.",
           extra=[N("used", "= 12,811", "tickets used")])
add(Q,
    B("A tournament ran for 3 days. Each day some tickets were sold and some were refunded. For every ticket really used, 50 rupees goes to charity. We want the donation.",
      GIVEN("q", "₹50 donated for every ticket used (sold − refunded)"),
      FIG("t", table(["Day", "Sold", "Refunded"], [["1", "4,768", "235"], ["2", "3,594", "187"], ["3", "5,213", "342"]]))),
    ASK(Q, "a1", "The question also says each ticket costs 125 rupees. Do we need that 125 to find the donation?",
        "No: the donation is ₹50 a ticket", ["Yes: multiply the tickets by 125", "Yes: add 125 and 50"],
        "The 125 is what people paid for a ticket. The charity gets 50 rupees for each ticket used, so the 125 is only there to distract us."),
    B("Add up the tickets sold. 4768 plus 3594 is 8362, and 5213 more makes 13575.",
      W("s1", "4,768 + 3,594 = 8,362"), W("s2", "8,362 + 5,213 = 13,575"), N("s2", "= 13,575", "sold")),
    B("Now the refunds. 235 plus 187 is 422, and 342 more makes 764.",
      W("r1", "235 + 187 = 422"), W("r2", "422 + 342 = 764"), N("r2", "= 764", "refunded")),
    sub[0],
    ASK(Q, "a2", "Now 12811 tickets at 50 rupees each. 50 is 5 tens. So what is an easy way to multiply by 50?",
        "× 5, then × 10", ["× 5, then + 10", "× 5 and stop"],
        "50 is 5 times 10. So multiply by 5 first, and then by 10, which just puts a zero on the end."),
    B("12811 times 5 is 64055. Times 10 puts a zero on the end: 640550. So the donation is 640550 rupees.",
      W("m1", "12,811 × 5 = 64,055"), W("m2", "64,055 × 10 = 6,40,550"),
      ANS("ans", "12,811 × 50 = 6,40,550"), RING("ans", "6,40,550")),
    B("Check the used tickets day by day: 4533, 3407 and 4871. Add those and we get 12811 again, so the count is right.",
      W("c1", "4,768 − 235 = 4,533"), W("c2", "3,594 − 187 = 3,407"), W("c3", "5,213 − 342 = 4,871"),
      W("c4", "4,533 + 3,407 + 4,871 = 12,811")),
    B("So pick out the numbers the question really uses: tickets sold, minus tickets refunded, times the donation for each."),
    )

# ── Three villages collecting rice ───────────────────────────────────────────

Q = "170dc4d7"
sub = take(Q, 2106, 389, "vb", "So the spoiled rice comes off.", extra=[N("vb", "= 1,717", "Village B")])
add(Q,
    B("Village A collected 1275 kilograms of rice and then 1548. Village B collected 2106 but returned 389 that was spoiled. Village C collected as much as A and B combined. How much altogether?",
      GIVEN("q", "A: 1,275 + 1,548.   B: 2,106 − 389.   C = A + B.")),
    B("Village A first. 1275 plus 1548 is 2823 kilograms.",
      W("va", "1,275 + 1,548 = 2,823"), N("va", "= 2,823", "Village A")),
    ASK(Q, "a1", "Village B collected 2106 kilograms but returned 389 of spoiled rice. What is Village B's real collection?",
        "2106 − 389", ["2106 + 389", "just 2106"],
        "Rice that was returned is no longer part of the collection. So it comes off: 2106 minus 389."),
    sub[0],
    B("Village C collected as much as A and B combined. 2823 plus 1717 is 4540. So Village C has 4540 kilograms.",
      W("vc", "2,823 + 1,717 = 4,540"), N("vc", "= 4,540", "A + B, and also C"),
      FIG("bars", bars(bar([(6.2, "A: 2,823", "a"), (3.8, "B: 1,717", "b")]), bar([(10, "C: 4,540", "c")])))),
    ASK(Q, "a2", "Look at the two bars. A and B together make 4540, and C is 4540 on its own. So what do all three villages make?",
        "2 lots of 4540", ["just 4540", "4540 + 2823"],
        "The top bar is A and B, and that is 4540. The bottom bar is C, another 4540. Altogether that is 2 lots of 4540."),
    B("4540 plus 4540 is 9080. All three villages collected 9080 kilograms.",
      ANS("ans", "4,540 + 4,540 = 9,080"), RING("ans", "9,080")),
    B("The trap is to stop at 4540. That is only Village C, or only A and B. The question asks for all three villages."),
    B("Check by adding the three villages one by one. 2823 plus 1717 plus 4540 is 9080 again.",
      W("c", "2,823 + 1,717 + 4,540 = 9,080")),
    B("So work out each village's real amount first. And when one part equals the rest put together, the whole is double that."),
    )

# ── Four shopkeepers: top two minus bottom two ───────────────────────────────

Q = "49848a61"
sub = take(Q, 987973, 687533, "ans",
           "Now the difference between those two totals. No borrowing is needed here, so go column by column.", "answer")
add(Q,
    B("4 shopkeepers counted their Diwali sales. They donate the difference between the top 2 earners' total and the bottom 2 earners' total. We want that donation.",
      GIVEN("q", "Donation = (top 2 added) − (bottom 2 added)"),
      FIG("t", table(["Shopkeeper", "Earned (₹)"], [["Ravi", "4,75,628"], ["Meena", "3,89,457"], ["Kiran", "5,12,345"], ["Priya", "2,98,076"]]))),
    ASK(Q, "a1", "First we must rank them. Who are the 2 highest earners?",
        "Kiran and Ravi", ["Ravi and Meena", "Kiran and Priya"],
        "Compare the lakhs first. Kiran has 5 lakhs and Ravi has 4 lakhs. Meena has 3 lakhs and Priya has only 2."),
    B("So the top 2 are Kiran and Ravi. Add their earnings: 512345 plus 475628 is 987973.",
      W("top", "5,12,345 + 4,75,628 = 9,87,973"), N("top", "= 9,87,973", "top 2")),
    B("The bottom 2 are Meena and Priya. 389457 plus 298076 is 687533.",
      W("bot", "3,89,457 + 2,98,076 = 6,87,533"), N("bot", "= 6,87,533", "bottom 2")),
    sub[0],
    B("So they donated 300440 rupees.", RING("ans", "= 3,00,440")),
    B("Careful: it is not the highest earner minus the lowest. Each pair is added first, and only then do we subtract."),
    B("Check by adding back. 687533 plus 300440 is 987973, the top 2 total.",
      W("c", "6,87,533 + 3,00,440 = 9,87,973")),
    B("So read the instruction in order: rank, add each pair, then find the difference."),
    )

# ── The corrected total ──────────────────────────────────────────────────────

Q = "555fbc6a"
add(Q,
    B("4 teams collected money, and the recorded total was 50000 rupees. Then it turned out that Team C really collected 1250 more than was recorded. We want the correct total.",
      GIVEN("q", "Recorded total = ₹50,000.  Team C: ₹1,250 more."), L("q2", "Correct total = ?")),
    ASK(Q, "a1", "We are not told Team C's amount. Do we have to work it out before we can fix the total?",
        "No: only the change matters", ["Yes: nothing works without it"],
        "Look at what the question asks for: the total, not Team C's amount. And we already have a total. It only needs correcting."),
    B("Here is why. The total is just the 4 amounts added together. If one of them changes and the other 3 stay put, the total changes by exactly the same amount."),
    ASK(Q, "a2", "Team C's real amount is 1250 more than recorded, and the other 3 teams stay the same. What happens to the total?",
        "It goes up by 1250", ["It goes down by 1250", "It stays at 50000"],
        "One of the 4 amounts has grown by 1250 and nothing else has changed. So the total grows by 1250 as well.",
        M("q", "₹1,250 more")),
    B("So the correct total is 50000 plus 1250, which is 51250 rupees.",
      ANS("ans", "50,000 + 1,250 = 51,250"), RING("ans", "51,250")),
    B("Let's check the long way. Teams A, B and D collected 12475, 8963 and 15208, which is 36646 together. So Team C was recorded as 50000 minus 36646, which is 13354.",
      W("c1", "12,475 + 8,963 + 15,208 = 36,646"), W("c2", "50,000 − 36,646 = 13,354"), N("c2", "= 13,354", "Team C, recorded")),
    B("Team C's real amount is 13354 plus 1250, which is 14604. And 36646 plus 14604 is 51250. The short way and the long way agree.",
      W("c3", "13,354 + 1,250 = 14,604"), W("c4", "36,646 + 14,604 = 51,250")),
    B("Careful with the word more. More than recorded pushes the total up, not down, and it pushes it up only once."),
    B("So when one part of a total is corrected, you do not need to rebuild everything. Just move the total by the same amount."),
    )

# ── Shopkeeper C: find the amount, then test a claim ─────────────────────────

Q = "6ad2d1b7"
sub1 = take(Q, 52000, 36775, "c", "What is left of the 52000 belongs to C.", extra=[M("c", "= 15,225", "box")])
sub2 = take(Q, 21435, 1275, "claim", "Now test the claim. A plus B is the 21435 we already found.",
            extra=[N("claim", "= 20,160", "what the claim says")])
add(Q,
    B("4 shopkeepers collected 52000 rupees in all. A collected 12475, B collected 8960 and D collected 15340. Someone says C collected exactly A plus B, minus 1275. We must find C, and test that claim.",
      GIVEN("q", "A = 12,475.  B = 8,960.  C = ?  D = 15,340."), L("q2", "Total = 52,000.  Claim: C = A + B − 1,275")),
    ASK(Q, "a1", "There are two statements about C: the total, and the claim. Which one do we use to find what C really collected?",
        "52,000 − (A + B + D)", ["A + B − 1,275", "52,000 − (A + B)"],
        "The total of 52000 is a fact. The other statement is only something they noticed, and we are asked to test it. So use the total, and take away A, B and D."),
    B("Add A, B and D. 12475 plus 8960 is 21435, and 15340 more makes 36775.",
      W("s1", "12,475 + 8,960 = 21,435"), W("s2", "21,435 + 15,340 = 36,775"), N("s2", "= 36,775", "A + B + D")),
    sub1[0],
    sub2[0],
    ASK(Q, "a2", "C really collected 15225. The claim says 20160. So is the observation correct?",
        "No: the two amounts differ", ["Yes: they are the same"],
        "Put the two numbers side by side: 15225 and 20160. They are not equal, so the observation does not hold."),
    B("15225 is not equal to 20160. So C collected 15225 rupees, and the observation is not correct.",
      W("ne", "15,225 ≠ 20,160"), ANS("ans", "C = ₹15,225; the observation is not correct", True), RING("ans", "₹15,225")),
    B("Check C against the total. 12475, 8960, 15225 and 15340 add up to 52000 exactly.",
      W("ch", "12,475 + 8,960 + 15,225 + 15,340 = 52,000")),
    B("So keep facts and claims apart. Find the answer from the facts, then hold the claim up against it."),
    )

# ── Did father add correctly? ────────────────────────────────────────────────

Q = "853202d9"
add(Q,
    B("Ravi's family spent 2475 on firecrackers, 1368 on sweets and 957 on clothes. Father says that makes 5000 in all. Ravi is not so sure. What is the real total?",
      GIVEN("q", "₹2,475 + ₹1,368 + ₹957 = ?"), L("q2", "Father says: ₹5,000")),
    ASK(Q, "a1", "Father says 5000. How can we find out whether he is right?",
        "Add the 3 amounts ourselves", ["Take his word for it", "Take 957 away from 5000"],
        "A total that someone tells you is only a claim. The real total comes from adding the 3 amounts ourselves."),
    B("Start with the first two. 2475 plus 1368 is 3843.",
      W("s1", "2,475 + 1,368 = 3,843")),
    B("Careful: we are not finished. 3843 covers only the firecrackers and the sweets. The clothes still have to go on.",
      M("s1", "3,843"), M("q", "₹957", "circle")),
    B("3843 plus 957. Look at the ends of the two numbers: 43 and 57 make exactly 100. Then 3800 plus 900 plus that 100 is 4800.",
      W("e", "43 + 57 = 100"), W("h", "3,800 + 900 + 100 = 4,800")),
    B("So the real total is 4800 rupees.",
      ANS("ans", "3,843 + 957 = 4,800"), RING("ans", "4,800")),
    B("Ravi was right to doubt. Father's 5000 is 200 too much. It was a rough guess, not a sum.",
      W("d", "5,000 − 4,800 = 200"), S("q2", "₹5,000", "200 too much")),
    B("Check by taking the clothes off again. 4800 minus 957 is 3843, the total of the first two.",
      W("c", "4,800 − 957 = 3,843")),
    B("So add in steps, look for ends that make a round 100, and never stop before the last amount is in."),
    )

# ── Four families pool money and share what is left ──────────────────────────

Q = "f35bf34f"
sub = take(Q, 16400, 13775, "left", "So take the spending out of the pool.", extra=[N("left", "= 2,625", "left over")])
add(Q,
    B("4 families pooled their money, spent 9625 on firecrackers and 4150 on sweets, and shared what was left equally. We want each family's share.",
      GIVEN("q", "Spent ₹9,625 and ₹4,150. The rest is shared by 4."),
      FIG("t", table(["Family", "Gave (₹)"], [["Sharma", "4,375"], ["Gupta", "3,948"], ["Patel", "5,217"], ["Mehta", "2,860"]]))),
    B("First the pool. 4375 plus 3948 is 8323. Then 5217 more makes 13540, and 2860 more makes 16400.",
      W("p1", "4,375 + 3,948 = 8,323"), W("p2", "8,323 + 5,217 = 13,540"), W("p3", "13,540 + 2,860 = 16,400"),
      N("p3", "= 16,400", "collected")),
    B("Next, the spending. 9625 plus 4150 is 13775.",
      W("sp", "9,625 + 4,150 = 13,775"), N("sp", "= 13,775", "spent")),
    ASK(Q, "a1", "The families share money equally among the 4 of them. Which amount gets shared?",
        "what is left after the spending", ["all the money collected", "the money that was spent"],
        "The story says they share the remaining money. So first take the spending out of the pool, and share only what is left."),
    sub[0],
    ASK(Q, "a2", "Careful: 2625 is for all 4 families together. Dividing by 4 can be done in 2 easy steps. Which?",
        "halve it, then halve again", ["halve it once", "take away 4"],
        "Half of a half is a quarter. So to divide by 4, cut the amount in half, and then cut that half in half."),
    B("Half of 2625 is 1312.5. Half of that is 656.25. So each family gets back 656.25 rupees.",
      W("h1", "2,625 ÷ 2 = 1,312.5"), W("h2", "1,312.5 ÷ 2 = 656.25"),
      ANS("ans", "2,625 ÷ 4 = 656.25"), RING("ans", "656.25")),
    B("Check by multiplying. 656.25 times 4 is 2625, all the money that was left.",
      W("c", "656.25 × 4 = 2,625")),
    B("So: total the pool, total the spending, subtract, and only then share. And an equal share does not have to be a whole number."),
    )

# ── Averages: Arjun's sixth innings ──────────────────────────────────────────

Q = "11110146"
add(Q,
    B("After 5 innings Arjun's average is 40.5 runs, though one of his 5 scores is hidden. After a 6th innings his average drops by 2.75. We want the 6th score.",
      GIVEN("q", "5 innings: average 40.5.   6 innings: average drops 2.75"), L("q2", "6th innings = ?")),
    ASK(Q, "a1", "One of the first 5 scores is unknown. Do we have to find it before we can go on?",
        "No: the average gives the total", ["Yes: nothing works without it", "Yes: it must be 40.5"],
        "An average times the number of innings gives the total of all of them, the hidden score included. So we can get the total without it."),
    B("Total for 5 innings is 40.5 times 5. Do it in two bits: 40 times 5 is 200, and 0.5 times 5 is 2.5. Together, 202.5 runs.",
      W("t1", "40 × 5 = 200"), W("t2", "0.5 × 5 = 2.5"), W("t5", "40.5 × 5 = 202.5"), N("t5", "= 202.5", "5 innings")),
    B("Now the new average. It dropped by 2.75, so it is 40.5 minus 2.75, which is 37.75.",
      W("na", "40.5 − 2.75 = 37.75"), N("na", "= 37.75", "new average")),
    ASK(Q, "a2", "That new average of 37.75 is spread over how many innings?",
        "6", ["5", "1"],
        "The new average is worked out after the 6th innings. So it covers all 6 innings, the old 5 and the new one."),
    B("Total for 6 innings is 37.75 times 6. 37 times 6 is 222, and 0.75 times 6 is 4.5. Together, 226.5 runs.",
      W("u1", "37 × 6 = 222"), W("u2", "0.75 × 6 = 4.5"), W("t6", "37.75 × 6 = 226.5"), N("t6", "= 226.5", "6 innings")),
    B("The 6th innings is the only difference between those two totals. 226.5 minus 202.5 is 24. Arjun scored 24 runs.",
      ANS("ans", "226.5 − 202.5 = 24"), RING("ans", "24")),
    B("Does 24 make sense? Yes. It is well below his average of 40.5, and a low score is exactly what pulls an average down."),
    B("Check: the 6 innings add up to 202.5 plus 24, which is 226.5. Divide by 6 and we get 37.75, the new average.",
      W("c", "(202.5 + 24) ÷ 6 = 37.75")),
    B("So with averages, think in totals. Average times how many gives the total, and the new score is the new total minus the old one."),
    )

# ── Averages: a score corrected afterwards ───────────────────────────────────

Q = "59dc509c"
add(Q,
    B("After 5 matches Arjun's average is 34.6 runs. Then the scorer finds that his 3rd match score should have been 2.5 runs higher. We want the corrected average for the 5 matches.",
      GIVEN("q", "5 matches: average 34.6.   One score is 2.5 too low."), L("q2", "Corrected average = ?")),
    ASK(Q, "a1", "The story gives two averages: 32.75 after 4 matches, and 34.6 after 5. Which one do we need?",
        "34.6, for all 5 matches", ["32.75, for 4 matches", "both, added together"],
        "We want the average across all 5 matches. The 34.6 already covers all 5 of them, so the 32.75 is not needed at all."),
    B("An average times the number of matches gives the total. 34 times 5 is 170, and 0.6 times 5 is 3. So the recorded total is 173 runs.",
      W("t1", "34 × 5 = 170"), W("t2", "0.6 × 5 = 3"), W("t", "34.6 × 5 = 173"), N("t", "= 173", "recorded total")),
    B("The 3rd match score goes up by 2.5, and nothing else changes. So the total goes up by 2.5 as well: 175.5.",
      W("ct", "173 + 2.5 = 175.5"), N("ct", "= 175.5", "corrected total")),
    ASK(Q, "a2", "The total went up by 2.5. What happens to the average of the 5 matches?",
        "It goes up by 2.5 ÷ 5", ["It goes up by 2.5", "It stays at 34.6"],
        "The extra 2.5 runs are shared out over all 5 matches. So the average rises by only a fifth of 2.5, not by the whole 2.5."),
    B("Divide the corrected total by 5. 175 divided by 5 is 35, and 0.5 divided by 5 is 0.1. So the corrected average is 35.1.",
      W("d1", "175 ÷ 5 = 35"), W("d2", "0.5 ÷ 5 = 0.1"), ANS("ans", "175.5 ÷ 5 = 35.1"), RING("ans", "35.1")),
    B("Check with the shortcut. The extra 2.5 runs shared over 5 matches is 0.5 each. And 34.6 plus 0.5 is 35.1. Same answer.",
      W("c1", "2.5 ÷ 5 = 0.5"), W("c2", "34.6 + 0.5 = 35.1")),
    B("So when a score is corrected, fix the total first and divide again. A change to one score is shared out across every match."),
    )
