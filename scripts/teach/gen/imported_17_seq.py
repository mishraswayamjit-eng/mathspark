"""Number-series lessons in batch 17 that fit one of the builders in imported_17_seq_rules."""
from imported_17_seq_rules import GAP, ap, geo, grow, odd

T = "IPMTB_grade5_ch03_"
L = {}

# ── A steady step ────────────────────────────────────────────────────────────

L[T + "q018"] = ap(
    T + "q018", [1, 3, 5, GAP, 9, GAP, 13, 15], [1, 3, 5, 7, 9, 11, 13, 15],
    "Here is a series with two gaps in it. Before we can fill a gap, we need the rule the series follows.",
    ["add 3", "multiply by 3"],
    "So for any series with gaps: find the step from two neighbours, test it on another pair, then step into each gap from the number before it.",
    ask2={"before": 1, "say": "Now the second gap. It sits just after 9. What goes in it?",
          "choices": ["10", "11", "12"], "answer": 1,
          "ifNot": "The step is always add 2, and the number just before the gap is 9. So count on 2 from 9."})

L[T + "q019"] = ap(
    T + "q019", [0, 2, 4, 6, 8, 10, GAP, GAP], [0, 2, 4, 6, 8, 10, 12, 14],
    "This series starts at 0 and we want the next two numbers. So first, how does it grow?",
    ["add 1", "multiply by 2"],
    "So to carry a series on: find the step, check it, then keep adding it, each time to the newest number.",
    ask2={"before": 1, "say": "One more to find. Which number do we add 2 to this time?",
          "choices": ["10", "12"], "answer": 1,
          "ifNot": "Each number grows from the one just before it. We have just found 12, so the next one is 2 more than 12."},
    closing="So the next two numbers are 12 and 14. These are the even numbers, counting up in 2s.")

L[T + "q021"] = ap(
    T + "q021", [5, 12, 19, 26, 33, GAP], [5, 12, 19, 26, 33, 40],
    "Five numbers, and we want the one that comes next. Let's find out how this series moves.",
    ["add 6", "add 8"],
    "So the plan: subtract neighbours to find the step, check it on a second pair, then add it to the last number.",
    ask2={"before": 0, "say": "So what comes after 33?", "choices": ["36", "40", "37"], "answer": 1,
          "ifNot": "The step is add 7. Start at 33 and count on 7: that takes us past 37, all the way to 40."},
    closing="So the next number in the series is 40.")

L[T + "q027"] = ap(
    T + "q027", [123, 234, GAP, 456, 567, 678], [123, 234, 345, 456, 567, 678],
    "Look at these numbers: 123, then 234, then a gap. One number is missing, and we are going to find it.",
    ["add 11", "add 101"],
    "So when a number is missing from the middle: find the step, step into the gap, and check that the next step lands on the number after it.",
    closing="So the missing number is 345. Look at its digits, 3, 4, 5: every digit climbs by 1 each time, which is what adding 111 does.")

L[T + "q028"] = ap(
    T + "q028", [GAP, 34, 51, 68, GAP], [17, 34, 51, 68, 85],
    "This series is missing a number at each end. The three in the middle will tell us the rule.",
    ["add 15", "add 34"],
    "So remember: to go forwards along a series, do the step. To go backwards, undo it.",
    ask2={"before": 0, "say": "The first gap is in front of 34. To step backwards from 34, what do we do?",
          "choices": ["add 17", "take away 17"], "answer": 1,
          "ifNot": "Going forwards, we add 17. Going backwards, we undo that. So we take 17 away from 34."},
    closing="So the missing numbers are 17 and 85. This is the 17 times table: 17, 34, 51, 68, 85.")

L[T + "q031"] = ap(
    T + "q031", [88, 66, 44, 22, GAP], [88, 66, 44, 22, 0],
    "These numbers are getting smaller: 88, 66, 44, 22. We want the one that comes next.",
    ["take away 2", "take away 11"],
    "So for a series that goes down: subtract neighbours to find the step, then take that step away from the last number.",
    answer_text={4: "00"},
    closing="The choices write zero as 00, with two digits, to match 88, 66, 44 and 22. So the missing number is 00, which is simply zero.")

L[T + "q036"] = ap(
    T + "q036", [15, 30, GAP, GAP, 75], [15, 30, 45, 60, 75],
    "Two gaps side by side this time, with 75 waiting at the end. The 15 and the 30 are our clue.",
    ["add 30", "add 10"],
    "So when the gaps sit together: find the step, fill them one after the other, and use the number after the gaps as your check.",
    ask2={"before": 1, "say": "Now the second gap. Which number do we add 15 to?",
          "choices": ["30", "45"], "answer": 1,
          "ifNot": "The second gap comes straight after the number we have just found. So we add 15 to 45, not to 30 again."},
    closing="So the missing numbers are 45 and 60, and the rule held all the way to 75.")

