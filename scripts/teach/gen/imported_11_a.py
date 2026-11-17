"""Batch 11, part A: addition and subtraction stories, and the questions that
come in pairs (one builder, fed each question's numbers; every line computed)."""
from imported_11_lib import (ANS, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, GIVENM, LB, LESSON, NOTE,  # noqa: F401
                             STRIKE, UL, W, col_sub, last_nth)

P = "AIGEN_grade5_"
T2 = "IPMTB_grade5_ch02_"
T5 = "IPMTB_grade5_ch05_"

LESSONS = {}

# ── Three money stories ──────────────────────────────────────────────────────

# The chai stall's cash box.
LESSONS[P + "f5e9568c-1246-4f58-bd0c-b166c1fe39cf"] = LESSON(
    B("Priya's family starts the week with 3,500 rupees in the cash box. Over four days, money comes in three times and goes out once. Let's follow it day by day.",
      GIVEN("q", "Start ₹3,500. Mon +2,475, Tue +1,860, Wed 1,345, Thu +2,190")),
    B("On Wednesday they spent 1,345 rupees on milk, tea leaves and sugar. What does spending do to the cash box?",
      UL("q", "Wed 1,345"),
      ask=CHOOSE(["add 1,345", "take away 1,345", "leave it out"], 1,
                 "Money that is spent leaves the cash box. So Wednesday is the one day we take away. On every other day we add.")),
    B("Start with Monday's earnings. 3,500 plus 2,475 makes 5,975 rupees in the box.",
      W("l1", "3,500 + 2,475 = 5,975")),
    B("Tuesday brings in 1,860 more. 5,975 plus 1,860 is 7,835.",
      W("l2", "5,975 + 1,860 = 7,835")),
    B("Now Wednesday, the spending day. Careful here: this one comes off. 7,835 minus 1,345 is 6,490.",
      W("l3", "7,835 − 1,345 = 6,490"), BOX("l3", "− 1,345")),
    B("On Thursday they earn again. 6,490 plus 2,190 is 8,680. So the cash box holds 8,680 rupees at the end of Thursday.",
      ANS("l4", "6,490 + 2,190 = 8,680"), CIRC("l4", "8,680")),
    B("The trap in this story is adding all five numbers, just because they are all money. Ask of each amount: did it come in, or did it go out?"),
    B("Check another way. All the money that came in adds up to 10,025. Take off the 1,345 that was spent, and we get 8,680 again.",
      W("l5", "3,500 + 2,475 + 1,860 + 2,190 = 10,025"), W("l6", "10,025 − 1,345 = 8,680")),
    B("So in a money story, start with what was there. Add what comes in, take away what goes out, one step at a time."),
)

# Ravi works backwards to Grandmother's gift.
LESSONS[P + "f8abac9a-d1af-40d5-b9e2-e7fc2785e5cd"] = LESSON(
    B("Ravi bought crackers, sweets and gifts, and still had 2,350 rupees left. Part of his money was 500 rupees from an old envelope. We want only what Grandmother gave him.",
      GIVEN("q", "Spent 1,245 + 867 + 1,538. Left 2,350. Envelope 500")),
    B("This is a work backwards story: we know the end and we want the start. First, the spending. 1,245 plus 867 plus 1,538 is 3,650 rupees.",
      W("l1", "1,245 + 867 + 1,538 = 3,650")),
    B("He spent 3,650 and still had 2,350 left. How do we find what he had before he started spending?",
      ask=CHOOSE(["3,650 + 2,350", "3,650 − 2,350", "2,350 − 500"], 0,
                 "Before the shopping, he was holding the money he spent and the money he kept. So we put the two back together: 3,650 plus 2,350.")),
    B("3,650 plus 2,350 is 6,000. So Ravi had 6,000 rupees before he bought anything.",
      W("l2", "3,650 + 2,350 = 6,000")),
    B("Careful here. 6,000 is one of the choices, but it did not all come from Grandmother. 500 of it came from the envelope.",
      UL("q", "Envelope 500")),
    B("So what do we do with the 500?",
      ask=CHOOSE(["add it to 6,000", "take it away from 6,000"], 1,
                 "The 6,000 already has the envelope money inside it. To leave only Grandmother's gift, we take the 500 out.")),
    B("6,000 minus 500 is 5,500. Grandmother gave him 5,500 rupees.",
      ANS("l3", "6,000 − 500 = 5,500"), CIRC("l3", "5,500")),
    B("Check by playing the story forwards. 5,500 plus 500 is 6,000. Take away the 3,650 he spent, and 2,350 is left, just as the story says.",
      W("l4", "5,500 + 500 = 6,000"), W("l5", "6,000 − 3,650 = 2,350")),
    B("So when a story gives you the end, walk backwards. Put back what was spent, then take out anything that came from somewhere else."),
)

