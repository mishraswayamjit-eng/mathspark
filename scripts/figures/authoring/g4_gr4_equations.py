"""Figures for Grade 4 gr4_equations. Writes data/question-figures/parts/g4-gr4_equations.json.

    python -X utf8 scripts/figures/authoring/g4_gr4_equations.py

Rules first (one-letter equations read from the question text and solved here), then the
questions drawn one by one. Every balance is worked out for the solved value before it is
kept, and every bar is drawn from its pieces' true values.
"""
import re
from fractions import Fraction

from g4_gr4_equations_lib import (Part, S, V, Uq, B, bm, bal, nl, tb, rect, grid, n, step_text, step_latex,
                                  last_number, says, steps_of, key_numbers)

P = Part("gr4_equations")


# ── Rule: an equation with the letter on one side ────────────────────────────

def equation_in(text):
    t = text.split(":", 1)[1] if ":" in text else text
    return t.split(". ")[0].strip().rstrip(".?").strip().replace("−", "-")


def parse(e):
    """(letter, the steps that build the left side from the letter, right side) or None."""
    def sign(s):
        return "add" if s == "+" else "sub"
    m = re.fullmatch(r"(\d*)([a-zA-Z])\s*([+-])\s*(\d+)\s*=\s*(\d+)", e)
    if m:
        return m.group(2), ([("mul", int(m.group(1)))] if m.group(1) else []) + [(sign(m.group(3)), int(m.group(4)))], int(m.group(5))
    m = re.fullmatch(r"(\d+)([a-zA-Z])\s*=\s*(\d+)", e)
    if m:
        return m.group(2), [("mul", int(m.group(1)))], int(m.group(3))
    m = re.fullmatch(r"([a-zA-Z])/(\d+)\s*=\s*(\d+)", e)
    if m:
        return m.group(1), [("div", int(m.group(2)))], int(m.group(3))
    m = re.fullmatch(r"([a-zA-Z])/(\d+)\s*([+-])\s*(\d+)\s*=\s*(\d+)", e)
    if m:
        return m.group(1), [("div", int(m.group(2))), (sign(m.group(3)), int(m.group(4)))], int(m.group(5))
    m = re.fullmatch(r"(\d+)\s*\+\s*([a-zA-Z])\s*=\s*(\d+)", e)
    if m:
        return m.group(2), [("radd", int(m.group(1)))], int(m.group(3))
    m = re.fullmatch(r"(\d+)\s*-\s*([a-zA-Z])\s*=\s*(\d+)", e)
    if m:
        return m.group(2), [("rsub", int(m.group(1)))], int(m.group(3))
    m = re.fullmatch(r"(\d+)/([a-zA-Z])\s*=\s*(\d+)", e)
    if m:
        return m.group(2), [("rdiv", int(m.group(1)))], int(m.group(3))
    return None


def side(cur, ops, sub=False):
    """The left side written out: with the letter, or (sub) with a number in its place."""
    for kind, k in ops:
        if kind == "mul":
            cur = ("%d × %s" if sub else "%d%s") % (k, cur)
        elif kind == "div":
            cur = ("%s ÷ %d" if sub else "%s/%d") % (cur, k)
        elif kind == "add":
            cur = "%s + %d" % (cur, k)
        elif kind == "sub":
            cur = "%s − %d" % (cur, k)
        elif kind == "radd":
            cur = "%d + %s" % (k, cur)
        elif kind == "rsub":
            cur = "%d − %s" % (k, cur)
        elif kind == "rdiv":
            cur = ("%d ÷ %s" if sub else "%d/%s") % (k, cur)
    return cur


def undo_value(kind, k, v):
    if kind in ("add", "radd"):
        return v - k
    if kind == "sub":
        return v + k
    if kind == "mul":
        return Fraction(v) / k
    if kind == "div":
        return v * k
    if kind == "rsub":
        return k - v
    return Fraction(k) / v if v else Fraction(-1)


def undo_text(kind, k, p):
    return {"add": "%s − %d" % (p, k), "radd": "%s − %d" % (p, k), "sub": "%s + %d" % (p, k),
            "mul": "%s ÷ %d" % (p, k), "div": "%s × %d" % (p, k),
            "rsub": "%d − %s" % (k, p), "rdiv": "%d ÷ %s" % (k, p)}[kind]


MOVE = {"add": "Take %d from both pans", "radd": "Take %d from both pans", "sub": "Add %d to both pans",
        "mul": "Share both pans into %d equal parts", "div": "Make both pans %d times as heavy",
        "rsub": None, "rdiv": None}


def linear(qid, eq=None, origin="rule", extra=None, key=True, quiet=False):
    q = P.q(qid)
    got = parse(eq.replace("−", "-") if eq else equation_in(q["questionText"]))
    if not got:
        return False
    var, ops, c = got
    vals = [Fraction(c)]
    for kind, k in reversed(ops):
        vals.append(undo_value(kind, k, vals[-1]))
    ans = vals[-1]
    if ans.denominator != 1 or ans < 0 or (key and float(ans) not in key_numbers(q)):
        if not quiet:
            P.note(qid, "equation rule: solved value %s is not the key" % n(ans))
        return False
    env = {var: ans}
    nest = [n(c)]
    for j, (kind, k) in enumerate(reversed(ops)):
        nest.append(undo_text(kind, k, nest[-1] if j == 0 else "(%s)" % nest[-1]))

    before = bal(side(var, ops), n(c), env, note="Both pans weigh the same. Find %s." % var)
    figs, k, done = [], 0, False
    for i in range(len(steps_of(q))):
        text, latex = step_text(q, i), step_latex(q, i)
        if text.strip().lower().startswith("check"):
            figs.append(bal(side(n(ans), ops, True), n(c), {}, hl=["left"],
                            note="Put %s in place of %s: both pans match" % (n(ans), var)))
            continue
        result = last_number(latex) if latex else None
        if k < len(ops) and result is not None and abs(result - float(vals[k + 1])) < 1e-9:
            kind, kk = list(reversed(ops))[k]
            k += 1
            left = side(var, ops[:len(ops) - k])
            r_num = undo_text(kind, kk, n(vals[k - 1]))
            r_nest = nest[k]
            n_val = "%s = %s" % (left, n(vals[k]))
            n_move = (MOVE[kind] % kk) if MOVE[kind] else None
            alts = []
            for right in ([r_num] if r_num == r_nest else [r_num, r_nest]):
                alts.append(bal(left, right, env, note=n_val, hl=["right"]))
                alts.append(bal(left, right, env, note=n_move, hl=["right"]))
            figs.append(alts)
        elif k == len(ops) and not done and says(text, ans) and not latex:
            figs.append(bal(var, n(ans), env, note="%s = %s" % (var, n(ans)), hl=["right"]))
            done = True
        else:
            figs.append(None)
    for i, fig in (extra or {}).items():
        figs[i] = fig
    P.put(qid, before, figs, origin=origin)
    return True


