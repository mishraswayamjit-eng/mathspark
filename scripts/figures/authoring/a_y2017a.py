"""2017 final paper, first batch: clocks, directions, shapes, then models."""
from a_helpers import F, V, bar, bars, fb, seg

VISUALS = {}

# Clock at 11:00; the hour hand turns through 165 degrees.
VISUALS["EXT_G5_FP_2017_005"] = V(
    F("clock", hour=11, minute=0, hl=["hour"], note="The hour hand now turns through 165°. What time is it then?"),
    [
        F("clock", hour=11, minute=0, hl=["hour"], note="The hour hand turns 30° every hour: 165 ÷ 30 = 5.5 hours"),
        F("clock", hour=4, minute=30, hl=["hour"], note="5 h 30 min after 11:00 a.m. is 4:30 p.m."),
    ])

# Cycling North-East, turns left to face West.
VISUALS["EXT_G5_FP_2017_023"] = V(
    F("compass", facing="NE", hl=["start"], note="He turns to his left until he faces West. How big is the turn?"),
    [
        F("compass", facing="NE", turns=[{"degrees": 45, "direction": "anticlockwise"}], showEnd=True, hl=["t0"],
          note="North-East to North is 45° to the left"),
        F("compass", facing="NE", turns=[{"degrees": 45, "direction": "anticlockwise"}] * 2, showEnd=True, hl=["t1"],
          note="North to North-West is another 45°: 90° so far"),
        F("compass", facing="NE", turns=[{"degrees": 45, "direction": "anticlockwise"}] * 3, showEnd=True, hl=["t2", "end"],
          note="North-West to West is another 45°: 135° in all"),
    ])

# Square and equilateral triangle with the same perimeter.
VISUALS["EXT_G5_FP_2017_018"] = V(
    F("triangle", shape="equilateral", sides={"ab": "8 cm", "bc": "8 cm", "ca": "8 cm"},
      note="A square has the same perimeter as this triangle. Its side = ?"),
    [
        F("triangle", shape="equilateral", sides={"ab": "8 cm", "bc": "8 cm", "ca": "8 cm"}, hl=["ab", "bc", "ca"],
          note="Triangle perimeter = 3 × 8 = 24 cm"),
        F("rectangle", square=True, length="6 cm", breadth="6 cm", inside="Perimeter = 24 cm", hl=["border"],
          note="Four equal sides share 24 cm: 24 ÷ 4 = 6 cm"),
    ])

# Breadth is half the length; perimeter 48 cm.
VISUALS["EXT_G5_FP_2017_019"] = V(
    F("rectangle", length="length", breadth="half the length", inside="Perimeter = 48 cm", proportion=2,
      note="Area = ?"),
    [
        F("rectangle", length="16 cm", breadth="8 cm", inside="Perimeter = 48 cm", proportion=2, hl=["length", "breadth"],
          note="Length + breadth = 24 cm = 3 breadths, so breadth 8 cm, length 16 cm"),
        F("rectangle", length="16 cm", breadth="8 cm", inside="Area = 128 sq.cm", proportion=2, hl=["fill"],
          note="Area = 16 × 8 = 128 sq.cm"),
    ])

# Perimeter of a rectangle with algebraic sides.
VISUALS["EXT_G5_FP_2017_030"] = V(
    F("rectangle", length="(4a + 3b)", breadth="(3a − b)", inside="Perimeter = ?"),
    [
        F("rectangle", length="(4a + 3b)", breadth="(3a − b)", hl=["length", "breadth"],
          note="One length + one breadth = 7a + 2b"),
        F("rectangle", length="(4a + 3b)", breadth="(3a − b)", inside="14a + 4b", hl=["border"],
          note="All the way round is twice that: 2 × (7a + 2b) = 14a + 4b"),
    ])

# Square ground, perimeter 120 m.
VISUALS["EXT_G5_FP_2017_040"] = V(
    F("rectangle", square=True, length="?", inside="Perimeter = 120 m", note="Find one side first, then the area"),
    [
        F("rectangle", square=True, length="30 m", breadth="30 m", hl=["length"],
          note="Four equal sides: 120 ÷ 4 = 30 m each"),
        F("rectangle", square=True, length="30 m", breadth="30 m", inside="Area = 900 sq.m", hl=["fill"],
          note="Area = 30 × 30 = 900 sq.m"),
    ])

# Dogs bark every 5, 8 and 12 minutes from 11:30 p.m.
VISUALS["EXT_G5_FP_2017_027"] = V(
    F("clock", hour=11, minute=30, note="All bark together now, then every 5, 8 and 12 minutes"),
    [
        F("clock", hour=11, minute=30, note="They bark together again after 120 minutes = 2 hours"),
        F("clock", hour=1, minute=30, hl=["hour"], note="2 hours after 11:30 p.m. is 1:30 a.m."),
    ])

# Train 200 m long passes a pole in 9 seconds.
VISUALS["EXT_G5_FP_2017_038"] = V(
    F("journey", places=["front at pole", "back at pole"], legs=[{"top": "200 m", "bottom": "9 seconds"}],
      note="To pass the pole the train moves its own length"),
    [
        F("journey", places=["front at pole", "back at pole"], legs=[{"top": "200 m", "bottom": "9 seconds"}], hl=["l0"],
          note="Speed = 200 ÷ 9 metres every second"),
        F("journey", places=["front at pole", "back at pole"], legs=[{"top": "80 km/hr", "bottom": "9 seconds"}], hl=["l0"],
          note="Multiply by 18/5 to change to km/hr: 80 km/hr"),
    ])

