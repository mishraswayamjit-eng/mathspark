"""Square numbers: story problems, spotting a square, last digits, sums of squares."""
from imported_19_lib import ANS, ANSR, B, FIG, L, M, N, S, W, GIVEN, ask, choose, lesson, pick

LESSONS = {}
A = "AIGEN_grade5_"
P = "IPMTB_grade5_ch04_q"

# ── Priya's diyas: add 15 and reach the next square ──────────────────────────

LESSONS[A + "e344c1e4-4633-4147-9ff3-d5e942eae3be"] = lesson(
    B("Priya has a square of diyas. Add 15 more, and she can make the very next bigger square. How many diyas are in her square now?",
      GIVEN("q", "A square + 15 = the next square")),
    B("Let's write the square numbers in a row. 1 times 1 is 1, 2 times 2 is 4, 3 times 3 is 9, and so on.",
      L("sq", "Squares: 1, 4, 9, 16, 25, 36, 49, 64, 81")),
    B("We need two neighbours in this list with a gap of exactly 15. Try 25 and 36. What is the gap between them?",
      M("sq", "25"), M("sq", "36"),
      ask=choose(["15", "11", "9"], 1,
                 "Count on from 25 until you reach 36. How many steps did you take?")),
    B("11. Too small. But look at how the gaps grow: 3, 5, 7, 9, 11. Each gap is 2 more than the one before.",
      W("g1", "36 − 25 = 11"), L("gp", "Gaps: 3, 5, 7, 9, 11, 13, 15")),
    B("So after 11 comes 13, and then 15. The gap of 15 sits between 49 and 64.",
      M("gp", "15", "box"), W("g2", "64 − 49 = 15")),
    B("Now, careful. Priya's square today is the one before the 15 extra diyas go in. Which number is that?",
      ask=choose(["64", "15", "49"], 2,
                 "64 is the bigger square, after the extra diyas are added. Her square today is the smaller of the two neighbours.")),
    B("49. That is 7 rows with 7 diyas in each.",
      ANSR("a", "7 × 7 = 49", "49")),
    B("Check it against the story. 49 plus 15 is 64, and 64 is 8 times 8. The next square, just as it should be.",
      W("c1", "49 + 15 = 64"), W("c2", "8 × 8 = 64")),
    B("So when you know the gap between two squares that are neighbours, list the squares, find that gap, and pick the one the question asks for."),
)

# ── Aarav's coins: an 8 square grows to an 11 square ─────────────────────────

LESSONS[A + "e419e561-ff8c-4daf-bae2-02021e8fdf47"] = lesson(
    B("Aarav had a square of coins with 8 on each side. Now he has a bigger square, with 11 on each side. How many coins did his uncle give him?",
      GIVEN("q", "Square of side 8 → square of side 11. Coins added?"),
      FIG("f1", {"kind": "grid", "rows": 8, "cols": 8})),
    B("Start with last week. 8 coins on each side means 8 rows, with 8 coins in every row. How do we count them all?",
      ask=choose(["8 + 8", "8 × 8", "8 × 4"], 1,
                 "8 plus 8 only counts two edges. The square is filled in: 8 rows, and 8 coins in each row. So it is rows times coins in a row.")),
    B("8 times 8 is 64. He had 64 coins last week.",
      W("w1", "8 × 8 = 64"), N("w1", "64", "last week")),
    B("This week the square is 11 rows of 11. 11 times 10 is 110, and one more 11 makes 121.",
      W("w2", "11 × 11 = 110 + 11"), W("w3", "11 × 11 = 121"), N("w3", "121", "this week")),
    B("The uncle's coins are the extra ones. Which sum finds them?",
      ask=choose(["121 + 64", "11 − 8", "121 − 64"], 2,
                 "11 minus 8 compares the sides, not the coins. We want how many more coins there are this week than last week.")),
    B("121 minus 64. Take away 60 first, which leaves 61. Then take away 4 more: 57.",
      W("w4", "121 − 60 = 61"), ANSR("a", "121 − 64 = 57", "57")),
    B("Check by adding back. 64 plus 57 is 121. It works.",
      W("c", "64 + 57 = 121")),
    B("The trap is to subtract the sides, 11 minus 8, and say 3. Sides are not coins!"),
    B("So: side times side gives the coins in each square. Then subtract to find what was added."),
)

