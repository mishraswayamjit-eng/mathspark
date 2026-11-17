"""Lessons written by hand for the questions in batch 04 that are not one plain line."""
from imported_04_lib import ANS, B, BOX, CHOOSE, CIRC, GIVEN, GIVENM, LB, LESSON, NOTE, STRIKE, UL, W, last_nth  # noqa: F401

P = "AIGEN_grade5_"
T = "IPMTB_grade5_ch07_"

LESSONS = {}

# ── Money and counting stories with no line given: build the line, then work it ──

# Raju's team fund: 200, six players give 15 each, 10 taken out.
LESSONS[P + "38dd3071-b434-4c5b-8213-3369e40a515a"] = LESSON(
    B("Raju's team fund starts with 200 rupees. Then 6 players put in 15 rupees each, and the coach takes out 10 rupees for a ball. How much is in the fund now?",
      GIVEN("q", "Start ₹200, 6 players × ₹15 in, ₹10 out")),
    B("Let's write the whole story as one line. Start with 200, add 6 lots of 15, then take away 10.",
      W("l1", "200 + 6 × 15 − 10")),
    B("Which piece of this line do we work out first?",
      ask=CHOOSE(["200 + 6", "6 × 15", "15 − 10"], 1,
                 "Think about the story. The players give 6 lots of 15 rupees, and we need that amount before we can add it. Times goes before plus and minus.")),
    B("6 times 15 is 90. That is what the players put in altogether.",
      UL("l1", "6 × 15"), NOTE("l1", "6 × 15", "90"), W("l2", "200 + 90 − 10")),
    B("Now only plus and minus are left, so we go left to right. 200 plus 90 is 290.",
      W("l3", "200 + 90 = 290")),
    B("Then the coach takes out 10. 290 minus 10 is 280, so the fund has 280 rupees.",
      ANS("l4", "290 − 10 = 280"), CIRC("l4", "280")),
    B("Here is the trap. Adding 200 and 6 first, just because they come first, would be adding rupees to players. The story tells you that makes no sense."),
    B("Check by walking backwards. 280 plus 10 is 290, and 290 minus 90 is 200, the money the fund started with.",
      W("l5", "280 + 10 = 290"), W("l6", "290 − 90 = 200")),
    B("So in a money story, work out each lot of so many each first. Then add and take away in the order things happened."),
)

# Priya: 100 rupees, 6 boxes at 9, the rest shared between 2 cousins.
LESSONS[P + "a1a76164-cb03-4478-8bc5-db4371e36f61"] = LESSON(
    B("Priya has 100 rupees. She buys 6 boxes of sparklers at 9 rupees each, then shares what is left equally between her 2 cousins.",
      GIVEN("q", "₹100, buys 6 boxes × ₹9, rest shared by 2")),
    B("What do we need to find first?",
      ask=CHOOSE(["100 ÷ 2", "6 × 9, the cost of the sparklers", "100 − 6"], 1,
                 "The cousins only share what is left after the shopping. So first we need to know what the sparklers cost: 6 boxes at 9 rupees each.")),
    B("6 times 9 is 54. The sparklers cost 54 rupees.",
      W("l1", "6 × 9 = 54")),
    B("Take that away from her 100 rupees. 100 minus 54 is 46, so 46 rupees are left.",
      W("l2", "100 − 54 = 46")),
    B("Now share the 46 rupees between the 2 cousins. 46 divided by 2 is 23, so each cousin gets 23 rupees.",
      ANS("l3", "46 ÷ 2 = 23"), CIRC("l3", "23")),
    B("As one line it looks like this. The brackets say: finish the shopping first, and only then share.",
      W("l4", "(100 − 6 × 9) ÷ 2 = 23"), UL("l4", "(100 − 6 × 9)")),
    B("Careful: 46 is one of the choices, but 46 is the money left over. The question asks for one cousin's share, so there is still a divide to do."),
    B("Check: 23 plus 23 is 46, and 46 plus 54 is 100. Every rupee is accounted for.",
      W("l5", "23 + 23 = 46"), W("l6", "46 + 54 = 100")),
    B("So follow the story in order: spend first, see what is left, then share it out."),
)

