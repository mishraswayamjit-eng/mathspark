"""Hand-written lessons: past papers 2020, 2021, 2022 and the start of 2023."""
from arithmetic_common import ANS, B, FIG, G, GIVEN, M, N, S, W, choose, lesson

LESSONS = {}

LESSONS["EXT_G5_FP_2020_006"] = lesson(
    B("Four sums made from 10 and 3. This time we want the greatest, so let's work out each one.",
      GIVEN("l1", "Which has the greatest value?", True),
      W("a", "10 − 3 × 3"), W("b", "(10 + 3) × 3"), W("c", "10 × 3 + 3"), W("d", "3 × 3 + 10")),
    B("Start with the first, 10 minus 3 times 3. Which part goes first?",
      ask=choose(["10 − 3", "3 × 3"], 1, "Times comes before minus. So 3 times 3 goes first, even though the minus is on the left.")),
    B("3 times 3 is 9, and 10 minus 9 is 1.", M("a", "3 × 3"), W("a1", "10 − 3 × 3 = 10 − 9 = 1")),
    B("The second has a bracket, and brackets go first. 10 plus 3 is 13, and 13 times 3 is 39.",
      M("b", "(10 + 3)", "box"), W("b1", "(10 + 3) × 3 = 13 × 3 = 39")),
    B("The third: 10 times 3 is 30, and 30 plus 3 is 33.", M("c", "10 × 3"), W("c1", "10 × 3 + 3 = 30 + 3 = 33")),
    B("The fourth: 3 times 3 is 9, and 9 plus 10 is 19.", M("d", "3 × 3"), W("d1", "3 × 3 + 10 = 9 + 10 = 19")),
    B("So the values are 1, 39, 33 and 19. The greatest is 39, from the one with the bracket.",
      ANS("e", "Greatest: (10 + 3) × 3", True), M("e", "(10 + 3) × 3", "circle")),
    B("See what the bracket did? It made the 3 multiply the whole of 10 plus 3, not just one number. Work each choice in the proper order, then compare."),
)

LESSONS["EXT_G5_FP_2020_021"] = lesson(
    B("Krina meant to multiply by 2, but pressed times 20. We want one more step that puts it right.",
      GIVEN("l1", "She did × 20, but wanted × 2", True)),
    B("Let's try it with a real number, so we can see what happened. Say her number was 7. She wanted 14, but the calculator shows 140.",
      W("l2", "7 × 2 = 14"), W("l3", "7 × 20 = 140")),
    B("140 instead of 14. How many times too big is her answer?",
      ask=choose(["2 times", "10 times", "20 times"], 1, "20 is 10 times as big as 2. So her answer came out 10 times as big as it should be.")),
    B("To fix an answer that is 10 times too big, we divide by 10. But look at the choices: none of them says divide by 10!",
      W("l4", "140 ÷ 10 = 14"), W("l5", "Choices: ÷ 20,  ÷ 40,  × 0.5,  × 0.1", label=True)),
    B("Which of the choices does the same job as dividing by 10?",
      ask=choose(["× 0.5", "÷ 20", "× 0.1"], 2,
                 "0.1 is one tenth. Multiplying by one tenth means taking a tenth of the number, and that is exactly the same as dividing by 10.")),
    B("140 times 0.1 is 14. So she should multiply by 0.1.",
      W("l6", "140 × 0.1 = 14"), ANS("l7", "Multiply by 0.1", True), M("l7", "0.1", "circle")),
    B("Why not divide by 20? That would undo the whole times 20 and leave just her starting number, 7. She still wants it doubled.",
      W("l8", "140 ÷ 20 = 7")),
    B("Remember: multiplying by 0.1 is the same as dividing by 10. And multiplying by 0.5 is the same as halving."),
)