# ── Riya's 225 tiles: (side)² + √225 ─────────────────────────────────────────

LESSONS[A + "e9baf609-4fe9-456e-b861-2647dd4dd744"] = lesson(
    B("This story is long, so let's pull out what it asks. Riya has 200 tiles and adds 25 more to make a square. We want the side squared, plus the square root of 225.",
      GIVEN("q", "(side)² + √225 = ?"), L("t", "Tiles: 200 + 25")),
    B("First, the tiles. 200 plus 25 is 225.",
      W("w1", "200 + 25 = 225")),
    B("225 tiles make a perfect square. The side is the number that, times itself, gives 225. Which of these could it be?",
      ask=choose(["25", "15", "5"], 1,
                 "5 times 5 is only 25, and 25 times 25 is far more than 225. Try the number in between.")),
    B("15. Let's test it. 15 times 10 is 150, and 15 times 5 is 75. Together that is 225.",
      W("w2", "15 × 15 = 150 + 75"), W("w3", "15 × 15 = 225")),
    B("So the side is 15 tiles. That also tells us the square root of 225: it is 15.",
      W("w4", "√225 = 15"), M("w4", "15", "underline")),
    B("Now the sum. The first part is the side squared. The side is 15. What is 15 squared?",
      ask=choose(["30", "225", "15"], 1,
                 "Squared means times itself, not times 2. And 15 times 15 is already on the board.")),
    B("225. Squaring the side takes us straight back to the number of tiles. Squaring and square root undo each other.",
      W("w5", "15² = 225")),
    B("Now add the two parts. 225 plus 15 is 240.",
      W("w6", "15² + √225 = 225 + 15"), ANSR("a", "225 + 15 = 240", "240")),
    B("Watch the trap. One part is the square, 225. The other is the root, 15. Adding 225 twice, or 15 twice, mixes them up."),
    B("In a long question, find what it really asks, work out each part, then put the parts together."),
)

# ── Riya's border: 196 tiles, then a border all round ────────────────────────

LESSONS[A + "f1fe077a-4169-4b2d-8add-83014e721e8e"] = lesson(
    B("Riya makes a square from 196 tiles. Then she puts a border of tiles all the way round, one tile wide, to make a bigger square. How many more tiles does she need?",
      GIVEN("q", "196 tiles in a square. Border all round: how many more?")),
    B("First, how long is a side? We need the number that times itself gives 196. It ends in 6, so let's try 14. 14 times 10 is 140, and 14 times 4 is 56.",
      W("w1", "14 × 14 = 140 + 56"), W("w2", "14 × 14 = 196")),
    B("140 and 56 make 196. So each side has 14 tiles.",
      M("w2", "14", "underline"), FIG("f1", {"kind": "rectangle", "square": True, "length": "14", "breadth": "14", "inside": "196 tiles"})),
    B("Now the border goes all the way round. Here is the turning point. How long is a side of the bigger square?",
      ask=choose(["15 tiles", "16 tiles", "18 tiles"], 1,
                 "The border adds one tile at each end of a side: one on the left, and one on the right. So how much longer does the side get?")),
    B("16. One extra tile at each end, so the side grows by 2.",
      W("w3", "14 + 2 = 16")),
    B("The bigger square is 16 rows of 16. 16 times 10 is 160, 16 times 6 is 96, and together they make 256.",
      W("w4", "16 × 16 = 160 + 96"), W("w5", "16 × 16 = 256")),
    B("Riya already has 196 of those tiles. Which sum gives the tiles she must buy?",
      ask=choose(["256 − 196", "256 + 196", "16 × 4"], 0,
                 "The big square needs 256 tiles, and she has 196 of them already. The ones to buy are the difference.")),
    B("256 minus 196 is 60. She needs 60 more tiles.",
      ANSR("a", "256 − 196 = 60", "60")),
    B("Check it another way. Four strips of 14 along the sides make 56. Add the 4 corner tiles, and we get 60 again.",
      W("c1", "4 × 14 = 56"), W("c2", "56 + 4 = 60")),
    B("The corners are the trap. It is easy to count the four sides and forget them. Big square minus small square never forgets anything."),
)

