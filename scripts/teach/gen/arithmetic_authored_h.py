"""Hand-written lessons: past papers 2023 (rest), 2024 and 2025."""
from arithmetic_common import ANS, B, FIG, G, GIVEN, M, N, S, W, choose, lesson

LESSONS = {}

LESSONS["EXT_G5_FP_2023_015"] = lesson(
    B("A bracket with fractions of numbers inside it, and then a divide by a fraction. One piece at a time.",
      GIVEN("l1", "(9 + 3/5 of 25 − 7/13 of 39) ÷ 4/3", True)),
    B("Brackets first, and inside the bracket, of means multiply. How do we find 3 fifths of 25?",
      ask=choose(["25 ÷ 3, then × 5", "25 − 5", "25 ÷ 5, then × 3"], 2,
                 "Fifths means sharing into 5 equal parts. So divide 25 by 5 to find one fifth, then take 3 of those parts.")),
    B("25 divided by 5 is 5, and 3 of those make 15. In the same way, 39 divided by 13 is 3, and 7 of those make 21.",
      M("l1", "3/5 of 25"), W("l2", "3/5 of 25 = 15"), M("l1", "7/13 of 39"), W("l3", "7/13 of 39 = 21")),
    B("So the bracket is 9 plus 15, minus 21. That leaves 3.", W("l4", "9 + 15 − 21 = 3"), W("l5", "3 ÷ (4/3)")),
    B("Now we must divide 3 by 4 thirds. What is the trick for dividing by a fraction?",
      ask=choose(["flip it and multiply", "flip it and add", "just divide by 4"], 0,
                 "To divide by a fraction, turn it upside down and multiply. So dividing by 4 thirds becomes multiplying by 3 quarters.")),
    B("3 times 3 quarters is 9 quarters.", W("l6", "3 ÷ (4/3) = 3 × 3/4 = 9/4")),
    B("8 quarters make 2 wholes, and there is one quarter more. That is 2 and a quarter, or 2.25.",
      ANS("l7", "9/4 = 2.25"), M("l7", "2.25", "circle")),
    B("Bracket first, reading of as times. And to divide by a fraction, flip it and multiply."),
)

LESSONS["EXT_G5_FP_2023_018"] = lesson(
    B("We want to know what part of a whole day 216 minutes is, written as a decimal.", GIVEN("l1", "216 minutes = ? of a day", True)),
    B("First we need a whole day in minutes. Which sum gives that?",
      ask=choose(["24 × 100", "24 × 60", "12 × 60"], 1, "A day has 24 hours, and each hour has 60 minutes. So it is 24 lots of 60.")),
    B("24 times 60 is 1440 minutes in a day. So our fraction is 216 out of 1440.", W("l2", "24 × 60 = 1440"), W("l3", "216/1440", label=True)),
    B("Big numbers, so shrink it in steps. Divide the top and bottom by 12, and we get 18 out of 120. Divide by 6, and we get 3 out of 20.",
      W("l4", "216/1440 = 18/120"), W("l5", "18/120 = 3/20")),
    B("Now turn 3 twentieths into a decimal. What should we change the 20 into?",
      ask=choose(["10", "100", "60"], 1,
                 "Decimals count in tenths and hundredths. 20 goes into 100 exactly 5 times, so twentieths can be turned into hundredths.")),
    B("Multiply the top and the bottom by 5. 3 twentieths becomes 15 hundredths, which is 0.15.",
      W("l6", "3/20 = 15/100 = 0.15"), ANS("l7", "216/1440 = 0.15"), M("l7", "0.15", "circle")),
    B("Check: 0.15 of 1440 minutes should be 216 minutes. It is.", W("l8", "0.15 × 1440 = 216")),
    B("Put both amounts in the same unit, write the fraction, simplify it, and then change it to hundredths."),
)

