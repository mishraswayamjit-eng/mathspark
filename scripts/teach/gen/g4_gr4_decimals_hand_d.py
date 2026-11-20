"""Lessons written for single questions: G4A_DECIMALS_027-040."""
from g4_gr4_decimals_lib import (ANS, FIG, GIVEN, GM, NOTE, RING, T, UL, W, WL, figure_of)

LESSONS = {}

# ── G4A_DECIMALS_027: 3 litres into 8 glasses ───────────────────────────────
t = T("G4A_DECIMALS_027")
t.say("3 litres of juice are poured equally into 8 glasses. How much juice is in each glass?",
      GIVEN("q", "3 litres poured equally into 8 glasses. Each = ?"), FIG("f", figure_of("G4A_DECIMALS_027")))
t.ask("Which sum do we need?",
      "3 ÷ 8", ["8 ÷ 3", "3 × 8"],
      "The juice is being shared, so the 3 litres are divided among the 8 glasses. The thing being shared comes first.")
t.say("Before we start: 8 glasses share only 3 litres, so each glass gets less than 1 litre. Our answer will begin with zero point something.",
      W("s", "3 ÷ 8 = ?"))
t.say("Here is a friendly way to divide by 8: halve, halve, and halve again. Half of 3 is 1.5.", W("h1", "3 ÷ 2 = 1.5"))
t.ask("Now halve again. What is half of 1.5?",
      "0.75", ["0.5", "0.25"],
      "Half of 1 is 0.5, and half of 0.5 is 0.25. Put them together: 0.5 and 0.25 make 0.75.")
t.say("Half of 1.5 is 0.75. One more halving to go. 0.75 is 750 thousandths, and half of 750 is 375. So half of 0.75 is 0.375.",
      W("h2", "1.5 ÷ 2 = 0.75"), W("k", "750 ÷ 2 = 375"), W("h3", "0.75 ÷ 2 = 0.375"))
t.say("So each glass has 0.375 litre of juice.", ANS("a", "3 ÷ 8 = 0.375"), RING("a", "0.375"))
t.say("Check: 8 glasses of 0.375 litre make exactly 3 litres. And 0.375 is less than 1, as we expected.",
      W("c", "8 × 0.375 = 3"))
t.done(LESSONS)

# ── G4A_DECIMALS_028: water level up 1.5, down 0.75 ─────────────────────────
t = T("G4A_DECIMALS_028")
t.say("The water in a tank is 36.8 centimetres deep. It rises by 1.5 centimetres, then falls by 0.75 centimetres. How deep is it now?",
      GIVEN("q", "36.8 cm deep. Up 1.5 cm, then down 0.75 cm. Now = ?"), FIG("f", figure_of("G4A_DECIMALS_028")))
t.ask("A rise and then a fall. What do we do with each one?",
      "add 1.5, subtract 0.75", ["add both", "subtract 1.5, add 0.75"],
      "A rise makes the water deeper, so we add it. A fall makes the water shallower, so we take it away.")
t.say("First the rise. 0.8 and 0.5 make 1.3, so a whole is carried over. 36.8 plus 1.5 is 38.3.",
      W("t1", "0.8 + 0.5 = 1.3"), W("s1", "36.8 + 1.5 = 38.3"), FIG("f", figure_of("G4A_DECIMALS_028", 0)))
t.say("Now the fall of 0.75. That has two digits after the point, so write 38.3 as 38.30 to match.",
      W("e", "38.3 = 38.30"))
t.ask("0.75 is nearly 1. Suppose we take away a whole 1 instead. How much too much have we taken?",
      "0.25", ["0.75", "0.5"],
      "1 is 0.25 more than 0.75. So we would have taken 0.25 too much, and we must give that back.")
t.say("38.30 take away 1 is 37.30. Now give back the extra 0.25. That makes 37.55.",
      W("v1", "38.30 − 1 = 37.30"), W("v2", "37.30 + 0.25 = 37.55"))
t.say("So the water is now 37.55 centimetres deep.",
      ANS("a", "38.30 − 0.75 = 37.55"), RING("a", "37.55"), FIG("f", figure_of("G4A_DECIMALS_028", 1)))
t.say("Check by adding back: 37.55 plus 0.75 is 38.30. Follow the story in order: add each rise, take away each fall.",
      W("c", "37.55 + 0.75 = 38.30"))
t.done(LESSONS)

