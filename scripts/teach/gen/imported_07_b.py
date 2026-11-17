"""Imported batch 07, part b: cricket bat, two innings, ribbon rolls, piggy bank, combined scores, sweets on both sides."""
from imported_07_lib import ANS, B, BOTH, E, G, GIVEN, M, N, S, W, choose, lesson, tail

P = "AIGEN_grade5_"
LESSONS = {}

# ── Saving for a bat: 45d + 140 = 500 ────────────────────────────────────────
qid = P + "b60243e7-d1d1-437e-96c5-bd53eb6da489"
LESSONS[qid] = lesson(
    B("Arjun wants a cricket bat that costs 500 rupees. He already has 140 rupees, and he earns 45 rupees a day. We need the equation for d days, and then d.",
      GIVEN("q", "Bat ₹500. Has ₹140. Earns ₹45 a day for d days.", True)),
    B("In d days he earns 45 times d. How does the 140 he already has fit in?",
      ask=choose(["45d − 140 = 500", "45d + 140 = 500", "45d = 500"], 1,
                 "The 140 rupees is his money too, so it counts towards the bat. His earnings and his 140 together must reach 500.")),
    B("Earnings of 45 d, plus the 140 he has, equals 500. Careful: leave out the 140 and he would work more days than he needs to.",
      W("e", "45d + 140 = 500"), N("e", "45d", "earned"), N("e", "140", "already has")),
    tail(qid, "d", 45, 140, 500, "e", found="Arjun needs to work for 8 days."),
    B("Check. 8 days at 45 rupees is 360 rupees. Add his 140 and we get 500, exactly the price of the bat.",
      W("c", "45 × 8 + 140 = 500")),
    B("So the choice we want is 45 d plus 140 equals 500, with d equal to 8. Write the equation, then solve it yourself instead of trusting the number printed beside it."),
    check=("d", 8))

# ── Two innings: x + 3x − 14 = 258 ───────────────────────────────────────────
qid = P + "b980072b-b3d1-4520-8146-bfff48779485"
LESSONS[qid] = lesson(
    B("Team India bats twice. The second innings is 3 times the first, minus 14. The two innings together make 258 runs, and x stands for the first innings.",
      GIVEN("q", "1st: x.   2nd: 3 times x, minus 14.   Total 258.", True)),
    B("The second innings is 3 x minus 14. Which equation gives the total of both innings?",
      ask=choose(["3x − 14 = 258", "x + 3x + 14 = 258", "x + 3x − 14 = 258"], 2,
                 "The total is both innings added: the first, x, and the second, 3 x minus 14. Leave out the x and you have only counted the second innings.")),
    B("First innings x, plus second innings 3 x minus 14, equals 258.",
      W("e", "x + 3x − 14 = 258"), N("e", "x", "1st"), N("e", "3x − 14", "2nd")),
    B("x and 3 x are like terms. 1 x and 3 x make 4 x.",
      G("e", ["x", "3x"], "4x"), W("e2", "4x − 14 = 258")),
    tail(qid, "x", 4, 14, 258, "e2", form="ax-b", found="The first innings was 68 runs."),
    B("Check. The second innings is 3 times 68, minus 14, which is 190. And 68 plus 190 is 258. It works.",
      W("c1", "3 × 68 − 14 = 190"), W("c2", "68 + 190 = 258")),
    B("So the choice we want is x plus 3 x minus 14 equals 258, with a first innings of 68 runs."),
    check=("x", 68))