LESSONS["EXT_G5_FP_2023_020"] = lesson(
    B("We add 3042 and 869, then take a mystery number away, and we are left with 2165. What was taken away?",
      GIVEN("l1", "3042 + 869 − ? = 2165")),
    B("First the sum. Add the 869 in two bites. 3042 plus 800 is 3842, and 69 more makes 3911.",
      W("l2", "3042 + 800 = 3842"), W("l3", "3842 + 69 = 3911"), M("l3", "3911")),
    B("So we start at 3911, take something away, and land on 2165. How do we find the something?",
      W("l4", "3911 − ? = 2165"),
      FIG("f1", {"kind": "barModel", "bars": [{"segments": [
          {"units": 4, "label": "?", "tone": "unknown"}, {"units": 5, "label": "2165", "tone": "a"}], "brace": "3911"}]}),
      ask=choose(["3911 + 2165", "2165 − 869", "3911 − 2165"], 2,
                 "Look at the bar. The whole is 3911 and one part is 2165. The other part is what is left when we take 2165 away from 3911.")),
    B("3911 minus 2000 is 1911. Then take away the other 165, and we get 1746.",
      W("l5", "3911 − 2000 = 1911"), W("l6", "1911 − 165 = 1746")),
    B("So the number to subtract is 1746.", ANS("l7", "3911 − 2165 = 1746"), M("l7", "1746", "circle")),
    B("Check by adding back. 1746 plus 2165 is 3911, our sum. It fits.", W("l8", "1746 + 2165 = 3911")),
    B("When a whole is split into two parts and you know one, subtract to get the other. A quick bar makes that easy to see."),
)

LESSONS["EXT_G5_FP_2023_030"] = lesson(
    B("We are given a multiplication fact, but asked a division with decimals. The digits match, so the fact will do the heavy work.",
      GIVEN("l1", "168 × 54 = 9072"), W("l2", "0.9072 ÷ 16.8 = ?")),
    B("First turn the fact into a division. Which division does it give us?",
      ask=choose(["168 ÷ 54 = 9072", "9072 ÷ 168 = 54", "9072 ÷ 54 = 54"], 1,
                 "If 168 lots of 54 make 9072, then 9072 shared into 168 equal parts gives 54 in each.")),
    B("So 9072 divided by 168 is 54. Now for the decimal points.", W("l3", "9072 ÷ 168 = 54")),
    B("9072 became 0.9072: the point moved four places, so it was divided by 10000. And 168 became 16.8, divided by 10.",
      W("l4", "0.9072 = 9072 ÷ 10000"), W("l5", "16.8 = 168 ÷ 10")),
    B("The number being shared is 10000 times smaller, so the answer shrinks 10000 times. But the divisor is 10 times smaller too. What does a smaller divisor do to the answer?",
      ask=choose(["makes it smaller", "makes it bigger", "changes nothing"], 1,
                 "Sharing among fewer gives each one more. So when the divisor gets 10 times smaller, the answer gets 10 times bigger.")),
    B("10000 times smaller, then 10 times bigger. Overall, the answer is 1000 times smaller than 54. That is 0.054.",
      W("l6", "10000 ÷ 10 = 1000"), W("l7", "54 ÷ 1000 = 0.054"), ANS("l8", "0.9072 ÷ 16.8 = 0.054"), M("l8", "0.054", "circle")),
    B("Check by multiplying back. 16.8 times 0.054 gives 0.9072. Just right.", W("l9", "16.8 × 0.054 = 0.9072")),
    B("In a division, shrinking the first number shrinks the answer, but shrinking the divisor makes the answer grow. Track both."),
)

