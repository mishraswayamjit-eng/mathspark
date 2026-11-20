"""Individually drawn figures for Grade 4 fractions: past papers and hand-written questions.

Each function draws one question. Where a step is given a list, the first figure whose
numbers are already stated at that step is used (see g4_gr4_fractions_lib.entry).
"""
import re

from g4_gr4_fractions_lib import balance, bar, bm, entry, fb, ft, seg, segs, setf, table, w

OWN = {}


def own(qid):
    def deco(fn):
        if qid in OWN:
            raise ValueError("twice: " + qid)
        OWN[qid] = fn
        return fn
    return deco


HALF = ["Fraction", "Top doubled", "Bottom"]


def half_rows(text, wanted):
    """Rows for the 'compare with one half' table, for the fractions named, read from the text."""
    found = [(int(n), int(d)) for n, d in re.findall(r"(\d+)/(\d+)", text)]
    rows = []
    for n, d in wanted:
        if (n, d) not in found:
            raise ValueError("fraction %d/%d is not in the text" % (n, d))
        rows.append([ft(n, d), str(2 * n), str(d)])
    return rows


# ── Past papers ──────────────────────────────────────────────────────────────

@own("EXT_G4_FP_2020_002")
def _(Q):
    before = fb([(9, 1, "1/9"), (18, 1, "1/18")], "1/9 + 1/18 = 1/□")
    return entry(Q, before, [
        fb([(18, 2, "1/9 = 2/18"), (18, 1, "1/18")], "Now both are eighteenths"),
        [fb([(18, 3, "3/18")], "2 + 1 = 3 eighteenths")],
        fb([(18, 3, "3/18"), (6, 1, "1/6")], "The same amount, in bigger pieces", ["b1"]),
        fb([(6, 1, "1/6")], "The box is 6"),
    ])


@own("EXT_G4_FP_2021_002")
def _(Q):
    return entry(Q, fb([(7, 2, "2/7")] * 3, "2/7 + 2/7 + 2/7 = ★/21"), [
        fb([(7, 6, "6/7")], "2 + 2 + 2 = 6 sevenths"),
        fb([(7, 6, "6/7"), (21, 0, "★/21")], "7 × 3 = 21: cut every piece into 3"),
        fb([(7, 6, "6/7"), (21, 18, "18/21")], "The same amount: 18 small pieces", ["b1"]),
        fb([(21, 18, "18/21")], "The star is 18"),
    ])


@own("EXT_G4_FP_2023_014")
def _(Q):
    before = balance("M/14 + M/14 + M/14", "162/126")
    tops = balance("M + M + M", "18", "The bottoms are both 14, so the tops must match")
    return entry(Q, before, [
        [balance("M/14 + M/14 + M/14", "18/14", "162/126 = 18/14"),
         w(before, "Divide 162 and 126 by 9 to get fourteenths")],
        tops,
        w(tops, "Share 18 equally among the three M"),
        balance("M", "6", "M is 6"),
    ])


@own("EXT_G4_FP_2023_025")
def _(Q):
    over = half_rows(Q.text, [(2, 3), (11, 15), (5, 7)])
    full = table(HALF, over + half_rows(Q.text, [(13, 29)]), "26 is less than 29, so 13/29 is less than half", ["r3"])
    return entry(Q, None, [
        None,
        table(HALF, over, "Each doubled top is more than the bottom: more than half"),
        full,
        w(full, "13/29 is the smallest", ["r3"]),
    ])


@own("EXT_G4_FP_2025_003")
def _(Q):
    under = half_rows(Q.text, [(14, 29), (9, 19), (7, 22)])
    full = table(HALF, under + half_rows(Q.text, [(17, 21)]), "34 is more than 21, so 17/21 is more than half", ["r3"])
    return entry(Q, None, [
        None,
        table(HALF, under, "Each doubled top is less than the bottom: less than half"),
        full,
        w(full, "17/21 is the greatest", ["r3"]),
    ])


@own("EXT_G4_FP_2024_005")
def _(Q):
    pieces = fb([(12, 1, "1/12"), (10, 1, "1/10"), (7, 1, "1/7"), (8, 1, "1/8")])
    return entry(Q, None, [
        None,
        w(pieces, "Fewer pieces in the whole means bigger pieces"),
        w(pieces, "7 is the smallest bottom number: the biggest pieces", ["b2"]),
        None,
    ])


