"""Batch 08 lessons written one at a time: formulas, fraction stories, two LCM stories, two odd ones out."""
from imported_08_lib import ANS, B, DIV, FIG, GIVEN, M, N, W, choose, lesson

LESSONS = {}
A = "AIGEN_grade5_"

# ── Formulas with a missing letter ───────────────────────────────────────────

LESSONS["IPMTB_grade5_ch09_q031"] = lesson(
    B("Here is a formula with three letters: a equals b divided by c. We know a is 3 and b is 18, and we want a plus c.",
      GIVEN("q", "a = b/c,   a = 3,   b = 18", True), W("want", "a + c = ?", label=True)),
    B("We cannot add yet, because c is still hiding. So first, put the numbers we know into the formula.",
      W("l1", "3 = 18/c", label=True)),
    B("3 equals 18 divided by c. So 18 has been split into equal parts, and each part is 3. How do we find c?",
      ask=choose(["18 − 3", "18 ÷ 3", "18 × 3"], 1,
                 "Ask how many 3s fit into 18. That is a division: 18 divided by 3.")),
    B("18 divided by 3 is 6. So c is 6.", W("l2", "18 ÷ 3 = 6"), W("l3", "c = 6", label=True), M("l3", "6", "box")),
    B("Careful: 6 is only c, not the answer. The question asks for a plus c.", M("want", "a + c")),
    B("a is 3 and c is 6. 3 plus 6 is 9.", ANS("ans", "3 + 6 = 9"), M("ans", "9", "circle")),
    B("Check c in the formula. 18 divided by 6 is 3, and a is 3. It fits.", W("chk", "18 ÷ 6 = 3")),
    B("So when a formula has a missing letter, put in what you know, find the missing one, and then answer what was really asked."),
)

LESSONS["IPMTB_grade5_ch09_q032"] = lesson(
    B("a equals b times c. We know a is 24 and c is one half. We need b minus a.",
      GIVEN("q", "a = b × c,   a = 24,   c = 1/2", True), W("want", "b − a = ?", label=True)),
    B("Put in what we know. 24 equals b times one half.", W("l1", "24 = b × 1/2", label=True)),
    B("b times one half means half of b. So half of b is 24. What is b?",
      ask=choose(["12", "24", "48"], 2,
                 "If half of b is 24, then b is two of those halves. 24 and 24 make 48. Halving 24 gives 12, but that goes the other way.")),
    B("Half of b is 24, so b is 24 times 2, which is 48.", W("l2", "24 × 2 = 48"), W("l3", "b = 48", label=True), M("l3", "48", "box")),
    B("Careful: the trap is to halve 24. But b times one half is 24, so b has to be bigger than 24, not smaller.",
      M("l1", "b × 1/2")),
    B("Now the question: b minus a. 48 minus 24 is 24.", ANS("ans", "48 − 24 = 24"), M("ans", "24", "circle", 2)),
    B("Check b in the formula. 48 times one half is 24, and a is 24. It works.", W("chk", "48 × 1/2 = 24")),
    B("Put in what you know, find the missing letter, and then do what the question asks with it."),
)

LESSONS["IPMTB_grade5_ch09_q033"] = lesson(
    B("L equals M times N. We know M is 13 and L is 78, and we must find N.",
      GIVEN("q", "L = M × N,   M = 13,   L = 78", True)),
    B("Put the numbers in place of their letters. 78 equals 13 times N.", W("l1", "78 = 13 × N", label=True)),
    B("13 times some number makes 78. What undoes times 13?",
      ask=choose(["subtract 13", "multiply by 13", "divide by 13"], 2,
                 "Times and divide are partners. To undo times 13, we divide by 13.")),
    B("So we divide both sides by 13. N is 78 divided by 13.", DIV("l1", "13"), W("l2", "N = 78 ÷ 13", label=True)),
    B("Count up in 13s. 13 times 5 is 65, and one more 13 makes 78. So 6 lots of 13 make 78.",
      W("l3", "13 × 5 = 65"), W("l4", "65 + 13 = 78")),
    B("So N is 6.", W("l5", "78 ÷ 13 = 6"), ANS("ans", "N = 6", True), M("ans", "6", "circle")),
    B("Careful not to add or multiply the 78 and the 13. N has to be small, because 13 times N is only 78."),
    B("Check: 13 times 6 is 78, and that matches L.", W("chk", "13 × 6 = 78")),
    B("When a formula says one number times another, you find a missing one by dividing."),
)