# ── G4A_DECIMALS_029: digits 0, 3, 5, 8 in □.□□□ (Hard) ─────────────────────
t = T("G4A_DECIMALS_029")
t.say("We have the digits 0, 3, 5 and 8. Each is used once to fill the four boxes. We want the greatest number minus the smallest number.",
      GIVEN("q", "Digits 0, 3, 5, 8 in □.□□□, each used once"), GIVEN("q2", "Greatest − smallest = ?"))
t.ask("Start with the greatest number. Which digit should go in the first box, before the point?",
      "8", ["0", "5"],
      "The place furthest to the left is worth the most. So the biggest digit, 8, goes there.")
t.say("Then the next biggest digit in each place after it: 5, then 3, then 0. The greatest number is 8.530.",
      WL("g", "Greatest = 8.530"), FIG("f", figure_of("G4A_DECIMALS_029", 0)))
t.ask("Now the smallest number. Which digit goes in the first box this time?",
      "0", ["3", "8"],
      "For the smallest number, the smallest digit goes in the biggest place. That is 0. A decimal is allowed to begin with a zero before the point.")
t.say("That is the trap. Whole numbers never start with a zero, so many children start with the 3. But a decimal can. The smallest number is 0.358.",
      WL("m", "Smallest = 0.358"), FIG("f", figure_of("G4A_DECIMALS_029", 1)))
t.say("Now subtract. Thousandths: 0 take away 8 needs a borrow, and 10 take away 8 is 2. Hundredths: only 2 are left, so borrow again, and 12 take away 5 is 7.",
      W("s", "8.530 − 0.358 = ?"), W("b1", "10 − 8 = 2"), W("b2", "12 − 5 = 7"))
t.say("Tenths: 4 are left, and 4 take away 3 is 1. Ones: 8 take away 0 is 8. So the difference is 8.172.",
      W("b3", "4 − 3 = 1"), ANS("a", "8.530 − 0.358 = 8.172"), RING("a", "8.172"))
t.say("Check by adding back: 8.172 plus 0.358 is 8.530. Biggest digits in the biggest places for the greatest. Smallest digits there for the smallest, and zero may lead.",
      W("c", "8.172 + 0.358 = 8.530"))
t.done(LESSONS)

# ── G4A_DECIMALS_031: plant grows 0.25 cm a day (Hard) ──────────────────────
t = T("G4A_DECIMALS_031")
t.say("A plant is 1.5 centimetres tall. It grows 0.25 centimetres every day. After how many days will it be exactly 4 centimetres tall?",
      GIVEN("q", "Plant 1.5 cm tall. Grows 0.25 cm a day."), GIVEN("q2", "4 cm tall after ? days"),
      FIG("f", figure_of("G4A_DECIMALS_031")))
t.ask("How much does the plant still have to grow?",
      "2.5 cm", ["4 cm", "5.5 cm"],
      "The plant does not start from zero. It is already 1.5 centimetres tall. So it only has to grow the gap from 1.5 up to 4.")
t.say("That is the key to this question. It needs 4 take away 1.5, which is 2.5 centimetres more. Not the whole 4.",
      W("g", "4 − 1.5 = 2.5"), UL("g", "2.5"))
t.say("Now, 0.25 is one quarter. And 4 quarters make 1 whole. So the plant grows 1 centimetre in 4 days.",
      W("d1", "4 × 0.25 = 1"))
t.ask("If 1 centimetre takes 4 days, how long do 2 centimetres take?",
      "8 days", ["4 days", "2 days"],
      "Each centimetre takes 4 days. So 2 centimetres take 4 days and then 4 days more.")
t.say("2 centimetres take 8 days. But it needs 2.5, so there is half a centimetre still to go. Half is two quarters, so that takes 2 more days.",
      W("d2", "8 × 0.25 = 2"), W("d3", "2 × 0.25 = 0.5"))
t.say("8 days and 2 more days make 10 days.", W("d4", "8 + 2 = 10"),
      ANS("a", "After 10 days", label=True), RING("a", "10"))
t.say("Check: 10 days of 0.25 is 2.5 centimetres, and 1.5 plus 2.5 is exactly 4. When something has a head start, find the gap first.",
      W("c", "1.5 + 10 × 0.25 = 4"))
t.done(LESSONS)

