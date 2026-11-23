"""Figures for Grade 4 gr4_algebra. Writes data/question-figures/parts/g4-gr4_algebra.json.

    python -X utf8 scripts/figures/authoring/g4_gr4_algebra.py

Most of this topic is reading and working with expressions, where a picture before answering
would give away what the notation means (that 3a is three lots of a, that ab is a rows of b).
So the "put the number in place of the letter" families get STEP figures only, shown after the
child has answered: a bar of equal pieces for 3a, a grid for ab and a². Story and shape
questions get a figure of their givens as well. Pure simplifying is left without a picture.
"""
import re

from g4_gr4_equations_lib import Part, S, V, Uq, B, bm, nl, tb, rect, tri, poly, grid, n, steps_of, step_text, key_numbers

P = Part("gr4_algebra")
put = P.put

# ── Rule: put numbers in place of letters ────────────────────────────────────

HEAD = re.compile(r"^If (.+?)(?::\s*|,? find the value of |, what is the value of )(.+?)\s*(?:=\?|[.?])$")
VALS = re.compile(r"([a-z])\s*=\s*(\d+)")


def pieces(count, label, value, tone):
    return [S(label, value, tone) for _ in range(count)]


def two_terms(qid, q, vals, m, minus):
    """ma + nb or ma − nb, with the question's own step wording deciding what each step shows."""
    c = [int(m.group(1) or 1), int(m.group(3) or 1)]
    let = [m.group(2), m.group(4)]
    if let[0] == let[1] or let[0] not in vals or let[1] not in vals:
        return
    name = [m.group(1) + let[0], m.group(3) + let[1]]
    v = [vals[let[0]], vals[let[1]]]
    prod = [c[0] * v[0], c[1] * v[1]]
    total = prod[0] - prod[1] if minus else prod[0] + prod[1]
    expr = "%s %s %s" % (name[0], "−" if minus else "+", name[1])
    if total <= 0 or float(total) not in key_numbers(q) or max(c) > 12 or (not minus and sum(c) > 12):
        return P.note(qid, "substitution rule does not fit")
    shown = [False, False]
    tone = ["a", "b"]

    def term(i):
        return pieces(c[i], n(v[i]) if shown[i] else let[i], v[i], tone[i])

    def keys(bar, start, count):
        return ["b%ds%d" % (bar, k) for k in range(start, start + count)][:8]

    def said(i):
        if c[i] == 1 and name[i] == let[i]:
            return ["%s is %d" % (let[i], v[i])]
        return ["%s = %d × %d = %d" % (name[i], c[i], v[i], prod[i]), "%s = %d × %d" % (name[i], c[i], v[i])]

    figs, seen = [], set()
    for i in range(len(steps_of(q))):
        text = step_text(q, i).replace("-", "−")
        means = re.match(r"^(\d*[a-z]) means", text)
        add = re.search(r"Now add ([a-z]), which is", text)
        if "So " in text or text.startswith(("The value", "Add the two parts", "Subtract the second part")):
            if shown == [True, True] and figs and "done" in seen:
                figs.append(None)   # the answer picture is already up
                continue
            seen.add("done")
            shown = [True, True]
            if minus:
                taken = S(n(prod[1]) if c[1] == 1 else name[1], prod[1], "b")
                figs.append(bm(B(name[0], taken, V(total, tone="a")), hl=["b0s1"], note="%s = %d" % (expr, total)))
            else:
                figs.append([bm(B("", term(0), term(1), brace=n(total)), note=note)
                             for note in ("%d + %d = %d" % (prod[0], prod[1], total), "%s = %d" % (expr, total))])
        elif means and means.group(1) in name or add and add.group(1) in let:
            k = name.index(means.group(1)) if means else let.index(add.group(1))
            shown[k] = True
            if minus:
                bars = [B(name[0], term(0))] + ([B(name[1], term(1))] if k == 1 else [])
                figs.append([bm(*bars, hl=["b%d" % k], note=note) for note in said(k)])
            else:
                start = 0 if k == 0 else c[0]
                figs.append([bm(B("", term(0), term(1)), hl=keys(0, start, c[k]), note=note) for note in said(k)])
        elif minus and "take away" in text:
            shown[1] = True
            figs.append(bm(B(name[0], term(0)), B(name[1], term(1)), hl=["b1"], note="Take away %s, which is %d" % (name[1], prod[1])))
        else:
            figs.append(None)
    put(qid, None, figs, origin="rule")


def square_or_product(qid, q, vals, a, b):
    """a² (b is a) or ab: a grid of b rows of a."""
    if a not in vals or b not in vals or max(vals[a], vals[b]) > 12 or float(vals[a] * vals[b]) not in key_numbers(q):
        return P.note(qid, "grid rule does not fit")
    va, vb = vals[a], vals[b]
    name = "%s²" % a if a == b else a + b
    count = len(steps_of(q))
    first = grid(vb, va, note="%s = %s × %s = %d × %d: %d rows of %d" % (name, a, b, va, vb, vb, va))
    last = [grid(vb, va, note="%d rows of %d make %d, so %s = %d" % (vb, va, va * vb, name, va * vb))]
    meaning = grid(vb, va, note="%s means %s × %s: %d rows of %d" % (name, a, b, vb, va))   # a step that only says what it means
    put(qid, None, [meaning] * (count - 2) + [first, last], origin="rule")