LESSONS["EXT_G5_FP_2020_026"] = lesson(
    B("A square bracket with a round bracket inside it, and the little word of in the middle.",
      GIVEN("l1", "778 − [5 + 3 of (25 − 2 × 10)]")),
    B("What is the very first thing to work out?",
      ask=choose(["778 − 5", "25 − 2", "2 × 10"], 2,
                 "Innermost bracket first, and inside it times goes before minus. So 2 times 10 is the first step. Doing 25 minus 2 first is the classic slip.")),
    B("2 times 10 is 20, and 25 minus 20 is 5. The round bracket is worth 5.",
      M("l1", "2 × 10"), W("l2", "25 − 2 × 10 = 25 − 20 = 5"), W("l3", "778 − [5 + 3 of 5]")),
    B("Now we meet 3 of 5. What does the word of tell us to do?",
      ask=choose(["add", "multiply", "divide"], 1, "3 of something means 3 lots of it. And lots of means multiply.")),
    B("3 times 5 is 15. And of is done before the plus, just like times. So the square bracket is 5 plus 15, which is 20.",
      M("l3", "3 of 5"), W("l4", "3 of 5 = 15"), W("l5", "5 + 15 = 20"), W("l6", "778 − 20")),
    B("And 778 minus 20 is 758.", ANS("l7", "778 − 20 = 758"), M("l7", "758", "circle")),
    B("Brackets from the inside out. Inside each one, of and times and divide go first, then plus and minus."),
)

LESSONS["EXT_G5_FP_2020_031"] = lesson(
    B("A container holds 2 decagrams of medicine. We want to know how many doses of 1 milligram that is.",
      GIVEN("l1", "2 decagrams = ? milligrams", True)),
    B("Two prefixes to unpack: deca and milli. Deca means 10, so one decagram is 10 grams. That makes 2 decagrams 20 grams.",
      W("l2", "1 decagram = 10 grams", label=True), W("l3", "2 × 10 = 20")),
    B("Milli means a thousandth. So how many milligrams make one gram?",
      ask=choose(["10", "100", "1000"], 2, "Milli means one thousandth. It takes 1000 thousandths to make one whole, so one gram is 1000 milligrams.")),
    B("One gram is 1000 milligrams.", W("l4", "1 gram = 1000 milligrams", label=True)),
    B("So 20 grams is 20 times 1000 milligrams. That is 20000, so there are 20000 doses.",
      ANS("l5", "20 × 1000 = 20000"), M("l5", "20000", "circle")),
    B("In one line, it is 2 times 10 times 1000. Notice we multiplied both times: going from a big unit to a small one, the number always grows.",
      W("l6", "2 × 10 × 1000 = 20000")),
    B("Learn what the prefixes mean. Then change units one step at a time, through the plain gram in the middle."),
)

LESSONS["EXT_G5_FP_2020_033"] = lesson(
    B("X leaves 2 when divided by 5. Y leaves 4 when divided by 5. What does X plus Y leave?",
      GIVEN("l1", "X ÷ 5 leaves 2.  Y ÷ 5 leaves 4.  (X + Y) ÷ 5 leaves ?", True)),
    B("Picture X as some bundles of 5 with 2 loose ones. And Y as bundles of 5 with 4 loose ones. For example, 7 and 9.",
      W("l2", "7 = 5 + 2"), W("l3", "9 = 5 + 4")),
    B("When we add, bundles join bundles, and loose ones join loose ones. 2 loose plus 4 loose makes 6 loose.", W("l4", "2 + 4 = 6")),
    B("6 loose ones. Can 6 be the remainder when we divide by 5?",
      ask=choose(["Yes, the remainder is 6", "No: 6 is one more 5, and 1 over"], 1,
                 "A remainder must be smaller than the divisor. 6 loose ones can make one more bundle of 5, and that leaves just 1.")),
    B("6 is one more 5, with 1 over. So the remainder is 1.", W("l5", "6 = 5 + 1"), M("l5", "1", "circle")),
    B("Check with our example. 7 plus 9 is 16, and 16 is 3 fives and 1 more.", W("l6", "7 + 9 = 16"), W("l7", "16 = 5 × 3 + 1")),
    B("So the remainder is 1, whatever X and Y are.", ANS("l8", "Remainder = 1", True), M("l8", "1", "circle")),
    B("Add the remainders. If the total reaches the divisor, take out one more group. What is left is the new remainder."),
)

