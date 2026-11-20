"""Lessons written for single questions: Q_CH11_006-015."""
from g4_gr4_decimals_lib import (ANS, FIG, GIVEN, GM, NOTE, RING, STRIKE, T, UL, W, WL, figure_of)

LESSONS = {}

# ── Q_CH11_006: 1.264 ÷ 0.04 ────────────────────────────────────────────────
t = T("Q_CH11_006")
t.say("1.264 divided by 0.04. Dividing by a decimal is awkward, so we change the sum into one where we divide by a whole number.",
      GM("q", "1.264 ÷ 0.04 = ?"))
t.ask("What should we multiply 0.04 by, to turn it into a whole number?",
      "100", ["10", "4"],
      "0.04 has two digits after the point. Times 10 would still leave a decimal. Times 100 moves the digits two places, and gives 4.")
t.say("Whatever we do to one number we must do to the other, so the answer stays the same. 1.264 times 100 is 126.4, and 0.04 times 100 is 4.",
      W("a1", "1.264 × 100 = 126.4"), W("a2", "0.04 × 100 = 4"), W("d", "1.264 ÷ 0.04 = 126.4 ÷ 4"))
t.say("Now divide 126.4 by 4. Split it into two easy parts: 120 and 6.4. First, 120 divided by 4 is 30.",
      W("sp", "126.4 = 120 + 6.4"), W("p1", "120 ÷ 4 = 30"))
t.ask("And what is 6.4 divided by 4?",
      "1.6", ["16", "0.16"],
      "6.4 is a bit more than 4, so the answer is a bit more than 1. And 4 times 1.6 is 6.4.")
t.say("6.4 divided by 4 is 1.6. Add the two parts: 30 and 1.6 make 31.6.",
      W("p2", "6.4 ÷ 4 = 1.6"), W("p3", "30 + 1.6 = 31.6"))
t.say("So 1.264 divided by 0.04 is 31.6.", ANS("a", "1.264 ÷ 0.04 = 31.6"), RING("a", "31.6"))
t.say("Check by multiplying back: 31.6 times 0.04 is 1.264. The answer is much bigger than 1.264, because lots of tiny pieces of 0.04 fit into it.",
      W("c", "31.6 × 0.04 = 1.264"))
t.done(LESSONS)

# ── Q_CH11_007: 3.43 ÷ 0.07 ─────────────────────────────────────────────────
t = T("Q_CH11_007")
t.say("3.43 divided by 0.07. We would much rather divide by a whole number, so let's change the sum without changing its answer.",
      GM("q", "3.43 ÷ 0.07 = ?"))
t.ask("How many digits does 0.07 have after the point?",
      "2", ["1", "3"],
      "After the point there is a 0 and then a 7. That is two digits.")
t.say("Two digits, so we multiply by 100 to clear them. And we do it to both numbers. 3.43 becomes 343, and 0.07 becomes 7.",
      W("a1", "3.43 × 100 = 343"), W("a2", "0.07 × 100 = 7"), W("d", "3.43 ÷ 0.07 = 343 ÷ 7"))
t.say("Now 343 divided by 7. Take a big bite first: 7 times 40 is 280. That leaves 63.",
      W("p1", "7 × 40 = 280"), W("p2", "343 − 280 = 63"))
t.ask("How many sevens are there in 63?",
      "9", ["8", "7"],
      "From the 7 times table: 7 times 9 is 63.")
t.say("So 7 goes in 40 times, and then 9 more times. 40 and 9 make 49.", W("p3", "63 ÷ 7 = 9"), W("p4", "40 + 9 = 49"))
t.say("So 3.43 divided by 0.07 is 49.", ANS("a", "3.43 ÷ 0.07 = 49"), RING("a", "49"))
t.say("Check by multiplying back: 49 times 0.07 is 3.43. To divide by a decimal, multiply both numbers by 10 or 100 until you divide by a whole number.",
      W("c", "49 × 0.07 = 3.43"))
t.done(LESSONS)

# ── Q_CH11_008: 7.06 ÷ 10 ───────────────────────────────────────────────────
t = T("Q_CH11_008")
t.say("Here is 7.06 in a place-value chart. We divide it by 10.", GM("q", "7.06 ÷ 10 = ?"), FIG("f", figure_of("Q_CH11_008")))
t.ask("Dividing by 10 makes the number ten times smaller. Which way do the digits move?",
      "1 place to the right", ["1 place to the left", "2 places to the right"],
      "Smaller places are on the right. So to become ten times smaller, each digit moves one place to the right.")
