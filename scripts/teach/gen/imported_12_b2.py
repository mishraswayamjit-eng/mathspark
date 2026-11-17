"""Textbook questions from batch 12, written one by one (second half)."""
from imported_12_lib import A, AL, B, CH, CIRC, E, G, GM, LB, LESSON, MINUS, NOTE, STRIKE, UL, W, split_times  # noqa: F401

T = "IPMTB_grade5_ch06_"

LESSONS = {}

# 7 bags of 25 kg into 5 kg packets.
LESSONS[T + "q019"] = LESSON(
    B("There are 7 bags of rice, with 25 kilograms in each. The rice is to be put into packets of 5 kilograms. How many packets can be filled?",
      G("q", "7 bags × 25 kg; packets of 5 kg")),
    B("What should we find first?",
      ask=CH(["25 − 5", "all the rice: 7 × 25", "7 + 25"], 1,
             "Before we can fill packets, we need to know how much rice there is. 7 bags of 25 kilograms is 7 times 25.")),
    B("7 times 25 is 175. There are 175 kilograms of rice.",
      E("a", "7 × 25"), UL("a", "175")),
    B("Now put 175 kilograms into packets of 5. 100 divided by 5 is 20, and 75 divided by 5 is 15. So that is 20 plus 15, which is 35 packets.",
      E("b1", "100 ÷ 5"), E("b2", "75 ÷ 5"), A("b", "175 ÷ 5")),
    B("Careful with the two sizes. 25 kilograms is a bag and 5 kilograms is a packet. Mixing them up is the easy slip here."),
    B("Check a second way. One bag of 25 kilograms fills 5 packets. So 7 bags fill 7 times 5, which is 35 packets.",
      E("k1", "25 ÷ 5"), E("k2", "7 × 5")),
    B("So find the total first, then divide by the size of one packet."),
)

# 25 rows of 20 rearranged into 10 rows.
LESSONS[T + "q021"] = LESSON(
    B("Bags stand in 25 rows, with 20 bags in each row. They are rearranged into 10 rows. How many bags will be in each row now?",
      G("q", "25 rows × 20 bags, rearranged into 10 rows")),
    B("When the bags are rearranged, what stays the same?",
      ask=CH(["the bags in each row", "the total number of bags", "the number of rows"], 1,
             "The rows change, and so does the number in a row. But no bag is added or taken away, so the total stays the same.")),
    B("So find the total. 25 rows of 20 bags is 500 bags.",
      E("a", "25 × 20"), UL("a", "500")),
    B("Now share the 500 bags over 10 rows. 500 divided by 10 is 50, so each row has 50 bags.",
      A("b", "500 ÷ 10")),
    B("Does that make sense? There are fewer rows now, so each row has to be longer. 50 is more than 20, so yes.",
      W("t", "50 > 20")),
    B("Check: 10 rows of 50 bags is 500 bags, the same total as before.",
      E("k", "10 × 50")),
    B("So when things are rearranged, the total does not change. Find it, then divide by the new number of rows."),
)

# Wage bill: 30 men at 2000, 10 men at 2500, 30 women at 1500.
LESSONS[T + "q023"] = LESSON(
    B("A factory has 40 men and 30 women. 30 of the men earn 2000 rupees each, the remaining 10 men earn 2500 each, and each woman earns 1500 a month. We want the monthly wage bill.",
      G("q", "Men: 30 at Rs. 2000 and 10 at Rs. 2500"), LB("q2", "Women: 30 at Rs. 1500", "given")),
    B("There are three groups to pay, so there are three multiplications. First, 30 men at 2000 rupees: that is 60,000 rupees.",
      E("g1", "30 × 2000")),
    B("Next, the 10 men at 2500 rupees: that is 25,000 rupees.",
      E("g2", "10 × 2500")),
    B("Now the 30 women at 1500 rupees. 3 times 15 is 45. So what is 30 times 1500?",
      W("h", "3 × 15 = 45"),
      ask=CH(["4500", "45,000", "4,50,000"], 1,
             "Count the zeros we set aside: one from 30 and two from 1500. That is three zeros to write after 45.")),
    B("30 women at 1500 rupees is 45,000 rupees.",
      E("g3", "30 × 1500")),
    B("Add the three groups. 60,000 plus 25,000 is 85,000, and 45,000 more makes 1,30,000 rupees.",
      E("t1", "60,000 + 25,000"), A("t", "85,000 + 45,000")),
    B("Careful with the two 30s. 30 men and 30 women are different groups with different pay, so each needs its own multiplication."),
    B("Check that nobody was missed. 30 men and 10 men make the 40 men, and the 30 women are counted once.",
      E("k", "30 + 10")),
    B("So pay each group separately, then add the groups."),
)

