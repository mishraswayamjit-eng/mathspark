"""Write data/teach/parts/g4-gr4_ages.json: a lesson for every gr4_ages question.

    python -X utf8 scripts/teach/gen/g4_gr4_ages.py

Generated families are written by rule (g4_gr4_ages_rules.py); every other question
has its own lesson in g4_gr4_ages_a.py ... _d.py. Shared helpers: g4_gr4_ratio_lib.py.
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_ratio_lib import build, questions  # noqa: E402
from g4_gr4_ages_rules import by_rule  # noqa: E402

TOPIC = "gr4_ages"
AUTHORED = ["g4_gr4_ages_a", "g4_gr4_ages_b", "g4_gr4_ages_c", "g4_gr4_ages_d"]
GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")


def main():
    lessons = {}
    for q in questions(TOPIC):
        if q["id"].startswith(GENERATED):
            made = by_rule(q)
            if made:
                lessons[q["id"]] = made
            else:
                print("no rule for %s: %s" % (q["id"], q["questionText"]))
    for name in AUTHORED:
        if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py")):
            lessons.update(importlib.import_module(name).LESSONS)
    build(TOPIC, lessons)


if __name__ == "__main__":
    main()
