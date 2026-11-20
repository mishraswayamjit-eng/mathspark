"""Figures for Grade 4 "Operations & BODMAS" (node gr4_operations).

    python -X utf8 scripts/figures/authoring/g4_gr4_operations.py            # write the part file
    python -X utf8 scripts/figures/authoring/g4_gr4_operations.py review     # ... and print every figure beside its question
    python -X utf8 scripts/figures/authoring/g4_gr4_operations.py review PYQ # ... only ids matching a pattern
    python -X utf8 scripts/figures/authoring/g4_gr4_operations.py missing    # ... and list the questions left without a figure

Writes data/question-figures/parts/g4-gr4_operations.json.

Most of this topic is bare arithmetic and order-of-operations sums, which get no picture.
Pictures go to: word problems (bar models, unitary tables), sums whose own steps hop along a
number line, and products whose own steps split a factor (shown as a bar cut in two).
"""
import re
import sys

from g4_gr4_operations_kit import (answer_text, bar, bm, entry, equal_segs, fb, finish, grid, journey, load, nl,
                                   num, seg, setf, step_figs, step_texts, table)

TOPIC = "gr4_operations"


# ── Rules: families that read their numbers from the question ────────────────

def split_step(st):
    """(step index, whole, part1, part2) for the first step that says 'Split A into B and C'."""
    for i, text in enumerate(st):
        m = re.search(r"Split (\d+) into (\d+) and (\d+)", text)
        if m:
            return i, int(m.group(1)), int(m.group(2)), int(m.group(3))
    return None


def rule_total_cost(q):
    """'Siya buys 11 stickers at Rs.25 each. What is the total cost?'"""
    m = re.search(r"buys (\d+) (\w+) at Rs\.(\d+) each\. What is the total cost", q["questionText"])
    if not m:
        return None
    n, item, price = int(m.group(1)), m.group(2), int(m.group(3))
    total = num(answer_text(q))
    if total != n * price:
        return None
    st = step_texts(q)
    lots = "%d %s at Rs.%d each" % (n, item, price)

    def row(brace, note=None, hl=None):
        return bm([bar(equal_segs(n, "Rs.%d" % price), brace=brace)], note=note, hl=hl)

    figure = row("Total = ?", note=lots) if n <= 12 else None
    figs = {}
    if n <= 12:
        figs[0] = row("Total = ?", note="%d lots of Rs.%d" % (n, price))
        figs[-1] = row("Rs.%d" % total, hl=["b0"])
    sp = split_step(st)
    if sp:
        i, whole, p1, p2 = sp
        other = price if whole == n else n
        # The step writes the two products out; read them from it.
        products = re.findall(r"(\d+) × (\d+) = (\d+)", st[i])
        if len(products) == 2 and int(products[0][2]) + int(products[1][2]) == total:
            a, b = int(products[0][2]), int(products[1][2])
            figs[i] = bm([bar([seg("%s × %s" % products[0][:2], a, "a"), seg("%s × %s" % products[1][:2], b, "b")],
                              brace="%d × %d" % (whole, other))],
                         note="Split %d into %d and %d" % (whole, p1, p2))
            if i + 1 < len(st) and "Add the two parts" in st[i + 1]:
                figs[i + 1] = bm([bar([seg(str(a), a, "a"), seg(str(b), b, "b")], brace="Rs.%d" % total)],
                                 note="%d + %d = %d" % (a, b, total), hl=["b0"])
                if i + 1 == len(st) - 1 or n > 12:
                    figs.pop(-1, None)
    return entry("rule", figure, step_figs(q, figs))


