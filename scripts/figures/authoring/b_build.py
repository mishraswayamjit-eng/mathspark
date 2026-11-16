"""Merge b_2021.py ... b_2025.py (each defines ENTRIES) into the part file.

    python -X utf8 scripts/figures/authoring/b_build.py
"""
import importlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "data", "question-figures", "parts", "finals-2021-2025.json")
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

# Set to True to print every step next to its figure's note (for a read-through
# after the question bank changes). Leave False for a normal build.
REVIEW = False

merged = {}
for year in ("2021", "2022", "2023", "2024", "2025"):
    if not os.path.exists(os.path.join(HERE, "b_%s.py" % year)):
        continue
    part = importlib.import_module("b_" + year).ENTRIES
    for qid, e in part.items():
        assert qid not in merged and ("_FP_%s_" % year) in qid, qid
        merged[qid] = e
    print(year, len(part))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(merged, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote", len(merged), "entries")

# Show the current steps of any question whose stepFigures no longer line up,
# so the figures can be rewritten against the question as it now stands.
sys.path.append(os.path.join(ROOT, "scripts", "bank"))
import bank  # noqa: E402  (scripts/bank/bank.py: the question bank, data/bank/)
seed = bank.load_by_id()
for qid in sorted(merged):
    q = seed.get(qid)
    figs = merged[qid].get("stepFigures")
    if q is None or figs is None:
        continue
    own = q.get("stepByStep") or []
    if REVIEW and len(own) == len(figs):
        # Side by side: each step as it now reads, and what its figure says.
        print("\n%s" % qid[-8:])
        for i, s in enumerate(own):
            f_ = figs[i]
            says = "-" if f_ is None else "%s | %s" % (f_["kind"], f_.get("note", ""))
            print("  s%d: %s\n      => %s" % (i, s.get("text", ""), says))
    if len(own) != len(figs):
        print("\nREALIGN %s: %d step figures, %d steps" % (qid, len(figs), len(own)))
        print("  Q:", q["questionText"])
        for i, s in enumerate(own):
            print("  s%d: %s" % (i, s.get("text", "")))
