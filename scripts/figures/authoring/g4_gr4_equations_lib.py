"""Shared kit for the Grade 4 figure writers of gr4_equations, gr4_ages and gr4_algebra.

What it gives the three topic scripts:
  - Part: loads one topic's questions, keeps the figures, checks every figure with the
    checker's own rules before it is kept, and writes the part file.
  - builders for the figure kinds used here (bar model, balance, number line, table ...).
    Bar pieces are given their TRUE values, so bars are in proportion by construction,
    and a numeric brace must equal the sum of its pieces.
  - ev(): works out both pans of a balance for the solved value, so a balance that is
    not true can never be written.
A step figure may be given as a list of alternatives: the first one the checker allows
at that step is used (the checker grounds a step figure on the step TEXT, not its latex).
"""
import io
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))
import validate  # noqa: E402

bank = validate.bank
PARTS = os.path.join(ROOT, "data", "question-figures", "parts")


# ── Numbers and text ─────────────────────────────────────────────────────────

def n(x):
    """A number as a child writes it: 12, 31.5 (never 12.0)."""
    if isinstance(x, Fraction):
        x = int(x) if x.denominator == 1 else float(x)
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        x = int(round(x))
    if isinstance(x, int):
        return str(x)
    return ("%.4f" % x).rstrip("0").rstrip(".")


def plain(s):
    """Step text or latex with the markup taken off."""
    s = s.replace("{,}", "").replace("\\times", " × ").replace("\\div", " ÷ ")
    s = re.sub(r"\\(?:text|mathrm|mathbf|textbf|boxed|quad)\b", " ", s)
    s = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r" \1 / \2 ", s)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("{", " ").replace("}", " ").replace("\\", " ")
    s = re.sub(r"(?<=\d),(?=\d)", "", s)
    return re.sub(r"\s+", " ", s)


def steps_of(q):
    return q.get("stepByStep") or []


def step_text(q, i):
    return steps_of(q)[i].get("text", "")


def step_latex(q, i):
    return plain(steps_of(q)[i].get("latex") or "")


def last_number(text):
    found = re.findall(r"\d+(?:\.\d+)?", text)
    return float(found[-1]) if found else None


def says(text, value):
    """True when `text` states this number as a whole token."""
    s = n(value)
    return re.search(r"(?<![\d.])" + re.escape(s) + r"(?![\d]|\.\d)", plain(text)) is not None


def key_text(q):
    return validate.correct_text(q)


def key_numbers(q):
    return validate.numbers_in(key_text(q))


def text_numbers(q):
    """The numbers written in the question text, in order."""
    cleaned = re.sub(r"(?<=\d),(?=\d)", "", q.get("questionText", ""))
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", cleaned)]


def allowed_before(q, uses_options=False):
    out = validate.numbers_in(q.get("questionText", ""))
    if uses_options:
        for t in validate.option_texts(q):
            out |= validate.numbers_in(t)
    return out


def allowed_at(q, i):
    out = allowed_before(q, True)
    for s in steps_of(q)[:i + 1]:
        out |= validate.numbers_in(s.get("text", ""))
    return out


def why_not(fig, allowed):
    """None if the checker would accept this figure with these numbers, else the reason."""
    ctx = validate.check_figure(fig, "f")
    if ctx.errors:
        return "; ".join(ctx.errors)
    extra = validate.ungrounded(ctx.numbers, allowed)
    if extra:
        return "shows " + validate.fmt(extra)
    return None


# ── One topic's part file ────────────────────────────────────────────────────

