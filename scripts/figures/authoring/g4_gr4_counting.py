"""Figures for Grade 4 "Counting & Arrangements" (gr4_counting).

    python -X utf8 scripts/figures/authoring/g4_gr4_counting.py

Writes data/question-figures/parts/g4-gr4_counting.json. These questions are all different
from one another, so each is drawn individually; two small rules cover the families that
do repeat (digits placed in boxes, and points joined on a circle).
"""
import math
import re

from g4_gr4_factors_lib import Part, steps_of, table, venn, number_line, with_note

P = Part("gr4_counting")
Q = P.Q


def A(qid, figure=None, steps=None, **kw):
    P.add(qid, figure, steps, origin=kw.pop("origin", "authored"), **kw)


def ring(k):
    """k points evenly round a circle, the first at the top, going clockwise."""
    return [[round(6 + 5 * math.sin(2 * math.pi * i / k), 2), round(6 - 5 * math.cos(2 * math.pi * i / k), 2)] for i in range(k)]


def polygon(points, note=None, hl=None, corners=None, dashed=None):
    fig = {"kind": "polygon", "points": points}
    if corners:
        fig["corners"] = corners
    if dashed:
        fig["dashed"] = [{"from": a, "to": b} for a, b in dashed]
    return with_note(fig, note, hl)


def bar(segs, note=None, hl=None, label=None, brace=None):
    """segs: (units, label or None, tone)."""
    one = {"segments": [dict([("units", u), ("tone", t)] + ([("label", lab)] if lab else [])) for u, lab, t in segs]}
    if label:
        one["label"] = label
    if brace:
        one["brace"] = brace
    return with_note({"kind": "barModel", "bars": [one]}, note, hl)


def squares(cols, rows, note=None, hl=None):
    return with_note({"kind": "rectangle", "square": cols == rows, "grid": {"cols": cols, "rows": rows}}, note, hl)


def grid(rows, cols, shaded, note=None):
    return with_note({"kind": "grid", "rows": rows, "cols": cols, "shaded": shaded}, note)


# ── Rule: digits placed in boxes, with the number of choices for each box ────

def slots(qid, heads, before_note, stages, origin="authored"):
    """stages: {step: (cells, note, highlight)}. The before figure is the empty boxes."""
    figs = {}
    for i, (cells, note, hl) in stages.items():
        figs[i] = table(cells, note, heads, hl)
    P.add(qid, table([["?"] * len(heads)], before_note, heads), figs, origin=origin)


PLACES4 = ["Thousands", "Hundreds", "Tens", "Ones"]
for qid in ("EXT_G4_FP_2023_031", "EXT_G4_FP_2025_019"):
    slots(qid, PLACES4, "Each digit is used once. The number must be odd", {
        0: ([["?", "?", "?", "7 or 9"]], "An odd number ends in an odd digit: 2 choices for the ones place", None),
        1: ([["3 choices", "2 choices", "1 choice", "2 choices"]], "The 3 digits left over fill the other places", None),
        2: ([["3 choices", "2 choices", "1 choice", "2 choices"]], "Multiply the choices together", None),
        3: ([["3 choices", "2 choices", "1 choice", "2 choices"]], "3 × 2 × 1 × 2 = 12 odd numbers", None),
    }, origin="rule")
