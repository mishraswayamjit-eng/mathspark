"""Lessons written one by one: newly written questions G4A_ALGEBRA_017 to 027."""
from g4_gr4_algebra_lib import (B, L, T, W, answer, arc, box, choose, fig, given, lesson, mark, note, strike, under)

LESSONS = {}

# Three years ago Meena was twice as old as Ravi was then. Ravi is x now. Meena now?   (2x − 3)
LESSONS["G4A_ALGEBRA_017"] = lesson([
    B("Two moments in this story: three years ago, and now. Ravi is x years old now. "
      "Three years ago, Meena was twice as old as Ravi was then. How old is Meena now?",
      given("g1", "3 years ago: Meena = twice Ravi", label=True), given("g2", "Ravi now: x years", label=True),
      fig("G4A_ALGEBRA_017")),
    B("The twice as old was true three years ago. So first: how old was Ravi three years ago?",
      ask=choose(["x − 3", "x + 3", "x"], 0,
                 "Three years ago he was younger. So take 3 away from his age now. That is x minus 3.")),
    B("Three years ago Ravi was x minus 3.", W("l1", "x − 3"), note("l1", "x − 3", "Ravi then")),
    B("Meena was twice that. 2 times, x minus 3. The 2 multiplies both parts, so we get 2 x minus 6.",
      W("l2", "2(x − 3) = 2x − 6"), arc("l2", "2", "x", "3"), note("l2", "2x − 6", "Meena then")),
    B("2 x minus 6. Is that Meena's age now?",
      ask=choose(["No, that was 3 years ago", "Yes, that is her age now"], 0,
                 "2 x minus 6 is how old Meena was three years ago. She has had three birthdays since then. "
                 "So we must add 3.")),
    B("That was her age three years ago. To reach today, add 3. Minus 6, then plus 3, makes minus 3.",
      answer("a1", "2x − 6 + 3 = 2x − 3"), mark("a1", "2x − 3")),
    B("Test it. Say Ravi is 10 now. Three years ago he was 7, and Meena was 14. Today she is 17. "
      "And 2 times 10, minus 3, is 17.",
      W("l3", "10 − 3 = 7"), W("l4", "2 × 7 = 14"), W("l5", "14 + 3 = 17"), W("l6", "2 × 10 − 3 = 17")),
    B("Keep track of which moment each age belongs to. Go back, double, then come forward again. "
      "Meena is 2 x minus 3."),
], "x", 3)

# Row of matchstick squares: first needs 4, each new one 3 more. n squares?   (3n + 1)
LESSONS["G4A_ALGEBRA_018"] = lesson([
    B("Rina makes a row of squares with matchsticks. The first square needs 4. "
      "Each new square shares a side, so it needs only 3 more. How many for a row of n squares?",
      given("g1", "first square: 4,   each new square: 3 more", label=True), fig("G4A_ALGEBRA_018")),
    B("Count some small rows. 1 square needs 4. 2 squares need 4 plus 3, which is 7. "
      "3 squares need 7 plus 3, which is 10.",
      L("l1", "1 square: 4,   2 squares: 7,   3 squares: 10")),
    B("In a row of n squares, the first one uses 4. How many of the squares are new ones, using 3 each?",
      ask=choose(["n − 1", "n", "n + 1"], 0,
                 "The first square is already counted with its 4 matchsticks. Take it out of the n squares. "
                 "That leaves n minus 1 new ones.")),
    B("n minus 1 new squares, with 3 matchsticks each. 3 times, n minus 1, is 3 n minus 3.",
      W("l2", "3(n − 1) = 3n − 3"), arc("l2", "3", "n", "1")),
    B("Now add the 4 for the first square. 4 minus 3 leaves 1. So it is 3 n plus 1.",
      answer("a1", "4 + 3n − 3 = 3n + 1"), mark("a1", "3n + 1")),
    B("Let's check with 3 squares. We counted 10. What does 3 n plus 1 give when n is 3?",
      ask=choose(["10", "13", "9"], 0,
                 "3 n means 3 times 3, which is 9. Then add 1.")),
    B("3 times 3 is 9, and 1 more is 10. It matches our count.", W("l3", "3 × 3 + 1 = 10")),
    B("The trap is 3 n plus 4. That gives 3 to every square and then 4 more. "
      "But the first square is counted only once. So the answer is 3 n plus 1."),
], "n", 3)

