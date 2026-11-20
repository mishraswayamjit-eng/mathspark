"""gr4_numbers, written per question: past final papers (EXT_G4_FP_...)."""
from g4_gr4_numbers_lib import A, FIG, G, Q, U, W, b, chart, table
from g4_gr4_numbers_a1 import LETTERS

L = {}

L["EXT_G4_FP_2020_019"] = [
    b("We are building a 5-digit number from clues. Let us set out 5 empty seats first.",
      G("5-digit number from the clues = ?"), W("TTh   Th   H   T   O")),
    b("One clue says 6 is in the greatest place. In a 5-digit number, which seat is the greatest place?",
      Q(["ten-thousands", "thousands", "ones"],
        "The greatest place is the seat furthest to the left. In a 5-digit number that is the ten-thousands place.")),
    b("So the 6 goes in the ten-thousands seat. The least place is the ones, so the 5 goes at the far right.",
      W("6   _   _   _   5")),
    b("Now the other clues. 9 in the thousands, 7 in the hundreds, and 1 in the tens.", W("6   9   7   1   5")),
    b("Read the seats from left to right. The number is 69715.", A("69715"), FIG(chart("69715"))),
    b("Careful: the clues were not given in order. The 9 was named first, but it does not go first. Always match each digit to its own seat."),
    b("Check with the clues: 6 ten-thousands, 9 thousands, 7 hundreds, 1 ten and 5 ones. Every clue fits."),
]

L["EXT_G4_FP_2021_031"] = [
    b("Here is a number with two stars in it. Both stars hide the same digit, and we want the difference between their place values.",
      G("6★74★3: difference of the two ★ place values")),
    b("First find the seats. From the right: 3 is in the ones, a star is in the tens, 4 is in the hundreds and 7 is in the thousands. Where is the other star?",
      W("ones: 3   tens: ★   hundreds: 4   thousands: 7"),
      Q(["ten-thousands", "thousands", "lakhs"],
        "Count on from the right: ones, tens, hundreds, thousands, and then ten-thousands. That is where the second star sits.")),
    b("So one star is worth the digit times 10000, and the other is worth the digit times 10.",
      W("★ × 10000   and   ★ × 10")),
    b("We do not know the star yet, so let us test with 1. The place values would be 10000 and 10, and their difference is 9990.",
      W("10000 − 10 = 9990")),
    b("With a bigger star, both values grow the same way. So the answer must be 9990 times a single digit. That is the key idea.",
      W("difference = ★ × 9990")),
    b("Try 7. The place values are 70000 and 70, and 70000 minus 70 is 69930. That is one of our choices!",
      W("70000 − 70 = 69930"), W("7 × 9990 = 69930")),
    b("Careful with the choice 49990. It looks right, but a star of 5 gives 49950. Close, but not the same.",
      W("5 × 9990 = 49950"), W("49950 ≠ 49990")),
    b("So the star is 7, and the difference is 69930.", A("69930")),
    b("The plan: find the two seats, test with a 1 to see the pattern, then look for the choice that fits."),
]

L["EXT_G4_FP_2022_011"] = [
    b("Here is 7,02,459. We swap the 5 and the 0, and then find the difference between the new number and the old one.",
      G("7,02,459: swap the 5 and the 0. Difference = ?"), FIG(chart("702459", [1, 4], note="Swap the two marked digits"))),
    b("After the swap, the 5 sits in the ten-thousands place and the 0 sits in the tens place. The new number is 7,52,409.",
      W("old: 7,02,459      new: 7,52,409")),
    b("Which number is bigger, the new one or the old one?",
      Q(["7,52,409", "7,02,459"],
        "Compare the ten-thousands digits. The new number has 5 there and the old one has 0, so the new number is bigger.")),
    b("Here is a quick way. Only two seats changed. The ten-thousands seat went from 0 up to 5, so the number gained 50000.",
      W("ten-thousands: 0 → 5    gain 50000")),
    b("But the tens seat went from 5 down to 0, so the number lost 50. That is the part people forget!",
      W("tens: 5 → 0    lose 50")),
    b("So the difference is 50000 minus 50, which is 49950.", W("50000 − 50 = 49950"), A("49950")),
    b("Check by subtracting the whole numbers. 7,52,409 minus 7,02,459 is 49950 as well.",
      W("7,52,409 − 7,02,459 = 49950")),
    b("So when two digits swap, just look at the seats that changed: what was gained, and what was lost."),
]

