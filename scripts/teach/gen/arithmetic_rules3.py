"""Rule lessons for the three average wordings, and the dispatcher that matches a question to its rule."""
import re

from arithmetic_common import ANS, B, FIG, GIVEN, M, W, choose, lesson, pick, placed
from arithmetic_rules import minus_times_plus, plus_times, plus_times_minus
from arithmetic_rules2 import divide_plus_times, equation, times_then

ORDINALS = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"]


def halves(nums, prefix):
    """Add a list in two halves. Returns (board lines, spoken sentence, total)."""
    k = len(nums) // 2
    first, second = nums[:k], nums[k:]
    x, y = sum(first), sum(second)
    total = x + y
    lines = [
        W(prefix + "1", "%s = %d" % (" + ".join(str(v) for v in first), x)),
        W(prefix + "2", "%s = %d" % (" + ".join(str(v) for v in second), y)),
        W(prefix + "3", "%d + %d = %d" % (x, y, total)),
        M(prefix + "3", str(total), "underline", 2 if str(total) in ("%d + %d" % (x, y)) else None),
    ]
    if k == 2:
        said = "%d plus %d is %d. %d plus %d is %d. And %d plus %d makes %d." % (
            first[0], first[1], x, second[0], second[1], y, x, y, total)
    else:
        said = "The first %d make %d. The last %d make %d. And %d plus %d is %d." % (k, x, len(second), y, x, y, total)
    return lines, said, total


def find_average(qid, nums):
    n = len(nums)
    lo, hi = min(nums), max(nums)
    lines, said, total = halves(nums, "s")
    avg = total // n
    assert avg * n == total, qid
    c1, r1 = placed(qid, "c1", "the total of all the numbers", ["the middle number", "the biggest number"])
    c2, r2 = placed(qid, "c2", str(n), ["2", str(hi)])
    answer = "%d ÷ %d = %d" % (total, n, avg)
    beats = [
        B(pick(qid, "i", [
            "Here are %d numbers, and we want their average. I've drawn them as bars: some tall, some short." % n,
            "We have %d numbers and we want their average. Look at them as bars. They are not all the same height." % n,
        ]), GIVEN("l1", "Average of %s = ?" % ", ".join(str(v) for v in nums), True),
            FIG("f1", {"kind": "barChart", "bars": [{"label": ORDINALS[i], "value": v} for i, v in enumerate(nums)]})),
        B(pick(qid, "q", [
            "The average is the height every bar would have if we levelled them all out. To level them, what do we need to find first?",
            "Think of the average as sharing fairly, so every bar ends up the same height. What do we need before we can share?",
        ]), ask=choose(c1, r1, "Levelling means pooling everything together and then sharing it out equally. So first we need the total: we add them all up.")),
        B(pick(qid, "p", ["So let's add, a few at a time. ", "Adding first, then. "]) + said, *lines),
        B(pick(qid, "q2", [
            "That is everything pooled together. Now we share it out equally. Into how many shares?",
            "We have the total. Next we share it out fairly. How many equal shares do we need?",
        ]), ask=choose(c2, r2, "Count the numbers in the list. There are %d of them, so the total is shared into %d equal parts." % (n, n))),
        B("%d divided by %d is %d. We can be sure of that, because %d times %d is %d. So the average is %d." % (total, n, avg, n, avg, total, avg),
          W("k1", "%d × %d = %d" % (n, avg, total)), ANS("a1", answer), M("a1", str(avg), "circle", 2 if str(avg) in str(total) else None),
          FIG("f2", {"kind": "barChart", "bars": [{"label": ORDINALS[i], "value": avg} for i in range(n)],
                     "note": "Levelled out: every bar is %d" % avg})),
        B("Does %d make sense? An average always lands between the smallest number and the biggest. Ours run from %d up to %d, and %d sits in between." % (avg, lo, hi, avg)),
        B(pick(qid, "s", [
            "So an average is three small jobs. Add them up, count them, and share equally.",
            "Remember the three steps for any average. Add them all, count how many, then divide the total by the count.",
        ])),
    ]
    return lesson(*beats, origin="rule")


