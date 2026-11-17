"""Integers: journeys where a move depends on the position (twice, opposite, halfway, a rule)."""
from imported_09_lib import ANS, B, FIG, GIVEN, M, N, W, Walk, choose, lesson

LESSONS = {}


def line(lo, hi, points, step=1):
    return {"kind": "numberLine", "min": lo, "max": hi, "step": step,
            "points": [{"at": at, "label": label} for at, label in points]}


# ── The Magic Elevator: two instructions depend on the distance from 0 ───────
w = Walk(0)
LESSONS["46b47e21"] = lesson(
    B("The lift starts at floor 0 and gets six instructions. Two of them are sneaky: they depend on where the lift is at that moment. So we go one instruction at a time.",
      GIVEN("g1", "Start 0: down 6, up 3, down (2 × distance from 0)"),
      GIVEN("g2", "then up 4, down 5, up (distance from 0)")),
    w.mv(-6, "Down 6 from floor 0."),
    w.mv(3, "Up 3."),
    B("Next: go down twice as many floors as our distance from 0. We are at minus 3. What is our distance from 0?",
      M("g1", "2 × distance from 0"),
      ask=choose(["3 floors", "−3 floors", "6 floors"], 0,
                 "Distance is how many steps away we are, and a count of steps is never negative. From minus 3 to 0 is 3 steps.")),
    B("The distance is 3, and twice 3 is 6. So this instruction really says: go down 6.",
      W("t", "2 × 3 = 6"), N("g1", "2 × distance from 0", "down 6")),
    w.mv(-6, "Down 6 from minus 3."),
    w.mv(4, "Up 4.", why=False),
    w.mv(-5, "Down 5.", why=False),
    B("Last one: go up by the absolute value of the position. That is just a grand name for its distance from 0. We are at minus 10. Where will the lift finish?",
      M("g2", "up (distance from 0)"),
      ask=choose(["floor 0", "floor −20", "floor 10"], 0,
                 "At minus 10 we are 10 steps from 0. Going up exactly that many steps brings us right back to 0.")),
    w.mv(10, "The distance is 10, so up 10.", tail="The lift ends on floor 0.",
         after=[ANS("a", "Final floor = 0", True), M("a", "0", "circle")]),
    B("Here is something neat. When you are below 0, going up by your distance from 0 always lands exactly on 0. So that last instruction settles it."),
    B("When an instruction depends on where you are, stop, find where you are, then move. And a distance from 0 is always a plain positive number."),
)

# ── The rule game: negative → down 3, zero or positive → up 7 ────────────────
w = Walk(-5)
LESSONS["6295477d"] = lesson(
    B("The submarine starts at minus 5. Each round it follows a rule: if the depth is negative, go down 3. If it is 0 or positive, go up 7. There are 5 rounds.",
      GIVEN("g", "Start −5. Negative: down 3. Zero or positive: up 7"), GIVEN("g2", "5 rounds")),
    B("Round 1. We are at minus 5. Which part of the rule do we use?",
      ask=choose(["down 3", "up 7"], 0,
                 "Minus 5 is a negative number, below sea level. The rule for a negative depth is to go down 3.")),
    w.mv(-3, "Minus 5 is negative, so down 3.", before=[M("g", "Negative: down 3")]),
    w.mv(-3, "Before Round 2 we test the rule again. Minus 8 is still negative, so down 3 again.", why=False),
    B("Think ahead. Will the submarine ever get to use the up 7 part of the rule?",
      ask=choose(["No, it keeps getting more negative", "Yes, in Round 3", "Yes, in the last round"], 0,
                 "Each round it is negative, so it goes down, and that makes it even more negative. It can never climb back to 0, so up 7 never happens.")),
    w.mv(-3, "Round 3. Still negative, so down 3.", why=False),
    w.mv(-3, "Round 4.", why=False),
    w.mv(-3, "Round 5.", why=False, tail="That was the last round.",
         after=[ANS("a", "After 5 rounds: −20 metres", True), M("a", "−20", "circle")]),
    B("A quick check. 5 rounds of going down 3 is 15 metres down altogether. And minus 5 minus 15 is minus 20.",
      W("c1", "5 × 3 = 15"), W("c2", "−5 − 15 = −20")),
    B("With a rule like this, test where you are before every single move. Here the answer to the test never changed, so it was down 3 every time."),
)

