"""Lessons written for single questions: G4A_DECIMALS_011-025."""
from g4_gr4_decimals_lib import (ANS, FIG, GIVEN, GM, NOTE, RING, T, UL, W, WL, figure_of)

LESSONS = {}

# ── G4A_DECIMALS_011: long jump, who came second ────────────────────────────
t = T("G4A_DECIMALS_011")
t.say("Four boys did the long jump. In a long jump, the longest jump wins. We want to know who came second.",
      GIVEN("q", "Long jump: who came second?"), FIG("f", figure_of("G4A_DECIMALS_011")))
t.say("The jumps have different numbers of digits, and that can fool us. More digits does not mean a longer jump. So let's give every jump three digits after the point.",
      FIG("f", figure_of("G4A_DECIMALS_011", 0)))
t.ask("Every jump has 3 wholes. So compare the parts after the point: 380, 045, 400 and 405. Which is the biggest?",
      "405", ["380", "400"],
      "405 is more than 400, and 400 is more than 380. So 405 is the biggest.",
      WL("k", "after the point: 380, 045, 400, 405"))
t.say("405 belongs to 3.405, and that is Dinesh. So Dinesh came first. But the question asks who came second, so we are not done.",
      UL("k", "405"))
t.ask("Who has the next longest jump?",
      "Chirag, 3.4", ["Anil, 3.38", "Bharat, 3.045"],
      "After 405 comes 400. That is 3.400, which is the same as 3.4, Chirag's jump. Anil's 3.38 is 3.380, a little less.")
t.say("3.4 looks short, but it is 3.400. That beats 3.380. And 3.045 has no tenths at all, so it is the shortest jump.",
      W("o", "3.405 > 3.4 > 3.38 > 3.045"), FIG("f", figure_of("G4A_DECIMALS_011", 2)))
t.say("So Chirag came second.", ANS("a", "Chirag came second (3.4 m)", label=True), RING("a", "Chirag"))
t.say("To compare decimals, give them all the same number of places first. And read the question to the end: it wanted second, not first.")
t.done(LESSONS)

# ── G4A_DECIMALS_012: the two 2s in 5.252 ───────────────────────────────────
t = T("G4A_DECIMALS_012")
t.say("The number 5.252 has two 2s in it. They look the same, but they are not worth the same. How many times as large is the first 2 as the second 2?",
      GIVEN("q", "5.252: first 2 is how many times the second 2?"), FIG("f", figure_of("G4A_DECIMALS_012")))
t.ask("The first 2 comes straight after the point. Which place is that?",
      "tenths", ["hundredths", "ones"],
      "The first place after the decimal point is always the tenths place.")
t.say("So the first 2 is worth 2 tenths. That is 0.2.", W("v1", "2/10 = 0.2"))
t.ask("The second 2 is the third digit after the point. Which place is that?",
      "thousandths", ["hundredths", "tenths"],
      "After the point the places go tenths, hundredths, thousandths. The third place is the thousandths.")
t.say("So the second 2 is worth 2 thousandths. That is 0.002.", W("v2", "2/1000 = 0.002"))
t.say("Each place is 10 times as large as the place on its right. From thousandths to hundredths is times 10. From hundredths to tenths is times 10 again.",
      W("j", "0.002 × 10 × 10 = 0.2"))
t.say("Two steps, and 10 times 10 is 100. So the first 2 is 100 times as large as the second 2.",
      ANS("a", "0.2 = 100 × 0.002"), RING("a", "100"))
t.say("Here is the trap: the two 2s are not neighbours. The 5 sits between them. One step apart is 10 times, but two steps apart is 100 times.")
t.done(LESSONS)

# ── G4A_DECIMALS_013: 2.5 kg + 0.375 kg + 14 kg ─────────────────────────────
t = T("G4A_DECIMALS_013")
t.say("Three parcels: 2.5 kilograms, 0.375 kilograms and 14 kilograms. We want the total weight.",
      GIVEN("q", "2.5 kg + 0.375 kg + 14 kg = ?"), FIG("f", figure_of("G4A_DECIMALS_013")))
