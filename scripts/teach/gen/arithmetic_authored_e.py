"""Hand-written lessons: past papers 2016 and 2017."""
from arithmetic_common import ANS, B, FIG, GIVEN, M, N, S, W, choose, lesson

LESSONS = {}

LESSONS["EXT_G5_FP_2016_002"] = lesson(
    B("Three bags hold 24 apples between them. We know two totals for pairs of bags, and we want the first and third bags together.",
      GIVEN("l1", "All three = 24.  1st + 2nd = 11.  2nd + 3rd = 18", True),
      FIG("f1", {"kind": "barModel", "bars": [{"segments": [
          {"units": 1, "label": "1st", "tone": "a"}, {"units": 1, "label": "2nd", "tone": "b"}, {"units": 1, "label": "3rd", "tone": "c"}],
          "brace": "24"}]})),
    B("All three bags hold 24. The first and second together hold 11. What does that tell us about the third bag?",
      ask=choose(["it holds 24 + 11", "it holds 11", "it holds 24 − 11"], 2,
                 "The three bags make 24. Take away the first two, which hold 11 between them, and what is left must be in the third bag.")),
    B("24 minus 11 is 13. The third bag holds 13 apples.", W("l2", "24 − 11 = 13"), N("l2", "13", "3rd bag")),
    B("Now the same idea from the other end. The second and third together hold 18, so the first bag holds 24 minus 18, which is 6.",
      W("l3", "24 − 18 = 6"), N("l3", "6", "1st bag")),
    B("First and third together: 6 plus 13 is 19.", ANS("l4", "6 + 13 = 19"), M("l4", "19", "circle")),
    B("Let's check with the second bag. It must hold 24 minus 19, which is 5. Then 6 plus 5 is 11, and 5 plus 13 is 18. Both clues fit.",
      W("l5", "24 − 19 = 5"), W("l6", "6 + 5 = 11"), W("l7", "5 + 13 = 18")),
    B("When you know the whole and one part, subtract to find the rest. Here we simply did that twice."),
)

LESSONS["EXT_G5_FP_2016_010"] = lesson(
    B("A boy played for 1 hour and 15 minutes. We want that as a decimal number of hours.", GIVEN("l1", "1 hour 15 minutes = ? hours", True)),
    B("It is tempting to put the 15 straight after the point. Why does that not work?",
      ask=choose(["because 15 is too small", "an hour has 60 minutes, not 100", "it does work"], 1,
                 "A decimal counts in tenths and hundredths. But minutes are sixtieths of an hour. So 15 minutes is 15 out of 60, not 15 out of 100.")),
    B("So 15 minutes is 15 out of 60 of an hour. 15 goes into 60 exactly 4 times, so that is one quarter of an hour.",
      W("l2", "15/60 = 1/4"), FIG("f1", {"kind": "clock", "hour": 1, "minute": 15, "note": "A quarter of the way round"})),
    B("And one quarter is 25 hundredths, which we write as 0.25.", W("l3", "1/4 = 25/100 = 0.25")),
    B("So the time is 1 whole hour plus 0.25 of an hour. That is 1.25 hours.", ANS("l4", "1 + 0.25 = 1.25"), M("l4", "1.25", "circle")),
    B("Check it backwards. 0.25 of 60 minutes is 15 minutes. Just right.", W("l5", "0.25 × 60 = 15")),
    B("To turn minutes into hours, divide by 60 first. Never just write the minutes after the point."),
)

LESSONS["EXT_G5_FP_2016_023"] = lesson(
    B("A line with decimals in it, and four different signs. The order matters just as much with decimals.",
      GIVEN("l1", "8 − 4.2 ÷ 6 + 0.3 × 0.4")),
    B("Which parts do we work out first?",
      ask=choose(["8 − 4.2", "6 + 0.3", "4.2 ÷ 6 and 0.3 × 0.4"], 2,
                 "Divide and times come before plus and minus. So the 4.2 divided by 6 and the 0.3 times 0.4 are both done first.")),
    B("First the divide. 42 divided by 6 is 7, so 4.2 divided by 6 is 0.7.",
      M("l1", "4.2 ÷ 6"), W("l2", "42 ÷ 6 = 7"), W("l3", "4.2 ÷ 6 = 0.7"), N("l1", "4.2 ÷ 6", "0.7")),
    B("Now the times. 3 times 4 is 12. There are two decimal places in the question, one in each number, so the answer has two as well: 0.12.",
      M("l1", "0.3 × 0.4"), W("l4", "3 × 4 = 12"), W("l5", "0.3 × 0.4 = 0.12"), N("l1", "0.3 × 0.4", "0.12")),
    B("Write the line again with those two answers in place.", W("l6", "8 − 4.2 ÷ 6 + 0.3 × 0.4 = 8 − 0.7 + 0.12")),
    B("Now left to right. 8 minus 0.7 is 7.3.", W("l7", "8 − 0.7 + 0.12 = 7.3 + 0.12")),
    B("7.3 is the same as 7.30. Add 0.12 and we get 7.42.", ANS("l8", "7.3 + 0.12 = 7.42"), M("l8", "7.42", "circle")),
    B("Same rule as always: times and divide first, then plus and minus from left to right. And count the decimal places when you multiply."),
)