L["EXT_G4_FP_2022_012"] = [
    b("There are two jobs here. First find the greatest of these 5 numbers. Then find the place value of the 6 in it.",
      G("Greatest of 12764, 46749, 34296, 47659, 26947", name="g"), W("Place value of its 6 = ?")),
    b("All of them have 5 digits, so compare the first digits: 1, 4, 3, 4 and 2. The biggest is 4, and two numbers start with 4.",
      U("46749", on="g"), U("47659", on="g")),
    b("46749 or 47659: which one is greater?",
      Q(["47659", "46749"],
        "Both start with 4, so look at the next digit. 7 thousands is more than 6 thousands, so 47659 is greater.")),
    b("The thousands digit decides it, because 7 is more than 6. So 47659 is the greatest.",
      W("47659 > 46749"), FIG(chart("47659", [2], note="Where does the 6 sit?"))),
    b("Now find its 6. Counting from the right: 9 ones, 5 tens, 6 hundreds. The 6 is in the hundreds place."),
    b("So its place value is 6 times 100, which is 600.", W("6 × 100 = 600"), A("600")),
    b("Careful: the 6 sits in a different seat in each number. In 46749 it is worth 6000. That is why we find the greatest number first.",
      W("In 46749 the 6 is worth 6000")),
    b("So: first choose the number, then find the seat, then multiply."),
]

L["EXT_G4_FP_2022_016"] = [
    b("First we need the one-digit prime numbers. A prime number has exactly 2 factors: 1 and itself.",
      G("Greatest − smallest, using the one-digit primes once")),
    b("Which of these is the full list of one-digit primes?",
      Q(["2, 3, 5, 7", "1, 3, 5, 7", "3, 5, 7, 9"],
        "1 is not a prime, because it has only one factor. And 9 is 3 times 3. The one-digit primes are 2, 3, 5 and 7.")),
    b("So our digits are 2, 3, 5 and 7. Each is used once.", W("digits: 2, 3, 5, 7")),
    b("For the greatest number, put the biggest digit first and go down. That gives 7532.", W("greatest: 7532")),
    b("For the smallest number, put the smallest digit first and go up. That gives 2357.", W("smallest: 2357")),
    b("Now subtract 2357 from 7532. We have to borrow twice, in the ones and in the tens, so go slowly.",
      W("7532 − 2357 = 5175")),
    b("The difference is 5175.", A("5175")),
    b("Check by adding back: 5175 plus 2357 is 7532. It works.", W("5175 + 2357 = 7532")),
    b("Careful: 2357 is one of the choices, but that is only the smallest number. The question wants the difference."),
]

L["EXT_G4_FP_2022_029"] = [
    b("Two years, written in Roman numerals. To find how long the company ran, we turn both into our numbers, subtract, and turn the answer back.",
      G("Began MCDXLIX, closed MDCLXV. How long?")),
    b("The starting year, part by part: M is 1000, C D is 400, X L is 40 and I X is 9. That makes 1449.",
      FIG(table(["M", "CD", "XL", "IX"], [["1000", "400", "40", "9"]], note="The starting year, part by part")),
      W("1000 + 400 + 40 + 9 = 1449")),
    b("The closing year starts M, then D C. D is 500 and C is 100. What is D C worth?",
      W("D = 500     C = 100"),
      Q(["600", "400", "500"],
        "Here the bigger letter D comes first, so we add: 500 and 100 make 600. Only C D, the other way round, is 400.")),
    b("This is the trap in this question. C D is 400, but D C is 600. The order of the letters changes everything.",
      W("CD = 400     DC = 600")),
    b("So the closing year is 1000, 600, 60 and 5. That makes 1665.", W("1000 + 600 + 60 + 5 = 1665")),
    b("Now subtract. 1665 minus 1449 is 216 years.", W("1665 − 1449 = 216")),
    b("Back to Roman. 216 is 200, 10 and 6. That is C C, then X, then V I.", W("216 = 200 + 10 + 6"), A("CCXVI")),
    b("So the plan: read each numeral in parts, do the sum in our own numbers, then write the answer in Roman letters."),
]

