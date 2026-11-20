"""Lessons written for single questions: Q_CH11_016-025 and Q_CH12_..."""
from g4_gr4_decimals_lib import (ANS, FIG, GIVEN, GM, RING, T, TABLE, UL, W, WL, figure_of)

LESSONS = {}

# ── Q_CH11_016: 2.5 × 0.4 ───────────────────────────────────────────────────
t = T("Q_CH11_016")
t.say("2.5 times 0.4. Two decimals to multiply.", GM("q", "2.5 × 0.4 = ?"))
t.say("First forget the points and multiply the digits. 25 times 4 is 100.", W("m", "25 × 4 = 100"))
t.ask("Now the point. 2.5 has one digit after the point, and so has 0.4. How many decimal places is that altogether?",
      "2", ["1", "3"],
      "Count one place for 2.5 and one place for 0.4. One and one make 2.")
t.say("So the answer needs two digits after the point. Count two digits from the right of 100, and put the point there. That gives 1.00.",
      W("p", "2.5 × 0.4 = 1.00"))
t.ask("1.00 is the same as which of these?",
      "1.0", ["10", "0.1"],
      "Zeros at the end, after the point, do not change a number. 1.00 and 1.0 are both just 1.")
t.say("So 2.5 times 0.4 is 1.0, which is simply 1.", ANS("a", "2.5 × 0.4 = 1.0"), RING("a", "1.0"))
t.say("Does it make sense? 0.4 is a little less than a half, and half of 2.5 is 1.25. So a little less than 1.25 is just right.",
      W("c", "2.5 ÷ 2 = 1.25"))
t.say("Multiply the digits, count the decimal places in both numbers, and give the answer that many places.")
t.done(LESSONS)

# ── Q_CH11_017: 0.03 × 0.6 ──────────────────────────────────────────────────
t = T("Q_CH11_017")
t.say("0.03 times 0.6. Both numbers are small, so the answer will be very small.", GM("q", "0.03 × 0.6 = ?"))
t.say("Forget the points and the zeros in front, and multiply the digits. 3 times 6 is 18.", W("m", "3 × 6 = 18"))
t.ask("Now count the decimal places. 0.03 has two digits after the point, and 0.6 has one. How many altogether?",
      "3", ["2", "1"],
      "Two places for 0.03 and one place for 0.6. Two and one make 3.")
t.say("So the answer needs three digits after the point. But 18 has only two digits. Hmm.")
t.ask("How do we give 18 three digits after the point?",
      "a zero in front: 0.018", ["a zero at the end: 0.180", "leave it as 0.18"],
      "A zero at the end would not move the 1 and the 8 at all. The zero must go in front, just after the point, to push them along.")
t.say("A zero goes in front of the 18. So the answer is 0.018.", ANS("a", "0.03 × 0.6 = 0.018"), RING("a", "0.018"))
t.say("Why does it work? 0.03 is 3 hundredths and 0.6 is 6 tenths. A tenth of a hundredth is a thousandth. So we get 18 thousandths.",
      W("w", "3/100 × 6/10 = 18/1000"))
t.say("When the digits are too few for the places you need, fill up with zeros just after the point.")
t.done(LESSONS)

# ── Q_CH11_020: the place of 8 in 45.783 ────────────────────────────────────
t = T("Q_CH11_020")
t.say("Here is 45.783 in a place-value chart. In which place is the digit 8?",
      GIVEN("q", "In 45.783, the digit 8 is in which place?"), FIG("f", figure_of("Q_CH11_020", 0)))
t.ask("First, is the 8 before the decimal point or after it?",
      "after the point", ["before the point"],
      "Find the point. It sits between the 5 and the 7. The 8 comes later, so it is after the point.")
t.say("After the point, the places have their own names. In order they are tenths, hundredths, thousandths.")
t.ask("Which digit after the point is the 8: the 1st, the 2nd or the 3rd?",
      "the 2nd", ["the 1st", "the 3rd"],
      "After the point come 7, then 8, then 3. So the 8 is the second one.")
t.say("The 7 is in the tenths place. The 8 is in the hundredths place. The 3 is in the thousandths place.",
      FIG("f", figure_of("Q_CH11_020", 2)))