t.ask("To add them we must line up the decimal points. But where is the decimal point in 14?",
      "at the end: 14.000", ["at the front: 0.14", "in the middle: 1.4"],
      "14 is a whole number. A whole number's point sits at the very end, after its last digit.")
t.say("So let's give every weight three digits after the point. 2.5 becomes 2.500, and 14 becomes 14.000. The zeros always go at the end.",
      W("e1", "2.5 = 2.500"), W("e2", "14 = 14.000"))
t.say("Add the first two. After the point, 500 and 375 make 875. And there are 2 wholes. So that is 2.875.",
      W("k", "500 + 375 = 875"), W("s1", "2.500 + 0.375 = 2.875"))
t.ask("Now we add the 14 wholes to 2.875. Which part of 2.875 will change?",
      "only the whole part", ["only the part after the point", "every digit"],
      "14 has nothing after its point. So the part after the point stays as it is, and only the wholes grow.")
t.say("2 wholes and 14 wholes make 16 wholes. So the total is 16.875.",
      W("w", "2 + 14 = 16"), ANS("a", "2.875 + 14.000 = 16.875"), RING("a", "16.875"))
t.say("The total weight is 16.875 kilograms. A quick check: the 14 alone is most of the answer, so any total less than 14 could not be right.")
t.say("When you add decimals of different lengths, line up the points and fill the gaps with zeros at the end.")
t.done(LESSONS)

# ── G4A_DECIMALS_014: by how much is 10 greater than 3.607 ──────────────────
t = T("G4A_DECIMALS_014")
t.say("By how much is 10 greater than 3.607? We want the gap between them.",
      GIVEN("q", "By how much is 10 greater than 3.607?"), FIG("f", figure_of("G4A_DECIMALS_014")))
t.ask("Which sum gives the gap?",
      "10 − 3.607", ["10 + 3.607", "3.607 − 10"],
      "By how much greater means the difference. We take the smaller number away from the bigger one.")
t.say("10 is a whole number. To match 3.607 we can write it with three zeros after the point.",
      W("e", "10 = 10.000"))
t.ask("Before we work it out: will the answer be more than 7, or less than 7?",
      "less than 7", ["more than 7"],
      "10 take away 3 is 7. But we take away a bit more than 3, so the answer is a bit less than 7.")
t.say("Let's count up from 3.607. How much does 0.607 need to reach 1? From the right: 7 needs 3 to make 10. Then the other digits need to reach 9: 0 needs 9, and 6 needs 3. That is 0.393.",
      W("u0", "0.607 + 0.393 = 1"), W("u1", "3.607 + 0.393 = 4"))
t.say("So from 3.607 up to 4 is 0.393. Then from 4 up to 10 is 6 more. Together that is 6.393.",
      W("u2", "4 + 6 = 10"), ANS("a", "10.000 − 3.607 = 6.393"), RING("a", "6.393"))
t.say("Check by adding back: 6.393 plus 3.607 makes exactly 10. And it is a bit less than 7, just as we expected.",
      W("c", "6.393 + 3.607 = 10"))
t.say("To subtract from a whole number, write it with zeros after the point, or count up from the smaller number.")
t.done(LESSONS)

# ── G4A_DECIMALS_015: 25 balls of 0.16 kg ───────────────────────────────────
t = T("G4A_DECIMALS_015")
t.say("One cricket ball weighs 0.16 kilograms. We want the weight of 25 balls.",
      GIVEN("q", "1 ball = 0.16 kg. 25 balls = ?"))
t.ask("Which sum do we need?",
      "0.16 × 25", ["0.16 + 25", "25 ÷ 0.16"],
      "25 balls, each the same weight, means 25 lots of 0.16. Lots of means times.")