class Part(object):
    def __init__(self, topic):
        self.topic = topic
        self.qs = dict((q["id"], q) for q in bank.load_bank(4) if q.get("node") == topic)
        self.out = {}
        self.log = []
        self.path = os.path.join(PARTS, "g4-%s.json" % topic)

    def q(self, qid):
        return self.qs[qid]

    def note(self, qid, message):
        self.log.append("%s: %s" % (qid, message))

    def put(self, qid, before=None, steps=None, origin="authored", uses_options=False, essential=False):
        """before: a figure, a list of alternatives, or None.
        steps: a list (one slot per step) or a dict {step index: slot}; a slot is a figure,
        a list of alternatives, or None."""
        if qid not in self.qs:
            return self.note(qid, "is not a question of this topic")
        if qid in self.out:
            return self.note(qid, "given a figure twice")
        q = self.qs[qid]
        entry = {"origin": origin}
        if before is not None:
            alts = before if isinstance(before, list) else [before]
            reasons = []
            for fig in alts:
                reason = None if essential else why_not(fig, allowed_before(q, uses_options))
                if reason is None:
                    entry["figure"] = fig
                    break
                reasons.append(reason)
            else:
                self.note(qid, "before-figure left out: " + " | ".join(reasons))
        count = len(steps_of(q))
        if steps:
            if isinstance(steps, dict):
                bad = [k for k in steps if not (0 <= k < count)]
                if bad:
                    self.note(qid, "step index %s out of range (question has %d steps)" % (bad, count))
                steps = [steps.get(i) for i in range(count)]
            if len(steps) != count:
                self.note(qid, "gave %d step slots, question has %d steps: step figures left out" % (len(steps), count))
            else:
                chosen = []
                for i, slot in enumerate(steps):
                    if slot is None:
                        chosen.append(None)
                        continue
                    alts = slot if isinstance(slot, list) else [slot]
                    reasons = []
                    for fig in alts:
                        reason = why_not(fig, allowed_at(q, i))
                        if reason is None:
                            chosen.append(fig)
                            break
                        reasons.append(reason)
                    else:
                        chosen.append(None)
                        self.note(qid, "step %d figure left out: %s" % (i, " | ".join(reasons)))
                if any(f is not None for f in chosen):
                    entry["stepFigures"] = chosen
        if uses_options:
            entry["usesOptions"] = True
        if essential:
            entry["essential"] = True
        if "figure" not in entry and "stepFigures" not in entry:
            return self.note(qid, "nothing left to keep")
        problems = validate.check_entry(qid, entry, q)
        if problems:
            for p in problems:
                self.note(qid, "REJECTED " + p)
            return
        self.out[qid] = entry

    def save(self):
        ordered = dict((k, self.out[k]) for k in sorted(self.out))
        with io.open(self.path, "w", encoding="utf-8", newline="\n") as f:
            json.dump(ordered, f, ensure_ascii=False, indent=1)
            f.write("\n")
        kinds, rule, steps_only = {}, 0, 0
        for e in self.out.values():
            fig = e.get("figure") or next(x for x in e["stepFigures"] if x)
            kinds[fig["kind"]] = kinds.get(fig["kind"], 0) + 1
            rule += e["origin"] == "rule"
            steps_only += "figure" not in e
        print("%s: %d of %d questions have a visual (%d by rule, %d individually; %d with step figures only; %d essential)" % (
            self.topic, len(self.out), len(self.qs), rule, len(self.out) - rule, steps_only,
            sum(1 for e in self.out.values() if e.get("essential"))))
        print("  by kind of first figure: " + ", ".join("%s %d" % kv for kv in sorted(kinds.items(), key=lambda kv: -kv[1])))
        print("  no visual: " + " ".join(sorted(set(self.qs) - set(self.out))))
        if self.log:
            print("  NOTES (%d)" % len(self.log))
            for line in self.log:
                print("   - " + line)
        print("wrote " + os.path.relpath(self.path, ROOT))

    def review(self, name=None):
        """Question, figure and step figures side by side, for reading."""
        path = os.path.join(HERE, "g4_%s_review.txt" % (name or self.topic))
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            for qid in sorted(self.out):
                q, e = self.qs[qid], self.out[qid]
                f.write("### %s  [%s]\n" % (qid, e["origin"]))
                f.write("Q: %s\n" % q["questionText"].replace("\n", " / "))
                f.write("O: %s   KEY %s\n" % (" | ".join(o["text"] for o in q["options"]), key_text(q)))
                f.write("FIG: %s\n" % (show(e["figure"]) if "figure" in e else "(none)"))
                figs = e.get("stepFigures") or [None] * len(steps_of(q))
                for i, s in enumerate(steps_of(q)):
                    f.write("  %d. %s%s\n" % (i, s.get("text", ""), (" [L: %s]" % plain(s["latex"])) if s.get("latex") else ""))
                    if figs[i] is not None:
                        f.write("     -> %s\n" % show(figs[i]))
                f.write("\n")