slots("EXT_G4_FP_2024_029", PLACES4, "Each digit is used once. The number must be more than 5000", {
    0: ([["5 or 7", "?", "?", "?"]], "The thousands digit must be 5 or 7: 2 choices", None),
    1: ([["2 choices", "3 choices", "2 choices", "1 choice"]], "The 3 digits left over fill the other places", None),
    2: ([["2 choices", "3 choices", "2 choices", "1 choice"]], "Multiply the choices together", None),
    3: ([["2 choices", "3 choices", "2 choices", "1 choice"]], "2 × 3 × 2 × 1 = 12 numbers", None),
}, origin="rule")
slots("G4A_COUNTING_020", ["Hundreds", "Tens", "Ones"], "Use 2, 0 and 5 once each to make 3-digit numbers", {
    0: ([["2 or 5", "?", "?"]], "The hundreds digit can be 2 or 5, but not 0", None),
})
slots("G4A_COUNTING_030", ["Hundreds", "Tens", "Ones"], "Digits 0, 1, 2 and 3, none repeated. The number must be even", {
    0: ([["3 choices", "2 choices", "0"]], "Ending in 0: the hundreds digit can be 1, 2 or 3", None),
    1: ([["3 choices", "2 choices", "0"], ["2 choices", "2 choices", "2"]], "Ending in 2: the hundreds digit can only be 1 or 3", ["r1"]),
    2: ([["3 choices", "2 choices", "0"], ["2 choices", "2 choices", "2"]], "Multiply along each row, then add the two rows", None),
    3: ([["3 choices", "2 choices", "0"], ["2 choices", "2 choices", "2"]], "The two rows together give 10 numbers", None),
})
slots("G4A_COUNTING_008", ["Tens", "Ones"], "Only the digits 3 and 8. A digit may be used twice", {
    0: ([["3 or 8", "3 or 8"]], "Each place can hold 3 or 8", None),
    1: ([["2 choices", "2 choices"]], "2 choices for each place", None),
    2: ([["3", "3"], ["3", "8"], ["8", "3"], ["8", "8"]], "33, 38, 83 and 88: 4 numbers", None),
})
slots("G4A_COUNTING_040", ["Tens", "Ones"], "Use 4 and 7 once each", {
    0: ([["4", "7"], ["7", "4"]], "4 first makes 47. 7 first makes 74", None),
    1: ([["4", "7"], ["7", "4"]], "No other ways: 2 different numbers", None),
})
slots("G4A_COUNTING_014", ["First", "Second", "Third"], "Anu, Binu and Charu each take one place", {
    0: ([["3 choices", "?", "?"]], "Any of the 3 children can stand first", None),
    1: ([["3 choices", "2 choices", "1 choice"]], "Then 2 children are left, and then 1", None),
    2: ([["3 choices", "2 choices", "1 choice"]], "Multiply the choices", None),
    3: ([["3 choices", "2 choices", "1 choice"]], "3 × 2 × 1 = 6 different orders", None),
})
slots("G4A_COUNTING_039", ["In front", "Behind"], "Anu and Bala: who stands in front?", {
    0: ([["Anu", "Bala"], ["Bala", "Anu"]], "Anu in front, or Bala in front", None),
    1: ([["Anu", "Bala"], ["Bala", "Anu"]], "No other ways: 2 different orders", None),
})
A("G4A_COUNTING_035", {"kind": "rectangle", "grid": {"cols": 3, "rows": 1}, "proportion": 2,
                       "note": "3 stripes: red, green or blue. Stripes that touch must be different"}, {
    0: table([["3 choices", "?", "?"]], "The first stripe can be any of 3 colours", ["Stripe 1", "Stripe 2", "Stripe 3"]),
    1: table([["3 choices", "2 choices", "?"]], "The second stripe must differ from the first", ["Stripe 1", "Stripe 2", "Stripe 3"]),
    2: table([["3 choices", "2 choices", "2 choices"]], "The third must differ only from the second",
             ["Stripe 1", "Stripe 2", "Stripe 3"]),
    3: table([["3 choices", "2 choices", "2 choices"]], "Multiply the choices", ["Stripe 1", "Stripe 2", "Stripe 3"]),
    4: table([["3 choices", "2 choices", "2 choices"]], "3 × 2 × 2 = 12 different flags", ["Stripe 1", "Stripe 2", "Stripe 3"]),
})
A("G4A_COUNTING_045", table([["ABC", "ACB"], ["BAC", "BCA"], ["CAB", "CBA"]], "All six orders. In how many is A first?"), {
    0: table([["ABC", "ACB"], ["BAC", "BCA"], ["CAB", "CBA"]], "The orders that begin with A", hl=["r0"]),
    1: table([["ABC", "ACB"], ["BAC", "BCA"], ["CAB", "CBA"]], "Anu is first in 2 of the orders", hl=["r0"]),
})
A("G4A_COUNTING_005", table([["Top A", "Skirt X"], ["Top B", "Skirt Y"], ["Top C", "–"]], "An outfit is one top with one skirt",
                            ["Tops", "Skirts"]), {
    0: table([["Top A", "with X, with Y"], ["Top B", "?"], ["Top C", "?"]], "Each top can go with either skirt: 2 outfits",
             ["Top", "Outfits"], ["r0"]),
    1: table([["Top A", "with X, with Y"], ["Top B", "with X, with Y"], ["Top C", "with X, with Y"]], "3 tops, with 2 outfits each",
             ["Top", "Outfits"]),
    2: table([["Top A", "with X, with Y"], ["Top B", "with X, with Y"], ["Top C", "with X, with Y"]], "6 different outfits",
             ["Top", "Outfits"]),
})

