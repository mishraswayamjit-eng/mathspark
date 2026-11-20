"""Lessons written one by one: G4A_AGES_022 to G4A_AGES_031."""
from g4_gr4_ratio_lib import (A, C, F, G, Lb, N, U, W, X, ask, bar, bars, beat, lesson, segs)

LESSONS = {}
L = LESSONS

L["G4A_AGES_022"] = lesson(
    beat("Aman is twice as old as Bhavna. Four years ago, Aman was three times as old as Bhavna was then. How old is Bhavna now?",
         G("q1", "Aman is twice as old as Bhavna"), G("q2", "4 years ago, Aman was 3 times as old as Bhavna"),
         G("q3", "Bhavna now = ?")),
    beat("Two clues, and both must be true. A good plan: try an age for Bhavna, use the first clue to get Aman's age, then test the second clue."),
    beat("Try Bhavna as 12. Then Aman is twice that, which is 24. Four years ago they were 8 and 20.",
         W("w1", "2 × 12 = 24"), W("w2", "12 − 4 = 8"), W("w3", "24 − 4 = 20")),
    beat("Four years ago Aman should be 3 times as old as Bhavna. Is 20 equal to 3 times 8?",
         ask=ask(["yes, it fits", "not quite: 3 × 8 = 24"], 1, "3 times 8 is 24. But Aman was 20 then, so the second clue does not fit.")),
    beat("So 12 does not work. Cross it out, and let us try a smaller age: 8.", X("w1", "12")),
    beat("If Bhavna is 8, Aman is twice that, which is 16. Four years ago they were 4 and 12.",
         W("w4", "2 × 8 = 16"), W("w5", "8 − 4 = 4"), W("w6", "16 − 4 = 12")),
    beat("And 3 times 4 is 12. Yes! This time both clues fit.", W("w7", "3 × 4 = 12")),
    beat("So Bhavna is 8 years old now.", A("ans", "Bhavna is 8 years old now"), C("ans", "8")),
    beat("Mind the traps. 16 is Aman's age. And 4 was Bhavna's age four years ago. The question asks for Bhavna now."),
    beat("When two clues must both be true, try an age, and test it against every clue."),
)

L["G4A_AGES_023"] = lesson(
    beat("A grandfather is 9 times as old as his grandson. Their ages add up to 70. How old will the grandfather be when the grandson is 10?",
         G("q1", "Grandfather is 9 times as old as his grandson"), G("q2", "Their ages add up to 70"),
         G("q3", "Grandfather's age when the grandson is 10 = ?")),
    beat("The grandson is 1 block and the grandfather is 9 blocks. Together that is 10 blocks.",
         F(bars(bar("Grandson", segs(1, "a")), bar("Grandfather", segs(9, "b")))), W("w1", "1 + 9 = 10")),
    beat("10 blocks make 70, so one block is 7. The grandson is 7 now, and the grandfather is 9 times 7, which is 63.",
         W("w2", "70 ÷ 10 = 7"), W("w3", "9 × 7 = 63"), N("w3", "63", "grandfather now")),
    beat("The grandson is 7 now. In how many years will he be 10?",
         ask=ask(["3 years", "7 years", "10 years"], 0, "From 7 up to 10 is 3 steps: 8, 9, 10. So 3 years.")),
    beat("10 minus 7 is 3. So we move 3 years ahead.", W("w4", "10 − 7 = 3")),
    beat("Now the trap. Do we multiply by 9 again? We do not. He is 9 times as old only today. Later on, both of them simply grow 3 years older."),
    beat("63 plus 3 is 66. So the grandfather will be 66 years old.",
         W("w5", "63 + 3 = 66"), A("ans", "The grandfather will be 66 years old"), C("ans", "66")),
    beat("So find both ages now, using blocks. Then move both people forward by the same number of years."),
)

