"""Engines for the imported Grade 5 figures (see imported_other.py).

Every engine takes the question's own numbers, written out in a spec module, and
builds: the before-answering figure (givens only, unknown "?") and one step-figure
slot per step of the question.

How a step figure is decided. The imported questions keep their working in the
steps' `latex` field, and the checker grounds a step figure on the step `text`
(plus the question and the answer choices). So for each step:
  - a value counts as WORKED OUT at the first step whose text or latex states it;
  - the figure for that step points at the part of the picture the step is about
    (highlight), and SHOWS the value only if the checker allows it there;
  - a value that could not be shown is shown at the first later step that allows it;
  - a step that works out nothing in the picture gets null.
Every figure is run through validate.check_figure with the checker's own grounding
rule before it is kept, and every finished entry through validate.check_entry.
"""
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..")))
import validate  # noqa: E402

bank = validate.bank
SOURCES = ("ai_generated", "ipm_textbook", "official_ipm_2020")
NOT_MINE = ("gr5_area", "gr5_angles", "gr5_triangles")

POOL = {}
for _q in bank.load_bank(5):
    if _q.get("topicId") == "grade5" and _q.get("source") in SOURCES and _q.get("node") not in NOT_MINE:
        POOL[_q["id"]] = _q
SHORT = {}
for _id in POOL:
    SHORT.setdefault(_id[-12:], []).append(_id)

E = {}          # question id -> QuestionVisual
PROBLEMS = []   # things a spec got wrong: printed, and the question is left out


def Q(sid):
    """A question by full id, or by the last 12 characters of an AIGEN id."""
    if sid in POOL:
        return POOL[sid]
    hits = SHORT.get(sid, [])
    if len(hits) != 1:
        raise KeyError("no single question for %r" % sid)
    return POOL[hits[0]]


# ── Numbers and text ─────────────────────────────────────────────────────────

def n(x):
    """A number as a child writes it: 12, 31.5, 45.75 (never 12.0)."""
    if isinstance(x, Fraction):
        x = int(x) if x.denominator == 1 else float(x)
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        x = int(round(x))
    if isinstance(x, int):
        return str(x)
    return ("%.4f" % x).rstrip("0").rstrip(".")


def commas(x):
    """Indian digit grouping for whole numbers from 1,000: 1,200 and 1,50,000."""
    s = n(x)
    if "." in s or len(s) < 4 or s.startswith("-"):
        return s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return ",".join(parts + [tail])


def fmt(x, unit=""):
    """A value with its unit: '₹' goes in front, anything else behind."""
    if unit in ("₹", "Rs."):
        f = float(x)
        return ("₹" if unit == "₹" else "Rs. ") + (commas(x) if abs(f - round(f)) < 1e-9 else "%.2f" % f)
    return commas(x) + ((" " + unit) if unit else "")


def plain(s):
    """Step text or latex with the markup taken off, so numbers and units can be matched."""
    s = s.replace("{,}", "").replace("{:}", ":").replace("\\times", " × ").replace("\\div", " ÷ ")
    s = re.sub(r"\\(?:text|mathrm|mathbf|textbf)\b", " ", s)
    s = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}", r" \1 / \2 ", s)
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("{", " ").replace("}", " ").replace("\\", " ")
    s = re.sub(r"(?<=\d),(?=\d)", "", s)
    return re.sub(r"\s+", " ", s)


def step_all(q, i):
    s = (q.get("stepByStep") or [])[i]
    return plain(s.get("text", "") + " ; " + (s.get("latex") or ""))


def says(text, value):
    """True when `text` (already plain) states this number as a whole token."""
    s = n(value)
    if s.startswith("-"):
        s = s[1:]
    tail = r"0*" if "." in s else r"(?:\.0+)?"
    return re.search(r"(?<![\d.])" + re.escape(s) + tail + r"(?![\d]|\.\d)", text) is not None


def allowed_at(q, i):
    """The numbers the checker lets a figure for step i show."""
    out = validate.numbers_in(q.get("questionText", ""))
    for t in validate.option_texts(q):
        out |= validate.numbers_in(t)
    for s in (q.get("stepByStep") or [])[:i + 1]:
        out |= validate.numbers_in(s.get("text", ""))
    return out


