"""Lessons written for single questions: past papers EXT_G4_FP_... and worksheet questions 001-003."""
from g4_gr4_decimals_lib import (ANS, FIG, GIVEN, GM, NOTE, RING, STRIKE, T, UL, W, WL, figure_of)

LESSONS = {}

# ── EXT_G4_FP_2020_012: 8 hrs 45 min as a decimal ────────────────────────────
t = T("EXT_G4_FP_2020_012")
t.say("We have 8 hours and 45 minutes. We want to write it as hours only, using a decimal.",
      GIVEN("q", "8 hrs 45 min = ? hrs"))
t.ask("The 8 whole hours are easy: they stay as 8. The tricky part is the 45 minutes. How many minutes make one whole hour?",
      "60", ["100", "10"],
      "Think of a clock. The minute hand goes all the way round in 60 minutes, and that is one hour.")
t.say("And that is the trap in this question. Minutes are parts of 60, not parts of 100. So we cannot just put the 45 after the point.",
      WL("h", "1 hour = 60 minutes"), UL("h", "60"))
t.say("45 minutes is 45 out of 60 of an hour. Let's make that fraction simpler. Divide the top and the bottom by 15.",
      W("f", "45/60 = 3/4"), NOTE("f", "45/60", "÷ 15", "below"))
t.ask("So 45 minutes is three quarters of an hour. What is three quarters as a decimal?",
      "0.75", ["0.45", "0.25"],
      "One quarter is 0.25. Three quarters is 3 lots of that, so it is more than 0.25.")
t.say("3 lots of 0.25 make 0.75. So 45 minutes is 0.75 of an hour.", W("d", "3/4 = 3 × 0.25 = 0.75"))
t.say("Now put the 8 whole hours back. 8 and 0.75 make 8.75.", W("s", "8 + 0.75 = 8.75"))
t.say("So 8 hours 45 minutes is 8.75 hours.", ANS("a", "8 hrs 45 min = 8.75 hrs", label=True), RING("a", "8.75 hrs"))
t.say("Check: 0.75 of 60 minutes is 45 minutes. It fits. For time, write the minutes over 60 first, then turn that fraction into a decimal.",
      W("c", "0.75 × 60 = 45"))
t.done(LESSONS)

# ── EXT_G4_FP_2020_032: by how much is 1.3 greater than 0.13 ────────────────
t = T("EXT_G4_FP_2020_032")
t.say("By how much is 1.3 greater than 0.13? We want the gap between the two numbers.",
      GIVEN("q", "By how much is 1.3 greater than 0.13?"))
t.ask("What do we do to find how much greater one number is than another?",
      "subtract: 1.3 − 0.13", ["divide: 1.3 ÷ 0.13", "add: 1.3 + 0.13"],
      "How much greater means the difference between them. To find a difference, we take the smaller number away from the bigger one.")
t.say("Before we subtract, the places must line up. 0.13 has two digits after the point, but 1.3 has only one. So we give 1.3 a zero at the end. It is still the same number.",
      W("e", "1.3 = 1.30"), UL("e", "1.30"))
t.say("Now we can write the subtraction with the points in line.", W("s", "1.30 − 0.13 = ?"))
t.ask("Start at the hundredths. 0 take away 3 cannot be done, so we borrow 1 tenth and turn it into 10 hundredths. How many tenths are left in 1.30?",
      "2 tenths", ["3 tenths", "1 tenth"],
      "There were 3 tenths. We borrowed 1 of them to make 10 hundredths, so 2 tenths are left.",
      NOTE("s", "1.30", "borrow 1 tenth"))
t.say("10 hundredths take away 3 hundredths leaves 7 hundredths. 2 tenths take away 1 tenth leaves 1 tenth. And 1 one take away nothing is 1.",
      W("p1", "10 − 3 = 7"), W("p2", "2 − 1 = 1"))
t.say("So 1.3 is greater than 0.13 by 1.17.", ANS("a", "1.30 − 0.13 = 1.17"), RING("a", "1.17"))
t.say("Check by adding back: 0.13 plus 1.17 makes 1.30. So for how much greater, line up the points, fill the gap with a zero, then subtract.",
      W("c", "0.13 + 1.17 = 1.30"))
t.done(LESSONS)