LESSONS["EXT_G5_FP_2021_030"] = lesson(
    B("We want to take away as little as possible from 13601, so that what is left divides exactly by 87.",
      GIVEN("l1", "13601 − ? is divisible by 87", True)),
    B("Which number tells us what to take away?",
      ask=choose(["the quotient of 13601 ÷ 87", "the remainder of 13601 ÷ 87", "13601 − 87"], 1,
                 "A remainder is exactly the bit that spoils a division. Take the remainder away, and what is left divides perfectly.")),
    B("So let's divide 13601 by 87, in chunks. 87 times 100 is 8700. That leaves 4901.",
      W("l2", "87 × 100 = 8700"), W("l3", "13601 − 8700 = 4901")),
    B("87 times 50 is 4350. That leaves 551.", W("l4", "87 × 50 = 4350"), W("l5", "4901 − 4350 = 551")),
    B("87 times 6 is 522. That leaves 29. And 29 is smaller than 87, so we stop here.", W("l6", "87 × 6 = 522"), W("l7", "551 − 522 = 29")),
    B("We used 100 and 50 and 6 lots of 87: that is 156 lots, with 29 left over.", W("l8", "13601 = 87 × 156 + 29"), M("l8", "29", "circle")),
    B("So take away the 29. What is left, 13572, is exactly 87 times 156.", ANS("l9", "13601 − 29 = 13572"), M("l9", "29", "circle")),
    B("The least number to subtract is always the remainder. Divide, and the leftover is your answer."),
)

LESSONS["EXT_G5_FP_2022_014"] = lesson(
    B("Four decimals made of 7s and 0s, placed to confuse the eye. Let's add them safely.",
      GIVEN("l1", "7.007 + 0.07 + 70.7 + 70.07")),
    B("Before adding decimals, what must we line up?",
      ask=choose(["the last digits", "the decimal points", "the first digits"], 1,
                 "Each digit must sit under digits of the same place: tenths under tenths, ones under ones. Lining up the points does exactly that.")),
    B("So write each one with three decimal places, padding with zeros. Now every point sits in the same spot.",
      W("p1", "7.007", label=True), W("p2", "0.070", label=True), W("p3", "70.700", label=True), W("p4", "70.070", label=True)),
    B("Add two at a time. 7.007 plus 0.07 is 7.077.", W("l2", "7.007 + 0.07 = 7.077")),
    B("Add 70.7 to that. The 7 tenths drop into the empty tenths place, and we get 77.777. All sevens!", W("l3", "7.077 + 70.7 = 77.777")),
    B("Last, add 70.07. Take care with the carries: 7 tens and 7 tens make more than 10 tens, so 1 goes into the hundreds place. We get 147.847.",
      ANS("l4", "77.777 + 70.07 = 147.847"), M("l4", "147.847", "circle")),
    B("A rough check. 7 plus 70 plus 70 is 147, and our answer is just a little more than that. Good.", W("l5", "7 + 70 + 70 = 147")),
    B("With decimals, line up the points, pad with zeros, and add place by place."),
)

LESSONS["EXT_G5_FP_2022_017"] = lesson(
    B("Fractions of numbers, a bracket, and a 2 standing right outside it. Remember that of means multiply.",
      GIVEN("l1", "5/6 of 72 − 2[2/5 of 40 + 1/9 of 27]")),
    B("Brackets first. Inside is 2 fifths of 40. How do we find 2 fifths of 40?",
      ask=choose(["40 ÷ 2, then × 5", "40 ÷ 5, then × 2", "40 − 5"], 1,
                 "Fifths means sharing into 5 equal parts. So divide 40 by 5 to get one fifth, then take 2 of those parts.")),
    B("40 divided by 5 is 8, and 2 of those make 16. And one ninth of 27 is 27 divided by 9, which is 3.",
      M("l1", "2/5 of 40"), W("l2", "2/5 of 40 = 16"), M("l1", "1/9 of 27"), W("l3", "1/9 of 27 = 3")),
    B("So the bracket is 16 plus 3, which is 19.", W("l4", "16 + 3 = 19"), W("l5", "5/6 of 72 − 2[19]")),
    B("Now the front. 5 sixths of 72: 72 divided by 6 is 12, and 5 of those make 60.",
      M("l5", "5/6 of 72"), W("l6", "72 ÷ 6 = 12"), W("l7", "5/6 of 72 = 60"), W("l8", "60 − 2 × 19")),
    B("We are down to 60 minus 2 times 19. Which part goes first?",
      ask=choose(["60 − 2", "2 × 19"], 1, "The 2 next to the bracket means times, and times comes before minus. So 2 times 19 goes first.")),
    B("2 times 19 is 38. And 60 minus 38 is 22.", W("l9", "2 × 19 = 38"), ANS("l10", "60 − 38 = 22"), M("l10", "22", "circle")),
    B("Read of as times. Do the bracket first, then times, and the minus right at the end."),
)

