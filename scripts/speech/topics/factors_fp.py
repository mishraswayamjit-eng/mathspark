"""Hand-written narration for the factors past-paper questions (EXT_G5_FP_...).

Keys: 'q' the question, 'o' the four options, 'h0'..'h2' hints, 's0'.. steps. Anything left
out is narrated by factors_rules.say. Times on the hour stay as '10:00' because the checker
needs both numbers of the printed time.
"""

PRODUCT_RULE = "H C F times L C M equals the first number times the second number."
PRODUCT_RULE_L = "L C M times H C F equals the first number times the second number."

HAND = {
    "EXT_G5_FP_2016_011": {
        "q": "Which of the following is the H C F of 18, 24 and 36?",
        "h0": "The H C F is the greatest number that divides all three numbers exactly. Test the options on 18 first, then check them on 24 and 36.",
        "h1": "H C F means the biggest common factor. Use prime factors. 18 is 2 times 3 times 3. 24 is 2 times 2 times 2 times 3. 36 is 2 times 2 times 3 times 3.",
        "s0": "The factors of 18 are 1, 2, 3, 6, 9 and 18.",
        "s1": "The factors of 24 are 1, 2, 3, 4, 6, 8, 12 and 24.",
        "s2": "The factors of 36 are 1, 2, 3, 4, 6, 9, 12, 18 and 36.",
        "s3": "The common factors are 1, 2, 3 and 6. The greatest is 6.",
    },
    "EXT_G5_FP_2016_016": {
        "h1": "The count of multiples of L, up to N, equals N divided by L. Take the whole part only.",
        "s0": "The L C M of 4 and 6 is 12.",
        "s1": "Numbers below 2009 means up to 2008.",
        "s2": "2008 divided by 12 is 167.3 and so on, so there are 167 numbers.",
    },
    "EXT_G5_FP_2017_013": {
        "h1": "The L C M of 2, 3 and 4 is 12. List the multiples of 12 between 10 and 99.",
        "s0": "The L C M of 2, 3 and 4 is 12.",
        "s1": "The two-digit multiples of 12 are 12, 24, 36, 48, 60, 72, 84 and 96.",
        "s2": "The count is 8.",
    },
    "EXT_G5_FP_2017_027": {
        "q": "Dog A barks every 5 minutes, Dog B barks every 8 minutes, and Dog C barks every 12 minutes. They started barking at 11 30 p m, and continued barking the whole night. Later that night, Mister John woke up when the three dogs barked at the same time, making a very loud noise. What time did Mister John wake up?",
        "o": ["1:00 a m", "1 30 p m", "1 30 a m", "2 30 p m"],
        "h0": "They bark together again after the L C M of 5, 8 and 12 minutes. Then add that time to 11 30 p m.",
        "h1": "The L C M tells when repeating events happen together again.",
        "s0": "The L C M of 5, 8 and 12 is 120 minutes, which is 2 hours.",
        "s1": "11 30 p m, plus 2 hours, is 1 30 a m.",
    },
    "EXT_G5_FP_2018_024": {
        "q": "Find the H C F of 54, 288 and 360.",
        "h1": "Or break each number into prime factors. 54 equals 2, times 3 times 3 times 3. Do the same for 288 and 360, then pick out the primes that all three share.",
        "h2": "Try a smaller one. 12 is 2 times 2, times 3. 20 is 2 times 2, times 5. And 28 is 2 times 2, times 7. All three share 2 times 2, so their H C F is 4.",
        "s0": "54 equals 2, times 3 times 3 times 3.",
        "s1": "288 equals 2 times 2 times 2 times 2 times 2, times 3 times 3.",
        "s2": "360 equals 2 times 2 times 2, times 3 times 3, times 5.",
        "s3": "In common, they have one 2 and two 3s. That gives 2 times 9, which is 18.",
    },
    "EXT_G5_FP_2018_040": {
        "h0": "If the remainder is 5, then 167 minus 5, and 95 minus 5, are exactly divisible by the number. Find their H C F. And the divisor must be bigger than 5.",
        "s0": "The number leaves remainder 5, so it divides 167 minus 5, which is 162, and 95 minus 5, which is 90, exactly.",
        "s1": "The largest number that divides both is their H C F. 162 is 18 times 9, and 90 is 18 times 5. And 9 and 5 share no factor, so the H C F is 18.",
        "s2": "A divisor must be bigger than its remainder, and 18 is bigger than 5. Check: 18 times 9, plus 5, is 167. And 18 times 5, plus 5, is 95.",
    },
    "EXT_G5_FP_2019_017": {
        "h0": "Find the L C M of 4, 5 and 6. Then list the three-digit multiples of it. The first is 120.",
        "h1": "Numbers divisible by all three are multiples of the L C M.",
        "s0": "The L C M of 4, 5 and 6 is 60.",
        "s1": "Look at the 3 digit multiples. The first is 60 times 2, which is 120. The last is 60 times 16, which is 960.",
        "s2": "From 2 to 16, that is 16 minus 2, plus 1, which makes 15 numbers.",
    },
    "EXT_G5_FP_2019_033": {
        "q": "The H C F of 513 and 456 is what?",
        "h0": "A number that divides both 513 and 456 also divides their difference. So start by subtracting.",
        "h1": "Work out 513 minus 456. The H C F must be a factor of that difference. Test the difference itself first: does it divide both numbers exactly?",
        "h2": "Try a smaller one. For 35 and 28, the difference is 7. 7 divides both 35 and 28 exactly, so their H C F is 7.",
        "s0": "513 minus 456 is 57.",
        "s1": "513 divided by 57 is 9, and 456 divided by 57 is 8. Both are exact.",
        "s2": "The H C F is 57.",
    },
    "EXT_G5_FP_2020_017": {
        "q": "Three electronic bells beep after every 2, 5 and 8 minutes. If they all beeped together at 10:00 a m, when will they beep together the next time?",
        "o": ["10 40 a m", "10 32 a m", "10 30 a m", "11 20 a m"],
        "h0": "They beep together again after the L C M of 2, 5 and 8 minutes. Add that to 10:00 a m.",
        "h1": "The L C M tells when repeating events coincide.",
        "s0": "The L C M of 2, 5 and 8 is 40 minutes.",
        "s1": "10:00 a m, plus 40 minutes, is 10 40 a m.",
    },
    "EXT_G5_FP_2020_029": {
        "q": "The H C F of 513, 1134 and 1215 is what?",
        "h1": "The digits of each number add up to 9, so each one can be divided by 3, and then by 3 again. Count how many 3s each number contains.",
        "h2": "Try a smaller one. 36 is 2 times 2, times 3 times 3. And 45 is 3 times 3, times 5. They share 3 times 3, so their H C F is 9.",
        "s0": "Break each number into prime factors. 513 equals 3 times 3 times 3, times 19. And 1134 equals 2, times 3 times 3 times 3 times 3, times 7.",
        "s1": "And 1215 equals 3 times 3 times 3 times 3 times 3, times 5.",
        "s2": "The only prime in all three is 3, and each number has at least three 3s. 3 times 3 times 3 is 27.",
    },
    "EXT_G5_FP_2021_039": {
        "q": "The least number which, when divided by 12, 15, 20 and 54, leaves in each case a remainder of 8.",
        "h0": "A number that leaves the same remainder with all divisors is: the L C M of the divisors, plus the remainder.",
        "h1": "The least number equals the L C M plus the remainder.",
        "s0": "A number that leaves remainder 8 every time is 8 more than a common multiple of 12, 15, 20 and 54. The least such number uses their L C M.",
        "s1": "The prime factors: 12 is 2 times 2, times 3. 15 is 3 times 5. 20 is 2 times 2, times 5. And 54 is 2, times 3 times 3 times 3.",
        "s2": "Take each prime the most times it appears in any one number. 2 times 2, times 3 times 3 times 3, times 5, equals 540. So the L C M is 540.",
    },
    "EXT_G5_FP_2022_019": {
        "h0": "H C F times L C M equals the product of the two numbers. Multiply 13 and 1989, then divide by 221.",
        "h1": PRODUCT_RULE,
        "s0": "13 times 1989 is 25857.",
        "s1": "The other number is 25857 divided by 221, which is 117.",
        "s2": "Check: 221 times 117 is 25857. Correct.",
    },
    "EXT_G5_FP_2022_039": {
        "q": "What is the sum of the L C M and the H C F of 12 and 90?",
        "h0": "Find the H C F, the biggest number that divides both, and the L C M, the smallest number both divide into. Then add them.",
        "h1": "Break both into prime factors. 12 is 2 times 2, times 3. And 90 is 2, times 3 times 3, times 5. The H C F uses the primes they share. The L C M uses each prime the most times it appears.",
        "h2": "Try a smaller one. 4 is 2 times 2, and 6 is 2 times 3. The H C F is 2, and the L C M is 2 times 2 times 3, which is 12. So the sum is 12 plus 2, which is 14.",
        "s0": "The H C F is 2 times 3, which is 6.",
        "s1": "The L C M is 2 squared, times 3 squared, times 5, which is 180.",
        "s2": "The sum is 180 plus 6, which is 186.",
    },
    "EXT_G5_FP_2023_006": {
        "q": "What is the difference of the L C M and the H C F of 48 and 120?",
        "h0": "Find the H C F, the biggest common factor, and the L C M, the smallest common multiple. Then subtract: L C M minus H C F.",
        "h1": "48 is 2 to the power of four, times 3. And 120 is 2 cubed, times 3, times 5. H C F times L C M equals 48 times 120.",
        "s0": "The H C F is 2 cubed times 3, which is 24.",
        "s1": "The L C M is 2 to the power of four, times 3, times 5, which is 240.",
        "s2": "The difference is 240 minus 24, which is 216.",
    },
    "EXT_G5_FP_2023_029": {
        "h0": "L C M times H C F equals the product of the two numbers. Multiply 882 and 14, then divide by 98.",
        "h1": "L C M times H C F equals the first times the second.",
        "s0": "882 times 14 is 12348.",
        "s1": "The other number is 12348 divided by 98, which is 126.",
    },
    "EXT_G5_FP_2024_013": {
        "h1": "The count of multiples of L, up to N, equals N divided by L. Ignore the remainder.",
        "s0": "The L C M of 6 and 9 is 18.",
        "s1": "Numbers below 3009 means up to 3008.",
        "s2": "3008 divided by 18 is 167.1 and so on, so the whole number part is 167.",
    },
    "EXT_G5_FP_2024_032": {
        "q": "The L C M and H C F of two numbers are 168 and 7 respectively. One of the numbers is 56. Find the square of the other number.",
        "h0": "Multiply the L C M and the H C F. This equals the product of the two numbers. Then divide by the number you know.",
        "h1": PRODUCT_RULE_L,
        "s0": "168 times 7 is 1176.",
        "s1": "The other number is 1176 divided by 56, which is 21.",
        "s2": "The square is 21 times 21, which is 441.",
    },
    "EXT_G5_FP_2025_009": {
        "h0": "Find the L C M of 5, 2 and 8. A number divisible by all three is a multiple of it. Then list the three-digit multiples.",
        "h1": "To count the multiples between two numbers: divide the last one by the L C M, then subtract the number of multiples below the range.",
        "s0": "The L C M of 5, 2 and 8 is 40.",
        "s1": "The smallest 3 digit multiple of 40 is 120, which is 40 times 3. The largest is 960, which is 40 times 24.",
        "s2": "The multiples run from 40 times 3, up to 40 times 24. So that is 24 minus 3, plus 1, which is 22.",
    },
    "EXT_G5_FP_2025_016": {
        "q": "The L C M and H C F of two numbers are 672 and 12 respectively. If one of the numbers is 84, find the other number.",
        "h0": "L C M times H C F equals the product of the two numbers. Multiply 672 and 12, then divide by 84.",
        "h1": PRODUCT_RULE_L,
        "s0": "672 times 12 is 8064.",
        "s1": "The other number is 8064 divided by 84, which is 96.",
    },
}
