"""Angles and lines, G5A_ANGLES_015 to 020: one lesson each, written by hand."""
from authored_01_lib import (ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LANS, LB, LESSON, NOTE, UL, W)  # noqa: F401

LESSONS = {}
P = "G5A_ANGLES_"

# Faces NE; 3 right angles clockwise, 135 anticlockwise -> faces South; back to NE: 135 anticlockwise
LESSONS[P + "015"] = LESSON(
    B("Asha faces North-East. She turns through 3 right angles clockwise, and then 135 degrees anticlockwise. What is the smallest turn that makes her face North-East again?",
      GIVEN("q", "Faces NE. Turns 3 right angles clockwise, 135° anticlockwise")),
    B("First find where she ends up. 3 right angles is 3 times 90, which is 270 degrees.",
      W("l1", "3 × 90 = 270")),
    B("270 clockwise is a full turn less 90. So it lands in the same place as 90 anticlockwise. From North-East, that is North-West.",
      W("l2", "360 − 270 = 90"), LB("l3", "North-East → North-West")),
    B("Now 135 anticlockwise from North-West. 45 takes her to West, 45 more to South-West, and 45 more to South. So she now faces South.",
      W("l4", "45 + 45 + 45 = 135"), LB("l5", "North-West → West → South-West → South")),
    B("She faces South and wants North-East. Going clockwise, through West and North, how big is that turn?",
      ask=CHOOSE(["135 degrees", "180 degrees", "225 degrees"], 2,
                 "Clockwise from South it is 90 to West, 90 more to North, and then 45 more to North-East. Add those three pieces.")),
    B("Clockwise it is 90 plus 90 plus 45, which is 225 degrees.",
      W("l6", "90 + 90 + 45 = 225")),
    B("But that is more than half a turn, so the other way must be shorter. Anticlockwise, through South-East and East, it is 360 minus 225, which is 135.",
      W("l7", "360 − 225 = 135")),
    B("So the smallest turn is 135 degrees anticlockwise.",
      LANS("a", "135° anticlockwise"), CIRC("a", "135° anticlockwise")),
    B("The trap is stopping at the first turn that works. 225 clockwise does bring her back, but the question asks for the smallest turn. Always check both ways round."),
    B("So: follow the turns to see where she faces now, then measure the way back in both directions and pick the smaller."),
)

# Robot turns 135 each ring: faces North again after 8 rings
LESSONS[P + "016"] = LESSON(
    B("A toy robot faces North. Each time a bell rings, it turns 135 degrees clockwise. After how many rings does it face North again for the first time?",
      GIVEN("q", "Robot faces North. Each ring: turns 135° clockwise")),
    B("The robot faces North again when its total turning is a whole number of full turns. A full turn is 360 degrees.",
      LB("l1", "Full turns: 360, 720, 1080, ...")),
    B("Add up the turning, ring by ring: 135, 270, 405, 540.",
      LB("l2", "135, 270, 405, 540")),
    B("After 4 rings the total is 540. Is the robot facing North?",
      W("l3", "540 − 360 = 180"),
      ask=CHOOSE(["Yes, North", "No, it faces South"], 1,
                 "540 is one full turn of 360, and then 180 more. That extra half turn leaves the robot facing South.")),
    B("540 is a full turn and a half. So after 4 rings the robot faces South, exactly backwards. That is a clue: 4 more rings will bring it the rest of the way."),
    B("Keep adding: 675, 810, 945, 1080.",
      LB("l4", "675, 810, 945, 1080")),
    B("1080 is 3 times 360. That is exactly 3 full turns, and it is the first total that is a multiple of 360.",
      W("l5", "3 × 360 = 1080"), CIRC("l4", "1080")),
    B("1080 is the 8th total. So the robot faces North again after 8 rings.",
      ANS("l6", "8 × 135 = 1080"), CIRC("l6", "8")),
    B("The tempting answers are 3, because of the 3 full turns, and 4, because 540 looks neat. But we are counting rings, and only the 8th ring lands exactly on North."),
    B("So for a turn that repeats, keep adding until the total is a whole number of full turns. Here that takes 8 rings."),
)

# Four rays, 20 + 30 + 40: five of the six angles are acute
LESSONS[P + "017"] = LESSON(
    B("Four rays, O A, O B, O C and O D, start from the same point. Going round in order, the angles between neighbours are 20, 30 and 40 degrees. Counting every angle made by two of the rays, how many are acute?",
      GIVEN("q", "Rays OA, OB, OC, OD. AOB = 20°, BOC = 30°, COD = 40°")),
    B("Every angle needs two rays as its arms. With 4 rays, there are 6 ways to pick the two arms. So there are 6 angles to look at, not just the 3 we are given.",
      LB("l1", "AOB, BOC, COD, AOC, BOD, AOD")),
    B("The three given angles are 20, 30 and 40. All are smaller than a right angle, so all are acute. That is 3 so far."),
    B("Now the angles made of two neighbours joined together. A O C is 20 plus 30, which is 50. B O D is 30 plus 40, which is 70. Both are acute. That makes 5.",
      W("l2", "20 + 30 = 50"), W("l3", "30 + 40 = 70")),
    B("One angle is left: A O D, made of all three parts. Is it acute?",
      ask=CHOOSE(["Yes, it is acute", "No, it is a right angle", "No, it is obtuse"], 1,
                 "Add all three parts: 20, 30 and 40. An acute angle has to be less than a right angle. Is this one?")),
    B("20 plus 30 plus 40 is exactly 90. That is a right angle. Acute means less than 90, so A O D does not count.",
      W("l4", "20 + 30 + 40 = 90"), NOTE("l4", "90", "right angle")),
    B("So the acute angles are 20, 30, 40, 50 and 70. There are 5 of them.",
      LANS("a", "Acute: 20°, 30°, 40°, 50°, 70°. That is 5 angles"), CIRC("a", "5 angles")),
    B("Two traps here. Counting only the 3 given angles misses the ones made by joining. And counting all 6 forgets that an angle of exactly 90 is not acute."),
    B("So list every pair of rays, find each angle, and test each one against the meaning of the word. Here 5 angles are acute."),
)