L["G4A_AGES_024"] = lesson(
    beat("Neel says that in 6 years he will be twice as old as he was 2 years ago. How old is Neel now?",
         G("q1", "In 6 years, Neel will be twice as old"), G("q2", "as he was 2 years ago. Neel now = ?")),
    beat("There are two moments: 2 years ago, and 6 years from now. At the later moment he is twice as old. So the earlier age is 1 block, and the later age is 2 blocks.",
         F(bars(bar("2 years ago", segs(1, "a")), bar("In 6 years", segs(1, "a") + segs(1, "c"))))),
    beat("How many years are there from 2 years ago to 6 years from now?",
         ask=ask(["4 years", "6 years", "8 years"], 2, "From 2 years ago up to today is 2 years. From today onwards is 6 more. So 2 plus 6.")),
    beat("2 plus 6 is 8 years. In those 8 years his age grows by exactly one block. So one block is 8.", W("w1", "2 + 6 = 8"), N("w1", "8", "one block")),
    beat("That means 2 years ago Neel was 8.", Lb("w2", "2 years ago: Neel was 8")),
    beat("Come forward 2 years to today. 8 plus 2 is 10. So Neel is 10 now.",
         W("w3", "8 + 2 = 10"), A("ans", "Neel is 10 years old now"), C("ans", "10")),
    beat("Check: in 6 years he will be 16. And twice 8 is 16. It works.", W("c1", "10 + 6 = 16"), W("c2", "2 × 8 = 16")),
    beat("Careful: 8 was his age 2 years ago, and 16 will be his age in 6 years. Today he is 10."),
    beat("So mark the two moments, count the years between them, and ask what that stretch of time must equal."),
)

L["G4A_AGES_025"] = lesson(
    beat("Three sisters were born 2 years apart, one after another. Their ages add up to 27. How old is the youngest?",
         G("q1", "Three sisters, born 2 years apart"), G("q2", "Their ages add up to 27. Youngest = ?")),
    beat("Picture the three ages in a row. The youngest is 2 below the middle sister. The oldest is 2 above her. So the middle sister's age is the fair share."),
    beat("If the 27 years are shared equally among the three, what does each get?",
         ask=ask(["8", "9", "13"], 1, "Sharing equally among 3 means dividing by 3. 27 divided by 3 is 9.")),
    beat("27 divided by 3 is 9. That is the middle sister's age.", W("w1", "27 ÷ 3 = 9"), N("w1", "9", "middle sister")),
    beat("The youngest is 2 years younger than the middle one. 9 minus 2 is 7.", W("w2", "9 − 2 = 7")),
    beat("So the youngest sister is 7 years old.", A("ans", "The youngest sister is 7 years old"), C("ans", "7")),
    beat("Check: the oldest is 9 plus 2, which is 11. And 7 plus 9 plus 11 is 27. It fits.", W("c1", "9 + 2 = 11"), W("c2", "7 + 9 + 11 = 27")),
    beat("Careful: 9 is the middle sister and 11 is the oldest. The question wants the youngest."),
    beat("When ages are equally spaced, the middle one is the total divided by how many there are."),
)

L["G4A_AGES_026"] = lesson(
    beat("Five years ago a family had 4 members with an average age of 19. Since then a baby was born. Today the 5 members have an average age of 20. How old is the baby?",
         G("q1", "5 years ago: 4 members, average age 19"), G("q2", "Today: 5 members (a new baby), average age 20"),
         G("q3", "Baby's age = ?")),
    beat("An average hides a total. An average of 19 for 4 people means their ages added up to 4 times 19, which is 76.",
         W("w1", "4 × 19 = 76"), N("w1", "76", "total 5 years ago")),
    beat("Those same 4 people are each 5 years older today. How much bigger is their total now?",
         ask=ask(["4 years", "5 years", "20 years"], 2, "Each of the 4 people grew 5 years older. That is 5, four times over: 4 times 5.")),
    beat("4 times 5 is 20. So today those four add up to 76 plus 20, which is 96.",
         W("w2", "4 × 5 = 20"), W("w3", "76 + 20 = 96"), N("w3", "96", "the 4 today")),
    beat("Now the whole family today: 5 members with an average of 20. Their total is 5 times 20, which is 100.",
         W("w4", "5 × 20 = 100"), N("w4", "100", "all 5 today")),
    beat("The only difference between those two totals is the baby. 100 minus 96 is 4.", W("w5", "100 − 96 = 4")),
    beat("So the baby is 4 years old.", A("ans", "The baby is 4 years old"), C("ans", "4")),
    beat("The trap is to compare 100 with 76 straight away. That forgets that the four older members have each grown 5 years."),
    beat("So turn averages into totals. Then remember that everyone grows older as time passes."),
)

