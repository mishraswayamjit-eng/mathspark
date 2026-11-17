"""Sequences and series (gr5_sequences): the terms set out in a row, the unknown as "?"."""
import re
from imported_other_lib import POOL, PROBLEMS, Q, expect, fmt, n, staged, table, wrap, validate

# ── Story patterns (each spec gives the terms as arithmetic on the question's numbers) ──


def series(sid, terms, given, word="Row", labels=None, what=None, unit="", ask="sum", ans=None, note=None, last_given=False):
    """terms: every term, first to last. given: how many of the first terms the question states.
    labels: the column names for the given terms and the last one (default "Row 1" ... "Row n").
    ask: 'term' (the last term) or 'sum' (all of them added)."""
    q = Q(sid)
    count = len(terms)
    want = ans if ans is not None else (terms[-1] if ask == "term" else sum(terms))
    if not expect(q, want, "series"):
        return
    labels = labels or ["%s %d" % (word, k + 1) for k in range(given)] + ["%s %d" % (word, count)]
    cell = lambda v: fmt(v, unit)
    gap = count > given + 1
    last = cell(terms[-1])

    def layout(end, note_, hl=None):
        heads = labels[:given] + (["…"] if gap else []) + [labels[-1]]
        cells = [cell(t) for t in terms[:given]] + (["…"] if gap else []) + [end]
        if len(heads) <= 5:
            return table([cells], headers=heads, note=note_, hl=hl)
        return table([[h, c] for h, c in zip(heads, cells)], headers=[word, what or "Number"], note=note_, hl=hl)

    start = last if last_given else "?"
    default = "The pattern goes on. What goes in the last box?" if ask == "term" else "The pattern goes on. How many in all of them together?"
    before = layout(start, note or default)
    stages = []
    if not last_given:
        stages.append(((terms[-1], "final") if ask == "term" else terms[-1], [
            layout(last, "Keep the pattern going: the last one is %s" % last, hl=["r0"] if len(labels[:given]) + 2 <= 5 else None),
            layout("?", "Keep the pattern going, one step at a time, to the last box")]))
    if ask == "sum":
        total = sum(terms)
        full = table(wrap([cell(t) for t in terms]), note="All %d of them. Added together: %s" % (count, fmt(total, unit)))
        stages.append(((total, "final"), [
            full,
            layout(last, "Added together: %s" % fmt(total, unit)),
            layout(start, "Added together: %s" % fmt(total, unit)),
            layout(start, "Now add them all together")]))
    staged(sid, before, stages)


R = "₹"
DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
WORDS = ["First", "Second", "Third"]

series("ee690589e4fb", [7 + 5 * i for i in range(6)], 3, labels=DAYS[:3] + ["Sat"], unit=R)
series("4ecb779627dd", [5 + 4 * i for i in range(8)], 3, ask="term")
series("d76c3cf0aefb", [5 + 4 * i for i in range(12)], 3, ans=424, note="12 rows are built, and 100 diyas are left over")
series("7efa676353df", [14 + 7 * i for i in range(8)], 3, word="Match")
series("56953204695e", [3 * 2 ** i for i in range(6)], 4, word="Day", what="Packets")
series("d07e7dd6ee49", [45 + 12 * i for i in range(8)], 1, word="Week", note="Each week 12 more runs than the week before. Total = ?")
series("027b4c337027", list(range(5, 51, 3)), 3, labels=["Row 1", "Row 2", "Row 3", "Last row"], last_given=True,
       note="Each row has 3 more dots. How many dots in all the rows?")