L["EXT_G4_FP_2023_019"] = [
    b("Here are 4 numbers, and each has a 6 in it. We want the number where the 6 is worth the most.",
      G("In which number is the 6 worth the most?"), W("34562    3342654    4256402    75621")),
    b("What decides how much a 6 is worth?",
      Q(["the seat the 6 sits in", "how long the number is", "the first digit"],
        "A long number does not help the 6. Only its own seat matters, so count the places from the right until you reach the 6.")),
    b("Start with 34562. From the right: 2 ones, then 6 tens. This 6 is worth 60.",
      W("34562:  6 tens = 60"), FIG(chart("34562", [3], note="The 6 is in the tens place"))),
    b("Next, 3342654. From the right: 4 ones, 5 tens, 6 hundreds. This 6 is worth 600.", W("3342654:  6 hundreds = 600")),
    b("Now 4256402. From the right: 2 ones, 0 tens, 4 hundreds, 6 thousands. This 6 is worth 6000.",
      W("4256402:  6 thousands = 6000"), FIG(chart("4256402", [3], note="The 6 is in the thousands place"))),
    b("Last, 75621. From the right: 1 one, 2 tens, 6 hundreds. Worth 600 again.", W("75621:  6 hundreds = 600")),
    b("6000 is the greatest of the four. So the number is 4256402.", A("4256402")),
    b("Did you spot the trap? 3342654 is just as long, but its 6 hides near the end. Check the seat, not the size of the number."),
]

L["EXT_G4_FP_2024_004"] = [
    b("In 768459 we compare two digits, the 4 and the 5. How many times the value of the 5 is the value of the 4?",
      G("768459: (value of 4) is ? times (value of 5)"), FIG(chart("768459", [3, 4], note="Compare the 4 and the 5"))),
    b("Count from the right: 9 ones, 5 tens, 4 hundreds. So what is the 4 worth?",
      Q(["400", "40", "4000"], "9 is in the ones, 5 is in the tens and 4 is in the hundreds. 4 hundreds is 400.")),
    b("4 hundreds is 400. And the 5 is in the tens, so it is worth 50.", W("4 × 100 = 400"), W("5 × 10 = 50")),
    b("How many times means: how many lots of 50 fit into 400? So we divide.", W("400 ÷ 50 = ?")),
    b("Cross off one zero from each, and we have 40 divided by 5. That is 8.", W("400 ÷ 50 = 40 ÷ 5"), W("40 ÷ 5 = 8")),
    b("So the 4 is worth 8 times as much as the 5.", A("8")),
    b("Careful: the hundreds seat is 10 times the tens seat, so 10 looks tempting. But the digits are different, so we must use 400 and 50."),
    b("Check: 50 times 8 is 400. It works.", W("50 × 8 = 400")),
]

L["EXT_G4_FP_2024_009"] = [
    b("Three small jobs hide in this question. Find two special numbers, add them, and then look for the 9 in the total.",
      G("Greatest 4-digit number + greatest 2-digit prime")),
    b("The greatest 4-digit number is easy. Fill every seat with a 9, and we get 9999.", W("greatest 4-digit number: 9999")),
    b("Now the greatest 2-digit prime. Which of these is it?",
      Q(["97", "99", "98"],
        "99 can be divided by 3, and 98 can be divided by 2, so they are not prime. 97 cannot be divided by anything except 1 and itself.")),
    b("Start at 99 and walk down. 99 is 3 times 33. 98 is 2 times 49. 97 passes every test, so 97 is our prime.",
      W("99 = 3 × 33"), W("98 = 2 × 49"), W("greatest 2-digit prime: 97")),
    b("Now add. 9999 is just 1 less than 10000. So add 97 to 10000 and take 1 away. We get 10096.",
      W("10000 + 97 − 1 = 10096"), W("9999 + 97 = 10096")),
    b("Here is the trap. The question is not about the 9s we started with. We must look for the 9 in the total, 10096.",
      FIG(chart("10096", [3], note="Where is the 9 now?"))),
    b("In 10096, count from the right: 6 ones, then 9 tens. So the 9 is worth 9 times 10, which is 90.",
      W("9 × 10 = 90"), A("90")),
    b("So: do every job in order, and only then answer the question that was asked."),
]

