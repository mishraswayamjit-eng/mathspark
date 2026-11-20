"""Lessons written one by one: hand-written questions Q_CH13_001 to 013."""
from g4_gr4_algebra_lib import (B, L, T, W, answer, arc, choose, fig, given, group, last_num, lesson, mark, note,
                                strike, under)

LESSONS = {}

# If a = 3, find the value of a + 4.   (7)
LESSONS["Q_CH13_001"] = lesson([
    B("The letter a is standing in for a number. We are told that a is 3. We want the value of a plus 4.",
      given("g1", "a = 3", label=True), given("g2", "a + 4", label=True)),
    B("What do we do with the letter a?",
      ask=choose(["swap it for 3", "write 3 next to the 4", "leave it as a letter"], 0,
                 "a is just a name tag for the number 3. So wherever we see a, we take it out "
                 "and put 3 in its place.")),
    B("Rub out the a and put 3 in its place. Now it says 3 plus 4.",
      strike("g2", "a", "3"), W("l1", "3 + 4")),
    B("The sign between them is a plus. So what do we do with the 3 and the 4?",
      ask=choose(["add them", "write them side by side", "multiply them"], 0,
                 "The plus sign is still there, and it tells us to add. "
                 "We do not just write the two digits next to each other.")),
    B("3 plus 4 is 7.", answer("a1", "3 + 4 = 7"), mark("a1", "7")),
    B("So when a is 3, a plus 4 is 7. Swap the letter for its number, then do what the sign says."),
])

# If a = 3, find the value of 4a.   (12)
LESSONS["Q_CH13_002"] = lesson([
    B("a is 3. We want the value of 4 a. Look: the 4 and the a are side by side, with no sign between them.",
      given("g1", "a = 3", label=True), given("g2", "4a", label=True)),
    B("There is a hidden sign between the 4 and the a. Which one is it?",
      ask=choose(["times", "plus", "no sign: it means 43"], 0,
                 "In algebra, a number right next to a letter means multiply. So 4 a means 4 times a. "
                 "It is 4 lots of a.")),
    B("4 a means 4 times a. I'll write the hidden sign in.", L("l1", "4a = 4 × a")),
    B("Now swap the a for 3. We get 4 times 3.", note("l1", T("a", 2), "3"), W("l2", "4 × 3")),
    B("4 times 3 is 12.", answer("a1", "4 × 3 = 12"), mark("a1", "12")),
    B("Watch out for two slips. 4 plus 3 is 7, but nothing here says add. "
      "And 4 a is not the digits 4 and 3 written side by side."),
    B("A number next to a letter always means times. So 4 a is 4 times 3, which is 12."),
])

# If a = 3, find the value of 2a/3.   (2)
LESSONS["Q_CH13_003"] = lesson([
    B("a is 3. We want 2 a over 3. The sloping line means divided by. So this is 2 a, divided by 3.",
      given("g1", "a = 3", label=True), given("g2", "2a/3", label=True)),
    B("What do we work out first?",
      ask=choose(["2a, the top part", "a ÷ 3", "3 ÷ 3"], 0,
                 "The whole of 2 a is being divided by 3. So we need to know what 2 a is before we can divide it.")),
    B("2 a means 2 times a. And a is 3, so 2 a is 2 times 3, which is 6.",
      under("g2", "2a"), W("l1", "2 × 3 = 6")),
    B("Are we finished at 6?",
      ask=choose(["No, divide by 3 next", "Yes, the answer is 6"], 0,
                 "6 is only the top part, 2 a. The expression still says divided by 3. So there is one more step.")),
    B("Now divide by 3. 6 divided by 3 is 2.", answer("a1", "6 ÷ 3 = 2"), mark("a1", "2")),
    B("So 2 a over 3 is 2. Work out the top first, then divide by the bottom."),
])

# If a = 3, find the value of (a + 12)/3.   (5)
LESSONS["Q_CH13_004"] = lesson([
    B("a is 3. We want a plus 12, in a bracket, all divided by 3.",
      given("g1", "a = 3", label=True), given("g2", "(a + 12)/3", label=True)),
    B("What does the bracket tell us to do first?",
      ask=choose(["add a and 12", "divide 12 by 3", "divide a by 3"], 0,
                 "A bracket is a parcel. Whatever is inside gets done first. "
                 "So we add a and 12 before any dividing.")),
    B("Inside the bracket: a plus 12. a is 3, so that is 3 plus 12, which is 15.",
      under("g2", "(a + 12)"), W("l1", "3 + 12 = 15")),
    B("Now the whole 15 is divided by 3. Not just the a, and not just the 12. The whole parcel.",
      W("l2", "15 ÷ 3")),
    B("15 divided by 3 is 5.", answer("a1", "15 ÷ 3 = 5"), mark("a1", T("5", 2))),
    B("If we divided only the a by 3, we would get 1, and then 1 plus 12 is 13. "
      "That is a different sum, because it ignores the bracket.",
      W("l3", "3 ÷ 3 + 12 = 13")),
    B("Bracket first, then divide the whole result. So the value is 5."),
])

