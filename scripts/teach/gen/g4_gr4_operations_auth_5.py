"""Individually written lessons, Grade 4 operations: hand-written questions CH09 011-025, CH12, CH14, CH15, DH."""
from g4_gr4_operations_common import (B, W, GIVEN, ANS, ANSR, M, RING, FIG, choose, lesson, figures)


def _figure(qid):
    spec = (figures().get(qid) or {}).get("figure")
    return FIG("fig", spec) if spec else None


LESSONS = {}

LESSONS["Q_CH09_011"] = lesson(
    B("Four signs in one line: divide, times, minus and plus. Let us sort out the order.",
      GIVEN("q", "72 ÷ 8 × 3 − 6 + 4")),
    B("Which chunk is done first?",
      ask=choose(["72 ÷ 8 × 3", "3 − 6", "6 + 4"], 0,
                 "Divide and times go before minus and plus. So the first chunk, 72 divided by 8 times 3, is done first.")),
    B("Divide and times go first. Box that chunk.", M("q", "72 ÷ 8 × 3", "box")),
    B("Inside the box we go left to right. 72 divided by 8 is 9. Then 9 times 3 is 27.", W("a", "72 ÷ 8 = 9"), W("b", "9 × 3 = 27")),
    B("Now the sum is 27 minus 6 plus 4.", W("l2", "27 − 6 + 4")),
    B("27 is not the final answer. Two jobs are left. Which comes first?",
      ask=choose(["27 − 6", "6 + 4"], 0, "Plus and minus are equal partners, so we go left to right. 27 take away 6 comes first.")),
    B("27 take away 6 is 21. Then 21 plus 4 is 25.", W("l3", "27 − 6 = 21"), *ANSR("ans", "21 + 4 = 25", "25")),
    B("The trap is adding the 6 and the 4 together first. Only the 6 is taken away. The 4 is added."),
    B("So: divide and times from left to right, then minus and plus from left to right."),
)

LESSONS["Q_CH09_012"] = lesson(
    B("5 pens cost 35 rupees. We want the cost of 8 pens.",
      GIVEN("q", "5 pens cost 35 rupees.    8 pens cost ?", label=True), _figure("Q_CH09_012")),
    B("We cannot jump straight from 5 pens to 8 pens. What should we find first?",
      ask=choose(["the cost of 1 pen", "the cost of 3 pens", "35 plus 8"], 0,
                 "Once we know the cost of 1 pen, we can find the cost of any number of pens.")),
    B("Find the cost of one pen. Share 35 rupees among 5 pens. 35 divided by 5 is 7.", W("a", "35 ÷ 5 = 7")),
    B("So one pen costs 7 rupees.", W("a2", "1 pen costs 7 rupees", label=True), M("a2", "7", "circle")),
    B("Now 8 pens at 7 rupees each. Which sum do we need?",
      ask=choose(["8 × 7", "8 + 7", "35 + 8"], 0, "Each of the 8 pens costs 7 rupees. So we need 8 lots of 7.")),
    B("8 times 7 is 56. So 8 pens cost 56 rupees.", *ANSR("ans", "8 × 7 = 56", "56")),
    B("Does it make sense? 8 pens are more than 5 pens, so they should cost more than 35 rupees. And 56 is more. Good."),
    B("So: find the cost of one first, then multiply by how many you want."),
)