# ── Ribbon rolls: 5r + 18 = 83, then 8 rolls ─────────────────────────────────
qid = P + "bbf0deaa-89fc-4839-ae35-857e83fc04d3"
vv = ("r", 13)
LESSONS[qid] = lesson(
    B("Meera buys 5 ribbon rolls and spends 18 rupees on glitter. Her bill is 83 rupees. Then she needs 3 more rolls, and we want her new bill.",
      GIVEN("q", "5 rolls + ₹18 glitter = ₹83.   3 more rolls: new bill?", True)),
    B("We cannot find the new bill straight away. What do we need to know first?",
      ask=choose(["the price of one ribbon roll", "nothing: just add 3 to 83", "how many glitter packets"], 0,
                 "Each extra roll costs the price of one roll, not 1 rupee. So first we must find that price from the first bill.")),
    B("Call the price of one roll r. Then 5 rolls cost 5 r. Add 18 for the glitter and we get the first bill, 83.",
      E("e", "5r + 18 = 83", *vv), N("e", "5r", "rolls"), N("e", "18", "glitter")),
    tail(qid, "r", 5, 18, 83, "e", vv=vv, asks=(), final=False, found="One ribbon roll costs 13 rupees."),
    B("Now she has 5 rolls and 3 more, which is 8 rolls. Which sum gives the new bill?",
      W("n", "5 + 3 = 8"),
      ask=choose(["8 × 13", "8 × 13 + 18", "83 + 3"], 1,
                 "8 rolls at 13 rupees is only the ribbon. The glitter is still on the bill, so we add the 18 as well.")),
    B("8 rolls at 13 rupees is 104 rupees. Add 18 for the glitter, and the new bill is 122 rupees.",
      W("m", "8 × 13 = 104"), ANS("a", "104 + 18 = 122"), M("a", "122", "circle")),
    B("Here is another way to check. The 3 extra rolls cost 3 times 13, which is 39. And the old bill of 83, plus 39, is 122 as well.",
      W("c1", "3 × 13 = 39"), W("c2", "83 + 39 = 122")),
    B("So when a price is hidden, find it first from what you know. Then use it for the new question. And don't drop the glitter!"),
)

# ── Piggy bank: 3w + 9 = 30 ──────────────────────────────────────────────────
qid = P + "be0f75bf-b9b7-4ff1-95fc-cad010472f07"
LESSONS[qid] = lesson(
    B("Priya has 9 rupees in her piggy bank and adds 3 rupees every week. After w weeks she has 30 rupees. We need the equation, and the number of weeks.",
      GIVEN("q", "₹9 saved, ₹3 each week, ₹30 after w weeks", True)),
    B("One of these numbers has to be multiplied by w. Which one?",
      ask=choose(["the 9", "the 3", "the 30"], 1,
                 "The 3 rupees goes in every single week, so after w weeks that is 3 times w. The 9 rupees was only there once, at the start.")),
    B("So she adds 3 w over the weeks. With the 9 she began with, that makes 30. Careful not to swap them: 9 w plus 3 would mean 9 rupees every week.",
      W("e", "3w + 9 = 30"), N("e", "3w", "weekly"), N("e", "9", "at the start")),
    tail(qid, "w", 3, 9, 30, "e", found="It took Priya 7 weeks."),
    B("Check. 7 weeks at 3 rupees is 21 rupees. Add the 9 and we get 30. It works.",
      W("c", "3 × 7 + 9 = 30")),
    B("So the choice we want is 3 w plus 9 equals 30, with w equal to 7 weeks."),
    check=("w", 7))