# 16,245 TVs a year, for two years (284 days is not needed).
LESSONS[T + "q025"] = LESSON(
    B("A unit works 284 days in a year and makes 16,245 televisions in that year. We want its production in two years.",
      G("q", "284 working days a year; 16,245 TVs a year; 2 years")),
    B("One of these numbers is not needed. Which one?",
      ask=CH(["16,245, the televisions", "284, the working days", "2, the years"], 1,
             "We are already told the whole year's production, 16,245. How many days it took does not change that.")),
    B("So we cross out the 284. Two years is simply 2 lots of 16,245.",
      STRIKE("q", "284 working days a year", "not needed"), W("l", "16,245 × 2 = ?")),
    B("Double it in two parts. 16,000 doubled is 32,000, and 245 doubled is 490.",
      E("a", "16,000 × 2"), E("b", "245 × 2")),
    B("32,000 plus 490 is 32,490 televisions.",
      A("c", "32,000 + 490")),
    B("One of the choices is 568. That is the 284 doubled: it counts working days, not televisions.",
      E("t", "284 × 2")),
    B("Check by halving. 32,490 divided by 2 is 16,245, one year's production.",
      E("k", "32,490 ÷ 2")),
    B("So read for what is asked and cross out what is not needed. Then the sum is often a simple one."),
)

# 10 books at 7, 15 notebooks at 8, 7 pencils at 3.
LESSONS[T + "q026"] = LESSON(
    B("Ramesh buys 10 books, 15 notebooks and 7 pencils. The prices are 7 rupees, 8 rupees and 3 rupees respectively. What is his total bill?",
      G("q", "10 books, 15 notebooks, 7 pencils"), LB("q2", "Rs. 7, Rs. 8, Rs. 3 respectively", "given")),
    B("Respectively means in the same order. So which price goes with the notebooks?",
      ask=CH(["Rs. 7", "Rs. 8", "Rs. 3"], 1,
             "Match first with first, second with second, third with third. Notebooks are second in the list, so they take the second price.")),
    B("10 books at 7 rupees cost 70 rupees.",
      E("a", "10 × 7"), NOTE("q", "10 books", "Rs. 7 each")),
    B("15 notebooks at 8 rupees cost 120 rupees.",
      E("b", "15 × 8"), NOTE("q", "15 notebooks", "Rs. 8 each")),
    B("And 7 pencils at 3 rupees cost 21 rupees.",
      E("c", "7 × 3"), NOTE("q", "7 pencils", "Rs. 3 each")),
    B("Add the three amounts. 70 plus 120 is 190, and 21 more makes 211 rupees.",
      E("t1", "70 + 120"), A("t", "190 + 21")),
    B("Watch the two 7s in this question. One is the price of a book, the other is the number of pencils. Mixing them up changes the bill."),
    B("Check by adding in a different order. 120 plus 21 is 141, and 141 plus 70 is 211.",
      E("k1", "120 + 21"), E("k2", "141 + 70")),
    B("So pair each thing with its own price, multiply, and add the amounts."),
)

# Rs. 990 shared by 33 students.
LESSONS[T + "q028"] = LESSON(
    B("33 students went on a trip that cost 990 rupees in all. Each pays the same. What is each student's share?",
      G("q", "Rs. 990 shared equally by 33 students")),
    B("Which sum gives one share?",
      ask=CH(["990 − 33", "990 ÷ 33", "990 × 33"], 1,
             "The cost is being split into 33 equal shares. Splitting into equal shares is dividing.")),
    B("Here is a fact that helps: 33 times 3 is 99.",
      E("a", "33 × 3")),
    B("33 times 3 is 99. So how many lots of 33 make 990?",
      ask=CH(["3", "30", "300"], 1,
             "990 is 10 times as big as 99. So we need 10 times as many lots of 33: not 3, but 30.")),
    B("33 times 30 is 990. So each student pays 30 rupees.",
      E("b", "33 × 30"), A("c", "990 ÷ 33")),
    B("Notice that 33 and 99 are both among the choices. They appear in the working, but neither one is the share."),
    B("Check: 30 rupees from each of 33 students. 30 times 30 is 900, 30 times 3 is 90, and together that is 990.",
      E("k1", "30 × 30"), E("k2", "30 × 3"), E("k3", "900 + 90")),
    B("So to share equally, divide. And a times fact you already know, like 33 times 3, can do most of the work."),
)

