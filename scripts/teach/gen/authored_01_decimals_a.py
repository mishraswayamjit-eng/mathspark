"""Decimals, G5A_DECIMALS_001 to 006: one lesson each, written by hand."""
from authored_01_lib import (ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LANS, LB, LESSON, NOTE, STRIKE, UL, W)  # noqa: F401

LESSONS = {}
P = "G5A_DECIMALS_"

# Decimal point left out: 40.5 more -> the real number is 4.5
LESSONS[P + "001"] = LESSON(
    B("Anu copied a decimal number with one digit after the point, but she left out the decimal point. What she wrote was 40.5 more than the real number. What was the real number?",
      GIVEN("q", "Point left out. Number written is 40.5 more. Real number?")),
    B("Take a number like 2.3. Leave out the point and it becomes 23. How many times as big is that?",
      LB("l1", "2.3 → 23"),
      ask=CHOOSE(["10 times", "9 times", "100 times"], 0,
                 "Without the point, the 2 ones become 2 tens and the 3 tenths become 3 ones. Every digit is worth 10 times as much.")),
    B("So the number Anu wrote is 10 times the real number.",
      LB("l2", "written number = 10 × real number")),
    B("Now the gap. She has 10 lots of the real number where there should be 1 lot. The extra is 9 lots. So 40.5 is 9 times the real number.",
      W("l3", "10 − 1 = 9"), LB("l4", "9 × real number = 40.5")),
    B("So divide 40.5 by 9. 405 divided by 9 is 45, so 40.5 divided by 9 is 4.5. The real number was 4.5.",
      W("l5", "405 ÷ 9 = 45"), *ANSC("l6", "40.5 ÷ 9 = 4.5", "4.5")),
    B("The trap is dividing by 10. The written number is 10 times the real one, but the difference between them is only 9 times."),
    B("Check: without its point, 4.5 becomes 45. And 45 minus 4.5 is 40.5.",
      W("c1", "45 − 4.5 = 40.5")),
    B("So when a number becomes 10 times as big, it has grown by 9 times itself. Divide the growth by 9."),
)

# 2.4 hours after 9:50 a.m. is 12:14 p.m.
LESSONS[P + "002"] = LESSON(
    B("A train journey takes 2.4 hours. The train leaves at 9:50 in the morning. At what time does it arrive?",
      GIVEN("q", "Journey takes 2.4 hours. Leaves at 9:50 a.m. Arrives?")),
    B("2.4 hours is 2 whole hours and 0.4 of an hour. How many minutes is 0.4 of an hour?",
      LB("l0", "1 hour = 60 minutes"), LB("l1", "2.4 hours = 2 hours + 0.4 of an hour"),
      ask=CHOOSE(["4 minutes", "40 minutes", "24 minutes"], 2,
                 "The 4 after the point means 4 tenths of an hour, not 4 minutes and not 40 minutes. An hour has 60 minutes, so find 4 tenths of 60.")),
    B("This is the trap. The digit after the point is not a count of minutes. 0.4 of an hour is 4 tenths of 60. One tenth of 60 is 6, and 4 sixes are 24.",
      W("l2", "0.4 × 60 = 24")),
    B("So the journey takes 2 hours 24 minutes.",
      LB("l3", "2.4 hours = 2 hours 24 minutes")),
    B("Now add that to 9:50. First the 2 hours: 9:50 becomes 11:50.",
      LB("l4", "9:50 a.m. + 2 hours = 11:50 a.m.")),
    B("Then the 24 minutes. 10 of them take us to 12 noon. That leaves 14 minutes more.",
      LB("l5", "11:50 a.m. + 10 minutes = 12:00 noon"), W("l6", "24 − 10 = 14")),
    B("14 minutes past 12 is 12:14 in the afternoon. That is when the train arrives.",
      LANS("a", "Arrives at 12:14 p.m."), CIRC("a", "12:14 p.m.")),
    B("So with decimal hours, change the decimal part into minutes first, using 60 minutes in an hour. Then add."),
)

# Pencils ₹4.50, erasers ₹2.50, 12 items for ₹44 -> 7 pencils
LESSONS[P + "003"] = LESSON(
    B("A pencil costs 4.50 rupees and an eraser costs 2.50 rupees. Anu buys 12 items, some of each, and pays exactly 44 rupees. How many pencils does she buy?",
      GIVEN("q", "Pencil ₹4.50, eraser ₹2.50. 12 items cost ₹44. Pencils?")),
    B("Here is a neat way in. Pretend all 12 items were erasers, the cheaper thing. The bill would be 12 times 2.50, which is 30 rupees.",
      W("l1", "12 × 2.50 = 30")),
    B("But the real bill is 44. That is 44 minus 30, which is 14 rupees more.",
      W("l2", "44 − 30 = 14")),
    B("Now swap one eraser for a pencil. By how much does the bill go up?",
      ask=CHOOSE(["₹4.50", "₹2", "₹2.50"], 1,
                 "We put a pencil in, but we also take an eraser out. So the bill goes up by the difference between the two prices.")),
    B("A pencil costs 4.50 and an eraser costs 2.50, so each swap adds 2 rupees.",
      W("l3", "4.50 − 2.50 = 2")),
    B("We need 14 rupees more, at 2 rupees a swap. 14 divided by 2 is 7 swaps. So there are 7 pencils.",
      *ANSC("l4", "14 ÷ 2 = 7", 7)),
    B("Careful which number you give. 12 minus 7 leaves 5 erasers, but the question asks for the pencils, and that is 7.",
      W("l5", "12 − 7 = 5")),
    B("Check: 7 pencils cost 31.50 and 5 erasers cost 12.50. Together that is 44 rupees.",
      W("c1", "7 × 4.50 = 31.50"), W("c2", "5 × 2.50 = 12.50"), W("c3", "31.50 + 12.50 = 44")),
    B("So with two prices and a total: pretend everything is the cheaper item, then count how many swaps make up the extra."),
)

