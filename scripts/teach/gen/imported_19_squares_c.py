"""Square numbers: putting numbers in for letters (x² + y², (x + y)², (x − y)², x² − y²)."""
from imported_19_lib import ANSR, B, L, M, N, S, W, GIVEN, choose, lesson, pick

LESSONS = {}
P = "IPMTB_grade5_ch04_q"


def squared_line(v):
    return "%d² = %d × %d = %d" % (v, v, v, v * v)


# ── x² + y² and x² − y²: square each, then add or subtract ───────────────────

def two_squares(qid, x, y, sign, ask_about):
    """sign '+' or '−'. ask_about: 'x' or 'y', the letter whose square the child is asked about."""
    plus = sign == "+"
    word = "plus" if plus else "minus"
    result = x * x + y * y if plus else x * x - y * y
    inner = x + y if plus else x - y
    told, told_v = ("x", x) if ask_about == "y" else ("y", y)
    asked, asked_v = ("y", y) if ask_about == "y" else ("x", x)
    expr = "x² %s y²" % sign
    numbers = "%d² %s %d²" % (x, sign, y)
    after = "Not %d!" % (asked_v * 2) if asked_v * 2 != asked_v * asked_v else ""
    return lesson(
        B(pick(qid, "open", [
            "We are told that x is %d and y is %d. We want x squared %s y squared." % (x, y, word),
            "Here x is %d and y is %d, and we need the value of x squared %s y squared." % (x, y, word)]),
          GIVEN("q", "x = %d, y = %d. Find %s" % (x, y, expr))),
        B("A letter is just a box with a number inside. So put the numbers in. Where x was, write %d. Where y was, write %d." % (x, y),
          W("w1", numbers), N("w1", "%d²" % x, "x²"), N("w1", "%d²" % y, "y²", "below", 2 if x == y else None)),
        B("Now, which comes first: squaring each number, or working out %d %s %d?" % (x, word, y),
          ask=choose(["%d %s %d first" % (x, sign, y), "square each number first"], 1,
                     "Look where the little 2 sits: on the x alone, and on the y alone. There is no bracket joining them, so each one is squared first.")),
        B("Each one is squared first. Start with %s. %d squared is %d times %d, which is %d." % (told, told_v, told_v, told_v, told_v * told_v),
          W("w2", squared_line(told_v))),
        B("Now %s. What does %d squared mean?" % (asked, asked_v),
          ask=choose(["%d × 2" % asked_v, "%d × %d" % (asked_v, asked_v), "%d + 2" % asked_v], 1,
                     "The little 2 does not mean times 2. It tells us to multiply the number by itself.")),
        B(("%d times %d is %d. %s" % (asked_v, asked_v, asked_v * asked_v, after)).strip(),
          W("w3", squared_line(asked_v))),
        B("Now %s. %d %s %d is %d." % ("add the two squares" if plus else "take y squared away from x squared", x * x, word, y * y, result),
          W("w4", "%d %s %d = %d" % (x * x, sign, y * y, result)),
          ANSR("a", "%s = %d" % (expr, result), str(result), True)),
        B("The trap is to do %d %s %d first, and then square. That gives %d squared, which is %d. It would only be right with a bracket round x %s y." % (x, word, y, inner, inner * inner, word),
          W("t", "(%d %s %d)² = %d" % (x, sign, y, inner * inner)), N("t", "(%d %s %d)²" % (x, sign, y), "a different sum")),
        B("So: put the numbers in, square each one, and only then %s." % ("add" if plus else "subtract")),
    )


LESSONS[P + "014"] = two_squares(P + "014", 2, 1, "+", "y")
LESSONS[P + "032"] = two_squares(P + "032", 2, 3, "+", "y")
LESSONS[P + "035"] = two_squares(P + "035", 4, 2, "−", "x")


# ── (x + y)² and (x − y)²: the bracket first, then square ────────────────────

