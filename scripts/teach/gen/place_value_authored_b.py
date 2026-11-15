"""Place-value lessons written by hand, part B: final papers 2016 to 2019 (EXT_G5_FP_...).

Also holds walk_lesson(), used for the five 'if (x + 37) is even, the 17th odd
number after it is...' questions. They are the same idea with different numbers,
so they share one carefully written lesson, with the wording varied a little.
"""
from place_value_lib import a, al, b, ch, fig, g, gl, nt, pchart, pick, ring, tbl, ul, w, wl, x

LESSONS = {}

PLACES4 = ["thousands", "hundreds", "tens", "units"]


def walk_lesson(qid, letter, base, start_kind, k, after, answer_text, try_value, prime_note=False):
    """'(letter + base) is start_kind. The k-th number of the OTHER kind after / before it?'

    base is signed (f − 9 has base −9). try_value is a small value of the letter
    used to check the answer with real numbers.
    """
    want = "odd" if start_kind == "even" else "even"
    expr = "%s %s %d" % (letter, "+" if base >= 0 else "−", abs(base))
    expr_say = "%s %s %d" % (letter, "plus" if base >= 0 else "minus", abs(base))
    jumps = k - 1
    reach = 1 + 2 * jumps
    result = base + reach if after else base - reach
    assert result > 0 and ("%d" % result) in answer_text, qid
    sign = "+" if after else "−"
    way = "after" if after else "before"
    start = try_value + base
    end = start + reach if after else start - reach
    assert start > 0 and end > 0 and start % 2 == (0 if start_kind == "even" else 1), qid
    assert try_value + result == end, qid

    beats = []
    beats.append(b(pick(qid, "open", [
        "This one looks like algebra, but it is really about counting along a line of numbers.",
        "A letter in the question, but no need to worry. This is a counting puzzle in disguise.",
    ]), gl("q", "(%s) is %s. The %dth %s number %s it?" % (
        expr, "a 2-digit prime" if prime_note else start_kind, k, want, way))))
    if prime_note:
        beats.append(b("First, a clue to decode. A prime with 2 digits cannot be even, because the only even prime is 2. So %s is an odd number." % expr_say,
                       wl("clue", "2-digit prime, so (%s) is odd" % expr)))
    beats.append(b("We do not know %s, and we do not need to. Think of %s as one %s number, and walk %s from it." % (
        letter, expr_say, start_kind, "forward" if after else "backwards")))
    beats.append(b("What is the first %s number %s any %s number?" % (want, way, start_kind),
                   ask=ch(["1 more", "2 more", "1 less"] if after else ["1 less", "2 less", "1 more"],
                          "Even and odd numbers take turns. So the number right next to it, 1 %s, is %s." % ("more" if after else "less", want))))
    beats.append(b("So the 1st one is 1 %s. After that, each new %s number is 2 further %s: 3 away, then 5 away." % (
        "more" if after else "less", want, "on" if after else "back"),
        wl("o1", "1st %s:  start %s 1" % (want, sign)), wl("o2", "2nd %s:  start %s 3" % (want, sign)),
        wl("o3", "3rd %s:  start %s 5" % (want, sign))))
    beats.append(b("To get from the 1st to the %dth takes %d more jumps of 2. Careful: %d jumps, not %d, because the 1st one is already counted." % (
        k, jumps, jumps, k), w("n", "%d − 1 = %d" % (k, jumps))))
    beats.append(b("%d jumps of 2 cover %d. Add the first step of 1, and we have gone %d in all." % (jumps, 2 * jumps, reach),
                   w("j", "%d × 2 = %d" % (jumps, 2 * jumps)), w("t", "1 + %d = %d" % (2 * jumps, reach)), ring("t", str(reach))))
    beats.append(b("So the %dth %s number is %d %s our starting number, %s." % (k, want, reach, "more than" if after else "less than", expr_say),
                   wl("e", "%dth %s:  (%s) %s %d" % (k, want, expr, sign, reach)), ul("e", "%s %d" % (sign, reach))))
    if after and base >= 0:
        line, say = "%d + %d = %d" % (base, reach, result), "Plus %d and plus %d together make plus %d." % (base, reach, result)
    elif after:
        line, say = "%d − %d = %d" % (reach, -base, result), "Minus %d and plus %d together make plus %d." % (-base, reach, result)
    else:
        line, say = "%d − %d = %d" % (base, reach, result), "Plus %d, then minus %d, leaves plus %d." % (base, reach, result)
    beats.append(b(say + " So we have %s plus %d." % (letter, result), w("s", line)))
    beats.append(b("Try it with a real number. If %s is %d, then %s is %d. Going %s by %d lands on %d. And %d plus %d is %d too." % (
        letter, try_value, expr_say, start, "on" if after else "back", reach, end, try_value, result, end),
        w("c1", "%d %s %d = %d" % (try_value, "+" if base >= 0 else "−", abs(base), start)),
        w("c2", "%d %s %d = %d" % (start, sign, reach, end)),
        w("c3", "%d + %d = %d" % (try_value, result, end))))
    core = "%s + %d" % (letter, result)
    beats.append(b("So the answer is %s plus %d. Remember: 1 step to reach the first one, then jumps of 2 for all the rest." % (letter, result),
                   al("ans", answer_text), ring("ans", core)))
    return beats


