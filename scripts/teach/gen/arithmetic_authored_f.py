"""Hand-written lessons: past papers 2018 and 2019."""
from arithmetic_common import ANS, B, FIG, G, GIVEN, M, N, S, THINK, W, choose, lesson

LESSONS = {}

LESSONS["EXT_G5_FP_2018_003"] = lesson(
    B("We are given one fact, and asked a sum that looks very like it. Same digits, different decimal points.",
      GIVEN("l1", "15 × 0.005 = 0.075"), W("l2", "1.5 × 0.05 × 100 = ?")),
    B("Compare the two. 15 has become 1.5, which is 10 times smaller. And 0.005 has become 0.05. Is that bigger or smaller, and by how much?",
      ask=choose(["10 times smaller", "10 times bigger", "just the same"], 1,
                 "0.005 is 5 thousandths, and 0.05 is 5 hundredths. Hundredths are 10 times bigger than thousandths, so that number became 10 times bigger.")),
    B("One number went 10 times smaller, the other 10 times bigger. Those two changes cancel each other out, so the product stays the same.",
      W("l3", "1.5 = 15 ÷ 10"), W("l4", "0.05 = 0.005 × 10"), W("l5", "1.5 × 0.05 = 0.075")),
    B("Now the last part, times 100. Multiplying by 100 shifts every digit two places to the left, so the point seems to hop two places to the right.",
      M("l2", "× 100")),
    B("0.075 times 100 is 7.5.", ANS("l6", "0.075 × 100 = 7.5"), M("l6", "7.5", "circle")),
    B("A check on the middle step. 15 times 5 is 75, and 1.5 times 0.05 has three decimal places in it, so it is 0.075. Good.", W("l7", "15 × 5 = 75")),
    B("When a new sum has the same digits as a fact you know, don't start again. Just track how each number has grown or shrunk."),
)

LESSONS["EXT_G5_FP_2018_016"] = lesson(
    B("Four sums made from 19 and 5. Exactly one of them comes to 100.",
      GIVEN("l1", "Which is equal to 100?", True),
      W("a", "19 − 5 × 5"), W("b", "(19 − 5) × 5"), W("c", "(19 + 5) × 5"), W("d", "19 × 5 + 5")),
    B("The first one. Times goes before minus: 5 times 5 is 25. And 19 minus 25 drops below zero. Not 100.",
      M("a", "5 × 5"), W("a1", "19 − 5 × 5 = 19 − 25 = −6")),
    B("The second. Bracket first: 19 minus 5 is 14, and 14 times 5 is 70. Not 100.",
      M("b", "(19 − 5)", "box"), W("b1", "(19 − 5) × 5 = 14 × 5 = 70")),
    B("The third. 19 plus 5 is 24, and 24 times 5 is 120. Too big.", M("c", "(19 + 5)", "box"), W("c1", "(19 + 5) × 5 = 24 × 5 = 120")),
    B("That leaves the last one, 19 times 5 plus 5. Let's make sure. Which part goes first?",
      ask=choose(["5 + 5", "19 × 5"], 1, "Times comes before plus. Adding 5 and 5 first would turn it into 19 times 10, which is a different sum.")),
    B("19 times 5. An easy way: 20 times 5 is 100, then take away one 5. That leaves 95.",
      M("d", "19 × 5"), W("d1", "20 × 5 = 100"), W("d2", "100 − 5 = 95"), N("d", "19 × 5", "95")),
    B("And 95 plus 5 is 100. This is the one.", ANS("d3", "19 × 5 + 5 = 100"), M("d3", "100", "circle")),
    B("You can also see it in one glance: 19 fives and one more five make 20 fives. Work each choice in the proper order, and brackets first."),
)

