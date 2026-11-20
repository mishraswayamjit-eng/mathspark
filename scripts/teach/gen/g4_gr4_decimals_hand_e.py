"""Lessons written for single questions: G4A_DECIMALS_041-054."""
from g4_gr4_decimals_lib import (ANS, FIG, GIVEN, RING, STRIKE, T, UL, W, WL, figure_of)

LESSONS = {}

# ── G4A_DECIMALS_041: race times, who came second ───────────────────────────
t = T("G4A_DECIMALS_041")
t.say("Five children ran a race. Here are their times in seconds. We want to know who came second.",
      GIVEN("q", "Race times in seconds: who came second?"), FIG("f", figure_of("G4A_DECIMALS_041")))
t.ask("In a race, which time wins?",
      "the least time", ["the greatest time"],
      "The fastest runner takes the least time. So in a race, the smallest number comes first.")
t.say("The times have different numbers of digits, so let's give every one three digits after the point. Then we can compare them fairly.",
      FIG("f", figure_of("G4A_DECIMALS_041", 0)))
t.ask("Every time has the same whole part. So look after the point: 500, 450, 058, 600 and 509. Which is the smallest?",
      "058", ["450", "500"],
      "058 is just 58. That is far less than 450 or 500. A zero straight after the point makes a number small.",
      WL("k", "after the point: 500, 450, 058, 600, 509"))
t.say("058 belongs to 12.058, and that is Chetan. So Chetan came first. The next smallest is 450, which belongs to 12.45. That is Bina.",
      W("o", "12.058 < 12.45 < 12.5 < 12.509 < 12.6"), FIG("f", figure_of("G4A_DECIMALS_041", 1)))
t.say("So Bina came second.", ANS("a", "Bina came second (12.45 seconds)", label=True), RING("a", "Bina"))
t.say("Notice Dev's 12.6. It has the fewest digits, so it looks small. But it is 12.600, the slowest time of all.")
t.say("Two things to remember: give decimals the same number of places before comparing, and in a race the least time wins.")
t.done(LESSONS)

# ── G4A_DECIMALS_042: 4.□□ with different digits adding to 9 (Hard) ─────────
t = T("G4A_DECIMALS_042")
t.say("A number looks like 4 point box box. Its three digits are all different, and they add up to 9. How many such numbers are there?",
      GIVEN("q", "4.□□ : three different digits that add up to 9"), GIVEN("q2", "How many such numbers?"))
t.ask("The first digit is 4. So what must the two boxes add up to?",
      "5", ["9", "13"],
      "All three digits make 9, and the 4 is already there. 9 take away 4 leaves 5 for the two boxes.")
t.say("The boxes must make 5. Now let's list every pair that makes 5, in order, starting with 0 in the first box. That way we miss nothing.",
      W("s", "9 − 4 = 5"), WL("l", "0+5,  1+4,  2+3,  3+2,  4+1,  5+0"))
t.ask("But the digits must all be different. Which pairs break that rule?",
      "1+4 and 4+1", ["0+5 and 5+0", "2+3 and 3+2"],
      "The number already starts with 4. A pair with a 4 in it would use the digit 4 twice.")
t.say("That is the trap. Those two pairs would give a number with two 4s in it. So out they go.",
      STRIKE("l", "1+4", "4 again"), STRIKE("l", "4+1", "4 again"))
t.say("4 pairs are left. They give the numbers 4.05, 4.23, 4.32 and 4.50.", WL("n", "4.05,  4.23,  4.32,  4.50"))
t.say("Notice that 4.23 and 4.32 are different numbers, so both count. And zero is a digit too, so 4.05 and 4.50 count as well.",
      W("c1", "4 + 0 + 5 = 9"), W("c2", "4 + 2 + 3 = 9"))
t.say("So 4 such numbers can be made.", ANS("a", "4 such numbers", label=True), RING("a", "4"))
t.say("For a puzzle like this, list every possibility in an organised way. Then test each one against every rule.")
t.done(LESSONS)