# In one crore how many tens are there?  -> ten lakh tens
LESSONS["EXT_G5_FP_2016_018"] = [
    b("One crore. That is a huge number, and we want to know how many tens are inside it.", gl("q", "1 crore = how many tens?")),
    b("One crore is 1 followed by 7 zeros. In the Indian system we put the commas like this.",
      w("c", "1,00,00,000"), fig("chart", pchart("10000000", hi=[0]))),
    b("How do we find how many tens fit into a number?",
      ask=ch(["divide by 10", "multiply by 10", "subtract 10"],
             "'How many tens' asks how many groups of 10 fit in. Making equal groups is dividing.")),
    b("Dividing by 10 takes one zero off the end. So 7 zeros become 6 zeros.", w("d", "1,00,00,000 ÷ 10 = 10,00,000")),
    b("Now read what is left, the Indian way. The lakhs come after the thousands. A 1 with 6 zeros is ten lakh.",
      wl("r", "10,00,000 = ten lakh")),
    b("Check by going back. Ten lakh tens, times 10, puts the zero back and gives one crore.", w("k", "10,00,000 × 10 = 1,00,00,000")),
    b("So there are ten lakh tens in one crore.", al("ans", "ten lakh tens"), ring("ans", "ten lakh")),
    b("To count the tens in a number, divide by 10. Then read the answer carefully, group by group."),
]

# Place value of 4 in the smallest 5-digit odd number from 1, 8, 4, 0, 7  -> 400
LESSONS["EXT_G5_FP_2016_019"] = [
    b("First we build the smallest 5 digit odd number from 1, 8, 4, 0 and 7. Then we see what its 4 is worth.",
      gl("q", "digits 1, 8, 4, 0, 7: smallest 5-digit odd number")),
    b("Odd means the last digit is odd. Our odd digits are 1 and 7, so one of them goes last.", wl("c", "last digit: 1 or 7")),
    b("For the smallest number we want a small digit at the front. Can 0 go first?",
      ask=ch(["No, it would not have 5 digits", "Yes, 0 is the smallest"],
             "A number that starts with 0 really has only 4 digits. So the front digit must be the smallest digit that is not 0.")),
    b("So 1 should lead, and that means 7 is the odd digit at the end. Fill the middle with the smallest first: 0, 4, 8. That gives 10487.",
      w("n", "10487")),
    b("If we had put 1 at the end instead, the smallest we could make is 40781. Much bigger.", w("k", "10487 < 40781")),
    b("Now find the 4. Units, tens, hundreds. It is in the hundreds place.",
      fig("chart", pchart("10487", hi=[2])), ul("n", "4"), nt("n", "4", "hundreds")),
    b("4 hundreds: 4 times 100 is 400.", w("pv", "4 × 100 = 400")),
    b("So the place value of the 4 is 400. Build the number first, then read the place.",
      al("ans", "Place value of 4 = 400"), ring("ans", "400")),
]