# ── EXT_G4_FP_2021_026: correct order of decimals ───────────────────────────
t = T("EXT_G4_FP_2021_026")
t.say("We must find the order that is correct. The little sign means is less than, so each number must be smaller than the one after it.",
      GIVEN("q", "Which order of decimals is correct?"))
t.say("Let's sort four of the numbers ourselves, and then look for the choice that matches. They all start with 4, so the whole part cannot help us. We must look after the point.",
      WL("n", "4.4    4.04    4.004    4.444"))
t.say("To compare fairly, give every number three digits after the point. Zeros at the end do not change a number.",
      FIG("f", figure_of("EXT_G4_FP_2021_026", 0)))
t.ask("Now read just the part after the point, as thousandths: 4, 40, 400 and 444. Which number is the smallest?",
      "4.004", ["4.4", "4.04"],
      "4.004 has only 4 thousandths after the point. 4.04 has 40 thousandths, and 4.4 has 400. So 4.004 is the smallest.",
      WL("k", "thousandths: 400, 40, 4, 444"))
t.say("Careful with 4.4. It looks short, but it is one of the big ones here. More digits does not mean a bigger number.",
      UL("n", "4.4"))
t.ask("And which of the four is the biggest?",
      "4.444", ["4.4", "4.04"],
      "As thousandths they are 4, 40, 400 and 444. The biggest of those is 444, and that belongs to 4.444.")
t.say("So from smallest to biggest we have 4.004, then 4.04, then 4.4, then 4.444.",
      ANS("a", "4.004 < 4.04 < 4.4 < 4.444"), RING("a", "4.004 < 4.04 < 4.4 < 4.444"))
t.say("Check each step: 4 thousandths, then 40, then 400, then 444. Each is less than the next. To order decimals, give them the same number of places, then compare.")
t.done(LESSONS)

# ── EXT_G4_FP_2022_021: 12.1212 + 17.005 − 9.1102 ───────────────────────────
t = T("EXT_G4_FP_2022_021")
t.say("Here is a sum with three decimals. We add the first two, then take away the third.",
      GM("q", "12.1212 + 17.005 − 9.1102 = ?"))
t.ask("Two of these numbers have four digits after the point. Which one does not?",
      "17.005", ["12.1212", "9.1102"],
      "Count the digits after each point. 17.005 has only three, so it is one short.")
t.say("So we give 17.005 one more zero. Careful: the zero goes at the very end, so the 5 stays in the thousandths place.",
      W("e", "17.005 = 17.0050"), UL("e", "17.0050"))
t.say("Now add the first two. From the right: 2 and 0 is 2. 1 and 5 is 6. 2 and 0 is 2. 1 and 0 is 1.",
      W("s1", "12.1212 + 17.0050 = ?"))
t.say("And the wholes: 12 and 17 make 29. So far we have 29.1262.",
      W("w1", "12 + 17 = 29"), W("s2", "12.1212 + 17.0050 = 29.1262"))
t.ask("What do we do with the 9.1102?",
      "take it away from 29.1262", ["add it to 29.1262", "take it away from 17.0050"],
      "Look at the sign in front of 9.1102. It is a minus, so we take it away from the total we have so far.")
t.say("From the right: 2 take away 2 is 0. 6 take away 0 is 6. 2 take away 1 is 1. 1 take away 1 is 0.",
      W("s3q", "29.1262 − 9.1102 = ?"))
t.say("And the wholes: 29 take away 9 is 20. That gives 20.0160.",
      W("w2", "29 − 9 = 20"), W("s3", "29.1262 − 9.1102 = 20.0160"))
t.say("So the answer is 20.0160. Notice where the 6 sits: in the thousandths place, just where the columns put it.",
      ANS("a", "12.1212 + 17.005 − 9.1102 = 20.0160"), RING("a", "20.0160"))
t.say("A quick check with the wholes only: 12 plus 17 take away 9 is 20, and our answer is just over 20. Line up the points, fill gaps with zeros, and go one column at a time.",
      W("c", "12 + 17 − 9 = 20"))
t.done(LESSONS)

# ── EXT_G4_FP_2022_024: descending order, sum of 1st and 4th (Hard) ─────────
t = T("EXT_G4_FP_2022_024")
t.say("There are two jobs here. First we put five decimals in descending order. Then we add the 1st and the 4th.",
      GIVEN("q", "0.0075, 0.219, 0.082, 0.07, 0.008"), GIVEN("q2", "Descending order. 1st + 4th = ?"))
