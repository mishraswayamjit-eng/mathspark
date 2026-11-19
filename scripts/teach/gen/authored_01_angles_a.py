"""Angles and lines, G5A_ANGLES_001 to 007: one lesson each, written by hand."""
from authored_01_lib import (ANS, ANSC, B, CHOOSE, CIRC, GIVEN, LANS, LB, LESSON, NOTE, UL, W)  # noqa: F401

LESSONS = {}
P = "G5A_ANGLES_"

# Which time gives exactly 45 degrees? 4:30
LESSONS[P + "001"] = LESSON(
    B("At which of these times is the smaller angle between the two hands exactly 45 degrees? 1:30, 4:30, 10:30, or 12:45.",
      GIVEN("q", "Exactly 45° between the hands?  1:30, 4:30, 10:30, 12:45")),
    B("First, the size of one gap. The clock face is a full turn of 360 degrees, split into 12 equal gaps between the numbers. So each gap is 30 degrees.",
      W("l1", "360 ÷ 12 = 30")),
    B("Take 4:30. The minute hand points at the 6. Where is the hour hand?",
      ask=CHOOSE(["exactly at the 4", "halfway between 4 and 5", "exactly at the 5"], 1,
                 "At half past, the hour hand has had half an hour to move on. So it is halfway from the 4 to the 5.")),
    B("That is the trap with clock angles. The hour hand does not wait at the 4. By half past, it has crept halfway to the 5.",
      LB("l2", "4:30: hour hand halfway between 4 and 5")),
    B("From the hour hand to the 5 is half a gap, which is 15 degrees. From the 5 to the 6 is a whole gap, 30 degrees.",
      W("l3", "30 ÷ 2 = 15")),
    B("15 plus 30 is 45. So at 4:30 the angle is exactly 45 degrees.",
      W("l4", "15 + 30 = 45"), CIRC("l4", "45")),
    B("Let's make sure of the others. At 1:30 the hands are 4 and a half gaps apart, and at 10:30 as well. That is 135 degrees each time.",
      W("l5", "4.5 × 30 = 135")),
    B("At 12:45 the minute hand is on the 9, and the hour hand is three quarters of the way from 12 to 1. That is 3 and three quarters gaps, which is 112.5 degrees.",
      W("l6", "3.75 × 30 = 112.5")),
    B("So the only time that gives 45 degrees is 4:30.",
      LANS("a", "At 4:30 the angle is 45°"), CIRC("a", "4:30")),
    B("For a clock angle: count the gaps between the hands, 30 degrees each, and always move the hour hand on for the minutes that have passed."),
)

# Hands together at 12: 66 degrees apart after 12 minutes
LESSONS[P + "002"] = LESSON(
    B("At 12 o'clock the two hands lie exactly together. After how many minutes is the angle between them 66 degrees for the first time?",
      GIVEN("q", "Hands together at 12:00. Minutes until they are 66° apart?")),
    B("Both hands move, so we need to know how fast each one turns. The minute hand goes all the way round, 360 degrees, in 60 minutes. That is 6 degrees every minute.",
      W("l1", "360 ÷ 60 = 6")),
    B("The hour hand moves just one gap, 30 degrees, in those 60 minutes. That is half a degree every minute.",
      W("l2", "30 ÷ 60 = 0.5")),
    B("So each minute, by how much does the angle between the hands grow?",
      ask=CHOOSE(["6 degrees", "6 and a half degrees", "5 and a half degrees"], 2,
                 "Both hands turn the same way round. The minute hand pulls ahead by 6 degrees, but the hour hand follows by half a degree. So the angle grows by the difference.")),
    B("6 minus a half is 5 and a half degrees each minute. To keep away from halves, double it: 11 degrees every 2 minutes.",
      W("l3", "6 − 0.5 = 5.5"), W("l4", "5.5 × 2 = 11")),
    B("Now, how many lots of 11 make 66? 66 divided by 11 is 6.",
      W("l5", "66 ÷ 11 = 6")),
    B("6 lots of 2 minutes is 12 minutes. The angle is 66 degrees after 12 minutes.",
      *ANSC("l6", "6 × 2 = 12", 12)),
    B("The tempting answer is 11 minutes, because 66 divided by 6 is 11. But that forgets the hour hand, which has been moving all the time."),
    B("Check: in 12 minutes the minute hand turns 72 degrees and the hour hand turns 6. And 72 minus 6 is 66.",
      W("c1", "12 × 6 = 72"), W("c2", "12 × 0.5 = 6"), W("c3", "72 − 6 = 66")),
    B("So when both hands move, work with how fast the angle between them grows, not with one hand alone. Here it takes 12 minutes."),
)