# If a = 3, find the value of a².   (9)
LESSONS["Q_CH13_005"] = lesson([
    B("a is 3. We want a squared. That is the a with a small 2 sitting up high.",
      given("g1", "a = 3", label=True), given("g2", "a²", label=True)),
    B("What does the small 2 tell us to do?",
      ask=choose(["multiply a by itself", "multiply a by 2", "add 2 to a"], 0,
                 "The small 2 is not an ordinary number. It says: use a two times, multiplied together. "
                 "So a squared is a times a.")),
    B("a squared means a times a.", L("l1", "a² = a × a")),
    B("Swap each a for 3. That gives 3 times 3.",
      note("l1", T("a", 2), "3"), note("l1", T("a", 3), "3"), W("l2", "3 × 3")),
    B("3 times 3 is 9.", answer("a1", "3 × 3 = 9"), mark("a1", "9")),
    B("Here is the most common slip: doing 3 times 2 and getting 6. Squared never means times 2.",
      W("l3", "3 × 2 = 6"), strike("l3", "× 2", "not times 2")),
    B("Squared means the number times itself. So a squared is 3 times 3, which is 9."),
])

# If a = 3, find the value of 4a².   (36)
LESSONS["Q_CH13_006"] = lesson([
    B("a is 3. We want 4 a squared. There is a 4, an a, and a small 2 up high.",
      given("g1", "a = 3", label=True), given("g2", "4a²", label=True)),
    B("Who does the small 2 belong to?",
      ask=choose(["only the a", "the 4 and the a together", "only the 4"], 0,
                 "The small 2 sits on the a, so it belongs to the a alone. The 4 is not squared.")),
    B("So we square the a first. a squared is a times a. That is 3 times 3, which is 9.",
      under("g2", "a²"), W("l1", "3 × 3 = 9")),
    B("Now, what do we do with the 4?",
      ask=choose(["multiply: 4 × 9", "add: 4 + 9", "nothing, we are done"], 0,
                 "4 a squared means 4 times a squared. A number next to a letter always means times. "
                 "So it is 4 times 9.")),
    B("4 times 9 is 36.", answer("a1", "4 × 9 = 36"), mark("a1", "36")),
    B("The trap is to do 4 times 3 first, and then square the 12. "
      "That gives a much bigger number, because it squares the 4 as well.",
      W("l2", "4 × 3 = 12")),
    B("Squares come first, then the times. So 4 a squared is 4 times 9, which is 36."),
])

# If a = 3 and b = 5, find the value of 4ab.   (60)
LESSONS["Q_CH13_007"] = lesson([
    B("a is 3 and b is 5. We want 4 a b. A number and two letters, all side by side.",
      given("g1", "a = 3, b = 5", label=True), given("g2", "4ab", label=True)),
    B("What does 4 a b mean?",
      ask=choose(["4 × a × b", "4 × a + b", "4 + a + b"], 0,
                 "When things stand side by side with no sign, they are all multiplied. "
                 "So 4 a b is 4 times a times b.")),
    B("So 4 a b means 4 times a times b. Nothing is added.", L("l1", "4ab = 4 × a × b")),
    B("Swap a for 3 and b for 5. We get 4 times 3 times 5.",
      note("l1", T("a", 2), "3"), note("l1", T("b", 2), "5"), W("l2", "4 × 3 × 5")),
    B("Multiply two at a time. 4 times 3 is 12. That 12 is only 4 a. We still have to multiply by b.",
      W("l3", "4 × 3 = 12")),
    B("So now 12 times 5. What is that?",
      ask=choose(["60", "17", "125"], 0,
                 "Think of 12 as 10 and 2. Multiply each of them by 5, then add the two answers.")),
    B("10 times 5 is 50, and 2 times 5 is 10. 50 plus 10 is 60.",
      W("l4", "10 × 5 + 2 × 5 = 50 + 10 = 60"), answer("a1", "12 × 5 = 60"), mark("a1", "60")),
    B("So 4 a b is 60. Side by side means times, for every number and letter in the row."),
])

