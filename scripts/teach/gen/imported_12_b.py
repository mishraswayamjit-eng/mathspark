"""Textbook questions from batch 12, written one by one (first half)."""
from imported_12_lib import A, AL, B, CH, CIRC, E, G, GM, LB, LESSON, MINUS, NOTE, STRIKE, UL, W, split_times  # noqa: F401

T = "IPMTB_grade5_ch06_"

LESSONS = {}

# A6BC × 7 = D9E98: find D.  (5614 × 7 = 39298)
LESSONS["IPM2020_G5_Q01"] = LESSON(
    B("Here is a multiplication in disguise. Each letter hides one digit, and different letters hide different digits. We have to find the digit behind the letter D.",
      G("q", "A6BC × 7 = D9E98")),
    B("We work from the right hand end, the ones, just as we do in any multiplication. The letter C times 7 has to end in 8.",
      UL("q", "C"), UL("q", "8", 1)),
    B("Which digit is hiding behind C?",
      ask=CH(["8, because the answer ends in 8", "4, because 4 × 7 = 28", "2, because 2 × 7 = 14"], 1,
             "Run through the 7 times table and watch the last digits. Only 4 times 7, which is 28, ends in 8.")),
    B("So C is 4. 4 times 7 is 28: we write the 8 and carry 2.",
      E("c", "4 × 7"), NOTE("c", "28", "write 8, carry 2")),
    B("Next, the letter B. B times 7, plus the 2 we carried, must end in 9.",
      UL("q", "B"), UL("q", "9", 2)),
    B("Only 1 fits: 1 times 7 is 7, and 2 more is 9. So B is 1, with nothing to carry.",
      E("b", "1 × 7 + 2")),
    B("Now the 6. 6 times 7 is 42. So E is 2, and we carry 4.",
      E("e", "6 × 7"), NOTE("e", "42", "write 2, carry 4")),
    B("Last, the letter A. A times 7, plus the 4 we carried, gives a number that ends in 9. So A times 7 on its own must end in which digit?",
      ask=CH(["9", "5", "3"], 1,
             "The carried 4 gets added on. To finish at 9 after adding 4, the letter A times 7 has to end in 5.")),
    B("Only 5 times 7 ends in 5. It is 35, and adding the carried 4 gives 39. So A is 5, and the digit in front, D, is 3.",
      E("a1", "5 × 7"), E("a", "35 + 4"), AL("ans", "D = 3", "3")),
    B("Check by putting every digit back. 5614 times 7 is 39,298. That matches the pattern, and all five letters are different digits.",
      E("k", "5614 × 7")),
    B("So in a letter puzzle, start from the ones, use the last digit of each times fact, and never forget the carry."),
)

# Divided by 16 instead of multiplying: quotient 7, remainder 14.
LESSONS[T + "q001"] = LESSON(
    B("A student was supposed to multiply a number by 16. Instead he divided it by 16, and got 7 with 14 left over. What should the answer have been?",
      G("q", "? ÷ 16 = 7, remainder 14.   What is ? × 16"), CIRC("q", "?")),
    B("Before we can multiply, we need the number he started with. Which sum rebuilds it?",
      ask=CH(["16 × 7 − 14", "16 + 7 + 14", "16 × 7 + 14"], 2,
             "Dividing made 7 groups of 16, with 14 left over. To rebuild the number, put the 7 groups of 16 together and add the 14 back on.")),
    B("7 groups of 16 make 112. Add the 14 left over and we have 126. That is the number he started with.",
      LB("f", "Number = divisor × quotient + remainder"), E("n1", "16 × 7"), E("n", "112 + 14"), UL("n", "126")),
    B("Careful: 126 is one of the choices, but it is only the starting number. The question wants what he should have got by multiplying it by 16."),
    split_times(126, 16, 10, "+", 6, "m",
                "So now the sum he was meant to do: 126 times 16. Split 16 into 10 and 6.",
                mid="126 times 10 is 1260. And 126 times 6 is 756.",
                end="1260 plus 756 is 2016. The correct answer is 2016.", final=True),
    B("Check by dividing back. 2016 divided by 16 is 126, the number we rebuilt.",
      E("k", "2016 ÷ 16")),
    B("So first undo the slip to find the number: divisor times quotient, plus remainder. Then do the sum that was really asked."),
)

