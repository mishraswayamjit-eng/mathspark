"""gr4_counting lessons, part A: the real past-paper questions (EXT_G4_FP_..., PYQ_...) and Q_CH21_013."""
from g4_counting_lib import a, b, c, g, l, qf, w

LESSONS = {}

LESSONS["EXT_G4_FP_2020_026"] = [
    b("8 points sit on a circle. We join every pair of points with a line segment. How many segments is that?",
      g("q", "8 points on a circle. Join every pair. How many?"), qf("EXT_G4_FP_2020_026")),
    b("Pick any one point. It can be joined to every other point. That is 7 segments from this one point.",
      w("c1", "8 − 1 = 7")),
    b("There are 8 points, each with 7 segments. 8 times 7 is 56. Is 56 our answer?", w("c2", "8 × 7 = 56"),
      ask=c("no, each segment is counted twice", ["yes, 56 segments", "no, we should add 8 and 7"],
            "A segment has two ends. We counted it once from each end, so every segment is in our 56 two times.")),
    b("The segment from one point to another is the same segment coming back. So we halve 56. That gives 28.",
      w("c3", "56 ÷ 2 = 28")),
    b("Let's check a slower way. The first point makes 7 new segments. The next makes 6 new ones, then 5, and so on down to 1.",
      w("c4", "7 + 6 + 5 + 4 + 3 + 2 + 1 = 28")),
    b("Both ways give 28. So there are 28 line segments.", a("ans", "28 segments")),
    b("The method: each point joins all the others. Then halve, because every segment got counted twice."),
]

LESSONS["PYQ_2019_Q07"] = [
    b("8 points, named A to H, are marked on a circle. We join every pair. How many line segments can we draw?",
      g("q", "Points A to H on a circle. Join every pair."), qf("PYQ_2019_Q07")),
    b("Start at A. It can be joined to B, C, D, E, F, G and H. That is 7 segments.", l("s1", "From A: 7")),
    b("Now B. It also joins 7 other points. But one of those segments is already drawn. Which one?",
      ask=c("the one to A", ["the one to C", "the one to H"],
            "We already drew the segment from A to B. Going from B back to A is the very same segment, so we must not count it again.")),
    b("So B gives only 6 new segments. C gives 5 new ones, D gives 4, and it keeps shrinking by 1.",
      l("s2", "From B: 6   From C: 5   From D: 4")),
    b("E gives 3, F gives 2, and G gives 1. And H? All its segments are drawn already.",
      l("s3", "From E: 3   From F: 2   From G: 1   From H: 0")),
    b("Now add them up. 7 plus 6 plus 5 plus 4 plus 3 plus 2 plus 1.", w("c1", "7 + 6 + 5 + 4 + 3 + 2 + 1 = 28")),
    b("That makes 28. So 28 line segments can be drawn.", a("ans", "28 segments")),
    b("A quick check: 8 points, times 7 partners each, then halved because each segment has two ends. That is 28 again.",
      w("ck", "8 × 7 ÷ 2 = 28")),
]


def _chess(first, last):
    return [
        b(first, g("q", "A, B, C, D. 2 games with every other. Total?")),
        b("A game needs 2 players. So first let's find all the pairs of players. Start with A: A and B, A and C, A and D.",
          l("p1", "AB  AC  AD")),
        b("Now B. The pair B and A is already on our list, written as A B. So which new pairs does B make?",
          ask=c("BC and BD", ["BA, BC and BD", "only BC"],
                "B with A is the same pair as A with B. So the new ones are B with C, and B with D.")),
        b("B gives B C and B D. And the last new pair is C and D.", l("p2", "BC  BD"), l("p3", "CD")),
        b("Count the pairs: 3, then 2, then 1. That makes 6 pairs.", w("c1", "3 + 2 + 1 = 6")),
        b("Every pair plays 2 games. 6 times 2 is 12.", w("c2", "6 × 2 = 12")),
        b("So 12 games were played altogether.", a("ans", "12 games")),
        b(last),
    ]


LESSONS["EXT_G4_FP_2021_004"] = _chess(
    "A, B, C and D play chess. Each one plays 2 games with every other player. How many games in all?",
    "The trap is 4 times 2, which is 8. Games belong to pairs, not to single players. So count the pairs first.")
LESSONS["PYQ_2016_Q17"] = _chess(
    "4 friends, A, B, C and D, are playing chess. Each of them plays 2 games with every other player. How many games is that altogether?",
    "Remember: a game belongs to a pair of players. List the pairs in order, count them, then multiply by the games each pair plays.")


def _points15(first):
    return [
        b(first, g("q", "? points on a circle → 15 segments")),
        b("We do not know the number of points, so let's build up from small cases. 2 points give just 1 segment.",
          l("t1", "2 points: 1")),
        b("Add a 3rd point. It can be joined to both of the points already there. How many segments now?",
          ask=c("3", ["2", "4"], "There was 1 segment. The new point adds 2 more, one to each old point. 1 plus 2.")),
        b("1 plus 2 is 3. Here is the pattern: each new point joins all the points already there.",
          l("t2", "3 points: 1 + 2 = 3")),
        b("A 4th point adds 3 more, which makes 6. A 5th point adds 4 more, which makes 10.",
          l("t3", "4 points: 3 + 3 = 6"), l("t4", "5 points: 6 + 4 = 10")),
        b("We want 15, and we are at 10. A 6th point adds 5 more. 10 plus 5 is 15. There it is!",
          l("t5", "6 points: 10 + 5 = 15")),
        b("So there were 6 points on the circle.", a("ans", "6 points")),
        b("Check another way: 6 points, each joined to 5 others, is 30. Halve it, since each segment was counted twice. 15.",
          w("ck1", "6 × 5 = 30"), w("ck2", "30 ÷ 2 = 15")),
    ]


