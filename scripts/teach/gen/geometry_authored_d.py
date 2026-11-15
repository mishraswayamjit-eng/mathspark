"""Geometry lessons written for one question each: the 2018 paper."""
from geometry_lib import (B, FIG, LV, W, both, choose, lesson, mark, strike)

LESSONS = {}


# 1 gram of seed per square metre; field 110 m by 70 m. How much seed?
LESSONS["EXT_G5_FP_2018_001"] = lesson([
    B("A field is 110 metres long and 70 metres wide. Every square metre of it needs 1 gram of grass seed. How much seed is that altogether?",
      W("l1", "Field: 110 m long, 70 m wide", tone="given", label=True),
      W("l2", "1 g of seed for each sq. m. Seed = ? kg", tone="given", label=True),
      FIG("f1", kind="rectangle", length="110 m", breadth="70 m", proportion=1.6)),
    B("The seed covers the ground inside the field, 1 gram on each square metre. So what do we need to find first?",
      ask=choose(["the perimeter: 2 × (110 + 70)", "the area: 110 × 70", "the sum: 110 + 70"], 1,
                 "Seed is spread over the ground inside the field, not along its fence. The ground inside is the area: length times breadth.")),
    B("We need the area. For 110 times 70, do 11 times 7 first, which is 77. Then the two zeros come along: 7700.",
      W("l3", "Area = length × breadth", label=True), W("l4", "11 × 7 = 77"), W("l5", "110 × 70 = 7700")),
    B("The field is 7700 square metres. At 1 gram for each square metre, that is 7700 grams of seed.",
      W("l6", "Seed = 7700 g", label=True),
      FIG("f2", kind="rectangle", length="110 m", breadth="70 m", proportion=1.6, inside="7700 sq. m", highlight=["fill"])),
    B("But the choices are in kilograms. How do we change grams into kilograms?",
      ask=choose(["multiply by 1000", "divide by 100", "divide by 1000"], 2,
                 "1000 grams make 1 kilogram. A kilogram is much bigger than a gram, so there will be fewer of them: we divide by 1000.")),
    B("1000 grams make 1 kilogram, so we divide by 1000. Every digit moves 3 places to the right, and 7700 becomes 7.7.",
      W("l7", "1000 g = 1 kg", label=True), W("l8", "7700 ÷ 1000 = 7.7")),
    B("So the field needs 7.7 kilograms of grass seed.",
      W("l9", "Seed needed = 7.7 kg", tone="answer", label=True), mark("l9", "7.7 kg", "circle")),
    B("Check by going back: 7.7 times 1000 is 7700 grams, 1 for each square metre.",
      W("l10", "7.7 × 1000 = 7700")),
    B("So: the area tells us how many square metres, and that tells us how many grams. The last step, changing the unit, is where the slips happen."),
], "authored")


# Which statement about complements and supplements is true?
LESSONS["EXT_G5_FP_2018_007"] = lesson([
    B("We have 3 statements about complementary and supplementary angles, and each one says always. A good way to test an always is to try it on a real angle. Let's pick 30 degrees.",
      W("l1", "Which statement is true?", tone="given", label=True), W("l2", "Test angle: 30°", label=True),
      FIG("f1", kind="angles", layout="single", parts=[{"label": "30°", "size": 30}])),
    B("The complement fits with our angle in a right angle, 90 degrees. The supplement fits with it on a straight line, 180 degrees.",
      W("l3", "complement = 90° − angle", label=True), W("l4", "supplement = 180° − angle", label=True)),
    B("So the complement of 30 is 90 take away 30, which is 60. And the supplement is 180 take away 30, which is 150.",
      W("l5", "90 − 30 = 60"), W("l6", "180 − 30 = 150"),
      FIG("f2", kind="angles", layout="onLine", parts=[{"label": "30°", "size": 30}, {"label": "150°", "size": 150}])),
    B("The first statement says the supplement is always less than 90 degrees. Our supplement is 150. What does that tell us?",
      W("l7", "A: supplement is always less than 90°", label=True),
      ask=choose(["A is true", "A is not always true"], 1,
                 "150 is bigger than 90. One example that breaks an always is enough: the first statement is not true.")),
    B("150 is more than 90, so the first statement is out. One example that breaks an always is enough.",
      W("l8", "150 > 90"), strike("l7", "always less than 90°", "150° is not")),
    B("The second statement says the complement of an acute angle is always acute. Acute means less than 90. Our 30 is acute, and its complement, 60, is acute too.",
      W("l9", "B: complement of an acute angle is acute", label=True), W("l10", "60 < 90"),
      FIG("f3", kind="angles", layout="inRightAngle", parts=[{"label": "30°", "size": 30}, {"label": "60°", "size": 60}])),
    B("But is it always so? Look at the drawing: the two angles share one square corner of 90 degrees. A piece of the corner is always smaller than the whole corner, so the complement is always less than 90.",
      mark("l9", "acute", "underline", nth=2)),
    B("The third statement says the complement and the supplement always add up to 360. Ours are 60 and 150, and 60 plus 150 is 210. So that one is out as well.",
      W("l11", "C: complement + supplement = 360°", label=True), W("l11b", "60 + 150 = 210"),
      strike("l11", "360°", "210° is not")),
    B("Only the second statement survives: the complementary angle of an acute angle is always an acute angle.",
      W("l12", "True: complement of an acute angle is acute", tone="answer", label=True), mark("l12", "True", "circle")),
    B("So when a statement says always, try it on a real angle. One example that breaks it is enough to throw it out. For the one that is left, look for the reason it must be true."),
], "authored")


