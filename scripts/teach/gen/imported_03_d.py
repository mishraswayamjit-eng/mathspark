"""Hand-written lessons: six order-of-operations (BODMAS) story sums."""
from imported_03_lib import ANS, ANSR, B, GIVEN, M, N, RING, W, WN, choose, lesson

LESSONS = {}
P = "AIGEN_grade5_"

# ── 30 − 2 × 6 + 3 × 4 ───────────────────────────────────────────────────────
E1 = "30 − 2 × 6 + 3 × 4"
LESSONS[P + "095d2be2-8a79-49d5-9077-143409859d27"] = lesson(
    B("Meera starts with 30 packets. She gives away 2 groups of 6, and gets 3 groups of 4. Here is the whole story as one sum.",
      GIVEN("q1", E1, False)),
    B("There is a minus, a plus and two times signs. What do we do first?",
      ask=choose(["30 − 2", "the two multiplications", "6 + 3"], 1,
                 "BODMAS puts multiplication before adding and subtracting. So the two times sums go first, wherever they sit in the line.")),
    B("2 times 6 is 12. Those are the packets she gives away.",
      M("q1", "2 × 6"), N("q1", "2 × 6", "12", "below")),
    B("3 times 4 is also 12. Those are the packets she gets from her teacher.",
      M("q1", "3 × 4"), N("q1", "3 × 4", "12", "below")),
    B("Now the line is much simpler: 30 minus 12 plus 12.",
      W("a", "30 − 12 + 12")),
    B("Only a minus and a plus are left. Which way do we go?",
      ask=choose(["left to right", "the plus first", "right to left"], 0,
                 "Plus and minus are equal partners, so neither one jumps the queue. We simply work from left to right.")),
    B("30 minus 12 is 18. Then 18 plus 12 is 30. Meera has 30 packets.",
      W("b", "30 − 12 = 18"), W("c", "18 + 12 = 30"), ANSR("d", E1 + " = 30", "30")),
    B("The trap is starting from the left with 30 minus 2, before the times sums are done. That mixes up loose packets with groups of packets."),
    B("It makes sense in the story too. She gave away 12 and got 12 back, so she still has her 30."),
    B("So: multiplications first, then plus and minus from left to right."),
)

# ── (3 × 12 + 8) ÷ 4 + 5 ─────────────────────────────────────────────────────
E2 = "(3 × 12 + 8) ÷ 4 + 5"
LESSONS[P + "0abdbafc-1973-41a8-acbd-7f83d8122ddf"] = lesson(
    B("Riya buys 3 boxes of 12 diyas, gets 8 more, shares them into 4 rows, and adds 5 to each row. This sum tells the whole story.",
      GIVEN("q1", E2, False)),
    B("Where do we start?",
      ask=choose(["the brackets", "the ÷ 4", "the + 5"], 0,
                 "The B in BODMAS comes first, and B is for brackets. We finish everything inside them before we touch the rest.")),
    B("Inside the brackets there is a times and a plus. The times goes first: 3 times 12 is 36.",
      M("q1", "3 × 12"), N("q1", "3 × 12", "36", "below")),
    B("Then add the 8. 36 plus 8 is 44, and that is all of Riya's diyas.",
      WN("a", "36 + 8 = 44", "44", "all the diyas")),
    B("The brackets are done, so the sum is now 44 divided by 4, plus 5. What comes next?",
      W("b", "44 ÷ 4 + 5"),
      ask=choose(["4 + 5 first", "44 ÷ 4 first"], 1,
                 "Division comes before addition. So we share the 44 into 4 rows first, and add the 5 afterwards.")),
    B("44 divided by 4 is 11. That is 11 diyas in each row.",
      WN("c", "44 ÷ 4 = 11", "11", "in each row")),
    B("Then 5 more go into each row. 11 plus 5 is 16.",
      ANSR("d", "11 + 5 = 16", "16")),
    B("Here is the trap. Add the 4 and the 5 first, and you would be sharing 44 diyas among 9 rows. The story has only 4 rows."),
    B("So: brackets first, then divide and multiply, then add and subtract."),
)

# ── 60 ÷ (2 + 3) × 4 − 8 + 5 ─────────────────────────────────────────────────
E3 = "60 ÷ (2 + 3) × 4 − 8 + 5"
LESSONS[P + "116040d3-d979-4293-a092-9018abc373f1"] = lesson(
    B("Priya's sum has every kind of sign in it, and brackets too. The order we work in decides the answer.",
      GIVEN("q1", E3, False)),
    B("Brackets first, always. 2 plus 3 is 5.",
      M("q1", "(2 + 3)", "box"), N("q1", "(2 + 3)", "5", "below"), W("a", "60 ÷ 5 × 4 − 8 + 5")),
    B("Now there is a divide and a times, side by side. Which one goes first?",
      ask=choose(["the ×, so 5 × 4", "the ÷, so 60 ÷ 5", "it does not matter"], 1,
                 "Divide and multiply are equal partners, so we take them from left to right. The divide is on the left, so it goes first.")),
    B("60 divided by 5 is 12. Then 12 times 4 is 48.",
      W("b", "60 ÷ 5 = 12"), W("c", "12 × 4 = 48")),
    B("Careful here. If you multiplied the 5 by the 4 first, the 60 would be divided by a much bigger number, and the whole answer would change."),
    B("What is left is 48 minus 8 plus 5.",
      W("d", "48 − 8 + 5")),
    B("A minus and a plus now. Which one first?",
      ask=choose(["8 + 5 first", "48 − 8 first"], 1,
                 "Plus and minus are equal partners too. So it is left to right again, and the minus is on the left.")),
    B("48 minus 8 is 40, and 40 plus 5 is 45. Priya needs 45 packets.",
      W("e", "48 − 8 = 40"), ANSR("g", "40 + 5 = 45", "45")),
    B("So: brackets first. Then divide and multiply, left to right. Then add and subtract, left to right."),
)

