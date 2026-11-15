"""Lessons written by hand: adding and dividing expressions, writing an expression, substitution with a twist."""
from algebra_lib import B, W, answer, arc, choose, given, group, lesson, mark, note, strike

LESSONS = {}

# Sum of a + b − 1, b − a + 1 and 1 − 2b
LESSONS["EXT_G5_FP_2016_022"] = lesson([
    B("We have three expressions, and sum means add them all. So I write them in one long line.",
      given("l1", "(a + b − 1) + (b − a + 1) + (1 − 2b)", label=True)),
    B("Look for partners that cancel. Which term cancels the very first a?",
      ask=choose(["+ b", "− a", "− 1"], 1,
                 "a and minus a are opposites. Put together, they make nothing at all.")),
    B("So a and minus a cancel. I cross them both out.",
      strike("l1", ("a", 1)), strike("l1", "− a", "0"), W("l2", "a − a = 0", label=True)),
    B("Now the b terms. There is a b, another b, and a minus 2 b. What do they make together?",
      ask=choose(["2b", "0", "4b"], 1,
                 "b and b make 2 b. Then minus 2 b takes both of them away again. Nothing is left.")),
    B("One b and another b make 2 b, and then minus 2 b takes them away. So the b terms vanish too.",
      group("l1", ["+ b", ("b", 2), "− 2b"], "0"), W("l3", "b + b − 2b = 0", label=True)),
    B("Only the plain numbers are left: minus 1, plus 1, and plus 1. Minus 1 and plus 1 cancel, so 1 remains.",
      group("l1", ["− 1", "+ 1", ("1", 3)], "1"), W("l4", "−1 + 1 + 1 = 1")),
    B("So the whole sum is just 1. All those letters, and they disappear completely!",
      answer("l5", "0 + 0 + 1 = 1"), mark("l5", ("1", 2))),
    B("Let's test with real numbers. Say a is 2 and b is 3. The three parts become 4, 2 and minus 5. "
      "And 4 plus 2 minus 5 is 1.",
      W("l6", "4 + 2 − 5 = 1")),
    B("To add expressions: write them in a line, then gather each family. a with a, b with b, numbers with numbers."),
])

# (4w + 5s − 3r) + (2w − 3s + 2r) + (4s − 3w + 4r)
LESSONS["EXT_G5_FP_2022_026"] = lesson([
    B("The word solve here really means simplify. Three brackets are added together, "
      "and there are three families of letters: w, s and r.",
      given("l1", "(4w + 5s − 3r) + (2w − 3s + 2r) + (4s − 3w + 4r)", label=True)),
    B("Let's start with the w family. Which terms go with 4 w?",
      ask=choose(["5s and − 3r", "2w and − 3w", "2w and 4s"], 1,
                 "Like terms have the same letter. So 4 w goes with the other w terms: 2 w, and minus 3 w.")),
    B("4 w plus 2 w is 6 w, and minus 3 w leaves 3 w.",
      group("l1", ["4w", "2w", "− 3w"], "3w"), W("l2", "4 + 2 − 3 = 3")),
    B("Now the s family. 5 s minus 3 s is 2 s, and 4 s more makes 6 s.",
      group("l1", ["5s", "− 3s", "4s"], "6s"), W("l3", "5 − 3 + 4 = 6")),
    B("Now the r family: minus 3 r, plus 2 r, plus 4 r. Careful with that first sign. How many r is that?",
      ask=choose(["9r", "3r", "−3r"], 1,
                 "The first one is minus 3 r, so we start 3 below zero. Plus 2 brings us to minus 1, "
                 "and plus 4 brings us up to 3. So 3 r.")),
    B("Minus 3, plus 2, plus 4 comes to 3. So that is 3 r.",
      group("l1", ["− 3r", "+ 2r", "+ 4r"], "3r"), W("l4", "−3 + 2 + 4 = 3")),
    B("Put the three families side by side: 6 s plus 3 w plus 3 r. "
      "The order does not matter, as long as each sign stays with its own term.",
      answer("l5", "6s + 3w + 3r", label=True), mark("l5", "6s + 3w + 3r")),
    B("Test it with every letter as 1. The three brackets give 6, 1 and 5, which add up to 12. "
      "And 6 plus 3 plus 3 is 12 as well.",
      W("l6", "6 + 1 + 5 = 12"), W("l7", "6 + 3 + 3 = 12")),
    B("So to add long expressions: take one letter family at a time, and keep the sign in front of each term."),
])

