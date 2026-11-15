"""2019 final paper, first batch: shapes, angles, clock, journeys, fraction strips."""
from a_helpers import F, V, fb

VISUALS = {}

# Length twice the breadth, perimeter 90 cm.
VISUALS["EXT_G5_FP_2019_001"] = V(
    F("rectangle", length="twice the breadth", breadth="breadth", inside="Perimeter = 90 cm", proportion=2, note="Area = ?"),
    [
        F("rectangle", length="30 cm", breadth="15 cm", inside="Perimeter = 90 cm", proportion=2, hl=["length", "breadth"],
          note="Length + breadth = 45 cm = 3 breadths, so breadth 15 cm, length 30 cm"),
        F("rectangle", length="30 cm", breadth="15 cm", inside="Area = 450 sq.cm", proportion=2, hl=["fill"],
          note="Area = 30 × 15 = 450 sq.cm"),
    ])

# Supplement of an obtuse angle.
VISUALS["EXT_G5_FP_2019_012"] = V(
    F("angles", layout="onLine", parts=[{"label": "obtuse angle", "size": 125}, {"label": "?"}],
      note="An angle and its supplement together make a straight line"),
    [
        F("angles", layout="onLine", parts=[{"label": "obtuse angle", "size": 125}, {"label": "?"}], hl=["p0"],
          note="An obtuse angle is more than 90° but less than 180°"),
        F("angles", layout="onLine", parts=[{"label": "obtuse angle", "size": 125}, {"label": "180° − x"}], hl=["p1"],
          note="What is left of the straight line is less than 90°"),
        F("angles", layout="onLine", parts=[{"label": "obtuse angle", "size": 125}, {"label": "acute angle"}], hl=["p1"],
          note="An angle smaller than 90° is an acute angle"),
    ])

# Complement of (35 − x) degrees.
VISUALS["EXT_G5_FP_2019_018"] = V(
    F("angles", layout="inRightAngle", parts=[{"label": "(35 − x)°"}, {"label": "?"}],
      note="An angle and its complement together make 90°"),
    [
        F("angles", layout="inRightAngle", parts=[{"label": "(35 − x)°"}, {"label": "90 − (35 − x)"}], hl=["p1"],
          note="The other piece is what is left of 90°"),
        None,
        F("angles", layout="inRightAngle", parts=[{"label": "(35 − x)°"}, {"label": "(55 + x)°"}], hl=["p1"],
          note="90 − 35 + x = (55 + x)°"),
    ])

# Square of side 15 cm and a rectangle of length 25 cm with the same area.
VISUALS["EXT_G5_FP_2019_022"] = V(
    F("rectangle", length="25 cm", breadth="?", inside="= area of 15 cm square",
      note="Find the breadth, then compare the two perimeters"),
    [
        F("rectangle", square=True, length="15 cm", breadth="15 cm", inside="225 sq.cm", hl=["fill"],
          note="Square area = 15 × 15 = 225 sq.cm"),
        F("rectangle", length="25 cm", breadth="9 cm", inside="225 sq.cm", proportion=2.8, hl=["breadth"],
          note="Rectangle breadth = 225 ÷ 25 = 9 cm"),
        F("rectangle", length="25 cm", breadth="9 cm", proportion=2.8, hl=["border"],
          note="Rectangle: 2 × (25 + 9) = 68 cm. Square: 4 × 15 = 60 cm"),
        None,
    ])

# Triangle with angles x, x + 10 and 2x − 6.
VISUALS["EXT_G5_FP_2019_028"] = V(
    F("triangle", shape="scalene", angles={"a": "(2x − 6)°", "b": "x°", "c": "(x + 10)°"},
      note="The three angles of a triangle add up to 180°"),
    [
        F("triangle", shape="scalene", angles={"a": "(2x − 6)°", "b": "x°", "c": "(x + 10)°"}, hl=["a", "b", "c"],
          note="x + x + 10 + 2x − 6 = 180, so 4x = 176 and x = 44"),
        F("triangle", shape="scalene", angles={"a": "82°", "b": "44°", "c": "54°"},
          note="The angles are 44°, 54° and 82°"),
        F("triangle", shape="scalene", angles={"a": "82°", "b": "44°", "c": "54°"}, hl=["a"],
          note="The greatest angle is 82°"),
    ])

# Right-angled triangle 9, 40, 41.
VISUALS["EXT_G5_FP_2019_036"] = V(
    F("triangle", shape="right", sides={"ab": "9 cm", "bc": "40 cm", "ca": "41 cm"}, note="Area = ?"),
    [
        F("triangle", shape="right", sides={"ab": "9 cm", "bc": "40 cm", "ca": "41 cm"}, hl=["ab", "bc"],
          note="The two sides that meet at the right angle are base 40 and height 9"),
        F("triangle", shape="right", sides={"ab": "9 cm", "bc": "40 cm", "ca": "41 cm"}, enclose=True, hl=["fill"],
          note="Half of the rectangle: ½ × 40 × 9 = 180 sq.cm"),
    ])

