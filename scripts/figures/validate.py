"""Check question figures, and build the file the app serves.

    python scripts/figures/validate.py            # check every part file, print coverage
    python scripts/figures/validate.py --build    # check, then write src/data/questionFigures/figures.json
    python scripts/figures/validate.py --part data/question-figures/parts/templated.json

Part files live in data/question-figures/parts/*.json. Each is one JSON object:
    { "<question id>": { ...QuestionVisual... }, ... }
The shapes are defined in src/lib/figures/types.ts; this file mirrors them.

What is enforced (see the rules at the top of types.ts):
  - every figure matches its type exactly (no unknown fields, values in range);
  - `figure` uses only numbers found in the question text (plus the answer
    choices when `usesOptions` is true), unless the entry is marked `essential`;
  - a step figure uses only numbers found in the question, the choices, or the
    steps up to and including its own;
  - `stepFigures` has one entry per step the question already has;
  - `steps` is allowed only where the question has no steps, only with
    origin "rule", and its last step must state the correct answer;
  - no child-facing text uses a word the tone rule bans.

Exit code 1 if anything fails. Nothing is written unless everything passes.
"""
import argparse
import collections
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEED = os.path.join(ROOT, "data", "mathspark_complete_seed.json")
PARTS = os.path.join(ROOT, "data", "question-figures", "parts")
OUT = os.path.join(ROOT, "src", "data", "questionFigures", "figures.json")

# Numbers any figure may show without the question stating them.
CONSTANTS = {0.0, 1.0, 2.0, 10.0, 12.0, 60.0, 90.0, 100.0, 180.0, 360.0, 1000.0}
BANNED = re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)
NUMBER = re.compile(r"\d+(?:\.\d+)?")
HIGHLIGHT_KEY = re.compile(r"^[a-z]+\d*(?:s\d+)?$")
COMPASS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def numbers_in(text):
    """The numbers written in a piece of text: '2,345' is 2345 and '9:33' is 9 and 33."""
    cleaned = re.sub(r"(?<=\d),(?=\d)", "", text)
    return {float(m) for m in NUMBER.findall(cleaned)}


# ── A small schema language ──────────────────────────────────────────────────
# Each checker is called as checker(value, path, ctx) and reports into ctx.

class Ctx(object):
    def __init__(self):
        self.errors = []
        self.numbers = set()   # numbers the figure shows
        self.texts = []        # child-facing strings

    def err(self, path, message):
        self.errors.append("%s: %s" % (path, message))


def Str(max_len=18):
    def check(v, path, ctx):
        if not isinstance(v, str) or not v.strip():
            return ctx.err(path, "must be non-empty text")
        if len(v) > max_len:
            ctx.err(path, "is %d characters, limit %d" % (len(v), max_len))
        if "<" in v or ">" in v:
            ctx.err(path, "must not contain < or >")
        ctx.numbers |= numbers_in(v)
        ctx.texts.append(v)
    return check


def Num(lo, hi, shown=False, whole=False):
    """A number in range. `shown` numbers appear in the picture, so they must be grounded."""
    def check(v, path, ctx):
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            return ctx.err(path, "must be a number")
        if whole and int(v) != v:
            ctx.err(path, "must be a whole number")
        if not (lo <= v <= hi):
            ctx.err(path, "must be between %s and %s" % (lo, hi))
        if shown:
            ctx.numbers.add(float(v))
    return check


def Bool(v, path, ctx):
    if not isinstance(v, bool):
        ctx.err(path, "must be true or false")


def Enum(*values):
    def check(v, path, ctx):
        if v not in values:
            ctx.err(path, "must be one of %s" % ", ".join(map(str, values)))
    return check


def Nullable(inner):
    def check(v, path, ctx):
        if v is not None:
            inner(v, path, ctx)
    return check


def List(item, lo=0, hi=99):
    def check(v, path, ctx):
        if not isinstance(v, list):
            return ctx.err(path, "must be a list")
        if not (lo <= len(v) <= hi):
            ctx.err(path, "must have %d to %d items, has %d" % (lo, hi, len(v)))
        for i, x in enumerate(v):
            item(x, "%s[%d]" % (path, i), ctx)
    return check


def Obj(required=None, optional=None):
    required = required or {}
    optional = optional or {}

    def check(v, path, ctx):
        if not isinstance(v, dict):
            return ctx.err(path, "must be an object")
        for key in required:
            if key not in v:
                ctx.err(path, "is missing '%s'" % key)
        for key, value in v.items():
            checker = required.get(key) or optional.get(key)
            if checker is None:
                ctx.err(path, "has a field '%s' that the type does not define" % key)
            else:
                checker(value, "%s.%s" % (path, key), ctx)
    return check


