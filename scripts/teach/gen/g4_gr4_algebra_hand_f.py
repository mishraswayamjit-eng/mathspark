"""Lessons written one by one: hand-written questions Q_CH13_014 to 025."""
from g4_gr4_algebra_lib import (B, L, T, W, answer, choose, fig, given, group, lesson, mark, note, strike, under)

LESSONS = {}

# Diya has m ten-rupee notes. Total amount?   (₹10m)
LESSONS["Q_CH13_014"] = lesson([
    B("Diya has m ten rupee notes. The m stands for how many notes she has. We want the total amount of money.",
      given("g1", "m notes of ₹10 each", label=True), fig("Q_CH13_014")),
    B("Try it with numbers first. 2 notes are worth 20 rupees. 3 notes are worth 30 rupees.",
      W("l1", "10 × 2 = 20"), W("l2", "10 × 3 = 30")),
    B("What did we do each time to get the total?",
      ask=choose(["10 times the number of notes", "10 plus the number of notes", "the number of notes divided by 10"], 0,
                 "Each note brings 10 rupees. Two notes bring 10 and 10. "
                 "So we multiply 10 by the number of notes.")),
    B("The total is always 10 times the number of notes. With m notes, it is 10 times m.", L("l3", "10 × m")),
    B("We leave out the times sign and write the number first. That gives 10 m rupees.",
      answer("a1", "₹10m", label=True), mark("a1", "₹10m")),
    B("m plus 10 would add 10 rupees only once, as if she had a single note. "
      "But every one of the m notes is worth 10."),
    B("Lots of the same thing means multiply. So m notes of 10 rupees are worth 10 m rupees."),
])

# m ten-rupee notes and n five-rupee notes. Total?   (₹(10m + 5n))
LESSONS["Q_CH13_015"] = lesson([
    B("Diya has m ten rupee notes and n five rupee notes. Two kinds of notes. We want the total amount.",
      given("g1", "m notes of ₹10,   n notes of ₹5", label=True), fig("Q_CH13_015")),
    B("Start with the ten rupee notes. There are m of them. What are they worth?",
      ask=choose(["10m", "m + 10", "m"], 0,
                 "Each of the m notes is worth 10 rupees. Lots of the same thing means multiply. "
                 "So they are worth 10 times m.")),
    B("m notes of 10 rupees are worth 10 m.", L("l1", "ten-rupee notes: 10m")),
    B("In the same way, n notes of 5 rupees are worth 5 times n, which is 5 n.", L("l2", "five-rupee notes: 5n")),
    B("Total means add the two values. 10 m plus 5 n.", L("l3", "10m + 5n")),
    B("Can we join 10 m and 5 n into one term, like 15 m n?",
      ask=choose(["No, m and n are different letters", "Yes, it makes 15mn"], 0,
                 "m and n count different things: ten rupee notes and five rupee notes. "
                 "Different letters cannot be joined into one term.")),
    B("So the total is 10 m plus 5 n rupees.", answer("a1", "₹(10m + 5n)", label=True), mark("a1", "₹(10m + 5n)")),
    B("Test it. With 2 ten rupee notes and 3 five rupee notes, she has 20 plus 15, which is 35 rupees.",
      W("l4", "10 × 2 + 5 × 3 = 20 + 15 = 35")),
    B("m plus n would only count the notes. To get the money, multiply each count by what that note is worth."),
])

# Out of m notes of Rs. 10 each, Diya spent 12 notes. Notes left?   (m − 12)
LESSONS["Q_CH13_016"] = lesson([
    B("Diya has m notes of 10 rupees each. She spends 12 of the notes on a cake. How many notes are left?",
      given("g1", "m notes of ₹10,   12 notes spent", label=True), fig("Q_CH13_016")),
    B("Read the question once more. What are we asked to count?",
      ask=choose(["notes", "rupees"], 0,
                 "The question says: how many notes are left. So we count notes, not money.")),
    B("We are counting notes. She starts with m notes.", L("l1", "notes at the start: m")),
    B("She spends 12 notes. What do we do with the 12?",
      ask=choose(["take it away from m", "add it to m", "take m away from it"], 0,
                 "Spending makes her pile of notes smaller. She had m, so we start from m and take 12 away.")),
    B("m take away 12. That is m minus 12.", answer("a1", "m − 12", label=True), mark("a1", "m − 12")),
    B("What about the 10 rupees on each note? It is extra information. "
      "It would matter for money, but we are only counting notes."),
    B("The 12 notes are worth 120 rupees. So m minus 120 would mix notes with rupees, and that makes no sense.",
      W("l2", "12 × 10 = 120")),
    B("Check what the question counts before you start. Here it is notes, so the answer is m minus 12."),
])

