"""Figures for Grade 4 gr4_ages. Writes data/question-figures/parts/g4-gr4_ages.json.

    python -X utf8 scripts/figures/authoring/g4_gr4_ages.py

An age is drawn as a bar whose length is the age, so two people's bars can be compared and
"years ago" / "years from now" are pieces put on or taken off. The generated family (two
ages, then a sum after or a difference before some years) is drawn by rule from the numbers
in the question; the rest are drawn one by one.
"""
import re

from g4_gr4_equations_lib import Part, S, V, Uq, B, bm, nl, tb, n, steps_of, step_text, says, key_numbers

P = Part("gr4_ages")
put = P.put

# ── Rule: "A is 47 years old and B is 9 years old. What was the difference ... / will be the sum ..." ──

PAIR = re.compile(r"^(\w+) is (\d+) years old and (\w+) is (\d+) years old\. What (?:was the difference in their ages (\d+) years ago|"
                  r"will be the sum of their ages after (\d+) years)\?$")


def sum_after(qid, q, n1, a, n2, b, y):
    texts = [s.get("text", "") for s in steps_of(q)]
    # The steps: the first person's new age, the second person's new age, then the two added.
    if (float(a + b + 2 * y) not in key_numbers(q) or len(texts) != 3 or not says(texts[0], a + y)
            or not says(texts[1], b + y) or not says(texts[2], a + b + 2 * y)):
        return P.note(qid, "sum rule does not fit the steps")
    more = lambda: S("%d more" % y, y, "c")
    base = lambda **kw: bm(B(n1, V(a), more(), brace=kw.pop("b1", None)), B(n2, V(b), more(), brace=kw.pop("b2", None)), **kw)
    put(qid, base(note="After %d years, what do their ages add up to?" % y),
        [base(b1=n(a + y), hl=["b0s1"], note="%s: %d + %d = %d" % (n1, a, y, a + y)),
         base(b1=n(a + y), b2=n(b + y), hl=["b1s1"], note="%s: %d + %d = %d" % (n2, b, y, b + y)),
         base(b1=n(a + y), b2=n(b + y), hl=["b0", "b1"], note="%d + %d = %d" % (a + y, b + y, a + b + 2 * y))], origin="rule")


def diff_before(qid, q, n1, a, n2, b, y):
    d = abs(a - b)
    if float(d) not in key_numbers(q) or min(a, b) - y <= 0:
        return P.note(qid, "difference rule does not fit")
    old, young = (0, 1) if a > b else (1, 0)
    names, ages = [n1, n2], [a, b]
    now = lambda **kw: bm(B(n1, V(a)), B(n2, V(b)), **kw)

    def gap(label, **kw):
        bars = [None, None]
        bars[old] = B(names[old], V(ages[young], tone="abc"[young]), S(label, d, "unknown" if label == "?" else "c"), brace=n(ages[old]))
        bars[young] = B(names[young], V(ages[young]))
        return bm(*bars, hl=["b%ds1" % old], **kw)

    def then(who, **kw):
        """`who` bars are split into the age then and the y years since."""
        bars = []
        for i in (0, 1):
            if i in who:
                bars.append(B(names[i], [V(ages[i] - y), S("%d years" % y, y, "c")], brace=n(ages[i])))
            else:
                bars.append(B(names[i], V(ages[i])))
        return bars

    before = now(note="%d years ago, what was the difference in their ages?" % y)
    count = len(steps_of(q))
    if count == 4:
        # The age then is written as a number where the checker allows it at that step, else as "47 − 6".
        was = lambda i, num: V(ages[i] - y) if num else S("%d − %d" % (ages[i], y), ages[i] - y)
        since = lambda: S("%d years" % y, y, "c")
        ways = [(True, True), (True, False), (False, True), (False, False)]
        s0 = [bm(B(n1, was(0, w), since(), brace=n(a)), B(n2, V(b)), hl=["b0s0"],
                 note=("%s's age %d years ago: %d − %d = %d" % (n1, y, a, y, a - y)) if w else "%s's age %d years ago" % (n1, y))
              for w in (True, False)]
        s1 = [bm(B(n1, was(0, w0), since(), brace=n(a)), B(n2, was(1, w1), since(), brace=n(b)), hl=["b1s0"],
                 note=("%s's age %d years ago: %d − %d = %d" % (n2, y, b, y, b - y)) if w1 else "%s's age %d years ago" % (n2, y))
              for w0, w1 in ways]
        s2 = [bm(B(n1 + " then", was(0, w0)), B(n2 + " then", was(1, w1)),
                 note=("%d − %d = %d" % (max(a, b) - y, min(a, b) - y, d)) if (w0 and w1) else "Compare the two ages %d years ago" % y)
              for w0, w1 in ways]
        s3 = gap(n(d), note="The gap is the same today: %d − %d = %d" % (max(a, b), min(a, b), d))
        figs = [s0, s1, s2, s3]
    elif count == 3 and says(step_text(q, 0), a - y) and says(step_text(q, 0), b - y) and says(step_text(q, 1), d):
        # Both ages then; their difference then; the same difference today.
        since = lambda: S("%d years" % y, y, "c")
        bars = [None, None]
        bars[old] = B(names[old] + " then", V(ages[young] - y, tone="abc"[young]), V(d, tone="c"), brace=n(ages[old] - y))
        bars[young] = B(names[young] + " then", V(ages[young] - y))
        figs = [bm(B(n1, V(a - y), since(), brace=n(a)), B(n2, V(b - y), since(), brace=n(b)), hl=["b0s0", "b1s0"],
                   note="%d years ago: %d − %d = %d and %d − %d = %d" % (y, a, y, a - y, b, y, b - y)),
                bm(*bars, hl=["b%ds1" % old], note="The difference then: %d − %d = %d" % (max(a, b) - y, min(a, b) - y, d)),
                gap(n(d), note="The same as today: %d − %d = %d" % (max(a, b), min(a, b), d))]
    else:
        return P.note(qid, "difference rule: unexpected number of steps")
    put(qid, before, figs, origin="rule")


