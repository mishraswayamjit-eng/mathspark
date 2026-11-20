"""Build data/teach/parts/g4-gr4_numbers.json: lessons for every Grade 4 "numbers" question.

    python -X utf8 scripts/teach/gen/g4_gr4_numbers.py

Families by rule (g4_gr4_numbers_rules.py); everything else written per question in the
g4_gr4_numbers_a*.py files. Only lessons that pass the checker are written.
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from g4_gr4_numbers_lib import build, questions, write_part  # noqa: E402
from g4_gr4_numbers_rules import rule_lessons  # noqa: E402

AUTHORED = ["g4_gr4_numbers_a1", "g4_gr4_numbers_a2", "g4_gr4_numbers_a3", "g4_gr4_numbers_a4",
            "g4_gr4_numbers_a5", "g4_gr4_numbers_a6"]


def main():
    qs = questions("gr4_numbers")
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
    write_part("gr4_numbers", lessons)


if __name__ == "__main__":
    main()
