"""Lessons by rule for the generated money-percent families.

Each rule matches one wording, reads the numbers out of the question, computes every
line, and returns a lesson. `rule_for(q)` returns (rule name, lesson) or None.
"""
import re

from money_percent_lib import (
    ANSWER, ASK, B, FIG, GIVEN, NOTE, RING, MARK, W, bar, bars, lesson, num, percent_steps,
    pick, rs, rupees, seg, sp, table, times_steps, two_bars,
)


def one(items):
    """pens -> pen."""
    return items[:-1] if items.endswith("s") else items


def last_nth(text, piece):
    """Which occurrence of `piece` is the last one on a line."""
    return text.count(piece)


def turn(qid):
    return pick(qid, "turn", ["Your turn next!", "Now you try one!", "You can do the next one yourself!"])


# ── Total cost: "Arjun buys 13 pens at Rs.5 each. What is the total cost?" ───

TOTAL = re.compile(r"^(\w+) buys (\d+) (\w+) at Rs\.(\d+) each\. What is the total cost\?$")


def total_cost(q, m):
    qid = q["id"]
    name, n, items, price = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
    item = one(items)
    cost = n * price
    beats = [
        B(pick(qid, "open", [
            "Here is %s's shopping. %d %s, at %s each. We want the total cost." % (name, n, items, rupees(price)),
            "%s is at the shop, buying %d %s. Each one costs %s. Let us find the total cost." % (name, n, items, rupees(price)),
            "%d %s, and every one costs %s. How much does %s pay altogether?" % (n, items, rupees(price), name),
        ]), GIVEN("q", "%d %s at %s each" % (n, items, rs(price))), W("q2", "Total cost = ?", label=True)),
        B(pick(qid, "bill", [
            "Let us lay it out like a shop bill. One %s costs %s, and there are %d of them." % (item, rupees(price), n),
            "A shopkeeper would write a bill like this. The price of one %s, how many, and a space for the cost." % item,
        ]), FIG("bill", table(["Item", "Each", "How many", "Cost"], [[items, rs(price), str(n), "?"]]))),
        ASK(qid, "a1", "So which sum gives the total cost?",
            "%d × %d" % (n, price), ["%d + %d" % (n, price), "%d − %d" % (max(n, price), min(n, price))],
            "Every one of the %d %s costs %s. That is %s, %d times over, so we multiply." % (n, items, rupees(price), rupees(price), n)),
    ]
    steps, last = times_steps(n, price, "t")
    for i, (say, ops) in enumerate(steps):
        if i == 0:
            say = pick(qid, "why", ["We multiply, because it is the same price again and again. ", "Same price, %d times, so it is a times sum. " % n]) + say
        beats.append(B(say, *ops))
    beats += [
        B(pick(qid, "ans", [
            "So the total cost is %s." % rupees(cost),
            "So %s pays %s altogether." % (name, rupees(cost)),
        ]), ANSWER("ans", "Total cost = %s" % rs(cost)), RING("ans", rs(cost)),
            FIG("bill", table(["Item", "Each", "How many", "Cost"], [[items, rs(price), str(n), rs(cost)]], highlight=["r0"]))),
        B("Let us check by sharing it back out. %s, in lots of %s, gives %d %s. It fits." % (rupees(cost), rupees(price), n, items),
          W("chk", "%d ÷ %d = %d" % (cost, price, n))),
        B(pick(qid, "sum", [
            "So for a shop sum like this, the cost of one, times how many, gives the total. ",
            "Remember it like this: price of one, times the number you buy, is the total cost. ",
        ]) + turn(qid)),
    ]
    return lesson(beats, "rule")


# ── Change: "... buys 5 books at Rs.8 each and pays Rs.65. How much change ...?" ──

CHANGE = re.compile(r"^(\w+) buys (\d+) (\w+) at Rs\.(\d+) each and pays Rs\.(\d+)\. How much change does \w+ get back\?$")