# Meena: 3 packets at 15, 2 packets at 9, pays with 80.
LESSONS[P + "c060004c-cd2d-4c04-a71d-dfb43a9db862"] = LESSON(
    B("Meena buys 3 packets of coloured powder at 15 rupees each and 2 packets of glitter at 9 rupees each. She pays with 80 rupees. How much change comes back?",
      GIVEN("q", "3 × ₹15 and 2 × ₹9, paid with ₹80")),
    B("Change is what is left after paying for everything. So we start with 80 and take away both costs.",
      W("l1", "80 − 3 × 15 − 2 × 9")),
    B("Which pieces of this line do we work out first?",
      ask=CHOOSE(["80 − 3", "3 × 15 and 2 × 9", "15 − 2"], 1,
                 "We cannot take a cost away until we know it. So the two times come first: 3 times 15, and 2 times 9.")),
    B("3 times 15 is 45. That is the coloured powder.",
      UL("l1", "3 × 15"), NOTE("l1", "3 × 15", "45")),
    B("2 times 9 is 18. That is the glitter. Now write the line again with 45 and 18 in place.",
      UL("l1", "2 × 9"), NOTE("l1", "2 × 9", "18"), W("l2", "80 − 45 − 18")),
    B("Take them off one at a time, left to right. 80 minus 45 is 35.",
      W("l3", "80 − 45 = 35")),
    B("And 35 minus 18 is 17. Meena gets 17 rupees back.",
      ANS("l4", "35 − 18 = 17"), CIRC("l4", "17")),
    B("The trap is stopping after one item. Taking off only the powder leaves 35, but the glitter has to be paid for too."),
    B("Check another way. The whole bill is 45 plus 18, which is 63. And 63 plus 17 is 80, the money she paid.",
      W("l5", "45 + 18 = 63"), W("l6", "63 + 17 = 80")),
    B("So for change: find the cost of each kind of thing, take every cost away from the money paid, and check by adding back."),
)

# Arjun's diyas: 4 packets of 15, gives 2 packets of 6, gift of (3 + 5) × 3, 4 broken.
LESSONS[P + "e4d78058-ffe3-43c7-8dfb-8107f58e4dba"] = LESSON(
    B("Arjun buys 4 packets of 15 diyas and gives away 2 packets of 6. Grandmother gifts him 3 plus 5, in brackets, times 3 more, and then 4 break. How many are left?",
      GIVEN("q", "4 × 15 bought, 2 × 6 given, (3 + 5) × 3 gift, 4 broken")),
    B("Let's put the story in one line. Diyas bought, minus diyas given away, plus the gift, minus the broken ones.",
      W("l1", "4 × 15 − 2 × 6 + (3 + 5) × 3 − 4")),
    B("Which piece of this line do we work out first?",
      ask=CHOOSE(["4 × 15", "3 + 5", "6 + 3"], 1,
                 "Look for the brackets. Whatever sits inside brackets is done before anything else, even before a times. So 3 plus 5 goes first.")),
    B("3 plus 5 is 8, so the gift is 8 times 3.",
      UL("l1", "(3 + 5)"), NOTE("l1", "(3 + 5)", "8"), W("l2", "4 × 15 − 2 × 6 + 8 × 3 − 4")),
    B("Now the times, before any plus or minus. 4 times 15 is 60 diyas bought, and 2 times 6 is 12 given away.",
      UL("l2", "4 × 15"), NOTE("l2", "4 × 15", "60"), UL("l2", "2 × 6"), NOTE("l2", "2 × 6", "12")),
    B("And 8 times 3 is 24 from Grandmother. Write the line again with 60, 12 and 24 in place.",
      UL("l2", "8 × 3"), NOTE("l2", "8 × 3", "24"), W("l3", "60 − 12 + 24 − 4")),
    B("Only plus and minus now, so we go left to right. 60 minus 12 is 48, and 48 plus 24 is 72.",
      W("l4", "60 − 12 = 48"), W("l5", "48 + 24 = 72")),
    B("Last, the 4 broken ones. 72 minus 4 is 68, so Arjun has 68 diyas.",
      ANS("l6", "72 − 4 = 68"), CIRC("l6", "68")),
    B("Name the trap: the gift. Skip the brackets and you might do 5 times 3 first, which gives a different gift. The brackets say add 3 and 5 first."),
    B("Check by walking backwards. 68 plus 4 is 72, 72 minus 24 is 48, and 48 plus 12 is 60, the diyas he bought.",
      W("l7", "68 + 4 = 72"), W("l8", "72 − 24 = 48"), W("l9", "48 + 12 = 60")),
    B("So turn the story into one line. Then brackets first, times next, and plus and minus from left to right."),
)