# ── Riya's corner: 625 tiles, 576 remain ─────────────────────────────────────

LESSONS[A + "fccc2071-ac7c-4d33-beab-d71273d4cc65"] = lesson(
    B("Riya has a big square of 625 tiles. She takes a small square out of one corner, and 576 tiles are left. We want the side of the square she can make from the tiles she took out.",
      GIVEN("q", "625 tiles − a small square = 576 tiles. Its side?")),
    B("First, how many tiles did she take out? Which sum tells us?",
      ask=choose(["625 + 576", "625 − 576", "625 ÷ 576"], 1,
                 "She started with 625, and 576 are still there. The missing tiles are the difference between those two numbers.")),
    B("625 minus 576. Let's count up. From 576, 24 more gets us to 600. Then 25 more gets us to 625.",
      W("w1", "576 + 24 = 600"), W("w2", "600 + 25 = 625")),
    B("24 and 25 make 49. So she took out 49 tiles.",
      W("w3", "625 − 576 = 49"), M("w3", "49", "underline")),
    B("Now those 49 tiles make a new square. The question asks for its side, not the number of tiles. Which number times itself makes 49?",
      ask=choose(["49", "7", "9"], 1,
                 "49 is how many tiles are in the whole square. The side is the number that, multiplied by itself, makes 49. Think of the 7 times table.")),
    B("7 times 7 is 49. So the new square has 7 tiles on each side.",
      W("w4", "7 × 7 = 49"), ANSR("a", "√49 = 7", "7")),
    B("Check that no tile has gone missing. The 576 left, plus the 49 taken out, make 625.",
      W("c", "576 + 49 = 625")),
    B("The trap is to stop at 49. That is how many tiles there are. The side is its square root."),
    B("So: subtract to find what was removed, then take the square root to find the side."),
)

# ── Which of these is (not) a square? ────────────────────────────────────────

LESSONS[P + "001"] = lesson(
    B("Four numbers. Three of them are square numbers, and one is not. We want the odd one out.",
      GIVEN("q", "Which is NOT a square number?"), L("o", "529    144    117    625")),
    B("A square number is a whole number times itself, like 3 times 3 is 9. Here is a quick test: a square number can only end in 0, 1, 4, 5, 6 or 9.",
      L("r", "Squares end in 0, 1, 4, 5, 6 or 9")),
    B("So look at the last digit of each number. Which one ends in a digit that is not on the list?",
      ask=choose(["144", "625", "117"], 2,
                 "144 ends in 4 and 625 ends in 5. Both of those are on the list. One of the numbers ends in 7.")),
    B("117 ends in 7, so it cannot be a square. Let's make sure. 10 times 10 is 100, and 11 times 11 is 121.",
      M("o", "117", "box"), W("w1", "10 × 10 = 100"), W("w2", "11 × 11 = 121")),
    B("117 sits between 100 and 121. There is no whole number between 10 and 11, so nothing times itself gives 117.",
      W("w3", "100 < 117 < 121")),
    B("Now the other three, to be sure they really are squares. 12 times 12 is 144.",
      W("w4", "12 × 12 = 144")),
    B("23 times 23 is 529. And 25 times 25 is 625. All three are squares.",
      W("w5", "23 × 23 = 529"), W("w6", "25 × 25 = 625")),
    B("So the one that is not a square number is 117.",
      ANSR("a", "117 is not a square number", "117", True)),
    B("Notice the word not in the question. Three of the choices are squares, so it is easy to pick the first square you spot."),
    B("The method: look at the last digit first. Then trap the number between two squares that are next to each other."),
)

