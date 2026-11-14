"""2020 final paper, first batch: the dotted grid, shapes, angles, clock, journey, tables."""
from a_helpers import F, V, bar, bars, fb, seg

VISUALS = {}

# The text says the 4 x 4 grid with its nine interior points "is shown": this is that picture.
VISUALS["EXT_G5_FP_2020_010"] = V(
    F("grid", rows=4, cols=4, dots=True, note="A 4 × 4 grid of squares with its 9 inside crossing points"),
    [
        F("grid", rows=4, cols=4, dots=True, note="Dots: one fewer than 4 each way, so 3 × 3 = 9"),
        None,
        None,
    ], essential=True)

# Right-angled triangle 7, 24, 25: which calculation gives the area?
VISUALS["EXT_G5_FP_2020_011"] = V(
    F("triangle", shape="right", sides={"ab": "24 cm", "bc": "7 cm", "ca": "25 cm"}, note="Area = ?"),
    [
        F("triangle", shape="right", sides={"ab": "24 cm", "bc": "7 cm", "ca": "25 cm"}, hl=["ab", "bc"],
          note="The two sides at the right angle are base 7 and height 24"),
        F("triangle", shape="right", sides={"ab": "24 cm", "bc": "7 cm", "ca": "25 cm"}, enclose=True, hl=["fill"],
          note="Half of the rectangle: ½ × 7 × 24 = 7 × 12"),
        None,
    ])

# Complement of (x − 35) degrees.
VISUALS["EXT_G5_FP_2020_007"] = V(
    F("angles", layout="inRightAngle", parts=[{"label": "(x − 35)°"}, {"label": "?"}],
      note="An angle and its complement together make 90°"),
    [
        F("angles", layout="inRightAngle", parts=[{"label": "(x − 35)°"}, {"label": "90 − (x − 35)"}], hl=["p1"],
          note="The other piece is what is left of 90°"),
        None,
        F("angles", layout="inRightAngle", parts=[{"label": "(x − 35)°"}, {"label": "(125 − x)°"}], hl=["p1"],
          note="90 − x + 35 = (125 − x)°"),
    ])

# Two rectangles with the same area.
VISUALS["EXT_G5_FP_2020_027"] = V(
    F("rectangle", length="16 cm", breadth="?", inside="same area as 12 × 8", proportion=2.6,
      note="The first rectangle is 12 cm by 8 cm"),
    [
        F("rectangle", length="12 cm", breadth="8 cm", inside="96 sq.cm", proportion=1.5, hl=["fill"],
          note="First rectangle: 12 × 8 = 96 sq.cm"),
        F("rectangle", length="16 cm", breadth="6 cm", inside="96 sq.cm", proportion=2.6, hl=["breadth"],
          note="Second rectangle: 96 ÷ 16 = 6 cm wide"),
    ])

# Bells every 2, 5 and 8 minutes, together at 10:00.
VISUALS["EXT_G5_FP_2020_017"] = V(
    F("clock", hour=10, minute=0, note="All three beep now, then every 2, 5 and 8 minutes"),
    [
        F("clock", hour=10, minute=0, note="The first number that 2, 5 and 8 all divide is 40"),
        F("clock", hour=10, minute=40, hl=["minute"], note="40 minutes after 10:00 is 10:40 a.m."),
    ])

# Ant at 15 feet a minute for 24 minutes 40 seconds.
VISUALS["EXT_G5_FP_2020_020"] = V(
    F("journey", places=["start", "24 min", "24 min 40 s"],
      legs=[{"top": "? ft", "bottom": "24 minutes"}, {"top": "? ft", "bottom": "40 seconds"}],
      note="The ant moves 15 feet every minute"),
    [
        F("journey", places=["start", "24 min", "24 min 40 s"],
          legs=[{"top": "360 ft", "bottom": "24 minutes"}, {"top": "? ft", "bottom": "40 seconds"}], hl=["l0"],
          note="24 minutes: 24 × 15 = 360 ft"),
        F("journey", places=["start", "24 min", "24 min 40 s"],
          legs=[{"top": "360 ft", "bottom": "24 minutes"}, {"top": "10 ft", "bottom": "40 seconds"}], hl=["l1"],
          note="40 seconds is two thirds of a minute: 10 ft"),
        F("journey", places=["start", "24 min", "24 min 40 s"],
          legs=[{"top": "360 ft", "bottom": "24 minutes"}, {"top": "10 ft", "bottom": "40 seconds"}], hl=["l0", "l1"],
          note="Total = 360 + 10 = 370 ft"),
    ])

