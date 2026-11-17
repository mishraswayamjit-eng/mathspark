"""Integers: journeys up and down a number line (floors, temperature, a well, mountains, divers)."""
from imported_09_lib import ANS, B, FIG, GIVEN, M, N, W, Walk, choose, circle_last, lesson

LESSONS = {}


def line(lo, hi, points, step=1):
    return {"kind": "numberLine", "min": lo, "max": hi, "step": step,
            "points": [{"at": at, "label": label} for at, label in points]}


# ── Neha's treasure hunt: floor 3, down 5, up 2 ──────────────────────────────
w = Walk(3)
LESSONS["2069901c"] = lesson(
    B("Neha starts on floor 3. She rides the lift down 5 floors, then climbs up 2. Let's follow her on a number line that stands up tall, with the ground floor at 0.",
      GIVEN("g", "Start at floor 3: down 5, then up 2"),
      FIG("f", line(-4, 6, [(3, "start"), (0, "ground")]))),
    B("Going down 5 floors from floor 3. Which sum is that?",
      ask=choose(["3 − 5", "3 + 5", "5 − 3"], 0,
                 "Down means the floor number gets smaller, so we subtract. And she begins at 3, so the 3 comes first: 3 minus 5.")),
    w.mv(-5, "Down 5 from floor 3.", before=[M("g", "down 5")]),
    B("Floor minus 2 is 2 floors under the ground, like a basement. Now she climbs up 2 floors. Where does she land?",
      M("g", "up 2"),
      ask=choose(["floor 0", "floor −4", "floor 4"], 0,
                 "Climbing up means adding. She is 2 floors below the ground and she climbs exactly 2, so she comes back level with the ground.")),
    w.mv(2, "Up means add.", tail="Neha finds the treasure on floor 0, the ground floor.",
         after=[ANS("a", "Treasure: floor 0", True), M("a", "floor 0", "circle")]),
    B("Check it another way. She went down 5 and up 2, so overall she is 3 floors lower than where she began. And 3 floors below floor 3 is floor 0.",
      W("c1", "5 − 2 = 3"), W("c2", "3 − 3 = 0")),
    B("The slip to watch for is adding everything together, 3 and 5 and 2, to get floor 10. Down and up pull in opposite directions, so they cannot simply be added."),
    B("So here is the plan: start where the story starts, subtract for down, add for up, and take one move at a time."),
)

# ── Shimla temperature: −3, up 8, down 11 ────────────────────────────────────
w = Walk(-3)
LESSONS["6f42c2e1"] = lesson(
    B("At 6 in the morning it is minus 3 degrees in Shimla. By noon the temperature rises by 8 degrees, and by midnight it drops by 11. A thermometer is just a number line standing up.",
      GIVEN("g", "Start −3°C: rises 8, then drops 11")),
    B("The temperature rises by 8 from minus 3. Which sum finds the noon temperature?",
      ask=choose(["−3 + 8", "−3 − 8", "3 + 8"], 0,
                 "Rising means getting warmer, so we add 8. And the morning is below zero, so the 3 keeps its minus sign.")),
    w.mv(8, "So we add 8.", before=[M("g", "rises 8")]),
    w.mv(-11, "Noon is 5 degrees. Now it drops by 11, so we subtract.", before=[M("g", "drops 11")]),
    B("So at midnight it is minus 6 degrees. Brrr, that is even colder than the morning.",
      ANS("a", "Midnight: −6°C", True), M("a", "−6°C", "circle")),
    B("Does that make sense? Up 8 and down 11 is 3 degrees down overall. And 3 degrees below minus 3 is minus 6. Yes.",
      W("c1", "11 − 8 = 3"), W("c2", "−3 − 3 = −6")),
    B("The slip to avoid is dropping the minus sign at the very start. Begin at 3 instead of minus 3, and every line after it slides."),
    B("So: rising is plus, dropping is minus, and you take the changes one at a time."),
)