for _qid in sorted(P.qs):
    linear(_qid, quiet=True)

# Square-root variants: "If √x + 1 = 6, find x."
for _qid, _q in sorted(P.qs.items()):
    _m = re.fullmatch(r"If √x \+ (\d+) = (\d+), find x\.", _q["questionText"])
    if _m and len(steps_of(_q)) == 2:
        _b, _c = int(_m.group(1)), int(_m.group(2))
        _r = _c - _b
        _env = {"x": _r * _r}
        if float(_r * _r) in key_numbers(_q):
            P.put(_qid, bal("√x + %d" % _b, n(_c), _env, note="Both pans weigh the same. Find x."),
                  [bal("√x", n(_r), _env, note="Take %d from both pans" % _b, hl=["right"]),
                   bal("x", "%d × %d" % (_r, _r), _env, note="x = %d" % (_r * _r), hl=["right"])], origin="rule")


# ── Drawn one by one: equations with the letter on both sides ────────────────

def balances(qid, env, before, steps, **kw):
    """before and each step: (left, right[, note[, highlight]]) or a list of such alternatives."""
    def one(spec):
        if spec is None:
            return None
        if isinstance(spec, list):
            return [one(s) for s in spec]
        if isinstance(spec, dict):
            return spec
        left, right = spec[0], spec[1]
        return bal(left, right, env, note=spec[2] if len(spec) > 2 else None, hl=spec[3] if len(spec) > 3 else None)
    P.put(qid, one(before), dict((i, one(s)) for i, s in steps.items()), **kw)


FIND = "Both pans weigh the same. Find %s."

balances("EXT_G4_FP_2020_005", {"x": 3}, ("3x − 7", "8 − 2x", FIND % "x"), {
    0: ("5x − 7", "8", "Add 2x to both pans"),
    1: [("5x", "8 + 7", "5x = 15"), ("5x", "8 + 7", "Add 7 to both pans")],
    2: [("x", "15 ÷ 5", "x = 3")],
    3: ("3 × 3 − 7", "8 − 2 × 3", "Check: both pans are 2"),
    4: ("x", "3", "x = 3", ["right"])})

balances("EXT_G4_FP_2022_002", {"a": 5}, ("6a + 8", "4a + 18", FIND % "a"), {
    0: ("2a + 8", "18", "Take 4a from both pans"),
    1: [("2a", "18 − 8", "2a = 10"), ("2a", "18 − 8", "Take 8 from both pans")],
    2: [("a", "10 ÷ 2", "a = 5"), ("a", "10 ÷ 2", "Share both pans into 2 equal parts")],
    3: ("6 × 5 + 8", "4 × 5 + 18", "Check: both pans are 38"),
    4: ("a", "5", "a = 5, which is not in the list", ["right"])})

balances("EXT_G4_FP_2023_021", {"P": 6}, ("7(3P − 4)", "4(5 + 3P) + 6", FIND % "P"), {
    0: ("21P − 28", "12P + 26", "Open the brackets"),
    1: [("9P", "26 + 28", "9P = 54"), ("9P", "26 + 28", "Take 12P from both pans, then add 28 to both")],
    2: ("P", "54 ÷ 9", "P = 6"),
    3: ("7 × 14", "4 × 23 + 6", "Check: both pans are 98"),
    4: ("P", "6", "P = 6", ["right"])})

balances("EXT_G4_FP_2024_012", {"y": 9}, ("16y − 36", "4y + (8 × 9)", FIND % "y"), {
    1: ("12y − 36", "72", "Take 4y from both pans"),
    2: [("12y", "72 + 36", "12y = 108"), ("12y", "72 + 36", "Add 36 to both pans")],
    3: [("y", "108 ÷ 12", "y = 9"), ("y", "(72 + 36) ÷ 12", "y = 9")],
    4: ("y", "9", "y = 9", ["right"])})

balances("EXT_G4_FP_2025_020", {"m": 21}, ("4m/3 + 17", "2m + 3", FIND % "m"), {
    0: ("4m + 51", "6m + 9", "Make every part 3 times as big"),
    1: ("51", "2m + 9", "Take 4m from both pans"),
    2: [("51 − 9", "2m", "2m = 42"), ("51 − 9", "2m", "Take 9 from both pans")],
    3: [("42 ÷ 2", "m", "m = 21"), ("(51 − 9) ÷ 2", "m", "m = 21")],
    4: ("4 × 21 ÷ 3 + 17", "2 × 21 + 3", "Check: both pans are 45"),
    5: ("m", "21", "m = 21", ["right"])})

balances("PYQ_2017_Q14", {"x": 4}, ("12x − 40", "2x", FIND % "x"), {
    0: ("12x", "2x + 40", "Add 40 to both pans"),
    1: ("10x", "40", "Take 2x from both pans"),
    2: ("x", "40 ÷ 10", "x = 4"),
    3: ("12 × 4 − 40", "2 × 4", "Check: both pans are 8")})

balances("PYQ_2018_Q27", {"x": 3}, ("97 − 17x", "5x + 31", FIND % "x"), {
    0: ("97", "22x + 31", "Add 17x to both pans"),
    1: ("97 − 31", "22x", "22x = 66"),
    2: ("66 ÷ 22", "x", "x = 3"),
    3: ("97 − 17 × 3", "5 × 3 + 31", "Check: both pans are 46")})

balances("PYQ_2019_Q13", {"x": 6}, ("15 − 3x", "x − 9", FIND % "x"), {
    0: ("15", "4x − 9", "Add 3x to both pans"),
    1: ("15 + 9", "4x", "4x = 24"),
    2: ("24 ÷ 4", "x", "x = 6"),
    3: ("6", "x", "x = 6", ["left"])})

balances("PYQ_2019_Q29", {"T": 8}, ("31 − T", "2T + 7", FIND % "T"), {
    0: ("31", "3T + 7", "Add T to both pans"),
    1: ("31 − 7", "3T", "3T = 24"),
    2: ("24 ÷ 3", "T", "T = 8"),
    3: ("31 − 8", "2 × 8 + 7", "Check: both pans are 23")})

balances("Q_CH14_008", {"h": 6}, ("7 + h + 2", "15", FIND % "h"), {
    0: ("9 + h", "15", "7 + 2 = 9"),
    1: ("h", "15 − 9", "h = 6"),
    2: ("7 + 6 + 2", "15", "Check: both pans are 15")})