LESSONS["IPMTB_grade5_ch09_q034"] = lesson(
    B("169 times 1 over x equals 13. First we find x. Then the question wants 3 x.",
      GIVEN("q", "169 × (1/x) = 13", True), W("want", "3x = ?", label=True)),
    B("169 times 1 over x is the same as 169 divided by x. So 169 divided by x equals 13.",
      W("l1", "169 ÷ x = 13", label=True)),
    B("169 is split into x equal parts, and each part is 13. How do we find x?",
      ask=choose(["169 ÷ 13", "169 × 13", "169 − 13"], 0,
                 "Ask how many 13s fit into 169. That is 169 divided by 13.")),
    B("13 times 10 is 130, and 13 times 3 is 39. 130 plus 39 is 169, so 13 lots of 13 make 169.",
      W("l2", "13 × 10 = 130"), W("l3", "13 × 3 = 39"), W("l4", "130 + 39 = 169")),
    B("So x is 13.", W("l5", "169 ÷ 13 = 13"), W("l6", "x = 13", label=True), M("l6", "13", "box")),
    B("Careful: x is not the answer yet. The question wants 3 x, which means 3 times x.", M("want", "3x")),
    B("3 times 13 is 39.", ANS("ans", "3 × 13 = 39"), M("ans", "39", "circle")),
    B("Check x in the equation. 13 times 13 is 169, so 169 divided by 13 really is 13.", W("chk", "13 × 13 = 169")),
    B("Find the letter first. Then read the question again to see what it really wants."),
)

LESSONS["IPMTB_grade5_ch09_q035"] = lesson(
    B("625 over x equals 25 over 1. First we find x. Then the question wants 4 x.",
      GIVEN("q", "625/x = 25/1", True), W("want", "4x = ?", label=True)),
    B("25 over 1 is just 25. So 625 divided by x equals 25.", W("l0", "25/1 = 25"), W("l1", "625 ÷ x = 25", label=True)),
    B("625 is split into x equal parts, and each part is 25. How do we find x?",
      ask=choose(["625 × 25", "625 ÷ 25", "625 − 25"], 1,
                 "Ask how many 25s fit into 625. That is 625 divided by 25.")),
    B("25 times 20 is 500, and 25 times 5 is 125. 500 plus 125 is 625, so 25 lots of 25 make 625.",
      W("l2", "25 × 20 = 500"), W("l3", "25 × 5 = 125"), W("l4", "500 + 125 = 625")),
    B("So x is 25.", W("l5", "625 ÷ 25 = 25"), W("l6", "x = 25", label=True), M("l6", "25", "box")),
    B("Careful: x is not the answer yet. The question wants 4 x, which means 4 times x.", M("want", "4x")),
    B("4 times 25 is 100.", ANS("ans", "4 × 25 = 100"), M("ans", "100", "circle")),
    B("Check x in the equation. 25 times 25 is 625, so 625 divided by 25 really is 25.", W("chk", "25 × 25 = 625")),
    B("Find the letter first. Then read the question again to see what it really wants."),
)

# ── Fraction stories ─────────────────────────────────────────────────────────

