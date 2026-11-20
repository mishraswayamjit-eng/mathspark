"""Check teach-mode lessons, and build the file the app serves.

    python -X utf8 scripts/teach/validate.py                    # every part, with coverage
    python -X utf8 scripts/teach/validate.py --part algebra      # one part
    python -X utf8 scripts/teach/validate.py --show <question id>  # print a lesson as a script to read
    python -X utf8 scripts/teach/validate.py --build             # check, then write src/data/teach/scripts.json

A part file is data/teach/parts/<name>.json: { "<question id>": TeachScript }.
The shapes are defined in src/lib/teach/types.ts; this file mirrors them.

What is enforced:
  - the maths on the board is TRUE. Every written line that is not a label must parse as
    maths; an equation with the unknown must hold when the answer is put in; a sum with
    no unknown must be exactly right;
  - the lesson ends on the question's keyed answer, written on the board as the answer;
  - everything the teacher says can be spoken (words, not symbols), is short, and uses
    only numbers that are in the question or already on the board;
  - board marks point at text that is really on the line they name;
  - the child gets a turn: at least one ask, with a right choice and a kind reply to a miss;
  - no word the tone rule bans.
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
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "figures"))
from common import number_tokens  # noqa: E402  (scripts/speech/common.py)
import validate as figure_check  # noqa: E402  (scripts/figures/validate.py)

sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)

PARTS = os.path.join(ROOT, "data", "teach", "parts")
OUT = os.path.join(ROOT, "src", "data", "teach", "scripts.json")

BANNED_WORDS = re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)
UNSPEAKABLE = set("×÷=+%₹°√/\\^_{}<>*|□★≠≤≥~#@$")
ALLOWED_HIGH = set("’‘“”–—…")
ABBREVIATIONS = re.compile(r"\b(?:cm|mm|km|kg|mg|ml|sq|hr|hrs|kmph|Rs)\b\.?")
DIGIT_DASH = re.compile(r"\d\s*[-−–]\s*\d")
GROUPED = re.compile(r"(?<![\d,])(?:\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})+,\d{3})(?!\d)(?!,\d)")
FREE_NUMBERS = {str(n) for n in range(0, 11)}
MAX_SAY = 240


# ── Maths on the board must be true ──────────────────────────────────────────

class NotMaths(Exception):
    pass


_RELATION = re.compile(r"(≠|≤|≥|=|<|>)")


def _tokens(text, variable):
    s = GROUPED.sub(lambda m: m.group(0).replace(",", ""), text)
    for k, v in {"½": "(1/2)", "¼": "(1/4)", "¾": "(3/4)", "⅓": "(1/3)", "⅔": "(2/3)", "²": "^2", "³": "^3"}.items():
        s = s.replace(k, v)
    s = s.replace("−", "-").replace("–", "-").replace("×", "*").replace("·", "*").replace("÷", "/")
    s = s.replace("[", "(").replace("]", ")").replace("{", "(").replace("}", ")")
    s = re.sub(r"\bof\b", "*", s)
    s = re.sub(r"(?:₹|\bRs\.?)\s*", "", s)
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c.isspace():
            i += 1
        elif c.isdigit() or (c == "." and i + 1 < len(s) and s[i + 1].isdigit()):
            m = re.match(r"\d*\.?\d+", s[i:])
            out.append(("num", Fraction(m.group(0))))
            i += len(m.group(0))
        elif c in "+-*/^()%√":
            out.append((c, None))
            i += 1
        elif c.isalpha():
            if variable and c == variable and not (i + 1 < len(s) and s[i + 1].isalpha()) and not (i > 0 and s[i - 1].isalpha()):
                out.append(("var", None))
                i += 1
            else:
                raise NotMaths("the word or letter at '%s'" % s[i:i + 12])
        else:
            raise NotMaths("the character '%s'" % c)
    # Implied multiplication: 4(3x − 5), 12x, (x + 1)(x − 1), 2√9.
    joined = []
    for tok in out:
        if joined:
            a, b = joined[-1][0], tok[0]
            if a in ("num", "var", ")", "%") and b in ("var", "(", "√"):
                joined.append(("*", None))
            elif a in (")", "var") and b == "num":
                joined.append(("*", None))
        joined.append(tok)
    return joined


def value_of(text, variable=None, at=None):
    """The exact value of a piece of maths. Raises NotMaths if it is not plain maths."""
    toks = _tokens(text, variable)
    if not toks:
        raise NotMaths("nothing there")
    pos = [0]

    def peek():
        return toks[pos[0]][0] if pos[0] < len(toks) else None

    def take():
        pos[0] += 1
        return toks[pos[0] - 1]

    def atom():
        k = peek()
        if k == "num":
            v = take()[1]
        elif k == "var":
            take()
            if at is None:
                raise NotMaths("an unknown with no value to check it against")
            v = at
        elif k == "(":
            take()
            v = total()
            if peek() != ")":
                raise NotMaths("a bracket that is not closed")
            take()
        elif k == "-":
            take()
            return -power()
        elif k == "+":
            take()
            return power()
        elif k == "√":
            take()
            inner = atom()
            root = None
            if inner >= 0:
                n, d = inner.numerator, inner.denominator
                rn, rd = int(round(n ** 0.5)), int(round(d ** 0.5))
                if rn * rn == n and rd * rd == d:
                    root = Fraction(rn, rd)
            if root is None:
                raise NotMaths("a square root that is not exact")
            v = root
        else:
            raise NotMaths("something missing")
        while peek() == "%":
            take()
            v = v / 100
        return v

    def power():
        v = atom()
        if peek() == "^":
            take()
            e = power()
            if e.denominator != 1 or abs(e) > 12:
                raise NotMaths("a power that is not a small whole number")
            v = v ** int(e)
        return v

    def product():
        v = power()
        while peek() in ("*", "/"):
            op = take()[0]
            w = power()
            if op == "/" and w == 0:
                raise NotMaths("division by zero")
            v = v * w if op == "*" else v / w
        return v

    def total():
        v = product()
        while peek() in ("+", "-"):
            op = take()[0]
            w = product()
            v = v + w if op == "+" else v - w
        return v

    v = total()
    if pos[0] != len(toks):
        raise NotMaths("something left over")
    return v


def check_line(text, variable, at):
    """None if the line is true maths; otherwise a sentence saying what is the matter."""
    if "?" in text or "≈" in text:
        # A line with a blank to fill, or an approximation, is shown but not checked.
        return None
    parts = _RELATION.split(text)
    try:
        values = [value_of(p, variable, at) for p in parts[0::2]]
    except NotMaths as e:
        return "is not plain maths (%s). Mark it label: true if it is words" % e
    for i, rel in enumerate(parts[1::2]):
        a, b = values[i], values[i + 1]
        holds = {"=": a == b, "≠": a != b, "<": a < b, ">": a > b, "≤": a <= b, "≥": a >= b}[rel]
        if not holds:
            shown = lambda v: str(v.numerator) if v.denominator == 1 else "%s/%s" % (v.numerator, v.denominator)
            return "is not true: the two sides are %s and %s%s" % (
                shown(a), shown(b), (" when %s = %s" % (variable, at)) if variable and variable in text else "")
    return None


# ── Words the teacher says ───────────────────────────────────────────────────

def check_say(text, where, grounded):
    problems = []
    if not isinstance(text, str) or not text.strip():
        return ["%s: nothing to say" % where]
    if len(text) > MAX_SAY:
        problems.append("%s: %d characters; keep each thing the teacher says under %d" % (where, len(text), MAX_SAY))
    bad = sorted({c for c in text if c in UNSPEAKABLE or (ord(c) > 0x2000 and c not in ALLOWED_HIGH)})
    if bad:
        problems.append("%s: has symbols that cannot be spoken: %s" % (where, " ".join(bad)))
    m = ABBREVIATIONS.search(text)
    if m:
        problems.append("%s: write the unit out in full, not '%s'" % (where, m.group(0)))
    if DIGIT_DASH.search(text):
        problems.append("%s: a dash between numbers; say 'minus' or 'to'" % where)
    if BANNED_WORDS.search(text):
        problems.append("%s: uses a word the tone rule bans" % where)
    extra = [n for n in number_tokens(text) if n not in grounded and n not in FREE_NUMBERS]
    if extra:
        problems.append("%s: says %s, which is not in the question or on the board yet" % (where, ", ".join(sorted(set(extra)))))
    return problems


# ── One lesson ───────────────────────────────────────────────────────────────

def option_texts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def correct_text(q):
    idx = "ABCD".find(q.get("correctAnswer", ""))
    options = option_texts(q)
    return options[idx] if 0 <= idx < len(options) else ""


def find_target(line_text, target):
    if not isinstance(target, dict) or not isinstance(target.get("text"), str) or not target["text"]:
        return False
    nth = target.get("nth", 1)
    if not isinstance(nth, int) or nth < 1 or set(target) - {"text", "nth"}:
        return False
    return line_text.count(target["text"]) >= nth


OP_FIELDS = {
    "write": ({"id", "text"}, {"tone", "label"}),
    "arc": ({"line", "from", "to"}, set()),
    "strike": ({"line", "target"}, {"note"}),
    "note": ({"line", "target", "text"}, {"place"}),
    "mark": ({"line", "target", "shape"}, set()),
    "both": ({"line", "text"}, set()),
    "divide": ({"line", "by"}, set()),
    "group": ({"line", "targets"}, {"label"}),
    "figure": ({"id", "spec"}, set()),
    "clear": (set(), set()),
}


def check_script(qid, script, q):
    problems = []
    if not isinstance(script, dict) or set(script) - {"check", "beats", "origin"}:
        return ["%s: a lesson has check (optional), beats and origin" % qid]
    if script.get("origin") not in ("rule", "authored"):
        problems.append("%s: origin must be 'rule' or 'authored'" % qid)
    beats = script.get("beats")
    if not isinstance(beats, list) or not (6 <= len(beats) <= 16):
        return problems + ["%s: needs 6 to 16 beats" % qid]

    variable, at = None, None
    check = script.get("check")
    if check is not None:
        ok = isinstance(check, dict) and set(check) == {"variable", "value"} and isinstance(check["variable"], str) \
            and re.fullmatch(r"[a-z]", check["variable"]) and isinstance(check["value"], str)
        if ok:
            try:
                at = value_of(check["value"])
                variable = check["variable"]
            except NotMaths:
                ok = False
        if not ok:
            problems.append("%s.check: needs a single small letter and its value, e.g. {\"variable\": \"x\", \"value\": \"7\"}" % qid)

    answer_tokens = set(number_tokens(correct_text(q)))
    grounded = set(number_tokens(q.get("questionText", "")))
    if at is not None:
        grounded |= set(number_tokens(script["check"]["value"]))
        if answer_tokens and not set(number_tokens(script["check"]["value"])) <= answer_tokens:
            problems.append("%s.check: the value %s is not the keyed answer %r" % (qid, script["check"]["value"], correct_text(q)))

    lines = {}            # id -> text of the lines now on the board
    answer_lines = []
    asks = 0
    first_write_tone = None
    last_was_ask = False

    for b, beat in enumerate(beats):
        where = "%s.beats[%d]" % (qid, b)
        if not isinstance(beat, dict) or set(beat) - {"say", "board", "ask"}:
            problems.append("%s: a beat has say, board (optional) and ask (optional)" % where)
            continue
        ops = beat.get("board", [])
        if not isinstance(ops, list) or len(ops) > 6:
            problems.append("%s.board: a list of at most 6 things" % where)
            ops = []
        for o, op in enumerate(ops):
            ow = "%s.board[%d]" % (where, o)
            kind = op.get("op") if isinstance(op, dict) else None
            if kind not in OP_FIELDS:
                problems.append("%s: op must be one of %s" % (ow, ", ".join(sorted(OP_FIELDS))))
                continue
            need, may = OP_FIELDS[kind]
            keys = set(op) - {"op"}
            if not need <= keys or keys - need - may:
                problems.append("%s: '%s' takes %s%s" % (ow, kind, ", ".join(sorted(need)) or "nothing",
                                                         (" and optionally " + ", ".join(sorted(may))) if may else ""))
                continue

            if kind == "clear":
                lines = {}
                continue
            if kind == "figure":
                ctx = figure_check.check_figure(op["spec"], ow + ".spec")
                problems += ctx.errors
                grounded |= {("%g" % n) for n in ctx.numbers}
                for t in ctx.texts:
                    grounded |= set(number_tokens(t))
                continue
            if kind == "write":
                text = op["text"]
                if not isinstance(op["id"], str) or not op["id"] or op["id"] in lines:
                    problems.append("%s: a line needs a new id" % ow)
                if not isinstance(text, str) or not text.strip() or len(text) > 60:
                    problems.append("%s: a line is 1 to 60 characters; split longer working over two lines" % ow)
                    continue
                tone = op.get("tone", "work")
                if tone not in ("given", "work", "answer"):
                    problems.append("%s: tone must be given, work or answer" % ow)
                if first_write_tone is None:
                    first_write_tone = tone
                if BANNED_WORDS.search(text):
                    problems.append("%s: uses a word the tone rule bans" % ow)
                if not op.get("label"):
                    matter = check_line(text, variable, at)
                    if matter:
                        problems.append("%s: \"%s\" %s" % (ow, text, matter))
                lines[op["id"]] = text
                grounded |= set(number_tokens(text))
                if tone == "answer":
                    answer_lines.append(text)
                continue

            # Every other op points at a line that is on the board.
            line_text = lines.get(op["line"])
            if line_text is None:
                problems.append("%s: there is no line '%s' on the board at this point" % (ow, op["line"]))
                continue
            targets = []
            if kind == "arc":
                targets = [op["from"]] + (op["to"] if isinstance(op["to"], list) else [None])
                if not isinstance(op["to"], list) or not (1 <= len(op["to"]) <= 4):
                    problems.append("%s: an arc goes to 1 to 4 places" % ow)
            elif kind in ("strike", "note", "mark"):
                targets = [op["target"]]
            elif kind == "group":
                targets = op["targets"] if isinstance(op["targets"], list) else [None]
                if not isinstance(op["targets"], list) or not (2 <= len(op["targets"]) <= 4):
                    problems.append("%s: a group joins 2 to 4 places" % ow)
            for t in targets:
                if not find_target(line_text, t):
                    problems.append("%s: %r is not found on the line \"%s\"" % (ow, t, line_text))
            if kind == "mark" and op["shape"] not in ("underline", "circle", "box"):
                problems.append("%s: shape must be underline, circle or box" % ow)
            if kind == "note" and op.get("place", "above") not in ("above", "below"):
                problems.append("%s: place must be above or below" % ow)
            if kind in ("both", "divide") and "=" not in line_text:
                problems.append("%s: '%s' needs a line with an equals sign" % (ow, kind))
            for key in ("note", "text", "by", "label"):
                if key in op and kind != "write":
                    v = op[key]
                    if not isinstance(v, str) or not v.strip() or len(v) > 24:
                        problems.append("%s.%s: 1 to 24 characters" % (ow, key))
                    else:
                        grounded |= set(number_tokens(v))
                        if BANNED_WORDS.search(v):
                            problems.append("%s.%s: uses a word the tone rule bans" % (ow, key))

        ask = beat.get("ask")
        if ask is not None:
            asks += 1
            if last_was_ask:
                problems.append("%s: two asks in a row; say or show something in between" % where)
            kind = ask.get("kind") if isinstance(ask, dict) else None
            if kind == "think":
                if set(ask) != {"kind"}:
                    problems.append("%s.ask: a 'think' ask has nothing else" % where)
            elif kind == "choose":
                choices = ask.get("choices")
                ok = set(ask) == {"kind", "choices", "answer", "ifNot"} and isinstance(choices, list) and 2 <= len(choices) <= 4 \
                    and all(isinstance(c, str) and 0 < len(c) <= 40 for c in choices) and len(set(choices)) == len(choices) \
                    and isinstance(ask.get("answer"), int) and not isinstance(ask.get("answer"), bool) and 0 <= ask["answer"] < len(choices)
                if not ok:
                    problems.append("%s.ask: 'choose' needs 2 to 4 different choices (each up to 40 characters), answer (index) and ifNot" % where)
                else:
                    for c in choices:
                        grounded |= set(number_tokens(c))
                        if BANNED_WORDS.search(c):
                            problems.append("%s.ask: a choice uses a word the tone rule bans" % where)
                    problems += check_say(ask["ifNot"], where + ".ask.ifNot", grounded)
            else:
                problems.append("%s.ask: kind must be 'choose' or 'think'" % where)
        last_was_ask = ask is not None

        # What is said may use anything the question states or the board shows by the end of this beat.
        problems += check_say(beat.get("say"), where + ".say", grounded)

    if first_write_tone != "given":
        problems.append("%s: the first thing written must be the question itself, with tone 'given'" % qid)
    if asks == 0:
        problems.append("%s: the child never gets a turn; add at least one ask" % qid)
    if isinstance(beats[-1], dict) and beats[-1].get("ask") is not None:
        problems.append("%s: the lesson must not end on an ask" % qid)
    if not answer_lines:
        problems.append("%s: write the final answer on the board with tone 'answer'" % qid)
    elif answer_tokens:
        said_at_end = set()
        for text in answer_lines[-1:]:
            said_at_end |= set(number_tokens(text))
        for beat in beats[-2:]:
            if isinstance(beat, dict) and isinstance(beat.get("say"), str):
                said_at_end |= set(number_tokens(beat["say"]))
        if not answer_tokens <= said_at_end:
            problems.append("%s: the lesson must end on the keyed answer %r" % (qid, correct_text(q)))
    return problems


# ── Running it ───────────────────────────────────────────────────────────────

def load_seed():
    """Every question a lesson may be written for: Grade 5 and Grade 4."""
    questions = bank.load_by_id(topic_id="grade5")
    questions.update((q["id"], q) for q in bank.load_bank(4))
    return questions


def show(qid, questions):
    q = questions.get(qid)
    if not q:
        sys.exit("not a Grade 4 or Grade 5 question: %s" % qid)
    print("QUESTION  %s" % q["questionText"])
    print("CHOICES   %s   (key %s)" % (" | ".join(option_texts(q)), q.get("correctAnswer")))
    for s in q.get("stepByStep") or []:
        print("STEP      %s" % s.get("text", ""))
    for path in sorted(glob.glob(os.path.join(PARTS, "*.json"))):
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        if qid not in part:
            continue
        print("\nLESSON in %s" % os.path.basename(path))
        for i, beat in enumerate(part[qid].get("beats", [])):
            print("\n %2d  SAY   %s" % (i + 1, beat.get("say", "")))
            for op in beat.get("board", []):
                rest = {k: v for k, v in op.items() if k != "op"}
                print("     BOARD %-7s %s" % (op.get("op"), json.dumps(rest, ensure_ascii=False)))
            if beat.get("ask"):
                print("     ASK   %s" % json.dumps(beat["ask"], ensure_ascii=False))
        for p in check_script(qid, part[qid], q):
            print("PROBLEM   " + p)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--part", help="check only this part (name without .json)")
    parser.add_argument("--show", help="print one question and its lesson")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--max", type=int, default=60)
    args = parser.parse_args()

    questions = load_seed()
    if args.show:
        show(args.show, questions)
        return
    if args.build and args.part:
        sys.exit("--build always uses every part; drop --part")

    files = [os.path.join(PARTS, args.part + ".json")] if args.part else sorted(glob.glob(os.path.join(PARTS, "*.json")))
    merged = {}
    owner = {}
    problems = []
    for path in files:
        name = os.path.splitext(os.path.basename(path))[0]
        if not os.path.exists(path):
            problems.append("%s: no part file yet" % name)
            continue
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        good = 0
        kinds = collections.Counter()
        for qid, script in part.items():
            if qid not in questions:
                problems.append("%s: %s is not a Grade 4 or Grade 5 question" % (name, qid))
                continue
            if qid in merged:
                problems.append("%s: %s already has a lesson in %s" % (name, qid, owner[qid]))
                continue
            found = check_script(qid, script, questions[qid])
            problems += found
            if not found:
                good += 1
                merged[qid] = script
                owner[qid] = name
                kinds[script.get("origin")] += 1
        print("  %-22s %4d lessons pass, of %d  (%s)" % (name, good, len(part), ", ".join("%d %s" % (n, k) for k, n in kinds.items())))

    if problems:
        print("\n%d PROBLEMS" % len(problems))
        for p in problems[:args.max]:
            print("  " + p)
        if len(problems) > args.max:
            print("  ... and %d more (use --max)" % (len(problems) - args.max))
        sys.exit(1)

    print("all checks passed")
    if args.build:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        served = {k: {kk: vv for kk, vv in merged[k].items() if kk == "beats"} for k in sorted(merged)}
        with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump(served, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        print("wrote %s (%d lessons)" % (os.path.relpath(OUT, ROOT), len(served)))


if __name__ == "__main__":
    main()