t.say("So the 8 is in the hundredths place.", ANS("a", "The 8 is in the hundredths place", label=True), RING("a", "hundredths"))
t.say("After the point, count along: tenths, hundredths, thousandths. And listen for the t h at the end. Hundreds are on the other side of the point.")
t.done(LESSONS)

# ── Q_CH11_021: the value of 6 in 2.0639 ────────────────────────────────────
t = T("Q_CH11_021")
t.say("What is the value of the 6 in 2.0639? Here is the number, with each digit under the name of its place.",
      GIVEN("q", "What is the value of 6 in 2.0639?"),
      TABLE("f", ["Ones", "Tenths", "Hundredths", "Thousandths", "Ten-thousandths"], [["2", "0", "6", "3", "9"]]))
t.say("The 6 is not simply worth 6. What a digit is worth depends on the place it sits in.")
t.ask("Count from the decimal point. Which digit after the point is the 6?",
      "the 2nd", ["the 1st", "the 3rd"],
      "After the point come 0, and then 6. The zero counts as a digit too. So the 6 is the second one.")
t.say("Careful with that zero. It is holding the tenths place. So the 6 is one place further along, in the hundredths place.",
      UL("q", "2.0639"))
t.ask("So the 6 is worth 6 hundredths. How do we write 6 hundredths as a decimal?",
      "0.06", ["0.6", "0.006"],
      "Hundredths are the second place after the point. So we write a 0 in the tenths place, and then the 6.")
t.say("The value of the 6 is 0.06.",
      W("d", "6/100 = 0.06"), ANS("a", "Value of 6 = 6 hundredths = 0.06", label=True), RING("a", "0.06"))
t.say("The digit itself is 6. But its value here is only 0.06, because of where it sits. Name the place first, then write the value.")
t.done(LESSONS)

# ── Q_CH11_022: apples and oranges by the kilogram ──────────────────────────
t = T("Q_CH11_022")
t.say("Riya buys 2.5 kilograms of apples at 120 rupees a kilogram, and 1.25 kilograms of oranges at 80 rupees a kilogram. How much does she spend?",
      GIVEN("q", "2.5 kg apples at ₹120 per kg"), GIVEN("q2", "1.25 kg oranges at ₹80 per kg. Total = ?"),
      FIG("f", figure_of("Q_CH11_022")))
t.say("Two costs to find, and then we add them. Start with the apples. 2.5 kilograms is 2 kilograms and half a kilogram.")
t.ask("2 kilograms of apples cost 240 rupees. What does half a kilogram cost?",
      "₹60", ["₹120", "₹50"],
      "Half a kilogram costs half the price of a whole kilogram. Half of 120 is 60.",
      W("a1", "2 × 120 = 240"))
t.say("Half a kilogram costs 60. So the apples cost 240 and 60, which is 300 rupees.",
      W("a2", "120 ÷ 2 = 60"), W("a3", "240 + 60 = 300"))
t.say("Now the oranges. 1.25 kilograms is 1 kilogram and a quarter of a kilogram. The 1 kilogram costs 80 rupees.")
t.ask("What does a quarter of a kilogram of oranges cost?",
      "₹20", ["₹25", "₹40"],
      "A quarter is one of 4 equal parts. 80 shared into 4 parts is 20 each.")
t.say("A quarter costs 20. So the oranges cost 80 and 20, which is 100 rupees.",
      W("o1", "80 ÷ 4 = 20"), W("o2", "80 + 20 = 100"))
t.say("Add the two costs. 300 and 100 make 400. Riya spends 400 rupees.",
      ANS("a", "300 + 100 = 400"), RING("a", "400"), FIG("f", figure_of("Q_CH11_022", 2)))
t.say("The decimals were friendly here: point five is a half, and point two five is a quarter. Find each cost on its own, then add.",
      W("c1", "2.5 × 120 = 300"), W("c2", "1.25 × 80 = 100"))
t.done(LESSONS)

# ── Q_CH11_023: 809 ÷ 10 ────────────────────────────────────────────────────
t = T("Q_CH11_023")
t.say("809 divided by 10.", GM("q", "809 ÷ 10 = ?"), FIG("f", figure_of("Q_CH11_023")))
t.ask("809 is a whole number. Where is its decimal point?",
      "at the end: 809.0", ["at the front: 0.809", "it has none"],
      "Every whole number has a decimal point hiding at its end. We can write 809 as 809.0.")
