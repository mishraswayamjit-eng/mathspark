"""Lessons written one by one: Grade 4 circles, G4A_CIRCLE_025 to 034."""
from g4_gr4_quads_lib import A, B, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring, strike

F = figure_getter("gr4_circle")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["G4A_CIRCLE_025"] = lesson([
    B("A wire 132 centimetres long is cut into 3 equal pieces. Each piece is bent into a circle. What is the radius of each circle? Use 22 over 7 for pi.",
      G("Wire 132 cm, cut into 3 equal pieces. Each makes a circle."), GQ("q2", "Radius of each circle = ?  (π = 22/7)"),
      F("G4A_CIRCLE_025")),
    B("Careful: the whole wire does not make one circle. First cut it. 132 divided by 3 is 44 centimetres for each piece.",
      W("l1", "132 ÷ 3 = 44"), note("l1", "44", "one piece", "below")),
    B("One piece goes once round its circle. So 44 centimetres is that circle's what?",
      ask=choose(["radius", "diameter", "circumference"], 2,
                 "The wire is bent to make the edge of the circle. The distance all the way round the edge is the circumference.")),
    B("It is the circumference. And circumference is 2 times 22 over 7 times r. 2 times 22 is 44, so that is 44 times r, divided by 7.",
      L("l2", "Circumference = 2 × 22/7 × r"), W("l3", "2 × 22 = 44")),
    B("44 times r, divided by 7, must give 44. So r divided by 7 is 1, and r is 7.", L("l4", "44 × r ÷ 7 = 44")),
    B("The radius of each circle is 7 centimetres.", A("a", "Radius = 7 cm", label=True), ring("a", "7")),
    B("Check: 2 times 22 over 7 times 7. The 7s cancel, and 2 times 22 is 44. That is one piece of wire.",
      W("c", "2 × 22/7 × 7 = 44")),
    B("So: cut first, then treat each piece as a circumference and work back to the radius."),
])

LESSONS["G4A_CIRCLE_026"] = lesson([
    B("Twelve equal circles sit inside a rectangle in 3 rows of 4, touching each other and the sides. The rectangle's area is 432 square centimetres. What is each circle's radius?",
      G("12 circles in a rectangle: 3 rows of 4."), GQ("q2", "Area of rectangle = 432 sq cm. Radius = ?"),
      F("G4A_CIRCLE_026")),
    B("Imagine a little square box drawn round every circle. The 12 boxes fill the rectangle exactly, like tiles.",
      L("l1", "12 equal little squares fill the rectangle")),
    B("So the 432 is shared equally among 12 little squares. 432 divided by 12 is 36. Check: 12 times 30 is 360, 12 times 6 is 72, and together they make 432.",
      W("l2", "432 ÷ 12 = 36"), W("l2a", "12 × 30 = 360"), W("l2b", "12 × 6 = 72"), W("l2c", "360 + 72 = 432")),
    B("A little square has an area of 36. How long is its side?",
      ask=choose(["6 cm", "9 cm", "18 cm"], 0,
                 "Area of a square is side times side. Which number times itself makes 36? Try 6 times 6.")),
    B("6 times 6 is 36. So each little square has a side of 6 centimetres.", W("l3", "6 × 6 = 36")),
    B("The circle just fits its square. So the side of the square, 6, is the circle's diameter. Don't stop here!",
      L("l4", "side of little square = diameter = 6 cm")),
    B("The question asks for the radius. Half of 6 is 3.", W("l5", "6 ÷ 2 = 3")),
    B("The radius of each circle is 3 centimetres.", A("a", "Radius = 3 cm", label=True), ring("a", "3")),
    B("Check: the rectangle is 4 times 6 long, which is 24, and 3 times 6 wide, which is 18. And 24 times 18 is 432.",
      W("c1", "4 × 6 = 24"), W("c2", "3 × 6 = 18"), W("c3", "24 × 18 = 432")),
])