# (12xy + 8y) ÷ 4y
LESSONS["EXT_G5_FP_2017_037"] = lesson([
    B("We are dividing 12 x y plus 8 y by 4 y. Quotient is just the name for the answer to a division.",
      given("l1", "(12xy + 8y) ÷ 4y", label=True)),
    B("There are two parts being divided. What does the 4 y divide?",
      ask=choose(["only the 12xy", "each part, one at a time", "only the 8y"], 1,
                 "When a sum is divided, every part of the sum is divided. "
                 "Like sharing 2 bags of sweets: you share out each bag.")),
    B("So we split it into two little divisions. 12 x y divided by 4 y, and 8 y divided by 4 y.",
      arc("l1", "4y", "12xy", "8y"), W("l2", "12xy ÷ 4y    and    8y ÷ 4y", label=True)),
    B("Take the first one. Numbers first: 12 divided by 4 is 3. "
      "Then the letters: there is a y on top and a y underneath.",
      W("l3", "12 ÷ 4 = 3")),
    B("What is y divided by y?",
      ask=choose(["0", "1", "y"], 1,
                 "Any number divided by itself is 1. 7 divided by 7 is 1, and y divided by y is 1 too. "
                 "So the y simply cancels.")),
    B("So the y cancels, and the x is left. 12 x y divided by 4 y is 3 x.",
      W("l4", "12xy ÷ 4y = 3x", label=True), strike("l4", ("y", 1)), strike("l4", ("y", 2))),
    B("Now the second part. 8 divided by 4 is 2, and the y cancels again. So we just get 2.",
      W("l5", "8 ÷ 4 = 2"), W("l6", "8y ÷ 4y = 2", label=True)),
    B("Put the two answers together: 3 x plus 2.",
      answer("l7", "3x + 2", label=True), mark("l7", "3x + 2")),
    B("Check by multiplying back. 4 y times 3 x is 12 x y, and 4 y times 2 is 8 y. "
      "That is exactly what we started with.",
      W("l8", "4y × (3x + 2) = 12xy + 8y", label=True)),
    B("To divide a sum: divide each part, numbers by numbers, "
      "and cancel any letter that is on both the top and the bottom."),
])

# Which expression divides 91abc to get 7c?
LESSONS["EXT_G5_FP_2018_027"] = lesson([
    B("Something divides 91 a b c and gives 7 c. We have to find that something.",
      given("l1", "91abc ÷ ? = 7c", label=True)),
    B("Try the idea with small numbers. 12 divided by 4 is 3. "
      "And if we did not know the 4, we could find it: 12 divided by 3 is 4.",
      W("l2", "12 ÷ 4 = 3"), W("l3", "12 ÷ 3 = 4")),
    B("So to find a missing divider, we divide the big one by the answer. "
      "Our missing piece is 91 a b c divided by 7 c.",
      W("l4", "? = 91abc ÷ 7c", label=True)),
    B("Numbers first. What is 91 divided by 7?",
      ask=choose(["12", "13", "14"], 1,
                 "Try 7 times 13. 7 times 10, and 7 times 3, added together make 91. So 91 divided by 7 is 13.")),
    B("91 divided by 7 is 13.",
      W("l5", "91 ÷ 7 = 13")),
    B("Now the letters: a b c divided by c. What is left?",
      ask=choose(["abc", "ab", "c"], 1,
                 "There is a c on top and a c underneath. c divided by c is 1, so the c cancels. Only a b is left.")),
    B("The c on top and the c below cancel each other, leaving a b.",
      W("l6", "abc ÷ c = ab", label=True), strike("l6", ("c", 1)), strike("l6", ("c", 2))),
    B("Put the number and the letters together: 13 a b.",
      answer("l7", "13ab", label=True), mark("l7", "13ab")),
    B("Check by multiplying back. 13 times 7 is 91, and a b times c is a b c. "
      "So 13 a b times 7 c really is 91 a b c.",
      W("l8", "13 × 7 = 91"), W("l9", "13ab × 7c = 91abc", label=True)),
    B("So to find a missing divider, divide by the answer instead. Numbers with numbers, and cancel matching letters."),
])

