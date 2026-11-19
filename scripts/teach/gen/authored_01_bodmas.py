"""BODMAS and order of operations, G5A_BODMAS_001 to 010: one lesson each, written by hand."""
from authored_01_lib import (ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LANS, LB, LESSON, NOTE, STRIKE, UL, W)  # noqa: F401

LESSONS = {}
P = "G5A_BODMAS_"

# 72 ÷ 6 + 3 × 4 − 2 = 22; brackets round (6 + 3) make it 30
LESSONS[P + "001"] = LESSON(
    B("72 divided by 6, plus 3 times 4, minus 2, comes to 22. We may put in one pair of brackets, and we want the value to become 30. Where do the brackets go?",
      W("q", "72 ÷ 6 + 3 × 4 − 2 = 22", "given")),
    B("Why 22? Division and multiplication come first: 72 divided by 6 is 12, and 3 times 4 is 12. Then 12 plus 12 minus 2 is 22.",
      W("l1", "12 + 12 − 2 = 22")),
    B("Brackets only help if they change what is done first. Which brackets would change nothing at all?",
      ask=CHOOSE(["(3 × 4)", "(6 + 3)", "(4 − 2)"], 0,
                 "3 times 4 is already done before the adding and subtracting. Brackets round it only tell us to do what we were doing anyway.")),
    B("So try brackets round 6 plus 3. Brackets first: 6 plus 3 is 9. Now we have 72 divided by 9, times 4, minus 2.",
      W("l2", "72 ÷ (6 + 3) × 4 − 2 = 72 ÷ 9 × 4 − 2"), UL("l2", "(6 + 3)")),
    B("Division and multiplication go from left to right. 72 divided by 9 is 8. Then 8 times 4 is 32.",
      W("l3", "72 ÷ 9 = 8"), W("l4", "8 × 4 = 32")),
    B("And 32 minus 2 is 30. That is the value we wanted. So the brackets go round 6 plus 3.",
      W("l5", "32 − 2 = 30"), ANS("a", "72 ÷ (6 + 3) × 4 − 2 = 30"), CIRC("a", "(6 + 3)")),
    B("Now the tempting one: brackets round 4 minus 2. Working from left to right it seems to give 30. But multiplication comes before addition: 3 times 2 is 6, and 12 plus 6 is only 18.",
      W("t1", "72 ÷ 6 + 3 × (4 − 2) = 18")),
    B("So to test a pair of brackets, do the bracket first, and then keep to the usual order for everything else."),
)

# 8 □ 2 □ 5 □ 3 with +, −, × once each: greatest value 21
LESSONS[P + "002"] = LESSON(
    B("The signs plus, minus and times go into the three boxes between 8, 2, 5 and 3, each sign used once. What is the greatest value the expression can have?",
      GIVEN("q", "8 □ 2 □ 5 □ 3, using +, − and × once each. Greatest value?")),
    B("The times sign is done first, wherever it sits. So let's try it in each box in turn. Each time, we pick the better places for plus and minus."),
    B("Times in the first box: 8 times 2 is 16. Then it is better to add the 5 and take away the 3. That gives 18.",
      W("l1", "8 × 2 = 16"), W("l2", "8 × 2 + 5 − 3 = 18")),
    B("Times in the middle box: 2 times 5 is 10. Add it to 8, and take away 3. That gives 15.",
      W("l3", "8 + 2 × 5 − 3 = 15")),
    B("Times in the last box: 5 times 3 is 15. Now plus and minus go in the first two boxes. Which way round is better?",
      LB("l4", "8 □ 2 □ 5 × 3"),
      ask=CHOOSE(["8 − 2 + 5 × 3", "8 + 2 − 5 × 3"], 0,
                 "Whatever follows the minus sign is taken away. In one choice that is just the small 2. In the other it is the whole of 5 times 3, which is 15.")),
    B("Take away only the small 2, and add the big 15. 8 minus 2, plus 15, is 21.",
      W("l5", "5 × 3 = 15"), ANS("l6", "8 − 2 + 5 × 3 = 21"), CIRC("l6", "21")),
    B("Compare 18, 15 and 21. The greatest value is 21.",
      UL("l2", "18"), UL("l3", "15", 1)),
    B("The surprise is that the times sign is not best next to the big 8. Between 5 and 3 it makes 15, and it lets us take away just the 2."),
    B("And always do the times first. Working 8 plus 2 times 5 from left to right gives a value that is far too big to be real."),
    B("So when you place signs, try the strongest sign in every position, and choose carefully what gets taken away. Here the best is 21."),
)

