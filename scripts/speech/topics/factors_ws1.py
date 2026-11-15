"""Hand-written narration for factors worksheet questions, part 1 (EXT_G5_WS_B3_016 to B4_010).

The missing digit, printed as an asterisk sign, is said as "star". Where the checker reads the
printed digits around it as one number ("7*14" is 7 then 14), the narration has to keep them so.
Plain-prose lines that need no help are left to the general converter.
"""

HAND = {
    "EXT_G5_WS_B3_016": {
        "q": "The greatest three-digit number that is completely divisible by 57 is what?",
        "h0": "You want the biggest multiple of 57 that still has three digits. The biggest three-digit number is 999, so see how many 57s fit into 999.",
        "h1": "57 times 10 is 570, and 57 times 20 is 1140, which is too big. So try multiples in between, like 57 times 17, and 57 times 18, and pick the largest one that stays below 1000.",
        "h2": "Example: the greatest two-digit number divisible by 23. 23 times 4 is 92, and 23 times 5 is 115, which has three digits. So it is 92.",
        "s0": "The answer must be a multiple of 57 that is no bigger than 999. 57 times 10 is 570, so try larger multiples.",
        "s1": "57 times 17 is 969, and 57 times 18 is 1026. 1026 has four digits, so it is too big.",
    },
    "EXT_G5_WS_B3_017": {
        "q": "The smallest four-digit number that is exactly divisible by 57 is what?",
        "h0": "You want the first multiple of 57 that reaches four digits. The smallest four-digit number is 1000, so find the first multiple of 57 that is 1000 or more.",
        "h1": "57 times 10 is 570, and 57 times 20 is 1140. The one you want lies between these. Try 57 times 17, then 57 times 18, and stop at the first one that passes 999.",
        "h2": "Example: the smallest three-digit number divisible by 23. 23 times 4 is 92, which has two digits, and 23 times 5 is 115, which has three. So it is 115.",
        "s0": "The answer is the first multiple of 57 that is 1000 or more. 57 times 10 is 570, so try larger multiples.",
        "s1": "57 times 17 is 969, which has only three digits. The next multiple is 57 times 18, which is 1026.",
    },
    "EXT_G5_WS_B3_022": {
        "h1": "Multiply the two known numbers: 12 times 15 is 180. Now work out how many 180s make 2880.",
        "h2": "Example: the product of three numbers is 60, and two of them are 3 and 4. 3 times 4 is 12, and 60 divided by 12 is 5, so the third number is 5.",
        "s0": "12 times 15 is 180.",
        "s1": "The third is 2880 divided by 180, which is 16.",
    },
    "EXT_G5_WS_B3_027": {
        "h1": "Take the extra 9 away from the sum: 153 minus 9 is 144. That leaves two equal numbers, each the same as the smaller multiple. Halve 144, then add 9 for the larger one.",
        "h2": "Example: two consecutive multiples of 5 add up to 35. 35 minus 5 is 30, and 30 divided by 2 is 15. So the multiples are 15 and 20, and the larger is 20.",
        "s0": "Consecutive multiples of 9 differ by 9. Take that extra 9 away from the sum: 153 minus 9 is 144.",
        "s1": "Now the two parts are equal, so the smaller multiple is 144 divided by 2, which is 72.",
        "s2": "The larger multiple is 72 plus 9, which is 81. Check: 72 plus 81 is 153. So the larger multiple is 81.",
    },
    "EXT_G5_WS_B4_001": {
        "q": "7, star, 14 is a four-digit multiple of 3. Which digit can replace the asterisk?",
        "h1": "Add the digits you know: 7 plus 1 plus 4 is 12. Now add each choice to 12 in turn, and see whether the total is in the 3 times table.",
        "h2": "Try a smaller one: 2, star, 4. With star as 3, the digit sum is 2 plus 3 plus 4, which is 9, a multiple of 3, so 234 works. With star as 5, the sum is 11, so 254 does not work. Test every choice this way.",
        "s0": "A number is a multiple of 3 when its digits add up to a multiple of 3. The known digits add up to 7 plus 1 plus 4, which is 12.",
        "s1": "With 6, the total is 12 plus 6, which is 18. With 9, it is 12 plus 9, which is 21. With 0, it is 12 plus 0, which is 12.",
        "s2": "18, 21 and 12 are all multiples of 3, so 7614, 7914 and 7014 are all multiples of 3.",
    },
    "EXT_G5_WS_B4_002": {
        "q": "In the number 5, star, star, the digits in place of the asterisks are the same. If this number is divisible by 3, which is the largest digit that can replace the asterisk?",
        "h1": "The digit sum is 5 plus star plus star. You want the largest digit, so test the biggest choice first. With 9, the sum is 5 plus 9 plus 9, which is 23. Is 23 a multiple of 3? If not, try the next biggest choice.",
        "h2": "Try a smaller one: 4, star, star. With star as 7, the digit sum is 4 plus 7 plus 7, which is 18, a multiple of 3, so 477 is divisible by 3.",
        "s0": "For 5, star, star to be divisible by 3, the digit sum, 5 plus star plus star, must be a multiple of 3.",
        "s1": "Test the biggest choice first. With 9: 5 plus 9 plus 9 is 23, which is not a multiple of 3.",
        "s2": "With 8: 5 plus 8 plus 8 is 21, and 21 is 3 times 7, so 588 is divisible by 3.",
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
        "h1": "You do not need the whole product. Multiply the last digits, 7 times 8, to find the digit the product ends in. Then count up to the next number ending in 0 or 5.",
        "h2": "Try a smaller one: 13 times 14 ends in 2, because 3 times 4 is 12. The next number ending in 0 or 5 ends in 5, which is 3 more. So the least number to add there is 3.",
        "s0": "For the units digit of the product: 7 times 8 is 56, so the product ends in 6.",
        "s1": "For the next number ending in 0 or 5, we need to add 4, for an ending of 0, or 9, for an ending of 5.",
        "s2": "The least number to add is 4.",
    },
    "EXT_G5_WS_B4_006": {
        "h1": "Multiply just the last digits: 9 times 7 is 63, so the product ends in the same digit as 63. What must you take away to make it end in 0? Check that your number is among the choices.",
        "h2": "Try a smaller one: 23 times 17 ends in 1, because 3 times 7 is 21. Take away 1, and the number ends in 0, so it is divisible by 5.",
        "s0": "A number is divisible by 5 when it ends in 0 or 5. The last digit of 169 times 47 comes from 9 times 7, which is 63, so the product ends in 3.",
        "s2": "Check: 169 times 47 is 7943, and 7943 minus 3 is 7940, which ends in 0.",
    },
    "EXT_G5_WS_B4_007": {
        "q": "A three-digit number, star, 96, is completely divisible by 7. Find the digit in place of the asterisk.",
        "h1": "Start with 7: is 796 a multiple of 7? 7 times 100 is 700, which leaves 96, and 96 is not a multiple of 7, because 7 times 13 is 91, and 7 times 14 is 98. So 796 does not work. Test the other digits the same way.",
        "h2": "Try a smaller one: is 342 divisible by 7? 7 times 40 is 280, which leaves 62, and 7 times 8 is 56, which leaves 6 over. So 342 is not divisible by 7.",
        "s1": "796 is 7 times 113, plus 5. And 696 is 7 times 99, plus 3. So the digits 7 and 6 both leave a remainder.",
        "s2": "396 is 7 times 56, plus 4, so the digit 3 leaves a remainder too.",
        "s3": "896 is 7 times 128 exactly, with nothing left over.",
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
        "h1": "Multiply just the last digits: 7 times 8 is 56. The product ends in the same digit as 56. What must you take away so that it ends in 0?",
        "h2": "Try a smaller one: 13 times 19 ends in 7, because 3 times 9 is 27. Take away 7, and the number ends in 0, so it is divisible by 10.",
        "s0": "A number is divisible by 10 when it ends in 0. The last digit of 97 times 238 comes from 7 times 8, which is 56, so the product ends in 6.",
        "s2": "Check: 97 times 238 is 23086, and 23086 minus 6 is 23080, which ends in 0.",
    },
}