# ── Brackets inside brackets ──

# 11 − [17 − {15 − 3(7 − 4)}]
LESSONS[T + "q003"] = LESSON(
    B("Three kinds of brackets here, one inside another, like boxes inside boxes. We open the innermost box first and work our way out.",
      GIVENM("l1", "11 − [17 − {15 − 3(7 − 4)}]")),
    B("Which brackets are the innermost ones?",
      ask=CHOOSE(["the square ones [ ]", "the curly ones { }", "the round ones ( )"], 2,
                 "Look for the brackets that have no other brackets inside them. Those are the round ones, around 7 minus 4.")),
    B("7 minus 4 is 3. And the 3 standing right outside that bracket means 3 times, so now we have 3 times 3.",
      UL("l1", "(7 − 4)"), NOTE("l1", "(7 − 4)", "3"), W("l2", "11 − [17 − {15 − 3 × 3}]")),
    B("Inside the curly brackets we now have 15 minus 3 times 3. What comes first?",
      ask=CHOOSE(["15 − 3", "3 × 3"], 1,
                 "Times goes before minus, even inside brackets. So 3 times 3 comes first.")),
    B("3 times 3 is 9. Careful: taking 3 away from 15 first is the classic slip here.",
      UL("l2", "3 × 3"), NOTE("l2", "3 × 3", "9"), W("l3", "11 − [17 − {15 − 9}]")),
    B("Now the curly brackets hold 15 minus 9, and that is 6.",
      UL("l3", "{15 − 9}"), NOTE("l3", "{15 − 9}", "6"), W("l4", "11 − [17 − 6]")),
    B("Next, the square brackets. 17 minus 6 is 11.",
      UL("l4", "[17 − 6]"), NOTE("l4", "[17 − 6]", "11"), W("l5", "11 − 11")),
    B("And 11 minus 11 is 0. All that work, and it comes to nothing at all!",
      ANS("l6", "11 − 11 = 0"), CIRC("l6", "0")),
    B("Check the layers once more: the round brackets gave 3, the curly ones gave 6, the square ones gave 11. And 11 take away 11 is 0.",
      W("l7", "11 − [17 − {15 − 9}] = 0")),
    B("So with brackets inside brackets, work from the inside out: round, then curly, then square."),
)

# (8 − 7) × [8 + 2 × bar(5 − 1)]
LESSONS[T + "q004"] = LESSON(
    B("This line has round brackets, square brackets, and a bar over 5 minus 1. A bar works like the tightest bracket of all.",
      GIVEN("l1", "(8 − 7) × [8 + 2 × bar(5 − 1)]")),
    B("So which piece do we work out first?",
      ask=CHOOSE(["8 − 7", "8 + 2", "5 − 1, under the bar"], 2,
                 "The bar is the innermost bracket. So the piece under the bar, 5 minus 1, goes before everything else.")),
    B("5 minus 1 is 4. Write the line again with 4 where the bar was.",
      UL("l1", "bar(5 − 1)"), NOTE("l1", "bar(5 − 1)", "4"), W("l2", "(8 − 7) × [8 + 2 × 4]")),
    B("Now look inside the square brackets: 8 plus 2 times 4. What comes first in there?",
      ask=CHOOSE(["8 + 2", "2 × 4"], 1,
                 "Times goes before plus, even inside brackets. So 2 times 4 comes first.")),
    B("2 times 4 is 8. Careful: adding the 8 and the 2 first is the trap in this one.",
      UL("l2", "2 × 4"), NOTE("l2", "2 × 4", "8"), W("l3", "(8 − 7) × [8 + 8]")),
    B("Now finish both brackets. 8 minus 7 is 1, and 8 plus 8 is 16.",
      UL("l3", "(8 − 7)"), NOTE("l3", "(8 − 7)", "1"), UL("l3", "[8 + 8]"), NOTE("l3", "[8 + 8]", "16"), W("l4", "1 × 16")),
    B("1 times 16 is 16. Multiplying by 1 changes nothing, so the answer is 16.",
      ANS("l5", "1 × 16 = 16"), CIRC("l5", "16", last_nth("1 × 16 = 16", "16"))),
    B("Check the square brackets backwards: 16 minus 8 is 8, and that 8 was our 2 times 4. It all fits.",
      W("l6", "16 − 8 = 8")),
    B("So work from the inside out: the bar, then the brackets. And inside each one, times before plus."),
)