# Anu 5k + 3, Bala 3k + 11, k from 1 to 10. For how many k does Anu have more?   (6)
LESSONS["G4A_ALGEBRA_019"] = lesson([
    B("Anu has 5 k plus 3 rupees. Bala has 3 k plus 11. k can be any whole number from 1 to 10. "
      "For how many of those does Anu have more?",
      given("g1", "Anu: 5k + 3,   Bala: 3k + 11", label=True)),
    B("Start with k as 1. Anu has 5 plus 3, which is 8. Bala has 3 plus 11, which is 14. Bala is ahead by 6.",
      W("l1", "5 × 1 + 3 = 8"), W("l2", "3 × 1 + 11 = 14"), W("l3", "14 − 8 = 6")),
    B("Each time k goes up by 1, Anu gains 5 rupees and Bala gains 3. What happens to the gap?",
      ask=choose(["it shrinks by 2", "it grows by 2", "it stays the same"], 0,
                 "Anu gains 5 while Bala gains only 3. So Anu catches up by 2 rupees every time k goes up by 1.")),
    B("Anu catches up by 2 each time. The gap goes 6, then 4, then 2, then 0. So when k is 4 they are level.",
      L("l4", "gap:  6, 4, 2, 0    (k = 1, 2, 3, 4)")),
    B("Check k as 4. Anu has 5 times 4, plus 3, which is 23. Bala has 3 times 4, plus 11, also 23. Equal.",
      W("l5", "5 × 4 + 3 = 23"), W("l6", "3 × 4 + 11 = 23")),
    B("When k is 4 they have the same. Does 4 count as Anu having more?",
      ask=choose(["No, equal is not more", "Yes, count it"], 0,
                 "More means really bigger. When both have 23 rupees, nobody has more. So 4 does not count.")),
    B("After 4, Anu pulls ahead and stays ahead. So she has more when k is 5, 6, 7, 8, 9 or 10.",
      L("l7", "k = 5, 6, 7, 8, 9, 10")),
    B("Count them. That is 6 values.", answer("a1", "6 values of k", label=True), mark("a1", "6")),
    B("Find where the two are equal. Then count only the values on the winning side. "
      "And equal never counts as more."),
])

# Card (2a + 5) by (a + 1), a square of side a cut from one corner. Perimeter left?   ((6a + 12) cm)
LESSONS["G4A_ALGEBRA_020"] = lesson([
    B("A card is 2 a plus 5 centimetres long and a plus 1 wide. A small square, with each side a centimetres, "
      "is cut from one corner. We want the perimeter of what is left.",
      given("g1", "card: (2a + 5) cm by (a + 1) cm", label=True), fig("G4A_ALGEBRA_020")),
    B("Start with the whole card, before the cut. Length plus breadth: 2 a plus 5, plus a plus 1, is 3 a plus 6.",
      W("l1", "2a + 5 + a + 1 = 3a + 6")),
    B("The perimeter is double that. 2 times 3 a is 6 a, and 2 times 6 is 12.",
      W("l2", "2(3a + 6) = 6a + 12"), arc("l2", "2", "3a", "6")),
    B("Now the cut. Trace the edge with your finger. At the corner, two pieces of the old edge have gone. "
      "Each one was a centimetres long.",
      L("l3", "edge lost:  a + a")),
    B("But the cut also makes new edges, on the inside of the corner. How long are the new edges altogether?",
      ask=choose(["a + a, the same as was lost", "nothing, there are no new edges", "4a, the whole small square"], 0,
                 "The hole is a square with side a. Two of its sides are now part of the card's edge. "
                 "So the new edges are a and a.")),
    B("Two edges of a were lost, and two new edges of a appeared. They balance exactly. "
      "The distance round does not change.",
      L("l4", "edge gained:  a + a")),
    B("So the perimeter is still 6 a plus 12 centimetres.", answer("a1", "6a + 12"), mark("a1", "6a + 12")),
    B("A square notch at a corner swaps two outside edges for two inside edges of the same length. "
      "So always trace the edge before you take anything away."),
], "a", 6)