LESSONS["EXT_G5_FP_2023_037"] = lesson(
    B("This line is not true yet. One pair of brackets will make it equal 19.", GIVEN("l1", "42 ÷ 7 × 2 + 16 = 19", True)),
    B("As it stands, we go left to right: 42 divided by 7 is 6, times 2, plus 16, comes to 28. Too big.", W("l2", "42 ÷ 7 × 2 + 16 = 28")),
    B("Think backwards from 19. If the plus 16 comes last, then just before it we had 3. So 42 divided by something must be 3. Divided by what?",
      W("l3", "19 − 16 = 3"),
      ask=choose(["7", "14", "21"], 1, "3 times 14 is 42. So 42 divided by 14 gives 3.")),
    B("We need to divide by 14. And 7 times 2 is 14! So the brackets go round 7 times 2.",
      W("l4", "42 ÷ (7 × 2) + 16"), M("l4", "(7 × 2)", "box")),
    B("Brackets first: 7 times 2 is 14. Then 42 divided by 14 is 3.",
      W("l5", "42 ÷ (7 × 2) + 16 = 42 ÷ 14 + 16"), W("l6", "42 ÷ 14 + 16 = 3 + 16")),
    B("And 3 plus 16 is 19. The line is true now.", ANS("l7", "42 ÷ (7 × 2) + 16 = 19"), M("l7", "(7 × 2)", "circle")),
    B("Here is something worth noticing. Divide and times are equally strong, so without brackets the divide on the left goes first. The brackets let the times jump the queue."),
    B("To place brackets, work backwards from the answer, and find which numbers can build the piece you need."),
)

LESSONS["EXT_G5_FP_2024_003"] = lesson(
    B("A long line with no brackets at all. It looks scary, but it breaks into pieces.",
      GIVEN("l1", "21 ÷ 84 × 16 − 7 × 3 + 306 ÷ 17")),
    B("The minus and the plus split the line into three chunks. What do we do first: the chunks, or the minus and plus between them?",
      M("l1", "21 ÷ 84 × 16"), M("l1", "7 × 3"), M("l1", "306 ÷ 17"),
      ask=choose(["the minus and the plus", "just go left to right", "the three chunks"], 2,
                 "Times and divide come before plus and minus. So each chunk is worked out on its own first.")),
    B("First chunk, left to right. 21 goes into 84 exactly 4 times, so 21 divided by 84 is one quarter. And a quarter of 16 is 4.",
      W("l2", "21 ÷ 84 = 1/4"), W("l3", "1/4 × 16 = 4"), N("l1", "21 ÷ 84 × 16", "4")),
    B("Second chunk: 7 times 3 is 21.", N("l1", "7 × 3", "21")),
    B("Third chunk: 306 divided by 17. 17 times 10 is 170 and 17 times 8 is 136. Together they make 306, so the answer is 18.",
      W("l4", "17 × 10 = 170"), W("l5", "17 × 8 = 136"), W("l6", "17 × 18 = 306"), N("l1", "306 ÷ 17", "18")),
    B("The line is now 4 minus 21 plus 18. But 4 minus 21 dips below zero. Is there a friendlier way?", W("l7", "4 − 21 + 18"),
      ask=choose(["do 21 + 18 first", "add the 18 first: 4 + 18 − 21", "swap it to 21 − 4"], 1,
                 "The minus belongs only to the 21. So we may bring the plus 18 forward: 4 plus 18, and then take away 21.")),
    B("4 plus 18 is 22, and 22 minus 21 is 1.",
      W("l8", "4 − 21 + 18 = 4 + 18 − 21"), W("l9", "4 + 18 = 22"), ANS("l10", "22 − 21 = 1"), M("l10", "= 1", "circle")),
    B("Split a long line at its plus and minus signs. Work out each chunk, then put the chunks together."),
)

LESSONS["EXT_G5_FP_2024_010"] = lesson(
    B("Four decimals built from 8s and 0s. They look alike, so the danger is letting a digit slip into a place where it does not belong.",
      GIVEN("l1", "8.008 + 0.08 + 80.8 + 80.08")),
    B("We will give every number three decimal places, so the points line up. What does 0.08 become?",
      ask=choose(["0.008", "0.080", "0.800"], 1,
                 "Padding means writing zeros at the end, after the last digit. So 0.08 becomes 0.080. A zero slipped in front of the 8 would change its value.")),
    B("Here they are, padded and lined up on the point.",
      W("p1", "8.008", label=True), W("p2", "0.080", label=True), W("p3", "80.800", label=True), W("p4", "80.080", label=True)),
    B("Add two at a time. 8.008 plus 0.08 is 8.088.", W("l2", "8.008 + 0.08 = 8.088")),
    B("Add 80.8 to that. The 8 tenths drop into the empty tenths place, and we get 88.888. All eights!", W("l3", "8.088 + 80.8 = 88.888")),
    B("Last, add 80.08. Take care: 8 tens and 8 tens make more than 10 tens, so 1 goes into the hundreds place. We get 168.968.",
      ANS("l4", "88.888 + 80.08 = 168.968"), M("l4", "168.968", "circle")),
    B("A rough check. 8 plus 80 plus 80 is 168, and our answer is just a little more than that. Good.", W("l5", "8 + 80 + 80 = 168")),
    B("With decimals, line up the points, pad with zeros at the end, and add place by place."),
)