@own("EXT_G4_FP_2025_039")
def _(Q):
    before = balance("5/□ + 8/□ + 11/□", "2")
    return entry(Q, before, [
        w(before, "The bottoms are the same, so add the tops"),
        balance("24/□", "2", "5 + 8 + 11 = 24"),
        balance("24/□", "2", "24 divided by which number gives 2?"),
        balance("24/12", "2", "24 ÷ 12 = 2, so the denominator is 12"),
    ])


@own("PYQ_2016_Q08")
def _(Q):
    before = fb([(4, 1, "1/4"), (3, 2, "2/3"), (2, 1, "1/2")], "1/4 + 2/3 − 1/2 = ?")
    five = fb([(12, 5, "5/12")], "3 + 8 − 6 = 5 twelfths")
    return entry(Q, before, [
        w(before, "Cut every strip into 12 equal pieces"),
        fb([(12, 3, "1/4 = 3/12"), (12, 8, "2/3 = 8/12"), (12, 6, "1/2 = 6/12")], "Now every piece is the same size"),
        five,
        w(five, "1/4 + 2/3 − 1/2 = 5/12", ["b0"]),
    ])


@own("PYQ_2016_Q25")
def _(Q):
    groups = setf(12, 4, item="friends", note="Groups of 3 friends: 12 ÷ 3 = 4")
    return entry(Q, fb([(3, 1, "1 friend: 1/3")], "12 friends. How many pizzas?", shape="circle"), [
        fb([(3, 3, "1 pizza: 3 friends")], "Three thirds make one whole pizza", shape="circle"),
        groups,
        w(groups, "4 groups, so 4 pizzas"),
    ])


@own("PYQ_2017_Q03")
def _(Q):
    gaps = fb([(17, 1, "1/17"), (18, 1, "1/18"), (19, 1, "1/19"), (20, 1, "1/20")])
    return entry(Q, None, [
        w(gaps, "The piece each fraction is short of a whole"),
        w(gaps, "1/20 is the smallest of the missing pieces", ["b3"]),
        None,
        fb([(20, 19, "19/20")], "19/20 is the closest to 1, so it is the largest"),
    ])


@own("PYQ_2018_Q35")
def _(Q):
    # The question gives its fractions in words, so the before-figure carries no numbers of its own.
    sixth = fb([(6, 1, "1/6 of the cake")], "The half cut into 3 parts: each is 1/6 of the cake")
    return entry(Q, fb([(2, 1, "after Saturday")], "Shaded: the cake left after Saturday"), [
        fb([(2, 1, "1/2 left")], "After Saturday, half of the cake is left"),
        fb([(2, 1, "the half left"), (3, 1, "1/3 of that half")], "He eats two thirds of the half, so one third of it is left"),
        sixth,
        w(sixth, "1/6 of the cake is left for Monday", ["b0"]),
    ])


# ── G4A: written for the app ─────────────────────────────────────────────────

@own("G4A_FRACTIONS_001")
def _(Q):
    before = fb([(8, 7, "7/8 litre"), (12, 5, "5/12 litre")], "7/8 − 5/12 = ?")
    return entry(Q, before, [
        w(before, "Cut both into 24 equal pieces"),
        [fb([(24, 21, "7/8 = 21/24"), (24, 10, "5/12 = 10/24")], "Now every piece is the same size")],
        None,
        fb([(24, 11, "11/24 litre")], "11/24 litre of lassi is left"),
    ])


@own("G4A_FRACTIONS_002")
def _(Q):
    def ribbon(left, units, tone, note, hl=None):
        return bm([bar([seg("2 2/3 m", units[0], "a"), seg(left, units[1], tone)], label="Ribbon", brace="5 1/4 m")], note, hl)
    return entry(Q, ribbon("?", (1, 1), "unknown", "2 2/3 m is cut off. How long is the ribbon now?"), [
        None, None, None,
        ribbon("2 7/12 m", (2.67, 2.58), "b", "The ribbon is now 2 7/12 m long", ["b0s1"]),
    ])


@own("G4A_FRACTIONS_003")
def _(Q):
    cake = fb([(6, 6, "1 cake = 6 slices")], "47 slices sold. How many cakes?", shape="circle")
    return entry(Q, cake, [
        w(cake, "47 slices, each one sixth of a cake: 47/6"),
        None,
        fb([(6, 6, "7 whole cakes"), (6, 5, "and 5/6 of a cake")], "47 ÷ 6 = 7 remainder 5", shape="circle"),
    ])


@own("G4A_FRACTIONS_005")
def _(Q):
    return entry(Q, None, [
        None, None, None,
        fb([(12, 7, "7/12"), (8, 5, "5/8"), (3, 2, "2/3"), (4, 3, "3/4")], "Smallest at the top, greatest at the bottom"),
    ])