# nth term 4n − 1: 3, 7, 11, 15, ... Which is a term?   (47)
LESSONS["G4A_ALGEBRA_021"] = lesson([
    B("The rule is 4 n minus 1. So the pattern starts 3, 7, 11, 15. We have four numbers to test, "
      "and only one of them belongs to the pattern.",
      given("g1", "nth term = 4n − 1:   3, 7, 11, 15, ...", label=True)),
    B("See how each term is made. Take a multiple of 4, like 4, 8, 12 or 16. Then take away 1.",
      L("l1", "4, 8, 12, 16   →   3, 7, 11, 15")),
    B("So if a number is in the pattern, what must we get when we add 1 to it?",
      ask=choose(["a multiple of 4", "an odd number", "a multiple of 3"], 0,
                 "Every term is 1 less than a multiple of 4. "
                 "So adding the 1 back must land us exactly on a multiple of 4.")),
    B("Test each number by adding 1. 44 becomes 45. 45 becomes 46. 46 becomes 47. And 47 becomes 48.",
      W("l2", "44 + 1 = 45"), W("l3", "45 + 1 = 46"), W("l4", "46 + 1 = 47"), W("l5", "47 + 1 = 48")),
    B("Which of 45, 46, 47 and 48 is a multiple of 4?",
      ask=choose(["48", "45", "46", "47"], 0,
                 "Count in fours from 44. The next one is 48. So of our four numbers, only 48 is a multiple of 4.")),
    B("48 divided by 4 is 12, a whole number. So 47 is in the pattern. It is the 12th term.",
      W("l6", "48 ÷ 4 = 12"), answer("a1", "4 × 12 − 1 = 47"), mark("a1", "47")),
    B("Watch out for 45. Taking 1 away from it gives 44, which is tempting. "
      "But the rule already takes 1 away, so to undo it we add 1."),
    B("To test a number against a rule, undo the rule backwards. Here: add 1, then see if 4 divides it exactly. "
      "Only 47 passes."),
])

# Sana ₹s, Tara ₹20 more. Tara gives ₹15 to Sana. Who has more now?   (Sana has ₹10 more)
LESSONS["G4A_ALGEBRA_022"] = lesson([
    B("Sana has s rupees. Tara has 20 rupees more than Sana. Then Tara gives 15 rupees to Sana. "
      "Who has more now, and by how much?",
      given("g1", "Sana: ₹s,   Tara: ₹20 more", label=True), fig("G4A_ALGEBRA_022")),
    B("Tara has 20 more than Sana. So Tara starts with s plus 20.",
      W("l1", "s + 20"), note("l1", "s + 20", "Tara at the start")),
    B("Tara gives 15 rupees to Sana. Whose money changes?",
      ask=choose(["both girls' money", "only Tara's", "only Sana's"], 0,
                 "The 15 rupees leave Tara's hand and land in Sana's. So Tara goes down by 15, and Sana goes up by 15.")),
    B("Tara loses 15. s plus 20, minus 15, is s plus 5.",
      W("l2", "s + 20 − 15 = s + 5"), note("l2", "s + 5", "Tara now")),
    B("Sana gains 15. So Sana now has s plus 15.", W("l3", "s + 15"), note("l3", "s + 15", "Sana now")),
    B("Now compare s plus 15 with s plus 5. Who has more?",
      ask=choose(["Sana", "Tara", "they are equal"], 0,
                 "Both have the same s. On top of that, Sana has 15 and Tara has only 5. So Sana has more.")),
    B("Both have s. Sana has 15 extra and Tara has 5 extra. 15 minus 5 is 10. So Sana has 10 rupees more.",
      W("l4", "15 − 5 = 10"), answer("a1", "Sana has ₹10 more", label=True), mark("a1", "₹10")),
    B("The trap is to take 15 off Tara's lead of 20 and stop there. But the same 15 also lands with Sana. "
      "Write both new amounts, then compare. Sana is 10 ahead."),
], "s", 10)

