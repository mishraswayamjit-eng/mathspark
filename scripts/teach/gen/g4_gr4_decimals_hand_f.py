"""Lessons written for single questions: past papers PYQ_... and Q_CH11_001-005."""
from g4_gr4_decimals_lib import (ANS, CHART, FIG, GIVEN, GM, NOTE, RING, STRIKE, T, UL, W, WL, figure_of)

LESSONS = {}

# ── PYQ_2016_Q02: difference between 9.07 and 7.9 ───────────────────────────
t = T("PYQ_2016_Q02")
t.say("We want the difference between 9.07 and 7.9.",
      GIVEN("q", "Difference between 9.07 and 7.9 = ?"), FIG("f", figure_of("PYQ_2016_Q02")))
t.ask("The word difference tells us what to do. What is it?",
      "subtract", ["add", "multiply"],
      "The difference is how far apart two numbers are. To find it, we take the smaller one away from the bigger one.")
t.say("9.07 has two digits after the point, and 7.9 has only one. So write 7.9 as 7.90, and put the points in line.",
      W("e", "7.9 = 7.90"), W("s", "9.07 − 7.90 = ?"))
t.say("Start at the hundredths. 7 take away 0 is 7.")
t.ask("Now the tenths: 0 take away 9. We cannot do that. So what do we do?",
      "borrow 1 from the ones", ["just write 9", "do 9 − 0 instead"],
      "0 tenths is less than 9 tenths, so we borrow 1 whole from the 9 ones. One whole is the same as 10 tenths.")
t.say("Now we have 10 tenths, and 10 take away 9 is 1. In the ones, 8 are left after the borrowing, and 8 take away 7 is 1.",
      W("t1", "10 − 9 = 1"), W("o", "8 − 7 = 1"), NOTE("s", "9.07", "8 ones left"))
t.say("So the difference is 1.17.", ANS("a", "9.07 − 7.90 = 1.17"), RING("a", "1.17"))
t.say("Check by adding back: 7.90 plus 1.17 makes 9.07. Line up the points, fill the gap with a zero, and remember what you borrowed.",
      W("c", "7.90 + 1.17 = 9.07"))
t.done(LESSONS)

# ── PYQ_2016_Q30: smallest + greatest of 0.023, 0.23, 0.0023, 2.3 ───────────
t = T("PYQ_2016_Q30")
t.say("Four numbers, all made from a 2 and a 3. We must find the smallest and the greatest, and then add those two.",
      GIVEN("q", "0.023, 0.23, 0.0023, 2.3"), GIVEN("q2", "Smallest + greatest = ?"))
t.say("The digits are the same each time, but they sit in different places. Let's give every number four digits after the point.",
      FIG("f", figure_of("PYQ_2016_Q30", 0)))
t.ask("Which number is the greatest?",
      "2.3", ["0.23", "0.0023"],
      "2.3 is the only one with a whole number part. All the others are less than 1.")
t.say("2.3 has 2 wholes, so it is the greatest. It is also the shortest number here, so do not judge by length.", UL("q", "2.3"))
t.ask("And which number is the smallest?",
      "0.0023", ["0.023", "0.23"],
      "The more zeros there are straight after the point, the smaller the number. 0.0023 has two zeros before its 2.")
t.say("The smallest is 0.0023, and the greatest is 2.3.", FIG("f", figure_of("PYQ_2016_Q30", 1)))
t.say("Now add them. Write 2.3 as 2.3000, so the points line up. The 2 and the 3 of 0.0023 drop into the last two places.",
      W("e", "2.3 = 2.3000"), W("s", "2.3000 + 0.0023 = 2.3023"))
t.say("So the sum is 2.3023.", ANS("a", "0.0023 + 2.3 = 2.3023"), RING("a", "2.3023"))
t.say("Keep the zeros in their places when you add, or the digits slip. Same number of places first, then compare, then add.")
t.done(LESSONS)