LESSONS[A + "0799b640-0073-4a01-9861-29cced10698d"] = lesson(
    B("Priya gives away one third of her ladoos, then one quarter of what is left, then eats 5, and 25 remain. We must find how many she made.",
      GIVEN("q", "gave 1/3, then 1/4 of the rest, ate 5, left 25", True)),
    B("We know the end of the story, but not the start. So which way should we work?",
      ask=choose(["forwards from the start", "backwards from the 25", "add up all the numbers"], 1,
                 "We do not know the starting number, so we cannot go forwards. We do know the ending, 25, so we undo each step from there.")),
    B("Undo the last step first. She ate 5 and had 25 left, so before eating she had 25 plus 5, which is 30.",
      W("l1", "25 + 5 = 30"), M("l1", "30", "box")),
    B("Before that, she gave her cousins one quarter of the ladoos she had left. So the 30 is the other 3 quarters.",
      FIG("bar", {"kind": "barModel", "bars": [{"segments": [
          {"units": 1, "label": "cousins", "tone": "b"}, {"units": 3, "label": "30 left", "tone": "a"}],
          "brace": "after neighbours = ?"}]}),
      W("l2", "3 quarters = 30", label=True)),
    B("If 3 quarters are 30, what is 1 quarter?",
      ask=choose(["10", "27", "90"], 0,
                 "3 equal parts make 30, so one part is 30 divided by 3. That is 10.")),
    B("One quarter is 10, so all 4 quarters are 40. She had 40 ladoos after the neighbours took their share.",
      W("l3", "30 ÷ 3 = 10"), W("l4", "10 × 4 = 40"), M("l4", "40", "box")),
    B("Same idea again. The neighbours took one third, so the 40 is the other 2 thirds.",
      W("l5", "2 thirds = 40", label=True)),
    B("Half of 40 is 20, so one third is 20. And 3 thirds, the whole lot, is 60.",
      W("l6", "40 ÷ 2 = 20"), W("l7", "20 × 3 = 60")),
    B("Priya made 60 ladoos.", ANS("ans", "Ladoos at the start = 60", True), M("ans", "60", "circle")),
    B("Careful: the one quarter was a quarter of what was left, not of all 60. That is why we went one step at a time."),
    B("Check forwards. One third of 60 is 20, which leaves 40. One quarter of 40 is 10, which leaves 30.",
      W("c1", "60 − 20 = 40"), W("c2", "40 − 10 = 30")),
    B("And 30 take away the 5 she ate is 25. It matches the story.", W("c3", "30 − 5 = 25")),
    B("When you know the end but not the start, work backwards and undo one step at a time."),
)

LESSONS[A + "7029fb7b-b253-42b2-895f-0ba3a875389f"] = lesson(
    B("Ravi has 600 rupees. He spends one quarter on books, gives 2 fifths of the rest to his sister, then spends one third of what is left on sweets. How much does he still have?",
      GIVEN("q", "₹600: 1/4 books, 2/5 of rest, 1/3 of rest", True)),
    B("Start with the books. One quarter of 600 is 600 divided by 4, which is 150.", W("l1", "1/4 of 600 = 150")),
    B("So 600 minus 150 leaves 450 rupees.", W("l2", "600 − 150 = 450"), M("l2", "450", "box")),
    B("Next he gives 2 fifths to his sister. 2 fifths of which amount?",
      ask=choose(["of the 600 he started with", "of the 450 that is left", "of the 150 he spent"], 1,
                 "The question says from the remaining money. After the books, the remaining money is 450, so we take 2 fifths of 450.")),
    B("One fifth of 450 is 90, so 2 fifths is 180. His sister gets 180 rupees.",
      W("l3", "450 ÷ 5 = 90"), W("l4", "2/5 of 450 = 180")),
    B("450 minus 180 leaves 270 rupees.", W("l5", "450 − 180 = 270"), M("l5", "270", "box")),
    B("Last, the sweets. Again it is one third of what is left, so one third of 270. That is 90.", W("l6", "1/3 of 270 = 90")),
    B("270 minus 90 leaves 180 rupees. That is what Ravi still has.", ANS("ans", "270 − 90 = 180"), M("ans", "180", "circle")),
    B("Careful: 180 turned up twice. The first 180 went to his sister. The 180 at the end is what Ravi keeps."),
    B("Check by adding it all back. 150 plus 180 plus 90 went out, which is 420. And 420 plus the 180 he kept is 600.",
      W("c1", "150 + 180 + 90 = 420"), W("c2", "420 + 180 = 600")),
    B("When a question says of the remaining money, find what is left after each step before you take the next fraction."),
)