balances("Q_CH14_013", {"z": 4}, ("z", "12 − 2z", FIND % "z"), {
    0: ("3z", "12", "Add 2z to both pans"),
    1: ("z", "12 ÷ 3", "z = 4"),
    2: ("4", "12 − 2 × 4", "Check: both pans are 4")})

balances("Q_CH14_014", {"a": 8}, ("6a − 32", "2a", FIND % "a"), {
    0: ("6a", "2a + 32", "Add 32 to both pans"),
    1: ("4a", "32", "Take 2a from both pans"),
    2: ("a", "32 ÷ 4", "a = 8"),
    3: ("6 × 8 − 32", "2 × 8", "Check: both pans are 16")})

balances("Q_CH14_015", {"b": 7}, ("4b + 5", "2b + 19", FIND % "b"), {
    0: ("2b + 5", "19", "Take 2b from both pans"),
    1: ("2b", "19 − 5", "2b = 14"),
    2: ("b", "14 ÷ 2", "b = 7"),
    3: ("4 × 7 + 5", "2 × 7 + 19", "Check: both pans are 33")})

balances("Q_CH14_016", {"c": 9}, ("7 + 5c", "3c + 25", FIND % "c"), {
    0: ("7 + 2c", "25", "Take 3c from both pans"),
    1: ("2c", "25 − 7", "2c = 18"),
    2: ("c", "18 ÷ 2", "c = 9"),
    3: ("7 + 5 × 9", "3 × 9 + 25", "Check: both pans are 52")})

balances("PYQ_2018_Q25", {"★": 18}, ("19/★ + 17/★", "2", "Both ★ are the same number"), {
    0: ("36/★", "2", "19 + 17 = 36 on top"),
    1: ("★", "36 ÷ 2", "★ = 18"),
    2: ("19/18 + 17/18", "2", "Check: 36/18 = 2"),
    3: ("★", "18", "★ = 18", ["right"])})

balances("PYQ_2016_Q07", {"p": 7}, ("21", "3 × p", "m = 21 and n = 3, so 21 = 3 × p"), {
    0: ("21 ÷ 3", "p", "p = 7"),
    1: ("21 ÷ 7", "3", "m ÷ p = 21 ÷ 7 = 3")})

# Find the letter, then use it.
balances("EXT_G4_FP_2022_023", {"P": 4}, ("8P + 7", "39", "Find P first. Then Q = P + 3."), {
    0: [("8P", "39 − 7", "8P = 32"), ("8P", "39 − 7", "Take 7 from both pans")],
    1: [("P", "32 ÷ 8", "P = 4"), ("P", "(39 − 7) ÷ 8", "Share both pans into 8 equal parts")],
    3: bm(B("P", V(4)), B("Q", V(4), V(3, tone="c"), brace="7"), note="2P + 3Q = 2 × 4 + 3 × 7")})

balances("EXT_G4_FP_2023_011", {"x": Fraction(31, 3)}, ("3x + 7", "38", "Use this to find 6x + 7"), {
    0: [("3x", "38 − 7", "3x = 31"), ("3x", "38 − 7", "Take 7 from both pans")],
    1: [("6x", "31 × 2", "6x = 62"), ("6x", "2 × (38 − 7)", "6x is double 3x")],
    2: [("6x + 7", "62 + 7", "6x + 7 = 69"), ("6x + 7", "2 × (38 − 7) + 7", "Add 7 to both pans")],
    3: ("6x + 7", "69", "69 is not in the list", ["right"])})

linear("EXT_G4_FP_2024_037", eq="12x − 19 = 53", origin="authored", key=False,
       extra={2: bal("5 × 6 + 29", "59", {}, note="Put 6 in place of x in 5x + 29"), 3: None})
linear("EXT_G4_FP_2025_035", eq="3m + 7 = 28", origin="authored", key=False,
       extra={2: bal("2 × 7 + 25", "39", {}, note="Put 7 in place of m in 2m + 25"), 3: None})

# Which equation is true? Only the pair that balances is drawn (after answering).
balances("EXT_G4_FP_2023_020", {"N": 8}, None, {
    2: ("44 − 4 × 8", "3 × 8 − 12", "Both sides are 12, so they balance"),
    4: ("44 − 4N", "3N − 12", "True when N = 8")})
balances("Q_CH14_017", {"x": 5}, None, {
    3: ("2 × 5 − 3", "7", "Both sides are 7, so they balance"),
    4: ("2x − 3", "7", "True when x = 5")})


# ── Drawn one by one: stories ────────────────────────────────────────────────

put = P.put

# Three times a number plus 7 equals 28.
put("EXT_G4_WS2_CH14_007",
    bm(B("", [Uq(7)] * 3, V(7, tone="b"), brace="28"), note="3 equal pieces and 7 more make 28"),
    {0: [bm(B("", [Uq(7)] * 3, brace="21"), note="28 − 7 = 21"),
         bm(B("", [Uq(7)] * 3, brace="28 − 7"), note="Take the 7 away: 3 equal pieces are left")],
     1: bm(B("", [V(7)] * 3, brace="28 − 7"), note="Each equal piece is 7", hl=["b0"]),
     2: bm(B("", [V(7)] * 3, V(7, tone="b"), brace="28"), note="Check: 3 × 7 + 7 = 28")})

put("EXT_G4_WS2_CH14_008",
    bm(B("Smaller", Uq(12)), B("Bigger", Uq(12), V(1, tone="c")), note="Two numbers in a row. Together they make 25."),
    {0: [bm(B("Smaller", Uq(12)), B("Bigger", Uq(12), V(1, tone="c")), hl=["b1s1"], note="25 − 1 = 24: two equal pieces are left"),
         bm(B("Smaller", Uq(12)), B("Bigger", Uq(12), V(1, tone="c")), hl=["b1s1"], note="Take the extra 1 away: two equal pieces are left")],
     1: bm(B("Smaller", V(12)), B("Bigger", V(12), V(1, tone="c")), note="Each equal piece is 12"),
     2: bm(B("Smaller", V(12)), B("Bigger", V(12), V(1, tone="c"), brace="13"), note="12 + 13 = 25")})

_H = ["Number", "Add 6", "Times 4"]
put("G4A_EQUATIONS_001", tb([["?", "?", "60"]], _H, note="Anil's number goes through two steps"),
    {0: tb([["?", "15", "60"]], _H, note="Undo the last step: 60 ÷ 4 = 15", hl=["r0"]),
     1: tb([["9", "15", "60"]], _H, note="Undo the first step: 15 − 6 = 9", hl=["r0"])})

