"""Batch 11, part B: addition and subtraction questions, each written by hand."""
from imported_11_lib import (ANS, ANSL, B, BOX, CHOOSE, CIRC, FIG, GIVEN, GIVENM, GROUP, LB, LESSON, NOTE,  # noqa: F401
                             STRIKE, TRI, UL, W)

T5 = "IPMTB_grade5_ch05_"

LESSONS = {}

# ── Numbers given in words ───────────────────────────────────────────────────

# Twenty five crore, seven hundred fifty six + sixty one lakh, twelve thousand, fifty four.
LESSONS[T5 + "q003"] = LESSON(
    B("Two numbers are given in words, and we must add them. The hard part is not the adding. It is writing each number with every digit in its right place.",
      GIVEN("q", "25 crore 756  +  61 lakh 12 thousand 54")),
    B("Take the first one: 25 crore, 756. After crores come lakhs, then thousands, then the last three digits. This number has no lakhs and no thousands. How is it written?",
      ask=CHOOSE(["25,756", "25,00,00,756", "25,00,756"], 1,
                 "The lakhs and the thousands are empty, but their places still have to be there. So two zeros go in for the lakhs and two more for the thousands.")),
    B("So the first number is 25, then two zeros for the lakhs, two zeros for the thousands, then 756.",
      W("l1", "25,00,00,756"), UL("l1", "00,00"), NOTE("l1", "00,00", "empty places")),
    B("The second is 61 lakh, 12 thousand, 54. Careful with the 54: it has no hundreds, so the last group is written 0, 5, 4.",
      W("l2", "61,12,054"), BOX("l2", "054")),
    B("Line them up by place, ones under ones, and add from the right.",
      W("l3", "25,00,00,756 + 61,12,054 = ?")),
    B("Ones: 6 plus 4 is 10. Write 0, carry 1. Tens: 5 plus 5, plus the carried 1, is 11. Write 1, carry 1.",
      LB("c1", "Ones: 6 + 4 = 10"), LB("c2", "Tens: 5 + 5 + 1 = 11")),
    B("Hundreds: 7 plus 0, plus the carried 1, is 8. So the last three digits are 810.",
      LB("c3", "Hundreds: 7 + 0 + 1 = 8"), W("l4", "756 + 54 = 810")),
    B("The rest is easy, because the first number has only zeros in its thousands and lakhs. The 12 thousand and the 61 lakh drop straight in."),
    B("So the sum is 25 crore, 61 lakh, 12 thousand, 810.",
      ANS("l5", "25,00,00,756 + 61,12,054 = 25,61,12,810"), CIRC("l5", "25,61,12,810")),
    B("The trap here is the commas. In the Indian system only the last group has three digits. Every group before it has two."),
    B("Check by taking the second number away again. We land back on 25 crore, 756.",
      W("l6", "25,61,12,810 − 61,12,054 = 25,00,00,756")),
    B("So write each number in digits, with zeros in the empty places. Line up the places, and then add."),
)