# ── G4A_DECIMALS_043: closest to 50 with digits 0, 4, 5, 9 (Hard) ───────────
t = T("G4A_DECIMALS_043")
t.say("We use the digits 0, 4, 5 and 9 once each to fill the four boxes. Which number that we can make is closest to 50?",
      GIVEN("q", "Digits 0, 4, 5, 9 in □□.□□, each used once"), GIVEN("q2", "Which number is closest to 50?"))
t.say("A number can be close to 50 from below, or from above. So we find the best number on each side, and then compare the two.")
t.ask("First, just below 50. What should the number start with?",
      "49", ["45", "40"],
      "To be just under 50 we want the biggest start that is below 50. With these digits, that is 49.")
t.say("That leaves the 0 and the 5 for after the point. To get as near to 50 as we can, we make it big: 49.50. Its gap to 50 is 0.50.",
      WL("b", "Below: 49.50"), W("g1", "50 − 49.50 = 0.50"), FIG("f", figure_of("G4A_DECIMALS_043", 0)))
t.ask("Now just above 50. The number starts with 50, and the 4 and the 9 are left. Which is nearer to 50?",
      "50.49", ["50.94"],
      "We want to stay as close to 50 as we can, so the part after the point should be small. Put the 4 before the 9.")
t.say("So the best number above is 50.49. Its gap to 50 is 0.49.",
      WL("u", "Above: 50.49"), W("g2", "50.49 − 50 = 0.49"))
t.say("Now compare the two gaps: 0.50 and 0.49. It is very close! But 0.49 is the smaller gap.",
      W("cmp", "0.49 < 0.50"), FIG("f", figure_of("G4A_DECIMALS_043", 2)))
t.say("So the number closest to 50 is 50.49.", ANS("a", "Closest to 50: 50.49", label=True), RING("a", "50.49"))
t.say("The trap is to look on one side only. For closest to, always check just below and just above, then compare the gaps.")
t.done(LESSONS)

# ── G4A_DECIMALS_044: 29 pencils, singles or packets (Hard) ─────────────────
t = T("G4A_DECIMALS_044")
t.say("Pencils cost 2.50 rupees each, or 20 rupees for a packet of 10. Meena needs 29 pencils, and she may buy more than she needs. What is the least she can pay?",
      GIVEN("q", "Pencil ₹2.50 each. Packet of 10 for ₹20."), GIVEN("q2", "Needs 29, may buy more. Least cost = ?"))
t.say("In a packet, each pencil costs 20 divided by 10, which is 2 rupees. That is cheaper than 2.50. So packets are a good idea.",
      W("r", "20 ÷ 10 = 2"))
t.ask("One way is to buy exactly 29. That is 2 packets, and how many single pencils?",
      "9", ["19", "29"],
      "2 packets give 20 pencils. She needs 29, so she needs 9 more.")
t.say("2 packets cost 40 rupees. 9 singles at 2.50 each cost 22.50. So exactly 29 pencils cost 62.50.",
      W("a1", "2 × 20 = 40"), W("a2", "9 × 2.50 = 22.50"), W("a3", "40 + 22.50 = 62.50"))
t.ask("But the question says she may buy more than she needs. What else could she try?",
      "3 packets", ["29 single pencils", "1 packet and 19 singles"],
      "A third packet gives her one pencil more than she needs. That is allowed, and packets are cheap.")
t.say("3 packets give 30 pencils, and they cost 60 rupees.", W("b1", "3 × 10 = 30"), W("b2", "3 × 20 = 60"))
t.say("60 is less than 62.50! The 9 single pencils cost 22.50, but a whole extra packet costs only 20.",
      W("cmp", "60 < 62.50"))
t.say("So the least Meena can pay is 60 rupees.", ANS("a", "Least cost = ₹60", label=True), RING("a", "₹60"))
t.say("And buying all 29 as singles costs 72.50, the most of all. The words may buy more were the clue: sometimes buying extra is cheaper.",
      W("s", "29 × 2.50 = 72.50"))
t.done(LESSONS)

