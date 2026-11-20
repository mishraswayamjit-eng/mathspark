"""gr4_sequences lessons written one by one: the four "find the sum" questions, the
previous-year questions (PYQ_...), and Q_CH15_018, Q_CH16_001 to Q_CH16_011.
"""
from g4_gr4_sequences_a import tenth_of_24
from g4_gr4_sequences_b import add_two_before, count_terms, cubes, missing_351, next_two_53, repeated_digits
from g4_gr4_sequences_lib import ans, b, ch, fig, g, grp, jumps, lab, mk, nt, qfig, tbl, w

L = {}
TOPIC = "gr4_sequences"


# ── PH3_EXT_G4_FP_2022_030_02_b: 1 + 3 + 5 + ... + 19 ────────────────────────
L["PH3_EXT_G4_FP_2022_030_02_b"] = [
    b("We have to add 1, 3, 5, and so on, up to 19. That is a lot of adding, so let's be clever about it.",
      g("l1", "1 + 3 + 5 + ... + 19 = ?", True)),
    b("Write out the whole list: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19. Count them. There are 10 numbers.",
      lab("l2", "1, 3, 5, 7, 9, 11, 13, 15, 17, 19"), lab("l3", "10 numbers")),
    b("Here is the trick. Pair the first with the last: 1 and 19. Then the next two: 3 and 17. What do you notice?",
      ask=ch("both pairs make 20", ["the pairs get bigger", "the pairs get smaller"],
             "1 plus 19 is 20. 3 plus 17 is 20 as well. One number goes up by 2 and the other comes down by 2, so the total stays the same.")),
    b("1 and 19 make 20. 3 and 17 make 20. So do 5 and 15, 7 and 13, and 9 and 11. Every pair makes 20.",
      grp("l2", ["1", "19"], "20"), grp("l2", ["3", "17"], "20"), w("l4", "1 + 19 = 20"), w("l5", "3 + 17 = 20")),
    b("We have 10 numbers. How many pairs do they make?",
      ask=ch("5", ["10", "20"], "Each pair uses up 2 numbers. So 10 numbers make 5 pairs.")),
    b("This is the step to be careful with. 10 numbers make 5 pairs, not 10 pairs.", w("l6", "10 ÷ 2 = 5")),
    b("5 pairs of 20 make 100. So the sum is 100.", ans("l7", "5 × 20 = 100", "100")),
    b("Here is a lovely check. Add up the first 10 odd numbers and you always get 10 times 10. That is 100 too.",
      w("l8", "10 × 10 = 100")),
    b("To add a long, evenly spaced list: pair the ends, see what each pair makes, and count the pairs."),
]


# ── PH3_EXT_G4_FP_2024_033_02_b: first 6 natural numbers ─────────────────────
L["PH3_EXT_G4_FP_2024_033_02_b"] = [
    b("Natural numbers are the counting numbers: 1, 2, 3, and so on. We want the first 6 of them added together.",
      g("l1", "Sum of the first 6 natural numbers = ?", True)),
    b("So our sum is 1 plus 2 plus 3 plus 4 plus 5 plus 6.", w("l2", "1 + 2 + 3 + 4 + 5 + 6 = ?")),
    b("We could add from left to right. But try pairing from the two ends. What do 1 and 6 make? And 2 and 5?",
      ask=ch("7 each time", ["6 each time", "7, and then 8"], "1 plus 6 is 7. 2 plus 5 is 7 too.")),
    b("1 and 6 make 7. 2 and 5 make 7. 3 and 4 make 7. Three pairs, and each one is worth 7.",
      grp("l2", ["1", "6"], "7"), w("l3", "1 + 6 = 7"), w("l4", "2 + 5 = 7"), w("l5", "3 + 4 = 7")),
    b("Notice it is 3 pairs, not 6. The 6 numbers are used up 2 at a time."),
    b("3 pairs of 7 make 21. So the sum is 21.", ans("l6", "3 × 7 = 21", "21")),
    b("Let's check the slow way, adding one at a time. The running total goes 1, 3, 6, 10, 15, 21. The same answer!",
      lab("l7", "running total: 1, 3, 6, 10, 15, 21")),
    b("Pairing the ends turns a long sum into one small multiplication. Try it whenever numbers go up in equal steps."),
]


