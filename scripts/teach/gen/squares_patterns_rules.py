"""Rules for the generated squares-patterns families: one lesson per wording.

Each rule takes a question and returns a list of beats, or None if the wording
is not its own. Every number is computed here; phrasing varies by a stable hash
of the question id.
"""
import re

from squares_patterns_lib import (
    answer, beat, both, choose, divide, given, grid, jumps, mark, note, pick, ring,
    seq_text, strike, table, times_split, W, words,
)


def option_numbers(q):
    out = []
    for o in q.get("options", []):
        text = o.get("text", "") if isinstance(o, dict) else str(o)
        if re.fullmatch(r"\d+", text.strip()):
            out.append(int(text))
    return out


# ── If √x + a = b, find x ────────────────────────────────────────────────────

ROOT_EQ = re.compile(r"^If √x \+ (\d+) = (\d+), find x\.$")


def root_equation(q):
    m = ROOT_EQ.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b = int(m.group(1)), int(m.group(2))
    r = b - a
    x = r * r
    beats = []
    beats.append(beat(pick(qid, "open", [
        "Here is our puzzle. The square root of x, plus %d, equals %d. We are hunting for x, the number hiding under the root sign." % (a, b),
        "Look at this one. The square root of x, plus %d, makes %d. Our job is to find x itself." % (a, b),
        "Let's read it together. The square root of x, plus %d, equals %d. Under that root sign sits x, and we want it." % (a, b),
    ]), given("l1", "√x + %d = %d" % (a, b))))
    beats.append(beat(pick(qid, "ask1", [
        "Think of the square root of x as one closed box. The box plus %d makes %d. So what do we clear away first?" % (a, b),
        "The root of x is not alone on the left. Something is sitting next to it. What should we move out of the way first?",
        "Before we touch the root sign, we want the root of x standing by itself. What is in its way?",
    ]), ask=choose("the + %d" % a, ["the root sign", "the %d" % b],
                   "Look at the left side again. The root of x has a plus %d hanging on to it. That goes first, and the root sign waits until the end." % a)))
    beats.append(beat(pick(qid, "undo", [
        "To undo plus %d, we take away %d. And to keep the balance level, we take it from both sides." % (a, a),
        "Plus %d is undone by minus %d. Whatever we do on the left, we do on the right as well." % (a, a),
        "So we subtract %d. Both sides, remember, or the balance tips." % a,
    ]), strike("l1", "+ %d" % a, "− %d" % a), both("l1", "− %d" % a)))
    beats.append(beat(pick(qid, "left", [
        "On the left, only the root of x is left. On the right, %d minus %d is %d." % (b, a, r),
        "Now the root of x stands alone. And %d minus %d gives us %d." % (b, a, r),
    ]), W("l2", "√x = %d − %d" % (b, a)), W("l3", "√x = %d" % r)))
    beats.append(beat(pick(qid, "trap", [
        "Careful, this is where many people stop! %d is the square root of x, not x. So how do we get x from %d?" % (r, r),
        "Now the trap. We have found the square root of x, and that is %d. We have not found x yet! What undoes a square root?" % r,
        "Don't put your pencil down yet. %d is only the root of x. Which sum takes us from the root back to x?" % r,
    ]), mark("l3", "√x", "box"),
        ask=choose("%d × %d" % (r, r), ["%d × 2" % r, "%d ÷ 2" % r],
                   "A square root is the number that multiplies by itself to make x. So we go back the other way: x is %d times %d, not %d times 2." % (r, r, r))))
    if r <= 12:
        beats.append(beat(pick(qid, "tiles", [
            "Picture a square of tiles, %d rows with %d tiles in each row. The side of the square is the root. All the tiles together are x." % (r, r),
            "Here is why. Build a square with %d rows of %d tiles. Its side is the square root, and the number of tiles in it is x." % (r, r),
        ]), grid("f1", r), W("l4", "x = %d × %d" % (r, r))))
    else:
        beats.append(beat(
            "Think of a big square of tiles, %d along each side. The side is the root, and all the tiles together are x. So x is %d times %d." % (r, r, r),
            W("l4", "x = %d × %d" % (r, r))))
    if r <= 10:
        beats.append(beat(pick(qid, "ans", [
            "%d times %d is %d. So x is %d. There is our hidden number!" % (r, r, x, x),
            "From our tables, %d times %d is %d. So x equals %d." % (r, r, x, x),
            "%d rows of %d makes %d tiles. So x is %d." % (r, r, x, x),
        ]), answer("l5", "x = %d" % x), ring("l5", "x = %d" % x)))
    else:
        tens, ones, p1, p2 = times_split(r)
        beats.append(beat(
            "%d times %d is a big one, so we split it. %d times 10 is %d, and %d times %d is %d." % (r, r, r, p1, r, ones, p2),
            W("l4b", "%d × %d = %d + %d" % (r, r, p1, p2))))
        beats.append(beat(pick(qid, "ans", [
            "%d plus %d is %d. So x is %d. There is our hidden number!" % (p1, p2, x, x),
            "Add them up: %d plus %d makes %d. So x equals %d." % (p1, p2, x, x),
        ]), answer("l5", "x = %d" % x), ring("l5", "x = %d" % x)))
    beats.append(beat(pick(qid, "check", [
        "Let's check it. The square root of %d is %d, and %d plus %d is %d. It fits perfectly." % (x, r, r, a, b),
        "Good mathematicians always check. Put %d in place of x: its square root is %d, and %d plus %d is %d. It works." % (x, r, r, a, b),
    ]), W("l6", "√%d + %d = %d" % (x, a, b))))
    beats.append(beat(pick(qid, "sum", [
        "So the plan for a puzzle like this: first get the root on its own, then square it to find x.",
        "Remember the two steps. Clear away what is added, then multiply the root by itself.",
        "Two moves, in order: undo the plus, then undo the root by squaring. Your turn next!",
    ])))
    return beats, ("x", x)


