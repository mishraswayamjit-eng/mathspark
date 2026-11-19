"""Hand-written narration for gr4_circle: lines the rules cannot say well.

HAND is keyed by question id (q / options / hints / steps; None leaves a line to the rules).
LINES is keyed by the printed line itself, wherever it appears in the topic. A line whose
print changes can therefore never be read against new text: gr4_circle.py reports it as UNUSED.
"""

HAND = {
    # Past papers whose question is printed as notes: said as sentences, same facts in the same order.
    "EXT_G4_FP_2021_024": {
        "q": "The area of a circle is 3 times its circumference. What is the radius?",
    },
    "EXT_G4_FP_2022_020": {
        "q": "The circumference and the area of a circle are numerically the same. What is the diameter?",
    },
    "EXT_G4_FP_2023_033": {
        "q": "The circumference of a circle is 132 centimetres. Find its area.",
    },
    "EXT_G4_FP_2025_015": {
        "q": "The circumference of a circle equals the perimeter of a rectangle, 14 centimetres by 8 centimetres. What is the radius?",
    },
}

LINES = {
    # G4A_CIRCLE_018
    "Example: Six circles in 2 rows of 3 fill a rectangle of perimeter 40 cm. Length + width = 3 + 2 = 5 diameters = 20 cm, so a diameter is 4 cm and the radius is 2 cm.":
        "Example: Six circles in 2 rows of 3 fill a rectangle of perimeter 40 centimetres. Length plus width equals 3 plus 2, which is 5 diameters, or 20 centimetres, so a diameter is 4 centimetres and the radius is 2 centimetres.",
}
