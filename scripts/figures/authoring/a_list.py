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
