"""Batch 05: counting numbers by their digits (three one-off questions)."""
from imported_05_lib import ANS, B, FIG, GIVEN, M, N, RING, W, ask, lesson, table

LESSONS = {}

LESSONS["IPMTB_grade5_ch02_q041"] = lesson(
    B("How many 2 digit numbers are odd? Let's count them without writing every single one.",
      GIVEN("q", "Two-digit odd numbers: how many?", True)),
    B("The 2 digit numbers start at 10 and stop at 99.",
      W("r", "10, 11, 12, ... 99", True)),
    B("What makes a number odd?",
      ask=ask("its last digit is 1, 3, 5, 7 or 9", ["its first digit is odd", "it has an odd number of digits"],
              "Look at 11 and 12 on the board. 12 ends in 2, so it is even. 11 ends in 1, so it is odd. Only the last digit decides.")),
    B("Take the numbers that start with 1. The odd ones are 11, 13, 15, 17 and 19. That is 5 of them.",
      W("t1", "11, 13, 15, 17, 19", True), N("t1", "11, 13, 15, 17, 19", "5 odd numbers")),
    B("The twenties give 5 more: 21, 23, 25, 27 and 29. In fact, every tens digit gives exactly 5 odd numbers.",
      W("t2", "21, 23, 25, 27, 29", True), N("t2", "21, 23, 25, 27, 29", "5 again")),
    B("So how many different tens digits can a 2 digit number have?",
      ask=ask("9", ["10", "5"],
              "The tens digit can be 1, 2, 3 and so on up to 9. It cannot be 0, because then the number would have only 1 digit.")),
    B("9 tens digits, with 5 odd numbers for each. 9 times 5 is 45.",
      ANS("a", "9 × 5 = 45"), RING("a", "45")),
    B("Check it another way. From 10 to 99 there are 90 numbers, and odd and even take turns. Half of 90 is 45.",
      W("c1", "99 − 9 = 90"), W("c2", "90 ÷ 2 = 45")),
    B("So to count without listing, find how many choices there are for each digit, then multiply."),
)

LESSONS["IPMTB_grade5_ch02_q042"] = lesson(
    B("How many 3 digit numbers are odd? There are far too many to list, so we need a clever count.",
      GIVEN("q", "Three-digit odd numbers: how many?", True)),
    B("The 3 digit numbers run from 100 up to 999. How many numbers is that?",
      W("r", "100, 101, 102, ... 999", True), W("n", "999 − 99 = ?"),
      ask=ask("900", ["999", "899"],
              "Count every number from 1 to 999, and there are 999. Now take away the 99 short ones, 1 to 99, and what is left is the 3 digit numbers.")),
    B("999 minus 99 is 900. So there are 900 numbers with 3 digits.",
      W("n2", "999 − 99 = 900"), M("n2", "900")),
    B("Now look at how they go: 100 is even, 101 is odd, 102 is even. Odd and even take turns, all the way to 999.",
      M("r", "101", "circle")),
    B("So what part of those 900 numbers is odd?",
      ask=ask("half of them", ["all of them", "one in every 10"],
              "Odd and even take turns, one after the other. The list starts on an even number and ends on an odd one, so they share it equally.")),
    B("Half of 900 is 450. There are 450 odd numbers with 3 digits.",
      ANS("a", "900 ÷ 2 = 450"), RING("a", "450")),
    B("Check by choosing digits. 9 choices for the hundreds, 10 for the tens, and 5 odd digits for the ones. 9 times 10 times 5 is 450 again.",
      W("c", "9 × 10 × 5 = 450")),
    B("Careful not to stop at 900: that is all the 3 digit numbers, odd and even together. Count the whole list, then take half."),
)

LESSONS["IPMTB_grade5_ch02_q045"] = lesson(
    B("We have the digits 3, 4 and 5, and each may be used once. How many different 3 digit numbers can we build?",
      GIVEN("q", "Digits 3, 4, 5, each used once", True)),
    B("A 3 digit number has 3 places to fill: hundreds, tens and ones. Let's fill them one at a time.",
      FIG("f", table(["Hundreds", "Tens", "Ones"], [["?", "?", "?"]]))),
    B("How many digits can we choose from for the hundreds place?",
      ask=ask("3", ["1", "5"],
              "Any of our digits can go first: the 3, the 4 or the 5. That makes 3 choices.")),
    B("Suppose the 3 goes first. Each digit is used only once, so only the 4 and the 5 are left for the tens. That is 2 choices.",
      W("h", "Hundreds: 3 choices", True), W("t", "Tens: 2 choices", True)),
    B("And once the tens place is filled, just 1 digit is left for the ones.",
      W("o", "Ones: 1 choice", True)),
    B("So how do we get the total?",
      ask=ask("3 × 2 × 1", ["3 × 3", "3 + 3"],
              "Each first digit can be followed by 2 different tens digits, and then by 1 ones digit. Choices that follow one another are multiplied.")),
    B("3 times 2 times 1 is 6. We can build 6 numbers.",
      ANS("a", "3 × 2 × 1 = 6"), RING("a", "6")),
    B("Let's list them to be sure. 345, 354, 435, 453, 534, 543. Yes, 6 numbers.",
      W("l", "345, 354, 435, 453, 534, 543", True)),
    B("Careful: 9 would be right only if a digit could be used again. Used once, the choices shrink each time: 3, then 2, then 1."),
)