def missing_number(qid, n, avg, known):
    total = n * avg
    lines, said, ksum = halves(known, "s")
    miss = total - ksum
    k = len(known)
    c1, r1 = placed(qid, "c1", "%d × %d" % (n, avg), ["%d ÷ %d" % (avg, n), "%d + %d" % (avg, n)])
    c2, r2 = placed(qid, "c2", "%d − %d" % (total, ksum), ["%d + %d" % (total, ksum), "%d ÷ %d" % (ksum, k)])
    answer = "%d − %d = %d" % (total, ksum, miss)
    beats = [
        B(pick(qid, "i", [
            "%d numbers have an average of %d. We know %d of them, and one is hiding. Let's find it." % (n, avg, k),
            "Here is a puzzle. %d numbers, average %d. We can see %d of them, but the last one is missing." % (n, avg, k),
        ]), GIVEN("l1", "Average of %d numbers = %d" % (n, avg), True),
            GIVEN("l2", "%s, ?" % ", ".join(str(v) for v in known), True),
            FIG("f1", {"kind": "barModel", "bars": [{"segments": [{"units": 1, "label": str(avg)} for _ in range(n)], "brace": "total = ?"}],
                       "note": "Levelled out, each of the %d would be %d" % (n, avg)})),
        B("An average of %d means that if we levelled all %d numbers out, each one would be %d. So what do all %d add up to?" % (avg, n, avg, n),
          ask=choose(c1, r1, "Picture %d equal bars, each one %d. The total is %d lots of %d, so we multiply." % (n, avg, n, avg))),
        B("%d times %d is %d. So all %d numbers together must make %d." % (n, avg, total, n, total),
          W("t1", "%d × %d = %d" % (n, avg, total)), M("t1", str(total))),
        B("Now add up the %d we know. " % k + said, *lines),
        B("All %d must make %d. The %d we know make %d. How do we find the hidden one?" % (n, total, k, ksum),
          ask=choose(c2, r2, "The hidden number is whatever is still needed to climb from %d up to %d. We find that gap by taking away." % (ksum, total))),
        B("%d minus %d is %d. So the missing number is %d." % (total, ksum, miss, miss),
          ANS("a1", answer), M("a1", str(miss), "circle", 2 if str(miss) in ("%d − %d" % (total, ksum)) else None)),
        B("Let's check. %d plus %d is %d, and %d shared among %d is %d. Just what the question told us." % (ksum, miss, total, total, n, avg),
          W("k1", "%d + %d = %d" % (ksum, miss, total)), W("k2", "%d ÷ %d = %d" % (total, n, avg))),
        B(pick(qid, "s", [
            "So when you know the average, multiply it by how many numbers there are to get the total. Then take away the ones you know.",
            "The key idea: average times count gives the total. Once you have the total, the missing number is just what is left.",
        ])),
    ]
    return lesson(*beats, origin="rule")