LESSONS["EXT_G4_FP_2021_014"] = _points15(
    "Some points are on a circle. Joining every pair gives 15 line segments at most. How many points are there?")
LESSONS["PYQ_2018_Q12"] = _points15(
    "The teacher joins every pair of points on a circle and gets 15 line segments, the most possible. How many points were on the circle?")


def _odd4(first, given, others_after_7):
    return [
        b(first, g("q", given)),
        b("What makes a number odd?",
          ask=c("its last digit is odd", ["its first digit is odd", "all its digits are odd"],
                "Only the ones digit decides whether a number is odd or even. The other digits do not matter.")),
        b("So the last digit must be odd. Of our digits, 7 and 9 are odd. That is 2 choices for the ones place.",
          l("b", "_ _ _ [7 or 9]")),
        b("Say we put 7 last. Then %s are left for the other 3 places: 3 choices, then 2, then 1. 3 times 2 times 1 is 6 numbers." % others_after_7,
          w("c1", "3 × 2 × 1 = 6")),
        b("It is the same story if 9 goes last: 6 more numbers. Careful not to stop at 6!"),
        b("6 numbers end in 7 and 6 numbers end in 9. 2 times 6 is 12.", w("c2", "2 × 6 = 12")),
        b("So 12 odd numbers can be made.", a("ans", "12 numbers")),
        b("The plan: fill the place that has a rule first. Then count the choices for the other places and multiply."),
    ]


LESSONS["EXT_G4_FP_2023_031"] = _odd4(
    "We have the digits 4, 7, 6 and 9. Using each one only once, how many 4-digit odd numbers can we make?",
    "Digits 4, 7, 6, 9, each once. 4-digit odd numbers?", "4, 6 and 9")
LESSONS["EXT_G4_FP_2025_019"] = _odd4(
    "Here are 4 digits: 7, 6, 9 and 4. Each is used once. How many 4-digit odd numbers can be made?",
    "Digits 7, 6, 9, 4, each once. 4-digit odd numbers?", "6, 9 and 4")

LESSONS["EXT_G4_FP_2023_035"] = [
    b("15 people are at a meeting. Each person shakes hands once with every other person. How many handshakes?",
      g("q", "15 people. Everyone shakes hands once. Total?")),
    b("Think about one person. They shake hands with everyone except themselves. That is 14 handshakes.",
      w("c1", "15 − 1 = 14")),
    b("15 people, 14 handshakes each. 15 times 10 is 150, and 15 times 4 is 60. Together, 210.",
      w("c2", "15 × 14 = 150 + 60"), w("c3", "150 + 60 = 210")),
    b("Is 210 the number of handshakes?",
      ask=c("no, halve it", ["yes, 210", "no, double it"],
            "When two people shake hands, that is one handshake. But we counted it once for each of them.")),
    b("Every handshake was counted twice, once for each person. So we halve 210. Half of 210 is 105.",
      w("c4", "210 ÷ 2 = 105")),
    b("So there are 105 handshakes.", a("ans", "105 handshakes")),
    b("Try it with 3 people: 3 times 2 is 6, and half of that is 3 handshakes. Each person with all the others, then halve.",
      w("ck", "3 × 2 ÷ 2 = 3")),
]

LESSONS["EXT_G4_FP_2024_029"] = [
    b("We have the digits 1, 5, 3 and 7. Using each one once, how many numbers bigger than 5000 can we make?",
      g("q", "Digits 1, 5, 3, 7, each once. Numbers > 5000?")),
    b("Which place decides whether a 4-digit number is bigger than 5000?",
      ask=c("the thousands place", ["the ones place", "the tens place"],
            "The thousands digit is worth the most. If it is 5 or more, the number is 5000 or more.")),
    b("So the first digit must be 5 or 7. If it were 1 or 3, the number would be too small. That gives 2 choices for the first place.",
      l("b", "[5 or 7] _ _ _")),
    b("Say 5 goes first. Then 1, 3 and 7 fill the other 3 places: 3 choices, then 2, then 1. That is 6 numbers.",
      w("c1", "3 × 2 × 1 = 6")),
    b("And if 7 goes first, we get 6 more in the same way. 2 times 6 is 12.", w("c2", "2 × 6 = 12")),
    b("So 12 numbers are greater than 5000.", a("ans", "12 numbers")),
    b("Careful: the 4 digits make 24 numbers in total, but only half of them start with 5 or 7.",
      w("ck", "4 × 3 × 2 × 1 = 24")),
    b("Fill the place that has a rule first, then count the choices for the rest."),
]

LESSONS["Q_CH21_013"] = [
    b("5 points are marked on a circle. A chord is a straight line joining 2 of the points. How many chords can we draw?",
      g("q", "5 points on a circle. How many chords?")),
    b("Let's name the points A, B, C, D and E. From A we can draw chords to B, C, D and E. That is 4.",
      l("s1", "From A: 4"), qf("Q_CH21_013", 0)),
    b("Now B. How many new chords can B make?",
      ask=c("3", ["4", "5"], "B joins C, D and E. The chord from B to A is already drawn, so it is not new.")),
    b("B gives 3 new chords. C gives 2 new ones, to D and E. D gives 1 new one, to E.",
      l("s2", "From B: 3   From C: 2   From D: 1")),
    b("And E? Every chord from E is already there. So we add: 4 plus 3 plus 2 plus 1.", w("c1", "4 + 3 + 2 + 1 = 10")),
    b("That is 10. So 10 chords can be drawn.", a("ans", "10 chords")),
    b("The trap is 5 times 4, which is 20. That counts each chord twice, once from each end. Half of 20 is 10 again.",
      w("ck1", "5 × 4 = 20"), w("ck2", "20 ÷ 2 = 10")),
]