# x years ago Soham was 8. His age y years hence?   (8 + x + y)
LESSONS["Q_CH13_017"] = lesson([
    B("x years ago, Soham was 8 years old. We want his age y years hence. Hence means from now.",
      given("g1", "x years ago: 8 years old", label=True), fig("Q_CH13_017")),
    B("We make two moves along the time line. First from the past to now. Then from now to the future.",
      L("l1", "x years ago   →   now   →   y years hence")),
    B("He was 8, x years ago. How old is he now?",
      ask=choose(["8 + x", "8 − x", "8"], 0,
                 "From x years ago to now, he has grown x years older. Growing older means adding. "
                 "So now he is 8 plus x.")),
    B("He has grown x years older. So now he is 8 plus x.", L("l2", "now: 8 + x")),
    B("y years hence means y years from now. What do we do with the y?",
      ask=choose(["add it to 8 + x", "add it to 8 only", "take it away"], 0,
                 "We are standing at now, where he is 8 plus x. "
                 "Moving y years into the future adds y to that age.")),
    B("Add y to his age now. That gives 8 plus x plus y.",
      answer("a1", "8 + x + y", label=True), mark("a1", "8 + x + y")),
    B("Try numbers. If x is 2, he is 10 now. If y is 5, he will be 15. And 8 plus 2 plus 5 is 15.",
      W("l3", "8 + 2 + 5 = 15")),
    B("Going forward in time always adds. Two moves forward, so two things are added to the 8."),
])

# A pen costs thrice as much as a pencil (₹x). Pen and pencil together?   (₹4x)
LESSONS["Q_CH13_018"] = lesson([
    B("A pencil costs x rupees. A pen costs thrice as much. We want the cost of a pen and a pencil together.",
      given("g1", "pencil: ₹x,   pen: thrice as much", label=True), fig("Q_CH13_018")),
    B("Thrice means three times. So what does the pen cost?",
      ask=choose(["3x", "x + 3", "x"], 0,
                 "Thrice as much means 3 times as much. 3 times x is written 3 x. "
                 "Adding 3 would only make it 3 rupees dearer.")),
    B("The pen costs 3 times x, which is 3 x.", W("l1", "3x"), note("l1", "3x", "pen")),
    B("Is 3 x the answer?",
      ask=choose(["No, add the pencil too", "Yes, it is 3x"], 0,
                 "3 x is the pen alone. The question asks for a pen and a pencil together. "
                 "So we add the pencil's x.")),
    B("Together: 3 x for the pen, plus x for the pencil.", W("l2", "3x + x")),
    B("x on its own is 1 x. So 3 x plus 1 x makes 4 x.", answer("a1", "3x + x = 4x"), mark("a1", "4x")),
    B("Check with numbers. If a pencil costs 5 rupees, the pen costs 15. Together that is 20. "
      "And 4 times 5 is 20.",
      W("l3", "5 + 15 = 20"), W("l4", "4 × 5 = 20")),
    B("Thrice means times 3. And together means add. So the two cost 4 x rupees."),
], "x", 4)

# y metres cut from a rope x metres long. What is left?   ((x − y) m)
LESSONS["Q_CH13_019"] = lesson([
    B("A rope is x metres long. A piece of y metres is cut from it. We want the length that is left.",
      given("g1", "rope: x m,   piece cut off: y m", label=True), fig("Q_CH13_019")),
    B("Try with numbers. A rope of 10 metres, with 3 metres cut off, leaves 10 minus 3, which is 7 metres.",
      W("l1", "10 − 3 = 7")),
    B("So cutting a piece off means which operation?",
      ask=choose(["subtract", "add", "multiply"], 0,
                 "After the cut, the rope is shorter. Making something smaller by an amount is taking away.")),
    B("Now use the letters. The whole rope, x, goes where the 10 was. The cut piece, y, goes where the 3 was.",
      strike("l1", "10", "x"), strike("l1", "3", "y")),
    B("Which one comes first in the subtraction?",
      ask=choose(["x − y", "y − x"], 0,
                 "We start with the whole rope and take the piece away from it. "
                 "The whole rope is x, so x comes first.")),
    B("So x minus y metres are left.", answer("a1", "(x − y) m", label=True), mark("a1", "(x − y) m")),
    B("Start with the whole, then take away the part. The order matters: 10 minus 3 is not the same as 3 minus 10."),
])