@own("G4A_FRACTIONS_006")
def _(Q):
    order = fb([(4, 3, "Bala 3/4"), (5, 3, "Asha 3/5"), (7, 3, "Dev 3/7"), (10, 3, "Chitra 3/10")])
    return entry(Q, None, [
        None,
        fb([(4, 1, "1/4"), (5, 1, "1/5"), (7, 1, "1/7"), (10, 1, "1/10")], "More pieces in the whole means smaller pieces"),
        w(order, "Longest at the top, shortest at the bottom"),
        w(order, "Asha ran the second longest distance", ["b1"]),
    ])


@own("G4A_FRACTIONS_007")
def _(Q):
    def money(ball, book, left, left_units=8, note=None, hl=None):
        return bm([bar([seg(ball, 9, "a"), seg(book, 8, "b"),
                        seg(left, left_units, "unknown" if left == "?" else "c")], brace="Rs. 240")], note, hl)
    ball = money("Rs. 90", "1/3", "?", note="One eighth is 30, so three eighths is 90", hl=["b0s0"])
    return entry(Q, money("3/8", "1/3", "?", note="Ball 3/8, book 1/3. How much is left?"), [
        ball,
        [money("Rs. 90", "Rs. 80", "?", note="1/3 of 240 = 80", hl=["b0s1"]), w(ball, "Now find 1/3 of 240", ["b0s1"])],
        None,
        money("Rs. 90", "book", "Rs. 70", 7, "Ravi has Rs. 70 left", ["b0s2"]),
    ])


@own("G4A_FRACTIONS_008")
def _(Q):
    def model(label=None, brace="?", note=None, hl=None):
        return bm([bar(segs(3, label, "a"), label="Girls", brace="18"),
                   bar(segs(5, label, "b"), label="Class", brace=brace)], note, hl)
    return entry(Q, model(note="3/5 of the class are girls. Whole class = ?"), [
        model(note="3 equal parts make 18", hl=["b0"]),
        [model("6", note="One part: 18 ÷ 3 = 6"), model(note="One part is 18 ÷ 3", hl=["b0s0"])],
        [model("6", note="The whole class is 5 parts", hl=["b1"]), model(note="The whole class is 5 parts", hl=["b1"])],
        [model("6", "30 children", "5 × 6 = 30 children"), model(None, "30 children", "There are 30 children in the class")],
    ])


@own("G4A_FRACTIONS_009")
def _(Q):
    before = bm([bar([seg("read 2/7", 2, "a"), seg("150 pages", 5, "b")], brace="? pages")],
                "2/7 is read. 150 pages are still to read")

    def sevenths(brace, note, hl=None):
        return bm([bar(segs(2, "30", "a") + segs(5, "30", "b"), brace=brace)], note, hl)
    return entry(Q, before, [
        w(before, "The pages still to read are the rest of the book", ["b0s1"]),
        sevenths("? pages", "5/7 of the book is 150 pages, so 1/7 is 30 pages"),
        sevenths("? pages", "The whole book is seven sevenths", ["b0"]),
        sevenths("210 pages", "The book has 210 pages"),
    ])


@own("G4A_FRACTIONS_010")
def _(Q):
    before = bm([bar([seg("1 5/6", 1, "a"), seg("?", 1, "unknown")], brace="3 1/2")], "3 1/2 − ? = 1 5/6")
    return entry(Q, before, [
        w(before, "The missing number is 3 1/2 − 1 5/6", ["b0s1"]),
        None, None,
        bm([bar([seg("1 5/6", 1.83, "a"), seg("1 2/3", 1.67, "b")], brace="3 1/2")], "1 2/3 must be subtracted", ["b0s1"]),
    ])


@own("G4A_FRACTIONS_011")
def _(Q):
    row = re.search(r"order: ((?:[RBG] )+[RBG]),", Q.text).group(1).split()
    red, blue, green = row.count("R"), row.count("B"), row.count("G")
    if len(row) != 12 or blue != 4:
        raise ValueError("bead row misread")
    return entry(Q, None, [
        table(["Colour", "Beads"], [["Red", str(red)], ["Blue", str(blue)], ["Green", str(green)]], "Count each colour in the row", ["r1"]),
        fb([(12, blue, "%d/12 are blue" % blue)], "%d blue beads out of 12" % blue),
        fb([(12, blue, "%d/12" % blue), (3, 1, "1/3")], "Divide the top and bottom by 4", ["b1"]),
        fb([(3, 1, "1/3 are blue")]),
    ])


