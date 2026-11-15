"""Hand-written lessons, part B: per cent questions from past papers."""
from money_percent_lib import ANSWER, ASK, B, FIG, GIVEN, MARK, NOTE, RING, W, bar, bars, lesson, seg, table

LESSONS = {}


def add(qid, beats):
    LESSONS[qid] = lesson(beats, "authored")


def price_bars(top, bottom, top_label, bottom_label, gap_label, gap=2.0):
    """A price and a lower price underneath it, with the gap named."""
    return bars(bar([seg(10 - gap, None, "a"), seg(gap, gap_label, "b")], top, top_label),
                bar([seg(10 - gap, bottom_label, "a")], bottom))


def ten_pieces(shaded, brace, note, label=None, tone="b"):
    """A whole cut into 10 equal pieces of 10% each, with some shaded."""
    return bars(bar([seg(1, label if i == 0 else None, tone) if i < shaded else seg(1) for i in range(10)], None, brace), note=note)


Q = "EXT_G5_FP_2016_032"
add(Q, [
    B("A shirt priced at 700 rupees is sold for 651 rupees in a sale. We want the discount as a per cent.",
      GIVEN("q", "Price Rs.700, sold for Rs.651"), W("q2", "Discount = ? %", label=True)),
    B("Two bars. The top is the price on the shirt, 700 rupees. The bottom is what it sold for, 651. The gap between them is the discount.",
      FIG("f", price_bars("Price", "Sale price", "Rs.700", "Rs.651", "discount ?", 1.2))),
    B("First the discount in rupees. 700 minus 651 is 49.",
      W("s1", "700 − 651 = 49"), NOTE("s1", "= 49", "discount", "below")),
    ASK(Q, "a1", "Now we need 49 rupees as a per cent. A per cent of which amount?",
        "of Rs.700, the price", ["of Rs.651, the sale price", "of Rs.49"],
        "A discount is always measured against the price before the sale. That is the 700 rupees."),
    B("Careful, this is the trap. The per cent is taken on the 700, the starting price, never on the 651.",
      MARK("q", "Rs.700", "box")),
    B("Per cent means out of every 100, and 700 is 7 hundreds. So share the 49 rupees over the 7 hundreds: 49 divided by 7 is 7.",
      W("s2", "700 ÷ 100 = 7"), W("s3", "49 ÷ 7 = 7")),
    B("So every 100 rupees of price gets 7 rupees off. That is a discount of 7 per cent.",
      ANSWER("ans", "Discount = 7%"), RING("ans", "7%")),
    B("Check: 1 per cent of 700 is 7, so 7 per cent is 7 times 7, which is 49. That is our discount.",
      W("c", "7% of 700 = 7 × 7 = 49")),
    B("So for a discount per cent: find the rupees off, then ask how many that is for every 100 of the starting price."),
])

Q = "EXT_G5_FP_2017_012"
add(Q, [
    B("Last month a clock cost 10800 rupees. This month the price has dropped to 8640 rupees. We want the discount as a per cent.",
      GIVEN("q", "Old price Rs.10800, new price Rs.8640"), W("q2", "Discount = ? %", label=True)),
    B("Two bars: last month's price on top, and this month's price underneath. The gap is how much the price dropped.",
      FIG("f", price_bars("Old price", "New price", "Rs.10800", "Rs.8640", "drop ?"))),
    B("First the drop in rupees. 10800 minus 8640 is 2160.",
      W("s1", "10800 − 8640 = 2160"), NOTE("s1", "= 2160", "the drop", "below")),
    ASK(Q, "a1", "The drop is 2160 rupees. To make it a per cent, which price do we compare it with?",
        "the old price, Rs.10800", ["the new price, Rs.8640", "the drop itself"],
        "A price cut is always measured against the price before the cut. That is the old price, 10800."),
    B("Now use our friendly 10 per cent. 10 per cent of 10800 is 10800 divided by 10, which is 1080.",
      W("s2", "10% of 10800 = 1080")),
    B("Look: 1080 and 1080 make 2160. So the drop is 2 lots of 10 per cent. That is 20 per cent.",
      W("s3", "2 × 1080 = 2160"), W("s4", "2 × 10% = 20%"),
      ANSWER("ans", "Discount = 20%"), RING("ans", "20%")),
    B("Check: 20 per cent of 10800 is 2160, and taking 2160 off 10800 gives 8640, this month's price.",
      W("c", "10800 − 20% of 10800 = 8640")),
    B("So for a per cent drop: find the drop in rupees, then see how many 10 per cents of the old price fit into it."),
])