def HighlightKey(v, path, ctx):
    if not isinstance(v, str) or not HIGHLIGHT_KEY.match(v):
        ctx.err(path, "is not a valid highlight key")


BASE = {"highlight": List(HighlightKey, 0, 8), "note": Str(70)}
GRID_POINT = List(Num(0, 12), 2, 2)

KINDS = {
    "triangle": Obj(
        {"shape": Enum("scalene", "right", "isosceles", "equilateral")},
        {"sides": Obj(optional={"ab": Str(), "bc": Str(), "ca": Str()}),
         "angles": Obj(optional={"a": Str(), "b": Str(), "c": Str()}),
         "height": Str(), "enclose": Bool}),
    "rectangle": Obj(
        {},
        {"square": Bool, "length": Str(), "breadth": Str(), "inside": Str(24), "proportion": Num(1, 3),
         "grid": Obj({"cols": Num(1, 12, shown=True, whole=True), "rows": Num(1, 12, shown=True, whole=True)})}),
    "polygon": Obj(
        {"points": List(GRID_POINT, 3, 12)},
        {"edges": List(Nullable(Str())), "corners": List(Nullable(Str())),
         "rightAngles": List(Num(0, 11, whole=True), 0, 12),
         "dashed": List(Obj({"from": Num(0, 11, whole=True), "to": Num(0, 11, whole=True)}, {"label": Str()}), 0, 4)}),
    "circle": Obj({}, {"radius": Str(), "diameter": Str()}),
    "angles": Obj(
        {"layout": Enum("single", "onLine", "inRightAngle", "aroundPoint", "crossing"),
         "parts": List(Obj({"label": Str()}, {"size": Num(1, 359)}), 1, 6)}),
    "clock": Obj(
        {"hour": Num(1, 12, shown=True, whole=True), "minute": Num(0, 59, shown=True, whole=True)},
        {"showAngle": Bool}),
    "compass": Obj(
        {"facing": Enum(*COMPASS)},
        {"turns": List(Obj({"degrees": Num(1, 720, shown=True), "direction": Enum("clockwise", "anticlockwise")}), 0, 4),
         "showEnd": Bool}),
    "fractionBars": Obj(
        {"bars": List(Obj({"parts": Num(1, 24, shown=True, whole=True), "shaded": Num(0, 24, shown=True, whole=True)},
                          {"label": Str()}), 1, 4)},
        {"shape": Enum("bar", "circle")}),
    "set": Obj(
        {"total": Num(1, 60, shown=True, whole=True)},
        {"groups": Num(1, 12, shown=True, whole=True), "shadedGroups": Num(0, 12, shown=True, whole=True), "item": Str(14)}),
    "barModel": Obj(
        {"bars": List(Obj(
            {"segments": List(Obj({"units": Num(0.2, 20)}, {"label": Str(), "tone": Enum("a", "b", "c", "unknown")}), 1, 12)},
            {"label": Str(), "brace": Str(24)}), 1, 3)}),
    "numberLine": Obj(
        {"min": Num(-100000, 100000), "max": Num(-100000, 100000), "step": Num(0.001, 100000)},
        {"points": List(Obj({"at": Num(-100000, 100000, shown=True)}, {"label": Str()}), 0, 6),
         "hops": List(Obj({"from": Num(-100000, 100000, shown=True), "to": Num(-100000, 100000, shown=True)}, {"label": Str()}), 0, 8)}),
    "journey": Obj(
        {"places": List(Str(14), 2, 4), "legs": List(Obj(optional={"top": Str(), "bottom": Str()}), 1, 3)}),
    "placeChart": Obj({"number": Str(13)}),
    "grid": Obj(
        {"rows": Num(1, 12, shown=True, whole=True), "cols": Num(1, 12, shown=True, whole=True)},
        {"shaded": List(List(Num(0, 11, whole=True), 2, 2), 0, 144), "dots": Bool}),
    "barChart": Obj(
        {"bars": List(Obj({"label": Str(14), "value": Num(0, 1000000, shown=True)}), 2, 8)},
        {"unit": Str(12), "each": Num(1, 100000, shown=True)}),
    "table": Obj({"rows": List(List(Str(), 1, 5), 1, 6)}, {"headers": List(Str(), 1, 5)}),
    "venn": Obj({"leftTitle": Str(), "rightTitle": Str(), "left": Str(40), "both": Str(40), "right": Str(40)}),
    "balance": Obj({"left": Str(24), "right": Str(24)}),
    "factorTree": Obj({"number": Num(2, 1000, shown=True, whole=True)}, {"depth": Num(0, 10, whole=True)}),
}