def ok_at(q, i, fig):
    ctx = validate.check_figure(fig, "f")
    return not ctx.errors and not validate.ungrounded(ctx.numbers, allowed_at(q, i))


def key_numbers(q):
    return validate.numbers_in(validate.correct_text(q))


def expect(q, value, what):
    """The spec's own arithmetic must land on the answer key, or the question is left out."""
    if value is None:
        return True
    if float(value) not in key_numbers(q) and round(float(value), 2) not in key_numbers(q):
        PROBLEMS.append("%s: %s computes %s, key is %r" % (q["id"][-12:], what, n(value), validate.correct_text(q)))
        return False
    return True


def cut(s, limit):
    return s if len(s) <= limit else s[:limit - 1].rstrip() + "…"


# ── The step runner ──────────────────────────────────────────────────────────

class Stage(object):
    """One thing a solution works out. `when(text)` says a step works it out;
    `final` stages are shown at the last step if nothing showed them earlier."""

    def __init__(self, key, when, final=False, group=None):
        self.key, self.when, self.final, self.group = key, when, final, group


def run(q, stages, render):
    """render(shown, focus) -> figure. Returns the stepFigures list (or None if the question has no steps)."""
    steps = q.get("stepByStep") or []
    if not steps:
        return None
    worked, shown, out = [], set(), []
    group = dict((s.key, s.group) for s in stages)
    settled = set()   # groups (ways of writing one value) that already have a way shown
    for i in range(len(steps)):
        text = step_all(q, i)
        new = [s.key for s in stages if s.key not in worked and group[s.key] not in settled and s.when(text)]
        if i == len(steps) - 1:
            new += [s.key for s in stages if s.final and s.key not in worked and s.key not in new]
        worked += new
        fresh = []
        for key in worked:
            if key in shown or group[key] in settled:
                continue
            if ok_at(q, i, render(shown | {key}, key)):
                shown.add(key)
                fresh.append(key)
                if group[key] is not None:
                    settled.add(group[key])
        new = [k for k in new if k in shown or group[k] not in settled]
        focus = new[0] if new else (fresh[0] if fresh else None)
        if focus is None:
            out.append(None)
            continue
        fig = render(shown, focus)
        out.append(fig if ok_at(q, i, fig) else None)
    return out


def add(q, before, step_figs=None, origin="rule", uses_options=False):
    entry = {"origin": origin}
    if before is not None:
        entry["figure"] = before
    if step_figs and any(f is not None for f in step_figs):
        entry["stepFigures"] = step_figs
    if uses_options:
        entry["usesOptions"] = True
    problems = validate.check_entry(q["id"], entry, q)
    if problems and "stepFigures" in entry:
        # Keep the before-answering figure if only a step figure is at fault.
        trimmed = dict(entry)
        del trimmed["stepFigures"]
        if "figure" in trimmed and not validate.check_entry(q["id"], trimmed, q):
            PROBLEMS.append("%s: step figures dropped: %s" % (q["id"][-12:], problems[0]))
            entry, problems = trimmed, []
    if problems:
        PROBLEMS.extend(problems)
        return
    if q["id"] in E:
        PROBLEMS.append("%s: given a figure twice" % q["id"])
        return
    E[q["id"]] = entry


# ── Engine: bar model of amounts ─────────────────────────────────────────────
# Segments:  S(label, value)   a given amount; the label shows it
#            H(label, value)   a given described another way ("20%", "60 × ₹8"); value worked out in the steps
#            U(label="?", n=1) the unknown: n equal pieces, found by balancing
# A bar is (label, [segments]) or (label, [segments], (brace label, brace value)).

def S(label, value):
    return {"t": "S", "label": label, "value": float(value)}


def H(label, value):
    return {"t": "H", "label": label, "value": float(value)}


def U(label="?", n=1):
    return {"t": "U", "label": label, "n": n, "value": None}