# Perimeter of a rectangle is 72 cm. Which pair is its length and breadth?
LESSONS["EXT_G5_FP_2018_009"] = lesson([
    B("The perimeter of a rectangle is 72 centimetres. We have to pick the pair of numbers that could be its length and breadth.",
      W("l1", "Rectangle: perimeter 72 cm", tone="given", label=True),
      W("l2", "Length and breadth = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", length="?", breadth="?", note="Perimeter = 72 cm")),
    B("The perimeter is the walk all the way round: 2 lengths and 2 breadths. So what must just one length and one breadth add up to?",
      ask=choose(["72", "72 ÷ 2", "72 ÷ 4"], 1,
                 "One length and one breadth take us exactly halfway round. So together they make half of 72.")),
    B("Halfway round is half of 72, which is 36. So we are looking for a pair that adds up to 36.",
      W("l3", "72 ÷ 2 = 36"), W("l4", "length + breadth = 36", label=True), mark("l4", "36", "box")),
    B("Let's test each pair. 9 plus 4 is 13. And 14 plus 4 is 18. Neither of them is 36.",
      W("l5", "9 + 4 = 13"), W("l6", "14 + 4 = 18")),
    B("Next pair: 19 plus 15 is 34. Close, but not 36.",
      W("l7", "19 + 15 = 34")),
    B("Last pair: 21 plus 15 is 36. That is the one.",
      W("l8", "21 + 15 = 36"), mark("l8", "36", "circle")),
    B("So the length is 21 centimetres and the breadth is 15 centimetres.",
      W("l9", "Length 21 cm, breadth 15 cm", tone="answer", label=True), mark("l9", "Length 21 cm, breadth 15 cm", "circle"),
      FIG("f2", kind="rectangle", length="21 cm", breadth="15 cm", highlight=["border"], note="Perimeter = 72 cm")),
    B("Check the whole walk: 2 times 36 is 72. It fits.",
      W("l10", "2 × (21 + 15) = 72")),
    B("The trap is to look for a pair that adds up to 72. Each side is walked twice, so the pair only has to make half of the perimeter."),
], "authored")