t.say("The 7 ones become 7 tenths. The 0 tenths become 0 hundredths. The 6 hundredths become 6 thousandths.",
      FIG("f", figure_of("Q_CH11_008", 1)))
t.ask("What happens to the 0 in the middle of 7.06?",
      "it moves along too", ["it disappears", "it stays where it was"],
      "Every digit moves, and zero is a digit. It keeps the 7 and the 6 apart, in their proper places.")
t.say("And the ones place is empty now, so we write a 0 in front of the point.")
t.say("So 7.06 divided by 10 is 0.706.", ANS("a", "7.06 ÷ 10 = 0.706"), RING("a", "0.706"),
      FIG("f", figure_of("Q_CH11_008", 2)))
t.say("Check: 0.706 times 10 moves every digit back, and we get 7.06. Dividing by 10 moves every digit one place to the right, zeros included.",
      W("c", "0.706 × 10 = 7.06"))
t.done(LESSONS)

# ── Q_CH11_009: 652.7 ÷ 100 ─────────────────────────────────────────────────
t = T("Q_CH11_009")
t.say("652.7 divided by 100.", GM("q", "652.7 ÷ 100 = ?"), FIG("f", figure_of("Q_CH11_009")))
t.ask("Will the answer be bigger or smaller than 652.7?",
      "smaller", ["bigger"],
      "Dividing shares the number out into 100 equal parts. Each part is much smaller than the whole.")
t.say("100 has two zeros, so every digit moves two places to the right. Let's go one place at a time. First: 652.7 becomes 65.27.",
      W("s1", "652.7 ÷ 10 = 65.27"), FIG("f", figure_of("Q_CH11_009", 1)))
t.ask("One more place to the right. What does 65.27 become?",
      "6.527", ["0.6527", "652.7"],
      "Each digit moves one more place to the right. The 6 tens become 6 ones, so the number starts with 6 and then the point.")
t.say("65.27 becomes 6.527.", W("s2", "65.27 ÷ 10 = 6.527"), FIG("f", figure_of("Q_CH11_009", 2)))
t.say("So 652.7 divided by 100 is 6.527.", ANS("a", "652.7 ÷ 100 = 6.527"), RING("a", "6.527"))
t.say("Does it make sense? 652.7 has about six and a half hundreds in it, and 6.527 is about six and a half. Yes.")
t.say("The digits stay the same, in the same order. Count the zeros in 100, and move the digits that many places to the right.")
t.done(LESSONS)

# ── Q_CH11_010: 3.8 ÷ 100 ───────────────────────────────────────────────────
t = T("Q_CH11_010")
t.say("3.8 divided by 100.", GM("q", "3.8 ÷ 100 = ?"), FIG("f", figure_of("Q_CH11_010")))
t.ask("100 has two zeros. What happens to the digits?",
      "they move 2 places right", ["they move 2 places left", "they move 1 place right"],
      "Dividing makes a number smaller, so the digits move right, into smaller places. Two zeros means two places.")
t.say("One place first. The 3 ones become 3 tenths, and the 8 tenths become 8 hundredths. 3.8 becomes 0.38.",
      W("s1", "3.8 ÷ 10 = 0.38"), FIG("f", figure_of("Q_CH11_010", 1)))
t.ask("Now one more place. The 3 moves to the hundredths and the 8 to the thousandths. What goes in the empty tenths place?",
      "a zero", ["nothing at all", "the 3 stays there"],
      "An empty place must be held by a zero. Without it, the 3 would slide back into the tenths place.")
t.say("A zero holds the tenths place. So 0.38 becomes 0.038.",
      W("s2", "0.38 ÷ 10 = 0.038"), FIG("f", figure_of("Q_CH11_010", 2)))
t.say("So 3.8 divided by 100 is 0.038.", ANS("a", "3.8 ÷ 100 = 0.038"), RING("a", "0.038"))
t.say("Check: 0.038 times 100 is 3.8. When the digits move right and leave a gap after the point, fill the gap with a zero.",
      W("c", "0.038 × 100 = 3.8"))
t.done(LESSONS)