# Diwali shopping, and what is left for the charity boxes.
LESSONS[P + "ffd98e99-960b-4a49-ae2e-f6b3c7441d56"] = LESSON(
    B("Ravi's family set aside 5,000 rupees for Diwali shopping. They bought crackers, sweets and decorations, and shared what was left between 2 charity boxes.",
      GIVEN("q", "₹5,000 set aside. Spent 2,475, 1,368, 957. Rest ÷ 2")),
    B("What do we need to find first?",
      ask=CHOOSE(["5,000 ÷ 2", "the total they spent", "5,000 − 2,475"], 1,
                 "Only the leftover money is shared. And we cannot know the leftover until we know what the three things cost altogether.")),
    B("Add the crackers and the sweets first. 2,475 plus 1,368 is 3,843.",
      W("l1", "2,475 + 1,368 = 3,843")),
    B("Now the decorations. 3,843 plus 957 is 4,800. So they spent 4,800 rupees.",
      W("l2", "3,843 + 957 = 4,800")),
    B("Take that from the 5,000 they set aside. 5,000 minus 4,800 leaves 200 rupees.",
      W("l3", "5,000 − 4,800 = 200")),
    B("Careful: 200 is one of the choices, but that is the whole leftover. It still has to be split between the 2 boxes.",
      BOX("q", "Rest ÷ 2")),
    B("200 divided by 2 is 100. Each charity box gets 100 rupees.",
      ANS("l4", "200 ÷ 2 = 100"), CIRC("l4", "100")),
    B("Check it. 2 boxes of 100 make 200, and 200 plus the 4,800 they spent is 5,000. Every rupee is accounted for.",
      W("l5", "2 × 100 = 200"), W("l6", "200 + 4,800 = 5,000")),
    B("So follow the story in order: total the spending, find what is left, then share it out."),
)


# ── Reverse the digits, then find the difference ─────────────────────────────

def _col_say(c, nxt, top_place):
    place = c["place"].capitalize()
    if c["borrow"] and not c["lent"]:
        return "%s: %d minus %d cannot be done, so we borrow 1 from the %s. That makes %d, and %d minus %d is %d." % (
            place, c["top"], c["bot"], nxt, c["eff"], c["eff"], c["bot"], c["res"])
    assert not c["borrow"], "a column that lends and borrows needs its own words"
    if c["lent"]:
        s = "Careful at the %s. The %d lent 1, so it is now %d. %d minus %d is %d." % (
            c["place"], c["top"], c["eff"], c["eff"], c["bot"], c["res"])
    else:
        s = "%s: %d minus %d is %d." % (place, c["top"], c["bot"], c["res"])
    if top_place and c["res"] == 0:
        s += " We do not write a 0 at the front of a number."
    return s


def _col_line(i, c):
    return LB("c%d" % i, "%s: %d − %d = %d" % (c["place"].capitalize(), c["eff"], c["bot"], c["res"]))