# ── G4A_DECIMALS_045: Kabir at the fair, working backwards (Hard) ───────────
t = T("G4A_DECIMALS_045")
t.say("Kabir spent 12.50 rupees on a snack, then half of what was left on a toy, then 5 rupees on a ride. He came home with 18.75. How much did he start with?",
      GIVEN("q", "Spent ₹12.50, then half of the rest, then ₹5."), GIVEN("q2", "Left: ₹18.75. Started with = ?"),
      FIG("f", figure_of("G4A_DECIMALS_045")))
t.say("We know the end and want the start. So we walk backwards through the story, undoing one step at a time, beginning with the last.")
t.ask("The last thing Kabir did was spend 5 rupees on a ride. How do we undo that?",
      "18.75 + 5", ["18.75 − 5", "18.75 × 2"],
      "Before the ride he still had those 5 rupees. So we give them back: we add 5.")
t.say("18.75 plus 5 is 23.75. That is what he had just before the ride.", W("s1", "18.75 + 5 = 23.75"))
t.ask("Before that, he spent half of his money on a toy. So the 23.75 is the half he kept. How do we undo the toy?",
      "double 23.75", ["halve 23.75", "add 5 again"],
      "He spent one half and kept the other half. Two equal halves make the whole, so we double.")
t.say("Double 23 is 46, and double 0.75 is 1.50. Together that is 47.50. He had 47.50 just before the toy.",
      W("d1", "2 × 23 = 46"), W("d2", "2 × 0.75 = 1.50"), W("s2", "2 × 23.75 = 47.50"))
t.say("The first thing he did was spend 12.50 on a snack. Give that back too. 47.50 plus 12.50 is 60.",
      W("s3", "47.50 + 12.50 = 60"), ANS("a", "Kabir took ₹60", label=True), RING("a", "₹60"))
t.say("Check by going forwards. 60 take away 12.50 is 47.50. Half of that is 23.75. Take away 5, and 18.75 is left. It works.",
      W("c1", "60 − 12.50 = 47.50"), W("c2", "47.50 ÷ 2 = 23.75"), W("c3", "23.75 − 5 = 18.75"))
t.say("The order matters. The 5 rupees came after the toy, so going backwards we add it before we double.")
t.done(LESSONS)

# ── G4A_DECIMALS_046: how many lie between 1/4 and 1/2 (Hard) ───────────────
t = T("G4A_DECIMALS_046")
t.say("Here are seven numbers. How many of them are greater than one quarter and less than one half?",
      GIVEN("q", "0.3, 0.045, 0.45, 0.205, 0.5, 0.26, 0.255"), GIVEN("q2", "How many are greater than 1/4 and less than 1/2?"))
t.say("First change the two fractions into decimals with three digits after the point. One quarter is 0.250, and one half is 0.500.",
      W("e1", "1/4 = 0.250"), W("e2", "1/2 = 0.500"))
t.say("Now write the seven numbers with three digits after the point too. Then each one is easy to test.",
      WL("l", "0.300 0.045 0.450 0.205 0.500 0.260 0.255"))
t.ask("Look at 0.500 in our list. Is it less than one half?",
      "No, it is equal to a half", ["Yes, so it counts"],
      "0.500 is exactly one half. The number must be less than a half, and equal is not less.")
t.say("So 0.500 is out. And two numbers are too small: 0.045 and 0.205 are both below 0.250.",
      STRIKE("l", "0.500", "equal, not less"), STRIKE("l", "0.045", "too small"), STRIKE("l", "0.205", "too small"))
t.ask("What about 0.255? Is it in or out?",
      "in: just above 0.250", ["out: below 0.250"],
      "0.255 has 5 thousandths more than 0.250. So it is a little above one quarter, and it is in.")
t.say("So four numbers fit: 0.3, 0.45, 0.26 and 0.255.",
      ANS("a", "4 numbers: 0.3, 0.45, 0.26, 0.255", label=True), RING("a", "4 numbers"),
      FIG("f", figure_of("G4A_DECIMALS_046", 3)))
t.say("Two traps here. A number equal to an end is not between the ends. And a long decimal like 0.045 can be very small. Test every number, one at a time.")
t.done(LESSONS)

