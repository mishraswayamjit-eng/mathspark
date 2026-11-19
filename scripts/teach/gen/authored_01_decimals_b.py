"""Decimals, G5A_DECIMALS_007 to 013 (the Easy warm-ups): one short lesson each, written by hand."""
from authored_01_lib import (ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LANS, LB, LESSON, NOTE, STRIKE, UL, W)  # noqa: F401

LESSONS = {}
P = "G5A_DECIMALS_"

# Place value of the 7 in 4.75: 7 tenths
LESSONS[P + "007"] = LESSON(
    B("In the number 4.75, what is the place value of the digit 7?",
      GIVEN("q", "In 4.75, what is the place value of the digit 7?")),
    B("The decimal point is our landmark. Just before it is the ones place. That is where the 4 sits.",
      NOTE("q", "4", "ones")),
    B("The 7 is the first digit after the point. What is that place called?",
      ask=CHOOSE(["tens", "tenths", "hundredths"], 1,
                 "Count the places after the point. The first one after the point is the tenths place, and the second is the hundredths.")),
    B("The first place after the point is the tenths. So the 7 stands for 7 tenths.",
      NOTE("q", "7", "tenths")),
    B("The 5 after it is in the hundredths place. And notice that tenths are not tens. The tens place is on the other side of the point.",
      NOTE("q", "5", "hundredths")),
    B("So the place value of the digit 7 is 7 tenths.",
      LANS("a", "7 tenths"), CIRC("a", "7 tenths")),
    B("Read the places outwards from the point: tenths first, then hundredths."),
)

# Hundredths digit of 36.482: 8
LESSONS[P + "008"] = LESSON(
    B("Which digit is in the hundredths place in 36.482?",
      GIVEN("q", "Which digit is in the hundredths place in 36.482?")),
    B("Start at the decimal point and step to the right. The places are tenths, then hundredths, then thousandths.",
      LB("l1", "tenths, hundredths, thousandths")),
    B("So the hundredths place is which place after the point?",
      ask=CHOOSE(["the first", "the second", "the third"], 1,
                 "Say them in order from the point: tenths, hundredths, thousandths. Hundredths comes second.")),
    B("After the point we have 4, then 8, then 2. The 4 is tenths, the 8 is hundredths, and the 2 is thousandths.",
      NOTE("q", "4", "tenths"), NOTE("q", "8", "hundredths", "above"), NOTE("q", "2", "thousandths")),
    B("So the digit in the hundredths place is 8.",
      LANS("a", "Hundredths digit: 8"), CIRC("a", "8")),
    B("Don't count from the front of the number. The 3 is in the tens place, on the other side of the point. Always count from the decimal point."),
)

# Greatest of 3.4, 3.9, 3.1, 3.7: 3.9
LESSONS[P + "009"] = LESSON(
    B("Which of these numbers is the greatest: 3.4, 3.9, 3.1 or 3.7?",
      GIVEN("q", "Greatest?   3.4,   3.9,   3.1,   3.7")),
    B("To compare decimals, start with the biggest place. All four numbers have 3 ones, so the ones can't decide it."),
    B("Where do we look next?",
      ask=CHOOSE(["the tenths digits", "the number of digits", "nowhere, they are equal"], 0,
                 "After the ones comes the tenths place, the first digit after the point. Those digits are different, so they decide.")),
    B("The tenths digits are 4, 9, 1 and 7. The biggest of those is 9.",
      UL("q", "3.9")),
    B("So the greatest number is 3.9.",
      LANS("a", "Greatest: 3.9"), CIRC("a", "3.9")),
    B("It makes sense: 3.9 is only one tenth short of 4, closer than any of the others. So compare the ones first, then the tenths."),
)