# ── Solve: ax ± b = c ────────────────────────────────────────────────────────

LINEAR = re.compile(r"^Solve: (\d+)x ([−+-]) (\d+) = (\d+)$")


def linear_equation(q):
    m = LINEAR.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, sign, b, c = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    minus = sign != "+"
    mid = c + b if minus else c - b
    x = mid // a
    assert a * x == mid
    op_word, undo_word = ("minus", "add") if minus else ("plus", "take away")
    op_sym, undo_sym = ("−", "+") if minus else ("+", "−")
    eq = "%dx %s %d = %d" % (a, op_sym, b, c)
    beats = []
    beats.append(beat(pick(qid, "open", [
        "Here is our equation. %d x, %s %d, equals %d. A number is hiding behind that x, and we are going to find it." % (a, op_word, b, c),
        "Let's read it. %d x, %s %d, equals %d. Our job is to find out what x is." % (a, op_word, b, c),
    ]), given("l1", eq)))
    beats.append(beat(pick(qid, "ask1", [
        "Think of the equals sign as a balance. Whatever we do to one side, we do to the other. So, what is in the way of the %d x?" % a,
        "We want the %d x on its own first. What is sitting next to it, in the way?" % a,
    ]), ask=choose("the %s %d" % (op_sym, b), ["the %d" % c, "the %d in front of x" % a],
                   "Look at the left side once more. The %d x has a %s %d hanging on to it. That is the first thing to clear away." % (a, op_word, b))))
    beats.append(beat(
        "To undo %s %d, we %s %d. And to keep the balance level, we do it to both sides." % (op_word, b, undo_word, b),
        strike("l1", "%s %d" % (op_sym, b), "%s %d" % (undo_sym, b)), both("l1", "%s %d" % (undo_sym, b))))
    beats.append(beat(
        "On the left, the %s %d is gone. On the right, %d %s %d makes %d." % (op_word, b, c, "plus" if minus else "minus", b, mid),
        W("l2", "%dx = %d %s %d" % (a, c, undo_sym, b)), W("l3", "%dx = %d" % (a, mid))))
    beats.append(beat(pick(qid, "ask2", [
        "Nearly there. %d x means %d times x. What undoes times %d?" % (a, a, a),
        "Now, %d x is %d lots of x. How do we get back to just one x?" % (a, a),
    ]), ask=choose("divide by %d" % a, ["subtract %d" % a, "multiply by %d" % a],
                   "Times and divide are partners. Whatever times does, divide undoes. So to undo times %d, we divide by %d." % (a, a))))
    beats.append(beat("So we divide both sides by %d." % a, divide("l3", str(a))))
    beats.append(beat(pick(qid, "ans", [
        "%d divided by %d is %d. So x equals %d. There is our hidden number!" % (mid, a, x, x),
        "%d shared into %d equal parts gives %d each. So x is %d." % (mid, a, x, x),
    ]), answer("l4", "x = %d" % x), ring("l4", "x = %d" % x)))
    beats.append(beat(
        "Always check. Put %d back in place of x. %d times %d is %d, and %d %s %d is %d. It works." % (x, a, x, mid, mid, op_word, b, c),
        W("l5", "%d × %d %s %d = %d" % (a, x, op_sym, b, c))))
    beats.append(beat(pick(qid, "sum", [
        "So here is the plan for any equation like this. First clear away what is added or taken off. Then undo the times.",
        "Two steps, every time: deal with the number standing beside the x term first, then divide to free the x.",
    ])))
    return beats, ("x", x)