Q = "EXT_G5_FP_2017_021"
add(Q, [
    B("In 1976 there were about 250000 lions in Africa. Since then the number has gone down by 90 per cent. How many lions are there now?",
      GIVEN("q", "250000 lions in 1976. Decreased by 90%."), W("q2", "Lions now = ?", label=True)),
    B("All the lions of 1976 are 100 per cent. Draw them as a bar of 10 equal pieces, 10 per cent each.",
      W("w", "Lions in 1976 = 100%", label=True),
      FIG("f", bars(bar([seg(1, None, "a") for _ in range(9)] + [seg(1, "left", "b")], None, "250000 lions"),
                    note="9 pieces are gone: that is 90%"))),
    ASK(Q, "a1", "90 per cent of the lions are gone. What per cent are still there?",
        "10%", ["90%", "100%"],
        "The whole is 100 per cent. Take away the 90 per cent that are gone, and 10 per cent are left."),
    B("100 minus 90 is 10. Careful: the question asks for the lions that are left, the 10 per cent, not the lions that are gone.",
      W("s1", "100% − 90% = 10%")),
    B("10 per cent is one tenth, so we divide by 10. 250000 divided by 10 is 25000.",
      W("s2", "10% of 250000 = 250000 ÷ 10 = 25000")),
    B("So about 25000 lions are left.",
      ANSWER("ans", "Lions now = 25000"), RING("ans", "25000")),
    B("Check: the lions that are gone are 250000 minus 25000, which is 225000. That is 9 pieces of 25000, the 90 per cent. It fits.",
      W("c1", "250000 − 25000 = 225000"), W("c2", "9 × 25000 = 225000")),
    B("So when something goes down by a per cent, find what per cent is left, and take that per cent of the starting number."),
])

Q = "EXT_G5_FP_2018_012"
add(Q, [
    B("Sachin has played 500 games and won 49 per cent of them. From now on he wins every game. How many more wins take him to 50 per cent?",
      GIVEN("q", "500 games played, 49% won. Then wins every game."), W("q2", "Extra wins to reach 50% = ?", label=True)),
    B("First, how many has he won so far? 1 per cent of 500 is 5. And 49 per cent is one 5 less than 50 lots of 5: 250 minus 5, which is 245.",
      W("s1", "1% of 500 = 5"), W("s2", "50 × 5 = 250"), W("s3", "49% of 500 = 250 − 5 = 245")),
    B("So he has 245 wins out of 500 games. For 50 per cent, his wins must be exactly half of his games.",
      FIG("t", table(["When", "Wins", "Games"], [["Now", "245", "500"], ["Later", "?", "?"]]))),
    ASK(Q, "a1", "Half of 500 is 250, and he has 245. So are 5 more wins enough?",
        "No: the games go up too", ["Yes: 245 + 5 = 250"],
        "Every extra win is also an extra game played. So the total does not stay at 500, and the halfway mark keeps moving."),
    B("That is the trap. Try 5 more: he has 250 wins, but out of 505 games. Double 250 is only 500, not 505. So not quite half yet.",
      W("t1", "245 + 5 = 250"), W("t2", "500 + 5 = 505"), W("t3", "2 × 250 = 500")),
    B("Here is a neat way to see it. Right now his losses are 500 minus 245, which is 255. He never loses again, so the losses stay at 255.",
      W("l", "500 − 245 = 255"), NOTE("l", "= 255", "losses", "below")),
    B("At 50 per cent, wins and losses are equal. So he needs 255 wins. He has 245, so he needs 255 minus 245: 10 more.",
      W("n", "255 − 245 = 10"), ANSWER("ans", "Extra wins = 10"), RING("ans", "10")),
    B("Check: 10 more wins gives 255 wins out of 510 games, and 255 is exactly half of 510. That is 50 per cent!",
      W("c1", "500 + 10 = 510"), W("c2", "2 × 255 = 510"),
      FIG("t", table(["When", "Wins", "Games"], [["Now", "245", "500"], ["Later", "255", "510"]], highlight=["r1"]))),
    B("So when a total keeps growing, look for the part that stays still. Here it was the losses."),
])

