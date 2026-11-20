"""Build data/teach/parts/g4-gr4_squares.json: lessons for every Grade 4 "squares" question.

    python -X utf8 scripts/teach/gen/g4_gr4_squares.py

Families by rule (g4_gr4_squares_rules.py); everything else written per question in the
g4_gr4_squares_a*.py files. The authoring kit is shared with gr4_numbers (g4_gr4_numbers_lib.py).
Only lessons that pass the checker are written.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from g4_gr4_numbers_lib import build, questions, write_part  # noqa: E402
from g4_gr4_squares_rules import rule_lessons  # noqa: E402

AUTHORED = ["g4_gr4_squares_a1", "g4_gr4_squares_a2", "g4_gr4_squares_a3", "g4_gr4_squares_a4", "g4_gr4_squares_a5"]


def main():
    qs = questions("gr4_squares")
    lessons = rule_lessons(qs)
    for name in AUTHORED:
        if not os.path.exists(os.path.join(HERE, name + ".py")):
            continue
        mod = importlib.import_module(name)
        for qid, beats in mod.L.items():
            assert qid not in lessons, qid
            if isinstance(beats, dict):
                lessons[qid] = build(qid, beats["beats"], check=beats.get("check"))
            else:
                lessons[qid] = build(qid, beats)
    write_part("gr4_squares", lessons)


if __name__ == "__main__":
    main()