# 72 ÷ 6 × 3 − [15 − {9 − (7 − 2 × 2)}] = 27
LESSONS[P + "003"] = LESSON(
    B("Here is a long one, with three kinds of brackets nested inside each other. We start from the innermost bracket and work outwards.",
      W("q", "72 ÷ 6 × 3 − [15 − {9 − (7 − 2 × 2)}]", "given")),
    B("The innermost is the round bracket: 7 minus 2 times 2.",
      UL("q", "(7 − 2 × 2)")),
    B("Inside it, what do we do first?",
      ask=CHOOSE(["7 − 2", "2 × 2"], 1,
                 "Inside a bracket the usual order still applies. Multiplication comes before subtraction, so 2 times 2 goes first.")),
    B("2 times 2 is 4, and 7 minus 4 is 3. The trap is doing 7 minus 2 first, just because it is written first.",
      W("l1", "7 − 2 × 2 = 3"), NOTE("q", "(7 − 2 × 2)", "3")),
    B("Next the curly bracket: 9 minus 3 is 6.",
      W("l2", "9 − 3 = 6")),
    B("Then the square bracket: 15 minus 6 is 9.",
      W("l3", "15 − 6 = 9")),
    B("Now the front part. Division and multiplication go from left to right: 72 divided by 6 is 12, and 12 times 3 is 36.",
      W("l4", "72 ÷ 6 = 12"), W("l5", "12 × 3 = 36")),
    B("Last, take the whole square bracket away. 36 minus 9 is 27.",
      *ANSC("l6", "36 − 9 = 27", 27)),
    B("So with nested brackets: innermost first, then outwards. And inside every bracket, keep to the usual order."),
)

# 24 ÷ □ + 6 × □ − □ with digits 2, 3, 4: greatest value 33
LESSONS[P + "004"] = LESSON(
    B("The digits 2, 3 and 4 go into the three boxes, once each: 24 divided by a box, plus 6 times a box, minus a box. What is the greatest value we can make?",
      GIVEN("q", "24 ÷ □ + 6 × □ − □, digits 2, 3, 4 once each. Greatest?")),
    B("Each box does a different job. One divides 24, one multiplies 6, and one is taken away. Ask which job gains the most from a big digit."),
    B("Which box should get the largest digit, 4?",
      ask=CHOOSE(["the one dividing 24", "the one multiplying 6", "the one taken away"], 1,
                 "Dividing by a big digit makes that part smaller, and taking away a big digit loses more. Only the multiplying box grows with a bigger digit.")),
    B("The 4 multiplies the 6, giving 24. Each extra 1 in that box is worth 6 more.",
      W("l1", "6 × 4 = 24")),
    B("Now 2 and 3 are left, for dividing and for taking away. First way: divide by 2, take away 3. 24 divided by 2 is 12. Then 12 plus 24 minus 3 is 33.",
      W("l2", "24 ÷ 2 = 12"), W("l3", "12 + 24 − 3 = 33")),
    B("Second way: divide by 3, take away 2. 24 divided by 3 is 8. Then 8 plus 24 minus 2 is 30.",
      W("l4", "24 ÷ 3 = 8"), W("l5", "8 + 24 − 2 = 30")),
    B("33 beats 30. Here is the trap: taking away the smallest digit feels right. But dividing by 2 and not by 3 gains 4, while taking away 3 and not 2 loses only 1.",
      W("l6", "12 − 8 = 4")),
    B("So the greatest value is 33.",
      ANS("a", "24 ÷ 2 + 6 × 4 − 3 = 33"), CIRC("a", "33")),
    B("When each box has a different job, ask how much each job changes with a bigger digit. Then test the close calls."),
)