# ── The well: dig 6, fill 2, dig 5, fill 3, dig 4 ────────────────────────────
w = Walk(0)
LESSONS["e48c0de7"] = lesson(
    B("A well is being dug. Ground level is 0, digging goes down, and filling comes back up. Day by day: dig 6, fill 2, dig 5, fill 3, dig 4.",
      GIVEN("g", "Start 0: dig 6, fill 2, dig 5, fill 3, dig 4")),
    B("Digging takes the bottom of the well below the ground. So is digging 6 metres a plus 6 or a minus 6?",
      ask=choose(["− 6", "+ 6"], 0,
                 "Below ground level the numbers are negative. Digging goes down, so each dig is a subtraction, and each fill is an addition.")),
    w.mv(-6, "Day 1, dig 6.", before=[M("g", "dig 6")]),
    w.mv(2, "Day 2, 2 metres of sand go back in, so we add.", before=[M("g", "fill 2")]),
    w.mv(-5, "Day 3, dig 5 more.", before=[M("g", "dig 5")]),
    B("Day 4, rain fills the well up by 3 metres. The bottom is at minus 9. Where is it now?",
      M("g", "fill 3"),
      ask=choose(["−6", "−12", "6"], 0,
                 "Filling up brings the bottom closer to ground level. So we add 3 to minus 9, and move 3 steps towards 0.")),
    w.mv(3, "Filling means adding.", why=False),
    w.mv(-4, "Day 5, dig 4 deeper.", why=False, tail="That is the final depth.",
         before=[M("g", "dig 4")], after=[ANS("a", "Final depth = −10 metres", True), M("a", "−10", "circle")]),
    B("Check with totals. They dug 6, 5 and 4, which is 15 metres down. They filled 2 and 3, which is 5 back up. 5 up and 15 down leaves 10 down.",
      W("c1", "6 + 5 + 4 = 15"), W("c2", "2 + 3 = 5"), W("c3", "5 − 15 = −10")),
    B("Careful not to add all five numbers together, as if nothing was ever filled back in. Down is minus, up is plus, one day at a time."),
)

# ── Deepa's mountain, and Arjun 10 metres higher ─────────────────────────────
w = Walk(0)
LESSONS["e69906c3"] = lesson(
    B("Deepa starts at sea level, 0. She climbs 12, slides down 19, climbs 8 and slides down 5. Arjun finishes 10 metres higher than Deepa, so we need Deepa first.",
      GIVEN("g", "Deepa: start 0, up 12, down 19, up 8, down 5"), GIVEN("g2", "Arjun: 10 metres higher than Deepa")),
    w.mv(12, "Up 12 from 0 is easy."),
    B("Now she slides down 19 from 12. Will she still be above sea level?",
      M("g", "down 19"),
      ask=choose(["Yes, at 7", "No, at −7", "No, at −31"], 1,
                 "She is only 12 metres up, and she slides 19. 12 of those bring her to sea level, and there are still 7 more to go down.")),
    w.mv(-19, "So we subtract 19."),
    w.mv(8, "Then up 8."),
    w.mv(-5, "And down 5.", tail="So Deepa ends 4 metres below sea level."),
    B("Arjun is 10 metres higher than Deepa's minus 4. Which sum gives his position?",
      M("g2", "10 metres higher"),
      ask=choose(["−4 + 10", "−4 − 10", "4 + 10"], 0,
                 "Higher means further up the number line, so we add 10. And Deepa is below sea level, so her 4 keeps its minus sign.")),
    B("Minus 4 plus 10 is 6. 4 of those steps bring him up to sea level, and then 6 more above it. Arjun is 6 metres above sea level.",
      ANS("a", "−4 + 10 = 6"), M("a", "6", "circle")),
    B("Check Deepa with totals. Up 12 and 8 is 20. Down 19 and 5 is 24. 20 up and 24 down leaves her 4 below. It matches.",
      W("c1", "12 + 8 = 20"), W("c2", "19 + 5 = 24"), W("c3", "20 − 24 = −4")),
    B("The trap is stopping at Deepa's minus 4. Always read the last line of the question again: it asked for Arjun."),
    B("One move at a time: up is plus, down is minus. Then do whatever the question asks at the end."),
)

