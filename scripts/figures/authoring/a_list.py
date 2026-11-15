"""List the Grade 5 past-paper questions of one year (or all) for authoring.
    python -X utf8 scripts/figures/authoring/a_list.py 2016
"""
import io, json, os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
YEARS = ["2016", "2017", "2018", "2019", "2020"]


def load():
    with io.open(os.path.join(ROOT, "data", "mathspark_complete_seed.json"), encoding="utf-8") as f:
        qs = json.load(f)["questions"]
    return [q for q in qs if q.get("topicId") == "grade5" and q.get("source") in ["g5_final_" + y for y in YEARS]]


if __name__ == "__main__":
    if sys.argv[1:2] == ["--covered"]:
        # Steps only, for the questions that have an entry in the part file, with each note beside its step.
        with io.open(os.path.join(ROOT, "data", "question-figures", "parts", "finals-2016-2020.json"), encoding="utf-8") as f:
            part = json.load(f)
        for q in load():
            if q["id"] not in part or (sys.argv[2:] and q["source"][-4:] not in sys.argv[2:]):
                continue
            figs = part[q["id"]].get("stepFigures") or []
            steps = q.get("stepByStep") or []
            print("## %s%s" % (q["id"], "" if len(figs) == len(steps) else "  LENGTH %d vs %d" % (len(figs), len(steps))))
            for i, s in enumerate(steps):
                fig = figs[i] if i < len(figs) else None
                print("  s%d: %s" % (i, s.get("text", "").replace("\n", " / ")))
                print("      -> %s" % ((fig.get("note") or fig["kind"]) if fig else "-"))
        sys.exit(0)
    want = sys.argv[1:] or YEARS
    for q in load():
        if q["source"][-4:] not in want:
            continue
        print("## %s [%s] ans=%s" % (q["id"], q.get("subTopic", ""), q["correctAnswer"]))
        print("Q: " + q["questionText"].replace("\n", " / "))
        print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
        for i, s in enumerate(q.get("stepByStep") or []):
            print("  s%d: %s" % (i, s.get("text", "").replace("\n", " / ")))
        print()