for _qid, _q in sorted(P.qs.items()):
    _m = PAIR.match(_q["questionText"])
    if _m:
        _a, _b = int(_m.group(2)), int(_m.group(4))
        if _m.group(5):
            diff_before(_qid, _q, _m.group(1), _a, _m.group(3), _b, int(_m.group(5)))
        else:
            sum_after(_qid, _q, _m.group(1), _a, _m.group(3), _b, int(_m.group(6)))


# ── Drawn one by one ─────────────────────────────────────────────────────────

put("G4A_AGES_001", bm(B("Asha", V(9, post=" now"), V(6, post=" more", tone="c"), brace="?"), note="Asha's age after 6 years"),
    {1: bm(B("Asha", V(9, post=" now"), V(6, post=" more", tone="c"), brace="15"), note="9 + 6 = 15")})

put("G4A_AGES_002", bm(B("Meera", V(10)), B("Father", V(10, tone="a"), Uq(28), brace="38"), note="How many years older is her father?"),
    {0: bm(B("Meera", V(10)), B("Father", V(10, tone="a"), Uq(28), brace="38"), hl=["b1s1"], note="The extra piece is how much older he is"),
     1: bm(B("Meera", V(10)), B("Father", V(10, tone="a"), V(28, tone="c"), brace="38"), hl=["b1s1"], note="38 − 10 = 28")})

put("G4A_AGES_003", bm(B("Tina", V(8)), B("Mother", [V(8)] * 4, brace="?"), note="Her mother is 4 times as old as Tina"),
    {1: bm(B("Tina", V(8)), B("Mother", [V(8)] * 4, brace="32"), hl=["b1"], note="8 × 4 = 32")})

put("G4A_AGES_004", bm(B("Zoya", V(6, post=" then"), S("four years", 4, "c"), brace="? now"), note="Four years have passed since she was 6"),
    {1: bm(B("Zoya", V(6, post=" then"), V(4, post=" years", tone="c"), brace="10 now"), note="6 + 4 = 10")})

put("G4A_AGES_005", nl(2015, 2024, 1, points=[(2015, "born 2015"), (2024, "2024")], ticks="none", note="Each step is one birthday"),
    {1: nl(2015, 2024, 1, points=[(2015, "born 2015"), (2024, "2024")], hops=[(2015, 2024, "9 years")], ticks="none", note="2024 − 2015 = 9")})

put("G4A_AGES_006", bm(B("Father", [S(None, 12)] * 3, brace="36"), B("Rohan", Uq(12)), note="Rohan is one-third as old as his father"),
    {1: bm(B("Father", [V(12)] * 3, brace="36"), B("Rohan", V(12)), hl=["b1"], note="36 ÷ 3 = 12")})

put("G4A_AGES_007", bm(B("Sunil", Uq(5)), B("Anil", Uq(5), V(3, tone="c")), note="After 10 years, how much older is Anil than Sunil?"),
    {0: bm(B("Sunil", V(5)), B("Anil", V(5), V(3, tone="c"), brace="8"), note="Suppose Sunil is 5, so Anil is 8"),
     1: bm(B("Sunil", V(5), V(10, tone="b"), brace="15"), B("Anil", V(5, tone="a"), V(10, tone="b"), V(3, tone="c"), brace="18"), note="After 10 years Sunil is 15 and Anil is 18"),
     2: bm(B("Sunil", V(5), V(10, tone="b"), brace="15"), B("Anil", V(5, tone="a"), V(10, tone="b"), V(3, tone="c"), brace="18"), hl=["b1s2"], note="18 − 15 = 3: the gap stays the same")})

