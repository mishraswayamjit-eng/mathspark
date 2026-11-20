"""Lessons written one by one: G4A_AGES_010 to G4A_AGES_021."""
from g4_gr4_ratio_lib import (A, C, F, G, N, U, W, ask, bar, bars, beat, lesson, seg, segs)

LESSONS = {}
L = LESSONS

L["G4A_AGES_010"] = lesson(
    beat("Farhan is 11 years old. His sister Rehana is 3 years younger. How old was Rehana 2 years ago?",
         G("q1", "Farhan is 11. Rehana is 3 years younger."), G("q2", "How old was Rehana 2 years ago?")),
    beat("There are two steps here. First Rehana's age now. Then we go back 2 years."),
    beat("Rehana is 3 years younger than Farhan. So how old is she now?",
         ask=ask(["11 + 3 = 14", "11 − 3 = 8", "11 − 2 = 9"], 1, "Younger means a smaller age. So take 3 away from Farhan's 11.")),
    beat("11 minus 3 is 8. Rehana is 8 now.", W("w1", "11 − 3 = 8"), N("w1", "8", "Rehana now")),
    beat("But the question asks about 2 years ago. Ago means back in time, so her age was smaller. 8 minus 2 is 6.",
         U("q2", "2 years ago"), W("w2", "8 − 2 = 6")),
    beat("So Rehana was 6 years old.", A("ans", "Rehana was 6 years old"), C("ans", "6")),
    beat("Careful not to stop at 8. That is her age now. And 8 plus 2 would be her age two years from now, not two years ago."),
    beat("So find the age now first, then move along the timeline: back for ago, forward for after."),
)

L["G4A_AGES_011"] = lesson(
    beat("Diya is 7 and her mother is 35. After 7 years, how many times as old as Diya will her mother be?",
         G("q1", "Diya is 7. Her mother is 35."), G("q2", "After 7 years, mother = ? times Diya's age")),
    beat("Today her mother is 5 times as old, because 5 times 7 is 35. But be careful: that will not stay true. After 7 years both ages change.",
         W("w1", "5 × 7 = 35")),
    beat("After 7 years Diya will be 7 plus 7, which is 14. Her mother will be 35 plus 7, which is 42.",
         W("w2", "7 + 7 = 14"), N("w2", "14", "Diya"), W("w3", "35 + 7 = 42"), N("w3", "42", "mother")),
    beat("How do we find how many times as old the mother is?",
         ask=ask(["42 − 14", "42 + 14", "42 ÷ 14"], 2,
                 "42 minus 14 gives the gap in years. The words how many times ask how many 14s fit into 42, and that is dividing.")),
    beat("14 times 3 is 42. So 42 divided by 14 is 3.", W("w4", "14 × 3 = 42"), W("w5", "42 ÷ 14 = 3")),
    beat("So her mother will be 3 times as old as Diya.", A("ans", "Her mother will be 3 times as old"), C("ans", "3 times")),
    beat("Notice what happened. The gap stays at 28 years for ever. But the number of times changed, from 5 times down to 3 times.",
         W("c1", "42 − 14 = 28")),
    beat("So for how many times as old at a later date: find both new ages first, then divide."),
)

L["G4A_AGES_012"] = lesson(
    beat("The ages of Anu and her mother add up to 44 years. Anu is 8. How old was her mother when Anu was born?",
         G("q1", "Anu + her mother = 44 years. Anu is 8."), G("q2", "Mother's age when Anu was born = ?")),
    beat("First the mother's age now. Together they are 44, and Anu is 8. So her mother is 44 minus 8, which is 36.",
         W("w1", "44 − 8 = 36"), N("w1", "36", "mother now")),
    beat("Now go back to the day Anu was born. How many years ago was that?",
         ask=ask(["8 years ago", "36 years ago", "44 years ago"], 0, "Anu is 8 years old. So she was born 8 years ago.")),
    beat("Anu was born 8 years ago. Her mother was 8 years younger then. 36 minus 8 is 28.", W("w2", "36 − 8 = 28")),
    beat("So her mother was 28 years old when Anu was born.", A("ans", "Her mother was 28 years old"), C("ans", "28")),
    beat("Careful: 36 is her mother's age today. We had to take 8 away twice: once to split the sum, and once to go back in time."),
    beat("Check: when Anu was 0, her mother was 28. Today they are 8 and 36, and 8 plus 36 is 44. It fits.", W("c1", "8 + 36 = 44")),
    beat("So find the age now, then go back by the child's age to reach the day the child was born."),
)

