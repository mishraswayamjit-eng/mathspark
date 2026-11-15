"""Hand-written lessons, part A: accounts, and finding the whole from a per cent."""
from money_percent_lib import ANSWER, ASK, B, FIG, GIVEN, MARK, NOTE, RING, W, bar, bars, lesson, seg, table

LESSONS = {}


def add(qid, beats):
    LESSONS[qid] = lesson(beats, "authored")


# ── Accounts: an entry written the opposite way round ────────────────────────

Q = "EXT_G5_WS_B2_024"
add(Q, [
    B("In this account, 600 rupees was spent. But by mistake it was entered as income, as money coming in. The balance shows 15000 rupees, and we must put it right.",
      GIVEN("q", "Spent Rs.600, but entered as income"), W("q2", "Balance shown = Rs.15000", label=True),
      W("q3", "Correct balance = ?", label=True)),
    B("Here is the 600 in a little table: what should have happened to it, and what really happened.",
      FIG("acc", table(["The Rs.600", "The balance"], [["Should be", "goes down"], ["By mistake", "went up"]]))),
    B("Spending makes a balance go down. So the 600 should have been taken away. Instead it was added, and the balance went up."),
    ASK(Q, "a1", "To put it right, how many times must we take 600 away?",
        "twice", ["once", "not at all: add 600"],
        "Taking 600 away once only removes the mistaken adding. The 600 that was really spent still has to come off after that."),
    B("First, undo the mistake. Take away the 600 that should never have been added. 15000 minus 600 is 14400.",
      W("s1", "15000 − 600 = 14400"), NOTE("s1", "− 600", "undo the mistake", "below")),
    B("Careful, here is the trap: we are not finished. 14400 is the balance before any spending. The 600 that was really spent must still come off.",
      MARK("s1", "14400")),
    B("14400 minus 600 is 13800. So the correct balance is 13800 rupees.",
      W("s2", "14400 − 600 = 13800"), NOTE("s2", "− 600", "the real spending", "below"),
      ANSWER("ans", "Correct balance = Rs.13800"), RING("ans", "Rs.13800")),
    B("Check: the mistake pushed the balance 600 the opposite way, so it is out by 2 lots of 600, which is 1200. And 15000 minus 1200 is 13800. It agrees.",
      W("c1", "2 × 600 = 1200"), W("c2", "15000 − 1200 = 13800")),
    B("So when an entry is written the opposite way round, the fix is double: once to undo it, and once to do it properly."),
])

Q = "EXT_G5_WS_B2_025"
add(Q, [
    B("This time 600 rupees came in as income. But by mistake it was written as spending. The balance shows 15000 rupees, and we must put it right.",
      GIVEN("q", "Income Rs.600, but entered as spending"), W("q2", "Balance shown = Rs.15000", label=True),
      W("q3", "Correct balance = ?", label=True)),
    B("Here is the 600 in a little table: what should have happened to it, and what really happened.",
      FIG("acc", table(["The Rs.600", "The balance"], [["Should be", "goes up"], ["By mistake", "went down"]]))),
    B("Income makes a balance go up. So the 600 should have been added. Instead it was taken away, and the balance went down."),
    ASK(Q, "a1", "So will the correct balance be more than 15000, or less?",
        "more than 15000", ["less than 15000", "exactly 15000"],
        "The 600 was money coming in, but the account treated it as money going out. So the balance shown is too small, and the correct one is bigger."),
    B("First, undo the mistake. Put back the 600 that should never have been taken away. 15000 plus 600 is 15600.",
      W("s1", "15000 + 600 = 15600"), NOTE("s1", "+ 600", "undo the mistake", "below")),
    B("Careful, here is the trap: we are not finished. 15600 is the balance before the income is counted. The 600 that really came in must still be added.",
      MARK("s1", "15600")),
    B("15600 plus 600 is 16200. So the correct balance is 16200 rupees.",
      W("s2", "15600 + 600 = 16200"), NOTE("s2", "+ 600", "the real income", "below"),
      ANSWER("ans", "Correct balance = Rs.16200"), RING("ans", "Rs.16200")),
    B("Check: the mistake pushed the balance 600 the opposite way, so it is out by 2 lots of 600, which is 1200. And 15000 plus 1200 is 16200. It agrees.",
      W("c1", "2 × 600 = 1200"), W("c2", "15000 + 1200 = 16200")),
    B("So when an entry is written the opposite way round, the fix is double: once to undo it, and once to do it properly."),
])

# ── From a per cent back to the whole ────────────────────────────────────────