# ── Find the square of n ─────────────────────────────────────────────────────

SQUARE_OF = re.compile(r"^Find the square of (\d+)\.$")


def square_of(q):
    m = SQUARE_OF.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    n = int(m.group(1))
    sq = n * n
    beats = []
    beats.append(beat(pick(qid, "open", [
        "Our question: find the square of %d. Before we work it out, let's see why it is called a square." % n,
        "Find the square of %d. That little word, square, is a big clue. So let's draw one." % n,
        "We want the square of %d. It gets its name from a shape, so let's start with the shape." % n,
    ]), given("l1", "%d² = ?" % n)))
    if n <= 12:
        beats.append(beat(pick(qid, "tiles", [
            "Here is a square made of tiles. It has %d rows, and %d tiles in every row. The square of %d is the number of tiles in it." % (n, n, n),
            "Look at this square of tiles: %d rows, with %d tiles in each row. Count all the tiles, and you have the square of %d." % (n, n, n),
        ]), grid("f1", n)))
        beats.append(beat(
            pick(qid, "ask1", ["So which sum gives us the square of %d?" % n,
                               "Which sum counts all the tiles in that square?"]),
            ask=choose("%d × %d" % (n, n), ["%d × 2" % n, "%d + 2" % n],
                       "Look at the tiles. There are %d rows, and each row has %d tiles. That is %d lots of %d, so %d times %d." % (n, n, n, n, n, n))))
    else:
        beats.append(beat(
            "A %d by %d square is too big for our board, so here is a baby one: 3 rows of 3 tiles. 3 times 3 is 9 tiles, so the square of 3 is 9." % (n, n),
            grid("f1", 3), W("l2", "3² = 3 × 3 = 9")))
        beats.append(beat(
            "Our square is the same idea, only bigger: %d rows, with %d tiles in each row. So which sum gives the square of %d?" % (n, n, n),
            ask=choose("%d × %d" % (n, n), ["%d × 2" % n, "%d + 2" % n],
                       "Think of the square: %d rows, and %d tiles in every row. That is %d lots of %d, so %d times %d." % (n, n, n, n, n, n))))
    beats.append(beat(pick(qid, "trap", [
        "Here is the trap to dodge. The little 2 does not mean times 2. It means the number is written twice and multiplied.",
        "Careful with that little 2 up in the air. It never means times 2. It tells us to multiply the number by itself.",
    ]), W("l3", "%d² = %d × %d" % (n, n, n)), note("l1", "²", "not × 2", "above")))
    if n <= 10:
        beats.append(beat(
            pick(qid, "ask2", ["And what is %d times %d? Use your tables." % (n, n),
                               "So, %d lots of %d. What does that make?" % (n, n)]),
            ask=choose(str(sq), [str(2 * n), str(sq - 1)],
                       "Count up in lots of %d, %d times over. You land on %d." % (n, n, sq))))
        beats.append(beat(
            "%d times %d is %d. So the square of %d is %d." % (n, n, sq, n, sq),
            W("l4", "%d × %d = %d" % (n, n, sq)), answer("l5", "%d² = %d" % (n, sq)), ring("l5", str(sq))))
    else:
        tens, ones, p1, p2 = times_split(n)
        beats.append(beat(
            "%d times %d is not in our tables, so we break the second %d into %d and %d." % (n, n, n, tens, ones),
            W("l4", "%d × %d = %d × %d + %d × %d" % (n, n, n, tens, n, ones))))
        beats.append(beat(
            "%d times %d is %d. And %d times %d is %d. What do they make together?" % (n, tens, p1, n, ones, p2),
            W("l5", "%d × %d = %d + %d" % (n, n, p1, p2)),
            ask=choose(str(sq), [str(sq - 10), str(sq + 10)],
                       "Take it slowly. Add the ones first, then the tens, then the hundreds. %d plus %d comes to %d." % (p1, p2, sq))))
        beats.append(beat(
            "%d plus %d is %d. So the square of %d is %d." % (p1, p2, sq, n, sq),
            answer("l6", "%d² = %d" % (n, sq)), ring("l6", str(sq))))
    beats.append(beat(pick(qid, "check", [
        "And if we go backwards, the square root of %d brings us home to %d. Square and square root undo each other." % (sq, n),
        "A quick check, going backwards: the square root of %d is %d, because %d times %d is %d." % (sq, n, n, n, sq),
    ]), W("l7", "√%d = %d" % (sq, n))))
    beats.append(beat(pick(qid, "sum", [
        "So, to square a number, multiply it by itself. Never by 2!",
        "Remember: the square of a number is that number times itself, like the tiles in a square.",
    ])))
    return beats, None