# If a = 3 and b = 5, find the value of 4a + b.   (17)
LESSONS["Q_CH13_008"] = lesson([
    B("a is 3 and b is 5. We want the value of 4 a plus b.",
      given("g1", "a = 3, b = 5", label=True), given("g2", "4a + b", label=True)),
    B("What does 4 a mean here?",
      ask=choose(["4 × 3", "4 + 3", "4 × 5"], 0,
                 "4 a is 4 times a. And a is 3, not 5. Each letter has its own number. So 4 a is 4 times 3.")),
    B("Swap the letters for their numbers. 4 a becomes 4 times 3. And b becomes 5.",
      note("g2", "a", "3"), note("g2", "b", "5"), W("l1", "4 × 3 + 5")),
    B("Times goes before plus. 4 times 3 is 12.", under("l1", "4 × 3"), W("l2", "4 × 3 = 12")),
    B("Is 12 the answer?",
      ask=choose(["No, add b", "Yes, it is 12"], 0,
                 "12 is only 4 a. The expression says plus b, and b is 5. So we add 5.")),
    B("12 plus 5 is 17.", answer("a1", "12 + 5 = 17"), mark("a1", "17")),
    B("So 4 a plus b is 17. Swap the letters, do the times first, and do not forget the part that is added."),
])

# If a = 3 and b = 5, find the value of 6b − 4a.   (18)
LESSONS["Q_CH13_009"] = lesson([
    B("a is 3 and b is 5. We want 6 b minus 4 a. Notice that b comes first this time.",
      given("g1", "a = 3, b = 5", label=True), given("g2", "6b − 4a", label=True)),
    B("First part: 6 b. That is 6 times b, and b is 5. 6 times 5 is 30.",
      under("g2", "6b"), W("l1", "6 × 5 = 30")),
    B("Second part: 4 a. Which sum is that?",
      ask=choose(["4 × 3", "4 × 5", "4 + 3"], 0,
                 "4 a is 4 times a. And a is 3. Each letter keeps its own number.")),
    B("4 times 3 is 12.", under("g2", "4a"), W("l2", "4 × 3 = 12")),
    B("Now we have 30 and 12. What does the sign between the two parts tell us?",
      ask=choose(["take 12 from 30", "add 12 to 30"], 0,
                 "The sign between 6 b and 4 a is a minus. So the second part is taken away from the first.")),
    B("30 minus 12 is 18.", answer("a1", "30 − 12 = 18"), mark("a1", "18")),
    B("Work out each part with its own letter first, and only then subtract. "
      "The trap is to do 6 minus 4 first: that mixes up the two letters."),
])

# If a = 3 and b = 5, find the value of 12 − 5a + 3b.   (12)
_L10 = "12 − 15 + 15 = 12"
LESSONS["Q_CH13_010"] = lesson([
    B("a is 3 and b is 5. We want 12, minus 5 a, plus 3 b.",
      given("g1", "a = 3, b = 5", label=True), given("g2", "12 − 5a + 3b", label=True)),
    B("Work out the letter parts first. 5 a is 5 times 3, which is 15. 3 b is 3 times 5, which is 15 too.",
      W("l1", "5 × 3 = 15"), W("l2", "3 × 5 = 15")),
    B("Put them back, each with the sign in front of it. 12, minus 15, plus 15.", W("l3", "12 − 15 + 15")),
    B("Look at the signs. Which part is taken away, and which is added?",
      ask=choose(["5a is taken away, 3b is added", "both are taken away", "both are added"], 0,
                 "Each part keeps the sign in front of it. There is a minus in front of 5 a, "
                 "and a plus in front of 3 b.")),
    B("12 minus 15 looks hard, because 15 is bigger than 12. But look closer. "
      "We take 15 away, and then we put 15 straight back.",
      under("l3", "− 15"), under("l3", "+ 15")),
    B("Taking 15 away and then adding 15. What does that do to the 12?",
      ask=choose(["nothing, it stays 12", "it makes 0", "it makes 30"], 0,
                 "Taking something away and then putting the same amount back leaves you where you started. "
                 "The two 15s undo each other.")),
    B("The minus 15 and the plus 15 cancel each other. We are left with 12.",
      strike("l3", "− 15"), strike("l3", "+ 15"), answer("a1", _L10), mark("a1", last_num(_L10, 12))),
    B("So the value is 12. Keep each sign with its own part. "
      "And when the same number is taken away and added, the two cancel."),
])