def rule_cost_of_one(q):
    """'If 24 pencils cost Rs.216, what is the cost of one pencil?'"""
    m = re.search(r"If (\d+) (\w+) cost Rs\.(\d+), what is the cost of one", q["questionText"])
    if not m:
        return None
    n, item, total = int(m.group(1)), m.group(2), int(m.group(3))
    one = num(answer_text(q))
    if one * n != total:
        return None
    share = "Share Rs.%d equally among %d" % (total, n)
    if n <= 12:
        brace = "%d %s: Rs.%d" % (n, item, total)

        def row(first, tone, every=None, note=None, hl=None):
            segs = equal_segs(n, every, first_label=first, first_tone=tone) if every is None else equal_segs(n, every)
            return bm([bar(segs, brace=brace)], note=note, hl=hl)

        figure = row("?", "unknown", note="Each of the %d %s costs the same" % (n, item))
        figs = {0: row("?", "unknown", note=share, hl=["b0s0"]),
                -1: row(None, None, every="Rs.%d" % one, note="One costs Rs.%d" % one)}
    else:
        head = [item.capitalize(), "Cost"]
        figure = table([[str(n), "Rs.%d" % total], ["1", "?"]], headers=head)
        figs = {0: table([[str(n), "Rs.%d" % total], ["1", "?"]], headers=head, note=share, hl=["r1"]),
                -1: table([[str(n), "Rs.%d" % total], ["1", "Rs.%d" % one]], headers=head, hl=["r1"])}
    return entry("rule", figure, step_figs(q, figs))


def rule_profit_loss(q):
    """'... buys a book for Rs.60 and sells it at a profit of 10%. What is the selling price?'"""
    m = re.search(r"for Rs\.(\d+) and (?:sells|sold) it at a (profit|loss) of (\d+)%\. What is the selling price",
                  q["questionText"])
    if not m:
        return None
    cp, kind, pct = int(m.group(1)), m.group(2), int(m.group(3))
    change = cp * pct // 100
    sp = cp + change if kind == "profit" else cp - change
    if cp * pct % 100 or num(answer_text(q)) != sp or len(step_texts(q)) != 2:
        return None
    if kind == "profit":
        def model(change_label, tone, brace, note=None, hl=None):
            return bm([bar([seg("Rs.%d" % cp, cp, "a")], label="Cost"),
                       bar([seg("Rs.%d" % cp, cp, "a"), seg(change_label, change, tone)], label="Selling", brace=brace)],
                      note=note, hl=hl)
        figure = model("+%d%%" % pct, "unknown", "?", note="The profit is %d%% of Rs.%d" % (pct, cp))
        figs = {0: model("Rs.%d" % change, "b", "?", note="Profit = %d%% of Rs.%d" % (pct, cp), hl=["b1s1"]),
                1: model("Rs.%d" % change, "b", "Rs.%d" % sp, note="%d + %d = %d" % (cp, change, sp), hl=["b1"])}
    else:
        def model(sp_label, sp_tone, loss_label, note=None, hl=None):
            return bm([bar([seg(sp_label, sp, sp_tone), seg(loss_label, change, "b")], brace="Cost Rs.%d" % cp)],
                      note=note, hl=hl)
        figure = model("Selling = ?", "unknown", "%d%% loss" % pct, note="The loss is %d%% of Rs.%d" % (pct, cp))
        figs = {0: model("Selling = ?", "unknown", "Rs.%d" % change, note="Loss = %d%% of Rs.%d" % (pct, cp), hl=["b0s1"]),
                1: model("Rs.%d" % sp, "a", "Rs.%d" % change, note="%d − %d = %d" % (cp, change, sp), hl=["b0s0"])}
    return entry("rule", figure, step_figs(q, figs))


