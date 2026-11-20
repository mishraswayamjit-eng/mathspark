"""Build data/teach/parts/g4-gr4_factors.json: a lesson for every Grade 4 question in gr4_factors.

    python -X utf8 scripts/teach/gen/g4_gr4_factors.py

Questions that share a family wording are written by rule (g4_gr4_factors_rules*.py). All the
others are written by hand (g4_gr4_factors_authored_*.py). Then check with:

    python -X utf8 scripts/teach/validate.py --part g4-gr4_factors
"""
import collections
import glob
import importlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402
from g4_gr4_factors_lib import factors, gcd, lcm  # noqa: E402
from g4_gr4_factors_rules import hcf_how, hcf_lesson  # noqa: E402
from g4_gr4_factors_rules3 import lcm_hcf_lesson  # noqa: E402
from g4_gr4_factors_rules2 import count_factors_lesson, count_multiples_lesson, lcm_how, lcm_lesson  # noqa: E402

TOPIC = "gr4_factors"
OUT = os.path.join(ROOT, "data", "teach", "parts", "g4-%s.json" % TOPIC)
FIGS = os.path.join(ROOT, "data", "question-figures", "parts", "g4-%s.json" % TOPIC)


def keyed(q):
    opts = [o.get("text", "") if isinstance(o, dict) else str(o) for o in q.get("options", [])]
    return opts["ABCD".index(q["correctAnswer"])]