# Subtract twenty five thousand, two hundred seventy six from seven lakh, four hundred eighty one.
LESSONS[T5 + "q004"] = LESSON(
    B("Here is a subtraction given in words. Notice which number is said first: 25 thousand, 276. That is the one being taken away.",
      GIVEN("q", "Subtract 25 thousand 276 from 7 lakh 481")),
    B("Which number goes on top in the subtraction?",
      ask=CHOOSE(["25 thousand 276", "7 lakh 481"], 1,
                 "Subtract this from that means: start with that. So 7 lakh 481 goes on top, and 25 thousand 276 is taken away from it.")),
    B("Write them in digits. 7 lakh 481 has no thousands at all, so zeros hold those places.",
      W("l1", "7,00,481 − 25,276 = ?"), UL("l1", "00"), NOTE("l1", "00", "no thousands")),
    B("Ones: 1 minus 6 cannot be done. Borrow from the 8 tens, which leaves 7 tens. Now 11 minus 6 is 5.",
      LB("c1", "Ones: 11 − 6 = 5"), BOX("c1", "11")),
    B("Tens: 7 minus 7 is 0. Hundreds: 4 minus 2 is 2.",
      LB("c2", "Tens: 7 − 7 = 0"), LB("c3", "Hundreds: 4 − 2 = 2")),
    B("Thousands: 0 minus 5. We need to borrow, but the ten-thousands place is 0 as well. So we go all the way to the 7 lakhs."),
    B("The 7 lakhs become 6. That lakh turns into 10 ten-thousands. One of those moves along, leaving 9, and the thousands place gets 10.",
      LB("c4", "7 lakhs → 6 lakhs, 9 ten-thousands, 10 thousands")),
    B("Now the thousands: 10 minus 5 is 5. Ten-thousands: 9 minus 2 is 7. And the 6 lakhs have nothing to lose.",
      LB("c5", "Thousands: 10 − 5 = 5"), LB("c6", "Ten-thousands: 9 − 2 = 7"), LB("c7", "Lakhs: 6 − 0 = 6")),
    B("Read it from the top place: 6 lakh, 75 thousand, 205.",
      ANS("l2", "7,00,481 − 25,276 = 6,75,205"), CIRC("l2", "6,75,205"), NOTE("l2", "6,75,205", "6 lakh 75 thousand 205")),
    B("Borrowing across zeros is where most slips happen. A zero that passes the borrow along becomes 9, not 10, because it hands 1 on to its neighbour."),
    B("Check by adding back. The answer plus 25 thousand 276 should rebuild 7 lakh 481, and it does.",
      W("l3", "6,75,205 + 25,276 = 7,00,481")),
    B("So write both numbers in digits, put the one you start with on top, and take extra care where zeros have to lend."),
)

# ── Greatest and smallest numbers ────────────────────────────────────────────

# Smallest 5-digit number minus greatest 4-digit number.
LESSONS[T5 + "q005"] = LESSON(
    B("No numbers are given here, only descriptions. We have to find the greatest 4 digit number and the smallest 5 digit number ourselves, and then subtract.",
      GIVEN("q", "smallest 5-digit number − greatest 4-digit number")),
    B("What is the greatest number you can write with 4 digits?",
      ask=CHOOSE(["9000", "9999", "1000"], 1,
                 "To make a number as big as possible, make every digit as big as possible. The biggest digit is 9, so we use a 9 in all four places.")),
    B("So the greatest 4 digit number is 9999. Every place is full.",
      LB("l1", "greatest 4-digit number = 9999"), UL("l1", "9999")),
    B("Now the smallest 5 digit number. It has to start with 1, because a number cannot start with 0. After that, every digit is as small as it can be.",
      LB("l2", "smallest 5-digit number = 10,000"), UL("l2", "10,000")),
    B("Before subtracting, look at the two numbers. When we count, 10,000 comes straight after 9999. They are next door neighbours.",
      W("l3", "9999 + 1 = 10,000")),
    B("So the difference between them is just 1.",
      ANS("l4", "10,000 − 9999 = 1"), CIRC("l4", "1", 2)),
    B("Don't be fooled by how different they look. One is all 9s and the other is nearly all 0s, yet they are only 1 apart."),
    B("So remember: the greatest number with some digits is all 9s, and the smallest number with one more digit is just 1 more than it."),
)

# Greatest 4-digit number plus smallest 5-digit number.
LESSONS[T5 + "q026"] = LESSON(
    B("This question describes two numbers without telling us what they are. So first we work out each one, and then we add.",
      GIVEN("q", "greatest 4-digit number + smallest 5-digit number")),
    B("The greatest 4 digit number has the biggest digit, 9, in every place.",
      LB("l1", "greatest 4-digit number = 9,999"), UL("l1", "9,999")),
    B("And what is the smallest number with 5 digits?",
      ask=CHOOSE(["10,000", "11,111", "99,999"], 0,
                 "The smallest 5 digit number has a 1 in front, because a number cannot start with 0. Then the smallest digit, 0, goes in every other place.")),
    B("So it is 10,000: a 1 and four 0s.",
      LB("l2", "smallest 5-digit number = 10,000"), UL("l2", "10,000")),
    B("Now add them. Adding 10,000 only changes the ten-thousands place. The four 9s stay just as they are.",
      W("l3", "9,999 + 10,000 = ?")),
    B("So we get a 1 in front of the four 9s: 19,999.",
      ANS("l4", "9,999 + 10,000 = 19,999"), CIRC("l4", "19,999")),
    B("Read the question word slowly. A question just like this one says subtract, and then the answer is 1. This one says add."),
    B("Check by taking away. 19,999 minus 10,000 is 9,999. Good.",
      W("l5", "19,999 − 10,000 = 9,999")),
    B("So turn each description into a number first: all 9s for the greatest, a 1 and then 0s for the smallest. Then do what the question asks."),
)