def rule_number_line(q):
    """'62 - 3 = ?' and '49 + 4 = ?': small hops along a number line, as the steps describe."""
    m = re.match(r"^(\d+) ([+\-−]) (\d+) = \?$", q["questionText"].strip())
    if not m:
        return None
    a, plus, b = int(m.group(1)), m.group(2) == "+", int(m.group(3))
    res = a + b if plus else a - b
    st = step_texts(q)
    if num(answer_text(q)) != res or res < 0 or len(st) < 2:
        return None
    count_up = (not plus) and st[0].startswith("Count up from")
    if b > 10 and not (count_up and res <= 8):
        return None
    lo = max(0, 5 * (((b if count_up else min(a, res)) - 2) // 5))
    hi = 5 * (-(-(max(a, res) + 2) // 5))
    sign = "+" if plus else "−"

    def line(points=None, hops=None, note=None):
        return nl(lo, hi, 1, points=points, hops=hops, note=note)

    if count_up:
        # '46 - 41': the steps count up from 41 to 46.
        figure = line(points=[(b, str(b)), (a, str(a))], note="How many steps is it from %d up to %d?" % (b, a))
        unit = [(n, n + 1) for n in range(b, a)]
        figs = {0: line(points=[(b, str(b)), (a, str(a))], hops=unit, note="Count the hops from %d up to %d" % (b, a)),
                -1: line(points=[(b, str(b)), (a, str(a))], hops=[(b, a, "%d steps" % res)], note="%d − %d = %d" % (a, b, res))}
        return entry("rule", figure, step_figs(q, figs))

    figure = line(points=[(a, str(a))], note="Start at %d and hop %s %d" % (a, "on" if plus else "back", b))
    whole = [(a, res, "%s%d" % (sign, b))]
    done = line(points=[(a, str(a)), (res, str(res))], hops=whole, note="%d %s %d = %d" % (a, sign, b, res))
    tens = [t for t in range(10 * (min(a, res) // 10 + 1), max(a, res), 10)]
    if len(tens) == 1 and re.search(r"first to reach|takes you to", st[0]):
        # The steps go through the ten: 62 → 60 → 59.
        t = tens[0]
        first = (a, t, "%s%d" % (sign, abs(a - t)))
        second = (t, res, "%s%d" % (sign, abs(t - res)))
        figs = {0: line(points=[(a, str(a))], hops=[first], note="First hop to the round number"),
                1: line(points=[(a, str(a)), (res, str(res))], hops=[first, second],
                        note="Then hop the last %d" % abs(t - res))}
        if len(st) > 2:
            figs[-1] = done
    elif b <= 8 and re.match(r"Start at \d+ and count back", st[0]):
        # '7 - 5': the steps count back one at a time.
        unit = [(n, n - 1) for n in range(a, res, -1)]
        figs = {0: line(points=[(a, str(a))], hops=unit, note="Count back %d hops" % b), -1: done}
    else:
        figs = {0: line(points=[(a, str(a))], hops=whole, note="Hop %s %d from %d" % ("on" if plus else "back", b, a)),
                -1: done}
    return entry("rule", figure, step_figs(q, figs))


def rule_product(q):
    """'75 × 45 = ?': when the steps split a factor, show the product as a bar cut in two."""
    m = re.match(r"^(\d+) × (\d+) = \?$", q["questionText"].strip())
    if not m:
        return None
    a, b = int(m.group(1)), int(m.group(2))
    prod = a * b
    st = step_texts(q)
    if num(answer_text(q)) != prod:
        return None
    last = len(st) - 1
    whole = "%d × %d" % (a, b)
    result = "%d × %d = %d" % (a, b, prod)

    if prod <= 12 and re.search(r"means %d groups of %d" % (a, b), st[0]):
        # A tiny fact: rows of squares. Shown only once the child has answered.
        return entry("rule", None, step_figs(q, {0: grid(a, b, note="%d rows of %d squares" % (a, b))}))

    sp = split_step(st)
    if sp and sp[0] == 0 and sp[1] in (a, b) and sp[2] + sp[3] == sp[1] and last >= 2:
        _, whole_n, p1, p2 = sp
        if whole_n == b:
            labels = ["%d × %d" % (a, p1), "%d × %d" % (a, p2)]
        else:
            labels = ["%d × %d" % (p1, b), "%d × %d" % (p2, b)]

        def cut(brace, hl, note=None):
            return bm([bar([seg(labels[0], p1, "a"), seg(labels[1], p2, "b")], brace=brace)], note=note, hl=hl)

        figs = {0: cut(whole, ["b0s0"], note="Split %d into %d and %d" % (whole_n, p1, p2)),
                1: cut(whole, ["b0s1"])}
        if last >= 3:
            figs[2] = cut(whole, ["b0s0", "b0s1"], note="Add the two parts")
        figs[last] = cut(result, ["b0"])
        return entry("rule", None, step_figs(q, figs))

    m0 = re.match(r"Work out (\d+) lots of (\d+)\.", st[0])
    if m0 and last == 2 and int(m0.group(2)) == b:
        k = int(m0.group(1))
        if k == a + 1 and a <= 30 and "one lot fewer" in st[1]:
            def lots(brace, hl=None, note=None):
                return bm([bar([seg("%d lots of %d" % (a, b), a, "a"), seg(str(b), 1, "b")], brace=brace)], note=note, hl=hl)
            return entry("rule", None, step_figs(q, {
                0: lots("%d lots of %d" % (k, b), hl=["b0"]),
                1: lots("%d lots of %d" % (k, b), hl=["b0s1"], note="Take one lot of %d away" % b),
                2: lots("%d lots of %d" % (k, b), hl=["b0s0"], note=result)}))
        if k == 2 * a and "half of" in st[1]:
            def halves(hl=None, note=None):
                return bm([bar([seg("%d lots of %d" % (a, b), 1, "a"), seg("%d lots of %d" % (a, b), 1, "b")],
                               brace="%d lots of %d" % (k, b))], note=note, hl=hl)
            return entry("rule", None, step_figs(q, {
                0: halves(hl=["b0"]),
                1: halves(hl=["b0s0"], note="%d is half of %d, so halve it" % (a, k)),
                2: halves(hl=["b0s0"], note=result)}))
    return None


RULES = [rule_total_cost, rule_cost_of_one, rule_profit_loss, rule_number_line, rule_product]


# ── Individually drawn questions ─────────────────────────────────────────────

def authored(Q):
    """Q maps id to question. Returns {id: entry}."""
    out = {}

    def add(qid, figure=None, figs=None):
        out[qid] = entry("authored", figure, step_figs(Q[qid], figs or {}))

    # Cough syrup: 150 ml, 25 ml a day.
    add("PYQ_2016_Q09",
        bm([bar([seg("25 ml", 25, "a"), seg("? days", 125, "unknown")], brace="150 ml")], note="25 ml is taken each day"),
        {0: bm([bar([seg("25 ml", 25, "a"), seg("? days", 125, "unknown")], brace="150 ml")],
               note="How many lots of 25 ml are in 150 ml?", hl=["b0s0"]),
         1: nl(0, 150, 25, hops=[(n, n + 25) for n in range(0, 150, 25)], note="Count the hops of 25 up to 150"),
         2: bm([bar(equal_segs(6, "25 ml"), brace="150 ml")], note="6 lots of 25 ml, one for each day")})

    # Three baskets: C = 22, A = C + 16, B = (A + C) + 12.
    def baskets(note=None, hl=None):
        c, a = 22, 22 + 16
        return bm([bar([seg("22", c, "a")], label="C"),
                   bar([seg("same as C", c, "a"), seg("16 more", 16, "b")], label="A"),
                   bar([seg("same as A", a, "c"), seg("same as C", c, "a"), seg("12 more", 12, "b")], label="B")],
                  note=note, hl=hl)
    add("PYQ_2016_Q12", baskets(note="How many oranges are there in all three baskets?"),
        {0: baskets(note="A has 16 more than C", hl=["b1"]),
         1: baskets(note="Put A and C together", hl=["b0", "b1"]),
         2: baskets(note="B is A and C together, and 12 more", hl=["b2"]),
         3: baskets(note="Add all three baskets", hl=["b0", "b1", "b2"])})

    # Three and a quarter dozen (no digits in the question, so pictures come with the steps).
    add("PYQ_2019_Q38", None,
        {0: fb([(12, 12, "1 dozen"), (12, 12, "1 dozen"), (12, 12, "1 dozen")], note="3 dozen is 3 × 12 = 36"),
         1: fb([(4, 1, "1 dozen")], note="A quarter of a dozen is 12 ÷ 4 = 3", hl=["b0"]),
         2: fb([(12, 12), (12, 12), (12, 12), (12, 3)], note="36 + 3 = 39 articles", hl=["b3"])})

    # 12 dozen against 5 score.
    def dozen_score(more=None, note=None, hl=None):
        if more:
            top = bar([seg("same as Shail", 100, "a"), seg(more, 44, "unknown" if more == "?" else "b")], label="Raunak")
        else:
            top = bar([seg("12 dozen", 144, "a")], label="Raunak")
        return bm([top, bar([seg("5 score", 100, "c")], label="Shail")], note=note, hl=hl)
    add("EXT_G4_FP_2021_033", dozen_score(note="Who has more, and by how much?"),
        {0: dozen_score(note="A dozen is 12, so 12 dozen is 12 × 12", hl=["b0"]),
         1: dozen_score(note="A score is 20, so 5 score is 5 × 20", hl=["b1"]),
         2: dozen_score(more="?", note="Subtract to find how many more Raunak has", hl=["b0s1"]),
         3: dozen_score(more="44 more", note="Raunak has 44 more", hl=["b0s1"])})

    # Bananas: Rs.30 for half a dozen, how many for Rs.85.
    head = ["Bananas", "Cost"]
    add("EXT_G4_FP_2022_025", table([["half dozen", "Rs.30"], ["?", "Rs.85"]], headers=head),
        {0: table([["6", "Rs.30"], ["?", "Rs.85"]], headers=head, note="Half a dozen is 6 bananas", hl=["r0"]),
         1: table([["6", "Rs.30"], ["1", "?"], ["?", "Rs.85"]], headers=head, note="Price of one banana: 30 ÷ 6", hl=["r1"]),
         2: table([["6", "Rs.30"], ["1", "?"], ["?", "Rs.85"]], headers=head, note="Divide Rs.85 by the price of one banana", hl=["r2"]),
         3: table([["6", "Rs.30"], ["17", "Rs.85"]], headers=head, hl=["r1"])})

    # A gross of notebooks for Rs.2592, cost of 68.
    head = ["Notebooks", "Cost"]
    add("EXT_G4_FP_2023_010", table([["1 gross", "Rs.2592"], ["68", "?"]], headers=head),
        {0: table([["12 dozen", "Rs.2592"], ["68", "?"]], headers=head, note="One gross is 12 dozen: 12 × 12 notebooks", hl=["r0"]),
         1: table([["12 dozen", "Rs.2592"], ["1", "?"], ["68", "?"]], headers=head, note="First find the cost of one notebook", hl=["r1"]),
         2: table([["12 dozen", "Rs.2592"], ["1", "?"], ["68", "?"]], headers=head, note="Then multiply by 68", hl=["r2"]),
         3: table([["1 gross", "Rs.2592"], ["68", "Rs.1224"]], headers=head, hl=["r1"])})

    # (2012 + 689) − ? = 1789.
    def gap(label, tone, note=None, hl=None):
        return bm([bar([seg("1789", 1789, "a"), seg(label, 2012 + 689 - 1789, tone)], brace="2012 + 689")], note=note, hl=hl)
    add("EXT_G4_FP_2024_013", gap("?", "unknown", note="What must be taken away to leave 1789?"),
        {0: gap("?", "unknown", note="First add 2012 and 689 to find the whole bar", hl=["b0"]),
         1: gap("?", "unknown", note="The gap is the sum take away 1789", hl=["b0s1"]),
         2: gap("912", "b", note="Subtract 912", hl=["b0s1"])})

    # Working backwards: half and 2 more, twice, leaves 8.
    def mangoes(note=None, hl=None):
        return bm([bar([seg("half", 22, "a"), seg("2", 2, "a"), seg("left", 20, "b")], label="Morning", brace="Start = ?"),
                   bar([seg("half", 10, "a"), seg("2", 2, "a"), seg("8", 8, "c")], label="Afternoon")], note=note, hl=hl)

    def afternoon(brace=None, note=None, hl=None):
        return bm([bar([seg("half", 10, "a"), seg("2", 2, "a"), seg("8", 8, "c")], label="Afternoon", brace=brace)], note=note, hl=hl)

    def morning(first, brace, note=None, hl=None):
        return bm([bar([seg(first, 22, "a"), seg("2", 2, "a"), seg("20", 20, "b")], label="Morning", brace=brace)], note=note, hl=hl)
    add("G4A_OPERATIONS_017", mangoes(note="Each time he sells half and 2 more. 8 are left at the end."),
        {0: afternoon(note="8 and 2 together are the other half", hl=["b0s1", "b0s2"]),
         1: afternoon(brace="20", note="So 20 mangoes were left after the morning", hl=["b0"]),
         2: morning("half", "Start = ?", note="20 and 2 together are the other half", hl=["b0s1", "b0s2"]),
         3: morning("22", "44", note="44 mangoes at the start", hl=["b0"])})

    # Asha and Bela: 60 stickers, Asha gives 8, then equal.
    def girls(asha, bela, note=None, hl=None):
        return bm([bar(asha, label="Asha"), bar(bela, label="Bela")], note=note, hl=hl)
    add("G4A_OPERATIONS_018",
        girls([seg("?", 38, "unknown")], [seg(None, 22, "b")], note="60 stickers in all. Asha gives 8 to Bela, then they are equal."),
        {0: girls([seg("half of 60", 30, "a")], [seg("half of 60", 30, "b")], note="After the gift both girls have the same number"),
         1: girls([seg("30", 30, "a"), seg("8", 8, "c")], [seg("22", 22, "b")], note="Give the 8 stickers back to Asha", hl=["b0s1"]),
         2: girls([seg("30", 30, "a"), seg("8", 8, "c")], [seg("22", 22, "b")], note="Check: 22 + 8 = 30", hl=["b1"]),
         3: girls([seg("38", 38, "a")], [seg("22", 22, "b")], note="Asha had 38 stickers at first", hl=["b0"])})

    # 500 oranges in boxes of 24: the last box.
    def last_box(label, tone, note=None, hl=None):
        return bm([bar([seg("20 oranges", 20, "a"), seg(label, 4, tone)], brace="A box holds 24")], note=note, hl=hl)
    add("G4A_OPERATIONS_019", None,
        {1: last_box(None, "unknown", note="The last box has only 20 oranges in it"),
         2: last_box("?", "unknown", note="How many more to reach 24?", hl=["b0s1"]),
         3: last_box("4", "b", note="4 more oranges fill the box", hl=["b0s1"])})

    # 10 pencils (₹4) and pens (₹9) for ₹60.
    add("G4A_OPERATIONS_023",
        bm([bar(equal_segs(10, "?", tone="unknown"), brace="10 items cost ₹60")], note="A pencil costs ₹4 and a pen costs ₹9"),
        {0: bm([bar(equal_segs(10, "₹4"), brace="₹40")], note="Pretend all 10 are pencils"),
         1: bm([bar(equal_segs(10, "₹4"), brace="₹40, but he paid ₹60")], note="₹20 more is still needed"),
         2: bm([bar([seg("₹9", 1, "b")] + equal_segs(9, "₹4"), brace="₹40 + ₹5")], note="Each pencil swapped for a pen adds ₹5", hl=["b0s0"]),
         3: bm([bar([seg("₹9", 1, "b") for _ in range(4)] + equal_segs(6, "₹4"), brace="₹60")], note="4 pens and 6 pencils cost ₹60")})

    # 35 × 12 = 35 × 10 + 35 × ?
    def lots35(second, tone, note=None, hl=None):
        return bm([bar([seg("35 × 10", 10, "a"), seg(second, 2, tone)], brace="35 × 12")], note=note, hl=hl)
    add("Q_CH09_009", lots35("35 × ?", "unknown"),
        {0: lots35("35 × ?", "unknown", note="12 lots of 35, split into 10 lots and some more", hl=["b0s0"]),
         1: lots35("35 × 2", "b", note="12 is 10 and 2 more", hl=["b0s1"]),
         2: lots35("35 × 2", "b", note="10 lots of 35 and 2 lots of 35", hl=["b0"])})

    # 5 pens cost ₹35, what do 8 cost.
    def pens(first=None, second="8 pens: ?", note=None, hl=None):
        return bm([bar(equal_segs(5, None, first_label=first, first_tone="a"), brace="5 pens: ₹35"),
                   bar(equal_segs(8, None, tone="unknown"), brace=second)], note=note, hl=hl)
    add("Q_CH09_012", pens(),
        {0: pens(first="?", note="Share ₹35 equally among the 5 pens", hl=["b0s0"]),
         1: pens(first="?", note="8 pens cost 8 times as much as one pen", hl=["b1"]),
         2: pens(second="8 pens: ₹56", hl=["b1"])})

    # 3 notebooks at ₹45 and 2 pens at ₹12.
    def shopping(brace, note=None, hl=None):
        return bm([bar([seg("₹45", 45, "a") for _ in range(3)] + [seg("₹12", 12, "b") for _ in range(2)], brace=brace)],
                  note=note, hl=hl)
    add("Q_CH09_020", shopping("Total = ?", note="3 notebooks and 2 pens"),
        {0: shopping("Total = ?", note="The notebooks: 3 lots of ₹45", hl=["b0s0", "b0s1", "b0s2"]),
         1: shopping("Total = ?", note="The pens: 2 lots of ₹12", hl=["b0s3", "b0s4"]),
         2: shopping("Total = ?", note="Add the two costs", hl=["b0"]),
         3: shopping("₹159", hl=["b0"])})

    # 7 × ? = 91
    add("Q_CH09_025", bm([bar(equal_segs(7, "?", tone="unknown"), brace="91")], note="7 equal parts make 91"),
        {0: bm([bar([seg("70", 70, "a"), seg("21", 21, "b")], brace="91")], note="Split 91 into 70 and 21"),
         1: bm([bar([seg("70", 70, "a"), seg("21", 21, "b")], brace="91")], note="Divide the 70 by 7", hl=["b0s0"]),
         2: bm([bar([seg("70", 70, "a"), seg("21", 21, "b")], brace="91")], note="Divide the 21 by 7", hl=["b0s1"]),
         3: bm([bar(equal_segs(7, "13"), brace="91")], note="7 × 13 = 91")})

    # 1/2 + 1/3 × 6
    add("Q_CH09_006", None,
        {0: setf(6, groups=3, shaded=1, note="One third of 6 is 2"),
         1: fb([(2, 2), (2, 2), (2, 1)], shape="circle", note="2 wholes and a half")})

    # 3 gross of pencils, 5 dozen given away.
    def pencils(left, given, brace, note=None, hl=None):
        return bm([bar([seg(left, 372, "unknown" if "?" in left else "a"), seg(given, 60, "b")], brace=brace)], note=note, hl=hl)
    add("Q_CH12_025", pencils("? left", "5 dozen", "3 gross", note="5 dozen pencils are given away"),
        {0: pencils("? left", "5 dozen", "3 gross = 432", note="One gross is 144, so 3 gross is 432", hl=["b0"]),
         1: pencils("? left", "60", "432", note="5 dozen is 5 × 12 = 60", hl=["b0s1"]),
         2: pencils("372", "60", "432", note="432 − 60 = 372", hl=["b0s0"])})

    # 72 chocolates, 6 each.
    add("Q_CH14_024",
        bm([bar([seg("6", 6, "a"), seg("? students", 66, "unknown")], brace="72 chocolates")], note="Each student gets 6 chocolates"),
        {0: bm([bar([seg("6", 6, "a"), seg("? students", 66, "unknown")], brace="72 chocolates")],
               note="How many groups of 6 are there in 72?", hl=["b0s0"]),
         1: bm([bar([seg("10 groups of 6", 60, "a"), seg("2 groups", 12, "b")], brace="72 chocolates")],
               note="60 is 10 groups of 6, and 12 is 2 groups of 6"),
         2: bm([bar(equal_segs(12, "6"), brace="72 chocolates")], note="12 groups of 6, so 12 students")})

    # 240 km in 4 hours.
    trip = journey(["Start", "End"], [{"top": "240 km", "bottom": "4 hours"}], note="Average speed = ?")
    add("Q_DH_017", trip,
        {0: journey(["Start", "End"], [{"top": "240 km", "bottom": "4 hours"}], note="Speed is the distance divided by the time", hl=["l0"]),
         1: bm([bar(equal_segs(4, "1 hour"), brace="240 km")], note="Share 240 km equally among the 4 hours"),
         2: bm([bar(equal_segs(4, "60 km"), brace="240 km")], note="60 km in each hour")})
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