# 10:10, the larger angle: 245 degrees
LESSONS[P + "003"] = LESSON(
    B("At 10:10, what is the larger angle between the hour hand and the minute hand, measured the long way round the clock?",
      GIVEN("q", "At 10:10, the larger angle between the hands?")),
    B("Let's measure both hands from the 12, going clockwise. The full turn is 360 degrees and there are 12 gaps, so each gap between numbers is 30 degrees.",
      W("l0", "360 ÷ 12 = 30")),
    B("The minute hand is at the 2. That is 2 gaps from the 12, so 60 degrees.",
      W("l1", "2 × 30 = 60")),
    B("Now the hour hand. At 10:10, where is it?",
      ask=CHOOSE(["exactly at the 10", "a little past the 10", "at the 11"], 1,
                 "10 minutes have passed since 10 o'clock, and the hour hand never stops moving. So it has crept a little past the 10.")),
    B("The 10 is 10 gaps round, which is 300 degrees. The hour hand moves half a degree each minute, so in 10 minutes it has moved 5 degrees more. It is at 305.",
      W("l2", "10 × 30 = 300"), W("l3", "10 × 0.5 = 5"), W("l4", "300 + 5 = 305")),
    B("Going clockwise from the minute hand at 60 to the hour hand at 305 is 305 minus 60, which is 245 degrees.",
      W("l5", "305 − 60 = 245")),
    B("Is 245 the long way round, or the short way?",
      ask=CHOOSE(["the long way", "the short way"], 0,
                 "Compare it with half of the full turn of 360. 245 is more than half a turn, so it must be the long way round.")),
    B("The other way round is 360 minus 245, which is 115. That is the smaller angle. The question wants the larger one, 245 degrees.",
      W("l6", "360 − 245 = 115"), LANS("a", "Larger angle = 245°"), CIRC("a", "245°")),
    B("Two traps here. Leaving the hour hand exactly on the 10 gives 240. And 115 is a real angle between the hands, but it is the short way round.",
      W("l7", "300 − 60 = 240")),
    B("So for a clock angle: place each hand in degrees from the 12, subtract, and then check which way round the question wants."),
)

# Minute hand turns 150 degrees: the hour hand turns 12.5 degrees
LESSONS[P + "004"] = LESSON(
    B("While the minute hand of a clock turns through 150 degrees, through how many degrees does the hour hand turn?",
      GIVEN("q", "Minute hand turns 150°. How far does the hour hand turn?")),
    B("The two hands are tied together by time. So the first thing to find is how long the minute hand takes to turn 150 degrees."),
    B("The minute hand turns a full 360 degrees in 60 minutes, which is 6 degrees a minute. 150 divided by 6 is 25. So 25 minutes pass.",
      W("l1", "360 ÷ 60 = 6"), W("l2", "150 ÷ 6 = 25")),
    B("In a whole hour, the hour hand only moves from one number to the next, which is 30 degrees. How much is that each minute?",
      LB("l3", "Hour hand: 30° in 60 minutes"),
      ask=CHOOSE(["half a degree", "2 degrees", "6 degrees"], 0,
                 "30 degrees are shared out over 60 minutes. 30 is half of 60, so the hour hand moves half a degree each minute.")),
    B("30 divided by 60 is a half. So the hour hand turns half a degree every minute.",
      W("l4", "30 ÷ 60 = 0.5")),
    B("In 25 minutes it turns 25 halves. Half of 25 is 12.5 degrees.",
      *ANSC("l5", "25 × 0.5 = 12.5", "12.5")),
    B("The trap is stopping at 25. That is the number of minutes that pass, not the degrees the hour hand turns."),
    B("Here is a quick check. The hour hand is 12 times slower than the minute hand. And 150 divided by 12 is 12.5 as well.",
      W("l6", "150 ÷ 12 = 12.5")),
    B("So when two hands are linked, find the time first. Then use each hand's own speed."),
)