def reverse_difference(a, a_s, slips, at, ans_s):
    digits = str(a)
    b = int(digits[::-1])
    b_s = a_s[0:0] + (str(b) if "," not in a_s else "%s,%s" % (str(b)[:-3], str(b)[-3:]))
    big, small = (a, b) if a > b else (b, a)
    big_s, small_s = (a_s, b_s) if a > b else (b_s, a_s)
    cols = col_sub(big, small)
    diff = big - small
    assert int(ans_s.replace(",", "")) == diff
    choices = list(slips)
    choices.insert(at, b_s)
    beats = [
        B("We have the number %s. We must flip its digits round, and then find the difference between the two numbers." % a_s,
          GIVENM("q", a_s)),
        B("Reversing means writing the digits in the opposite order, last digit first. What do we get?",
          ask=CHOOSE(choices, at,
                     "Read the digits from the back: %s. Written in that order, the new number is %s." % (
                         ", ".join(digits[::-1]), b_s))),
        B("So the reversed number is %s. Difference means subtract, and we always take the smaller number from the bigger one." % b_s,
          W("l1", "%s %s %s = ?" % (big_s, "−", small_s)), UL("l1", big_s), NOTE("l1", big_s, "bigger, on top")),
    ]
    careful = 0
    for i, c in enumerate(cols):
        nxt = cols[i + 1]["place"] if i + 1 < len(cols) else ""
        say = _col_say(c, nxt, i == len(cols) - 1)
        if say.startswith("Careful at the"):
            careful += 1
            if careful > 1:
                say = say.replace("Careful at the", "The same thing happens at the", 1)
        if i == 0:
            say = "Start at the ones. " + say.split(": ", 1)[1][0].upper() + say.split(": ", 1)[1][1:]
        ops = [_col_line(i, c)]
        if c["borrow"]:
            ops.append(BOX("c%d" % i, str(c["eff"])))
        beats.append(B(say, *ops))
    line = "%s − %s = %s" % (big_s, small_s, ans_s)
    beats += [
        B("Now read the digits from the top place down. The difference is %s." % ans_s,
          ANS("l2", line), CIRC("l2", ans_s, last_nth(line, ans_s))),
        B("The classic slip is to take the smaller digit from the bigger one in every column, whichever is on top. The top number stays on top, and we borrow when its digit is too small."),
        B("Check by adding back. %s plus %s should give %s, and it does." % (ans_s, small_s, big_s),
          W("l3", "%s + %s = %s" % (ans_s, small_s, big_s))),
        B("So: reverse the digits, put the bigger number on top, subtract place by place from the ones, and borrow when you need to."),
    ]
    return LESSON(*beats)


LESSONS[T2 + "q007"] = reverse_difference(2371, "2371", ["1372", "3217"], 1, "639")
LESSONS[T2 + "q032"] = reverse_difference(5341, "5,341", ["1,345", "3,514"], 0, "3,906")


# ── What should be added to reach 99,999? ────────────────────────────────────