# ── Points joined in pairs ───────────────────────────────────────────────────

SQUARE = [[2, 2], [10, 2], [10, 10], [2, 10]]
A("EXT_G4_FP_2021_004", polygon(SQUARE, "Each line joins two players. Each pair plays 2 games", corners=list("ABCD"),
                                dashed=[(0, 2), (1, 3)]), {
    0: table([["AB", "AC", "AD"], ["BC", "BD", "CD"]], "6 pairs: one for each line in the picture"),
    1: table([["AB", "AC", "AD"], ["BC", "BD", "CD"]], "Each of the 6 pairs plays 2 games"),
    2: table([["AB", "AC", "AD"], ["BC", "BD", "CD"]], "6 pairs, 2 games each: 12 games"),
})
A("PYQ_2016_Q17", polygon(SQUARE, "Each line joins two players who play each other", corners=list("ABCD"), dashed=[(0, 2), (1, 3)]), {
    0: table([["A and B", "A and C", "A and D"]], "The pairs with A: 3 pairs"),
    1: table([["A and B", "A and C", "A and D"], ["B and C", "B and D"]], "The new pairs with B: 2 more", hl=["r1"]),
    2: table([["A and B", "A and C", "A and D"], ["B and C", "B and D"], ["C and D"]], "The last new pair. 3 + 2 + 1 = 6 pairs",
             hl=["r2"]),
    3: table([["A and B", "A and C", "A and D"], ["B and C", "B and D"], ["C and D"]], "6 pairs, 2 games each: 6 × 2 = 12 games"),
})
A("EXT_G4_FP_2020_026", polygon(ring(8), "The corners are the 8 points. Join every pair, not just neighbours"))
A("PYQ_2019_Q07", polygon(ring(8), "Every pair of points can be joined, not just neighbours", corners=list("ABCDEFGH")), {
    1: table([["A", "7"], ["B", "6"], ["C", "5"], ["…", "…"], ["G", "1"]], "Each point has one fewer new segment than the point before",
             ["From", "New segments"]),
    3: table([["A", "7"], ["B", "6"], ["C", "5"], ["…", "…"], ["G", "1"]], "Adding from 7 down to 1 gives 28", ["From", "New segments"]),
})
A("Q_CH21_013", polygon(ring(5), "5 points on a circle. A chord joins two of them. How many chords?"), {
    0: polygon(ring(5), "From A: chords to B, C, D and E. That is 4 chords", ["e0", "e4"], list("ABCDE"), [(0, 2), (0, 3)]),
    1: polygon(ring(5), "From B: new chords to C, D and E. That is 3 more", ["e1"], list("ABCDE"), [(0, 2), (0, 3), (1, 3), (1, 4)]),
    2: table([["A", "4"], ["B", "3"], ["C", "2"], ["D", "1"]], "From C there are 2 new chords, and from D there is 1", ["From", "New chords"],
             ["r2", "r3"]),
    3: table([["A", "4"], ["B", "3"], ["C", "2"], ["D", "1"]], "4 + 3 + 2 + 1 = 10 chords", ["From", "New chords"]),
})
A("PYQ_2018_Q12", None, {
    0: table([["2", "1"]], "Start with 2 points and 1 segment", ["Points", "Segments"]),
    1: table([["2", "1"], ["3", "3"], ["4", "6"]], "The 3rd point adds 2 segments. The 4th adds 3", ["Points", "Segments"], ["r1", "r2"]),
    2: table([["2", "1"], ["3", "3"], ["4", "6"], ["5", "10"], ["6", "15"]], "The 5th point adds 4. The 6th adds 5",
             ["Points", "Segments"], ["r3", "r4"]),
    3: table([["2", "1"], ["3", "3"], ["4", "6"], ["5", "10"], ["6", "15"]], "15 segments are reached with 6 points",
             ["Points", "Segments"], ["r4"]),
})
A("EXT_G4_FP_2021_014", None, {
    1: table([["2", "1"], ["3", "3"], ["4", "6"]], "Each new point joins to all the points already there", ["Points", "Segments"]),
    2: table([["2", "1"], ["3", "3"], ["4", "6"], ["5", "10"]], "5 points give 10. One more point adds 5 more", ["Points", "Segments"], ["r3"]),
    3: table([["2", "1"], ["3", "3"], ["4", "6"], ["5", "10"], ["6", "15"]], "6 points give 15 segments", ["Points", "Segments"], ["r4"]),
})
FLAVOURS = ["mango", "chocolate", "vanilla", "strawberry"]
A("G4A_COUNTING_019", None, {
    0: polygon(SQUARE, "Mango pairs with each of the other 3 flavours", ["e0", "e3"], FLAVOURS, [(0, 2)]),
    1: polygon(SQUARE, "Chocolate adds 2 new pairs. Vanilla adds 1 new pair", ["e1", "e2"], FLAVOURS, [(0, 2), (1, 3)]),
    2: polygon(SQUARE, "Every line is one pair: 3 + 2 + 1", None, FLAVOURS, [(0, 2), (1, 3)]),
    3: polygon(SQUARE, "6 lines, so 6 different pairs", None, FLAVOURS, [(0, 2), (1, 3)]),
})