# ── Two scores added: (3x + 7) + (5x − 3) = 84 ───────────────────────────────
qid = P + "c49393ce-30d1-4539-909e-8ebb3be06eee"
LESSONS[qid] = lesson(
    B("Virat's score is 3 x plus 7, and Rohit's is 5 x minus 3. Together they score 84 runs. We want x.",
      GIVEN("q", "(3x + 7) + (5x − 3) = 84")),
    B("Combined means added. So let's gather like terms: the x terms together, and the plain numbers together. First, 3 x and 5 x make 8 x.",
      G("q", ["3x", "5x"], "8x")),
    B("Now the plain numbers: plus 7 and minus 3. What do they make together?",
      ask=choose(["+ 10", "+ 4", "− 4"], 1,
                 "Start with 7 and take 3 away. That leaves 4. The minus sign belongs to the 3, so the 3 is taken off, not added.")),
    B("So the equation becomes 8 x plus 4 equals 84.",
      G("q", ["+ 7", "− 3"], "+ 4"), W("e2", "8x + 4 = 84")),
    tail(qid, "x", 8, 4, 84, "e2", asks=("div",)),
    B("Check. Virat: 3 times 10, plus 7, is 37. Rohit: 5 times 10, minus 3, is 47. And 37 plus 47 is 84.",
      W("c1", "3 × 10 + 7 = 37"), W("c2", "5 × 10 − 3 = 47"), W("c3", "37 + 47 = 84")),
    B("So: add the expressions, gather the x terms and the plain numbers, then solve as usual."),
    check=("x", 10))

# ── Samosas at a match: 8x + 10 = 50 ─────────────────────────────────────────
qid = P + "c67c78d2-2a91-484a-9ed0-0b00b5eca4cf"
LESSONS[qid] = lesson(
    B("Arjun sells samosas at x rupees each: 3 in the first innings and 5 in the second. A happy customer tips him 10 rupees, and he earns 50 rupees in all.",
      GIVEN("q", "3 + 5 samosas at ₹x each, tip ₹10, total ₹50", True)),
    B("He sold 3 and then 5, so 8 samosas, each bringing in x rupees. Which equation matches his earnings?",
      W("n", "3 + 5 = 8"),
      ask=choose(["8x + 10 = 50", "8x − 10 = 50", "8 + 10x = 50"], 0,
                 "8 samosas at x rupees is 8 x. The tip is extra money on top, so it is added. 8 x plus 10 makes 50.")),
    B("8 x from the samosas, plus the tip of 10, equals 50.",
      W("e", "8x + 10 = 50"), N("e", "8x", "samosas"), N("e", "10", "tip")),
    tail(qid, "x", 8, 10, 50, "e", found="One samosa costs 5 rupees."),
    B("Check. 8 samosas at 5 rupees is 40 rupees, and the tip makes 50. It works.",
      W("c", "8 × 5 + 10 = 50")),
    B("The tip did not come from samosas. So we take it off first, and then share the rest among the 8 samosas."),
    check=("x", 5))

# ── Sweets and fireworks: 5x + 45 = 3x + 129 ─────────────────────────────────
qid = P + "ca68545b-06d3-4ef6-b3fb-9ba7b21b2677"
LESSONS[qid] = lesson(
    B("Ravi buys 5 boxes of sweets and pays 45 rupees for decorations. Meena buys 3 of the same boxes and pays 129 rupees for fireworks. They spend exactly the same. What does one box cost?",
      GIVEN("q", "Ravi: 5 boxes + ₹45.   Meena: 3 boxes + ₹129.   Equal.", True)),
    B("Each box costs x rupees. So Ravi spends 5 x plus 45, and Meena spends 3 x plus 129. Equal spending means the two are equal.",
      W("e", "5x + 45 = 3x + 129"), N("e", "5x + 45", "Ravi"), N("e", "3x + 129", "Meena")),
    B("Now x is on both sides. Which move collects the x terms on one side?",
      ask=choose(["take 3x from both sides", "take 5x from the left only", "add 3x to both sides"], 0,
                 "Take the smaller lot of x, which is 3 x, from both sides. The right side then has no x at all, and the balance stays level.")),
    B("Take 3 x from both sides. On the left, 5 x minus 3 x is 2 x. The right is just 129.",
      S("e", "3x", "− 3x"), BOTH("e", "− 3x"), W("e2", "2x + 45 = 129")),
    B("That line tells a little story of its own. Ravi's 2 extra boxes, plus his 45, match Meena's 129. Careful not to add the 45 and the 129: they sit on opposite sides.",
      M("e2", "2x")),
    tail(qid, "x", 2, 45, 129, "e2", found="One box of sweets costs 42 rupees."),
    B("Check both. Ravi: 5 times 42, plus 45, is 255. Meena: 3 times 42, plus 129, is 255. The same! It works.",
      W("c1", "5 × 42 + 45 = 255"), W("c2", "3 × 42 + 129 = 255")),
    B("When the letter is on both sides, take the smaller lot from both sides first. Then it is a two step equation."),
    check=("x", 42))