# ── Perimeters ───────────────────────────────────────────────────────────────

LESSONS[T5 + "q006"] = LESSON(
    B("A triangular ground has sides of 225 metres, 362 metres and 289 metres. We want its perimeter.",
      GIVEN("q", "Triangle with sides 225 m, 362 m, 289 m"), FIG("f1", TRI("scalene", "225 m", "362 m", "289 m"))),
    B("What does perimeter mean?",
      ask=CHOOSE(["the space inside", "the distance all the way round", "the longest side"], 1,
                 "Imagine walking along the edge of the ground until you are back where you started. The distance you walk is the perimeter, so we add all three sides.")),
    B("So the perimeter is the three sides added together.",
      LB("l1", "Perimeter = side + side + side"), W("l2", "225 + 362 + 289 = ?")),
    B("Add the ones first. 5 plus 2 plus 9 is 16. Write the 6 and carry the 1.",
      LB("c1", "Ones: 5 + 2 + 9 = 16"), BOX("c1", "16")),
    B("Tens next, and don't forget the carried 1. 2 plus 6 plus 8, plus 1, is 17. Write 7, carry 1.",
      LB("c2", "Tens: 2 + 6 + 8 + 1 = 17"), BOX("c2", "17")),
    B("Hundreds: 2 plus 3 plus 2, plus the carried 1, is 8.",
      LB("c3", "Hundreds: 2 + 3 + 2 + 1 = 8")),
    B("So the perimeter is 876 metres.",
      ANS("l3", "225 + 362 + 289 = 876"), CIRC("l3", "876")),
    B("The carried 1 is the one that gets lost. Forget it in the tens and your answer comes out 10 short. Write each carry small, above the next column."),
    B("Check by adding in a different order. 362 plus 289 is 651, and 651 plus 225 is 876.",
      W("l4", "362 + 289 = 651"), W("l5", "651 + 225 = 876")),
    B("So perimeter means all the way round: add every side, and watch the carries."),
)

LESSONS[T5 + "q032"] = LESSON(
    B("An equilateral triangle has sides of 223 metres. We want its perimeter, the distance all the way round.",
      GIVEN("q", "Equilateral triangle, side 223 m. Perimeter = ?"), FIG("f1", TRI("equilateral", "223 m", "223 m", "223 m"))),
    B("The question gives only one length. What do we know about the other two sides?",
      ask=CHOOSE(["We cannot tell", "They are shorter", "They are 223 metres too"], 2,
                 "Equilateral means equal sides. All three sides of this triangle are the same length, 223 metres each.")),
    B("So the perimeter is 223, three times over. Adding the same number 3 times is the same as multiplying by 3.",
      W("l1", "223 + 223 + 223 = 3 × 223"), UL("l1", "3 × 223")),
    B("Multiply place by place. 3 times 3 ones is 9. 3 times 2 tens is 6 tens. 3 times 2 hundreds is 6 hundreds.",
      W("l2", "3 × 3 = 9"), W("l3", "3 × 20 = 60"), W("l4", "3 × 200 = 600")),
    B("6 hundreds, 6 tens and 9 ones make 669. The perimeter is 669 metres.",
      ANS("l5", "3 × 223 = 669"), CIRC("l5", "669")),
    B("Check by adding instead. 223 plus 223 is 446, and 446 plus 223 is 669.",
      W("l6", "223 + 223 = 446"), W("l7", "446 + 223 = 669")),
    B("Notice that 446 is among the choices. That is only two sides. And 223 alone is just one. A triangle has three.",
      BOX("l6", "446")),
    B("So for a shape whose sides are all equal, the perimeter is one side times the number of sides."),
)