LESSONS["Q_CH09_013"] = lesson(
    B("Two sides with an equals sign between them. The brackets have moved, and one number has gone missing.",
      GIVEN("q", "(12 × 5) × 4 = 12 × (5 × ?)")),
    B("Look at the left side. It multiplies three numbers: 12, 5 and 4.",
      M("q", "12", "underline"), M("q", "5", "underline"), M("q", "4", "underline")),
    B("The right side must multiply the same three numbers. It already shows 12 and 5. Which one is missing?",
      ask=choose(["4", "60", "20"], 0, "The left side uses 12, 5 and 4. The right side shows 12 and 5. So the 4 is missing.")),
    B("The 4 is missing.", ANS("ans", "(12 × 5) × 4 = 12 × (5 × 4)"), RING("ans", "4", 2)),
    B("Let us check both sides. On the left, 12 times 5 is 60, and 60 times 4 is 240.", W("c0", "12 × 5 = 60"), W("c1", "60 × 4 = 240")),
    B("On the right, 5 times 4 is 20, and 12 times 20 is 240. The same!", W("c2", "5 × 4 = 20"), W("c3", "12 × 20 = 240")),
    B("So when you multiply three numbers, you can group them any way you like. The answer stays the same, and the missing number is 4."),
)

LESSONS["Q_CH09_014"] = lesson(
    B("This sum is meant to equal 36. Let us see what it gives now, and whether brackets can fix it.",
      GIVEN("q", "8 + 4 × 3 = 36", label=True)),
    B("With no brackets, times goes first. 4 times 3 is 12, and 8 plus 12 is 20. Not 36.", W("n", "8 + 4 × 3 = 8 + 12 = 20")),
    B("We need a bigger answer. Which job should we make happen first?",
      ask=choose(["8 + 4", "4 × 3"], 0, "4 times 3 already goes first, and that gave 20. So try making 8 plus 4 go first instead.")),
    B("Brackets make a job go first. Put them round 8 plus 4.", W("t", "(8 + 4) × 3"), M("t", "(8 + 4)", "box")),
    B("Brackets first. 8 plus 4 is 12.", W("t1", "12 × 3")),
    B("Then 12 times 3 is 36. That is our number!", W("t2", "12 × 3 = 36")),
    B("So the brackets go round 8 plus 4.", ANS("ans", "(8 + 4) × 3 = 36"), RING("ans", "(8 + 4)")),
    B("Brackets round 4 times 3 would change nothing, because times goes first anyway. Brackets only help when they change the order."),
)

LESSONS["Q_CH09_015"] = lesson(
    B("Two gaps, and each needs a sign. The answer must be 9. We test the choices.",
      GIVEN("q", "12 __ 4 __ 3 = 9", label=True)),
    B("Try plus then minus. 12 plus 4 is 16, and 16 take away 3 is 13. Not 9.", W("t1a", "12 + 4 = 16"), W("t1", "16 − 3 = 13")),
    B("Try times then minus. 12 times 4 is 48, and 48 take away 3 is 45. Far too big.", W("t2a", "12 × 4 = 48"), W("t2", "48 − 3 = 45")),
    B("Now try divide then times: 12 divided by 4 times 3. Which goes first?",
      W("t3", "12 ÷ 4 × 3"),
      ask=choose(["12 ÷ 4", "4 × 3"], 0,
                 "Divide and times are equal partners, so we go left to right. 12 divided by 4 comes first.")),
    B("Left to right. 12 divided by 4 is 3. Then 3 times 3 is 9. That is our number!", W("t3a", "12 ÷ 4 = 3"), W("t3b", "3 × 3 = 9")),
    B("So the signs are divide, then times.", ANS("ans", "12 ÷ 4 × 3 = 9"), RING("ans", "÷ 4 ×")),
    B("Careful with the trap. Doing 4 times 3 first would give 12 divided by 12, which is 1. With divide and times, go left to right."),
    B("So test each pair of signs, and always follow the order rules."),
)