@own("G4A_FRACTIONS_013")
def _(Q):
    before = fb([(2, 1, "1/2 litre"), (4, 3, "3/4 litre"), (8, 5, "5/8 litre")], "How much in all?")
    return entry(Q, before, [
        [fb([(8, 4, "1/2 = 4/8"), (8, 6, "3/4 = 6/8"), (8, 5, "5/8")], "Now all three are eighths"),
         w(before, "Change 1/2 and 3/4 to eighths", ["b0", "b1"])],
        None,
        fb([(8, 8, "8/8 = 1 litre"), (8, 7, "7/8 litre")], "15/8 is 8/8 and 7/8 more: 1 7/8 litres"),
    ])


@own("G4A_FRACTIONS_014")
def _(Q):
    return entry(Q, None, [
        None, None,
        bm([bar([seg("90 min", 1, "a")] + segs(3, None, "b"), brace="360 min")],
           "90 minutes fits into 360 minutes four times", ["b0s0"]),
        fb([(4, 1, "1/4 of the day")], "Maths takes 1/4 of the school day"),
    ])


@own("G4A_FRACTIONS_015")
def _(Q):
    between = fb([(12, 4, "1/3 = 4/12"), (12, 5, "5/12"), (12, 6, "1/2 = 6/12")])
    return entry(Q, None, [
        [fb([(12, 4, "1/3 = 4/12"), (12, 6, "1/2 = 6/12")], "Both written in twelfths")],
        w(between, "5/12 is more than 4/12 and less than 6/12", ["b1"]),
        w(between, "5/12 lies between 1/3 and 1/2", ["b1"]),
    ])


@own("G4A_FRACTIONS_016")
def _(Q):
    def cloth(brace, note, hl=None):
        return bm([bar([seg("2 3/4 m", 2.75, "a"), seg("1 5/6 m", 1.83, "b")], brace=brace)], note, hl)
    return entry(Q, cloth("? m", "Kurta and shirt together"), [
        None, None, None,
        cloth("4 7/12 m", "3 + 1 7/12 = 4 7/12 m of cloth", ["b0"]),
    ])


@own("G4A_FRACTIONS_017")
def _(Q):
    return entry(Q, fb([(4, 0)] * 3, "3 pizzas shared equally among 4 children", shape="circle"), [
        fb([(4, 1)] * 3, "One quarter of each pizza: 3/4 of a pizza for each child", shape="circle"),
        fb([(4, 3, "3/4"), (8, 6, "6/8")], "Cut each quarter into two eighths"),
        fb([(8, 6, "the share: 6/8"), (8, 3, "eaten: 3/8")], "Half of 6 eighths is 3 eighths", ["b1"]),
    ])


@own("G4A_FRACTIONS_019")
def _(Q):
    before = bm([bar([seg("35 bowled", 1, "a"), seg("?", 1, "unknown")], brace="50 overs")],
                "What fraction is still to be bowled?")
    return entry(Q, before, [
        [bm([bar([seg("35 bowled", 7, "a"), seg("15 left", 3, "b")], brace="50 overs")], "50 − 35 = 15 overs", ["b0s1"]),
         w(before, "Overs left = 50 − 35", ["b0s1"])],
        None, None,
        fb([(10, 3, "3/10 still to bowl")], "3/10 of the overs is still to be bowled"),
    ])


@own("G4A_FRACTIONS_020")
def _(Q):
    def box(brace, note, hl=None):
        return bm([bar([seg("2/3", 2, "a"), seg("3/4", 2.25, "b")], brace=brace)], note, hl)
    return entry(Q, box("□", "Take 2/3 away from the box and 3/4 is left"), [
        box("□", "So the box is 3/4 + 2/3", ["b0"]),
        None, None,
        box("1 5/12", "17/12 is one whole and 5/12"),
    ])