t.say("Forget the point for a moment and do 16 times 25. A handy fact: 4 times 25 is 100. And 16 is 4 fours, so 16 times 25 is 4 hundreds. That is 400.",
      W("m1", "4 × 25 = 100"), W("m2", "16 × 25 = 4 × 100 = 400"))
t.ask("Now put the point back. 0.16 has two digits after the point. So where does the point go in 400?",
      "4.00", ["40.0", "0.400"],
      "Two decimal places in the question means two decimal places in the answer. Count two digits from the right of 400 and put the point there.")
t.say("That gives 4.00, and 4.00 is just 4.", W("p", "0.16 × 25 = 4.00"))
t.say("So 25 balls weigh 4 kilograms.", ANS("a", "25 balls weigh 4 kg", label=True), RING("a", "4 kg"))
t.say("Does 4 make sense? 0.16 is a little less than 0.2, and 25 lots of 0.2 would be 5. So a little less than 5 is just right.",
      W("c", "25 × 0.2 = 5"))
t.say("To multiply a decimal: multiply as whole numbers, then give the answer as many decimal places as the question had.")
t.done(LESSONS)

# ── G4A_DECIMALS_016: 0.045 × 1000 ÷ 10 ─────────────────────────────────────
t = T("G4A_DECIMALS_016")
t.say("Here we multiply by 1000 and then divide by 10. We work from left to right, one step at a time.",
      GM("q", "0.045 × 1000 ÷ 10 = ?"), FIG("f", figure_of("G4A_DECIMALS_016")))
t.ask("1000 has three zeros. So what does multiplying by 1000 do to each digit?",
      "moves it 3 places left", ["moves it 3 places right", "moves it 1 place left"],
      "Multiplying makes a number bigger, so the digits move left, to bigger places. Three zeros means three places.")
t.say("So the 4 moves from the hundredths up to the tens, and the 5 moves from the thousandths up to the ones. 0.045 times 1000 is 45.",
      W("s1", "0.045 × 1000 = 45"), FIG("f", figure_of("G4A_DECIMALS_016", 0)))
t.ask("We are not done: now divide 45 by 10. Which way do the digits move this time?",
      "1 place to the right", ["1 place to the left", "3 places to the right"],
      "Dividing makes a number smaller, so the digits move right, to smaller places. 10 has one zero, so they move one place.")
t.say("The 4 moves down to the ones, and the 5 moves down to the tenths. 45 divided by 10 is 4.5.",
      W("s2", "45 ÷ 10 = 4.5"), FIG("f", figure_of("G4A_DECIMALS_016", 1)))
t.say("So the answer is 4.5.", ANS("a", "0.045 × 1000 ÷ 10 = 4.5"), RING("a", "4.5"))
t.say("The trap is to stop at 45. There are two signs, so there are two steps. A shortcut: times 1000 then divided by 10 is the same as times 100.",
      W("c", "0.045 × 100 = 4.5"))
t.done(LESSONS)

# ── G4A_DECIMALS_017: □ × 100 = 3.7 ─────────────────────────────────────────
t = T("G4A_DECIMALS_017")
t.say("Some number was multiplied by 100, and it became 3.7. We want the number in the box, the number before it was multiplied.",
      GIVEN("q", "□ × 100 = 3.7"), FIG("f", figure_of("G4A_DECIMALS_017")))
t.ask("How do we undo multiplying by 100?",
      "divide by 100", ["multiply by 100 again", "subtract 100"],
      "Times and divide are partners. Whatever times does, divide undoes.")
t.say("So the box is 3.7 divided by 100. And notice: the box must be smaller than 3.7, because multiplying by 100 made it grow into 3.7.",
      W("b", "3.7 ÷ 100 = ?"))
t.say("Dividing by 100 moves every digit two places to the right. Let's do one place at a time. One place: 3.7 becomes 0.37.",
      W("d1", "3.7 ÷ 10 = 0.37"))
t.ask("Now one more place to the right. What does 0.37 become?",
      "0.037", ["0.0037", "0.307"],
      "The 3 moves from the tenths to the hundredths, and the 7 from the hundredths to the thousandths. The empty tenths place gets a zero.")