# ── PYQ_2017_Q07: change from Rs. 50 for Rs. 39.46 ──────────────────────────
t = T("PYQ_2017_Q07")
t.say("Mrs. Joshi's groceries cost 39.46 rupees. She gives the cashier a 50 rupee note. How much comes back?",
      GIVEN("q", "Groceries Rs. 39.46. Pays Rs. 50. Change = ?"), FIG("f", figure_of("PYQ_2017_Q07")))
t.ask("Which sum gives the change?",
      "50 − 39.46", ["50 + 39.46", "39.46 − 50"],
      "The change is what is left of the 50 rupees after the bill is paid. So we take the bill away from 50.")
t.say("Shopkeepers do this by counting up. We go from 39.46 up to 40 first, and then from 40 up to 50.",
      WL("p", "39.46  →  40  →  50"), W("p2", "39.46 = 39 + 0.46"))
t.ask("How far is it from 39.46 up to 40?",
      "0.54", ["0.44", "0.64"],
      "Look at the part after the point, 0.46. Together, 0.46 and 0.54 make exactly 1 whole rupee. With 0.44 we would stop a little short of 40.")
t.say("From 39.46 up to 40 is 0.54.", W("u1", "39.46 + 0.54 = 40"), FIG("f", figure_of("PYQ_2017_Q07", 1)))
t.say("And from 40 up to 50 is 10 more.", W("u2", "40 + 10 = 50"))
t.say("Put the two jumps together: 10 and 0.54. The cashier returns 10.54 rupees.",
      ANS("a", "50 − 39.46 = 10.54"), RING("a", "10.54"))
t.say("Check: 39.46 plus 10.54 makes 50. And it makes sense: 39.46 is nearly 40, so the change should be just over 10.",
      W("c", "39.46 + 10.54 = 50"))
t.done(LESSONS)

# ── PYQ_2017_Q17: 0.97 written instead of 9.7 ───────────────────────────────
t = T("PYQ_2017_Q17")
t.say("A student should have written 9.7, but he wrote 0.97. By how much was his number off?",
      GIVEN("q", "Wrote 0.97 instead of 9.7. Off by = ?"), FIG("f", figure_of("PYQ_2017_Q17")))
t.ask("How do we find how far apart the two numbers are?",
      "9.7 − 0.97", ["9.7 + 0.97", "9.7 ÷ 0.97"],
      "How far off means the difference between them. We take the smaller number away from the bigger one.")
t.say("First a quick guess. 9.7 is nearly 10, and 0.97 is nearly 1. So the gap should be somewhere near 9.",
      W("est", "10 − 1 = 9"))
t.say("Now exactly. Write 9.7 as 9.70, so both numbers have two digits after the point.",
      W("e", "9.7 = 9.70"), W("s", "9.70 − 0.97 = ?"))
t.ask("Here is a clever way. 0.97 is nearly 1, so take away a whole 1 first. That gives 8.70. But how much too much did we take?",
      "0.03", ["0.97", "0.3"],
      "1 is just 3 hundredths more than 0.97. So we took away 0.03 too much.",
      W("v1", "9.70 − 1 = 8.70"))
t.say("We took 0.03 too much, so we give it back. 8.70 and 0.03 make 8.73.", W("v2", "8.70 + 0.03 = 8.73"))
t.say("So his number was off by 8.73.", ANS("a", "9.70 − 0.97 = 8.73"), RING("a", "8.73"))
t.say("Check: 0.97 plus 8.73 makes 9.70. And 8.73 is near our guess of 9, so the decimal point is in the right place.",
      W("c", "0.97 + 8.73 = 9.70"))
t.done(LESSONS)

# ── PYQ_2017_Q25: for how many digits d is 2.00d5 > 2.005 (Hard) ────────────
t = T("PYQ_2017_Q25")
t.say("The letter d stands for one digit. We want to know for how many digits the number 2.00d5 is greater than 2.005.",
      GIVEN("q", "d is a digit.  2.00d5 > 2.005"), GIVEN("q2", "How many values of d work?"))