put("G4A_AGES_008", bm(B("Ravi", V(12, post=" now"), Uq(8), brace="20"), note="How many more years until Ravi is 20?"),
    {1: bm(B("Ravi", V(12, post=" now"), V(8, tone="c"), brace="20"), hl=["b0s1"], note="20 − 12 = 8")})

_c = lambda t="a": V(7, tone=t)
put("G4A_AGES_009", bm(B("Chirag", _c()), B("Bina", _c(), V(2, tone="b")), B("Amit", _c(), V(2, tone="b"), V(3, tone="c"), brace="?")),
    {0: bm(B("Chirag", _c()), B("Bina", _c(), V(2, tone="b"), brace="9"), B("Amit", _c(), V(2, tone="b"), V(3, tone="c"), brace="?"), hl=["b1"], note="7 + 2 = 9"),
     1: bm(B("Chirag", _c()), B("Bina", _c(), V(2, tone="b"), brace="9"), B("Amit", _c(), V(2, tone="b"), V(3, tone="c"), brace="12"), hl=["b2"], note="9 + 3 = 12")})

put("G4A_AGES_010", bm(B("Farhan", S(None, 8), V(3, tone="c"), brace="11"), B("Rehana", Uq(8)), note="Rehana is 3 years younger. How old was she 2 years ago?"),
    {0: bm(B("Farhan", V(8), V(3, tone="c"), brace="11"), B("Rehana", V(8, tone="a")), hl=["b1"], note="11 − 3 = 8: Rehana's age now"),
     1: bm(B("Farhan", V(8), V(3, tone="c"), brace="11"), B("Rehana", V(6, tone="a"), V(2, tone="b"), brace="8"), hl=["b1s0"], note="8 − 2 = 6")})

put("G4A_AGES_011", bm(B("Diya", V(7), V(7, tone="c")), B("Mother", V(35), V(7, tone="c")), note="After 7 years, how many times as old as Diya is her mother?"),
    {0: bm(B("Diya", V(7), V(7, tone="c"), brace="14"), B("Mother", V(35), V(7, tone="c")), hl=["b0"], note="7 + 7 = 14"),
     1: bm(B("Diya", V(7), V(7, tone="c"), brace="14"), B("Mother", V(35), V(7, tone="c"), brace="42"), hl=["b1"], note="35 + 7 = 42"),
     2: bm(B("Diya", V(14)), B("Mother", [V(14)] * 3, brace="42"), note="42 ÷ 14 = 3")})

put("G4A_AGES_012", bm(B("", V(8, "Anu ", tone="a"), Uq(36, "Mother ?"), brace="44"), note="How old was her mother when Anu was born?"),
    {0: bm(B("", V(8, "Anu ", tone="a"), V(36, "Mother ", tone="b"), brace="44"), hl=["b0s1"], note="44 − 8 = 36"),
     2: bm(B("Mother", S("28 at Anu's birth", 28, "b"), V(8, post=" years", tone="a"), brace="36"), hl=["b0s0"], note="36 − 8 = 28")})

_s = lambda y, **kw: bm(B("Younger", y), B("Older", y, V(4, tone="c"), brace=kw.pop("brace", None)), **kw)
put("G4A_AGES_013", _s(Uq(8), note="Their ages add up to 20 years. One is 4 years older."),
    {0: _s(Uq(8), hl=["b1s1"], note="20 − 4 = 16: two equal pieces are left"),
     1: _s(V(8), note="Half of 16 is 8"),
     2: _s(V(8), brace="12", hl=["b1"], note="8 + 4 = 12")})

put("G4A_AGES_014", bm(B("Son", Uq(12)), B("Father", [Uq(12)] * 3), note="Their ages add up to 48 years"),
    {0: bm(B("Son", Uq(12)), B("Father", [Uq(12)] * 3), note="1 part and 3 parts make 4 equal parts"),
     1: bm(B("Son", V(12)), B("Father", [V(12)] * 3), note="48 ÷ 4 = 12"),
     2: bm(B("Son", V(12)), B("Father", [V(12)] * 3), hl=["b0"], note="The son is 12 years old")})

put("G4A_AGES_015", bm(B("Kiran", V(9, post=" then"), S("three years", 3, "b"), V(4, post=" years", tone="c"), brace="?"), note="From three years ago, to today, to 4 years from now"),
    {0: bm(B("Kiran", V(9, post=" then"), V(3, post=" years", tone="b"), V(4, post=" years", tone="c"), brace="?"), hl=["b0s0", "b0s1"], note="Today: 9 + 3 = 12"),
     1: bm(B("Kiran", V(12, post=" today"), V(4, post=" years", tone="c"), brace="16"), note="12 + 4 = 16")})

