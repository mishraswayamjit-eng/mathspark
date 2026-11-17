"""Helpers for the imported-04 lessons: board ops, and a rule that teaches an
order-of-operations line (brackets, then times and divide, then plus and minus)
one move at a time, computing every number it writes or says.

Board ops are plain dicts in the shape of src/lib/teach/types.ts.
"""
import hashlib
import re
from fractions import Fraction

MINUS = "−"
OPW = {"+": "plus", MINUS: "minus", "×": "times", "÷": "divided by"}
OPNAME = {"+": "plus", MINUS: "minus", "×": "times", "÷": "divide"}


# ── Board ops ────────────────────────────────────────────────────────────────

def W(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text}
    if tone:
        op["tone"] = tone
    return op


def LB(id, text, tone=None):
    op = {"op": "write", "id": id, "text": text, "label": True}
    if tone:
        op["tone"] = tone
    return op


def GIVEN(id, text):
    return LB(id, text, "given")


def GIVENM(id, text):
    return W(id, text, "given")


def ANS(id, text):
    return W(id, text, "answer")


def _target(text, nth=1):
    t = {"text": str(text)}
    if nth != 1:
        t["nth"] = nth
    return t


def MARK(line, text, shape="circle", nth=1):
    return {"op": "mark", "line": line, "target": _target(text, nth), "shape": shape}


def CIRC(line, text, nth=1):
    return MARK(line, text, "circle", nth)


def UL(line, text, nth=1):
    return MARK(line, text, "underline", nth)


def BOX(line, text, nth=1):
    return MARK(line, text, "box", nth)


def NOTE(line, target, text, place="below", nth=1):
    return {"op": "note", "line": line, "target": _target(target, nth), "text": str(text), "place": place}


def STRIKE(line, target, note=None, nth=1):
    op = {"op": "strike", "line": line, "target": _target(target, nth)}
    if note:
        op["note"] = note
    return op


def CHOOSE(choices, answer, if_not):
    return {"kind": "choose", "choices": choices, "answer": answer, "ifNot": if_not}


def B(say, *ops, **kw):
    beat = {"say": say}
    if ops:
        beat["board"] = list(ops)
    if kw.get("ask"):
        beat["ask"] = kw["ask"]
    return beat


def LESSON(*beats):
    return {"origin": "authored", "beats": list(beats)}