# 2138574: digits that keep their position when arranged in ascending order  -> three
LESSONS["EXT_G5_FP_2016_024"] = [
    b("Here are the digits of 2138574, spread out so we can see each position clearly.", gl("o", "2  1  3  8  5  7  4")),
    b("We must arrange them in ascending order. Ascending means smallest first. So which digit comes first?",
      ask=ch(["1", "2", "8"], "Ascending means going up, like climbing stairs. So we start with the smallest digit, which is 1.")),
    b("In order they are 1, 2, 3, 4, 5, 7, 8. I have written them right underneath, so each digit sits below the one in the same position.",
      wl("s", "1  2  3  4  5  7  8")),
    b("Now compare, position by position. First position: 2 on top, 1 below. Different. Second: 1 and 2. Different again."),
    b("Third position: 3 on top and 3 below. The same!", ring("o", "3"), ring("s", "3")),
    b("Fourth: 8 and 4, different. Fifth: 5 and 5, the same. Sixth: 7 and 7, the same. Last: 4 and 8, different.",
      ring("o", "5"), ring("s", "5"), ring("o", "7"), ring("s", "7")),
    b("Count the rings: the 3, the 5 and the 7. Three digits kept their positions.",
      al("ans", "three digits: 3, 5 and 7"), ring("ans", "three")),
    b("Write the two arrangements one under the other, then compare place by place. The picture does the work."),
]

# Mr. Sam: age a multiple of 8 in 2000, a multiple of 7 in 2001  -> 1952
LESSONS["EXT_G5_FP_2016_025"] = [
    b("Two clues about Mr. Sam's age. In 2000 it was a multiple of 8, and in 2001 it was a multiple of 7.",
      gl("q", "2000: a multiple of 8.   2001: a multiple of 7.")),
    b("From 2000 to 2001 he grows exactly 1 year older. So we want a multiple of 8 whose very next number is a multiple of 7."),
    b("Here are the multiples of 8. For each one, think about the number that comes just after it.",
      wl("m", "8, 16, 24, 32, 40, 48, 56, 64")),
    b("Which multiple of 8 is followed by a multiple of 7?",
      ask=ch(["48, then 49", "40, then 41", "56, then 57"],
             "41 and 57 are not in the 7 times table. But 49 is 7 times 7. So the pair is 48 and 49.")),
    b("48 is 8 times 6, and 49 is 7 times 7. So he was 48 in the year 2000.",
      w("e", "8 × 6 = 48"), w("s", "7 × 7 = 49"), ring("m", "48")),
    b("He was born 48 years before 2000. 2000 minus 48 is 1952.", w("y", "2000 − 48 = 1952")),
    b("Check the second clue. In 2001 he is 2001 minus 1952, which is 49. Both clues fit.", w("c", "2001 − 1952 = 49")),
    b("So Mr. Sam was born in 1952. One year apart means two numbers next to each other: that was the key.",
      a("ans", "1952"), ring("ans", "1952")),
]

LESSONS["EXT_G5_FP_2016_040"] = walk_lesson("EXT_G5_FP_2016_040", "f", -9, "even", 25, True, "(f + 40)", 11)
LESSONS["EXT_G5_FP_2017_028"] = walk_lesson("EXT_G5_FP_2017_028", "x", 37, "even", 17, True, "(x + 70)", 1)
LESSONS["EXT_G5_FP_2018_033"] = walk_lesson("EXT_G5_FP_2018_033", "x", 37, "even", 17, False, "(x + 4)", 3)

# Greatest odd number from 7, 5, 2, 0, 4  -> 74205
LESSONS["EXT_G5_FP_2017_033"] = [
    b("We want the greatest odd number that uses 7, 5, 2, 0 and 4, each once.", gl("q", "digits 7, 5, 2, 0, 4: greatest odd number")),
    b("For the greatest number we would love to write the digits biggest first. That gives 75420. But it ends in 0, so it is even. Not allowed!",
      w("t", "75420"), x("t", "75420", "even")),
    b("An odd number needs an odd digit at the end. Our odd digits are 7 and 5. Which one should go last?",
      ask=ch(["5", "7"],
             "The 7 is our biggest digit, so it is worth far more at the front. We spend the smaller odd digit, 5, on the units place.")),
    b("Keep 7 in front, put 5 at the end, and arrange what is left, 4, 2 and 0, biggest first. That makes 74205.",
      w("n", "74205"), fig("chart", pchart("74205"))),
    b("Compare it with putting 7 at the end. The best we could do then is 54207, and 74205 is far greater.", w("k", "74205 > 54207")),
    b("And it really is odd, because it ends in 5.", ul("n", "5"), nt("n", "5", "odd")),
    b("So the greatest odd number is 74205.", a("ans", "74205"), ring("ans", "74205")),
    b("Decide the last digit first, using the smaller odd digit. Then put the others in order, biggest first."),
]