put("G4A_EQUATIONS_002",
    bm(B("Kabir", Uq(32)), B("Diya", Uq(32), Uq(32)), note="Together they save ₹96"),
    {0: bm(B("Kabir", Uq(32)), B("Diya", Uq(32), Uq(32)), note="Kabir has 1 share and Diya has 2 shares"),
     1: bm(B("Kabir", V(32, "₹")), B("Diya", V(32, "₹"), V(32, "₹")), note="96 ÷ 3 = 32 for each share"),
     2: bm(B("Kabir", V(32, "₹")), B("Diya", V(32, "₹"), V(32, "₹")), note="Kabir saves ₹32", hl=["b0"])})

put("G4A_EQUATIONS_003",
    bm(B("", [V(7)] * 8, V(5, tone="b"), brace="?"), note="8 children get 7 toffees each. 5 toffees are left over."),
    {0: bm(B("", [V(7)] * 8, V(5, tone="b")), hl=["b0s%d" % i for i in range(8)], note="8 × 7 = 56 toffees given out"),
     1: bm(B("", V(56), V(5, tone="b"), brace="61"), note="56 + 5 = 61")})

_R = dict(length="15 cm", inside="Perimeter 46 cm", proportion=15.0 / 8)
put("G4A_EQUATIONS_004", rect(breadth="?", **_R),
    {0: [rect(breadth="?", hl=["length", "breadth"], note="One length and one breadth: 46 ÷ 2 = 23", **_R)],
     1: rect(breadth="8 cm", hl=["breadth"], note="23 − 15 = 8", **_R)})

_E = {"boxes": 4, "box": 4, "kg": 1}
put("G4A_EQUATIONS_005", bal("3 boxes + 2 kg", "14 kg", _E),
    {0: bal("3 boxes + 2 kg", "14 kg", _E, note="Both pans weigh the same"),
     1: bal("3 boxes", "12 kg", _E, note="Take 2 kg off each pan: 14 − 2 = 12"),
     2: bal("1 box", "4 kg", _E, note="12 ÷ 3 = 4")})

put("G4A_EQUATIONS_006",
    bm(B("Tara", Uq(12)), B("Mother", [Uq(12)] * 3), note="Mother is 3 times as old as Tara, and 24 years older"),
    {0: bm(B("Tara", Uq(12)), B("Mother", [Uq(12)] * 3), hl=["b1s1", "b1s2"], note="The 2 extra shares are the 24 years"),
     1: bm(B("Tara", V(12)), B("Mother", [V(12)] * 3), note="24 ÷ 2 = 12 for each share"),
     2: bm(B("Tara", V(12)), B("Mother", [V(12)] * 3), hl=["b0"], note="Tara is 12 years old")})

put("G4A_EQUATIONS_007",
    bm(B("", [Uq(13)] * 5, V(35, "₹", tone="b"), brace="₹100"), note="5 pens and the ₹35 change make up the ₹100 note"),
    {0: [bm(B("", [Uq(13)] * 5, V(35, "₹", tone="b"), brace="₹100"), hl=["b0s%d" % i for i in range(5)], note="100 − 35 = 65 for the 5 pens"),
         bm(B("", [Uq(13)] * 5, V(35, "₹", tone="b"), brace="₹100"), hl=["b0s5"], note="Take the ₹35 change away from ₹100")],
     1: [bm(B("", [V(13, "₹")] * 5, V(35, "₹", tone="b"), brace="₹100"), note="65 ÷ 5 = 13"),
         bm(B("", [V(13, "₹")] * 5, V(35, "₹", tone="b"), brace="₹100"), note="Each pen costs ₹13")]})

put("G4A_EQUATIONS_008",
    bm(B("", V(30, "₹"), Uq(60, "? km at ₹12"), brace="₹90"), note="₹30 for the first km, then ₹12 for each km after it"),
    {0: [bm(B("", V(30, "₹"), Uq(60, "? km at ₹12"), brace="₹90"), hl=["b0s1"], note="90 − 30 = 60 for the other kilometres"),
         bm(B("", V(30, "₹"), Uq(60, "? km at ₹12"), brace="₹90"), hl=["b0s1"], note="Take the first ₹30 away from ₹90")],
     1: bm(B("", V(30, "₹"), [V(12, "₹", tone="b")] * 5, brace="₹90"), hl=["b0s%d" % i for i in range(1, 6)], note="5 pieces of ₹12: 5 km after the first"),
     2: bm(B("", V(30, "₹"), [V(12, "₹", tone="b")] * 5, brace="₹90"), note="1 + 5 = 6 km", hl=["b0"])})

put("G4A_EQUATIONS_009",
    bm(B("", S("★", 9), S("★", 9), brace="18"), B("", S("★", 9, "a"), S("▲", 5, "b"), brace="14"), note="The same shape is always the same number"),
    {0: bm(B("", V(9), V(9), brace="18"), B("", S("★", 9, "a"), S("▲", 5, "b"), brace="14"), hl=["b0"], note="18 ÷ 2 = 9, so ★ is 9"),
     1: bm(B("", V(9), V(9), brace="18"), B("", V(9, tone="a"), V(5, tone="b"), brace="14"), hl=["b1s1"], note="14 − 9 = 5, so ▲ is 5")})

put("G4A_EQUATIONS_010",
    bm(B("", Uq(12, "half of ?"), V(8, tone="b"), brace="20"), note="Half of the number and 8 more make 20"),
    {0: bm(B("", V(12), V(8, tone="b"), brace="20"), hl=["b0s0"], note="20 − 8 = 12 is half of the number"),
     1: bm(B("The number", V(12), V(12), brace="24"), note="12 × 2 = 24")})

put("G4A_EQUATIONS_011",
    bm(B("", S("6 cows' legs", 24), S("hens' legs", 20, "b"), brace="44 legs"), note="How many hens are there?"),
    {0: [bm(B("", S("6 cows' legs", 24), S("hens' legs", 20, "b"), brace="44 legs"), hl=["b0s0"], note="6 × 4 = 24 legs for the cows"),
         bm(B("", S("6 cows' legs", 24), S("hens' legs", 20, "b"), brace="44 legs"), hl=["b0s0"], note="Each cow has four legs: count the cows' legs first")],
     1: bm(B("", S("6 cows' legs", 24), V(20, post=" legs", tone="b"), brace="44 legs"), hl=["b0s1"], note="The hens have 20 legs"),
     2: bm(B("", S("6 cows' legs", 24), [V(2, tone="b")] * 10, brace="44 legs"), note="20 ÷ 2 = 10 hens")})

put("G4A_EQUATIONS_012",
    bm(B("Gopal", S("x", 12)), B("Sister", S("3 less than x", 9)), note="Their ages add up to 21 years"),
    {1: bm(B("Gopal", S("x", 12)), B("Sister", S("x − 3", 9)), hl=["b1"], note="3 years younger than Gopal: x − 3"),
     2: bm(B("Gopal", S("x", 12)), B("Sister", S("x − 3", 9)), note="x + x − 3 = 21")})