_g = lambda t, **kw: bm(B("Geeta", S("age then", 8), t), B("Hari", S("age then", 8), t), **kw)
put("G4A_AGES_016", _g(S("3 years", 3, "c"), note="Now their ages add up to 25. What about 3 years ago?"),
    {0: _g(S("3 years", 3, "c"), hl=["b0s1", "b1s1"], note="Three years ago each was 3 years younger"),
     1: _g(S("3 years", 3, "c"), hl=["b0s1", "b1s1"], note="3 + 3 = 6 years less in all"),
     2: _g(S("3 years", 3, "c"), hl=["b0s0", "b1s0"], note="25 − 6 = 19")})

put("G4A_AGES_017", bm(B("Grandfather", V(72)), B("Father", Uq(36)), B("Jay", Uq(9)), note="Father: half of grandfather. Jay: one-quarter of father."),
    {0: bm(B("Grandfather", V(36), V(36)), B("Father", V(36)), B("Jay", Uq(9)), hl=["b1"], note="72 ÷ 2 = 36"),
     1: bm(B("Grandfather", V(36), V(36)), B("Father", [V(9)] * 4, brace="36"), B("Jay", V(9)), hl=["b2"], note="36 ÷ 4 = 9")})

put("G4A_AGES_018", bm(B("Varun", V(9)), B("Father", V(9), V(27, tone="c")), note="How old is his father when Varun is 15?"),
    {0: bm(B("Varun", V(9)), B("Father", V(9), V(27, tone="c")), hl=["b1s1"], note="The gap of 27 years never changes"),
     1: bm(B("Varun", V(15)), B("Father", V(15), V(27, tone="c"), brace="42"), hl=["b1"], note="15 + 27 = 42")})

put("G4A_AGES_019", bm(B("Rahul", V(10)), B("Father", V(40)), note="After how many years will the father be 3 times as old?"),
    {0: bm(B("Rahul", V(10), V(5, tone="c"), brace="15"), B("Father", V(40)), hl=["b0s1"], note="Try 5 years: 10 + 5 = 15"),
     1: bm(B("Rahul", V(10), V(5, tone="c"), brace="15"), B("Father", V(40), V(5, tone="c"), brace="45"), hl=["b1s1"], note="40 + 5 = 45"),
     2: bm(B("Rahul", V(15)), B("Father", [V(15)] * 3, brace="45"), note="45 is 3 times 15")})

put("G4A_AGES_020", bm(B("Ali", V(14)), B("Sara", V(8)), note="Earlier, Sara was exactly half Ali's age. How old was Ali then?"),
    {0: bm(B("Ali", V(8, tone="b"), V(6, tone="c"), brace="14"), B("Sara", V(8)), hl=["b0s1"], note="14 − 8 = 6: Ali is always 6 years older"),
     1: bm(B("Ali then", S("Sara's age", 6, "b"), V(6, tone="c")), B("Sara then", V(6)), note="Half his age: Sara's age equals the gap, so she was 6"),
     2: bm(B("Ali then", V(6, tone="b"), V(6, tone="c"), brace="12"), B("Sara then", V(6)), hl=["b0"], note="6 + 6 = 12")})

put("G4A_AGES_021", bm(B("Daughter then", Uq(4)), B("Mother then", [Uq(4)] * 7), note="Five years ago, Mother was 7 times as old. She is 33 now."),
    {0: bm(B("Daughter then", Uq(4)), B("Mother then", [Uq(4)] * 7, brace="28"), hl=["b1"], note="33 − 5 = 28"),
     1: bm(B("Daughter then", V(4)), B("Mother then", [V(4)] * 7, brace="28"), note="28 ÷ 7 = 4"),
     2: bm(B("Daughter now", V(4), V(5, post=" years", tone="c"), brace="9"), note="4 + 5 = 9")})

put("G4A_AGES_022", bm(B("Bhavna", Uq(8)), B("Aman", Uq(8), Uq(8)), note="Four years ago Aman was three times as old as Bhavna"),
    {0: bm(B("Bhavna", V(8)), B("Aman", V(8), V(8), brace="16"), note="Try Bhavna as 8: Aman is 2 × 8 = 16"),
     1: bm(B("Bhavna then", V(4)), B("Aman then", S("16 − 4 = 12", 12)), note="Four years ago: 8 − 4 = 4 and 16 − 4 = 12"),
     2: bm(B("Bhavna then", V(4)), B("Aman then", [V(4)] * 3, brace="12"), note="12 is 3 times 4, so both clues fit")})