t.say("2.00d5 has four digits after the point. So write 2.005 with four digits as well, by adding a zero at the end.",
      W("e", "2.005 = 2.0050"), WL("cmp", "2.00d5   and   2.0050"))
t.say("Now compare from the left, one place at a time. The ones match. The tenths match. The hundredths match. The first place that can differ is the thousandths: d against 5.",
      UL("cmp", "d"), UL("cmp", "5", nth=2))
t.ask("If d is bigger than 5, our number is greater. How many digits are bigger than 5?",
      "4", ["5", "3"],
      "The digits bigger than 5 are 6, 7, 8 and 9. Count them: there are 4.")
t.say("So 6, 7, 8 and 9 all work. But we are not finished. What if d is 5 itself?",
      WL("w", "d = 6, 7, 8, 9 work"), WL("x0", "d = 5:   2.0055   and   2.0050"))
t.ask("With d as 5, the number is 2.0055. How does it compare with 2.0050?",
      "2.0055 is greater", ["they are equal", "2.0055 is smaller"],
      "The first three places after the point match. So look at the last place: 5 against 0. 5 is more, so 2.0055 is greater.")
t.say("That is the trap. When d is 5 the thousandths are level, but the last digit, 5, beats the 0. So 5 works too.",
      W("x", "2.0055 > 2.0050"))
t.say("And if d is 4, we get 2.0045, which is less than 2.0050. Smaller digits are no good either.", W("y", "2.0045 < 2.0050"))
t.say("So d can be 5, 6, 7, 8 or 9. That is 5 values.",
      ANS("a", "d = 5, 6, 7, 8, 9: that is 5 values", label=True), RING("a", "5 values"))
t.say("Give both numbers the same number of places, compare from the left, and always test the digit that makes them level.")
t.done(LESSONS)

# ── PYQ_2018_Q06: the smallest decimal fraction ─────────────────────────────
t = T("PYQ_2018_Q06")
t.say("Here are four decimals. Which one is the smallest?",
      GIVEN("q", "Which is the smallest?"), GIVEN("o", "0.007    0.07    7.07    0.70"))
t.say("Each one is made of 7s and zeros. What matters is the place where each 7 sits. Let's give them all three digits after the point.",
      FIG("f", figure_of("PYQ_2018_Q06", 0)))
t.ask("In which number does the 7 sit in the smallest place?",
      "0.007", ["0.07", "0.70"],
      "After the point the places get smaller and smaller: tenths, hundredths, thousandths. In 0.007 the 7 is in the thousandths, the smallest place here.")
t.say("Read them all as thousandths: 7, then 70, then 7070, then 700. The smallest of those is 7.",
      WL("k", "thousandths: 7, 70, 7070, 700"))
t.ask("One of the four is far bigger than all the rest. Which one?",
      "7.07", ["0.70", "0.07"],
      "7.07 is the only one with whole ones in front of the point. All the others are less than 1.")
t.say("7.07 has 7 whole ones, so it is the biggest by far. And the smallest is 0.007.",
      STRIKE("o", "7.07", "7 wholes: biggest"), ANS("a", "0.007 < 0.07 < 0.70 < 7.07"), RING("a", "0.007"),
      FIG("f", figure_of("PYQ_2018_Q06", 2)))
t.say("A decimal is not smaller just because it is shorter. 0.07 is shorter than 0.007, but it is ten times as big. Look at the place, not the length.")
t.done(LESSONS)

# ── PYQ_2018_Q08: place value of 5 in 7.256 ─────────────────────────────────
t = T("PYQ_2018_Q08")
t.say("Here is 7.256 in a place-value chart. We want the place value of the digit 5.",
      GIVEN("q", "Place value of the digit 5 in 7.256 = ?"), CHART("f", "7.256"))
t.ask("The first place after the point is the tenths place. Which digit is sitting there?",
      "2", ["5", "7"],
      "Find the decimal point, then look at the very next digit. It is the 2.")