Q = "EXT_G5_FP_2016_005"
add(Q, [
    B("36 is 12 per cent of some number. So we have a part, and we want the whole number.",
      GIVEN("q", "12% of the number = 36"), W("q2", "The number = ?", label=True)),
    B("Per cent means out of every 100. So the whole number is 100 per cent, and 36 is only 12 of those 100 parts.",
      W("w", "The whole number = 100%", label=True),
      FIG("f", bars(bar([seg(1.2, "12%", "b"), seg(8.8)], None, "100% = ?"), note="The 12% piece is 36"))),
    ASK(Q, "a1", "What is the easiest thing to find first?",
        "1%, by doing 36 ÷ 12", ["12% of 36", "36 × 12"],
        "We know that 12 per cent is 36. Share that 36 into 12 equal parts, and each part is 1 per cent. That is a lovely stepping stone."),
    B("12 per cent is 36. So 1 per cent is 36 divided by 12, which is 3.",
      W("s1", "36 ÷ 12 = 3"), NOTE("s1", "= 3", "1%", "below")),
    B("Careful: a common slip is to find 12 per cent of 36. But 36 is already the 12 per cent. We are climbing up to the whole, not down to a smaller part.",
      MARK("q", "36")),
    B("The whole is 100 per cent, so we need 100 lots of 3. 100 times 3 is 300.",
      W("s2", "100 × 3 = 300"), ANSWER("ans", "The number = 300"), RING("ans", "300")),
    B("Check it. 10 per cent of 300 is 30, and 1 per cent is 3. So 12 per cent is 30 plus 3 plus 3, which is 36. It works.",
      W("c1", "10% of 300 = 30"), W("c2", "12% of 300 = 30 + 3 + 3 = 36")),
    B("So when you know a per cent of a number and want the whole number, find 1 per cent first, then multiply by 100."),
])

Q = "EXT_G5_FP_2019_016"
add(Q, [
    B("40 per cent of the students passed, and 420 students did not. We want the number of students who took the exam.",
      GIVEN("q", "40% passed. 420 students did not pass."), W("q2", "All the students = ?", label=True)),
    B("All the students together are 100 per cent. Let us draw them as one bar, cut into 10 equal pieces of 10 per cent each.",
      W("w", "All the students = 100%", label=True),
      FIG("f", bars(bar([seg(1, None, "a") for _ in range(4)] + [seg(1, None, "b") for _ in range(6)], None, "100% = ?"),
                    note="4 pieces passed, 6 pieces did not"))),
    ASK(Q, "a1", "420 is the number who did not pass. What per cent of the students is that?",
        "60%", ["40%", "100%"],
        "40 per cent passed. The rest did not, and the rest is 100 minus 40, which is 60 per cent."),
    B("Careful, here is the trap. 420 is not the 40 per cent. It is the other part: 100 minus 40, which is 60 per cent.",
      W("s1", "100% − 40% = 60%"), W("s2", "60% of the students = 420", label=True)),
    B("60 per cent is 6 of our 10 pieces. So one piece is 420 divided by 6, which is 70.",
      W("s3", "420 ÷ 6 = 70"), NOTE("s3", "= 70", "10%", "below")),
    B("All the students are 10 pieces. 10 times 70 is 700.",
      W("s4", "10 × 70 = 700"), ANSWER("ans", "All the students = 700"), RING("ans", "700")),
    B("Check: one piece is 70, so the 4 pieces who passed are 280. And 700 minus 280 is 420, the ones who did not pass. It works.",
      W("c1", "4 × 70 = 280"), W("c2", "700 − 280 = 420")),
    B("So first ask: which per cent does my number really stand for? Then find one piece, and build up to the whole 100 per cent."),
])

Q = "EXT_G5_FP_2020_003"
add(Q, [
    B("20 per cent of an electricity bill is taken off, and 100 rupees is still to be paid. We want the bill before anything was taken off.",
      GIVEN("q", "20% is taken off the bill. Rs.100 is left to pay."), W("q2", "The bill = ?", label=True)),
    B("The whole bill is 100 per cent. Cut it into 5 equal pieces, and each piece is 20 per cent.",
      W("w", "5 × 20% = 100%"),
      FIG("f", bars(bar([seg(1, "20%", "b")] + [seg(1, None, "a") for _ in range(4)], None, "the bill = ?"),
                    note="1 piece is taken off, 4 pieces are left"))),
    ASK(Q, "a1", "One piece, 20 per cent, is taken off. So the 100 rupees left to pay is what per cent of the bill?",
        "80%", ["20%", "100%"],
        "100 per cent, take away 20 per cent, leaves 80 per cent. The 100 rupees is that 80 per cent."),
    B("Careful: the 100 rupees is not the whole bill, and it is not the 20 per cent either. It is the 80 per cent that is left: 4 of the 5 pieces.",
      W("s1", "100% − 20% = 80%")),
    B("4 pieces are 100 rupees. So one piece is 100 divided by 4, which is 25 rupees.",
      W("s2", "100 ÷ 4 = 25"), NOTE("s2", "= 25", "20%", "below")),
    B("The whole bill is 5 pieces. 5 times 25 is 125. So the bill was 125 rupees.",
      W("s3", "5 × 25 = 125"), ANSWER("ans", "The bill = Rs.125"), RING("ans", "Rs.125")),
    B("Check: 20 per cent of 125 is one piece, 25 rupees. And 125 minus 25 is 100, just as the question says.",
      W("c", "125 − 25 = 100")),
    B("So when a part is taken off, work out what per cent is left, find one piece, and build the whole."),
])

