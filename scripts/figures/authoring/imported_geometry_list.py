"""List the imported Grade 5 geometry questions (area, angles, triangles), for authoring.
    python -X utf8 scripts/figures/authoring/imported_geometry_list.py [node] [start] [end]
node: gr5_area | gr5_angles | gr5_triangles | all
"""
import os, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402

NODES = ("gr5_area", "gr5_angles", "gr5_triangles")
SOURCES = ("ai_generated", "ipm_textbook", "official_ipm_2020")


def load(node="all"):
    qs = bank.load_bank(5)
    nodes = NODES if node == "all" else (node,)
    out = [q for q in qs if q.get("node") in nodes and q.get("source") in SOURCES]
    out.sort(key=lambda q: (NODES.index(q["node"]), q["id"]))
    return out


if __name__ == "__main__":
    node = sys.argv[1] if len(sys.argv) > 1 else "all"
    qs = load(node)
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    b = int(sys.argv[3]) if len(sys.argv) > 3 else len(qs)
    print("%d questions" % len(qs))
    for q in qs[a:b]:
        print("## %s [%s | %s | %s] ans=%s" % (q["id"], q["node"], q.get("subTopic", ""), q["source"], q["correctAnswer"]))
        print("Q: " + q["questionText"].replace("\n", " / "))
        print("O: " + " | ".join("%s) %s" % (o["id"], o["text"]) for o in q["options"]))
        for i, s in enumerate(q.get("stepByStep") or []):
            print("  s%d: %s" % (i, s.get("text", "").replace("\n", " / ")))