# ── Sameer: −8, up 12, down 5, up twice the slide ────────────────────────────
w = Walk(-8)
LESSONS["feedb55a"] = lesson(
    B("Sameer starts at minus 8. Round 1, he climbs 12. Round 2, he slides down 5. Round 3, he climbs twice the distance he slid in Round 2.",
      GIVEN("g", "Start −8: up 12, down 5, up twice the slide")),
    w.mv(12, "Round 1, up 12.", before=[M("g", "up 12")]),
    w.mv(-5, "Round 2, down 5.", before=[M("g", "down 5")]),
    B("Round 3: he climbs twice the distance he slid down in Round 2. How far is that climb?",
      M("g", "up twice the slide"),
      ask=choose(["10 metres", "2 metres", "5 metres"], 0,
                 "Look back at Round 2. The slide was 5 metres, and twice 5 is 10. It is the slide we double, not the place where he is standing.")),
    B("Twice 5 is 10, so in Round 3 he climbs 10 metres.",
      W("t", "2 × 5 = 10"), N("g", "up twice the slide", "up 10")),
    w.mv(10, "Up 10 from minus 1.", why=False, tail="Sameer finishes at plus 9.",
         after=[ANS("a", "Final position = +9", True), M("a", "+9", "circle")]),
    B("Check with totals. Up 12, up 10 and down 5 is 17 up overall. And minus 8 plus 17 is 9. It matches.",
      W("c1", "12 + 10 − 5 = 17"), W("c2", "−8 + 17 = 9")),
    B("The trap here was the word twice. It doubles the slide of 5, not Sameer's position."),
    B("So: keep track of the position after every round, and read carefully what each round's move depends on."),
)

# ── Ravi's submarine, and Sita halfway to −6 ─────────────────────────────────
w = Walk(-12)
LESSONS["00674043"] = lesson(
    B("Ravi's submarine starts at minus 12, then rises 5, dives 8 and rises 19. Sita is exactly halfway between where he ends up and minus 6. So first we must find Ravi.",
      GIVEN("g", "Ravi: start −12, up 5, down 8, up 19"), GIVEN("g2", "Sita: halfway between Ravi and −6")),
    B("Rising means going up the number line. So for the first move, rising 5 metres, which sum do we write?",
      ask=choose(["−12 + 5", "−12 − 5", "12 + 5"], 0,
                 "Rising takes us up, towards 0, so we add. And we start below the surface, so the 12 keeps its minus sign.")),
    w.mv(5, before=[M("g", "up 5")]),
    w.mv(-8, "Then he dives 8, so we subtract.", before=[M("g", "down 8")]),
    w.mv(19, "Now he rises 19.", before=[M("g", "up 19")]),
    B("So Ravi is at 4, above the surface. Sita is halfway between 4 and minus 6. First, how far apart are 4 and minus 6?",
      ask=choose(["10 metres", "2 metres", "6 metres"], 0,
                 "From minus 6 up to 0 is 6 steps, and from 0 up to 4 is 4 more. They are on opposite sides of 0, so we add the two.")),
    B("They sit on opposite sides of 0, so the gap is 6 plus 4, which is 10. Halfway is half of 10, so 5 steps from either end.",
      W("h1", "6 + 4 = 10"), W("h2", "10 ÷ 2 = 5"),
      FIG("f", line(-6, 4, [(-6, "−6"), (4, "Ravi")]))),
    B("5 steps down from Ravi's 4 takes us to minus 1. So Sita is at minus 1, which is 1 metre below the surface.",
      ANS("a", "4 − 5 = −1"), M("a", "−1", "circle")),
    B("Check from the other end. 5 steps up from minus 6 is also minus 1. Both ends agree, so minus 1 really is the middle.",
      W("c", "−6 + 5 = −1")),
    B("So: follow the moves one at a time, adding for up and subtracting for down. And for halfway, find the gap, then travel half of it."),
)