def bracket_squared(qid, x, y, sign):
    plus = sign == "+"
    word = "plus" if plus else "minus"
    r = x + y if plus else x - y
    apart = x * x + y * y if plus else x * x - y * y
    expr = "(x %s y)²" % sign
    choices = [str(r * 2), str(r * r)] if r * 2 != r * r else [str(r + 2), str(r * r)]
    if r == 1:
        said = "1. 1 squared is 1 times 1, and that is just 1."
    else:
        said = "%d. %d squared is %d times %d." % (r * r, r, r, r)
    return lesson(
        B(pick(qid, "open", [
            "We are told that x is %d and y is %d. We want x %s y, all squared." % (x, y, word),
            "Here x is %d and y is %d. We need the value of x %s y, all squared." % (x, y, word)]),
          GIVEN("q", "x = %d, y = %d. Find %s" % (x, y, expr))),
        B("A letter is just a box with a number inside. So put the numbers in. Where x was, write %d. Where y was, write %d." % (x, y),
          W("w1", "(%d %s %d)²" % (x, sign, y))),
        B("There is a bracket, with a little 2 sitting outside it. What do we do first?",
          M("w1", "(%d %s %d)" % (x, sign, y), "box"),
          ask=choose(["square %d and square %d" % (x, y), "work out the bracket"], 1,
                     "The little 2 is outside the bracket, so it squares everything inside together. Brackets always come first.")),
        B("The bracket first. %d %s %d is %d." % (x, word, y, r),
          W("w2", "%d %s %d = %d" % (x, sign, y, r))),
        B("So now we have %d squared. What is that?" % r,
          W("w3", "%d²" % r),
          ask=choose(choices, 1,
                     "Squared means the number is multiplied by itself. It does not mean times 2.")),
        B(said,
          W("w4", squared_line(r)), ANSR("a", "%s = %d" % (expr, r * r), str(r * r), True)),
        B("The trap is to square each number on its own. %d squared %s %d squared is %d %s %d, which is %d. That is a different sum, with no bracket." % (x, word, y, x * x, word, y * y, apart),
          W("t", "%d² %s %d² = %d %s %d = %d" % (x, sign, y, x * x, sign, y * y, apart)),
          N("t", "%d² %s %d²" % (x, sign, y), "a different sum")),
        B("So: numbers in, bracket first, then square."),
    )


LESSONS[P + "015"] = bracket_squared(P + "015", 3, 2, "+")
LESSONS[P + "033"] = bracket_squared(P + "033", 1, 4, "+")
LESSONS[P + "016"] = bracket_squared(P + "016", 5, 2, "−")
LESSONS[P + "034"] = bracket_squared(P + "034", 3, 2, "−")

# ── (x − y) = 4: square the whole bracket ────────────────────────────────────

LESSONS[P + "036"] = lesson(
    B("We are told that x minus y is 4. We want x minus y, all squared.",
      GIVEN("q", "(x − y) = 4. Find (x − y)²")),
    B("We are not told x, and we are not told y. Do we need to know them?",
      ask=choose(["Yes: find x and y first", "No: we know the whole bracket"], 1,
                 "Look at what is being squared: the whole bracket, x minus y. And the question tells us what that bracket is worth.")),
    B("We do not. The bracket x minus y is worth 4. So where we see that bracket, we can write 4.",
      M("q", "(x − y)", "box", 2), L("w1", "(x − y)² = 4²")),
    B("So what is 4 squared?",
      ask=choose(["8", "4", "16"], 2,
                 "Squared means the number is multiplied by itself. Not times 2, and not left as it is.")),
    B("4 times 4 is 16.",
      W("w2", "4² = 4 × 4 = 16"), ANSR("a", "(x − y)² = 16", "16", True)),
    B("Test it with real numbers. Say x is 7 and y is 3. 7 minus 3 is 4, and 4 squared is 16.",
      W("c1", "(7 − 3)² = 16")),
    B("Or say x is 5 and y is 1. Again 5 minus 1 is 4, and we get 16. It does not matter which numbers hide inside.",
      W("c2", "(5 − 1)² = 16")),
    B("Two traps: 8 comes from doubling, and 4 from forgetting to square. When you know what a whole bracket is worth, just use it."),
)

# ── The square of x² + y² ────────────────────────────────────────────────────

LESSONS[P + "022"] = lesson(
    B("We are told x is 6 and y is 8. We want the square of x squared plus y squared.",
      GIVEN("q", "x = 6, y = 8. Find the square of x² + y²")),
    B("Read that slowly, because there are two jobs. First find x squared plus y squared. Then square that whole answer.",
      L("j1", "Job 1: x² + y²"), L("j2", "Job 2: square the result")),
    B("Job 1. x is 6, so x squared is 6 times 6, which is 36. y is 8, so y squared is 8 times 8, which is 64.",
      W("w1", "6² = 6 × 6 = 36"), W("w2", "8² = 8 × 8 = 64")),
    B("Now add them. What is 36 plus 64?",
      ask=choose(["90", "100", "110"], 1,
                 "Add the units first: 6 and 4 make 10. Then add the tens, and do not forget the ten you just made.")),
    B("100. A lovely round number. That is job 1 done.",
      W("w3", "36 + 64 = 100"), S("j1", "Job 1: x² + y²", "done")),
    B("So, are we finished?",
      ask=choose(["Yes: the answer is 100", "No: now square the 100"], 1,
                 "Look back at the question. It asks for the square of x squared plus y squared. So far we have only found the part inside.")),
    B("Job 2. 100 squared is 100 times 100, and that is 10,000.",
      W("w4", "100² = 100 × 100 = 10,000"), ANSR("a", "(x² + y²)² = 10,000", "10,000", True)),
    B("Check the whole thing in one line: 6 squared plus 8 squared, all squared, is 10,000.",
      W("c", "(6² + 8²)² = 10,000")),
    B("The trap is to stop at 100, which is waiting among the choices. And when you square 100, count the zeros: two zeros times two zeros gives four."),
    B("So when a question says the square of something, find the something first, then square it."),
)