# If a = 3 and b = 5, find the value of 4(a + b).   (32)
LESSONS["Q_CH13_011"] = lesson([
    B("a is 3 and b is 5. We want 4 times a plus b, with a plus b in a bracket.",
      given("g1", "a = 3, b = 5", label=True), given("g2", "4(a + b)", label=True)),
    B("A bracket, with a 4 outside. What do we do first?",
      ask=choose(["a + b, inside the bracket", "4 × a"], 0,
                 "A bracket is done first. So we add a and b before the 4 does anything.")),
    B("Inside the bracket: a plus b is 3 plus 5, which is 8.", under("g2", "(a + b)"), W("l1", "3 + 5 = 8")),
    B("The 4 is right next to the bracket. What does it do to the 8?",
      ask=choose(["multiplies it: 4 × 8", "is added to it: 4 + 8"], 0,
                 "A number touching a bracket multiplies the whole bracket. So it is 4 times 8.")),
    B("4 times 8 is 32.", answer("a1", "4 × 8 = 32"), mark("a1", "32")),
    B("Another way gives the same. 4 times 3 is 12, 4 times 5 is 20, and 12 plus 20 is 32. "
      "The 4 multiplies both a and b.",
      arc("g2", "4", "a", "b"), W("l2", "4 × 3 + 4 × 5 = 12 + 20 = 32")),
    B("The trap is to multiply only one of the letters by 4. The 4 multiplies the whole bracket. The value is 32."),
])

# What is half of the square of t?   (t²/2)
LESSONS["Q_CH13_012"] = lesson([
    B("Words into algebra. Half of the square of t. Two things happen here: a squaring and a halving.",
      given("g1", "half of the square of t", label=True)),
    B("Which one happens first?",
      ask=choose(["square t, then halve", "halve t, then square"], 0,
                 "The square of t is the thing, and we want half of that thing. "
                 "So the square has to be made first.")),
    B("The square of t is t times t. We write it as t squared.",
      under("g1", "the square of t"), L("l1", "t × t = t²")),
    B("Now half of that. What does half mean?",
      ask=choose(["divide by 2", "multiply by 2", "take away 2"], 0,
                 "Half means split into 2 equal parts and keep one of them. That is dividing by 2.")),
    B("Half means divide by 2. So we write t squared over 2.",
      under("g1", "half of"), answer("a1", "t²/2", label=True), mark("a1", "t²/2")),
    B("Try it with t as 4. The square of 4 is 16. And half of 16 is 8.",
      W("l2", "4 × 4 = 16"), W("l3", "16 ÷ 2 = 8")),
    B("If we halved first, we would get 2, and 2 times 2 is only 4. Not the same! So the order matters.",
      W("l4", "4 ÷ 2 = 2"), W("l5", "2 × 2 = 4")),
    B("Square first, then halve. That is t squared, divided by 2."),
])

# The sum of d and its successor   (2d + 1)
LESSONS["Q_CH13_013"] = lesson([
    B("We want the sum of d and its successor. The successor of a number is the one that comes just after it.",
      given("g1", "d and its successor", label=True), fig("Q_CH13_013")),
    B("What is the successor of d?",
      ask=choose(["d + 1", "d + 2", "2d"], 0,
                 "The next number is always 1 more. The successor of 5 is 6. So the successor of d is d plus 1.")),
    B("The successor of d is d plus 1.", W("l1", "d + 1"), note("l1", "d + 1", "successor")),
    B("Sum means add. So we add d, and d plus 1.", W("l2", "d + d + 1")),
    B("Look at d plus d. What is that?",
      ask=choose(["2d", "d²", "d"], 0,
                 "One d and another d make two d's. We write 2 d. "
                 "d squared would be d times d, which is something else.")),
    B("Two d's make 2 d. The extra 1 stays. So the sum is 2 d plus 1.",
      group("l2", [T("d", 1), T("d", 2)], "2d"), answer("a1", "d + d + 1 = 2d + 1"), mark("a1", "2d + 1")),
    B("Check with d as 5. Its successor is 6, and 5 plus 6 is 11. And 2 times 5, plus 1, is 11.",
      W("l3", "5 + 6 = 11"), W("l4", "2 × 5 + 1 = 11")),
    B("Write the second number using the letter first. Then add like with like. The sum is 2 d plus 1."),
], "d", 1)
