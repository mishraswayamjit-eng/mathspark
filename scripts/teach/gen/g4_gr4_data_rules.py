"""Data handling: lessons by rule for the generated average questions (three wordings).

    A  Find the average of: 44, 26, 51, 56, 48
    B  The average of 4 numbers is 58. If 3 of the numbers are 71, 56, 72, find the missing number.
    C  The average of 4 numbers is 49. When a new number 59 is added, what is the new average?

Each rule reads the numbers from the question, computes every line, and picks its phrasing
by a stable hash of the question id.
"""
import re

from g4_gr4_time_lib import beat, given, w, lab, ans, mark, box, pick, choose

WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def running_sum(nums, prefix):
    """Board lines and spoken phrases for adding a list one number at a time."""
    ops, said = [], []
    total = nums[0]
    for i, n in enumerate(nums[1:]):
        ops.append(w("%s%d" % (prefix, i), "%d + %d = %d" % (total, n, total + n)))
        if i == 0:
            said.append("%d plus %d is %d" % (total, n, total + n))
        elif i == len(nums) - 2:
            said.append("and %d more makes %d" % (n, total + n))
        else:
            said.append("add %d to get %d" % (n, total + n))
        total += n
    return ops, said, total


def say_sum(said):
    caps = [p[0].upper() + p[1:] for p in said]
    if len(said) > 1 and said[-1].startswith("and "):
        return ". ".join(caps[:-1]) + ", " + said[-1] + "."
    return ". ".join(caps) + "."


def rule_a(q):
    qid = q["id"]
    nums = [int(x) for x in re.findall(r"\d+", q["questionText"])]
    n = len(nums)
    listed = ", ".join(str(x) for x in nums)
    ops, said, total = running_sum(nums, "s")
    avg = total // n
    assert avg * n == total
    beats = [
        beat(pick(qid, "open", [
            "We want the average of these %s numbers: %s." % (WORDS[n], listed),
            "Here are %s numbers: %s. Let's find their average." % (WORDS[n], listed)]),
            given("q", "Average of %s = ?" % listed)),
        beat(pick(qid, "idea", [
            "The average is the fair share. Imagine putting all the numbers into one pot, and then sharing the pot out equally.",
            "Think of the average as levelling out. We pile everything together, then give each number the same share."]),
            lab("r", "Average = total ÷ how many numbers")),
    ]
    if n <= 4:
        beats.append(beat("First the total. " + say_sum(said), *ops))
    else:
        beats.append(beat("First the total. We add one number at a time. " + say_sum(said[:2]), *ops[:2]))
        beats.append(beat("Keep going. " + say_sum(said[2:]), *ops[2:]))
    beats += [
        beat(pick(qid, "ask", [
            "The total is %d. Now, what do we divide it by?" % total,
            "So the pot holds %d. How many shares do we cut it into?" % total]),
            box("s%d" % (n - 2), str(total)),
            ask=choose("%d, how many numbers there are" % n, ["2", "%d, the first number" % nums[0]],
                       "Count the numbers in the list. There are %d of them, so the total is shared %d ways." % (n, n))),
        beat("%d divided by %d is %d, because %d times %d is %d." % (total, n, avg, n, avg, total),
             w("d", "%d ÷ %d = %d" % (total, n, avg)), w("c", "%d × %d = %d" % (n, avg, total))),
        beat("So the average is %d." % avg, ans("a", "Average = %d" % avg, str(avg))),
        beat("Does it look sensible? The smallest number is %d and the biggest is %d, and %d sits between them. An average always does."
             % (min(nums), max(nums), avg)),
        beat(pick(qid, "sum", [
            "So for any average: add everything up, then divide by how many numbers there are.",
            "Two steps every time: find the total, then share it by the count."])),
    ]
    return beats


