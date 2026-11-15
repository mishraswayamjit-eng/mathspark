"""Lessons written by hand for the one-off worksheet questions (place-value algebra, bags, pen and pencil)."""
from algebra_lib import B, THINK, W, answer, both, choose, divide, given, group, lesson, mark, note, strike

LESSONS = {}

# 7**19: the two stars are the same digit; their place values differ by 5400.
LESSONS["EXT_G5_WS_01_008"] = lesson([
    B("Here is a five digit number with two stars in it. Both stars hide the same digit, and we are going to find it.",
      given("l1", "7 * * 1 9", label=True)),
    B("First, look at where the stars sit. Which two places are they in?",
      ask=choose(["hundreds and tens", "thousands and hundreds", "ten thousands and thousands"], 1,
                 "Count the places from the right. The 9 is in the ones, the 1 is in the tens. "
                 "Then come the two stars, in the hundreds and the thousands.")),
    B("Let's call the hidden digit d. In the thousands place it is worth 1000 times d. "
      "In the hundreds place it is worth 100 times d.",
      note("l1", ("*", 1), "1000d"), note("l1", ("*", 2), "100d", "below")),
    B("We are told the difference between those two values is 5400. So 1000 d, minus 100 d, equals 5400.",
      W("l2", "1000d − 100d = 5400")),
    B("1000 lots of d, take away 100 lots of d, leaves 900 lots of d. So 900 d equals 5400.",
      group("l2", ["1000d", "100d"], "900d"), W("l3", "900d = 5400")),
    B("900 d means 900 times d. What undoes times 900?",
      ask=choose(["subtract 900", "divide by 900", "multiply by 900"], 1,
                 "Times and divide are partners. To undo times 900, we divide by 900, and we do it to both sides.")),
    B("So we divide both sides by 900. 5400 divided by 900 is 6.",
      divide("l3", "900"), answer("l4", "d = 6"), mark("l4", "d = 6")),
    B("Let's check. A 6 in the thousands place is worth 6000. A 6 in the hundreds place is worth 600. "
      "6000 minus 600 is 5400. It works.",
      W("l5", "6000 − 600 = 5400")),
    B("So when the same digit sits in two places, write each place value using a letter, subtract, and solve. "
      "The digit is 6."),
], "d", 6)

# 3*8*2: thousands and tens; difference 6930.
LESSONS["EXT_G5_WS_01_009"] = lesson([
    B("This number has two stars, and the same digit hides behind both. Let's find out which digit it is.",
      given("l1", "3 * 8 * 2", label=True)),
    B("The same digit is worth different amounts in different places. So, where are the two stars?",
      ask=choose(["thousands and tens", "thousands and hundreds", "hundreds and ones"], 0,
                 "Count from the right: 2 is in the ones, then a star in the tens, 8 in the hundreds, "
                 "and the other star in the thousands.")),
    B("Call the digit d. In the thousands place it is worth 1000 times d. In the tens place it is worth 10 times d.",
      note("l1", ("*", 1), "1000d"), note("l1", ("*", 2), "10d", "below")),
    B("The question says the difference between those values is 6930. So 1000 d, minus 10 d, equals 6930.",
      W("l2", "1000d − 10d = 6930")),
    B("1000 lots of d, take away 10 lots of d, is 990 lots of d.",
      group("l2", ["1000d", "10d"], "990d"), W("l3", "990d = 6930")),
    B("Now d is being multiplied by 990. How do we get d on its own?",
      ask=choose(["take 990 from both sides", "divide both sides by 990", "multiply both sides by 990"], 1,
                 "990 d means 990 times d, and divide is what undoes times. So we divide both sides by 990.")),
    B("So a bar goes under each side, and we divide by 990. 990 times 7 is 6930, so d equals 7.",
      divide("l3", "990"), answer("l4", "d = 7"), mark("l4", "d = 7")),
    B("Check it. A 7 in the thousands place is worth 7000, and a 7 in the tens place is worth 70. "
      "7000 minus 70 is 6930. Just right.",
      W("l5", "7000 − 70 = 6930")),
    B("So the repeated digit is 7. The trick was to write both place values with one letter, "
      "then solve a small equation."),
], "d", 7)