LESSONS[A + "bf07efef-d936-4bea-aca0-bd914e8044d0"] = lesson(
    B("Arjun spends 2 fifths of his money on balls, then 3 quarters of the rest on a bat, and has 90 rupees left. We want the total he collected.",
      GIVEN("q", "2/5 on balls, 3/4 of rest on bat, ₹90 left", True)),
    B("We know the end, so we work backwards. He spent 3 quarters of the remaining money on the bat. What fraction of it was left over?",
      ask=choose(["3/4", "1/5", "1/4"], 2,
                 "The whole is 4 quarters. Take away the 3 quarters spent on the bat, and 1 quarter is left.")),
    B("So the 90 rupees is one quarter of the money he had after the balls. All 4 quarters is 90 times 4, which is 360.",
      FIG("bar", {"kind": "barModel", "bars": [{"segments": [
          {"units": 3, "label": "bat", "tone": "b"}, {"units": 1, "label": "₹90", "tone": "a"}],
          "brace": "after the balls = ?"}]}),
      W("l1", "90 × 4 = 360"), M("l1", "360", "box")),
    B("Now the balls. He spent 2 fifths of the total on them. So the 360 is how many fifths of the total?",
      ask=choose(["2 fifths", "3 fifths", "5 fifths"], 1,
                 "The total is 5 fifths. 2 fifths went on balls, so 3 fifths were left, and that is the 360.")),
    B("3 fifths is 360, so 1 fifth is 360 divided by 3, which is 120.", W("l2", "3 fifths = 360", label=True), W("l3", "360 ÷ 3 = 120")),
    B("And the whole amount, 5 fifths, is 120 times 5. That is 600 rupees.",
      W("l4", "120 × 5 = 600"), ANS("ans", "Total collected = ₹600", True), M("ans", "₹600", "circle")),
    B("Careful: the 3 quarters came out of what was left after the balls, not out of the whole amount. That is why we undid the bat first."),
    B("Check forwards. 2 fifths of 600 is 240, which leaves 360. 3 quarters of 360 is 270, which leaves 90.",
      W("c1", "600 − 240 = 360"), W("c2", "360 − 270 = 90")),
    B("Know the end but not the start? Work backwards, one step at a time."),
)

# ── Two lowest-common-multiple stories ───────────────────────────────────────

LESSONS[A + "5ba10b20-1546-4183-a2c5-2d5847b4866d"] = lesson(
    B("Red packets come in bundles of 6, blue in bundles of 8 and yellow in bundles of 9. Meera wants the same number of each colour, and as few as possible.",
      GIVEN("q", "Bundles: red 6, blue 8, yellow 9. Same number of each", True)),
    B("She can only buy whole bundles. So her number must be in the 6 times table, the 8 times table and the 9 times table, and be the smallest that is. What are we looking for?",
      ask=choose(["the highest common factor", "the lowest common multiple", "6 + 8 + 9"], 1,
                 "Whole bundles can only make multiples. We want the smallest number that is a multiple of 6, 8 and 9: the lowest common multiple.")),
    B("Break each number into primes. 6 is 2 times 3. 8 is 2 times 2 times 2. 9 is 3 times 3.",
      W("f6", "6 = 2 × 3"), W("f8", "8 = 2 × 2 × 2"), W("f9", "9 = 3 × 3")),
    B("Our number must hold each of these inside it. 8 needs 2 three times over. 6 needs 2 only once. How many times must our number contain 2?",
      ask=choose(["once", "3 times", "4 times"], 1,
                 "The number must hold the whole of 8, and 8 is 2 times 2 times 2. Those three 2s cover the 6 as well, so 3 times is enough.")),
    B("So we take 2 times 2 times 2 from the 8. In the same way, we take 3 times 3 from the 9, and that covers the 3 in 6.",
      M("f8", "2 × 2 × 2"), M("f9", "3 × 3")),
    B("Multiply what we took. 2 times 2 times 2 is 8, and 3 times 3 is 9. 8 times 9 is 72.",
      W("l1", "2 × 2 × 2 × 3 × 3 = 72"), ANS("ans", "Packets of each colour = 72", True), M("ans", "72", "circle")),
    B("Careful: multiplying 6 times 8 times 9 also gives a common multiple, but a far bigger one than Meera needs."),
    B("Check. 72 divided by 6 is 12 bundles, 72 divided by 8 is 9 bundles, and 72 divided by 9 is 8 bundles. All whole bundles.",
      W("c1", "72 ÷ 6 = 12"), W("c2", "72 ÷ 8 = 9"), W("c3", "72 ÷ 9 = 8")),
    B("Same number of each from different bundle sizes means lowest common multiple. Take each prime the most times it appears in any one number."),
)