# ── The sunflower: root tip −8, stem tip +14 ─────────────────────────────────
LESSONS["687b6c4c"] = lesson(
    B("Neha's sunflower. The soil is 0. The root tip is at minus 8 centimetres, below the soil, and the stem tip is at plus 14, above it. How long is the whole plant?",
      GIVEN("g", "Root tip −8 cm, stem tip +14 cm"),
      FIG("f", line(-8, 14, [(-8, "root tip"), (0, "soil"), (14, "stem tip")], 2))),
    B("Look at the picture. Is the whole plant longer or shorter than 14 centimetres?",
      ask=choose(["longer than 14 cm", "shorter than 14 cm", "exactly 14 cm"], 0,
                 "14 centimetres is only the part above the soil. The root carries on below the soil, so the whole plant must be longer than that.")),
    B("Split the plant at the soil. Below the soil, from minus 8 up to 0, there are 8 centimetres of root.",
      M("g", "−8 cm"), W("p1", "Below the soil: 8 cm", label=True)),
    B("Above the soil, from 0 up to 14, there are 14 centimetres of stem.",
      M("g", "+14 cm"), W("p2", "Above the soil: 14 cm", label=True)),
    B("So how do we get the whole length?",
      ask=choose(["8 + 14", "14 − 8", "just 14"], 0,
                 "The root and the stem are two separate pieces, one below the soil and one above. To get the whole plant we join them, so we add.")),
    B("8 plus 14 is 22. The plant is 22 centimetres long, from root tip to stem tip.",
      ANS("a", "8 + 14 = 22"), M("a", "22", "circle")),
    B("As a subtraction it looks like this: 14 minus minus 8. Taking away a negative is the same as adding, so again we get 22.",
      W("c", "14 − (−8) = 22"), N("c", "− (−8)", "same as + 8")),
    B("The slip to avoid is 14 minus 8, which gives 6. That would only be right if both tips were above the soil."),
    B("When two points are on opposite sides of 0, the distance between them is their two distances from 0, added together."),
)

# ── The diver: platform +5, dive to −8, up 3 ─────────────────────────────────
w = Walk(-8)
LESSONS["82d013e7"] = lesson(
    B("Vikram stands on a platform 5 metres above the water. He dives to 8 metres below the surface, then swims up 3. We want the height difference between where he started and where he finished.",
      GIVEN("g", "Platform +5. Dives to −8, then swims up 3")),
    B("After the dive he is at minus 8. Then he swims up 3 metres. Where is he now?",
      M("g", "swims up 3"),
      ask=choose(["−5", "−11", "5"], 0,
                 "Swimming up brings him closer to the surface, so we add 3. From minus 8, 3 steps towards 0 is minus 5.")),
    w.mv(3, "Up means add."),
    B("So he starts at plus 5 and ends at minus 5. One is above the water and the other is below it.",
      FIG("f", line(-8, 5, [(5, "start"), (0, "water"), (-5, "end")]))),
    B("How do we find the gap between plus 5 and minus 5?",
      ask=choose(["5 + 5", "5 − 5", "8 + 3"], 0,
                 "They are on opposite sides of the water. From the platform down to the surface is 5 metres, and from the surface down to him is 5 more. We add.")),
    B("5 metres down to the water, and 5 more below it. 5 plus 5 is 10 metres.",
      W("d", "5 + 5 = 10"), ANS("a", "5 − (−5) = 10"), M("a", "10", "circle")),
    B("The tempting slip is 5 take away 5, which gives 0. But he is clearly not back on the platform! Opposite sides of 0 means we add the two distances."),
    B("So: write both positions as numbers. Then, if they are on opposite sides of 0, add their distances from 0."),
)