# ── 'of' in a line ──

# 16 − 12 ÷ 4 + 1/2 of 10
LESSONS[T + "q011"] = LESSON(
    B("This line has a minus, a divide, a plus, and the little word of. Let's sort out what of means first.",
      GIVENM("l1", "16 − 12 ÷ 4 + 1/2 of 10")),
    B("What does half of 10 ask us to do?",
      ask=CHOOSE(["add 1/2 and 10", "multiply: 1/2 × 10", "take 1/2 away from 10"], 1,
                 "Of means times. Half of 10 means a half times 10, which is the same as cutting 10 into 2 equal parts.")),
    B("Half of 10 is 5. Of is a kind of times, so it is done early, before any plus or minus.",
      UL("l1", "1/2 of 10"), NOTE("l1", "1/2 of 10", "5")),
    B("The divide goes early too: 12 divided by 4 is 3. Now write the line again with 3 and 5 in place.",
      UL("l1", "12 ÷ 4"), NOTE("l1", "12 ÷ 4", "3"), W("l2", "16 − 3 + 5")),
    B("The trap was at the very start: 16 minus 12 looks ready to go. But that 12 belongs to the divide, so it had to be divided by 4 first."),
    B("Only minus and plus are left, so we go left to right. 16 minus 3 is 13.",
      W("l3", "16 − 3 = 13")),
    B("And 13 plus 5 is 18. That is our answer.",
      ANS("l4", "13 + 5 = 18"), CIRC("l4", "18")),
    B("Check by walking backwards. 18 minus 5 is 13, and 13 plus 3 is 16, right where the line started.",
      W("l5", "18 − 5 = 13"), W("l6", "13 + 3 = 16")),
    B("So: of and divide first, then plus and minus from left to right."),
)

# 20 − 8 ÷ 2 + 1/3 of 18
LESSONS[T + "q027"] = LESSON(
    B("A minus, a divide, a plus, and a fraction of a number, all in one line. The order we choose decides the answer.",
      GIVENM("l1", "20 − 8 ÷ 2 + 1/3 of 18")),
    B("Which pieces get done before the minus and the plus?",
      ask=CHOOSE(["20 − 8", "8 ÷ 2 and 1/3 of 18", "2 + 1/3"], 1,
                 "Of means times, and times and divide always go before plus and minus. So the two early jobs are 8 divided by 2, and a third of 18.")),
    B("Start with the of. A third of 18 means 18 shared into 3 equal parts, and 18 divided by 3 is 6.",
      UL("l1", "1/3 of 18"), NOTE("l1", "1/3 of 18", "6"), W("l2", "18 ÷ 3 = 6")),
    B("Now the divide. 8 divided by 2 is 4. Write the line again with 4 and 6 in place.",
      UL("l1", "8 ÷ 2"), NOTE("l1", "8 ÷ 2", "4"), W("l3", "20 − 4 + 6")),
    B("Only minus and plus are left: 20 minus 4 plus 6. Which do we do first?",
      ask=CHOOSE(["20 − 4", "4 + 6"], 0,
                 "Plus and minus are equal partners, so we read from left to right, like a sentence. That means 20 minus 4 comes first.")),
    B("Left to right it is: 20 minus 4 is 16.",
      W("l4", "20 − 4 = 16")),
    B("And 16 plus 6 is 22. That is our answer.",
      ANS("l5", "16 + 6 = 22"), CIRC("l5", "22")),
    B("Name the trap: starting with 20 minus 8 because it is on the left. That 8 belongs to the divide, so it must be halved first."),
    B("Check by walking backwards. 22 minus 6 is 16, and 16 plus 4 is 20, right where the line started.",
      W("l6", "22 − 6 = 16"), W("l7", "16 + 4 = 20")),
    B("So: of and divide go first, then plus and minus from left to right."),
)

