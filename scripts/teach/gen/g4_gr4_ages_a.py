"""Lessons written one by one: the three past-paper questions EXT_G4_FP_..., and G4A_AGES_001 to 009."""
from g4_gr4_ratio_lib import (A, C, F, G, Lb, N, U, W, ask, bar, bars, beat, lesson, seg, segs)

LESSONS = {}
L = LESSONS


def line(lo, hi, points=None, hops=None):
    spec = {"kind": "numberLine", "min": lo, "max": hi, "step": 1}
    if points:
        spec["points"] = [{"at": a, "label": t} for a, t in points]
    if hops:
        spec["hops"] = [{"from": a, "to": b, "label": t} for a, b, t in hops]
    return F(spec)


L["EXT_G4_FP_2021_010"] = lesson(
    beat("5 years ago, a mother's age and her daughter's age added up to 5 x. We want what they will add up to 5 years from now.",
         G("q1", "5 years ago: mother + daughter = 5x"), G("q2", "5 years from now: mother + daughter = ?")),
    beat("Do not worry about the 5 x. It is just a name for a number we are not told. All we need is how much the sum grows."),
    beat("From 5 years ago to 5 years from now. How many years is that?",
         ask=ask(["0 years", "5 years", "10 years"], 2,
                 "From 5 years ago up to today is 5 years. From today to 5 years ahead is 5 more. So 5 plus 5.")),
    beat("5 plus 5 is 10. So 10 years go by.", W("w1", "5 + 5 = 10")),
    beat("Now the trap. In those 10 years, how much does the sum of the two ages grow?",
         ask=ask(["by 5", "by 10", "by 20"], 2,
                 "The mother grows 10 years older. The daughter grows 10 years older too. Two people, so 10 and 10 more.")),
    beat("10 for the mother and 10 for the daughter. 10 plus 10 is 20. The sum grows by 20.", W("w2", "10 + 10 = 20")),
    beat("The sum was 5 x. Now it is 20 bigger. So the answer is 5 x plus 20.",
         A("ans", "Sum 5 years from now = 5x + 20"), C("ans", "5x + 20")),
    beat("Let us test it with real ages. Say they were 30 and 5 back then, which adds up to 35. Ten years on they are 40 and 15, which adds up to 55. And 55 is 35 plus 20.",
         W("c1", "30 + 5 = 35"), W("c2", "40 + 15 = 55"), W("c3", "35 + 20 = 55")),
    beat("When time passes, every person in the sum grows older. Two people, 10 years each, makes 20 more. So it is 5 x plus 20."),
)


def couple_and_son(opening, hence):
    return lesson(
        beat(opening,
             G("q1", "6 years ago: husband + wife = 48"), G("q2", "Now: husband + wife + son = 63"),
             G("q3", "Son's age 6 years from now = ?")),
        beat("Three different times are mixed up here: 6 years ago, now, and 6 years from now. " + hence + "Let us bring everything to now first."),
        beat("6 years ago the husband and wife added up to 48. What do the two of them add up to now?",
             ask=ask(["48", "54", "60"], 2, "The husband is 6 years older now, and the wife is 6 years older too. So add 6 twice.")),
        beat("48, plus 6 for the husband, plus 6 for the wife. That is 60. This is the trap: two people, so we add 6 twice.",
             W("w1", "48 + 6 + 6 = 60"), N("w1", "60", "husband + wife now")),
        beat("Now all three add up to 63. Take away the parents' 60 and the son is left. 63 minus 60 is 3. The son is 3 years old now.",
             W("w2", "63 − 60 = 3"), N("w2", "3", "son now", "below", 2)),
        beat("Is 3 our answer?",
             ask=ask(["yes, 3 is the answer", "not yet: add 6 years"], 1,
                     "Read the last line again. It asks for the son's age 6 years from now, not his age today."),
             ),
        beat("6 years from now he will be 3 plus 6, which is 9. So the son will be 9 years old.",
             U("q3", "6 years from now"), W("w3", "3 + 6 = 9"), A("ans", "The son will be 9 years old"), C("ans", "9")),
        beat("So bring every sum to the same time first. And when time moves, add the years once for each person."),
    )


L["EXT_G4_FP_2021_019"] = couple_and_son(
    "6 years ago, a husband's and wife's ages added up to 48. Today the husband, wife and son add up to 63. How old will the son be 6 years from now?",
    "")

