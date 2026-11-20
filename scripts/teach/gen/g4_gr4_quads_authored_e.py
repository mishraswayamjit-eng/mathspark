"""Lessons written one by one: Grade 4 quadrilaterals, Q_CH20_005 to 012."""
from g4_gr4_quads_lib import A, B, G, L, T, W, arc, box, choose, divide, figure_getter, group, lesson, note, ring, strike

F = figure_getter("gr4_quads")
LESSONS = {}


def GQ(id, text):
    return W(id, text, tone="given", label=True)


LESSONS["Q_CH20_005"] = lesson([
    B("A rectangle is 12 centimetres long and 7 centimetres broad. What is its perimeter?",
      G("Rectangle: length 12 cm, breadth 7 cm. Perimeter = ?"), F("Q_CH20_005")),
    B("Perimeter is the walk all the way round. First, one length and one breadth: 12 plus 7 is 19.",
      W("l1", "12 + 7 = 19")),
    B("Is 19 the whole perimeter?",
      ask=choose(["Yes, 19 cm", "No, it is only halfway round"], 1,
                 "A rectangle has four sides: two lengths and two breadths. 12 plus 7 walks along just two of them.")),
    B("19 is only halfway round. There are two lengths and two breadths, so we double it.",
      note("l1", "19", "halfway round", "below")),
    B("2 times 19 is 38.", W("l2", "2 × 19 = 38")),
    B("The perimeter is 38 centimetres.", A("a", "Perimeter = 38 cm", label=True), ring("a", "38")),
    B("Check by walking all four sides: 12, 7, 12 and 7 make 38.", W("c", "12 + 7 + 12 + 7 = 38")),
    B("Careful not to multiply 12 by 7. That gives the area. For perimeter we add the sides."),
])

LESSONS["Q_CH20_006"] = lesson([
    B("A rectangle is 15 centimetres long and 8 centimetres broad. What is its area?",
      G("Rectangle: length 15 cm, breadth 8 cm. Area = ?"), F("Q_CH20_006")),
    B("Area is the space inside: 8 rows of little squares with 15 in each row. Which sum counts them?",
      ask=choose(["15 + 8", "15 × 8", "2 × (15 + 8)"], 1,
                 "Adding the sides takes you along the edge. Rows of squares are counted by multiplying: 15 times 8.")),
    B("So we need 15 times 8. Let's split 15 into 10 and 5.", L("l0", "Area = length × breadth"),
      W("l1", "15 × 8 = 10 × 8 + 5 × 8"), note("l1", "15", "10 + 5", "below")),
    B("10 times 8 is 80. And 5 times 8 is 40.", W("l2", "10 × 8 = 80"), W("l3", "5 × 8 = 40")),
    B("Don't stop at 80! That is only part of the rectangle. Add the other part: 80 plus 40 is 120.",
      W("l4", "80 + 40 = 120")),
    B("The area is 120 square centimetres.", A("a", "Area = 120 cm²", label=True), ring("a", "120")),
    B("Check by going backwards: 120 shared into 8 rows gives 15 in each row.", W("c", "120 ÷ 8 = 15")),
    B("For area, multiply length by breadth. If the sum is big, split one number and add the parts."),
])

LESSONS["Q_CH20_007"] = lesson([
    B("A square's perimeter and its area are the same number. What is its side? The choices are 8, 6 and 4.",
      G("Square: perimeter and area are the same number."), GQ("q2", "Side = 8, 6 or 4?"), F("Q_CH20_007")),
    B("The perimeter is 4 times the side. The area is the side times the side. We can simply test each choice.",
      L("l1", "Perimeter = 4 × side"), L("l2", "Area = side × side")),
    B("Try 8. The perimeter is 4 times 8, which is 32. The area is 8 times 8, which is 64. Not the same.",
      W("l3", "4 × 8 = 32"), W("l4", "8 × 8 = 64")),
    B("Try 6. The perimeter is 24 and the area is 36. Closer, but still not the same.",
      W("l5", "4 × 6 = 24"), W("l6", "6 × 6 = 36")),
    B("The area is still too big, so we go smaller. For a side of 4, what are the perimeter and the area?",
      ask=choose(["16 and 16", "16 and 8", "8 and 16"], 0,
                 "The perimeter is 4 times 4. The area is 4 times 4 as well. Both sums are the same.")),
    B("4 times 4 is 16 for the perimeter, and 4 times 4 is 16 for the area. They match!", W("l7", "4 × 4 = 16")),
    B("The side of the square is 4.", A("a", "Side = 4", label=True), ring("a", "4")),
    B("Can you see why? Perimeter is 4 times the side and area is side times the side. They agree when the side itself is 4."),
])