# ── G4A_DECIMALS_047: three-digit decimals between 0.3 and 0.31 (Hard) ──────
t = T("G4A_DECIMALS_047")
t.say("How many numbers with exactly three digits after the point are greater than 0.3 and less than 0.31?",
      GIVEN("q", "3 digits after the point, between 0.3 and 0.31"), GIVEN("q2", "How many such numbers?"),
      FIG("f", figure_of("G4A_DECIMALS_047")))
t.say("It looks as if there is no room between 0.3 and 0.31. But write both with three digits after the point, and room appears.",
      W("e1", "0.3 = 0.300"), W("e2", "0.31 = 0.310"))
t.ask("What is the first number after 0.300 that has three digits after the point?",
      "0.301", ["0.31", "0.3001"],
      "Add one thousandth to 0.300, and we get 0.301. 0.3001 has four digits after the point, which is too many.")
t.say("Then come 0.302, 0.303, and so on, up to 0.309. The next one after that would be 0.310, which is the end itself.",
      WL("l", "0.301  0.302  0.303  0.304  0.305"), WL("l2", "0.306  0.307  0.308  0.309"))
t.ask("Do we count the two ends, 0.300 and 0.310?",
      "No, only what lies between", ["Yes, both ends", "Just 0.310"],
      "The numbers must be greater than 0.3 and less than 0.31. The two ends are equal to those, not greater or less.")
t.say("So we count from 0.301 to 0.309. The last digit runs from 1 up to 9. That is 9 numbers.",
      ANS("a", "9 numbers", label=True), RING("a", "9"))
t.say("Careful: 310 take away 300 is 10, but that counts one of the ends. Between them there are only 9.",
      W("t1", "310 − 300 = 10"))
t.say("When you count the numbers between two ends, write the ends with the same number of places, list what lies between, and leave the ends out.")
t.done(LESSONS)

# ── G4A_DECIMALS_048: order five numbers, smallest + middle ─────────────────
t = T("G4A_DECIMALS_048")
t.say("Sneha puts five numbers in order, smallest first. Then she adds the smallest and the middle one. What does she get?",
      GIVEN("q", "2.5, 2.45, 2.405, 2.08, 2.6"), GIVEN("q2", "In order. Smallest + middle = ?"))
t.say("The numbers have different lengths. A longer decimal is not always bigger. So give each one three digits after the point.",
      FIG("f", figure_of("G4A_DECIMALS_048", 0)))
t.ask("They all have 2 wholes. So look after the point: 500, 450, 405, 080 and 600. Which is the smallest?",
      "080", ["405", "500"],
      "080 is just 80. That is far less than 405. So 2.08 is the smallest, because it has 0 tenths.",
      WL("k", "after the point: 500, 450, 405, 080, 600"))
t.say("In order, the parts after the point go 080, 405, 450, 500, 600. So the numbers are 2.08, 2.405, 2.45, 2.5 and 2.6.",
      WL("o", "2.08,  2.405,  2.45,  2.5,  2.6"), FIG("f", figure_of("G4A_DECIMALS_048", 1)))
t.ask("There are five numbers in a line. Which position is the middle one?",
      "the 3rd", ["the 2nd", "the 4th"],
      "With five in a line, the middle one has two on its left and two on its right. That is the 3rd.")
t.say("The smallest is 2.08, and the 3rd, the middle one, is 2.45.", UL("o", "2.08"), UL("o", "2.45"))
t.say("Add them. Hundredths: 8 and 5 make 13, so write 3 and carry 1. Tenths: 0 and 4 and the carried 1 make 5. Ones: 2 and 2 make 4.",
      W("h", "8 + 5 = 13"), ANS("a", "2.08 + 2.45 = 4.53"), RING("a", "4.53"))
t.say("Sneha gets 4.53. Order first, with every number written to the same number of places. Then pick the ones the question asks for.")
t.done(LESSONS)