L["G4A_AGES_027"] = lesson(
    beat("The ages of a father, a mother and their son add up to 75. The son is 3. What did the family's ages add up to five years ago?",
         G("q1", "Father + mother + son = 75 years. The son is 3."), G("q2", "Five years ago, the family's ages added up to ?")),
    beat("Five years ago. The son is only 3 now. So where was he five years ago?",
         ask=ask(["he was 2", "he was 8", "not born yet"], 2,
                 "He is 3 now, so he was born 3 years ago. Five years ago is before that. He was not in the family yet.")),
    beat("Not born yet! That is the trap in this question. Five years ago the family was only the father and the mother.",
         U("q1", "The son is 3")),
    beat("So take the son out. The parents add up to 75 minus 3, which is 72 now.", W("w1", "75 − 3 = 72"), N("w1", "72", "parents now")),
    beat("Five years ago the father was 5 years younger, and the mother was 5 years younger. 5 plus 5 is 10 years less.", W("w2", "5 + 5 = 10")),
    beat("72 minus 10 is 62. So five years ago the family's ages added up to 62 years.",
         W("w3", "72 − 10 = 62"), A("ans", "Five years ago: 62 years"), C("ans", "62")),
    beat("If we had taken 5 years off all three people, we would have counted a boy who was not there yet."),
    beat("So when you go back in time, check that each person had been born."),
)

L["G4A_AGES_028"] = lesson(
    beat("When Meera was born, her mother was 26. Today her mother is exactly 3 times as old as Meera. How old is her mother today?",
         G("q1", "When Meera was born, her mother was 26"), G("q2", "Today her mother is 3 times as old. Mother = ?")),
    beat("When Meera was 0, her mother was 26. So her mother is 26 years older than her. And that gap never changes.", U("q1", "26")),
    beat("Today the mother is 3 times as old. So Meera is 1 block and her mother is 3 blocks. The 2 extra blocks are the gap.",
         F(bars(bar("Meera", segs(1, "a")), bar("Mother", segs(1, "a") + segs(2, "c"))))),
    beat("The 2 extra blocks make 26 years. So how big is 1 block?",
         ask=ask(["13", "26", "52"], 0, "2 blocks are 26 years. One block is half of that: 26 divided by 2.")),
    beat("26 divided by 2 is 13. One block is 13, and that is Meera's age today.", W("w1", "26 ÷ 2 = 13"), N("w1", "13", "Meera today")),
    beat("Her mother is 3 blocks. 3 times 13 is 39. So her mother is 39 today.",
         W("w2", "3 × 13 = 39"), A("ans", "Her mother is 39 years old today"), C("ans", "39")),
    beat("Check: 39 minus 13 is 26. The gap is right, and 39 is 3 times 13.", W("c1", "39 − 13 = 26")),
    beat("Mind the traps. 26 is the gap, not Meera's age, so 26 times 3 does not work. And 13 is Meera, not her mother."),
    beat("So use the gap that never changes, together with the blocks."),
)

