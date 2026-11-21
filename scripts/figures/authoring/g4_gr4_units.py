"""Figures for Grade 4 "Decimal Units of Measurement" (node gr4_units).

    python -X utf8 scripts/figures/authoring/g4_gr4_units.py            # write the part file
    python -X utf8 scripts/figures/authoring/g4_gr4_units.py review     # ... and print every figure beside its question
    python -X utf8 scripts/figures/authoring/g4_gr4_units.py review G4A # ... only ids matching a pattern
    python -X utf8 scripts/figures/authoring/g4_gr4_units.py missing    # ... and list the questions left without a figure

Writes data/question-figures/parts/g4-gr4_units.json.

Bar models carry the word problems (a whole and its parts, equal lots), place-value charts
show where the digits of a decimal measure sit, and small tables line up conversions.
Bar pieces are given in the question's own quantities (grams, millilitres, ...) so they are
drawn in proportion.
"""
import re
import sys

from g4_gr4_operations_kit import (answer_text, bar, bm, entry, equal_segs, fb, finish, journey, load, nl, num, pc,
                                   seg, setf, show, step_figs, step_texts, table)

TOPIC = "gr4_units"


# ── Rules ────────────────────────────────────────────────────────────────────

def rule_bags(q):
    """'Isha has 5 bags of rice, each weighing 8 kg 500 g. What is the total weight in grams?'"""
    m = re.search(r"has (\d+) bags of (\w+), each weighing (\d+) kg (\d+) g\. What is the total weight in grams",
                  q["questionText"])
    if not m or len(step_texts(q)) != 2:
        return None
    n, what, kg, g = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    one = kg * 1000 + g
    total = n * one
    if num(answer_text(q)) != total:
        return None

    def bags(label, brace, note=None, hl=None):
        return bm([bar(equal_segs(n, label), brace=brace)], note=note, hl=hl)

    figure = bags("%d kg %d g" % (kg, g), "Total = ? g", note="%d bags of %s, all the same weight" % (n, what))
    figs = {0: bags("%d g" % one, "Total = ? g", note="1 kg = 1000 g, so one bag is %d g" % one, hl=["b0s0"]),
            1: bags("%d g" % one, "%d g" % total, note="%d × %d = %d" % (one, n, total), hl=["b0"])}
    return entry("rule", figure, step_figs(q, figs))


def rule_glasses(q):
    """'A bottle holds 20 litres of water. How many glasses of 300 ml each can be filled?'"""
    m = re.search(r"A (\w+) holds (\d+) litres of water\. How many glasses of (\d+) ml each can be filled", q["questionText"])
    if not m or len(step_texts(q)) != 2:
        return None
    holder, litres, glass = m.group(1), int(m.group(2)), int(m.group(3))
    ml = litres * 1000
    count = num(answer_text(q))
    if count != ml // glass:
        return None

    # One glass is only a sliver of the whole (1.5% to 4%), too thin to label on a bar,
    # so the givens are lined up in a table instead.
    def jug(whole, glasses, note=None, hl=None):
        return table([["The %s" % holder, whole], ["One glass", "%d ml" % glass], ["Glasses filled", glasses]], note=note, hl=hl)

    exact = ml % glass == 0
    figure = jug("%d litres" % litres, "?")
    figs = {0: jug("%d ml" % ml, "?", note="1 litre = 1000 ml, so %d litres = %d ml" % (litres, ml), hl=["r0"]),
            1: jug("%d ml" % ml, str(count),
                   note=("%d ÷ %d = %d glasses" if exact else "%d ÷ %d gives %d full glasses") % (ml, glass, count), hl=["r2"])}
    return entry("rule", figure, step_figs(q, figs))


RULES = [rule_bags, rule_glasses]


# ── Individually drawn questions ─────────────────────────────────────────────

