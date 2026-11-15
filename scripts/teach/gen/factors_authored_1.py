"""Hand-written lessons, part 1: worksheet questions on multiples and divisibility by 3, 5."""
from factors_lib import *  # noqa: F401,F403

LESSONS = {}

# The greatest three-digit number that is completely divisible by 57.
LESSONS["EXT_G5_WS_B3_016"] = LESSON(
    B("We want the greatest three-digit number that 57 divides exactly. So it must be in the 57 times table, and it must not go past 999.",
      GIVEN("q", "Greatest 3-digit multiple of 57 = ?"), LB("top", "Biggest 3-digit number: 999")),
    B("Let's get close to 999 quickly. 57 times 10 is 570. That is too small, so we need more 57s.",
      W("m10", "57 × 10 = 570")),
    B("Double it: 57 times 20 is 1140. What does that tell us?",
      W("m20", "57 × 20 = 1140"),
      ask=CHOOSE(["That is our answer", "Too far: it has four digits", "We need even more 57s"], 1,
                 "1140 has four digits, so it has gone past 999. Our number is somewhere between 10 lots and 20 lots of 57.")),
    B("So we step back from 1140, one 57 at a time. 1140 minus 57 is 1083. Still four digits.",
      W("s1", "1140 − 57 = 1083")),
    B("Step back again. 1083 minus 57 is 1026. Still too big.",
      W("s2", "1083 − 57 = 1026")),
    B("Once more: 1026 minus 57 is 969. Three digits at last!",
      W("s3", "1026 − 57 = 969"), CIRC("s3", "969")),
    B("We took 3 lots away from 20 lots, so that is 17 lots. 57 times 17 is 969, and the next one up, 57 times 18, is 1026.",
      W("m17", "57 × 17 = 969"), W("m18", "57 × 18 = 1026")),
    B("So the greatest three-digit multiple of 57 is 969.",
      ANS("ans", "Answer: 969"), CIRC("ans", "969")),
    B("One trap: a bigger-looking choice is no good unless it is in the 57 times table. So jump close with easy multiples, then step one 57 at a time until you are just under the limit."),
)

# The smallest four-digit number that is exactly divisible by 57.
LESSONS["EXT_G5_WS_B3_017"] = LESSON(
    B("We want the smallest four-digit number in the 57 times table. Four-digit numbers start at 1000, so we need the first multiple of 57 that reaches 1000 or more.",
      GIVEN("q", "Smallest 4-digit multiple of 57 = ?"), LB("low", "Smallest 4-digit number: 1000")),
    B("Jump close first. 57 times 10 is 570, and double that, 57 times 20, is 1140.",
      W("m10", "57 × 10 = 570"), W("m20", "57 × 20 = 1140")),
    B("1140 has four digits and it is in the 57 times table. But it is 140 past 1000. Is it surely the smallest?",
      W("gap", "1140 − 1000 = 140"),
      ask=CHOOSE(["Yes, it must be", "Not yet: a smaller one may fit"], 1,
                 "The gap of 140 is bigger than 57. So there is room for another multiple of 57 between 1000 and 1140.")),
    B("So step back one 57 at a time. 1140 minus 57 is 1083. Still four digits.",
      W("s1", "1140 − 57 = 1083")),
    B("Step back again. 1083 minus 57 is 1026. Still four digits!",
      W("s2", "1083 − 57 = 1026")),
    B("And once more: 1026 minus 57 is 969. That has only three digits, so now we have gone too far.",
      W("s3", "1026 − 57 = 969"), STRIKE("s3", "969", "3 digits")),
    B("So 1026 is the smallest four-digit multiple. It is 18 lots of 57.",
      W("m18", "57 × 18 = 1026"), ANS("ans", "Answer: 1026"), CIRC("ans", "1026")),
    B("Name the trap: 1140 is a four-digit multiple of 57 too, and it is easy to stop there. Always step back to see whether a smaller one still fits."),
)