put("G4A_AGES_023", bm(B("Grandson", Uq(7)), B("Grandfather", [Uq(7)] * 9), note="Their ages add up to 70 years"),
    {0: bm(B("Grandson", V(7)), B("Grandfather", [V(7)] * 9), note="10 equal parts are 70, so one part is 70 ÷ 10 = 7"),
     1: bm(B("Grandson", V(7)), B("Grandfather", [V(7)] * 9, brace="63"), hl=["b1"], note="9 × 7 = 63"),
     2: bm(B("Grandson", V(7), V(3, tone="c"), brace="10"), B("Grandfather", V(63)), hl=["b0s1"], note="10 − 7 = 3 years from now"),
     3: bm(B("Grandson", V(7), V(3, tone="c"), brace="10"), B("Grandfather", V(63), V(3, tone="c"), brace="66"), hl=["b1"], note="63 + 3 = 66")})

_n = lambda y, **kw: bm(B("2 years ago", y), B("In 6 years", y, V(2, tone="b"), V(6, tone="c"), brace=kw.pop("brace", None)), **kw)
put("G4A_AGES_024", _n(Uq(8), note="In 6 years he will be twice as old as he was 2 years ago"),
    {0: _n(Uq(8), hl=["b1s1", "b1s2"], note="From 2 years ago to 6 years from now: 2 + 6 = 8 years"),
     1: _n(V(8), note="Twice as old: the 8 extra years equal his age 2 years ago"),
     2: bm(B("Now", V(8), V(2, tone="b"), brace="10"), note="8 + 2 = 10"),
     3: _n(V(8), brace="16", hl=["b1"], note="Check: in 6 years he is 16, which is twice 8")})

_two = V(2, tone="c")
put("G4A_AGES_025", bm(B("Youngest", Uq(7)), B("Middle", Uq(7), _two), B("Oldest", Uq(7), _two, _two), note="Born 2 years apart. Their ages add up to 27 years."),
    {0: bm(B("Youngest", Uq(7), _two, brace="9"), B("Middle", Uq(7), _two, brace="9"), B("Oldest", Uq(7), _two, brace="9"), hl=["b0s1"],
           note="Move 2 from the oldest to the youngest: 27 ÷ 3 = 9"),
     1: bm(B("Youngest", V(7)), B("Middle", V(7), _two, brace="9"), B("Oldest", Uq(7), _two, _two), hl=["b0"], note="9 − 2 = 7"),
     2: bm(B("Youngest", V(7)), B("Middle", V(9)), B("Oldest", V(11)), note="Check: 7 + 9 + 11 = 27")})

_H = ["When", "Members", "Average age", "Total age"]
put("G4A_AGES_026", tb([["5 years ago", "4", "19"], ["Today", "5", "20"]], _H[:3], note="A baby was born in between"),
    {0: tb([["5 years ago", "4", "19", "4 × 19"], ["Today", "5", "20", "?"]], _H, hl=["r0"], note="Total age = members × average age"),
     1: tb([["5 years ago", "4", "19", "4 × 19"], ["Today", "5", "20", "?"]], _H, note="The same 4 people today: 4 × 19 + 4 × 5"),
     2: tb([["5 years ago", "4", "19", "4 × 19"], ["Today", "5", "20", "5 × 20"]], _H, hl=["r1"], note="All 5 members today: 5 × 20"),
     3: tb([["5 years ago", "4", "19", "4 × 19"], ["Today", "5", "20", "5 × 20"]], _H, note="The baby is the difference: 4 years old")})

put("G4A_AGES_027", bm(B("Now", S("Father and Mother", 72), V(3, "Son ", tone="c"), brace="75"), note="Five years ago the son was not born yet"),
    {0: bm(B("Now", S("Father and Mother", 72), V(3, "Son ", tone="c"), brace="75"), hl=["b0s1"], note="The son is 3, so 5 years ago he was not born yet"),
     1: [bm(B("Now", V(72, tone="a"), V(3, "Son ", tone="c"), brace="75"), hl=["b0s0"], note="75 − 3 = 72 for the two parents"),
         bm(B("Now", S("75 − 3", 72), V(3, "Son ", tone="c"), brace="75"), hl=["b0s0"], note="Take the son's 3 years away for the two parents")],
     2: [bm(B("5 years ago", V(62), S("5 + 5", 10, "c"), brace="72"), hl=["b0s0"], note="72 − 2 × 5 = 62"),
         bm(B("5 years ago", V(62), S("5 + 5", 10, "c"), brace="75 − 3"), hl=["b0s0"], note="Each parent was 5 years younger: 62")]})

