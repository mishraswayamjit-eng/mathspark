"""Hand-written fixes for past papers 2016 and 2017 (EXT_G5_FP_2016_*, EXT_G5_FP_2017_*)."""


def S(*texts):
    return [{"text": t, "latex": ""} for t in texts]


HAND = {
    "EXT_G5_FP_2016_004": {
        "steps": S(
            "From 12 to 1 the hour hand takes 60 minutes.",
            "The hand has gone 4/5 of the way, so 4/5 of the 60 minutes have passed.",
            "One fifth of 60 is 60 ÷ 5 = 12, so four fifths is 4 × 12 = 48 minutes.",
            "So the time is 48 minutes past 12, which is 12:48.",
        ),
        "why": "Step 2 chained '4/5 of 60 = 60 ÷ 5 × 4 = ...', which reads as an untrue sum (60 = 48).",
    },
    "EXT_G5_FP_2016_009": {
        "hints": [
            "Open the bracket first: the 4 multiplies BOTH x and 6. Mind the minus sign in front of the 4: it applies to both parts.",
            "After opening the bracket you have 3x take away 4x, and a number taken away as well. Collect the x terms, then find x.",
            "Try a similar one: 2x − 3(x + 1) is 0. Opening the bracket gives 2x − 3x − 3, which must be 0. So −x is 3, and x is −3.",
        ],
        "steps": S(
            "Open the bracket: 4(x + 6) is 4x + 24. With the minus sign in front, the left side becomes 3x − 4x − 24.",
            "Collect the x terms: 3x − 4x is −x. So −x − 24 must equal 0.",
            "That means −x is 24, so x is −24.",
            "Check: 3 × (−24) − 4 × (−24 + 6) = −72 + 72 = 0. So x = −24.",
        ),
        "why": "Hint 2 gave away the 24 of the answer; the steps wrote equations in a form that reads as untrue sums.",
    },
    "EXT_G5_FP_2016_012": {
        "hints": [
            "Give all the fractions the same denominator so that you can compare them. Pick a number that 3, 8 and 12 all divide into exactly.",
            "Rewrite 1/3 and 7/8 with that common denominator first. Then rewrite each choice the same way and see which one lies between them.",
            "Try a smaller one: is 5/8 between 1/2 and 3/4? In eighths they are 4/8, 5/8 and 6/8, so yes, 5/8 lies between them.",
        ],
        "why": "Both hints named the denominator of the answer; there was no third hint.",
    },
    "EXT_G5_FP_2016_029": {
        "hints": [
            "Make all four fractions have the same bottom number. Find the smallest number that 2, 4, 3 and 6 all divide into.",
            "Rewrite each fraction with that common denominator. Then add and subtract only the top numbers, in the order given.",
            "Try a smaller one: 1/2 − 1/4 + 1/8. In eighths that is 4/8 − 2/8 + 1/8 = 3/8.",
        ],
        "why": "Hint 1 named the denominator of the answer; there was no third hint.",
    },
    "EXT_G5_FP_2016_033": {
        "steps": S(
            "One dozen is 12 eggs, so see how many twelves are in 27.",
            "12 goes into 27 twice (2 × 12 = 24), with 3 eggs left over.",
            "The 3 left-over eggs are 3/12 of a dozen, and 3/12 = 1/4 = 0.25.",
            "So 27 eggs are 2 + 0.25 = 2.25 dozen.",
        ),
        "why": "Step 1 wrote '27 ÷ 12 = 2 remainder 3', which is not a true sum as written.",
    },
    "EXT_G5_FP_2017_005": {
        "hints": [
            "The hour hand goes all the way round, 360°, in 12 hours. How many degrees does it turn in one hour?",
            "Divide 165° by the degrees turned in one hour to find how many hours pass. Half an hour counts too. Then add that time to 11:00 a.m.",
            "Try a smaller one: if the hour hand turns 90° starting from 2:00, that is a quarter of the full circle, so 3 hours pass and the time is 5:00.",
        ],
        "why": "Both hints stated the 30 that appears in the answer (4:30); there was no third hint.",
    },
    "EXT_G5_FP_2017_010": {
        "steps": S(
            "Try + × ÷: 10 + 6 × 4 ÷ 6 = 10 + 4 = 14. That is not 28.",
            "Try + − ÷: 4 ÷ 6 is not a whole number, so 10 + 6 − 4 ÷ 6 cannot be 28.",
            "Try + × −: multiply first, 6 × 4 = 24, then 10 + 24 − 6 = 28. This one works.",
            "So the signs are +, × and −, in that order.",
        ),
        "why": "The steps were labelled by option letter ('Option A: ...') and never said the answer in words.",
    },
    "EXT_G5_FP_2017_014": {
        "hints": [
            "One dozen is 12. So ask: how many twelves are in 21, and what part of a dozen is left over?",
            "12 goes into 21 once, with 9 left over. Write the 9 left over as a fraction of 12, then turn it into a decimal.",
            "Try a smaller one: 30 eggs. 12 goes in twice with 6 left over, and 6/12 = 0.5, so 30 eggs are 2.5 dozen.",
        ],
        "steps": S(
            "One dozen is 12 oranges. 12 goes into 21 once, with 21 − 12 = 9 oranges left over.",
            "The 9 left over are 9/12 of a dozen, and 9/12 = 3/4 = 0.75.",
            "So 21 oranges are 1 + 0.75 = 1.75 dozen.",
        ),
        "why": "Hint 1 trailed off mid-sum, and both it and step 1 wrote '21 ÷ 12 = 1 ...', which is not a true sum.",
    },
    "EXT_G5_FP_2017_016": {
        "hints": [
            "A perfect square is a whole number multiplied by itself. Look for whole numbers whose squares land near each choice.",
            "Start from 100 × 100 = 10000 and 101 × 101 = 10201. Is 10025 either of these? Test the other choices in the same way: a number ending in 25 could be the square of a number ending in 5.",
            "For example, 35 × 35 = 1225, so 1225 is a perfect square. A shortcut for squaring a number ending in 5: for 35, work out 3 × 4 = 12 and write 25 after it.",
        ],
        "why": "Hint 1 stated the answer outright ('105² = 11025'); there was no third hint.",
    },
    "EXT_G5_FP_2017_022": {
        "steps": S(
            "Find the pay for one day: 504 ÷ 7 = 72, so he earns Rs.72 a day.",
            "Now see how many days at Rs.72 a day make Rs.792: 792 ÷ 72 = 11.",
            "So he should work 11 days.",
        ),
        "why": "Step 2 ('Days for Rs.792 = 792 ÷ 72 = 11') reads as an untrue sum, and no step stated the answer in words.",
    },
    "EXT_G5_FP_2017_024": {
        "steps": S(
            "Top: 2/3 + 1/3 = 3/3, which is 1.",
            "Bottom: 2/3 − 1/3 = 1/3.",
            "Now divide the top by the bottom: 1 divided by 1/3. Dividing by 1/3 is the same as multiplying by 3, so 1 × 3 = 3.",
            "So the value is 3.",
        ),
        "why": "Step 3 wrote '1 ÷ 1/3 = 1 × 3', which read left to right is not a true sum.",
    },
    "EXT_G5_FP_2017_029": {
        "steps": S(
            "1 km is 1000 m and 1 hour is 3600 seconds. So to change m/s into km/hr, multiply by 3600 and divide by 1000, which is the same as multiplying by 18/5.",
            "30 × 18/5: first 30 ÷ 5 = 6, then 6 × 18 = 108.",
            "So the speed is 108 km/hr.",
        ),
        "why": "The solution was a single step that did not say where 18/5 comes from.",
    },
    "EXT_G5_FP_2017_036": {
        "steps": S(
            "Each term is 1 less than a power of 2: 2 − 1, 4 − 1, 8 − 1, 16 − 1 and so on. So the 30th term is 2³⁰ − 1.",
            "The units digits of the powers of 2 go 2, 4, 8, 6 and then repeat every 4 powers.",
            "30 is 7 lots of 4 with 2 left over (7 × 4 = 28), so 2³⁰ has the 2nd digit of the cycle: it ends in 4.",
            "Take away 1: the 30th term ends in 4 − 1 = 3.",
            "So the units digit is 3.",
        ),
        "why": "Step 3 wrote '30 ÷ 4 = 7 remainder 2', which is not a true sum as written.",
    },
}