# Chess 5/8, carrom 3/8, both 1/4: who plays neither?
VISUALS["EXT_G5_FP_2020_019"] = V(
    F("venn", leftTitle="Chess 5/8", rightTitle="Carrom 3/8", left="chess only", both="1/4 play both", right="carrom only",
      note="What fraction of the teachers is outside both circles?"),
    [
        F("venn", leftTitle="Chess 5/8", rightTitle="Carrom 3/8", left="chess only", both="1/4 play both", right="carrom only",
          hl=["left", "both", "right"], note="In the circles: 5/8 + 3/8 − 1/4 = 3/4 (overlap counted once)"),
        fb((4, 3, "3/4 play a game"), note="Neither = 1 − 3/4 = 1/4"),
    ])

# Messages: m each hour for 5 hours, p each hour for 4 hours.
VISUALS["EXT_G5_FP_2020_002"] = V(
    bars(bar([seg("m", 1, "a") for _ in range(5)], label="Arnav"),
         bar([seg("p", 1, "b") for _ in range(4)], label="Pranav"),
         note="One box for each hour of messages"),
    [
        bars(bar([seg("m", 1, "a") for _ in range(5)], label="Arnav", brace="5m"),
             bar([seg("p", 1, "b") for _ in range(4)], label="Pranav"),
             hl=["b0"], note="Arnav: 5 lots of m = 5m"),
        bars(bar([seg("m", 1, "a") for _ in range(5)], label="Arnav", brace="5m"),
             bar([seg("p", 1, "b") for _ in range(4)], label="Pranav", brace="4p"),
             hl=["b1"], note="Pranav: 4 lots of p = 4p"),
        bars(bar([seg("m", 1, "a") for _ in range(5)], label="Arnav", brace="5m"),
             bar([seg("p", 1, "b") for _ in range(4)], label="Pranav", brace="4p"),
             note="Together: 5m + 4p"),
    ])

# Harry's saddle: money out and money in.
_saddle = [["April", "buys", "Rs.100"], ["May", "sells", "Rs.200"], ["June", "buys", "Rs.300"], ["July", "sells", "Rs.400"]]
VISUALS["EXT_G5_FP_2020_012"] = V(
    F("table", headers=["Month", "Harry", "Price"], rows=_saddle, note="Compare all the money paid out with all the money received"),
    [
        F("table", headers=["Month", "Harry", "Price"], rows=_saddle, hl=["r0", "r2"], note="Paid out: 100 + 300 = Rs.400"),
        F("table", headers=["Month", "Harry", "Price"], rows=_saddle, hl=["r1", "r3"], note="Received: 200 + 400 = Rs.600"),
        F("table", headers=["Paid out", "Received", "Profit"], rows=[["Rs.400", "Rs.600", "Rs.200"]],
          note="Profit = 600 − 400 = Rs.200"),
    ])

# Apples, mangoes, oranges from three pair totals.
VISUALS["EXT_G5_FP_2020_015"] = V(
    F("table", headers=["Fruits", "Total"], rows=[["A + M", "400"], ["M + O", "300"], ["A + O", "440"]],
      note="He then sells 100 of each. How many of each are left?"),
    [
        F("table", headers=["Fruits", "Total"], rows=[["A + M", "400"], ["M + O", "300"], ["A + O", "440"]],
          hl=["r0", "r1", "r2"], note="All three add to 1140, counting every fruit twice: A + M + O = 570"),
        F("table", headers=["Fruit", "How many"], rows=[["O", "570 − 400 = 170"], ["A", "570 − 300 = 270"], ["M", "570 − 440 = 130"]],
          note="Take each pair away from 570 to find the fruit left out"),
        F("table", headers=["Fruit", "Had", "Left"], rows=[["A", "270", "170"], ["M", "130", "30"], ["O", "170", "70"]],
          note="Selling 100 of each leaves 170, 30 and 70"),
        None,
    ])

# In which number do the place values of 9 and 7 differ by 83000?
VISUALS["EXT_G5_FP_2020_016"] = V(None, [
    F("placeChart", number="1907000", hl=["d1", "d3"], note="9 is worth 900000 and 7 is worth 7000: difference 893000"),
    F("placeChart", number="109700", hl=["d2", "d3"], note="9 is worth 9000 and 7 is worth 700: difference 8300"),
    F("placeChart", number="197000", hl=["d1", "d2"], note="9 is worth 90000 and 7 is worth 7000: 90000 − 7000 = 83000"),
    F("placeChart", number="91700", hl=["d0", "d2"], note="9 is worth 90000 and 7 is worth 700: difference 89300"),
], usesOptions=True)