def new_number(qid, n, avg, new):
    total = n * avg
    nt = total + new
    m = n + 1
    navg = nt // m
    assert navg * m == nt and new > avg, qid
    c1, r1 = placed(qid, "c1", "%d × %d" % (n, avg), ["%d ÷ %d" % (avg, n), "%d + %d" % (avg, new)])
    c2, r2 = placed(qid, "c2", str(m), [str(n), "2"])
    tens, ones = (avg // 10) * 10, avg % 10
    if ones == 0:
        product = B("%d times %d is %d. That is what the %d numbers add up to." % (n, avg, total, n),
                    W("t1", "%d × %d = %d" % (n, avg, total)), M("t1", str(total)))
    else:
        x, y = n * tens, n * ones
        product = B("Split %d into %d and %d. %d times %d is %d, %d times %d is %d, and together that is %d. That is what the %d numbers add up to."
                    % (avg, tens, ones, n, tens, x, n, ones, y, total, n),
                    W("t1", "%d × %d = %d × %d + %d × %d" % (n, avg, n, tens, n, ones)),
                    W("t2", "%d + %d = %d" % (x, y, total)), M("t2", str(total), "underline", 2 if str(total) in ("%d + %d" % (x, y)) else None))
    answer = "%d ÷ %d = %d" % (nt, m, navg)
    beats = [
        B(pick(qid, "i", [
            "%d numbers have an average of %d. Then a new number, %d, joins them. We want the average now." % (n, avg, new),
            "Here is the story. %d numbers, average %d. Along comes one more number, %d. What happens to the average?" % (n, avg, new),
        ]), GIVEN("l1", "Average of %d numbers = %d" % (n, avg), True), GIVEN("l2", "New number: %d" % new, True)),
        B("We are not told what the %d numbers are. But we can still find what they add up to. How?" % n,
          ask=choose(c1, r1, "An average of %d means the %d numbers, levelled out, would each be %d. So their total is %d lots of %d." % (avg, n, avg, n, avg))),
        product,
        B("Now the new number joins in. %d plus %d is %d." % (total, new, nt), W("t3", "%d + %d = %d" % (total, new, nt))),
        B(pick(qid, "q2", [
            "Here comes the trap. How many numbers are we sharing among now?",
            "Careful with the next step. How many numbers are there altogether now?",
        ]), ask=choose(c2, r2, "There were %d numbers and one more has joined, so now there are %d. The new total is shared among all %d." % (n, m, m))),
        B("%d divided by %d is %d. We can check: %d times %d is %d. So the new average is %d." % (nt, m, navg, m, navg, nt, navg),
          W("k1", "%d × %d = %d" % (m, navg, nt)), ANS("a1", answer), M("a1", str(navg), "circle", 2 if str(navg) in str(nt) else None)),
        B("The newcomer was bigger than the old average, so it pulled the average up, from %d to %d. But only a little: one number against %d cannot drag it all the way to %d." % (avg, navg, n, new)),
        B(pick(qid, "s", [
            "So: find the old total, add the newcomer, then share among the new count.",
            "Three steps. Old average times old count gives the old total. Add the new number. Divide by the new count.",
        ])),
    ]
    return lesson(*beats, origin="rule")


# ── Matching a question to its rule ──────────────────────────────────────────

def ints(text):
    return [int(v) for v in re.findall(r"\d+", text)]


def correct_text(q):
    idx = "ABCD".find(q.get("correctAnswer", ""))
    o = q["options"][idx]
    return o.get("text", "") if isinstance(o, dict) else str(o)


def rule_for(q):
    """The lesson for a generated question, or None if no rule matches its wording."""
    qid = q["id"]
    text = q["questionText"].strip().replace(" - ", " − ")
    m = re.fullmatch(r"Simplify: (\d+) \+ (\d+) × (\d+)", text)
    if m:
        return plus_times(qid, *map(int, m.groups()))
    m = re.fullmatch(r"Simplify: (\d+) \+ (\d+) × (\d+) − (\d+)", text)
    if m:
        return plus_times_minus(qid, *map(int, m.groups()))
    m = re.fullmatch(r"Simplify: (\d+) − (\d+) × (\d+) \+ (\d+)", text)
    if m:
        return minus_times_plus(qid, *map(int, m.groups()))
    m = re.fullmatch(r"Simplify: (\d+) × (\d+) ([+−]) (\d+)", text)
    if m:
        return times_then(qid, int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4)))
    m = re.fullmatch(r"Simplify: (\d+) ÷ (\d+) \+ (\d+) × (\d+)", text)
    if m:
        return divide_plus_times(qid, *map(int, m.groups()), answer_text=correct_text(q))
    m = re.fullmatch(r"Solve: (\d+)x ([+−]) (\d+) = (\d+)", text)
    if m:
        return equation(qid, int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4)))
    m = re.fullmatch(r"Find the average of: ([\d, ]+)", text)
    if m:
        return find_average(qid, ints(m.group(1)))
    m = re.fullmatch(r"The average of (\d+) numbers is (\d+)\. If \d+ of the numbers are ([\d, ]+), find the missing number\.", text)
    if m:
        return missing_number(qid, int(m.group(1)), int(m.group(2)), ints(m.group(3)))
    m = re.fullmatch(r"The average of (\d+) numbers is (\d+)\. When a new number (\d+) is added, what is the new average\?", text)
    if m:
        return new_number(qid, int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None