LESSONS["EXT_G5_FP_2024_022"] = lesson(
    B("2000 is divided by a mystery number, giving 29 with 57 left over. We need that divisor, and then its square.",
      GIVEN("l1", "2000 ÷ ? gives quotient 29, remainder 57", True)),
    B("Write the division the other way round: divisor times quotient, plus remainder. What do the equal groups add up to, without the leftover?",
      W("l2", "2000 = ? × 29 + 57"),
      ask=choose(["2000 + 57", "2000 − 57", "2000 ÷ 57"], 1,
                 "The 57 is what was left after the groups were made. Take it away from 2000 and we have exactly the groups.")),
    B("2000 minus 57 is 1943. So the mystery number times 29 is 1943.", S("l2", "+ 57", "− 57"), W("l3", "2000 − 57 = 1943")),
    B("How many 29s are in 1943? 29 times 60 is 1740. That leaves 203, and 203 is 29 times 7.",
      W("l4", "29 × 60 = 1740"), W("l5", "1943 − 1740 = 203"), W("l6", "29 × 7 = 203")),
    B("60 and 7 make 67. So the divisor is 67. And that fits: the remainder, 57, is smaller than 67.", W("l7", "29 × 67 = 1943"), M("l7", "67")),
    B("Are we finished?",
      ask=choose(["Yes, the answer is 67", "No, we need 67 squared"], 1, "67 is the divisor. But the question asks for the square of the divisor, so one more step.")),
    B("67 times 67. 67 times 60 is 4020, and 67 times 7 is 469. Together, 4489.",
      W("l8", "67 × 60 = 4020"), W("l9", "67 × 7 = 469"), W("l10", "4020 + 469 = 4489"), ANS("l11", "67 × 67 = 4489"), M("l11", "4489", "circle")),
    B("Take the remainder off, divide by the quotient to get the divisor, and then do whatever the question asks with it."),
)

LESSONS["EXT_G5_FP_2024_027"] = lesson(
    B("One division fact is given, and a second division is asked. The digits are the same, so we will reuse the fact.",
      GIVEN("l1", "867 ÷ 12.75 = 68"), W("l2", "8.67 ÷ 6.8 = ?")),
    B("The new sum divides by 6.8, which looks like the 68, not like the 12.75. So first swap the fact around. 867 divided by 68 is what?",
      ask=choose(["68", "12.75", "867"], 1,
                 "In a division fact, the divisor and the answer can swap places. 867 divided by 12.75 gives 68, so 867 divided by 68 gives 12.75.")),
    B("867 divided by 68 is 12.75. Now look at the decimal points.", W("l3", "867 ÷ 68 = 12.75")),
    B("867 became 8.67, so it was divided by 100. And 68 became 6.8, divided by 10.", W("l4", "8.67 = 867 ÷ 100"), W("l5", "6.8 = 68 ÷ 10")),
    B("The first number is 100 times smaller, which makes the answer 100 times smaller. But the divisor is 10 times smaller, which makes the answer 10 times bigger. Overall: 10 times smaller.",
      W("l6", "100 ÷ 10 = 10")),
    B("So take 12.75 and make it 10 times smaller. The point moves one place to the left: 1.275.",
      W("l7", "12.75 ÷ 10 = 1.275"), ANS("l8", "8.67 ÷ 6.8 = 1.275"), M("l8", "1.275", "circle")),
    B("Does it feel right? 8.67 is a little more than 6.8, so the answer should be a little more than 1. And it is."),
    B("Reuse the given fact. Then track each decimal point: a smaller first number shrinks the answer, a smaller divisor grows it."),
)