t.say("The empty place is filled with a zero. So the number in the box is 0.037.",
      W("d2", "0.37 ÷ 10 = 0.037"), ANS("a", "3.7 ÷ 100 = 0.037"), RING("a", "0.037"),
      FIG("f", figure_of("G4A_DECIMALS_017", 1)))
t.say("Check: 0.037 times 100 moves the digits two places back to the left, and we get 3.7. To find a missing number, undo what was done to it.",
      W("c", "0.037 × 100 = 3.7"))
t.done(LESSONS)

# ── G4A_DECIMALS_018: greatest of 0.58, 3/5, 5/8, 0.65 ──────────────────────
t = T("G4A_DECIMALS_018")
t.say("Which of these four is the greatest? Two are decimals and two are fractions. That is hard to compare, so let's turn them all into decimals.",
      GIVEN("q", "Greatest: 0.58, 3/5, 5/8, 0.65 ?"))
t.ask("Start with 3 over 5. If we double the top and the bottom, we get tenths. What is 3 over 5 as a decimal?",
      "0.6", ["0.35", "0.3"],
      "Double the top and the bottom: 3 over 5 becomes 6 over 10. And 6 tenths is written 0.6.",
      W("f0", "3/5 = ?/10"))
t.say("3 over 5 is 6 over 10, and that is 0.6.", W("f1", "3/5 = 6/10 = 0.6"))
t.say("Now 5 over 8. One eighth is half of a quarter, and that is 0.125. So 5 eighths is 5 lots of 0.125, which is 0.625.",
      W("g0", "1/8 = 0.125"), W("g1", "5/8 = 5 × 0.125 = 0.625"))
t.say("Now write all four with three digits after the point: 0.580, 0.600, 0.625 and 0.650.",
      FIG("f", figure_of("G4A_DECIMALS_018", 2)))
t.ask("Which one is the greatest?",
      "0.650", ["0.625", "0.580"],
      "Compare the tenths first. 0.580 has 5 tenths and the rest have 6. Then look at the hundredths: 0, 2 and 5. The 5 is the biggest, so 0.650 wins.")
t.say("0.650 is 0.65. So the greatest is 0.65.", ANS("a", "0.65 > 5/8 > 3/5 > 0.58"), RING("a", "0.65"))
t.say("5 over 8 looked big, but 0.65 is just a little more. When fractions and decimals are mixed, put them all in the same form before you compare.")
t.done(LESSONS)

# ── G4A_DECIMALS_019: 1.75 as a mixed number ────────────────────────────────
t = T("G4A_DECIMALS_019")
t.say("We want to write 1.75 as a mixed number: a whole number and a fraction, as simple as it can be.",
      GIVEN("q", "Write 1.75 as a mixed number in lowest terms"))
t.say("The 1 before the point is 1 whole, and it stays as it is. Only the part after the point, 0.75, has to become a fraction.",
      UL("q", "1.75"), W("s", "1.75 = 1 + 0.75"))
t.ask("0.75 has two digits after the point. So which fraction is it?",
      "75/100", ["75/10", "7/5"],
      "Two digits after the point means hundredths. So 0.75 is 75 over 100.")
t.say("0.75 is 75 hundredths.", W("f1", "0.75 = 75/100"))
t.ask("Now make it simpler. Which of these numbers divides both 75 and 100?",
      "25", ["10", "20"],
      "25 goes into 75 three times, and into 100 four times. 10 and 20 do not go into 75 exactly.")
t.say("75 divided by 25 is 3. 100 divided by 25 is 4. So 0.75 is three quarters.",
      W("f2", "75/100 = 3/4"), NOTE("f2", "75/100", "÷ 25", "below"))
t.say("Put the whole back. 1.75 is 1 and three quarters.",
      ANS("a", "1.75 = 1 3/4", label=True), RING("a", "1 3/4"), FIG("f", figure_of("G4A_DECIMALS_019", 2)))