t.say("The numbers have different lengths, and that can fool us. So we give every one four digits after the point.",
      FIG("f", figure_of("EXT_G4_FP_2022_024", 0)))
t.ask("Descending means biggest first. Which number is the biggest?",
      "0.219", ["0.0075", "0.082"],
      "0.219 is the only one with a digit in the tenths place: it has 2 tenths. All the others have 0 tenths. So it is the biggest, even though 0.0075 has more digits.")
t.say("Now read the parts after the point as whole numbers. 2190 is first. Then come 820, then 700, then 80, and last of all 75.",
      WL("k", "ten-thousandths: 2190, 820, 700, 80, 75"),
      WL("o", "0.219, 0.082, 0.07, 0.008, 0.0075"))
t.ask("Count along our ordered line. Which number is 4th?",
      "0.008", ["0.0075", "0.07"],
      "Count them off: 0.219 is 1st, 0.082 is 2nd, 0.07 is 3rd, and 0.008 is 4th. 0.0075 is the smallest, so it comes last.")
t.say("That is the trap. 0.0075 has the most digits, but 80 beats 75, so 0.008 is bigger. The 1st is 0.219 and the 4th is 0.008.",
      UL("o", "0.219"), UL("o", "0.008"))
t.say("Now add them with the points in line. 219 thousandths and 8 thousandths make 227 thousandths.",
      W("t", "219 + 8 = 227"), W("s", "0.219 + 0.008 = 0.227"))
t.say("So the sum of the 1st and the 4th is 0.227.", ANS("a", "0.219 + 0.008 = 0.227"), RING("a", "0.227"))
t.say("When decimals have different lengths, write them all with the same number of places before you compare. Then nothing can hide.")
t.done(LESSONS)

# ── EXT_G4_FP_2023_016: 23.2323 − 14.4141 + 13.0423 ─────────────────────────
t = T("EXT_G4_FP_2023_016")
t.say("Three decimals in a chain. All of them have four digits after the point, so they already line up. We work from left to right: subtract first, then add.",
      GM("q", "23.2323 − 14.4141 + 13.0423 = ?"))
t.ask("Start the subtraction from the right. 3 take away 1 is 2. The next column is 2 take away 4. Can we do that straight away?",
      "No, we borrow first", ["Yes, it is 2", "Swap them: 4 − 2"],
      "2 is smaller than 4, so we cannot take 4 away yet. And we must never swap the digits. We borrow 1 from the next place.",
      W("s1", "23.2323 − 14.4141 = ?"))
t.say("We borrow 1 from the next place, so the 2 becomes 12. And 12 take away 4 is 8. The place we borrowed from had 3, so now it has 2. And 2 take away 1 is 1.",
      W("b", "12 − 4 = 8"), W("b2", "2 − 1 = 1"))
t.say("The tenths are 2 take away 4 again. Borrow from the ones: 12 take away 4 is 8. Now the ones have only 2 left, so 2 take away 4 needs one more borrow. Again 12 take away 4 is 8.",
      NOTE("s1", "23.2323", "3 borrows in all"))
t.say("The tens had 2 and lent 1, so 1 is left, and 1 take away 1 is 0. So the subtraction gives 8.8182. Check by adding back: 8.8182 plus 14.4141 is 23.2323. Good.",
      W("s2", "23.2323 − 14.4141 = 8.8182"), W("c1", "8.8182 + 14.4141 = 23.2323"))
t.ask("Now, what do we do with the 13.0423?",
      "add it to 8.8182", ["take it away from 8.8182", "add it to 14.4141"],
      "Look at the sign in front of 13.0423. It is a plus, so we add it to what we have so far.")
t.say("From the right: 2 and 3 is 5. 8 and 2 is 10, so write 0 and carry 1. 1 and 4 and the carried 1 make 6. 8 and 0 is 8.",
      W("s3", "8.8182 + 13.0423 = ?"))
t.say("And the wholes: 8 and 13 make 21. So the answer is 21.8605.",
      W("w", "8 + 13 = 21"), ANS("a", "8.8182 + 13.0423 = 21.8605"), RING("a", "21.8605"))
t.say("A quick check with the wholes only: 23 take away 14, plus 13, is 22. Our 21.8605 is close to that. Go left to right, and borrow with care.",
      W("e", "23 − 14 + 13 = 22"))
t.done(LESSONS)