LESSONS["Q_CH09_016"] = lesson(
    B("999 times 7 looks like hard work. But 999 has a very friendly neighbour.", GIVEN("q", "999 × 7 = ?")),
    B("Which round number is just 1 more than 999?",
      ask=choose(["1,000", "900", "990"], 0, "999 plus 1 is 1,000. And 1,000 is very easy to multiply.")),
    B("999 is 1 less than 1,000. So start with 1,000 lots of 7. That is 7,000.",
      W("a", "999 = 1,000 − 1"), W("b", "1,000 × 7 = 7,000")),
    B("But 1,000 lots is one lot too many. What do we take away?",
      ask=choose(["one 7", "just 1", "one 999"], 0, "We counted one extra lot of 7. So we take away 7, not 1.")),
    B("Take away one lot of 7. 7,000 take away 7 is 6,993.", W("c", "7,000 − 7 = 6,993")),
    B("So 999 times 7 is 6,993.", *ANSR("ans", "999 × 7 = 6,993", "6,993")),
    B("A quick check on the last digit. 9 times 7 is 63, which ends in 3. Our answer ends in 3 too.", W("d", "9 × 7 = 63")),
    B("So when a number is 1 less than a round number, use the round number, then take one lot away."),
)

LESSONS["Q_CH09_017"] = lesson(
    B("We divide 157 by 6 and want the remainder. That is what is left over after making as many groups of 6 as we can.",
      GIVEN("q", "157 ÷ 6  →  remainder ?", label=True)),
    B("Build up in sixes. 6 times 10 is 60, so 6 times 20 is 120.", W("a0", "6 × 10 = 60"), W("a", "6 × 20 = 120")),
    B("From 120 we still have 37 to go to reach 157.", W("b", "157 − 120 = 37")),
    B("How many sixes fit into 37?",
      ask=choose(["6", "7", "5"], 0, "Say the 6 times table. 6 sixes fit inside 37, but 7 sixes would be too many.")),
    B("6 times 6 is 36. So altogether 26 sixes fit, and they make 156.", W("c", "6 × 6 = 36"), W("d", "6 × 26 = 120 + 36 = 156")),
    B("157 take away 156 leaves 1. So the remainder is 1.", *ANSR("ans", "157 − 156 = 1", "1")),
    B("A remainder is always smaller than the number you divide by. 1 is smaller than 6, so that fits."),
    B("So to find a remainder, find the biggest multiple that fits, then subtract. Here the remainder is 1."),
)

LESSONS["Q_CH09_019"] = lesson(
    B("25 times 4. Here is a neat trick: multiplying by 4 is the same as doubling, and then doubling again.",
      GIVEN("q", "25 × 4 = ?")),
    B("Why does that work? Because 4 is 2 times 2.", W("a", "4 = 2 × 2")),
    B("So first, double 25. What is 25 plus 25?",
      ask=choose(["50", "45", "55"], 0, "2 tens doubled is 4 tens. 5 doubled is 10, which is one more ten. That makes 5 tens, and 5 tens is 50.")),
    B("Double 25 is 50.", W("b", "25 × 2 = 50")),
    B("Now double again. Double 50 is 100.", W("c", "50 × 2 = 100")),
    B("So 25 times 4 is 100.", *ANSR("ans", "25 × 4 = 100", "100")),
    B("This is a fact worth keeping in your head: four 25s make 100."),
    B("So to multiply by 4, double and double again."),
)

LESSONS["Q_CH09_020"] = lesson(
    B("Ria buys two kinds of things: notebooks and pens. We find the cost of each kind, then add.",
      GIVEN("q", "3 notebooks at 45 rupees.   2 pens at 12 rupees.", label=True), _figure("Q_CH09_020")),
    B("Start with the notebooks. 3 notebooks at 45 rupees each. Which sum?",
      ask=choose(["3 × 45", "3 + 45", "45 − 3"], 0, "Each of the 3 notebooks costs 45 rupees. So we need 3 lots of 45.")),
    B("3 times 45. 3 times 40 is 120, and 3 times 5 is 15. Together, 135 rupees.",
      W("a1", "3 × 40 = 120"), W("a2", "3 × 5 = 15"), W("a", "3 × 45 = 120 + 15 = 135")),
    B("Now the pens. 2 pens at 12 rupees each. 2 times 12 is 24 rupees.", W("b", "2 × 12 = 24")),
    B("We have 135 rupees for notebooks and 24 rupees for pens. What is the last step?",
      ask=choose(["add them", "take one from the other", "stop at 135"], 0,
                 "She paid for both the notebooks and the pens. So we add the two costs together.")),
    B("135 plus 24 is 159. Ria spent 159 rupees.", *ANSR("ans", "135 + 24 = 159", "159")),
    B("We can write the whole story on one line. Times first, then the plus.", W("all", "3 × 45 + 2 × 12 = 159")),
    B("So: work out each kind of thing on its own, then add the costs. The total is 159 rupees."),
)