# Tens digit exactly four times the thousands digit  -> 2386
LESSONS["EXT_G5_FP_2017_039"] = [
    b("Four numbers. In one of them, the tens digit is exactly four times the thousands digit.",
      gl("q", "tens digit = 4 × thousands digit"), gl("opts", "8621   2386   8326   4538")),
    b("In a 4 digit number the thousands digit is the first one, and the tens digit is the third one. Here they are in 8621.",
      fig("chart", pchart("8621", hi=[0, 2]))),
    b("Think before testing. If the thousands digit is 8, four times it is 32, and that is not a single digit. So both numbers starting with 8 are out.",
      w("t", "4 × 8 = 32"), x("opts", "8621"), x("opts", "8326")),
    b("Now 2386. Its thousands digit is 2. So what must its tens digit be?",
      ask=ch(["8", "6", "4"], "Four times the thousands digit: 4 times 2 is 8. So we need an 8 in the tens place.")),
    b("4 times 2 is 8, and the tens digit of 2386 really is 8. It fits!", w("u", "4 × 2 = 8"), ring("opts", "2386")),
    b("Check the last one, 4538. 4 times 4 is 16, but its tens digit is 3. Out.", w("v", "4 × 4 = 16"), x("opts", "4538")),
    b("So the number is 2386.", a("ans", "2386"), ring("ans", "2386")),
    b("Name the places first. Then test each number, and use what you know to rule some out quickly."),
]

# Put a 2 between the 3 and 5 of 43541  -> more by 389000
LESSONS["EXT_G5_FP_2018_002"] = [
    b("Here is 43541. We are going to slip a 2 in between the 3 and the 5.", g("n", "43541")),
    b("The 4 and the 3 stay in front, then comes the new 2, then 5, 4, 1. That makes 432541.", w("m", "432541")),
    b("What happened to the 4 and the 3 at the front when the 2 squeezed in?",
      ask=ch(["they moved one place to the left", "they stayed in the same places", "they moved one place to the right"],
             "The number grew from 5 digits to 6. So the front digits were pushed one column to the left, where they are worth 10 times more.")),
    b("In the new number the 4 is in the lakhs place, and the 3 is in the ten-thousands place. They are worth far more now.",
      fig("chart", pchart("432541", hi=[0, 1, 2]))),
    b("To find how much more the new number is, subtract the old from the new. The last three digits are the same in both, so they cancel to zeros.",
      w("s", "432541 − 43541 = 389000")),
    b("Check by adding back: 43541 plus 389000 is 432541.", w("c", "43541 + 389000 = 432541")),
    b("So the new number is more by 389000. That is far more than the new 2 is worth, because the 4 and the 3 moved as well.",
      a("ans", "389000"), ring("ans", "389000")),
    b("When a digit is slipped in, every digit to its left jumps one column. Subtract the whole numbers to see the full change."),
]