def added_to_reach(part, part_s, total_s, ans_s, v):
    total = int(total_s.replace(",", ""))
    cols = col_sub(total, part)
    assert not any(c["borrow"] for c in cols)
    assert int(ans_s.replace(",", "")) == total - part
    said = ["%s: 9 minus %d is %d." % (c["place"].capitalize(), c["bot"], c["res"]) for c in cols]
    said[0] = "Start at the ones. 9 minus %d is %d." % (cols[0]["bot"], cols[0]["res"])
    said[4] = "And the ten-thousands: 9 minus %d is %d." % (cols[4]["bot"], cols[4]["res"])
    lines = [LB("c%d" % i, "%s: 9 − %d = %d" % (c["place"].capitalize(), c["bot"], c["res"])) for i, c in enumerate(cols)]
    digits = ", ".join(str(c["res"]) for c in reversed(cols))
    line = "%s − %s = %s" % (total_s, part_s, ans_s)
    intro = [
        "What should be added to %s to get %s? We know the total and one part of it, and we want the missing part.",
        "Some number, added to %s, makes %s. The total is known, one part is known, and the other part is hiding.",
    ][v] % (part_s, total_s)
    ask_say = ["Which sum finds the missing part?", "How do we find the part that is hiding?"][v]
    choices = ["%s − %s" % (total_s, part_s), "%s + %s" % (total_s, part_s), "%s − %s" % (part_s, total_s)]
    at = [0, 1][v]
    if at == 1:
        choices[0], choices[1] = choices[1], choices[0]
    return LESSON(
        B(intro, GIVENM("q", "%s + ? = %s" % (part_s, total_s)), BOX("q", "?")),
        B(ask_say, ask=CHOOSE(choices, at,
                              "The missing part is what is left when we take the part we know out of the total. So we subtract: %s minus %s." % (total_s, part_s))),
        B(["Write it as a subtraction. Good news: every digit on top is a 9, so there is no borrowing anywhere.",
           "So it is a subtraction. Look at the top number: all 9s. No column will need to borrow."][v],
          W("l1", "%s − %s = ?" % (total_s, part_s)), UL("l1", total_s)),
        B(said[0] + " " + said[1], lines[0], lines[1]),
        B(said[2] + " " + said[3], lines[2], lines[3]),
        B(said[4], lines[4]),
        B("Now read the digits from the biggest place down: %s. That is %s." % (digits, ans_s),
          ANS("l2", line), CIRC("l2", ans_s)),
        B("Careful with the 0 at the end. It has to be written, because it holds the ones place. Leave it out and every other digit slides into a smaller place."),
        B(["Check by adding. %s plus %s is %s. It fits.", "Check it. %s plus %s gives %s, just as the question wanted."][v] % (part_s, ans_s, total_s),
          W("l3", "%s + %s = %s" % (part_s, ans_s, total_s))),
        B("So when a question asks what should be added, subtract: the total minus the part you know."),
    )


LESSONS[T5 + "q009"] = added_to_reach(70369, "70,369", "99,999", "29,630", 0)
LESSONS[T5 + "q028"] = added_to_reach(65269, "65,269", "99,999", "34,730", 1)


# ── The sum of two ages after some years ─────────────────────────────────────

def ages_after(n1, a1, n2, a2, yrs, v):
    f1, f2 = a1 + yrs, a2 + yrs
    now, grow = a1 + a2, 2 * yrs
    total = f1 + f2
    assert now + grow == total
    choices = ["just one of them", "both of them"]
    at = 1
    if v == 1:
        choices.reverse()
        at = 0
    return LESSON(
        B(["%s is %d years old and %s is %d. We want the sum of their ages after %d years.",
           "Today %s is %d and %s is %d. The question jumps %d years ahead and asks for the sum of their ages then."][v] % (n1, a1, n2, a2, yrs),
          GIVEN("q", "Now: %s %d, %s %d. Sum of ages after %d years = ?" % (n1, a1, n2, a2, yrs)), UL("q", "after %d years" % yrs)),
        B("In %d years, how many of them grow %d years older?" % (yrs, yrs),
          ask=CHOOSE(choices, at,
                     "Time passes for everybody. In %d years %s is %d years older, and so is %s. So the %d is added once for each of them." % (
                         yrs, n1, yrs, n2, yrs))),
        B("%s first. %d plus %d is %d." % (n1, a1, yrs, f1), W("l1", "%d + %d = %d" % (a1, yrs, f1))),
        B("Now %s. %d plus %d is %d." % (n2, a2, yrs, f2), W("l2", "%d + %d = %d" % (a2, yrs, f2))),
        B("Add the two new ages. %d plus %d is %d. The sum of their ages will be %d years." % (f1, f2, total, total),
          ANS("l3", "%d + %d = %d" % (f1, f2, total)), CIRC("l3", str(total), last_nth("%d + %d = %d" % (f1, f2, total), str(total)))),
        B("Here is the trap: adding the %d only once. The sum of their ages today is %d, and two people each grow %d years older." % (yrs, now, yrs),
          W("l4", "%d + %d = %d" % (a1, a2, now))),
        B("That gives us a second way, and a check. The sum grows by 2 times %d, which is %d. And %d plus %d is %d again." % (yrs, grow, now, grow, total),
          W("l5", "2 × %d = %d" % (yrs, grow)), W("l6", "%d + %d = %d" % (now, grow, total))),
        B("So when time passes, every person in the story gets older. Add the years to each age, then add the ages."),
    )