# 6*8*4: which choice can be the difference between the place values of the repeated digit?
LESSONS["EXT_G5_WS_01_010"] = lesson([
    B("Two stars again, hiding the same digit. But this time we are not told the digit. "
      "We are asked what the difference between its two place values could be.",
      given("l1", "6 * 8 * 4", label=True)),
    B("Start with the places. Where do the two stars sit?",
      ask=choose(["thousands and hundreds", "hundreds and tens", "thousands and tens"], 2,
                 "From the right: 4 is in the ones, a star in the tens, 8 in the hundreds, "
                 "and the other star in the thousands.")),
    B("Let's try the easiest digit, 1. Then the two place values are 1000 and 10, and the difference is 990.",
      W("l2", "1000 − 10 = 990")),
    B("If the digit were 2, we would get 2000 minus 20. That is just 2 lots of 990. "
      "So the difference is always the digit times 990.",
      W("l3", "2000 − 20 = 2 × 990"), W("l4", "difference = digit × 990", label=True),
      mark("l4", "digit × 990", "underline")),
    B("So the right choice must be in the 990 times table. 540 is smaller than 990, so it is out. "
      "Have a think: which of the others could it be?",
      W("l4b", "choices: 3030, 540, 8910, 1880", label=True), strike("l4b", "540"),
      ask=THINK),
    B("2 times 990 is 1980, so 1880 just misses. 3 times 990 is 2970, and 4 times is 3960, so 3030 is skipped too.",
      W("l5", "2 × 990 = 1980"), W("l6", "3 × 990 = 2970"), W("l7", "4 × 990 = 3960"),
      strike("l4b", "1880"), strike("l4b", "3030")),
    B("Now try the biggest digit, 9. 9 times 990 is 8910. That is one of our choices!",
      answer("l8", "9 × 990 = 8910"), mark("l8", "8910")),
    B("Check with the digit 9. In the thousands place it is worth 9000, and in the tens place 90. "
      "9000 minus 90 is 8910.",
      W("l9", "9000 − 90 = 8910")),
    B("So the difference can be 8910. When you do not know the digit, try 1 first and look for the pattern."),
])

# For any natural number X, 2X + 11 is never ...
LESSONS["EXT_G5_WS_B2_005"] = lesson([
    B("Here is a little number machine: 2 X plus 11. X can be any counting number we like. "
      "The question asks what kind of number can never come out.",
      given("l1", "2X + 11", label=True)),
    B("When a question says any number, try a few small ones. With X as 1 we get 13. With 2 we get 15. With 3 we get 17.",
      W("l2", "2 × 1 + 11 = 13"), W("l3", "2 × 2 + 11 = 15"), W("l4", "2 × 3 + 11 = 17")),
    B("Look at 13, 15 and 17. What do they have in common?",
      ask=choose(["they are all even", "they are all odd", "they are all prime"], 1,
                 "Look at the last digits: 3, 5 and 7. None of these numbers can be shared into 2 equal groups. "
                 "They are all odd. And 15 is 3 times 5, so they are not all prime.")),
    B("Is that just luck? No. 2 times any whole number is always even. That is what even means.",
      mark("l1", "2X", "underline"), note("l1", "2X", "always even")),
    B("And 11 is odd. An even number plus an odd number is always odd.",
      note("l1", "11", "odd"), W("l5", "even + odd = odd", label=True)),
    B("So 2 X plus 11 is odd every single time. That means it can never be even.",
      answer("l6", "2X + 11 is never even", label=True), mark("l6", "never even")),
    B("And the other choices? 13 and 17 are prime, so it can be prime. "
      "And every answer we got was a whole number. So those can happen."),
    B("So the plan: try a few small numbers, spot the pattern, then ask why the pattern must always hold."),
])

