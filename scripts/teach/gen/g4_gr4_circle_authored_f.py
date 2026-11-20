"""Lessons written one by one: Grade 4 circles, Q_CH21_012 to 020."""
from g4_gr4_quads_lib import A, B, FIG, G, L, THINK, W, box, choose, figure_getter, lesson, mark, note, ring, strike

F = figure_getter("gr4_circle")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["Q_CH21_012"] = lesson([
    B("A circular track has a radius of 35 metres. How far does a runner go in 3 laps? Use 22 over 7 for pi.",
      G("Track: radius 35 m. Distance in 3 laps = ? (π = 22/7)"), F("Q_CH21_012")),
    B("One lap is once round the track. Which measure of a circle is that?",
      ask=choose(["the area", "the circumference", "the diameter"], 1,
                 "The runner goes round the edge of the circle. The distance round the edge is the circumference.")),
    B("One lap is the circumference: pi times the diameter. The diameter is double the radius: 2 times 35 is 70.",
      L("l1", "Circumference = π × diameter"), W("l2", "2 × 35 = 70")),
    B("Now 22 over 7, times 70. Let the 7 divide first: 70 divided by 7 is 10.",
      W("l3", "22/7 × 70"), strike("l3", "7"), W("l4", "70 ÷ 7 = 10")),
    B("22 times 10 is 220. So one lap is 220 metres.", W("l5", "22 × 10 = 220"), note("l5", "220", "one lap", "below")),
    B("Don't stop at one lap! The runner goes round 3 times. 3 times 220 is 660.", W("l6", "3 × 220 = 660")),
    B("The runner goes 660 metres.", A("a", "3 laps = 660 m", label=True), ring("a", "660")),
    B("Always read to the end of the question. First one lap, then as many laps as it asks for."),
])

LESSONS["Q_CH21_014"] = lesson([
    B("A diameter divides a circle into two equal parts. What is each part called?",
      G("A diameter cuts a circle into 2 equal parts."), GQ("q2", "Each part is called a: ?"), F("Q_CH21_014")),
    B("A diameter passes straight through the centre. So the piece on one side is exactly the same as the piece on the other.",
      F("Q_CH21_014", 0)),
    B("Two equal parts. So what fraction of the circle is each part?",
      ask=choose(["a half", "a quarter", "a third"], 0,
                 "When something is shared into 2 equal parts, each part is one half.")),
    B("Each part is half of the circle.", L("l1", "each part = half of the circle"), F("Q_CH21_014", 1)),
    B("There is a little word that means half: semi. You may know it from semi final, the match halfway to the final.",
      L("l2", "semi = half")),
    B("So half of a circle is called a semicircle.", A("a", "A semicircle", label=True), ring("a", "semicircle"),
      F("Q_CH21_014", 2)),
    B("An arc is only a piece of the curved edge, and a quarter circle is one of four parts. Half a circle is a semicircle."),
])

LESSONS["Q_CH21_015"] = lesson([
    B("A wheel has a diameter of 28 centimetres. How many complete turns will it make to cover 440 centimetres? Use 22 over 7 for pi.",
      G("Wheel: diameter 28 cm. Turns to cover 440 cm = ?"), L("p", "π = 22/7"), F("Q_CH21_015")),
    B("Picture the wheel rolling. In one full turn, every bit of its rim touches the ground once. So how far does it move in one turn?",
      ask=choose(["its diameter", "its circumference", "its radius"], 1,
                 "In one turn the whole rim is laid out along the ground. The length of the rim is the circumference.")),
    B("One turn moves the wheel forward by one circumference. That is pi times the diameter: 22 over 7, times 28.",
      L("l1", "one turn = circumference"), W("l2", "22/7 × 28")),
    B("Let the 7 divide first: 28 divided by 7 is 4. Then 22 times 4 is 88.",
      strike("l2", "7"), W("l3", "28 ÷ 7 = 4"), W("l4", "22 × 4 = 88")),
    B("So each turn covers 88 centimetres. Careful: 88 is not the answer. It is the distance for one turn.",
      note("l4", "88", "one turn", "below")),
    B("How many 88s fit into 440? 88 times 5 is 440.", W("l5", "88 × 5 = 440"), W("l6", "440 ÷ 88 = 5")),
    B("The wheel makes 5 complete turns.", A("a", "5 turns", label=True), ring("a", "5")),
    B("For rolling wheels: one turn is one circumference. Then divide the whole distance by that."),
])

LESSONS["Q_CH21_016"] = lesson([
    B("Circles that have the same centre but different radii have a special name. What is it?",
      G("Same centre, different radii. These circles are called: ?")),
    B("Different radii means different sizes: a small circle, a bigger one, a bigger one still.",
      L("l1", "different radii: different sizes")),
    B("So could they be called equal circles, or congruent circles?",
      ask=choose(["Yes", "No, those mean the same size"], 1,
                 "Equal and congruent both mean exactly the same size. These circles have different radii, so they are different sizes.")),
    B("No. Those names are for circles of the same size. What is special here is that they all share one centre.",
      L("l2", "they share one centre"), mark("l2", "one centre")),
    B("Think of a target board, or the ripples when a stone drops into a pond. Rings inside rings, all round one middle point."),
    B("Circles like that are called concentric circles. Con means together, and centric is about the centre.",
      A("a", "Concentric circles", label=True), ring("a", "Concentric")),
    B("So: same centre, different sizes, concentric. Listen for the word centre hiding inside the name."),
])