def then_add_take(qid, q, vals, m):
    """mx + p − q, worked left to right."""
    c, x, p, k = int(m.group(1)), m.group(2), int(m.group(3)), int(m.group(4))
    if x not in vals or len(steps_of(q)) != 3 or c > 11:
        return P.note(qid, "left-to-right rule does not fit")
    v = vals[x]
    total = c * v + p - k
    if total <= 0 or float(total) not in key_numbers(q):
        return P.note(qid, "left-to-right rule does not fit")
    xs = pieces(c, n(v), v, "a")
    name = "%d%s" % (c, x)
    put(qid, None,
        [[bm(B("", xs), hl=["b0"], note=note) for note in ("%s = %d × %d = %d" % (name, c, v, c * v), "%s = %d × %d" % (name, c, v))],
         [bm(B("", xs, V(p, tone="b")), hl=["b0s%d" % c], note=note) for note in ("%d + %d = %d" % (c * v, p, c * v + p), "Then add %d" % p)],
         bm(B("", V(total, tone="a"), S("%d taken away" % k, k, "c")), hl=["b0s0"], note="%s + %d − %d = %d" % (name, p, k, total))],
        origin="rule")


for _qid, _q in sorted(P.qs.items()):
    _h = HEAD.match(_q["questionText"].replace("-", "−"))
    if not _h:
        continue
    _vals = dict((k, int(val)) for k, val in VALS.findall(_h.group(1)))
    _e = _h.group(2).replace(" ", "")
    _m = re.fullmatch(r"(\d*)([a-z])\+(\d*)([a-z])", _e)
    if _m:
        two_terms(_qid, _q, _vals, _m, False)
        continue
    _m = re.fullmatch(r"(\d*)([a-z])−(\d*)([a-z])", _e)
    if _m:
        two_terms(_qid, _q, _vals, _m, True)
        continue
    _m = re.fullmatch(r"([a-z])²", _e)
    if _m:
        square_or_product(_qid, _q, _vals, _m.group(1), _m.group(1))
        continue
    _m = re.fullmatch(r"([a-z])([a-z])", _e)
    if _m:
        square_or_product(_qid, _q, _vals, _m.group(1), _m.group(2))
        continue
    _m = re.fullmatch(r"(\d+)([a-z])\+(\d+)−(\d+)", _e)
    if _m:
        then_add_take(_qid, _q, _vals, _m)


# ── Rule: "Simplify: 3x + 1 + 2x + 2" (step figures only) ────────────────────
# The terms are sorted into two columns, x terms and plain numbers, and each column is joined.
# Shown after answering only: the sorted table is most of the answer.

SIMPLIFY = re.compile(r"^Simplify: (\d+)([a-z]) \+ (\d+) \+ (\d+)([a-z]) ([+−]) (\d+)$")
for _qid, _q in sorted(P.qs.items()):
    _m = SIMPLIFY.match(_q["questionText"].replace("-", "−"))
    if not _m:
        continue
    _a, _b, _c, _d = int(_m.group(1)), int(_m.group(3)), int(_m.group(4)), int(_m.group(7))
    _x, _sign = _m.group(2), _m.group(6)
    _k = _b + _d if _sign == "+" else _b - _d
    _ans = "%d%s + %d" % (_a + _c, _x, _k)
    _t = [s.get("text", "") for s in steps_of(_q)]
    _lets = "%d%s + %d%s" % (_a, _x, _c, _x)
    _nums = "%d %s %d" % (_b, _sign, _d)
    if (_x != _m.group(5) or _k <= 0 or P.q(_qid) and _ans != [o["text"] for o in _q["options"] if o["id"] == _q["correctAnswer"]][0]
            or len(_t) != 3 or ("%d%s" % (_a + _c, _x)) not in _t[0] or ("= %d" % _k) not in _t[1] or _ans not in _t[2]):
        P.note(_qid, "simplify rule does not fit the steps")
        continue
    _H = ["%s terms" % _x, "Plain numbers"]
    put(_qid, None,
        [tb([[_lets, _nums], ["%d%s" % (_a + _c, _x), "?"]], _H, hl=["r1"], note="Join the %s terms: %s = %d%s" % (_x, _lets, _a + _c, _x)),
         tb([[_lets, _nums], ["%d%s" % (_a + _c, _x), n(_k)]], _H, hl=["r1"], note="Now the plain numbers: %s = %d" % (_nums, _k)),
         tb([[_lets, _nums], ["%d%s" % (_a + _c, _x), n(_k)]], _H, note="The two kinds cannot be joined: %s" % _ans)],
        origin="rule")


# ── Drawn one by one: putting numbers in (step figures only) ─────────────────

put("Q_CH13_001", None,
    {0: bm(B("a + 4", V(3), V(4, tone="b")), hl=["b0s0"], note="Write 3 in place of a: a + 4 becomes 3 + 4"),
     1: bm(B("a + 4", V(3), V(4, tone="b"), brace="7"), note="3 + 4 = 7"),
     2: bm(B("a + 4", V(3), V(4, tone="b"), brace="7"), hl=["b0"], note="The value of a + 4 is 7")})

put("Q_CH13_003", None,
    {0: bm(B("2a", V(3), V(3), brace="6"), note="2a means 2 times a: 2 × 3 = 6"),
     1: bm(B("2a/3", [V(2, tone="b")] * 3, brace="6"), note="The line means divide by 3: 6 ÷ 3 = 2"),
     2: bm(B("2a/3", [V(2, tone="b")] * 3, brace="6"), hl=["b0s0"], note="The value of 2a/3 is 2")})

_fa, _fb = [V(3)] * 5, [V(5, tone="b")] * 3
put("Q_CH13_010", None,
    {0: bm(B("5a", _fa, brace="15"), note="5a means 5 times a: 5 × 3 = 15"),
     1: bm(B("5a", _fa, brace="15"), B("3b", _fb, brace="15"), hl=["b1"], note="3b means 3 times b: 3 × 5 = 15"),
     2: bm(B("take away", _fa, brace="15"), B("add", _fb, brace="15"), hl=["b0", "b1"], note="12 − 15 + 15: taking 15 away and adding 15 undo each other"),
     3: bm(B("", V(12, tone="c")), note="12 − 15 + 15 = 12")})