# 10 + 10 × 10 = 100 + □
LESSONS[T + "q014"] = LESSON(
    B("Two sides, and they must be worth the same. On the left, 10 plus 10 times 10. On the right, 100 plus a missing number in the box.",
      GIVEN("l1", "10 + 10 × 10 = 100 + □")),
    B("Start with the left side. What is 10 plus 10 times 10?",
      ask=CHOOSE(["200", "110", "30"], 1,
                 "Times goes before plus. So first 10 times 10 is 100, and only then do we add the other 10.")),
    B("10 times 10 is 100. Then 10 plus 100 is 110, so the left side is worth 110.",
      UL("l1", "10 × 10"), NOTE("l1", "10 × 10", "100"), W("l2", "10 + 100 = 110")),
    B("The trap is adding the two 10s first and then multiplying. That gives 200, but it is a different sum: the one with brackets round 10 plus 10.",
      W("l3", "(10 + 10) × 10 = 200")),
    B("Now the right side has to be worth 110 as well. So 100 plus what makes 110?",
      W("l4", "100 + ? = 110"),
      ask=CHOOSE(["10", "100", "0"], 0,
                 "We need to climb from 100 up to 110. The gap between them is the number in the box.")),
    B("110 minus 100 is 10. So the box holds 10.",
      ANS("l5", "110 − 100 = 10"), CIRC("l5", "10", last_nth("110 − 100 = 10", "10"))),
    B("Check: with 10 in the box, the right side is 100 plus 10, which is 110. The left side is 110 too, so the two sides match.",
      W("l6", "10 + 10 × 10 = 100 + 10")),
    B("So when one side has a box: work out the complete side first, with times before plus. Then find what makes the other side match."),
)

# ── True or not true ──

# Which is correct: 7 + 7 × 7 = 77, 25 + 7 × 0 = 0, 6 + 6 − 6 × 6 ÷ 6 = 6, 16[2 + 3 × 2 − 8] = 16
_C15 = "6 + 6 − 6 × 6 ÷ 6 = 6"
LESSONS[T + "q015"] = LESSON(
    B("Four number sentences, and only one of them is true. We will test each one, using the proper order every time.",
      GIVEN("q", "Which one is correct?"), LB("a", "7 + 7 × 7 = 77"), LB("b", "25 + 7 × 0 = 0"),
      LB("c", _C15), LB("d", "16[2 + 3 × 2 − 8] = 16")),
    B("Take the first one, 7 plus 7 times 7. What do we work out first?",
      ask=CHOOSE(["7 + 7", "7 × 7"], 1,
                 "Times goes before plus, wherever it sits. So 7 times 7 comes first.")),
    B("7 times 7 is 49, and 7 plus 49 is 56. The sentence says 77, so it is not true.",
      W("a1", "7 × 7 = 49"), W("a2", "7 + 49 = 56"), STRIKE("a", "77", "56")),
    B("Next one. The 0 only wipes out the 7 it multiplies: 7 times 0 is 0. So this is 25 plus 0, which is 25, not 0.",
      W("b1", "25 + 7 × 0 = 25"), STRIKE("b", "0", "25", last_nth("25 + 7 × 0 = 0", "0"))),
    B("Now the third one. Which piece of it goes first?",
      ask=CHOOSE(["6 + 6", "6 × 6", "6 − 6"], 1,
                 "Times and divide go before plus and minus. Reading from the left, the first of them is 6 times 6.")),
    B("6 times 6 is 36, and 36 divided by 6 is 6. So that whole piece is worth 6.",
      UL("c", "6 × 6 ÷ 6"), W("c1", "6 × 6 = 36"), W("c2", "36 ÷ 6 = 6")),
    B("Now the line reads 6 plus 6 minus 6. Left to right, 6 plus 6 is 12, and 12 minus 6 is 6.",
      W("c3", "6 + 6 = 12"), W("c4", "12 − 6 = 6")),
    B("The sentence says 6, and we got 6. This one is true!",
      BOX("c", _C15)),
    B("Let's make sure of the last one. Inside the brackets, 3 times 2 is 6, then 2 plus 6 is 8, and 8 minus 8 is 0.",
      W("d1", "2 + 3 × 2 − 8 = 0")),
    B("A number standing right outside a bracket means times. 16 times 0 is 0, not 16, so that one is not true.",
      W("d2", "16 × 0 = 0"), STRIKE("d", "16", "0", last_nth("16[2 + 3 × 2 − 8] = 16", "16"))),
    B("So the only true sentence is 6 plus 6, minus 6 times 6 divided by 6, equals 6.",
      ANS("ans", _C15), CIRC("ans", _C15)),
    B("To test a number sentence, work out the left side by the rules. Then see whether it really matches the right side."),
)