# ── PH3_EXT_G4_FP_2025_021_03: 10 + 15 + 20 + ... + 105 ──────────────────────
L["PH3_EXT_G4_FP_2025_021_03"] = [
    b("We must add 10, 15, 20, and so on, all the way to 105. First question: how many numbers are we adding?",
      g("l1", "10 + 15 + 20 + ... + 105 = ?", True)),
    b("They are all multiples of 5. 10 is 2 fives, so it is the 2nd multiple. 105 is 21 fives, so it is the 21st multiple.",
      w("l2", "10 = 2 × 5"), w("l3", "105 = 21 × 5")),
    b("So the list runs from the 2nd multiple of 5 to the 21st. How many numbers is that?",
      ask=ch("20", ["21", "19"],
             "From the 1st to the 21st would be 21 numbers. We start at the 2nd, so 1 is left out. That gives 20.")),
    b("There are 21 multiples up to 105, but the 1st one, 5 itself, is not in our list. So we have 20 numbers.",
      w("l4", "21 − 1 = 20")),
    b("Now pair the ends. 10 and 105 make 115. 15 and 100 make 115 as well. Every pair makes 115.",
      w("l5", "10 + 105 = 115"), w("l6", "15 + 100 = 115")),
    b("We have 20 numbers. How many pairs do they make?",
      ask=ch("10", ["20", "5"], "A pair uses up 2 numbers. So 20 numbers make 10 pairs.")),
    b("Careful here: 20 numbers make 10 pairs, not 20 pairs. Counting each pair twice is the classic slip.",
      w("l7", "20 ÷ 2 = 10")),
    b("10 pairs of 115 make 1150. So the sum is 1150.", ans("l8", "10 × 115 = 1150", "1150")),
    b("For a long, evenly spaced sum: count the numbers, pair the ends, and multiply the pair total by the number of pairs."),
]


# ── PH3_EXT_G4_WS2_CH16_016_01_b: first 19 even numbers ──────────────────────
L["PH3_EXT_G4_WS2_CH16_016_01_b"] = [
    b("The even numbers start 2, 4, 6. We want the first 19 of them, all added up.",
      g("l1", "Sum of the first 19 even numbers = ?", True)),
    b("First we need to know where the list ends. What is the 19th even number?",
      ask=ch("38", ["19", "36"],
             "The 1st even number is 2, the 2nd is 4, the 3rd is 6. Each one is double its place. So the 19th is double 19.")),
    b("Each even number is double its place number. So the 19th one is 19 times 2, which is 38.",
      w("l2", "19 × 2 = 38"), lab("l3", "2 + 4 + 6 + ... + 38")),
    b("Now pair the ends. 2 and 38 make 40. 4 and 36 make 40. Every pair makes 40.",
      w("l4", "2 + 38 = 40"), w("l5", "4 + 36 = 40")),
    b("Here is the tricky part. 19 is an odd number. What happens when we pair up 19 numbers?",
      ask=ch("9 pairs and 1 left over", ["10 pairs", "19 pairs"],
             "Pairs use the numbers 2 at a time. 9 pairs use all but one of the 19, so 1 number is left in the middle.")),
    b("9 pairs use 18 numbers, and 1 is left alone in the middle. The middle one is the 10th even number, which is 20.",
      w("l6", "9 × 2 = 18"), w("l7", "19 − 18 = 1"), lab("l8", "middle number: 20")),
    b("9 pairs of 40 make 360.", w("l9", "9 × 40 = 360")),
    b("Don't forget the one in the middle. 360 plus 20 is 380. So the sum is 380.", ans("l10", "360 + 20 = 380", "380")),
    b("A quick check. Each pair of 40 is like two 20s. So the whole sum is like 19 twenties, and 19 times 20 is 380.",
      w("l11", "19 × 20 = 380")),
    b("When you pair up an odd count of numbers, one is left in the middle. Add it on at the end."),
]


