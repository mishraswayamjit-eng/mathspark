"""Individually drawn figures for Grade 4 ratio and proportion.

Each function draws one question. Where a step is given a list, the first figure whose
numbers are already stated at that step is used (see g4_gr4_fractions_lib.entry).
"""
from g4_gr4_fractions_lib import bar, bm, entry, nline, seg, segs, table, w

OWN = {}


def own(qid):
    def deco(fn):
        if qid in OWN:
            raise ValueError("twice: " + qid)
        OWN[qid] = fn
        return fn
    return deco


def unitary(Q, head, given, unit, asked, answer, notes, mid=None):
    """Unitary method as a table: the given row, the row for one, the row asked for.

    `mid` is an optional extra step that rewrites the asked row (e.g. 1 hour as 60 minutes).
    """
    before = table(head, [given, asked])
    steps = [table(head, [given, unit, asked], notes[0], ["r1"])]
    if mid:
        asked = mid[0]
        steps.append(table(head, [given, unit, asked], mid[1], ["r2"]))
    done = table(head, [given, unit, answer], notes[1], ["r2"])
    steps += [done, w(done, notes[2], ["r2"])]
    return entry(Q, before, steps[:Q.n])


def simplest(names, a, b, g):
    """Two bars in proportion, whole and then cut into pieces of size g."""
    whole = bm([bar([seg(str(a), a // g, "a")], label=names[0]), bar([seg(str(b), b // g, "b")], label=names[1])])
    cut = bm([bar(segs(a // g, str(g), "a"), label=names[0]), bar(segs(b // g, str(g), "b"), label=names[1])])
    return whole, cut


@own("G4A_RATIO_001")
def _(Q):
    whole, cut = simplest(("Boys", "Girls"), 12, 18, 6)
    return entry(Q, w(whole, "Boys to girls in its simplest form = ?"), [
        w(whole, "Boys to girls is 12 : 18"),
        w(cut, "12 ÷ 6 = 2 and 18 ÷ 6 = 3"),
        w(cut, "2 parts to 3 parts: 2 : 3"),
    ])


@own("G4A_RATIO_002")
def _(Q):
    whole, cut = simplest(("First number", "Second number"), 20, 35, 5)
    return entry(Q, w(whole, "20 : 35 in its simplest form = ?"), [
        w(whole, "5 divides both 20 and 35"),
        w(cut, "20 ÷ 5 = 4 and 35 ÷ 5 = 7"),
        w(cut, "4 parts to 7 parts: 4 : 7"),
    ])


@own("G4A_RATIO_003")
def _(Q):
    def books(label, note, hl=None):
        return bm([bar(segs(4, label, "a"), brace="₹ 60")], note, hl)
    return entry(Q, books(None, "4 notebooks. 1 notebook = ?"), [
        books(None, "All 4 cost the same, so divide by 4"),
        books("₹ 15", "60 ÷ 4 = 15"),
        books("₹ 15", "1 notebook costs ₹ 15", ["b0s0"]),
    ])


@own("G4A_RATIO_004")
def _(Q):
    def balls(brace, note, hl=None):
        return bm([bar(segs(3, None, "a") + segs(5, None, "b"), brace=brace)], note, hl)
    red = ["b0s0", "b0s1", "b0s2"]
    return entry(Q, balls(None, "3 red balls and 5 blue balls. Red to all = ?"), [
        balls("8 balls", "3 + 5 = 8 balls in all"),
        balls("8 balls", "Red balls come first, then all the balls", red),
        balls("8 balls", "Red to all is 3 : 8", red),
    ])


@own("G4A_RATIO_005")
def _(Q):
    head = ["First", "Second"]
    done = table(head, [["2", "3"], ["6", "9"]], "2 × 3 = 6 and 3 × 3 = 9", ["r1"])
    return entry(Q, None, [
        table(head, [["2", "3"], ["2 × 3", "3 × 3"]], "Multiply both numbers by 3"),
        done,
        w(done, "6 : 9 is equal to 2 : 3", ["r1"]),
    ])


@own("G4A_RATIO_006")
def _(Q):
    head = ["Lemon juice", "Water"]
    before = table(head, [["1 cup", "4 cups"], ["3 cups", "?"]])
    return entry(Q, before, [
        w(before, "The juice is 3 times as much as before", ["r1"]),
        w(before, "So the water must be 3 times as much too", ["r1"]),
        table(head, [["1 cup", "4 cups"], ["3 cups", "12 cups"]], "4 × 3 = 12 cups of water", ["r1"]),
    ])


@own("G4A_RATIO_007")
def _(Q):
    one = nline(0, 3, 1, hops=[(0, 1, "60 km")])
    three = nline(0, 3, 1, hops=[(0, 1, "60 km"), (1, 2, "60 km"), (2, 3, "60 km")])
    return entry(Q, w(one, "Hours along the line. Distance in 3 hours = ?"), [
        w(one, "In 1 hour the car travels 60 km", ["h0"]),
        w(three, "3 times as far: 60 × 3 = 180"),
        w(three, "It travels 180 km in 3 hours"),
    ])


@own("G4A_RATIO_008")
def _(Q):
    head = ["Money", "Samosas"]
    before = table(head, [["₹ 10", "2"], ["₹ 50", "?"]])
    done = table(head, [["₹ 10", "2"], ["₹ 50", "10"]], "5 times as many samosas: 2 × 5 = 10", ["r1"])
    return entry(Q, before, [
        w(before, "50 ÷ 10 = 5, so ₹ 50 is 5 times as much money", ["r1"]),
        done,
        w(done, "₹ 50 buys 10 samosas", ["r1"]),
    ])


@own("G4A_RATIO_009")
def _(Q):
    # No figure before answering: the parts could simply be counted.
    parts = bm([bar(segs(3, None, "a"), label="First child"), bar(segs(7, None, "b"), label="Second child")])
    return entry(Q, None, [
        w(parts, "3 parts for the first child and 7 for the second"),
        w(parts, "3 + 7 = 10"),
        w(parts, "10 equal parts altogether"),
    ])


@own("G4A_RATIO_010")
def _(Q):
    before = bm([bar([seg(None, 7, "a")], label="Cloth", brace="14 m"), bar([seg("2 m", 1, "b")], label="1 shirt")],
                "How many shirts can he make?")
    cut = bm([bar(segs(7, "2 m", "b"), label="Cloth", brace="14 m")])
    return entry(Q, before, [
        w(before, "Each shirt needs 2 metres of cloth", ["b1"]),
        w(cut, "14 ÷ 2 = 7"),
        w(cut, "He can make 7 shirts"),
    ])


@own("G4A_RATIO_011")
def _(Q):
    whole = bm([bar([seg("50", 1, "a")], label="50 paise"), bar([seg("200", 4, "b")], label="₹ 2")])
    cut = bm([bar([seg("50", 1, "a")], label="50 paise"), bar(segs(4, "50", "b"), label="₹ 2")])
    return entry(Q, None, [
        None,
        w(whole, "In paise the ratio is 50 : 200"),
        w(cut, "50 ÷ 50 = 1 and 200 ÷ 50 = 4"),
        w(cut, "1 part to 4 parts: 1 : 4"),
    ])


@own("G4A_RATIO_012")
def _(Q):
    before = bm([bar([seg("8 girls", 1, "a"), seg("boys ?", 1, "unknown")], brace="20 children")], "Girls to boys = ?")
    whole, cut = simplest(("Girls", "Boys"), 8, 12, 4)
    return entry(Q, before, [
        bm([bar([seg("8 girls", 2, "a"), seg("12 boys", 3, "b")], brace="20 children")], "20 − 8 = 12 boys", ["b0s1"]),
        w(whole, "Girls to boys is 8 : 12"),
        w(cut, "8 ÷ 4 = 2 and 12 ÷ 4 = 3"),
        w(cut, "2 parts to 3 parts: 2 : 3"),
    ])


@own("G4A_RATIO_013")
def _(Q):
    return unitary(Q, ["Rice", "Cost"], ["5 kg", "₹ 300"], ["1 kg", "₹ 60"], ["8 kg", "?"], ["8 kg", "₹ 480"],
                   ["300 ÷ 5 = 60 rupees for 1 kg", "8 times as much: 60 × 8 = 480", "8 kg of rice cost ₹ 480"])


@own("G4A_RATIO_014")
def _(Q):
    def share(label, chetan, note, hl=None):
        return bm([bar(segs(1, label, "a"), label="Amit"), bar(segs(2, label, "b"), label="Bina"),
                   bar(segs(3, label, "c"), label="Chetan", brace=chetan)], note, hl)
    return entry(Q, share(None, "?", "₹ 120 is shared in the ratio 1 : 2 : 3"), [
        share(None, "?", "1 + 2 + 3 = 6 equal parts"),
        share("₹ 20", "?", "One part: 120 ÷ 6 = 20 rupees"),
        share("₹ 20", "?", "Chetan gets 3 parts: 3 × 20 = 60", ["b2"]),
        share("₹ 20", "₹ 60", "Chetan gets ₹ 60", ["b2"]),
    ])


@own("G4A_RATIO_015")
def _(Q):
    def box(label, pens, note, hl=None):
        return bm([bar(segs(4, label, "a"), label="Pencils", brace="28"),
                   bar(segs(3, label, "b"), label="Pens", brace=pens)], note, hl)
    return entry(Q, box(None, "?", "Pencils to pens = 4 : 3. How many altogether?"), [
        box("7", "?", "One part: 28 ÷ 4 = 7", ["b0"]),
        box("7", "21", "Pens are 3 parts: 3 × 7 = 21", ["b1"]),
        box("7", "21", "Altogether: 28 + 21 = 49"),
        box("7", "21", "49 pencils and pens altogether"),
    ])


@own("G4A_RATIO_016")
def _(Q):
    return unitary(Q, ["Distance", "Time"], ["240 km", "4 hours"], ["60 km", "1 hour"], ["420 km", "?"], ["420 km", "7 hours"],
                   ["240 ÷ 4 = 60 km in 1 hour", "420 ÷ 60 = 7", "The train takes 7 hours"])


@own("G4A_RATIO_017")
def _(Q):
    return unitary(Q, ["People", "Flour"], ["6", "300 g"], ["1", "50 g"], ["4", "?"], ["4", "200 g"],
                   ["For 1 person: 300 ÷ 6 = 50 grams", "For 4 people: 50 × 4 = 200", "200 grams of flour are needed"])


@own("G4A_RATIO_018")
def _(Q):
    def share(label, note, hl=None):
        return bm([bar(segs(4, label, "a"), label="Kiran"), bar(segs(5, label, "b"), label="Leela")], note, hl)
    return entry(Q, share(None, "45 mangoes are shared in the ratio 4 : 5"), [
        share(None, "4 + 5 = 9 equal parts"),
        share("5", "One part: 45 ÷ 9 = 5 mangoes"),
        share("5", "Leela has 5 parts and Kiran has 4: 1 part more", ["b1s4"]),
        share("5", "Leela gets 5 more mangoes", ["b1s4"]),
    ])


@own("G4A_RATIO_019")
def _(Q):
    return unitary(Q, ["On the map", "Really"], ["2 cm", "10 km"], ["1 cm", "5 km"], ["7 cm", "?"], ["7 cm", "35 km"],
                   ["1 cm stands for 10 ÷ 2 = 5 km", "7 cm stands for 7 × 5 = 35 km", "The towns are really 35 km apart"])


@own("G4A_RATIO_020")
def _(Q):
    tones = ["a", "b", "c"]
    whole = bm([bar([seg(str(n), n // 6, t)]) for n, t in zip((18, 24, 30), tones)])
    cut = bm([bar(segs(n // 6, "6", t)) for n, t in zip((18, 24, 30), tones)])
    return entry(Q, w(whole, "18 : 24 : 30 in its simplest form = ?"), [
        w(whole, "6 divides 18, 24 and 30"),
        w(cut, "18 ÷ 6 = 3, 24 ÷ 6 = 4 and 30 ÷ 6 = 5"),
        w(cut, "3 parts, 4 parts and 5 parts: 3 : 4 : 5"),
    ])


@own("G4A_RATIO_021")
def _(Q):
    head = ["Ratio", "Simplest form"]
    rows = [["4 : 6", "2 : 3"], ["8 : 12", "2 : 3"], ["12 : 18", "2 : 3"], ["6 : 8", "3 : 4"]]
    full = table(head, rows, "6 : 8 simplifies to 3 : 4, which is different", ["r3"])
    return entry(Q, None, [
        table(head, rows[:1]),
        table(head, rows[:3], "These simplify to 2 : 3 as well"),
        full,
        w(full, "6 : 8 is not equal to 4 : 6", ["r3"]),
    ])


@own("G4A_RATIO_022")
def _(Q):
    return unitary(Q, ["Time", "Bottles"], ["9 minutes", "45"], ["1 minute", "5"], ["1 hour", "?"], ["60 minutes", "300"],
                   ["In 1 minute: 45 ÷ 9 = 5 bottles", "5 × 60 = 300", "300 bottles in 1 hour"],
                   mid=(["60 minutes", "?"], "1 hour is 60 minutes"))


@own("G4A_RATIO_023")
def _(Q):
    def stamps(label, arun, note, hl=None):
        return bm([bar(segs(3, label, "a"), label="Arun", brace=arun),
                   bar(segs(3, label, "b") + segs(2, label, "c"), label="Bela")], note, hl)
    more = ["b1s3", "b1s4"]
    before = bm([bar(segs(3, None, "a"), label="Arun", brace="?"), bar(segs(5, None, "b"), label="Bela")],
                "Ratio 3 : 5. Bela has 12 more stamps than Arun")
    return entry(Q, before, [
        stamps(None, "?", "Bela has 5 − 3 = 2 parts more", more),
        stamps("6", "?", "2 parts are 12 stamps, so one part is 12 ÷ 2 = 6", more),
        stamps("6", "18 stamps", "Arun has 3 parts: 3 × 6 = 18", ["b0"]),
        stamps("6", "18 stamps", "Arun has 18 stamps", ["b0"]),
    ])


@own("G4A_RATIO_024")
def _(Q):
    def field(breadth, note, hl=None):
        return w({"kind": "rectangle", "length": "40 m", "breadth": breadth, "proportion": 1.67}, note, hl)

    def parts(breadth_label, breadth, note, hl=None):
        return bm([bar(segs(5, "8 m", "a"), label="Length", brace="40 m"),
                   bar(segs(3, breadth_label, "b"), label="Breadth", brace=breadth)], note, hl)
    return entry(Q, field("?", "Length : breadth = 5 : 3. Perimeter = ?"), [
        parts(None, "?", "One part: 40 ÷ 5 = 8 m", ["b0"]),
        parts("8 m", "24 m", "The breadth is 3 parts: 3 × 8 = 24 m", ["b1"]),
        field("24 m", "One length and one breadth: 40 + 24 = 64 m", ["length", "breadth"]),
        field("24 m", "All the way round: 64 × 2 = 128 m", ["border"]),
    ])


@own("G4A_RATIO_025")
def _(Q):
    def money(labels, braces, note, hl=None):
        return bm([bar(segs(2, labels[0], "a"), label="Asha", brace=braces[0]),
                   bar(segs(3, labels[1], "b"), label="Bina", brace=braces[1]),
                   bar(segs(4, labels[2], "c"), label="Chitra", brace=braces[2])], note, hl)
    p = "₹ 20"
    return entry(Q, money((None, None, None), ("₹ 40", None, "?"), "Asha : Bina = 2 : 3. Bina : Chitra = 3 : 4"), [
        money((p, None, None), ("₹ 40", None, "?"), "Asha's 2 parts are ₹ 40: 40 ÷ 2 = 20", ["b0"]),
        money((p, p, None), ("₹ 40", "₹ 60", "?"), "Bina has 3 parts: 3 × 20 = 60", ["b1"]),
        money((p, p, None), ("₹ 40", "₹ 60", "?"), "Bina's 3 parts are ₹ 60, so one part is still ₹ 20", ["b1"]),
        money((p, p, p), ("₹ 40", "₹ 60", "₹ 80"), "Chitra has 4 parts: 4 × 20 = 80", ["b2"]),
    ])


@own("G4A_RATIO_026")
def _(Q):
    def bag(label, note):
        return bm([bar(segs(2, label, "a") + segs(3, label, "b"), brace="20 marbles")], note)

    def two(red, green, note, hl=None):
        return bm([bar([seg(*s) for s in red], label="Red"), bar([seg(*s) for s in green], label="Green")], note, hl)
    return entry(Q, bag(None, "Red : green = 2 : 3. Then 4 more red marbles are put in"), [
        bag("4", "2 + 3 = 5 parts, so one part is 20 ÷ 5 = 4 marbles"),
        two([("8", 2, "a")], [("12", 3, "b")], "Red: 2 × 4 = 8. Green: 3 × 4 = 12"),
        two([("8", 2, "a"), ("4", 1, "c")], [("12", 3, "b")], "8 + 4 = 12 red, and still 12 green", ["b0s1"]),
        two([("12", 3, "a")], [("12", 3, "b")], "12 : 12 simplifies to 1 : 1"),
    ])


@own("G4A_RATIO_027")
def _(Q):
    def rows(pen, pens_brace, pencils_brace, note, hl=None):
        return bm([bar(segs(3, pen, "a", 5), label="3 pens", brace=pens_brace),
                   bar(segs(5, "₹ 6", "b", 3), label="5 pencils", brace=pencils_brace)], note, hl)
    four = bm([bar(segs(4, "₹ 10", "a", 5), label="4 pens", brace="₹ 40")])
    return entry(Q, rows(None, None, None, "Both rows cost the same. 4 pens = ?"), [
        rows(None, None, "₹ 30", "5 pencils cost 5 × 6 = 30 rupees", ["b1"]),
        rows("₹ 10", "₹ 30", "₹ 30", "3 pens cost ₹ 30, so 1 pen costs 30 ÷ 3 = 10", ["b0"]),
        w(four, "4 pens cost 4 × 10 = 40"),
        w(four, "4 pens cost ₹ 40"),
    ])


@own("G4A_RATIO_028")
def _(Q):
    def share(label, note, hl=None):
        return bm([bar(segs(1, label, "a"), label="Child A"), bar(segs(3, label, "b"), label="Child B"),
                   bar(segs(4, label, "c"), label="Child C")], note, hl)
    gap = ["b2s1", "b2s2", "b2s3"]
    return entry(Q, share(None, "96 sweets are shared in the ratio 1 : 3 : 4"), [
        share(None, "1 + 3 + 4 = 8 equal parts"),
        share("12", "One part: 96 ÷ 8 = 12 sweets"),
        share("12", "4 parts and 1 part are 3 parts apart", gap),
        share("12", "3 × 12 = 36 sweets", gap),
    ])


@own("G4A_RATIO_029")
def _(Q):
    head = ["Distance", "Time"]
    given, unit = ["3 km", "45 minutes"], ["1 km", "15 minutes"]
    done = table(head, [given, unit, ["8 km", "120 minutes"]], "120 ÷ 15 = 8", ["r2"])
    return entry(Q, table(head, [given, ["?", "2 hours"]]), [
        table(head, [given, unit, ["?", "2 hours"]], "1 km takes 45 ÷ 3 = 15 minutes", ["r1"]),
        table(head, [given, unit, ["?", "120 minutes"]], "2 hours is 120 minutes", ["r2"]),
        done,
        w(done, "Hari walks 8 km in 2 hours", ["r2"]),
    ])


@own("G4A_RATIO_030")
def _(Q):
    head = ["Paint", "Blue", "Yellow"]
    rows = [["One lot", "2 tins", "3 tins"], ["He has", "12 tins", "15 tins"]]
    lots = table(head, rows + [["Lots", "6", "5"]])
    return entry(Q, table(head, rows, "Greatest number of tins of green paint = ?"), [
        w(lots, "Blue: 12 ÷ 2 = 6 lots. Yellow: 15 ÷ 3 = 5 lots", ["r2"]),
        w(lots, "The yellow runs out first, so only 5 lots", ["r2"]),
        w(lots, "Each lot is 2 + 3 = 5 tins of green paint", ["r0"]),
        w(lots, "5 × 5 = 25 tins of green paint"),
    ])


@own("G4A_RATIO_031")
def _(Q):
    def stickers(label, asha, note, hl=None):
        return bm([bar(segs(3, label, "a") + segs(2, label, "c"), label="Asha", brace=asha),
                   bar(segs(3, label, "b"), label="Bina")], note, hl)
    gap = ["b0s3", "b0s4"]
    start = stickers("6", "30", "Asha had 5 parts: 5 × 6 = 30", ["b0"])
    return entry(Q, bm([bar(segs(5, None, "a"), label="Asha"), bar(segs(3, None, "b"), label="Bina")],
                       "Asha gives 6 stickers to Bina. Then they have the same"), [
        stickers(None, None, "The gap at first is twice 6: 12 stickers", gap),
        stickers("6", None, "The gap is 5 − 3 = 2 parts, so one part is 12 ÷ 2 = 6", gap),
        start,
        bm([bar(segs(4, "6", "a"), label="Asha", brace="24"), bar(segs(4, "6", "b"), label="Bina", brace="24")],
           "Check: 30 and 18 become 24 and 24"),
        w(start, "Asha had 30 stickers at first", ["b0"]),
    ])


@own("G4A_RATIO_032")
def _(Q):
    def job(rest, tone, note, hl=None):
        return bm([bar([seg("4 days", 4, "a"), seg(rest, 8, tone)], label="The job", brace="12 days for 8 workers")], note, hl)
    before = job("?", "unknown", "After 4 days, 8 more workers join")
    return entry(Q, before, [
        None,
        w(before, "The 8 workers do the first 4 days of the job", ["b0s0"]),
        w(before, "The rest of the job is still to do", ["b0s1"]),
        w(before, "Now 8 + 8 = 16 workers share the rest", ["b0s1"]),
        job("4 more days", "b", "16 workers finish the rest in 4 more days", ["b0s1"]),
    ])


@own("G4A_RATIO_033")
def _(Q):
    head = ["Ratio", "Asha", "Bina", "Chitra"]
    first = [["Asha : Bina", "2", "3", "-"], ["Bina : Chitra", "-", "4", "5"]]
    joined = [["Asha : Bina", "8", "12", "-"], ["Bina : Chitra", "-", "12", "15"], ["Together", "8", "12", "15"]]
    before = table(head, first, "₹ 70 is shared. Chitra = ?")
    together = table(head, joined)
    rupees = table(head, joined + [["Rupees", "₹ 16", "₹ 24", "₹ 30"]])
    return entry(Q, before, [
        w(before, "Make Bina's part 12 in both ratios"),
        w(together, "2 : 3 becomes 8 : 12 and 4 : 5 becomes 12 : 15", ["r2"]),
        w(together, "Count the parts: 8 + 12 + 15 = 35", ["r2"]),
        w(together, "One part: 70 ÷ 35 = 2 rupees", ["r2"]),
        w(rupees, "Chitra has 15 parts: 15 × 2 = 30", ["r3"]),
        w(rupees, "Chitra gets ₹ 30", ["r3"]),
    ])


@own("G4A_RATIO_034")
def _(Q):
    head = ["Beads", "Red", "Blue"]

    def grow(added, blue, blue_brace, note, hl=None):
        return bm([bar(segs(2, None, "a"), label="Red before"),
                   bar(segs(2, None, "a") + segs(4, added, "c"), label="Red after"),
                   bar(segs(3, blue, "b"), label="Blue", brace=blue_brace)], note, hl)
    new = ["b1s2", "b1s3", "b1s4", "b1s5"]
    check = bm([bar(segs(6, "2", "a"), label="Red after", brace="12"), bar(segs(3, "2", "b"), label="Blue", brace="6")])
    return entry(Q, table(head, [["Before", "2", "3"], ["After", "2", "1"]], "8 red beads are added. The blue beads stay the same"), [
        table(head, [["Before", "2", "3"], ["After", "6", "3"]], "2 : 1 is the same as 6 : 3. Now blue is 3 parts both times", ["r1"]),
        grow(None, None, None, "Red grows from 2 parts to 6 parts", new),
        grow("2", None, None, "4 parts are the 8 beads added: 8 ÷ 4 = 2", new),
        grow("2", "2", "6 beads", "Blue is 3 parts: 3 × 2 = 6", ["b2"]),
        w(check, "Check: 12 red and 6 blue is 2 : 1"),
        w(check, "There are 6 blue beads in the box", ["b1"]),
    ])


@own("G4A_RATIO_035")
def _(Q):
    head = ["Coin", "In one group"]
    group = table(head, [["₹ 1", "3"], ["₹ 2", "2"], ["₹ 5", "1"]])
    return entry(Q, w(group, "The coins are worth ₹ 96 altogether"), [
        [table(["Coin", "In one group", "Worth"], [["₹ 1", "3", "₹ 3"], ["₹ 2", "2", "₹ 4"], ["₹ 5", "1", "₹ 5"]], "One group is worth 3 + 4 + 5 = ₹ 12"),
         w(group, "One group of 3, 2 and 1 coins is worth ₹ 12")],
        w(group, "96 ÷ 12 = 8 groups"),
        w(group, "Each of the 8 groups has one ₹ 5 coin", ["r2"]),
        w(group, "There are 8 coins of ₹ 5", ["r2"]),
    ])


@own("G4A_RATIO_036")
def _(Q):
    four = bm([bar(segs(4, None, "a"), label="Pole")])
    eight = bm([bar(segs(8, None, "b"), label="New pole")])
    return entry(Q, w(four, "Cutting it into 4 pieces takes 12 minutes"), [
        w(four, "3 cuts make 4 pieces"),
        w(four, "One cut takes 12 ÷ 3 = 4 minutes"),
        w(eight, "7 cuts make 8 pieces"),
        w(eight, "7 cuts take 7 × 4 = 28 minutes"),
        w(eight, "He will take 28 minutes"),
    ])


@own("G4A_RATIO_037")
def _(Q):
    def four(gap, note):
        return nline(0, 6, 2, points=[(0, "ring 1"), (2, "ring 2"), (4, "ring 3"), (6, "ring 4")],
                     hops=[(0, 2, gap), (2, 4, gap), (4, 6, gap)], ticks="none", note=note)

    def twelve(ticks, note):
        return nline(0, 22, 2, points=[(0, "ring 1"), (22, "ring 12")], ticks=ticks, note=note)
    return entry(Q, nline(0, 6, 6, points=[(0, "ring 1"), (6, "ring 4")], ticks="ends",
                          note="Seconds along the line. 4 rings take 6 seconds"), [
        four(None, "4 rings have 3 gaps"),
        four("2 s", "One gap: 6 ÷ 3 = 2 seconds"),
        twelve("none", "12 rings have 11 gaps"),
        twelve("ends", "11 gaps of 2 seconds: 11 × 2 = 22"),
        twelve("ends", "It will take 22 seconds"),
    ])


@own("G4A_RATIO_038")
def _(Q):
    def jugs(a, b, note, hl=None):
        return bm([bar([seg(a[0], 1, "a"), seg(a[1], 3, "b")], label="Jug A", brace="8 cups"),
                   bar([seg(b[0], 2, "a"), seg(b[1], 2, "b")], label="Jug B", brace="8 cups")], note, hl)
    pot = bm([bar(segs(3, "2", "a") + segs(5, "2", "b"), label="Pot")])
    return entry(Q, jugs(("juice", "water"), ("juice", "water"), "Jug A is 1 : 3. Jug B is 1 : 1. Both go into one pot"), [
        jugs(("2 cups", "6 cups"), ("juice", "water"), "Jug A: 4 parts make 8 cups, so each part is 2 cups", ["b0"]),
        jugs(("2 cups", "6 cups"), ("4 cups", "4 cups"), "Jug B: 2 parts make 8 cups, so each part is 4 cups", ["b1"]),
        bm([bar([seg("6 cups", 3, "a"), seg("10 cups", 5, "b")], label="Pot")], "Juice: 2 + 4 = 6. Water: 6 + 4 = 10"),
        w(pot, "6 ÷ 2 = 3 and 10 ÷ 2 = 5"),
        w(pot, "Lemon juice to water is 3 : 5"),
    ])


@own("G4A_RATIO_039")
def _(Q):
    def cls(label, braces, note):
        return bm([bar(segs(4, label, "a"), label="Boys", brace=braces[0]),
                   bar(segs(5, label, "b"), label="Girls", brace=braces[1])], note)
    return entry(Q, cls(None, (None, None), "Boys : girls = 4 : 5. How many children could there be?"), [
        [cls(None, (None, None), "4 + 5 = 9 equal parts"), cls(None, (None, None), "4 parts are boys and 5 parts are girls")],
        cls(None, (None, None), "The number of children is a multiple of 9"),
        cls("4", (None, None), "36 is a multiple of 9: 36 ÷ 9 = 4 in each part"),
        cls("4", ("16", "20"), "Check: 16 boys and 20 girls is 4 : 5"),
        cls("4", ("16", "20"), "The class could have 36 children"),
    ])


@own("G4A_RATIO_040")
def _(Q):
    def rides(km, start, start_units, note, hl=None):
        return bm([bar([seg(start, start_units, "c")] + segs(3, km, "a"), label="3 km ride", brace="₹ 50"),
                   bar([seg(start, start_units, "c")] + segs(5, km, "a"), label="5 km ride", brace="₹ 70")], note, hl)

    def ten(start, brace, note):
        return bm([bar([seg(start, 2, "c")] + segs(10, "₹ 10", "a"), label="10 km ride", brace=brace)], note)
    extra = ["b1s4", "b1s5"]
    return entry(Q, rides(None, "start", 1, "A fixed starting charge, then the same for every km"), [
        [rides(None, "start", 1, "The 2 extra km cost 70 − 50 = ₹ 20", extra),
         rides(None, "start", 1, "The 2 extra km cost the extra money: 70 − 50", extra)],
        rides("₹ 10", "start", 2, "Half of that is the cost of one km: ₹ 10", extra),
        [rides("₹ 10", "₹ 20", 2, "Starting charge: 50 − 3 × 10 = 20", ["b0s0"]),
         rides("₹ 10", "start", 2, "Starting charge: 50 − 3 × 10", ["b0s0"])],
        [ten("₹ 20", "₹ 120", "20 + 10 × 10 = 120"), ten("start", "₹ 120", "Starting charge + 10 × 10 = ₹ 120")],
        [ten("₹ 20", "₹ 120", "A 10 km ride costs ₹ 120"), ten("start", "₹ 120", "A 10 km ride costs ₹ 120")],
    ])


@own("G4A_RATIO_041")
def _(Q):
    def share(label, ravi, note, hl=None):
        return bm([bar(segs(7, label, "a"), label="Ravi", brace=ravi), bar(segs(3, label, "b"), label="Sita")], note, hl)
    down = bm([bar([seg("30", 5, "a"), seg("12", 2, "c")], label="Ravi", brace="42"), bar([seg(None, 3, "b")], label="Sita")])
    return entry(Q, share(None, None, "60 sweets in the ratio 7 : 3. Ravi wants equal shares"), [
        [share("6", None, "7 + 3 = 10 parts, so one part is 60 ÷ 10 = 6"), share(None, None, "7 + 3 = 10 equal parts. Find one part")],
        [share("6", "42", "Ravi has 7 × 6 = 42"), share(None, "42", "Ravi has 42 sweets and Sita has the rest", ["b0"])],
        bm([bar([seg("30", 5, "a")], label="Ravi"), bar([seg("30", 5, "b")], label="Sita")], "Equal shares: half of 60 each"),
        w(down, "Ravi must come down from 42 to 30: 42 − 30 = 12", ["b0s1"]),
        w(down, "Ravi must give 12 sweets to Sita", ["b0s1"]),
    ])


@own("G4A_RATIO_042")
def _(Q):
    # The question gives its fractions in words, so the before-figure carries no numbers.
    def both(asha, bina, braces, note, hl=None):
        return bm([bar([seg(asha[0], 1, "a"), seg(asha[1], 1, "a"), seg(asha[2], 1, "b")], label="Asha", brace=braces[0]),
                   bar([seg(bina[0], 2, "a"), seg(bina[1], 2, "b")], label="Bina", brace=braces[1])], note, hl)
    done = both(("3", "3", "3"), ("6", "6"), ("9", "12"), "9 ÷ 3 = 3 and 12 ÷ 3 = 4")
    return entry(Q, both((None,) * 3, (None,) * 2, (None, None), "Two-thirds of Asha's equals one-half of Bina's"), [
        both((None, None, None), ("6", None), (None, None), "Say the equal shaded amount is 6 stickers"),
        both(("3", "3", "3"), ("6", None), ("9", None), "One-third is 3, so Asha has 9", ["b0"]),
        both(("3", "3", "3"), ("6", "6"), ("9", "12"), "Half is 6, so Bina has 12", ["b1"]),
        done,
        w(done, "Asha's stickers to Bina's stickers is 3 : 4"),
    ])


@own("G4A_RATIO_043")
def _(Q):
    head = ["Hens", "Days", "Eggs"]
    before = table(head, [["4", "3", "12"], ["6", "5", "?"]])
    done = table(head, [["4", "3", "12"], ["6", "5", "30"]], "1 egg for each hen-day: 30 eggs", ["r1"])
    return entry(Q, before, [
        w(before, "4 hens for 3 days is 12 hen-days", ["r0"]),
        w(before, "12 eggs in 12 hen-days: 1 egg for each hen-day", ["r0"]),
        w(before, "6 hens for 5 days is 30 hen-days", ["r1"]),
        done,
        w(done, "6 hens will lay 30 eggs in 5 days", ["r1"]),
    ])


@own("G4A_RATIO_044")
def _(Q):
    def share(label, braces, note, hl=None):
        return bm([bar(segs(3, label, "a"), label="Anu", brace=braces[0]),
                   bar(segs(4, label, "b"), label="Bala", brace=braces[1])], note, hl)
    return entry(Q, share(None, (None, None), "More than 40, fewer than 50 sweets. Bala gets over 25"), [
        share(None, (None, None), "3 + 4 = 7 parts, so the total is 42 or 49"),
        share("6", (None, "24"), "42 sweets: Bala gets 24. That is not more than 25", ["b1"]),
        share("7", (None, "28"), "49 sweets: Bala gets 28. That is more than 25", ["b1"]),
        share("7", ("21", "28"), "Anu gets 3 parts of 7: 3 × 7 = 21", ["b0"]),
        share("7", ("21", "28"), "Anu gets 21 sweets", ["b0"]),
    ])


@own("G4A_RATIO_045")
def _(Q):
    def club(label, girls, note, hl=None):
        return bm([bar(segs(3, label, "a"), label="Girls", brace=girls),
                   bar(segs(5, "8", "b"), label="Boys", brace="40")], note, hl)
    boys = ["b0s3", "b0s4", "b0s5", "b0s6", "b0s7"]
    return entry(Q, bm([bar(segs(3, None, "a"), label="Girls", brace="?"), bar(segs(8, None, "b"), label="All children")],
                       "Girls : all children = 3 : 8. There are 40 boys"), [
        [bm([bar(segs(3, None, "a") + segs(5, None, "b"), label="All children")], "8 − 3 = 5 parts are boys", boys),
         bm([bar(segs(3, None, "a") + segs(5, None, "b"), label="All children")], "Girls are 3 of the 8 parts. The rest are boys", boys)],
        club(None, "?", "The 40 boys are 5 parts: 40 ÷ 5 = 8", ["b1"]),
        club("8", "24", "Girls are 3 parts: 3 × 8 = 24", ["b0"]),
        club("8", "24", "Check: 24 girls out of 64 children is 3 : 8"),
        club("8", "24", "There are 24 girls", ["b0"]),
    ])


@own("G4A_RATIO_046")
def _(Q):
    head = ["Distance ridden", "Asha", "Bala"]
    same, end = "In the same time", "When Asha ends"
    before = table(head, [[same, "5 km", "4 km"], [end, "30 km", "?"]], "The ride is 30 km long")
    road = {"kind": "journey", "places": ["Start", "Bala", "Finish"], "legs": [{"top": "24 km"}, {"top": "6 km"}]}
    return entry(Q, before, [
        w(before, "Asha rides 30 ÷ 5 = 6 lots of 5 km", ["r1"]),
        table(head, [[same, "5 km", "4 km"], [end, "30 km", "24 km"]], "In each lot Bala rides 4 km: 6 × 4 = 24", ["r1"]),
        w(road, "When Asha finishes: 30 − 24 = 6 km to go", ["l1"]),
        w(road, "Bala still has 6 km to go", ["l1"]),
    ])


@own("Q_CH09_018")
def _(Q):
    head = ["Workers", "Days"]
    before = table(head, [["12", "10"], ["15", "?"]])
    done = table(head, [["12", "10"], ["15", "8"]], "Share the work: 120 ÷ 15 = 8", ["r1"])
    return entry(Q, before, [
        w(before, "12 workers for 10 days: 120 days of work for one worker", ["r0"]),
        done,
        w(done, "15 workers need 8 days", ["r1"]),
    ])