# Which is NOT correct. The one that is not: 8 ÷ 2 × 6 − 3 ÷ 9 + 27 = 3
_C31 = "8 ÷ 2 × 6 − 3 ÷ 9 + 27 = 3"
LESSONS[T + "q031"] = LESSON(
    B("Four number sentences. Three of them are true and one is not, and we are hunting for the one that is not.",
      GIVEN("q", "Which one is NOT correct?")),
    B("Take the first one. Of means times, so we need a fifth of 125. 125 shared into 5 equal parts is 25.",
      W("a", "1/5 of 125 ÷ 25 − 1 = 0"), UL("a", "1/5 of 125"), W("a1", "1/5 of 125 = 25")),
    B("Then 25 divided by 25 is 1, and 1 minus 1 is 0. It says 0, so this one is true.",
      W("a2", "25 ÷ 25 − 1 = 0")),
    B("The next one ends in times 0. Anything times 0 is 0, so it is true whatever the brackets come to.",
      W("b", "{9 − 3 − (7 + 6 − 6 − 6 − 7)} × 0 = 0"), BOX("b", "× 0")),
    B("Now this one, which claims to equal 3. Which pieces do we work out first?",
      LB("c", _C31),
      ask=CHOOSE(["8 ÷ 2 × 6, and 3 ÷ 9", "2 × 6 − 3", "9 + 27"], 0,
                 "Divide and times go before minus and plus. So the early jobs are 8 divided by 2 times 6, and 3 divided by 9.")),
    B("Left to right: 8 divided by 2 is 4, and 4 times 6 is 24.",
      UL("c", "8 ÷ 2 × 6"), W("c1", "8 ÷ 2 × 6 = 24")),
    B("3 divided by 9 does not come out whole. It is 3 parts out of 9, which is just a third.",
      UL("c", "3 ÷ 9"), W("c2", "3 ÷ 9 = 1/3"), W("c3", "24 − 1/3 + 27")),
    B("24 plus 27 is 51, and taking away a third leaves more than 50. That is nowhere near 3!",
      W("c4", "24 + 27 = 51"), W("c5", "51 − 1/3 > 50"), STRIKE("c", "3", "over 50", last_nth(_C31, "3"))),
    B("So this sentence is not true. Let's make sure the last one is fine. It starts with a quarter divided by three quarters.",
      W("d", "(1/4) ÷ (3/4) ÷ (2/4) × (4/3) = 8/9")),
    B("Three quarters is 3 times as big as a quarter. So a quarter divided by three quarters is a third.",
      W("d1", "(1/4) ÷ (3/4) = 1/3")),
    B("Next, divide that third by two quarters. Two quarters is a half, and dividing by a half doubles, so we get two thirds.",
      W("d2", "(1/3) ÷ (2/4) = 2/3")),
    B("Last, two thirds times 4 over 3. On top 2 times 4 is 8, underneath 3 times 3 is 9, so we get 8 over 9, just as it says.",
      W("d3", "(2/3) × (4/3) = 8/9")),
    B("So the one that is not correct is 8 divided by 2, times 6, minus 3 divided by 9, plus 27. It does not equal 3.",
      ANS("ans", "8 ÷ 2 × 6 − 3 ÷ 9 + 27 ≠ 3"), CIRC("ans", "≠ 3")),
    B("Two traps here: stopping at the first sentence that looks odd, and forgetting the question wants the one that is not true. Work every sentence out by the rules."),
)

# ── One-off lines ──

