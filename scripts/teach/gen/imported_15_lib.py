"""Helpers for the imported-15 lessons (profit and loss stories).

Board ops are plain dicts in the shape of src/lib/teach/types.ts. The class L
builds one lesson a beat at a time and computes every number it writes or says,
so a board line cannot disagree with the words spoken over it.
"""
import hashlib
from fractions import Fraction

MINUS = "−"
OPW = {"+": "plus", MINUS: "minus", "×": "times", "÷": "divided by"}


def f(n):
    """A number as it is written and said: 1,170 not 1170."""
    if isinstance(n, str):
        return n
    return "{:,}".format(n)


def num(n):
    return Fraction(n) if isinstance(n, str) else n


def cap(s):
    return s[0].upper() + s[1:]


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


def pick(qid, salt, options):
    """A stable choice among a few phrasings."""
    h = int(hashlib.md5((qid + "|" + salt).encode("utf-8")).hexdigest(), 16)
    return options[h % len(options)]


def last_nth(text, sub):
    """Which occurrence (counted the way str.count does) is the last place `sub` appears."""
    assert sub in text, (sub, text)
    return text.count(sub)


def say_list(items):
    items = [str(i) for i in items]
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


def apply_op(a, op, b):
    a, b = num(a), num(b)
    if op == "+":
        r = a + b
    elif op == MINUS:
        assert a >= b, "goes below zero"
        r = a - b
    elif op == "×":
        r = a * b
    else:
        r = Fraction(a) / Fraction(b)
    r = Fraction(r)
    assert r.denominator == 1, "not a whole number: %s %s %s" % (a, op, b)
    return int(r)


# ── One lesson ───────────────────────────────────────────────────────────────

