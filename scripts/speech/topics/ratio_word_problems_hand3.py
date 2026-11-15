"""Hand-written narration: worksheet questions B2 020 to 030 and B3 005 to 040.

Each entry gives the question, the hints and the steps as spoken. Answer choices are spoken by rule.
"""

HAND = {
    "EXT_G5_WS_B2_020": {
        "q": "At the start of the academic year, there were 1005 students in the school. During the year, 13 students left, and 42 students joined the school. If 1000 students passed the final examination, how many students failed?",
        "hints": [
            "First, find the total students at the end of the year. Then subtract those who passed.",
            "The total at the end is 1005 minus 13, plus 42, which is 1034. The number who failed is 1034 minus 1000.",
            "Try this. Start with 100, 5 leave, and 10 join. That makes 105. If 95 pass, the number who failed is 105 minus 95, which is 10.",
        ],
        "steps": [
            "Students at the end: 1005 minus 13, plus 42, which is 1034.",
            "The number who failed is 1034 minus 1000, which is 34.",
            "Verify: check the answer matches option A.",
        ],
    },
    "EXT_G5_WS_B2_022": {
        "q": "In a class, there are 11 fewer boys than girls. If the total number of girls is 42, then the overall strength of the class is?",
        "hints": [
            "If there are 42 girls, and 11 fewer boys, how many boys are there?",
            "Boys: 42 minus 11, which is 31. The total is boys plus girls.",
            "Try this. 20 girls, and 5 fewer boys, means 15 boys. The total is 35.",
        ],
        "steps": [
            "Boys: 42 minus 11, which is 31.",
            "Total: 42 plus 31, which is 73.",
        ],
    },
    "EXT_G5_WS_B2_023": {
        "q": "A and B contested an election. A received 275 votes. B won by a majority of 35 votes. How many votes were cast in this election?",
        "hints": [
            "If A got 275, and B won by 35, how many did B get?",
            "B's votes are 275 plus 35, which is 310. The total votes are A plus B.",
            "Try this. A gets 100, and B wins by 20. So B gets 120. The total is 220.",
        ],
        "steps": [
            "B won by 35 means B got 35 more than A. So B got 275 plus 35, which is 310.",
            "The total votes are 275 plus 310, which is 585.",
            "Verify: check the answer matches option C.",
        ],
    },
    "EXT_G5_WS_B2_026": {
        "q": "In a class of 40 students, exactly 18 have been to Delhi, and exactly 15 have been to Kashmir. 6 students have been to both Delhi and Kashmir. How many students have not been to Delhi or Kashmir?",
        "hints": [
            "Use the inclusion exclusion principle: the total who visited equals Delhi, plus Kashmir, minus both.",
            "Visited at least one: 18 plus 15, minus 6, which is 27. Not visited: 40 minus 27.",
            "Try this. In a class of 20, 10 play cricket, 8 play football, and 3 play both. At least one: 10 plus 8, minus 3, which is 15. Neither: 20 minus 15, which is 5.",
        ],
        "steps": [
            "Students who visited at least one place: 18 plus 15, minus 6, which is 27.",
            "Students who visited neither: 40 minus 27, which is 13.",
            "Verify: check the answer matches option A.",
        ],
    },
    "EXT_G5_WS_B2_027": {
        "q": "In a class, there are 30 students in all. Every student speaks at least one of the two languages, Hindi and Marathi. If 21 students speak Hindi, and 5 students speak both languages, then how many students speak only Marathi?",
        "hints": [
            "If 21 speak Hindi, and some also speak Marathi, find how many speak only Marathi.",
            "The total equals Hindi only, plus Marathi only, plus both. Hindi only is 21 minus 5, which is 16. Marathi only is 30 minus 16, minus 5.",
            "Try this. 20 students, 15 speak English, and 3 speak both. English only is 12. Other only is 20 minus 12, minus 3, which is 5.",
        ],
        "steps": [
            "Hindi only is 21 minus 5, which is 16.",
            "Marathi only is 30 minus 16, minus 5, which is 9.",
            "Hmm, wait. That gives 9, which is option B. Let me recheck. The total equals Hindi only, plus both, plus Marathi only. 30 equals 16 plus 5, plus Marathi only. So Marathi only is 9.",
        ],
    },
    "EXT_G5_WS_B2_029": {
        "q": "Four players joined a chess tournament. Each player played one game against the other players. How many games were played in all, in this tournament?",
        "hints": [
            "If each player plays every other player once, count the pairs.",
            "With 4 players, A, B, C and D, the games are: A B, A C, A D, B C, B D, C D. That is 6 games.",
            "Try 3 players: A B, A C, B C. That is 3 games. The formula is n, times n minus 1, divided by 2.",
        ],
        "steps": [
            "The number of games equals the number of ways to choose 2 players from 4.",
            "That equals 4 times 3, divided by 2, which is 6.",
            "Verify: check the answer matches option C.",
        ],
    },
    "EXT_G5_WS_B2_030": {
        "q": "At a meeting, 13 people shook hands with each other. How many handshakes took place in all?",
        "hints": [
            "Same idea as the chess problem: count pairs of people.",
            "The formula is n, times n minus 1, divided by 2, where n is 13.",
            "Try 4 people: 4 times 3, divided by 2, is 6 handshakes. For 13 people: 13 times 12, divided by 2.",
        ],
        "steps": [
            "Handshakes: 13 times 12, divided by 2.",
            "That equals 156 divided by 2, which is 78.",
            "Verify: check the answer matches option A.",
        ],
    },
    "EXT_G5_WS_B3_005": {
        "q": "A factory makes 1720 boxes every day. What is the total production in the month of July?",
        "hints": [
            "July has 31 days. The total is 1720 times 31.",
            "Break it down: 1720 times 30, plus 1720 times 1.",
            "Try this. 100 boxes a day, times 31 days, is 3100 boxes.",
        ],
        "steps": [
            "July has 31 days.",
            "The total is 1720 times 31. That is 1720 times 30, plus 1720. Which is 51600 plus 1720, giving 53320.",
        ],
    },
    "EXT_G5_WS_B3_013": {
        "q": "12.5 kilograms of sweets were distributed equally amongst 25 students, out of which 17 are girls, and the rest are boys. What quantity of sweets did each boy receive?",
        "hints": [
            "Sweets per student: 12.5 kilograms divided by 25. They are distributed equally among all students, not just boys.",
            "12.5 kilograms is 12500 grams. Each student gets 12500 divided by 25, which is 500 grams.",
            "Try this. Number equals divisor times quotient, plus remainder. For example, 27 equals 5 times 5, plus 2.",
        ],
        "steps": [
            "12.5 kilograms is 12500 grams.",
            "Each student gets 12500 divided by 25, which is 500 grams.",
            "The answer is option B.",
        ],
    },
    "EXT_G5_WS_B3_019": {
        "q": "Instead of multiplying, a student divided a number by 13, and got 11 as the quotient, and 4 as the remainder. What was the correct answer to the problem?",
        "hints": [
            "The student divided instead of multiplying. First, find the number.",
            "The number is 13 times 11, plus 4, which is 147. The correct operation is 147 times 13, which is 1911.",
            "Try this. Divided by 5, the quotient is 3 and the remainder is 1, so the number is 16. We should multiply: 16 times 5 is 80.",
        ],
        "steps": [
            "The number is 13 times 11, plus 4, which is 147.",
            "The correct answer is 147 times 13, which is 1911.",
            "The answer is option A.",
        ],
    },
    "EXT_G5_WS_B3_025": {
        "q": "In a basket, there are 56 apples. Amey takes out 4 apples at a time, and replaces them with 3 oranges. He continues this process till all the apples in the basket are replaced. How many oranges will there be in the basket in the end?",
        "hints": [
            "Each round: remove 4 apples, add 3 oranges. How many rounds until 56 apples are gone?",
            "Rounds: 56 divided by 4, which is 14. Oranges: 14 times 3, which is 42.",
            "Try this. 8 apples. Remove 2, and add 1, each round. That is 4 rounds, and 4 oranges.",
        ],
        "steps": [
            "Rounds: 56 divided by 4, which is 14.",
            "Oranges: 14 times 3, which is 42.",
            "The answer is option A.",
        ],
    },
    "EXT_G5_WS_B3_028": {
        "q": "Four years hence, Siya will be 3 years older than Diya. The sum of their present ages is 35 years. How old is Siya at present?",
        "hints": [
            "In 4 years, Siya will be 3 years older than Diya. This means Siya is always 3 years older.",
            "S equals D plus 3. S plus D equals 35. So, D plus 3, plus D, equals 35. 2 D equals 32. D equals 16, and S equals 19.",
            "Try this. A is 5 years older, and the sum is 25. Then B is 10, and A is 15.",
        ],
        "steps": [
            "Siya is 3 years older than Diya, which is always true. So S equals D plus 3.",
            "S plus D equals 35. So, D plus 3, plus D, equals 35. D equals 16, and S equals 19.",
            "The answer is option A.",
        ],
    },
    "EXT_G5_WS_B3_030": {
        "q": "At a sports meet, there were 14 events, and in each event, gold, silver and bronze medals were awarded. If the total number of medals won by boys is 6 less than those won by the girls, how many medals did the boys win?",
        "hints": [
            "The total medals are 14 events, times 3 medals, which is 42.",
            "Boys plus girls equals 42. Girls equal boys plus 6. So boys, plus boys, plus 6, equals 42.",
            "Try with simple numbers first, to check your method. Then apply it to the real problem.",
        ],
        "steps": [
            "The total medals are 14 times 3, which is 42.",
            "B, plus B plus 6, equals 42.",
            "2 B equals 36, so B equals 18.",
        ],
    },
    "EXT_G5_WS_B3_032": {
        "q": "Jiya has an equal number of notes of denomination 5 rupees, 10 rupees and 20 rupees. If she has 910 rupees in all, how many notes of each kind does she have?",
        "hints": [
            "Read the question carefully. This tests your understanding of equal distribution. Identify what information is given, and what you need to find.",
            "Write down the key formula or relationship for equal distribution. Think step by step about how to connect the given values to the answer.",
            "Try a simpler version of the problem first. Then apply the same method to the actual numbers.",
        ],
        "steps": [
            "The value of one set is 5 plus 10 plus 20, which is 35.",
            "The number of each is 910 divided by 35, which is 26.",
        ],
    },
    "EXT_G5_WS_B3_033": {
        "q": "Minal purchased an equal number of stamps of 5 paise, 20 paise and 25 paise. She paid 9 rupees in all for these stamps. What is the total number of stamps that Minal bought?",
        "hints": [
            "Each set of 3 stamps costs 5 plus 20 plus 25, which is 50 paise.",
            "9 rupees is 900 paise. Sets: 900 divided by 50, which is 18. Total stamps: 18 times 3, which is 54.",
            "Try a simpler version with smaller numbers, to check your method works. Then apply it to the real question.",
        ],
        "steps": [
            "A set of 3 stamps costs 5 plus 20 plus 25, which is 50 paise.",
            "900 divided by 50 is 18 sets.",
            "Total stamps: 18 times 3, which is 54.",
        ],
    },
    "EXT_G5_WS_B3_037": {
        "q": "If six people consume 1 kilogram of rice in a day, what quantity of rice will be consumed by 24 people in a week?",
        "hints": [
            "Scale up the people: 24 divided by 6 is 4 times more people, which means 4 kilograms a day.",
            "Scale up the time: 1 week is 7 days, which means 4 times 7, or 28 kilograms.",
            "Try this. 3 people eat 2 kilograms a day. 6 people, in 3 days, eat 2 times 2 times 3, which is 12 kilograms.",
        ],
        "steps": [
            "24 people is 4 groups of 6, which means 4 kilograms a day.",
            "7 days, times 4 kilograms a day, is 28 kilograms.",
        ],
    },
    "EXT_G5_WS_B3_040": {
        "q": "In a school, there are 4 girls for every 7 boys, and for every 55 students, there is a teacher. If the total strength of the boys in the school is 455, how many teachers are there in the school?",
        "hints": [
            "4 girls, for every 7 boys. If there are 455 boys, find the girls.",
            "Girls: 455 times 4 over 7, which is 260. Total students: 455 plus 260, which is 715.",
            "Try with simple numbers first, to check your method. Then apply it to the real problem.",
        ],
        "steps": [
            "There are 455 boys, and the ratio is 4 is to 7. So the girls are 455 times 4 over 7, which is 260.",
            "The total number of students is 715.",
            "Teachers: 715 divided by 55, which is 13.",
        ],
    },
}
