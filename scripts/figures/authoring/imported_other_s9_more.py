"""Simple interest, HCF stories, square arrangements, integers on a line, and a few textbook one-offs."""
import re
from math import gcd
from imported_other_lib import PROBLEMS, Q, commas, expect, key_numbers, model, says, staged, S, H, U

# ── Simple interest: the deposit, and one equal piece of interest for each year ──


def M(v, tag=""):
    return S("₹" + commas(v) + (" " + tag if tag else ""), v)


def interest(sid, P, r, t, ask, ans=None):
    """ask: 'interest' or 'amount'. The yearly interest pieces are drawn to scale (never thinner than a label needs)."""
    q = Q(sid)
    yearly = P * r / 100.0
    total, amount = yearly * t, P + yearly * t
    if not expect(q, ans if ans is not None else (total if ask == "interest" else amount), "simple interest"):
        return
    money = lambda v: "₹" + commas(v)

    def fig(piece, brace, note, hl=False):
        segs = [{"units": 10, "label": money(P), "tone": "a"}]
        segs += [{"units": round(max(1.2, 10.0 * yearly / P), 2), "label": piece, "tone": "unknown" if piece.endswith("%") else "b"} for _ in range(t)]
        bar = {"segments": segs}
        if brace:
            bar["brace"] = brace
        out = {"kind": "barModel", "bars": [bar], "note": note}
        if hl:
            out["highlight"] = ["b0s%d" % (i + 1) for i in range(t)]
        return out

    rate = "%s%%" % (int(r) if r == int(r) else r)
    brace = "?" if ask == "amount" else None
    before = fig(rate, brace, "Each small piece is one year's interest: %s of %s" % (rate, money(P)))
    stages = [
        (yearly, [fig(money(yearly), brace, "One year's interest: %s of %s = %s" % (rate, money(P), money(yearly)), True),
                  fig(rate, brace, "Work out one year's interest first", True)]),
        ((total, "final") if ask == "interest" else total, [
            fig(money(yearly), brace, "All the yearly pieces together: %s" % money(total), True),
            fig(rate, brace, "All the yearly pieces together: %s" % money(total), True),
            fig(rate, brace, "Add up the yearly pieces", True)]),
    ]
    if ask == "amount":
        stages.append(((amount, "final"), [
            fig(money(yearly), money(amount), "Deposit and interest together: %s" % money(amount)),
            fig(rate, money(amount), "Deposit and interest together: %s" % money(amount)),
            fig(rate, "?", "Add the interest to the deposit")]))
    staged(sid, before, stages)


interest("8515dcb63a22", 2500, 6, 2, "interest")
interest("ce5101471802", 3000, 8, 2, "amount", ans=280)
interest("e9ecedba89a4", 4000, 5, 3, "amount")
interest("bef1adb36e89", 4000, 5, 3, "amount", ans=100)
interest("26146e0fd3ae", 5000, 6, 3, "interest", ans=6)

# The rate or the number of years is the unknown: the interest is the "?" part of the amount.
model("295eeed4ec27", [("", [M(2000), U("?", 3)], ("₹2,480", 2480))], ans=lambda u: u * 100 / 2000,
      note="3 equal pieces, one for each year. What % of ₹2,000 is one piece?", unote="One year's interest: %s")
model("fd4b2c08666b", [("", [M(3500), U("? years × 8%")], ("₹4,340", 4340))], ans=lambda u: u / 280,
      note="How many years of 8% interest make up the ? piece?", unote="All the interest: %s")
model("d2266623d882", [("", [M(2500), U("? years × 8%")], ("₹3,100", 3100))], ans=lambda u: u / 200,
      note="How many years of 8% interest make up the ? piece?", unote="All the interest: %s")
model("4d7dc3aee230", [("", [M(5000), U("? years × 6%")], ("₹6,500", 6500))], ans=lambda u: u / 300,
      note="How many years of 6% interest make up the ? piece?", unote="All the interest: %s")