put("Q_CH13_002", None,
    {0: bm(B("4a", [S("a", 3)] * 4), note="4a means 4 lots of a"),
     1: bm(B("4a", [V(3)] * 4, brace="12"), note="4 × 3 = 12")})

put("Q_CH13_004", None,
    {0: bm(B("a + 12", V(3), V(12, tone="b"), brace="15"), note="Work out the bracket first: 3 + 12 = 15"),
     1: bm(B("(a + 12)/3", [V(5, tone="c")] * 3, brace="15"), note="The whole bracket is divided by 3: 15 ÷ 3 = 5"),
     2: bm(B("(a + 12)/3", [V(5, tone="c")] * 3, brace="15"), hl=["b0s0"], note="The value of (a + 12)/3 is 5")})

put("Q_CH13_006", None,
    {0: grid(3, 3, note="a² = 3 × 3 = 9: 3 rows of 3"),
     1: bm(B("4a²", [V(9)] * 4, brace="36"), note="4 lots of 9 make 36")})

_g = [V(3), V(5, tone="b")]
put("Q_CH13_011", None,
    {0: [bm(B("a + b", _g, brace="8"), note="3 + 5 = 8"), bm(B("a + b", _g), note="Work out the bracket first: 3 + 5")],
     1: bm(B("4(a + b)", _g * 4, brace="32"), note="4 groups of 3 + 5 make 32")})

put("EXT_G4_FP_2020_018", None,
    {0: bm(B("b", V(3, tone="b")), B("a", V(3, tone="b"), V(3, tone="b"), brace="6"), hl=["b1"], note="a = 2 × 3 = 6"),
     1: [bm(B("2a", S("3", 3, "b"), V(9, tone="a"), brace="12"), hl=["b0s1"], note="2 × 6 − 3 = 12 − 3 = 9"),
         bm(B("2a", V(6), V(6)), B("b", V(3, tone="b")), note="2a − b = 2 × 6 − 3 = 9")]})

# Collecting like terms, shown as pieces (after answering only: the picture is the answer).
_a = lambda t="a": S("a", 3, t)
put("Q_CH13_021", None,
    {0: bm(B("5a + a", [_a()] * 5, _a("b")), hl=["b0s5"], note="The a on its own means 1a"),
     1: bm(B("5a + a", [_a()] * 5, _a("b")), note="5 + 1 = 6 pieces of a"),
     2: bm(B("5a + a", [_a()] * 6, brace="6a"), note="5a + a = 6a")})

_x, _y = S("x", 3, "a"), S("y", 2, "b")
put("Q_CH13_022", None,
    {0: bm(B("3x + 4y", [_x] * 3, [_y] * 4), B("x + 2y", _x, [_y] * 2), hl=["b0s0", "b0s1", "b0s2", "b1s0"], note="3x and 1x make 4x"),
     1: bm(B("3x + 4y", [_x] * 3, [_y] * 4), B("x + 2y", _x, [_y] * 2), hl=["b0s3", "b0s4", "b0s5", "b0s6", "b1s1", "b1s2"], note="4y and 2y make 6y"),
     2: bm(B("", [_x] * 4, [_y] * 6, brace="4x + 6y"), note="x and y are different letters, so they stay as two parts")})

_b, _c = S("b", 2, "a"), S("c", 1.5, "b")
_row = lambda: B("2b + 4c", [_b] * 2, [_c] * 4)
put("EXT_G4_WS2_CH13_007", None,
    {0: bm(_row(), _row(), _row(), hl=["b0s0", "b0s1", "b1s0", "b1s1", "b2s0", "b2s1"], note="3 groups of 2b make 6b"),
     1: bm(_row(), _row(), _row(), note="3 groups of 4c make 12c"),
     2: bm(_row(), _row(), _row(), hl=["b0", "b1", "b2"], note="3(2b + 4c) = 6b + 12c")})

_d = S("x − y", 2, "c")
put("EXT_G4_WS2_CH13_005", None,
    {0: bm(B("x", S("y", 3, "b"), _d), hl=["b0s1"], note="The difference of x and y is x − y"),
     1: bm(B("", [_d] * 4), note="4 times the whole difference"),
     2: bm(B("", [_d] * 4, brace="4(x − y)"), note="The brackets keep x − y together")})


# ── Drawn one by one: stories ────────────────────────────────────────────────

put("EXT_G4_WS2_CH13_001", bm(B("", S("x kg", 5), S("2 kg", 2, "b"), brace="?"), note="Apples and bananas together"),
    {1: bm(B("", S("x kg", 5), S("2 kg", 2, "b"), brace="?"), hl=["b0"], note="Total weight: add the two weights"),
     2: bm(B("", S("x kg", 5), S("2 kg", 2, "b"), brace="(x + 2) kg"))})

put("EXT_G4_WS2_CH13_002", bm(B("", [S("k", 2)] * 6, brace="?"), note="k pages every hour, for 6 hours"),
    {1: bm(B("", [S("k", 2)] * 6, brace="?"), hl=["b0"], note="6 lots of k: 6 × k = 6k"),
     2: bm(B("", [S("k", 2)] * 6, brace="6k pages"))})