# Smallest of 0.52, 0.35, 0.25, 0.55: 0.25
LESSONS[P + "010"] = LESSON(
    B("Which of these numbers is the smallest: 0.52, 0.35, 0.25 or 0.55?",
      GIVEN("q", "Smallest?   0.52,   0.35,   0.25,   0.55")),
    B("All four have 0 ones. So go to the tenths, the first digit after the point: 5, 3, 2 and 5."),
    B("Which number has the fewest tenths?",
      ask=CHOOSE(["0.52", "0.35", "0.25"], 2,
                 "Look only at the first digit after the point. 0.52 has 5 tenths, 0.35 has 3 tenths, and 0.25 has 2 tenths.")),
    B("0.25 has only 2 tenths, fewer than any other. Once the tenths decide it, the hundredths don't matter.",
      UL("q", "0.25")),
    B("A slip to avoid: picking 0.52 because it ends in a small 2. That 2 is only hundredths. Its 5 tenths make it much bigger."),
    B("So the smallest number is 0.25.",
      LANS("a", "Smallest: 0.25"), CIRC("a", "0.25")),
    B("Compare the tenths first. Look at the hundredths only when the tenths are the same, as in 0.52 and 0.55."),
)

# 2.5 + 1.3 = 3.8
LESSONS[P + "011"] = LESSON(
    B("What is 2.5 plus 1.3? We add tenths with tenths, and ones with ones.",
      W("q", "2.5 + 1.3", "given")),
    B("Start with the tenths. They are the digits just after each point: 5 tenths and 3 tenths.",
      UL("q", "5"), UL("q", "3")),
    B("5 tenths and 3 tenths make how many tenths?",
      ask=CHOOSE(["8 tenths", "2 tenths", "8 ones"], 0,
                 "We are adding, so put the 5 tenths and the 3 tenths together. 5 and 3 make 8, and they are still tenths.")),
    B("8 tenths. Now the ones: 2 and 1 make 3.",
      W("l1", "0.5 + 0.3 = 0.8"), W("l2", "2 + 1 = 3")),
    B("3 ones and 8 tenths make 3.8.",
      *ANSC("l3", "2.5 + 1.3 = 3.8", "3.8")),
    B("Check by taking away: 3.8 minus 1.3 brings us back to 2.5. So line up the points, and add each place with its own kind.",
      W("c1", "3.8 − 1.3 = 2.5")),
)

# ₹8.50 − ₹3.20 = ₹5.30
LESSONS[P + "012"] = LESSON(
    B("Rani had 8.50 rupees. She spent 3.20 rupees on a pencil. How much money does she have left?",
      GIVEN("q", "Rani had ₹8.50. She spent ₹3.20. Money left?")),
    B("She spent some of her money. Do we add, or take away?",
      ask=CHOOSE(["add", "take away"], 1,
                 "Spending makes the money in her purse go down. So we take away what she spent from what she had.")),
    B("We take away. Line up the points, so that rupees are under rupees and paise are under paise.",
      W("l1", "8.50 − 3.20")),
    B("Paise first: 50 paise take away 20 paise leaves 30 paise.",
      W("l2", "50 − 20 = 30")),
    B("Rupees next: 8 take away 3 leaves 5 rupees.",
      W("l3", "8 − 3 = 5")),
    B("5 rupees and 30 paise. Rani has 5.30 rupees left.",
      *ANSC("l4", "8.50 − 3.20 = 5.30", "5.30")),
    B("Check by adding back: 5.30 plus 3.20 is 8.50, just what she started with.",
      W("c1", "5.30 + 3.20 = 8.50")),
)

# 4.6 × 10 = 46
LESSONS[P + "013"] = LESSON(
    B("What is 4.6 times 10?",
      W("q", "4.6 × 10", "given")),
    B("Multiplying by 10 makes every digit worth 10 times as much. So each digit moves one place to the left."),
    B("The 4 ones become 4 tens. The 6 tenths become 6 ones.",
      NOTE("q", "4", "ones → tens", "above"), NOTE("q", "6", "tenths → ones")),
    B("So what is 4.6 times 10?",
      ask=CHOOSE(["46", "460", "40.6"], 0,
                 "We have 4 tens and 6 ones. Write the 4 in the tens place and the 6 in the ones place.")),
    B("4 tens and 6 ones make 46. It looks as if the decimal point has hopped one place to the right.",
      *ANSC("l1", "4.6 × 10 = 46", "46")),
    B("Two slips to avoid: don't hop two places, and don't push a zero into the middle. Times 10 means one hop. Check: 46 divided by 10 is 4.6 again.",
      W("c1", "46 ÷ 10 = 4.6")),
)