put("G4A_EQUATIONS_013",
    bm(B("Six times", [Uq(7)] * 6), B("Number + 35", Uq(7), V(35, tone="b")), note="Six times a number is the same as the number and 35 more"),
    {0: bm(B("Six times", [Uq(7)] * 6), B("Number + 35", Uq(7), V(35, tone="b")), hl=["b0s1", "b0s2", "b0s3", "b0s4", "b0s5", "b1s1"],
           note="Take one piece from each bar: 5 pieces match the 35"),
     1: bm(B("Six times", [V(7)] * 6), B("Number + 35", V(7), V(35, tone="b")), note="35 ÷ 5 = 7")})

_E = {"tins": 5, "tin": 5, "kg": 1}
put("G4A_EQUATIONS_014", bal("5 tins + 3 kg", "2 tins + 18 kg", _E),
    {0: bal("3 tins + 3 kg", "18 kg", _E, note="Take 2 tins off each pan"),
     1: bal("3 tins", "15 kg", _E, note="Take 3 kg off each pan: 18 − 3 = 15"),
     2: bal("1 tin", "5 kg", _E, note="15 ÷ 3 = 5")})

put("G4A_EQUATIONS_015",
    bm(B("Asha", V(52)), B("Bina", V(28)), note="Asha gives stickers to Bina until both have the same number"),
    {0: bm(B("Asha", V(52)), B("Bina", V(28)), note="52 + 28 = 80 stickers in all"),
     1: bm(B("Asha", V(40)), B("Bina", V(40)), note="80 ÷ 2 = 40 each"),
     2: bm(B("Asha", V(40), V(12, tone="c"), brace="52"), B("Bina", V(28), V(12, tone="c"), brace="40"), hl=["b0s1", "b1s1"],
           note="52 − 40 = 12 stickers move across")})

_H = ["What", "Autos", "Cars", "In all"]
_W = ["Wheels each", "3", "4", "–"]
put("G4A_EQUATIONS_016", tb([_W, ["Vehicles", "?", "?", "10"], ["Wheels", "?", "?", "34"]], _H),
    {0: tb([_W, ["Vehicles", "10", "0", "10"], ["Wheels", "10 × 3", "0", "?"]], _H, hl=["r1"], note="Suppose all 10 are auto-rickshaws"),
     1: tb([_W, ["Vehicles", "10", "0", "10"], ["Wheels", "10 × 3", "0", "?"]], _H, hl=["r2"], note="34 − 10 × 3 = 4 extra wheels are really there"),
     2: tb([_W, ["Vehicles", "6", "4", "10"], ["Wheels", "6 × 3", "4 × 4", "34"]], _H, hl=["r1"], note="Each car adds 1 wheel: 4 cars and 6 autos")})

_B = lambda a, b, c, **kw: bm(B("Bala", a), B("Jaya", a, a), B("Chitra", a, V(5, tone="c")), **kw)
put("G4A_EQUATIONS_017", _B(Uq(10), 0, 0, note="Together they have 45 shells"),
    {0: _B(Uq(10), 0, 0, note="4 equal shares and 5 more"),
     1: [_B(Uq(10), 0, 0, hl=["b2s1"], note="45 − 5 = 40 for the 4 shares"),
         _B(Uq(10), 0, 0, hl=["b2s1"], note="Take the extra 5 away from 45")],
     2: [_B(V(10), 0, 0, note="40 ÷ 4 = 10"), _B(V(10), 0, 0, note="Each share is 10 shells")]})

_R = dict(inside="Perimeter 48 m", proportion=17.0 / 7)
put("G4A_EQUATIONS_018", rect(length="2 breadths + 3 m", breadth="?", **_R),
    {0: [rect(length="2 breadths + 3 m", breadth="?", hl=["length", "breadth"], note="One length and one breadth: 48 ÷ 2 = 24", **_R),
         rect(length="2 breadths + 3 m", breadth="?", hl=["length", "breadth"], note="One length and one breadth make half of 48 m", **_R)],
     1: [bm(B("", [Uq(7, "breadth")] * 3, V(3, post=" m", tone="b"), brace="24 m"), note="24 − 3 = 21 for the 3 breadths"),
         bm(B("", [Uq(7, "breadth")] * 3, V(3, post=" m", tone="b"), brace="24 m"), note="Take the 3 m away from 24 m")],
     2: bm(B("", [V(7, post=" m")] * 3, V(3, post=" m", tone="b"), brace="24 m"), note="Each breadth is 7 m"),
     3: rect(length="17 m", breadth="7 m", hl=["length"], note="2 × 7 + 3 = 17", **_R)})

_B = lambda nb, **kw: bm(B("Raju", [nb] * 3, V(14, "₹", tone="c")), B("Sonu", [nb] * 4, V(2, "₹", tone="c")), **kw)
put("G4A_EQUATIONS_019", _B(Uq(12), note="Both started with the same money. Each ? is one notebook."),
    {0: _B(Uq(12), note="3 notebooks and ₹14 equal 4 notebooks and ₹2"),
     1: _B(Uq(12), hl=["b1s3"], note="Sonu bought 1 more notebook than Raju"),
     2: _B(V(12, "₹"), hl=["b1s3"], note="14 − 2 = 12, so one notebook costs ₹12")})

put("G4A_EQUATIONS_020",
    bm(B("", S("book (half)", 75), V(30, "₹", tone="b"), V(45, "₹", tone="c"), brace="?"), note="Half goes on a book, ₹30 on a pen, and ₹45 is left"),
    {0: bm(B("", S("book (half)", 75), V(30, "₹", tone="b"), V(45, "₹", tone="c"), brace="?"), hl=["b0s1", "b0s2"], note="45 + 30 = 75 is the other half"),
     1: bm(B("", V(75, "₹"), V(30, "₹", tone="b"), V(45, "₹", tone="c"), brace="₹150"), note="75 × 2 = 150")})

_H = ["Step", "Asha", "Bina"]
_T1 = [["Start", "1", "1"], ["First", "1 + 8 = 9", "2"], ["Then", "18", "2 + 8 = 10"]]
_T2 = [["Start", "n", "n"], ["First", "n + 8", "2n"], ["Then", "2n + 16", "2n + 8"]]
put("G4A_EQUATIONS_021", tb([["Start", "same number", "same number"], ["First", "add 8", "double"], ["Then", "double", "add 8"]], _H),
    {0: tb(_T1, _H, note="Try the number 1"),
     1: tb(_T1, _H, hl=["r2"], note="18 − 10 = 8"),
     2: tb(_T2, _H, note="For any start n: Asha doubles the 8 as well"),
     3: tb(_T2, _H, hl=["r2"], note="16 − 8 = 8")})