# ── Q_CH11_011: 3/4 as a decimal ────────────────────────────────────────────
t = T("Q_CH11_011")
t.say("We want to write 3 over 4 as a decimal. The bar shows it: 3 parts out of 4 are shaded.",
      GIVEN("q", "Convert 3/4 to a decimal"), FIG("f", figure_of("Q_CH11_011")))
t.say("Decimals are tenths and hundredths. So one good way is to change the bottom number into 100.", W("m", "4 × ? = 100"))
t.ask("4 times what makes 100?",
      "25", ["20", "40"],
      "Think of a rupee. 4 coins of 25 paise make 100 paise.")
t.say("So multiply the top and the bottom by 25. 3 times 25 is 75. So 3 over 4 is 75 over 100.",
      W("t1", "3 × 25 = 75"), W("f1", "3/4 = 75/100"), NOTE("f1", "3/4", "× 25 top and bottom", "below"))
t.ask("How do we write 75 hundredths as a decimal?",
      "0.75", ["7.5", "0.075"],
      "Hundredths take two digits after the point. So 75 hundredths is 0.75. It must be less than 1, because 3 out of 4 is less than a whole.")
t.say("So 3 over 4 is 0.75.", ANS("a", "3/4 = 0.75"), RING("a", "0.75"), FIG("f", figure_of("Q_CH11_011", 3)))
t.say("We can also divide 3 by 4. 30 tenths shared by 4 is 7 tenths, with 2 tenths left. Those are 20 hundredths, and 20 shared by 4 is 5. Again 0.75.",
      WL("d0", "3 = 30 tenths"), W("d1", "4 × 7 = 28"), W("d2", "20 ÷ 4 = 5"))
t.say("Three quarters is 0.75. Think of 75 paise, three quarters of a rupee. It is a fact worth keeping in your head.")
t.done(LESSONS)

# ── Q_CH11_012: 0.125 as a fraction in simplest form ────────────────────────
t = T("Q_CH11_012")
t.say("We want to write 0.125 as a fraction, as simple as it can be.",
      GIVEN("q", "Express 0.125 as a fraction in simplest form"))
t.ask("0.125 has three digits after the point. So what goes on the bottom of the fraction?",
      "1000", ["100", "10"],
      "One digit means tenths, two digits mean hundredths, and three digits mean thousandths. So the bottom is 1000.")
t.say("0.125 is 125 thousandths.", W("f1", "0.125 = 125/1000"))
t.ask("Now we simplify. Both numbers divide by 25. 125 divided by 25 is 5. What is 1000 divided by 25?",
      "40", ["4", "400"],
      "4 lots of 25 make 100. So 40 lots of 25 make 1000.",
      W("k", "125 ÷ 25 = 5"))
t.say("So 125 over 1000 becomes 5 over 40.", W("f2", "125/1000 = 5/40"), NOTE("f2", "125/1000", "÷ 25", "below"))
t.say("Are we done? Not yet. 5 and 40 both divide by 5. That gives 1 over 8.",
      W("f3", "5/40 = 1/8"), NOTE("f3", "5/40", "÷ 5", "below"))
t.say("1 and 8 share no factor, so this is the simplest form. 0.125 is one eighth.",
      ANS("a", "0.125 = 1/8"), RING("a", "1/8"), FIG("f", figure_of("Q_CH11_012", 2)))
t.say("Check: 8 lots of 0.125 make exactly 1. Write the decimal over 10, 100 or 1000, then keep dividing until nothing more goes into both.",
      W("c", "8 × 0.125 = 1"))
t.done(LESSONS)

# ── Q_CH11_013: greatest of 0.5, 0.05, 0.55, 0.505 ──────────────────────────
t = T("Q_CH11_013")
t.say("Which of these four decimals is the greatest? They are all made of 5s and zeros, so we must look closely.",
      GIVEN("q", "Greatest: 0.5, 0.05, 0.55, 0.505 ?"))
t.say("First give them all three digits after the point. Zeros at the end do not change a number.",
      FIG("f", figure_of("Q_CH11_013", 0)))
t.ask("Compare the tenths first. Which number has 0 tenths?",
      "0.05", ["0.5", "0.505"],
      "The tenths digit is the first digit after the point. In 0.05 that digit is 0.")
t.say("0.05 has no tenths at all, so it is the smallest. The other three all have 5 tenths, so that is a tie.",
      STRIKE("q", "0.05", "0 tenths"))