# ── Submarine: dive to 3 times the depth, then rise to −6 ────────────────────
w = Walk(0)
_sub = [
    w.mv(-18, "Dive 18."),
    w.mv(7, "Rise 7."),
    w.mv(-12, "Dive 12."),
    w.mv(5, "Rise 5.", why=False),
]
LESSONS["680cc8a1"] = lesson(
    B("The submarine starts at 0 and gets five commands: dive 18, rise 7, dive 12, rise 5, then dive to 3 times its depth. After that it must rise to 6 metres below sea level. How far is that rise?",
      GIVEN("g", "Start 0: dive 18, rise 7, dive 12, rise 5"), GIVEN("g2", "then dive to 3 × the depth; rise to −6")),
    _sub,
    B("We are at minus 18, so the depth is 18 metres. The last command says dive to 3 times this depth. Where is that?",
      M("g2", "3 × the depth"),
      ask=choose(["−54", "−21", "54"], 0,
                 "3 times 18 metres deep is 54 metres deep. And deep means below sea level, so the position is minus 54.")),
    B("3 times 18 is 54. So the submarine is now 54 metres down, at minus 54.",
      W("t", "3 × 18 = 54"), W("p", "Position = −54", label=True)),
    B("Now it must rise to minus 6. How do we find how far it rises?",
      M("g2", "rise to −6"),
      ask=choose(["54 − 6", "54 + 6", "6 − 54"], 0,
                 "Both places are below sea level, on the same side of 0. One is 54 down and the other is 6 down, so the gap between them is 54 take away 6.")),
    B("54 minus 6 is 48. The submarine must rise 48 metres.",
      ANS("a", "54 − 6 = 48"), M("a", "48", "circle")),
    B("Check: start at minus 54 and rise 48. Minus 54 plus 48 is minus 6. Exactly where the captain wanted to be.",
      W("c", "−54 + 48 = −6")),
    B("The trap is adding the 6, as if the submarine went all the way up past the surface. It stops 6 metres short of the surface."),
    B("So: track the position, turn the tricky command into a plain number, and for a gap on the same side of 0, subtract."),
)

# ── Desert Explorer: left, twice, right, opposite, left ──────────────────────
w = Walk(0, horizontal=True)
_r1 = w.mv(-7, "Round 1, 7 steps left.")
w.pos = -14
_r3 = w.mv(5, "Round 3, 5 steps right.")
w.pos = 9
_r5 = w.mv(-3, "Round 5, 3 steps left.")
LESSONS["b1cba709"] = lesson(
    B("Vikram starts at 0. He moves 7 left, then goes to twice his position, then 5 right, then to the opposite of his position, then 3 left. Left is the minus direction, right is plus.",
      GIVEN("g", "Start 0: 7 left, twice, 5 right, opposite, 3 left")),
    _r1,
    B("Round 2: go to twice the current position. We are at minus 7. What is twice minus 7?",
      M("g", "twice"),
      ask=choose(["−14", "14", "−5"], 0,
                 "Twice minus 7 is minus 7 and another minus 7. Two lots of 7 steps to the left of 0 make 14 steps to the left: minus 14.")),
    B("2 times minus 7 is minus 14. Doubling a negative number sends it further from 0, on the same side.",
      W("t", "2 × (−7) = −14"), M("t", "−14")),
    _r3,
    B("Round 4: go to the opposite of the current position. What is the opposite of minus 9?",
      M("g", "opposite"),
      ask=choose(["9", "−9", "0"], 0,
                 "The opposite of a number is the same distance from 0, on the other side. Minus 9 is 9 steps left of 0, so its opposite is 9 steps right of 0.")),
    B("The opposite of minus 9 is 9. Same distance from 0, other side.",
      W("o", "−(−9) = 9"), M("o", "9", "underline", 2)),
    _r5,
    B("Position 6 is between 1 and 10, so Vikram wins the cricket bat.",
      ANS("a", "Position 6: cricket bat", True), M("a", "6", "circle")),
    B("Let's run back over the positions: minus 7, minus 14, minus 9, then 9, then 6. Each one follows from the one before."),
    B("Two words did the tricky work here. Twice keeps you on the same side of 0, only further out. Opposite flips you over to the other side."),
)