# Dividing by 0.25 is multiplying by 4
LESSONS[P + "004"] = LESSON(
    B("Dividing any number by 0.25 always gives the same result as doing something simpler. What is it?",
      GIVEN("q", "Dividing any number by 0.25 is the same as ...?")),
    B("First, what is 0.25? It is one quarter.",
      W("l1", "0.25 = 1/4")),
    B("Dividing by a quarter asks: how many quarters fit into the number? Think of rotis cut into quarters."),
    B("How many quarters fit into 1 whole?",
      ask=CHOOSE(["a quarter of one", "4", "25"], 1,
                 "Cut 1 whole roti into quarters and count the pieces. There are 4 of them.")),
    B("4 quarters fit into each whole. So 1 divided by 0.25 is 4.",
      W("l2", "1 ÷ 0.25 = 4")),
    B("Test it with 3. Each whole holds 4 quarters, so 3 wholes hold 3 times 4, which is 12. And 3 divided by 0.25 is 12.",
      W("l3", "3 × 4 = 12"), W("l4", "3 ÷ 0.25 = 12")),
    B("So dividing by 0.25 is the same as multiplying the number by 4.",
      LANS("a", "÷ 0.25 is the same as × 4"), CIRC("a", "× 4")),
    B("The trap is mixing up dividing by a quarter with taking a quarter. Taking a quarter makes a number smaller. Dividing by a number less than 1 makes it bigger."),
    B("So think of dividing as asking how many fit. Small pieces fit many times: 4 quarters in every whole."),
)

# Sum 7.2, difference 1.8 -> larger number 4.5
LESSONS[P + "005"] = LESSON(
    B("Two decimal numbers add up to 7.2, and their difference is 1.8. What is the larger of the two numbers?",
      GIVEN("q", "Two numbers: sum 7.2, difference 1.8. The larger number?")),
    B("Picture the two numbers as two bars. The larger bar is the smaller bar with an extra piece of 1.8 on the end.",
      LB("l1", "larger = smaller + 1.8")),
    B("If we add the difference, 1.8, to the sum, what do we have?",
      ask=CHOOSE(["2 copies of the larger number", "2 copies of the smaller number", "the larger number"], 0,
                 "The sum is one larger and one smaller. Adding 1.8 stretches the smaller one until it is as long as the larger. So now we have 2 of the larger.")),
    B("The sum is larger plus smaller. Add the 1.8, and the smaller grows to match the larger. So 7.2 plus 1.8 is twice the larger number. That is 9.",
      W("l2", "7.2 + 1.8 = 9")),
    B("Twice the larger is 9, and half of 9 is 4.5. So the larger number is 4.5.",
      *ANSC("l3", "9 ÷ 2 = 4.5", "4.5")),
    B("Check. The smaller is 4.5 minus 1.8, which is 2.7. And 4.5 plus 2.7 is 7.2. Both facts fit.",
      W("c1", "4.5 − 1.8 = 2.7"), W("c2", "4.5 + 2.7 = 7.2")),
    B("Watch the traps. Half of the sum, 3.6, would only be right if the two numbers were equal. And 2.7 is the smaller number, not the larger.",
      W("t1", "7.2 ÷ 2 = 3.6")),
    B("So: the sum plus the difference gives twice the larger number. The larger number here is 4.5."),
)

# Two-decimal-digit numbers between 3.4 and 3.5: 9
LESSONS[P + "006"] = LESSON(
    B("How many numbers with exactly two digits after the decimal point, like 3.47, are greater than 3.4 and less than 3.5?",
      GIVEN("q", "Two decimal digits, greater than 3.4 and less than 3.5")),
    B("At first it looks as if nothing fits between 3.4 and 3.5. But write both ends with two digits after the point: 3.40 and 3.50.",
      W("l1", "3.4 = 3.40"), W("l2", "3.5 = 3.50")),
    B("Now we can see the hundredths in between. They start at 3.41 and go up to 3.49.",
      LB("l3", "3.41, 3.42, 3.43, 3.44, 3.45, 3.46, 3.47, 3.48, 3.49")),
    B("Should we count 3.40 and 3.50 as well?",
      ask=CHOOSE(["Yes, both", "No, neither", "Only 3.40"], 1,
                 "3.40 is equal to 3.4, and 3.50 is equal to 3.5. The numbers must be greater than one end and less than the other, so the ends themselves stay out.")),
    B("The ends are equal to 3.4 and 3.5, so they are not between them. That is the trap: letting an end slip in, and counting one or two too many."),
    B("Count the list. The last digits run from 1 to 9, so there are 9 numbers.",
      LANS("a", "3.41 to 3.49: 9 numbers"), CIRC("a", "9 numbers")),
    B("So to count decimals between two ends: write the ends with the same number of digits, list what lies strictly between, and leave the ends out."),
)
