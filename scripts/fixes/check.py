"""Check proposed fixes to question hints and steps.

    python -X utf8 scripts/fixes/check.py                       # every part file
    python -X utf8 scripts/fixes/check.py --part generated-hints
    python -X utf8 scripts/fixes/check.py --show <question id>   # the question as it stands, with any fix

A part file is data/question-fixes/parts/<name>.json:
    { "<question id>": { "hints": ["...", "...", "..."], "steps": [{"text": "...", "latex": ""}], "why": "..." } }
Give only the fields you are replacing (`hints`, `steps`, or both) plus `why`.
The part named `answers` may also give `options`, `correctAnswer` or `questionText`, each with a `proof`.

What is enforced:
  - hints: exactly three, each real guidance for THIS question, none of them stating the answer;
  - steps: two to five, in plain words, the last one stating the correct answer, no filler
    ("The answer is option B"), no thinking aloud ("hmm", "wait", "let me recheck");
  - every piece of arithmetic written out in a hint or step is actually true;
  - nothing uses a word the tone rule bans.
Exit code 1 if anything fails.
"""
import argparse
import glob
import io
import json
import os
import re
import sys
from fractions import Fraction

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)

PARTS = os.path.join(ROOT, "data", "question-fixes", "parts")

BANNED = re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)
THINKING = re.compile(r"\b(hmm+|wait|recheck|re-check|re-examine|let me|actually|oops|but option)\b", re.I)
FILLER = re.compile(r"\b(the answer is option|check the answer matches|answer matches option|apply the relevant formula|option [A-D]\b)", re.I)
GENERIC = [
    "read the question carefully", "try working step by step", "check your answer by substituting back",
    "this tests your understanding", "identify what's being asked", "identify what is being asked",
]
GROUPED = re.compile(r"(?<![\d,])(?:\d{1,3}(?:,\d{3})+|\d{1,2}(?:,\d{2})+,\d{3})(?!\d)(?!,\d)")
NUMBER = re.compile(r"\d+(?:\.\d+)?")


def ungroup(text):
    return GROUPED.sub(lambda m: m.group(0).replace(",", ""), text)


def numbers_in(text):
    return {Fraction(m) for m in NUMBER.findall(ungroup(text))}


# ── Arithmetic that is written out must be true ──────────────────────────────

_RUN = re.compile(r"[0-9(][0-9 .()+\-−–×x*÷/=]*=[0-9 .()+\-−–×x*÷/=]*[0-9)]")
_TOKEN = re.compile(r"\d+(?:\.\d+)?|[()+\-*/]")


def _value(expr):
    """The exact value of a plain arithmetic expression, or None if it is not one."""
    s = expr.replace("×", "*").replace("x", "*").replace("÷", "/").replace("−", "-").replace("–", "-").strip()
    if not s or re.search(r"[^0-9 .()+\-*/]", s):
        return None
    tokens = _TOKEN.findall(s)
    if "".join(tokens) != s.replace(" ", ""):
        return None
    pos = [0]

    def peek():
        return tokens[pos[0]] if pos[0] < len(tokens) else None

    def take():
        pos[0] += 1
        return tokens[pos[0] - 1]

    def atom():
        t = peek()
        if t == "(":
            take()
            v = total()
            if peek() != ")":
                raise ValueError
            take()
            return v
        if t == "-":
            take()
            return -atom()
        if t is None or not re.match(r"\d", t):
            raise ValueError
        return Fraction(take())

    def product():
        v = atom()
        while peek() in ("*", "/"):
            op = take()
            w = atom()
            if op == "/" and w == 0:
                raise ValueError
            v = v * w if op == "*" else v / w
        return v

    def total():
        v = product()
        while peek() in ("+", "-"):
            op = take()
            w = product()
            v = v + w if op == "+" else v - w
        return v

    try:
        v = total()
        return v if pos[0] == len(tokens) else None
    except (ValueError, ZeroDivisionError):
        return None