# Two banks side by side.
model("2a80ea906940", [("Bank A", [M(2000), H("10%", 200), H("10%", 200)]), ("Bank B", [M(3000), H("6%", 180), H("6%", 180)])],
      compare=False, ans=5760, note="2 years in each bank: one interest piece for each year")
model("957393b12eb2", [("Bank A", [M(1800), H("5%", 90), H("5%", 90)]), ("Bank B", [H("the rest", 1200), H("10%", 120), H("10%", 120)])],
      compare=False, ans=420, note="₹3,000 in all. 2 years in each bank: one interest piece a year")


# ── HCF stories: each amount as a bar; the answer is the biggest piece that measures them all ──

def hcf(sid, items, unit="", note=None):
    """items: [(name, amount)], amounts as the question states them."""
    q = Q(sid)
    h = 0
    for _, v in items:
        h = gcd(h, v)
    quotients = [v // h for _, v in items]
    if not ({float(h), float(sum(quotients))} | set(float(k) for k in quotients)) & key_numbers(q):
        PROBLEMS.append("%s: HCF %d and its quotients are not in the key %r" % (sid, h, q["options"]))
        return
    biggest = float(max(v for _, v in items))
    lab = lambda v: ("%d %s" % (v, unit)).strip()

    def fig(cut, note_, hl=None):
        bars = []
        for name, v in items:
            width = round(max(1.0, 12.0 * v / biggest), 2)
            if cut:
                k = v // h
                segs = [{"units": round(width / k, 2), "label": str(h), "tone": "a"} for _ in range(k)]
            else:
                segs = [{"units": width, "label": lab(v), "tone": "a"}]
            bars.append({"label": name, "segments": segs})
        out = {"kind": "barModel", "bars": bars, "note": note_}
        if hl:
            out["highlight"] = hl
        return out

    before = fig(False, note or "Split every bar into equal groups of the same size, as big as possible")
    alts = []
    if all(v // h <= 12 and 12.0 * v / biggest / (v // h) >= 0.2 for _, v in items):
        alts.append(fig(True, "Every bar is made of %ds: the biggest size that fits them all" % h))
    alts.append(fig(False, "Look for the biggest number that divides all of them exactly"))
    # The step that names the HCF (not an earlier one that merely lists it among the factors).
    staged(sid, before, [(r"(?:HCF|GCD|G\.C\.D|H\.C\.F|common)[^;]*?(?<![\d.])%d(?![\d.])" % h, alts)])


BAGS = "The same in every bag: as many bags as possible"
RIBBON = "Cut into equal pieces, as long as possible, with nothing left over"
hcf("7313a1159646", [("Ribbon 1", 84), ("Ribbon 2", 60)], "cm", RIBBON)
hcf("6edb34ac6ac4", [("Balls", 180), ("Bats", 240), ("Stumps", 300)], note="The same in every prize box: as many boxes as possible")
hcf("7f134649afbb", [("Strip 1", 126), ("Strip 2", 90)], "cm", RIBBON)
hcf("3a664ec058c6", [("Chocolates", 180), ("Toffees", 240), ("Biscuits", 300)], note=BAGS)
hcf("e642fc7f9564", [("Chocolates", 180), ("Toffees", 252), ("Biscuits", 324)], note=BAGS)
hcf("6f05c14318ec", [("Red balls", 168), ("White balls", 252), ("Tennis balls", 420)], note="The same in every kit: as many kits as possible")
hcf("20bec72811ac", [("Laddoos", 72), ("Barfis", 108), ("Kaju katlis", 90)], note=BAGS)
hcf("2a26f1aeebaf", [("Chocolates", 84), ("Toffees", 126), ("Biscuits", 210)], note=BAGS)
hcf("4609f5372d1b", [("Chocolates", 84), ("Toffees", 126), ("Biscuits", 210)], note=BAGS)
hcf("f32247e02337", [("Chocolates", 84), ("Sparklers", 60)], note=BAGS)
hcf("9d0868a1524d", [("Chocolates", 120), ("Diyas", 84), ("Stickers", 156)], note=BAGS)
hcf("d6fff9d3f4e1", [("Chocolates", 72), ("Toffees", 90)], note=BAGS)
hcf("aa8526e95db7", [("Toffees", 132), ("Stickers", 96), ("Erasers", 60)], note=BAGS)
hcf("cab70eaddbc2", [("Biscuits", 80), ("Cups of chai", 120)], note="The same on every plate: as many plates as possible")
hcf("b155779d975d", [("Chocolates", 84), ("Sparklers", 60)], note=BAGS)
hcf("4b96de676312", [("Coconut", 144), ("Jaggery", 108)], note="The same in every box: as many boxes as possible")
hcf("9d3c267122e1", [("Barfis", 84), ("Kaju katlis", 126), ("Laddoos", 210)], note=BAGS)
hcf("1b961dd959fc", [("Red balls", 168), ("White balls", 252), ("Tennis balls", 126)], note="The same in every kit bag: as many bags as possible")
hcf("549bbacfe704", [("Kaju laddoos", 60), ("Besan laddoos", 84)], note="The same in every box: as many boxes as possible")
hcf("420cdf0f5db8", [("Powders", 168), ("Diyas", 120), ("Candles", 96)], note="The same in every kit: as many kits as possible")
hcf("8275ff9d4359", [("Flowers", 108), ("Ribbons", 84)], note="The same in every bundle: as many bundles as possible")
hcf("15da60a30ab4", [("Chocolates", 36), ("Diyas", 54)], note=BAGS)
hcf("8f4dc69c30cc", [("Laddoos", 96), ("Chips packets", 72), ("Diyas", 48)], note="The same on every plate: as many plates as possible")
hcf("9884b16c964e", [("Biscuits", 156), ("Pakoras", 104)], note="The same in every box: as many boxes as possible")
hcf("5a867a94e72d", [("Priya's ribbon", 126), ("Arjun's ribbon", 84)], "cm", RIBBON)
hcf("d7b7676da6de", [("Jasmine", 150), ("Rose", 225)], note="The same in every bundle: as many bundles as possible")
hcf("e5da1f267719", [("Chocolates", 180), ("Toffees", 252), ("Biscuits", 324)], note=BAGS)
hcf("8302e1adbf64", [("First ribbon", 48), ("Second ribbon", 72), ("Third ribbon", 120)], "cm", RIBBON)
hcf("8ca00218f5ab", [("Samosas", 126), ("Gulab jamuns", 90)], note="The same on every plate: as many plates as possible")
hcf("41390c5d0d1a", [("Chocolates", 72), ("Toffees", 108), ("Diyas", 90)], note=BAGS)
hcf("38122be0cf0f", [("Wall 1", 120), ("Wall 2", 90)], "cm", "Square tiles, as big as possible, must fit both widths exactly")
hcf("aa8e59c1c907", [("Chocolates", 72), ("Rangoli packets", 108)], note=BAGS)
hcf("9cb1b090803d", [("Barfis", 120), ("Kaju katlis", 84), ("Gulab jamuns", 108)], note=BAGS)
hcf("05a8e1c0adb8", [("Roll 1", 180), ("Roll 2", 252)], "cm", RIBBON)
hcf("2e833319c14e", [("Tennis balls", 54), ("Rubber balls", 90)], note="The same in every group: as many groups as possible")
hcf("b0b4e7a67b66", [("Marigolds", 126), ("Jasmine", 84)], note="The same in every bouquet: as many bouquets as possible")
hcf("c74993dd62dd", [("Chocolates", 120), ("Diyas", 84), ("Stickers", 156)], note=BAGS)
hcf("c7a074e7342b", [("Red balls", 108), ("White balls", 90)], note="The same in every kit: as many kits as possible")
hcf("55c05a1c1335", [("Barfis", 84), ("Kaju katlis", 126), ("Gulab jamuns", 210)], note=BAGS)


# A floor to cover with the largest square tiles: the picture is the floor.
def floor(sid, length, breadth):
    h = gcd(length, breadth)
    base = {"kind": "rectangle", "length": "%d cm" % length, "breadth": "%d cm" % breadth,
            "proportion": round(min(3.0, max(1.0, float(length) / breadth)), 2)}
    stages = []
    if length // h <= 12 and breadth // h <= 12:
        stages.append((r"(?:HCF|GCD|common)[^;]*?(?<![\d.])%d(?![\d.])" % h, [
            dict(base, grid={"cols": length // h, "rows": breadth // h}, note="Square tiles of side %d cm fit exactly both ways" % h),
            dict(base, highlight=["length", "breadth"], note="The tile side must divide both the length and the breadth")]))
    staged(sid, dict(base, note="Whole square tiles, as large as possible, no cutting"), stages)


floor("3c42770cf2d3", 504, 360)
floor("ea2a0bb28b3b", 168, 120)


# ── Square arrangements ──────────────────────────────────────────────────────

def square(sid, inside=None, side=None, note=None, answer=None):
    """Either the count inside is given and the side is "?", or the side is given and the count is "?"."""
    base = {"kind": "rectangle", "square": True}
    before = dict(base, note=note)
    if inside:
        before.update(inside=inside, length="?")
    else:
        before.update(length=side, inside="?")
    stages = []
    if answer:
        done = dict(base, note=note)
        if inside:
            done.update(inside=inside, length=answer, highlight=["length"])
        else:
            done.update(length=side, inside=answer, highlight=["fill"])
        stages.append(((float(re.sub(r"[^\d.]", "", answer)), "final"), done))
    staged(sid, before, stages)


ROWS = "As many rows as there are in each row"
square("5f51d2dd081e", inside="225 players", note=ROWS, answer="15")
square("d38266802416", inside="196 diyas", note=ROWS, answer="14")
square("2c5423b7c938", inside="196 players", note=ROWS, answer="14")
square("27b47d5d3f45", inside="225 grains", note=ROWS, answer="15")
square("IPMTB_grade5_ch04_q009", inside="576 students", note=ROWS, answer="24")
square("IPMTB_grade5_ch04_q027", inside="625 students", note="As many rooms as there are students in each room", answer="25")
square("IPMTB_grade5_ch04_q028", inside="169 sq.cm", note="A square: all four sides are the same", answer="13 cm")
square("IPMTB_grade5_ch04_q010", side="21 cm", note="Area of the square = ?", answer="441")
square("IPMTB_grade5_ch04_q029", side="26 cm", note="Area of the square = ?", answer="676")
square("IPMTB_grade5_ch04_q005", side="31", note="31 rows with 31 students in each. How many in all?", answer="961")
square("IPMTB_grade5_ch04_q024", side="34", note="34 rooms with 34 boys in each. How many in all?", answer="1156")


# ── Triangular grounds (gr5_operations1): the picture is the ground ──────────

def ground(sid, sides, shape, total):
    base = {"kind": "triangle", "shape": shape, "sides": {"ab": sides[0], "bc": sides[1], "ca": sides[2]}}
    staged(sid, dict(base, note="Perimeter = once all the way round = ?"),
           [((total, "final"), dict(base, highlight=["ab", "bc", "ca"], note="Add the three sides: %d m" % total))])


ground("IPMTB_grade5_ch05_q006", ["225 m", "362 m", "289 m"], "scalene", 876)
ground("IPMTB_grade5_ch05_q037", ["230 m", "402 m", "270 m"], "scalene", 902)
ground("IPMTB_grade5_ch05_q032", ["223 m", "223 m", "223 m"], "equilateral", 669)


# ── Integers on a line (authored one by one) ─────────────────────────────────
# A point cannot be placed at a negative number (see the report), so the line is numbered and the note says where to start.

staged("62c081980083", {"kind": "numberLine", "min": -10, "max": 10, "step": 1,
                        "note": "Start at −3. Go up 8, then down 11. Where do you land?"}, [], origin="authored")
staged("82b0270c6447", {"kind": "numberLine", "min": -10, "max": 15, "step": 1, "points": [{"at": 0, "label": "soil"}, {"at": 14, "label": "stem tip"}],
                        "note": "The root tip is at −8. How far from root tip to stem tip?"}, [], origin="authored")