# 12 minutes as a decimal of an hour.
VISUALS["EXT_G5_FP_2019_027"] = V(
    F("clock", hour=12, minute=12, hl=["minute"], note="What part of a full hour is 12 minutes?"),
    [
        F("clock", hour=12, minute=12, hl=["minute"], note="12 of the 60 minutes have gone: 12/60 of an hour"),
        fb((5, 1, "12/60 = 1/5"), shape="circle", note="12 minutes is one of 5 equal parts of the hour"),
        fb((5, 1, "1/5"), (10, 2, "2/10 = 0.2"), note="1/5 is the same as 2/10, which is 0.2"),
        None,
    ])

# 900 m in 18 minutes; how far in an hour?
VISUALS["EXT_G5_FP_2019_006"] = V(
    F("journey", places=["start", "18 min later"], legs=[{"top": "900 m", "bottom": "18 minutes"}],
      note="How far in 60 minutes at the same pace?"),
    [
        F("journey", places=["start", "1 min later"], legs=[{"top": "50 m", "bottom": "1 minute"}],
          note="In one minute: 900 ÷ 18 = 50 m"),
        F("journey", places=["start", "1 hour later"], legs=[{"top": "3000 m", "bottom": "60 minutes"}],
          note="In 60 minutes: 50 × 60 = 3000 m"),
        F("journey", places=["start", "1 hour later"], legs=[{"top": "3 km", "bottom": "60 minutes"}], hl=["l0"],
          note="3000 m = 3 km"),
    ])

# 18 km at 72 km/hr.
VISUALS["EXT_G5_FP_2019_023"] = V(
    F("journey", places=["start", "finish"], legs=[{"top": "18 km at 72 km/hr", "bottom": "? minutes"}]),
    [
        F("journey", places=["start", "finish"], legs=[{"top": "18 km at 72 km/hr", "bottom": "1/4 hour"}],
          note="18 km is a quarter of 72 km, so it takes 1/4 of an hour"),
        F("journey", places=["start", "finish"], legs=[{"top": "18 km at 72 km/hr", "bottom": "15 minutes"}], hl=["l0"],
          note="1/4 × 60 = 15 minutes"),
    ])

# Equilateral triangle and square with equal perimeters: the pair that works.
VISUALS["EXT_G5_FP_2019_024"] = V(None, [
    None,
    F("triangle", shape="equilateral", sides={"ab": "9", "bc": "9", "ca": "9"}, hl=["ab", "bc", "ca"],
      note="Triangle of side 9: 3 × 9 = 27. Square of side 9: 4 × 9 = 36"),
    F("triangle", shape="equilateral", sides={"ab": "12", "bc": "12", "ca": "12"}, hl=["ab", "bc", "ca"],
      note="Triangle of side 12: 3 × 12 = 36. Square of side 10: 4 × 10 = 40"),
    F("triangle", shape="equilateral", sides={"ab": "16", "bc": "16", "ca": "16"}, hl=["ab", "bc", "ca"],
      note="Triangle: 3 × 16 = 48. Square of side 12: 4 × 12 = 48. Equal"),
    None,
], usesOptions=True)

# Smallest of 11/12, 10/11, 21/22, 7/6.
VISUALS["EXT_G5_FP_2019_019"] = V(
    fb((12, 11, "11/12"), (11, 10, "10/11"), (22, 21, "21/22"),
       note="7/6 is more than a whole. Look at the piece each of these is missing"),
    [
        None,
        fb((12, 11, "1/12 missing"), (11, 10, "1/11 missing"), (22, 21, "1/22 missing"),
           note="Each is one piece short of a whole: 1/12, 1/11 and 1/22"),
        fb((12, 11, "11/12"), (11, 10, "10/11"), (22, 21, "21/22"), hl=["b1"],
           note="1/11 is the biggest missing piece, so 10/11 is the smallest"),
    ], usesOptions=True)

# A fraction equivalent to 36/54.
VISUALS["EXT_G5_FP_2019_011"] = V(None, [
    fb((3, 2, "36/54 = 2/3"), note="Divide top and bottom by 18: 36/54 = 2/3"),
    fb((3, 2, "36/54 = 2/3"), (21, 14, "14/21"), hl=["b1"], note="14/21 shades the same amount: divide by 7 to get 2/3"),
    None,
    None,
])