# Five numbers in a row, middle m. Smallest plus greatest?   (2m)
LESSONS["G4A_ALGEBRA_023"] = lesson([
    B("Five whole numbers come one after another. The middle one is m. "
      "We want the smallest and the greatest added together.",
      given("g1", "five numbers in a row, middle one m", label=True), fig("G4A_ALGEBRA_023")),
    B("Look at the example: 6, 7, 8, 9, 10. The middle is 8. The smallest, 6, is 2 less than 8. "
      "The greatest, 10, is 2 more.",
      L("l1", "6, 7, 8, 9, 10"), under("l1", "8")),
    B("So if the middle number is m, what is the smallest?",
      ask=choose(["m − 2", "m − 1", "m"], 0,
                 "Step back from the middle, one at a time. One step back is m minus 1. "
                 "Two steps back is m minus 2. That is the smallest.")),
    B("Step out from the middle, both ways. The five numbers are m minus 2, m minus 1, m, m plus 1 and m plus 2.",
      L("l2", "m − 2,  m − 1,  m,  m + 1,  m + 2"), box("l2", "m − 2"), box("l2", "m + 2")),
    B("Add the smallest and the greatest. m minus 2, plus m plus 2.", W("l3", "m − 2 + m + 2")),
    B("What happens to the minus 2 and the plus 2?",
      ask=choose(["they cancel out", "they make 4", "they make 2"], 0,
                 "Taking 2 away and then adding 2 brings you back to where you started. Together they make nothing.")),
    B("Minus 2 and plus 2 cancel. All that is left is m and m, which is 2 m.",
      strike("l3", "− 2"), strike("l3", "+ 2"), answer("a1", "m − 2 + m + 2 = 2m"), mark("a1", "2m")),
    B("Check with the example. 6 plus 10 is 16. And 2 times 8 is 16.",
      W("l4", "6 + 10 = 16"), W("l5", "2 × 8 = 16")),
    B("When m is in the middle, the two ends are the same distance away, one on each side. "
      "So together they make 2 m."),
], "m", 2)

# Perimeter (10a + 6), length (3a + 2). Breadth?   ((2a + 1) cm)
LESSONS["G4A_ALGEBRA_024"] = lesson([
    B("A rectangle has a perimeter of 10 a plus 6 centimetres. Its length is 3 a plus 2 centimetres. "
      "We want its breadth.",
      given("g1", "perimeter (10a + 6) cm,  length (3a + 2) cm", label=True), fig("G4A_ALGEBRA_024")),
    B("The perimeter is 2 lengths and 2 breadths. So what is half the perimeter?",
      ask=choose(["1 length + 1 breadth", "2 lengths", "1 breadth"], 0,
                 "Cut the trip round the rectangle in half. Half of 2 lengths and 2 breadths is "
                 "1 length and 1 breadth.")),
    B("So halve the perimeter. Half of 10 a is 5 a. Half of 6 is 3. One length plus one breadth is 5 a plus 3.",
      W("l1", "(10a + 6) ÷ 2 = 5a + 3")),
    B("Now take the length away. What is left is the breadth.", W("l2", "5a + 3 − (3a + 2)")),
    B("We take away the whole length, 3 a plus 2. What happens to the 2?",
      ask=choose(["it is taken away too", "it is added"], 0,
                 "The bracket says the whole length goes. That is the 3 a, and the 2 as well. Both are taken away.")),
    B("Letters first: 5 a minus 3 a is 2 a. Then numbers: 3 minus 2 is 1.",
      W("l3", "5a − 3a = 2a"), W("l4", "3 − 2 = 1")),
    B("So the breadth is 2 a plus 1 centimetres.",
      answer("a1", "5a + 3 − (3a + 2) = 2a + 1"), mark("a1", "2a + 1")),
    B("Check by going forwards. Length plus breadth is 5 a plus 3. Double it, and we are back at 10 a plus 6.",
      W("l5", "2(5a + 3) = 10a + 6")),
    B("To work back from a perimeter: halve it first, then take away the side you know."),
], "a", 2)

# Two-digit number, tens t, ones u, plus the number with digits swapped   (11t + 11u)
LESSONS["G4A_ALGEBRA_025"] = lesson([
    B("A two digit number has tens digit t and ones digit u. Swap the digits to make a second number. "
      "We want the sum of the two numbers.",
      given("g1", "tens digit t,   ones digit u", label=True), fig("G4A_ALGEBRA_025")),
    B("Try real digits first. Tens digit 4 and ones digit 3 make 43. That is 4 tens and 3 ones.",
      W("l1", "4 × 10 + 3 = 43")),
    B("So with letters, what is the number with tens digit t and ones digit u worth?",
      ask=choose(["10t + u", "t + u", "tu"], 0,
                 "A digit in the tens place is worth ten times itself. So t in the tens place is worth 10 t. "
                 "Then add the ones digit, u.")),
    B("The first number is worth 10 t plus u.", L("l2", "first number = 10t + u")),
    B("Now swap the digits. u moves to the tens place, and t to the ones place. "
      "So the second number is worth 10 u plus t.",
      L("l3", "swapped number = 10u + t")),
    B("Add them. For t: 10 t and 1 more t make 11 t. For u: 1 u and 10 u make 11 u.",
      L("l4", "10t + t = 11t"), L("l5", "u + 10u = 11u")),
    B("So the sum is 11 t plus 11 u.", answer("a1", "11t + 11u", label=True), mark("a1", "11t + 11u")),
    B("Check with 43 and 34. 43 plus 34 is 77. And 11 times 4, plus 11 times 3, is 44 plus 33, also 77.",
      W("l6", "43 + 34 = 77"), W("l7", "11 × 4 + 11 × 3 = 44 + 33 = 77")),
    B("Each digit sits in the tens place once and in the ones place once. "
      "That is why each one is counted 11 times."),
])