# 6 + 4 × (□ − 3) ÷ 2 = 20: the box is 10
LESSONS[P + "005"] = LESSON(
    B("Which number goes in the box? 6, plus 4 times the bracket, divided by 2, equals 20. Inside the bracket is the box minus 3.",
      GIVEN("q", "6 + 4 × (□ − 3) ÷ 2 = 20")),
    B("We'll work backwards. Think about the order the left side is worked out in: the bracket, then times 4 and divide by 2, and the 6 is added last of all."),
    B("To work backwards, which do we undo first?",
      ask=CHOOSE(["the + 6", "the × 4", "the − 3"], 0,
                 "Working backwards is like taking off shoes and socks: the last thing put on comes off first. The 6 is added last, so it is undone first.")),
    B("Undo the plus 6: 20 minus 6 is 14. So the middle part, 4 times the bracket divided by 2, equals 14.",
      STRIKE("q", "6 +", "− 6"), W("l1", "20 − 6 = 14"), LB("l2", "4 × (□ − 3) ÷ 2 = 14")),
    B("Undo the divide by 2: 14 times 2 is 28. So 4 times the bracket is 28.",
      W("l3", "14 × 2 = 28"), LB("l4", "4 × (□ − 3) = 28")),
    B("Undo the times 4: 28 divided by 4 is 7. So the bracket equals 7.",
      W("l5", "28 ÷ 4 = 7"), LB("l6", "□ − 3 = 7")),
    B("Careful with the last step. The box minus 3 is 7, so we add the 3 back. 7 plus 3 is 10.",
      *ANSC("l7", "7 + 3 = 10", 10)),
    B("Check: 10 minus 3 is 7. 4 times 7 is 28, and divided by 2 that is 14. And 6 plus 14 is 20.",
      W("c1", "6 + 4 × (10 − 3) ÷ 2 = 20")),
    B("The trap at the start is adding 6 and 4 first. The 4 belongs to the multiplication, so the 6 waits till last. And working backwards, the last operation is undone first."),
)

# Exactly one true statement: 30 − 12 ÷ 2 × 3 = 12
LESSONS[P + "006"] = LESSON(
    B("Four statements, and exactly one of them is true. We'll work out the left side of each with the correct order, and compare it with the number after the equals sign.",
      GIVEN("q", "Exactly one of the four statements is true. Which one?")),
    B("Take this one: 18 minus 6 divided by 3, plus 3. Is it 7? What do we do first?",
      LB("s2", "18 − 6 ÷ 3 + 3 = 7 ?"),
      ask=CHOOSE(["18 − 6", "6 ÷ 3", "3 + 3"], 1,
                 "Division comes before adding and subtracting, wherever it sits. So 6 divided by 3 goes first.")),
    B("6 divided by 3 is 2. Then 18 minus 2 plus 3 is 19, not 7. You only get 7 by doing 18 minus 6 first. So this one is out.",
      W("l2", "18 − 6 ÷ 3 + 3 = 19"), STRIKE("s2", "= 7")),
    B("Next: 4 plus 6 times 5, minus 20. Is it 30? Multiply first: 6 times 5 is 30. Then 4 plus 30 minus 20 is 14. Out.",
      LB("s3", "4 + 6 × 5 − 20 = 30 ?"), W("l3", "4 + 6 × 5 − 20 = 14"), STRIKE("s3", "= 30")),
    B("Next: 2 times 9, minus 3 times 2. Is it 30? Both multiplications go first: 18 minus 6 is 12. Out.",
      LB("s4", "2 × 9 − 3 × 2 = 30 ?"), W("l4", "2 × 9 − 3 × 2 = 12"), STRIKE("s4", "= 30")),
    B("Last: 30 minus 12 divided by 2, times 3. Is it 12? Division and multiplication go from left to right: 12 divided by 2 is 6, and 6 times 3 is 18.",
      LB("s1", "30 − 12 ÷ 2 × 3 = 12 ?"), W("l5", "12 ÷ 2 × 3 = 18")),
    B("Then 30 minus 18 is 12. It matches! This is the true statement.",
      ANS("a", "30 − 12 ÷ 2 × 3 = 12"), CIRC("a", "30 − 12 ÷ 2 × 3 = 12")),
    B("See the pattern in the three that fell? Each one only works if you go straight from left to right. That is the trap."),
    B("So find the divide and times parts first, do those, and only then add and subtract."),
)

