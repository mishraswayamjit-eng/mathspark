"""Figures for Grade 4 ratio and proportion (node gr4_ratio).

    python -X utf8 scripts/figures/authoring/g4_gr4_ratio.py            # write the part file, print counts
    python -X utf8 scripts/figures/authoring/g4_gr4_ratio.py all        # also print every entry for review
    python -X utf8 scripts/figures/authoring/g4_gr4_ratio.py <text>     # print entries whose id or rule matches

Writes data/question-figures/parts/g4-gr4_ratio.json.
Generated families are drawn by the rules below; the rest are in g4_gr4_ratio_own.py.
"""
import re
import sys

from g4_gr4_fractions_lib import Q, bar, bm, entry, load, report, seg, segs, table, write
from g4_gr4_ratio_own import OWN

NODE = "gr4_ratio"
RULES = []


def rule(name):
    def deco(fn):
        RULES.append((name, fn))
        return fn
    return deco


@rule("two ages in a ratio")
def r_ages(Qq):
    m = re.match(r"The ages of ([A-Z][a-z]+) and ([A-Z][a-z]+) are in the ratio (\d+):(\d+)\. If \2 is (\d+) years old, how old is \1\?$", Qq.text)
    if not m or Qq.n != 3:
        return None
    first, second, a, b, age = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), int(m.group(5))
    if not (1 <= a <= 12 and 1 <= b <= 12) or age % b:
        return None
    unit = age // b
    if Qq.answer.strip() != str(unit * a):
        raise ValueError("%s: answer key disagrees" % Qq.id)

    def model(label, brace, note, hl=None):
        return bm([bar(segs(a, label, "unknown" if brace == "?" else "a"), label=first, brace=brace),
                   bar(segs(b, label, "b"), label=second, brace="%d years" % age)], note, hl)

    return entry(Qq, model(None, "?", "Ratio %d:%d. Every piece is the same size" % (a, b)), [
        model(None, "?", "%d equal parts for %s, %d for %s" % (a, first, b, second)),
        model(str(unit), "?", "One part: %d ÷ %d = %d" % (age, b, unit), ["b1"]),
        model(str(unit), "%d years" % (unit * a), "%d × %d = %d" % (a, unit, unit * a), ["b0"]),
    ], origin="rule")


@rule("share a quantity in the ratio a:b")
def r_share(Qq):
    m = re.match(r"Divide (\d+) in the ratio (\d+):(\d+)\. What is the (smaller|larger) share\?$", Qq.text)
    if m:
        total, a, b, which, item, noun = int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4), "", "share"
    else:
        m = re.match(r"([A-Z][a-z]+) has (\d+) ([a-z]+) and divides them in the ratio (\d+):(\d+)\. How many \3 are in the (smaller|larger) group\?$", Qq.text)
        if not m:
            return None
        total, item, a, b, which, noun = int(m.group(2)), " " + m.group(3), int(m.group(4)), int(m.group(5)), m.group(6), "group"
    if Qq.n not in (3, 4) or a == b or min(a, b) < 1 or total % (a + b):
        return None
    parts = a + b
    unit = total // parts
    wanted = max(a, b) if which == "larger" else min(a, b)
    ans = unit * wanted
    if Qq.answer.strip() != str(ans):
        raise ValueError("%s: answer key disagrees" % Qq.id)
    brace = ("%d%s" % (total, item))[:24]
    first_wanted = a == wanted
    small = parts <= 12

    def pieces(label=None, note=None, hl=None):
        if small:
            return bm([bar(segs(a, label, "a") + segs(b, label, "b"), brace=brace)], note, hl)
        # Too many parts to draw one by one: two blocks in proportion.
        return bm([bar([seg("%d parts" % a, a, "a"), seg("%d parts" % b, b, "b")], brace=brace)], note, hl)

    if small:
        keys = ["b0s%d" % i for i in (range(a) if first_wanted else range(a, parts))]
        keys = keys if len(keys) <= 8 else None
    else:
        keys = ["b0s0" if first_wanted else "b0s1"]
    after = bm([bar([seg(str(ans) if first_wanted else None, a, "a"),
                     seg(None if first_wanted else str(ans), b, "b")], brace=brace)],
               "The %s %s is %d" % (which, noun, ans), ["b0s0" if first_wanted else "b0s1"])
    before = pieces(note="Ratio %d:%d. The %s %s = ?" % (a, b, which, noun))
    # The bank's steps do not always say the numbers in words, so each step has a plainer fallback.
    figs = [
        [pieces(note="%d + %d = %d equal parts in all" % (a, b, parts)),
         pieces(note="Count the equal parts: %d and %d" % (a, b))],
        [pieces(str(unit) if small else None, "One part: %d ÷ %d = %d" % (total, parts, unit)),
         pieces(note="One part: %d ÷ %d" % (total, parts))],
        [pieces(str(unit) if small else None, "%d parts of %d: %d × %d = %d" % (wanted, unit, wanted, unit, ans), keys),
         pieces(note="%d parts make %d" % (wanted, ans), hl=keys)],
    ]
    if Qq.n == 4:
        figs.append(after)
    return entry(Qq, before, figs, origin="rule")


@rule("proportion a : b = c : x")
def r_proportion(Qq):
    m = re.match(r"If (\d+) : (\d+) = (\d+) : x, find x\.$", Qq.text)
    if not m or Qq.n != 3:
        return None
    a, b, c = [int(g) for g in m.groups()]
    if a < 1 or c % a or c == a:
        return None
    k = c // a
    x = b * k
    if Qq.answer.strip() != str(x):
        raise ValueError("%s: answer key disagrees" % Qq.id)

    def tab(last, note=None, hl=None):
        return table(["First term", "Second term"], [[str(a), str(b)], [str(c), last]], note, hl)

    return entry(Qq, tab("x"), [
        tab("x", "First terms: %d × %d = %d" % (a, k, c), ["r1"]),
        tab(str(x), "Second terms: %d × %d = %d" % (b, k, x), ["r1"]),
        tab(str(x), "x = %d" % x, ["r1"]),
    ], origin="rule")


def build():
    questions = load(NODE)
    out, rule_of = {}, {}
    for q in questions:
        Qq = Q(q)
        if q["id"] in OWN:
            e = OWN[q["id"]](Qq)
            if e:
                if e["origin"] != "authored":
                    raise ValueError(q["id"])
                out[q["id"]], rule_of[q["id"]] = e, "own"
            continue
        for name, fn in RULES:
            e = fn(Qq)
            if e:
                out[q["id"]], rule_of[q["id"]] = e, name
                break
    missing = [i for i in OWN if i not in {q["id"] for q in questions}]
    if missing:
        raise ValueError("not in this topic: %s" % missing)
    return questions, out, rule_of


if __name__ == "__main__":
    questions, out, rule_of = build()
    print("wrote", write("g4-%s.json" % NODE, out))
    report(NODE, questions, out, rule_of, sys.argv[1] if len(sys.argv) > 1 else None)
    left_out = [q["id"] for q in questions if q["id"] not in out]
    print("  no visual (%d): %s" % (len(left_out), " ".join(left_out)))