# ── G4A_DECIMALS_049: notebook costs ₹7.50 more than a pen (Hard) ───────────
t = T("G4A_DECIMALS_049")
t.say("A notebook costs 7.50 rupees more than a pen. Rohan buys 2 notebooks and 3 pens for 65 rupees. What does one notebook cost?",
      GIVEN("q", "Notebook = pen + ₹7.50"), GIVEN("q2", "2 notebooks + 3 pens = ₹65. Notebook = ?"),
      FIG("f", figure_of("G4A_DECIMALS_049")))
t.say("Here is a clever idea. Imagine swapping each notebook for a pen. Every swap makes the bill 7.50 cheaper, and in the end every item costs the same.")
t.ask("Rohan has 2 notebooks. If both are swapped for pens, how much cheaper is the bill?",
      "₹15", ["₹7.50", "₹22.50"],
      "Each notebook costs 7.50 more than a pen. There are 2 notebooks, so that is 7.50 twice.")
t.say("Two lots of 7.50 make 15. Take that extra away from the bill: 65 take away 15 is 50.",
      W("x", "2 × 7.50 = 15"), W("y", "65 − 15 = 50"))
t.say("Now we have only pens: the 2 swapped ones and the 3 real ones. That is 5 pens, costing 50 rupees.", W("n", "2 + 3 = 5"))
t.ask("So what does one pen cost?",
      "₹10", ["₹13", "₹25"],
      "5 pens cost 50 rupees. Share 50 into 5 equal parts.")
t.say("One pen costs 10 rupees. But stop! The question asks for a notebook, not a pen.", W("p", "50 ÷ 5 = 10"))
t.say("A notebook costs 7.50 more than a pen. 10 plus 7.50 is 17.50.",
      W("nb", "10 + 7.50 = 17.50"), ANS("a", "Notebook = ₹17.50", label=True), RING("a", "₹17.50"))
t.say("Check: 2 notebooks at 17.50 and 3 pens at 10 make 65. When one thing costs more than another, take off the extra first, then share.",
      W("c", "2 × 17.50 + 3 × 10 = 65"))
t.done(LESSONS)

# ── G4A_DECIMALS_050: divided by 10 instead of multiplying ──────────────────
t = T("G4A_DECIMALS_050")
t.say("Arun had to multiply a number by 10. By mistake he divided it by 10, and got 0.47. What answer should he have got?",
      GIVEN("q", "Should multiply by 10. Divided by 10: got 0.47."), GIVEN("q2", "Right answer = ?"),
      FIG("f", figure_of("G4A_DECIMALS_050")))
t.ask("He divided his number by 10 and got 0.47. How do we get back to his number?",
      "0.47 × 10", ["0.47 ÷ 10", "0.47 + 10"],
      "He divided by 10. To go back we undo that, and multiplying undoes dividing.")
t.say("Multiplying by 10 moves every digit one place to the left. 0.47 becomes 4.7. That is the number Arun started with.",
      W("s1", "0.47 × 10 = 4.7"), FIG("f", figure_of("G4A_DECIMALS_050", 0)))
t.ask("We have his number, 4.7. What was he supposed to do with it?",
      "multiply it by 10", ["divide it by 10", "nothing more"],
      "Read the first line again. Arun had to multiply the number by 10. So far we have only found the number.")
t.say("4.7 times 10. Every digit moves one more place to the left, and we get 47.",
      W("s2", "4.7 × 10 = 47"), FIG("f", figure_of("G4A_DECIMALS_050", 1)))
t.say("Arun should have got 47.", ANS("a", "Right answer = 47", label=True), RING("a", "47"))
t.say("We multiplied by 10 twice: once to undo, once to do the sum. That is the same as 0.47 times 100.",
      W("c", "0.47 × 100 = 47"))
t.say("When someone does the opposite by mistake: first undo it to find the starting number, then do what was really asked.")
t.done(LESSONS)

# ── G4A_DECIMALS_051: digits for the box in 5.□8 (Hard) ─────────────────────
t = T("G4A_DECIMALS_051")
t.say("The number 5 point box 8 has one missing digit. It must be greater than 5.4 and less than 5.68. How many different digits can go in the box?",
      GIVEN("q", "5.□8 is greater than 5.4 and less than 5.68"), GIVEN("q2", "How many digits can go in the box?"),
      FIG("f", figure_of("G4A_DECIMALS_051")))