LESSONS["EXT_G5_FP_2022_021"] = lesson(
    B("This line is not true yet. One pair of brackets will make it equal 29.", GIVEN("l1", "6 ÷ 21 − 9 × 36 + 11 = 29", True)),
    B("Think backwards. If the plus 11 comes last, then everything before it must make 18. And there is a 36 in the line. What is 18 compared with 36?",
      W("l2", "29 − 11 = 18"),
      ask=choose(["double it", "half of it", "a third of it"], 1, "36 is 18 plus 18. So 18 is exactly half of 36.")),
    B("So we need half of 36. That means the part in front, 6 divided by something, should come to a half. 6 divided by 12 is a half.",
      W("l3", "6 ÷ 12 = 1/2")),
    B("Can we make 12 after the divide sign? Yes: 21 minus 9 is 12. So the brackets go round 21 minus 9.",
      W("l4", "6 ÷ (21 − 9) × 36 + 11"), M("l4", "(21 − 9)", "box")),
    B("Brackets first, giving 12. Then left to right: 6 divided by 12 is a half, and half of 36 is 18.",
      W("l5", "6 ÷ (21 − 9) × 36 + 11 = 6 ÷ 12 × 36 + 11"), W("l6", "6 ÷ 12 × 36 = 18")),
    B("And 18 plus 11 is 29. The line is true now.", ANS("l7", "6 ÷ (21 − 9) × 36 + 11 = 29"), M("l7", "(21 − 9)", "circle")),
    B("To place brackets, work backwards from the answer you need. Then look for numbers that can build the missing piece."),
)

LESSONS["EXT_G5_FP_2022_023"] = lesson(
    B("A two-digit number ending in 8, times a three-digit number ending in 6. The other digits are hidden. Which choice can be the product?",
      GIVEN("l1", "♣8 × ♣♣6 = ?", True), W("l2", "1808,  970608,  79764,  50808", label=True)),
    B("We cannot multiply hidden digits. But what can we say for certain about the product?",
      ask=choose(["its first digit", "its last digit", "nothing at all"], 1,
                 "The last digit of the product depends only on the last digits of the two numbers, and those are showing: 8 and 6.")),
    B("8 times 6 is 48, so the product must end in 8. That removes 79764, which ends in 4.",
      W("l3", "8 × 6 = 48"), M("l3", "8", "circle", 2), S("l2", "79764")),
    B("The other three all end in 8, so now test the size. The smallest numbers that fit are 18 and 106, and 18 times 106 is 1908.",
      W("l4", "18 × 106 = 1908")),
    B("1808 is below the smallest possible product, so it is out.", S("l2", "1808", "too small")),
    B("The biggest numbers that fit are 98 and 996, and 98 times 996 is 97608. That has five digits, so the six-digit 970608 is far too big.",
      W("l5", "98 × 996 = 97608"), S("l2", "970608", "too big")),
    B("Only 50808 is left. And it works: 58 times 876 is 50808.",
      W("l6", "58 × 876 = 50808"), ANS("l7", "The product can be 50808", True), M("l7", "50808", "circle")),
    B("Two tests for a hidden-digit product: the last digit, and then the smallest and biggest it could be."),
)