put("EXT_G4_WS2_CH13_003", bm(B("", Uq(6, "age now ?"), S("8 years", 3, "c"), brace="y"), note="8 years from now Rahul will be y years old"),
    {1: bm(B("", Uq(6, "age now ?"), S("8 years", 3, "c"), brace="y"), hl=["b0s1"], note="Now he is 8 years younger: take 8 away from y"),
     2: bm(B("", S("y − 8", 6), S("8 years", 3, "c"), brace="y"), hl=["b0s0"])})

_ab = [S("a", 4), S("b", 3, "b")]
put("EXT_G4_WS2_CH13_004", bm(B("", _ab, S("4", 2, "c"), brace="?"), note="The sum of a and b, and 4 more"),
    {0: bm(B("", _ab, brace="a + b"), note="The sum of a and b"),
     1: bm(B("", _ab, S("4", 2, "c")), hl=["b0s2"], note="4 more than this: add 4"),
     2: bm(B("", _ab, S("4", 2, "c"), brace="a + b + 4"))})

_q3 = [S("₹q", 2)] * 3
put("G4A_ALGEBRA_001", bm(B("", _q3, Uq(4, "left ?"), brace="₹p"), note="3 pencils at ₹q each are paid for out of ₹p"),
    {0: bm(B("", _q3, Uq(4, "left ?"), brace="₹p"), hl=["b0s0", "b0s1", "b0s2"], note="3 pencils cost 3 times q: 3q rupees"),
     1: bm(B("", _q3, Uq(4, "left ?"), brace="₹p"), hl=["b0s3"], note="Money left = money she had − money she spent"),
     2: bm(B("", _q3, S("p − 3q", 4, "c"), brace="₹p"), hl=["b0s3"])})

put("G4A_ALGEBRA_002", bm(B("First", S("r", 10)), B("Second", S("40 fewer than r", 7)), note="Total runs in both innings = ?"),
    {1: bm(B("First", S("r", 10)), B("Second", S("r − 40", 7)), hl=["b1"], note="40 fewer than r is r − 40"),
     2: bm(B("First", S("r", 10)), B("Second", S("r − 40", 7)), note="r + r − 40: the two r terms make 2r"),
     3: bm(B("First", S("r", 10)), B("Second", S("r − 40", 7)), hl=["b0", "b1"], note="Total: 2r − 40")})

_H = ["Position", "1st", "2nd", "3rd", "nth"]
put("G4A_ALGEBRA_004", tb([["Odd number", "1", "3", "5", "?"]], _H),
    {0: tb([["Even number", "2", "4", "6", "2n"], ["Odd number", "1", "3", "5", "?"]], _H, hl=["r0"], note="Each even number is 2 times its position"),
     1: tb([["Even number", "2", "4", "6", "2n"], ["Odd number", "1", "3", "5", "?"]], _H, hl=["r1"], note="Each odd number is 1 less than the even number above it"),
     3: tb([["Even number", "2", "4", "6", "2n"], ["Odd number", "1", "3", "5", "2n − 1"]], _H, hl=["r1"])})

_t = {"ab": "(2a + 3) cm", "ca": "(2a + 3) cm", "bc": "(a − 2) cm"}
put("G4A_ALGEBRA_005", tri("isosceles", _t, note="Perimeter = ?"),
    {0: tri("isosceles", _t, hl=["ab", "bc", "ca"], note="Add the three sides"),
     1: tri("isosceles", _t, note="The a terms: 2a + 2a + a = 5a"),
     2: tri("isosceles", _t, note="The numbers: 3 + 3 − 2 = 4"),
     3: tri("isosceles", _t, hl=["ab", "bc", "ca"], note="Perimeter = (5a + 4) cm")})

_pts = [(1, 3), (11, 3), (11, 8), (1, 8)]
_ed = ["wall", "q m", "p m", "q m"]
put("G4A_ALGEBRA_006", poly(_pts, _ed, right=[0, 1, 2, 3], note="A fence goes on three sides only"),
    {1: poly(_pts, _ed, right=[0, 1, 2, 3], hl=["e1", "e2", "e3"], note="The fence: one long side and two short sides"),
     2: poly(_pts, _ed, right=[0, 1, 2, 3], hl=["e1", "e2", "e3"], note="p + q + q"),
     3: poly(_pts, _ed, right=[0, 1, 2, 3], hl=["e1", "e2", "e3"], note="Fence = (p + 2q) m")})

_x = S("x", 3)
put("G4A_ALGEBRA_009", bm(B("Anu", _x), B("Father", [_x] * 3, V(4, tone="c")), note="Sum of their ages after 5 years = ?"),
    {0: bm(B("Anu", _x), B("Father", [_x] * 3, V(4, tone="c"), brace="3x + 4"), hl=["b1"], note="Three times x and 4 more"),
     1: bm(B("Anu", _x, V(5, tone="b"), brace="x + 5"), B("Father", [_x] * 3, V(4, tone="c"), V(5, tone="b"), brace="3x + 9"), hl=["b0s1", "b1s4"], note="After 5 years each is 5 older"),
     2: bm(B("Anu", _x, V(5, tone="b"), brace="x + 5"), B("Father", [_x] * 3, V(4, tone="c"), V(5, tone="b"), brace="3x + 9"), note="The x terms make 4x and the numbers make 14"),
     3: bm(B("Anu", _x, V(5, tone="b"), brace="x + 5"), B("Father", [_x] * 3, V(4, tone="c"), V(5, tone="b"), brace="3x + 9"), hl=["b0", "b1"], note="Sum = 4x + 14")})