_H = ["Number", "Swapped", "Difference"]
_T = [["18", "81", "63"], ["27", "72", "45"], ["36", "63", "27"], ["45", "54", "9"]]
put("G4A_EQUATIONS_022", None,
    {1: tb([r[:2] + ["?"] for r in _T], _H, note="The swapped number must be the greater one"),
     2: tb(_T, _H),
     3: tb(_T, _H, hl=["r2"], note="Only 36 gives a difference of 27")})

put("G4A_EQUATIONS_023",
    bm(B("Sonu", Uq(10)), B("Ravi", [Uq(10)] * 4), note="Then each wins 5 more. Now Ravi has 3 times as many as Sonu."),
    {0: bm(B("Sonu", V(10)), B("Ravi", [V(10)] * 4, brace="40"), note="Test Sonu = 10: Ravi has 4 × 10 = 40"),
     1: bm(B("Sonu", V(10), V(5, tone="c"), brace="15"), B("Ravi", [V(10)] * 4, V(5, tone="c"), brace="45"), hl=["b0s1", "b1s4"], note="Each wins 5 more"),
     2: bm(B("Sonu", V(15)), B("Ravi", [V(15)] * 3, brace="45"), note="45 is 3 times 15, so both clues fit")})

_A = lambda a, b, **kw: bm(B("Basket", *a), B("The rest", *b), **kw)
_a0 = (S("Asha: half", 9), V(1, tone="c"), S("the rest", 8, "b"))
_b0 = (S("Bala: half", 4, "a"), V(1, tone="c"), S("3 left", 3, "b"))
_b1 = (V(4, tone="a"), V(1, tone="c"), S("3 left", 3, "b"))
_a1 = (S("Asha: half", 9), V(1, tone="c"), V(8, tone="b"))
put("G4A_EQUATIONS_024",
    bm(B("Basket", *_a0, brace="?"), B("The rest", *_b0), note="Each takes half and 1 more. Then 3 are left."),
    {0: bm(B("Basket", *_a0, brace="?"), B("The rest", *_b0), hl=["b1s1", "b1s2"], note="The 3 left and his extra 1 are half of what Bala found"),
     1: bm(B("Basket", *_a0, brace="?"), B("The rest", *_b1, brace="8"), hl=["b1"], note="4 × 2 = 8 mangoes before Bala"),
     2: bm(B("Basket", *_a1, brace="?"), B("The rest", *_b1, brace="8"), hl=["b0s1", "b0s2"], note="8 + 1 = 9 is half of the basket"),
     3: bm(B("Basket", V(9), V(1, tone="c"), V(8, tone="b"), brace="18"), B("The rest", *_b1, brace="8"), hl=["b0"], note="9 × 2 = 18")})

_H = ["What", "Won", "Lost", "In all"]
_W = ["Points each", "+5", "−2", "–"]
put("G4A_EQUATIONS_025", tb([_W, ["Rounds", "?", "?", "20"], ["Points", "?", "?", "65"]], _H),
    {0: tb([_W, ["Rounds", "20", "0", "20"], ["Points", "100", "0", "100"]], _H, note="Suppose she won all 20 rounds: 20 × 5 = 100"),
     2: tb([_W, ["Rounds", "?", "5", "20"], ["Points", "?", "?", "65"]], _H, hl=["r1"], note="100 − 65 = 35, and 35 ÷ 7 = 5 lost rounds"),
     3: tb([_W, ["Rounds", "15", "5", "20"], ["Points", "75", "−10", "65"]], _H, hl=["r2"], note="Check: 75 − 10 = 65"),
     4: tb([_W, ["Rounds", "15", "5", "20"], ["Points", "75", "−10", "65"]], _H, hl=["r1"], note="20 − 5 = 15 rounds won")})

_B = lambda pen, pencil, **kw: bm(B("", [pen] * 2, [pencil] * 3, brace="₹36"), B("", [pen] * 2, [pencil] * 5, brace="₹48"), **kw)
_pen, _pencil = S("pen", 9, "a"), S("pencil", 6, "b")
put("G4A_EQUATIONS_026", _B(_pen, _pencil, note="Same shop, same prices"),
    {0: _B(_pen, _pencil, hl=["b1s5", "b1s6"], note="2 extra pencils cost 48 − 36 = 12 rupees"),
     1: _B(_pen, V(6, "₹", tone="b"), note="12 ÷ 2 = 6 rupees for one pencil"),
     2: _B(_pen, V(6, "₹", tone="b"), hl=["b0s0", "b0s1"], note="36 − 18 = 18 rupees for the 2 pens"),
     3: _B(V(9, "₹", tone="a"), V(6, "₹", tone="b"), hl=["b0s0", "b0s1"], note="18 ÷ 2 = 9 rupees for one pen")})

_pts = [(23, "23"), (27, "27"), (31, "31"), (35, "35"), (39, "39")]
put("G4A_EQUATIONS_027", None,
    {0: nl(20, 40, 1, points=_pts, ticks="ends", note="Between 20 and 40, and 3 more than a multiple of 4"),
     2: nl(20, 40, 1, points=_pts, ticks="ends", hl=["p1"], note="Only 27 ends in 2 or 7")})

_E = {"melon": 7, "melons": 7, "mangoes": 3, "mango": 3, "guava": 1, "guavas": 1}
put("G4A_EQUATIONS_028", bal("1 melon", "2 mangoes + 1 guava", _E, note="Also: 1 mango weighs the same as 3 guavas"),
    {0: bal("2 mangoes", "6 guavas", _E, note="2 × 3 = 6"),
     1: bal("1 melon", "7 guavas", _E, note="6 + 1 = 7"),
     2: bal("2 melons", "14 guavas", _E, note="2 × 7 = 14")})

_ends = [(36, "36"), (86, "86")]
put("G4A_EQUATIONS_029", nl(36, 86, 5, points=_ends, ticks="none", note="The number is as far above 36 as it is below 86"),
    {0: nl(36, 86, 5, points=_ends, ticks="none", note="It is exactly halfway between 36 and 86"),
     1: nl(36, 86, 5, points=_ends, hops=[(36, 86, "50")], ticks="none", note="86 − 36 = 50"),
     2: nl(36, 86, 5, points=_ends, hops=[(36, 61, "25"), (61, 86, "25")], ticks="none", note="50 ÷ 2 = 25"),
     3: nl(36, 86, 5, points=[(36, "36"), (61, "61"), (86, "86")], hops=[(36, 61, "25"), (61, 86, "25")], ticks="none", hl=["p1"], note="36 + 25 = 61")})