LESSONS["EXT_G5_FP_2018_021"] = lesson(
    B("A long multiplication gives a number of minutes, and we want to know how many weeks that is.",
      GIVEN("l1", "8 × 7 × 6 × 5 × 4 × 3 × 2 × 1 minutes = ? weeks", True)),
    B("We could multiply it all out, but let's be clever and leave it as a product. First, how many minutes are in one week?",
      ask=choose(["7 × 60", "24 × 60", "7 × 24 × 60"], 2,
                 "A week is 7 days. Each day is 24 hours. Each hour is 60 minutes. So we multiply all three.")),
    B("Now hunt for those same pieces inside our product. There is a 7 already. And 6 times 4 makes the 24.",
      W("l2", "1 week = 7 × 24 × 60 minutes", label=True), M("l1", "7", "circle"), G("l1", ["6", "4"], "24"), W("l3", "6 × 4 = 24")),
    B("What is left over? 8, 5, 3, 2 and 1. 8 times 5 is 40. Then 40 times 3 times 2 is 240.",
      W("l4", "8 × 5 = 40"), W("l5", "40 × 3 × 2 × 1 = 240")),
    B("And 240 is 60 times 4. So there is our 60, with a 4 to spare.", W("l6", "240 = 60 × 4")),
    B("So our product is 7 times 24 times 60, and then times 4. How many weeks is that?",
      ask=choose(["240", "4", "8"], 1, "We matched the 7, the 24 and the 60 that make one week, and a 4 was left over. So it is 4 lots of a week.")),
    B("It is 4 weeks.", ANS("l7", "7 × 24 × 60 × 4 minutes = 4 weeks", True), M("l7", "4 weeks", "circle")),
    B("The long way agrees. The product is 40320 minutes, a week is 10080 minutes, and 40320 divided by 10080 is 4.",
      W("l8", "7 × 24 × 60 = 10080"), W("l9", "40320 ÷ 10080 = 4")),
    B("When a big product has to be divided, look for the divisor's pieces hiding inside it before you multiply anything out."),
)

LESSONS["EXT_G5_FP_2018_028"] = lesson(
    B("A man bought some articles, counted in dozens. One of these decimals cannot be right. Which?",
      GIVEN("l1", "Dozens of articles: which one is impossible?", True), W("l2", "3.75,  3.25,  3.15,  3.5", label=True)),
    B("You can only buy whole articles. So when we turn the dozens into single articles, the answer must be a whole number. How do we turn dozens into articles?",
      ask=choose(["divide by 12", "multiply by 10", "multiply by 12"], 2,
                 "Each dozen is 12 articles. So the number of articles is the number of dozens times 12.")),
    B("The 3 whole dozens are fine in every choice: that is 36 articles. So only the part after the point needs testing.", W("l3", "3 × 12 = 36")),
    B("0.75 of a dozen is three quarters of 12, which is 9. Whole. 0.25 is a quarter of 12, which is 3. Whole. And 0.5 is half of 12, which is 6. Whole.",
      W("l4", "0.75 × 12 = 9"), W("l5", "0.25 × 12 = 3"), W("l6", "0.5 × 12 = 6")),
    B("Now the last one, 0.15 of a dozen. Will that be a whole number of articles? Have a guess before we work it out.",
      W("l6b", "0.15 × 12 = ?"), ask=THINK),
    B("0.15 times 12 comes to 1.8. Nobody can buy 1.8 of an article!", W("l7", "0.15 × 12 = 1.8"), M("l7", "1.8")),
    B("So 3.15 dozen would mean 37.8 articles, and that cannot happen. 3.15 is the impossible one.",
      ANS("l8", "3.15 × 12 = 37.8"), M("l8", "3.15", "circle"), S("l2", "3.15")),
    B("A count of things must be whole. Change the dozens into single items, and see whether it comes out whole."),
)

