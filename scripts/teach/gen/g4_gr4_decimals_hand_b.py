"""Lessons written for single questions: worksheet questions 004-007 and G4A_DECIMALS_001-010."""
from g4_gr4_decimals_lib import (ANS, CHART, FIG, GIVEN, GM, NOTE, RING, STRIKE, T, UL, W, WL, figure_of)

LESSONS = {}

# ── EXT_G4_WS2_CH11_004: 3.25 + 1.8 ─────────────────────────────────────────
t = T("EXT_G4_WS2_CH11_004")
t.say("Let's add 3.25 and 1.8.", GM("q", "3.25 + 1.8 = ?"))
t.ask("Before we add decimals, what must we line up?",
      "the decimal points", ["the last digits", "the first digits"],
      "If we lined up the last digits, the 8 tenths would sit under the 5 hundredths. Tenths must go under tenths, so we line up the points.")
t.say("3.25 has two digits after the point, but 1.8 has only one. So we give 1.8 a zero at the end. Now both have two.",
      W("e", "1.8 = 1.80"), W("s", "3.25 + 1.80 = ?"))
t.say("Start at the hundredths. 5 and 0 make 5.", UL("s", "3.25"))
t.ask("Now the tenths. 2 tenths and 8 tenths make 10 tenths. What is 10 tenths the same as?",
      "1 whole", ["10 wholes", "1 tenth"],
      "Think of a bar cut into 10 equal pieces. All 10 pieces together are the whole bar. So 10 tenths is 1 whole.",
      W("t1", "2 + 8 = 10"))
t.say("So we write 0 in the tenths place and carry 1 to the ones. This is where slips happen: do not forget the carried 1.",
      NOTE("t1", "10", "write 0, carry 1"))
t.say("Now the ones. 3 and 1 and the carried 1 make 5. So the answer is 5.05.",
      W("o", "3 + 1 + 1 = 5"), ANS("a", "3.25 + 1.80 = 5.05"), RING("a", "5.05"))
t.say("Does it make sense? 1.8 is nearly 2, and 3.25 plus 2 would be a little over 5. Yes. Line up the points, fill gaps with zeros, and carry just as with whole numbers.")
t.done(LESSONS)

# ── EXT_G4_WS2_CH11_005: 7.5 − 2.38 ─────────────────────────────────────────
t = T("EXT_G4_WS2_CH11_005")
t.say("We want 7.5 take away 2.38.", GM("q", "7.5 − 2.38 = ?"))
t.say("2.38 has two digits after the point, and 7.5 has only one. So we write 7.5 as 7.50, and put the points in line.",
      W("e", "7.5 = 7.50"), W("s", "7.50 − 2.38 = ?"))
t.ask("Start at the hundredths: 0 take away 8. We cannot do that. So what do we do?",
      "borrow 1 tenth", ["just write 8", "do 8 − 0 instead"],
      "0 is smaller than 8, so we cannot take 8 away, and we must not swap them round. We borrow 1 tenth from the 5 tenths, and turn it into 10 hundredths.")
t.say("1 tenth is the same as 10 hundredths. Now we have 10 hundredths, and 10 take away 8 leaves 2.",
      W("h", "10 − 8 = 2"))
t.ask("We lent away 1 of the 5 tenths. How many tenths are left on top?",
      "4", ["5", "6"],
      "There were 5 tenths and we lent 1 of them to the hundredths. 5 take away 1 leaves 4.",
      NOTE("s", "7.50", "1 tenth lent"))
t.say("So the tenths are 4 take away 3, which is 1. Careful: it is 4, not 5, because of the borrowing. Then the ones: 7 take away 2 is 5.",
      W("t1", "4 − 3 = 1"), W("o", "7 − 2 = 5"))
t.say("So 7.5 take away 2.38 is 5.12.", ANS("a", "7.50 − 2.38 = 5.12"), RING("a", "5.12"))
t.say("Check by adding back: 5.12 plus 2.38 makes 7.50. Line up the points, fill the gap with a zero, and remember what you borrowed.",
      W("c", "5.12 + 2.38 = 7.50"))
