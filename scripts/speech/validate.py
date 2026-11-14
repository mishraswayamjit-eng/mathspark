"""Check question narration, and build the file the app serves.

    python -X utf8 scripts/speech/validate.py                 # check every part, print coverage
    python -X utf8 scripts/speech/validate.py --topic fractions
    python -X utf8 scripts/speech/validate.py --build         # check, then write src/data/questionSpeech/speech.json

A part file is data/question-speech/parts/<topic>.json:
    { "<question id>": { "q": "...", "options": ["...", "...", "...", "..."], "hints": ["...", "...", "..."], "steps": ["...", ...] } }

What is enforced, for every string:
  - it says the same numbers, in the same order, as the text it narrates (so narration can
    never change the maths, add a value, or give an answer away);
  - it is plain speakable words: no maths symbols, no slashes, no unit abbreviations;
  - it is present exactly where the source has text, and empty where the source is empty.
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import PARTS, ROOT, TOPICS, load_grade5, number_tokens, source_strings, topic_of  # noqa: E402

OUT = os.path.join(ROOT, "src", "data", "questionSpeech", "speech.json")
MAX_CHARS = 700

BANNED_CHARS = set("×÷=+%₹°√/\\^_{}<>*|□★≠≤≥~#@$")
ALLOWED_HIGH = set("’‘“”–—…")
ABBREVIATIONS = re.compile(r"\b(?:cm|mm|km|kg|mg|ml|sq|hr|hrs|kmph|Rs)\b\.?")
DIGIT_DASH = re.compile(r"\d\s*[-−–]\s*\d")


def check_string(spoken, source, where, also=None):
    """Problems with one narrated string. `also` is an alternative source it may match instead."""
    problems = []
    if not isinstance(spoken, str):
        return ["%s: must be text" % where]
    if not source.strip():
        if spoken.strip():
            problems.append("%s: the source is empty, so this must be empty" % where)
        return problems
    if not spoken.strip():
        return ["%s: missing (the source has text)" % where]
    if len(spoken) > MAX_CHARS:
        problems.append("%s: %d characters, limit %d" % (where, len(spoken), MAX_CHARS))
    bad = sorted({c for c in spoken if c in BANNED_CHARS or (ord(c) > 0x2000 and c not in ALLOWED_HIGH)})
    if bad:
        problems.append("%s: has symbols that cannot be spoken: %s" % (where, " ".join(bad)))
    m = ABBREVIATIONS.search(spoken)
    if m:
        problems.append("%s: write the unit out in full, not '%s'" % (where, m.group(0)))
    if DIGIT_DASH.search(spoken):
        problems.append("%s: a dash between numbers; say 'minus' or 'to'" % where)
    if spoken != spoken.strip() or "  " in spoken or "\n" in spoken:
        problems.append("%s: stray spaces or line breaks" % where)
    said = number_tokens(spoken)
    wanted = number_tokens(source)
    if said != wanted and not (also is not None and said == number_tokens(also)):
        problems.append("%s: numbers differ. Source has [%s], narration has [%s]" % (where, " ".join(wanted), " ".join(said)))
    return problems


def check_entry(qid, entry, q):
    if not isinstance(entry, dict) or set(entry) != {"q", "options", "hints", "steps"}:
        return ["%s: must have exactly q, options, hints, steps" % qid]
    src = source_strings(q)
    problems = check_string(entry["q"], src["q"], qid + ".q")
    for key in ("options", "hints", "steps"):
        if not isinstance(entry[key], list) or len(entry[key]) != len(src[key]):
            problems.append("%s.%s: needs %d entries" % (qid, key, len(src[key])))
            continue
        own = q.get("stepByStep") or []
        for i, spoken in enumerate(entry[key]):
            also = None
            if key == "steps" and i < len(own) and own[i].get("latex"):
                # A step may also say the numbers of its maths line.
                also = "%s %s" % (src[key][i], re.sub(r"\\[a-zA-Z]+", " ", own[i]["latex"]))
            problems += check_string(spoken, src[key][i], "%s.%s[%d]" % (qid, key, i), also)
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--topic", choices=TOPICS, help="check only this topic's part file")
    parser.add_argument("--build", action="store_true", help="write the merged file the app serves")
    parser.add_argument("--max", type=int, default=60, help="how many problems to print")
    args = parser.parse_args()
    if args.build and args.topic:
        sys.exit("--build always uses every part; drop --topic")

    questions = {q["id"]: q for q in load_grade5()}
    totals = collections.Counter(topic_of(q) for q in questions.values())
    files = [os.path.join(PARTS, args.topic + ".json")] if args.topic else sorted(glob.glob(os.path.join(PARTS, "*.json")))

    merged = {}
    covered = collections.Counter()
    problems = []
    for path in files:
        slug = os.path.splitext(os.path.basename(path))[0]
        if slug not in TOPICS:
            problems.append("%s: not a topic name" % os.path.basename(path))
            continue
        if not os.path.exists(path):
            problems.append("%s: no part file yet" % slug)
            continue
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
        for qid, entry in part.items():
            q = questions.get(qid)
            if q is None:
                problems.append("%s: %s is not a Grade 5 question" % (slug, qid))
            elif topic_of(q) != slug:
                problems.append("%s: %s belongs to topic %s" % (slug, qid, topic_of(q)))
            else:
                found = check_entry(qid, entry, q)
                problems += found
                if not found:
                    merged[qid] = entry
                    covered[slug] += 1

    for slug in ([args.topic] if args.topic else TOPICS):
        print("  %-22s %4d of %4d questions pass" % (slug, covered[slug], totals[slug]))
    print("  %-22s %4d of %4d" % ("total", sum(covered.values()), sum(totals[s] for s in ([args.topic] if args.topic else TOPICS))))

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
        with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
            json.dump({k: merged[k] for k in sorted(merged)}, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        print("wrote %s (%d questions)" % (os.path.relpath(OUT, ROOT), len(merged)))


if __name__ == "__main__":
    main()