def check_figure(fig, path):
    """Returns (errors, numbers shown, texts)."""
    ctx = Ctx()
    if not isinstance(fig, dict) or fig.get("kind") not in KINDS:
        ctx.err(path, "kind must be one of %s" % ", ".join(sorted(KINDS)))
        return ctx
    body = dict(fig)
    kind = body.pop("kind")
    for key, checker in BASE.items():
        if key in body:
            checker(body.pop(key), "%s.%s" % (path, key), ctx)
    KINDS[kind](body, path, ctx)
    if ctx.errors:
        return ctx

    # Checks that span more than one field.
    if kind == "angles" and fig["layout"] == "crossing" and len(fig["parts"]) != 4:
        ctx.err(path, "a crossing has exactly four parts")
    if kind == "angles" and fig["layout"] == "single" and len(fig["parts"]) != 1:
        ctx.err(path, "a single angle has exactly one part")
    if kind == "journey" and len(fig["legs"]) != len(fig["places"]) - 1:
        ctx.err(path, "needs one leg between each pair of places")
    if kind == "set":
        groups = fig.get("groups")
        if groups and fig["total"] % groups != 0:
            ctx.err(path, "groups must divide total")
        if fig.get("shadedGroups", 0) > (groups or 0):
            ctx.err(path, "shadedGroups cannot be more than groups")
    if kind == "fractionBars":
        for i, bar in enumerate(fig["bars"]):
            if bar["shaded"] > bar["parts"]:
                ctx.err("%s.bars[%d]" % (path, i), "shaded cannot be more than parts")
    if kind == "polygon":
        n = len(fig["points"])
        for key in ("edges", "corners"):
            if key in fig and len(fig[key]) != n:
                ctx.err(path, "%s needs one entry per corner (%d)" % (key, n))
        for i in fig.get("rightAngles", []):
            if i >= n:
                ctx.err(path, "rightAngles refers to a corner that does not exist")
        for d in fig.get("dashed", []):
            if d["from"] >= n or d["to"] >= n:
                ctx.err(path, "dashed refers to a corner that does not exist")
    if kind == "numberLine":
        if fig["max"] <= fig["min"] or (fig["max"] - fig["min"]) / fig["step"] > 40:
            ctx.err(path, "needs max above min and at most 40 ticks")
    if kind == "placeChart":
        if not re.match(r"^\d{1,9}(\.\d{1,3})?$", fig["number"]):
            ctx.err(path, "number must be digits with at most one decimal point")
    if kind == "table" and "headers" in fig:
        if any(len(r) != len(fig["headers"]) for r in fig["rows"]):
            ctx.err(path, "every row needs one cell per header")
    for text in ctx.texts:
        if BANNED.search(text):
            ctx.err(path, "uses a word the tone rule bans: %r" % text)
    return ctx


# ── Question-level checks ────────────────────────────────────────────────────

def option_texts(q):
    out = []
    for o in q.get("options", []):
        out.append(o.get("text", "") if isinstance(o, dict) else str(o))
    return out


def correct_text(q):
    for o in q.get("options", []):
        if isinstance(o, dict) and o.get("id") == q.get("correctAnswer"):
            return o.get("text", "")
    return ""


def ungrounded(shown, allowed):
    return sorted(n for n in shown if n not in allowed and n not in CONSTANTS)


def fmt(nums):
    return ", ".join(("%g" % n) for n in nums)


TOP_FIELDS = {"figure", "stepFigures", "steps", "usesOptions", "essential", "origin"}