LESSONS[T5 + "q037"] = LESSON(
    B("A triangular ground has sides of 230 metres, 402 metres and 270 metres. Perimeter means the distance all the way round, so we add the three sides.",
      GIVEN("q", "Triangle with sides 230 m, 402 m, 270 m"), FIG("f1", TRI("scalene", "230 m", "402 m", "270 m")),
      W("l1", "230 + 402 + 270 = ?")),
    B("We may add in any order we like. Which two of these make a nice round number together?",
      ask=CHOOSE(["230 and 402", "402 and 270", "230 and 270"], 2,
                 "Look for endings that fit together. 230 has 3 tens and 270 has 7 tens, and 3 tens plus 7 tens make a whole hundred.")),
    B("230 plus 270 is exactly 500.",
      GROUP("l1", ["230", "270"], "500"), W("l2", "230 + 270 = 500")),
    B("Now add the third side. 500 plus 402 is 902. The perimeter is 902 metres.",
      W("l3", "500 + 402 = 902"), UL("l3", "902")),
    B("Now look at the choices. 902 is not there. Two of them are close to it, but close is not the same."),
    B("So we check before we decide. Add in the order given: 230 plus 402 is 632, and 632 plus 270 is 902 again.",
      W("l4", "230 + 402 = 632"), W("l5", "632 + 270 = 902")),
    B("Our working is sound, and 902 is not listed. So the answer is, none of these.",
      ANSL("l6", "Perimeter = 902 m → None of these"), CIRC("l6", "None of these")),
    B("So add all the sides, check the sum a second way, and only then pick none of these. When your checked number is not listed, trust your working."),
)

# ── A missing digit ──────────────────────────────────────────────────────────

LESSONS[T5 + "q008"] = LESSON(
    B("A digit has gone missing from the first number. It starts with 7, then the hidden digit, then 3 and 5. When 5467 is taken away from it, 2268 is left.",
      GIVEN("q", "7□35 − 5467 = 2268"), BOX("q", "□")),
    B("We cannot subtract from a number with a hole in it. So how can we find the whole number?",
      ask=CHOOSE(["2268 + 5467", "5467 − 2268", "2268 − 5467"], 0,
                 "Adding undoes taking away. If taking 5467 away left 2268, then putting 5467 back on to 2268 gives the number we started with.")),
    B("So we add 2268 and 5467, column by column.",
      W("l1", "2268 + 5467 = ?")),
    B("Ones: 8 plus 7 is 15. Write 5, carry 1. Tens: 6 plus 6, plus the carried 1, is 13. Write 3, carry 1.",
      LB("c1", "Ones: 8 + 7 = 15"), LB("c2", "Tens: 6 + 6 + 1 = 13")),
    B("Hundreds: 2 plus 4 is 6, and the carried 1 makes 7. Thousands: 2 plus 5 is 7.",
      LB("c3", "Hundreds: 2 + 4 + 1 = 7"), LB("c4", "Thousands: 2 + 5 = 7")),
    B("So the starting number is 7735.",
      W("l2", "2268 + 5467 = 7735"), UL("l2", "7735")),
    B("Lay 7735 beside the number with the hole. The 7 in front, the 3 and the 5 all match. The hidden digit sits in the hundreds place, and it is 7.",
      ANSL("l3", "7□35 = 7735, so □ = 7"), CIRC("l3", "□ = 7")),
    B("Careful: the answer is not the whole number. The question asks only for the digit behind the star."),
    B("Check with the real subtraction. 7735 minus 5467 is 2268. It works.",
      W("l4", "7735 − 5467 = 2268")),
    B("So for a missing digit in a subtraction, add the result back to the number taken away, then read off the hidden digit."),
)

LESSONS[T5 + "q029"] = LESSON(
    B("A digit is hiding behind the star. The number starts 8, 0, then the hidden digit, then 5. Take 4005 away from it, and 4000 is left.",
      GIVEN("q", "80□5 − 4005 = 4000"), BOX("q", "□")),
    B("How can we find the whole number first?",
      ask=CHOOSE(["4005 − 4000", "4000 + 4005", "4000 − 4005"], 1,
                 "Adding undoes taking away. If 4005 was taken away and 4000 is left, then 4000 plus 4005 brings the starting number back.")),
    B("So we add. 4000 plus 4000 is 8000, and 5 more makes 8005.",
      W("l1", "4000 + 4000 = 8000"), W("l2", "8000 + 5 = 8005")),
    B("So the starting number is 8005.",
      W("l3", "4000 + 4005 = 8005"), UL("l3", "8005")),
    B("Lay 8005 beside the number with the hole. The 8, the first 0 and the 5 all match. So the hidden digit is the other 0, the one in the tens place.",
      ANSL("l4", "80□5 = 8005, so □ = 0"), CIRC("l4", "□ = 0")),
    B("Does it feel odd for the answer to be 0? Zero is a digit like any other. Here it holds the tens place, and without it the number would lose a whole place."),
    B("Check with the real subtraction. 8005 minus 4005 is 4000. It works.",
      W("l5", "8005 − 4005 = 4000")),
    B("So work backwards with addition to find the whole number, then read off the digit that was hidden."),
)