L["G4A_AGES_013"] = lesson(
    beat("The ages of two sisters add up to 20 years. One is 4 years older than the other. How old is the older sister?",
         G("q1", "Two sisters' ages add up to 20"), G("q2", "One is 4 years older. The older sister = ?")),
    beat("Look at the bars. The older sister's bar is the same as the younger one's, plus 4 extra years.",
         F(bars(bar("Younger", [seg("?", 4, "a")]), bar("Older", [seg("?", 4, "a"), seg("4", 1, "c")])))),
    beat("If we take away those 4 extra years, what is left of the 20?",
         ask=ask(["10", "16", "24"], 1, "Taking away means subtracting. 20 minus 4 is 16.")),
    beat("20 minus 4 is 16. Now the two bars are equal, and together they make 16.", W("w1", "20 − 4 = 16")),
    beat("Half of 16 is 8. So the younger sister is 8.", W("w2", "16 ÷ 2 = 8"), N("w2", "8", "younger sister")),
    beat("The older sister gets her 4 years back. 8 plus 4 is 12. So the older sister is 12.",
         W("w3", "8 + 4 = 12"), A("ans", "The older sister is 12 years old"), C("ans", "12")),
    beat("Check: 8 plus 12 is 20, and 12 is 4 more than 8. Both clues fit.", W("c1", "8 + 12 = 20")),
    beat("The trap is to halve the 20 straight away. That would make the sisters the same age, and one is older."),
    beat("So: take away the extra, halve, then add the extra back for the older one."),
)

L["G4A_AGES_014"] = lesson(
    beat("A father is 3 times as old as his son. Their ages add up to 48 years. How old is the son?",
         G("q1", "A father is 3 times as old as his son"), G("q2", "Their ages add up to 48. The son = ?")),
    beat("Think of the son's age as 1 block. The father is 3 times as old, so he is 3 of the same blocks.",
         F(bars(bar("Son", segs(1, "a")), bar("Father", segs(3, "b"))))),
    beat("How many equal blocks are there altogether?",
         ask=ask(["2", "3", "4"], 2, "Count the son's own block too. 1 block for the son, and 3 for the father.")),
    beat("1 plus 3 is 4 blocks. This is the trap: do not forget the son's own block.", W("w1", "1 + 3 = 4")),
    beat("The 4 blocks add up to 48. So one block is 48 divided by 4, which is 12.", W("w2", "48 ÷ 4 = 12"), N("w2", "12", "one block")),
    beat("The son is one block. So the son is 12 years old.", A("ans", "The son is 12 years old"), C("ans", "12")),
    beat("Check: the father is 3 times 12, which is 36. And 12 plus 36 is 48. It fits.", W("c1", "3 × 12 = 36"), W("c2", "12 + 36 = 48")),
    beat("So when one age is so many times another, draw blocks, count them all, and share the total."),
)

L["G4A_AGES_015"] = lesson(
    beat("Three years ago, Kiran was 9 years old. How old will she be 4 years from now?",
         G("q1", "Three years ago, Kiran was 9"), G("q2", "How old will she be 4 years from now?")),
    beat("There are two jumps on the timeline: from the past up to today, and then from today into the future."),
    beat("First jump. She was 9 three years ago. So how old is she today?",
         ask=ask(["6", "9", "12"], 2, "From three years ago up to today, 3 years have passed. She is older now: 9 plus 3.")),
    beat("9 plus 3 is 12. Kiran is 12 today.", W("w1", "9 + 3 = 12"), N("w1", "12", "today")),
    beat("Second jump: 4 years from now. 12 plus 4 is 16.", W("w2", "12 + 4 = 16"),
         F({"kind": "numberLine", "min": 9, "max": 16, "step": 1,
            "points": [{"at": 9, "label": "then"}, {"at": 12, "label": "today"}],
            "hops": [{"from": 9, "to": 12, "label": "+ 3"}, {"from": 12, "to": 16, "label": "+ 4"}]})),
    beat("So Kiran will be 16 years old.", A("ans", "Kiran will be 16 years old"), C("ans", "16")),
    beat("The trap is to add the 4 straight to the 9. That skips the 3 years that have already gone by."),
    beat("A quick check: from three years ago to four years ahead is 7 years in all. And 9 plus 7 is 16.",
         W("c1", "3 + 4 = 7"), W("c2", "9 + 7 = 16")),
    beat("So always find today's age first, then jump to the time the question asks about."),
)