L["G4A_AGES_029"] = lesson(
    beat("Anu and Bela are 20 together. Bela and Charu are 26 together. Anu and Charu are 24 together. How old is Charu?",
         G("q1", "Anu + Bela = 20     Bela + Charu = 26"), G("q2", "Anu + Charu = 24     Charu = ?")),
    beat("Look at the three sums. Each girl appears in exactly two of them."),
    beat("So if we add all three sums together, what do we get?",
         ask=ask(["each girl counted once", "each girl counted twice", "each girl counted 3 times"], 1,
                 "Count the names. Anu is in two of the sums. Bela is in two. Charu is in two. So every girl is counted twice.")),
    beat("20 plus 26 plus 24 is 70. That is every girl counted twice.", W("w1", "20 + 26 + 24 = 70")),
    beat("So halve it. 70 divided by 2 is 35. The three girls together are 35 years.", W("w2", "70 ÷ 2 = 35"), N("w2", "35", "all three")),
    beat("Now the neat part. Anu and Bela together are 20. Take them away from 35, and only Charu is left.",
         U("q1", "Anu + Bela = 20"), W("w3", "35 − 20 = 15")),
    beat("35 minus 20 is 15. So Charu is 15 years old.", A("ans", "Charu is 15 years old"), C("ans", "15")),
    beat("Check: Anu is 35 minus 26, which is 9. And Anu plus Charu is 9 plus 15, which is 24. It fits.",
         W("c1", "35 − 26 = 9"), W("c2", "9 + 15 = 24")),
    beat("When everyone appears twice, add everything and halve. Then take away the pair you do not need."),
)

L["G4A_AGES_030"] = lesson(
    beat("A father is 40. His three children are 4, 6 and 8. After how many years will the father's age equal the sum of his children's ages?",
         G("q1", "Father is 40. His children are 4, 6 and 8."), G("q2", "After ? years: father = sum of the children")),
    beat("Today the children add up to 4 plus 6 plus 8, which is 18. The father is 40. So he is ahead by 40 minus 18, which is 22.",
         W("w1", "4 + 6 + 8 = 18"), W("w2", "40 − 18 = 22"), N("w2", "22", "the gap")),
    beat("Now watch one year go by. The father gains 1 year. But there are three children, and each gains 1. So the children's sum gains 3."),
    beat("So each year, by how much does the gap close?",
         ask=ask(["by 1", "by 2", "by 3"], 1, "The children's sum goes up by 3, but the father also goes up by 1. The children catch up by 3 minus 1.")),
    beat("3 minus 1 is 2. The gap closes by 2 every year. This is the trap: not by 3, because the father keeps growing older too.",
         W("w3", "3 − 1 = 2")),
    beat("The gap is 22, and it closes by 2 a year. 22 divided by 2 is 11.", W("w4", "22 ÷ 2 = 11")),
    beat("So it happens after 11 years.", A("ans", "After 11 years"), C("ans", "11")),
    beat("Check: in 11 years the father is 51. The children are 15, 17 and 19, and they add up to 51 too.",
         W("c1", "40 + 11 = 51"), W("c2", "15 + 17 + 19 = 51")),
    beat("So find the gap, find how fast it closes each year, and divide."),
)

L["G4A_AGES_031"] = lesson(
    beat("A mother was 28 when her twin daughters were born. Today the mother and the two twins add up to 64. How old is each twin?",
         G("q1", "Mother was 28 when her twins were born"), G("q2", "Today: mother + twin + twin = 64. Each twin = ?")),
    beat("On the day the twins were born, they were both 0. So the three ages added up to just 28.", W("w1", "28 + 0 + 0 = 28")),
    beat("Today the total is 64. So it has grown by 64 minus 28, which is 36.", W("w2", "64 − 28 = 36"), N("w2", "36", "growth")),
    beat("Each year that passes, how much does the total of the three ages grow?",
         ask=ask(["by 1", "by 2", "by 3"], 2,
                 "Three people each have a birthday: the mother and both twins. So the total goes up by 3 every year.")),
    beat("By 3 each year. The trap is to forget the mother. She grows older too!"),
    beat("The total grew by 36, at 3 a year. 36 divided by 3 is 12. So 12 years have passed.", W("w3", "36 ÷ 3 = 12")),
    beat("12 years since they were born. So each twin is 12 years old.", A("ans", "Each twin is 12 years old"), C("ans", "12")),
    beat("Check: the mother is 28 plus 12, which is 40. And 40 plus 12 plus 12 is 64. It fits.",
         W("c1", "28 + 12 = 40"), W("c2", "40 + 12 + 12 = 64")),
    beat("So count how many people are growing older. The total grows by that many every year."),
)