LESSONS["EXT_G5_FP_2016_031"] = lesson(
    B("Four little sums made of 9s and 3s. We want the one with the least value, so let's work out each.",
      GIVEN("l1", "Which has the least value?", True),
      W("a", "9 × 3 + 3"), W("b", "3 × 3 + 9"), W("c", "9 − 3 × 3"), W("d", "(9 + 3) × 3")),
    B("The first one. Times goes first: 9 times 3 is 27, and 27 plus 3 is 30.", M("a", "9 × 3"), W("a1", "9 × 3 + 3 = 27 + 3 = 30")),
    B("The second. 3 times 3 is 9, and 9 plus 9 is 18.", M("b", "3 × 3"), W("b1", "3 × 3 + 9 = 9 + 9 = 18")),
    B("The fourth has a bracket, so that goes first. 9 plus 3 is 12, and 12 times 3 is 36.",
      M("d", "(9 + 3)", "box"), W("d1", "(9 + 3) × 3 = 12 × 3 = 36")),
    B("Now the third one, 9 minus 3 times 3. Which part goes first?",
      ask=choose(["9 − 3", "3 × 3"], 1, "Times comes before minus. So 3 times 3 goes first, even though the minus is on the left.")),
    B("3 times 3 is 9, and 9 minus 9 is 0.", M("c", "3 × 3"), W("c1", "9 − 3 × 3 = 9 − 9 = 0")),
    B("So the values are 30, 18, 0 and 36. Nothing here is smaller than 0, so the third one is the least.",
      ANS("e", "Least: 9 − 3 × 3", True), M("e", "9 − 3 × 3", "circle")),
    B("Work out every choice in the proper order before you compare. One slip in the order can change which one wins."),
)

LESSONS["EXT_G5_FP_2016_033"] = lesson(
    B("A man bought 27 eggs. We want to say that in dozens, as a decimal.",
      GIVEN("l1", "27 eggs = ? dozen", True), W("l2", "1 dozen = 12 eggs", label=True)),
    B("How many full dozens fit into 27?",
      ask=choose(["1", "2", "3"], 1, "Count in 12s. Two 12s still fit inside 27, but a third 12 would go past it.")),
    B("2 dozens use up 24 eggs. That leaves 3 eggs over.", W("l3", "12 × 2 = 24"), W("l4", "27 = 12 × 2 + 3"), M("l4", "3", "circle")),
    B("Those 3 left-over eggs are only part of a dozen. What fraction of a dozen are they?",
      ask=choose(["3/10", "3/12", "3/27"], 1,
                 "A dozen has 12 eggs, so 3 eggs are 3 out of 12, not 3 out of 10. This is exactly where the decimal trap hides.")),
    B("3 out of 12 is one quarter. And one quarter, as a decimal, is 0.25.", W("l5", "3/12 = 1/4 = 0.25")),
    B("So 27 eggs are 2 dozens and 0.25 of a dozen. That is 2.25 dozen.", ANS("l6", "2 + 0.25 = 2.25"), M("l6", "2.25", "circle")),
    B("Check: 2.25 times 12 should take us back to 27 eggs. It does.", W("l7", "2.25 × 12 = 27")),
    B("The leftovers become a fraction of the group size, here twelfths. Then turn that fraction into a decimal."),
)

LESSONS["EXT_G5_FP_2017_010"] = lesson(
    B("Three boxes to fill with signs, so that the line comes to 28.", GIVEN("l1", "10 □ 6 □ 4 □ 6 = 28", True)),
    B("We test each set, always doing times and divide before plus and minus. First set: plus, times, divide. Which part goes first?",
      W("a", "10 + 6 × 4 ÷ 6"),
      ask=choose(["10 + 6", "6 × 4", "4 ÷ 6"], 1,
                 "Times and divide come before plus. And between a times and a divide we go from left to right, so 6 times 4 is first.")),
    B("6 times 4 is 24. Then 24 divided by 6 is 4, and 10 plus 4 is 14. Not 28.",
      M("a", "6 × 4"), W("a1", "10 + 6 × 4 ÷ 6 = 10 + 24 ÷ 6 = 14"), S("a", "10 + 6 × 4 ÷ 6")),
    B("Second set: plus, minus, divide. That needs 4 divided by 6, which is not a whole number. So this line cannot land exactly on 28.",
      W("b", "10 + 6 − 4 ÷ 6"), M("b", "4 ÷ 6"), S("b", "10 + 6 − 4 ÷ 6")),
    B("Third set: plus, times, minus. Times first again: 6 times 4 is 24.",
      W("c", "10 + 6 × 4 − 6"), M("c", "6 × 4"), W("c1", "10 + 6 × 4 − 6 = 10 + 24 − 6")),
    B("Now left to right. 10 plus 24 is 34, and 34 minus 6 is 28. That is the one.",
      W("c2", "10 + 24 − 6 = 34 − 6"), ANS("c3", "10 + 6 × 4 − 6 = 28"), M("c3", "28", "circle")),
    B("So the signs are plus, times, minus. For box puzzles, test each set and follow the proper order every time."),
)

