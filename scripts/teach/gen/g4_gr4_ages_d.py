"""Lessons written one by one: G4A_AGES_032 to G4A_AGES_039, PYQ_2016_Q10 and PYQ_2019_Q05."""
from g4_gr4_ratio_lib import (A, C, F, G, Lb, N, U, W, ask, bar, bars, beat, lesson, seg, segs)
from g4_gr4_ages_a import couple_and_son

LESSONS = {}
L = LESSONS

L["G4A_AGES_032"] = lesson(
    beat("A father's age and his son's age use the same two digits, swapped round. The father is 27 years older. The son is a teenager, 13 to 19. How old is the father?",
         G("q1", "Father's and son's ages: same 2 digits, swapped"), G("q2", "Father is 27 years older. Son is 13 to 19."),
         G("q3", "Father = ?")),
    beat("The son is a teenager, so there are only a few ages to test. For each one, swap the digits to get the father's age, then check the gap of 27."),
    beat("Start with 13. Swap the digits and we get 31. The gap is 31 minus 13, which is 18. Too small.", W("w1", "31 − 13 = 18")),
    beat("Next, the son is 14. Swap the digits. How old is the father?",
         Lb("t1", "Next try: the son is 14"),
         ask=ask(["15", "41", "44"], 1, "14 is written with a 1 and a 4. Swap them round and we get 41.")),
    beat("41 minus 14 is 27. That is exactly the gap we want!", W("w2", "41 − 14 = 27"), C("w2", "27")),
    beat("Should we keep going? Try 15 and 51: they are 36 apart. Each year older for the son makes the gap bigger. So 14 is the only one.",
         W("w3", "51 − 15 = 36")),
    beat("So the son is 14 and the father is 41 years old.", A("ans", "The father is 41 years old"), C("ans", "41")),
    beat("Other pairs, like 25 and 52, are also 27 apart. But a son of 25 is not a teenager. Every clue must fit.", W("c1", "52 − 25 = 27")),
    beat("When only a few ages are possible, test them one by one against every clue."),
)

L["G4A_AGES_033"] = lesson(
    beat("Asha is 8. She tells her older sister Bina: when I am as old as you are now, you will be 20. How old is Bina now?",
         G("q1", "Asha is 8. Bina is older."), G("q2", "When Asha is as old as Bina is now, Bina will be 20"),
         G("q3", "Bina now = ?")),
    beat("Let us untangle Asha's sentence. Asha needs some years to reach Bina's age. In those very same years, Bina grows too, and reaches 20."),
    beat("So there are two equal steps. One from 8 up to Bina's age now. And one from Bina's age now up to 20.",
         F(bars(bar(None, [seg("step", 1, "a"), seg("step", 1, "b")], brace="from 8 to 20")))),
    beat("The two equal steps together go from 8 to 20. How long are the two steps together?",
         ask=ask(["12 years", "20 years", "28 years"], 0, "From 8 up to 20: take 8 away from 20.")),
    beat("20 minus 8 is 12. That is two steps. So one step is 12 divided by 2, which is 6 years.",
         W("w1", "20 − 8 = 12"), W("w2", "12 ÷ 2 = 6"), N("w2", "6", "one step")),
    beat("Bina's age is one step above Asha's 8. 8 plus 6 is 14. So Bina is 14 now.",
         W("w3", "8 + 6 = 14"), A("ans", "Bina is 14 years old now"), C("ans", "14")),
    beat("Check: in 6 years Asha will be 14, which is Bina's age now. And Bina will be 14 plus 6, which is 20. Just as Asha said.",
         W("c1", "14 + 6 = 20")),
    beat("The trap is to stop at 12. That is two steps, not Bina's age. Bina is exactly halfway between 8 and 20."),
    beat("So the gap between two sisters stays the same. Here it fits twice between 8 and 20."),
)