_n, _1 = S("n", 5), V(1, tone="c")
_three = lambda **kw: bm(B("Smallest", _n), B("Next", _n, _1), B("Largest", _n, _1, _1), **kw)
put("G4A_ALGEBRA_010", tb([["n", "?", "?"]], ["Smallest", "Next", "Largest"], note="Three numbers, one after another"),
    {0: tb([["n", "n + 1", "n + 2"]], ["Smallest", "Next", "Largest"]),
     1: _three(note="n + n + 1 + n + 2"),
     2: _three(hl=["b1s1", "b2s1", "b2s2"], note="Three n make 3n, and 1 + 2 = 3"),
     3: _three(note="Sum = 3n + 3")})

_r = S("₹12", 12, "b")
_taxi = lambda **kw: bm(B("", V(50, "₹"), _r, _r, S("…", 12, "b"), _r, brace="d km"), **kw)
put("G4A_ALGEBRA_011", _taxi(note="First km ₹50, then ₹12 for every km after it"),
    {0: _taxi(hl=["b0s0"], note="The first kilometre costs ₹50"),
     1: _taxi(hl=["b0s1", "b0s2", "b0s3", "b0s4"], note="d − 1 kilometres at ₹12 each: 12d − 12"),
     2: _taxi(note="50 + 12d − 12"),
     3: _taxi(hl=["b0"], note="Fare = 12d + 38")})

_m = lambda t="a": S("m", 4, t)
put("G4A_ALGEBRA_012", bm(B("Riya", [_m()] * 3, V(5, tone="c")), B("Sameer", [_m()] * 2, V(4, tone="c")), note="Riya gives one full box to Sameer"),
    {0: bm(B("Riya", [_m()] * 2, V(5, tone="c"), brace="2m + 5"), B("Sameer", [_m()] * 2, V(4, tone="c")), hl=["b0"], note="Riya now has 2 boxes and 5 loose mangoes"),
     1: bm(B("Riya", [_m()] * 2, V(5, tone="c"), brace="2m + 5"), B("Sameer", [_m()] * 2, _m("b"), V(4, tone="c"), brace="3m + 4"), hl=["b1s2"], note="Sameer now has 3 boxes and 4 loose mangoes"),
     2: bm(B("Riya", [_m()] * 2, V(5, tone="c"), brace="2m + 5"), B("Sameer", [_m()] * 2, _m("b"), V(4, tone="c"), brace="3m + 4"), hl=["b1s2"], note="3m − 2m = m, and 4 − 5 takes 1 away"),
     3: bm(B("Riya", [_m()] * 2, V(5, tone="c"), brace="2m + 5"), B("Sameer", [_m()] * 2, _m("b"), V(4, tone="c"), brace="3m + 4"), note="Sameer has m − 1 more")})

_o = [(0, "n"), (1, "n + 1"), (3, "n + 3"), (5, "n + 5"), (7, "n + 7"), (9, "n + 9")]
_c = [(10, "10"), (11, "11"), (13, "13"), (15, "15"), (17, "17"), (19, "19")]
put("G4A_ALGEBRA_013", None,
    {1: nl(0, 10, 1, points=_o, ticks="none", note="Odd numbers go up in twos from n + 1"),
     2: nl(10, 20, 1, points=_c, ticks="none", note="Check with n = 10: the 5th one is 19, which is 10 + 9"),
     3: nl(0, 10, 1, points=_o, ticks="none", hl=["p5"], note="The 5th odd number after n is n + 9")})

_sq = dict(square=True, length="(3a + 6) cm")
_q = {"ab": "?", "bc": "?", "ca": "?"}
put("G4A_ALGEBRA_014", rect(note="This wire square is opened out and bent into a triangle", **_sq),
    {0: rect(hl=["border"], note="Wire = 4 × (3a + 6) = 12a + 24 cm", **_sq),
     1: tri("equilateral", _q, hl=["ab", "bc", "ca"], note="The three equal sides add up to 12a + 24 cm"),
     2: tri("equilateral", _q, note="12a ÷ 3 = 4a and 24 ÷ 3 = 8"),
     3: tri("equilateral", {"ab": "(4a + 8) cm", "bc": "(4a + 8) cm", "ca": "(4a + 8) cm"})})

_g = [S("x", 3), S("x", 3), S("y", 4, "b")]
put("G4A_ALGEBRA_015", bm(B("2x + y", _g, brace="10"), note="Use this to find 6x + 3y − 4"),
    {0: bm(B("2x + y", _g, brace="10"), B("6x + 3y", _g * 3), note="6x + 3y is 3 groups of 2x + y"),
     1: bm(B("2x + y", _g, brace="10"), B("6x + 3y", _g * 3, brace="30"), hl=["b1"], note="3 × 10 = 30"),
     2: bm(B("2x + y", _g, brace="10"), B("6x + 3y", _g * 3, brace="30"), note="30 − 4 = 26")})

_w = S("x − 3", 4)
put("G4A_ALGEBRA_017", bm(B("Ravi then", Uq(4)), B("Meena then", Uq(4), Uq(4)), note="Three years ago. Ravi is x years old now."),
    {0: bm(B("Ravi then", _w), B("Meena then", Uq(4), Uq(4)), hl=["b0"], note="Three years ago Ravi was x − 3"),
     1: bm(B("Ravi then", _w), B("Meena then", _w, _w, brace="2x − 6"), hl=["b1"], note="Twice that: 2 × (x − 3) = 2x − 6"),
     2: bm(B("Meena now", _w, _w, V(3, tone="c"), brace="2x − 6 + 3"), hl=["b0s2"], note="Add 3 years to reach her age now"),
     3: bm(B("Meena now", _w, _w, V(3, tone="c"), brace="2x − 3"))})