# Five ages, total 105, overlapping pair totals.
_pairs = "A+B = 39, B+C = 40, C+D = 38, D+E = 44"
VISUALS["EXT_G5_FP_2017_001"] = V(
    bars(bar([seg("A"), seg("B"), seg("C"), seg("D"), seg("E")], brace="105 in all"),
         note=_pairs + ". Youngest = ?"),
    [
        bars(bar([seg("A", tone="a"), seg("B", tone="a"), seg("C", tone="b"), seg("D", tone="b"), seg("E = 28", tone="c")], brace="105 in all"),
             hl=["b0s4"], note="Take away A + B and C + D: 105 − 39 − 38 = 28"),
        bars(bar([seg("A = 21", tone="c"), seg("B", tone="a"), seg("C", tone="a"), seg("D", tone="b"), seg("E", tone="b")], brace="105 in all"),
             hl=["b0s0"], note="Take away B + C and D + E: 105 − 40 − 44 = 21"),
        bars(bar([seg("A = 21"), seg("B = 18"), seg("C = 22"), seg("D = 16"), seg("E = 28")], brace="105 in all"),
             note="Work along the pairs: B = 18, C = 22, D = 16"),
        bars(bar([seg("A = 21"), seg("B = 18"), seg("C = 22"), seg("D = 16", tone="a"), seg("E = 28")], brace="105 in all"),
             hl=["b0s3"], note="The youngest is D, aged 16"),
    ])

# Tank 5/6 full, 30 litres removed, now 4/5 full.
VISUALS["EXT_G5_FP_2017_002"] = V(
    fb((6, 5, "before: 5/6 full"), (5, 4, "after: 4/5 full"), note="30 litres were taken out in between. Full tank = ?"),
    [
        fb((6, 5, "5/6 = 25/30"), (5, 4, "4/5 = 24/30"), note="In thirtieths the gap is 25/30 − 24/30 = 1/30"),
        fb((6, 5, "5/6 = 25/30"), (5, 4, "4/5 = 24/30"), note="That gap of 1/30 of the tank is the 30 litres"),
        fb((1, 1, "full = 900 litres"), note="30 parts of 30 litres each: 30 × 30 = 900 litres"),
    ])

# Wholesaler gives 20% off the list price; retailer sells at 8% off it.
VISUALS["EXT_G5_FP_2017_003"] = V(
    bars(bar([seg("100%", 10, "a")], label="list price"),
         bar([seg("shop pays ?", 8, "unknown"), seg("20% off", 2, "b")]),
         bar([seg("shop sells for ?", 9.2, "unknown"), seg("8%", 0.8, "b")]),
         note="Both discounts are taken off the same list price"),
    [
        bars(bar([seg("Rs.100", 10, "a")], label="list price"),
             bar([seg("shop pays ?", 8, "unknown"), seg("20% off", 2, "b")]),
             bar([seg("shop sells for ?", 9.2, "unknown"), seg("8%", 0.8, "b")]),
             hl=["b0"], note="Pretend the list price is Rs.100"),
        bars(bar([seg("Rs.100", 10, "a")], label="list price"),
             bar([seg("shop pays Rs.80", 8, "a"), seg("20% off", 2, "b")]),
             bar([seg("shop sells for ?", 9.2, "unknown"), seg("8%", 0.8, "b")]),
             hl=["b1s0"], note="The shop pays 100 − 20 = Rs.80"),
        bars(bar([seg("Rs.100", 10, "a")], label="list price"),
             bar([seg("shop pays Rs.80", 8, "a"), seg("20% off", 2, "b")]),
             bar([seg("shop sells Rs.92", 9.2, "a"), seg("8%", 0.8, "b")]),
             hl=["b2s0"], note="The shop sells for 100 − 8 = Rs.92"),
        bars(bar([seg("shop pays Rs.80", 8, "a"), seg("profit Rs.12", 1.2, "c")], brace="shop sells Rs.92"),
             hl=["b0s1"], note="Profit 12 on a cost of 80 = 12 ÷ 80 × 100 = 15%"),
    ])

# Four children, ages add to 20.
VISUALS["EXT_G5_FP_2017_006"] = V(
    F("table", headers=["Child", "Age"],
      rows=[["David", "Chetan + 5"], ["Bunty", "David − 3"], ["Anil", "Chetan − 3"], ["All four", "20 in total"]],
      note="Everyone is described from Chetan or David. Anil = ?"),
    [
        F("table", headers=["Child", "Age"],
          rows=[["Chetan", "c"], ["David", "c + 5"], ["Bunty", "c + 2"], ["Anil", "c − 3"]],
          note="Write every age using Chetan's age c"),
        F("table", headers=["Child", "Age"],
          rows=[["Chetan", "c"], ["David", "c + 5"], ["Bunty", "c + 2"], ["Anil", "c − 3"]],
          note="Add them up: 4c + 4 = 20"),
        None,
        F("table", headers=["Child", "Age"],
          rows=[["Chetan", "4"], ["Anil", "4 − 3 = 1"]], hl=["r1"],
          note="Chetan is 4, so Anil is 4 − 3 = 1 year old"),
    ])