LESSONS["EXT_G5_FP_2024_036"] = lesson(
    B("Three boxes to fill with signs, so that the line comes to 16. We will test each set of signs.",
      GIVEN("l1", "12 □ 6 □ 3 □ 14 = 16", True)),
    B("First set: times, minus, divide. That would need 3 divided by 14, which is not a whole number. So it cannot land exactly on 16.",
      W("a", "12 × 6 − 3 ÷ 14"), M("a", "3 ÷ 14"), S("a", "12 × 6 − 3 ÷ 14")),
    B("Second set: minus, divide, plus. Which part of this goes first?", W("b", "12 − 6 ÷ 3 + 14"),
      ask=choose(["12 − 6", "3 + 14", "6 ÷ 3"], 2, "Divide comes before plus and minus. So 6 divided by 3 goes first, though it sits in the middle.")),
    B("6 divided by 3 is 2. Then 12 minus 2, plus 14, is 24. Not 16.", M("b", "6 ÷ 3"), W("b1", "12 − 6 ÷ 3 + 14 = 12 − 2 + 14 = 24")),
    B("Third set: times, divide, plus. 12 times 6 is 72, divided by 3 is 24, and adding 14 gives 38. Not 16 either.",
      W("c1", "12 × 6 ÷ 3 + 14 = 72 ÷ 3 + 14 = 38")),
    B("Fourth set: plus, times, minus. Times first: 6 times 3 is 18. Then 12 plus 18 is 30, and 30 minus 14 is 16. That is the one!",
      W("d", "12 + 6 × 3 − 14"), M("d", "6 × 3"), W("d1", "12 + 6 × 3 − 14 = 12 + 18 − 14"), W("d2", "12 + 18 = 30"),
      ANS("d3", "12 + 6 × 3 − 14 = 16"), M("d3", "16", "circle")),
    B("So the signs are plus, times, minus. Test every set, and each time do times and divide before plus and minus."),
)

LESSONS["EXT_G5_FP_2025_004"] = lesson(
    B("We multiply all the one-digit odd numbers together, divide by 18, and want to know what is left over.",
      GIVEN("l1", "(product of one-digit odd numbers) ÷ 18", True)),
    B("Which are the one-digit odd numbers?",
      ask=choose(["1, 3, 5, 7", "1, 3, 5, 7, 9", "3, 5, 7, 9"], 1, "One-digit numbers go up to 9. The odd ones among them are 1, 3, 5, 7 and 9. Don't leave out the 1 or the 9.")),
    B("Multiply them a step at a time. 1 times 3 times 5 is 15. Then 15 times 7 is 105. Then 105 times 9 is 945.",
      W("l2", "1 × 3 × 5 = 15"), W("l3", "15 × 7 = 105"), W("l4", "105 × 9 = 945"), M("l4", "945")),
    B("Now divide 945 by 18, in chunks. 18 times 50 is 900. That leaves 45.", W("l5", "18 × 50 = 900"), W("l6", "945 − 900 = 45")),
    B("18 times 2 is 36. That leaves 9. And 9 is smaller than 18, so we stop.", W("l7", "18 × 2 = 36"), W("l8", "45 − 36 = 9")),
    B("So 945 is 52 lots of 18, with 9 left over. The remainder is 9.", ANS("l9", "945 = 18 × 52 + 9"), M("l9", "9", "circle", 2)),
    B("A neat sense check. 945 is odd, and any number of 18s is even. So the leftover has to be odd. That fits our 9."),
    B("For a remainder, take out the divisor in big easy chunks until what is left is smaller than the divisor."),
)