t.say("Think of money: 75 paise is three quarters of a rupee. Keep the whole, write the decimal part over 100, then simplify.",
      W("c", "1 + 3/4 = 1.75"))
t.done(LESSONS)

# ── G4A_DECIMALS_020: Tara's change from Rs. 100 ────────────────────────────
t = T("G4A_DECIMALS_020")
t.say("Tara buys a notebook, a pen and an eraser, and pays with a 100 rupee note. We want her change.",
      GIVEN("q", "Rs. 37.50 + Rs. 12.75 + Rs. 4.25. Pays Rs. 100."), GIVEN("q2", "Change = ?"),
      FIG("f", figure_of("G4A_DECIMALS_020")))
t.ask("What must we find first?",
      "the total bill", ["100 − 37.50", "the dearest item"],
      "Change is what is left after the whole bill is paid. So first we need the whole bill: all three prices added up.")
t.say("Look for friendly pairs. 12.75 and 4.25 go well together, because 0.75 and 0.25 make exactly 1 rupee. Then 12 and 4 and that 1 make 17.",
      W("p1", "0.75 + 0.25 = 1"), W("p0", "12 + 4 + 1 = 17"), W("p2", "12.75 + 4.25 = 17.00"))
t.say("Now add the notebook. 37.50 and 17 more make 54.50. That is the bill.",
      W("b", "37.50 + 17.00 = 54.50"), NOTE("b", "54.50", "the bill", "below"))
t.ask("Now how do we find the change?",
      "100 − 54.50", ["100 + 54.50", "54.50 − 37.50"],
      "The change is what is left of the 100 rupees after the bill is paid. So we take the bill away from 100.")
t.say("Count up from the bill. From 54.50 to 55 is 0.50. From 55 to 100 is 45. So the change is 45.50.",
      W("u1", "54.50 + 0.50 = 55"), W("u2", "55 + 45 = 100"), ANS("a", "100.00 − 54.50 = 45.50"), RING("a", "45.50"))
t.say("So Tara gets 45.50 rupees back. Check: the bill, 54.50, plus the change, 45.50, makes exactly 100.",
      W("c", "54.50 + 45.50 = 100"))
t.say("Two steps for change: add up the bill, then take it from the money paid. And remember, 54.50 is the bill, not the change.")
t.done(LESSONS)

# ── G4A_DECIMALS_021: bus tickets, there and back, 6 days ───────────────────
t = T("G4A_DECIMALS_021")
t.say("A bus ticket costs 12.50 rupees. Asha goes to school and comes back by bus, on 6 days. How much does she spend?",
      GIVEN("q", "Ticket Rs. 12.50. To school and back, 6 days."), GIVEN("q2", "Total = ?"))
t.ask("How many tickets does Asha need each day?",
      "2", ["1", "6"],
      "She goes to school by bus, and she comes back by bus. That is two rides, so she needs two tickets each day.")
t.say("That is the part to watch: the words and comes back. So each day she buys 2 tickets.", UL("q", "and back"))
t.say("Two tickets cost 12.50 and 12.50. The two half rupees make 1 whole rupee, so that is exactly 25 rupees a day.",
      W("d", "12.50 + 12.50 = 25"))
t.ask("Each day costs 25 rupees, and she travels on 6 days. Which sum gives the total?",
      "25 × 6", ["25 + 6", "12.50 × 6"],
      "Every one of the 6 days costs 25 rupees. So we need 6 lots of 25.")
t.say("6 lots of 25. 4 lots of 25 make 100, and 2 more lots make 50. So 6 lots make 150.",
      W("m1", "4 × 25 = 100"), W("m2", "2 × 25 = 50"), W("m3", "6 × 25 = 150"))
t.say("So Asha spends 150 rupees on tickets.", ANS("a", "Asha spends Rs. 150.00", label=True), RING("a", "Rs. 150.00"))
t.say("Check it another way: 2 tickets a day for 6 days is 12 tickets, and 12 times 12.50 is 150. Always count the tickets before you multiply.",
      W("c1", "2 × 6 = 12"), W("c2", "12 × 12.50 = 150"))