LESSONS["Q_CH09_021"] = lesson(
    B("1,000 divided by 8. Dividing by 8 sounds hard, but halving is easy. And 8 is made of halvings.",
      GIVEN("q", "1,000 ÷ 8 = ?")),
    B("8 is 2 times 2 times 2. So dividing by 8 is the same as halving three times.", W("a", "8 = 2 × 2 × 2")),
    B("First halving. Half of 1,000 is 500.", W("h1", "1,000 ÷ 2 = 500")),
    B("Second halving. What is half of 500?",
      ask=choose(["250", "200", "300"], 0, "Half of 5 hundreds is 2 and a half hundreds. That is 250.")),
    B("Half of 500 is 250.", W("h2", "500 ÷ 2 = 250")),
    B("Third halving. Half of 250. Half of 200 is 100, and half of 50 is 25. Together, 125.",
      W("h3a", "200 ÷ 2 = 100"), W("h3b", "50 ÷ 2 = 25"), W("h3", "250 ÷ 2 = 125")),
    B("So 1,000 divided by 8 is 125.", *ANSR("ans", "1,000 ÷ 8 = 125", "125")),
    B("Check. 8 times 100 is 800, and 8 times 25 is 200. Together that is 1,000. It fits.",
      W("c1", "8 × 100 = 800"), W("c2", "8 × 25 = 200"), W("c", "800 + 200 = 1,000")),
    B("So to divide by 8, halve, halve, and halve again. The answer is 125."),
)

LESSONS["Q_CH09_022"] = lesson(
    B("This question is about a rule, not about one sum. What happens when any number is multiplied by 1?",
      GIVEN("q", "Any number × 1 = ?", label=True)),
    B("Let us try a few. Multiplying by 1 means one group. One group of 6 is just 6.", W("a", "6 × 1 = 6")),
    B("Try another. What is 9 times 1?",
      ask=choose(["9", "10", "1"], 0, "9 times 1 means one group of 9. One group of 9 is just 9.")),
    B("One group of 9 is 9. It works for bigger numbers too. One group of 45 is 45.", W("b", "9 × 1 = 9"), W("c", "45 × 1 = 45")),
    B("Look down the board. Each time, the answer is the very number we started with.",
      M("a", "6", "circle", 2), M("b", "9", "circle", 2), M("c", "45", "circle", 2)),
    B("So any number multiplied by 1 gives the same number.",
      ANS("ans", "Any number × 1 = the same number", label=True), RING("ans", "the same number")),
    B("Do not mix it up with adding 1, which makes a number one bigger. Multiplying by 1 changes nothing at all."),
)

LESSONS["Q_CH09_023"] = lesson(
    B("Another rule question. What happens when any number is multiplied by 0?",
      GIVEN("q", "Any number × 0 = ?", label=True)),
    B("Picture 4 plates with nothing on any of them. How many sweets altogether? None. So 4 times 0 is 0.", W("a", "4 × 0 = 0")),
    B("Try a bigger one. 100 plates, all empty. How many sweets?",
      ask=choose(["0", "100", "1"], 0, "Every plate is empty. However many empty plates you have, there are still no sweets at all.")),
    B("Still none. 100 times 0 is 0.", W("b", "100 × 0 = 0")),
    B("It never matters how big the number is. Lots of nothing is still nothing.",
      M("a", "0", "circle", 2), M("b", "0", "circle", 4)),
    B("So any number multiplied by 0 gives 0.", ANS("ans", "Any number × 0 = 0", label=True), RING("ans", "0", 2)),
    B("Do not mix it up with multiplying by 1, which gives the same number back. Multiplying by 0 always gives 0."),
)