# [70 + {5 × 8 − (12 − 3 × 5)}] × 3
LESSONS[T + "q018"] = LESSON(
    B("Round brackets inside curly ones inside square ones, and a times 3 waiting at the end. We start in the middle and work outwards.",
      GIVENM("l1", "[70 + {5 × 8 − (12 − 3 × 5)}] × 3")),
    B("The round brackets hold 12 minus 3 times 5. What goes first in there?",
      ask=CHOOSE(["12 − 3", "3 × 5"], 1,
                 "Times goes before minus, even inside brackets. So 3 times 5 comes first.")),
    B("3 times 5 is 15. So the round brackets now hold 12 minus 15.",
      UL("l1", "3 × 5"), NOTE("l1", "3 × 5", "15"), W("l2", "[70 + {5 × 8 − (12 − 15)}] × 3")),
    B("Here is something unusual: 15 is bigger than 12. Taking 15 from 12 lands us 3 below zero, and we write that as minus 3.",
      W("l3", "12 − 15 = −3")),
    B("Now the curly brackets. 5 times 8 is 40, so they hold 40, take away minus 3.",
      UL("l2", "5 × 8"), NOTE("l2", "5 × 8", "40"), W("l4", "[70 + {40 − (−3)}] × 3")),
    B("What does taking away minus 3 do to the 40?",
      ask=CHOOSE(["makes it 3 smaller: 37", "makes it 3 bigger: 43", "leaves it at 40"], 1,
                 "Think of minus 3 as owing 3 rupees. If someone takes that debt away, you are 3 rupees better off. So taking away minus 3 is the same as adding 3.")),
    B("So 40 take away minus 3 is 40 plus 3, which is 43. That finishes the curly brackets.",
      W("l5", "40 − (−3) = 40 + 3"), W("l6", "[70 + 43] × 3")),
    B("Square brackets next: 70 plus 43 is 113.",
      UL("l6", "[70 + 43]"), NOTE("l6", "[70 + 43]", "113"), W("l7", "113 × 3")),
    B("Last of all, the times 3. 113 times 3 is 339.",
      ANS("l8", "113 × 3 = 339"), CIRC("l8", "339")),
    B("The trap was in the middle. Treat 12 minus 15 as a plain 3 and you would take 3 off the 40, when really 3 gets added on."),
    B("Check that last times: 100 times 3 is 300, 13 times 3 is 39, and 300 plus 39 is 339.",
      W("l9", "100 × 3 + 13 × 3 = 339"), W("l10", "300 + 39 = 339")),
    B("So peel the brackets from the inside out: round, curly, square. And inside each one, times goes before plus and minus."),
)

# (7 + 2 − 14 × (1/2) − 5 − 2) × 0
_L26 = "(7 + 2 − 14 × (1/2) − 5 − 2) × 0"
LESSONS[T + "q026"] = LESSON(
    B("A long bracket, full of work to do. But before starting any of it, look at what is waiting right at the end of the line.",
      GIVENM("l1", _L26)),
    B("The whole bracket is multiplied by 0. What does that do?",
      BOX("l1", "× 0"),
      ask=CHOOSE(["Nothing: the answer is the bracket", "It makes the whole answer 0", "It takes 0 away"], 1,
                 "Times 0 means zero lots of something. Zero lots of any number, big or small, is nothing at all.")),
    B("Think of 3 times 0 as 3 empty plates: nothing on any of them. Even 1000 empty plates still hold nothing.",
      W("l2", "3 × 0 = 0"), W("l3", "1000 × 0 = 0")),
    B("So whatever the bracket comes to, the answer will be 0. We do not even need to work the bracket out!",
      UL("l1", "(7 + 2 − 14 × (1/2) − 5 − 2)"), NOTE("l1", "(7 + 2 − 14 × (1/2) − 5 − 2)", "any number")),
    B("The bracket, times 0, equals 0.",
      ANS("l4", _L26 + " = 0"), CIRC("l4", "0", last_nth(_L26 + " = 0", "0"))),
    B("The trap is diving into the bracket, with its half of 14 and all those take aways, and making a slip in there. None of it was needed."),
    B("So look before you leap: scan the whole line first. If everything is multiplied by 0, the answer is 0."),
)