# ── Ages ─────────────────────────────────────────────────────────────────────

# Sujata is 7 years older than Madhuri; in 10 years their ages add up to 67.
LESSONS[T5 + "q011"] = LESSON(
    B("Sujata is 7 years older than Madhuri. In 10 years their ages will add up to 67. We want their ages today.",
      GIVEN("q", "Sujata = Madhuri + 7. Sum after 10 years = 67")),
    B("The 67 belongs to 10 years from now. What is the sum of their ages today?",
      ask=CHOOSE(["67 − 10", "67 − 20", "67 + 20"], 1,
                 "Both of them grow 10 years older, so the sum grows by 10 two times. That is 20 extra years to take off, not 10.")),
    B("2 times 10 is 20, and 67 minus 20 is 47. So today their ages add up to 47.",
      W("l1", "2 × 10 = 20"), W("l2", "67 − 20 = 47")),
    B("Now the other clue: Sujata is 7 years older. Take those 7 extra years away, and what is left is two equal ages, both Madhuri's. 47 minus 7 is 40.",
      UL("q", "Madhuri + 7"), W("l3", "47 − 7 = 40")),
    B("Two equal ages add up to 40, so each one is 40 divided by 2, which is 20. Madhuri is 20.",
      W("l4", "40 ÷ 2 = 20")),
    B("And Sujata is 7 more. 20 plus 7 is 27.",
      W("l5", "20 + 7 = 27")),
    B("So today Sujata is 27 years old and Madhuri is 20.",
      ANSL("l6", "Sujata 27 years, Madhuri 20 years"), BOX("l6", "Sujata 27 years, Madhuri 20 years")),
    B("Careful with the names. One choice has the same two numbers the other way round. Sujata is the older one, so she must be the 27."),
    B("Check with the story. In 10 years Madhuri is 30 and Sujata is 37. And 30 plus 37 is 67.",
      W("l7", "20 + 10 = 30"), W("l8", "27 + 10 = 37"), W("l9", "30 + 37 = 67")),
    B("So go back to today's sum first. Take off the extra years of the older one, and halve what is left."),
)

# 10 years ago Manisha was 19.
LESSONS[T5 + "q015"] = LESSON(
    B("10 years ago, Manisha was 19. We want her age 10 years from now. Notice there are three moments in this story: back then, today, and later.",
      GIVEN("q", "10 years ago: 19 years old. After 10 years: ?")),
    B("Which age must we find first?",
      ask=CHOOSE(["her age today", "her age after 10 years", "her age 20 years ago"], 0,
                 "The story jumps from the past to the future, but today sits in between. Find her age today first, then step forward.")),
    B("From 10 years ago up to today is 10 years. So today she is 19 plus 10, which is 29.",
      W("l1", "19 + 10 = 29"), NOTE("l1", "29", "today")),
    B("Careful: 29 is one of the choices, but that is her age today. The question asks about 10 years later."),
    B("Step forward 10 more years. 29 plus 10 is 39. Manisha will be 39 years old.",
      ANS("l2", "29 + 10 = 39"), CIRC("l2", "39")),
    B("See it on a number line. From 19, one hop of 10 lands on today. A second hop of 10 lands on 39.",
      FIG("f1", {"kind": "numberLine", "min": 19, "max": 39, "step": 10, "tickLabels": "all",
                 "hops": [{"from": 19, "to": 29, "label": "+10"}, {"from": 29, "to": 39, "label": "+10"}]})),
    B("Two hops of 10 make 20 years in all, and 19 plus 20 is 39. The same answer, so we can be sure.",
      W("l3", "19 + 20 = 39")),
    B("So when a story has ago and after in it, find today first. Then count on from today."),
)