LESSONS["EXT_G5_FP_2022_024"] = lesson(
    B("We are given that 6.7 times 58 is 388.6. The new sum has the same digits, with the points in different places.",
      GIVEN("l1", "6.7 × 58 = 388.6"), W("l2", "0.67 × 5.8 = ?")),
    B("How did 6.7 turn into 0.67?",
      ask=choose(["it was divided by 100", "it was multiplied by 10", "it was divided by 10"], 2,
                 "The point moved one place to the left. That makes a number 10 times smaller, which is dividing by 10.")),
    B("6.7 was divided by 10. And 58 became 5.8, so it was divided by 10 as well.", W("l3", "0.67 = 6.7 ÷ 10"), W("l4", "5.8 = 58 ÷ 10")),
    B("Both numbers are 10 times smaller. So the product is 10 times 10 smaller, which is 100 times smaller.", W("l5", "10 × 10 = 100")),
    B("Dividing by 100 moves the point two places to the left. 388.6 becomes 3.886.",
      W("l6", "388.6 ÷ 100 = 3.886"), ANS("l7", "0.67 × 5.8 = 3.886"), M("l7", "3.886", "circle")),
    B("Does that feel right? About two thirds of nearly 6 should be close to 4. And 3.886 is."),
    B("Keep the digits from the fact you were given. Then work out how much smaller each number became, and shrink the answer by both."),
)

LESSONS["EXT_G5_FP_2023_001"] = lesson(
    B("Four big numbers to add. Before you start, look at the digits. Something is going on.",
      GIVEN("l1", "1234 + 2341 + 3412 + 4123"),
      FIG("f1", {"kind": "table", "headers": ["Th", "H", "T", "U"],
                 "rows": [["1", "2", "3", "4"], ["2", "3", "4", "1"], ["3", "4", "1", "2"], ["4", "1", "2", "3"]]})),
    B("Read down each column of the table. What do you notice?",
      ask=choose(["each holds one digit 4 times", "each holds 1, 2, 3, 4 in some order", "nothing special"], 1,
                 "Read down any column. You will find a 1, a 2, a 3 and a 4, just in a different order each time.")),
    B("So every column adds up to the same thing: 1 plus 2 plus 3 plus 4, which is 10.", W("l2", "1 + 2 + 3 + 4 = 10")),
    B("Units column: 10. Write 0, carry 1. Tens column: 10, plus the carried 1, is 11. Write 1, carry 1.",
      W("l3", "Units: 10, so write 0 and carry 1", label=True), W("l4", "10 + 1 = 11")),
    B("The hundreds do just the same: 11, write 1, carry 1. And the thousands make 11 as well, which we write in full.",
      W("l5", "Hundreds: 11.  Thousands: 11", label=True)),
    B("Reading the digits off: 11110.", ANS("l6", "1234 + 2341 + 3412 + 4123 = 11110"), M("l6", "11110", "circle")),
    B("Another way to see it. Every place holds 10, so the total is 10 lots of 1111.", W("l7", "10 × 1111 = 11110")),
    B("Before a big addition, look down the columns. A pattern can turn four long numbers into one small sum."),
)

LESSONS["EXT_G5_FP_2023_005"] = lesson(
    B("A product on top, divided by a sum underneath. Let's write the top and the bottom separately.",
      GIVEN("t", "1 × 2 × 3 × 4 × 5 × 6 × 7"), GIVEN("b", "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8")),
    B("Bottom first, it is easier. Pair the ends: 1 plus 8 is 9, and 2 plus 7 is 9 as well. Every pair makes 9. How many pairs do 8 numbers make?",
      ask=choose(["8", "4", "9"], 1, "Each pair uses up 2 numbers. So 8 numbers make 4 pairs.")),
    B("4 pairs of 9 make 36. So the bottom is 36.", W("l2", "4 × 9 = 36"), W("l3", "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 = 36")),
    B("Now the top. Don't multiply it out yet! We are going to divide by 36, and 36 is 6 times 6. The top has a 6. Which two other numbers on top make another 6?",
      ask=choose(["1 and 5", "2 and 3", "4 and 2"], 1, "2 times 3 is 6. So the 2, the 3 and the 6 on top multiply to 36 between them.")),
    B("So 2 times 3 times 6 is 36, and that cancels with the 36 underneath.",
      G("t", ["2", "3", "6"], "36"), W("l4", "2 × 3 × 6 = 36")),
    B("What is left on top? 1, 4, 5 and 7. 4 times 5 is 20, and 20 times 7 is 140.",
      W("l5", "4 × 5 = 20"), ANS("l6", "20 × 7 = 140"), M("l6", "140", "circle")),
    B("The long way agrees. The top multiplies out to 5040, and 5040 divided by 36 is 140.", W("l7", "5040 ÷ 36 = 140")),
    B("When a big product is divided by something, look for that something hiding among the factors. Cancel first, multiply after."),
)
