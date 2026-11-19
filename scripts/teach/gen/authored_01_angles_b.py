"""Angles and lines, G5A_ANGLES_008 to 014: one lesson each, written by hand."""
from authored_01_lib import (ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LANS, LB, LESSON, NOTE, UL, W)  # noqa: F401

LESSONS = {}
P = "G5A_ANGLES_"

# Complement + supplement = 194: the angle is 38 degrees
LESSONS[P + "008"] = LESSON(
    B("The complement and the supplement of an angle add up to 194 degrees. What is the angle?",
      GIVEN("q", "Complement + supplement of an angle = 194°. The angle?")),
    B("The complement is 90 minus the angle. The supplement is 180 minus the angle.",
      LB("l1", "complement = 90° − angle"), LB("l2", "supplement = 180° − angle")),
    B("Add the two. 90 and 180 make 270. And the angle has been taken away twice, once in each.",
      W("l3", "90 + 180 = 270"), LB("l4", "270° − 2 angles = 194°")),
    B("So what are the 2 copies of the angle worth?",
      ask=CHOOSE(["270 − 194", "270 + 194", "194 − 90"], 0,
                 "270 with the 2 angles taken away leaves 194. So the 2 angles are the gap between 270 and 194.")),
    B("270 minus 194 is 76. So 2 copies of the angle make 76 degrees.",
      W("l5", "270 − 194 = 76")),
    B("Here is the trap: 76 is two copies, because the angle was taken away twice. So halve it. 76 divided by 2 is 38.",
      *ANSC("l6", "76 ÷ 2 = 38", 38)),
    B("Check. The complement of 38 is 52. The supplement is 142. And 52 plus 142 is 194.",
      W("c1", "90 − 38 = 52"), W("c2", "180 − 38 = 142"), W("c3", "52 + 142 = 194")),
    B("So write the complement and the supplement from their totals, 90 and 180, and count how many times the angle is taken away."),
)

# P, Q complementary; Q, R supplementary: R is 90 degrees bigger than P
LESSONS[P + "009"] = LESSON(
    B("Angle P and angle Q are complementary. Angle Q and angle R are supplementary. How much bigger is angle R than angle P?",
      GIVEN("q", "P and Q complementary. Q and R supplementary. R − P?")),
    B("Complementary means they add up to 90. So P and Q make 90, and P is 90 minus Q.",
      LB("l1", "P + Q = 90°, so P = 90° − Q")),
    B("Supplementary means they add up to 180. So Q and R make 180, and R is 180 minus Q.",
      LB("l2", "Q + R = 180°, so R = 180° − Q")),
    B("We don't know Q. Do we need it, to compare R with P?",
      ask=CHOOSE(["Yes, it depends on Q", "No, the same Q comes off both"], 1,
                 "Look at the two lines on the board. P is 90 take away Q, and R is 180 take away Q. The very same Q is taken away both times.")),
    B("The same Q is taken from both. So the gap between R and P is just the gap between 180 and 90.",
      W("l3", "180 − 90 = 90")),
    B("Angle R is always 90 degrees bigger than angle P.",
      LANS("a", "R is 90° bigger than P"), CIRC("a", "90°")),
    B("Try it. If Q is 30, then P is 60 and R is 150. The gap is 90.",
      W("c1", "90 − 30 = 60"), W("c2", "180 − 30 = 150"), W("c3", "150 − 60 = 90")),
    B("Change Q to 50. Now P is 40 and R is 130. The gap is 90 again, so it does not depend on Q at all.",
      W("c4", "90 − 50 = 40"), W("c5", "180 − 50 = 130"), W("c6", "130 − 40 = 90")),
    B("So when the same unknown is taken from two totals, it doesn't matter what it is. The difference is the difference of the totals, 90 degrees."),
)