# ── PYQ_2016_Q01 ─────────────────────────────────────────────────────────────
L["PYQ_2016_Q01"] = [
    b("The series is 48, 51, 57, 69, and then a star. We must find the number hiding behind the star.",
      g("l1", "48, 51, 57, 69, ★", True), fig("f1", qfig(TOPIC, "PYQ_2016_Q01"))),
    b("Find the jumps. 51 minus 48 is 3. 57 minus 51 is 6. 69 minus 57 is 12.",
      w("l2", "51 − 48 = 3"), w("l3", "57 − 51 = 6"), w("l4", "69 − 57 = 12"), jumps("l1", ["+3", "+6", "+12"])),
    b("The jumps are 3, 6 and 12. How do they grow?",
      ask=ch("each is double the one before", ["each is 3 more", "each is 6 more"],
             "3 to 6 could be adding 3. But 6 to 12 is not adding 3. Doubling fits both: double 3 is 6, and double 6 is 12.")),
    b("The jumps double each time. So the next jump is double 12, which is 24. The trap is to use an old jump again.",
      w("l5", "12 × 2 = 24"), nt("l1", ",", "+24", "below", 4)),
    b("69 plus 24 is 93. So the star stands for 93.", ans("l6", "69 + 24 = 93", "93")),
    b("Read the jumps once more: 3, 6, 12, 24. Each one is double the last. It fits."),
    b("When the jumps are not steady, check whether they grow by adding or by multiplying. Here they doubled."),
]


# ── PYQ_2017_Q05 ─────────────────────────────────────────────────────────────
L["PYQ_2017_Q05"] = [
    b("A man walks 66 kilometres in 6 days. Each day he walks 4 kilometres less than the day before. How far does he walk on the 6th day?",
      g("l1", "66 km in 6 days. Each day 4 km less.", True), g("l1b", "Day 6 = ?", True)),
    b("We don't know how far he walked on any single day. So here is the plan: compare every day with day 6, the shortest walk of all."),
    b("Day 5 is 4 kilometres more than day 6. So how much more than day 6 is day 4?",
      ask=ch("8", ["4", "6"],
             "Day 4 is 4 more than day 5, and day 5 is 4 more than day 6. That is 4 and 4, which makes 8.")),
    b("So day 5 is 4 more than day 6. Day 4 is 8 more. Then 12 more, 16 more, and day 1 is 20 more.",
      tbl("f1", [["Day 6", "shortest walk"], ["Day 5", "+ 4"], ["Day 4", "+ 8"], ["Day 3", "+ 12"], ["Day 2", "+ 16"], ["Day 1", "+ 20"]],
          "Every day compared with day 6")),
    b("Add up all the extra: 4 plus 8 plus 12 plus 16 plus 20. That is 60 kilometres of extra walking.",
      w("l2", "4 + 8 + 12 + 16 + 20 = 60")),
    b("Now take that extra 60 away from the total. What does the leftover stand for?",
      ask=ch("6 walks as long as day 6", ["the walk on day 6", "the walk on day 1"],
             "Without the extras, every one of the 6 days is as short as day 6. So what is left is 6 equal walks.")),
    b("66 take away 60 leaves 6 kilometres. That is 6 equal walks, so each one is 1 kilometre.",
      w("l3", "66 − 60 = 6"), w("l4", "6 ÷ 6 = 1")),
    b("So on the 6th day he walked just 1 kilometre.", ans("l5", "Day 6 = 1 km", None, True)),
    b("Check. The six days were 21, 17, 13, 9, 5 and 1 kilometres. Add them up and you get 66. It works.",
      w("l6", "21 + 17 + 13 + 9 + 5 + 1 = 66")),
    b("The trap is to share 66 equally among 6 days. The days are not equal! Compare every day with the one you want, then take away the extras."),
]