def rule_b(q):
    qid = q["id"]
    m = re.match(r"The average of (\d+) numbers is (\d+)\. If (\d+) of the numbers are ([\d, ]+), find the missing number", q["questionText"])
    n, avg, k = int(m.group(1)), int(m.group(2)), int(m.group(3))
    known = [int(x) for x in re.findall(r"\d+", m.group(4))]
    assert len(known) == k == n - 1
    listed = ", ".join(str(x) for x in known)
    total = n * avg
    ops, said, s = running_sum(known, "s")
    missing = total - s
    beats = [
        beat("The average of %d numbers is %d. We know %d of them: %s. We must find the missing one." % (n, avg, k, listed),
             given("q", "Average of %d numbers is %d." % (n, avg)), lab("q2", "Known: %s.   Missing = ?" % listed)),
        beat(pick(qid, "idea", [
            "An average is a fair share. It is as if every one of the %d numbers were %d. That tells us the total." % (n, avg),
            "Here is the key. If the average of %d numbers is %d, the numbers add up to the same as %d lots of %d." % (n, avg, n, avg)])),
        beat("So how do we find the total of all %d numbers?" % n,
             ask=choose("%d × %d" % (avg, n), ["%d + %d" % (avg, n), "%d ÷ %d" % (avg, n)],
                        "If each of the %d numbers were %d, the total would be %d lots of %d. So we multiply." % (n, avg, n, avg))),
        beat("%d times %d is %d. All %d numbers together make %d." % (avg, n, total, n, total),
             w("t", "%d × %d = %d" % (avg, n, total)), box("t", str(total))),
        beat("Now add the %d numbers we know. " % k + say_sum(said), *ops),
        beat(pick(qid, "left", [
            "The missing number is whatever is left. %d minus %d is %d." % (total, s, missing),
            "Take the known part away from the total. %d minus %d leaves %d." % (total, s, missing)]),
            w("m", "%d − %d = %d" % (total, s, missing))),
        beat("The missing number is %d." % missing, ans("a", "Missing number = %d" % missing, str(missing))),
        beat("Check: %d plus %d is %d, and %d divided by %d is %d. It works." % (s, missing, total, total, n, avg),
             w("c", "%d ÷ %d = %d" % (total, n, avg))),
        beat(pick(qid, "sum", [
            "So: average times count gives the total. Then take away what you know.",
            "Turn the average into a total first. The missing number is the total minus the rest."])),
    ]
    return beats


def rule_c(q):
    qid = q["id"]
    m = re.match(r"The average of (\d+) numbers is (\d+)\. When a new number (\d+) is added", q["questionText"])
    n, avg, new = int(m.group(1)), int(m.group(2)), int(m.group(3))
    total = n * avg
    total2 = total + new
    n2 = n + 1
    avg2 = total2 // n2
    assert avg2 * n2 == total2
    if new > avg:
        sense = "The new number, %d, is bigger than the old average, %d. So it pulled the average up a little. That makes sense." % (new, avg)
    elif new < avg:
        sense = "The new number, %d, is smaller than the old average, %d. So it pulled the average down a little. That makes sense." % (new, avg)
    else:
        sense = "The new number is the same as the old average, so the average did not move at all."
    beats = [
        beat("The average of %d numbers is %d. Then a new number, %d, joins them. What is the new average?" % (n, avg, new),
             given("q", "Average of %d numbers is %d. A new number %d joins." % (n, avg, new)), lab("q2", "New average = ?")),
        beat(pick(qid, "idea", [
            "We do not know what the %d numbers are. But we do not need to! Their total is enough." % n,
            "The %d numbers are a secret, and that is fine. All we need is what they add up to." % n])),
        beat("%d numbers with an average of %d add up to the same as %d lots of %d. %d times %d is %d."
             % (n, avg, n, avg, avg, n, total),
             w("t", "%d × %d = %d" % (avg, n, total)), lab("t2", "Old total: %d" % total)),
        beat("Now the new number joins the pot. %d plus %d is %d." % (total, new, total2),
             w("u", "%d + %d = %d" % (total, new, total2))),
        beat("We must share the new total. How many numbers are there now?",
             ask=choose(str(n2), [str(n), "2"],
                        "There were %d numbers, and 1 more joined. %d plus 1 is %d. Forgetting to count the new one is the classic slip."
                        % (n, n, n2))),
        beat("There are %d numbers now. %d divided by %d is %d, because %d times %d is %d."
             % (n2, total2, n2, avg2, n2, avg2, total2),
             w("d", "%d ÷ %d = %d" % (total2, n2, avg2)), w("c", "%d × %d = %d" % (n2, avg2, total2))),
        beat("The new average is %d." % avg2, ans("a", "New average = %d" % avg2, str(avg2))),
        beat(sense),
        beat(pick(qid, "sum", [
            "So: old average times old count gives the old total. Add the newcomer, then divide by the new count.",
            "Go through the total every time. Find it, add the new number, and share it among one more."])),
    ]
    return beats


def lesson_for(q):
    text = q["questionText"]
    if text.startswith("Find the average of:"):
        return rule_a(q)
    if "find the missing number" in text:
        return rule_b(q)
    if "When a new number" in text:
        return rule_c(q)
    return None