# ── G4A_DECIMALS_032: bananas by the dozen, guavas each (Hard) ──────────────
t = T("G4A_DECIMALS_032")
t.say("A dozen bananas cost 54 rupees. Guavas cost 7.50 rupees each. Imran buys 8 bananas and 5 guavas. How much does he pay?",
      GIVEN("q", "A dozen bananas: Rs. 54. Guavas: Rs. 7.50 each."), GIVEN("q2", "8 bananas + 5 guavas = ?"))
t.ask("How many bananas are there in a dozen?",
      "12", ["10", "6"],
      "A dozen always means 12, like a dozen eggs.")
t.say("Here is the trap. The price is for 12 bananas, but Imran buys only 8. So first we need the price of just one banana.",
      WL("z", "A dozen = 12"), UL("q2", "8 bananas"))
t.say("One banana costs 54 divided by 12. 12 times 4 is 48, and 6 rupees are left. 6 is half of 12, so each banana costs 4 and a half rupees: 4.50.",
      W("b0", "12 × 4 = 48"), W("b1", "54 − 48 = 6"), W("b2", "54 ÷ 12 = 4.50"))
t.ask("So what do 8 bananas cost?",
      "Rs. 36", ["Rs. 32", "Rs. 54"],
      "8 lots of 4 rupees is 32 rupees. And 8 lots of half a rupee is 4 rupees more.")
t.say("8 bananas cost 36 rupees.", W("b3", "8 × 4.50 = 36"))
t.say("Now the guavas. 5 lots of 7 rupees is 35 rupees. 5 lots of half a rupee is 2.50. So 5 guavas cost 37.50.",
      W("g1", "5 × 7 = 35"), W("g2", "5 × 0.50 = 2.50"), W("g3", "5 × 7.50 = 37.50"))
t.say("Add the two amounts. 36 and 37.50 make 73.50. Imran pays 73.50 rupees.",
      ANS("a", "36.00 + 37.50 = 73.50"), RING("a", "73.50"))
t.say("A price for a dozen is not the price for 8. Find the price of one first, then multiply by how many were bought.")
t.done(LESSONS)

# ── G4A_DECIMALS_033: multiplied by 10 instead of dividing ──────────────────
t = T("G4A_DECIMALS_033")
t.say("Rahul had to divide a number by 10. By mistake he multiplied it by 10, and got 62.5. What should he have got?",
      GIVEN("q", "Should divide by 10. Multiplied by 10: got 62.5."), GIVEN("q2", "Right answer = ?"),
      FIG("f", figure_of("G4A_DECIMALS_033")))
t.say("There are two jobs. First find the number Rahul started with. Then do to it what he was supposed to do.")
t.ask("He multiplied his number by 10 and got 62.5. How do we get back to his number?",
      "62.5 ÷ 10", ["62.5 × 10", "62.5 − 10"],
      "He multiplied by 10. To go back we undo that, and dividing undoes multiplying.")
t.say("Dividing by 10 moves every digit one place to the right. 62.5 becomes 6.25. That is the number Rahul started with.",
      W("s1", "62.5 ÷ 10 = 6.25"), FIG("f", figure_of("G4A_DECIMALS_033", 0)))
t.ask("We have found 6.25. Are we finished?",
      "No: now divide it by 10", ["Yes: 6.25 is the answer", "No: now multiply it by 10"],
      "6.25 is only the number Rahul started with. He was asked to divide it by 10, and nobody has done that yet.")
t.say("So divide 6.25 by 10. Every digit moves one more place to the right, and we get 0.625.",
      W("s2", "6.25 ÷ 10 = 0.625"), FIG("f", figure_of("G4A_DECIMALS_033", 1)))
t.say("Rahul's answer should have been 0.625.", ANS("a", "Right answer = 0.625", label=True), RING("a", "0.625"))
t.say("We divided by 10 twice: once to undo, once to do the sum. That is the same as dividing 62.5 by 100. Undo first, then do it right.",
      W("c", "62.5 ÷ 100 = 0.625"))
t.done(LESSONS)

# ── G4A_DECIMALS_034: order 0.4, 3/8, 0.38, 7/20 (Hard) ─────────────────────
t = T("G4A_DECIMALS_034")
t.say("We must put four numbers in order, smallest first. Two are decimals and two are fractions, so let's turn them all into decimals.",
      GIVEN("q", "Smallest to greatest: 0.4, 3/8, 0.38, 7/20"))
t.ask("Start with 7 over 20. Change it into hundredths. What is it as a decimal?",
      "0.35", ["0.7", "3.5"],
      "20 times 5 is 100, so multiply the top by 5 as well. That gives 0.35, which is less than 1, as it should be.",
      W("f0", "7/20 = ?/100"))
