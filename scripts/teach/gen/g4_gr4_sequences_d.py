"""gr4_sequences lessons written one by one: Q_CH16_013 to Q_CH16_025."""
from g4_gr4_sequences_lib import ans, b, ch, fig, g, jumps, lab, mk, nt, qfig, w
from g4_gr4_sequences_rules import _labelled_line

L = {}
TOPIC = "gr4_sequences"


# ── Q_CH16_013 ───────────────────────────────────────────────────────────────
L["Q_CH16_013"] = [
    b("Our terms are 3, 7, 11, 15, 19. Let's find the one that comes next.",
      g("l1", "3, 7, 11, 15, 19, ___", True)),
    b("Start with the first two. How big is the jump from 3 to 7?",
      ask=ch("4", ["3", "5"], "Count on from 3: 4, 5, 6, 7. That is 4 steps. Or 7 take away 3 is 4.")),
    b("7 minus 3 is 4. Now check the others. 11 minus 7 is 4, and 15 minus 11 is 4. Every jump is 4.",
      w("l2", "7 − 3 = 4"), w("l3", "11 − 7 = 4"), w("l4", "15 − 11 = 4"), _labelled_line("Q_CH16_013", 4)),
    b("So the rule is: add 4 each time.", jumps("l1", ["+4", "+4", "+4", "+4"])),
    b("The last term is 19. 19 plus 4 is 23. So the next term is 23.", ans("l5", "19 + 4 = 23", "23")),
    b("Quick check. From 19 to 23 is a jump of 4, the same as all the others. It fits.", nt("l1", ",", "+4", "below", 5)),
    b("Find the jump, check that it never changes, then add it once more. That is the whole plan."),
]


# ── Q_CH16_014 ───────────────────────────────────────────────────────────────
L["Q_CH16_014"] = [
    b("The numbers are 3, 6, 12, 24, 48. What comes next?", g("l1", "3, 6, 12, 24, 48, ___", True)),
    b("Try the jumps: 3, then 6, then 12, then 24. They are not steady. But look, the jumps are growing just like the numbers themselves.",
      jumps("l1", ["+3", "+6", "+12", "+24"])),
    b("So adding is not the rule. Which move works at every step?",
      ask=ch("double the number", ["add 3", "add 6"],
             "Adding 3 works only once. Doubling works every time: double 3 is 6, and double 6 is 12.")),
    b("3 times 2 is 6. 6 times 2 is 12. 12 times 2 is 24. 24 times 2 is 48. Each number is double the one before.",
      w("l2", "3 × 2 = 6"), w("l3", "6 × 2 = 12"), w("l4", "12 × 2 = 24"), w("l5", "24 × 2 = 48")),
    b("So we double 48. Double 40 is 80, and double 8 is 16. Together that makes 96.",
      w("l6", "40 × 2 = 80"), w("l7", "8 × 2 = 16"), ans("l8", "48 × 2 = 96", "96")),
    b("The trap is to add the last jump, 24, once more. But the jumps double too. The next jump is 48, and 48 plus 48 is 96.",
      w("l9", "48 + 48 = 96")),
    b("When the jumps keep growing fast, test for multiplying. Here each number is double the one before."),
]


# ── Q_CH16_015 ───────────────────────────────────────────────────────────────
L["Q_CH16_015"] = [
    b("The numbers are 1, 4, 9, 16, 25. Let's work out what comes next.", g("l1", "1, 4, 9, 16, 25, ___", True)),
    b("Let's look at how each number is made. 4 is 2 times 2. 9 is 3 times 3.",
      w("l2", "2 × 2 = 4"), w("l3", "3 × 3 = 9")),
    b("So how is 16 made?",
      ask=ch("4 × 4", ["4 × 3", "4 + 4"], "4 times 4 is 16. Each number in the list is a counting number multiplied by itself.")),
    b("And 1 is 1 times 1, 16 is 4 times 4, and 25 is 5 times 5. These are called the square numbers.",
      w("l4", "1 × 1 = 1"), w("l5", "4 × 4 = 16"), w("l6", "5 × 5 = 25")),
    b("We have used 1, 2, 3, 4 and 5. Next comes 6, multiplied by itself. Careful: not 5 times 6. 6 times 6 is 36.",
      ans("l7", "6 × 6 = 36", "36")),
    b("Check with the jumps: 3, 5, 7, 9. They grow by 2, so the next jump is 11. And 25 plus 11 is 36. The same answer.",
      jumps("l1", ["+3", "+5", "+7", "+9", "+11"]), w("l8", "25 + 11 = 36")),
    b("So the next number is 36. When you see 1, 4, 9, 16, think square numbers: each counting number times itself."),
]