LESSONS["EXT_G5_FP_2025_019"] = lesson(
    B("Four decimals, with minus and plus signs mixed together.", GIVEN("l1", "2.007 − 14.659 + 16.317 − 2.042")),
    B("Going left to right, we would start by taking 14.659 from 2.007, and dip below zero. There is a friendlier way. Which two numbers are being taken away?",
      ask=choose(["2.007 and 16.317", "14.659 and 2.042", "14.659 and 16.317"], 1,
                 "Each number owns the sign in front of it. The minus signs sit in front of 14.659 and 2.042.")),
    B("So gather them into two teams. The ones we add, and the ones we take away.",
      G("l1", ["2.007", "+ 16.317"], "add"), G("l1", ["− 14.659", "− 2.042"], "take away")),
    B("The adding team: 2.007 plus 16.317 is 18.324.", W("l2", "2.007 + 16.317 = 18.324")),
    B("The taking-away team: 14.659 plus 2.042 is 16.701.", W("l3", "14.659 + 2.042 = 16.701")),
    B("Now one subtraction. 18.324 minus 16 is 2.324, and taking away the other 0.701 leaves 1.623.",
      W("l4", "18.324 − 16 = 2.324"), W("l5", "2.324 − 0.701 = 1.623"), ANS("l6", "18.324 − 16.701 = 1.623"), M("l6", "1.623", "circle")),
    B("A rough check with whole numbers: 2 minus 15, plus 16, minus 2 is 1. Our answer is a bit more than 1. Good.", W("l7", "2 − 15 + 16 − 2 = 1")),
    B("When plus and minus are mixed, add up everything with a plus, add up everything with a minus, and subtract once."),
)

LESSONS["EXT_G5_FP_2025_023"] = lesson(
    B("A bracket in the middle and a little chain of times and divide on the end.", GIVEN("l1", "200 − (20 × 7 + 150 ÷ 3) + 8 × 2 ÷ 8")),
    B("Where do we start?",
      ask=choose(["200 − 20", "the bracket", "8 × 2 ÷ 8"], 1, "Brackets come before everything else. So we work out the inside of the bracket first.")),
    B("Inside the bracket, times and divide go before the plus. 20 times 7 is 140. 150 divided by 3 is 50.",
      M("l1", "20 × 7"), N("l1", "20 × 7", "140"), M("l1", "150 ÷ 3"), N("l1", "150 ÷ 3", "50")),
    B("140 plus 50 is 190. So the whole bracket is worth 190.", W("l2", "20 × 7 + 150 ÷ 3 = 140 + 50 = 190"), W("l3", "200 − 190 + 8 × 2 ÷ 8")),
    B("The bracket is gone. What comes next?",
      ask=choose(["200 − 190", "190 + 8", "8 × 2 ÷ 8"], 2, "Times and divide still come before plus and minus. So the 8 times 2 divided by 8 at the end is next.")),
    B("8 times 2 is 16, and 16 divided by 8 is 2. Times 8 and divide by 8 undo each other, so only the 2 is left.",
      M("l3", "8 × 2 ÷ 8"), W("l4", "8 × 2 ÷ 8 = 16 ÷ 8 = 2"), W("l5", "200 − 190 + 2")),
    B("Now left to right. 200 minus 190 is 10, and 10 plus 2 is 12.", ANS("l6", "200 − 190 + 2 = 12"), M("l6", "12", "circle")),
    B("Bracket first. Then times and divide. Then plus and minus, from left to right."),
)

LESSONS["EXT_G5_FP_2025_030"] = lesson(
    B("Two jobs here. Multiply 7.2 by 3.9, then see how much more that is than the smallest 2-digit prime number.",
      GIVEN("l1", "7.2 × 3.9 − (smallest 2-digit prime) = ?", True)),
    B("First the product. Forget the points for a moment and do 72 times 39. 72 times 40 is 2880, and one 72 less is 2808.",
      W("l2", "72 × 40 = 2880"), W("l3", "2880 − 72 = 2808"), W("l4", "72 × 39 = 2808")),
    B("Now put the point back. 7.2 and 3.9 have one decimal place each. How many decimal places does the product have?",
      ask=choose(["0", "1", "2"], 2, "One decimal place in each number makes two altogether. So the product has two decimal places.")),
    B("So 2808 becomes 28.08. That feels right, because 7 times 4 is 28.", W("l5", "7.2 × 3.9 = 28.08"), M("l5", "28.08"), W("l5b", "7 × 4 = 28")),
    B("Next, what is the smallest 2-digit prime number?",
      ask=choose(["10", "11", "13"], 1,
                 "10 is the smallest 2-digit number, but it divides by 2 and by 5, so it is not prime. The next one, 11, divides only by 1 and itself.")),
    B("It is 11. And 28.08 minus 11 is 17.08.", ANS("l6", "28.08 − 11 = 17.08"), M("l6", "17.08", "circle")),
    B("To multiply decimals, multiply as whole numbers, then count the decimal places to put the point back."),
)

