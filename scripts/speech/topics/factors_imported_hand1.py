"""Hand-written narration for imported factors questions (AIGEN_grade5_..., IPMTB_grade5_...).

Keys as in the other hand files: 'q', 'o' (four options), 'h0'..'h2', 's0'... A hand-written step
is the whole spoken step: where it should also read the maths line printed under the step, the
words for that line are written here too. Anything left out goes through factors_imported_rules.

AIGEN ids are long, so they are keyed by their first 21 characters ('AIGEN_grade5_' + 8); factors.py
checks that each such key names exactly one question.
"""

HAND = {
    "AIGEN_grade5_382913bb": {
        "h2": "Here's a similar problem: A number is divisible by 4, leaves remainder 2 when divided by 3, and is less than 30. Multiples of 4 below 30 are 4, 8, 12, 16, 20, 24 and 28. Check the remainder when divided by 3. 4 divided by 3 leaves remainder 1. 8 divided by 3 leaves remainder 2. Answer: 8. There could also be 20. Use the same approach for your problem!",
    },
    "AIGEN_grade5_3aed085e": {
        "h2": "Similar problem: Find the largest multiple of 12 between 200 and 300. 300 divided by 12 equals 25, so 12 times 25 equals 300. But 300 is not strictly between 200 and 300. So try 12 times 24, which is 288. That's between 200 and 300. The sum of the digits of 288 is 2 plus 8 plus 8, which is 18.",
        "s3": "Check: Is 396 between 300 and 400? Yes! Is 396 divisible by 4? 396 divided by 4 equals 99. Is 396 divisible by 9? 3 plus 9 plus 6 equals 18, and 18 divided by 9 equals 2.",
    },
    "AIGEN_grade5_37cb2537": {
        "h2": "Similar problem: If you have 36 red beads and 48 blue beads, and want equal-sized groups as large as possible, the H C F of 36 and 48 is 12. So you get 36 divided by 12, which is 3 red groups, and 48 divided by 12, which is 4 blue groups. That makes 7 groups in total. If each group costs 10 rupees, the total is 70 rupees.",
    },
    "AIGEN_grade5_501ac709": {
        "h2": "Here's a similar problem: A courtyard is 120 centimetres by 180 centimetres. The H C F of 120 and 180 is 60. So the largest square tile is 60 centimetres by 60 centimetres. The number of tiles equals 120 times 180, divided by 60 times 60. That is 21600 divided by 3600, which is 6 tiles. Now try the same method with 360 and 504!",
    },
    "AIGEN_grade5_6db9284a": {
        "h2": "Here's a similar problem: If you buy pencils in packs of 6 and erasers in packs of 8, the least number you can buy equally is the L C M of 6 and 8, which is 24. If pencils cost 2 rupees each and erasers cost 3 rupees each, the total is 24 times 2 rupees, plus 24 times 3 rupees. That is 48 rupees plus 72 rupees, which is 120 rupees.",
        "s2": "L C M: take the highest power of each prime factor. L C M equals 2 to the power of 4, times 3 squared, which is 16 times 9, which is 144.",
    },
    "AIGEN_grade5_78e9c34b": {
        "s3": "The H C F uses the common primes with the smallest powers. Both have 3, where the smallest power is 3 to the power of one. And both have 5 squared, where the smallest power is 5 squared. H C F equals 3 to the power of 1, times 5 squared, which is 3 times 25, which is 75.",
    },
    "AIGEN_grade5_79b0b1e1": {
        "s1": "List all factors of 180. The number of factors is open bracket 2 plus 1 close bracket, times open bracket 2 plus 1 close bracket, times open bracket 1 plus 1 close bracket, which equals 18. They are: 1, 2, 3, 4, 5, 6, 9, 10, 12, 15, 18, 20, 30, 36, 45, 60, 90 and 180.",
    },
    "AIGEN_grade5_905c1d7b": {
        "s1": "Use the factor-counting formula: if a number equals P to the power A, times Q to the power B, then the number of factors equals open bracket A plus 1 close bracket, times open bracket B plus 1 close bracket. Here, the number of factors equals open bracket 3 plus 1 close bracket, times open bracket 2 plus 1 close bracket. That is 4 times 3, which is 12.",
    },
    "AIGEN_grade5_bbb676d2": {
        "s2": "Use the factor-counting formula: if a number equals P to the power A, times Q to the power B, the total number of factors is open bracket A plus 1 close bracket, times open bracket B plus 1 close bracket. Here, the number of factors equals open bracket 3 plus 1 close bracket, times open bracket 2 plus 1 close bracket. That is 4 times 3, which is 12.",
    },
    "AIGEN_grade5_c2bc13fb": {
        "h1": "First, list all the factors of 84: 1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42 and 84. The number of friends must be a factor, and 84 divided by the number of friends must be more than 5.",
        "s3": "Each friend must get more than 5 chocolates. So 84 divided by the number of friends is greater than 5. That means the number of friends is less than 84 divided by 5, which is 16.8.",
    },
    "AIGEN_grade5_d02117b0": {
        "s4": "Pick the smallest powers. 2 squared is the smallest of 2 cubed, 2 squared, and 2 to the power of four. 3 to the power of one is the smallest of 3 to the power of one, 3 squared, and 3 to the power of one. And 7 to the power of one, because all have 7 to the power of one. H C F equals 2 squared, times 3 to the power of 1, times 7 to the power of 1. That is 4 times 3 times 7, which is 84.",
    },
    "AIGEN_grade5_eca45cd9": {
        "s1": "Check each number. 41 is prime. 42 is divisible by 2, so not prime. 43 is prime. 44 is divisible by 2. 45 is divisible by 5. 46 is divisible by 2. 47 is prime. 48 is divisible by 2. 49 is 7 times 7, so not prime.",
    },
    "IPMTB_grade5_ch01_q035": {
        "h2": "Here's a similar problem: How many primes between 80 and 90? List them. 81, divided by 3, is 27. 82 is even. 83 is not divisible by 2, 3, 5 or 7, so it is prime! 84 is even. 85, divided by 5, is 17. 86 is even. 87, divided by 3, is 29. 88 is even. 89 is not divisible by 2, 3, 5 or 7, so it is prime! So there are 2 primes between 80 and 90.",
        "s5": "Check 97. Try dividing by 2: no, it's odd. By 3: 9 plus 7 equals 16, which is not divisible by 3. By 5: it doesn't end in 0 or 5. By 7: 7 times 13 equals 91, and 7 times 14 equals 98, so no. 97 is prime!",
    },
    "IPMTB_grade5_ch01_q036": {
        "s3": "Primes from 10 to 19. Check each. 10, no, it is divisible by 2 and 5. 11, yes. 12, no. 13, yes. 14, no. 15, no. 16, no. 17, yes. 18, no. 19, yes. That's 4 more: 11, 13, 17 and 19.",
        "s4": "Primes from 20 to 29. 20, no. 21, no, it is 3 times 7. 22, no. 23, yes. 24, no. 25, no, it is 5 times 5. 26, no. 27, no. 28, no. 29, yes. That's 2 more: 23 and 29.",
        "s5": "Primes from 30 to 39. 30, no. 31, yes. 32, no. 33, no, it is 3 times 11. 34, no. 35, no, it is 5 times 7. 36, no. 37, yes. 38, no. 39, no, it is 3 times 13. That's 2 more: 31 and 37.",
        "s6": "Primes from 40 to 49. 40, no. 41, yes. 42, no. 43, yes. 44, no. 45, no. 46, no. 47, yes. 48, no. 49, no, it is 7 times 7. That's 3 more: 41, 43 and 47.",
    },
    "IPMTB_grade5_ch01_q038": {
        "h2": "Here's a similar problem: How many odd prime numbers are there between 1 and 10? The odd numbers are 3, 5, 7 and 9. Check each: 3 is prime, 5 is prime, 7 is prime, and 9 equals 3 times 3, so it is not prime. Answer: 3 odd primes between 1 and 10. Now use the same approach for even primes between 1 and 100!",
        "s6": "Why? Because every even number greater than 2 can be written as 2 times something, so it always has at least three factors: 1, 2, and itself.",
    },
}