L["PYQ_2017_Q12"] = count_terms("PYQ_2017_Q12", [1, 8, 15, 22, 29], 113, (70, 42), 1)
L["PYQ_2017_Q37"] = tenth_of_24(1)


# ── PYQ_2018_Q38 ─────────────────────────────────────────────────────────────
L["PYQ_2018_Q38"] = [
    b("The series is 519, 398, 277, 156, and then a star. The numbers are shrinking. Let's find the next one.",
      g("l1", "519, 398, 277, 156, ★", True), fig("f1", qfig(TOPIC, "PYQ_2018_Q38"))),
    b("Find the first drop. 519 minus 398 is 121.", w("l2", "519 − 398 = 121"), nt("l1", ",", "−121")),
    b("Before we trust that, what should we do?",
      ask=ch("check the other drops", ["take 121 from 519 again", "halve 156"],
             "One drop does not make a rule. Test the other neighbours to see if the drop is always 121.")),
    b("398 minus 277 is 121. 277 minus 156 is 121. The drop is 121 every time.",
      w("l3", "398 − 277 = 121"), w("l4", "277 − 156 = 121"), nt("l1", ",", "−121", "below", 2), nt("l1", ",", "−121", "below", 3)),
    b("So take 121 away from 156. Take away 100 first to get 56. Then take away 21 to get 35.",
      w("l5", "156 − 100 = 56"), w("l6", "56 − 21 = 35")),
    b("So the star stands for 35.", ans("l7", "156 − 121 = 35", "35")),
    b("Check by adding back. 35 plus 121 is 156. It fits.", w("l8", "35 + 121 = 156")),
    b("Find the jump, check it on every pair, then make one more jump. And with big numbers, subtract in easy pieces."),
]


# ── PYQ_2019_Q28 ─────────────────────────────────────────────────────────────
L["PYQ_2019_Q28"] = [
    b("The series is 5, 14, 25, 38, then a star, then 70 and 89. This time the hidden number is in the middle.",
      g("l1", "5, 14, 25, 38, ★, 70, 89", True)),
    b("Find the jumps we can see. 5 to 14 is 9. 14 to 25 is 11. 25 to 38 is 13.",
      jumps("l1", ["+9", "+11", "+13"])),
    b("The jumps are 9, 11, 13. What is the next jump?",
      ask=ch("15", ["13", "10"], "Each jump is 2 more than the one before. After 13 comes 15.")),
    b("The jumps grow by 2, so the next one is 15. And 38 plus 15 is 53.",
      nt("l1", ",", "+15", "below", 4), w("l2", "38 + 15 = 53")),
    b("Here is the good part. The numbers after the star let us check. The next jumps should be 17 and 19.",
      lab("l3", "jumps: 9, 11, 13, 15, 17, 19")),
    b("53 plus 17 is 70. And 70 plus 19 is 89. Both match the series!",
      w("l4", "53 + 17 = 70"), w("l5", "70 + 19 = 89")),
    b("So the star stands for 53.", ans("l6", "★ = 53", "53", True)),
    b("A number in the middle has to fit on both sides. Always test your answer against the numbers that come after it."),
]