def check_entry(qid, entry, q):
    """All problems with one question's visual. Returns a list of strings."""
    problems = []
    if not isinstance(entry, dict):
        return ["%s: must be an object" % qid]
    for key in entry:
        if key not in TOP_FIELDS:
            problems.append("%s: has a field '%s' that the type does not define" % (qid, key))
    if entry.get("origin") not in ("rule", "authored"):
        problems.append("%s: origin must be 'rule' or 'authored'" % qid)
    if not any(k in entry for k in ("figure", "stepFigures", "steps")):
        problems.append("%s: has no figure, stepFigures or steps" % qid)
    if entry.get("essential") and "figure" not in entry:
        problems.append("%s: essential needs a figure" % qid)

    question_numbers = numbers_in(q.get("questionText", ""))
    option_numbers = set()
    for t in option_texts(q):
        option_numbers |= numbers_in(t)

    if "figure" in entry:
        ctx = check_figure(entry["figure"], "%s.figure" % qid)
        problems += ctx.errors
        if not ctx.errors and not entry.get("essential"):
            allowed = question_numbers | (option_numbers if entry.get("usesOptions") else set())
            extra = ungrounded(ctx.numbers, allowed)
            if extra:
                problems.append("%s.figure: shows %s, not in the question text (givens only)" % (qid, fmt(extra)))

    own_steps = q.get("stepByStep") or []
    if "stepFigures" in entry:
        figs = entry["stepFigures"]
        if not isinstance(figs, list) or len(figs) != len(own_steps):
            problems.append("%s.stepFigures: needs %d entries, one per step of the question" % (qid, len(own_steps)))
        else:
            allowed = question_numbers | option_numbers
            for i, fig in enumerate(figs):
                allowed = allowed | numbers_in(own_steps[i].get("text", ""))
                if fig is None:
                    continue
                ctx = check_figure(fig, "%s.stepFigures[%d]" % (qid, i))
                problems += ctx.errors
                extra = [] if ctx.errors else ungrounded(ctx.numbers, allowed)
                if extra:
                    problems.append("%s.stepFigures[%d]: shows %s, not stated by this point" % (qid, i, fmt(extra)))

    if "steps" in entry:
        steps = entry["steps"]
        if own_steps:
            problems.append("%s.steps: the question already has steps; use stepFigures" % qid)
        elif entry.get("origin") != "rule":
            problems.append("%s.steps: only rule-computed entries may supply steps" % qid)
        elif not isinstance(steps, list) or not (1 <= len(steps) <= 6):
            problems.append("%s.steps: needs 1 to 6 steps" % qid)
        else:
            allowed = question_numbers | option_numbers
            for i, step in enumerate(steps):
                where = "%s.steps[%d]" % (qid, i)
                if not isinstance(step, dict) or set(step) - {"text", "figure"} or not isinstance(step.get("text"), str) or not step["text"].strip():
                    problems.append("%s: needs text, and optionally figure" % where)
                    continue
                if len(step["text"]) > 220:
                    problems.append("%s: text is over 220 characters" % where)
                if BANNED.search(step["text"]):
                    problems.append("%s: uses a word the tone rule bans" % where)
                allowed = allowed | numbers_in(step["text"])
                if "figure" in step:
                    ctx = check_figure(step["figure"], where + ".figure")
                    problems += ctx.errors
                    extra = [] if ctx.errors else ungrounded(ctx.numbers, allowed)
                    if extra:
                        problems.append("%s.figure: shows %s, not stated by this point" % (where, fmt(extra)))
            # The computed solution must land on the answer key.
            answer = numbers_in(correct_text(q))
            if steps and isinstance(steps[-1], dict) and isinstance(steps[-1].get("text"), str):
                if not answer or not answer <= numbers_in(steps[-1]["text"]):
                    problems.append("%s.steps: the last step does not state the correct answer %r" % (qid, correct_text(q)))
    return problems


def load_seed():
    with io.open(SEED, encoding="utf-8") as f:
        data = json.load(f)
    return {q["id"]: q for q in data["questions"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--part", action="append", help="check only this part file (repeatable)")
    parser.add_argument("--build", action="store_true", help="write the merged file the app serves")
    parser.add_argument("--quiet", action="store_true", help="do not print the coverage table")
    args = parser.parse_args()

    questions = load_seed()
    files = args.part or sorted(glob.glob(os.path.join(PARTS, "*.json")))
    if args.build and args.part:
        sys.exit("--build always uses every part file; drop --part")

    merged = {}
    owner = {}
    problems = []
    for path in files:
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        if not isinstance(part, dict):
            problems.append("%s: must be one JSON object keyed by question id" % path)
            continue
        for qid, entry in part.items():
            if qid not in questions:
                problems.append("%s: %s is not a question in the seed file" % (os.path.basename(path), qid))
                continue
            if qid in merged:
                problems.append("%s: %s is already in %s" % (os.path.basename(path), qid, owner[qid]))
                continue
            problems += check_entry(qid, entry, questions[qid])
            merged[qid] = entry
            owner[qid] = os.path.basename(path)

    if not args.quiet:
        by_topic = collections.Counter()
        with_figure = collections.Counter()
        for qid, entry in merged.items():
            key = questions[qid].get("subTopic", "")
            by_topic[key] += 1
            if "figure" in entry:
                with_figure[key] += 1
        print("%d questions have visuals (%d with a figure before answering, %d essential)" % (
            len(merged), sum(1 for e in merged.values() if "figure" in e), sum(1 for e in merged.values() if e.get("essential"))))
        for key, n in by_topic.most_common():
            print("  %4d  (%d with figure)  %s" % (n, with_figure[key], key))

    if problems:
        print("\n%d PROBLEMS" % len(problems))
        for p in problems[:200]:
            print("  " + p)
        if len(problems) > 200:
            print("  ... and %d more" % (len(problems) - 200))
        sys.exit(1)

    print("all checks passed")
    if args.build:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        # Drop the authoring-only flags the app has no use for.
        served = {}
        for qid in sorted(merged):
            served[qid] = {k: v for k, v in merged[qid].items() if k in ("figure", "stepFigures", "steps")}
        with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(served, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        print("wrote %s (%d questions)" % (os.path.relpath(OUT, ROOT), len(served)))


if __name__ == "__main__":
    main()