# ── Places in a queue ────────────────────────────────────────────────────────

A("G4A_COUNTING_002", bar([(6, "in front", "a"), (1, "M", "b"), (4, "behind", "c")], "Meera (M) is 7th from the front and 5th from the back",
                          brace="? children"), {
    0: bar([(6, "7 − 1", "a"), (1, "M", "b"), (4, "5 − 1", "c")], "In front of Meera: 7 − 1. Behind her: 5 − 1", ["b0s0", "b0s2"]),
    1: bar([(6, "7 − 1", "a"), (1, "M", "b"), (4, "5 − 1", "c")], "Add the two groups, and count Meera herself once", ["b0s1"]),
    2: bar([(6, "7 − 1", "a"), (1, "M", "b"), (4, "5 − 1", "c")], "There are 11 children in the queue", brace="11 children"),
})
A("G4A_COUNTING_012", bar([(11, "in front", "a"), (1, "A", "b"), (18, "behind", "c")], "Arjun (A) is 12th from the front. His place from the back = ?",
                          brace="30 children"), {
    0: bar([(12, "first 12", "a"), (18, "30 − 12 behind", "c")], "Arjun is the last of the first 12. The rest are behind him",
           ["b0s1"], brace="30 children"),
    1: bar([(11, "in front", "a"), (1, "A", "b"), (18, "18 behind", "c")], "From the back: 18 children come first, then Arjun",
           ["b0s1"], brace="30 children"),
    2: bar([(11, "in front", "a"), (1, "A", "b"), (18, "18 behind", "c")], "Arjun is 19th from the back", ["b0s1"], brace="30 children"),
})
A("G4A_COUNTING_022", number_line(1, 15, 14, "ends", [{"at": 8, "label": "Ravi"}, {"at": 15, "label": "Sana"}],
                                  note="Places in the queue, from the front. How many stand between them?"), {
    0: number_line(8, 15, 1, "all", [{"at": x} for x in (9, 10, 11, 12, 13, 14)], note="Places 9 to 14 are between Ravi and Sana",
                   hl=["p0", "p1", "p2", "p3", "p4", "p5"]),
    2: number_line(8, 15, 1, "all", [{"at": x} for x in (9, 10, 11, 12, 13, 14)], note="Count the dots: 6 people stand between them"),
})
A("G4A_COUNTING_032", None, {
    0: bar([(14, "15 − 1", "a"), (1, "T", "b"), (5, "6 − 1", "c")], "Tara's new spot: 15th from the left and 6th from the right", ["b0s1"]),
    1: bar([(14, "15 − 1", "a"), (1, "T", "b"), (5, "6 − 1", "c")], "15 + 6 counts Tara's spot twice, so take away 1"),
    2: bar([(14, "15 − 1", "a"), (1, "T", "b"), (5, "6 − 1", "c")], "There are 20 children in the row", brace="20 children"),
})
A("G4A_COUNTING_041", table([["Asha", "Bina", "Chetan", "Dev", "Esha"]], "The front of the queue is on the left"), {
    0: table([["Asha", "Bina", "Chetan", "Dev", "Esha"]], "Count from the front", ["1st", "2nd", "…", "…", "…"]),
    1: table([["Asha", "Bina", "Chetan", "Dev", "Esha"]], "The next child, Chetan, is 3rd", ["1st", "2nd", "3rd", "…", "…"]),
})
A("G4A_COUNTING_042", None, {
    0: table([["1st", "2nd", "3rd", "Ravi"]], "The places in front of the 4th place"),
    1: table([["1st", "2nd", "3rd", "Ravi"]], "3 children are standing in front of Ravi"),
})
A("G4A_COUNTING_047", number_line(1, 7, 1, "all", note="The chairs are numbered 1 to 7. Which one is exactly in the middle?"), {
    1: number_line(1, 7, 1, "all", [{"at": x} for x in (1, 2, 3, 5, 6, 7)], note="Chairs 1, 2, 3 on one side and 5, 6, 7 on the other"),
    2: number_line(1, 7, 1, "all", [{"at": 4, "label": "middle"}], note="With three chairs on each side, the middle one is Chair 4", hl=["p0"]),
})