Q = "EXT_G5_FP_2018_030"
add(Q, [
    B("An article is priced at 800 rupees, and it is sold at a discount of 20 per cent. We want the sale price.",
      GIVEN("q", "Price Rs.800. Discount 20%."), W("q2", "Sale price = ?", label=True)),
    B("A discount is money taken off the price. So the sale price is the shorter bar, and the gap between the two is the discount.",
      FIG("f", price_bars("Price", "Sale price", "Rs.800", "?", "discount ?"))),
    ASK(Q, "a1", "First we need the discount in rupees. It is 20 per cent of what?",
        "of the price, Rs.800", ["of the sale price", "of the discount"],
        "The discount is taken off the price on the article. So it is 20 per cent of 800."),
    B("10 per cent of 800 is 80. So 20 per cent is 2 times 80, which is 160. The discount is 160 rupees.",
      W("s1", "10% of 800 = 800 ÷ 10 = 80"), W("s2", "20% of 800 = 2 × 80 = 160"), NOTE("s2", "= 160", "discount", "below")),
    ASK(Q, "a2", "Is 160 the sale price?",
        "No: take it away from 800", ["Yes, 160 is the sale price", "No: add it to 800"],
        "160 rupees is what comes off. The sale price is what is left of the 800 after the discount is taken away."),
    B("800 minus 160 is 640. So the sale price is 640 rupees.",
      W("s3", "800 − 160 = 640"), ANSWER("ans", "Sale price = Rs.640"), RING("ans", "Rs.640"),
      FIG("f", price_bars("Price", "Sale price", "Rs.800", "Rs.640", "Rs.160"))),
    B("Check it another way. With 20 per cent off, you pay the other 80 per cent. That is 8 lots of 80, which is 640. Same answer.",
      W("c", "80% of 800 = 8 × 80 = 640")),
    B("So for a discount: find the per cent of the price, then take it away."),
])

Q = "EXT_G5_FP_2018_035"
add(Q, [
    B("There are 5 tests, each out of 80 marks. A student has 30 per cent on the first 4. He wants 35 per cent over all 5. What must he score in the 5th test?",
      GIVEN("q", "5 tests of 80 marks. 30% in the first 4."), W("q2", "Marks in test 5, for 35% overall = ?", label=True)),
    B("Lots of numbers, so let us put them in a table. We need the marks he has from the first 4 tests, and the marks he wants from all 5.",
      FIG("t", table(["Tests", "Out of", "Per cent", "Marks"], [["First 4", "?", "30%", "?"], ["All 5", "?", "35%", "?"]]))),
    B("All 5 tests are out of 5 times 80, which is 400 marks. The first 4 tests are out of 4 times 80, which is 320.",
      W("s1", "5 × 80 = 400"), W("s2", "4 × 80 = 320")),
    B("He wants 35 per cent of 400. Per cent means out of every 100, and 400 is 4 hundreds. 4 times 35 is 140 marks.",
      W("pc", "35% = 35 out of every 100", label=True), W("s3", "35% of 400 = 4 × 35 = 140"), NOTE("s3", "= 140", "target", "below")),
    ASK(Q, "a1", "Now the marks he already has. He scored 30 per cent, but of which total?",
        "of 320, the first 4 tests", ["of 400, all 5 tests", "of 80, one test"],
        "He scored 30 per cent in the first 4 tests only. Those 4 tests are out of 320 marks."),
    B("10 per cent of 320 is 32. So 30 per cent is 3 times 32, which is 96. He has 96 marks so far.",
      W("s4", "10% of 320 = 32"), W("s5", "30% of 320 = 3 × 32 = 96")),
    B("He needs 140 and he has 96. The 5th test must give the difference: 140 minus 96 is 44.",
      W("s6", "140 − 96 = 44"), ANSWER("ans", "Marks in test 5 = 44"), RING("ans", "44"),
      FIG("t", table(["Tests", "Out of", "Per cent", "Marks"], [["First 4", "320", "30%", "96"], ["All 5", "400", "35%", "140"]]))),
    B("Check: 96 plus 44 is 140, and 140 out of 400 is 35 for every 100. That is 35 per cent.",
      W("c", "96 + 44 = 140")),
    B("So for a target per cent: find the marks needed in total, find the marks already scored, and subtract."),
])