put("G4A_ALGEBRA_018", grid(1, 3, note="A row of squares made with matchsticks"),
    {0: grid(1, 1, note="The first square uses 4 matchsticks"),
     1: grid(1, 3, note="Each new square needs only 3 more: 3 × (n − 1) = 3n − 3"),
     2: grid(1, 3, note="4 + 3n − 3 = 3n + 1"),
     3: grid(1, 3, note="Check with 3 squares: 3 × 3 + 1 = 10")})

_H = ["k", "Anu: 5k + 3", "Bala: 3k + 11"]
put("G4A_ALGEBRA_019", None,
    {1: tb([["1", "8", "14"], ["4", "23", "23"]], _H, note="The gap of 6 closes by 2 each time k goes up by 1"),
     2: tb([["1", "8", "14"], ["4", "23", "23"]], _H, hl=["r1"], note="Equal at k = 4. Anu has more for k = 5 to 10.")})

_L = [(0.6, 4.2), (9, 4.2), (9, 6.6), (11.4, 6.6), (11.4, 7.8), (0.6, 7.8)]
_le = [None, "a cm", "a cm", None, "(2a + 5) cm", "(a + 1) cm"]
_ra = [0, 1, 2, 3, 4, 5]
put("G4A_ALGEBRA_020", poly(_L, _le, right=_ra, note="A square of side a cm is cut from one corner"),
    {0: rect(length="(2a + 5) cm", breadth="(a + 1) cm", proportion=3, hl=["border"], note="Whole card: 2 × (3a + 6) = 6a + 12 cm"),
     1: poly(_L, _le, right=_ra, note="The cut takes away two outside pieces, each a cm long"),
     2: poly(_L, _le, right=_ra, hl=["e1", "e2"], note="Two new inside edges, each a cm long, take their place"),
     3: poly(_L, _le, right=_ra, note="The perimeter is still (6a + 12) cm")})

_s = lambda t="a": S("s", 30, t)
put("G4A_ALGEBRA_022", bm(B("Sana", _s()), B("Tara", _s(), V(20, "₹", tone="c")), note="Then Tara gives ₹15 to Sana"),
    {0: bm(B("Sana", _s(), brace="s"), B("Tara", _s(), V(20, "₹", tone="c"), brace="s + 20")),
     1: bm(B("Sana", _s(), brace="s"), B("Tara", _s(), V(5, "₹", tone="c"), brace="s + 5"), hl=["b1"], note="Tara: s + 20 − 15 = s + 5"),
     2: bm(B("Sana", _s(), V(15, "₹", tone="b"), brace="s + 15"), B("Tara", _s(), V(5, "₹", tone="c"), brace="s + 5"), hl=["b0"], note="Sana: s + 15"),
     3: bm(B("Sana", _s(), V(5, "₹", tone="c"), V(10, "₹", tone="b"), brace="s + 15"), B("Tara", _s(), V(5, "₹", tone="c"), brace="s + 5"), hl=["b0s2"], note="s + 15 is 10 more than s + 5")})

put("G4A_ALGEBRA_023", tb([["?", "?", "m", "?", "?"]], note="Five numbers in a row. The middle one is m."),
    {0: tb([["m − 2", "m − 1", "m", "m + 1", "m + 2"]]),
     1: tb([["m − 2", "m − 1", "m", "m + 1", "m + 2"]], hl=["r0"], note="Smallest: m − 2. Greatest: m + 2."),
     2: tb([["m − 2", "m − 1", "m", "m + 1", "m + 2"]], note="m − 2 + m + 2: the − 2 and the + 2 cancel"),
     3: tb([["6", "7", "8", "9", "10"]], note="Check: 6 + 10 = 16, and 2 × 8 = 16"),
     4: tb([["m − 2", "m − 1", "m", "m + 1", "m + 2"]], note="Smallest + greatest = 2m")})

_R = dict(length="(3a + 2) cm", inside="Perimeter (10a + 6) cm", proportion=1.6)
put("G4A_ALGEBRA_024", rect(breadth="?", **_R),
    {0: rect(breadth="?", hl=["length", "breadth"], note="Length + breadth = half of 10a + 6 = 5a + 3", **_R),
     1: rect(breadth="?", hl=["breadth"], note="Breadth = 5a + 3 − (3a + 2)", **_R),
     2: rect(breadth="?", hl=["breadth"], note="5a − 3a = 2a and 3 − 2 = 1", **_R),
     3: rect(breadth="(2a + 1) cm", hl=["breadth"], **_R)})

_H = ["Number", "Tens", "Ones"]
_T = [["First", "t", "u"], ["Swapped", "u", "t"]]
put("G4A_ALGEBRA_025", tb(_T, _H, note="Swapping the digits makes a second number"),
    {0: tb(_T, _H, hl=["r0"], note="The first number is worth 10t + u"),
     1: tb(_T, _H, hl=["r1"], note="The swapped number is worth 10u + t"),
     2: tb(_T, _H, note="10t + t = 11t and u + 10u = 11u"),
     3: tb([["First", "4", "3"], ["Swapped", "3", "4"]], _H, note="Check: 43 + 34 = 77, and 11 × 4 + 11 × 3 = 77")})

_x6, _2 = S("x", 6), V(2, tone="c")
_top = B("3x + 2", [_x6] * 3, _2, brace="20")
put("G4A_ALGEBRA_026", bm(_top, note="Use this to find 3(x + 2)"),
    {0: bm(_top, B("3(x + 2)", [_x6, _2] * 3, brace="3x + 6"), note="Open the bracket: 3 lots of x + 2"),
     1: bm(_top, B("3(x + 2)", [_x6, _2] * 3, brace="3x + 6"), hl=["b1s3", "b1s5"], note="3x + 6 is 4 more than 3x + 2"),
     2: bm(_top, B("3(x + 2)", [_x6, _2] * 3, brace="24"), hl=["b1"], note="20 + 4 = 24"),
     3: bm(_top, B("3(x + 2)", [V(6), _2] * 3, brace="24"), note="Check: x = 6, and 3 × (6 + 2) = 24")})

