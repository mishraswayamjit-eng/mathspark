"""2018 final paper, first batch: shapes, angles, journeys, place value, factor trees."""
from a_helpers import F, V, fb

VISUALS = {}

# Field 110 m by 70 m, 1 gram of seed per square metre.
VISUALS["EXT_G5_FP_2018_001"] = V(
    F("rectangle", length="110 m", breadth="70 m", inside="1 g of seed per sq.m", note="How much seed for the whole field?"),
    [
        F("rectangle", length="110 m", breadth="70 m", inside="7700 sq.m", hl=["fill"], note="Area = 110 × 70 = 7700 sq.m"),
        F("rectangle", length="110 m", breadth="70 m", inside="7700 g of seed", hl=["fill"], note="1 g for each sq.m: 7700 g"),
        F("rectangle", length="110 m", breadth="70 m", inside="7.7 kg of seed", note="1000 g make 1 kg: 7700 ÷ 1000 = 7.7 kg"),
    ])

# A 2 is slipped between the 3 and the 5 of 43541.
VISUALS["EXT_G5_FP_2018_002"] = V(
    F("placeChart", number="43541", hl=["d1", "d2"], note="A 2 goes in between the 3 and the 5. How much bigger is it now?"),
    [
        F("placeChart", number="432541", hl=["d2"], note="New number 432541: the 4 and 3 each moved one place left"),
        F("placeChart", number="432541", note="432541 − 43541 = 389000"),
    ])

# Statements about complements and supplements.
VISUALS["EXT_G5_FP_2018_007"] = V(None, [
    F("angles", layout="onLine", parts=[{"label": "30°", "size": 30}, {"label": "150°"}], hl=["p1"],
      note="The supplement of 30° is 150°, which is more than 90°"),
    F("angles", layout="inRightAngle", parts=[{"label": "x"}, {"label": "90° − x"}], hl=["p1"],
      note="Both pieces fit inside a right angle, so both are acute"),
    None,
    None,
])

# C is halfway between 1/5 and 1/3.
VISUALS["EXT_G5_FP_2018_008"] = V(
    fb((5, 1, "A = 1/5"), (3, 1, "B = 1/3"), note="C is exactly halfway between A and B"),
    [
        fb((15, 3, "A = 3/15"), (15, 5, "B = 5/15"), note="Cut both into 15 equal parts to compare"),
        fb((15, 3, "A = 3/15"), (15, 4, "C = 4/15"), (15, 5, "B = 5/15"), hl=["b1"],
           note="Halfway between 3 parts and 5 parts is 4 parts"),
        None,
    ])

# Rectangle with perimeter 72 cm: which pair of sides?
VISUALS["EXT_G5_FP_2018_009"] = V(
    F("rectangle", length="length ?", breadth="breadth ?", inside="Perimeter = 72 cm"),
    [
        F("rectangle", length="length ?", breadth="breadth ?", inside="Perimeter = 72 cm", hl=["length", "breadth"],
          note="One length + one breadth = 72 ÷ 2 = 36"),
        None,
        F("rectangle", length="21", breadth="15", inside="Perimeter = 72 cm", hl=["length", "breadth"],
          note="21 + 15 = 36, so this pair fits"),
    ])

# Complement of (38 − x) degrees.
VISUALS["EXT_G5_FP_2018_014"] = V(
    F("angles", layout="inRightAngle", parts=[{"label": "(38 − x)°"}, {"label": "?"}],
      note="An angle and its complement together make 90°"),
    [
        F("angles", layout="inRightAngle", parts=[{"label": "(38 − x)°"}, {"label": "90 − (38 − x)"}], hl=["p1"],
          note="The other piece is what is left of 90°"),
        None,
        F("angles", layout="inRightAngle", parts=[{"label": "(38 − x)°"}, {"label": "(52 + x)°"}], hl=["p1"],
          note="90 − 38 + x = (52 + x)°"),
    ])