# Supplementary angles: they cannot both be acute
LESSONS[P + "018"] = LESSON(
    B("Two angles are supplementary. Which statement is true for every such pair? One must be obtuse. They cannot both be acute. They cannot be equal. Or, the larger one is always more than a right angle.",
      GIVEN("q", "Supplementary angles. Which statement is always true?")),
    B("Supplementary angles add up to 180 degrees. A statement that is always true must survive every pair. So let's hunt for a pair that breaks a statement.",
      LB("l1", "angle + angle = 180°")),
    B("Can you think of a supplementary pair where the two angles are equal?",
      ask=CHOOSE(["90 and 90", "60 and 60", "100 and 100"], 0,
                 "Equal angles that add up to 180 must each be half of 180. And half of 180 is 90.")),
    B("90 and 90 make 180. This is the pair most people forget, and that is the trap in this question.",
      W("l2", "90 + 90 = 180")),
    B("Test the statements on it. One must be obtuse? Neither is. They cannot be equal? They are. The larger is more than 90? It is exactly 90. One pair breaks three statements.",
      LB("l3", "90° and 90°: not obtuse, equal, not more than 90°")),
    B("That leaves: they cannot both be acute. Acute means less than 90. So two acute angles add up to less than 90 plus 90, which is less than 180."),
    B("Take 89 and 89, the biggest acute angles in whole degrees. They only reach 178. Two acute angles can never be supplementary.",
      W("l4", "89 + 89 = 178"), W("l5", "178 < 180")),
    B("So the statement that is always true is: they cannot both be acute.",
      LANS("a", "They cannot both be acute"), CIRC("a", "They cannot both be acute")),
    B("To test an always statement, look for one pair that breaks it. The equal pair, 90 and 90, is a good one to try first."),
)

# AOB = 70, BOC = 50, sharing OB: AOC is 20 or 120
LESSONS[P + "019"] = LESSON(
    B("Angle A O B is 70 degrees and angle B O C is 50 degrees. The two angles share the arm O B. What are all the possible sizes of angle A O C?",
      GIVEN("q", "Angle AOB = 70°, angle BOC = 50°, sharing arm OB. AOC?")),
    B("Picture O B first, with O A 70 degrees away from it. Now we add O C, 50 degrees from O B. But on which side of O B? The question does not say."),
    B("So how many places can ray O C go?",
      ask=CHOOSE(["only 1", "2, one on each side of OB", "lots of places"], 1,
                 "O C must be 50 degrees from O B. It can swing 50 degrees to one side of O B, or 50 degrees to the other. That makes 2 places.")),
    B("First place: O C is on the far side of O B, away from O A. The two angles sit side by side, so we add. 70 plus 50 is 120.",
      W("l1", "70 + 50 = 120")),
    B("Second place: O C is on the same side as O A, tucked inside the 70. Now the angles overlap, so we subtract. 70 minus 50 is 20.",
      W("l2", "70 − 50 = 20")),
    B("Both pictures fit the question. So angle A O C can be 20 degrees or 120 degrees.",
      LANS("a", "Angle AOC = 20° or 120°"), CIRC("a", "20° or 120°")),
    B("The trap is drawing just one picture and stopping at 120. When a question asks for every possible size, ask yourself: could this be drawn another way?"),
    B("Check the second picture. From O A it is 20 degrees to O C, and then 50 more to O B. That makes 70, which is angle A O B.",
      W("c1", "20 + 50 = 70")),
    B("So when two angles share an arm, they can sit side by side or overlap. Add for one, subtract for the other: 120 or 20."),
)

# 9 spokes: smaller angle between spoke 2 and spoke 8 is 120 degrees
LESSONS[P + "020"] = LESSON(
    B("A wheel has 9 equally spaced spokes, numbered 1 to 9 in order. What is the smaller angle between spoke 2 and spoke 8?",
      GIVEN("q", "9 equal spokes. Smaller angle between spoke 2 and spoke 8?")),
    B("9 spokes share the full turn equally, so there are 9 equal gaps. Each gap is 360 divided by 9, which is 40 degrees.",
      W("l1", "360 ÷ 9 = 40")),
    B("Count the gaps going up from spoke 2 to spoke 8. 8 minus 2 is 6 gaps. That is 6 times 40, which is 240 degrees.",
      W("l2", "8 − 2 = 6"), W("l3", "6 × 40 = 240")),
    B("The question wants the smaller angle. Is 240 the one?",
      ask=CHOOSE(["Yes, 240", "No, go the other way round"], 1,
                 "Compare 240 with half of the full turn of 360. It is more than half, so there must be a shorter way round the wheel.")),
    B("240 is more than half a turn. So go the other way: from spoke 8 to 9, then to 1, then to 2. That is only 3 gaps.",
      LB("l4", "8 → 9 → 1 → 2: 3 gaps")),
    B("3 times 40 is 120. The smaller angle is 120 degrees.",
      *ANSC("l5", "3 × 40 = 120", 120)),
    B("Check: the two ways round should make a full turn. 240 plus 120 is 360.",
      W("c1", "240 + 120 = 360")),
    B("On a wheel there are always two ways round. Count the gaps both ways, and pick the one the question asks for."),
)