t.done(LESSONS)

# ── EXT_G4_WS2_CH11_006: 0.6 × 0.3 ──────────────────────────────────────────
t = T("EXT_G4_WS2_CH11_006")
t.say("Here we multiply two decimals: 0.6 times 0.3.", GM("q", "0.6 × 0.3 = ?"))
t.say("First, forget the points for a moment and multiply the digits. 6 times 3 is 18.", W("m", "6 × 3 = 18"))
t.ask("Now we put the point back. 0.6 has one digit after the point, and 0.3 has one too. How many decimal places is that altogether?",
      "2", ["1", "3"],
      "Count one place for 0.6 and one place for 0.3. One and one make 2.")
t.say("So the answer needs 2 digits after the point. 18 with two digits after the point is 0.18.",
      W("p", "0.6 × 0.3 = 0.18"))
t.say("Why does that work? 0.6 is 6 tenths and 0.3 is 3 tenths. A tenth of a tenth is a hundredth. So we get 18 hundredths.",
      W("w", "6/10 × 3/10 = 18/100"))
t.ask("Here is a good check. Should the answer be bigger than 0.6, or smaller?",
      "smaller than 0.6", ["bigger than 0.6"],
      "0.3 is less than 1. So we are taking only a part of 0.6, and a part of something is smaller than the whole thing.")
t.say("0.18 is smaller than 0.6, so it fits. The answer is 0.18.", ANS("a", "0.6 × 0.3 = 0.18"), RING("a", "0.18"))
t.say("To multiply decimals: multiply the digits, count the decimal places in both numbers, and give the answer that many places.")
t.done(LESSONS)

# ── EXT_G4_WS2_CH11_007: 4.8 ÷ 0.4 ──────────────────────────────────────────
t = T("EXT_G4_WS2_CH11_007")
t.say("We want 4.8 divided by 0.4. Dividing by a decimal is awkward. So here is a trick: turn the number we divide by into a whole number.",
      GM("q", "4.8 ÷ 0.4 = ?"))
t.ask("What can we multiply 0.4 by to make it a whole number?",
      "10", ["2", "4"],
      "Multiplying by 10 moves each digit one place to the left. So 0.4 times 10 is 4, a whole number.")
t.say("But to keep the answer the same, we must do the same thing to both numbers. 4.8 times 10 is 48, and 0.4 times 10 is 4.",
      W("a1", "4.8 × 10 = 48"), W("a2", "0.4 × 10 = 4"))
t.say("So our sum has become 48 divided by 4. It has the same answer, and it is much friendlier.",
      W("d", "4.8 ÷ 0.4 = 48 ÷ 4"))
t.ask("What is 48 divided by 4?",
      "12", ["1.2", "120"],
      "How many fours make 48? 10 fours, and then 2 more fours. That is 12 fours.")
t.say("So 4.8 divided by 0.4 is 12.", ANS("a", "4.8 ÷ 0.4 = 12"), RING("a", "12"))
t.say("Notice the answer is bigger than 4.8. That is fine. We are asking how many small pieces of 0.4 fit into 4.8, and lots of them fit.")
t.say("Check by multiplying back: 12 times 0.4 is 4.8. To divide by a decimal, multiply both numbers by 10 until you are dividing by a whole number.",
      W("c", "12 × 0.4 = 4.8"))
t.done(LESSONS)

# ── G4A_DECIMALS_001: hundredths digit of 536.429 ───────────────────────────
t = T("G4A_DECIMALS_001")
t.say("Here is the number 536.429 in a place-value chart. We want the digit in the hundredths place.",
      GIVEN("q", "In 536.429, which digit is in the hundredths place?"), CHART("f", "536.429"))
t.say("Careful with the names. Hundreds are on the left of the point. Hundredths, with a t h on the end, are on the right of the point.",
      UL("q", "hundredths"))