L["EXT_G4_FP_2022_035"] = lesson(
    beat("3 years ago, the ages of Nirav and Vipul added up to 38. Vipul is 2 years younger than Nirav. We want Vipul's age after 2 years.",
         G("q1", "3 years ago: Nirav + Vipul = 38"), G("q2", "Vipul is 2 years younger than Nirav"),
         G("q3", "Vipul's age after 2 years = ?")),
    beat("First bring the sum to today. 3 years ago they added up to 38. What do their ages add up to now?",
         ask=ask(["38", "41", "44"], 2, "Nirav is 3 years older now, and Vipul is 3 years older too. So add 3 twice.")),
    beat("38 plus 3 plus 3 is 44. Two people, so the 3 is added twice.", W("w1", "38 + 3 + 3 = 44"), N("w1", "44", "sum now")),
    beat("Now we split the 44 between them. Look at the bars. Nirav's bar is the same as Vipul's bar, plus 2 extra years.",
         F(bars(bar("Vipul", [seg("?", 4, "a")]), bar("Nirav", [seg("?", 4, "a"), seg("2", 1, "c")])))),
    beat("Take away Nirav's 2 extra years. 44 minus 2 is 42. Now we have two equal bars.", W("w2", "44 − 2 = 42")),
    beat("Half of 42 is 21. So Vipul is 21 years old now.", W("w3", "42 ÷ 2 = 21"), N("w3", "21", "Vipul now")),
    beat("The question asks for Vipul's age after 2 years. So what do we do?",
         ask=ask(["21 − 2", "21 + 2", "nothing: 21 is the answer"], 1, "After means going forward in time. Vipul will be 2 years older than he is now.")),
    beat("21 plus 2 is 23. So after 2 years Vipul will be 23 years old.",
         W("w4", "21 + 2 = 23"), A("ans", "Vipul will be 23 years old"), C("ans", "23")),
    beat("Check today's ages. Vipul is 21, so Nirav is 2 more, which is 23. And 21 plus 23 is 44. It fits.", W("c1", "21 + 23 = 44")),
    beat("So: bring the sum to today, take away the extra years, halve, and then move to the time the question asks about."),
)

L["G4A_AGES_001"] = lesson(
    beat("Asha is 9 years old now. We want her age after 6 years.", G("q1", "Asha is 9 years old now"), G("q2", "After 6 years she will be ?")),
    beat("After 6 years. Are we moving forward in time, or back?",
         ask=ask(["back: she gets younger", "forward: she gets older"], 1,
                 "After means later on, in the future. As the years go by, Asha grows older.")),
    beat("Every birthday adds 1 to her age. 6 birthdays add 6. So we add: 9 plus 6. Count on 6 from 9: 10, 11, 12, 13, 14, 15.",
         W("w1", "9 + 6 = 15"), Lb("w2", "10, 11, 12, 13, 14, 15"), line(9, 15, [(9, "now")], [(9, 15, "+ 6")])),
    beat("So Asha will be 15 years old.", A("ans", "Asha will be 15 years old"), C("ans", "15")),
    beat("Two slips to watch for. 9 minus 6 would be her age 6 years ago. And 9 times 6 is far too big: each year adds only 1."),
    beat("Check: 15 minus 6 takes us back to 9, her age now.", W("c1", "15 − 6 = 9")),
    beat("The word after means forward in time, so add the years."),
)

L["G4A_AGES_002"] = lesson(
    beat("Meera is 10 years old and her father is 38. How many years older than Meera is her father?",
         G("q1", "Meera is 10. Her father is 38."), G("q2", "How many years older is her father?")),
    beat("How many years older. Those words ask for the gap between the two ages.", U("q2", "How many years older")),
    beat("How do we find the gap between two numbers?",
         ask=ask(["38 + 10", "38 − 10", "38 ÷ 10"], 1,
                 "Adding would put the two ages together. For how much older, take the smaller age away from the bigger one.")),
    beat("38 minus 10. Take one ten away from 38 and we have 28.", W("w1", "38 − 10 = 28")),
    beat("So her father is 28 years older than Meera.", A("ans", "Her father is 28 years older"), C("ans", "28")),
    beat("Check: start at Meera's age, 10, and add 28. We land on 38, her father's age.", W("c1", "10 + 28 = 38")),
    beat("Here is a nice fact. When Meera was born, her father was 28. And he will always be 28 years older than her."),
    beat("So the words how much older mean: subtract the smaller age from the bigger one."),
)

