"""Write the review inputs for making printed steps follow the lesson (imported Grade 5).

    python -X utf8 scripts/fixes/steps_inputs.py [parts]

A question is a candidate when its worked steps use a value that is neither in the
question, nor in its answer choices, nor anywhere in its 'Explain it to me' lesson (so the
steps and the lesson reach the answer by different working), or when a step breaks a
writing rule (a banned word, thinking aloud, markdown asterisks).
Writes data/bank-import/repairs/steps-in-NN.json. Reads only.
"""
import collections
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
sys.path.insert(0, os.path.join(ROOT, "scripts", "speech"))
import bank  # noqa: E402
import common  # noqa: E402

OUT = os.path.join(ROOT, "data", "bank-import", "repairs")
IMPORTED = ("ai_generated", "ipm_textbook", "official_ipm_2020")
STYLE = [
    ("banned word", re.compile(r"\b(wrong|incorrect|failed|fail|error)\b", re.I)),
    ("thinks aloud", re.compile(r"\b(wait|hmm+|oops|nope|doesn'?t work|actually correct)\b", re.I)),
    ("markdown asterisks", re.compile(r"\*\*[^*]+\*\*")),
]


def load_parts(folder):
    out = {}
    for path in sorted(glob.glob(os.path.join(ROOT, folder, "*.json"))):
        with io.open(path, encoding="utf-8") as f:
            out.update(json.load(f))
    return out


def nums(text):
    return set(str(t).replace(",", "") for t in common.number_tokens(text or ""))


def lesson_digest(lesson):
    lines = []
    for beat in lesson.get("beats", []):
        writes = [b.get("text", "") for b in beat.get("board", []) if b.get("op") == "write"]
        line = beat.get("say", "")
        if writes:
            line += "   [board: " + " | ".join(writes) + "]"
        lines.append(line)
    return lines


def main():
    parts = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    names = {n["id"]: n["name"] for n in bank.tree_nodes(5)}
    lessons = load_parts("data/teach/parts")
    figures = load_parts("data/question-figures/parts")
    rows = sorted([q for q in bank.load_bank(5) if q.get("source") in IMPORTED], key=lambda q: (q.get("node") or "", q["id"]))
    picked = []
    why_count = collections.Counter()
    for q in rows:
        steps = [s if isinstance(s, dict) else {"text": s} for s in (q.get("stepByStep") or [])]
        lesson = lessons.get(q["id"])
        if not steps or not lesson:
            continue
        step_text = " ".join((s.get("text") or "") + " " + (s.get("latex") or "") for s in steps)
        known = nums(q.get("questionText")) | nums(" ".join(o["text"] for o in q["options"])) | nums(json.dumps(lesson, ensure_ascii=False))
        extra = sorted(nums(step_text) - known - set(str(i) for i in range(0, 11)))
        why = []
        if len(extra) >= 2:
            why.append("steps use values the lesson never does: " + ", ".join(extra[:8]))
        for label, rx in STYLE:
            if any(rx.search(s.get("text") or "") for s in steps):
                why.append("a step " + ("uses a " + label if label == "banned word" else label if label != "markdown asterisks" else "has markdown asterisks"))
        if not why:
            continue
        for w in why:
            why_count[w.split(":")[0]] += 1
        fig = figures.get(q["id"]) or {}
        picked.append({
            "id": q["id"], "topic": names.get(q.get("node")), "flagged": why,
            "question": q.get("questionText"), "options": {o["id"]: o["text"] for o in q["options"]},
            "answer": q.get("correctAnswer"),
            "steps": [{k: s[k] for k in ("text", "latex") if s.get(k)} for s in steps],
            "lesson": lesson_digest(lesson),
            "stepPictures": [(f.get("note") or f.get("kind")) if f else None for f in fig.get("stepFigures", [])] if fig.get("stepFigures") else None,
        })

    print("%d imported questions, %d candidates" % (len(rows), len(picked)))
    for w, n in why_count.most_common():
        print("  %4d  %s" % (n, w))
    size = (len(picked) + parts - 1) // parts
    for i in range(parts):
        chunk = picked[i * size:(i + 1) * size]
        with io.open(os.path.join(OUT, "steps-in-%02d.json" % (i + 1)), "w", encoding="utf-8", newline="\n") as f:
            json.dump(chunk, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("steps-in-%02d.json  %d questions, %d KB" % (i + 1, len(chunk), os.path.getsize(os.path.join(OUT, "steps-in-%02d.json" % (i + 1))) // 1024))


if __name__ == "__main__":
    main()