_p = lambda v: S(None, v)
put("G4A_ALGEBRA_027", bm(B("", _p(3), _p(3), S("…", 3), _p(3), brace="n pieces"), note="Each cut takes 3 minutes. How long is all the cutting?"),
    {0: bm(B("1 cut", _p(6), _p(6), brace="2 pieces", chk=False), B("2 cuts", [_p(4)] * 3, brace="3 pieces", chk=False), note="The cuts are always 1 fewer than the pieces"),
     1: bm(B("", _p(3), _p(3), S("…", 3), _p(3), brace="n pieces"), note="n pieces need n − 1 cuts"),
     2: bm(B("", _p(3), _p(3), S("…", 3), _p(3), brace="n pieces"), note="3 × (n − 1) = 3n − 3 minutes")})

put("EXT_G4_FP_2020_037", rect(length="breadth + 2", breadth="a + 2", inside="Perimeter = ?"),
    {0: rect(length="a + 4", breadth="a + 2", inside="Perimeter = ?", hl=["length"], note="The length is 2 more: a + 2 + 2 = a + 4"),
     1: rect(length="a + 4", breadth="a + 2", inside="Perimeter = ?", hl=["length", "breadth"], note="a + 4 + a + 2 = 2a + 6"),
     2: rect(length="a + 4", breadth="a + 2", inside="Perimeter = 4a + 12", hl=["border"], note="2 × (2a + 6) = 4a + 12")})

_H = ["When", "Sum of ages"]
put("PYQ_2017_Q18", tb([["5 years ago", "5x"], ["Today", "?"], ["5 years hence", "?"]], _H, note="A mother and her daughter"),
    {0: tb([["5 years ago", "5x"], ["Today", "5x + 10"], ["5 years hence", "?"]], _H, hl=["r1"], note="Each is 5 years older: 5 + 5 = 10 more"),
     1: tb([["5 years ago", "5x"], ["Today", "5x + 10"], ["5 years hence", "?"]], _H, hl=["r2"], note="Each grows 5 years older again: another 10"),
     2: tb([["5 years ago", "5x"], ["Today", "5x + 10"], ["5 years hence", "5x + 20"]], _H, hl=["r2"], note="10 + 10 = 20"),
     3: tb([["5 years ago", "5x"], ["Today", "5x + 10"], ["5 years hence", "5x + 20"]], _H, note="Count the years for both people, all the way to 5 years hence")})

_all = {"ab": "(7m − 2n)", "bc": "(7m − 2n)", "ca": "(7m − 2n)"}
put("PYQ_2017_Q22", tri("equilateral", {"bc": "(7m − 2n)"}, note="Perimeter = ?"),
    {0: tri("equilateral", _all, hl=["ab", "bc", "ca"], note="3 equal sides: the perimeter is 3 times one side"),
     1: tri("equilateral", _all, note="3 times 7m is 21m"),
     2: tri("equilateral", _all, note="3 times 2n is 6n, and it is still taken away"),
     3: tri("equilateral", _all, hl=["ab", "bc", "ca"], note="Perimeter = 21m − 6n")})

_R = dict(length="(2a + 5b) cm", breadth="7 cm", proportion=2.2)
put("PYQ_2018_Q04", rect(note="Perimeter = ?", **_R),
    {0: rect(hl=["border"], note="Perimeter = 2 lengths and 2 breadths", **_R),
     1: rect(hl=["length"], note="2 lengths: 4a + 10b", **_R),
     2: rect(hl=["breadth"], note="2 breadths: 2 × 7 = 14", **_R),
     3: rect(hl=["border"], note="Perimeter = (4a + 10b + 14) cm", **_R)})

_sq = dict(square=True, length="(3a + 2b)")
put("PYQ_2018_Q37", rect(note="Perimeter = ?", **_sq),
    {0: rect(hl=["border"], note="4 equal sides: the perimeter is 4 times the side", **_sq),
     1: rect(hl=["border"], note="Multiply each part of the side by 4", **_sq),
     2: rect(hl=["border"], note="2(6a + 4b) is 12a + 8b as well", **_sq)})

_sq = dict(square=True, length="(4x − 3y) cm")
put("PYQ_2019_Q36", rect(note="Perimeter = ?", **_sq),
    {0: rect(hl=["border"], note="4 equal sides: the perimeter is 4 times one side", **_sq),
     1: rect(hl=["border"], note="4 times 4x is 16x", **_sq),
     2: rect(hl=["border"], note="4 times 3y is 12y, and it is still taken away", **_sq),
     3: rect(hl=["border"], note="Perimeter = (16x − 12y) cm", **_sq)})

# Counting on or back in twos from a letter.
_o = [(0, "P"), (2, "P + 2"), (4, "P + 4"), (6, "P + 6")]
_h = [(0, 2, "1st"), (2, 4, "2nd"), (4, 6, "3rd")]
put("PYQ_2016_Q20", None,
    {1: nl(0, 8, 1, points=_o, hops=_h, ticks="none", note="Each odd number after P adds 2 more"),
     2: nl(0, 8, 1, points=_o, hops=_h, ticks="none", note="The 17th needs 17 jumps of 2: 17 × 2 = 34")})

put("PYQ_2017_Q24", None,
    {2: nl(12, 20, 2, points=[(20, "20"), (18, "18"), (16, "16"), (14, "14")], hops=[(20, 18, "1st"), (18, 16, "2nd"), (16, 14, "3rd")],
           ticks="none", note="Check with 20: the 3rd even number before it is 20 − 6 = 14")})