LESSONS["EXT_G5_FP_2018_032"] = lesson(
    B("A three-digit number ending in 7, times a two-digit number ending in 8. Clubs hide the other digits. Which choice can be the product?",
      GIVEN("l1", "♣♣7 × ♣8 = ?", True), W("l2", "1906,  977706,  29405,  52606", label=True)),
    B("We can see only the last digits, 7 and 8. What must the product end in?",
      ask=choose(["5", "6", "8"], 1, "The last digit of a product comes from the last digits multiplied together. Work out 7 times 8, and look at the digit it ends in.")),
    B("7 times 8 is 56, so the product ends in 6. That removes 29405, which ends in 5.",
      W("l3", "7 × 8 = 56"), M("l3", "6", "circle"), S("l2", "29405")),
    B("Three are left, all ending in 6. So test the size. The smallest numbers that fit are 107 and 18, and 107 times 18 is 1926.",
      W("l4", "107 × 18 = 1926")),
    B("1906 is smaller than that, so it is out. Only just, but out.", S("l2", "1906", "too small")),
    B("The biggest numbers that fit are 997 and 98. 997 times 98 is 97706. So what about 977706?", W("l5", "997 × 98 = 97706"),
      ask=choose(["It is possible", "It is too big"], 1,
                 "Count the digits. The biggest possible product, 97706, has five digits. 977706 has six, so it is far too big.")),
    B("Cross out 977706. Only 52606 is left, and it does work: 907 times 58 is 52606.",
      S("l2", "977706", "too big"), W("l6", "907 × 58 = 52606"), ANS("l7", "The product can be 52606", True), M("l7", "52606", "circle")),
    B("Last digit first, then smallest and biggest. Those two tests sort out almost every hidden-digit product."),
)

LESSONS["EXT_G5_FP_2018_037"] = lesson(
    B("This line is not true yet. We need to slip in one pair of brackets so that it really equals 40.",
      GIVEN("l1", "3 × 25 − 13 + 4 = 40", True)),
    B("As it stands, 3 times 25 is 75, and 75 minus 13 plus 4 is 66. Too big. So the brackets must bring it down.",
      W("l2a", "3 × 25 = 75"), W("l2", "3 × 25 − 13 + 4 = 66")),
    B("Let's think backwards from 40. If the plus 4 comes last, then just before it we had 36. And 36 is 3 times what?",
      W("l3", "40 − 4 = 36"),
      ask=choose(["13", "12", "33"], 1, "Go up the 3 times table. You reach 36 at 3 times 12.")),
    B("So we want the 3 to multiply 12. Can we make 12 from the numbers that follow? Yes: 25 minus 13 is 12. Put the brackets there.",
      W("l4", "3 × (25 − 13) + 4"), M("l4", "(25 − 13)", "box")),
    B("Brackets first: 25 minus 13 is 12. Then times: 3 times 12 is 36.",
      W("l5", "3 × (25 − 13) + 4 = 3 × 12 + 4"), W("l6", "3 × 12 + 4 = 36 + 4")),
    B("And 36 plus 4 is 40. The line is true now.", ANS("l7", "3 × (25 − 13) + 4 = 40"), M("l7", "(25 − 13)", "circle")),
    B("The other choices do not work. Brackets round 3 times 25 change nothing. Round 13 plus 4 we get 58, and the long bracket gives 48.",
      W("l8", "3 × 25 − (13 + 4) = 58"), W("l9", "3 × (25 − 13 + 4) = 48")),
    B("To place brackets, work backwards from the answer you need, and look for the numbers that can make it."),
)

LESSONS["EXT_G5_FP_2019_003"] = lesson(
    B("Five decimals. We put them in descending order, biggest first, and then add the 1st and the 4th.",
      GIVEN("l1", "0.062,  0.05,  0.56,  0.034,  0.007", True)),
    B("To compare decimals fairly, give them all the same number of decimal places. The longest have 3 places, so we pad the others with zeros.",
      W("l2", "0.062,  0.050,  0.560,  0.034,  0.007", label=True)),
    B("Now every one is a number of thousandths. Which is the biggest?", W("l3", "thousandths: 62, 50, 560, 34, 7", label=True),
      ask=choose(["0.062", "0.560", "0.050"], 1,
                 "Read them as thousandths: 62, 50, 560, 34 and 7. The biggest of those is 560, so 0.560 is the biggest decimal.")),
    B("Descending order means biggest first. So: 560, 62, 50, 34, 7 thousandths.",
      W("l4", "0.560,  0.062,  0.050,  0.034,  0.007", label=True)),
    B("The 1st is 0.560, which is our 0.56. Count along to the 4th, and it is 0.034.",
      M("l4", "0.560", "circle"), M("l4", "0.034", "circle")),
    B("Add them. 560 thousandths plus 34 thousandths is 594 thousandths. That is 0.594.",
      W("l5", "560 + 34 = 594"), ANS("l6", "0.56 + 0.034 = 0.594"), M("l6", "0.594", "circle")),
    B("The trap was to think 0.062 beats 0.56 because it has more digits. Line up the decimal places and that trap disappears."),
    B("To order decimals, pad them to the same length. Then compare them like whole numbers."),
)