# OP and OQ halve two angles on a straight line: POQ is 90 degrees
LESSONS[P + "005"] = LESSON(
    B("Point O is on a straight line A B. A ray O C makes two angles, A O C and C O B. Ray O P cuts A O C in half, and ray O Q cuts C O B in half. How big is angle P O Q?",
      GIVEN("q", "O on line AB. OP halves angle AOC, OQ halves angle COB. POQ?")),
    B("Angles A O C and C O B sit side by side on a straight line. So together they make 180 degrees.",
      LB("l1", "AOC + COB = 180°")),
    B("Angle P O Q is made of two pieces: from O P to O C, and from O C to O Q. The first piece is half of A O C. The second is half of C O B.",
      LB("l2", "POQ = half of AOC + half of COB")),
    B("Half of one angle, plus half of the other. What is that the same as?",
      ask=CHOOSE(["half of their total", "their total", "it depends on OC"], 0,
                 "Halving each part and then adding gives the same as adding first and then halving. So it is half of the total.")),
    B("Half of each is the same as half of the total. The total is 180, and half of 180 is 90.",
      W("l3", "180 ÷ 2 = 90")),
    B("So angle P O Q is 90 degrees, a right angle.",
      LANS("a", "Angle POQ = 90°"), CIRC("a", "90°")),
    B("Does it change when O C moves? Try it. If A O C is 100 and C O B is 80, the halves are 50 and 40. They make 90.",
      W("c1", "100 + 80 = 180"), W("c2", "50 + 40 = 90")),
    B("Move O C so that the angles are 60 and 120. The halves are 30 and 60. That is 90 again!",
      W("c3", "60 + 120 = 180"), W("c4", "30 + 60 = 90")),
    B("The trap is thinking we must know where O C is. We don't. When two angles on a straight line are each halved, the two halves always make 90 degrees."),
)

# Two lines cross; three angles add to 250: the smallest is 70 degrees
LESSONS[P + "006"] = LESSON(
    B("Two straight lines cross, making 4 angles. Three of the 4 angles add up to 250 degrees. What is the smallest of the 4 angles?",
      GIVEN("q", "Two lines cross. Three of the four angles add up to 250°")),
    B("The 4 angles go all the way round a point, so they make a full turn, 360 degrees. Three of them make 250. So the one left out is 360 minus 250, which is 110.",
      W("l1", "360 − 250 = 110")),
    B("Is 110 the smallest? Let's find the others. What do we know about the angle opposite the 110?",
      ask=CHOOSE(["it is also 110", "it is 70", "it is 250"], 0,
                 "When two straight lines cross, the angles opposite each other are equal. So the angle opposite the 110 is 110 as well.")),
    B("Opposite angles are equal, so there are two angles of 110.",
      LB("l2", "Opposite angles: 110° and 110°")),
    B("Each of the other two angles sits beside a 110 on a straight line. A straight line is 180, so each one is 180 minus 110, which is 70.",
      W("l3", "180 − 110 = 70")),
    B("So the 4 angles are 110, 70, 110 and 70. The smallest is 70 degrees.",
      LANS("a", "Smallest angle = 70°"), CIRC("a", "70°")),
    B("The trap is stopping at 110, the angle we found first. It was the one left out, but it is not the smallest."),
    B("Check: the three that were added are 70, 110 and 70. They make 250, just as the question says.",
      W("c1", "70 + 110 + 70 = 250")),
    B("So when two lines cross, there are only two sizes of angle. Opposite angles are equal, and neighbours add up to 180."),
)

# Supplement is 4 times the complement: the angle is 60 degrees
LESSONS[P + "007"] = LESSON(
    B("The supplement of an angle is 4 times its complement. What is the angle?",
      GIVEN("q", "Supplement of an angle = 4 × its complement. The angle?")),
    B("Two words to pin down. The complement is what the angle needs to reach 90 degrees. The supplement is what it needs to reach 180.",
      LB("l1", "complement = 90° − angle"), LB("l2", "supplement = 180° − angle")),
    B("For the same angle, how much bigger is the supplement than the complement?",
      ask=CHOOSE(["90 degrees", "180 degrees", "it depends on the angle"], 0,
                 "Both start from the same angle. One climbs to 90 and the other climbs to 180. So the supplement always goes 90 further.")),
    B("180 minus 90 is 90. So the supplement is always the complement plus 90.",
      W("l3", "180 − 90 = 90"), LB("l4", "supplement = complement + 90°")),
    B("Here the supplement is 4 lots of the complement. That is 1 lot, plus 3 more lots. So those 3 extra lots must be the 90.",
      LB("l5", "3 × complement = 90°")),
    B("90 divided by 3 is 30. So the complement is 30 degrees.",
      W("l6", "90 ÷ 3 = 30")),
    B("Careful: 30 is the complement, not the angle. The angle is 90 minus 30, which is 60 degrees.",
      *ANSC("l7", "90 − 30 = 60", 60)),
    B("Check: the complement of 60 is 30. Its supplement is 180 minus 60, which is 120. And 4 times 30 is 120.",
      W("c1", "180 − 60 = 120"), W("c2", "4 × 30 = 120")),
    B("So remember: the supplement is always 90 more than the complement. That one fact unlocks the question."),
)