def show(fig):
    """A figure on one line, for reading."""
    k = fig["kind"]
    tail = ""
    if fig.get("note"):
        tail += "  NOTE: " + fig["note"]
    if fig.get("highlight"):
        tail += "  HL: " + ",".join(fig["highlight"])
    if k == "barModel":
        bars = []
        for b in fig["bars"]:
            segs = " ".join("[%s:%s%s]" % (s.get("label", ""), n(s["units"]), "?" if s.get("tone") == "unknown" else "") for s in b["segments"])
            bars.append("%s: %s%s" % (b.get("label", ""), segs, (" }%s" % b["brace"]) if b.get("brace") else ""))
        return "BARS " + " // ".join(bars) + tail
    if k == "balance":
        return "BALANCE  %s  |  %s%s" % (fig["left"], fig["right"], tail)
    if k == "table":
        return "TABLE %s %s%s" % (fig.get("headers", ""), fig["rows"], tail)
    body = dict((a, b) for a, b in fig.items() if a not in ("kind", "note", "highlight"))
    return "%s %s%s" % (k.upper(), json.dumps(body, ensure_ascii=False), tail)


# ── Builders ─────────────────────────────────────────────────────────────────

def _finish(fig, note, hl):
    if note:
        if len(note) > 70:
            raise ValueError("note over 70 characters: %r" % note)
        fig["note"] = note
    if hl:
        fig["highlight"] = list(hl)
    return fig


def S(label, value, tone=None):
    """A bar piece with a free label and its true value (the value sets the drawn width)."""
    return {"label": label, "value": float(value), "tone": tone}


def V(value, pre="", post="", tone=None):
    """A bar piece labelled with its own value: V(35, "₹") is "₹35"."""
    return S(pre + n(value) + post, value, tone)


def Uq(value, label="?"):
    """The unknown piece, drawn at its true width."""
    return S(label, value, "unknown")


def B(label, *segs, **kw):
    """One bar: B("Kabir", Uq(32), brace="₹96"). Lists of pieces are flattened."""
    flat = []
    for s in segs:
        flat.extend(s if isinstance(s, list) else [s])
    return {"label": label, "segs": flat, "brace": kw.get("brace"), "chk": kw.get("chk", True)}


def bm(*bars, **kw):
    """A bar model. Every bar is drawn to the same scale, from the pieces' true values."""
    biggest = max(sum(s["value"] for s in b["segs"]) for b in bars)
    scale = 12.0 / biggest
    out = []
    for bi, b in enumerate(bars):
        total = sum(s["value"] for s in b["segs"])
        brace = b["brace"]
        if brace and b["chk"] and re.match(r"^(₹|Rs\. )?[\d,.]+( [A-Za-z]+)?$", brace):
            stated = sorted(validate.numbers_in(brace))[0]
            if abs(stated - total) > 1e-9:
                raise ValueError("bar %r: pieces add up to %s, brace says %s" % (b["label"], n(total), brace))
        segs = []
        for s in b["segs"]:
            seg = {"units": round(min(20.0, max(0.4, s["value"] * scale)), 2)}
            if s["label"]:
                seg["label"] = s["label"]
            seg["tone"] = s["tone"] or ("unknown" if (s["label"] or "").startswith("?") else "abc"[bi % 3])
            segs.append(seg)
        bar = {"segments": segs}
        if b["label"]:
            bar["label"] = b["label"]
        if brace:
            bar["brace"] = brace
        out.append(bar)
    return _finish({"kind": "barModel", "bars": out}, kw.get("note"), kw.get("hl"))


_TOK = re.compile(r"\s*(\d+(?:\.\d+)?|[A-Za-z★▲□]+|[()+\-−×÷/√])")