# ── Q_CH16_016 ───────────────────────────────────────────────────────────────
L["Q_CH16_016"] = [
    b("The numbers are 1, 3, 6, 10, 15, 21. What comes next?", g("l1", "1, 3, 6, 10, 15, 21, ___", True)),
    b("Measure the jumps. 1 to 3 is 2. 3 to 6 is 3. Then 4, then 5, then 6.",
      jumps("l1", ["+2", "+3", "+4", "+5", "+6"])),
    b("The jumps are 2, 3, 4, 5, 6. What will the next jump be?",
      ask=ch("7", ["6", "9"], "Each jump is 1 more than the one before. After 6 comes 7.")),
    b("The jump grows by 1 every time. So the next jump is 7, not 6 again.", nt("l1", ",", "+7", "below", 6)),
    b("21 plus 7 is 28. So the next number is 28.", ans("l2", "21 + 7 = 28", "28")),
    b("These numbers have a nice secret. 3 is 1 plus 2. 6 is 1 plus 2 plus 3. 10 is 1 plus 2 plus 3 plus 4. Each one adds the next counting number.",
      w("l3", "1 + 2 = 3"), w("l4", "1 + 2 + 3 = 6"), w("l5", "1 + 2 + 3 + 4 = 10")),
    b("When the jumps are not the same, look at the jumps themselves. Here they simply count up: 2, 3, 4, 5, 6, 7."),
]


# ── Q_CH16_017 ───────────────────────────────────────────────────────────────
L["Q_CH16_017"] = [
    b("The terms are 2, 5, 14, 41. Only four of them, and they grow fast. Let's find the next.",
      g("l1", "2, 5, 14, 41, ___", True)),
    b("Find the jumps. 5 minus 2 is 3. 14 minus 5 is 9. 41 minus 14 is 27.",
      w("l2", "5 − 2 = 3"), w("l3", "14 − 5 = 9"), w("l4", "41 − 14 = 27"), jumps("l1", ["+3", "+9", "+27"])),
    b("The jumps are 3, 9 and 27. How do they grow?",
      ask=ch("each is 3 times the last", ["each is 6 more", "each is double the last"],
             "3 to 9 could be adding 6. But 9 plus 6 is not 27. Times 3 fits both: 3 times 3 is 9, and 9 times 3 is 27.")),
    b("This is the thing to spot. The jumps don't grow by adding. Each jump is 3 times the one before. So the next jump is 27 times 3, which is 81.",
      w("l5", "27 × 3 = 81"), nt("l1", ",", "+81", "below", 4)),
    b("41 plus 81 is 122. So the next term is 122.", ans("l6", "41 + 81 = 122", "122")),
    b("Here is a second way to see it. Each term is 3 times the one before, take away 1. 2 times 3 is 6, and 6 take away 1 is 5.",
      w("l7", "2 × 3 − 1 = 5"), w("l8", "5 × 3 − 1 = 14")),
    b("Try it on the last term. 41 times 3 is 123, and 123 take away 1 is 122. Both ways agree.",
      w("l9", "41 × 3 = 123"), w("l10", "123 − 1 = 122")),
    b("When the jumps are not steady, ask if they are multiplied each time. And a second way to the same answer is the best check."),
]


# ── Q_CH16_018 ───────────────────────────────────────────────────────────────
L["Q_CH16_018"] = [
    b("The terms are 1, 2, 6, 24, 120. They grow faster and faster. What is next?",
      g("l1", "1, 2, 6, 24, 120, ___", True)),
    b("Adding can't keep up with growth like this, so think times. 1 times 2 is 2. 2 times 3 is 6.",
      w("l2", "1 × 2 = 2"), w("l3", "2 × 3 = 6")),
    b("Now from 6 to 24. 6 times what makes 24?",
      ask=ch("4", ["3", "18"], "6 times 4 is 24. We are multiplying here, not adding.")),
    b("6 times 4 is 24, and 24 times 5 is 120. Look at the multipliers: 2, 3, 4, 5.",
      w("l4", "6 × 4 = 24"), w("l5", "24 × 5 = 120"), jumps("l1", ["×2", "×3", "×4", "×5"])),
    b("So what do we multiply by next?",
      ask=ch("6", ["5", "10"], "The multiplier goes up by 1 each time: 2, 3, 4, 5. So the next one is 6.")),
    b("120 times 6. 100 sixes are 600 and 20 sixes are 120. Together that is 720.",
      w("l6", "100 × 6 = 600"), w("l7", "20 × 6 = 120"), ans("l8", "120 × 6 = 720", "720")),
    b("So the next term is 720. The trap is to use an old multiplier again. Here the multiplier itself keeps growing."),
    b("In some patterns you multiply by a different number each time. Then look for the pattern in the multipliers."),
]