_H = ["Multiply to 35", "Add up to"]
put("G4A_EQUATIONS_030", None,
    {0: tb([["1 and 35", "?"], ["5 and 7", "?"]], _H),
     1: tb([["1 and 35", "36"], ["5 and 7", "12"]], _H, hl=["r1"], note="5 + 7 = 12, so the numbers are 5 and 7"),
     2: tb([["1 and 35", "36"], ["5 and 7", "12"]], _H, hl=["r1"], note="7 − 5 = 2")})

_H = ["Packs of 7", "Pencils left", "Packs of 4"]
_no = "not exact"
put("G4A_EQUATIONS_031", None,
    {0: tb([["0", "30", _no]], _H, note="30 is not a multiple of 4"),
     1: tb([["0", "30", _no], ["1", "23", _no], ["2", "?", "?"], ["3", "9", _no], ["4", "2", _no]], _H),
     2: tb([["0", "30", _no], ["1", "23", _no], ["2", "16", "4"], ["3", "9", _no], ["4", "2", _no]], _H, hl=["r2"], note="16 is exactly 4 packs of 4"),
     3: tb([["0", "30", _no], ["1", "23", _no], ["2", "16", "4"], ["3", "9", _no], ["4", "2", _no]], _H, hl=["r2"], note="2 + 4 = 6 packs")})

put("G4A_EQUATIONS_033",
    bm(B("Pari", V(6)), B("Sunita", V(30)), note="In how many years will Sunita be 3 times as old as Pari?"),
    {0: bm(B("Pari", V(6)), B("Sunita", V(6), V(24, tone="c"), brace="30"), hl=["b1s1"], note="The gap of 24 years stays the same every year"),
     1: bm(B("Pari then", Uq(12)), B("Sunita then", Uq(12), [S("?", 12, "c")] * 2), hl=["b1s1", "b1s2"], note="3 times as old: the gap is 2 times Pari's age"),
     2: bm(B("Pari then", V(12)), B("Sunita then", [V(12)] * 3, brace="36"), note="24 ÷ 2 = 12"),
     3: bm(B("Pari", V(6), V(6, tone="c"), brace="12"), B("Sunita", V(30), V(6, tone="c"), brace="36"), hl=["b0s1", "b1s1"], note="12 − 6 = 6 years from now")})

put("G4A_EQUATIONS_034",
    nl(0, 10, 1, hops=[(0, 3, "day"), (3, 1, "night")], note="The well is 10 m deep. Up 3 m by day, back 2 m by night."),
    {0: nl(0, 10, 1, hops=[(0, 3, "day"), (3, 1, "night")], hl=["h0", "h1"], note="Each day and night together: 3 − 2 = 1 m up"),
     1: nl(0, 10, 1, points=[(7, "start here")], hops=[(7, 10, "last day")], note="10 − 3 = 7: from 7 m one climb reaches the top"),
     2: nl(0, 10, 1, points=[(7, "after 7 days")], note="Gaining 1 m a day, it is at 7 m after 7 days and nights"),
     3: nl(0, 10, 1, points=[(7, "7 m"), (10, "top")], hops=[(7, 10, "day 8")], hl=["h0"], note="7 + 3 = 10")})

_bought = lambda p: B("Bought", [p] * 3, S(p["label"] if p["label"] != "oranges" else "bananas", 6, "b"), brace="24 fruits")
put("PYQ_2016_Q16",
    bm(_bought(S("oranges", 6)), B("Dropped", [S("oranges", 3, "a")] * 2, S("bananas", 3, "b"), brace="24 − 15"), note="She took home 15 of the 24 fruits"),
    {0: bm(_bought(V(6)), B("Dropped", [S("oranges", 3, "a")] * 2, S("bananas", 3, "b"), brace="24 − 15"), hl=["b0"], note="24 ÷ 4 = 6 a piece: 18 oranges and 6 bananas"),
     1: bm(_bought(V(6)), B("Dropped", [S("oranges", 3, "a")] * 2, S("bananas", 3, "b"), brace="9"), hl=["b1"], note="24 − 15 = 9 fruits dropped"),
     2: bm(_bought(V(6)), B("Dropped", [V(3, tone="a")] * 2, V(3, tone="b"), brace="9"), hl=["b1"], note="9 ÷ 3 = 3 a piece: 6 oranges and 3 bananas"),
     3: bm(_bought(V(6)), B("Dropped", [V(3, tone="a")] * 2, V(3, tone="b"), brace="9"), hl=["b1s0", "b1s1"], note="18 − 6 = 12 oranges reach home")})

_f5, _f10 = S("5 p", 5, "a"), S("10 p stamps", 50, "b")
put("PYQ_2017_Q11",
    bm(B("First", _f5, _f10, brace="55 paise"), B("Second", _f5, _f10, _f10, brace="Rs. 1 and 5 paise"), note="Same 5 paise stamps, twice as many 10 paise stamps"),
    {0: bm(B("First", _f5, _f10, brace="55 paise"), B("Second", _f5, _f10, _f10, brace="105 paise"), hl=["b1s2"], note="105 − 55 = 50 paise for the extra stamps"),
     1: bm(B("First", _f5, V(50, post=" p", tone="b"), brace="55 paise"), B("Second", _f5, [V(50, post=" p", tone="b")] * 2, brace="105 paise"), hl=["b0s1"], note="50 ÷ 10 = 5 stamps of 10 paise"),
     2: bm(B("First", V(5, post=" p", tone="a"), V(50, post=" p", tone="b"), brace="55 paise"), B("Second", _f5, [V(50, post=" p", tone="b")] * 2, brace="105 paise"), hl=["b0s0"], note="55 − 50 = 5 paise spent on 5 paise stamps"),
     3: bm(B("First", V(5, post=" p", tone="a"), V(50, post=" p", tone="b"), brace="55 paise"), B("Second", _f5, [V(50, post=" p", tone="b")] * 2, brace="105 paise"), hl=["b0s0"], note="5 ÷ 5 = 1 stamp of 5 paise")})

put("PYQ_2018_Q10",
    bm(B("Men", Uq(42)), B("Women", Uq(42), V(21, tone="c")), note="Together 105 people. There are 21 more women than men."),
    {0: bm(B("Men", Uq(42)), B("Women", Uq(42), V(21, tone="c")), hl=["b1s1"], note="105 − 21 = 84: two equal pieces are left"),
     1: bm(B("Men", V(42)), B("Women", V(42), V(21, tone="c")), note="84 ÷ 2 = 42 men"),
     2: bm(B("Men", V(42)), B("Women", V(42), V(21, tone="c"), brace="63"), hl=["b1"], note="42 + 21 = 63 women")})