# ── Desert rounds: Sandstorm left, Oasis right, then back to 0 ───────────────
w = Walk(0, horizontal=True)
LESSONS["29a8cab7"] = lesson(
    B("Vikram starts at 0. Sandstorm cards send him left and Oasis cards send him right: 8 left, 5 right, 11 left, 3 right, 6 left. Then he must get back to Zara, who is at 0.",
      GIVEN("g", "Start 0: 8 left, 5 right, 11 left, 3 right, 6 left")),
    B("Round 1: he moves 8 steps left from 0. Where is he?",
      ask=choose(["−8", "8", "0"], 0,
                 "Numbers to the left of 0 are negative. 8 steps to the left of 0 is minus 8.")),
    w.mv(-8, "Left is the minus direction.", why=False),
    w.mv(5, "Round 2, 5 right."),
    w.mv(-11, "Round 3, 11 left."),
    w.mv(3, "Round 4, 3 right.", why=False),
    w.mv(-6, "Round 5, 6 left.", why=False),
    B("So Vikram finishes at minus 17, and Zara is at 0. Which way must he walk to reach her, and how far?",
      ask=choose(["17 steps right", "17 steps left", "7 steps right"], 0,
                 "Minus 17 is 17 steps to the left of 0. To get back to 0 he must walk the other way, to the right, the same 17 steps.")),
    B("He is 17 steps to the left of 0, so he walks 17 steps to the right to reach Zara.",
      W("b", "−17 + 17 = 0"), ANS("a", "17 steps to the right", True), M("a", "17", "circle")),
    B("Check with totals. Left moves: 8, 11 and 6 make 25. Right moves: 5 and 3 make 8. 8 right and 25 left leaves 17 to the left.",
      W("c1", "8 + 11 + 6 = 25"), W("c2", "5 + 3 = 8"), W("c3", "8 − 25 = −17")),
    B("Notice the twist at the end. His position is minus 17, on the left, but the walk home is 17 to the right. Where you are and which way you must go are opposites."),
    B("So: left is minus, right is plus, one move at a time. Then read what the question wants at the very end."),
)

# ── Two lift rides: Priya and Arjun ──────────────────────────────────────────
w = Walk(0)
LESSONS["b2187a13"] = lesson(
    B("Two lift rides. Priya starts at floor 0: down 3, up 8, down 6, up 4. Arjun starts at floor 2 and goes down 5. We want the difference between their final floors.",
      GIVEN("g", "Priya: start 0, down 3, up 8, down 6, up 4"), GIVEN("g2", "Arjun: start 2, down 5")),
    w.mv(-3, "Priya first. Down 3."),
    w.mv(8, "Up 8."),
    w.mv(-6, "Down 6."),
    w.mv(4, "Up 4.", why=False, tail="So Priya finishes on floor 3."),
    B("Now Arjun. He starts at floor 2 and goes down 5. Where does he end?",
      M("g2", "start 2, down 5"),
      ask=choose(["floor −3", "floor 3", "floor 7"], 0,
                 "Down means subtract. He has only 2 floors before the ground, and he goes down 5, so the other 3 floors are below the ground.")),
    B("2 minus 5 is minus 3. So Arjun is in the basement, 3 floors below the ground.",
      W("r", "2 − 5 = −3"), M("r", "−3")),
    B("Priya is at 3 and Arjun is at minus 3. How many floors apart are they?",
      ask=choose(["6 floors", "0 floors", "3 floors"], 0,
                 "Count the floors between them. From minus 3 up to the ground is 3 floors, and from the ground up to floor 3 is 3 more.")),
    B("3 floors below the ground and 3 floors above it. 3 plus 3 is 6 floors apart.",
      ANS("a", "3 − (−3) = 6"), M("a", "6", "circle")),
    B("Careful: 3 take away 3 would say they are on the same floor. But subtracting a negative number is the same as adding. 3 minus minus 3 is 3 plus 3.",
      N("a", "− (−3)", "same as + 3")),
    B("So: follow each person separately to the end. Then, for two floors on opposite sides of 0, add their distances from 0."),
)