LESSONS[T5 + "q010"] = ages_after("Pawan", 14, "Akash", 10, 7, 0)
LESSONS[T5 + "q033"] = ages_after("Rajesh", 15, "Rakesh", 9, 8, 1)


# ── Sixteen thousand or sixty thousand? ──────────────────────────────────────

def teen_ty(teen_word, teen, ty_word, ty, v):
    ones = teen - 10
    diff = ty - teen
    mid = ty - 10
    big, small, ans = "%d,000" % ty, "%d,000" % teen, "%d,000" % diff
    choices = [small, big, "%d,%d00" % (teen // 10, teen % 10)]
    at = 0
    if v == 1:
        choices = [big, small, choices[2]]
        at = 1
    return LESSON(
        B("A student meant to write %s thousand, but wrote %s thousand. The two sound almost the same! We want to know how far apart they really are." % (teen_word, ty_word),
          GIVEN("q", "meant: %s thousand   wrote: %s thousand" % (teen_word, ty_word))),
        B("First, %s thousand in digits. Which is it?" % teen_word,
          ask=CHOOSE(choices, at,
                     "%s is 1 ten and %d ones. So %s thousand starts with a 1 and %s %d, and then has three zeros for the thousands." % (
                         teen_word.capitalize(), ones, teen_word, "an" if ones == 8 else "a", ones))),
        B("So %s thousand is %s. And %s is %d tens, so %s thousand starts with %s %d and a 0, then three zeros: %s." % (
            teen_word, small, ty_word, ty // 10, ty_word, "an" if ty // 10 == 8 else "a", ty // 10, big),
          LB("l1", "%s thousand = %s" % (teen_word, small)), LB("l2", "%s thousand = %s" % (ty_word, big)),
          UL("l1", small), UL("l2", big)),
        B(["How far off was the answer? That is the difference, so we subtract the smaller number from the bigger.",
           "By how much means the gap between the two. To find a gap we subtract, smaller from bigger."][v],
          W("l3", "%s − %s = ?" % (big, small))),
        B("Both numbers are whole thousands, so just think %d minus %d. Take 10 away to get %d, then %d more away to get %d." % (ty, teen, mid, ones, diff),
          W("l4", "%d − %d = ?" % (ty, teen)), W("l5", "%d − 10 = %d" % (ty, mid)), W("l5b", "%d − %d = %d" % (mid, ones, diff))),
        B("%d thousands is %s. The answer was off by %s." % (diff, ans, ans),
          ANS("l6", "%s − %s = %s" % (big, small, ans)), CIRC("l6", ans)),
        B("Listen to the endings. %s ends in teen, which means ten and some more. %s ends differently, and means %d tens. One small sound, one very big difference." % (
            teen_word.capitalize(), ty_word.capitalize(), ty // 10)),
        B("Check by adding back. %s plus %s is %s." % (small, ans, big),
          W("l7", "%s + %s = %s" % (small, ans, big))),
        B("So write both numbers in digits first. Then subtract the smaller from the bigger."),
    )


LESSONS[T5 + "q019"] = teen_ty("sixteen", 16, "sixty", 60, 0)
LESSONS[T5 + "q044"] = teen_ty("eighteen", 18, "eighty", 80, 1)