t.say("Our number has two digits after the point. So write 5.4 as 5.40, to match. Now we test the digits one by one.",
      W("e", "5.4 = 5.40"))
t.ask("Try 3 in the box. That gives 5.38. Is 5.38 greater than 5.40?",
      "No, 5.38 is smaller", ["Yes, 5.38 is bigger"],
      "Compare the tenths. 5.38 has 3 tenths and 5.40 has 4 tenths. So 5.38 is smaller.",
      WL("t1", "5.38 and 5.40"))
t.say("So 3 is too small, and so are 0, 1 and 2. They give 5.08, 5.18, 5.28 and 5.38, all below 5.40.",
      WL("x", "5.08, 5.18, 5.28, 5.38: too small"))
t.say("Try 4. That gives 5.48, which is above 5.40 and below 5.68. It fits. Try 5. That gives 5.58, and it fits too.",
      W("ok1", "5.40 < 5.48 < 5.68"), W("ok2", "5.40 < 5.58 < 5.68"))
t.ask("Now try 6 in the box. That gives 5.68. Is it less than 5.68?",
      "No, it is equal", ["Yes, it fits"],
      "5.68 and 5.68 are the same number. The rule says less than, and equal is not less.")
t.say("So 6 does not fit, and 7, 8 and 9 are bigger still. Only the digits 4 and 5 fit.",
      FIG("f", figure_of("G4A_DECIMALS_051", 2)))
t.say("So 2 different digits can go in the box.", ANS("a", "2 digits fit: 4 and 5", label=True), RING("a", "2 digits"))
t.say("Test the digits one by one, and take extra care at the two ends. Equal to an end is not inside.")
t.done(LESSONS)

# ── G4A_DECIMALS_052: tea and samosas, change from ₹100 ─────────────────────
t = T("G4A_DECIMALS_052")
t.say("Four friends are at a tea stall. Tea costs 12.50 rupees and a samosa costs 7.50. Everyone has tea. All except one have a samosa. They pay with 100 rupees.",
      GIVEN("q", "Tea ₹12.50, samosa ₹7.50. 4 friends, ₹100 note."),
      GIVEN("q2", "All have tea. All but one have a samosa. Change = ?"), FIG("f", figure_of("G4A_DECIMALS_052")))
t.ask("There are 4 cups of tea. How many samosas are there?",
      "3", ["4", "1"],
      "All of them except one. There are 4 friends, so take 1 away. 3 friends eat a samosa.")
t.say("First the tea. 2 cups cost 12.50 twice, which is 25. So 4 cups cost double that: 50 rupees.",
      W("t1", "2 × 12.50 = 25"), W("t2", "4 × 12.50 = 50"))
t.say("Now the 3 samosas. 3 lots of 7 is 21, and 3 lots of half a rupee is 1.50. So the samosas cost 22.50.",
      W("m1", "3 × 7 = 21"), W("m2", "3 × 0.50 = 1.50"), W("m3", "3 × 7.50 = 22.50"))
t.say("Add them for the bill. 50 and 22.50 make 72.50.", W("b", "50 + 22.50 = 72.50"), UL("b", "72.50"))
t.ask("Is 72.50 our answer?",
      "No, we need the change", ["Yes, that is the answer"],
      "72.50 is the bill. The question asks how much comes back from the 100 rupee note.")
t.say("Count up from the bill. From 72.50 to 73 is 0.50. From 73 to 100 is 27. So the change is 27.50.",
      W("u1", "72.50 + 0.50 = 73"), W("u2", "73 + 27 = 100"), ANS("a", "100 − 72.50 = 27.50"), RING("a", "27.50"))
t.say("Check: the bill, 72.50, plus the change, 27.50, makes 100. Count the things carefully before you multiply, and finish the question.",
      W("c", "72.50 + 27.50 = 100"))
t.done(LESSONS)