t.say("After the tenths come the hundredths, and then the thousandths. So we have 2 tenths, 5 hundredths and 6 thousandths.",
      FIG("f", figure_of("PYQ_2018_Q08", 1)))
t.ask("So the 5 stands for 5 hundredths. How do we write 5 hundredths as a fraction?",
      "5/100", ["5/10", "5/1000"],
      "Hundredths means parts out of 100. So 5 hundredths is 5 over 100.")
t.say("The place value of the 5 is 5 over 100.",
      ANS("a", "Place value of 5 = 5/100", label=True), RING("a", "5/100"), W("d", "5/100 = 0.05"))
t.say("If the 5 were on the left of the point, it would be worth far more. Here it is after the point, in the second place, so it is only 5 hundredths.")
t.say("After the point, count the places: tenths, hundredths, thousandths. The name of the place gives you the bottom of the fraction.")
t.done(LESSONS)

# ── PYQ_2019_Q01: 9 1/8 as a decimal ────────────────────────────────────────
t = T("PYQ_2019_Q01")
t.say("We want to write 9 and one eighth as a decimal.",
      GIVEN("q", "Write 9 1/8 as a decimal"), FIG("f", figure_of("PYQ_2019_Q01")))
t.say("The 9 wholes stay just as they are. Only the fraction part, one eighth, has to be changed.", UL("q", "1/8"))
t.ask("Let's turn one eighth into thousandths. 8 times what makes 1000?",
      "125", ["100", "12.5"],
      "8 times 100 is not enough. 8 times 125 makes exactly 1000.",
      W("m", "8 × ? = 1000"))
t.say("So multiply the top and the bottom by 125. One eighth is 125 thousandths.",
      W("f1", "1/8 = 125/1000"), NOTE("f1", "1/8", "× 125 top and bottom", "below"))
t.ask("How do we write 125 thousandths as a decimal?",
      "0.125", ["1.25", "0.0125"],
      "Thousandths take three digits after the point. So 125 thousandths is 0.125.")
t.say("Now put the 9 wholes back. 9 and 0.125 make 9.125.",
      W("s", "9 + 0.125 = 9.125"), ANS("a", "9 1/8 = 9.125", label=True), RING("a", "9.125"))
t.say("The trap is to write the 1 and the 8 straight after the point. A fraction is a division, so we have to work it out.")
t.say("Another way to see it: one quarter is 0.25, and one eighth is half of that. Keep the whole number, and change only the fraction.",
      W("h", "0.25 ÷ 2 = 0.125"))
t.done(LESSONS)

# ── PYQ_2019_Q19: 0.0357 × 100 ──────────────────────────────────────────────
t = T("PYQ_2019_Q19")
t.say("We multiply the decimal 0.0357 by 100.", GM("q", "0.0357 × 100 = ?"))
t.ask("100 has two zeros. So what does multiplying by 100 do to the digits?",
      "moves them 2 places left", ["moves them 2 places right", "moves them 1 place left"],
      "Multiplying makes a number bigger, so the digits move left, into bigger places. Two zeros means two places.")
t.say("Let's go one place at a time. One place to the left: 0.0357 becomes 0.357.",
      W("s1", "0.0357 × 10 = 0.357"), FIG("f", figure_of("PYQ_2019_Q19", 1)))
t.ask("Now one more place to the left. What does 0.357 become?",
      "3.57", ["35.7", "3.057"],
      "Each digit moves just one place more. The 3 moves from the tenths into the ones, and no new digit appears between the others.")
t.say("0.357 becomes 3.57. So the answer is 3.57.",
      W("s2", "0.357 × 10 = 3.57"), FIG("f", figure_of("PYQ_2019_Q19", 2)),
      ANS("a", "0.0357 × 100 = 3.57"), RING("a", "3.57"))