t.say("7 times 5 is 35, and 20 times 5 is 100. So 7 over 20 is 35 hundredths, 0.35.", W("f1", "7/20 = 35/100 = 0.35"))
t.say("Now 3 over 8. One eighth is 0.125. So 3 eighths is 3 lots of 0.125, which is 0.375.",
      W("g0", "1/8 = 0.125"), W("g1", "3/8 = 3 × 0.125 = 0.375"))
t.say("Now write all four with three digits after the point, so they are easy to compare.",
      FIG("f", figure_of("G4A_DECIMALS_034", 2)), WL("k", "thousandths: 400, 375, 380, 350"))
t.ask("Here is the tricky pair. Which is bigger: 3 over 8, which is 0.375, or 0.38?",
      "0.38", ["3/8", "they are equal"],
      "0.38 is the same as 0.380. Now compare 375 thousandths with 380 thousandths. 380 is more.")
t.say("0.375 has more digits, but 0.380 is bigger. So in order we have 350, then 375, then 380, then 400.",
      FIG("f", figure_of("G4A_DECIMALS_034", 3)))
t.say("Back in their own clothes: 7 over 20, then 3 over 8, then 0.38, then 0.4.",
      ANS("a", "7/20 < 3/8 < 0.38 < 0.4"), RING("a", "7/20 < 3/8 < 0.38 < 0.4"))
t.say("Turn everything into decimals with the same number of places, then compare. And check which end the question wants first: here, the smallest.")
t.done(LESSONS)

# ── G4A_DECIMALS_035: three numbers add up to 10 (Hard) ─────────────────────
t = T("G4A_DECIMALS_035")
t.say("Three numbers add up to 10. Two of them are 3.45 and 2.8. How much greater is the third number than the smallest of the three?",
      GM("q", "3.45 + 2.8 + ? = 10"), GIVEN("q2", "Third number − smallest number = ?"),
      FIG("f", figure_of("G4A_DECIMALS_035")))
t.ask("What must we find first?",
      "the third number", ["3.45 − 2.8", "the biggest number"],
      "We cannot compare the third number with anything until we know what it is. So we find it first.")
t.say("Add the two numbers we know. Write 2.8 as 2.80. Then 0.45 and 0.80 make 1.25, and with 3 and 2 that is 6.25.",
      W("k", "0.45 + 0.80 = 1.25"), W("s1", "3.45 + 2.80 = 6.25"))
t.say("The third number is what is left of the 10. From 6.25 up to 7 is 0.75, and from 7 up to 10 is 3. So the third number is 3.75.",
      W("u", "6.25 + 0.75 = 7"), W("s2", "10 − 6.25 = 3.75"))
t.ask("Now we have all three: 3.45, 2.8 and 3.75. Which is the smallest?",
      "2.8", ["3.45", "3.75"],
      "2.8 has only 2 wholes. The other two have 3 wholes. So 2.8 is the smallest, even though it has the fewest digits.")
t.say("So we want 3.75 take away 2.80. From 2.80 up to 3 is 0.20, and from 3 up to 3.75 is 0.75. Together that is 0.95.",
      W("v1", "2.80 + 0.20 = 3"), W("v2", "0.20 + 0.75 = 0.95"), ANS("a", "3.75 − 2.80 = 0.95"))
t.say("The third number is 0.95 greater than the smallest.", RING("a", "0.95"))
t.say("Check: 3.45 plus 2.8 plus 3.75 is 10. And notice that 3.75 was not the final answer. Always read what the question asks for at the very end.",
      W("c", "3.45 + 2.8 + 3.75 = 10"))
t.done(LESSONS)

# ── G4A_DECIMALS_036: bottle of oil, half used (Hard) ───────────────────────
t = T("G4A_DECIMALS_036")
t.say("A full bottle of oil weighs 2.35 kilograms. When half the oil has been used, it weighs 1.3 kilograms. What does the empty bottle weigh?",
      GIVEN("q", "Full bottle: 2.35 kg. Half the oil used: 1.3 kg."), GIVEN("q2", "Empty bottle = ?"),
      FIG("f", figure_of("G4A_DECIMALS_036")))
t.say("Look at the two bars. The bottle is the same both times. The only thing that changed is that half of the oil has gone.")
t.ask("So the drop in weight is the weight of what?",
      "half the oil", ["the bottle", "all the oil"],
      "Between the two weighings, only oil was used, and exactly half of it. So the weight that went missing is half the oil.")