# Arnav m messages an hour for 5 hours, Pranav p an hour for 4 hours.
LESSONS["EXT_G5_FP_2020_002"] = lesson([
    B("Two friends are sending messages. Arnav sends m messages every hour, for 5 hours. "
      "Pranav sends p every hour, for 4 hours. We want the total.",
      given("l1", "Arnav: m each hour, for 5 hours", label=True),
      given("l2", "Pranav: p each hour, for 4 hours", label=True)),
    B("Imagine m was 3. Then Arnav sends 3, and 3, and 3, and 3, and 3. That is 5 lots of 3.",
      W("l3", "3 + 3 + 3 + 3 + 3 = 5 × 3")),
    B("So with m messages each hour, for 5 hours, how many does Arnav send?",
      ask=choose(["m + 5", "5m", "m"], 1,
                 "m each hour for 5 hours is m, 5 times over. And 5 lots of m is written 5 m.")),
    B("5 lots of m. We write that as 5 m.",
      W("l4", "Arnav = 5 × m = 5m", label=True), mark("l4", "5m", "underline")),
    B("Pranav is the same idea. p messages each hour for 4 hours is 4 lots of p, which is 4 p.",
      W("l5", "Pranav = 4 × p = 4p", label=True), mark("l5", "4p", "underline")),
    B("Total means add. Can we join 5 m and 4 p into one term, like 9 m p?",
      ask=choose(["Yes: 9mp", "No: m and p are different letters"], 1,
                 "m and p stand for different numbers, so they are not like terms. "
                 "We can only write them side by side, with a plus between.")),
    B("So the total is 5 m plus 4 p.",
      answer("l6", "5m + 4p", label=True), mark("l6", "5m + 4p")),
    B("Test it. Say m is 2 and p is 3. Arnav sends 10, Pranav sends 12, and that is 22 altogether. "
      "And 5 times 2, plus 4 times 3, is 22.",
      W("l7", "5 × 2 = 10"), W("l8", "4 × 3 = 12"), W("l9", "10 + 12 = 22")),
    B("So so many each hour, for so many hours, means multiply. And different letters always stay apart."),
])

# If a/b = 2, what is 4b/a?
LESSONS["EXT_G5_FP_2020_022"] = lesson([
    B("We are not told a or b. We only know that a divided by b is 2. Yet that is enough to find 4 b over a.",
      given("l1", "a/b = 2", label=True), given("l2", "4b/a = ?", label=True)),
    B("a divided by b is 2. What does that tell us about a and b?",
      ask=choose(["b is 2 times a", "a is 2 times b", "a is 2 more than b"], 1,
                 "10 divided by 5 is 2, because 10 is 2 times 5. In the same way, "
                 "a divided by b is 2 means a is 2 times b.")),
    B("So a is double b. Let's pick an easy pair that fits: b is 1 and a is 2.",
      W("l3", "a = 2 × b", label=True), W("l4", "try b = 1, a = 2", label=True)),
    B("Now work out 4 b over a. 4 times 1 is 4, and 4 divided by 2 is 2.",
      W("l5", "4 × 1 ÷ 2 = 2")),
    B("Was that luck? Try another pair: b is 3 and a is 6. 4 times 3 is 12, and 12 divided by 6 is 2 again.",
      W("l6", "try b = 3, a = 6", label=True), W("l7", "4 × 3 = 12"), W("l8", "12 ÷ 6 = 2")),
    B("Here is why it always works. If a over b is 2, what is b over a, the fraction flipped?",
      ask=choose(["2", "1/2", "−2"], 1,
                 "Flipping a fraction turns it upside down. 2 is 2 over 1, so upside down it is 1 over 2, a half.")),
    B("b over a is a half. And 4 b over a is 4 times that. 4 times a half is 2.",
      W("l9", "b/a = 1/2", label=True), answer("l10", "4 × 1/2 = 2"), mark("l10", ("2", 2))),
    B("So when you only know how two letters compare, try easy numbers that fit, then look for the reason. "
      "The answer is 2."),
])