LESSONS["G4A_CIRCLE_027"] = lesson([
    B("A round pond has a radius of 7 metres. A path 7 metres wide runs all the way round it. What is the area of the path? Use 22 over 7 for pi.",
      G("Pond: radius 7 m. Path 7 m wide all round."), GQ("q2", "Area of the path = ?  (π = 22/7)"),
      F("G4A_CIRCLE_027")),
    B("The path is a ring. A ring is a big circle with a smaller circle taken out of its middle.",
      L("l1", "path = big circle − pond")),
    B("The big circle is the pond and the path together. What is its radius?",
      ask=choose(["7 m", "14 m", "21 m"], 1,
                 "From the centre, go 7 metres to the edge of the pond. Then 7 more metres across the path.")),
    B("7 for the pond and 7 more for the path: 14 metres.", W("l2", "7 + 7 = 14")),
    B("Big circle: 22 over 7, times 14, times 14. 14 divided by 7 is 2. So we have 22 times 2 times 14.",
      W("l3", "22/7 × 14 × 14"), strike("l3", "7"), W("l4", "14 ÷ 7 = 2")),
    B("22 times 2 is 44. 44 times 14: 44 times 10 is 440, and 44 times 4 is 176. Together, 616.",
      W("l5", "44 × 10 = 440"), W("l6", "44 × 4 = 176"), W("l7", "440 + 176 = 616")),
    B("The pond: 22 over 7, times 7, times 7. One 7 cancels. That leaves 22 times 7, which is 154.",
      W("l8", "22 × 7 = 154")),
    B("Take the pond out of the big circle. 616 minus 154 is 462.", W("l9", "616 − 154 = 462")),
    B("The area of the path is 462 square metres.", A("a", "Area of path = 462 sq m", label=True), ring("a", "462")),
    B("Surprised? The path is as wide as the pond's radius, but its area is 3 times the pond's. Rings on the outside are big!"),
])

LESSONS["G4A_CIRCLE_028"] = lesson([
    B("When a circle's radius is made twice as long, its circumference becomes 88 centimetres longer. What was the radius at the start? Use 22 over 7 for pi.",
      G("Radius doubled: circumference grows by 88 cm."), GQ("q2", "Radius at the start = ?  (π = 22/7)"),
      F("G4A_CIRCLE_028")),
    B("Circumference is 2 times pi times the radius. If we double the radius, what happens to the circumference?",
      L("l1", "Circumference = 2 × π × radius"),
      ask=choose(["It doubles too", "It grows by 2 cm", "It stays the same"], 0,
                 "The radius is multiplied into the circumference. Make the radius twice as big, and the whole answer is twice as big.")),
    B("It doubles. So the new circumference is the old one, and then the old one again.",
      L("l2", "new = old + old")),
    B("Here's the key. The extra part is exactly one old circumference. And the extra part is 88. So the old circumference was 88.",
      L("l3", "extra = old = 88 cm"), box("l3", "88 cm")),
    B("Careful: 88 is not the new circumference. It is the amount it grew, which equals the old one."),
    B("Now find the radius. 2 times 22 is 44, so the circumference is 44 times r, divided by 7. 88 divided by 44 is 2.",
      W("l4", "2 × 22 = 44"), W("l5", "88 ÷ 44 = 2")),
    B("So r divided by 7 is 2, and r is 2 times 7, which is 14.", W("l6", "2 × 7 = 14")),
    B("The radius at the start was 14 centimetres.", A("a", "Radius at the start = 14 cm", label=True), ring("a", "14")),
    B("Check: the doubled radius is 28. Its circumference is 44 times 4, which is 176. And 176 minus 88 is 88. It grew by 88.",
      W("c1", "2 × 14 = 28"), W("c2", "44 × 4 = 176"), W("c3", "176 − 88 = 88")),
])

LESSONS["G4A_CIRCLE_029"] = lesson([
    B("Seven points are marked on a circle. Each point is joined to every other point, except the two right next to it. How many chords are drawn?",
      G("7 points on a circle. Join each to all but its 2 neighbours."), GQ("q2", "How many chords?")),
    B("Stand on one point. There are 7 points in all. You can't join to yourself, and you skip your 2 neighbours. That rules out 3 points.",
      W("l1", "1 + 2 = 3"), note("l1", "3", "not joined", "below")),
    B("So how many chords leave your point?",
      ask=choose(["4", "5", "6"], 0, "7 points, and 3 of them are ruled out: yourself and your two neighbours. Take 3 from 7.")),
    B("7 minus 3 is 4. Each point sends out 4 chords.", W("l2", "7 − 3 = 4")),
    B("7 points with 4 chords each: 7 times 4 is 28. But wait. Is 28 the answer?", W("l3", "7 × 4 = 28")),
    B("Here's the trap. Every chord has two ends, so we counted each chord twice: once from each end.",
      note("l3", "28", "each counted twice", "below")),
    B("So we halve it. Half of 28 is 14.", W("l4", "28 ÷ 2 = 14")),
    B("14 chords are drawn.", A("a", "14 chords", label=True), ring("a", "14")),
    B("Counting from every point is quick, but remember that each line gets counted from both of its ends. Halve at the end."),
])