@own("G4A_FRACTIONS_021")
def _(Q):
    before = bm([bar([seg("books", 2, "a"), seg("pen", 1, "b"), seg("Rs. 90", 3, "c")], brace="?")],
                "Books: 1/3 of the money. Pen: 1/4 of the rest")
    quarters = bm([bar([seg("books", 2, "a"), seg("Rs. 30", 1, "b")] + segs(3, "Rs. 30", "c"), brace="?")],
                  "3/4 of the rest is Rs. 90, so 1/4 of it is Rs. 30")
    thirds = [seg("Rs. 60", 2, "a"), seg("Rs. 60", 2, "b"), seg("Rs. 60", 2, "b")]
    return entry(Q, before, [
        quarters,
        [bm([bar([seg("books", 2, "a"), seg("Rs. 120", 4, "b")], brace="?")], "4 quarters: 4 × 30 = Rs. 120 left after the books"),
         w(quarters, "The money left after the books was 4 quarters", ["b0s1", "b0s2", "b0s3", "b0s4"])],
        bm([bar(thirds, brace="?")], "Rs. 120 is 2/3 of the money, so 1/3 is Rs. 60", ["b0s1", "b0s2"]),
        bm([bar(thirds, brace="Rs. 180")], "3 × 60 = Rs. 180 at first"),
    ])


@own("G4A_FRACTIONS_022")
def _(Q):
    def basket(brace, note):
        return bm([bar([seg("ripe 2/5", 6, "a"), seg("raw 1/3", 5, "b"), seg("16", 4, "c")], brace=brace)], note)
    return entry(Q, basket("? mangoes", "The remaining 16 mangoes are half-ripe"), [
        None, None,
        bm([bar([seg("ripe", 6, "a"), seg("raw", 5, "b")] + segs(4, "4", "c"), brace="? mangoes")],
           "4/15 of the basket is 16 mangoes, so 1/15 is 4", ["b0s2", "b0s3", "b0s4", "b0s5"]),
        basket("60 mangoes", "15 × 4 = 60 mangoes"),
    ])


@own("G4A_FRACTIONS_025")
def _(Q):
    head = ["When", "Water"]
    rows = [["At the start", "10 litres"], ["Morning", "3 3/4 used"], ["Afternoon", "2 5/8 used"], ["Evening", "1 1/2 poured in"]]
    return entry(Q, table(head, rows, "How much water is in the tank now?"), [
        None, None, None,
        table(head, rows + [["Now", "5 1/8 litres"]], hl=["r4"]),
    ])


@own("G4A_FRACTIONS_026")
def _(Q):
    def rope(brace, note, hl=None):
        return bm([bar([seg("1/3", 4, "a"), seg("10 m", 5, "b"), seg("1/4 left", 3, "c")], brace=brace)], note, hl)
    return entry(Q, rope("? m", "How long was the rope at first?"), [
        rope("? m", "The first piece is 1/3 and the piece left is 1/4 of the rope", ["b0s0", "b0s2"]),
        rope("? m", "The 10 m piece is the other part of the rope", ["b0s1"]),
        bm([bar([seg("1/3", 4, "a")] + segs(5, "2 m", "b") + [seg("1/4", 3, "c")], brace="? m")],
           "5/12 of the rope is 10 m, so 1/12 is 2 m"),
        rope("24 m", "12 × 2 = 24 m"),
    ])


@own("G4A_FRACTIONS_028")
def _(Q):
    def share(pieces, note, hl=None):
        return bm([bar([seg(*p) for p in pieces], brace="72 marbles")], note, hl)
    return entry(Q, share([("Arun 1/4", 1, "a"), ("what is left", 3, "unknown")], "Bina takes 2/3 of what is left. Chetan gets the rest"), [
        share([("Arun 18", 1, "a"), ("?", 3, "unknown")], "1/4 of 72 = 18", ["b0s0"]),
        share([("Arun 18", 1, "a"), ("54 left", 3, "b")], "72 − 18 = 54", ["b0s1"]),
        share([("Arun 18", 1, "a"), ("Bina 36", 2, "b"), ("?", 1, "unknown")], "2/3 of 54 = 36", ["b0s1"]),
        share([("Arun 18", 1, "a"), ("Bina 36", 2, "b"), ("Chetan 18", 1, "c")], "54 − 36 = 18", ["b0s2"]),
        bm([bar(segs(2, "18", "b"), label="Bina"), bar(segs(1, "18", "c"), label="Chetan")], "36 − 18 = 18 more for Bina", ["b0s1"]),
    ])


@own("G4A_FRACTIONS_029")
def _(Q):
    under = half_rows(Q.text, [(5, 11), (9, 20), (49, 100)])
    full = table(HALF, under + half_rows(Q.text, [(7, 13), (13, 25), (8, 15)]),
                 "These doubled tops are more than the bottoms", ["r3", "r4", "r5"])
    return entry(Q, None, [
        None,
        table(HALF, under, "Each doubled top is less than the bottom: less than 1/2"),
        full,
        w(full, "3 of the fractions are greater than 1/2", ["r3", "r4", "r5"]),
    ])