# ── Find the square root of N ────────────────────────────────────────────────

ROOT_OF = re.compile(r"^Find the square root of (\d+)\.$")


def square_root(q):
    m = ROOT_OF.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    N = int(m.group(1))
    r = int(round(N ** 0.5))
    assert r * r == N
    l1 = "√%d = ?" % N
    beats = []
    beats.append(beat(pick(qid, "open", [
        "Find the square root of %d. First, let's be sure what that is asking." % N,
        "We want the square root of %d. Before we hunt for it, what does a square root mean?" % N,
    ]), given("l1", l1)))
    beats.append(beat(
        pick(qid, "ask1", ["What is a square root question really asking?",
                           "Which of these is the square root asking for?"]),
        ask=choose("which number × itself = %d" % N, ["what is half of %d" % N, "what is %d × %d" % (N, N)],
                   "A square root is not a half. It asks: which number, multiplied by itself, makes %d?" % N)))
    beats.append(beat(pick(qid, "boxes", [
        "Yes. The same number goes in both boxes: something times itself makes %d. Think of %d tiles laid out as a perfect square. How long is one side?" % (N, N),
        "So we need one number for both boxes. Picture %d tiles arranged in a perfect square: the square root is the length of its side." % N,
    ]), W("l2", "? × ? = %d" % N)))
    if r <= 10:
        k = r - 1
        beats.append(beat(
            "Let's test some numbers. %d times %d is %d. That is too small." % (k, k, k * k),
            W("l3", "%d × %d = %d" % (k, k, k * k))))
        beats.append(beat(
            "Too small, so we go one bigger. What is %d times %d?" % (r, r),
            ask=choose(str(N), [str(2 * r), str(r * (r + 1))],
                       "%d times %d means %d lots of %d. Count up in lots of %d and you land on %d." % (r, r, r, r, r, N))))
        beats.append(beat(
            "%d times %d is exactly %d. Look: %d tiles make a square with %d on each side." % (r, r, N, N, r),
            W("l4", "%d × %d = %d" % (r, r, N)), grid("f1", r)))
        beats.append(beat(
            "So the square root of %d is %d." % (N, r),
            answer("l5", "√%d = %d" % (N, r)), ring("l5", str(r), ("√%d = " % N).count(str(r)) + 1)))
        beats.append(beat(pick(qid, "sum", [
            "So for a square root, hunt for the number that multiplies by itself to make it. Your times tables do the rest.",
            "Remember: a square root is the side of the square. Find the number that, times itself, gives what you started with.",
        ])))
        return beats, None
    if r % 10 == 0:
        front, small = N // 100, r // 10
        beats.append(beat(
            "%d ends in two zeros. Cover them for a moment and we see %d. Which number, times itself, makes %d?" % (N, front, front),
            mark("l1", "00"),
            ask=choose(str(small), [str(small + 1), str(small - 1)],
                       "Try your tables: %d times %d is %d." % (small, small, front))))
        beats.append(beat(
            "%d times %d is %d. So %d tens times %d tens is %d hundreds: %d times %d is %d." % (small, small, front, small, small, front, r, r, N),
            W("l3", "%d × %d = %d" % (small, small, front)), W("l4", "%d × %d = %d" % (r, r, N))))
        beats.append(beat(
            "So the square root of %d is %d. There it is!" % (N, r),
            answer("l5", "√%d = %d" % (N, r)), ring("l5", str(r))))
        beats.append(beat(
            "Picture it: %d rows with %d tiles in each row is %d tiles. A perfect square." % (r, r, N)))
        beats.append(beat(
            "So when a number ends in two zeros, find the root of the front part, then put one zero back."))
        return beats, None
    t = (r // 10) * 10
    lo, hi = t * t, (t + 10) * (t + 10)
    beats.append(beat(
        "%d is too big for our tables, so we trap it between two squares we know. %d times %d is %d. %d times %d is %d." % (N, t, t, lo, t + 10, t + 10, hi),
        W("l3", "%d × %d = %d" % (t, t, lo)), W("l4", "%d × %d = %d" % (t + 10, t + 10, hi))))
    beats.append(beat(
        "%d sits between %d and %d. So where is our number?" % (N, lo, hi),
        ask=choose("between %d and %d" % (t, t + 10), ["between %d and %d" % (t - 10, t), "between %d and %d" % (t + 10, t + 20)],
                   "Look at the two lines. %d is more than %d and less than %d. So its root is more than %d and less than %d." % (N, lo, hi, t, t + 10))))
    d = N % 10
    ends = [e for e in range(1, 10) if (e * e) % 10 == d]
    last = mark("l1", str(d), "underline", l1.count(str(d)))
    if len(ends) == 1:
        e = ends[0]
        beats.append(beat(
            "Now the clever clue: the last digit. %d ends in %d, and only a number ending in %d has a square ending in %d. Between %d and %d that leaves just %d." % (N, d, e, d, t, t + 10, r),
            last, words("l5", "ends in %d, so try %d" % (e, r))))
    else:
        e1, e2 = ends
        c1, c2 = t + e1, t + e2
        other = c2 if r == c1 else c1
        near_lo = (N - lo) < (hi - N)
        assert (r == c1) == near_lo
        beats.append(beat(
            "Now the clever clue: the last digit. %d ends in %d. %d times %d is %d, and %d times %d is %d: both end in %d." % (N, d, e1, e1, e1 * e1, e2, e2, e2 * e2, d),
            last, W("l5", "%d × %d = %d" % (e1, e1, e1 * e1)), W("l6", "%d × %d = %d" % (e2, e2, e2 * e2))))
        beats.append(beat(
            "So our number ends in %d or %d: it is %d or %d. Now, %d is closer to %d than to %d. Which one shall we try?" % (
                e1, e2, c1, c2, N, lo if near_lo else hi, hi if near_lo else lo),
            words("l7", "%d or %d" % (c1, c2)),
            ask=choose(str(r), [str(other)],
                       "%d is the square of %d, and %d is close to it. So we want the one nearer to %d, and that is %d." % (
                           lo if near_lo else hi, t if near_lo else t + 10, N, t if near_lo else t + 10, r))))
    tens, ones, p1, p2 = times_split(r)
    beats.append(beat(
        "Let's test %d. Break the second %d into %d and %d. %d times %d is %d, and %d times %d is %d." % (r, r, tens, ones, r, tens, p1, r, ones, p2),
        W("l8", "%d × %d = %d × %d + %d × %d" % (r, r, r, tens, r, ones)),
        W("l9", "%d × %d = %d + %d" % (r, r, p1, p2))))
    beats.append(beat(
        "%d plus %d is %d. That is our number exactly!" % (p1, p2, N),
        W("l10", "%d × %d = %d" % (r, r, N))))
    beats.append(beat(
        "So the square root of %d is %d." % (N, r),
        answer("l11", "√%d = %d" % (N, r)), ring("l11", str(r), ("√%d = " % N).count(str(r)) + 1)))
    beats.append(beat(pick(qid, "sum", [
        "So for a big square root: trap it between two tens, let the last digit pick the candidates, then multiply to make sure.",
        "That is the plan every time: squeeze it between two tens, read the last digit, and test your best guess by multiplying.",
    ])))
    return beats, None


# ── Which of the following is a perfect square? (generated wording) ──────────

def which_perfect_square(q):
    if q["questionText"].strip() != "Which of the following is a perfect square?":
        return None
    opts = option_numbers(q)
    if len(opts) != 4:
        return None
    key = opts["ABCD".index(q["correctAnswer"])]
    k = int(round(key ** 0.5))
    if k * k != key or k > 12 or k < 4:
        return None
    rest = [o for o in opts if o != key]
    if not all(key < o < (k + 1) * (k + 1) for o in rest):
        return None
    listing = "%d, %d, %d or %d" % tuple(opts)
    beats = []
    beats.append(beat(
        "Which of these is a perfect square: %s? Let's remember what a perfect square is first." % listing,
        given("l1", "Perfect square: %s?" % listing, True)))
    beats.append(beat(
        "A perfect square is a number of tiles that makes a full square, with nothing left over. Like 9 tiles, in 3 rows of 3.",
        grid("f1", 3), W("l2", "3 × 3 = 9")))
    beats.append(beat(
        "Let's walk up the squares until we reach our numbers. %d times %d is %d: too small." % (
            k - 1, k - 1, (k - 1) * (k - 1)),
        W("l3", "%d × %d = %d" % (k - 1, k - 1, (k - 1) * (k - 1)))))
    beats.append(beat(
        "The next square is %d times %d. What does that make?" % (k, k),
        W("l3b", "%d × %d = ?" % (k, k)),
        ask=choose(str(key), [str(key - 10), str(2 * k)],
                   "%d times %d is %d lots of %d. From the %d times table, that is %d." % (k, k, k, k, k, key))))
    beats.append(beat(
        "%d times %d is %d, and there it is in our list! %d tiles make a square with %d on each side." % (k, k, key, key, k),
        note("l3b", "?", str(key), "above"), grid("f2", k), mark("l1", str(key))))
    beats.append(beat(
        "What about the others? The very next square is %d times %d, which is %d. So %d, %d and %d are stuck in the gap between two squares." % (
            k + 1, k + 1, (k + 1) * (k + 1), rest[0], rest[1], rest[2]),
        W("l5", "%d × %d = %d" % (k + 1, k + 1, (k + 1) * (k + 1)))))
    beats.append(beat(
        "So the perfect square is %d." % key,
        answer("l6", "%d = %d × %d" % (key, k, k)), ring("l6", str(key))))
    beats.append(beat(
        "To test for a perfect square, walk up the squares and see whether you land exactly on the number."))
    return beats, None


# ── Sequences (generated wordings) ───────────────────────────────────────────

def ordinal(n):
    if 10 <= n % 100 <= 20:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def term_nth(terms, i):
    """Which occurrence of str(terms[i]) in the comma list is the i-th term itself."""
    prefix = ", ".join(str(t) for t in terms[:i])
    return prefix.count(str(terms[i])) + 1


NTH_TERM = re.compile(r"^In an arithmetic sequence starting (\d+), (\d+), (\d+), \.\.\., find the (\d+)(?:st|nd|rd|th) term\.$")


def nth_term(q):
    m = NTH_TERM.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b, c, n = [int(g) for g in m.groups()]
    d = b - a
    assert c - b == d and d > 0
    hops = n - 1
    total = hops * d
    ans = a + total
    nth = ordinal(n)
    beats = []
    beats.append(beat(pick(qid, "open", [
        "Here is our sequence: %d, %d, %d, and on it goes. We want the %s term, far down the line." % (a, b, c, nth),
        "The numbers start %d, %d, %d, and keep going. Our job is to find the %s one without writing them all out." % (a, b, c, nth),
    ]), given("l1", seq_text([a, b, c], "…"), True)))
    beats.append(beat(
        pick(qid, "ask1", ["First, see how it grows. What is the jump from each number to the next?",
                           "Look at two neighbours at a time. What do we add to get from one to the next?"]),
        ask=choose("+ %d" % d, ["+ %d" % (d + 1), "+ %d" % (d - 1)],
                   "Subtract neighbours: %d minus %d is %d, and %d minus %d is %d again. So the jump is plus %d." % (b, a, d, c, b, d, d))))
    beats.append(beat(
        "Plus %d, every single time. A sequence that climbs by the same jump each time is called an arithmetic sequence." % d,
        jumps("l1", ["+%d" % d, "+%d" % d])))
    beats.append(beat(
        "We can't write out all %d terms, so let's count jumps instead. The 2nd term is 1 jump from the start. The 3rd term is 2 jumps." % n,
        table("f1", ["Term", "Jumps from start"], [["1st", "0"], ["2nd", "1"], ["3rd", "2"], ["4th", "3"]])))
    beats.append(beat(
        "See the pattern in the table? So how many jumps take us to the %s term?" % nth,
        ask=choose(str(hops), [str(n), str(n + 1)],
                   "Look at the table again. The jumps are always 1 fewer than the term number, because the 1st term needs no jump at all. So the %s term needs %d jumps." % (nth, hops))))
    if hops <= 10 or d <= 2:
        beats.append(beat(
            "%d jumps, and each jump is %d. %d times %d is %d." % (hops, d, hops, d, total),
            W("l2", "%d × %d = %d" % (hops, d, total))))
    else:
        beats.append(beat(
            "%d jumps of %d each. A quick way: %d times %d is %d, and one jump fewer is %d." % (hops, d, n, d, n * d, total),
            W("l2", "%d × %d = %d" % (n, d, n * d)), W("l3", "%d × %d = %d − %d = %d" % (hops, d, n * d, d, total))))
    beats.append(beat(
        "Now start at %d, the first term, and add all those jumps. %d plus %d is %d. So the %s term is %d." % (a, a, total, ans, nth, ans),
        W("l4", "%d + %d = %d" % (a, total, ans)), answer("l5", "%s term = %d" % (nth, ans), True),
        ring("l5", str(ans), ("%s term = " % nth).count(str(ans)) + 1)))
    beats.append(beat(
        "Let's test the idea on a term we already know. The 3rd term is 2 jumps from %d: %d plus 2 times %d is %d. And %d is right there in our list." % (a, a, d, c, c),
        W("l6", "%d + 2 × %d = %d" % (a, d, c)), mark("l1", str(c), "underline", term_nth([a, b, c], 2))))
    beats.append(beat(pick(qid, "sum", [
        "So for a far away term: find the jump, use one fewer jumps than the term number, and add them to the first term.",
        "The plan: find the jump, count the jumps, which is always 1 fewer than the term number, multiply, then add the first term.",
    ])))
    return beats, None


NEXT_NUMBER = re.compile(r"^Find the next number(?: in the sequence)?: ([\d, ]+), \?$")


def next_number(q):
    m = NEXT_NUMBER.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    terms = [int(t) for t in m.group(1).split(",")]
    gaps = [y - x for x, y in zip(terms, terms[1:])]
    last = terms[-1]
    line = seq_text(terms, "?")
    said = ", ".join(str(t) for t in terms)
    beats = []
    beats.append(beat(pick(qid, "open", [
        "Here is a line of numbers: %s, and then a gap. We need the number that comes next." % said,
        "Look at this pattern: %s. Something comes next, and the numbers themselves will tell us what." % said,
    ]), given("l1", line, True)))
    if len(set(gaps)) == 1:
        d = gaps[0]
        nxt = last + d
        beats.append(beat(
            "Look at two neighbours at a time. What is the jump from each number to the next?",
            ask=choose("+ %d" % d, ["+ %d" % (d + 1), "× 2"],
                       "From %d to %d is %d more. From %d to %d is %d more again. The jump is plus %d." % (terms[0], terms[1], d, terms[1], terms[2], d, d))))
        beats.append(beat(
            "Plus %d, plus %d, plus %d, all the way along. The jump never changes." % (d, d, d),
            jumps("l1", ["+%d" % d] * len(gaps))))
        beats.append(beat(
            "The last number we have is %d. So what comes next?" % last,
            ask=choose(str(nxt), [str(last + 1), str(last * 2)],
                       "Keep the very same jump. Start at %d and go up %d more." % (last, d))))
        beats.append(beat(
            "%d plus %d is %d. So the next number is %d." % (last, d, nxt, nxt),
            answer("l2", "%d + %d = %d" % (last, d, nxt)), ring("l2", str(nxt), ("%d + %d = " % (last, d)).count(str(nxt)) + 1),
            note("l1", "?", str(nxt), "above")))
        beats.append(beat(
            "Read the whole line back: %s, %d. Every step is plus %d. It fits." % (said, nxt, d),
            words("l3", seq_text(terms + [nxt]))))
        beats.append(beat(
            "For any number pattern, look at the jumps between neighbours first. If they are all the same, make that jump once more."))
        return beats, None
    ratio = terms[1] // terms[0]
    if not all(y == x * ratio for x, y in zip(terms, terms[1:])) or ratio != 2:
        return None
    nxt = last * ratio
    beats.append(beat(
        "Let's write the jumps underneath. " + " ".join(
            "From %d to %d is plus %d." % (x, y, y - x) for x, y in zip(terms, terms[1:])),
        jumps("l1", ["+%d" % g for g in gaps])))
    beats.append(beat(
        "The jumps are not the same: they keep growing. So adding is not the rule. What takes each number to the next one?",
        ask=choose("× 2", ["+ %d" % gaps[0], "× 3"],
                   "Adding the same amount does not work here, because the jumps change. But double each number and you get the next one, every time.")))
    shown = list(zip(terms, terms[1:]))[:3]
    beats.append(beat(
        "Each number is double the one before it. " + " ".join("%d times 2 is %d." % (x, y) for x, y in shown),
        [W("m%d" % i, "%d × 2 = %d" % (x, y)) for i, (x, y) in enumerate(shown)]))
    beats.append(beat(
        "So what comes after %d?" % last,
        ask=choose(str(nxt), [str(last + gaps[-1]), str(nxt + 1)],
                   "Don't add the last jump again. The rule is double, so we double %d." % last)))
    beats.append(beat(
        "%d times 2 is %d. So the next number is %d." % (last, nxt, nxt),
        answer("l2", "%d × 2 = %d" % (last, nxt)), ring("l2", str(nxt)), note("l1", "?", str(nxt), "above")))
    beats.append(beat(
        "Read it back: %s, %d. Each one is double the one before. It fits." % (said, nxt),
        words("l3", seq_text(terms + [nxt]))))
    beats.append(beat(
        "So when the jumps keep growing, try multiplying instead of adding."))
    return beats, None


SERIES_SUM = re.compile(r"^Find the sum of the arithmetic series: (\d+), (\d+), (\d+), \.\.\., (\d+)\.$")


def series_sum(q):
    m = SERIES_SUM.match(q["questionText"].strip())
    if not m:
        return None
    qid = q["id"]
    a, b, c, last = [int(g) for g in m.groups()]
    d = b - a
    climb = last - a
    assert c - b == d and climb % d == 0
    hops = climb // d
    n = hops + 1
    pair = a + last
    twice = n * pair
    assert twice % 2 == 0
    total = twice // 2
    s3 = a + b + c
    beats = []
    beats.append(beat(pick(qid, "open", [
        "We need to add up %d, %d, %d, and so on, all the way to %d. One by one would take ages, so let's be clever." % (a, b, c, last),
        "Add %d, %d, %d, and every number in the pattern up to %d. That is a long sum, so we will look for a short cut." % (a, b, c, last),
    ]), given("l1", seq_text([a, b, c], "…, %d" % last), True)))
    beats.append(beat(
        "First, the jump. %d minus %d is %d, and %d minus %d is %d. So the numbers climb by %d each time." % (b, a, d, c, b, d, d),
        jumps("l1", ["+%d" % d, "+%d" % d])))
    beats.append(beat(
        "How many numbers are in the list? From %d up to %d is a climb of %d. In jumps of %d, that is %d jumps." % (a, last, climb, d, hops),
        W("l2", "%d − %d = %d" % (last, a, climb)), W("l3", "%d ÷ %d = %d" % (climb, d, hops))))
    beats.append(beat(
        "%d jumps. So how many numbers are there?" % hops,
        ask=choose(str(n), [str(hops), str(hops - 1)],
                   "Think of fence posts. 1 jump joins 2 numbers, and 2 jumps join 3 numbers. There is always 1 more number than jumps.")))
    beats.append(beat(
        "1 more than the jumps: %d numbers in all." % n,
        W("l4", "%d + 1 = %d" % (hops, n))))
    beats.append(beat(
        "Now the clever bit. Add the first and the last: %d plus %d is %d. Then the second and the second last: %d plus %d is %d again!" % (
            a, last, pair, b, last - d, pair),
        W("l5", "%d + %d = %d" % (a, last, pair)), W("l6", "%d + %d = %d" % (b, last - d, pair))))
    beats.append(beat(
        "Every pair makes %d. So write the list twice, once forwards and once backwards, and we get %d pairs of %d. %d times %d is %d." % (
            pair, n, pair, n, pair, twice),
        W("l7", "%d × %d = %d" % (n, pair, twice))))
    beats.append(beat(
        "But %d has every number counted twice. What do we do to get the real sum?" % twice,
        ask=choose("halve it", ["double it", "keep %d" % twice],
                   "We wrote the list two times, so %d is double the sum. Halving it brings us back." % twice)))
    beats.append(beat(
        "Half of %d is %d. So the sum is %d." % (twice, total, total),
        W("l8", "%d ÷ 2 = %d" % (twice, total)), answer("l9", "Sum = %d" % total, True), ring("l9", str(total))))
    beats.append(beat(
        "Does the trick really work? Try just the first 3 numbers. %d plus %d plus %d is %d. The trick says: %d plus %d is %d, times 3, then halved. That is %d too." % (
            a, b, c, s3, a, c, a + c, s3),
        W("l10", "%d + %d + %d = %d" % (a, b, c, s3)), W("l11", "3 × %d ÷ 2 = %d" % (a + c, s3))))
    beats.append(beat(pick(qid, "sum", [
        "So, to add a long, evenly spaced list: count the numbers, add the first and the last, multiply, and halve.",
        "The short cut: how many numbers, times first plus last, then halve. Just remember to count the numbers, not the jumps.",
    ])))
    return beats, None


RULES = [root_equation, linear_equation, square_of, square_root, which_perfect_square,
         nth_term, next_number, series_sum]