# Complementary: a multiple of 7 and a multiple of 11 -> 35 and 55, difference 20
LESSONS[P + "010"] = LESSON(
    B("Two angles are complementary. In whole degrees, one of them is a multiple of 7 and the other is a multiple of 11. What is the difference between the two angles?",
      GIVEN("q", "Complementary: a multiple of 7 and a multiple of 11")),
    B("Complementary angles add up to 90 degrees. So we need a multiple of 7 and a multiple of 11 that make 90 together.",
      LB("l1", "multiple of 7 + multiple of 11 = 90")),
    B("There are fewer multiples of 11, so list those: 11, 22, 33, 44, 55, 66, 77, 88.",
      LB("l2", "11, 22, 33, 44, 55, 66, 77, 88")),
    B("Take each one from 90 to see what its partner would have to be: 79, 68, 57, 46, 35, 24, 13 and 2.",
      LB("l3", "79, 68, 57, 46, 35, 24, 13, 2")),
    B("Which of those partners is a multiple of 7?",
      ask=CHOOSE(["57", "35", "24"], 1,
                 "Run through the 7 times table in your head. 5 sevens are 35, and none of the other numbers in the list turn up.")),
    B("Only 35 is a multiple of 7: it is 5 sevens. Its partner is 55, which is 5 elevens. So the angles are 35 and 55.",
      CIRC("l3", "35"), W("l4", "5 × 7 = 35"), W("l5", "5 × 11 = 55"), W("l6", "35 + 55 = 90")),
    B("The question asks for the difference. 55 minus 35 is 20 degrees.",
      *ANSC("l7", "55 − 35 = 20", 20)),
    B("The slip to avoid is guessing a pair that looks neat. A careful list shows there is only one pair that passes both tests."),
    B("So when two conditions must both hold, list everything that fits the first one, then test each against the second."),
)

# Lamp post between two parallel roads: 35 + 40 = 75 degrees
LESSONS[P + "011"] = LESSON(
    B("Two parallel roads run east to west, with a lamp post E between them. The line from B on the north road makes 35 degrees with that road. The line from D on the south road makes 40 degrees. We want angle B E D.",
      GIVEN("q", "Parallel roads. BE at 35° to north road, DE at 40° to south")),
    B("The angle at E does not touch either road, so the 35 and the 40 seem far away from it. Here is the trick: draw a new line through E, parallel to both roads.",
      LB("l1", "Draw a line through E, parallel to the roads")),
    B("That new line cuts angle B E D into two parts: an upper part, towards B, and a lower part, towards D.",
      LB("l2", "BED = upper part + lower part")),
    B("Look at the upper part and the 35 degree angle at B. They sit in a Z shape between two parallel lines. What do we know about them?",
      ask=CHOOSE(["they are equal", "they add up to 180", "they add up to 90"], 0,
                 "The line B E crosses two parallel lines, the north road and our new line. The angles in the Z shape are alternate angles, and alternate angles are equal.")),
    B("They are alternate angles, so they are equal. The upper part is 35 degrees.",
      LB("l3", "upper part = 35° (alternate angles)")),
    B("In the same way, the line D E makes a Z with the south road and our new line. So the lower part is 40 degrees.",
      LB("l4", "lower part = 40° (alternate angles)")),
    B("Add the two parts. 35 plus 40 is 75. Angle B E D is 75 degrees.",
      *ANSC("l5", "35 + 40 = 75", 75)),
    B("The tempting moves are to subtract the two angles, or to take them from 180. But the lamp post is between the roads, so the two parts sit side by side, and we add."),
    B("So when an angle is stuck between two parallel lines, draw a third parallel line through its corner. Then each part matches an angle you know."),
)

# Alternate angles add to 124: each obtuse angle is 118 degrees
LESSONS[P + "012"] = LESSON(
    B("A straight line crosses two parallel lines. An angle at the first crossing and its alternate angle at the second add up to 124 degrees. How big is each obtuse angle at the crossings?",
      GIVEN("q", "Two alternate angles add up to 124°. Each obtuse angle?")),
    B("What do we know about a pair of alternate angles between parallel lines?",
      ask=CHOOSE(["they are equal", "they add up to 180", "one is double the other"], 0,
                 "Alternate angles sit in a Z shape between the parallel lines. And between parallel lines, alternate angles are always equal.")),
    B("Alternate angles are equal. Two equal angles add up to 124, so each one is 124 divided by 2, which is 62 degrees.",
      W("l1", "124 ÷ 2 = 62")),
    B("Now read the question again. It asks for the obtuse angles, the ones bigger than a right angle. 62 is acute, so we are not done yet.",
      UL("q", "obtuse")),
    B("At each crossing, an obtuse angle sits beside a 62 degree angle on a straight line. Together they make 180.",
      LB("l2", "62° + obtuse angle = 180°")),
    B("180 minus 62 is 118. Each obtuse angle is 118 degrees.",
      *ANSC("l3", "180 − 62 = 118", 118)),
    B("Two traps to dodge. 62 is an angle at the crossings, but it is the acute one. And 124 is two angles added together, not one angle."),
    B("Check: 118 is bigger than a right angle, so it is obtuse. And 62 plus 118 is 180, a straight line.",
      W("c1", "62 + 118 = 180")),
    B("So at parallel lines there are only two sizes of angle, an acute one and an obtuse one, and together they make 180."),
)