L["G4A_AGES_003"] = lesson(
    beat("Tina is 8 years old. Her mother is 4 times as old as Tina. How old is her mother?",
         G("q1", "Tina is 8 years old"), G("q2", "Her mother is 4 times as old. Mother = ?")),
    beat("4 times as old. Picture Tina's age as one block of 8. Her mother's age is 4 of those blocks.",
         F(bars(bar("Tina", segs(1, "a", "8")), bar("Mother", segs(4, "b", "8"))))),
    beat("So which sum gives the mother's age?",
         ask=ask(["8 + 4", "8 × 4", "8 ÷ 4"], 1,
                 "The words times as old tell us to multiply. 8 plus 4 would make her only 4 years older than Tina.")),
    beat("8 times 4. Count four 8s: 8, 16, 24, 32.", Lb("w1", "8, 16, 24, 32"), W("w2", "8 × 4 = 32")),
    beat("So her mother is 32 years old.", A("ans", "Her mother is 32 years old"), C("ans", "32")),
    beat("Does it make sense? A mother is much older than her 8 year old child, and 32 sounds right."),
    beat("Remember: times as old means multiply."),
)

L["G4A_AGES_004"] = lesson(
    beat("Four years ago, Zoya was 6 years old. How old is she now?", G("q1", "Four years ago, Zoya was 6"), G("q2", "How old is she now?")),
    beat("Four years ago is in the past. To come back to today, does her age go up or down?",
         ask=ask(["up", "down"], 0, "She was 6 back then. Since then she has had 4 more birthdays, so she is older today.")),
    beat("From then to now, 4 years have passed. So we add 4. 6 plus 4 is 10.",
         W("w1", "6 + 4 = 10"), line(6, 10, [(6, "4 years ago"), (10, "now")], [(6, 10, "+ 4")])),
    beat("So Zoya is 10 years old now.", A("ans", "Zoya is 10 years old now"), C("ans", "10")),
    beat("The trap is to see the word ago and subtract. But the 6 is already her age in the past. Coming forward to today, we add."),
    beat("Check: go back 4 years from 10 and we get 6, just as the question says.", W("c1", "10 − 4 = 6")),
    beat("So first ask where you are on the timeline. From the past up to now, add."),
)

L["G4A_AGES_005"] = lesson(
    beat("Dev was born in the year 2015. How old was he on his birthday in 2024?",
         G("q1", "Dev was born in 2015"), G("q2", "His age on his birthday in 2024 = ?")),
    beat("On each birthday Dev's age goes up by 1. So his age is the number of years from 2015 to 2024."),
    beat("How do we find the number of years from 2015 to 2024?",
         ask=ask(["2024 + 2015", "2024 − 2015", "count both years: 10"], 1,
                 "The years between two dates come from subtracting the earlier year from the later one.")),
    beat("2024 minus 2015 is 9. You can count the hops on the line too: 9 hops take you from 2015 to 2024.",
         W("w1", "2024 − 2015 = 9"), line(2015, 2024, [(2015, "born"), (2024, "birthday")])),
    beat("So Dev was 9 years old.", A("ans", "Dev was 9 years old"), C("ans", "9")),
    beat("The trap is counting 2015 itself as year 1. But in 2015 Dev was a newborn baby, 0 years old. His first birthday came in 2016.",
         Lb("n1", "2015: born (age 0)     2016: age 1")),
    beat("So age on a birthday is that year minus the birth year."),
)