# 135 TV sets at Rs. 15,025.
LESSONS[T + "q003"] = LESSON(
    B("A dealer buys 135 television sets, and each one costs 15,025 rupees. We want the cost of all of them.",
      G("q", "135 TV sets at Rs. 15,025 each")),
    B("Which sum gives the total cost?",
      ask=CH(["135 + 15,025", "135 × 15,025", "15,025 ÷ 135"], 1,
             "Every set costs the same 15,025 rupees, and there are 135 of them. 135 equal lots means we multiply.")),
    B("Big numbers are tamed by splitting. 135 is 100 plus 30 plus 5, so we multiply 15,025 by each piece.",
      W("s", "15,025 × 135 = 15,025 × (100 + 30 + 5)"), UL("s", "(100 + 30 + 5)")),
    B("15,025 times 100: write two zeros on the end. That is 15,02,500.",
      E("m1", "15,025 × 100")),
    B("15,025 times 30. First times 3, which is 45,075. Then times 10 puts a zero on the end: 4,50,750.",
      E("m2a", "15,025 × 3"), E("m2", "15,025 × 30")),
    B("15,025 times 5. Times 10 would be 1,50,250, and 5 is half of 10, so halve it: 75,125.",
      E("m3a", "15,025 × 10"), E("m3", "15,025 × 5")),
    B("Now add the three pieces. 15,02,500 plus 4,50,750 is 19,53,250. Then 75,125 more makes 20,28,375 rupees.",
      E("t1", "15,02,500 + 4,50,750"), A("t", "19,53,250 + 75,125")),
    B("A rough check: 15,000 times 135 is 20,25,000. Our answer is a little more than that, as it should be. So the size is right.",
      E("k", "15,000 × 135")),
    B("So for a big multiplication: split one number into easy pieces, multiply each piece, and add them with the places lined up."),
)

# Wage bill: 20 men at 3000, 30 men at 2500, 10 boys at 1000.
LESSONS[T + "q006"] = LESSON(
    B("A factory has 50 men and 10 boys. 20 of the men earn 3000 rupees a month each, the remaining men earn 2500 each, and each boy earns 1000. We want the whole month's wage bill.",
      G("q", "50 men: 20 at Rs. 3000, the rest at Rs. 2500"), LB("q2", "10 boys at Rs. 1000", "given")),
    B("How many men earn 2500 rupees?",
      ask=CH(["50", "30", "20"], 1,
             "20 of the 50 men are already counted in the 3000 rupee group. The remaining men are 50 minus 20.")),
    B("50 minus 20 is 30. So 30 men earn 2500 rupees each.",
      E("r", "50 − 20"), NOTE("q", "the rest", "30 men")),
    B("Now pay each group. 20 men at 3000 rupees is 60,000 rupees.",
      E("g1", "20 × 3000")),
    B("30 men at 2500 rupees is 75,000 rupees.",
      E("g2", "30 × 2500")),
    B("And 10 boys at 1000 rupees is 10,000 rupees.",
      E("g3", "10 × 1000")),
    B("Add the three groups. 60,000 plus 75,000 plus 10,000 is 1,45,000 rupees.",
      A("t", "60,000 + 75,000 + 10,000")),
    B("The choices all use the same leading digits, so the zeros decide it. Our total is one lakh and forty five thousand: 1,45,000."),
    B("Check that nobody was missed. 20 plus 30 plus 10 is 60 people, the same as 50 men and 10 boys.",
      E("k1", "20 + 30 + 10"), E("k2", "50 + 10")),
    B("So split the workers into groups that earn the same, pay each group, then add the groups."),
)

# 1610 boxes a day in August.
LESSONS[T + "q007"] = LESSON(
    B("A unit makes 1610 boxes every day. We want its production for the whole month of August.",
      G("q", "1610 boxes every day, for the month of August")),
    B("The question hides one number from us. How many days does August have?",
      ask=CH(["30", "31", "28"], 1,
             "Count the months on your knuckles. July and August both land on a knuckle, so both have 31 days.")),
    B("August has 31 days. So we want 1610 times 31.",
      LB("d", "August = 31 days"), UL("d", "31")),
    B("31 is 30 plus 1. So we find 1610 times 30, and then add one more 1610.",
      W("s", "1610 × 31 = 1610 × 30 + 1610 × 1"), UL("s", "30")),
    B("1610 times 3 is 4830, so 1610 times 30 is 48,300.",
      E("m1", "1610 × 3"), E("m2", "1610 × 30")),
    B("Add the last day's 1610. 48,300 plus 1610 is 49,910 boxes.",
      A("t", "48,300 + 1610")),
    B("Careful: treating August as a 30 day month would lose a whole day, 1610 boxes."),
    B("A rough check: 1600 times 31 is 49,600. Our answer is a little more than that, so it looks right.",
      E("k", "1600 × 31")),
    B("So find the hidden number first, the days in the month. Then multiply."),
)

# 10 books + 5 notebooks = Rs. 140; notebook Rs. 8.
LESSONS[T + "q009"] = LESSON(
    B("10 books and 5 notebooks cost 140 rupees altogether. Each notebook costs 8 rupees. We want the price of one book.",
      G("q", "10 books + 5 notebooks = Rs. 140; a notebook is Rs. 8")),
    B("We know the price of a notebook. So what can we work out straight away?",
      ask=CH(["140 ÷ 10", "the cost of all 5 notebooks", "140 ÷ 15"], 1,
             "The 140 rupees paid for books and notebooks together, so we cannot share it out yet. First find what the 5 notebooks cost.")),
    B("5 notebooks at 8 rupees each cost 40 rupees.",
      E("a", "5 × 8")),
    B("Take the notebooks out of the bill. 140 minus 40 is 100, so the books cost 100 rupees.",
      E("b", "140 − 40"), STRIKE("q", "5 notebooks", "− 40")),
    B("100 rupees bought 10 books. 100 divided by 10 is 10, so each book costs 10 rupees.",
      A("c", "100 ÷ 10")),
    B("The trap is dividing 140 by all 15 things. That would treat a book and a notebook as the same price, and they are not."),
    B("Check: 10 books at 10 rupees and 5 notebooks at 8 rupees. That is 100 plus 40, which is 140.",
      E("k", "10 × 10 + 5 × 8")),
    B("So take away the part you know, then share what is left among the things you do not know."),
)