LESSONS["EXT_G5_FP_2019_010"] = lesson(
    B("This line is not true as it stands. One pair of brackets will make it equal 33.", GIVEN("l1", "12 − 7 × 5 + 8 = 33", True)),
    B("Without brackets, times goes first. 7 times 5 is 35, and 12 minus 35 already drops below zero. Nowhere near 33.",
      W("l2", "7 × 5 = 35")),
    B("So think backwards from 33. If the plus 8 comes last, then just before it we had 25. And 25 is 5 times what?",
      W("l3", "33 − 8 = 25"),
      ask=choose(["4", "5", "7"], 1, "5 times 5 is 25. So we need a 5 to be sitting in front of the times 5.")),
    B("We need a 5 in front of the times 5. And look: 12 minus 7 is 5! So the brackets go round 12 minus 7.",
      W("l4", "(12 − 7) × 5 + 8"), M("l4", "(12 − 7)", "box")),
    B("Brackets first: 12 minus 7 is 5. Then 5 times 5 is 25.", W("l5", "(12 − 7) × 5 + 8 = 5 × 5 + 8"), W("l6", "5 × 5 + 8 = 25 + 8")),
    B("And 25 plus 8 is 33. The line is true now.", ANS("l7", "(12 − 7) × 5 + 8 = 33"), M("l7", "(12 − 7)", "circle")),
    B("What about the other choices? Brackets round 7 times 5 change nothing. The other two only make the amount we subtract bigger, so they sink below zero as well."),
    B("To place brackets, work backwards from the answer, and see which numbers can build what you need."),
)

LESSONS["EXT_G5_FP_2019_013"] = lesson(
    B("A basket of 104 mangoes. Again and again we take out 4 mangoes and put in 3 apples, until no mangoes are left. How many apples then?",
      GIVEN("l1", "104 mangoes. Each swap: 4 mangoes out, 3 apples in", True)),
    B("First, how many swaps does it take to clear out all the mangoes?",
      ask=choose(["104 − 4", "104 ÷ 4", "104 × 3"], 1,
                 "Each swap removes 4 mangoes. So we need to know how many 4s there are in 104, and that is a division.")),
    B("100 divided by 4 is 25, and the 4 that is left makes one more group. So 104 divided by 4 is 26 swaps.",
      W("l2", "100 ÷ 4 = 25"), W("l3", "104 ÷ 4 = 26"), M("l3", "26")),
    B("Every swap puts 3 apples in. So how do we find the number of apples?",
      ask=choose(["26 + 3", "104 × 3", "26 × 3"], 2, "There are 26 swaps, and each one adds 3 apples. That is 26 lots of 3.")),
    B("26 times 3. 20 times 3 is 60, 6 times 3 is 18, and together that is 78 apples.",
      W("l4", "26 × 3 = 20 × 3 + 6 × 3"), W("l5", "60 + 18 = 78"), ANS("l6", "26 × 3 = 78"), M("l6", "78", "circle")),
    B("Does 78 make sense? Yes. Only 3 apples go in for every 4 mangoes that come out, so there should be fewer apples than there were mangoes."),
    B("Count the swaps first, by dividing. Then multiply by what each swap brings in."),
)