def model(sid, bars, unit="₹", ans=None, note=None, unote=None, check=True, origin="rule", compare=True):
    """compare=False: two bars with no unknown piece are two separate amounts, not a difference to find."""
    q = Q(sid)
    bars = [list(b) + [None] * (3 - len(b)) for b in bars]
    totals = []
    unknown = None
    for bi, (label, segs, brace) in enumerate(bars):
        for si, s in enumerate(segs):
            if s["t"] == "U":
                if unknown is not None:
                    PROBLEMS.append("%s: more than one unknown" % sid)
                    return
                unknown = (bi, si)
        known = sum(s["value"] for s in segs if s["t"] != "U")
        totals.append(brace[1] if brace else (known if not any(s["t"] == "U" for s in segs) else None))
    u = None
    if unknown is not None:
        bi, si = unknown
        segs = bars[bi][1]
        known = sum(s["value"] for s in segs if s["t"] != "U")
        whole = bars[bi][2][1] if bars[bi][2] else next((t for j, t in enumerate(totals) if j != bi and t is not None), None)
        if whole is None:
            PROBLEMS.append("%s: nothing to balance the unknown against" % sid)
            return
        u = (whole - known) / segs[si]["n"]
        if u <= 0:
            PROBLEMS.append("%s: the unknown comes out as %s" % (sid, n(u)))
            return
        segs[si]["value"] = u
        totals[bi] = whole
    elif len(bars) == 2 and compare:
        u = abs(totals[0] - totals[1])
    if check:
        want = ans(u) if callable(ans) else (ans if ans is not None else u)
        if not expect(q, want, "bar model"):
            return

    biggest = max(sum(s["value"] * (s.get("n") or 1) for s in b[1]) for b in bars)
    scale = 12.0 / biggest

    def units(v):
        return round(min(20.0, max(1.0, v * scale)), 2)

    stages, notes = [], {}
    for bi, (label, segs, brace) in enumerate(bars):
        for si, s in enumerate(segs):
            if s["t"] == "H":
                key = "h%d_%d" % (bi, si)
                stages.append(Stage(key, (lambda v: lambda t: says(t, v))(s["value"])))
                notes[key] = ("%s = %s" % (s["label"], fmt(s["value"], unit)), "This step works out the %s part" % cut(s["label"], 18))
        if not brace and len(segs) > 1 and not any(s["t"] == "U" for s in segs) and len(bars) > 1:
            key = "t%d" % bi
            stages.append(Stage(key, (lambda v: lambda t: says(t, v))(totals[bi])))
            notes[key] = ("%s in all: %s" % (label or "This bar", fmt(totals[bi], unit)), "Add up the pieces of this bar")
    if u is not None:
        # If another piece has the same value, a step stating it need not be about the unknown: wait for the last step.
        twin = any(abs(s["value"] - u) < 1e-9 for b in bars for s in b[1] if s["t"] != "U") or any(t is not None and abs(t - u) < 1e-9 for t in totals)
        stages.append(Stage("u", (lambda t: False) if twin else (lambda t: says(t, u)), final=True))
        tmpl = unote or "? = %s"
        notes["u"] = (tmpl % fmt(u, unit) if "%s" in tmpl else tmpl, "This is the part to find")

    def render(shown, focus):
        fig_bars, hl = [], []
        for bi, (label, segs, brace) in enumerate(bars):
            out = []
            for si, s in enumerate(segs):
                key = "h%d_%d" % (bi, si)
                if s["t"] == "S":
                    pieces = [(s["label"], None)]
                elif s["t"] == "H":
                    both = "%s = %s" % (s["label"], fmt(s["value"], unit))
                    lab = s["label"] if key not in shown else (both if len(both) <= 18 else fmt(s["value"], unit))
                    pieces = [(lab, None)]
                else:
                    lab = s["label"]
                    if "u" in shown:   # "? girls" becomes "613 girls"; "? × ₹9" becomes the amount
                        m = re.match(r"^\? ([a-z]+)$", lab)
                        lab = "%s %s" % (fmt(u, unit), m.group(1)) if m and not unit else fmt(u, unit)
                    pieces = [(lab, None if "u" in shown else "unknown")] * s["n"]
                for lab, tone in pieces:
                    if focus == key or (focus == "u" and s["t"] == "U"):
                        hl.append("b%ds%d" % (bi, len(out)))
                    seg = {"units": units(s["value"]), "label": lab, "tone": tone or "abc"[(si + bi) % 3]}
                    out.append(seg)
            bar = {"segments": out}
            if label:
                bar["label"] = label
            if brace:
                bar["brace"] = brace[0]
            elif "t%d" % bi in shown:
                bar["brace"] = fmt(totals[bi], unit)
            if focus == "t%d" % bi:
                hl.append("b%d" % bi)
            fig_bars.append(bar)
        fig = {"kind": "barModel", "bars": fig_bars}
        if focus is None:
            if note:
                fig["note"] = note
        else:
            fig["note"] = cut(notes[focus][0] if focus in shown else notes[focus][1], 70)
            if hl:
                fig["highlight"] = hl[:8]
        return fig

    add(q, render(set(), None), run(q, stages, render), origin=origin)