# The continuous product of three numbers is 2880. Two of them are 12 and 15.
LESSONS["EXT_G5_WS_B3_022"] = LESSON(
    B("Three numbers multiply together to make 2880. Two of them are 12 and 15, and the third is hiding.",
      GIVENM("q", "12 × 15 × ? = 2880")),
    B("First, squash the two numbers we know into one. 12 times 10 is 120, and 12 times 5 is 60. Together that is 180.",
      W("p1", "12 × 15 = 120 + 60"), W("p2", "12 × 15 = 180"), GROUP("q", ["12", "15"], "180")),
    B("So now 180 times the hidden number is 2880. How do we find a missing factor?",
      W("e", "180 × ? = 2880"),
      ask=CHOOSE(["Subtract 180 from 2880", "Divide 2880 by 180", "Multiply 2880 by 180"], 1,
                 "Times and divide are partners. If 180 times something makes 2880, then 2880 divided by 180 gives that something.")),
    B("2880 divided by 180. Both end in 0, so knock a 0 off each. That leaves 288 divided by 18.",
      W("d", "2880 ÷ 180 = 288 ÷ 18"), STRIKE("d", "0", None, 1), STRIKE("d", "0", None, 2)),
    B("18 times 10 is 180. Take that from 288 and 108 is left. And 18 times 6 is 108.",
      W("d1", "18 × 10 = 180"), W("d2", "288 − 180 = 108"), W("d3", "18 × 6 = 108")),
    B("10 lots and 6 lots make 16 lots. So the third number is 16.",
      W("d4", "288 ÷ 18 = 16"), ANS("ans", "Third number = 16"), CIRC("ans", "16")),
    B("Check it. 180 times 10 is 1800, and 180 times 6 is 1080. Together that is 2880. It works.",
      W("c1", "180 × 16 = 1800 + 1080"), W("c2", "12 × 15 × 16 = 2880")),
    B("So when a product is known and one factor is missing: multiply the factors you have, then divide the product by that."),
)

# The sum of two consecutive multiples of 9 is 153. Which is the larger?
LESSONS["EXT_G5_WS_B3_027"] = LESSON(
    B("Two multiples of 9, next-door neighbours in the 9 times table, add up to 153. We want the larger one.",
      GIVEN("q", "Two neighbouring multiples of 9 add up to 153")),
    B("Neighbours in the 9 times table are always 9 apart. So the larger one is just the smaller one with an extra 9 on the end. Look at the two bars.",
      FIG("bars", {"kind": "barModel", "bars": [
          {"label": "smaller", "segments": [{"units": 3, "label": "?", "tone": "unknown"}]},
          {"label": "larger", "segments": [{"units": 3, "label": "?", "tone": "unknown"}, {"units": 1, "label": "9", "tone": "a"}]},
      ], "note": "Together the two bars make 153."})),
    B("Suppose we take that extra 9 away from the total. What would be left?",
      ask=CHOOSE(["The larger multiple", "Two equal parts", "Nothing useful"], 1,
                 "Without the extra 9, the two bars are exactly the same length. So what is left is two equal parts, each one the smaller multiple.")),
    B("153 minus 9 is 144. That is two copies of the smaller multiple.",
      W("a", "153 − 9 = 144")),
    B("So halve it. 144 divided by 2 is 72, and that is the smaller multiple.",
      W("b", "144 ÷ 2 = 72")),
    B("Careful: the question asks for the larger one. Put the 9 back: 72 plus 9 is 81.",
      W("c", "72 + 9 = 81"), ANS("ans", "Larger multiple = 81"), CIRC("ans", "81")),
    B("Check. 72 is 9 times 8 and 81 is 9 times 9, so they are neighbours in the table. And 72 plus 81 is 153.",
      W("k1", "72 = 9 × 8"), W("k2", "81 = 9 × 9"), W("k3", "72 + 81 = 153")),
    B("So for two neighbours with a known sum: take away the gap, halve, then add the gap back for the bigger one."),
)

# 7✻14 is a four-digit multiple of 3. Which digit can replace the asterisk?
LESSONS["EXT_G5_WS_B4_001"] = LESSON(
    B("One digit of this four-digit number is hidden behind a star. The number is a multiple of 3, and we must find which digit could be hiding there.",
      GIVEN("q", "7✻14 is a multiple of 3")),
    B("What is the quick test for a multiple of 3?",
      ask=CHOOSE(["Look at the last digit", "See whether it is odd", "Add up the digits"], 2,
                 "The last digit does not help with 3. The trick is to add up all the digits: if the sum is in the 3 times table, so is the number.")),
    B("Add the digits we can see. 7 plus 1 plus 4 is 12.",
      UL("q", "7"), UL("q", "1"), UL("q", "4"), W("s", "7 + 1 + 4 = 12")),
    B("12 is already in the 3 times table. So the hidden digit must keep the total in the 3 times table. Let's try each choice.",
      NOTE("s", "12", "3 × 4", "below")),
    B("With 6: 12 plus 6 is 18, and 18 is 3 times 6. That works.",
      W("t6", "12 + 6 = 18"), NOTE("t6", "18", "3 × 6", "below")),
    B("With 9: 12 plus 9 is 21. Is 21 in the 3 times table?",
      W("t9", "12 + 9 = 21"),
      ask=CHOOSE(["Yes: 3 × 7 = 21", "No: there is a remainder"], 0,
                 "3 times 7 is 21, so yes. That means 9 works as well.")),
    B("And with 0: 12 plus 0 is still 12, which is 3 times 4. So 0 works too!",
      W("t0", "12 + 0 = 12")),
    B("So 7614, 7914 and 7014 are all multiples of 3. Any of the three digits can hide behind the star: all of these.",
      LB("all", "7614, 7914, 7014: all multiples of 3"), ANS("ans", "Answer: all of these"), CIRC("ans", "all of these")),
    B("The trap here is stopping at the first digit that works. When all of these is one of the choices, test every one."),
)