L["G4A_AGES_034"] = lesson(
    beat("Ravi's age this year is a multiple of 3. Last year it was a multiple of 4. Next year it will be a multiple of 5. He is under 60. How old is he?",
         G("q1", "This year: a multiple of 3. Last year: a multiple of 4."), G("q2", "Next year: a multiple of 5. Under 60. Ravi = ?")),
    beat("Three clues, and all must be true together. Let us start with the easiest one to spot: next year's age is a multiple of 5."),
    beat("Multiples of 5 end in 0 or 5. So what digit does this year's age end in?",
         ask=ask(["0 or 5", "1 or 6", "9 or 4"], 2,
                 "This year is 1 less than next year. 1 less than a number ending in 0 ends in 9. 1 less than a number ending in 5 ends in 4.")),
    beat("So this year's age ends in 9 or 4. Which of those, under 60, are multiples of 3? They are 9, 24, 39 and 54.",
         Lb("w1", "Ends in 9 or 4, multiple of 3: 9, 24, 39, 54")),
    beat("Now the last clue. Take 1 away from each to get last year's age: 8, 23, 38 and 53.", Lb("w2", "Last year: 8, 23, 38, 53")),
    beat("Which of those is a multiple of 4?",
         ask=ask(["8", "23", "38"], 0, "4 times 2 is 8. None of the others is in the 4 times table.")),
    beat("Only 8 works. So last year Ravi was 8, and this year he is 9.",
         W("w3", "4 × 2 = 8"), A("ans", "Ravi is 9 years old this year"), C("ans", "9")),
    beat("Check all three clues. 9 is 3 times 3. Last year's 8 is 4 times 2. Next year's 10 is 5 times 2. All of them fit.",
         W("c1", "3 × 3 = 9"), W("c2", "5 × 2 = 10")),
    beat("Look at 21. It is a multiple of 3, and last year's 20 is a multiple of 4. Tempting! But next year's 22 is not a multiple of 5. Every clue must fit.",
         Lb("c3", "21: last year 20 fits, next year 22 does not")),
    beat("With several clues, use one to make a short list, then test the list against the others."),
)

L["G4A_AGES_035"] = lesson(
    beat("Ritu and her two brothers are all more than 4 years old. Five years from now their ages will add up to 50. What did they add up to 2 years ago?",
         G("q1", "Ritu and her 2 brothers: three children"), G("q2", "In 5 years their ages will add up to 50"),
         G("q3", "What did they add up to 2 years ago?")),
    beat("We are given a sum in the future and asked for a sum in the past. And there are three children, so every year counts three times."),
    beat("From 5 years ahead, back to 2 years ago. How many years back is that altogether?",
         ask=ask(["3 years", "5 years", "7 years"], 2, "First 5 years back to today, then 2 more years back. So 5 plus 2.")),
    beat("5 plus 2 is 7 years back.", W("w1", "5 + 2 = 7")),
    beat("Each of the three children was 7 years younger. So the sum was smaller by 3 times 7, which is 21. The trap is to take 7 off only once.",
         W("w2", "3 × 7 = 21")),
    beat("50 minus 21 is 29. So two years ago their ages added up to 29 years.",
         W("w3", "50 − 21 = 29"), A("ans", "Two years ago: 29 years"), C("ans", "29")),
    beat("Check in two steps. Back to today: take off 3 times 5, which is 15, leaving 35. Back 2 more years: take off 3 times 2, which is 6, leaving 29.",
         W("c1", "50 − 15 = 35"), W("c2", "35 − 6 = 29")),
    beat("And why are we told they are all more than 4 years old? So that we know all three were already born 2 years ago."),
    beat("So when a sum of ages moves in time, multiply the years by the number of people."),
)