Q = "EXT_G5_FP_2019_025"
add(Q, [
    B("A student scored 72 per cent on a test of 25 questions. We want the number of answers that were not correct.",
      GIVEN("q", "25 questions. Scored 72%."), W("q2", "Answers not correct = ?", label=True)),
    B("72 per cent means 72 right out of every 100. But this test has only 25 questions, and 25 is one quarter of 100.",
      W("pc", "72% = 72 out of every 100", label=True), W("s1", "4 × 25 = 100")),
    ASK(Q, "a1", "100 questions would give 72 right. This test is a quarter of that size. So how many did he get right?",
        "72 ÷ 4", ["72 × 4", "72 − 25"],
        "A quarter of the questions means a quarter of the right answers. And to find a quarter, we divide by 4."),
    B("To divide by 4, halve and halve again. Half of 72 is 36, and half of 36 is 18. So he got 18 answers right.",
      W("s2", "72 ÷ 2 = 36"), W("s3", "36 ÷ 2 = 18"), W("s4", "72% of 25 = 18")),
    ASK(Q, "a2", "Careful now. Is 18 our answer?",
        "No: we want the ones not correct", ["Yes, 18"],
        "18 is the number he got right. The question asks for the answers that were not correct: the rest of the 25."),
    B("25 questions, 18 right. 25 minus 18 is 7. So 7 answers were not correct.",
      W("s5", "25 − 18 = 7"), ANSWER("ans", "Not correct = 7"), RING("ans", "7"),
      FIG("f", bars(bar([seg(18, "18 right", "a"), seg(7, "7", "b")], None, "25 questions")))),
    B("Check it another way. 100 minus 72 is 28, so 28 per cent were not correct. A quarter of 28 is 7. Same answer.",
      W("c1", "100% − 72% = 28%"), W("c2", "28 ÷ 4 = 7")),
    B("So read to the very end. Find the per cent, then check whether the question wants that part, or the rest."),
])

Q = "EXT_G5_FP_2020_032"
add(Q, [
    B("This one sounds like a tongue twister: 5 per cent, of 5 per cent, of 100 rupees.",
      GIVEN("q", "5% of 5% of Rs.100 = ?")),
    B("The trick is to start from the far end, and take one step at a time. So first: 5 per cent of 100 rupees.",
      MARK("q", "5% of Rs.100")),
    B("Per cent means out of every 100. So 5 per cent of 100 rupees is simply 5 rupees.",
      W("s1", "5% of 100 = 5"),
      FIG("f", bars(bar([seg(0.6, "5", "b"), seg(9.4)], None, "Rs.100"), note="5 out of every 100"))),
    ASK(Q, "a1", "Now we need 5 per cent of those 5 rupees. Will that be more than 1 rupee, or less?",
        "less than 1 rupee", ["more than 1 rupee", "exactly 5 rupees"],
        "5 per cent is a small part: only 5 out of every 100. A small part of just 5 rupees must be tiny, less than 1 rupee."),
    B("Let us use paise to see it clearly. Each rupee is 100 paise, so 5 rupees is 500 paise.",
      W("s2", "5 × 100 = 500"), NOTE("s2", "= 500", "paise", "below")),
    B("10 per cent of 500 is 50, and 5 per cent is half of that: 25. So the answer is 25 paise.",
      W("s3", "10% of 500 = 50"), W("s4", "5% of 500 = 50 ÷ 2 = 25")),
    B("25 paise is a quarter of a rupee. In rupees, we write it as 0.25.",
      W("s5", "25 ÷ 100 = 0.25"), ANSWER("ans", "5% of 5% of Rs.100 = Rs.0.25", label=False), RING("ans", "Rs.0.25")),
    B("Careful with the trap here. The two 5 per cents do not add up to 10 per cent. Each one takes its own small slice of what is in front of it."),
    B("So for a per cent of a per cent: start from the end, and take one slice at a time."),
])