# Brackets round the last two numbers: the value changes for 20 − 6 + 4
LESSONS[P + "007"] = LESSON(
    B("Meena says that putting brackets round the last two numbers of an expression never changes its value. For which of the four expressions does the value change?",
      GIVEN("q", "Brackets round the last two numbers: which value changes?")),
    B("We work out each one twice: as written, and with brackets round the last two numbers. Start with 20 plus 6 minus 4. Both ways give 22. No change.",
      W("l1", "20 + 6 − 4 = 22"), W("l2", "20 + (6 − 4) = 22")),
    B("20 times 6 divided by 3: as written it comes to 40. With brackets it is 20 times 2, which is also 40. No change.",
      W("l3", "20 × 6 ÷ 3 = 40"), W("l4", "20 × (6 ÷ 3) = 40")),
    B("20 plus 6 times 4: the multiplication is done first anyway, so the brackets add nothing. Both ways give 44.",
      W("l5", "20 + 6 × 4 = 44"), W("l6", "20 + (6 × 4) = 44")),
    B("Now 20 minus 6 plus 4. As written, we go from left to right and get 18. With brackets round 6 plus 4, how much is taken away from 20?",
      W("l7", "20 − 6 + 4 = 18"),
      ask=CHOOSE(["6", "10", "2"], 1,
                 "The brackets are done first, and 6 plus 4 is 10. So now the whole 10 is taken away, not just the 6.")),
    B("With brackets, the whole of 6 plus 4 is taken away. 20 minus 10 is 10. The value has changed, from 18 to 10.",
      W("l8", "20 − (6 + 4) = 10")),
    B("So the value changes for 20 minus 6 plus 4.",
      LANS("a", "20 − 6 + 4 changes: 18 becomes 10"), CIRC("a", "20 − 6 + 4")),
    B("Why this one? A minus sign in front of a bracket takes away everything inside it. Without the brackets the 4 was being added. With them, it is taken away."),
    B("So watch for a minus sign just before a bracket. That is where brackets change the value."),
)

# Kabir: 40 − 8 × □ + 6 left to right gives 134 -> box 4 -> correct value 14
LESSONS[P + "008"] = LESSON(
    B("Kabir worked out 40 minus 8 times a box, plus 6, from left to right, and got 134. What is the correct value of the expression, with the same number in the box?",
      GIVEN("q", "40 − 8 × □ + 6. Left to right, Kabir got 134. Correct value?")),
    B("Two jobs here. First find the number in the box, by following Kabir's working backwards. Then work the expression out properly."),
    B("Kabir went from left to right. So his first step was 40 minus 8, which is 32. Then he multiplied 32 by the box, and added 6 to reach 134.",
      W("l1", "40 − 8 = 32"), LB("l2", "Kabir: 32 × □ + 6 = 134")),
    B("Undo his plus 6: 134 minus 6 is 128. So 32 times the box is 128.",
      W("l3", "134 − 6 = 128")),
    B("Undo the times 32: 128 divided by 32 is 4. The number in the box is 4.",
      W("l4", "128 ÷ 32 = 4"), LB("l5", "□ = 4")),
    B("So, is 4 our answer?",
      ask=CHOOSE(["Yes, 4", "No, now work it out properly"], 1,
                 "4 is only the number in the box. The question asks for the correct value of the whole expression, so there is one more job to do.")),
    B("Now the correct order, with 4 in the box. Multiply first: 8 times 4 is 32.",
      W("l6", "40 − 8 × 4 + 6"), UL("l6", "8 × 4"), W("l7", "8 × 4 = 32")),
    B("Then subtract and add, from left to right. 40 minus 32 is 8, and 8 plus 6 is 14. The correct value is 14.",
      *ANSC("l8", "40 − 32 + 6 = 14", 14)),
    B("One more place to slip: after 40 minus 32, the 6 is added, not taken away. Only the 32 has a minus sign in front of it."),
    B("So when someone has used a different order, follow their steps backwards to find the missing number. Then start again with the correct order."),
)