L["G4A_AGES_006"] = lesson(
    beat("Rohan's father is 36 years old. Rohan is one-third as old as his father. How old is Rohan?",
         G("q1", "Rohan's father is 36 years old"), G("q2", "Rohan is one-third as old. Rohan = ?")),
    beat("One-third means: cut the father's age into 3 equal parts, and take 1 of them.",
         F(bars(bar("Father", segs(3, "a", "?"), brace="36")))),
    beat("So what do we do with 36?",
         ask=ask(["36 × 3", "36 − 3", "36 ÷ 3"], 2,
                 "Cutting into 3 equal parts is dividing by 3. Rohan is younger than his father, so the answer must be smaller than 36.")),
    beat("36 divided by 3 is 12, because 3 times 12 is 36.", W("w1", "3 × 12 = 36"), W("w2", "36 ÷ 3 = 12")),
    beat("So Rohan is 12 years old.", A("ans", "Rohan is 12 years old"), C("ans", "12")),
    beat("Careful: one-third is not the same as half. Half of 36 would be 18. A third means 3 equal parts, so each part is smaller.",
         Lb("n1", "Half of 36 is 18: not what we want")),
    beat("So one-third as old means divide by 3."),
)

L["G4A_AGES_007"] = lesson(
    beat("Anil is 3 years older than his brother Sunil today. How many years older will Anil be after 10 years?",
         G("q1", "Anil is 3 years older than Sunil today"), G("q2", "After 10 years, how many years older is Anil?")),
    beat("No ages are given, so let us try some. Say Sunil is 5 today. Then Anil is 5 plus 3, which is 8.",
         Lb("t1", "Try: Sunil is 5 today"), W("w1", "5 + 3 = 8"), N("w1", "8", "Anil")),
    beat("Now jump 10 years ahead. Sunil will be 15 and Anil will be 18.", W("w2", "5 + 10 = 15"), W("w3", "8 + 10 = 18")),
    beat("So after 10 years, how many years older is Anil?",
         ask=ask(["3", "7", "13"], 0, "Take Sunil's new age away from Anil's new age: 18 minus 15.")),
    beat("18 minus 15 is 3. Still 3 years older!", W("w4", "18 − 15 = 3")),
    beat("That is no accident. Both brothers grow older by the same 10 years. So the gap between them stays exactly the same."),
    beat("So Anil will still be 3 years older.", A("ans", "Anil will still be 3 years older"), C("ans", "3")),
    beat("The gap between two people's ages never changes. Not after 10 years, not ever."),
)

L["G4A_AGES_008"] = lesson(
    beat("Ravi is 12 years old now. In how many years will he be 20?",
         G("q1", "Ravi is 12 years old now"), G("q2", "In how many years will he be 20?")),
    beat("We know his age now, 12, and his age later, 20. We want the number of years in between."),
    beat("How do we find the years in between?",
         ask=ask(["20 + 12", "20 − 12", "20 × 12"], 1,
                 "Adding 20 and 12 would join the two ages together. For the years in between, take the age now away from the age later.")),
    beat("20 minus 12 is 8. You can also count on from 12 until you reach 20. That takes 8 hops.",
         W("w1", "20 − 12 = 8"), line(12, 20, [(12, "now"), (20, "later")])),
    beat("So Ravi will be 20 in 8 years.", A("ans", "Ravi will be 20 in 8 years"), C("ans", "8 years")),
    beat("Check: 12 plus 8 is 20. Yes.", W("c1", "12 + 8 = 20")),
    beat("So the age later, minus the age now, gives the years in between."),
)

L["G4A_AGES_009"] = lesson(
    beat("Amit is 3 years older than Bina. Bina is 2 years older than Chirag. Chirag is 7. How old is Amit?",
         G("q1", "Amit is 3 years older than Bina"), G("q2", "Bina is 2 years older than Chirag"), G("q3", "Chirag is 7. Amit = ?")),
    beat("This is a chain of three children. Which child's age do we know for sure?",
         ask=ask(["Amit", "Bina", "Chirag"], 2, "Only one age is given as a number: Chirag is 7. So the chain starts with Chirag.")),
    beat("Start with Chirag, who is 7. Bina is 2 years older than Chirag. So Bina is 7 plus 2, which is 9.",
         W("w1", "7 + 2 = 9"), N("w1", "9", "Bina")),
    beat("Next link. Amit is 3 years older than Bina. Careful: older than Bina, not older than Chirag.", U("q1", "than Bina")),
    beat("9 plus 3 is 12.", W("w2", "9 + 3 = 12"), N("w2", "12", "Amit")),
    beat("So Amit is 12 years old.", A("ans", "Amit is 12 years old"), C("ans", "12")),
    beat("Check the order: Chirag 7, Bina 9, Amit 12. Each one is older than the one before, just as the question says."),
    beat("So start from the age you know and walk along the chain, one person at a time."),
)