# 17 years ago Mahesh was 17.
LESSONS[T5 + "q038"] = LESSON(
    B("17 years ago, Mahesh was 17. We want his age 17 years from now. So many 17s! Let's keep them apart.",
      GIVEN("q", "17 years ago: 17 years old. After 17 years: ?")),
    B("First, his age today. From 17 years ago up to now is 17 years, so today he is 17 plus 17, which is 34.",
      W("l1", "17 + 17 = 34"), NOTE("l1", "34", "today")),
    B("Is 34 our answer?",
      ask=CHOOSE(["Yes, he is 34", "No, go 17 years further"], 1,
                 "34 is his age today, and it is waiting among the choices to catch us. The question asks for his age 17 years after today.")),
    B("So step forward. 34 plus 17 is 51. Mahesh will be 51 years old.",
      W("l2", "34 + 17 = 51"), UL("l2", "51")),
    B("See it on a number line. Start at 17, hop 17 to reach today, and hop 17 again to reach 51.",
      FIG("f1", {"kind": "numberLine", "min": 17, "max": 51, "step": 17, "tickLabels": "all",
                 "hops": [{"from": 17, "to": 34, "label": "+17"}, {"from": 34, "to": 51, "label": "+17"}]})),
    B("Now look at the choices. None of the three numbers is 51. So the right choice is the last one: none of these.",
      ANSL("l3", "51 years → None of these"), CIRC("l3", "None of these")),
    B("Don't let none of these worry you. When your working is checked and your number is not listed, trust your working."),
    B("So when ago and after come together, find today's age first, then count on."),
)

# Sum 12, difference 6.
LESSONS[T5 + "q040"] = LESSON(
    B("Seeta's and Reeta's ages add up to 12, and the difference between them is 6. Two clues, and both must be true at once.",
      GIVEN("q", "Sum of ages = 12, difference = 6")),
    B("The older girl is the younger girl plus 6. If we take those 6 extra years away from the sum, what is left?",
      ask=CHOOSE(["the older girl's age", "two equal ages", "nothing useful"], 1,
                 "Take the extra 6 away from the older girl and she is the same age as the younger one. So what remains of the sum is two equal ages.")),
    B("12 minus 6 is 6. That 6 is two equal ages put together.",
      W("l1", "12 − 6 = 6")),
    B("So the younger age is 6 divided by 2, which is 3.",
      W("l2", "6 ÷ 2 = 3")),
    B("The older age is 6 more. 3 plus 6 is 9.",
      W("l3", "3 + 6 = 9")),
    B("The question does not say which girl is older, so look at the choices. Only one has 9 and 3: Seeta 9 years, Reeta 3 years.",
      ANSL("l4", "Seeta 9 years, Reeta 3 years"), BOX("l4", "Seeta 9 years, Reeta 3 years")),
    B("Here is the trap: testing only one clue. 6 and 6 add up to 12, but their difference is 0. The right pair must pass both tests."),
    B("Our pair does. 9 plus 3 is 12, and 9 minus 3 is 6.",
      W("l5", "9 + 3 = 12"), W("l6", "9 − 3 = 6")),
    B("So with a sum and a difference: take the difference off the sum, halve it for the smaller number, then add the difference back for the bigger."),
)

# ── Sums and differences ─────────────────────────────────────────────────────

LESSONS[T5 + "q014"] = LESSON(
    B("We have two lists: the numbers from 11 to 15, and the numbers from 21 to 25. We want the difference between their sums.",
      GIVEN("q", "11 + 12 + 13 + 14 + 15   and   21 + 22 + 23 + 24 + 25")),
    B("We could add up each list and subtract. But before all that work, compare the lists. Put 11 next to 21, 12 next to 22, and so on."),
    B("How much bigger is each number in the second list than its partner in the first?",
      ask=CHOOSE(["1", "5", "10"], 2,
                 "Look at the pairs. 21 is 10 more than 11. 22 is 10 more than 12. Every number in the second list is exactly 10 bigger than its partner.")),
    B("Every pair differs by 10.",
      W("l1", "21 − 11 = 10"), W("l2", "22 − 12 = 10"), W("l3", "25 − 15 = 10")),
    B("And how many pairs are there? Count from 11 to 15: that is 5 numbers. So the second sum is bigger by 5 lots of 10, which is 50.",
      ANS("l4", "5 × 10 = 50"), CIRC("l4", "50")),
    B("Careful when counting from 11 to 15. It is 5 numbers, not 4, because both ends are included."),
    B("Check the long way. 11 to 15 add up to 65. 21 to 25 add up to 115. And 115 minus 65 is 50.",
      W("l5", "11 + 12 + 13 + 14 + 15 = 65"), W("l6", "21 + 22 + 23 + 24 + 25 = 115"), W("l7", "115 − 65 = 50")),
    B("So before a long sum, look for a pattern. When every number moves up by the same amount, multiply that amount by how many numbers there are."),
)