# Two sides of a square are (3a − 7) cm and (2a − 1) cm. Perimeter?
LESSONS["EXT_G5_FP_2018_018"] = lesson([
    B("Two sides of a square are written with the letter a: 3 a minus 7, and 2 a minus 1. We want to know what its perimeter can be.",
      W("l1", "Square: sides (3a − 7) cm and (2a − 1) cm", tone="given", label=True),
      W("l2", "Perimeter = ?", tone="given", label=True),
      FIG("f1", kind="rectangle", square=True, length="(3a − 7) cm", breadth="(2a − 1) cm")),
    B("The two sides look different. But this is a square. So what must be true about them?",
      ask=choose(["they are equal", "one is double the other", "they add up to 90"], 0,
                 "Every side of a square has the same length. So although they are written differently, these two sides are equal.")),
    B("All sides of a square are equal, so we can write an equation: 3 a minus 7 equals 2 a minus 1.",
      LV("l3", "3a − 7 = 2a − 1", {"a": 6})),
    B("Let's clear the minus 7 first, by adding 7 to both sides. On the right, minus 1 plus 7 makes plus 6.",
      strike("l3", "− 7", "+ 7"), both("l3", "+ 7"), LV("l4", "3a = 2a + 6", {"a": 6})),
    B("Now take 2 a away from both sides. 3 a take away 2 a leaves 1 a. So a equals 6.",
      strike("l4", "2a", "− 2a"), both("l4", "− 2a"), LV("l5", "a = 6", {"a": 6})),
    B("We know a is 6. What do we do with it next?",
      ask=choose(["multiply it by 4", "put it into 3a − 7 for the side", "nothing: the answer is 6"], 1,
                 "a is not the side. The side is 3 a minus 7, so we put 6 in place of a to find it.")),
    B("Put 6 in place of a. 3 times 6, minus 7, is 11. Check with the other side: 2 times 6, minus 1, is 11 too. So the side is 11 centimetres.",
      W("l6", "3 × 6 − 7 = 11"), W("l7", "2 × 6 − 1 = 11"),
      FIG("f2", kind="rectangle", square=True, length="11 cm", breadth="11 cm")),
    B("The perimeter is the walk round all 4 equal sides. 4 times 11 is 44.",
      W("l8", "Perimeter of square = 4 × side", label=True), W("l9", "4 × 11 = 44")),
    B("So the perimeter is 44 centimetres.",
      W("l10", "Perimeter = 44 cm", tone="answer", label=True), mark("l10", "44 cm", "circle"),
      FIG("f3", kind="rectangle", square=True, length="11 cm", breadth="11 cm", highlight=["border"], note="Perimeter = 44 cm")),
    B("So: equal sides give an equation, the equation gives a, a gives the side, and 4 sides give the perimeter. Do not stop at a."),
], "authored")


# Equilateral triangle with perimeter (16a + 7b); a = 2, b = 4. Side?
LESSONS["EXT_G5_FP_2018_029"] = lesson([
    B("The perimeter of an equilateral triangle is written with letters: 16 a plus 7 b. We are told a is 2 and b is 4, and we want one side.",
      W("l1", "Equilateral triangle: perimeter (16a + 7b)", tone="given", label=True),
      W("l2", "a = 2, b = 4. Side = ?", tone="given", label=True),
      FIG("f1", kind="triangle", shape="equilateral", sides={"ab": "?", "bc": "?", "ca": "?"}, note="Perimeter = 16a + 7b")),
    B("First we turn the perimeter into a real number. What does 16 a mean when a is 2?",
      ask=choose(["16 + 2", "162", "16 × 2"], 2,
                 "A number written right next to a letter means times. So 16 a is 16 times 2.")),
    B("16 a is 16 times 2, which is 32. And 7 b is 7 times 4, which is 28.",
      W("l3", "16 × 2 = 32"), W("l4", "7 × 4 = 28")),
    B("Add the two pieces. 32 plus 28 is 60. So the perimeter, the walk all the way round, is 60.",
      W("l5", "32 + 28 = 60"),
      FIG("f2", kind="triangle", shape="equilateral", sides={"ab": "?", "bc": "?", "ca": "?"}, note="Perimeter = 60")),
    B("Now, the triangle is equilateral. So how do we get one side from 60?",
      ask=choose(["60 ÷ 2", "60 ÷ 3", "60 ÷ 4"], 1,
                 "Equilateral means all 3 sides of the triangle are equal. So the 60 is shared into 3 equal parts.")),
    B("3 equal sides share the 60. 60 divided by 3 is 20. So each side is 20.",
      W("l6", "60 ÷ 3 = 20"), W("l7", "Side = 20", tone="answer", label=True), mark("l7", "20", "circle"),
      FIG("f3", kind="triangle", shape="equilateral", sides={"ab": "20", "bc": "20", "ca": "20"}, highlight=["ab", "bc", "ca"])),
    B("Check the walk: 20 plus 20 plus 20 makes 60. It fits.",
      W("l8", "20 + 20 + 20 = 60")),
    B("So: put the numbers in place of the letters to get the perimeter, then share it among the 3 equal sides."),
], "authored")