# ── A gift for each: (x + 15) + (3x + 15) = 142 ──────────────────────────────
qid = P + "cd74c938-5bf2-4971-b21f-3e70affa1a03"
LESSONS[qid] = lesson(
    B("Riya has some rupees saved, and Arjun has exactly 3 times as much. Their mother gives each of them 15 rupees. Now they have 142 rupees together. What did Riya have at first?",
      GIVEN("q", "Riya x, Arjun 3 times x, ₹15 each, total ₹142", True)),
    B("Call Riya's savings x. Then Arjun's are 3 x. After the gift, Riya has x plus 15, and Arjun has 3 x plus 15.",
      W("r", "Riya: x + 15", label=True), W("a", "Arjun: 3x + 15", label=True)),
    B("Together that is 142.",
      W("e", "(x + 15) + (3x + 15) = 142")),
    B("Gather the like terms. x and 3 x make 4 x. And how much gift money is there altogether?",
      G("e", ["x", "3x"], "4x"),
      ask=choose(["15", "30", "45"], 1, "Each of them gets 15 rupees, and there are 2 children. 15 and 15 make 30.")),
    B("Careful: the gift comes twice, once for each child. So the equation is 4 x plus 30 equals 142.",
      G("e", ["15", ("15", 2)], "30"), W("e2", "4x + 30 = 142")),
    tail(qid, "x", 4, 30, 142, "e2", found="Riya had 28 rupees at first."),
    B("Check. Arjun had 3 times 28, which is 84. After the gifts they have 43 and 99, and 43 plus 99 is 142.",
      W("c1", "3 × 28 = 84"), W("c2", "28 + 15 = 43"), W("c3", "84 + 15 = 99"), W("c4", "43 + 99 = 142")),
    B("So: write each person's money with the same letter, add, gather like terms, and undo one step at a time."),
    check=("x", 28))

# ── Drinks and samosas: 7x + 18 = 60 ─────────────────────────────────────────
qid = P + "cec9f5f0-a04f-4f74-8363-b4a5fcdde87d"
LESSONS[qid] = lesson(
    B("Meera spends 18 rupees on drinks, then buys packets of samosas at 7 rupees each. Altogether she spends 60 rupees. How many packets did she buy?",
      GIVEN("q", "₹18 on drinks, ₹7 a packet, ₹60 in all", True)),
    B("Before any algebra, think about the money. How much of the 60 rupees went on samosas?",
      ask=choose(["60 + 18", "60 ÷ 7", "60 − 18"], 2,
                 "The 60 rupees covers drinks and samosas. Take away the 18 for drinks, and what is left paid for the samosas.")),
    B("Now let's write that same idea as an equation. x packets at 7 rupees is 7 x. With the drinks, 7 x plus 18 equals 60.",
      W("e", "7x + 18 = 60"), N("e", "7x", "samosas"), N("e", "18", "drinks")),
    tail(qid, "x", 7, 18, 60, "e", asks=("div",), found="Meera bought 6 packets."),
    B("Check. 6 packets at 7 rupees is 42 rupees. Add 18 for the drinks, and we get 60. It works.",
      W("c", "6 × 7 + 18 = 60")),
    B("Taking away the drinks money, and taking 18 from both sides, are the same idea. An equation just writes your thinking down."),
    check=("x", 6))