# Rs. 7070 shared by 35 students.
LESSONS[T + "q010"] = LESSON(
    B("35 students went on a trip that cost 7070 rupees in all. Each pays the same. How much is one student's share?",
      G("q", "Rs. 7070 shared equally by 35 students")),
    B("Which sum gives one share?",
      ask=CH(["7070 × 35", "7070 − 35", "7070 ÷ 35"], 2,
             "The cost is being split into 35 equal shares. Splitting into equal shares is dividing.")),
    B("Look closely at 7070. It is 7000 and 70, and both of those are friendly to 35.",
      E("s", "7000 + 70")),
    B("35 times 2 is 70. And 35 times 200 is 7000.",
      E("a", "35 × 2"), E("b", "35 × 200")),
    B("So the 7000 gives each student 200 rupees, and the 70 gives each student 2 rupees more. What is the share?",
      ask=CH(["22", "220", "202"], 2,
             "200 and 2 are added together: 2 hundreds, no tens, and 2 ones. The zero in the tens place has to be written.")),
    B("200 plus 2 is 202. Each student pays 202 rupees.",
      A("c", "200 + 2")),
    B("That zero in the middle is the trap. Leave it out and 202 turns into 22, which is far too small for a 7070 rupee trip."),
    B("Check by multiplying back. 202 times 35 is 7070.",
      E("k", "202 × 35")),
    B("So split the total into pieces that divide easily, divide each piece, and keep every zero in its place."),
)

# Divisor 32 instead of 23; answer 1380.
LESSONS[T + "q015"] = LESSON(
    B("A student divided by 32 when he should have divided by 23. His answer came out as 1380. The number he was dividing never changed, so let's find it first.",
      G("q", "Divided by 32 instead of 23, and got 1380")),
    B("How do we get back the number he divided?",
      ask=CH(["23 × 1380", "32 × 1380", "1380 ÷ 32"], 1,
             "He really did divide by 32, so 32 is the number that undoes his work. Multiply his answer by the divisor he used.")),
    split_times(1380, 32, 30, "+", 2, "m",
                "So we want 1380 times 32. Split 32 into 30 and 2.",
                mid="1380 times 30 is 41,400. And 1380 times 2 is 2760.",
                end="41,400 plus 2760 is 44,160. That is the number he was dividing."),
    B("Now divide 44,160 by the right number, 23. Try 2000 lots: 23 times 2000 is 46,000. That overshoots by 1840.",
      E("d1", "23 × 2000"), E("d2", "46,000 − 44,160")),
    B("And 1840 is 23 times 80. So we take 80 lots back off: 2000 minus 80 is 1920.",
      E("d3", "23 × 80"), A("d", "2000 − 80")),
    B("Notice the right answer is bigger than 1380. Dividing by a smaller number always gives a bigger answer, so anything below 1380 could not be right."),
    B("Check by multiplying back. 1920 times 23 is 44,160, the number we found.",
      E("k", "1920 × 23")),
    B("So undo the slip first: multiply his answer by the divisor he used. Then divide by the divisor he should have used."),
)

# 3695 ÷ ? = 230 remainder 15.
LESSONS[T + "q018"] = LESSON(
    B("3695 is divided by a mystery number. The quotient is 230 and the remainder is 15. We have to find the mystery number, the divisor.",
      G("q", "3695 ÷ ? = 230, remainder 15"), CIRC("q", "?")),
    B("Every division obeys one rule. Let's write it, and then put in what we know.",
      LB("f", "Number = divisor × quotient + remainder"), W("l1", "3695 = ? × 230 + 15")),
    B("What should we do with the remainder, 15, first?",
      ask=CH(["add it to 3695", "take it away from 3695", "divide it by 230"], 1,
             "The 15 is the bit left over after the equal groups were made. Take it away, and what remains is made of full groups only.")),
    B("3695 minus 15 is 3680. So the mystery number times 230 is exactly 3680.",
      STRIKE("l1", "+ 15", "− 15"), E("l2", "3695 − 15"), W("l3", "? × 230 = 3680")),
    B("How many lots of 230 make 3680? 10 lots make 2300, and that leaves 1380.",
      E("d1", "230 × 10"), E("d2", "3680 − 2300")),
    B("1380 is 6 more lots of 230. So that is 10 lots and 6 lots: the divisor is 16.",
      E("d3", "230 × 6"), A("d", "10 + 6")),
    B("Here is a handy test. A remainder must always be smaller than the divisor. 15 is smaller than 16, so 16 passes.",
      W("t", "15 < 16")),
    B("Check: 16 times 230, plus 15, is 3695.",
      E("k", "16 × 230 + 15")),
    B("So to find a missing divisor: take the remainder off the number, then divide by the quotient."),
)