def ev(expr, env):
    """The value of a pan such as "4m/3 + 17" or "3 boxes + 2 kg" for the values in env."""
    toks, pos, s = [], 0, expr.strip()
    while pos < len(s):
        m = _TOK.match(s, pos)
        if not m:
            raise ValueError("cannot read %r" % expr)
        toks.append(m.group(1))
        pos = m.end()
    at = [0]

    def peek():
        return toks[at[0]] if at[0] < len(toks) else None

    def take():
        at[0] += 1
        return toks[at[0] - 1]

    def factor():
        t = take()
        if t == "(":
            v = total()
            if take() != ")":
                raise ValueError("bracket not closed in %r" % expr)
            return v
        if t == "√":
            v = factor()
            r = Fraction(int(round(float(v) ** 0.5)))
            if r * r != v:
                raise ValueError("not a perfect square in %r" % expr)
            return r
        if re.match(r"\d", t):
            return Fraction(t)
        if t in env:
            return Fraction(env[t])
        raise ValueError("unknown name %r in %r" % (t, expr))

    def term():
        v = factor()
        while True:
            t = peek()
            if t == "×":
                take()
                v = v * factor()
            elif t in ("÷", "/"):
                take()
                v = v / factor()
            elif t is not None and (t in ("(", "√") or re.match(r"[A-Za-z★▲□]", t)):
                v = v * factor()
            else:
                return v

    def total():
        v = term()
        while peek() in ("+", "-", "−"):
            t = take()
            w = term()
            v = v + w if t == "+" else v - w
        return v

    v = total()
    if peek() is not None:
        raise ValueError("could not read all of %r" % expr)
    return v


def bal(left, right, env=None, note=None, hl=None):
    """A balance. With env, both pans are worked out and must be equal."""
    if env is not None:
        a, b = ev(left, env), ev(right, env)
        if a != b:
            raise ValueError("balance is not true: %s is %s but %s is %s" % (left, n(a), right, n(b)))
    return _finish({"kind": "balance", "left": left, "right": right}, note, hl)


def nl(lo, hi, step, points=None, hops=None, ticks=None, note=None, hl=None):
    fig = {"kind": "numberLine", "min": lo, "max": hi, "step": step}
    if ticks:
        fig["tickLabels"] = ticks
    if points:
        fig["points"] = [dict([("at", p[0])] + ([("label", p[1])] if len(p) > 1 and p[1] else [])) for p in points]
    if hops:
        fig["hops"] = [dict([("from", h[0]), ("to", h[1])] + ([("label", h[2])] if len(h) > 2 and h[2] else [])) for h in hops]
    return _finish(fig, note, hl)


def tb(rows, headers=None, note=None, hl=None):
    fig = {"kind": "table", "rows": [[str(c) for c in r] for r in rows]}
    if headers:
        fig["headers"] = list(headers)
    return _finish(fig, note, hl)


def rect(length=None, breadth=None, inside=None, proportion=None, square=False, grid=None, note=None, hl=None):
    fig = {"kind": "rectangle"}
    if square:
        fig["square"] = True
    if length:
        fig["length"] = length
    if breadth:
        fig["breadth"] = breadth
    if inside:
        fig["inside"] = inside
    if proportion:
        fig["proportion"] = round(min(3.0, max(1.0, proportion)), 2)
    if grid:
        fig["grid"] = {"cols": grid[0], "rows": grid[1]}
    return _finish(fig, note, hl)


def tri(shape, sides=None, note=None, hl=None):
    fig = {"kind": "triangle", "shape": shape}
    if sides:
        fig["sides"] = sides
    return _finish(fig, note, hl)


def poly(points, edges=None, right=None, note=None, hl=None):
    fig = {"kind": "polygon", "points": [list(p) for p in points]}
    if edges:
        fig["edges"] = list(edges)
    if right:
        fig["rightAngles"] = list(right)
    return _finish(fig, note, hl)


def grid(rows, cols, note=None):
    return _finish({"kind": "grid", "rows": rows, "cols": cols}, note, None)