L[T + "q041"] = ap(
    T + "q041", [2, 4, 6, GAP, 10, GAP, 14, 16], [2, 4, 6, 8, 10, 12, 14, 16],
    "Eight places in this series, and two of them are empty. Let's work out the rule, then fill them.",
    ["add 4", "add 1"],
    "So the method is: find the step, test it, and fill each gap from the number just before it. Then check with the number just after.",
    ask2={"before": 1, "say": "On to the second gap, the one after 10. What goes there?",
          "choices": ["12", "11", "13"], "answer": 0,
          "ifNot": "The number before the gap is 10, and the step is add 2. So we want 2 more than 10."})

# ── One number that does not fit ─────────────────────────────────────────────

L[T + "q013"] = odd(
    T + "q013", [1, 8, 15, 22, 29, 38], 5,
    "One of these six numbers does not belong. To catch it, we first find the rule the others follow.",
    ["add 8", "add 6"], [29, 22],
    "So to find the odd one out: find the step, then test every jump, right to the end. The number where the step breaks is the one.")

L[T + "q020"] = odd(
    T + "q020", [7, 14, 21, 25, 35, 42], 3,
    "Somewhere in this series a number has sneaked in that should not be there. Let's find the pattern first.",
    ["add 14", "add 6"], [21, 35],
    "So when one number in the middle does not fit, two jumps break. The odd one out is the number that sits in both of them.",
    rule_say="14 minus 7 is 7, and 21 minus 14 is 7. Going up in 7s, starting from 7: this is the 7 times table. Now we test every jump.")

L[T + "q046"] = odd(
    T + "q046", [2, 10, 18, 26, 35, 42], 4,
    "Five of these numbers follow one rule and one of them breaks it. Let's find the rule first.",
    ["add 10", "add 6"], [26, 42],
    "So test every jump. When two jumps in a row do not fit, look for the number they share: that is the odd one out.")

# ── Multiply or divide each time ─────────────────────────────────────────────

L[T + "q023"] = geo(
    T + "q023", [1, 3, 9, 27, 81], "×", 3,
    "This series climbs slowly at first and then very fast: 1, 3, 9, 27, 81. That is a clue about its rule.",
    ["add 2", "multiply by 2"], [108, 729],
    "The move is multiply by 3, and we do it just once. So we want 81 times 3.",
    "So when the jumps keep growing, try dividing a number by the one before it. If the answer is the same each time, the rule is to multiply.")

L[T + "q033"] = geo(
    T + "q033", [32, 16, 8, 4], "÷", 2,
    "These numbers shrink quickly: 32, 16, 8, 4. We want the one that comes next.",
    ["take away 16", "divide by 4"], [1, 0],
    "The move is divide by 2, and we do it just once. So we want half of 4.",
    "So when a series shrinks by smaller and smaller jumps, test for halving, or dividing by the same number each time.")

L[T + "q042"] = geo(
    T + "q042", [2, 4, 8, 16, 32], "×", 2,
    "2, 4, 8, 16, 32. You may know these numbers already. Let's find the rule properly, then the number that comes next.",
    ["add 2", "multiply by 4"], [48, 256],
    "The move is multiply by 2, and we do it just once. So we want double 32.",
    "So if adding does not explain a series, try multiplying. Here every number is double the one before.")

# ── The jump itself changes ──────────────────────────────────────────────────

L[T + "q025"] = grow(
    T + "q025", [2, 5, 10, 17, 26], 2,
    "We want the next two numbers after 26. This series has a small twist in it, so let's go carefully.",
    [9, 10],
    "So when the jumps are not equal, write the jumps down as a series of their own. Find their pattern, and it gives you the next jump.")

L[T + "q043"] = grow(
    T + "q043", [6, 13, 19, 24, 28], 1,
    "This series is still climbing, but look how it slows down: 6, 13, 19, 24, 28. Let's see what is going on.",
    [4, 5],
    "So when a series slows down, write out its jumps. Here they shrink by 1 each time, and that tells us the next jump.")

L[T + "q044"] = grow(
    T + "q044", [1, 2, 4, 7, 11, 16], 2,
    "Six numbers, and we want the two that follow 16. The numbers spread out more and more as we go.",
    [5, 10],
    "So when the jumps keep changing, list them. If the jumps grow by 1 each time, keep them growing to find what comes next.")
