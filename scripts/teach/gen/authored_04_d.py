"""Triangles 001 to 005 (side lengths), written one by one."""
from authored_04_lib import ANSC, ANSL, B, BOX, CHOOSE, CIRC, GIVEN, LB, LESSON, NOTE, STRIKE, UL, W  # noqa: F401

LESSONS = {}

RULE = "Two shorter sides together > longest side"
FLAT = ("If the two short sticks together are exactly as long as the long one, they must lie flat along it to reach. "
        "There is no room to rise up into a triangle.")

# Five sets of lengths: how many make a triangle?
LESSONS["G5A_TRIANGLES_001"] = LESSON(
    B("We have five sets of three lengths. We want to know how many of them can be the three sides of a triangle.",
      GIVEN("q", "How many of these 5 sets can make a triangle?"),
      LB("s", "3,4,7 | 5,5,9 | 2,6,9 | 4,7,10 | 6,6,12")),
    B("Picture the longest stick lying flat, with the two shorter sticks hinged at its ends. Their tips can only meet if, together, they are longer than it.",
      LB("r", RULE)),
    B("Set 2: 5 plus 5 is 10, which is more than 9. That makes a triangle. Set 4: 4 plus 7 is 11, more than 10. That makes one too.",
      W("l1", "5 + 5 = 10 > 9"), W("l2", "4 + 7 = 11 > 10")),
    B("Set 3: 2 plus 6 is 8, which is less than 9. The two short sticks cannot reach each other. No triangle.",
      W("l3", "2 + 6 = 8 < 9"), STRIKE("s", "2,6,9", "too short")),
    B("Now Set 1. 3 plus 4 is exactly 7. Can those three make a triangle?",
      W("l4", "3 + 4 = 7"),
      ask=CHOOSE(["yes, equal is enough", "no, the sticks lie flat"], 1, FLAT)),
    B("Equal is not enough. That is the trap here: the sticks just lie flat. Set 5 is the same, because 6 plus 6 is exactly 12.",
      W("l5", "6 + 6 = 12"), STRIKE("s", "3,4,7", "flat"), STRIKE("s", "6,6,12", "flat")),
    B("So only Set 2 and Set 4 work. That makes 2 sets.",
      CIRC("s", "5,5,9"), CIRC("s", "4,7,10"), *ANSL("a", "Only Set 2 and Set 4 → 2 sets", "2 sets")),
    B("So to test three lengths, add the two shorter ones and compare with the longest. More means a triangle. Equal or less means none."),
)

# Sticks 2, 3, 4, 5, 7: how many triangles?
LESSONS["G5A_TRIANGLES_002"] = LESSON(
    B("Mira has sticks of 2, 3, 4, 5 and 7 centimetres. She picks three at a time and tries to make a triangle. How many different triangles can she make?",
      GIVEN("q", "Sticks 2, 3, 4, 5, 7 cm. Pick 3: how many triangles?")),
    B("Three sticks close up only when the two shorter ones together are longer than the longest. So we list every choice in order, and test each one.",
      LB("r", RULE)),
    B("Start with the 2 and the 3 together. With the 4 as the third stick: 2 plus 3 is 5, more than 4. That works.",
      W("l1", "2 + 3 = 5 > 4")),
    B("Now 2, 3 and 5. 2 plus 3 is exactly 5. Does that make a triangle?",
      ask=CHOOSE(["yes, equal is enough", "no, the sticks lie flat"], 1, FLAT)),
    B("No. Equal is not enough, the sticks lie flat. And 2, 3, 7 is worse still, because 5 is less than 7.",
      LB("l2", "2, 3, 5: only equal.   2, 3, 7: too short")),
    B("Next, the 2 with the 4. 2 plus 4 is 6, more than 5, so 2, 4, 5 works. But 6 is less than 7, so 2, 4, 7 does not. And 2, 5, 7 is only equal.",
      W("l3", "2 + 4 = 6 > 5"), W("l4", "2 + 4 = 6 < 7"), W("l5", "2 + 5 = 7")),
    B("Now the choices without the 2. 3 plus 4 is 7, more than 5, so 3, 4, 5 works. But 3, 4, 7 is only equal.",
      W("l6", "3 + 4 = 7 > 5"), LB("l7", "3, 4, 7: only equal")),
    B("3 plus 5 is 8, more than 7, so 3, 5, 7 works. And 4 plus 5 is 9, more than 7, so 4, 5, 7 works.",
      W("l8", "3 + 5 = 8 > 7"), W("l9", "4 + 5 = 9 > 7")),
    B("Count the ones that work. There are 5 of them, so Mira can make 5 triangles.",
      LB("l10", "(2,3,4) (2,4,5) (3,4,5) (3,5,7) (4,5,7)"), *ANSL("a", "5 triangles", "5")),
    B("We tested 10 choices in all. The trap is to count every one of them, or to let in the flat ones where the short sticks only equal the long one."),
    B("So list the choices in order so none is missed, and test each: the two shorter sticks together must beat the longest."),
)