# 2017 + a 3-digit palindrome = a 4-digit palindrome; digit sum of the 3-digit one  -> 13
LESSONS["EXT_G5_FP_2018_005"] = [
    b("A palindrome reads the same both ways, like 707. We add a 3 digit palindrome to 2017 and get a 4 digit palindrome.",
      gl("q", "2017 + (3-digit palindrome) = 4-digit palindrome")),
    b("Our 3 digit palindrome has the same first and last digit. And 2017 plus a 3 digit number should still start with 2, so the answer must end in 2 as well.",
      wl("p", "the number looks like:  a b a"), wl("r", "the total looks like:  2 _ _ 2")),
    b("Look at the units. 7 plus our last digit must end in 2. Which digit does that?",
      ask=ch(["5", "2", "9"], "7 plus 5 makes a ten and 2 more, so it ends in 2. No other single digit does that.")),
    b("7 plus 5 is 12. So the last digit is 5, and because it is a palindrome, the first digit is 5 too.",
      w("u", "7 + 5 = 12"), wl("p2", "the number is:  5 b 5")),
    b("Now the middle digit. Try 0 in the middle first: 2017 plus 505 is 2522. Not a palindrome yet.", w("t0", "2017 + 505 = 2522")),
    b("Each time the middle digit goes up by 1, the total goes up by 10: 2522, 2532, 2542, 2552. Stop! 2552 reads the same backwards.",
      wl("seq", "2522, 2532, 2542, 2552"), ring("seq", "2552")),
    b("We went up 3 steps, so the middle digit is 3. The number is 535, and 2017 plus 535 is 2552.", w("t3", "2017 + 535 = 2552")),
    b("The question wants the digit sum of 535. 5 plus 3 plus 5 is 13.", w("s", "5 + 3 + 5 = 13")),
    b("So the answer is 13. Start from the units digit, because that is where a sum begins.", a("ans", "13"), ring("ans", "13")),
]

# Greatest 5-digit number from 9, 5, 0, 7, 3; difference of the place values of 5 and 3  -> 470
LESSONS["EXT_G5_FP_2018_022"] = [
    b("First we build the greatest 5 digit number from 9, 5, 0, 7 and 3. Then we compare what its 5 and its 3 are worth.",
      gl("q", "digits 9, 5, 0, 7, 3: greatest 5-digit number")),
    b("To make the greatest number, how do we arrange the digits?",
      ask=ch(["biggest digit first", "smallest digit first", "zero first"],
             "The places on the left are worth the most. So the biggest digits should go there, in order.")),
    b("9, 7, 5, 3, 0. The greatest number is 97530.", w("n", "97530"), fig("chart", pchart("97530", hi=[2, 3]))),
    b("The 5 has landed in the hundreds place. 5 times 100 is 500.",
      ul("n", "5"), nt("n", "5", "hundreds", "above"), w("va", "5 × 100 = 500")),
    b("The 3 is in the tens place. 3 times 10 is 30.", ul("n", "3"), nt("n", "3", "tens", "below"), w("vb", "3 × 10 = 30")),
    b("Difference means subtract. Careful: we subtract the place values, not the digits. 500 minus 30 is 470.", w("d", "500 − 30 = 470")),
    b("So the difference is 470.", al("ans", "Difference = 470"), ring("ans", "470")),
    b("Build the number, find each place value, then subtract. Three small steps, in that order."),
]

# The 27th even number after 27  -> 80
LESSONS["EXT_G5_FP_2019_014"] = [
    b("We want the 27th even number that comes after 27.", gl("q", "the 27th even number after 27")),
    b("27 is odd. So what is the first even number after it?",
      ask=ch(["28", "27", "29"], "Odd and even numbers take turns. One more than 27 is 28, and 28 is even.")),
    b("So the list starts 28, 30, 32, 34 and carries on in jumps of 2.", wl("l", "28, 30, 32, 34, …")),
    b("28 is the 1st. To reach the 27th we need 26 more jumps. Careful: 26, not 27, because 28 itself is already counted.",
      w("j", "27 − 1 = 26")),
    b("26 jumps of 2 cover 52.", w("m", "26 × 2 = 52")),
    b("28 plus 52 is 80.", w("s", "28 + 52 = 80")),
    b("A quick test of the method on a small case: the 2nd even number should be 28 plus 1 jump, which is 30. Yes, it is.",
      w("c", "28 + 1 × 2 = 30")),
    b("So the 27th even number after 27 is 80. Find the first one, then add one jump fewer than the position.",
      a("ans", "80"), ring("ans", "80")),
]