series("94e5c4e582d1", [7 + 5 * i for i in range(8)], 3, word="Day", unit=R, ask="term")
series("7634c8bb105d", [3 * 2 ** i for i in range(6)], 4, word="Day", what="Rupees", labels=DAYS[:4] + ["Sat"], unit=R)
series("fbd7a72b1ef5", [120 + 15 * i for i in range(7)], 1, word="Match", note="Each match 15 more runs than the one before. Total = ?")
series("043f0cb3c530", [3 + 4 * i for i in range(6)], 3)
series("c394181debf4", [14 + 7 * i for i in range(8)], 3, word="Hour")
series("71f500156066", [7 + 5 * i for i in range(8)], 3, word="Day", unit=R)
series("23dd2a488708", [3 * 2 ** i for i in range(6)], 4, word="Day", what="Rupees", unit=R, ask="term")
series("81db406f8cfb", [5 + 4 * i for i in range(8)], 3)
series("9f0edf64b65b", [5 + 4 * i for i in range(8)], 3, labels=WORDS + ["Row 8"], ask="term")
series("08910c395980", [5 + 4 * i for i in range(8)], 3)
series("9e4f8c5cca9f", [5 + 4 * i for i in range(7)], 3, labels=WORDS + ["Row 7"], ask="term")
series("0f3f64d1f90e", [6 + 6 * i for i in range(8)], 3, word="Ring", ans=434, note="8 rings and the 1 centre dot are half of all her dots")
series("07f3d561f6cf", [14 + 6 * i for i in range(8)], 1, word="Day", note="Each day 6 more samosas than the day before. Total = ?")
series("0665631dedcc", [12 + 6 * i for i in range(7)], 1, word="Match", ans=220, note="Each match 6 more runs. Total, plus a bonus of 10 = ?")
series("2d9552a0242f", [5 + 3 * i for i in range(12)], 3)
series("a16f27fc528c", [5 + 3 * i for i in range(15)], 3)
series("67f448cfe685", [5 + 4 * i for i in range(12)], 3)
series("fbd541626efb", [5 + 3 * i for i in range(6)], 3, labels=WORDS + ["Row 6"])
series("ebd04d868784", [5 + 3 * i for i in range(12)], 3, word="Ring")
series("f7cfa6212a05", [3 * 2 ** i for i in range(5)], 3, word="Day", ans=1395, note="Each packet costs ₹15. Cost of all the packets = ?")
series("5993ea75befe", [15 + 6 * i for i in range(7)], 3, word="Innings")
series("f86ccb6ef4b3", [6 + 4 * i for i in range(5)], 3, word="Over")
series("a41c3e92bc45", [5 + 3 * i for i in range(12)], 3, labels=WORDS + ["Ring 12"])
series("46548d866784", [5 + 4 * i for i in range(8)], 3, ask="term")
series("55b43754b228", [5 + 4 * i for i in range(5)], 3, note="Only the first 5 rows are taken. How many diyas in them?")
series("e3084e2ce698", [6 + 5 * i for i in range(8)], 3, labels=WORDS + ["Hour 8"])
series("28b56a00f003", list(range(20, 1, -3)), 3, labels=["Bottom", "Next", "Next", "Top"], last_given=True,
       note="Each layer is smaller by the same amount. How many samosas in all?")
series("2a3376aaaee5", [4 + 3 * i for i in range(8)], 3, word="Minute")
series("ded5e4569af1", [3 + 4 * i for i in range(7)], 4, word="Day", what="Rupees", labels=DAYS[:4] + ["Sun"], unit=R, ask="term")

staged("fd3ffd99600e", table([["5", "8", "11", "…"]], headers=["Ring 1", "Ring 2", "Ring 3", "…"],
                             note="100 stones in all. How many full rings can she make?"), [], origin="authored")
staged("9b9cf50653bb", table([[str(15 + 6 * i), str(10 + 4 * i)] for i in range(6)], headers=["Rohit", "Virat"],
                             note="One row for each innings. Difference between the two totals = ?"), [], origin="authored")
staged("0eee25daf5c9", table([["5", "11", "17", "23", "29"], ["…", "Day 12: ?"]],
                             note="One number for each day. Day 12 = ? and the total of all 12 = ?"), [], origin="authored")


# ── Textbook series: read the terms straight from the question ──────────────

TOKEN = r"\[box\]|\*|\?|\.\.\.|\d+/\d+|\d+(?:\.\d+)?"
SERIES = re.compile(r"((?:%s)(?:\s*,\s*(?:%s))+)" % (TOKEN, TOKEN))
BLANKS = ("[box]", "*", "?", "...")
HOW_MANY = {"two": 2, "three": 3}


def textbook(q):
    text = q["questionText"]
    runs = [re.findall(TOKEN, m) for m in SERIES.findall(text)]
    if not runs:
        return
    tokens = max(runs, key=len)
    if len(tokens) < 3 or len(tokens) > 12:
        return
    odd = re.search(r"odd man out|does not belong", text, re.I) is not None
    cells = ["?" if t in BLANKS else t for t in tokens]
    if not odd:
        m = re.search(r"next (two|three)", text, re.I)
        asked = HOW_MANY[m.group(1).lower()] if m else (1 if re.search(r"\bnext\b", text, re.I) else 0)
        trailing = 0
        while trailing < len(cells) and cells[-1 - trailing] == "?":
            trailing += 1
        if asked > trailing:
            cells += ["?"] * (asked - trailing)
        if "?" not in cells:
            return
    blanks = cells.count("?")
    before = table(wrap(cells), note="Which number does not fit the pattern?" if odd else "Find the pattern, then fill in each ?")
    key = validate.correct_text(q)
    answers = [t for t in re.findall(TOKEN, key) if t not in BLANKS]
    stages = []
    if odd and len(answers) == 1:
        stages.append(("final", table(wrap(cells), note="%s does not fit the pattern" % answers[0])))
    elif not odd and len(answers) == blanks and "square of" not in text.lower():
        filled, it = [], iter(answers)
        for c in cells:
            filled.append(next(it) if c == "?" else c)
        # Shown at the step that works the last answer out; if that number is already in the
        # question (as a term, or inside a fraction), no step can be told apart by it: the last step.
        plain_number = re.match(r"^\d+(\.\d+)?$", answers[-1]) and float(answers[-1]) not in validate.numbers_in(text)
        trig = (float(answers[-1]), "final") if plain_number else "final"
        stages.append((trig, table(wrap(filled), note="The series with every ? filled in")))
    staged(q["id"], before, stages)


for _q in sorted(POOL.values(), key=lambda x: x["id"]):
    if _q["node"] == "gr5_sequences" and _q["id"].startswith("IPMTB"):
        textbook(_q)