LESSONS["Q_CH21_017"] = lesson([
    B("The area of a circle is 616 square centimetres. Find its radius. Use 22 over 7 for pi.",
      G("Circle: area = 616 cm². Radius = ? (π = 22/7)"), F("Q_CH21_017")),
    B("The area is 22 over 7, times the radius, times the radius. We know the area, so we work backwards.",
      L("l1", "22/7 × radius × radius = 616")),
    B("To undo 22 over 7, we divide by 22 and then multiply by 7. First, 616 divided by 22 is 28.",
      W("l2", "616 ÷ 22 = 28")),
    B("Then 28 times 7 is 196. So radius times radius is 196.", W("l3", "28 × 7 = 196"),
      note("l3", "196", "radius × radius", "below")),
    B("Careful: 196 is not the radius. It is the radius times itself. Which number times itself makes 196?",
      W("h1", "10 × 10 = 100"), W("h2", "20 × 20 = 400"),
      ask=choose(["14", "98", "49"], 0,
                 "Halving 196 will not do it. We need a number times itself. 10 times 10 is 100 and 20 times 20 is 400, so it lies between 10 and 20.")),
    B("It is between 10 and 20. Try 14: 14 times 10 is 140, and 14 times 4 is 56. Together, 196. Yes!",
      W("l4", "14 × 10 = 140"), W("l5", "14 × 4 = 56"), W("l6", "140 + 56 = 196")),
    B("The radius is 14 centimetres.", A("a", "Radius = 14 cm", label=True), ring("a", "14")),
    B("Working backwards from an area: undo the pi, then find the number that multiplies by itself. Two steps, not one."),
])

LESSONS["Q_CH21_018"] = lesson([
    B("A circle has a radius of 7 centimetres. Looking just at the numbers, which is larger: its circumference or its area?",
      G("Circle: radius 7 cm. Which number is larger:"), GQ("q2", "circumference or area?  (π = 22/7)"), F("Q_CH21_018")),
    B("We can't guess, so we work out both. Circumference first: 2 times 22 over 7 times 7.",
      W("l1", "2 × 22/7 × 7"), strike("l1", "/7"), strike("l1", "× 7")),
    B("The 7s cancel, leaving 2 times 22. The circumference is 44.", W("l2", "2 × 22 = 44"),
      note("l2", "44", "circumference", "below")),
    B("Now the area. Which sum do we need?",
      ask=choose(["22/7 × 7 × 7", "2 × 22/7 × 7", "22/7 × 7"], 0,
                 "Area is pi times the radius times the radius. The radius goes in twice, and there is no 2.")),
    B("22 over 7, times 7, times 7. One 7 cancels, leaving 22 times 7, which is 154.",
      W("l3", "22/7 × 7 × 7 = 154"), note("l3", "154", "area", "below")),
    B("Compare the two numbers. 154 is greater than 44.", W("l4", "154 > 44")),
    B("So the area is the larger number: 154 is greater than 44.",
      A("a", "Area: 154 > 44", label=True), ring("a", "Area")),
    B("One is in centimetres and the other in square centimetres, so we only compare the numbers, just as the question says."),
])

LESSONS["Q_CH21_019"] = lesson([
    B("How many radii and how many diameters can a circle have?",
      G("How many radii and diameters can a circle have?"), F("Q_CH21_019", 0)),
    B("A radius joins the centre to a point on the circle. We usually draw just one. But could we draw another, to a different point?",
      ask=choose(["Yes, to any point", "No, only one"], 0,
                 "Pick any point on the circle and join it to the centre. That is a radius too. Every point gives one.")),
    B("Yes! Every point on the circle gives a radius. And between any two points there are always more points. There is no end to them.",
      L("l1", "radii: no end to them")),
    B("Now diameters. A diameter is a straight line through the centre. Turn it a tiny bit, and you have a new diameter.",
      F("Q_CH21_019", 1)),
    B("You can keep turning it by smaller and smaller amounts, for ever. So there is no end to the diameters either.",
      L("l2", "diameters: no end to them")),
    B("The word for no end is infinite. A circle has infinite radii and infinite diameters.",
      A("a", "Infinite radii, infinite diameters", label=True), ring("a", "Infinite radii")),
    B("We draw one radius or one diameter to keep pictures tidy. But the circle really has endlessly many of each."),
])

LESSONS["Q_CH21_020"] = lesson([
    B("Find the perimeter of a semicircle with diameter 14 centimetres. Use 22 over 7 for pi.",
      G("Semicircle: diameter 14 cm. Perimeter = ? (π = 22/7)"), F("Q_CH21_020")),
    B("A semicircle is half a circle, like half a roti. Walk all the way round its edge. What kinds of edge do you walk along?",
      ask=choose(["a curved edge only", "a curved edge and a straight edge"], 1,
                 "Half a roti has a round side and a flat side where it was cut. The perimeter goes along both.")),
    B("A curved edge and a straight edge. That's the trap in this question: people forget the straight edge.",
      L("l1", "Perimeter = curved edge + straight edge")),
    B("The curved edge is half of the whole circle's circumference. The whole circle: 22 over 7 times 14. 14 divided by 7 is 2, and 22 times 2 is 44.",
      W("l2", "22/7 × 14 = 44"), F("Q_CH21_020", 0)),
    B("Half of 44 is 22. So the curved edge is 22 centimetres.", W("l3", "44 ÷ 2 = 22"), F("Q_CH21_020", 1)),
    B("The straight edge is the diameter itself: 14 centimetres.", note("l1", "straight edge", "14 cm", "below"),
      F("Q_CH21_020", 2)),
    B("Add the two edges. 22 plus 14 is 36.", W("l4", "22 + 14 = 36"), F("Q_CH21_020", 3)),
    B("The perimeter of the semicircle is 36 centimetres.", A("a", "Perimeter = 36 cm", label=True), ring("a", "36")),
    B("Perimeter means all the way round. For a semicircle that is the curve and the flat side together."),
])