@own("G4A_FRACTIONS_030")
def _(Q):
    before = bm([bar([seg(None, 6.5, "a")], label="Ribbon", brace="6 1/2 m"),
                 bar([seg("3/4 m", 0.75, "b")], label="One gift")], "As many gifts as she can. How much is left over?")

    def used(last, tone, note):
        return bm([bar(segs(8, None, "b", 0.75) + [seg(last, 0.5, tone)], brace="6 1/2 m")], note, ["b0s8"])
    return entry(Q, before, [
        bm([bar(segs(4, "3/4 m", "b", 0.75), brace="3 m")], "4 gifts use 3 m of ribbon"),
        bm([bar(segs(8, "3/4 m", "b", 0.75), brace="6 m")], "8 gifts use 6 m. A ninth gift does not fit"),
        used("?", "unknown", "8 gifts use 6 m of the 6 1/2 m"),
        used("1/2 m", "c", "1/2 m of ribbon is left over"),
    ])


@own("G4A_FRACTIONS_031")
def _(Q):
    return entry(Q, fb([(2, 1, "1/2"), (4, 1, "1/4"), (8, 1, "1/8"), (16, 1, "1/16")], "What must be added to make exactly 1?"), [
        fb([(16, 15, "15/16")], "8 + 4 + 2 + 1 = 15 sixteenths"),
        fb([(16, 15, "15/16"), (16, 16, "16/16 = 1")], "One whole is 16/16"),
        fb([(16, 15, "15/16"), (16, 1, "1/16")], "15/16 + 1/16 = 16/16", ["b1"]),
    ])


@own("G4A_FRACTIONS_032")
def _(Q):
    before = bm([bar(segs(5, None, "a"), label="Boys"), bar(segs(4, None, "b"), label="Girls")],
                "5/9 are boys. There are 40 more boys than girls")

    def model(every, note, hl=None):
        return bm([bar(segs(4, every, "a") + [seg("40", 1, "c")], label="Boys"),
                   bar(segs(4, every, "b"), label="Girls")], note, hl)
    return entry(Q, before, [
        w(before, "Boys are 5 of the 9 parts. Girls are the rest"),
        model(None, "The gap between boys and girls is one part", ["b0s4"]),
        model(None, "So 1/9 of the school is 40 pupils", ["b0s4"]),
        model("40", "9 × 40 = 360 pupils"),
    ])


@own("G4A_FRACTIONS_033")
def _(Q):
    return entry(Q, None, [
        None, None, None,
        fb([(24, 6, "1/4 = 6/24"), (24, 11, "11/24"), (24, 16, "2/3 = 16/24")], "11/24 is 5/24 away from each", ["b1"]),
    ])


@own("G4A_FRACTIONS_034")
def _(Q):
    head = ["People", "Cups of rice"]
    return entry(Q, table(head, [["4", "1 1/2"], ["10", "?"]]), [
        table(head, [["4", "1 1/2"], ["4", "1 1/2"], ["2", "?"]], "10 people = 4 + 4 + 2 people"),
        table(head, [["8", "3"], ["2", "?"]], "4 people need 1 1/2 cups, so 8 people need 3 cups", ["r0"]),
        table(head, [["8", "3"], ["2", "3/4"]], "Half of 1 1/2 cups is 3/4 cup", ["r1"]),
        table(head, [["8", "3"], ["2", "3/4"], ["10", "3 3/4"]], "3 + 3/4 = 3 3/4 cups", ["r2"]),
    ])


@own("G4A_FRACTIONS_035")
def _(Q):
    t = table(["Girl", "Done", "In 36ths"], [["Asha", "5/6", "30/36"], ["Bela", "7/9", "28/36"], ["Charu", "3/4", "27/36"]])
    return entry(Q, None, [
        w(t, "All three written in thirty-sixths"),
        w(t, "Asha has done the most and Charu the least", ["r0", "r2"]),
        w(t, "30/36 − 27/36 = 3/36", ["r0", "r2"]),
        w(t, "3/36 = 1/12 of the homework", ["r0", "r2"]),
    ])


# ── Q_CH07: hand-written chapter questions ───────────────────────────────────

@own("Q_CH07_002")
def _(Q):
    sevenths = fb([(7, 3, "3/7"), (7, 5, "5/7"), (7, 2, "2/7"), (7, 6, "6/7")])
    return entry(Q, None, [
        w(sevenths, "Every piece is one seventh, so the pieces are the same size"),
        w(sevenths, "6 is the biggest top number: the most pieces", ["b3"]),
        w(sevenths, "6/7 is the largest", ["b3"]),
    ])