def change(q, m):
    qid = q["id"]
    name, n, items, price, paid = m.group(1), int(m.group(2)), m.group(3), int(m.group(4)), int(m.group(5))
    cost = n * price
    back = paid - cost
    assert back > 0, qid

    def bill(c, b, hl=None):
        extra = {"highlight": hl} if hl else {}
        return table(["Bill", "Rupees"], [["%d %s" % (n, items), c], ["Paid", rs(paid)], ["Change", b]], **extra)

    beats = [
        B(pick(qid, "open", [
            "%s buys %d %s at %s each, and hands over %s. We want the change that comes back." % (name, n, items, rupees(price), rupees(paid)),
            "Here is a shop sum with two parts. %d %s at %s each, and %s pays with %s. How much change?" % (n, items, rupees(price), name, rupees(paid)),
        ]), GIVEN("q", "%d %s at %s each. Pays %s." % (n, items, rs(price), rs(paid))), W("q2", "Change = ?", label=True)),
        B("Look at the bill. Some of the %s pays for the %s, and whatever is left comes back as change." % (rupees(paid), items),
          FIG("bill", bill("?", "?"))),
        ASK(qid, "a1", "What must we find first?",
            "the total cost of the %s" % items, ["%d − %d" % (paid, price), "%d + %d" % (paid, price)],
            "The shopkeeper keeps the price of all %d %s, not just one. So first we need the total cost." % (n, items)),
    ]
    steps, last = times_steps(n, price, "c")
    for i, (say, ops) in enumerate(steps):
        if i == 0:
            say = "%d %s at %s each: that is %d times %d. " % (n, items, rupees(price), n, price) + say
        beats.append(B(say, *ops))
    take = pick(qid, "take", [
        "%d take away %d leaves %d." % (paid, cost, back),
        "From %d, take off the %d. That leaves %d." % (paid, cost, back),
    ]) if back > 10 else "Count up from %d to %d. That is %d more." % (cost, paid, back)
    beats += [
        ASK(qid, "a2", "Careful: %d is only the cost, not the answer. %s paid %d. So how do we find the change?" % (cost, name, paid),
            "%d − %d" % (paid, cost), ["%d + %d" % (paid, cost), "%d is the change" % cost],
            "Change is what is left of the money paid, once the cost is taken out. So we take %d away from %d." % (cost, paid),
            FIG("bill", bill(rs(cost), "?", ["r0"]))),
        B(take, W("s", "%d − %d = %d" % (paid, cost, back)),
          NOTE("s", str(paid), "paid"), NOTE("s", "− %d" % cost, "cost")),
        B("So %s gets %s back." % (name, rupees(back)),
          ANSWER("ans", "Change = %s" % rs(back)), RING("ans", rs(back)),
          FIG("bill", bill(rs(cost), rs(back), ["r2"]))),
        B(pick(qid, "chk", [
            "Check it the shopkeeper's way. The cost, %d, plus the change, %d, should make the %d that was paid. It does." % (cost, back, paid),
            "A quick check. Cost plus change should give back the money paid: %d plus %d is %d. It works." % (cost, back, paid),
        ]), W("chk", "%d + %d = %d" % (cost, back, paid))),
        B(pick(qid, "sum", [
            "So a change sum takes two moves. First find the total cost. Then take it away from the money paid. ",
            "Two moves, every time: work out the total cost, then subtract it from what was paid. ",
        ]) + turn(qid)),
    ]
    return lesson(beats, "rule")


# ── Cost of one: "If 8 sharpeners cost Rs.24, what is the cost of one sharpener?" ──

UNIT = re.compile(r"^If (\d+) (\w+) cost Rs\.(\d+), what is the cost of one (\w+)\?$")


