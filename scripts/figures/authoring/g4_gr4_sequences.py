"""Figures for Grade 4 "Sequence & Series" (gr4_sequences).

    python -X utf8 scripts/figures/authoring/g4_gr4_sequences.py

Writes data/question-figures/parts/g4-gr4_sequences.json.

The main picture is the pattern set out on a number line with a hop for every jump, so a
child can see whether the jumps are equal, growing or shrinking. Where the numbers would
sit on top of each other (3, 9, 27, 81 ...) the links are set out in a table instead:
From | Jump | To. The unknown is never placed on the line before the steps reach it.
"""
import math
import re

from g4_gr4_factors_lib import (Part, n, nums, steps_of, stated, allowed_at, key_text, table, wrap, number_line,
                            with_note, tick_step, cut)

P = Part("gr4_sequences")
Q = P.Q

TOKEN = r"\d+/\d+|\d+(?:\.\d+)?|★|\*|\?|_{2,}"
RUN = re.compile(r"(?:%s)(?:\s*,\s*(?:%s))+" % (TOKEN, TOKEN))
BLANK = re.compile(r"^(★|\*|\?|_{2,})$")


def num(tok):
    return float(tok) if "." in tok else int(tok)


def tokens_of(text):
    """The longest list of terms written in the question, blanks included."""
    runs = [re.findall(TOKEN, m.group(0)) for m in RUN.finditer(text)]
    return max(runs, key=len) if runs else []


def ordinal(k):
    if 10 <= k % 100 <= 13:
        return "%dth" % k
    return "%d%s" % (k, {1: "st", 2: "nd", 3: "rd"}.get(k % 10, "th"))


def width(label):
    return 7.2 * len(label) + 2


def line_fits(vals, disp, labels):
    """True when the numbers and the jump labels can sit on a 264-unit line without touching."""
    lo, hi = min(vals), max(vals)
    if hi == lo or len(vals) > 6:
        return False
    px = 264.0 / (hi - lo)
    pts = sorted((v * px, width(d)) for v, d in zip(vals, disp))
    for (x1, w1), (x2, w2) in zip(pts, pts[1:]):
        if x2 - x1 < (w1 + w2) / 2:
            return False
    hops = sorted(((a + b) / 2.0 * px, width(lab)) for a, b, lab in zip(vals, vals[1:], labels))
    for (x1, w1), (x2, w2) in zip(hops, hops[1:]):
        if x2 - x1 < (w1 + w2) / 2:
            return False
    return True


