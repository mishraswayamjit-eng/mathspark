"""Print the built part beside each question's steps, for reading through by eye.
    python -X utf8 scripts/figures/authoring/imported_geometry_review.py [node] [start] [end]
"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import imported_geometry_list as listing  # noqa: E402

PART = os.path.join(ROOT, "data", "question-figures", "parts", "imported-geometry.json")


def brief(fig):
    if fig is None:
        return "-"
    f = dict(fig)
    kind = f.pop("kind")
    note = f.pop("note", None)
    f.pop("points", None)
    f.pop("proportion", None)
    body = json.dumps(f, ensure_ascii=False, separators=(",", ":"))
    body = body.replace('"label":', "").replace('"size":', "~").replace("null,", "").replace("null", "")
    return "%s %s%s" % (kind, body, ("  « %s »" % note) if note else "")


if __name__ == "__main__":
    with io.open(PART, encoding="utf-8") as f:
        part = json.load(f)
    node = sys.argv[1] if len(sys.argv) > 1 else "all"
    qs = listing.load(node)
    a = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    b = int(sys.argv[3]) if len(sys.argv) > 3 else len(qs)
    for q in qs[a:b]:
        e = part.get(q["id"])
        if e is None:
            continue
        answer = next(o["text"] for o in q["options"] if o["id"] == q["correctAnswer"])
        print("## %s  ans=%s" % (q["id"][13:28], answer))
        print("Q: " + q["questionText"].replace("\n", " ")[:230])
        print("  BEFORE: " + brief(e.get("figure")))
        figs = e.get("stepFigures") or [None] * len(q["stepByStep"])
        for i, s in enumerate(q["stepByStep"]):
            if figs[i] is not None:
                print("  s%d %s" % (i, s["text"].replace("\n", " ")[:110]))
                print("     => " + brief(figs[i]))