put("G4A_AGES_028", bm(B("Meera", Uq(13)), B("Mother", [Uq(13)] * 3), note="Mother was 26 when Meera was born. Now she is 3 times as old."),
    {0: bm(B("Meera", Uq(13)), B("Mother", [Uq(13)] * 3), hl=["b1s1", "b1s2"], note="Mother is always 26 years older"),
     1: bm(B("Meera", Uq(13)), B("Mother", [Uq(13)] * 3), hl=["b1s1", "b1s2"], note="3 − 1 = 2 parts make the gap of 26"),
     2: bm(B("Meera", V(13)), B("Mother", [V(13)] * 3), note="26 ÷ 2 = 13"),
     3: bm(B("Meera", V(13)), B("Mother", [V(13)] * 3, brace="39"), hl=["b1"], note="3 × 13 = 39")})

_T = [["Anu + Bela", "20"], ["Bela + Charu", "26"], ["Anu + Charu", "24"]]
put("G4A_AGES_029", tb(_T, ["Pair", "Ages together"], note="How old is Charu?"),
    {0: tb(_T, ["Pair", "Ages together"], hl=["r0", "r1", "r2"], note="Add the three totals: each child is counted twice"),
     1: [tb(_T, ["Pair", "Ages together"], note="70 ÷ 2 = 35 for Anu, Bela and Charu together"),
         tb(_T, ["Pair", "Ages together"], note="Half of that is Anu, Bela and Charu together")],
     2: tb(_T, ["Pair", "Ages together"], hl=["r0"], note="35 − 20 = 15 is left for Charu")})

put("G4A_AGES_030", bm(B("Father", V(40)), B("Children", V(4), V(6), V(8)), note="When will the children's ages add up to the father's age?"),
    {0: bm(B("Father", V(40)), B("Children", V(4), V(6), V(8), brace="18"), hl=["b1"], note="4 + 6 + 8 = 18"),
     1: bm(B("Father", V(18, tone="b"), V(22, tone="c"), brace="40"), B("Children", V(4), V(6), V(8), brace="18"), hl=["b0s1"], note="40 − 18 = 22 is the gap"),
     2: bm(B("Father", V(18, tone="b"), V(22, tone="c"), brace="40"), B("Children", V(4), V(6), V(8), brace="18"), hl=["b0s1"], note="Each year the gap closes by 3 − 1 = 2"),
     3: bm(B("Father", V(18, tone="b"), V(22, tone="c"), brace="40"), B("Children", V(4), V(6), V(8), brace="18"), hl=["b0s1"], note="22 ÷ 2 = 11 years"),
     4: bm(B("Father", V(51)), B("Children", V(15), V(17), V(19), brace="51"), note="Check: 15 + 17 + 19 = 51")})

_m = lambda t, **kw: bm(B("", V(28, tone="a"), [t] * 3, brace="64"), **kw)
put("G4A_AGES_031", _m(Uq(12), note="Mother was 28 at the start. Then all three grow older together."),
    {0: _m(Uq(12), hl=["b0s0"], note="At the birth the three ages added up to 28"),
     1: _m(Uq(12), hl=["b0s1", "b0s2", "b0s3"], note="64 − 28 = 36 years added since then"),
     2: _m(V(12, tone="c"), note="36 ÷ 3 = 12 years for each person"),
     3: bm(B("Mother", V(28), V(12, tone="c"), brace="40"), B("Twin", V(12, tone="c")), B("Twin", V(12, tone="c")), note="Check: 40 + 12 + 12 = 64")})

_H = ["Father", "Gap", "Father", "Gap"]
_pairs = [(13, 31), (14, 41), (15, 51), (16, 61), (17, 71), (18, 81), (19, 91)]
_cell = lambda i, gap: [n(_pairs[i][1]), n(_pairs[i][1] - _pairs[i][0]) if gap else "?"] if i < len(_pairs) else ["–", "–"]
_rows = lambda gap: [_cell(i, gap) + _cell(i + 4, gap) for i in range(4)]
put("G4A_AGES_032", None,
    {0: tb(_rows(False), _H, note="The son is 13 to 19. Swap the digits for the father."),
     1: tb(_rows(True), _H, note="Gap = father's age take away the son's age"),
     2: tb([["14", "41", "27"]], ["Son", "Father", "Gap"], hl=["r0"], note="Only 14 and 41 have a gap of 27")})

