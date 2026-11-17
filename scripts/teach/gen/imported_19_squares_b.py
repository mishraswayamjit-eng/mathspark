"""Square numbers: rows and rooms, areas of squares, square roots, least and largest squares."""
from imported_19_lib import ANSR, B, FIG, L, M, N, S, W, GIVEN, choose, lesson, num

LESSONS = {}
P = "IPMTB_grade5_ch04_q"


# ── n in each row, n rows ────────────────────────────────────────────────────

def rows(n, things, group, groups, trap):
    tens, units = n - n % 10, n % 10
    a, b, total = n * tens, n * units, n * n
    second = ("%d times 1 is just %d" % (n, n)) if units == 1 else ("%d times %d is %d" % (n, units, b))
    return lesson(
        B("%d %s in every %s, and %d %s in all. How many %s altogether?" % (n, things, group, n, groups, things),
          GIVEN("q", "%d in each %s, %d %s. Total?" % (n, group, n, groups))),
        B("These are equal groups, counted again and again. Which sum gives the total?",
          ask=choose(["%d + %d" % (n, n), "%d × %d" % (n, n), "%d × 2" % n], 1,
                     "%d plus %d counts only two %s. There are %d %s, each with %d in it, so we multiply." % (n, n, groups, n, groups, n))),
        B("%d times %d. A number times itself: that is a square number. It is a big sum, so let's split one %d into %d and %d." % (n, n, n, tens, units),
          W("w1", "%d × %d = %d × %d + %d × %d" % (n, n, n, tens, n, units)),
          M("w1", "%d × %d" % (n, tens)), M("w1", "%d × %d" % (n, units))),
        B("Take the first part. What is %d times %d?" % (n, tens),
          ask=choose([str(n * tens // 10), num(a), num(tens * tens)], 1,
                     "Work out %d times %d first. Then make it ten times bigger, because %d is %d tens." % (n, tens // 10, tens, tens // 10))),
        B("%s. Now the second part: %s." % (num(a), second),
          W("w2", "%d × %d = %s" % (n, tens, num(a))), W("w3", "%d × %d = %s" % (n, units, num(b)))),
        B("Add the two parts. %s plus %s is %s. So there are %s %s." % (num(a), num(b), num(total), num(total), things),
          ANSR("a", "%s + %s = %s" % (num(a), num(b), num(total)), num(total))),
        B("Does that look sensible? %d times %d is %s, so our answer should be a bit more than %s. It is." % (tens, tens, num(tens * tens), num(tens * tens)),
          W("c", "%d × %d = %s" % (tens, tens, num(tens * tens)))),
        trap,
        B("So for %d %s of %d, multiply %d by itself. Split it into tens and ones to make the sum easy." % (n, groups, n, n)),
    )


LESSONS[P + "005"] = rows(31, "students", "row", "rows",
                          B("The trap is to stop at 31 times 30. That leaves out one whole row of 31 students."))
LESSONS[P + "024"] = rows(34, "boys", "room", "rooms",
                          B("The trap is to add. 34 plus 34 is only 68, and that counts just two of the rooms.",
                            W("t", "34 + 34 = 68"), S("t", "34 + 34 = 68", "only 2 rooms")))


# ── The area of a square from its side ───────────────────────────────────────

def area(side, unit_choices, unit_answer, unit_miss, check, last):
    tens, units = side - side % 10, side % 10
    a, b, total = side * tens, side * units, side * side
    second = ("%d times 1 is just %d" % (side, side)) if units == 1 else ("%d times %d is %d" % (side, units, b))
    return lesson(
        B("Here is a square, and each side is %d centimetres. We want its area: how much flat space it covers." % side,
          GIVEN("q", "Square: side %d cm. Area = ?" % side),
          FIG("f1", {"kind": "rectangle", "square": True, "length": "%d cm" % side, "breadth": "%d cm" % side, "inside": "Area = ?"})),
        B("How do we find the area of a square?",
          ask=choose(["side × 4", "side × side", "side + side"], 1,
                     "Side times 4 goes round the edge. That is the perimeter. Area fills the inside: rows of little squares, so it is side times side.")),
        B("Side times side. So the area is %d times %d." % (side, side),
          L("r", "Area = side × side"), L("w0", "Area = %d × %d" % (side, side))),
        B("Split one %d into %d and %d. %d times %d is %d, and %s." % (side, tens, units, side, tens, a, second),
          W("w1", "%d × %d = %d × %d + %d × %d" % (side, side, side, tens, side, units)),
          W("w2", "%d × %d = %d" % (side, tens, a)), W("w3", "%d × %d = %d" % (side, units, b))),
        B("Add the two parts. %d plus %d is %d." % (a, b, total),
          W("w4", "%d + %d = %d" % (a, b, total)), M("w4", str(total), "underline")),
        B("Now the unit, and this matters. The sides are in centimetres. What is the area measured in?",
          ask=choose(unit_choices, unit_answer, unit_miss)),
        B("Square centimetres. So the area is %d square centimetres." % total,
          ANSR("a", "Area = %d sq.cm" % total, "%d sq.cm" % total, True)),
        check,
        last,
    )


LESSONS[P + "010"] = area(
    21, ["cm", "sq.cm"], 1,
    "Plain centimetres measure a length, like a side. Area is counted in little squares, each 1 centimetre by 1 centimetre.",
    B("Quick check: 20 times 20 is 400. A square of side 21 should cover a little more than that, and 441 does.",
      W("c", "20 × 20 = 400")),
    B("Two things to watch: keep the digits of the number in the right order, and write square centimetres for an area. Side times side, then square units."))

LESSONS[P + "029"] = area(
    26, ["sq.mm", "cm", "sq.cm"], 2,
    "Plain centimetres measure a length, not an area. And the side was given in centimetres, so the little squares we count are centimetre squares.",
    B("Quick check: 20 times 20 is 400, and 30 times 30 is 900. A square of side 26 should be in between, and 676 is.",
      W("c1", "20 × 20 = 400"), W("c2", "30 × 30 = 900")),
    B("The choices try to catch you on the unit. The number alone is not the answer. Side times side, then square units to match the side."))

# ── Square roots: the same number of rows as in each row ─────────────────────

HALF_TRAP = "The trap is to halve the total. Halving undoes adding a number to itself. A square root undoes multiplying it by itself."
ROOT_PLAN = "So to find a square root: trap it between two easy squares, use the last digit to narrow it down, then multiply to check."

LESSONS[P + "009"] = lesson(
    B("Students stand in rows. The number of rows is the same as the number of students in each row, and there are 576 students in all. How many rows?",
      GIVEN("q", "rows = students in each row. Total 576. Rows = ?")),
    B("Rows times students in a row gives the total. Here those two numbers are the same. So what are we looking for?",
      L("r", "□ × □ = 576"),
      ask=choose(["576 ÷ 2", "the square root of 576", "576 × 576"], 1,
                 "Halving would work if the number were added to itself. Here it is multiplied by itself, so we need the number whose square is 576.")),
    B("Let's close in on it. 20 times 20 is 400: too small. 30 times 30 is 900: too big. So our number is in the twenties.",
      W("w1", "20 × 20 = 400"), W("w2", "30 × 30 = 900")),
    B("Now the last digit. 576 ends in 6. 4 times 4 is 16, and 6 times 6 is 36, and both end in 6. So the number is 24 or 26.",
      W("w3", "4 × 4 = 16"), W("w4", "6 × 6 = 36"), L("t", "Try 24 or 26")),
    B("Here is a helper: 25 times 25 is 625, and that is more than 576. So which one is it?",
      W("w5", "25 × 25 = 625"),
      ask=choose(["26", "24"], 1,
                 "25 squared is already too big, so 26 squared would be bigger still. We need the one below 25.")),
    B("24. Let's check it. 24 times 20 is 480, and 24 times 4 is 96. Together they make 576. Yes!",
      W("w6", "24 × 24 = 480 + 96"), W("w7", "480 + 96 = 576")),
    B("So there are 24 rows, with 24 students in each.",
      ANSR("a", "√576 = 24", "24")),
    B(HALF_TRAP),
    B(ROOT_PLAN),
)

LESSONS[P + "027"] = lesson(
    B("Students sit in rooms. The number of rooms is the same as the number of students in each room, and there are 625 students in all. How many rooms?",
      GIVEN("q", "rooms = students in each room. Total 625. Rooms = ?")),
    B("Rooms times students in a room gives the total, and here those two numbers are the same. So what do we need?",
      L("r", "□ × □ = 625"),
      ask=choose(["the square root of 625", "625 ÷ 2", "625 × 2"], 0,
                 "Halving would work if the number were added to itself. Here it is multiplied by itself, so we need the number whose square is 625.")),
    B("Close in on it. 20 times 20 is 400: too small. 30 times 30 is 900: too big. So the number is in the twenties.",
      W("w1", "20 × 20 = 400"), W("w2", "30 × 30 = 900")),
    B("Now the last digit. 625 ends in 5. Only a number ending in 5 has a square ending in 5. So the one to try is 25.",
      M("q", "625"), L("t", "Try 25")),
    B("25 times 25. 25 times 20 is 500, and 25 times 5 is 125. What do they make together?",
      W("w3", "25 × 25 = 500 + 125"),
      ask=choose(["525", "625", "650"], 1,
                 "Add the two parts on the board: 500, and then 125 more.")),
    B("625, exactly what we wanted. So there are 25 rooms, with 25 students in each.",
      W("w4", "500 + 125 = 625"), ANSR("a", "√625 = 25", "25")),
    B("The other choices are close on purpose: 24, 26 and 27. Only a number ending in 5 can give a square ending in 5, so they are out at once.",
      L("x", "24, 26, 27: their squares cannot end in 5")),
    B(HALF_TRAP),
    B(ROOT_PLAN),
)

LESSONS[P + "028"] = lesson(
    B("A square has an area of 169 square centimetres. We want the length of each side.",
      GIVEN("q", "Square: area 169 sq.cm. Side = ?"),
      FIG("f1", {"kind": "rectangle", "square": True, "length": "?", "inside": "169 sq.cm"})),
    B("For a square, area is side times side. We know the area and want the side. So what must we find?",
      L("r", "side × side = 169"),
      ask=choose(["169 ÷ 4", "169 ÷ 2", "the square root of 169"], 2,
                 "Dividing by 4 is for a perimeter, where four sides are added. Here the side is multiplied by itself, so we need the number whose square is 169.")),
    B("Close in on it. 10 times 10 is 100: too small. 20 times 20 is 400: too big. So the side is in the teens.",
      W("w1", "10 × 10 = 100"), W("w2", "20 × 20 = 400")),
    B("Now the last digit. 169 ends in 9. 3 times 3 is 9, and 7 times 7 is 49. So the side is 13 or 17.",
      W("w3", "3 × 3 = 9"), W("w4", "7 × 7 = 49"), L("t", "Try 13 or 17")),
    B("169 is much nearer to 100 than to 400. So which one should we try?",
      ask=choose(["17", "13"], 1,
                 "17 is close to 20, so its square would be close to 400. 169 is down near 100, so try the smaller one.")),
    B("13. Check it: 13 times 10 is 130, and 13 times 3 is 39. Together they make 169. Yes!",
      W("w5", "13 × 13 = 130 + 39"), W("w6", "130 + 39 = 169")),
    B("So each side is 13 centimetres.",
      ANSR("a", "Side = 13 cm", "13 cm", True)),
    B("Mind the unit. The area is in square centimetres, so the side is in plain centimetres. Not millimetres, and not square centimetres."),
    B("So for the side of a square, take the square root of the area. " + ROOT_PLAN[3:]),
)

# ── The flowers and the temples ──────────────────────────────────────────────

LESSONS[P + "013"] = lesson(
    B("A man offers flowers at every temple in the city. In each temple he puts as many flowers as there are temples. He uses 4 baskets, with 100 flowers in each. How many temples?",
      GIVEN("q", "4 baskets of 100 flowers."), L("q2", "Flowers in each temple = number of temples")),
    B("First, how many flowers did he use? 4 baskets of 100 is 400.",
      W("w1", "4 × 100 = 400")),
    B("Now the clever clue. Suppose there were just 3 temples. He would put 3 flowers in each, and use 3 times 3, which is 9 flowers.",
      L("e", "If 3 temples: 3 × 3 = 9 flowers")),
    B("So the total is always the number of temples times itself. Which number, times itself, makes 400?",
      L("r", "temples × temples = 400"),
      ask=choose(["200", "100", "20"], 2,
                 "200 is half of 400, but 200 times 200 is far too big. Think: 2 times 2 is 4. So which number times itself is 400?")),
    B("20. 2 times 2 is 4, so 20 times 20 is 400.",
      W("w2", "20 × 20 = 400"), ANSR("a", "√400 = 20", "20")),
    B("So there are 20 temples, and he puts 20 flowers in each one."),
    B("Check with the story: 20 temples with 20 flowers each is 400 flowers. That is exactly 4 baskets of 100."),
    B("The other choices are numbers from the story: 4 is the baskets, and 100 is the flowers in one basket. Neither is the number of temples."),
    B("When the number in each group equals the number of groups, the total is a square. Find the total, then take its square root."),
)

# ── The least and the largest 4-digit squares ────────────────────────────────

LESSONS[P + "011"] = lesson(
    B("We want the smallest number with 4 digits that is also a perfect square.",
      GIVEN("q", "Least 4-digit number that is a perfect square?")),
    B("Start with the smallest 4 digit number of all. Which is it?",
      ask=choose(["1,111", "1,000", "9,999"], 1,
                 "The smallest 4 digit number uses the smallest digits it can: a 1 to start, and then zeros.")),
    B("1,000. If 1,000 were a square, we would be done. So let's test it. 30 times 30 is 900: close, but below.",
      L("s", "Smallest 4-digit number: 1,000"), W("w1", "30 × 30 = 900")),
    B("31 times 31 is 961. Still only 3 digits.",
      W("w2", "31 × 31 = 961"), N("w2", "961", "3 digits")),
    B("Now 32 times 32. 32 times 30 is 960, and 32 times 2 is 64. Together they make 1,024.",
      W("w3", "32 × 32 = 960 + 64"), W("w4", "960 + 64 = 1,024")),
    B("So 961 is just below 1,000, and 1,024 is just above it. Is 1,000 itself a square?",
      W("w5", "961 < 1,000 < 1,024"),
      ask=choose(["Yes", "No, it falls in the gap"], 1,
                 "31 squared is 961 and 32 squared is 1,024. There is no whole number between 31 and 32, so nothing squares to 1,000.")),
    B("It is not. The squares jump from 961 straight to 1,024. So the first square with 4 digits is 1,024.",
      ANSR("a", "32 × 32 = 1,024", "1,024")),
    B("The trap is to answer 1,000 just because it is the least 4 digit number. It also has to be a perfect square."),
    B("So: start at the smallest 4 digit number, and find the first square at or above it."),
)

LESSONS[P + "012"] = lesson(
    B("We want the largest number with 4 digits that is also a perfect square.",
      GIVEN("q", "Largest 4-digit number that is a perfect square?")),
    B("The largest 4 digit number is 9,999. The very next number, 10,000, has 5 digits.",
      L("s", "Largest 4-digit number: 9,999"), L("s2", "Next number: 10,000 (5 digits)")),
    B("Here is a lucky fact. 10,000 is a square: 100 times 100.",
      W("w1", "100 × 100 = 10,000")),
    B("That square has 5 digits, so it is too big. Which square comes just before it?",
      ask=choose(["90 × 90", "99 × 99", "9,999"], 1,
                 "Squares come in order, one after another. The square just before 100 squared comes from the number just before 100.")),
    B("99 times 99. Here is an easy way. 100 lots of 99 make 9,900. We only want 99 lots, so we take one 99 away.",
      W("w2", "99 × 100 = 9,900"), W("w3", "99 × 99 = 9,900 − 99")),
    B("What is 9,900 minus 99?",
      ask=choose(["9,811", "9,899", "9,801"], 2,
                 "Take away 100 first. That is 1 too many, because 99 is 1 less than 100. So give 1 back.")),
    B("9,900 minus 100 is 9,800, and 1 back makes 9,801. So 99 times 99 is 9,801.",
      W("w4", "9,900 − 100 = 9,800"), ANSR("a", "99 × 99 = 9,801", "9,801")),
    B("The trap is 9,999. It is the largest 4 digit number, but it sits between 9,801 and 10,000, so it is not a square.",
      W("w5", "9,801 < 9,999 < 10,000")),
    B("So: find the first square that is too big, then step back one. 100 squared has 5 digits, so 99 squared is the largest with 4."),
)

# ── A square made from given digits ──────────────────────────────────────────

LESSONS[P + "030"] = lesson(
    B("We have the digits 2, 4, 0 and 1. We must arrange them into a 4 digit number that is a square, and we want the smallest one.",
      GIVEN("q", "Smallest 4-digit square using the digits 2, 4, 0, 1"), L("o", "1240    412    1,024    2410")),
    B("Two things must be true: the number uses all four digits, and it is a square. One choice fails the first test straight away. Which?",
      ask=choose(["1240", "412", "2410"], 1,
                 "Count the digits in each choice. The number must have four digits, and one of them must be the 0.")),
    B("412 has only 3 digits, and no 0. Out.",
      S("o", "412", "3 digits")),
    B("Now look at 1240 and 2410. Both end in one zero. A square that ends in 0 comes from 10, 20, 30 and so on, and those squares end in two zeros.",
      W("w1", "10 × 10 = 100"), W("w2", "20 × 20 = 400"), W("w3", "30 × 30 = 900")),
    B("So a number ending in just one zero can never be a square. 1240 and 2410 are out.",
      S("o", "1240"), S("o", "2410")),
    B("That leaves 1,024. Let's make sure. 30 times 30 is 900, so we want a number a little more than 30. And 1,024 ends in 4. Which shall we try?",
      ask=choose(["31", "35", "32"], 2,
                 "Look at last digits. 1 times 1 ends in 1, and 5 times 5 ends in 5. But 2 times 2 is 4, so try the one ending in 2.")),
    B("32. 32 times 30 is 960, and 32 times 2 is 64. Together they make 1,024. It is a square!",
      W("w4", "32 × 32 = 960 + 64"), ANSR("a", "32 × 32 = 1,024", "1,024")),
    B("Is it the smallest? Yes. The square before it is 31 times 31, which is 961, and that has only 3 digits.",
      W("w5", "31 × 31 = 961")),
    B("So check both things every time: the right digits, and a true square."),
)

LESSONS[P + "031"] = lesson(
    B("We have the digits 1, 8, 9 and 0. We must arrange them into a 4 digit number that is a square, and we want the largest one.",
      GIVEN("q", "Largest 4-digit square using the digits 1, 8, 9, 0"), L("o", "9810    9081    8910    9801")),
    B("All four choices use the right digits. So the real question is: which one is a square? Look at 10 times 10, 20 times 20 and 30 times 30. How many zeros do those squares end in?",
      W("w1", "10 × 10 = 100"), W("w2", "20 × 20 = 400"), W("w3", "30 × 30 = 900"),
      ask=choose(["one", "two"], 1,
                 "Look at 100, 400 and 900 on the board, and count the zeros at the end of each.")),
    B("Two. A square that ends in 0 always ends in two zeros. 9810 and 8910 end in just one, so they are out.",
      S("o", "9810"), S("o", "8910")),
    B("Now 9801. It is just below 10,000, and 10,000 is 100 times 100. So let's try the number just below 100, which is 99.",
      W("w4", "100 × 100 = 10,000"), L("t", "Try 99")),
    B("100 lots of 99 make 9,900. We only want 99 lots, so take one 99 away. What is 9,900 minus 99?",
      W("w5", "99 × 100 = 9,900"), W("w6", "99 × 99 = 9,900 − 99"),
      ask=choose(["9,801", "9,811", "9,899"], 0,
                 "Take away 100 first. That is 1 too many, because 99 is 1 less than 100. So give 1 back.")),
    B("9,801. So 99 times 99 is 9,801. It is a square, and it uses 9, 8, 0 and 1.",
      ANSR("a", "99 × 99 = 9,801", "9,801"), M("o", "9801", "circle")),
    B("And it is the largest. The next square is 100 times 100, which already has 5 digits."),
    B("What about 9081? 95 times 95 is 9,025, and 96 times 96 is 9,216. 9081 falls in the gap, so it is not a square.",
      W("w7", "95 × 95 = 9,025"), W("w8", "96 × 96 = 9,216"), S("o", "9081")),
    B("The trap is 9810. It is the biggest number these digits can make, but it is not a square. Biggest is not enough: it must be a square too."),
)