LESSONS["G4A_CIRCLE_030"] = lesson([
    B("Eight points are equally spaced round a circle. Every pair is joined by a chord. How many of these chords are not diameters?",
      G("8 equally spaced points on a circle. Every pair is joined."), GQ("q2", "How many chords are NOT diameters?")),
    B("Plan: count all the chords, then take away the ones that are diameters.", L("l0", "all chords − diameters")),
    B("All the chords. The first point joins 7 others. The next gives 6 new chords, then 5, 4, 3, 2 and 1.",
      W("l1", "7 + 6 + 5 + 4 + 3 + 2 + 1 = 28")),
    B("That adds up to 28 chords. Now, when is a chord a diameter?",
      ask=choose(["when it joins neighbours", "when it joins opposite points"], 1,
                 "A diameter passes through the centre. That happens only when the two points are straight across the circle from each other.")),
    B("A diameter joins two opposite points. 8 points make 4 opposite pairs. So there are 4 diameters.",
      W("l2", "8 ÷ 2 = 4"), note("l2", "4", "diameters", "below")),
    B("Careful: not 8 diameters. Each diameter uses up 2 points, one at each end."),
    B("Take the diameters away. 28 minus 4 is 24.", W("l3", "28 − 4 = 24")),
    B("24 of the chords are not diameters.", A("a", "24 chords", label=True), ring("a", "24")),
    B("When a question says not, count everything first, then take away the ones you don't want."),
])

LESSONS["G4A_CIRCLE_031"] = lesson([
    B("A small circle inside a big circle touches it at one point, and also passes through the big circle's centre. The big diameter is 24 centimetres. How far apart are the centres?",
      G("Small circle inside big circle: touches it at one point"), GQ("q2", "and passes through its centre. Big diameter = 24 cm."),
      F("G4A_CIRCLE_031")),
    B("Start with the big circle. Its radius is half of 24, which is 12 centimetres.", W("l1", "24 ÷ 2 = 12")),
    B("So from the touching point to the big centre is 12 centimetres. The small circle passes through both of those points.",
      L("l2", "touching point to big centre = 12 cm")),
    B("The small circle stretches from the touching point right across to the big centre. So that 12 centimetres is the small circle's what?",
      ask=choose(["its radius", "its diameter"], 1,
                 "The two points are on opposite sides of the small circle, as far apart as they can be. That full width is its diameter.")),
    B("It is the small circle's diameter. And the small centre sits halfway along a diameter.", L("l3", "small diameter = 12 cm")),
    B("Half of 12 is 6. So the small centre is 6 centimetres from the big centre.", W("l4", "12 ÷ 2 = 6")),
    B("The centres are 6 centimetres apart.", A("a", "Centres are 6 cm apart", label=True), ring("a", "6")),
    B("We halved twice: 24 to 12 for the big radius, then 12 to 6 for the small radius. Each halving had its own reason."),
])

LESSONS["G4A_CIRCLE_032"] = lesson([
    B("Three coins of different sizes each touch the other two. The distances between their centres are 7, 8 and 9 centimetres. What is the radius of the largest coin?",
      G("3 touching coins. Centres are 7 cm, 8 cm, 9 cm apart."), GQ("q2", "Radius of the largest coin = ?"),
      F("G4A_CIRCLE_032")),
    B("When two coins touch, the distance between their centres is one radius plus the other radius. So each distance is two radii added.",
      L("l1", "each distance = radius + radius")),
    B("Add all three distances: 7 plus 8 plus 9 is 24. In that total, how many times is each coin's radius counted?",
      W("l2", "7 + 8 + 9 = 24"),
      ask=choose(["once", "twice", "3 times"], 1,
                 "Each coin touches two others. So its radius is part of two of the distances.")),
    B("Twice! So 24 is every radius counted twice. Halve it: the three radii add up to 12.",
      W("l3", "24 ÷ 2 = 12"), note("l3", "12", "all 3 radii", "below")),
    B("The two smaller coins have the closest centres: 7 centimetres. So their two radii add up to 7.",
      box("q", "7 cm")),
    B("All three radii make 12. The two smaller ones make 7. So the largest is 12 minus 7, which is 5.",
      W("l4", "12 − 7 = 5")),
    B("The radius of the largest coin is 5 centimetres.", A("a", "Largest radius = 5 cm", label=True), ring("a", "5")),
    B("Check: the radii are 3, 4 and 5. 3 plus 4 is 7. 3 plus 5 is 8. 4 plus 5 is 9. All three distances match!",
      W("c1", "3 + 4 = 7"), W("c2", "3 + 5 = 8"), W("c3", "4 + 5 = 9")),
    B("The trap is halving the 9. That only works for two equal coins, and these are all different."),
])