@own("Q_CH07_003")
def _(Q):
    return entry(Q, None, [
        None,
        fb([(4, 1, "1/4"), (8, 1, "1/8"), (5, 1, "1/5"), (2, 1, "1/2")], "More pieces in the whole means smaller pieces", ["b1"]),
        fb([(4, 3, "3/4"), (8, 3, "3/8"), (5, 3, "3/5")], "3 eighths is the least amount", ["b1"]),
    ])


@own("Q_CH07_004")
def _(Q):
    mixed = fb([(5, 5)] * 3 + [(5, 2)])
    return entry(Q, w(mixed, "3 2/5 = ?/5"), [
        w(mixed, "Each whole is 5 fifths: 3 × 5 = 15 fifths", ["b0", "b1", "b2"]),
        w(mixed, "15 + 2 = 17 fifths", ["b3"]),
        w(mixed, "3 2/5 = 17/5"),
    ])


@own("Q_CH07_006")
def _(Q):
    return entry(Q, fb([(8, 3, "3/8"), (8, 5, "5/8")]), [
        fb([(8, 8, "8/8")], "3 + 5 = 8 eighths", ["b0"]),
        fb([(8, 8, "8/8 = 1")], "8 eighths make one whole", ["b0"]),
    ])


@own("Q_CH07_007")
def _(Q):
    before = fb([(3, 1, "1/3"), (4, 1, "1/4")])
    return entry(Q, before, [
        w(before, "Different sizes. Cut both into 12 equal pieces"),
        fb([(12, 4, "1/3 = 4/12"), (12, 3, "1/4 = 3/12")], "Now every piece is the same size"),
        fb([(12, 7, "7/12")], "4 + 3 = 7 twelfths", ["b0"]),
    ])


@own("Q_CH07_008")
def _(Q):
    return entry(Q, fb([(6, 5, "5/6"), (3, 1, "1/3")], "5/6 − 1/3 = ?"), [
        fb([(6, 5, "5/6"), (6, 2, "1/3 = 2/6")], "Now both are sixths", ["b1"]),
        fb([(6, 3, "3/6")], "5 − 2 = 3 sixths", ["b0"]),
        fb([(6, 3, "3/6"), (2, 1, "1/2")], "The same amount, in bigger pieces", ["b1"]),
    ])


@own("Q_CH07_009")
def _(Q):
    before = bm([bar(segs(3, None, "a") + segs(2, None, "b"), brace="10")], "3/5 of 10 = ?")
    three = setf(10, 5, 3, note="3 groups of 2: 3 × 2 = 6", hl=["shaded"])
    return entry(Q, before, [
        setf(10, 5, note="10 shared into 5 equal groups: 2 in each"),
        three,
        w(three, "3/5 × 10 = 6", ["shaded"]),
    ])


@own("Q_CH07_010")
def _(Q):
    before = bm([bar(segs(2, None, "a") + segs(1, None, "b"), brace="45")], "2/3 of 45 = ?")
    two = setf(45, 3, 2, note="Two thirds is 2 of these groups", hl=["shaded"])
    return entry(Q, before, [
        setf(45, 3, note="45 shared into 3 equal groups: 15 in each"),
        two,
        w(two, "2 groups of 15 make 30", ["shaded"]),
    ])


@own("Q_CH07_011")
def _(Q):
    pair = fb([(4, 3, "3/4"), (8, 6, "6/8")])
    return entry(Q, fb([(4, 3, "3/4")], "Which fraction is the same amount?"), [
        None,
        w(pair, "Each piece is cut into 2: 3 × 2 = 6 and 4 × 2 = 8"),
        w(pair, "6/8 is the same amount as 3/4", ["b1"]),
    ])


@own("Q_CH07_012")
def _(Q):
    before = fb([(24, 18, "18/24")])
    pair = fb([(24, 18, "18/24"), (4, 3, "3/4")])
    return entry(Q, before, [
        w(before, "6 divides both 18 and 24"),
        w(pair, "18 ÷ 6 = 3 and 24 ÷ 6 = 4"),
        w(pair, "The same amount, in bigger pieces", ["b1"]),
    ])


@own("Q_CH07_013")
def _(Q):
    return entry(Q, fb([(5, 2, "Riya: 2/5")], "1/5 was left over. What fraction did the others eat?", shape="circle"), [
        fb([(5, 5, "whole pizza: 5/5")], shape="circle"),
        fb([(5, 3, "2/5 + 1/5 = 3/5")], "Riya's share and the leftover together", shape="circle"),
        None,
        fb([(5, 2, "the others: 2/5")], "5/5 − 3/5 = 2/5", shape="circle"),
    ])