t.ask("The first place after the point is the tenths place. Which digit is in the tenths place?",
      "4", ["5", "2"],
      "Find the decimal point, then look at the very next digit. It is 4.")
t.say("After tenths come hundredths, and then thousandths. So we have 4 tenths, 2 hundredths and 9 thousandths.",
      FIG("f", figure_of("G4A_DECIMALS_001", 0)))
t.say("So the digit in the hundredths place is 2.",
      ANS("a", "Hundredths digit of 536.429 = 2", label=True), RING("a", "= 2"))
t.say("The 5 is the one that tries to fool us. It is in the hundreds place, far away on the left of the point.", UL("q", "5"))
t.say("After the point, say the places in order: tenths, hundredths, thousandths. Then you will always land on the right digit.")
t.done(LESSONS)

# ── G4A_DECIMALS_002: seven and nine hundredths ─────────────────────────────
t = T("G4A_DECIMALS_002")
t.say("We want the decimal that means seven and nine hundredths. Let's build it piece by piece.",
      GIVEN("q", "Which decimal means seven and nine hundredths?"))
t.say("The word and stands for the decimal point. Seven comes before it, so we have 7 wholes, and then the point.",
      UL("q", "and"), WL("p", "seven = 7 wholes, then the point"))
t.ask("Now, nine hundredths. Which place after the point is the hundredths place?",
      "the 2nd place", ["the 1st place", "the 3rd place"],
      "After the point, the places go tenths, then hundredths. So hundredths are the second place.")
t.say("So the 9 must sit in the second place. But what about the first place, the tenths? Nobody mentioned any tenths. So a zero has to hold that place.",
      WL("p2", "tenths: none.  hundredths: 9"))
t.ask("So which decimal is it?",
      "7.09", ["7.9", "7.009"],
      "7.9 is nine tenths, and 7.009 is nine thousandths. For nine hundredths, the 9 is in the second place, with a zero before it.")
t.say("7 wholes, 0 tenths and 9 hundredths. That is 7.09.",
      ANS("a", "seven and nine hundredths = 7.09", label=True), RING("a", "7.09"),
      FIG("f", figure_of("G4A_DECIMALS_002", 2)))
t.say("The zero is a place holder. Leave it out, and the 9 slides into the tenths place and becomes ten times too big.",
      W("c", "7 + 9/100 = 7.09"))
t.done(LESSONS)

# ── G4A_DECIMALS_003: 4 + 3/10 + 7/1000 ─────────────────────────────────────
t = T("G4A_DECIMALS_003")
t.say("Three pieces to put together into one decimal. Each piece tells us which place its digit goes in.",
      GM("q", "4 + 3/10 + 7/1000 = ?"))
t.say("4 is the whole part. 3 over 10 is 3 tenths, so a 3 goes in the first place after the point.",
      NOTE("q", "3/10", "3 tenths"))
t.ask("What about 7 over 1000? That is 7 of what?",
      "thousandths", ["hundredths", "tenths"],
      "The bottom number names the place. A bottom of 10 means tenths. A bottom of 1000 means thousandths.")
t.say("Thousandths are the third place after the point. The tenths are the first. So what sits between them, in the hundredths place? Nothing was given, so a zero must hold it.",
      NOTE("q", "7/1000", "7 thousandths", "below"))
t.ask("So what is the number?",
      "4.307", ["4.37", "4.037"],
      "In 4.37 the 7 has slipped into the hundredths place. In 4.037 the 3 has slipped. We need 3 tenths, then 0 hundredths, then 7 thousandths.")
t.say("3 tenths, 0 hundredths, 7 thousandths, after the 4. That makes 4.307.",
      FIG("f", figure_of("G4A_DECIMALS_003", 2)), ANS("a", "4 + 3/10 + 7/1000 = 4.307"), RING("a", "4.307"))
t.say("A place that nobody mentions still needs a zero. Without it, the digits after it slide into places that are too big.")
t.done(LESSONS)