# ── Engine: sharing in a ratio (one bar per sharer, equal pieces) ────────────

def ratio(sid, names, parts, total=None, share=None, unit="", shown=None, ask=None, ans=None, note=None, what="Ratio"):
    """parts: the pieces drawn per sharer (the ratio in lowest terms).
    shown: the ratio as the question writes it, if different (ages 12 and 8).
    total=(label, value) the amount shared, or share=(index, label, value) one known share.
    ask: index of the sharer whose share is wanted (brace "?")."""
    q = Q(sid)
    if max(parts) > 12 or len(names) > 3:
        PROBLEMS.append("%s: too many pieces to draw" % sid)
        return
    one = Fraction(total[1], sum(parts)) if total else Fraction(share[2], parts[share[0]])
    shares = [one * p for p in parts]
    if ans is not None:
        want = ans(shares, one) if callable(ans) else ans
        if not expect(q, want, "ratio"):
            return
    written = " : ".join(str(x) for x in (shown or parts))
    base = note or ("%s %s. Together: %s" % (what, written, total[0]) if total else "%s %s" % (what, written))

    if not unit:   # "90 packets" -> packets, "₹540" -> ₹
        m = re.match(r"^(₹)?[\d,.]+\s*(.*)$", (total or share[1:])[0])
        unit = (m.group(1) or m.group(2)) if m else ""
    count = sum(parts)
    state = {"share": False}   # one piece is only "worked out" before any share is

    known = total[1] if total else share[2]   # the amount the sharing starts from

    def share_when(v):
        # A share is worked out from the whole amount (2/5 × 90) or from one piece (7 × 7), not just named.
        def when(t):
            hit = says(t, v) and (says(t, known) or ("×" in t and says(t, one)))
            state["share"] = state["share"] or hit
            return hit
        return when

    stages = [Stage("sum", lambda t: says(t, count) and "+" in t and not state["share"]),
              Stage("one", lambda t: says(t, one) and says(t, known) and ("÷" in t or "/" in t) and not state["share"])]
    for i in range(len(names)):
        if not (share and share[0] == i):
            stages.append(Stage("s%d" % i, share_when(shares[i]), final=(ask == i and float(shares[i]) in key_numbers(q))))

    def render(seen, focus):
        bars, hl = [], []
        for i, name in enumerate(names):
            segs = []
            for _ in range(parts[i]):
                seg = {"units": 1, "tone": "abc"[i]}
                if "one" in seen:
                    seg["label"] = n(one)
                segs.append(seg)
            bar = {"label": name, "segments": segs}
            if share and share[0] == i:
                bar["brace"] = share[1]
            elif "s%d" % i in seen:
                bar["brace"] = fmt(shares[i], unit)
            elif ask == i:
                bar["brace"] = "?"
            if focus == "s%d" % i:
                hl.append("b%d" % i)
            bars.append(bar)
        fig = {"kind": "barModel", "bars": bars}
        if focus is None:
            fig["note"] = cut(base, 70)
        elif focus == "sum":
            written_sum = " + ".join(str(p) for p in parts)
            fig["note"] = "%s = %d equal pieces in all" % (written_sum, count) if "sum" in seen else "Count the equal pieces in all the bars"
        elif focus == "one":
            fig["note"] = "Each equal piece is %s" % fmt(one, unit) if "one" in seen else "Count the equal pieces, then find one piece"
        else:
            i = int(focus[1:])
            fig["note"] = cut("%s: %d pieces = %s" % (names[i], parts[i], fmt(shares[i], unit)) if focus in seen
                              else "%s has %d of the equal pieces" % (names[i], parts[i]), 70)
        if hl:
            fig["highlight"] = hl
        return fig

    add(q, render(set(), None), run(q, stages, render))


