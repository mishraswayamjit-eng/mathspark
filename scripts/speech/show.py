"""Read narration next to its source, the way a reviewer would.

    python -X utf8 scripts/speech/show.py --topic fractions --list          # every question in the topic, one line each
    python -X utf8 scripts/speech/show.py --topic fractions --n 15 --seed 3 # a random sample, source and narration together
    python -X utf8 scripts/speech/show.py --id EXT_G5_FP_2025_011           # one question
    python -X utf8 scripts/speech/show.py --topic fractions --source --from 0 --to 40   # the source material only

`--source` prints what has to be narrated, as JSON, for writing narration by hand.
"""
import argparse
import io
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import PARTS, TOPICS, load_grade5, source_strings, topic_of  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--topic", choices=TOPICS)
    parser.add_argument("--id")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--source", action="store_true")
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--from", dest="start", type=int, default=0)
    parser.add_argument("--to", dest="end", type=int, default=None)
    args = parser.parse_args()

    questions = load_grade5()
    if args.id:
        chosen = [q for q in questions if q["id"] == args.id]
        topic = topic_of(chosen[0]) if chosen else None
    else:
        if not args.topic:
            sys.exit("give --topic or --id")
        topic = args.topic
        chosen = sorted((q for q in questions if topic_of(q) == topic), key=lambda q: q["id"])
    if not chosen:
        sys.exit("no such question")

    if args.list:
        for i, q in enumerate(chosen):
            print("%4d  %-34s %-26s %s" % (i, q["id"], q.get("source", ""), q["questionText"][:90].replace("\n", " ")))
        print("%d questions" % len(chosen))
        return

    if args.source:
        out = {q["id"]: source_strings(q) for q in chosen[args.start:args.end]}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return

    part = {}
    path = os.path.join(PARTS, "%s.json" % topic)
    if os.path.exists(path):
        with io.open(path, encoding="utf-8") as f:
            part = json.load(f)
    if not args.id:
        random.seed(args.seed)
        chosen = random.sample(chosen, min(args.n, len(chosen)))
    for q in chosen:
        src = source_strings(q)
        said = part.get(q["id"])
        print("=" * 100)
        print(q["id"], "|", q.get("subTopic", ""), "|", q.get("source", ""))
        for key in ("q", "options", "hints", "steps"):
            items = [src[key]] if key == "q" else src[key]
            spoken = None if said is None else ([said[key]] if key == "q" else said[key])
            for i, text in enumerate(items):
                label = key if key == "q" else "%s[%d]" % (key, i)
                print("  %-10s PRINT  %s" % (label, text))
                if spoken is not None and i < len(spoken):
                    print("  %-10s SPOKEN %s" % ("", spoken[i]))
        if said is None:
            print("  (no narration yet)")


if __name__ == "__main__":
    main()