LESSONS[T5 + "q041"] = LESSON(
    B("This sentence has two sums inside it, and then a difference between them. Brackets help us see the two sums.",
      GIVENM("q", "(22 + 47) − (11 + 22) = ?")),
    B("Which do we work out first?",
      ask=CHOOSE(["the difference", "the two sums"], 1,
                 "The difference is between the two sums, so the sums have to exist first. Work out each bracket, then subtract.")),
    B("First sum: 22 plus 47 is 69.",
      UL("q", "(22 + 47)"), W("l1", "22 + 47 = 69")),
    B("Second sum: 11 plus 22 is 33.",
      UL("q", "(11 + 22)"), W("l2", "11 + 22 = 33")),
    B("Now the difference. 69 minus 33 is 36.",
      ANS("l3", "69 − 33 = 36"), CIRC("l3", "36")),
    B("The words sum and difference sit close together here. Sum means add, difference means subtract. Adding all four numbers is the slip this question is hoping for."),
    B("Here is a neat check. 22 is in both sums, so it cancels out. What is left is 47 minus 11, and that is 36 too.",
      STRIKE("q", "22"), STRIKE("q", "22", None, 2), W("l4", "47 − 11 = 36")),
    B("So read the sentence in pieces: find each sum, then take the smaller from the bigger."),
)

# ── Schools ──────────────────────────────────────────────────────────────────

# 1600 students, 987 boys: how many more boys than girls?
LESSONS[T5 + "q022"] = LESSON(
    B("A school has 1600 students, and 987 of them are boys. The rest are girls. We want to know how many more boys there are than girls.",
      GIVEN("q", "1600 students, 987 boys. Boys − girls = ?")),
    B("What must we find before we can compare?",
      ask=CHOOSE(["the number of girls", "1600 + 987", "nothing, it is 987"], 0,
                 "To say how many more boys there are, we need both numbers. We know the boys. The girls are the rest of the school.")),
    B("The girls are 1600 minus 987. Here is a quick way. 987 is just 13 less than 1000.",
      W("l1", "1600 − 987 = ?"), W("l2", "1000 − 987 = 13")),
    B("So take away 1000, which leaves 600. We took 13 too many, so give 13 back. 600 plus 13 is 613 girls.",
      W("l3", "1600 − 1000 = 600"), W("l4", "600 + 13 = 613")),
    B("Careful: 613 is among the choices, but that is only the number of girls. The question asks how many more boys.",
      BOX("l4", "613")),
    B("How many more means subtract. 987 minus 613 needs no borrowing: 7 minus 3 is 4, 8 minus 1 is 7, and 9 minus 6 is 3.",
      W("l5", "987 − 613 = ?")),
    B("So there are 374 more boys than girls.",
      ANS("l6", "987 − 613 = 374"), CIRC("l6", "374")),
    B("Check both steps. 613 girls plus 987 boys make 1600, the whole school. And 613 plus 374 is 987.",
      W("l7", "613 + 987 = 1600"), W("l8", "613 + 374 = 987")),
    B("So find the missing group first. Then subtract the smaller group from the bigger to see how many more."),
)