class L:
    def __init__(self, qid, who, pro="she", poss="her"):
        self.qid = qid
        self.who = who
        self.pro = pro
        self.poss = poss
        self.beats = []
        self.n = 0
        self.T = None          # money spent
        self.S = None          # money earned
        self.P = None          # profit
        self.sale_vals = []
        self.last = None       # id of the last line written by calc/add

    # ── basics ──
    def nid(self):
        self.n += 1
        return "l%d" % self.n

    def pk(self, salt, options):
        return pick(self.qid, salt, options)

    def b(self, say, *ops, **kw):
        self.beats.append(B(say, *ops, **kw))
        return self

    def intro(self, say, label):
        return self.b(say, GIVEN("q", label))

    def fmt(self, text, **kw):
        return text.format(who=self.who, Who=cap(self.who), pro=self.pro, Pro=cap(self.pro), poss=self.poss, **kw)

    def calc(self, a, op, b, say, *more, **kw):
        """Write 'a op b = r', saying `say` ({a} {b} {r} are filled in). Returns r."""
        r = apply_op(a, op, b)
        lid = self.nid()
        line = "%s %s %s = %s" % (f(a), op, f(b), f(r))
        if kw.get("answer"):
            ops = [ANS(lid, line), CIRC(lid, f(r), last_nth(line, f(r)))]
        else:
            ops = [W(lid, line)]
        if kw.get("note"):
            ops.append(UL(lid, f(r), last_nth(line, f(r))))
            ops.append(NOTE(lid, f(r), kw["note"], "below", last_nth(line, f(r))))
        self.b(self.fmt(say, a=f(a), b=f(b), r=f(r)), *(ops + list(more)))
        self.last = lid
        return r

    def add(self, nums, say, note=None, answer=False):
        """Write 'a + b + c = T'. {sum} is 'a plus b plus c', {r} the total."""
        r = sum(nums)
        lid = self.nid()
        line = "%s = %s" % (" + ".join(f(x) for x in nums), f(r))
        ops = [ANS(lid, line) if answer else W(lid, line)]
        if note:
            ops.append(UL(lid, f(r), last_nth(line, f(r))))
            ops.append(NOTE(lid, f(r), note, "below", last_nth(line, f(r))))
        self.b(self.fmt(say, sum=" plus ".join(f(x) for x in nums), r=f(r)), *ops)
        self.last = lid
        return r

    def line(self, text, say, *more, **kw):
        """Write a line given as text (the checker proves it true)."""
        lid = self.nid()
        op = ANS(lid, text) if kw.get("answer") else W(lid, text)
        self.b(self.fmt(say), op, *more)
        self.last = lid
        return lid

    # ── the parts of a profit story ──
    def plan(self):
        say = self.pk("plan", [
            "Profit is the money that comes in, take away the money that goes out. So we need two totals: what {who} spent, and what {pro} earned.",
            "To find a profit we need two amounts: the money {who} spent, and the money {pro} earned. Profit is earned, take away spent.",
            "Here is the plan. Add up the money going out, add up the money coming in, and the gap between them is the profit.",
        ])
        return self.b(self.fmt(say), LB("p", "Profit = money earned − money spent"))

    def costs(self, items, mark=None):
        """items: (name, amount) for a plain cost, (name, n, price) for n things at a price each."""
        mult = [it for it in items if len(it) == 3]
        flat = [it for it in items if len(it) == 2]
        vals = []
        for i, (name, n, p) in enumerate(mult):
            v = apply_op(n, "×", p)
            vals.append(v)
            if i == 0:
                say = "Start with the money going out. %s: {a} times {b} is {r} rupees." % cap(name)
            else:
                say = self.pk("c%d" % i, ["Next, %s: {a} times {b} is {r} rupees.", "Then %s: {a} times {b} is {r} rupees."]) % name
            if len(mult) == 1 and not flat:
                say += " That is everything {who} spent."
                self.calc(n, "×", p, say, note="money spent")
            else:
                self.calc(n, "×", p, say)
        if len(mult) == 1 and not flat:
            self.T = vals[0]
        elif not mult and len(flat) == 1:
            self.T = flat[0][1]
            ops = [UL("q", mark)] if mark else []
            self.b(self.fmt("The money going out is quick this time. {Who} spent %s rupees on %s, and that is the whole cost." % (
                f(self.T), flat[0][0])), *ops)
        else:
            nums = vals + [v for _, v in flat]
            names = say_list([n for n, _ in flat])
            if mult and flat:
                say = "Now add %s. {sum} is {r} rupees. That is everything {who} spent." % names
            elif mult:
                say = "Add those together. {sum} is {r} rupees. That is everything {who} spent."
            else:
                say = "Start with the money going out: %s. {sum} is {r} rupees, and that is everything {who} spent." % names
            self.T = self.add(nums, say, note="money spent")
        return self.T

    def sold(self, made_say, made, lost, things, why, mark=None):
        """Ask how many were really sold, then write made − lost."""
        s = made - lost
        choices = ["all %s" % f(made), "%s + %s = %s" % (f(made), f(lost), f(made + lost))]
        at = self.pk("soldat", [0, 1, 2])
        choices.insert(at, "%s − %s = %s" % (f(made), f(lost), f(s)))
        q = self.pk("soldq", ["But how many were actually sold?", "How many of them brought in money?", "So how many were really sold?"])
        self.b(self.fmt(made_say) + " " + q, ask=CHOOSE(choices, at, self.fmt(
            "Look at the story again: %s %s %s. They bring in no money, so they come off. %s minus %s is %s." % (
                f(lost), things, why, f(made), f(lost), f(s)))))
        say = self.pk("soldsay", [
            "So only {r} %s were sold. {Who} still paid for all {a}, and that is the trap in this story." % things,
            "{a} minus {b} is {r}, so {r} %s were sold. The cost does not shrink, though: all {a} were paid for." % things,
            "That leaves {r} %s sold. Careful here: the {b} that %s earn nothing, but they still cost money." % (things, why),
        ])
        more = [CIRC("q", mark)] if mark else []
        return self.calc(made, MINUS, lost, say, *more)

    def sale(self, n, p, phrase, only=False):
        lead = "Now the money coming in. " if not self.sale_vals else self.pk("s%d" % len(self.sale_vals), ["Next, ", "Then "])
        ph = phrase.format(n=f(n), p=f(p))
        say = lead + (cap(ph) if lead.endswith(". ") else ph) + ": {a} times {b} is {r} rupees."
        if only:
            say += self.pk("only", [" That is all the money earned.", " That is the money earned."])
            v = self.calc(n, "×", p, say, note="money earned")
            self.S = v
        else:
            v = self.calc(n, "×", p, say)
        self.sale_vals.append(v)
        return v

    def sales_total(self):
        self.S = self.add(self.sale_vals, self.pk("stot", [
            "Altogether, {sum} is {r} rupees earned.",
            "Put the sales together: {sum} is {r} rupees. That is the money earned.",
        ]), note="money earned")
        return self.S

    def ask_profit(self):
        S, T = f(self.S), f(self.T)
        choices = ["Yes, all ₹%s" % S, "No: take away the ₹%s spent" % T]
        at = self.pk("apat", [0, 1])
        if at == 0:
            choices.reverse()
        return self.b(self.fmt(self.pk("apq", [
            "%s rupees came in. So is the profit %s rupees?" % (S, S),
            "{Who} took in %s rupees. Is all of that profit?" % S,
        ])), ask=CHOOSE(choices, at, self.fmt(
            "Part of that %s rupees only pays back the %s rupees {who} spent. Profit is what is left after the cost comes off." % (S, T))))

    def profit(self, answer=True):
        say = self.pk("prof", [
            "Now subtract. {a} minus {b} is {r}.",
            "Money earned, take away money spent: {a} minus {b} is {r}.",
            "Last step: {a} minus {b} is {r}.",
        ])
        if answer:
            say += self.pk("prof2", [" So the profit is {r} rupees.", " That is a profit of {r} rupees.", " {Who} makes a profit of {r} rupees."])
        else:
            say += " That is the profit."
        self.P = self.calc(self.S, MINUS, self.T, say, answer=answer)
        return self.P

    def check(self):
        self.calc(self.P, "+", self.T, self.pk("chk", [
            "Check by adding back. {a} plus {b} is {r}, exactly the money that came in.",
            "Let's check. The profit and the cost together should make the money earned: {a} plus {b} is {r}. It fits.",
            "A quick check: {a} plus {b} is {r}, and that is the money earned. It works.",
        ]))
        return self

    def sumup(self, kind="plain"):
        text = {
            "plain": [
                "So for any profit story: add up all the money spent, add up the money earned, then subtract.",
                "So the method is: total cost first, total sales next, and profit is sales take away cost.",
                "So remember the plan: every cost goes into one total, the sales go into another, and the gap is the profit.",
            ],
            "lost": [
                "So the method is: total up every cost, count only what was really sold, then take the cost away from the money earned.",
                "So in a story like this: all the costs count, but only the things really sold bring money in. Then subtract.",
                "So remember: pay for everything, earn only from what is sold, and profit is earned take away spent.",
            ],
            "two": [
                "So when things sell at two prices: work out each batch on its own, add the two, then take away the total cost.",
                "So the method is: total cost, then the money from each batch, then earned take away spent.",
            ],
        }[kind]
        return self.b(self.pk("sum", text))

    def done(self):
        assert 6 <= len(self.beats) <= 16, "%s has %d beats" % (self.qid, len(self.beats))
        for i, beat in enumerate(self.beats):
            assert len(beat["say"]) <= 240, "%s beat %d is %d characters: %s" % (self.qid, i, len(beat["say"]), beat["say"])
            assert len(beat.get("board", [])) <= 6, "%s beat %d has too many ops" % (self.qid, i)
            for op in beat.get("board", []):
                if op["op"] == "write":
                    assert len(op["text"]) <= 60, "%s: line of %d characters: %s" % (self.qid, len(op["text"]), op["text"])
        return {"origin": "authored", "beats": self.beats}