# From a wire x metres long, y cm was cut. How many cm left?   ((100x − y) cm)
LESSONS["Q_CH13_020"] = lesson([
    B("A wire is x metres long. A piece of y centimetres is cut off. We want what is left, in centimetres.",
      given("g1", "wire: x m,   cut off: y cm", label=True), fig("Q_CH13_020")),
    B("Look at the units. Can we subtract centimetres from metres straight away?",
      ask=choose(["No, make the units the same first", "Yes, x − y"], 0,
                 "Metres and centimetres are different sizes, so we cannot mix them. "
                 "Both lengths must be in the same unit first.")),
    B("The answer is wanted in centimetres. So we change the metres. 1 metre is 100 centimetres.",
      L("l1", "1 m = 100 cm")),
    B("So how many centimetres is x metres?",
      ask=choose(["100x", "x + 100", "1000x"], 0,
                 "Every one of the x metres is 100 centimetres. Lots of the same thing means multiply. "
                 "So it is 100 times x.")),
    B("x metres is 100 times x centimetres, written 100 x.", L("l2", "x m = 100x cm")),
    B("Now both lengths are in centimetres. Take away the y that was cut.",
      answer("a1", "(100x − y) cm", label=True), mark("a1", "(100x − y) cm")),
    B("Try it. A 2 metre wire is 200 centimetres. Cut off 30, and 170 are left.",
      W("l3", "100 × 2 − 30 = 200 − 30 = 170")),
    B("Same units first, then subtract. And remember: 100 centimetres in a metre. "
      "1000 is for metres in a kilometre."),
])

# Simplify: 5a + a   (6a)
LESSONS["Q_CH13_021"] = lesson([
    B("5 a plus a. Both pieces have the same letter, so they are like terms. Like terms can be joined.",
      given("g1", "5a + a")),
    B("The second a has no number in front. How many a's is it?",
      ask=choose(["1", "0", "5"], 0,
                 "A letter on its own is one of that letter. We just do not write the 1. So a means 1 a.")),
    B("a on its own means 1 a. I'll write the hidden 1 in.",
      note("g1", T("a", 2), "1a"), W("l1", "5a + 1a")),
    B("Think of apples. 5 apples and 1 more apple make 6 apples.", W("l2", "5 + 1 = 6")),
    B("So what is 5 a plus 1 a?",
      ask=choose(["6a", "5a²", "6a²"], 0,
                 "We are adding, not multiplying. Apples added to apples give more apples, not squared apples. "
                 "The letter stays the same.")),
    B("5 a plus a is 6 a.", answer("a1", "5a + a = 6a"), mark("a1", "6a")),
    B("To add like terms, add the numbers in front and keep the letter. "
      "And the number is written before the letter: 6 a."),
], "a", 6)

# Add: (3x + 4y) and (x + 2y)   (4x + 6y)
LESSONS["Q_CH13_022"] = lesson([
    B("We add two expressions: 3 x plus 4 y, and x plus 2 y.",
      given("g1", "(3x + 4y) + (x + 2y)", label=True)),
    B("Which terms can be added together?",
      ask=choose(["3x with x, 4y with 2y", "3x with 4y, x with 2y", "all of them into one term"], 0,
                 "Only like terms join, and like terms have the same letter. "
                 "So x terms go with x terms, and y terms with y terms.")),
    B("The x family: 3 x and x. The lone x is 1 x. So 3 x and 1 x make 4 x.",
      group("g1", ["3x", T("x", 2)], "4x"), L("l1", "3x + x = 4x")),
    B("Now the y family: 4 y and 2 y. What do they make?",
      ask=choose(["6y", "8y", "2y"], 0,
                 "4 lots of y and 2 more lots of y. Count them together: 4 plus 2 is 6. So 6 y.")),
    B("4 y and 2 y make 6 y.", group("g1", ["4y", "2y"], "6y"), L("l2", "4y + 2y = 6y")),
    B("x and y are different letters, so the two parts stay side by side. The sum is 4 x plus 6 y.",
      answer("a1", "4x + 6y", label=True), mark("a1", "4x + 6y")),
    B("Test with x as 1 and y as 1. The brackets are 7 and 3, which make 10. And 4 plus 6 is 10.",
      W("l3", "(3 + 4) + (1 + 2) = 7 + 3 = 10"), W("l4", "4 + 6 = 10")),
    B("Never squash it all into one term with x y. Only like terms join. The answer is 4 x plus 6 y."),
])