t.done(LESSONS)

# ── G4A_DECIMALS_022: Rs. 342 shared by 4 ───────────────────────────────────
t = T("G4A_DECIMALS_022")
t.say("Four friends share a bill of 342 rupees equally. How much does each one pay?",
      GIVEN("q", "Rs. 342 shared equally by 4 friends. Each = ?"), FIG("f", figure_of("G4A_DECIMALS_022")))
t.ask("Which sum do we need?",
      "342 ÷ 4", ["342 × 4", "342 − 4"],
      "Sharing equally means dividing. We divide the bill by the number of friends.")
t.say("Share the rupees first. 4 times 80 is 320. That leaves 22, and 4 times 5 is 20. So each friend gets 80 and 5, which is 85 rupees.",
      W("d1", "4 × 80 = 320"), W("d2", "342 − 320 = 22"), W("d3", "4 × 5 = 20"), W("d0", "80 + 5 = 85"))
t.say("4 times 85 is 340. So 2 rupees are still left over.", W("d4", "4 × 85 = 340"), W("d5", "342 − 340 = 2"))
t.ask("What do we do with the 2 rupees left over?",
      "change them to paise and share", ["write .2 after the 85", "leave them out"],
      "Those 2 rupees are part of the bill, so they must be shared too. We cannot give each friend a whole rupee from them, so we change them into paise.")
t.say("2 rupees are 200 paise. 200 paise shared by 4 is 50 paise each.",
      WL("pp", "2 rupees = 200 paise"), W("p", "200 ÷ 4 = 50"))
t.ask("Each friend pays 85 rupees and 50 paise. How is that written?",
      "Rs. 85.50", ["Rs. 85.05", "Rs. 85.2"],
      "50 paise is half a rupee, and that is written point five zero. Point zero five would be only 5 paise.")
t.say("So each friend pays 85.50 rupees.", ANS("a", "342 ÷ 4 = 85.50"), RING("a", "85.50"))
t.say("Check: 4 lots of 85.50 make 342. When rupees are left over after sharing, turn them into paise and keep sharing.",
      W("c", "4 × 85.50 = 342"))
t.done(LESSONS)

# ── G4A_DECIMALS_023: halfway between 2.4 and 2.5 ───────────────────────────
t = T("G4A_DECIMALS_023")
t.say("Which number is exactly halfway between 2.4 and 2.5? Here they are on a number line.",
      GIVEN("q", "Exactly halfway between 2.4 and 2.5 = ?"), FIG("f", figure_of("G4A_DECIMALS_023")))
t.say("They look like neighbours. But write each with two digits after the point, and we can see the space between them.",
      W("e1", "2.4 = 2.40"), W("e2", "2.5 = 2.50"), FIG("f", figure_of("G4A_DECIMALS_023", 0)))
t.ask("How big is the gap from 2.40 to 2.50?",
      "0.10", ["1", "0.01"],
      "2.50 is 10 hundredths more than 2.40. Ten hundredths is written 0.10.")
t.say("The gap is 0.10. Halfway means we go half of the gap. Half of 0.10 is 0.05.", W("h", "0.10 ÷ 2 = 0.05"))
t.ask("So we start at 2.40. How much do we add to reach the halfway point?",
      "0.05", ["0.5", "0.005"],
      "Half of the gap is 0.05, which is 5 hundredths. Adding 0.5 would jump far past 2.50.")
t.say("2.40 and 0.05 more is 2.45.", W("s", "2.40 + 0.05 = 2.45"),
      ANS("a", "Halfway = 2.45", label=True), RING("a", "2.45"), FIG("f", figure_of("G4A_DECIMALS_023", 3)))
t.say("Check from the other side: 2.50 take away 0.05 is also 2.45. It is the same distance from both ends.",
      W("c", "2.50 − 0.05 = 2.45"))