# ── Q_CH15_018 ───────────────────────────────────────────────────────────────
L["Q_CH15_018"] = [
    b("The numbers are 2, 6, 12, 20, 30. Which number comes next?",
      g("l1", "2, 6, 12, 20, 30, ?", True), fig("f1", qfig(TOPIC, "Q_CH15_018"))),
    b("Measure the jumps. 2 to 6 is 4. 6 to 12 is 6. 12 to 20 is 8. 20 to 30 is 10.",
      jumps("l1", ["+4", "+6", "+8", "+10"])),
    b("The jumps are 4, 6, 8, 10. What will the next jump be?",
      ask=ch("12", ["10", "14"], "The jumps go up by 2 each time: 4, 6, 8, 10. So the next jump is 12.")),
    b("The jumps grow by 2 each time. So the next jump is 12, not 10 again.", nt("l1", ",", "+12", "below", 5)),
    b("30 plus 12 is 42. So the next number is 42.", ans("l2", "30 + 12 = 42", "42")),
    b("Here is another way to see these numbers. 2 is 1 times 2. 6 is 2 times 3. 12 is 3 times 4. So the 6th number is 6 times 7, which is 42 again.",
      w("l3", "1 × 2 = 2"), w("l4", "2 × 3 = 6"), w("l5", "3 × 4 = 12"), w("l6", "6 × 7 = 42")),
    b("When the jumps change, look for the pattern in the jumps. And if you can find a second way, use it to check."),
]


L["Q_CH16_001"] = repeated_digits(1)


# ── Q_CH16_002: 416, 525, 636, 749 (by jumps, then the digits as a check) ────
L["Q_CH16_002"] = [
    b("The sequence is 416, 525, 636, 749. What comes next? Let's measure the jumps.",
      g("l1", "416, 525, 636, 749, ?", True)),
    b("525 minus 416 is 109. 636 minus 525 is 111. 749 minus 636 is 113.",
      w("l2", "525 − 416 = 109"), w("l3", "636 − 525 = 111"), w("l4", "749 − 636 = 113"),
      jumps("l1", ["+109", "+111", "+113"])),
    b("Here is the thing to spot. Are the jumps all the same?",
      ask=ch("no, they grow by 2", ["yes, always 109", "no, they grow by 10"],
             "Look closely: 109, 111, 113. Each jump is 2 more than the one before.")),
    b("The jumps look alike, but they are not the same. They grow by 2. So the next jump is 115.",
      nt("l1", ",", "+115", "below", 4)),
    b("749 plus 115. Add 100 to get 849. Then add 15 to get 864.",
      w("l5", "749 + 100 = 849"), w("l6", "849 + 15 = 864")),
    b("So the next term is 864.", ans("l7", "749 + 115 = 864", "864")),
    b("There is a second way to see it. The first digits go 4, 5, 6, 7. And the last two digits are 4 times 4, 5 times 5, 6 times 6, 7 times 7.",
      w("l8", "4 × 4 = 16"), w("l9", "5 × 5 = 25"), w("l10", "6 × 6 = 36"), w("l11", "7 × 7 = 49")),
    b("So next comes 8, followed by 8 times 8, which is 64. That makes 864 again. Two ways, one answer.",
      w("l12", "8 × 8 = 64")),
    b("Jumps that look nearly the same may still be changing. Work each one out exactly before you decide on the rule."),
]


# ── Q_CH16_003 ───────────────────────────────────────────────────────────────
L["Q_CH16_003"] = [
    b("The list is 2, 6, 12, 20, a question mark, 42, 56. The missing number sits in the middle.",
      g("l1", "2, 6, 12, 20, ?, 42, 56", True)),
    b("Start with the jumps we can see. 2 to 6 is 4. 6 to 12 is 6. 12 to 20 is 8.",
      jumps("l1", ["+4", "+6", "+8"])),
    b("The jumps are 4, 6, 8. So what is the jump into the missing number?",
      ask=ch("10", ["8", "12"], "Each jump is 2 bigger than the last. After 8 comes 10.")),
    b("The jumps grow by 2, so the next jump is 10. And 20 plus 10 is 30.",
      nt("l1", ",", "+10", "below", 4), w("l2", "20 + 10 = 30")),
    b("Now test it with the numbers after the gap. The next jumps should be 12 and 14.",
      lab("l3", "jumps: 4, 6, 8, 10, 12, 14")),
    b("30 plus 12 is 42. And 42 plus 14 is 56. Both fit the list perfectly.",
      w("l4", "30 + 12 = 42"), w("l5", "42 + 14 = 56")),
    b("So the missing number is 30.", ans("l6", "? = 30", "30", True)),
    b("When the gap is in the middle, the numbers after it are a free check. Use them!"),
]