# Add: (7a + 5b) and (3a − b)   (10a + 4b)
LESSONS["Q_CH13_023"] = lesson([
    B("We add two expressions: 7 a plus 5 b, and 3 a minus b. Watch the minus sign in the second one.",
      given("g1", "(7a + 5b) + (3a − b)", label=True)),
    B("The a family first. 7 a and 3 a make 10 a.",
      group("g1", ["7a", "3a"], "10a"), L("l1", "7a + 3a = 10a")),
    B("Now the b family. Look at the sign in front of the second b. What is it?",
      ask=choose(["minus", "plus"], 0,
                 "In the second bracket it says 3 a minus b. So that b is being taken away.")),
    B("So 5 b is added, and b is taken away. The lone b is 1 b.", under("g1", "5b"), under("g1", "− b")),
    B("5 b take away 1 b. What is left?",
      ask=choose(["4b", "6b", "5b"], 0,
                 "5 of something, take away 1 of them, leaves 4. So 4 b are left.")),
    B("5 b minus 1 b is 4 b. It is 4 b to be added, because more b's were added than taken away.",
      L("l2", "5b − b = 4b")),
    B("So the sum is 10 a plus 4 b.", answer("a1", "10a + 4b", label=True), mark("a1", "10a + 4b")),
    B("Test with a as 1 and b as 1. The brackets are 12 and 2, which make 14. And 10 plus 4 is 14.",
      W("l3", "(7 + 5) + (3 − 1) = 12 + 2 = 14"), W("l4", "10 + 4 = 14")),
    B("Each term keeps the sign in front of it. Collect the a's, collect the b's, and you get 10 a plus 4 b."),
])

# Which pair are unlike terms?   (4m and 3n)
LESSONS["Q_CH13_024"] = lesson([
    B("Like terms have exactly the same letter. Unlike terms have different letters. "
      "We have four pairs, and we must find the unlike pair.",
      given("g1", "Which pair are unlike terms?", label=True)),
    B("What do we look at to decide?",
      ask=choose(["the letters", "the numbers in front", "the signs"], 0,
                 "The numbers in front can be anything, and so can the signs. Only the letter decides. "
                 "Same letter means like terms.")),
    B("First pair: 5 a and 3 a. Both have an a. They are like terms.",
      L("l1", "5a and 3a"), note("l1", "5a and 3a", "like")),
    B("Second pair: y and 12 y. The lone y is 1 y. Both have a y. Like terms again.",
      L("l2", "y and 12y"), note("l2", "y and 12y", "like")),
    B("Third pair: 7 x and minus 2 x. Does the minus sign make them unlike?",
      L("l3", "7x and −2x"),
      ask=choose(["No, both still have x", "Yes, the sign is different"], 0,
                 "A minus sign does not change the letter. Both terms carry an x, so they are still like terms.")),
    B("Both have an x. So they are like terms too.", note("l3", "7x and −2x", "like")),
    B("Last pair: 4 m and 3 n. One has m, and the other has n. Different letters. These are unlike terms.",
      answer("a1", "4m and 3n", label=True), mark("a1", "4m and 3n"), note("a1", "4m and 3n", "unlike", "below")),
    B("Same letter, like. Different letters, unlike. So the unlike pair is 4 m and 3 n."),
])

# Subtract (2x + 3) from (5x + 7).   (3x + 4)
LESSONS["Q_CH13_025"] = lesson([
    B("Subtract 2 x plus 3, from 5 x plus 7. The first job is to get the order right.",
      given("g1", "Subtract (2x + 3) from (5x + 7)", label=True)),
    B("Subtract this, from that. Which one do we start with?",
      ask=choose(["5x + 7", "2x + 3"], 0,
                 "Subtract 2 from 9 means 9 minus 2. The number after the word from is where we start. "
                 "So we start with 5 x plus 7.")),
    B("We start with 5 x plus 7, and take away 2 x plus 3.", W("l1", "(5x + 7) − (2x + 3)")),
    B("Take away the x terms first. 5 x take away 2 x is 3 x.",
      group("l1", ["5x", "2x"], "3x"), W("l2", "5x − 2x = 3x")),
    B("Now the plain numbers, 7 and 3. The whole second bracket is being taken away. So what happens to the 3?",
      ask=choose(["it is taken from 7", "it is added to 7"], 0,
                 "We are taking away the whole of 2 x plus 3. So the 3 goes too. That is 7 take away 3.")),
    B("7 take away 3 is 4.", W("l3", "7 − 3 = 4")),
    B("So the result is 3 x plus 4.", answer("a1", "(5x + 7) − (2x + 3) = 3x + 4"), mark("a1", "3x + 4")),
    B("Test with x as 1. The first bracket is 12 and the second is 5. 12 minus 5 is 7. And 3 plus 4 is 7.",
      W("l4", "(5 + 7) − (2 + 3) = 12 − 5 = 7"), W("l5", "3 + 4 = 7")),
    B("From tells you where to start. Then take away letters from letters, and numbers from numbers."),
], "x", 4)