t.say("So 809 is the same as 809.0.", W("e", "809 = 809.0"), FIG("f", figure_of("Q_CH11_023", 0)))
t.say("Dividing by 10 moves every digit one place to the right. The 8 hundreds become 8 tens. The 0 tens become 0 ones. The 9 ones become 9 tenths.")
t.ask("What happens to the 0 in the middle?",
      "it stays between the 8 and the 9", ["it drops out", "it goes to the end"],
      "Every digit keeps its order. The zero is holding a place, so it must stay between the 8 and the 9.")
t.say("So 809 divided by 10 is 80.9.", ANS("a", "809 ÷ 10 = 80.9"), RING("a", "80.9"),
      FIG("f", figure_of("Q_CH11_023", 1)))
t.say("Check: 80.9 times 10 is 809. The digits 8, 0, 9 stay in the same order. Only the point seems to hop one place to the left.",
      W("c", "80.9 × 10 = 809"))
t.done(LESSONS)

# ── Q_CH11_024: ascending order of 3.3, 3.03, 3.303, 3.33 ───────────────────
t = T("Q_CH11_024")
t.say("We must put four decimals in ascending order.", GIVEN("q", "Ascending order: 3.3, 3.03, 3.303, 3.33"))
t.ask("What does ascending order mean?",
      "smallest first", ["biggest first"],
      "Ascending means going up, like climbing stairs. So we start with the smallest and finish with the biggest.")
t.say("The numbers have different lengths, so give each one three digits after the point. Then we can compare them fairly.",
      FIG("f", figure_of("Q_CH11_024", 0)))
t.ask("They all have 3 wholes. So look after the point: 300, 030, 303 and 330. Which is the smallest?",
      "030", ["300", "303"],
      "030 is just 30. The others are all 300 or more.",
      WL("k", "after the point: 300, 030, 303, 330"))
t.say("So 3.03 comes first. It has 0 tenths, and the others all have 3 tenths. Next is 300, which is 3.3.")
t.ask("Two are left: 3.303 and 3.33. Which is bigger?",
      "3.33", ["3.303"],
      "3.33 is the same as 3.330. Now compare 330 with 303. 330 is more.")
t.say("3.303 has more digits, but 3.33 is bigger. So the order is 3.03, then 3.3, then 3.303, then 3.33.",
      ANS("a", "3.03 < 3.3 < 3.303 < 3.33"), RING("a", "3.03 < 3.3 < 3.303 < 3.33"),
      FIG("f", figure_of("Q_CH11_024", 2)))
t.say("Same number of places first. Then compare from the left. A longer decimal is not always a bigger one.")
t.done(LESSONS)

# ── Q_CH11_025: 0.25 × 0.4 × 0.8 ────────────────────────────────────────────
t = T("Q_CH11_025")
t.say("Three decimals to multiply. We take them two at a time.", GM("q", "0.25 × 0.4 × 0.8 = ?"))
t.say("Start with 0.25 times 0.4. Forget the points: 25 times 4 is 100.", W("m1", "25 × 4 = 100"), UL("q", "0.25 × 0.4"))
t.ask("0.25 has two digits after the point and 0.4 has one. So the answer needs three. Where does the point go in 100?",
      "0.100", ["1.00", "10.0"],
      "Two places and one place make three places. Count three digits from the right of 100, and put the point there.")
t.say("That gives 0.100, and 0.100 is just 0.1. It makes sense: 0.25 is a quarter, and a quarter of 0.4 is 0.1.",
      W("p1", "0.25 × 0.4 = 0.100"), W("p1b", "0.100 = 0.1"))
t.ask("Now 0.1 times 0.8. The digits give 1 times 8, which is 8. The two numbers have two decimal places altogether. So what is the answer?",
      "0.08", ["0.8", "0.008"],
      "We need two digits after the point, but 8 is only one digit. So a zero goes in front of it: 0.08.")
t.say("0.1 times 0.8 is 0.08.", W("p2", "0.1 × 0.8 = 0.08"))
t.say("So the whole product is 0.08.", ANS("a", "0.25 × 0.4 × 0.8 = 0.08"), RING("a", "0.08"))
t.say("A good check: all three numbers are less than 1, so the product must be smaller than each of them. 0.08 is. Multiply two at a time, and count the places each time.")
t.done(LESSONS)