L["G4A_AGES_016"] = lesson(
    beat("The ages of Geeta and Hari add up to 25 years now. What did their ages add up to 3 years ago?",
         G("q1", "Geeta + Hari = 25 years now"), G("q2", "What did their ages add up to 3 years ago?")),
    beat("Three years ago. So we go back in time, and the ages were smaller."),
    beat("How many people were 3 years younger back then?",
         ask=ask(["only Geeta", "only Hari", "both of them"], 2,
                 "Time goes back for everybody. Geeta was 3 years younger, and Hari was 3 years younger too.")),
    beat("Geeta was 3 years younger, and so was Hari. 3 plus 3 is 6. So the sum was 6 years smaller.", W("w1", "3 + 3 = 6")),
    beat("25 minus 6 is 19. So three years ago their ages added up to 19 years.",
         W("w2", "25 − 6 = 19"), A("ans", "Their ages added up to 19 years"), C("ans", "19")),
    beat("The trap is to take away 3 only once. The sum has two people in it, so the 3 comes off twice."),
    beat("Let us test it with real ages. Say Geeta is 12 and Hari is 13 now. Three years ago they were 9 and 10, which adds up to 19.",
         W("c1", "12 + 13 = 25"), W("c2", "9 + 10 = 19")),
    beat("So when a sum of ages moves in time, it moves once for every person in it."),
)

L["G4A_AGES_017"] = lesson(
    beat("Jay's grandfather is 72. Jay's father is half as old as the grandfather. Jay is one-quarter as old as his father. How old is Jay?",
         G("q1", "Grandfather is 72. Father is half as old."), G("q2", "Jay is one-quarter as old as his father. Jay = ?")),
    beat("We work down the family, one step at a time. First the father. Half of 72 is 36. So the father is 36.",
         W("w1", "72 ÷ 2 = 36"), N("w1", "36", "father")),
    beat("Jay is one-quarter as old as his father. So we take one-quarter of which number?",
         ask=ask(["36", "72"], 0,
                 "Read it again: one-quarter as old as his father. The father is 36, so we take a quarter of 36, not of the grandfather's 72.")),
    beat("One-quarter means 4 equal parts. So divide 36 by 4. 36 divided by 4 is 9.", U("q2", "his father"), W("w2", "36 ÷ 4 = 9")),
    beat("So Jay is 9 years old.", A("ans", "Jay is 9 years old"), C("ans", "9")),
    beat("Check by climbing back up the family. 9 times 4 is 36, the father. And 36 times 2 is 72, the grandfather.",
         W("c1", "9 × 4 = 36"), W("c2", "36 × 2 = 72")),
    beat("So use each age to find the next one. Half means divide by 2. One-quarter means divide by 4."),
)

L["G4A_AGES_018"] = lesson(
    beat("Varun is 9 years old. His father is 27 years older than him. How old will his father be when Varun is 15?",
         G("q1", "Varun is 9. His father is 27 years older."), G("q2", "Father's age when Varun is 15 = ?")),
    beat("Here is the key fact about ages. The gap between two people never changes. The father is 27 years older today, and he always will be.",
         U("q1", "27 years older")),
    beat("So when Varun is 15, how do we find his father's age?",
         ask=ask(["9 + 27", "15 + 27", "15 + 9"], 1,
                 "At that time Varun is 15, and his father is still 27 years older than him. So add 27 to 15.")),
    beat("15 plus 27. First 15 plus 20 is 35. Then 7 more is 42.", W("w1", "15 + 20 = 35"), W("w2", "35 + 7 = 42"), W("w3", "15 + 27 = 42")),
    beat("So his father will be 42 years old.", A("ans", "His father will be 42 years old"), C("ans", "42")),
    beat("Here is another way. The father is 9 plus 27, which is 36 now. Varun reaches 15 in 6 years, and 36 plus 6 is 42. The same answer.",
         W("c1", "9 + 27 = 36"), W("c2", "15 − 9 = 6"), W("c3", "36 + 6 = 42")),
    beat("Careful: 36 is the father's age now. The question asks for his age later, when Varun is 15."),
    beat("So remember: the gap between two ages stays the same for ever. Use it at any time you like."),
)