LESSONS["G4A_CIRCLE_033"] = lesson([
    B("Two round tins of radius 7 centimetres stand touching. A ribbon is pulled tight round both: straight across on two sides, and curving round the outer half of each tin. How long is it?",
      G("2 touching tins, radius 7 cm. A tight ribbon round both."), GQ("q2", "Length of the ribbon = ?  (π = 22/7)"),
      F("G4A_CIRCLE_033")),
    B("Split the ribbon into easy pieces: two straight parts, and two curved parts.", L("l1", "ribbon = 2 straight parts + 2 curved parts")),
    B("A straight part runs from one tin across to the other. It is as long as the gap between the centres: one radius plus one radius.",
      W("l2", "7 + 7 = 14")),
    B("There is a straight part on both sides. 2 times 14 is 28.", W("l3", "2 × 14 = 28"), note("l3", "28", "straight", "below")),
    B("Now the curves. The ribbon goes round half of one tin and half of the other. What do two half circles make?",
      ask=choose(["one whole circle", "two whole circles", "half a circle"], 0,
                 "Half and half make one whole. The two curved parts together are the same as going once round one tin.")),
    B("One whole circle! Its circumference is 2 times 22 over 7 times 7. The 7s cancel, leaving 2 times 22, which is 44.",
      W("l4", "2 × 22/7 × 7 = 44"), note("l4", "44", "curved", "below")),
    B("Add the straight parts and the curved parts. 28 plus 44 is 72.", W("l5", "28 + 44 = 72")),
    B("The ribbon is 72 centimetres long.", A("a", "Ribbon = 72 cm", label=True), ring("a", "72")),
    B("The trap is going right round both tins: 2 times 44, which is 88. The ribbon only hugs the outer half of each tin.",
      W("c", "2 × 44 = 88"), note("c", "88", "too long", "below")),
])

LESSONS["G4A_CIRCLE_034"] = lesson([
    B("The hour hand of a clock is 7 centimetres long. How far does its tip travel in one full day of 24 hours? Use 22 over 7 for pi.",
      G("Hour hand 7 cm long. One day = 24 hours."), GQ("q2", "Distance the tip travels = ?  (π = 22/7)"),
      F("G4A_CIRCLE_034")),
    B("As the hand turns, its tip draws a circle. The hand is the radius of that circle: 7 centimetres.",
      L("l1", "tip moves on a circle of radius 7 cm")),
    B("Once round is the circumference: 2 times 22 over 7 times 7. The 7s cancel, leaving 2 times 22, which is 44.",
      W("l2", "2 × 22/7 × 7 = 44"), note("l2", "44", "once round", "below")),
    B("Now think about the clock. How long does the hour hand take to go once round?",
      ask=choose(["1 hour", "12 hours", "24 hours"], 1,
                 "The minute hand goes round in 1 hour. The hour hand is slow: it creeps from 12 all the way back to 12 in 12 hours.")),
    B("12 hours for one round. A day has 24 hours, so the hour hand goes round 24 divided by 12 times: that is 2 rounds.",
      W("l3", "24 ÷ 12 = 2")),
    B("2 rounds of 44 centimetres. 2 times 44 is 88.", W("l4", "2 × 44 = 88")),
    B("The tip of the hour hand travels 88 centimetres in a day.", A("a", "Distance = 88 cm", label=True), ring("a", "88")),
    B("Two traps: stopping at one round, or thinking the hour hand goes round every hour. That one is the minute hand!"),
])