def false_arithmetic(text):
    """Written-out sums in `text` that do not hold, as strings. '≈' is never checked."""
    out = []
    clean = ungroup(text)
    for k, v in {"½": "(1/2)", "¼": "(1/4)", "¾": "(3/4)", "⅓": "(1/3)", "⅔": "(2/3)"}.items():
        clean = clean.replace(k, v)
    for match in _RUN.finditer(clean):
        run = match.group(0)
        # A run that starts mid-calculation ("x × 20 × 7 = 70", "5% of 250 × ...") is not the whole sum.
        before = clean[:match.start()].rstrip()[-1:]
        after = clean[match.end():].lstrip()[:1]
        if before and (before in "×x*÷/+-−–%^√(=" or before.isalpha() and clean[match.start() - 1:match.start()] != " "):
            continue
        if after and after in "×*÷/+−–%^":
            continue
        # "20000 ÷ 300 = 66 remainder 200" is a true statement about a division that does not go exactly.
        tail = clean[match.end():].lstrip().lower()
        if tail.startswith(("remainder", "rem ", "r ", "left over")) and "÷" in run:
            continue
        sides = run.split("=")
        values = [_value(s) for s in sides]
        for i in range(len(sides) - 1):
            a, b = values[i], values[i + 1]
            if a is None or b is None:
                continue
            # A side that is a bare number next to a real calculation: they must agree.
            if not (re.search(r"[+\-−–×x*÷/]", sides[i]) or re.search(r"[+\-−–×x*÷/]", sides[i + 1])):
                continue
            # Allow a decimal that is the calculation rounded to the places shown.
            shown = sides[i + 1].strip() if re.fullmatch(r"\s*\d+\.\d+\s*", sides[i + 1]) else None
            if a != b:
                if shown is not None and abs(a - b) <= Fraction(1, 2 * 10 ** len(shown.split(".")[1])):
                    continue
                out.append("%s = %s" % (sides[i].strip(), sides[i + 1].strip()))
    return out


# ── Checks ───────────────────────────────────────────────────────────────────

def option_texts(q):
    return [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]


def correct_text(q, fix=None):
    letter = (fix or {}).get("correctAnswer") or q.get("correctAnswer")
    options = (fix or {}).get("options") or option_texts(q)
    idx = "ABCD".find(letter)
    return options[idx] if 0 <= idx < len(options) else ""


def answer_numbers(q, fix=None):
    """Numbers that would give the answer away: in the correct choice, not in the question, and not tiny."""
    question = numbers_in((fix or {}).get("questionText") or q.get("questionText", ""))
    return {n for n in numbers_in(correct_text(q, fix)) if n not in question and (n >= 10 or n.denominator != 1)}