# ── G4A_DECIMALS_004: between 4.3 and 4.4 ───────────────────────────────────
t = T("G4A_DECIMALS_004")
t.say("We want the number that is greater than 4.3 but less than 4.4. Here are the four choices.",
      GIVEN("q", "Greater than 4.3 but less than 4.4?"), GIVEN("o", "4.03    4.43    4.5    4.35"))
t.say("4.3 and 4.4 look like next-door neighbours with nothing between them. But let's zoom in. Write both with two digits after the point.",
      W("e1", "4.3 = 4.30"), W("e2", "4.4 = 4.40"), FIG("f", figure_of("G4A_DECIMALS_004", 0)))
t.ask("Now there is room between 4.30 and 4.40. Which choice sits in there?",
      "4.35", ["4.03", "4.43", "4.5"],
      "The number must have 3 tenths, like 4.30, and then a little more. 4.03 has 0 tenths. 4.43 and 4.5 are past 4.40.")
t.say("4.35 comes after 4.30 and before 4.40. It is right between them.",
      FIG("f", figure_of("G4A_DECIMALS_004", 1)))
t.say("Why not the others? 4.03 has 0 tenths, so it is less than 4.3. And 4.43 and 4.5 are both more than 4.4.",
      STRIKE("o", "4.03", "too small"), STRIKE("o", "4.43", "too big"), STRIKE("o", "4.5", "too big"))
t.say("So the answer is 4.35.", ANS("a", "4.30 < 4.35 < 4.40"), RING("a", "4.35"))
t.say("Between any two decimals there is always room for more. Add a zero to each end, and the numbers in between show up.")
t.done(LESSONS)

# ── G4A_DECIMALS_005: 1.6 km + 0.85 km ──────────────────────────────────────
t = T("G4A_DECIMALS_005")
t.say("Riya walks 1.6 kilometres to school, and then 0.85 kilometres more to the library. How far is that in all?",
      GIVEN("q", "1.6 km, then 0.85 km. How far in all?"), FIG("f", figure_of("G4A_DECIMALS_005")))
t.ask("What do we do with the two distances to find the whole walk?",
      "add them", ["subtract them", "multiply them"],
      "She walks one part, and then another part. To find the whole walk we put the two parts together, and that is adding.")
t.say("0.85 has two digits after the point and 1.6 has one. So write 1.6 as 1.60. Careful: line up the points, not the last digits.",
      W("e", "1.6 = 1.60"), W("s", "1.60 + 0.85 = ?"))
t.say("Hundredths first. 0 and 5 make 5.")
t.ask("Now the tenths. 6 tenths and 8 tenths make 14 tenths. What do we do with 14 tenths?",
      "write 4, carry 1 whole", ["write 14", "write 4, forget the 1"],
      "10 tenths make 1 whole. So 14 tenths is 1 whole and 4 tenths. We write the 4 in the tenths place and carry the 1 to the ones.",
      W("t1", "6 + 8 = 14"))
t.say("Then the ones. 1 and 0 and the carried 1 make 2. So the total is 2.45.",
      ANS("a", "1.60 + 0.85 = 2.45"), RING("a", "2.45"))
t.say("Riya walks 2.45 kilometres in all. Does it make sense? About one and a half, plus nearly 1, is about two and a half. Yes.",
      WL("u", "Riya walks 2.45 km"))
t.say("When you add decimals, the points go in a line, and tenths are added to tenths.")
t.done(LESSONS)

# ── G4A_DECIMALS_006: 5 m − 1.35 m ──────────────────────────────────────────
t = T("G4A_DECIMALS_006")
t.say("A rope is 5 metres long. A piece of 1.35 metres is cut off. How much rope is left?",
      GIVEN("q", "5 m rope. 1.35 m cut off. Left = ?"), FIG("f", figure_of("G4A_DECIMALS_006")))
t.ask("Which sum tells us what is left?",
      "5 − 1.35", ["5 + 1.35", "1.35 − 5"],
      "A piece is cut off, so the rope gets shorter. We take 1.35 away from 5.")