t.say("Find the drop. 2.35 take away 1.30 is 1.05. So half the oil weighs 1.05 kilograms.",
      W("h", "2.35 − 1.30 = 1.05"), NOTE("h", "1.05", "half the oil", "below"))
t.ask("Then how much does all the oil weigh?",
      "2.1 kg", ["1.05 kg", "0.525 kg"],
      "Half the oil is 1.05. All the oil is two halves, so we double it.")
t.say("Double 1.05 is 2.1. All the oil weighs 2.1 kilograms.", W("o", "2 × 1.05 = 2.1"))
t.say("The full bottle is the bottle plus all the oil. So take the oil away: 2.35 take away 2.10 leaves 0.25. The empty bottle weighs 0.25 kilograms.",
      ANS("a", "2.35 − 2.10 = 0.25"), RING("a", "0.25"), FIG("f", figure_of("G4A_DECIMALS_036", 3)))
t.say("Check: the bottle, 0.25, plus half the oil, 1.05, makes 1.30. The trap is to halve the whole 2.35. Only the oil is halved; the bottle stays the same.",
      W("c", "0.25 + 1.05 = 1.30"))
t.done(LESSONS)

# ── G4A_DECIMALS_037: how much less than 1 is 0.9 + 0.09 + 0.009 ────────────
t = T("G4A_DECIMALS_037")
t.say("How much less than 1 is this sum? Two jobs: first add the three numbers, then see how far the total is from 1.",
      GIVEN("q", "How much less than 1 is 0.9 + 0.09 + 0.009 ?"))
t.say("Write all three with three digits after the point, so the places line up.",
      W("e1", "0.9 = 0.900"), W("e2", "0.09 = 0.090"))
t.ask("Each 9 sits in its own place: one in the tenths, one in the hundredths, one in the thousandths. So what is the sum?",
      "0.999", ["0.27", "0.0999"],
      "Each 9 is in a different place, so nothing needs carrying. 9 tenths, 9 hundredths and 9 thousandths make 0.999.")
t.say("The sum is 0.999.", W("s", "0.900 + 0.090 + 0.009 = 0.999"))
t.ask("Now compare with 1. Write 1 as 1.000: that is 1000 thousandths. And 0.999 is 999 thousandths. How big is the gap?",
      "1 thousandth", ["1 hundredth", "1 tenth"],
      "999 is just 1 less than 1000. And we are counting in thousandths. So the gap is 1 thousandth.",
      WL("k", "1000 thousandths and 999 thousandths"))
t.say("1 thousandth is written 0.001. So the sum is 0.001 less than 1.",
      ANS("a", "1.000 − 0.999 = 0.001"), RING("a", "0.001"))
t.say("Check: 0.999 plus 0.001 makes exactly 1.", W("c", "0.999 + 0.001 = 1"))
t.say("Watch out: 0.999 is the sum, not the answer. The question asked how far the sum is from 1.")
t.done(LESSONS)

# ── G4A_DECIMALS_038: Mira thinks of a number (Hard) ────────────────────────
t = T("G4A_DECIMALS_038")
t.say("Mira thinks of a number. She multiplies it by 100, then subtracts 4.5, then divides by 10, and ends on 2.05. What was her number?",
      GIVEN("q", "? × 100, then − 4.5, then ÷ 10, gives 2.05"))
t.say("We know the end and we want the start. So we walk backwards, undoing one step at a time, beginning with the last thing she did.")
t.ask("The last thing Mira did was divide by 10. How do we undo that?",
      "multiply 2.05 by 10", ["divide 2.05 by 10", "add 10 to 2.05"],
      "Times and divide are partners. To undo a divide by 10, we multiply by 10.")
t.say("2.05 times 10 is 20.5. That is what she had just before dividing.", W("s1", "2.05 × 10 = 20.5"))
t.ask("Before that, she subtracted 4.5. How do we undo a subtraction?",
      "add 4.5", ["subtract 4.5 again", "multiply by 4.5"],
      "To undo taking away, we give it back. So we add 4.5.")
t.say("20.5 plus 4.5 is 25. That is what she had just before subtracting.", W("s2", "20.5 + 4.5 = 25"))
t.say("The first thing she did was multiply by 100. To undo it, divide by 100. Careful: by 100, not by 10. 25 divided by 100 is 0.25.",
      W("s3", "25 ÷ 100 = 0.25"), ANS("a", "Mira's number = 0.25", label=True), RING("a", "0.25"))