def check_entry(qid, fix, q, part_name):
    problems = []
    allowed = {"hints", "steps", "why"}
    if part_name == "answers":
        allowed |= {"options", "correctAnswer", "questionText", "proof"}
    for key in fix:
        if key not in allowed:
            problems.append("%s: field '%s' is not allowed in this part" % (qid, key))
    if not isinstance(fix.get("why"), str) or len(fix["why"].strip()) < 8:
        problems.append("%s: needs a short 'why'" % qid)
    if not any(k in fix for k in ("hints", "steps", "options", "correctAnswer", "questionText")):
        problems.append("%s: changes nothing" % qid)
    if any(k in fix for k in ("options", "correctAnswer", "questionText")):
        if not isinstance(fix.get("proof"), str) or len(fix["proof"].strip()) < 20:
            problems.append("%s: a change to the question, choices or key needs a 'proof'" % qid)
        if "options" in fix and (not isinstance(fix["options"], list) or len(fix["options"]) != 4
                                 or len(set(fix["options"])) != 4 or not all(isinstance(o, str) and o.strip() for o in fix["options"])):
            problems.append("%s.options: needs four different, non-empty choices" % qid)
        if "correctAnswer" in fix and fix["correctAnswer"] not in ("A", "B", "C", "D"):
            problems.append("%s.correctAnswer: must be A, B, C or D" % qid)

    giveaway = answer_numbers(q, fix)

    if "hints" in fix:
        hints = fix["hints"]
        if not isinstance(hints, list) or len(hints) != 3 or not all(isinstance(h, str) and h.strip() for h in hints):
            problems.append("%s.hints: needs exactly three non-empty hints" % qid)
        else:
            if len(set(h.strip().lower() for h in hints)) != 3:
                problems.append("%s.hints: the three hints must be different" % qid)
            for i, h in enumerate(hints):
                where = "%s.hints[%d]" % (qid, i)
                if len(h) > 320:
                    problems.append("%s: %d characters, limit 320" % (where, len(h)))
                low = h.lower()
                if any(g in low for g in GENERIC):
                    problems.append("%s: generic filler; say something about this question" % where)
                if THINKING.search(h):
                    problems.append("%s: reads like thinking aloud" % where)
                if BANNED.search(h):
                    problems.append("%s: uses a word the tone rule bans" % where)
                leaked = sorted(n for n in numbers_in(h) if n in giveaway)
                if leaked:
                    problems.append("%s: states the answer (%s)" % (where, ", ".join(str(float(n)).rstrip("0").rstrip(".") for n in leaked)))
                for bad in false_arithmetic(h):
                    problems.append("%s: this sum is not true: %s" % (where, bad))

    if "steps" in fix:
        steps = fix["steps"]
        ok = isinstance(steps, list) and 2 <= len(steps) <= 5 and all(
            isinstance(s, dict) and set(s) <= {"text", "latex"} and isinstance(s.get("text"), str) and s["text"].strip()
            and isinstance(s.get("latex", ""), str) for s in steps)
        if not ok:
            problems.append("%s.steps: needs 2 to 5 steps, each {text, latex?}" % qid)
        else:
            for i, s in enumerate(steps):
                where = "%s.steps[%d]" % (qid, i)
                t = s["text"]
                if len(t) > 260:
                    problems.append("%s: %d characters, limit 260" % (where, len(t)))
                if FILLER.search(t):
                    problems.append("%s: filler; say the working, not the option letter" % where)
                if THINKING.search(t):
                    problems.append("%s: reads like thinking aloud" % where)
                if BANNED.search(t):
                    problems.append("%s: uses a word the tone rule bans" % where)
                for bad in false_arithmetic(t):
                    problems.append("%s: this sum is not true: %s" % (where, bad))
            answer = numbers_in(correct_text(q, fix))
            last = numbers_in(steps[-1]["text"] + " " + steps[-1].get("latex", ""))
            if answer and not answer <= last:
                problems.append("%s.steps: the last step must state the correct answer %r" % (qid, correct_text(q, fix)))
    return problems


def load_seed():
    return bank.load_by_id(topic_id="grade5")


def show(qid, questions):
    q = questions.get(qid)
    if not q:
        sys.exit("not a Grade 5 question: %s" % qid)
    print(json.dumps({k: q.get(k) for k in ("id", "subTopic", "source", "questionText", "options", "correctAnswer", "hints", "stepByStep")},
                     ensure_ascii=False, indent=1))
    for path in sorted(glob.glob(os.path.join(PARTS, "*.json"))):
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        if qid in part:
            print("\nFIX in %s:" % os.path.basename(path))
            print(json.dumps(part[qid], ensure_ascii=False, indent=1))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--part", help="check only this part (name without .json)")
    parser.add_argument("--show", help="print one question and any fix for it")
    parser.add_argument("--max", type=int, default=60)
    args = parser.parse_args()

    questions = load_seed()
    if args.show:
        show(args.show, questions)
        return

    files = [os.path.join(PARTS, args.part + ".json")] if args.part else sorted(glob.glob(os.path.join(PARTS, "*.json")))
    seen = {}
    problems = []
    for path in files:
        name = os.path.splitext(os.path.basename(path))[0]
        if not os.path.exists(path):
            problems.append("%s: no part file yet" % name)
            continue
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        good = 0
        for qid, fix in part.items():
            if qid not in questions:
                problems.append("%s: %s is not a Grade 5 question" % (name, qid))
                continue
            if qid in seen:
                problems.append("%s: %s is already fixed in %s" % (name, qid, seen[qid]))
                continue
            seen[qid] = name
            found = check_entry(qid, fix, questions[qid], name) if isinstance(fix, dict) else ["%s: must be an object" % qid]
            problems += found
            good += 0 if found else 1
        print("  %-22s %4d fixes pass, of %d" % (name, good, len(part)))

    if problems:
        print("\n%d PROBLEMS" % len(problems))
        for p in problems[:args.max]:
            print("  " + p)
        if len(problems) > args.max:
            print("  ... and %d more (use --max)" % (len(problems) - args.max))
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