def authored(Q):
    out = {}

    def add(qid, figure=None, figs=None):
        out[qid] = entry("authored", figure, step_figs(Q[qid], figs or {}))

    # ── A decimal measure on the place-value chart ──────────────────────────
    # The answer written as a decimal: the chart comes with the step that states it.
    add("EXT_G4_FP_2020_029", None, {2: pc("5.015", note="5 whole grams, and 15 mg in the thousandths")})
    add("EXT_G4_FP_2022_031", None, {2: pc("11.011", note="11 whole kilograms, and 11 g in the thousandths")})
    add("G4A_UNITS_001", None, {2: pc("4.075", note="4 whole kilometres, and 75 m in the thousandths")})
    add("PYQ_2017_Q30", None, {0: pc("0.07", note="70 ÷ 1000 = 0.07"), 2: pc("7.07", note="7 + 0.07 = 7.07 kg")})
    add("PYQ_2019_Q37", None, {0: pc("0.07", note="70 ÷ 1000 = 0.07"), 1: pc("7.07", note="7 + 0.07 = 7.07 kg")})
    add("Q_CH12_013", None, {1: pc("0.8", note="800 ÷ 1000 = 0.8")})
    add("Q_CH12_014", None, {1: pc("0.08", note="80 ÷ 1000 = 0.08")})
    add("Q_CH12_015", None, {1: pc("0.005", note="5 ÷ 1000 = 0.005")})
    add("Q_CH12_021", None, {1: pc("0.03", note="30 ÷ 1000 = 0.03")})
    add("Q_CH12_017", None, {2: pc("30.7", note="30 + 0.7 = 30.7 dm")})
    # A decimal given in the question: the chart shows what each digit is worth.
    add("PYQ_2018_Q09", pc("8.05", note="8.05 kg"),
        {0: pc("8.05", note="8 whole kilograms and 0.05 kg more", hl=["d1", "d2"])})
    add("PYQ_2016_Q38", pc("11.11", note="11.11 kilogram"),
        {0: pc("11.11", note="11 whole kilograms and 0.11 kg more", hl=["d2", "d3"])})
    add("Q_CH12_006", pc("37.02", note="37.02 kg"),
        {0: pc("37.02", note="37 whole kilograms and 0.02 kg more", hl=["d2", "d3"])})
    # Split a decimal measure into the whole unit and the small unit (steps rewritten Nov 2026:
    # split, then multiply the part after the point, then state the answer).
    def split_measure(qid, number, whole, part, big, small, times, small_amount, digits, name):
        head = ["Part", "In %s and %s" % (big, small)]
        add(qid, pc(number, note="%s %s" % (number, name)),
            {0: pc(number, note="%s whole %s and %s %s more" % (whole, name, part, big), hl=digits),
             1: table([["%s %s" % (whole, big), "%s %s" % (whole, big)], ["%s %s" % (part, big), "? %s" % small]], headers=head,
                      note="1 %s is %d %s, so multiply %s by %d" % (big, times, small, part, times), hl=["r1"]),
             2: table([["%s %s" % (whole, big), "%s %s" % (whole, big)], ["%s %s" % (part, big), "%s %s" % (small_amount, small)]],
                      headers=head, note="%s %s = %s %s %s %s" % (number, big, whole, big, small_amount, small), hl=["r1"])})
    split_measure("Q_CH12_018", "2.5", "2", "0.5", "kg", "g", 1000, "500", ["d1"], "kilograms")
    split_measure("Q_CH12_019", "2.05", "2", "0.05", "l", "ml", 1000, "50", ["d1", "d2"], "litres")
    split_measure("Q_CH12_020", "2.05", "2", "0.05", "m", "cm", 100, "5", ["d1", "d2"], "metres")

    # ── Lengths joined together ─────────────────────────────────────────────
    def three_lengths(first, second, brace, note=None, hl=None):
        return bm([bar([seg(first, 200, "a"), seg(second, 20, "b"), seg("15 cm", 15, "c")], brace=brace)], note=note, hl=hl)
    add("PYQ_2017_Q15", three_lengths("2 m", "2 dm", "? cm"),
        {0: three_lengths("200 cm", "2 dm", "? cm", note="1 m is 100 cm, so 2 m is 200 cm", hl=["b0s0"]),
         1: three_lengths("200 cm", "20 cm", "? cm", note="1 dm is 10 cm, so 2 dm is 20 cm", hl=["b0s1"]),
         2: three_lengths("200 cm", "20 cm", "235 cm", note="200 + 20 + 15 = 235", hl=["b0"])})
    add("EXT_G4_FP_2021_009", three_lengths("2 m", "2 dm", "? cm"),
        {0: three_lengths("2 m", "2 dm", "? cm", note="1 m = 100 cm. Change the 2 m first.", hl=["b0s0"]),
         1: three_lengths("2 m", "2 dm", "? cm", note="1 dm = 10 cm. Now change the 2 dm.", hl=["b0s1"]),
         2: three_lengths("2 m", "2 dm", "235 cm", note="The three lengths together make 235 cm", hl=["b0"])})

    def m_dm(first, second, brace, note=None, hl=None):
        return bm([bar([seg(first, 30, "a"), seg(second, 7, "b")], brace=brace)], note=note, hl=hl)
    add("Q_CH12_016", m_dm("3 m", "7 dm", "? cm"),
        {0: m_dm("300 cm", "7 dm", "? cm", note="1 m is 100 cm, so 3 m is 300 cm", hl=["b0s0"]),
         1: m_dm("300 cm", "70 cm", "? cm", note="1 dm is 10 cm, so 7 dm is 70 cm", hl=["b0s1"]),
         2: m_dm("300 cm", "70 cm", "370 cm", note="300 + 70 = 370", hl=["b0"])})

    head = ["Length", "In metres"]
    add("Q_CH12_009", table([["4 km", "?"], ["40 m", "40 m"], ["400 cm", "?"]], headers=head),
        {0: table([["4 km", "4000 m"], ["40 m", "40 m"], ["400 cm", "?"]], headers=head, note="1 km is 1000 m", hl=["r0"]),
         1: table([["4 km", "4000 m"], ["40 m", "40 m"], ["400 cm", "4 m"]], headers=head, note="100 cm make 1 m", hl=["r2"]),
         2: table([["4 km", "4000 m"], ["40 m", "40 m"], ["400 cm", "4 m"]], headers=head, note="4000 + 40 + 4 = 4044 metres")})

    head = ["Amount", "In grams"]
    add("EXT_G4_FP_2023_024", table([["100 decigrams", "?"], ["300 decagrams", "?"]], headers=head),
        {0: table([["100 decigrams", "10 g"], ["300 decagrams", "?"]], headers=head, note="10 decigrams make 1 gram", hl=["r0"]),
         1: table([["100 decigrams", "10 g"], ["300 decagrams", "3000 g"]], headers=head, note="1 decagram is 10 grams", hl=["r1"]),
         2: table([["100 decigrams", "10 g"], ["300 decagrams", "3000 g"]], headers=head, note="Add the two amounts"),
         3: table([["100 decigrams", "10 g"], ["300 decagrams", "3000 g"]], headers=head, note="10 + 3000 = 3010 grams")})

    # ── Unitary tables ──────────────────────────────────────────────────────
    head = ["Mangoes", "Juice"]
    add("EXT_G4_FP_2022_039", table([["4", "250 ml"], ["?", "1 decalitre"]], headers=head),
        {0: table([["4", "250 ml"], ["?", "10 litres"]], headers=head, note="1 decalitre is 10 litres", hl=["r1"]),
         1: table([["4", "250 ml"], ["?", "10000 ml"]], headers=head, note="How many lots of 250 ml fit in 10000 ml?", hl=["r1"]),
         2: table([["4", "250 ml"], ["160", "10000 ml"]], headers=head, note="Each lot of 250 ml needs 4 mangoes", hl=["r1"])})

    head = ["Eggs", "Cost"]
    add("EXT_G4_FP_2024_014", table([["1 gross", "Rs.864"], ["1 score", "?"]], headers=head),
        {0: table([["12 dozen", "Rs.864"], ["1 score", "?"]], headers=head, note="A gross is 12 dozen: 12 × 12 eggs", hl=["r0"]),
         1: table([["12 dozen", "Rs.864"], ["1", "?"], ["1 score", "?"]], headers=head, note="First find the price of one egg", hl=["r1"]),
         2: table([["12 dozen", "Rs.864"], ["1", "?"], ["20", "?"]], headers=head, note="A score is 20 eggs", hl=["r2"]),
         3: table([["1 gross", "Rs.864"], ["1 score", "Rs.120"]], headers=head, hl=["r1"])})

    head = ["Fruit", "Cost"]
    fruit = [["1 score oranges", "Rs.130"], ["1 dozen apples", "Rs.180"], ["12 oranges", "?"], ["17 apples", "?"]]
    add("EXT_G4_FP_2025_023", table(fruit, headers=head),
        {0: table(fruit, headers=head, note="A score is 20, so 20 oranges cost Rs.130", hl=["r0"]),
         1: table(fruit, headers=head, note="12 oranges cost 12 times the price of one", hl=["r2"]),
         2: table(fruit, headers=head, note="A dozen is 12, so 12 apples cost Rs.180", hl=["r1"]),
         3: table(fruit, headers=head, note="17 apples cost 17 times the price of one", hl=["r3"]),
         4: table(fruit, headers=head, note="Add the two costs", hl=["r2", "r3"])})

    head = ["Thickness", "Sheets"]
    add("PYQ_2017_Q04", table([["5 cm", "500"], ["1 m 22.5 cm", "?"]], headers=head),
        {0: table([["5 cm", "500"], ["122.5 cm", "?"]], headers=head, note="1 metre is 100 cm: 100 + 22.5 = 122.5 cm", hl=["r1"]),
         1: table([["5 cm", "500"], ["1 cm", "100"], ["122.5 cm", "?"]], headers=head, note="500 ÷ 5 = 100 sheets in 1 cm", hl=["r1"]),
         2: table([["5 cm", "500"], ["1 cm", "100"], ["122.5 cm", "12250"]], headers=head, note="122.5 × 100 = 12250", hl=["r2"])})

    head = ["Shop", "Milk", "Price"]
    shops = [["P", "500 ml", "₹28"], ["Q", "1.5 litres", "₹81"], ["R", "250 ml", "₹15"], ["S", "2 litres", "₹110"]]
    add("G4A_UNITS_031", table(shops, headers=head, note="Where does one litre cost the least?"),
        {0: table(shops, headers=head, note="Shop P: 500 ml is half a litre", hl=["r0"]),
         1: table(shops, headers=head, note="R sells a quarter of a litre, S sells 2 litres", hl=["r2", "r3"]),
         2: table(shops, headers=head, note="Shop Q: 1.5 litres is three half-litres", hl=["r1"]),
         3: table([["P", "₹56"], ["Q", "₹54"], ["R", "₹60"], ["S", "₹55"]], headers=["Shop", "1 litre costs"],
                  note="The least is ₹54, at Shop Q", hl=["r1"])})

    # ── A whole and its parts ───────────────────────────────────────────────
    def bottle(left, brace, note=None, hl=None):
        return bm([bar([seg(left, 850, "unknown" if "?" in left else "a"), seg("350 ml", 350, "b")], brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_002", bottle("? ml left", "1.2 litres", note="Meera drinks 350 ml"),
        {0: bottle("? ml left", "1.2 litres", note="1 litre = 1000 ml, so change 1.2 litres into ml", hl=["b0"]),
         1: bottle("? ml left", "1.2 litres", note="Take away the 350 ml that Meera drank", hl=["b0s1"]),
         2: bottle("850 ml", "1.2 litres", note="850 ml are left", hl=["b0s0"])})

    def pencil(gap, tone, note=None, hl=None):
        return bm([bar([seg("14 cm 6 mm", 146, "a")], label="New"),
                   bar([seg("12 cm 9 mm", 129, "a"), seg(gap, 17, tone)], label="Now")], note=note, hl=hl)
    add("G4A_UNITS_003", pencil("?", "unknown", note="How many millimetres shorter is it now?"),
        {0: pencil("?", "unknown", note="1 cm = 10 mm. Change 14 cm 6 mm into mm.", hl=["b0"]),
         1: pencil("?", "unknown", note="Change 12 cm 9 mm into mm too", hl=["b1s0"]),
         2: pencil("17 mm", "b", note="It is 17 mm shorter", hl=["b1s1"])})

    def vegetables(brace, note=None, hl=None):
        return bm([bar([seg("1 kg 750 g", 1750, "a"), seg("2 kg 400 g", 2400, "b")], brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_004", vegetables("Total = ? kg", note="Potatoes and onions together"),
        {0: vegetables("Total = ? kg", note="Add the grams first: 750 g and 400 g", hl=["b0"]),
         2: vegetables("4 kg 150 g = 4.15 kg", hl=["b0"])})

    def bananas(sold, left, brace, note=None, hl=None):
        return bm([bar([seg(sold, 60, "b"), seg(left, 24, "unknown" if "?" in left else "a")], brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_005", bananas("3 score sold", "? left", "7 dozen"),
        {0: bananas("3 score sold", "? left", "7 dozen = 7 × 12", note="1 dozen = 12", hl=["b0"]),
         1: bananas("3 × 20 sold", "? left", "7 dozen = 7 × 12", note="1 score = 20", hl=["b0s0"]),
         2: bananas("3 score sold", "24 left", "7 dozen", note="24 bananas are left", hl=["b0s1"])})

    def gross(left, brace, note=None, hl=None):
        return bm([bar([seg("54 × 2 given", 108, "b"), seg(left, 36, "unknown" if "?" in left else "a")], brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_006", gross("? left", "1 gross", note="54 children get 2 pencils each"),
        {0: gross("? left", "1 gross = 12 dozen", note="12 dozen is 12 × 12 pencils", hl=["b0"]),
         1: gross("? left", "1 gross = 12 dozen", note="Pencils given: 54 lots of 2", hl=["b0s0"]),
         2: gross("36 left", "1 gross = 12 dozen", note="36 pencils remain in the box", hl=["b0s1"])})

    def cloth(used, left, brace, note=None, hl=None):
        return bm([bar([seg(used, 235, "b"), seg(left, 265, "unknown" if "?" in left else "a")], brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_013", cloth("2 m 35 cm used", "? left", "5 m"),
        {0: cloth("235 cm", "? left", "500 cm", note="5 m = 500 cm and 2 m 35 cm = 235 cm", hl=["b0"]),
         1: cloth("235 cm", "? left", "500 cm", note="Subtract the cloth he used", hl=["b0s1"]),
         2: cloth("235 cm", "2 m 65 cm", "500 cm", note="265 cm is 2 m 65 cm", hl=["b0s1"])})

    def basket(brace, note=None, hl=None):
        return bm([bar([seg("600 g", 600, "b"), seg("12 mangoes", 3600, "a")], brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_017", basket("4 kg 200 g", note="The empty basket weighs 600 g"),
        {0: basket("4200 g", note="4 kg 200 g = 4200 g", hl=["b0"]),
         1: basket("4200 g", note="Take away the 600 g basket to leave the mangoes", hl=["b0s1"]),
         2: bm([bar(equal_segs(12, "300 g"), brace="12 mangoes")], note="Shared among 12 mangoes: 300 g each")})

    def tins(box, note=None, hl=None):
        return bm([bar([seg(box, 300, "unknown" if box == "?" else "c"), seg("12 tins", 4800, "a")], brace="5 kg 100 g"),
                   bar([seg(None, 300, "unknown" if box == "?" else "c"), seg("12 − 4 tins", 3200, "a")], brace="3 kg 500 g")],
                  note=note, hl=hl)
    add("G4A_UNITS_032", tins("?", note="The small piece at the front is the empty box"),
        {0: tins("?", note="The two weighings differ by the weight of 4 tins", hl=["b0s1", "b1s1"]),
         3: tins("300 g", note="The empty box weighs 300 g", hl=["b0s0"])})

    def lace(more, brace, note=None, hl=None):
        return bm([bar([seg("1 m 20 cm", 120, "a"), seg("85 cm", 85, "b"), seg("600 mm", 60, "c"),
                        seg(more, 35, "unknown")], brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_034", lace("?", "3 m", note="Three pieces of lace, and the gap still to fill"),
        {0: lace("?", "3 m", note="Change each piece into centimetres", hl=["b0s0", "b0s2"]),
         1: lace("?", "3 m", note="Add the three pieces", hl=["b0s0", "b0s1", "b0s2"]),
         2: lace("?", "300 cm", note="Rani needs 3 m, which is 300 cm", hl=["b0s3"]),
         3: lace("35 cm", "300 cm", note="She needs 35 cm more lace", hl=["b0s3"])})

    def rice(sold, left, brace, note=None, hl=None):
        return bm([bar([seg(sold, 2750, "b"), seg(left, 2650, "unknown" if "?" in left else "a")], brace=brace)], note=note, hl=hl)
    add("Q_CH12_024", rice("2 kg 750 g sold", "? left", "5.4 kg"),
        {0: rice("2 kg 750 g sold", "? left", "5400 g", note="5.4 kg is 5400 g", hl=["b0"]),
         1: rice("2 kg 750 g sold", "? left", "5400 g", note="Change 2 kg 750 g into grams too", hl=["b0s0"]),
         2: rice("2 kg 750 g sold", "? left", "5400 g", note="Subtract the rice that was sold", hl=["b0s1"]),
         3: rice("2 kg 750 g sold", "2 kg 650 g", "5400 g", note="2650 g is 2 kg 650 g", hl=["b0s1"])})

    add("G4A_UNITS_040", bm([bar([seg("250 g", 250, "a"), seg("500 g", 500, "b")], brace="Total = ?")], note="Sugar and flour together"),
        {0: bm([bar([seg("250 g", 250, "a"), seg("500 g", 500, "b")], brace="Total = ?")],
               note="Both weights are in grams, so add them", hl=["b0"]),
         1: bm([bar([seg("250 g", 250, "a"), seg("500 g", 500, "b")], brace="750 g")], hl=["b0"])})

    def rope(left, tone, note=None, hl=None):
        return bm([bar([seg("3 m cut off", 3, "b"), seg(left, 5, tone)], brace="8 m")], note=note, hl=hl)
    add("G4A_UNITS_041", rope("? left", "unknown"),
        {0: rope("? left", "unknown", note="Take the 3 m piece away from the 8 m rope", hl=["b0s0"]),
         1: rope("5 m left", "a", hl=["b0s1"])})

    add("G4A_UNITS_045", bm([bar([seg("15 cm", 15, "a"), seg("5 cm", 5, "b")], brace="?")], note="A pencil and an eraser, end to end"),
        {0: bm([bar([seg("15 cm", 15, "a"), seg("5 cm", 5, "b")], brace="?")], note="End to end, the two lengths are added", hl=["b0"]),
         1: bm([bar([seg("15 cm", 15, "a"), seg("5 cm", 5, "b")], brace="20 cm")], hl=["b0"])})

    # ── Equal lots ──────────────────────────────────────────────────────────
    def lots(qid, n, each, before_brace, note, steps):
        """n equal pieces. steps: {index: (piece label, brace, note)}"""
        add(qid, bm([bar(equal_segs(n, each), brace=before_brace)], note=note),
            {i: bm([bar(equal_segs(n, s[0]), brace=s[1])], note=s[2], hl=["b0"]) for i, s in steps.items()})

    lots("G4A_UNITS_007", 6, "750 ml", "? litres", "6 packets of milk",
         {0: ("750 ml", "? litres", "First find the total: 6 lots of 750 ml"), 2: ("750 ml", "4.5 litres", "1000 ml = 1 litre")})
    lots("G4A_UNITS_012", 10, "250 mg", "? g", "A strip of 10 tablets",
         {0: ("250 mg", "2500 mg", "10 lots of 250 mg"), 2: ("250 mg", "2.5 g", "1000 mg = 1 g")})
    lots("G4A_UNITS_014", 5, "4 hm", "? km", "5 rounds of the track",
         {0: ("4 hm", "? km", "1 hm = 100 m, so one round is 4 × 100 m"), 1: ("4 hm", "? km", "Then 5 rounds"),
          2: ("4 hm", "2 km", "Sunil runs 2 km")})
    lots("G4A_UNITS_035", 3, "1 m", "? cm", None, {0: ("100 cm", "? cm", "One metre is 100 centimetres"), 1: ("100 cm", "300 cm", "3 × 100 = 300")})
    lots("G4A_UNITS_036", 5, "1 kg", "? g", None, {0: ("1000 g", "? g", "One kilogram is 1000 grams"), 1: ("1000 g", "5000 g", "5 × 1000 = 5000")})
    lots("G4A_UNITS_038", 2, "1 dozen", "? eggs", None, {0: ("12", "? eggs", "One dozen is 12"), 1: ("12", "24 eggs", "2 × 12 = 24")})
    lots("G4A_UNITS_044", 4, "2 litres", "Total = ?", "4 bottles of juice",
         {0: ("2 litres", "Total = ?", "4 lots of 2 litres, so multiply"), 1: ("2 litres", "8 litres", "4 × 2 = 8")})

    add("G4A_UNITS_037", None,
        {0: bm([bar(equal_segs(2, "1000 ml"), brace="2000 ml")], note="One litre is 1000 millilitres"),
         1: bm([bar(equal_segs(2, "1 litre"), brace="2000 ml = 2 litres")], note="2000 ÷ 1000 = 2", hl=["b0"])})

    # 3 m cut into 8 equal pieces.
    def plank(first, tone, brace, note=None, hl=None):
        return bm([bar(equal_segs(8, None, first_label=first, first_tone=tone), brace=brace)], note=note, hl=hl)
    add("G4A_UNITS_009", plank("?", "unknown", "3 m", note="8 equal pieces"),
        {0: plank("?", "unknown", "3 m", note="1 m = 100 cm, so change 3 m into centimetres", hl=["b0"]),
         1: plank("?", "unknown", "3 m", note="Share the length equally among 8 pieces", hl=["b0s0"]),
         2: plank("37.5 cm", "a", "3 m", note="Each piece is 37.5 cm long", hl=["b0s0"])})

    # There and back, 5 days.
    add("G4A_UNITS_008", journey(["Home", "School"], [{"top": "850 m"}], note="There and back, on each of the 5 school days"),
        {0: bm([bar([seg("850 m there", 1, "a"), seg("850 m back", 1, "b")], brace="One day")], note="One day is there and back"),
         1: bm([bar(equal_segs(5, "one day"), brace="5 days")], note="Then 5 days of walking"),
         2: bm([bar(equal_segs(5, "one day"), brace="8.5 km")], note="Ravi walks 8.5 km in the week", hl=["b0"])})

    # A trek in three stretches.
    def trek(a, b, c, note=None, hl=None):
        return journey(["Start", "Breakfast", "Lunch", "Evening"], [{"top": a}, {"top": b}, {"top": c}], note=note, hl=hl)
    add("G4A_UNITS_016", trek("2 km 75 m", "850 m", "1.5 km", note="Total distance = ? km"),
        {0: trek("2075 m", "850 m", "1500 m", note="Write each distance in metres", hl=["l0", "l2"]),
         1: trek("2075 m", "850 m", "1500 m", note="Add the three distances", hl=["l0", "l1", "l2"]),
         2: trek("2075 m", "850 m", "1500 m", note="Arjun walks 4.425 km in all")})

    # How many fit: measurement division with a small piece and the rest.
    def fit(piece, piece_units, rest, rest_units, brace, note=None, hl=None):
        return bm([bar([seg(piece, piece_units, "a"), seg(rest, rest_units, "unknown")], brace=brace)], note=note, hl=hl)
    add("Q_CH11_019", fit("125 ml", 125, "? bottles", 2375, "2.5 litres", note="Each bottle holds 125 ml"),
        {0: fit("125 ml", 125, "? bottles", 2375, "2500 ml", note="2.5 litres is 2.5 × 1000 = 2500 ml", hl=["b0"]),
         1: fit("125 ml", 125, "? bottles", 2375, "2500 ml", note="125 × 20 = 2500, so 20 bottles", hl=["b0s0"])})
    add("G4A_UNITS_015", fit("1 dozen", 12, "? boxes", 138, "150 laddoos", note="Laddoos come only in boxes of one dozen"),
        {0: fit("12", 12, "? boxes", 138, "150 laddoos", note="1 dozen = 12. Divide 150 by 12.", hl=["b0s0"]),
         1: bm([bar([seg("12 boxes: 144", 144, "a"), seg("6", 6, "b")], brace="150 laddoos")],
               note="12 boxes hold 144, so 6 more laddoos are needed", hl=["b0s1"]),
         2: bm([bar([seg("12 boxes: 144", 144, "a"), seg("6", 6, "b")], brace="150 laddoos")],
               note="The last 6 need one more box: 13 boxes", hl=["b0"])})

    # Pipe 12 m cut into 1 m 50 cm pieces.
    add("G4A_UNITS_027",
        bm([bar([seg("1 m 50 cm", 1.5, "a"), seg("1 m 50 cm", 1.5, "a"), seg("and so on", 9, "unknown")], brace="12 m")],
           note="Each cut takes 4 minutes"),
        {1: bm([bar(equal_segs(8, "1 m 50 cm"), brace="12 m")], note="8 pieces: count the cuts between them"),
         3: bm([bar(equal_segs(8, "1 m 50 cm"), brace="12 m")], note="All the cutting takes 28 minutes")})

    # Fence 20 m, posts every 2 m 50 cm.
    add("G4A_UNITS_021",
        bm([bar([seg("2 m 50 cm", 2.5, "a"), seg("2 m 50 cm", 2.5, "a"), seg("and so on", 15, "unknown")], brace="20 m")],
           note="A post stands at each end and at every join"),
        {0: bm([bar([seg("250 cm", 2.5, "a"), seg("250 cm", 2.5, "a"), seg("and so on", 15, "unknown")], brace="2000 cm")],
               note="20 m = 2000 cm and 2 m 50 cm = 250 cm"),
         1: nl(0, 20, 2.5, ticks="ends", note="Count the gaps between the marks"),
         2: nl(0, 20, 2.5, ticks="ends", note="Each mark is a post: one more than the gaps"),
         3: nl(0, 20, 2.5, ticks="ends", note="There are 9 posts")})

    # Juice in 8 glasses, 3 drunk.
    add("G4A_UNITS_022", fb([(8, 3, "1 litre 200 ml")], note="8 equal glasses. The shaded 3 are drunk."),
        {0: fb([(8, 3, "1200 ml")], note="1 litre 200 ml = 1200 ml"),
         2: fb([(8, 3, "1200 ml")], note="8 − 3 = 5 glasses are left", hl=["b0"]),
         3: fb([(8, 3, "1200 ml")], note="The 5 glasses hold 750 ml = 0.75 litres", hl=["b0"])})

    # Frog in a well.
    def well(points=None, hops=None, note=None):
        return nl(0, 260, 10, ticks="ends", points=points, hops=hops, note=note)
    add("G4A_UNITS_025",
        well(hops=[(0, 50, "up 50 cm")], note="Each night it slips back 20 cm. The well is 2 m 60 cm deep."),
        {0: well(points=[(30, "30 cm")], hops=[(0, 50, "+50"), (50, 30, "−20")], note="One day and night: up 30 cm"),
         1: well(points=[(210, "210 cm")], hops=[(0, 210, "7 days and nights")], note="7 lots of 30 cm take it to 210 cm"),
         2: well(points=[(210, "210 cm")], hops=[(0, 210, "7 days and nights"), (210, 260, "+50")],
                 note="The next climb of 50 cm reaches the top at 260 cm"),
         3: well(points=[(210, "210 cm")], hops=[(0, 210, "7 days and nights"), (210, 260, "+50")], note="Out on the 8th day")})

    # Smallest number that is both dozens and scores.
    add("G4A_UNITS_020", None,
        {1: nl(0, 60, 10, points=[(20, None), (40, None), (60, None)], note="Multiples of 20: which one can 12 divide?"),
         2: bm([bar(equal_segs(5, "12"), label="Pencils"), bar(equal_segs(3, "20", tone="b"), label="Erasers")],
               note="Packets of 12 and packets of 20 both reach 60")})

    # Which length is greatest.
    head = ["Length", "In metres"]
    add("G4A_UNITS_011", None,
        {0: table([["1.08 km", "1080 m"], ["1 km 800 m", "1800 m"]], headers=head),
         1: table([["1.08 km", "1080 m"], ["1 km 800 m", "1800 m"], ["1008 m", "1008 m"], ["10800 cm", "108 m"]], headers=head),
         2: {"kind": "barChart", "unit": "m", "highlight": ["b1"], "note": "The greatest is 1800 m, which is 1 km 800 m",
             "bars": [{"label": "1.08 km", "value": 1080}, {"label": "1 km 800 m", "value": 1800},
                      {"label": "1008 m", "value": 1008}, {"label": "10800 cm", "value": 108}]}})

    # Three parcels.
    head = ["Parcel", "In grams"]
    weights = [["2.4 kg", "2400 g"], ["2 kg 50 g", "2050 g"], ["2450 g", "2450 g"]]
    add("G4A_UNITS_026", None,
        {0: table([["2.4 kg", "?"], ["2 kg 50 g", "?"], ["2450 g", "2450 g"]], headers=head, note="Change each weight into grams"),
         1: table(weights, headers=head, note="Lightest 2050 g, heaviest 2450 g", hl=["r1", "r2"]),
         2: table(weights, headers=head, note="Add the lightest and the heaviest", hl=["r1", "r2"]),
         3: table(weights, headers=head, note="Together 4500 g, which is 4.5 kg", hl=["r1", "r2"])})

    # ── Dozens and scores as sets and fractions ─────────────────────────────
    add("G4A_UNITS_039", fb([(2, 1, "1 dozen")], note="Half of the dozen is shaded"),
        {0: setf(12, item="bananas", note="One dozen is 12"),
         1: setf(12, groups=2, shaded=1, item="bananas", note="Half a dozen is 12 ÷ 2 = 6")})
    add("G4A_UNITS_046", setf(36, item="bananas", note="How many dozen is this?"),
        {0: setf(36, item="bananas", note="One dozen is 12 bananas"),
         1: setf(36, groups=3, item="bananas", note="36 ÷ 12 = 3 groups of a dozen")})
    # The next four follow the steps as rewritten in Nov 2026.
    add("Q_CH12_007", None,
        {0: setf(20, item="articles", note="1 score is 20 articles"),
         1: setf(20, groups=10, shaded=1, item="articles", note="Ten equal groups: one tenth of 20 is 2", hl=["shaded"]),
         2: setf(20, groups=10, shaded=3, item="articles", note="Three tenths are 3 × 2 = 6 articles", hl=["shaded"])})
    add("Q_CH12_005", None,
        {1: fb([(8, 1, "1 litre = 1000 ml")], note="125 ml goes into 1000 ml exactly 8 times"),
         2: fb([(8, 1, "1 litre")], note="125 ml is 1 of the 8 equal parts, so it is 1/8 l", hl=["b0"])})
    add("Q_CH12_008", None,
        {0: fb([(12, 12, "1 gross")], note="1 gross is 12 dozens: each piece is one dozen"),
         1: fb([(12, 1, "1 gross")], note="One dozen is 1 of the 12 equal parts of a gross", hl=["b0"]),
         2: fb([(12, 1, "1 gross")], note="So 1/12 of a gross makes a dozen", hl=["b0"])})
    head = ["Pair", "How far apart"]
    pairs = [["kilogram & tonne", "1000 times"], ["metre & kilometre", "1000 times"], ["gram & decagram", "10 times"],
             ["centilitre & litre", "100 times"]]
    add("Q_CH12_004", None,
        {1: table(pairs[:2], headers=head, note="1 tonne is 1000 kg and 1 km is 1000 m"),
         2: table(pairs[:3], headers=head, note="1 decagram is 10 grams", hl=["r2"]),
         3: table(pairs, headers=head, note="1 litre is 100 centilitres", hl=["r3"])})
    return out


def main():
    questions = load(TOPIC)
    Q = {q["id"]: q for q in questions}
    out = {}
    for q in questions:
        for rule in RULES:
            e = rule(q)
            if e is not None and ("figure" in e or "stepFigures" in e):
                out[q["id"]] = e
                break
    for qid, e in authored(Q).items():
        out[qid] = e
    finish(TOPIC, questions, out, sys.argv)


if __name__ == "__main__":
    main()