# ── Gaps and posts ───────────────────────────────────────────────────────────

A("G4A_COUNTING_003", number_line(0, 40, 40, "ends", [{"at": 0, "label": "post"}, {"at": 40, "label": "post"}],
                                  [{"from": 0, "to": 5, "label": "5 m"}], "A 40 m fence. A post every 5 m, with one at each end"), {
    0: number_line(0, 40, 5, "all", note="Mark every 5 m along the fence. Count the gaps between the marks"),
    1: number_line(0, 40, 5, "all", [{"at": 0, "label": "post"}, {"at": 40, "label": "post"}],
                   note="Every mark is a post, so there is one more post than gaps", hl=["p0", "p1"]),
    2: number_line(0, 40, 5, "all", [{"at": 0, "label": "post"}, {"at": 40, "label": "post"}], note="8 gaps, so 9 posts"),
})
A("G4A_COUNTING_013", {"kind": "rectangle", "square": True, "length": "12 m", "breadth": "12 m",
                       "note": "A post at every corner, and every 3 m along each side"}, {
    0: {"kind": "rectangle", "square": True, "length": "12 m", "breadth": "12 m", "highlight": ["border"],
        "note": "Find the distance all the way around the garden"},
    1: {"kind": "rectangle", "square": True, "length": "12 m", "breadth": "12 m", "highlight": ["border"],
        "note": "Split the whole distance around into gaps of 3 m"},
    2: {"kind": "rectangle", "square": True, "length": "12 m", "breadth": "12 m", "highlight": ["border"],
        "note": "The path closes up, so the last gap ends at the first post"},
    3: {"kind": "rectangle", "square": True, "length": "12 m", "breadth": "12 m",
        "note": "Around a closed loop, 16 gaps need 16 posts"},
})
A("G4A_COUNTING_007", bar([(6, "plank", "a")], "Cut into 6 pieces, one cut at a time. How many cuts?"), {
    0: bar([(3, None, "a"), (3, None, "a")], "It starts as 1 piece. The first cut makes 1 more piece"),
    1: bar([(1, None, "a")] * 6, "6 pieces: 5 more than at the start, so 5 cuts"),
    2: bar([(1, None, "a")] * 6, "Each line inside the plank is one cut: 5 cuts"),
})
A("G4A_COUNTING_018", number_line(1, 7, 1, "all", [{"at": 1}, {"at": 4}, {"at": 7}], [{"from": 1, "to": 4, "label": "48 steps"}],
                                  "Floors 1 to 7. From floor 1 to floor 4 is 48 steps. To floor 7 = ?"), {
    0: number_line(1, 7, 1, "all", [{"at": 1}, {"at": 4}, {"at": 7}], [{"from": 1, "to": 2}, {"from": 2, "to": 3}, {"from": 3, "to": 4}],
                   "From the 1st floor to the 4th there are 3 flights of stairs, not 4", ["h0", "h1", "h2"]),
    1: number_line(1, 7, 1, "all", [{"at": 1}, {"at": 4}, {"at": 7}], [{"from": 1, "to": 2}, {"from": 2, "to": 3}, {"from": 3, "to": 4}],
                   "The 48 steps are shared equally over the 3 flights"),
    2: number_line(1, 7, 1, "all", [{"at": 1}, {"at": 4}, {"at": 7}], [{"from": 1, "to": 7, "label": "6 flights"}],
                   "From the 1st floor to the 7th there are 6 flights", ["h0"]),
    3: number_line(1, 7, 1, "all", [{"at": 1}, {"at": 4}, {"at": 7}], [{"from": 1, "to": 7, "label": "96 steps"}],
                   "6 flights make 96 steps", ["h0"]),
})
_rings = [{"at": x, "label": "ring"} for x in (0, 2, 4, 6)]
A("G4A_COUNTING_031", number_line(0, 6, 2, "ends", _rings, note="4 rings take 6 seconds, from the first ring to the last. 10 rings = ?"), {
    0: number_line(0, 6, 2, "ends", _rings, [{"from": a, "to": a + 2, "label": "gap"} for a in (0, 2, 4)],
                   "4 rings have 3 gaps between them. Each gap is 6 ÷ 3 seconds", ["h0", "h1", "h2"]),
    1: number_line(0, 6, 2, "ends", _rings, [{"from": a, "to": a + 2, "label": "gap"} for a in (0, 2, 4)],
                   "In the same way, 10 rings have 9 gaps between them"),
    3: number_line(0, 18, 2, "ends", [{"at": 0, "label": "1st ring"}, {"at": 18, "label": "10th ring"}],
                   [{"from": 0, "to": 18, "label": "9 gaps"}], "10 rings take 18 seconds", ["h0"]),
})
A("G4A_COUNTING_001", number_line(15, 42, 27, "ends", note="How many whole numbers from 15 to 42, with both ends counted?"), {
    0: number_line(15, 42, 1, "ends", hops=[{"from": 15, "to": 42, "label": "42 − 15 jumps"}], note="Subtract to count the jumps of 1"),
    1: number_line(15, 42, 1, "ends", [{"at": 15, "label": "count me too"}], [{"from": 15, "to": 42, "label": "42 − 15 jumps"}],
                   "The jumps miss the starting number 15, so add 1", ["p0"]),
    2: number_line(15, 42, 1, "ends", note="Every mark is one number: 28 whole numbers from 15 to 42"),
})
A("G4A_COUNTING_038", None, {
    0: number_line(10, 15, 1, "all", [{"at": x} for x in (11, 12, 13, 14)], note="After 10 and before 15: 11, 12, 13, 14",
                   hl=["p0", "p1", "p2", "p3"]),
    1: number_line(10, 15, 1, "all", [{"at": x} for x in (11, 12, 13, 14)], note="Count the dots: 4 whole numbers between 10 and 15"),
})
A("G4A_COUNTING_037", None, {
    0: number_line(6, 10, 1, "all", [{"at": x} for x in (6, 7, 8, 9, 10)], note="Count the numbers one by one: 6, 7, 8, 9, 10"),
    1: number_line(6, 10, 1, "all", [{"at": x} for x in (6, 7, 8, 9, 10)], note="Ria writes 5 numbers"),
})
A("G4A_COUNTING_023", None, {
    0: number_line(100, 200, 10, "all", note="The numbers that end in 0, from 100 to 200"),
    1: number_line(100, 200, 10, "all", [{"at": 100, "label": "start"}], [{"from": 100, "to": 200, "label": "10 jumps of ten"}],
                   "10 jumps, and one more for the starting number", ["p0"]),
    2: number_line(100, 200, 10, "all", note="Every mark is one number: 11 numbers"),
})
A("G4A_COUNTING_017", None, {
    1: number_line(14, 98, 7, "ends", note="The 2-digit multiples of 7 run from 14 to 98, in jumps of 7"),
    3: number_line(14, 98, 7, "ends", note="Every mark is a multiple of 7: 13 of them"),
})
A("G4A_COUNTING_009", None, {
    0: bar([(9, "1 to 9", "a"), (16, "?", "unknown")], "Pages 1 to 9 have one digit each", ["b0s0"], brace="pages 1 to 25"),
    1: bar([(9, "1 to 9", "a"), (16, "10 to 25: 16 pages", "b")], "Pages 10 to 25 have two digits each", ["b0s1"], brace="pages 1 to 25"),
    2: bar([(9, "1 digit each", "a"), (16, "2 digits each", "b")], "Add the digits of the two groups", brace="pages 1 to 25"),
    3: bar([(9, "1 digit each", "a"), (16, "2 digits each", "b")], "In all, 41 digits are printed", brace="41 digits"),
})