Q = "EXT_G5_FP_2022_037"
add(Q, [
    B("Here is a line with two per cents, and a hidden number, A. We have to find A.",
      GIVEN("q", "15% of 40 − 25% of A = 2"), W("q2", "A = ?", label=True)),
    B("One of the per cents has no letter in it, so we can work it out straight away. That is 15 per cent of 40.",
      MARK("q", "15% of 40")),
    B("10 per cent of 40 is 4, and 5 per cent is half of that, which is 2. So 15 per cent of 40 is 4 plus 2: that makes 6.",
      W("s1", "10% of 40 = 4"), W("s2", "15% of 40 = 4 + 2 = 6")),
    B("So the line now says: 6, minus 25 per cent of A, equals 2.",
      W("s3", "6 − 25% of A = 2", label=True)),
    ASK(Q, "a1", "6 minus something leaves 2. What is the something?",
        "4", ["8", "2"],
        "Start at 6 and come down to 2. You have taken away 4. So 25 per cent of A is 4."),
    B("6 minus 4 is 2. So 25 per cent of A must be 4.",
      W("s4", "6 − 4 = 2"), W("s5", "25% of A = 4", label=True)),
    B("25 per cent is one quarter. If a quarter of A is 4, then the whole of A is 4 quarters: 4 times 4, which is 16.",
      W("s6", "4 × 4 = 16"), ANSWER("ans", "A = 16"), RING("ans", "16"),
      FIG("f", bars(bar([seg(1, "4", "b"), seg(1, "4"), seg(1, "4"), seg(1, "4")], None, "A"), note="4 quarters make the whole of A"))),
    B("Careful with that last step. A common slip is to take a quarter of 4. But 4 is already the quarter, so we multiply up, not down."),
    B("Check: a quarter of 16 is 4, and 6 minus 4 is 2. It works.",
      W("c", "15% of 40 − 25% of 16 = 2")),
    B("So work out the per cent you can, see what the missing per cent must be, then build up to the whole."),
])

Q = "EXT_G5_FP_2023_007"
add(Q, [
    B("Here is a line with a hidden number, Z, and two per cents. We want Z.",
      GIVEN("q", "Z + 16% of 150 = 13% of 600"), W("q2", "Z = ?", label=True)),
    B("Think of the equals sign as a balance. Before we can find Z, we turn each per cent into a plain number. Start with 16 per cent of 150.",
      MARK("q", "16% of 150")),
    B("10 per cent of 150 is 15. 5 per cent is half of that, 7.5. And 1 per cent is 1.5.",
      W("a1", "10% of 150 = 15"), W("a2", "5% of 150 = 7.5"), W("a3", "1% of 150 = 1.5")),
    B("16 per cent is 10 and 5 and 1 together. 15 plus 7.5 plus 1.5 makes 24.",
      W("a4", "16% of 150 = 15 + 7.5 + 1.5 = 24")),
    B("Now 13 per cent of 600. 1 per cent of 600 is 6, so we need 13 sixes. 10 sixes are 60, and 3 sixes are 18. Together, 78.",
      W("b1", "1% of 600 = 6"), W("b2", "13% of 600 = 60 + 18 = 78")),
    B("So our line becomes: Z plus 24 equals 78. Here it is on a balance.",
      W("e", "Z + 24 = 78", label=True), FIG("bal", {"kind": "balance", "left": "Z + 24", "right": "78"})),
    ASK(Q, "a1", "Z plus 24 makes 78. How do we find Z?",
        "78 − 24", ["78 + 24", "24 − 78"],
        "Z and 24 together make 78. Take the 24 away from the 78, and what is left is Z."),
    B("78 minus 24 is 54. So Z is 54.",
      W("s", "78 − 24 = 54"), ANSWER("ans", "Z = 54"), RING("ans", "54")),
    B("Check: 54 plus 24 is 78, and 78 is 13 per cent of 600. Both sides balance.",
      W("c", "54 + 16% of 150 = 13% of 600")),
    B("So with a line like this, turn each per cent into a plain number first. Then it is a simple missing number sum."),
])

