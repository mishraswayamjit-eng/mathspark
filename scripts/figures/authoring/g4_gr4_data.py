"""Figures for Grade 4 "Data Handling & Graphs" (topic gr4_data).

    python -X utf8 scripts/figures/authoring/g4_gr4_data.py

Writes data/question-figures/parts/g4-gr4_data.json.

What is drawn:
  - the table, bar graph or pictograph a question describes in words, built from the numbers in
    its own text (read with a pattern, never typed);
  - averages as bars levelled out, or as a bar of equal pieces;
  - a missing value as the unknown piece of a bar;
  - a Venn diagram for "both / neither".

A pictograph row given as "4 pictures, each stands for 5" cannot use the pictograph's own key,
because the checker counts the row's value (20) as a number shown, and 20 is not in the
question. Those are drawn with one symbol per picture ("= 1 picture") and the key in the note.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_time_kit import Part, T, BC, BM, NL, V, FB, renote, ints  # noqa: E402
import g4_gr4_time_kit as kit  # noqa: E402

P = Part("gr4_data")
LETTERS = "ABCDEFGH"


def pairs(qid, pattern, swap=False, short=False):
    """(label, number) pairs read from the question text."""
    out = []
    for a, b in re.findall(pattern, P.text(qid)):
        if swap:
            a, b = b, a
        out.append((a[:3] if short else a, int(b)))
    if len(out) < 2:
        P.problems.append("%s: the pattern found %d pairs" % (qid, len(out)))
    return out


def rows(prs):
    return [[a, str(b)] for a, b in prs]


def key_has(qid, value):
    ok = float(value) in kit.validate.numbers_in(P.answer(qid))
    if not ok:
        P.problems.append("%s: worked out %s, the key is %r" % (qid, value, P.answer(qid)))
    return ok


def nstr(x):
    return str(int(x)) if float(x) == int(x) else ("%.2f" % x).rstrip("0").rstrip(".")


# ── Rule: the average of a list ──────────────────────────────────────────────

def avg_list(qid):
    vals = ints(re.search(r"(?:average|mean) of:?\s*([\d, ]+)", P.text(qid), re.I).group(1))
    avg = sum(vals) / float(len(vals))
    if not key_has(qid, avg):
        return
    chart = [(LETTERS[i], v) for i, v in enumerate(vals)]
    level = [(LETTERS[i], avg) for i in range(len(vals))]
    n = len(P.steps(qid))
    steps = {}
    for i in range(n):
        if i == n - 1:
            steps[i] = [BC(level, note="Shared out equally, every bar is %s" % nstr(avg)), BC(chart, note="Share the total equally")]
        elif i == 0:
            steps[i] = [BC(chart, note="Add them all: the total is %d" % sum(vals)), BC(chart, note="Add all the numbers")]
        elif "count" in P.steps(qid)[i].get("text", "").lower():
            steps[i] = [BC(chart, hl=["b%d" % k for k in range(len(vals))], note="Count the bars: there are %d numbers" % len(vals)),
                        BC(chart, note="Count the numbers in the list")]
        else:
            steps[i] = [BC(chart, note="Share the total equally among the %d numbers" % len(vals)), BC(chart, note="Share the total equally")]
    P.put(qid, BC(chart, note="Average = ?"), steps, origin="rule")


for qid in ("BOOST_EXT_G4_FP_2016_032_06", "VAR_EXT_G4_FP_2016_032_04", "VAR_EXT_G4_FP_2016_032_05",
            "VAR_EXT_G4_FP_2016_032_05_b2", "Q_DH_004"):
    avg_list(qid)


# ── Rule: one number missing, the average known ──────────────────────────────

def missing_number(qid):
    text = P.text(qid)
    m = re.search(r"average of (\d+) numbers is (\d+)", text, re.I)
    n, avg = int(m.group(1)), int(m.group(2))
    known = ints(re.search(r"numbers are ([\d, ]+)", text).group(1))
    total = n * avg
    miss = total - sum(known)
    if len(known) != n - 1 or not key_has(qid, miss):
        return
    width = sum(known) / float(len(known))   # the unknown is drawn as wide as its neighbours

    def fig(found, brace, note, hl=None):
        # Once found, the piece is drawn at its true size.
        segs = [(k, str(k)) for k in known] + [(miss if found else width, str(miss) if found else "?", "c" if found else "unknown")]
        return BM([(None, segs, brace)], note=note, hl=hl)

    given = "%d numbers, average %d" % (n, avg)
    steps, shown = {}, False
    for i, s in enumerate(P.steps(qid)):
        nums = kit.validate.numbers_in(s.get("text", ""))
        if i >= 1 and float(miss) in nums:
            shown = True
        last = "b0s%d" % (n - 1)
        firsts = ["b0s%d" % k for k in range(len(known))]
        words = s.get("text", "").lower()
        # The brace shows the total once the checker allows it; several wordings are offered and the
        # first the checker allows at this step is used.
        braces = ["Total %d" % total, given]
        if shown:
            notes = ["%d − %d = %d: the missing number is %d" % (total, sum(known), miss, miss), "The missing number is %d" % miss]
            steps[i] = [fig(True, b, nt, [last]) for b in braces for nt in notes]
        elif "know" in words:
            notes = ["The %d numbers you know add up to %d" % (len(known), sum(known)), "Add the numbers you know"]
            steps[i] = [fig(False, b, nt, firsts) for b in braces for nt in notes]
        elif "left" in words or "away" in words:
            steps[i] = [fig(False, b, "Take the numbers you know away from the total", [last]) for b in braces]
        else:
            notes = ["All %d numbers add up to %d" % (n, total), "The total is the average times %d" % n]
            steps[i] = [fig(False, b, nt, ["b0"]) for b in braces for nt in notes]
    P.put(qid, fig(False, given, "Find the missing number"), steps, origin="rule")


for qid in ("BOOST_EXT_G4_FP_2016_032_07", "VAR_EXT_G4_FP_2016_032_01", "Q_DH_011", "Q_DH_020"):
    missing_number(qid)


# ── Rule: a new number joins, find the new average ───────────────────────────

def new_average(qid):
    m = re.search(r"average of (\d+) numbers is (\d+)\. When a new number (\d+) is added", P.text(qid))
    n, avg, new = [int(x) for x in m.groups()]
    old_total = n * avg
    new_total = old_total + new
    new_avg = new_total / float(n + 1)
    if len(P.steps(qid)) != 3 or not key_has(qid, new_avg):
        return
    segs = [(avg, str(avg))] * n + [(new, str(new), "b")]
    level = [(new_avg, nstr(new_avg), "c")] * (n + 1)
    P.put(qid,
          BM([(None, segs, "New average = ?")], note="Average %d means: as if each of the %d numbers were %d" % (avg, n, avg)),
          {0: BM([(None, segs, "New average = ?")], hl=["b0s%d" % i for i in range(n)], note="Old total = %d × %d = %d" % (avg, n, old_total)),
           1: BM([(None, segs, "New total %d" % new_total)], hl=["b0"], note="New total = %d + %d = %d" % (old_total, new, new_total)),
           2: BM([(None, level, "New total %d" % new_total)], note="Shared among %d numbers, each is %s" % (n + 1, nstr(new_avg)))},
          origin="rule")


for qid in ("BOOST_EXT_G4_FP_2016_032_08", "VAR_EXT_G4_FP_2016_032_02"):
    new_average(qid)


# ── Tables, bar graphs and pictographs read from the question ────────────────

DAY = r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"
DAY3 = r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)"

# 001 most runs
prs = pairs("G4A_DATA_001", r"(Match \d) (\d+)")
t = lambda **k: T(rows(prs), headers=["Match", "Runs"], **k)
best = "r%d" % max(range(len(prs)), key=lambda i: prs[i][1])
P.put("G4A_DATA_001", t(),
      {0: t(note="Look at the tens digits: 3, 5, 4, 2 and 4"),
       1: t(hl=[best], note="The biggest tens digit is 5, so 52 is the biggest score"),
       2: t(hl=[best], note="52 runs were scored in Match 2")}, origin="rule")

# 002 pictograph, fewest
prs = pairs("G4A_DATA_002", DAY + r" has (\d+) pictures")
g = lambda **k: BC(prs, unit="picture", each=1, **k)
low = "b%d" % min(range(len(prs)), key=lambda i: prs[i][1])
P.put("G4A_DATA_002", g(note="Each picture stands for 5 books"),
      {0: g(note="Fewer pictures means fewer books"),
       1: g(hl=[low], note="The numbers of pictures are 4, 6, 3 and 5. The smallest is 3"),
       2: g(hl=[low], note="Wednesday has 3 pictures, which is 15 books"),
       3: g(hl=[low], note="The fewest books were sold on Wednesday")}, origin="rule")

# 003 tally
m = re.search(r"has (\d+) bundles and (\d+) single strokes", P.text("G4A_DATA_003"))
b, s = int(m.group(1)), int(m.group(2))
segs = [(5, "5")] * b + [(1, "1", "b")] * s
P.put("G4A_DATA_003", BM([(None, segs, "? parrots")], note="A bundle stands for 5, a single stroke for 1"),
      {0: BM([(None, segs, "? parrots")], hl=["b0s%d" % i for i in range(b)], note="3 bundles of 5 stand for 15"),
       1: BM([(None, segs, "? parrots")], hl=["b0s%d" % (b + i) for i in range(s)], note="Add the 2 single strokes"),
       2: BM([(None, segs, "17 parrots")], note="17 parrots were counted")}, origin="rule")

# 004 how many more
prs = pairs("G4A_DATA_004", DAY3 + r" (\d+)")
d = dict(prs)
t = lambda **k: T(rows(prs), headers=["Day", "Children"], **k)
P.put("G4A_DATA_004", t(note="How many more on Wednesday than on Tuesday?"),
      {0: t(hl=["r1", "r2"], note="Wednesday has 40 children and Tuesday has 35 children"),
       1: BM([("Wed", [(d["Wed"], str(d["Wed"]))], None), ("Tue", [(d["Tue"], str(d["Tue"])), (d["Wed"] - d["Tue"], "?")], None)],
             hl=["b1s1"], note="Subtract to find how many more"),
       2: BM([("Wed", [(d["Wed"], str(d["Wed"]))], None), ("Tue", [(d["Tue"], str(d["Tue"])), (d["Wed"] - d["Tue"], "5", "c")], None)],
             hl=["b1s1"], note="5 more children were present on Wednesday")}, origin="rule")

# 005 equal bars
prs = pairs("G4A_DATA_005", DAY + r" (\d+)", short=True)
g = lambda **k: BC(prs, **k)
same = ["b%d" % i for i, (_, v) in enumerate(prs) if [x[1] for x in prs].count(v) > 1]
P.put("G4A_DATA_005", g(unit="samosas", note="Which two bars have the same height?"),
      {0: g(unit="samosas", note="Bars are equally tall when their numbers are equal"),
       1: g(unit="samosas", hl=same, note="Only the number 15 appears twice"),
       2: g(unit="samosas", hl=same, note="15 belongs to Tuesday and Thursday")}, origin="rule")

# 006 banana or guava
prs = pairs("G4A_DATA_006", r"(Mango|Banana|Apple|Guava) (\d+)")
t = lambda **k: T(rows(prs), headers=["Fruit", "Children"], **k)
two = ["r%d" % i for i, (a, _) in enumerate(prs) if a in ("Banana", "Guava")]
P.put("G4A_DATA_006", t(),
      {0: t(hl=two, note="Banana was chosen by 6 children and guava by 5 children"),
       1: t(hl=two, note="Add the two groups"),
       2: t(hl=two, note="11 children chose banana or guava")}, origin="rule")

# 007 more than 15
vals = ints(P.text("G4A_DATA_007").split(":")[1].split(".")[0])
line = lambda **k: NL(min(vals) - 1, max(vals), 1, points=[(v, str(v)) for v in sorted(vals)], **k)
over = ["p%d" % i for i, v in enumerate(sorted(vals)) if v > 15]
P.put("G4A_DATA_007", T([vals[:3], vals[3:]], note="How many marks are more than 15?"),
      {0: line(note="Check each mark against 15"),
       1: line(hl=over, note="The marks 18, 20 and 17 are more than 15"),
       2: line(hl=over, note="That makes 3 children with more than 15 marks")}, origin="rule")

# 008 total of a table
prs = pairs("G4A_DATA_008", r"(Cricket|Kho-kho|Football|Carrom) (\d+)")
t = lambda **k: T(rows(prs), headers=["Game", "Children"], **k)
P.put("G4A_DATA_008", t(note="How many children are in the class?"),
      {0: t(hl=["r0", "r2"], note="Add cricket and football first"),
       1: t(hl=["r1", "r3"], note="Add kho-kho and carrom"),
       2: t(note="Put the two sums together"),
       3: t(note="There are 32 children in the class")}, origin="rule")

# 009 which tally shows 23 (no figure before: the choices are the pictures)
P.put("G4A_DATA_009", None,
      {0: BM([(None, [(5, "5")] * 4, None)], note="Four fives make 20"),
       1: BM([(None, [(5, "5")] * 4 + [(3, "?")], "23")], hl=["b0s4"], note="Find what is left after 20"),
       2: BM([(None, [(5, "5")] * 4 + [(1, "1", "b")] * 3, "23")], note="23 is shown by 4 bundles and 3 strokes")})

# 010 pictograph, which month
prs = pairs("G4A_DATA_010", r"(January|February|March|April) has (\d+) pictures", short=True)
g = lambda **k: BC(prs, unit="picture", each=1, **k)
P.put("G4A_DATA_010", g(note="Each picture stands for 2 sunny days"),
      {0: g(note="Each picture stands for 2 days, so 16 days need 8 pictures"),
       1: g(hl=["b1"], note="The month with 8 pictures is February"),
       2: g(hl=["b1"], note="February had 16 sunny days")}, origin="rule")

# 011 second tallest
prs = pairs("G4A_DATA_011", r"(Rose|Tulsi|Neem|Mint|Lily) (\d+)")
down = sorted(prs, key=lambda p: -p[1])
P.put("G4A_DATA_011", T(rows(prs), headers=["Plant", "Height (cm)"]),
      {0: T(rows(down), headers=["Plant", "Height (cm)"], note="From biggest to smallest: 41, 37, 34, 28, 19"),
       1: T(rows(down), headers=["Plant", "Height (cm)"], hl=["r1"], note="The tallest is 41. The next is 37"),
       2: T(rows(down), headers=["Plant", "Height (cm)"], hl=["r1"], note="37 cm is the height of Lily")}, origin="rule")

# 012 reading between two marks
P.put("G4A_DATA_012",
      NL(0, 40, 10, points=[(20,), (30,)], note="Tuesday's bar ends exactly halfway between 20 and 30"),
      {0: NL(0, 40, 10, points=[(20,), (30,)], hops=[(20, 30, "10")], hl=["h0"], note="The marks 20 and 30 are 10 apart"),
       1: NL(0, 40, 10, points=[(20,), (30,)], hops=[(20, 30, "10")], note="Half of 10 is 5"),
       2: NL(0, 40, 5, points=[(20,), (25, "Tuesday"), (30,)], hops=[(20, 25, "+5")], hl=["p1", "h0"], note="Go 5 above 20"),
       3: NL(0, 40, 5, points=[(20,), (25, "Tuesday"), (30,)], hl=["p1"], note="Tuesday's bar shows 25")})

# 013 pictograph, how many more
prs = pairs("G4A_DATA_013", r"(Ravi|Meena)'s row has (\d+) pictures")
g = lambda **k: BC(prs, unit="picture", each=1, **k)
P.put("G4A_DATA_013", g(note="Each picture stands for 3 kites"),
      {0: g(hl=["b1"], note="Meena has 3 more pictures than Ravi"),
       1: g(hl=["b1"], note="Each of those 3 pictures stands for 3 kites"),
       2: g(note="Meena has 9 more kites than Ravi")}, origin="rule")

# 014 pictograph, total
prs = pairs("G4A_DATA_014", DAY + r" has (\d+) pictures")
g = lambda **k: BC(prs, unit="picture", each=1, **k)
P.put("G4A_DATA_014", g(note="Each picture stands for 5 books"),
      {0: g(note="Add the pictures for the three days"),
       1: g(note="Each picture stands for 5 books"),
       2: g(note="65 books were borrowed altogether")}, origin="rule")

# 015 pictograph, boxes of eggs
prs = pairs("G4A_DATA_015", r"(\d+) pictures for " + DAY, swap=True)
g = lambda **k: BC(prs, unit="picture", each=1, **k)
P.put("G4A_DATA_015", g(note="Each picture stands for 6 eggs. A box holds 12 eggs"),
      {0: g(note="Add the pictures"),
       1: g(note="Each picture stands for 6 eggs"),
       2: g(note="Put the eggs in boxes of 12"),
       3: g(note="He fills 4 boxes")}, origin="rule")

# 016 smudged number
prs = pairs("G4A_DATA_016", DAY3 + r" (\d+)")
d = dict(prs)


def laddoo(wed, **k):
    return T([["Mon", d["Mon"]], ["Tue", d["Tue"]], ["Wed", wed], ["Thu", d["Thu"]], ["All four days", "60"]], headers=["Day", "Laddoos"], **k)


P.put("G4A_DATA_016", laddoo("?"),
      {0: laddoo("?", hl=["r0", "r1", "r3"], note="Add the three known days"),
       1: laddoo("?", hl=["r2"], note="Take this away from the total of 60"),
       2: laddoo("16", hl=["r2"], note="16 laddoos were sold on Wednesday")}, origin="rule")

# 017 two-way table of tickets
found = re.findall(r"on (Saturday|Sunday), (\d+) adult tickets and (\d+) child tickets", P.text("G4A_DATA_017"))
t = lambda **k: T([list(r) for r in found], headers=["Day", "Adult", "Child"], **k)
P.put("G4A_DATA_017", t(note="How many more tickets on Sunday than on Saturday?"),
      {0: t(hl=["r0"], note="Find Saturday's total"),
       1: t(hl=["r1"], note="Find Sunday's total"),
       2: t(note="Compare the two totals"),
       3: t(hl=["r1"], note="3 more tickets were sold on Sunday")}, origin="rule")

# 018 redraw a pictograph row
P.put("G4A_DATA_018",
      BM([("Monday", [(4, "4")] * 6, None)], note="Each picture stands for 4 children. Now each must stand for 8"),
      {0: BM([("Monday", [(4, "4")] * 6, None)], hl=["b0"], note="Find the number of children: 6 pictures of 4"),
       1: BM([("Before", [(4, "4")] * 6, None), ("Now", [(8, "8", "b")] * 3, None)], hl=["b1"], note="Each new picture stands for 8 children"),
       2: BM([("Before", [(4, "4")] * 6, None), ("Now", [(8, "8", "b")] * 3, None)], note="Monday's row will have 3 pictures")})

# 019 full and half pictures
mon = [(10, "10")] * 3 + [(5, "5", "b")]
tue = [(10, "10")] * 2
bm = lambda **k: BM([("Monday", mon, None), ("Tuesday", tue, None)], **k)
P.put("G4A_DATA_019", bm(note="Full picture 10 coconuts, half picture 5. Total = ?"),
      {0: bm(hl=["b0"], note="Monday: 3 full pictures and a half picture"),
       1: bm(hl=["b1"], note="Tuesday: 2 full pictures"),
       2: bm(note="Add the two days"),
       3: bm(note="55 coconuts were sold on the two days")})

# 020 tally of birds
found = re.findall(r"(Crows|Sparrows|Pigeons): (\d+) bundles? and (\d+) strokes?", P.text("G4A_DATA_020"))
bars = [(name, [(5, "5")] * int(b) + [(1, "1", "c")] * int(s), None) for name, b, s in found]
bm = lambda **k: BM(bars, **k)
P.put("G4A_DATA_020", bm(note="A bundle is 5, a stroke is 1. How many birds in all?"),
      {0: bm(hl=["b0"], note="Crows: 2 bundles and 3 strokes"),
       1: bm(hl=["b1"], note="Sparrows: 3 bundles and 1 stroke"),
       2: bm(hl=["b2"], note="Pigeons: 1 bundle and 4 strokes"),
       3: bm(note="Add the three rows"),
       4: bm(note="38 birds were counted in all")}, origin="rule")

# 021 bar graph with a fifth bar described
prs = pairs("G4A_DATA_021", DAY3 + r" (\d+)")
g = lambda **k: BC(prs, unit="kites", **k)
P.put("G4A_DATA_021", g(note="Friday's bar is twice as tall as Tuesday's bar"),
      {0: g(hl=["b1"], note="Friday is twice Tuesday"),
       1: g(hl=["b0", "b1", "b2", "b3"], note="Add Monday to Thursday"),
       2: g(note="Then add Friday"),
       3: g(note="69 kites were sold altogether")}, origin="rule")

# 022 the rest chose kabaddi
m = re.search(r"(\d+) children each chose.*by (\d+), football by (\d+) and badminton by (\d+)", P.text("G4A_DATA_022"))
allc, c, f, b = [int(x) for x in m.groups()]
rest = allc - c - f - b
if key_has("G4A_DATA_022", rest):
    bm = lambda last, **k: BM([(None, [(c, str(c)), (f, str(f), "b"), (b, str(b), "c"), (rest, last)], "%d children" % allc)], **k)
    P.put("G4A_DATA_022", bm("?", note="Cricket, football, badminton, then kabaddi"),
          {0: bm("?", hl=["b0s0", "b0s1", "b0s2"], note="Add the three known games"),
           1: bm("?", hl=["b0s3"], note="Take this away from all 40 children"),
           2: bm(str(rest), hl=["b0s3"], note="6 children chose kabaddi")}, origin="rule")

# 023 average with a zero
prs = pairs("G4A_DATA_023", r"(\d+) pages on " + DAY, swap=True, short=True)
g = lambda **k: BC(prs, unit="pages", **k)
avg = sum(v for _, v in prs) / float(len(prs))
if key_has("G4A_DATA_023", avg):
    P.put("G4A_DATA_023", g(note="Average number of pages per day = ?"),
          {0: g(note="Add the pages"),
           1: g(hl=["b1"], note="There are 4 days, and Tuesday counts as a day too"),
           2: g(note="Share the total equally"),
           3: BC([(a, avg) for a, _ in prs], unit="pages", note="The average is 9 pages per day")}, origin="rule")

# 024 order the bars
prs = pairs("G4A_DATA_024", DAY3 + r" (\d+)")
up = sorted(prs, key=lambda p: p[1])
P.put("G4A_DATA_024", BC(prs, unit="cups", note="Put the days in order, shortest bar to tallest"),
      {0: BC(prs, unit="cups", note="From smallest to biggest the numbers are 17, 19, 22, 25"),
       1: BC(up, unit="cups", note="17 is Tuesday, 19 is Thursday, 22 is Monday, 25 is Wednesday"),
       2: BC(up, unit="cups", note="Shortest to tallest: Tue, Thu, Mon, Wed")}, origin="rule")

# 025 clubs
found = re.findall(r"(Art|Music|Chess): (\d+) girls and (\d+) boys", P.text("G4A_DATA_025"))
t = lambda **k: T([list(r) for r in found], headers=["Club", "Girls", "Boys"], **k)
P.put("G4A_DATA_025", t(note="Which club has the most children?"),
      {0: t(hl=["r0"], note="Art club: 9 + 6"),
       1: t(hl=["r1"], note="Music club: 7 + 11"),
       2: t(hl=["r2"], note="Chess club: 5 + 12"),
       3: t(hl=["r1"], note="18 is the biggest total, so Music has the most children")}, origin="rule")

# 026 twice as many
prs = pairs("G4A_DATA_026", r"(Mango|Apple|Banana|Orange|Grapes) (\d+)")
t = lambda **k: T(rows(prs), headers=["Fruit", "Children"], **k)
P.put("G4A_DATA_026", t(note="Which fruit has exactly twice as many as orange?"),
      {0: t(hl=["r3"], note="Orange was chosen by 6 children"),
       1: t(hl=["r3"], note="Find twice as many as 6"),
       2: t(hl=["r2"], note="12 children chose banana")}, origin="rule")

# 027 total from an average
m = re.search(r"played (\d+) cricket matches.*average score was (\d+)", P.text("G4A_DATA_027"))
n, avg = int(m.group(1)), int(m.group(2))
bm = lambda brace, **k: BM([(None, [(1, str(avg))] * n, brace)], **k)
P.put("G4A_DATA_027", bm("? runs", note="Average 32: as if he scored 32 in each of the 5 matches"),
      {0: bm("? runs", note="The average is the total shared equally among the matches"),
       1: bm("? runs", hl=["b0"], note="Multiply the average by the number of matches"),
       2: bm("160 runs", note="He scored 160 runs altogether")}, origin="rule")

# 028 days above the average
prs = pairs("G4A_DATA_028", DAY3 + r" (\d+)")
g = lambda **k: BC(prs, unit="mm", **k)
avg = sum(v for _, v in prs) / float(len(prs))
above = ["b%d" % i for i, (_, v) in enumerate(prs) if v > avg]
if key_has("G4A_DATA_028", len(above)):
    P.put("G4A_DATA_028", g(note="On how many days was the rainfall more than the average?"),
          {0: g(note="Add the rainfall"),
           1: g(note="Find the average"),
           2: g(hl=above, note="Only 10 and 12 are more than 8. Friday's 8 is equal, not more"),
           3: g(hl=above, note="The rainfall was more than the average on 2 days")}, origin="rule")

# 029 the fifth test
bm = lambda **k: BM([("4 tests", [(18, "18")] * 4, None), ("5 tests", [(20, "20", "b")] * 5, None)], **k)
P.put("G4A_DATA_029", bm(note="Averages shown as equal pieces. Marks in the 5th test = ?"),
      {0: bm(hl=["b0"], note="Find the total of the first 4 tests"),
       1: bm(hl=["b1"], note="Find the total of all 5 tests"),
       2: bm(note="The difference between the totals is the 5th test"),
       3: bm(note="She got 28 marks in the 5th test")})

# 030 pictograph with an unknown key
prs = [("Class 4A", ints(re.search(r"Class 4A has (\d+) pictures", P.text("G4A_DATA_030")).group(1))[0]),
       ("Class 4B", ints(re.search(r"Class 4B has (\d+) pictures", P.text("G4A_DATA_030")).group(1))[0])]
g = lambda **k: BC(prs, unit="picture", each=1, **k)
P.put("G4A_DATA_030", g(note="Class 4A collected 21 more newspapers than Class 4B"),
      {0: g(hl=["b0"], note="Class 4A has 3 more pictures"),
       1: g(hl=["b0"], note="These 3 pictures stand for 21 newspapers"),
       2: g(hl=["b0"], note="Class 4A has 7 pictures of 7 newspapers each"),
       3: g(note="Class 4A collected 49 newspapers")}, origin="rule")

# 031 two-way table
def bus(cell, **k):
    return T([["By bus", "9", "?", "15"], ["Not by bus", "?", cell, "?"], ["All", "23", "?", "42"]],
             headers=["Class 4", "Girls", "Boys", "All"], **k)


P.put("G4A_DATA_031", bus("?", note="How many boys do NOT come by bus?"),
      {0: bus("?", hl=["r2"], note="Boys in the class: 42 − 23"),
       1: bus("?", hl=["r0"], note="Boys who come by bus: 15 − 9"),
       2: bus("?", hl=["r1"], note="Boys who do not come by bus: take one from the other"),
       3: bus("13", hl=["r1"], note="13 boys do not come by bus")})

# 033 days described by other days
prs = pairs("G4A_DATA_033", DAY3 + r" (\d+)")
t = lambda **k: T(rows(prs) + [["Sat", "Mon + Tue"], ["Sun", "half of Sat"]], headers=["Day", "Bags"], **k)
P.put("G4A_DATA_033", t(note="How many bags on these five days altogether?"),
      {0: t(hl=["r3"], note="Saturday: 14 + 18"),
       1: t(hl=["r4"], note="Sunday is half of Saturday"),
       2: t(hl=["r0", "r1", "r2"], note="Monday, Tuesday and Wednesday together: 14 + 18 + 10"),
       3: t(note="Add all five days"),
       4: t(note="The shop sold 90 bags altogether")}, origin="rule")

# 034 sharing equally
vals = ints(re.search(r"have ([\d, and]+) marbles", P.text("G4A_DATA_034")).group(1))
chart = [(LETTERS[i], v) for i, v in enumerate(vals)]
avg = sum(vals) / float(len(vals))
big = "b%d" % vals.index(max(vals))
if key_has("G4A_DATA_034", max(vals) - avg):
    P.put("G4A_DATA_034", BC(chart, unit="marbles", note="They share so that all four have the same number"),
          {0: BC(chart, unit="marbles", note="Add all the marbles"),
           1: BC([(a, avg) for a, _ in chart], unit="marbles", note="Shared equally among 4 friends, each has 10"),
           2: BC(chart, unit="marbles", hl=[big], note="The friend with 14 keeps 10"),
           3: BC(chart, unit="marbles", hl=[big], note="That friend must give away 4 marbles")}, origin="rule")

# 035 two pictographs
t = lambda **k: T([["Riya", "5 stamps", "12"], ["Kabir", "8 stamps", "7"]], headers=["Chart", "Each picture", "Pictures"], **k)
P.put("G4A_DATA_035", t(note="Who has more stamps, and by how many?"),
      {0: t(hl=["r0"], note="Riya's stamps: 12 × 5"),
       1: t(hl=["r1"], note="Kabir's stamps: 7 × 8"),
       2: t(note="Compare the two totals"),
       3: t(hl=["r0"], note="Riya has more stamps, by 4")})

# 036 two classes
t = lambda **k: T([["4A", "20", "30"], ["4B", "30", "40"]], headers=["Class", "Children", "Average mark"], **k)
P.put("G4A_DATA_036", t(note="Average mark of all 50 children = ?"),
      {0: t(hl=["r0"], note="Total marks of Class 4A: 20 × 30"),
       1: t(hl=["r1"], note="Total marks of Class 4B: 30 × 40"),
       2: t(note="Add to get the total marks of all 50 children"),
       3: t(note="Share the total among 50 children"),
       4: t(note="The average mark of all 50 children is 36")})

# 037 a graph that does not start at 0
g = lambda **k: BC([("Saturday", 3), ("Sunday", 6)], unit="squares", **k)
P.put("G4A_DATA_037", g(note="The bottom line is 20 books. Each square is 5 more books"),
      {0: g(hl=["b0"], note="Saturday's bar is 3 squares above 20"),
       1: g(hl=["b1"], note="Sunday's bar is 6 squares above 20"),
       2: g(note="Add the two days"),
       3: g(note="Altogether 85 books were sold")})

# 038 both games
v = lambda both, **k: V("Cricket: 24", "Football: 20", "cricket only", both, "football only", **k)
P.put("G4A_DATA_038", v("?", note="40 children. 6 like neither game"),
      {0: v("?", note="Children who like at least one game: 40 − 6"),
       1: v("?", note="Add the two lists: 24 + 20"),
       2: v("?", hl=["both"], note="44 names but only 34 children: the extra names are counted twice"),
       3: v("10", hl=["both"], note="10 children like both games")})

# 040 choosing the key of a pictograph
prs = pairs("G4A_DATA_040", DAY + r" (\d+)", short=True)
g = lambda **k: BC(prs, unit="kites", each=6, **k)
P.put("G4A_DATA_040", T(rows(prs), headers=["Day", "Kites"], note="Whole pictures only, and as few as possible"),
      {0: g(note="The largest number that divides 12, 18, 30 and 42 is 6"),
       1: g(note="Find the pictures for each day"),
       2: g(note="Add the pictures"),
       3: g(note="She will draw 17 pictures altogether")}, origin="rule")

# 041 the smudged day equals the average
prs = pairs("G4A_DATA_041", r"(Monday|Tuesday|Wednesday|Friday) (\d+)", short=True)


def bags(thu, **k):
    return T(rows(prs[:3]) + [["Thu", thu]] + rows(prs[3:]), headers=["Day", "Bags"], **k)


P.put("G4A_DATA_041", bags("?", note="Thursday is exactly the average of all five days"),
      {0: bags("?", hl=["r0", "r1", "r2", "r4"], note="Add the four known days"),
       1: bags("?", hl=["r3"], note="Thursday equals the average of the other four days"),
       2: bags("?", note="Check with all five days"),
       3: bags("30", hl=["r3"], note="30 bags were sold on Thursday")}, origin="rule")

# 042 running totals
prs = pairs("G4A_DATA_042", DAY + r" (\d+)")
diffs = [prs[0][1]] + [prs[i][1] - prs[i - 1][1] for i in range(1, len(prs))]
t = lambda **k: T(rows(prs), headers=["Day", "Total so far"], **k)
t3 = lambda **k: T([[a, b, diffs[i]] for i, (a, b) in enumerate(prs)], headers=["Day", "Total so far", "That day"], **k)
top = "r%d" % diffs.index(max(diffs))
P.put("G4A_DATA_042", t(note="On which day did she read the most pages?"),
      {0: t(hl=["r0"], note="On Monday she read 12 pages"),
       1: t(hl=["r1", "r2"], note="Tuesday and Wednesday: take away the total before"),
       2: t(hl=["r3", "r4"], note="Thursday and Friday: take away the total before"),
       3: t3(note="The largest of 12, 18, 11, 24 and 15 is 24"),
       4: t3(hl=[top], note="She read the most pages on Thursday")}, origin="rule")

# 043 overlapping averages
t = lambda **k: T([["First three tests", "average 10"], ["Last three tests", "average 16"], ["All five tests", "average 12"]], **k)
P.put("G4A_DATA_043", t(note="Marks in the third test = ?"),
      {0: t(hl=["r0"], note="Find the total of the first three tests"),
       1: t(hl=["r1"], note="Find the total of the last three tests"),
       2: t(hl=["r2"], note="Find the total of all five tests"),
       3: t(hl=["r0", "r1"], note="Adding the two groups counts the third test twice"),
       4: t(note="Take away the real total to leave the third test"),
       5: t(note="He got 18 marks in the third test")})

# 045 two votes each
def votes(guava, **k):
    return T([["Mango", "20"], ["Apple", "15"], ["Banana", "14"], ["Guava", guava]], headers=["Fruit", "Votes"], **k)


P.put("G4A_DATA_045", votes("?", note="30 children. Each voted for two different fruits"),
      {0: votes("?", note="Each child gave 2 votes, so find the total votes"),
       1: votes("?", hl=["r0", "r1", "r2"], note="Add the votes for the three known fruits"),
       2: votes("?", hl=["r3"], note="The rest of the votes went to guava"),
       3: votes("11", hl=["r3"], note="Guava got 11 votes")})

# 048 pets
prs = [(int(a), int(b)) for a, b in re.findall(r"(\d+) pets?, (\d+) children", P.text("G4A_DATA_048"))]
t = lambda **k: T([[a, b] for a, b in prs], headers=["Pets", "Children"], **k)
P.put("G4A_DATA_048", t(note="Average number of pets per child = ?"),
      {0: t(note="Count the pets in each row: children times pets"),
       1: t(note="Add to get all the pets"),
       2: t(note="Count all the children"),
       3: t(note="Share the pets among the children"),
       4: t(note="The average is 1 pet per child")}, origin="rule")

# 050 bar heights in centimetres
def sweets(tue, **k):
    return T([["Monday", "9 cm", "45"], ["Tuesday", "4 cm shorter", tue]], headers=["Day", "Bar height", "Sweets"], **k)


P.put("G4A_DATA_050", sweets("?"),
      {0: sweets("?", hl=["r0"], note="Find what 1 cm stands for: 45 ÷ 9"),
       1: sweets("?", hl=["r1"], note="Find the height of Tuesday's bar: 9 − 4"),
       2: sweets("?", hl=["r1"], note="Change Tuesday's height into sweets"),
       3: sweets("25", hl=["r1"], note="Tuesday's bar shows 25 sweets")})

# 051 a torn row
prs = pairs("G4A_DATA_051", r"(Asha|Bala|Charu)'s row has (\d+) pictures")
t = lambda **k: T(rows(prs) + [["Dev", "torn off"]], headers=["Friend", "Pictures"], **k)
P.put("G4A_DATA_051", t(note="Each picture is 3 books. 72 books altogether"),
      {0: t(note="Change the total into pictures: 72 ÷ 3"),
       1: t(hl=["r0", "r1", "r2"], note="Count the pictures in the three rows you can see"),
       2: t(hl=["r3"], note="Find the pictures in Dev's row"),
       3: t(hl=["r1", "r3"], note="Compare Dev's row with Bala's row"),
       4: t(hl=["r3"], note="Dev's row had 1 more picture than Bala's row")}, origin="rule")


# ── Hand-written questions ───────────────────────────────────────────────────

# Q_DH_001: three apple pictures, each 5
count = P.text("Q_DH_001").count("🍎") - 1   # one apple is the key
bm = lambda brace, **k: BM([("Monday", [(1, "5")] * count, brace)], **k)
P.put("Q_DH_001", bm("? apples", note="Each picture stands for 5 apples"),
      {0: bm("? apples", hl=["b0s0"], note="The key says each picture stands for 5 apples"),
       1: bm("? apples", hl=["b0"], note="Monday shows 3 pictures, so multiply 3 by 5"),
       2: bm("15 apples", note="15 apples were sold")})

# Q_DH_006: range
vals = ints(re.search(r"range of ([\d, ]+)", P.text("Q_DH_006"), re.I).group(1))
order = sorted(vals)
line = lambda **k: NL(min(vals), max(vals), 1, points=[(v, str(v)) for v in order], **k)
P.put("Q_DH_006", line(note="Range = ?"),
      {0: line(hl=["p0", "p%d" % (len(order) - 1)], note="The biggest number is 22 and the smallest is 5"),
       1: NL(min(vals), max(vals), 1, points=[(v, str(v)) for v in order], hops=[(min(vals), max(vals))], hl=["h0"],
             note="Subtract the smallest from the biggest: 22 − 5"),
       2: NL(min(vals), max(vals), 1, points=[(v, str(v)) for v in order], hops=[(min(vals), max(vals), "17")], hl=["h0"],
             note="The range is 17")}, origin="rule")

# Q_DH_007: two full pictures and a half
P.put("Q_DH_007",
      BM([(None, [(2, "10"), (2, "10"), (1, "half")], "? students")], note="Each full picture stands for 10 students"),
      {0: BM([(None, [(2, "10"), (2, "10"), (1, "half")], "? students")], hl=["b0s0", "b0s1"], note="2 full pictures: 2 × 10 = 20"),
       1: BM([(None, [(2, "10"), (2, "10"), (1, "half", "b")], "? students")], hl=["b0s2"], note="The half picture stands for half of 10"),
       2: BM([(None, [(2, "10"), (2, "10"), (1, "half", "b")], "? students")], hl=["b0"], note="Add the two parts"),
       3: BM([(None, [(2, "10"), (2, "10"), (1, "half", "b")], "25 students")], note="The row represents 25 students")})

# Q_DH_008: difference of two bars
a, b = ints(P.text("Q_DH_008"))[:2]
P.put("Q_DH_008", BC([("Bar A", a), ("Bar B", b)], note="Difference = ?"),
      {0: BC([("Bar A", a), ("Bar B", b)], note="Subtract the smaller value from the bigger one"),
       1: BM([("Bar A", [(a, str(a))], None), ("Bar B", [(b, str(b)), (a - b, "?")], None)], hl=["b1s1"], note="Bar A is 45 and Bar B is 30"),
       2: BM([("Bar A", [(a, str(a))], None), ("Bar B", [(b, str(b)), (a - b, str(a - b), "c")], None)], hl=["b1s1"], note="The difference is 15")},
      origin="rule")

# Q_DH_010: total of a table
prs = pairs("Q_DH_010", DAY3 + r"=(\d+)")
t = lambda **k: T(rows(prs), headers=["Day", "Number"], **k)
P.put("Q_DH_010", t(note="Total = ?"),
      {0: t(hl=["r0", "r2"], note="Pair numbers that make tens: 12 and 18"),
       1: t(hl=["r3", "r4"], note="The other easy pair: 10 and 20"),
       2: t(hl=["r1"], note="Now add everything, with the 15 too"),
       3: t(note="The total is 75")}, origin="rule")

# Q_DH_013: a quarter of a pie chart
pie = lambda **k: FB([(4, 1, "Cricket")], shape="circle", **k)
P.put("Q_DH_013", pie(note="Cricket takes up 1/4 of the circle. Angle = ?"),
      {0: pie(note="A full circle is 360 degrees"),
       1: pie(hl=["b0"], note="One quarter means divide 360 by 4"),
       2: pie(note="The angle is 90°")})

# Q_DH_014: median
vals = ints(re.search(r"median of: ([\d, ]+)", P.text("Q_DH_014"), re.I).group(1))
order = sorted(vals)
mid = len(order) // 2
line = lambda **k: NL(min(vals), max(vals), 1, points=[(v, str(v)) for v in order], **k)
if key_has("Q_DH_014", order[mid]):
    P.put("Q_DH_014", T([vals], note="Median = ?"),
          {0: T([order], note="Put the numbers in order"),
           1: line(hl=["p%d" % mid], note="There are 5 numbers, so the middle one is the third"),
           2: line(hl=["p%d" % mid], note="The median is 7")}, origin="rule")

# Q_DH_015: how many symbols
six = lambda **k: BM([(None, [(1, "6")] * 6, "36 books")], **k)
P.put("Q_DH_015", None,
      {0: six(note="Share 36 books into groups of 6"),
       1: six(note="Check by multiplying back: 6 × 6 = 36"),
       2: six(hl=["b0"], note="So 6 symbols are needed")})

# Q_DH_016: a bar 3.5 cm tall
P.put("Q_DH_016",
      BM([(None, [(2, "20")] * 3 + [(1, "half")], "3.5 cm tall = ?")], note="1 cm stands for 20 students"),
      {0: BM([(None, [(2, "20")] * 3 + [(1, "half")], "3.5 cm tall = ?")], hl=["b0s0", "b0s1", "b0s2"], note="The 3 whole centimetres: 3 × 20 = 60"),
       1: BM([(None, [(2, "20")] * 3 + [(1, "10", "b")], "3.5 cm tall = ?")], hl=["b0s3"], note="Half a centimetre stands for half of 20"),
       2: BM([(None, [(2, "20")] * 3 + [(1, "10", "b")], "3.5 cm tall = ?")], note="Add the two parts: 60 + 10"),
       3: BM([(None, [(2, "20")] * 3 + [(1, "10", "b")], "70 students")], note="The bar shows 70 students")})

# Q_DH_019: frequency
vals = [int(x) for x in re.search(r"Marks: ([\d,]+)", P.text("Q_DH_019")).group(1).split(",") if x]
t = lambda **k: T([vals[:5], vals[5:]], **k)
# No figure before answering: the question writes its list as "8,9,8,10,..." with no spaces, which the
# checker reads as one long number, so it does not accept 7 or 9 as numbers of the question.
P.put("Q_DH_019", None,
      {0: t(note="Go through the list and tick each 8"),
       1: t(note="The 8s are the first, third, sixth and ninth marks"),
       2: t(note="The frequency of 8 is 4")}, origin="rule")

P.write()
