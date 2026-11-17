"""Square-number lessons for batch 18 that share a structure. Three builders, each fed
one question's numbers and story, computing every board line:

  root      'N things in a square: how many in each row?'
  grow1     'a square of N; add one row and one column: how many more?'
  next_sq   'adding D more makes the next bigger square: how many now (or then)?'
"""
import math

from imported_18_lib import ANS, B, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, P, UL, W, last_nth, pick

LESSONS = {}


def times_parts(a, b, prefix):
    """a × b split into tens and units of b: (what to say, the lines to write)."""
    t, u = (b // 10) * 10, b % 10
    p1, p2 = a * t, a * u
    say = "%d times %d is %d, and %d times %d is %d. %d plus %d is %d." % (a, t, p1, a, u, p2, p1, p2, a * b)
    ops = [W(prefix + "a", "%d × %d = %d" % (a, t, p1)), W(prefix + "b", "%d × %d = %d" % (a, u, p2)),
           W(prefix + "c", "%d + %d = %d" % (p1, p2, a * b))]
    return say, ops


# ── root ─────────────────────────────────────────────────────────────────────

def root(qid, intro, given, N, each, ending, trap_say, trap_ops=()):
    r = math.isqrt(N)
    assert r * r == N and 10 < r < 20
    say_t, ops_t = times_parts(r, r, "m")
    beats = [
        B(intro, GIVEN("q", given)),
        B(pick(qid, "ask1", [
            "A square has as many rows as there are %s in each row. So what kind of number are we hunting for?" % each,
            "In a square, the number of rows and the number of %s in a row are the same. So what are we looking for?" % each,
        ]), ask=CHOOSE(["half of %d" % N, "a number that times itself makes %d" % N, "%d shared by 4" % N], 1,
                       "Rows times %s in a row gives the total. In a square those two numbers are the same, so we need a number that, multiplied by itself, makes %d." % (each, N))),
        B("We want a number that, multiplied by itself, makes %d. That number is called the square root of %d." % (N, N),
          W("l1", "? × ? = %d" % N)),
        B("Start with easy numbers, to see roughly how big it is. 10 times 10 is 100, which is too small. 20 times 20 is 400, which is too big. So our number is between 10 and 20.",
          W("l2", "10 × 10 = 100"), W("l3", "20 × 20 = 400")),
    ]
    if N % 10 == 5:
        beats.append(B("Now look at the last digit of %d. Which number between 10 and 20 could work?" % N,
                       ask=CHOOSE(["12", "%d" % r, "18"], 1,
                                  "%d ends in 5. A number times itself ends in 5 only when the number itself ends in 5. Between 10 and 20, that is %d." % (N, r))))
        beats.append(B("%d ends in 5, so our number must end in 5 as well. Let's test %d. %s It works!" % (N, r, say_t), *ops_t))
        other = r - 1
        check = "Check the one just below, to be sure. %d times %d is %d, which is too small. So %d is the only fit." % (other, other, other * other, r)
    else:
        assert N % 10 == 6 and r % 10 == 4
        beats.append(B("Now look at the last digit of %d. Which numbers between 10 and 20 could work?" % N,
                       ask=CHOOSE(["15", "%d or %d" % (r, r + 2), "12 or 18"], 1,
                                  "%d ends in 6, so our number times itself must end in 6. Try the last digits: 4 times 4 ends in 6, and so does 6 times 6." % N)))
        beats.append(B("4 times 4 and 6 times 6 both end in 6, so it is %d or %d. Test %d first. %s It works!" % (r, r + 2, r, say_t), *ops_t))
        other = r + 2
        check = "Check the other one, to be sure. %d times %d is %d, which is too big. So %d is the only fit." % (other, other, other * other, r)
    ans = "√%d = %d" % (N, r)
    beats += [
        B("So the square root of %d is %d. %s" % (N, r, ending), ANS("a", ans), CIRC("a", str(r), last_nth(ans, str(r)))),
        B(check, W("c", "%d × %d = %d" % (other, other, other * other))),
        B(trap_say, *trap_ops),
        B(pick(qid, "sum", [
            "So to undo a square: find the two tens it sits between, let the last digit narrow it down, then test by multiplying.",
            "So for a square root: trap it between two easy squares, use the last digit as a clue, and always test your guess by multiplying.",
        ])),
    ]
    return LESSON(*beats)


LESSONS[P + "4018fb94-5a51-48e9-8353-5f51d2dd081e"] = root(
    P + "4018fb94-5a51-48e9-8353-5f51d2dd081e",
    "The coach has 225 players and wants them in equal rows and columns, a perfect square, for the photo. How many players stand in each row?",
    "225 players in a square: how many in each row?",
    225, "players", "There are 15 players in each row, and 15 rows.",
    "One of the choices is 25, and it catches the eye because 225 ends in 25. But 25 times 25 is 625, which is far too big.",
    [W("t", "25 × 25 = 625")])

LESSONS[P + "b5826a5e-9dbc-4728-9980-27b47d5d3f45"] = root(
    P + "b5826a5e-9dbc-4728-9980-27b47d5d3f45",
    "Ravi fills a square rangoli with 225 grains of coloured rice, in equal rows and columns. How many grains are along each side?",
    "225 grains fill a square: how many along each side?",
    225, "grains", "Ravi has 15 grains along each side.",
    "Watch out for 25 among the choices. It looks tempting, sitting there at the end of 225, but 25 times 25 is 625. That is much more rice than Ravi has.",
    [W("t", "25 × 25 = 625")])

LESSONS[P + "7034871d-5286-4b0f-a015-d38266802416"] = root(
    P + "7034871d-5286-4b0f-a015-d38266802416",
    "Priya uses all of her 196 diyas to make one perfect square. How many diyas are along each side?",
    "196 diyas in a square: how many along each side?",
    196, "diyas", "Priya has 14 diyas along each side.",
    "One of the choices is 49. That is 196 shared by 4, as if the diyas only went round the edge. But they fill the whole square, so we need rows times columns.",
    [W("t", "196 ÷ 4 = 49")])

LESSONS[P + "9634fbd4-d138-4fbe-96ab-2c5423b7c938"] = root(
    P + "9634fbd4-d138-4fbe-96ab-2c5423b7c938",
    "The coach has 196 players and wants them in a perfect square for the group photo. How many players stand in each row?",
    "196 players in a square: how many in each row?",
    196, "players", "There are 14 players in each row.",
    "The trap is guessing from the last digit alone. Both 14 and 16 looked possible, and only multiplying could tell them apart.")


# ── grow1 ────────────────────────────────────────────────────────────────────

def grow1(qid, intro, given, N, thing, who, lures, ending, trap_say, trap_ops=()):
    r = math.isqrt(N)
    assert r * r == N
    big = r + 1
    L = big * big
    X = L - N
    say_t, ops_t = times_parts(big, big, "m")
    say_r, ops_r = times_parts(r, r, "s")
    ans = "%d − %d = %d" % (L, N, X)
    return LESSON(
        B(intro, GIVEN("q", given)),
        B("First we need the side of the square %s has now. Which number, multiplied by itself, makes %d?" % (who, N),
          ask=CHOOSE([str(lures[0]), str(r), str(lures[1])], 1,
                     "Test each one by multiplying it by itself. Only %d times %d comes to %d." % (r, r, N))),
        B("Let's test %d. %s So the square is %d by %d." % (r, say_r, r, r), *ops_r),
        B("Now add one more row and one more column. How big is the new square?",
          ask=CHOOSE(["%d by %d" % (r, big), "%d by %d" % (big, big), "%d by %d" % (r + 2, r + 2)], 1,
                     "One more row makes %d rows. One more column makes %d in each row. So each side grows by just 1." % (big, big))),
        B("The new square is %d by %d. %s" % (big, big, say_t), *ops_t),
        B("The extra %s are the gap between the two squares. %d minus %d is %d. %s" % (thing, L, N, X, ending),
          ANS("a", ans), CIRC("a", str(X), last_nth(ans, str(X)))),
        B("Here is a neat way to see it, and to check. The new row has %d, the new column has %d, and 1 more fills the corner. %d plus %d plus 1 is %d as well." % (r, r, r, r, X),
          W("c", "%d + %d + 1 = %d" % (r, r, X)), UL("c", "1", last_nth("%d + %d + 1" % (r, r), "1")), NOTE("c", "+ 1", "corner", "below", 2)),
        B(trap_say, *trap_ops),
        B(pick(qid, "sum", [
            "So to grow a square by one: find its side, make the next square, and take away. Or count a row, a column and 1 corner.",
            "So the step from one square to the next is a row, a column and 1 corner. Find the side first, and the rest follows.",
        ])),
    )


LESSONS[P + "3a6979fe-4e4c-43ab-9fa8-0c3727ec7112"] = grow1(
    P + "3a6979fe-4e4c-43ab-9fa8-0c3727ec7112",
    "Meera has 225 water balloons in a square grid. Kiran asks: to add one more row and one more column, making a bigger square, how many more balloons are needed?",
    "225 balloons in a square. Add a row and a column: how many?",
    225, "balloons", "Meera", (25, 45), "Meera needs 31 more balloons.",
    "The trap is forgetting the corner. A row of 15 and a column of 15 make 30, but that leaves a hole where they meet.",
    [W("t", "15 + 15 = 30")])

LESSONS[P + "431b360d-b7ae-4ab9-b271-4df51d6beba5"] = grow1(
    P + "431b360d-b7ae-4ab9-b271-4df51d6beba5",
    "Ankit fills a square tray with 196 samosas, in equal rows and columns. He wants one extra row and one extra column, to make a bigger square. How many more samosas does he need?",
    "196 samosas in a square. Add a row and a column: how many?",
    196, "samosas", "Ankit", (16, 49), "Ankit needs 29 more samosas.",
    "The trap is stopping at the size of the new tray, or forgetting the corner piece where the new row and the new column meet. The corner needs a samosa too.")


# ── next_sq ──────────────────────────────────────────────────────────────────

def next_sq(qid, intro, given, D, thing, want, ending, trap_say):
    assert (D - 1) % 2 == 0
    n = (D - 1) // 2
    small, big = n * n, (n + 1) * (n + 1)
    assert big - small == D
    beats = [
        B(intro, GIVEN("q", given)),
        B(pick(qid, "pic", [
            "Picture a square of %s. To grow it into the very next square, we add one more row along the bottom and one more column down the side." % thing,
            "Think how a square grows into the next one up. It gets one more row along the bottom, and one more column down the side.",
        ])),
        B("The new row is as long as a side of the small square. So is the new column. And 1 more fills the corner where they meet.",
          LB("f", "extra = row + column + 1 corner")),
        B("There are %d extra %s, and one of them is the corner. How many are left for the new row and the new column together?" % (D, thing),
          ask=CHOOSE([str(D + 1), str(D - 1), str(D)], 1,
                     "The %d extra ones are a row, a column and 1 corner piece. Take the corner away, and what is left is the row and the column." % D)),
        B("%d minus 1 is %d. That is the row and the column together." % (D, D - 1),
          W("l1", "%d − 1 = %d" % (D, D - 1)), NOTE("l1", "− 1", "the corner")),
        B("The row and the column are the same length, so we halve. %d divided by 2 is %d. The small square has %d %s on each side." % (D - 1, n, n, thing),
          W("l2", "%d ÷ 2 = %d" % (D - 1, n)), UL("l2", str(n), last_nth("%d ÷ 2 = %d" % (D - 1, n), str(n)))),
    ]
    if want == "small":
        say_t, ops_t = times_parts(n, n, "m")
        ans = "%d × %d = %d" % (n, n, small)
        beats.append(B("So the small square holds %d times %d. %s" % (n, n, say_t), *ops_t))
        beats.append(B(ending, ANS("a", ans), CIRC("a", str(small))))
        beats.append(B("Check: the next square is %d times %d, which is %d. And %d minus %d is %d, just as the story says." % (n + 1, n + 1, big, big, small, D),
                       W("c1", "%d × %d = %d" % (n + 1, n + 1, big)), W("c2", "%d − %d = %d" % (big, small, D))))
    else:
        say_t, ops_t = times_parts(n + 1, n + 1, "m")
        ans = "%d × %d = %d" % (n + 1, n + 1, big)
        beats.append(B("But the question asks about the larger square. Its side is 1 more: %d plus 1 is %d." % (n, n + 1),
                       W("l3", "%d + 1 = %d" % (n, n + 1))))
        beats.append(B("So the larger square holds %d times %d. %s" % (n + 1, n + 1, say_t), *ops_t))
        beats.append(B(ending, ANS("a", ans), CIRC("a", str(big))))
        beats.append(B("Check: the smaller square is %d times %d, which is %d. And %d minus %d is %d, just as the story says." % (n, n, small, big, small, D),
                       W("c1", "%d × %d = %d" % (n, n, small)), W("c2", "%d − %d = %d" % (big, small, D))))
    beats.append(B(trap_say))
    beats.append(B(pick(qid, "sum", [
        "So the jump from one square to the next is always a row, a column and 1 corner. Take off the 1, halve, and you have the side.",
        "So remember how squares grow: a row, a column and 1 corner. Take the corner off the extra, halve what is left, and that is the side.",
        "So when you are told the gap between two squares that are neighbours: take away 1 for the corner, halve, and you have the smaller side.",
    ])))
    return LESSON(*beats)


LESSONS[P + "0095ccb9-0d88-44c3-9fdb-b29654aa1edc"] = next_sq(
    P + "0095ccb9-0d88-44c3-9fdb-b29654aa1edc",
    "Priya and her friends have diyas in a perfect square. With 57 more diyas, they could rearrange them all into the next larger perfect square. How many diyas do they have now?",
    "A square of diyas + 57 more = the next larger square",
    57, "diyas", "small",
    "They started with 784 diyas. And the side, 28, is more than 10, just as the question said.",
    "Careful: 841 is among the choices too, but that is the bigger square. The question asks how many they had to begin with.")

LESSONS[P + "6bbe6abc-c0c0-42b4-926a-2a31c04afbf5"] = next_sq(
    P + "6bbe6abc-c0c0-42b4-926a-2a31c04afbf5",
    "Ravi has tiles in a perfect square. He says that with 39 more tiles, he can make the next bigger perfect square. How many tiles does he have now?",
    "A square of tiles + 39 more = the next bigger square",
    39, "tiles", "small",
    "Ravi has 361 tiles now.",
    "Careful: 400 is among the choices too, but that is the bigger square Ravi is dreaming of. The question asks what he has now.")

LESSONS[P + "8328bb29-7e38-4413-80dd-d3d06b4adf46"] = next_sq(
    P + "8328bb29-7e38-4413-80dd-d3d06b4adf46",
    "Arjun makes a perfect square of diyas. Then he adds 45 more diyas and has the next bigger perfect square. How many diyas were in the first square?",
    "First square of diyas + 45 more = the next bigger square",
    45, "diyas", "small",
    "The first square had 484 diyas.",
    "Careful: 529 is among the choices too, but that is the second square. The question asks about the first.")

LESSONS[P + "ce55588b-dcc6-4b9b-8e0d-ebec13105471"] = next_sq(
    P + "ce55588b-dcc6-4b9b-8e0d-ebec13105471",
    "Priya has diyas arranged in a square. With 45 more diyas, she can form the next bigger perfect square. How many diyas does she have now?",
    "A square of diyas + 45 more = the next bigger square",
    45, "diyas", "small",
    "Priya has 484 diyas now.",
    "Two traps to name. 529 is the bigger square, not the one she has. And 22 is only the side: the question asks for all the diyas, so we had to square it.")

LESSONS[P + "9810a55e-70aa-440c-be5c-b09ea5a517f9"] = next_sq(
    P + "9810a55e-70aa-440c-be5c-b09ea5a517f9",
    "Priya goes from one perfect square of diyas to the very next one, and needs exactly 45 extra diyas to do it. How many diyas are in the larger square?",
    "Smaller square of diyas + 45 more = the next square",
    45, "diyas", "large",
    "The larger square has 529 diyas.",
    "Careful: 484 is among the choices too, but that is the smaller square. Always look back at which square the question asks for.")