LESSONS[P + "002"] = lesson(
    B("Four numbers, and only one of them is a square number. Let's hunt for it.",
      GIVEN("q", "Which is a square number?"), L("o", "554    289    111    69")),
    B("To test a number, we trap it between two squares that are next door to each other. Start with 69. 8 times 8 is 64, and 9 times 9 is 81.",
      W("w1", "8 × 8 = 64"), W("w2", "9 × 9 = 81")),
    B("69 is between 64 and 81, and there is no whole number between 8 and 9. So 69 is out.",
      W("w3", "64 < 69 < 81"), S("o", "69")),
    B("Now 111. 10 times 10 is 100, and 11 times 11 is 121. 111 is stuck between them. Out.",
      W("w4a", "10 × 10 = 100"), W("w4b", "11 × 11 = 121"), S("o", "111")),
    B("Now 289. It is between 100 and 20 times 20, which is 400. So we want a number in the teens. 289 ends in 9. Which of these, squared, ends in 9?",
      W("w5", "20 × 20 = 400"),
      ask=choose(["15", "16", "17"], 2,
                 "Look at the last digits. 5 times 5 ends in 5, and 6 times 6 ends in 6. Now work out 7 times 7, and look at its last digit.")),
    B("17. Let's try it. 17 times 10 is 170, and 17 times 7 is 119. Together they make 289.",
      W("w6", "17 × 17 = 170 + 119"), W("w7", "170 + 119 = 289")),
    B("So 289 is 17 times 17. It is a square number.",
      ANSR("a", "17 × 17 = 289", "289"), M("o", "289", "circle")),
    B("And 554? 23 times 23 is 529, and 24 times 24 is 576. 554 is trapped between them, so it is not a square.",
      W("w8", "23 × 23 = 529"), W("w9", "24 × 24 = 576"), S("o", "554")),
    B("Notice that 69 and 111 end in 9 and 1, just as many squares do. A friendly last digit is not enough on its own."),
    B("So, to test for a square: guess the size, use the last digit to choose a number to try, and multiply it by itself."),
)

LESSONS[P + "021"] = lesson(
    B("Four numbers, and one of them is a square. Let's find it.",
      GIVEN("q", "Which is a square?"), L("o", "800    8,381    1,000    1,089")),
    B("A handy fact to start: 30 times 30 is 900. So 800 comes from a number just under 30, if it is a square at all.",
      W("w0", "30 × 30 = 900")),
    B("28 times 28 is 784, and 29 times 29 is 841. 800 falls in the gap between them, so it is not a square.",
      W("w1", "28 × 28 = 784"), W("w2", "29 × 29 = 841"), S("o", "800")),
    B("Now 1,000. 31 times 31 is 961, and 32 times 32 is 1,024. 1,000 falls in that gap. Not a square either.",
      W("w3", "31 × 31 = 961"), W("w4", "32 × 32 = 1,024"), S("o", "1,000")),
    B("1,089 comes just after 1,024. So which number should we try squaring?",
      ask=choose(["31", "33", "30"], 1,
                 "32 times 32 gave 1,024, which is a little too small. So try the next number up.")),
    B("33. 33 times 30 is 990, and 33 times 3 is 99. Together they make 1,089. Got it!",
      W("w5", "33 × 33 = 990 + 99"), W("w6", "990 + 99 = 1,089")),
    B("So 1,089 is 33 times 33. That is our square.",
      ANSR("a", "33 × 33 = 1,089", "1,089"), M("o", "1,089", "circle")),
    B("What about 8,381? It ends in 1, which looks promising. But 91 times 91 is 8,281, and 92 times 92 is 8,464. 8,381 sits in the gap.",
      W("w7", "91 × 91 = 8,281"), W("w8", "92 × 92 = 8,464"), S("o", "8,381")),
    B("So a friendly last digit is not proof. Trap the number between two squares that are next to each other, or find the number that squares to it."),
)


# ── The last digit of a square ───────────────────────────────────────────────