L["G4A_AGES_036"] = lesson(
    beat("A mother is 5 times as old as her daughter. In 6 years their ages will add up to 60. How old is the daughter now?",
         G("q1", "A mother is 5 times as old as her daughter"), G("q2", "In 6 years their ages will add up to 60"),
         G("q3", "Daughter now = ?")),
    beat("One clue is about today: 5 times as old. The other is about 6 years from now: the sum of 60. We must bring them to the same time."),
    beat("In 6 years they add up to 60. So what do they add up to today?",
         ask=ask(["48", "54", "66"], 0,
                 "Both of them will be 6 years older. So today's sum is smaller by 6 for the mother, and by 6 again for the daughter.")),
    beat("60, minus 6, minus 6, is 48. Two people, so the 6 comes off twice. That is the trap here.",
         W("w1", "60 − 6 − 6 = 48"), N("w1", "48", "sum today")),
    beat("Today the daughter is 1 block and the mother is 5 blocks. That is 6 blocks.",
         F(bars(bar("Daughter", segs(1, "a")), bar("Mother", segs(5, "b")))), W("w2", "1 + 5 = 6")),
    beat("6 blocks make 48. 48 divided by 6 is 8. The daughter is one block, so she is 8.",
         W("w3", "48 ÷ 6 = 8"), A("ans", "The daughter is 8 years old now"), C("ans", "8")),
    beat("Check: the mother is 5 times 8, which is 40. In 6 years they are 14 and 46, and 14 plus 46 is 60.",
         W("c1", "5 × 8 = 40"), W("c2", "14 + 46 = 60")),
    beat("So bring the sum to the same time as the other clue. Then use blocks."),
)

L["G4A_AGES_037"] = lesson(
    beat("The ages of two cousins multiply to give 84. The older one is 5 years older. What do their two ages add up to?",
         G("q1", "Two cousins: their ages multiply to give 84"), G("q2", "The older is 5 years older. Ages add up to ?")),
    beat("We need two numbers that multiply to 84. Let us list the pairs, starting small.",
         Lb("p1", "1 × 84     2 × 42     3 × 28"), Lb("p2", "4 × 21     6 × 14     7 × 12")),
    beat("We want the pair that is 5 apart. Which one is it?",
         ask=ask(["4 and 21", "6 and 14", "7 and 12"], 2,
                 "Find the gap in each pair. 4 and 21 are much too far apart. 14 minus 6 is 8. But 12 minus 7 is 5.")),
    beat("12 minus 7 is 5, and 7 times 12 is 84. So the cousins are 7 and 12.", C("p2", "7 × 12"), W("w1", "12 − 7 = 5"), W("w2", "7 × 12 = 84")),
    beat("Now read the question again. It does not ask for either age. It asks what the two ages add up to.", U("q2", "add up to")),
    beat("7 plus 12 is 19. So their ages add up to 19.", W("w3", "7 + 12 = 19"), A("ans", "Their ages add up to 19"), C("ans", "19")),
    beat("Pairs like 6 and 14 also multiply to 84, but they are 8 apart, not 5. Both clues must fit."),
    beat("So list the pairs that multiply to the number, then pick the pair with the right gap."),
)

L["G4A_AGES_038"] = lesson(
    beat("Kabir's age in months is the same number as his grandfather's age in years. Their ages add up to 78 years. How old is Kabir?",
         G("q1", "Kabir's age in months = grandfather's age in years"), G("q2", "Their ages add up to 78 years. Kabir = ?")),
    beat("A strange clue! Let us try it out. If Kabir were 1 year old, he would be 12 months old. So his grandfather would be 12 years old.",
         Lb("f1", "1 year = 12 months")),
    beat("So the grandfather's age is always how many times Kabir's age?",
         ask=ask(["2 times", "12 times", "78 times"], 1,
                 "Every year of Kabir's age is 12 months. So the number of months is 12 times the number of years.")),
    beat("So Kabir is 1 block and his grandfather is 12 blocks. Together that is 13 blocks.",
         F(bars(bar("Kabir", segs(1, "a")), bar("Grandfather", segs(12, "b")))), W("w1", "1 + 12 = 13")),
    beat("13 blocks make 78 years. 13 times 6 is 78, so one block is 6.", W("w2", "13 × 6 = 78"), W("w3", "78 ÷ 13 = 6")),
    beat("Kabir is one block. So Kabir is 6 years old.", A("ans", "Kabir is 6 years old"), C("ans", "6")),
    beat("Check: 6 years is 6 times 12, which is 72 months. So his grandfather is 72 years old. And 6 plus 72 is 78.",
         W("c1", "6 × 12 = 72"), W("c2", "6 + 72 = 78")),
    beat("Careful: 72 is the grandfather's age, and 12 is only the number of months in a year. The question asks for Kabir."),
    beat("So change both ages to the same unit, see how many times one is of the other, then use blocks."),
)