t.ask("To break the tie, look at the hundredths. We have 0.500, 0.550 and 0.505. Which has the biggest hundredths digit?",
      "0.550", ["0.505", "0.500"],
      "Look at the second digit after the point: 0, then 5, then 0. The 5 belongs to 0.550.")
t.say("0.550 wins, and 0.550 is 0.55. The trap is 0.505: it looks big because it has the most digits. But as thousandths it is 505 against 550.",
      WL("k", "thousandths: 500, 50, 550, 505"))
t.say("So the greatest is 0.55.", ANS("a", "0.55 > 0.505 > 0.5 > 0.05"), RING("a", "0.55"),
      FIG("f", figure_of("Q_CH11_013", 2)))
t.say("To compare decimals: same number of places first, then compare from the left, one place at a time.")
t.done(LESSONS)

# ── Q_CH11_014: 34.56 + 7.8 + 0.004 ─────────────────────────────────────────
t = T("Q_CH11_014")
t.say("Three decimals to add, and all three have different lengths. So first we line them up.",
      GM("q", "34.56 + 7.8 + 0.004 = ?"))
t.say("0.004 has three digits after the point, so give the others three as well. Zeros go at the end.",
      W("e1", "34.56 = 34.560"), W("e2", "7.8 = 7.800"))
t.say("Add the first two. Start from the right. Thousandths: 0 and 0. Hundredths: 6 and 0 make 6.",
      W("s0", "34.560 + 7.800 = ?"))
t.ask("Tenths: 5 and 8 make 13 tenths. What do we write?",
      "write 3, carry 1", ["write 13", "write 3 and nothing more"],
      "13 tenths is 1 whole and 3 tenths. The 3 stays in the tenths place, and the 1 is carried to the ones.",
      W("t1", "5 + 8 = 13"))
t.say("Ones: 4 and 7 and the carried 1 make 12. Write 2, carry 1. Tens: 3 and the carried 1 make 4. So far we have 42.36.",
      W("o", "4 + 7 + 1 = 12"), W("s1", "34.56 + 7.80 = 42.36"))
t.ask("Now add the 0.004. In which place does its 4 land?",
      "the thousandths place", ["the hundredths place", "the ten-thousandths place"],
      "In 0.004 the 4 is the third digit after the point. The third place is the thousandths.")
t.say("42.36 is 42.360. The 4 drops into the empty thousandths place. So the total is 42.364.",
      ANS("a", "42.360 + 0.004 = 42.364"), RING("a", "42.364"))
t.say("A rough check: about 35 and about 8 make 43, and our answer is a little under that. Line up the points, and every digit finds its own column.",
      W("c", "35 + 8 = 43"))
t.done(LESSONS)

# ── Q_CH11_015: 50 − 23.75 ──────────────────────────────────────────────────
t = T("Q_CH11_015")
t.say("50 take away 23.75. 50 is a whole number, so we can write it as 50.00 to match.",
      GM("q", "50 − 23.75 = ?"), W("e", "50 = 50.00"))
t.say("Let's take 23.75 away in two bites: first the 23 wholes, and then the 0.75.", W("sp", "23.75 = 23 + 0.75"))
t.ask("First bite. What is 50 take away 23?",
      "27", ["37", "33"],
      "Check by adding: 23 and 27 make 50. With 37 we would get far too much.")
t.say("50 take away 23 is 27.", W("b1", "50 − 23 = 27"))
t.ask("Second bite: take 0.75 from 27. Break one whole open. What is 1 take away 0.75?",
      "0.25", ["0.75", "0.35"],
      "0.75 is three quarters. Take three quarters from a whole, and one quarter is left. That is 0.25.")
t.say("So one of the 27 wholes turns into 0.25. That leaves 26 wholes and 0.25, which is 26.25.",
      W("b2", "1 − 0.75 = 0.25"), W("b2b", "27 − 1 = 26"), W("b3", "27 − 0.75 = 26.25"))
t.say("So 50 take away 23.75 is 26.25.", ANS("a", "50 − 23.75 = 26.25"), RING("a", "26.25"))
t.say("Check by adding back: 26.25 plus 23.75 makes 50. The answer had to be below 27, because we took away more than 23.",
      W("c", "26.25 + 23.75 = 50"))
t.done(LESSONS)