# x = 3, y = −2: xy/(x − y)
LESSONS["EXT_G5_FP_2021_015"] = lesson([
    B("x is 3 and y is minus 2. We need x y, over x minus y. "
      "The negative number makes this one a little tricky, so we go slowly.",
      given("l1", "x = 3,  y = −2", label=True), given("l2", "xy/(x − y)", label=True)),
    B("Do the top first. x y means x times y, so that is 3 times minus 2. What is 3 times minus 2?",
      note("l2", "xy", "3 × (−2)"),
      ask=choose(["6", "−6", "1"], 1,
                 "3 lots of minus 2 is minus 2, minus 2, minus 2. That is minus 6. "
                 "A positive times a negative is negative.")),
    B("So the top is minus 6.",
      W("l3", "3 × (−2) = −6")),
    B("Now the bottom: x minus y. That is 3, minus, minus 2. What does that come to?",
      note("l2", "(x − y)", "3 − (−2)", "below"),
      ask=choose(["1", "5", "−5"], 1,
                 "Taking away a negative is the same as adding. So 3 minus minus 2 is 3 plus 2, which is 5. "
                 "Writing 3 minus 2 here is the classic slip.")),
    B("Taking away minus 2 is the same as adding 2. So the bottom is 3 plus 2, which is 5.",
      W("l4", "3 − (−2) = 3 + 2"), W("l5", "3 + 2 = 5")),
    B("Top over bottom: minus 6 over 5. It does not divide exactly, so we leave it as a fraction.",
      answer("l6", "−6 ÷ 5 = −6/5"), mark("l6", "−6/5")),
    B("A quick sense check. The top is negative and the bottom is positive, so the answer should be negative. "
      "And it is: minus 6 over 5."),
    B("So: put the numbers in, with brackets round any negative. "
      "Work out the top and the bottom separately, then divide."),
])

# a = 17, b = (a − 1) ÷ 2, c = b + 3: a² − c² + b²
LESSONS["EXT_G5_FP_2025_037"] = lesson([
    B("Three letters, but only a is given. b is built from a, and c is built from b. So we find them in that order.",
      given("l1", "a = 17,  b = (a − 1) ÷ 2,  c = b + 3", label=True), given("l2", "a² − c² + b² = ?", label=True)),
    B("b first. a minus 1 is 17 minus 1, which is 16. Half of 16 is 8. So b is 8.",
      W("l3", "17 − 1 = 16"), W("l4", "16 ÷ 2 = 8"), note("l4", "8", "b")),
    B("Then c is b plus 3. 8 plus 3 is 11.",
      W("l5", "8 + 3 = 11"), note("l5", "11", "c")),
    B("Now the squares. What does a squared mean, when a is 17?",
      ask=choose(["17 × 2", "17 × 17", "17 + 17"], 1,
                 "Squared means the number times itself. So 17 squared is 17 times 17, not 17 times 2.")),
    B("17 times 17 is 289. 11 times 11 is 121. And 8 times 8 is 64.",
      W("l6", "17² = 289"), W("l7", "11² = 121"), W("l8", "8² = 64")),
    B("So we have 289, minus 121, plus 64. Which do we do first?",
      W("l9", "289 − 121 + 64"),
      ask=choose(["121 + 64", "289 − 121", "either way is fine"], 1,
                 "Plus and minus are done from left to right. Adding 121 and 64 first would take away too much.")),
    B("289 minus 121 is 168. Then 168 plus 64 is 232.",
      W("l10", "289 − 121 = 168"), answer("l11", "168 + 64 = 232"), mark("l11", "232")),
    B("So: find the letters in order, square each one, then work from left to right. The answer is 232."),
])