LESSONS[A + "6db9284a-f51e-4201-b3a8-4828153f6100"] = lesson(
    B("Rockets come in boxes of 48 and sparklers in boxes of 36. The family buys the same number of each, as few as possible, using only full boxes. Then we find the cost.",
      GIVEN("q", "Rockets: boxes of 48. Sparklers: boxes of 36.", True),
      W("q2", "Rocket ₹15 each, sparkler ₹8 each", label=True)),
    B("Full boxes of 48 give a multiple of 48. Full boxes of 36 give a multiple of 36. We want the same number of each, and the least. What do we need?",
      ask=choose(["the lowest common multiple", "the highest common factor", "48 + 36"], 0,
                 "Whole boxes can only make multiples. We want the smallest number that is a multiple of both 48 and 36: the lowest common multiple.")),
    B("Break each number into primes. 48 is 2 times 2 times 2 times 2 times 3.", W("f1", "48 = 2 × 2 × 2 × 2 × 3")),
    B("And 36 is 2 times 2 times 3 times 3.", W("f2", "36 = 2 × 2 × 3 × 3")),
    B("For the lowest common multiple, take each prime the most times it appears in one number. 2 appears 4 times in 48, and 3 appears twice in 36.",
      M("f1", "2 × 2 × 2 × 2"), M("f2", "3 × 3")),
    B("2 times 2 times 2 times 2 is 16, and 3 times 3 is 9. 16 times 9 is 144.",
      W("l1", "2 × 2 × 2 × 2 = 16"), W("l2", "16 × 9 = 144"), M("l2", "144", "box")),
    B("So they buy 144 rockets and 144 sparklers. That is 3 full boxes of rockets and 4 full boxes of sparklers.",
      W("l3", "48 × 3 = 144"), W("l4", "36 × 4 = 144")),
    B("Now the money. 144 times 10 is 1440. Half of that, 720, is 144 times 5. Together, 144 rockets at 15 rupees cost 2160.",
      W("l5", "144 × 10 = 1,440"), W("l6", "144 × 5 = 720"), W("l7", "1,440 + 720 = 2,160")),
    B("For the sparklers, times 8 is three doubles. Double 144 is 288, double again is 576, and once more is 1152.",
      W("l8", "144 × 2 = 288"), W("l9", "288 × 2 = 576"), W("l10", "576 × 2 = 1,152")),
    B("Careful: 2160 is only the rockets, and 1152 is only the sparklers. The question wants both together. 2160 plus 1152 is 3312 rupees.",
      ANS("ans", "2,160 + 1,152 = 3,312"), M("ans", "3,312", "circle")),
    B("Same number from two box sizes means lowest common multiple. Find that number first, and only then work out the cost."),
)

# ── Two stories where the highest common factor is not the last step ─────────

