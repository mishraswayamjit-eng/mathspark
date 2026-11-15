"""Hand-written narration: past-paper questions 2020 to 2025, and worksheet B2 questions 007 to 019.

Each entry gives the question, the hints and the steps as spoken. Answer choices are spoken by rule.
"""

HAND = {
    "EXT_G5_FP_2020_009": {
        "q": "A man earned 120 rupees when he sold 8 dozens of mangoes. How much would he earn, if he sold 20 dozens of mangoes?",
        "hints": [
            "Find the earning on one dozen first. Then multiply by 20.",
            "Unitary method.",
            "",
        ],
        "steps": [
            "1 dozen earns 120 divided by 8, which is 15 rupees.",
            "20 dozens earn 20 times 15, which is 300 rupees.",
        ],
    },
    "EXT_G5_FP_2020_024": {
        "q": "A man takes up a work to be completed in 30 days, for 27000 rupees. He works for 18 days, and then leaves. If you were the employer, how much would you pay him?",
        "hints": [
            "He should be paid only for the days he worked. Find the pay for one day first: 27000 divided by 30.",
            "Then multiply one day's pay by the 18 days he worked.",
            "Try a smaller one. 1000 rupees for 10 days, is 100 rupees a day. For 4 days of work, the pay is 4 times 100, which is 400 rupees.",
        ],
        "steps": [
            "The pay per day is 27000 divided by 30, which is 900 rupees.",
            "The pay for 18 days is 18 times 900, which is 16,200 rupees.",
        ],
    },
    "EXT_G5_FP_2021_038": {
        "q": "A tailor has 37.5 metres of cloth, and he has to make 8 pieces out of a metre of cloth. How many pieces can he make out of this cloth?",
        "hints": [
            "Each metre gives 8 pieces. So multiply the number of metres by 8.",
            "Pieces equal metres, times pieces per metre.",
            "",
        ],
        "steps": [
            "37.5 times 8 is 300 pieces.",
            "300 is not among the first three options. So the answer is, none of these.",
        ],
    },
    "EXT_G5_FP_2022_001": {
        "q": "One gross note book is bought for 936 rupees. Find the cost of 48 books.",
        "hints": [
            "One gross means 144. Find the cost of one book first, then multiply by 48.",
            "1 gross is 12 dozen, which is 144. Unitary method.",
            "",
        ],
        "steps": [
            "The cost of 1 book is 936 divided by 144, which is 6.50 rupees.",
            "The cost of 48 books is 48 times 6.50, which is 312 rupees.",
        ],
    },
    "EXT_G5_FP_2022_038": {
        "q": "If 16 jugs can hold 1 decalitre of juice, how many jugs will be required to hold 15625 millilitres?",
        "hints": [
            "1 decalitre is 10 litres, which is 10,000 millilitres. Find how many millilitres one jug holds, then divide 15625 by it.",
            "1 decalitre is 10 litres, which is 10,000 millilitres. Unitary method.",
            "",
        ],
        "steps": [
            "1 jug holds 10000 divided by 16, which is 625 millilitres.",
            "Jugs needed: 15625 divided by 625, which is 25.",
        ],
    },
    "EXT_G5_FP_2023_014": {
        "q": "12 men can complete a work in 54 days. How many men will be required, to complete the same work in 24 days?",
        "hints": [
            "Fewer days means more men. The total work, which is men times days, stays the same.",
            "Men times days is constant.",
            "",
        ],
        "steps": [
            "The total work is 12 times 54, which is 648 man days.",
            "Men for 24 days: 648 divided by 24, which is 27 men.",
        ],
    },
    "EXT_G5_FP_2023_025": {
        "q": "A car travels 126 kilometres in 12 litres of petrol. How many kilometres will it travel in 22 litres of petrol?",
        "hints": [
            "Find how far the car goes on just 1 litre, then multiply by 22.",
            "Unitary method.",
            "",
        ],
        "steps": [
            "On 1 litre, it goes 126 divided by 12, which is 10.5 kilometres.",
            "On 22 litres, it goes 22 times 10.5, which is 231 kilometres.",
        ],
    },
    "EXT_G5_FP_2024_018": {
        "q": "Three dozen mangoes cost 1800 rupees. How much would 26 mangoes cost?",
        "hints": [
            "One dozen means 12. Three dozen is how many mangoes? Find the cost of one mango first.",
            "Unitary method: find the value of 1, then multiply.",
            "",
        ],
        "steps": [
            "3 dozen is 3 times 12, which is 36 mangoes.",
            "The cost of 1 mango is 1800 divided by 36, which is 50 rupees.",
            "The cost of 26 mangoes is 26 times 50, which is 1300 rupees.",
        ],
    },
    "EXT_G5_FP_2025_003": {
        "q": "1 gross of cricket balls costs 32,400 rupees. What will be the cost of 85 cricket balls?",
        "hints": [
            "1 gross is 144 items. Find the cost of one ball, then multiply by 85.",
            "1 dozen is 12, and 1 gross is 12 dozen, which is 144.",
            "",
        ],
        "steps": [
            "The cost of 1 ball is 32,400 divided by 144, which is 225 rupees.",
            "The cost of 85 balls is 85 times 225, which is 19,125 rupees.",
        ],
    },
    "EXT_G5_FP_2025_025": {
        "q": "15 men can do a work in 28 days. If the work has to be done in 20 days, how many more men will be required?",
        "hints": [
            "Fewer days means more men. The total work, which is men times days, stays the same. And the question asks for more men, not the total.",
            "Men times days is constant. This is inverse proportion.",
            "",
        ],
        "steps": [
            "The total work is 15 times 28, which is 420 man days.",
            "Men needed for 20 days: 420 divided by 20, which is 21.",
            "More men needed: 21 minus 15, which is 6.",
        ],
    },
    "EXT_G5_WS_B2_007": {
        "q": "In how many ways can 28 be written as a sum of two odd numbers?",
        "hints": [
            "You need pairs of odd numbers that add up to 28. Swapping the two numbers, like 1 plus 27, and 27 plus 1, counts as the same way.",
            "Start with the smallest odd number, and list in order: 1 plus 27, 3 plus 25, 5 plus 23, and so on. Stop when the first number would become bigger than the second.",
            "Here is an example with 12. The pairs of odd numbers are 1 plus 11, 3 plus 9, and 5 plus 7. The next would be 7 plus 5, a repeat. So 12 can be written in 3 ways.",
        ],
        "steps": [
            "List the pairs of odd numbers that add up to 28, starting with the smallest odd number: 1 plus 27, 3 plus 25, 5 plus 23, 7 plus 21, 9 plus 19, 11 plus 17, 13 plus 15.",
            "The next pair would be 15 plus 13, which repeats 13 plus 15. So the list is complete.",
            "Count the pairs. So 28 can be written as a sum of two odd numbers in 7 ways.",
        ],
    },
    "EXT_G5_WS_B2_010": {
        "q": "Add the difference of 7369 and 2418 to their sum. The result is what number?",
        "hints": [
            "First, find the difference and the sum separately. Then add them together.",
            "The difference is 7369 minus 2418, which is 4951. The sum is 7369 plus 2418, which is 9787.",
            "Try this. The difference of 10 and 3 is 7. The sum of 10 and 3 is 13. Add them: 7 plus 13 is 20. That's 2 times 10, which is 2 times the larger number!",
        ],
        "steps": [
            "The difference is 7369 minus 2418, which is 4951.",
            "The sum is 7369 plus 2418, which is 9787.",
            "The result is 4951 plus 9787, which is 14738.",
        ],
    },
    "EXT_G5_WS_B2_015": {
        "q": "6 years hence, Sumit will be 17 years old. What was his age, 8 years ago?",
        "hints": [
            "If Sumit will be 17 in 6 years, what is his current age?",
            "His current age is 17 minus 6, which is 11. His age 8 years ago is 11 minus 8.",
            "Try this. If Riya will be 20 in 5 years, her current age is 15. 3 years ago, she was 12.",
        ],
        "steps": [
            "His current age is 17 minus 6, which is 11 years.",
            "His age 8 years ago is 11 minus 8, which is 3 years.",
        ],
    },
    "EXT_G5_WS_B2_016": {
        "q": "The present ages of Disha and Nisha add up to 25 years. What was the sum of their ages, 4 years ago?",
        "hints": [
            "If their current total age is 25, how much was each person younger, 4 years ago?",
            "Each was 4 years younger. The total reduction is 4 times 2, which is 8 years.",
            "Try this. If A plus B equals 20 today, then 3 years ago: A minus 3, plus B minus 3, equals 20 minus 6, which is 14.",
        ],
        "steps": [
            "4 years ago, each person was 4 years younger.",
            "The sum 4 years ago is 25 minus 4, minus 4. That is 25 minus 8, which is 17.",
        ],
    },
    "EXT_G5_WS_B2_017": {
        "q": "In 2020, the sum of the ages of Mister Joshi, his wife and his son was 100 years. What will the sum of their ages be, in the year 2028?",
        "hints": [
            "How many years pass from 2020 to 2028? Each person ages by that many years.",
            "8 years pass. 3 people each age 8 years. That is 3 times 8, which is 24 extra years.",
            "Try this. If 2 people's ages sum to 50 in 2020, then in 2025: 50 plus 2 times 5, which is 60.",
        ],
        "steps": [
            "Years elapsed: 2028 minus 2020, which is 8.",
            "Each of 3 people ages 8 years. The total increase is 3 times 8, which is 24.",
            "The new sum is 100 plus 24, which is 124.",
        ],
    },
    "EXT_G5_WS_B2_018": {
        "q": "4 years from now, the ages of Vijay and Vinay will add up to 67 years. What was the sum of their ages, 5 years ago?",
        "hints": [
            "There are two people, so every year that passes adds 2 years to the sum of their ages. Going back in time takes 2 years off, for each year.",
            "From 4 years in the future, back to 5 years in the past, is 4 plus 5, which is 9 years. In 9 years, the sum of two ages changes by 2 times 9. Take that away from 67.",
            "Here is an example. In 2 years, two ages will add up to 30. What was the sum, 3 years ago? That is 2 plus 3, which is 5 years earlier. So the sum is 2 times 5, which is 10 less: 30 minus 10 is 20 years.",
        ],
        "steps": [
            "In 4 years, each of the two will be 4 years older. So the sum now is 67, minus 2 times 4, which is 59 years.",
            "5 years ago, each of them was 5 years younger. So take away 2 times 5, which is 10 years.",
            "59 minus 10 is 49. So the sum of their ages, 5 years ago, was 49 years.",
        ],
    },
    "EXT_G5_WS_B2_019": {
        "q": "The sum of the ages of Aman and Suman, in the year 2015, was 87 years. If Aman celebrated his 37th birthday in the year 2005, in which year was Suman born?",
        "hints": [
            "Work in three small steps. Find Aman's age in 2015, then Suman's age in 2015, then count back to the year Suman was born.",
            "From 2005 to 2015 is 10 years. So Aman was 37 plus 10, which is 47, in 2015. Take 47 away from 87, to get Suman's age in 2015. Then subtract that age from 2015.",
            "Here is an example. Riya turned 10 in 2000, so she was 15 in 2005. If Riya and Tara's ages added up to 35 in 2005, Tara was 35 minus 15, which is 20. So Tara was born in 2005 minus 20, which is 1985.",
        ],
        "steps": [
            "Aman was 37 in 2005, so in 2015 he was 37 plus 10, which is 47.",
            "Suman's age in 2015 is 87 minus 47, which is 40.",
            "Suman's birth year is 2015 minus 40, which is 1975.",
        ],
    },
}