L["Q_CH16_004"] = cubes(1)
L["Q_CH16_005"] = next_two_53(1)
L["Q_CH16_006"] = missing_351("Q_CH16_006", 1)


# ── Q_CH16_007 ───────────────────────────────────────────────────────────────
L["Q_CH16_007"] = [
    b("The series is 37, 39, 42, 47, 54, then a hidden number, then 78.",
      g("l1", "37, 39, 42, 47, 54, *, 78", True)),
    b("Find the jumps. 37 to 39 is 2. Then 3, then 5, then 7.", jumps("l1", ["+2", "+3", "+5", "+7"])),
    b("The jumps are 2, 3, 5, 7. Think about which family these numbers belong to. What comes next?",
      ask=ch("11, the next prime number", ["9, the next odd number", "8, one more than 7"],
             "If these were the odd numbers, 2 would not be there. 2, 3, 5 and 7 are prime numbers. 9 is 3 times 3, so it is not prime. The next prime is 11.")),
    b("This is the trap. 2, 3, 5, 7 look as if 9 should follow. But they are the primes, and 9 is 3 times 3. So the next jump is 11.",
      w("l2", "9 = 3 × 3"), lab("l3", "primes: 2, 3, 5, 7, 11, 13")),
    b("54 plus 11 is 65.", w("l4", "54 + 11 = 65")),
    b("Now test it with the last number. The prime after 11 is 13, and 65 plus 13 is 78. That is exactly the last number in the series.",
      w("l5", "65 + 13 = 78")),
    b("So the hidden number is 65.", ans("l6", "* = 65", "65", True)),
    b("And if we had used 9? 54 plus 9 is 63. Then we would need a jump of 15 to reach 78, and that fits no pattern.",
      w("l7", "54 + 9 = 63"), w("l8", "78 − 63 = 15")),
    b("When jumps look almost like a pattern you know, check carefully which family they really belong to. Then test with the numbers that follow."),
]


# ── Q_CH16_008 ───────────────────────────────────────────────────────────────
L["Q_CH16_008"] = [
    b("The sequence starts 53, 60, 68, 77. We want the 10th term, so first we need the rule.",
      g("l1", "53, 60, 68, 77, ...", True), g("l1b", "10th term = ?", True)),
    b("Look at the jumps. 53 to 60 is 7. 60 to 68 is 8. 68 to 77 is 9.", jumps("l1", ["+7", "+8", "+9"])),
    b("How do the jumps change?",
      ask=ch("each jump is 1 bigger", ["they stay the same", "each jump is 1 smaller"],
             "Read them again: 7, 8, 9. Each jump is 1 more than the one before.")),
    b("77 is the 4th term. To reach the 10th we need 6 more jumps: 10, 11, 12, 13, 14 and 15. Counting them is the tricky part.",
      nt("l1", "77", "4th", "above"), w("l2", "10 − 4 = 6"), lab("l3", "next jumps: 10, 11, 12, 13, 14, 15")),
    b("The 5th term is 77 plus 10, which is 87. The 6th is 87 plus 11, which is 98.",
      w("l4", "77 + 10 = 87"), nt("l4", "87", "5th"), w("l5", "87 + 11 = 98"), nt("l5", "98", "6th")),
    b("The 7th is 98 plus 12, which is 110. The 8th is 110 plus 13, which is 123. Don't stop there, it is only the 8th!",
      w("l6", "98 + 12 = 110"), nt("l6", "110", "7th"), w("l7", "110 + 13 = 123"), nt("l7", "123", "8th")),
    b("The 9th term is 123 plus 14, which is 137.", w("l8", "123 + 14 = 137"), nt("l8", "137", "9th")),
    b("One jump is left. Which one?",
      ask=ch("15", ["14", "16"], "We listed six jumps: 10, 11, 12, 13, 14, 15. Five are used, so the last is 15.")),
    b("137 plus 15 is 152. So the 10th term is 152.", ans("l9", "137 + 15 = 152", "152")),
    b("When jumps keep changing, walk forward one term at a time and label each term. That way you stop at exactly the right one."),
]


