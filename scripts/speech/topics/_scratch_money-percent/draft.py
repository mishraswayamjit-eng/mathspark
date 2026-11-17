"""Show new questions (not in the baseline): source, what the script says, and checker problems.

    python -X utf8 scripts/speech/topics/_scratch_money-percent/draft.py FROM TO [fails|compact|stats]

compact: print only the spoken line where it differs from print; always print problems.
"""
import importlib.util
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOPICS_DIR = os.path.dirname(HERE)
SPEECH = os.path.dirname(TOPICS_DIR)
sys.path.insert(0, TOPICS_DIR)
sys.path.insert(0, SPEECH)
from common import load_grade5, source_strings, topic_of  # noqa: E402
import validate  # noqa: E402

spec = importlib.util.spec_from_file_location("mp", os.path.join(TOPICS_DIR, "money-percent.py"))
mp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mp)

with io.open(os.path.join(HERE, "baseline.json"), encoding="utf-8") as f:
    BASE = json.load(f)


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    end = int(sys.argv[2]) if len(sys.argv) > 2 else None
    mode = sys.argv[3] if len(sys.argv) > 3 else ""
    qs = sorted((q for q in load_grade5() if topic_of(q) == "money-percent" and q["id"] not in BASE), key=lambda q: q["id"])
    total_fail = 0
    for idx, q in enumerate(qs[start:end], start):
        entry = mp.entry_for(q)
        problems = validate.check_entry(q["id"], entry, q)
        total_fail += 1 if problems else 0
        if mode == "stats":
            continue
        if mode == "list":
            print(idx, q["id"][:22], "|", q["questionText"][:110].replace("\n", " "), "| steps", len(source_strings(q)["steps"]))
            continue
        if mode == "fails" and not problems:
            continue
        src = source_strings(q)
        if mode == "prose":
            import re
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = [entry[key]] if key == "q" else entry[key]
                for i, text in enumerate(items):
                    risky = re.search(r"[=×÷+−/→()<>*_₁₂≈…⏰']|\b[A-Z]{2,}\b| - |\d[A-Za-z]\b", text.replace("'s", "")) is not None
                    if risky:
                        continue
                    simple = re.sub(r"₹\s*([\d,.]*\d)", r"\1 rupees", text)
                    simple = re.sub(r"\s*%", " percent", simple).replace(" — ", ", ").replace("—", ", ").strip()
                    simple = re.sub(r":$", ".", simple)
                    if key == "options":
                        simple = simple.rstrip(".")
                    elif simple and simple[-1] not in ".?!":
                        simple += "."
                    if simple != spoken[i]:
                        print("%d %s%d P %s" % (idx, key[0], i, text))
                        print("       S %s" % spoken[i])
            continue
        if mode in ("math", "spoken"):
            import re
            print("## %d %s" % (idx, q["id"][13:21]))
            for key in ("q", "options", "hints", "steps"):
                items = [src[key]] if key == "q" else src[key]
                spoken = [entry[key]] if key == "q" else entry[key]
                for i, text in enumerate(items):
                    label = key if key == "q" else "%s%d" % (key[0], i)
                    risky = re.search(r"[=×÷+−/→()<>*_₁₂≈…⏰']|\b[A-Z]{2,}\b| - |\d[A-Za-z]\b", text.replace("'s", "")) is not None
                    if mode == "spoken" or risky:
                        print(" %-3s %s" % (label, spoken[i]))
            continue
        print("=" * 90)
        print(idx, q["id"], "|", q.get("subTopic", ""), "| answer", q.get("correctAnswer"))
        for key in ("q", "options", "hints", "steps"):
            items = [src[key]] if key == "q" else src[key]
            spoken = [entry[key]] if key == "q" else entry[key]
            for i, text in enumerate(items):
                label = key if key == "q" else "%s%d" % (key[0], i)
                print(" %-3s P %s" % (label, text))
                if i < len(spoken) and spoken[i] != text:
                    print("     S %s" % spoken[i])
        own = q.get("stepByStep") or []
        for i, s in enumerate(own):
            if s.get("latex"):
                print(" s%d latex: %s" % (i, s["latex"]))
        for p in problems:
            print(" !! " + p)
    print("%d questions, %d with problems" % (len(qs[start:end]), total_fail))


if __name__ == "__main__":
    main()
