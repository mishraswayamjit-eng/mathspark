"""Hand-written narration for factors worksheet questions, part 2 (EXT_G5_WS_B4_011 to B5_019).

Lists printed without spaces ("22,23,25,27") are read out as ordinary lists. Plain-prose
lines that need no help are left to the general converter.
"""

RULE_TAIL = ("add the 1st and 3rd digits, then add the 2nd and 4th digits. "
             "The number is a multiple of 11 when the two totals are equal, or differ by 11.")
RULE_11 = "make two totals: " + RULE_TAIL

HAND = {
    "EXT_G5_WS_B4_011": {
        "q": "Find the digit at the star, if 56, star, 8 is a four-digit multiple of 11.",
        "h0": "For 11, " + RULE_11,
        "h1": "In 56, star, 8, the 2nd and 4th digits give 6 plus 8, which is 14. The 1st and 3rd digits give 5 plus star. Which digit makes the two totals match?",
        "h2": "Try a smaller one: 2, star, 53. The 2nd and 4th digits give star plus 3, and the 1st and 3rd give 2 plus 5, which is 7. They match when star is 4, and 2453 is 11 times 223.",
        "s0": "The rule for 11: " + RULE_TAIL,
        "s1": "In 56, star, 8, the 2nd and 4th digits give 6 plus 8, which is 14, and the 1st and 3rd digits give 5 plus star.",
        "s2": "The totals match when 5 plus star is 14, so star is 9. No single digit could make the totals differ by 11.",
        "s3": "Check: 5698 is 11 times 518. So the digit is 9.",
    },
    "EXT_G5_WS_B4_012": {
        "q": "The number star, 5, star, 0 is completely divisible by 11. The asterisks denote the same digit. Find that digit.",
        "h0": "For 11, " + RULE_11,
        "h1": "In star, 5, star, 0, the 2nd and 4th digits give 5 plus 0, which is 5. The 1st and 3rd give star plus star, which is always even, so it can never equal 5. So look for star plus star that is 11 more than 5.",
        "h2": "Try a similar one: star, 1, star, 6. The 2nd and 4th digits give 1 plus 6, which is 7. Star plus star cannot be 7, so make it 11 more, which is 18. Then star is 9, and 9196 is 11 times 836.",
        "s0": "The odd position sum is 2 times star. The even position sum is 5.",
        "s1": "If 2 times star, minus 5, is 0, then star is 2.5, which is not a digit.",
        "s2": "If 2 times star, minus 5, is 11, then 2 times star is 16, so star is 8. That works.",
        "s3": "Verify: 8580 divided by 11 is 780. Correct.",
    },
    "EXT_G5_WS_B4_013": {
        "h1": "12 times 46 is 552. How much bigger than 552 is 555? The next multiple of 12 is one more 12 after 552.",
        "h2": "Try a smaller one: what is the least number to add to 20, to make it divisible by 7? 7 times 2 is 14, and 20 minus 14 is 6, so 20 is 6 past a multiple of 7. Add 7 minus 6, which is 1, to reach 21.",
        "s0": "Divide 555 by 12. 12 times 46 is 552, and 555 minus 552 is 3. So 555 is 3 more than a multiple of 12.",
        "s1": "The next multiple of 12 is 552 plus 12, which is 564.",
        "s2": "564 minus 555 is 9, so the least number to add is 9.",
    },
    "EXT_G5_WS_B4_014": {
        "h0": "18 is 2 times 9, so a number divisible by 18 must be divisible by both 2 and 9. That means it is even, and its digits add up to a multiple of 9.",
        "h1": "Start with 1881. Its last digit is odd, so it is not divisible by 2, and cannot be divisible by 18. For each even choice, add the digits, and see whether the total is a multiple of 9.",
        "h2": "Try a smaller one: is 594 divisible by 18? It is even, and 5 plus 9 plus 4 is 18, a multiple of 9. So yes: 594 is 18 times 33.",
        "s0": "18 is 2 times 9, so the number must be even, and its digits must add up to a multiple of 9.",
        "s2": "3072: 3 plus 0 plus 7 plus 2 is 12, not a multiple of 9. 6666: 6 plus 6 plus 6 plus 6 is 24, not a multiple of 9.",
        "s3": "3978 is even, and 3 plus 9 plus 7 plus 8 is 27, which is 9 times 3.",
        "s4": "So 3978 is exactly divisible by 18. 3978 is 18 times 221.",
    },
    "EXT_G5_WS_B4_016": {
        "h2": "A similar one: can a prime number end in 4? Numbers ending in 4 are 4, 14, 24, 34, and so on. All are even, and bigger than 2, so each can be divided by 2. No prime ends in 4.",
        "s0": "Numbers ending in 6 are even: 6, 16, 26, 36, and so on.",
        "s1": "The only even prime is 2. No prime greater than 2 is even.",
        "s2": "So 6 can never be the units digit of a prime.",
    },
    "EXT_G5_WS_B4_017": {
        "h0": "Prior to 59 means going backwards. List the prime numbers just below 59, largest first, and count to the fourth.",
        "h1": "Go down from 59, and test each odd number. 57 is 3 times 19, and 55 is 5 times 11, so they are not prime, but 53 is. So 53 is the first prime before 59. Keep going down for three more.",
        "h2": "Try a smaller one: the third prime before 30. Going down: 29 is prime, the 1st. 23 is prime, the 2nd. 19 is prime, the 3rd. So it is 19.",
        "s0": "The primes less than 59, going down, are 53, 47, 43, 41, 37, and so on.",
        "s1": "Count: 53 is 1st, 47 is 2nd, 43 is 3rd, 41 is 4th.",
        "s2": "The 4th consecutive prime before 59 is 41.",
    },
    "EXT_G5_WS_B4_021": {
        "h0": "Both digits must be prime, so each digit is 2, 3, 5 or 7. The whole two-digit number must be prime as well.",
        "h1": "A number ending in 2 is even, and one ending in 5 is in the 5 times table, so the ones digit must be 3 or 7. That leaves 23, 33, 53, 73, 27, 37, 57 and 77. Test each: is it prime?",
        "h2": "A similar one: two-digit primes whose digits are both 1 or 3. The numbers are 11, 13, 31 and 33. 33 is 3 times 11, so it is not prime. The other three are. So there are 3.",
        "s0": "The possible two-digit numbers with both digits prime are: 22, 23, 25, 27. Then 32, 33, 35, 37. Then 52, 53, 55, 57. Then 72, 73, 75, 77.",
        "s1": "Check which are prime: 23, 37, 53 and 73 are.",
        "s2": "All the others fail. 22 is even. 25 divides by 5. 27 divides by 3. 32 is even. 33 divides by 3. 35 divides by 5. 52 is even. 55 divides by 5. 57 divides by 3. 72 is even. 75 divides by 5. 77 divides by 7.",
        "s3": "The count is 4.",
    },
    "EXT_G5_WS_B4_022": {
        "o": ["M minus 1", "M minus 4", "M plus 1", "M plus 5"],
        "h1": "99 is 9 times 11, and 98 is even, so neither is prime. The next one down, 97, is prime, so M is 97. Now work out each choice, like 97 plus 5, and see which is in the 4 times table.",
        "h2": "Try a smaller one: the greatest one-digit prime is 7. Then 7 plus 1 is 8, and 8 is 4 times 2. So there, it is the prime plus 1 that is divisible by 4.",
        "s0": "M is 97, the greatest two-digit prime.",
        "s1": "M minus 1 is 96. 96 divided by 4 is 24, which is exact.",
        "s2": "M minus 4 is 93. 93 divided by 4 is 23.25, not exact.",
        "s3": "M plus 1 is 98. 98 divided by 4 is 24.5, not exact.",
        "s4": "The answer: M minus 1.",
    },
    "EXT_G5_WS_B5_003": {
        "q": "The successor of the square of the smallest two-digit prime number is what?",
        "h1": "The two-digit numbers start at 10, which is even, so it is not prime. The next number, 11, is prime. Now work out 11 times 11, and then add 1.",
        "h2": "Try a smaller one: the successor of the square of the smallest odd prime. The smallest odd prime is 3. 3 times 3 is 9, and the number after 9 is 10.",
        "s0": "The smallest two-digit prime is 11.",
        "s1": "11 squared is 121.",
        "s2": "The successor is 121 plus 1, which is 122.",
    },
    "EXT_G5_WS_B5_006": {
        "h1": "99 and 98 are not prime, but 97 is. To square it, split the sum: 97 times 97 is 97 times 100, minus 97 times 3. Work that out, then look at the hundreds digit.",
        "h2": "Try a smaller one: 13 times 13 is 13 times 10, plus 13 times 3. That is 130 plus 39, which is 169. In 169, the hundreds digit is 1.",
        "s0": "The greatest 2 digit prime is 97.",
        "s1": "97 squared is 9409.",
        "s2": "The hundreds digit of 9409 is 4.",
    },
    "EXT_G5_WS_B5_007": {
        "h0": "Read the order carefully: first add the one-digit primes, then square the total.",
        "h1": "The one-digit primes are 2, 3, 5 and 7. 1 is not a prime. Add them up, then multiply the total by itself.",
        "h2": "Try a smaller one: the square of the sum of 1, 2 and 3. The sum is 1 plus 2 plus 3, which is 6, and 6 times 6 is 36.",
        "s0": "The one-digit primes are 2, 3, 5 and 7.",
        "s1": "The sum is 2 plus 3 plus 5 plus 7, which is 17.",
        "s2": "17 squared is 289.",
    },
    "EXT_G5_WS_B5_017": {
        "h1": "588 is 2 times 2, times 3, times 7 times 7. Pair them up: two 2s, two 7s. Which factor is left on its own? Dividing by it leaves only pairs.",
        "h2": "Try a smaller one: 50 is 2, times 5 times 5. The 5s make a pair, but the 2 is alone. Divide by 2: 50 divided by 2 is 25, and 5 times 5 is 25.",
        "s0": "Break 588 into prime factors. 588 equals 2 times 2, times 3, times 7 times 7.",
        "s2": "Divide by 3: 588 divided by 3 is 196, and 14 times 14 is 196.",
    },
    "EXT_G5_WS_B5_019": {
        "h1": "3 times 4 times 5 times 6 is the same as 3, times 2 times 2, times 5, times 2 times 3. Pair them up: the 3s pair, and two of the 2s pair. Which primes are left without a partner? Multiply by exactly those.",
        "h2": "Try a smaller one: 2 times 3 times 6 times 7 is the same as 2 times 3, times 2 times 3, times 7. The 2s pair, and the 3s pair, but 7 is alone. Multiply by 7: 252 times 7 is 1764, and 42 times 42 is 1764.",
        "s0": "3 times 4 times 5 times 6 is 360.",
        "s1": "In prime factors, 360 is 2 times 2 times 2, times 3 times 3, times 5. The 3s pair, and two of the 2s pair, but one 2 and the 5 have no partner.",
        "s2": "Multiply by 2 times 5, which is 10, to give each a partner: 360 times 10 is 3600.",
        "s3": "60 times 60 is 3600, a square number. So the smallest number to multiply by is 10.",
    },
}