t.say("5 is a whole number, so its decimal point is hiding at the end. We can write it as 5.00. Now it has two places, just like 1.35.",
      W("e", "5 = 5.00"))
t.ask("Before we work it out: will the answer be more than 4, or less than 4?",
      "less than 4", ["more than 4"],
      "Taking away just 1 would leave 4. But we take away a bit more than 1. So a bit less than 4 is left.")
t.say("Here is an easy way: count up from 1.35 to 5. First hop to the next whole number. 0.35 needs 0.65 more to make 1, so from 1.35 up to 2 is 0.65.",
      W("u0", "0.35 + 0.65 = 1"), W("u1", "1.35 + 0.65 = 2"))
t.say("Then from 2 up to 5 is 3 more. The two hops together are 3 and 0.65. That is 3.65.",
      W("u2", "2 + 3 = 5"), ANS("a", "5.00 − 1.35 = 3.65"), RING("a", "3.65"))
t.say("So 3.65 metres of rope is left. Check by adding back: 3.65 plus 1.35 makes 5.",
      W("c", "3.65 + 1.35 = 5"))
t.say("When you subtract from a whole number, write it with a point and zeros first. Then nothing gets left out.")
t.done(LESSONS)

# ── G4A_DECIMALS_007: Rs. 4.50 × 10 ─────────────────────────────────────────
t = T("G4A_DECIMALS_007")
t.say("One pencil costs 4 rupees and 50 paise, written 4.50. We want the cost of 10 pencils.",
      GIVEN("q", "1 pencil costs Rs. 4.50. Cost of 10 pencils = ?"), WL("r", "Rs. 4.50 = 4 rupees 50 paise"))
t.ask("Which sum gives the cost of 10 pencils?",
      "4.50 × 10", ["4.50 + 10", "4.50 ÷ 10"],
      "Ten pencils means ten lots of the price. Lots of means times. Adding 10 would only make it 10 rupees dearer.")
t.say("Multiplying by 10 makes every digit worth ten times as much. So every digit hops one place to the left.",
      FIG("f", figure_of("G4A_DECIMALS_007")))
t.say("The 4 ones become 4 tens. The 5 tenths become 5 ones. So 4.50 times 10 is 45.00.",
      FIG("f", figure_of("G4A_DECIMALS_007", 0)), W("m", "4.50 × 10 = 45.00"))
t.ask("Let's check it with coins. 10 lots of 4 rupees is 40 rupees. And what do 10 lots of 50 paise make?",
      "5 rupees", ["50 rupees", "half a rupee"],
      "Two 50 paise coins make 1 rupee. So ten of them make 5 rupees.",
      W("k1", "10 × 4 = 40"))
t.say("40 rupees and 5 rupees make 45 rupees. The same answer, so we can trust it.", W("k2", "40 + 5 = 45"))
t.say("So 10 pencils cost 45 rupees.", ANS("a", "10 pencils cost Rs. 45.00", label=True), RING("a", "Rs. 45.00"))
t.say("To multiply by 10, move every digit one place to the left. The digits stay the same; only their places change.")
t.done(LESSONS)

# ── G4A_DECIMALS_008: 7/20 as a decimal ─────────────────────────────────────
t = T("G4A_DECIMALS_008")
t.say("We want to write 7 over 20 as a decimal. The bar shows it: 7 parts out of 20 are shaded.",
      GIVEN("q", "Write 7/20 as a decimal"), FIG("f", figure_of("G4A_DECIMALS_008")))
t.say("Decimals are all about tenths and hundredths. So if we can change the bottom number into 100, the rest is easy.",
      W("g", "7/20 = ?/100"))
t.ask("20 times what makes 100?",
      "5", ["10", "80"],
      "Count the twenties on your fingers until you reach 100. You will need 5 of them.")
t.say("Whatever we do to the bottom, we must do to the top as well. 20 times 5 is 100, and 7 times 5 is 35.",
      W("f1", "7/20 = 35/100"), NOTE("f1", "7/20", "× 5 top and bottom", "below"))