# ── Q_CH16_020 ───────────────────────────────────────────────────────────────
L["Q_CH16_020"] = [
    b("The numbers are 2, 3, 5, 8, 13, 21. One more belongs at the end.", g("l1", "2, 3, 5, 8, 13, 21, ___", True)),
    b("Try the jumps: 1, 2, 3, 5, 8. That is strange. The jumps look just like the list itself, one step behind!",
      jumps("l1", ["+1", "+2", "+3", "+5", "+8"])),
    b("That is a big clue. Look at 2, 3 and 5. How is 5 made from the two numbers before it?",
      ask=ch("2 + 3", ["2 × 3", "3 + 3"], "Add the two numbers just before it. 2 plus 3 is 5.")),
    b("2 plus 3 is 5. 3 plus 5 is 8. 5 plus 8 is 13. 8 plus 13 is 21. Each number is the sum of the two before it.",
      w("l2", "2 + 3 = 5"), w("l3", "3 + 5 = 8"), w("l4", "5 + 8 = 13"), w("l5", "8 + 13 = 21")),
    b("So add the last two numbers in the list, 13 and 21. Careful: use both of them, not 21 and an old jump.",
      mk("l1", "13", "underline"), mk("l1", "21", "underline")),
    b("13 plus 21 is 34. So the missing number is 34.", ans("l6", "13 + 21 = 34", "34")),
    b("This is a famous pattern. When the jumps look odd, test whether each number is the two before it added together."),
]


# ── Q_CH16_021 ───────────────────────────────────────────────────────────────
L["Q_CH16_021"] = [
    b("Here are six numbers: 2, 5, 10, 17, 28, 37. Five follow a rule and one does not. Let's catch it.",
      g("l1", "2, 5, 10, 17, 28, 37", True), fig("f1", qfig(TOPIC, "Q_CH16_021"))),
    b("Measure the jumps. They are 3, then 5, then 7, then 11, then 9.",
      jumps("l1", ["+3", "+5", "+7", "+11", "+9"])),
    b("Most of those jumps go up nicely. Which two look out of order?",
      ask=ch("11 and 9", ["3 and 5", "5 and 7"],
             "3, 5, 7 go up by 2 each time. Next should come 9 and then 11. But here they come as 11 and then 9.")),
    b("Both of those jumps touch 28. The jump into 28 is too big, and the jump out of it is too small. So 28 is the one that breaks the pattern.",
      mk("l1", "28", "box")),
    b("What should be there instead? 17 plus 9 is 26. And then 26 plus 11 is 37, which matches the last number.",
      w("l2", "17 + 9 = 26"), w("l3", "26 + 11 = 37")),
    b("Here is another way to see it. Each number is a square number plus 1. 1 times 1 plus 1 is 2. 2 times 2 plus 1 is 5. 3 times 3 plus 1 is 10.",
      w("l4", "1 × 1 + 1 = 2"), w("l5", "2 × 2 + 1 = 5"), w("l6", "3 × 3 + 1 = 10")),
    b("Then 5 times 5 plus 1 is 26, not 28. So the number that does not belong is 28.",
      w("l7", "5 × 5 + 1 = 26"), ans("l8", "28 does not belong", "28", True)),
    b("To find the odd one out, look at the jumps. The number sitting between two jumps that don't fit is the culprit."),
]


# ── Q_CH16_022 ───────────────────────────────────────────────────────────────
L["Q_CH16_022"] = [
    b("The terms are 4, 12, 36, 108. Let's find the next term.", g("l1", "4, 12, 36, 108, ___", True)),
    b("From 4 to 12 we could add 8, or we could multiply by 3. Which of these also works from 12 to 36?",
      ask=ch("multiply by 3", ["add 8", "multiply by 2"],
             "Adding 8 to 12 does not give 36. But 12 times 3 is 36. So the rule is times 3.")),
    b("4 times 3 is 12. 12 times 3 is 36. 36 times 3 is 108. Each term is 3 times the one before.",
      w("l2", "4 × 3 = 12"), w("l3", "12 × 3 = 36"), w("l4", "36 × 3 = 108"), jumps("l1", ["×3", "×3", "×3"])),
    b("So the next term is 108 times 3. 100 threes are 300, and 8 threes are 24.",
      w("l5", "100 × 3 = 300"), w("l6", "8 × 3 = 24")),
    b("300 plus 24 is 324. So the next term is 324.", ans("l7", "108 × 3 = 324", "324")),
    b("Check by going backwards. 324 divided by 3 is 108. It fits.", w("l8", "324 ÷ 3 = 108")),
    b("One step can fool you, because adding and multiplying may both fit it. Always test your rule on a second step."),
]