@own("Q_CH07_014")
def _(Q):
    return entry(Q, None, [
        None,
        fb([(12, 8, "2/3 = 8/12"), (12, 9, "3/4 = 9/12"), (12, 10, "5/6 = 10/12"), (12, 6, "1/2 = 6/12")], "Now every piece is the same size"),
        fb([(12, 6, "6/12"), (12, 8, "8/12"), (12, 9, "9/12"), (12, 10, "10/12")], "Smallest at the top"),
        fb([(12, 6, "1/2"), (12, 8, "2/3"), (12, 9, "3/4"), (12, 10, "5/6")], "In ascending order"),
    ])


@own("Q_CH07_015")
def _(Q):
    block = {"kind": "grid", "rows": 3, "cols": 5, "shaded": [[r, c] for r in range(2) for c in range(3)],
             "note": "2 of the 3 rows and 3 of the 5 columns: 6 of the 15 squares"}
    return entry(Q, None, [
        block,
        fb([(15, 6, "6/15")], "6 ÷ 3 = 2 and 15 ÷ 3 = 5"),
        fb([(15, 6, "6/15"), (5, 2, "2/5")], "The same amount, in bigger pieces", ["b1"]),
    ])


@own("Q_CH07_016")
def _(Q):
    return entry(Q, None, [
        None,
        fb([(3, 1, "1/3"), (3, 2, "2/3"), (3, 3, "3/3 = 1 whole")], "1/3 + 2/3 = 3/3, which is one whole", ["b2"]),
        None,
    ])


@own("Q_CH07_018")
def _(Q):
    opts = " ".join(o["text"] for o in Q.q["options"])
    over = half_rows(opts, [(3, 4), (5, 6), (7, 8)])
    full = table(HALF, over + half_rows(opts, [(1, 4)]), "2 is smaller than 4, so 1/4 is less than half", ["r3"])
    return entry(Q, None, [
        None,
        table(HALF, over, "Each doubled top is bigger than the bottom: more than half"),
        full,
        w(full, "1/4 lies between 0 and 1/2", ["r3"]),
    ])


@own("Q_CH07_020")
def _(Q):
    before = fb([(4, 3, "3/4 full"), (3, 1, "1/3 used")], "What fraction is left?")
    return entry(Q, before, [
        w(before, "Different sizes. Cut both into 12 equal pieces"),
        [fb([(12, 9, "3/4 = 9/12"), (3, 1, "1/3")], "3/4 in twelfths", ["b0"])],
        [fb([(12, 9, "3/4 = 9/12"), (12, 4, "1/3 = 4/12")], "1/3 in twelfths", ["b1"])],
        None,
        fb([(12, 5, "5/12 left")], "5/12 of the tank is left"),
    ])


@own("Q_CH07_021")
def _(Q):
    before = fb([(8, 5, "5/8"), (5, 3, "3/5")])
    return entry(Q, None, [
        w(before, "Pieces of different sizes. Use 40 as the common bottom"),
        None, None,
        fb([(8, 5, "5/8 = 25/40"), (5, 3, "3/5 = 24/40")], "25/40 is more than 24/40", ["b0"]),
    ])


@own("Q_CH07_022")
def _(Q):
    wholes = fb([(3, 3)] * 4)
    return entry(Q, w(wholes, "4 wholes = ?/3"), [
        fb([(3, 3, "1 whole = 3/3")]),
        w(wholes, "4 wholes are 12 thirds"),
        w(wholes, "4 = 12/3"),
    ])


@own("Q_CH07_023")
def _(Q):
    return entry(Q, None, [
        None,
        fb([(24, 8, "8/24 of a day")], "8 hours out of 24 hours"),
        fb([(24, 8, "8/24"), (3, 1, "1/3")], "Divide the top and bottom by 8", ["b1"]),
        fb([(3, 1, "1/3 of a day")]),
    ])


@own("Q_CH07_024")
def _(Q):
    def rope(label, note, hl=None):
        return bm([bar(segs(3, label, "a") + segs(1, label, "b"), brace="20 m")], note, hl)
    used = ["b0s0", "b0s1", "b0s2"]
    return entry(Q, rope(None, "3/4 of the rope is used"), [
        rope("5 m", "One quarter of 20 m is 5 m"),
        rope("5 m", "Three quarters is 3 of these parts", used),
        rope("5 m", "15 m of the rope is used", used),
    ])