LESSONS["EXT_G5_FP_2019_026"] = lesson(
    B("A round bracket inside a curly bracket, and then a little minus 4 on the end.", GIVEN("l1", "{(4 + 2 × 6) ÷ 4} − 4")),
    B("What is the very first thing to work out?",
      ask=choose(["4 + 2", "2 × 6", "÷ 4"], 1,
                 "We start inside the innermost bracket. And in there, times goes before plus. So 2 times 6 is the very first step.")),
    B("2 times 6 is 12. Then 4 plus 12 is 16. The round bracket is done.",
      M("l1", "2 × 6"), N("l1", "2 × 6", "12"), W("l2", "4 + 2 × 6 = 4 + 12 = 16"), W("l3", "{16 ÷ 4} − 4")),
    B("Now the curly bracket. 16 divided by 4 is 4.", M("l3", "{16 ÷ 4}", "box"), N("l3", "{16 ÷ 4}", "4"), W("l4", "4 − 4")),
    B("And 4 minus 4 is 0.", ANS("l5", "4 − 4 = 0"), M("l5", "0", "circle")),
    B("Here is the trap they set. Adding 4 and 2 first gives 6 times 6, which is 36. Carry on from there and you reach 5, which is one of the choices!",
      W("l6", "(4 + 2) × 6 = 36")),
    B("Inside a bracket the same order still applies: times and divide before plus and minus. Then move outwards, bracket by bracket."),
)

LESSONS["EXT_G5_FP_2019_027"] = lesson(
    B("We want to write 12 minutes as a decimal part of an hour.", GIVEN("l1", "12 minutes = ? of an hour", True)),
    B("First as a fraction. 12 minutes is what fraction of an hour?",
      ask=choose(["12/100", "12/60", "12/10"], 1, "An hour has 60 minutes, not 100. So 12 minutes is 12 out of 60.")),
    B("12 goes into 60 exactly 5 times. So 12 minutes is one fifth of an hour.",
      W("l2", "12/60 = 1/5"), FIG("f1", {"kind": "fractionBars", "shape": "circle", "bars": [{"parts": 5, "shaded": 1, "label": "1/5 of an hour"}]})),
    B("Now one fifth as a decimal. Decimals like tenths, so change it: one fifth is the same as 2 tenths, and 2 tenths is 0.2.",
      W("l3", "1/5 = 2/10 = 0.2")),
    B("The choices show it as 0.20. That is the same number: a zero on the end of a decimal changes nothing.",
      ANS("l4", "12/60 = 0.20"), M("l4", "0.20", "circle")),
    B("Check: 0.2 of 60 minutes is 12 minutes. Yes.", W("l5", "0.2 × 60 = 12")),
    B("The tempting slip is to write the 12 straight after the point. But minutes are sixtieths of an hour, so always divide by 60."),
)

LESSONS["EXT_G5_FP_2019_038"] = lesson(
    B("A college has girls and boys, in a commerce stream and a science stream. Lots of numbers, so let's take them one at a time.",
      GIVEN("l1", "Girls = 735, which is 145 less than the boys", True), W("l2", "Commerce: 435 boys + 375 girls", label=True)),
    B("The girls are 145 less than the boys. So how do we find the number of boys?",
      ask=choose(["735 − 145", "735 + 145"], 1,
                 "The girls are the smaller group. So the boys are 145 more than the girls: start from 735 and add 145.")),
    B("735 plus 145 is 880. There are 880 boys.", W("l3", "735 + 145 = 880")),
    B("So the whole college is 880 boys plus 735 girls. That is 1615 students.", W("l4", "880 + 735 = 1615"), M("l4", "1615")),
    B("The commerce stream has 435 boys and 375 girls, which is 810 students.", W("l5", "435 + 375 = 810"), M("l5", "810")),
    B("Everyone who is not in commerce is in science. 1615 minus 810 is 805.", ANS("l6", "1615 − 810 = 805"), M("l6", "805", "circle")),
    B("Let's check another way. Science boys: 880 minus 435 is 445. Science girls: 735 minus 375 is 360. And 445 plus 360 is 805.",
      W("l7", "880 − 435 = 445"), W("l8", "735 − 375 = 360"), W("l9", "445 + 360 = 805")),
    B("In a long word problem, find one missing number at a time. And watch which group is the bigger one when you read less than."),
)