def stall(qid, who, intro, given, costs, sales, pro="she", poss="her", lost=None, trap=None, kind=None, cost_mark=None):
    """The plain shape: total cost, (how many sold), sales, profit, check.

    sales: (n, price, phrase); n may be 'sold' (what is left after `lost`) or
    'rest' (what is still unsold after the earlier batches).
    lost: (made_say, made, lost, things, why, mark)
    """
    l = L(qid, who, pro, poss)
    l.intro(intro, given)
    l.plan()
    l.costs(costs, cost_mark)
    n_sold = None
    things = None
    if lost:
        made_say, made, n_lost, things, why, mark = lost
        n_sold = l.sold(made_say, made, n_lost, things, why, mark)
    taken = 0
    for n, p, phrase in sales:
        if n == "sold":
            n = n_sold
        elif n == "rest":
            n = l.calc(n_sold, MINUS, taken, l.pk("rest", [
                "The rest go at a different price. {a} minus {b} leaves {r} %s." % things,
                "How many are left for the second batch? {a} minus {b} is {r} %s." % things,
            ]))
        taken += n
        l.sale(n, p, phrase, only=len(sales) == 1)
    if len(sales) > 1:
        l.sales_total()
    if not lost:
        l.ask_profit()
    l.profit()
    if trap:
        l.b(trap)
    l.check()
    l.sumup(kind or ("lost" if lost else ("two" if len(sales) > 1 else "plain")))
    return l.done()