def divide_steps(total, n):
    """total ÷ n (exact) for shop sums. Returns a list of (say, [ops])."""
    q = total // n
    assert q * n == total
    final = W("d9", "%d ÷ %d = %d" % (total, n, q))
    if q == 10:
        return [("%d is exactly %d tens. So %d divided by %d is 10." % (total, n, total, n), [final])]
    if n <= 10:
        return [("Think of the %d times table. %d times what makes %d? %d times %d is %d." % (n, n, total, n, q, total), [final])]
    if n % 10 == 0:
        t = total // 10
        k = n // 10
        return [
            ("Dividing by %d is easier in two steps: divide by 10, then by %d. First, %d divided by 10 is %d." % (n, k, total, t),
             [W("d1", "%d ÷ 10 = %d" % (total, t))]),
            ("Then %d divided by %d is %d. So %d divided by %d is %d." % (t, k, q, total, n, q),
             [W("d2", "%d ÷ %d = %d" % (t, k, q)), final]),
        ]
    if q == 3:
        return [("Count in lots of %d. %d, and %d more, and %d more, makes %d. That is 3 lots." % (n, n, n, n, total),
                 [W("d1", "%d + %d + %d = %d" % (n, n, n, total)), final])]
    if q == 9:
        ten = n * 10
        return [
            ("Try 10 lots first. %d times 10 is %d. That is a little too much." % (n, ten), [W("d1", "%d × 10 = %d" % (n, ten))]),
            ("Take one lot of %d off: %d minus %d is %d. So it is 9 lots, one fewer than 10." % (n, ten, n, total),
             [W("d2", "%d − %d = %d" % (ten, n, total)), final]),
        ]
    if q > 10:
        ten = n * 10
        left = total - ten
        more = left // n
        return [
            ("Try 10 lots first. %d times 10 is %d. That uses up most of the %d." % (n, ten, total), [W("d1", "%d × 10 = %d" % (n, ten))]),
            ("What is left? %d minus %d is %d, and that is %d more lots of %d." % (total, ten, left, more, n),
             [W("d2", "%d − %d = %d" % (total, ten, left)), W("d3", "%d ÷ %d = %d" % (left, n, more))]),
            ("10 lots and %d more lots make %d lots. So %d divided by %d is %d." % (more, q, total, n, q),
             [W("d4", "10 + %d = %d" % (more, q)), final]),
        ]
    tens, ones = (n // 10) * 10, n % 10
    a, b = tens * q, ones * q
    return [
        ("We need the number that, times %d, makes %d. Let us try %d. %d is %d and %d. %d times %d is %d, and %d times %d is %d."
         % (n, total, q, n, tens, ones, tens, q, a, ones, q, b),
         [W("d1", "%d × %d = %d" % (tens, q, a)), W("d2", "%d × %d = %d" % (ones, q, b))]),
        ("Together, %d plus %d is %d. It fits exactly. So %d divided by %d is %d." % (a, b, total, total, n, q),
         [W("d3", "%d + %d = %d" % (a, b, total)), final]),
    ]


def unit_cost(q, m):
    qid = q["id"]
    n, items, total, item = int(m.group(1)), m.group(2), int(m.group(3)), m.group(4)
    each = total // n
    if n <= 12:
        segments = [seg(1, "?") for _ in range(n)]
    else:
        segments = [seg(1, "?"), seg(1, "?"), seg(2, "..."), seg(1, "?")]
    brace = "%d %s: %s" % (n, items, rs(total))
    beats = [
        B(pick(qid, "open", [
            "%d %s cost %s altogether. We want the cost of just one %s." % (n, items, rupees(total), item),
            "Here we know the price of the whole lot: %d %s for %s. Our job is to find the price of one %s." % (n, items, rupees(total), item),
        ]), GIVEN("q", "%d %s cost %s" % (n, items, rs(total))), W("q2", "1 %s = ?" % item, label=True)),
        B(pick(qid, "bar", [
            "Picture the %s as one long bar, cut into %d equal pieces, one piece for each %s. Every %s costs the same." % (rupees(total), n, item, item),
            "Think of the %s as a bar shared into %d equal pieces. Each piece is the price of one %s." % (rupees(total), n, item),
        ]), FIG("bar", bars(bar(segments, None, brace)))),
        ASK(qid, "a1", "So which sum finds the cost of one %s?" % item,
            "%d ÷ %d" % (total, n), ["%d × %d" % (total, n), "%d − %d" % (total, n)],
            "We are sharing %s equally among %d %s. Sharing equally is dividing." % (rupees(total), n, items)),
    ]
    for say, ops in divide_steps(total, n):
        beats.append(B(say, *ops))
    beats += [
        B(pick(qid, "ans", [
            "So one %s costs %s." % (item, rupees(each)),
            "There it is: each %s costs %s." % (item, rupees(each)),
        ]), ANSWER("ans", "1 %s = %s" % (item, rs(each))), RING("ans", rs(each))),
        B("Check by building it back up. %d %s at %s each: %d times %d is %d. It fits." % (n, items, rupees(each), n, each, total),
          W("chk", "%d × %d = %d" % (n, each, total))),
        B(pick(qid, "sum", [
            "So when you know the cost of many and want the cost of one, divide the total by how many. ",
            "Cost of many, and you want the cost of one? Divide the total cost by the number of things. ",
        ]) + turn(qid)),
    ]
    return lesson(beats, "rule")


# ── Selling price after a profit or a loss per cent ──────────────────────────

PROFIT = re.compile(r"^(\w+) buys an? ([\w ]+) for Rs\.(\d+) and sells it at a profit of (\d+)%\. What is the selling price\?$")
LOSS = re.compile(r"^(\w+) bought an? ([\w ]+) for Rs\.(\d+) and sold it at a loss of (\d+)%\. What is the selling price\?$")


def selling_price(q, m, profit):
    qid = q["id"]
    name, thing, cp, p = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
    word = "profit" if profit else "loss"
    beats = [
        B(pick(qid, "open", [
            "%s pays %s for a %s. That is the cost price. It is sold at a %s of %d per cent, and we want the selling price." % (name, rupees(cp), thing, word, p),
            "The %s costs %s %s: that is the cost price. Then it is sold at a %s of %d per cent. What is the selling price?" % (thing, name, rupees(cp), word, p),
        ]), GIVEN("q", "Cost price %s. %s %d%%." % (rs(cp), word.capitalize(), p)), W("q2", "Selling price = ?", label=True)),
        B(pick(qid, "bars1", [
            "Here are two bars. The top one is the cost price, %s. The bottom one is the selling price, and we do not know it yet.",
            "Let us draw it as two bars. On top, the cost price: %s. Underneath, the selling price, which we have to find.",
            "Picture two bars, one under the other. The cost price, %s, is on top. The selling price is below, with a question mark for now.",
        ]) % rupees(cp),
          FIG("bars", two_bars(rs(cp), "?", word + " ?", p, profit))),
        B(pick(qid, "bars2", [
            "A profit means it is sold for more than it cost, so the bottom bar is longer. That extra bit on the end is the profit.",
            "With a profit, the selling price is bigger than the cost price. So the bottom bar sticks out, and the bit that sticks out is the profit.",
        ]) if profit else pick(qid, "bars2", [
            "A loss means it is sold for less than it cost, so the bottom bar is shorter. That missing bit is the loss.",
            "With a loss, the selling price is smaller than the cost price. So the bottom bar stops short, and the gap is the loss.",
        ]),
          FIG("bars", two_bars(rs(cp), "?", word + " ?", p, profit, hl=True))),
        ASK(qid, "a1", "The %s is %d per cent. But %d per cent of what?" % (word, p, p),
            "of the cost price, %s" % rs(cp), ["of the selling price", "of the %s" % word],
            "A %s is always measured against the money paid at the start. That is the cost price, %s." % (word, rupees(cp)),
            MARK("q", "%d%%" % p)),
        B(pick(qid, "trap", [
            "Careful, this is the classic trap. %s per cent is always worked out on the cost price, never on the selling price. And per cent means out of every 100." % word.capitalize(),
            "This is where many children slip. %s per cent is always taken on the cost price, not the selling price. And remember, per cent means out of every 100." % word.capitalize(),
        ]), W("pc", "%d%% = %d out of every 100" % (p, p), label=True), MARK("q", rs(cp), "box")),
    ]
    if cp == 100:
        v = p
        steps = [("And here the cost price is exactly 100 rupees. So %d out of every 100 is simply %s." % (p, rupees(p)),
                  [W("p1", "%d%% of 100 = %d" % (p, p))])]
    else:
        v, steps, _ = percent_steps(qid, p, cp, "p", unit="rupees")
    for i, (say, ops) in enumerate(steps):
        if i == len(steps) - 1:
            text = ops[-1]["text"]
            piece = "= %s" % num(v)
            ops = ops + [NOTE(ops[-1]["id"], piece, word, "below", last_nth(text, piece))]
            say = say + " That is the %s." % word
        beats.append(B(say, *ops))
    price = cp + v if profit else cp - v
    sign, wrong_sign = ("+", "−") if profit else ("−", "+")
    beats += [
        ASK(qid, "a2", "So the %s is %s. How do we get the selling price?" % (word, rupees(v)),
            "%d %s %s" % (cp, sign, num(v)), ["%d %s %s" % (cp, wrong_sign, num(v)), "%s is the selling price" % rs(v)],
            ("A profit means selling for more than was paid. So the profit is added on top of the cost price." if profit else
             "A loss means selling for less than was paid. So the loss is taken away from the cost price.")),
        B(("%d plus %s is %s. So the selling price is %s." if profit else "%d take away %s is %s. So the selling price is %s.")
          % (cp, sp(v), sp(price), rupees(price)),
          W("s", "%d %s %s = %s" % (cp, sign, num(v), num(price))),
          ANSWER("ans", "Selling price = %s" % rs(price)), RING("ans", rs(price)),
          FIG("bars", two_bars(rs(cp), rs(price), rs(v), p, profit))),
        B((pick(qid, "chk", [
            "Does that make sense? A profit should lift the selling price above the cost price, and %s is %s more than %d. It fits.",
            "Quick check. With a profit, the selling price must be bigger than the cost price. %s is %s above %d. Good.",
        ]) if profit else pick(qid, "chk", [
            "Does that make sense? A loss should drop the selling price below the cost price, and %s is %s less than %d. It fits.",
            "Quick check. With a loss, the selling price must be smaller than the cost price. %s is %s below %d. Good.",
        ])) % (sp(price), sp(v), cp),
          W("chk", ("%s − %d = %s" % (num(price), cp, num(v))) if profit else ("%d − %s = %s" % (cp, num(price), num(v))))),
        B(("So for a profit: find the per cent of the cost price, then add it on. " if profit else
           "So for a loss: find the per cent of the cost price, then take it away. ") + turn(qid)),
    ]
    return lesson(beats, "rule")


# ── A per cent of a quantity ─────────────────────────────────────────────────

GIRLS = re.compile(r"^Out of (\d+) students, (\d+)% are girls\. How many girls are there\?$")
MARKS = re.compile(r"^A test has (\d+) marks\. A student scored (\d+)%\. How many marks did the student score\?$")
PLAIN = re.compile(r"^What is (\d+)% of (\d+)\?$")


def whole_bar(p, base, brace):
    """The whole quantity cut into halves, quarters or tenths, with the pieces we want shaded."""
    if p == 50:
        return bars(bar([seg(1, num(base / 2.0) if base % 2 else str(base // 2), "b"), seg(1)], None, brace), note="2 equal pieces: each is 50%")
    if p in (25, 75):
        q = num(base / 4.0) if base % 4 else str(base // 4)
        k = p // 25
        return bars(bar([seg(1, q, "b") if i < k else seg(1) for i in range(4)], None, brace), note="4 equal pieces: each is 25%")
    tenth = num(base / 10.0) if base % 10 else str(base // 10)
    k = p // 10
    segments = [seg(1, tenth, "b") if i < k else seg(1) for i in range(10)]
    note = "10 equal pieces: each is 10%"
    if p % 10 == 5:
        segments[k] = seg(1, tenth if k == 0 else None, "c")
        note = "10 equal pieces: each is 10%. Half a piece is 5%"
    return bars(bar(segments, None, brace), note=note)


def percentage(q, kind, base, p):
    qid = q["id"]
    if kind == "girls":
        given, want, whole, part = "%d students. %d%% are girls." % (base, p), "Girls = ?", "students", "girls"
        opener = pick(qid, "open", [
            "There are %d students, and %d per cent of them are girls. We want the number of girls." % (base, p),
            "%d students in all, and %d per cent are girls. How many girls is that?" % (base, p),
        ])
        meaning = "Per cent means out of every 100. So %d per cent girls means %d girls in every 100 students." % (p, p)
        trap = "Careful: that does not mean %d girls altogether. It is %d in every 100, and here there are %d students." % (p, p, base)
    elif kind == "marks":
        given, want, whole, part = "Test: %d marks. Scored %d%%." % (base, p), "Marks scored = ?", "marks", "marks"
        opener = pick(qid, "open", [
            "The test is out of %d marks, and the student scored %d per cent. We want the actual marks." % (base, p),
            "A test with %d marks, and a score of %d per cent. How many marks is that?" % (base, p),
        ])
        meaning = "Per cent means out of every 100. So scoring %d per cent means getting %d marks for every 100 marks in the test." % (p, p)
        trap = "Careful: that does not mean %d marks altogether. It is %d for every 100, and this test has %d marks." % (p, p, base)
    else:
        given, want, whole, part = "%d%% of %d = ?" % (p, base), None, "", ""
        opener = pick(qid, "open", [
            "We want %d per cent of %d." % (p, base),
            "Here is a short one. What is %d per cent of %d?" % (p, base),
        ])
        meaning = "Per cent means out of every 100. So %d per cent means %d for every 100." % (p, p)
        trap = "Careful: the answer is not just %d. It is %d for every 100, and we have %d." % (p, p, base)
    first = [GIVEN("q", given)] + ([W("q2", want, label=True)] if want else [])
    beats = [
        B(opener, *first),
        B(meaning, W("pc", "%d%% = %d out of every 100" % (p, p), label=True),
          FIG("hundred", bars(bar([seg(p / 10.0, str(p), "b"), seg((100 - p) / 10.0)], None, "every 100")))),
    ]
    if base != 100:
        beats.append(B(trap, MARK("q", str(base))))
    brace = ("%d %s" % (base, whole)).strip()

    if base == 100:
        v = p
        beats.append(ASK(
            qid, "a1", "Now look at the whole: it is exactly 100. So how many is %d out of every 100 here?" % p,
            str(p), [num(p / 10.0), "100"],
            "When the whole is exactly 100, there is just one lot of 100. So %d per cent of it is simply %d." % (p, p)))
        beats.append(B("One lot of 100 gives %d, and there is only one lot here. So %d per cent of 100 is %d." % (p, p, p), W("p1", "%d%% of 100 = %d" % (p, p))))
        route = "hundred"
    else:
        v, steps, _ = percent_steps(qid, p, base, "p", unit=part)
        if p == 50:
            route = "half"
            beats.append(ASK(
                qid, "a1", "50 out of every 100. Which fraction is that?", "one half", ["one fifth", "one fiftieth"],
                "50 is half of 100. So 50 per cent is the same as one half."))
        elif p in (25, 75):
            route = "quarter"
            lead = "25 out of every 100. Which fraction is that?" if p == 25 else \
                "75 per cent is 3 lots of 25 per cent, so let us find 25 per cent first. 25 out of every 100 is which fraction?"
            ops = [] if p == 25 else [W("p0", "75% = 3 × 25%")]
            beats.append(ASK(
                qid, "a1", lead, "one quarter", ["one fifth", "one half"],
                "4 lots of 25 make 100. So 25 per cent is 1 out of 4 equal parts, and that is one quarter.", *ops))
        else:
            route = "tenth"
            tenth = base / 10.0
            if p == 10:
                beats.append(ASK(
                    qid, "a1", "10 per cent is 10 out of every 100, and that is one tenth. So what do we do to %d?" % base,
                    "divide by 10", ["divide by 100", "take away 10"],
                    "One tenth means 1 of 10 equal pieces. To cut %d into 10 equal pieces, we divide by 10." % base))
            else:
                beats.append(ASK(
                    qid, "a1", pick(qid, "ask10", [
                        "The friendly per cent to start from is 10 per cent. What is 10 per cent of %d?" % base,
                        "Let us start from an easy one. What is 10 per cent of %d?" % base,
                    ]), num(tenth), [num(base / 100.0), str(base - 10)],
                    "10 per cent is one tenth, so we divide by 10, not by 100. %d divided by 10 is %s." % (base, sp(tenth))))
        for i, (say, ops) in enumerate(steps):
            if i == (1 if route == "quarter" else 0):
                ops = ops + [FIG("whole", whole_bar(p, base, brace))]
            if i == 0 and route == "tenth":
                say = pick(qid, "t0", [
                    "%d divided by 10 is %s. So 10 per cent is %s. On the bar, that is 1 piece out of 10.",
                    "One tenth of %d is %s, so 10 per cent is %s. Look at the bar: it is 1 of the 10 equal pieces.",
                ]) % (base, sp(tenth), sp(tenth))
            if i == 0 and route == "quarter":
                say = "One quarter. And a quarter is half of a half, so we halve, and then halve again. Half of %d is %s." % (base, sp(base / 2.0))
            if i == 0 and route == "half":
                say = "One half. So we simply halve the number. Half of %d is %s." % (base, sp(v))
            beats.append(B(say, *ops))

    if kind == "girls":
        assert float(v) == int(v), qid
        answer = B("So there are %s girls." % sp(v), ANSWER("ans", "Girls = %s" % num(v)), RING("ans", num(v)))
    elif kind == "marks":
        answer = B("So the student scored %s marks." % sp(v), ANSWER("ans", "Marks scored = %s" % num(v)), RING("ans", num(v)))
    else:
        text = "%d%% of %d = %s" % (p, base, num(v))
        answer = B(pick(qid, "plainans", ["There is our answer: %s.", "And that is it: the answer is %s."]) % sp(v),
                   ANSWER("ans", text, label=False), RING("ans", num(v), text.count(num(v))))
    beats.append(answer)

    if base == 100:
        beats.append(B("Check with the picture. Out of 100, the shaded part is %d and the rest is %d. Together they make the whole 100." % (p, 100 - p),
                       W("chk", "%d + %d = 100" % (p, 100 - p))))
    elif base % 100 == 0:
        h = base // 100
        beats.append(B(pick(qid, "chk", [
            "Check it another way. %d is %d hundreds, and each hundred gives %d. %d times %d is %s. Same answer." % (base, h, p, h, p, sp(v)),
            "Let us check with hundreds. There are %d hundreds in %d, and each one gives %d. %d times %d is %s. It matches." % (h, base, p, h, p, sp(v)),
        ]), W("chk", "%d × %d = %s" % (h, p, num(v)))))
    elif route == "tenth":
        tenth = base / 10.0
        beats.append(B("Check the pieces. 10 pieces of %s should build the whole %d again. 10 times %s is %d. Good." % (sp(tenth), base, sp(tenth), base),
                       W("chk", "10 × %s = %d" % (num(tenth), base))))
    elif route == "quarter":
        qv = base / 4.0
        beats.append(B("Check the pieces. 4 quarters of %s should build the whole %d again. 4 times %s is %d. Good." % (sp(qv), base, sp(qv), base),
                       W("chk", "4 × %s = %d" % (num(qv), base))))
    else:
        beats.append(B("Check: two halves should make the whole. %s plus %s is %d. Good." % (sp(v), sp(v), base),
                       W("chk", "%s + %s = %d" % (num(v), num(v), base))))

    sums = {
        "hundred": "So remember: per cent means out of every 100. When the whole is exactly 100, the per cent is the answer. ",
        "half": "So remember: 50 per cent is one half. Just halve the number. ",
        "quarter": "So remember: 25 per cent is one quarter. Halve it, and halve it again. " if p == 25 else
                   "So remember: 25 per cent is one quarter, and 75 per cent is 3 of those quarters. ",
        "tenth": pick(qid, "sum", [
            "So remember: per cent means out of every 100. Find 10 per cent by dividing by 10, then build the per cent you need from it. ",
            "So the trick is: find 10 per cent first, by dividing by 10. Then build up the per cent you need. ",
        ]),
    }
    beats.append(B(sums[route] + turn(qid)))
    return lesson(beats, "rule")


# ── Simple interest, and the amount ──────────────────────────────────────────

SI_FIND = re.compile(r"^Find the simple interest on Rs\.(\d+) at (\d+)% per annum for (\d+) years\.$")
SI_AMOUNT = re.compile(r"^Rs\.(\d+) is invested at (\d+)% simple interest\. What is the amount after (\d+) years\?$")


def year_steps(h, r):
    """h hundreds, each earning r rupees: h × r, in steps a child can follow."""
    y = h * r
    final = W("y9", "%d × %d = %d" % (h, r, y))
    if h > 10 and h % 10 == 0:
        k = h // 10
        a = k * r
        return [("%d times %d is %d. So %d times %d is 10 times as much: %d." % (k, r, a, h, r, y),
                 [W("y1", "%d × %d = %d" % (k, r, a)), final])]
    if h > 10 and r > 10:
        rest = r - 10
        a, b = h * 10, h * rest
        return [
            ("%d is 10 and %d, so we take two easy bites. %d times 10 is %d, and %d times %d is %d." % (r, rest, h, a, h, rest, b),
             [W("y1", "%d × 10 = %d" % (h, a)), W("y2", "%d × %d = %d" % (h, rest, b))]),
            ("Together, %d plus %d makes %d. So %d times %d is %d." % (a, b, y, h, r, y),
             [W("y3", "%d + %d = %d" % (a, b, y)), final]),
        ]
    return [("%d times %d is %d." % (h, r, y), [final])]


def simple_interest(q, m, amount):
    qid = q["id"]
    P, R, T = int(m.group(1)), int(m.group(2)), int(m.group(3))
    assert P % 100 == 0 and 2 <= T <= 5, qid
    h = P // 100
    y = h * R
    I = y * T
    A = P + I
    if h <= 12:
        segments = [seg(1, "100") for _ in range(h)]
    else:
        segments = [seg(1, "100"), seg(1, "100"), seg(2, "..."), seg(1, "100")]
    hundreds = "1 hundred" if h == 1 else "%d hundreds" % h
    if amount:
        opener = pick(qid, "open", [
            "%s is invested at %d per cent simple interest for %d years. We want the amount at the end: everything that is there after %d years." % (rupees(P), R, T, T),
            "Someone puts %s in a bank at %d per cent simple interest, and leaves it for %d years. How much is there at the end? That is called the amount." % (rupees(P), R, T),
        ])
        first = [GIVEN("q", "%s at %d%% simple interest for %d years" % (rs(P), R, T)), W("q2", "Amount = ?", label=True)]
    else:
        opener = pick(qid, "open", [
            "%s is put in a bank, at %d per cent per annum, for %d years. Per annum just means every year. We want the simple interest: the extra money it earns." % (rupees(P), R, T),
            "Here %s earns simple interest at %d per cent per annum for %d years. Per annum means each year. How much extra money does it earn?" % (rupees(P), R, T),
        ])
        first = [GIVEN("q", "%s at %d%% per annum for %d years" % (rs(P), R, T)), W("q2", "Simple interest = ?", label=True)]
    beats = [
        B(opener, *first),
        B(pick(qid, "mean", [
            "%d per cent means %d out of every 100. So every 100 rupees earns %s in one year." % (R, R, rupees(R)),
            "What does %d per cent tell us? %d out of every 100. So in one year, every 100 rupees earns %s." % (R, R, rupees(R)),
        ]), W("m", "Every Rs.100 earns %s in 1 year" % rs(R), label=True), MARK("q", "%d%%" % R)),
        B(pick(qid, "hund", [
            "So how many hundreds are in %d? %d divided by 100 is %d. That is %s." % (P, P, h, hundreds),
            "Let us count the hundreds in %d. %d divided by 100 is %d, so there are %s." % (P, P, h, hundreds),
        ]), W("h", "%d ÷ 100 = %d" % (P, h)),
            FIG("hundreds", bars(bar(segments, None, "%s = %s" % (rs(P), hundreds)), note="Each 100 earns %s in a year" % rs(R)))),
        ASK(qid, "a1", "Each of the %s earns %s in a year. So which sum gives the interest for one year?" % (hundreds, rupees(R)),
            "%d × %d" % (h, R), ["%d + %d" % (h, R), "%d × %d" % (P, R)],
            "Every one of the %s earns %s. So that is %s, %d times over: %d times %d." % (hundreds, rupees(R), rupees(R), h, h, R)),
    ]
    ysteps = year_steps(h, R)
    for i, (say, ops) in enumerate(ysteps):
        if i == len(ysteps) - 1:
            say += " That is what one year earns: %s of interest." % rupees(y)
            ops = ops + [NOTE("y9", "= %d" % y, "1 year", "below")]
        beats.append(B(say, *ops))
    rows = [[str(i), rs(y)] for i in range(1, T + 1)]
    beats.append(B(pick(qid, "steady", [
        "Simple interest is steady. It earns the same %s every single year. Look at the table, one year at a time." % rupees(y),
        "The lovely thing about simple interest: every year earns exactly the same, %s. Here it is, a year at a time." % rupees(y),
    ]), FIG("years", table(["Year", "Interest"], rows))))
    total_ops = [W("i", "%d × %d = %d" % (T, y, I)), NOTE("i", "= %d" % I, "interest", "below")]
    if T == 2:
        total_say = "%d twice is %d. That is the interest for both years." % (y, I)
    else:
        total_say = "%d times %d is %d. That is the interest for all %d years." % (T, y, I, T)
    if amount:
        lead = "The money stays for 2 years, so the %d comes twice. " % y if T == 2 else "So we need %d, %d times over. " % (y, T)
        beats.append(B(lead + total_say, *total_ops))
    else:
        beats.append(ASK(qid, "a2", "So what is the interest for %s?" % ("both years" if T == 2 else "all %d years" % T),
                         "%d × %d" % (T, y), ["%d + %d" % (T, y), "just %d" % y],
                         "Each of the %d years adds another %s. So we need %d, %d times over." % (T, rupees(y), y, T)))
        beats.append(B(total_say, *total_ops))
    beats += [
        B(pick(qid, "formula", [
            "Here is the same idea as a formula. The money at the start is called the principal. Simple interest is principal, times rate, times time, divided by 100.",
            "Grown-ups write this as a formula. The starting money is the principal. Simple interest is principal, times rate, times time in years, divided by 100.",
        ]), W("f", "Simple interest = Principal × Rate × Time ÷ 100", label=True)),
        B("Put our numbers in. %d times %d times %d, divided by 100, comes to %d. The same answer, so we can trust it." % (P, R, T, I),
          W("f2", "%d × %d × %d ÷ 100 = %d" % (P, R, T, I)), NOTE("f2", str(P), "principal"), NOTE("f2", "× %d ×" % R, "rate")),
    ]
    if amount:
        beats += [
            ASK(qid, "a2", "Now, careful. The question asks for the amount after %d years. Is %d the amount?" % (T, I),
                "No: add back the %s" % rs(P), ["Yes: %s is the amount" % rs(I), "No: take it away from %s" % rs(P)],
                "%s is only the interest, the extra money. The amount is everything in the bank: the %s put in at the start, plus the interest." % (rupees(I).capitalize(), rupees(P))),
            B("%d plus %d is %d. So the amount after %d years is %s." % (P, I, A, T, rupees(A)),
              W("a", "%d + %d = %d" % (P, I, A)), NOTE("a", str(P), "principal"), NOTE("a", "+ %d" % I, "interest"),
              ANSWER("ans", "Amount = %s" % rs(A)), RING("ans", rs(A))),
            B(pick(qid, "sum", [
                "So: find what one year earns, multiply by the number of years, and for the amount, add the interest back on to the money at the start. ",
                "Three moves. Interest for one year, then for all the years, and then add it to the starting money to get the amount. ",
            ]) + turn(qid)),
        ]
    else:
        beats += [
            B("So the simple interest is %s." % rupees(I), ANSWER("ans", "Simple interest = %s" % rs(I)), RING("ans", rs(I))),
            B(pick(qid, "sum", [
                "So for simple interest: find what one year earns, then multiply by the number of years. The formula says the very same thing. ",
                "Two moves. First the interest for one year, then times the number of years. Or use the formula: principal, times rate, times time, divided by 100. ",
            ]) + turn(qid)),
        ]
    return lesson(beats, "rule")


# ── Which rule fits this question? ───────────────────────────────────────────

def rule_for(q):
    text = q["questionText"].strip()
    m = TOTAL.match(text)
    if m:
        return "total cost", total_cost(q, m)
    m = CHANGE.match(text)
    if m:
        return "change", change(q, m)
    m = UNIT.match(text)
    if m:
        return "cost of one", unit_cost(q, m)
    m = PROFIT.match(text)
    if m:
        return "profit: selling price", selling_price(q, m, True)
    m = LOSS.match(text)
    if m:
        return "loss: selling price", selling_price(q, m, False)
    m = GIRLS.match(text)
    if m:
        return "per cent of a group", percentage(q, "girls", int(m.group(1)), int(m.group(2)))
    m = MARKS.match(text)
    if m:
        return "per cent of marks", percentage(q, "marks", int(m.group(1)), int(m.group(2)))
    m = PLAIN.match(text)
    if m:
        return "per cent of a number", percentage(q, "plain", int(m.group(2)), int(m.group(1)))
    m = SI_FIND.match(text)
    if m:
        return "simple interest", simple_interest(q, m, False)
    m = SI_AMOUNT.match(text)
    if m:
        return "simple interest: amount", simple_interest(q, m, True)
    return None