# ── Chai and biscuits: 5x + 4 × 3 = 47 ───────────────────────────────────────
qid = P + "cf751092-e4cd-4d31-8966-e57fae114164"
LESSONS[qid] = lesson(
    B("Priya sells chai at x rupees a cup and biscuit packets at 3 rupees each. She sells 5 cups and 4 packets, and earns 47 rupees.",
      GIVEN("q", "5 cups at ₹x, 4 packets at ₹3, total ₹47", True)),
    B("The chai brings in 5 x. The biscuits bring in 4 times 3 rupees. Together they make 47.",
      W("e", "5x + 4 × 3 = 47"), N("e", "5x", "chai"), N("e", "4 × 3", "biscuits")),
    B("We can work out the biscuit money straight away. How much is it?",
      ask=choose(["7 rupees", "12 rupees", "43 rupees"], 1,
                 "4 packets at 3 rupees each means 4 times 3, which is 12 rupees. We multiply, because every packet costs 3.")),
    B("So the equation is 5 x plus 12 equals 47.",
      S("e", "4 × 3", "12"), W("e2", "5x + 12 = 47")),
    tail(qid, "x", 5, 12, 47, "e2", found="One cup of chai costs 7 rupees."),
    B("Check. 5 cups at 7 rupees is 35 rupees, and the biscuits add 12. 35 plus 12 is 47. It works.",
      W("c", "5 × 7 + 12 = 47")),
    B("Work out anything you can first, like the biscuit money. Then the equation is a simple two step one."),
    check=("x", 7))

# ── Saving each week: 8w + 17 = 73 ───────────────────────────────────────────
qid = P + "cfb4178b-7b44-4ae4-8a6e-22d74100cce9"
LESSONS[qid] = lesson(
    B("Ravi has 17 rupees saved and earns 8 rupees each week. After w weeks he has exactly 73 rupees. We need the equation, and then w.",
      GIVEN("q", "₹17 saved, ₹8 each week, ₹73 after w weeks", True)),
    B("Which equation matches Ravi's savings?",
      ask=choose(["8w − 17 = 73", "17w + 8 = 73", "8w + 17 = 73"], 2,
                 "He earns 8 rupees every week, so the 8 goes with w. The 17 he already had is added on top. Together they make 73.")),
    B("8 w from the weeks, plus the 17 he started with, equals 73.",
      W("e", "8w + 17 = 73"), N("e", "8w", "earned"), N("e", "17", "at the start")),
    tail(qid, "w", 8, 17, 73, "e", asks=("div",), found="Ravi worked for 7 weeks."),
    B("Check. 7 weeks at 8 rupees is 56 rupees, and 17 more makes 73. It works.",
      W("c", "8 × 7 + 17 = 73")),
    B("So the choice we want is 8 w plus 17 equals 73, with w equal to 7. Two choices share that equation, so only solving it tells them apart."),
    check=("w", 7))

# ── Jerseys and stumps: 8x + 19 = 91 ─────────────────────────────────────────
qid = P + "d104bda8-5feb-498f-a56d-b42fee37bc1f"
LESSONS[qid] = lesson(
    B("Coach Sharma buys jerseys at 8 rupees each, and a set of stumps for 19 rupees. The bill is 91 rupees. How many jerseys did he buy?",
      GIVEN("q", "₹8 a jersey, ₹19 for stumps, bill ₹91", True)),
    B("Let x be the number of jerseys. They cost 8 times x rupees. Add the stumps, and we have the whole bill.",
      W("e", "8x + 19 = 91"), N("e", "8x", "jerseys"), N("e", "19", "stumps")),
    tail(qid, "x", 8, 19, 91, "e", asks=("clear", "div"), found="The coach bought 9 jerseys."),
    B("Check. 9 jerseys at 8 rupees is 72 rupees. Add the stumps at 19, and the bill is 91. It works.",
      W("c", "9 × 8 + 19 = 91")),
    B("The stumps are bought once, so their cost comes off first. Then the rest is shared out at 8 rupees a jersey."),
    check=("x", 9))
