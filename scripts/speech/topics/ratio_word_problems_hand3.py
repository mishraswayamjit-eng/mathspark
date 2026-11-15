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
            "13 students left, so 1005 minus 13 is 992 students remained.",
            "42 students joined. So the school had 992 plus 42, which is 1034 students, at the end of the year.",
            "1000 of them passed, so 1034 minus 1000 is 34. So 34 students did not pass.",
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
            "B won by 35 votes, which means B got 35 more votes than A: 275 plus 35, which is 310 votes.",
            "Add the votes of A and B, to get all the votes cast: 275 plus 310 is 585.",
            "So, 585 votes were cast in this election.",
        ],
    },
    "EXT_G5_WS_B2_026": {
        "q": "In a class of 40 students, exactly 18 have been to Delhi, and exactly 15 have been to Kashmir. 6 students have been to both Delhi and Kashmir. How many students have not been to Delhi or Kashmir?",
        "hints": [
            "The 6 students who have been to both places are counted in the 18, and also in the 15. If you just add 18 and 15, they get counted twice.",
            "Find how many have been to at least one place: add 18 and 15, then take away 6, so nobody is counted twice. Then subtract that from the 40 students in the class.",
            "Here is an example. In a class of 20, 10 play cricket, 8 play football, and 3 play both. At least one game: 10 plus 8, minus 3, which is 15. Neither game: 20 minus 15, which is 5 students.",
        ],
        "steps": [
            "Add the two groups: 18 plus 15 is 33. The 6 students who went to both places are counted twice in this total.",
            "Take the 6 away once: 33 minus 6 is 27 students, who have been to at least one of the places.",
            "The rest of the class went to neither: 40 minus 27 is 13. So 13 students have not been to Delhi or Kashmir.",
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
            "Every student speaks Hindi, Marathi, or both. So the students who do not speak Hindi must speak only Marathi.",
            "21 of the 30 students speak Hindi. This already includes the 5 who speak both. 30 minus 21 is 9.",
            "So, 9 students speak only Marathi.",
        ],
    },
    "EXT_G5_WS_B2_029": {
        "q": "Four players joined a chess tournament. Each player played one game against the other players. How many games were played in all, in this tournament?",
        "hints": [
            "Each game needs two players. So count the pairs of players, taking care not to count the same game twice.",
            "Call the players A, B, C and D. A plays 3 games, against B, C and D. B has already played A, so count only B's new games. Carry on for C.",
            "Here is an example with 3 players, A, B and C. A plays B and C, which is 2 games. Then B plays C, which is 1 new game. The total is 2 plus 1, which is 3 games.",
        ],
        "steps": [
            "Call the players A, B, C and D. Each game is played by one pair of players.",
            "A plays B, C and D: 3 games. B has already played A, so B has 2 new games, against C and D. C has 1 new game, against D. D has no new games.",
            "3 plus 2 plus 1 is 6. So 6 games were played in all.",
        ],
    },
    "EXT_G5_WS_B2_030": {
        "q": "At a meeting, 13 people shook hands with each other. How many handshakes took place in all?",
        "hints": [
            "Each handshake is between two people. Count the pairs of people, taking care not to count the same handshake twice.",
            "Each of the 13 people shakes hands with the 12 others, which looks like 13 times 12. But that counts every handshake twice, once for each person in it. So, what must you do to 13 times 12?",
            "Here is an example with 4 people. Each shakes hands with 3 others: 4 times 3 is 12. Every handshake was counted twice, so there are 12 divided by 2, which is 6 handshakes.",
        ],
        "steps": [
            "Each of the 13 people shakes hands with the 12 others: 13 times 12 is 156.",
            "This counts every handshake twice, once for each of the two people in it. So divide by 2.",
            "156 divided by 2 is 78. So 78 handshakes took place in all.",
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
            "The sweets are shared equally among all 25 students. So a boy gets the same amount as any other student. The numbers of girls and boys do not matter.",
            "Change 12.5 kilograms into grams first. 1 kilogram is 1000 grams, so 12.5 kilograms is 12500 grams. Then share 12500 grams equally among 25 students.",
            "Here is an example. 1.5 kilograms of rice is shared equally among 5 families. 1.5 kilograms is 1500 grams, and 1500 divided by 5 is 300. So each family gets 300 grams.",
        ],
        "steps": [
            "The sweets are shared equally among all 25 students, so each boy gets the same as every other student.",
            "Change kilograms to grams: 12.5 kilograms is 12.5 times 1000 grams, which is 12500 grams.",
            "12500 divided by 25 is 500. So each boy received 500 grams of sweets.",
        ],
    },
    "EXT_G5_WS_B3_019": {
        "q": "Instead of multiplying, a student divided a number by 13, and got 11 as the quotient, and 4 as the remainder. What was the correct answer to the problem?",
        "hints": [
            "First, find the number the student started with. In a division, the number equals divisor times quotient, plus remainder.",
            "The number is 13 times 11, plus 4. Work that out. Then do what the student was meant to do: multiply that number by 13.",
            "Here is an example. A student divided a number by 5, and got quotient 3, and remainder 1. The number is 5 times 3, plus 1, which is 16. He should have multiplied: 16 times 5 is 80.",
        ],
        "steps": [
            "Find the number. Divisor times quotient, plus remainder, is 13 times 11, plus 4. That is 143 plus 4, which is 147.",
            "The student should have multiplied this number by 13: 147 times 13 is 1911.",
            "So, the correct answer to the problem was 1911.",
        ],
    },
    "EXT_G5_WS_B3_025": {
        "q": "In a basket, there are 56 apples. Amey takes out 4 apples at a time, and replaces them with 3 oranges. He continues this process till all the apples in the basket are replaced. How many oranges will there be in the basket in the end?",
        "hints": [
            "Each turn, 4 apples come out, and 3 oranges go in. So first, count how many turns it takes to remove all 56 apples.",
            "The number of turns is 56 divided by 4. Each turn puts 3 oranges in the basket, so multiply the number of turns by 3.",
            "Here is an example. A basket has 10 apples. Each turn, 2 apples are swapped for 1 orange. That takes 10 divided by 2, which is 5 turns. So there are 5 times 1, which is 5 oranges, at the end.",
        ],
        "steps": [
            "Amey removes 4 apples each turn. So emptying 56 apples takes 56 divided by 4, which is 14 turns.",
            "Each turn, he puts in 3 oranges: 14 times 3 is 42.",
            "So, there will be 42 oranges in the basket in the end.",
        ],
    },
    "EXT_G5_WS_B3_028": {
        "q": "Four years hence, Siya will be 3 years older than Diya. The sum of their present ages is 35 years. How old is Siya at present?",
        "hints": [
            "The gap between two people's ages never changes. If Siya will be 3 years older in four years, she is 3 years older right now too.",
            "Their ages add up to 35, and Siya's is 3 more than Diya's. Take the extra 3 away: 35 minus 3 is 32. That is two equal parts, each one Diya's age. Find Diya's age, then add 3.",
            "Here is an example. Anu is 5 years older than Binu, and their ages add up to 25. 25 minus 5 is 20, and 20 divided by 2 is 10. So Binu is 10, and Anu is 10 plus 5, which is 15.",
        ],
        "steps": [
            "The gap between two ages never changes. So Siya is 3 years older than Diya now as well.",
            "Take the extra 3 years away from the sum: 35 minus 3 is 32. This is twice Diya's age, so Diya is 32 divided by 2, which is 16 years old.",
            "Siya is 16 plus 3, which is 19. So Siya is 19 years old at present.",
        ],
    },
    "EXT_G5_WS_B3_030": {
        "q": "At a sports meet, there were 14 events, and in each event, gold, silver and bronze medals were awarded. If the total number of medals won by boys is 6 less than those won by the girls, how many medals did the boys win?",
        "hints": [
            "First, find the total number of medals: 14 events, with 3 medals in each. Then split that total between boys and girls, with the boys getting 6 fewer.",
            "There are 14 times 3, which is 42 medals. Take away the girls' extra 6: 42 minus 6 is 36. Now both shares are equal, and each one equals the boys' share.",
            "Here is an example. 20 sweets are shared, so that Ravi gets 4 fewer than Sita. 20 minus 4 is 16, and 16 divided by 2 is 8. So Ravi gets 8, and Sita gets 12.",
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
            "She has the same number of each note. So group the notes into sets of one 5 rupee, one 10 rupee, and one 20 rupee note.",
            "One set is worth 5 plus 10 plus 20, which is 35 rupees. Work out how many such sets make 910 rupees. That is the number of notes of each kind.",
            "Here is an example. Ali has equal numbers of 1 rupee and 2 rupee coins, worth 30 rupees in all. One set is worth 1 plus 2, which is 3 rupees, and 30 divided by 3 is 10. So he has 10 coins of each kind.",
        ],
        "steps": [
            "The value of one set is 5 plus 10 plus 20, which is 35.",
            "The number of each is 910 divided by 35, which is 26.",
        ],
    },
    "EXT_G5_WS_B3_033": {
        "q": "Minal purchased an equal number of stamps of 5 paise, 20 paise and 25 paise. She paid 9 rupees in all for these stamps. What is the total number of stamps that Minal bought?",
        "hints": [
            "She bought the same number of each stamp. Group them into sets of one 5 paise, one 20 paise, and one 25 paise stamp. Remember, 1 rupee is 100 paise.",
            "One set costs 5 plus 20 plus 25, which is 50 paise, and 9 rupees is 900 paise. Find how many sets she bought. Each set has 3 stamps, so multiply the number of sets by 3.",
            "Here is an example. Equal numbers of 10 paise and 15 paise stamps cost 1 rupee in all. One set costs 25 paise, and 100 divided by 25 is 4 sets. Each set has 2 stamps, so that is 4 times 2, which is 8 stamps.",
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
            "Two things change here: the number of people, and the number of days. Deal with one at a time.",
            "24 people is 24 divided by 6, which is 4 groups of six, and each group eats 1 kilogram a day. Find how much 24 people eat in one day, then multiply by the 7 days in a week.",
            "Here is an example. 3 people eat 2 kilograms of rice a day. 6 people are 2 groups of three, so they eat 2 times 2, which is 4 kilograms a day. In 3 days, they eat 4 times 3, which is 12 kilograms.",
        ],
        "steps": [
            "24 people is 4 groups of 6, which means 4 kilograms a day.",
            "7 days, times 4 kilograms a day, is 28 kilograms.",
        ],
    },
    "EXT_G5_WS_B3_040": {
        "q": "In a school, there are 4 girls for every 7 boys, and for every 55 students, there is a teacher. If the total strength of the boys in the school is 455, how many teachers are there in the school?",
        "hints": [
            "First, find the number of girls from the boys. Then the total number of students. And last, the number of teachers.",
            "There are 7 boys in each group, and 455 divided by 7 is 65 groups. Each group also has 4 girls. Find the girls, add the boys to get all the students, then count how many 55s are in that total.",
            "Here is an example. 2 girls for every 3 boys, and 30 boys. That is 30 divided by 3, which is 10 groups. So 10 times 2 is 20 girls, and 50 students. With one teacher for every 25 students, 50 divided by 25 is 2 teachers.",
        ],
        "steps": [
            "There are 455 boys, and the ratio is 4 is to 7. So the girls are 455 times 4 over 7, which is 260.",
            "The total number of students is 715.",
            "Teachers: 715 divided by 55, which is 13.",
        ],
    },
}