t.ask("So we have 35 hundredths. How do we write 35 hundredths as a decimal?",
      "0.35", ["3.5", "0.035"],
      "Hundredths need two digits after the point. So 35 hundredths is 0.35. It has to be less than 1, because 7 out of 20 is less than a whole.")
t.say("So 7 over 20 is 0.35.", ANS("a", "7/20 = 0.35"), RING("a", "0.35"))
t.say("Does it make sense? 7 is less than half of 20, and 0.35 is less than a half. Yes, it fits.")
t.say("To turn a fraction into a decimal, try to make the bottom 10 or 100. Then just read it off.")
t.done(LESSONS)

# ── G4A_DECIMALS_009: 7.2 m ÷ 6 ─────────────────────────────────────────────
t = T("G4A_DECIMALS_009")
t.say("A ribbon 7.2 metres long is cut into 6 equal pieces. How long is each piece?",
      GIVEN("q", "7.2 m ribbon cut into 6 equal pieces. Each = ?"), FIG("f", figure_of("G4A_DECIMALS_009")))
t.ask("Which sum do we need?",
      "7.2 ÷ 6", ["7.2 × 6", "7.2 − 6"],
      "Equal pieces means equal sharing, and sharing is dividing.")
t.say("Let's think of 7.2 in tenths. 7 ones are 70 tenths, and 2 more tenths make 72 tenths.",
      WL("t1", "7 ones = 70 tenths. 70 + 2 = 72 tenths"))
t.ask("Now share 72 tenths into 6 equal groups. What is 72 divided by 6?",
      "12", ["13", "11"],
      "Try 6 times 12. That is 6 tens and 6 twos, and together they make 72.")
t.say("72 divided by 6 is 12. But careful: these are 12 tenths, not 12 wholes.", W("d", "72 ÷ 6 = 12"), NOTE("d", "12", "tenths"))
t.ask("How do we write 12 tenths as a decimal?",
      "1.2", ["12", "0.12"],
      "10 tenths make 1 whole. So 12 tenths is 1 whole and 2 tenths, which is written 1.2.")
t.say("So each piece is 1.2 metres long.", ANS("a", "7.2 ÷ 6 = 1.2"), RING("a", "1.2"))
t.say("Check: 6 pieces of 1.2 make 7.2. And each piece is shorter than the whole ribbon, as it must be.",
      W("c", "6 × 1.2 = 7.2"))
t.done(LESSONS)

# ── G4A_DECIMALS_010: 8 rupees and 5 paise ──────────────────────────────────
t = T("G4A_DECIMALS_010")
t.say("Aman has 8 rupees and 5 paise. We want to write that amount in rupees, with a decimal point.",
      GIVEN("q", "8 rupees and 5 paise = Rs. ?"))
t.ask("How many paise make 1 rupee?",
      "100", ["10", "50"],
      "One rupee is 100 paise. Two 50 paise coins make a rupee.")
t.say("So 1 paisa is one hundredth of a rupee. That means paise live in the hundredths place, and they always take two digits after the point.",
      WL("h", "100 paise = 1 rupee"))
t.say("5 paise is 5 hundredths of a rupee. As a decimal, that is 0.05.", W("p", "5/100 = 0.05"))
t.ask("So how do we write 8 rupees and 5 paise?",
      "Rs. 8.05", ["Rs. 8.50", "Rs. 85.00"],
      "8.50 would mean 8 rupees and 50 paise. We have only 5 paise, so a zero must sit in the tenths place.")
t.say("8 rupees, and 0.05 of a rupee. Together that is 8.05.",
      W("s", "8 + 0.05 = 8.05"), FIG("f", figure_of("G4A_DECIMALS_010", 1)))
t.say("So the amount is 8.05 rupees.", ANS("a", "8 rupees 5 paise = Rs. 8.05", label=True), RING("a", "Rs. 8.05"))
t.say("Paise always take two places after the point. 5 paise is point zero five, and 50 paise is point five zero.")
t.done(LESSONS)