# Digits 2, 3, 4, 5: numbers with 5 in the hundreds place  -> 6
LESSONS["EXT_G5_FP_2019_020"] = [
    b("All the 4 digit numbers made from 2, 3, 4 and 5, each used once. In how many is the 5 in the hundreds place?",
      gl("q", "digits 2, 3, 4, 5: numbers with 5 in the hundreds")),
    b("Let's pin the 5 where it has to be. The hundreds place is taken, and three places are still empty.",
      fig("table", tbl(PLACES4, [["?", "5", "?", "?"]]))),
    b("Which digits are left to fill the empty places?",
      ask=ch(["2, 3 and 4", "2, 3, 4 and 5", "any digits at all"],
             "Each digit is used only once, and the 5 is already taken. So only 2, 3 and 4 are left.")),
    b("For the thousands place we can pick any of the 3. Then 2 are left for the tens, and 1 for the units.", w("m", "3 × 2 × 1 = 6")),
    b("Let's list them: 2534, 2543, 3524, 3542, 4523, 4532. Every one has 5 in the hundreds place.",
      wl("l", "2534, 2543, 3524, 3542, 4523, 4532")),
    b("So there are 6 such numbers.", al("ans", "6 numbers"), ring("ans", "6")),
    b("Pin down the place that is decided. Then count the choices for the others and multiply."),
]

# Rearrange the digits of 75003064 to form the smallest number  -> 30004567
LESSONS["EXT_G5_FP_2019_030"] = [
    b("Here is 75003064. We may shuffle its digits any way we like, to make the smallest number we can.", g("n", "75003064")),
    b("First sort the digits from smallest to biggest. There are three zeros, then 3, 4, 5, 6 and 7.",
      wl("d", "in order: 0, 0, 0, 3, 4, 5, 6, 7")),
    b("The smallest digit is 0. Can our number start with 0?",
      ask=ch(["No, it would lose a digit", "Yes, 0 is the smallest"],
             "A zero at the front is never written, so the number would become shorter. We need the smallest digit that is not zero.")),
    b("So 3 goes first.", wl("n1", "3 . . . . . . .")),
    b("Now the zeros are welcome. They go straight after the 3, in the biggest places left, where they keep the number small.",
      wl("n2", "3 0 0 0 . . . .")),
    b("Then the rest in rising order: 4, 5, 6, 7. That makes 30004567.", w("n3", "30004567"), fig("chart", pchart("30004567"))),
    b("Careful: 30405067 also starts with 3, but it spends a 4 in the lakhs place where a 0 could go. Ours is smaller.",
      w("k", "30004567 < 30405067")),
    b("So the smallest number is 30004567. Smallest digit that is not zero first, then the zeros, then the rest in order.",
      a("ans", "30004567"), ring("ans", "30004567")),
]

# In 87459, how many times is the place value of 7 to that of 5?  -> 140
LESSONS["EXT_G5_FP_2019_037"] = [
    b("Here is 87459. We compare what the 7 is worth with what the 5 is worth.",
      g("n", "87459"), ul("n", "7"), nt("n", "7", "thousands", "above"), ul("n", "5"), nt("n", "5", "tens", "below")),
    b("Find them in the chart. What is the 7 worth?",
      fig("chart", pchart("87459", hi=[1, 3])),
      ask=ch(["7000", "700", "7"], "Count from the right: units, tens, hundreds, thousands. So the 7 means 7 thousands.")),
    b("7 times 1000 is 7000. And the 5 is in the tens place, so it is worth 5 times 10, which is 50.",
      w("va", "7 × 1000 = 7000"), w("vb", "5 × 10 = 50")),
    b("'How many times' is which sum?",
      ask=ch(["7000 ÷ 50", "1000 ÷ 10", "7000 − 50"],
             "1000 divided by 10 compares the columns only, and forgets the digits 7 and 5. We divide the full place values.")),
    b("7000 divided by 50. Cross a zero off each to make it easier: 700 divided by 5 is 140.",
      w("d", "7000 ÷ 50 = 140"), w("e", "700 ÷ 5 = 140")),
    b("Check: 140 times 50 gives back 7000.", w("c", "140 × 50 = 7000")),
    b("So the place value of the 7 is 140 times the place value of the 5.", al("ans", "140 times"), ring("ans", "140")),
    b("The digits are different here, so comparing the columns alone is not enough. Always divide the full place values."),
]
