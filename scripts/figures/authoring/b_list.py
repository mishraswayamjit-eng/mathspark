"""List the Grade 5 past-paper questions of one year (Past papers B helper).

    python -X utf8 scripts/figures/authoring/b_list.py 2021
"""
import io, json, os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
with io.open(os.path.join(ROOT, "data", "mathspark_complete_seed.json"), encoding="utf-8") as f:
    qs = json.load(f)["questions"]
years = sys.argv[1:] or ["2021", "2022", "2023", "2024", "2025"]
for y in years:
    for q in qs:
        if q.get("topicId") == "grade5" and q.get("source") == "g5_final_" + y:
            print("### %s [%s] ans=%s" % (q["id"], q.get("subTopic", ""), q.get("correctAnswer")))
            print("Q:", q["questionText"].replace("\n", " / "))
            print("O:", " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
            for i, s in enumerate(q.get("stepByStep") or []):
                print("  s%d: %s" % (i, s.get("text", "").replace("\n", " / ")))
