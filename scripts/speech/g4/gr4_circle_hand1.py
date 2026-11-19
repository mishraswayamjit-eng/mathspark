"""Hand-written narration for gr4_circle: lines the rules cannot say well.

HAND is keyed by question id (q / options / hints / steps; None leaves a line to the rules).
LINES is keyed by the printed line itself, wherever it appears in the topic.
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
    "'Con-centric' means 'with the same centre.'":
        "Concentric means: with the same centre.",
    "A chord through the centre = diameter. It's the longest chord.":
        "A chord through the centre is a diameter. It's the longest chord.",
    "Infinite diameters = infinite axes of symmetry.":
        "Infinite diameters means infinite axes of symmetry.",
    "'Semi' means half. So semicircle = half circle.":
        "Semi means half. So semicircle means half circle.",
    "Each half = a semicircle.":
        "Each half is a semicircle.",
    "Same centre + different radii = concentric circles.":
        "Same centre, plus different radii, gives concentric circles.",
    "1 lap = C = 2πr = 2 × 22/7 × 35 = 220 m":
        "1 lap equals C, which is 2 pi r. That is 2 times 22 over 7 times 35, which is 220 metres. 2 times 22 times 5 equals 220.",
    "1 lap = circumference = 2πr = 2 × 22/7 × 35.":
        "1 lap equals the circumference, which is 2 pi r. That is 2 times 22 over 7 times 35.",
    "Half circumference = πd/2 = 22/7 × 14/2 = 22/7 × 7 = 22 cm.":
        "Half the circumference equals pi d over 2. That is 22 over 7 times 14 over 2, which is 22 over 7 times 7, or 22 centimetres.",
    "Example: Six circles in 2 rows of 3 fill a rectangle of perimeter 40 cm. Length + width = 3 + 2 = 5 diameters = 20 cm, so a diameter is 4 cm and the radius is 2 cm.":
        "Example: Six circles in 2 rows of 3 fill a rectangle of perimeter 40 centimetres. Length plus width equals 3 plus 2, which is 5 diameters, or 20 centimetres, so a diameter is 4 centimetres and the radius is 2 centimetres.",
    "C = 2πr → r = C/(2π)":
        "C equals 2 pi r, so r equals C over 2 pi. So r equals 440, divided by 2 times 22 over 7.",
    "C = πd → d = C/π":
        "C equals pi d, so d equals C over pi. So d equals 176 divided by 22 over 7, which is 176 times 7 over 22.",
    "C = 2πr. So r = C ÷ (2π) = 440 ÷ (2 × 22/7).":
        "C equals 2 pi r. So r equals C divided by 2 pi, which is 440, divided by 2 times 22 over 7.",
}