# In 5✻✻ the two hidden digits are the same; divisible by 3; largest digit?
LESSONS["EXT_G5_WS_B4_002"] = LESSON(
    B("Two stars hide the same digit, twice. The number is divisible by 3, and we want the largest digit that works.",
      GIVEN("q", "5✻✻ is divisible by 3 (same digit twice)")),
    B("For 3, we add the digits. Here that is 5, plus the hidden digit, plus the hidden digit again.",
      LB("s", "Digit sum = 5 + ✻ + ✻")),
    B("We want the largest digit. So which choice should we test first?",
      ask=CHOOSE(["5, the smallest", "9, the biggest", "The order does not matter"], 1,
                 "We are hunting for the largest digit that works. So start from the biggest choice, 9, and work down. The first one that passes wins.")),
    B("Try 9. 5 plus 9 plus 9 is 23. That is 3 times 7, plus 2 left over, so 9 does not work.",
      W("t9", "5 + 9 + 9 = 23"), NOTE("t9", "23", "3 × 7 + 2", "below")),
    B("Next biggest is 8. 5 plus 8 plus 8 is 21, and 21 is 3 times 7 exactly. So 588 is divisible by 3.",
      W("t8", "5 + 8 + 8 = 21"), NOTE("t8", "21", "3 × 7", "below"), W("d", "588 ÷ 3 = 196")),
    B("We started from the top, so no bigger digit works. The largest digit is 8.",
      ANS("ans", "Largest digit = 8"), CIRC("ans", "8")),
    B("A trap to notice: 5 works too, because 5 plus 5 plus 5 is 15. But the question asks for the largest, and 8 beats 5.",
      W("t5", "5 + 5 + 5 = 15")),
    B("So: write the digit sum, test from the biggest choice down, and stop at the first one that lands in the 3 times table."),
)

# How many numbers between 60 and 100 are exactly divisible by 3?
LESSONS["EXT_G5_WS_B4_003"] = LESSON(
    B("How many numbers between 60 and 100 are in the 3 times table? Writing them all out works, but there is a smarter way to count.",
      GIVEN("q", "Multiples of 3 between 60 and 100: how many?")),
    B("Between means 60 and 100 themselves are not counted. So what is the first multiple of 3 after 60?",
      ask=CHOOSE(["60", "61", "63"], 2,
                 "60 is a multiple of 3, but between does not include the ends. The next multiple is 3 more, which is 63.")),
    B("63 is 3 times 21. So it is the 21st number in the 3 times table.",
      W("a", "63 = 3 × 21")),
    B("Now the last one. 100 is not in the 3 times table, but 99 is: 3 times 33. So the last one is the 33rd.",
      W("b", "99 = 3 × 33"),
      FIG("line", {"kind": "numberLine", "min": 60, "max": 99, "step": 3, "tickLabels": "ends",
                   "points": [{"at": 63, "label": "21st"}, {"at": 99, "label": "33rd"}]})),
    B("So we are counting from the 21st to the 33rd. How many numbers is that?",
      ask=CHOOSE(["33 − 21 = 12", "33 − 21 + 1 = 13", "33 + 21 = 54"], 1,
                 "Subtracting gives the number of jumps, which is 12. But we count both ends, the 21st and the 33rd, so we add 1.")),
    B("33 minus 21 is 12 jumps, plus 1 because both ends count. That makes 13.",
      W("c", "33 − 21 + 1 = 13"), ANS("ans", "13 numbers"), CIRC("ans", "13")),
    B("The classic slip is forgetting that plus 1. Think of counting from the 1st to the 3rd: that is 3 things, not 2."),
    B("So to count multiples in a range: find the first and the last, see which numbers they are in the table, subtract, and add 1."),
)