# Square whose sides are given by two expressions.
VISUALS["EXT_G5_FP_2018_018"] = V(
    F("rectangle", square=True, length="(3a − 7) cm", breadth="(2a − 1) cm", note="All sides of a square are equal. Perimeter = ?"),
    [
        F("rectangle", square=True, length="(3a − 7) cm", breadth="(2a − 1) cm", hl=["length", "breadth"],
          note="Equal sides: 3a − 7 = 2a − 1, so a = 6"),
        F("rectangle", square=True, length="11 cm", breadth="11 cm", hl=["length"], note="Side = 3 × 6 − 7 = 11 cm"),
        F("rectangle", square=True, length="11 cm", breadth="11 cm", inside="Perimeter = 44 cm", hl=["border"],
          note="Perimeter = 4 × 11 = 44 cm"),
    ])

# Equilateral triangle with perimeter 16a + 7b.
VISUALS["EXT_G5_FP_2018_029"] = V(
    F("triangle", shape="equilateral", sides={"ab": "?", "bc": "?", "ca": "?"},
      note="Perimeter = 16a + 7b, with a = 2 and b = 4"),
    [
        F("triangle", shape="equilateral", sides={"ab": "?", "bc": "?", "ca": "?"}, hl=["ab", "bc", "ca"],
          note="Perimeter = 16 × 2 + 7 × 4 = 32 + 28 = 60"),
        F("triangle", shape="equilateral", sides={"ab": "20", "bc": "20", "ca": "20"},
          note="Three equal sides share 60: 60 ÷ 3 = 20"),
    ])

# Train 100 m long at 36 km/hr passes a standing man.
VISUALS["EXT_G5_FP_2018_036"] = V(
    F("journey", places=["front at man", "back at man"], legs=[{"top": "100 m", "bottom": "? seconds"}],
      note="The train moves its own length at 36 km/hr"),
    [
        F("journey", places=["front at man", "back at man"], legs=[{"top": "100 m at 10 m/s", "bottom": "? seconds"}],
          note="36 km/hr is the same as 10 metres every second"),
        F("journey", places=["front at man", "back at man"], legs=[{"top": "100 m at 10 m/s", "bottom": "10 seconds"}], hl=["l0"],
          note="Time = 100 ÷ 10 = 10 seconds"),
    ])

# Walking at 6 km/hr for 3 minutes.
VISUALS["EXT_G5_FP_2018_020"] = V(
    F("journey", places=["start", "3 min later"], legs=[{"top": "? m", "bottom": "3 minutes"}],
      note="He walks 6 km in every hour"),
    [
        F("journey", places=["start", "1 hour later"], legs=[{"top": "6000 m", "bottom": "60 minutes"}],
          note="6 km = 6000 m, walked in 60 minutes"),
        F("journey", places=["start", "1 min later"], legs=[{"top": "100 m", "bottom": "1 minute"}],
          note="In one minute: 6000 ÷ 60 = 100 m"),
        F("journey", places=["start", "3 min later"], legs=[{"top": "300 m", "bottom": "3 minutes"}], hl=["l0"],
          note="In 3 minutes: 3 × 100 = 300 m"),
    ])

# HCF of 54, 288 and 360 by prime factors.
VISUALS["EXT_G5_FP_2018_024"] = V(None, [
    F("factorTree", number=54, hl=["primes"], note="54 = 2 × 3 × 3 × 3"),
    F("factorTree", number=288, hl=["primes"], note="288 = 2 × 2 × 2 × 2 × 2 × 3 × 3"),
    F("factorTree", number=360, hl=["primes"], note="360 = 2 × 2 × 2 × 3 × 3 × 5"),
    F("table", headers=["Number", "2s", "3s"], rows=[["54", "one", "three"], ["288", "five", "two"], ["360", "three", "two"]],
      note="Shared by all: one 2 and two 3s, so 2 × 9 = 18"),
])

# Greatest number from 9, 5, 0, 7, 3; place values of 5 and 3.
VISUALS["EXT_G5_FP_2018_022"] = V(
    F("table", rows=[["9", "5", "0", "7", "3"]], note="Make the greatest number, then look at where 5 and 3 sit"),
    [
        F("placeChart", number="97530", note="Biggest digits first: 97530"),
        F("placeChart", number="97530", hl=["d2", "d3"], note="5 is in the hundreds (500); 3 is in the tens (30)"),
        F("placeChart", number="97530", hl=["d2", "d3"], note="Difference = 500 − 30 = 470"),
    ])