# The value of 3x + 2 is 20. What is 3(x + 2)?   (24)
LESSONS["G4A_ALGEBRA_026"] = lesson([
    B("We are told that 3 x plus 2 is 20. We want the value of 3 times, x plus 2, with a bracket.",
      given("g1", "3x + 2 = 20", label=True), given("g2", "3(x + 2) = ?", label=True), fig("G4A_ALGEBRA_026")),
    B("These two look almost the same. Are they the same thing?",
      ask=choose(["No, the bracket changes it", "Yes, they are the same"], 0,
                 "With the bracket, the 3 multiplies the x and the 2 as well. "
                 "Without the bracket, only the x is multiplied.")),
    B("Open the bracket. 3 times x is 3 x. 3 times 2 is 6. So it is 3 x plus 6.",
      arc("g2", "3", "x", "2"), L("l1", "3(x + 2) = 3x + 6")),
    B("Now compare. We know 3 x plus 2. We want 3 x plus 6. The 3 x part is the same in both.",
      L("l2", "3x + 2    and    3x + 6"), under("l2", T("3x", 1)), under("l2", T("3x", 2))),
    B("How much more is 3 x plus 6 than 3 x plus 2?",
      ask=choose(["4 more", "6 more", "2 more"], 0,
                 "The 3 x is the same in both. So just compare the plain numbers. From 2 up to 6 is 4.")),
    B("It is 4 more. 3 x plus 2 is 20, so 3 x plus 6 is 20 plus 4, which is 24.",
      W("l3", "6 − 2 = 4"), answer("a1", "20 + 4 = 24"), mark("a1", "24")),
    B("We can check by finding x. x must be 6, because 3 times 6, plus 2, is 20. "
      "And 3 times, 6 plus 2, is 3 times 8, which is 24.",
      W("l4", "3 × 6 + 2 = 20"), W("l5", "3 × (6 + 2) = 24")),
    B("The trap is to add the whole 6 on to the 20. But the 20 already has a 2 inside it. "
      "So we add only 4, and get 24."),
])

# Pole cut into n pieces, each cut 3 minutes   (3n − 3)
LESSONS["G4A_ALGEBRA_027"] = lesson([
    B("A carpenter cuts a long pole into n pieces. Each cut takes 3 minutes. How long does all the cutting take?",
      given("g1", "n pieces,   each cut takes 3 minutes", label=True), fig("G4A_ALGEBRA_027")),
    B("Careful. The time goes with the cuts, not with the pieces. So first we count the cuts."),
    B("Picture a stick. 1 cut makes 2 pieces. 2 cuts make 3 pieces.",
      L("l1", "1 cut: 2 pieces,    2 cuts: 3 pieces")),
    B("So how many cuts make n pieces?",
      ask=choose(["n − 1", "n", "n + 1"], 0,
                 "The cuts are always 1 fewer than the pieces. 2 pieces need 1 cut. 3 pieces need 2 cuts. "
                 "So n pieces need n minus 1 cuts.")),
    B("n minus 1 cuts, at 3 minutes each. That is 3 times, n minus 1.", W("l2", "3(n − 1)")),
    B("Open the bracket. What is 3 times, n minus 1?",
      ask=choose(["3n − 3", "3n − 1", "n − 3"], 0,
                 "The 3 multiplies both parts in the bracket. 3 times n is 3 n. "
                 "And 3 times 1 is 3, so 3 is taken away, not 1.")),
    B("3 times n is 3 n. 3 times 1 is 3. So the cutting takes 3 n minus 3 minutes.",
      arc("l2", "3", "n", "1"), answer("a1", "3(n − 1) = 3n − 3"), mark("a1", "3n − 3")),
    B("Check with 2 pieces. That is 1 cut, so 3 minutes. And 3 times 2, minus 3, is 3. It fits.",
      W("l3", "3 × 2 − 3 = 3")),
    B("Count the cuts, not the pieces. There is always one cut fewer. That gives 3 n minus 3."),
], "n", 3)