def last_digit(qid, options, answer, can):
    """options: the four digits as printed; answer: the keyed digit; can: True for 'can be', False for 'cannot be'."""
    opts = "    ".join(options)
    endings = ["0", "1", "4", "5", "6", "9"]
    others = [o for o in options if o != answer]
    if can:
        first = B("We have four digits. Only one of them can be the last digit of a square number. Which?",
                  GIVEN("q", "Which digit can be in the units place of a square?"), L("o", opts))
        test = B("Now test the choices. %s, %s and %s are not on our list. %s is." % (others[0], others[1], others[2], answer),
                 [S("o", o) for o in others], M("o", answer, "circle"))
        end = B("So a square number can end in %s. For example, 10 times 10 is 100." % answer,
                ANSR("a", "A square can end in %s" % answer, answer, True), W("e", "10 × 10 = 100"))
        trap = B("The trap is to think any digit can turn up at the end of a square. No square ever ends in 2, 3, 7 or 8.")
    else:
        first = B("We have four digits. Three of them can be the last digit of a square number. One never can. Which?",
                  GIVEN("q", "Which digit can NOT be in the units place of a square?"), L("o", opts))
        test = B("Now test the choices. %s, %s and %s are all on our list. %s is not." % (others[0], others[1], others[2], answer),
                 M("o", answer, "circle"))
        end = B("So a square number can never end in %s." % answer,
                ANSR("a", "A square never ends in %s" % answer, answer, True))
        trap = B("Notice the words can not in the question. Three of the choices are fine endings, and we want the one that is not. The four digits that never end a square are 2, 3, 7 and 8.")
    return lesson(
        first,
        B("The units place is the last digit. And here is a lovely fact: the last digit of a square depends only on the last digit of the number you square. So we only need to test 0 to 9."),
        B("Let's square them. 0 times 0 is 0. 1 times 1 is 1. 2 times 2 is 4. 3 times 3 is 9. 4 times 4 is 16.",
          L("s1", "0×0 = 0   1×1 = 1   2×2 = 4   3×3 = 9   4×4 = 16")),
        B("5 times 5 is 25. 6 times 6 is 36. 7 times 7 is 49. 8 times 8 is 64. 9 times 9 is 81.",
          L("s2", "5×5 = 25   6×6 = 36   7×7 = 49   8×8 = 64   9×9 = 81")),
        B("Now look only at the last digit of each answer. 16 ends in 6. What does 49 end in?",
          M("s1", "16"), M("s2", "49"),
          ask=choose(["4", "9", "7"], 1,
                     "The last digit is the one on the right, in the units place. 49 has 4 tens and 9 units.")),
        B("9. Collect all ten last digits, and only six different ones turn up: 0, 1, 4, 5, 6 and 9.",
          L("r", "Last digits of squares: 0, 1, 4, 5, 6, 9"), M("r", "0, 1, 4, 5, 6, 9", "box")),
        test,
        end,
        trap,
        B("So remember the six endings a square can have: 0, 1, 4, 5, 6 and 9."),
    )


LESSONS[P + "006"] = last_digit(P + "006", ["2", "3", "0", "7"], "0", True)
LESSONS[P + "007"] = last_digit(P + "007", ["1", "4", "5", "8"], "8", False)


# ── The square of which number is the sum of two squares? ────────────────────