LESSONS["Q_CH20_008"] = lesson([
    B("A rectangle has a perimeter of 32 metres. Which pair can be its length and breadth?",
      G("Rectangle: perimeter = 32 m."), GQ("q2", "Which pair can be the length and breadth?"), F("Q_CH20_008")),
    B("The perimeter is two lengths and two breadths. So one length and one breadth must add up to what?",
      ask=choose(["32", "16", "64"], 1, "32 is all four sides. One length and one breadth is half of the way round, so we halve 32.")),
    B("Half of 32 is 16. A pair fits only if it adds up to 16.", W("l1", "32 ÷ 2 = 16"), box("l1", "16")),
    B("Test 18 and 14. They add up to 32. Careful, that's the trap! 32 is the whole perimeter, not half. This pair is too big.",
      W("l2", "18 + 14 = 32"), note("l2", "32", "too big", "below")),
    B("Test 8 and 7. They add up to 15. That is 1 short of 16. So close, but no.", W("l3", "8 + 7 = 15")),
    B("Test 10.5 and 5.5. The two halves make 1 whole, and 10 plus 5 is 15. So that is 16. It fits!",
      W("l4", "10.5 + 5.5 = 16"), ring("l4", "16")),
    B("So the length and breadth can be 10.5 metres and 5.5 metres.",
      A("a", "10.5 m and 5.5 m", label=True), ring("a", "10.5 m and 5.5 m")),
    B("Sides don't have to be whole numbers. Halve the perimeter, then look for the pair that adds up to it: 10.5 and 5.5."),
])

LESSONS["Q_CH20_009"] = lesson([
    B("This rectangle's sides are written with letters. The length is 2 m plus 5 n. The breadth is m minus 3 n. We want the perimeter.",
      G("Rectangle: length (2m + 5n), breadth (m − 3n)."), GQ("q2", "Perimeter = ?"), F("Q_CH20_009")),
    B("Letters don't change the plan. Perimeter is still length plus breadth, then doubled.",
      L("l0", "Perimeter = 2 × (length + breadth)")),
    B("First add the length and the breadth. Collect the m's together: 2 m and 1 more m make 3 m.",
      L("l1", "(2m + 5n) + (m − 3n)"), group("l1", [T("2m"), T("m", 2)], "3m")),
    B("Now the n's. We have 5 n, and then minus 3 n. What is left?",
      ask=choose(["8n", "2n", "15n"], 1,
                 "The breadth has minus 3 n, so we take 3 n away from the 5 n. 5 take away 3 is 2.")),
    B("5 n take away 3 n leaves 2 n. So length plus breadth is 3 m plus 2 n. That is halfway round.",
      group("l1", [T("5n"), T("3n")], "2n"), L("l2", "length + breadth = 3m + 2n")),
    B("Now double everything. 2 times 3 m is 6 m. And 2 times 2 n is 4 n.",
      L("l3", "2 × (3m + 2n) = 6m + 4n"), arc("l3", "2", ["3m", "2n"])),
    B("Careful: the 2 multiplies both parts, the 3 m and the 2 n. Doubling only one of them is the classic slip."),
    B("So the perimeter is 6 m plus 4 n.", A("a", "Perimeter = 6m + 4n", label=True), ring("a", "6m + 4n")),
    B("With letters or with numbers, the plan is the same: add the two sides, then double."),
])