# ── EXT_G4_FP_2023_037: if 0.42 × 645 = 270.9 then 4.2 × 6.45 ───────────────
t = T("EXT_G4_FP_2023_037")
t.say("We are told that 0.42 times 645 is 270.9. Now we want 4.2 times 6.45. Good news: we do not need to multiply at all.",
      GM("q", "0.42 × 645 = 270.9"), W("q2", "4.2 × 6.45 = ?", tone="given"))
t.say("Look at the digits. 4 and 2 in both. 6, 4 and 5 in both. Only the decimal points have moved. So the answer has the same digits too, and we just have to find where its point goes.",
      UL("q", "0.42"), UL("q2", "4.2"))
t.ask("Compare 4.2 with 0.42. How many times as big is 4.2?",
      "10 times", ["100 times", "they are equal"],
      "From 0.42 to 4.2, each digit has moved one place to the left. One place to the left makes a number 10 times as big.")
t.say("So the answer becomes 10 times as big. 270.9 times 10 is 2709.", W("a1", "270.9 × 10 = 2709"))
t.ask("Now compare 6.45 with 645. What has happened?",
      "100 times smaller", ["10 times smaller", "100 times bigger"],
      "From 645 to 6.45, each digit has moved two places to the right. Two places to the right makes a number 100 times smaller.",
      UL("q", "645"), UL("q2", "6.45"))
t.say("So the answer becomes 100 times smaller. 2709 divided by 100 is 27.09.", W("a2", "2709 ÷ 100 = 27.09"))
t.say("So 4.2 times 6.45 is 27.09.", ANS("a", "4.2 × 6.45 = 27.09"), RING("a", "27.09"))
t.say("Check with an estimate: 4 times 6 is 24, and 27.09 is near 24. So the point is in the right place. Same digits, so just track how the points moved.",
      W("e", "4 × 6 = 24"))
t.done(LESSONS)

# ── EXT_G4_FP_2024_016: 1.8 + 2.3 − 1.9 + 2.7 − 3.2 ─────────────────────────
t = T("EXT_G4_FP_2024_016")
t.say("This is a long chain of adding and taking away. Here is a neat trick: collect the numbers we add in one group, and the numbers we take away in another.",
      GM("q", "1.8 + 2.3 − 1.9 + 2.7 − 3.2 = ?"))
t.ask("Which numbers are being taken away?",
      "1.9 and 3.2", ["2.3 and 2.7", "1.8 and 1.9"],
      "Look for the minus signs. There is a minus in front of 1.9 and a minus in front of 3.2.")
t.say("So 1.9 and 3.2 are taken away. The other three, 1.8, 2.3 and 2.7, are added.",
      RING("q", "− 1.9"), RING("q", "− 3.2"))
t.say("First the numbers we add. 2.3 and 2.7 are friends: together they make exactly 5. Then 5 and 1.8 make 6.8.",
      W("p", "1.8 + 2.3 + 2.7 = 6.8"))
t.say("Next the numbers we take away. 1.9 and 3.2 make 5.1.", W("m", "1.9 + 3.2 = 5.1"))
t.ask("We have added 6.8 in all, and we must take away 5.1 in all. What is 6.8 take away 5.1?",
      "1.7", ["1.6", "11.9"],
      "Do it place by place. 8 tenths take away 1 tenth leaves 7 tenths. 6 ones take away 5 ones leaves 1 one.")
t.say("8 tenths take away 1 tenth is 7 tenths, and 6 take away 5 is 1. So the answer is 1.7.",
      ANS("a", "6.8 − 5.1 = 1.7"), RING("a", "1.7"))
t.say("In a long chain, gather the pluses, gather the minuses, then subtract once. It is quicker, and there are fewer places to slip.")
t.done(LESSONS)

# ── EXT_G4_FP_2024_031: which fraction equals 0.125 ─────────────────────────
t = T("EXT_G4_FP_2024_031")
t.say("We need the fraction that is equal to 0.125. Here are the four choices.",
      GIVEN("q", "Which fraction equals 0.125?"), GIVEN("o", "4/32    6/24    5/80    8/36"))
t.say("First, turn 0.125 into a fraction. It has three digits after the point, so it is 125 thousandths.",
      W("f", "0.125 = 125/1000"))