# Sides 4 and 9: how many whole-number third sides?
LESSONS["G5A_TRIANGLES_003"] = LESSON(
    B("Two sides of a triangle are 4 centimetres and 9 centimetres. The third side is a whole number. How many different lengths can it have?",
      GIVEN("q", "Sides 4 cm and 9 cm. Third side: how many whole lengths?")),
    B("The third side cannot be too long, and it cannot be too short. Let's find both limits."),
    B("Too long first. If the third side is the longest, the 4 and the 9 together must be longer than it. 4 plus 9 is 13, so the third side is less than 13.",
      W("l1", "4 + 9 = 13"), LB("l2", "third side < 13")),
    B("Now too short. If 9 is the longest side, the 4 and the third side together must beat 9. 9 minus 4 is 5, so the third side is more than 5.",
      W("l3", "9 − 4 = 5"), LB("l4", "third side > 5")),
    B("Can the third side be exactly 5, or exactly 13?",
      ask=CHOOSE(["yes, both", "no, neither", "only 13"], 1,
                 "With 5, the sides 4 and 5 together are exactly 9, so they lie flat along it. With 13, the 4 and the 9 lie flat along the 13. Neither makes a triangle.")),
    B("Neither. At 5 or at 13 the sides lie flat in a straight line. So the third side can be 6, 7, 8, 9, 10, 11 or 12.",
      LB("l5", "6, 7, 8, 9, 10, 11, 12")),
    B("Count them: there are 7 different lengths.",
      *ANSL("a", "7 different lengths", "7")),
    B("A slip to dodge: 12 minus 6 is 6, but that counts the jumps between the numbers. From 6 to 12 there are 7 numbers, because both ends are in.",
      W("l6", "12 − 6 = 6"), W("l7", "6 + 1 = 7")),
    B("Check the two ends. 4 plus 6 is 10, which beats 9. And 4 plus 9 is 13, which beats 12. Both make triangles.",
      W("l8", "4 + 6 = 10 > 9"), W("l9", "4 + 9 = 13 > 12")),
    B("So the third side lies between the difference and the sum of the other two, without touching either. Here that gives 7 lengths."),
)

# PQ = 7 km, QR = 12 km: which could PR be?
LESSONS["G5A_TRIANGLES_004"] = LESSON(
    B("Villages P, Q and R are not in one straight line. Road PQ is 7 kilometres and road QR is 12 kilometres. Which of these four lengths could road PR be?",
      GIVEN("q", "PQ = 7 km, QR = 12 km. Which could PR be?"),
      LB("o", "19 km    5 km    18 km    4 km")),
    B("The three roads make a triangle. Going from P to R, the straight road must be shorter than the way round through Q. The way round is 7 plus 12, which is 19.",
      W("l1", "7 + 12 = 19"), LB("l2", "PR < 19")),
    B("So could PR be exactly 19 kilometres?",
      ask=CHOOSE(["yes", "no"], 1,
                 "PR is 19 only if going straight is just as long as going through Q. That happens only when Q is on the straight line from P to R, and the story says it is not.")),
    B("No. 19 would put all three villages in one straight line. Cross it out.",
      STRIKE("o", "19 km", "in a line")),
    B("PR cannot be too short either. Roads PQ and PR together must be longer than QR. 12 minus 7 is 5, so PR must be more than 5.",
      W("l3", "12 − 7 = 5"), LB("l4", "PR > 5")),
    B("So 5 is out: it only just reaches, in a straight line again. And 4 is out, because 7 plus 4 is 11, too short to cover the 12.",
      STRIKE("o", "5 km", "in a line"), W("l5", "7 + 4 = 11 < 12"), STRIKE("o", "4 km", "too short")),
    B("Only 18 is left. It is more than 5 and less than 19. So road PR could be 18 kilometres.",
      *ANSC("a", "5 < 18 < 19", 18), CIRC("o", "18 km")),
    B("Check: 7 plus 12 is 19, more than 18. And 7 plus 18 is 25, more than 12. The triangle closes.",
      W("l6", "7 + 18 = 25 > 12")),
    B("So the third side of a triangle is always between the difference and the sum of the other two. Here only 18 fits."),
)

# Whole-number sides, perimeter 13: how many triangles?
LESSONS["G5A_TRIANGLES_005"] = LESSON(
    B("How many different triangles have whole number sides and a perimeter of 13 centimetres? The same three lengths count only once.",
      GIVEN("q", "Whole-number sides, perimeter 13 cm. How many triangles?")),
    B("Lots of sets of three numbers add up to 13, like 1, 1 and 11. But most of them cannot close up into a triangle. So we start with the longest side.",
      W("l1", "1 + 1 + 11 = 13"), NOTE("l1", "11", "far too long")),
    B("The longest side must be shorter than the other two together. So it is less than half of 13, which is 6 and a half. The longest side is 6 at most.",
      LB("l2", "Longest side < 6½ → at most 6")),
    B("And how small can the longest side be? Could it be 4?",
      W("l3", "4 + 4 + 4 = 12"),
      ask=CHOOSE(["yes", "no"], 1,
                 "If the longest side is 4, the three sides add up to 12 at most. That cannot reach 13.")),
    B("No: 4 plus 4 plus 4 is only 12. So the longest side is 5 or 6. That leaves just two cases to list.",
      LB("l4", "Longest side: 5 or 6")),
    B("Longest side 6: the other two add up to 7. They can be 6 and 1, or 5 and 2, or 4 and 3. That is 3 triangles.",
      W("l5", "13 − 6 = 7"), LB("l6", "6, 6, 1     6, 5, 2     6, 4, 3")),
    B("Longest side 5: the other two add up to 8, and neither may be more than 5. They can be 5 and 3, or 4 and 4. That is 2 triangles.",
      W("l7", "13 − 5 = 8"), LB("l8", "5, 5, 3     5, 4, 4")),
    B("3 triangles and 2 triangles make 5 in all.",
      *ANSC("a", "3 + 2 = 5", 5)),
    B("Check one that looks risky: 6, 6 and 1. Its two shorter sides are 6 and 1, which make 7, and 7 beats 6. It closes.",
      W("l9", "6 + 1 = 7 > 6")),
    B("So fix the longest side first: it must be less than half the perimeter. Then list in order. There are 5 triangles."),
)