Q = "EXT_G5_FP_2023_033"
add(Q, [
    B("What per cent is 84 minutes, of 7 hours?",
      GIVEN("q", "84 minutes out of 7 hours = ? %")),
    ASK(Q, "a1", "Before we compare them, what must we fix?",
        "make the units the same", ["divide 84 by 7", "add 84 and 7"],
        "84 is in minutes and 7 is in hours. We can only compare two amounts when they are in the same unit."),
    B("Careful: 84 divided by 7 would mix minutes with hours. Change the hours into minutes first. Each hour is 60 minutes, so 7 hours is 7 times 60: 420 minutes.",
      W("s1", "7 × 60 = 420"), NOTE("s1", "= 420", "minutes", "below")),
    B("So the real question is: 84 minutes is what per cent of 420 minutes? Here are the 420 minutes, cut into 10 equal pieces of 10 per cent.",
      W("s2", "84 out of 420 = ? %", label=True),
      FIG("f", ten_pieces(0, "420 minutes", "10 equal pieces: each is 10%"))),
    B("One piece is 10 per cent of 420. Divide by 10: that is 42 minutes.",
      W("s3", "10% of 420 = 420 ÷ 10 = 42")),
    ASK(Q, "a2", "One piece is 42 minutes. How many pieces make 84 minutes?",
        "2", ["4", "42"],
        "42 and 42 make 84. So 84 minutes is 2 of the 10 per cent pieces."),
    B("42 plus 42 is 84. So 84 minutes is 2 pieces of 10 per cent, and that is 20 per cent.",
      W("s4", "2 × 42 = 84"), W("s5", "2 × 10% = 20%"),
      ANSWER("ans", "84 minutes = 20% of 7 hours"), RING("ans", "20%"),
      FIG("f", ten_pieces(2, "420 minutes", "2 pieces of 42 minutes = 84 minutes", "42"))),
    B("Check: 20 per cent is one fifth, and 420 divided by 5 is 84. It fits.",
      W("c", "420 ÷ 5 = 84")),
    B("So for what per cent is this of that: put them in the same units first, then see how many 10 per cents fit."),
])

Q = "EXT_G5_FP_2024_026"
add(Q, [
    B("Mishti has marks in four subjects. Three are out of 50 and one is out of 100. We want her overall percentage.",
      GIVEN("q", "44/50, 50/50, 42/50 and 84/100"), W("q2", "Overall percentage = ?", label=True)),
    B("Let us make a mark sheet. For the overall percentage we need two totals: the marks she scored, and the marks they were out of.",
      FIG("t", table(["Subject", "Scored", "Out of"],
                     [["Science", "44", "50"], ["Maths", "50", "50"], ["English", "42", "50"], ["Social Sci.", "84", "100"], ["Total", "?", "?"]]))),
    B("Add up what she scored, one line at a time. 44 plus 50 is 94. Add 42 to get 136. Add 84 to get 220.",
      W("s1", "44 + 50 = 94"), W("s2", "94 + 42 = 136"), W("s3", "136 + 84 = 220")),
    B("Now the marks they were out of. 50 plus 50 plus 50 is 150, and 100 more makes 250.",
      W("s4", "50 + 50 + 50 = 150"), W("s5", "150 + 100 = 250"),
      FIG("t", table(["Subject", "Scored", "Out of"],
                     [["Science", "44", "50"], ["Maths", "50", "50"], ["English", "42", "50"], ["Social Sci.", "84", "100"], ["Total", "220", "250"]],
                     highlight=["r4"]))),
    ASK(Q, "a1", "She scored 220 marks. For the overall percentage, that is 220 out of what?",
        "out of 250, all the marks", ["out of 100", "out of 150"],
        "Three papers were out of 50 and one was out of 100. Altogether that is 250 marks, so we compare 220 with 250."),
    B("So she has 220 out of 250. Per cent means out of 100, so shrink the 250 down to 100. Divide both by 5: 44 out of 50. Then double both: 88 out of 100.",
      W("s6", "220/250 = 44/50 = 88/100")),
    B("88 out of 100 is 88 per cent.",
      ANSWER("ans", "Overall = 88%"), RING("ans", "88%")),
    B("Careful with a tempting shortcut: finding the per cent for each subject and averaging them. That does not work here, because Social Science carries more marks than the others."),
    B("Check: she lost 250 minus 220, which is 30 marks. 10 per cent of 250 is 25, so she lost a bit more than 10 per cent. 88 per cent is sensible.",
      W("c1", "250 − 220 = 30"), W("c2", "10% of 250 = 25")),
    B("So for an overall percentage: total scored, over total marks, then turn it into out of 100."),
])

