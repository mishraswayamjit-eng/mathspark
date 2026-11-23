"""Figures for Grade 4 "Factors & Multiples" (gr4_factors).

    python -X utf8 scripts/figures/authoring/g4_gr4_factors.py

Writes data/question-figures/parts/g4-gr4_factors.json. Rules read the numbers from the
question and its own steps; the individually drawn ones are further down.
"""
import math
import re

from g4_gr4_factors_lib import (Part, ints, steps_of, stated, table, wrap, venn, number_line, with_note,
                            join_and, cut)

P = Part("gr4_factors")
Q = P.Q


def is_prime(x):
    return x > 1 and all(x % d for d in range(2, int(x ** 0.5) + 1))


def tree(number, depth=None, note=None, hl=None):
    fig = {"kind": "factorTree", "number": number}
    if depth is not None:
        fig["depth"] = depth
    return with_note(fig, note, hl)


def balance(left, right, note=None, hl=None):
    return with_note({"kind": "balance", "left": left, "right": right}, note, hl)


def place(number, note=None, hl=None):
    return with_note({"kind": "placeChart", "number": number}, note, hl)


def clock(hour, minute, note=None, hl=None):
    return with_note({"kind": "clock", "hour": hour, "minute": minute}, note, hl)


def times(xs):
    return " × ".join(str(x) for x in xs)


def commas(xs):
    return ", ".join(str(x) for x in xs)


VENN_ROOM = 13   # characters that fit inside one part of the two circles


def factor_venn(a, b, la, common, lb, note, hl=None):
    """Factors of a only, of both, of b only. None when a list is too long to fit in its part."""
    parts = [commas(la) or "–", commas(common) or "–", commas(lb) or "–"]
    if max(len(p) for p in parts) > VENN_ROOM:
        return None
    return venn("Factors of %d" % a, "Factors of %d" % b, parts[0], parts[1], parts[2], note, hl)


# ── Rule: the HCF of two numbers ─────────────────────────────────────────────

def hcf_before(a, b):
    return venn("Factors of %d" % a, "Factors of %d" % b, "?", "?", "?",
                "HCF = the biggest number that is a factor of both")