LESSONS[A + "d2d891ad-f5a3-456a-884a-6265abe8f31e"] = lesson(
    B("A long story! Groups of 108, 144 and 180 players are split into squads, and then Arjun buys jerseys in packs of 8. Let's read right to the end to see what is asked.",
      GIVEN("q", "Players: 108, 144, 180. Jerseys in packs of 8.", True)),
    B("The question asks for the number of jersey packs, so that every player gets a jersey. What do we need to know for that?",
      ask=choose(["the size of each squad", "how many players there are in all", "the number of squads"], 1,
                 "Every player needs one jersey, whichever squad they are in. So what matters is how many players there are altogether.")),
    B("Let's look at the squads anyway. The biggest squad size is the highest common factor, which is 36. 108 is 36 times 3, 144 is 36 times 4, and 180 is 36 times 5.",
      W("s1", "108 = 36 × 3"), W("s2", "144 = 36 × 4"), W("s3", "180 = 36 × 5")),
    B("That makes 3 plus 4 plus 5, which is 12 squads of 36. But sorting players into squads does not add or remove a single player.",
      W("s4", "3 + 4 + 5 = 12")),
    B("So count the players. 108 plus 144 is 252, and 252 plus 180 is 432.",
      W("l1", "108 + 144 = 252"), W("l2", "252 + 180 = 432"), M("l2", "432", "box")),
    B("432 players, and 8 jerseys in a pack. How do we find the number of packs?",
      ask=choose(["432 × 8", "432 ÷ 36", "432 ÷ 8"], 2,
                 "Each pack covers 8 players. So we ask how many 8s are in 432, and that is 432 divided by 8.")),
    B("8 times 50 is 400, and 8 times 4 is 32. So 432 divided by 8 is 54 packs, with no jerseys spare.",
      W("l3", "8 × 50 = 400"), W("l4", "8 × 4 = 32"), ANS("ans", "432 ÷ 8 = 54"), M("ans", "54", "circle")),
    B("Careful: 36 and 12 are tempting, but they are the squad size and the number of squads. The question asked for packs of jerseys."),
    B("Check. 54 packs of 8 is 432 jerseys, one for each player. And 12 squads of 36 is 432 players too.",
      W("c1", "54 × 8 = 432"), W("c2", "12 × 36 = 432")),
    B("In a long word problem, find the final question first. Then use the numbers that answer it."),
)

LESSONS[A + "d5d104e8-c935-41c0-aa93-28c87b65c8f4"] = lesson(
    B("Arjun has 180 coins and 240 notes for prize bags. Each bag gets 3 coins, 4 notes and 5 pencils. How many pencils does he need altogether?",
      GIVEN("q", "180 coins, 240 notes. Each bag: 3 coins, 4 notes, 5 pencils", True)),
    B("To count the pencils, we first need the number of bags. Which sum gives it?",
      ask=choose(["180 × 3", "180 ÷ 3", "180 + 240"], 1,
                 "180 coins are shared out 3 to a bag. So the number of bags is how many 3s are in 180: 180 divided by 3.")),
    B("180 divided by 3 is 60. So there are 60 bags.", W("l1", "180 ÷ 3 = 60"), M("l1", "60", "box")),
    B("Let's make sure with the notes. 240 divided by 4 is also 60. Good, the two agree.", W("l2", "240 ÷ 4 = 60")),
    B("Is 60 really the greatest possible number of bags? 180 is 60 times 3, and 240 is 60 times 4.",
      W("l3", "180 = 60 × 3"), W("l4", "240 = 60 × 4")),
    B("3 and 4 have no common factor bigger than 1, so no bigger number divides both. 60 is the highest common factor, just as the story says.",
      W("l5", "HCF of 180 and 240 = 60", label=True)),
    B("Now the pencils. 60 bags with 5 pencils in each is 60 times 5, which is 300.",
      ANS("ans", "60 × 5 = 300"), M("ans", "300", "circle")),
    B("Careful: 5 is the pencils in one bag, and 60 is the number of bags. The question wants the pencils for all the bags together."),
    B("Check. 300 pencils shared among 60 bags gives 5 each.", W("chk", "300 ÷ 60 = 5")),
    B("Find the number of groups first. Then multiply by how many each group gets."),
)