# ── 48 ÷ (4 + 2) × 3 − 5 ─────────────────────────────────────────────────────
E4 = "48 ÷ (4 + 2) × 3 − 5"
LESSONS[P + "144fb76b-3e40-448b-8de5-3798287ec4d9"] = lesson(
    B("Here is the coach's formula for Rohit's score. It has brackets, a divide, a times and a minus.",
      GIVEN("q1", E4, False)),
    B("What is the very first job?",
      ask=choose(["48 ÷ 4", "4 + 2", "3 − 5"], 1,
                 "The brackets are like a fence round 4 plus 2. Whatever is inside the fence gets done before anything else.")),
    B("4 plus 2 is 6. So now we have 48 divided by 6, times 3, minus 5.",
      M("q1", "(4 + 2)", "box"), N("q1", "(4 + 2)", "6", "below"), W("a", "48 ÷ 6 × 3 − 5")),
    B("That was the trap. The 4 sits right next to the divide sign, so it is tempting to do 48 divided by 4. But the bracket has to be finished first."),
    B("Next there is a divide, a times and a minus. Which one now?",
      ask=choose(["48 ÷ 6", "6 × 3", "3 − 5"], 0,
                 "The minus waits till last. Divide and times are equal partners, so we take whichever comes first from the left, and that is the divide.")),
    B("48 divided by 6 is 8. Then 8 times 3 is 24.",
      W("b", "48 ÷ 6 = 8"), W("c", "8 × 3 = 24")),
    B("Last of all, the minus. 24 minus 5 is 19, so Rohit's score is 19.",
      ANSR("d", "24 − 5 = 19", "19")),
    B("So: brackets, then divide and multiply from left to right, and the minus right at the end."),
)

# ── 100 − 5 × 12 − 8 ─────────────────────────────────────────────────────────
E5 = "100 − 5 × 12 − 8"
LESSONS[P + "17fb61ee-1992-4602-8c18-a1fe1a4d38e9"] = lesson(
    B("Riya pays with a 100 rupee note. She buys 5 packets of samosas at 12 rupees each, then spends 8 rupees on chai. Here is the sum.",
      GIVEN("q1", E5, False)),
    B("Which part do we work out first?",
      ask=choose(["100 − 5", "5 × 12", "12 − 8"], 1,
                 "Multiplication goes before subtraction. It fits the story too: we must know what the samosas cost before we take it off the 100.")),
    B("5 times 12 is 60. That is the cost of the samosas.",
      M("q1", "5 × 12"), N("q1", "5 × 12", "60", "below"), W("a", "100 − 60 − 8")),
    B("Now there are two subtractions, and we go from left to right. 100 minus 60 is 40.",
      W("b", "100 − 60 = 40")),
    B("Then the chai. 40 minus 8 is 32, so Riya has 32 rupees left.",
      ANSR("c", "40 − 8 = 32", "32")),
    B("The classic slip is doing 100 minus 5 first, and then multiplying. That would leave Riya with far more money than the note she started with!"),
    B("Check with the story. 60 for samosas and 8 for chai is 68 rupees spent. And 68 plus 32 makes the 100 rupee note.",
      W("d", "60 + 8 = 68"), W("e", "68 + 32 = 100")),
    B("So: do the times first, then the subtractions from left to right."),
)

# ── 48 laddoos in 6 boxes, then 5 more in each ───────────────────────────────
LESSONS[P + "1ee7a7c7-db2b-43ac-9baf-e466c39d5d80"] = lesson(
    B("Ananya has 48 laddoos. She packs them equally into 6 boxes, and then her mom adds 5 more to each box. How many are in each box now?",
      GIVEN("q1", "48 laddoos, 6 equal boxes, then 5 more in each box")),
    B("What happens first in the story?",
      ask=choose(["mom adds 5 laddoos", "48 is shared into 6 boxes"], 1,
                 "Read it again: she packs the 48 into boxes first. Mom's extra laddoos come afterwards, when the boxes are already filled.")),
    B("So the sum is 48 divided by 6, plus 5.",
      W("a", "48 ÷ 6 + 5")),
    B("BODMAS agrees with the story: divide before you add. 48 divided by 6 is 8, so there are 8 laddoos in each box.",
      M("a", "48 ÷ 6"), WN("b", "48 ÷ 6 = 8", "8", "in each box")),
    B("Then mom adds 5 to each box. 8 plus 5 is 13 laddoos.",
      ANSR("c", "8 + 5 = 13", "13")),
    B("Here is the trap. The 5 goes into each box, so it is added after the sharing. Add 5 to the 48 first and you get 53, which is a different story.",
      W("d", "48 + 5 = 53"), N("d", "48 + 5", "not this story", "below")),
    B("Let's check by counting every laddoo. Mom gave 5 to each of the 6 boxes, which is 30. So there are 48 plus 30, 78 laddoos, and 6 boxes of 13 is 78 too.",
      W("e", "6 × 5 = 30"), W("g", "48 + 30 = 78"), W("h", "6 × 13 = 78")),
    B("So follow the story in order. And if you are unsure, BODMAS says the same thing: divide before you add."),
)