t.say("For a halfway number: find the gap, halve it, and add that to the smaller number.")
t.done(LESSONS)

# ── G4A_DECIMALS_024: 20 m of cloth, 6 shirts of 2.25 m ─────────────────────
t = T("G4A_DECIMALS_024")
t.say("A tailor has 20 metres of cloth. He stitches 6 shirts, and each shirt uses 2.25 metres. How much cloth is left?",
      GIVEN("q", "20 m cloth. 6 shirts, 2.25 m each. Left = ?"), FIG("f", figure_of("G4A_DECIMALS_024")))
t.ask("What must we find first?",
      "cloth for all 6 shirts", ["20 − 2.25", "20 ÷ 6"],
      "He stitches 6 shirts, not just one. So first we need the cloth for all 6 shirts.")
t.say("6 times 2.25, in two bites. 6 times 2 is 12. Then 6 times 0.25: 0.25 is a quarter, and 6 quarters make one and a half, 1.5.",
      W("m1", "6 × 2 = 12"), W("m2", "6 × 0.25 = 1.5"))
t.say("Careful there: 6 quarters is more than a whole. It is 1.5. Now put the bites together. 12 and 1.5 make 13.5 metres used.",
      W("m3", "6 × 2.25 = 12 + 1.5 = 13.5"))
t.ask("The shirts use 13.5 metres. How do we find what is left?",
      "20 − 13.5", ["20 + 13.5", "13.5 − 6"],
      "The cloth that is used is gone. So we take it away from the 20 metres he had.")
t.say("Count up from 13.5. Up to 14 is 0.5. From 14 up to 20 is 6. So 6.5 is left.",
      W("u1", "13.5 + 0.5 = 14"), W("u2", "14 + 6 = 20"), ANS("a", "20 − 13.5 = 6.5"), RING("a", "6.5"))
t.say("So 6.5 metres of cloth is left. Check: 13.5 used and 6.5 left make 20.", W("c", "13.5 + 6.5 = 20"))
t.say("Two steps: multiply to find what was used, then subtract it from what he had.")
t.done(LESSONS)

# ── G4A_DECIMALS_025: 8th number of 0.4, 0.7, 1.0, 1.3 ──────────────────────
t = T("G4A_DECIMALS_025")
t.say("Here is a pattern that keeps growing in the same way. We want its 8th number.",
      GIVEN("q", "0.4, 0.7, 1.0, 1.3, ...   8th number = ?"), FIG("f", figure_of("G4A_DECIMALS_025")))
t.ask("How much is added each time?",
      "0.3", ["0.4", "3"],
      "Look at the first two numbers. To get from 0.4 to 0.7 we add 0.3. And from 0.7 to 1.0 we add 0.3 again.")
t.say("Each jump is 0.3.", W("j", "0.4 + 0.3 = 0.7"), W("j2", "0.7 + 0.3 = 1.0"))
t.ask("We start on the 1st number. How many jumps does it take to land on the 8th number?",
      "7", ["8", "6"],
      "The 1st number needs no jump. The 2nd needs 1 jump, and the 3rd needs 2. The jumps are always one less than the position. So the 8th needs 7.")
t.say("That is the trap: 8 numbers, but only 7 jumps between them. 7 jumps of 0.3 make 2.1.", W("m", "7 × 0.3 = 2.1"))
t.say("Start at 0.4 and add 2.1. That gives 2.5.", W("s", "0.4 + 2.1 = 2.5"),
      ANS("a", "8th number = 2.5", label=True), RING("a", "2.5"))
t.say("Let's check by writing them all out. After 1.3 come 1.6, 1.9, 2.2 and 2.5. Count them: the 8th is 2.5.",
      WL("l", "0.4, 0.7, 1.0, 1.3, 1.6, 1.9, 2.2, 2.5"), UL("l", "2.5"))
t.say("In a pattern, find the jump. Then remember: to reach a number, you need one jump fewer than its position.")
t.done(LESSONS)