LESSONS["Q_CH09_024"] = lesson(
    B("A chain of four instructions. We follow them one at a time, in order, and keep track on the board.",
      GIVEN("q", "Start 5  →  double  →  + 3  →  × 4  →  − 2", label=True)),
    B("Start with 5. Double it. 5 times 2 is 10.", W("a", "5 × 2 = 10")),
    B("Add 3. 10 plus 3 is 13.", W("b", "10 + 3 = 13")),
    B("Now multiply by 4. Which number do we multiply?",
      ask=choose(["13, our newest number", "3, the one just added", "5, the start"], 0,
                 "Each instruction works on the newest number in the chain. Right now that is 13.")),
    B("13 times 4. 10 times 4 is 40, and 3 times 4 is 12. Together, 52.",
      W("c1", "10 × 4 = 40"), W("c2", "3 × 4 = 12"), W("c", "13 × 4 = 40 + 12 = 52")),
    B("Is 52 the answer?",
      ask=choose(["Not yet: subtract 2", "Yes, 52"], 0, "There is one more instruction in the chain: subtract 2.")),
    B("Last step. 52 take away 2 is 50.", *ANSR("ans", "52 − 2 = 50", "50")),
    B("So in a chain like this, do every step in order, each on the newest number, and do not stop early."),
)

LESSONS["Q_CH09_025"] = lesson(
    B("7 times some number makes 91. We need to find that hidden number.",
      GIVEN("q", "7 × ? = 91"), _figure("Q_CH09_025")),
    B("Which sum finds the hidden number?",
      ask=choose(["91 ÷ 7", "91 − 7", "91 × 7"], 0, "7 equal groups make 91. To find the size of one group, we divide 91 by 7.")),
    B("Divide undoes times. So we need 91 divided by 7.", W("d", "91 ÷ 7 = ?")),
    B("Split 91 into two friendly pieces: 70 and 21. Both are in the 7 times table.", W("s", "91 = 70 + 21")),
    B("70 divided by 7 is 10. And 21 divided by 7 is 3.", W("s1", "70 ÷ 7 = 10"), W("s2", "21 ÷ 7 = 3")),
    B("10 and 3 make 13. So the hidden number is 13.", *ANSR("ans", "91 ÷ 7 = 13", "13")),
    B("Check by multiplying. 7 times 13 is 91. It fits.", W("c", "7 × 13 = 91")),
    B("So to find a missing number in a times sum, divide. Here it is 13."),
)

LESSONS["Q_CH12_025"] = lesson(
    B("A box has 3 gross of pencils, and 5 dozen are given away. The answer must be in pencils, so we change everything into pencils first.",
      GIVEN("q", "3 gross of pencils.   5 dozen given away.", label=True)),
    B("One gross is 12 dozen. And one dozen is 12. So how many pencils are in one gross?",
      W("g", "1 gross = 12 dozen", label=True),
      ask=choose(["144", "24", "120"], 0, "12 dozen means 12 lots of 12. And 12 times 12 is 144.")),
    B("12 times 12 is 144. So one gross is 144 pencils.", W("g1", "12 × 12 = 144")),
    B("3 gross is 3 times 144. 3 times 100 is 300, 3 times 40 is 120, and 3 times 4 is 12. Together, 432 pencils.",
      W("a1", "3 × 100 = 300"), W("a2", "3 × 40 = 120"), W("a3", "3 × 4 = 12"), W("a", "3 × 144 = 300 + 120 + 12 = 432")),
    B("Now the pencils given away. 5 dozen is 5 times 12, which is 60.", W("b", "5 × 12 = 60")),
    B("The box had 432 pencils, and 60 are given away. What now?",
      ask=choose(["432 − 60", "432 + 60", "stop at 432"], 0, "Given away means they leave the box. So take 60 away from 432.")),
    B("432 take away 60 is 372. So 372 pencils are left.", *ANSR("ans", "432 − 60 = 372", "372")),
    B("The trap is mixing units. Gross, dozen and pencils are different sizes, so change everything into pencils before you subtract."),
)