t.say("Look at the digits: 3, 5, 7, in the same order, with nothing new between them. Only their places have changed.")
t.say("A quick check: 0.0357 is close to 0.04, and 0.04 times 100 is 4. Our 3.57 is near 4. To multiply by 100, move every digit two places to the left.",
      W("c", "0.04 × 100 = 4"))
t.done(LESSONS)

# ── Q_CH11_001: 12.5 ÷ 10 ───────────────────────────────────────────────────
t = T("Q_CH11_001")
t.say("Here is 12.5 in a place-value chart. We want to divide it by 10.",
      GM("q", "12.5 ÷ 10 = ?"), FIG("f", figure_of("Q_CH11_001")))
t.ask("What does dividing by 10 do to a number?",
      "makes it 10 times smaller", ["makes it 10 times bigger", "leaves it the same"],
      "Dividing shares a number out, so it gets smaller. Dividing by 10 makes it 10 times smaller.")
t.say("So every digit becomes worth ten times less. That means every digit moves one place to the right.")
t.ask("The 2 is in the ones place now. Where does it go?",
      "the tenths place", ["the tens place", "the hundredths place"],
      "One place to the right of the ones is the tenths place, just after the decimal point.")
t.say("The 1 ten becomes 1 one. The 2 ones become 2 tenths. The 5 tenths become 5 hundredths. That makes 1.25.",
      FIG("f", figure_of("Q_CH11_001", 2)))
t.say("So 12.5 divided by 10 is 1.25.", ANS("a", "12.5 ÷ 10 = 1.25"), RING("a", "1.25"))
t.say("Check by multiplying back: 1.25 times 10 is 12.5. One zero in 10, so the digits move one place.",
      W("c", "1.25 × 10 = 12.5"))
t.done(LESSONS)

# ── Q_CH11_002: 12.5 ÷ 100 ──────────────────────────────────────────────────
t = T("Q_CH11_002")
t.say("This time we divide 12.5 by 100.", GM("q", "12.5 ÷ 100 = ?"), FIG("f", figure_of("Q_CH11_002")))
t.ask("100 has two zeros. How many places do the digits move to the right?",
      "2 places", ["1 place", "3 places"],
      "Each zero stands for one division by 10, and each division by 10 moves the digits one place. Two zeros, two places.")
t.say("Let's take one place at a time. One place to the right: 12.5 becomes 1.25.", W("s1", "12.5 ÷ 10 = 1.25"))
t.ask("Now one more place to the right. What does 1.25 become?",
      "0.125", ["0.0125", "12.5"],
      "The 1 moves from the ones into the tenths. Nothing is left in the ones place, so we write a 0 there.")
t.say("1.25 becomes 0.125. The ones place is empty now, so a zero stands in front of the point.",
      W("s2", "1.25 ÷ 10 = 0.125"), FIG("f", figure_of("Q_CH11_002", 2)))
t.say("So 12.5 divided by 100 is 0.125.", ANS("a", "12.5 ÷ 100 = 0.125"), RING("a", "0.125"))
t.say("Check: 0.125 times 100 takes us back to 12.5. Count the zeros, and move the digits that many places to the right.",
      W("c", "0.125 × 100 = 12.5"))
t.done(LESSONS)

# ── Q_CH11_003: 12.5 ÷ 10000 ────────────────────────────────────────────────
t = T("Q_CH11_003")
t.say("Now a big one: 12.5 divided by 10000.", GM("q", "12.5 ÷ 10000 = ?"), FIG("f", figure_of("Q_CH11_003")))
t.ask("How many zeros does 10000 have?",
      "4", ["3", "5"],
      "Count them one by one after the 1. There are 4 zeros.")
t.say("So dividing by 10000 is like dividing by 10 four times. Each time, every digit moves one place to the right.")
t.say("The first two moves: 12.5 becomes 1.25, and then 1.25 becomes 0.125.",
      W("s1", "12.5 ÷ 10 = 1.25"), W("s2", "1.25 ÷ 10 = 0.125"))