def sum_of_squares(qid, a, b, root):
    """root: the whole number whose square is a² + b², or None when there is none."""
    sa, sb = a * a, b * b
    total = sa + sb
    start = [
        B("This question is a mouthful. In short: square %d, square %d, add the two answers, and then find which number squared gives that total." % (a, b),
          GIVEN("q", "?² = %d² + %d²" % (a, b))),
        B("Start with the square of %d. What does squaring a number mean?" % a,
          ask=choose(["%d × 2" % a, "%d × %d" % (a, a), "%d + %d" % (a, a)], 1,
                     "Squaring is multiplying a number by itself. So the square of %d is %d times %d." % (a, a, a))),
        B("%d times %d is %d. And the square of %d is %d times %d, which is %d." % (a, a, sa, b, b, b, sb),
          W("w1", "%d² = %d × %d = %d" % (a, a, a, sa)), W("w2", "%d² = %d × %d = %d" % (b, b, b, sb))),
        B("Now add the two squares. %d plus %d is %d." % (sa, sb, total),
          W("w3", "%d + %d = %d" % (sa, sb, total)), M("w3", str(total), "underline")),
    ]
    if root:
        rest = [
            B("Last step. Which number, times itself, makes %d?" % total,
              ask=choose([str(a + b), str(total), str(root)], 2,
                         "%d is just %d plus %d, and %d times %d is much more than %d. We need the number whose square is %d." % (a + b, a, b, a + b, a + b, total, total))),
            B("%d times %d is %d. So the number is %d." % (root, root, total, root),
              W("w4", "%d × %d = %d" % (root, root, total)), ANSR("a", "%d² = %d² + %d²" % (root, a, b), str(root))),
            B("Careful with the trap: you cannot add %d and %d first and say %d. Square each number first, then add." % (a, b, a + b)),
            B("So: square each number, add the squares, then find the number whose square is that total."),
        ]
    else:
        lo = int(total ** 0.5)
        hi = lo + 1
        rest = [
            B("Last step. Which number, times itself, makes %d? Try %d. %d times %d is %d. Too small." % (total, lo, lo, lo, lo * lo),
              W("w4", "%d × %d = %d" % (lo, lo, lo * lo))),
            B("Try the next number, %d. %d times %d is %d. What does that tell us?" % (hi, hi, hi, hi * hi),
              W("w5", "%d × %d = %d" % (hi, hi, hi * hi)),
              ask=choose(["the number is %d" % lo, "the number is %d" % hi, "%d is not a square" % total], 2,
                         "%d is below %d, and %d is above it. So %d falls in the gap between two squares that are next door." % (lo * lo, total, hi * hi, total))),
            B("%d is stuck between %d and %d. No whole number squared gives %d, so 5, 6 and 7 are all out." % (total, lo * lo, hi * hi, total),
              W("w6", "%d < %d < %d" % (lo * lo, total, hi * hi))),
            B("So the answer is: none of these.",
              ANS("a", "None of these", True), M("a", "None of these", "circle")),
            B("It can feel odd to pick none of these. But we did the sum and tested the numbers on both sides, so we can be sure."),
            B("So: square each number, add the squares, then look for a number whose square is that total. Sometimes there is none."),
        ]
    return lesson(*(start + rest))


LESSONS[P + "008"] = sum_of_squares(P + "008", 3, 4, 5)
LESSONS[P + "025"] = sum_of_squares(P + "025", 3, 7, None)

# ── Add it to itself: 4. Multiply it by itself: 4. ───────────────────────────

LESSONS[P + "026"] = lesson(
    B("A mystery number. Add it to itself and we get 4. Multiply it by itself and we get 4 again. Both clues must be true.",
      GIVEN("q", "□ + □ = 4   and   □ × □ = 4")),
    B("Start with the adding clue. Two equal numbers add up to 4. What is each one?",
      M("q", "□ + □ = 4"),
      ask=choose(["4", "2", "8"], 1,
                 "Two equal numbers make 4 together. So share 4 into two equal parts.")),
    B("2, because 2 plus 2 is 4.",
      W("w1", "2 + 2 = 4")),
    B("We are not done. The second clue has to fit as well. 2 times 2 is 4. Yes, it does!",
      M("q", "□ × □ = 4"), W("w2", "2 × 2 = 4")),
    B("Both clues fit, so the number is 2.",
      ANSR("a", "The number is 2", "2", True)),
    B("Let's see why the other choices do not work. 1 plus 1 is only 2. And 3 plus 3 is 6. Neither gives 4.",
      W("w3", "1 + 1 = 2"), W("w4", "3 + 3 = 6")),
    B("Here is something to watch. For 2, doubling and squaring give the same answer. For most numbers they do not: 3 doubled is 6, but 3 squared is 9.",
      W("w5", "3 × 3 = 9")),
    B("So with two clues, use one clue to find the number and the other clue to check it."),
)