_g = [(0, "G"), (12, "G + 12")]
put("PYQ_2018_Q21", None,
    {1: nl(0, 12, 2, points=_g, ticks="none", note="6 steps back, 2 each time, take away 12"),
     2: nl(0, 12, 2, points=_g, ticks="none", hl=["p0"], note="G + 12 − 12 = G")})

# Notes, ropes and prices written with letters.
put("Q_CH13_013", bm(B("d", S("d", 5)), B("Successor", Uq(6)), note="The successor is the next number"),
    {0: bm(B("d", S("d", 5)), B("Successor", S("d", 5), V(1, tone="c"), brace="d + 1"), hl=["b1"]),
     1: bm(B("d", S("d", 5)), B("Successor", S("d", 5), V(1, tone="c"), brace="d + 1"), hl=["b0", "b1"], note="Add them: d + d + 1"),
     2: bm(B("d", S("d", 5)), B("Successor", S("d", 5), V(1, tone="c"), brace="d + 1"), hl=["b0s0", "b1s0"], note="d and d together make 2d"),
     3: bm(B("d", V(5)), B("Successor", V(5), V(1, tone="c"), brace="6"), note="Check with d = 5: 5 + 6 = 11, so the sum is 2d + 1")})

_t = S("₹10", 10)
_notes = lambda **kw: bm(B("", _t, _t, S("…", 10), _t, brace=kw.pop("brace", "m notes")), **kw)
put("Q_CH13_014", _notes(note="m notes of ten rupees each"),
    {0: bm(B("2 notes", _t, _t, brace="₹20"), B("3 notes", _t, _t, _t, brace="₹30"), note="2 notes make ₹20 and 3 notes make ₹30"),
     1: _notes(note="The total is always 10 times the number of notes"),
     2: _notes(brace="₹10m", note="m notes are worth 10 times m")})

_f = lambda v: [S(None, v), S(None, v), S("…", v), S(None, v)]
_two = lambda b1, b2, **kw: bm(B("Ten-rupee notes", _f(10), brace=b1), B("Five-rupee notes", _f(5), brace=b2), **kw)
put("Q_CH13_015", _two("m notes", "n notes"),
    {0: _two("10m", "n notes", hl=["b0"], note="m ten-rupee notes are worth 10 times m"),
     1: _two("10m", "5n", hl=["b1"], note="n five-rupee notes are worth 5 times n"),
     2: _two("10m", "5n", hl=["b0", "b1"], note="Total = ₹(10m + 5n)")})

put("Q_CH13_016", bm(B("", S("12 spent", 5, "c"), Uq(7, "left ?"), brace="m notes")),
    {1: bm(B("", S("12 spent", 5, "c"), Uq(7, "left ?"), brace="m notes"), hl=["b0s0"], note="She spends 12 notes: take 12 away from m"),
     2: bm(B("", S("12 spent", 5, "c"), S("m − 12", 7), brace="m notes"), hl=["b0s1"], note="We are counting notes, not rupees")})

_so = [S("8 then", 8), S("x years", 3, "b"), S("y years", 4, "c")]
put("Q_CH13_017", bm(B("Soham", _so, brace="?"), note="From x years ago, to now, to y years from now"),
    {0: bm(B("Soham", _so, brace="?"), hl=["b0s0", "b0s1"], note="His age now is 8 + x"),
     1: bm(B("Soham", _so, brace="?"), hl=["b0s2"], note="y years hence: add y to his age now"),
     2: bm(B("Soham", _so, brace="8 + x + y"))})

_px = S("₹x", 3)
put("Q_CH13_018", bm(B("Pencil", _px), B("Pen", [_px] * 3), note="A pen costs thrice as much as a pencil"),
    {0: bm(B("Pencil", _px), B("Pen", [_px] * 3, brace="₹3x"), hl=["b1"], note="Thrice means 3 times: the pen costs 3 × x"),
     1: bm(B("Pencil", _px), B("Pen", [_px] * 3, brace="₹3x"), hl=["b0", "b1"], note="3 lots of x and 1 more lot of x make 4 lots of x"),
     2: bm(B("Together", [_px] * 4, brace="₹4x"), note="A pen and a pencil together cost ₹4x")})

put("Q_CH13_019", bm(B("", S("y m cut", 4, "c"), Uq(8, "left ?"), brace="x m")),
    {0: bm(B("", S("y m cut", 4, "c"), Uq(8, "left ?"), brace="x m"), hl=["b0"], note="The whole rope is x metres long"),
     1: bm(B("", S("y m cut", 4, "c"), Uq(8, "left ?"), brace="x m"), hl=["b0s0"], note="Cutting makes it shorter: subtract y from x"),
     2: bm(B("", S("y m cut", 4, "c"), S("(x − y) m", 8), brace="x m"), hl=["b0s1"])})

put("Q_CH13_020", bm(B("", S("y cm cut", 3, "c"), Uq(9, "? cm left"), brace="x m"), note="The wire is in metres, the cut piece is in centimetres"),
    {0: bm(B("", S("y cm cut", 3, "c"), Uq(9, "? cm left"), brace="100x cm"), note="1 m = 100 cm, so x m = 100x cm"),
     1: bm(B("", S("y cm cut", 3, "c"), Uq(9, "? cm left"), brace="100x cm"), hl=["b0s0"], note="Now both are in centimetres: take away y"),
     2: bm(B("", S("y cm cut", 3, "c"), S("(100x − y) cm", 9), brace="100x cm"), hl=["b0s1"])})

P.save()
P.review()