# How many two-digit multiples of 4 are there in all?
LESSONS["EXT_G5_WS_B4_004"] = LESSON(
    B("How many two-digit numbers are in the 4 times table? Two-digit numbers run from 10 to 99.",
      GIVEN("q", "Two-digit multiples of 4: how many?"), LB("r", "Two-digit numbers: 10 to 99")),
    B("What is the first two-digit number in the 4 times table?",
      ask=CHOOSE(["8", "10", "12"], 2,
                 "8 is in the table but has only one digit, and 10 is not in the table at all. 4 times 3 is 12, so 12 is the first.")),
    B("12 is 4 times 3. So the first two-digit multiple is number 3 in the table.",
      W("a", "12 = 4 × 3")),
    B("For the last one, start near 99. 4 times 25 is 100, which has three digits. Step back one 4 and we land on 96, which is 4 times 24.",
      W("b1", "4 × 25 = 100"), W("b", "96 = 4 × 24")),
    B("So we count from number 3 in the table up to number 24. How many multiples is that?",
      ask=CHOOSE(["21", "22", "24"], 1,
                 "Up to 96 there are 24 multiples of 4. The first 2 of them, which are 4 and 8, have only one digit. Take those 2 away and 22 are left.")),
    B("24 minus 3, plus 1 for counting both ends, is 22.",
      W("c", "24 − 3 + 1 = 22"), ANS("ans", "22 multiples"), CIRC("ans", "22")),
    B("Here is another way to see it. 24 multiples of 4 go up to 96, but 4 and 8 have only one digit. 24 minus 2 is 22 again.",
      W("k", "24 − 2 = 22")),
    B("So: find the first and last multiple, note which numbers they are in the table, subtract, and add 1."),
)

# Least number to add to 527 × 308 so the sum is divisible by 5.
LESSONS["EXT_G5_WS_B4_005"] = LESSON(
    B("We must add the least number to 527 times 308 so that 5 divides the result. That looks like a big multiplication, but we can dodge it.",
      GIVEN("q", "527 × 308 + ? is divisible by 5")),
    B("When is a number divisible by 5?",
      ask=CHOOSE(["When its digits add up to 5", "When it ends in 0 or 5", "When it is odd"], 1,
                 "Think of the 5 times table: 5, 10, and so on. Every number in it ends in 5 or 0. So only the last digit matters.")),
    B("So we only need the last digit of the product. And that comes only from the two last digits: 7 times 8.",
      UL("q", "7"), UL("q", "8"), W("m", "7 × 8 = 56")),
    B("7 times 8 is 56, so the whole product ends in 6.",
      CIRC("m", "6"), LB("e", "The product ends in 6")),
    B("Count up from a number ending in 6. Which do we reach first?",
      ask=CHOOSE(["Ending in 5, after adding 9", "Ending in 0, after adding 4", "Ending in 5, after adding 1"], 1,
                 "From 6 we count 7, 8, 9, and then 0. That is 4 steps. To reach a 5 we would have to carry on for 9 steps.")),
    B("6 plus 4 makes 10, so adding 4 makes the number end in 0. The least number to add is 4.",
      W("a", "6 + 4 = 10"), ANS("ans", "Least number to add = 4"), CIRC("ans", "4")),
    B("We can check with the full product. 527 times 308 is 162316. Add 4 and we get 162320, which ends in 0.",
      W("c1", "527 × 308 = 162316"), W("c2", "162316 + 4 = 162320")),
    B("Adding 9 would work as well, but the question asks for the least. So: find the last digit, then count up to the next 0 or 5."),
)

# What to subtract from 169 × 47 so the result is divisible by 5.
LESSONS["EXT_G5_WS_B4_006"] = LESSON(
    B("We take a number away from 169 times 47 so that 5 divides what is left. A number is divisible by 5 only when it ends in 0 or 5.",
      GIVEN("q", "169 × 47 − ? is divisible by 5")),
    B("So we need the last digit of the product. Which digits decide it?",
      ask=CHOOSE(["The 1 and the 4", "All of the digits", "The 9 and the 7"], 2,
                 "Only the ones digits can reach the ones place of the answer. So we multiply just the 9 and the 7.")),
    B("9 times 7 is 63. So the product ends in 3.",
      UL("q", "9"), UL("q", "7"), W("m", "9 × 7 = 63"), CIRC("m", "3")),
    B("We are taking away now, so we go down. From a number ending in 3, what do we reach first?",
      ask=CHOOSE(["Ending in 0, after taking 3", "Ending in 5, after taking 8", "Ending in 5, after taking 2"], 0,
                 "Count down from 3: 2, 1, 0. Three steps and the number ends in 0. Reaching a 5 would take 8 steps.")),
    B("Take away 3 and the last digit becomes 0. So 3 should be subtracted.",
      W("a", "3 − 3 = 0"), ANS("ans", "Subtract 3"), CIRC("ans", "3")),
    B("Check with the full product. 169 times 47 is 7943. Take away 3 and we get 7940, which ends in 0.",
      W("c1", "169 × 47 = 7943"), W("c2", "7943 − 3 = 7940")),
    B("Taking away 8 would also work, but 8 is not among the choices. The method: find the last digit of the product, then step down to the nearest 0 or 5."),
)