L["Q_CH16_009"] = add_two_before(1)


# ── Q_CH16_010 ───────────────────────────────────────────────────────────────
L["Q_CH16_010"] = [
    b("Our terms are fractions: 1 fifth, 2 fifths, 4 fifths, 7 fifths, 11 fifths. We want the next one.",
      g("l1", "1/5, 2/5, 4/5, 7/5, 11/5, ___", True)),
    b("Every fraction has the same bottom number, 5. So where is the pattern hiding?",
      ask=ch("in the top numbers", ["in the bottom numbers", "there is no pattern"],
             "The bottom number never changes. Only the top numbers move: 1, 2, 4, 7, 11.")),
    b("Look only at the tops: 1, 2, 4, 7, 11. The jumps between them are 1, 2, 3 and 4.",
      lab("l2", "top numbers: 1, 2, 4, 7, 11"), jumps("l2", ["+1", "+2", "+3", "+4"])),
    b("So what is the next jump?",
      ask=ch("5", ["4", "6"], "The jumps go 1, 2, 3, 4. Each is 1 more than the last, so the next is 5.")),
    b("11 plus 5 is 16. So the next term is 16 fifths.", w("l3", "11 + 5 = 16"), w("l4", "16/5")),
    b("The choices are mixed numbers, so let's change it. 5 fifths make 1 whole. So 15 fifths make 3 wholes, and 1 fifth is left over.",
      w("l5", "15/5 = 3"), w("l6", "16/5 = 3 + 1/5")),
    b("So the next term is 3 and 1 fifth.", ans("l7", "16/5 = 3 1/5", "3 1/5", True)),
    b("Careful: 11 fifths is the same as 2 and 1 fifth. That is the last term we were given, not the next one."),
    b("With fractions that share a bottom number, find the pattern in the tops. Then write the answer in the form the question wants."),
]


# ── Q_CH16_011 ───────────────────────────────────────────────────────────────
L["Q_CH16_011"] = [
    b("The series is 0.25, 0.50, 1, 1.75, a hidden number, and then 4. Decimals this time, but the idea is the same.",
      g("l1", "0.25, 0.50, 1, 1.75, *, 4", True)),
    b("Find the jumps. 0.50 minus 0.25 is 0.25. 1 minus 0.50 is 0.50. 1.75 minus 1 is 0.75.",
      w("l2", "0.50 − 0.25 = 0.25"), w("l3", "1 − 0.50 = 0.50"), w("l4", "1.75 − 1 = 0.75")),
    b("The jumps are 0.25, 0.50, 0.75. What is the next jump?",
      ask=ch("1", ["0.75", "0.100"],
             "Each jump is 0.25 more than the last. And 0.75 plus 0.25 makes exactly 1 whole.")),
    b("The jumps grow by 0.25 each time. 0.75 plus 0.25 is 1 whole. So the next jump is 1.",
      w("l5", "0.75 + 0.25 = 1")),
    b("1.75 plus 1 is 2.75.", w("l6", "1.75 + 1 = 2.75")),
    b("Test it with the last number. The jump after 1 is 1.25. And 2.75 plus 1.25 is 4. It matches!",
      w("l7", "1 + 0.25 = 1.25"), w("l8", "2.75 + 1.25 = 4")),
    b("So the hidden number is 2.75.", ans("l9", "* = 2.75", "2.75", True)),
    b("Decimals follow the same plan as whole numbers. Find the jumps, see how they change, and check with the numbers that follow."),
]
