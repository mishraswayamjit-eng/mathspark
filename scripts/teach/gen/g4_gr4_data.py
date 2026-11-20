"""Build data/teach/parts/g4-gr4_data.json: a lesson for every Grade 4 data handling question.

    python -X utf8 scripts/teach/gen/g4_gr4_data.py

Generated families (ids VAR_..., BOOST_...) get their lesson from g4_gr4_data_rules.py.
Every other question has a lesson written for it in g4_gr4_data_a.py, _b.py, ...
(each has a dict L: question id -> list of beats).
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g4_gr4_time_lib import write_part, topic_questions  # noqa: E402
import g4_gr4_data_rules as rules  # noqa: E402

HELPERS = ["g4_gr4_data_a", "g4_gr4_data_b", "g4_gr4_data_c", "g4_gr4_data_d", "g4_gr4_data_e", "g4_gr4_data_f"]
GENERATED = ("VAR_", "VAR2_", "BOOST_", "PH3_")


def main():
    lessons = {}
    for q in topic_questions("gr4_data"):
        if q["id"].startswith(GENERATED):
            beats = rules.lesson_for(q)
            if beats:
                lessons[q["id"]] = ("rule", beats)
    for name in HELPERS:
        if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), name + ".py")):
            continue
        mod = importlib.import_module(name)
        for qid, beats in mod.L.items():
            if qid in lessons:
                sys.exit("two lessons for %s" % qid)
            lessons[qid] = ("authored", beats)
    write_part("gr4_data", lessons)


if __name__ == "__main__":
    main()