# Least number to add to 3600 to make a multiple of 79: 34, which is not offered.
LESSONS[T + "q031"] = LESSON(
    B("We want the least number to add to 3600 so that 79 divides the total exactly. So first we need to see how far 3600 is past a multiple of 79.",
      G("q", "3600 + ? is exactly divisible by 79"), CIRC("q", "?")),
    B("79 is 1 less than 80, and 80 times 45 is exactly 3600. So 79 times 45 is 45 less than that: 3555.",
      E("a1", "80 × 45"), W("a2", "79 × 45 = 3600 − 45"), E("a", "79 × 45")),
    B("So 3555 is a multiple of 79, and 3600 is 45 past it. That 45 is the remainder.",
      E("r", "3600 − 3555"), LB("r2", "3600 ÷ 79 = 45, remainder 45")),
    B("The remainder is 45. So what is the least number to add?",
      ask=CH(["45", "79", "79 − 45"], 2,
             "We need to climb to the next multiple of 79. We are already 45 past the last one, so the gap still to go is 79 minus 45.")),
    B("79 minus 45 is 34. So 34 is the least number to add.",
      E("g", "79 − 45"), UL("g", "34")),
    B("Check: 3600 plus 34 is 3634, and 79 times 46 is 3634 too. It divides exactly.",
      E("k1", "3600 + 34"), E("k2", "79 × 46")),
    B("Now look at the choices: 33, 47 and 79. Our 34 is not there. So the answer is none of these.",
      LB("ch", "Choices: 33, 47, 79"), AL("ans", "34 is not a choice: None of these", "None of these")),
    B("33 sits so close to 34 that one small slip in subtracting would land on it. That is why the check mattered."),
    B("So divide to find the remainder. The least number to add is the divisor minus the remainder."),
)

# 137 radios at Rs. 525.
LESSONS[T + "q036"] = LESSON(
    B("A dealer buys 137 radios at 525 rupees each. We want the cost of all the radios.",
      G("q", "137 radios at Rs. 525 each")),
    B("That is 137 times 525. Split 525 into 500 and 25, and multiply 137 by each piece.",
      W("s", "137 × 525 = 137 × 500 + 137 × 25"), UL("s", "500")),
    B("How can we get 137 times 500 quickly?",
      ask=CH(["137 × 5, then one zero", "137 × 5, then two zeros", "137 + 500"], 1,
             "500 is 5 hundreds. So multiply by 5 first, and then the hundred puts two zeros on the end.")),
    B("137 times 5 is 685. Two zeros on the end make 68,500.",
      E("a1", "137 × 5"), E("a", "137 × 500")),
    B("Now 137 times 25. 137 times 20 is 2740, and we already have 137 times 5, which is 685. Together, 3425.",
      E("b1", "137 × 20"), E("b2", "2740 + 685"), E("b", "137 × 25")),
    B("Add the two pieces. 68,500 plus 3425 is 71,925 rupees.",
      A("t", "68,500 + 3425")),
    B("The choices are very close to each other, so add with care: 500 and 425 make 925, with nothing to carry into the thousands.",
      E("t2", "500 + 425")),
    B("Check another way. 140 radios would cost 73,500. That is 3 radios too many, which is 1575. And 73,500 minus 1575 is 71,925.",
      E("k1", "140 × 525"), E("k2", "3 × 525"), E("k3", "73,500 − 1575")),
    B("So split one number into easy pieces, multiply each piece, and add them carefully."),
)

# Divisor 61 instead of 16; answer 16.
LESSONS[T + "q039"] = LESSON(
    B("A student divided by 61 when the divisor should have been 16. His answer was 16. The number being divided did not change, so we find it first.",
      G("q", "Divided by 61 instead of 16, and got 16")),
    B("How do we get back the number he divided?",
      ask=CH(["16 × 16", "61 × 16", "61 ÷ 16"], 1,
             "He really did divide by 61 and got 16. To undo a division we multiply: the divisor he used, times his answer.")),
    B("60 times 16 is 960, and one more 16 makes 976. So the number being divided is 976.",
      E("a1", "60 × 16"), E("a", "61 × 16"), UL("a", "976")),
    B("Now we divide 976 by the right divisor, 16. Look at the board before you work anything out. What is 976 divided by 16?",
      ask=CH(["16", "61", "77"], 1,
             "We built 976 as 61 times 16. So when we divide it by 16, the 16 comes back out and 61 is left.")),
    B("976 divided by 16 is 61. The correct answer is 61.",
      A("b", "976 ÷ 16")),
    B("Isn't that neat? The two numbers simply swapped places. And notice 16 is among the choices: that is the student's own answer, not the correct one."),
    B("Check: 61 lots of 16. 16 times 60 is 960, and 16 more is 976.",
      E("k", "960 + 16")),
    B("So multiply his answer by the divisor he used to get the number back. Then divide by the divisor he should have used."),
)
