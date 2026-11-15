"""Hand-written narration for factors worksheet questions, part 1 (EXT_G5_WS_B3_016 to B4_010).

The missing digit, printed as an asterisk sign, is said as "star". Where the checker reads the
printed digits around it as one number ("7*14" is 7 then 14), the narration has to keep them so.
"""

HAND = {
    "EXT_G5_WS_B3_016": {
        "q": "The greatest three-digit number that is completely divisible by 57 is what?",
        "h0": "Find the largest 3 digit multiple of 57.",
        "h1": "999 divided by 57 is 17.5 and so on. So 17 times 57 is 969. Check: 18 times 57 is 1026, which has 4 digits. So it is 969.",
        "s0": "999 divided by 57 is 17.5 and so on, so the largest whole multiple is 17.",
        "s1": "17 times 57 is 969.",
    },
    "EXT_G5_WS_B3_017": {
        "q": "The smallest four-digit number that is exactly divisible by 57 is what?",
        "h0": "Find the smallest 4 digit multiple of 57.",
        "h1": "1000 divided by 57 is 17.5 and so on, so the ceiling is 18. 18 times 57 is 1026.",
        "s0": "1000 divided by 57 is 17.5 and so on. Round up to 18.",
        "s1": "18 times 57 is 1026.",
    },
    "EXT_G5_WS_B3_022": {
        "h0": "The product is 2880. Two numbers are 12 and 15. The third is 2880, divided by the product of 12 and 15.",
        "h1": "12 times 15 is 180. The third is 2880 divided by 180, which is 16.",
        "h2": "Try this: the product is 60, and two numbers are 3 and 4. The third is 60 divided by 12, which is 5.",
        "s0": "12 times 15 is 180.",
        "s1": "The third is 2880 divided by 180, which is 16.",
    },
    "EXT_G5_WS_B3_027": {
        "h0": "Let the multiples be 9 k, and 9 times, open bracket, k plus 1, close bracket. Their sum is 9 k plus 9 k plus 9, which is 18 k plus 9, and that equals 153.",
        "h1": "18 k equals 144, so k equals 8. The multiples are 72 and 81.",
        "h2": "Try consecutive multiples of 5 that add up to 25. 5 k, plus 5 times, open bracket, k plus 1, close bracket, is 10 k plus 5, which equals 25. So k equals 2. The numbers are 10 and 15.",
        "s0": "9 k, plus 9 times, open bracket, k plus 1, close bracket, equals 153.",
        "s1": "18 k plus 9 equals 153, so k equals 8.",
        "s2": "The multiples are 72 and 81. The larger is 81.",
    },
    "EXT_G5_WS_B4_001": {
        "q": "7, star, 14 is a four-digit multiple of 3. Which digit can replace the asterisk?",
        "h1": "Add up the digits: 7 plus star plus 1 plus 4, which is 12 plus star. Which values of star make this divisible by 3?",
        "h2": "Try a simpler one. Is 3, blank, 6 divisible by 3? The digit sum is 9 plus star. If star is 0, we get 9, which works. If star is 3, we get 12, which works. If star is 6, we get 15, which works. If star is 9, we get 18, which works.",
        "s0": "The sum of the digits is 7 plus star plus 1 plus 4, which is 12 plus star.",
        "s1": "For divisibility by 3, 12 plus star must be a multiple of 3.",
        "s2": "Since 12 is already divisible by 3, star must also be divisible by 3. So star is 0, 3, 6, or 9.",
        "s3": "All three given options, 6, 9 and 0, work!",
    },
    "EXT_G5_WS_B4_002": {
        "q": "In the number 5, star, star, the digits in place of the asterisks are the same. If this number is divisible by 3, which is the largest digit that can replace the asterisk?",
        "h1": "The digit sum is 5 plus star plus star, which is 5 plus 2 times star. This must be divisible by 3. Try star as 0, 1, 2, and so on, up to 9.",
        "h2": "A similar one: is 7, blank, blank, 7 divisible by 3, with the same digit in both blanks? The sum is 14 plus 2 times star. Star as 2 gives 18, which works. Star as 5 gives 24, which works. Star as 8 gives 30, which works. The largest is 8.",
        "s0": "The digit sum is 5 plus 2 times star.",
        "s1": "For divisibility by 3, 5 plus 2 times star must leave remainder 0 when divided by 3. Test some values.",
        "s2": "Star as 2 gives 9, which works. Star as 5 gives 15, which works. Star as 8 gives 21, which works. Star as 9 gives 23, which does not work.",
        "s3": "The largest valid digit is 8.",
    },
    "EXT_G5_WS_B4_003": {
        "h0": "Between 60 and 100 usually means 61 to 99, not including 60 and 100 themselves.",
        "h1": "The multiples of 3 in this range start at 63, which is 3 times 21, and end at 99, which is 3 times 33.",
        "h2": "A similar one: how many multiples of 5 are between 10 and 40? The first is 15, and the last is 35. The count is 35 minus 15, divided by 5, plus 1, which is 5.",
        "s0": "The first multiple of 3 after 60 is 63, which is 3 times 21.",
        "s1": "The last multiple of 3 before 100 is 99, which is 3 times 33.",
        "s2": "The count is 33 minus 21, plus 1, which is 13.",
    },
    "EXT_G5_WS_B4_004": {
        "h1": "The first two-digit multiple of 4 is 12, which is 4 times 3. The last is 96, which is 4 times 24.",
        "h2": "A similar one: how many two-digit multiples of 5 are there? The first is 10, which is 5 times 2. The last is 95, which is 5 times 19. The count is 19 minus 2, plus 1, which is 18.",
        "s0": "The first two-digit multiple of 4 is 12, which is 4 times 3.",
        "s1": "The last two-digit multiple of 4 is 96, which is 4 times 24.",
        "s2": "The count is 24 minus 3, plus 1, which is 22.",
    },
    "EXT_G5_WS_B4_005": {
        "h1": "For the units digit of 527 times 308, just look at 7 times 8, which is 56. So the product ends in 6. To reach 0 or 5, add 4, to get a number ending in 0, or add 9, to get a number ending in 5. The least is 4.",
        "h2": "A similar one: 13 times 14 is 182. It ends in 2. To be divisible by 5, add 3, to get 185, or add 8, to get 190. The least is 3.",
        "s0": "For the units digit of the product: 7 times 8 is 56, so the product ends in 6.",
        "s1": "For the next number ending in 0 or 5, we need to add 4, for an ending of 0, or 9, for an ending of 5.",
        "s2": "The least number to add is 4.",
    },
    "EXT_G5_WS_B4_006": {
        "h0": "Similar to question 5. Find what the product ends in, then figure out what to subtract to make it end in 0 or 5.",
        "h1": "Units: 9 times 7 is 63, so the product ends in 3. Subtract 3 to get an ending of 0, or subtract 8 to get an ending of 5.",
        "h2": "Try this: 23 times 17 is 391, which ends in 1. Subtract 1 to get 390, and that divided by 5 is 78. It works.",
        "s0": "Units digit: 9 times 7 is 63, so the product ends in 3.",
        "s1": "Subtract 3. An ending of 3, minus 3, gives an ending of 0, which is divisible by 5.",
        "s2": "169 times 47 is 7943. And 7943 minus 3 is 7940, which is 5 times 1588. Correct.",
    },
    "EXT_G5_WS_B4_007": {
        "q": "A three-digit number, star, 96, is completely divisible by 7. Find the digit in place of the asterisk.",
        "h1": "Test each one. 796 divided by 7 is 113.7 and so on, not a whole number. 896 divided by 7 is 128, a whole number. 696 divided by 7 is 99.4 and so on, not a whole number. 396 divided by 7 is 56.6 and so on, not a whole number.",
        "h2": "A similar one: find star, if star, 42 is divisible by 7. Test: 742 divided by 7 is 106, which works. So star is 7.",
        "s0": "Test each option by putting it into star, 96.",
        "s1": "Option A, which is 7: 796 divided by 7 is 113.71 and so on. That does not work.",
        "s2": "Option B, which is 8: 896 divided by 7 is 128. That works.",
        "s3": "The answer: star is 8.",
    },
    "EXT_G5_WS_B4_009": {
        "q": "The number 7, star, star, 5 leaves no remainder when divided by 9. The digits in place of the asterisks are the same. Which is the smallest digit that can replace the star?",
        "h1": "The digit sum is 7 plus star plus star plus 5, which is 12 plus 2 times star. Find the smallest star, from 0 to 9, where 12 plus 2 times star is divisible by 9.",
        "h2": "A similar one: 4, star, star, 1 is divisible by 9. The sum is 5 plus 2 times star. Star as 2 gives 9, which works, and it is the smallest.",
        "s0": "The digit sum is 7 plus star plus star plus 5, which is 12 plus 2 times star.",
        "s1": "We need 12 plus 2 times star to be divisible by 9. Try some values.",
        "s2": "Star as 0 gives 12, no. Star as 1 gives 14, no. Star as 2 gives 16, no. Star as 3 gives 18, which is 9 times 2, yes.",
        "s3": "The smallest star is 3.",
    },
    "EXT_G5_WS_B4_010": {
        "h1": "Find what the product ends in. For the units of 97 times 238, look at 7 times 8, which is 56. So the product ends in 6. Subtract 6.",
        "h2": "A similar one: 13 times 19 is 247. It ends in 7. Subtract 7 to get 240, and that divided by 10 is 24. It works.",
        "s0": "Units digit of the product: 7 times 8 is 56, so the product ends in 6.",
        "s2": "97 times 238 is 23086. And 23086 minus 6 is 23080.",
    },
}