Q = "EXT_G5_FP_2022_015"
add(Q, [
    B("A student needs 40 per cent to pass. He scores 94 marks, and that is 74 marks short. We want the maximum marks.",
      GIVEN("q", "Pass mark = 40%. Scored 94, short by 74."), W("q2", "Maximum marks = ?", label=True)),
    ASK(Q, "a1", "He scored 94, and he was 74 marks short of passing. So what was the pass mark?",
        "94 + 74", ["94 − 74", "74"],
        "Being 74 short means he needed 74 more marks to reach the pass mark. So the pass mark is 94 plus 74."),
    B("94 plus 74 is 168. So he needed 168 marks to pass.",
      W("s1", "94 + 74 = 168"), NOTE("s1", "= 168", "pass mark", "below")),
    B("That pass mark is 40 per cent of the maximum. The maximum is the whole, 100 per cent. Picture it as 10 equal pieces of 10 per cent.",
      W("s2", "40% of the maximum = 168", label=True), W("w", "Maximum = 100%", label=True),
      FIG("f", bars(bar([seg(1, None, "b") for _ in range(4)] + [seg(1) for _ in range(6)], None, "100% = ?"),
                    note="4 pieces = 168 marks"))),
    B("40 per cent is 4 pieces. So one piece is 168 divided by 4, which is 42.",
      W("s3", "168 ÷ 4 = 42"), NOTE("s3", "= 42", "10%", "below")),
    B("The maximum is all 10 pieces. 10 times 42 is 420.",
      W("s4", "10 × 42 = 420"), ANSWER("ans", "Maximum marks = 420"), RING("ans", "420")),
    B("Check: 4 pieces of 42 make 168, the pass mark. He scored 94, and 168 minus 94 is 74. He is short by 74, as the question says.",
      W("c1", "4 × 42 = 168"), W("c2", "168 − 94 = 74")),
    B("So: first find the pass mark. Then use it as the per cent you know, and build up to the whole."),
])

Q = "EXT_G5_FP_2024_015"
add(Q, [
    B("28 per cent of a number is 196. We want 43 per cent of that same number.",
      GIVEN("q", "28% of a number = 196"), W("q2", "43% of the same number = ?", label=True),
      FIG("f", bars(bar([seg(2.8, "28% = 196", "b"), seg(7.2)], None, "the whole number"), note="We know the 28% piece. We want a 43% piece."))),
    ASK(Q, "a1", "We need a stepping stone between 28 per cent and 43 per cent. What is the handiest one?",
        "1% of the number", ["28% of 196", "43% of 196"],
        "196 is already 28 per cent of the number. Share it into 28 equal parts and each part is 1 per cent. From 1 per cent we can reach any per cent."),
    B("So how many 28s make 196? Let us try 7. 20 times 7 is 140, and 8 times 7 is 56.",
      W("s1", "20 × 7 = 140"), W("s2", "8 × 7 = 56")),
    B("140 plus 56 is 196. It fits exactly. So 1 per cent of the number is 7.",
      W("s3", "140 + 56 = 196"), W("s4", "196 ÷ 28 = 7"), NOTE("s4", "= 7", "1%", "below")),
    B("Careful: do not take 43 per cent of 196. 196 is only a part of the number, not the number itself.",
      MARK("q", "196")),
    B("43 per cent is 43 lots of 1 per cent. 40 times 7 is 280, and 3 times 7 is 21. Together, 301.",
      W("s5", "40 × 7 = 280"), W("s6", "3 × 7 = 21"), W("s7", "43 × 7 = 280 + 21 = 301")),
    B("So 43 per cent of the number is 301.",
      ANSWER("ans", "43% of the number = 301"), RING("ans", "301")),
    B("Check: the whole number is 100 times 7, which is 700. Half of 700 is 350, and 43 per cent should be a bit less than half. 301 is. Sensible.",
      W("c1", "100 × 7 = 700"), W("c2", "700 ÷ 2 = 350")),
    B("So to go from one per cent of a number to another, drop down to 1 per cent, then climb back up."),
])