def by_rule(q, figs):
    """(wording, lesson, the answer the rule reached) for a family wording, or (None, None, None)."""
    text = q["questionText"].strip()
    qid = q["id"]
    m = re.fullmatch(r"(?:Find the HCF|(?:The )?H\.?C\.?F\.?) of (\d+) and (\d+)(?:\.| is:|\?)", text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "HCF of a and b (%s)" % hcf_how(a, b), hcf_lesson(qid, a, b), gcd(a, b)
    m = re.fullmatch(r"(?:Find the LCM|(?:The )?L\.?C\.?M\.?) of (\d+) and (\d+)(?:\.| is:|\?)", text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "LCM of a and b (%s)" % lcm_how(a, b), lcm_lesson(qid, a, b), lcm(a, b)
    m = re.fullmatch(r"Difference between LCM and HCF of (\d+) and (\d+)\?", text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "LCM and HCF of a and b, then one more step", lcm_hcf_lesson(qid, a, b, "diff"), lcm(a, b) - gcd(a, b)
    m = re.fullmatch(r"(?:Sum of LCM and HCF of|What is the sum of the L\.C\.M\. and H\.C\.F\. of the numbers) (\d+) and (\d+)\?", text)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        return "LCM and HCF of a and b, then one more step", lcm_hcf_lesson(qid, a, b, "sum"), lcm(a, b) + gcd(a, b)
    m = re.fullmatch(r"LCM of (\d+) and (\d+) divided by HCF of (\d+) and (\d+)\?", text)
    if m and m.group(1) == m.group(3) and m.group(2) == m.group(4):
        a, b = int(m.group(1)), int(m.group(2))
        return "LCM and HCF of a and b, then one more step", lcm_hcf_lesson(qid, a, b, "ratio"), lcm(a, b) // gcd(a, b)
    m = re.fullmatch(r"How many factors does (\d+) have\?", text)
    if m:
        n = int(m.group(1))
        return "How many factors does n have", count_factors_lesson(qid, n), len(factors(n))
    m = re.fullmatch(r"How many numbers from (\d+) to (\d+) are divisible by (\d+)\?", text)
    if m:
        lo, hi, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        figure = None
        steps = (figs.get(qid) or {}).get("stepFigures") or []
        if steps and isinstance(steps[-1], dict) and steps[-1].get("kind") == "numberLine":
            figure = dict(steps[-1])
            figure["note"] = "Multiples of %d from %d to %d" % (d, lo, hi)
        return "How many numbers from a to b are divisible by d", count_multiples_lesson(qid, lo, hi, d, figure), hi // d - (lo - 1) // d
    return None, None, None


def lint(qid, script):
    """Things the checker does not look at, but a reader would trip on."""
    notes = []
    lines = {}
    for i, beat in enumerate(script["beats"]):
        if len(beat["say"]) > 240:
            notes.append("%s beat %d: %d characters said" % (qid, i + 1, len(beat["say"])))
        for op in beat.get("board", []):
            if op["op"] == "write":
                lines[op["id"]] = op["text"]
            if op["op"] == "clear":
                lines = {}
            targets = []
            if op["op"] in ("mark", "strike", "note"):
                targets = [op["target"]]
            elif op["op"] == "arc":
                targets = [op["from"]] + op["to"]
            elif op["op"] == "group":
                targets = op["targets"]
            text = lines.get(op.get("line"), "")
            for t in targets:
                # A mark on a number must land on the whole number, not on digits inside a longer one,
                # unless the line is a bare number (digits are marked on purpose there).
                if not re.fullmatch(r"\d+", t["text"]) or re.fullmatch(r"[\d,★ ]+", text):
                    continue
                pos, start = -1, 0
                for _ in range(t.get("nth", 1)):
                    pos = text.find(t["text"], start)
                    start = pos + 1
                    if pos == -1:
                        break
                if pos == -1:
                    continue
                before = text[pos - 1] if pos > 0 else " "
                after = text[pos + len(t["text"])] if pos + len(t["text"]) < len(text) else " "
                if before.isdigit() or after.isdigit():
                    notes.append("%s beat %d: the mark on %r lands inside a longer number on \"%s\"" % (qid, i + 1, t["text"], text))
    return notes


def main():
    questions = [q for q in bank.load_bank(4) if q.get("node") == TOPIC]
    figs = {}
    if os.path.exists(FIGS):
        with io.open(FIGS, encoding="utf-8") as f:
            figs = json.load(f)
    lessons = collections.OrderedDict()
    wordings = collections.Counter()
    authored = {}
    for path in sorted(glob.glob(os.path.join(HERE, "g4_gr4_factors_authored_*.py"))):
        module = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        for qid, script in module.LESSONS.items():
            if qid in authored:
                sys.exit("two hand-written lessons for %s" % qid)
            authored[qid] = script

    missing = []
    for q in questions:
        qid = q["id"]
        if qid in authored:
            lessons[qid] = authored[qid]
            wordings["written by hand"] += 1
            continue
        wording, lesson, answer = by_rule(q, figs)
        if lesson:
            if str(answer) != keyed(q).strip():
                sys.exit("%s: the rule reaches %s but the key is %r" % (qid, answer, keyed(q)))
            lessons[qid] = lesson
            wordings[wording] += 1
            continue
        missing.append(qid)
    stray = sorted(set(authored) - {q["id"] for q in questions})
    if stray:
        sys.exit("hand-written lessons for questions not in this topic: %s" % ", ".join(stray))

    notes = []
    for qid, script in lessons.items():
        notes += lint(qid, script)

    # The right choice must not always be the first button: where it is first, move it to
    # a place picked by a stable hash of the question id and the beat.
    import hashlib
    for qid, script in lessons.items():
        for i, beat in enumerate(script["beats"]):
            ask = beat.get("ask")
            if ask and ask.get("kind") == "choose" and ask["answer"] == 0:
                to = int(hashlib.md5(("%s:%d" % (qid, i)).encode("utf-8")).hexdigest(), 16) % len(ask["choices"])
                ask["choices"][0], ask["choices"][to] = ask["choices"][to], ask["choices"][0]
                ask["answer"] = to

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(lessons, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print("%d questions in the topic, %d lessons written to %s" % (len(questions), len(lessons), os.path.relpath(OUT, ROOT)))
    for wording, n in sorted(wordings.items()):
        print("  %4d  %s" % (n, wording))
    if missing:
        print("%d without a lesson" % len(missing))
    for n in notes:
        print("NOTE  " + n)


if __name__ == "__main__":
    main()