LESSONS["Q_CH14_024"] = lesson(
    B("72 chocolates are shared out, and each student gets 6. We want to know how many students there are.",
      GIVEN("q", "72 chocolates.  6 for each student.  Students = ?", label=True)),
    B("Each student takes a group of 6. So what are we counting?",
      ask=choose(["how many 6s are in 72", "72 and 6 more", "72 lots of 6"], 0,
                 "Every student takes away one group of 6. So we count how many groups of 6 there are in 72.")),
    B("Counting groups of 6 in 72 is a division. 72 divided by 6.", W("d", "72 ÷ 6 = ?")),
    B("Split 72 into 60 and 12. 60 is 10 groups of 6.", W("s", "72 = 60 + 12"), W("s1", "60 ÷ 6 = 10")),
    B("And 12 is 2 more groups of 6.", W("s2", "12 ÷ 6 = 2")),
    B("10 groups and 2 groups make 12 groups. So there are 12 students.", *ANSR("ans", "72 ÷ 6 = 12", "12")),
    B("Check by multiplying. 12 students with 6 chocolates each is 72 chocolates. It fits.", W("c", "12 × 6 = 72")),
    B("So when things are shared in equal groups, divide to find how many groups. Here, 12 students."),
)

LESSONS["Q_CH15_019"] = lesson(
    B("We are told two facts and asked for the next one: 14 times 14. We can simply work it out.",
      GIVEN("q", "12 × 12 = 144,  13 × 13 = 169,  14 × 14 = ?", label=True)),
    B("Split one of the 14s into 10 and 4.", W("s", "14 = 10 + 4")),
    B("First piece. What is 14 times 10?",
      ask=choose(["140", "24", "1400"], 0, "14 tens is 140. Multiplying by 10 puts a 0 on the end.")),
    B("14 times 10 is 140. Now 14 times 4: 10 times 4 is 40, and 4 times 4 is 16, so 56.",
      W("a", "14 × 10 = 140"), W("b1", "10 × 4 = 40"), W("b2", "4 × 4 = 16"), W("b", "14 × 4 = 40 + 16 = 56")),
    B("Add the two pieces. 140 plus 56 is 196.", *ANSR("ans", "14 × 14 = 140 + 56 = 196", "196")),
    B("Now look at the pattern in the question. From 144 to 169 is a jump of 25.", W("p1", "169 − 144 = 25")),
    B("From 169 to 196 is a jump of 27. The jump grew by 2.", W("p2", "196 − 169 = 27")),
    B("So the trap is adding 25 again. The jump gets 2 bigger each time. The answer is 196."),
)

LESSONS["Q_DH_017"] = lesson(
    B("A car goes 240 kilometres in 4 hours. Average speed means: how far does it go in one hour, if every hour is the same?",
      GIVEN("q", "240 km in 4 hours.    Speed = ?", label=True)),
    B("So we share the 240 kilometres equally among the 4 hours. Which sum is that?",
      ask=choose(["240 ÷ 4", "240 × 4", "240 + 4"], 0, "Sharing equally means dividing. So we need 240 divided by 4.")),
    B("Speed is distance divided by time.", W("f", "Speed = distance ÷ time", label=True), W("d", "240 ÷ 4 = ?")),
    B("24 divided by 4 is 6. So 240 divided by 4 is 60.", W("a", "24 ÷ 4 = 6"), W("b", "240 ÷ 4 = 60")),
    B("So the car goes 60 kilometres in each hour. Its average speed is 60 kilometres an hour.",
      ANS("ans", "Speed = 60 km/h", label=True), RING("ans", "60")),
    B("Check. 4 hours at 60 kilometres each hour makes 240 kilometres. It fits.", W("c", "60 × 4 = 240")),
    B("So to find speed, divide the distance by the time."),
)