L["G4A_AGES_019"] = lesson(
    beat("Rahul is 10 and his father is 40. After how many years will the father be 3 times as old as Rahul?",
         G("q1", "Rahul is 10. His father is 40."), G("q2", "After ? years, father = 3 times Rahul's age")),
    beat("Today the father is 4 times as old, since 4 times 10 is 40. As the years pass, both ages go up together, and that number of times gets smaller."),
    beat("One thing never changes: the gap. 40 minus 10 is 30. The father is always 30 years older.",
         W("w1", "40 − 10 = 30"), N("w1", "30", "the gap")),
    beat("When the father is 3 times as old, picture Rahul as 1 block and his father as 3 blocks. The father's 2 extra blocks are the gap.",
         F(bars(bar("Rahul", segs(1, "a")), bar("Father", segs(1, "a") + segs(2, "c"))))),
    beat("The 2 extra blocks make 30 years. So how big is 1 block?",
         ask=ask(["10", "15", "30"], 1, "2 blocks are 30 years. So one block is half of 30.")),
    beat("30 divided by 2 is 15. One block is Rahul's age at that time. So Rahul will be 15.",
         W("w2", "30 ÷ 2 = 15"), N("w2", "15", "Rahul then")),
    beat("Rahul is 10 now. He will be 15 after 15 minus 10, which is 5 years.",
         W("w3", "15 − 10 = 5"), A("ans", "After 5 years"), C("ans", "5")),
    beat("Check: after 5 years the father is 45. And 3 times 15 is 45. It works.", W("c1", "40 + 5 = 45"), W("c2", "3 × 15 = 45")),
    beat("You could also test a choice. After 10 years they would be 20 and 50. But 3 times 20 is 60, not 50. So 10 years is too late.",
         W("c3", "10 + 10 = 20"), W("c4", "40 + 10 = 50"), W("c5", "3 × 20 = 60")),
    beat("So use the gap. It never changes, and here it is 2 blocks. The answer is after 5 years."),
)

L["G4A_AGES_020"] = lesson(
    beat("Ali is 14 and his sister Sara is 8. How old was Ali when Sara was exactly half his age?",
         G("q1", "Ali is 14. His sister Sara is 8."), G("q2", "Ali's age when Sara was half his age = ?")),
    beat("Start with the gap. 14 minus 8 is 6. Ali is always 6 years older than Sara.", W("w1", "14 − 8 = 6"), N("w1", "6", "the gap")),
    beat("When Sara is half of Ali's age, Sara is 1 block and Ali is 2 blocks. So Ali's extra block, the gap, is the same size as Sara's age.",
         F(bars(bar("Sara", segs(1, "a")), bar("Ali", segs(1, "a") + segs(1, "c"))))),
    beat("The gap is 6 years. So how old was Sara at that time?",
         ask=ask(["4", "6", "7"], 1, "Sara's block and the gap block are the same size. The gap is 6, so Sara was 6.")),
    beat("Sara was 6. Ali was 6 years older: 6 plus 6 is 12.", W("w2", "6 + 6 = 12")),
    beat("So Ali was 12 years old.", A("ans", "Ali was 12 years old"), C("ans", "12")),
    beat("Check: half of 12 is 6. Yes, Sara was exactly half of Ali's age.", W("c1", "12 ÷ 2 = 6")),
    beat("Two traps. 6 was Sara's age, but the question asks for Ali. And half of 14 is 7, but when Ali was 7, Sara was only 1."),
    beat("So when one person is double the other, the younger one's age is equal to the gap."),
)

L["G4A_AGES_021"] = lesson(
    beat("Five years ago, a mother was 7 times as old as her daughter. The mother is 33 now. How old is the daughter now?",
         G("q1", "Five years ago: mother = 7 times daughter"), G("q2", "Mother is 33 now. Daughter now = ?")),
    beat("The 7 times clue is about five years ago. So we must go back to that time before we use it. That is the trap: do not divide 33 by 7.",
         U("q1", "Five years ago")),
    beat("Five years ago the mother was 33 minus 5, which is 28.", W("w1", "33 − 5 = 28"), N("w1", "28", "mother then")),
    beat("Back then she was 7 times as old as her daughter. So how old was the daughter then?",
         ask=ask(["28 × 7", "28 ÷ 7 = 4", "28 − 7 = 21"], 1,
                 "The mother's age was 7 times the daughter's. So the daughter's age is the mother's 28 shared into 7 equal parts.")),
    beat("28 divided by 7 is 4. The daughter was 4 years old then.", W("w2", "28 ÷ 7 = 4"), N("w2", "4", "daughter then")),
    beat("Now come back to today. 5 years have passed, so the daughter is 4 plus 5, which is 9.", W("w3", "4 + 5 = 9")),
    beat("So the daughter is 9 years old now.", A("ans", "The daughter is 9 years old now"), C("ans", "9")),
    beat("Careful to add the 5 years just once, and only at the end. 4 was her age back then. 9 is her age now."),
    beat("So go to the time the clue talks about, do the sum there, then come back to today."),
)