def pick(qid, salt, options):
    """A stable choice among a few phrasings."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


def count_upto(text, sub, pos):
    """Which occurrence of `sub` (counted the way str.count does) starts at `pos`."""
    n = 0
    i = text.find(sub)
    while i != -1:
        n += 1
        if i == pos:
            return n
        if i > pos:
            break
        i = text.find(sub, i + len(sub))
    # The wanted place overlaps an earlier match: fall back to a plain scan.
    n = 0
    i = text.find(sub)
    while i != -1:
        n += 1
        if i == pos:
            return n
        i = text.find(sub, i + 1)
    raise ValueError("%r is not at %d in %r" % (sub, pos, text))


def last_nth(text, sub):
    """The nth of the last place `sub` appears in `text`."""
    return count_upto(text, sub, text.rfind(sub))


def say_plus(nums):
    return " plus ".join(str(n) for n in nums)


def say_list(items):
    items = [str(i) for i in items]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


# ── An order-of-operations line as flat tokens ───────────────────────────────

def parse(expr):
    toks = []
    for t in re.findall(r"\d+|[+−×÷()]", expr):
        toks.append(int(t) if t.isdigit() else t)
    return toks


def render(toks):
    """(text, start position of each token)."""
    text = ""
    starts = []
    for i, t in enumerate(toks):
        if i and toks[i - 1] != "(" and t != ")":
            text += " "
        starts.append(len(text))
        text += str(t)
    return text, starts


def evalx(toks):
    s = ""
    for t in toks:
        if isinstance(t, int):
            s += "Fraction(%d)" % t
        else:
            s += {"+": "+", MINUS: "-", "×": "*", "÷": "/", "(": "(", ")": ")"}[t]
    return eval(s, {"Fraction": Fraction})


def apply_op(a, op, b):
    if op == "+":
        return a + b
    if op == MINUS:
        assert a >= b, "goes below zero: %d − %d" % (a, b)
        return a - b
    if op == "×":
        return a * b
    assert b != 0 and a % b == 0, "does not divide: %d ÷ %d" % (a, b)
    return a // b


def sent(a, op, b, r):
    return "%d %s %d is %d" % (a, OPW[op], b, r)


def find_pass(toks):
    """The next set of jobs that can all be done on this line.

    Returns (kind, [job]); a job is a dict with a, op, b, res, s, e (token span
    replaced), and flags. kind is 'B' (inside brackets) or 'DM'.
    """
    jobs = []
    if "(" in toks:
        i = 0
        while i < len(toks):
            if toks[i] == "(":
                j = i + 1
                while toks[j] not in ("(", ")"):
                    j += 1
                if toks[j] == ")":
                    ks = list(range(i + 2, j, 2))
                    k = next((x for x in ks if toks[x] in "×÷"), ks[0])
                    closes = (j - i - 1) == 3
                    a, op, b = toks[k - 1], toks[k], toks[k + 1]
                    jobs.append({"a": a, "op": op, "b": b, "res": apply_op(a, op, b),
                                 "s": i if closes else k - 1, "e": j if closes else k + 1,
                                 "closes": closes, "others": [toks[x] for x in ks if x != k]})
                    i = j
            i += 1
        return "B", jobs
    # Terms are the pieces between plus and minus signs.
    start = 0
    bounds = []
    for i, t in enumerate(toks):
        if t in ("+", MINUS):
            bounds.append((start, i - 1))
            start = i + 1
    bounds.append((start, len(toks) - 1))
    for s, e in bounds:
        if e > s:
            k = s + 1
            a, op, b = toks[k - 1], toks[k], toks[k + 1]
            job = {"a": a, "op": op, "b": b, "res": apply_op(a, op, b), "s": k - 1, "e": k + 1}
            if k + 2 <= e:
                job["next"] = (toks[k + 1], toks[k + 2], toks[k + 3])
            jobs.append(job)
    return "DM", jobs


def pairs_of(toks):
    """Every neighbouring 'a op b' in the line, reading straight across (brackets ignored)."""
    flat = [t for t in toks if t not in ("(", ")")]
    return [(flat[k - 1], flat[k], flat[k + 1]) for k in range(1, len(flat), 2)]


def ptext(p):
    return "%d %s %d" % p


def bodmas(qid, expr, intro, ending, answer):
    """A whole lesson for one order-of-operations line."""
    toks = parse(expr)
    assert evalx(toks) == answer, "%s: %s is %s, not %s" % (qid, expr, evalx(toks), answer)
    had_brackets = "(" in toks
    text, starts = render(toks)
    beats = [B(intro, GIVENM("l1", text))]
    cur = "l1"
    n_line = [1]

    def new_line():
        n_line[0] += 1
        return "l%d" % n_line[0]

    # ── Ask 1: which piece first? ──
    kind, jobs = find_pass(toks)
    first = jobs[0]
    right = (first["a"], first["op"], first["b"])
    right_set = {ptext((j["a"], j["op"], j["b"])) for j in jobs}
    allp = pairs_of(toks)
    idx = allp.index(right)
    cands = []
    if idx != 0:
        cands.append(allp[0])
    chain_in_ask = False
    if kind == "DM" and first.get("next") and first["next"][1] != first["op"]:
        cands.append(first["next"])
        chain_in_ask = True
    if idx + 1 < len(allp):
        cands.append(allp[idx + 1])
    if idx - 1 >= 0:
        cands.append(allp[idx - 1])
    cands += [p for p in allp if p[1] in ("+", MINUS)]
    cands += allp
    others = []
    for p in cands:
        t = ptext(p)
        if t not in right_set and t not in others:
            others.append(t)
        if len(others) == 2:
            break
    at = pick(qid, "ask1", list(range(len(others) + 1)))
    choices = list(others)
    choices.insert(at, ptext(right))
    words = "%d %s %d" % (first["a"], OPW[first["op"]], first["b"])
    if kind == "B" and first["closes"]:
        if_not = "Look for the brackets. Whatever sits inside them is worked out before anything else, so %s goes first." % words
    elif kind == "B":
        other = OPNAME[first["others"][0]]
        if first["op"] in "×÷":
            if_not = "Brackets go first. And inside the brackets, %s goes before %s, so %s is the very first job." % (
                OPNAME[first["op"]], other, words)
        else:
            if_not = "Brackets go first. Inside them we read from left to right, so %s is the very first job." % words
    elif chain_in_ask:
        if_not = ("Times and divide go before plus and minus. And when they sit side by side, "
                  "we take them from left to right, so %s goes first." % words)
    else:
        if_not = "%s is stronger than plus and minus, so it goes first, wherever it sits in the line. Here that is %s." % (
            OPNAME[first["op"]].capitalize(), words)
    beats.append(B(pick(qid, "ask1say", [
        "Before we work anything out, look along the whole line. Which piece do we do first?",
        "Don't rush in from the left. Which piece of this line has to be done first?",
        "There are several jobs in this line. Which one comes first?",
    ]), ask=CHOOSE(choices, at, if_not)))

    asked2 = False
    pb = 0
    pd = 0
    after_chain_ask = False

    # ── Passes: brackets, then times and divide ──
    while True:
        if "(" not in toks and not any(t in ("×", "÷") for t in toks):
            break
        if len(toks) == 3:
            break
        kind, jobs = find_pass(toks)
        text, starts = render(toks)
        for i, job in enumerate(jobs):
            a, op, b, res = job["a"], job["op"], job["b"], job["res"]
            s = sent(a, op, b, res)
            target = render(toks[job["s"]:job["e"] + 1])[0]
            nth = count_upto(text, target, starts[job["s"]])
            last = i == len(jobs) - 1
            if kind == "B":
                if pb == 0:
                    lead = pick(qid, "brlead", ["Brackets come first", "Brackets are always the first job",
                                                "The brackets get done first"]) if i == 0 else ""
                    if len(jobs) > 1:
                        where = "In the %s pair, " % ["first", "second", "third"][i]
                        if i == 0:
                            lead += ", and there are %s pairs. " % {2: "two", 3: "three"}[len(jobs)]
                        if not job["closes"] and op in "×÷":
                            say = "%s%s%s goes before %s, so %s." % (lead, where, OPNAME[op], OPNAME[job["others"][0]], s)
                        else:
                            say = "%s%s%s." % (lead, where, s)
                    elif job["closes"]:
                        say = "%s. Inside them, %s, so we write %d where the bracket was." % (lead, s, res)
                    elif op in "×÷":
                        say = "%s. In there the same order holds, so %s goes before %s: %s." % (
                            lead, OPNAME[op], OPNAME[job["others"][0]], s)
                    else:
                        say = "%s. Inside them we read from left to right: %s." % (lead, s)
                else:
                    if job["closes"]:
                        say = pick(qid, "brfin%d" % pb, ["Now finish the bracket: %s.", "That bracket has one job left: %s."]) % s
                    else:
                        say = "Still inside the brackets, we go left to right: %s." % s
                if last and len(jobs) > 1:
                    if all(j["closes"] for j in jobs):
                        say += " Write the line again with %s where the brackets were." % say_list([j["res"] for j in jobs])
                    else:
                        say += " Write the line again with those in place."
            else:
                mixed_chain = bool(job.get("next")) and job["next"][1] != op
                if mixed_chain and not asked2 and "ask" not in beats[-1] and not (pd == 0 and i == 0 and chain_in_ask):
                    c2 = [ptext((a, op, b)), ptext(job["next"])]
                    at2 = pick(qid, "ask2", [0, 1])
                    if at2 == 1:
                        c2.reverse()
                    beats.append(B(
                        "Now look at %d %s %d %s %d. %s and %s sit side by side. Which goes first?" % (
                            a, OPW[op], b, OPW[job["next"][1]], job["next"][2],
                            OPNAME[op].capitalize(), OPNAME[job["next"][1]]),
                        ask=CHOOSE(c2, at2,
                                   "Times and divide are equal partners, so neither one is stronger. "
                                   "We take them from left to right, and %d %s %d is on the left." % (a, OPW[op], b))))
                    asked2 = True
                    after_chain_ask = True
                if after_chain_ask:
                    say = "Left to right it is: %s." % s
                    after_chain_ask = False
                elif pd == 0 and i == 0:
                    if had_brackets:
                        say = pick(qid, "dmlead", ["With the brackets gone, times and divide come next. %s.",
                                                   "No brackets are left, so now we look for times and divide. %s."]) % s
                    else:
                        left = allp[0]
                        if (left[0], left[1], left[2]) != (a, op, b) and left[1] in ("+", MINUS):
                            say = pick(qid, "trap", [
                                "It is tempting to start on the left with %d %s %d. But %s is stronger than %s, so %d %s %d goes first: that makes %d.",
                                "Starting on the left with %d %s %d is the classic slip. %s goes before %s, so %d %s %d is first, and that makes %d.",
                            ])
                            if say.startswith("It is"):
                                say = say % (left[0], OPW[left[1]], left[2], OPNAME[op], OPNAME[left[1]], a, OPW[op], b, res)
                            else:
                                say = say % (left[0], OPW[left[1]], left[2], OPNAME[op].capitalize(), OPNAME[left[1]], a, OPW[op], b, res)
                        else:
                            say = "%s is stronger than plus and minus, so it goes first. %s." % (OPNAME[op].capitalize(), s[0].upper() + s[1:])
                elif i == 0:
                    say = pick(qid, "carry%d" % pd, ["Carry on along that piece: %s.", "Keep going with that same piece: %s."]) % s
                elif i == len(jobs) - 1 and i >= 2:
                    say = "And the last one: %s." % s
                elif op == jobs[i - 1]["op"]:
                    say = "There is another %s waiting: %s." % (OPNAME[op], s)
                else:
                    say = "The %s goes early too: %s." % (OPNAME[op], s)
                if last and len(jobs) > 1:
                    say += " Write the line again with %s in place." % say_list([j["res"] for j in jobs])
            ops = [UL(cur, target, nth), NOTE(cur, target, res, "below", nth)]
            if last:
                new = list(toks)
                for j in sorted(jobs, key=lambda x: -x["s"]):
                    new[j["s"]:j["e"] + 1] = [j["res"]]
                toks = new
                cur = new_line()
                ops.append(W(cur, render(toks)[0]))
            beats.append(B(say, *ops))
        if kind == "B":
            pb += 1
        else:
            pd += 1

    # ── The last stretch: plus and minus left to right, or one last times or divide ──
    steps = []
    run = toks[0]
    for k in range(1, len(toks), 2):
        r = apply_op(run, toks[k], toks[k + 1])
        steps.append((run, toks[k], toks[k + 1], r))
        run = r
    assert run == answer
    n = len(steps)
    is_as = toks[1] in ("+", MINUS)
    asked_as = False
    if is_as and n >= 2 and not asked2 and steps[0][1] == MINUS and steps[1][1] == "+" and "ask" not in beats[-1]:
        a, _, b, _ = steps[0]
        c = steps[1][2]
        c2 = ["%d − %d" % (a, b), "%d + %d" % (b, c)]
        at2 = pick(qid, "ask3", [0, 1])
        if at2 == 1:
            c2.reverse()
        beats.append(B("Only plus and minus are left: %d minus %d plus %d. Which do we do first?" % (a, b, c),
                       ask=CHOOSE(c2, at2,
                                  "Plus and minus are equal partners, so we read from left to right, like a sentence. "
                                  "That means %d minus %d comes first." % (a, b))))
        asked_as = True
    trap_at = None
    for t in range(n - 1):
        if steps[t][1] == MINUS and steps[t + 1][1] == "+" and not (asked_as and t == 0):
            trap_at = t
            break
    if n <= 3:
        groups = [[k] for k in range(n)]
    else:
        groups = []
        k = 0
        while k < n - 1:
            groups.append(list(range(k, min(k + 2, n - 1))))
            k += 2
        groups.append([n - 1])
    for g, grp in enumerate(groups):
        final = grp[-1] == n - 1
        body = ", and ".join(sent(*steps[k]) for k in grp)
        if g == 0:
            if asked_as:
                lead = "Left to right it is: "
            elif n == 1:
                lead = pick(qid, "one", ["One job is left: ", "Just one job left: "])
            elif is_as:
                lead = "Only plus and minus are left now, so we go left to right: "
            else:
                lead = ""
        elif final:
            lead = "And "
        else:
            lead = pick(qid, "mid%d" % g, ["Next, ", "Then ", "Keep going: "])
        say = lead + body + "."
        if trap_at is not None and trap_at in grp:
            say += " Careful: the %d comes off before the %d goes on, because we read left to right." % (
                steps[trap_at][2], steps[trap_at + 1][2])
        ops = []
        for k in grp:
            a, op, b, r = steps[k]
            lid = new_line()
            line = "%d %s %d = %d" % (a, op, b, r)
            if k == n - 1:
                ops.append(ANS(lid, line))
                ops.append(CIRC(lid, str(r), last_nth(line, str(r))))
            else:
                ops.append(W(lid, line))
        if final:
            say += " " + ending
        beats.append(B(say, *ops))

    # ── Check ──
    INV = {"+": MINUS, MINUS: "+", "×": "÷", "÷": "×"}
    a, op, b, r = steps[-1]
    back1 = W(new_line(), "%d %s %d = %d" % (r, INV[op], b, a))
    if n >= 2:
        a0, op0, b0, r0 = steps[-2]
        tail = "right where that line started" if n == 2 else "just as it says on the board"
        beats.append(B(pick(qid, "inv2", ["Check by walking backwards. %d %s %d is %d, and %d %s %d is %d, %s.",
                                          "Let's check by undoing our steps. %d %s %d is %d, and %d %s %d is %d, %s."]) % (
            r, OPW[INV[op]], b, a, r0, OPW[INV[op0]], b0, a0, tail),
            back1, W(new_line(), "%d %s %d = %d" % (r0, INV[op0], b0, a0))))
    else:
        beats.append(B(pick(qid, "inv", ["Check the last step backwards: %d %s %d is %d. It fits.",
                                         "Check by undoing the last step: %d %s %d is %d. It fits."]) % (r, OPW[INV[op]], b, a),
                       back1))

    # ── The method in one line ──
    if had_brackets:
        beats.append(B(pick(qid, "sum", [
            "So the order is: brackets first, then times and divide from left to right, then plus and minus from left to right.",
            "So every time: clear the brackets, then do times and divide as you meet them, then finish with plus and minus, left to right.",
            "So here is the plan for a line like this. Brackets, then times and divide, then plus and minus, always reading left to right.",
        ])))
    else:
        beats.append(B(pick(qid, "sum", [
            "So remember: times and divide go first, wherever they sit in the line. Then plus and minus, from left to right.",
            "So the plan is: hunt for the times and divide signs first. When only plus and minus are left, read from left to right.",
            "So in a line with no brackets: times and divide before plus and minus, and left to right when the signs are equal partners.",
        ])))
    return LESSON(*beats)