# ── Team Cheetah: four moves, then halfway to +30 ────────────────────────────
w = Walk(0, horizontal=True)
LESSONS["88489cc3"] = lesson(
    B("Team Cheetah starts at 0: forward 12, backward 19, forward 8, backward 15. Then Round 5 says: go to the spot exactly halfway between where you are and plus 30.",
      GIVEN("g", "Start 0: forward 12, back 19, forward 8, back 15"), GIVEN("g2", "then halfway between there and +30")),
    w.mv(12, "Forward 12."),
    w.mv(-19, "Backward 19."),
    w.mv(8, "Forward 8."),
    w.mv(-15, "Backward 15.", why=False),
    B("They are at minus 14, and the other end is plus 30. How far apart are those two?",
      M("g2", "halfway"),
      ask=choose(["44 steps", "16 steps", "30 steps"], 0,
                 "They are on opposite sides of 0. From minus 14 to 0 is 14 steps, and from 0 to 30 is 30 more, so we add.")),
    B("14 plus 30 is 44 steps. Halfway is half of 44, which is 22 steps.",
      W("h1", "14 + 30 = 44"), W("h2", "44 ÷ 2 = 22"),
      FIG("f", line(-14, 30, [(-14, "now"), (0, "0"), (30, "+30")], 2))),
    B("So they go 22 steps forward from minus 14. Minus 14 plus 22 is 8. Their final position is 8.",
      ANS("a", "−14 + 22 = 8"), M("a", "8", "circle")),
    B("Check from the other end: 22 steps back from 30 is also 8. So 8 really is in the middle.",
      W("c", "30 − 22 = 8")),
    B("A quicker way some people like: add the two ends, then halve. Minus 14 plus 30 is 16, and half of 16 is 8.",
      W("q1", "−14 + 30 = 16"), W("q2", "16 ÷ 2 = 8")),
    B("The slip to avoid is halving the 30 on its own, or treating the minus 14 as plus 14. The gap has to count both sides of 0."),
    B("So: follow the moves, then for halfway, find the whole gap and travel half of it."),
)

# ── Deep Sea Diver: halfway between the end and the deepest point ────────────
w = Walk(0)
_dive = [
    w.mv(-12, "Round 1, down 12.", why=False),
    w.mv(5, "Round 2, up 5."),
    w.mv(-9, "Round 3, down 9."),
    w.mv(-6, "Round 4, down 6.", why=False),
    w.mv(14, "Round 5, up 14.", why=False),
    w.mv(-7, "Round 6, down 7.", why=False),
]
LESSONS["4facbbce"] = lesson(
    B("The submarine starts at 0 and has 6 rounds: down 12, up 5, down 9, down 6, up 14, down 7. The treasure is halfway between where it ends and the deepest point it ever reached.",
      GIVEN("g", "Start 0: down 12, up 5, down 9, down 6, up 14, down 7"),
      GIVEN("g2", "Treasure: halfway between the end and the deepest point")),
    B("Before we start: to find the treasure, which positions will we need?",
      M("g2", "the end"), M("g2", "the deepest point"),
      ask=choose(["the last one and the deepest one", "only the last one", "only the first one"], 0,
                 "The treasure is halfway between two places: where the submarine ends, and the deepest point it ever reached. So we must watch every position along the way.")),
    _dive,
    B("The submarine ends at minus 15. Now look back down the board. Which was the deepest point it ever reached?",
      ask=choose(["−22", "−15", "−16"], 0,
                 "Deepest means furthest below 0, so we want the biggest number after a minus sign. Look at the end of Round 4.")),
    B("The deepest point was minus 22, after Round 4. Notice it is not the final position.",
      M("s4", "−22", "circle"), M("s6", "−15", "circle")),
    B("From minus 15 down to minus 22 is a gap of 7 metres. Half of 7 is 3 and a half, which we write as 3.5.",
      W("h1", "22 − 15 = 7"), W("h2", "7 ÷ 2 = 3.5")),
    B("So the treasure is 3.5 metres below minus 15. That is minus 18.5.",
      ANS("a", "−15 − 3.5 = −18.5"), M("a", "−18.5", "circle")),
    B("Check from the other side: 3.5 metres up from minus 22 is also minus 18.5.",
      W("c", "−22 + 3.5 = −18.5")),
    B("So: keep every position, not only the last one. Then halfway means find the gap, and go half of it."),
)