_e = [(8, "Asha now"), (20, "Bina then")]
put("G4A_AGES_033", nl(8, 20, 1, points=_e, ticks="ends", note="When Asha is as old as Bina is now, Bina will be 20"),
    {0: nl(8, 20, 1, points=_e, ticks="ends", note="Asha grows up to Bina's age while Bina grows up to 20"),
     1: nl(8, 20, 1, points=_e, hops=[(8, 20, "12")], ticks="ends", note="Two equal steps together: 20 − 8 = 12"),
     2: nl(8, 20, 1, points=_e, hops=[(8, 14, "half"), (14, 20, "half")], ticks="ends", note="Each step is half of 12"),
     3: nl(8, 20, 1, points=[(8, "Asha now"), (14, "Bina now"), (20, "Bina then")], hops=[(8, 14, "half"), (14, 20, "half")], ticks="ends", hl=["p1"], note="One step above 8 is 14"),
     4: nl(8, 20, 1, points=[(8, "Asha now"), (14, "Bina now"), (20, "Bina then")], hops=[(8, 14, "6"), (14, 20, "6")], ticks="ends", note="Check: in 6 years Asha is 14 and Bina is 20")})

_H = ["This year", "Last year", "Multiple of 4?"]
put("G4A_AGES_034", None,
    {1: tb([["9", "?", "?"], ["24", "?", "?"], ["39", "?", "?"], ["54", "?", "?"]], _H, note="Multiples of 3 under 60 that end in 9 or 4"),
     2: tb([["9", "8", "yes"], ["24", "23", "no"], ["39", "38", "no"], ["54", "53", "no"]], _H, hl=["r0"], note="Only 8 is a multiple of 4")})

_H = ["When", "Ages add up to"]
put("G4A_AGES_035", tb([["2 years ago", "?"], ["Today", "?"], ["Five years on", "50"]], _H, note="Three children, each more than 4 years old"),
    {0: tb([["2 years ago", "?"], ["Today", "35"], ["Five years on", "50"]], _H, hl=["r1"], note="50 − 3 × 5 = 35"),
     1: tb([["2 years ago", "29"], ["Today", "35"], ["Five years on", "50"]], _H, hl=["r0"], note="35 − 3 × 2 = 29")})

put("G4A_AGES_036", bm(B("Daughter", Uq(8)), B("Mother", [Uq(8)] * 5), note="In 6 years their ages will add up to 60 years"),
    {0: [bm(B("Daughter", Uq(8)), B("Mother", [Uq(8)] * 5), note="Today: 60 − 2 × 6 = 48"),
         bm(B("Daughter", Uq(8)), B("Mother", [Uq(8)] * 5), note="Take 6 years off each of them: 60 − 6 − 6 today")],
     1: bm(B("Daughter", Uq(8)), B("Mother", [Uq(8)] * 5), note="1 + 5 = 6 equal parts"),
     2: [bm(B("Daughter", V(8)), B("Mother", [V(8)] * 5), note="48 ÷ 6 = 8"), bm(B("Daughter", V(8)), B("Mother", [V(8)] * 5), note="Each part is 8 years")],
     3: bm(B("Daughter", V(8), V(6, tone="c"), brace="14"), B("Mother", V(40), V(6, tone="c"), brace="46"), note="Check: 14 + 46 = 60")})

_H = ["Multiply to 84", "Gap"]
_f = [(1, 84), (2, 42), (3, 28), (4, 21), (6, 14), (7, 12)]
put("G4A_AGES_037", None,
    {0: tb([["%d and %d" % p, "?"] for p in _f], _H),
     1: tb([["%d and %d" % p, n(p[1] - p[0])] for p in _f], _H),
     2: tb([["%d and %d" % p, n(p[1] - p[0])] for p in _f], _H, hl=["r5"], note="Only 7 and 12 are 5 apart"),
     3: tb([["%d and %d" % p, n(p[1] - p[0])] for p in _f], _H, hl=["r5"], note="7 + 12 = 19")})

put("G4A_AGES_038", None,
    {0: bm(B("Kabir", Uq(6)), B("Grandfather", [Uq(6)] * 12), note="A year has 12 months, so Grandfather is 12 times as old"),
     1: bm(B("Kabir", Uq(6)), B("Grandfather", [Uq(6)] * 12), note="1 part and 12 parts add up to 78 years"),
     2: bm(B("Kabir", V(6)), B("Grandfather", [V(6)] * 12), note="Each part is 6 years"),
     3: bm(B("Kabir", V(6)), B("Grandfather", [V(6)] * 12, brace="72"), note="Check: 6 + 72 = 78")})