LESSONS["Q_CH20_010"] = lesson([
    B("This rectangle's sides use a letter, a. The length is 3 a minus 5 and the breadth is a plus 5. The perimeter is 40 centimetres. We must find a.",
      G("Rectangle: length (3a − 5) cm, breadth (a + 5) cm."), GQ("q2", "Perimeter = 40 cm. Find a."), F("Q_CH20_010")),
    B("Start with what we know about perimeters. Length plus breadth is half of the perimeter. Half of 40 is 20.",
      W("l1", "40 ÷ 2 = 20"), note("l1", "20", "length + breadth", "below")),
    B("Now add the length and the breadth. 3 a and 1 more a make 4 a. But what happens to the minus 5 and the plus 5?",
      W("l2", "(3a − 5) + (a + 5) = ?"),
      ask=choose(["They make 10", "They cancel out", "They make 25"], 1,
                 "Minus 5 means take 5 away. Plus 5 puts 5 back. So together they do nothing at all.")),
    B("Minus 5 and plus 5 cancel. So length plus breadth is just 4 a.",
      strike("l2", "− 5"), strike("l2", "+ 5"), W("l3", "(3a − 5) + (a + 5) = 4a")),
    B("Here's the trap: 4 a is only halfway round. So 4 a equals 20, not 40.", W("l4", "4a = 20"), box("l4", "20")),
    B("4 times what makes 20? We divide 20 by 4.", divide("l4", "4")),
    B("20 divided by 4 is 5. So a is 5.", A("a", "a = 5"), ring("a", "a = 5")),
    B("Check. The length is 3 times 5 minus 5, which is 10. The breadth is 5 plus 5, which is 10 too.",
      W("c1", "3 × 5 − 5 = 10"), W("c2", "5 + 5 = 10")),
    B("10 plus 10 is 20, and double 20 is 40. That is our perimeter, so a equals 5 works!", W("c3", "2 × (10 + 10) = 40")),
], check=("a", 5))

LESSONS["Q_CH20_011"] = lesson([
    B("Sam ran ten rounds of a rectangular field, 350 metres long and 120 metres wide. What total distance did Sam run?",
      G("Field: 350 m long, 120 m wide. Sam runs 10 rounds."), GQ("q2", "Total distance = ?"), F("Q_CH20_011")),
    B("One round is the perimeter of the field. One length and one width: 350 plus 120 is 470.",
      W("l1", "350 + 120 = 470")),
    B("Is 470 metres one full round?",
      ask=choose(["Yes", "No, it is half a round"], 1,
                 "350 plus 120 takes Sam along one long side and one short side. He is at the opposite corner, only halfway round.")),
    B("470 is only halfway. Double it for a full round: 2 times 470 is 940 metres.",
      note("l1", "470", "halfway round", "below"), W("l2", "2 × 470 = 940")),
    B("Sam ran ten rounds. 10 times 940 is 9400 metres.", W("l3", "10 × 940 = 9400")),
    B("Now look at the choices. 9400 metres isn't there, but some are in kilometres. 1000 metres make 1 kilometre.",
      L("l4", "1000 m = 1 km")),
    B("9400 divided by 1000 is 9.4. So Sam ran 9.4 kilometres.",
      W("l5", "9400 ÷ 1000 = 9.4"), A("a", "Sam ran 9.4 km", label=True), ring("a", "9.4 km")),
    B("Three things to watch here: double for the full round, times 10 for ten rounds, and change the unit at the end."),
])

LESSONS["Q_CH20_012"] = lesson([
    B("The length and breadth of a rectangle add up to 12 centimetres, and they differ by 2 centimetres. We want the area.",
      G("Length + breadth = 12 cm. Length − breadth = 2 cm."), GQ("q2", "Area = ?"), F("Q_CH20_012")),
    B("Careful: 12 and 2 are not the sides. They are the sum and the difference. First we must find the two sides.",
      box("q", "12 cm"), box("q", "2 cm", 2)),
    B("The length is the breadth and 2 more. So take that extra 2 away from 12. What is left is two equal breadths.",
      W("l1", "12 − 2 = 10"), note("l1", "10", "2 breadths", "below")),
    B("Two breadths make 10. So what is one breadth?",
      ask=choose(["10 cm", "5 cm", "6 cm"], 1, "10 is two equal breadths together. Halve it to get one breadth.")),
    B("Half of 10 is 5. The breadth is 5 centimetres. The length is 2 more, which is 7.",
      W("l2", "10 ÷ 2 = 5"), W("l3", "5 + 2 = 7")),
    B("Check the clues: 7 plus 5 is 12, and 7 minus 5 is 2. Both fit.", W("l4", "7 + 5 = 12"), W("l5", "7 − 5 = 2")),
    B("Now the area: 7 times 5 is 35.", W("l6", "7 × 5 = 35")),
    B("The area is 35 square centimetres.", A("a", "Area = 35 cm²", label=True), ring("a", "35")),
    B("So with a sum and a difference: take the difference off, halve what is left, and you have the smaller side."),
])