# Triangle PQR between parallel lines: angles 68, 50, 62 -> largest 68
LESSONS[P + "013"] = LESSON(
    B("P is on the top one of two parallel lines. Q and R are on the bottom one. P Q makes 50 degrees with the top line on the left of P, and P R makes 62 degrees with it on the right. What is the largest angle of triangle P Q R?",
      GIVEN("q", "P on top line; Q, R on bottom line. PQ at 50°, PR at 62°")),
    B("At P, three angles lie along the straight top line: the 50 on the left, the triangle's angle Q P R in the middle, and the 62 on the right. Together they make 180.",
      LB("l1", "50° + angle QPR + 62° = 180°")),
    B("So how do we find angle Q P R?",
      ask=CHOOSE(["180 − 50 − 62", "50 + 62", "180 − 62"], 0,
                 "The three angles share the straight line, 180 degrees. Take away the 50 and the 62, and what is left is the angle in the middle.")),
    B("50 and 62 make 112. And 180 minus 112 is 68. So angle Q P R is 68 degrees.",
      W("l2", "50 + 62 = 112"), W("l3", "180 − 112 = 68")),
    B("Now the angle at Q. The line P Q crosses the two parallel lines and makes a Z shape. So the angle at Q equals the 50. They are alternate angles.",
      LB("l4", "angle PQR = 50° (alternate angles)")),
    B("In the same way, the angle at R equals the 62.",
      LB("l5", "angle PRQ = 62° (alternate angles)")),
    B("The triangle's angles are 68, 50 and 62. The largest is 68 degrees.",
      LANS("a", "Largest angle = 68°"), CIRC("a", "68°")),
    B("The trap is 112. That is the 50 and the 62 added together, and it is not an angle of the triangle at all. Find all three angles before you choose the largest."),
    B("Check: 68 plus 50 plus 62 is 180, just right for a triangle.",
      W("c1", "68 + 50 + 62 = 180")),
    B("So between parallel lines, use the straight line at the top and the alternate angles at the bottom. The largest angle here is 68 degrees."),
)

# 135 clockwise then 270 anticlockwise, ends facing North: started South-East
LESSONS[P + "014"] = LESSON(
    B("Ravi turns 135 degrees clockwise, and then 270 degrees anticlockwise. He is now facing North. Which way was he facing at the start?",
      GIVEN("q", "135° clockwise, then 270° anticlockwise. Now faces North")),
    B("There are two turns, in opposite directions. Let's squash them into one single turn first."),
    B("135 clockwise, then 270 anticlockwise. What single turn is that the same as?",
      ask=CHOOSE(["135 anticlockwise", "405 anticlockwise", "135 clockwise"], 0,
                 "The two turns go opposite ways, so the clockwise one undoes part of the anticlockwise one. Take the smaller from the bigger. The bigger one was anticlockwise.")),
    B("270 minus 135 is 135. The anticlockwise turn was the bigger one, so overall Ravi turned 135 degrees anticlockwise.",
      W("l1", "270 − 135 = 135"), NOTE("l1", "135", "anticlockwise", "below", 2)),
    B("He ended facing North. To find where he started, we undo his turn. Which way do we turn from North?",
      ask=CHOOSE(["135 clockwise", "135 anticlockwise"], 0,
                 "To undo a turn, go back the opposite way. He turned anticlockwise, so we wind him back clockwise.")),
    B("That is the trap. Turning anticlockwise from North would carry his turn on, not take it back. To undo it, we go clockwise.",
      LB("l2", "Undo: from North, turn 135° clockwise")),
    B("From North, 90 degrees clockwise is East. We need 135, which is 45 more. Halfway from East to South is South-East.",
      W("l3", "90 + 45 = 135"), LB("l4", "North → East → South-East")),
    B("So Ravi started facing South-East.",
      LANS("a", "Start: South-East"), CIRC("a", "South-East")),
    B("Check. From South-East, 135 clockwise takes him to West. Then 270 anticlockwise from West goes past South and East, to North. That matches.",
      LB("c1", "South-East → West → South → East → North")),
    B("So to find a starting direction: squash the turns into one, then undo that one turn from the finish."),
)