# Three bags, 27 oranges. First + second = 13, second + third = 19. First + third?
LESSONS["EXT_G5_WS_B2_021"] = lesson([
    B("Three bags of oranges. We know three totals, so let me write them down in short.",
      given("l1", "1st + 2nd + 3rd = 27", label=True), given("l2", "1st + 2nd = 13", label=True),
      given("l3", "2nd + 3rd = 19", label=True)),
    B("Look at the first two lines. All three bags hold 27, and the first and second together hold 13. "
      "Which bag can we find from that?",
      ask=choose(["the first bag", "the second bag", "the third bag"], 2,
                 "The 13 covers the first and second bags. Take those away from all 27 oranges, "
                 "and what is left must be in the third bag.")),
    B("So the third bag holds 27 minus 13, which is 14 oranges.",
      group("l1", ["1st", "2nd"], "13"), W("l4", "27 − 13 = 14"), note("l4", "14", "3rd bag")),
    B("We can use the same idea again. The second and third bags hold 19, so the first bag holds 27 minus 19. That is 8.",
      group("l1", [("2nd", 1), "3rd"], "19"), W("l5", "27 − 19 = 8"), note("l5", "8", "1st bag")),
    B("Careful now. The question does not want one bag. What is it asking for?",
      ask=choose(["the first bag only", "the first and third bags together", "the second bag"], 1,
                 "Read the last line of the question again. It asks how many oranges in all "
                 "in the first and the third bags.")),
    B("So we add the first bag and the third bag. 8 plus 14 is 22.",
      answer("l6", "8 + 14 = 22"), mark("l6", "22")),
    B("Let's check with the second bag. The first two hold 13, so the second has 13 minus 8, which is 5. "
      "And 5 plus 14 is 19, just as the question said.",
      W("l7", "13 − 8 = 5"), W("l8", "5 + 14 = 19")),
    B("So when you know the whole and a part, subtract to find the missing part. The answer is 22 oranges."),
])

# Pen + pencil = Rs 18, pen is Rs 10 more. Cost of 3 pencils?
LESSONS["EXT_G5_WS_B3_029"] = lesson([
    B("A pen and a pencil cost 18 rupees together, and the pen costs 10 rupees more than the pencil. "
      "Let me write that in short.",
      given("l1", "pen + pencil = 18", label=True), given("l2", "pen = pencil + 10", label=True)),
    B("So a pen is really a pencil with 10 rupees extra. Let me swap the pen for that. "
      "Now we have a pencil, plus 10, plus another pencil, making 18.",
      note("l1", "pen", "pencil + 10"), W("l3", "pencil + 10 + pencil = 18", label=True)),
    B("Take the extra 10 away, and 8 rupees are left. What does that 8 pay for?",
      strike("l3", "+ 10", "− 10"), W("l4", "18 − 10 = 8"),
      ask=choose(["one pencil", "two pencils", "one pen"], 1,
                 "Look at the line above. Once the 10 is gone, what is left on that side is a pencil "
                 "and another pencil. So 8 rupees pays for two pencils.")),
    B("Two pencils cost 8 rupees, so one pencil costs half of that, which is 4 rupees.",
      W("l5", "8 ÷ 2 = 4"), note("l5", "4", "one pencil")),
    B("Now read the question once more. Is 4 our answer?",
      ask=choose(["Yes, a pencil costs 4", "No, we need 3 pencils"], 1,
                 "4 rupees is the price of one pencil. But the question asks how much we pay for 3 pencils.")),
    B("3 pencils cost 3 times 4, which is 12 rupees.",
      answer("l6", "3 × 4 = 12"), mark("l6", "12")),
    B("Check the story. A pencil is 4, so a pen is 4 plus 10, which is 14. And 4 plus 14 is 18. It fits.",
      W("l7", "4 + 10 = 14"), W("l8", "4 + 14 = 18")),
    B("So the plan: take off the extra, share what is left equally, then answer exactly what was asked. 12 rupees."),
])