_two = V(2, tone="c")
_boxes = lambda b: [b, b, _two, b, _two, _two, b, _two, _two, _two]
put("PYQ_2018_Q31",
    bm(B("", _boxes(Uq(22)), brace="100 marbles"), note="Four boxes in a row. Each has 2 more than the one before."),
    {0: bm(B("", _boxes(Uq(22)), brace="100 marbles"), hl=["b0s2", "b0s4", "b0s5", "b0s7", "b0s8", "b0s9"], note="2 + 4 + 6 = 12 extra marbles"),
     1: bm(B("", _boxes(V(22)), brace="100 marbles"), note="(100 − 12) ÷ 4 = 22 in the first box"),
     2: bm(B("", V(22), V(24), V(26), V(28), brace="100 marbles"), note="22 + 24 + 26 + 28 = 100"),
     3: bm(B("", V(22), V(24), V(26), V(28, tone="c")), hl=["b0s0", "b0s1", "b0s2"], note="22 + 24 + 26 = 72")})

put("Q_CH14_018",
    bm(B("", Uq(15), V(8, tone="b"), brace="23"), note="A number and 8 together make 23"),
    {1: bm(B("", V(15), V(8, tone="b"), brace="23"), hl=["b0s0"], note="23 − 8 = 15"),
     2: bm(B("", V(15), V(8, tone="b"), brace="23"), note="Check: 15 + 8 = 23")})

put("Q_CH14_019",
    bm(B("", [Uq(9)] * 7, brace="63"), note="Seven equal pieces make 63"),
    {0: bm(B("", [Uq(9)] * 7, brace="63"), hl=["b0"], note="7 × the number = 63"),
     1: bm(B("", [V(9)] * 7, brace="63"), note="Dividing undoes multiplying: 63 ÷ 7 = 9"),
     2: bm(B("", [V(9)] * 7, brace="63"), hl=["b0"], note="Check: 7 × 9 = 63, so the number is 9")})

put("Q_CH14_020",
    bm(B("Three times", [Uq(7)] * 3), B("", V(16, tone="b"), V(5, tone="c")), note="Three times a number, decreased by 5, is 16"),
    {0: bm(B("Three times", [Uq(7)] * 3), B("", V(16, tone="b"), V(5, tone="c"), brace="21"), hl=["b1"], note="16 + 5 = 21 is three times the number"),
     1: bm(B("Three times", [V(7)] * 3), B("", V(16, tone="b"), V(5, tone="c"), brace="21"), note="21 ÷ 3 = 7"),
     2: bm(B("Three times", [V(7)] * 3), B("", V(16, tone="b"), V(5, tone="c"), brace="21"), note="Check: 3 × 7 − 5 = 16")})

put("Q_CH14_021",
    bm(B("Brother", Uq(7)), B("Riya", Uq(7), Uq(7), V(3, tone="c"), brace="17 years"), note="Riya's age is twice her brother's age and 3 more"),
    {0: bm(B("Brother", Uq(7)), B("Riya", Uq(7), Uq(7), V(3, tone="c"), brace="17 years"), hl=["b1s2"], note="17 − 3 = 14 is twice his age"),
     1: bm(B("Brother", V(7)), B("Riya", V(7), V(7), V(3, tone="c"), brace="17 years"), note="14 ÷ 2 = 7")})

put("Q_CH14_023",
    bm(B("", V(45, "₹", " spent"), V(78, "₹", " left", tone="b"), brace="?"), note="What he spent and what he has left"),
    {1: bm(B("", V(45, "₹", " spent"), V(78, "₹", " left", tone="b"), brace="₹123"), note="78 + 45 = 123")})

_one = V(1, tone="c")
put("Q_CH14_025",
    bm(B("Smallest", Uq(11)), B("Middle", Uq(11), _one), B("Largest", Uq(11), _one, _one), note="Three numbers in a row. Together they make 36."),
    {0: bm(B("Smallest", Uq(11), _one), B("Middle", Uq(11), _one), B("Largest", Uq(11), _one), hl=["b0s1"], note="Move 1 from the largest to the smallest: three equal bars"),
     1: bm(B("Smallest", Uq(11), _one, brace="12"), B("Middle", Uq(11), _one, brace="12"), B("Largest", Uq(11), _one, brace="12"), note="36 ÷ 3 = 12 is the middle number"),
     2: bm(B("Smallest", V(11)), B("Middle", V(12)), B("Largest", V(13)), note="11 + 12 + 13 = 36")})

put("EXT_G4_FP_2021_028",
    bm(B("Bigger", Uq(4), V(8, tone="c")), B("Smaller", Uq(4)), note="The two numbers add up to 16. Their difference is 8."),
    {0: bm(B("Bigger", Uq(4), V(8, tone="c")), B("Smaller + 8", Uq(4), V(8, tone="c")), hl=["b1s1"], note="16 + 8 is twice the bigger number"),
     1: bm(B("Bigger", Uq(4), V(8, tone="c")), B("Smaller + 8", Uq(4), V(8, tone="c")), hl=["b0"], note="Half of 16 + 8 is the bigger number")})

put("EXT_G4_FP_2023_006",
    bm(B("Mishti", V(97)), B("Manav", V(11)), note="Mishti gives some pens. Then she has twice as many as Manav."),
    {0: bm(B("Mishti", V(97)), B("Manav", V(11)), note="The 97 + 11 pens in all do not change"),
     1: bm(B("Mishti", Uq(36), Uq(36)), B("Manav", Uq(36)), note="After giving: 3 equal shares of the 97 + 11 pens"),
     2: bm(B("Mishti", V(36), V(36)), B("Manav", V(11), V(25, tone="c"), brace="36"), hl=["b1s1"], note="36 − 11 = 25 pens given"),
     3: bm(B("Mishti", V(36), V(36), brace="72"), B("Manav", V(36)), note="97 − 25 = 72, which is twice 36")})

_T = [["m + n", "18"], ["n + p", "24"], ["m + p", "36"]]
put("EXT_G4_FP_2023_028", tb(_T, ["Sum", "Value"], note="Find p"),
    {0: tb(_T, ["Sum", "Value"], hl=["r0", "r1", "r2"], note="Add all three: each letter is counted twice"),
     2: tb(_T, ["Sum", "Value"], hl=["r0"], note="Take m + n = 18 away from m + n + p to leave p")})

put("EXT_G4_FP_2024_028",
    bm(B("Smaller", Uq(7)), B("Bigger", Uq(7), V(2, tone="c")), note="Two odd numbers next to each other add up to 16"),
    {0: nl(5, 11, 1, points=[(7, "7"), (8, "half of 16"), (9, "9")], note="The odd numbers on each side of 8 are 7 and 9"),
     1: [grid(7, 7, note="7 × 7 = 49"), grid(7, 7, note="The square of 7: 7 rows of 7")],
     2: [grid(9, 9, note="9 × 9 = 81"), grid(9, 9, note="The square of 9: 9 rows of 9")]})

P.save()
P.review()