LESSONS["EXT_G5_FP_2017_014"] = lesson(
    B("A man bought 21 oranges. We want to write that as a decimal number of dozens.",
      GIVEN("l1", "21 oranges = ? dozen", True), W("l2", "1 dozen = 12 oranges", label=True)),
    B("21 is more than one dozen but less than two. So there is one full dozen, and 9 oranges left over.",
      W("l3", "21 = 12 × 1 + 9"), M("l3", "9", "circle")),
    B("What fraction of a dozen are those 9 left-over oranges?",
      ask=choose(["9/10", "9/21", "9/12"], 2,
                 "A full dozen is 12 oranges, so 9 oranges are 9 out of 12. Using 9 out of 10 would be thinking in tens, not dozens.")),
    B("9 out of 12. Divide the top and the bottom by 3, and it becomes three quarters.",
      W("l4", "9/12 = 3/4"),
      FIG("f1", {"kind": "fractionBars", "bars": [{"parts": 12, "shaded": 9, "label": "9/12"}, {"parts": 4, "shaded": 3, "label": "3/4"}]})),
    B("One quarter is 0.25. So what is three quarters as a decimal?", W("l5", "1/4 = 0.25"),
      ask=choose(["0.34", "0.75", "0.9"], 1, "Three quarters is 3 lots of one quarter. And 3 lots of 0.25 make 0.75.")),
    B("So 21 oranges are 1 dozen and 0.75 of a dozen. That is 1.75 dozen.",
      W("l6", "3 × 0.25 = 0.75"), ANS("l7", "1 + 0.75 = 1.75"), M("l7", "1.75", "circle")),
    B("Check: 1.75 times 12 gives back 21 oranges.", W("l8", "1.75 × 12 = 21")),
    B("The tempting slip is to pop the 21 straight into a decimal. That would only be right if a dozen were 10. Leftovers are twelfths."),
)

LESSONS["EXT_G5_FP_2017_015"] = lesson(
    B("Round, curly and square brackets, all in one line. We open them from the inside out.",
      GIVEN("l1", "8 + 6 ÷ 2 − [2 × 3 − {2 − (3 + 2)}]")),
    B("Which part do we do first?",
      ask=choose(["8 + 6", "the round bracket (3 + 2)", "6 ÷ 2"], 1,
                 "Brackets come before everything, and the innermost bracket comes first of all. That is the round one, 3 plus 2.")),
    B("3 plus 2 is 5.", M("l1", "(3 + 2)", "box"), N("l1", "(3 + 2)", "5"), W("l2", "8 + 6 ÷ 2 − [2 × 3 − {2 − 5}]")),
    B("Next the curly bracket: 2 minus 5. We are taking away more than we have. What do we get?",
      M("l2", "{2 − 5}", "box"),
      ask=choose(["3", "0", "−3, which is 3 below zero"], 2,
                 "From 2, taking away 2 gets us down to 0. There are still 3 more to take away, so we finish 3 below zero. We write minus 3.")),
    B("So the curly bracket is worth minus 3.", W("l3", "2 − 5 = −3"), W("l4", "8 + 6 ÷ 2 − [2 × 3 − (−3)]")),
    B("Inside the square bracket, times first: 2 times 3 is 6. Then 6 minus, minus 3. Taking away a minus number is the same as adding, so that is 6 plus 3, which is 9.",
      M("l4", "− (−3)", "circle"), N("l4", "− (−3)", "+ 3"), W("l5", "2 × 3 − (−3) = 6 + 3 = 9"), W("l6", "8 + 6 ÷ 2 − 9")),
    B("No brackets left. Divide goes before plus and minus: 6 divided by 2 is 3.", M("l6", "6 ÷ 2"), W("l7", "8 + 6 ÷ 2 − 9 = 8 + 3 − 9")),
    B("Left to right now. 8 plus 3 is 11, and 11 minus 9 is 2.", W("l8", "8 + 3 = 11"), ANS("l9", "11 − 9 = 2"), M("l9", "2", "circle")),
    B("Innermost bracket first and work outwards. Then divide and times. Then plus and minus, left to right."),
)