# 5 × 125 × 15 ÷ 625 × 3 × 45
LESSONS[T + "q032"] = LESSON(
    B("Only times and divide in this line, no plus or minus at all. Times and divide are equal partners, so we go from left to right.",
      GIVENM("l1", "5 × 125 × 15 ÷ 625 × 3 × 45")),
    B("Start on the left with 5 times 125. 5 times 100 is 500, and 5 times 25 is 125, so together that is 625.",
      UL("l1", "5 × 125"), W("l2", "5 × 100 = 500"), W("l3", "5 × 25 = 125"), W("l4", "5 × 125 = 625")),
    B("So now the line starts 625 times 15, divided by 625. Do you spot anything?",
      W("l5", "625 × 15 ÷ 625 × 3 × 45"),
      ask=CHOOSE(["Work out 625 × 15 the long way", "× 625 and ÷ 625 undo each other", "Divide 15 by 625"], 1,
                 "We multiply by 625 and then divide by 625. One undoes the other, like a step forward and then a step back. So only the 15 is left.")),
    B("Times 625 and divided by 625 cancel each other out. That leaves just the 15.",
      STRIKE("l5", "625 ×"), STRIKE("l5", "÷ 625"), W("l6", "15 × 3 × 45")),
    B("Carry on, left to right. 15 times 3 is 45, so we are left with 45 times 45.",
      W("l7", "15 × 3 = 45"), W("l8", "45 × 45")),
    B("Split one 45 into 40 and 5. 45 times 40 is 1800, and 45 times 5 is 225.",
      W("l9", "45 × 40 = 1800"), W("l10", "45 × 5 = 225")),
    B("1800 plus 225 is 2025. So the whole line is worth 2025.",
      W("l11", "1800 + 225 = 2025"), ANS("l12", "45 × 45 = 2025"), CIRC("l12", "2025")),
    B("Careful with the divide sign: it only belongs to the 625 right after it. The 3 and the 45 are still multiplying, so the answer stays big."),
    B("Check the shortcut the long way: 625 times 15 is 9375, and 9375 divided by 625 is 15 again.",
      W("l13", "625 × 15 = 9375"), W("l14", "9375 ÷ 625 = 15")),
    B("So with only times and divide: go left to right, and watch for a times and a divide by the same number, because they cancel."),
)

# How many three-digit even numbers are there?
LESSONS["IPMTB_grade5_ch02_q018"] = LESSON(
    B("How many three-digit numbers are even? Counting them one by one would take all day, so let's be clever about it.",
      GIVEN("q", "Three-digit even numbers: how many?")),
    B("First, all the three-digit numbers. The numbers from 1 to 99 have one or two digits, so the three-digit ones run from 100 up to 999.",
      LB("r0", "1 to 99: one or two digits"), LB("r1", "100 to 999: three digits")),
    B("How many numbers is that, from 100 to 999?",
      ask=CHOOSE(["899", "900", "999"], 1,
                 "Think of all the numbers from 1 to 999. That is 999 numbers. The first 99 of them are too short, so we take those away.")),
    B("999 minus 99 is 900. So there are 900 three-digit numbers altogether.",
      W("l1", "999 − 99 = 900")),
    B("Now walk along them. 100 is even, 101 is odd, 102 is even, 103 is odd. Even and odd take turns, all the way to 999.",
      LB("seq", "100, 101, 102, 103, … 998, 999"), UL("seq", "100"), UL("seq", "102"), UL("seq", "998")),
    B("The run starts on an even number, 100, and ends on an odd one, 999. So the 900 numbers pair up exactly, one even with one odd, and none left over."),
    B("So what share of the 900 numbers is even?",
      ask=CHOOSE(["all of them", "half of them", "a third of them"], 1,
                 "Even and odd take turns the whole way, and every even number has an odd partner. So exactly half of them are even.")),
    B("Half of 900 is 450. So there are 450 three-digit even numbers.",
      ANS("l2", "900 ÷ 2 = 450"), CIRC("l2", "450")),
    B("Check another way. The even ones go 100, 102, 104, and on up to 998. From 100 to 998 is a gap of 898.",
      LB("ev", "100, 102, 104, … 998"), W("l3", "998 − 100 = 898")),
    B("Each jump is 2, so that is 449 jumps. And 449 jumps join up 450 numbers, because the starting number counts too.",
      W("l4", "898 ÷ 2 = 449"), W("l5", "449 + 1 = 450")),
    B("So count the whole run first, then take half, because even and odd take turns. The trap is stopping at 900, which counts the odd ones too."),
)