# ── Engine: a journey in stretches ───────────────────────────────────────────

def leg(d=None, s=None, t=None, hd=None, ht=None, hs=None, tl=None, dl=None):
    """One stretch. d, s, t are GIVEN in the question (t in hours; use Fraction for minutes).
    hd, ht, hs are worked out in the steps. tl / dl: how the question words a given time / distance."""
    return {"d": d, "s": s, "t": t, "hd": hd, "ht": ht, "hs": hs, "tl": tl, "dl": dl}


def mins(m):
    return Fraction(m, 60)


def time_forms(t):
    """Ways a solution may write a time, as (label, test on plain text)."""
    t = Fraction(t).limit_denominator(3600)
    total = t * 60
    out = []
    if total.denominator == 1:
        m = int(total)
        h, r = divmod(m, 60)
        dec = n(float(t))
        if len(dec.split(".")[-1]) <= 2 or "." not in dec:
            out.append((dec + " h", lambda x, dec=dec: re.search(
                r"(?<![\d.])" + re.escape(dec) + r"(?:\.0)?\s*(?:hours?|hrs?|h)\b(?!\s*(?:and\s*)?\d+\s*(?:minutes?|mins?|m\b))", x) is not None))
        if h and r:
            out.append(("%d h %d min" % (h, r), lambda x, h=h, r=r: re.search(r"(?<![\d.])%d\s*(?:hours?|hrs?|h)\s*(?:and\s*)?%d\s*(?:minutes?|mins?|m)\b" % (h, r), x) is not None))
        out.append(("%d min" % m, lambda x, m=m: re.search(r"(?<![\d.])%d\s*(?:minutes?|mins?)\b" % m, x) is not None))
    return out