LESSONS["EXT_G5_FP_2017_025"] = lesson(
    B("A two-digit number ending in 9, times a three-digit number ending in 3. The other digits are hidden. Which of the four choices could be the product?",
      GIVEN("l1", "♣9 × ♣♣3 = ?", True), W("l2", "1907,  957,  46847,  756927", label=True)),
    B("The usual first test is the last digit. 9 times 3 is 27, so the product ends in 7. But look: all four choices end in 7! What else can we test?",
      W("l3", "9 × 3 = 27"),
      ask=choose(["whether it is even", "how big the product can be", "its middle digit"], 1,
                 "We know how many digits each number has. So we can work out the smallest and the biggest the product could possibly be.")),
    B("Smallest first. The smallest two-digit number ending in 9 is 19. The smallest three-digit number ending in 3 is 103. And 19 times 103 is 1957.",
      W("l4", "19 × 103 = 1957")),
    B("So nothing below 1957 is possible. That rules out 957, and it rules out 1907 as well, by just a whisker.",
      S("l2", "957", "too small"), S("l2", "1907", "too small")),
    B("Now the biggest. 99 times 993 is 98307, which has five digits. So the six-digit number 756927 is far too big.",
      W("l5", "99 × 993 = 98307"), S("l2", "756927", "too big")),
    B("Only 46847 is left. And it really works: 79 times 593 is 46847.",
      W("l6", "79 × 593 = 46847"), ANS("l7", "The product can be 46847", True), M("l7", "46847", "circle")),
    B("When the last-digit test cannot separate the choices, test the size: the smallest and the biggest the product could be."),
)

LESSONS["EXT_G5_FP_2017_026"] = lesson(
    B("We are handed a fact for free: 21 times 24 is 504. The new sum has the same digits, just with decimal points in them.",
      GIVEN("l1", "21 × 24 = 504"), W("l2", "2.1 × 0.24 = ?")),
    B("So the digits of the answer will be 5, 0, 4 again. We only have to place the point. First, how did 21 turn into 2.1?",
      ask=choose(["it was divided by 100", "it was divided by 10", "it was multiplied by 10"], 1,
                 "The point has moved one place to the left, which makes the number 10 times smaller. That is dividing by 10.")),
    B("21 was divided by 10. And 24 became 0.24: the point moved two places, so it was divided by 100.",
      W("l3", "2.1 = 21 ÷ 10"), W("l4", "0.24 = 24 ÷ 100")),
    B("So the answer is 504 made 10 times smaller, and then 100 times smaller again. Altogether that is 1000 times smaller.",
      W("l5", "10 × 100 = 1000")),
    B("Dividing by 1000 moves the point three places to the left. 504 becomes 0.504.",
      W("l6", "504 ÷ 1000 = 0.504"), ANS("l7", "2.1 × 0.24 = 0.504"), M("l7", "0.504", "circle")),
    B("A quick way to see it: count the decimal places in the question. One in 2.1 and two in 0.24 makes three, so the answer has three decimal places."),
    B("When you are given a multiplication fact, keep the digits and just work out where the point belongs."),
)

LESSONS["EXT_G5_FP_2017_032"] = lesson(
    B("One long sum divided by another. We could add them both up, but let's look at the numbers first.",
      GIVEN("l1", "(66 + 77 + 88 + 99) ÷ (11 + 22 + 33 + 44)")),
    B("What do you notice about every number here?",
      ask=choose(["they are all even", "they are all multiples of 11", "they are all odd"], 1,
                 "66 is 6 elevens, 77 is 7 elevens, and so on. Every number here is in the 11 times table.")),
    B("So the top is 6 elevens, 7 elevens, 8 elevens and 9 elevens. 6 plus 7 plus 8 plus 9 is 30, so the top is 30 elevens.",
      W("l2", "6 + 7 + 8 + 9 = 30"), W("l3", "66 + 77 + 88 + 99 = 30 × 11")),
    B("The bottom is 1, 2, 3 and 4 elevens. That makes 10 elevens.", W("l4", "1 + 2 + 3 + 4 = 10"), W("l5", "11 + 22 + 33 + 44 = 10 × 11")),
    B("So we have 30 elevens divided by 10 elevens. What is that?",
      ask=choose(["20", "3", "33"], 1, "The elevens are the same on the top and on the bottom, so they cancel out. We are left with 30 divided by 10.")),
    B("30 divided by 10 is 3.", ANS("l6", "30 ÷ 10 = 3"), M("l6", "3", "circle", 2)),
    B("The long way agrees. The top adds to 330, the bottom to 110, and 330 divided by 110 is 3.", W("l7", "330 ÷ 110 = 3")),
    B("Before a long calculation, look for something all the numbers share. It can shrink the work to almost nothing."),
)