t.ask("Let's make that simpler. 8 lots of 125 make 1000. So if we divide the top and the bottom by 125, what do we get?",
      "1/8", ["1/4", "1/5"],
      "125 divided by 125 is 1. And 1000 divided by 125 is 8, because 8 lots of 125 make 1000. So we get 1 over 8.",
      W("g", "8 × 125 = 1000"))
t.say("So 0.125 is one eighth. That is worth remembering.", W("h", "125/1000 = 1/8"), UL("h", "1/8"))
t.ask("Now we hunt for a choice that is also one eighth. In one eighth, the bottom is 8 times the top. Which choice is like that?",
      "4/32", ["6/24", "5/80", "8/36"],
      "Multiply each top by 8 and see if you get the bottom. 8 times 4 is 32, so the first one matches.")
t.say("4 over 32. Divide the top and the bottom by 4, and we get 1 over 8. So it equals 0.125.",
      ANS("a", "4/32 = 1/8 = 0.125"), RING("o", "4/32"))
t.say("The others do not match. 6 over 24 is one quarter, 5 over 80 is one sixteenth, and 8 over 36 is 2 ninths.",
      W("x1", "6/24 = 1/4"), W("x2", "5/80 = 1/16"), W("x3", "8/36 = 2/9"))
t.say("So the answer is 4 over 32. The plan: write the decimal as a fraction, simplify it, then simplify each choice and match.")
t.done(LESSONS)

# ── EXT_G4_FP_2025_016: 19.19 − 7.62 + 4.37 − 8.95 (Hard: none of these) ────
t = T("EXT_G4_FP_2025_016")
t.say("A chain of four decimals. The choices are very close together, so we must be careful. Let's gather the numbers we add, and the numbers we take away.",
      GM("q", "19.19 − 7.62 + 4.37 − 8.95 = ?"))
t.ask("Which two numbers are added?",
      "19.19 and 4.37", ["7.62 and 8.95", "19.19 and 7.62"],
      "19.19 has no sign in front, so it counts as a plus. 4.37 has a plus in front. The other two have minus signs.")
t.say("Add those two. After the point, 0.19 and 0.37 make 0.56. The wholes, 19 and 4, make 23. So we add 23.56 in all.",
      W("p1", "0.19 + 0.37 = 0.56"), W("p2", "19 + 4 = 23"), W("p", "19.19 + 4.37 = 23.56"))
t.say("Now the two we take away. 0.62 and 0.95 make 1.57. 7 and 8 make 15. Together that is 16.57.",
      W("m1", "0.62 + 0.95 = 1.57"), W("m2", "7 + 8 = 15"), W("m", "7.62 + 8.95 = 16.57"))
t.say("So we need 23.56 take away 16.57. Count up: from 16.57 to 17 is 0.43. From 17 to 23.56 is 6.56. And 0.43 plus 6.56 is 6.99.",
      W("u1", "16.57 + 0.43 = 17"), W("u2", "17 + 6.56 = 23.56"), W("s", "23.56 − 16.57 = 6.99"))
t.say("Before we trust it, check by adding back. 6.99 plus 16.57 is 23.56. Our working is sound.",
      W("c", "6.99 + 16.57 = 23.56"))
t.ask("Now look at the choices: 7.99, 5.69, 6.79, or none of these. We got 6.99. What do we pick?",
      "None of these", ["6.79, it is the closest", "7.99, it ends in 99"],
      "6.99 is not in the list. A number that only looks close is not the answer. When careful working gives a number that is not listed, we choose none of these.",
      WL("o", "Choices: 7.99, 5.69, 6.79, None of these"))
t.say("That is the trap here. The listed numbers each look a bit like 6.99, but none of them is 6.99. So the answer is none of these.",
      ANS("a", "6.99 is not listed: None of these", label=True), RING("a", "None of these"))
t.say("Work carefully, check by adding back, and then trust your answer, even when it is not one of the numbers shown.")
t.done(LESSONS)

# ── EXT_G4_WS2_CH11_001: 0.28 as a fraction in lowest terms ─────────────────
t = T("EXT_G4_WS2_CH11_001")
t.say("We want to write 0.28 as a fraction, as simple as it can be. The square shows 0.28: some of its small squares are shaded.",
      GIVEN("q", "0.28 as a fraction in lowest terms = ?"), FIG("f", figure_of("EXT_G4_WS2_CH11_001")))
t.ask("0.28 has two digits after the point. So what goes on the bottom of the fraction?",
      "100", ["10", "1000"],
      "One digit after the point means tenths. Two digits mean hundredths, so the bottom is 100. The big square in the picture is cut into 100 small squares.")