# ── G4A_DECIMALS_053: who has the most juice left (Hard) ────────────────────
t = T("G4A_DECIMALS_053")
t.say("Four children have bottles of juice of the same size. The table shows how much of the bottle each one drank. Who has the most juice left?",
      GIVEN("q", "Who has the most juice left?"), FIG("f", figure_of("G4A_DECIMALS_053")))
t.ask("The child with the most left is the child who drank what?",
      "the least", ["the most"],
      "The bottles start the same. The more you drink, the less is left. So the child who drank the least has the most left.")
t.say("So we are hunting for the smallest amount drunk. Let's change the fractions to decimals. One eighth is 0.125, so 5 eighths is 0.625.",
      W("g0", "1/8 = 0.125"), W("g1", "5/8 = 5 × 0.125 = 0.625"))
t.ask("Now 13 over 20. 20 times 5 is 100, and 13 times 5 is 65. So what is 13 over 20 as a decimal?",
      "0.65", ["6.5", "0.13"],
      "We have 65 over 100, which is 65 hundredths. Hundredths take two digits after the point, so it is 0.65.",
      W("h0", "20 × 5 = 100"), W("h1", "13 × 5 = 65"))
t.say("13 over 20 is 0.65. Now all four are decimals.",
      W("h2", "13/20 = 65/100 = 0.65"), FIG("f", figure_of("G4A_DECIMALS_053", 1)))
t.say("With three digits each: 0.600, 0.625, 0.580 and 0.650. Only one of them has 5 tenths. The rest have 6 tenths. So 0.580 is the smallest.",
      FIG("f", figure_of("G4A_DECIMALS_053", 2)))
t.say("0.58 is Charu's. She drank the least, so Charu has the most juice left.",
      ANS("a", "Charu drank the least (0.58): most left", label=True), RING("a", "Charu"))
t.say("Watch the flip in this question. Dinu drank the most, so Dinu has the least left. Most left means least drunk.")
t.done(LESSONS)

# ── G4A_DECIMALS_054: the forgotten decimal point (Hard) ────────────────────
t = T("G4A_DECIMALS_054")
t.say("Sana copied a number with two digits after the point, but forgot the point. Her number is 14.85 more than the real one. What is the real number?",
      GIVEN("q", "A number with 2 decimal places, written with no point"), GIVEN("q2", "It became 14.85 bigger. Real number = ?"))
t.say("This is hard to solve forwards. But we have four choices, so let's test them. Rub out the point, and see how much bigger the number gets.",
      WL("o", "1.50    0.85    0.15    0.51"))
t.ask("Start with 1.50. Without its point, what does it become?",
      "150", ["15", "1500"],
      "Just rub out the point and read the digits that are left: 1, 5, 0. That is 150.")
t.say("150 take away 1.50 is 148.50. That is far more than 14.85. So 1.50 is out, and we need a much smaller number.",
      W("t1", "150 − 1.50 = 148.50"), STRIKE("o", "1.50", "too big"))
t.say("Try 0.85. Without the point it is 85. And 85 take away 0.85 is 84.15. Still too much.",
      W("t2", "85 − 0.85 = 84.15"), STRIKE("o", "0.85", "too big"))
t.ask("Try 0.15. Without the point it is 15. What is 15 take away 0.15?",
      "14.85", ["15.15", "14.15"],
      "Taking a little bit from 15 leaves just under 15. Take the 0.15 out of one of the wholes, and that whole becomes 0.85. So the answer is 14.85.")
t.say("15 take away 0.15 is 14.85. That matches the question exactly! So the real number is 0.15.",
      W("t3", "15 − 0.15 = 14.85"), ANS("a", "Real number = 0.15", label=True), RING("a", "0.15"))
t.say("The last choice, 0.51, becomes 51, and that is 50.49 bigger. So it is out too. Notice that 1.50 had the right digits, but its gap was ten times too big.",
      W("t4", "51 − 0.51 = 50.49"))
t.say("When a puzzle is hard to work forwards, test each choice against the story. One of them will fit.")
t.done(LESSONS)