t.say("Check by going forwards. 0.25 times 100 is 25. Take away 4.5 and we get 20.5. Divide by 10 and we get 2.05. It works.",
      W("c1", "0.25 × 100 = 25"), W("c2", "25 − 4.5 = 20.5"), W("c3", "20.5 ÷ 10 = 2.05"))
t.say("To work backwards: start from the end, go in the opposite order, and use the opposite operation each time.")
t.done(LESSONS)

# ── G4A_DECIMALS_039: saving 50 paise more each day (Hard) ──────────────────
t = T("G4A_DECIMALS_039")
t.say("Asha saves 2.50 rupees on Monday. Each day after that she saves 50 paise more than the day before. How much has she saved after 6 days?",
      GIVEN("q", "Day 1: Rs. 2.50. Each day 50 paise more. 6 days."), GIVEN("q2", "Total saved = ?"))
t.ask("Does Asha save the same amount every day?",
      "No, it grows each day", ["Yes, Rs. 2.50 every day"],
      "Read it again: each day she saves 50 paise more than the day before. So the amount keeps growing.")
t.say("So we cannot just multiply. Let's list all six days. 50 paise is 0.50 of a rupee, so each amount is 0.50 more than the last.",
      WL("h", "50 paise = Rs. 0.50"), FIG("f", figure_of("G4A_DECIMALS_039", 0)))
t.ask("Here is a clever way to add them: pair the first with the last. What is 2.50 plus 5.00?",
      "7.50", ["7.00", "8.00"],
      "2 and 5 make 7, and the half rupee comes along too. So it is 7.50.")
t.say("Now pair the second with the fifth: 3.00 and 4.50 make 7.50 too. And the third with the fourth: 3.50 and 4.00, also 7.50. Every pair is the same!",
      W("p1", "2.50 + 5.00 = 7.50"), W("p2", "3.00 + 4.50 = 7.50"), W("p3", "3.50 + 4.00 = 7.50"))
t.say("So we have 3 pairs of 7.50. 3 lots of 7 is 21, and 3 lots of half a rupee is 1.50. Together that is 22.50.",
      W("m0", "3 × 7 = 21"), W("m1", "3 × 0.50 = 1.50"), W("m", "3 × 7.50 = 22.50"))
t.say("So Asha has saved 22.50 rupees.", ANS("a", "Total saved = Rs. 22.50", label=True), RING("a", "Rs. 22.50"))
t.say("Do not just do 6 lots of 2.50. When an amount changes every day, list the days first, and then add.")
t.done(LESSONS)

# ── G4A_DECIMALS_040: pieces of 0.125 m from 2 1/2 m ────────────────────────
t = T("G4A_DECIMALS_040")
t.say("How many pieces, each 0.125 metres long, can be cut from a wire two and a half metres long?",
      GIVEN("q", "Pieces of 0.125 m from a wire 2 1/2 m long = ?"))
t.say("0.125 is a decimal worth knowing by heart. Here is a clue: one quarter is 0.25.", W("k0", "1/4 = 0.25"))
t.ask("0.125 is half of 0.25. So which fraction is 0.125?",
      "1/8", ["1/4", "1/5"],
      "Half of a quarter is an eighth. Cut each of the 4 quarters in two, and you get 8 equal parts.")
t.say("0.125 is one eighth of a metre. So 8 pieces fit into 1 metre.",
      W("e", "8 × 0.125 = 1"), FIG("f", figure_of("G4A_DECIMALS_040", 0)))
t.ask("How many pieces come from 2 whole metres?",
      "16", ["8", "10"],
      "8 pieces come from each metre. Two metres give 8 and 8 more.")
t.say("2 metres give 16 pieces.", W("m", "2 × 8 = 16"))
t.say("Do not forget the extra half metre. A whole metre gives 8 pieces, so half a metre gives half of 8, which is 4 more.",
      W("h", "8 ÷ 2 = 4"), FIG("f", figure_of("G4A_DECIMALS_040", 2)))
t.say("16 and 4 make 20. So 20 pieces can be cut.", W("s", "16 + 4 = 20"),
      ANS("a", "20 pieces", label=True), RING("a", "20"))
t.say("Check: 20 pieces of 0.125 make 2.5, which is two and a half metres. Knowing that 0.125 is one eighth made this easy.",
      W("c", "20 × 0.125 = 2.5"))
t.done(LESSONS)