t.say("So 0.28 is 28 hundredths: 28 over 100.", W("f1", "0.28 = 28/100"))
t.ask("Lowest terms means the top and the bottom share no factor. Which of these divides both 28 and 100 exactly?",
      "4", ["7", "8"],
      "4 goes into 28 exactly 7 times, and 4 goes into 100 exactly too. 7 goes into 28, but not into 100.")
t.say("Divide the top and the bottom by 4. 28 divided by 4 is 7. 100 divided by 4 is 25.",
      W("f2", "28/100 = 7/25"), NOTE("f2", "28/100", "÷ 4", "below"))
t.say("Can we go further? 7 does not go into 25, and nothing else goes into 7. So we stop here.")
t.say("So 0.28 is 7 over 25.", ANS("a", "0.28 = 7/25"), RING("a", "7/25"))
t.say("Check: 7 times 4 is 28, and 25 times 4 is 100, so we are back at 28 over 100. Write the decimal over 10 or 100, then divide the top and the bottom until you cannot.",
      W("c1", "7 × 4 = 28"), W("c2", "25 × 4 = 100"))
t.done(LESSONS)

# ── EXT_G4_WS2_CH11_002: which is greater, 0.5 or 0.05 ──────────────────────
t = T("EXT_G4_WS2_CH11_002")
t.say("Which is greater, 0.5 or 0.05? Both have a 5 in them. But the 5 does not sit in the same place.",
      GIVEN("q", "Which is greater: 0.5 or 0.05?"))
t.ask("In 0.5, which place is the 5 in?",
      "tenths", ["hundredths", "ones"],
      "The first place after the point is the tenths place. In 0.5 the 5 comes straight after the point.")
t.say("So 0.5 is 5 tenths. In 0.05 there is a zero in the tenths place, and the 5 has been pushed along to the hundredths.",
      NOTE("q", "0.5", "5 tenths"), NOTE("q", "0.05", "5 hundredths", "below"))
t.say("To compare them fairly, give both two digits after the point. 0.5 is the same as 0.50, and that is 50 hundredths.",
      W("e", "0.5 = 0.50"), WL("h", "50 hundredths and 5 hundredths"))
t.think("50 hundredths, or 5 hundredths. Which is more? Have a think.")
t.say("Here they are on a number line. 0.50 is far to the right of 0.05.",
      FIG("f", figure_of("EXT_G4_WS2_CH11_002", 1)))
t.say("50 hundredths is more than 5 hundredths. So 0.5 is greater.", ANS("a", "0.5 > 0.05"), RING("a", "0.5"))
t.say("The same digit is worth more in a bigger place. A tenth is ten times as big as a hundredth, so look at the place first.")
t.done(LESSONS)

# ── EXT_G4_WS2_CH11_003: round 4.756 to one decimal place ───────────────────
t = T("EXT_G4_WS2_CH11_003")
t.say("We want to round 4.756 to one decimal place. That means we keep just one digit after the point.",
      GIVEN("q", "Round 4.756 to one decimal place"))
t.ask("Which digit of 4.756 is the tenths digit, the one we keep?",
      "7", ["5", "6"],
      "The tenths digit is the first digit after the point. In 4.756 that is the 7.")
t.say("So our answer will be either 4.7 or 4.8. The digit just after the 7 decides which.",
      UL("q", "7"), WL("r", "4.7 or 4.8 ?"))
t.ask("The digit after the 7 is 5. What does the rounding rule say?",
      "5 or more: round up", ["5 or more: round down", "just drop the extra digits"],
      "The rule is: if the next digit is 0 to 4, the digit we keep stays as it is. If it is 5 or more, the digit we keep goes up by 1.")
t.say("The next digit is 5, so we round up. The 7 becomes 8, and the digits after it are dropped.",
      STRIKE("q", "56", "drop"))
t.say("So 4.756 rounded to one decimal place is 4.8.", ANS("a", "4.756 ≈ 4.8"), RING("a", "4.8"))
t.say("On the number line, 4.756 sits past the middle, nearer to 4.8. So rounding up makes sense.",
      FIG("f", figure_of("EXT_G4_WS2_CH11_003", 2)))
t.say("To round: find the digit you keep, look at the one next door, and let it decide. 5 or more, up we go.")
t.done(LESSONS)