L["EXT_G4_FP_2025_002"] = [
    b("There are 7 Roman letters: I, V, X, L, C, D and M. We use each one once, to make the greatest number and the smallest number.",
      G("All 7 Roman letters once: greatest − smallest"), FIG(LETTERS)),
    b("For the greatest, write the letters from biggest to smallest. Then every letter is added, and we get 1666.",
      W("MDCLXVI"), W("1000 + 500 + 100 + 50 + 10 + 5 + 1 = 1666")),
    b("For the smallest, we want letters that take away instead of add. When does a Roman letter take away?",
      Q(["when it stands before a bigger letter", "when it stands after a bigger letter", "when it is written twice"],
        "A smaller letter in front of a bigger one is taken away, like I V for 4. So we put small letters in front where the rules allow.")),
    b("M has to stay in front. After it we make pairs with the smaller letter first: C D, X L and I V.", W("MCDXLIV")),
    b("C D is 400, X L is 40 and I V is 4. With the 1000 in front, that makes 1444.", W("1000 + 400 + 40 + 4 = 1444")),
    b("Here is the trap: the smallest number is not just the letters turned around. I V X L C D M is not a proper numeral at all."),
    b("Now subtract. 1666 minus 1444 is 222.", W("1666 − 1444 = 222")),
    b("222 is 200, 20 and 2. In Roman letters that is C C, then X X, then I I.", W("222 = 200 + 20 + 2"), A("CCXXII")),
    b("So remember: biggest letters first to add, and a small letter in front to take away."),
]

L["EXT_G4_FP_2025_018"] = [
    b("Here is 86352. We swap its 6 and its 5, and then find the difference between the two numbers.",
      G("86352: swap the 6 and the 5. Difference = ?"), FIG(chart("86352", [1, 3], note="Swap the two marked digits"))),
    b("The 6 is in the thousands place and the 5 is in the tens place. Swap them, and the new number is 85362.",
      W("old: 86352      new: 85362")),
    b("Which number is bigger now?",
      Q(["86352, the old one", "85362, the new one"],
        "Look at the thousands digit. The old number has 6 thousands and the new one has only 5, so the old number is bigger.")),
    b("Only two seats changed. The thousands seat dropped from 6 to 5, so the number lost 1000.",
      W("thousands: 6 → 5    lose 1000")),
    b("But the tens seat rose from 5 to 6, so it gained 10 back.", W("tens: 5 → 6    gain 10")),
    b("So the two numbers are 1000 minus 10 apart. That is 990.", W("1000 − 10 = 990"), A("990")),
    b("Check by subtracting the whole numbers. 86352 minus 85362 is 990 as well.", W("86352 − 85362 = 990")),
    b("So when two digits swap, look only at the seats that changed: what was lost, and what was gained."),
]

L["EXT_G4_FP_2025_036"] = [
    b("Find two numbers, subtract them, and then write the answer in Roman numerals. One job at a time.",
      G("Greatest 3-digit even − smallest 3-digit odd, in Roman")),
    b("The greatest 3-digit number is 999, but that is odd. So what is the greatest 3-digit even number?",
      W("greatest 3-digit number: 999"),
      Q(["998", "990", "1000"], "Step down just one from 999. 998 ends in 8, so it is even, and it still has 3 digits.")),
    b("998 it is. The smallest 3-digit number is 100, but that is even. One step up gives the smallest odd one, 101.",
      W("greatest even: 998"), W("smallest 3-digit number: 100"), W("smallest odd: 101")),
    b("This is where slips happen. If we forget the words even and odd, we use 999 and 100, and the answer goes astray."),
    b("Now subtract. 998 minus 101 is 897.", W("998 − 101 = 897")),
    b("Time for Roman letters. Split 897 into 800, 90 and 7.", W("897 = 800 + 90 + 7"), FIG(LETTERS)),
    b("800 is D for 500, and three Cs. 90 is 10 less than 100, so X C. And 7 is V I I.",
      W("800 = DCCC     90 = XC     7 = VII")),
    b("Join them in order: D C C C, then X C, then V I I.", A("DCCCXCVII")),
    b("So: read the words carefully, do the sum in our own numbers, and change to Roman letters at the very end."),
]