# ── Q_CH16_023 ───────────────────────────────────────────────────────────────
L["Q_CH16_023"] = [
    b("This time we are given the rule: n times, n plus 1. Here n is the place of the term: 1 for the 1st, 2 for the 2nd, and so on.",
      g("l1", "2, 6, 12, 20, 30, 42", True), g("l1b", "rule: n × (n + 1)", True)),
    b("Let's test the rule. The 1st term is 1 times 2. The 2nd is 2 times 3. The 3rd is 3 times 4. Each is the place number times the number just after it.",
      w("l2", "1 × 2 = 2"), w("l3", "2 × 3 = 6"), w("l4", "3 × 4 = 12")),
    b("So for the 10th term, which two numbers do we multiply?",
      ask=ch("10 and 11", ["10 and 10", "9 and 10"],
             "Here n is 10. And n plus 1 is the number just after it, which is 11.")),
    b("n is 10, and the number just after it is 11. Careful: 9 times 10 would be the 9th term, not the 10th.",
      w("l5", "10 + 1 = 11")),
    b("10 times 11 is 110. So the 10th term is 110.", ans("l6", "10 × 11 = 110", "110")),
    b("Check the rule on the last term we can see. The 6th term should be 6 times 7, which is 42. Yes, it matches.",
      w("l7", "6 × 7 = 42"), mk("l1", "42", "underline")),
    b("When a rule uses n, put the place number in for n. Then you can jump straight to any term without listing them all."),
]


# ── Q_CH16_024 ───────────────────────────────────────────────────────────────
L["Q_CH16_024"] = [
    b("The numbers are 729, 243, 81, 27, 9. They shrink quickly. What comes next?",
      g("l1", "729, 243, 81, 27, 9, ___", True)),
    b("Look at the small end, where the numbers are easy. Which rule works at every step?",
      ask=ch("divide by 3 each time", ["take away 18 each time", "halve each time"],
             "27 take away 18 is 9, but 81 take away 18 is not 27. Dividing by 3 works every time.")),
    b("27 divided by 3 is 9. 81 divided by 3 is 27. 243 divided by 3 is 81. Each number is the one before it, divided by 3.",
      w("l2", "27 ÷ 3 = 9"), w("l3", "81 ÷ 3 = 27"), w("l4", "243 ÷ 3 = 81"), jumps("l1", ["÷3", "÷3", "÷3"], first=2)),
    b("So divide the last number by 3. 9 divided by 3 is 3.",
      nt("l1", ",", "÷3"), nt("l1", ",", "÷3", "below", 5), ans("l5", "9 ÷ 3 = 3", "3")),
    b("The trap is to subtract. 9 take away 3 is 6, but this pattern divides. It never takes away."),
    b("Check by going back up. 3 times 3 is 9, and 9 times 3 is 27. It fits.",
      w("l6", "3 × 3 = 9"), w("l7", "9 × 3 = 27")),
    b("So the next number is 3. When numbers shrink fast, test for dividing, and start with the small numbers where it is easy to see."),
]


# ── Q_CH16_025 ───────────────────────────────────────────────────────────────
L["Q_CH16_025"] = [
    b("What a tangle: 1, 1, 2, 4, 3, 9, 4, 16, 5, and then a gap. It goes up and down, so one simple rule won't do.",
      g("l1", "1, 1, 2, 4, 3, 9, 4, 16, 5, ___", True)),
    b("Read every second number, starting from the very first. What do you get?",
      ask=ch("1, 2, 3, 4, 5", ["1, 4, 9, 16", "1, 1, 2, 4"],
             "Start at the first number and skip one each time: 1, then 2, then 3, then 4, then 5.")),
    b("Two patterns are woven together. One is 1, 2, 3, 4, 5. The numbers in between are 1, 4, 9, 16.",
      lab("l2", "every second number: 1, 2, 3, 4, 5"), lab("l3", "in between: 1, 4, 9, 16, ?")),
    b("Look at each pair. 2 is followed by 4. 3 is followed by 9. 4 is followed by 16. Each in-between number is the number before it, times itself.",
      w("l4", "2 × 2 = 4"), w("l5", "3 × 3 = 9"), w("l6", "4 × 4 = 16")),
    b("The gap comes straight after the 5. So what goes there?",
      ask=ch("5 × 5", ["5 + 1", "5 × 4"],
             "The gap belongs to the in-between pattern. It is the number just before it, times itself. That is 5 times 5.")),
    b("The gap is not the next counting number. It belongs to the in-between pattern. 5 times 5 is 25.",
      ans("l7", "5 × 5 = 25", "25")),
    b("So the next term is 25. When a list zigzags, split it into two patterns, and work out which one the gap belongs to."),
]