def jump_labels(vals):
    """(label, the number a step must state before the label is shown, how the sum is written)."""
    pairs = list(zip(vals, vals[1:]))
    grows = all(isinstance(a, int) and isinstance(b, int) and a > 0 and b % a == 0 and b // a >= 2 for a, b in pairs)
    shrinks = all(isinstance(a, int) and isinstance(b, int) and b > 0 and a % b == 0 and a // b >= 2 for a, b in pairs)
    steady = len(set(b - a for a, b in pairs)) == 1
    out = []
    for a, b in pairs:
        if grows and not steady:
            out.append(("× %d" % (b // a), b // a, "×"))
        elif shrinks and not steady:
            out.append(("÷ %d" % (a // b), a // b, "÷"))
        elif b >= a:
            out.append(("+%s" % n(b - a), b - a, "+"))
        else:
            out.append(("−%s" % n(a - b), a - b, "−"))
    return out, (grows or shrinks) and not steady


def series(qid, disp=None, vals=None, origin="authored", note=None, mode=None, before=None, labels=None,
           intro=None, far=None, uses_options=False, reveal=None, rule_known=False):
    """disp: every term as written, None for an unknown. vals: every term as a number.
    Unknowns are filled from the answer key when vals is not given.
    far: the position of the last term, when terms are skipped and the question asks for it."""
    q = Q[qid]
    if disp is None:
        toks = tokens_of(q["questionText"])
        disp = [None if BLANK.match(t) else t for t in toks]
    if vals is None:
        answers = [num(t) for t in re.findall(r"\d+(?:\.\d+)?", key_text(q))]
        while disp.count(None) < len(answers):
            disp = disp + [None]
        if disp.count(None) != len(answers):
            P.log.append("%s: %d blanks but the key has %d numbers" % (qid, disp.count(None), len(answers)))
            return
        it = iter(answers)
        vals = [next(it) if d is None else num(d) for d in disp]
    given = [d is not None for d in disp]
    disp = [d if d is not None else n(v) for d, v in zip(disp, vals)]
    N = len(vals)
    auto, multiply = jump_labels(vals)
    labels = labels or auto
    if mode is None:
        mode = "links" if multiply or not line_fits(vals, disp, [l[0] for l in labels]) else "line"
    unknown_last = not given[-1]
    reveal = reveal or {}   # {index of an unknown: the step that finds it}, when the number alone cannot tell
    steady = rule_known or len(set(l[0] for l in labels)) == 1
    head ="Rule" if any(l[2] in "×÷" for l in labels) else "Jump"

    def line(vis, labelled, note_, hl_pts=(), hl_hops=()):
        ks = sorted(vis)
        if len(ks) < 2:
            return None
        shown = [vals[k] for k in ks]
        lo, hi = min(shown), max(shown)
        if all(isinstance(v, int) for v in shown):
            g = 0
            for v in shown:
                g = math.gcd(g, v - lo)
            step = tick_step(lo, hi, g or 1)
        else:
            step = (hi - lo) / 10.0
        points = [{"at": vals[k], "label": disp[k]} for k in ks]
        hops, hl = [], []
        for k in ks:
            if k + 1 in vis:
                hop = {"from": vals[k], "to": vals[k + 1]}
                if k in labelled:
                    hop["label"] = labels[k][0]
                if k in hl_hops:
                    hl.append("h%d" % len(hops))
                hops.append(hop)
        for j, k in enumerate(ks):
            if k in hl_pts:
                hl.append("p%d" % j)
        return number_line(lo, hi, step, "none", points, hops[-8:], note_, hl)

    def links(vis, labelled, note_, hl_rows=()):
        rows, hl = [], []
        for k in range(N - 1):
            if k in vis and (k + 1 in vis or not given[k + 1]):
                if k in hl_rows:
                    hl.append(len(rows))
                rows.append([disp[k], labels[k][0] if k in labelled else "?", disp[k + 1] if k + 1 in vis else "?"])
        if not rows:
            return None
        drop = max(0, len(rows) - 6)
        hl = ["r%d" % (r - drop) for r in hl if r >= drop]
        return table(rows[drop:], note_, ["From", head, "To"], hl if len(hl) < len(rows[drop:]) else None)

    def draw(vis, labelled, note_, new_pts=(), new_labels=()):
        if mode == "line":
            return line(vis, labelled, note_, new_pts, [k - 1 for k in new_pts])
        return links(vis, labelled, note_, set(new_labels) | set(k - 1 for k in new_pts))

    # Before answering: the givens only.
    start = set(k for k in range(N) if given[k])
    if before is None:
        if note is None:
            if far:
                note = "The pattern goes on. Which number is the %s term?" % ordinal(far)
            elif all(given):
                note = "Look at the jumps from each number to the next"
            elif unknown_last:
                note = "How big is each jump? What comes next?" if not multiply else "What is the rule? What comes next?"
            else:
                note = "How big are the jumps? Find the missing number"
        if mode == "line":
            before = line(start, set(), note)
        else:
            cells = [d if g else "?" for d, g in zip(disp, given)]
            if far:
                cells = [d for d, g in zip(disp, given) if g] + ["…", "?"]
            before = table(wrap(cells), note)

    q_allowed = nums(q["questionText"])
    prev = (frozenset(k for k in start if vals[k] in q_allowed), frozenset())
    figs = {}
    count = len(steps_of(q))
    for i in range(count):
        al, st = allowed_at(q, i), stated(q, i)
        said = " ".join(s.get("text", "") for s in steps_of(q)[:i + 1])
        vis = set()
        for k in range(N):
            if given[k] and vals[k] in al:
                vis.add(k)
            elif not given[k] and vals[k] in al:
                # found once a step gives it as a result ("= 80", "is 80", "to get 80"), not merely mentions the number
                found = re.search(r"(?:=|\bis|\bare|\bget|term,|number,|stands for)\s+(?:the\s+)?%s(?!\d|\.\d)" % re.escape(n(vals[k])), said)
                if (i >= reveal[k]) if k in reveal else (found is not None or i == count - 1):
                    vis.add(k)
        # an unknown is only shown once every unknown before it is
        for k in sorted(vis):
            if not given[k] and any(not given[j] and j not in vis for j in range(k)):
                vis.discard(k)
        labelled = set()
        for k in range(N - 1):
            if k not in vis or not (k + 1 in vis or not given[k + 1]):
                continue
            ok = labels[k][1] in st
            if ok and k + 1 not in vis and not steady:
                # the jump into a number not found yet: only once a step names it as the next jump
                ok = re.search(r"(?:next|after that)(?:\s+\w+){0,3}?\s+(?:is|are)\s+[\d., and]*?(?<![\d.])%s(?!\d|\.\d)"
                               % re.escape(n(labels[k][1])), said) is not None
            if not ok:
                break   # jumps are shown in order, so a number stated for another reason is not taken for a jump
            labelled.add(k)
        if intro and intro[0] == i:
            figs[i] = draw(vis, set(), intro[1])
            prev = (frozenset(vis), frozenset())
            continue
        state = (frozenset(vis), frozenset(labelled))
        if state == prev or not (labelled or any(not given[k] for k in vis)):
            continue
        new_pts = sorted(k for k in vis - prev[0] if not given[k])
        new_labels = sorted(labelled - prev[1])
        if new_pts:
            k = new_pts[-1]
            if k - 1 in vis and k - 1 in labelled:
                text = "%s %s %s = %s" % (disp[k - 1], labels[k - 1][2], n(labels[k - 1][1]), disp[k])
            elif far and k == N - 1:
                text = "The %s term is %s" % (ordinal(far), disp[k])
            else:
                text = "The missing number is %s" % disp[k] if not unknown_last else "Next comes %s" % disp[k]
        else:
            shown = [labels[k][0] for k in sorted(labelled)]
            if len(set(shown)) == 1:
                text = ("Every jump is %s" if head == "Jump" else "The rule every time is %s") % shown[0]
            else:
                text = ("The jumps: %s" if head == "Jump" else "The rules: %s") % ", ".join(shown)
        figs[i] = draw(vis, labelled, cut(text), new_pts, new_labels)
        prev = state
    P.add(qid, before, figs, origin=origin, uses_options=uses_options)


# ── Rule: "find the Nth term" of a pattern with equal jumps ──────────────────

def nth_term(qid, given, nth, origin="rule"):
    q = Q[qid]
    answer = int(re.findall(r"\d+", key_text(q))[0])
    d = given[1] - given[0]
    first = given[0]
    if first + (nth - 1) * d != answer:
        P.log.append("%s: the %s term works out as %d, key is %d" % (qid, ordinal(nth), first + (nth - 1) * d, answer))
        return
    sign = "+" if d > 0 else "−"

    def near(labelled, note):
        lo, hi = min(given), max(given)
        hops = [{"from": a, "to": b} for a, b in zip(given, given[1:])]
        if labelled:
            for h in hops:
                h["label"] = "%s%d" % (sign, abs(d))
        return number_line(lo, hi, abs(d), "none", [{"at": v, "label": str(v)} for v in given], hops, note)

    def whole(label, note):
        lo, hi = min(first, answer), max(first, answer)
        hop = {"from": first, "to": answer}
        if label:
            hop["label"] = label
        return number_line(lo, hi, tick_step(lo, hi, abs(d)), "ends",
                           [{"at": first, "label": "1st"}, {"at": answer, "label": ordinal(nth)}], [hop], note, ["h0"])

    total = abs(answer - first)
    finals = []
    for label in ("%d jumps of %d" % (nth - 1, abs(d)), "%s%d" % (sign, total), None):
        for note in ("%d %s %d = %d" % (first, sign, total, answer), "The %s term is %d" % (ordinal(nth), answer)):
            finals.append(whole(label, note))
    before = near(False, "The pattern goes on. Which number is the %s term?" % ordinal(nth))
    figs, labelled, done = {}, False, False
    count = len(steps_of(q))
    for i in range(count):
        st = stated(q, i)
        if not done and (answer in st or i == count - 1):
            figs[i] = finals
            done = True
        elif not labelled and not done and abs(d) in st:
            figs[i] = near(True, "Every jump is %s%d" % (sign, abs(d)))
            labelled = True
    P.add(qid, before, figs, origin=origin)


# ── Rule: adding a list by pairing its two ends ──────────────────────────────

def pair_sum(qid):
    q = Q[qid]
    figs, rows = {}, []
    for i, s in enumerate(steps_of(q)):
        t = s.get("text", "")
        m_list = re.search(r"(?:list:|numbers are) ([\d, and]+?)\.", t)
        m_make = re.search(r"(\d+) pairs of (\d+) make (\d+)", t)
        m_mid = re.search(r"middle number is (\d+)", t)
        m_total = re.search(r"to get (\d+)", t)
        if m_list and not rows:
            cells = re.findall(r"\d+", m_list.group(1))
            figs[i] = table(wrap(cells), "%d numbers to add" % len(cells))
        elif "Pair" in t and not rows:
            pairs = [(a, b) for a, b, _ in re.findall(r"(\d+) \+ (\d+) = (\d+)", t)] or re.findall(r"(\d+) and (\d+)", t)
            for a, b in pairs:
                rows.append([a, "+", b, "=", str(int(a) + int(b))])
            if "and so on" in t:
                rows.append(["…", "+", "…", "=", rows[0][4]])
            figs[i] = table(rows, "Pair the numbers from the two ends. Every pair makes %s" % rows[0][4])
        elif rows and m_mid:
            figs[i] = table(rows, "The pairs leave %s alone in the middle" % m_mid.group(1))
        elif rows and m_make and m_total:
            figs[i] = table(rows, "%s pairs of %s make %s. With the middle number: %s" % (m_make.groups() + (m_total.group(1),)))
        elif rows and m_make:
            figs[i] = table(rows, "%s pairs of %s make %s" % m_make.groups())
        elif rows and m_total:
            figs[i] = table(rows, "Add the middle number to get %s" % m_total.group(1))
    P.add(qid, None, figs)


# ── The generated families (PH3_...) ─────────────────────────────────────────

for qid in P.ids("PH3_"):
    text = Q[qid]["questionText"]
    m_nth = re.match(r"^In an arithmetic sequence starting ([\d, ]+), \.\.\., find the (\d+)(?:st|nd|rd|th) term\.$", text)
    if text.startswith("Find the next number"):
        series(qid, origin="rule")
    elif m_nth:
        nth_term(qid, [int(x) for x in re.findall(r"\d+", m_nth.group(1))], int(m_nth.group(2)))
    elif text.startswith("Find the sum"):
        pair_sum(qid)
    else:
        P.log.append("%s: no rule for this wording" % qid)


# ═════════════════════════════════════════════════════════════════════════════
# Individually drawn
# ═════════════════════════════════════════════════════════════════════════════

def A(qid, figure=None, steps=None, **kw):
    P.add(qid, figure, steps, origin="authored", **kw)


# Next term / missing term, read from the question and filled from the answer key
for qid in ("PYQ_2016_Q01", "PYQ_2018_Q38", "PYQ_2019_Q28", "Q_CH15_018", "Q_CH16_002", "Q_CH16_003", "Q_CH16_005",
            "Q_CH16_006", "Q_CH16_007", "Q_CH16_011", "Q_CH16_013", "Q_CH16_014", "Q_CH16_016", "Q_CH16_017",
            "Q_CH16_018", "Q_CH16_022", "EXT_G4_WS2_CH16_005", "EXT_G4_WS2_CH16_006",
            "EXT_G4_FP_2025_017"):
    series(qid)
series("Q_CH16_024", reveal={5: 2})   # the answer, 3, is also the number divided by, so the step is named here
series("EXT_G4_FP_2022_017", disp=["122", "117", "107", "92", "72", None])

# The tenth term, reached one jump at a time
series("PYQ_2017_Q37", disp=["24", "39", "53", "66", "78"] + [None] * 5, vals=[24, 39, 53, 66, 78, 89, 99, 108, 116, 123], far=10)
series("EXT_G4_FP_2021_013", disp=["24", "39", "53", "66", "78"] + [None] * 5, vals=[24, 39, 53, 66, 78, 89, 99, 108, 116, 123], far=10)
series("Q_CH16_008", disp=["53", "60", "68", "77"] + [None] * 6, vals=[53, 60, 68, 77, 87, 98, 110, 123, 137, 152], far=10)
series("EXT_G4_FP_2024_039", disp=["12", "23", "33", "42", "50"] + [None] * 4, vals=[12, 23, 33, 42, 50, 57, 63, 68, 72], far=9)

# Equal jumps, a term far along
nth_term("EXT_G4_FP_2023_015", [24, 41, 58, 75, 92], 28, origin="authored")
nth_term("EXT_G4_FP_2024_007", [7, 10, 13, 16, 19], 11, origin="authored")
nth_term("EXT_G4_FP_2025_037", [12, 19, 26, 33, 40], 38, origin="authored")
nth_term("EXT_G4_WS2_CH16_015", [92, 88, 84, 80, 76], 18, origin="authored")

# Two rules taking turns: × 3, then − 2
_v = [2, 6, 4, 12, 10, 30, 28, 84, 82, 246]
series("G4A_SEQUENCES_007", disp=[str(x) for x in _v[:7]] + [None] * 3, vals=_v, mode="links", far=10, rule_known=True,
       labels=[("× 3", 3, "×") if k % 2 == 0 else ("− 2", 2, "−") for k in range(9)],
       before=table(wrap([str(x) for x in _v[:7]] + ["…"], 4), "Find the rule. Which number is the 10th?"))

# Fractions: the jumps are in the top numbers
series("Q_CH16_010", disp=["1", "2", "4", "7", "11", None], vals=[1, 2, 4, 7, 11, 16],
       before=table(wrap(["1/5", "2/5", "4/5", "7/5", "11/5", "?"], 3), "How do the fractions grow? What comes next?"),
       intro=(0, "The bottom number is always 5, so watch the top numbers"))

# One number breaks the pattern
A("Q_CH16_021",
  number_line(2, 37, 1, "none", [{"at": v, "label": str(v)} for v in (2, 5, 10, 17, 28, 37)],
              [{"from": a, "to": b} for a, b in zip((2, 5, 10, 17, 28), (5, 10, 17, 28, 37))],
              "One number breaks the pattern. Look at the jumps"), {
      0: number_line(2, 37, 1, "none", [{"at": v, "label": str(v)} for v in (2, 5, 10, 17, 28, 37)],
                     [{"from": a, "to": b, "label": "+%d" % (b - a)} for a, b in zip((2, 5, 10, 17, 28), (5, 10, 17, 28, 37))],
                     "The gaps between neighbours are 3, 5, 7, 11 and 9"),
      1: number_line(2, 37, 1, "none", [{"at": v, "label": str(v)} for v in (2, 5, 10, 17, 28, 37)],
                     [{"from": a, "to": b, "label": "+%d" % (b - a)} for a, b in zip((2, 5, 10, 17, 28), (5, 10, 17, 28, 37))],
                     "After 3, 5, 7 the gaps should be 9 and then 11, not 11 and then 9", ["h3", "h4"]),
      2: number_line(2, 37, 1, "none", [{"at": v, "label": str(v)} for v in (2, 5, 10, 17, 26, 37)],
                     [{"from": a, "to": b, "label": "+%d" % (b - a)} for a, b in zip((2, 5, 10, 17, 26), (5, 10, 17, 26, 37))],
                     "With 26 in that place: 17 + 9 = 26, and 26 + 11 = 37", ["p4"]),
      3: number_line(2, 37, 1, "none", [{"at": v, "label": str(v)} for v in (2, 5, 10, 17, 28, 37)],
                     [{"from": a, "to": b, "label": "+%d" % (b - a)} for a, b in zip((2, 5, 10, 17, 28), (5, 10, 17, 28, 37))],
                     "28 is the number that does not belong", ["p4"]),
  })


# Each term is the two before it added together
def sums(qid, vals, known, note):
    q = Q[qid]
    cells = [str(v) for v in vals[:known]] + ["?"] * (len(vals) - known)
    figs = {}
    rows_before = None
    for i in range(len(steps_of(q))):
        al = allowed_at(q, i) if i < len(steps_of(q)) - 1 else allowed_at(q, i)
        st = stated(q, i)
        rows = []
        for k in range(2, len(vals)):
            a, b, c = vals[k - 2], vals[k - 1], vals[k]
            said = re.search(r"(?<!\d)%d \+ %d = %d(?!\d)" % (a, b, c), " ".join(s.get("text", "") for s in steps_of(q)[:i + 1]))
            if said or (k >= known and c in st and all(x in al for x in (a, b))):
                rows.append([str(a), "+", str(b), "=", str(c)])
        rows = rows[-6:]
        if rows and rows != rows_before:
            figs[i] = table(rows, "Add two neighbours to get the number after them", hl=["r%d" % (len(rows) - 1)])
            rows_before = rows
    P.add(qid, table(wrap(cells), note), figs, origin="authored")


sums("EXT_G4_WS2_CH16_009", [4, 7, 11, 18, 29, 47, 76], 5, "How is each number made from the ones before it?")
sums("Q_CH16_009", [4, 7, 11, 18, 29, 47, 76], 5, "How is each number made from the ones before it?")
sums("Q_CH16_020", [2, 3, 5, 8, 13, 21, 34], 6, "How is each number made from the ones before it?")


# Squares, cubes and n × (n + 1): the position and the term side by side
def indexed(qid, terms, how, head, note, before_cells=None):
    """terms: every term. how(k) -> the working for position k, e.g. '3 × 3'."""
    q = Q[qid]
    known = len(terms) - 1
    cells = before_cells or [str(t) for t in terms[:known]] + ["?"]
    figs, last_rows = {}, None
    count = len(steps_of(q))
    for i in range(count):
        text = " ".join(s.get("text", "") for s in steps_of(q)[:i + 1])
        st = stated(q, i)
        rows = []
        for k in range(1, len(terms) + 1):
            if re.search(r"(?<!\d)%s(?!\d)" % re.escape(how(k)), text) or (k == len(terms) and terms[-1] in st and rows):
                rows.append([str(k), how(k), str(terms[k - 1]) if (k <= known or terms[-1] in st) else "?"])
        rows = rows[-6:]
        if rows and rows != last_rows:
            figs[i] = table(rows, note, ["Position", head, "Number"], ["r%d" % (len(rows) - 1)])
            last_rows = rows
    P.add(qid, table(wrap(cells), "What is the rule? What comes next?"), figs, origin="authored")


indexed("Q_CH16_004", [1, 8, 27, 64, 125, 216], lambda k: "%d × %d × %d" % (k, k, k), "Multiply", "Each number is its position used three times")
indexed("Q_CH16_015", [1, 4, 9, 16, 25, 36], lambda k: "%d × %d" % (k, k), "Multiply", "Each number is its position times itself")

A("EXT_G4_WS2_CH16_004", table(wrap(["1", "8", "27", "64", "125", "?"], 3), "What is the rule? What comes next?"), {
    0: table([["2nd", "2 × 2 × 2", "8"]], "A number multiplied by itself three times", ["Position", "Multiply", "Number"]),
    1: table([["2nd", "2 × 2 × 2", "8"], ["5th", "5 × 5 × 5", "125"]], "The position is the number that is multiplied",
             ["Position", "Multiply", "Number"], ["r1"]),
    2: table([["2nd", "2 × 2 × 2", "8"], ["5th", "5 × 5 × 5", "125"], ["6th", "6 × 6 × 6", "216"]],
             "The 6th term uses 6, so it is 216", ["Position", "Multiply", "Number"], ["r2"]),
})
A("Q_CH16_023", table(wrap(["2", "6", "12", "20", "30", "42"], 3), "The rule is n × (n + 1). What is the 10th term?"), {
    0: table([["1", "1 × 2", "2"], ["2", "2 × 3", "6"]], "Position times the number just after it", ["Position n", "n × (n + 1)", "Term"]),
    1: table([["1", "1 × 2", "2"], ["2", "2 × 3", "6"], ["10", "10 × 11", "?"]], "For the 10th term, n is 10 and the next number is 11",
             ["Position n", "n × (n + 1)", "Term"], ["r2"]),
    2: table([["1", "1 × 2", "2"], ["2", "2 × 3", "6"], ["10", "10 × 11", "110"]], "The 10th term is 110",
             ["Position n", "n × (n + 1)", "Term"], ["r2"]),
})

# 416, 525, 636, 749: split into a first part and a square
A("EXT_G4_WS2_CH16_002", table([["416", "525", "636", "749", "?"]], "What is the rule? What comes next?"), {
    0: table([["4", "16"], ["5", "25"], ["6", "36"], ["7", "49"]], "Split each number into two parts", ["First part", "Second part"]),
    1: table([["4", "16"], ["5", "25"], ["6", "36"], ["7", "49"]], "The second part is the first part times itself",
             ["First part", "Second part"]),
    2: table([["4", "16"], ["5", "25"], ["6", "36"], ["7", "49"], ["8", "?"]], "The next first part is 8",
             ["First part", "Second part"], ["r4"]),
    3: table([["4", "16"], ["5", "25"], ["6", "36"], ["7", "49"], ["8", "64"]], "Join 8 and 64 to make 864",
             ["First part", "Second part"], ["r4"]),
})

# 9999999, 777777, ___, 3333, 111
_nines = ["9999999", "777777", "?", "3333", "111"]
for qid in ("EXT_G4_WS2_CH16_001", "Q_CH16_001"):
    A(qid, table([_nines], "Look at the digit used, and at how many times it is written"), {
        0: table([_nines, ["9", "7", "5", "3", "1"]], "Second row: the digit used. It goes down by 2 each time", hl=["r1"]),
        1: table([_nines, ["9", "7", "5", "3", "1"], ["7", "6", "5", "4", "3"]],
                 "Third row: how many digits. It goes down by 1 each time", hl=["r2"]),
        2: table([["9999999", "777777", "55555", "3333", "111"]], "The digit 5, written 5 times: 55555"),
    })

# Two patterns woven together
A("G4A_SEQUENCES_001", table(wrap(["2", "50", "5", "46", "8", "42", "11", "38"], 4),
                             "Read along the top row, then the bottom row. What is the 15th number?"), {
    0: table([["2", "50"], ["5", "46"], ["8", "42"], ["11", "38"]], "Odd places go up by 3. Even places go down by 4",
             ["Odd places", "Even places"]),
    1: table([["2", "50"], ["5", "46"], ["8", "42"], ["11", "38"]], "The 15th place is an odd place: use the left column",
             ["Odd places", "Even places"]),
    3: number_line(2, 23, 3, "ends", [{"at": 2, "label": "1st"}, {"at": 23, "label": "8th"}],
                   [{"from": 2, "to": 23, "label": "7 jumps of 3"}], "The 8th number of 2, 5, 8, 11, … is 23", ["h0"]),
})
A("Q_CH16_025", table(wrap(["1", "1", "2", "4", "3", "9", "4", "16", "5", "?"]), "Two patterns take turns. What comes next?"), {
    0: table([["1", "1"], ["2", "4"], ["3", "9"], ["4", "16"], ["5", "?"]], "Every other number, from the first: 1, 2, 3, 4, 5",
             ["Counting", "In between"]),
    1: table([["1", "1"], ["2", "4"], ["3", "9"], ["4", "16"], ["5", "?"]], "Each number on the right is its partner times itself",
             ["Counting", "In between"]),
    2: table([["1", "1"], ["2", "4"], ["3", "9"], ["4", "16"], ["5", "25"]], "5 × 5 = 25", ["Counting", "In between"], ["r4"]),
})

# A repeating block of symbols
_sym = [["*", "■", "○", "△", "⊕"]]
A("EXT_G4_WS2_CH16_018", table(_sym, "These 5 symbols repeat in this order. Which one is in the 37th place?"), {
    0: table(_sym, "The last symbol of a group sits at place 5, 10, 15 and so on"),
    1: table(_sym, "Place 35 is the end of a full group"),
    2: table(_sym, "Place 37 is 2 places into the next group"),
    3: table(_sym, "The 2nd symbol in the group is ■"),
})

# How many terms from the first to the last
for qid, given, last in (("EXT_G4_WS2_CH16_017", [1, 7, 13, 19, 25], 103), ("PYQ_2017_Q12", [1, 8, 15, 22, 29], 113)):
    d = given[1] - given[0]
    jumps = (last - given[0]) // d
    pts = [{"at": given[0], "label": str(given[0])}] + [{"at": v} for v in given[1:]] + [{"at": last, "label": str(last)}]
    A(qid, number_line(given[0], last, last - given[0], "none", pts,
                       note="%s, … %d: how many numbers in all?" % (", ".join(str(v) for v in given), last)), {
        0: number_line(given[0], last, last - given[0], "none", pts, [{"from": given[0], "to": given[1], "label": "+%d" % d}],
                       "Every jump is %d" % d, ["h0"]),
        1: [number_line(given[0], last, last - given[0], "none", pts, [{"from": given[0], "to": last, "label": str(last - given[0])}],
                        "From %d to %d is a distance of %d" % (given[0], last, last - given[0]), ["h0"]),
            number_line(given[0], last, last - given[0], "none", pts, [{"from": given[0], "to": last}],
                        "Find the distance from the first number to the last", ["h0"])],
        2: [number_line(given[0], last, d, "none", [pts[0], pts[-1]], [{"from": given[0], "to": last, "label": "%d jumps of %d" % (jumps, d)}],
                        "Each little gap is one jump of %d" % d),
            number_line(given[0], last, d, "none", [pts[0], pts[-1]], [{"from": given[0], "to": last, "label": "jumps of %d" % d}],
                        "Each little gap is one jump of %d. Count the gaps" % d)],
        3: [number_line(given[0], last, d, "none", [pts[0], pts[-1]], [{"from": given[0], "to": last, "label": "%d jumps" % jumps}],
                        "%d jumps join %d numbers" % (jumps, jumps + 1)),
            number_line(given[0], last, d, "none", [pts[0], pts[-1]], note="One more number than jumps: %d numbers" % (jumps + 1))],
    })

# A pattern that stops at 99: which of its numbers are even
A("G4A_SEQUENCES_002", number_line(4, 19, 5, "none", [{"at": v, "label": str(v)} for v in (4, 9, 14, 19)],
                                   [{"from": a, "to": a + 5, "label": "+5"} for a in (4, 9, 14)],
                                   "It goes on like this as far as 99. How many of its numbers are even?"), {
    0: number_line(4, 19, 5, "none", [{"at": v, "label": str(v)} for v in (4, 9, 14, 19)],
                   [{"from": a, "to": a + 5, "label": "+5"} for a in (4, 9, 14)], "Even, odd, even, odd: the numbers take turns",
                   ["p0", "p2"]),
    1: number_line(4, 94, 10, "ends", [{"at": 4}, {"at": 14}, {"at": 24}, {"at": 94}], note="The even ones end in 4: 4, 14, 24, … 94"),
    2: number_line(4, 94, 10, "ends", [{"at": 4}, {"at": 94}], [{"from": 4, "to": 94, "label": "9 jumps of 10"}],
                   "9 jumps of 10 join 10 numbers", ["h0"]),
})

# Two patterns that meet
_ab = [["A", "5", "9", "13", "17"], ["B", "2", "9", "16", "23"]]
A("G4A_SEQUENCES_008", table(_ab, "A goes up in 4s and B in 7s. Both have 9. Where do they meet next?"), {
    0: table(_ab, "From 9, pattern A goes up in 4s and pattern B goes up in 7s"),
    2: number_line(9, 37, 28, "ends", [{"at": 9, "label": "both"}, {"at": 37, "label": "both"}], [{"from": 9, "to": 37, "label": "+28"}],
                   "28 is a multiple of 4 and of 7, so both patterns land on 9 + 28", ["h0"]),
    3: number_line(2, 37, 1, "none", [{"at": v, "label": str(v)} for v in (2, 9, 16, 23, 30, 37)],
                   [{"from": a, "to": a + 4} for a in range(5, 37, 4)], "Hops are pattern A, dots are pattern B. They meet at 9 and 37",
                   ["p1", "p5"]),
})

# The 5th number is 23 and the 8th is 35
A("G4A_SEQUENCES_009", number_line(1, 8, 1, "all", [{"at": 5, "label": "23"}, {"at": 8, "label": "35"}],
                                   note="Below the line: the position. Above: the number there. 1st number = ?"), {
    0: number_line(1, 8, 1, "all", [{"at": 5, "label": "23"}, {"at": 8, "label": "35"}], [{"from": 5, "to": 8, "label": "3 jumps: +12"}],
                   "From the 5th number to the 8th: 3 jumps, and the numbers rise by 12", ["h0"]),
    1: number_line(1, 8, 1, "all", [{"at": 5, "label": "23"}, {"at": 8, "label": "35"}], [{"from": 5, "to": 8, "label": "3 jumps of 4"}],
                   "12 shared over 3 jumps: one jump is 4", ["h0"]),
    2: number_line(1, 8, 1, "all", [{"at": 5, "label": "23"}, {"at": 8, "label": "35"}], [{"from": 5, "to": 1, "label": "4 jumps of 4"}],
                   "Back from the 5th number to the 1st is 4 jumps, not 5", ["h0"]),
    3: number_line(1, 8, 1, "all", [{"at": 1, "label": "7"}, {"at": 5, "label": "23"}, {"at": 8, "label": "35"}],
                   [{"from": 5, "to": 1, "label": "−16"}], "Go back 16 from 23 to reach 7", ["p0"]),
})

# Saving a little more each day
_saved = [5, 8, 11, 14, 17, 20, 23, 26]
_total = [5, 13, 24, 38, 55, 75, 98, 124]
_days = ["+%d" % v for v in _saved]   # each bar is named by what was added that day
A("G4A_SEQUENCES_006", None, {
    0: table(wrap(_saved, 4), "Rupees saved day by day: 3 more each day"),
    1: {"kind": "barChart", "unit": "₹ in all", "bars": [{"label": d, "value": v} for d, v in zip(_days, _total)],
        "note": "The running total after each day. Under each bar: what was added"},
    2: {"kind": "barChart", "unit": "₹ in all", "bars": [{"label": d, "value": v} for d, v in zip(_days, _total)],
        "highlight": ["b6"], "note": "After the 7th day the total is 98: not yet more than 100"},
    3: {"kind": "barChart", "unit": "₹ in all", "bars": [{"label": d, "value": v} for d, v in zip(_days, _total)],
        "highlight": ["b7"], "note": "On the 8th day the total becomes 124"},
})

# 66 km in 6 days, 4 km less each day
A("PYQ_2017_Q05", None, {
    0: table([["Day 6", "?"], ["Day 5", "? + 4"], ["Day 4", "? + 8"], ["Day 3", "? + 12"], ["Day 2", "? + 16"], ["Day 1", "? + 20"]],
             "Compare every day with day 6", ["Day", "km walked"]),
    1: table([["Day 6", "?"], ["Day 5", "? + 4"], ["Day 4", "? + 8"], ["Day 3", "? + 12"], ["Day 2", "? + 16"], ["Day 1", "? + 20"]],
             "The extra kilometres come to 60 km", ["Day", "km walked"]),
    3: {"kind": "barChart", "unit": "km", "bars": [{"label": "Day %d" % (k + 1), "value": v} for k, v in enumerate((21, 17, 13, 9, 5, 1))],
        "highlight": ["b5"], "note": "21 + 17 + 13 + 9 + 5 + 1 = 66. He walked 1 km on the 6th day"},
})

# Odd numbers add up to squares
A("EXT_G4_FP_2025_004", None, {
    0: {"kind": "grid", "rows": 2, "cols": 2, "shaded": [[0, 1], [1, 0], [1, 1]],
        "note": "The first 2 odd numbers make a 2 by 2 square: 4 in all"},
    1: {"kind": "grid", "rows": 3, "cols": 3, "shaded": [[0, 2], [1, 2], [2, 0], [2, 1], [2, 2]],
        "note": "The first 3 odd numbers make a 3 by 3 square: 9 in all"},
    2: {"kind": "grid", "rows": 12, "cols": 12, "note": "The first 12 odd numbers fill a 12 by 12 square"},
})
A("EXT_G4_FP_2021_027", None, {
    0: {"kind": "grid", "rows": 3, "cols": 3, "shaded": [[0, 2], [1, 2], [2, 0], [2, 1], [2, 2]],
        "note": "1 + 3 + 5 = 9: the odd numbers wrap round to make a 3 by 3 square"},
})

# Counting back through the odd numbers
A("EXT_G4_FP_2021_030", None, {
    3: number_line(609, 725, 116, "ends", [{"at": 725, "label": "1st"}, {"at": 609, "label": "59th"}],
                   [{"from": 725, "to": 609, "label": "58 jumps of 2"}], "Jump back 116 from 725 to land on 609", ["h0"]),
})

P.save()