L["G4A_AGES_039"] = lesson(
    beat("Tara's age and her uncle's age are in the ratio 2 to 5. Six years ago they were in the ratio 1 to 4. How old is her uncle now?",
         G("q1", "Tara : her uncle = 2 : 5 now"), G("q2", "Six years ago it was 1 : 4. Uncle now = ?")),
    beat("Careful: the 2 and the 5 are not ages. They are parts. So we cannot just take 6 away from them. We need real ages."),
    beat("Real ages in the ratio 2 to 5 come from multiplying both by the same number. Both must be more than 6, so start at 8 and 20. Then 10 and 25, 12 and 30, 14 and 35.",
         Lb("w1", "Now: 8 and 20, 10 and 25, 12 and 30, 14 and 35")),
    beat("Take 6 years off each pair. We get 2 and 14, 4 and 19, 6 and 24, 8 and 29.",
         Lb("w2", "6 years ago: 2 and 14, 4 and 19, 6 and 24, 8 and 29")),
    beat("Six years ago the ratio was 1 to 4. So the uncle was 4 times Tara's age. Which pair fits?",
         ask=ask(["2 and 14", "4 and 19", "6 and 24"], 2,
                 "Multiply the smaller number by 4 and see if you get the bigger one. Only 4 times 6 gives its partner, 24.")),
    beat("4 times 6 is 24. So six years ago Tara was 6 and her uncle was 24.", W("w3", "4 × 6 = 24"), C("w2", "6 and 24")),
    beat("Come back to today. Tara is 6 plus 6, which is 12. Her uncle is 24 plus 6, which is 30.", W("w4", "6 + 6 = 12"), W("w5", "24 + 6 = 30")),
    beat("So her uncle is 30 years old now.", A("ans", "Her uncle is 30 years old now"), C("ans", "30")),
    beat("Check today's ratio. Divide 12 and 30 by 6 and we get 2 and 5. Yes, 2 to 5.", W("c1", "12 ÷ 6 = 2"), W("c2", "30 ÷ 6 = 5")),
    beat("So list real ages that fit one clue, then test them against the other clue."),
)

L["PYQ_2016_Q10"] = lesson(
    beat("Sarika was born in 2006 and Surya was born in 2013. In which year will Sarika be twice the age of Surya?",
         G("q1", "Sarika was born in 2006. Surya was born in 2013."), G("q2", "In which year is Sarika twice as old as Surya?")),
    beat("First, how much older is Sarika? 2013 minus 2006 is 7. Sarika is 7 years older, and she always will be.",
         W("w1", "2013 − 2006 = 7"), N("w1", "7", "the gap")),
    beat("When Sarika is twice Surya's age, Surya is 1 block and Sarika is 2 blocks. Sarika's extra block is the gap.",
         F(bars(bar("Surya", segs(1, "a")), bar("Sarika", segs(1, "a") + segs(1, "c"))))),
    beat("The gap is 7 years. So how old is Surya when Sarika is twice his age?",
         ask=ask(["3 and a half", "7", "14"], 1, "The extra block is the gap, which is 7. Surya's block is the same size. So Surya is 7.")),
    beat("Surya is 7, and Sarika is 7 plus 7, which is 14. And 14 is twice 7.", W("w2", "7 + 7 = 14")),
    beat("Now, in which year is Surya 7 years old? He was born in 2013, so add 7. 2013 plus 7 is 2020.", W("w3", "2013 + 7 = 2020")),
    beat("So the year is 2020.", A("ans", "The year is 2020"), C("ans", "2020")),
    beat("Check with Sarika. 2020 minus 2006 is 14. So in 2020 she is 14 and Surya is 7. Exactly twice.", W("c1", "2020 − 2006 = 14")),
    beat("What about 2019, one year earlier? Then they would be 13 and 6, and twice 6 is 12, not 13. So only 2020 works.",
         Lb("c2", "In 2019: Sarika 13, Surya 6"), W("c3", "2 × 6 = 12")),
    beat("The gap between two ages never changes. When one is double the other, the younger one's age equals the gap."),
)

L["PYQ_2019_Q05"] = couple_and_son(
    "6 years ago, the ages of a husband and wife added up to 48. Now the husband, wife and son add up to 63. What will the son's age be, 6 years hence?",
    "The word hence means from now. ")
