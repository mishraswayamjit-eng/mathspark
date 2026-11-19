"""Hand-written narration for gr4_quads: lines the rules cannot say well.

HAND is keyed by question id (q / options / hints / steps; None leaves a line to the rules).
LINES is keyed by the printed line itself, wherever it appears in the topic. A line whose
print changes can therefore never be read against new text: gr4_quads.py reports it as UNUSED.
"""

HAND = {
    # Past papers whose question is printed as notes: said as sentences, same facts in the same order.
    "EXT_G4_FP_2020_017": {
        "q": "A rectangle's length is 2 more than its width. The length is 8 feet. What is its area?",
    },
    "EXT_G4_FP_2020_028": {
        "q": "A wire is bent into a rectangle, 16 centimetres by 12 centimetres. The same wire is bent into a square. What is the side of the square?",
    },
    "EXT_G4_FP_2021_038": {
        "q": "The perimeter of a square of side a is 28 centimetres. What is the area of a rectangle that is 3 a by 2 a?",
    },
    "EXT_G4_FP_2022_013": {
        "q": "The perimeter of a square is 132 centimetres. What is its area?",
    },
    "EXT_G4_FP_2023_012": {
        "q": "The perimeters of a square and an equilateral triangle are the same. The side of the triangle is 12 centimetres. What is the area of the square?",
    },
    "EXT_G4_FP_2024_032": {
        "q": "The perimeter of a rectangle is 76 centimetres. Which of these cannot be its length and breadth?",
    },
    "EXT_G4_FP_2025_028": {
        "q": "The breadth of a rectangle is 12 centimetres, and its perimeter is 52 centimetres. What is its area?",
    },
}

LINES = {
    # Q_CH20_010
    "P = 2(L+B). 40 = 2[(3a−5) + (a+5)].":
        "P equals 2 times, L plus B. So 40 equals 2 times, open bracket, 3 a minus 5, plus a plus 5, close bracket.",
    "40 = 2[4a]. So 40 = 8a.":
        "40 equals 2 times 4 a. So 40 equals 8 a.",
    # Q_CH20_014
    "Square perimeter = 4 × 6 = 24 cm. Triangle perimeter = same = 24 cm.":
        "Square perimeter equals 4 times 6, which is 24 centimetres. The triangle perimeter is the same, 24 centimetres.",
    # G4A_QUADS_025
    "Similar problem: the length is 2 times the breadth. Then the area is 2 x breadth x breadth. An area of 50 sq cm works, because 50 ÷ 2 = 25 = 5 x 5, giving a rectangle 10 cm by 5 cm. An area of 40 sq cm does not, because 40 ÷ 2 = 20 is not a number times itself.":
        "Similar problem: the length is 2 times the breadth. Then the area is 2 times breadth times breadth. An area of 50 square centimetres works, because 50 divided by 2 is 25, which is 5 times 5, giving a rectangle 10 centimetres by 5 centimetres. An area of 40 square centimetres does not, because 40 divided by 2 is 20, which is not a number times itself.",
    # G4A_QUADS_022
    "Similar problem: is 'a quadrilateral with four right angles is always a square' true? A rectangle 5 cm by 2 cm has four right angles, but its sides are not all equal. One shape that breaks the statement is enough, so it is not always true.":
        "Similar problem: is this statement true? A quadrilateral with four right angles is always a square. A rectangle 5 centimetres by 2 centimetres has four right angles, but its sides are not all equal. One shape that breaks the statement is enough, so it is not always true.",
    # Q_CH20_004 (rewritten help): the print is about how the unit is written, so the letters are said
    "Similar example: a square has a side of 7 m. Its area is 7 × 7 = 49 square metres, written 49 sq. m.":
        "Similar example: a square has a side of 7 metres. Its area is 7 times 7, which is 49 square metres, written 49 s q m.",
    "The side is in metres, so the area is in square metres, written sq. m. The unit m on its own measures length, not area.":
        "The side is in metres, so the area is in square metres, written s q m. The unit m on its own measures length, not area.",
}