# 1500 students, 643 boys: how many girls?
LESSONS[T5 + "q042"] = LESSON(
    B("A school has 1500 students. 643 are boys and the rest are girls. How many girls are there?",
      GIVEN("q", "1500 students, 643 boys, the rest are girls")),
    B("The school is boys and girls together. Which sum finds the girls?",
      ask=CHOOSE(["1500 + 643", "1500 − 643", "643 − 1500"], 1,
                 "The girls are what is left when the boys are taken out of the whole school. So we subtract 643 from 1500.")),
    B("Now the subtraction. The top number ends in two zeros, so we shall have to borrow carefully.",
      W("l1", "1500 − 643 = ?"), UL("l1", "00")),
    B("Ones: 0 minus 3 cannot be done, and the tens place is 0 too. So borrow from the 5 hundreds. That leaves 4 hundreds and gives 10 tens.",
      LB("c1", "5 hundreds → 4 hundreds and 10 tens")),
    B("Now one of those tens moves to the ones. 9 tens stay behind, and the ones place has 10. 10 minus 3 is 7.",
      LB("c2", "Ones: 10 − 3 = 7")),
    B("Tens: 9 minus 4 is 5.",
      LB("c3", "Tens: 9 − 4 = 5"), BOX("c3", "9")),
    B("Hundreds: 4 minus 6 cannot be done, so borrow the 1 thousand. That makes 14, and 14 minus 6 is 8.",
      LB("c4", "Hundreds: 14 − 6 = 8")),
    B("Read the digits from the top place: 857. There are 857 girls.",
      ANS("l2", "1500 − 643 = 857"), CIRC("l2", "857")),
    B("The slip to watch is at the tens. After lending, that zero becomes 9, not 10. Miss it, and the answer comes out a whole hundred too big."),
    B("Check by adding. 857 girls plus 643 boys is 1500.",
      W("l3", "857 + 643 = 1500")),
    B("So the whole minus one part gives the other part. And when the top number has zeros, borrow one place at a time."),
)

# 1007 students, 17 left, 49 joined, 1000 passed.
LESSONS[T5 + "q017"] = LESSON(
    B("A school begins the year with 1007 students. Some leave, some join, and at the end 1000 pass the examination. We want the number who did not pass.",
      GIVEN("q", "1007 students. 17 left, 49 joined. 1000 passed")),
    B("Before we think about the examination, what do we need to know?",
      ask=CHOOSE(["1007 − 1000", "students at the end of the year", "17 + 49"], 1,
                 "The examination comes at the end of the year, after students have left and joined. So first we need the number of students at the end of the year.")),
    B("17 students left, so they come off. 1007 minus 17 is 990.",
      UL("q", "17 left"), W("l1", "1007 − 17 = 990")),
    B("49 joined, so they go on. 990 plus 49 is 1039. That is how many took the final examination.",
      UL("q", "49 joined"), W("l2", "990 + 49 = 1039")),
    B("Out of 1039, 1000 passed. The rest did not. 1039 minus 1000 is 39.",
      ANS("l3", "1039 − 1000 = 39"), CIRC("l3", "39")),
    B("The trap is to rush in with 1007 minus 1000, which gives only 7. That forgets the school changed during the year."),
    B("Check with a shortcut. 49 came in and 17 went out, so the school grew by 32. And 1007 plus 32 is 1039, the same as before.",
      W("l4", "49 − 17 = 32"), W("l5", "1007 + 32 = 1039")),
    B("So when a group changes over time, bring the group up to date first: take off who left, add who joined. Then answer the question."),
)

# 1900 students, 170 left, 143 joined, 1300 passed.
LESSONS[T5 + "q047"] = LESSON(
    B("A school starts the year with 1900 students. During the year 170 leave and 143 join. In the final examination 1300 pass. How many did not pass?",
      GIVEN("q", "1900 students. 170 left, 143 joined. 1300 passed")),
    B("Let's keep count as the year goes by. First, 170 students leave. 1900 minus 170 is 1730.",
      UL("q", "170 left"), W("l1", "1900 − 170 = 1730")),
    B("Then 143 new students join. What do we do with the 143?",
      ask=CHOOSE(["take it away", "add it"], 1,
                 "Students who join make the school bigger. So the 143 is added on.")),
    B("1730 plus 143 is 1873. That is how many students were there for the examination.",
      UL("q", "143 joined"), W("l2", "1730 + 143 = 1873")),
    B("1300 of them passed. The others are what is left when 1300 is taken away from 1873, and that is 573.",
      ANS("l3", "1873 − 1300 = 573"), CIRC("l3", "573")),
    B("Don't start from 1900 and go straight to the examination. 1900 minus 1300 is 600, but the school had changed by then.",
      W("l4", "1900 − 1300 = 600")),
    B("Look how close the choices are to one another. One slip in the adding changes the answer, so we check. 573 plus 1300 is 1873.",
      W("l5", "573 + 1300 = 1873")),
    B("So follow the year in order: take off the leavers, add the joiners, and only then take away those who passed."),
)