t.ask("The third move. What does 0.125 become?",
      "0.0125", ["0.00125", "0.1250"],
      "Every digit moves one place to the right, and a zero fills the empty tenths place. So 0.125 becomes 0.0125.")
t.say("That is three moves. One more to go: 0.0125 becomes 0.00125. Each move puts one more zero after the point.",
      W("s3", "0.125 ÷ 10 = 0.0125"), W("s4", "0.0125 ÷ 10 = 0.00125"))
t.say("So 12.5 divided by 10000 is 0.00125.", ANS("a", "12.5 ÷ 10000 = 0.00125"), RING("a", "0.00125"))
t.say("Check: 0.00125 times 10000 is 12.5. It is easy to move one place too few or too many, so count the zeros and count your moves.",
      W("c", "0.00125 × 10000 = 12.5"))
t.done(LESSONS)

# ── Q_CH11_004: 28 ÷ 5 ──────────────────────────────────────────────────────
t = T("Q_CH11_004")
t.say("28 divided by 5. This one does not come out as a whole number, so we will need a decimal.", GM("q", "28 ÷ 5 = ?"))
t.ask("How many whole fives fit into 28?",
      "5", ["6", "4"],
      "Count in fives up to 28. Five fives fit, but six fives would go past 28.")
t.say("5 fives are 25. That leaves 3 ones over.", W("d1", "5 × 5 = 25"), W("d2", "28 − 25 = 3"))
t.ask("What do we do with the 3 that are left over?",
      "change them into 30 tenths", ["write 5.3", "leave them out"],
      "We can keep sharing. 3 ones cannot be shared by 5 as wholes, but each one is 10 tenths. So 3 ones are 30 tenths.")
t.say("3 ones are 30 tenths. Share 30 tenths by 5, and each share is 6 tenths.",
      WL("t1", "3 ones = 30 tenths"), W("d3", "30 ÷ 5 = 6"))
t.say("5 ones and 6 tenths. So 28 divided by 5 is 5.6.", ANS("a", "28 ÷ 5 = 5.6"), RING("a", "5.6"))
t.say("Check by multiplying back: 5.6 times 5 is 28.", W("c", "5.6 × 5 = 28"))
t.say("A neat shortcut: to divide by 5, double the number and then divide by 10. Double 28 is 56, and 56 divided by 10 is 5.6.",
      W("x1", "28 × 2 = 56"), W("x2", "56 ÷ 10 = 5.6"))
t.done(LESSONS)

# ── Q_CH11_005: 11.2 ÷ 4 ────────────────────────────────────────────────────
t = T("Q_CH11_005")
t.say("11.2 divided by 4. We divide just as with whole numbers, and keep the decimal point in its place.",
      GM("q", "11.2 ÷ 4 = ?"), WL("w", "11.2 = 11 ones and 2 tenths"))
t.ask("Start with the whole part. How many fours fit into 11?",
      "2", ["3", "1"],
      "Two fours are 8, and that fits into 11. Three fours would go past 11.")
t.say("2 fours are 8. That leaves 3 ones over.", W("d1", "4 × 2 = 8"), W("d2", "11 − 8 = 3"))
t.say("Those 3 ones are 30 tenths. And there are 2 tenths in the number already. Together that is 32 tenths.",
      WL("t1", "3 ones = 30 tenths"), W("d3", "30 + 2 = 32"))
t.ask("Share 32 tenths by 4. How many tenths in each share?",
      "8 tenths", ["7 tenths", "9 tenths"],
      "From the 4 times table: 4 times 8 is 32.")
t.say("2 ones and 8 tenths. So 11.2 divided by 4 is 2.8.",
      W("d4", "32 ÷ 4 = 8"), ANS("a", "11.2 ÷ 4 = 2.8"), RING("a", "2.8"))
t.say("Check by multiplying back: 2.8 times 4 is 11.2.", W("c", "2.8 × 4 = 11.2"))
t.say("When ones are left over, turn them into tenths and keep on sharing.")
t.done(LESSONS)