# ── Counting shapes inside a shape ───────────────────────────────────────────

A("G4A_COUNTING_015", squares(2, 2, "A window of 4 small panes. Count the squares of every size"), {
    0: grid(2, 2, [[0, 0]], "4 small squares, each like the shaded one"),
    1: grid(2, 2, [[0, 0], [0, 1], [1, 0], [1, 1]], "The whole window, all 4 panes together, is 1 big square"),
    2: squares(2, 2, "Add the small squares and the big square"),
    3: squares(2, 2, "4 small and 1 big: 5 squares"),
})
A("G4A_COUNTING_027", squares(3, 3, "A board of 9 small squares. Count the squares of every size"), {
    0: grid(3, 3, [[0, 0]], "9 small squares, each like the shaded one"),
    1: grid(3, 3, [[0, 0], [0, 1], [1, 0], [1, 1]], "A square 2 wide and 2 tall fits in each corner: 4 of them"),
    2: grid(3, 3, [[r, c] for r in range(3) for c in range(3)], "The whole board is 1 large square"),
    3: squares(3, 3, "Add all the sizes"),
    4: squares(3, 3, "9 small, 4 middle-sized and 1 large: 14 squares"),
})
STRIP = [(1, None, "a")] * 4
A("G4A_COUNTING_028", bar(STRIP, "A strip of small squares in a row. Count rectangles of every size"), {
    0: bar(STRIP, "Rectangles made of 1 square: 4", ["b0s0"]),
    1: bar(STRIP, "2 squares side by side: 3 ways. 3 squares side by side: 2 ways", ["b0s0", "b0s1"]),
    2: bar(STRIP, "The whole strip of 4 squares: 1 more", ["b0"]),
    4: bar(STRIP, "4 + 3 + 2 + 1 = 10 rectangles"),
})
TRI = [[6, 1], [1, 11], [4.33, 11], [7.67, 11], [11, 11]]
A("G4A_COUNTING_021", polygon(TRI, "Two lines from the top corner to the base. Count every triangle", dashed=[(0, 2), (0, 3)]), {
    0: polygon(TRI, "3 small triangles, side by side", ["e1", "e2", "e3"], dashed=[(0, 2), (0, 3)]),
    1: polygon(TRI, "2 neighbours together make a bigger triangle: 2 ways", ["e1", "e2"], dashed=[(0, 2), (0, 3)]),
    2: polygon(TRI, "All three together make the 1 big triangle", ["e0", "e1", "e2", "e3", "e4"], dashed=[(0, 2), (0, 3)]),
    4: polygon(TRI, "3 + 2 + 1 = 6 triangles", dashed=[(0, 2), (0, 3)]),
})

# ── Numbers in one list, the other list, or both ─────────────────────────────

A("G4A_COUNTING_034", venn("Multiples of 2", "Multiples of 3", "?", "?", "?", "Numbers from 1 to 60. How many are inside the circles?"), {
    0: venn("Multiples of 2", "Multiples of 3", "?", "?", "?", "Count each whole circle: multiples of 2, and multiples of 3"),
    1: venn("Multiples of 2", "Multiples of 3", "?", "6, 12, …", "?", "The middle holds the multiples of 6, counted in both circles", ["both"]),
    2: venn("Multiples of 2", "Multiples of 3", "?", "6, 12, …", "?", "Add the two circles, then take the middle away once",
            ["left", "both", "right"]),
    3: venn("Multiples of 2", "Multiples of 3", "?", "6, 12, …", "?", "40 numbers are inside the circles"),
})

P.save()