_H = ["Now (2 : 5)", "6 years ago"]
_now = [(8, 20), (10, 25), (12, 30), (14, 35), (16, 40)]
put("G4A_AGES_039", bm(B("Tara", [S(None, 6)] * 2), B("Uncle", [S(None, 6)] * 5), note="Now 2 : 5. Six years ago their ages were in the ratio 1 : 4."),
    {0: tb([["%d and %d" % p, "?"] for p in _now], _H),
     1: tb([["%d and %d" % p, "%d and %d" % (p[0] - 6, p[1] - 6)] for p in _now], _H),
     2: tb([["%d and %d" % p, "%d and %d" % (p[0] - 6, p[1] - 6)] for p in _now], _H, hl=["r2"], note="4 × 6 = 24, so 6 and 24 are in the ratio 1 : 4"),
     3: tb([["%d and %d" % p, "%d and %d" % (p[0] - 6, p[1] - 6)] for p in _now], _H, hl=["r2"], note="That pair is 12 and 30 now")})

# Past papers
_b = [(2006, "2006"), (2013, "2013")]
put("PYQ_2016_Q10", nl(2006, 2022, 1, points=_b, ticks="none", note="Sarika is born in 2006 and Surya in 2013"),
    {0: nl(2006, 2022, 1, points=_b, hops=[(2006, 2013, "2013 − 2006")], ticks="none", note="Sarika is older by 2013 − 2006 years"),
     1: bm(B("Surya", V(7)), B("Sarika", V(7, tone="a"), V(7, tone="c"), brace="14"), note="Twice as old: the gap of 7 equals Surya's age"),
     2: nl(2006, 2022, 1, points=_b + [(2020, "2020")], hops=[(2013, 2020, "7 years")], ticks="none", hl=["p2"], note="2013 + 7 = 2020"),
     3: nl(2006, 2022, 1, points=_b + [(2020, "2020")], hops=[(2006, 2020, "14 years"), (2013, 2020, "7 years")], ticks="none", note="In 2020 Sarika is 14 and Surya is 7")})

_hw = lambda now, son, **kw: bm(B("6 years ago", S("Husband + wife 48", 48)), B("Now", now, son, brace="63"), **kw)
put("PYQ_2019_Q05", _hw(S("Husband + wife ?", 60, "unknown"), Uq(3, "Son ?"), note="Find the son's age 6 years from now"),
    {0: _hw(V(60, "Husband + wife "), Uq(3, "Son ?"), hl=["b1s0"], note="Each is 6 years older: 48 + 6 + 6 = 60"),
     1: _hw(V(60, "Husband + wife "), Uq(3, "Son ?"), hl=["b1s1"], note="Take the parents' 60 away from 63 for the son's age now"),
     2: bm(B("Son", S("now", 3), V(6, post=" years", tone="c"), brace="9"), note="6 years from now he will be 9")})

put("EXT_G4_FP_2021_019", _hw(S("Husband + wife ?", 60, "unknown"), Uq(3, "Son ?"), note="Find the son's age 6 years from now"),
    {0: _hw(S("48 + 12", 60), Uq(3, "Son ?"), hl=["b1s0"], note="Each is 6 years older now, so add 12"),
     1: _hw(S("48 + 12", 60), Uq(3, "Son ?"), hl=["b1s1"], note="What is left of 63 is the son's age now"),
     2: bm(B("Son", S("now", 3), V(6, post=" years", tone="c"), brace="?"), note="Add 6 years to his age now"),
     3: bm(B("Son", S("now", 3), V(6, post=" years", tone="c"), brace="9"), note="The son will be 9 years old")})

_H = ["When", "Sum of ages"]
put("EXT_G4_FP_2021_010", tb([["5 years ago", "5x"], ["Now", "?"], ["5 years from now", "?"]], _H, note="A mother and her daughter"),
    {0: tb([["5 years ago", "5x"], ["Now", "?"], ["5 years from now", "?"]], _H, note="From 5 years ago to 5 years from now is 5 + 5 = 10 years"),
     1: tb([["5 years ago", "5x"], ["Now", "?"], ["5 years from now", "?"]], _H, hl=["r2"], note="Two people each grow 10 years older: 2 × 10 = 20"),
     2: tb([["5 years ago", "5x"], ["Now", "5x + 10"], ["5 years from now", "5x + 20"]], _H, hl=["r2"])})

_v = lambda y, **kw: bm(B("Vipul", y), B("Nirav", y, V(2, tone="c")), **kw)
put("EXT_G4_FP_2022_035", _v(Uq(21), note="3 years ago their ages added up to 38. Vipul is 2 years younger."),
    {0: [_v(Uq(21), note="Now: 38 + 2 × 3 = 44"), _v(Uq(21), note="Both are 3 years older now, so add 6 to 38")],
     1: [_v(V(21), hl=["b1s1"], note="(44 − 2) ÷ 2 = 21"), _v(Uq(21), hl=["b1s1"], note="Take away the extra 2 years, then share equally")],
     2: bm(B("Vipul", V(21, post=" now"), V(2, post=" years", tone="c"), brace="23"), note="21 + 2 = 23")})

P.save()
P.review()