Q = "EXT_G5_FP_2025_005"
add(Q, [
    B("We start with 80. Some per cent of 80 is added to it, and the sum must equal the square of 12. Which per cent?",
      GIVEN("q", "80 + (? % of 80) = the square of 12")),
    B("First the target. The square of 12 is 12 times 12. 12 tens are 120, and 12 twos are 24. Together, 144.",
      W("s1", "12 × 10 = 120"), W("s2", "12 × 2 = 24"), W("s3", "12² = 120 + 24 = 144")),
    ASK(Q, "a1", "We start at 80 and must reach 144. How do we find what has to be added?",
        "144 − 80", ["144 + 80", "144 ÷ 80"],
        "We want the gap between where we are, 80, and where we must get to, 144. A gap is found by subtracting."),
    B("144 minus 80 is 64. So 64 must be added.",
      W("s4", "144 − 80 = 64"),
      FIG("f", bars(bar([seg(8, "80", "a"), seg(6.4, "64", "b")], None, "144")))),
    B("Careful: 64 is not the answer yet. The question asks what per cent of 80 that 64 is.",
      MARK("q", "? % of 80")),
    B("Use 10 per cent of 80, which is 8. How many 8s make 64? 8 times 8 is 64.",
      W("s5", "10% of 80 = 8"), W("s6", "8 × 8 = 64")),
    B("So 64 is 8 lots of 10 per cent. That is 80 per cent of 80.",
      W("s7", "8 × 10% = 80%"), ANSWER("ans", "80% of 80 must be added"), RING("ans", "80%")),
    B("Check: 80 per cent of 80 is 64, and 80 plus 64 is 144, the square of 12.",
      W("c", "80 + 80% of 80 = 144")),
    B("So: find the target, find the gap, then ask what per cent of the starting number the gap is."),
])

Q = "EXT_G5_FP_2025_020"
add(Q, [
    B("Here is a line with two per cents and a hidden number, M. We want M.",
      GIVEN("q", "6.5% of 800 = 8% of 250 + M"), W("q2", "M = ?", label=True)),
    B("First we turn each per cent into a plain number. Start on the left, with 6.5 per cent of 800.",
      MARK("q", "6.5% of 800")),
    B("1 per cent of 800 is 8. So 6 per cent is 6 times 8, which is 48. And half a per cent is half of 8, which is 4.",
      W("a1", "1% of 800 = 8"), W("a2", "6% of 800 = 6 × 8 = 48"), W("a3", "0.5% of 800 = 8 ÷ 2 = 4")),
    B("6.5 per cent is 6 per cent and half a per cent together. 48 plus 4 is 52.",
      W("a4", "6.5% of 800 = 48 + 4 = 52")),
    B("Now 8 per cent of 250. 1 per cent of 250 is 2.5, and 8 times 2.5 is 20.",
      W("b1", "1% of 250 = 2.5"), W("b2", "8% of 250 = 8 × 2.5 = 20")),
    B("So the line now says: 52 equals 20 plus M. Here it is on a balance.",
      W("e", "52 = 20 + M", label=True), FIG("bal", {"kind": "balance", "left": "52", "right": "20 + M"})),
    ASK(Q, "a1", "20 plus M makes 52. How do we find M?",
        "52 − 20", ["52 + 20", "20 − 52"],
        "20 and M together make 52. Take the 20 away from the 52, and what is left is M."),
    B("52 minus 20 is 32. So M is 32.",
      W("s", "52 − 20 = 32"), ANSWER("ans", "M = 32"), RING("ans", "32")),
    B("Check: 20 plus 32 is 52, and 52 is 6.5 per cent of 800. Both sides balance.",
      W("c", "6.5% of 800 = 8% of 250 + 32")),
    B("So with a line like this, turn each per cent into a plain number first. Then it is a simple missing number sum."),
])