# ── Q_CH12_002: rupees into dollars ─────────────────────────────────────────
t = T("Q_CH12_002")
t.say("One American dollar is worth 40 rupees. How many dollars do we get for 100 rupees?",
      GIVEN("q", "1 dollar = 40 rupees. 100 rupees = ? dollars"), FIG("f", figure_of("Q_CH12_002")))
t.ask("Which sum do we need?",
      "100 ÷ 40", ["100 × 40", "100 − 40"],
      "Each dollar uses up 40 rupees. We want to know how many 40s fit into 100, and that is dividing.")
t.say("Take out the whole dollars first. 2 dollars use 80 rupees. That leaves 20 rupees.",
      W("d1", "2 × 40 = 80"), W("d2", "100 − 80 = 20"), FIG("f", figure_of("Q_CH12_002", 1)))
t.ask("We have 20 rupees left, and a dollar costs 40. How much of a dollar do 20 rupees buy?",
      "half a dollar", ["a quarter of a dollar", "one more dollar"],
      "20 is half of 40. So 20 rupees buy half a dollar.")
t.say("Half a dollar. As a decimal, a half is 0.5.", W("h", "20 ÷ 40 = 0.5"))
t.say("2 dollars and half a dollar. So 100 rupees give 2.5 dollars.", ANS("a", "100 ÷ 40 = 2.5"), RING("a", "2.5"))
t.say("Check: 2.5 lots of 40 make 100. And it makes sense: 100 rupees is more than 2 lots of 40, but less than 3 lots.",
      W("c", "2.5 × 40 = 100"))
t.say("To change money, divide by what one unit costs. And when something is left over, turn it into a decimal part.")
t.done(LESSONS)

# ── Q_CH12_022: 240 paise in rupees ─────────────────────────────────────────
t = T("Q_CH12_022")
t.say("We want to write 240 paise in rupees.", GIVEN("q", "240 paise = Rs. ?"))
t.ask("How many paise make 1 rupee?",
      "100", ["10", "1000"],
      "One rupee is 100 paise.")
t.say("100 paise make 1 rupee. So 200 paise make 2 rupees.", WL("h", "100 paise = 1 rupee"), W("d1", "2 × 100 = 200"))
t.say("Take those 200 paise out of the 240. 40 paise are left over.", W("d2", "240 − 200 = 40"))
t.ask("So we have 2 rupees and 40 paise. How is that written in rupees?",
      "Rs. 2.40", ["Rs. 24.0", "Rs. 2.04"],
      "The rupees go before the point, and the paise go after it, in two places. 40 paise is point four zero.")
t.say("2 rupees and 40 paise is written 2.40.", ANS("a", "240 paise = Rs. 2.40", label=True), RING("a", "Rs. 2.40"))
t.say("That is the same as dividing 240 by 100: the digits move two places to the right.", W("c", "240 ÷ 100 = 2.40"))
t.say("To change paise into rupees, divide by 100. The rupees are much bigger than paise, so the number gets smaller.")
t.done(LESSONS)

# ── Q_CH12_023: Rs. 4.06 in paise ───────────────────────────────────────────
t = T("Q_CH12_023")
t.say("We want to write 4.06 rupees in paise.", GIVEN("q", "Rs. 4.06 = ? paise"))
t.ask("How many paise are there in 1 rupee?",
      "100", ["10", "1000"],
      "One rupee is 100 paise.")
t.say("So the 4 whole rupees are 4 lots of 100 paise. That is 400 paise.", W("d1", "4 × 100 = 400"))
t.ask("Now look after the point: zero six. How many paise is that?",
      "6 paise", ["60 paise", "0.6 paise"],
      "The two digits after the point show the paise. Zero six means just 6. For 60 paise it would say six zero.")
t.say("That is the part to watch. It is 6 paise, not 60. The zero is holding the tenths place.", UL("q", "4.06"))
t.say("400 paise and 6 paise make 406 paise.", W("d2", "400 + 6 = 406"),
      ANS("a", "Rs. 4.06 = 406 paise", label=True), RING("a", "406 paise"))
t.say("That is the same as multiplying 4.06 by 100: the digits move two places to the left.", W("c", "4.06 × 100 = 406"))
t.say("To change rupees into paise, multiply by 100. Paise are small, so there are many more of them.")
t.done(LESSONS)