# Greatest of four expressions in 999 and 12: 999 × 12 + 12 ÷ 12
LESSONS[P + "009"] = LESSON(
    B("Four expressions are built from 999 and 12. Which has the greatest value? We'll reason it out, without ever multiplying 999 by 12.",
      GIVEN("q", "Which is greatest? Decide without multiplying 999 by 12")),
    B("Start with 999 times the bracket 12 minus 12, plus 12. The bracket is 0, and 999 times 0 is 0. So this one is only 12.",
      W("l1", "999 × (12 − 12) + 12 = 12")),
    B("Next: 999 plus 12 in a bracket, times 12, divided by 12. Multiplying by 12 and then dividing by 12 brings us straight back. So it is just 999 plus 12, which is 1011.",
      W("l2", "(999 + 12) × 12 ÷ 12 = 1011")),
    B("The other two both start with 999 times 12. That is far more than 1011, so the winner is one of these two.",
      W("l3", "999 × 12 − 12"), W("l4", "999 × 12 + 12 ÷ 12")),
    B("The first of them, 999 times 12, minus 12, is 12 less than 999 times 12.",
      NOTE("l3", "− 12", "12 less")),
    B("In the second one, 999 times 12, plus 12 divided by 12, what is added to 999 times 12?",
      ask=CHOOSE(["12", "1", "nothing"], 1,
                 "Division is done before addition. So 12 divided by 12 is worked out first, and that is 1. Then the 1 is added.")),
    B("The division comes before the addition, and 12 divided by 12 is 1. So this one is 1 more than 999 times 12.",
      W("l5", "12 ÷ 12 = 1"), NOTE("l4", "+ 12 ÷ 12", "1 more")),
    B("1 more beats 12 less. So the greatest is 999 times 12, plus 12 divided by 12.",
      LANS("a", "Greatest: 999 × 12 + 12 ÷ 12"), CIRC("a", "999 × 12 + 12 ÷ 12")),
    B("The trap would be working that one from left to right, adding 12 and then dividing everything by 12. The order of operations is what makes it the biggest."),
    B("So you can compare big expressions without big sums. Look at what each one does to the part they share."),
)

# 24 □ 8 □ 2 □ 5 = 25: 24 − 8 ÷ 2 + 5, so × is not used
LESSONS[P + "010"] = LESSON(
    B("24, 8, 2 and 5 have a box between each pair, and the answer is 25. Each box holds plus, minus, times or divide, and no sign is used twice. Which sign is not used?",
      GIVEN("q", "24 □ 8 □ 2 □ 5 = 25, no sign used twice")),
    B("Look at the target. 25 is just 1 more than 24. So the 8, the 2 and the 5 must together add exactly 1.",
      W("l1", "25 − 24 = 1")),
    B("Suppose the 5 is added. Then the 8 and the 2 must take away 4, because 5 minus 4 is 1. How can 8 and 2 make 4?",
      W("l2", "5 − 4 = 1"),
      ask=CHOOSE(["8 − 2", "8 ÷ 2", "8 × 2"], 1,
                 "8 minus 2 is 6, and 8 times 2 is much too big. Only 8 divided by 2 gives 4.")),
    B("8 divided by 2 is 4. So try this: 24, minus 8 divided by 2, plus 5.",
      W("l3", "8 ÷ 2 = 4"), W("l4", "24 − 8 ÷ 2 + 5")),
    B("Division first: 8 divided by 2 is 4. Then 24 minus 4, plus 5, is 25. It works!",
      W("l5", "24 − 4 + 5 = 25")),
    B("The signs we used are minus, divide and plus. The one left out is the multiplication sign.",
      LANS("a", "Not used: the multiplication sign ×"), CIRC("a", "×")),
    B("There is a tempting other try: 24 divided by 8, plus 2 times 5. From left to right it seems to reach 25. But with the correct order it is 3 plus 10, which is 13.",
      W("t1", "24 ÷ 8 + 2 × 5 = 13")),
    B("So start from the target, see how far it is from the first number, and always test your idea with the correct order."),
)
