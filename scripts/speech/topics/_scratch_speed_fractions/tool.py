"""Scratch helper for the measurement-speed and fractions narration of imported questions.

    python -X utf8 scripts/speech/topics/_scratch_speed_fractions/tool.py snapshot   # save the part files as they are now (once)
    python -X utf8 scripts/speech/topics/_scratch_speed_fractions/tool.py compare    # every snapshot entry unchanged in the part file?
    python -X utf8 scripts/speech/topics/_scratch_speed_fractions/tool.py source <slug> [from] [to]   # source of the new questions
    python -X utf8 scripts/speech/topics/_scratch_speed_fractions/tool.py show <slug> [from] [to]     # source and narration of new questions
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
from common import PARTS, load_grade5, source_strings, topic_of  # noqa: E402

SLUGS = ("measurement-speed", "fractions")


def read(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def snap_path(slug):
    return os.path.join(HERE, "before_%s.json" % slug)


def new_questions(slug):
    before = json.loads(read(snap_path(slug)))
    return sorted((q for q in load_grade5() if topic_of(q) == slug and q["id"] not in before), key=lambda q: q["id"])


def main():
    cmd = sys.argv[1]
    if cmd == "snapshot":
        for slug in SLUGS:
            if os.path.exists(snap_path(slug)):
                print("snapshot exists, kept:", slug)
                continue
            text = read(os.path.join(PARTS, slug + ".json"))
            with io.open(snap_path(slug), "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print("saved", slug, len(json.loads(text)), "entries")
    elif cmd == "compare":
        for slug in SLUGS:
            before = json.loads(read(snap_path(slug)))
            now = json.loads(read(os.path.join(PARTS, slug + ".json")))
            changed = [k for k in before if json.dumps(before[k], ensure_ascii=False) != json.dumps(now.get(k), ensure_ascii=False)]
            # byte check: the old file's text for each entry must appear verbatim in the new file
            old_text, new_text = read(snap_path(slug)), read(os.path.join(PARTS, slug + ".json"))
            byte_bad = 0
            for k in before:
                chunk = json.dumps({k: before[k]}, ensure_ascii=False, indent=1)[2:-2]
                if chunk not in old_text:
                    sys.exit("snapshot is not in the expected layout: " + k)
                if chunk not in new_text:
                    byte_bad += 1
            print("%s: %d before, %d now, %d added, %d changed, %d not byte-identical" % (
                slug, len(before), len(now), len(set(now) - set(before)), len(changed), byte_bad))
            for k in changed[:20]:
                print("   CHANGED", k)
    elif cmd == "spoken":
        slug = sys.argv[2]
        start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        end = int(sys.argv[4]) if len(sys.argv) > 4 else None
        part = json.loads(read(os.path.join(PARTS, slug + ".json")))
        for q in new_questions(slug)[start:end]:
            said = part[q["id"]]
            print("=" * 60)
            print(q["id"])
            if "q" in sys.argv[5:]:
                print("  q  " + said["q"])
                print("  o  " + " | ".join(said["options"]))
                continue
            for key in ("hints", "steps"):
                for i, text in enumerate(said[key]):
                    print("  %s%d %s" % (key[0], i, text))
    elif cmd in ("source", "show"):
        slug = sys.argv[2]
        start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
        end = int(sys.argv[4]) if len(sys.argv) > 4 else None
        part = json.loads(read(os.path.join(PARTS, slug + ".json")))
        qs = new_questions(slug)
        print("%d new questions" % len(qs))
        for q in qs[start:end]:
            src = source_strings(q)
            said = part.get(q["id"]) if cmd == "show" else None
            print("=" * 90)
            print(q["id"], "|", q.get("subTopic", ""), "|", q.get("source", ""))
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = None if said is None else ([said[key]] if key == "q" else said[key])
                for i, text in enumerate(items):
                    print("  %-9s P %s" % (key if key == "q" else "%s[%d]" % (key, i), text))
                    if spoken is not None and i < len(spoken) and spoken[i] != text:
                        print("  %-9s S %s" % ("", spoken[i]))
            own = q.get("stepByStep") or []
            for i, s in enumerate(own):
                if s.get("latex"):
                    print("  latex[%d]   %s" % (i, s["latex"]))


if __name__ == "__main__":
    main()