LESSONS["EXT_G5_FP_2025_033"] = lesson(
    B("Two three-digit numbers, one ending in 7 and one ending in 6. Stars hide the rest. Which choice can be their product?",
      GIVEN("l1", "**7 × **6 = ?", True), W("l2", "11332,  353362,  994312,  457647", label=True)),
    B("Start with what we can see: the last digits, 7 and 6. What must the product end in?",
      ask=choose(["2", "7", "6"], 0, "Multiply the two last digits, 7 and 6, and look at the digit that answer ends in. That is the last digit of the product.")),
    B("7 times 6 is 42, so the product ends in 2. That removes 457647, which ends in 7.",
      W("l3", "7 × 6 = 42"), M("l3", "2", "circle"), S("l2", "457647")),
    B("Three are left, all ending in 2. So test the size. The smallest numbers that fit are 107 and 106, and 107 times 106 is 11342.",
      W("l4", "107 × 106 = 11342")),
    B("11332 is just below that. So close, but too small. Out.", S("l2", "11332", "too small")),
    B("The biggest numbers that fit are 997 and 996, and 997 times 996 is 993012. So 994312 is just too big. Out.",
      W("l5", "997 × 996 = 993012"), S("l2", "994312", "too big")),
    B("Only 353362 is left. And it does work: 547 times 646 is 353362.",
      W("l6", "547 × 646 = 353362"), ANS("l7", "The product can be 353362", True), M("l7", "353362", "circle")),
    B("Notice how close the decoys were to the limits. Work out the smallest and the biggest exactly, and you cannot be tricked."),
)

LESSONS["EXT_G5_FP_2025_035"] = lesson(
    B("This line is not true yet. One pair of brackets, in the right place, makes it equal 19.",
      GIVEN("l1", "192 ÷ 12 × 3 − 4 + 13 = 19", True)),
    B("As it stands: 192 divided by 12 is 16, times 3 is 48, and then minus 4 plus 13 gives 57. Far too big.",
      W("l2", "192 ÷ 12 = 16"), W("l3", "16 × 3 = 48"), W("l4", "48 − 4 + 13 = 57")),
    B("Think backwards from 19. If the plus 13 comes last, then just before it we had 6. So 192 divided by something is 6. Divided by what?",
      W("l5", "19 − 13 = 6"),
      ask=choose(["36", "32", "12"], 1, "Try 6 times 32. It comes to exactly 192. So 192 divided by 32 is 6.")),
    B("We need to divide by 32. Can we build 32 from the 12, the 3 and the 4? 12 times 3 is 36, and 36 minus 4 is 32. Yes!",
      W("l6", "6 × 32 = 192"), W("l7", "12 × 3 − 4 = 32")),
    B("So the brackets go round 12 times 3 minus 4. Brackets first gives 32, and 192 divided by 32 is 6.",
      W("l8", "192 ÷ (12 × 3 − 4) + 13"), M("l8", "(12 × 3 − 4)", "box"), W("l9", "192 ÷ (12 × 3 − 4) + 13 = 192 ÷ 32 + 13")),
    B("And 6 plus 13 is 19. The line is true now.", ANS("l10", "192 ÷ (12 × 3 − 4) + 13 = 19"), M("l10", "(12 × 3 − 4)", "circle")),
    B("The shorter bracket, round 12 times 3 only, would mean dividing 192 by 36, and that does not come out whole. The longer one is needed."),
    B("To place brackets, work backwards from the answer, and build the number you need from the ones that are there."),
)