def hcf_step_figures(q, a, b):
    g = math.gcd(a, b)
    lists, mult, rows = {}, {}, []
    last = None
    out = []
    count = len(steps_of(q))
    for i, s in enumerate(steps_of(q)):
        t = s.get("text", "")
        fig = None
        m_list = re.search(r"factors of (\d+) are ([\d, and]+?)\.", t)
        m_both = re.search(r"numbers in both lists are ([\d, and]+?)\.", t)
        m_mult = re.findall(r"\b(\d+) = (\d+) × (\d+)(?! ×)", t)
        m_share = re.search(r"share are ([\d, and]+?)\.", t)
        here = [x for x in (a, b) if re.search(r"(?<![\d.])%d(?![\d.])" % x, t)]
        if m_list:
            N = int(m_list.group(1))
            lists[N] = ints(m_list.group(2))
            fig = table(wrap(lists[N]), note="The factors of %d" % N)
        elif m_both and a in lists and b in lists:
            common = ints(m_both.group(1))
            note = "In both lists: %s. The biggest is %d" % (join_and(common), max(common))
            fig = [factor_venn(a, b, [x for x in lists[a] if x not in common], common,
                               [x for x in lists[b] if x not in common], note, ["both"]),
                   table(wrap(common), note=note)]
            last = fig
        elif lists and ("not divide" in t or "does divide" in t):
            src = list(lists)[0]
            tgt = b if src == a else a
            no = re.search(r"((?:\d+(?:, | and )?)+) (?:do|does) not divide", t)
            yes = re.search(r"(\d+),? does divide", t)
            if no:
                rows += [[str(x), "no"] for x in ints(no.group(1))]
            if yes:
                rows.append([yes.group(1), "yes"])
            shown = rows[-6:]
            if shown:
                fig = table(shown, headers=["Factor of %d" % src, "Divides %d?" % tgt],
                            hl=["r%d" % (len(shown) - 1)] if yes else None,
                            note=("%s is the biggest factor of %d that divides %d" % (yes.group(1), src, tgt)) if yes
                            else "Try the factors of %d on %d, biggest first" % (src, tgt))
                if yes:
                    last = fig
        elif m_mult and all(int(x[0]) in (a, b) for x in m_mult):
            for N, p, r in m_mult:
                mult[int(N)] = (int(p), int(r))
            if len(m_mult) == 1:
                N, p, r = [int(x) for x in m_mult[0]]
                if is_prime(p) and is_prime(r):
                    fig = tree(N, note="%d = %d × %d" % (N, p, r))
        elif m_share:
            shared = ints(m_share.group(1))
            fig = venn(str(a), str(b), "…", times(shared), "…", "Shared prime factors: %s" % join_and(shared), ["both"])
            last = fig
        elif re.search(r"in both|share|contain", t) and g in stated(q, i):
            note = "Both numbers have %d in them, and nothing bigger. HCF = %d" % (g, g)
            cands = []
            if a in mult and b in mult:
                cands.append(venn("%d = %d × %d" % ((a,) + mult[a]), "%d = %d × %d" % ((b,) + mult[b]),
                                  str(a // g), str(g), str(b // g), note, ["both"]))
            cands.append(venn(str(a), str(b), str(a // g), str(g), str(b // g), note, ["both"]))
            cands.append(venn(str(a), str(b), "…", str(g), "…", note, ["both"]))
            fig = cands
            last = cands
        elif len(here) == 1 and re.search(r"prime factors|divides %d exactly" % here[0], t):
            fig = tree(here[0], note="Break %d into prime factors" % here[0])
        if fig is None and i == count - 1 and last is not None and g in stated(q, i):
            cands = last if isinstance(last, list) else [last]
            fig = [with_note(c, "The HCF of %d and %d is %d" % (a, b, g), c.get("highlight")) for c in cands if c]
        out.append(fig)
    return out


# ── Rule: the LCM of two numbers ─────────────────────────────────────────────

def lcm_before(a, b):
    return table([[str(a), "?", "?", "…"], [str(b), "?", "?", "…"]],
                 note="Count on in %ds and in %ds. LCM = the first number in both rows" % (a, b))


def lcm_step_figures(q, a, b):
    out = []
    mults, rows = None, []
    own, pieces, wide, small = None, None, False, None
    for i, s in enumerate(steps_of(q)):
        t = s.get("text", "")
        fig = None
        m_prod = re.search(r"LCM × HCF = (\d+) × (\d+) = (\d+)", t)
        m_div = re.search(r"= (\d+), so LCM = (\d+) ÷ (\d+) = (\d+)", t)
        m_big = re.search(r"multiples of the bigger number, (\d+): ([\d, and]+?)\.", t)
        m_own = re.search(r"multiples of the bigger number, (\d+)\. The first one is \1 itself", t)
        m_row = re.search(r"multiples of (\d+): ([\d, ]+)\.", t)
        m_first = re.search(r"first number that is in both lists is (\d+)", t)
        m_lcm = re.search(r"(?:The LCM is|the LCM of \d+ and \d+ is) (\d+)", t)
        if m_own:
            # the bigger number is itself a multiple of the smaller one: show it built from the smaller number
            big = int(m_own.group(1))
            small = a if big == b else b
            own = big
            fig = with_note({"kind": "barModel", "bars": [{"label": str(big), "segments": [{"units": 12, "label": str(big), "tone": "a"}]}]},
                            "The first multiple of %d is %d itself. Does %d go into it?" % (big, big, small))
        elif own and re.search(r"%d × (\d+) = %d" % (small, own), t):
            times_ = int(re.search(r"%d × (\d+) = %d" % (small, own), t).group(1))
            pieces = {"kind": "barModel", "bars": [
                {"label": str(own), "segments": [{"units": 12, "label": str(own), "tone": "a"}]},
                {"label": "%ds" % small, "segments": [{"units": 12.0 / times_, "label": str(small), "tone": "b"}] * times_}]}
            fig = with_note(pieces, "%d goes into %d exactly: %d × %d = %d" % (small, own, small, times_, own), ["b1"])
        elif own and pieces and m_lcm:
            fig = with_note(pieces, "%d is a multiple of both, and nothing smaller is: the LCM" % own, ["b0"])
        elif m_prod:
            fig = balance("HCF × LCM", "%d × %d" % (a, b),
                          "HCF × LCM is the same as %d × %d = %s" % (a, b, m_prod.group(3)))
        elif m_div:
            h, product, _, l = m_div.groups()
            fig = balance("%s × %s" % (h, l), "%d × %d" % (a, b),
                          "The HCF is %s, so the LCM is %s ÷ %s = %s" % (h, product, h, l), ["left"])
        elif m_big:
            big = int(m_big.group(1))
            small = a if big == b else b
            mults = [str(x) for x in ints(m_big.group(2))]
            wide = len(mults) > 5   # too many for one row of headings: set the multiples out in rows instead
            if wide:
                fig = table(wrap(mults), note="Multiples of %d. Which is the first that %d goes into exactly?" % (big, small))
            else:
                fig = table([["?"] * len(mults)], headers=mults,
                            note="Multiples of %d. Which is the first that %d goes into exactly?" % (big, small))
        elif mults and re.search(r"÷ %d = \d+|%d × \d+ = %s(?!\d)" % (small, small, mults[-1]), t):
            said = "Does %d go into it exactly? %s is the first that works" % (small, mults[-1])
            if wide:
                rows_ = wrap(mults)
                fig = table(rows_, note="%d goes into %s exactly, and into none before it" % (small, mults[-1]), hl=["r%d" % (len(rows_) - 1)])
            else:
                fig = table([["no"] * (len(mults) - 1) + ["yes"]], headers=mults, note=said)
        elif mults and m_lcm:
            if wide:
                fig = table(wrap(mults), note="The LCM of %d and %d is %s" % (a, b, m_lcm.group(1)))
            else:
                fig = table([["no"] * (len(mults) - 1) + ["yes"]], headers=mults, hl=["r0"],
                            note="The LCM of %d and %d is %s" % (a, b, m_lcm.group(1)))
        elif m_row:
            rows.append([str(x) for x in ints(m_row.group(2))])
            width = max(len(r) for r in rows)
            padded = [r + ["…"] * (width - len(r)) for r in rows]
            fig = table(padded, hl=["r%d" % (len(rows) - 1)], note="Multiples of %s" % m_row.group(1))
        elif rows and m_first:
            width = max(len(r) for r in rows)
            padded = [r + ["…"] * (width - len(r)) for r in rows]
            fig = table(padded, note="%s is the first number in both rows: the LCM" % m_first.group(1))
        out.append(fig)
    return out


BARE = re.compile(r"^(?:Find the |The )?(H\.?C\.?F\.?|L\.?C\.?M\.?) of (\d+) and (\d+)(?: is:|[.?])?$")
for qid in P.ids():
    m = BARE.match(Q[qid]["questionText"].strip())
    if not m or qid in ("EXT_G4_FP_2020_020", "Q_CH06_005", "PYQ_2017_Q19"):
        continue
    a, b = int(m.group(2)), int(m.group(3))
    if m.group(1).startswith("H"):
        P.add(qid, hcf_before(a, b), hcf_step_figures(Q[qid], a, b))
    else:
        P.add(qid, lcm_before(a, b), lcm_step_figures(Q[qid], a, b))


# ── Rule: factor pairs ("How many factors does N have?") ─────────────────────

def pairs_before(N):
    return table([["1", "×", str(N)], ["?", "×", "?"]], note="Find every pair of numbers that multiply to %d" % N)


def pairs_step_figures(q, N):
    found, out = [], []
    count = len(steps_of(q))
    for i, s in enumerate(steps_of(q)):
        t = s.get("text", "")
        new = []
        for x, y in re.findall(r"(\d+) × (\d+)", t):
            x, y = int(x), int(y)
            if x * y == N and x <= y and (x, y) not in found and (x, y) not in new:
                new.append((x, y))
        found = sorted(found + new)
        cells = ["%d × %d" % p for p in found]
        fig = None
        if new:
            fig = table(wrap(cells, 4), note="Factor pairs of %d found so far" % N)
        elif i == count - 1 and found:
            fig = table(wrap(cells, 4), note="Every factor pair of %d. Count each different number once" % N)
        out.append(fig)
    return out


for qid in P.ids():
    m = re.match(r"^How many factors does (\d+) have\?$", Q[qid]["questionText"].strip())
    if m:
        N = int(m.group(1))
        P.add(qid, pairs_before(N), pairs_step_figures(Q[qid], N))


# ── Rule: "How many numbers from A to B are divisible by k?" ─────────────────

def range_count(qid):
    q = Q[qid]
    m = re.match(r"^How many numbers from (\d+) to (\d+) are divisible by (\d+)\?$", q["questionText"].strip())
    if not m:
        return
    lo, hi, k = [int(x) for x in m.groups()]
    first = -(-lo // k) * k
    last = hi // k * k
    span = hi - lo

    def line(points, hops=None, note=None, hl=None):
        return number_line(lo, hi, span, "ends", [{"at": p, "label": str(p)} for p in points], hops, note, hl)

    before = line([], note="How many multiples of %d are on this line, from %d to %d?" % (k, lo, hi))
    figs = {}
    m1, m2 = first // k, last // k
    jumps = m2 - m1
    answer = jumps + 1
    seen_first = seen_last = counted = False
    for i, s in enumerate(steps_of(q)):
        t = s.get("text", "")
        if not seen_first and re.search(r"first multiple of %d" % k, t, re.I) and first in stated(q, i):
            figs[i] = line([first], note="The first multiple of %d on the line is %d × %d = %d" % (k, k, m1, first), hl=["p0"])
            seen_first = True
        elif seen_first and not seen_last and last in stated(q, i):
            figs[i] = line([first, last], note="The last multiple of %d on the line is %d × %d = %d" % (k, k, m2, last), hl=["p1"])
            seen_last = True
        elif seen_last and not counted and answer in stated(q, i):
            if jumps in stated(q, i):   # the step itself counts the jumps (an answer choice with that number does not count)
                figs[i] = line([first, last], [{"from": first, "to": last, "label": "%d jumps of %d" % (jumps, k)}],
                               "%d × %d up to %d × %d: %d jumps, and the first one too: %d" % (k, m1, k, m2, jumps, answer), ["h0"])
            else:
                figs[i] = line([first, last], [{"from": first, "to": last, "label": "jumps of %d" % k}],
                               "%d × %d, and so on up to %d × %d: %d multiples" % (k, m1, k, m2, answer), ["h0"])
            counted = True
        elif counted and answer in stated(q, i):
            figs[i] = line([first, last], [{"from": first, "to": last, "label": "jumps of %d" % k}],
                           "%d multiples of %d from %d to %d" % (answer, k, lo, hi))
    P.add(qid, before, figs)


for qid in P.ids("PH3_"):
    range_count(qid)


# ── Rule: prime factors of two numbers in two circles (LCM and HCF together) ─

def prime_venn(qid):
    q = Q[qid]
    nums_q = ints(q["questionText"])
    a, b = nums_q[-2], nums_q[-1]
    before = venn(str(a), str(b), "?", "?", "?",
                  "Sort the prime factors of %d and %d. Shared ones go in the middle" % (a, b))
    figs = {}
    base = None
    g, l = math.gcd(a, b), a * b // math.gcd(a, b)
    for i, s in enumerate(steps_of(q)):
        t = s.get("text", "")
        both = re.search(r"(\d+) = ((?:\d+ × )+\d+) and (\d+) = ((?:\d+ × )+\d+)", t)
        if both and int(both.group(1)) == a and int(both.group(3)) == b:
            fa, fb = ints(both.group(2)), ints(both.group(4))
            common = []
            rest_b = list(fb)
            rest_a = []
            for p in fa:
                if p in rest_b:
                    rest_b.remove(p)
                    common.append(p)
                else:
                    rest_a.append(p)
            base = venn(str(a), str(b), times(rest_a) or "–", times(common), times(rest_b) or "–")
            if g in stated(q, i):
                shared = times(common) if len(common) == 1 else "%s = %d" % (times(common), g)
                figs[i] = with_note(base, "The middle is shared by both numbers: %s, the HCF" % shared, ["both"])
            else:
                figs[i] = with_note(base, "The prime factors of %d and %d, with the shared ones in the middle" % (a, b))
        elif base and re.search(r"HCF is|They share", t) and g in stated(q, i):
            figs[i] = with_note(base, "The middle is shared by both numbers: its product is %d, the HCF" % g, ["both"])
        elif base and re.search(r"For the LCM|The LCM needs", t):
            figs[i] = [with_note(base, "LCM = everything in the picture multiplied together: %d" % l, ["left", "both", "right"]),
                       with_note(base, "LCM = everything in the picture multiplied together", ["left", "both", "right"])]
    P.add(qid, before, figs, origin="authored")


for qid in ("EXT_G4_FP_2021_040", "EXT_G4_FP_2022_034", "EXT_G4_FP_2023_005", "EXT_G4_FP_2025_040", "EXT_G4_FP_2024_010"):
    prime_venn(qid)


# ── Rule: HCF × LCM = product of the two numbers ─────────────────────────────

def product_rule(qid, h, l, x):
    q = Q[qid]
    other = h * l // x
    figs = {0: balance("%d × %d" % (h, l), "%d × ?" % x, "HCF × LCM = one number × the other number"),
            len(steps_of(q)) - 1: balance("%d × %d" % (h, l), "%d × %d" % (x, other),
                                          "The other number is %d" % other, ["right"])}
    P.add(qid, None, figs)


_n = ints(Q["EXT_G4_FP_2022_003"]["questionText"])
product_rule("EXT_G4_FP_2022_003", _n[0], _n[1], _n[2])
_n = ints(Q["EXT_G4_FP_2023_027"]["questionText"])
product_rule("EXT_G4_FP_2023_027", _n[1], _n[0], _n[2])
_n = ints(Q["Q_CH06_021"]["questionText"])
product_rule("Q_CH06_021", _n[0], _n[1], _n[2])


# ═════════════════════════════════════════════════════════════════════════════
# Individually drawn
# ═════════════════════════════════════════════════════════════════════════════

def A(qid, figure=None, steps=None, **kw):
    P.add(qid, figure, steps, origin="authored", **kw)


def bars(*rows, **kw):
    """rows: (label, [(units, label, tone)...]). Units are scaled so the longest bar is 12."""
    biggest = max(sum(u for u, _, _ in segs) for _, segs in rows)
    out = []
    for label, segs in rows:
        out.append({"label": label, "segments": [{"units": round(max(0.2, u * 12.0 / biggest), 3), "label": lab, "tone": tone}
                                                 for u, lab, tone in segs]})
    return with_note({"kind": "barModel", "bars": out}, kw.get("note"), kw.get("hl"))


# HCF and LCM, one at a time
A("EXT_G4_FP_2020_020", hcf_before(24, 72), {
    0: bars(("72", [(24, "24", "a")] * 3), ("24", [(24, "24", "b")]), note="24 fits into 72 exactly, with nothing left over"),
    2: venn("Factors of 24", "Factors of 72", "–", "1, …, 24", "…, 72", "24 divides both, and nothing bigger divides 24", ["both"]),
})
A("Q_CH06_005", hcf_before(12, 18), hcf_step_figures(Q["Q_CH06_005"], 12, 18))
A("Q_CH06_009", None, {
    2: venn("Factors of 9", "Factors of 16", "3, 9", "1", "2, 4, 8, 16", "Only 1 is in both lists", ["both"]),
    3: venn("Factors of 9", "Factors of 16", "3, 9", "1", "2, 4, 8, 16", "9 and 16 share no factor except 1: co-prime", ["both"]),
})
A("Q_CH06_011", None, {
    2: {"kind": "rectangle", "square": True, "grid": {"cols": 2, "rows": 2},
        "note": "2 × 2 = 4, so 4 has three factors: 1, 2 and 4"},
})
A("PYQ_2017_Q19", lcm_before(48, 54), {
    0: venn("48 = 6 × 8", "54 = 6 × 9", "8", "6", "9", "6 is in both numbers. 8 and 9 are the parts left over", ["both"]),
    1: venn("48 = 6 × 8", "54 = 6 × 9", "8", "6", "9", "LCM = 6 × 8 × 9, using the shared 6 only once", ["left", "both", "right"]),
    2: venn("48 = 6 × 8", "54 = 6 × 9", "8", "6", "9", "6 × 8 × 9 = 432, and both 48 and 54 divide it"),
})
A("PYQ_2018_Q30", hcf_before(24, 32), {
    0: table(wrap([1, 2, 3, 4, 6, 8, 12, 24], 4), note="Factors of 24. The biggest one that also divides 32 is 8"),
    1: table([["no", "no", "yes"]], headers=["32", "64", "96"], note="Multiples of 32. Does 24 divide it exactly? 96 works first"),
    2: balance("HCF + LCM", "8 + 96", "8 + 96 = 104", ["right"]),
})
A("G4A_FACTORS_006", venn("Factors of 12", "Factors of 20", "…", "?", "…", "A common factor belongs in the middle"), {
    2: venn("Factors of 12", "Factors of 20", "…", "4", "…", "4 divides both 12 and 20, so it goes in the middle", ["both"]),
})
A("Q_CH06_020", table([["4", "?", "?", "…"], ["6", "?", "?", "…"]],
                      note="Count on in 4s and in 6s. Which numbers land in both rows?"), {
    0: table(wrap([4, 8, 12, 16, 20, 24, 28, 32, 36]), note="Multiples of 4"),
    1: table(wrap([6, 12, 18, 24, 30, 36]), note="Multiples of 6"),
    3: table([["12", "24", "36"]], note="These three numbers are in both lists"),
})

# Factor pairs
A("G4A_FACTORS_004", pairs_before(18), {
    0: table([["1 × 18"]], note="Factor pairs of 18 found so far"),
    1: table([["1 × 18", "2 × 9"]], note="Factor pairs of 18 found so far"),
    2: table([["1 × 18", "2 × 9", "3 × 6"]], note="4 and 5 do not divide 18, so these are all the pairs"),
    3: table([["1 × 18", "2 × 9", "3 × 6"]], note="Six factors: 1, 2, 3, 6, 9, 18"),
}, uses_options=True)
A("G4A_FACTORS_013", pairs_before(48), {
    0: table(wrap(["1 × 48", "2 × 24", "3 × 16", "4 × 12", "6 × 8"], 3), note="The factor pairs of 48"),
    2: table(wrap(["1 × 48", "2 × 24", "3 × 16", "4 × 12", "6 × 8"], 3), note="10 factors in all. Only 1 and 3 are odd"),
})
A("PYQ_2016_Q03", table([["1", "×", "98"], ["?", "×", "?"]], note="How many pairs of numbers multiply to 98?"),
  pairs_step_figures(Q["PYQ_2016_Q03"], 98))
A("PYQ_2019_Q22", table([["1", "×", "136"], ["?", "×", "?"]], note="How many pairs of numbers multiply to 136?"),
  pairs_step_figures(Q["PYQ_2019_Q22"], 136))
A("G4A_FACTORS_001", None, {
    2: {"kind": "rectangle", "grid": {"cols": 9, "rows": 4}, "proportion": 2.25,
        "note": "4 rows of 9 make 36 exactly, so 9 is a factor of 36"},
})

# Factor trees
A("Q_CH06_007", tree(60, 0, "Split 60 again and again until every part is prime"), {
    0: tree(60, 1, "60 = 2 × 30"),
    1: tree(60, None, "30 = 2 × 15, and then 15 = 3 × 5"),
    2: tree(60, None, "Every circled number is prime: 2 × 2 × 3 × 5", ["primes"]),
})
A("G4A_FACTORS_015", tree(84, 0, "Split 84 until every part is prime. Which prime is the greatest?"), {
    0: tree(84, 1, "Start by splitting 84 into two smaller factors"),
    1: tree(84, None, "Keep splitting until all the parts are prime"),
    2: tree(84, None, "The prime factors are 2, 3 and 7. The greatest is 7", ["primes"]),
})
A("PYQ_2017_Q06", None, {
    0: tree(90, None, "The prime factors of 90", ["primes"]),
    3: table([["3", "5", "6"]], note="The three dice. 3 × 5 × 6 = 90"),
})

# Measuring and packing with the HCF
A("G4A_FACTORS_008", {"kind": "rectangle", "length": "60 cm", "breadth": "48 cm", "proportion": 1.25,
                      "note": "Equal square tiles, no cutting. Biggest tile side = ?"}, {
    0: {"kind": "rectangle", "length": "60 cm", "breadth": "48 cm", "proportion": 1.25,
        "highlight": ["length", "breadth"], "note": "The tile side must divide both 48 and 60 exactly"},
    1: table(wrap([1, 2, 3, 4, 6, 12], 3), note="Tile sides that fit both 48 cm and 60 cm"),
    3: [{"kind": "rectangle", "length": "60 cm", "breadth": "48 cm", "proportion": 1.25, "grid": {"cols": 5, "rows": 4},
         "note": "Tiles of side 12 cm cover the panel exactly"},
        {"kind": "rectangle", "length": "60 cm", "breadth": "48 cm", "proportion": 1.25, "inside": "12 cm tiles",
         "highlight": ["fill"], "note": "12 cm is the biggest side that fits both ways exactly"}],
})
_f84 = [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84]
A("PYQ_2018_Q01", bars(("Ribbon 1", [(84, "84 m", "a")]), ("Ribbon 2", [(108, "108 m", "b")]),
                       note="Cut both into equal pieces, as long as possible, nothing left over"), {
    0: bars(("Ribbon 1", [(84, "84 m", "a")]), ("Ribbon 2", [(108, "108 m", "b")]),
            note="The piece length must divide both 84 and 108 exactly"),
    1: table(wrap(_f84, 4), note="The factors of 84"),
    2: bars(("Ribbon 1", [(84, "84 m", "a")]), ("Ribbon 2", [(12, "12", "b")] * 9), hl=["b1"],
            note="12 is the biggest factor of 84 that divides 108: 9 pieces"),
    3: bars(("Ribbon 1", [(12, "12", "a")] * 7), ("Ribbon 2", [(12, "12", "b")] * 9),
            note="Both ribbons cut into pieces of 12 metres: 7 pieces and 9 pieces"),
})
A("Q_CH06_014", bars(("Apples", [(48, "48", "a")]), ("Oranges", [(36, "36", "b")]),
                     note="Same number of fruits in every box, as many as possible"), {
    0: bars(("Apples", [(48, "48", "a")]), ("Oranges", [(36, "36", "b")]),
            note="The number in a box must divide both 48 and 36 exactly"),
    1: table(wrap([1, 2, 3, 4, 6, 9, 12, 18, 36]), note="Factors of 36. Test them on 48, biggest first: 12 works"),
    2: bars(("Apples", [(12, "12", "a")] * 4), ("Oranges", [(12, "12", "b")] * 3),
            note="4 boxes of 12 apples and 3 boxes of 12 oranges"),
})

# Things that happen together again (LCM)
A("Q_CH06_013", clock(9, 0, "Both bells ring now. One rings every 12 minutes, the other every 18"), {
    0: table([["Bell 1", "12", "24", "36", "48"], ["Bell 2", "18", "36", "54", "…"]],
             note="Minutes after 9:00 when each bell rings"),
    1: table([["Bell 1", "12", "24", "36", "48"], ["Bell 2", "18", "36", "54", "…"]],
             note="36 is the first number in both rows"),
    2: clock(9, 36, "36 minutes after 9:00 is 9:36", ["minute"]),
})
A("G4A_FACTORS_018", clock(6, 0, "Both buses leave now. Pune: every 15 minutes. Nashik: every 20 minutes"), {
    0: table([["no", "no", "yes"]], headers=["20", "40", "60"], note="Multiples of 20. Does 15 divide it exactly?"),
    2: table([["6:00", "7:00", "8:00", "9:00", "10:00"]], note="The times when both buses leave together"),
    3: table([["6:00", "7:00", "8:00", "9:00", "10:00"]], note="Count the times, with 6:00 and 10:00 included: 5"),
})
A("G4A_FACTORS_024", table([["Pune", "7:00", "12 minutes"], ["Nashik", "7:06", "18 minutes"]],
                           headers=["Bus to", "First bus", "Then every"], note="When do two buses first leave at the same moment?"), {
    0: table([["Pune", "7:00", "7:12", "7:24", "7:36"]], note="Pune buses: add 12 minutes each time"),
    1: table([["Pune", "7:00", "7:12", "7:24", "7:36"], ["Nashik", "7:06", "7:24", "7:42", "…"]], hl=["r1"],
             note="Nashik buses: add 18 minutes each time"),
    3: table([["Pune", "7:00", "7:12", "7:24", "7:36"], ["Nashik", "7:06", "7:24", "7:42", "…"]],
             note="7:24 is the first time that is in both rows"),
})
A("G4A_FACTORS_007", None, {
    1: table([["no", "no", "no", "?"]], headers=["9", "18", "27", "36"], note="Multiples of 9. Does 4 divide it exactly?"),
    2: table([["no", "no", "no", "yes"]], headers=["9", "18", "27", "36"], note="4 and 6 both divide 36"),
    3: table([["no", "no", "no", "yes"]], headers=["9", "18", "27", "36"], hl=["r0"],
             note="All three lights blink together again after 36 seconds"),
})
A("EXT_G4_FP_2020_036", None, {
    2: number_line(0, 120, 24, "all", [{"at": x} for x in (24, 48, 72, 96)],
                   note="24, 48, 72 and 96 have two digits. 120 has three", hl=["p0", "p1", "p2", "p3"]),
})
A("Q_CH01_026", None, {
    2: number_line(0, 72, 9, "ends", [{"at": 72, "label": "8th"}], note="8 jumps of 9 from 0 land on 72", hl=["p0"]),
})

# Counting multiples with two circles
A("G4A_FACTORS_017", venn("Anu: every 3rd", "Biju: every 4th", "?", "?", "?",
                          "50 steps in all. How many are outside both circles?"), {
    0: venn("Anu: every 3rd", "Biju: every 4th", "?", "?", "?", "Anu's whole circle holds 16 steps", ["left", "both"]),
    1: venn("Anu: every 3rd", "Biju: every 4th", "16 − 4", "4", "12 − 4",
            "Biju's circle holds 12. The 4 multiples of 12 are in both", ["both"]),
    2: venn("Anu: every 3rd", "Biju: every 4th", "16 − 4", "4", "12 − 4",
            "Inside the circles: 16 + 12 − 4 steps", ["left", "both", "right"]),
    3: venn("Anu: every 3rd", "Biju: every 4th", "16 − 4", "4", "12 − 4", "Of the 50 steps, 26 are outside both circles"),
})
A("G4A_FACTORS_030", venn("Multiples of 4", "Multiples of 6", "?", "…", "…",
                          "Numbers from 1 to 100. How many belong only in the left part?"), {
    0: venn("Multiples of 4", "Multiples of 6", "?", "…", "…", "First count the whole Multiples of 4 circle", ["left", "both"]),
    1: venn("Multiples of 4", "Multiples of 6", "?", "12, 24, … 96", "…", "The middle holds the multiples of 12", ["both"]),
    2: venn("Multiples of 4", "Multiples of 6", "?", "12, 24, … 96", "…", "Take the middle away from the Multiples of 4 circle", ["left"]),
    3: venn("Multiples of 4", "Multiples of 6", "17", "12, 24, … 96", "…", "17 numbers are multiples of 4 but not of 6", ["left"]),
})
A("PYQ_2019_Q35", venn("Multiples of 4", "Multiples of 5", "…", "?", "…", "Numbers up to 100. How many go in the middle?"), {
    0: venn("Multiples of 4", "Multiples of 5", "…", "20, …", "…", "20 is the smallest number in both notebooks", ["both"]),
    1: venn("Multiples of 4", "Multiples of 5", "…", "20, 40, … 100", "…", "Every common number is a multiple of 20", ["both"]),
    2: venn("Multiples of 4", "Multiples of 5", "…", "20, 40, … 100", "…", "20, 40, 60, 80, 100: 5 numbers in the middle", ["both"]),
})

# Prime numbers
_primes50 = [x for x in range(2, 51) if is_prime(x)]


def _cell(x):
    return [(x - 1) // 10, (x - 1) % 10]


A("Q_CH06_025", {"kind": "grid", "rows": 5, "cols": 10, "note": "The numbers 1 to 50 in rows of 10, before any are crossed out"}, {
    0: {"kind": "grid", "rows": 5, "cols": 10, "shaded": [_cell(x) for x in (2, 3, 5, 7)],
        "note": "Keep 2, 3, 5 and 7. Cross out all their other multiples"},
    1: {"kind": "grid", "rows": 5, "cols": 10, "shaded": [_cell(x) for x in _primes50],
        "note": "Shaded squares are the numbers left. Every composite number is gone"},
    2: {"kind": "grid", "rows": 5, "cols": 10, "shaded": [_cell(x) for x in _primes50],
        "note": "The numbers left up to 50 are all prime numbers"},
})
A("Q_CH06_023", number_line(10, 20, 1, "all", note="Which of the numbers between 10 and 20 are prime?"), {
    0: number_line(10, 20, 1, "all", [{"at": 11}, {"at": 19}], note="Look at the numbers from 11 to 19"),
    2: number_line(10, 20, 1, "all", [{"at": x} for x in (11, 13, 17, 19)], note="11, 13, 17 and 19 are prime",
                   hl=["p0", "p1", "p2", "p3"]),
    3: number_line(10, 20, 1, "all", [{"at": x} for x in (11, 13, 17, 19)], note="Count the dots: 4 prime numbers"),
})
A("PYQ_2016_Q06", None, {
    2: number_line(20, 29, 1, "all", [{"at": 23}, {"at": 29}], note="From 20 to 29, only 23 and 29 are prime", hl=["p0", "p1"]),
})
A("PYQ_2019_Q04", None, {
    1: number_line(20, 29, 1, "all", [{"at": 23}, {"at": 29}], note="From 20 to 29, only 23 and 29 are prime", hl=["p0", "p1"]),
})

# Divisibility tests on the digits
A("Q_CH06_010", place("4518"), {
    0: place("4518", "For 9, add up all the digits of the number"),
    1: place("4518", "4 + 5 + 1 + 8 = 18", ["d0", "d1", "d2", "d3"]),
    2: place("4518", "The digit sum is 18, and 18 ÷ 9 = 2 exactly"),
    3: place("4518", "Yes: 9 divides 4,518, and its digit sum is 18"),
})
A("Q_CH06_012", place("8294"), {
    0: place("8294", "1st and 3rd places: 8 + 9 = 17", ["d0", "d2"]),
    1: place("8294", "2nd and 4th places: 2 + 4 = 6", ["d1", "d3"]),
    2: place("8294", "17 − 6 = 11, so 11 divides 8,294"),
})
A("G4A_FACTORS_016", place("4729"), {
    0: place("4729", "Add the four digits", ["d0", "d1", "d2", "d3"]),
    1: place("4729", "The digits add up to 22. The multiple of 9 just below is 18"),
    2: place("4725", "Take away 4 to get 4,725, which 9 divides", ["d3"]),
})
A("EXT_G4_FP_2021_020", place("73251"), {
    0: place("73251", "Test for 3: add all the digits", ["d0", "d1", "d2", "d3", "d4"]),
    2: place("73251", "Only the 2 is even, so the 2 must move to the end", ["d2", "d4"]),
    3: place("73152", "Swap the 2 and the 1 to get 73152", ["d2", "d4"]),
})
A("PYQ_2019_Q12", place("73251"), {
    0: place("73251", "The digits add up to 18, so 3 divides it", ["d0", "d1", "d2", "d3", "d4"]),
    2: place("73251", "Only the 2 is even, so the 2 must move to the ones place", ["d2", "d4"]),
    3: place("73152", "Swap the 2 and the 1 to get 73152", ["d2", "d4"]),
})

PLACES4 = ["Thousands", "Hundreds", "Tens", "Ones"]
A("EXT_G4_FP_2020_040", table([["2", "★", "1", "★"]], headers=PLACES4,
                              note="Both stars are the same digit. 11 divides the number"), {
    0: table([["1st and 3rd", "2 + 1"]], headers=["Places", "Digits added"], note="Add the 1st and 3rd digits"),
    1: table([["1st and 3rd", "2 + 1"], ["2nd and 4th", "★ + ★"]], headers=["Places", "Digits added"], hl=["r1"],
             note="★ + ★ is double a digit, so it is even. It cannot be 3"),
    2: table([["1st and 3rd", "2 + 1"], ["2nd and 4th", "★ + ★ = 3 + 11"]], headers=["Places", "Digits added"], hl=["r1"],
             note="So the two sums must differ by 11"),
    4: table([["2", "7", "1", "7"]], headers=PLACES4, note="Check the number 2717"),
})
A("EXT_G4_FP_2022_036", table([["9", "★", "3", "★"]], headers=PLACES4,
                              note="Both stars are the same digit. 11 divides the number"), {
    1: table([["1st and 3rd", "9 + 3"], ["2nd and 4th", "★ + ★"]], headers=["Places", "Digits added"], hl=["r0"],
             note="For 11, the two sums must be equal, or differ by 11"),
    2: table([["1st and 3rd", "9 + 3 = 12"], ["2nd and 4th", "6 + 6 = 12"]], headers=["Places", "Digits added"], hl=["r1"],
             note="The two stars add to 12, so each star is 6"),
    4: table([["9", "6", "3", "6"]], headers=PLACES4, note="The digit is 6, which is not 4, 5 or 7"),
})
A("EXT_G4_FP_2024_021", table([["A", "5", "9"], ["5", "B", "2"], ["6", "C", "9"]],
                              note="Each row is a number that 9 divides. Find A, B and C"), {
    0: table([["4", "5", "9"], ["5", "B", "2"], ["6", "C", "9"]], hl=["r0"], note="5 + 9 = 14. The next multiple of 9 is 18, so A is 4"),
    1: table([["4", "5", "9"], ["5", "2", "2"], ["6", "C", "9"]], hl=["r1"], note="5 + 2 = 7. The next multiple of 9 is 9, so B is 2"),
    2: table([["4", "5", "9"], ["5", "2", "2"], ["6", "3", "9"]], hl=["r2"], note="6 + 9 = 15. The next multiple of 9 is 18, so C is 3"),
    4: table([["4", "2", "3"]], note="Odd, and as big as it can be: 423"),
})
A("EXT_G4_FP_2023_018", table([["1", "A", "9", "A", "5"]], note="Both A's are the same digit. 7 divides the number"), {
    1: table([["1", "4", "9", "4", "5"]], note="With 4 in both blanks the number is 14945"),
    4: table([["1", "4", "9", "4", "5"]], note="14945 is divisible by 7, so A is 4"),
}, uses_options=False)
A("G4A_FACTORS_010", table([["7", "?", "4"]], headers=["Hundreds", "Tens", "Ones"],
                           note="Smallest digit for ? so that 3 divides the number"), {
    1: table([["7", "?", "4"]], headers=["Hundreds", "Tens", "Ones"], note="Add the digits you know: 7 and 4"),
    2: table([["7", "?", "4"]], headers=["Hundreds", "Tens", "Ones"], note="The next multiple of 3 is 12. It needs 1 more"),
    3: table([["7", "1", "4"]], headers=["Hundreds", "Tens", "Ones"], note="The smallest digit is 1, giving 714"),
})
A("PYQ_2016_Q13", table([["5", "★", "7"], ["5", "7", "♥"], ["Ψ", "5", "9"]],
                        note="11 divides all three numbers. Find ★, ♥ and Ψ"), {
    0: table([["5", "★", "7"], ["5", "7", "♥"], ["Ψ", "5", "9"]],
             note="First digit + last digit − middle digit must come to 0 or 11"),
    1: table([["5", "1", "7"], ["5", "7", "♥"], ["Ψ", "5", "9"]], hl=["r0"], note="5 + 7 = 12, so ★ must be 1 to leave 11"),
    2: table([["5", "1", "7"], ["5", "7", "2"], ["Ψ", "5", "9"]], hl=["r1"], note="5 plus ♥ must equal 7, so ♥ is 2"),
    3: table([["5", "1", "7"], ["5", "7", "2"], ["7", "5", "9"]], hl=["r2"], note="Ψ plus 9 less 5 must come to 11, so Ψ is 7"),
    4: table([["7", "2", "1"]], note="Biggest digit first: 721"),
})
A("PYQ_2018_Q16", table([["8", "★", "2", "★"]], headers=PLACES4, note="Both stars are the same digit. 9 divides the number"), {
    0: table([["8", "★", "2", "★"]], headers=PLACES4, note="The digits you know: 8 + 2 = 10"),
    1: table([["8", "★", "2", "★"]], headers=PLACES4, note="★ + ★ must lift 10 up to 18 or to 27"),
    2: table([["8", "★", "2", "★"]], headers=PLACES4, note="★ + ★ is even, so it is 8. Each star is 4"),
    3: table([["8", "4", "2", "4"]], headers=PLACES4, note="8 + 4 + 2 + 4 = 18, a multiple of 9"),
})
A("PYQ_2019_Q21", table([["9", "★", "8", "★"]], headers=PLACES4, note="Both stars are the same digit. 9 divides the number"), {
    0: table([["9", "★", "8", "★"]], headers=PLACES4, note="The digits you know: 9 + 8 = 17"),
    1: table([["9", "★", "8", "★"]], headers=PLACES4, note="★ + ★ must lift 17 up to 18, 27 or 36"),
    2: table([["9", "★", "8", "★"]], headers=PLACES4, note="★ + ★ is even, so it is 10. Each star is 5"),
    3: table([["9", "5", "8", "5"]], headers=PLACES4, note="9 + 5 + 8 + 5 = 27, a multiple of 9"),
})

P.save()