def journey(sid, places, legs, du="km", su="km/hr", note=None, origin="rule"):
    q = Q(sid)
    for L in legs:   # fill in what follows from two known values
        d = L["d"] if L["d"] is not None else L["hd"]
        s = L["s"] if L["s"] is not None else L["hs"]
        t = L["t"] if L["t"] is not None else L["ht"]
        if d is None and s is not None and t is not None:
            L["hd"] = Fraction(s) * Fraction(t)
        if t is None and s is not None and d is not None:
            L["ht"] = Fraction(d) / Fraction(s)
        if s is None and d is not None and t is not None:
            L["hs"] = Fraction(d) / Fraction(t)

    def given_time(L):
        if L["tl"]:
            return L["tl"]
        forms = time_forms(L["t"])
        return forms[0][0] if forms else None

    stages, form, why = [], {}, {}
    d_unit = r"(?:km|kilomet)" if du == "km" else r"(?:m\b|met)"
    for i, L in enumerate(legs):
        d_ = L["d"] if L["d"] is not None else L["hd"]
        s_ = L["s"] if L["s"] is not None else L["hs"]
        if L["hd"] is not None:
            product = L["s"] is not None and L["t"] is not None
            why["d%d" % i] = "Distance = speed × time for this stretch" if product else "Find the length of this stretch"
            stages.append(Stage("d%d" % i, (lambda v, sp: lambda x: re.search(
                r"(?<![\d.])" + re.escape(n(v)) + r"(?:\.0)?\s*" + d_unit, x) is not None and (sp is None or says(x, sp)))(
                    L["hd"], L["s"] if product else None)))
        if L["ht"] is not None:
            if su == "m/s":
                sec = n(L["ht"])
                forms = [(sec + " s", lambda x, sec=sec: re.search(r"(?<![\d.])" + re.escape(sec) + r"\s*(?:seconds?|secs?|s)\b", x) is not None)]
            else:
                forms = time_forms(L["ht"])
            for j, (label, test) in enumerate(forms):
                key = "t%d_%d" % (i, j)
                form[key] = label
                why[key] = "Time = distance ÷ speed for this stretch"
                stages.append(Stage(key, (lambda test, a, b: lambda x: test(x) and says(x, a) and says(x, b))(test, s_, d_), group="t%d" % i))
        if L["hs"] is not None:
            why["s%d" % i] = "Speed = distance ÷ time for this stretch"
            stages.append(Stage("s%d" % i, (lambda v, a: lambda x: re.search(
                r"(?<![\d.])" + re.escape(n(v)) + r"(?:\.0)?\s*(?:km\s*/\s*h|km\s*per|kmph|m\s*/\s*s)", x) is not None and says(x, a))(L["hs"], d_)))

    def render(seen, focus):
        out, hl = [], []
        for i, L in enumerate(legs):
            top = L["dl"] or (fmt(L["d"], du) if L["d"] is not None else (fmt(L["hd"], du) if "d%d" % i in seen else None))
            speed = "%s %s" % (n(L["s"]), su) if L["s"] is not None else ("%s %s" % (n(L["hs"]), su) if "s%d" % i in seen else None)
            time = given_time(L) if L["t"] is not None else None
            found = time is None
            if time is None:
                time = next((form[k] for k in sorted(form) if k.startswith("t%d_" % i) and k in seen), None)
            bottom = ", ".join(x for x in (speed, time) if x)
            if len(bottom) > 18:   # no room for both: once the time is worked out, it is what the later steps use
                bottom = time if found else speed
            one = {}
            if top:
                one["top"] = top
            if bottom:
                one["bottom"] = bottom
            out.append(one)
            if focus and focus[1:].split("_")[0] == str(i):
                hl.append("l%d" % i)
        fig = {"kind": "journey", "places": places, "legs": out}
        if focus is None:
            if note:
                fig["note"] = note
        else:
            fig["note"] = why[focus]
            fig["highlight"] = hl
        return fig

    # Only one way of writing a time is kept per stretch: the first that a step uses.
    def run_once():
        return run(q, stages, render)

    figs = run_once()
    add(q, render(set(), None), figs, origin=origin)


# ── Engine: a table (rows of a series, or the givens of a long story) ────────

def table(rows, note=None, headers=None, hl=None):
    fig = {"kind": "table", "rows": rows}
    if headers:
        fig["headers"] = headers
    if note:
        fig["note"] = cut(note, 70)
    if hl:
        fig["highlight"] = hl
    return fig


def wrap(cells, width=5):
    """Rows of at most `width` cells, as even as they can be (6 cells make 3 and 3, not 5 and 1)."""
    rows = -(-len(cells) // width)
    per = -(-len(cells) // rows)
    return [cells[i:i + per] for i in range(0, len(cells), per)]


def staged(sid, before, stages, origin="rule", uses_options=False):
    """An entry whose step figures are set out by the spec: `stages` is a list of (trigger, figure).
    trigger: a number (the step whose working states it), a regex string, 'final' (the last
    step), or (number, 'final') (the step that states it, else the last step).
    figure: one figure, or a list of them: the first the checker allows at that step is used."""
    q = Q(sid)
    table_ = {}
    st = []

    def trigger(trig):
        if trig == "final":
            return lambda t: False
        if isinstance(trig, tuple):
            return lambda t: says(t, trig[0])
        if isinstance(trig, str):
            return lambda t: re.search(trig, t, re.I) is not None
        return lambda t: says(t, trig)

    for k, (trig, fig) in enumerate(stages):
        alts = fig if isinstance(fig, list) else [fig]
        for a, one in enumerate(alts):
            key = "k%d_%d" % (k, a)
            table_[key] = one
            st.append(Stage(key, trigger(trig), final=(trig == "final" or isinstance(trig, tuple)),
                            group=("g%d" % k) if len(alts) > 1 else None))

    def render(seen, focus):
        return table_[focus] if focus else before

    add(q, before, run(q, st, render), origin=origin, uses_options=uses_options)
